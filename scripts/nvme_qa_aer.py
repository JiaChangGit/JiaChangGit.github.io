"""Q82–Q92: asynchronous notification and acknowledgment."""
from scripts.nvme_qa_extension import question

question(82,'Host 為什麼需要預先送出 Asynchronous Event Request？沒有事件時為何保持 Outstanding？ || Why post Asynchronous Event Requests before events, and why do they remain outstanding?', 'aer_request',['aerfull','idctrl','aec'],'''
AER 提供 controller 可使用的通知回覆機會。controller 不能在沒有對應 Request 的情況下，任意產生一筆一般 AER completion，因此 Host 先提交 Request，等待日後事件。 || AER provides a request the controller can complete to report an event. It is not an unsolicited ordinary completion without a corresponding request, so the host posts requests in advance.
每筆 AER 屬於提交它的 controller 與 Admin Queue。它等待的是事件，不是對某個 namespace 執行讀寫。 || Each AER belongs to its controller and Admin Queue. It waits for an event rather than reading or writing a namespace.
Identify.AERL+1 是同時未完成 Request 的上限。選配通知另查 OAES 與 FID0Bh，不能把 AERL 當成事件種類數。 || Identify.AERL+1 limits outstanding requests. OAES and FID0Bh govern optional notifications; AERL is not an event-type count.
AER 的命令特定欄位都是 Reserved；Host 仍需分配 Admin SQ 中唯一的 CID。事件發生後，DW0 的 AET／AEI／LID 與必要的 DW1 描述結果。 || Command-specific fields are reserved; allocate a unique outstanding Admin CID. Event completion supplies AET/AEI/LID in DW0 and event-specific DW1 where defined.
完成初始化及通知設定後，提交不超過上限的 AER。收到事件時保存回覆，處理並確認事件，再補上 Request，維持可用的通知機會。 || After initialization and notification setup, post requests within the limit. Preserve a returned event, handle and acknowledge it, then replenish the request pool.
沒有事件時長時間保持 outstanding 是正常行為，Host 不應替 AER 設一般命令 timeout。它不需要定期回成功來證明自己仍存在。 || Remaining outstanding without events is normal; the host should not assign an ordinary timeout. AER does not need periodic success completions as a liveness signal.
超過並行上限時，會涉及 Asynchronous Event Request Limit Exceeded（1/05h）。尚未有事件而未完成，則不是 Command Timeout 的規範錯誤結果。 || Exceeding the outstanding limit can produce Asynchronous Event Request Limit Exceeded (1/05h). Waiting without an event is not a specified timeout error.
比對 Host 尚未完成的 AER 數、AERL、通知設定與事件條件，而不是只計算命令已等待幾秒。 || Compare outstanding request count, AERL, notification configuration and event conditions rather than elapsed seconds alone.
先確認是否真的有 AER 已提交且尚未完成，再追查 controller 為何沒有通知。 || First establish that a request was actually submitted and remains outstanding.
''')

