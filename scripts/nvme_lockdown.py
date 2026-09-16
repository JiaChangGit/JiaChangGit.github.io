"""Register the Command and Feature Lockdown report."""
from pathlib import Path
import json
import re
from scripts.nvme_lockdown_content import BASE, REPORT_ID, UNITS, bi
from scripts.nvme_lockdown_terms import TERMS
ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'LOCKDOWN'


def install(reports, titles, modules, glossaries, images):
    from scripts.nvme_lessons import LESSONS
    from scripts.nvme_course_walkthroughs import COURSES
    from scripts.nvme_reader_context import REPORT_CONTEXT
    from scripts.nvme_overviews import OVERVIEWS
    from scripts.nvme_review_bank import BANK
    figures = [f for f in json.loads((ROOT/'.ai/nvme-report/figure-table-register.json').read_text())['entries'] if f['report_id']==REPORT_ID]
    report = dict(prefix=PREFIX,source_id=BASE,scope_entry='LOCKDOWN-BASE-INCLUDE',date='2026-09-16',
      title_zh='NVMe Command and Feature Lockdown：查詢、限制範圍與持續性',
      title_en='NVMe Command and Feature Lockdown: Queries, Scope, and Persistence',
      range='Base §8.1.5、§5.2.13.1.20（LID 14h）、§5.2.16',
      range_en='Base §§8.1.5, 5.2.13.1.20 (LID 14h), 5.2.16',course_claim_first=True,claims=[])
    modules[REPORT_ID] = []
    for u in UNITS:
        cid=PREFIX+'-'+u['key'].upper(); mid='lockdown-'+u['key']
        report['claims'].append(dict(key=u['key'].upper(),source_id=BASE,section=u['section'],
          printed_pages=re.sub(r'\d+',lambda m:str(int(m[0])-26),u['pages']),pdf_pages=u['pages'],
          normative_keyword='none',scope_entry_id='LOCKDOWN-BASE-INCLUDE',zh_tw=u['summary']['zh'],en=u['summary']['en']))
        titles[cid]=(u['title']['zh'],u['title']['en'])
        modules[REPORT_ID].append(dict(id=mid,title=u['title'],lead=u['summary'],sources=[cid],
          figures=[int(f['number']) for f in figures if f['teaching_module']==mid],rows=bi([],[]),example=u['example'],pitfall=bi('','')))
        LESSONS[mid]=dict(headers=bi(['問題','判斷','例子'],['Question','Interpretation','Example']),teaching=[s[1] for s in u['steps']],reading=u['reading'])
        COURSES[mid]=dict(title=u['title']['zh'],steps=u['steps'],outcome=u['example']['zh'])
    extras=[
      ('PERSISTENCE-EXCEPTIONS','persistence','5.2.30.1.25.4.1','520',
       '持續性啟用時，未凍結或無認證解凍支援的 Lockdown Persistence Personality，不能透過 Lockdown 禁止 Set Features 或 FID 22h。若任一 personality 支援認證解凍，特定 CDP Authentication 的 Security Send／Receive 必須仍被允許。',
       'With persistence enabled, an unfrozen Lockdown Persistence Personality or one without authenticated unfreeze support prevents Lockdown from prohibiting Set Features or FID 22h. If any personality supports authenticated unfreeze, the specified CDP Authentication Security Send/Receive operations remain allowed.'),
      ('UUID-VALIDITY','uuid','8.1.31.2','763-764',
       'UIDX=0 不指定 UUID；非零索引需指向該資訊支援的有效 UUID。全 0、NVMe Invalid UUID 或不支援於該資訊的 UUID 會導向 Invalid Field in Command。',
       'UIDX=0 selects no UUID. A nonzero index must identify a valid UUID supported for the information; zero, NVMe Invalid UUID or an unsupported UUID produces Invalid Field in Command.'),
      ('PROHIBITED-EXECUTION','result','8.1.5','624',
       '受限制的操作從 Admin Queue 收到時，命令以 Command Prohibited by Command and Feature Lockdown 中止；從 Management Endpoint 收到時，回 Access Denied Error Response。',
       'A prohibited operation received on the Admin Queue is aborted with Command Prohibited by Command and Feature Lockdown; a Management Endpoint returns an Access Denied Error Response.'),
    ]
    for key,mid,section,pages,zh,en in extras:
        report['claims'].append(dict(key=key,source_id=BASE,section=section,pdf_pages=pages,
          printed_pages=re.sub(r'\d+',lambda m:str(int(m[0])-26),pages),normative_keyword='none',
          scope_entry_id='LOCKDOWN-BASE-INCLUDE' if section=='8.1.5' else 'LOCKDOWN-BASE-PREREQUISITES',zh_tw=zh,en=en))
        titles[PREFIX+'-'+key]=(zh.split('；')[0],en.split(';')[0])
        module=next(m for m in modules[REPORT_ID] if m['id']=='lockdown-'+mid)
        module['sources'].append(PREFIX+'-'+key)
        module['overview_claim_count']=2
    reports[REPORT_ID]=report
    glossaries[REPORT_ID]=[(t,'') for t in TERMS]
    images[REPORT_ID]=dict(zh='posts/2026/dogMC_title.jpg',en='posts/2026/cat_title.jpg')
    REPORT_CONTEXT[REPORT_ID]=dict(
      intro=bi('Command and Feature Lockdown 處理的是「哪些管理操作，在什麼入口、哪些控制器上不准執行」。理解它需要把能力、目前狀態與修改命令接起來，再分清限制何時解除、斷電後是否保留。本文以一個 FID 的限制與讀回為例，從全貌走到命令欄位、兩種 Log 格式與必要的持續性例外。',
       'Command and Feature Lockdown defines which management operations are prohibited, on which incoming interfaces and controllers. Connect capability checks, current state and state-changing commands, then determine how prohibitions end and whether they survive power cycles. One FID example leads from the overall process to command fields, both log formats and persistence exceptions.'),
      axes=bi([
       ['先知道能限制什麼','先查裝置是否支援整體限制或逐一指定控制器，再查哪些操作允許被禁止。功能存在、操作受支援、操作可禁止，是三個不同問題。'],
       ['把限制範圍說清楚','依序選操作、接收入口與控制器。只禁止一項設定、只限制某個入口，或只選某台控制器，會得到不同的影響範圍。'],
       ['查詢要能驗證設定','一般格式看全體共同項目；增強格式看指定控制器或全體彙整，再分辨某項是否所有控制器都符合。用相同條件讀回才有比較意義。'],
       ['理解限制的生命週期','限制可以用命令解除；經過斷電循環後是否仍保留，還要看最初選的控制器範圍與持續性設定。最後補足認證解凍與廠商定義的必要條件。']],
       [['Discover what can be restricted','First check whether the device supports subsystem-wide or controller-scoped restrictions, then find eligible operations. Capability, command support and prohibitable eligibility are separate questions.'],
        ['Specify the affected scope','Select the operation, incoming interface and controllers in turn. Restricting one setting, one interface or one controller produces different affected scopes.'],
        ['Verify with the right query','Basic format reports common all-controller items. Enhanced format selects a controller or aggregates all and distinguishes whether each item applies to every controller. Match query conditions before comparing.'],
        ['Follow the restriction lifecycle','A command can remove a restriction. Survival across a power cycle also depends on the original controller scope and persistence settings. Finally, account for authenticated-unfreeze exceptions and vendor definitions.']]),
      background=bi(['適合學過 OS、Computer Organization 並了解 SSD 基本概念的讀者。以 PCIe 主機管理流程為主要情境；Management Endpoint 只解釋 Base 明載的關係。所有控制器編號、可禁止清單及命令編碼案例均為說明性範例，實際可用項目由裝置能力決定。'],
       ['Assumes operating systems, computer organization and basic SSD knowledge. The main context is PCIe host administration; Management Endpoint coverage is limited to the relationships defined by Base. Controller identifiers, eligibility lists and command encodings are illustrative and depend on actual device support.']))
    OVERVIEWS[REPORT_ID]=bi([
      '可以用一個問題帶著讀：如果只想限制控制器 7 經 Admin Queue 修改 FID 06h，應查哪些能力、送哪些參數、用什麼回覆證明限制成立？沿著這條線，清單、欄位與錯誤碼才有各自的位置。',
      '中文教學先補足每一步的理由，再在問答前整理相關規格圖表的欄位關係。兩種 Log 的長度、控制器編號、代碼清單與 UUID 索引會各自演算，避免只記住縮寫而失去它所描述的對象。'],
      ['Follow one question: to restrict controller 7 from setting FID 06h through its Admin Queue, which capabilities must be checked, which parameters must be sent, and which response confirms the restriction?',
       'This sequence gives each list, selector and result a purpose. Log sizes, controller identifiers, operation codes and UUID indices are kept distinct throughout the examples.'])
    questions=[
      ('eligibility','LID 14h 可禁止清單含 06h，就代表目前已禁止嗎？','Does 06h in a prohibitable list mean it is currently prohibited?',
       '不代表。先看 SCP 確認它是哪種代碼，CNTTS=0 只表示可禁止。要查目前 Admin Queue 限制，應用同一種類並選 CNTTS=1，再配合正確格式與控制器範圍。',
       'No. SCP first determines the code class, and CNTTS=0 reports eligibility only. Query CNTTS=1 for current Admin Queue restrictions using the intended format and controller scope.',['QUERY','BASIC']),
      ('union','全體增強清單回 06 00，能說全部控制器都允許 06h 嗎？','Does enhanced all-controller entry 06 00 mean every controller allows 06h?',
       '不能。這是一筆已回報的 CFI=06h，ACNTL=0 表示至少一台但非全部符合這次查詢。如果 CNTTS=1，它表示只有部分控制器目前禁止；要找是哪台需用特定 CNTLID 查詢。',
       'No. CFI=06h is present and ACNTL=0 means at least one but not all controllers match the query. With CNTTS=1, some controllers prohibit it; query specific CNTLIDs to identify them.',['ENHANCED']),
      ('encoding','要解除 controller7 的 FID06h 限制，能只送 PRHBT=0 嗎？','Is PRHBT=0 alone enough to remove controller 7’s FID06h restriction?',
       '還需保留 SCP=2、OFI=06h、IFC=0、CSEL=1、CSS=7 等相同選擇，並確保執行 Lockdown 的入口仍允許。PRHBT 只決定禁止或允許，不指定對象。',
       'The same selectors are still needed: SCP=2, OFI=06h, IFC=0, CSEL=1 and CSS=7, with an allowed Lockdown path. PRHBT chooses prohibit versus allow, not the target.',['COMMAND','TARGETS']),
      ('persist','LDPE=1，是否每個 CSEL 建立的限制都能跨斷電保留？','Does LDPE=1 preserve prohibitions created with every CSEL across power cycles?',
       '不是。跨 power cycle 的 Lockdown Persistence 規則針對 CSEL=0 的全體限制；CSEL=1、2 仍依其在 power cycle 或後續解除時結束的規則。',
       'No. Lockdown Persistence applies to CSEL=0 all-controller prohibitions. CSEL=1/2 retain their power-cycle-or-allowance lifetime.',['PERSISTENCE']),
      ('offset','增強 Log 第二筆在 byte18，UUID 第二項在 byte64，兩個 2 可以互用嗎？','Can the value two be used interchangeably for the second log descriptor and UUID entry?',
       '不能。CFIDS=2 時增強 Log 第 2 筆從 16+1×2=18 開始；UIDX=2 選 UUID 第 2 項，其 entry 從 64 開始。OT=0 的 Get Log 起點還要 4-byte 對齊，所以讀含 byte18 的資料可從 16 開始。索引和值的位置是不同單位。',
       'No. With CFIDS=2 the second log descriptor starts at 16+1×2=18. UIDX=2 selects UUID entry two at byte64. An OT=0 Get Log offset must also be Dword aligned, so reading data containing byte18 can start at16. Indices and byte positions have different units.',['ENHANCED','QUERY','UUID']),
    ]
    BANK[REPORT_ID]=[dict(id='lockdown-'+k,question=bi(qz,qe),answer=bi(az,ae),sources=[PREFIX+'-'+s for s in src]) for k,qz,qe,az,ae,src in questions]


