"""Render and validate concise, paired review questions for every edition."""
from __future__ import annotations
import html
import re
try:
    from scripts.nvme_review_bank import BANK
except ModuleNotFoundError:
    from nvme_review_bank import BANK


def question_bank(report_id, modules):
    return BANK[report_id]


def render_questions(report_id, modules, claims, language, fmt, section_no=0):
    bank = question_bank(report_id, modules)
    by_id = {c['id']: c for c in claims}
    key = 'citation_en' if language == 'en' else 'citation_zh_tw'
    heading = 'Check your understanding' if language == 'en' else '學完後想一想'
    label = 'Sources' if language == 'en' else '來源'
    lines = [f'<section id="knowledge-check"><h2 id="review-questions">{heading}</h2>']
    paragraph_no = 0
    for index, q in enumerate(bank, 1):
        paragraph_no += 1
        answer = html.escape(q['answer'][language])
        answer_paragraph = (
            f'<p class="reader-paragraph review-answer">'
            f'<span class="paragraph-number" aria-label="{section_no:02d}.{paragraph_no:02d}">{section_no:02d}.{paragraph_no:02d}.</span>'
            f'<span class="paragraph-text">{answer}</span></p>'
        )
        lines.extend([f'<!-- qa:{q["id"]} -->',
            f'<details class="review-question" id="qa-{q["id"]}"><summary>{index}. {html.escape(q["question"][language])}</summary>',
            f'<div data-qa-answer="{q["id"]}">{answer_paragraph}</div>',
            f'<details class="source-note"><summary>{label}</summary>'])
        lines.extend('<p>' + html.escape(by_id[s][key]) + '</p>' for s in q['sources'])
        lines.append('</details></details>')
    return '\n'.join(lines + ['</section>'])


def validate_questions(report_id, modules, claims, text, language, fmt):
    errors = []
    bank = question_bank(report_id, modules)
    by_id = {c['id']: c for c in claims}
    if not bank:
        return ['缺少概念複習題']
    for lang in ('zh', 'en'):
        for field in ('question', 'answer'):
            values = [q[field].get(lang, '').strip() for q in bank]
            if not all(values) or len(values) != len(set(values)):
                errors.append(f'{lang} 的 {field} 缺少內容或重複')
        paragraphs = {m[f][lang] for m in modules for f in ('lead', 'example', 'pitfall')}
        if any(q['answer'][lang] in paragraphs for q in bank):
            errors.append(f'{lang} 答案直接複製正文')
    matches = list(re.finditer(r'<!-- qa:([^ ]+) -->', text))
    if [m.group(1) for m in matches] != [q['id'] for q in bank]:
        return errors + ['自問自答題號、數量或順序與雙語題庫不一致']
    key = 'citation_en' if language == 'en' else 'citation_zh_tw'
    for i, q in enumerate(bank):
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        block = html.unescape(text[matches[i].start():end])
        if not q['sources'] or any(s not in by_id or by_id[s]['report_id'] != report_id for s in q['sources']):
            errors.append(f'{q["id"]} 缺少同報告的有效來源')
        for s in q['sources']:
            if s in by_id and by_id[s][key] not in block:
                errors.append(f'{q["id"]} 缺少答案來源定位')
        if q['question'][language] not in block or q['answer'][language] not in block:
            errors.append(f'{q["id"]} 未完整呈現問題與答案')
    return errors
