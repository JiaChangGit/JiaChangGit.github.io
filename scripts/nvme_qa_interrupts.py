"""Q286–296: CQ routing, aggregation and actual interrupt masking."""
from scripts.nvme_qa_extension import question
from scripts.nvme_qa_model import COMMON, REFS, pair
REFS['interruptfull']='P|3.5–3.5.2 (interrupt delivery and masks), 3.8.4|13-16,24-26|9, 42–48'
REFS['interruptmask']='B|3.1.4 (INTMS, INTMC)|85|39–40'
REFS['interruptfeature']='B|5.2.30.2.1–5.2.30.2.2|540-541|543–544'
COMMON['interrupt_op']={**COMMON['command'],**COMMON['feature'],
 9:pair("""Completion 中斷與 Asynchronous Event Request 是不同機制。AER 本身完成時也會產生 CQE，但不能把一般 I/O interrupt 當成新的 NVMe 非同步事件。 || Completion interrupts and Asynchronous Event Requests are different mechanisms; an AER completion also uses a CQE, but an ordinary I/O interrupt is not an NVMe asynchronous event."""),
 10:pair("""合法中斷設定與傳送本身不要求新增 Error Information。設定命令若失敗，才依錯誤條件比對；CQE 已寫入而 Host 沒處理，也不自動構成 controller 的 Error Log entry。 || Normal configuration/delivery does not require an error entry. Failed commands follow error rules; an unconsumed CQE does not automatically create a controller error entry."""),
 11:pair("""中斷不逐次記入 PEL。Feature 設定是否記錄仍須符合該 FID 的 Set Feature Event 支援與成功變更條件，不能用 PEL 計算中斷總數。 || Interrupts are not individually recorded in PEL. Feature changes follow FID-specific event rules, so PEL is not an interrupt counter."""),
 12:pair("""CLR 後原 I/O queues 失效，CQ 與 vector 關係需隨 queue 重建。FID08h 的 reset 值為0，FID09h 預設不停用合併；PCIe mask 與中斷模式則須依實際 reset 來源核對，不能將 CC.EN 與 FLR 混用。 || CLR invalidates I/O queues and their vector associations. FID08h resets to zero and FID09h defaults to coalescing allowed; PCIe masks/modes require reset-source-specific treatment."""),
 13:pair("""Subsystem Reset 後重新建立受影響 controller 的 queue、vector 關聯與需要的設定。不能只因同一個 vector 編號還存在，就沿用舊 CQ 的處理資料。 || Rebuild affected queues, vector associations and settings after subsystem reset; a reused vector number does not preserve the old CQ lifetime."""),
 14:pair("""Power Cycle 後重新配置中斷模式與 queues，再讀回或設定所需 Feature。切換中斷模式時，規範也不要求保留原 coalescing 設定，建議重新設定。 || Configure interrupt mode, queues and features after power cycle; mode changes also need not retain coalescing and reconfiguration is recommended."""),
 15:pair("""同一 vector 可服務多條 CQ，遮蔽或變更該 vector 的合併設定會影響這些 CQ 的通知。不同 controller 的相同 vector 數值不代表同一份 NVMe 設定。 || A shared vector’s mask/coalescing affects notifications for all associated CQs; equal vector numbers on different controllers do not identify one NVMe setting.""")}
def q(n,t,b,o=None):question(n,t,'interrupt_op',['interruptfull','interruptmask','interruptfeature','create','delete','cqe','feature','setfeat'],b,o)

