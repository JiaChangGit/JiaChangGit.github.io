"""One-time, idempotent migration of approved reports and old link landings."""
import json
from copy import deepcopy
from pathlib import Path
from scripts.build_nvme_reports import REPORTS, REPORT_MODULES, artifact_ids
from scripts.nvme_report_split import SPLITS, EXTRA

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / '.ai/nvme-report'

def main():
    docs = {name:json.loads((CONTROL/(name+'.json')).read_text()) for name in ('scope','output-contract','figure-table-register')}
    scope, contract, register = (docs[n] for n in ('scope','output-contract','figure-table-register'))
    old_ids = {v[0] for v in SPLITS.values()}
    if not any(r['id'] in old_ids for r in scope['reports']):
        print('Topic migration already applied'); return
    old_scopes = {r['id']:r for r in scope['reports']}
    old_artifacts = deepcopy(contract['artifacts'])
    old_figures = deepcopy(register['entries'])
    contract['artifacts'] = [a for a in contract['artifacts'] if a['report_id'] not in old_ids]
    scope['reports'] = [r for r in scope['reports'] if r['id'] not in old_ids]
    register['entries'] = [f for f in register['entries'] if f['report_id'] not in old_ids]
    for rid,(old,prefix,*_) in SPLITS.items():
        numbers = set(EXTRA[rid]) | {n for m in REPORT_MODULES[rid] for n in m['figures']}
        selected = []
        for f in old_figures:
            if f['report_id'] != old or int(f['number']) not in numbers: continue
            if f['source_id']=='NVME-NVM-CS-1.3':
                if rid in {'base-boot-partitions','base-telemetry','base-hmb-emulation'}: continue
                if rid=='base-device-self-test' and f['number']!='111': continue
                if rid=='base-namespace-management' and f['number']=='111': continue
            f=deepcopy(f); f['id']=prefix+'-'+f['id'].split('-',1)[1]; f['report_id']=rid
            f['required_artifact_ids']=[artifact_ids(rid)[0]]; f['introduced_in']=[artifact_ids(rid)[0]]
            selected.append(f)
        register['entries'].extend(selected)
        s=deepcopy(old_scopes[old]); s['id']=rid
        s['sections']=list(dict.fromkeys(c['source_id']+' §'+c['section'] for c in REPORTS[rid]['claims']))
        s['included_figure_ids']=[f['id'] for f in selected]
        s['dependency_figures']=[f['number'] for f in selected if f.get('role')=='referenced_dependency']
        s['title']=REPORTS[rid]['title_zh']; s['approval_note']='2026-09-11：使用者核准拆篇、獨立教學、全局報告與完整圖表教學。'
        scope['reports'].append(s)
        old_editions=[a for a in old_artifacts if a['report_id']==old]
        for index,(fmt,lang) in enumerate([('html','zh-Hant-TW'),('markdown','zh-Hant-TW'),('markdown','en')]):
            a=deepcopy(next(a for a in old_editions if a['format']==fmt and a['language']==lang))
            a.update(id=artifact_ids(rid)[index],report_id=rid)
            a['required_source_ids']=sorted({c['source_id'] for c in REPORTS[rid]['claims']} | {f['source_id'] for f in selected})
            a['path']=f'DOCS/nvme-spec-report/{rid}/tutorial-zh-tw.html' if fmt=='html' else f'_posts/2026-09-11-nvme-{rid}-'+('en' if lang=='en' else 'zh-tw')+'.md'
            if fmt!='html': a['parity_group']=prefix.lower()+'-bilingual'
            contract['artifacts'].append(a)
    for a in contract['artifacts']:
        a['claim_coverage']='all' if a['format']=='html' else 'overview'
        a['purpose']='中文漸進教學與完整逐圖解釋' if a['format']=='html' else '全局觀念、流程與案例；接續閱讀 Spec；中英文對等'
    for f in register['entries']:
        if f['scope_status']=='INCLUDE':
            f['required_artifact_ids']=[a['id'] for a in contract['artifacts'] if a['report_id']==f['report_id'] and a['format']=='html']
            f['introduced_in']=f['required_artifact_ids'][:]
    for key,value in list(contract.items()):
        if isinstance(value,list) and value and isinstance(value[0],str) and any(x in {a['id'] for a in old_artifacts} for x in value):
            contract[key]=[a['id'] for a in contract['artifacts']]
    contract['editorial_policy'].update(per_figure_takeaway_example_details=True,post_purpose='global view before opening the specification',per_figure_worksheet_required=False)
    scope['approval_note']='2026-09-11：13 篇各 3 版。中文 HTML 保留完整圖表教學；中英文 Pages 以全局觀念銜接規格。完全排除 Fabrics。'
    scope['background_policy']['formerly_excluded_topics_allowed']=False
    for name,doc in docs.items():
        (CONTROL/(name+'.json')).write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
    for a in old_artifacts:
        if a['report_id'] not in old_ids: continue
        targets=[rid for rid,v in SPLITS.items() if v[0]==a['report_id'] and rid!='base-device-self-test']
        if a['report_id']=='base-self-test-namespace-management': targets=['base-device-self-test','base-namespace-management']
        if a['report_id']=='base-self-test-hmb-emulation': targets=['base-hmb-emulation','base-device-self-test']
        if a['format']=='html':
            links=''.join(f'<li><a href="../{rid}/tutorial-zh-tw.html">{REPORTS[rid]["title_zh"]}</a></li>' for rid in targets)
            body='<!doctype html><html lang="zh-Hant-TW"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>文章已拆分</title><body><main><h1>請選擇獨立主題</h1><ul>'+links+'</ul></main></body></html>'
        else:
            lang='en' if a['language']=='en' else 'zh-tw'
            old_text=(ROOT/a['path']).read_text(); fm=old_text[:old_text.index('---',4)+3]
            fm+='\n\n'+('This article is now available as separate topics.' if lang=='en' else '這篇合輯已拆成獨立主題。')+'\n\n'
            body=fm+'\n'.join(f'- [{REPORTS[rid]["title_en" if lang=="en" else "title_zh"]}]({{% post_url 2026-09-11-nvme-{rid}-{lang} %}})' for rid in targets)+'\n'
            # Link landing pages remain reachable but are not listed as reports.
            body=body.replace('tags: [NVMe, PCIe, Specification]','tags: []').replace('category: NVMe','category: archive')
        (ROOT/a['path']).write_text(body)
    print('Migrated',len(scope['reports']),'reports and',len(contract['artifacts']),'editions')

if __name__=='__main__': main()
