"""Reader-oriented editions, with one home for each source-backed conclusion.

The HTML course exposes the mechanism progressively. The paired posts put the
same source-backed details behind disclosures so the main path works in a report.
"""
from __future__ import annotations

import html
import re
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def esc(value):
    return html.escape(str(value), quote=False)


def pair(language, zh, en):
    return en if language == "en" else zh


def text_key(language):
    return "en" if language == "en" else "zh_tw"


def similar(left, right):
    def norm(value):
        return re.sub(r"[\W_]+", "", value.casefold())
    a, b = norm(left), norm(right)
    return bool(a and b) and (a in b or b in a or SequenceMatcher(None, a, b).ratio() > .76)


class Reading:
    def __init__(self, report_id, report, claims, figures, modules, language, tutorial, api):
        self.id, self.report, self.claims = report_id, report, claims
        self.figures, self.modules = figures, modules
        self.lang, self.tutorial, self.api = language, tutorial, api
        self.by_id = {c["id"]: c for c in claims}
        self.used_claims, self.used_figures = set(), set()
        # A definition may reappear once when a hidden field section needs it,
        # but a long note must never keep explaining the same term.
        self.term_note_counts = {}
        self.paragraph_no = 0
        self.term_sources = dict(api.REPORT_GLOSSARIES[report_id])
        if report_id == 'nvm-command-set-1.3':
            from scripts.nvme_nvmcs_figures import TERMS
            self.term_sources.update({t: '' for t in TERMS})
        elif report_id == 'base-boot-telemetry-sanitize':
            from scripts.nvme_bts_terms import TERMS
            self.term_sources.update({t: '' for t in TERMS})
        self.definitions = {}
        for term in set(self.term_sources) | set(api.TERM_LIBRARY):
            definition = api.report_term_definition(term, report_id, language, api.term_definition)
            if not any(s in definition for s in ("這是本 Figure", "A source field label", "來源定義尚未", "source-located field", "依本 Figure 上方", "interpret within this Figure")):
                self.definitions[term] = definition

        from scripts.nvme_reader_terms import definitions
        self.definitions.update(definitions(report_id, language))

    def terms(self, value, extra=()):
        candidates = dict(self.definitions)
        for term, definition in extra:
            if not any(s in definition for s in ("這是本 Figure", "A source field label", "相關欄位", "Related fields", "依本 Figure 上方", "interpret within this Figure")):
                candidates.setdefault(term, definition)
        notes = []
        grouped = {}
        for term in sorted(candidates, key=lambda t: (-len(t), t)):
            pattern = r'(?<![A-Za-z0-9])' + re.escape(term) + (r'(?=\d|\b)' if term == 'CDW' else r'(?![A-Za-z0-9])')
            term_key = term.casefold()
            case_insensitive = {
                'Host', 'logical block', 'metadata', 'Dword', 'token bucket',
                'index', 'offset', 'index-offset', 'zero-based', 'word',
                'page offset', 'bit range', 'raw value',
            }
            if self.term_note_counts.get(term_key, 0) >= 2 or not re.search(pattern, value, re.I if term in case_insensitive else 0):
                continue
            definition = candidates[term]
            self.term_note_counts[term_key] = self.term_note_counts.get(term_key, 0) + 1
            grouped.setdefault(definition, []).append(term)
        for definition, terms in grouped.items():
            notes.append(f'<div><dt>{esc(" / ".join(terms))}</dt><dd>{esc(definition)}</dd></div>')
        if not notes:
            return ""
        return '<dl class="term-note" aria-label="' + pair(self.lang, "本段名詞", "Terms in this passage") + '">' + "".join(notes) + '</dl>'

    def paragraph(self, value, extra=(), css=""):
        if not value:
            return ""
        self.paragraph_no += 1
        classes = 'reader-paragraph' + (f' {css}' if css else '')
        number = f'<span class="paragraph-number" aria-hidden="true">{self.paragraph_no:02d}.</span>'
        return f'<p class="{classes}">{number}{esc(value)}</p>' + self.terms(value, extra)

    def source(self, claims):
        if not claims:
            return ""
        citation_key = "citation_en" if self.lang == "en" else "citation_zh_tw"
        short = []
        for c in claims:
            source = {"NVME-BASE-2.4": "Base 2.4", "NVME-NVM-CS-1.3": "NVM Command Set 1.3", "NVME-PCIE-TRANSPORT-1.4": "PCIe Transport 1.4"}[c["source_id"]]
            ref = f'{source} §{c["section"]}'
            if ref not in short:
                short.append(ref)
        citations = list(dict.fromkeys(c[citation_key] for c in claims))
        return ('<details class="source-note"><summary>' + pair(self.lang, "來源：", "Sources: ") + esc(" · ".join(short)) + '</summary>'
                + "".join('<p>' + esc(c) + '</p>' for c in citations) + '</details>')

    def claim(self, c):
        if c["id"] in self.used_claims:
            return ""
        self.used_claims.add(c["id"])
        return f'<!-- claim:{c["id"]} -->\n' + self.paragraph(c[text_key(self.lang)]) + self.source([c])

    def table(self, headers, rows, caption=""):
        if not rows:
            return ""
        out = ['<div class="table-wrap"><table>']
        if caption:
            out.append('<caption>' + esc(caption) + '</caption>')
        out += ['<thead><tr>' + ''.join('<th scope="col">' + esc(c) + '</th>' for c in headers) + '</tr></thead><tbody>']
        out += ['<tr>' + ''.join('<td>' + esc(c) + '</td>' for c in row) + '</tr>' for row in rows]
        out.append('</tbody></table></div>')
        return ''.join(out) + self.terms(' '.join(' '.join(row) for row in rows))

    def figure(self, f):
        if f['id'] in self.used_figures:
            return ''
        self.used_figures.add(f['id'])
        c = self.by_id[f['id'] + '-CLAIM']
        label = {'NVME-BASE-2.4': 'Base', 'NVME-NVM-CS-1.3': 'NVM', 'NVME-PCIE-TRANSPORT-1.4': 'PCIe'}[f['source_id']]
        out = [f'<!-- figure-table:{f["id"]} -->', f'<details class="field-note" id="figure-{f["id"]}"><summary>{label} Figure {f["number"]} · {esc(f["title"])}</summary>']
        out.append(self.claim(c))
        # Known, source-backed definitions are useful; generic worksheets are not.
        guide = self.api.expanded_figure_guide(f, self.lang)
        specific = [(term, definition) for term, definition in guide['terms']
                    if term not in {'Related fields', '相關欄位'} and not any(x in definition for x in ('這是本 Figure', 'A source field label'))]
        out.append(self.terms(' '.join(f.get('key_items', [])), specific))
        out.append('</details>')
        return '\n'.join(out)

    def assigned_figures(self):
        groups = {m['id']: [] for m in self.modules}
        remainder = []
        for f in self.figures:
            module = None
            if self.id == 'nvm-command-set-1.3':
                from scripts.nvme_nvmcs_figures import lesson_for
                module = lesson_for(f)['id']
            else:
                matches = [m for m in self.modules if int(f['number']) in m['figures']]
                if matches:
                    # Same Figure numbers across documents need the proper topic.
                    if f['source_id'] == 'NVME-NVM-CS-1.3':
                        matches = [m for m in matches if any(self.by_id[s]['source_id'] == f['source_id'] for s in m['sources'])] or matches
                    module = matches[0]['id']
            if module in groups:
                groups[module].append(f)
            else:
                remainder.append(f)
        return groups, remainder

    def body(self):
        from scripts.nvme_reader_context import REPORT_CONTEXT
        from scripts.nvme_reader_visuals import module_illustration
        context = REPORT_CONTEXT[self.id]
        out = ['<section id="topic-overview" class="topic-overview">']
        out.append(self.paragraph(context['intro'][self.lang], css='opening'))
        out.append('<h2 id="main-ideas">' + pair(self.lang, '這篇的主軸', 'The main ideas') + '</h2>')
        out.append('<div class="topic-map">')
        for index, (title, explanation) in enumerate(context['axes'][self.lang], 1):
            out.append(f'<article><span class="axis-number">{index:02d}</span><h3>{esc(title)}</h3>{self.paragraph(explanation, css="axis-description")}</article>')
        out.append('</div>')
        out.append(self.terms(' '.join(' '.join(row) for row in context['axes'][self.lang])))
        for paragraph in context['background'][self.lang]:
            out.append(self.paragraph(paragraph))
        out.append('</section>')
        groups, remainder = self.assigned_figures()
        for index, module in enumerate(self.modules, 1):
            if module['id'] == 'nvmcs-rate-graph':
                self.definitions['SC'] = pair(self.lang, 'Scope；此處是儲存媒體存取描述子的作用範圍，與 CQE 的 Status Code 不同。', 'Scope: the scope of a storage-medium access descriptor, distinct from CQE Status Code.')
                self.definitions['SI'] = pair(self.lang, 'Scope Identifier；指定 SC 所選範圍中的實體。', 'Scope Identifier: identifies the entity in the scope selected by SC.')
            sources = [self.by_id[s] for s in module['sources']]
            fresh = [c for c in sources if c['id'] not in self.used_claims]
            out.append(f'<section class="lesson" id="module-{module["id"]}"><h2 id="heading-{module["id"]}"><span class="section-number">{index:02d}</span> {esc(module["title"][self.lang])}</h2>')
            lead = module['lead'][self.lang]
            if not any(similar(module['lead'][lang], c[text_key(lang)]) for c in fresh for lang in ('zh', 'en')):
                out.append(self.paragraph(lead))
            illustration = module_illustration(self.id, module, self.lang)
            if illustration:
                out.append(illustration)
                out.append(self.terms(re.sub('<[^>]+>', ' ', illustration)))
            if not self.tutorial and fresh:
                out.append('<details class="technical-note"><summary>' + pair(self.lang, '機制與適用條件', 'Mechanism and applicable conditions') + '</summary>')
            out.extend(self.claim(c) for c in fresh)
            if not self.tutorial and fresh:
                out.append('</details>')
            rows = module['rows'][self.lang]
            headers = pair(self.lang, ['項目', '作用或差異', '適用條件'], ['Item', 'Role or distinction', 'Conditions'])
            if rows:
                out.append(self.table(headers[:len(rows[0])], rows))
            example = module['example'][self.lang]
            if example and not any(similar(module['example'][lang], c[text_key(lang)]) for c in sources for lang in ('zh', 'en')):
                out.append('<aside class="worked-example"><h3>' + pair(self.lang, '例子', 'Example') + '</h3>' + self.paragraph(example) + '</aside>')
            # Normative exceptions live in the claim; simulated debugging is omitted.
            if groups[module['id']]:
                out.append('<details class="technical-note"><summary>' + pair(self.lang, '進一步理解欄位與資料結構', 'Fields and data structures in more depth') + '</summary>')
                out.extend(self.figure(f) for f in groups[module['id']])
                out.append('</details>')
            out.append('</section>')
        remaining_claims = [c for c in self.claims if c['figure'] is None and c['id'] not in self.used_claims]
        if remaining_claims or remainder:
            out.append('<section id="additional-details"><h2 id="further-mechanisms">' + pair(self.lang, '補充機制與資料格式', 'Additional mechanisms and data formats') + '</h2>')
            out.extend(self.claim(c) for c in remaining_claims)
            out.extend(self.figure(f) for f in remainder)
            out.append('</section>')
        out.append(self.api.render_questions(self.id, self.modules, self.claims, self.lang, 'html', self.paragraph_no))
        return '\n'.join(out)


