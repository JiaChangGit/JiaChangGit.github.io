"""Install the consolidated report and its forward-only specification route."""
from pathlib import Path
import json,re
from scripts.nvme_admin_io_scope import REPORT_ID, BASE, NVM
from scripts.nvme_admin_io_content import UNITS, bi

ROOT=Path(__file__).resolve().parents[1]

ROUTE_CUES = {'B01': {'zh': 'Admin opcode、資料方向與 NSID；Figure 144 同時比較 Format 與 Sanitize 各狀態下的命令限制。',
         'en': 'Admin opcodes, data direction, and NSID; compare command restrictions during Format and the Sanitize '
               'states in Figure 144.'},
 'B02': {'zh': 'Abort：目標與 IANP → AER：完成格式、事件型別、事件參數。',
         'en': 'Abort: target and IANP → AER: completion layout, event types, and parameters.'},
 'B03': {'zh': 'Device Self-test：NSID 與 STC → 作業互動 → 完成狀態。先提醒啟動命令成功不等於背景測試完成，稍後在 LID 06h 看紀錄。',
         'en': 'Device Self-test: NSID and STC → operation interactions → command status. Distinguish request success '
               'from background-test completion; inspect results later at LID 06h.'},
 'B04': {'zh': 'Firmware Commit → Image Download → Format → Get Features → Get Log Page 共同格式 → LID 00h–08h。LID 06h 接回 '
               'Self-test；07h／08h 用同一張 block 範圍圖說明 Telemetry。',
         'en': 'Firmware Commit → Image Download → Format → Get Features → common Get Log Page format → LIDs 00h–08h. '
               'LID 06h completes Self-test; use one block-range diagram for Telemetry LIDs 07h/08h.'},
 'B05': {'zh': 'LID 12h：依 FID 索引，區分支援、scope 與內容／能力變動；不展開排除 FID。',
         'en': 'LID 12h: index by FID and distinguish support, scope, and content/capability changes; skip excluded '
               'FIDs.'},
 'B06': {'zh': 'Boot Partition LID 15h：BPID 選對象，16-byte header 與映像資料分開，LPO 用 Log 起點計算。',
         'en': 'Boot Partition LID 15h: select BPID, distinguish the 16-byte header from image data, and measure LPO '
               'from the start of the log.'},
 'B07': {'zh': 'LID 24h：只讀預設配置狀態及其支援條件，不進入還原配置流程。',
         'en': 'LID 24h: read default-configuration status and support conditions without entering restoration '
               'workflows.'},
 'B08': {'zh': 'Sanitize Status LID 81h：先看 SSTAT，再看有效的 SPROG、action 資訊及估計時間；把命令接受與最終結果分開。',
         'en': 'Sanitize Status LID 81h: read SSTAT before valid SPROG, action information, and time estimates; '
               'distinguish acceptance from final results.'},
 'B09': {'zh': '先讀 Get Log Page completion，再讀 Identify 請求。CNS 01h 長表分組講，接著依原順序讀 '
               '02h、03h、04h、05h、06h、07h、08h、10h、11h、12h、13h、16h。',
         'en': 'Read Get Log Page completion, then the Identify request. Group the long CNS 01h table, then follow CNS '
               '02h, 03h, 04h, 05h, 06h, 07h, 08h, 10h, 11h, 12h, 13h, and 16h in page order.'},
 'B10': {'zh': 'CNS 18h、19h、1Ah、1Bh、1Ch、1Dh、1Fh、20h：資源與格式清單。以 CNSSID 起始索引、GENCTR 與最多 12 筆項目示範 Underlying Namespace 列舉。',
         'en': 'CNS 18h, 19h, 1Ah, 1Bh, 1Ch, 1Dh, 1Fh, and 20h: resource and format lists. Demonstrate '
               'underlying-namespace enumeration with CNSSID, GENCTR, and the 12-entry limit.'},
 'B11': {'zh': 'Identify 的共同完成行為；接著順向跳到 Namespace Attachment。',
         'en': 'Identify completion behavior; continue forward to Namespace Attachment.'},
 'B12': {'zh': 'Namespace Attachment → Management → Sanitize。先比較附加關係和儲存物件，再用 SEL／CSI／回傳 NSID 讀 Management；Sanitize 的 '
               'SANACT 和 Overwrite 欄位接回先前 LID 81h 的狀態。',
         'en': 'Namespace Attachment → Management → Sanitize. Separate associations from storage objects, then read '
               'SEL, CSI, and returned NSID. Connect Sanitize actions and Overwrite fields to the earlier LID 81h '
               'state.'},
 'B13': {'zh': 'Security Receive → Send → Set Features 共同規則 → FID 01h、02h、04h、06h、07h、0Bh、0Ch、0Eh。',
         'en': 'Security Receive → Send → common Set Features rules → FIDs 01h, 02h, 04h, 06h, 07h, 0Bh, 0Ch, and '
               '0Eh.'},
 'B14': {'zh': 'FID 10h 與 11h：熱管理界線、非 operational 狀態的背景活動。',
         'en': 'FIDs 10h and 11h: thermal-management limits and background activity in non-operational states.'},
 'B15': {'zh': 'Sanitize Config FID 17h：用 NDI=1、NDAS=1 的例子比較 NODRM=0 的拒絕與 NODRM=1 的警告處理。',
         'en': 'Sanitize Config FID 17h: with NDI=1 and NDAS=1, contrast rejection for NODRM=0 with warning-mode '
               'processing for NODRM=1.'},
 'B16': {'zh': 'FID 19h：Set 選組合索引，Get 回目前索引；對回稍早 Identify 的命令集 vector。',
         'en': 'FID 19h: Set selects a combination index and Get returns it; connect this to the previously explained '
               'Identify vector.'},
 'B17': {'zh': 'FID 80h：PBSLC 的 pre-boot software load count，不解成進度百分比。',
         'en': 'FID 80h: PBSLC is a pre-boot software load count, not a completion percentage.'},
 'B18': {'zh': 'Boot Write Protection FID 85h 的 Set／Get 狀態 → PCIe 中斷 FID 08h／09h → HMB FID 0Dh。同頁的章節界線須辨清。',
         'en': 'Boot Write Protection FID 85h Set/Get states → PCIe interrupt FIDs 08h/09h → HMB FID 0Dh. Observe the '
               'section boundaries on shared pages.'},
 'B19': {'zh': '在同一頁略過 §5.2.30.3，直接讀 §5.2.30.4 的 Set Features completion。',
         'en': 'On the same page, skip §5.2.30.3 and read Set Features completion in §5.2.30.4.'},
 'B20': {'zh': 'Create CQ → Create SQ → Delete CQ → Delete SQ；頁面依此順序，但實際刪除先 SQ 後 CQ。',
         'en': 'Create CQ → Create SQ → Delete CQ → Delete SQ in page order; actual teardown removes referencing SQs '
               'before their CQ.'},
 'B21': {'zh': '第 7 章 opcode 表只讀 Flush 列；同頁 Cancel 開始處停下。',
         'en': 'Read only the Flush row of the Chapter 7 opcode table; stop before Cancel on the same page.'},
 'B22': {'zh': '從頁面中的 §7.2 開始，讀 Flush 時間界線、VWC.FB、cache 不存在或未啟用時的行為。然後關閉 Base 的報告段落。',
         'en': 'Start at §7.2 on the page. Read Flush ordering, VWC.FB, and absent/disabled-cache behavior, then '
               'finish the Base part.'},
 'N01': {'zh': 'Compare → Copy → Dataset Management → Read → Verify → Write → Write Uncorrectable → Write '
               'Zeroes。先比較要提供什麼，再讀每筆命令欄位與結果。',
         'en': 'Compare → Copy → Dataset Management → Read → Verify → Write → Write Uncorrectable → Write Zeroes. '
               'Compare required input before reading fields and results.'},
 'N02': {'zh': 'NVM 的 AER Notice 與 Format 專屬欄位，補回前面 Base 留下的共同位置。',
         'en': 'NVM AER notices and Format-specific fields complete the common layouts already explained from Base.'},
 'N03': {'zh': 'NVM Power Management 補充 → LBA Range Type。', 'en': 'NVM Power Management additions → LBA Range Type.'},
 'N04': {'zh': '在同頁跳過 Error Recovery，從 Write Atomicity Normal 的 DN 開始。',
         'en': 'Skip Error Recovery on the same page and start at Write Atomicity Normal and DN.'},
 'N05': {'zh': '同頁只讀 Error Information 與 SMART／Health 兩節；不要繼續到 Device Self-test。',
         'en': 'Read only Error Information and SMART/Health on this page; stop before Device Self-test.'},
 'N06': {'zh': '依序讀 NVM Identify 各 CNS：容量與基本格式 → controller 能力 → 延伸 namespace 格式 →命令限制 →格式查詢及粒度。',
         'en': 'Follow NVM Identify CNS structures: capacity/base formats → controller capabilities → extended '
               'namespace formats → command limits → format selection and granularity.'},
 'N07': {'zh': 'LBA Format List 的布局與 CNS 適用表；用同一個 Format Index 把整份 I/O 例子串起來。',
         'en': 'LBA Format List layout and CNS applicability; finish by keeping one Format Index consistent throughout '
               'the I/O example.'}}


