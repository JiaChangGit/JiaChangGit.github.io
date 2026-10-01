from scripts.nvme_qa_model import add

add(10,'Admin Submission Queue 與 Admin Completion Queue 如何透過 AQA、ASQ 及 ACQ 建立？ || How are the Admin Submission and Completion Queues established through AQA, ASQ and ACQ?','register',['adminreg','init','reset'],'''
Create I/O Queue 本身也是 Admin 命令，所以必須先有可用的 Admin Queue，才能建立 I/O Queue。這也是 Admin Queue 需要透過 Register 配置，而不能依賴尚未建立的命令通道來建立自己的原因。 || Establish the management channel before using Create I/O Queue. An absent Admin queue cannot create itself through a command.
每個 controller 有 QID=0 的 Admin SQ／CQ；這不是一般 I/O QID。 || Each controller has an Admin SQ/CQ with QID=0, separate from I/O queue identifiers.
AQA 指定 Admin SQ 與 CQ 各自的長度，ASQ 與 ACQ 則提供各自的實體起始位址。這兩條 queue 必須使用實體連續的記憶體，不能套用 Create I/O Queue 中 PC=0 的 PRP list 建立方式。 || AQA gives both lengths; ASQ/ACQ give their physical bases. Admin queues require physical contiguity and are not created with a PC=0 Create Queue PRP list.
ASQS、ACQS 均為 zero-based；64 entries 寫 63。Admin SQE 64 bytes、CQE 16 bytes；兩條 queue 可以有不同長度。 || ASQS/ACQS are zero-based: 64 entries encode as 63. Admin SQEs are 64 bytes and CQEs 16 bytes; the two queues need not have equal lengths.
Host 先配置並初始化記憶體，再於 EN=0 時寫入 AQA、ASQ、ACQ，並把 Admin CQ 的 Phase 初始化為 0。完成 CC 設定後啟用 controller，等到 RDY=1，才提交第一筆 Admin 命令。 || Allocate and initialize memory, write the three registers with EN=0 and clear Admin CQ phases. Configure CC, enable, wait for RDY=1, then submit the first Admin command.
Host 應能透過 Admin SQ 提交 Identify，並在 Admin CQ 收到 CID 相符的完成結果。ACQ 與 interrupt vector 0 關聯，但 Host 也可以輪詢 Phase 來辨認完成，不一定要等待中斷通知。 || Identify can be submitted and matched by CID in Admin CQ. ACQ is associated with interrupt vector 0, while the host can also poll phase tags.
size=0 編碼的是一個位置，不是停用 queue 的合法方式；以這種配置啟用 controller，結果屬於 undefined behavior。此外，Delete I/O Queue 只用來刪除 I/O Queue，不能用來刪除 Admin Queue。 || Size=0 encodes one slot and is not a legal way to disable an Admin queue; enabling in that configuration is undefined. Delete I/O Queue cannot delete Admin queues.
應同時核對 AQA 的長度、實際配置的記憶體與第一筆 CQE。即使 Register 回讀值正確，也還不能證明 controller 真的能存取 Host 提供的記憶體。 || Compare AQA, allocated memory and the first CQE. Correct register readback does not establish device access to the supplied memory.
先看 ASQ／ACQ 的位址與 CC.MPS 對齊，再看是否清除舊 Phase。 || First check queue addresses and CC.MPS alignment, then initialization of stale phase tags.
''')

