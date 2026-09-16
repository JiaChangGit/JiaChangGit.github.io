"""Register the independent Flexible Data Placement report."""
from pathlib import Path
import json
import re
from scripts.nvme_fdp_content import BASE, NVM, REPORT_ID, UNITS, bi
from scripts.nvme_fdp_terms import TERMS
ROOT = Path(__file__).resolve().parents[1]
PREFIX = "FDP"

def install(reports, titles, modules, glossaries, images):
    from scripts.nvme_lessons import LESSONS
    from scripts.nvme_course_walkthroughs import COURSES
    from scripts.nvme_reader_context import REPORT_CONTEXT
    from scripts.nvme_overviews import OVERVIEWS
    from scripts.nvme_review_bank import BANK
    figures = [f for f in json.loads((ROOT/'.ai/nvme-report/figure-table-register.json').read_text())['entries'] if f['report_id'] == REPORT_ID]
    report = dict(prefix=PREFIX, source_id=BASE, scope_entry='FDP-BASE-INCLUDE', date='2026-09-16',
                  title_zh='NVMe Flexible Data Placement：資料放置、回收單位與事件觀察',
                  title_en='NVMe Flexible Data Placement: Placement, Reclaim Units, and Events',
                  range='Base §3.2.4、§5.2.13.1.29–32、§5.2.30.1.21–22、§7.3–7.4、§8.1.9.4、§8.1.12；NVM §3.2、§4.1.4.6–7',
                  range_en='Base §§3.2.4, 5.2.13.1.29–32, 5.2.30.1.21–22, 7.3–7.4, 8.1.9.4, 8.1.12; NVM §§3.2, 4.1.4.6–7',
                  course_claim_first=True, claims=[])
    modules[REPORT_ID] = []
    for u in UNITS:
        cid = PREFIX+'-'+u['key'].upper()
        mid = 'fdp-'+u['key']
        printed = u['pages'] if u['source'] == NVM else re.sub(r'\d+', lambda m: str(int(m[0])-26), u['pages'])
        report['claims'].append(dict(key=u['key'].upper(), source_id=u['source'], section=u['section'],
          printed_pages=printed, pdf_pages=u['pages'], normative_keyword='none',
          zh_tw=u['summary']['zh'], en=u['summary']['en'],
          scope_entry_id='FDP-'+('NVM' if u['source']==NVM else 'BASE')+('-DEPENDENCY' if u['key']=='namespace' else '-INCLUDE')))
        titles[cid] = (u['title']['zh'], u['title']['en'])
        modules[REPORT_ID].append(dict(id=mid, title=u['title'], lead=u['summary'], sources=[cid],
          figures=[int(f['number']) for f in figures if f['teaching_module']==mid],
          rows=bi([], []), example=u['example'], pitfall=bi('', '')))
        LESSONS[mid] = dict(headers=bi(['問題','判斷','例子'], ['Question','Interpretation','Example']),
                            teaching=[s[1] for s in u['steps']], reading=u['reading'])
        COURSES[mid] = dict(title=u['title']['zh'], steps=u['steps'], outcome=u['example']['zh'])
    report['claims'].append(dict(key='STATISTICS-COMMANDS',source_id=NVM,section='4.1.4.6',printed_pages='79',pdf_pages='79',normative_keyword='none',scope_entry_id='FDP-NVM-INCLUDE',zh_tw='NVM 的 HBMW／MBMW 計入 User Data Out Commands、Write Zeroes 和 Write Uncorrectable；命令是否有等量主機 payload，不能代替這項統計分類。',en='For NVM, HBMW/MBMW include User Data Out Commands, Write Zeroes and Write Uncorrectable; an equal-size host payload is not the criterion for accounting.'))
    titles['FDP-STATISTICS-COMMANDS'] = ('NVM 統計計入的命令','Commands included in NVM accounting')
    modules[REPORT_ID][10]['sources'].append('FDP-STATISTICS-COMMANDS')
    modules[REPORT_ID][10]['overview_claim_count'] = 2
    reports[REPORT_ID] = report
    glossaries[REPORT_ID] = [(t, '') for t in TERMS]
    images[REPORT_ID] = dict(zh='posts/2026/dogMC_title.jpg', en='posts/2026/cat_title.jpg')
    REPORT_CONTEXT[REPORT_ID] = dict(
      intro=bi('FDP 讓主機把資料何時會一起失效的知識，轉成 SSD 可以使用的放置選擇。本文從回收成本開始，連起配置、namespace 映射、Write、RUH 更新，以及能驗證使用結果的狀態、統計與事件。讀完應能解釋一個 PID 如何選到目前的 RU，也能判斷一次操作究竟改了參照、邏輯資料，還是整個群組設定。',
               'FDP translates the host’s knowledge of which data expires together into placement choices the SSD can use. This report connects reclamation cost, configuration, namespace mappings, Writes, RUH updates, and the status, statistics and events used to assess the result. Follow a PID to its current RU and distinguish changes to a reference, logical data, or the group configuration.'),
      axes=bi([
       ['資料為什麼要一起放','先從有效資料搬移的成本理解目的，再分清 RG、RUH、RU，以及初始與持續隔離。它們決定分組的範圍與搬移後仍須維持的條件。'],
       ['設定如何接到一筆 Write','配置定義資源與 PID 格式；namespace 清單把 PHNDL 對到 RUH；Data Placement Directive 再讓 Write 明確選擇 RG 與 PHNDL。'],
       ['資料生命週期與主機控制','Status 查當下剩餘量，Update 換空 RU，DSM 描述失效的 LBA。三者分工不同，配合使用才有機會改善回收成本。'],
       ['如何知道實際發生什麼','Usage 看配置來源，Statistics 看累計量，Events 看原因與位置；先辨識範圍、期間與有效位，才能正確解讀數據。']],
       [['Why place data together?','Start with valid-data relocation cost, then separate RG, RUH and RU and compare initial versus persistent isolation. These define grouping and relocation constraints.'],
        ['From configuration to one Write','A configuration defines resources and PID layout. The namespace maps PHNDL to RUH, and the Data Placement Directive lets a Write choose RG and PHNDL.'],
        ['Data lifetime and host control','Status observes available writes, Update selects an empty RU, and DSM describes expired LBAs. Their distinct roles work together to reduce reclamation cost.'],
        ['Observe actual behavior','Usage shows allocation origin, Statistics measures cumulative work, and Events records causes and locations. Check scope, interval and validity before interpreting values.']]),
      background=bi(['適合具備 OS、Computer Organization 與 SSD 基本概念的讀者。以 PCIe 與 NVM Command Set 為情境；所有數量與命令值的例子都是說明性設定，實際能力以裝置回覆為準。本文包含指定主範圍，必要引用只講理解 FDP 所需的欄位與條件。'],
                     ['Assumes operating systems, computer organization and basic SSD knowledge. Examples use PCIe and the NVM Command Set. Counts and encodings are illustrative; device responses define actual capabilities. Necessary references explain the fields and conditions needed for FDP without expanding into unrelated topics.']))
    OVERVIEWS[REPORT_ID] = bi([
      '可以沿著一批資料走完全文：先按預期失效時間分組，再設定可用資源與映射；寫入時透過 PID 選到目前 RU，寫滿或主動 Update 後使用下一個 RU。舊資料何時失效、何時由主機提供解除配置資訊，是另一條同樣重要的線。',
      '以下教學先按理解順序串起這條資料路徑，再把各張規格表放回它所解答的問題。資料量、資源數、清單索引與命令的數量減 1 編碼會各自演算，不用背一串縮寫來猜其意義。'],
      ['Follow one data batch: group by expected expiration, configure resources and mappings, and use a PID to select the current RU. Filling it or issuing Update moves future writes to another RU. When the old data expires and the host describes deallocation is a separate, equally important part of the lifecycle.',
       'The explanation follows this data path before returning each specification structure to the question it answers. Data sizes, resource counts, list indices and zero-based count encodings are kept distinct.'])
    questions = [
      ('mapping','PHNDL 1 對 RUH 3、RGIF=2，PID 8001h 寫向哪裡？','Where does PID 8001h point when PHNDL 1 maps to RUH 3 and RGIF=2?',
       '高 2 bits 是 RGID 2，低 14 bits 是 PHNDL 1；查 namespace 的表得到 RUH 3，因此使用 RUH 3 在 RG 2 目前參照的 RU。它不是實體地址，也不是 LBA。',
       'The high two bits select RG 2 and the low fourteen select PHNDL 1. The namespace maps it to RUH 3, so the Write uses that handle’s current RU in RG 2. This is neither a physical address nor an LBA.',['CONFIG','MODEL']),
      ('invalid','同一個非法 PID 放在 Write 和 RUH Update，結果一樣嗎？','Does the same invalid PID have the same effect in Write and RUH Update?',
       '不同。明確使用 Data Placement 的 Write 由控制器另選可存取的位置，並依事件啟用條件記錄；Update 拒絕非法 PID，而且失敗前可能部分更新。這兩種規則不能互套。',
       'No. A Data Placement Write selects an accessible fallback location and logs under the enablement rules. Update rejects invalid PIDs, and partial updates may precede failure. The rules are not interchangeable.',['WRITE','UPDATE']),
      ('counts','NUMFDPC=1、NPHNDLS=2、NPID=1，各是多少項？','How many items do NUMFDPC=1, NPHNDLS=2 and NPID=1 represent?',
       '依序為 2 筆配置、2 個明確 Placement Handles、2 個 Update PIDs。前後兩者採數量減 1，中間直接計數；名稱都像數量，編碼卻不同。',
       'Two configurations, two explicitly supplied Placement Handles, and two Update PIDs. The first and last use count-minus-one encoding; NPHNDLS is direct.',['CONFIG','NAMESPACE','UPDATE']),
      ('isolation','共享同一 Persistently Isolated RUH，能保證兩個 namespace 彼此隔離嗎？','Does sharing a Persistently Isolated RUH isolate two namespaces from each other?',
       '不能。持續隔離是按 RUH 區分資料來源；兩個 namespace 共用同一個 RUH，正好落在同一個隔離對象之內，還會共享相關事件設定效果。',
       'No. Persistent isolation distinguishes originating RUHs. Two namespaces sharing one RUH are within the same isolation identity and also share the effect of its event settings.',['ISOLATION','EVENTS']),
      ('event-range','Media Reallocated 回 NLBAM=8、LBA=100，能列出全部被搬的 LBA 嗎？','Can NLBAM=8 and LBA=100 identify all relocated LBAs?',
       '不能。先確認 LBAV 有效；100 只是其中一個位置。其餘 7 個可能不連續，也無法由這筆事件的單一 LBA 欄重建完整清單。',
       'No. First check LBAV. LBA 100 is one example; the other seven may be disjoint and cannot be reconstructed from that single field.',['EVENT-RECORD']),
      ('measurement','改過 FDP 配置後，能用之前的 HBMW／MBMW 繼續算同一段增量嗎？','Can HBMW/MBMW deltas continue across an FDP configuration change?',
       '不能直接延續。成功改變 Feature 值會清零統計，應結束舊量測、重新建立起點；也要避免飽和或 ΔHBMW=0 的情況。',
       'Not directly. A successful feature-value change clears the counters. End the previous interval and establish a new baseline; also account for saturation and a zero host-write delta.',['STATISTICS','ENABLE']),
    ]
    BANK[REPORT_ID] = [dict(id='fdp-'+key,question=bi(qz,qe),answer=bi(az,ae),sources=[PREFIX+'-'+s for s in src])
      for key,qz,qe,az,ae,src in questions]


