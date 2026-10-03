"""Approved Q69–Q320 authoring support. No generated placeholder questions."""
from scripts.nvme_qa_model import COMMON, REFS, add, pair

REFS.update({
 'firmware':'B|3.11–3.11.1, 5.2.9–5.2.10|161-164,228-232|187–193',
 'fwpel':'B|5.2.13.1.14.2.2, 5.2.13.1.14.2.4|278-281|238, 240–241',
 'boot':'B|8.1.3–8.1.3.3.3|612-618|679–683',
 'bootreg':'B|3.1.4 (BPINFO, BPRSEL, BPMBL)|95-96|49–51',
 'bootlog':'B|5.2.13.1.21|309-310|279–280',
 'bootprotect':'B|5.2.30.1.39|538-540|542',
 'selftest':'B|5.2.6, 8.1.8|225-227,640-642|176–180, 700–701',
 'nvmselftest':'N|4.1.4.3|75-76|111',
 'nvmcreate':'N|4.1.5.8, 4.1.6, 5.8|108,110-113,162-163|132–134',
 'nsattach':'B|5.2.24–5.2.25, 8.1.17–8.1.17.2|470-474,686-689|442–450',
 'nspelevent':'B|5.2.13.1.14.2.6|284-285|247',
 'getlog':'B|5.2.13–5.2.13.1.1|238-244|203–211',
 'smart':'B|5.2.13.1.3|246-251|213–214',
 'fwlog':'B|5.2.13.1.4|251-252|215',
 'changedlog':'B|5.2.13.1.5|252|',
 'commandseffects':'B|5.2.13.1.6|252-255|216–217',
 'dstlog':'B|5.2.13.1.7|255-258|218–219',
 'telemetrylog':'B|5.2.13.1.8–5.2.13.1.9|258-263|220–223',
})

# Topic profiles are explicit shared answers. Individual exceptions override them.
COMMON['log_query']={
 9:pair("""讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。RAE=1 保留事件，讀取失敗也必須保留。Immediate 與 One-Shot 事件另有清除方式，不能全部套用讀 Log 確認。 || Reading a log does not itself require a new event. A successful RAE=0 read may acknowledge its event; RAE=1 and unsuccessful reads retain it. Immediate and One-Shot events have separate clearing rules."""),
 10:pair("""Get Log Page 回傳指定 Log 的資料。某些清單會因讀取而清除已回報的變更，某些事件也受 RAE 影響；讀取前先保存需要比對的狀態。讀取成功本身不要求新增 Error Information，失敗時則依 CQE 與錯誤記錄規則判斷。 || Get Log Page returns the selected data. Reads can clear reported changes or acknowledge events, depending on the log and RAE, so preserve comparison evidence first. A successful read does not require an error entry; failed reads follow CQE and error-log rules."""),
 11:pair("""Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。即使讀取的是 PEL，也不表示這次讀取會新增同類事件；只有另行發生且符合支援與記錄條件的事件，才依規則記錄。 || Get Log Page is not a per-read PEL audit trail. Reading PEL does not create another such event; separately occurring events follow their supported logging conditions."""),
 12:pair("""Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。Log 內容是否保留則是另一個問題：Error Information entries 建議清除，但 Error Count 保留；SMART 的累計資訊與 PEL 依各欄位規則持續，不能隨查詢一起當成遺失。 || Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. Content retention is separate: Error Information entries should clear but Error Count persists; SMART cumulative information and PEL follow their field-specific persistence rules."""),
 13:pair("""NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。它不等於恢復出廠設定；Figure 209 的 Restore to Default Content 欄描述製造預設內容的恢復，不能拿來當一般 Reset 的保留表。 || After subsystem reset, recover query access on affected controllers and re-read the logs. This is not restoration of manufacturing defaults; Figure 209’s Restore to Default Content column is not an ordinary reset-retention table."""),
 14:pair("""Power Cycle 後重新提交查詢。SMART 的生命週期資訊及 PEL 具有跨斷電的保留規則；Error Information entries 則建議清除，但其累計 Error Count 仍保留。目前溫度、正在執行的操作及回報 context 必須依各自定義重新判讀，不能把所有 bytes 當成固定不變。 || Reissue the query after a power cycle. SMART lifetime information and PEL have persistent content; Error Information entries should clear while the cumulative Error Count persists. Reassess current temperature, active operations and reporting contexts under their own rules rather than expecting every byte to remain fixed."""),
 15:pair("""查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。controller、namespace、domain 與 subsystem 的資料範圍也不同；多個 Host 共同查詢時，應記錄由誰讀取及何時確認，避免誤以為另一端沒有發生事件。 || Queries do not write namespace user data, but some reads acknowledge events or clear reported lists. Logs have controller, namespace, domain or subsystem scopes; track readers and acknowledgment times when several hosts share the view.""")}

