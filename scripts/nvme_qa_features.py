from scripts.nvme_qa_model import add

add(54,'Feature 的 Current、Default、Saved Value 及 Supported Capabilities 分別代表什麼？ || What do Current, Default, Saved and Supported Capabilities mean?','feature',['feature','getfeat','idctrl'],'''
分開正在使用的值、出廠預設、持續保存值及「能不能改／存」的能力；這四者不是四份相同設定。 || Separate the active value, manufacturing default, saved value and change/save capabilities; these are not four identical settings.
同一 FID、scope 與 selector 下比較才有意義；不同 namespace 的 Current 可能不同。 || Compare the same FID, scope and selectors; Current can differ across namespaces.
Identify.ONCS.SSFS 表示 Save／Select 支援；具備此機制後用 Get Features.SEL=3 查該 FID 的 CHANG、NSSPEC、SVBL。 || ONCS.SSFS advertises Save/Select support. Under that mechanism, Get Features.SEL=3 returns CHANG/NSSPEC/SVBL for the FID.
SEL=0 Current、1 Default、2 Saved、3 Supported Capabilities。SEL=3 的 DW0 bit2／1／0 分別是 CHANG／NSSPEC／SVBL，不是 Feature 的工作值。 || SEL0/1/2/3 select Current/Default/Saved/Supported Capabilities. With SEL3, DW0 bits2/1/0 are CHANG/NSSPEC/SVBL, not operational values.
先讀能力，再讀 Current；需要比較重設結果時才讀 Saved／Default。不可保存或尚無 Saved 時，SEL=2 回 Default；個別 Feature 沒有 Default 的例外另處理。 || Read capabilities and Current first, then Saved/Default for reset analysis. If unsaveable or never saved, SEL2 returns Default, subject to features that define no Default.
例如 SEL3 回 5 表示可改、可存、NSSPEC=0；不表示 Current=5。NSSPEC=0 也不能單獨推論一定是 controller scope。 || SEL3 result5 means changeable, saveable and NSSPEC=0, not Current=5. NSSPEC=0 alone does not establish controller scope.
不支援 FID 為 Invalid Field（0/02h）。SEL=4～7 是保留編碼；SEL 未支援時不能把能力查詢結果當成有效 CHANG／SVBL。 || Unsupported FID uses Invalid Field (0/02h); SEL4–7 are reserved. Without Select support, do not treat a response as valid CHANG/SVBL discovery.
比對時同時保留 FID 與 SEL；只有回傳 DW0 數字沒有辦法知道是值還是能力 bitmap。 || Preserve FID and SEL with the returned DW0 to distinguish a value from a capability bitmap.
先查 SEL，這通常比懷疑 Set 沒生效更早排除解碼錯誤。 || First check SEL before concluding that Set failed to take effect.
''')

add(55,'Set Features 的 Save 位元如何影響 Controller Reset 與 Power Cycle 後的 Feature 值？ || How does Set Features.Save affect values after reset and power cycling?','feature',['feature','setfeat','getfeat'],'''
讓 Host 決定只改目前值，或同時更新下次恢復時使用的持續值。 || Let the host change only the active value or also the persistent value used on restoration.
保存依 Feature scope；namespace-scoped 保存與 controller-scoped 保存不能混成一份全域設定。 || Saving follows feature scope; namespace-scoped and controller-scoped settings are not one global value.
確認 ONCS.SSFS 與此 FID 的 SVBL；「裝置支援 Save」不保證每個 Feature 都可保存。 || Check ONCS.SSFS and the FID's SVBL. Controller Save support does not make every feature saveable.
Set CDW10.SV=0 改 Current、不改 Saved；SV=1 成功時改 Current 與 Saved。Default 不因此變成 Host 設的值。 || SV=0 changes Current without updating Saved; successful SV=1 updates both. Default does not become the host's chosen value.
先查支援，Set 並等待完成，再分別 Get Current／Saved；經指定重設後依 scope 及例外驗 Current。 || Discover support, Set and await completion, then read Current/Saved separately. After the chosen reset, verify Current under scope and exception rules.
例：Saved=A，SV=0 改成 B，目前應使用 B；符合 Saved 恢復條件的重設後回 A，不是 B。 || With Saved=A and an SV=0 change to B, Current becomes B; a reset that restores Saved returns it to A, not B.
不可保存卻 SV=1 必須回 Feature Identifier Not Saveable（SCT=1, SC=0Dh）；不能默默成功後遺失設定。 || SV=1 for an unsaveable feature shall return Feature Identifier Not Saveable (1/0Dh), not silently succeed and lose the saved setting.
保存成功、目前生效與重設後恢復是三個驗證點；僅 Get Current=B 不證明 Saved=B。 || Save success, active application and restoration are three separate checks. Current=B does not establish Saved=B.
先看原 Set 的 SV 與該 FID 的 SVBL，再看發生的是哪種、哪個範圍的重設。 || First inspect original SV/SVBL, then reset type and coverage.
''')

