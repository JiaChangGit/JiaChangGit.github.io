"""Q246–255: controller topology, namespace paths and flexible resources."""
from scripts.nvme_qa_extension import question
from scripts.nvme_qa_model import COMMON, REFS, pair
REFS['multipath']='B|2.4.1–2.4.2 (PCIe topology)|60-63|19–22'
REFS['virtualcmd']='B|5.3.6|559-561|587–590'
REFS['virtualid']='B|5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)|428-430|360–362'
REFS['ana']='B|2.4.2, 8.1.1 (PCIe namespace access)|63,604-610|675–678'
REFS['analog']='B|5.2.13.1.13|267-270|229–231'
COMMON['virtual_op']={**COMMON['command'],
 9:pair("""資源配置與 Online／Offline 不定義統一成功 AER。Namespace 屬性或 ANA 狀態若另外符合變更條件，才依各自通知設定與規則回報。 || Resource allocation and Online/Offline do not define a universal success AER; qualifying namespace or ANA changes follow their own rules."""),
 10:pair("""用 Primary Controller Capabilities、Secondary Controller List 及目前 queue／interrupt 能力確認配置；namespace 路徑則讀 Active List、Controller List 與適用 ANA Log。不要把資源數量變更當成 Error Log 紀錄。 || Verify resource state through capability/list structures and path state through namespace/ANA data; allocation changes are not themselves error entries."""),
 11:pair("""Virtualization Management 不是專用 PEL 事件。若流程包含已完成的 Reset 或符合條件的 namespace 管理，則依那些事件記錄；不能要求每次 Assign 都新增 Reset event。 || Virtualization Management has no dedicated PEL event; actual resets or qualifying namespace operations follow their events, not every Assign."""),
 12:pair("""Primary 被 Disable、CLR 或 Shutdown 時，其 secondary 必須轉 Offline；Online 轉 Offline 會移除 Flexible Resources。Primary 的 Flexible Allocation 設定可持續，但新配置需由非 CC.EN Controller Reset 的 CLR 生效。 || Primary disable/CLR/shutdown takes secondaries Offline, removing their flexible resources on the transition. Primary allocation is persistent but a new value takes effect after a CLR other than CC.EN Controller Reset."""),
 13:pair("""Subsystem Reset 影響範圍內的 primary／secondary 操作環境須重建。不要把持續的 primary allocation 設定，誤當成 secondary 仍 Online 或原 queues 仍存在。 || Rebuild affected primary/secondary operation after subsystem reset; persistent primary allocation does not preserve Online state or queues."""),
 14:pair("""Primary Flexible Allocation 跨 Power Cycle 保留；secondary 的 Online 狀態與資源需重新查詢及配置。Namespace 與 attachment 的持續性是另一項規則，不因 secondary Offline 就刪除。 || Primary flexible allocation persists across power cycles; rediscover/reconfigure secondary resources and state. Offline does not delete persistent namespace/attachment configuration."""),
 15:pair("""Primary 管理自己的 secondary 群組及 Flexible Resource pool，同一份資源不能同時分給兩個 controller。Shared namespace 則讓多條路徑存取同一份資料，Host 仍需協調同時寫入。 || A primary manages its own secondaries/pool; one resource cannot belong to two controllers simultaneously. Shared namespaces expose the same data and require host write coordination.""")}

def q(n,t,r,b,o=None): question(n,t,'virtual_op',r+['multipath','virtual','virtualcmd','virtualid','nsattach','idlist','reset'],b,o)