def question(number,title,profile,refs,body,overrides=None):
    # The existing helper authors nine topic-specific answers; explicit profiles
    # replace common retention/event answers after the helper returns.
    from scripts.nvme_qa_model import QUESTIONS
    add(number,title,'command',refs,body)
    q=QUESTIONS[-1];q['profile']=profile
    q['answers'].update(COMMON[profile])
    if overrides:q['answers'].update({k:pair(v) for k,v in overrides.items()})

REFS['aerfull']='B|5.2.2 (PCIe-applicable events)|209-217|150–160'
REFS['abort']='B|5.2.1|207-208|147–149'
REFS['pciereset']='P|3.3|11-12|'
REFS['shutdownfull']='B|3.6–3.6.1 (memory-based scope and shutdown)|139-141|85'
COMMON['reset_review']={**COMMON['register'],**COMMON['queue'],15:pair("""Controller Reset 以該 controller 為範圍；Subsystem Reset 在單 domain 涵蓋全部，multi-domain 則依實作涵蓋一個或全部 domains。Shutdown 的可斷電範圍還須看 CAP.CPS；共享 namespace 的其他路徑不應被當成獨立資料副本。 || Controller Reset targets one controller; subsystem reset covers one/all domains as defined for the implementation. Power-off readiness also depends on CAP.CPS; shared paths are not independent data copies.""")}
REFS['commrecovery']='B|9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)|851-854|'
COMMON['error_review']={**COMMON['command'],
 12:pair("""Controller Level Reset 會中止未完成的命令並重設 queue 狀態；Host 不應繼續等待舊命令的 CQE。這不代表命令先前造成的資料修改已回復，也不表示背景管理操作一定停止。先保存可取得的錯誤證據，再於恢復後依該操作的狀態或 Log 確認結果。Error Information entries 建議清除，但 Error Count 保留，因此不能用重設後沒有 entry 來否定重設前的錯誤。 || Controller Level Reset aborts outstanding commands and resets queues; do not wait for old CQEs. It does not roll back prior changes or universally stop background operations. Preserve available evidence, then inspect operation-specific state after recovery. Error Information entries should clear while Error Count persists, so an absent post-reset entry does not disprove an earlier error."""),
 13:pair("""NVM Subsystem Reset 使受影響的 controllers 執行 Controller Level Reset，必須先恢復查詢通道，才能繼續檢查。它不是恢復出廠設定，也不能保證故障原因已排除。分別核對原操作的結果、目前設定及仍保留的 Log，並確認其他共用資源的 controllers 是否同時受到重設。 || A subsystem reset applies Controller Level Reset to affected controllers. Restore query access before inspection; it is neither factory restoration nor proof that the fault is resolved. Verify operation results, current settings, retained logs and the reset coverage of controllers sharing resources."""),
 14:pair("""Power Cycle 後，舊 queue 與未完成命令的追蹤關係不能沿用；Host 需重新初始化，再查實際資料與操作狀態。SMART 累計資訊及 PEL 的持續性規則，與錯誤命令是否成功是不同問題。Error Information entries 建議清除而 Error Count 保留；因此要把斷電前保存的 SQE、CQE 及 Log，與重新上電後的觀察一起比對。 || After a power cycle, rebuild queues and command tracking before checking actual data and operation state. SMART/PEL persistence does not establish command success. Error entries should clear but Error Count persists, so correlate pre-power-loss requests, completions and logs with fresh observations."""),
 15:pair("""單筆命令失敗不代表其他命令、namespace 或 controller 都失效。先區分參數錯誤、queue 故障與 controller 故障；只有共享資源或狀態也受影響時，才擴大處理範圍。 || One command failure does not establish failure of other commands, namespaces or controllers. Distinguish parameter, queue and controller failures, broadening recovery when shared resources or state are affected.""")}
