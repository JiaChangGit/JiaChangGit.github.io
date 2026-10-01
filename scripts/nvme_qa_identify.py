from scripts.nvme_qa_model import add

add(44,'Identify Controller 與 Identify Namespace 分別提供哪些重要資訊？ || What important information is provided by Identify Controller and Identify Namespace?','identify',['idcmd','idctrl','idns','idlist'],'''
Identify Controller 用來了解 controller 支援哪些能力；Identify Namespace 則用來了解指定 namespace 的容量、格式及資料保護設定。先分清楚查詢對象，才知道該讀哪一組欄位。 || Separate controller capability from a particular namespace's capacity, format and protection configuration.
Identify Controller 以接收命令的 controller 為查詢入口。Namespace 資料則要搭配 NSID、CNS 及 CSI，確認要查的是哪個 namespace，以及哪一種資料結構。 || Controller data describes the receiving controller's view; NSID/CNS/CSI select namespace information.
基本查詢入口是 CNS01h 的 Controller 資料，以及 CNS00h 的 NVM Namespace 資料。CNS05h／06h 查詢命令集特定的補充結構，CNS08h 則提供不依賴特定命令集的 Namespace 資料。 || Main entry points are CNS01h Controller and CNS00h NVM Namespace; CNS05h/06h are command-set specific, while CNS08h is command-set independent Namespace data.
Controller 看 SN、MN、FR、MDTS、OACS、ONCS、LPA、SQES／CQES；NVM Namespace 看 NSZE／NCAP／NUSE、FLBAS／LBAF、MC／DPC／DPS、原子性及群組識別。 || Controller fields include SN/MN/FR, MDTS, OACS/ONCS, LPA and SQES/CQES. NVM Namespace includes NSZE/NCAP/NUSE, FLBAS/LBAF, MC/DPC/DPS, atomicity and group identifiers.
先查 Controller 資料及 Active Namespace ID List，再逐一查詢各 namespace 適用的資料結構。計算容量時，使用目前選定的 LBA format，將 block 數換算成 bytes。 || Read Controller and the active list, then the applicable structures for each namespace. Convert block counts using the currently selected LBA format.
Identify 回傳 4096-byte 結構與成功 CQE。例：NSZE=8192、LBADS=12，邏輯位址空間為 8192×4096=32 MiB。 || Identify returns a 4096-byte structure and successful CQE. NSZE=8192 and LBADS=12 describe 32 MiB of logical address space.
不支援 CNS 時，回報 Invalid Field（0/02h）；namespace 所屬命令集不支援該 CNS 時，回報 Invalid I/O Command Set（1/2Ch）。至於 NSID 是否合法，則依該 CNS 的使用規則判斷。 || Unsupported CNS uses Invalid Field (0/02h); an incompatible namespace command set uses Invalid I/O Command Set (1/2Ch). Apply CNS-specific NSID rules.
controller 宣告支援某個命令，不代表每個 namespace 都具備適合的格式，或目前都能由此 controller 存取。因此，驗證時必須同時確認 controller 能力與目標 namespace 的條件。 || Controller opcode support does not make every namespace format or current state suitable; both levels must permit the operation.
先確認 buffer 是由哪個 CNS 回傳，再使用對應的結構解碼。例如，不能將 CNS08h 的回傳資料當成 CNS00h 的格式讀取。 || First identify the returned CNS structure; do not decode CNS08h with the CNS00h layout.
''')