def install(reports,titles,modules,glossaries,images):
    from scripts.nvme_lessons import LESSONS
    from scripts.nvme_course_walkthroughs import COURSES
    from scripts.nvme_reader_context import REPORT_CONTEXT
    from scripts.nvme_overviews import OVERVIEWS
    from scripts.nvme_review_bank import BANK
    register=json.loads((ROOT/'.ai/nvme-report/figure-table-register.json').read_text())['entries']
    figures=[f for f in register if f['report_id']==REPORT_ID]
    report=dict(prefix='ADMINIO',source_id=BASE,scope_entry='ADMINIO-BASE-INCLUDE',date='2026-09-13',
                title_zh='NVMe 管理與資料命令：沿著 Spec 講解',title_en='NVMe Management and Data Commands: A Specification Walkthrough',
                range='Base 第 5、7 章及指定 NVM 章節，扣除本篇明列的排除項目',
                range_en='Selected Base Chapters 5/7 and NVM sections, minus the explicit exclusions',claims=[])
    modules[REPORT_ID]=[]
    for u in UNITS:
        key=u['key'].upper();claim_id='ADMINIO-'+key;module_id='adminio-'+u['key']
        printed=u['pages'] if u['source']==NVM else re.sub(r'\d+',lambda m:str(int(m[0])-26),u['pages'])
        report['claims'].append(dict(key=key,source_id=u['source'],section=u['sections'],printed_pages=printed,pdf_pages=u['pages'],
            normative_keyword='none',zh_tw=u['summary']['zh'],en=u['summary']['en'],scope_entry_id='ADMINIO-'+('BASE' if u['source']==BASE else 'NVM')+'-INCLUDE'))
        titles[claim_id]=(u['title']['zh'],u['title']['en'])
        modules[REPORT_ID].append(dict(id=module_id,title=u['title'],lead=u['summary'],sources=[claim_id],
            figures=[int(f['number']) for f in figures if f['teaching_module']==module_id],rows=bi([],[]),example=u['example'],pitfall=bi('','')))
        LESSONS[module_id]=dict(headers=bi(['觀察對象','如何判斷','說明性範例'],['Object','Interpretation','Example']),teaching=[s[1] for s in u['steps']],reading=u['reading'])
        COURSES[module_id]=dict(title=u['title']['zh'],steps=u['steps'],outcome=u['example']['zh'])
    from scripts.nvme_admin_io_deep_course import apply
    apply(COURSES)
    report['title_tutorial_zh']='NVMe 管理與資料命令：從一筆 I/O 學會裝置運作'
    reports[REPORT_ID]=report
    glossaries[REPORT_ID]=[('NVMe',''),('namespace',''),('controller',''),('LBA',''),('Dword',''),('SQE',''),('CQE',''),('NSID',''),('CNS',''),('FID',''),('LID',''),('index',''),('offset',''),('metadata',''),('FUA','')]
    images[REPORT_ID]={'zh':'posts/2026/dogMC_title.jpg','en':'posts/2026/cat_title.jpg'}
    REPORT_CONTEXT[REPORT_ID]=dict(
      intro=bi('這份報告串起主機管理 SSD 與執行資料操作所需的介面：如何確認能力、調整運作方式、接收狀態，再把 Read／Write 等命令的範圍與完成保證講清楚。先看全貌，接著真的打開 Base 與 NVM Command Set，依頁碼往後讀。',
               'This report connects the interfaces used to manage an SSD and perform data operations: establish capabilities, configure behavior, receive status, and explain the range and completion guarantees of commands such as Read and Write. Start with the overall picture, then open Base and the NVM Command Set and move forward through their pages.'),
      axes=bi([
        ['認識裝置與可用能力','Identify 是裝置及 namespace 的能力地圖；Log 補充狀態與變動。先知道查詢在問誰，才知道如何使用回覆。'],
        ['安排命令與設定行為','Features 設定行為，SQ／CQ 承接命令。維護時再依目的選動作：Create 與 Attach 分別建立空間及存取關係；Self-test、Telemetry、Sanitize 則各有作業狀態與結果。'],
        ['用資料流比較 I/O','Read 取回資料，Write 送入資料，Compare 接收預期資料，Verify 不傳回一般資料，Copy 只傳來源描述子。用資料方向和結果比較八種命令。'],
        ['判斷結果能保證什麼','命令完成、立即中止、內容相同、持久保存與原子性是不同證據；用範圍、時間順序和格式條件界定每一種保證。']],
       [['Establish the device and its capabilities','Identify maps device and namespace capabilities; logs add status and changes. Know the target of each query before interpreting its response.'],
        ['Arrange commands and configure behavior','Features configure behavior, while SQs/CQs carry commands. Choose maintenance actions by purpose: Create and Attach establish storage and access separately; Self-test, Telemetry, and Sanitize each have their own operation states and results.'],
        ['Compare I/O by data flow','Read returns data, Write supplies it, Compare supplies expected data, Verify returns no normal payload, and Copy supplies descriptors. Compare all eight commands by direction and result.'],
        ['Understand what a result guarantees','Completion, immediate abort, matching content, persistence, and atomicity are distinct evidence. Bound each by target range, ordering, and format conditions.']]),
      background=bi(['讀者已學過 OS 與 Computer Organization。本篇用 4096-byte LBA 的例子建立共同背景；實際裝置的大小仍須從 Identify 確認。本篇依主範圍納入 Self-test、namespace 操作、Boot、Telemetry 與 Sanitize 的相關介面。'],
                    ['The audience knows operating systems and computer organization. Examples assume 4096-byte LBAs where stated; actual formats still come from Identify. The selected scope includes the related Self-test, namespace, Boot, Telemetry, and Sanitize interfaces.']))
    OVERVIEWS[REPORT_ID]=bi(
      ['學習時，把「能力 → 設定 → 操作 → 結果」連起來；正式開 Spec 報告時，則採「Base 5 → Base 7 → NVM 指定章節」的順序。兩種順序解決不同需求：先建立理解，再減少翻頁。',
       'Base 和 NVM 的共同介面與專屬定義不用每次來回找。例如先在 Base 說明 Format 範圍，等讀到 NVM 時再補 PIL／PI／MSET。先前留下的問題在 NVM 段集中回答，全程只切換一次文件。'],
      ['For learning, connect capabilities → settings → operations → results. For the live specification report, follow Base 5 → Base 7 → selected NVM sections. The former builds understanding; the latter reduces page movement.',
       'Avoid repeatedly switching between common and command-set-specific definitions. Explain Format scope in Base and complete PIL/PI/MSET in the NVM part. Resolve those earlier questions together, switching documents only once.'])
    qa=[
      ('abort','Abort 的 status 成功，但 IANP=1，可以立即收回原命令的 buffer 嗎？','Successful Abort status with IANP=1: may the original buffer be reclaimed immediately?',
       '不能只根據這筆 Abort 回覆作決定。IANP=1 沒有立即中止保證，必須確認原命令最終完成與其記憶體使用已結束。','Not from that response alone. IANP=1 gives no immediate-abort guarantee; establish the original command’s completion and end of memory use.',['ABORT']),
      ('lengths','8 blocks 的 Read 與 8 blocks 的 DSM 範圍，長度欄位應各填多少？','How are eight blocks encoded for Read and a DSM range?',
       'Read 的 NLB 填 7；DSM 範圍描述子的 LLB 填 8。兩者不是同一個欄位，外層 DSM 的 NR 還另外表示描述子數減 1。','Read uses NLB=7; a DSM range uses LLB=8. They are different fields, while the outer DSM NR separately encodes descriptor count minus one.',['READ','DATASET']),
      ('format','Format 指定 NSID=3，為什麼還可能影響其他 namespaces？','Why can Format with NSID=3 affect other namespaces?',
       '還必須檢查 SES 選出的 FNS 或 SENS 分支。scope bit 若指定整體範圍，單看 NSID 不能縮小該命令的效果。','SES selects the relevant FNS or SENS branch. A scope bit selecting the wider target is not narrowed merely by the NSID value.',['FORMAT']),
      ('queue','刪除共用 CQ 前，為什麼不能只確認它現在是空的？','Why is an empty shared CQ insufficient justification for deleting it?',
       '空佇列只描述目前沒有待消費的完成項目，不代表沒有 SQ 引用。先移除那些 SQ 並遵守完成及記憶體生命週期條件，再刪 CQ。','Emptiness means there are no completions to consume now, not that no SQ references it. Remove referencing SQs and satisfy completion/lifetime requirements before deleting the CQ.',['QUEUES']),
      ('persistence','Write A 尚未完成就提交 Flush，只等到 Flush 成功，能證明 A 已持久保存嗎？','If Flush is submitted before Write A completes, does successful Flush alone prove A is persistent?',
       '不能。保證集合至少包含 Flush 提交前已完成的命令；若要把 A 納入保證，主機先建立 A 已完成再提交 Flush 的順序。','No. The guaranteed set includes commands completed before Flush submission. Establish A’s completion before submitting Flush to include it in that guarantee.',['FLUSH','WRITE']),
    ]
    BANK[REPORT_ID]=[dict(id='adminio-'+q[0],question=bi(q[1],q[2]),answer=bi(q[3],q[4]),sources=['ADMINIO-'+s for s in q[5]]) for q in qa]