add(56,'不支援的 Feature、不合法 Feature 值或 Controller 不支援 Save 時，應如何回應？ || Which errors apply to unsupported features, invalid values and unsupported Save?','feature',['feature','setfeat','getfeat','status'],'''
區分不支援功能、不能改、不能保存與值不合法；它們有不同原因和修正方法。 || Distinguish unsupported function, unchangeability, unsaveability and invalid value; their causes and corrections differ.
針對該 FID、目標 scope、目前狀態與此次 Set／Get，不是只看 controller 型號。 || Evaluate the FID, target scope, current state and this Get/Set operation, not merely the controller model.
Get SEL3 的能力需配合 ONCS.SSFS；CHANG=1 只代表至少有可改的值，不保證目前進入的永久狀態仍可改。 || SEL3 capabilities require SSFS. CHANG=1 means some values are changeable, not that a current permanent state can be reversed.
檢查 FID、SV、NSID、CDW11 及資料 buffer；有些 Feature 需要特定 selector，不能只檢查 DW0。 || Check FID, SV, NSID, CDW11 and payload. Some features require selectors beyond a single value.
用合法 Current 建基準，再分開測不支援 FID、非法值、SV=1、scope 錯誤；避免一筆同時違反多項。 || Establish a valid baseline, then separately test unsupported FID, bad values, SV=1 and wrong scope.
合法 Set 完成後才是已設定；對不可改 Feature 寫相同值，規範允許成功或 Feature Not Changeable，不能只接受其中一種。 || Successful Set establishes completion. Setting an unchangeable feature to its existing value may succeed or return Feature Not Changeable; both are permitted.
不支援 FID／非法定義值：0/02h；不可保存：1/0Dh；不可改：1/0Eh；controller-scope 的 Set 卻給有效 NSID：1/0Fh。個別 FID 的順序或狀態錯誤優先。 || Unsupported FID/invalid defined value:0/02h; unsaveable:1/0Dh; unchangeable:1/0Eh; controller-scoped Set with a valid NSID:1/0Fh. Specific FID ordering/state errors take precedence.
錯誤完成後重新 Get，確認結果符合那個 Feature 的錯誤處理；不要把回錯誤與一定完全沒有副作用畫等號。 || Re-read after failure according to the feature's error rules; an error is not a universal proof of no side effects.
先排除測例同時非法的情況，否則不同合法錯誤碼可能被誤判。 || First exclude multiple simultaneous faults that allow different valid error choices.
''')

add(57,'Host 如何判斷某個 Feature 是否需要指定 NSID？ || How does the host determine whether a feature requires NSID?','feature',['feature','getfeat','setfeat','nvmfeat'],'''
在寫設定前選對作用對象，避免把 controller 設定誤送成 namespace 設定。 || Select the correct target before changing configuration.
Feature scope 可為 controller、namespace、subsystem、Set、Group 或其他管理物件；不是只有兩種。 || Feature scope can be controller, namespace, subsystem, set, group or another management entity, not just two categories.
SEL3.NSSPEC=1 表示 namespace scope；=0 時再看 Feature Identifiers Supported and Effects 的 scope 及 Figure 466／NVM Figure92。 || SEL3.NSSPEC=1 indicates namespace scope. With zero, inspect the feature-effects scope and Figure466/NVM Figure92.
controller scope 的 Get／Set 可用 NSID=0 或 FFFFFFFFh；有效 namespace ID 用於 controller-scope Get 可回 controller 值，但 Set 要回 scope 錯誤。 || Controller-scoped Get/Set accepts NSID0 or FFFFFFFFh. A valid namespace ID on Get can return the controller value, whereas Set must report the scope error.
先確認 FID scope，再填 NSID 與其他物件 selector。namespace scope 通常用 active NSID；broadcast Get 與 Set 的規則不同，multi-domain 還有限制。 || Determine scope, then NSID and other selectors. Namespace scope normally uses an active NSID; broadcast Get/Set differ and multi-domain restrictions apply.
例：FID05h Error Recovery 設 namespace，FID01h Arbitration 設 controller；兩者即使 CDW11 都是數值也不能共用相同 NSID 規則。 || FID05h Error Recovery is namespace-scoped and FID01h Arbitration controller-scoped; numeric CDW11 values do not make their NSID rules interchangeable.
controller-scope Set 給有效 NSID：Feature Not Namespace Specific（1/0Fh）。namespace-scope Get 用 FFFFFFFFh 一般為 Invalid Namespace or Format（0/0Bh），個別例外優先。 || Controller-scoped Set with a valid NSID returns1/0Fh. Namespace-scoped Get with FFFFFFFFh generally returns0/0Bh, subject to specific exceptions.
NSSPEC=0 與 subsystem／Set scope 可以同時成立，不能把它解成「所有 namespace 都套同一個 controller 值」。 || NSSPEC=0 can coexist with subsystem/set scope; it does not universally mean one controller value for all namespaces.
先看 scope 定義，再檢查原命令 NSID，不先猜 namespace 是否壞掉。 || First read the scope definition and original NSID before suspecting namespace failure.
''')

