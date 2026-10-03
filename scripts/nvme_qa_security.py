"""Q237–245: protocol transport versus security policy and Lockdown scope."""
from scripts.nvme_qa_extension import question
from scripts.nvme_qa_model import COMMON, REFS, pair
REFS['security']='B|5.2.28–5.2.29|480-482|456–462'
REFS['lockdown']='B|5.2.16, 8.1.5|431-434,623-625|365–367'
REFS['locklog']='B|5.2.13.1.20|305-309|274–278'
REFS['lockpersist']='B|5.2.30.1.25.4–5.2.30.1.25.4.1|519-520|518–519'
COMMON['security_op']={**COMMON['command'],
 9:pair("""Security Send／Receive 的一般資料交換不定義統一成功 AER。若所選協定或其他功能造成特定狀態變化，須依該功能另行確認；不能自行編造「認證完成」NVMe 事件。 || Generic Security Send/Receive defines no universal success AER. Protocol-specific or other resulting conditions require their own rules; do not invent an authentication-complete NVMe event."""),
 10:pair("""先分開 NVMe CQE 與安全協定回覆：CQE 說明命令傳輸／處理，Security Receive 的 payload 才依協定描述安全操作結果。Error Information 仍依 NVMe 錯誤記錄條件處理。 || Separate NVMe CQE from protocol results in Security Receive payload. Error Information follows NVMe error-logging conditions."""),
 11:pair("""Security 資料交換不是 PEL 的通用逐命令稽核紀錄。若裝置支援 TCG-defined 或其他相關事件，需使用該事件的實際定義；三份 NVMe 規格不足以自行定義外部安全協定內容。 || Security exchange is not a generic per-command PEL audit trail. TCG-defined or related events require their actual definitions beyond these three NVMe specifications."""),
 12:pair("""CLR 後 Security Receive 待取的結果可能不保留。安全鎖定、認證 session 與金鑰的持續性由所選協定決定，不能把失去傳輸結果解讀成自動解鎖或清除金鑰。 || Pending Security Receive data may not survive CLR. Lock/session/key persistence is protocol-specific; lost transport results do not establish unlock or key erasure."""),
 13:pair("""Subsystem Reset 後重新確認通訊及協定狀態。NVMe Base 不給所有 Security Protocol 一個共同的認證或鎖定保留答案，因此測試須先指定協定與狀態。 || Rediscover communication and protocol state after subsystem reset. Base supplies no universal authentication/lock retention rule for every security protocol."""),
 14:pair("""Power Cycle 後不能只因 NVMe queues 已重建，就推論安全狀態回到未鎖定。以協定的持久設定、session 規則與查詢結果判斷；未指定協定時，結論只能是 NVMe 三份來源未定義。 || Recreated queues do not prove an unlocked security state after power cycle. Apply the selected protocol’s persistent/session rules; absent that choice these NVMe sources do not define one answer."""),
 15:pair("""資料經目標 controller 傳送，但安全操作可能影響一個範圍、namespace 或整個 subsystem；真正範圍由 SECP、SPSP 與 payload 指定的協定決定，不能只看 Admin Queue 所屬 controller。 || The target controller transports data, while protocol selectors/payload determine whether effects reach a range, namespace or subsystem.""")}
COMMON['lockdown_op']={**COMMON['command'],
 9:pair("""Lockdown 成功不定義一個一般性的設定完成 AER。Host 應用 Lockdown Log 與目標命令結果確認；其他獨立事件才依其通知規則處理。 || Lockdown success defines no generic configuration-complete AER. Verify the log and target command behavior; separate events follow their own rules."""),
 10:pair("""Lockdown Log 的目前禁止清單應反映成功操作，並要用相同的介面、scope、controller 與 UUID 選擇比較。被禁止命令的錯誤 CQE 則另依 Error Information 記錄規則關聯。 || Current prohibitions should reflect success under matching interface/scope/controller/UUID selectors; denied commands use ordinary error-log correlation."""),
 11:pair("""Lockdown 命令本身不是專用的標準 PEL 事件。若另外修改 Lockdown Persistence Personality，須按其支援的 personality 事件規則判斷，不能把兩個操作混成同一筆紀錄。 || Lockdown itself has no dedicated standard PEL event. A separate persistence-personality change follows its supported event rules."""),
 12:pair("""成功建立的禁止狀態不因一般 CLR 解除；要允許命令，需合法的後續 Lockdown 操作，或符合指定的 power-cycle 解除條件。 || Ordinary CLR does not remove a successful prohibition; removal requires an allowed subsequent Lockdown or its specified power-cycle condition."""),
 13:pair("""Subsystem Reset 不等於 Power Cycle，不能用它自動解除禁止。仍要保留相同 scope 的狀態，並考慮 personality 明定的例外。 || Subsystem reset is not power cycle and does not automatically remove prohibitions; preserve scope-specific state and explicit personality exceptions."""),
 14:pair("""CSEL=0 的 subsystem 禁止，LDPE=1 時跨 Power Cycle 保留，直到後續操作解除；LDPE=0 則在 Power Cycle 解除。CSEL=1／2 的禁止到 Power Cycle 為止，不因 LDPE=1 就取得跨斷電持續性。 || CSEL0 persists across power cycles only with LDPE1; otherwise power cycle removes it. CSEL1/2 end at power cycle regardless of LDPE."""),
 15:pair("""CSEL 選全部、指定 controller 或指定 primary 的 secondary 群組；IFC 選收命令介面。禁止一個介面不表示其他介面也被禁止；FID scope 只限制對該 FID 的 Set Features，不能誤當成 Get 也自動禁止。 || CSEL selects controllers and IFC the receiving interface. One interface’s prohibition does not cover others; FID scope targets Set Features, not automatic Get prohibition.""")}

