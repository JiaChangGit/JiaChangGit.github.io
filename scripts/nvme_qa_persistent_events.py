"""Q205–216: persistent history, stable reporting contexts and clocks."""
from scripts.nvme_qa_extension import question
from scripts.nvme_qa_model import COMMON, REFS, pair
REFS['pelcontext']='B|5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)|270-282,284|232–244, 246'
REFS['nvmpel']='N|4.1.4.4|76-77|112'
COMMON['pel_query']={**COMMON['command'],**COMMON['log_query'],
 9:pair('Base 2.4 沒有「每新增 PEL entry 就回報 PEL Changed AER」的一般事件。造成紀錄的原始狀況可能有自己的通知，例如 SMART 警告或 Sanitize；必須依原始事件的條件判斷。 || Base 2.4 does not define a generic PEL Changed AER for every appended entry. The underlying condition may have its own SMART, Sanitize or other notification rules.'),
 10:pair('建立 context 固定這次要回報的事件集合；期間新事件仍要記錄，但不能混入既有 context。讀取或釋放 context 不代表清空 PEL，錯誤的 Get Log 則另依 Error Information 規則處理。 || A context fixes the reported event set. New events remain logged but shall not enter that context. Reading/releasing a context does not erase PEL; failed reads use ordinary error-log rules.'),
 11:pair('PEL 的查詢不是另一筆 PEL 讀取事件。只有受支援的原始事件才依各自觸發條件記錄；高頻相同事件可依規範允許的廠商門檻抑制，不能要求無限逐筆重複。 || PEL retrieval is not itself a PEL read event. Supported underlying events follow their triggers, with permitted vendor-threshold suppression of frequent repeated events.'),
 12:pair('Controller Level Reset 後，PEL 事件內容須保留，但查詢 context 不保證仍有效。恢復查詢通道後重新建立 context，不能把中斷前的半份資料接上新的 context。 || Event content survives CLR; the reporting context need not. Re-establish it after recovery instead of joining partial data across contexts.'),
 13:pair('Subsystem Reset 不清除持久事件；Reset 完成時還可能依支援規則新增 Power-on or Reset 事件。報告 context 的保留是另一回事，應重新建立一致的讀取範圍。 || Subsystem reset preserves events and may add the supported Power-on or Reset event at completion; establish a fresh consistent reporting context.'),
 14:pair('事件內容須跨 Power Cycle 保留，規範也建議設計盡量降低失電時的事件遺失。容量淘汰、高頻抑制，以及 Sanitize 為避免洩漏使用者資料而移除或修改事件，是不同的例外，不能把它們誤認為一般斷電清空。 || Events persist across power cycles, with minimal power-failure loss recommended. Capacity eviction, repeated-event suppression and Sanitize-related privacy removal are distinct from ordinary power-cycle clearing.'),
 15:pair('PEL 是 subsystem 全域的事件歷史。事件 Header 的 CNTLID 指出建立紀錄的 controller；影響多個 controller 的事件建議只記一次，不要求每條路徑都有一份副本。共享查詢 context 時須避免一端釋放另一端仍在讀的 context。 || PEL is subsystem-global. CNTLID identifies the recording controller; multi-controller events should be logged once. Coordinate readers so one does not release a context still used by another.')}

def q(n,t,r,b,o=None): question(n,t,'pel_query',r+['pelcontext','timestamp','nvmpel'],b,o)

