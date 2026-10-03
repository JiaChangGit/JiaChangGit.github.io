"""Q93–106: interpreting errors without inventing universal logging rules."""
from scripts.nvme_qa_extension import question

def q(n,t,refs,b,overrides=None):
    question(n,t,'error_review',refs,b,overrides)

q(93,'Invalid Opcode、Invalid Field、CID Conflict 與 Sequence Error 如何區分？ || How do opcode, field, CID and sequence errors differ?', ['status','sqe','order'], '''
先判斷錯誤發生在哪一層，才知道要修改命令內容，還是修正 Host 的命令管理。例如 Opcode 不受支援，與同一條 SQ 重複使用尚未完成的 CID，是兩種不同問題。 || Classify the failure before changing command encoding or host bookkeeping. An unsupported opcode differs from reusing an outstanding CID in the same SQ.
Status 描述指定 SQID／CID 的完成；除非另外發現 queue 或 controller 故障，不應把單一命令的參數錯誤擴大成整個裝置失效。 || Status describes the identified command. A parameter error does not establish queue-wide or controller-wide failure.
先以 Identify 與 Commands Supported and Effects 確認 Opcode，再查該命令的欄位與順序要求。CID 是否重複，則要查看 Host 的 outstanding 清單。 || Check opcode support using Identify and Commands Supported and Effects, then command fields and sequence requirements. CID reuse requires the host outstanding list.
SCT=0：SC=01h 是 Invalid Command Opcode；02h 是 Invalid Field in Command；03h 是 Command ID Conflict；0Ch 是 Command Sequence Error。CID 的唯一性以同一條 SQ 的未完成命令為範圍。 || For SCT=0, SC01h is Invalid Command Opcode, 02h Invalid Field, 03h CID Conflict and 0Ch Command Sequence Error. CID uniqueness applies to outstanding commands within one SQ.
保留原始 SQE，確認命令集與支援能力，逐一檢查指定欄位，再重建命令先後順序。一次只改一個已確認的問題，才能知道哪項修正有效。 || Preserve the SQE, establish command set and support, inspect fields, then reconstruct sequencing. Change one identified defect at a time.
合法且成功執行的命令回成功 CQE；如果測試故意製造錯誤，正確結果則是符合該條件的錯誤完成，不能要求所有測試都回成功。 || A valid, successfully executed command returns success; a negative test passes by returning the applicable error, not by succeeding.
Invalid Field 應在沒有更明確指定 Status 時使用。若同時存在多個錯誤，除非另有優先規則，controller 可選擇其中一個；CID Conflict 的搜尋深度也是實作相關。 || Use Invalid Field unless a more specific status is specified. For multiple simultaneous faults, status selection is vendor-defined unless priority is specified; CID-conflict search depth is implementation-specific.
將支援宣告、SQE 與 CQE 對在一起。若用一筆同時有非法 Opcode、非法 NSID 的命令驗證精確 Status，測試本身就無法隔離原因。 || Correlate support, SQE and CQE. A command with both an invalid opcode and invalid NSID does not isolate an exact-status test.
先確認 CQE 屬於這次提交，而不是重用 CID 後誤配到舊完成；再查第一個違反的命令條件。 || First verify that the CQE belongs to this submission rather than an earlier reuse of its CID, then inspect the violated condition.
''')

