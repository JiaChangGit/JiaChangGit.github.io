from scripts.nvme_qa_model import add

add(44,'Identify Controller 與 Identify Namespace 分別提供哪些重要資訊？ || What important information is provided by Identify Controller and Identify Namespace?','identify',['idcmd','idctrl','idns','idlist'],'''
先分清 controller 能做什麼，與特定 namespace 採用什麼容量、格式和保護設定。 || Separate controller capability from a particular namespace's capacity, format and protection configuration.
Controller 資料以接收命令的 controller 為觀察入口；Namespace 資料由 NSID／CNS／CSI 指定。 || Controller data describes the receiving controller's view; NSID/CNS/CSI select namespace information.
基本入口為 CNS01h Controller、CNS00h NVM Namespace；CNS05h／06h 為 command-set specific，CNS08h 為 command-set independent Namespace。 || Main entry points are CNS01h Controller and CNS00h NVM Namespace; CNS05h/06h are command-set specific, while CNS08h is command-set independent Namespace data.
Controller 看 SN、MN、FR、MDTS、OACS、ONCS、LPA、SQES／CQES；NVM Namespace 看 NSZE／NCAP／NUSE、FLBAS／LBAF、MC／DPC／DPS、原子性及群組識別。 || Controller fields include SN/MN/FR, MDTS, OACS/ONCS, LPA and SQES/CQES. NVM Namespace includes NSZE/NCAP/NUSE, FLBAS/LBAF, MC/DPC/DPS, atomicity and group identifiers.
先查 Controller 和 active list，再逐 namespace 查適用的幾種結構；用目前選定 LBA format 將 block 數轉成 bytes。 || Read Controller and the active list, then the applicable structures for each namespace. Convert block counts using the currently selected LBA format.
Identify 回傳 4096-byte 結構與成功 CQE。例：NSZE=8192、LBADS=12，邏輯位址空間為 8192×4096=32 MiB。 || Identify returns a 4096-byte structure and successful CQE. NSZE=8192 and LBADS=12 describe 32 MiB of logical address space.
不支援 CNS：Invalid Field（0/02h）；namespace 所屬 command set 不支援該 CNS：Invalid I/O Command Set（1/2Ch）。NSID 情況依該 CNS。 || Unsupported CNS uses Invalid Field (0/02h); an incompatible namespace command set uses Invalid I/O Command Set (1/2Ch). Apply CNS-specific NSID rules.
「Controller 支援某命令」不代表每個 namespace 都有適合的格式或目前可存取；能力與 namespace 條件須相交檢查。 || Controller opcode support does not make every namespace format or current state suitable; both levels must permit the operation.
先檢查拿到哪個 CNS 的 buffer，再依那個結構解碼，避免把 CNS08h 當 CNS00h。 || First identify the returned CNS structure; do not decode CNS08h with the CNS00h layout.
''')

add(45,'Active Namespace ID List、Allocated Namespace ID List 及 Namespace Descriptor List 有什麼差異？ || How do active, allocated and namespace descriptor lists differ?','identify',['idlist','nsid'],'''
分開「可由此 controller 使用」「已配置存在」與「這個 namespace 的識別資料」。 || Separate accessibility through this controller, allocation/existence and the identity of one namespace.
Active list 是 controller 的視角；Allocated list 可包含未附加的 namespace；Descriptor list 是單一 NSID 的屬性集合。 || The active list is controller-relative; the allocated list can include unattached namespaces; descriptors describe one NSID.
CNS02h 查 Active，10h 查 Allocated，03h 查 Namespace Identification Descriptors；Allocated 查詢還依 Namespace Management 支援。 || CNS02h queries active IDs, CNS10h allocated IDs and CNS03h namespace identification descriptors. Allocation queries depend on Namespace Management support.
List 的 NSID 是分頁起點，回傳大於起點的 IDs；Descriptor 有 NIDT／NIDL／NID，描述例如 EUI64、NGUID、UUID、CSI。 || List NSID is a pagination cursor returning greater IDs. Descriptors contain NIDT/NIDL/NID for identifiers such as EUI64, NGUID, UUID and CSI.
從 NSID=0 讀起，依遞增 ID 繼續下一批；查單一 namespace 的 Descriptor 時，NSID 則是目標。不要把兩種用途混淆。 || Start list enumeration at NSID=0 and continue from returned IDs; for a descriptor query NSID selects the target, not a cursor.
例：Allocated={1,3,8}、Active={1,8}，表示 3 已配置但不在此 controller 的 active list；不是 namespace3 必然損壞。 || Allocated={1,3,8} and Active={1,8} mean namespace3 is allocated but not active here, not necessarily damaged.
CNS02h／10h 的起點 FFFFFFFEh 或 FFFFFFFFh 須回 Invalid Namespace or Format（0/0Bh）。未支援 CNS 則為 0/02h。 || CNS02h/10h cursors FFFFFFFEh or FFFFFFFFh shall return Invalid Namespace or Format (0/0Bh); unsupported CNS uses 0/02h.
用 Descriptor 的穩定識別關聯裝置，而非永遠假設 NSID 不變；分頁期間若配置改變，需重新取得一致的清單。 || Correlate stable descriptor identifiers rather than assuming NSIDs never change. Restart enumeration when configuration changes compromise a consistent view.
先確認 NSID 在此次命令中代表目標，還是「從這個 ID 之後開始列」。 || First determine whether NSID is a target or a start-after cursor.
''')

