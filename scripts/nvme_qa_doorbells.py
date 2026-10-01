from scripts.nvme_qa_model import add

add(22,'Host 應在什麼時候更新 SQ Tail Doorbell 與 CQ Head Doorbell？ || When should the host update SQ Tail and CQ Head doorbells?','register',['queue','pcie'],'''
Host 需要通知 controller，哪些 SQE 已經準備好，以及哪些 CQE 已經處理完畢。更新 SQ Tail 是提交新命令；更新 CQ Head 則是釋放已處理的完成位置，讓 controller 可以再次使用。 || Notify the controller of completed host memory work: SQ Tail submits commands, while CQ Head releases completion slots.
每條 SQ／CQ 各有自己的 Doorbell；更新其中一條不會自動更新另一條。 || Each SQ/CQ has its own doorbell; updating one does not update another.
更新前，先確認 queue 仍然有效，而且 controller 已就緒。提交命令時也要確認 SQ 有足夠的可用位置，再依 CAP.DSTRD 找到正確的 Doorbell Register。 || Verify a valid queue, a ready controller, sufficient free slots and the register address derived from CAP.DSTRD.
SQ Tail 指向下一個可放入 SQE 的位置；CQ Head 指向下一個等待 Host 處理的 CQE。Doorbell 要寫入更新後的索引值，而不是這次新增或處理了幾筆。 || SQ Tail points to the next insertion slot; CQ Head points to the next completion to consume. Writes contain new pointer values, not increments.
提交時，Host 先寫好完整的 SQE，並依平台要求確保 controller 能看見這些記憶體內容，之後才更新 SQ Tail。接收完成結果時，則先讀取並處理有效的 CQE，再更新 CQ Head。Host 可以一次提交多筆命令，也可以一次釋放多個已處理的完成位置。 || Make complete SQEs visible using the platform's memory-ordering requirements before updating Tail. Consume valid CQEs before updating Head; batching is allowed.
更新 SQ Tail 後，controller 才能得知哪些新命令可以讀取；更新 CQ Head 後，controller 才能得知哪些完成位置可以重用。因此，CQ Head 前進並不表示 Host 提交了新的 I/O 命令。 || The controller learns which commands can be fetched and which CQ slots can be reused. Advancing CQ Head does not submit new I/O.
如果 Host 尚未處理 CQE 就提前釋放位置，該 CQE 可能被後續的完成結果覆寫。如果 SQE 尚未準備好就更新 Tail，controller 也可能讀到不完整的命令。這些都是使用順序錯誤，不能預期 controller 一定會回傳某個固定的錯誤 CQE。 || Releasing unconsumed CQEs risks overwrite. Submitting incomplete SQEs violates usage ordering and has no guaranteed single error CQE.
驗證時，依時間先後比對 Host 寫入 SQE、更新 Tail、controller 寫入帶有新 Phase 的 CQE，以及 Host 更新 Head 這四個動作。它們分別代表準備命令、提交命令、回報完成及釋放完成位置，不能互相替代。 || Build a timeline of SQE writes, Tail updates, CQE phase changes and Head updates; they have distinct roles.
先檢查 Doorbell 是否誤寫成「這次處理的筆數」。正確值應是更新後的索引；索引到達 queue 尾端後，要依 queue 大小回到起點。 || First check whether the host wrote a count instead of the new index modulo queue size.
''')