question(83,'事件發生後，Host 如何從 AER Completion 取得事件種類與 Log 位置？ || How does AER completion identify the event and its log?', 'aer_request',['aerfull','cqe'],'''
Completion 的成功 Status 只表示 AER 正常完成；真正的通知內容放在命令特定結果中。必須再解析事件欄位，才能知道要讀哪張 Log。 || A successful status completes the AER; the actual event is in its command-specific result. Decode that result to select the next log.
以 AER 的 SQID 與 CID 找到原 Request，再解讀這個 controller 回報的事件。不能把另一筆普通 Admin 命令的 DW0 當成 AER 格式。 || Match the request by SQID/CID before decoding the controller’s event; another Admin command’s DW0 need not use the AER format.
支援的事件種類由能力及 Figure 153～160 等事件表定義。先解 AET，再用它選 AEI 的對應表。 || Capabilities and event tables define the supported events. Decode AET first to select the AEI table.
DW0 bits2:0 是 AET、bits15:8 是 AEI、bits23:16 是 LID。DW1 是事件特定參數；若事件沒有定義它，不能自行當成 NSID。 || DW0[2:0] is AET, [15:8] AEI and [23:16] LID. DW1 is event-specific; do not assume it is NSID without a definition.
先驗 CQE 的 Phase 與命令身分，再解 SCT／SC。正常 AER completion 才進一步解事件內容，依事件表讀取 Log 或執行對應處理。 || Validate phase and identity, then SCT/SC. For normal event completions, decode the event and follow its associated read or handling rule.
例如 AET=Notice、AEI=Firmware Activation Starting，指向 Firmware Slot Information；它表示開始啟用，不表示新韌體已啟用完成。Sanitize 的事件也要搭配 DW1 的 target 定義。 || Firmware Activation Starting is a Notice pointing to Firmware Slot Information; it signals starting, not completion. Sanitize events additionally use their defined DW1 target.
若 AER 本身以 1/05h 等錯誤完成，不能把 DW0 任意解成正常事件。AEI 的相同數值在不同 AET 下也可能代表不同事情。 || Do not decode arbitrary DW0 as an event when the AER itself failed. Identical AEI values can mean different things under different AETs.
保存完整 CQE 與後續 Log，核對事件所指的 LID 及 target，而不是只保留翻譯過的一行訊息。 || Preserve raw CQE and subsequent log, checking LID and target instead of retaining only a translated message.
先確認 AET 有沒有選錯解碼表，再檢查 LID 與 DW1。 || First check the AET-selected decoding table, then LID and DW1.
''')

question(84,'Host 處理事件後，為什麼需要讀取對應 Log 並重新送出 AER？ || Why read the associated log and post another AER after an event?', 'aer_request',['aerfull','getlog'],'''
讀取 Log 用來了解並確認事件；重新提交 AER 則提供下一次回報機會。兩個動作目的不同，少做其中一個都可能讓後續通知看似停止。 || Reading the log obtains and acknowledges event information; posting AER supplies the next response opportunity. Missing either can stall future notification.
一般事件回報後，相關事件類型會被自動遮蔽，直到 Host 按規則確認。Immediate 與 One-Shot 另有規則，不能套用相同清除流程。 || Ordinary reported event types are automatically masked until acknowledged. Immediate and One-Shot events have separate clearing behavior.
確認此事件對應的 LID、RAE 規則與通知啟用狀態。AERL 只限制等待中的 Request，不能解除事件遮蔽。 || Check the event’s LID, RAE rule and enablement. AERL limits outstanding requests; it does not unmask events.
一般使用 Get Log Page 並以 RAE=0 確認；RAE=1 保留事件。新的 AER 是另一個 Admin 命令，必須有自己的有效 CID。 || Ordinary acknowledgment uses Get Log Page with RAE=0; RAE=1 retains the event. The replacement AER is another Admin command with a valid CID.
先保存通知，再讀取並處理所需資訊，依事件規則確認，最後維持適當數量的 AER。若警告條件仍持續，確認前應考慮調整門檻或遮蔽，避免不停回報同一狀態。 || Preserve the notification, read and process evidence, acknowledge as defined and maintain request availability. For persistent conditions, consider threshold or mask changes before acknowledgment to avoid repeated reports.
成功確認後，事件回報機制可繼續；但若條件仍成立，仍可能再次通知。重新提交 AER 本身不等於已清除原事件。 || Acknowledgment permits further reporting, but a continuing condition can be reported again. Posting another AER alone does not clear the original event.
讀取失敗時事件必須保留，不能把嘗試過 RAE=0 當成清除成功。若是 One-Shot，則在回報時已清除，應依該事件處理。 || Failed reads retain the event; an attempted RAE=0 request is not success. One-Shot events clear on reporting and follow their specific handling.
檢查三件事是否都完成：事件資訊已保存、確認動作成功、仍有 AER 等待。它們不是同一個成功碼能證明的事情。 || Verify evidence preservation, successful acknowledgment and an available AER separately; one status does not prove all three.
先確認是不是只補 Request 卻沒清除事件，或只讀 Log 卻忘了補 Request。 || First distinguish a missing acknowledgment from a missing replacement request.
''')