q(94,'Namespace、Log、Queue、Queue Size 與 Interrupt Vector 錯誤如何定位？ || How are namespace, log, queue, size and vector errors located?', ['status','create','delete','getlog','nsid'], '''
這些錯誤都與識別或範圍有關，但所指的物件不同。先知道命令要查或建立哪個物件，才能判斷數值是否存在、是否有效，以及是否允許在這裡使用。 || These errors concern different identified objects. Determine what the command addresses before testing existence, range and applicability.
NSID 指 namespace，LID 指 Log 類型，QID 指 queue；QSIZE 是深度的編碼，IV 是中斷向量。它們不能因為都是數字，就共用同一套有效範圍。 || NSID, LID and QID identify different objects; QSIZE encodes depth and IV selects a vector. Their numerical ranges are unrelated.
使用 Active／Allocated Namespace List、Supported Log Pages、CAP.MQES、Number of Queues 與可用中斷資源，建立測試前的配置快照。 || Snapshot namespace lists, Supported Log Pages, CAP.MQES, Number of Queues and available interrupt resources.
常見對照為 Invalid Namespace or Format 0/0Bh、Invalid Log Page 1/09h、Invalid Queue Identifier 1/01h、Invalid Queue Size 1/02h、Invalid Interrupt Vector 1/08h；Create SQ 的無效 CQID 則有 Completion Queue Invalid 1/00h。 || Typical SCT/SC pairs are namespace 0/0Bh, log 1/09h, queue ID 1/01h, queue size 1/02h and vector 1/08h. Invalid CQID in Create SQ uses Completion Queue Invalid 1/00h.
先建立合法基準命令，再只替換目標欄位。例如測 QSIZE 超限時，應保留合法 QID、位址及 IV，避免另一個錯誤先被回報。 || Start with a valid command and alter only the tested field. A size test should keep QID, address and vector valid.
合法建立成功後，Host 才能將 queue 視為存在。錯誤測試完成後，還要確認沒有留下可使用的半完成 queue 配置。 || Only successful creation establishes a queue. After a negative test, ensure no usable partial queue configuration was left behind.
上述代碼只適用於對應命令及條件。對 Get Log 使用錯誤 NSID，可能依該 Log 的 scope 規則回 Invalid Field；不能一律要求 Invalid Namespace。 || Apply codes to their defined commands and conditions. An inappropriate NSID in Get Log may require Invalid Field under the log-scope rules, not universally Invalid Namespace.
把命令專屬完成表與當時配置共同驗證，而不是只用通用 Status 名稱比對。 || Compare the command-specific completion definition with the configuration at submission time.
先查原始欄位的編碼與單位，尤其 QSIZE 為零起算；CAP.MQES=7 表示最多 8 個 entry，不是 7 個。 || Check encoding and units first: QSIZE is zero-based, so CAP.MQES=7 permits eight entries.
''')

q(95,'Firmware、Format 與容量錯誤為何不能只看名稱？ || Why must firmware, format and capacity errors be tied to their commands?', ['status','idctrl','nsmanage'], '''
目的在區分映像、格式與資源問題，避免將不同命令回傳的「容量不足」混成同一件事。修正 slot 選擇，不會解決 namespace 配置容量不足。 || Distinguish image, format and resource problems. Correcting a firmware slot cannot fix insufficient namespace allocation capacity.
Firmware Commit 影響韌體映像與啟用安排；Format 改變目標 namespace 的格式；Namespace Management 與 Capacity Management 分別管理不同層級的容量。 || Firmware Commit concerns images and activation; Format concerns namespace format; Namespace and Capacity Management manage different resource levels.
檢查 FRMW／Firmware Slot Information、支援的 LBA formats、總容量與未配置容量，以及命令的操作範圍。 || Check FRMW, Firmware Slot Information, supported LBA formats, total/unallocated capacity and command scope.
Invalid Firmware Slot=1/06h，Invalid Firmware Image=1/07h，Invalid Format=1/0Ah。Namespace Insufficient Capacity=1/15h；Capacity Management 的 Insufficient Capacity=1/26h；一般 Capacity Exceeded=0/81h。 || Codes are firmware slot 1/06h, image 1/07h and format 1/0Ah. Namespace Insufficient Capacity is 1/15h, Capacity Management Insufficient Capacity 1/26h and generic Capacity Exceeded 0/81h.
先確認 Opcode，再讀它的錯誤條件；重算要求的 bytes、logical blocks 或配置單位。只有單位一致，要求量與可用量才有比較意義。 || Identify the opcode and its error conditions, then calculate requested bytes, logical blocks or allocation units consistently.
正向測試應得到該操作的完成結果；負向測試則確認錯誤被拒絕，且原先有效的配置仍符合該命令的失敗處理規則。 || Positive tests establish the operation’s completion; negative tests establish rejection and the command-defined disposition of existing configuration.
不要把 1/15h 與 0/81h 視為可任意替換。也不要將 Firmware Activation Requires Reset 類型的狀態直接當成映像損壞，它可能是啟用還需要另一個步驟。 || These capacity codes are not interchangeable. Firmware Activation Requires Reset can indicate an additional activation step rather than an invalid image.
比較配置前後 Identify 與 Log，並保留完整 SCT／SC；只儲存 SC 會遺失類別資訊。 || Compare pre/post Identify and logs and retain SCT with SC; SC alone loses its category.
先查失敗的是 Download、Commit、Format、Create Namespace 還是 Capacity Management，再決定要檢查的資源。 || First identify which of Download, Commit, Format, namespace creation or Capacity Management failed.
''')

