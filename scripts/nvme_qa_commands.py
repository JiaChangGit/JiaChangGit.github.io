from scripts.nvme_qa_model import add

add(31,'一筆 NVMe Command 的 Opcode、CID、NSID、Data Pointer 及 Command Dword 各有什麼用途？ || What do Opcode, CID, NSID, Data Pointer and command dwords mean?','queue',['sqe','idctrl'],'''
把「做什麼、對誰做、資料在哪、用哪些參數」編成 controller 可以讀取的命令。 || Encode the operation, target, data location and parameters into a command the controller can read.
Opcode 的意義先由 Admin／I/O command set 決定；相同數值放在不同命令集不一定是相同操作。 || Opcode interpretation depends on the Admin/I/O command set; equal numeric values need not mean the same operation across sets.
先查對應能力，如 OACS、ONCS、SGLS，並核對 namespace 的 CSI；不是所有命令都使用全部公共欄位。 || Check capabilities such as OACS, ONCS and SGLS and the namespace CSI. Not every command uses every common field.
CDW0 含 OPC、FUSE、PSDT、CID；NSID 選目標；MPTR／DPTR 描述資料；CDW10～15 由各命令定義。Common command 是 64 bytes。 || CDW0 contains OPC, FUSE, PSDT and CID. NSID selects the target, MPTR/DPTR describe data, and CDW10–15 are command-specific. The common command is 64 bytes.
選 command set→查 Opcode 與能力→設定合法 NSID／參數→準備資料與指標→分配同 SQ 唯一 CID→提交。PCIe Admin 使用 PRP，不能任意改用 SGL。 || Select command set, opcode/support, legal NSID/parameters, data/pointers and a unique outstanding CID, then submit. PCIe Admin commands use PRPs, not arbitrary SGLs.
完成由 SQID+CID 對回；真正的資料或結果可能在 Host buffer 或 CQE DW0／1，不是全部塞在 Status。 || Match completion by SQID+CID. Results may reside in the host buffer or CQE DW0/1, not solely Status.
不支援 opcode 為 Invalid Command Opcode（0/01h）；非法已定義欄位通常是 Invalid Field（0/02h），有專用錯誤則用其定義。 || Unsupported opcode uses Invalid Command Opcode (0/01h). Invalid defined fields generally use Invalid Field (0/02h), subject to specific error definitions.
核對 Opcode 所屬 command set、宣告能力與 payload 長度；DPTR 位址合法也不保證描述的資料長度足夠。 || Cross-check command-set context, support and payload size. A valid DPTR address does not prove sufficient described data length.
先確認 SQ 是 Admin 還是 I/O，以及使用哪份命令集解碼。 || First identify whether the SQ is Admin or I/O and which command set decodes it.
''')

add(32,'Reserved 欄位非零、不合法 Command Dword 組合或不支援 Opcode 應如何處理？ || How are nonzero reserved fields, illegal field combinations and unsupported opcodes handled?','queue',['conventions','sqe','status'],'''
分清 reserved bits 與已定義欄位中的 reserved coded value，避免錯誤地要求所有保留位都必須被檢查。 || Distinguish reserved bits from reserved coded values in defined fields; not every reserved bit requires receiver validation.
涉及 Host 建構命令的義務與 controller 的檢查義務，兩者不是同一句規定。 || Host construction requirements and controller validation requirements are separate.
查 Base §1.4.1 的 reserved 定義、Opcode 支援與每個命令的欄位限制。 || Use Base §1.4.1 reserved semantics, opcode support and the individual command's field restrictions.
Host 須將 reserved 欄位清零；接收端不必檢查 reserved bits／bytes／fields。已定義欄位收到 reserved 編碼則須報錯。 || The host shall zero reserved fields; the recipient need not check reserved bits/bytes/fields. A reserved coded value in a defined command field shall be reported as an error.
先建立全零 SQE，再填使用欄位；學習錯誤處理時一次只改一項，並記錄該要求是 shall 還是 should。 || Start from a zeroed SQE and populate used fields. Change one item per error exercise and record whether the requirement says shall or should.
合法組合依命令正常完成；controller 沒檢查某 reserved bit 不代表 Host 寫非零就合法。 || A legal combination follows normal completion. Lack of reserved-bit checking does not make a nonzero host value legal.
未支援或 reserved opcode：0/01h。定義欄位非法值：一般 0/02h，除非明定專用 Status。多錯誤並存通常可選其中一種；不把 reserved bit 非零一律判為必須 0/02h。 || Unsupported/reserved opcode: 0/01h. Illegal defined field: generally 0/02h unless a specific status applies. Multiple faults usually permit choosing one; nonzero reserved bits do not universally mandate 0/02h.
測試報告應同時列 Host 是否違規、controller 是否有義務偵測；這樣才不會把合法的未檢查行為判成韌體 bug。 || Record both host violation and controller detection obligations to avoid labeling permitted nonchecking as a firmware bug.
先問改到的是「保留位」還是「已定義欄位中的保留編碼」。 || First ask whether the modified item is a reserved bit or a reserved encoding within a defined field.
''')