question(85,'AER Request 數量超過 Controller 上限時，應如何回應？ || What happens when outstanding AERs exceed the controller limit?', 'aer_request',['aerfull','idctrl'],'''
AER 上限限制 controller 必須維護的等待命令數，避免 Host 無限制占用回報資源。這個數量與內部可能發生多少事件不同。 || The limit bounds waiting request resources, not the number of possible events.
上限適用此 controller 同時 outstanding 的 AER，不是整個 subsystem 曾提交過的累計數。 || It applies to concurrent outstanding AERs on this controller, not lifetime submissions across the subsystem.
Identify.AERL 是 zero-based，實際上限為 AERL+1。例如 AERL=3，最多同時保留 4 筆未完成 AER。 || AERL is zero-based: AERL=3 permits four outstanding requests.
Host 追蹤每個 AER 的 CID、提交與完成時間。已完成的 Request 不再占用 outstanding 名額，補送前須先更新追蹤紀錄。 || Track CID and submission/completion times. Completed requests no longer consume the limit; update tracking before replenishing.
先讀 AERL，再建立不超過上限的等待集合。驗證超限行為時，只額外提交一筆，並排除同時有事件完成 Request 的競爭情況。 || Read AERL and post within the limit. For an excess-request test, add one while controlling concurrent event completions that could free a slot.
合法上限內且沒有事件時，Request 正常等待。若同時有一筆完成，後來提交的新 Request 可能仍在合法上限內，不能只看總提交次數判斷。 || Within the limit, requests wait normally. A concurrent completion can make a later request valid; total submission count is insufficient.
超過上限的命令對應 Asynchronous Event Request Limit Exceeded（SCT=1, SC=05h）。不要將它與 Abort Command Limit Exceeded（1/03h）混用。 || Excess AERs use Asynchronous Event Request Limit Exceeded (1/05h), not Abort Command Limit Exceeded (1/03h).
將 AERL+1 與每個時間點的未完成數比對，並保存回報事件造成的名額變化。 || Compare AERL+1 against concurrent outstanding counts and account for slots freed by event completions.
先確認 AERL 已加 1，且 Host 沒把已完成 Request 繼續算在等待集合中。 || First check the +1 conversion and removal of completed requests from the outstanding set.
''')

question(86,'沒有掛入 AER 時發生事件，Controller 如何保留與回報？ || How are events handled when no AER is outstanding?', 'aer_request',['aerfull','getlog'],'''
這题区分事件發生與通知送達。沒有 Request，不表示事件一定沒發生；但也不能要求每種事件都永久排隊等待。 || Distinguish occurrence from delivery. No request does not imply no event, but not every event must wait indefinitely.
一般事件、Immediate 與 One-Shot 的規則不同；還要確認事件原本已啟用，且不是被遮蔽的重複通知。 || Ordinary, Immediate and One-Shot events differ; establish enablement and masking first.
檢查 OAES、FID0Bh、事件種類及 AER outstanding 紀錄。是否支援某個 Log，不足以證明所有相關事件都啟用。 || Check OAES, FID0Bh, event type and request history. Log support alone does not enable every related event.
一般 pending event 保存的是事件資訊，後續用 AER CQE 的 AET／AEI／LID 回覆。Immediate 必須在發生時已有 Request，否則不得回報。 || Ordinary pending information can supply a later AER. Immediate events require an outstanding request at occurrence and must not be reported otherwise.
建立無 Request 的受控期間，再觸發已啟用的一般事件，之後送 AER。期間若成功讀 Log 清除事件，或發生 CLR，就不能再要求後續一定收到原通知。 || Trigger an enabled ordinary event without a request, then post AER. A clearing log read or CLR in between removes the basis for expecting the old notification.
對一般已啟用事件，規範建議保留資訊供下一個 Request 回覆；這是 should，不是對所有種類的無條件永久保留要求。 || For enabled ordinary events, the specification recommends retaining information for the next request. This is should, not unconditional permanent retention for all event classes.
沒有 Request 不會因此產生一筆超限或失敗 CQE。Immediate 未回報若符合上述條件，是規範要求，不能判為遺失事件的韌體缺陷。 || Absence of a request does not create an error CQE. Omitting an Immediate event under these conditions is required, not a firmware notification-loss defect.
比對事件時間、Request 時間、Log 確認及 CLR。只有把這些時間排清楚，才知道通知是否仍應存在。 || Correlate occurrence, request, acknowledgment and CLR times to determine whether a notification should remain pending.
先辨認事件類型，再問有沒有保留；不要對 Immediate 套用一般 pending 規則。 || Identify the event class before applying ordinary pending-event retention.
''')

