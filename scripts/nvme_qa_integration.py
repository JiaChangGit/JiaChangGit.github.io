"""Q297–320: distinct evidence-correlation exercises, linked to mechanisms."""
from scripts.nvme_qa_extension import question
from scripts.nvme_qa_model import QUESTIONS

def q(n,t,profile,refs,related,b,o=None):
    question(n,t,profile,refs,b,o)
    QUESTIONS[-1]['related']=related

q(297,"宣告支援的 Command 卻失敗，第一步怎麼查？ || Where do you start when an advertised command fails?",'error_review',['idctrl','commandseffects','status'],[50,81,93],'''
本題練習區分「支援命令」與「這次要求合法且可執行」。支援並不保證所有參數及狀態都成功。 || Distinguish command support from legality and executability of this request.
先固定同一 controller、命令集、namespace 與測試時點，避免拿另一條路徑的能力來比。 || Match controller, command set, namespace and time before comparing support.
保存 Identify 的支援位元與 Effects.CSUPP，並記錄 CSI／UUID 選擇。 || Preserve Identify support, CSUPP and CSI/UUID selectors.
假設支援 Format，卻回 Invalid Format；先讀原命令的 LBAF 與 namespace 可用格式。 || If supported Format returns Invalid Format, compare its LBAF with the namespace’s formats.
先解 CQE，再逐項核對參數、namespace 狀態、Write Protection 與當時的管理操作限制。 || Decode the CQE, then validate selectors, namespace state, protection and active-operation restrictions.
若只因選到不支援的 LBA Format 而失敗，這可與「支援 Format」完全一致。 || Rejecting an unsupported LBA format can be consistent with supporting Format.
若所有前提成立卻回 Invalid Opcode，才進一步核對命令集及支援宣告是否矛盾；單次失敗不能直接定案。 || Invalid Opcode with all prerequisites met warrants support-consistency investigation, not an automatic conclusion from any failure.
以同時點、單一變因的合法對照命令驗證，避免用另一組不同參數的成功取代原問題。 || Use a contemporaneous valid control differing in one relevant condition.
先檢查實際 SCT／SC，而不是只看應用程式顯示的「失敗」。 || First inspect SCT/SC rather than an application’s generic failure label.
''')
q(298,"未宣告支援的 Command 卻成功，是否一定合規？ || Does success of an unadvertised command prove compliance?",'error_review',['idctrl','commandseffects','status'],[48,50,80],'''
Success 只能說明這次命令的回覆，不能補正本來應準確回報的支援資訊。 || Success does not correct an inaccurate capability declaration.
先確認欄位確實適用於這個 controller 類型、命令集與查詢版本。 || Establish applicability to controller type, command set and query revision.
對照 Identify、Supported Log Pages 或 Commands Supported and Effects 的對應宣告，不混用不同能力欄。 || Compare the relevant discovery interface rather than unrelated capability bits.
例如 Effects 中某 opcode 的 CSUPP=0，但相同 CSI 下合法命令完成且有實際效果，兩項證據需要調查。 || CSUPP0 and successful effective execution of that opcode under the same CSI require investigation.
先排除舊快照、Firmware Activation、錯誤 opcode 分類與誤解保留欄位，再重做同時點查詢。 || Exclude stale snapshots, activation, opcode-category confusion and reserved-field misinterpretation.
宣告應與當前支援一致；驗證要同時看回覆與可觀察結果，避免假的 Success 沒做事。 || Capability, completion and observable effects must agree.
只有規範要求不支援時拒絕，才能指定對應錯誤；不能把未知／不適用欄位清零一概當成禁止命令。 || Require rejection only where the specification defines unsupported behavior; inapplicable zero fields do not universally prohibit commands.
若確認同一合法條件下宣告與執行矛盾，保留兩份原始回覆，指出違反的具體欄位規則。 || Preserve contradictory evidence and cite the exact declaration rule.
先檢查查詢 selector 與命令 selector 是否一致。 || First compare discovery and execution selectors.
''')
q(299,"Set 成功但 Get 或行為不同，如何縮小問題？ || How is a successful Set with different readback or behavior investigated?",'feature',['feature','setfeat','featureeffects'],[54,55,66,68],'''
將接受設定、目前值、保存值與實際效果拆開，才知道差異發生在哪一層。 || Separate acceptance, current value, saved value and actual effect.
Feature 可能屬於 controller、namespace 或其他實體，Get 必須指定相同目標。 || Feature scope determines the target that Get must match.
查 SEL=3 的能力與該 FID 的欄位定義，確認是否允許 controller 調整要求值。 || Check supported capabilities and whether the feature may adjust requested values.
例如 KATO 可依 KAS 向上調整，讀回值大於要求不必然是錯誤；不能只做逐 bit 相等比較。 || KATO may round up to KAS granularity, so a larger readback is not necessarily wrong.
先保存 Set 的 SV／NSID／資料，再用 SEL=0 查 Current；需要測保存時才另查 Saved 並執行指定 reset。 || Preserve Set selectors/data, read Current and separately test Saved/restoration.
讀回合法調整後的值且實際行為符合該值，可構成成功驗證。 || Valid adjusted readback with matching behavior can be a passing result.
若讀的是 Default 或另一 NSID，先修正查詢；若 selector 都相同且沒有允許調整或並行修改，才定位 controller 不一致。 || Correct selector mistakes before diagnosing unexplained same-target inconsistency.
保存中途的其他 Set、reset、模式切換；它們都可能使測試後的 Current 不同。 || Track intervening configuration, resets and mode changes.
先確認 Get.SEL=0 以及 FID 的作用範圍。 || First check Current selection and feature scope.
''')
q(300,"AER 已完成，但對應 Log 看不到資訊，怎麼查？ || Why might an AER completion have no matching visible log information?",'aer_request',['aerfull','getlog','smart'],[83,84,90,92],'''
通知指出曾發生符合條件的事件；後續 Log 可能是目前狀態，不一定保存事件發生時的完整快照。 || A notice identifies a qualifying event, while the log may expose current state rather than a historical snapshot.
讀取範圍與事件的 controller、namespace 或 Group 必須相符。 || Match log scope to the event’s endpoint and entity.
保存 AER.CQE.DW0 的事件分類、資訊與 LID，並核對所需額外 selector。 || Preserve event type, information, LID and required selectors.
例如溫度越過門檻後又恢復，SMART Current Warning 可能已清除；這不否定稍早通知。 || A temperature warning may clear before a later SMART read without invalidating the earlier event.
先讀正確 Log，再查其他 Host 或程式是否已用 RAE=0 確認，及 Log 是否在兩次讀取間變動。 || Read the matching log and check intervening acknowledgments and state changes.
事件資訊、讀取時間與目前狀態能形成合理時間線，即使目前警告已消失也可能正常。 || A coherent timeline can explain cleared current state after a valid event.
Immediate、One-Shot 與一般事件清除方式不同；不能要求每種事件都必須留在 Log 等 Host 讀。 || Immediate, One-Shot and ordinary events have distinct clearing rules.
若事件與 Log 持續矛盾，保存首次讀取原件與所有 RAE 操作，避免重讀把證據改掉。 || Preserve the first read and all acknowledgments before investigating persistent inconsistency.
先檢查 LID、scope 與事件至讀取之間的時間差。 || First check LID, scope and observation delay.
''')
q(301,"失敗 CQE 沒新增 Error Entry，一定違規嗎？ || Does every failed CQE require a new error entry?",'error_review',['status','error'],[99,103],'''
Error Information 不是所有失敗 CQE 的逐筆必備副本；必須找出此錯誤是否有明確記錄要求。 || Error Information is not a mandatory one-entry copy of every failed CQE.
以同一 controller 的命令與 Error Count 比較；短時間多個錯誤可能覆蓋舊 entry。 || Match controller and error counts, considering overwrite by concurrent failures.
查 CQE.More、錯誤類別與該命令專屬的補充記錄要求。 || Inspect More and command-specific logging requirements.
More=1 指出有額外狀態資訊；More=0 不能反推絕不記錄。 || More1 indicates additional status information, while More0 does not prohibit logging.
保存失敗前後的 Error Count 與所有有效 entries，再依 SQID／CID／Status 關聯。 || Compare before/after counts and correlate valid entries by command identity and status.
若該類錯誤不強制新增且沒有其他違反條件，沒有新 entry 可以合規。 || Absence can be compliant where no applicable mandatory logging requirement exists.
若命令明定必須寫 Error Information 補充資訊，例如特定容量不足條件，缺少記錄就不能用一般可選規則帶過。 || Explicit mandatory details, such as specified capacity failures, override general optionality.
排除 ring 覆蓋、重設清除與錯誤讀取長度後，才判斷記錄是否真的缺失。 || Exclude overwrite, reset clearing and incomplete reads before declaring a missing record.
先找出這一個錯誤的 shall／should／may 記錄要求。 || First establish this error’s exact logging requirement strength.
''')
q(302,"CQE、Error Information 與 PEL 不同，何時才是矛盾？ || When do differing CQE, Error Information and PEL records conflict?",'error_review',['status','error','pelcontext'],[100,101,106,213],'''
三者記錄目的與時間不同，不能要求整筆資料逐 byte 一致。 || The three records have different purposes and timing, not bytewise equivalence.
CQE 屬於一筆命令，Error entry 補充錯誤，PEL 描述持續事件及其影響範圍。 || CQEs describe commands, error entries add failure details and PEL describes persistent events.
查事件支援、More 與原始命令身分，確認比較的是同一件事。 || Verify event support, More and command identity before correlating.
Error Status 的15:1應與相符 CQE Status 相同；Phase 可有其規範允許處理，不應當作錯誤碼的一部分。 || Matching error status bits 15:1 match CQE status; phase follows its separate rule.
先關聯 controller、SQID、CID 與時間，再解析 PEL 的事件專屬欄位，例如 Format 的 INFO／FNVMS。 || Correlate identity/time before parsing event-specific outcome fields.
Sanitize 命令成功接受，但稍後操作失敗時，早先 Success CQE 與失敗完成事件可以同時正確。 || Successful sanitize acceptance and later operation failure can both be correct.
若把不同時間的同 CID 或 PEL 請求值當成完成值，會形成假矛盾；真正違規需指明同一欄位關係的要求。 || Reused CIDs and requested-versus-completed values can create false contradictions.
建立含「接受、開始、操作完成、查詢」的時間線，再逐欄比對。 || Build an acceptance/start/operation-completion/query timeline.
先確認三份紀錄各自能證明什麼，而不是先找相同文字。 || First establish what each record actually proves.
''')
q(303,"Reset 後 Feature 保留或 Saved 遺失，如何判斷？ || How are unexpected feature retention or lost saved values assessed?",'feature',['feature','setfeat'],[55,67,318],'''
不可保存不等於不持續；可保存也不代表最近一次未設定 SV 的 Current 值必須跨斷電保留。 || Non-saveable does not mean nonpersistent, and unsaved current values need not survive power loss.
先判斷 Feature scope 與 reset 實際涵蓋的物件，部分重設和整體重設可能不同。 || Compare feature scope with actual reset coverage.
保存 Supported Capabilities、Current、Saved 與 Default，以及最後一次成功 Set 的 SV。 || Preserve capabilities, value classes and the last successful Set’s save bit.
例如 Namespace Write Protection 具有專屬持續性，不能只因不可保存就要求 CLR 清除。 || Namespace write protection has explicit retention despite being non-saveable.
先用成功 Set 建立已知 Saved，再執行明確 reset 類型，恢復後查同一目標的 Current／Saved。 || Establish known saved state, apply a specific reset and requery the same target.
恢復值符合一般 Feature 規則及個別例外才通過，不以「所有值變0」當成功。 || Pass criteria follow restoration rules and explicit exceptions, not universal zeroing.
若 Set.SV 未成功或中途另有合法 Set，就不能把差異直接歸為保存遺失。 || Failed saves or intervening changes invalidate a simple lost-save diagnosis.
將每個 FID 的保存與持續性分欄，並記錄 reset 來源和範圍。 || Record saveability, persistence, reset source and coverage separately.
先檢查成功 Set 的 SV 與該 FID 的例外。 || First check the successful save and feature-specific exceptions.
''')
q(304,"Namespace 變更後，Identify、Changed List 與 AER 如何對照？ || How are namespace changes reconciled across Identify, lists and AER?",'namespace_op',['nsattach','changedlog','aerfull','nspelevent'],[160,162,167,168],'''
Identify 描述目前配置，Changed List 列出曾變更的 NSID，AER 則提醒 Host 需要重新查詢。 || Identify exposes current configuration, the changed list identifies changes and AER prompts rediscovery.
同一 namespace 的變更不一定讓每台 controller 看到相同清單；需看各台 attachment 與通知規則。 || Controllers can observe different changes according to attachment and notification rules.
查支援、AEC 與等待中的 AER，再保存管理命令前後的清單。 || Record support/enables, pending requests and before/after inventories.
Attach 後看 Active List，Create 後看 Allocated List；兩者不能互相代替。 || Attachment changes active inventory while creation changes allocated inventory.
以單一操作建立時間線，等命令完成，再讀事件與清單，最後重讀 Identify 確认目前結果。 || Perform one operation, observe completion/notice and rediscover current state.
Changed List 有 NSID 並不表示該 namespace 目前仍存在；Delete 也能讓 Host 需要更新舊資訊。 || A changed NSID need not still exist because deletion also requires rediscovery.
清單超量可用 FFFFFFFFh 表示無法逐一列出，此時應重新探索全部，不把它當成真實 NSID。 || Overflow uses FFFFFFFFh and requires full rediscovery, not treating it as a real namespace.
先保存首次清單讀取，並區分管理命令所在 controller 與其他被通知 controller。 || Preserve the first list and distinguish the initiating endpoint from notified peers.
先確認此次變更是 Create／Delete 還是 Attach／Detach。 || First identify the management operation class.
''')
q(305,"Firmware Activation 後 FR 或 Slot 沒改，如何判斷？ || How are unchanged firmware revision or slot fields assessed after activation?",'firmware_op',['firmware','fwlog','fwpel'],[139,140,144],'''
下載、存入 slot、排程啟用與真正啟用是不同階段，不能把 Download Success 當成已換韌體。 || Download, slot commit, scheduled activation and actual activation are distinct stages.
Firmware 的 slot 與啟用可由同 Domain 的 controllers 共用，查詢必須在相關範圍內。 || Slot/activation state may be shared within a domain.
查 FRMW、LID03h 的 CAFS／NAFS／FRS，以及 Identify.FR。 || Inspect capability, current/next active slots, slot revisions and current firmware revision.
保存 Commit Action、Slot 與 CQE；某些結果要求 CLR、Subsystem 或 Conventional Reset，不是任意 reset 都能替代。 || Preserve action/slot/status and execute the specifically required activation reset.
先確認 Commit 有效，再執行指定啟用步驟，恢復後讀 FR 與目前 slot。 || Verify commit, perform activation and rediscover current state.
若新映像版本字串與舊版相同，FR 沒變不證明沒啟用；還需 slot 與其他可靠版本證據。 || Equal version strings do not alone prove activation failure.
啟用失敗可回復可用映像；PEL 的 New Firmware Revision 是要求的新版本，不自動證明已成為目前版本。 || Fallback and requested PEL revision are not proof of active new firmware.
把 pending slot、active slot、實際 FR 與 Firmware Commit／Reset 事件分開核對。 || Reconcile pending/active slot, current revision and commit/reset events separately.
先檢查 Commit Action 與是否做了正確類型的啟用。 || First verify action and activation mechanism.
''')
q(306,"Sanitize 命令成功後 Log 還在進行中，是錯誤嗎？ || Is an in-progress log after sanitize command success an error?",'sanitize_op',['sanitizecmd','sanitizelog','sanitizestate','sanitizepel'],[128,130,131,133],'''
Sanitize 的命令完成只表示操作已被接受並啟動；清除媒體可在背景繼續。 || Sanitize command completion acknowledges initiation, while media sanitization can continue in the background.
先分 Subsystem 與 Namespace Sanitize，並查正確 NSID 的結果。 || Match subsystem or namespace scope and result selection.
查 SANICAP、命令類型、Sanitize Status 及支援的完成事件。 || Inspect capabilities, command scope, status and supported completion events.
SPROG 是進度，SOS 是操作狀態；不能只看到 SPROG=FFFFh 就忽略 SOS 與 verification state。 || Interpret progress with operation and verification state, not FFFFh alone.
保存啟動 CQE，持續查狀態；有完成 AER 時再查相同操作的最終結果。 || Preserve initiation completion and poll state, then correlate final result with any completion event.
啟動成功後 SOS=進行中可以正常；真正完成時才應切換相應完成狀態並符合事件／Log 順序。 || In-progress after initiation is normal; final state must follow actual operation completion.
若已確認同一操作完成，Log 卻持續顯示進行中，先排除新的 Sanitize、錯誤 scope 或舊快取回覆。 || Exclude a newer operation, wrong scope and stale data before diagnosing a stuck status.
比對命令、Log、AER 及 PEL 的同一次操作，分清「命令完成」與「清除完成」。 || Correlate one operation across command, log, AER and PEL.
先檢查你稱為「完成」的證據到底是哪一種。 || First identify what the claimed completion actually establishes.
''')
q(307,"Self-test 已結束但沒有結果，如何驗證？ || How is a missing result after self-test investigated?",'selftest_op',['selftest','dstlog','nvmselftest'],[152,153,155,156],'''
啟動命令成功不代表測試成功；測試結束要由 Current Operation 與結果紀錄一起確認。 || Start-command success is not test success; current operation and result history establish the outcome.
確認查同一 controller／共享操作範圍，並使用正確的 Log 版本與完整長度。 || Match controller/shared-test scope and read the complete log correctly.
查 OACS、DSTO、EDSTT 與 LID06h；結果最新在前，有20筆結果位置。 || Inspect support/options/time and LID06h's20 newest-first result slots.
Current Operation、Completion Percentage、DSTR、DSTC 與 VDINFO 分別描述進行狀態、結果及欄位有效性。 || Current state, progress, result code, test code and validity bits have distinct roles.
保存開始前結果，啟動一次測試，等 Log 顯示結束，再與最新結果比對。 || Capture history, run one test and compare the newest result after completion.
規範要求結果更新與 Current Operation 回到 idle 的順序一致；讀到 idle 時應能查到本次應記錄的結果。 || Result update and return to idle follow the specified ordering for a test that produces a result.
Idle 時送 Abort 可成功但不新增結果；不能把這種情況誤判為漏記一次測試。 || An Abort while idle can succeed without creating a test result.
Short 遇 CLR 會中止，Extended 具有不同持續性；用測試種類與中斷時間解釋結果代碼。 || Interpret reset effects using the distinct short/extended-test rules.
先確認真的曾啟動測試，而非只成功送出 idle Abort。 || First establish that a test actually started.
''')
q(308,"Shutdown 與 Unsafe Shutdowns 計數不符直覺，如何判斷？ || How are unexpected unsafe-shutdown counts assessed?",'reset_review',['smart','shutdownfull','pciereset'],[183,184,186,199],'''
計數不能只按 Host 寫了 Normal 或 Abrupt 分類；需看主電源移除時的實際完成狀態。 || Count behavior depends on state at main-power loss, not only the requested shutdown type.
Base2.4 使用 Unexpected Power Loss Count（UPL）；它是裝置記錄的失電事件，不是 Host 呼叫 Shutdown 的次數。 || Base2.4 UPL counts qualifying power losses, not host shutdown calls.
保存 SMART 計數、CC.SHN、CSTS.SHST 及實際失電時點。 || Preserve count, request, status and actual power-loss time.
一般條件為主電源移除時 SHST 尚未10b；適用的帶外 Ignore Shutdown 情況另看媒體是否仍活躍。 || Ordinary qualification concerns main-power loss before SHST10b, with a separate applicable out-of-band ignore-shutdown case.
先讀基準計數，發出 shutdown，觀察狀態，再於指定時點斷電，恢復後比較。 || Read baseline, request shutdown, observe status and compare after controlled power cycling.
Abrupt 也可能達到 Shutdown Complete 後才失電，因此不能要求每次 Abrupt 都增加 UPL。 || Abrupt shutdown can complete before power loss and need not increment UPL each time.
Normal 要求若尚未完成就掉電，仍可能計數增加；沒有失電的 controller reset 也不能自動算一次。 || Incomplete normal shutdown may qualify, while controller reset without power loss does not automatically count.
比對真正失電前最後狀態，避免使用重啟後 SHST 的值倒推。 || Use pre-loss state rather than post-restart SHST.
先確認主電源是否真的移除，以及當時 SHST 是否已10b。 || First establish actual main-power loss and SHST at that moment.
''')
q(309,"Critical Warning 改變卻沒有 AER，先看哪些設定？ || Which settings explain a warning change without an AER?",'aer_request',['smart','aerfull','feature'],[61,88,196,202],'''
狀態改變與應通知的事件條件不同；警告消失不一定與警告出現有同樣通知要求。 || State transitions and event conditions differ; clearing a warning need not mirror assertion.
SMART 整體警告與 Group-specific 警告要用各自 scope 與設定。 || Aggregate and group-specific warnings use different scopes/settings.
確認 AEC 對應位元、支援能力、是否有 outstanding AER，以及舊同類事件是否尚未確認。 || Check support/enables, pending AERs and unacknowledged prior events.
保存變化前後 CW、溫度／spare 等原始值及門檻；不要只保存應用程式的警告文字。 || Preserve warning bits, measured values and thresholds rather than only UI labels.
先確認達到事件條件，再查 AER 是否被其他事件占用或通知被合併，最後檢查相關 Log 的 RAE 讀取。 || Verify qualifying conditions, competing/coalesced events and acknowledgment reads.
已啟用且符合條件的事件，應依該類型排隊與回報規則被處理；不一定每次取樣變動都另完成一筆 AER。 || Qualifying enabled events follow their queuing rules, not one AER per sampled fluctuation.
如果沒有等待中的 AER，不能要求當下就有 CQE；同樣地，不應把未處理 CQE 誤判成 controller 沒通知。 || No pending request means no immediate CQE; unconsumed completions are not missing notifications.
將 CW 時間線、AEC、AER 清單及 RAE 操作放在一起，找出真正缺少的一步。 || Correlate warning, configuration, requests and acknowledgments.
先確認事件發生時的 AEC，而不是事後才讀到的設定。 || First verify AEC at event time.
''')
q(310,"PEL 事件排列與實際時間不同，如何驗證？ || How is apparent PEL event-order mismatch investigated?",'pel_query',['pelcontext','nvmpel','timestamp'],[213,214,215,216],'''
事件在 Log 的排列、Header timestamp 與操作實際先後是三種不同資訊。 || Log order, event timestamp and real operation order are distinct.
PEL 為 subsystem 範圍，多個 controller 的事件可能交錯，也可能受供應商允許的排序影響。 || Subsystem PEL can interleave controllers and permits defined vendor ordering.
查目前報告 context、Generation Number 與 Timestamp Origin／SYNC。 || Inspect reporting context, generation and clock origin/synchronization.
Timestamp 可因 Host Set、reset 或 saved-value 恢復而跳變；不能把它一律當嚴格遞增序號。 || Host changes and restoration can move timestamps, so they are not universal monotonic sequence numbers.
先在同一 context 讀完整事件，依 EHL／EL 正確走訪，再用 Timestamp Change 與 Reset 事件解釋時間變化。 || Read one consistent context, parse lengths and account for clock-change/reset events.
規範建議新到舊排列，但允許供應商定義的事件順序；測試不能把 should 改成絕對排序要求。 || Newest-first is recommended with vendor-defined ordering allowed, not an unconditional mandate.
若分段讀取混用不同 context，或把 EL 不含 vendor bytes 來算，可能產生假的亂序或壞事件。 || Mixed contexts and incorrect event-length accounting can create false disorder.
用 Host 單調時間保存提交與完成，作為比對線索，但不要求它與未同步的裝置時計完全相等。 || Use a host monotonic timeline as evidence without equating unsynchronized clocks.
先確認是否讀了同一份 context 與正確事件邊界。 || First verify context and event boundaries.
''')
q(311,"CFS=1 卻缺少錯誤資訊，還能查什麼？ || What evidence remains when CFS is set with little diagnostic information?",'reset_review',['cc','ready','error','smart','pelcontext','virtual','commrecovery'],[6,105,117],'''
Fatal 狀態可能讓正常查詢也失敗；缺少 Log 不表示 CFS 不合理，也不代表應持續送更多命令。 || Fatal conditions may break diagnostics; absent logs do not invalidate CFS or justify unlimited further commands.
先判斷這是一般 controller，還是正處 Offline 的 secondary；後者也會設定 CFS。 || Distinguish fatal failure from a secondary controller’s Offline state.
保存 CC、CSTS、CAP、VS、可存取的設定資訊與近期管理操作。 || Preserve accessible controller state, capabilities and recent management history.
若通道仍允許，讀 Error、SMART、PEL 或先前已存在的 Telemetry；不保證每個 CFS 原因都有專用可讀紀錄。 || Obtain available diagnostics without assuming every CFS cause has a readable dedicated record.
先留存最小原始證據，再依裝置可用狀態做 reset 與恢復，之後補查持續性紀錄。 || Preserve evidence before reset/recovery, then query surviving records.
恢復後重新初始化及探索，確認 CFS 不再阻止服務；舊命令結果仍需按中斷的不確定性處理。 || Reinitialize and verify recovery while retaining uncertainty about interrupted commands.
若 MMIO 無法可靠讀取，就不能把全1或預設值直接解析成真實 NVMe 狀態。 || Unreliable/all-ones reads are not automatically valid NVMe state.
分開 controller 回報、Host timeout 與通訊失效的證據，避免將其中一項代替全部原因。 || Separate device status, host timeout and communication-failure evidence.
先確認 controller 角色與目前 Register 讀取是否可信。 || First establish role and register-read validity.
''')
q(312,"Abort 後看見兩次 Completion，如何判斷是否重複？ || How are two observed completions after Abort classified?",'recovery',['abort','cqe','status'],[107,110,112],'''
Abort 命令與目標命令各自有完成結果，所以總共兩筆 CQE 可以正常；真正要檢查的是目標命令是否被完成兩次。 || Abort and its target each complete; two total CQEs can be normal, unlike duplicate target completion.
使用 controller、SQID、CID 與 queue 使用期間識別每筆命令。 || Identify commands by endpoint, SQID/CID and queue lifetime.
保存 Abort 指定的 SQID／CID、Abort 自己的 CID 及 CQE.DW0.IANP。 || Record target identity, Abort’s own identity and IANP.
IANP=0 表示 Abort 已達成規定的立即中止效果，但目標命令仍須依其完成規則結束，不能因此省略目標命令的 CQE。IANP=1 則表示沒有取得這項立即效果，目標命令之後仍可能正常完成。 || IANP semantics do not erase the target’s completion, and IANP1 permits later normal completion.
先分出 Admin Abort CQE 與原 I/O CQE，再檢查 Host 是否因 Phase 或 Head 錯誤讀了同一筆兩次。 || Separate Abort and target CQEs, then exclude host double-consumption.
正常情況可以是一筆 Abort CQE 加上一筆目標命令 CQE，Host 應將兩者分別對回各自的命令。目標命令可能已經修改部分資料，因此看到 Abort 完成後，不能直接假設原命令完全沒執行而原樣重送。 || Handle one completion for each command without assuming the target had no effects.
若已排除 Host 重複讀取同一 CQE，也確認 CID 沒有重用，controller 卻仍對同一次提交的目標命令產生兩筆有效 CQE，才是同一命令被完成兩次的問題。 || Two genuine completions for the same target in one lifetime violate single-completion tracking.
CID 重用與 CQ 繞回必須排除，不能只憑兩張截圖顯示相同 CID 就判重複。 || Exclude CID reuse and CQ wrap before declaring duplicates.
先檢查兩筆 CQE 的 SQID／CID，哪一筆其實屬於 Abort。 || First identify which completion belongs to Abort itself.
''')
q(313,"Delete 完成後仍存取 Queue Memory，有何問題？ || What is wrong with queue-memory access after completed deletion?",'recovery',['delete','create','retirement'],[19,227,295],'''
Queue 記憶體回收以完成的生命週期為界；越過界線的存取可能破壞已重新分配給其他用途的資料。 || Access after the queue lifetime can corrupt memory already reused elsewhere.
先限定是被刪除 SQ／CQ 本身，還是其他仍有效命令的 buffer；兩者不能混為一談。 || Distinguish deleted queue memory from buffers belonging to other live commands.
保存 Delete 的目標 QID、成功 CQE 與 queue 記憶體位址範圍。 || Preserve target QID, successful deletion completion and memory range.
刪 SQ 與刪 CQ 的依賴及完成要求不同；提交 Delete 不代表已成功結束使用。 || Submission is not successful deletion, and SQ/CQ dependencies differ.
先等刪除成功，再判斷觀察到的存取是否確實來自該 queue，排除位址被新 queue 合法重用。 || Check accesses after success and exclude legitimate address reuse by another queue.
成功回收後，controller 不應再把該範圍當成已刪除 queue 使用。 || After retirement, the controller must not continue using it as the deleted queue.
若仍有這類存取，可能覆寫 Host 資料、使用錯誤命令或產生無法關聯完成，不能以一般 timeout 掩蓋。 || Such access can corrupt host data or produce invalid command/completion behavior.
保留位址重用時間與新舊 QID 對照；只有位址相同仍不足以證明舊 queue 在存取。 || Preserve reuse timing and queue identities; address equality alone is insufficient.
先確認成功 Delete CQE 已經完成，而非命令還在 outstanding。 || First establish successful deletion completion.
''')
q(314,"Reset 後讀到舊 CQE，如何處理？ || How should a CQE from before reset be handled?",'recovery',['reset','cqe','pciereset','commrecovery'],[9,21,115,179],'''
舊記憶體殘留與 reset 完成後新發出的非法舊完成，是兩種不同問題。 || Residual memory differs from a newly posted stale completion after reset.
Reset 結束受影響 queue 的舊使用期間，新 queue 即使沿用位址與 QID 也屬於新的期間。 || Reset ends old queue lifetimes even when addresses and identifiers are reused.
查 reset 來源、RDY 變化、CQ 初始化與 Host 期待的 Phase。 || Inspect reset source, readiness transitions, CQ initialization and expected phase.
Host 重建 outstanding map，將舊命令與新命令分開；不能用相同 CID 自動配到新請求。 || Rebuild command tracking without associating an old CID with a new request.
先完成 reset 與記憶體初始化，再啟用新 queue；只處理新使用期間中有效的 CQE。 || Finish reset and initialize memory before accepting valid new-lifetime completions.
殘留的舊 CQE 不作正常新完成處理；中斷前操作是否已修改媒體，另用操作結果與恢復規則判斷。 || Ignore stale completions while separately resolving possible prior media effects.
如果 controller 在重設完成後仍主動寫入舊 queue，需按生命週期違規調查；單純殘留 bytes 不足以證明它做了這件事。 || New writes to a retired queue require investigation, unlike passive residual bytes.
用記憶體初始化前後與寫入時點分辨殘留、Host 重複處理及真正晚到的存取。 || Correlate initialization and write timing to distinguish stale storage from late access.
先檢查新 queue 的 Phase 與命令追蹤是否重新初始化。 || First verify phase and command-tracking initialization.
''')
q(315,"Detach 後 Namespace Command 仍成功，何時合理？ || When can command success after detach be reasonable?",'namespace_op',['nsattach','idlist','status'],[164,165],'''
「接受進 SQ」不等於成功完成；也不是所有帶 NSID 的命令都要求 namespace 已附加。 || Submission acceptance is not successful execution, and some queries can address allocated inactive namespaces.
Detach 影響指定 controller 的 attachment，其他仍 attached 的 controller 可以保留存取。 || Detach affects selected endpoints, not every attached path.
讀該 controller 的 Active List 與 namespace 的 Attached Controller List，確認操作真的完成。 || Verify completed detach through both views.
分清一般 I/O、allocated-namespace Identify 與其他有特殊 NSID 規則的管理命令。 || Distinguish ordinary I/O from allocated-namespace queries and special management commands.
先等 Detach 成功，再送全新的命令到被移除的路徑；不要拿 Detach 前已完成的 CQE 來比較。 || Submit a new command after successful detach on the detached endpoint.
另一條仍附加路徑的 I/O 成功可以正常；查 allocated 資料也可能合法。 || Success on another attached path or an allowed allocated query can be normal.
對已 inactive namespace 的一般適用命令，若無例外應回 Invalid Field；invalid NSID 則是不同條件的 Invalid Namespace or Format。 || Applicable inactive-namespace commands require Invalid Field absent an exception, distinct from invalid-NSID status.
Outstanding 命令依 Detach 與各命令規則處理，測試要分開操作前後提交的命令。 || Separate outstanding and newly submitted commands when assessing detach effects.
先確認命令送到哪台 controller，以及命令種類是否真的需要 active namespace。 || First check endpoint and active-namespace requirement.
''')
q(316,"Lockdown 後仍可操作，如何確認是否漏鎖？ || How is apparent Lockdown bypass investigated?",'lockdown_op',['lockdown','locklog','lockpersist'],[242,243,244,245],'''
Lockdown 指定介面、controller 範圍及命令或 Feature；只符合其中一項不代表必須被禁止。 || A prohibition matches interface, controller scope and command/feature target together.
CSEL、CNTLID、IFC 與 SCP 共同決定目標，不能只記 opcode。 || Scope selectors jointly define the target, not opcode alone.
先讀 Lockdown 支援與適用的目前禁止清單，使用相同 UUID、介面及 controller 選擇。 || Read supported/current prohibitions under matching selectors.
SCP 指 Feature 時限制 Set Features，不自動禁止 Get；增強 FFFFh 彙整的 ACNTL=0 也不代表無人受限制。 || Feature scope prohibits Set, not automatically Get; enhanced aggregate ACNTL0 is not no prohibition.
確認 Lockdown 成功後，對完全符合 selector 的目標重試；同時設一個應允許的對照命令。 || Test an exact matching target plus an allowed control after successful Lockdown.
匹配的被禁止 Admin command 應回 Command Prohibited by Command and Feature Lockdown（0/23h）。 || A prohibited matching Admin command requires 0/23h.
先排除 Power Cycle 解除、後續允許操作、不同介面或 personality 的明文例外，再判斷執行成功是否矛盾。 || Exclude expiry, later allowance, mismatched interfaces and explicit personality exceptions.
比對 Lockdown CQE、清單與目標命令行為，三者必須使用同一組選擇條件。 || Correlate configuration, inventory and behavior under identical selectors.
先檢查 IFC／CSEL／SCP，而不是只看功能名稱。 || First inspect interface, controller scope and command-versus-feature selection.
''')
q(317,"Power State 恢復太慢，如何量測才公平？ || How is excessive power-state recovery latency measured correctly?",'power_config',['powerdetail','psd','power','smart'],[188,190,192,194],'''
命令總延遲包含退出狀態、進入目標狀態與實際工作，不能全部算成 EXLAT。 || Command latency includes exit, possible entry and execution, not only EXLAT.
先確認來源與目標 Power State，以及當時是否受 thermal management 等其他條件影響。 || Establish source/target states and concurrent thermal constraints.
查 PSD 的 NOPS、ENLAT、EXLAT，及 Power Management／APST 設定。 || Read state types, entry/exit latencies and selected policies.
APST.ITPT 是閒置等待時間，單位ms；ENLAT／EXLAT 是轉換延遲，單位µs，不能相加前忘記換算。 || ITPT is idle time in milliseconds; entry/exit latencies are in microseconds.
記錄最後一次活動、進入省電狀態、觸發退出及恢復處理命令的時間。量測轉換延遲時，應將命令本身的執行時間分開，避免把媒體讀取時間也算成退出省電狀態的時間。 || Separate idle, transition trigger, recovery and command execution timing.
例如從非工作狀態回到前一工作狀態，按相關退出與進入延遲判斷，而不是把完整 Read 完成時間等同 EXLAT。 || Assess relevant transitions rather than equating full read latency with EXLAT.
若只有 CQE 時間而無法分辨內部狀態切換，證據不足以單獨證明 EXLAT 違規。 || CQE timing alone may not isolate an exit-latency violation.
用同 workload 的工作狀態基準、溫度與設定快照做比較，說明仍無法排除的因素。 || Compare an operational baseline with matching workload, temperature and settings.
先確認單位及計時起點。 || First verify units and timing origin.
''')
q(318,"如何比較三種 Reset 對同一功能的影響？ || How are three reset types compared for one feature?",'reset_review',['reset','pciereset','feature','setfeat','shutdownfull'],[174,178,180],'''
要判斷差異是否由 reset 引起，每次測試都應從相同的初始狀態開始，再分別套用不同 reset。若連測試前的設定都不同，就無法把觀察到的差異歸因於 reset 類型。 || Compare matched initial states under distinct reset mechanisms.
Controller Level Reset、Subsystem Reset 與 Power Cycle 的範圍及持續性條件不同。 || Reset coverage and persistence conditions differ across the three cases.
先選一個明確功能，保存其能力、Current／Saved、Log 與涉及的其他 controllers。 || Select one function and capture support, state and affected endpoints.
分欄記錄 Register、queue、設定值、操作是否持續及儲存資料；不要把全部寫成單一「保留／不保留」。 || Track registers, queues, settings, ongoing operation and stored data separately.
每次恢復相同初始條件，只改 reset 類型；完成後先恢復查詢通道，再檢查各欄。 || Reset from matched baselines and restore query access before comparison.
例如 Extended Self-test 可在 CLR 後持續，但 I/O queues 仍失效；兩個結果可以同時成立。 || Extended self-test persistence and I/O queue invalidation can coexist under CLR.
CC.EN reset 的 Register 保留例外不能套用到所有 CLR；同樣，Subsystem Reset 不是 Restore Defaults。 || CC.EN-specific register exceptions do not cover all CLR, and subsystem reset is not factory restoration.
每個差異都連到明確規則，未定義的行為標示證據界線，不猜一個統一答案。 || Tie differences to explicit rules and retain limits where behavior is unspecified.
先把 reset 的實際觸發方式寫清楚。 || First identify the actual reset trigger.
''')
q(319,"如何判斷操作真正影響誰？ || How is an operation’s real scope established?",'error_review',['commandseffects','idctrl','idlist','capacitymodel'],[2,47,81,275],'''
命令從某個 Admin Queue 送入，不代表效果只限於該 controller。 || Submission through one Admin Queue does not limit effects to that controller.
作用範圍可能是 namespace、controller、Group、Domain 或 subsystem，需由命令與欄位共同決定。 || Commands and selectors determine namespace, controller, group, domain or subsystem effects.
查命令欄位、Feature scope、Identify 的能力及 Commands Supported and Effects 的相關資訊。 || Inspect command selectors, feature scope, capabilities and command effects.
NSID=FFFFFFFFh 的意思因命令而異；Effects 未回報某 scope 也不能取代命令的明文定義。 || Broadcast semantics are command-specific and effects metadata does not replace explicit scope definitions.
列出提交端、目標與共用資源，再選一個範圍內及一個範圍外對照物件觀察。 || Identify endpoint, targets and shared resources, then observe inside/outside controls.
例如 Detach 指定一台 controller，而共享 namespace 資料並未因此複製或刪除。 || Detaching one endpoint does not duplicate or delete shared namespace data.
對範圍外物件的變化，先排除共用資源與同時發生的另一操作，再判是否超出規範。 || Exclude shared-resource and concurrent-operation causes before alleging out-of-scope effects.
比較使用相同物件 ID 與穩定時點；不同 controller 的 Active List 本來就可能不同。 || Compare matching entities and times; active inventories can legitimately differ by endpoint.
先讀該命令對 selector 的定義，特別是0與FFFFFFFFh。 || First read special selector values for that specific command.
''')
q(320,"如何把所有介面串成一次完整的符合性驗證？ || How are the interfaces combined into one conformance investigation?",'error_review',['idctrl','commandseffects','feature','getlog','aerfull','status','error','pelcontext'],[297,299,300,301,302,318,319],'''
完整驗證要形成可追溯的證據鏈：宣告、前提、操作、結果、通知、紀錄及持續性各自有依據。 || Build traceable evidence across advertisement, prerequisites, operation, result, notice, record and persistence.
先界定功能與受影響物件，避免一次測多個功能而無法分清哪個造成差異。 || Define one function and its scope before testing multiple interacting mechanisms.
保存 Identify、Supported／Effects Logs 與需要的 Feature 設定作為基準。 || Capture discovery, effects and relevant configuration as the baseline.
保存原命令及 selector、CQE、相關 Log、AER 與 PEL；不適用或不支援的介面明確標記理由。 || Record request, completion and applicable logs/events, explaining inapplicable or unsupported interfaces.
先做合法正常案例，再一次只改一個非法參數或順序；最後從相同基準分別驗證 reset 與 Power Cycle。 || Run a valid case, isolate invalid conditions and then test persistence from matched baselines.
結論能指出哪個規範要求被哪些觀察支持，以及哪些資料仍不足以判斷。 || Conclusions identify supported requirements and remaining evidence limitations.
禁止把 may 當 shall、把未定義行為指定為固定 Status，或用「命令成功」省略背景操作最終結果。 || Do not turn permissions into mandates, invent statuses for undefined behavior or equate acceptance with background completion.
用一張時間線串起原始資料，保留規格章節、Figure 與 PDF 頁碼，讓另一位讀者能重走推理。 || Link raw evidence on a timeline with source sections, figures and PDF pages.
先寫出這次要驗證的一條具體規範要求，再決定需要哪些證據。 || First state one precise requirement and then select the evidence needed to test it.
''')