add(58,'Arbitration、Number of Queues 及 I/O Command Set Profile Feature 如何設定與驗證？ || How are Arbitration, Number of Queues and I/O Command Set Profile configured and checked?','feature',['arbit','number','profile','idlist','setcomplete','status'],'''
三者分別控制排程參數、queue 配額與可使用的 command-set 組合，必須放在正確初始化階段。 || These control scheduling parameters, queue allocations and allowed command-set combinations at different initialization stages.
本題三個 Feature 都以 controller 為作用入口，但改 Profile 會影響 namespace 與命令集可用性。 || All three target controller configuration, while Profile affects namespace/command-set usability.
Arbitration 看 CAP.AMS／CC.AMS；Number of Queues 看成功 Set 回覆；Profile 先看 CAP.CSS.IOCSS 與 CNS1Ch vectors。 || Arbitration uses CAP.AMS/CC.AMS; queue allocation uses successful Set results; Profile requires CAP.CSS.IOCSS and CNS1Ch vectors.
FID01h：AB／HPW／MPW／LPW；FID07h：NSQR／NCQR→NSQA／NCQA；FID19h：IOCSCI 是組合 index。 || FID01h uses AB/HPW/MPW/LPW; FID07h maps requested to allocated SQ/CQ counts; FID19h.IOCSCI is a combination index.
按初始化流程先選 Command Set Profile、確認 namespace，再配置 Number of Queues 並建 CQ／SQ；Arbitration 參数與 CC.AMS／QPRIO 協同驗證。 || Select the profile and discover namespaces, allocate queues and create CQs/SQs; verify arbitration parameters together with CC.AMS/QPRIO.
Get 回讀需用同 FID 與 selector。CC.CSS≠110b 時，Set FID19h 成功但沒有作用；CC.CSS=110b 時才使用選到的組合。Profile index=0 指第 0 組，不代表停用命令集；FID07h 的配額則不代表已建立 queue 數。 || Read back the same FID/selectors. With CC.CSS other than110b, Set FID19h succeeds without effect; with110b, the selected combination applies. Profile index0 selects combination0, not no command sets. FID07h allocation is not instantiated queue count.
FID07h 建 queue 後再 Set 是0/0Ch。CC.CSS=110b 時，若 IOCSCI 選到值為 0 的組合，或已 attach 的 namespace 使用了該組合不支援的命令集，FID19h 須回 Combination Rejected。注意規格內部差異：Figure104 將 Combination Rejected 列為1/2Bh，Figure554 列為1/15h；本題保留此差異，不僅靠其中一表判韌體違規。 || Setting FID07h after queue creation returns0/0Ch. With CC.CSS=110b, FID19h shall return Combination Rejected if IOCSCI selects a zero-valued combination or an attached namespace uses an I/O command set absent from that combination. The supplied spec conflicts: Figure104 lists Combination Rejected as1/2Bh, Figure554 as1/15h. Preserve that discrepancy rather than declaring noncompliance from either table alone.
同時驗設定、可建立 queue 範圍與實際可用命令集；三個 Feature 的 Get 值不能互相代替。 || Verify settings, creatable queue ranges and usable command sets independently.
先確認順序：是否在已建 I/O queue 後才想重新分配數量。 || First check whether queue allocation was attempted after I/O queue creation.
''')

add(59,'Interrupt Coalescing 與 Interrupt Vector Configuration 如何設定與驗證？ || How are interrupt coalescing and vector configuration set and verified?','feature',['irqfeat','irq','create'],'''
以可接受的通知延遲換取較低的中斷處理負擔；completion 張貼與 IRQ 產生不是同一時間點。 || Trade notification latency against interrupt overhead; posting a completion and generating an IRQ are different events.
FID08h 控制 I/O interrupt coalescing；FID09h 對指定 vector 決定是否套用 coalescing。Admin CQ 不支援 coalescing。 || FID08h controls I/O interrupt coalescing; FID09h selects its application per vector. Admin CQ does not support coalescing.
檢查 CQ.IEN／IV、PCIe interrupt 模式及 mask。PCIe 規範要求支援這些 Feature，但聚合演算法可以有實作差異。 || Check CQ.IEN/IV, PCIe interrupt mode and masks. Feature support is required, while aggregation algorithms remain implementation-specific.
FID08h：TIME 單位100 μs、THR 為 zero-based；任一為0會隱含停用 coalescing。FID09h：IV 與 CD，CD=1 是不聚合，不是遮蔽中斷。 || FID08h TIME uses100 μs units and THR is zero-based; either zero implicitly disables coalescing. FID09h uses IV/CD; CD=1 disables coalescing, not interrupts.
先以 Create CQ 關聯合法 vector，再 Set FID09h；設定 FID08h 後 Get 回讀，以多筆 completion 的時間與 IRQ 行為一起觀察。 || Associate a valid vector with a CQ before Set FID09h. Set/read FID08h and observe CQE timing alongside interrupts.
參數成功生效，但不能把 TIME／THR 當成對每個 workload 絕對精準的中斷時刻；PCIe 描述其使用方式為 implementation specific，甚至可不實作聚合。 || Settings can complete successfully without defining exact IRQ timing for every workload. PCIe makes parameter use implementation-specific and permits no coalescing implementation.
FID09h 的 IV 非法或未關聯既有 I/O CQ，應回 Invalid Field（0/02h）；這不同於 Create CQ 的 Invalid Interrupt Vector（1/08h）。 || Invalid or unassociated IV in FID09h should return Invalid Field (0/02h), unlike Create CQ's Invalid Interrupt Vector (1/08h).
驗 Get 值、CQ 配置、mask 與通知行為；CD=1 後仍被 MSI-X mask 遮住，不是不聚合設定失敗。 || Check readback, CQ mapping, masks and notification behavior. CD=1 does not override an MSI-X mask.
先區分 coalescing disable 與 interrupt masking，兩者不能用同一個 bit 解釋。 || First distinguish disabling coalescing from masking interrupts.
''')