add(11,'Admin Queue 與 I/O Queue 的 Size、Base Address 及 Memory Page 對齊有哪些要求？ || What are the size, base-address and page-alignment requirements for Admin and I/O queues?','queue',['adminreg','cap','qattr','create'],'''
配置 queue 時，必須分清 entry 數量、每筆 entry 的 bytes 數，以及需要幾個記憶體頁面。這些數量的單位不同；混用時，queue 就可能超出實際配置的記憶體範圍。 || Keep entry counts, byte sizes and memory pages distinct, and prevent a queue from exceeding allocated memory.
對齊與大小規則會因 queue 類型及記憶體位置而異。Admin Queue、一般 I/O Queue，以及能力允許時放在 CMB 的 queue，必須分別確認，不能把其中一種配置的規則直接套到其他配置。 || Distinguish Admin/I/O and host-memory/CMB configurations. A rule for one is not automatically universal.
Admin Queue 的長度限制來自 AQA；I/O Queue 則要核對 CAP.MQES、CQR 與 CC.IOSQES／IOCQES。如果使用 CMB，還須確認 CMBSZ 的 queue 支援能力，以及 CMBLOC.CQDA／CQPDS 定義的例外。 || Check AQA for Admin, and CAP.MQES/CQR and CC.IOSQES/IOCQES for I/O. CMB exceptions depend on CMBLOC.CQDA/CQPDS and CMBSZ queue support.
Queue 長度欄位編碼的是 entry 數量減 1。在一般配置中，queue 的基底位址，以及非連續 queue 的各個 PRP 頁面，都要依 CC.MPS 對齊，PRP1 的 offset 則為 0。 || Length fields encode entries−1. Ordinary bases and each PRP page of a discontiguous queue align to CC.MPS; PRP1 has offset zero.
先決定 queue 有幾個位置、每筆 entry 有多大，再算出所需 bytes 數並配置頁面。如果支援非連續配置，接著建立 PRP list，最後提交 Create 命令。Queue 仍有效時，Host 不得任意修改這份 PRP list。 || Choose slots and entry size, calculate bytes, allocate pages and a PRP list if supported, then Create. Do not alter a queue's live PRP list.
每條 queue 至少需要 2 個位置。Admin Queue 最多有 4096 個位置，I/O Queue 則最多有 min(65536, MQES+1) 個。為了分辨 Full 與 Empty，環狀 queue 還必須保留一個位置不使用。 || Minimum size is two slots; Admin maximum is 4096 and I/O maximum min(65536, MQES+1). One slot remains unavailable to distinguish full from empty.
I/O queue 大小非法時，回報 Invalid Queue Size（1/02h）；PRP offset 非零時，應回報 PRP Offset Invalid（0/13h）。若 PC 設定違反 CQR 要求，則要分別確認 Create SQ 與 Create CQ 使用的是建議還是強制回覆，不能把兩者的要求強度視為相同。 || Invalid I/O sizes map to Invalid Queue Size (1/02h); nonzero PRP offsets should return PRP Offset Invalid (0/13h). Apply the specific SQ/CQ requirement for PC violating CQR.
例如，同樣有 128 個位置，NVM SQ 需要 8192 bytes，而 CQ 只需要 2048 bytes。兩者的 QSIZE 雖然都是 127，每筆 entry 的大小卻不同，因此不能只憑 QSIZE 相同，就把所需的記憶體容量算成同一個數值。 || A 128-slot NVM SQ needs 8192 bytes, its CQ 2048 bytes. Equal QSIZE=127 does not imply equal byte allocations.
先檢查 QSIZE 是否重複加 1、entry size 是否誤用，以及對齊採用的是 CC.MPS 而非任意 OS page size。 || First check double application of +1, wrong entry size and alignment against CC.MPS rather than an assumed OS page size.
''')

add(12,'Host 如何建立 I/O Completion Queue 與 I/O Submission Queue？兩者必須遵守什麼建立順序？ || How are I/O CQs and SQs created, and why must the CQ be created first?','queue',['create','queue','number'],'''
SQ 中的命令需要一個有效的 CQ 來回報完成，所以 Host 必須先建立 CQ，才能建立指向它的 SQ。這是物件之間的依賴要求，不只是效能上的建議。 || Every I/O needs a valid completion destination. Create the CQ before its SQ: this is an ordering requirement, not merely a performance recommendation.
一個 SQ 在建立時指定其 CQ；多個 SQ 可以指向同一個已存在的 CQ。 || An SQ selects its CQ at creation; several SQs may use one existing CQ.
建立 queue 前，先取得 Number of Queues 配額，再確認 CAP.MQES／CQR、entry 大小與可用的 interrupt vector 範圍。後續 Create 命令的參數必須符合這些限制。 || Allocate Number of Queues first, then check MQES/CQR, entry sizes and interrupt-vector limits.
Create CQ 用 PRP1、QID、QSIZE、PC、IEN、IV；Create SQ 加上 CQID、QPRIO、NVMSETID。NVMSETID=0 表示沒有指定 Set 關聯。 || Create CQ uses PRP1, QID, QSIZE, PC, IEN and IV. Create SQ additionally uses CQID, QPRIO and NVMSETID; zero NVMSETID means no specific set association.
Host 先準備 CQ 記憶體並初始化 Phase，送出 Create CQ，等待成功完成。接著送出 Create SQ，以 CQID 指向剛建立的 CQ，並再次等待成功。兩個步驟都完成後，才開始填寫 I/O SQE 並更新 Tail。 || Initialize CQ memory/phases, Create CQ and await success, Create SQ referring to its CQID and await success, then populate SQEs and update Tail.
兩筆 Create 命令都會在 Admin CQ 回報成功（0/00h）。新建立的 I/O CQ 是供後續 I/O 命令回報結果使用，因此 Host 不應到新 CQ 等待建立它的那筆 Create 命令完成。 || Both Create commands complete successfully (0/00h) on Admin CQ. Later I/O completions go to the new I/O CQ; its own Create completion does not.
CQID 在支援範圍內但未建立，回 Completion Queue Invalid（1/00h）；CQID=0 或超界回 Invalid Queue Identifier（1/01h）。 || An in-range CQID that has not been created returns Completion Queue Invalid (1/00h); CQID=0 or out of range returns Invalid Queue Identifier (1/01h).
應確認 Create SQ 的 CQID 與 Host 保存的 SQ→CQ 對照一致。Create CQ 成功只代表該 CQ 已存在，並不會自動把所有 SQ 都連到它。 || Match CQID against the host's SQ-to-CQ map. Creating a CQ does not automatically associate every SQ with it.
先檢查 CQ Create 是否已成功完成，而非只是已提交。 || First check that CQ creation completed successfully, not merely that its command was submitted.
''')