q(286,"CQ 如何指定 Interrupt Vector？ || How does a CQ select an interrupt vector?",'''
CQ 決定完成結果放在哪裡，IV 決定透過哪個中斷通知 Host，兩個編號不必相同。 || CQ identity selects completion storage, while IV selects notification; the numbers need not match.
關聯建立在 I/O CQ 上，SQ 透過 CQID 間接使用該通知路徑。 || I/O CQs own vector associations; SQs use them through CQID.
先確認 PCIe 中斷模式及已配置的 vector 數，再建立 CQ。 || Establish interrupt mode and allocated vectors before CQ creation.
Create CQ.CDW11 的 IV[31:16] 選 vector，IEN[1] 啟用該 CQ 中斷；PC[0] 控制記憶體配置。 || IV selects the vector, IEN enables CQ interrupts and PC selects memory contiguity.
配置中斷資源、建立 CQ、建立關聯 SQ，之後才送 I/O 驗證通知。 || Allocate vectors, create CQ and SQ, then verify with I/O.
例如 CQ5 使用 IV2；來自 SQ7 的完成寫入 CQ5，Host 收 IV2 後查 CQ5，再由 CQE.SQID／CID 找命令。 || CQ5 can use IV2; an SQ7 completion goes to CQ5 and is identified by SQID/CID after IV2 notification.
Create CQ 指定不合法 vector 時對應 Invalid Interrupt Vector（SCT1、SC08h）；不能以 QID 是否有效代替 IV 檢查。 || Invalid vector selection maps to 1/08h, independently of QID validity.
核對 CQ 建立成功、IV、IEN 與 Host 處理程序的 CQ 清單。 || Correlate successful creation, IV/IEN and the host handler’s CQ list.
先確認 Host 收到該 vector 後，實際輪詢的是哪條 CQ。 || First identify which CQ the host checks for that vector.
''')
q(287,"多條 CQ 共用 Vector 與獨立 Vector 有何不同？ || How do shared and dedicated CQ vectors differ?",'''
共用 vector 節省中斷資源，但 Host 收到通知後可能需要查多條 CQ；獨立 vector 較容易分散處理。 || Sharing saves vectors but requires scanning more CQs; dedicated vectors simplify distribution.
合併門檻以 vector 為單位，同 vector 的多條 CQ 可能共同參與通知判斷。 || Aggregation thresholds apply per vector and may cover several CQs.
查目前模式的 vector 能力與已建立 CQ 的 IV／IEN。 || Inspect available vectors and CQ IV/IEN associations.
CQE 仍以 SQID、CID 識別命令，中斷訊息不攜帶每筆命令的完整身分。 || CQEs retain command identity; the interrupt does not enumerate completed commands.
建立 vector→CQ 清單，收到通知後檢查相關 CQ，處理有效 Phase 的 entries，再更新各自 Head Doorbell。 || Maintain vector-to-CQ membership, consume valid entries and acknowledge each CQ.
兩條 CQ 共用 IV3 時，一次中斷可引導 Host 處理兩邊多筆完成；不能期待每條 CQ 各一個通知。 || One IV3 interrupt can cover multiple completions in two CQs.
沒有一個通用「中斷數必須等於 CQE 數」規則；共用加上合併會讓兩者自然不同。 || Interrupt and CQE counts need not match under sharing and aggregation.
比較延遲與公平性時，分別統計每條 CQ 的寫入及 Host 處理時間，避免只看共用 vector 次數。 || Measure per-CQ posting and consumption, not only shared-vector counts.
先檢查共用關係是否完整，尤其有沒有漏查其中一條 CQ。 || First check whether the handler misses a CQ sharing the vector.
''')
q(288,"Interrupt Coalescing 的 Threshold 與 Time 如何作用？ || How do coalescing threshold and time work?",'''
合併多筆完成通知可減少 Host 中斷開銷，但可能增加通知延遲；CQE 本身仍可先寫入。 || Aggregation reduces host overhead at possible notification-latency cost without requiring delayed CQE posting.
FID08h 僅適用 I/O queues，不適用 Admin CQ。 || FID08h applies to I/O queues, not Admin CQ.
Get／Set FID08h 取得或設定 TIME 與 THR；再查各 vector 的 FID09h.CD。 || Read/configure TIME/THR and check each vector’s coalescing-disable bit.
TIME[15:8] 單位100µs；THR[7:0] 是 zero-based 建議最小完成數。 || TIME is in100 µs units and THR is a zero-based recommended completion count.
先確保兩欄非零且 CD=0，再以固定 workload 比較通知與 CQE 時間。 || Establish nonzero settings and CD0 before comparing notification timing under a fixed workload.
TIME=5、THR=7 表示500µs與8筆完成的建議值；不是 controller 必須恰好等滿兩者才發通知。 || TIME5/THR7 recommends500 µs and 8 completions, not waiting for both exact values.
PCIe 規範允許實作選擇合併算法，甚至不實作合併；不能因提早或稍晚於建議值就單獨判違規。 || PCIe permits implementation-specific aggregation, including none; deviation from recommended timing alone is not a violation.
Host 更新 CQ Head 可讓計時或門檻重新開始；持續處理某 vector 的 workload 可能持續延後新通知。 || CQ-head updates may restart aggregation and ongoing servicing can continually postpone another notification.
先確認測到的是 CQE 寫入延遲，還是中斷通知延遲。 || First distinguish completion posting from interrupt delay.
''')
q(289,"如何停用 Interrupt Coalescing？ || How is interrupt coalescing disabled?",'''
停用合併讓通知不再套用聚合延遲，並不是關閉中斷。 || Disabling aggregation removes coalescing, not interrupts.
FID08h 影響 controller 的 I/O 中斷設定；FID09h.CD 可只停用指定 vector 的合併。 || FID08h controls I/O aggregation globally, while FID09h.CD disables it per vector.
讀 FID08h、FID09h 及 CQ.IEN，確認目前設定與通知路徑。 || Read aggregation settings, vector overrides and CQ interrupt enable.
TIME=0 或 THR=0 任一成立就隱含停用合併；CD=1 則禁止對該 vector 套用合併設定。 || Either zero TIME or zero THR implicitly disables aggregation; CD1 prevents aggregation on that vector.
需要全部停用時設定 FID08h；只停一條 vector 時，先有關聯 I/O CQ，再設定 FID09h。 || Use FID08h globally, or associate an I/O CQ before setting a per-vector override.
設定後 Get 讀回正確；有可通知的完成時，依模式與 mask 判斷中斷，而非仍等待原聚合門檻。 || Verify readback and apply delivery/mask rules rather than the previous aggregation threshold.
即使 THR=0 的一般數量編碼看似1，這裡仍有明確的停用規則，不能忽略。 || THR0 has an explicit disable meaning despite ordinary zero-based count interpretation.
關閉合併不保證每筆 CQE 都對應一次獨立中斷；共用 vector 與 Host 處理中的行為仍存在。 || No aggregation does not require one separate interrupt per CQE.
先檢查是不是把 CD=1 誤當成 vector 被遮蔽。 || First check whether CD1 was mistaken for masking.
''')
q(290,"FID09h 是遮蔽中斷嗎？真正的 Mask 要如何設定？ || Does FID09h mask interrupts, and where are actual masks configured?",'''
原題把 Interrupt Vector Configuration 當成 mask；實際上 FID09h 的 CD 只控制該 vector 是否使用合併。 || The original premise confuses FID09h coalescing control with interrupt masking.
Mask 阻止中斷送出，影響所有使用該 vector 的 CQ 通知。 || A mask blocks delivery for all CQs sharing that vector.
先確認目前是 pin-based、MSI 還是 MSI-X，才能選正確的 mask 介面。 || Select the masking interface after establishing the active interrupt mode.
Pin／MSI 用 INTMS 寫1設 mask、INTMC 寫1清 mask；MSI-X 用 Function Mask 與 Table 的 Vector Mask。 || INTMS write-one sets and INTMC write-one clears pin/MSI masks; MSI-X uses function and table-vector masks.
先保留原設定，再遮蔽、處理 CQ、更新 Head，最後解除遮蔽並檢查是否仍有待處理完成。 || Preserve state, mask, service/acknowledge CQs, unmask and check remaining work.
INTMC 對目標bit寫1才解除，寫0沒有作用；這和一般「寫0就是清除」的 Register 不同。 || INTMC requires writing one to clear a mask; zero has no effect.
MSI-X 模式下 Host 不得存取 INTMS／INTMC，若違反，其結果未定義，不能編造必定的 NVMe Status。 || INTMS/INTMC access is prohibited and undefined under MSI-X, not a guaranteed NVMe status.
Get FID09h.CD 只能證明合併設定，不能證明 MSI-X table 已解除 mask。 || FID09h readback does not establish MSI-X mask state.
先讀目前模式及真正的 mask 位元。 || First inspect actual mode and mask bits.
''',{8:'Mask Register 讀寫沒有 NVMe CQE，DNR／More 不適用；如果同時用 Get／Set FID09h 查合併，只有那些命令才有 CQE。 || Mask register accesses have no NVMe CQE; only separate Get/Set Feature commands carry DNR/More.'})
q(291,"Vector 被遮蔽時，Controller 還能寫 CQE 嗎？ || Can completions be posted while a vector is masked?",'''
Mask 控制通知，並不暫停命令執行或凍結 CQ。 || Masking controls notification rather than command execution or CQ posting.
所有使用該 vector 的 CQ 都可能繼續累積完成，直到各自空間不足。 || Associated CQs can accumulate completions until their capacity limits intervene.
讀實際 mask、CQ.IEN、CQ 位置與 Phase；MSI-X 可另看 PBA。 || Inspect masks, IEN, CQ position/phase and applicable MSI-X pending bits.
Controller 仍依正常規則寫 CQE；MSI-X 因 mask 不能送出的中斷會以對應 pending bit 表示。 || Normal CQE posting continues; MSI-X masks cause pending-interrupt indication.
遮蔽後可用合法的 CQ 輪詢確認完成，處理後仍需更新 Head Doorbell 釋放空間。 || Poll and consume valid CQEs, then update head to release space.
看見新 Phase 的 CQE 卻沒有通知，在 mask 尚未解除時可能完全正常。 || A new valid CQE without an interrupt can be normal while masked.
CQ Full 是空間問題，與 mask 不同；長期不處理完成會間接讓 CQ 滿，但不是 mask 直接禁止寫入。 || CQ fullness is a capacity consequence of nonconsumption, not a direct masking rule.
不要用「沒有 interrupt」推導「沒有完成」；兩者需分開觀察。 || Absence of an interrupt does not establish absence of completion.
先讀 CQ 的有效 Phase，再看通知設定。 || First check valid CQ phase before notification configuration.
''')
q(292,"解除 Mask 後如何處理累積完成？ || How are accumulated completions handled after unmasking?",'''
一個 pending 中斷可以代表多筆完成，Host 仍必須從 CQ 逐筆取得真正結果。 || One pending interrupt can represent many completions whose results remain in CQs.
共享 vector 時，要處理所有關聯且可能有新完成的 CQ。 || Service all relevant CQs sharing the vector.
核對 MSI-X 的 Function／Vector Mask、PBA，或 pin／MSI 的 INTM 及對應 CQ。 || Check mode-specific masks/pending state and associated queues.
MSI-X 兩層 mask 都清除後，待送中斷才可送出；只清其中一層仍可能不通知。 || Pending MSI-X delivery requires both mask layers clear.
解除遮蔽後讀 CQ、依 Phase 處理，再更新各 Head；處理與重新掛通知間要避免漏掉剛到的新 CQE。 || Unmask, process valid CQEs and acknowledge heads while handling arrival races.
累積10筆完成可能由一次通知引導 Host 全部處理，不要求補送10次歷史中斷。 || Ten accumulated completions need not cause ten replayed interrupts.
INTM 遮蔽 MSI 時，對應 MSI Capability pending 不會因此設起；不能把 MSI-X PBA 規則原封套用。 || INTM masking suppresses MSI pending assertion; MSI-X PBA semantics cannot be copied to it.
以「所有有效 CQE 是否被處理」判斷完整性，不以通知次數等於命令數判斷。 || Judge consumption completeness, not equality of interrupt and command counts.
先檢查是否還有另一層 mask 或漏列的共用 CQ。 || First check another mask layer or omitted shared CQ.
''')
q(293,"已被 CQ 使用的 Vector 可以修改設定嗎？ || Can an in-use vector be reconfigured?",'''
需先分清修改合併、修改 mask，還是改變 CQ 的 vector 關聯，這不是同一件事。 || Distinguish coalescing changes, masking and reassignment of CQ association.
FID09h 改指定 vector 的合併設定，會影響目前共用該 vector 的所有 CQ。 || FID09h changes aggregation for the selected vector and its associated CQs.
設定 FID09h 前，該 IV 必須已關聯一條存在的 I/O CQ。 || FID09h requires prior association with an existing I/O CQ.
CD=1 停用合併，CD=0 使用全域合併；它沒有修改 Create CQ.IV 的功能。 || CD selects aggregation behavior, not reassignment of Create CQ.IV.
保留 CQ 關聯，Set FID09h 後 Get 相同 IV；若需要換 CQ 的 IV，依合法 queue 生命週期重建該關聯。 || Change/read back vector settings; recreate the queue association when a different IV is needed.
已存在 CQ 正是設定 FID09h 的前提，不是禁止修改的理由。 || An existing CQ is the feature’s prerequisite, not a prohibition on change.
IV 非法或未關聯存在的 I/O CQ 時，controller 應回 Invalid Field；這裡的 should 不等於強制唯一結果。 || Invalid/unassociated IV should produce Invalid Field, preserving the recommendation strength.
比較前後結果時，保存其他共用 CQ 與 mask 狀態，避免把外部條件變更誤算成 Feature 行為。 || Preserve shared-CQ and mask state to isolate feature effects.
先確認真正想修改的是 CD、mask，還是 CQ.IV。 || First identify which of CD, mask or CQ.IV is intended to change.
''')
q(294,"Reset 後中斷設定要如何恢復？ || How are interrupts restored after reset?",'''
Queue 與 vector 的關聯會隨 queue 生命週期結束；PCIe 模式與 mask 是否保留則依 reset 來源不同。 || Queue associations end with queue lifetime; PCIe mode/mask retention depends on the reset source.
只重設一個 controller 與更大範圍 reset 不同，不能重配未受影響的另一台 controller。 || One-controller reset differs from broader reset and does not justify reconfiguring unaffected controllers.
先查 CC／CSTS 與 PCIe interrupt mode，再讀需要的 Feature Current。 || Inspect controller state, interrupt mode and feature current values.
FID08h 的 TIME／THR reset 值0；FID09h 預設允許合併，但當全域合併停用時，不會因此自動啟用延遲。 || FID08h resets to zero; default per-vector coalescing permission does not enable a disabled global aggregation policy.
恢復 Admin 通道、配置 vectors、重建 CQ／SQ，再設定 FID09h 與需要的 FID08h。 || Recover Admin access, vectors and queues before configuring per-vector/global aggregation.
新的合法 CQE 可以經正確 vector 被 Host 找到，舊 CQE 不應混進新 queue 的完成追蹤。 || New completions are consumed through the rebuilt path without importing stale CQEs.
FID09h 在 CQ 尚未重建前就設定，可能觸發未關聯 IV 的錯誤。 || Setting FID09h before rebuilding its CQ can violate the association prerequisite.
模式切換也可能失去合併設定，需重新設定；不能只測 CC.EN reset 就推論 Power Cycle。 || Mode changes may lose aggregation settings; CC.EN testing does not establish power-cycle behavior.
先核對 reset 類型及新 CQ 建立成功的時點。 || First check reset type and successful new-CQ creation time.
''')
q(295,"Queue 刪除後如何回收中斷資源？ || How are interrupt resources reclaimed after queue deletion?",'''
刪除 CQ 結束一個完成目的地，不代表 Host 配置的 PCIe vector 自動從整個 function 消失。 || CQ deletion removes one completion destination, not the host-allocated PCIe vector itself.
同一 vector 可能仍被其他 CQ 使用，因此要按關聯計數回收。 || Other CQs may still use the vector, requiring association-aware reclamation.
保存 SQ→CQ→IV 關係與尚未完成命令，不能只列 SQ 編號。 || Preserve SQ-to-CQ-to-IV dependencies and outstanding commands.
先刪依賴的 SQ 並等待完成，再刪 CQ；成功後解除 Host 對該 CQ 的處理資料。 || Delete dependent SQs and wait, then delete CQ and retire its host handling state.
最後檢查同 IV 是否還有其他 CQ，才決定移除 handler 或釋放 Host 中斷資源。 || Release the handler/vector only after checking remaining CQ users.
CQ1、CQ2 共用 IV3，刪 CQ1 後 IV3 仍需服務 CQ2；不應把 CQ2 的通知一起關掉。 || Deleting CQ1 leaves IV3 serving CQ2 when both shared it.
CQ 仍被 SQ 引用時不能合法刪除；成功刪除前也不能提前回收 CQ 記憶體。 || Referenced CQs cannot be deleted successfully, nor their memory reclaimed early.
同時比對 queue 刪除 CQE、Host 關聯清單與剩餘 CQ 通知，避免資源洩漏或過早釋放。 || Correlate deletion completion, host membership and remaining notification paths.
先確認 vector 是獨占還是共用。 || First establish whether the vector is dedicated or shared.
''')
q(296,"如何比對 Interrupt、CQ 與實際完成行為？ || How are interrupt settings, CQ state and completions cross-checked?",'''
將命令完成與通知分開，才能定位是 controller 沒完成，還是 Host 沒被通知或沒處理。 || Separating completion from notification distinguishes execution failures from delivery/consumption failures.
追蹤一條完整路徑：SQ 的命令、關聯 CQ、使用的 vector 與 Host 處理程序。 || Follow a complete SQ-command-to-CQ-to-vector-to-handler path.
讀 CQ.IEN／IV、FID08h、FID09h、真實 mask 與 CQ Phase。 || Inspect routing, aggregation, masks and phase.
保存提交時間、CQE 出現時間、通知時間與 Head 更新時間，四者不是同一時點。 || Preserve submission, CQE posting, notification and head-update times separately.
先確認新 CQE，再查是否應通知；最後核對 Host 是否處理並釋放空間。 || Establish a valid CQE, assess notification, then verify consumption and reclamation.
完成已存在、mask=1且 Host 用輪詢處理，是可以成立的正常案例；中斷不是完成有效性的唯一證據。 || A posted CQE consumed by polling while masked can be valid normal behavior.
如果 Phase 不匹配、查錯 CQ 或漏更新 Head，先修正 Host 證據；不能只因未收到 interrupt 就判 SSD 丟命令。 || Resolve wrong phase/CQ or missing head updates before diagnosing a lost command from absent interrupts.
用同一次測試的設定快照與時間線互相比對，避免拿測試後讀值解釋測試中行為。 || Correlate settings and observations from the same test interval.
先從該命令的 CQ 位置與 Phase 查起。 || First inspect the command’s CQ position and phase.
''')