question(87,'多個相同或不同事件同時發生時，Controller 如何合併與回報？ || How can concurrent identical or different events be combined and reported?', 'aer_request',['aerfull'],'''
通知機制避免每次狀態變動都占用一筆 Request，但仍要讓 Host 找到需要處理的資訊。事件次數、Log entries 與 AER completions 不一定一對一。 || Notification can consolidate conditions while preserving actionable information. Occurrences, log entries and AER completions need not correspond one-to-one.
相同 event type 且回覆內容相同的事件，可以合併；不同種類或不同回覆則有待回報的排隊建議。回報後的自動遮蔽也會影響後續通知。 || Events of the same type with identical responses may be combined. Different types or responses have a queuing recommendation; automatic masking also affects reporting.
先確認每種事件受支援並啟用，並記錄可用 AER 數。只有一筆 Request 時，不能期待多個事件同時各回一筆 completion。 || Establish support/enablement and available request count. One request cannot simultaneously yield several independent completions.
以 AET、AEI、LID 及事件特定參數比較回覆，不要只比 AEI。相同 AEI 在不同類型中可能不是同一事件。 || Compare AET, AEI, LID and event-specific parameters, not AEI alone.
先觸發已知事件集合，逐筆接收並保存回覆，依規則讀 Log 與補 Request。確認後再觀察新的事件，避免把仍被遮蔽的通知當成未偵測。 || Trigger known conditions, preserve responses and process logs/replenish requests. Check acknowledgment before expecting further notifications of a masked type.
相同回覆合併成一筆是 may；保留不同回覆的佇列是 should。規範沒有因此保證 AER 完成順序能還原所有內部事件的精確時間線。 || Combining identical responses is permitted; queuing differing responses is recommended. AER order does not thereby provide a precise timeline of every internal occurrence.
合法合併不應被判為少回 completion 的錯誤。若 Host 同時送入過多 AER，則另依 1/05h 處理，與事件合併無關。 || Legitimate consolidation is not a missing-completion error. Excess requests separately invoke 1/05h handling.
用 Log 的紀錄或 generation 補充通知，而不是把 AER 數量直接當成故障發生次數。 || Use log records or generations to supplement notifications rather than treating AER count as fault count.
先查回覆內容是否相同，以及前一通知是否仍處於自動遮蔽狀態。 || First check identical responses and whether the previous notification remains masked.
''')