add(46,'Controller List、UUID List 及 I/O Command Set Identify 資料分別有什麼用途？ || What are Controller Lists, the UUID List and I/O Command Set Identify data used for?','identify',['idlist','idcmd','uuid','profile'],'''
回答「由哪些 controller 存取」「用哪套 vendor 定義解讀」「哪些 command sets 能同時使用」三種不同問題。 || Answer three different questions: which controllers can access, which vendor definition to use and which command sets can operate together.
Controller List 是關係清單；UUID List 是 vendor-specific 資訊的選擇表，不等於 namespace 的 UUID Descriptor。 || Controller Lists describe relationships. The UUID List selects vendor-specific information and is not the namespace UUID descriptor.
CNS12h 查某 namespace 附加的 controllers，13h 查 subsystem I/O controllers，17h 查 UUID List，1Ch 查 command-set combinations。 || CNS12h lists controllers attached to a namespace, 13h subsystem I/O controllers, 17h the UUID List and 1Ch command-set combinations.
CNTID 是 Controller List 的起點或特定 CNS 的目標；UIDX=0 不指定 UUID。CNS1Ch 的每個 vector 是一組可同時使用的 CSI。 || CNTID is a list cursor or CNS-specific target; UIDX=0 selects no UUID. Each CNS1Ch vector describes a simultaneously supported set combination.
先依問題選 CNS，再用正確 selector；CNS1Ch 選出組合後，FID19h 的 IOCSCI 使用該組合的 index，不是直接填 CSI bitmap。 || Select CNS and selectors for the question. After CNS1Ch discovery, FID19h.IOCSCI selects the combination index, not the CSI bitmap itself.
Controller List 回識別值與數量；UUID List 回有定義順序的 entries；command-set vectors 告訴 Host 可選配置，不自動啟用它們。 || Lists return identities/counts or UUID entries; command-set vectors advertise available combinations without automatically enabling them.
未支援 CNS 回 0/02h；CNS12h 的 NSID=FFFFFFFFh 回 0/02h。UUID selector 的非法狀態另依 §8.1.31，不能當成 namespace 不存在。 || Unsupported CNS and CNS12h NSID=FFFFFFFFh use 0/02h. Illegal UUID selection follows §8.1.31, not namespace-absence rules.
核對 CNTID 與 NSID 各自作用，不將 controller list 當 active namespace list；核對 FID19h Current 是否選到預期 vector。 || Keep CNTID and NSID roles separate and verify that FID19h Current selects the intended vector.
先確認 UIDX 是 UUID List 的索引，不是 UUID 本體，也不是 namespace ID。 || First confirm that UIDX is a UUID List index, not the UUID value or an NSID.
''')