add(33,'NSID 不存在、Inactive、不適用或錯誤使用 Broadcast NSID 時，應回傳什麼類型的 Status？ || Which statuses apply to invalid, inactive, unused and improperly broadcast NSIDs?','queue',['sqe','nsid','feature'],'''
避免把不存在、未附加與命令根本不用 NSID 混成同一種錯誤。 || Separate invalid identity, inactive namespace and a command that does not use NSID.
NSID 的 active 狀態是相對某 controller；另一條路徑可用不代表這個 controller 也可用。 || Active state is controller-relative. Accessibility through another path does not establish activity on this controller.
用 Active／Allocated namespace lists 及 command 的 NSID 使用規則判斷；再查命令有沒有例外。 || Use active/allocated lists and the command's NSID rules, then check command-specific exceptions.
NSID=0、有效 allocated NSID、inactive NSID 與 FFFFFFFFh 必須分開解讀；FFFFFFFFh 的範圍由每條命令定義。 || Distinguish zero, valid allocated, inactive and FFFFFFFFh identifiers. Each command defines the scope of FFFFFFFFh.
先確認命令是否用 NSID，再確認命令是否允許該 namespace 狀態與 broadcast。Identify 某些 CNS 本來就是查 allocated/inactive，不能套用一般 I/O 假設。 || Determine whether NSID is used, then permitted namespace state and broadcast support. Some Identify CNS values intentionally query allocated/inactive namespaces.
合法目標依命令完成；某些查詢對不存在或 inactive 的回覆有特別規定，不能只套總表。 || Legal targets follow the command's completion rules. Some queries define special replies for absent/inactive objects that override the generic rule.
Figure 93 的預設：使用 NSID 的命令遇 inactive 回 Invalid Field（0/02h），invalid 回 Invalid Namespace or Format（0/0Bh）；不支援 broadcast 卻用 FFFFFFFFh，或不用 NSID 卻填非零，回 0/02h。命令例外優先。 || Figure 93 defaults: inactive on an NSID-using command returns 0/02h, invalid returns 0/0Bh. Unsupported broadcast or nonzero NSID on an unused field returns 0/02h. Command-specific exceptions take precedence.
將原 SQE 的 NSID、當時 active list、CNS／FID／Opcode 規則一起核對；不要只用現在的清單解釋過去命令。 || Correlate the original NSID, the list at that time and CNS/FID/opcode rules. A current list alone may not explain a past request.
先查命令是否真的屬於 Figure 93 的一般情況，或已有明確例外。 || First check whether the command uses the generic rule or defines an explicit exception.
''')

