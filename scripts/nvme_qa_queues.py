from scripts.nvme_qa_model import add

add(10,'Admin Submission Queue 與 Admin Completion Queue 如何透過 AQA、ASQ 及 ACQ 建立？ || How are the Admin Submission and Completion Queues established through AQA, ASQ and ACQ?','register',['adminreg','init','reset'],'''
先提供承載管理命令的通道，才有辦法使用 Create I/O Queue；Admin queue 不能用尚不存在的自己來建立自己。 || Establish the management channel before using Create I/O Queue. An absent Admin queue cannot create itself through a command.
每個 controller 有 QID=0 的 Admin SQ／CQ；這不是一般 I/O QID。 || Each controller has an Admin SQ/CQ with QID=0, separate from I/O queue identifiers.
AQA 決定各自長度；ASQ／ACQ 提供各自實體起點。Admin queue 必須實體連續，不能用 PC=0 的 Create Queue PRP list 方式建立。 || AQA gives both lengths; ASQ/ACQ give their physical bases. Admin queues require physical contiguity and are not created with a PC=0 Create Queue PRP list.
ASQS、ACQS 均為 zero-based；64 entries 寫 63。Admin SQE 64 bytes、CQE 16 bytes；兩條 queue 可以有不同長度。 || ASQS/ACQS are zero-based: 64 entries encode as 63. Admin SQEs are 64 bytes and CQEs 16 bytes; the two queues need not have equal lengths.
配置並清理記憶體，在 EN=0 時寫入三個 Register，清 Admin CQ Phase；完成 CC 設定後 Enable，等 RDY=1 再提交第一個 Admin command。 || Allocate and initialize memory, write the three registers with EN=0 and clear Admin CQ phases. Configure CC, enable, wait for RDY=1, then submit the first Admin command.
Admin SQ 可送 Identify，Admin CQ 可回對應 CID；ACQ 關聯 interrupt vector 0，但 Host 仍可透過 Phase 輪詢完成。 || Identify can be submitted and matched by CID in Admin CQ. ACQ is associated with interrupt vector 0, while the host can also poll phase tags.
size=0 對應一個 slot，不是停用 queue 的合法方法；以此 Enable 的結果 undefined。也不能用 Delete I/O Queue 刪 Admin queue。 || Size=0 encodes one slot and is not a legal way to disable an Admin queue; enabling in that configuration is undefined. Delete I/O Queue cannot delete Admin queues.
核對 AQA 長度、實際記憶體配置與第一筆 CQE。Register 可讀回正確不代表裝置能存取 Host 所給記憶體。 || Compare AQA, allocated memory and the first CQE. Correct register readback does not establish device access to the supplied memory.
先看 ASQ／ACQ 的位址與 CC.MPS 對齊，再看是否清除舊 Phase。 || First check queue addresses and CC.MPS alignment, then initialization of stale phase tags.
''')