add(47,'NVM Set、Endurance Group、Domain 及 Secondary Controller 資訊應從哪種 Identify 資料取得？ || Which Identify structures describe NVM Sets, Endurance Groups, Domains and Secondary Controllers?','identify',['idlist','virtual','idctrl','idns'],'''
建立資源歸屬關係，避免把 Set、Group、Domain 和 controller 當成同一層物件。 || Establish resource membership instead of treating sets, groups, domains and controllers as interchangeable objects.
每種清單有自己的 ID、容量或資源欄位；本題只探索資料，不執行容量或虛擬化修改。 || Each list has its own IDs and capacity/resource fields. This question discovers information rather than changing capacity or virtualization state.
先查 CTRATT 的相關能力與 OACS.VMS；CNS04h、19h、18h、14h／15h 分別對應 Set、Endurance Group、Domain、Primary／Secondary Controller。 || Check relevant CTRATT capabilities and OACS.VMS. CNS04h,19h,18h and14h/15h describe sets, endurance groups, domains and primary/secondary controllers respectively.
NVM Set Attributes 帶 ENDGID；Namespace 資料帶 NVMSETID／ENDGID；Domain entry 帶 DID、TDC、UDC；Secondary entry 帶 SCID、PCID、狀態與 VQ／VI 資源數。 || Set attributes include ENDGID; namespace data includes NVMSETID/ENDGID; domain entries include DID/TDC/UDC; secondary entries include SCID/PCID, state and VQ/VI counts.
從 namespace 群組識別向上查 Set／Group；以 Domain list 看容量歸屬；從 Primary capabilities 與 Secondary list 看已分配的 queue／interrupt 資源。 || Trace namespace membership through sets/groups, domain capacity and primary/secondary resource information for allocated queues and interrupts.
得到可關聯的 ID 與屬性，不是所有零欄位都代表資源數為零；須先確認該能力與欄位在此配置中有效。 || Results provide related IDs/attributes. A zero field is not always a zero resource count; first establish support and field validity.
未支援的 CNS 是 0/02h；某些清單起點超過現有 ID 會得到空清單，不能一律要求錯誤。 || Unsupported CNS uses 0/02h; cursors beyond existing IDs may return empty lists rather than errors.
比較清單的資源數與 Number of Queues、可建立 QID／可用 IV；Primary 能力與 Secondary 已配置資源不是同一個數。 || Compare resources with queue allocations, valid QIDs and vectors. Primary capacity and secondary allocations are different quantities.
先檢查查詢的是哪個 Primary controller，以及 list 的起點是否正確。 || First check the selected primary controller and pagination starting point.
''')

add(48,'CNS、CSI、NSID 或 UUID Index 不支援或不合法時，Controller 應如何回應？ || How should unsupported or invalid CNS, CSI, NSID and UUID Index values be handled?','identify',['idcmd','idlist','uuid','status','idns'],'''
依 selector 的實際用途判斷錯誤，不能把所有 Identify 失敗都寫成 Invalid Namespace。 || Judge selectors by their actual roles rather than calling every Identify failure an invalid namespace.
同一個 NSID／CSI 對不同 CNS 可以有不同合法性；測例需固定 CNS 與前提。 || The same NSID/CSI can be legal for one CNS and illegal for another; fix the CNS and prerequisites in each test.
Figure 336 指定每個 CNS 是否使用 NSID、CNTID、CSI；UIDX 使用還受 UUID 選擇能力控制。 || Figure336 specifies use of NSID/CNTID/CSI per CNS; UUID-selection capability controls UIDX use.
未使用 CNTID 時 Host 清零、controller 忽略；未使用 CSI 時 Host 應清零，controller 應忽略，但非零時也可回 Invalid Field。 || For unused CNTID, the host clears it and the controller ignores it. For unused CSI, the host should clear it; the controller should ignore it but may return Invalid Field if nonzero.
一次固定其他 selector，只改待測欄位；先寫出該 CNS 的專用規則，再用通則補足。 || Hold other selectors constant, vary the target field and apply CNS-specific rules before generic defaults.
有效查詢回 4096 bytes；例如 CNS11h 對符合定義的 unallocated NSID 可回全零，與 invalid NSID 的錯誤不同。 || Valid queries return 4096 bytes. CNS11h can return zero-filled data for a defined unallocated NSID, distinct from an invalid-NSID error.
未支援 CNS：0/02h；namespace command set 不支援該 CNS：1/2Ch；CNS02h／10h 的非法末端起點：0/0Bh。若命令使用 UUID 選擇，UIDX 指向不支援該資料的 UUID、全零 UUID 或 NVMe Invalid UUID，須回 0/02h；CSI 則依該 CNS 是否使用它及 namespace 的命令集判斷。 || Unsupported CNS:0/02h; incompatible namespace command set:1/2Ch; prohibited terminal cursors for CNS02h/10h:0/0Bh. For UUID selection, an unsupported UUID for the requested information, an all-zero UUID or the NVMe Invalid UUID shall return 0/02h. CSI handling depends on whether the CNS uses CSI and on the namespace command set.
將 CQE 與原 CDW10、11、14 一起保存；同樣的 0/02h 可由不同欄位造成。 || Preserve CQE with CDW10/11/14; different selectors can produce the same 0/02h.
先檢查這個 CNS 是否真的使用被測欄位；忽略未使用欄位不等於漏驗合法性。 || First check whether the CNS uses that selector. Ignoring an unused field is not automatically a validation omission.
''')

