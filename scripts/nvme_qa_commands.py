from scripts.nvme_qa_model import add

add(31,'一筆 NVMe Command 的 Opcode、CID、NSID、Data Pointer 及 Command Dword 各有什麼用途？ || What do Opcode, CID, NSID, Data Pointer and command dwords mean?','queue',['sqe','idctrl'],'''
一筆命令必須讓 controller 知道要執行什麼操作、目標是誰、資料放在哪裡，以及要使用哪些參數。Command 格式就是把這些資訊放進各自指定的欄位。 || Encode the operation, target, data location and parameters into a command the controller can read.
解讀 Opcode 前，先確認這是 Admin 命令，還是哪一種 I/O command set 的命令。相同的 Opcode 數值，在不同命令集中不一定代表相同操作。 || Opcode interpretation depends on the Admin/I/O command set; equal numeric values need not mean the same operation across sets.
先確認對應能力，例如 OACS、ONCS、SGLS，並核對 namespace 使用的 CSI。接著再看該命令實際使用哪些公共欄位，不能假設每條命令都使用全部欄位。 || Check capabilities such as OACS, ONCS and SGLS and the namespace CSI. Not every command uses every common field.
公共 Command 格式為 64 bytes。CDW0 包含 OPC、FUSE、PSDT、CID；NSID 指定目標 namespace；MPTR 與 DPTR 描述 metadata 及資料的位置；CDW10～15 則由各命令定義用途。 || CDW0 contains OPC, FUSE, PSDT and CID. NSID selects the target, MPTR/DPTR describe data, and CDW10–15 are command-specific. The common command is 64 bytes.
先選定命令集，查明 Opcode 及支援能力，再設定合法的 NSID 與命令參數。準備好資料及指標後，分配一個在同一 SQ 中尚未使用的 CID，最後提交命令。PCIe Admin 命令使用 PRP，不能任意改用 SGL。 || Select command set, opcode/support, legal NSID/parameters, data/pointers and a unique outstanding CID, then submit. PCIe Admin commands use PRPs, not arbitrary SGLs.
Host 透過 SQID 與 CID 將 completion 配對回原命令。Status 表示完成狀態；命令產生的資料或其他結果，則可能放在 Host buffer 或 CQE DW0／1，並不是全部都放在 Status 裡。 || Match completion by SQID+CID. Results may reside in the host buffer or CQE DW0/1, not solely Status.
不支援的 Opcode 回報 Invalid Command Opcode（0/01h）。已定義欄位的值不合法時，通常回報 Invalid Field（0/02h）；如果該命令對此情況定義了專用 Status，則依專用規則處理。 || Unsupported opcode uses Invalid Command Opcode (0/01h). Invalid defined fields generally use Invalid Field (0/02h), subject to specific error definitions.
一起核對 Opcode 所屬的命令集、controller 宣告的能力，以及資料長度。即使 DPTR 位址合法，也不表示它描述的記憶體範圍足以容納這次傳輸的全部資料。 || Cross-check command-set context, support and payload size. A valid DPTR address does not prove sufficient described data length.
先確認命令是從 Admin SQ 還是 I/O SQ 提交，再確認應使用哪一份命令集規格解讀 Opcode 及參數。 || First identify whether the SQ is Admin or I/O and which command set decodes it.
''')

