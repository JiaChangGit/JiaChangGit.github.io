from scripts.nvme_qa_model import add

add(22,'Host 應在什麼時候更新 SQ Tail Doorbell 與 CQ Head Doorbell？ || When should the host update SQ Tail and CQ Head doorbells?','register',['queue','pcie'],'''
把 Host 已做完的記憶體工作通知 controller：SQ Tail 提交命令，CQ Head 釋放完成位置。 || Notify the controller of completed host memory work: SQ Tail submits commands, while CQ Head releases completion slots.
每條 SQ／CQ 各有自己的 Doorbell；更新其中一條不會自動更新另一條。 || Each SQ/CQ has its own doorbell; updating one does not update another.
確認 queue 有效、controller ready、剩餘 slots 足夠，並依 CAP.DSTRD 找到正確 Register。 || Verify a valid queue, a ready controller, sufficient free slots and the register address derived from CAP.DSTRD.
SQ Tail 指向下一個可放 SQE 的 slot；CQ Head 指向下一個待消費 CQE。寫入的是新指標值，不是增加多少筆。 || SQ Tail points to the next insertion slot; CQ Head points to the next completion to consume. Writes contain new pointer values, not increments.
先寫完整 SQE 並完成平台要求的記憶體可見性，再更新 Tail；讀取並處理有效 CQE 後再更新 Head，可一次提交或確認多筆。 || Make complete SQEs visible using the platform's memory-ordering requirements before updating Tail. Consume valid CQEs before updating Head; batching is allowed.
controller 得知哪些命令可讀，以及哪些 CQ slots 可重用。CQ Head 前進不代表提交了新 I/O。 || The controller learns which commands can be fetched and which CQ slots can be reused. Advancing CQ Head does not submit new I/O.
未消費 CQE 就提前釋放位置，可能使資料被覆寫；未準備好 SQE 就提交，違反正確使用順序，不能期待一個固定錯誤 CQE。 || Releasing unconsumed CQEs risks overwrite. Submitting incomplete SQEs violates usage ordering and has no guaranteed single error CQE.
把 Host 記憶體寫入、Tail 更新、CQE Phase 改變與 Head 更新排成時間線，四個動作各有不同用途。 || Build a timeline of SQE writes, Tail updates, CQE phase changes and Head updates; they have distinct roles.
先檢查是否把 Doorbell 值寫成「本次筆數」，而不是 modulo queue size 的新索引。 || First check whether the host wrote a count instead of the new index modulo queue size.
''')

add(23,'Doorbell 值重複、倒退、超過 Queue 範圍或寫到錯誤 QID 時，可能造成什麼問題？ || What happens with repeated, apparently backward, out-of-range or wrong-QID doorbells?','register',['queue','pcie','aer'],'''
判斷指標移動是否合法，避免把環狀索引當成只會遞增的計數器。 || Validate pointer movement without treating a ring index as a monotonically increasing counter.
錯誤影響該 queue；若 CQ 共享，還會牽動使用它的 SQ。寫到不存在 queue 與有效 queue 的非法值要分開。 || Errors affect the target queue and possibly SQs sharing its CQ. Access to a nonexistent queue differs from an invalid value on an existing queue.
需要 queue size、前次指標、可用／已消費 slots 與 QID 映射；只有新值不夠判斷。 || Need size, previous pointer, available/consumed slots and QID mapping. The new value alone is insufficient.
新值應在 0 到 size−1；同值沒有宣布新的 slots。較小值可能是合法 wrap，而非真正「倒退」。 || New values lie in 0..size−1. A repeated value announces no new slots; a numerically smaller value may be a valid wrap.
例：size=8，Tail 6→1 代表前進 3 slots，前提是有三個可用位置及有效 SQE。6→6 不能用來表示提交一整圈。 || For size=8, Tail 6→1 advances three slots, provided three are free and populated. A 6→6 write cannot announce a full ring of new commands.
合法移動讓 controller 辨識正確數量；Host 不應讀 Doorbell 回值驗證，讀回值是 vendor specific。 || A valid movement communicates the correct count. Doorbell readback is vendor-specific and is not a verification method.
有效 queue 上非法值有 Invalid Doorbell Write Value 的非同步錯誤處理；寫不存在 queue 的 Doorbell 結果 undefined。不要把事件資訊碼當成該 MMIO write 的 CQE Status。 || Invalid values on an existing queue have Invalid Doorbell Write Value asynchronous handling; writing a nonexistent queue doorbell is undefined. Event information is not a CQE status for the MMIO write.
核對原指標、環大小與空間，而非只比新舊數字大小。錯誤事件與受影響 queue 的停止取新命令也應一起確認。 || Compare old pointer, ring size and available space, not just numeric ordering. Correlate the error event with affected-queue command consumption.
先算 (new−old+size) modulo size，並核對這個前進量是否真的合法。 || First calculate (new−old+size) modulo size and verify that the resulting advance is legal.
''',{9:'Base §3.3.1.2 規定：非法 Doorbell 值且有 outstanding Asynchronous Event Request 時，張貼對應錯誤事件。受影響 SQ 可完成已取得命令，但不再取得新命令；Host 刪除並重建 queue。 || Base §3.3.1.2 specifies an error event for an invalid doorbell value with an outstanding Asynchronous Event Request. An affected SQ may complete consumed commands but consumes no new ones; the host deletes and recreates the queue.',10:'此錯誤事件屬 Error 類型，應依其指定的 Log 查補充資料；MMIO 寫入本身沒有 More 位元。不要把錯誤 QID 的 undefined 情況強行規定成一定有 Log。 || Follow the Error event’s indicated log for additional information; the MMIO write itself has no More bit. Do not invent mandatory logging for undefined nonexistent-QID accesses.'})