COMMON['recovery']={**COMMON['command'], **COMMON['queue']}
REFS.update({
 'format':'B|5.1.1, 5.2.11|204-205,232-235|144, 194–196',
 'nvmformat':'N|4.1.2|62-63|91',
 'sanitizecmd':'B|5.2.26–5.2.27|474-480|451–455',
 'sanitizelog':'B|5.2.13.1.38|339-346|312',
 'sanitizestate':'B|8.1.27.1–8.1.27.5|737-758|770–779',
 'sanitizerestrict':'B|5.1.1–5.1.2 (PCIe commands)|204-207|144–146',
 'sanitizeconfig':'B|5.2.30.1.16|503-504|492',
 'nvmsanitize':'N|4.1.7, 5.12|113,173-175|200–201',
 'formatpel':'B|5.2.13.1.14.2.7–5.2.13.1.14.2.8|285-287|248–249',
 'sanitizepel':'B|5.2.13.1.14.2.9–5.2.13.1.14.2.10|287-288|250–251',
})
COMMON['format_op']={**COMMON['command'],
 9:pair("""Format 改變 namespace 屬性時，依支援與通知設定回報對應 Namespace Attribute Changed，並更新 Changed Namespace 清單；FPI 僅由 0 變非 0 或由非 0 變 0 時才符合相關變更通知條件，不是每個百分比都通知。 || Format attribute changes follow namespace-change support/configuration and changed-list rules. Relevant FPI notifications concern zero/nonzero transitions, not every percentage update."""),
 10:pair("""成功後重新讀 Identify Namespace 的格式與容量，並查看 Changed Namespace 清單。錯誤時依 CQE.More 讀 Error Information；不能以一筆成功的 Get Log Page 取代 Format 本身的完成結果。 || Re-read namespace format/capacity and changed lists after success. For errors use CQE.More and Error Information; a successful Get Log does not substitute for Format completion."""),
 11:pair("""支援 PEL 與對應事件時，Format Start（07h）保存要求，Format Completion（08h）保存操作結果。Completion 的 FNVMS 與 INFO 必須一起讀；若原 Format 沒有 CQE，INFO 可為 0，不能直接解成格式化成功。 || With supported PEL events, Format Start07h records the request and Completion08h the outcome. Read FNVMS with INFO; INFO can be zero when no Format CQE was reported and does not alone prove success."""),
 12:pair("""Controller Reset 結束舊命令通道，不能沿用原 Format 的 outstanding 狀態或等待舊 CQE。恢復後重新讀格式、FPI 與可取得的 Format Completion Event，確認媒體實際狀態；Reset 本身既不證明格式化成功，也不保證回復舊格式。 || Controller Reset ends the old command channel. Re-read format, FPI and available Format Completion events after recovery; reset proves neither format success nor rollback."""),
 13:pair("""NVM Subsystem Reset 後先恢復通道，再逐一查詢原 Format 範圍內的 namespaces。不能只查提交命令的 controller，就假設所有受影響 namespace 都已完成或恢復。 || After subsystem reset, recover access and inspect namespaces in the original format scope; one controller’s recovery does not establish all namespace outcomes."""),
 14:pair("""Power Cycle 中斷時若沒有可信的 Format 成功完成，Host 應重新確認目前格式與可用性，必要時重新執行符合當前狀態的 Format。先前資料可能已被破壞，不能因命令沒有回成功就假設資料仍在。 || Without trustworthy successful completion before power interruption, reassess format and usability and, if needed, perform a valid new Format. Missing success does not imply old data survived."""),
 15:pair("""依 SES 選擇 FNA.FNS 或 FNA.SENS，再與 NSID 一起決定範圍。同一共享 namespace 可由其他 controller 存取，因此需要協調相關 I/O；提交到某個 controller，不表示只影響它自己的資料。 || Select FNA.FNS or SENS using SES, then combine it with NSID. Coordinate other access paths to shared namespaces; submission to one controller does not imply controller-local data impact.""")}