add(11,'Admin Queue 與 I/O Queue 的 Size、Base Address 及 Memory Page 對齊有哪些要求？ || What are the size, base-address and page-alignment requirements for Admin and I/O queues?','queue',['adminreg','cap','qattr','create'],'''
避免把 entries、bytes、memory pages 當成同一個長度，也避免 queue 超出配置記憶體。 || Keep entry counts, byte sizes and memory pages distinct, and prevent a queue from exceeding allocated memory.
規則分 Admin 與 I/O，也分 Host memory 與能力允許的 CMB；不能從其中一種推論全部配置。 || Distinguish Admin/I/O and host-memory/CMB configurations. A rule for one is not automatically universal.
Admin 看 AQA；I/O 看 CAP.MQES、CQR 與 CC.IOSQES／IOCQES。CMB 例外另看 CMBLOC.CQDA／CQPDS 與 CMBSZ 的 queue 支援。 || Check AQA for Admin, and CAP.MQES/CQR and CC.IOSQES/IOCQES for I/O. CMB exceptions depend on CMBLOC.CQDA/CQPDS and CMBSZ queue support.
長度欄位是 entries−1。一般 queue base 與非連續 queue 的每個 PRP 頁依 CC.MPS 對齊；PRP1 的 offset 為 0。 || Length fields encode entries−1. Ordinary bases and each PRP page of a discontiguous queue align to CC.MPS; PRP1 has offset zero.
先決定 slots 和 entry size，再計算 bytes、配置頁面、建立 PRP list（若允許），最後提交 Create。PRP list 在 queue 有效期間不得任意改動。 || Choose slots and entry size, calculate bytes, allocate pages and a PRP list if supported, then Create. Do not alter a queue's live PRP list.
最少 2 slots；Admin 最多 4096，I/O 最多 min(65536, MQES+1)。為分辨滿與空，每條 queue 保留一個不能使用的 slot。 || Minimum size is two slots; Admin maximum is 4096 and I/O maximum min(65536, MQES+1). One slot remains unavailable to distinguish full from empty.
I/O 大小錯誤對應 Invalid Queue Size（1/02h）；非零 PRP offset 應回 PRP Offset Invalid（0/13h）；違反 CQR 的 PC 設定依 Create SQ／CQ 的規範強度判斷。 || Invalid I/O sizes map to Invalid Queue Size (1/02h); nonzero PRP offsets should return PRP Offset Invalid (0/13h). Apply the specific SQ/CQ requirement for PC violating CQR.
例：128-slot NVM SQ 需要 8192 bytes，CQ 需要 2048 bytes；不是因為 QSIZE 都是 127 就配置相同 bytes。 || A 128-slot NVM SQ needs 8192 bytes, its CQ 2048 bytes. Equal QSIZE=127 does not imply equal byte allocations.
先檢查 QSIZE 是否重複加 1、entry size 是否誤用，以及對齊採用的是 CC.MPS 而非任意 OS page size。 || First check double application of +1, wrong entry size and alignment against CC.MPS rather than an assumed OS page size.
''')

add(12,'Host 如何建立 I/O Completion Queue 與 I/O Submission Queue？兩者必須遵守什麼建立順序？ || How are I/O CQs and SQs created, and why must the CQ be created first?','queue',['create','queue','number'],'''
每筆 I/O 必須有合法的回覆目的地，所以先建立 CQ，再把 SQ 指向它；這是相依順序要求，不只是效能建議。 || Every I/O needs a valid completion destination. Create the CQ before its SQ: this is an ordering requirement, not merely a performance recommendation.
一個 SQ 在建立時指定其 CQ；多個 SQ 可以指向同一個已存在的 CQ。 || An SQ selects its CQ at creation; several SQs may use one existing CQ.
先配置 Number of Queues，再核對 CAP.MQES／CQR、entry sizes 與 interrupt vector 範圍。 || Allocate Number of Queues first, then check MQES/CQR, entry sizes and interrupt-vector limits.
Create CQ 用 PRP1、QID、QSIZE、PC、IEN、IV；Create SQ 加上 CQID、QPRIO、NVMSETID。NVMSETID=0 表示沒有指定 Set 關聯。 || Create CQ uses PRP1, QID, QSIZE, PC, IEN and IV. Create SQ additionally uses CQID, QPRIO and NVMSETID; zero NVMSETID means no specific set association.
準備 CQ 記憶體及初始 Phase→Create CQ 並等成功→Create SQ 指向 CQID 並等成功→填 SQE、更新 Tail。 || Initialize CQ memory/phases, Create CQ and await success, Create SQ referring to its CQID and await success, then populate SQEs and update Tail.
兩個 Create 都在 Admin CQ 回成功（0/00h），之後 I/O 命令的完成寫入新 I/O CQ；不能到新 CQ 等待它自己的 Create completion。 || Both Create commands complete successfully (0/00h) on Admin CQ. Later I/O completions go to the new I/O CQ; its own Create completion does not.
CQID 在支援範圍內但未建立，回 Completion Queue Invalid（1/00h）；CQID=0 或超界回 Invalid Queue Identifier（1/01h）。 || An in-range CQID that has not been created returns Completion Queue Invalid (1/00h); CQID=0 or out of range returns Invalid Queue Identifier (1/01h).
核對 Create SQ 中的 CQID 與 Host 的 SQ→CQ 映射；成功的 Create CQ 不代表任意 SQ 都自動連到它。 || Match CQID against the host's SQ-to-CQ map. Creating a CQ does not automatically associate every SQ with it.
先檢查 CQ Create 是否已成功完成，而非只是已提交。 || First check that CQ creation completed successfully, not merely that its command was submitted.
''')