add(34,'CQE 中的 SQHD、SQID、CID、Phase Tag 及 Status 分別有什麼用途？ || What are SQHD, SQID, CID, phase and status used for in a CQE?','queue',['cqe','queue'],'''
一筆 CQE 同時提供命令結果、原命令身分與 queue 進度；這些欄位不能彼此代替。 || A CQE carries command result, identity and queue progress; these fields are not interchangeable.
SQHD 屬於 CQE.SQID 指定的 SQ；P 屬於 CQ slot；Status 屬於 SQID+CID 指定的命令。 || SQHD describes the identified SQ, P the CQ slot, and Status the command identified by SQID+CID.
使用當前 queue 配置與 CQE 的公共格式，不是由某個 Feature 選擇 SQHD 意義。 || Interpret using current queue configuration and the common CQE layout, not a feature-selected meaning of SQHD.
DW2：SQHD、SQID；DW3：CID、P、Status；DW0／1 是命令特定結果。SQHD 表示建立 CQE 當時已消費的位置。 || DW2 contains SQHD/SQID; DW3 contains CID/P/Status; DW0/1 carry command-specific results. SQHD reports consumption when that CQE was constructed.
先以 P 驗有效性，再對 SQID+CID、解析 Status 與結果，更新 SQ 可用 slots，最後釋放 CQ slot。 || Validate P, match SQID+CID, decode status/results, update SQ slot availability and finally release the CQ slot.
例：一筆 completion 報 SQHD=8，表示 Head 已前進到 8，不表示 slots 0～7 的所有命令已執行完成。 || SQHD=8 reports head advancement to eight; it does not establish execution completion of every command from slots zero through seven.
Status 需同讀 SCT、SC；P 不屬錯誤碼。CQE 格式錯誤或未知 CID 先檢查記憶體／lifetime，不替它編造一個新的 NVMe Status。 || Decode SCT and SC together; P is not an error code. Malformed CQEs or unknown CIDs require checking memory/lifetimes, not inventing a new NVMe status.
SQHD 進度、命令完成與資料 buffer 可回收的時機分開核對；可重用 SQ slot 不代表可提前釋放該命令資料。 || Distinguish SQ consumption, command completion and data-buffer reclamation. Reusable SQ slots do not permit early release of command data.
先確認是新的 P，再解釋其他欄位；順序反過來容易將舊記憶體當錯誤完成。 || First establish a new phase before interpreting the remaining fields, avoiding stale-memory completions.
''')

add(35,'Status Code Type 與 Status Code 應如何解析？ || How should Status Code Type and Status Code be decoded?','queue',['status','cqe'],'''
同一個 SC 數值在不同 SCT 有不同意義，必須用成對值判讀。 || The same SC can mean different things under different SCTs; decode the pair.
Status 屬於這筆完成，還要搭配 Opcode、command set 與錯誤發生條件。 || Status belongs to this completion and must be interpreted with opcode, command set and failure conditions.
公共 SCT／SC 定義在 Base；NVM 特定狀態再看 NVM Command Set，不能用不同 command set 的表解釋。 || Base defines common SCT/SC values; use NVM definitions for its specific codes, not another command set's table.
在 CQE DW3 中 SCT=bits27:25、SC=24:17，P=16；若程式先取最後 16-bit word，SCT 位置變為 11:9、SC 為 8:1。 || In CQE DW3, SCT is bits27:25, SC bits24:17 and P bit16. In the final 16-bit word, SCT occupies bits11:9 and SC bits8:1.
先確認資料寬度與 endian，再抽 SCT／SC，選正確表，最後讀 DNR、More、CRD 與命令特定結果。 || Confirm data width/endianness, extract SCT/SC, select the correct table, then inspect DNR, More, CRD and command-specific results.
SCT=0、SC=00h 表示 Successful Completion；SQID／CID 與 P 仍須正確，不能只看到低位元全零就認定這是新成功完成。 || SCT=0, SC=00h means Successful Completion, but matching and phase still matter; zero low bits alone do not establish a new valid success.
例：0/01h 是 Invalid Command Opcode；1/01h 是 Invalid Queue Identifier。SCT=2 為 Media and Data Integrity，3 為 Path Related，7 為 Vendor Specific。 || For example, 0/01h is Invalid Command Opcode and 1/01h Invalid Queue Identifier. SCT2 is Media/Data Integrity, SCT3 Path Related and SCT7 Vendor Specific.
保留原始 CQE bytes 與解碼值；不同工具若移除 P 或重新打包 Status，輸出的整數不能直接逐值比較。 || Preserve raw CQE bytes and decoded values. Tools that remove P or repack status cannot have their integers compared blindly.
先檢查是否漏移除 Phase 或把 DW3 位元位置套到 16-bit Status word。 || First check accidental inclusion of P or use of DW3 bit positions on a 16-bit status word.
''')