add(45,'Active Namespace ID List、Allocated Namespace ID List 及 Namespace Descriptor List 有什麼差異？ || How do active, allocated and namespace descriptor lists differ?','identify',['idlist','nsid'],'''
這三種查詢分別回答：哪些 namespace 可由此 controller 使用、哪些 namespace 已經配置，以及某個 namespace 有哪些識別資料。它們不是同一份清單的不同名稱。 || Separate accessibility through this controller, allocation/existence and the identity of one namespace.
Active List 反映此 controller 可使用的 namespace；Allocated List 可以包含已配置但尚未附加的 namespace。Descriptor List 則不是 namespace 名單，而是單一 NSID 的識別屬性集合。 || The active list is controller-relative; the allocated list can include unattached namespaces; descriptors describe one NSID.
CNS02h 查詢 Active List，CNS10h 查詢 Allocated List，CNS03h 查詢 Namespace Identification Descriptor List。使用 Allocated List 查詢前，還要確認 Namespace Management 支援能力。 || CNS02h queries active IDs, CNS10h allocated IDs and CNS03h namespace identification descriptors. Allocation queries depend on Namespace Management support.
查詢 ID List 時，NSID 是分頁的起點，回傳清單列出大於該起點的 ID。Descriptor 則透過 NIDT、NIDL、NID 描述識別資料，例如 EUI64、NGUID、UUID 或 CSI；它不是用來列出其他 namespace。 || List NSID is a pagination cursor returning greater IDs. Descriptors contain NIDT/NIDL/NID for identifiers such as EUI64, NGUID, UUID and CSI.
讀取 ID List 時，先以 NSID=0 查詢，再依回傳的遞增 ID 繼續讀取下一批。查詢 Descriptor List 時，NSID 改為指定要查的 namespace。因此，同一個 NSID 欄位在這兩類查詢中的用途不同。 || Start list enumeration at NSID=0 and continue from returned IDs; for a descriptor query NSID selects the target, not a cursor.
例如 Allocated={1,3,8}，而 Active={1,8}，表示 namespace 3 已配置，但目前不在此 controller 的 Active List 中。這個差異本身不代表 namespace 3 已損壞。 || Allocated={1,3,8} and Active={1,8} mean namespace3 is allocated but not active here, not necessarily damaged.
CNS02h 或 CNS10h 若將起點設為 FFFFFFFEh 或 FFFFFFFFh，必須回報 Invalid Namespace or Format（0/0Bh）。若問題是 controller 不支援所選 CNS，則回報 0/02h。 || CNS02h/10h cursors FFFFFFFEh or FFFFFFFFh shall return Invalid Namespace or Format (0/0Bh); unsupported CNS uses 0/02h.
跨時間比對 namespace 時，使用 Descriptor 提供的穩定識別資料，不要假設 NSID 永遠不變。如果分頁讀取期間發生配置變更，則需重新取得彼此一致的清單內容。 || Correlate stable descriptor identifiers rather than assuming NSIDs never change. Restart enumeration when configuration changes compromise a consistent view.
先確認 NSID 在此次命令中代表目標，還是「從這個 ID 之後開始列」。 || First determine whether NSID is a target or a start-after cursor.
''')

