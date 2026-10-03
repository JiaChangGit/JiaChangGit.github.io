"""Q107–117: Base 2.4 immediate/deferred Abort and host recovery."""
from scripts.nvme_qa_extension import question

def q(n,t,refs,b,o=None): question(n,t,'recovery',refs,b,o)

q(107,'Abort 如何用 SQID 與 CID 指定目標？ || How does Abort identify its target with SQID and CID?', ['abort','sqe','idctrl'], '''
Abort 請求中止一筆先前提交的命令，讓 Host 不必只為一筆逾時操作立即重設整個 controller。它是請求，不是保證目標尚未執行。 || Abort requests cancellation of a previously submitted command without necessarily resetting the controller; it does not prove the target was never executed.
目標可以位於 Admin SQ 或 I/O SQ。Abort 自己也是 Admin 命令，有自己的 CID 與完成結果。 || The target can be in the Admin SQ or an I/O SQ. Abort is itself an Admin command with its own CID and completion.
Identify.ACL 宣告可同時 outstanding 的 Abort 數量，零起算；一般命令的 queue 深度不能代替 ACL。 || Identify.ACL is the zero-based concurrent Abort limit; queue depth does not replace it.
Abort CDW10 bits31:16 是目標 CID，15:0 是目標 SQID；Abort 自己的 CDW0.CID 則用來配對 Abort 的 CQE。 || Abort CDW10 bits 31:16 select target CID and bits 15:0 target SQID; CDW0.CID identifies the Abort command itself.
從 outstanding 清單找到目標 SQID／CID，保留目標的 buffer，再以新的 Admin CID 提交 Abort；分別追蹤兩筆完成。 || Locate the target in outstanding tracking, retain its buffers, submit Abort with a distinct Admin CID and track both completions.
Abort 成功 CQE 的 DW0.IANP=0 表示立即中止已執行；IANP=1 表示未執行立即中止，仍可能稍後中止。最後也要查看目標 CQE。 || On successful Abort, DW0.IANP=0 reports immediate abort; IANP=1 reports no immediate abort but allows deferred abort. Inspect the target CQE too.
超過 ACL 時，controller 可回 Abort Command Limit Exceeded（1/03h）。目標找不到則可由成功 Abort 的 IANP=1 表示，不應固定要求 Invalid Queue Identifier。 || Excess outstanding Aborts may receive 1/03h. A missing target can be represented by successful Abort with IANP=1, not a universal Invalid Queue Identifier requirement.
模擬 SQ3／CID7 與 SQ4／CID7 同時存在時，CDW10=(7<<16)|3 只指定前者。用這個例子驗證解析是否把兩個欄位顛倒。 || If SQ3/CID7 and SQ4/CID7 coexist, CDW10=(7<<16)|3 targets only the former; this detects swapped fields.
先確認 Abort 的目標 CID 不是誤填成 Abort 自己的 CID。 || First check that target CID was not confused with the Abort command’s own CID.
''')

q(108,'Abort 已完成、不存在或指定錯誤 SQID／CID 的命令時會怎樣？ || What happens when Abort targets a completed or missing command?', ['abort','status'], '''
目標在 Host 決定中止與 controller 處理 Abort 之間可能已完成，所以「沒找到」是必須處理的正常競爭情況。 || A target may finish between the host deciding to abort and the controller processing Abort; absence is a normal race to handle.
判斷的是指定 SQID／CID 在那個時點的命令，不是 Host 曾經提交過同一編號就永遠存在。 || The target is the command at the specified IDs at that time, not every historic use of those numbers.
保留 queue 使用期間與 CID 配置紀錄，避免 Abort 延遲到 CID 已被下一筆命令重用。 || Preserve queue-lifetime and CID-allocation records so a delayed Abort is not misdirected to a later reuse.
讀 Abort 的 CQE Status 及 DW0.IANP，並檢查目標是否已留下有效 CQE。IANP=1 的原因可以是找不到目標，也可以是無法立即中止。 || Read Abort status and IANP and check for a target CQE. IANP=1 can mean absence or inability to abort immediately.
先處理已收到的目標完成，再處理 Abort 結果；如果目標仍 outstanding 且 IANP=1，繼續追蹤目標，不能擅自釋放 buffer。 || Process an already received target completion; if it remains outstanding with IANP=1, continue tracking and retain its buffers.
有效的 Abort 命令即使沒中止目標，也可回成功且 IANP=1。這表示請求處理完成，不是目標操作成功或回復。 || A valid Abort can succeed with IANP=1 without cancelling the target; this reports request processing, not target success or rollback.
不要把所有不存在的 SQID／CID 都要求成某個固定錯誤 Status。若 Abort 本身欄位另有非法值，則依該非法條件處理。 || Do not assign a universal error status to every missing SQID/CID target; separate any independent invalid encoding in Abort itself.
如果測試期待「目標已完成後 Abort 必須失敗」，應修正為核對 IANP 與既有目標結果。 || Replace a test requiring Abort failure for a completed target with checks of IANP and the existing target result.
先查目標是否其實早已完成，只是 Host 尚未消費 CQE。 || First check whether the target already completed but its CQE has not been consumed.
''')