COMMON['sanitize_op']={**COMMON['command'],
 9:pair("""依狀態轉移回報 Sanitize Operation Completed、Completed With Unexpected Deallocation 或 Entered Media Verification State，AER 的 LID=81h。由 Admin SQ 啟動時，僅啟動該操作的 controller 回報這次通知；仍須查看 Log 分辨成功、失敗或驗證階段。 || State transitions report completed, unexpected-deallocation completion or media-verification entry with LID81h. For Admin-SQ initiation, only the initiating controller reports the event; inspect the log for actual outcome."""),
 10:pair("""Sanitize Status 在啟動 CQE 張貼前更新，之後隨狀態轉移更新；它跨 Reset 與斷電保留。用相同目標的 SOS、SANS、SPROG、SCDW10 及 GDE／NDE 比對，不以背景失敗要求原啟動命令再回第二筆 CQE。 || Sanitize Status updates before the initiating CQE and on transitions, persisting across resets/power. Match target, SOS, SANS, SPROG, SCDW10 and GDE/NDE; background failure does not require a second initiation CQE."""),
 11:pair("""支援對應 PEL 事件時，進入 Processing 記錄 Sanitize Start（09h）；進入 Idle、Restricted Failure 或 Unrestricted Failure 記錄 Completion（0Ah）。Completion 也包含失敗，事件 NSID 可用來分辨 subsystem 與 namespace 目標。 || Supported PEL logging records Start09h on entering processing and Completion0Ah on entering Idle or either failure state. Completion includes failures; NSID distinguishes subsystem and namespace targets."""),
 12:pair("""Sanitize 背景操作不因 Controller Level Reset 而中止。Host 重新建立查詢通道後讀同一目標的 LID81h。另需分辨 Reset 來源：傳輸層 Reset 等條件可能取消 Media Verification，使 MVCNCLD 設為 1，而不是取消整個清除操作。 || Background sanitization continues through Controller Level Reset. Re-read target LID81h after recovery. Some reset sources cancel media verification and set MVCNCLD without cancelling the entire sanitize operation."""),
 13:pair("""NVM Subsystem Reset 也不提供中止 Sanitize 的方法。操作的狀態與 Log 需要保留；如果原本要求 Media Verification，還要檢查 MVCNCLD 及後續 deallocation 階段。 || Subsystem reset does not abort sanitization. Preserve operation/log state and check MVCNCLD and post-verification deallocation when verification was requested."""),
 14:pair("""斷電期間無法進行媒體處理，但重新供電後 Sanitize 仍須依保存的狀態繼續，不可當成從未開始。恢復後查看 SOS／SANS 與進度，不能只見 SPROG=FFFFh 就宣告成功。 || Processing cannot occur without power, but sanitization continues from retained state after power returns. Inspect SOS/SANS and progress; SPROG=FFFFh alone is not success."""),
 15:pair("""Subsystem Sanitize 限制整個 subsystem 的相關存取；Namespace Sanitize 則針對指定 namespace，但所有可存取它的 controller 都受限制。共享韌體更新等操作另有全域限制，不能只因另一 namespace 的資料不被清除，就推論完全沒有影響。 || Subsystem sanitization restricts subsystem access; namespace sanitization targets one namespace across its controllers. Shared operations such as firmware update have additional restrictions even when other namespace data is not erased.""")}
