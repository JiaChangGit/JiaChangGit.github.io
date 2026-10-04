"""Q69–Q81: log selection, coherent reads and evidence interpretation."""
from scripts.nvme_qa_extension import question

question(69,'Supported Log Pages 有什麼用途？讀取其他 Log 前，應如何確認支援能力？ || What does Supported Log Pages provide, and how should support be checked before reading another log?', 'log_query',['getlog','idctrl','profile'],'''
Supported Log Pages 提供查詢目錄，讓 Host 知道目前這個介面支援哪些 LID，以及各 LID 是否允許用 entry 索引讀取。它能避免把不支援誤認為資料為零；不過，先讀它是探索方法，不是每次 Get Log Page 前都必須重送的命令。 || Supported Log Pages is a directory of LIDs and index-offset support on the current interface. It distinguishes lack of support from zero-valued data. Reading it is a discovery method, not a mandatory command before every log request.
回覆屬於收到命令的介面與 controller。不同介面可能支援不同 Log；CC.CSS=110b 時，CSI 與已啟用的 Command Set Profile 也會影響結果，不能把另一個介面的清單直接當成本介面的能力。 || Results describe the receiving interface and controller. Interfaces can differ; with CC.CSS=110b, CSI and the enabled command-set profile also affect support. Another interface’s directory is not interchangeable.
Get Log Page 使用 LID=00h。Identify.LPA 的 LPEDS 決定延伸 offset 與長度能力；各 LID 的 LSUPP、IOS 則分別表示支援及 index-offset 能力。 || Use Get Log Page LID=00h. Identify.LPA.LPEDS controls extended offset/length support; each LID entry supplies LSUPP and IOS for support and index-offset capability.
整張表有 256 個 4-byte entries。LID=n 的 entry 位於 4×n；bit0 是 LSUPP，bit1 是 IOS，高位 LIDSP 另依該 Log 定義。LSUPP=0 時，Host 應忽略其餘欄位。 || There are 256 four-byte entries. LID n is at byte 4n; bit 0 is LSUPP, bit 1 IOS, and LIDSP is log-specific. The host should ignore other fields when LSUPP=0.
先選對 controller 與命令集，讀取 00h，再找到目標 LID 的 entry。確認支援後，才依該 Log 的 scope、長度及參數讀取內容；能力在韌體或配置變更後需要重新確認。 || Select the controller and command set, read 00h, and inspect the target entry. Then apply that log’s scope, length and parameters. Rediscover capability after relevant firmware or configuration changes.
成功取得的是能力表，不是各 Log 的內容。例如 LID=81h 的 LSUPP=1，只能證明可以查 Sanitize Status，不能據此宣稱已執行或完成 Sanitize。 || Success returns a capability directory, not the logs themselves. LSUPP=1 for 81h establishes Sanitize Status availability, not that sanitization has run or completed.
不支援的 LID 一般回 Invalid Log Page（1/09h）；若 LSUPP=1，卻使用不支援的 OT=1，回 Invalid Field（0/02h）。兩者分別是 Log 不支援與讀取方式非法。 || An unsupported LID normally returns Invalid Log Page (1/09h). Using unsupported OT=1 returns Invalid Field (0/02h), even when the LID is supported. These are different failures.
將 LSUPP、IOS、LPA 與實際合法查詢一起比較。不能要求所有支援的 Log 都支援 index offset，也不能用一次非法參數失敗推翻 LSUPP。 || Compare LSUPP, IOS and LPA against a valid request. Supported logs need not support index offsets; an invalid request does not by itself contradict LSUPP.
先確認清單與後續命令來自同一介面、相同 CSI 及設定期間，再檢查目標 entry 是否按 4 bytes 定位。 || First establish the same interface, CSI and configuration period, then verify four-byte entry addressing.
''')