q(109,'重複 Abort 與並行 Abort 如何套用 ACL？ || How does ACL apply to repeated and concurrent Abort commands?', ['abort','idctrl'], '''
ACL 限制同時處理的 Abort 請求數量，不是每秒可中止多少命令，也不是可被中止的 namespace 數。 || ACL limits concurrent Abort requests, not cancellations per second or namespace count.
每一筆尚未完成的 Abort 都占用其並行配額；多筆指向同一目標，也不能當成只送了一筆。 || Each outstanding Abort consumes concurrent capacity, including several targeting the same command.
Identify.ACL=0 表示支援至少 1 筆並行 Abort；ACL=3 表示 4 筆。Host 應依完成回收這份配額。 || ACL=0 permits one outstanding Abort and ACL=3 four; release host accounting on completion.
分開記錄 Abort 自己的 Admin CID、目標 SQID／CID 及結果。大量中止可考慮支援的 Cancel，或刪除並重建 I/O SQ。 || Track each Abort CID, target IDs and result separately. Bulk cancellation can use supported Cancel or I/O SQ deletion/recreation.
提交前檢查配額，達上限就等待先前 Abort 完成。重複目標時仍逐筆處理 Abort CQE，但目標命令不能因此完成兩次。 || Check capacity before submission and wait at the limit. Repeated targets still have separate Abort CQEs but only one target completion.
例如 ACL=1，兩筆 Abort outstanding 符合配額；其中一筆完成後才提交下一筆，就不會因 Host 超量造成干擾。 || With ACL=1, two outstanding Aborts fit the limit; submitting another after one completes avoids host overrun.
controller 可將超額請求完成為 Abort Command Limit Exceeded（1/03h），規範不是要求每個超額時點都必定看到此碼。 || The controller may complete excess requests with 1/03h; the specification does not mandate observing that code on every over-limit test.
測量 outstanding 數時，以提交到完成的期間計算；不要拿累計 Abort 次數與 ACL 比較。 || Count submissions not yet completed rather than cumulative Abort operations.
先確認測試是否漏掉 ACL 的零起算，或重複計入已完成的 Abort。 || First check zero-based ACL interpretation and removal of completed requests from the count.
''')

q(110,'Abort 成功是否代表目標完全沒有執行？ || Does successful Abort prove that the target never executed?', ['abort','order'], '''
不代表。Abort 能停止後續處理，卻不是交易回復機制；目標可能在中止前已傳輸部分資料或改變狀態。 || No. Abort can stop further processing but is not transaction rollback; data transfer or state changes may already have occurred.
要分別判斷 Abort 的完成、立即中止保證，以及目標在中止前已產生的效果。 || Separate Abort completion, immediate-abort guarantees and effects already produced by the target.
Base 2.4 的關鍵證據是成功 Abort 的 IANP，而不是單看 Status=Success。 || The Base2.4 evidence is IANP in a successful Abort, not success status alone.
IANP=0 時，除之後張貼目標 CQE 外，Abort CQE 張貼後不得再有目標命令造成的 Host memory 存取或媒體／管理狀態改變。 || IANP=0 prohibits subsequent target effects after the Abort CQE, including host-memory access and media/management changes, except posting the target CQE.
記錄 Abort CQE 時點及 IANP，等待並處理目標 CQE，再依命令語意確認資料結果。若需重試 Write，先處理可能已執行部分與重試的關係。 || Record Abort completion and IANP, handle target completion and assess data under command semantics before retrying a possibly partially executed write.
立即中止後，目標以 Command Abort Requested 完成。目標 CQE 可在 Abort CQE 之前，也可在滿足無後續效果條件下之後出現。 || Immediate abort yields target Command Abort Requested. The target CQE may precede or, under the no-subsequent-effects guarantee, follow the Abort CQE.
IANP=1 不保證無後續效果；如果資料傳輸已開始而未完成，且目標 CQE 尚未張貼，就不能宣稱符合立即中止條件。 || IANP=1 gives no no-subsequent-effects guarantee. An initiated but incomplete transfer without a posted target CQE precludes immediate abort.
合規測試應檢查 Abort CQE 之後是否仍有被禁止的目標效果，而不是要求整個命令從來沒有做過任何事。 || Test prohibited effects after Abort completion rather than requiring that the target never performed any work.
先確認判斷使用的是 IANP=0，還是只看到 Abort Status=Success 就過度推論。 || First check whether the conclusion is based on IANP=0 or merely Abort success.
''')