question(88,'Asynchronous Event Configuration 如何啟用或遮蔽特定事件？ || How does Asynchronous Event Configuration enable or disable notifications?', 'aer_request',['aec','aerfull','idctrl'],'''
FID0Bh 選擇 Host 希望接收的適用通知。這是通知政策，不會消除裝置已發生的健康問題，也不會自動提交 AER。 || FID0Bh selects applicable notifications. It neither removes the underlying condition nor submits AERs automatically.
設定以 controller 為操作對象，控制指定的 SMART 與選配事件通知。它不是所有 Error 類型事件的總開關。 || It configures specified SMART and optional notifications on a controller, not a universal switch for all Error events.
讀 OAES 與相關能力，確認想啟用的事件受支援，再查 FID0Bh Current。設定支援和當下事件是否仍被遮蔽，是不同狀態。 || Check OAES and applicable support, then Current FID0Bh. Configuration enablement and automatic pending-event masking are separate states.
Set Features.CDW11 的各 bit 選擇事件通知；Get Features 讀回 Current。這份 bitmap 不是 AER completion 的 AET／AEI 編碼。 || Set CDW11 enables notification bits; Get returns Current. The bitmap is not the AET/AEI encoding of an AER completion.
先設定合法的啟用值並等待成功，再讀回確認，確保有 AER 等待，最後建立事件條件。若條件在啟用前已成立，仍須依 Feature 的既有條件規則判斷。 || Set valid bits, await success, read Current, ensure a pending AER and establish the condition. Conditions already true at enablement follow the feature’s rules as well.
成功表示設定已完成；Host 是否收到通知，還取決於事件條件、遮蔽與 Request。停用通知不代表該警告位一定清零。 || Success establishes configuration; delivery still depends on condition, masking and requests. Disabling notification does not necessarily clear the warning itself.
啟用不支援的事件，必須回 Invalid Field（0/02h）。沒有 AER 而暫時收不到通知，不是 Set Features 的失敗 Status。 || Enabling unsupported events returns Invalid Field (0/02h). Lack of an available AER is not a Set Features failure status.
一起比對能力、Current mask、實際警告及 AER。只確認 Set 成功，不足以判斷通知路徑全部正常。 || Correlate support, current mask, actual condition and AER availability. Set success alone does not validate the whole notification path.
先檢查事件是未啟用，還是已回報後等待確認而被自動遮蔽。 || First distinguish disabled notification from automatic masking after a previous report.
''')

question(89,'SMART、Namespace、Firmware、Telemetry、Sanitize、Self-test 與 PEL 各有哪些通知條件？ || What notification conditions apply to SMART, namespaces, firmware, telemetry, sanitize, self-test and PEL?', 'aer_request',['aerfull','smart','dstlog','pel'],'''
這题要校正「每個功能完成都會有一種 AER」的假設。事件必須有規範定義，不能只因功能有 Log，就自行增加完成通知。 || Correct the assumption that every function has a completion AER. Events require an actual specification definition; having a log is insufficient.
事件可能描述 controller 健康、namespace 變更、韌體啟用或 sanitization target。不同 scope 的事件要讀不同資料，不只看接收它的 controller。 || Events can describe controller health, namespace changes, activation or sanitization targets. Match the affected scope, not only the receiving controller.
用 OAES、FID0Bh 與事件表確認選配通知。Device Self-test 支援位與 PEL 支援位，不會自動宣告一個通用的 Self-test Completed 或 PEL Changed AER。 || Use OAES, FID0Bh and event tables. Self-test or PEL support does not automatically define a generic Self-test Completed or PEL Changed AER.
SMART 類型使用 02h；namespace 變更依 Attached／Allocated 分別關聯 04h／1Ch；Firmware Activation Starting 關聯 03h；Telemetry Changed 關聯 08h；Sanitize 類型關聯 81h。 || SMART uses 02h; attached/allocated namespace changes use 04h/1Ch; activation starting uses 03h; telemetry changes use 08h; sanitize events use 81h.
先辨認事件條件，再找對應 Log。Self-test 正常完成應查 06h 的結果；若另符合 Diagnostic Failure 的錯誤條件，才依該 Error 事件處理，不能將兩者等同。 || Identify the event condition before selecting its log. Normal self-test completion is established from 06h; a separately applicable Diagnostic Failure uses the Error event rules.
Sanitize 有完成、非預期 deallocation 與進入 Media Verification 等不同事件，不可全部翻成清除成功。Firmware Activation Starting 也只表示開始，不是最終啟用成功。 || Sanitize distinguishes completion, unexpected deallocation and entry into Media Verification. Activation Starting likewise does not establish final activation success.
某個操作沒有規定完成 AER 時，沒收到通知不是 Status 錯誤。判定漏報前，必須指出具體事件定義、支援、啟用及 Request 條件。 || Absence of an undefined completion event is not an error. A missing-event claim must establish the defined event, support, enablement and request conditions.
將實際操作結果、專用 Log 與 AER 條件分開核對，再以 PEL 的獨立支援事件補充歷史，不要求三者一對一。 || Compare operation results, dedicated logs and AER conditions separately, then supplement with supported PEL events; they need not map one-to-one.
先檢查期待的事件是否真的在本版規格中有定義，而不是由功能名稱推測。 || First verify that the expected event is actually defined in this revision.
''')