add(60,'Volatile Write Cache 與 Write Atomicity Normal 控制什麼行為？ || What do Volatile Write Cache and Write Atomicity Normal control?','feature',['vwc','nvmfeat','nvmatomic','idns'],'''
分開持久性與原子性：資料是否已進入非揮發儲存，與多個 logical blocks 是否以規定單位更新，是不同保證。 || Separate persistence from atomicity: reaching nonvolatile storage is different from updating logical blocks as a defined unit.
FID06h 管 controller volatile write cache；FID0Ah 決定正常寫入原子性要求，不能直接改 namespace 的 atomic unit 宣告。 || FID06h controls controller volatile caching; FID0Ah controls normal atomicity requirements, not the advertised namespace atomic units.
VWC 宣告 cache 是否存在；AWUN／AWUPF、namespace overrides 與 boundary 描述原子性。 || VWC advertises cache presence; AWUN/AWUPF, namespace overrides and boundaries describe atomicity.
FID06h.WCE=0 時寫入使用者資料必須持久；FID0Ah.DN=1 不要求 AWUN／NAWUN，但仍須遵守 AWUPF／NAWUPF。 || With FID06h.WCE=0, written user data must be persistent. FID0Ah.DN=1 removes AWUN/NAWUN requirements while retaining AWUPF/NAWUPF.
先讀能力與格式，Set 後 Get，再用符合單位和邊界的假設 Write 比較允許結果；若需讓既有工作與新設定分界清楚，先排空。 || Read capabilities/format, Set/Get, then compare allowed outcomes for Writes respecting units/boundaries. Drain first for a clean setting transition.
WCE=0 不會讓任意大小 Write 都原子；DN=1 也不會自動讓完成資料持久。兩個控制不能互相代替。 || WCE=0 does not make arbitrary-size writes atomic; DN=1 does not make completion persistent. The controls are not substitutes.
沒有 volatile cache 卻 Get／Set FID06h，須回 Invalid Field（0/02h）；其他參數與 namespace／atomic 規則依適用命令判斷。 || Get/Set FID06h without volatile cache shall return Invalid Field (0/02h). Other conditions follow applicable command/namespace/atomicity rules.
把 Current.WCE／DN 與 Identify 的有效 atomic unit 一起看；FUA 是個別命令持久性要求，不擴大 atomic unit。 || Correlate Current.WCE/DN with the effective atomic units. FUA requests persistence for a command without enlarging its atomic unit.
先釐清預期是「不撕裂」還是「斷電不遺失」，再選驗證欄位。 || First identify whether the requirement is no torn update or survival of power loss.
''')

add(61,'Asynchronous Event Configuration 如何決定哪些事件需要回報？ || How does Asynchronous Event Configuration select reported events?','feature',['aec','aer','idctrl','nvmfeat'],'''
讓 Host 選擇需要的狀態變更通知；它不會替 Host 自動送出等待事件的 Request。 || Select desired change notifications; configuration does not submit an event request on the host's behalf.
FID0Bh 作用於 controller 的通知設定，個別通知對應 SMART、namespace 或其他不同 scope 的狀態。 || FID0Bh configures controller notifications about state with various scopes.
OAES 表示選配事件支援，SMART 的警告也有相應能力；NVM 特定 bit 另見 NVM 規格。 || OAES advertises optional event support, with applicable health capabilities and NVM-specific bit definitions.
CDW11 的各啟用 bit 選通知；AER completion 的 AET／AEI／LID 描述實際事件。兩者不是相同 bitmap。 || CDW11 enable bits select notifications. AER completion AET/AEI/LID describes the event; it is not the same bitmap.
查支援→Set 合法事件 mask→掛 AER→條件成立→讀事件及對應 Log→依事件規則確認並補 Request。 || Discover support, Set the mask, post AER, observe a condition, read the event/log, acknowledge under its rules and replenish requests.
若啟用時條件已成立，也會依本 Feature 的規則送事件；不是只有設定後新發生的變化才可能回報。 || A condition already true when enabled is also reported under this feature's rules; reporting is not limited to later state changes.
嘗試啟用 controller 不支援的事件，須回 Invalid Field（0/02h）。沒有 outstanding AER 導致尚未收到通知，不是 Set Features 錯誤 Status。 || Enabling an unsupported event shall return Invalid Field (0/02h). No outstanding AER can delay notification without being a Set Features error.
核對 OAES、Current mask、pending Request 與事件是否仍被遮蔽；只看 mask=1 不能證明 Host 一定立即收到。 || Correlate OAES, Current mask, pending requests and event masking. An enabled bit alone does not guarantee immediate delivery.
先檢查是否真的掛入尚未完成的 AER，以及先前事件是否已按規則確認。 || First check outstanding AERs and acknowledgement of prior events.
''',{9:'本題正是設定通知。事件種類有各自條件與清除規則；FID0Bh 不是所有 Error 類型事件的通用總開關，也不能用 Get Features 代替補 AER。 || This feature configures notifications, with event-specific conditions and clearing rules. FID0Bh is not a universal switch for every Error event, and Get Features does not replenish AERs.'})