q(246,"Subsystem、Primary 與 Secondary Controller 是什麼關係？ || How are subsystems, primary and secondary controllers related?", [], '''
Controller 是命令入口，namespace 是儲存物件；虛擬化把部分 queue 與 interrupt 資源交由 primary 管理分配。 || Controllers are command endpoints, namespaces storage objects; virtualization lets a primary allocate queue/interrupt resources.
一個 subsystem 可有多個 primary，各有 secondary 群組；secondary 與其 primary 必須在同一 domain。 || A subsystem can contain multiple primary groups, with each secondary in its primary’s domain.
查 OACS.VMS、Primary Controller Capabilities 與 Secondary Controller List，不憑 PCI function 編號猜 parent。 || Discover VMS and the primary/secondary structures rather than inferring parentage from function numbers.
VQ 管一組 SQ／CQ，VI 管一個 interrupt vector；Private Resources 固定歸屬，Flexible Resources 可受管理重新分配。 || VQ manages an SQ/CQ pair, VI a vector; private resources are fixed and flexible resources reallocatable.
先畫出 primary→secondary 關係，再標每個 controller 的可用資源與 attached namespaces，最後才規劃 queues。 || Map parentage, resources and attachment before creating queues.
每個 Online 且啟用的 secondary 仍是完整 NVMe controller，Host 可用正常 NVMe 命令操作。 || An enabled Online secondary remains a compliant NVMe controller.
不支援 Virtualization Management 的 controller 不能被要求接受資源管理命令；管理命令需送到對應 primary。 || Resource management requires support and the associated primary endpoint.
PCIe PF／VF 與 NVMe primary／secondary 在支援兩者時相對應，但不能把所有多 controller 裝置都假定有 SR-IOV。 || PF/VF map to primary/secondary when both are supported; not all multi-controller devices implement SR-IOV.
先確認實際拓樸與能力，再討論哪一台可以配置哪一台。 || First establish topology and capability before management authority.
''')
q(247,"Private 與 Shared Namespace 如何 Attach 到 Controller？ || How are private and shared namespaces attached?", [], '''
Attach 建立存取路徑，不是複製 namespace 資料。Private／Shared 決定能否同時附加到多個 controller。 || Attachment creates access paths, not copies; private/shared determines simultaneous attachments.
Private 同時只附加一台，Shared 可附加多台，但仍受命令集、資源與數量限制。 || Private permits one attached controller at a time; shared permits several subject to constraints.
查 namespace.NMIC、相關 controller 能力與已附加 Controller List。 || Inspect NMIC, controller capabilities and attachment list.
Namespace Attachment 以 NSID 指目標，SEL 指 Attach／Detach，資料 buffer 列出 CNTLID。 || Attachment uses target NSID, Attach/Detach selector and controller-ID list.
先確認目標已配置與分享能力，再 Attach 所選 controller，讀各台 Active List 驗證。 || Confirm allocation/sharing, attach and verify active lists per controller.
Shared 的多個入口看到同一份資料；Private 已有一個入口時，不能再同時增加另一個。 || Shared paths see the same data; a private namespace cannot acquire a second simultaneous attachment.
Private 已附加其他 controller 時，可對應 Namespace Is Private；重複附加同一台則是 Namespace Already Attached。 || A private namespace attached elsewhere differs from an already-attached target.
用每台 Active List 與 namespace Controller List 雙向核對，避免只看一條路徑。 || Cross-check per-controller active lists against the namespace controller list.
先檢查是「已存在」還是「已附加」，兩者不同。 || First distinguish existence from attachment.
''')
q(248,"如何取得 Namespace 對應的 Controller List？ || How is a namespace’s attached-controller list retrieved?", [], '''
這份清單回答 namespace 已附加在哪些 controller，與列出 subsystem 全部 controller 的清單不同。 || It lists attachment endpoints, not every controller in the subsystem.
查詢以指定 namespace 為範圍；同一 subsystem 中未附加的 controller 不應被誤算為可用路徑。 || Scope is the selected namespace; unattached controllers are not access paths.
使用 Identify 的 Attached Controller List 選擇，核對 CNS、NSID 與起始 Controller Identifier。 || Select Attached Controller List with the proper CNS, NSID and starting controller identifier.
回覆有數量及 Controller Identifier entries；分段時遵守起始 ID 的包含規則，不套用 Active Namespace List 的不同條件。 || Parse count/IDs and obey the inclusive starting-controller rule, not a different namespace-list pagination rule.
讀第一段，依最後 ID 推進下一次起點直到讀完，並留意期間 attachment 可能改變。 || Read successive pages using the next ID after the last entry, considering concurrent changes.
取得當時 attached controllers，再逐台確認 Online、Ready 與 ANA，才知道哪條路徑現在能用。 || Attachment discovery precedes Online/Ready/ANA availability checks.
NSID 或 CNS 不合法依 Identify 規則回應；一份空清單不代表 namespace 一定已刪除。 || Invalid selectors follow Identify rules; an empty attachment list does not prove deletion.
與各台 Active Namespace List 交叉確認，必要時在管理操作完成後重讀，避免比較不同時點。 || Cross-check per-controller active lists at consistent times.
先確認使用的是 attached list，還是 subsystem controller inventory。 || First check which controller-list selection was used.
''')
q(249,"一台 Controller Reset 時，其他路徑能否繼續存取 Shared Namespace？ || Can other paths continue during one controller’s reset?", ['ana'], '''
Shared namespace 提供多條路徑，但不能保證任何故障都完全不影響其他路徑。 || Shared namespaces provide paths, not immunity to every shared failure.
一般 CLR 針對一台；primary 重設可使其 secondary Offline，共用媒體或 domain 問題也可能擴大影響。 || CLR usually targets one controller, but primary resets offline secondaries and shared media/domain faults can broaden impact.
查 parent 關係、domain、attachment、ANA 及其他路徑 Ready 狀態。 || Check parentage, domain, attachment, ANA and readiness of alternate paths.
其他 controller 的獨立 queues 可繼續有效；但資料命令是否可執行仍受 namespace Ready、ANA 與存取限制。 || Independent queues can remain valid while namespace/ANA/access restrictions still govern I/O.
停止失效路徑新提交，確認替代路徑可用，再處理原路徑未完成命令與新命令的相依性。 || Quiesce the failed path, establish an alternative and resolve old/new command dependencies.
在其他路徑與共享資源都正常時，可以繼續存取同一資料，不需要再建立一份 namespace。 || A healthy alternative can access the same data without creating another namespace.
不能因路徑切換成功，就假定舊路徑的 Write 全部未執行；重試可能與原操作效果重疊。 || Successful failover does not prove old Writes unexecuted; retries may overlap effects.
以控制關係與命令結果判斷影響，避免「一台 Reset 一定不影響其他台」的過度概括。 || Use topology and outcomes rather than assuming universal reset isolation.
先檢查被 Reset 的是否是替代路徑所依賴的 primary。 || First check whether the reset controller is the alternate path’s parent.
''')
q(250,"NVM Subsystem Reset 會影響哪些 Controller？ || Which controllers are affected by subsystem reset?", [], '''
Reset 名稱包含 subsystem，但多 domain 裝置仍可能只重設一個 domain，必須確認實作範圍。 || Multi-domain implementations may reset one domain despite the subsystem-reset name.
單 domain 涵蓋全部；multi-domain 依實作涵蓋發起所在 domain，或全部 domains。 || Single-domain scope is all; multi-domain scope is one or all domains as implemented.
查 domain 拓樸、CAP.NSSRS 與重設後 CSTS.NSSRO。 || Inspect topology, host-reset capability and NSSRO evidence.
NSSR.NSSRC=4E564D65h 是受支援時的觸發方式；受影響範圍會 CLR 各 controller，並停用其 PMR。 || Supported NSSR triggers reset; affected controllers undergo CLR and their PMRs are disabled.
先停止範圍內工作，觸發 Reset，逐台確認重新初始化與路徑恢復。 || Quiesce the intended scope, reset and restore each affected path.
受影響 queues 必須重建；範圍外 controller 是否可用仍由其自身與共享媒體狀態決定。 || Rebuild affected queues; outside paths depend on their own/shared-resource health.
Register Reset 沒有一筆可指定 DNR／More 的 CQE；不能等待虛構的 Reset Command Completion。 || Register-triggered reset has no CQE or DNR/More.
把實際受影響 controller 清單與 domain 配置比較，而不只觀察發起端。 || Compare all affected controllers with domain configuration.
先確認裝置宣告或實作的是單 domain 還是多 domain 的 reset 範圍。 || First establish actual domain reset scope.
''',{8:'NSSR Register 寫入沒有 CQE，因此 DNR 與 More 不適用；恢復後查詢命令的 CQE 是另一筆命令的結果。 || NSSR writes have no CQE/DNR/More; post-recovery query CQEs belong to those queries.'})
q(251,"Namespace 變更如何通知其他 Controller？ || How are namespace changes reported through other controllers?", ['changedlog','aerfull','analog'], '''
管理操作可能由一條路徑發起，其他 Host 仍需要更新自己的 namespace 視圖。 || Management on one path can require rediscovery by hosts using other paths.
通知依受影響的 attached namespace 與 controller 觀察範圍，不是每台都無條件收到同一個通知。 || Notification follows affected attachment/views rather than unconditional broadcast.
查 AEC.NAN、待處理 AER、Changed Namespace List 與各台 Active List；ANA 變更另外查其通知設定。 || Check NAN, AERs, changed/active lists and separate ANA notice configuration.
Attached Namespace Attribute Changed 提醒 Host 重查，Changed Namespace List 提供需重查的 NSID；清單溢位以 FFFFFFFFh 表示需全面重查。 || The notice prompts rediscovery; changed IDs narrow it, while FFFFFFFFh requires broad rediscovery.
操作完成後處理通知、讀清單並更新 Identify；讀取確認與遮蔽規則影響後續同類通知。 || Process notice, read changes and refresh Identify with acknowledgment/masking accounted for.
其他受影響 controller 的視圖與新配置一致；不要求每次改動一筆對一筆保留無限通知。 || Affected views converge with configuration without requiring unlimited one-event-per-change history.
Admin Namespace Delete 的處理 controller 有通知排除規則，不能要求它因自己的刪除再收到相同通知。 || The processing controller has a specific Admin Delete notice exclusion.
Namespace attribute notice 與 ANA change notice 描述不同變化，不能拿其中一份 Log 取代另一份。 || Namespace and ANA notices describe different changes and logs.
先檢查事件是否對這個 controller 適用，以及舊事件是否仍遮蔽新回報。 || First check applicability and existing event masking.
''')
q(252,"Asymmetric Controller Behavior 與 ANA 如何協助選路徑？ || How do asymmetric behavior and ANA guide path selection?", ['ana','analog'], '''
相同 namespace 經不同 controller 存取，可能有不同效能或可用性；非對稱行為不只出現在網路傳輸。 || Access characteristics can differ across controllers, including PCIe paths.
ANA 狀態描述 controller 與 ANA Group 的關係；不是 namespace 永久只有一個全域狀態。 || ANA state describes a controller-to-group relationship, not one global namespace state.
查 CMIC.ANARS、ANACAP、ANATT、namespace.ANAGRPID 與 LID0Ch。 || Inspect ANA capability, transition time, group membership and LID0Ch.
Optimized／Non-Optimized 都可正常執行支援命令；Inaccessible、Persistent Loss 與 Change 對資料存取有不同限制與恢復建議。 || Optimized/non-optimized support normal commands; inaccessible, persistent loss and change impose distinct restrictions.
先找可用路徑，再優先考慮 Optimized；遇到通知重新讀 ANA，不能永久把某 controller 寫死為最佳路徑。 || Select accessible paths, prefer optimized access and refresh after notices.
Non-Optimized 可能較慢但不是錯誤；另一條路徑可對同一群組回不同狀態。 || Non-optimized is usable, and another path may report a different state for the same group.
受限制狀態對非例外命令分別回 Asymmetric Access Inaccessible、Persistent Loss 或 Transition；不是所有 Admin 命令都被一律禁止。 || Restricted states use their corresponding asymmetric-access status for nonexempt commands, not every Admin command.
僅量到效能不同，不能反推必定支援 ANA Reporting；應先確認宣告再用 Log 解釋。 || Different performance does not prove ANA reporting support; check capability first.
先確認 ANAGRPID 對應的 controller 視圖，而不是讀錯路徑的 Log。 || First match group state to the actual controller path.
''')
q(253,"Secondary Controller 如何 Online 或 Offline？ || How does a secondary transition Online or Offline?", [], '''
Online 代表資源與狀態允許 Host 使用，還不等於 CC.EN／RDY 已經完成啟用。 || Online permits use but is not the same as enabled/ready.
由 associated primary 管理該 secondary；Offline 時 CSTS.CFS=1，其他 controller properties undefined。 || The associated primary manages it; Offline sets CFS and leaves other properties undefined.
查 Secondary List.SCS、NVQ、NVI 與 primary 是否已 enabled。 || Inspect secondary state/resource counts and primary enablement.
Virtualization Management ACT=7 Offline、8 Assign、9 Online；Offline 會移除 Flexible Resources。 || ACT7 offlines,8 assigns and 9 onlines; offlining removes flexible resources.
建議先 Offline，再配置 VQ／VI，做 CLR；若為 VF 建議 VF FLR，再 Online，最後執行 NVMe enable 與 queue 初始化。 || Recommended sequence: Offline, assign, CLR (prefer VF FLR for a VF), Online, then enable and initialize queues.
支援 VQ 時至少 2 組，包含 Admin 與至少 1 組 I/O；支援 VI 時至少 vector0 的資源，才可 Online。 || With flexible VQ support, at least two resources are needed; with VI support, vector0 must be assigned.
未 Offline 就 Assign，或資源不足／primary 未 enabled 卻要求 Online，回 Invalid Secondary Controller State；重複相同 Online／Offline 不是錯誤。 || Wrong state or insufficient Online prerequisites cause Invalid Secondary Controller State; repeated same-state requests are allowed.
把 SCS 與 CC.EN／CSTS.RDY 分開驗證，避免把 Offline 的 CFS 當成一定發生未知硬體故障。 || Validate Online and Enable separately; expected Offline CFS is not unexplained hardware failure.
先檢查資源與狀態前提是否完成，再判斷啟用超時。 || First establish prerequisites before diagnosing enable timeout.
''')
q(254,"Virtualization Management 如何分配與釋放資源？ || How are virtualization resources assigned and released?", [], '''
Flexible Resource pool 可在 primary 與它的 secondary 間分配，但不是動態擴充實體總資源。 || Flexible allocation redistributes a finite pool rather than creating resources.
VQ 與 VI 分開計數；Private Resources 不可用此命令重新指派。 || VQ and VI are separate pools; private resources cannot be reassigned.
查 CRT、總量、已分配量、secondary 最大值與 preferred granularity。 || Read resource types, totals, assignments, per-secondary maxima and granularity.
CDW10.CNTLID／RT／ACT 選目標、種類與動作，CDW11.NR 指要求數量；CQE.DW0.NRM 是實際修改數量。 || CNTLID/RT/ACT select target/type/action, NR requests a count and NRM reports the modified count.
secondary 先 Offline，再 Assign；要釋放 Online secondary 的 Flexible Resources，可將其 Offline。Primary 新配置則等指定類型的 CLR 才生效。 || Assign only while Offline; offlining removes secondary resources. Primary allocation changes need the specified later reset.
NRM 可比 NR 小或大，須讀回能力與清單確認，不能把 requested count 當成實際值。 || NRM may be smaller or larger than NR; verify actual allocation.
超出總量或每台上限對應 Invalid Number of Controller Resources；不存在、Private 或已被使用的資源範圍對應 Invalid Resource Identifier。 || Invalid total/per-controller count differs from invalid/private/in-use resource ranges.
將所有配置加總與 pool 比較；相同 resource 不能同時屬兩台，preferred granularity 也不能直接當成任意硬性拒絕規則。 || Reconcile pool ownership and distinguish preferred granularity from mandatory rejection.
先檢查 CQE.NRM 與 readback，而不是只看送出的 NR。 || First check NRM and readback rather than requested NR.
''')
q(255,"Reset 與 Power Cycle 後 Virtualization 資源如何恢復？ || How are virtualization resources restored after reset and power cycle?", [], '''
Primary 的持久配置與 secondary 的即時資源指派有不同生命週期，必須分開保存與驗證。 || Primary persistent allocation and secondary live assignment have different lifetimes.
除了被重設的 controller，也要檢查依賴該 primary 的 secondary 群組。 || Include dependent secondaries, not only the reset controller.
保存 Primary Capabilities、Secondary List、重設來源與 PCIe function 關係。 || Snapshot capabilities, secondary list, reset source and function relationships.
Primary Flexible Allocation 是持久設定，新值在非 Controller Reset 的 CLR 後生效；僅清 CC.EN 不符合這個生效條件。 || Primary allocation is persistent and new values take effect after CLR other than CC.EN Controller Reset.
Primary 恢復後重新查 secondary 狀態，依 Offline→Assign→適當 CLR→Online→Enable 重建使用環境。 || After primary recovery, rediscover and rebuild secondary operation through the required sequence.
可保留的 allocation 設定正確恢復，secondary 重新取得適足資源，新的 queues 才有效。 || Persistent allocation and freshly established secondary resources/queues are validated separately.
不能因 primary allocation 還在，就要求 secondary 原 I/O queues 或原 Online 狀態一併保留。 || Retained primary allocation does not preserve secondary queues or Online state.
Namespace attachment 可持續存在，即使 secondary 暫時 Offline；不應因此重複 Create Namespace。 || Persistent attachment can remain while secondary is Offline; do not recreate the namespace merely for that reason.
先檢查 Reset 是否使 primary Disable，連帶造成 secondary Offline 與資源移除。 || First check the primary-reset cascade into secondary Offline/resource removal.
''')