question(70,'Error Information Log 與 SMART / Health Information Log 分別記錄什麼？ || What do Error Information and SMART/Health Information record?', 'log_query',['getlog','error','smart'],'''
Error Information 用來追查某次錯誤的細節；SMART / Health 則提供目前警告及生命週期累計資訊。前者回答哪筆命令或哪個錯誤，後者回答目前健康狀態與長期使用情況，不能互相替代。 || Error Information explains individual errors; SMART/Health describes current warnings and lifetime usage. They answer different questions and are not substitutes.
LID01h 是 controller 的錯誤紀錄。LID02h 可依支援情況接受 namespace 查詢，但 Base 2.4 明確指出本版沒有 namespace-specific SMART 欄位，因此兩種回覆包含相同資訊，不能自行標成各 namespace 的獨立使用量。 || LID01h is controller-scoped. LID02h may accept namespace requests, but Base 2.4 defines no namespace-specific SMART information, so controller and namespace reports contain identical information rather than independent usage totals.
ELPE+1 表示最多可讀多少個 Error Information entries；LPA 的 SMART 支援位決定是否接受 per-namespace 請求。先確認支援，再解讀 Log 內容。 || ELPE+1 gives the maximum Error Information entry count. The LPA SMART bit determines whether per-namespace requests are accepted; establish support before interpreting the data.
01h 每筆 64 bytes，重點是 ECNT、SQID、CID、Status、參數錯誤位置與 NSID。02h 為 512 bytes，重點是 Critical Warning、溫度、spare、Percentage Used，以及資料量、命令、時間和錯誤累計。 || Each 01h entry is 64 bytes, with ECNT, SQID, CID, status, parameter location and NSID. The 512-byte 02h page contains warnings, temperature, spare, endurance estimate and cumulative usage/error counters.
遇到錯誤時先保存 CQE，接著讀 01h 對回命令，再以同時段 02h 觀察健康狀態。先記錄取樣時間，避免將很久以前的錯誤與目前警告錯配。 || Preserve the CQE, correlate 01h to the command, then sample 02h for health context. Record times to avoid pairing an old error with an unrelated current warning.
成功讀取不代表裝置沒有錯誤。ECNT=0 表示該 entry 無效；Percentage Used=100 表示估計耐久度已耗用，並不直接表示裝置已失效。 || A successful read does not mean an error-free device. ECNT=0 marks an invalid entry; Percentage Used=100 describes estimated endurance consumption, not necessarily device failure.
不支援 per-namespace SMART 卻指定一般 NSID，須回 Invalid Field（0/02h）。Log 中的舊錯誤 Status 是紀錄內容，與本次 Get Log Page 的完成 Status 不同。 || A specific-NSID SMART request without support returns Invalid Field (0/02h). Historical status in the log is distinct from the status of the current Get Log Page command.
SMART 的 Error Log Entries 累計不等於目前 01h buffer 裡的有效筆數；有限容量與重設清除可能讓歷史總量大於現存 entries。 || The SMART Error Log Entries total is not the number of entries currently visible in 01h. Finite capacity and reset clearing can make the lifetime total larger.
先確認你比較的是錯誤歷史、目前警告，還是累計計數，再核對各欄位的有效性與時間。 || First identify whether the comparison concerns error history, current warning state or a cumulative count, then check validity and timing.
''')

question(71,'Firmware Slot Information、Changed Namespace List 及 Commands Supported and Effects Log 分別用來確認什麼？ || What do Firmware Slot, Changed Namespace and Commands Supported and Effects logs establish?', 'log_query',['fwlog','changedlog','commandseffects'],'''
這三張 Log 分別回答韌體從哪個 slot 執行、哪些 namespace 發生過變更，以及命令受不受支援、可能造成什麼影響。它們不是通用的操作歷史清單。 || These logs identify the running firmware slot, namespaces with reported changes, and command support/effects. None is a universal operation history.
03h 的資料依 multi-domain 能力屬於 domain 或 subsystem；04h 描述此 controller 的 attached namespace 變更；05h 的命令支援則以接收命令的 controller 與命令集為準。 || 03h is domain or subsystem scoped; 04h describes attached-namespace changes for this controller; 05h describes its commands for the selected command set.
先查 00h 支援表及相關 Identify 能力。Firmware 的 slot 數與唯讀限制由 Identify.FRMW 提供，不能只靠 03h 中非零字串的數量推算。 || Check 00h and relevant Identify capabilities. Slot count and read-only restrictions come from FRMW, not merely the number of nonzero strings in 03h.
03h 讀 CAFS、NAFS 與 FRS1～7；04h 讀 NSID 清單及首筆 FFFFFFFFh 的溢位標記；05h 讀各 Opcode 的 CSUPP、effects、CSE／CSER 與 CSP。 || Read CAFS, NAFS and FRS1–7 in 03h; NSIDs and the leading FFFFFFFFh overflow marker in 04h; and CSUPP, effects, CSE/CSER and CSP in 05h.
先根據問題選 Log：更新韌體後比較 03h 與 Identify.FR；收到 namespace 通知後讀 04h，再查 Identify；執行管理命令前讀 05h，完成後重查可能被改變的能力。 || Choose by purpose: compare 03h with Identify.FR after activation; read 04h and rediscover namespaces after notification; use 05h before a management operation and refresh affected capabilities afterward.
例如 NAFS=2 只表示 slot 2 等待適用的 CLR 啟用，不表示目前已從 slot 2 執行。04h 出現 NSID=7 也只指出有變更，不能單憑清單判斷它被 Format 或刪除。 || NAFS=2 identifies a slot awaiting an applicable CLR, not the currently running slot. NSID7 in 04h signals change without specifying whether it was formatted or deleted.
各次 Get 的錯誤與 Log 所描述的事件分開。不存在支援的 LID 回 1/09h；非法已定義參數依 Get 規則回 0/02h，不能把空 slot 或空變更清單本身當成失敗。 || Separate retrieval errors from reported state. Unsupported LIDs return 1/09h; invalid defined parameters follow 0/02h rules. Empty slots or empty change lists are not themselves retrieval failures.
核對 active slot 與 FR、變更清單與新的 Identify，以及 CSUPP 與合法命令行為。每一組對照有不同目的，不要求三張 Log 的數值彼此相同。 || Correlate the active slot with FR, changed IDs with fresh Identify, and CSUPP with valid command behavior. The three logs need not contain matching values.
先確認是否把 NAFS 當 CAFS，或把 Changed List 當成完整 Active Namespace List。 || First check for confusing NAFS with CAFS or a changed list with the complete active namespace inventory.
''')