add(46,'Controller List、UUID List 及 I/O Command Set Identify 資料分別有什麼用途？ || What are Controller Lists, the UUID List and I/O Command Set Identify data used for?','identify',['idlist','idcmd','uuid','profile'],'''
這些資料分別回答三個問題：哪些 controller 與 namespace 有存取關係、應使用哪一套廠商定義解讀資料，以及哪些 I/O command sets 可以同時使用。 || Answer three different questions: which controllers can access, which vendor definition to use and which command sets can operate together.
Controller List 描述 controller 的名單或附加關係。UUID List 則讓 Host 選擇廠商特定資料所使用的定義；它與 namespace 自身的 UUID Descriptor 是不同資訊。 || Controller Lists describe relationships. The UUID List selects vendor-specific information and is not the namespace UUID descriptor.
CNS12h 查某 namespace 附加的 controllers，13h 查 subsystem I/O controllers，17h 查 UUID List，1Ch 查 command-set combinations。 || CNS12h lists controllers attached to a namespace, 13h subsystem I/O controllers, 17h the UUID List and 1Ch command-set combinations.
CNTID 的用途取決於 CNS，可能是清單的查詢起點，也可能指定目標 controller。UIDX=0 表示不指定 UUID。CNS1Ch 回傳的每個 vector，則表示一組可同時使用的 CSI。 || CNTID is a list cursor or CNS-specific target; UIDX=0 selects no UUID. Each CNS1Ch vector describes a simultaneously supported set combination.
先依查詢目的選擇 CNS，再設定它使用的選擇欄位。若從 CNS1Ch 選定一組命令集組合，設定 FID19h 時，IOCSCI 要填該組合的索引，不能直接填入 CSI bitmap。 || Select CNS and selectors for the question. After CNS1Ch discovery, FID19h.IOCSCI selects the combination index, not the CSI bitmap itself.
Controller List 回傳 controller 識別值及數量；UUID List 回傳依規定順序排列的 entries；命令集組合 vectors 則列出 Host 可選的配置。查到某個組合，不表示它已自動啟用。 || Lists return identities/counts or UUID entries; command-set vectors advertise available combinations without automatically enabling them.
不支援 CNS 時，回報 0/02h；CNS12h 使用 NSID=FFFFFFFFh 時，也回報 0/02h。UUID 選擇錯誤則依 §8.1.31 判斷，不能一律解釋為 namespace 不存在。 || Unsupported CNS and CNS12h NSID=FFFFFFFFh use 0/02h. Illegal UUID selection follows §8.1.31, not namespace-absence rules.
先核對 CNTID 與 NSID 在所選 CNS 中各自的用途，不要把 Controller List 當成 Active Namespace ID List。設定命令集組合後，另以 FID19h 的 Current 值確認是否選到預期的 vector。 || Keep CNTID and NSID roles separate and verify that FID19h Current selects the intended vector.
先確認 UIDX 填的是 UUID List 的索引。它不是 UUID 本身，也不是 namespace ID。 || First confirm that UIDX is a UUID List index, not the UUID value or an NSID.
''')

add(47,'NVM Set、Endurance Group、Domain 及 Secondary Controller 資訊應從哪種 Identify 資料取得？ || Which Identify structures describe NVM Sets, Endurance Groups, Domains and Secondary Controllers?','identify',['idlist','virtual','idctrl','idns'],'''
這些 Identify 資料用來建立資源歸屬關係。NVM Set、Endurance Group、Domain 與 controller 分別描述不同的管理對象，不能當成同一層的物件。 || Establish resource membership instead of treating sets, groups, domains and controllers as interchangeable objects.
每種清單都有自己的 ID、容量或資源欄位。本題著重查明它們的關係與屬性，不涉及修改容量配置或虛擬化資源。 || Each list has its own IDs and capacity/resource fields. This question discovers information rather than changing capacity or virtualization state.
先查 CTRATT 的相關能力與 OACS.VMS；CNS04h、19h、18h、14h／15h 分別對應 Set、Endurance Group、Domain、Primary／Secondary Controller。 || Check relevant CTRATT capabilities and OACS.VMS. CNS04h,19h,18h and14h/15h describe sets, endurance groups, domains and primary/secondary controllers respectively.
NVM Set Attributes 透過 ENDGID 表示所屬 Endurance Group；Namespace 資料則提供 NVMSETID 與 ENDGID。Domain entry 的 DID、TDC、UDC 用來描述識別及容量；Secondary Controller entry 的 SCID、PCID、狀態及 VQ／VI 數量，則用來描述 controller 關係與資源。 || Set attributes include ENDGID; namespace data includes NVMSETID/ENDGID; domain entries include DID/TDC/UDC; secondary entries include SCID/PCID, state and VQ/VI counts.
先由 namespace 的群組識別資料，查出對應的 NVM Set 與 Endurance Group。再利用 Domain List 確認容量歸屬，並透過 Primary Controller Capabilities 及 Secondary Controller List，了解 queue 與 interrupt 資源的配置。 || Trace namespace membership through sets/groups, domain capacity and primary/secondary resource information for allocated queues and interrupts.
成功查詢後，應取得能互相對應的 ID 與屬性。但欄位為零不一定表示資源數量為零；必須先確認相關能力受支援，而且這個欄位在目前配置下有效。 || Results provide related IDs/attributes. A zero field is not always a zero resource count; first establish support and field validity.
不支援的 CNS 回報 0/02h。某些清單查詢若將起點設在目前最大 ID 之後，則會回傳空清單；不能只因沒有 entry，就要求 controller 回報錯誤。 || Unsupported CNS uses 0/02h; cursors beyond existing IDs may return empty lists rather than errors.
比對清單中的資源數、Number of Queues，以及實際可建立的 QID 與可用 IV。同時分清楚 Primary Controller 宣告的能力，與 Secondary Controller 已獲配置的資源，兩者不一定是相同數量。 || Compare resources with queue allocations, valid QIDs and vectors. Primary capacity and secondary allocations are different quantities.
先確認查詢是送到哪個 Primary Controller，再確認清單的查詢起點是否符合預期。 || First check the selected primary controller and pagination starting point.
''')