COMMON['firmware_op']={**COMMON['command'],
 9:pair("""開始不經 Reset 的韌體啟用時，受影響 controller 在 Firmware Activation Notices 啟用下回報 Firmware Activation Starting。載入失敗另有 Firmware Image Load Error；Download 每一段成功不會各自觸發啟用通知。 || Starting reset-free activation triggers Firmware Activation Starting on affected controllers when notices are enabled. Load failure has a separate error event; each successful download segment does not trigger activation."""),
 10:pair("""用 Firmware Slot Information 區分目前 Active 與下次 Reset 預定 Active，再用 Identify.FR 確認真正執行的版本。失敗時另依 CQE.More 查 Error Information；slot 中已有新映像，不表示它已執行。 || Distinguish active and next-reset slots with Firmware Slot Information and confirm running revision through Identify.FR. Use More for error details; stored does not mean executing."""),
 11:pair("""支援 PEL 時，Firmware Commit 完成記錄 Event02h，含舊版本、要求啟用的新版本、CA、slot 與 Status。NFR 是要求的新版本，不是啟用成功證明；Reset Event 的 FA／FREV 可補充實際啟用結果。 || PEL Commit02h records old/requested revisions, action, slot and status. Requested NFR is not proof of activation; Reset-event FA/FREV provide outcome evidence."""),
 12:pair("""Download 後、Commit 完成前若發生 Controller Level Reset，已下載的暫存映像部分必須丟棄。已完成 Commit 的 slot 與待啟用安排則依 CA 及回傳的必要 Reset 類型判斷；不能只因任何 Reset 就假設新映像會啟用。 || A CLR between download and completed Commit discards staged portions. Committed slots/pending activation follow CA and required reset type; not every reset activates the image."""),
 13:pair("""Subsystem Reset 會影響其涵蓋的 controllers，並可滿足明確要求此 Reset 的待啟用映像。恢復後重新查 FR、slot 及能力；未完成 Commit 的暫存下載不能沿用。 || Subsystem reset affects its covered controllers and satisfies a required subsystem-reset activation. Recheck revision, slots and capabilities; uncommitted staging cannot be reused."""),
 14:pair("""若在要求啟用的 Commit 尚未完成時進入 D3cold，恢復後可使用原映像或該次新映像，必須實際查證。已完成下載但尚未完成 Commit 的暫存部分，不能當成跨斷電保存的有效 slot。 || Entering D3cold during activation Commit can resume with the old or newly activated image; verify it. Uncommitted downloaded portions are not a persistent slot."""),
 15:pair("""同一 domain 的 controllers 共用 firmware slots，該 domain 使用相同映像；單一 domain 時即涵蓋 subsystem。Host 應協調所有受影響存取者，並避免多個更新流程互相重疊。 || Controllers in one domain share slots/image, covering the subsystem in a single-domain system. Coordinate affected accessors and avoid overlapping update sequences.""")}