question(72,'Device Self-test、Persistent Event 及 Sanitize Status Log 分別適用於哪些情境？ || When should Device Self-test, Persistent Event and Sanitize Status logs be used?', 'log_query',['dstlog','pel','getlog'],'''
Self-test Log 用來看測試進度與最近結果；PEL 用來追查跨時間的特定事件；Sanitize Status 用來判斷清除操作的目前狀態及最後結果。先選對證據種類，才不會把命令接受當成工作完成。 || Self-test logs show progress and recent results; PEL provides supported historical events; Sanitize Status reports sanitization state and outcome. Choose the right evidence before equating acceptance with completion.
Self-test scope 受 DSTO.SDSO 等能力影響；PEL 屬於 subsystem；81h 的 NSID 則用來区分 subsystem 與 namespace sanitization target。查詢的 controller 不一定就是事件影響的全部範圍。 || Self-test scope depends on capabilities such as DSTO.SDSO. PEL is subsystem-scoped; 81h uses NSID to distinguish subsystem and namespace targets. The querying controller is not necessarily the full affected scope.
讀 OACS 的 Self-test 能力、LPA 的 PEL 能力，以及 SANICAP／namespace Sanitize 能力，再確認 LID06h、0Dh、81h 受支援。Log 可讀不代表任意操作方法都可用。 || Check self-test OACS, PEL LPA and subsystem/namespace sanitize capabilities, then the relevant LIDs. A readable status log does not establish every operation method.
06h 先讀 DSTOS，再解釋進度與結果有效位；0Dh 先建立或取得 reporting context，再依事件長度走訪；81h 先看 SSTAT，再使用 SPROG 及相關結果欄位。 || For 06h read DSTOS before progress and validity-qualified results. For 0Dh establish or obtain a reporting context and traverse lengths. For 81h inspect SSTAT before SPROG and outcome fields.
例如 Sanitize 命令完成後，持續查 81h 判斷背景操作；Self-test 結束後讀 06h 最新有效結果；要追查先前重設或管理操作，才到 PEL 找支援的事件。 || Poll 81h after sanitize acceptance for background completion; inspect the newest valid 06h result after self-test; use PEL for supported historical reset or management events.
Get 成功表示讀取成功，不表示 Self-test 通過或 Sanitize 成功。PEL 沒有某筆事件，也要先確認事件支援、記錄條件與保存範圍。 || Successful Get establishes retrieval, not a passed test or successful sanitize. Missing PEL events require checking event support, logging conditions and retained history.
不支援的 LID 回 1/09h；PEL context 順序錯誤可能回 Command Sequence Error（0/0Ch）。操作本身失敗要看其專用 Log 狀態，不能替本次成功 Get 改成失敗 CQE。 || Unsupported LIDs return 1/09h; invalid PEL context sequencing can return 0/0Ch. Operation failures in returned data do not turn a successful retrieval CQE into failure.
以操作目標、時間及最新結果交叉比對。不得將舊 Self-test 結果或上次 Sanitize 成功，當成目前這次作業已成功的證據。 || Correlate target, time and latest results. An old test result or previous sanitize success is not proof of success for the current operation.
先確認讀取對象與 operation 是否相符，再判斷進度或歷史事件。 || First match the queried target and operation before interpreting progress or history.
''')