add(24,'Host 如何根據 CAP.DSTRD 計算每個 SQ 與 CQ Doorbell 的位置？ || How are SQ/CQ doorbell addresses calculated from CAP.DSTRD?','register',['cap','pcie','pciconfig'],'''
從 NVMe Register base 與 QID 找到唯一的 Doorbell 位址，避免通知錯 queue。 || Derive the unique doorbell address from the NVMe register base and QID.
計算以此 controller 的 MMIO base 為起點；不是相對某條 queue 的記憶體 base。 || Offsets are relative to the controller's MMIO base, not a queue's memory address.
PCI BAR0／BAR1 提供 NVMe Register 空間位置，CAP.DSTRD 提供相鄰 Doorbell stride。 || PCI BAR0/BAR1 locate the NVMe register space; CAP.DSTRD provides adjacent-doorbell stride.
stride=4×2^DSTRD；SQy offset=1000h+2y×stride；CQy offset=1000h+(2y+1)×stride。每個 Doorbell 本身仍是 32 bits。 || stride=4×2^DSTRD; SQy offset=1000h+2y×stride; CQy offset=1000h+(2y+1)×stride. Each doorbell itself remains 32 bits.
先取得映射 base，算 stride，再依 QID 選 SQ 或 CQ 公式，最後做合法寬度的 MMIO 存取。 || Obtain the mapped base, calculate stride, select the SQ/CQ expression for QID, then access with a legal MMIO width.
例：DSTRD=2、QID=3，SQ offset=1060h、CQ offset=1070h。把各 offset 加到 controller base，才是完整位址。 || DSTRD=2 and QID=3 give SQ offset 1060h and CQ offset 1070h. Add the controller base for full addresses.
位址計算本身沒有 Status。錯位址可能指到別的有效 queue，甚至造成 undefined access，不能期待 controller 自動知道 Host 原本想寫哪條。 || Address calculation has no status. A wrong address can select another valid queue or an undefined location; the controller cannot infer host intent.
將計算結果與建立時 QID、映射 BAR 範圍核對。DSTRD 不是 bytes，也不是直接乘在 QID 上的係數。 || Match results against created QIDs and the mapped BAR range. DSTRD is an exponent, not a byte count or a direct QID multiplier.
先確認公式是否漏掉 SQ／CQ 交錯所需的 2y 與 2y+1。 || First check the alternating 2y and 2y+1 indices.
''')