add(36,'More 與 Do Not Retry 位元分別代表什麼？DNR 為 0 是否代表一定能直接重試？ || What do More and DNR mean, and does DNR=0 guarantee an immediate safe retry?','queue',['status','error','behavior','fatal'],'''
把「可能重試成功」「是否有補充錯誤資訊」與「重試是否安全」分開。 || Separate potential retry success, additional error information and retry safety.
判讀同一筆 CQE；DNR 的相同命令重試語意涵蓋同一 NVM subsystem 的任何 controller。 || Decode the same CQE; DNR's identical-command retry semantics cover any controller in the same subsystem.
公共位元固定存在；CRD 的使用還需 Host Behavior Support.ACRE 與 Identify.CRDT1～3。 || The common bits always exist; CRD use additionally depends on Host Behavior Support.ACRE and Identify.CRDT1–3.
DNR 不表示資料一定沒改；More=1 表示 LID 01h 有此命令的更多 Status 資訊，不是「還有另一筆 completion」。 || DNR does not establish that data was unchanged. More=1 points to additional status in LID01h, not another completion.
先解析錯誤原因；若 DNR=0，修正暫時條件並依有效 CRD 等待，再判斷是否能安全重送。對非冪等操作，還要確認先前作業是否已生效。 || Decode the cause; with DNR=0, address transient conditions, respect valid CRD guidance and assess retry safety. For non-idempotent work, determine whether the earlier operation took effect.
重試成功須看新 CQE。DNR=0 只說 may succeed，不保證立即成功，也不保證重送不會造成重複作用。 || Only the new CQE establishes retry success. DNR=0 means may succeed, not immediate or duplicate-free success.
不變參數的非法命令重送未必有用；明定 DNR 的 Status 按其規則，例如 Command Interrupted（0/21h）要求 DNR=0，且需 ACRE 啟用才可回報。 || Repeating unchanged invalid parameters is not useful. Apply explicit DNR rules: Command Interrupted (0/21h) requires DNR=0 and may be returned only with ACRE enabled.
More=1 與 Error Information 中可關聯的額外資訊應一致；CRD 必須依 DNR／ACRE 決定是否有意義。 || More=1 must correspond to associated additional Error Information. Interpret CRD only when DNR/ACRE make it applicable.
先檢查錯誤是已明確完成，還是只有 Host timeout；沒有 CQE 時根本沒有可讀的 DNR。 || First distinguish an actual error completion from a host timeout; without a CQE there is no DNR to interpret.
''')