add(48,'CNS、CSI、NSID 或 UUID Index 不支援或不合法時，Controller 應如何回應？ || How should unsupported or invalid CNS, CSI, NSID and UUID Index values be handled?','identify',['idcmd','idlist','uuid','status','idns'],'''
Identify 失敗時，必須先看哪個選擇欄位不符合使用規則。CNS、CSI、NSID 與 UUID Index 的用途不同，不能將所有失敗都歸為 Invalid Namespace。 || Judge selectors by their actual roles rather than calling every Identify failure an invalid namespace.
相同的 NSID 或 CSI，用在不同 CNS 時，合法性可能不同。因此，測試某個欄位前，必須固定 CNS 及相關前提。 || The same NSID/CSI can be legal for one CNS and illegal for another; fix the CNS and prerequisites in each test.
Figure 336 指定每個 CNS 是否使用 NSID、CNTID、CSI；UIDX 使用還受 UUID 選擇能力控制。 || Figure336 specifies use of NSID/CNTID/CSI per CNS; UUID-selection capability controls UIDX use.
CNS 不使用 CNTID 時，Host 將它清零，controller 忽略它。對不使用的 CSI，規範建議 Host 清零，並建議 controller 忽略；若 Host 填入非零值，controller 也可以回報 Invalid Field。 || For unused CNTID, the host clears it and the controller ignores it. For unused CSI, the host should clear it; the controller should ignore it but may return Invalid Field if nonzero.
驗證時先固定其他選擇欄位，每次只改動待測欄位。先列出所選 CNS 的專用規則，再用通用規則補足，避免忽略例外。 || Hold other selectors constant, vary the target field and apply CNS-specific rules before generic defaults.
有效查詢回傳 4096 bytes。例如，CNS11h 對符合定義的未配置 NSID，可以回傳全零資料；這與指定無效 NSID 而回報錯誤，是不同情況。 || Valid queries return 4096 bytes. CNS11h can return zero-filled data for a defined unallocated NSID, distinct from an invalid-NSID error.
不支援 CNS 時回報 0/02h；namespace 所屬命令集不支援該 CNS 時回報 1/2Ch；CNS02h／10h 使用非法的末端起點時回報 0/0Bh。如果命令使用 UUID 選擇，而 UIDX 指向不支援該資料的 UUID、全零 UUID 或 NVMe Invalid UUID，則必須回報 0/02h。CSI 的合法性則要看該 CNS 是否使用它，以及 namespace 所屬的命令集。 || Unsupported CNS:0/02h; incompatible namespace command set:1/2Ch; prohibited terminal cursors for CNS02h/10h:0/0Bh. For UUID selection, an unsupported UUID for the requested information, an all-zero UUID or the NVMe Invalid UUID shall return 0/02h. CSI handling depends on whether the CNS uses CSI and on the namespace command set.
保留 CQE 及原命令的 CDW10、CDW11、CDW14。不同欄位錯誤都可能得到 0/02h，只有 Status 數值不足以指出是哪個參數造成失敗。 || Preserve CQE with CDW10/11/14; different selectors can produce the same 0/02h.
先確認這個 CNS 是否使用待測欄位。若規範要求或允許忽略該欄位，controller 沒有因它報錯，就不能直接判為漏做檢查。 || First check whether the CNS uses that selector. Ignoring an unused field is not automatically a validation omission.
''')