def q(n,t,b,o=None): question(n,t,'security_op' if n<242 else 'lockdown_op',['security','lockdown','locklog','lockpersist','idctrl'],b,o)

q(237,"如何確認 Security Send／Receive 與實際協定支援？ || How are Security Send/Receive and protocols discovered?", '''
NVMe 命令支援與特定安全協定支援是兩層能力，先確認前者，才能安全解讀後者的回覆。 || NVMe command support and security-protocol support are separate capability layers.
OACS 描述 controller 的命令能力；協定探索回覆才說明它能處理哪些 SECP。 || OACS describes commands; discovery identifies supported SECP values.
查 Identify.OACS 的 Security Send／Receive 支援，並核對 Commands Supported and Effects。 || Check the OACS support bit and Commands Supported and Effects.
Security Receive 使用 SECP=00h 探索支援協定；這次查詢不需要先送 Security Send。 || Security Receive SECP00h discovers protocols without a prior Security Send.
先探索，再依所選協定配置 SPSP、NSSF 與資料長度，後續 Send／Receive 配對依協定定義。 || Discover first, then encode selectors/lengths and protocol-specific exchange ordering.
NVMe 成功表示命令完成；協定清單指出可繼續使用的安全協定，不表示已完成認證。 || Successful discovery identifies protocols, not authentication success.
Security Receive 指定不支援 SECP 必須 Invalid Field in Command；完全不支援 Opcode 則是另一層命令支援問題。 || Unsupported Receive SECP requires Invalid Field; unsupported Opcode is a different layer.
Identify、效果 Log 與探索結果應一致，但不能因 Opcode 受支援就要求每個 SECP 都成功。 || Command support does not promise every SECP.
先檢查失敗出在 NVMe 命令層，還是選到未支援的安全協定。 || First locate failure at command or protocol selection level.
''')
q(238,"Security Protocol、欄位或資料長度不合法時如何處理？ || How are invalid security selectors or lengths handled?", '''
必須分清外層 NVMe 欄位與內層安全資料，否則容易期待錯的 Status。 || Separate outer NVMe fields from inner protocol data to predict the right response.
SECP、SPSP、NSSF 與 DPTR／長度都屬查證範圍，但 payload 格式由協定定義。 || Selectors, pointers and lengths matter; protocol definitions govern payload validity.
先查 SECP 探索結果與 NVMe 命令支援，再選具體協定。 || Establish supported commands and protocols before forming a request.
Receive 的 AL 與 Send 的 TL 依 Security Protocol In／Out、INC_512=0 的定義使用；不能當成 NVMe 一般 zero-based Dword 數。 || AL/TL follow Security Protocol In/Out with INC_512=0, not generic zero-based Dword counts.
先核對 NVMe 欄位與 buffer 長度，再解析協定內容；NSSF 只在 EAh 的指定用途下有定義。 || Validate outer fields/buffer before payload; NSSF is defined for specified EAh uses.
合法傳輸取得對應資料或協定回覆；應按協定結果決定認證或安全操作是否成功。 || Valid transport returns protocol results that separately establish security success.
Receive 不支援 SECP、Send 使用保留 SECP 須 Invalid Field。內層認證失敗可能以協定 payload 表示，不能全部改寫成 Invalid Field 或 Access Denied CQE。 || Unsupported Receive/reserved Send SECP requires Invalid Field; inner authentication failure may be a protocol result rather than those CQE statuses.
對同一測試記錄外層 CQE 與內層 result，避免把兩者混為一個錯誤碼。 || Preserve both outer CQE and inner result.
先檢查 AL／TL 單位與實際 buffer 是否足夠，而不是直接猜密碼錯誤。 || First check lengths and buffer capacity before diagnosing credentials.
''')
q(239,"Security 資料傳輸失敗應如何區分 Status 與協定錯誤？ || How are security transfer and protocol failures distinguished?", '''
資料根本沒有正確傳送，與資料送到後協定拒絕，是不同故障階段。 || Failed transport differs from a protocol rejecting successfully delivered data.
先看 NVMe 命令，再看所選安全協定；同一個安全動作可能涉及多筆 Send／Receive。 || Analyze command transport before the multi-command protocol exchange.
保存完整 SQE、DPTR、長度、CQE 與有效的 Receive payload。 || Preserve SQE, pointers, length, CQE and valid receive payload.
Data Transfer Error 表示命令資料傳輸問題；安全結果可能另外以協定欄位回報，不能只靠字面上的「Security」決定 Status。 || Data Transfer Error concerns data movement; security outcomes may be encoded separately in protocol fields.
先檢查 CQE 是否允許信任回傳資料，再依協定解碼；失敗傳輸的舊 buffer 內容不能當新回覆。 || Establish valid returned data before decoding; stale buffers after transfer failure are not new results.
成功 CQE 只證明該 NVMe 命令成功完成，還需讀協定結果才知道操作是否獲准。 || A successful CQE still requires protocol-result interpretation.
未支援欄位、傳輸錯誤、內部錯誤與認證拒絕各有不同前提；沒有「所有安全失敗都回同一 Status」的規則。 || Unsupported fields, transfer failures, internal errors and authentication rejection have distinct premises.
將兩層結果與先後順序對回原始 request，避免讀到上一個 exchange 的結果。 || Correlate both layers and sequence to the intended exchange.
先檢查是不是把成功傳輸的「協定拒絕」誤認成 DMA 失敗。 || First distinguish protocol rejection from DMA failure.
''')
q(240,"Security 狀態如何影響其他 Admin Command？ || How can security state affect other Admin commands?", '''
安全協定可能限制其他操作，但不能用一個抽象的「Locked」推論所有 Admin 都被禁止。 || Security policy may restrict operations, but an unspecified Locked state does not prohibit every Admin command.
影響範圍由協定、保護對象與 NVMe 明定互動共同決定。 || Protocol, protected objects and explicit NVMe interactions determine scope.
確認實際 SECP／安全狀態、Lockdown Log，以及適用的 Security Personality 設定。 || Identify the actual protocol/state, Lockdown log and applicable personality settings.
Security Send／Receive 傳送協定；Lockdown 是另一个命令禁止機制；Namespace Write Protection 又控制另一種存取狀態。 || Security transport, Lockdown and Namespace Write Protection are distinct mechanisms.
先判斷被拒命令與範圍，再確認哪一項機制要求拒絕，最後對照該機制指定的 Status。 || Identify command/scope, the denying mechanism and its specified response.
被允許的查詢仍可能正常運作；解除一種限制不保證其他限制一起解除。 || Permitted queries may continue, and removing one restriction need not remove others.
不能把所有拒絕都要求回 Command Prohibited by Lockdown；只有符合 Lockdown 條件才使用該通用 SC23h。 || Generic SC23h applies to Lockdown, not every security denial.
原始協定回覆、Lockdown 清單與命令行為要分層吻合，不能混用安全狀態名稱。 || Correlate each mechanism separately with observed behavior.
先指出是哪一個具體機制阻擋命令，再談解鎖與重試。 || First identify the precise denying mechanism before unlock/retry reasoning.
''')
q(241,"Reset 與 Power Cycle 後 Security 狀態是否保留？ || Does security state survive reset or power cycle?", '''
原問題必須指定「哪個安全協定的哪個狀態」，才會有可驗證的保留答案。 || A testable answer requires a particular protocol and state.
長期金鑰、持久鎖定設定、暫時 session 與待取的 Receive 資料，不是同一種狀態。 || Keys, persistent policy, sessions and pending receive data have different lifetimes.
記錄 SECP、協定版本、操作前狀態與 Reset 來源；三份 NVMe 規格只提供其明定的傳輸邊界。 || Record protocol/revision/state and reset source; the three NVMe specs define only their stated transport behavior.
Base 明定失聯或 CLR 可能不保留 Security Receive 資料；這不等於永久設定被擦除。 || Base permits loss of receive results after communication loss/CLR, not automatic erasure of persistent security settings.
恢復後重新建立需要的交換並查詢狀態，再依協定確認是否需重新認證。 || Recover communication, query state and reauthenticate if the selected protocol requires it.
正確結果是符合已指定協定的保留規則，而不是所有狀態一律保留或一律清空。 || Correctness follows selected protocol retention, not universal keep/clear behavior.
協定未指定時，不得捏造固定 Status、解鎖結果或金鑰處理；應明確標示來源未定義的部分。 || Without a protocol, do not invent statuses, unlock results or key handling; state the specification boundary.
把傳輸重新初始化、session 重建與持久設定驗證拆成三項，比單看命令成功更可靠。 || Verify transport, session and persistent state separately.
先檢查題目中的「Security 狀態」究竟指哪個欄位或協定物件。 || First identify the exact field or protocol object meant by security state.
''')
q(242,"Lockdown 如何限制指定 Command 或 Feature？ || How does Lockdown restrict commands or features?", '''
Lockdown 限制命令在選定介面與 controller 執行，用來控制管理入口；它不是加密資料或設定 namespace 唯讀。 || Lockdown controls execution at selected interfaces/controllers, not encryption or namespace write protection.
CSEL=0 選 subsystem，1 選指定 controller，2 選指定 primary 的 secondary 群組；IFC 另選收命令的介面。 || CSEL selects subsystem, controller or a primary’s secondaries; IFC selects the receiving interface.
查 OACS.CFLS／CCFLS 與 LID14h 的可禁止清單；哪些 Opcode／FID 可禁止由實作宣告。 || Check CFLS/CCFLS and the prohibitable list, which is implementation-defined.
CDW10.SCP 選 Admin Opcode 或 Set Features FID，OFI 指目標，PRHBT=1 禁止、0 允許；CDW14.CSS 選 controller，必要時 UIDX 選定義。 || SCP/OFI select opcode or FID, PRHBT controls prohibition, and CSS/UIDX select target controller/definition.
先查能力與清單，再送 Lockdown，等成功後讀目前禁止清單，最後以相同介面驗證目標命令。 || Discover, apply, await success, read current prohibition and test the matching interface.
成功後選定目標受限制；重複禁止已禁止項目，或允許已允許項目，都不是錯誤。 || Successful scope enforcement is idempotent for repeat prohibit/allow operations.
不可禁止項目必須回命令特定 Prohibition of Command Execution Not Supported；不支援 CCFLS 卻指定非零 CSEL 須 Invalid Field。 || Nonprohibitable targets require the command-specific prohibition-not-supported status; unsupported nonzero CSEL requires Invalid Field.
一個 FID 被禁止是阻止 Set，不是同時禁止 Get；也不等於 Set Features 全部 Opcode 被禁止。 || Prohibiting one FID targets Set, not Get or necessarily the entire Set Features opcode.
先核對 SCP、OFI、CSEL、CSS 與 IFC 五個選擇是否對到同一個測試目標。 || First align scope, target, controller selection and receiving interface.
''')
q(243,"執行被 Lockdown 禁止的命令或 Feature 應如何回應？ || What response is required for a prohibited command or feature?", '''
成功設下禁止後，還要驗證目標操作真的被阻擋，不能只看到設定命令成功就結束。 || Verify actual enforcement after successful configuration.
條件包含目標 controller、收到命令的介面、Opcode 或 Set FID，以及適用 UUID。 || Match controller, receiving interface, opcode/FID and applicable UUID.
讀目前禁止清單，並確認原 Lockdown 的 CQE 與所選範圍。 || Read current prohibitions and confirm the successful setting/scope.
Admin SQ 上收到符合禁止條件的命令，必須中止並回 Command Prohibited by Command and Feature Lockdown，SCT=0、SC=23h。 || A prohibited command received on the Admin SQ shall abort with SCT0/SC23h.
先成功建立禁止，再送一筆其餘參數合法的目標命令，最後查 CQE 及操作是否未執行。 || Apply the restriction, submit an otherwise-valid target command and verify denial/no execution.
驗證中的預期成功，是禁止生效而目標命令被拒絕；不是要求目標也回 Successful Completion。 || Test success means enforcement, not successful execution of the denied command.
Lockdown 命令自己不被支援或參數非法，與已禁止的目標命令被拒絕，是不同 Status。Personality 的 CDP Authentication 明定例外也要保留。 || Configuration failures differ from target denial; preserve explicit CDP Authentication exceptions.
LDPE 啟用且符合 authenticated unfreeze 支援條件時，指定 CDP Authentication 的 Security Send／Receive 必須允許，即使先前被禁止。 || With enabled persistence and the required authenticated-unfreeze support, CDP Authentication Send/Receive remains allowed despite prior prohibition.
先檢查是否測到錯誤介面、錯誤 controller，或規範明定的允許例外。 || First check target/interface and explicit exceptions.
''')
q(244,"Lockdown Log 的一般與增強格式如何解讀？ || How are normal and enhanced Lockdown logs interpreted?", '''
Log 分開回報「可以禁止」與「目前禁止」，這兩份清單不能互換。 || The log distinguishes prohibitable capability from current prohibitions.
一般格式的部分清單描述全體 controller；增強格式可指定單台或以 FFFFh 彙整至少一台回報的項目。 || Normal lists can describe all controllers; enhanced lists can select one or aggregate entries reported by at least one.
查 CFLS、CCFLS；ELPF=1 需要 controller-scoped 支援，LSI.CNTLID 只在增強格式使用。 || Enhanced ELPF1 requires CCFLS; LSI.CNTLID is used only there.
LSP.CNTTS=0 可禁止、1 Admin 已禁止、2 帶外已禁止；SCP 選 Opcode／FID。一般 LNGTH 是 bytes 數；增強依 SZE、NCFID、CFIDS 解析 descriptors。 || CNTTS chooses capability/Admin/OOB prohibition; SCP selects identifiers. Normal LNGTH counts bytes; enhanced sizes/counts govern descriptors.
先確定查詢條件，再檢查 Header 回報的 CS／SS。增強 FFFFh 清單中 ACNTL=1 表示全體，0 表示至少一台但非全體。 || Match returned selectors; in the enhanced aggregate, ACNTL1 means all and 0 some but not all.
例如兩台中只有 controller1 禁止 FID12h，增強彙整可列它且 ACNTL=0；不能因此說「沒有禁止」。 || If only controller1 prohibits FID12h, an aggregate entry with ACNTL0 means partial coverage, not no prohibition.
不支援 CCFLS 卻要求增強格式須 Invalid Field；不能把每份增強 Log 固定當成 512 bytes。 || Unsupported enhanced format requires Invalid Field; enhanced log length is not universally 512 bytes.
以特定 controller 查詢驗證彙整清單，再比較實際命令，避免把聯集誤看成交集。 || Compare per-controller results and behavior to distinguish union from intersection.
先檢查 ELPF 與 CNTLID，確認使用的是哪一種全體／部分語意。 || First identify format and controller selector before interpreting coverage.
''')
q(245,"Reset 與 Power Cycle 後 Lockdown 是否保留？ || Does Lockdown survive resets and power cycles?", '''
持續性取決於 CSEL 與 Lockdown Persistence，不能只用「Lockdown 已啟用」一個布林值判斷。 || Retention depends on CSEL and persistence settings, not one Lockdown-enabled flag.
先區分 subsystem 禁止與指定 controller／secondary 群組禁止。 || Separate subsystem prohibitions from selected-controller/group prohibitions.
保存原 Lockdown 的 CSEL、PRHBT、IFC 與目標，並讀 Personality 的實際 LDPS。 || Preserve original selectors and read actual personality LDPS.
LDPE 是設定輸入，LDPS 是回覆狀態；前者寫入不等於後者必然已成功生效。 || LDPE is requested input and LDPS returned state; submission does not establish success.
重設前讀清單，執行指定種類的 Reset 或 Power Cycle，再以相同 selector 讀回並驗證目標命令。 || Snapshot, perform the specified reset/power cycle and repeat the same query/behavior checks.
一般 Reset 保留禁止；Power Cycle 後 CSEL0 依 LDPS 保留或解除，CSEL1／2 不取得跨斷電持續性。 || Ordinary reset retains restrictions; power-cycle behavior depends on scope and persistence, with no CSEL1/2 persistence extension.
不能因 Subsystem Reset 沒解除就當作失敗，也不能因 LDPE=1 就要求所有 controller-scoped 禁止跨斷電存在。 || Neither retention after subsystem reset nor loss of controller-scoped restrictions after power cycle is automatically a failure.
同時核對範圍、實際 personality 狀態與重設種類，才能得出唯一預期。 || Scope, actual personality state and reset type jointly determine the expectation.
先檢查是否把 Controller Reset、Subsystem Reset 與真的斷電混稱為 Reset。 || First distinguish the three actual reset/power actions.
''')