q(96,'Data Transfer Error、Internal Error 與 Namespace Not Ready 有何不同？ || How do transfer, internal and namespace-readiness errors differ?', ['status','fatal','ready'], '''
三者分別指出資料傳輸、controller 內部處理及 namespace 可存取狀態。區分原因，才能選擇修正記憶體映射、處理裝置錯誤，或等待狀態改變。 || These identify data movement, internal processing and namespace accessibility, requiring different recovery actions.
Data Transfer Error 與 Internal Error 通常針對該命令；Namespace Not Ready 針對所選 namespace 的可用性。任何一項都不能單憑名稱推論全部 namespace 已毀損。 || Transfer/internal errors describe a command; readiness concerns the selected namespace. None alone proves destruction of all namespaces.
保存資料指標、Host 記憶體配置、CSTS 與 namespace 狀態，必要時讀 Error Information。Ready Mode 與 CFS 用來補足判斷，但不是同一欄位。 || Preserve pointers, host memory mappings, CSTS and namespace state; read Error Information when applicable. Ready mode and CFS provide distinct evidence.
Data Transfer Error=0/04h；Internal Error=0/06h；Namespace Not Ready=0/82h。Admin Command Media Not Ready=0/24h 另有 CRIME 與時間限制，不能和 namespace 狀態互換。 || Codes are 0/04h, 0/06h and 0/82h. Admin Command Media Not Ready, 0/24h, has separate CRIME and timing conditions.
先保存 CQE，再檢查資料位址與 buffer 使用期間；若位址正確，結合 Error Log、CSTS 及 namespace 狀態定位。失敗的 Read buffer 不應當成有效讀取結果。 || Preserve the CQE, check buffer addresses and lifetime, then logs, CSTS and namespace state. Do not treat failed-read data as a valid result.
恢復後的成功命令才提供有效結果；看到 RDY=1，只表示對應 controller ready 條件成立，不保證每個 namespace 可立即存取。 || A successful command after recovery establishes its result; RDY=1 alone does not establish immediate access to every namespace.
Namespace Not Ready 不用來取代已定義的 ANA 狀態錯誤。Internal Error 也不必然要求 CFS=1；只有更嚴重的 controller 情況才另行判定。 || Namespace Not Ready does not replace defined ANA statuses. Internal Error does not universally require CFS=1.
確認錯誤種類與證據一致：合法資料指標不排除裝置內部錯誤；namespace 暫時不可用也不表示 Opcode 不受支援。 || Valid pointers do not rule out internal errors, and temporary namespace unavailability does not imply an unsupported opcode.
先確認 CQE 指向哪筆命令，再檢查該命令的 buffer 是否在完成前被回收或改寫。 || Correlate the CQE first, then check whether its buffer was reclaimed or modified before completion.
''', {9:'Internal Error 的細節建議透過對應錯誤 AER 回報；Data Transfer Error 或 Namespace Not Ready 則不能一律要求同樣的事件。仍需區分事件發生、回報條件與是否有 AER 可用。 || Internal Error details should be reported through an appropriate error AER; transfer or readiness errors do not universally require that same event. Distinguish occurrence, reporting conditions and available requests.'})

q(97,'Power Loss、Abort、SQ Deletion 與 Fused 失敗如何反映於完成？ || How do power loss, abort, SQ deletion and fused failures appear?', ['status','abort','delete','order','reset'], '''
中止原因決定 Status，也決定 Host 能否期待 CQE。尤其突然斷電或 Reset 可能讓完成通道消失，不能要求裝置在無法通訊後仍逐筆回報。 || Abort cause determines status and whether a completion can be expected. Sudden power loss or reset can remove the completion channel.
Abort 指向一筆命令，SQ Deletion 涵蓋該 SQ 的未完成命令，Fused 失敗涉及配對操作；電源及 Reset 的範圍則可能更大。 || Abort targets one command, SQ deletion covers its outstanding commands and fused failure affects the pair; power and reset can have broader scope.
保存目標 SQID／CID、Delete 或 Abort 完成、CC／CSTS 及 FUSE 設定，才能重建真正的中止原因。 || Preserve target IDs, Abort/Delete completions, CC/CSTS and FUSE encoding to reconstruct the cause.
Power Loss Notification=0/05h；Command Abort Requested=0/07h；SQ Deletion=0/08h；Failed Fused Command=0/09h；Missing Fused Command=0/0Ah。這些是目標命令的 Status。 || Target-command codes are power-loss notification 0/05h, abort requested 0/07h, SQ deletion 0/08h, failed fused 0/09h and missing fused 0/0Ah.
先判斷 queue 是否仍有效，再讀目標完成；若已 Reset，依新生命週期重建 queue 與追蹤資料。Abort 本身的 CQE 與目標命令 CQE 要各自處理。 || Establish queue validity before consuming target completions. After reset, rebuild queues and tracking; handle Abort and target CQEs separately.
成功處理中止，並不等於目標命令回 Success。測試應驗證目標只完成一次，或在 Reset 規則下不再等待舊 queue 的完成。 || Correct cancellation does not require target success. Verify one target completion, or abandon old completion expectations under reset rules.
Power Loss Notification Status 不表示每次拔電都能留下 CQE。Fused missing 與另一筆已執行失敗也不同；應依配對、相鄰及順序條件判斷。 || A power-loss-notification status does not mean every power removal produces CQEs. A missing fused partner differs from a partner that failed.
將目標 CQE、管理命令 CQE 與 queue／電源事件按時間比對，不要只用最後讀到的一個 Status 代表整段流程。 || Correlate target, management completions and queue/power transitions by time rather than using one final status for the entire sequence.
先確認是否真的收到 Power Loss Notification，或其實是突然失去電源；這會改變對完成回報的期待。 || First distinguish an actual power-loss notification from abrupt loss of power, since completion expectations differ.
''')

