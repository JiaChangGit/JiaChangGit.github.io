#!/usr/bin/env python3
"""Build the PCIe course from authored HTML and its curriculum (stdlib only).

Run from any directory. --check validates all outputs without writing files.
The source PDFs are never copied or embedded in the generated course.
"""
from __future__ import annotations

import argparse
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".ai/pcie-course"
OUTPUT = ROOT / "DOCS/pcie-course"
DATE = "2026-10-19"
CHAPTER_DESCRIPTION = "先看懂 PCIe 在系統中的角色，再沿著 Capability、Figure、Table 與欄位，完成第一次連線速率查詢。"
E = html.escape
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class Document(HTMLParser):
    """Collect headings, anchors and offline/accessibility invariants."""

    def __init__(self, text: str) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, dict[str, str | None]]] = []
        self.ids: set[str] = set()
        self.hrefs: list[str] = []
        self.headings: list[tuple[str, str]] = []
        self.errors: list[str] = []
        self.heading_id: str | None = None
        self.heading_text: list[str] | None = None
        self.svg_labels: list[set[str]] = []
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag in {"script", "iframe", "object", "embed"}:
            self.errors.append(f"Forbidden offline element: {tag}")
        if tag == "link" and "stylesheet" in (attr.get("rel") or ""):
            self.errors.append("External stylesheets are not permitted")
        if tag in {"img", "image", "source", "video", "audio"}:
            self.errors.append(f"Use inline SVG rather than external media: {tag}")
        for key, value in attrs:
            if key.startswith("on"):
                self.errors.append(f"Event handler is not permitted: {key}")
            if key in {"href", "src"} and (value or "").strip().lower().startswith("javascript:"):
                self.errors.append("JavaScript URLs are not permitted")
        identifier = attr.get("id")
        if identifier:
            if identifier in self.ids:
                self.errors.append(f"Duplicate id: {identifier}")
            self.ids.add(identifier)
        if tag == "a" and attr.get("href"):
            self.hrefs.append(attr["href"])
        if tag == "h2":
            self.heading_id = identifier or next((a.get("id") for t, a in reversed(self.stack) if t == "section" and a.get("id")), None)
            self.heading_text = []
            if not self.heading_id:
                self.errors.append("Every h2 needs an id or a containing section id")
        if tag == "svg":
            self.svg_labels.append(set())
            if attr.get("role") != "img":
                self.errors.append("Inline SVG needs role=img")
        if tag in {"title", "desc"} and self.svg_labels:
            self.svg_labels[-1].add(tag)
        if tag not in VOID:
            self.stack.append((tag, attr))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == "h2" and self.heading_text is not None:
            if self.heading_id:
                self.headings.append((self.heading_id, " ".join("".join(self.heading_text).split())))
            self.heading_text = None
            self.heading_id = None
        if tag == "svg" and self.svg_labels:
            labels = self.svg_labels.pop()
            if labels != {"title", "desc"}:
                self.errors.append("Inline SVG needs both title and desc")
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        if self.heading_text is not None:
            self.heading_text.append(data)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def toc_for(body: str) -> str:
    doc = Document(body)
    if doc.errors:
        raise ValueError("\n".join(doc.errors))
    if not doc.headings:
        raise ValueError("Course content needs at least one h2")
    return "<ol>" + "".join(f'<li><a href="#{E(identifier)}">{E(title)}</a></li>' for identifier, title in doc.headings) + "</ol>"


