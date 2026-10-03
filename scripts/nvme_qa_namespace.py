"""Q157–173: allocation, attachment and write protection are distinct state."""
from scripts.nvme_qa_extension import question

def q(n,t,r,b,o=None): question(n,t,'namespace_op',r+['nsattach','idctrl','idlist','nspelevent'],b,o)

q(157,'如何確認 Namespace Management 與 Attachment 支援？ || How are namespace management and attachment supported?', ['commandseffects'], '''
Management 建立／刪除 namespace，Attachment 決定哪些 controller 能使用它。這兩項能力相關，但不完全等價。 || Management creates/deletes namespaces; attachment controls controller access. The capabilities are related but not equivalent.
配置存在於 subsystem；active 存取則以各 controller 為準。 || Allocation is subsystem inventory; active access is controller-specific.
Identify.OACS.NMS=1 表示支援 Management，也必須支援 Attachment；NMS=0 的 controller 仍可能單獨支援 Attachment，應查 Command Effects。 || NMS1 requires both commands; NMS0 can still support attachment alone, discoverable through Command Effects.
Namespace Management Opcode0Dh，Attachment15h；前者 SEL 選建立／刪除／恢復，後者選 Attach／Detach。 || Opcodes0Dh and 15h have different SEL action definitions.
先確認命令支援，再探索 namespace 與 controller 清單，最後建立需要的管理操作。 || Establish command support, enumerate objects and construct the intended operation.
宣告 NMS 後，兩種命令及相關變更通知能力應符合要求；單獨 Attachment 支援不代表可建立新 namespace。 || NMS entails both command capabilities; attachment-only support does not authorize creation.
不支援命令用相應 Opcode 錯誤；支援命令但不支援 Restore Default 操作用 Invalid Field，不能把整個 Management 判成不支援。 || Distinguish unsupported opcode from unsupported Restore Default action, which uses Invalid Field.
交叉比對 OACS、Effects.CSUPP 及合法操作，不只看一個位元。 || Cross-check OACS, CSUPP and valid behavior.
先確認是否誤把 NMS=0 解成 Attachment 一定不支援。 || First check the mistaken implication that NMS0 forbids attachment.
''')

q(158,'建立 Namespace 時 NSZE、NCAP、Format 與 Thin Provisioning 如何設定？ || How are size, capacity, format and thin provisioning selected?', ['nvmcreate','idns'], '''
NSZE 決定可定址範圍，NCAP 決定可配置的 logical blocks；兩者都使用選定格式的 block 單位，不是 bytes。 || NSZE defines address range and NCAP allocatable logical blocks, both in the selected format’s units.
建立新 namespace 會消耗其 NVM Set／Endurance Group 的容量，但尚未附加任何 controller。 || Creation consumes selected resources without attaching the new namespace.
查共同 namespace 能力、格式清單、thin provisioning 支援與未配置容量；有 granularity 資訊時一併使用。 || Inspect common capabilities, format list, thin provisioning, unallocated capacity and reported granularity.
填 NSZE、NCAP、FLBAS、DPS、NMIC 及需要的資源 IDs。NCAP 不得大於 NSZE；使用小於 NSZE 的 NCAP 需要相應 thin provisioning 支援。 || Set NSZE/NCAP/FLBAS/DPS/NMIC and resource IDs. NCAP cannot exceed NSZE; smaller capacity requires thin-provisioning support.
先選格式再換算 blocks。假設 1000 個4KiB blocks，就是4000KiB使用者容量；實際 NVM allocation 可能因配置單位而更大。 || Select format before conversion:1000×4 KiB=4000 KiB user capacity, while physical allocation can be larger.
Create 成功 CQE.DW0 回 NSID，並以指定屬性格式化；再查 Identify 確認，之後才 Attach。 || Successful creation returns NSID in DW0 and formats the namespace; verify before attachment.
非法格式回 Invalid Format；不支援 thin provisioning 有專屬狀態；資源不足另分容量與 NSID 上限。 || Invalid format, unsupported thin provisioning, capacity shortage and ID exhaustion are distinct.
比較要求的 blocks／格式與回報的 NSZE／NCAP／NVMCAP，不要求它們有相同單位或數值。 || Compare requested block counts/format with NSZE/NCAP/NVMCAP using their distinct units.
先檢查 NCAP／NSZE 是否以正確 LBA 大小換算。 || First verify block-size conversion.
''')