add(62,'Power Management、Autonomous Power State Transition 及 Host Controlled Thermal Management 有何差異？ || How do Power Management, APST and Host Controlled Thermal Management differ?','feature',['power','thermal','idctrl'],'''
分開 Host 直接選 power state、閒置時自動轉換，以及依溫度降低功耗／效能三種控制。 || Separate explicit host power-state selection, idle-driven automatic transitions and temperature-driven power/performance management.
設定以 controller 為入口；多 controller 共用 domain 時，功耗狀態可能互相影響，不能只觀察單一路徑。 || Configuration targets a controller, while shared-domain controllers can interact in power behavior.
讀 NPSS／Power State Descriptors、APSTA 與 HCTMA、MNTMT／MXTMT。 || Read NPSS/power-state descriptors, APSTA, HCTMA and MNTMT/MXTMT.
FID02h 選 PS 與相關限制；FID0Ch.APSTE 啟用 32-entry 表，每格 ITPT 是該狀態的 idle ms、ITPS 是目標非工作狀態；FID10h.TMT1／TMT2 是 Kelvin 溫度。 || FID02h selects PS and related limits. FID0Ch.APSTE enables a32-entry table with ITPT idle milliseconds in that state and ITPS targeting a nonoperational state. FID10h TMT1/TMT2 use kelvins.
先看可用 states 與 latency，再決定主動 PS 或 APST 表；另設定合法 TMT1<TMT2（兩者非零時）。APST 每到新 state，使用新 state 的 idle 條件。 || Discover states/latencies, select explicit PS or an APST table and separately set legal TMT1<TMT2 when both are nonzero. Each new state uses its own idle-transition condition.
Set FID02h 成功時已到指定 PS，但 APST 啟用後還可再自動轉移；HCTM 觸發不等於 Host 又送了一筆 Power Management。 || Successful FID02h Set establishes the requested PS, but enabled APST may transition again. HCTM activity is not another host Power Management command.
不支援 state、非法 APST 目標或溫度範圍／順序，用對應欄位要求判 Invalid Field（0/02h）；不能以「較省電」合理化非法設定。 || Unsupported states, invalid APST targets and illegal thermal ranges/order follow the relevant Invalid Field (0/02h) requirements.
Get 設定、目前操作狀態、SMART 溫度與 HCTM 計數分開比對；不能只用功耗下降推論是 APST。 || Compare configuration, operational state, SMART temperature and HCTM counters separately. Lower power alone does not identify APST as the cause.
先辨認觸發來源是 Host Set、idle 計時還是溫度，再檢查該路徑設定。 || First identify whether the trigger was host Set, idle timing or temperature.
''',{12:'Power Management／APST 不可保存時依 Figure466 回預設；HCTM 在不可保存情況仍標為持續。若可保存，改按 Saved 規則；同 domain 多 controller 的控制還需協調。 || Non-saveable Power Management/APST follows Figure466 defaults; non-saveable HCTM is persistent. Saveable configurations use Saved rules, with coordination among controllers sharing a domain.',14:'不能把這三個 FID 都歸成斷電清除：不可保存的 HCTM 持續，而 Power Management／APST 不持續；可保存者依 Saved 恢復。 || Do not classify all three as volatile: non-saveable HCTM persists, whereas Power Management/APST do not; saveable features restore Saved.'})

add(63,'Timestamp、Keep Alive Timer 及 Host Memory Buffer 如何設定與驗證？ || How are Timestamp, Keep Alive Timer and Host Memory Buffer configured and verified?','feature',['timestamp','keepalive','hmb','idctrl'],'''
三者分別提供事件時間基準、通訊存活監測與 controller 可專用的 Host 記憶體；不可共用同一種驗證方法。 || These provide event time, communication-liveness monitoring and dedicated host memory, requiring different validation methods.
Timestamp／Keep Alive 是 controller 時間狀態；HMB 還涉及 Host 記憶體使用權與生命週期。 || Timestamp/Keep Alive are controller time state; HMB also controls ownership/lifetime of host memory.
Timestamp 看 ONCS；Keep Alive 看 KAS 與 CTRATT.TBKAS；HMB 看 HMPRE、HMMIN、HMMINDS、HMMAXD。 || Check ONCS for Timestamp, KAS/CTRATT.TBKAS for Keep Alive, and HMPRE/HMMIN/HMMINDS/HMMAXD for HMB.
FID0Eh 用8-byte buffer 設48-bit ms Timestamp；FID0Fh 用 KATO ms 並按 KAS×100 ms 向上取整；FID0Dh 設 EHM／MR、HSIZE、descriptor address／count。 || FID0Eh sets a48-bit millisecond Timestamp in an8-byte buffer. FID0Fh sets KATO milliseconds rounded up to KAS×100 ms. FID0Dh configures EHM/MR, HSIZE and descriptor address/count.
Timestamp Set 後 Get 應增加已過時間；KATO Set 後 Get 讀實際取整值；HMB 準備合法頁面再 Enable，停用成功後才能收回。MR=1 必須連內容與 descriptor 都與先前相同。 || Timestamp Get should reflect elapsed time; KATO Get returns the rounded value. Allocate valid HMB pages before enabling and reclaim only after successful disable. MR=1 requires unchanged contents and descriptors as well as layout.
例：KAS=10、KATO要求1500 ms，取整後為2000 ms。HMB 的 Get 同時回 CQE 狀態及 attributes buffer，不是只有一個開關值。 || KAS=10 rounds requested KATO1500 ms to2000 ms. HMB Get returns CQE state and an attributes buffer, not only an enable bit.
HMB 已啟用再 Enable：Command Sequence Error（0/0Ch）；HMDLEC=0：Invalid Field（0/02h）。PCIe KATO=0 可停用，不能套用其他 transport 的強制啟用規則。 || Re-enabling enabled HMB returns0/0Ch; HMDLEC=0 returns0/02h. PCIe allows KATO=0 to disable; do not import another transport's mandatory-enablement rule.
Timestamp 看 Origin／Synch，不硬當絕對時鐘；KATO 看取整後 Current；HMB 看能力、配置、實際 EHM 與記憶體是否仍被保留。 || Check Timestamp Origin/Synch rather than assuming a perfect wall clock, rounded KATO Current and HMB support/configuration/EHM/memory retention.
先分清此次 FID 的結果在 CQE 還是 data buffer，並確認各時間和大小單位。 || First locate the result in CQE versus data buffer and verify time/size units.
''',{11:'若支援 PEL，Timestamp Change 按事件條件記錄；Set Features 的記錄則查該 FID 的要求與 PEL 支援。不能把時間每增加 1 ms 都當一筆 Timestamp Change。 || With PEL support, Timestamp Change follows its event conditions; feature logging follows per-FID requirements. Ordinary one-millisecond advancement is not a Timestamp Change event.',12:'HMB 不保留啟用設定，重設後重新配置；MR=1 只在記憶體及內容完整保留時可用。Timestamp 若跨該種 CLR 繼續更新須保留 Origin；不繼續更新時，CLR 會將 Timestamp 清為 0；若有 Saved 恢復，還須配合保存值，並回讀 Origin。Keep Alive 依其可保存／預設規則重新確認。 || HMB enable configuration is not retained and must be restored; MR=1 requires fully retained memory/content. A Timestamp maintained across that CLR must retain Origin; otherwise CLR clears the timestamp to zero; also account for a restored Saved value and read back Origin. Recheck Keep Alive under its save/default rules.',13:'受影響 controller 的 HMB 需重配；Timestamp 不能假設每種 CLR 都有相同延續結果；Keep Alive 必須依恢復後 Current 重建 Host 的維持計時。 || Reconfigure HMB on affected controllers, do not assume identical Timestamp continuity for all CLR methods, and rebuild host Keep Alive timing from restored Current.',14:'HMB 不是非揮發儲存，不能因位址相同就宣稱 MR=1。Timestamp 若恢復 Saved 可能倒退至保存值；PCIe Keep Alive 未另保存時預設 KATO=0。 || HMB is not nonvolatile storage; equal addresses do not justify MR=1. Restoring Saved Timestamp may move time backward. PCIe Keep Alive defaults to KATO=0 unless restoration rules provide otherwise.'})