add(49,'Serial Number、Model Number、Firmware Revision、MDTS 及 Optional Admin Command 欄位應如何解讀？ || How are SN, MN, FR, MDTS and optional Admin capability fields interpreted?','identify',['idctrl','cap','conventions'],'''
同一張 Identify 大表同時含識別字串、傳輸限制與能力 bitmap，不能用相同數字解碼方法處理。 || One large Identify structure combines identity strings, transfer limits and capability bitmaps, requiring different interpretation methods.
SN／MN 識別 subsystem，FR 表示目前啟用韌體；MDTS 限定單次資料傳輸；OACS 表示選配 Admin 能力。 || SN/MN identify the subsystem, FR the active firmware, MDTS a transfer limit and OACS optional Admin capabilities.
CNS01h：SN bytes23:4、MN63:24、FR71:64、MDTS byte77、OACS bytes257:256。 || In CNS01h: SN bytes23:4, MN63:24, FR71:64, MDTS byte77 and OACS bytes257:256.
字串依 ASCII 與空白填補解讀；MDTS 非零時上限=2^MDTS×2^(12+CAP.MPSMIN) bytes，不是乘 CC.MPS。MDTS=0 表示此欄不設上限，仍有命令自己的限制。 || Decode ASCII strings and space padding. Nonzero MDTS limits bytes to 2^MDTS×2^(12+CAP.MPSMIN), not CC.MPS. MDTS=0 removes this limit, not all command-specific limits.
先確定結構與欄位偏移，分別抽字串／位元／指數。算資料長度時另核對 CTRATT.MEM 是否排除 metadata。 || Confirm layout/offsets, then decode strings, bits and exponents separately. Check CTRATT.MEM when accounting for metadata in transfer length.
例：MPSMIN=0、MDTS=5，限制 128 KiB；若 MEM=0，32 個 4096-byte 資料加每塊 16-byte metadata 會超過此值。 || MPSMIN=0 and MDTS=5 give 128 KiB. With MEM=0, 32 blocks of4096-byte data plus16-byte metadata per block exceed it.
超過 MDTS 的命令回 Invalid Field（0/02h）；選配 opcode 未支援通常為 0/01h，不能用「版本很新」主張必須成功。 || Exceeding MDTS returns Invalid Field (0/02h). Unsupported optional opcodes generally use 0/01h; a recent revision does not require all options.
FR 對照 Firmware Slot Information 的目前 active slot，不要拿 pending slot 比；OACS 對照相應 Commands Supported entry。 || Compare FR with the currently active firmware slot, not a pending slot; cross-check OACS with corresponding command-support entries.
先檢查 MDTS 是否被當成 bytes 或以錯誤 page size 計算。 || First check whether MDTS was treated as a byte count or multiplied by the wrong page size.
''')

add(50,'Identify 宣告支援某功能後，應如何透過對應 Command 及 Commands Supported and Effects Log 驗證？ || How can advertised Identify support be cross-checked against commands and the Commands Supported and Effects Log?','identify',['effects','idctrl','idcmd'],'''
確認能力宣告能接到合法操作，而不是只驗證 Identify 的某個 bit 為 1。 || Connect an advertised bit to a legal operation instead of validating the bit alone.
測試限定同一 controller、command set、namespace 配置與時間，避免比較不同上下文。 || Compare the same controller, command set, namespace configuration and time.
先看 Identify 的功能能力，再看 LPA.CELP 及 LID05h 中正確 Admin／I/O opcode 的 CSUPP 與 effects。 || Check Identify support, LPA.CELP and the correct Admin/I/O opcode's CSUPP and effects in LID05h.
除了 CSUPP，讀 LBCC、NCC、NIC、CCC、CSE 等欄位，確認資料、能力、清單及執行限制的可能影響。 || Read CSUPP together with LBCC, NCC, NIC, CCC and CSE to understand data/capability/list changes and execution restrictions.
建立合法前提→查支援→準備合法參數與資源→執行→驗 CQE 與結果→重新探索 effects 指出的資訊。 || Establish legal prerequisites, discover support, prepare valid parameters/resources, execute, verify result and rediscover information affected by the command.
支援代表有合法使用方式，不代表任意參數／目前狀態都會成功；完成還需達到該命令定義的效果。 || Support means a legal supported operation exists, not that every parameter/state succeeds. Completion must also match the command's defined effect.
0/01h 可能與 opcode 支援矛盾；但 0/02h、Namespace Not Ready、Lockdown 等要先核對參數及狀態，不能立刻判支援宣告錯誤。 || 0/01h may contradict opcode support, but Invalid Field, Namespace Not Ready or Lockdown first require checking parameters and state.
Commands Supported and Effects 是能力／影響描述，不是「這個命令最近執行過」的歷史紀錄。 || Commands Supported and Effects describes capability/effects, not recent execution history.
先檢查拿的是 Admin 還是 I/O opcode entry，以及 CSI 是否選對。 || First check Admin versus I/O entry selection and CSI.
''')