add(23,'Doorbell 值重複、倒退、超過 Queue 範圍或寫到錯誤 QID 時，可能造成什麼問題？ || What happens with repeated, apparently backward, out-of-range or wrong-QID doorbells?','register',['queue','pcie','aer'],'''
判斷指標移動是否合法，避免把環狀索引當成只會遞增的計數器。 || Validate pointer movement without treating a ring index as a monotonically increasing counter.
錯誤會影響被寫入 Doorbell 的 queue。如果是多條 SQ 共用的 CQ，影響還可能延伸到這些 SQ。另外，向不存在的 queue 寫 Doorbell，與向有效 queue 寫入非法值，是兩種不同情況。 || Errors affect the target queue and possibly SQs sharing its CQ. Access to a nonexistent queue differs from an invalid value on an existing queue.
判斷指標是否合法，需要知道 queue 大小、原來的指標、可用或已處理的位置數量，以及 Doorbell 對應的 QID。只看新寫入的數字，無法判斷這次移動是否正確。 || Need size, previous pointer, available/consumed slots and QID mapping. The new value alone is insufficient.
合法索引介於 0 與 size−1。再次寫入相同的值，不表示新增了一批位置；寫入較小的值也不一定是倒退，因為指標可能剛好跨過 queue 尾端，回到起點。 || New values lie in 0..size−1. A repeated value announces no new slots; a numerically smaller value may be a valid wrap.
例如，queue 大小為 8，Tail 從 6 變成 1，代表前進 3 個位置。這次提交是否合法，還要確認原本有 3 個可用位置，而且對應的 SQE 都已準備好。相反地，從 6 再寫回 6，不能用來表示提交了整整一圈的命令。 || For size=8, Tail 6→1 advances three slots, provided three are free and populated. A 6→6 write cannot announce a full ring of new commands.
合法的指標更新，能讓 controller 算出新提交或新釋放的位置數量。不過，Host 不應靠讀回 Doorbell 來驗證寫入結果，因為 Doorbell 的讀回值由廠商定義。 || A valid movement communicates the correct count. Doorbell readback is vendor-specific and is not a verification method.
向有效 queue 寫入非法值時，適用 Invalid Doorbell Write Value 的非同步錯誤處理；向不存在的 queue 寫 Doorbell 時，結果則未定義。前者的事件資訊碼不是這次 MMIO 寫入的 CQE Status，兩者不能混為一談。 || Invalid values on an existing queue have Invalid Doorbell Write Value asynchronous handling; writing a nonexistent queue doorbell is undefined. Event information is not a CQE status for the MMIO write.
先依原指標、queue 大小及剩餘空間判斷移動是否合法，不要只比較新舊數字的大小。若發生 Doorbell 錯誤，還應一起檢查對應的非同步事件，以及受影響 queue 是否停止取得新命令。 || Compare old pointer, ring size and available space, not just numeric ordering. Correlate the error event with affected-queue command consumption.
先用 (new−old+size) modulo size 算出前進量，再確認這些位置是否確實可以提交或釋放。 || First calculate (new−old+size) modulo size and verify that the resulting advance is legal.
''',{9:'依 Base §3.3.1.2，若 Doorbell 值非法，而且有尚未完成的 Asynchronous Event Request，controller 會透過它回報對應錯誤事件。受影響的 SQ 可以完成已取得的命令，但不再取得新命令；Host 則需刪除並重建 queue。 || Base §3.3.1.2 specifies an error event for an invalid doorbell value with an outstanding Asynchronous Event Request. An affected SQ may complete consumed commands but consumes no new ones; the host deletes and recreates the queue.',10:'這是 Error 類型的非同步事件，應讀取事件指定的 Log，取得補充資料。MMIO 寫入本身沒有 More 位元。另外，若是寫到不存在 QID 的 Doorbell，規範已將結果列為未定義，不能再要求它一定產生 Log。 || Follow the Error event’s indicated log for additional information; the MMIO write itself has no More bit. Do not invent mandatory logging for undefined nonexistent-QID accesses.'})

add(24,'Host 如何根據 CAP.DSTRD 計算每個 SQ 與 CQ Doorbell 的位置？ || How are SQ/CQ doorbell addresses calculated from CAP.DSTRD?','register',['cap','pcie','pciconfig'],'''
Host 必須根據 NVMe Register 的起始位址及 QID，找出要更新的 Doorbell 位址，才能把通知送到正確的 queue。 || Derive the unique doorbell address from the NVMe register base and QID.
Doorbell 位址以該 controller 的 MMIO 起始位址為基準，不是以 SQ 或 CQ 記憶體的起始位址為基準。 || Offsets are relative to the controller's MMIO base, not a queue's memory address.
PCI BAR0／BAR1 用來找出 NVMe Register 空間的位置；CAP.DSTRD 則用來計算相鄰 Doorbell 的位址間距。 || PCI BAR0/BAR1 locate the NVMe register space; CAP.DSTRD provides adjacent-doorbell stride.
stride=4×2^DSTRD；SQy offset=1000h+2y×stride；CQy offset=1000h+(2y+1)×stride。每個 Doorbell 本身仍是 32 bits。 || stride=4×2^DSTRD; SQy offset=1000h+2y×stride; CQy offset=1000h+(2y+1)×stride. Each doorbell itself remains 32 bits.
先取得映射後的 Register 起始位址，再由 DSTRD 算出 stride。接著依 QID 選用 SQ 或 CQ 的公式，算出 Doorbell 位址，最後使用規定的存取寬度執行 MMIO 寫入。 || Obtain the mapped base, calculate stride, select the SQ/CQ expression for QID, then access with a legal MMIO width.
例：DSTRD=2、QID=3，SQ offset=1060h、CQ offset=1070h。把各 offset 加到 controller base，才是完整位址。 || DSTRD=2 and QID=3 give SQ offset 1060h and CQ offset 1070h. Add the controller base for full addresses.
計算位址本身不會產生 Command Status。如果算錯位址，可能寫到另一條有效 queue，也可能形成結果未定義的存取。controller 無法因此得知 Host 原本想更新哪一條 queue。 || Address calculation has no status. A wrong address can select another valid queue or an undefined location; the controller cannot infer host intent.
把算出的 Doorbell 位址，與建立 queue 時使用的 QID 及 BAR 映射範圍交叉比對。DSTRD 是計算間距時使用的編碼，不能直接當成 byte 數，也不能直接拿來乘上 QID。 || Match results against created QIDs and the mapped BAR range. DSTRD is an exponent, not a byte count or a direct QID multiplier.
先確認公式是否漏掉 SQ／CQ 交錯所需的 2y 與 2y+1。 || First check the alternating 2y and 2y+1 indices.
''')