q(205,'如何確認 Persistent Event Log 及個別事件的支援能力？ || How is PEL and individual event support established?', ['idctrl','getlog'], '''
先確認整份 Log，再確認事件種類，才能判斷缺少紀錄是否合理。支援 PEL 不表示所有選配事件都必須實作。 || Establish log support and then event support; PEL support does not require every optional event.
PEL 是 NVM subsystem 全域資訊；Header 中的 controller 識別不會把它變成私有 Log。 || PEL is subsystem-global despite controller identifiers in its entries.
查 Identify.LPA 的 PEL 支援位元、PELS 的最大容量，以及 Supported Log Pages 對 LID0Dh 的宣告。建立 context 後再看 Supported Events Bitmap。 || Check LPA, PELS and LID0Dh support, then the header’s Supported Events Bitmap.
PELS 以 64 KiB 為單位；ECRH 表示 ACT=3 與 GNUM 支援。符合 Base 2.0 以後版本且支援 PEL 的實作必須設 ECRH=1。 || PELS uses 64 KiB units. ECRH supports ACT=3 and GNUM and is required for PEL implementations conforming to Base 2.0 or later.
確認 Log 能力後讀 Header，依事件支援及命令支援核對必要事件，再設計測試。 || Read the header and map mandatory/conditional events before testing.
取得支援矩陣，而不是只得到「有／沒有 PEL」一個結論。 || Obtain an event support matrix rather than one yes/no log result.
不支援的 LID 使用 Invalid Log Page 等對應錯誤；不能因某個選配事件未宣告就判定整份 Log 違規。 || Unsupported logs follow Invalid Log Page handling; an unadvertised optional event does not invalidate the log.
Figure 233 的 bitmap 將 bits221:16 列保留，但 Figure 236 又列 ET10h，這是來源內部不一致；涉及該事件時須保留差異，不自行編造一致的位元表。 || Figure 233 reserves bits 221:16 while Figure 236 defines ET10h. Preserve this source inconsistency rather than inventing a reconciled bitmap.
先檢查測試期待的事件是 mandatory、依命令支援而 mandatory，還是 optional。 || First classify the expected event’s support requirement.
''')
q(206,'PEL Context 如何建立、分段讀取與釋放？ || How is a PEL context established, read and released?', ['getlog'], '''
Context 固定一份可一致讀取的事件集合，避免大型 Log 在分段傳輸期間被新事件改變內容。 || A context stabilizes an event set while a large log is read in segments.
Context 是這次回報的視圖，不是停止 controller 記錄新事件。 || It is a reporting view, not suspension of event recording.
確認 LID0Dh、ECRH 與 Header 的 TLL、LHL、GNUM、RCI。 || Check LID0Dh, ECRH and TLL/LHL/GNUM/RCI.
ACT=1 建立並讀取；ACT=0 讀既有 context；ACT=2 釋放；ACT=3 建立或沿用 context 並固定回 512-byte Header。 || ACT1 establishes/reads, ACT0 reads, ACT2 releases and ACT3 establishes/reuses with a fixed 512-byte header.
先 ACT=3 讀 Header，記錄 GNUM；依 TLL 用 ACT=0 與 LPO 分段讀取，讀完再讀 GNUM，確認相同後 ACT=2 釋放。 || Read the header with ACT3, retain GNUM, fetch segments with ACT0/LPO, recheck GNUM and release with ACT2.
各段來自相同 context；期間新發生事件留待下一次 context 回報。ACT=3 的 buffer 至少配置 512 bytes。 || Segments share a context; newly logged events appear in a later context. Allocate at least 512 bytes for ACT3.
ACT=0 無 context 或 ACT=1 已有 context，須回 Command Sequence Error。ACT=2 沒有 context 也不是錯誤。 || ACT0 without a context or ACT1 with one requires Command Sequence Error; ACT2 without one is not an error.
GNUM 不一致時，已讀資料可能無效，Host 應重新讀取，不能只補最後一段。 || A changed GNUM means the assembled data may be invalid and should be reread.
先確認每段 ACT、LPO 與 GNUM，避免把不同 context 的資料拼在一起。 || First compare ACT, offsets and generation across segments.
''')
q(207,'Context 不存在或重複建立時，應如何回應？ || What happens for absent or duplicate PEL contexts?', [], '''
原題的「超過 context 數量上限」應改成檢查 ACT 與既有 context。這套介面沒有讓 Host 任意建立帶不同 ID 的 context 清單。 || Replace the presumed context-count limit with ACT/existing-context rules; this interface does not create an arbitrary list of host-selected context IDs.
判斷的是處理命令當下，是否已有 persistent reporting context。 || Evaluate context existence when the command is processed.
使用 ACT=3 的 RCE 與 RCPIT／RCPID，了解既有 context 及建立來源。 || Use ACT3 RCE and reporting-port information to inspect an existing context.
RCE=0 代表這次命令處理前沒有 context；ACT=3 仍會建立成功，不能把 0 翻成建立失敗。 || RCE=0 means none existed before processing; ACT3 still successfully establishes one.
需要沿用就 ACT=0；要取得新事件集合，先協調讀者，再 ACT=2 釋放並重新建立。 || Read with ACT0; coordinate readers before release/re-establishment for a fresh set.
ACT=3 不論原本是否存在都成功回 Header，RCE 區分先前狀態；ACT=2 可重複釋放。 || ACT3 returns a header in either case, with RCE distinguishing prior state; repeated ACT2 release is allowed.
ACT=1 重複建立與 ACT=0 無 context 都是 Command Sequence Error，不能替這兩種條件改用假想的資源數量錯誤。 || Duplicate ACT1 and absent-context ACT0 require Command Sequence Error, not an invented resource-count status.
把 CQE 成功與 RCE 的前置狀態放在一起解讀，兩者並不矛盾。 || Successful CQE and RCE describing prior state are compatible.
先檢查是否把 RCE 誤解成命令執行後的「目前已建立」布林值。 || First check whether RCE was mistaken for a post-command existence flag.
''')
q(208,'SMART、Firmware、Timestamp、Reset 與 Hardware Error 如何記錄？ || How are key PEL event classes recorded?', ['fwpel','smart'], '''
每類事件有不同觸發點與資料格式；辨認事件後才能決定哪個欄位能回答問題。 || Each event has its own trigger and payload; decode type before interpreting fields.
Header.CNTLID 標示記錄來源；多 controller 的共同事件建議只記一次，事件資料可列多個 controller。 || CNTLID identifies the recorder; shared events should be recorded once and may describe several controllers.
確認 PEL 與所需事件支援；PCIe 的 SMART Snapshot 是 PEL 支援後的必要事件。 || Establish event support; SMART snapshots are required for PCIe implementations supporting PEL.
ET01h 帶 512-byte SMART 快照；02h 帶 Firmware Commit 的 action、slot、status 與 requested revision；03h 帶變更前時間；04h 帶 reset descriptors；05h 以硬體錯誤代碼選 payload。 || ET01 carries SMART; 02 commit action/slot/status/requested revision; 03 previous time; 04 reset descriptors; 05 code-selected hardware data.
先讀 ET、ETR、EL，再按該格式解析。SMART 快照至少每 24 power-on hours 記錄一次；Reset 事件於重設完成時記錄。 || Decode ET/ETR/length first. SMART snapshots occur at least once per 24 power-on hours; reset events are logged on completion.
Firmware NFR 代表要求啟用的版本，不保證已啟用；Reset descriptor 的 FA 能補充有無啟用及是否失敗。 || Firmware NFR is the requested revision, not proof of activation; reset FA supplies activation outcome.
硬體錯誤只要求記錄已支援且符合條件者，並有高頻抑制例外；不能要求每個命令 Invalid Field 都有硬體錯誤事件。 || Supported qualifying hardware errors are logged subject to suppression; an Invalid Field command error need not be a hardware event.
使用實際 CQE、Identify.FR、SMART 快照與事件 payload 互證，避免只憑事件名稱猜結果。 || Correlate CQEs, FR, SMART and payload rather than event names alone.
先確認使用的 ETR 與 payload 格式一致，並分清「要求」與「完成」。 || First check event revision and distinguish requested action from completed effect.
''')
q(209,'Namespace、Format 與 Sanitize 對應哪些 Persistent Events？ || Which persistent events describe namespace, format and sanitize operations?', ['nspelevent','formatpel','sanitizepel'], '''
管理操作的開始與完成可能相隔很久，需要不同事件才能重建過程。 || Long management operations need distinct start and completion evidence.
Namespace 事件辨認目標 NSID；Format 與 Sanitize 還要依命令判斷單一 namespace 或較廣範圍。 || Identify NSID and command-specific namespace or wider scope.
確認操作支援與事件支援；PEL 的條件性必要事件隨對應命令能力判斷。 || Check command capability and conditionally mandatory PEL event support.
ET06h 記 Namespace Create／Delete；07h、08h 為 Format Start／Completion；09h、0Ah 為 Sanitize Start／Completion。NVM 的 FLBAS、DPS 解釋來自 NVM Command Set。 || ET06 records namespace create/delete; 07/08 format start/completion; 09/0A sanitize start/completion. NVM defines FLBAS/DPS interpretation.
以目標、action、開始資料與完成資料配對；Attach／Detach 不是 Namespace Create／Delete，不應硬套 ET06h。 || Pair target/action and start/end data; Attach/Detach are not ET06 create/delete operations.
Format completion 需連 FNVMS 與 INFO 判讀；Sanitize 進入 Media Verification 並不等於已產生正常最終完成事件。 || Interpret Format with FNVMS/INFO; entering Sanitize Media Verification is not final completion.
Reset 導致沒有 Format CQE 時，不能把紀錄中保留或零值 Status 當成成功證明。 || If reset prevented a Format CQE, absent/zero status evidence is not proof of success.
NVM Namespace 刪除全部時，FLBAS／DPS 保留；單一刪除則描述被刪前的格式，不能在物件消失後仍要求 Identify 可讀。 || FLBAS/DPS are reserved for delete-all; single deletion describes the former format, not an object still available to Identify.
先檢查這筆紀錄是 Start 還是 Completion，以及完成資料是否真的有效。 || First distinguish start from completion and validate outcome fields.
''')
q(210,'PEL 達容量上限時，舊事件如何處理？ || How are events removed when PEL reaches its limits?', [], '''
PEL 有容量限制，Host 不能假設所有事件從出廠開始永久逐筆保存。 || PEL is bounded; not every event is retained forever.
限制可能來自總 bytes、總事件數，或個別事件類別的內部容量。 || Limits may be total bytes, event count or per-category capacity.
查 PELS、TLL、TNEV 與產品的廠商定義政策；Header 的目前數量不是終身發生次數。 || Check PELS, TLL/TNEV and vendor policy; current count is not lifetime occurrence count.
到達限制後，刪除哪些事件由廠商決定，可能保留較舊但較重要的紀錄；不保證嚴格 FIFO。 || Eviction is vendor-specific and may retain older important events rather than strict FIFO order.
取得前後兩份完整 context，按事件內容比對，再考慮容量淘汰、高頻抑制與 Sanitize 的影響。 || Compare complete contexts and account for eviction, frequency suppression and Sanitize.
Controller 可回報仍保留的有效集合；事件數沒有單調增加，不足以單獨判定資料遺失違規。 || A valid retained set need not have a monotonically growing count.
規範建議容量足以支應使用壽命，但這是 should；不能改寫成永遠不得淘汰的 shall。 || Lifetime-sized capacity is a should, not a prohibition on all eviction.
GNUM 表示新 context 的內容相較前次改變，不是累計事件總數；兩者不應混算。 || GNUM tracks changed content at context establishment, not total event occurrences.
先確認是否已達任一廠商定義限制，而不是只檢查 TLL 是否剛好等於 PELS。 || First consider all limits, not only whether TLL equals PELS.
''')
q(211,'PEL 新增事件後，是否一定發送 Asynchronous Event？ || Does a new PEL event require an asynchronous notification?', ['aerfull','aec'], '''
本題要修正「有持久紀錄就一定有即時通知」的假設，這是兩條不同的回報途徑。 || Correct the assumption that persistent recording always implies immediate notification.
PEL 提供跨重設歷史；AER 回報受支援且符合通知條件的即時事件。 || PEL provides persistent history while AER reports eligible asynchronous conditions.
分別查 Supported Events Bitmap 與 AER/AEC 的支援設定，不能拿 PEL bitmap 當 AER 遮罩。 || Check PEL support separately from AER/AEC; the event bitmap is not an AER mask.
例如 SMART Critical Warning 可能同時符合 PEL hardware event 與 SMART AER；一般 Timestamp Change 則沒有因此定義一個 PEL Changed 通知。 || A critical warning may qualify for both mechanisms; Timestamp Change does not create a generic PEL Changed notification.
先找造成 PEL 紀錄的原始事件，再檢查它是否另有 AER 類型、設定、遮蔽與 request 條件。 || Identify the underlying event and then its separate AER type, enablement, masking and request requirements.
可能只看到 PEL，也可能兩者都有；須按事件種類而不是按「Log 改了」判定。 || PEL-only or dual reporting may be correct depending on the underlying event.
沒有規範定義的通知時，不能要求回報自行命名的 AER，或把沒有 AER 判成命令錯誤。 || Do not invent a notification or command error where none is defined.
為每個測試列出兩條獨立預期：是否記錄，以及是否通知。 || Record separate expectations for logging and notification.
先檢查測試是否把不存在的一般 PEL Changed AER 當成必需。 || First check whether the test assumes a nonexistent generic PEL Changed AER.
''')
q(212,'Reset 與 Power Cycle 後，PEL 哪些東西應保留？ || What persists in PEL across resets and power cycles?', [], '''
要分清持久事件與暫時的讀取 context：事件保留不表示查詢可以從中斷處無條件接續。 || Persistent events and temporary reporting contexts have different lifetimes.
持久性涵蓋 subsystem 的事件內容；context 則服務一次一致的報告讀取。 || Persistence protects subsystem history; a context serves one consistent retrieval.
保存重設前的完整 Header、事件資料與 GNUM，重設後重新建立 context。 || Save a complete pre-reset view and establish a new context afterward.
新 Header 的時間、GNUM、事件數可能改變；新增 Power-on or Reset entry 也會改變低 offset 的事件排列。 || Header time, generation, count and offsets may change, including from a new reset event.
按事件內容與來源關聯前後紀錄，不要求同一事件永遠位於同一 byte offset。 || Correlate event identity/content rather than demanding fixed offsets.
原有持久事件依保留規則仍可讀；context 若已失效，就重新開始一致的讀取。 || Persisted events remain subject to retention rules; an expired context requires a fresh read.
不能把舊 context 的 Command Sequence Error 當成 PEL 已清空。容量淘汰、抑制或 Sanitize 也需獨立排除。 || A stale-context sequence error does not prove erased history; assess eviction, suppression and Sanitize separately.
用新 context 取得的完整資料驗證事件，而不是只檢查 Reset 前後第一筆是否相同。 || Validate the complete fresh view rather than only the first entry.
先確認消失的是事件本身，還是只失去讀取 context。 || First distinguish missing history from missing context.
''')
q(213,'PEL 的 Header、長度與事件順序如何驗證？ || How are PEL headers, lengths and ordering validated?', [], '''
PEL 是可變長度紀錄，錯算一個長度會讓後面每筆事件都解析錯位。 || One length error can misalign every subsequent variable-length event.
先區分「整份 Log」與「單筆事件」兩層資料。Log Revision（LREV）指出整份 Log 的格式版本；每筆事件內的 Event Type Revision（ETR）則指出該類事件資料的格式版本。兩者不是同一個版本欄位，解析時要分別確認。 || Distinguish the whole log from individual events. Log Revision (LREV) identifies the overall log format, while each Event Type Revision (ETR) identifies the format of that event type. Validate both rather than treating them as one version.
先由 Identify Controller.LPA 確認 PEL 支援能力，再讀 Log Header。Total Log Length（TLL）是整份資料的 bytes 數，Total Number of Events（TNEV）是事件筆數；Log Header Length（LHL）用來計算第一筆事件從哪裡開始，Generation Number（GNUM）則用來辨認 Log 是否已更新。界定整份資料後，再檢查每筆事件的長度。 || Confirm PEL support through Identify Controller.LPA, then read the log header. Total Log Length (TLL) counts log bytes and Total Number of Events (TNEV) counts entries. Log Header Length (LHL) locates the first event, while Generation Number (GNUM) helps detect updates. Establish these bounds before parsing individual events.
LHL 的計算起點是 Log 的 byte 20，因此 Log Header 總長為 LHL+20。每筆事件的 Event Header Length（EHL）也不包含最前面的3 bytes，所以事件標頭總長為 EHL+3。Event Length（EL）描述標頭後方的資料，且已包含 Vendor Specific Information Length（VSIL）指定的廠商資訊；因此整筆事件長度是 EHL+3+EL，而扣除廠商資訊後的 Event Data 長度是 EL−VSIL。 || LHL starts counting at log byte 20, so the full log header occupies LHL+20 bytes. Event Header Length (EHL) similarly excludes the first three event bytes. Event Length (EL) covers data after the event header and already includes the vendor information counted by Vendor Specific Information Length (VSIL). Total event length is EHL+3+EL; event data excluding vendor information is EL−VSIL.
從 Header 結尾開始，依每筆總長前進並檢查界限。例如 EHL=21、EL=20、VSIL=4，整筆 44 bytes，其中 Event Data 為 16 bytes。 || Advance by validated lengths. With hypothetical EHL=21, EL=20 and VSIL=4, the event is 44 bytes with 16 bytes of event data.
解析完 TNEV 筆事件後，所有已解析的事件都應落在 TLL 指定的有效資料範圍內。每筆事件不保證從4-byte對齊的位置開始，因此不能擅自插入 padding，否則下一筆事件的起點就會算錯。 || Walk the reported events within bounds; individual events are not guaranteed four-byte aligned.
若 VSIL>EL，表示宣告的廠商資訊比包含它的資料範圍還大；若事件結尾超過 TLL，則表示解析結果已超出整份 Log。這兩種情況都需要檢查長度欄位與取得的資料是否一致。Get Log Page 的傳輸對齊要求，不會讓每筆事件自動變成相同長度。 || VSIL>EL or an event beyond TLL is inconsistent; transfer alignment does not make events fixed-size.
較新事件建議放較低 offset，但發生順序判定由廠商決定；Timestamp 可改變，不能直接依數值重排後宣稱原 Log 錯誤。 || Newer-first ordering is recommended with vendor-defined occurrence ordering; timestamp changes prevent simplistic numeric sorting.
先檢查是否重複把 VSIL 加進總長，或漏了 EHL 的 +3。 || First check double-counted VSIL and the EHL+3 rule.
''')
q(214,'Timestamp 如何設定並以 Get Features 驗證？ || How is Timestamp set and verified?', ['feature','getfeat','setfeat'], '''
Timestamp 讓 Host 提供事件關聯用的時間基準；它不保證可作安全用途，也不是所有 controller 共用的一只時鐘。 || Timestamp supplies a host time basis for correlation, not a security clock or automatically shared clock.
設定作用於目標 controller；跨 controller 比對仍需處理時間差與 Reset 資訊。 || It targets a controller; cross-controller correlation needs offsets and reset evidence.
查 Identify.ONCS 的 Timestamp 支援，以及 FID0Eh 的保存能力。 || Check ONCS Timestamp support and FID0Eh saveability.
Set 傳 8-byte buffer，bytes5:0 為自 1970-01-01 UTC 起的毫秒數，bytes7:6 保留；Get 多回 Timestamp Origin 與 SYNC。 || Set uses an eight-byte buffer with a 48-bit UTC-epoch millisecond value; Get adds Origin and SYNC.
先記錄 Host 時間，送 Set 並等成功，再 Get Current；比較時容許已經過的時間，而不是要求與 Set 值逐 byte 相等。 || Record host time, await successful Set, then Get Current with elapsed time accounted for.
Origin=001b 表示由 Set Features 初始化；回值為設定值加上 controller 計入的經過時間。 || Origin=001b marks Set Features initialization; value includes counted elapsed time.
不支援的 Feature、非法欄位或 Save 要求依各自 Feature 錯誤回應。不能把失敗 Set 當成時鐘已更新。 || Unsupported/invalid/save failures follow feature status rules; a failed Set does not establish an update.
比較設定、Origin、SYNC 與讀取時間點，再決定差值是否合理。 || Compare setting, Origin, SYNC and read timing together.
先檢查傳輸的是毫秒，不是秒，並確認只有低 48 bits 是 Timestamp。 || First check milliseconds versus seconds and the 48-bit encoding.
''',{9:'Set Timestamp 本身沒有一般的成功 AER；事件時間可能因此改變，但不代表須送出 PEL Changed 通知。 || Set Timestamp defines no generic success AER or PEL Changed notice.',10:'成功 Set 後 Get Current 應反映新時間基準；Error Information 仍依命令失敗與記錄條件處理。 || Get Current reflects a successful new time basis; error records follow command-error rules.',11:'Timestamp 使用專屬 Timestamp Change Event，不得記成一般 Set Feature Event。 || Timestamp uses its dedicated Change event and shall not be recorded as a generic Set Feature event.',12:'若此種 CLR 保持 Timestamp 持續計時，就必須保留 Origin；不保持時則依 Timestamp 的初始化／保存規則重新判讀。 || A CLR method that maintains the running timestamp shall preserve Origin; otherwise apply its initialization/saved-value rules.',13:'對每個受重設 controller 分別檢查 Timestamp 是否持續及 Origin；不能假設 subsystem 中所有時鐘數值完全相同。 || Check continued counting and Origin per affected controller, not assumed equality across the subsystem.',14:'若功能可保存且曾保存，恢復的是 Saved 值，時間可能向後跳；不能要求斷電期間仍一定連續增加。 || Restoring a saved value can move time backward; uninterrupted counting through power loss is not guaranteed.',15:'設定一個 controller 的時間不代表替所有 controller 校時。 || Setting one controller does not synchronize every controller.'})
q(215,'Timestamp 如何增加、Wrap-around，Origin 與 SYNC 怎麼看？ || How do Timestamp counting, wrap-around, Origin and SYNC work?', [], '''
同樣的數字可能是 UTC 時間，也可能只是 Reset 後經過時間；必須先解讀屬性。 || The same number can represent host-set epoch time or time since reset; interpret attributes first.
48-bit 值屬於該 controller 的時間基準，不能直接推論跨 controller 的絕對先後。 || The 48-bit value belongs to that controller’s time basis.
Get FID0Eh Current，讀 Timestamp 及 TSTMPS；需要歷史變更時搭配 PEL 的 Timestamp Change。 || Read Current Timestamp/TSTMPS and historical changes from PEL.
Origin=000b 表示 CLR 初始化為 0；001b 表示 Host Set 初始化。SYNC=0 表示初始化後連續計毫秒；SYNC=1 表示可能省略廠商定義的時間區間。 || Origin000 means reset initialization and 001 host initialization. SYNC0 means continuous millisecond counting; SYNC1 permits omitted intervals.
先確認 Origin，再算經過時間；設定值加經過時間超出 48 bits 時，回報值應以 2^48 取模。 || Establish Origin, then elapsed time; overflow should be reduced modulo 2^48.
在相同基準且沒有其他變更時，差值可按 48-bit 模數計算；SYNC=1 則不能要求與壁鐘完全一致。 || Modular differences work within the same basis; SYNC1 prevents demanding wall-clock equality.
時間變小可能是 Wrap-around、重設、恢復 Saved 或重新 Set，不必然代表計數器壞掉。 || A smaller value may reflect wrap, reset, saved restoration or a new Set rather than corruption.
用 Origin、SYNC、Reset 事件與 Timestamp Change 排除基準切換後，再比較先後。 || Use attributes and change/reset events before ordering timestamps.
先檢查比較的兩個時間點是否仍屬同一個時間基準。 || First establish that both values share one time basis.
''')
q(216,'Timestamp 變更如何記錄，Reset 與 Power Cycle 後怎麼判讀？ || How are Timestamp changes and reset outcomes interpreted?', ['feature'], '''
事件時間會因校時而不連續，Timestamp Change 提供連接新舊時間基準的資訊。 || Timestamp Change connects discontinuous old and new time bases.
變更與 Reset 都要依相關 controller 判讀，不能把整個 subsystem 當成單一時鐘。 || Interpret changes and resets per controller rather than assuming a subsystem clock.
確認 Timestamp 與 PEL 支援，保存目前值、Origin、SYNC、Saved 及 Reset 來源。 || Check support and preserve current attributes, saved value and reset source.
ET03h 的 Header 時間描述新時間，PTSTP 保存變更前時間，MSR 表示距上次 CLR 的毫秒數。 || ET03 header uses the new time; PTSTP records the prior value and MSR the time since CLR.
先用 PTSTP 與 Header 建立新舊基準關係，再用 MSR、Power-on or Reset descriptors 比對控制器間的觀察。 || Relate old/new values, then use MSR and reset descriptors for correlation.
若 CLR 持續維持 Timestamp，Origin 也必須保留；若不維持，須按初始化與可能的 Saved 恢復重新解讀。 || A CLR retaining the running clock preserves Origin; otherwise account for initialization and any saved restoration.
不能把校時造成的時間倒退判成 PEL 順序違規，也不能把 Timestamp 記成 ET0Bh 的普通 Set Feature 事件。 || A backward clock adjustment does not prove event-order violation; Timestamp shall not use generic ET0Bh Set Feature logging.
重設後的 Get、Timestamp Change 與 Power-on or Reset 應能形成合理的時間解釋，但不能假設所有事件時間都單調增加。 || Get and change/reset events should support a coherent explanation without assuming all timestamps monotonically increase.
先檢查時間是否被重新設定或恢復 Saved，再調查事件排序。 || First check clock updates or saved restoration before event ordering.
''',{11:'Timestamp Change 以 ET03h 記錄，普通 Set Feature Event 明確不適用此 FID。 || Timestamp changes use ET03h; generic Set Feature logging explicitly excludes this FID.'})