add(37,'Completion 已寫入但 Host 未處理，可能與 Phase Tag、CQ 位置或 Interrupt 有什麼關係？ || Why might a posted completion remain unprocessed by the host?','queue',['cqe','pcie','irq','irqfeat'],'''
將 controller 已張貼完成與 Host 已收到通知／已消費完成分成不同階段。 || Separate completion posting, notification delivery and host consumption.
涉及目標 CQ 的記憶體、Host Head／expected Phase 與 CQ 關聯中斷，未必是命令執行失敗。 || This involves CQ memory, host Head/expected phase and interrupt routing, not necessarily execution failure.
確認 Create CQ.IEN／IV、使用的 MSI 或 MSI-X 模式、mask 與中斷 Feature。 || Check Create CQ.IEN/IV, the selected MSI/MSI-X mode, masks and interrupt features.
MSI-X 檢查 Function Mask、vector mask／PBA；一般 MSI 的 INTMS／INTMC 規則不同。CQE 有效性仍以正確位置與 Phase 判斷。 || For MSI-X inspect Function Mask, vector mask and PBA; ordinary MSI uses different INTMS/INTMC rules. CQE validity still depends on location and phase.
先驗 Host 正在讀正確 CQ Head，再驗 P；有新 CQE 則處理。沒有中斷時再檢查 IEN、IV、mask、coalescing 與 Host handler。 || Inspect the correct CQ Head and phase first. Process valid CQEs; investigate missing interrupts through IEN, IV, masks, coalescing and the host handler.
可輪詢處理一筆合法完成，即使它沒有一對一中斷。中斷數不必等於 completion 數。 || Polling can consume a valid completion without a one-to-one interrupt. Interrupt count need not equal completion count.
「沒收到中斷」本身沒有 NVMe error Status；原 CQE 甚至可能是成功。不要因此憑空回 Internal Error。 || Missing an interrupt does not itself carry an NVMe error status; the CQE may be successful. Do not invent Internal Error for it.
比較 CQE 張貼、mask 改變、中斷到達與 Head 更新時間；IRQ 是通知，不是完成內容本身。 || Compare posting, masking, interrupt delivery and Head-update times. An IRQ is notification, not the completion payload itself.
先檢查 Host 是否讀錯 CQ／slot 或 expected Phase；這比先猜中斷遺失更直接。 || First check CQ/slot selection and expected phase before assuming interrupt loss.
''')

add(38,'多個 Command 同時 Outstanding 時，Controller 是否必須按照提交順序完成？ || Must outstanding commands complete in submission order?','queue',['order','nvmatomic'],'''
理解 queue 保存提交順序，不等於所有命令具備執行或完成的先後保證。 || Understand that queued submission order is not a universal execution/completion-order guarantee.
一般獨立命令即使在同一 SQ，也不能假設 FIFO completion；跨 SQ 更不能靠相近提交時間建立依賴。 || Independent commands need not complete FIFO even within one SQ; nearby submission times across SQs do not establish dependency.
先看命令是否屬 fused operation 或有專屬順序規則；FUSES 表示 fused 支援。 || Check for a fused operation or command-specific ordering rule; FUSES advertises fused support.
需要分開 submitted、consumed、processing、completed 四個階段；SQHD 只反映其中的 consumed。 || Distinguish submitted, consumed, processing and completed stages. SQHD only reports consumption.
若 B 依賴 A 的結果，Host 等 A 成功完成後再提交 B；若需要媒體持久性，另套 Flush／FUA，不能只靠順序。 || If B depends on A, wait for A's successful completion before submitting B. Apply Flush/FUA separately for persistence.
沒有依賴的 Read B 先於 Read A 完成可以合法；Host 必須按 SQID／CID 分派，而不是按送出陣列順序。 || Independent Read B may legally complete before Read A; match by SQID/CID rather than submission-array order.
單純反序完成沒有錯誤 Status。若違反明定多命令序列，才依該序列專用錯誤判斷。 || Out-of-order completion alone has no error status. Violations of defined multicommand sequences follow their own errors.
測試需要驗命令要求的因果關係，不能用「看起來沒照順序」當唯一不合規證據。 || Test required causal relations rather than treating apparent reordering alone as noncompliance.
先問兩筆命令有沒有規範明定或 Host 主動建立的相依關係。 || First identify a specification-defined or host-established dependency.
''')