add(25,'Host 能否存取未建立、已刪除或 Controller 未 Enable 時的 Queue Doorbell？ || May the host access doorbells of uncreated/deleted queues or a disabled controller?','register',['pcie','queue','qattr','delete'],'''
Doorbell 只有在對應 queue 有效時才能使用。即使 Host 能算出某個 Doorbell 的 Register 位址，也不代表那條 queue 目前已經建立。 || Respect queue lifetime: an address in the doorbell region does not mean a queue currently exists.
I/O queue 必須在建立成功後才能使用；刪除成功或 Controller Reset 之後，Host 就不能再沿用原來的 queue。 || Use each queue after successful creation and retire it after successful deletion or controller reset.
檢查 Host 維護的 queue 紀錄，以及 CC.EN、CSTS.RDY。Doorbell 的讀回值不能用來判斷 queue 是否存在。 || Check host queue-lifetime records, CC.EN and CSTS.RDY; doorbell readback cannot establish queue existence.
SQyTDBL 與 CQyHDBL 分別通知有效 queue 的新 Tail 與 Head。Admin Queue 的 QID 為 0，其設定來自 AQA、ASQ、ACQ，並隨 controller 初始化建立可用狀態。 || SQyTDBL/CQyHDBL announce pointers for valid queues. Admin Q0's environment comes from AQA/ASQ/ACQ and initialization.
對 I/O queue，Host 先建立並等待成功，再開始使用。準備刪除時，先停止提交新命令，並在 Delete 成功後停止使用原 queue。Controller Reset 之後，即使打算沿用相同 QID，也必須重新建立 I/O queue。 || Create successfully, use, stop submissions, successfully delete, then stop all use. Reused QIDs after reset still require reconstruction.
正確管理 queue 的使用期間，就不應向不存在的 queue 寫 Doorbell。Doorbell 只負責通知指標更新，不會自動替 Host 建立 queue。 || Correct lifetime management avoids nonexistent-queue writes. A doorbell does not automatically create a queue.
PCIe §3.1.2 將向不存在的 SQ 或 CQ 寫 Doorbell 列為結果未定義的行為。CSTS.RDY=0 時也不符合命令提交的前提，因此不能要求 controller 一定回報 Invalid Queue Identifier 或某個指定的非同步事件。 || PCIe §3.1.2 defines writes to nonexistent SQ/CQ doorbells as undefined. RDY=0 violates submission prerequisites. No guaranteed Invalid Queue Identifier or AER follows.
以 Create 與 Delete 的完成時間界定 queue 的有效期間，再檢查所有 Doorbell 更新是否都發生在這段期間內。 || Use Create/Delete completion times to establish the valid interval and check doorbell timestamps against it.
先檢查其他 CPU 是否仍保留舊 queue 的參照，並在 queue 已刪除後繼續更新它的 Doorbell。 || First check whether another CPU still holds a stale reference to the deleted queue.
''')