question(73,'Endurance Group、Predictable Latency、Lockdown、Boot Partition 及 Media Unit Status Log 各記錄什麼？ || What do Endurance Group, Predictable Latency, Lockdown, Boot Partition and Media Unit Status logs contain?', 'log_query',['getlog','idctrl'],'''
這些 Log 分別描述群組耐久度、可預測延遲狀態、禁止操作清單、開機分割區狀態，以及媒體單元資源。目的不同，不能把它們統稱為健康資訊後使用相同欄位判讀。 || These logs describe group endurance, predictable-latency state, prohibited operations, boot partitions and media-unit resources. They are not interchangeable health reports.
先辨認管理對象：Endurance Group 使用 ENDGID，Predictable Latency 針對 NVM Set；Lockdown 依選擇與支援範圍，Boot Partition 透過 controller 查詢，Media Unit 則反映 domain 或 subsystem 資源。 || Establish the management object: endurance group, NVM set, lockdown selection/scope, controller-accessed boot partitions, or domain/subsystem media units.
先查 00h 及相關 Identify 能力。主要 LID 為 09h、0Ah／0Bh、14h、15h、10h；同一個 LSI 在不同 LID 的意義可能不同。 || Check 00h and relevant Identify capabilities. The main LIDs are 09h, 0Ah/0Bh, 14h, 15h and 10h. LSI can mean different things for different logs.
09h 看警告、spare 與壽命計數；0Ah／0Bh 看 Set 的 latency 狀態及事件集合；14h 看禁止的 Opcode／FID；15h 看分割區識別與保護狀態；10h 看 Media Unit 識別、歸屬及狀態。 || Inspect group warnings/spare/endurance in 09h, set latency state/events in 0Ah/0Bh, prohibited opcodes/FIDs in 14h, partition identity/protection in 15h, and media-unit identity/association/state in 10h.
由待回答的問題選 LID，再由 Identify 建立資源 ID 的對應，最後依該 Log 的參數與結構解碼。例如要查 group 3 的健康狀態，LSI 應選 ENDGID=3，而不是隨手填 NSID。 || Choose the LID by question, map resource IDs through Identify, then apply the log’s selectors and structure. Group-3 health requires ENDGID=3, not an arbitrary NSID substituted into LSI.
成功回覆只描述選定對象。例如一個 group 的警告不能推論成全部 namespace 都有相同媒體故障；Lockdown 列出禁止項目，也不是那些命令的執行歷史。 || Results describe the selected object. One group warning does not establish identical media faults in every namespace; lockdown entries are prohibitions, not execution history.
不支援的 LID 與非法資源選擇須分開處理。前者是 1/09h；後者依該 Log 的已定義參數與專用 Status 判斷，不能一律改成 Invalid Namespace。 || Distinguish unsupported LIDs (1/09h) from invalid resource selectors governed by each log’s defined fields and specific status. Do not classify all selector failures as Invalid Namespace.
核對資源歸屬、Log 狀態及實際功能。例如被禁止的 FID，應與 Lockdown 設定一致；Media Unit 狀態則要連同 namespace 所依賴的資源判斷。 || Correlate resource association, reported state and behavior. Prohibited FIDs should match lockdown policy; media-unit state must be related to namespace dependencies.
先檢查是否把 ENDGID、NVMSETID、NSID 或 Media Unit ID 混用。 || First check whether different resource identifier types were confused.
''')

question(74,'Host 如何依 Log Page 的 Scope 正確設定 NSID 及其他欄位？ || How should NSID and other selectors follow a log’s scope?', 'log_query',['getlog','smart','uuid'],'''
scope 決定資料描述哪個物件；選擇欄位則指出這次要查哪個實例。NSID 出現在公共命令格式中，不表示每張 Log 都可以查任意 namespace。 || Scope identifies the kind of object described; selectors identify its instance. A common NSID field does not make every log per-namespace.
Figure 209 列出 controller、namespace、domain、subsystem 等範圍，但個別欄位也可能有更具體的定義。讀完整張表後，仍要核對該 LID 的例外。 || Figure 209 lists scopes, while individual fields may define more specific ones. Read both the directory and the selected LID’s exceptions.
用 LSUPP 確認 Log 支援，再查 LPA、multi-domain 能力，以及該 LID 是否使用 CSI 或 UUID 選擇。這些能力決定哪些查詢組合有效。 || Check LSUPP, LPA, multi-domain support and whether CSI/UUID selection applies. Together they determine valid query combinations.
controller 或 subsystem scope 的 Log，一般使用 NSID=0 或 FFFFFFFFh；LSI、LSP、CSI 與 UIDX 各有獨立用途。不能把 LSI 當成 NSID 的延伸位元。 || Controller/subsystem logs normally use NSID=0 or FFFFFFFFh. LSI, LSP, CSI and UIDX are separate selectors, not extensions of NSID.
先寫出要查的物件，例如某 controller、ENDGID=3 或某 sanitization target，再把它映射到正確欄位。其餘未定義欄位依 Reserved 規則填寫。 || Name the target object first, then map it to the specified fields. Fill unused fields according to reserved-field rules.
合法查詢回傳所選範圍的資料。例如 aggregate SMART 與某 group 的耐久度是不同範圍，不能複製同一份資料後標成每個 namespace 的獨立統計。 || A valid request returns the selected scope. Aggregate SMART and group endurance are different views; copying an aggregate does not create independent namespace statistics.
依共同規則，controller 或 subsystem scope 的 Log 若指定 0／FFFFFFFFh 以外的 NSID，須回 Invalid Field（0/02h）。其他 scope 則按各 LID 與 NSID 規則處理。 || Under the common rule, controller/subsystem logs with another NSID return Invalid Field (0/02h). Other scopes use their LID-specific and NSID rules.
將命令中的選擇欄位、Identify 的資源對應與回傳內容一起保存，才能確定比較的是同一物件。 || Retain command selectors, Identify associations and returned data so comparisons refer to the same object.
先查該 LID 的 scope，而不是看到 NSID 非零就認定回覆是 namespace 專屬資料。 || Check the LID’s scope first; a nonzero NSID alone does not establish namespace-specific information.
''')