def render_route(reader):
    lang=reader.lang;manifest=json.loads((ROOT/'.ai/nvme-report/admin-io-route.json').read_text())
    reader.figure_label='R';reader.figure_paragraph_no=0
    out=['<section id="spec-route" class="spec-route"><h2>'+bi('開著 Spec 的報告路徑','The live specification route')[lang]+'</h2>']
    out.append(reader.paragraph(bi('先開 Base 2.4 PDF，從檢視器的第 202 頁開始。完成 B22 後，再切換 NVM Command Set 1.3 PDF 的第 27 頁。表中使用檢視器的 PDF 頁數，不是印在頁面下方或目錄中的數字。',
        'Open the Base 2.4 PDF at viewer page 202. After B22, switch to the NVM Command Set 1.3 PDF at page 27. The table uses PDF viewer page numbers, not printed footer or table-of-contents numbers.')[lang]))
    out.append(reader.table(bi(['打開的檔案','頁碼對照'],['File to open','Page numbering'])[lang],[
      ['NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf',bi('PDF 頁 = 正文印刷頁 + 26；以本表實際位置為準。','PDF page = body printed page + 26; use the verified destinations below.')[lang]],
      ['NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf',bi('PDF 頁與印刷頁相同。','PDF and printed page numbers match.')[lang]]]))
    out.append(reader.paragraph(bi('每站先跳到「起點」的章節標題，按順序往下讀，到列出的停止標題前停下。起點或停止點可能在頁面中段，因此不以整頁作為納入範圍。§5.2.13.2 沒有需要另講的 PCIe Log 定義；§5.2.14.3 的子項已全部排除，兩處不另外停留。',
        'At each stop, locate the starting section heading and read forward until just before the listed stopping heading. Boundaries may be mid-page: inclusion is not by whole page. Base §5.2.13.2 adds no PCIe log definition requiring a stop, and all subsections of §5.2.14.3 are excluded.')[lang]))
    for source,label in [(BASE,bi('先讀 Base 2.4：B01–B22','First: Base 2.4, B01–B22')[lang]),(NVM,bi('只切換這一次：NVM Command Set 1.3，N01–N07','The only document switch: NVM Command Set 1.3, N01–N07')[lang])]:
        out.append('<h3>'+label+'</h3><div class="table-wrap"><table class="route-table"><thead><tr>'+''.join('<th scope="col">'+h+'</th>' for h in bi(['站點','起點（PDF 頁／章節）','這一段怎麼講','停止位置'],['Stop','Start: PDF page / section','What to explain in order','Stop before'])[lang])+'</tr></thead><tbody>')
        for r in manifest['routes']:
            if r['source_id']!=source:continue
            out.append('<tr id="route-'+r['id']+'" data-route-source="'+source+'" data-pdf-page="'+str(r['start_pdf_page'])+'"><th scope="row">'+r['id']+'</th><td><strong>'+str(r['start_pdf_page'])+'</strong><br>§'+r['start_section']+'</td><td>'+reader.api.html.escape(ROUTE_CUES[r['id']][lang])+'</td><td>'+bi('PDF ','PDF ')[lang]+str(r['end_pdf_page'])+'<br>§'+r['stop_before_section']+bi(' 標題前',' heading')[lang]+'</td></tr>')
        out.append('</tbody></table></div>')
    out.append(reader.paragraph(bi('有些共用表格列出已排除的功能。本次不朗讀那些功能列，也不跟進其設定章節；但保留命令本身的欄位，仍要解釋其單位與有效條件。例如 AER 的事件參數照 §5.2.2 判讀，不因此加入電壓或資料佇列 Feature 的配置。',
        'Some shared tables list excluded functions. Skip those function rows and configuration sections while still explaining units and validity of retained command fields. For example, interpret AER event parameters in §5.2.2 without adding voltage or data-queue feature configuration.')[lang]))
    out.append('<details class="scope-selection"><summary>'+bi('核對本篇的納入與排除清單','Check the exact inclusion and exclusion list')[lang]+'</summary>')
    selections=manifest['selection'];retained=manifest['included_selectors']
    rows=[
      [bi('主範圍','Main scope')[lang],bi('Base 第 5、7 章扣除下列項目；NVM 只納入明列小節及其子節。','Base Chapters 5/7 minus the exclusions; NVM includes only the listed sections and their descendants.')[lang]],
      ['NVM',', '.join(selections['nvm_roots'])],
      [bi('Base 排除章節','Excluded Base sections')[lang],', '.join(selections['excluded_base_sections'])],
      [bi('保留 FID','Retained FIDs')[lang],', '.join(retained['fid'])],
      [bi('保留 LID','Retained LIDs')[lang],', '.join(retained['lid'])],
      [bi('保留 CNS','Retained CNS values')[lang],', '.join(retained['cns'])],
      [bi('排除 FID','Excluded FIDs')[lang],', '.join(selections['excluded_fids'])],
      [bi('排除 LID','Excluded LIDs')[lang],', '.join(selections['excluded_lids'])],
      [bi('排除 CNS','Excluded CNS values')[lang],', '.join(selections['excluded_cns'])]]
    out.append(reader.table(bi(['範圍項目','內容'],['Scope item','Selection'])[lang],rows))
    out.append('</details></section>');reader.figure_label=None
    return '\n'.join(out)