add(32,'Reserved 欄位非零、不合法 Command Dword 組合或不支援 Opcode 應如何處理？ || How are nonzero reserved fields, illegal field combinations and unsupported opcodes handled?','queue',['conventions','sqe','status'],'''
必須分清楚「整個 bit 或欄位被標為 Reserved」與「已定義欄位中的某個編碼值被保留」這兩種情況。它們對 controller 的檢查要求不同，不能一律要求保留位非零就必須報錯。 || Distinguish reserved bits from reserved coded values in defined fields; not every reserved bit requires receiver validation.
Host 如何填寫命令，以及 controller 必須檢查哪些內容，是兩組不同的義務。Host 填錯欄位，不一定代表 controller 也有義務偵測該錯誤。 || Host construction requirements and controller validation requirements are separate.
查 Base §1.4.1 的 reserved 定義、Opcode 支援與每個命令的欄位限制。 || Use Base §1.4.1 reserved semantics, opcode support and the individual command's field restrictions.
Host 必須將 Reserved 欄位清零，但接收端不必檢查 Reserved bits、bytes 或 fields。另一種情況是：欄位本身已有定義，Host 卻填入其中保留不用的編碼；對這種保留編碼，controller 必須報錯。 || The host shall zero reserved fields; the recipient need not check reserved bits/bytes/fields. A reserved coded value in a defined command field shall be reported as an error.
Host 可先將 SQE 全部清零，再填入命令實際使用的欄位。驗證錯誤處理時，每次只改一項條件，並記錄規範對該條件使用的是 shall 還是 should，避免把建議要求當成強制要求。 || Start from a zeroed SQE and populate used fields. Change one item per error exercise and record whether the requirement says shall or should.
合法的欄位組合應依命令定義正常處理。如果 controller 沒有檢查某個 Reserved bit，也不能因此推論 Host 將該 bit 寫成非零就是合法用法。 || A legal combination follows normal completion. Lack of reserved-bit checking does not make a nonzero host value legal.
不支援或保留的 Opcode 回報 0/01h；已定義欄位中的非法值，一般回報 0/02h，除非另有專用 Status。多個錯誤同時存在時，通常可以選擇其中一種回報。因此，不能把「Reserved bit 非零」一律判定為必須回報 0/02h。 || Unsupported/reserved opcode: 0/01h. Illegal defined field: generally 0/02h unless a specific status applies. Multiple faults usually permit choosing one; nonzero reserved bits do not universally mandate 0/02h.
驗證紀錄應分別說明：Host 是否違反填寫規則，以及 controller 是否有義務偵測這項錯誤。只有把兩者分開，才不會將規範允許不檢查的情況，誤判成韌體缺陷。 || Record both host violation and controller detection obligations to avoid labeling permitted nonchecking as a firmware bug.
先問改到的是「保留位」還是「已定義欄位中的保留編碼」。 || First ask whether the modified item is a reserved bit or a reserved encoding within a defined field.
''')

add(33,'NSID 不存在、Inactive、不適用或錯誤使用 Broadcast NSID 時，應回傳什麼類型的 Status？ || Which statuses apply to invalid, inactive, unused and improperly broadcast NSIDs?','queue',['sqe','nsid','feature'],'''
命令指定的 namespace 不存在、尚未對此 controller 啟用，以及命令根本不使用 NSID，是不同情況。先分清楚原因，才能選對 Status。 || Separate invalid identity, inactive namespace and a command that does not use NSID.
namespace 是否為 active，是相對於接收命令的 controller 而言。它可以經由另一個 controller 存取，不代表目前這個 controller 也能存取它。 || Active state is controller-relative. Accessibility through another path does not establish activity on this controller.
先用 Active 與 Allocated Namespace ID List 確認狀態，再查該命令如何使用 NSID，以及是否定義了例外處理。 || Use active/allocated lists and the command's NSID rules, then check command-specific exceptions.
NSID=0、有效且已配置的 NSID、inactive NSID，以及 FFFFFFFFh，必須依命令規則分別判讀。尤其 FFFFFFFFh 影響哪些 namespace，要看各命令自己的定義，不能一律視為同一種廣播範圍。 || Distinguish zero, valid allocated, inactive and FFFFFFFFh identifiers. Each command defines the scope of FFFFFFFFh.
先確認命令是否使用 NSID，再確認它是否允許目前的 namespace 狀態及 broadcast 用法。例如，Identify 的某些 CNS 本來就是查詢 allocated 或 inactive namespace，不能直接套用一般 I/O 命令的限制。 || Determine whether NSID is used, then permitted namespace state and broadcast support. Some Identify CNS values intentionally query allocated/inactive namespaces.
目標合法時，依該命令的定義完成處理。有些查詢對不存在或 inactive namespace 定義了特殊回覆，因此必須先看命令本身的規則，再使用通用 Status 表。 || Legal targets follow the command's completion rules. Some queries define special replies for absent/inactive objects that override the generic rule.
依 Figure 93 的一般規則，使用 NSID 的命令若指定 inactive namespace，回報 Invalid Field（0/02h）；若指定無效 NSID，則回報 Invalid Namespace or Format（0/0Bh）。命令不支援 broadcast 卻填入 FFFFFFFFh，或命令不使用 NSID 卻填入非零值時，回報 0/02h。若命令另有明確例外，則優先依例外規則處理。 || Figure 93 defaults: inactive on an NSID-using command returns 0/02h, invalid returns 0/0Bh. Unsupported broadcast or nonzero NSID on an unused field returns 0/02h. Command-specific exceptions take precedence.
一起核對原 SQE 的 NSID、提交當時的 active list，以及該 CNS、FID 或 Opcode 的使用規則。namespace 狀態之後可能改變，不能只拿現在的清單解釋過去命令的結果。 || Correlate the original NSID, the list at that time and CNS/FID/opcode rules. A current list alone may not explain a past request.
先查命令是否真的屬於 Figure 93 的一般情況，或已有明確例外。 || First check whether the command uses the generic rule or defines an explicit exception.
''')

