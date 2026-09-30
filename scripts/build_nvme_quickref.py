#!/usr/bin/env python3
"""Build the 7-topic figure reference and its three index editions, without PDFs."""
from pathlib import Path
import argparse
import html
import json
import re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.nvme_quickref_data import load, TOPICS

ROOT=Path(__file__).resolve().parents[1]
CONTROL=ROOT/'.ai/nvme-quickref'
OUT=ROOT/'DOCS/nvme-quick-reference'
CARDS=load()
SOURCES=json.loads((ROOT/'.ai/nvme-report/source-register.json').read_text())['sources']
REG=json.loads((CONTROL/'figures.json').read_text())['figures']
DATE='2026-09-29'
SHORT={'B':'Base 2.4','N':'NVM Command Set 1.3','P':'PCIe Transport 1.4'}
TOPIC={row[0]:row for row in TOPICS}
E=html.escape
def tr(zh,en,lang):return zh if lang=='zh' else en
def numrange(pair):return str(pair[0]) if pair[0]==pair[1] else f'{pair[0]}–{pair[1]}'
def visible(text,lang):
    # Preserve digit sequences and identifiers; separate English prose from numbers.
    if lang=='en':
        text=re.sub(r'(?<=[a-z])(?=\d)', ' ',text)
        text=re.sub(r'(?<=\d)(?=(?:bytes?|bits?|blocks?|entries|data|metadata|microseconds|seconds|Dwords?)\b)', ' ',text)
    else:
        text=re.sub(r'(?<=[\u4e00-\u9fff])(?=[A-Za-z0-9])|(?<=[A-Za-z0-9])(?=[\u4e00-\u9fff])', ' ', text)
    return E(text)
def url(topic,lang='zh',standalone=False,key=None):
    if standalone:u=('index' if topic=='index' else topic)+'.html'
    else:u='/nvme/figure-reference/'+('' if topic=='index' else topic+'/')+('zh-tw' if lang=='zh' else 'en')+'/'
    return u+('#figure-'+key.lower() if key else '')
def anchor(key,lang,standalone=False):
    entry=REG[key]
    label=(CARDS[key]['title'] if lang=='zh' else entry['title'])
    return f'<a href="{url(entry["group"],lang,standalone,key)}">{SHORT[key[0]]} Figure {entry["number"]} · {E(label)}</a>'