add(26,'SQ Tail 與 CQ Head 發生 Wrap-around 時，Host 與 Controller 應如何處理？ || How should SQ Tail and CQ Head wrap around?','register',['queue','pcie'],'''
環狀 queue 讓固定大小的記憶體可以重複使用。指標走到尾端後回到起點，不需要每繞一圈就重新建立 queue。 || Reuse fixed storage as a ring without recreating the queue each turn.
SQ Tail 與 CQ Head 都由 Host 推進；SQ Head 與 CQ Tail 則由 controller 維護。判斷指標變化時，要先分清楚是哪一端負責更新。 || The host advances SQ Tail and CQ Head; the controller maintains SQ Head and CQ Tail.
計算時使用該 queue 實際配置的位置數 N，也就是 QSIZE+1。CAP.MQES 表示能力上限，不能直接當成每條 queue 的實際大小。 || Use the actual N=QSIZE+1 slots, not CAP.MQES as every queue's size.
每前進一步計算 (index+1) modulo N。Tail 是下一個寫入位置，Head 是下一個讀取位置，兩者相等表示空。 || Advance with (index+1) modulo N. Tail is the next insertion position, Head the next consumption position; equality means empty.
索引從 N−1 回到 0 時，Host 仍須正確追蹤這次實際前進了幾個位置。更新 SQ Tail 不能超過可用空間；更新 CQ Head 不能跳過尚未處理的 CQE。 || Wrap N−1 to zero while tracking the real count. Do not overfill the SQ or release unconsumed CQ entries.
例如 N=8，CQ Head 從 7 變成 2，表示 Host 已處理索引 7、0、1 的 3 筆 CQE，而不是指標倒退了 5 個位置。 || With N=8, CQ Head 7→2 consumes slots 7, 0 and 1: three entries, not a backward movement of five.
合法的 wrap-around 不是錯誤。若誤把 queue 大小 N 當成最大合法索引，並將 N 寫入 Doorbell，才會超出範圍。非法指標的處理方式見第 23 題。 || Valid wrap is not an error. Writing N as an index is out of range; invalid-pointer handling follows Question 23.
驗證時，要一起檢查 Head、Tail 與 queue 大小的環狀索引關係。Doorbell 數值變小，可能只是正常跨過尾端，不能單憑這點判定違反規範。 || Validate modulo relationships among Head, Tail and size. A decreasing doorbell value alone is not a violation.
先確認程式使用的是實際位置數 N，還是編碼值 QSIZE。若忘記加 1，每次繞回起點的計算都會差一個位置。 || First check whether the ring uses N slots or encoded QSIZE. Omitting +1 creates an error every wrap.
''')

add(27,'CQ Wrap-around 後 Phase Tag 如何變化？Host 如何利用 Phase Tag 辨識新 Completion？ || How does the CQ phase change across wrap, and how does the host identify a new completion?','queue',['cqe','queue','reset'],'''
CQ 的同一個位置會反覆使用。Phase Tag 讓 Host 分辨目前看到的是這一圈的新完成結果，還是上一圈留下的舊資料。 || Let the host distinguish a newly posted completion from data left in the same slot by a previous pass.
Phase 用來辨識 CQE 屬於哪一圈，不表示命令成功或失敗，也不是 SQ 的指標。 || Phase belongs to the CQ ring lifetime; it is neither CID success/failure nor an SQ pointer.
Phase 是 PCIe CQE 的基本機制，不需要額外啟用 Feature。建立 CQ 前，Host 將每個位置的 Phase 初始化為 0，並將自己第一次等待的 Phase 設為 1。 || This is a basic PCIe CQE mechanism, not an optional feature. Initialize every slot's phase to zero before creation and initially expect one.
CQE DW3 bit16 為 P；controller 每次在同一 slot 放入新 CQE 時反轉該 slot 的前次 Phase。 || CQE DW3 bit16 is P. Each new posting in a slot inverts that slot's previous phase.
Host 先檢查目前 Head 指向的 CQE；只有 P 符合期待值時，才處理這筆完成結果。當 Head 從 N−1 回到 0 時，Host 才反轉期待的 Phase，開始辨識下一圈的 CQE。 || Inspect the current Head; consume only when P matches the expected phase. Flip the expected phase when Head wraps N−1→0.
第一圈的新 CQE 使用 P=1，下一圈使用 P=0。Phase 是每繞完一圈才改變，不是相鄰的每筆 completion 都依序交替為 1、0、1、0。 || Newly posted entries use P=1 on the first pass and P=0 on the next. Adjacent completions do not alternate 1,0,1,0 within one pass.
Phase 不符合期待值，表示該位置還沒有這一圈的新完成結果，並不代表某種錯誤 Status。此時不能把該位置殘留的 CID 或 SC 當成新命令的結果。 || A phase mismatch means no new completion at that position, not an error status. Do not decode stale CID/SC as a new result.
測試至少要讓 CQ 完整繞過一圈，並比對 CQ Head、Host 期待的 P 與 CQE 實際的 P。重建 queue 時必須重新初始化，不能沿用前一次 queue 的期待值。 || Exercise at least one wrap and compare Head, expected P and actual P. Reinitialize after queue recreation rather than inheriting the old phase.
先檢查 Host 是否誤在處理每一筆 CQE 後都反轉期待的 P，或在重設後忘記重新初始化 CQ。 || First check for toggling the expected phase after every entry or failing to initialize CQ after reset.
''')

