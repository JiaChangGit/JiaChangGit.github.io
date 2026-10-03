"""Q149–156: short and extended tests have different reset semantics."""
from scripts.nvme_qa_extension import question

def q(n,t,b): question(n,t,'selftest_op',['selftest','dstlog','nvmselftest','idctrl','aerfull'],b)

q(149,'如何確認 Device Self-test 支援與可測範圍？ || How are self-test support and coverage established?', '''
Self-test 提供裝置內部的診斷流程，可檢查 controller 與指定媒體，但它不能取代 Host 對資料內容的完整驗證。 || Self-test diagnoses controller and selected media internally; it does not replace complete host data validation.
NSID=0 只測 controller；特定 active NSID 加入該 namespace；FFFFFFFFh 包含開始時此 controller 可存取的全部 attached namespaces。 || NSID0 tests the controller, an active ID includes that namespace andFFFFFFFFh includes namespaces accessible through that controller at start.
Identify.OACS 確認支援，DSTO.SDSO 決定單一測試限制的範圍，EDSTT 提供延伸測試時間。 || OACS establishes support, DSTO.SDSO concurrency scope and EDSTT extended-test duration.
Device Self-test 使用 STC 選操作；Get Log Page LID06h 查目前測試與最近 20 次結果。 || STC selects the test action and LID06h reports current operation and 20 results.
先確認能力與 namespace 狀態，保存舊 Log，再啟動選定測試並追蹤新狀態。 || Establish support/state, preserve the old log, then start and monitor the selected test.
啟動成功表示背景測試已開始；真正通過要看新 Result 的 DSTR=0，而非只看啟動 CQE。 || Initiation success starts background testing; passing requires a new result with DSTR0.
不存在的 NSID 回 Invalid Namespace or Format；已配置但 inactive 的 NSID 回 Invalid Field in Command，這兩種情況不能混寫。 || Invalid NSID uses Invalid Namespace/Format; an inactive NSID uses Invalid Field. Keep the cases distinct.
核對 OACS、實際 STC、NSID 與 Log 的測試代碼，確認啟動的是預期測試。 || Match OACS, STC, target and logged test code.
先確認「不存在」與「存在但未 active」的差別。 || First distinguish an invalid ID from an existing inactive namespace.
''')

q(150,'Short 與 Extended Self-test 有何差別？ || How do short and extended self-tests differ?', '''
兩者提供不同深度與時間的診斷；實際 segments 與測試內容由廠商設計，規格中的 RAM／媒體檢查圖只是教學示例。 || They offer different diagnostic duration/depth; segment contents are vendor-defined and the illustrated RAM/media checks are informative examples.
兩者都依 NSID 選範圍，且可能因共享資源影響其他工作的效能。 || Both use NSID coverage and can affect other work through shared resources.
EDSTT 是延伸測試時間資訊；短程測試建議在 2 分鐘內完成。這些 should 不應提升為所有情況的硬性 shall。 || EDSTT reports extended duration; short tests should finish within two minutes. Preserve the strength of these recommendations.
STC=1 啟動 Short，2 啟動 Extended；Log 的 DSTOS 表示正在執行哪種操作，DSTCS 表示完成百分比。 || STC1/2 selects short/extended; DSTOS identifies the current test and DSTCS its percentage.
依所需診斷與可接受影響選測試，保存開始時間並查進度；若命令需要暫停測試，controller 先暫停、完成該命令，再恢復測試。 || Select depth/impact, record start and monitor; commands requiring suspension run between test suspension and resumption.
測試結束後由 Result 判定成功或哪個 segment 失敗；短程通過不保證延伸測試也必然通過。 || Results determine pass/failure; a short pass does not guarantee an extended pass.
關鍵差異是 Reset：Short 必須被影響它的 CLR 中止；Extended 必須跨 CLR 與恢復供電後繼續。 || Reset is a crucial difference: CLR aborts short tests, while extended tests persist across CLR and resume after restored power.
驗證時間時保留其他工作與暫停因素；驗證 Reset 時分別套用兩種測試規則。 || Account for other work/suspension when reviewing timing and apply the distinct reset rules.
先查 STC，不要把 Extended 的持續性套到 Short，或反過來。 || First inspect STC before applying reset persistence.
''')