add(51,'Namespace 建立、刪除、Attach、Detach 或 Format 後，哪些 Identify 資料與 Namespace List 應更新？ || Which Identify data and lists change after namespace creation, deletion, attachment, detachment or format?','identify',['idlist','idns','nsmanage','effects'],'''
把配置變更連回 Host 應重新探索的資料，避免使用舊容量、格式或附加清單。 || Connect configuration changes to rediscovery instead of continuing with stale capacity, format or attachment data.
Create／Delete 改存在狀態；Attach／Detach 改 controller 可見性；Format 改該操作範圍內的資料格式。 || Create/Delete change existence, Attach/Detach controller accessibility, and Format the data format within its defined scope.
OACS.NMS 確認管理支援；Format 還看 OACS／FNA 及 NVM 支援格式。 || OACS.NMS advertises namespace management; Format also uses OACS/FNA and NVM format support.
Allocated list、Active list、CNS12h attached controller list，及 Namespace 的 FLBAS、DPS、NSZE／NCAP 等欄位分開檢查。 || Separately inspect allocated/active lists, CNS12h attached controllers and namespace format/capacity fields such as FLBAS/DPS/NSZE/NCAP.
記錄操作前快照，等管理命令完成，再查受影響清單與 namespace。Create 成功不自動等於 Attach 成功。 || Capture before-state, wait for management completion, then reread affected lists/namespace data. Successful Create does not automatically attach the namespace.
Create 後出現在 Allocated；Attach 後出現在目標 controller 的 Active；Detach 後從該 Active 移除但仍可 Allocated；Format 後檢查選定格式而非預期 NSID 必變。 || Create adds to Allocated; Attach adds to the target Active list; Detach removes from that Active list without necessarily deallocating; Format updates the selected format rather than necessarily changing NSID.
若管理命令失敗，不能一律假設全部資料已更新或全部未變；先看該命令的失敗及部分操作規則，再重新查詢。 || A failed management command does not universally imply either every change occurred or none occurred; examine its failure/partial-operation rules and rediscover.
將管理結果、清單、namespace 結構及適用的 Changed Namespace 通知核對；事件不是取代 Identify 的完整配置副本。 || Correlate management results, lists, namespace data and applicable Changed Namespace notification. The event is not a full replacement for Identify configuration data.
先確認查詢的是受 Attach／Detach 影響的 controller，並等待前一管理命令完成。 || First verify the affected controller and completion of the preceding management command.
''',{9:'若操作符合 Namespace Attribute Changed 等事件條件，依 OAES、通知設定、事件遮蔽與 pending Request 回報。不能要求每次 Identify 查詢都產生事件；觸發原因是前面的配置變更。 || Qualifying namespace changes use OAES, notification configuration, masking and pending-request rules. Identify queries do not themselves generate these events; the preceding configuration change does.',11:'若支援 PEL 且操作符合 Change Namespace 或 Format 事件條件，按對應事件記錄；這是管理操作的歷史，不是後續 Identify 查詢的歷史。 || Supported PEL records qualifying Change Namespace or Format events under their definitions. These describe management operations, not subsequent Identify queries.'})

