"""Answered review questions generated from paired, source-located teaching data."""
from __future__ import annotations

import html
import re


def question_bank(report_id, modules):
    """Keep questions, answers, examples, and citations paired before rendering."""
    result = []
    for module in modules:
        for kind, zh, en in [
            ("lead", "「{title}」的核心判讀規則是什麼？", "What is the governing interpretation for “{title}”?"),
            ("rows", "「{title}」中，哪些概念或條件必須分開比較？", "Which concepts or conditions must be distinguished in “{title}”?"),
            ("example", "「{title}」如何套用到具體數值或操作情境？", "How does “{title}” apply to a concrete calculation or operational scenario?"),
            ("pitfall", "「{title}」最容易出現什麼誤判？如何排查？", "What misinterpretation is most likely in “{title}”, and how is it debugged?"),
        ]:
            answers = {}
            for lang in ("zh", "en"):
                answers[lang] = (
                    "\n".join(" — ".join(row) for row in module["rows"][lang])
                    if kind == "rows" else module[kind][lang]
                )
            result.append(dict(
                id=f"{report_id}-{module['id']}-{kind}",
                question={"zh": zh.format(title=module["title"]["zh"]), "en": en.format(title=module["title"]["en"])},
                answer=answers, sources=module["sources"], informative=kind in {"example", "pitfall"},
            ))
    return result


def render_questions(report_id, modules, claims, language, fmt):
    bank = question_bank(report_id, modules)
    by_id = {item["id"]: item for item in claims}
    heading = "Self-questions and worked answers" if language == "en" else "自問自答：規則、比較、案例與排錯"
    intro = (
        f"{len(bank)} answered questions revisit this report's scope. Each answer retains the same source links as the teaching module; calculations and debugging examples are informative."
        if language == "en" else
        f"以下 {len(bank)} 題均附答案，針對本報告範圍複習。每題保留對應教學單元的來源；數值案例與排錯建議屬說明性內容。"
    )
    citation_key = "citation_en" if language == "en" else "citation_zh_tw"
    if fmt == "html":
        lines = [f'<section id="self-questions"><h2>{heading}</h2><p>{intro}</p>']
        for index, item in enumerate(bank, 1):
            lines.append(f'<details data-qa-id="{item["id"]}" id="qa-{item["id"]}"><summary>Q{index:02d}. {html.escape(item["question"][language])}</summary>')
            lines.append(f'<div data-qa-answer="{item["id"]}">')
            for paragraph in item["answer"][language].splitlines():
                lines.append(f'<p>{html.escape(paragraph)}</p>')
            lines.append('</div>')
            for source in item["sources"]:
                lines.append(f'<p class="source-note">{html.escape(by_id[source][citation_key])}</p>')
            lines.append('</details>')
        return "\n".join(lines + ['</section>'])
    lines = [f'## {heading}', '', intro, '']
    for index, item in enumerate(bank, 1):
        lines.extend([f'### Q{index:02d}. {item["question"][language]}', '', f'<!-- qa:{item["id"]} -->', '', '**Answer.**' if language == 'en' else '**答。**', ''])
        paragraphs = item['answer'][language].splitlines()
        lines.extend((['- ' + p for p in paragraphs] if len(paragraphs) > 1 else paragraphs))
        lines.extend(['', '> ' + '; '.join(by_id[s][citation_key] for s in item['sources']), ''])
    return "\n".join(lines)


def validate_questions(report_id, modules, claims, text, language, fmt):
    """Check actual rendered answers, source locators, and stable question order."""
    errors = []
    bank = question_bank(report_id, modules)
    by_id = {item['id']: item for item in claims}
    if len(bank) < 16:
        errors.append('自問自答至少需要 16 題')
    for module in modules:
        for field in ('title', 'lead', 'example', 'pitfall'):
            if any(not module[field].get(lang, '').strip() for lang in ('zh', 'en')):
                errors.append(f"{module['id']} 的 {field} 缺少成對中英文")
        for field in ('rows', 'nodes'):
            if len(module[field]['zh']) != len(module[field]['en']):
                errors.append(f"{module['id']} 的 {field} 中英文結構不一致")
        if [len(row) for row in module['rows']['zh']] != [len(row) for row in module['rows']['en']]:
            errors.append(f"{module['id']} 的比較表中英文欄位不一致")
    marker = r'data-qa-id="([^"]+)"' if fmt == 'html' else r'<!-- qa:([^ ]+) -->'
    matches = list(re.finditer(marker, text))
    if [m.group(1) for m in matches] != [item['id'] for item in bank]:
        errors.append('自問自答題號、數量或順序與雙語題庫不一致')
        return errors
    citation_key = 'citation_en' if language == 'en' else 'citation_zh_tw'
    for index, item in enumerate(bank):
        end = matches[index+1].start() if index+1 < len(matches) else len(text)
        block = html.unescape(text[matches[index].start():end])
        if not item['sources'] or any(s not in by_id or by_id[s]['report_id'] != report_id for s in item['sources']):
            errors.append(f"{item['id']} 缺少同報告的有效來源")
        for source in item['sources']:
            if source in by_id and by_id[source][citation_key] not in block:
                errors.append(f"{item['id']} 缺少答案來源定位")
        answer = item['answer'].get(language, '')
        if not answer.strip() or any(line not in block for line in answer.splitlines()):
            errors.append(f"{item['id']} 未完整呈現答案")
    return errors