add(34,'CQE 中的 SQHD、SQID、CID、Phase Tag 及 Status 分別有什麼用途？ || What are SQHD, SQID, CID, phase and status used for in a CQE?','queue',['cqe','queue'],'''
一筆 CQE 同時提供命令結果、原命令身分與 queue 進度；這些欄位不能彼此代替。 || A CQE carries command result, identity and queue progress; these fields are not interchangeable.
SQHD 描述的是 SQID 指定之 SQ 的進度；P 用來辨識目前 CQ 位置中的資料是否有效；Status 則是 SQID 與 CID 指定之命令的結果。三者描述的對象不同。 || SQHD describes the identified SQ, P the CQ slot, and Status the command identified by SQID+CID.
判讀時使用目前的 queue 配置及 CQE 公共格式。SQHD 的意義由格式定義，不會因某個 Feature 的選擇而改變。 || Interpret using current queue configuration and the common CQE layout, not a feature-selected meaning of SQHD.
DW2：SQHD、SQID；DW3：CID、P、Status；DW0／1 是命令特定結果。SQHD 表示建立 CQE 當時已消費的位置。 || DW2 contains SQHD/SQID; DW3 contains CID/P/Status; DW0/1 carry command-specific results. SQHD reports consumption when that CQE was constructed.
先以 P 確認 CQE 有效，再透過 SQID 與 CID 找到原命令，解析 Status 及其他結果。接著更新 SQ 可用位置的紀錄，最後釋放這筆 CQE 所占的位置。 || Validate P, match SQID+CID, decode status/results, update SQ slot availability and finally release the CQ slot.
例如，一筆 completion 回報 SQHD=8，只表示 controller 的 SQ Head 已前進到 8。它不表示原先放在索引 0～7 的所有命令，都已經執行完成。 || SQHD=8 reports head advancement to eight; it does not establish execution completion of every command from slots zero through seven.
解析 Status 時，必須一起讀取 SCT 與 SC；P 不屬於錯誤碼。如果 CQE 格式異常或 CID 無法對回命令，先檢查記憶體內容及 queue 是否已重建，不要替這類現象自行定義新的 NVMe Status。 || Decode SCT and SC together; P is not an error code. Malformed CQEs or unknown CIDs require checking memory/lifetimes, not inventing a new NVMe status.
分別確認 SQHD 的進度、命令是否完成，以及資料 buffer 何時可以回收。SQ 位置已可重用，只表示 controller 已消費該 SQE，不表示 Host 可以提前釋放命令仍在使用的資料 buffer。 || Distinguish SQ consumption, command completion and data-buffer reclamation. Reusable SQ slots do not permit early release of command data.
先確認 P 符合目前期待值，再解讀其他欄位。若反過來先看 CID 或 Status，容易把上一圈留下的資料誤認為新的錯誤完成。 || First establish a new phase before interpreting the remaining fields, avoiding stale-memory completions.
''')

add(35,'Status Code Type 與 Status Code 應如何解析？ || How should Status Code Type and Status Code be decoded?','queue',['status','cqe'],'''
同一個 SC 數值在不同 SCT 有不同意義，必須用成對值判讀。 || The same SC can mean different things under different SCTs; decode the pair.
Status 是這一筆命令的完成狀態。解讀時還要搭配 Opcode、所屬命令集及當時的錯誤條件，才能知道這個結果代表什麼。 || Status belongs to this completion and must be interpreted with opcode, command set and failure conditions.
公共 SCT／SC 定義在 Base；NVM 命令特有的狀態則由 NVM Command Set 補充。查表時必須使用對應命令集的定義，不能拿另一種命令集的同一數值來解釋。 || Base defines common SCT/SC values; use NVM definitions for its specific codes, not another command set's table.
在 CQE DW3 中 SCT=bits27:25、SC=24:17，P=16；若程式先取最後 16-bit word，SCT 位置變為 11:9、SC 為 8:1。 || In CQE DW3, SCT is bits27:25, SC bits24:17 and P bit16. In the final 16-bit word, SCT occupies bits11:9 and SC bits8:1.
先確認程式讀取的資料寬度及位元組順序，再取出 SCT 與 SC，查閱對應的 Status 表。之後再解讀 DNR、More、CRD 及命令特定的結果欄位。 || Confirm data width/endianness, extract SCT/SC, select the correct table, then inspect DNR, More, CRD and command-specific results.
SCT=0、SC=00h 表示 Successful Completion。不過，Host 仍須先確認 P 有效，而且 SQID 與 CID 能對回原命令；不能只因部分低位元為零，就認定讀到了一筆新的成功完成。 || SCT=0, SC=00h means Successful Completion, but matching and phase still matter; zero low bits alone do not establish a new valid success.
例：0/01h 是 Invalid Command Opcode；1/01h 是 Invalid Queue Identifier。SCT=2 為 Media and Data Integrity，3 為 Path Related，7 為 Vendor Specific。 || For example, 0/01h is Invalid Command Opcode and 1/01h Invalid Queue Identifier. SCT2 is Media/Data Integrity, SCT3 Path Related and SCT7 Vendor Specific.
驗證時同時保留原始 CQE bytes 與解碼後的欄位值。有些工具會先移除 P，或重新排列 Status 的位元，因此不同工具輸出的整數，不能在未確認格式前直接比較。 || Preserve raw CQE bytes and decoded values. Tools that remove P or repack status cannot have their integers compared blindly.
先檢查是否誤把 Phase 算進 Status，或把 DW3 的位元位置直接套用到已取出的 16-bit Status word。 || First check accidental inclusion of P or use of DW3 bit positions on a 16-bit status word.
''')