add(52,'Firmware Activation、Reset 及 Power Cycle 後，哪些 Identify 資料可能改變，哪些應保持不變？ || Which Identify data may change after firmware activation, reset or power cycling?','identify',['idctrl','identity','idns','reset','effects'],'''
依欄位性質判斷變更，而不是把整個 4096-byte buffer 都要求完全相同。 || Judge change by field semantics instead of requiring the whole 4096-byte buffer to remain identical.
分固定身分、韌體宣告能力、持續配置與動態狀態；這四種資料有不同變更原因。 || Separate stable identity, firmware-advertised capability, persistent configuration and dynamic state.
保存 SN／MN、namespace 穩定識別、FR、能力位、容量／格式／附加關係及動態欄位作比較基準。 || Preserve identity, namespace stable identifiers, FR, capabilities, capacity/format/attachments and dynamic fields as separate comparison groups.
FR 應描述目前 active firmware；MDTS／能力需在更新後重新確認；NUSE 等動態數值不能當固定識別值。 || FR describes active firmware. Rediscover MDTS/capabilities after an update; dynamic fields such as NUSE are not fixed identities.
先記錄改變來源：只是 Reset、Power Cycle，還是同時 Activation／管理配置；恢復後用相同 CNS／NSID／CSI 讀取，再逐欄對照定義。 || Record whether reset/power cycling also activated firmware or changed configuration. Reread with identical selectors and compare by field definition.
普通 Reset 不是重新命名裝置、刪除 namespace 或 Format 的操作；但若同時啟用新韌體，FR 與其可合法變更的能力不能要求沿用舊值。 || Ordinary reset is not a rename, namespace deletion or format operation. Concurrent firmware activation can change FR and legitimately change advertised capabilities.
比較工作沒有新的 CQE Status；若 post-reset Identify 失敗，先分初始化未完成、無效 NSID 與選錯 CNS，不把全部差異定義成韌體錯誤。 || Comparison has no new status. For failed post-reset Identify distinguish incomplete initialization, invalid NSID and wrong CNS before attributing every difference to firmware.
使用 stable ID 確認比較的是同一物件；保留 raw bytes，同時把 padding、reserved、動態欄位與真正語意差異分開。 || Confirm object identity with stable IDs. Preserve raw bytes while separating padding, reserved/dynamic fields and meaningful changes.
先檢查 Reset 是否同時觸發 pending firmware activation，或查到了另一個 controller／namespace。 || First check concurrent pending firmware activation and accidental selection of another controller/namespace.
''')

add(53,'Identify、Feature、Log Page 與實際 Command 行為不一致時，應如何定位問題？ || How should inconsistencies among Identify, features, logs and command behavior be investigated?','identify',['idcmd','effects','feature','getfeat','error'],'''
用完整證據鏈判斷不一致，而不是因某個介面顯示支援就忽略當下條件。 || Build a complete evidence chain instead of letting one advertised capability override current conditions.
限定 controller、NSID、CSI、時間與配置；跨 controller 或不同時點的快照未必描述相同狀態。 || Hold controller, NSID, CSI, time and configuration constant; different views/times need not describe the same state.
Identify 查能力，Get Features 查設定，Log 查狀態／事件或效果宣告；三者用途不同。 || Identify discovers capability, Get Features configuration, and logs state/events or effect declarations. Their roles differ.
保存原 SQE、CQE、Identify 原始 buffer、FID 的 SEL 值、LID 與其他 selectors；明確區分 Current 和 Supported Capabilities。 || Preserve SQE/CQE, raw Identify, Feature SEL and log selectors. Distinguish Current from Supported Capabilities.
先檢查版本／解碼→scope／selectors→合法參數→目前狀態與先後→結果；必要時用單一控制變因的教學測例重現。 || Check revision/decoding, scope/selectors, legal parameters, current state/order and result; isolate one variable when reproducing.
一致的意思是各介面的規範關係成立，不是所有回傳值相同；例如 CHANG=1 與 Current=0 可以同時正確。 || Consistency means the specified relationships hold, not equal numeric values. CHANG=1 and Current=0 can both be correct.
原命令的 SCT／SC 決定下一步；More=1 再找可關聯的 Error Information。沒有 Status 的 Host timeout 需先定位提交／完成階段。 || Use original SCT/SC for next steps and associated Error Information when More=1. A host timeout without status first requires locating the submission/completion stage.
只有把必要前提、同一物件與時序都固定後，仍違反明确要求，才能提出可驗證的不合規結論。 || A defensible noncompliance conclusion requires fixed prerequisites, object and timing, plus a remaining contradiction with an explicit requirement.
第一個檢查是這幾份證據是否來自同一 controller／namespace、同一設定時期及相同 selector。 || First verify that all evidence describes the same controller/namespace, configuration interval and selectors.
''')