add(25,'Host 能否存取未建立、已刪除或 Controller 未 Enable 時的 Queue Doorbell？ || May the host access doorbells of uncreated/deleted queues or a disabled controller?','register',['pcie','queue','qattr','delete'],'''
保護 queue 的有效使用期間：有 Register 位址不代表那條 queue 目前存在。 || Respect queue lifetime: an address in the doorbell region does not mean a queue currently exists.
每條 queue 必須在建立成功後使用，刪除成功或 controller reset 後停止沿用。 || Use each queue after successful creation and retire it after successful deletion or controller reset.
檢查 Host 的 queue 存在紀錄、CC.EN、CSTS.RDY；不能從 Doorbell 讀回值判斷 queue 是否存在。 || Check host queue-lifetime records, CC.EN and CSTS.RDY; doorbell readback cannot establish queue existence.
SQyTDBL 與 CQyHDBL 只通知有效 queue 的新指標；Admin Q0 的有效環境來自 AQA／ASQ／ACQ 及初始化。 || SQyTDBL/CQyHDBL announce pointers for valid queues. Admin Q0's environment comes from AQA/ASQ/ACQ and initialization.
建立並確認成功→使用→停止提交→Delete 成功→停止使用。Controller Reset 之後即使 QID 相同也重新經過建立。 || Create successfully, use, stop submissions, successfully delete, then stop all use. Reused QIDs after reset still require reconstruction.
成功的生命周期管理不應對不存在 queue 寫 Doorbell；Doorbell 不會幫 Host 自動建立 queue。 || Correct lifetime management avoids nonexistent-queue writes. A doorbell does not automatically create a queue.
PCIe §3.1.2 將不存在 SQ／CQ 的 Doorbell 寫入列為 undefined；RDY=0 不符合命令提交前提。不能要求一定回 Invalid Queue Identifier 或某個 AER。 || PCIe §3.1.2 defines writes to nonexistent SQ/CQ doorbells as undefined. RDY=0 violates submission prerequisites. No guaranteed Invalid Queue Identifier or AER follows.
用 Create／Delete completion 的時間建立有效區間，再檢查 Doorbell 是否落在區間內。 || Use Create/Delete completion times to establish the valid interval and check doorbell timestamps against it.
先檢查是否有其他 CPU 還持有已刪 queue 的舊引用。 || First check whether another CPU still holds a stale reference to the deleted queue.
''')

add(26,'SQ Tail 與 CQ Head 發生 Wrap-around 時，Host 與 Controller 應如何處理？ || How should SQ Tail and CQ Head wrap around?','register',['queue','pcie'],'''
將固定大小記憶體重複作為環狀 queue 使用，不需要每走一圈重新建立。 || Reuse fixed storage as a ring without recreating the queue each turn.
SQ Tail 由 Host 前進，CQ Head 也由 Host 前進；相對的 SQ Head、CQ Tail 是 controller 維護。 || The host advances SQ Tail and CQ Head; the controller maintains SQ Head and CQ Tail.
使用實際 queue slots 數 N，也就是 QSIZE+1；不是拿 CAP.MQES 當每條 queue 的實際大小。 || Use the actual N=QSIZE+1 slots, not CAP.MQES as every queue's size.
每前進一步計算 (index+1) modulo N。Tail 是下一個寫入位置，Head 是下一個讀取位置，兩者相等表示空。 || Advance with (index+1) modulo N. Tail is the next insertion position, Head the next consumption position; equality means empty.
從 N−1 前進到 0，保留實際前進筆數；SQ 不超過可用容量，CQ 不跳過尚未處理的 entry。 || Wrap N−1 to zero while tracking the real count. Do not overfill the SQ or release unconsumed CQ entries.
例：N=8，CQ Head 7→2 表示消費 slots 7、0、1 共 3 筆，不是倒退 5 筆。 || With N=8, CQ Head 7→2 consumes slots 7, 0 and 1: three entries, not a backward movement of five.
合法 wrap 不是錯誤；錯把 size 當最大索引而寫 N，才是超出 queue 範圍。非法指標的處理與第 23 題相同。 || Valid wrap is not an error. Writing N as an index is out of range; invalid-pointer handling follows Question 23.
同時驗 Head／Tail 與 queue size 的 modulo 關係；只看 Doorbell 值下降不能判定違規。 || Validate modulo relationships among Head, Tail and size. A decreasing doorbell value alone is not a violation.
先查環大小用的是 slots N 還是編碼值 QSIZE；少加 1 會每圈錯一格。 || First check whether the ring uses N slots or encoded QSIZE. Omitting +1 creates an error every wrap.
''')

