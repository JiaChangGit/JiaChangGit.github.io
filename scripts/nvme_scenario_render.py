"""Exercises share the existing series URLs and canonical figure explanations."""
from html import escape as E
import re
from scripts.nvme_scenarios import load

CASES = load()
SHORT = {'B':'Base 2.4', 'N':'NVM Command Set 1.3', 'P':'PCIe Transport 1.4'}

def refs(token, register):
    owner, locations = token.split(':')
    pages=[]
    for part in locations.split(','):
        pair=[int(n) for n in part.split('-')]
        pages.extend(range(pair[0],pair[-1]+1))
    if '@' in owner:
        prefix, section=owner.split('@'); title='§'+section
    else:
        prefix=owner[0]; row=register[owner]; section=row['section']
        assert all(row['pdf_pages'][0] <= p <= row['pdf_pages'][1] for p in pages), token
        title=f'§{section} · Figure {row["number"]} · {row["title"]}'
    return dict(token=token, prefix=prefix, section=section, title=title, pages=pages)

def ranges(pages):
    groups=[]
    for n in sorted(set(pages)):
        if groups and n==groups[-1][-1]+1: groups[-1].append(n)
        else: groups.append([n])
    return ', '.join(str(g[0]) if len(g)==1 else f'{g[0]}–{g[-1]}' for g in groups)

def source_html(c,lang,register):
    items=[]
    for token in c['sources']:
        r=refs(token,register); delta=26 if r['prefix']=='B' else 0
        items.append('<li>'+E(SHORT[r['prefix']]+' · '+r['title'])+' · '+('文件頁 ' if lang=='zh' else 'Printed pages ')+ranges([n-delta for n in r['pages']])+' · PDF '+ranges(r['pages'])+'</li>')
    return '<ul class="qr-case-sources">'+''.join(items)+'</ul>'

def jump(c,lang,standalone,url):
    i=0 if lang=='zh' else 1
    return '<a href="'+url(c['topic'],lang,standalone)+'#exercise-'+c['id']+'">'+E(c['title'][i])+'</a>'

INTERFACES=[
('Identify','能力、識別、資料格式與限制，包括 OACS、SANICAP、CTRATT 等 controller attributes；先選 CNS，再確認 NSID／CSI。','Capabilities, identity, formats and limits, including controller attributes such as OACS, SANICAP and CTRATT; select CNS and the applicable NSID/CSI.'),
('Controller properties','CAP、CC、CSTS 等 NVMe 暫存器：能力、配置與就緒狀態。PCIe 使用記憶體映射存取。','NVMe registers such as CAP, CC and CSTS: capabilities, configuration and readiness, accessed through memory mapping on PCIe.'),
('PCIe configuration space','BAR、PCI CMD、Link Status、MSI-X、PCIe AER；回答傳輸與 function 組態問題。','BARs, PCI CMD, Link Status, MSI-X and PCIe AER answer transport and function-configuration questions.'),
('Get Features','目前、預設、保存值或可變更能力；必須保留 FID 與 SEL。','Current, default, saved values or supported capabilities; retain both FID and SEL.'),
('Get Log Page','狀態、累計量、事件與快照；每個 LID 的 target、讀取與確認規則不同。','Status, counters, events and snapshots, with LID-specific targeting, retrieval and acknowledgment rules.'),
('SMART / Health','透過 Get Log Page LID=02h 取得，不是另一種通用查詢命令；其統計範圍由能力與 NSID 決定。','Retrieved through Get Log Page LID=02h, not a separate generic command; capability and NSID determine reporting scope.'),
]

def index_html(lang,standalone,topics,url,table):
    i=0 if lang=='zh' else 1
    out=['<section id="exercise-index"><h2>'+('從情境選擇查詢方法' if i==0 else 'Choose a lookup through scenarios')+'</h2>']
    out.append('<p>'+('下面 45 題整合在原有七冊，不另外複製欄位教學。先選問題，作答後再沿解答連到原圖判讀；同一題只有一個固定位置。' if i==0 else 'The 45 exercises live within the existing seven volumes, without duplicating field guides. Choose a question, attempt it, then follow its answer to the canonical figure explanations. Each exercise has one location.')+'</p>')
    out.append(table(['查詢介面','能取得的資訊'] if i==0 else ['Interface','What it provides'],[[E(r[0]),E(r[1+i])] for r in INTERFACES]))
    for slug,zh,en,*_ in topics:
        cases=[c for c in CASES if c['topic']==slug]
        out.append('<h3>'+E(zh if i==0 else en)+'</h3><ol class="qr-exercise-list">')
        out.extend('<li>'+jump(c,lang,standalone,url)+'</li>' for c in cases)
        out.append('</ol>')
    out.append('</section>')
    return '\n'.join(out)

