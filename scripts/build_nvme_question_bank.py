#!/usr/bin/env python3
"""Build the approved 328-question bank in 27 volumes and three editions."""
from pathlib import Path
import argparse
import html
import json
import re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.nvme_qa_model import load, LABELS, REFS, COMMON
from scripts.nvme_qa_teaching import VOLUMES, INTRO, AIDS, LESSONS
from scripts.nvme_qa_presentation import reading_plan
from scripts.nvme_qa_visuals import VISUALS

ROOT=Path(__file__).resolve().parents[1]
QUESTIONS=load()
E=html.escape
SHORT={'B':'Base 2.4','N':'NVM Command Set 1.3','P':'PCIe Transport 1.4'}
SOURCES=json.loads((ROOT/'.ai/nvme-report/source-register.json').read_text())['sources']
FIGURES=json.loads((ROOT/'.ai/nvme-quickref/figures.json').read_text())['figures']
DATE='2026-10-01'

def post_date(slug):
    return DATE if slug in ['index']+[v[0] for v in VOLUMES[:6]] else ('2026-10-03' if slug=='data-io' else '2026-10-02')

def tr(zh,en,lang):return zh if lang=='zh' else en
def txt(pair,lang):
    s=pair[0 if lang=='zh' else 1]
    if lang=='en':
        s=re.sub(r'(?<=[a-z])(?=\d)', ' ',s)
        s=re.sub(r'\b(FID|LID|CNS|SCT|SC|SEL|NSID|CID|SQID|SQHD)(?=\d)',r'\1 ',s)
        s=re.sub(r'(?<=\d)(?=(?:bytes?|bits?|entries|ms|microseconds|seconds)\b)', ' ',s)
    else:s=re.sub(r'(?<=[\u4e00-\u9fff])(?=[A-Za-z0-9])|(?<=[A-Za-z0-9])(?=[\u4e00-\u9fff])',' ',s)
    return E(s)
def url(slug,lang='zh',standalone=False):
    if standalone:return slug+'.html'
    return '/nvme/question-bank/'+('' if slug=='index' else slug+'/')+('zh-tw' if lang=='zh' else 'en')+'/'
def source_parts(key):return REFS[key].split('|')
def page_ranges(ranges,offset=0):
    values=[]
    for r in ranges.split(','):
        ends=[int(n)-offset for n in r.split('-')]
        values.append('–'.join(map(str,ends)))
    return ', '.join(values)
def cite(keys,lang):
    return '<p class="qa-citations">'+tr('來源：','Sources: ',lang)+' · '.join('<a href="#ref-'+key+'">'+SHORT[source_parts(key)[0]]+' §'+E(source_parts(key)[1])+'</a>' for key in dict.fromkeys(keys))+'</p>'