question(90,'Host 讀取 Log 後，事件如何清除或保留？ || How does reading a log clear or retain an event?', 'aer_request',['aerfull','getlog'],'''
事件確認控制後續通知是否重新開放，不是刪除全部歷史或修復根本原因。清除通知後，原警告可能仍存在。 || Acknowledgment controls further reporting; it does not erase all history or repair the cause. The underlying warning may remain.
以該事件指定的 Log 與目標為準；讀取另一張 Log，或另一個 namespace 的資料，不一定確認目前這個事件。 || Use the event’s specified log and target. Reading another log or target need not acknowledge it.
先看事件是否採一般讀 Log 確認，還是 Immediate／One-Shot 的特殊方式。只有適用的事件才用 RAE 判讀。 || Establish ordinary log-based acknowledgment versus Immediate/One-Shot behavior before applying RAE.
RAE=0 表示成功完成後清除對應事件；RAE=1 表示保留。LID、NSID 與其他選擇欄位仍要符合事件對應的 Log 規則。 || RAE=0 clears the associated event on success; RAE=1 retains it. LID, NSID and other selectors still must identify the correct log view.
保存通知與原狀態，按需以 RAE=1 讀取，再以適用的 RAE=0 成功讀取確認。不要把任意片段讀取都當成每種 Log 通用的確認方法。 || Preserve notification and state, retain where needed with RAE=1, and acknowledge via the applicable successful RAE=0 read. Do not invent a universal partial-read acknowledgment rule.
成功確認後，事件遮蔽依其規則解除；若狀態持續，後續通知仍可能再次出現。RAE 保留的是事件，不是保證回傳資料從此凍結。 || Successful acknowledgment unmasks as defined; a continuing condition can recur. RAE retains the event, not necessarily a frozen data snapshot.
Get 失敗時，事件必須保留。不能因 Host 寫了 RAE=0，就在 CQE 顯示失敗時仍要求事件消失。 || Failed Gets must retain the event regardless of the requested RAE=0.
比對成功 CQE 的時間、RAE、事件 mask 與後續通知。讀取時與事件發生時的即時值可能不同，不代表確認動作錯誤。 || Correlate successful completion time, RAE, mask state and later notifications. Current state can differ from event-time state without invalidating acknowledgment.
先確認用來確認事件的 Get Log Page 是否真的成功，而不只是已送出。 || First establish that acknowledgment completed successfully rather than merely being submitted.
''')

question(91,'AER 能否被 Abort？Reset 時尚未完成的 Request 如何處理？ || Can AER be aborted, and what happens to pending requests during reset?', 'aer_request',['aerfull','abort','reset'],'''
AER 雖然沒有一般 timeout，仍是有 CID 的 Admin 命令。Host 停止使用事件通道時，要分清楚針對單筆 Request 的 Abort，與重設整個 controller 的處理。 || AER has an Admin CID despite not having an ordinary timeout. Distinguish a targeted Abort from resetting the whole controller.
Abort 以 SQID=0 與目標 AER 的 CID 指定它；Controller Reset 則影響此 controller 的全部 outstanding AER。 || Target the AER with SQID=0 and its CID; controller reset affects all its outstanding AERs.
Abort 的並行上限由 ACL+1 決定，與 AERL+1 不同。沒有特殊的 AER Abort 成功保證，仍要依 Abort 結果判斷。 || ACL+1 limits concurrent Aborts, independently of AERL+1. Aborting AER has no universal success guarantee beyond Abort semantics.
保留 Abort 自己的 CID、目標 CID，以及 CQE.DW0 的 IANP。IANP=0 表示已執行 immediate abort；IANP=1 不代表目標從此不會被 deferred abort。 || Track the Abort CID, target CID and IANP. IANP=0 identifies immediate abort; IANP=1 does not rule out a later deferred abort.
送出 Abort 後，分別處理 Abort 與目標 Request 的結果。如果改採 Reset，則依重設規則終止舊追蹤，恢復後建立新的 AER，不能等待重設中止的舊 Request 回 CQE。 || Process Abort and target results separately. If resetting instead, terminate old tracking under reset rules and post new AERs after recovery without waiting for reset-aborted CQEs.
Abort 可能和事件完成競爭：目標可能先正常回報事件。真正被 Abort 的目標回 Command Abort Requested；被 Controller Reset 中止的 AER 則不得回 CQE，兩種情況不同。 || An event can win the race and complete normally. An aborted target reports Command Abort Requested; a controller-reset-aborted AER must not return a CQE. These outcomes differ.
Abort 超限可回 Abort Command Limit Exceeded（1/03h）。目標已完成或未找到時，不能一律要求 Abort 本身失敗；應讀 IANP，並確認是否已有目標 completion。 || Excess Abort commands may return 1/03h. A missing/already-completed target does not universally make Abort fail; inspect IANP and target completion history.
核對同一 Admin Queue 使用期間內的 CID，避免 Reset 後重用 CID 時，把新 Request 當成舊 Abort 的目標。 || Correlate CIDs within one Admin Queue lifetime so reused post-reset CIDs are not mistaken for old targets.
先辨認 Request 是由 Abort 結束、事件完成，還是被 Reset 中止，再決定應不應有 CQE。 || First identify event completion, Abort or reset termination before deciding whether a CQE is expected.
''')