VISUALS={
 'io-03':(['命令','實際 LBA 範圍','以 LBA 8 分界'],['Command','Actual LBA range','Boundary at LBA 8'],[
     ['A','8–11',('8 9 10 11：同一區間','8 9 10 11: one interval')],
     ['B','6–9',('6 7 │ 8 9：跨界','6 7 | 8 9: crosses the boundary')]]),
 'io-05':(['順序','主機觀察／動作'],['Order','Host observation/action'],[
     ['1',('提交 data Write，FUA=1','Submit data Write, FUA=1')],
     ['2',('等待並確認 data Write 成功','Wait for and verify data Write success')],
     ['3',('才提交 index Write，FUA=1','Only then submit index Write, FUA=1')],
     ['4',('等待並確認 index Write 成功','Wait for and verify index Write success')]]),
 'features-03':(['來源 entry','條件','目的 state'],['Source entry','Condition','Destination state'],[
     ['PS0',('在 PS0 達到 100 ms idle 門檻','Reach the 100 ms idle threshold in PS0'),'PS2'],
     ['PS2',('在 PS2 達到 500 ms idle 門檻','Reach the 500 ms idle threshold in PS2'),'PS3']]),
}

def cases_html(topic,lang,standalone,anchor,register,table):
    i=0 if lang=='zh' else 1
    cases=[c for c in CASES if c['topic']==topic]
    out=['<section id="exercises"><h2>'+('先做情境練習' if i==0 else 'Try the scenarios first')+'</h2>',
         '<p>'+('每題資料均為教學假設，不是實際裝置回傳。先寫下查詢介面、目標、欄位與可支持的結論，再展開解答。題目只做 Spec 推導，不會執行命令。' if i==0 else 'All observations are hypothetical, not device measurements. Before opening an answer, identify the interface, target, fields and supported conclusion. These are specification exercises; no commands are executed.')+'</p>']
    if standalone:
        out.append('<aside class="qr-note"><p>練習方法：先不要急著解每個 bit。把需求寫成一句能驗證的話，例如「這個 namespace 的這筆 Write，在什麼條件下具有哪種保證」。作答時分開記錄「已知」「推導結果」「仍缺的證據」。解答中的三段依序帶你走過判讀；不熟的欄位可由末尾連結回本冊原圖介紹。</p></aside>')
    out.append('<nav class="qr-toc" id="exercise-toc" aria-label="'+('情境索引' if i==0 else 'Exercise index')+'"><ol>')
    out.extend('<li><a href="#exercise-'+c['id']+'">'+E(c['title'][i])+'</a></li>' for c in cases)
    out.append('</ol></nav>')
    for n,c in enumerate(cases,1):
        out.append('<article class="qr-card qr-case" id="exercise-'+c['id']+'" data-scenario="'+c['id']+'"><h3><span class="qr-number">'+('練習 ' if i==0 else 'EXERCISE ')+f'{n:02d}</span>'+E(c['title'][i])+'</h3>')
        out.append('<p class="qr-case-question">'+E(c['question'][i])+'</p><div class="qr-observations"><h4>'+('模擬回傳與已知條件' if i==0 else 'Hypothetical observations and assumptions')+'</h4><ul>')
        out.extend('<li>'+E(p[i])+'</li>' for p in c['observations'])
        out.append('</ul></div><details class="qr-answer"><summary>'+('展開解答：查詢路徑與完整推導' if i==0 else 'Show answer: lookup route and reasoning')+'</summary>')
        out.append('<p class="qr-route"><strong>'+('查詢次序：' if i==0 else 'Lookup sequence: ')+'</strong>'+E(c['route'][i])+'</p>')
        for step,p in enumerate(c['steps'],1):
            out.append('<p data-reasoning="'+c['id']+f'-{step}"><span class="qr-step">'+('推導 ' if i==0 else 'Step ')+str(step)+'</span>'+E(p[i])+'</p>')
        if c['id'] in VISUALS:
            zh,en,rows=VISUALS[c['id']]
            out.append(table(zh if i==0 else en,[[E(v[i] if isinstance(v,tuple) else v) for v in row] for row in rows]))
        out.append('<div class="qr-related">'+('需要重看欄位時，接著查：' if i==0 else 'Revisit the field explanations: ')+''.join(anchor(k,lang,standalone) for k in c['figures'])+'</div>')
        out.append('<h4>'+('本題原文定位' if i==0 else 'Source locations for this exercise')+'</h4>'+source_html(c,lang,register)+'</details>')
        out.append('<a href="#exercise-toc">'+('回情境索引' if i==0 else 'Back to exercise index')+'</a></article>')
    out.append('</section>')
    return '\n'.join(out)