add(27,'CQ Wrap-around 後 Phase Tag 如何變化？Host 如何利用 Phase Tag 辨識新 Completion？ || How does the CQ phase change across wrap, and how does the host identify a new completion?','queue',['cqe','queue','reset'],'''
讓 Host 在重用同一個 CQ slot 時，辨識新寫入的完成與上一圈殘留資料。 || Let the host distinguish a newly posted completion from data left in the same slot by a previous pass.
Phase 是 CQ 的環狀生命週期資訊，不是某個 CID 的成功／失敗，也不是 SQ 的指標。 || Phase belongs to the CQ ring lifetime; it is neither CID success/failure nor an SQ pointer.
這是 PCIe CQE 的基本機制，不需要額外 Feature。建立前 Host 把各 slot Phase 初始化為 0，初次期待 1。 || This is a basic PCIe CQE mechanism, not an optional feature. Initialize every slot's phase to zero before creation and initially expect one.
CQE DW3 bit16 為 P；controller 每次在同一 slot 放入新 CQE 時反轉該 slot 的前次 Phase。 || CQE DW3 bit16 is P. Each new posting in a slot inverts that slot's previous phase.
Host 只讀當前 Head，P 符合期待值才處理；Head 跨 N−1→0 時反轉自己的期待 Phase，再檢查下一圈。 || Inspect the current Head; consume only when P matches the expected phase. Flip the expected phase when Head wraps N−1→0.
第一圈的新 CQE 為 P=1，下一圈為 P=0。不是每相鄰一筆 completion 就 1、0、1、0 交替。 || Newly posted entries use P=1 on the first pass and P=0 on the next. Adjacent completions do not alternate 1,0,1,0 within one pass.
Phase 不符表示該位置還沒有本圈新完成，並非錯誤 Status；不能接著解讀殘留 CID／SC 作為新命令結果。 || A phase mismatch means no new completion at that position, not an error status. Do not decode stale CID/SC as a new result.
測試至少跨一圈，核對 CQ Head、期待 P 與實際 P；重建 queue 後重新初始化，不能繼承前次期待值。 || Exercise at least one wrap and compare Head, expected P and actual P. Reinitialize after queue recreation rather than inheriting the old phase.
先查 Host 是否每一筆都反轉期待 P，或重設後忘記清 CQ。 || First check for toggling the expected phase after every entry or failing to initialize CQ after reset.
''')

add(28,'CQ Full 通常如何形成？CQ Full 時 Controller 能否繼續處理相關 SQ？ || How does CQ Full arise, and may related SQ processing continue?','queue',['queue','order'],'''
用 flow control 防止尚未消費的完成被覆寫。CQ 滿通常表示完成產生速度超過 Host 釋放速度。 || Flow control prevents overwriting unconsumed completions. Fullness usually means completions arrive faster than the host releases slots.
影響該 CQ 與其關聯 SQ；其他不使用此 CQ 的 SQ 必須繼續處理。 || It affects the CQ and associated SQs. Processing must continue for SQs not associated with that full CQ.
看實際 CQ size、Host CQ Head 更新與待處理完成，不以 Number of Queues 推斷容量。 || Inspect actual CQ size, Head updates and pending completions, not Number of Queues.
Full 條件是 (Tail+1) modulo N = Head，保留一格；Tail 是 controller 內部狀態，Host 不直接讀它。 || Full means (Tail+1) modulo N = Head, leaving one slot unused. Tail is controller-internal, not directly readable by the host.
Host 逐筆驗 Phase、處理結果，再更新 Head。controller 在可用 slot 出現前不得張貼新完成到此 CQ。 || The host validates phases, processes results and advances Head. The controller shall not post another completion to this CQ until a slot is available.
controller 可停止處理相關 SQ 的新增 entry；規範是 may，不能推論所有已取得命令必須瞬間停止或全部繼續。 || The controller may stop processing further associated SQ entries. This does not require all consumed commands either to stop instantly or to continue unconditionally.
CQ Full 是容量狀態，不是要求回報的 NVMe 錯誤码。為騰空間覆寫未確認 CQE 才破壞正確性。 || CQ Full is a capacity state, not a required error status. Overwriting unacknowledged entries to make room violates correctness.
若只有共享此 CQ 的 SQ 停滯，先驗 Host 消費；若獨立 CQ 的 SQ 也被此狀態停止，需檢查是否符合繼續處理要求。 || If only its associated SQs stall, inspect consumption first. If independent SQs stop because of this full CQ, check the requirement to continue their processing.
先看 Host 是否讀了 CQE 卻忘記更新 CQ Head Doorbell；讀取本身不會釋放 controller 看見的空間。 || First check for reading CQEs without updating CQ Head. Reading alone does not release space as seen by the controller.
''')

