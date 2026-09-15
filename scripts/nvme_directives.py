"""Register the independent Directives and Streams report."""
from pathlib import Path
import json
import re
from scripts.nvme_directives_content import BASE, NVM, REPORT_ID, UNITS, bi

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'STREAMS'

TERMS = {
 'Directives': ('主機與控制器交換附加資訊的機制；依類型定義查詢、設定與 I/O 附加資訊。', 'A mechanism for exchanging additional host/controller information, with type-specific management and I/O semantics.'),
 'Streams': ('以串流編號標示相關寫入資料的 Directive；不直接指定 NAND 實體位置。', 'A Directive that groups related writes using stream identifiers without selecting physical NAND addresses.'),
 'Stream Identifier': ('串流編號；主機選擇的 16-bit 標記，其意義還取決於 namespace、主機身分與共享設定。', 'A host-selected 16-bit grouping label interpreted with namespace, host identity, and sharing configuration.'),
 'Host Identifier': ('主機識別值；用來判斷不同控制器是否服務同一主機，與串流編號不同。', 'The identity used to associate controllers with a host, distinct from a Stream Identifier.'),
 'DTYPE': ('Directive Type；選 Directive 類型。Enable 的外層操作類型與內層目標類型必須分開讀。', 'Directive Type; selects a directive. Enable uses separate outer-operation and inner-target type fields.'),
 'DOPER': ('Directive Operation；在所選類型與命令方向下，指定要執行的操作。', 'Directive Operation; selects an operation within a directive type and command direction.'),
 'DSPEC': ('Directive Specific；含義由類型和操作決定，在 Streams 的 I/O 中放串流編號。', 'Directive Specific; interpreted by type/operation and used as the Stream Identifier in Streams I/O.'),
 'ENDIR': ('Enable Directive；1 要求啟用，0 要求停用 CDW12 選定的類型。', 'Enable Directive; one enables and zero disables the type selected in CDW12.'),
 'DIRS': ('Directives Supported；OACS 中的 Directives 整體支援位元。', 'Directives Supported; the general capability bit in OACS.'),
 'SDIRS': ('Streams Directive Supported；控制器是否支援 Streams。', 'Streams Directive Supported; whether the controller supports Streams.'),
 'SDIRE': ('Streams Directive Enabled；指定 namespace 目前是否已啟用 Streams。', 'Streams Directive Enabled; whether Streams is enabled for the selected namespace.'),
 'SDIRCLR': ('Streams Directive Persistent Across Controller Level Resets；Streams 此位元為 0，仍須讀多控制器的保留例外。', 'Streams persistence across Controller Level Resets; zero for Streams, interpreted with the multi-controller exception.'),
 'EXHID': ('Enable Extended Host Identifier；0 選 64-bit，1 選 128-bit 身分格式。', 'Enable Extended Host Identifier; zero selects 64 bits and one selects 128 bits.'),
 'HOSTID': ('Host Identifier 資料結構中的實際身分值。', 'The actual identity value in the Host Identifier data structure.'),
 'HIDS': ('Host Identifier Support；CTRATT 中表示支援 128-bit 身分的位元。', 'Host Identifier Support; the CTRATT bit advertising 128-bit identity support.'),
 'MSL': ('Max Streams Limit；整個 NVM subsystem 同時開啟串流的上限。', 'Max Streams Limit; the subsystem-wide concurrent-open limit.'),
 'NSSA': ('NVM Subsystem Streams Available；未分配成 namespace 專用的資源池大小，不等於其中完全閒置的數量。', 'NVM Subsystem Streams Available; the non-exclusively allocated pool size, not its idle-resource count.'),
 'NSSO': ('NVM Subsystem Streams Open；使用非專用資源池的開啟串流數。', 'NVM Subsystem Streams Open; open streams using the nonexclusive pool.'),
 'NSSC': ('NVM Subsystem Stream Capability；包含主機身分要求與串流共享能力。', 'NVM Subsystem Stream Capability; contains identity requirements and sharing capabilities.'),
 'SRNZID': ('Streams Require Non-Zero Host Identifier；1 表示啟用前必須先登記非零主機身分。', 'Streams Require Non-Zero Host Identifier; one requires registration before enablement.'),
 'SSID': ('Shared Stream Identifiers；決定不同非零主機身分是否可共享同一 namespace 的同號串流。', 'Shared Stream Identifiers; controls sharing of equal identifiers across nonzero host identities within a namespace.'),
 'NSA': ('Namespace Streams Allocated；指定 namespace 與可見主機關聯下的專用配置數，也用於 Allocate 的完成回覆。', 'Namespace Streams Allocated; the exclusive allocation for the namespace and visible host association, also returned by Allocate.'),
 'NSR': ('Namespace Streams Requested；主機要求的專用資源數，直接計數。', 'Namespace Streams Requested; the directly encoded exclusive resource request count.'),
 'NSO': ('Namespace Streams Open；指定 namespace 與可見主機關聯下的開啟串流數。', 'Namespace Streams Open; the open count for the selected namespace and visible host association.'),
 'OSC': ('Open Stream Count；Get Status 清單中的開啟數量，後面才是各串流編號。', 'Open Stream Count; the status-list count preceding the actual identifiers.'),
 'SWS': ('Stream Write Size；在 NVM Command Set 以 logical blocks 表示最佳寫入的對齊與大小單位。', 'Stream Write Size; the optimal write alignment/size unit, measured in logical blocks for NVM.'),
 'SGS': ('Stream Granularity Size；以 SWS 為單位表示媒體配置的粒度大小。', 'Stream Granularity Size; allocation granularity measured in SWS units.'),
 'CETYPE': ('Command Extension Type；決定 Write 的命令擴充與 CDW13 格式，本篇例子使用 0。', 'Command Extension Type; selects the Write extension and CDW13 layout; examples here use zero.'),
 'NUMD': ('Number of Dwords；有資料傳輸時，欄位保存 4-byte 單位的數量減 1。', 'Number of Dwords; for buffered transfers, encodes the count of four-byte units minus one.'),
 'NLB': ('Number of Logical Blocks；Write 的區塊數量減 1。', 'Number of Logical Blocks; the Write block count minus one.'),
 'MDTS': ('Maximum Data Transfer Size；非零時以最小記憶體頁大小乘 2 的冪表示最大傳輸量。', 'Maximum Data Transfer Size; nonzero values encode a power-of-two multiple of the minimum memory page size.'),
 'bit vector': ('位元向量；每個 bit 的位置對應一種類型，bit 值回答支援、啟用或保留狀態。', 'A bit vector maps each bit position to a type and each bit value to a support, enablement, or persistence state.'),
 'payload': ('命令伴隨傳輸的資料內容；命令欄位與 CQE 回覆不因此都算作 payload。', 'Data carried by a command transfer, distinct from command fields and completion values.'),
 'alignment': ('對齊；起始位置符合指定單位的倍數，和總長度是否為倍數要分開檢查。', 'Alignment; the start position is a multiple of the required unit, checked separately from transfer length.'),
 'granularity': ('粒度；用來安排寫入或配置的一個大小單位，不是資源個數。', 'Granularity; a size unit used for writes or allocation, not a resource count.'),
 'buffer': ('記憶體緩衝區；主機準備用來提供或接收資料的空間。', 'A memory buffer prepared by the host to supply or receive data.'),
 'Flexible Data Placement': ('另一種資料配置能力；本篇只使用「已啟用它的 Endurance Group 內不能啟用 Streams」這項限制。', 'A separate placement capability; this report uses only its mutual-exclusion constraint with Streams.'),
 'Endurance Group': ('耐久度群組；namespace 所屬的媒體管理範圍，本篇只用它判斷 Streams 的啟用限制。', 'A media-management grouping containing namespaces, used here only for the Streams enablement restriction.'),
}