q(98,'Host 如何依 Status、More、DNR 與 CRD 決定下一步？ || How do status, More, DNR and CRD guide recovery?', ['status','behavior','idctrl','fatal'], '''
復原要先找出失敗原因，再決定重試是否合理。DNR=0 只是相同命令可能成功，不代表可以忽略資料是否已部分執行，或無限立即重送。 || Diagnose before retrying. DNR=0 permits the possibility of success, not unlimited immediate retries or assumptions about partial effects.
這些欄位屬於單一命令完成；Abort、刪 queue 或 Reset 則會擴大處理範圍，應以失敗影響與通道可用性決定。 || These fields describe one completion; Abort, queue deletion and reset have broader scopes and depend on failure severity and channel availability.
用 CQE 的 SCT／SC、M、DNR、CRD，搭配 Host Behavior Support.ACRE 與 Identify.CRDT1～3。M=1 時另讀 Error Information。 || Use SCT/SC, M, DNR and CRD with ACRE and CRDT1–3; M=1 points to additional Error Information.
ACRE=1 且 DNR=0 時，CRD=1、2、3 分別選 CRDT1、2、3；CRD=0 不要求額外延遲。DNR=1 或 ACRE=0 時，CRD 為保留欄位。 || With ACRE=1 and DNR=0, CRD selects CRDT1–3 or zero extra delay. CRD is reserved when DNR=1 or ACRE=0.
先解析錯誤與補充資訊，修正非法參數或等待必要狀態，再判斷命令是否適合重試。若 queue 失效，才進入 queue 復原；Admin 通道失效則考慮 controller 復原。 || Decode the error and additional information, correct parameters or wait for state, then assess retry safety. Recover queues or the controller when their channels are compromised.
成功的復原包含有效的新結果，以及不再受舊命令後續動作影響；單純重試回 Success，仍不足以證明先前命令未重複寫入。 || Successful recovery needs a valid new result and control over old-command effects; retry success alone does not rule out duplicate writes.
Command Interrupted=0/21h 只能在 ACRE=1 時回傳，且 DNR 必須為 0。Format In Progress 也要求 DNR=0；其他錯誤不能只憑名稱自行指定 DNR。 || Command Interrupted 0/21h requires ACRE=1 and DNR=0. Format In Progress also requires DNR=0; other names do not establish a universal DNR value.
將 Host 的重試時間與 CRD／CRDT 比較；規範建議至少等待該時間，但提早重試本身不算錯誤。 || Compare retry timing with CRD/CRDT. Waiting at least the indicated delay is recommended, but an earlier retry is not itself an error.
先檢查測試是否把 DNR=0 誤寫成「必須立即重試成功」。 || First check whether the test incorrectly interprets DNR=0 as a guarantee of immediate retry success.
''')