add(13,'多個 SQ 共用一個 CQ 與每個 SQ 使用獨立 CQ 有什麼差異？ || How does sharing a CQ differ from giving every SQ its own CQ?','queue',['queue','create','cqe'],'''
在資源用量與完成處理隔離之間取捨；共用 CQ 可以減少 CQ 資源，但會把完成流量集中。 || Trade resource usage against completion-path isolation. Shared CQs reduce CQ resources but concentrate completion traffic.
共享的是 completion slots 與 CQ 關聯通知，不是讓所有 SQ 共用同一個 CID 空間。 || Completion slots and CQ notification are shared; the SQs do not become one CID namespace.
Number of Queues 分別回 SQ／CQ 配額；Create SQ 的 CQID 指定映射，CQ 的 IEN／IV 決定通知配置。 || Number of Queues returns separate SQ/CQ allocations. Create SQ.CQID selects the mapping; CQ.IEN/IV configures notification.
CQE 的 SQID+CID 對回原命令，SQHD 則更新該 SQ 的消費位置。 || CQE.SQID+CID identifies the original command; SQHD updates consumption for that SQ.
先建 CQ，再建兩條以上 SQ 指向同一 CQID；Host 消費每筆 CQE 時按 SQID 分派，最後更新該 CQ 的 Head。 || Create the CQ and multiple SQs referencing it. Dispatch each CQE by SQID, then advance the shared CQ head.
例：SQ1/CID7 與 SQ2/CID7 可以同時存在，回覆必須分別對回；這與在同一 SQ 重用 outstanding CID 不同。 || SQ1/CID7 and SQ2/CID7 may coexist and must be matched separately, unlike reusing an outstanding CID within one SQ.
合法共用不產生錯誤；不存在 CQID 用 Create SQ 的專用 Status。共用 CQ 已滿不等於每個 SQ 自動回 Invalid Queue Size。 || Valid sharing is not an error. Missing CQIDs follow Create SQ status rules; a full shared CQ does not automatically produce Invalid Queue Size for each SQ.
比較可用 completion slots、SQ 流量與 Host 消費速率；不能只看 SQ 數量推測沒有瓶頸。 || Compare completion capacity, submission traffic and host consumption rate; SQ count alone does not establish freedom from bottlenecks.
先看 completion 對應是不是只用 CID，漏了 SQID。 || First check whether completion matching incorrectly uses CID without SQID.
''')