ROUTE = [
 ('Base',110,111,'3.2.4','3.2.5',bi('看 70 的 RG／RUH／RU 關係，先建立名詞位置。','Use Figure 70 to establish RG/RUH/RU relationships.')),
 ('Base',319,327,'5.2.13.1.29–5.2.13.1.32','5.2.13.1.33',bi('從 FDP Configurations 標題起：配置和 PID → Usage → Statistics → Events。先標記事件的 NVM 擴充，最後切文件再接。','Start at FDP Configurations: configuration/PID → Usage → Statistics → Events. Flag the NVM event extension for the final document switch.')),
 ('Base',506,509,'5.2.30.1.21–5.2.30.1.22','5.2.30.1.23',bi('先用 1Dh 把群組設定完成，再用 1Eh 選 RUH 的事件。','Use 1Dh for the group configuration, then 1Eh for events on RUHs.')),
 ('Base',594,597,'7.3–7.4','7.5',bi('比較 Receive/Status 和 Send/Update；用 2 個 PID 演算 NPID 與 buffer。','Compare Receive/Status with Send/Update and work through the two-PID count and buffer.')),
 ('Base',653,653,'8.1.9.4','8.1.10',bi('只讀 Data Placement 標題下的內容，確認沒有直接的 Directive Send／Receive 操作。','Read only under Data Placement and confirm that no direct Directive Send/Receive operations exist.')),
 ('Base',673,678,'8.1.12','8.1.13',bi('從頁底 Flexible Data Placement 標題起，以 730→731→732 收束全貌，再走啟用、reset 後恢復與 Write。','Start at the Flexible Data Placement heading near the page bottom. Tie together 730→731→732, then enablement, reset recovery and Writes.')),
 ('NVM',26,26,'3.2','3.3',bi('一次切到 NVM，補完整 21 的 PID／RUHID／EARUTR／RUAMW。','Switch once to NVM and complete Figure 21: PID/RUHID/EARUTR/RUAMW.')),
 ('NVM',79,79,'4.1.4.6–4.1.4.7','4.1.4.8',bi('確認統計計入的命令，再用 116 解讀 Media Reallocated 的 ETSP。','Confirm the commands counted in Statistics, then use Figure 116 for the Media Reallocated ETSP.')),
]