q(159,'Create Namespace 容量不足或參數不合法如何回應？ || How are namespace-creation resource and parameter errors reported?', ['nvmcreate','status','error'], '''
失敗原因可以是容量、識別碼數量、格式或資源歸屬。分清它們才知道縮小容量、刪除其他 namespace 或改格式是否有用。 || Distinguish capacity, identifier count, format and resource mapping before choosing a remedy.
容量依所選資源池判斷，不能把其他 Endurance Group 的剩餘空間直接當成可用。 || Capacity is evaluated in the selected resource pool, not unrelated groups.
讀未配置容量、NN／MNAN 的適用定義、格式與 granularity，以及 NVM Set／EG 清單。 || Inspect capacity, applicable namespace limits, formats/granularity and resource lists.
1/15h 是 Namespace Insufficient Capacity，1/16h 是 Namespace Identifier Unavailable，1/0Ah 是 Invalid Format，1/1Bh 是 Thin Provisioning Not Supported。 || Distinct codes are capacity1/15h, identifier1/16h, format1/0Ah and thin provisioning1/1Bh.
以合法基準逐項改參數；容量不足時讀 Error Information.CSINFO 的所需未配置容量 bytes，再決定修正。 || Isolate parameters; for insufficient capacity inspect CSINFO’s required unallocated bytes.
拒絕後不能把任意 DW0 當成新 NSID，只有成功 Create 的 DW0 才具有該意義。 || Only successful Create DW0 contains the created NSID.
沒有遵循 granularity 的偏好倍數可能浪費 allocation capacity，但不應只因未符合偏好就拒絕原本合法的 Create。 || Missing preferred granularity can waste allocation but must not alone reject an otherwise valid create.
比對要求量與真正配置量，區分「格式不允許」與「可用容量不足」。 || Distinguish invalid format from insufficient allocation using consistent quantities.
先查失敗 Status 的完整 SCT／SC，再決定是哪個資源不足。 || First decode SCT/SC before choosing the resource to inspect.
''')

q(160,'Create 後 Allocated Namespace List 如何更新？ || How does creation change the allocated namespace list?', ['nsid'], '''
Allocated 表示 namespace 已存在；Active 表示可經某 controller 存取。Create 只先建立前者。 || Allocated means existence; active means access through a controller. Creation establishes allocation first.
Allocated List 描述適用 inventory；各 controller 的 Active List 可不同。 || Allocated inventory and controller-specific active lists are distinct.
使用 Identify CNS10h 與新 NSID 的 Identify；Active List CNS02h 用於後續 Attach 驗證。 || Query CNS10h and the new namespace; CNS02h verifies later attachment.
Create CQE.DW0 回傳 controller 選出的 NSID，不是 Host 預先保證的連號。 || Create returns a controller-selected ID, not a guaranteed host-predicted sequence.
保存建立前清單，等待成功後重新列舉，確認新 ID 出現並可讀其已配置屬性。 || Snapshot inventory, await success and enumerate again to identify the new object.
新 ID 應在 Allocated List，但不應因 Create 自動出現在任何 controller 的 Active List。 || The new ID is allocated but creation does not automatically attach it.
清單太長時依 NSID 起點繼續讀；只讀第一頁就說新 ID 不存在可能是 Host 錯誤。 || Continue enumeration when lists are longer than one response.
對回 DW0、Allocated List 與 namespace 屬性，避免只用數量增加判斷是哪個物件。 || Correlate returned ID, inventory and attributes rather than count alone.
先確認查的是 CNS10h 而不是 CNS02h。 || First distinguish allocated CNS10h from active CNS02h.
''')