add(14,'Host 如何確認 Controller 支援 Physically Contiguous 或其他 Queue 形式？ || How does the host determine supported queue memory layouts?','queue',['cap','adminreg','create'],'''
讓 queue 的記憶體描述方式符合 controller 可使用的形式；虛擬位址連續不等於實體連續。 || Describe queue memory in a layout the controller supports. Virtual contiguity does not establish physical contiguity.
Admin queue 固定要求實體連續；I/O queue 是否可由多個頁面組成，依 CAP.CQR 與配置位置決定。 || Admin queues require physical contiguity. Discontiguous I/O queues depend on CAP.CQR and memory location.
CQR=1 要求實體連續；CQR=0 允許 I/O 使用非連續頁面。放在 CMB 時還要查 CMBSZ.SQS／CQS、CMBLOC.CQPDS／CQDA。 || CQR=1 requires physical contiguity; CQR=0 allows discontiguous I/O queues. CMB placement additionally requires CMBSZ.SQS/CQS and CMBLOC.CQPDS/CQDA checks.
Create I/O Queue 的 PC=1：PRP1 是 queue base；PC=0：PRP1 是描述 queue 頁面的 PRP list 位址，並非資料傳輸的一般 PRP2 規則。 || With Create I/O Queue.PC=1, PRP1 is the queue base; with PC=0 it points to a queue-page PRP list, distinct from ordinary data-transfer PRP2 rules.
確認位置和能力，建立對齊且完整的 page list，提交 Create；直到成功 Delete 或 reset 前保留 list 位置與內容。 || Confirm placement/support, build a complete aligned page list and Create. Retain the list's address and contents until successful deletion or reset.
controller 能依所選形式取 SQE／寫 CQE；成功 Create 不授權 Host 在執行中重新排列頁面。 || The controller fetches SQEs/writes CQEs through the chosen layout. Successful Create does not authorize rearranging its pages while live.
CQR=1 且 PC=0：Create CQ 必須（shall）回 Invalid Field（0/02h），Create SQ 的對應要求為建議（should）回覆；不支援的 CMB 用法可能為 Invalid Use of Controller Memory Buffer（0/12h）。 || For CQR=1 and PC=0, Create CQ shall return Invalid Field (0/02h), while Create SQ says should. Unsupported CMB usage may return Invalid Use of Controller Memory Buffer (0/12h).
把 CQR、PC、PRP1 解讀與實際頁面布局四者核對；不要只驗證 Create completion。 || Cross-check CQR, PC, PRP1 interpretation and actual page layout, rather than validating only the completion.
先問 PRP1 指向 queue 本體，還是 PRP list；兩者搞反會讓有效位址也變成錯誤結構。 || First ask whether PRP1 addresses queue storage or its page list. Confusing them breaks the layout even with valid addresses.
''')

add(15,'QID 重複、QID 為 0、CQID 不存在、Queue Size 超過 CAP.MQES 或 Interrupt Vector 非法時，Controller 應如何回應？ || Which statuses apply to duplicate/zero QIDs, missing CQIDs, oversized queues and invalid vectors?','queue',['create','status','irq'],'''
把不同參數錯誤對到各自的 Status，不能全部統一寫 Invalid Field。 || Match distinct parameter errors to their defined statuses instead of flattening them into Invalid Field.
檢查的是 Create I/O Queue Admin command；QID 重複依 SQ 或 CQ 各自的識別空間判斷。 || This concerns Create I/O Queue Admin commands. Duplicate QIDs are checked within the SQ or CQ identifier space respectively.
CAP.MQES、Number of Queues 回覆和 PCIe interrupt 配置是合法範圍的依據。 || CAP.MQES, Number of Queues allocations and PCIe interrupt configuration establish legal ranges.
以 QID、CQID、QSIZE、IV 為主，並確認 IOSQES／IOCQES 已初始化；錯誤欄位在 CDW10／11。 || Inspect QID, CQID, QSIZE and IV, and initialization of IOSQES/IOCQES. The relevant parameters are in CDW10/11.
學習測例一次只改一個條件：先建立合法參考配置，再分別送重複 QID、缺 CQID 等假設命令，避免多錯誤遮蔽預期。 || For a learning test, change one condition at a time from a valid baseline; multiple errors can obscure the expected result.
合法參數回成功並建立指定 queue；失敗後不能把該 QID 當成已建立。 || Valid parameters successfully create the queue; after failure, do not treat the requested QID as created.
同類 QID 重複／0／超範圍：1/01h；QSIZE=0 或超支援：1/02h；合法範圍內 CQID 未建立：1/00h；CQID=0／超界：1/01h；非法 IV：1/08h。多個錯誤同時成立時，除特別規定外由實作選擇回哪個。 || Duplicate/zero/out-of-range QID: 1/01h. Zero/unsupported QSIZE: 1/02h. In-range uncreated CQID: 1/00h. Zero/out-of-range CQID: 1/01h. Invalid IV: 1/08h. Unless specified otherwise, implementations choose among simultaneously applicable errors.
Error Information 若有資料，可用 Parameter Error Location 回指欄位；但沒有 More=1 不能硬要求該錯誤一定有 entry。 || When available, Error Information Parameter Error Location can identify the field. Without More=1, do not assume every such error must have an entry.
先检查測例是否真的只有一個非法欄位，以及 expected SCT 是否為 1，避免只比較 SC。 || First check that only one field is invalid and the expected SCT is 1, rather than comparing SC alone.
''')