q(111,'Abort 未立即中止時，目標還能正常完成嗎？ || Can a target complete normally if Abort did not immediately cancel it?', ['abort'], '''
可以。IANP=1 表示未執行立即中止，controller 仍可稍後中止，也可能讓目標正常完成。Host 必須保留兩種可能。 || Yes. IANP=1 allows either deferred cancellation or normal target completion.
Abort 的結果與目標結果是兩個狀態。Abort 失敗或未立即中止，不會自動把目標命令標成失敗。 || Abort and target outcomes are separate; failed or non-immediate Abort does not automatically fail the target.
查看成功 Abort 的 IANP 及目標 CQE。若 Abort 自己以錯誤完成，不應把保留或未定義的 DW0 當成有效 IANP 結果。 || Inspect IANP on successful Abort and the target CQE. Do not interpret reserved/undefined DW0 from a failed Abort as a valid IANP result.
目標若延後被中止，Status 必須是 Command Abort Requested；若正常執行完成，則依目標命令回報實際結果。 || A deferred-aborted target must report Command Abort Requested; otherwise it reports its actual execution result.
IANP=1 後持續等待有效目標 CQE，同時依 Host 復原策略控制等待時間。若需要擴大到 Reset，先完成 queue 使用期間的切換與資源保護。 || After IANP=1, track the target under host recovery time limits; escalating to reset requires proper queue-lifetime and resource handling.
收到目標成功 CQE 是合法可能；收到 Command Abort Requested 也是合法可能。兩者都不需要再產生第二筆目標完成。 || Either target success or Command Abort Requested can be valid, without a second target completion.
不要將 IANP=1 解釋成「永遠不會中止」，也不要解釋成「一定晚一點中止」。 || IANP=1 means neither that cancellation will never occur nor that it definitely will occur later.
比對實際目標結果，而不是以 Abort 的完成碼推算目標的最終 Status。 || Validate the target’s actual result rather than deriving it from Abort status.
先查目標 CQE；沒有這項證據時，就先把目標結果列為尚未確認。 || First inspect the target CQE; without it, leave the outcome unresolved.
''')

q(112,'Abort 與目標完成同時到達，Host 如何避免重複處理？ || How does the host handle racing Abort and target completions?', ['abort','cqe','queue'], '''
並行完成會讓 Host 的 timeout 路徑與一般完成路徑同時碰到同一份追蹤資料。需要同步的是 Host 狀態，不是要求 controller 將所有完成排成固定順序。 || Timeout and normal completion paths can race over host tracking. Synchronize host state rather than demanding a universal completion order.
一筆 Abort 與一筆目標命令有各自的生命週期；共享目標不代表兩個 CQE 是同一個完成。 || Abort and target have separate lifetimes; their CQEs are distinct even though they refer to one target.
用 CQE.SQID＋CID、有效 Phase 與 queue 使用期間識別命令；只比 CID 不足以跨 queue 關聯。 || Identify completions by SQID+CID, phase and queue lifetime; CID alone is insufficient across queues.
追蹤資料要能表示目標未完成、已完成，以及 Abort 尚未完成／已完成。只有目標結果才能交付目標的上層完成。 || Track target and Abort completion independently; only the target result completes the target to higher software layers.
收到任一 CQE 時，以同步方式更新相應狀態。目標先完成就保存結果，之後 Abort CQE 只結束 Abort；Abort 先完成則依 IANP 與目標狀態繼續處理。 || Update the appropriate state atomically. A later Abort CQE closes Abort only; an earlier Abort CQE requires IANP and target-state handling.
每筆命令各完成一次，每份資源各回收一次。兩個不同命令的 CQE 都存在是正常，不能誤算成目標完成兩次。 || Each command completes once and resources are reclaimed once. Two CQEs for two different commands are not duplicate target completion.
不能固定要求目標 CQE 一定先於 Abort CQE；Base 2.4 在滿足立即中止的無後續效果保證時，允許任一張貼順序。 || Do not universally require target CQE first; Base2.4 permits either posting order when immediate-abort no-subsequent-effects conditions are met.
驗證同一 target SQID／CID 沒有被上層完成兩次，且新的 CID 使用期間不會吃到舊 Abort 的結果。 || Verify single upper-layer completion and prevent old Abort results from affecting a reused CID lifetime.
先查兩個 CQE 的 SQID／CID 是否其實分別屬於 Abort 與目標。 || First determine whether the two CQEs actually belong to Abort and target separately.
''')