def render(report_id, report, claims, figures, modules, language, tutorial, api):
    reading = Reading(report_id, report, claims, figures, modules, language, tutorial, api)
    body = reading.body()
    title = report['title_en'] if language == 'en' else report['title_zh']
    sources = '\n'.join(api.SOURCES[s]['marker'] for s in dict.fromkeys(c['source_id'] for c in claims))
    footer = '<footer class="reference-editions"><details class="source-note"><summary>' + pair(language, '採用的規格版本', 'Specification editions') + '</summary>' + ''.join('<p>' + esc(s) + '</p>' for s in sources.splitlines()) + '</details></footer>'
    if not tutorial:
        description = pair(language, '從主題主軸到關鍵機制、條件與例子的 NVMe 技術報告。', 'An NVMe technical report covering the main ideas, mechanisms, conditions, and examples.')
        frontmatter = api.frontmatter(report_id, title, description, language)
        frontmatter = frontmatter.replace('toc: yes', 'toc: yes\nnvme_notes: true')
        return frontmatter + '\n<div class="nvme-note">\n' + body + '\n' + footer + '\n</div>\n'
    css = (ROOT / 'assets/css/nvme-reader.css').read_text(encoding='utf-8')
    toc = ''.join(f'<a href="#module-{m["id"]}">{index:02d} {esc(m["title"]["zh"])}</a>' for index, m in enumerate(modules, 1))
    return f'''<!DOCTYPE html>
<html lang="zh-Hant-TW"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#eef1f2" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0c1113" media="(prefers-color-scheme: dark)">
<title>{esc(title)}</title><style>{css}</style></head>
<body class="edition-tutorial"><a class="skip-link" href="#main">跳到正文</a>
<div class="reader-shell"><aside class="reader-nav"><details><summary>閱讀目錄</summary><nav aria-label="章節目錄"><a href="#topic-overview">主題與主軸</a>{toc}<a href="#knowledge-check">學完後想一想</a></nav></details></aside>
<main id="main" class="nvme-note"><header class="reader-heading"><p class="eyebrow">NVMe · 規格與原理</p><h1>{esc(title)}</h1></header>
{body}
{footer}</main></div></body></html>'''