add(49,'Serial Number、Model Number、Firmware Revision、MDTS 及 Optional Admin Command 欄位應如何解讀？ || How are SN, MN, FR, MDTS and optional Admin capability fields interpreted?','identify',['idctrl','cap','conventions'],'''
Identify Controller 同時包含識別字串、傳輸限制及能力 bitmap。這些欄位的資料型態不同，必須各自解讀，不能全部當成一般整數。 || One large Identify structure combines identity strings, transfer limits and capability bitmaps, requiring different interpretation methods.
SN 與 MN 識別 NVM subsystem，FR 描述目前啟用的韌體版本。MDTS 限制單次資料傳輸大小，OACS 則宣告選配 Admin 功能的支援能力。 || SN/MN identify the subsystem, FR the active firmware, MDTS a transfer limit and OACS optional Admin capabilities.
CNS01h：SN bytes23:4、MN63:24、FR71:64、MDTS byte77、OACS bytes257:256。 || In CNS01h: SN bytes23:4, MN63:24, FR71:64, MDTS byte77 and OACS bytes257:256.
識別字串依 ASCII 解讀，並注意尾端的空白填補。MDTS 非零時，傳輸上限為 2^MDTS×2^(12+CAP.MPSMIN) bytes；計算使用 CAP.MPSMIN，不是 CC.MPS。MDTS=0 只表示此欄位不設定上限，命令本身仍可能有其他長度限制。 || Decode ASCII strings and space padding. Nonzero MDTS limits bytes to 2^MDTS×2^(12+CAP.MPSMIN), not CC.MPS. MDTS=0 removes this limit, not all command-specific limits.
先確認回傳結構及欄位位置，再依資料型態分別讀取字串、能力位及指數編碼。計算傳輸長度時，另查 CTRATT.MEM，確認 metadata 是否計入限制。 || Confirm layout/offsets, then decode strings, bits and exponents separately. Check CTRATT.MEM when accounting for metadata in transfer length.
例如 MPSMIN=0、MDTS=5，傳輸上限為 128 KiB。若 MEM=0，傳送 32 個 4096-byte 資料區塊時，還要計入每塊 16-byte 的 metadata；加總後就超過 128 KiB。 || MPSMIN=0 and MDTS=5 give 128 KiB. With MEM=0, 32 blocks of4096-byte data plus16-byte metadata per block exceed it.
超過 MDTS 的命令回報 Invalid Field（0/02h）；不支援的選配 Opcode 通常回報 0/01h。NVMe 版本較新，不代表所有選配命令都必須支援。 || Exceeding MDTS returns Invalid Field (0/02h). Unsupported optional opcodes generally use 0/01h; a recent revision does not require all options.
將 FR 與 Firmware Slot Information 中目前 active slot 的版本比對，不要誤拿尚待啟用的 slot 比較。OACS 宣告的能力，則應與 Commands Supported and Effects Log 中對應命令的支援欄位一致。 || Compare FR with the currently active firmware slot, not a pending slot; cross-check OACS with corresponding command-support entries.
先檢查是否把 MDTS 的編碼直接當成 byte 數，或誤用目前的 CC.MPS 來計算傳輸上限。 || First check whether MDTS was treated as a byte count or multiplied by the wrong page size.
''')