add(36,'More 與 Do Not Retry 位元分別代表什麼？DNR 為 0 是否代表一定能直接重試？ || What do More and DNR mean, and does DNR=0 guarantee an immediate safe retry?','queue',['status','error','behavior','fatal'],'''
判讀重試時，有三個問題要分開：相同命令是否可能成功、是否有補充錯誤資訊，以及再次執行是否安全。DNR 與 More 不能單獨回答全部問題。 || Separate potential retry success, additional error information and retry safety.
DNR 與 More 都針對目前這筆 CQE。DNR 所說的「重試相同命令」，也包含改由同一 NVM subsystem 的其他 controller 提交，不能只換 controller 就忽略它的含義。 || Decode the same CQE; DNR's identical-command retry semantics cover any controller in the same subsystem.
這些公共位元固定存在於 CQE 格式中。若要使用 CRD 指示的重試延遲，還需確認 Host Behavior Support.ACRE，以及 Identify.CRDT1～3 的設定與數值。 || The common bits always exist; CRD use additionally depends on Host Behavior Support.ACRE and Identify.CRDT1–3.
DNR 不表示命令一定尚未修改資料。More=1 則表示 Error Information Log（LID 01h）包含這筆命令的額外 Status 資訊，不是表示後面還會有另一筆 completion。 || DNR does not establish that data was unchanged. More=1 points to additional status in LID01h, not another completion.
先分析錯誤原因。若 DNR=0，應處理暫時性的失敗條件，依有效的 CRD 等待，再判斷能否安全重送。若同一操作執行兩次可能產生不同結果，還要先確認前一次操作是否已經生效，避免重複作用。 || Decode the cause; with DNR=0, address transient conditions, respect valid CRD guidance and assess retry safety. For non-idempotent work, determine whether the earlier operation took effect.
重試是否成功，必須看重試命令的新 CQE。DNR=0 只表示重試可能成功，不保證立刻重送就會成功，也不保證再次執行不會造成重複作用。 || Only the new CQE establishes retry success. DNR=0 means may succeed, not immediate or duplicate-free success.
若命令因參數非法而失敗，卻完全不修改參數就重送，通常無法解決問題。對明確規定 DNR 的 Status，則必須遵守該規則；例如 Command Interrupted（0/21h）要求 DNR=0，而且只有在 ACRE 已啟用時才能回報。 || Repeating unchanged invalid parameters is not useful. Apply explicit DNR rules: Command Interrupted (0/21h) requires DNR=0 and may be returned only with ACRE enabled.
More=1 時，應能在 Error Information Log 中找到可與此命令關聯的額外資訊。CRD 是否有效，則必須搭配 DNR 與 ACRE 判斷，不能只看到非零值就直接使用。 || More=1 must correspond to associated additional Error Information. Interpret CRD only when DNR/ACRE make it applicable.
先確認是否已收到錯誤 CQE，還是只有 Host 自己判定 timeout。如果根本沒有 CQE，就沒有可用來判斷的 DNR。 || First distinguish an actual error completion from a host timeout; without a CQE there is no DNR to interpret.
''')