def table(headers,rows,lang):
    return '<div class="qr-table" tabindex="0" role="region" aria-label="'+tr('可橫向捲動的比較表','Horizontally scrollable comparison table',lang)+'"><table><thead><tr>'+''.join('<th scope="col">'+txt(v,lang)+'</th>' for v in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+txt(v,lang)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def nav(slug,lang,standalone):
    items=[(url('index',lang,standalone),tr('題庫總索引','Question index',lang))]
    if standalone:items +=[(url(slug,'zh'),'Pages 中文'),(url(slug,'en'),'English')]
    else:items +=[(url(slug,'en' if lang=='zh' else 'zh'),tr('English','繁體中文',lang)),('/DOCS/nvme-question-bank/'+slug+'.html',tr('繁中教學 HTML','Chinese tutorial HTML',lang))]
    return '<nav class="qr-top" aria-label="'+tr('題庫與版本','Bank and editions',lang)+'"><a href="#content">'+tr('跳到內容','Skip to content',lang)+'</a>'+''.join('<a href="'+u+'">'+t+'</a>' for u,t in items)+'</nav>'

GLOSSARY=[
('Controller / namespace',('controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。','A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.')),
('SQ / CQ / SQE / CQE',('Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。','Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.')),
('Register / Identify / Feature / Log',('Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。','A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.')),
('index / offset / zero-based',('index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。','An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.')),
('Scope / reset / retention',('scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。','Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.')),
]

def glossary(lang):
    return '<aside class="qa-glossary"><h2>'+tr('先認識本文使用的字詞','Terms used in this volume',lang)+'</h2><dl>'+''.join('<dt>'+E(k)+'</dt><dd>'+txt(v,lang)+'</dd>' for k,v in GLOSSARY)+'</dl></aside>'

def aid(slug,lang,standalone):
    a=AIDS[slug]
    out=['<section id="overview" class="qa-overview"><h2>'+txt(a['title'],lang)+'</h2><p class="qa-takeaway">'+txt(a['takeaway'],lang)+'</p>',table(a['headers'],a['rows'],lang),'<p><strong>'+tr('舉例看懂：','Worked interpretation: ',lang)+'</strong>'+txt(a['example'],lang)+'</p>',cite(a['refs'],lang),'</section>']
    if standalone:
        out+=['<section class="qa-lesson"><h2>先把觀念接起來</h2>']
        for n,(title,text) in enumerate(LESSONS[slug],1):
            out+=['<article><h3>教學 '+str(n)+' · '+E(title)+'</h3><p>'+txt((text,''),'zh')+'</p>']
            if slug=='data-io' and n==3:
                out+=['<p>沿用 <a href="#q-323">Q323</a> 的教學假設：Single Atomicity Mode、正常單位 8 個區塊、斷電單位 2 個區塊，兩種邊界均從 LBA 0 起每 16 個區塊出現。下表問的是「整筆寫入是否落在保證範圍內」，不是命令能不能成功。</p>',table(
                    [(x,'') for x in ['Write 的 LBA 範圍','整筆正常原子性','整筆斷電原子性']],
                    [[(x,'') for x in row] for row in [
                        ['14～15：2 個區塊','有；不超過 8 個，且沒有跨界','有；不超過 2 個，且沒有跨界'],
                        ['15～16：2 個區塊','沒有這項 2-block 保證；跨越 LBA 16 邊界','沒有這項 2-block 保證；跨越 LBA 16 邊界'],
                        ['12～15：4 個區塊','有；不超過 8 個，且沒有跨界','沒有整筆 4-block 保證；超過 2 個區塊']]],lang),
                    '<p>第二列說明起點的重要性；第三列則說明：即使沒有跨界，也仍須分別檢查正常與斷電原子單位。失去整筆保證不等於必然出現部分更新，也不代表每個區塊都失去 controller 的基本原子保證。</p>',cite(['atomicdata','idns'],lang)]
            out+=['</article>']
        if slug=='features':
            out+=['<div class="qa-state" role="img" aria-label="APST 教學假設：PS0 閒置超過 2000 ms 後進入 PS3；需要處理命令時離開 PS3，並考慮退出延遲"><span>PS0<br>可處理命令</span><span class="qa-arrow">idle &gt; ITPT<br>↓</span><span>PS3<br>非工作狀態</span><span class="qa-arrow">需要處理命令<br>↓</span><span>離開 PS3<br>考慮 EXLAT</span></div><p>這張圖使用教學假設的狀態路徑，不表示每個 SSD 都支援 PS3。實際判讀時，先查 Power State Descriptor 的 NOPS、ENLAT、EXLAT，確認狀態類型及進出延遲，再看 APST 的 ITPS 與 ITPT 如何設定。圖中只呈現已啟用 APST 的這條路徑，沒有列出其他狀態選擇。ITPT 指定轉入目標狀態前，需要閒置多久；ENLAT 與 EXLAT 則分別描述進入及離開狀態所需的延遲，三者發生的階段不同。</p>',cite(['power','powerstates','idctrl'],lang)]
        if slug=='health':
            out+=['<div class="qa-state" role="img" aria-label="教學假設：PS0 閒置超過 2000 ms 進入 PS3；I/O 到達時回到最近的工作狀態 PS0"><span>PS0<br>工作狀態</span><span class="qa-arrow">APSTE=1<br>閒置超過 ITPT=2000 ms<br>↓</span><span>PS3<br>NOPS=1</span><span class="qa-arrow">I/O 需要處理<br>退出 PS3，再進入 PS0<br>↓</span><span>PS0<br>恢復處理 I/O</span></div><p>這是教學假設的單一路徑：先確認 PS3 受支援，再將 PS0 的 APST entry 設為 ITPS=3。進入 PS3 的閒置門檻不包含在每筆 I/O 的退出延遲裡；返回 PS0 的轉換上限則要考慮 PS3.EXLAT 與 PS0.ENLAT。若 controller 經過其他狀態，需按各段轉換再計算。</p>',cite(['powerdetail','psd','power'],lang)]
        out+=['</section>']
    return '\n'.join(out)

def short_rule(value):
    return (value[0].split('。')[0]+'。',re.split(r'(?<=[.!?])\s+',value[1])[0])

def shared_key(value):
    for group,rows in COMMON.items():
        for i,text in rows.items():
            if text==value:return group,i
    return None


def lookup_route(q,lang):
    route=q.get('lookup')
    if not route:return ''
    return '\n'.join([f'<section class="qa-lookup" id="q-{q["id"]:03d}-lookup"><h4>'+txt(route['title'],lang)+'</h4>',
        '<p>'+txt(route['intro'],lang)+'</p>',table(route['headers'],route['rows'],lang),
        '<p>'+txt(route['conclusion'],lang)+'</p>',cite(route['refs'],lang),'</section>'])

def visual_flow(q,lang):
    v=VISUALS[q['id']];qid=f'q-{q["id"]:03d}'
    out=[f'<figure class="qa-flow" id="{qid}-flow"><figcaption>'+txt(v['title'],lang)+'</figcaption>',
         '<p>'+txt(v['intro'],lang)+'</p><ol class="qa-flow-steps">']
    branches=v.get('branches',[])
    for i,(title,body) in enumerate(v['steps']):
        branch=i in branches
        cls='qa-flow-branch' if branch else 'qa-flow-step'
        # No sequential arrow may connect mutually exclusive alternatives.
        arrow=i>0 and not branch and not (i-1 in branches)
        out +=[f'<li class="{cls}">'+('<span class="qa-flow-arrow" aria-hidden="true">↓</span>' if arrow else '')+'<strong>'+txt(title,lang)+'</strong><p>'+txt(body,lang)+'</p></li>']
    out+=['</ol><p class="qa-flow-conclusion">'+txt(v['conclusion'],lang)+'</p></figure>']
    return '\n'.join(out)


def question(q,lang,shared,standalone=False):
    qid=f'q-{q["id"]:03d}';plan=reading_plan(q);visual=VISUALS.get(q['id'])
    replaced=set(visual['replaces']) if visual else set()
    rendered={1};seen={plan['lead']};flow_done=False
    out=[f'<article class="qa-question" id="{qid}" data-question="{q["id"]}" data-answer-kind="{plan["kind"]}"><h2><a class="qa-qid" href="#{qid}">Q{q["id"]:02d}</a> '+txt(q['title'],lang)+'</h2>',
         '<p class="qa-prompt">'+txt(q.get('practice',plan['prompt']),lang)+'</p>',
         f'<details class="qa-answer" id="{qid}-answer"><summary>'+tr('展開解答與推導','Reveal the explanation',lang)+'</summary>',
         f'<p class="qa-answer-lead" id="{qid}-a-01">'+txt(plan['lead'],lang)+'</p><div class="qa-sections">']
    def paragraph(i):
        value=q['answers'][i];key=shared_key(value)
        anchor=f'<span class="qa-anchor" id="{qid}-a-{i:02d}"></span>'
        rendered.add(i)
        if value in seen:return anchor
        seen.add(value)
        if key:
            shared.add(key);group,j=key
            return anchor+'<p>'+txt(short_rule(value),lang)+' <a class="qa-rule-link" href="#common-'+group+'-'+str(j)+'">'+tr('完整條件見本冊說明','Read the complete conditions in this volume',lang)+'</a></p>'
        return anchor+'<p>'+txt(value,lang)+'</p>'
    section_no=0
    for section in plan['sections']:
        fields=section['fields'];visible=[i for i in fields if i not in replaced]
        put_flow=visual and not flow_done and 5 in fields
        if not visible and not put_flow:continue
        section_no+=1
        out+=[f'<section class="qa-section" id="{qid}-s-{section_no:02d}" data-answer-section="{section_no}"><h3><span>{section_no}.</span> '+txt(section['title'],lang)+'</h3>']
        if section.get('table'):
            rows=[]
            for i in visible:
                rendered.add(i)
                out+=[f'<span class="qa-anchor" id="{qid}-a-{i:02d}"></span>']
                rows.append([LABELS[i-1],q['answers'][i]])
            out+=[table([('觸發方式','Trigger'),('這項操作或狀態會如何變化','Effect on this operation or state')],rows,lang)]
        else:
            for i in visible:
                out+=[paragraph(i)]
                if i==3 and q.get('lookup'):out+=[lookup_route(q,lang)]
        if put_flow:
            for i in sorted(replaced):
                if i not in rendered:
                    out+=[f'<span class="qa-anchor" id="{qid}-a-{i:02d}"></span>'];rendered.add(i)
            out+=[visual_flow(q,lang)];flow_done=True
        out+=['</section>']
    if visual and not flow_done:raise ValueError(f'Missing visual position for {qid}')
    out+=['</div>']
    # Keep previously shared deep links working, without retaining irrelevant
    # legacy paragraphs in the hidden DOM or search text.
    out+=[''.join(f'<span class="qa-anchor" id="{qid}-a-{i:02d}"></span>' for i in q['answers'] if i not in rendered)]
    if plan['related']:
        out+=['<p class="qa-related">'+tr('相關機制：','Related mechanisms: ',lang)+' · '.join('<a href="'+url(next(v[0] for v in VOLUMES if v[1]<=n<=v[2]),lang,standalone)+'#q-'+str(n).zfill(3)+'">Q'+str(n)+'</a>' for n in plan['related'])+'</p>']
    out+=['<details class="qa-source-links"><summary>'+tr('本題原文定位','Source locations for this question',lang)+'</summary>',cite(q['refs'],lang),'</details></details><a class="qa-back" href="#question-index">'+tr('回本冊題目','Back to questions',lang)+'</a></article>']
    return '\n'.join(out)

def common_rules(shared,lang):
    titles={'data_io':('資料 I/O 的事件、紀錄與重設','Data-I/O events, records and reset'),'feature_events':('Set Feature 的事件記錄','Set Feature event recording'),'register':('Register 存取','Register access'),'command':('命令完成、事件與紀錄','Command completion, events and records'),'queue':('Queue 的重設與影響範圍','Queue reset and scope'),'identify':('查詢的重設與影響範圍','Query reset and scope'),'feature':('Feature 的重設與影響範圍','Feature reset and scope')}
    if not shared:return ''
    out=['<section id="common-rules" class="qa-common"><h2>'+tr('共用規則：各題連到的完整解釋','Shared rules linked from the answers',lang)+'</h2><p>'+tr('這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。','Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.',lang)+'</p>']
    for group,i in sorted(shared):
        out +=[f'<article id="common-{group}-{i}"><h3>'+txt(titles.get(group,('本主題的共用條件','Shared conditions for this topic')),lang)+' · '+txt(LABELS[i-1],lang)+'</h3><p>'+txt(COMMON[group][i],lang)+'</p></article>']
    return '\n'.join(out+['</section>'])

def sources(keys,lang,standalone):
    out=['<section id="source-index"><h2>'+tr('原文定位與既有圖表判讀','Source locations and existing figure guides',lang)+'</h2><p>'+tr('Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。','Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.',lang)+'</p><ul class="qa-references">']
    for key in sorted(keys,key=lambda k:(source_parts(k)[0],int(source_parts(k)[2].split(',')[0].split('-')[0]),k)):
        prefix,section,pages,figs=source_parts(key)
        out +=[f'<li id="ref-{key}"><strong>'+SHORT[prefix]+' · §'+E(section)+'</strong><br>'+tr('文件頁 ','Printed pages ',lang)+page_ranges(pages,26 if prefix=='B' else 0)+' · PDF '+page_ranges(pages)+((' · Figure '+figs) if figs else '')+'</li>']
    out+=['</ul><h3>'+tr('需要看欄位圖時','When you need a field guide',lang)+'</h3><p>'+tr('以下連結可開啟對應的圖表教學，查閱欄位及判讀方式。每張圖保留固定的教學位置，方便之後反覆查詢。','Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.',lang)+'</p><ul>']
    chosen={'B36','B41','B42','B44','B45','B46','B93','B97','B101','B104','B126','B338','B473','B543','B544','N123'}
    if 'adminsupport' in keys:chosen|={'B217'}
    if 'iofields' in keys:
        chosen|={'N4','N8','N53','N54','N70','N71','N39','N47','N83','N155','N174','N175'}
    prefixes=set(source_parts(k)[0] for k in keys)
    numbers=set()
    for key in keys:
        prefix,_,_,fs=source_parts(key)
        for r in fs.split(','):
            if r.strip():
                z=r.strip().split('–');numbers.update(prefix+str(n) for n in range(int(z[0]),int(z[-1])+1))
    for key in sorted(chosen&numbers&FIGURES.keys()):
        f=FIGURES[key];target=('../nvme-quick-reference/'+f['group']+'.html' if standalone else '/nvme/figure-reference/'+f['group']+'/'+tr('zh-tw','en',lang)+'/')+'#figure-'+key.lower()
        out+=['<li><a href="'+target+'">'+SHORT[key[0]]+' Figure '+str(f['number'])+' · '+E(f['title'])+'</a></li>']
    out+=['</ul><details><summary>'+tr('使用的原始文件','Original documents used',lang)+'</summary><ul class="qr-sources">']
    for s in SOURCES:out+=['<li>'+E(s['title'])+' · Revision '+s['revision']+' · '+s['ratified_date']+'<br><code>'+E(s['filename'])+'</code></li>']
    return '\n'.join(out+['</ul></details></section>'])

def index_body(lang,standalone):
    out=['<h1>'+tr('NVMe Base 2.4 自問自答題庫','NVMe Base 2.4 Self-Study Question Bank',lang)+'</h1><p class="qr-intro">'+tr('本題庫收錄第 1～328 題，依主題分成 27 冊。先理解 controller 啟用、queue 及 command 的運作，再學習如何查詢能力與設定功能。每題除了說明機制，也練習將實際觀察結果與規範要求互相比對。','Questions 1–328 in 27 volumes: from controller enable, queues and commands to capability discovery and configuration. Learn both the mechanisms and how to judge observations against the specification.',lang)+'</p><div class="qr-series">']
    for slug,a,b,zh,en in VOLUMES:
        out+=['<article><h2><a href="'+url(slug,lang,standalone)+'">'+tr(zh,en,lang)+'</a></h2><p class="qr-tags">Q'+str(a)+'–Q'+str(b)+'</p><p>'+txt(INTRO[slug],lang)+'</p></article>']
    out+=['</div><section><h2>'+tr('怎麼使用這份題庫','How to use this bank',lang)+'</h2><ol><li>'+tr('先說出功能的目的、影響對象與正常順序，再選查詢欄位。','Explain purpose, affected objects and sequence before selecting query fields.',lang)+'</li><li>'+tr('每題依問題安排解答：查詢題跟著欄位找證據，操作題看先後順序，比較題先分清對象。事件、錯誤與重設只在和問題有關時說明；流程圖中的分支條件與等待點也是答案的一部分。','Answers follow the question: trace evidence for lookups, dependencies for operations and distinctions for comparisons. Events, errors and resets appear when relevant. Conditions and wait points in the flows are part of the explanation.',lang)+'</li><li>'+tr('判斷韌體是否符合規範前，先確認要求適用的前提。shall 表示強制要求，should 表示建議，may 表示允許。若規範將行為列為 undefined，就沒有固定結果可供驗收，不能自行指定必須回報的 Status。','Establish preconditions before judging firmware. Shall is a requirement, should a recommendation, may permission. Undefined behavior does not supply a fixed expected status.',lang)+'</li></ol><p>'+tr('所有算例皆為教學假設，不是實體裝置量測。範圍是 PCIe SSD 使用的三份規格；不含 NVMe over Fabrics、PCIe Link 與封包細節。必要的 PCIe 設定、中斷、Register 及 Doorbell 仍包含在內。','All numerical examples are hypothetical, not hardware measurements. The scope is the three specifications as used by PCIe SSDs, excluding NVMe over Fabrics and PCIe link/packet details while retaining necessary PCIe configuration, interrupts, registers and doorbells.',lang)+'</p></section>',controls(lang,True),'<section id="question-index"><h2>'+tr('全部題目','All questions',lang)+'</h2><ol class="qa-index">']
    for q in QUESTIONS:
        slug=next(v[0] for v in VOLUMES if v[1]<=q['id']<=v[2])
        out+=['<li class="qa-search-item"><a href="'+url(slug,lang,standalone)+f'#q-{q["id"]:03d}">Q{q["id"]:02d} · '+txt(q['title'],lang)+'</a></li>']
    return '\n'.join(out+['</ol></section>'])

def controls(lang,index=False):
    return '<div class="qa-controls" hidden><label>'+tr('搜尋本頁','Search this page',lang)+' <input type="search" id="qa-search" placeholder="'+tr('題號、欄位或關鍵字','Question number, field or keyword',lang)+'"></label>'+('' if index else '<button type="button" data-expand="true">'+tr('展開全部解答','Expand all answers',lang)+'</button><button type="button" data-expand="false">'+tr('收合全部解答','Collapse all answers',lang)+'</button>')+'<output id="qa-count" aria-live="polite"></output></div>'

SCRIPT='''<script>
(function(){
 const root=document.querySelector('.nvme-qa'); if(!root)return;
 root.querySelectorAll('.qa-controls').forEach(x=>x.hidden=false);
 root.querySelectorAll('[data-expand]').forEach(b=>b.addEventListener('click',()=>root.querySelectorAll('.qa-answer').forEach(d=>d.open=b.dataset.expand==='true')));
 const input=root.querySelector('#qa-search'),items=[...root.querySelectorAll('.qa-question,.qa-search-item')],output=root.querySelector('#qa-count');
 if(input)input.addEventListener('input',()=>{const q=input.value.trim().toLowerCase();let n=0;items.forEach(el=>{el.hidden=!el.textContent.toLowerCase().includes(q);if(!el.hidden)n++;});output.textContent=n+' / '+items.length;});
 function reveal(){let el=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(el){for(let p=el;p;p=p.parentElement){if(p.tagName==='DETAILS')p.open=true;}el.hidden=false;}}
 addEventListener('hashchange',reveal);reveal();
 let printState=[];addEventListener('beforeprint',()=>{printState=[...root.querySelectorAll('details')].map(d=>[d,d.open]);printState.forEach(([d])=>d.open=true);});addEventListener('afterprint',()=>printState.forEach(([d,open])=>d.open=open));
 const toggle=root.querySelector('[data-theme-toggle]');if(toggle)toggle.addEventListener('click',()=>{const dark=document.documentElement.dataset.theme?document.documentElement.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;document.documentElement.dataset.theme=dark?'light':'dark';});
})();
</script>'''

def body(slug,lang,standalone):
    out=['<div class="nvme-quickref nvme-qa">',nav(slug,lang,standalone)]
    if standalone:out+=['<button class="qa-theme" type="button" data-theme-toggle>切換明／暗色</button>']
    out+=['<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>']
    if slug=='index':out+=[index_body(lang,standalone)]
    else:
        _,a,b,zh,en=next(v for v in VOLUMES if v[0]==slug)
        out+=['<header><p class="qa-range">Q'+str(a)+'–Q'+str(b)+'</p><h1>'+tr(zh,en,lang)+'</h1><p class="qr-intro">'+txt(INTRO[slug],lang)+'</p><p>'+tr('先練習，再展開解答。各題依需要使用文字、欄位判讀、比較或流程說明，不要求相同的回答項目。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。','Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.',lang)+'</p></header>',glossary(lang),aid(slug,lang,standalone),controls(lang),'<section id="question-index"><h2>'+tr('本冊題目','Questions in this volume',lang)+'</h2><ol class="qa-index">']
        qs=[q for q in QUESTIONS if a<=q['id']<=b]
        for q in qs:out+=[f'<li><a href="#q-{q["id"]:03d}">Q{q["id"]:02d} · '+txt(q['title'],lang)+'</a></li>']
        out+=['</ol></section>'];shared=set()
        for q in qs:out+=[question(q,lang,shared,standalone)]
        out+=[common_rules(shared,lang)]
        keys=set(r for q in qs for r in q['refs'])|set(AIDS[slug]['refs'])
        if slug=='features':keys|={'powerstates','power','idctrl'}
        out+=[sources(keys,lang,standalone)]
    out+=['</main>',nav(slug,lang,standalone),'</div>',SCRIPT]
    return '\n'.join(out)

def artifacts():
    result={}
    css=(ROOT/'assets/css/nvme-quickref.css').read_text()+'\n'+(ROOT/'assets/css/nvme-question-bank.css').read_text()
    for slug in ['index']+[v[0] for v in VOLUMES]:
        for lang in ['zh','en']:
            title=tr('NVMe 自問自答題庫：','NVMe Self-Study Bank: ',lang)+(tr('總索引 · Q1–328','Index · Q1–328',lang) if slug=='index' else next(v[3 if lang=='zh' else 4] for v in VOLUMES if v[0]==slug))
            front='---\nlayout: post\ntitle: '+json.dumps(title,ensure_ascii=False)+'\ndate: '+post_date(slug)+' 00:00:00 +0800\ncategories: [nvme]\npermalink: '+url(slug,lang)+'\nlang: '+tr('zh-TW','en',lang)+'\nnvme_quickref: true\nnvme_qa: true\n---\n\n'
            result[ROOT/'_posts'/f'{post_date(slug)}-nvme-question-bank-{slug}-{tr("zh-tw","en",lang)}.md']=front+body(slug,lang,False)+'\n'
        title='NVMe 自問自答題庫：'+('總索引 · Q1–328' if slug=='index' else next(v[3] for v in VOLUMES if v[0]==slug))
        result[ROOT/'DOCS/nvme-question-bank'/f'{slug}.html']='<!doctype html>\n<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><title>'+E(title)+'</title><style>'+css+'</style></head><body class="qr-standalone">\n'+body(slug,'zh',True)+'\n</body></html>\n'
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    outputs=artifacts();drift=[]
    for path,content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text()!=content:drift.append(str(path.relative_to(ROOT)))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content,encoding='utf-8')
    if drift:raise SystemExit('Question-bank artifact drift: '+', '.join(drift))
    print(('Verified' if args.check else 'Built')+f' {len(outputs)} question-bank artifacts: 328 questions, question-specific answers, 27 volumes + index, 3 editions')
if __name__=='__main__':main()