add(16,'Number of Queues Feature 回傳的數值與實際可建立的 Queue 數量有什麼關係？ || How do Number of Queues results relate to queues that can actually be created?','feature',['number','create'],'''
先取得 I/O SQ 與 CQ 配額，再在配額內建立 queue；配額不是 queue 本身，也不是每條 queue 的深度。 || Obtain SQ/CQ allocations before creating queues. Allocation is neither an instantiated queue nor queue depth.
FID 07h 作用於 controller，不包含 Admin SQ／CQ。 || FID 07h has controller scope and excludes Admin SQ/CQ.
用 Set Features FID 07h 的 CQE DW0 回覆判斷實際配置，之後可 Get Features 讀回。CAP.MQES 另限制每條深度。 || Use Set Features FID 07h CQE DW0 for actual allocations, with Get Features readback. CAP.MQES separately limits per-queue depth.
CDW11 的 NSQR／NCQR 與 DW0 的 NSQA／NCQA 都是 zero-based；回覆可能比要求少，也可能因配置單位而較多。 || Requested NSQR/NCQR and returned NSQA/NCQA are zero-based. Allocations may be smaller or larger than requested because of allocation units.
CLR 後、任何 I/O Queue 建立前設定；第一筆成功設定決定此次配置。之後到下一次 CLR 前配置數不改變。 || Set it after CLR and before creating any I/O queue. The first successful setting fixes allocation until the next CLR.
例：DW0=00030007h 表示 4 個 CQ、8 個 SQ 配額；仍須個別 Create，QID 範圍分別依 4 與 8 判斷。 || DW0=00030007h allocates four CQs and eight SQs. Each still requires Create, with the respective QID ranges.
已有 I/O queue 再 Set 必須回 Command Sequence Error（0/0Ch）；Requested=FFFFh 應回 Invalid Field（0/02h）。尚未建 queue 的後續 Set 應成功但不改已配置數。 || Setting after an I/O queue exists shall return Command Sequence Error (0/0Ch). Requested=FFFFh should return Invalid Field (0/02h). Subsequent Set before queue creation should succeed without changing allocation.
核對回覆的配額、實際已建 queue 清單與 MQES 三份資訊，不能把 Get 的配額解成目前存在數。 || Compare allocations, the actual created-queue list and MQES. Allocated counts are not current existence counts.
先檢查是否用了 requested 值而忽略 returned 值，或忘記對 NSQA／NCQA 加 1。 || First check whether requested values were used instead of returned allocations or whether +1 was omitted.
''',{12:'CLR 後第一筆成功 Set FID 07h 重新配置 queue 數；Host 應重新取得回覆，再重建 I/O queue，不能直接沿用前次配額。 || The first successful Set FID 07h after CLR allocates anew. Read the result and recreate queues rather than assuming the previous allocation.',13:'受影響 controller 經 CLR 後重新協商 Number of Queues；NVM Subsystem Reset 不會保留舊 I/O Queue 配置讓 Host 直接送 I/O。 || Renegotiate Number of Queues after the affected controller’s CLR. NVM Subsystem Reset does not preserve old I/O queues for immediate reuse.',14:'重新初始化、設定 FID 07h 並建立 queue；Saved／Default 的一般概念不能代替這個初始化順序。 || Reinitialize, set FID 07h and create queues; generic Saved/Default concepts do not replace this initialization sequence.'})

