"""Register PEL editions and a Base-to-NVM forward presentation route."""
from scripts.nvme_report_extension import bi,install_report
from scripts.nvme_pel_content import REPORT_ID,UNITS
from scripts.nvme_pel_terms import TERMS

CONFIG=dict(id=REPORT_ID,prefix='PEL',date='2026-09-25',
 title=bi('NVMe Persistent Event Log：讀取流程、事件格式與歷史判讀',
 'NVMe Persistent Event Log: Retrieval, Event Formats, and Historical Interpretation'),
 range=bi('Base §5.2.13.1.14（LID 0Dh）＋ NVM Command Set §4.1.4.4',
 'Base §5.2.13.1.14 (LID 0Dh) + NVM Command Set §4.1.4.4'),
 context=dict(intro=bi(
 '裝置重設後，如何知道之前發生過什麼？Persistent Event Log 保存跨重設的重要事件，將健康快照、韌體更新、電源、namespace 與設定變更放進共同的紀錄格式。本篇先說明如何讀出同一份資料，再學會把時間、對象、參數與結果連起來，同時分辨紀錄能證明什麼、不能證明什麼。',
 'After a device resets, how can we tell what happened before it? Persistent Event Log retains significant events in a common format, including health snapshots, firmware updates, power events, namespace changes and configuration. This report first explains consistent retrieval, then connects time, target, parameters and outcomes while respecting what the evidence can establish.'),
 axes=bi([
 ['這份歷史保存什麼','事件種類支援、保存上限與實際內容是三件事。先認識 subsystem 範圍、持久性與遺漏的可能性，避免把有限紀錄當作完整流水帳。'],
 ['一次讀取的生命週期','建立 context → 讀 header → 分段讀取 → 比對 generation → 釋放。新事件與正在讀的事件集合分開，才能理解為什麼需要context。'],
 ['資料的三層結構','外層log header描述整份報告；共同event header描述一筆事件；ED保存該種類的內容。每一層長度和版本各有用途。'],
 ['從事件還原合理的關係','按健康、時間／重設、儲存變更、清除、硬體及設定分組。一起看對象、動作和結果，不以單一名稱、百分比或時間戳推論成功。'],
 ['Base 與 NVM 怎麼接起來','Base提供Namespace Change外框，NVM補定FLBAS與DPS。最後再學廠商擴充，遇到未知內容也能辨認範圍並保留原始資料。']],
 [['What the history preserves','Support, storage limits and actual contents are distinct. Understand subsystem scope, persistence and possible omissions before treating the log as a complete trace.'],
 ['The retrieval lifecycle','Establish context → read header → retrieve chunks → compare generation → release. Separate newly logged events from the fixed set being retrieved.'],
 ['Three layers of data','The log header describes the report, the common event header describes one record, and ED contains type-specific data. Lengths and revisions belong to different layers.'],
 ['Build justified relationships','Group health, time/reset, storage changes, sanitization, hardware and configuration. Combine target, action and result rather than inferring success from one name, percentage or timestamp.'],
 ['Connecting Base and NVM','Base provides the Namespace Change envelope; NVM specifies FLBAS/DPS. Vendor extensions complete the picture while unknown content remains bounded and preserved.']]),
 background=bi([
 '適合已學過OS、Computer Organization並了解SSD基本概念的讀者。文中的控制器A／B、namespace7及示範數值只用來說明規則，不代表每台裝置都有相同配置。',
 '中文教學版以循序推理與欄位案例深入學習；中英文post先建立全局觀念，再接續順向Spec報告路徑。主範圍固定為上述兩節，其他來源只補足理解事件所需的欄位。'],
 ['Assumes operating systems, computer organization and basic SSD concepts. Controllers A/B, namespace7 and numeric examples are illustrative, not assumed hardware configurations.',
 'The Chinese tutorial develops the reasoning and field examples; the equivalent posts establish a global view and then provide a forward Spec route. Other references supply only fields needed to interpret these events.'])),
 connections=bi([
 '可以把整篇想成五個連續問題：這台裝置會記什麼；這次讀到哪一份；每筆從哪裡開始；事件內容代表什麼；最後能做出什麼有根據的判斷。前一個問題沒弄清楚，後面的數字就容易讀錯。',
 '本文用流程圖說明context，用資料區塊圖說明長度，用時間與對象的對比解釋事件。規格欄位很多時採分組表格，共用格式只解釋一次，再由每張圖的獨立案例連回。'],
 ['Follow five questions: what can this device log, which report am I reading, where does each record begin, what does its payload mean, and what conclusion does the evidence support?',
 'Use a lifecycle diagram for contexts, a byte-layout diagram for lengths, and time/target comparisons for events. Group related fields and explain shared structures once, with a distinct example for each source figure.']),questions=[])

