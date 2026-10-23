#!/usr/bin/env python3
"""Validate inspectable links in PCIe guided diagrams, not learning or prose quality.

Checks controls, target membership, visible explanations/conditions/citations,
source claim IDs and SVG accessibility. A pass does not verify protocol sequence,
translation, source interpretation, layout, or whether a reader understands.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
from typing import Mapping

try:
    from .pcie_teaching import Element, MAX_STEPS, Tree, expand_walks
except ImportError:
    from pcie_teaching import Element, MAX_STEPS, Tree, expand_walks

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".ai/pcie-course"


def _class_nodes(node: Element, name: str) -> list[Element]:
    return [child for child in node.descendants() if child.has_class(name)]


def _is_visible(node: Element, stop: Element) -> bool:
    current = node
    while current is not None:
        style = current.attrs.get("style") or ""
        if ("hidden" in current.attrs or current.attrs.get("aria-hidden") == "true"
                or re.search(r"(?:display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0(?:\D|$))", style, re.I)
                or current.tag == "details" and "open" not in current.attrs):
            return False
        if current is stop:
            return True
        current = current.parent
    return False


def validate_teaching(text: str, claims: Mapping[str, dict] | set[str] | None = None,
                      *, require_walk: bool = False) -> list[str]:
    """Return structural errors. ``claims=None`` checks structure without registry lookup."""
    document = Tree(text).root
    all_nodes = list(document.descendants())
    walks = [node for node in all_nodes if node.has_class("guided-walk")]
    errors = []
    if require_walk and not walks:
        errors.append("No guided-walk found")
    # Duplicate IDs elsewhere can break SVG labels or fragment navigation too.
    ids = Counter(node.attrs["id"] for node in all_nodes if node.attrs.get("id"))
    errors.extend(f"Duplicate document id: {identifier}" for identifier, count in ids.items() if count > 1)
    by_id = {node.attrs["id"]: node for node in all_nodes if node.attrs.get("id")}
    radio_names: set[str] = set()
    for walk_index, walk in enumerate(walks, 1):
        label = walk.attrs.get("id") or f"guide #{walk_index}"

        def need(condition, message):
            if not condition:
                errors.append(f"{label}: {message}")

        need(walk.attrs.get("id"), "guide needs a unique id")
        need(walk.attrs.get("data-walk-version") == "1", "unsupported or missing data-walk-version")
        need(not _class_nodes(walk, "guided-walk"), "nested guides are not supported")
        heading = by_id.get(walk.attrs.get("aria-labelledby"))
        need(walk.attrs.get("role") == "group" and heading is not None and heading.text(), "guide needs a named group")
        for node in walk.descendants():
            need(node.tag not in {"script", "iframe", "object", "embed", "style", "link", "image", "img", "audio", "video", "source"}, f"unsupported active/external element: {node.tag}")
            for key, value in node.attrs.items():
                need(not key.startswith("on"), f"event handler forbidden: {key}")
                if key in {"href", "src", "xlink:href"}:
                    need(not re.match(r"\s*(?:javascript|data):", value or "", re.I), "active URL forbidden")
                    if value and value.startswith("#"):
                        need(value[1:] in by_id, f"fragment target missing: {value}")
        orders = _class_nodes(walk, "walk-order")
        need(len(orders) == 1 and orders[0].text() and _is_visible(orders[0], walk), "one visible reading-order explanation is required")
        controls = _class_nodes(walk, "walk-choice")
        steps = _class_nodes(walk, "walk-step")
        need(1 <= len(steps) <= MAX_STEPS, f"use 1–{MAX_STEPS} steps")
        expected = [str(index) for index in range(1, len(steps) + 1)]
        need([step.attrs.get("data-walk-step") for step in steps] == expected, "step identifiers must follow the authored reading order")
        need([control.attrs.get("data-walk-step") for control in controls] == expected, "every step needs its own matching control")
        names = {control.attrs.get("name") for control in controls}
        need(len(names) == 1 and None not in names and "" not in names, "controls must share one nonempty radio group name")
        need(not names.intersection(radio_names), "radio group name reused by another guide")
        radio_names.update(name for name in names if name)
        need(sum("checked" in control.attrs for control in controls) == 1, "exactly one step must be initially selected")
        views = _class_nodes(walk, "walk-view")
        need(len(views) == 1 and views[0].parent is walk, "one direct-child walk-view is required by the CSS contract")
        view = views[0] if len(views) == 1 else None
        direct = [node for node in walk.children if isinstance(node, Element)]
        for number, control in enumerate(controls):
            need(control.tag == "input" and control.attrs.get("type") == "radio", "step controls must be native radio inputs")
            need(control.parent is walk and "disabled" not in control.attrs and control.attrs.get("tabindex") != "-1" and _is_visible(control, walk), "a step control is unavailable to native keyboard navigation")
            identifier = control.attrs.get("id")
            matches = [node for node in walk.descendants("label") if node.attrs.get("for") == identifier and node.has_class("walk-label")]
            need(identifier and len(matches) == 1 and matches[0].text(), "each control needs exactly one descriptive label")
            if control in direct:
                position = direct.index(control)
                need(position + 1 < len(direct) and direct[position + 1] in matches, "control label must immediately follow its input for highlight styling")
                need(view in direct and direct.index(view) > position, "walk-view must follow all controls for highlight styling")
            if view and number < len(steps):
                needs = {view.attrs.get("id"), steps[number].attrs.get("id")}
                need(None not in needs and needs <= set((control.attrs.get("aria-controls") or "").split()), "control must identify the diagram and its matching explanation")
        svgs = list(view.descendants("svg")) if view else []
        need(len(svgs) == 1, "one complete SVG is required")
        targets: dict[str, Element] = {}
        if len(svgs) == 1:
            svg = svgs[0]
            need(svg.attrs.get("role") == "img" and svg.attrs.get("viewbox"), "SVG needs role=img and a viewBox")
            accessible = set((svg.attrs.get("aria-labelledby") or "").split())
            for tag in ("title", "desc"):
                nodes = list(svg.descendants(tag))
                need(len(nodes) == 1 and nodes[0].text() and nodes[0].attrs.get("id") in accessible, f"SVG needs one labelled, nonempty {tag}")
            for node in svg.descendants():
                target = node.attrs.get("data-walk-target")
                if target:
                    need(target not in targets, f"duplicate diagram target: {target}")
                    targets[target] = node
                    need(node.has_class("walk-node"), f"target {target} is not styled as a walk-node")
        expected_memberships: dict[str, set[str]] = {}
        for step in steps:
            number = step.attrs.get("data-walk-step")
            members = (step.attrs.get("data-walk-targets") or "").split()
            need(members and len(set(members)) == len(members), f"step {number} needs unique target identifiers")
            for target in members:
                need(target in targets, f"step {number} points to missing diagram target: {target}")
                expected_memberships.setdefault(target, set()).add(number)
            need(view is not None and step in list(view.descendants()), f"step {number} must be in walk-view")
            for category in ("walk-condition", "walk-explanation", "walk-source"):
                regions = _class_nodes(step, category)
                need(len(regions) == 1 and regions[0].text() and _is_visible(regions[0], walk), f"step {number} needs one visible {category}")
                if category == "walk-source" and len(regions) == 1:
                    references = (regions[0].attrs.get("data-source-claims") or "").split()
                    need(references and len(references) == len(set(references)), f"step {number} source needs unique claim references")
                    if claims is not None:
                        for claim in references:
                            need(claim in claims, f"step {number} references unknown source claim: {claim}")
        need(set(targets) == set(expected_memberships), "diagram and explanation target sets differ")
        for target, node in targets.items():
            membership = (node.attrs.get("data-walk-steps") or "").split()
            need(len(membership) == len(set(membership)) and set(membership) == expected_memberships.get(target, set()), f"highlight membership differs for target {target}")
        for component in _class_nodes(walk, "walk-component"):
            target = component.attrs.get("data-component-target")
            need(target in targets, f"component has no diagram target: {target}")
            actions = _class_nodes(component, "walk-component-action")
            need(len(actions) == 1 and actions[0].text() and _is_visible(actions[0], walk), f"component {target} needs a visible action explanation")
            details = list(component.descendants("details"))
            need(len(details) == 1 and any(x.tag == "summary" and x.text() for x in details[0].descendants()) and any(isinstance(x, Element) and x.tag != "summary" and x.text() for x in details[0].children), f"component {target} needs a basic-responsibility details section")
            href = f'#{component.attrs.get("id")}'
            links = [node for node in walk.descendants("a") if node.attrs.get("href") == href]
            need(len(links) >= 2, f"component {target} needs SVG and text navigation links")
            node = targets.get(target)
            need(node is not None and node.parent is not None and node.parent.tag == "a" and node.parent.attrs.get("href") == href, f"component {target} SVG link is disconnected")
    return errors


def load_claims(directory: Path) -> dict[str, dict]:
    claims = {}
    for path in sorted(directory.glob("*claims.json")):
        for claim in json.loads(path.read_text(encoding="utf-8-sig")).get("claims", []):
            claims[claim["id"]] = claim
    return claims


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="Authored or generated HTML files; default: all authored chapter editions")
    parser.add_argument("--claims-dir", type=Path, default=SOURCE)
    parser.add_argument("--require-walk", action="store_true", help="Require a guided diagram in each supplied file")
    args = parser.parse_args()
    paths = args.paths or sorted({*SOURCE.glob("chapter*.html"), *SOURCE.glob("post.*.html")})
    try:
        claims = load_claims(args.claims_dir)
        errors = []
        walks = 0
        for path in paths:
            text = path.read_text(encoding="utf-8-sig")
            if "pcie-walk:" in text:
                expanded = expand_walks(text, SOURCE)
                if expanded != text:
                    errors.append(f"{path}: authored guided diagram differs from its JSON; regenerate its pcie-walk block")
            walks += len(_class_nodes(Tree(text).root, "guided-walk"))
            errors.extend(f"{path}: {error}" for error in validate_teaching(text, claims, require_walk=args.require_walk))
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Checked {len(paths)} documents, {walks} guided diagrams and {len(claims)} registered claims. Structural checks passed; technical meaning, prose and layout still require review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