add(17,'Host 刪除 I/O Queue 時，SQ 與 CQ 的相依關係如何限制刪除順序？ || Why must associated SQs be deleted before their CQ?','queue',['queue','delete'],'''
避免仍有命令要完成的 SQ 失去回覆位置。對關聯 queue，這是 Host 必須遵守的刪除順序。 || Prevent active SQs from losing their completion destination. For associated queues this is a required host deletion order.
一個 CQ 可能被多條 SQ 使用，必須刪除所有相關 SQ，不是只刪 QID 相同的 SQ。 || A CQ may serve multiple SQs. Delete every associated SQ, not only an SQ with the same numeric QID.
使用 Host 在 Create SQ 時保存的 SQ→CQID 對照；Number of Queues 不提供這張連線清單。 || Use the host's SQ-to-CQID map from creation. Number of Queues does not provide this association list.
Delete I/O SQ／CQ 的 CDW10.QID 指定對象；它們都透過 Admin SQ 提交。 || Delete I/O SQ/CQ selects the target with CDW10.QID; both travel through Admin SQ.
停止向目標 SQ 提交，適當等待既有命令，逐一 Delete SQ 並等成功，消費需要處理的舊完成，再 Delete CQ。 || Stop submissions, appropriately drain work, delete each associated SQ and await success, process needed old completions, then delete the CQ.
Delete CQ 成功後，Host 才可收回其 PRP list 與 queue 資源；Delete SQ 的成功另建立該 SQ 命令處理的終止界線。 || Successful Delete CQ allows reclamation of its PRP list and queue resources. Successful Delete SQ separately establishes termination of processing for that SQ's commands.
尚有相關 SQ 時 Delete CQ 必須回 Invalid Queue Deletion（1/0Ch）；QID=0 或非法對象回 Invalid Queue Identifier（1/01h）。 || Delete CQ with associated SQs shall return Invalid Queue Deletion (1/0Ch); zero or invalid QID returns Invalid Queue Identifier (1/01h).
把刪除成功時間接到記憶體釋放時間；「已送 Delete」不足以允許提前收回 DMA 記憶體。 || Correlate successful deletion with memory reclamation. Merely submitting Delete does not authorize early reclamation of DMA memory.
先檢查 CQ 是否還被另一條 SQ 指向，而非只檢查 CQ 自己是否已空。 || First check whether another SQ still references the CQ, not only whether the CQ appears empty.
''')

add(18,'刪除不存在的 Queue、仍被 SQ 使用的 CQ 或仍有 Outstanding Command 的 SQ 時，應如何處理？ || What happens when deleting a missing queue, a referenced CQ or an SQ with outstanding commands?','queue',['delete','reset'],'''
分開「刪除要求非法」與「合法刪除造成命令終止」；仍有 outstanding 並不直接讓 Delete SQ 變成非法。 || Distinguish an invalid deletion request from valid deletion terminating commands. Outstanding work does not itself make Delete SQ illegal.
刪 SQ 影響那條 SQ 的所有未完成 I/O；刪 CQ 先受所有相關 SQ 的存在狀態限制。 || SQ deletion affects its outstanding I/O; CQ deletion depends on the existence of every associated SQ.
先查 Host 的建立／刪除紀錄與 outstanding 清單。這些是執行狀態，不是 Identify 的選配能力。 || Consult host creation/deletion and outstanding-command records. These are runtime state, not Identify optional capabilities.
Delete 的 QID 必須有效且不為 0；目標 I/O 命令仍以各自 SQID／CID 辨識。 || Delete requires a valid nonzero QID; affected I/O commands retain their own SQID/CID identities.
正常拆除先排空再刪。若為中止工作而刪 SQ，等 Delete 成功後，把未收到 CQE 的原命令作隱含中止處理。 || Drain before normal teardown. If deleting an SQ to stop work, treat remaining commands without CQEs as implicitly aborted after successful Delete.
Delete SQ 成功前，原命令可能已成功或回中止 CQE；成功之後不得再為原 SQ 命令寫 completion。 || Before successful Delete SQ, original commands may complete normally or with abort status. After success, no further completions may be posted for those commands.
非法 QID：1/01h；仍有 SQ 的 CQ：1/0Ch。原 I/O 若因刪 SQ 中止，狀態為 Command Aborted due to SQ Deletion（0/08h），也可能以 Delete 成功形成隱含完成。 || Invalid QID: 1/01h. CQ still referenced: 1/0Ch. I/O aborted by SQ deletion uses 0/08h, including implicit completion established by successful Delete.
測試應同時計數已收到 CQE 與 Delete 成功後隱含中止者；不要要求每個原命令都必須實際出現一筆 CQE。 || Account for both received CQEs and implicit aborts after successful Delete; do not require a physical CQE for every original command.
先檢查 Delete SQ 是否已成功完成；在它還 outstanding 時，不能宣布所有原命令已停止。 || First check whether Delete SQ itself completed successfully. Its outstanding state does not establish that all original work stopped.
''')