q(161,'Attach／Detach 如何指定 Controller？ || How are controllers selected for attachment changes?', [], '''
Attachment 改變存取關係，不建立或刪除 namespace，也不改它的使用者資料格式。 || Attachment changes access relationships without creating/deleting or reformatting the namespace.
命令 NSID 指目標 namespace，資料中的 Controller List 指要變更的 controllers。 || NSID selects the namespace and the payload Controller List selects controllers.
確認目標已配置、共享能力、controller IDs、Command Set 支援與 MAXCNA／MAXDNA 限制。 || Check allocation, sharing, controller IDs, command-set support and attachment limits.
SEL0=Attach，1=Detach；傳輸4096-byte Controller List。List 的 entries 是 CNTLID，不是 NSID。 || SEL0 attaches and 1 detaches using a 4096-byte list of controller IDs, not namespace IDs.
建立合法清單，提交並等待完成，再到每個目標 controller 查 Active List 與 namespace 的 Controller List。 || Submit a valid list and verify each targeted controller and namespace relationship afterward.
成功後只有所列關係變更，namespace 仍在 Allocated inventory 中。 || Successful attachment change preserves namespace allocation.
Controller List 有非法或 Administrative controller 時回 Controller List Invalid；命令集不支援與未啟用各有不同狀態。 || Invalid/admin-controller list entries and unsupported/disabled command sets have separate statuses.
失敗時 Error Information.CSINFO 指第一個失敗 entry 的 byte offset；遇錯後不再處理後續 entries，不能假設整個清單全部回復。 || CSINFO identifies the first failing entry offset; processing stops there, without a universal all-or-nothing rollback guarantee.
先查 Controller List 的 count、排序與每個 CNTLID 是否來自正確清單。 || First check list count/order and controller identity.
''')

q(162,'Attach／Detach 後 Active List 與 Controller List 如何互相驗證？ || How are active and controller lists cross-checked?', ['idlist'], '''
同一關係可以從 controller 看可用 namespaces，也可以從 namespace 看附加 controllers；雙向核對能找出只更新一邊的錯誤。 || View the relationship from both controller and namespace to detect one-sided updates.
每個 controller 的 Active List 只代表自己，不能當成 subsystem 全部 namespace。 || An active list belongs to one controller, not the full subsystem.
用 CNS02h 與 CNS12h 等適用 Identify 清單，並核對 controller 身分。 || Use applicable active/controller-list queries such as CNS02h/12h with verified identity.
保存 NSID、CNTLID、查詢起點與回傳 entries，避免分頁時漏掉目標。 || Preserve IDs and pagination markers to avoid missing the target.
Attach 成功後兩個方向都應呈現關係；Detach 成功後兩個方向都不再呈現該附加關係。 || Successful attach appears in both views; detach removes it from both.
例如 namespace7 只附加A，Attach到B後，B的Active含7，namespace7的Controller List含A、B。 || If namespace7 attaches toA thenB, B’s active list contains7 and the namespace’s controller list containsA/B.
查詢期間若另有管理操作，清單可能代表不同時間；先停止變更或建立穩定快照，再判矛盾。 || Concurrent management can make snapshots temporally inconsistent; stabilize before diagnosing contradiction.
Allocated List 在單純 Attach／Detach 前後仍應保留該 namespace，與 active 關係分開比較。 || Allocation persists across attachment-only changes.
先排除讀錯 controller 或讀取時間不同。 || First exclude wrong controller and mismatched sample times.
''')