add(64,'Host Behavior Support、Error Recovery 及 Read Recovery Level 有什麼用途？ || What do Host Behavior Support, Error Recovery and Read Recovery Level do?','feature',['behavior','nvmfeat','rrl','status'],'''
分別告訴 controller Host 懂哪些擴充、設定特定 namespace 的錯誤恢復屬性、選擇讀取恢復策略。 || Advertise host understanding of extensions, configure namespace error recovery and choose a read-recovery strategy.
FID16h 為 controller；FID05h 為 namespace；FID12h 依支援的 NVM Set 模型為 NVM Set 或 subsystem。 || FID16h is controller-scoped, FID05h namespace-scoped, and FID12h set/subsystem-scoped according to NVM Set support.
ACRE 與相關能力配合使用；DULBE 先查 namespace NSFEAT.DAE；Read Recovery Level 先查 RRLS 支援 bitmap。 || Pair ACRE with relevant capabilities, check NSFEAT.DAE before DULBE and RRLS before selecting a recovery level.
FID16h 的 data buffer 含 ACRE、LBAFEE 等；FID05h.TLER 單位100 ms、DULBE 在 bit16；FID12h 的 RRL 是等級碼，不是 RRLS bitmap。 || FID16h payload includes ACRE/LBAFEE. FID05h TLER uses100 ms and DULBE bit16. FID12h RRL is a level code, not the RRLS bitmap.
先確認能力再設定；TLER 從錯誤恢復開始計時，不能拿它當從提交起算的所有命令 timeout。RRL 需對支援的目標設定後讀回。 || Discover support before Set. TLER starts when error recovery begins, not at command submission as a universal timeout. Set/read an advertised RRL for the correct target.
ACRE 允許適用的 advanced retry 行為；DULBE 改變未寫／deallocated block 的回應；選 Fast Fail 不表示保證固定 latency 或零次內部嘗試。 || ACRE enables applicable advanced retry behavior; DULBE changes unwritten/deallocated-block responses. Fast Fail does not promise fixed latency or zero internal attempts.
未支援等級、非法設定按 Invalid Field（0/02h）等專屬規則；Command Interrupted（0/21h）只有 ACRE=1 才能回，且 DNR 必須0。 || Unsupported levels/invalid settings follow0/02h and applicable rules. Command Interrupted0/21h requires ACRE=1 and DNR=0.
LBAFEE 會影響可用擴充格式的呈現與使用；能力、Host 宣告與 namespace 格式需一起解讀。 || LBAFEE affects exposure/use of extended formats; interpret capability, host declaration and namespace format together.
先檢查是不是把 TLER 当整筆命令期限，或把 RRLS 的位元位置直接當 RRL 數值。 || First check whether TLER was treated as whole-command timeout or RRLS was confused with an RRL code.
''',{12:'不可保存的 Host Behavior Support 與 Error Recovery 不持續，Read Recovery Level 則持續；可保存時改按 Saved 與 scope 的重設規則。 || Non-saveable Host Behavior Support and Error Recovery are nonpersistent, while Read Recovery Level persists. Saveable cases follow Saved and scope-dependent reset rules.',14:'Power Cycle 後重新取得各 FID 的 Current。不可保存的 RRL 仍持續，不能因沒有 Saved 就認定應回0；Host Behavior Support／Error Recovery 另按其恢復規則。 || Re-read Current after a power cycle. Non-saveable RRL still persists; absence of Saved does not mean it must return zero. Host Behavior Support/Error Recovery use their separate restoration rules.'})

