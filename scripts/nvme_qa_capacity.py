"""Q256–267: resource hierarchy, health scope and capacity accounting."""
from scripts.nvme_qa_extension import question
from scripts.nvme_qa_model import COMMON, REFS, pair
REFS['capacitymodel']='B|3.2.2–3.2.3, 3.8|106-110,151-155|67–69, 86–89'
REFS['capacitycmd']='B|5.2.3|217-221|162–166'
REFS['capacityop']='B|8.1.4|620-623|'
REFS['eghealth']='B|5.2.13.1.10|263-265|224–225'
REFS['egevents']='B|3.2.3.1, 5.2.13.1.15, 5.2.30.1.17|110,296,504|261, 493'
REFS['mediaunit']='B|5.2.13.1.16|296-298|262–264'
COMMON['capacity_op']={**COMMON['command'],
 9:pair("""容量配置本身不保證一個通用完成 AER；若刪除 Set／Group 連帶刪除 namespaces，須依明定的 namespace 清單與通知規則更新受影響 controller。健康事件則另由 FID18h 與 AEC 控制。 || Capacity completion has no generic AER; cascaded namespace deletion follows explicit list/notice rules. Health events use separate FID18h/AEC settings."""),
 10:pair("""配置完成後核對 Group／Set／Namespace 清單與對應層級的容量欄位。Media Unit Status 受支援時，也應反映歸屬。容量不足的 Create 有明定 Error Information 補充資料要求，不能只保留 CQE。 || Verify lists, layer-specific capacity and supported media ownership. Insufficient-capacity creation has explicit error-log detail requirements beyond the CQE."""),
 11:pair("""Capacity Management 本身沒有一個通用的專用 PEL 完成事件。若操作另外符合支援的 namespace、硬體警告等事件條件，依那些條件記錄，不按建立／刪除每個物件自行編造事件。 || There is no universal dedicated Capacity Management PEL completion event; separately qualifying namespace or hardware events use their own conditions."""),
 12:pair("""已完成的 Group、Set 與 namespace 配置不是普通 CLR 的暫存 queue，不能因 controller 重設就當作刪除。未完成管理操作則重查實際清單與容量，不能假設自動 rollback。 || Completed storage configuration is not volatile queue state and is not deleted by ordinary CLR. Requery interrupted operations rather than assume rollback."""),
 13:pair("""Subsystem Reset 與 Restore Default Capacity Configuration 是不同操作。重設後保留已完成的儲存配置並重新探索；只有另行執行配置操作，才依該操作的要求變更物件。 || Subsystem reset is distinct from restoring default capacity configuration; rediscover retained storage configuration unless a separate management action changed it."""),
 14:pair("""已完成的容量配置跨 Power Cycle 保留。若失電打斷配置，恢復後用可讀的清單、容量及事件判斷，不能將未收到 CQE 直接視為未修改。 || Completed configuration persists across power cycles; requery interrupted operations because missing CQE does not prove no effect."""),
 15:pair("""刪除 Endurance Group 會連帶刪除所含 NVM Sets 與 namespaces；刪 Set 也會刪其 namespaces，影響所有附加路徑。單一 namespace 的容量配置則應在它所在的資源層級核算。 || Deleting a group cascades through sets/namespaces; deleting a set removes its namespaces across all paths. Account namespace allocation in its containing resource layer.""")}

def q(n,t,r,b,o=None): question(n,t,'capacity_op',r+['capacitymodel','capacitycmd','capacityop','eghealth','egevents','idctrl','idlist','nvmcreate'],b,o)

