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
        title=bi('命令在記憶體，Doorbell通告佇列位置','Commands reside in memory; doorbells announce queue positions')
        out.append(diagram(title,bi('作者依Transport 1.4繪製。SQ是Submission Queue（提交佇列），CQ是Completion Queue（完成佇列）；BAR是Base Address Register（基底位址暫存器）。圖先區分記憶體資料與裝置Register，完整時序接正文。','Author diagram based on Transport 1.4. SQ means Submission Queue; CQ means Completion Queue; BAR means Base Address Register. This view separates memory data from device registers; the detailed sequence follows in the text.'),elements,height=370))
        out.append(r.paragraph(bi('重點是把三件事接起來：主機把命令寫入SQ（保存命令的提交佇列），再更新Doorbell通知位置；控制器取走命令並執行，最後把結果放進CQ（保存結果的完成佇列）。Doorbell不攜帶命令本體；中斷也不能取代完成項目的狀態。','The host writes a command to the SQ (Submission Queue), then updates a doorbell to announce its position. The controller fetches and executes the command, then places the result in the CQ (Completion Queue). The doorbell does not carry the command, and an interrupt does not replace completion status.')))
        out.append(r.paragraph(bi('前情只需記得：Base定義共同的命令與佇列模型，本篇補上PCIe的位址、存取及通知方式。Transport 1.4 §1.5（p.7）引用的PCIe Base為6.2；本站PCIe課程以6.0為準，查PCIe特定細節時須保留這個版本差異。','Prerequisite: Base defines the shared command/queue model; this report supplies PCIe addresses, accesses, and notifications. Transport 1.4 §1.5 (p.7) references PCIe Base 6.2, while this site’s PCIe course uses 6.0. Retain that distinction when checking PCIe-specific details.')))
        items=[('mmio-doorbell',bi('第一步：通知要寫到哪裡？','First: where does the notification go?'),bi('沿§3.1找到BAR0／BAR1與存取規則，再到§3.1.2讀DSTRD和queue identifier如何決定位移。','Follow §3.1 into BAR0/BAR1 and access rules, then §3.1.2 for DSTRD and queue-ID offsets.')),
               ('command',bi('第二步：命令與結果怎麼往返？','Next: how do command and result travel?'),bi('沿§3.4的交換時序，逐一看SQE、Doorbell、取命令、CQE與CQ head更新。SQE與CQE分別是佇列中的命令和完成項目。','Follow §3.4 through SQE, doorbell, fetch, CQE, and CQ-head update. SQE/CQE are submission/completion entries.')),
               ('interrupts',bi('第三步：收到通知後要讀什麼？','Then: what follows an interrupt?'),bi('接中斷模式與完成佇列處理，再把PCIe錯誤和NVMe命令狀態分開。接收端眼圖量測是另一個診斷入口。','Continue into interrupt mode and completion processing, keeping PCIe errors separate from NVMe command status. Receiver eye measurements are a separate diagnostic path.'))]
        claims=['PCIE14-SCOPE','PCIE14-MMIO','PCIE14-DOORBELL','PCIE14-COMMAND']
    else:
        elements=[box(20,25,330,80,[bi('已選格式：資料／metadata','Selected format: data / metadata')]),box(410,25,330,80,[bi('Read／Write：範圍與指標','Read / Write: range and pointers')]),
                  box(410,270,330,80,[bi('完成狀態與資料保證','Completion and data guarantees')]),box(20,270,330,80,[bi('能力、條件與適用範圍','Capabilities and conditions')]),
                  arrow(350,65,410,65),arrow(575,105,575,270),arrow(410,310,350,310)]
        title=bi('先讀既有格式，再理解命令及完成結果','Read the selected format before the command and result')
        out.append(diagram(title,bi('作者繪製的閱讀關係圖。LBA是Logical Block Address（邏輯區塊位址），metadata是隨區塊保存的附加資料；圖不要求每次I/O之前重新Format。','Author reading map. LBA means Logical Block Address; metadata is additional block-associated information. The map does not require reformatting before each I/O.'),elements,height=375))
        out.append(r.paragraph(bi('同一個Read或Write，先要知道namespace（邏輯儲存空間）採用什麼格式。接著用LBA（指定區塊位置的位址）、區塊數和資料指標描述範圍，再核對完成狀態及所需的持久性、原子性與保護條件。','For a Read or Write, first establish the namespace (logical storage space) format. Then interpret the LBA (Logical Block Address), block count, and data pointers, followed by completion status and the required persistence, atomicity, and protection conditions.')))
        out.append(r.paragraph(bi('前情只回顧：Base 2.4定義共同提交與完成機制，NVM Command Set 1.3補上區塊命令的語意。以下先沿一筆資料走，再分組閱讀管理與進階功能，不把所有功能串成每筆I/O的必要步驟。','Base 2.4 supplies the common submission/completion mechanism; NVM Command Set 1.3 adds block-command semantics. Follow one data operation first, then the management and advanced topics; they are not mandatory stages of every I/O.')))
        items=[('nvmcs-identify',bi('第一步：同一個namespace，該讀哪份Identify？','First: which Identify data describes this namespace?'),bi('先連起共通namespace資訊、NVM特定資訊與格式清單，確認本次要用的資料大小和metadata配置。','Connect common namespace data, NVM-specific data, and format lists to establish data size and metadata arrangement.')),
               ('nvmcs-read-write',bi('第二步：從範圍走到傳輸量','Next: connect the range to transfer size'),bi('沿SLBA、以0為基底的NLB與資料指標解讀Read／Write，再依所選格式追資料與metadata。','Read SLBA, zero-based NLB, and data pointers, then trace data and metadata under the selected format.')),
               ('nvmcs-atomic',bi('第三步：完成後具備哪些保證？','Then: which guarantees apply?'),bi('把正常原子性、斷電原子性、順序與資料保護分別接到條件，Copy與資源管理再沿各自主題閱讀。','Apply normal/power-fail atomicity, ordering, and protection under their conditions; follow Copy and resource management in their own sections.'))]
        claims=['NVMCS13-FOUNDATION','NVMCS13-IDENTIFY','NVMCS13-METADATA','NVMCS13-READ-WRITE']
    out.append('<div class="st-route"><h3>'+bi('沿這條路線讀下去','Continue along this reading route')+'</h3>')
    for target,title,explanation in items:
        out.append('<h4>'+link(target,title)+'</h4>'+r.paragraph(explanation))
    out.append('</div>')
    out.append(r.source([r.by_id[k] for k in claims]))
    out.append('</section>')
    return '\n'.join(out)