add(19,'Queue 刪除後，Controller 是否還能存取原 Queue Memory 或回報原 Queue 的 Completion？ || May the controller access deleted queue memory or post completions for its old commands?','queue',['delete','create','queue'],'''
找出可以安全收回記憶體的界線，並區分「先前已寫入但 Host 晚看到」與「刪除成功後才寫入」。 || Establish the memory-reclamation boundary and distinguish an earlier write observed late from a new write after successful deletion.
Delete SQ 不會同時刪除共用 CQ；CQ 中先前完成仍可能等待 Host 消費。 || Deleting an SQ does not delete its shared CQ; already posted completions may remain for host consumption.
以 Admin CQ 上 Delete 的成功結果為界，不以 Host 送出時間或自訂 timeout 為界。 || Use successful Delete completion on Admin CQ as the boundary, not submission time or a host timeout.
追蹤被刪 QID、關聯 CQID、PRP list 位址及 memory lifetime。相同位址重新使用後必須能區分新舊 queue。 || Track deleted QID, associated CQID, PRP-list address and memory lifetime. Reused addresses require distinguishing queue lifetimes.
停止提交、Delete 並等成功，再收回對應 queue／PRP list。只刪 SQ 時繼續妥善處理仍存在 CQ 的已張貼內容。 || Stop submissions, successfully delete, then reclaim the corresponding queue/list memory. With SQ-only deletion, handle existing posted entries in the surviving CQ.
成功 Delete SQ 後不得新增原 SQ 命令的 completion；成功 Delete CQ 後其描述 PRP list 可釋放，已刪 queue 不再是可用 DMA 目標。 || After successful Delete SQ, no new completions for its old commands may be posted. Successful Delete CQ permits releasing its list; a deleted queue is no longer a valid DMA target.
若 Delete 本身失敗或沒有完成，不能推論記憶體已可收回。逾時不是另一種 Successful Completion。 || Failure or absence of Delete completion does not authorize memory reclamation. Timeout is not a substitute for success.
用寫入時間、CQ Phase、Delete completion 與 Host 消費時間核對；晚消費的舊 CQE 不等於違規的晚寫入。 || Correlate write time, phase, Delete completion and host consumption. Late consumption of an old CQE is not necessarily a prohibited late write.
先確認所見 CQE 真正寫入於 Delete 成功之前還是之後。 || First establish whether the CQE was actually posted before or after successful Delete.
''')