add(50,'Identify 宣告支援某功能後，應如何透過對應 Command 及 Commands Supported and Effects Log 驗證？ || How can advertised Identify support be cross-checked against commands and the Commands Supported and Effects Log?','identify',['effects','idctrl','idcmd'],'''
驗證能力時，要確認 Host 能在合法條件下使用該功能，不能只確認 Identify 的支援位為 1，就認定功能已驗證完成。 || Connect an advertised bit to a legal operation instead of validating the bit alone.
查詢與測試應針對同一 controller、命令集及 namespace 配置，並注意資料取得的時間。不同配置或不同時點的結果，不能直接當成同一狀態比較。 || Compare the same controller, command set, namespace configuration and time.
先查 Identify 的功能支援欄位，再確認 LPA.CELP。接著從 LID05h 選出正確的 Admin 或 I/O Opcode entry，讀取 CSUPP 與命令效果欄位。 || Check Identify support, LPA.CELP and the correct Admin/I/O opcode's CSUPP and effects in LID05h.
除了 CSUPP，還要讀取 LBCC、NCC、NIC、CCC、CSE 等欄位。它們用來說明命令可能如何影響資料、能力與 namespace 清單，以及執行時有哪些限制。 || Read CSUPP together with LBCC, NCC, NIC, CCC and CSE to understand data/capability/list changes and execution restrictions.
先確認合法前提與支援能力，準備好參數及資源，再執行命令。完成後檢查 CQE 與實際結果，並依 effects 欄位指出的變更，重新查詢可能受影響的資訊。 || Establish legal prerequisites, discover support, prepare valid parameters/resources, execute, verify result and rediscover information affected by the command.
宣告支援表示這項功能有合法的使用方式，不表示任何參數或任何狀態下都會成功。驗證成功時，也不能只看 CQE，還要確認命令產生了規範要求的效果。 || Support means a legal supported operation exists, not that every parameter/state succeeds. Completion must also match the command's defined effect.
若回報 0/01h，可能與 Opcode 支援宣告矛盾。但若回報 0/02h、Namespace Not Ready，或受到 Lockdown 限制，則應先查參數與目前狀態，不能立即判定支援宣告錯誤。 || 0/01h may contradict opcode support, but Invalid Field, Namespace Not Ready or Lockdown first require checking parameters and state.
Commands Supported and Effects Log 描述命令支援能力及可能影響，不是執行歷史。某個 entry 宣告命令受支援，不表示這條命令最近曾經執行過。 || Commands Supported and Effects describes capability/effects, not recent execution history.
先檢查拿的是 Admin 還是 I/O opcode entry，以及 CSI 是否選對。 || First check Admin versus I/O entry selection and CSI.
''')

