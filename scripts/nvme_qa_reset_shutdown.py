"""Q174–187: reset scope, shutdown completion and actual power loss."""
from scripts.nvme_qa_extension import question
def q(n,t,r,b,o=None): question(n,t,'reset_review',r+['reset','cc','shutdownfull','pciereset','smart'],b,o)

q(174,'Controller、Subsystem 與 Queue Level Reset 範圍有何不同？ || How do controller, subsystem and queue resets differ?', [], '''
選擇合適的範圍，才能恢復故障並掌握哪些工作會被中止。 || Choose recovery scope with known impact on ongoing work.
Queue Reset 刪除重建指定 I/O queue；CLR 重設一個 controller 的命令環境；Subsystem Reset 涵蓋一個或全部 domains。 || Queue reset recreates selected I/O queues; CLR resets a controller; subsystem reset covers its defined domains.
查 CAP.NSSRS、controller／domain 拓樸與 queue 相依關係。 || Check NSSRS, domain topology and queue dependencies.
Queue Reset 用 Delete／Create；Controller Reset 清 CC.EN；NSSR.NSSRC 寫 4E564D65h 請求支援的 Subsystem Reset。 || Use Delete/Create, clear CC.EN or write4E564D65h to supported NSSR respectively.
停止受影響提交，選擇範圍，完成等待與重建，再恢復命令。重建 CQ 前先處理依賴它的 SQ。 || Quiesce, reset/rebuild and resume, respecting SQ/CQ dependencies.
新 queue 或 controller 恢復可用，原使用期間的追蹤不再沿用。 || Recovered resources begin a new valid lifetime.
Register 觸發 Reset 沒有 CQE；Delete／Create 才有其命令完成。 || Register reset has no CQE; queue-management commands do.
用實際被刪除的 queues 與受影響 controllers 驗證範圍，不能只看 Host 函式名稱。 || Verify affected resources rather than host function names.
先確認這次所說的 Reset 具體是哪一種。 || First identify the actual reset mechanism.
''')
q(175,'Conventional、FLR、Hot 與 Fundamental Reset 如何對應 NVMe？ || How do PCIe reset types affect NVMe?', [], '''
本題只教 NVMe 可觀察的重設效果，不展開 Link 或封包。不同來源會影響 Register 保留與韌體啟用。 || Focus on NVMe-visible effects; reset source changes retention and activation.
FLR 針對 function；Conventional Reset 包含適用的 Hot／Fundamental 形式，實際影響須依裝置拓樸確認。 || FLR is function-level; Conventional Reset includes Hot/Fundamental forms, with topology determining affected controllers.
確認 PCIe reset 支援、CAP 與待啟用 Firmware Commit 要求。 || Check reset support, CAP and pending firmware requirements.
PCIe Transport3.3 將 Conventional 與 FLR 列為 CLR 來源；CC.EN 的 Controller Reset 不重設 PCI configuration space。 || Conventional/FLR initiate CLR; CC.EN reset does not reset PCI configuration space.
記錄實際來源，恢復適用 PCI 配置，再執行 NVMe 初始化。 || Record source, restore applicable PCI configuration and initialize NVMe.
受影響 NVMe queues 依 CLR 重建；不能期待 FLR 保留 I/O queues。 || Rebuild affected queues; FLR does not preserve I/O queues.
要求 Conventional Reset 才能啟用的映像，不會因 FLR 或 CC.EN Reset 提前啟用。 || FLR/CC.EN do not satisfy a required Conventional Reset.
CMBMSC 對 FLR 另有保留例外，不能概括成所有 Register 皆歸零。 || Respect exceptions such as CMBMSC retention under FLR.
先查 Host 到底觸發哪個 reset source。 || First identify the actual reset source.
''')
q(176,'Reset 發生在 Idle、命令或背景操作中，如何判斷結果？ || How do reset outcomes depend on ongoing activity?', ['sanitizecmd','selftest','firmware'], '''
Reset 對命令通道與背景操作可能有不同效果，不能只用「全部中止」概括。 || Channels and background operations can have different reset behavior.
受影響 queues 結束，但資料與持久管理狀態各依自己的規則。 || Queues end while data/management state follow specific rules.
保存 outstanding 清單、操作 Log 與 Reset 來源。 || Snapshot outstanding work, logs and reset source.
Sanitize 持續；Short Self-test 中止；Extended Self-test 恢復；未 Commit 的 firmware 下載丟棄。 || Sanitize continues, short tests abort, extended tests resume and uncommitted staging is discarded.
Reset 前記錄階段，恢復後讀對應 Log 與 Identify，不憑舊 CQE bytes 猜結果。 || Record stage and reread state instead of stale CQE bytes.
逐項判定完成、中止、持續或仍未知，再決定後續。 || Classify each operation as complete, stopped, continuing or unresolved.
沒有 CQE 不等於沒執行；Reset 不保證 Write 回復成舊資料。 || Missing CQE does not prove no execution or rollback.
按各功能的持久性驗證，不要求所有功能有同一結果。 || Apply per-function persistence.
先區分命令本身與它啟動的背景工作。 || First distinguish the command from its background work.
''')
q(177,'Reset 期間 CSTS.RDY 應如何變化？ || How does RDY behave during reset?', ['cap','crto'], '''
RDY 確認停用或重新就緒，不能以 Host 寫入 EN 代替觀察。 || RDY confirms disable/readiness, not just EN writes.
RDY 是 controller 狀態，不保證每個 namespace ready。 || RDY is controller state, not universal namespace readiness.
讀 CAP.TO、Ready Mode 與 CRTO 能力。 || Read CAP.TO and ready-mode/CRTO capabilities.
清 EN 後等 RDY=0；重新設 EN=1 後按正確期限等 RDY=1。 || Wait RDY0 after disable and RDY1 after enable with proper deadlines.
停用完成前不重新 Enable，先完成新環境設定再啟用。 || Complete disable/configuration before re-enabling.
RDY 轉移與所選模式一致；media 尚未就緒時仍遵循模式限制。 || Transitions and media restrictions follow the selected mode.
Register 讀取失敗不能當成 RDY=0 證據。 || An inaccessible register is not RDY0 evidence.
保存 EN、RDY、CFS 與時間，區分請求與確認。 || Correlate request and acknowledgment with timing.
先排除存取失敗回傳的填充值。 || First exclude failed-access fill values.
''')
q(178,'Reset 後哪些 Register、Feature 與 Queue 要重建？ || What needs rebuilding after reset?', ['feature','adminreg'], '''
重建依 Reset 來源與 Feature 規則，不能照抄舊記憶體。 || Rebuild by reset source and feature rules.
I/O queues 失效、Admin 指標重設；持久 namespace 與 Saved 設定是另一層。 || Queues/pointers reset separately from persistent configuration.
查 Register 例外、Feature 能力／Current 與 queue 配額。 || Check retention exceptions, features and queue allocation.
CC.EN Reset 保留 AQA／ASQ／ACQ、指定 PMR registers 與 CMBMSC，但不保留 queue 指標。 || CC.EN reset preserves specified registers, not queue pointers.
恢復必要 PCI／Register 設定，初始化 Admin Phase，Enable 等 RDY，配置功能，再建 CQ／SQ。 || Restore transport/registers, initialize phase, enable/wait, configure and recreate queues.
新 queue 正常完成命令，Current Feature 符合恢復規則。 || New queues work and features restore correctly.
保留位址不代表舊 CQE 有效；不可保存 Feature 也不一定回零。 || Retained addresses do not validate CQEs; non-saveable is not necessarily zero.
比較 Saved、Current 與例外，不用「全部歸零」的固定斷言。 || Compare values and exceptions rather than blanket zeroing.
先確認 Reset 來源再決定初始化步驟。 || Establish reset source first.
''')
q(179,'Reset 後舊 Outstanding 與 Completion 應如何處理？ || How are old outstanding commands handled after reset?', ['commrecovery'], '''
避免舊完成誤配新 CID，以及舊命令晚到的存取干擾新工作。 || Prevent stale-CID confusion and late effects.
追蹤按 queue 使用期間隔離，共享資料的其他 controller 也可能參與復原。 || Separate lifetimes, including cross-controller recovery.
保存 Reset 完成證據與舊 SQID／CID 清單。 || Preserve reset and old-command evidence.
重新初始化 Phase 與指標，不把 Reset 前 CQE 當新完成。 || Reinitialize phase/pointers, ignoring old-generation CQEs.
確認舊處理已停止，再回收資源或由其他 controller 重試改寫命令。 || Establish termination before reclamation or mutating retries.
每筆新命令只收到新使用期間的結果；舊命令資料效果另行確認。 || New commands use new results; assess prior data effects separately.
失去通訊時不能要求全部舊命令回固定 Abort Status。 || Lost communication precludes a universal abort-CQE requirement.
區分 controller 新寫入與記憶體殘留的 CQE。 || Distinguish fresh writes from residual bytes.
先查 Phase 初始化與 CID 重用紀錄。 || Inspect phase and CID reuse first.
''')
q(180,'Reset 後如何確認 Feature、Log、Namespace 與 Firmware？ || How is state revalidated after reset?', ['feature','firmware','sanitizelog','dstlog'], '''
RDY=1 之外，還要知道哪些設定恢復、哪些背景操作持續。 || RDY1 alone does not establish restored settings or background state.
依 controller、namespace、subsystem 的各自範圍查詢。 || Query each defined scope.
使用受支援的 Identify、Get Features 與 Logs。 || Use supported discovery interfaces.
Feature 查 Current／Saved；namespace 查身分與清單；firmware 查 FR／slots；背景操作查對應 Log。 || Inspect feature values, namespace lists, firmware and operation logs.
恢復 Admin 通道後查狀態，再建立與新格式／能力一致的 I/O 環境。 || Discover state before resuming correctly configured I/O.
變化應能解釋，例如 Sanitize 進度延續，但舊 AER 已失效。 || Explain differences such as continued sanitization with invalidated AERs.
Error entries 清除而計數保留可以同時符合規範。 || Cleared entries and retained counters can both conform.
按持久、恢復及即時欄位分類比對。 || Compare persistent, restored and live fields appropriately.
先排除把一份空 Log 推論成所有歷史消失。 || Avoid generalizing one empty log to all history.
''')
q(181,'Reset 超時或 CFS 未清除時怎麼辦？ || What if reset times out or CFS remains?', ['fatal','cap','crto'], '''
先區分期限用錯與持續故障，不無限重送。 || Distinguish a wrong deadline from persistent failure.
先處理該 controller，擴大範圍前確認平台支援及其他使用者。 || Start locally and assess broader impact.
保存 CAP／CRTO、EN／RDY／CFS、來源與時間。 || Preserve capability/state/source/timing.
停用用 CAP.TO，啟用依 Ready Mode；fatal recovery 依 Base9.5。 || Apply the correct deadlines and fatal-recovery rules.
確認讀值有效，先 Controller Reset；CFS 仍未清除才評估適用的 Subsystem Reset。 || Validate readings, reset controller and consider subsystem reset if appropriate.
恢復後狀態與命令通道都可用，不只是一個 CFS 位元清零。 || Recovery includes usable channels, not only cleared CFS.
不能以任意更短的 Host timeout 判違規，也不盲目要求不適合平台的 Subsystem Reset。 || Avoid unjustified short deadlines or unsuitable subsystem resets.
先排除 Secondary Offline 預期造成的 CFS。 || Exclude expected Offline-secondary CFS.
先核對期限與 controller 角色。 || Verify deadline and role first.
''')
q(182,'Host 如何用 CC.SHN 做 Normal Shutdown？ || How is normal shutdown requested?', [], '''
Normal Shutdown 準備保存與媒體關機，不等於停用 controller。 || Normal shutdown prepares media, unlike disable.
可斷電範圍須依 CAP.CPS 協調相關 controllers。 || Coordinate controllers in CAP.CPS power scope.
讀 CPS、RTD3E、SHST 與 ST。 || Read power scope, latency and shutdown status.
SHN=01b 要求 Normal；SHST=10b、ST=0 表示 controller shutdown 完成。 || SHN01b requests normal shutdown; SHST10b/ST0 confirms it.
停止新 I/O 並等既有命令，建議刪 SQ 再刪 CQ，最後設 SHN 並等待。 || Quiesce/drain, delete SQs then CQs, request shutdown and wait.
完成後可斷電狀態持續到規定的狀態改變事件。 || Readiness persists until a defined state-changing event.
寫 SHN 沒有 CQE；處理中命令可被 Power Loss Notification Status 中止。 || SHN has no CQE; commands may be aborted for power-loss notification.
確認實際 SHST，不能只看送出 SHN。 || Verify acknowledgment rather than request alone.
先確認是否誤用清 EN 代替關機。 || Exclude disable-as-shutdown first.
''')
q(183,'何時算 Shutdown Complete，可以移除電源？ || When is power removal appropriate?', ['cap'], '''
發出通知不等於完成保存，需等實際完成狀態。 || Notification is not completed preparation.
domain／subsystem scope 須全部相關 controllers ready。 || All controllers in the power scope must be ready.
查 SHST、ST、CPS 與 RTD3E。 || Inspect status, scope and latency guidance.
SHST01b=處理中，10b=完成；一般 controller shutdown 用 ST0。 || SHST01b/10b mean processing/complete with ST0 for controller shutdown.
輪詢完成；RTD3E=0 時建議至少等待1秒供處理，不是到1秒就無條件拔電。 || Poll completion; the one-second guidance for RTD3E0 is not unconditional removal permission.
所需範圍皆 ready-to-power-off 才符合建議。 || Establish readiness across the required scope.
之後 Reset 或允許的媒體存取可能使先前 readiness 失效。 || Later reset/media access can invalidate readiness.
用最後狀態與實際失電時點比對，不忽略中間操作。 || Correlate latest state with actual loss.
先查 CPS 是否要求等待其他 controller。 || Check multi-controller power scope first.
''')
q(184,'Normal、Abrupt Shutdown 與直接斷電有何不同？ || How do normal, abrupt and unannounced loss differ?', [], '''
Normal 與 Abrupt 都有通知；直接失電可能沒有準備時間。 || Both shutdown types notify; unannounced loss may not.
流程不同會影響未完成工作與持久性，但仍需確認 power scope。 || Work/persistence opportunities differ within the required power scope.
保存 SHN、SHST、power 事件及 SMART.UPL。 || Preserve shutdown, power and counter evidence.
SHN01b／10b 分別選 Normal／Abrupt，兩者都用 SHST10b 回報完成。 || Both modes report completion through SHST10b.
Normal 建議排空與刪 queue；Abrupt 停止新 I/O 再通知；直接斷電無法等待。 || Normal drains/deletes; abrupt stops new I/O/notifies; sudden loss cannot wait.
Abrupt 若完成且失電時仍 ready，不必只因名稱就增加 UPL。 || Ready abrupt shutdown does not increment UPL merely by name.
未完成 volatile writes 的持久性不能只靠 Shutdown 名稱保證。 || Procedure names do not guarantee outstanding-write persistence.
分別觀察要求、完成與失電三個時點。 || Observe request, completion and actual loss.
先查失電時 SHST 與媒體狀態。 || Inspect state at loss first.
''')
q(185,'Shutdown 期間能否繼續新命令或保留 Outstanding？ || What may remain outstanding during shutdown?', [], '''
持續提交新 I/O 會妨礙有序關機，因此先停止新工作。 || Continued I/O obstructs orderly shutdown.
I/O 與 Admin 不同，AER outstanding 不等於資料尚未寫完。 || Pending AERs are not pending data writes.
觀察 outstanding 清單與 SHST。 || Inspect command tracking and shutdown state.
正常流程排空 I/O；Admin 是否先 Abort 由 Host 選擇，完成時建議只剩 AER。 || Drain I/O; Admin abortion is host policy, with only AERs recommended outstanding at completion.
停止新工作並處理既有結果，送 SHN 後不任意清 EN 影響關機時間。 || Quiesce/process results, request shutdown and avoid disrupting it with EN clearing.
SHST 完成可與 pending AER 並存。 || Complete shutdown can coexist with pending AERs.
處理中命令可因 Power Loss Notification 被中止，不保證晚到命令成功。 || Late commands may be aborted for power-loss notification.
確認 Host 沒把 AER 計入資料排空條件。 || Exclude AERs from data-drain expectations.
先查卡住的是 I/O 還是長駐 AER。 || Identify the pending command type first.
''')
q(186,'Normal／Abrupt 如何影響 Unsafe Shutdowns？ || How do shutdown modes affect the former Unsafe Shutdowns counter?', [], '''
Base2.4 改稱 Unexpected Power Losses（UPL），依真正失去 main power 時的狀態計數。 || Base2.4 calls it UPL and counts actual loss conditions.
UPL 是 SMART 生命週期資訊，不是每筆 Shutdown 的結果。 || UPL is lifetime information, not per-shutdown status.
讀 LID02h bytes144～159，保存失電前狀態。 || Read bytes144–159 and preserve pre-loss state.
main power 失去且 SHST≠10b 時必須增加；另有 out-of-band Ignore Shutdown 導致媒體不在 shutdown state 的條件。 || Increment with SHST≠10b at loss or the defined Ignore Shutdown/media exception.
先取基準，發通知並等完成，再移電與查增量；記錄中途媒體重新啟用。 || Baseline, request/wait, remove power and compare, recording intervening activity.
完成且保持 ready 的 Normal 或 Abrupt，不因名稱增加 UPL；未完成便失電則增加。 || Ready normal/abrupt shutdown does not increment by name; premature loss does.
沒有真正 power loss 的 Reset 不必增加 UPL。 || Reset alone is not a power-loss count.
依 if-and-only-if 條件驗證，排除額外失電及錯誤取樣。 || Apply exact conditions, excluding extra losses and wrong samples.
先查失電當下 readiness，不只看曾寫什麼 SHN。 || Check readiness at actual loss.
''')
q(187,'非正常失電後為何查 SMART、Error 與 PEL？ || Why inspect health, errors and persistent events after loss?', ['error','pel'], '''
各資料補充計數、目前錯誤與持久事件，填補失電時沒有 CQE 的觀察空白。 || Counters/errors/history help reconstruct the missing-completion interval.
使用相同身分，分清累計與即時狀態。 || Match identity and cumulative/live state.
確認 PEL 支援與事件，使用正確 LID。 || Check supported events and correct log selection.
SMART 看 UPL／Power Cycles／MDIE，Error 看 ECNT，PEL 看 Reset 與相關操作。 || Inspect power/error counters and reset/operation events.
恢復 Admin 後先保存 Log，再做可能覆寫歷史的測試。 || Preserve logs before generating additional history.
可知道失電與未確認操作；無 Error entry 不代表資料全部安全。 || Absence of an error entry does not establish data safety.
Error entries 建議於 power cycle 清除，空 Log 不必然違規，持久 counters 另看。 || Cleared entries can conform while counters persist.
比較計數、事件及電源時間線，不要求紀錄一對一。 || Correlate timelines without one-to-one record assumptions.
先保存恢復後第一份快照。 || Preserve the first recovered snapshot.
''')
