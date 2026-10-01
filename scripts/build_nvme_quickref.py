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
from scripts.nvme_scenario_render import CASES, index_html, cases_html

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
        title=tr('NVMe 圖表判讀與情境練習總索引','NVMe Figure Reference and Scenario Index',lang)
        out+=['<header><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4</p><h1>'+title+'</h1><p class="qr-intro">'+tr('從問題、欄位或圖號，找到需要核對的原始定義。七冊整合 45 道情境練習與 117 張常用圖表，從需求走到查詢介面、欄位與可驗證的結論。每題及每張圖均有固定位置，其他入口直接連回。','Find original definitions by question, field or figure number. Seven volumes combine 45 scenarios with 117 selected figures, connecting requirements to query interfaces, fields and defensible conclusions. Each exercise and figure has one canonical location.',lang)+'</p></header>',introduction(lang),'<section class="qr-series">']
        for i,(slug,zh,en,iz,ie) in enumerate(TOPICS,1):
            count=sum(r['group']==slug for r in REG.values())
            out.append('<article><h2><a href="'+url(slug,lang,standalone)+'">'+f'{i:02d} · '+E(zh if lang=='zh' else en)+'</a></h2><p>'+E(iz if lang=='zh' else ie)+'</p><p class="qr-tags">'+str(count)+tr(' 張原圖',' source figures',lang)+'</p></article>')
        out.append('</section>')
        out.append(index_html(lang,standalone,TOPICS,url,table))
        out.append('<section id="figure-index"><h2>'+tr('手上有欄位或圖號：完整索引','Complete field and figure index',lang)+'</h2>')
        rows=[]
        for key in sorted(REG,key=lambda k:('BNP'.index(k[0]),int(k[1:]))):
            r=REG[key];rows.append([anchor(key,lang,standalone),'§'+r['section']+'<br>PDF '+numrange(r['pdf_pages']),E(' · '.join(CARDS[key]['tags']))])
        out.append(table(tr(['原圖與介紹','原文位置','可搜尋欄位／識別值'],['Figure and explanation','Source location','Searchable fields / identifiers'],lang),rows,'qr-catalog'))
        out.append('</section>')
    else:
        row=TOPIC[topic];ordinal=next(i for i,t in enumerate(TOPICS,1) if t[0]==topic)
        title=tr('NVMe 圖表判讀與情境練習 ','NVMe Figures and Scenarios ',lang)+f'{ordinal:02d} · '+row[1 if lang=='zh' else 2]
        keys=[k for k in CARDS if REG[k]['group']==topic]
        out+=['<header><p class="qr-eyebrow">'+tr('反覆查詢 · 欄位判讀 · 原文定位','LOOKUP · FIELD INTERPRETATION · SOURCE LOCATIONS',lang)+'</p><h1>'+E(title)+'</h1><p class="qr-intro">'+row[3 if lang=='zh' else 4]+'</p></header>',introduction(lang)]
        out.append('<nav class="qr-top" aria-label="'+tr('本冊閱讀入口','Volume entry points',lang)+'"><a href="#exercises">'+tr('從情境練習開始','Start with scenarios',lang)+'</a><a href="#figure-index">'+tr('直接查圖表','Go to figures',lang)+'</a></nav>')
        out.append(cases_html(topic,lang,standalone,anchor,REG,table))
        out.append('<nav class="qr-toc" id="figure-index" aria-label="'+tr('本冊圖表索引','Volume figure index',lang)+'"><h2>'+tr('本冊圖表','Figures in this volume',lang)+'</h2><ol>')
        out.extend('<li><a href="#figure-'+k.lower()+'">'+SHORT[k[0]]+' Figure '+str(REG[k]['number'])+' · '+E(CARDS[k]['title'] if lang=='zh' else REG[k]['title'])+'</a></li>' for k in keys)
        out.append('</ol></nav>')
        for i,k in enumerate(keys,1):out.append(render_card(k,i,lang,standalone))
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
            front={'layout':'post','title':title,'date':DATE+' 09:00:00 +0800','categories':['nvme'],'tags':['NVMe','Reference'],'permalink':url(topic,lang),'nvme_quickref':True,'last_modified_at':'2026-10-01','lang':'zh-Hant-TW' if lang=='zh' else 'en','description':tr('NVMe 情境練習與圖表速查：查詢路徑、欄位推導、完整解答及 Spec 位置。','NVMe scenarios and source figures: lookup routes, field reasoning, worked answers and precise specification locations.',lang)}
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
