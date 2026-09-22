"""Registration helpers for independently authored, three-edition reports."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def bi(zh, en):
    return {'zh': zh, 'en': en}


def printed(pages):
    return re.sub(r'\d+', lambda match: str(int(match[0]) - 26), pages)


def install_report(config, units, terms, reports, titles, modules, glossaries, images):
    from scripts.nvme_lessons import LESSONS
    from scripts.nvme_course_walkthroughs import COURSES
    from scripts.nvme_reader_context import REPORT_CONTEXT
    from scripts.nvme_overviews import OVERVIEWS
    from scripts.nvme_review_bank import BANK
    rid, prefix = config['id'], config['prefix']
    figures = [f for f in json.loads((ROOT/'.ai/nvme-report/figure-table-register.json').read_text())['entries'] if f['report_id']==rid]
    report = dict(prefix=prefix, source_id='NVME-BASE-2.4', scope_entry=prefix+'-BASE-INCLUDE',
        date=config['date'], title_zh=config['title']['zh'], title_en=config['title']['en'],
        range=config['range']['zh'], range_en=config['range']['en'], course_claim_first=True, claims=[])
    modules[rid] = []
    for unit in units:
        mid = prefix.lower()+'-'+unit['key']
        sources=[]
        for index, claim in enumerate(unit['claims']):
            key=unit['key'].upper()+(f'-{index+1}' if index else '')
            cid=prefix+'-'+key; sources.append(cid)
            report['claims'].append(dict(key=key,source_id='NVME-BASE-2.4',section=claim['section'],
                printed_pages=printed(claim['pages']),pdf_pages=claim['pages'],normative_keyword='none',
                scope_entry_id=prefix+'-BASE-'+('PREREQUISITES' if claim.get('background') else 'INCLUDE'),
                zh_tw=claim['text']['zh'],en=claim['text']['en']))
            titles[cid]=(unit['title']['zh'],unit['title']['en'])
        modules[rid].append(dict(id=mid,title=unit['title'],lead=unit['claims'][0]['text'],sources=sources,
            figures=[int(f['number']) for f in figures if f['teaching_module']==mid],rows=bi([],[]),
            example=unit['example'],pitfall=bi('','')))
        LESSONS[mid]=dict(headers=bi(['問題','欄位與條件','解讀'],['Question','Fields and conditions','Interpretation']),
            teaching=[text for _,text in unit['steps']],reading=unit['reading'])
        COURSES[mid]=dict(title=unit['title']['zh'],steps=unit['steps'],outcome=unit['example']['zh'])
    reports[rid]=report
    glossaries[rid]=[(term,'') for term in terms]
    images[rid]=dict(zh='posts/2026/dogMC_title.jpg',en='posts/2026/cat_title.jpg')
    REPORT_CONTEXT[rid]=config['context']
    OVERVIEWS[rid]=config['connections']
    BANK[rid]=[dict(id=prefix.lower()+'-'+q['key'],question=q['question'],answer=q['answer'],
        sources=[prefix+'-'+source for source in q['sources']]) for q in config['questions']]


def render_forward_route(reader, route):
    lang=reader.lang;reader.figure_label='R';reader.figure_paragraph_no=0
    out=['<section id="spec-route"><h2>'+bi('開著 Spec 的順向報告路徑','A forward route through the specification')[lang]+'</h2>']
    out.append(reader.paragraph(bi('先用本文的全貌與案例說明機制，再按下列 Base PDF 檢視器頁碼往後讀。共用頁從指定標題開始，在停止標題前結束；必要背景已在中文教學說明，不必為每個引用往返翻頁。',
        'Explain the mechanism with the overview and examples, then follow these Base PDF viewer pages in order. On shared pages, start at the specified heading and stop before the next named heading. The Chinese tutorial explains necessary background without repeated reference detours.')[lang]))
    rows=[]
    for index,(start,end,section,stop,focus) in enumerate(route,1):
        pages=str(start) if start==end else f'{start}–{end}'
        rows.append([f'R{index} · Base PDF {pages}','§'+section,
            focus[lang]+' '+bi(f'在 §{stop} 前停止。',f'Stop before §{stop}.')[lang]])
    out.append(reader.table(bi(['頁碼順序','章節起點','重點與停止位置'],['Page order','Start section','Focus and stop heading'])[lang],rows))
    out.append('</section>');reader.figure_label=None
    return '\n'.join(out)
