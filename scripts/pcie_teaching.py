#!/usr/bin/env python3
"""Render authored PCIe reading guides with native HTML controls (no JavaScript).

The author chooses the diagram and its technical sequence. This helper only joins
named SVG targets to visible explanations; it does not infer protocol behavior.
Use ``python scripts/pcie_teaching.py guide.json > guide.html`` or import render_walk.
The JSON keys match render_walk; steps/components are lists of dictionaries.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from typing import Iterable, Mapping
import xml.etree.ElementTree as ET

MAX_STEPS = 8
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
IDENTIFIER = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")


@dataclass
class Element:
    tag: str
    attrs: dict[str, str | None]
    children: list[Element | str] = field(default_factory=list)
    parent: Element | None = field(default=None, repr=False)

    def has_class(self, name: str) -> bool:
        return name in (self.attrs.get("class") or "").split()

    def descendants(self, tag: str | None = None) -> Iterable[Element]:
        for child in self.children:
            if isinstance(child, Element):
                if tag is None or child.tag == tag:
                    yield child
                yield from child.descendants(tag)

    def text(self) -> str:
        return " ".join(" ".join(x.text() if isinstance(x, Element) else x for x in self.children).split())


class Tree(HTMLParser):
    """Small HTML tree for structural checks; not a browser/layout substitute."""

    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.root = Element("document", {})
        self.stack = [self.root]
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = Element(tag, dict(attrs), parent=self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


@dataclass(frozen=True)
class WalkStep:
    title: str
    html: str
    targets: tuple[str, ...]
    condition_html: str
    source_html: str
    claim_ids: tuple[str, ...]


@dataclass(frozen=True)
class WalkComponent:
    target: str
    title: str
    html: str
    basic_html: str


def _identifier(value: str, context: str) -> None:
    if not IDENTIFIER.fullmatch(value):
        raise ValueError(f"{context}: use a letter followed by ASCII letters, numbers, '_' or '-': {value!r}")


def _visible_html(value: str, context: str) -> None:
    if not value or not Tree(value).root.text():
        raise ValueError(f"{context}: visible text is required")


def render_walk(*, walk_id: str, title: str, svg: str,
                steps: Iterable[WalkStep | Mapping], caption_html: str,
                order_html: str, components: Iterable[WalkComponent | Mapping] = (),
                language: str = "zh", summary_html: str = "") -> str:
    """Build one guide. SVG groups use ``data-walk-target="stable-name"``.

    All explanations stay visible. Inputs only select a highlight, and native
    radio keyboard navigation works without scripting. Conditions and citations
    are authored prose, not generated assertions. SVG title/desc IDs must already
    be unique within the page. Include teaching.css via the normal course builder.
    """
    _identifier(walk_id, "walk_id")
    if language not in {"zh", "en"}:
        raise ValueError("language must be 'zh' or 'en'")
    steps = [s if isinstance(s, WalkStep) else WalkStep(**s) for s in steps]
    components = [c if isinstance(c, WalkComponent) else WalkComponent(**c) for c in components]
    if not 1 <= len(steps) <= MAX_STEPS:
        raise ValueError(f"A guide needs 1–{MAX_STEPS} authored steps")
    for value, context in [(title, "title"), (caption_html, "caption"), (order_html, "order")]:
        _visible_html(value, context)
    if summary_html:
        _visible_html(summary_html, "summary")
    memberships: dict[str, list[str]] = {}
    for index, step in enumerate(steps, 1):
        for key in ("title", "html", "condition_html", "source_html"):
            _visible_html(getattr(step, key), f"Step {index} {key}")
        if not step.targets or len(set(step.targets)) != len(step.targets):
            raise ValueError(f"Step {index}: targets must be a nonempty list without duplicates")
        if not step.claim_ids or len(set(step.claim_ids)) != len(step.claim_ids):
            raise ValueError(f"Step {index}: claim_ids must be nonempty without duplicates")
        for claim in step.claim_ids:
            _identifier(claim, f"Step {index} claim")
        for target in step.targets:
            _identifier(target, f"Step {index} target")
            memberships.setdefault(target, []).append(str(index))
    try:
        root = ET.fromstring(svg)
    except ET.ParseError as error:
        raise ValueError(f"SVG is not well-formed XML: {error}") from error
    if root.tag != "svg":
        raise ValueError("Provide an inline <svg> without a namespace prefix")
    nodes = {}
    for node in root.iter():
        target = node.get("data-walk-target")
        if target:
            _identifier(target, "SVG target")
            if target in nodes:
                raise ValueError(f"Duplicate SVG target: {target}")
            nodes[target] = node
    if set(nodes) != set(memberships):
        raise ValueError(f"SVG targets must match the step targets: missing={sorted(set(memberships) - set(nodes))}, unused={sorted(set(nodes) - set(memberships))}")
    for target, node in nodes.items():
        classes = set(node.get("class", "").split()) | {"walk-node"}
        node.set("class", " ".join(sorted(classes)))
        node.set("data-walk-steps", " ".join(memberships[target]))
    component_ids = set()
    for component in components:
        if component.target not in nodes or component.target in component_ids:
            raise ValueError(f"Component target must identify one unique diagram node: {component.target}")
        component_ids.add(component.target)
        for key in ("title", "html", "basic_html"):
            _visible_html(getattr(component, key), f"Component {component.target} {key}")
        node = nodes[component.target]
        parent = next((p for p in root.iter() if node in list(p)), None)
        if parent is None or parent.tag == "a" or any(c.tag == "a" for c in node.iter()):
            raise ValueError(f"Component {component.target}: target must allow a non-nested SVG link")
        link = ET.Element("a", {"href": f"#{walk_id}-component-{component.target}", "aria-label": component.title})
        position = list(parent).index(node)
        parent.remove(node)
        link.append(node)
        parent.insert(position, link)
    e = html.escape
    is_en = language == "en"
    instruction = ("Select a step to highlight its part of the diagram. The full diagram and all explanations remain visible. Use the arrow keys within the step controls."
                   if is_en else "選擇步驟後，圖中對應的元件與下方解說會加上重點標示。完整圖與所有解說會持續顯示；也可用方向鍵切換步驟。")
    out = [f'<div class="guided-walk" id="{e(walk_id)}" role="group" aria-labelledby="{e(walk_id)}-title" data-walk-version="1">',
           f'<h3 id="{e(walk_id)}-title">{e(title)}</h3>',
           f'<p class="walk-help" id="{e(walk_id)}-help">{instruction}</p>',
           f'<div class="walk-order">{order_html}</div>']
    for index, step in enumerate(steps, 1):
        checked = ' checked="checked"' if index == 1 else ""
        out.append(f'<input class="walk-choice" type="radio" name="{e(walk_id)}-step" id="{e(walk_id)}-choice-{index}" value="{index}" data-walk-step="{index}" aria-describedby="{e(walk_id)}-help" aria-controls="{e(walk_id)}-view {e(walk_id)}-step-{index}"{checked}>')
        out.append(f'<label class="walk-label" for="{e(walk_id)}-choice-{index}">{index}. {e(step.title)}</label>')
    out.extend([f'<div class="walk-view" id="{e(walk_id)}-view">', '<figure class="diagram walk-diagram">',
                ET.tostring(root, encoding="unicode"), f'<figcaption>{caption_html}</figcaption></figure>'])
    if summary_html:
        out.append(f'<div class="walk-summary">{summary_html}</div>')
    out.append('<ol class="walk-steps">')
    for index, step in enumerate(steps, 1):
        out.append(f'<li class="walk-step" id="{e(walk_id)}-step-{index}" data-walk-step="{index}" data-walk-targets="{e(" ".join(step.targets))}"><h4>{e(step.title)}</h4><div class="walk-condition">{step.condition_html}</div><div class="walk-explanation">{step.html}</div><div class="walk-source" data-source-claims="{e(" ".join(step.claim_ids))}">{step.source_html}</div></li>')
    out.append('</ol></div>')
    if components:
        heading = "Diagram components" if is_en else "圖中元件"
        basic = "Basic responsibility" if is_en else "基本責任"
        out.append(f'<div class="walk-components"><h4>{heading}</h4><ul class="walk-component-links">')
        for component in components:
            out.append(f'<li><a href="#{e(walk_id)}-component-{e(component.target)}">{e(component.title)}</a></li>')
        out.append('</ul>')
        for component in components:
            out.append(f'<section class="walk-component" id="{e(walk_id)}-component-{e(component.target)}" data-component-target="{e(component.target)}"><h4>{e(component.title)}</h4><div class="walk-component-action">{component.html}</div><details><summary>{basic}</summary>{component.basic_html}</details></section>')
        out.append('</div>')
    out.append('</div>')
    result = "\n".join(out)
    # Keep the same checks available to direct imports and the JSON CLI.
    try:
        from .validate_pcie_teaching import validate_teaching
    except ImportError:
        from validate_pcie_teaching import validate_teaching
    errors = validate_teaching(result)
    if errors:
        raise ValueError("\n".join(errors))
    return result


WALK_REGION = re.compile(r'<!--\s*pcie-walk:\s*([^<>\r\n]+?)\s*-->[\s\S]*?<!--\s*/pcie-walk\s*-->')


def expand_walks(text: str, source_dir: Path) -> str:
    """Refresh paired authored regions from local walk JSON, preserving markers.

    Only files in source_dir/walks may be loaded; source PDFs and arbitrary local
    paths cannot be included by a marker. Dangling markers are authoring errors.
    """
    source_dir = Path(source_dir).resolve()
    walks_dir = (source_dir / 'walks').resolve()
    if len(re.findall(r'<!--\s*pcie-walk:', text)) != len(WALK_REGION.findall(text)) or len(re.findall(r'<!--\s*/pcie-walk\s*-->', text)) != len(WALK_REGION.findall(text)):
        raise ValueError('Each pcie-walk marker needs exactly one closing marker')

    def replace(match: re.Match) -> str:
        relative = match.group(1).strip()
        if '\\' in relative or ':' in relative:
            raise ValueError(f'Use a relative walks/*.json path: {relative}')
        candidate = (source_dir / relative).resolve()
        if not candidate.is_relative_to(walks_dir) or candidate.suffix != '.json':
            raise ValueError(f'Guide source must stay inside walks/: {relative}')
        data = json.loads(candidate.read_text(encoding='utf-8-sig'))
        rendered = render_walk(**data)
        return f'<!-- pcie-walk: {relative} -->\n{rendered}\n<!-- /pcie-walk -->'

    return WALK_REGION.sub(replace, text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 guide JSON, or authored HTML with --refresh-authored")
    parser.add_argument("--output", type=Path, help="Write the fragment instead of stdout")
    parser.add_argument("--refresh-authored", action="store_true", help="Refresh paired walk regions in an authored HTML file, in place")
    args = parser.parse_args()
    try:
        if args.refresh_authored:
            if args.output or args.input.suffix != '.html':
                parser.error('--refresh-authored requires an authored HTML file and no --output')
            authored = args.input.read_text(encoding='utf-8-sig')
            if not WALK_REGION.search(authored):
                parser.error('No paired pcie-walk region found in the authored HTML')
            result = expand_walks(authored, args.input.parent)
            if result != authored:
                args.input.write_text(result, encoding='utf-8', newline='\n')
            print(f'Refreshed authored guide regions: {args.input}')
            return 0
        result = render_walk(**json.loads(args.input.read_text(encoding="utf-8-sig"))) + "\n"
    except (ValueError, TypeError, OSError) as error:
        parser.error(str(error))
    if args.output:
        args.output.write_text(result, encoding="utf-8", newline="\n")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(result, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