q(151,'Self-test 進行中再次啟動或要求中止會怎樣？ || What happens when self-test is restarted or cancelled?', '''
避免同一限制範圍同時跑多個測試，並提供明確的背景操作中止方法。中止 Self-test 操作應使用 STC=Fh。 || Concurrency is limited and STCFh explicitly cancels the background self-test operation.
DSTO.SDSO=0 以 controller 判斷是否已有測試；SDSO=1 則以 subsystem 判斷。 || SDSO0 checks controller-level concurrency andSDSO1 subsystem-level concurrency.
先讀 DSTO 與 LID06h；只看目前 controller 的 Host outstanding 清單不足以知道另一端是否已開始測試。 || Read DSTO and LID06h; local host command tracking cannot rule out an already running background test.
STC1／2／3 為新操作；Fh 中止；Eh 是廠商特定，互動規則也可能不同。 || STC1/2/3 start operations, Fh cancels andEh has vendor-specific interactions.
已有測試時送 Fh，controller 先中止、建立最新結果，再將目前操作設為 idle，最後完成命令。 || With an active test, cancellation precedes a new result, idle state and command completion.
沒有測試時送 Fh 仍成功，且不修改 Self-test Log；不能為這次空中止捏造新結果。 || Cancelling with no test succeeds without changing the log.
已有測試時再送1／2／3，回 Device Self-test In Progress（1/1Dh）；不能要求它默默重啟原測試。 || Starting1/2/3 while a test is active returns 1/1Dh rather than silently restarting it.
核對中止 CQE 前 Log 更新順序，以及新結果 DSTR=1，避免把 idle 當成唯一證據。 || Verify log update ordering and DSTR1 rather than idle alone.
先查使用的是 STC=Fh，還是誤用 Abort 去中止早已完成的啟動命令。 || First distinguish STCFh from Abort targeting an already completed initiation command.
''')

q(152,'Current Operation 與 Completion Percentage 如何解讀？ || How are current operation and completion percentage interpreted?', '''
Log 開頭描述正在執行的工作，後面的 Result List 描述已結束的測試。兩者可能同時存在，不應用舊結果取代當前進度。 || The header describes current work while the result list describes finished tests; old results do not replace current progress.
依測試的 controller／共享範圍讀正確 Log，並保存取樣時間。 || Query the appropriate test scope and retain sampling time.
先確認支援，再使用 LID06h 的 CDSTO、CDSTC 與 RDS1。 || Use LID06h CDSTO/CDSTC/RDS1 after checking support.
DSTOS=0 為無操作，1 為 Short，2 為 Extended，3 為 Host-Initiated Refresh；DSTCS 的值25代表25%，不是零起算26%。 || DSTOS0 is idle,1 short,2 extended,3 refresh; DSTCS25 means 25%, not26%.
先讀 DSTOS，只有有操作時才解讀 DSTCS；idle 時應忽略百分比，再查看最新 Result。 || Read operation before percentage; ignore percentage when idle and inspect the latest result.
Short／Extended 結束時，必須先建立結果才清 DSTOS。讀到 idle 並搭配新 Result，才知道操作如何結束。 || A short/extended result must be created before clearing DSTOS; idle plus new result establishes outcome.
百分比不動不一定失敗，可能測試在某個 segment 或被其他命令暫停；也不能把100%欄位當成全部結果。 || A stationary percentage need not prove failure; segment work or suspension may explain it. Percentage does not replace outcome.
比較連續快照的 operation、進度與最新結果，避免只用一個百分比斷言韌體卡住。 || Compare operation, progress and result across snapshots rather than diagnosing a stall from one number.
先看 DSTOS 是否為0，若是就不要繼續解讀殘留的 DSTCS。 || First check idle before interpreting a leftover percentage.
''')