q(163,'重複 Attach、非法 Controller 或未 Attach 就 Detach 如何回應？ || How are attachment relationship errors reported?', ['status'], '''
這些錯誤描述關係與清單，不代表 namespace 資料必定損壞。 || Relationship/list errors do not imply namespace-data damage.
以每個 Controller List entry 當時的附加狀態判斷，可能在前幾項成功後才遇到錯誤。 || Evaluate each list entry against its state; earlier entries may have been processed before failure.
讀目前 Controller List、NMIC 共享設定及目標 controller 能力。 || Inspect current attachment, sharing and target capabilities.
Already Attached=1/18h，Private=1/19h，Not Attached=1/1Ah，Controller List Invalid=1/1Ch。 || Codes distinguish already-attached1/18h, private1/19h, not-attached1/1Ah and invalid-list1/1Ch.
一次測一種關係錯誤，收到完成後讀回全部受測 entries，確認第一個錯誤位置與停止處理行為。 || Isolate the error and reread affected relationships and first-failure position.
合法操作改變指定關係；負向操作回相應狀態，且不處理第一個失敗 entry 之後的 entries。 || Valid operations change relationships; errors stop processing further list entries.
Private namespace 已附加一個 controller，附加第二個會因 Private 限制被拒絕；不是因容量不足。 || A second attachment of an already attached private namespace is rejected for privacy, not capacity.
把 Status、CSINFO offset 與前後清單一起驗證，避免只看整筆命令失敗就認定無任何變更。 || Correlate status/offset and pre/post lists instead of assuming global rollback.
先查 namespace 是否為 private，以及是否早已附加。 || First check sharing mode and existing attachment.
''')

q(164,'Detach 時還有 Outstanding Command，應如何處理？ || What happens to outstanding commands during detach?', ['sqe','nsid'], '''
Detach 會讓該 controller 對目標 NSID 的存取關係失效。Host 先停止新 I/O 並排空較容易管理，但韌體仍須正確處理未完成命令。 || Detach invalidates controller access; quiescing first helps hosts, but outstanding-command behavior remains specified.
只改變指定 controller 與 namespace 的關係；其他仍附加的 controller 不因此自動 Detach。 || Only specified relationships change; other attached controllers remain attached.
保存 outstanding SQID／CID、目標 NSID 與 Attachment 完成時間。 || Preserve outstanding IDs, namespace and detach completion timing.
Base8.1.17 將已提交但未完成及後續提交的目標命令，按 inactive NSID 規則處理；再套用各命令明文例外。 || Base8.1.17 applies inactive-NSID rules to outstanding and later commands, subject to command exceptions.
停止新提交，完成需要的資料同步，等待可排空的工作，再 Detach；若刻意測競爭，完整保存命令與狀態轉移順序。 || Quiesce, synchronize and drain where possible before detach; race tests must retain precise ordering.
Detach 成功後關係消失；先前已完成的命令不重複完成，未完成者按 inactive 規則處理。 || Detach removes the relationship without duplicate completions; outstanding work follows inactive rules.
通用 inactive 規則是 Invalid Field，但命令可另有明確例外；不能把所有命令強制寫成同一碼。 || Generic inactive handling uses Invalid Field, with explicit command exceptions.
確認沒有把已完成的 I/O 誤歸到 Detach 後，也沒有在完成前回收仍可能使用的 buffer。 || Check timing classification and premature buffer reclamation.
先查看命令在 Detach 生效時是否真的仍未完成。 || First establish whether the command was outstanding at detach.
''')