q(113,'Timeout 後一定要依 Abort、Queue Reset、Controller Reset 的順序嗎？ || Must every timeout follow Abort, queue reset, then controller reset?', ['abort','fatal','reset','commrecovery'], '''
沒有適用於所有命令的固定三步程序。Host 要先判斷是單筆命令太慢、queue 失效，還是 controller 已無法通訊，再選擇能解決問題的範圍。 || There is no universal three-step sequence. Diagnose a slow command, failed queue or lost controller communication before selecting recovery scope.
Abort 針對命令；I/O queue 刪除／重建針對相關 queue；Controller Reset 會影響該 controller 的全部 queue 與未完成命令。 || Abort targets a command; queue deletion/recreation targets queues; controller reset affects all its queues and outstanding commands.
保存 CQ 指標、Phase、中斷設定、CSTS 與其他命令的進度。CAP.TO 不代表每條 I/O 的 timeout。 || Preserve CQ position/phase, interrupts, CSTS and other-command progress. CAP.TO is not a per-I/O timeout.
可用操作包括 Abort、Delete I/O SQ／CQ、重新建立 queue，以及 CC.EN 觸發的重設；每種操作都需要有效的前提與完成確認。 || Available actions include Abort, queue deletion/recreation and reset via CC.EN, each with its own preconditions and completion checks.
先排除 Host 漏處理 CQE；若 Admin 通道正常，可嘗試針對目標 Abort。若 queue 受損，依規範復原 queue；Admin 發生嚴重錯誤或刪 queue 無完成時，建議重設 controller。 || First exclude missed CQEs. With a working Admin path, consider Abort; recover damaged queues; serious Admin errors or uncompleted deletion call for controller reset.
復原完成應同時建立可用新通道、結束舊命令的後續存取風險，並重新確認可能持續的背景管理操作。 || Recovery establishes usable new channels, resolves old-command access risks and rechecks any continuing background operations.
Host 計時器到期不是 controller 回傳的 NVMe Status。不能為「沒收到 CQE」捏造 Timeout CQE，也不能無條件要求先送一筆注定無法完成的 Abort。 || A host timeout is not an NVMe completion status. Do not fabricate a timeout CQE or require Abort when the Admin path cannot complete it.
測試計畫要標示哪些是 Spec 要求，哪些是 Host 選定的 timeout 與升級策略。 || Mark specification requirements separately from host-selected timeouts and escalation policies.
先確認 CQ 裡是否已有完成；若只是中斷遺漏，重設會掩蓋真正問題。 || First inspect the CQ for an existing completion; resetting can conceal an interrupt-handling problem.
''')