add(13,'多個 SQ 共用一個 CQ 與每個 SQ 使用獨立 CQ 有什麼差異？ || How does sharing a CQ differ from giving every SQ its own CQ?','queue',['queue','create','cqe'],'''
共用 CQ 可以減少 CQ 資源用量，但也會把多條 SQ 的完成流量集中到同一處。因此，選擇共用或獨立 CQ 時，要考慮資源用量與完成處理能否互相隔離。 || Trade resource usage against completion-path isolation. Shared CQs reduce CQ resources but concentrate completion traffic.
多條 SQ 共用的是 CQ 的完成位置及相關通知資源。各條 SQ 仍各自管理 CID，所以不會因此變成共用同一個命令識別空間。 || Completion slots and CQ notification are shared; the SQs do not become one CID namespace.
Number of Queues 分別回傳 SQ 與 CQ 的配額；Create SQ 的 CQID 指出它使用哪條 CQ；Create CQ 的 IEN 與 IV 則設定中斷通知。這三組欄位分別處理數量、關聯及通知。 || Number of Queues returns separate SQ/CQ allocations. Create SQ.CQID selects the mapping; CQ.IEN/IV configures notification.
Host 以 CQE 的 SQID 與 CID 找到原命令，再以 SQHD 更新該 SQ 已被 controller 消費到的位置。 || CQE.SQID+CID identifies the original command; SQHD updates consumption for that SQ.
先建立 CQ，再建立多條 SQ，並讓它們的 CQID 指向同一個 CQ。Host 讀取 CQE 時，先以 SQID 找出來源 SQ，再處理該命令的完成；處理完畢後，更新共用 CQ 的 Head。 || Create the CQ and multiple SQs referencing it. Dispatch each CQE by SQID, then advance the shared CQ head.
例如，SQ1/CID7 與 SQ2/CID7 可以同時存在，Host 必須把回覆各自對回正確的 SQ。這不代表同一條 SQ 也可以在命令尚未完成時，重複使用同一個 CID。 || SQ1/CID7 and SQ2/CID7 may coexist and must be matched separately, unlike reusing an outstanding CID within one SQ.
合法地共用 CQ 不會造成錯誤。若 Create SQ 指定不存在的 CQID，則使用該命令定義的錯誤 Status。至於共用 CQ 已滿，應按空間不足的處理規則判斷，不能把它當成每條 SQ 都要回報 Invalid Queue Size。 || Valid sharing is not an error. Missing CQIDs follow Create SQ status rules; a full shared CQ does not automatically produce Invalid Queue Size for each SQ.
應一起觀察 CQ 可用的位置數、各 SQ 的完成流量，以及 Host 處理完成的速度。只知道建立了多少條 SQ，還不足以判斷共用 CQ 是否成為瓶頸。 || Compare completion capacity, submission traffic and host consumption rate; SQ count alone does not establish freedom from bottlenecks.
先看 completion 對應是不是只用 CID，漏了 SQID。 || First check whether completion matching incorrectly uses CID without SQID.
''')