add(37,'Completion 已寫入但 Host 未處理，可能與 Phase Tag、CQ 位置或 Interrupt 有什麼關係？ || Why might a posted completion remain unprocessed by the host?','queue',['cqe','pcie','irq','irqfeat'],'''
controller 已寫入 completion、Host 已收到中斷通知，以及 Host 已處理 CQE，是三個不同階段。前一階段完成，不代表後一階段也已完成。 || Separate completion posting, notification delivery and host consumption.
需要檢查目標 CQ 的記憶體、Host 維護的 Head 與期待 Phase，以及這條 CQ 使用的中斷。Host 尚未處理結果，不一定表示命令執行失敗。 || This involves CQ memory, host Head/expected phase and interrupt routing, not necessarily execution failure.
確認 Create CQ.IEN／IV、使用的 MSI 或 MSI-X 模式、mask 與中斷 Feature。 || Check Create CQ.IEN/IV, the selected MSI/MSI-X mode, masks and interrupt features.
使用 MSI-X 時，檢查 Function Mask、vector mask 與 PBA；使用一般 MSI 時，則依 INTMS／INTMC 的規則判斷。無論中斷如何設定，CQE 是否有效仍由正確的 CQ 位置與 Phase 決定。 || For MSI-X inspect Function Mask, vector mask and PBA; ordinary MSI uses different INTMS/INTMC rules. CQE validity still depends on location and phase.
先確認 Host 讀取的是正確 CQ 的目前 Head，再檢查 P。有有效的新 CQE 就應處理；如果問題是沒有收到中斷，再檢查 IEN、IV、mask、coalescing 設定及 Host 的中斷處理程式。 || Inspect the correct CQ Head and phase first. Process valid CQEs; investigate missing interrupts through IEN, IV, masks, coalescing and the host handler.
Host 可以透過輪詢處理合法的 CQE，即使這筆完成沒有各自對應一個中斷。中斷可能合併通知，因此中斷數量不必等於 completion 數量。 || Polling can consume a valid completion without a one-to-one interrupt. Interrupt count need not equal completion count.
沒有收到中斷，本身不對應某個 NVMe 錯誤 Status，原來的 CQE 甚至可能表示成功。不能只因中斷未到達，就判定 controller 應回報 Internal Error。 || Missing an interrupt does not itself carry an NVMe error status; the CQE may be successful. Do not invent Internal Error for it.
比對 CQE 寫入、mask 變更、中斷到達及 Head 更新的時間。中斷負責通知 Host；真正的命令結果仍在 CQE 中。 || Compare posting, masking, interrupt delivery and Head-update times. An IRQ is notification, not the completion payload itself.
先確認 Host 是否讀錯 CQ、讀錯位置，或使用錯誤的期待 Phase。這些資訊能直接判斷 CQE 是否被漏讀，再進一步追查中斷路徑。 || First check CQ/slot selection and expected phase before assuming interrupt loss.
''')

add(38,'多個 Command 同時 Outstanding 時，Controller 是否必須按照提交順序完成？ || Must outstanding commands complete in submission order?','queue',['order','nvmatomic'],'''
SQ 保留命令的提交順序，但這不表示 controller 必須依相同順序執行或完成所有命令。理解這個差別，才能正確建立命令之間的依賴。 || Understand that queued submission order is not a universal execution/completion-order guarantee.
一般互不相依的命令，即使放在同一條 SQ，也不能假設先提交就一定先完成。來自不同 SQ 的命令，更不能只因提交時間接近，就推論它們有先後保證。 || Independent commands need not complete FIFO even within one SQ; nearby submission times across SQs do not establish dependency.
先看命令是否屬 fused operation 或有專屬順序規則；FUSES 表示 fused 支援。 || Check for a fused operation or command-specific ordering rule; FUSES advertises fused support.
應分清楚命令已提交、SQE 已被消費、命令開始處理，以及命令已完成這四個階段。SQHD 只反映 SQE 已被消費的進度，不直接表示命令已完成。 || Distinguish submitted, consumed, processing and completed stages. SQHD only reports consumption.
如果命令 B 需要使用命令 A 的結果，Host 應等 A 成功完成後才提交 B。如果還要求資料已持久保存，則要另外依 Flush 或 FUA 的規則處理，不能只靠提交順序保證。 || If B depends on A, wait for A's successful completion before submitting B. Apply Flush/FUA separately for persistence.
若 Read A 與 Read B 沒有相依關係，較晚提交的 B 先完成可以是合法行為。Host 必須依 SQID 與 CID 配對結果，不能假設 completion 會按照提交陣列的順序回來。 || Independent Read B may legally complete before Read A; match by SQID/CID rather than submission-array order.
單純以相反順序完成，不構成某個錯誤 Status。只有違反規範明定的多命令先後規則時，才依該序列的專用錯誤條件判斷。 || Out-of-order completion alone has no error status. Violations of defined multicommand sequences follow their own errors.
驗證時，應指出命令之間實際要求哪一種先後關係，再檢查結果是否符合。只說「看起來沒有依序完成」，不足以判定不符合規範。 || Test required causal relations rather than treating apparent reordering alone as noncompliance.
先問兩筆命令有沒有規範明定或 Host 主動建立的相依關係。 || First identify a specification-defined or host-established dependency.
''')

