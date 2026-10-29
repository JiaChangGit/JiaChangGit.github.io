"""Authored openings for the two reports in the approved shared-style scope."""
from html import escape as e
from scripts.nvme_reader_visuals import diagram, box, arrow

def opening(r):
    zh=r.lang=='zh'
    def bi(a,b):return a if zh else b
    def link(module,label):
        local=any(m['id']==module for m in r.modules)
        url=('#module-'+module if local else '/DOCS/nvme-spec-report/'+r.id+'/tutorial-zh-tw.html#module-'+module)
        return '<a href="'+e(url,quote=True)+'">'+e(label)+'</a>'
    out=['<section id="topic-overview" class="topic-overview"><h2 id="main-ideas">'+bi('先沿一筆命令看全貌','Start with one command')+'</h2>']
    if r.id=='pcie-transport-1.4':
        elements=[box(20,25,290,75,[bi('主機記憶體：SQ／CQ','Host memory: SQ / CQ')]),box(450,25,290,75,[bi('NVMe 控制器','NVMe controller')]),
                  box(235,280,300,70,[bi('BAR 指向的 Register 空間','BAR-mapped register space')]),
                  arrow(310,60,450,60,bi('命令與完成項目的記憶體交換','Queue-entry memory transfers')),
                  arrow(165,100,310,280,bi('主機更新 Doorbell','Host updates doorbells')),
                  arrow(450,280,595,100,bi('控制器接收通知','Controller receives notification'))]
        title=bi('命令放在主機記憶體，Doorbell 通知佇列位置','Commands reside in memory; doorbells announce queue positions')
        out.append(diagram(title,bi('作者依 NVMe over PCIe Transport 1.4 繪製。SQ 是 Submission Queue（提交佇列），CQ 是 Completion Queue（完成佇列）；BAR 是 Base Address Register（基底位址暫存器）。圖中先分開主機記憶體與控制器暫存器；完整時序見下文。','Author diagram based on NVMe over PCIe Transport 1.4. SQ means Submission Queue; CQ means Completion Queue; BAR means Base Address Register. This view separates host memory from controller registers; the detailed sequence follows in the text.'),elements,height=370))
        out.append(r.paragraph(bi('主機先把命令放進 SQ（提交佇列），再更新 SQ Tail Doorbell，通知控制器新的佇列位置。控制器取走並執行命令後，將完成結果放進 CQ（完成佇列）。Doorbell 不攜帶命令本體；中斷則提示主機有工作要處理，命令結果仍要讀 CQE。','The host writes a command to the SQ (Submission Queue), then updates the SQ Tail Doorbell to announce the new queue position. The controller fetches and executes the command, then places its result in the CQ (Completion Queue). The doorbell does not carry the command; the host reads the CQE to obtain the result.')))
        out.append(r.paragraph(bi('Base 2.4 定義共通的命令與佇列模型；本文補上 PCIe 的位址、存取及通知方式。Transport 1.4 §1.5（p.7）引用 PCIe Base 6.2，本站 PCIe 課程則使用 6.0。查 PCIe 專屬細節時，請先確認適用版本。','Base 2.4 defines the shared command/queue model; this report supplies PCIe addresses, accesses, and notifications. Transport 1.4 §1.5 (p.7) references PCIe Base 6.2, while this site’s PCIe course uses 6.0. Check the applicable version when reading PCIe-specific details.')))
        items=[('mmio-doorbell',bi('第一步：通知要寫到哪裡？','First: where does the notification go?'),bi('先沿 §3.1 找到 BAR0／BAR1 與存取規則，再看 §3.1.2：DSTRD 和 Queue Identifier 如何決定 Doorbell 的位移。','Follow §3.1 into BAR0/BAR1 and access rules, then §3.1.2 for DSTRD and queue-ID offsets.')),
               ('command',bi('第二步：命令與結果怎麼往返？','Next: how do command and result travel?'),bi('沿 §3.4 的時序，依次看主機寫入 SQE、更新 Doorbell，控制器取命令、寫入 CQE，以及主機更新 CQ Head。SQE 與 CQE 分別是佇列中的命令項目和完成項目。','Follow §3.4 through SQE, doorbell, fetch, CQE, and CQ-head update. SQE/CQE are submission/completion entries.')),
               ('interrupts',bi('第三步：收到通知後要讀什麼？','Then: what follows an interrupt?'),bi('接著看中斷模式與完成佇列處理，並分開判讀 PCIe 錯誤和 NVMe 命令狀態。接收端眼圖量測則是另一個診斷入口。','Continue into interrupt mode and completion processing, keeping PCIe errors separate from NVMe command status. Receiver eye measurements are a separate diagnostic path.'))]
        claims=['PCIE14-SCOPE','PCIE14-MMIO','PCIE14-DOORBELL','PCIE14-COMMAND']
    else:
        elements=[box(20,25,330,80,[bi('已選格式：資料／metadata','Selected format: data / metadata')]),box(410,25,330,80,[bi('Read／Write：範圍與指標','Read / Write: range and pointers')]),
                  box(410,270,330,80,[bi('完成狀態與資料保證','Completion and data guarantees')]),box(20,270,330,80,[bi('能力、條件與適用範圍','Capabilities and conditions')]),
                  arrow(350,65,410,65),arrow(575,105,575,270),arrow(410,310,350,310)]
        title=bi('先讀既有格式，再理解命令及完成結果','Read the selected format before the command and result')
        out.append(diagram(title,bi('作者繪製的閱讀關係圖。LBA 是 Logical Block Address（邏輯區塊位址），metadata 是隨區塊保存的附加資料；讀取現有格式不表示每次 I/O 前都要重新 Format。','Author reading map. LBA means Logical Block Address; metadata is additional block-associated information. The map does not require reformatting before each I/O.'),elements,height=375))
        out.append(r.paragraph(bi('解讀 Read 或 Write 時，先確認 namespace（邏輯儲存空間）使用的格式。接著用 LBA（邏輯區塊位址）、區塊數和資料指標描述存取範圍，再依命令及其條件確認完成狀態、持久性、原子性與資料保護。','For a Read or Write, first establish the namespace (logical storage space) format. Then interpret the LBA (Logical Block Address), block count, and data pointers, followed by completion status and the required persistence, atomicity, and protection conditions.')))
        out.append(r.paragraph(bi('Base 2.4 定義共通的提交與完成機制；NVM Command Set 1.3 補上區塊命令的語意。以下先沿一筆資料操作閱讀，再按主題查管理與進階功能。','Base 2.4 supplies the common submission/completion mechanism; NVM Command Set 1.3 adds block-command semantics. Follow one data operation first, then the management and advanced topics; they are not mandatory stages of every I/O.')))
        items=[('nvmcs-identify',bi('第一步：同一個 namespace，該讀哪份 Identify？','First: which Identify data describes this namespace?'),bi('先連起共通的 namespace 資訊、NVM 專屬資訊與格式清單，確認資料大小和 metadata 配置。','Connect common namespace data, NVM-specific data, and format lists to establish data size and metadata arrangement.')),
               ('nvmcs-read-write',bi('第二步：從範圍走到傳輸量','Next: connect the range to transfer size'),bi('先用 SLBA、從 0 起算的 NLB 與資料指標解讀 Read／Write，再依所選格式追蹤資料與 metadata。','Read SLBA, zero-based NLB, and data pointers, then trace data and metadata under the selected format.')),
               ('nvmcs-atomic',bi('第三步：完成後具備哪些保證？','Then: which guarantees apply?'),bi('分別確認正常原子性、斷電原子性、順序與資料保護的適用條件；Copy 與資源管理則沿各自主題閱讀。','Apply normal/power-fail atomicity, ordering, and protection under their conditions; follow Copy and resource management in their own sections.'))]
        claims=['NVMCS13-FOUNDATION','NVMCS13-IDENTIFY','NVMCS13-METADATA','NVMCS13-READ-WRITE']
    out.append('<div class="st-route"><h3>'+bi('沿這條路線讀下去','Continue along this reading route')+'</h3>')
    for target,title,explanation in items:
        out.append('<h4>'+link(target,title)+'</h4>'+r.paragraph(explanation))
    out.append('</div>')
    # Cross-series links point to the matching language, with relative paths in
    # the standalone tutorial so the published HTML remains usable offline.
    locale='zh-tw' if zh else 'en'
    if r.id=='pcie-transport-1.4':
        q=('../../nvme-question-bank/doorbells.html#q-027' if r.tutorial else '/nvme/question-bank/doorbells/'+locale+'/#q-027')
        f=('../../nvme-quick-reference/command.html#exercise-command-01' if r.tutorial else '/nvme/figure-reference/command/'+locale+'/#exercise-command-01')
        links=[(q,bi('自問自答：CQ 繞回後如何用 Phase 辨識新結果？','Self-study: identify new completions after CQ wrap')),
               (f,bi('圖表情境：CID 相同時，如何配對完成項目？','Figure scenario: match completions with the same CID'))]
    else:
        q=('../../nvme-question-bank/data-io.html#q-321' if r.tutorial else '/nvme/question-bank/data-io/'+locale+'/#q-321')
        f=('../../nvme-quick-reference/io.html#exercise-io-01' if r.tutorial else '/nvme/figure-reference/io/'+locale+'/#exercise-io-01')
        links=[(q,bi('自問自答：如何檢查 Read／Write 的長度與範圍？','Self-study: validate Read/Write length and range')),
               (f,bi('圖表情境：正常原子性與斷電原子性有什麼不同？','Figure scenario: normal versus power-fail atomicity'))]
    out.append('<nav class="st-route" aria-label="'+bi('相關教材','Related lessons')+'"><h3>'+bi('接著用情境練習','Continue with worked scenarios')+'</h3>')
    for url,label in links:
        out.append('<p><a href="'+e(url,quote=True)+'">'+e(label)+'</a></p>')
    out.append('</nav>')
    out.append(r.source([r.by_id[k] for k in claims]))
    out.append('</section>')
    return '\n'.join(out)