add(14,'Host 如何確認 Controller 支援 Physically Contiguous 或其他 Queue 形式？ || How does the host determine supported queue memory layouts?','queue',['cap','adminreg','create'],'''
Host 必須用 controller 支援的方式描述 queue 記憶體。尤其要注意，程式看到的虛擬位址即使連續，底層實體記憶體也不一定連續。 || Describe queue memory in a layout the controller supports. Virtual contiguity does not establish physical contiguity.
Admin Queue 一律要求實體記憶體連續。I/O Queue 能否使用實體不連續的頁面，則取決於 CAP.CQR，以及 queue 配置在哪一種記憶體中。 || Admin queues require physical contiguity. Discontiguous I/O queues depend on CAP.CQR and memory location.
CQR=1 要求實體連續；CQR=0 允許 I/O 使用非連續頁面。放在 CMB 時還要查 CMBSZ.SQS／CQS、CMBLOC.CQPDS／CQDA。 || CQR=1 requires physical contiguity; CQR=0 allows discontiguous I/O queues. CMB placement additionally requires CMBSZ.SQS/CQS and CMBLOC.CQPDS/CQDA checks.
PC 決定 PRP1 的解讀方式：PC=1 時，PRP1 直接指向 queue 的基底位址；PC=0 時，PRP1 指向描述各個 queue 頁面的 PRP list。這裡不能套用一般資料傳輸中 PRP2 的判斷方式。 || With Create I/O Queue.PC=1, PRP1 is the queue base; with PC=0 it points to a queue-page PRP list, distinct from ordinary data-transfer PRP2 rules.
Host 先確認記憶體位置與支援能力，再建立完整且符合對齊要求的頁面清單，最後提交 Create。Queue 仍在使用期間，清單的位置與內容都必須保留，直到 Delete 成功或重設終止該 queue 為止。 || Confirm placement/support, build a complete aligned page list and Create. Retain the list's address and contents until successful deletion or reset.
建立成功後，controller 應能按照所選的記憶體形式讀取 SQE 或寫入 CQE。不過，Create 成功並不表示 Host 可以在 queue 使用中重新排列頁面。 || The controller fetches SQEs/writes CQEs through the chosen layout. Successful Create does not authorize rearranging its pages while live.
CQR=1 且 PC=0：Create CQ 必須（shall）回 Invalid Field（0/02h），Create SQ 的對應要求為建議（should）回覆；不支援的 CMB 用法可能為 Invalid Use of Controller Memory Buffer（0/12h）。 || For CQR=1 and PC=0, Create CQ shall return Invalid Field (0/02h), while Create SQ says should. Unsupported CMB usage may return Invalid Use of Controller Memory Buffer (0/12h).
驗證時，要把 CAP.CQR、Create 命令的 PC、PRP1 指向的內容，以及實際頁面配置一起核對。只確認 Create 回報成功，還不足以證明 Host 對這些欄位的解讀正確。 || Cross-check CQR, PC, PRP1 interpretation and actual page layout, rather than validating only the completion.
先確認 PRP1 應該指向 queue 本體，還是 PRP list。如果把兩者弄反，即使位址可存取，controller 讀到的內容仍不是它預期的資料結構。 || First ask whether PRP1 addresses queue storage or its page list. Confusing them breaks the layout even with valid addresses.
''')

add(15,'QID 重複、QID 為 0、CQID 不存在、Queue Size 超過 CAP.MQES 或 Interrupt Vector 非法時，Controller 應如何回應？ || Which statuses apply to duplicate/zero QIDs, missing CQIDs, oversized queues and invalid vectors?','queue',['create','status','irq'],'''
不同的參數錯誤有各自適用的 Status。這題要練習根據錯誤欄位與狀態選擇正確結果，避免把所有情況都歸成 Invalid Field。 || Match distinct parameter errors to their defined statuses instead of flattening them into Invalid Field.
這裡檢查的是透過 Admin Queue 提交的 Create I/O Queue 命令。判斷 QID 是否重複時，SQ 與 CQ 各有自己的識別空間，必須在相同類型內比較。 || This concerns Create I/O Queue Admin commands. Duplicate QIDs are checked within the SQ or CQ identifier space respectively.
CAP.MQES、Number of Queues 回覆和 PCIe interrupt 配置是合法範圍的依據。 || CAP.MQES, Number of Queues allocations and PCIe interrupt configuration establish legal ranges.
重點檢查 QID、CQID、QSIZE 與 IV，這些參數位於 CDW10／11。同時確認 IOSQES 與 IOCQES 已正確初始化，避免將 entry 大小設定錯誤誤認為個別 queue 參數的問題。 || Inspect QID, CQID, QSIZE and IV, and initialization of IOSQES/IOCQES. The relevant parameters are in CDW10/11.
先建立一組合法的參數作為比較基準，再一次只改一個條件，例如重複的 QID 或未建立的 CQID。若一筆命令同時有多個錯誤，controller 可能先回報其中另一個錯誤，讓測試結果難以判讀。 || For a learning test, change one condition at a time from a valid baseline; multiple errors can obscure the expected result.
合法參數回成功並建立指定 queue；失敗後不能把該 QID 當成已建立。 || Valid parameters successfully create the queue; after failure, do not treat the requested QID as created.
同類 QID 重複／0／超範圍：1/01h；QSIZE=0 或超支援：1/02h；合法範圍內 CQID 未建立：1/00h；CQID=0／超界：1/01h；非法 IV：1/08h。多個錯誤同時成立時，除特別規定外由實作選擇回哪個。 || Duplicate/zero/out-of-range QID: 1/01h. Zero/unsupported QSIZE: 1/02h. In-range uncreated CQID: 1/00h. Zero/out-of-range CQID: 1/01h. Invalid IV: 1/08h. Unless specified otherwise, implementations choose among simultaneously applicable errors.
若 Error Information Log 有對應紀錄，可用 Parameter Error Location 找出錯誤欄位。但在沒有 More=1 的保證時，不能只因命令失敗，就要求一定新增一筆 Error Information entry。 || When available, Error Information Parameter Error Location can identify the field. Without More=1, do not assume every such error must have an entry.
先確認測例確實只有一個非法條件，再核對預期的 SCT。這類命令專用錯誤通常要以 SCT=1 搭配 SC 判讀，不能只比較 SC 數字。 || First check that only one field is invalid and the expected SCT is 1, rather than comparing SC alone.
''')