add(51,'Namespace 建立、刪除、Attach、Detach 或 Format 後，哪些 Identify 資料與 Namespace List 應更新？ || Which Identify data and lists change after namespace creation, deletion, attachment, detachment or format?','identify',['idlist','idns','nsmanage','effects'],'''
namespace 配置改變後，Host 必須重新取得受影響的資訊，才能避免沿用舊容量、舊格式或舊的附加關係。 || Connect configuration changes to rediscovery instead of continuing with stale capacity, format or attachment data.
Create／Delete 改變 namespace 是否存在；Attach／Detach 改變 controller 是否能使用它；Format 則改變操作範圍內的資料格式。不同操作需要檢查的資料也不同。 || Create/Delete change existence, Attach/Detach controller accessibility, and Format the data format within its defined scope.
OACS.NMS 確認管理支援；Format 還看 OACS／FNA 及 NVM 支援格式。 || OACS.NMS advertises namespace management; Format also uses OACS/FNA and NVM format support.
分別檢查 Allocated List、Active List、CNS12h 回傳的已附加 Controller List，以及 Namespace 資料中的 FLBAS、DPS、NSZE、NCAP 等欄位，不要期待每種操作都改變相同欄位。 || Separately inspect allocated/active lists, CNS12h attached controllers and namespace format/capacity fields such as FLBAS/DPS/NSZE/NCAP.
先記錄操作前的資料，等待管理命令完成，再重新查詢受影響的清單及 namespace。尤其 Create 成功只表示 namespace 已建立，不表示它已自動附加到 controller。 || Capture before-state, wait for management completion, then reread affected lists/namespace data. Successful Create does not automatically attach the namespace.
Create 後，namespace 應出現在 Allocated List；Attach 後，應出現在目標 controller 的 Active List。Detach 後，它會從該 Active List 移除，但仍可能留在 Allocated List。Format 後則要檢查選定格式是否正確，不能假設 NSID 必須改變。 || Create adds to Allocated; Attach adds to the target Active list; Detach removes from that Active list without necessarily deallocating; Format updates the selected format rather than necessarily changing NSID.
管理命令失敗時，不能直接假設所有資料都已更新，也不能假設完全沒有變動。先查該命令對失敗及部分完成的規則，再重新查詢實際狀態。 || A failed management command does not universally imply either every change occurred or none occurred; examine its failure/partial-operation rules and rediscover.
將管理命令結果、相關清單、Namespace 資料結構，以及適用的 Changed Namespace 通知一起比對。事件用來通知變更，不能代替 Identify 所提供的完整配置資料。 || Correlate management results, lists, namespace data and applicable Changed Namespace notification. The event is not a full replacement for Identify configuration data.
先確認查詢送到的是受 Attach／Detach 影響的 controller，並確認前一筆管理命令已經完成，再解讀查詢結果。 || First verify the affected controller and completion of the preceding management command.
''',{9:'若操作符合 Namespace Attribute Changed 等事件條件，依 OAES、通知設定、事件遮蔽與 pending Request 回報。不能要求每次 Identify 查詢都產生事件；觸發原因是前面的配置變更。 || Qualifying namespace changes use OAES, notification configuration, masking and pending-request rules. Identify queries do not themselves generate these events; the preceding configuration change does.',11:'若支援 PEL 且操作符合 Change Namespace 或 Format 事件條件，按對應事件記錄；這是管理操作的歷史，不是後續 Identify 查詢的歷史。 || Supported PEL records qualifying Change Namespace or Format events under their definitions. These describe management operations, not subsequent Identify queries.'})

add(52,'Firmware Activation、Reset 及 Power Cycle 後，哪些 Identify 資料可能改變，哪些應保持不變？ || Which Identify data may change after firmware activation, reset or power cycling?','identify',['idctrl','identity','idns','reset','effects'],'''
是否允許 Identify 資料改變，要逐欄依性質判斷。不能將整個 4096-byte buffer 一律要求完全相同，因為其中包含動態狀態及可能更新的能力。 || Judge change by field semantics instead of requiring the whole 4096-byte buffer to remain identical.
可先分成固定身分、韌體宣告能力、持續配置與動態狀態四類。這四類資料允許改變的原因不同，因此比較時也要使用不同的判斷條件。 || Separate stable identity, firmware-advertised capability, persistent configuration and dynamic state.
保存 SN／MN、namespace 穩定識別、FR、能力位、容量／格式／附加關係及動態欄位作比較基準。 || Preserve identity, namespace stable identifiers, FR, capabilities, capacity/format/attachments and dynamic fields as separate comparison groups.
FR 應描述目前已啟用的韌體；韌體更新後，MDTS 及能力位需要重新確認。NUSE 等動態數值則可能隨使用狀態改變，不能拿來當固定的裝置識別資料。 || FR describes active firmware. Rediscover MDTS/capabilities after an update; dynamic fields such as NUSE are not fixed identities.
先記錄發生了哪些操作：只有 Reset 或 Power Cycle，還是同時有韌體啟用或管理配置變更。恢復後，使用相同的 CNS、NSID、CSI 查詢，再逐欄對照其保留及變更規則。 || Record whether reset/power cycling also activated firmware or changed configuration. Reread with identical selectors and compare by field definition.
一般 Reset 並不是重新命名裝置、刪除 namespace 或執行 Format。如果重設同時啟用了新韌體，則 FR 及規範允許隨之變更的能力，不能一律要求保留舊值。 || Ordinary reset is not a rename, namespace deletion or format operation. Concurrent firmware activation can change FR and legitimately change advertised capabilities.
比較前後資料本身不會產生新的 CQE Status。如果重設後 Identify 失敗，應先分辨是初始化尚未完成、NSID 無效，還是 CNS 選錯，不能把所有差異都直接歸為韌體錯誤。 || Comparison has no new status. For failed post-reset Identify distinguish incomplete initialization, invalid NSID and wrong CNS before attributing every difference to firmware.
先用穩定識別資料確認比較的是同一物件，並保留原始 bytes。再分別處理填補空白、Reserved 欄位、動態值及真正有意義的屬性變更，避免只做逐 byte 比較就下結論。 || Confirm object identity with stable IDs. Preserve raw bytes while separating padding, reserved/dynamic fields and meaningful changes.
先確認這次 Reset 是否同時啟用了待啟用的韌體，或查詢是否實際送到另一個 controller／namespace。 || First check concurrent pending firmware activation and accidental selection of another controller/namespace.
''')