q(99,'哪些錯誤需要 Error Information？ || Which errors require Error Information?', ['error','status','aerfull'], '''
Error Information 補充 CQE 無法容納的錯誤資訊，也能記錄不屬於特定命令的錯誤。它不是全部命令失敗的逐筆交易明細。 || Error Information extends CQEs and can describe non-command errors; it is not a mandatory transaction ledger of every failed command.
LID 01h 的範圍是 controller；entry 是否能對應命令，要看 SQID、CID 及其有效條件。 || LID01h is controller-wide; SQID/CID validity determines whether an entry is command-specific.
ELPE 決定最多 entry 數，CQE.M 表示該命令有補充資訊，Error 類型 AER 也可能引導 Host 查這份 Log。 || ELPE determines entry capacity; CQE.M identifies additional command information, and error AERs can also lead to this log.
讀 Get Log Page LID=01h，保留 ECNT、SQID、CID、STS、Parameter Error Location、NSID 與 LPVER。 || Read LID01h and retain ECNT, SQID, CID, STS, Parameter Error Location, NSID and LPVER.
收到 M=1 的錯誤完成後儘快保存 Log，並讀取足夠多 entry，避免只看最新一筆卻漏掉較早發生的目標錯誤。 || After an error with M=1, promptly preserve enough entries rather than assuming the newest entry is the target.
找到可關聯的 entry，並能以補充欄位解釋原始錯誤。若是非命令錯誤，SQID／CID=FFFFh 本身可以是正確回覆。 || Success is a correlated explanatory entry; SQID/CID=FFFFh can be correct for a non-command-specific error.
M=0 表示這筆命令沒有額外狀態資訊，不能強制每次 Invalid Field 都新增 entry。若 M=1 卻缺少資訊，仍先排除覆寫、Reset 清除及查錯 controller。 || M=0 does not mandate an entry for every Invalid Field. For M=1 with missing information, exclude overwrite, reset clearing and querying the wrong controller.
將 M、Error AER 與 entry 的關聯條件一起驗證；不要只比較「失敗 CQE 數」與「entry 數」。 || Validate correlation among M, error AERs and entries rather than requiring failure count to equal entry count.
先檢查 M，以及讀 Log 前是否已發生 Reset 或足以覆寫舊 entry 的新錯誤。 || First inspect M and any intervening reset or entry-overwriting errors.
''')

q(100,'如何從 Error Information 對回原始命令與錯誤欄位？ || How is an error entry correlated with its command and parameter?', ['error','sqe'], '''
關聯紀錄可把「哪個欄位錯了」轉成可驗證的原始 bytes。只看自然語言 Status，通常不足以找到 Host 真正送出的錯誤參數。 || Correlation turns a reported parameter fault into inspectable original bytes; a status name alone rarely locates the actual encoding mistake.
SQID＋CID 對應同一個 queue 使用期間的命令；因為 CID 會重用，還必須搭配 ECNT、時間與當時的命令快照。 || SQID+CID identifies a command within one queue lifetime; reuse requires ECNT, timing and a submission snapshot.
確認 LPVER，Base 2.4 的 entry 設為 1；CSI／OPC 在 LPVER≥1 才有效。 || Check LPVER, which is 1 in Base 2.4; CSI/OPC are valid for LPVER≥1.
Parameter Error Location 的 bits 7:0 是 SQE byte offset，10:8 是該 byte 的 bit；多 byte／bit 欄位指向最低有效位置。此 PEL 縮寫不要與 Persistent Event Log 混淆。 || Parameter Error Location bits 7:0 give SQE byte offset and bits 10:8 the bit within it; multi-bit/byte fields use their least-significant position. This PEL abbreviation differs from Persistent Event Log.
先對回 queue 使用期間，再比 SQID／CID／OPC／NSID；最後依 byte、bit 位置解碼原 SQE。例如位置指向 CDW10，就檢查那個命令對 CDW10 的定義。 || Establish queue lifetime, match IDs/opcode/namespace, then decode the original SQE at the reported byte and bit.
成功關聯後，可指出實際送出的值與違反條件，並用只修正該欄位的重測驗證。 || A successful correlation identifies the submitted value and violated condition, enabling a one-field correction test.
非命令錯誤的 SQID、CID、Parameter Error Location 應為 FFFFh；不能把 FFFFh 當成合法命令的資料偏移去讀記憶體。 || Non-command-specific errors use FFFFh for SQID, CID and Parameter Error Location; do not use it as a command-memory offset.
比對 namespace 與命令集後再解讀 LBA／CSINFO，因為這些欄位的意義取決於命令，而不是每個錯誤都一定有 failing LBA。 || Interpret LBA/CSINFO only after identifying namespace and command set; not every error carries a failing LBA.
先確認 CID 是否已重用；這是把正確 Log 誤配成另一筆命令的常見原因。 || Check CID reuse first; it can make a correct entry appear to describe the wrong command.
''')