def install(reports, titles, modules, glossaries, images):
    from scripts.nvme_lessons import LESSONS
    from scripts.nvme_course_walkthroughs import COURSES
    from scripts.nvme_reader_context import REPORT_CONTEXT
    from scripts.nvme_overviews import OVERVIEWS
    from scripts.nvme_review_bank import BANK
    figures = [f for f in json.loads((ROOT/'.ai/nvme-report/figure-table-register.json').read_text())['entries'] if f['report_id'] == REPORT_ID]
    report = dict(prefix=PREFIX, source_id=BASE, scope_entry='STREAMS-BASE-INCLUDE', date='2026-09-15',
                  title_zh='NVMe Directives 與 Streams：從主機分組到寫入與資源管理',
                  title_en='NVMe Directives and Streams: Host Grouping, Writes, and Resources',
                  range='Base §8.1.9（排除 §8.1.9.4）、§5.2.7、§5.2.8、§5.2.30.1.35（PCIe）及 NVM §5.13',
                  range_en='Base §8.1.9 excluding §8.1.9.4, §§5.2.7/5.2.8, §5.2.30.1.35 (PCIe), and NVM §5.13',
                  course_claim_first=True, claims=[])
    modules[REPORT_ID] = []
    for u in UNITS:
        cid = PREFIX+'-'+u['key'].upper()
        mid = 'streams-'+u['key']
        printed = u['pages'] if u['source'] == NVM else re.sub(r'\d+', lambda m: str(int(m[0])-26), u['pages'])
        report['claims'].append(dict(key=u['key'].upper(), source_id=u['source'], section=u['section'],
          printed_pages=printed, pdf_pages=u['pages'], normative_keyword='none',
          zh_tw=u['summary']['zh'], en=u['summary']['en'],
          scope_entry_id='STREAMS-'+('NVM' if u['source']==NVM else 'BASE')+'-INCLUDE'))
        titles[cid] = (u['title']['zh'], u['title']['en'])
        modules[REPORT_ID].append(dict(id=mid, title=u['title'], lead=u['summary'], sources=[cid],
          figures=[int(f['number']) for f in figures if f['teaching_module']==mid],
          rows=bi([], []), example=u['example'], pitfall=bi('', '')))
        LESSONS[mid] = dict(headers=bi(['問題','判斷','例子'], ['Question','Interpretation','Example']),
                            teaching=[s[1] for s in u['steps']], reading=u['reading'])
        COURSES[mid] = dict(title=u['title']['zh'], steps=u['steps'], outcome=u['example']['zh'])
    reports[REPORT_ID] = report
    glossaries[REPORT_ID] = [(t, '') for t in TERMS]
    images[REPORT_ID] = dict(zh='posts/2026/dogMC_title.jpg', en='posts/2026/cat_title.jpg')
    REPORT_CONTEXT[REPORT_ID] = dict(
      intro=bi('這篇說明主機如何把「哪些資料屬於同一組」告訴 SSD。先建立主機、控制器、namespace 與串流的關係，再走過能力查詢、啟用、資源配置、Write 與釋放；最後看相同編號在不同路徑下的含義，以及 SWS／SGS 如何影響資料安排。',
               'This report explains how a host tells an SSD which data belongs together. Establish the relationships among host, controller, namespace, and stream, then follow capability checks, enablement, allocation, writes, and release. Finally examine identifier sharing across paths and the meaning of SWS/SGS for data organization.'),
      axes=bi([
       ['資料分組的目的','Stream Identifier 為寫入補上資料關聯，LBA 仍決定寫入位置。先理解這個分工，才不會把串流當成另一個 namespace。'],
       ['管理流程與資料流','查能力、登記身分、啟用功能與配置資源是準備工作；真正使用串流的是帶標記的 Write。管理命令不必跟每一筆資料同步重送。'],
       ['身分與資源的共享範圍','Host Identifier 與 SSID 決定哪些路徑共用串流；NSA、NSSA、NSO 則區分容量、資源池與目前使用狀態。'],
       ['大小安排與生命週期','SWS／SGS 協助安排寫入與解除配置；Release、停用及 reset 決定追蹤狀態何時結束，這和使用者資料是否仍存在不同。']],
       [['Why group data?','A Stream Identifier adds a relationship between writes while LBA still selects the destination. A stream is not another namespace.'],
        ['Management and data flow','Capability queries, identity registration, enablement, and allocation prepare the system; tagged Writes actually use streams. Management commands are not repeated for every payload.'],
        ['Identity and resource sharing','Host Identifier and SSID determine which paths share a stream. NSA, NSSA, and NSO distinguish capacity, the resource pool, and current use.'],
        ['Size and lifetime','SWS/SGS guide writes and deallocation. Release, disablement, and reset affect tracking state independently of the continued existence of user data.']]),
      background=bi(['讀者只需有 OS、Computer Organization 與 SSD 基本概念。本文以 PCIe 控制器為情境，完整涵蓋指定 Directives／Streams 範圍；Data Placement §8.1.9.4 不展開。例子的數量、LBA 與主機 A／B 是說明性設定，實際能力以裝置回覆為準。'],
                     ['The assumed background is operating systems, computer organization, and basic SSD concepts. Examples use PCIe controllers and cover the specified Directives/Streams scope, excluding Data Placement §8.1.9.4. Counts, LBAs, and host labels are illustrative; actual capabilities come from the device.']))
    OVERVIEWS[REPORT_ID] = bi([
      '可以把這篇想成一次完整的資料使用週期：先決定哪幾筆資料有關，再確認控制器支援、各路徑的主機身分與啟用狀態，接著選擇資源來源。Write 帶入編號時才產生串流活動；資料不再屬於這次群組時，再結束編號的使用。',
      '兩個數字相同不一定代表同一件事：相同 Stream Identifier 可能屬於不同主機，SWS=8 與 NSA=8 更分別是資料大小和資源個數。後面的例子會逐步固定其他條件，只改一項設定，觀察意義如何變化。'],
      ['Follow a complete data-use cycle: decide which data is related, verify support, establish host identities and enablement, and choose a resource source. Writes create stream activity; release ends an identifier’s current grouping when it is no longer needed.',
       'Equal numbers need not mean equal things: the same Stream Identifier may belong to different hosts, and SWS=8 versus NSA=8 means data size versus resource count. The examples hold other conditions fixed while changing one factor.'])
    questions = [
      ('stages', 'SDIRS=1、NSA=3、NSO=0，這些值互相矛盾嗎？', 'Are SDIRS=1, NSA=3, and NSO=0 contradictory?',
       '不矛盾。它們分別是支援能力、已配置專用容量與目前開啟數。主機可以已啟用且配置容量，但還沒有用任何串流編號寫入。',
       'No. They describe support, exclusive capacity, and the current open count. The host can have enabled and allocated capacity without yet issuing a stream-tagged write.', ['ENABLE','RESOURCES']),
      ('host-zero', 'C1、C2 都是 Host Identifier=0h，可否當成同一主機的 stream 7？', 'Do C1 and C2 with Host Identifier=0h share host identity for stream 7?',
       '不能只因兩個值都是 0h 就合併。0h 表示不建立跨控制器主機關聯；先登記相同非零識別值，才符合共同主機的判斷前提。',
       'No. Zero explicitly does not establish a cross-controller host association. Matching nonzero identities are needed for that common-host relationship.', ['HOST','SHARING']),
      ('allocation', '已取得 3 個專用資源，再送 NSR=2，能變成 5 個嗎？', 'After receiving three exclusive resources, can another NSR=2 request make five?',
       '不能。已有專用配置時重複申請會被拒絕；要先歸還原配置，再請求完整的新數量，並檢查實際授予數。釋放一個編號不等於歸還整份配置。',
       'No. A request while that exclusive allocation exists is rejected. Release the allocation, request the full new count, and inspect the grant. Releasing one identifier is not releasing the whole allocation.', ['RESOURCES','LIFETIME']),
      ('sizing', '4 KiB/block、SWS=8、SGS=4，LBA 136 起的 16-block Write 與同起點解除配置，各符合哪個大小建議？', 'With 4 KiB/block, SWS=8, and SGS=4, which size recommendations are met by a 16-block Write and deallocation starting at LBA 136?',
       'Write 的起點與長度都是 8 的倍數，符合 SWS；Stream Granularity 是 32 blocks，起點 136 與長度 16 都不是 32 的倍數，所以不符合該解除配置最佳化建議。這不是在宣告命令必須失敗。',
       'The Write start and length are multiples of eight and satisfy SWS. Stream granularity is 32 blocks; neither 136 nor 16 is a multiple of 32, so the deallocation optimization recommendation is not met. This does not declare the command invalid.', ['SIZES']),
      ('scope', '整體 Get Status 只列出一次編號 7，能證明只有一個 namespace 正在用它嗎？', 'If subsystem Get Status lists identifier 7 once, does that prove only one namespace uses it?',
       '不能。整體查詢只涵蓋非專用資源，跨 namespace 的重複編號只回一次。要知道某個 namespace 的狀態，需要用該 NSID 和正確主機關聯查詢。',
       'No. The subsystem query covers nonexclusive resources and deduplicates equal identifiers across namespaces. Query the particular NSID under the appropriate host association for its details.', ['LIFETIME']),
    ]
    BANK[REPORT_ID] = [dict(id='streams-'+key, question=bi(qz,qe), answer=bi(az,ae), sources=[PREFIX+'-'+s for s in src])
                       for key,qz,qe,az,ae,src in questions]