add(20,'Queue Level Reset 的影響範圍是什麼？Outstanding Command 應如何處理？ || What is the scope of Queue Level Reset, and how is outstanding work handled?','queue',['reset','delete','create'],'''
在不重設整個 controller 的情況下重建 I/O queue。PCIe 的 Queue Level Reset 是刪除再建立，不是另一個 Reset opcode。 || Rebuild I/O queues without resetting the whole controller. PCIe Queue Level Reset means deletion and recreation, not a separate reset opcode.
只重設目標 queue 及必要相依 queue；若重建 CQ，所有使用它的 SQ 都需先刪除並在 CQ 重建後再建。 || Reset the target and its necessary dependencies. Rebuilding a CQ requires deleting its SQs first and recreating them afterward.
依已建立的 queue 關係與 Create／Delete 規則執行，不靠一個另行定義的 Queue Reset Feature。 || Use existing queue associations and Create/Delete rules, not a separate Queue Reset feature.
Delete SQ／CQ、Create CQ／SQ；QID 可重用，但 queue 記憶體與指標從新生命週期開始。 || Use Delete SQ/CQ and Create CQ/SQ. QIDs may be reused, but memory and pointers begin a new lifetime.
正常應先讓工作完成，再刪除；需要中止時按 Delete SQ 的明確／隱含完成規則。新 CQ 初始化 Phase，先 CQ 後 SQ。 || Normally let work finish before deletion. For cancellation, apply explicit/implicit Delete SQ completion rules. Initialize new CQ phases and create CQ before SQ.
重建成功後新命令可執行，原 outstanding 命令不會自動搬入新 SQ。 || New commands execute after reconstruction; old outstanding commands are not automatically migrated into the new SQ.
錯誤刪 CQ 得 1/0Ch；沒有有效 CQ 就先建 SQ 得相應 CQID 錯誤。Queue reset 本身沒有額外統一 Status。 || Deleting a referenced CQ returns 1/0Ch; premature SQ creation returns the applicable CQID error. Queue reset has no additional universal status.
核對刪除／建立順序與新舊 CID 對照，並檢查其他獨立 queue 是否保持正常。 || Check teardown/recreation ordering, command-lifetime tracking and continued operation of independent queues.
先列出目標 CQ 的所有使用者；漏一條共享 SQ 就可能使重設流程不合法。 || First enumerate every SQ using the target CQ; omitting one can invalidate the reset sequence.
''')

add(21,'Controller Reset 後，原有 I/O Queue 是否有效？Host 需要重新執行哪些操作？ || Are old I/O queues valid after Controller Reset, and what must the host do again?','queue',['reset','init','number','create'],'''
把故障前的命令與恢複後的新命令分開，避免誤認殘留 completion。 || Separate pre-failure commands from new work after recovery to avoid accepting stale completions.
Controller Level Reset 刪除該 controller 的全部 I/O SQ／CQ；不同於只刪除一條 SQ。 || Controller Level Reset deletes all I/O SQs/CQs of that controller, unlike deleting only one SQ.
重讀必要 Identify，確認 Number of Queues 配額與 entry size／interrupt 設定，不能直接假設前次值仍有效。 || Re-read necessary Identify data and verify queue allocations, entry sizes and interrupt settings rather than assuming previous values remain usable.
Admin Register、CC、Get／Set Features、Create CQ／SQ 共同構成重建路徑。 || Admin registers, CC, Get/Set Features and Create CQ/SQ together establish the recovery path.
確認 RDY=0→初始化 Admin CQ Phase 與 CC→Enable、等 RDY→恢復必要 Feature→Set Number of Queues→建 CQ→建 SQ→允許新 I/O。 || Confirm RDY=0, initialize Admin CQ phases and CC, enable/wait ready, restore needed features, set Number of Queues, create CQ then SQ, and allow new I/O.
每次 Create 在 Admin CQ 成功後，對應新 queue 才有效；不論是否沿用相同 QID 或位址。 || Each new queue becomes valid after its successful Create completion on Admin CQ, even when reusing an identifier or address.
直接更新舊 queue Doorbell 不構成合法恢復，不能要求它繼續處理；重建命令的失敗則依各自 Status 處理。 || Updating old queue doorbells is not a valid recovery method. Failures of reconstruction commands follow their specific status rules.
保存 reset 前後的 queue generation 與命令對照；這是 Host 追蹤方法，不是新增一個 NVMe wire field。 || Track queue lifetimes and command mappings across reset in host software; this is not a new NVMe wire field.
先看 Host 是否在新 Create 成功前就恢復 I/O。 || First check whether host I/O resumed before new Create commands succeeded.
''')