add(39,'哪些 Command 具有順序相依性？Host 為什麼不能假設所有 Command 都依序完成？ || Which commands have ordering dependencies, and why is universal ordered completion unsafe to assume?','queue',['order','create','delete','setfeat','nvmatomic'],'''
把真正的相依序列明確建立，避免把一般 queue 排隊當成交易機制。 || Explicitly establish real dependencies instead of treating queuing as a transaction mechanism.
典型例子：CQ→SQ 建立、SQ→CQ 刪除、Set Features 成功→受新值影響的新命令，以及支援的 fused pair。 || Examples include CQ-before-SQ creation, SQ-before-CQ deletion, successful Set Features before affected new commands, and supported fused pairs.
查 FUSES、所選 Feature 與各命令規則；不是用一個全域「按順序」能力位解決所有情況。 || Check FUSES and individual feature/command rules; no global ordered-mode bit resolves every case.
FUSE=01b／10b 表示成對第一／第二筆；PCIe 中必須在同一 SQ 相鄰並用同一次 Tail 更新提交。 || FUSE=01b/10b marks the first/second command. In PCIe they must be adjacent in one SQ and submitted by one Tail update.
一般依賴用等待 completion 建立；fused pair 依其專用規則一同提交，兩筆各有 CQE。不要把兩筆同時提交後再猜 controller 會替 Host 排好。 || Establish ordinary dependencies by waiting for completion; submit fused pairs under their special rules with separate CQEs. Do not assume the controller orders arbitrary concurrent requests for the host.
Set Features 成功後才提交的命令使用新設定；早已提交的命令可能使用舊或新設定。需要一致測試時先排空。 || Commands submitted after successful Set Features use the new value; previously submitted ones may use old or new settings. Drain first when testing a clean transition.
缺少相鄰 fused partner：Command Aborted due to Missing Fused Command（0/0Ah）；CQ/SQ 相依錯誤按 Create／Delete 專用 Status，不一律 0/0Ch。 || A missing adjacent fused partner uses 0/0Ah. Queue dependency errors use Create/Delete-specific statuses, not universally 0/0Ch.
畫出各 completion 與下一次 submission 的邊界；FUA 控制持久性，不會代替這些相依關係。 || Trace completion-to-submission boundaries. FUA controls persistence, not these dependencies.
先檢查 Host 是否真的等待前一步成功，而非只等待提交函式返回。 || First check whether the host waited for successful completion rather than merely submission-function return.
''')

add(40,'Outstanding Command 達到限制或 CQ Full 時，Controller 如何限制取得新 Command？ || How do outstanding limits and CQ Full constrain further command handling?','queue',['queue','order','cqe'],'''
區分 Host 的可提交容量、controller 內部執行資源與 CQ 可張貼容量，避免用單一 queue depth 解釋全部停滯。 || Separate host submission capacity, internal execution resources and completion capacity instead of using one queue-depth value to explain every stall.
限制可針對 SQ、共享 CQ 或 controller 內部資源；不是每個限制都代表整個 controller 失效。 || Limits may affect an SQ, shared CQ or internal resources; not every limit is controller-wide failure.
Host 依 queue size／SQHD 保留空間與唯一 CID；不要把其他 transport 的 MAXCMD 流量控制假設直接套到 PCIe。 || The host uses queue size/SQHD and unique CIDs. Do not import another transport's MAXCMD flow-control assumptions into PCIe.
內部取得已提交 SQE 的算法是 vendor specific；仲裁決定從哪條 SQ 開始處理 candidate commands。取得與開始執行也不同。 || Fetching submitted SQEs uses a vendor-specific algorithm; arbitration selects where candidate processing starts. Fetch and execution start are distinct.
Host 不覆寫未消費 SQE；controller 不向滿 CQ 張貼，必要時停止處理相關 SQ 的更多命令，獨立 SQ 仍繼續。 || The host must not overwrite unconsumed SQEs; the controller must not post into a full CQ and may pause related further processing while independent SQs continue.
容量釋放後可正常前進；SQ slot 已釋放但命令仍 outstanding 是可能的，因為取得不等於完成。 || Progress resumes as capacity becomes available. A freed SQ slot can belong to a still-outstanding command because consumption is not completion.
到達正常資源限制不自动要求錯誤 CQE；違反 queue 指標、重用 CID 或超過特定命令限制時才按各自規則回應。 || Normal resource limits do not automatically require error CQEs; pointer misuse, CID reuse and command-specific limits have separate rules.
以不同階段的證據核對，不可只觀察 Host submission count 就宣告 controller 已同時執行全部命令。 || Use evidence for each stage; submitted count does not establish simultaneous execution of every command.
先辨認滿的是 SQ、CQ，還是僅 Host 的 outstanding 配額。 || First determine whether the SQ, CQ or only the host outstanding limit is full.
''')