q(153,'成功、失敗、中止、Reset 與斷電後的 Self-test 結果怎麼看？ || How are self-test outcomes and interruption effects interpreted?', '''
測試結果需要保留原因，才能區分裝置診斷失敗與 Host 主動中止。Extended 因 Reset 暫停後恢復，不應被錯記成測試已失敗。 || Outcome codes distinguish diagnostic failure from host cancellation; resumed extended testing must not be mislabeled as failed due to reset alone.
結果屬於一次測試，包含當時測試代碼與時間；不是啟動命令的 CQE Status。 || Results describe test instances and their code/time, not initiation-command status.
用 LID06h 的 DSTR、DSTC、POH 及 valid diagnostic fields。 || Read DSTR, DSTC, POH and valid diagnostic fields in LID06h.
DSTR0=成功，1=Self-test 命令中止，2=CLR 中止，3=namespace 移除，4=Format，5=致命或未知測試錯誤，6／7=segment 失敗，8=未知中止，9=Sanitize 中止。 || DSTR0 success;1 command cancellation;2 CLR;3 namespace removal;4 Format;5 fatal/unknown test error;6/7 segment failure;8 unknown abort;9 Sanitize.
先判斷 Short 或 Extended，再對照中止事件。Short 遇 CLR 結束；Extended 跨 Reset／恢復供電繼續，之後才產生最終結果。 || Identify test type before matching interruption: CLR ends short testing but extended testing resumes and produces its final result later.
成功用 DSTR0；已知 segment 失敗用7並提供 SEGN；沒有新結果可能是 Extended 仍在恢復執行，不可直接判定 Log 遺漏。 || DSTR0 passes;7 provides a known failing segment. No new result can mean extended testing is still resuming.
規格沒有 Power Loss 專屬 DSTR 值；不能自創代碼。Format 是否中止測試還需依 Figure701 的 scope 組合。 || There is no separate power-loss DSTR code; Format cancellation also depends on Figure701 scope combinations.
比對外部 Reset／Format／Sanitize 時間、測試類型及 Log，確認結果原因能互相解釋。 || Correlate external operations, test type and log cause.
先確認 Extended 是否本來就應該繼續，避免把沒有 Reset-aborted Result 視為錯誤。 || First check extended-test continuation before expecting a reset-aborted entry.
''')

q(154,'Self-test 完成一定有 Asynchronous Event 嗎？ || Does every self-test completion generate an AER?', '''
原題容易暗示有通用完成通知，需要修正：正常 Self-test 完成以 Log 判定，不能等待不存在的通用完成事件。 || Correct the implied premise: normal completion is established by the log, not a nonexistent generic completion event.
啟動命令先完成，背景測試稍後結束；兩者不同，也不會自動轉成 AER。 || Initiation completion and later background completion are distinct and do not automatically create an AER.
查 Self-test 能力與 LID06h；診斷失敗另看 Error 類型的 Diagnostic Failure 定義。 || Check self-test/LID06h support and the separate Diagnostic Failure error event.
Diagnostic Failure 的 AET=0、AEI=02h，與 Device Self-test Log 的 DSTR 不同；不是把 DSTR 全部放進 AER。 || Diagnostic Failure uses AET0/AEI02h and is distinct from DSTR.
啟動後定期讀 DSTOS 與新 Result；收到診斷錯誤事件時再查補充 Error Information，並與測試結果關聯。 || Monitor operation/new result; correlate any diagnostic-error event and additional error information.
正常完成且沒有 AER 可以符合規範；有診斷失敗事件也仍須讀具體結果，不能只用事件當完整診斷。 || Normal completion without AER can conform; an error event still does not replace detailed results.
不能把沒有 Self-test Completed AER 寫成必定不合規的測項，也不能因有 AER 就把測試當成功。 || Do not fail compliance solely for absent generic completion AER or interpret any AER as success.
以實際定義的事件與 Log 驗證，避免把 Sanitize Completed 的機制套到 Self-test。 || Validate defined events rather than transplanting Sanitize completion semantics.
先查測試要求是否用了規格沒有定義的事件名稱。 || First inspect whether the test expects an undefined event.
''')