add(16,'Number of Queues Feature 回傳的數值與實際可建立的 Queue 數量有什麼關係？ || How do Number of Queues results relate to queues that can actually be created?','feature',['number','create'],'''
Host 先向 controller 取得 I/O SQ 與 CQ 的數量配額，再依配額建立 queue。配額只說明可建立的數量，既不代表 queue 已建立，也不代表每條 queue 的深度。 || Obtain SQ/CQ allocations before creating queues. Allocation is neither an instantiated queue nor queue depth.
FID 07h 作用於 controller，不包含 Admin SQ／CQ。 || FID 07h has controller scope and excludes Admin SQ/CQ.
實際分配數量應以 Set Features FID 07h 成功回覆的 CQE DW0 為準，之後也可用 Get Features 讀回。CAP.MQES 則回答另一個問題：每條 I/O Queue 最多可以有幾個 entry。 || Use Set Features FID 07h CQE DW0 for actual allocations, with Get Features readback. CAP.MQES separately limits per-queue depth.
CDW11 的 NSQR／NCQR 與 DW0 的 NSQA／NCQA 都是 zero-based；回覆可能比要求少，也可能因配置單位而較多。 || Requested NSQR/NCQR and returned NSQA/NCQA are zero-based. Allocations may be smaller or larger than requested because of allocation units.
Host 必須在 CLR 之後、任何 I/O Queue 建立之前設定 Number of Queues。第一筆成功的 Set 決定這一輪的配額；直到下一次 CLR 發生前，分配數量都不再改變。 || Set it after CLR and before creating any I/O queue. The first successful setting fixes allocation until the next CLR.
例如，DW0=00030007h 表示分配了 4 個 CQ 與 8 個 SQ 的配額。Host 仍須逐一送出 Create 才能建立它們，而 CQ、SQ 的合法 QID 範圍分別依各自配額判斷。 || DW0=00030007h allocates four CQs and eight SQs. Each still requires Create, with the respective QID ranges.
若已建立 I/O Queue 才送出 Set，controller 必須回傳 Command Sequence Error（0/0Ch）。若要求值為 FFFFh，則建議回傳 Invalid Field（0/02h）。在尚未建立 queue 的情況下，再次送出 Set 應可成功，但不改變第一筆成功 Set 所決定的配額。 || Setting after an I/O queue exists shall return Command Sequence Error (0/0Ch). Requested=FFFFh should return Invalid Field (0/02h). Subsequent Set before queue creation should succeed without changing allocation.
應分別保存回覆的配額、目前已建立的 queue 清單，以及 MQES 限制。Get Features 回報的是配額，不能將它解讀成目前實際存在的 queue 數量。 || Compare allocations, the actual created-queue list and MQES. Allocated counts are not current existence counts.
先確認 Host 使用的是 controller 實際回傳的配額，而不是自己原先要求的數量，再檢查是否已對 NSQA 與 NCQA 的編碼值加 1。 || First check whether requested values were used instead of returned allocations or whether +1 was omitted.
''',{12:'Controller Level Reset 後，第一筆成功的 Set FID07h 會重新配置 queue 數量。Host 應使用這次的回覆重建 I/O queue，不能直接沿用前一次的配額。 || The first successful Set FID 07h after CLR allocates anew. Read the result and recreate queues rather than assuming the previous allocation.',13:'受影響的 controller 經過 Controller Level Reset 後，必須重新協商 Number of Queues。NVM Subsystem Reset 不會保留原 I/O queue，讓 Host 在恢復後直接沿用它們提交 I/O。 || Renegotiate Number of Queues after the affected controller’s CLR. NVM Subsystem Reset does not preserve old I/O queues for immediate reuse.',14:'Power Cycle 後，先重新初始化，再設定 FID07h，最後建立 queue。不能只套用 Saved 或 Default 的一般概念，就省略這些初始化步驟。 || Reinitialize, set FID 07h and create queues; generic Saved/Default concepts do not replace this initialization sequence.'})