def render(template: str, css: str, *, title: str, description: str, eyebrow: str,
           body: str, is_index: bool = False, chapter_number: int | None = None,
           ready_numbers: list[int] | None = None, edition_date: str = DATE) -> str:
    if is_index:
        top_links = '<a href="chapter-0.html">開始 Chapter 0</a>'
        bottom_links = '<a href="chapter-0.html">開始閱讀 Chapter 0 →</a><a href="#content">回到導讀</a>'
    else:
        top_links = '<a href="index.html">課程總覽</a>'
        ready_numbers = ready_numbers or []
        position = ready_numbers.index(chapter_number)
        links = ['<a href="index.html">課程總覽</a>']
        if position:
            previous = ready_numbers[position - 1]
            links.append(f'<a href="chapter-{previous}.html">← Chapter {previous}</a>')
        if position + 1 < len(ready_numbers):
            following = ready_numbers[position + 1]
            links.append(f'<a href="chapter-{following}.html">Chapter {following} →</a>')
        links.append('<a href="#content">回到本章開頭 ↑</a>')
        bottom_links = ''.join(links)
    values = {
        "title": E(title), "description": E(description), "eyebrow": E(eyebrow),
        "css": css.rstrip(), "body": body.strip(), "toc": toc_for(body), "editiondate": E(edition_date),
        "toclabel": "課程導讀" if is_index else "本章閱讀路徑",
        "toplinks": top_links,
        "bottomnav": '<nav class="bottom-nav" aria-label="下一步">' + bottom_links + '</nav>',
    }
    return re.sub(r"\{\{([a-z]+)\}\}", lambda match: values[match.group(1)], template).rstrip() + "\n"


def curriculum_body(curriculum: dict) -> str:
    chapters = curriculum["chapters"]
    numbers = [chapter["number"] for chapter in chapters]
    if len(numbers) != len(set(numbers)) or 0 not in numbers:
        raise ValueError("Curriculum needs unique chapter numbers including Chapter 0")
    if any(chapter["status"] not in {"ready", "planned"} for chapter in chapters):
        raise ValueError("Unknown curriculum status")
    ready = [chapter['number'] for chapter in chapters if chapter['status'] == 'ready']
    if 0 not in ready:
        raise ValueError('Chapter 0 must be ready before publishing the course')
    completed = '、'.join(f'Chapter {number}' for number in ready)
    cards = []
    for chapter in chapters:
        number = chapter["number"]
        ready = chapter["status"] == "ready"
        title = chapter["title"]
        heading = f'<a href="chapter-{number}.html">{E(title)}</a>' if ready else E(title)
        prerequisites = chapter.get("prerequisites", [])
        if any(item not in numbers for item in prerequisites):
            raise ValueError(f"Unknown prerequisite in Chapter {number}")
        prerequisite_text = "、".join(f"Chapter {item}" for item in prerequisites) if prerequisites else "基本程式與 CPU／記憶體概念；不需要 PCIe 經驗"
        topics = "".join(f"<li>{E(topic)}</li>" for topic in chapter["topics"])
        cards.append(
            f'<article class="chapter-card {"ready" if ready else "planned"}" id="chapter-{number}">'
            f'<div class="chapter-meta"><span>CHAPTER {number}</span><span class="status">{"已完成 · 可閱讀" if ready else "規劃中 · 尚未撰寫"}</span></div>'
            f'<h3>{heading}</h3><p class="chapter-question">{E(chapter["question"])}</p>'
            f'<ul>{topics}</ul><p class="prerequisites"><strong>先備知識：</strong>{E(prerequisite_text)}</p></article>'
        )
    return '\n'.join([
        '<section id="start"><h2>先把系統看懂，再深入各領域</h2>',
        '<p class="lead">這套課程從裝置在系統裡的角色出發。先理解軟體為什麼要查這個欄位，再沿著規格找出答案，逐步走進裝置發現、資源配置、傳輸與系統管理。</p>',
        f'<p>目前可以完整閱讀 {completed}。下列其他章節是後續課程規劃，尚未完成教材；章節主題與順序仍可能隨來源查證結果調整。</p>',
        '<p><a class="start-link" href="chapter-0.html">從 Chapter 0 開始 →</a></p></section>',
        '<section id="method"><h2>讀情境，也讀推理過程</h2>',
        '<p>每個情境先說明需求、對象與前提，再帶讀者找到規格中的結構、欄位及適用條件。案例會明確標示假設讀值，解答則說明能得到什麼結論，以及還缺哪些證據。</p>',
        '<ul><li><strong>先想，再看答案：</strong>正文以問題串起解說，章末再用不同情境檢查理解。</li><li><strong>同一觀念集中說明：</strong>後續章節連回先備知識，再加入新的條件與判斷。</li><li><strong>依問題安排閱讀順序：</strong>Figure、Table 與條文按查詢需求串接，不要求依文件頁碼順讀。</li></ul></section>',
        '<section id="curriculum"><h2>課程安排</h2><p>章號提供一條漸進的閱讀路徑；已有相關基礎時，也可以依各章的先備知識選擇切入點。</p>',
        '<div class="chapter-list">' + '\n'.join(cards) + '</div></section>',
        '<section id="versions"><h2>版本與來源怎麼讀？</h2>',
        '<p>目前已完成章節的欄位與圖表以 <strong>PCI Express Base Specification Revision 6.0</strong> 為準，韌體背景另參考 <strong>PCI Firmware Specification Revision 3.3</strong>。Firmware 3.3 列出的 Base 參考版本為 5.0，因此教材逐項保留來源版本，不把兩份文件當成同版配套。</p>',
        '<p>章內引用會列出章節、適用的 Figure／Table 與頁碼。補充資料標明來源及版本；作者設計的配置、讀值與推演也會另行標示。後續進階章節若需要其他規格，會在完成查證後再納入教材。</p>',
        '<p><a href="chapter-0.html#sources">查看 Chapter 0 的來源與版本說明 →</a></p></section>',
    ])