add(65,'Namespace Write Protection 如何設定？不同保護模式在 Reset 與 Power Cycle 後是否保留？ || How is namespace write protection configured, and which modes survive reset or power cycling?','feature',['nwp','idctrl'],'''
防止 namespace 被修改，並區分可解除、直到斷電及永久三種保護生命週期。 || Prevent namespace modification with reversible, until-power-cycle and permanent protection lifetimes.
保護屬於 namespace，其他可存取該 namespace 的 controller 也必須遵守；不只是這條 queue 的軟體旗標。 || Protection belongs to the namespace and applies through other controllers accessing it, not just one queue's software flag.
Identify.NWPC 是能力；WPC 的 WPUPCC／PWPC 是允許進入特定模式的控制；Get FID84h.WPS 才是目前狀態。 || NWPC advertises capability, WPC.WPUPCC/PWPC permits entering specific modes and Get FID84h.WPS reports current state.
WPS=0 無保護、1 基本保護、2 到 Power Cycle、3 永久。此 Feature 不可保存、沒有 Default，不能用 SV=1 製造持續性。 || WPS0/1/2/3 means none/basic/until-power-cycle/permanent. This feature is unsaveable and has no Default; SV=1 does not create persistence.
查能力與進入許可，針對 NSID Set WPS，再 Get Current；進入保護時 controller 須將該 namespace 的 volatile data／metadata 提交到非揮發媒體。 || Check support/entry permission, Set WPS for NSID and read Current. Entering protection commits that namespace's volatile data/metadata to nonvolatile media.
成功後被禁止的操作須依寫保護規則拒絕；一般 Read 仍以可讀狀態處理。不能只看到 Set 成功就省略行為核對。 || After success, prohibited operations must obey protection rules while ordinary reads remain governed by readable state. Verify behavior in addition to Set success.
試圖改變 WPS2／3、缺許可位或 multi-domain 禁止的 WPS2 轉換：Feature Not Changeable（1/0Eh）；Get Default：0/02h；受禁止的命令可回 Namespace is Write Protected（0/20h）。 || Changing WPS2/3, missing entry permission or prohibited multi-domain WPS2 transition uses1/0Eh; Get Default uses0/02h; prohibited commands may return Namespace is Write Protected0/20h.
CHANG=1 不表示進入永久保護後能解除。WPC 控制位重設與 namespace 已存在的 WPS 狀態是不同事情。 || CHANG=1 does not promise reversal of permanent protection. Reset of WPC permission bits differs from the namespace's existing WPS state.
先讀 Current.WPS 與 WPC，確認是能力不支援、進入不允許，還是已處在不可改狀態。 || First read Current.WPS and WPC to separate missing support, denied entry and an already unchangeable state.
''',{12:'Controller Reset 保留既有 WPS，包括 Until Power Cycle；不會因 FID84h 不可保存就解除保護。 || Controller Reset preserves existing WPS, including Until Power Cycle; unsaveability does not remove protection.',13:'NVM Subsystem Reset 不等於 Power Cycle，WPS 依狀態機持續；不能用 NSSR 當解除 Until Power Cycle 的方法。 || NVM Subsystem Reset is not a power cycle; WPS follows its state machine. NSSR is not a method to remove Until Power Cycle protection.',14:'實際 Power Cycle 後，WPS2 回 No Write Protect；基本 WPS1 與永久 WPS3 持續。永久保護不能用一般 Set／Reset 解開。 || An actual power cycle returns WPS2 to No Write Protect; basic WPS1 and permanent WPS3 persist. Ordinary Set/reset cannot remove permanent protection.'})

add(66,'Set Features 成功後，為什麼還應使用 Get Features 確認？ || Why read Get Features after a successful Set Features?','feature',['getfeat','setfeat','setcomplete','keepalive','number'],'''
確認實際使用的值和 Host 要求的值之間是否有規範允許的轉換，並避免只看成功碼。 || Verify transformations between the requested and effective value rather than relying only on success status.
同一 FID、scope、selector 與操作時期才可比較；Get Supported Capabilities 不等於 Get Current。 || Compare identical FID/scope/selectors and time; Supported Capabilities is not Current.
先知道 Feature 的回覆格式與支援能力；某些值在 CQE，某些在 data buffer，某些兩處都有。 || Know the response format and support; values may be in CQE, a payload or both.
保存原 Set 的 SV／參數、Set CQE 結果，Get SEL0 讀 Current，必要時 SEL2 讀 Saved。 || Preserve original SV/parameters and Set results, read Current with SEL0 and Saved with SEL2 when needed.
等 Set 成功完成再 Get；避免另一個 Host 同時修改共用 scope。動態值如 Timestamp 以合理經過時間比較，不要求逐 bit 相同。 || Await successful Set before Get and coordinate concurrent shared-scope writers. Compare dynamic values such as Timestamp with elapsed time rather than byte equality.
成功 Set 的 CQE 不得早於屬性設定完成；KATO 可能向上取整，Number of Queues 回實際配置，這些不同於原請求不一定是錯。 || Successful Set completion cannot precede completion of attribute setting. Rounded KATO and allocated queue counts may validly differ from requests.
若後續 Get 失敗，它有自己的 Status，不能將它覆蓋原 Set 結果；先檢查 selector、scope 和中間 reset。 || A later Get failure has its own status and does not replace the Set result. Check selectors, scope and intervening reset.
Get 證明可讀到設定，行為驗證另證明功能採用它；兩者都需要，但不用重複把相同數值測成多個題目。 || Readback establishes reported configuration; behavioral checks establish its use. Both are needed, without duplicating the same comparison as separate tests.
先核對 SEL 是否為 Current，以及 Set 與 Get 之間是否有 reset／其他 Set。 || First confirm SEL=Current and no intervening reset or other Set.
''')