add(39,'哪些 Command 具有順序相依性？Host 為什麼不能假設所有 Command 都依序完成？ || Which commands have ordering dependencies, and why is universal ordered completion unsafe to assume?','queue',['order','create','delete','setfeat','nvmatomic'],'''
Host 必須明確建立真正需要的命令依賴。把命令依序放入 queue，不會自動得到一組不可分割、依序完成的操作。 || Explicitly establish real dependencies instead of treating queuing as a transaction mechanism.
例如，先成功建立 CQ，才能建立使用它的 SQ；刪除時則先刪 SQ，再刪 CQ。另一類例子是等 Set Features 成功後，再提交需要使用新設定的命令。支援的 fused pair 則有自己的成對提交規則。 || Examples include CQ-before-SQ creation, SQ-before-CQ deletion, successful Set Features before affected new commands, and supported fused pairs.
分別查閱 FUSES、使用中的 Feature，以及相關命令的順序要求。不存在一個通用能力位，可以替所有命令建立相同的順序保證。 || Check FUSES and individual feature/command rules; no global ordered-mode bit resolves every case.
FUSE=01b／10b 表示成對第一／第二筆；PCIe 中必須在同一 SQ 相鄰並用同一次 Tail 更新提交。 || FUSE=01b/10b marks the first/second command. In PCIe they must be adjacent in one SQ and submitted by one Tail update.
一般命令的相依關係，可以透過等待前一筆 completion 來建立；fused pair 則必須依專用規則一起提交，而且兩筆命令各自有 CQE。不能將兩筆相依命令同時送出後，就假設 controller 會自動安排成 Host 想要的順序。 || Establish ordinary dependencies by waiting for completion; submit fused pairs under their special rules with separate CQEs. Do not assume the controller orders arbitrary concurrent requests for the host.
Set Features 成功後才提交的命令，使用新的設定；在此之前已提交的命令，則可能使用舊值或新值。如果驗證需要排除這種差異，應先等待既有命令完成，再變更設定。 || Commands submitted after successful Set Features use the new value; previously submitted ones may use old or new settings. Drain first when testing a clean transition.
缺少相鄰的 fused partner 時，回報 Command Aborted due to Missing Fused Command（0/0Ah）。CQ 與 SQ 的建立或刪除順序錯誤，則依各自的 Create／Delete Status 處理，不能全部套用 0/0Ch。 || A missing adjacent fused partner uses 0/0Ah. Queue dependency errors use Create/Delete-specific statuses, not universally 0/0Ch.
在時間線上標出前一步 completion 與下一步 submission，確認 Host 確實建立了必要的先後關係。FUA 控制的是資料持久性，不能替代這些命令之間的依賴。 || Trace completion-to-submission boundaries. FUA controls persistence, not these dependencies.
先確認 Host 等待的是前一步成功完成，而不是僅等到提交函式返回。函式返回時，命令可能還沒有執行完畢。 || First check whether the host waited for successful completion rather than merely submission-function return.
''')

add(40,'Outstanding Command 達到限制或 CQ Full 時，Controller 如何限制取得新 Command？ || How do outstanding limits and CQ Full constrain further command handling?','queue',['queue','order','cqe'],'''
必須分清楚三種限制：SQ 還能放多少命令、controller 內部還有多少執行資源，以及 CQ 還能放多少完成結果。單用一個 queue depth 數字，無法解釋所有停滯原因。 || Separate host submission capacity, internal execution resources and completion capacity instead of using one queue-depth value to explain every stall.
限制可針對 SQ、共享 CQ 或 controller 內部資源；不是每個限制都代表整個 controller 失效。 || Limits may affect an SQ, shared CQ or internal resources; not every limit is controller-wide failure.
Host 根據 queue 大小及 SQHD 追蹤可用位置，同時維持未完成命令的 CID 唯一性。其他 transport 使用的 MAXCMD 流量控制假設，不能直接套用到 PCIe。 || The host uses queue size/SQHD and unique CIDs. Do not import another transport's MAXCMD flow-control assumptions into PCIe.
controller 如何從已提交的 SQE 取得命令，由廠商實作決定；仲裁則決定從哪條 SQ 選出候選命令，開始處理。取得 SQE 與開始執行命令，仍是不同動作。 || Fetching submitted SQEs uses a vendor-specific algorithm; arbitration selects where candidate processing starts. Fetch and execution start are distinct.
Host 不得覆寫 controller 尚未消費的 SQE；controller 也不得向已滿的 CQ 寫入 completion。必要時，controller 可以停止處理關聯 SQ 的更多命令，但使用其他獨立 CQ 的 SQ 仍須繼續處理。 || The host must not overwrite unconsumed SQEs; the controller must not post into a full CQ and may pause related further processing while independent SQs continue.
空間釋放後，處理可以繼續。SQ 的某個位置已經可用，但原先放在那裡的命令仍未完成，是可能發生的情況，因為取得 SQE 不等於完成命令。 || Progress resumes as capacity becomes available. A freed SQ slot can belong to a still-outstanding command because consumption is not completion.
正常達到資源限制，不表示 controller 必須回報錯誤 CQE。如果 Host 違反 queue 指標規則、重用未完成命令的 CID，或超過某類命令的專用限制，才依各項錯誤規則處理。 || Normal resource limits do not automatically require error CQEs; pointer misuse, CID reuse and command-specific limits have separate rules.
分別收集提交、取得、開始處理及完成的證據。只看到 Host 已提交多少筆命令，不能推論 controller 已同時開始執行全部命令。 || Use evidence for each stage; submitted count does not establish simultaneous execution of every command.
先辨認是哪一項限制用完：SQ 位置、CQ 位置，還是 Host 自己設定的未完成命令配額。 || First determine whether the SQ, CQ or only the host outstanding limit is full.
''')