add(53,'Identify、Feature、Log Page 與實際 Command 行為不一致時，應如何定位問題？ || How should inconsistencies among Identify, features, logs and command behavior be investigated?','identify',['idcmd','effects','feature','getfeat','error'],'''
判定不一致時，要把能力、設定、當下狀態及命令結果連起來檢查。不能只因某個介面顯示支援，就忽略實際使用所需的其他條件。 || Build a complete evidence chain instead of letting one advertised capability override current conditions.
比對前，先固定 controller、NSID、CSI、時間及配置。來自不同 controller 或不同時點的資料，可能本來就在描述不同狀態。 || Hold controller, NSID, CSI, time and configuration constant; different views/times need not describe the same state.
Identify 描述能力與屬性；Get Features 查詢設定；Log Page 則依種類提供狀態、事件或命令效果。三者用途不同，數值不相同本身不代表矛盾。 || Identify discovers capability, Get Features configuration, and logs state/events or effect declarations. Their roles differ.
保留原 SQE、CQE、Identify 原始 buffer，以及 Get Features 使用的 SEL、Get Log Page 使用的 LID 和其他選擇欄位。尤其要分清楚讀到的是 Current 值，還是 Supported Capabilities。 || Preserve SQE/CQE, raw Identify, Feature SEL and log selectors. Distinguish Current from Supported Capabilities.
先確認規格版本與解碼方式，再檢查操作範圍及選擇欄位。接著確認參數合法、目前狀態允許執行，而且先後順序正確，最後才判斷結果。若仍有矛盾，可用每次只改一項條件的情境重現。 || Check revision/decoding, scope/selectors, legal parameters, current state/order and result; isolate one variable when reproducing.
一致是指各介面符合規範定義的關係，不是回傳值必須全部相同。例如 CHANG=1 表示 Feature 可變更，Current=0 表示目前設定為 0，兩者可以同時正確。 || Consistency means the specified relationships hold, not equal numeric values. CHANG=1 and Current=0 can both be correct.
先依原命令的 SCT／SC 決定下一步；More=1 時，再查可與命令關聯的 Error Information。如果只有 Host timeout 而沒有 CQE，則先追查命令是否提交及完成，不能直接套用某個 Status 的處理方式。 || Use original SCT/SC for next steps and associated Error Information when More=1. A host timeout without status first requires locating the submission/completion stage.
只有確認必要前提成立、資料來自同一物件，而且時間順序一致後，結果仍違反明確規定，才能提出可驗證的不符合規範結論。 || A defensible noncompliance conclusion requires fixed prerequisites, object and timing, plus a remaining contradiction with an explicit requirement.
第一步先確認這些資料是否來自同一 controller／namespace、同一設定期間，並且使用相同或互相對應的選擇欄位。 || First verify that all evidence describes the same controller/namespace, configuration interval and selectors.
''')