q(165,'Detach 後再送 Namespace Command 應得到什麼？ || How are commands handled after namespace detach?', ['sqe','nsid'], '''
Detach 使 NSID 在該 controller 成為 inactive，不是從 subsystem 刪除。這個區別決定後續命令與查詢怎麼處理。 || Detach makes an ID inactive on that controller without deleting it from the subsystem.
同一 NSID 仍可在另一個已附加 controller 上 active，因此路徑是判斷的一部分。 || The same namespace can remain active through another controller.
查該 controller Active List、Allocated List 與 namespace Controller List。 || Inspect controller-active, allocated and namespace-controller lists.
對使用 NSID 的命令，Figure93 指定 inactive 預設 Invalid Field；Identify 管理查詢等有自身 selector 規則。 || Figure93 uses Invalid Field for inactive IDs by default; Identify and other management selectors have their own rules.
等 Detach 完成，再從已 Detach 的 controller 提交目標命令；對比仍 attached 的 controller，保持其他條件相同。 || After completion, compare the detached and still-attached paths with other conditions fixed.
正常資料存取不能因 namespace 仍存在就繼續視為 active；允許查已配置物件的管理命令則仍可合法工作。 || Allocation does not authorize normal active data access, while allocated-object management queries can remain valid.
不能把所有成功的 Identify 都當成「Detach 沒生效」，也不能把 inactive 與非法 NSID 的 Status 混用。 || Successful allocated-object Identify does not disprove detach; inactive and invalid IDs differ.
用具體 Opcode／CNS 的規則比對，而不是只看 NSID 相同。 || Apply the specific opcode/CNS rule, not NSID alone.
先確認測試送的是 I/O，還是允許查詢 inactive 物件的 Admin 命令。 || First distinguish ordinary I/O from permitted inactive-object queries.
''')

q(166,'刪除不存在或仍 Attached 的 Namespace 如何處理？ || How are nonexistent or attached namespace deletions handled?', ['sqe','nsid','nwp'], '''
需要修正「Attached 就一定禁止刪除」的前提：規範建議先 Detach，但 Delete 也會將 namespace 從所有 controllers 移除。 || Correct the premise that attached namespaces cannot be deleted: prior detach is recommended, and deletion itself removes all attachments.
Delete 移除 subsystem 中的物件，不只是某個 controller 的存取關係。 || Deletion removes the object, not merely one access path.
確認 Allocated List、保護狀態、背景操作與影響範圍，再選單一或全部刪除。 || Check allocation, protection, background work and scope before individual/all deletion.
Management SEL=1 為 Delete，NSID 選既有物件；FFFFFFFFh 表示刪除全部，沒有任何 valid namespace 時此全刪操作仍成功。 || SEL1 deletes; NSID selects an existing namespace andFFFFFFFFh all. Delete-all with no valid namespaces succeeds.
停止相關 I/O，建議先從所有 controllers Detach，再 Delete，最後讀回 Allocated／Active lists。 || Quiesce, preferably detach all accessors, delete and refresh inventory/active lists.
成功後 namespace 不再存在，原附加關係也消失；原 NSID 可能以後重用，不能只用數字當永久身分。 || Success removes object and attachment; the numeric NSID may later be reused.
特定不存在 ID 依 NSID 類型與命令規則拒絕；不能套用全刪空集合成功的例外。保護或正在清除另有相應拒絕條件。 || Specific nonexistent targets follow NSID/command errors, unlike empty delete-all; protection/sanitization impose additional restrictions.
對比刪除前後完整 inventory 與識別資訊，確認沒有僅 Detach 而未 Delete。 || Verify actual inventory removal rather than only detachment.
先查是否用了 FFFFFFFFh，這會改變空集合的完成語意。 || First inspect broadcast NSID before judging empty-inventory behavior.
''')