q(256,"NVM Set、Endurance Group 與 Namespace 是什麼關係？ || How are NVM sets, endurance groups and namespaces related?", [], '''
這些物件分別組織容量、耐用度與邏輯存取，不能把它們當作同一個 ID 的不同名字。 || They organize capacity, endurance and logical access rather than rename one object.
支援 NVM Set 時，formatted namespace 完整位於一個 Set；Set 完整位於一個 Endurance Group；Group 完整位於一個 domain。 || With set support, a formatted namespace resides in one set, each set in one group and each group in one domain.
查 CTRATT 的 Set／Group 支援與各 List，再讀 namespace 的 NVMSETID、ENDGID。 || Read support and lists, then namespace membership identifiers.
NVM Set List 回容量與所屬 Group；Endurance Group Log 回其健康與容量；Identify Namespace 回邏輯 block 與歸屬。 || Set lists, group logs and namespace Identify provide distinct capacity, health and membership views.
先畫支援的層級，再填實際 ID。未支援 NVM Sets 時，不要畫出虛構的 Set0 當必要中間層。 || Draw supported layers and actual IDs; absence of set support does not create a fictional Set0 layer.
例如 EG1 有 Set2、Set3，各有 namespaces；同 Group 的 Sets 由該 Group 共同管理耐用度。 || Example EG1 contains Set2/3 and their namespaces, with endurance managed across those sets.
NVM Sets 支援要求同時支援 Endurance Groups；反方向不成立，Group 可以存在而沒有 Set 功能。 || Set support requires groups; group support does not require sets.
用 namespace、Set、Group 三種查詢確認相同歸屬，避免只看一個名稱相近的 ID。 || Cross-check membership through all supported layers.
先檢查裝置實際支援哪些層級，再判斷欄位的零值。 || First establish supported layers before interpreting zero IDs.
''')
q(257,"如何從 Identify 探索 NVM Set 與 Endurance Group？ || How are sets and groups discovered through Identify?", [], '''
支援位元回答有沒有能力，清單回答目前有哪些物件，最大 ID 則不是目前物件數。 || Capability, inventory and maximum identifier answer different questions.
探索以所查 controller 能取得的 subsystem／domain 資訊為準。 || Discovery reflects information accessible through the queried controller.
查 CTRATT、NSETIDMAX、ENDGIDMAX；再取 NVM Set List 與 Endurance Group List。 || Read support/maxima and the respective inventories.
Set 屬性有總容量、未配置容量及 ENDGID；Group 的詳細容量和健康需再讀 LID09h。 || Set attributes include capacities/membership; detailed group data comes from LID09h.
先讀能力，再分段列舉有效 ID，最後逐個讀屬性與健康；不要從 1 到最大 ID 全部假定存在。 || Enumerate actual IDs before reading details; do not assume every possible ID exists.
取得目前物件及歸屬，能分清沒有配置與不支援能力。 || Discover inventory and distinguish absent allocation from unsupported capability.
不支援時輸出的相應 ID 欄位須按規範清零；這不代表真的存在可供指定的有效 ID0。 || Required zero output for unsupported functionality does not create valid entity0.
核對宣告、清單、最大 ID 與 namespace 歸屬的一致性。 || Reconcile advertisement, inventories, maxima and membership.
先檢查是否把 NSETIDMAX／ENDGIDMAX 誤當成現有總數。 || First check confusion between maximum ID and current count.
''')
q(258,"Namespace 如何建立於指定 Set 或 Group？ || How is a namespace created in a selected set or group?", [], '''
選擇歸屬可讓新 namespace 使用指定資源池；邏輯容量還需換算成該格式的 blocks。 || Select a resource pool while encoding logical capacity in blocks of the chosen format.
Create 的歸屬欄位決定新物件所在位置，不是把既有 namespace 搬過去。 || Creation selects placement for a new object rather than moving an existing namespace.
查支援的 Lists、可用容量與 LBA Format，再確認 NVMSETID／ENDGID 的組合。 || Check inventory, capacity and LBA format before selecting membership.
NVM Namespace Create 資料包含 NSZE、NCAP、FLBAS、DPS 與歸屬 ID；NCAP 不得大於 NSZE。 || Create fields combine logical size/capacity, format/protection and membership.
兩個 ID 都為 0 可由 controller 選擇；指定 Group 而 Set=0 時在該 Group 中選；指定 Set 必須搭配正確的非零 Group。 || Both zero delegate selection; group-only selects within it; a specified set requires its correct nonzero group.
成功 CQE.DW0 回新 NSID，再讀 allocated Identify 確認實際歸屬；Create 不會自動完成 Attachment。 || Success returns NSID; verify allocated Identify and attach separately.
指定不存在或不匹配的組合不能當成自動選擇；須按 Create 的非法欄位／資源錯誤處理。 || Nonexistent/mismatched explicit membership is not automatic selection.
比對回傳 NVMSETID、ENDGID 與容量扣除的層級，確認不是只建立成功卻查錯物件。 || Verify returned membership and the correct allocation layer.
先檢查所選 Set 真的屬於指定 Group，而不是只確認兩個 ID 各自存在。 || First verify membership, not merely existence of both IDs.
''')
q(259,"指定不存在的 NVM Set 或 Endurance Group 時會怎樣？ || What happens when a set or group identifier does not exist?", [], '''
ID0 與不存在的非零 ID 可能有不同意義，而且同一個零值在不同命令也不同。 || Zero and nonexistent nonzero identifiers differ, with zero semantics varying by command.
先限定操作是 Namespace Create、Capacity Create/Delete、Get Log 還是 Feature。 || Identify whether the operation is namespace/capacity management, logging or a feature.
從相應 List 驗證目前有效 ID，再讀該命令欄位的特殊值定義。 || Check current inventory and command-specific special values.
例如 Capacity Create Group 的 ELID=0 可自動選 domain；Delete Group 的 ELID=0 則非法。 || For example, zero ELID auto-selects a domain for group creation but is invalid for group deletion.
先建立合法對照案例，再只換成不存在的非零 ID，避免混入格式、scope 等其他錯誤。 || Start from a valid request and isolate one nonexistent identifier.
合法自動選擇應成功並回實際 ID；非法明確 ID 不應悄悄改成別的物件。 || Valid automatic selection returns the selected ID; invalid explicit IDs must not silently target another object.
Capacity Management 非零 ELID 不對應既有物件、Delete 指定0或不存在物件，須 Invalid Field；FID18h 指定不存在 Group 也須 Invalid Field。 || Invalid capacity entity selectors and nonexistent FID18h groups require Invalid Field.
沒有 Group 支援時，Base 對命令中 ENDGID 有忽略規則；必須先分清未支援功能與已支援但 ID 非法。 || Base has ENDGID-ignore rules when groups are unsupported; distinguish absence of capability from invalid IDs under support.
先查該命令對 0 的明確定義，不能套一個全域「0 永遠非法」規則。 || First read zero semantics for that specific command.
''')
q(260,"Endurance Group Information Log 提供哪些健康與容量資訊？ || What does the Endurance Group Information Log report?", [], '''
這份 Log 將健康與工作量縮小到一個 Group，適合比較不同資源池，而不只看整顆 SSD 的 SMART。 || This log provides group-scoped health/workload rather than only aggregate SMART.
LID09h 以 LSI.ENDGID 選目標，資料涵蓋該 Group 的生命週期。 || LID09h selects ENDGID and describes the group’s lifetime.
確認 Group 支援及存在，再讀 512-byte Log。 || Establish support and existence before reading the 512-byte structure.
EGCW、AVSP、AVSPT、PUSED 描述健康；DUR、DUW、MUW 描述讀寫量；HRC、HWC、MDIE、NEILE 描述計數；TEGCAP、UEGCAP 為容量 bytes。 || Health, host/media data volume, command/error counts and byte capacities occupy distinct field groups.
先讀健康狀態，再用前後快照比較工作量。此處 DUR／DUW／MUW 用 10^9 bytes 向上取整，不能套 SMART 的 512000-byte 單位。 || Inspect health and difference snapshots; these data counters use rounded billions of bytes, not SMART’s 512000-byte units.
MUW 包含內部資料搬移，DUW 不含，因此可用來分析額外媒體寫入；仍要考慮取整與0代表未回報。 || MUW includes internal writes unlike DUW; account for quantization and unreported zero values.
沒有回報值不等於真實消耗為0；不能對分母為0或未回報的 DUW 計算有效 write amplification。 || Unreported zero is not zero consumption and cannot support a meaningful amplification ratio.
Group Log 與 namespace membership、SMART 的整體警告需一致，但不能要求各欄逐 byte 相同。 || Correlate group membership and aggregate warning semantics, not bytewise equality with SMART.
先檢查是不是把兩種 Log 名稱相同的 Data Units 用錯單位。 || First check same-name counters with different units.
''')
q(261,"Endurance Group 的警告、Spare 與壽命事件如何更新？ || How are group health warnings and events updated?", [], '''
Group 健康值、待確認事件清單與 Host AER 通知各負責不同階段，要分開設定和確認。 || Live health, pending-group entries and host notices form separate stages.
FID18h 逐 Group 設定，AEC 則控制 aggregate log change 通知。 || FID18h is per-group, while AEC enables aggregate-log notices.
查 EGCW、AVSP／AVSPT／PUSED、FID18h.EGCW 與 AEC 的相關 notice bit。 || Inspect live health, per-group event mask and AEC notice enablement.
EGCW bit0 低 spare、bit2 可靠性降低、bit3 Group 唯讀；namespace Write Protection 不得造成 EGRO。bit1 保留，不能照抄 SMART 溫度 bit。 || Group warning bits 0/2/3 indicate spare/reliability/read-only; namespace write protection must not set EGRO. Bit 1 is reserved, unlike SMART temperature.
啟用 Group 事件後，有待處理條件就列入 LID0Fh；Host 讀0Fh找 ID，再讀各 Group 的09h。09h 成功 RAE=0 才清該 Group 事件並移除其 entry。 || Pending groups enter0Fh; read it, then each09h. Successful09h RAE0 acknowledges/removes that group’s pending entry.
讀0Fh確認通知不等於逐 Group 事件全部清除；事件目前已消退時，09h 的 EGCW 也可能已為0。 || Aggregate acknowledgment is not acknowledgment of every group; current warning may already have cleared.
FID18h 設保留警告 bit 或不存在 Group 須 Invalid Field。 || Reserved warning bits or nonexistent groups in FID18h require Invalid Field.
只有全部 Groups 都設相應 warning bit，才依規範要求在整體 SMART 設對應 bit；單一 Group 警告不可直接當成全部媒體唯讀。 || The specified aggregate SMART rule applies when all groups assert the bit, not merely one group.
先檢查是否只確認0Fh就以為09h的 Group 事件也已清除。 || First check confusion between aggregate and per-group acknowledgment.
''',{9:'Group 事件新增至 aggregate log 後，依 AEC 與 AER 條件通知；FID18h 管哪種 Group 警告加入清單，AEC 管清單變更是否通知 Host。 || FID18h selects group warnings for the aggregate; AEC and AER conditions govern host notice of additions.',10:'LID0Fh 回待確認的 Group IDs；LID09h 回指定 Group 的目前健康。成功讀09h且 RAE=0，才清除該 Group 的待處理事件。 || LID0Fh lists pending group IDs;09h reports current group health and successful RAE0 reads acknowledge that group.'})
q(262,"如何確認總容量與未配置容量？ || How are total and unallocated capacities determined?", [], '''
未配置容量必須先問「還沒分給哪一層」，否則容易把已分給 Group 但尚未建立 namespace 的空間算錯。 || Unallocated means unallocated to a particular next layer, not universally free for any operation.
可能分別是 subsystem、domain、Group 或 Set 的容量池。 || Capacity pools exist at subsystem, domain, group or set scope.
查 TNVMCAP／UNVMCAP、Domain Attributes、TEGCAP／UEGCAP，以及 Set 的 Total／Unallocated Capacity。 || Read controller/domain capacities, group capacities and set attributes.
這些實體容量欄位使用 bytes；namespace NSZE／NCAP 使用目前 LBA 格式的 blocks，不能直接把原始數字相減。 || Physical-capacity fields use bytes; namespace sizes use formatted blocks.
依將執行的管理操作選 Figure89 指定的容量來源，再計入配置粒度與 Capacity Adjustment Factor。 || Select the operation’s capacity source under Figure89, including granularity and adjustment factor.
例如 Create Set 從既有 Group 的 UEGCAP 分配，成功不要求 subsystem UNVMCAP 再減一次。 || Creating a set allocates from UEGCAP without requiring another decrease in subsystem UNVMCAP.
零值有時表示未回報，需讀該欄定義與支援條件；不能一律當作沒有容量。 || Zero may mean unreported under field-specific rules rather than no capacity.
以同一層級的前後數值驗證，避免把不同配置階段相加造成雙重計算。 || Compare within one layer to avoid double counting.
先明確說出這次要建立的是 Group、Set 還是 namespace。 || First identify which entity is being created.
''')
q(263,"Namespace 建立與刪除如何改變未配置容量？ || How do namespace creation and deletion affect free capacity?", [], '''
Namespace 使用所屬容量池，並非每次都直接改變 Identify Controller.UNVMCAP。 || Namespace allocation consumes its containing pool, not always controller UNVMCAP.
有 Set 用 Set 容量；無 Set 但有 Group 用 Group；更簡單配置則使用對應 domain／subsystem 容量。 || Use the supported containing layer: set, group or domain/subsystem.
保存 namespace 所屬 ID、LBA 格式、實際 NVMCAP 與該池前後容量。 || Preserve membership, format, actual NVMCAP and pool snapshots.
NSZE 描述邏輯大小，NCAP 描述可配置邏輯 blocks；實體消耗還有配置粒度，不必精確等於 NSZE×LBA bytes。 || Logical size/capacity and physical consumption differ because of allocation granularity.
成功 Create 後查新 namespace 與池餘額；Delete 完成後查清單移除與可重新使用的容量。 || After creation/deletion verify inventory and the corresponding pool.
容量應依該層級與規則釋出／扣除；Detach 只移除路徑，不能當成 Delete 來預期容量歸還。 || Capacity follows allocation rules; Detach alone does not return namespace capacity.
容量不足與 NSID 數量耗盡是不同錯誤，不能只看到 Create 失敗就判定 bytes 不足。 || Capacity exhaustion differs from identifier/count exhaustion.
把有效資料內容、namespace 存在與容量帳目分開驗證，刪 namespace 也不等於已做資料抹除。 || Verify allocation separately from data sanitization; deletion is not proof of purge.
先檢查是否看錯層級的 Unallocated 欄位，或把 Detach 當成容量釋放。 || First check the accounting layer and whether the operation was only Detach.
''')
q(264,"Capacity Management 如何配置或釋放 Group 與 Set？ || How does Capacity Management allocate and release groups and sets?", [], '''
Fixed 模式選既有配置，Variable 模式指定新物件容量，兩者不是同一組操作流程。 || Fixed selects supported layouts; Variable creates entities by requested capacity.
Group／Set 變更可連帶影響包含的 namespaces 與所有存取路徑。 || Changes can cascade to contained namespaces and all paths.
查 CTRATT 的 Fixed／Variable 與 Delete 支援；Fixed 再讀 Supported Capacity Configuration List。 || Check management/deletion support and supported fixed configurations.
OPER0 選配置，1／2 建立／刪 Group，3／4 建立／刪 Set，5 恢復預設。ELID 意義隨 OPER 變，CAPU:CAPL 為建立容量 bytes。 || OPER selects layout/create/delete/restore; ELID meaning varies and CAPU:CAPL encodes create bytes.
Variable 通常先 Group 再 Set 再 namespace；Fixed 改到另一配置前須依條件清除原配置，不能任意覆蓋正在使用的配置。 || Variable allocation proceeds group→set→namespace; fixed reconfiguration follows clearing/selection prerequisites.
Create 成功 CQE.DW0.CELID 回建立的 ID；其他操作不能把同一欄當作永遠有效的物件 ID。 || Creation returns CELID; other operations do not universally return a valid created ID.
刪 Group／Set 會連帶刪子物件；恢復預設前仍有 Group／Set 時須 Command Sequence Error。 || Deletion cascades; default restoration with remaining groups/sets requires Command Sequence Error.
完成後重新讀清單、歸屬與容量；操作過程中的中間觀察可能 indeterminate，不宜拿單一中間快照作最終結果。 || Requery final lists/ownership/capacity; intermediate accesses may be indeterminate.
先確認 OPER 選的是預期模式與動作，尤其 ELID=0 在各動作的不同意義。 || First check operation and its zero-identifier semantics.
''')
q(265,"要求容量或物件數超過可用資源時應回什麼？ || What happens when capacity or identifiers are exhausted?", [], '''
容量 bytes 不夠與沒有可用 ID 是不同限制，題目應先固定是哪一種。 || Capacity exhaustion and identifier exhaustion are distinct limits.
Create Group 核對 domain／subsystem 可配置量與最大 Group 大小；Create Set 核對 Group 的 UEGCAP。 || Group creation checks relevant pool/max size; set creation checks UEGCAP.
查 MEGCAP、UNVMCAP、domain 容量、UEGCAP 與目前 ID 清單。 || Inspect capacity limits and inventory.
容量請求使用 CAPU:CAPL bytes，並考慮調整因子與實作配置粒度後所需資源。 || Interpret requested bytes with adjustment and allocation granularity.
先做只超容量但 ID 尚可用的案例，再做容量足夠但 ID 耗盡的案例，以隔離不同限制。 || Isolate capacity and identifier exhaustion in separate scenarios.
資源足夠時建立成功且回 CELID；不足時不應假裝建立了不存在的物件。 || Adequate resources create an entity and return CELID; failure must not fabricate one.
容量不足回命令特定 Insufficient Capacity（1/26h）；無可用 ID 回 Identifier Unavailable（1/2Dh）。 || Capacity shortage returns 1/26h; identifier exhaustion returns 1/2Dh.
正文要求 Error.CSINFO 回可建立的最大容量；Figure165 卻寫所需容量，兩處不一致。教材保留這項來源差異，不以其中一個數字直接替韌體判定合規。 || Prose specifies largest creatable capacity in CSINFO, while Figure165 describes required capacity. Preserve this conflict rather than using one interpretation as an unconditional conformance oracle.
先確認失敗的限制種類；涉及 CSINFO 語意時再核對這項規格內部差異。 || First identify the exhausted resource, then the CSINFO source ambiguity.
''',{10:'容量不足的 Create Group／Set 在支援 Error Log 時，必須記錄明定的 CSINFO 補充容量資訊；其數字語意在正文與 Figure165 有差異，應一併記錄來源。 || Insufficient-capacity creation requires the stated CSINFO detail when Error Log is supported; preserve the prose/Figure165 semantic conflict.'})
q(266,"容量配置完成後，哪些 Identify 與 Log 應更新？ || Which views change after capacity reconfiguration?", [], '''
單一成功 CQE 不足以驗證配置；所有描述同一物件的查詢都應形成一致結果。 || Validate coherent views, not just successful CQE.
依變更層級檢查 Group、Set、namespace、domain 及 Media Unit 歸屬。 || Inspect affected group/set/namespace/domain/media relationships.
保存前後 Identify Lists、容量欄位、Group Log 與受支援的 Media Unit Status。 || Preserve inventory, capacity and ownership snapshots.
Create Group 更新 Group List 與上層容量；Create Set 更新 Set List 與 UEGCAP，卻不改 UNVMCAP；刪除則依序移除子物件與回收該層容量。 || Group creation changes parent capacity; set creation changes set inventory/UEGCAP but not UNVMCAP; deletion follows its cascade.
先等管理命令完成，再重讀受影響物件；若仍有其他 Host 同時改配置，需記錄時序才能比較。 || Read after completion and account for concurrent management.
例如刪 Set 後，其 namespaces 從 allocated list 移除，Media Unit 的 NVMSETID 清零，Group 可用容量增加。 || Deleting a set removes its namespaces, clears applicable media ownership and returns group capacity.
操作中間的清單先後更新有明定順序，不能一律要求每個 byte 對所有讀者瞬間原子變更。 || Ordered intermediate updates are not universally atomic byte-for-byte to all readers.
用完整變更鏈確認：物件消失、子物件消失、容量回到正確父層、通知讓其他讀者重查。 || Verify the full chain of inventory, child removal, accounting and rediscovery notices.
先檢查觀察是在完成前還是完成後，以及是否有人同時進行第二次配置。 || First check completion and concurrent-operation timing.
''')
q(267,"Reset 與 Power Cycle 後 Group、Set 與容量配置如何保留？ || How does storage configuration persist across reset and power cycle?", [], '''
容量配置代表儲存組織，與需要重建的 I/O queues 不同，重設不能被當成清空配置命令。 || Storage organization is distinct from transient I/O queues; reset is not configuration deletion.
已完成的 Group、Set、namespace 歸屬與容量帳目是比對對象。 || Compare completed entity membership and capacity accounting.
保存配置清單、識別資訊、容量及是否有待完成管理操作。 || Snapshot configuration, identity, capacities and outstanding management.
Restore Default Capacity Configuration 是另外的 OPER5，並有清空現有物件的先決條件；普通 Reset 不等於這項命令。 || OPER5 default restoration is separate and has inventory prerequisites.
恢復命令通道後重新探索，再確認物件與歸屬；對失電時未完成的操作，不假定成功、失敗或 rollback。 || Rediscover after channel recovery; interrupted operations require outcome discovery rather than assumed rollback.
已完成配置應能對回原物件，容量差異則需由其他合法管理變更或可說明的狀態解釋。 || Completed configuration remains identifiable; explain differences through actual management/state changes.
未收到 CQE 只表示 Host 不知道結果，不表示原配置必定完整未改。 || Missing completion establishes uncertainty, not an unchanged configuration.
先區分「重設造成暫時不可查」與「配置已真正消失」，前者不能直接判成持久性失敗。 || Distinguish temporary query unavailability from missing persistent configuration.
先查這段期間是否還執行了 Restore、Delete 或其他容量管理操作。 || First check for separate restore/delete/reconfiguration activity.
''')
