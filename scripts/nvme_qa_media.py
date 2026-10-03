"""Q268–275: ownership, placement and observable media information."""
from scripts.nvme_qa_extension import question
from scripts.nvme_qa_model import REFS
REFS['fdpmodel']='B|3.2.4, 8.1.12|110-113,674-678|70–72, 730–732'
REFS['fdpcontrol']='B|5.2.13.1.29–5.2.13.1.32, 5.2.30.1.21–5.2.30.1.22, 7.3–7.4|319-327,506-509,594-597|293–303, 499–506, 650–657'
REFS['fdpnvm']='N|3.2, 4.1.4.6–4.1.4.7|26,79|21, 116'

def q(n,t,b,o=None):question(n,t,'log_query',['capacitymodel','mediaunit','fdpmodel','fdpcontrol','fdpnvm','idctrl','idns','idlist','ana'],b,o)

q(268,"Domain、Set、Group、Media Unit 與 Namespace 是單一層級嗎？ || Do domains, sets, groups, media units and namespaces form one hierarchy?",'''
這些名稱描述不同觀點：Domain 是管理與通訊邊界，Group 管耐用度，Set 組織容量，Namespace 提供邏輯位址，FDP 則決定資料放置。 || These names represent management, endurance, capacity, logical addressing and data-placement views.
支援 Set 時，namespace 位於一個 Set，Set 位於一個 Endurance Group，Group 位於一個 Domain；Reclaim Group 不是再插入這條鏈的一層 namespace 容器。 || With sets, namespace→set→endurance group→domain is ownership; a reclaim group is not another namespace container inserted into that chain.
讀 CTRATT、各 Identify List、Namespace 歸屬及 FDP Configurations，不從名詞相似推測支援。 || Read capabilities, inventories, namespace membership and FDP configurations.
Media Unit 是規範提供的媒體資訊單位；Reclaim Unit 是 FDP 的回收單位，兩者不能直接畫上等號。 || A media unit is a reported media-information entity; an FDP reclaim unit is a reclamation entity, not necessarily the same object.
先畫管理歸屬，再另外畫 Placement Handle 如何選到 RUH 與 RU。兩張圖各自回答「屬於誰」和「放在哪裡」。 || Draw ownership separately from placement-handle selection; they answer membership and placement respectively.
可以說明一個 namespace 的歸屬，以及它的資料如何透過 FDP 放到所選資源，而不虛構一對一關係。 || Explain both ownership and placement without inventing one-to-one mappings.
Media Unit 不保證等於一顆 die；Channel 與 Media Unit 的關係也不能一律當成單一路徑。 || A media unit is not guaranteed to be a die, nor is channel membership universally one-to-one.
對照各 ID 的定義、有效範圍及查詢時點；相同數值出現在不同 ID 欄不表示同一物件。 || Compare identifier definitions, scopes and observation times rather than numeric equality.
先檢查圖上每條連線代表包含、歸屬還是動態參照。 || First label every edge as containment, ownership or a dynamic reference.
''')
q(269,"如何取得 Domain 與資源歸屬？ || How are domains and resource ownership discovered?",'''
在多 Domain 裝置中，先確定查詢視角，才知道容量與資源清單涵蓋哪個範圍。 || Establish the observation domain before interpreting resource and capacity inventories.
Domain 可以沒有 controller，也可以沒有 Endurance Group，不能只靠目前看得到的 controller 數量推算所有 Domain。 || A domain can contain no controller or no endurance group; visible controllers do not enumerate all domains.
查 CTRATT.MDS、Identify Controller 的 Domain 資訊，以及 Domain、Endurance Group、Set 清單。 || Read MDS, controller domain information and domain/group/set inventories.
Identify Namespace 的 ENDGID、NVMSETID 描述歸屬；Media Unit Status 的 DID、ENDGID、NVMSETID 則提供媒體端關係。 || Namespace membership and media-unit DID/group/set fields provide complementary ownership views.
先取得有效 DID，再列資源與 namespace，將每筆紀錄的 controller 和 DID 一起保存。 || Enumerate valid domains and resources, preserving controller and DID with each observation.
同一張對照表能回答某 namespace 使用哪個 Group，以及查到的容量屬於哪個 Domain。 || A joined view identifies the namespace’s group and the domain owning the reported capacity.
LID10h 的 LSI.DID=0 指目前 controller 所在 Domain；非法非零 DID 必須回 Invalid Field，不能悄悄查另一個 Domain。 || LID10h DID0 selects the controller’s domain; an invalid nonzero DID requires Invalid Field.
單 Domain 與多 Domain 的零值定義不同，需搭配 MDS 判讀；不要把缺少跨 Domain 資訊當成該資源不存在。 || Interpret zero with MDS and distinguish unavailable cross-domain information from absent resources.
先看查詢是送到哪個 controller，以及 selector 是否明確指定 Domain。 || First check the endpoint and domain selector.
''')
q(270,"Reclaim Group、Reclaim Unit 與 RU Handle 各代表什麼？ || What are a reclaim group, reclaim unit and reclaim-unit handle?",'''
FDP 讓 Host 表達資料放置意圖，controller 仍負責實際回收及更換使用中的 RU。 || FDP conveys placement intent while the controller manages reclamation and active-RU replacement.
FDP 配置以 Endurance Group 為範圍；RG 與 RUH 的 ID 只在該配置中有意義。 || FDP configuration is endurance-group scoped; RG/RUH identifiers belong to that configuration.
讀 LID20h 的 NRG、NRUH 與 RUH descriptors，再查 FID1Dh 是否啟用及所選配置。 || Read configuration counts/descriptors and the enabled configuration through FID1Dh.
RG 收納可回收的 RUs；一個 RUH 在每個 RG 各參照一個 RU。同一 RU 同時最多由一個 RUH 參照。 || An RG contains RUs; each RUH references one RU in every RG, while an RU has at most one current RUH reference.
Host 先選 RG 與 Placement Handle，再由 handle 對到 RUH。當目前 RU 用滿，controller 在同一 RG 換成另一個空 RU。 || Select RG and placement handle, map to RUH, and let the controller replace a full RU within that RG.
教學例：RUH2 可同時參照 RG0 的 RU甲與 RG1 的 RU乙；只給 RUH2 還不能唯一指定這兩者之一。 || Example: RUH2 references one RU in RG0 and another in RG1; RUH2 alone does not select between them.
Initially Isolated 與 Persistently Isolated 對回收時混放資料的要求不同，不能只靠 RUH 編號推論永久隔離。 || Initially and persistently isolated handles have different reclamation mixing requirements.
將所選配置、RG、RUH 類型與目前狀態一起比對；RUH ID 固定不代表其參照的 RU 永遠不變。 || Correlate configuration, RG, handle type and state; a stable RUH ID does not imply a fixed RU reference.
先檢查是否把 handle 當成實體 RU 位址。 || First check whether a handle was mistaken for a physical RU address.
''')
q(271,"Namespace 如何透過 Placement Handle 選擇 RU？ || How does a namespace select an RU through a placement handle?",'''
Namespace 使用自己的 Placement Handle 清單，將 Write 中的放置意圖轉成 Group 內的 RUH。 || A namespace’s placement-handle list maps write placement intent to group-level RUHs.
同一 PH 數值在不同 namespace 可以對到不同 RUH；不同 namespaces 也可能共用 RUH，須符合配置限制。 || The same PH can map differently across namespaces, while sharing RUHs is possible under configuration constraints.
讀 namespace 的 handle 清單、FDP 配置與 I/O Management Receive 的 RUH Status。 || Read namespace handle mapping, configuration and RUH status.
Write 的 DTYPE=02h 啟用 FDP 指示，DSPEC 的 PID 包含 RGID 與 PH；PID 裡不是直接填 RUH ID。 || FDP writes use DTYPE02h and a DSPEC PID encoding RGID plus PH, not a raw RUH ID.
先解 PID，再以 PH 查出 RUH，最後用 RGID 找到該 RUH 在所選 RG 目前參照的 RU。 || Decode PID, map PH to RUH and select that handle’s current RU in the chosen RG.
例如 NS1 的 PH0 對 RUH2、PID 選 RG1，就使用 RUH2 在 RG1 的目前 RU；不是 RUH0。 || If NS1 PH0 maps to RUH2 and PID selects RG1, placement uses RUH2's current RU in RG1.
Write 的 PID 非法時，controller 必須改選可存取的 RG／RUH，並依啟用設定記 Invalid PID 事件；RUH Update 的非法參數不能套用相同容錯。 || Invalid write PID requires fallback placement and enabled-event handling; invalid RUH Update selectors do not use that fallback rule.
未使用 FDP Directive 的 Write 走 PH0 與 controller 所選 RG；不能因此宣稱完全繞過 FDP 配置。 || Writes without the directive use PH0 and a controller-selected RG, not a bypass of FDP configuration.
先檢查 DSPEC 解碼及 namespace 的 PH→RUH 對照，再看媒體結果。 || First verify PID decoding and the namespace-specific PH-to-RUH mapping.
''')
q(272,"Media Unit Status Log 提供哪些資訊，如何走訪描述資料？ || What does Media Unit Status report and how are descriptors traversed?",'''
這份 Log 用來查看 Domain 中媒體單位的歸屬、容量調整與耗損資訊，不是逐筆 I/O 的完成紀錄。 || This log reports domain media ownership, adjustment and wear, not per-I/O completion.
LID10h 以 LSI.DID 選 Domain；Media Unit ID 與 Channel ID 的唯一性範圍是 Domain。 || LID10h selects a domain; media-unit and channel identifiers are domain-local.
查 Supported Log Pages 與 Domain 支援，再取得 Header 的 NMU、CCHANS、SELC。 || Check log/domain support and header counts/configuration.
描述資料包含 MUID、DID、ENDGID、NVMSETID、CAF、AVSP、PUSED、MUCS 與 CIO；CIO 指向 Channel 清單，MUCS 是清單筆數。 || Descriptors provide identity, ownership, adjustment, spare/wear and channel-list location/count.
以 CIO 找清單起點，以 MUCS×2 bytes 讀 Channel IDs；有 Channel 清單時，描述資料長度由 CIO 加清單長度推算，不能固定每筆都是同樣大小。 || Locate the channel list at CIO and read MUCS two-byte IDs; applicable descriptor length is CIO plus list length, not a universal fixed stride.
Channel IDs 需按順序讀取；CCHANS=0 表示未回報共同 Channel 數，不能直接當作裝置沒有 Channel。 || Parse ordered IDs; CCHANS0 means the common-channel count is unreported, not no channels exist.
SELC=0 代表已清除容量配置時，Group、Set、CAF 與 Channel 數等欄須依其清零規則解讀，不能當作一般已配置狀態。 || Cleared capacity configuration has specified zero fields and is not an ordinary populated configuration.
Media Unit 的 AVSP、PUSED 與 Endurance Group 健康值之間，規範沒有要求簡單平均關係。 || The specification does not define group health as a simple average of media-unit values.
先檢查 DID 與描述資料邊界，避免第一筆長度算錯後讓後面所有欄位位移。 || First check domain selection and descriptor boundaries.
''')
q(273,"能從 Media Unit Status 直接判斷 Namespace 不可用嗎？ || Can Media Unit Status directly establish namespace unavailability?",'''
原題假設 Media Unit 有一個可直接轉成 Namespace Ready 的不可用狀態；LID10h 沒有提供這種通用對應。 || The original premise assumes a universal media-unavailable-to-namespace-ready mapping that LID10h does not provide.
媒體耗損、namespace 存取狀態與某條 controller 路徑是否可用，是不同觀察範圍。 || Media wear, namespace accessibility and controller-path availability are distinct observations.
查 namespace 歸屬、controller Ready、適用 ANA 狀態及實際命令結果；Media Unit Log 只補充媒體資訊。 || Combine membership, controller readiness, applicable ANA and command results, using media-unit data as context.
PUSED 估算耐用度消耗，AVSP 描述 spare；兩者都不是 Namespace Not Ready 的直接編碼。 || Percentage used estimates endurance consumption and spare reports reserve; neither directly encodes Namespace Not Ready.
先確認 namespace 已附加且路徑允許存取，再觀察合法命令失敗原因，最後才查共享媒體是否能解釋影響範圍。 || Establish attachment/path access, inspect a valid command’s failure and then correlate media ownership.
PUSED 超過 100 不等於所有讀寫必須失敗；裝置仍可依其實際能力繼續服務。 || Percentage used above100 does not require all I/O to fail.
Namespace Not Ready、ANA Inaccessible 與媒體錯誤分屬不同原因，應按實際條件與對應 Status 判斷。 || Namespace Not Ready, ANA Inaccessible and media errors have different conditions and statuses.
若多個 namespaces 同時受影響，檢查共用的 Group、Set 或 controller，仍不能只憑同時發生就證明因果。 || Correlate shared resources for simultaneous failures without treating coincidence as proof.
先保存失敗命令的 SCT／SC 與 namespace 路徑狀態。 || First preserve completion status and namespace-path state.
''')
q(274,"媒體狀態變化會產生哪些通知與紀錄？ || Which notices and records can accompany media changes?",'''
規範沒有通用的「Media Unit 任一欄變更」AER。必須先辨識實際變化屬於健康警告、ANA、namespace 屬性還是 FDP 事件。 || There is no generic AER for every media-unit field change; classify health, ANA, namespace or FDP changes first.
警告可能屬於 Endurance Group、subsystem，或僅屬於某 controller 的路徑；這些通知不能互相代替。 || Warnings can be group, subsystem or controller-path scoped and are not interchangeable.
讀 AEC、FID18h、FDP Event 設定與對應支援位元。 || Read AEC, group-health and FDP-event enables with capability bits.
SMART／Endurance Group Logs 提供警告，ANA Log 提供路徑狀態，FDP Events 記錄已啟用的放置事件。 || Health logs report warnings, ANA reports paths and FDP logs enabled placement events.
先保存 AER 的 Type、Information、LID，再讀相符 Log；需要保留事件時使用 RAE=1。 || Preserve AER type/information/LID, then read the matching log with RAE1 when retention is needed.
例如某 Group spare 低於門檻，應檢查 EGCW 與已啟用的 aggregate notice，而非期待一個 Media Unit Lost 事件。 || A group spare warning calls for EGCW and configured aggregate notice, not an invented Media Unit Lost event.
沒有事件前，先排除未啟用、沒有掛 AER、已被別的讀取確認，或變化根本不符合事件條件。 || Before declaring a missing event, check enables, pending AERs, prior acknowledgments and qualifying conditions.
PEL 只有在支援且符合指定事件時記錄；不能要求每次 PUSED 更新都新增事件。 || PEL records supported qualifying events, not every percentage-used update.
先確定「哪個欄位如何改變」，再找規範定義的事件。 || First specify the actual field transition before selecting an event rule.
''')
q(275,"如何辨識管理實體的 Scope，避免混用 ID？ || How are entity scopes distinguished without confusing identifiers?",'''
相同數字可以同時是 NSID、DID、ENDGID 或 RGID；完整識別需要欄位種類與其所屬範圍。 || The same number can identify a namespace, domain, group or reclaim group; field type and enclosing scope are essential.
操作的命令入口、設定的範圍與資料的歸屬可能不同。 || Command endpoint, configuration scope and data ownership can differ.
先查命令／Feature 的 scope，再用 Identify 和相關清單解析指定 ID。 || Establish command/feature scope before resolving identifiers through inventories.
記錄 controller ID、Domain、Group、Namespace 與命令 selector；不適用的欄位明確留空，不填猜測的0。 || Record applicable endpoint, domain, group, namespace and selectors without inventing zero IDs for inapplicable fields.
逐步回答「送給誰、指定誰、誰會一起受影響」，再選擇跨 controller 的比對對象。 || Ask who receives it, who is targeted and who shares the effects before cross-controller comparison.
例如 FDP 的 FID1Dh 以 Group 為範圍；同 Group 的 namespaces 共用配置，但各自 PH 清單仍不同。 || FID1Dh is group-scoped while namespaces retain distinct placement-handle mappings.
不存在 ID、未支援功能與無法取得跨 Domain 資訊，不能全部用同一種錯誤解釋。 || Absent IDs, unsupported functionality and inaccessible cross-domain information are distinct conditions.
同一物件的比較需保持 selector 與時間一致；若管理操作途中改變歸屬，先重新探索。 || Compare matching selectors/times and rediscover after ownership changes.
先把所有未標種類的裸數字補上欄位名稱與上層範圍。 || First qualify every bare number with its field and enclosing scope.
''')