q(114,'Abort 本身也 Timeout，Host 應如何復原？ || How should the host recover when Abort itself times out?', ['fatal','abort','reset'], '''
這時不只目標結果不明，連 Admin 通道是否可完成命令都需要確認。無限追加 Abort 會增加未完成請求，卻不能證明舊命令已停止。 || Now both target outcome and Admin-channel health are uncertain. Repeated Abort submissions do not establish that old commands stopped.
復原可能從單一命令擴大到 controller；應先通知使用這個 controller 的 queue 管理與資源回收邏輯。 || Recovery may widen to the controller, requiring coordination with all its queue and resource management.
檢查 Admin CQ 的 Phase／Head、CSTS.CFS／RDY，以及 Abort outstanding 是否超過 ACL。 || Check Admin CQ phase/head, CFS/RDY and ACL accounting.
保存 Abort 的 Admin CID、目標 IDs、提交時間及已觀察的 CQE。後續 Reset 是另一項操作，不應偽造 Abort 的完成結果。 || Preserve Abort CID, target IDs, timing and observed CQEs; a subsequent reset does not fabricate an Abort result.
先排除 Admin CQ 已有完成但 Host 漏讀。若確認嚴重 Admin 問題，依 Base 9.1／9.5 進行 Controller Reset、等待狀態，再重建操作環境。 || Exclude missed Admin CQEs; serious Admin failure calls for controller reset, state confirmation and reinitialization under Base9.1/9.5.
成功復原後，新命令可以使用新 queue；舊目標是否曾完成其資料效果，仍需依命令與持久化語意判斷。 || New commands use recovered queues; prior data effects still require command-specific persistence analysis.
沒有 Abort CQE 就沒有可解讀的 IANP、DNR 或 More。也不能將 Reset 成功當成目標 Write 從未發生的證明。 || Without an Abort CQE there is no IANP, DNR or More to decode. Successful reset does not prove a target write never happened.
以 Register 狀態、新 queue 的可用性及持續操作的 Log 交叉確認，不只用「Reset 函式回傳成功」當成全部證據。 || Correlate registers, new queue usability and background-operation logs rather than relying only on a host reset routine’s return value.
先檢查 Admin CQ 是否已滿或被 Host 停止消費。 || First check whether the Admin CQ is full or no longer being consumed.
''')

q(115,'Reset 後如何處理舊命令、舊完成與舊 Queue？ || How are old commands, completions and queues handled after reset?', ['reset','queue','cqe','commrecovery'], '''
Reset 劃分命令與 queue 的使用期間。記憶體內還看得到舊 bytes，不代表它們仍是可用的命令或完成。 || Reset separates queue lifetimes; surviving memory bytes are not evidence of valid commands or completions.
受影響 controller 的 I/O queues 與未完成追蹤要重建。媒體上的既有資料與獨立背景操作，則有各自的保留或繼續規則。 || Rebuild affected I/O queues and outstanding tracking; stored data and independent background operations follow separate rules.
查看 Reset 類型、CC／CSTS 及 Admin Queue Register 保留條件；不要把清 CC.EN 的例外套到所有 Reset 來源。 || Check reset type, CC/CSTS and Admin-register retention; CC.EN-reset exceptions do not apply to every source.
Host 重設 SQ／CQ 指標與期待 Phase，將新提交與舊追蹤隔離；背景 Sanitize 等另用對應 Log 查進度。 || Reset host queue pointers/expected phase and separate new submissions from old tracking; inspect continuing operations through their logs.
先停止新提交，完成 Reset 的等待與存取停止確認，再建立新 queue，最後恢復 I/O。需要重試時，先分析原命令是否可能已產生效果。 || Stop submissions, complete reset and access-termination checks, create new queues, then resume I/O with retry analysis of possible prior effects.
新 queue 只接受新生命週期的有效完成；Host 不再以舊 CID 清單等待已被 Reset 結束的所有 CQE。 || New queues accept completions for their new lifetime; the host does not wait for all old CQEs after reset termination.
Reset 通常不是逐筆回傳某個固定錯誤碼。AER 更明定因 Reset 中止時不得回 CQE；其他命令也不能一律要求 Command Abort Requested。 || Reset is not universal per-command completion with one error code. Reset-aborted AERs expressly have no CQE; other commands do not universally return Command Abort Requested.
同時驗證新 queue 正常，以及舊 buffer 不再被舊命令使用；僅看新命令成功，無法排除舊命令晚到的存取。 || Validate new queues and termination of old-buffer accesses; new-command success alone does not exclude late old-command activity.
先查 Host 是否重用了舊 Phase 或追蹤資料，造成把舊 CQE 當成新完成。 || First inspect reused phase or tracking state that could make stale CQEs appear new.
''')