q(167,'Namespace 變更後哪些事件與 Log 應更新？ || Which events and logs follow namespace changes?', ['aerfull','aec','changedlog','nspelevent'], '''
變更通知讓 Host 更新已快取的配置；事件、變更清單與 Identify 現況各自回答不同問題。 || Notifications invalidate host caches, changed lists identify changes and Identify describes current configuration.
Create／Delete 改 inventory；Attach／Detach 改特定 controller 的 Active List。 || Create/delete change inventory; attach/detach change controller-active membership.
確認 Attached／Allocated notices 的支援與 AEC，以及 AER 是否可用。 || Check attached/allocated notice support, enablement and available requests.
LID04h 列 attached namespace 變更，1Ch 列 allocated 變更；Identify 再查目前狀態，PEL Change Namespace 記錄其定義的管理事件。 || LID04h/1Ch identify attached/allocated changes; Identify and defined PEL management events serve different purposes.
管理命令完成後處理各受影響 controller 的通知，保存變更清單，再重新 Identify。 || Process affected-controller notices, preserve lists and refresh Identify after management completion.
Admin Delete 的提交端不回報該次刪除通知；其他符合條件的 controller 仍回報。不能要求每端通知數必須一樣。 || The Admin Delete recipient omits its own deletion notice while other eligible controllers report; equal counts are not required.
未啟用通知、事件已遮蔽或已被讀取確認，都會影響可見 AER；不是只用「命令成功卻沒AER」判錯。 || Disabled/masked/acknowledged events change observable AERs; command success alone does not prove a missing event defect.
將命令來源、受影響清單與各 controller AEC 放在同一張時間表，避免混淆觀察端。 || Correlate origin, affected lists and per-controller AEC on a timeline.
先查自己是不是處理 Admin Delete 的那個 controller。 || First check whether the observer is the Admin Delete recipient.
''')

q(168,'Changed Namespace List 超過容量如何表示？ || How does changed-namespace overflow work?', ['changedlog','getlog'], '''
變更清單容量有限，溢位標記要求 Host 重新探索全部相關 namespace，而不是只相信不完整清單。 || Overflow requests a full relevant rescan instead of trusting an incomplete list.
LID04h 針對該 controller 的 attached namespace 變更，不是整個 subsystem 的通用變更歷史。 || LID04h concerns attached changes for that controller, not universal subsystem history.
查看 LID04h 的固定1024個NSID entry與讀取／清除規則。 || Apply the fixed1024-entry layout and read/clear rules.
超過1024個變更 namespace 時，第一筆 FFFFFFFFh，其餘清零，表示不能逐筆列全。 || More than1024 changed namespaces yieldsFFFFFFFFh first and zeros in remaining entries.
先判斷第一筆是否為溢位標記；若是，重新列舉並讀取需要的 namespace 屬性，不把 FFFFFFFFh 當實際 namespace。 || Detect the marker, enumerate and refresh properties rather than treating it as an object ID.
完整重掃能恢復現況；不要求 controller 透過多讀幾次04h分頁吐出被省略的全部歷史。 || Full rescan restores current state; repeated04h reads are not historical pagination.
Get Log 傳輸截短與清單自身溢位不同；短 buffer 不應被誤判成沒有其他變更。 || A short transfer is distinct from log overflow.
比較最終 Identify 現況與重掃後 Host 快取，確認溢位後仍能正確同步。 || Validate rescan cache against current Identify state.
先看首項 FFFFFFFFh，再決定逐項刷新還是完整重掃。 || First inspect the overflow marker before choosing incremental/full refresh.
''')

q(169,'Reset 或 Power Cycle 後 Namespace 配置與 Attachment 是否保留？ || Do namespace configuration and attachment survive resets?', ['reset','nsid'], '''
namespace 是持久配置，不隨 queue 重建而重新建立。將這兩層分開，才能避免恢復時誤刪或重複建立物件。 || Namespaces are persistent configuration, separate from recreated queues.
已完成的配置與 attachment 保留；未完成命令則需恢復後查實際狀態。 || Completed configuration persists; interrupted commands require state discovery.
保存 namespace 全球識別、NSID、格式與附加清單，恢復後重新 Identify。 || Preserve global identity, NSID, format and attachment for comparison.
Controller Reset、Subsystem Reset 與 Power Cycle 不等於 Restore Default Namespace Configuration；後者是明確管理操作。 || Resets/power cycle are not the explicit Restore Default Namespace Configuration operation.
恢復 Admin Queue後列舉既有 namespace，確認附加關係，再建 I/O queues，而不是無條件重新Create。 || Recover Admin access, enumerate existing namespaces/attachments, then build queues rather than recreating objects.
原合法配置可恢復存取；Secondary Controller Offline 操作也不應清除 attachment。 || Existing configuration becomes accessible again; secondary-controller Offline does not erase attachment.
若 Reset 前命令結果未知，清單可顯示已成功的變更；不能只因未收到CQE就假設沒有執行。 || Post-reset lists may reflect an operation whose CQE was lost; absence of completion does not prove non-execution.
用持久身分與屬性比對，避免 NSID 重用造成誤配。 || Match persistent identity/properties to avoid NSID-reuse mistakes.
先確認 Host 恢復程序有沒有自己做 Restore 或 Delete。 || First check whether host recovery itself restored defaults or deleted objects.
''')