add(67,'Firmware Activation、Namespace 刪除、Controller Reset 及 Power Cycle 後，Feature 應如何變化？ || How should features change after activation, namespace deletion, reset and power cycling?','feature',['feature','setfeat','timestamp','hmb','nwp','nsmanage'],'''
按事件與 Feature 的個別規則建立持續性預期，避免一律判「都清除」或「都保留」。 || Establish persistence expectations per event and feature instead of assuming universal clearing or retention.
先分 controller、namespace 與共享管理物件 scope，再分 Current／Saved／Default。 || Separate controller, namespace and shared-object scope, then Current/Saved/Default.
查 SEL3.SVBL、Figure466 或 NVM Figure92，再看該 FID 的特殊規定；不可保存與不可持續不是同義詞。 || Check SVBL, Figure466/NVM Figure92 and feature-specific exceptions. Unsaveable and nonpersistent are not synonyms.
記錄事件是否真的造成 CLR、是否含整個 subsystem；Namespace Delete 移除的是該物件，不能將同號新 NSID 當成原設定的自然延續。 || Record actual CLR occurrence and coverage. Namespace deletion removes an object; a new namespace reusing its number is not automatically the same configured object.
保存前快照→執行已定義事件→恢復管理通道→讀 Current／Saved／能力→驗行為；對 Firmware Activation 先確認它採用哪種啟用與 Reset 路徑。 || Snapshot, perform the defined event, restore management access, reread values/capabilities and verify behavior. For activation, identify its actual activation/reset path.
例：SV=0 的可保存 Feature 可在重設後回較舊 Saved；HMB 需重配；WPS2 撐過 Controller Reset 卻在 Power Cycle 解除。 || An SV=0 change to a saveable feature can revert to older Saved after reset; HMB needs reconfiguration; WPS2 survives Controller Reset but ends at a power cycle.
物件已刪後的 Get／Set 依該 FID 與 NSID 規則回應；不能因無法讀舊 NSID 的 Feature 就判保存失敗。 || Access after object deletion follows that FID's NSID rules; failure to read a deleted namespace is not evidence of failed saving.
對比前後要保留 namespace 身分、SV、scope、重設原因與發生時間，不只一欄「Feature 值不同」。 || Preserve object identity, SV, scope, reset cause and timing, not merely a changed-value flag.
先確認測到的是同一物件，以及事件是否真的觸發預期的重設範圍。 || First confirm the same object and the actual reset coverage.
''')

add(68,'Feature 宣告支援但 Get、Set 或實際功能行為不一致時，應如何驗證？ || How should supported-feature claims be checked when Get, Set and behavior appear inconsistent?','feature',['feature','getfeat','setfeat','setcomplete','irqfeat','effects'],'''
用可重現的最小條件找出矛盾屬於能力、設定、觀察方式還是韌體行為。 || Isolate whether the contradiction lies in capability, configuration, observation or firmware behavior under reproducible conditions.
鎖定同一 controller、FID、NSID／其他 selector 與配置時期，防止跨 scope 的數值混用。 || Fix controller, FID, NSID/other selectors and configuration interval to avoid mixing scopes.
對照 Identify、Feature Supported and Effects、SEL3 能力；NSSPEC=0 不一定 controller scope，CHANG=1 不一定任何時候可改。 || Compare Identify, feature-effects information and SEL3. NSSPEC=0 is not necessarily controller scope; CHANG=1 is not unconditional changeability.
保存原 Set、Get 的 FID／SEL／SV／CDW11／buffer 與 CQE，並記下開始驗行為前有哪些命令已 outstanding。 || Preserve FID/SEL/SV/CDW11/payloads and CQEs, and identify commands already outstanding before behavioral checks.
能力查詢→合法 Set→等完成→Get Current→提交新命令驗效果；再單獨驗 Saved 與 reset。一次只改一個因素。 || Discover, legally Set, await completion, Get Current and submit new affected work; test saving/reset separately, changing one factor at a time.
一致結果須符合規範允許範圍：KATO 取整、動態 Timestamp、implementation-specific interrupt coalescing 都不能用「不等於請求」直接判錯。 || Consistency means conformance to allowed outcomes. Rounded KATO, dynamic Timestamp and implementation-specific coalescing cannot be rejected simply for differing from a request.
不支援 FID=0/02h、SV 錯=1/0Dh、不可改=1/0Eh、scope 錯=1/0Fh 先各自排除；多錯誤共存時保留規範允許的選擇。 || First distinguish unsupported FID0/02h, unsaveable1/0Dh, unchangeable1/0Eh and wrong-scope1/0Fh; retain allowed status choices for multiple faults.
不合規結論應附一條明確要求、成立的前提、原始命令與回覆，以及能排除 selector／時序誤用的證據。 || A noncompliance finding should include the explicit requirement, established prerequisites, raw request/response and evidence excluding selector/timing misuse.
先查 Get 是否讀了錯誤 SEL／NSID，或測行為的命令其實在 Set 成功前已提交。 || First check wrong SEL/NSID or behavioral test commands submitted before Set completed.
''')