add(28,'CQ Full 通常如何形成？CQ Full 時 Controller 能否繼續處理相關 SQ？ || How does CQ Full arise, and may related SQ processing continue?','queue',['queue','order'],'''
CQ 的空間管理用來避免尚未處理的完成結果被覆寫。當 controller 產生 completion 的速度，超過 Host 處理並釋放位置的速度，CQ 就可能變滿。 || Flow control prevents overwriting unconsumed completions. Fullness usually means completions arrive faster than the host releases slots.
影響該 CQ 與其關聯 SQ；其他不使用此 CQ 的 SQ 必須繼續處理。 || It affects the CQ and associated SQs. Processing must continue for SQs not associated with that full CQ.
判斷容量時，要看 CQ 的實際大小、Host 更新 CQ Head 的情況，以及尚未處理的完成結果。Number of Queues 表示 queue 數量，不能用來推算一條 CQ 能容納多少筆 CQE。 || Inspect actual CQ size, Head updates and pending completions, not Number of Queues.
CQ 保留一個位置不用；當 (Tail+1) modulo N = Head 時，就表示 CQ 已滿。這裡的 Tail 由 controller 維護，Host 不能直接讀取它。 || Full means (Tail+1) modulo N = Head, leaving one slot unused. Tail is controller-internal, not directly readable by the host.
Host 逐筆確認 Phase 並處理 CQE，之後再更新 Head，釋放已處理的位置。在可用位置出現之前，controller 不得向這條 CQ 寫入新的完成結果。 || The host validates phases, processes results and advances Head. The controller shall not post another completion to this CQ until a slot is available.
controller 可以停止處理關聯 SQ 中的新 entry。規範在這裡使用 may，因此不能進一步推論：所有已取得的命令都必須立刻停止，或都必須繼續執行。 || The controller may stop processing further associated SQ entries. This does not require all consumed commands either to stop instantly or to continue unconditionally.
CQ Full 是空間已滿的狀態，不是一個必須回報的 NVMe 錯誤碼。controller 不能為了騰出空間，覆寫 Host 尚未確認處理完畢的 CQE。 || CQ Full is a capacity state, not a required error status. Overwriting unacknowledged entries to make room violates correctness.
如果只有共用這條 CQ 的 SQ 停滯，先檢查 Host 是否持續處理並釋放 CQE。如果連使用其他獨立 CQ 的 SQ 也因這條 CQ 已滿而停止，則要檢查是否違反繼續處理其他 SQ 的要求。 || If only its associated SQs stall, inspect consumption first. If independent SQs stop because of this full CQ, check the requirement to continue their processing.
先檢查 Host 是否已讀取 CQE，卻忘了更新 CQ Head Doorbell。單純讀取記憶體，不會通知 controller 這些位置已經可以重用。 || First check for reading CQEs without updating CQ Head. Reading alone does not release space as seen by the controller.
''')