q(101,'Error Log 的 Status 必須與 CQE 完全逐 bit 相同嗎？ || Must an error entry match every CQE status bit?', ['error','cqe'], '''
需要區分命令狀態與 Phase。若把包含 Phase 的整個 word 直接比較，可能將合法紀錄判成不一致。 || Separate command status from phase; comparing the entire word can reject a valid entry.
只對同一筆命令的 entry 與 CQE 做比較；非命令錯誤並沒有原始 CQE 可逐 bit 對照。 || Compare matched command-specific records; non-command errors have no originating CQE for exact comparison.
依 Figure 212 的 STS 與 Figure 101 的 Status 解碼，不要套用作業系統已移位或移除 Phase 的數值格式。 || Decode Figure212 STS and Figure101 status rather than assuming an OS-transformed numeric representation.
Error STS bits15:1 保存該命令的 Status；bit0 是 Phase，可表示原 CQE 的 P。CQE 中 Status 與 P 的位置不同，需先正規化再比較。 || Error STS bits 15:1 contain command status; bit 0 may indicate the CQE phase. Normalize their different placements before comparison.
保存原始 CQE 與 entry，先抽出 SCT／SC／DNR／M／CRD，再獨立處理 Phase；並確認 ECNT、SQID 與 CID。 || Preserve raw data, extract status components and handle phase separately, confirming ECNT and command IDs.
同一命令的 Status 應一致；Phase 依其「可回報」的定義處理，不要求所有記錄格式的完整 word 一樣。 || Matched command status should agree; phase follows its optional-reporting definition rather than requiring identical raw words.
非命令錯誤使用最適合的 Status，不是缺少 CQE 就代表錯誤。多個錯誤條件時，也要以實際選定的完成 Status 比對。 || Non-command errors use the most applicable status; absence of a CQE is not itself a defect. For multiple faults compare the selected completion status.
同時檢查解析程式是否把 SC、SCT 或 Phase 錯移一位；錯誤的 decoder 會讓所有 entry 都看似不符。 || Check decoder shifts for SC, SCT and phase; a parser defect can make every entry appear inconsistent.
先比較抽出的 SCT／SC，而不是十六進位字串的表面差異。 || Compare extracted SCT/SC before interpreting differences in raw hexadecimal strings.
''')

q(102,'多個錯誤、Log 容量與 Error Count 如何處理？ || How do concurrent errors, log capacity and Error Count interact?', ['error','idctrl'], '''
Error Count 用來辨識錯誤紀錄，而 Log 容量決定目前看得到多少歷史。兩者不同，所以有限的 Log 可以包含很大的累計序號。 || Error Count identifies records while capacity limits visible history; a small log can contain large cumulative identifiers.
容量與 entry 排序以 controller 的 Error Information 為範圍，不是每個 namespace 各自建立相同數量的 entry。 || Capacity and ordering are per-controller Error Information, not separate identical arrays for every namespace.
Identify.ELPE 為零起算，ELPE=3 表示最多 4 筆，每筆 64 bytes。 || ELPE is zero-based: ELPE=3 means at most four 64-byte entries.
ECNT 是 64-bit 計數，從 1 開始；0 表示無效 entry。最大值再增加時必須回到 1，不經過 0。 || ECNT is 64-bit and begins at one; zero marks an invalid entry. Incrementing the maximum wraps to one, not zero.
依發生時間由新到舊讀取。Log 滿時，controller 建議插入新 entry 並丟棄最舊 entry；取樣前後要保留 ECNT，才知道是否已有更新。 || Read newest first. When full, the controller should insert the new entry and discard the oldest; retain ECNT across samples to detect updates.
假設容量 4、最近序號為 9，正常可見 9、8、7、6；看不到 1～5 不表示它們沒有發生。 || With capacity four and latest count nine, entries 9,8,7,6 can be visible; absence of 1–5 does not mean they never occurred.
ECNT=0 的空 entry 不能當成第零次錯誤；也不要因序號有間隔，就直接判定 Log 壞掉，應先考慮取樣期間新增及被移除的紀錄。 || Zero is not a zeroth error. Gaps require considering updates and removed records before diagnosing corruption.
比較 SMART Error Information Log Entries 時，要分清累計值與目前 entry 數；它們的數值不需要相同。 || Distinguish the SMART cumulative entry count from current log occupancy; they need not be equal.
先檢查讀取長度是否只涵蓋一筆，卻被誤認為 controller 只保存一筆。 || First check whether the requested length retrieved only one entry rather than the full supported history.
''')