COMMON['selftest_op']={**COMMON['command'],
 9:pair("""本規格沒有通用的 Device Self-test Completed AER。正常完成應讀 LID06h 確認；測試發現診斷失敗時，另依 Diagnostic Failure 錯誤事件及其回報條件處理。 || There is no generic Device Self-test Completed AER. Read LID06h for normal completion; diagnostic failures separately follow Diagnostic Failure error-event conditions."""),
 10:pair("""短程／延伸測試完成或被中止時，先建立最新 Self-test Result，再將目前操作設為 idle。診斷欄位要先檢查 valid bits；不是每個失敗結果都具有有效 NSID、LBA、SCT 與 SC。 || Short/extended completion or cancellation creates the newest result before returning current operation to idle. Check diagnostic valid bits before NSID/LBA/SCT/SC."""),
 11:pair("""PEL 沒有通用的逐次 Self-test 結果事件；完整測試歷史以 LID06h 為主。若同時發生可記錄的硬體錯誤或 Reset，則是那些事件另行記錄，不可拿來取代 Self-test Result。 || PEL has no generic per-self-test result event; use LID06h. Separately qualifying hardware/reset events do not replace the self-test result."""),
 12:pair("""影響執行 controller 的 Controller Level Reset 必須中止短程測試；延伸測試則必須跨 CLR 保留，並在重設完成後恢復。恢復的 segment 由廠商決定，規範建議只需重做被中斷的最後 segment。 || CLR aborts a short test but an extended test must persist and resume after reset. The resume segment is vendor-specific; implementations should only need to repeat the interrupted last segment."""),
 13:pair("""Subsystem Reset 會對其範圍內的 controller 造成 CLR：短程測試被中止，延伸測試必須恢復。不能把重新建立 Admin Queue 與重新開始整個延伸測試當成同一件事。 || Subsystem reset causes CLR on covered controllers: short tests abort and extended tests resume. Rebuilding Admin Queues is not restarting the entire extended test."""),
 14:pair("""延伸測試必須在電源恢復後繼續；短程測試則不具有這項延續要求。恢復後先讀 DSTOS、進度與最新結果，不能只因 power cycle 就期待兩者都新增 Reset-aborted 結果。 || Extended testing must resume after power restoration; short testing has no such continuation requirement. Read operation/progress/results rather than requiring reset-aborted results for both."""),
 15:pair("""測試由收到命令的 controller 執行，NSID 決定包含哪些 namespace。DSTO.SDSO 決定同時只能有一個測試的限制是在 controller 或 subsystem；即使沒有測試其他 namespace，共享資源仍可能使其他工作變慢。 || The receiving controller runs the test and NSID selects coverage. DSTO.SDSO determines controller/subsystem concurrency scope; shared resources may slow unrelated work.""")}
COMMON['namespace_op']={**COMMON['command'],
 9:pair("""Create／Delete 影響 Allocated List，Attach／Detach 影響指定 controller 的 Active List。依各 controller 的事件支援與 AEC 回報變更；Admin SQ 收到 Delete 的 controller 不回報該次刪除通知，其他受影響且啟用通知的 controller 仍須依規則回報。 || Create/delete affect allocated inventory; attach/detach affect controller active lists. Apply per-controller support/AEC. The Admin Delete recipient does not report its own deletion notice; other eligible controllers do."""),
 10:pair("""使用 Identify 的 Allocated、Active 與 Controller List 確認目前配置；Changed Attached Namespace List04h 與 Changed Allocated Namespace List1Ch 指出曾變更的 NSID，不能代替完整現況。失敗則依 More 與 Error Information 補充欄位處理。 || Identify lists establish current allocation/attachment; changed lists04h/1Ch identify changes rather than complete state. Errors use More and applicable Error Information fields."""),
 11:pair("""支援 PEL 時，Namespace Management 對應的 Change Namespace Event06h 記錄建立／刪除等規定事件。Attach／Detach 不應直接當成 Create／Delete；Write Protection 則依該 Feature 是否支援 Set Feature Event 記錄。 || Supported Change Namespace06h records defined management changes; do not treat attachment as creation/deletion. Write protection follows supported Set Feature-event rules."""),
 12:pair("""已完成的 namespace 配置與 Attach／Detach 跨 Reset 保留；重設的是命令通道，不是自動刪除 namespace。若 Reset 前未收到完成，恢復後須查清單確認結果，不能假設整筆操作必定回復。 || Completed configuration/attachment survives reset; command channels reset without deleting namespaces. For interrupted commands, inspect lists rather than assuming rollback."""),
 13:pair("""Subsystem Reset 不等於 Restore Default Namespace Configuration。恢復後重新探索原 namespace 與附加關係，再建立 I/O queues；多 domain 的實際 Reset 範圍另行確認。 || Subsystem reset is not Restore Default Namespace Configuration. Rediscover persisted namespaces/attachments and rebuild queues, accounting for domain scope."""),
 14:pair("""Power Cycle 後，已完成的 namespace 配置與附加關係仍需保留。Write Protect 與 Permanent Write Protect 保留；Write Protect Until Power Cycle 則在實際 power cycle 轉回未保護，不能把這個例外套到全部配置。 || Completed namespace configuration/attachments persist. Ordinary/permanent write protection persist; until-power-cycle protection clears on a real power cycle, not all configuration."""),
 15:pair("""建立／刪除影響 subsystem 的 namespace inventory；附加清單指定哪些 controllers 改變存取關係。共享 namespace 的保護狀態必須由所有附加的 controllers 執行，不因換路徑而解除。 || Creation/deletion changes inventory and attachment lists select affected controllers. Shared namespace protection applies through all attached controllers.""")}