q(170,'Private 與 Shared Namespace 有何差別？ || How do private and shared namespaces differ?', ['idns'], '''
Private 限制同時附加一個 controller；Shared 可允許多 controller 附加。這是存取拓樸，不是資料加密或讀寫權限名稱。 || Private limits attachment to one controller; shared allows multiple. These describe access topology, not encryption or access permissions.
多條路徑可指向同一份 namespace 資料，不能把每條路徑當成獨立副本。 || Multiple paths can address one data object, not separate copies.
看 Identify Namespace.NMIC 共享能力與實際 Controller List。 || Inspect NMIC and actual attachments.
Create 時指定 NMIC，Attachment 用 Controller List 操作關係；Shared 仍受 MAXCNA／MAXDNA 等限制。 || NMIC is selected at creation; attachment changes relationships within supported limits.
先配置共享屬性，再附加需要的 controllers，逐端查 Active List。 || Configure sharing, attach controllers and verify each active list.
Shared 可由多端存取；Private 從A Detach後可再Attach到B，但不能同時保有兩端關係。 || Shared permits multiple accessors; private can move fromA toB through detachment but not attach to both simultaneously.
Private 已附加另一controller時，新增附加回 Namespace Is Private。 || Additional attachment of an already attached private namespace uses Namespace Is Private.
檢查身分、資料與附加關係，避免把多路徑誤算成多份容量。 || Compare identity/data/attachments rather than counting paths as additional capacity.
先查 NMIC，而不是用「有兩個controller」推論所有namespace都Shared。 || First inspect NMIC instead of assuming all namespaces are shared in a multi-controller system.
''')

q(171,'三種 Write Protection 模式與進入條件有何不同？ || How do write-protection modes and entry controls differ?', ['nwp'], '''
保護模式決定能否解除以及何時解除；選 Permanent 前必須理解它不是可隨時切回的普通開關。 || Protection modes differ in reversibility; permanent protection is not an ordinary reversible toggle.
WPS 屬於 namespace，所有附加controllers共同執行。 || WPS is namespace state enforced across attached controllers.
NWPC 宣告支援模式；RPMB 的 WPC 控制進入 Until Power Cycle 或 Permanent 是否被允許；FID84h 回報實際 WPS。 || NWPC advertises modes, RPMB WPC gates entry and FID84h reports actual WPS.
WPS0=未保護，1=Write Protect，2=Until Power Cycle，3=Permanent。一般Write Protect可用合法Set解除，後兩者不能靠Set任意改變。 || WPS0/1/2/3 select unprotected/ordinary/until-cycle/permanent; only ordinary protection is normally reversible by Set.
查能力與進入許可，設定WPS，等待完成，再Get確認。轉入受保護狀態前，controller須提交該namespace的volatile cache data／metadata到非揮發媒體。 || Check support/entry permission, Set and Get; entering protection commits associated volatile cached data/metadata.
WPS與實際禁止改寫的行為一致；Read仍可依正常條件處理。 || State and write prohibition agree while reads remain subject to normal conditions.
進入未允許狀態或改變Until Power Cycle／Permanent回 Feature Not Changeable；multi-domain不得使用Until Power Cycle。 || Disallowed entry or changing locked modes uses Feature Not Changeable; until-cycle mode is prohibited in multi-domain systems.
WPC只是進入許可，不是WPS；把控制位清零不會自動解除既有保護。 || WPC is entry permission, not state; clearing it does not remove existing protection.
先區分 NWPC、WPC 與 WPS，不要把三者當同一個位元。 || First distinguish capability, permission and state.
''')