def post(css: str, body: str, language: str, chapter: dict) -> str:
    is_zh = language == "zh"
    slug = "zh-tw" if is_zh else "en"
    number = chapter['number']
    english_title = chapter.get('title_en')
    if number == 0 and not english_title:
        english_title = 'From the System View to Your First Specification Query'
    if not english_title:
        raise ValueError(f'Missing title_en for Chapter {number}')
    title = f"PCIe Chapter {number}：" + chapter['title'] if is_zh else f"PCIe Chapter {number}: " + english_title
    scoped_css = css.replace(".pcie-surface", ".pcie-article")
    # Blog readers select their theme through html[data-theme]. Following the
    # operating-system preference here would put light text on the blog's white
    # background when the two theme choices differ. Standalone pages keep the
    # original prefers-color-scheme behavior.
    scoped_css = re.sub(
        r'@media \(prefers-color-scheme: dark\) \{\n(.*?)\n\}',
        lambda match: match.group(1).replace('.pcie-article', 'html[data-theme="dark"] .pcie-article'),
        scoped_css, flags=re.S,
    )
    scoped_css += '\nhtml:not([data-theme="dark"]) .pcie-article { color-scheme: light; }\nhtml[data-theme="dark"] .pcie-article { color-scheme: dark; }\n'
    # No unscoped selectors are introduced into the surrounding Jekyll layout.
    scoped_css += "\n.pcie-article { background: transparent; margin: 1.5rem 0; }\n.pcie-article .lesson { padding: 0; border: 0; background: transparent; }\n"
    links = [('課程總覽' if is_zh else 'Course overview', '/DOCS/pcie-course/index.html'),
             ('繁中完整教學' if is_zh else 'Full Chinese tutorial', f'/DOCS/pcie-course/chapter-{number}.html'),
             ('English' if is_zh else '繁體中文', f'/pcie/chapter-{number}-en/' if is_zh else f'/pcie/chapter-{number}-zh-tw/')]
    navigation = '<nav class="bottom-nav" aria-label="' + ('課程與語言版本' if is_zh else 'Course and editions') + '">' + ''.join(f'<a href="{url}">{label}</a>' for label, url in links) + '</nav>'
    return '\n'.join([
        '---', 'layout: post', 'title: ' + json.dumps(title, ensure_ascii=False),
        'date: ' + chapter.get('publication_date', DATE) + ' 00:00:00 +0800', f'permalink: /pcie/chapter-{number}-' + slug + '/',
        'categories: [PCIe]', 'tags: [PCIe, Specification]', 'lang: ' + ('zh-TW' if is_zh else 'en'),
        '---', '', '<style>', scoped_css.rstrip(), '</style>',
        '<div class="pcie-article" lang="' + ('zh-Hant-TW' if is_zh else 'en') + '">',
        navigation, '<article class="lesson">', body.strip(), '</article>', navigation, '</div>', '',
    ])