add(41,'Round Robin 與 Weighted Round Robin Arbitration 有什麼差異？ || How do Round Robin and Weighted Round Robin arbitration differ?','feature',['order','arbit','cap','create'],'''
決定多條 SQ 都有可處理工作時，下一批從哪條開始，並允許 Host 表達服務優先級。 || Select which SQ starts the next batch when several contain eligible work, allowing host service priorities.
仲裁控制開始處理 candidate commands 的選擇，不保證 completion 順序或固定 IOPS 比例。 || Arbitration governs candidate processing starts, not completion order or a fixed IOPS ratio.
所有 controller 支援 Round Robin；選配 WRR 看 CAP.AMS，再用 CC.AMS 選擇。 || All controllers support Round Robin. Discover optional WRR via CAP.AMS and select it with CC.AMS.
FID 01h 提供 Arbitration Burst（AB）及 HPW／MPW／LPW；SQ.QPRIO 在 WRR 生效。AB=7 表示不限 burst，其他值為 2^AB；權重為欄位值+1。 || FID01h provides AB and HPW/MPW/LPW; QPRIO applies in WRR. AB=7 means unlimited burst, otherwise 2^AB; weights encode value+1.
Disable 時選 CC.AMS；Enable 後設定 FID 01h，建立 SQ 的 QPRIO，再以持續可執行的工作觀察選擇行為。 || Select CC.AMS while disabled, set FID01h after enabling, create SQ priorities and observe under continuously eligible workloads.
RR 對含 Admin 的 SQ 平等輪流；WRR 先 Admin，再 Urgent，再依權重分配 High／Medium／Low，類別內還有輪流規則。 || RR gives all SQs, including Admin, equal round-robin priority. WRR prioritizes Admin, then Urgent, then weighted High/Medium/Low service with within-class rules.
不支援 CC.AMS 的 Register 設定是 undefined，不是 Set Features 的 Invalid Field。FID 01h 非法已定義參數則按命令規則。 || Unsupported CC.AMS programming is undefined, not a Set Features Invalid Field completion. Invalid defined FID01h parameters follow command rules.
Get FID 01h 讀回只是設定證據；執行時間、媒體衝突與 CQ 壓力也影響量測吞吐，不能只拿 IOPS 比值判斷 WRR。 || Get FID01h verifies configuration only. Service time, media contention and CQ pressure affect throughput, so IOPS ratios alone cannot validate WRR.
先看 CC.AMS 是否真的選 WRR，再解讀 QPRIO 與權重。 || First confirm CC.AMS actually selects WRR before interpreting priorities and weights.
''')

