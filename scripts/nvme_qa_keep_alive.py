"""Q217–222: optional PCIe Keep Alive and its actual timeout conditions."""
from scripts.nvme_qa_extension import question
from scripts.nvme_qa_model import COMMON, pair
COMMON['keepalive_op']={**COMMON['command'],**COMMON['feature'],
 9:pair('Keep Alive 成功不產生另一筆成功 AER。Timeout 後 controller 必須停止處理命令並設定 CFS，Host 不能依賴還能用 AER 收到故障通知。 || A successful Keep Alive defines no separate success AER. Timeout stops command processing and sets CFS, so the host cannot rely on continued AER delivery.'),
 10:pair('Keep Alive Timeout 必須在 CQT 指定的清理時間內記錄 Error Information entry，Status 為 Keep Alive Timeout Expired。這是明定的記錄義務，不能與一般命令失敗是否需要 entry 混為一談。 || Keep Alive Timeout requires an Error Information entry with Keep Alive Timeout Expired within CQT cleanup time; this is an explicit requirement distinct from ordinary command-error logging.'),
 11:pair('若 PEL 支援對應 Controller Fatal Status 硬體事件，Timeout 導致 CFS=1 時依該事件規則記錄；不是每筆 Keep Alive 都記一筆 PEL。 || Supported PEL Controller Fatal Status hardware events follow the resulting CFS condition; individual Keep Alive commands are not a PEL trace.'),
 15:pair('Timer 屬於目標 controller；其逾時清理停止該 controller 處理命令，不是刪除 namespace 或清除使用者資料。其他路徑若要接手，仍須先處理失聯路徑可能留下的未完成操作。 || The timer targets a controller. Cleanup stops its processing, not namespace or user-data deletion. Failover must still account for unresolved work on the failed path.')}

def q(n,t,b,o=None): question(n,t,'keepalive_op',['keepalive','idctrl','feature','setfeat','commrecovery'],b,o)