add(29,'Host 釋放 CQ 空間後，Controller 應如何恢復 Command 處理？ || How does processing resume when the host releases CQ space?','queue',['queue','pcie','order'],'''
CQ 空間釋放後，原本受容量限制的工作便能繼續。CQ Full 本身不表示 queue 已失效，因此不需要只因空間曾經用完就重新建立 queue。 || Resume work after capacity becomes available rather than treating ordinary CQ Full as a recreation error.
Host 釋放的是這條 CQ 中的完成位置，讓關聯 SQ 的命令可以回報結果。這不會改變可建立的 queue 數量，也不會改變 namespace 的能力。 || Released slots serve completions from associated SQs; queue allocations and namespace capabilities do not change.
先確認 queue 仍然存在，而且沒有其他停止處理的原因，例如正在重設、CSTS.CFS 已設定，或 queue 處於 Processing Paused 狀態。 || Verify a live queue and no independent stop condition such as reset, CFS or Processing Paused.
Host 將新的 Head 索引寫入 CQ Head Doorbell。controller 根據 Head 的前進量得知哪些位置可以重用，後續寫入 CQE 時仍須使用正確的 Phase。 || The host writes the new CQ Head, allowing the controller to reuse released slots with correct phases for subsequent completions.
Host 處理 CQE 並更新 Head 後，controller 才得知有新的可用空間，接著可以寫入等待回報的完成結果，並繼續處理受影響的工作。實際執行次序仍受仲裁設定及其他正常條件限制。 || Consume CQEs, update Head, allow slots to become available, then post waiting completions and continue affected work under normal scheduling and other constraints.
已釋放的位置可以再次使用，不必重建 queue。不過，規範沒有為所有裝置訂出同一個固定時間，要求從 Head 更新到下一筆 CQE 出現必須相隔多久。 || Released slots are reusable without recreation. There is no universal fixed latency from a Head update to the next CQE.
正確更新 CQ Head 不會另外產生一筆成功 CQE。如果 Head 值非法，應依 Doorbell 的錯誤處理規則判斷，不能套用 Create Queue 的錯誤 Status。 || Correct release has no special success CQE. An invalid Head remains a doorbell-usage issue, not a Create Queue error.
檢查後續 CQE 是否寫入合法且已釋放的位置，並比較共用這條 CQ 的 SQ 與其他獨立 SQ 的處理進度。 || Verify legal reuse of released slots and compare progress on associated and independent SQs.
先確認 Head 是否寫到正確 CQ 的 Register。如果 QID 用錯，Host 雖然執行了寫入，原本已滿的 CQ 卻沒有收到空間已釋放的通知。 || First verify the correct CQ doorbell address; updating another QID does not release this full CQ.
''')

add(30,'多個 SQ 共用一個 CQ 時，Host 如何依 SQID 與 CID 辨識 Completion 來源？ || How does the host identify completions from SQs sharing a CQ?','queue',['cqe','queue','sqe'],'''
Host 必須將每筆 completion 配對到原來的命令，才能交付正確結果。CID 只要求在同一條 SQ 的未完成命令之間保持唯一；不同 SQ 可以同時使用相同 CID。 || Deliver completion to the correct request. CID uniqueness is required among outstanding commands of the same SQ.
Host 追蹤命令時，必須一起考慮 controller、SQ 的這次建立與使用期間、SQID 及 CID。controller 與 queue 的使用期間是 Host 自己維護的上下文，並不是 CQE 裡額外增加的欄位。 || Matching includes controller, SQ lifetime, SQID and CID. Controller/lifetime are host context, not additional CQE fields.
Host 使用建立 queue 時記錄的 SQ 與 CQ 對應關係，以及未完成命令的追蹤表，來尋找原命令。Identify 不會回報每筆未完成命令的位置。 || Use the creation-time SQ-to-CQ map and outstanding table, not Identify for per-command locations.
CQE.SQID 指出命令來自哪條 SQ，CID 則指出該 SQ 內的哪筆命令。SQHD 回報 controller 已消費到的 SQ 位置，不代表這筆完成命令原先所在的 SQ 位置。 || SQID identifies the SQ and CID its command. SQHD reports consumption progress, not the original slot of that command.
Host 先確認 CQE 的 Phase 有效，再用 SQID 與 CID 找到原命令，處理 Status 及回傳資料，並更新該 SQ 的 Head 紀錄。這些工作完成後，才釋放 CQ 中的這個位置。 || Validate phase first, match SQID/CID, process status/data, update that SQ's head information, then release the CQ slot.
例如 SQ1 的 CID9 與 SQ2 的 CID9 可以共用同一條 CQ。即使兩筆命令以相反順序完成，Host 仍可透過 SQID 與 CID 分別找到正確的原命令。 || SQ1/CID9 and SQ2/CID9 are matched correctly even if they complete in reverse order.
同一條 SQ 中，未完成命令的 CID 重複時，可能回報 Command ID Conflict（0/03h）。controller 為了偵測衝突，會搜尋多少筆既有命令，由實作決定；這不免除 Host 維持 CID 唯一性的責任。 || Reusing an outstanding CID in one SQ may return Command ID Conflict (0/03h). The conflict-search extent is implementation-specific; host uniqueness obligations remain.
先確認 CQE 指出的 SQID 確實關聯到這條 CQ，再確認 CID 屬於目前這次建立的 SQ，而不是前一次 queue 留下的追蹤資料。 || Check that SQID is associated with this CQ and CID belongs to its current queue lifetime.
先檢查 Host 是否誤把「CQID+CID」當成唯一識別方式。多條 SQ 共用 CQ 時，相同 CID 仍可能代表不同命令。 || First check for an incorrect CQID+CID matching key.
''')