q(103,'非 Success CQE 沒有新增 Error Entry，一定違規嗎？ || Is a non-success CQE without a new error entry always nonconforming?', ['error','status'], '''
這題練習判斷證據是否足夠。命令失敗與必須提供額外錯誤資訊不是同一項要求，不能只看非零 Status 就宣告韌體違規。 || This tests sufficiency of evidence: command failure and required additional error information are separate requirements.
判斷限於這筆命令與其對應的記錄條件，不能用另一筆命令的新 entry 填補這筆命令的證據。 || Evaluate this command and its logging conditions; an unrelated new entry does not satisfy its evidence requirement.
保存 CQE.M、SCT／SC、錯誤前後 ECNT、ELPE 與 Reset 時間。 || Preserve M, SCT/SC, ECNT before/after, ELPE and reset timing.
關鍵欄位是 More；M=1 表示有這筆命令的補充資訊。Error AER 或個別命令規則也可能建立額外的記錄要求。 || More is central: M=1 identifies additional information for this command. Error AERs and particular command rules may impose further requirements.
先找出要求記錄的規範條件，再排除讀錯 controller、讀取太短、較新錯誤覆寫及 Reset 清除。最後才評估是否缺少必要 entry。 || Establish the logging requirement, exclude wrong controller, short read, overwrite and reset clearing, then evaluate missing required information.
合理結果可能是「這次不要求新增」；也可能是「要求的資訊仍可找到」。合規判斷不應預設每次都要讓 Error Count 增加。 || A valid result may be that no entry is required or that required information exists. Compliance does not require every failure to increment Error Count.
如果在排除其他原因後，M=1 仍沒有可關聯資訊，就有具體不一致可追查；M=0 且沒有額外條件時，不能用同一標準定罪。 || Unexplained missing information for M=1 is a concrete inconsistency; M=0 without an additional rule does not establish the same defect.
測試報告應附上規範條件、原 CQE 與 Log 快照，而不是只有「沒有看到 entry」一句結論。 || Attach the requirement, original CQE and log snapshots rather than only stating that no entry was seen.
先查測試程式是否把「每個非成功完成都必須新增 Log」寫成固定斷言。 || First inspect any test assertion that every non-success completion must create an entry.
''')

q(104,'一般命令錯誤後，其他命令是否可以繼續？ || Can other commands continue after an ordinary command error?', ['fatal','status','delete'], '''
多數命令錯誤不會破壞 queue，因此復原可以限制在失敗命令。這能避免為了單一非法參數，無故中止其他正常工作。 || Most command errors do not compromise queues, so recovery can remain local instead of aborting unrelated work.
先區分命令、queue 與 controller 三層。只有發現更廣泛的故障證據，才擴大復原範圍。 || Distinguish command, queue and controller failures, widening recovery only with broader evidence.
檢查 CQE、CSTS.CFS、queue 指標及其他命令是否仍正常完成；Error Information 用來補充原因。 || Inspect CQEs, CFS, queue pointers and continued completion of other commands, with Error Information for context.
Base 9.1 說明大多數命令錯誤仍應繼續處理命令；嚴重 queue 錯誤則建議刪除並重建相關 SQ／CQ。 || Base9.1 recommends continued processing for most command errors and queue recreation for serious queue failures.
保存失敗命令，確認 queue 沒有損壞後繼續合法命令；若 queue 受損，停止使用並依 SQ→CQ 的相依關係復原。 || Preserve the failed command and continue valid work if queues remain sound; stop and recover damaged queues in dependency order.
後續合法命令可以成功完成，同時先前失敗仍保留為一次独立結果。不能因後續成功，就抹去原本的錯誤。 || Later valid commands can succeed while the earlier failure remains a distinct result.
若 Admin 命令遇到嚴重通道錯誤，或 Delete Queue 沒有完成，規範建議 Controller Level Reset；這與普通 Invalid Field 不同。 || Serious Admin-channel failure or an uncompleted queue deletion calls for Controller Level Reset, unlike ordinary Invalid Field.
驗證錯誤隔離能力時，分別觀察同 SQ、共享 CQ 與其他 CQ 的命令，避免將資源壅塞誤認為全部停止。 || Observe commands in the same SQ, shared CQ and other CQs to distinguish congestion from a global processing stop.
先看 CQ 是否已滿；CQ Full 可以讓處理停住，卻不代表那筆參數錯誤破壞了 controller。 || Check for a full CQ first; backpressure can halt progress without controller damage.
''')

