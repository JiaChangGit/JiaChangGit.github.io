"""Reader-oriented editions, with one home for each source-backed conclusion.

The HTML course exposes the mechanism progressively. The paired posts explain the overall flow and representative cases before
directing the reader to the specification.
"""
from __future__ import annotations

import html
import re
from difflib import SequenceMatcher
from pathlib import Path
from scripts.nvme_lessons import LESSONS
from scripts.nvme_plain_language import chinese

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
        self.all_modules = modules
        if not tutorial:
            selected = POST_MODULES.get(report_id)
            self.modules = [m for m in modules if not selected or m['id'] in selected]
        self.lang, self.tutorial, self.api = language, tutorial, api
        self.by_id = {c["id"]: c for c in claims}
        self.used_claims, self.used_figures = set(), set()
        self.detail_homes = {}
        self.figure_label = None
        self.figure_paragraph_no = 0
        # Define each term once per document, including hidden field sections.
        self.term_note_counts = {}
        self.section_no = 0
        self.section_paragraph_no = 0
        self.axis_no = 0
        self.axis_paragraph_no = 0
        self.term_sources = dict(api.REPORT_GLOSSARIES[report_id])
        if report_id == 'nvm-command-set-1.3':
            from scripts.nvme_nvmcs_figures import TERMS
            self.term_sources.update({t: '' for t in TERMS})
        elif report_id in {'base-boot-partitions','base-telemetry','base-sanitize'}:
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
            if self.term_note_counts.get(term_key, 0) >= 1 or not re.search(pattern, value, re.I if term in case_insensitive else 0):
                continue
            definition = candidates[term]
            self.term_note_counts[term_key] = self.term_note_counts.get(term_key, 0) + 1
            grouped.setdefault(definition, []).append(term)
        for definition, terms in grouped.items():
            notes.append(f'<div><dt>{esc(" / ".join(terms))}</dt><dd>{esc(definition)}</dd></div>')
        if not notes:
            return ""
        return '<dl class="term-note" aria-label="' + pair(self.lang, "本段名詞", "Terms in this passage") + '">' + "".join(notes) + '</dl>'

    def begin_section(self, number):
        self.section_no = int(number)
        self.section_paragraph_no = 0

    def begin_axis(self, number):
        self.axis_no = int(number)
        self.axis_paragraph_no = 0

    def paragraph(self, value, extra=(), css=""):
        if not value:
            return ""
        if self.lang == 'zh':
            value = chinese(value)
        classes = 'reader-paragraph' + (f' {css}' if css else '')
        if self.figure_label:
            self.figure_paragraph_no += 1
            label=f'{self.figure_label}-{self.figure_paragraph_no}'
            number=f'<span class="paragraph-number figure-paragraph-number" aria-label="{label}">{label}</span>'
        else:
            self.section_paragraph_no += 1
            number = f'<span class="paragraph-number" aria-label="{self.section_no:02d}.{self.section_paragraph_no:02d}">{self.section_no:02d}.{self.section_paragraph_no:02d}.</span>'
        return f'<p class="{classes}">{number}<span class="paragraph-text">{esc(value)}</span></p>' + self.terms(value, extra)

    def axis_paragraph(self, value, extra=()):
        """Render text inside a main-axis card with its own block numbering."""
        if not value:
            return ""
        self.axis_paragraph_no += 1
        number = f'{self.axis_no:02d}-{self.axis_paragraph_no:02d}'
        return (
            f'<p class="axis-paragraph"><span class="axis-paragraph-number" '
            f'aria-label="{number}">{number}</span><span class="paragraph-text">{esc(value)}</span></p>'
            + self.terms(value, extra)
        )

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
        self.figure_label = label+f['number']
        self.figure_paragraph_no = 0
        from scripts.nvme_figure_lessons import lesson, detail
        teaching = lesson(f)
        out = [f'<!-- figure-table:{f["id"]} -->', f'<article class="field-note" id="figure-{f["id"]}"><h4>{label} Figure {f["number"]} · {esc(f["title"])}</h4>']
        out.append('<div class="figure-takeaway"><h5>一句話重點</h5>'+self.claim(c)+'</div>')
        out.append('<div class="figure-example"><h5>用例子讀懂</h5>'+self.paragraph(teaching['example'])+'</div>')
        explanation=detail(f)
        out.append('<details class="figure-detail"><summary>欄位、條件與相關細節</summary>')
        # A shared rule has one home; each Figure still has its own takeaway
        # and example above. Do not paste the group introduction into every card.
        if explanation:
            key=re.sub(r'\s+','',explanation)
            if key in self.detail_homes:
                out.append('<a class="reading-link" href="#figure-'+self.detail_homes[key]+'">共用規則已在前面的相關圖表說明，點此對照。</a>')
            else:
                self.detail_homes[key]=f['id']
                if not similar(explanation,teaching['takeaway']) and not similar(explanation,teaching['example']):
                    out.append(self.paragraph(explanation))
        items=f.get('key_items',[])
        out.append('<div class="field-index"><strong>對照 Spec 的欄位與標示</strong><ul>'+''.join('<li>'+esc(x)+'</li>' for x in items)+'</ul></div>')
        out.append(self.terms(' '.join(items)))
        out.append('</details></article>')
        self.figure_label = None
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
        # Place dependencies beside the concept that uses them, not in an
        # unrelated catch-all at the end. Keys include source document identity.
        extra = {
            'base-ch3': {'39':'properties-init','40':'properties-init','49':'properties-init','50':'properties-init','51':'properties-init',
                         **{str(n):'memory-capacity' for n in range(65,72)}},
            'base-admin-fw-logs': {'155':'fw-lid03-proof','347':'fw-lid03-proof','348':'fw-lid03-proof','474':'fw-lid03-proof'},
            'base-power-features': {'483':'apst-state-machine'},
            'base-self-test-namespace-management': {'346':'namespace-events'},
            'pcie-transport-1.4': {'68':'eom','69':'config-error'},
            'base-boot-telemetry-sanitize': {
                **{str(n):'boot-protection' for n in (188,189,190,191,192,193,198,199,464,465,466,757,758,760,761,762)},
                **{str(n):'telemetry-capture' for n in (203,205,206,207,208,209)},
            },
        }.get(self.id, {})
        if self.id in {'base-device-self-test','base-hmb-emulation','base-namespace-management','base-boot-partitions','base-telemetry','base-sanitize'}:
            from scripts.nvme_report_split import EXTRA
            extra.update({str(n):self.modules[0]['id'] for n in EXTRA[self.id]})
        unassigned = []
        for f in remainder:
            target = extra.get(f['number'])
            if target:
                groups[target].append(f)
            else:
                unassigned.append(f)
        return groups, unassigned

    def body(self):
        from scripts.nvme_reader_context import REPORT_CONTEXT
        from scripts.nvme_reader_visuals import module_illustration
        context = REPORT_CONTEXT[self.id]
        self.begin_section(0)
        out = ['<section id="topic-overview" class="topic-overview">']
        out.append(self.paragraph(context['intro'][self.lang], css='opening'))
        out.append('<h2 id="main-ideas">' + pair(self.lang, '這篇的主軸', 'The main ideas') + '</h2>')
        out.append('<div class="topic-map">')
        for index, (title, explanation) in enumerate(context['axes'][self.lang], 1):
            self.begin_axis(index)
            out.append(f'<article><span class="axis-number">{index:02d}</span><h3>{esc(title)}</h3>{self.axis_paragraph(explanation)}</article>')
        out.append('</div>')
        for paragraph in context['background'][self.lang]:
            out.append(self.paragraph(paragraph))
        from scripts.nvme_overviews import OVERVIEWS
        overview = OVERVIEWS[self.id]
        out.append('<div class="overview-connections"><h3>' + pair(self.lang, '把主軸連起來', 'Connecting the main ideas') + '</h3>')
        for passage in overview[self.lang]:
            out.append(self.paragraph(passage))
        out.append('</div>')
        out.append('</section>')
        groups, remainder = self.assigned_figures() if self.tutorial else ({m['id']:[] for m in self.modules}, [])
        for index, module in enumerate(self.modules, 1):
            lesson = LESSONS[module['id']]
            self.begin_section(index)
            if module['id'] == 'nvmcs-rate-graph':
                self.definitions['SC'] = pair(self.lang, 'Scope；此處是儲存媒體存取描述子的作用範圍，與 CQE 的 Status Code 不同。', 'Scope: the scope of a storage-medium access descriptor, distinct from CQE Status Code.')
                self.definitions['SI'] = pair(self.lang, 'Scope Identifier；指定 SC 所選範圍中的實體。', 'Scope Identifier: identifies the entity in the scope selected by SC.')
            sources = [self.by_id[s] for s in module['sources']]
            fresh = [c for c in sources if c['id'] not in self.used_claims]
            if not self.tutorial:
                fresh = fresh[:1]
            out.append(f'<section class="lesson" id="module-{module["id"]}"><h2 id="heading-{module["id"]}"><span class="section-number">{index:02d}</span> {esc(module["title"][self.lang])}</h2>')
            lead = module['lead'][self.lang]
            if not self.tutorial and not any(similar(module['lead'][lang], c[text_key(lang)]) for c in fresh for lang in ('zh', 'en')):
                out.append(self.paragraph(lead))
            if self.tutorial:
                out.append('<div class="lesson-explanation">')
                out.extend(self.paragraph(p) for p in lesson['teaching'])
                out.append(self.source(sources))
                out.append('</div>')
            illustration = module_illustration(self.id, module, self.lang)
            if illustration:
                out.append(illustration)
                out.append(self.terms(re.sub('<[^>]+>', ' ', illustration)))
            out.extend(self.claim(c) for c in fresh)
            rows = module['rows'][self.lang]
            headers = lesson['headers'][self.lang]
            if rows:
                out.append(self.table(headers[:len(rows[0])], rows, module['title'][self.lang]))
            example = module['example'][self.lang]
            if example and not any(similar(module['example'][lang], c[text_key(lang)]) for c in sources for lang in ('zh', 'en')):
                out.append('<aside class="worked-example"><h3>' + pair(self.lang, '說明性範例', 'Illustrative example') + '</h3>' + self.paragraph(example) + '</aside>')
            # Normative exceptions live in the claim; simulated debugging is omitted.
            if groups[module['id']]:
                out.append('<a class="reading-link" href="#reading-' + module['id'] + '">' + pair(self.lang, '閱讀相關規格圖表 → ', 'Read the related specification figures → ') + esc(module['title'][self.lang]) + '</a>')
            out.append('</section>')
        remaining_claims = [c for c in self.claims if c['figure'] is None and c['id'] not in self.used_claims] if self.tutorial else []
        if remainder:
            raise ValueError(f'{self.id}: figures lack a teaching home: {[f["id"] for f in remainder]}')
        self.begin_section(len(self.modules) + 1)
        if not self.tutorial:
            out.append('<section id="spec-reading"><h2>' + pair(self.lang, '接著打開 Spec 看什麼', 'Where to continue in the specification') + '</h2>')
            out.append(self.paragraph(pair(self.lang, '以下按概念列出閱讀位置。報告時先用上面的流程說明問題，再打開對應章節看欄位與完整條件。中文教學 HTML 另有本篇全部圖表的逐圖重點、案例與細節。', 'Use the flow above to frame the problem, then open the corresponding sections for fields and full conditions. The Chinese tutorial also explains every in-scope figure with its takeaway, example, and details.')))
            rows=[]
            for module in self.all_modules:
                references=list(dict.fromkeys({'NVME-BASE-2.4':'Base 2.4','NVME-NVM-CS-1.3':'NVM 1.3','NVME-PCIE-TRANSPORT-1.4':'PCIe Transport 1.4'}[self.by_id[s]['source_id']]+' §'+self.by_id[s]['section'] for s in module['sources']))
                rows.append([module['title'][self.lang], ' · '.join(references)])
            out.append(self.table(pair(self.lang,['要說明的觀念','Spec 閱讀位置'],['Concept to explain','Specification sections']),rows))
            out.append('<a class="reading-link" href="/DOCS/nvme-spec-report/'+self.id+'/tutorial-zh-tw.html">'+pair(self.lang,'開啟完整中文教學與逐圖解釋 →','Open the complete Chinese tutorial and figure explanations →')+'</a></section>')
            self.begin_section(len(self.modules)+2)
            out.append(self.api.render_questions(self.id,self.all_modules,self.claims,self.lang,'html',len(self.modules)+2))
            return '\n'.join(out)
        out.append('<section id="figure-reading"><h2><span class="section-number">' + str(len(self.modules)+1).zfill(2) + '</span> ' + pair(self.lang, '讀懂本篇的規格圖表', 'Reading the specification figures') + '</h2>')
        out.append(self.paragraph(pair(self.lang,
            '以下依概念整理規格中的圖表。每組先說明讀取順序與要判斷的問題，接著列出各圖的欄位或行為說明。可以由正文的連結跳到對應組別，也可以用這一節檢查自己能否把欄位連回完整操作。',
            'The specification figures below are grouped by concept. Each group explains the reading order and question to resolve, followed by the fields or behavior described by each figure. Follow links from the lessons or use this section to connect fields to complete operations.')))
        for index, module in enumerate(self.modules, 1):
            if not groups[module['id']]:
                continue
            out.append('<details open class="figure-reading-group" id="reading-' + module['id'] + '"><summary>' + pair(self.lang, '圖表組 ', 'Figure group ') + f'{index:02d} · ' + esc(module['title'][self.lang]) + f' · {len(groups[module["id"]])} 張圖表</summary>')
            out.append(self.paragraph(LESSONS[module['id']]['reading'][self.lang]))
            out.append('<a class="reading-link" href="#module-' + module['id'] + '">' + pair(self.lang, '回到本節的解釋與範例', 'Return to the explanation and example') + '</a>')
            out.extend(self.figure(f) for f in groups[module['id']])
            out.append('</details>')
        out.extend(self.claim(c) for c in remaining_claims)
        out.append('</section>')
        if not self.tutorial:
            out.append('</details>')
        question_section = len(self.modules) + 2
        self.begin_section(question_section)
        out.append(self.api.render_questions(self.id, self.modules, self.claims, self.lang, 'html', question_section))
        return '\n'.join(out)


POST_MODULES = {
 'nvm-command-set-1.3': {'nvmcs-capacity','nvmcs-metadata','nvmcs-read-write','nvmcs-compare-verify','nvmcs-copy','nvmcs-atomic','nvmcs-pi-checking','nvmcs-rate-modes'},
}


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
<div class="reader-shell"><aside class="reader-nav"><details open><summary>閱讀目錄</summary><nav aria-label="章節目錄"><a href="#topic-overview">主題與主軸</a>{toc}<a href="#figure-reading">讀懂本篇的規格圖表</a><a href="#knowledge-check">學完後想一想</a></nav></details></aside>
<main id="main" class="nvme-note"><header class="reader-heading"><p class="eyebrow">NVMe · 規格與原理</p><h1>{esc(title)}</h1></header>
{body}
{footer}</main></div></body></html>'''