question(92,'AER 已完成，但對應 Log 看不到預期資訊時，應如何定位？ || How should an AER be investigated when the associated log lacks expected information?', 'aer_request',['aerfull','getlog','smart','error'],'''
通知描述曾發生的條件，Log 則可能描述目前狀態或有限歷史，因此兩者不一定是同一時點的副本。先找出資料類型，才能判斷是真的不一致。 || Notifications describe an occurrence; logs may show current state or bounded history rather than a same-time copy. Identify the data model before claiming inconsistency.
固定 controller、事件 target 與讀取介面。共用資源的狀態可能已由另一個 Host 讀取或確認，不能只看本地程式紀錄。 || Fix controller, target and interface. Another host may have read or acknowledged shared state outside the local trace.
核對 AET／AEI 的規範定義與 LID，再查支援能力及 Log 的更新、清除與保留規則。不要先假設每個事件都新增一筆 entry。 || Check the event definition/LID and the log’s update, clearing and retention rules. Not every event creates an entry.
保留原 CQE、RAE、LID、NSID、LSI、讀取時間與有效欄位。SMART Critical Warning 反映處理 Get 時的狀態，可能已不同於事件發生時。 || Preserve CQE, selectors, RAE, time and valid fields. SMART Critical Warning reflects Get processing time and may differ from event-time state.
先排除讀錯 Log 或對象，再檢查其他讀取、重設、generation 變化及 transient condition 已恢復。最後才比對規範是否要求仍能查到特定資訊。 || Exclude wrong log/target, intervening reads/reset, generation changes and recovered transient conditions before testing a specific retention requirement.
例如溫度曾達門檻而觸發事件，稍後讀 SMART 時溫度已降低，兩者可以同時正確。相反地，More=1 的命令錯誤應有可關聯的補充資訊，須用相應規則檢查。 || Temperature can trigger an event and fall before SMART is read. Conversely, a More=1 command error calls for correlatable supplemental information under its own rules.
沒有預期資料不會自動改變已成功的 AER Status。若後續 Get 失敗，保留那筆命令的獨立錯誤，不能把兩筆結果混成一個。 || Missing expected data does not rewrite the successful AER status. Preserve a subsequent Get failure separately.
完整結論要指出事件條件、Log 的資料時點及所有中間動作。只有在保留前提都成立時仍缺少必要資訊，才形成可驗證的矛盾。 || Establish the event condition, log time model and intervening actions. A contradiction requires the relevant retention preconditions to hold.
先檢查 Log 是即時狀態還是事件歷史，這決定它是否必須保留事件當時的數值。 || First distinguish current-state logs from event history; that determines whether event-time values must remain visible.
''')