def table(headers,rows,cls=''):
    return '<div class="qr-table"><table class="'+cls+'"><thead><tr>'+''.join('<th scope="col">'+v+'</th>' for v in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+v+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def source_list(lang):
    return '<footer id="source-files"><h2>'+tr('原始文件','Source documents',lang)+'</h2><p>'+tr('頁碼採本次提供的 ratified PDF；Base 的 PDF 頁＝文件頁＋26，另兩份相同。圖號與英文原名保留，可用 PDF 搜尋定位。公開網站不附原始 PDF。','Locations refer to the supplied ratified PDFs. For Base, PDF page = printed page +26; the other two use identical page numbers. Original figure numbers and English titles are retained for PDF search. Source PDFs are not redistributed.',lang)+'</p><ul class="qr-sources">'+''.join('<li>'+E(s['title'])+' · Revision '+s['revision']+' · '+s['ratified_date']+'<br><code>'+E(s['filename'])+'</code></li>' for s in SOURCES)+'</ul></footer>'
def nav(topic,lang,standalone):
    if standalone:
        links=[(url('index',standalone=True),'總索引'),(url(topic,'zh'),'GitHub Pages 中文'),(url(topic,'en'),'English')]
    else:
        links=[(url('index',lang),tr('總索引','Index',lang)),(url(topic,'en' if lang=='zh' else 'zh'),tr('English','繁體中文',lang)),('/DOCS/nvme-quick-reference/'+('index' if topic=='index' else topic)+'.html',tr('繁中 HTML','Chinese HTML',lang))]
    return '<nav class="qr-top" aria-label="'+tr('版本與索引','Editions and index',lang)+'"><a href="#content">'+tr('跳到內容','Skip to content',lang)+'</a>'+''.join(f'<a href="{u}">{l}</a>' for u,l in links)+'</nav>'

ROUTES=[
 ('啟用後一直沒有 ready','Controller never becomes ready','P12 B36 B41 B42 B57'),
 ('完成結果對不到原命令','Completion does not match the command','B97 B98 B99 B101'),
 ('Invalid Field 不知道是哪個欄位','Locate an invalid command field','B101 B103 B212 B93'),
 ('資料傳輸長度或地址不對','Incorrect transfer length or address','B92 B93 B111 B113 B119'),
 ('讀寫範圍或容量不符合預期','Unexpected range or capacity','N123 N125 N53 N54 N18'),
 ('PI 檢查失敗或 metadata 錯位','PI failure or misplaced metadata','N127 N128 N155 N174 N175'),
 ('空閒後第一筆 I/O 特別慢','First I/O after idle is slow','B340 B468 B475 B477'),
 ('有 CQE 卻收不到中斷','CQE exists but interrupt is absent','B99 P44 P45 P46 B543'),
 ('效能下降或溫度升高','Performance drops or temperature rises','P55 B213 B482 B225'),
 ('把不同時間的 log 拼在一起','Avoid combining different log captures','B204 B208 B221 B223 B232 B233'),
 ('韌體更新後還是舊版本','Firmware update still reports old revision','B191 B187 B215'),
 ('新建 namespace 卻無法存取','Created namespace is inaccessible','B446 N134 B443 B346'),
 ('Sanitize 已接受但不確定結果','Sanitize accepted but outcome is unclear','B451 B454 B312'),
 ('寫入被保護或 Boot 更新被拒絕','Protected writes or rejected Boot updates','B201 B541 B542'),
]
WORKED={
'init':('主機看見裝置，CC.EN 已設 1，但沒有正常處理命令。','P12 B36 B41 B42 B57',[
 '先確認 PCI memory space 與 Bus Master 設定，再核對 BAR 映射、CAP 支援及 CC 選值。這一步排除「能枚舉就一定已完成所有設定」的誤判。',
 '同時記錄 CC.CRIME、CSTS.RDY／CFS 與 elapsed time。ready 模式不同，能處理的命令範圍與等待目標也不同。',
 '最後依 CRIMT／CRWMT 的單位核對等待時間；若已有 CQE，改走命令狀態查詢，而不是把所有失敗都留在初始化問題。']),
'command':('工具回報一筆非零 completion，還不知道是參數錯誤或媒體失敗。','B98 B99 B101 B102 B212',[
 '保留完整 DW2／DW3，先用 phase 判新項目，再用 SQID／CID 對回命令；這樣才知道應查哪種 opcode。',
 '把 SCT 和 SC 分開。SCT 選表，SC 查細項；如果工具已將 status 移位，先記錄工具格式，再使用原圖 bit 編號。',
 'M=1 時查 Error Information。把 BYTLOC／BITLOC 對回 SQE 原始 bytes，而非只留下翻譯後的錯誤名稱。']),
'identify':('應用程式說要讀 32 KiB，但原始命令與 buffer 長度看來不同。','B333 N123 N125 N54 N153 N154',[
 '先確認 Identify CNS 與 namespace，從 FLBAS 選到正確 LBAF。LBAF 的 LBADS 是資料大小指數，MS 是每 block 的 metadata bytes。',
 '用 NLB+1 求 blocks，再乘資料大小；32 KiB 在 4 KiB 格式是 8 blocks，Read 的 NLB 應為 7。',
 '另依 metadata 是交錯或分開、PI 的 PRACT 行為計傳輸 buffer，不能把 namespace 資料容量與實際傳輸 bytes 混用。']),
'io':('同一份資料換成帶 PI 的格式後，Read／Write 開始發生保護或長度錯誤。','N125 N128 N153 N154 N174 N175',[
 '先由 LBAF 與 ELBAF 確认資料大小、metadata 大小、Guard 格式和 tag 位數。不能因為 metadata 都是 16 bytes，就沿用相同 PI 配置。',
 '再對每筆命令確認 PRACT／PRCHK。16-bit Guard 圖裡，8-byte metadata 和大於 8-byte metadata 的 host 傳輸規則不同。',
 '最後檢查交錯／分開 buffer 的位置及 PI byte order。只有位置和格式都一致，才適合比較 Guard 或 tags 的數值。']),
'features':('空閒兩秒後裝置省電，但下一次 I/O 的延遲突然增加。','B198 B340 B475 B477 B468',[
 '用 Get Features SEL=0讀目前 APST 開關與條目，避免把預設或保存值誤當實際設定。',
 '找出當時來源 state 的 entry，ITPT=2000 以毫秒計，ITPS 選目的 state。再到該 state 描述子看 NOPS 及 EXLAT。',
 'EXLAT 以微秒計，0 是未回報。若比較 idle I/O exit limit，另查 FID02h 的 IIELL；它和 APST 等待時間不是同一個延遲。']),
'logs':('在持久事件中看到某次錯誤，希望保留可供後續核對的同一份歷史。','B232 B233 B234 B236',[
 '使用支援的 context 建立動作，讀 header 保存 TLL、TNEV、LREV、GNUM 與來源資訊；不要每個 chunk 都重新建立。',
 '以 ACT0讀資料並按 EHL+3+EL走事件。VSIL 已包含在 EL 中，只用來切開 vendor 資訊與 Event Data。',
 '每筆先依 ET／ETR 找格式，再記時間、對象及結果。最後確認整份長度、事件數及 context 一致性；缺少某事件不能直接證明那件事沒發生。']),
'maintenance':('Sanitize 命令成功，但驗證程式不確定是否可以宣告清除完成。','B451 B454 B312',[
 '先確認命令是 subsystem 或 namespace Sanitize，保存其目標與 CDW10。兩者 PREQ 的 bit 位置不同。',
 '命令成功只表示要求已被接受；接著查目標的 Sanitize Status，把 SOS、SPROG 和 sanitize state 一起讀。',
 '例如 SPROG=FFFFh 但 SOS=3，結果仍是失敗。若有 Media Verification，要將該狀態與正常完成分開，不用單一百分比作結論。']),
}

def render_card(key,ordinal,lang,standalone):
    c=CARDS[key];r=REG[key];title=c['title'] if lang=='zh' else r['title']
    out=[f'<article class="qr-card" id="figure-{key.lower()}" data-figure="{key}">',
         f'<h2><span class="qr-number">{ordinal:02d}</span>{E(title)}</h2>',
         '<p class="qr-original">'+SHORT[key[0]]+f' · Figure {r["number"]} · '+E(r['title'])+'</p>',
         '<p class="qr-location">§'+r['section']+' · '+tr('文件頁 ','Printed pages ',lang)+numrange(r['printed_pages'])+' · PDF '+numrange(r['pdf_pages'])+'</p>']
    labels=tr(['用途','欄位與關係','判讀與例子'],['Use','Fields and relationships','Interpretation and example'],lang)
    for i,text in enumerate(c['paragraphs'][lang],1):
        out.append(f'<p class="qr-explanation" data-paragraph="{key}-{i}"><span class="qr-step">{ordinal:02d}.{i} · {labels[min(i-1,2)]}</span>{visible(text,lang)}</p>')
    if c.get('field_routes'):
        out.append('<h3>'+tr('大表內的欄位位置','Field locations within the large table',lang)+'</h3>')
        out.append(table(tr(['欄位','查詢內容','PDF 頁'],['Fields','Information to find','PDF pages'],lang),[[E(row[0]),E(row[1 if lang=='zh' else 2]),numrange(row[3:5])] for row in c['field_routes']]))
    out.append('<p class="qr-tags">'+tr('搜尋詞：','Search terms: ',lang)+E(' · '.join(c['tags']))+'</p>')
    out.append('<div class="qr-related">'+tr('接著查：','Related lookups: ',lang)+''.join(anchor(k,lang,standalone) for k in c['related'])+'</div>')
    out.append('<a href="#figure-index">'+tr('回本冊圖表索引','Back to this volume’s figure index',lang)+'</a></article>')
    return '\n'.join(out)

def introduction(lang):
    return '<aside class="qr-note"><p>'+tr('每張原圖都有用途、欄位和判讀例子。例子中的數值用於說明，不代表你的裝置設定；原文另有條件時，依該欄位與命令定義判斷。','Each source figure has a use, field guide and worked interpretation. Example numbers are illustrative, not assumed device settings. Apply the conditions belonging to the field and command.',lang)+'</p><p>'+tr('用瀏覽器「在頁面中尋找」搜尋欄位、FID、LID、CNS 或 Figure。bit／byte 位置沿用原圖：bit 是位元，byte 是 8 bits，Dword 是 4 bytes；index 是第幾筆，offset 是相對起點的偏移，須看當處使用的單位。','Use browser Find for fields, FID, LID, CNS or Figure. Positions follow the source: a byte is 8 bits and a Dword is 4 bytes. An index counts entries; an offset measures displacement from an origin in the specified unit.',lang)+'</p><p>'+tr('FID（Feature Identifier）選擇功能；LID（Log Page Identifier）選擇紀錄頁；CNS（Controller or Namespace Structure）選擇 Identify 回傳的資料結構。','FID (Feature Identifier) selects a feature; LID (Log Page Identifier) selects a log page; CNS (Controller or Namespace Structure) selects the structure returned by Identify.',lang)+'</p></aside>'

def body(topic,lang,standalone=False):
    out=['<div class="nvme-quickref">',nav(topic,lang,standalone),'<main id="content">']
    if topic=='index':
        title=tr('NVMe 圖表速查總索引','NVMe Figure Reference Index',lang)
        out+=['<header><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4</p><h1>'+title+'</h1><p class="qr-intro">'+tr('從問題、欄位或圖號，找到需要核對的原始定義。七冊收錄 117 張常用圖表，優先處理能力、參數、結果與異常判讀；每張只在一冊保留完整介紹，其他位置連回。','Find original definitions by question, field or figure number. Seven volumes cover 117 selected figures for capabilities, parameters, results and abnormal behavior. Each has one canonical explanation, linked from other locations.',lang)+'</p></header>',introduction(lang),'<section class="qr-series">']
        for i,(slug,zh,en,iz,ie) in enumerate(TOPICS,1):
            count=sum(r['group']==slug for r in REG.values())
            out.append('<article><h2><a href="'+url(slug,lang,standalone)+'">'+f'{i:02d} · '+E(zh if lang=='zh' else en)+'</a></h2><p>'+E(iz if lang=='zh' else ie)+'</p><p class="qr-tags">'+str(count)+tr(' 張原圖',' source figures',lang)+'</p></article>')
        out.append('</section><section id="questions"><h2>'+tr('手上有問題：從這條查詢路徑開始','Start with the question at hand',lang)+'</h2>')
        out.append(table(tr(['要確認的問題','建議依次查閱'],['Question','Suggested lookup sequence'],lang),[[E(r[0 if lang=='zh' else 1]),'<br>'.join(anchor(k,lang,standalone) for k in r[2].split())] for r in ROUTES]))
        out.append('</section><section id="figure-index"><h2>'+tr('手上有欄位或圖號：完整索引','Complete field and figure index',lang)+'</h2>')
        rows=[]
        for key in sorted(REG,key=lambda k:('BNP'.index(k[0]),int(k[1:]))):
            r=REG[key];rows.append([anchor(key,lang,standalone),'§'+r['section']+'<br>PDF '+numrange(r['pdf_pages']),E(' · '.join(CARDS[key]['tags']))])
        out.append(table(tr(['原圖與介紹','原文位置','可搜尋欄位／識別值'],['Figure and explanation','Source location','Searchable fields / identifiers'],lang),rows,'qr-catalog'))
        out.append('</section>')
    else:
        row=TOPIC[topic];ordinal=next(i for i,t in enumerate(TOPICS,1) if t[0]==topic)
        title=tr('NVMe 圖表速查 ','NVMe Figure Reference ',lang)+f'{ordinal:02d} · '+row[1 if lang=='zh' else 2]
        keys=[k for k in CARDS if REG[k]['group']==topic]
        out+=['<header><p class="qr-eyebrow">'+tr('反覆查詢 · 欄位判讀 · 原文定位','LOOKUP · FIELD INTERPRETATION · SOURCE LOCATIONS',lang)+'</p><h1>'+E(title)+'</h1><p class="qr-intro">'+row[3 if lang=='zh' else 4]+'</p></header>',introduction(lang)]
        out.append('<nav class="qr-toc" id="figure-index" aria-label="'+tr('本冊圖表索引','Volume figure index',lang)+'"><h2>'+tr('本冊圖表','Figures in this volume',lang)+'</h2><ol>')
        out.extend('<li><a href="#figure-'+k.lower()+'">'+SHORT[k[0]]+' Figure '+str(REG[k]['number'])+' · '+E(CARDS[k]['title'] if lang=='zh' else REG[k]['title'])+'</a></li>' for k in keys)
        out.append('</ol></nav>')
        for i,k in enumerate(keys,1):out.append(render_card(k,i,lang,standalone))
        if standalone:
            question,links,steps=WORKED[topic]
            out.append('<section class="qr-note" id="worked-route"><h2>把幾張圖接成一次查詢</h2><p>'+E(question)+'</p>')
            for i,text in enumerate(steps,1):out.append('<p><span class="qr-step">R'+str(i)+'</span>'+E(text)+'</p>')
            out.append('<div class="qr-related">'+''.join(anchor(k,lang,True) for k in links.split())+'</div></section>')
    out+=[source_list(lang),'</main></div>']
    return title,'\n'.join(out)

def generated():
    outputs={};css=(ROOT/'assets/css/nvme-quickref.css').read_text()
    for topic in ['index']+[t[0] for t in TOPICS]:
        title,content=body(topic,'zh',True)
        outputs[f'DOCS/nvme-quick-reference/{topic}.html']='<!doctype html>\n<html lang="zh-Hant-TW"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>'+E(title)+'</title><style>\n'+css+'\n</style></head><body class="qr-standalone">\n'+content+'\n</body></html>\n'
        for lang in ['zh','en']:
            title,content=body(topic,lang)
            suffix='zh-tw' if lang=='zh' else 'en'
            front={'layout':'post','title':title,'date':DATE+' 09:00:00 +0800','categories':['nvme'],'tags':['NVMe','Reference'],'permalink':url(topic,lang),'nvme_quickref':True,'lang':'zh-Hant-TW' if lang=='zh' else 'en','description':tr('NVMe 原圖用途、欄位與判讀速查，附完整 Spec 位置。','NVMe source figures: uses, fields and interpretation with precise specification locations.',lang)}
            header='---\n'+'\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in front.items())+'\n---\n\n'
            outputs[f'_posts/{DATE}-nvme-figure-reference-{topic}-{suffix}.md']=header+content+'\n'
    return outputs

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    outputs=generated();bad=[]
    for rel,content in outputs.items():
        path=ROOT/rel
        if args.check:
            if not path.exists() or path.read_text()!=content:bad.append(rel)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
    manifest={'schema_version':1,'artifacts':[{'path':p,'format':'html' if p.endswith('.html') else 'markdown','url':'/'+p if p.endswith('.html') else re.search(r'^permalink: "([^"]+)"',v,re.M)[1]} for p,v in outputs.items()]}
    path=CONTROL/'outputs.json';content=json.dumps(manifest,ensure_ascii=False,indent=2)+'\n'
    if args.check:
        if not path.exists() or path.read_text()!=content:bad.append(str(path.relative_to(ROOT)))
    else:path.write_text(content)
    if bad:print('Stale quick-reference artifacts: '+', '.join(bad));return 1
    print(f'Quick reference: {len(CARDS)} source figures, {len(outputs)} artifacts, '+('verified' if args.check else 'built'));return 0

if __name__=='__main__':raise SystemExit(main())