COMMON['aer_request']={
 9:pair("""AER 的正常用途就是讓 controller 以完成這筆 Request 的方式回報事件。必須分清楚事件本身、通知是否啟用、是否被遮蔽，以及是否還有 Request 可用；送出 AER 不會替 Host 啟用所有選配事件。 || AER reports an event by completing a request. Distinguish the event condition, enablement, masking and available requests; submitting AER does not enable every optional event."""),
 10:pair("""依 AET、AEI、LID 讀取對應 Log；Error 類型指向 Error Information，SMART 類型指向 SMART / Health。AER 成功本身不要求額外新增 Error Information，且即時狀態可能在事件發生後已改變，需保存通知與讀取的時間。 || Use AET, AEI and LID to select the associated log. Error events point to Error Information and SMART events to SMART/Health. A successful AER does not itself require an error entry; current state may have changed since the event, so record both times."""),
 11:pair("""PEL 是否記錄由原始事件決定，不由 AER Request 是否完成決定。先確認該 Persistent Event 受支援且符合記錄條件；不能為每筆 AER 或每次讀取 Log 強制增加一筆 PEL 紀錄。 || PEL logging depends on the underlying event, not on AER completion. Check supported event conditions rather than requiring an entry for every request or acknowledgment."""),
 12:pair("""Controller Reset 會中止尚未完成的 AER，而且這些被重設中止的 Request 不得回傳 CQE。Controller Level Reset 也會清除尚未通知的 pending event；Host 恢復後重新提交 AER，並依各 Log 的保留規則查詢狀態。 || Controller Reset aborts outstanding AERs without CQEs. Controller Level Reset also clears pending notifications. After recovery submit fresh requests and read retained state under each log’s rules."""),
 13:pair("""受 NVM Subsystem Reset 影響的 controller 重新建立 Admin Queue 後，須重新掛入 AER。不要等待舊 Request 的完成；其他 controller 是否同時受影響，要依實際重設涵蓋範圍判斷。 || After subsystem reset, reestablish Admin Queues and AERs on affected controllers. Do not wait for old requests; determine other controllers’ involvement from actual reset coverage."""),
 14:pair("""Power Cycle 後，舊 AER 不是有效 Request。Host 重新初始化後，確認 Asynchronous Event Configuration 恢復成哪個值，再掛入新 Request；保存下來的 Log 歷史不代表舊通知也會全部重新播放。 || Old AERs are invalid after a power cycle. Reinitialize, check the restored asynchronous-event configuration and post new requests. Persistent log history does not imply replay of every old notification."""),
 15:pair("""Request 提交到特定 controller，完成也回到它的 Admin CQ；事件影響範圍則可能是 namespace、domain 或 subsystem。多個 controller 可因同一共享狀態各自回報，不能只靠通知數量推算獨立故障數。 || Requests and completions belong to a controller, while event scope may be a namespace, domain or subsystem. Several controllers can report one shared condition; notification count is not independent-failure count.""")}