def illustration(key,language):
    from scripts.nvme_reader_visuals import steps,diagram,box,arrow,module_illustration
    if key=='adminio-command-map':
        from html import escape
        headers=bi(['命令','主機提供什麼','SSD 處理什麼／主機得到什麼'],['Command','Host supplies','Device operation / host receives'])[language]
        rows=bi([
          ['Read','LBA 範圍及接收 buffer','讀取內容，將資料傳回主機。'],
          ['Write','LBA 範圍及要寫入的資料','把資料寫入指定範圍。'],
          ['Compare','LBA 範圍及預期資料','比對儲存內容；回報相同或 Compare Failure。'],
          ['Verify','LBA 範圍與檢查選項','執行驗證，沒有一般 Read 的資料回傳。'],
          ['Copy','來源範圍描述子與目的起點','在裝置內複製資料，主機不搬送整段內容。'],
          ['Dataset Management','範圍描述子與屬性','提供使用提示或要求解除配置；不是寫入零值。'],
          ['Write Uncorrectable','LBA 範圍','標記不可更正條件；後續存取依規格回報錯誤。'],
          ['Write Zeroes','LBA 範圍與控制選項','依零值／解除配置條件處理，不需傳送一般資料 payload。']],
         [['Read','LBA range and receive buffer','Reads content and returns data to the host.'],
          ['Write','LBA range and new data','Stores the supplied data in the selected range.'],
          ['Compare','LBA range and expected data','Compares stored content; returns a match or Compare Failure.'],
          ['Verify','LBA range and checking controls','Validates without returning a normal Read payload.'],
          ['Copy','Source descriptors and destination start','Copies within the device without moving the full content through the host.'],
          ['Dataset Management','Range descriptors and attributes','Provides usage hints or requests deallocation; it is not a zeroing command.'],
          ['Write Uncorrectable','LBA range','Marks an uncorrectable condition for subsequent access.'],
          ['Write Zeroes','LBA range and controls','Applies zeroing/deallocation rules without a normal host payload.']])[language]
        return '<figure><div class="table-wrap"><table><thead><tr>'+''.join('<th scope="col">'+escape(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+escape(c)+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div><figcaption>'+bi('先以資料方向與問題比較 8 種命令，再到後文讀各自條件。來源：NVM 1.3 §3.3.1–3.3.8。','Compare the eight commands by data flow and the question each answers, then read their conditions below. Source: NVM 1.3 §3.3.1–3.3.8.')[language]+'</figcaption></figure>'
    if key=='adminio-firmware':return module_illustration('base-admin-fw-logs',{'id':'fw-commit-state'},language)
    if key=='adminio-features':return module_illustration('base-power-features',{'id':'apst-state-machine'},language)
    if key=='adminio-aer':
        return steps(bi('一般事件：通知與取得完整紀錄分兩步','A typical event: notification precedes full log retrieval')[language],bi(
            ['主機先提交 AER，讓控制器保有可完成的要求。','事件發生：控制器完成 AER，帶回 AET／AEI／LID。','主機讀相應 Log，確認事件內容與有效欄位。','依事件規則清除通知，並維持需要的 outstanding AER。'],
            ['The host posts AERs so requests are available for completion.','An event completes an AER with AET/AEI/LID.','The host reads the associated log and validates its fields.','Clear the event according to its rules and maintain the required outstanding AERs.'])[language],
            bi('這條流程適用於相應的一般事件；Immediate 與 One Shot 的例外在正文分開說明。','This applies to the corresponding ordinary events; Immediate and One Shot exceptions are explained separately.')[language])
    if key=='adminio-queues':
        return steps(bi('用引用關係決定操作順序','Queue references determine the operation order')[language],bi(
            ['先用 Number of Queues 協商可用數量。','建立 CQ 2，再建立指向 CQ 2 的 SQ 3、SQ 4。','正常命令的完成項目寫到 CQ 2。','移除時先刪 SQ 3、SQ 4，再刪 CQ 2。'],
            ['Negotiate counts with Number of Queues.','Create CQ 2, then SQs 3 and 4 referencing it.','Normal commands post their completions to CQ 2.','Remove SQs 3 and 4 before deleting CQ 2.'])[language],
            bi('Spec 先列 Delete CQ 再列 Delete SQ，是文件編排；實際移除仍須先消除 SQ 引用。','The specification lists Delete CQ before Delete SQ; actual teardown still removes SQ references first.')[language])
    if key=='adminio-flush':
        return diagram(bi('Write A 的持久保存界線','The persistence boundary for Write A')[language],bi(
            '已完成的 A 被後續 Flush 涵蓋；與 Flush 同時仍在執行的 B，不能只靠這次 Flush 判定已持久保存。',
            'The completed A is covered by the later Flush. Persistence of B, still outstanding at submission, cannot be inferred from this Flush alone.')[language],[
            box(20,25,210,75,['Write A',bi('CQE 已完成','CQE complete')[language]]),arrow(230,62,275,62),
            box(275,25,210,75,['Flush',bi('主機提交','Host submits')[language]],'command'),arrow(485,62,530,62),
            box(530,25,210,75,['Flush',bi('CQE 成功','CQE success')[language]],'success'),
            box(275,145,465,65,[bi('Write B：提交 Flush 時仍未完成','Write B: outstanding at Flush submission')[language]],'decision')],235)
    if key=='adminio-copy':
        return diagram(bi('兩個來源範圍接成一段目的範圍','Two source ranges concatenate at the destination')[language],bi(
            '說明性範例：4 blocks 接 6 blocks。目的起點為 1000，第二段必須接在 1004；主機傳的是兩筆描述子，NR=1。',
            'Illustrative example: four blocks followed by six. With destination 1000, the second range starts at 1004. The host transfers two descriptors, encoded as NR=1.')[language],[
            box(20,20,280,65,[bi('來源 A：4 blocks','Source A: 4 blocks')[language]]),box(380,20,360,65,[bi('來源 B：6 blocks','Source B: 6 blocks')[language]]),
            arrow(160,85,160,135),arrow(560,85,560,135),
            box(20,135,288,65,['1000–1003'],'command'),box(308,135,432,65,['1004–1009'],'success')],225)
    return ''