add(17,'Host 刪除 I/O Queue 時，SQ 與 CQ 的相依關係如何限制刪除順序？ || Why must associated SQs be deleted before their CQ?','queue',['queue','delete'],'''
Host 必須先刪除依賴 CQ 的 SQ，才能刪除該 CQ。這個順序可避免 SQ 還有命令需要回報時，完成結果的目的地卻已不存在。 || Prevent active SQs from losing their completion destination. For associated queues this is a required host deletion order.
一個 CQ 可能同時被多條 SQ 使用，因此要先刪除所有指向它的 SQ。只刪除與 CQ 具有相同 QID 的 SQ，並不足以滿足這個條件。 || A CQ may serve multiple SQs. Delete every associated SQ, not only an SQ with the same numeric QID.
使用 Host 在 Create SQ 時保存的 SQ→CQID 對照；Number of Queues 不提供這張連線清單。 || Use the host's SQ-to-CQID map from creation. Number of Queues does not provide this association list.
Delete I/O SQ／CQ 的 CDW10.QID 指定對象；它們都透過 Admin SQ 提交。 || Delete I/O SQ/CQ selects the target with CDW10.QID; both travel through Admin SQ.
Host 先停止向目標 SQ 提交新命令，並適當等待既有命令處理完畢。接著逐一送出 Delete SQ 並等待成功，處理仍需讀取的舊完成結果，最後才送出 Delete CQ。 || Stop submissions, appropriately drain work, delete each associated SQ and await success, process needed old completions, then delete the CQ.
Delete SQ 成功，表示該 SQ 的命令處理已到達規範定義的終止點。Delete CQ 成功後，Host 才能收回該 CQ 的 PRP list 與 queue 資源；兩個完成點不能互相代替。 || Successful Delete CQ allows reclamation of its PRP list and queue resources. Successful Delete SQ separately establishes termination of processing for that SQ's commands.
尚有相關 SQ 時 Delete CQ 必須回 Invalid Queue Deletion（1/0Ch）；QID=0 或非法對象回 Invalid Queue Identifier（1/01h）。 || Delete CQ with associated SQs shall return Invalid Queue Deletion (1/0Ch); zero or invalid QID returns Invalid Queue Identifier (1/01h).
應比較 Delete 成功回覆與記憶體釋放的先後時間。只要刪除命令尚未成功，Host 就不能僅憑「已送出 Delete」而提前回收裝置可能仍會存取的記憶體。 || Correlate successful deletion with memory reclamation. Merely submitting Delete does not authorize early reclamation of DMA memory.
先檢查 CQ 是否還被另一條 SQ 指向，而非只檢查 CQ 自己是否已空。 || First check whether another SQ still references the CQ, not only whether the CQ appears empty.
''')

add(18,'刪除不存在的 Queue、仍被 SQ 使用的 CQ 或仍有 Outstanding Command 的 SQ 時，應如何處理？ || What happens when deleting a missing queue, a referenced CQ or an SQ with outstanding commands?','queue',['delete','reset'],'''
仍有未完成命令，不會直接讓 Delete SQ 變成非法操作。判斷時應分清楚：刪除要求本身不合法，與合法刪除導致原命令終止，是兩種不同情況。 || Distinguish an invalid deletion request from valid deletion terminating commands. Outstanding work does not itself make Delete SQ illegal.
刪除 SQ 會影響該 SQ 中尚未完成的 I/O。刪除 CQ 則另有前提：所有依賴它的 SQ 都必須已被刪除，才能繼續進行。 || SQ deletion affects its outstanding I/O; CQ deletion depends on the existence of every associated SQ.
先檢查 Host 記錄的 queue 建立與刪除結果，以及尚未完成的命令。這些是目前的執行狀態，不能只靠 Identify 的選配能力位得知。 || Consult host creation/deletion and outstanding-command records. These are runtime state, not Identify optional capabilities.
Delete 的 QID 必須有效且不為 0；目標 I/O 命令仍以各自 SQID／CID 辨識。 || Delete requires a valid nonzero QID; affected I/O commands retain their own SQID/CID identities.
正常拆除時，Host 先等待既有工作完成，再刪除 queue。如果目的是中止工作而直接刪除 SQ，則在 Delete 成功後，將仍未收到 CQE 的原命令視為已隱含中止。 || Drain before normal teardown. If deleting an SQ to stop work, treat remaining commands without CQEs as implicitly aborted after successful Delete.
在 Delete SQ 成功之前，原命令可能正常完成，也可能收到表示中止的 CQE。但是 Delete SQ 一旦成功，controller 就不得再為那些原 SQ 命令寫入新的 completion。 || Before successful Delete SQ, original commands may complete normally or with abort status. After success, no further completions may be posted for those commands.
QID 非法時回報 1/01h；CQ 仍被 SQ 使用時回報 1/0Ch。原 I/O 命令若因刪除 SQ 而中止，可以透過 CQE 回報 Command Aborted due to SQ Deletion（0/08h），也可能在 Delete 成功時依規則形成隱含完成，沒有各自的 CQE。 || Invalid QID: 1/01h. CQ still referenced: 1/0Ch. I/O aborted by SQ deletion uses 0/08h, including implicit completion established by successful Delete.
驗證時，應把已收到 CQE 的命令，以及 Delete 成功後被視為隱含中止的命令，一起納入統計。不能只計算實際 CQE，並要求每筆原命令都一定有獨立回覆。 || Account for both received CQEs and implicit aborts after successful Delete; do not require a physical CQE for every original command.
先檢查 Delete SQ 是否已成功完成；在它還 outstanding 時，不能宣布所有原命令已停止。 || First check whether Delete SQ itself completed successfully. Its outstanding state does not establish that all original work stopped.
''')