q(105,'哪些嚴重情況可能設定 CSTS.CFS，Host 應怎麼判斷？ || When may serious failures set CFS, and how should the host interpret it?', ['fatal','cc','virtual'], '''
CFS 提供 Host 在正常完成通道可能失效時仍可查看的嚴重狀態。它不是每筆失敗命令都必須設定的錯誤總旗標。 || CFS exposes a serious condition when completion communication may fail; it is not a mandatory flag for every command error.
CFS 屬於 controller。共享 subsystem 的其他 controller 是否受影響，必須另外觀察，不能只靠一個 CFS 位元推論。 || CFS is controller state; impact on other controllers requires separate evidence.
直接讀 CSTS.CFS，保存 CC、CAP、Ready 狀態及時間；若是 Secondary Controller，也先查 Online／Offline 狀態。 || Read CFS directly and preserve CC, CAP, readiness and timing; for secondary controllers also check Online/Offline state.
Base 9.5 允許在嚴重錯誤導致無法透過 Admin 或 I/O CQE 通訊時設定 CFS。Offline Secondary Controller 的 CFS 則有虛擬化定義。 || Base9.5 permits CFS for serious conditions preventing CQE communication. Offline secondary controllers have a separate virtualization use of CFS.
遇到 timeout 或重複錯誤時讀 CFS；確認是需復原的 fatal 狀態後，先做該 controller 的 Reset 與重新初始化，仍無法清除才評估支援且平台適用的 Subsystem Reset。 || On timeouts or repeated errors, read CFS. For a fatal condition, reset/reinitialize that controller, then consider supported platform-appropriate subsystem reset if the condition persists.
復原後應恢復可用狀態與正常命令處理。僅 CFS 清為 0，仍不足以省略 Admin Queue、Ready 與 I/O queue 的重新建立。 || Recovery must restore usable state and command processing; CFS clearing does not replace queue and readiness initialization.
CFS 本身不是 CQE，也不以中斷表示此狀態。若 controller 已無法回 CQE，就不能再要求每筆未完成命令都有 Internal Error CQE。 || CFS is not a CQE and its condition is not signaled by an interrupt. Lost completion communication cannot support a requirement for every outstanding command to return Internal Error.
比對 controller 角色、虛擬化狀態、實際通訊能力與 Reset 結果，才可區分預期 Offline 與真正 fatal 問題。 || Correlate role, virtualization state, communication and reset outcome to distinguish expected Offline state from fatal failure.
先確認這是不是 Offline 的 Secondary Controller，避免把預期的管理狀態誤判成硬體損壞。 || First determine whether this is an Offline secondary controller rather than a hardware failure.
''', {8:'讀取 CFS 沒有 CQE，因此 DNR／More 不適用於這個 Register 讀取。只有另外收到命令 CQE 時，才解讀該 CQE 的位元。 || Reading CFS has no CQE, so DNR/More do not apply to the register read; decode them only in a separately received completion.'})

q(106,'如何交叉比對 CQE、Error Information 與 Persistent Event？ || How are CQEs, Error Information and persistent events correlated?', ['cqe','error','pel','timestamp'], '''
三份證據的粒度不同：CQE 是單一命令結果，Error Information 是補充錯誤，PEL 是重要事件歷史。交叉比對能補足資訊，但不應要求一對一出現。 || CQEs describe commands, Error Information extends errors and PEL records significant events. Correlation adds evidence without requiring one-to-one records.
先標明 controller、namespace、queue 使用期間與事件範圍；不同範圍的紀錄可以有關聯，卻不一定代表同一筆命令。 || Establish controller, namespace, queue lifetime and event scope; related scopes do not necessarily identify one command.
確認 Error Log 的 ELPE、PEL 支援與 Supported Events Bitmap，以及 Timestamp 的來源與同步狀態。 || Check ELPE, PEL support/event bitmap and timestamp origin/synchronization.
CQE 用 SQID／CID／Status；Error entry 加 ECNT、NSID、OPC；PEL 用事件類型、controller 身分、時間及事件資料。Parameter Error Location 不是 Persistent Event Log 的位置。 || Use SQID/CID/status, then ECNT/NSID/opcode, then PEL event type/controller/time/data. Parameter Error Location is not a PEL file offset.
先對回命令與 Error entry，再找同一操作或時段的 PEL；若 Timestamp 曾變更，先重建時間關係，再下事件順序的結論。 || Match command and error entry first, then related PEL events; account for timestamp changes before ordering events.
成功的判讀會說明哪份證據支持哪個結論，以及哪些部分仍無法確認。例如有 Format Start，不代表已有 Format Completion。 || A useful result states what each source establishes and leaves unresolved; Format Start does not establish Format Completion.
缺少 PEL entry 不一定違規，先檢查該事件是否受支援及應記錄。另一方面，不能以「Log 選配」否定已宣告支援後的必要行為。 || A missing PEL entry is not automatically a defect; check support and recording conditions, but optional support does not excuse required behavior once advertised.
將能力、事件條件、CQE 與各自保留規則放在同一條時間線；Reset 後 entry 消失與計數保留可以同時成立。 || Correlate capability, trigger, CQE and retention on one timeline; entries clearing and counters persisting after reset can both be correct.
先確認三份紀錄的取樣時間與 controller 身分一致，再分析看似矛盾的值。 || First align sampling times and controller identity before interpreting apparent contradictions.
''')