question(75,'大型 Log 如何分段讀取？Offset、Length、重疊及缺口應如何處理？ || How are large logs read in chunks, including offsets, lengths, overlaps and gaps?', 'log_query',['getlog','telemetrylog'],'''
分段讀取讓 Host 用有限 buffer 取得大型 Log，但必須同時保證位址連續及內容一致。每段 Get 都成功，只能證明各段傳輸成功，不能自動證明合併檔完整。 || Chunking reads a large log with bounded buffers. Both coverage and consistency matter; individually successful reads do not establish a complete coherent file.
Offset 是 Log 內的位置，不是 Host buffer 位址。OT=0 使用 byte offset；OT=1 使用該 Log 定義的 entry index，兩種單位不能混算。 || Offsets locate data within the log, not host memory. OT=0 uses bytes; OT=1 uses log-defined entry indices. Do not mix their units.
LPA.LPEDS 確認延伸長度與 offset，目標 LID 的 IOS 確認 index offset；另依 MDTS 與此 Log 的長度規則選擇每次傳輸量。 || Check LPA.LPEDS and per-LID IOS, then size transfers using MDTS and log-specific length rules.
NUMD=(NUMDU<<16)|NUMDL，通常傳輸 bytes=4×(NUMD+1)。LPOU／LPOL 組成 64-bit offset；byte offset 要 Dword 對齊。某些 Log 另有 entry 或 header 規則。 || NUMD=(NUMDU<<16)|NUMDL normally encodes bytes/4−1. LPOU/LPOL form the 64-bit offset; byte offsets require Dword alignment, with further log-specific constraints.
例如讀取 8192 bytes，可用兩段 4096 bytes，offset 分別為 0、4096，NUMD 都是 1023。記錄每段範圍，確認沒有缺口；重疊區可比對，但若期間內容改變，不能任意挑一段覆蓋另一段。 || An 8192-byte log can use two 4096-byte reads at offsets 0 and 4096, each NUMD=1023. Check coverage; overlaps can be compared, but changing content prevents arbitrary merging.
成功後應取得預定範圍。若要求長度超過 Log 尾端，除另有規定外，超出部分的結果未定義；不能把那些 bytes 當成 Log 的延伸資料。 || Success covers the requested valid range. Unless otherwise specified, bytes beyond the log end are undefined and are not additional log content.
Offset 大於 Log 大小，或不支援 IOS 卻使用 OT=1，須回 0/02h。byte offset 低兩位非零時，controller 可回 0/02h，也可依低兩位為零處理；不能把這個允許選擇寫成唯一錯誤結果。 || An offset beyond the log or OT=1 without IOS returns 0/02h. For nonzero low two byte-offset bits, the controller may reject or operate as if those bits were zero; neither outcome is universally mandatory.
核對總長度、各段 offset／NUMD、generation 或 reporting context。涵蓋完整與同一份快照，是兩個都要成立的條件。 || Verify total length, offsets/NUMD and generation or reporting context. Complete coverage and one coherent snapshot are separate requirements.
先確認 Offset 單位及 NUMD 的加 1 換算，再檢查是否混入另一代資料。 || First check offset units and NUMD’s +1 conversion, then look for mixed generations.
''')

question(76,'Log Specific Identifier、UUID Index 及 Retain Asynchronous Event 有什麼用途？ || What are LSI, UUID Index and Retain Asynchronous Event used for?', 'log_query',['getlog','uuid','aer'],'''
這三個欄位分別選資源、選資料定義，以及決定讀取後是否保留事件。它們控制不同部分，不能因為都叫參數就互相替代。 || These fields select a resource, a data-definition context, and event retention. Their roles are independent.
LSI 的意義由 LID 決定；UIDX 從 UUID List 選擇適用定義；RAE 則影響這次讀取所對應的非同步事件。不是所有 Log 都使用三者。 || LSI is LID-specific; UIDX selects a UUID-list definition; RAE controls the associated event. Not every log uses all three.
先看該 LID 是否定義 LSI，以及 Get Log Page 是否支援 UUID 選擇。RAE 是否有實際作用，則要看該事件如何確認與清除。 || Check whether LSI is defined and UUID selection supported. RAE behavior depends on the event’s acknowledgment rules.
LSI 在 CDW11 bits31:16；UIDX 在 CDW14 bits6:0，0 表示不指定 UUID；RAE 在 CDW10 bit15。UIDX 是索引，不是 UUID 的數值本體。 || LSI is CDW11[31:16], UIDX CDW14[6:0] with zero meaning no UUID selection, and RAE CDW10[15]. UIDX is an index, not the UUID itself.
先固定目標與 UUID 定義，再決定是否要保留事件以繼續取樣。若需要分段讀取與事後確認，保存每次 RAE，並遵守該 Log 的特定確認方式。 || Fix the target and UUID definition, then decide whether the event should remain pending. Record RAE for each chunk and follow the selected log’s acknowledgment procedure.
RAE=1 的成功讀取保留對應事件；RAE=0 的成功讀取依規則清除。若命令未成功，事件必須保留，不能因 Host 已嘗試讀取就視為確認。 || Successful RAE=1 reads retain the event; successful RAE=0 reads clear it as defined. Failed reads must retain it; an attempted read is not acknowledgment.
非法 UUID 選擇依 §8.1.31 回 Invalid Field（0/02h）；LSI 非法則按該 LID 定義處理。不能用改 RAE 的方式修正錯誤的資源 ID。 || Invalid UUID selection follows 0/02h rules in §8.1.31; invalid LSI follows the LID definition. Changing RAE does not fix the selected resource.
核對 LSI 的目標、UIDX 對應資料及事件是否仍 pending。讀取相同 bytes 但 RAE 不同，後續通知行為可能不同。 || Compare the target, UUID mapping and pending-event state. Identical returned bytes with different RAE can produce different subsequent notification behavior.
先檢查是否曾有另一個成功的 RAE=0 讀取，提前確認了正在追蹤的事件。 || First look for another successful RAE=0 read that already acknowledged the event.
''')