def render_route(reader):
    lang=reader.lang
    reader.figure_label='R';reader.figure_paragraph_no=0
    out=['<section id="spec-route"><h2>'+bi('開著 Spec 的順向報告路徑','A forward route through the specifications')[lang]+'</h2>']
    out.append(reader.paragraph(bi('先用本文主軸與例子講全貌，再依下列 PDF 檢視器頁碼向後翻。Base 只切一次到 NVM。共用頁以起始章節與停止標題為界；教學所用的必要背景已在中文 HTML 解釋，不必在現場為每個引用來回翻頁。',
      'Establish the overall picture with the examples, then move forward through the actual PDF viewer pages below. Switch from Base to NVM once. On shared pages, use the start section and stop heading. The Chinese tutorial explains necessary background so the live report need not jump to every reference.')[lang]))
    rows=[]
    for i,(doc,start,end,section,stop,explain) in enumerate(ROUTE,1):
        rows.append([f'R{i} · {doc} PDF '+str(start)+(f'–{end}' if end!=start else ''),
          f'§{section}',explain[lang]+' '+bi(f'在 §{stop} 前停下。',f'Stop before §{stop}.')[lang]])
    out.append(reader.table(bi(['翻頁順序','主範圍','要說清楚的關係與停止位置'],['Page sequence','Primary scope','What to explain and where to stop'])[lang],rows))
    out.append('</section>');reader.figure_label=None
    return '\n'.join(out)