q(155,'Segment、Diagnostic Information 與 Failing LBA 何時有效？ || When are segment, diagnostic and failing-LBA fields valid?', '''
欄位有值不代表有效。有效位元讓 Host 避免把保留或未知資料當成精確故障位置。 || Nonzero fields need not be valid; validity bits prevent false precision.
SEGN 指內部測試 segment；FLBA 指 namespace 的 logical block，兩者沒有固定換算關係。 || SEGN identifies an internal test segment and FLBA a logical block; they are not interchangeable.
先看 DSTR，再看 VDINFO 的 NSIDVLD、FVLD、SCTVLD、SCVLD。 || Read DSTR and VDINFO validity bits before the corresponding fields.
只有 DSTR=7 時 SEGN 表示第一個已知失敗 segment；FLBA 只有 FVLD=1 才有效，NVM 定義它是造成失敗的某一個 LBA。 || SEGN is the first known failed segment only for DSTR7; FVLD validates one failing LBA under NVM semantics.
先確認結果非空，再確認各 valid bit，最後用有效 NSID 與 FLBA 對回 namespace；沒有有效 NSID 時，不能自行猜測其歸屬。 || Check nonempty result and valid bits before mapping namespace/LBA; do not invent namespace association.
多個 LBA 失敗時，只回其中一個是合法，不保證列出全部，也不保證是最低 LBA。 || Reporting one of several failing LBAs is valid; completeness or lowest-LBA ordering is not guaranteed.
無效欄位應忽略，不要因其值超範圍就判違規；同時，也不能忽略已宣告有效但明顯錯誤的內容。 || Ignore invalid fields rather than validating their range, while valid contradictory data remains significant.
以有效位元、測試結果與格式共同驗證，區分「未知位置」與「已知位置不合理」。 || Distinguish unknown location from an inconsistent valid location using validity and format.
先檢查 FVLD，而不是先把 FLBA=0 當成 LBA0 壞掉。 || First inspect FVLD before diagnosing LBA0 from a zero value.
''')

q(156,'Self-test 結果如何排列，超過20次後怎麼辦？ || How are the 20 self-test results ordered and replaced?', '''
固定大小歷史讓 Host 查最近測試，但不能當成裝置出廠以來所有診斷的永久清單。 || Fixed history supports recent diagnosis rather than a complete lifetime audit.
LID06h 保存20個結果，每個28 bytes，前4 bytes 是目前狀態。 || LID06h has 20 results of 28 bytes after a 4-byte current-status header.
使用 Log 固定結構與 DSTC／DSTR 空 entry 規則，不要用全零判斷是否有效。 || Use structural and empty-entry rules, not an all-zero test.
RDS1 最新，RDS2 次新，依序到 RDS20。未使用 entry 的 DSTR=Fh、DSTC=0，其他欄位應忽略。 || RDS1 is newest through RDS20 oldest; unused entries have DSTRFh/DSTC0 and other fields ignored.
測試前保存RDS1，完成後確認新結果移到第一筆，舊結果向後排列；超過容量後最舊結果不再列入最近20次。 || Snapshot RDS1, then verify insertion and older-result displacement; history beyond20 is no longer included.
第21次結束後仍只顯示最近20次，不需要新增第21個結構，也不算遺失必要欄位。 || After the 21st result,20 structures still represent the recent history.
沒有進行中的測試而送STC=Fh不修改Log，不能要求插入「中止成功」的新測試結果。 || STCFh with no active test leaves the log unchanged rather than inserting a synthetic cancellation result.
用 DSTC、DSTR、POH 與診斷內容比較前後快照，避免只用可能重複的時間值辨識唯一測試。 || Compare code, outcome, hours and diagnostics rather than treating potentially repeated timestamps as unique IDs.
先確認讀取長度涵蓋564 bytes的完整資料，而不是只拿到前幾個結果。 || First ensure the transfer covers the full564-byte structure rather than a truncated result list.
''')