def validate_outputs(outputs: dict[Path, str]) -> None:
    docs = {path: Document(text) for path, text in outputs.items()}
    errors = []
    for path, doc in docs.items():
        errors.extend(f'{path.relative_to(ROOT)}: {error}' for error in doc.errors)
        for href in doc.hrefs:
            if href.startswith('#') and href[1:] not in doc.ids:
                errors.append(f'{path.name}: missing anchor {href}')
            elif path.suffix == '.html' and not re.match(r'^(?:[a-z][a-z0-9+.-]*:|/|#)', href, re.I):
                target_name, _, fragment = href.partition('#')
                target = path.parent / target_name
                if target not in docs:
                    errors.append(f'{path.name}: missing offline target {href}')
                elif fragment and fragment not in docs[target].ids:
                    errors.append(f'{path.name}: missing target anchor {href}')
        if path.suffix == '.html':
            text = outputs[path]
            for required in ['lang="zh-Hant-TW"', 'viewport-fit=cover', 'class="skip-link"']:
                if required not in text:
                    errors.append(f'{path.name}: missing {required}')
            if len(re.findall(r'<style(?:\s|>)', text)) != 1:
                errors.append(f'{path.name}: expected one inline stylesheet')
        if re.search(r'@import\b|@font-face\b|url\s*\(', outputs[path], re.I):
            errors.append(f'{path.name}: CSS must not depend on external resources')
    if errors:
        raise ValueError('\n'.join(errors))


def build() -> dict[Path, str]:
    template = read(SOURCE / 'template.html')
    css = read(SOURCE / 'course.css')
    curriculum = json.loads(read(SOURCE / 'curriculum.json'))
    index_body = curriculum_body(curriculum)
    ready = sorted((chapter for chapter in curriculum['chapters'] if chapter['status'] == 'ready'),
                   key=lambda chapter: chapter['number'])
    ready_numbers = [chapter['number'] for chapter in ready]
    outputs = {
        OUTPUT / 'index.html': render(template, css, title=curriculum['title'], description=curriculum['description'],
                                     eyebrow='PCIe · 系統與規格閱讀 / COURSE GUIDE', body=index_body, is_index=True,
                                     edition_date=max(chapter.get('publication_date', DATE) for chapter in ready)),
    }
    for chapter in ready:
        number = chapter['number']
        body = read(SOURCE / f'chapter{number}.zh.html')
        description = chapter.get('description', CHAPTER_DESCRIPTION if number == 0 else chapter['question'])
        outputs[OUTPUT / f'chapter-{number}.html'] = render(
            template, css, title=chapter['title'], description=description,
            eyebrow=f'PCIe · 系統與規格閱讀 / CHAPTER {number}', body=body,
            chapter_number=number, ready_numbers=ready_numbers, edition_date=chapter.get('publication_date', DATE),
        )
        for language in ('zh', 'en'):
            source = SOURCE / (f'post.{language}.html' if number == 0 else f'chapter{number}.post.{language}.html')
            slug = 'zh-tw' if language == 'zh' else 'en'
            publication_date = chapter.get('publication_date', DATE)
            outputs[ROOT / f'_posts/{publication_date}-pcie-chapter-{number}-{slug}.md'] = post(css, read(source), language, chapter)
    validate_outputs(outputs)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check generated artifacts without changing files')
    args = parser.parse_args()
    try:
        outputs = build()
        changed = [path for path, text in outputs.items() if not path.exists() or read(path) != text]
        if args.check:
            if changed:
                print('Generated outputs are missing or out of date:', file=sys.stderr)
                for path in changed:
                    print('  ' + path.relative_to(ROOT).as_posix(), file=sys.stderr)
                return 1
            print(f'PCIe course check passed: {len(outputs)} outputs, offline dependencies and local links valid.')
            return 0
        for path in changed:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(outputs[path], encoding='utf-8', newline='\n')
            print('Wrote ' + path.relative_to(ROOT).as_posix())
        print(f'PCIe course built: {len(outputs)} outputs ({len(changed)} changed).')
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(f'PCIe course build failed: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