add(19,'Queue 刪除後，Controller 是否還能存取原 Queue Memory 或回報原 Queue 的 Completion？ || May the controller access deleted queue memory or post completions for its old commands?','queue',['delete','create','queue'],'''
刪除 queue 後能否回收記憶體，取決於刪除是否已成功完成。判斷違規存取時，也必須區分：CQE 是先前已寫入、只是 Host 較晚讀到，還是真的在刪除成功後才寫入。 || Establish the memory-reclamation boundary and distinguish an earlier write observed late from a new write after successful deletion.
刪除 SQ 不會一併刪除它使用的 CQ。如果 CQ 仍存在，其中先前已寫入的完成結果，仍可能等待 Host 處理。 || Deleting an SQ does not delete its shared CQ; already posted completions may remain for host consumption.
以 Admin CQ 回報 Delete 成功的時點，判斷 queue 的刪除是否完成。Host 送出 Delete 的時間，或自行設定的 timeout 到期，都不能代替這個完成結果。 || Use successful Delete completion on Admin CQ as the boundary, not submission time or a host timeout.
Host 需要追蹤被刪除的 QID、關聯 CQID、PRP list 位址，以及記憶體何時可回收。即使同一位址稍後用來建立新 queue，也必須能分辨它屬於哪一輪配置。 || Track deleted QID, associated CQID, PRP-list address and memory lifetime. Reused addresses require distinguishing queue lifetimes.
先停止提交新命令，再送出 Delete 並等待成功，之後才回收對應的 queue 記憶體與 PRP list。若只刪除 SQ，而 CQ 仍存在，Host 還須處理其中先前已寫入的完成結果。 || Stop submissions, successfully delete, then reclaim the corresponding queue/list memory. With SQ-only deletion, handle existing posted entries in the surviving CQ.
Delete SQ 成功後，controller 不得再為原 SQ 的命令新增 completion。Delete CQ 成功後，Host 可釋放其 PRP list 與記憶體，controller 也不能再把已刪除的 queue 當作可存取的 DMA 目標。 || After successful Delete SQ, no new completions for its old commands may be posted. Successful Delete CQ permits releasing its list; a deleted queue is no longer a valid DMA target.
若 Delete 本身失敗或沒有完成，不能推論記憶體已可收回。逾時不是另一種 Successful Completion。 || Failure or absence of Delete completion does not authorize memory reclamation. Timeout is not a substitute for success.
應一併核對 CQE 的寫入時間、Phase、Delete 完成時間，以及 Host 實際讀取 CQE 的時間。Host 較晚處理到舊 CQE，並不等於 controller 在刪除成功後才違規寫入。 || Correlate write time, phase, Delete completion and host consumption. Late consumption of an old CQE is not necessarily a prohibited late write.
先確認所見 CQE 真正寫入於 Delete 成功之前還是之後。 || First establish whether the CQE was actually posted before or after successful Delete.
''')