add(29,'Host 釋放 CQ 空間後，Controller 應如何恢復 Command 處理？ || How does processing resume when the host releases CQ space?','queue',['queue','pcie','order'],'''
讓被 CQ 容量限制的正常工作繼續，而不是把 CQ Full 當成需要重新 Create 的錯誤。 || Resume work after capacity becomes available rather than treating ordinary CQ Full as a recreation error.
釋放的是此 CQ 的 slots，供關聯 SQ 的命令完成使用；不改變 queue 配額或 namespace 能力。 || Released slots serve completions from associated SQs; queue allocations and namespace capabilities do not change.
確認 queue 仍存在且没有其他停止原因，例如正在 reset、CFS 或 Processing Paused。 || Verify a live queue and no independent stop condition such as reset, CFS or Processing Paused.
Host 寫 CQ Head 新索引；controller 依 Head 推進取得可再用 slots，後續完成仍使用正確 Phase。 || The host writes the new CQ Head, allowing the controller to reuse released slots with correct phases for subsequent completions.
消費 CQE→更新 Head→controller 得到空間→張貼等待完成並繼續受影響工作的處理。排程仍受正常仲裁與其他條件約束。 || Consume CQEs, update Head, allow slots to become available, then post waiting completions and continue affected work under normal scheduling and other constraints.
已釋放的 slots 可以重用，不必重建 queue；規範沒有給所有裝置一個固定的「Head 更新到下一 CQE」延遲。 || Released slots are reusable without recreation. There is no universal fixed latency from a Head update to the next CQE.
正確釋放沒有特殊成功 CQE；Head 非法仍是 Doorbell 使用問題，而不是 Create Queue 的錯誤。 || Correct release has no special success CQE. An invalid Head remains a doorbell-usage issue, not a Create Queue error.
檢查新的 CQE 是否占用合法可用 slot，並比較相關與獨立 SQ 的進度。 || Verify legal reuse of released slots and compare progress on associated and independent SQs.
先確認 Head 寫到對的 CQ Register；錯 QID 會讓 Host 以為已釋放，實際滿的 CQ 卻沒有變。 || First verify the correct CQ doorbell address; updating another QID does not release this full CQ.
''')

add(30,'多個 SQ 共用一個 CQ 時，Host 如何依 SQID 與 CID 辨識 Completion 來源？ || How does the host identify completions from SQs sharing a CQ?','queue',['cqe','queue','sqe'],'''
把每個完成交給正確原始要求；CID 只在同一 SQ 的 outstanding 命令中要求唯一。 || Deliver completion to the correct request. CID uniqueness is required among outstanding commands of the same SQ.
辨識鍵包含 controller、SQ lifetime、SQID 與 CID；controller／lifetime 是 Host 追蹤上下文，不是新增 CQE 欄位。 || Matching includes controller, SQ lifetime, SQID and CID. Controller/lifetime are host context, not additional CQE fields.
使用建立時的 SQ→CQ 映射與 outstanding 表，不靠 Identify 回傳每筆命令位置。 || Use the creation-time SQ-to-CQ map and outstanding table, not Identify for per-command locations.
CQE.SQID 指來源 SQ，CID 指該 SQ 內命令；SQHD 只報已消費 SQ 位置，不是該命令最初所在 slot。 || SQID identifies the SQ and CID its command. SQHD reports consumption progress, not the original slot of that command.
先驗 CQE Phase，再讀 SQID／CID，定位原要求、處理 Status 和資料、更新該 SQ 的 Head 資訊，最後釋放 CQ slot。 || Validate phase first, match SQID/CID, process status/data, update that SQ's head information, then release the CQ slot.
SQ1/CID9 和 SQ2/CID9 的完成能獨立正確配對，即使它們反序完成。 || SQ1/CID9 and SQ2/CID9 are matched correctly even if they complete in reverse order.
同 SQ 的 CID 重複可能回 Command ID Conflict（0/03h）；實作搜尋多少既有命令以偵測衝突是 implementation specific，Host 仍有唯一性義務。 || Reusing an outstanding CID in one SQ may return Command ID Conflict (0/03h). The conflict-search extent is implementation-specific; host uniqueness obligations remain.
核對 CQE 的 SQID 是否確實關聯這個 CQ，以及該 CID 是否屬於當前 queue 生命週期。 || Check that SQID is associated with this CQ and CID belongs to its current queue lifetime.
先檢查完成表是否錯用「CQID+CID」當唯一鍵。 || First check for an incorrect CQID+CID matching key.
''')