question(77,'分段讀取期間 Log 內容改變時，Host 如何判斷資料是否一致？ || How can a host detect inconsistent log chunks when content changes?', 'log_query',['getlog','telemetrylog','pel'],'''
這題要防止把不同時點的資料拼成一份看似完整的報告。長度正確、沒有缺口，仍不代表所有欄位屬於同一次擷取。 || This prevents combining different times into an apparently complete report. Correct length and coverage do not establish a single capture.
一致性判斷由各 Log 提供的機制決定。Telemetry 有 generation，PEL 有 reporting context；沒有此類機制的動態 Log，不能自行假設跨命令原子快照。 || Consistency is log-specific: Telemetry has generations, PEL reporting contexts. Other dynamic logs do not gain cross-command atomic snapshots by assumption.
先確認支援的 Log 結構與版本，再找 generation、總長度、可用狀態或 context action。不能只查看 Get Log Page 的公共欄位。 || Check the supported log structure/version and its generation, total length, availability or context action. Common command fields alone are insufficient.
Telemetry 記錄 TCDGN／相關 generation 及資料區邊界；PEL 記錄 context、TLL、事件長度與版本。每段同時保存 offset、length 及取得時間。 || Retain Telemetry generation and area boundaries, or PEL context/TLL/event lengths and versions, together with each chunk’s offset, length and acquisition time.
先取得 header，再按同一擷取或 context 讀取；必要時重讀 header。若前後 generation 改變，應重新取得一致資料，或明確標示無法證明一致，不能只換掉最後一份 header。 || Read the header, use the same capture/context and recheck the header where applicable. A changed generation requires reacquisition or an explicit consistency limitation, not just replacement of the header.
例如最初 TCDGN=10、最後=11，兩次 Get 都成功仍不足以證明中間所有 chunks 來自第 10 代。成功的分析結果必須連同一致性證據保存。 || Initial TCDGN=10 and final=11 leave intervening chunks unproven even when all Gets succeed. Retain consistency evidence with the resulting report.
內容改變不一定產生錯誤 CQE；動態更新本身可以合法。PEL 的非法 context 操作則可能得到 0/0Ch，應和資料版本改變分開判斷。 || Content changes need not produce an error CQE. Invalid PEL context operations can produce 0/0Ch, which is distinct from a legitimate generation change.
將 header、每段資料及查詢順序當成一組證據，不能拿最後讀到的 capability 或 generation 回頭替所有舊 chunks 背書。 || Treat headers, chunks and query order as one evidence set. The last capability or generation value cannot retroactively validate every earlier chunk.
先看 generation 或 context 是否在整段讀取期間保持一致，再檢查解析器。 || Check generation/context continuity before blaming the parser.
''')

question(78,'Error Information Log 或 Persistent Event Log 到達容量上限時，舊紀錄如何處理？ || How are old records handled when Error Information or PEL reaches capacity?', 'log_query',['error','pel'],'''
有限容量的 Log 不可能無限保存歷史，因此必須分清楚累計事件數與目前還能讀到的紀錄。缺少舊 entry 不一定表示事件從未發生。 || Finite logs cannot preserve unlimited history. Distinguish cumulative counts from currently readable records; a missing old entry does not prove the event never occurred.
Error Information 以 controller 為範圍；PEL 保存 subsystem 的支援事件，並透過 reporting context 提供報告。兩者的容量與讀取生命週期不同。 || Error Information is controller-scoped; PEL contains supported subsystem events accessed through reporting contexts. Capacity and read lifecycles differ.
Error Information 的容量由 ELPE+1 決定；PEL 先看支援能力、報告 TLL、事件數與最大容量資訊。不能把 SMART 累計值當成目前 buffer 的長度。 || ELPE+1 sets Error Information capacity. For PEL inspect support, report length/event count and maximum capacity; SMART totals do not size the current buffer.
Error entries 依新到舊排列，ECNT 識別每次錯誤。PEL 依 event header 的 EHL、EL、ET、ETR 走訪，不能假設每筆固定 64 bytes。 || Error entries are newest first with ECNT identity. PEL traversal uses EHL, EL, ET and ETR; events are not fixed 64-byte error entries.
取樣時記錄有效 entries 與首尾識別，再於後次取樣找重疊範圍。若最舊紀錄已不在可讀範圍，標示歷史缺口，不能補造它的內容或順序。 || Record valid entries and boundary identities, then correlate overlapping samples. Mark lost history explicitly rather than inventing missing records or their order.
Error Log 已滿又新增 entry 時，規範建議插入新 entry 並丟棄最舊 entry。PEL 是有限的持續歷史，讀完整份報告也不等於讀到裝置全部生命週期事件。 || When Error Information is full, the specification recommends inserting the new entry and discarding the oldest. A complete finite PEL report is not the device’s entire lifetime history.
容量用完不會使合法 Get 自動回失敗；應檢查回覆內容與各 Log 的保存規則。只有查詢參數或 context 不合法時，才依相應 Status 處理。 || Full storage does not automatically make a valid Get fail. Inspect retention behavior; invalid parameters or contexts are separate command errors.
ECNT／SMART 的累計變化與目前筆數可能不同；應以容量及保留規則解釋，不能要求每次取樣都仍含所有舊紀錄。 || ECNT/SMART totals may diverge from visible entry counts. Explain the difference using capacity and retention, not an expectation of unlimited historical preservation.
先確認讀取長度是否只要求前幾筆，再判斷是真的被淘汰，還是 Host 根本沒讀完整。 || First check whether the request asked for only the newest few entries before concluding that older records were evicted.
''')