q(116,'如何區分 Command Timeout、Ready Timeout 與長時間操作？ || How do command, ready and long-operation timeouts differ?', ['cap','crto','ready','abort','aerfull','idctrl'], '''
不同等待對象需要不同期限：命令等待 CQE，初始化等待 RDY，背景操作則可能在命令已完成後持續。混用期限會造成不必要的 Reset。 || Command completion, readiness and background-operation completion are different waits; sharing one deadline causes false timeouts.
Host 命令 timeout 是軟體政策；Ready 等待針對 controller 狀態；Sanitize 等進度則屬指定管理操作的範圍。 || Host command timeouts are software policy, readiness concerns controller state and background progress belongs to the management operation.
停用看 CAP.TO；啟用依 Ready Mode 與 CRTO／CAP 規則；個別功能若宣告預估時間或最大時間，則按其欄位定義使用。 || Disable uses CAP.TO; enable uses ready-mode and CRTO/CAP rules; interpret function estimates and maxima under their own definitions.
觀察 CQE、CSTS.RDY 及操作狀態 Log。AER 沒事件時應保持 outstanding，規範建議不套一般命令 timeout。 || Observe CQEs, RDY and operation logs. AER remains outstanding without an event and should not use an ordinary command timeout.
先寫清楚正在等待哪個狀態轉移，再從正確起點計時。例如成功啟動 Sanitize 後，改查 Sanitize Status，不繼續等第二個 Sanitize CQE。 || Name the awaited transition and timer start. After Sanitize initiation succeeds, monitor its status rather than expecting a second command CQE.
期限內達到指定狀態才是該項等待成功。命令回 Success 與媒體工作完成，可能分屬不同時間。 || The wait succeeds when its specified state is reached; command success and media-operation completion can occur separately.
沒有全 NVMe 命令共用的 CAP.TO。預估完成時間也不應自動升級成必須遵守的硬性 timeout。 || CAP.TO is not universal across commands, and an estimated duration is not automatically a mandatory deadline.
將測試報告中的每個 timeout 註明來源、單位、起算時點與是估計還是上限。 || Record source, units, starting event and whether each timeout is an estimate or limit.
先檢查把哪個等待對象套進了哪個計時器。 || First check which timer was applied to which awaited state.
''')

q(117,'Timeout 時如何定位提交、取得、執行、完成或 Host 處理階段？ || How is a timeout located along submission, execution and completion?', ['sqe','cqe','queue','pcie','irq','fatal'], '''
沿命令生命週期保存證據，可以把「沒完成」拆成可查的階段，而不急著歸咎韌體執行太慢。 || Evidence along the command lifetime localizes missing progress before blaming slow firmware execution.
分析一筆目標命令時，也要觀察其 SQ、關聯 CQ、共享向量與其他命令，因為瓶頸可能位於共用資源。 || Analyze the target together with its SQ, CQ, shared vector and neighboring commands to locate shared bottlenecks.
使用 SQE 快照、SQ Tail Doorbell、回報的 SQHD、CQ Phase／Head、中斷設定與 CSTS；這些都是 PCIe NVMe 介面層證據。 || Use SQE snapshots, tail doorbell, reported SQHD, CQ phase/head, interrupt configuration and CSTS as interface evidence.
SQHD 前進表示已消費位置，不表示每筆命令完成；有效目標 CQE 才提供完成結果；中斷則是通知 Host 查 CQ 的機制。 || Advanced SQHD establishes consumption, not completion of every command; a valid target CQE establishes its result, while interrupts notify the host to inspect CQs.
依序確認 SQE 對 controller 可見、Doorbell 已更新、CQ 是否有新 Phase、Host 是否消費並更新 Head。若無法觀察內部取得時點，就明確保留這項不確定性。 || Check visibility, doorbell update, new CQ phase and host consumption/head updates. State uncertainty when internal fetch timing is unobservable.
能定位到「CQE 已存在但中斷或 Host 處理遺漏」，就不應再宣稱命令未執行。若只有 Doorbell 證據，也不能宣稱 controller 已取得命令。 || An existing CQE localizes the issue beyond execution; a doorbell write alone does not prove command fetch.
這項診斷本身沒有固定 NVMe Status。不同階段的錯誤應保留各自證據，不用一個自創 Timeout Status 取代。 || This diagnosis has no single NVMe status; preserve stage-specific evidence rather than inventing a timeout status.
比對同時間的有效 CQE、共享 CQ 空間及中斷遮蔽，排除 Host 端的進度阻塞。 || Correlate valid completions, shared CQ space and interrupt masking to identify host-side stalls.
先直接檢查目標 CQ 的期待 Phase 位置；這通常最快區分「尚未回報」與「已回報但未處理」。 || First inspect the expected-phase CQ slot to distinguish an unreported result from an unconsumed completion.
''')