add(41,'Round Robin 與 Weighted Round Robin Arbitration 有什麼差異？ || How do Round Robin and Weighted Round Robin arbitration differ?','feature',['order','arbit','cap','create'],'''
多條 SQ 同時有可處理的命令時，仲裁決定下一批從哪條 SQ 開始處理。不同仲裁方式也讓 Host 能表達各 SQ 希望取得的服務優先順序。 || Select which SQ starts the next batch when several contain eligible work, allowing host service priorities.
仲裁影響的是哪些候選命令先開始處理，不保證 completion 的回報順序，也不保證量測到固定的 IOPS 比例。 || Arbitration governs candidate processing starts, not completion order or a fixed IOPS ratio.
所有 controller 都支援 Round Robin。若要使用選配的 Weighted Round Robin（WRR），先查 CAP.AMS 確認支援，再透過 CC.AMS 選用。 || All controllers support Round Robin. Discover optional WRR via CAP.AMS and select it with CC.AMS.
FID 01h 提供 Arbitration Burst（AB）及 HPW／MPW／LPW；SQ.QPRIO 在 WRR 生效。AB=7 表示不限 burst，其他值為 2^AB；權重為欄位值+1。 || FID01h provides AB and HPW/MPW/LPW; QPRIO applies in WRR. AB=7 means unlimited burst, otherwise 2^AB; weights encode value+1.
在 controller 停用時選定 CC.AMS。啟用後設定 FID 01h，並在建立 SQ 時設定 QPRIO。驗證時，持續提供可執行的命令，觀察 controller 如何選擇開始處理的 SQ。 || Select CC.AMS while disabled, set FID01h after enabling, create SQ priorities and observe under continuously eligible workloads.
Round Robin 讓各 SQ 輪流獲得處理機會，Admin SQ 也包含在內。WRR 則先處理 Admin，再處理 Urgent，之後依權重分配 High、Medium、Low；同一類別內仍有輪流選擇的規則。 || RR gives all SQs, including Admin, equal round-robin priority. WRR prioritizes Admin, then Urgent, then weighted High/Medium/Low service with within-class rules.
若將 CC.AMS 設為不支援的值，該 Register 操作的結果未定義，不能要求回傳 Set Features 的 Invalid Field。若是 FID 01h 中已定義的參數值非法，則依 Set Features 的命令規則處理。 || Unsupported CC.AMS programming is undefined, not a Set Features Invalid Field completion. Invalid defined FID01h parameters follow command rules.
Get Features 讀回 FID 01h，只能證明目前設定值。命令執行時間、媒體資源衝突及 CQ 空間也會影響吞吐量，因此不能只看 IOPS 比例，就判定 WRR 是否正確。 || Get FID01h verifies configuration only. Service time, media contention and CQ pressure affect throughput, so IOPS ratios alone cannot validate WRR.
先看 CC.AMS 是否真的選 WRR，再解讀 QPRIO 與權重。 || First confirm CC.AMS actually selects WRR before interpreting priorities and weights.
''')