def render_route(reader):
    """Post-only forward page route, based on the supplied PDF's actual pages."""
    lang=reader.lang
    reader.figure_label='R'; reader.figure_paragraph_no=0
    out=['<section id="spec-route"><h2>'+bi('開著 Spec 的報告路徑','The live specification route')[lang]+'</h2>']
    out.append(reader.paragraph(bi('先用本文的例子建立全貌，再開 Base PDF 第 227 頁。下面依實際 PDF 頁碼往後走，最後只切換一次到 NVM。章節共用同一頁時，以標題為停止位置；不要使用目錄中的舊頁碼代替 PDF 檢視器頁碼。',
      'Use the examples to establish the overall picture, then open Base at PDF page 227. Proceed forward through the viewer pages below and switch once to NVM. On shared pages, stop at the named heading; use viewer pages rather than stale contents-page numbers.')[lang]))
    rows=bi([
      ['R1 · Base PDF 227–228','§5.2.7 → §5.2.8','先比較 Receive／Send 的 DPTR、NUMD、DTYPE／DOPER；在 §5.2.9 Firmware Commit 前停下。'],
      ['R2 · Base PDF 534–536','§5.2.30.1.35 → .35.1','讀 Host Identifier 與 PCIe 規則：EXHID、HOSTID、0h、非零身分、不可保存；在 .35.2 標題前停下。'],
      ['R3 · Base PDF 642–646','§8.1.9 → §8.1.9.2','從 Directives 標題開始；用 702／703 看類型，再用 704–707 看查詢與啟用。'],
      ['R4 · Base PDF 646–653','§8.1.9.3','708 大小組成 → 709 操作 → 710 共享 → 711–715 參數／狀態／配置 → 兩個 Release；在 §8.1.9.4 前停下。'],
      ['R5 · NVM PDF 175','§5.13','確認 SWS 的單位是 logical blocks，帶入 4 KiB、SWS=8、SGS=4 完成換算。']],
     [['R1 · Base PDF 227–228','§5.2.7 → §5.2.8','Compare DPTR, NUMD, and DTYPE/DOPER for Receive/Send; stop before §5.2.9 Firmware Commit.'],
      ['R2 · Base PDF 534–536','§5.2.30.1.35 → .35.1','Read EXHID, HOSTID, zero/nonzero identity, and non-saveability under PCIe; stop before .35.2.'],
      ['R3 · Base PDF 642–646','§8.1.9 → §8.1.9.2','Start at Directives. Use 702/703 for types, then 704–707 for queries and enablement.'],
      ['R4 · Base PDF 646–653','§8.1.9.3','708 sizes → 709 operations → 710 sharing → 711–715 parameters/status/allocation → the two releases. Stop before §8.1.9.4.'],
      ['R5 · NVM PDF 175','§5.13','Confirm SWS is in logical blocks and finish the 4 KiB, SWS=8, SGS=4 calculation.']])[lang]
    out.append(reader.table(bi(['翻頁順序','章節','在這裡講清楚什麼'],['Page sequence','Sections','What to explain here'])[lang], rows))
    out.append('</section>'); reader.figure_label=None
    return '\n'.join(out)