ROUTE=[
 (305,309,'5.2.13.1.20','5.2.13.1.21',bi('從 Command and Feature Lockdown 標題起：查詢選擇 → 一般清單 → 增強外框與描述器。用 A／B 例子比較全體共同項目與部分控制器項目。','Start at Command and Feature Lockdown: selectors → basic list → enhanced header/descriptors. Use A/B to compare common and partial-controller items.')),
 (431,434,'5.2.16','5.2.17',bi('從 Lockdown command 標題起：用 controller7／FID06h 算 CDW10、14，再分清設定失敗與後續命令被禁止。','Start at Lockdown command: encode CDW10/14 for controller7/FID06h, then distinguish configuration failure from a prohibited later command.')),
 (623,625,'8.1.5','8.1.6',bi('從 Command and Feature Lockdown 標題起，收束介面、能力與持續性規則；以 CSEL0 對照 CSEL1/2 的 power cycle 結果。','Start at Command and Feature Lockdown and connect interfaces, support and persistence. Compare power-cycle results for CSEL0 versus CSEL1/2.')),
]


def render_route(reader):
    lang=reader.lang;reader.figure_label='R';reader.figure_paragraph_no=0
    out=['<section id="spec-route"><h2>'+bi('開著 Spec 的順向報告路徑','A forward route through the specification')[lang]+'</h2>']
    out.append(reader.paragraph(bi('先用本文的全貌、流程與案例說明目的，再依下列 Base PDF 檢視器頁碼向後翻。共用頁只讀指定起始標題到停止標題；不必為每個必要引用往返翻頁，中文教學已集中解釋其欄位與條件。',
      'Establish the purpose with the overview, process and examples, then move forward through the Base PDF viewer pages below. On shared pages, read only between the specified headings. The Chinese tutorial explains necessary referenced fields and conditions without requiring a detour for every reference.')[lang]))
    rows=[[f'R{i} · Base PDF {a}–{b}',f'§{section}',why[lang]+' '+bi(f'在 §{stop} 前停下。',f'Stop before §{stop}.')[lang]] for i,(a,b,section,stop,why) in enumerate(ROUTE,1)]
    out.append(reader.table(bi(['翻頁順序','主範圍','重點與停止位置'],['Page sequence','Primary scope','Focus and stop heading'])[lang],rows))
    out.append('</section>');reader.figure_label=None
    return '\n'.join(out)