add(20,'Queue Level Reset 的影響範圍是什麼？Outstanding Command 應如何處理？ || What is the scope of Queue Level Reset, and how is outstanding work handled?','queue',['reset','delete','create'],'''
Queue Level Reset 可在不重設整個 controller 的情況下，重新建立 I/O Queue。對 PCIe 而言，這個流程是刪除後再建立 queue，並沒有另一個專用的 Reset opcode。 || Rebuild I/O queues without resetting the whole controller. PCIe Queue Level Reset means deletion and recreation, not a separate reset opcode.
影響範圍包括目標 queue，以及重建時必須一併處理的相關 queue。例如，若要重建 CQ，就要先刪除所有使用它的 SQ；等 CQ 重建完成後，再重建這些 SQ。 || Reset the target and its necessary dependencies. Rebuilding a CQ requires deleting its SQs first and recreating them afterward.
依既有 SQ 與 CQ 的關聯，以及 Create／Delete 的順序規則執行。這個流程不依靠另一個獨立的 Queue Reset Feature。 || Use existing queue associations and Create/Delete rules, not a separate Queue Reset feature.
流程會使用 Delete SQ／CQ 與 Create CQ／SQ。雖然 QID 可以重用，但新 queue 的記憶體與指標都屬於新一輪配置，不能接續上一輪的命令狀態。 || Use Delete SQ/CQ and Create CQ/SQ. QIDs may be reused, but memory and pointers begin a new lifetime.
正常情況下，Host 先讓既有工作完成，再刪除 queue。若必須中止工作，則依 Delete SQ 的明確或隱含完成規則處理。重建時先初始化新 CQ 的 Phase，建立 CQ，最後才建立依賴它的 SQ。 || Normally let work finish before deletion. For cancellation, apply explicit/implicit Delete SQ completion rules. Initialize new CQ phases and create CQ before SQ.
重建成功後新命令可執行，原 outstanding 命令不會自動搬入新 SQ。 || New commands execute after reconstruction; old outstanding commands are not automatically migrated into the new SQ.
若 CQ 仍被 SQ 使用就嘗試刪除，會遇到 1/0Ch；若沒有有效 CQ 就建立 SQ，則依 CQID 的錯誤條件回覆。Queue Level Reset 是由這些命令組成的流程，本身沒有額外、統一的 Status。 || Deleting a referenced CQ returns 1/0Ch; premature SQ creation returns the applicable CQID error. Queue reset has no additional universal status.
核對刪除／建立順序與新舊 CID 對照，並檢查其他獨立 queue 是否保持正常。 || Check teardown/recreation ordering, command-lifetime tracking and continued operation of independent queues.
先列出目標 CQ 的所有使用者；漏一條共享 SQ 就可能使重設流程不合法。 || First enumerate every SQ using the target CQ; omitting one can invalidate the reset sequence.
''')

add(21,'Controller Reset 後，原有 I/O Queue 是否有效？Host 需要重新執行哪些操作？ || Are old I/O queues valid after Controller Reset, and what must the host do again?','queue',['reset','init','number','create'],'''
Host 必須把重設前的命令與恢復後的新命令分開追蹤，才能避免把記憶體中殘留的 completion 誤認成新命令的結果。 || Separate pre-failure commands from new work after recovery to avoid accepting stale completions.
Controller Level Reset 刪除該 controller 的全部 I/O SQ／CQ；不同於只刪除一條 SQ。 || Controller Level Reset deletes all I/O SQs/CQs of that controller, unlike deleting only one SQ.
恢復後應重新查詢必要的 Identify 資訊，並確認 Number of Queues 配額、entry 大小與中斷設定。不能未經確認，就假設上一輪設定仍可直接使用。 || Re-read necessary Identify data and verify queue allocations, entry sizes and interrupt settings rather than assuming previous values remain usable.
重建流程需要先設定 Admin Queue Register 與 CC，再視需要使用 Get／Set Features，最後以 Create CQ／SQ 建立 I/O 通道。這些步驟共同構成恢復流程，不能只做其中一部分。 || Admin registers, CC, Get/Set Features and Create CQ/SQ together establish the recovery path.
Host 先確認 RDY=0，初始化 Admin CQ 的 Phase 與 CC，再啟用 controller 並等待就緒。接著恢復必要的 Feature、設定 Number of Queues，依序建立 CQ、SQ。只有完成上述步驟後，才能允許新的 I/O 提交。 || Confirm RDY=0, initialize Admin CQ phases and CC, enable/wait ready, restore needed features, set Number of Queues, create CQ then SQ, and allow new I/O.
每筆 Create 都必須先在 Admin CQ 成功完成，對應的新 queue 才能使用。即使沿用相同 QID 或位址，也不能跳過這個完成確認。 || Each new queue becomes valid after its successful Create completion on Admin CQ, even when reusing an identifier or address.
直接更新舊 queue 的 Doorbell，不是合法的恢復流程，不能要求 controller 繼續處理該 queue。若是在重新建立 queue 時命令失敗，則依對應 Create 命令的 Status 處理。 || Updating old queue doorbells is not a valid recovery method. Failures of reconstruction commands follow their specific status rules.
Host 應保存重設前後的 queue 建立紀錄與命令對照，用來區分新舊配置。這是 Host 自行管理的追蹤資訊，不是要求在 NVMe 傳輸格式中新增欄位。 || Track queue lifetimes and command mappings across reset in host software; this is not a new NVMe wire field.
先看 Host 是否在新 Create 成功前就恢復 I/O。 || First check whether host I/O resumed before new Create commands succeeded.
''')