q(172,'Write Protection 在 Reset 與 Power Cycle 後如何保留？ || How does write protection persist across reset and power?', ['nwp','feature'], '''
FID84h不可保存，不代表保護不持續。其狀態有明確持久性，不能套用一般Saved Feature的直覺。 || FID84h is non-saveable but has explicit persistent state; generic saved-feature assumptions do not apply.
保留規則跟隨namespace，不因controller更換而解除。 || Persistence follows the namespace, not one access controller.
Get FID84h讀Current WPS，並記錄實際Reset來源及是否有power cycle。 || Read current WPS and record the actual reset/power event.
WPS1／3跨Reset與power cycle保留；WPS2跨非power-cycle的CLR保留，但power cycle回WPS0。 || WPS1/3 persist across reset/power; WPS2 survives non-power CLR and clears to 0 on power cycle.
建立基準狀態，執行指定事件，恢復後Get並驗證寫入限制；不要把CC.EN清零當成拔電。 || Set baseline, perform the selected event and verify state/behavior; clearingCC.EN is not power cycling.
普通Controller Reset後WPS2仍受保護，是正確結果；真正power cycle後則解除。 || WPS2 remaining protected after controller reset is correct; actual power cycling releases it.
本Feature沒有Default值，Get SEL=Default回Invalid Field；不能要求一個虛構Default來解釋恢復。 || No default value exists; Get Default returns Invalid Field, not a fabricated restoration value.
同時比對讀回WPS與Write／Format限制，不只確認Set曾成功。 || Compare WPS and actual write/format restrictions.
先查測試使用的Reset是否真的包含電源循環。 || First establish whether a real power cycle occurred.
''')

q(173,'Write Protection 如何影響 Format、Sanitize 與 Namespace Management？ || How does protection affect format, sanitize and namespace management?', ['nwp','format','sanitizecmd'], '''
保護不只阻止Write；任何會修改受保護namespace的操作，都要依命令互動規則檢查，包含未直接指定它的廣範圍操作。 || Protection covers operations modifying the namespace, including broad commands not naming it directly.
共享namespace在所有附加controller受保護；Format或Subsystem Sanitize的scope若涵蓋它，也不能繞過。 || All attached paths enforce protection, including covering Format/subsystem-sanitize scopes.
查WPS、命令scope與Figure737允許清單；不能只檢查Opcode名稱。 || Check WPS, scope and Figure737 permitted actions.
Read／Compare／Verify等通常允許；Flush成功且無效果，因進入保護時已提交cache。Namespace Attachment允許，但Delete、Format或Sanitize修改受保護物件會被限制。 || Reads/Compare/Verify generally remain allowed; Flush succeeds without effect after cache commitment. Attachment is allowed, while modifying deletion/format/sanitize is restricted.
先算完整影響範圍，再檢查所有受影響namespace的WPS，最後套用命令的附加條件。 || Compute full impact before checking each namespace’s protection and command exceptions.
允許查詢可正常完成；禁止修改應被拒絕且資料維持受保護，不因換controller就成功。 || Allowed queries succeed while prohibited changes are rejected across paths.
符合禁止修改條件時回 Namespace is Write Protected；不能因Sanitize通常忽略SMART唯讀警告，就忽略Host設定的namespace保護。 || Prohibited modifications use Namespace is Write Protected; ignoring SMART critical warnings for sanitize does not bypass namespace protection.
以同一受保護資料測直接Write與跨namespace範圍操作，確認scope判斷一致。 || Cross-check direct writes and broader operations against the same protection scope.
先區分SMART的媒體唯讀警告與FID84h的namespace保護狀態。 || First distinguish SMART read-only warning from configured namespace protection.
''')