for key,qz,qe,az,ae,src in [
 ('existing','ACT3成功回RCE=0，要再送ACT1才能讀事件嗎？','After successful ACT3 returns RCE=0, is ACT1 still needed?',
 '不需要。RCE0表示命令處理前沒有context，ACT3已建立並回header；接續用ACT0。這時再送ACT1，反而因已有context而得到Command Sequence Error。',
 'No. RCE=0 describes absence before processing; ACT3 has established the context and returned the header. Continue with ACT0. ACT1 would now fail because a context exists.',['CONTEXT']),
 ('length','EHL21、VSIL4、EL20時，事件是44還是48 bytes？','With EHL21, VSIL4 and EL20, is the record 44 or 48 bytes?',
 '44。EHL+3是24-byte header；EL20已含4-byte VSI，ED只剩16。48把VSI算了兩次，會錯過下一筆的開頭。',
 '44. EHL+3 is the 24-byte header; EL20 already includes four VSI bytes, leaving sixteen ED bytes. 48 double-counts VSI and misses the next record’s start.',['LAYOUT']),
 ('snapshot','PEL的Telemetry header寫Data Area3有9個blocks，這筆事件含那些資料嗎？','Does a PEL telemetry header naming nine data blocks include those blocks?',
 '不含。ET0C只複製前512 bytes header，提供當時的邊界、原因和generation等資料；不能當成完整Telemetry內容，也不保證現在還能取得相同版本。',
 'No. ET0C copies only the first512 header bytes, preserving historical boundaries, reason and generation. It neither contains the full data nor guarantees the same capture remains available.',['HEALTH']),
 ('mapping','事件byte32=12h就能說這份namespace每個LBA有18 bytes嗎？','Does event byte32=12h imply an 18-byte LBA?',
 '不能。有效FLBAS裡12h代表format index2與延伸LBA metadata，不是大小18。還要先確認操作不是Delete All；實際資料與metadata大小來自所選格式定義。',
 'No. Valid FLBAS12h selects format index2 and extended metadata, not size18. First exclude Delete All, where the field is reserved; actual sizes come from the selected format definition.',['NAMESPACE','NAMESPACE-3']),
 ('completion','Sanitize completion事件的SPROG=FFFFh，是否能證明已成功清除？','Does SPROG=FFFFh in a sanitize-completion event prove successful sanitization?',
 '不能。先讀SOS；例如SOS3就是失敗。FFFFh也用在非處理狀態與Media Verification，這不是一個可獨立判斷成功的百分比。',
 'No. Read SOS: for example, 3 means failure. FFFFh also appears outside processing and during Media Verification; it is not a standalone success percentage.',['SANITIZE','SANITIZE-2']),
 ('missing','找不到某次設定事件，就能說主機沒改過設定嗎？','Does absence of a feature event prove the host never changed that setting?',
 '不能。先看該Feature的記錄政策與支援；有些禁止用ET0B記錄，有些是選用或不建議。再考慮容量淘汰、頻率抑制，以及目前context是否早於那次變更。',
 'No. Check the feature’s logging policy and support first: it may be prohibited, optional or discouraged. Then consider eviction, frequency suppression and whether the current context predates the change.',['FEATURES','PURPOSE','CONTEXT']),
]:CONFIG['questions'].append(dict(key=key,question=bi(qz,qe),answer=bi(az,ae),sources=src))

def install(reports,titles,modules,glossaries,images):
    install_report(CONFIG,UNITS,TERMS,reports,titles,modules,glossaries,images)

ROUTE=[
 ('Base',270,272,'5.2.13.1.14','Figure233',bi('先講保存範圍與限制，再沿ACT四種動作說明context生命週期。270頁從本節標題開始，略過前面的ANA表尾。','Start at the section heading, after the preceding table tail. Explain retention/limits and the four ACT operations.')),
 ('Base',273,277,'Figure233','5.2.13.1.14.2.1',bi('由log header走到共同event header，再用ECRH與事件類型表收束。只讀本篇範圍內的欄位。','Walk from the log header to the event header, then ECRH and the type table. Use the scoped fields taught here.')),
 ('Base',278,284,'5.2.13.1.14.2.1','5.2.13.1.14.2.6',bi('SMART快照→韌體→時鐘→重設→硬體。先說每種事件能證明什麼，再看該種附加資料。','Cover SMART, firmware, time, reset and hardware; state what each establishes before reading its payload.')),
 ('Base',284,290,'5.2.13.1.14.2.6','5.2.13.1.14.2.13',bi('Namespace、Format、Sanitize與Set Feature，再到Telemetry。Figure247的FLBAS／DPS先說用途，最後切NVM時補格式。','Cover Namespace, Format, Sanitize, Set Feature and Telemetry. Introduce FLBAS/DPS here and complete their decoding in the final NVM stop.')),
 ('Base',291,296,'5.2.13.1.14.2.13','5.2.13.1.15',bi('溫度、Media Verification、Personality、實體映射與廠商描述子。296頁讀完TCG事件段落，在下一log標題前停止。','Finish thermal, verification, personality, entity mappings and vendor descriptors. Stop after the TCG paragraph, before the next log section.')),
 ('NVM',76,77,'4.1.4.4','4.1.4.5',bi('只切一次文件，從Persistent Event Log標題讀到Figure112，補齊Create／單一Delete／Delete All的FLBAS與DPS來源。','Switch documents once. Read the Persistent Event Log heading and Figure112 to finish FLBAS/DPS origins for Create, single Delete and Delete All.')),
]

def render_route(reader):
    lang=reader.lang;reader.figure_label='R';reader.figure_paragraph_no=0
    out=['<section id="spec-route"><h2>'+bi('開著 Spec 的順向報告路徑','A forward route through the specification')[lang]+'</h2>']
    out.append(reader.paragraph(bi('用上面的全貌與案例先講清楚問題，再依PDF檢視器頁碼往後讀。Base完整走完這一節後，只切一次到NVM；中文教學已解釋必要引用，不需要為每個欄位來回翻頁。',
        'Frame the problem using the overview and examples, then follow PDF viewer page numbers forward. Finish the Base section and switch to NVM once. The Chinese tutorial explains necessary references without repeated page detours.')[lang]))
    rows=[]
    for i,(book,start,end,section,stop,focus) in enumerate(ROUTE,1):
        rows.append([f'R{i} · {book} PDF {start}–{end}',section,focus[lang]+' '+bi(f'停止於 {stop} 之前。',f'Stop before {stop}.')[lang]])
    out.append(reader.table(bi(['頁碼順序','起點標題','講解重點與停止位置'],['Page order','Start heading','Focus and stop heading'])[lang],rows))
    out.append('</section>');reader.figure_label=None
    return '\n'.join(out)