add(42,'Urgent、High、Medium 及 Low Queue Priority 在哪些情況下生效？ || When do Urgent, High, Medium and Low queue priorities take effect?','feature',['order','create','arbit'],'''
Queue Priority 用來讓不同 SQ 取得不同的服務機會，但只有在選用對應仲裁機制時，這項設定才會生效。 || Give SQs different service opportunities only under the applicable arbitration mechanism.
QPRIO 是 SQ 層級設定，不是每筆 Read／Write 的 priority 欄位。 || QPRIO is an SQ-level setting, not a per-Read/Write priority field.
CAP.AMS 支援 WRR 且 CC.AMS 已選 WRR 才使用 QPRIO；否則 controller 必須忽略它。 || QPRIO is used only when WRR is supported and selected through CC.AMS; otherwise it shall be ignored.
Create SQ CDW11.QPRIO：00b Urgent、01b High、10b Medium、11b Low；FID 01h 為後三種設定權重。 || Create SQ CDW11.QPRIO encodes Urgent00b, High01b, Medium10b and Low11b; FID01h weights the latter three.
Host 可依工作類型建立不同 SQ，並設定各自的 QPRIO。若要改變既有 SQ 的這項屬性，需依 queue 重建流程處理；修改 Host 記憶體中已提交過的 Create SQE，不會改變現有 SQ 的設定。 || Create SQs with suitable QPRIO. Change an existing queue through reconstruction, not by editing an old Create SQE in host memory.
Urgent 的優先順序高於 High、Medium、Low，但低於 Admin。若 Urgent 工作持續不斷，較低類別可能長時間得不到處理機會，因此不能假設 High 一定享有固定的最低頻寬。 || Urgent outranks weighted service but remains below Admin. Persistent Urgent work may starve lower classes; High has no universal fixed minimum bandwidth.
Round Robin 模式下，controller 忽略 QPRIO 是合法行為，不能因此判定優先級功能失效。若 queue 參數本身非法，仍依 Create Queue 的 Status 規則處理。 || Ignoring QPRIO under RR is correct, not a failed priority feature. Invalid queue parameters still follow Create statuses.
驗證時一起記錄每條 SQ 的 QPRIO、CC.AMS 及 FID 01h。只有優先級而不知道仲裁模式，或只有模式而不知道權重，都不足以解釋實際選擇順序。 || Preserve each SQ's QPRIO, CC.AMS and FID01h together; none alone explains priority behavior.
先排除其實正在用 RR 的情況。 || First rule out operation under RR.
''')

add(43,'多個 Queue 競爭資源時，如何判斷 Arbitration 是否符合設定？ || How can arbitration be evaluated when multiple queues compete?','feature',['order','arbit','create'],'''
判斷仲裁是否符合規範，需要觀察 controller 如何選擇開始處理的命令。延遲或吞吐量有差異，不一定表示選擇規則遭到違反。 || Translate candidate-selection requirements into evidence rather than equating latency or throughput differences with arbitration violations.
比較同一 controller 上互相競爭的 SQ，並先排除 CQ Full、命令相依、處理成本不同，以及 Host 沒有持續提供命令等干擾因素。 || Observe competing SQs on one controller after excluding CQ Full, dependencies, unequal service costs and insufficient offered work.
記錄 CAP.AMS、CC.AMS、FID 01h 的 AB／權重及每條 SQ 的 QPRIO。 || Record CAP.AMS, CC.AMS, FID01h AB/weights and each SQ's QPRIO.
WRR 在 High、Medium、Low 類別中，每輪能開始處理的命令數，受到剩餘服務額度及 AB 限制。因此，不只要看 SQ 是否非空，還要確認其中確實有可開始處理的候選命令。 || In WRR, processing starts per round are limited by remaining credits and AB. Ready candidates matter, not merely a nonempty SQ.
可用命令類型與大小相近、Host 持續提交，而且 CQ 不阻塞的情境來比較。若能取得開始處理或排程紀錄，就直接核對選擇順序；如果只有 CQE，則必須承認完成結果不足以還原全部內部排程。 || Use comparable commands, sustained supply and nonblocking CQs. Compare processing-start/scheduler evidence where available; CQEs alone cannot reconstruct all internal choices.
例如 High 與 Low 的權重為 4:1，描述的是分配服務額度的比例，不代表每個短時間區間內，完成命令數都必須剛好是 4:1。 || High/Low weights of 4:1 describe service credits, not an exact completion ratio in every short interval.
仲裁量測本身不會產生錯誤 CQE。應先確認設定命令成功，再對照規範中的 shall 與 may。如果測試期間沒有持續提供可處理的命令，就不宜單憑吞吐結果判定不符合規範。 || Measurement itself has no error CQE. Verify configuration success and distinguish shall/may requirements; unsuitable workload conditions do not establish noncompliance.
要判定違反規範，必須指出具體的選擇規則，以及哪一段觀察結果與它矛盾。只有「高優先級比較慢」的現象，還不足以完成這項判斷。 || A noncompliance claim needs a contradiction between a defined selection rule and evidence, not merely slower high-priority work.
先確認高優先級 SQ 是否持續有可開始處理的命令，再確認關聯 CQ 沒有因空間已滿而阻塞。 || First verify continuously eligible high-priority candidates and available CQ space.
''')