q(217,'PCIe Host 如何確認 Keep Alive 支援？ || How does a PCIe host discover Keep Alive support?', '''
Keep Alive 是通訊存活監測，不是每筆 I/O 的執行期限。PCIe 不要求所有 SSD 都啟用它。 || Keep Alive monitors communication liveness, not each I/O’s execution deadline; PCIe does not require every SSD to enable it.
每個 controller 各自有 Timer，不能以另一個 controller 的活動替代。 || Each controller has its own timer; activity on another controller does not substitute.
Identify.KAS 非零表示支援，並給出以 100 ms 為單位的設定粒度；CTRATT.TBKAS 表示 Traffic Based 模式。 || Nonzero KAS advertises support and 100 ms granularity units; CTRATT.TBKAS identifies Traffic Based mode.
支援 Timer 就必須支援 Keep Alive 命令；設定透過 FID0Fh.KATO，單位為毫秒。 || Timer support requires the Keep Alive command; FID0Fh KATO configures milliseconds.
先讀 KAS，再判斷模式及需要的 KATO，最後 Get 確認實際採用值。 || Read KAS, determine mode, configure and read back the actual timeout.
PCIe 的預設 KATO=0，即停用；支援能力非零與目前有啟用，是不同資訊。 || PCIe defaults to disabled KATO=0; support and active use are distinct.
KAS=0 時不能要求它接受 Keep Alive 或 Timer 設定；依實際不支援的 Opcode／Feature 回應判讀。 || KAS=0 does not promise command/feature acceptance; apply the relevant unsupported-command/feature rules.
KAS、TBKAS、Commands Supported and Effects 與實際 FID 行為需一致。 || KAS, TBKAS, command support/effects and feature behavior must agree.
先檢查是否誤把 PCIe 的選配能力當成所有裝置的必要功能。 || First check whether an optional PCIe capability was incorrectly assumed mandatory.
''')
q(218,'Keep Alive Timer 如何設定、調整與停用？ || How is the timer configured, adjusted and disabled?', '''
Host 設定可容忍的通訊空窗；controller 依支援粒度採用可實作的值。 || The host chooses a communication interval and the controller applies supported granularity.
設定作用於此 controller，不是整個 subsystem 的共同 I/O timeout。 || It is controller-scoped, not a subsystem-wide I/O timeout.
先讀 KAS 與目前 FID0Fh.KATO，並確認 Feature 的保存能力。 || Read KAS, current KATO and feature saveability.
Set Features CDW11.KATO 指定毫秒；controller 必須向上取到 KAS 的粒度。非零值低於實作最小值時，採最小值。 || KATO is milliseconds; round upward to KAS granularity and apply an implementation minimum when needed.
Set 成功後 Get 讀實際值，再更新 Host 的發送排程；PCIe 可設 KATO=0 停用。 || Read the effective timeout after success and update host scheduling; PCIe allows KATO=0 to disable.
例如 KAS=10 表示 1000 ms 粒度，要求 1500 ms 會向上成 2000 ms，前提是沒有更大的最小值。 || With hypothetical KAS=10, 1500 ms rounds to 2000 ms unless a larger minimum applies.
若要求超過適用傳輸允許的最大值，回 Keep Alive Timeout Invalid 且保留原設定；不能自行替 PCIe 編造固定最大限制。 || An applicable transport maximum violation returns Keep Alive Timeout Invalid without changing the setting; do not invent a fixed PCIe maximum.
Get 的回值可合法大於要求值；只有確認粒度與最小值後，才能判定調整是否不合理。 || A larger readback can be valid because of rounding/minimums.
先檢查 Host 是否仍按要求的 1500 ms 而不是實際 2000 ms 排程。 || First check whether host scheduling uses the requested or effective timeout.
''')
q(219,'Host 如何在 Timer 到期前維持 Keep Alive？ || How does the host maintain liveness before expiry?', '''
預留時間餘裕，才能容納排程、命令處理與傳輸延遲；在最後一刻送出不代表 controller 已及時處理。 || Margin accommodates scheduling and processing delay; last-moment submission does not prove timely controller processing.
只有 EN=1、RDY=1、SHN=00b、SHST=00b 且 KATO 非零時 Timer 才 active。 || The timer is active only with EN=RDY=1, SHN=SHST=00b and nonzero KATO.
讀實際 KATO，並確認 Command Based 或 Traffic Based 模式。 || Read effective KATO and determine the active mode.
Command Based 的 controller 在 Keep Alive 成功完成，或成功設定非零 KATO 時重新計時；普通 Read 不會替代它。 || Command Based restarts on successful Keep Alive or nonzero KATO Set, not ordinary Reads.
Host 建議每 KATT/2 送 Keep Alive，並在 Admin SQ 保留可提交空間；調整 KATO 成功後也更新排程。 || The host should send at KATT/2 and keep Admin SQ space available, adjusting scheduling after successful KATO changes.
持續收到成功 Completion 能證明這條通訊路徑仍能往返；不是證明每筆媒體操作都已完成。 || Successful completions demonstrate communication, not completion of every media operation.
Keep Alive 自己長時間沒有 Completion 時，Host 依其送出後 KATT 的判斷與恢復規則處理，不能無限補送來掩蓋失聯。 || Missing Keep Alive completion is assessed against KATT and recovery rules rather than hidden by endless submissions.
把 Host 送出、controller 完成與 Host 收到的時間分開，才能解釋兩端觀察差異。 || Separate submission, controller completion and host receipt timestamps.
先檢查 Admin SQ 是否被其他命令塞滿，導致 Keep Alive 根本尚未提交。 || First check whether Admin SQ congestion prevented actual submission.
''')
q(220,'Keep Alive Timeout 後，Controller 必須做哪些清理？ || What cleanup is required after Keep Alive Timeout?', '''
Timeout 清理讓失去可靠通訊的 controller 停止繼續處理命令，降低 Host 轉移工作後仍有舊操作進行的風險。 || Cleanup stops processing on a failed communication path before host recovery introduces new work.
本題只列 PCIe 適用動作；它不刪 namespace、不執行 Sanitize，也不承諾回復已寫入資料。 || PCIe cleanup neither deletes namespaces, sanitizes data nor rolls back writes.
查 Identify.CQT、CSTS.CFS 與 Error Information，並保留 outstanding 清單。 || Check CQT, CFS and Error Information with outstanding-command records.
規範要求在 CQT 內記錄 Keep Alive Timeout Expired、停止命令處理，並設 CSTS.CFS=1。 || Within CQT, log Keep Alive Timeout Expired, stop processing and set CFS.
Host 停止提交到該路徑，保存可取得的狀態，再依通訊恢復與 Reset 流程重建。 || Stop submissions, preserve available evidence and recover/reinitialize the path.
完成清理表示停止處理；不代表每筆 outstanding 都會取得成功或錯誤 CQE。 || Cleanup establishes stopped processing, not a CQE for every outstanding command.
不能以 Keep Alive Timeout 直接指定舊 Write「沒有執行」，也不能假設所有舊命令可以安全原樣重送。 || Timeout does not prove old Writes unexecuted or safely retryable unchanged.
CFS、Error entry 與清理時間應一致，資料操作則另查實際效果與重試相依性。 || Correlate fatal state, error record and cleanup timing separately from data effects.
先確認逾時是 Host 自己判斷，還是 controller 已偵測並完成清理。 || First distinguish host-detected timeout from controller-detected/completed cleanup.
''')
q(221,'Controller Reset 後，是否要重新設定 Keep Alive？ || Must Keep Alive be reconfigured after reset?', '''
Reset 結束舊命令環境，但 Timer 的恢復還取決於 Feature 保存與持續性，不能只因記得舊 KATO 就直接沿用排程。 || Reset ends the old command environment; restored timer configuration follows feature persistence rather than host memory of old KATO.
針對被重設的 controller，重新確認設定與 Timer active 條件。 || Reassess the affected controller’s configuration and activation conditions.
查恢復後 Current KATO、支援能力及適用的 Saved／Default 規則。 || Read restored Current KATO and applicable Saved/Default behavior.
Timer 在 EN／RDY／SHN／SHST 任一條件不符時 inactive；再次由 inactive 轉 active 時初始化為有效 KATO。 || Invalid activation conditions make the timer inactive; activation initializes it to effective KATO.
完成初始化，Get 確認 KATO；若為 0 而 Host 需要啟用，再 Set 非零值並讀回，然後重啟 Host 維護排程。 || Initialize, read KATO, enable/read back if needed and restart host maintenance scheduling.
Host 排程與 controller 的實際值、模式及新使用期間一致。 || Host scheduling matches the actual value, mode and new controller lifetime.
Reset 前尚未完成的 Keep Alive 不能拿舊 CQE bytes 當成 Reset 後成功的存活證據。 || Pre-reset commands or stale CQE bytes do not establish post-reset liveness.
重設前後比較的是設定恢復規則，不是要求倒數值接續到最後一毫秒。 || Validate restored configuration, not continuation of the old countdown to the millisecond.
先讀 Current KATO，再決定是否需要重設值，避免把「必須重查」誤寫成所有裝置都「必須重設同一值」。 || Read Current before deciding whether to reconfigure; rediscovery is not universally rewriting one value.
''')
q(222,'Command Based 與 Traffic Based Keep Alive 有何不同？ || How do command-based and traffic-based Keep Alive differ?', '''
兩種方式判斷存活的證據不同：前者靠專用命令，後者可利用一般命令流量。 || One mode relies on explicit Keep Alive commands; the other can use normal command traffic.
模式由支援 Keep Alive 的 controller.TBKAS 決定，不是 Host 任意忽略專用命令就算啟用 Traffic Based。 || Controller TBKAS determines support; the host cannot unilaterally assume traffic-based operation.
確認 KAS 非零與 CTRATT.TBKAS；TBKAS=0 使用 Command Based。 || Check nonzero KAS and TBKAS; zero selects command-based behavior.
Traffic Based 的 controller 看每個 KATT 區間是否曾 fetched Admin 或 I/O command；Host 則用已提交且已處理 Completion 的活動作為省略 Keep Alive 的證據。 || Traffic-based controller checks for fetched commands per KATT interval; the host uses submitted-and-completed activity to decide whether to skip Keep Alive.
Host 在 Traffic Based 模式建議每 KATT/4 檢查是否需送專用命令；沒有足夠活動時仍送 Keep Alive。 || In traffic-based mode the host should check every KATT/4 and send Keep Alive when qualifying traffic is absent.
一個區間有取得命令，controller 可開始下一區間，因此最後一次 fetched 後到偵測 Timeout 可能接近 2×KATT。 || A fetch in an interval permits the next interval, so detection can take nearly 2×KATT after the last fetch.
不能要求 Traffic Based 在最後一筆命令後剛好 KATT 就一定 Timeout，也不能只因一筆長命令仍 outstanding 就認為每個後續區間都有新流量。 || Do not require expiry exactly KATT after the last fetch or treat one long outstanding command as new traffic in every interval.
依 fetched、completed 與區間邊界核對，不把「Host 已寫 SQE」當成 controller 已取得。 || Compare fetch/completion evidence and interval boundaries, not merely a prepared SQE.
先檢查 TBKAS 與實際採用的兩端模式是否一致。 || First check mode agreement with TBKAS.
''')