question(79,'哪些 Log 資料在 Controller Reset、NVM Subsystem Reset 或 Power Cycle 後仍可保留？ || Which log data survives controller reset, subsystem reset or power cycling?', 'log_query',['getlog','error','smart','pel','reset'],'''
判斷保留性時，要把查詢命令、暫時回報狀態與真正保存的歷史分開。重設使 Get 中止，不表示它原本要讀的所有資料都被清除。 || Separate the query command, temporary reporting state and retained history. An aborted Get does not imply erasure of all underlying data.
保留規則可能適用整張 Log，也可能只適用其中某個欄位。多 controller 或 multi-domain 配置還要先確認重設影響哪些範圍。 || Retention may apply to a whole log or individual fields. Establish reset coverage in multi-controller and multi-domain configurations.
讀各 Log 的保留敘述與 Reset 章節。Figure 209 的 Restore to Default Content 指製造預設內容的恢復，並不是「遇到任何 Reset 就清空」的能力位。 || Use log-specific retention text and reset rules. Figure 209’s Restore to Default Content concerns manufacturing defaults, not clearing on every reset.
典型比較是 Error Information entries、其 ECNT、SMART 累計值、即時溫度、PEL 事件及 PEL context。這六種資訊即使相鄰，也不能套用同一保留結論。 || Compare error entries, their ECNT, SMART totals, current temperature, PEL events and PEL context separately. Proximity does not imply identical retention.
先取得同一對象的前置快照，執行指定重設，恢復查詢後再讀。記錄中間是否同時發生 Firmware Activation、Format 或出廠配置恢復，避免把多個原因混成一個。 || Capture the same target before reset, perform the specified event, recover and read again. Record concurrent activation, format or manufacturing-default restoration as separate causes.
Error entries 在 CLR 與 Power Cycle 後建議清除，但 ECNT 持續；SMART 生命週期資訊原則上跨 Power Cycle 保留，個別欄位另有例外；PEL 事件的持續性不能套到 reporting context。 || Error entries should clear on CLR/power cycle while ECNT persists. SMART lifetime data persists across power cycles unless a field says otherwise. Persistent PEL events do not make reporting contexts persistent.
比較前後值本身沒有新的 Status。如果恢復後 Get 失敗，先檢查 controller 是否 Ready、選擇欄位與 context 是否有效，不能將查詢失敗解釋成內容已被清零。 || Comparing values creates no status. A failed post-reset Get first requires checking readiness, selectors and context; it is not evidence of cleared data.
以欄位的有效條件與單位比較，而不是要求整個 buffer 完全相同。累計保留與目前狀態重新取樣可以同時成立。 || Compare field semantics and validity rather than requiring byte-identical buffers. Persistent counters can coexist with newly sampled current state.
先確認是在比較內容保留，還是在比較一個已失效的 context 或未完成查詢。 || First determine whether the discrepancy concerns stored content, an invalidated context or an interrupted query.
''')