add(42,'Urgent、High、Medium 及 Low Queue Priority 在哪些情況下生效？ || When do Urgent, High, Medium and Low queue priorities take effect?','feature',['order','create','arbit'],'''
讓不同 SQ 取得不同服務機會，但只有選用對應仲裁機制時才有意義。 || Give SQs different service opportunities only under the applicable arbitration mechanism.
QPRIO 是 SQ 層級設定，不是每筆 Read／Write 的 priority 欄位。 || QPRIO is an SQ-level setting, not a per-Read/Write priority field.
CAP.AMS 支援 WRR 且 CC.AMS 已選 WRR 才使用 QPRIO；否則 controller 必須忽略它。 || QPRIO is used only when WRR is supported and selected through CC.AMS; otherwise it shall be ignored.
Create SQ CDW11.QPRIO：00b Urgent、01b High、10b Medium、11b Low；FID 01h 為後三種設定權重。 || Create SQ CDW11.QPRIO encodes Urgent00b, High01b, Medium10b and Low11b; FID01h weights the latter three.
依工作類型建立 SQ 並設 QPRIO；想改既有 SQ 屬性，須按 queue 重建流程，不是改 Host 記憶體中的舊 Create SQE。 || Create SQs with suitable QPRIO. Change an existing queue through reconstruction, not by editing an old Create SQE in host memory.
Urgent 高於加權類別但低於 Admin；連續 Urgent 工作可能讓較低類別飢餓，不能期待 High 永遠有固定最低頻寬。 || Urgent outranks weighted service but remains below Admin. Persistent Urgent work may starve lower classes; High has no universal fixed minimum bandwidth.
在 RR 模式下 QPRIO 被忽略是合法行為，不應回報「優先級功能失效」；非法 queue 參數仍按 Create Status。 || Ignoring QPRIO under RR is correct, not a failed priority feature. Invalid queue parameters still follow Create statuses.
將每條 SQ 的 QPRIO、CC.AMS 與 FID 01h 一起保存；缺任一項都不足以解釋優先行為。 || Preserve each SQ's QPRIO, CC.AMS and FID01h together; none alone explains priority behavior.
先排除其實正在用 RR 的情況。 || First rule out operation under RR.
''')

add(43,'多個 Queue 競爭資源時，如何判斷 Arbitration 是否符合設定？ || How can arbitration be evaluated when multiple queues compete?','feature',['order','arbit','create'],'''
把規範對 candidate 選擇的要求轉成可判讀證據，避免把延遲或吞吐差異直接當成仲裁違規。 || Translate candidate-selection requirements into evidence rather than equating latency or throughput differences with arbitration violations.
觀察同一 controller 的競爭 SQ；先排除 CQ Full、命令依賴、不同服務成本與 Host 供應不足。 || Observe competing SQs on one controller after excluding CQ Full, dependencies, unequal service costs and insufficient offered work.
記錄 CAP.AMS、CC.AMS、FID 01h 的 AB／權重及每條 SQ 的 QPRIO。 || Record CAP.AMS, CC.AMS, FID01h AB/weights and each SQ's QPRIO.
WRR 高／中／低每輪能開始處理的數量受剩餘 credits 與 AB 限制；需要知道是否有 ready candidate，不只 SQ 是否非空。 || In WRR, processing starts per round are limited by remaining credits and AB. Ready candidates matter, not merely a nonempty SQ.
用相近命令類型與大小、持續供應且 CQ 不阻塞的教學情境；比較可觀測的開始處理或排程紀錄，只有 CQE 時需承認無法還原全部內部選擇。 || Use comparable commands, sustained supply and nonblocking CQs. Compare processing-start/scheduler evidence where available; CQEs alone cannot reconstruct all internal choices.
例如 High／Low 權重 4:1 指服務 credits，不能要求每個短時間窗口都剛好完成 4:1。 || High/Low weights of 4:1 describe service credits, not an exact completion ratio in every short interval.
Arbitration 量測本身没有錯誤 CQE；先驗設定命令成功，再對照規範的 shall／may。供應條件不成立時，不宜判不合規。 || Measurement itself has no error CQE. Verify configuration success and distinguish shall/may requirements; unsuitable workload conditions do not establish noncompliance.
要判違規，需指出哪一條明定選擇規則與哪段證據矛盾，而不是只有「高優先比較慢」。 || A noncompliance claim needs a contradiction between a defined selection rule and evidence, not merely slower high-priority work.
先檢查高優先 SQ 是否真的持續有可開始處理的 candidate，並確認 CQ 沒滿。 || First verify continuously eligible high-priority candidates and available CQ space.
''')