question(80,'Supported Log Pages 或 Commands Supported and Effects 的宣告與實際行為不一致時，如何判斷？ || How should advertised log/command support be checked against actual behavior?', 'log_query',['getlog','commandseffects','idctrl','profile'],'''
這題要建立可重現的能力一致性檢查。宣告支援只表示存在合法用法，不能把任何參數下的失敗都判為能力造假。 || Build a reproducible support-consistency check. Support establishes valid uses, not success for every parameter combination.
固定接收介面、controller、CSI、UUID 選擇及配置時間。尤其 CC.CSS=110b 時，尚未啟用的命令集會被視為不支援。 || Fix interface, controller, CSI, UUID selection and configuration time. With CC.CSS=110b, a command set not enabled by the profile is treated as unsupported.
一起保存 LSUPP、IOS、CSUPP、Identify 的功能位與 FID19h 設定。不要拿 LID 的支援位去判斷任意 Opcode，也不要反過來混用。 || Preserve LSUPP/IOS, CSUPP, Identify capability bits and FID19h. Log support and opcode support are different declarations.
測試命令保留 LID 或 Opcode、NSID、CSI、LSP、LSI、OT、長度及資料指標。取得 CQE 後再讀 SCT／SC，而不是只記一個工具錯誤訊息。 || Retain all relevant selectors, length and data pointers, then decode CQE SCT/SC rather than only a tool’s error string.
先構造符合能力、scope 及狀態的合法命令，再執行並核對結果。若失敗，逐項排除非法參數、被 Lockdown 禁止、namespace 未就緒及配置變更。 || Construct a request meeting capability, scope and state requirements, execute, then exclude invalid fields, lockdown, namespace readiness and intervening changes before declaring a contradiction.
在同一穩定配置下，明確宣告支援卻對合法請求回不支援，才形成需要追查的矛盾；合法的限制性 Status 不能直接當成不支援。 || In a stable context, unsupported status for a valid advertised operation is a contradiction to investigate. A legitimate restrictive status is not equivalent to lack of support.
Get 不支援 LID 使用 1/09h；不支援 Opcode 使用 0/01h；0/02h 通常需要回頭檢查參數。保留規範的專用例外與多重錯誤選擇，不能只比一個預期數字。 || Unsupported LID uses 1/09h; unsupported opcode uses 0/01h; 0/02h calls for parameter review. Preserve specific exceptions and allowed choices for multiple errors.
比較內容、行為與時間關係三者。若韌體已啟用新版本，應先重讀宣告，不能用舊表要求新 controller 行為。 || Compare declarations, behavior and timing. After activation, rediscover support instead of imposing an old table on new firmware.
先確認兩份證據來自同一介面與同一命令集配置，這通常比先懷疑韌體更能排除誤判。 || First verify the same interface and command-set configuration on both sides of the comparison.
''')

question(81,'Host 如何從 Commands Supported and Effects Log 確認 Opcode 支援及影響範圍？ || How does Commands Supported and Effects describe opcode support and impact?', 'log_query',['commandseffects','idctrl','profile'],'''
這張表讓 Host 在執行命令前，了解是否支援，以及操作可能改變資料、namespace 配置或 controller 能力。它描述可能效果，不是每次執行一定發生的全部效果。 || The table describes support and possible effects on data, namespaces and controller capability. It reports overall possible effects, not effects guaranteed on every invocation.
Admin Opcode 與 I/O Opcode 使用不同區域；I/O 區還要選對命令集。CSP 可以同時表示多種 scope，因為實際參數可能決定不同影響對象。 || Admin and I/O opcodes occupy separate regions; the I/O region also requires the correct command set. CSP can name several possible scopes because parameters affect actual impact.
先確認 LPA.CSES、LID05h 支援與命令集選擇。CSP=0 表示未回報 scope，不能解成「不影響任何物件」。 || Check LPA.CSES, LID05h and command-set selection. CSP=0 means no scope is reported, not no affected object.
Admin entry 位於 4×Opcode；I/O entry 位於 1024+4×Opcode。讀 CSUPP、LBCC、NCC、NIC、CCC，並搭配 CSE、CSER、USS 與 CSP，不只看最低位。 || Admin entry offset is 4×opcode; I/O offset is 1024+4×opcode. Decode support, effects, submission recommendations, UUID selection and scope rather than only bit 0.
先找到正確 entry，再依 CSE／CSER 的建議協調其他工作。Host 支援非零 CSER 值時，使用其放寬建議；不支援時回到 CSE。命令完成後，重新查詢可能改變的能力或清單。 || Select the entry and coordinate work under CSE/CSER recommendations. Use a supported nonzero CSER relaxation; otherwise use CSE. Rediscover potentially changed capabilities or inventory afterward.
例如 NIC=1 表示命令可能改變 namespace 數量或多個 namespace 的能力，不表示這次呼叫一定新增一個 namespace。CSUPP=0 時，其餘 entry 欄位須為零。 || NIC=1 permits inventory or multi-namespace capability changes; it does not guarantee one new namespace per call. CSUPP=0 requires all other entry fields to be zero.
讀表失敗依 Get Log Page 處理；實際命令失敗則依該命令 Status。CSE 的建議不能任意提高成一個固定的強制錯誤碼。 || Retrieval errors follow Get Log Page; operation errors follow the command. Submission recommendations do not authorize inventing a mandatory status for every violation.
將 effects 與操作前後 Identify、清單及使用者資料影響交叉比對。CSUPP 與 Identify 宣告應一致，但實際效果仍須依本次參數判斷。 || Correlate effects with before/after Identify, inventory and data. Support declarations should agree; actual effects depend on this invocation’s parameters.
先確認 entry 偏移是否漏加 I/O 區的 1024 bytes，再檢查 CSI 與 CSP=0 是否被誤解。 || First check the I/O region’s 1024-byte base, then CSI and the interpretation of CSP=0.
''')
