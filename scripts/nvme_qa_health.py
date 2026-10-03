"""Q188–204: power transitions, thermal control and health accounting."""
from scripts.nvme_qa_extension import question
from scripts.nvme_qa_model import COMMON, REFS, pair

REFS['powerdetail']='B|8.1.19.1–8.1.19.5|692-697|738–741'
REFS['psd']='B|5.2.14.2.1 (Power State Descriptor)|410-413|340–341'
COMMON['power_config']={**COMMON['command'],**COMMON['feature'],
 9:pair('切換 Power State 或開始降速，不會自動產生同名的 AER。若溫度另外達到已設定的警告條件，才依 SMART／Health 事件與通知設定回報；HCTM 的 TMT1、TMT2 不是 Temperature Threshold Feature 的同一組門檻。 || A power-state transition or throttling action does not itself define an AER. Temperature warnings use SMART/Health event conditions and configuration; HCTM TMT1/TMT2 are distinct from Temperature Threshold feature limits.'),
 10:pair('SMART 的 Thermal Management transition count 與累計時間可協助確認 HCTM 行為；一般 Power State 切換沒有逐次記錄的標準 Log。成功設定不要求 Error Information entry，設定失敗時才依 CQE 與記錄條件查證。 || SMART thermal transition counts and accumulated times help verify HCTM. There is no generic per-transition power-state log. Successful configuration requires no error entry; failures follow CQE and logging rules.'),
 11:pair('若支援 PEL 的 Set Feature Event，先確認該 FID 可記錄且已宣告支援。符合條件的設定變更依規則記錄；自動進入 Power State 或每次降速，不等於又執行一次 Set Features。 || For supported PEL Set Feature events, verify that the FID permits and supports logging. Eligible setting changes are recorded; automatic state transitions and throttling are not additional Set Features commands.')}

def q(n,t,r,b,o=None):
 question(n,t,'power_config' if n<196 else 'log_query',r+['smart','powerdetail','psd','power','thermal','aec','feature','setfeat'],b,o)

q(188,'Power State Descriptor 能告訴 Host 哪些事情？ || What does a Power State Descriptor tell the host?', [], '''
Host 需要在功耗、效能與喚醒時間之間選擇。Descriptor 提供可比較的狀態資料，但不是保證每一筆命令都在相同時間內完成。 || The host trades power against performance and wake latency. Descriptors characterize states, not the completion time of every command.
每個 controller 依 NPSS 提供 PS0 到 PSn；NPSS 採 zero-based 編碼，例如 4 代表 5 個狀態。 || NPSS enumerates controller states PS0 through PSn; a value of 4 means five states.
先確認 Power Management 適用於此 controller，再查 NPSS 與各筆 PSD。對不支援此功能的 controller，Host 應忽略 PSD。 || Establish Power Management applicability, then inspect NPSS and PSDs; ignore PSDs for a controller without support.
NOPS 區分工作與非工作狀態；MP 配合功率尺度，ENLAT／EXLAT 以微秒描述進出延遲。RRT、RRL、RWT、RWL 是相對效能排序；IDLP、ACTP 各有尺度與量測條件，MBW 配合 MBWS 表示宣告的最高頻寬。 || NOPS classifies the state; MP uses its scale; ENLAT/EXLAT are microseconds. Relative performance ranks differ from scaled idle/active power and MBW/MBWS bandwidth.
先比較 NOPS 與最大功率，再比較進出延遲，最後以相同種類的相對效能欄位排序。不同欄位的數字不能交叉比較。 || Compare class and power, then transition latency, then like-for-like performance ranks.
Identify 成功後，Host 能挑出合適狀態；真正設定仍須透過 Power Management 或 APST。 || Successful Identify supports state selection; Power Management or APST performs selection in operation.
超出 NPSS 的狀態不是合法選項；設定非法 Power State 時應回報 Invalid Field in Command。未宣告的量測值也不能解讀成零功耗或零延遲保證。 || A state beyond NPSS is invalid for selection. Unreported measurements are not guarantees of zero consumption or latency.
把 PSD 的 NOPS、功率尺度與 Feature 選中的狀態一起核對；不要把相對排名當作實際 IOPS。 || Cross-check NOPS, scales and selected state; ranks are not absolute IOPS.
先檢查是否把 NPSS 當成狀態總數，或漏乘功率、頻寬的尺度。 || First check NPSS encoding and power/bandwidth scales.
''')
q(189,'Operational 與 Non-Operational Power State 差在哪裡？ || How do operational and non-operational power states differ?', [], '''
這個分類回答「目前是否準備好處理 I/O」，不是在說 controller 是否完全斷電。 || This classifies I/O readiness, not whether the controller is completely unpowered.
NOPS=0 為工作狀態；NOPS=1 為非工作狀態。非工作狀態仍可能處理 Register、Admin 命令與允許的背景工作。 || NOPS=0 is operational; NOPS=1 is non-operational, while registers, Admin commands and permitted background work may remain active.
查 PSD.NOPS、目前 Power Management 設定與 Non-Operational Power State Config。 || Inspect PSD.NOPS, Power Management and Non-Operational Power State Config.
APST 可自動進入非工作狀態；NOPPME 控制非工作狀態中的背景工作政策，不能當成禁止所有 Admin 存取的開關。 || APST enters non-operational states; NOPPME controls background policy, not all Admin access.
進入非工作狀態後若需處理 I/O，controller 自動回到最近的工作狀態，再處理 I/O；這項恢復不以 APST 是否啟用為前提。 || I/O causes return to the last operational state regardless of APST enablement.
I/O 能在恢復工作狀態後完成；Host 不需先用 Set Features 喚醒每一筆 I/O。 || I/O completes after resumption without a separate Set Features wake command per I/O.
不能因合法 I/O 到達非工作狀態就直接判定命令非法；若指定不存在的 Power State，才是設定參數問題。 || Arrival during a non-operational state is not itself an invalid I/O request; selecting a nonexistent state is a configuration error.
看到非工作狀態期間仍有 Admin 活動或暫時較高功耗，不足以單獨判定違規；須核對允許的操作與功率上限。 || Admin activity or temporary power above the non-operational limit requires examination of permitted operations and applicable power bounds.
先確認測到的是 I/O、Admin 還是背景工作，不能只看「裝置仍有活動」。 || First classify the observed activity as I/O, Admin or background work.
''')
q(190,'Entry 與 Exit Latency 如何影響命令等待時間？ || How do entry and exit latency affect command waits?', [], '''
命令可能必須等狀態切換完成，因此需把轉換時間與命令本身的執行時間分開。 || Separate state-transition delay from command execution time.
ENLAT 描述進入目標狀態，EXLAT 描述離開原狀態；切換路徑涉及多個狀態時，不能只取其中最小值。 || ENLAT applies to entry and EXLAT to exit; a multi-state path cannot be reduced to its smallest value.
讀取原狀態與目標狀態的 PSD；非工作狀態恢復 I/O 時也需知道最近的工作狀態。 || Read source and destination PSDs and the last operational state.
以微秒為單位計算原狀態 EXLAT 加目標狀態 ENLAT。ITPT 則是進入轉換之前的閒置等待時間，單位是毫秒。 || Add source EXLAT and destination ENLAT in microseconds; ITPT is a separate idle delay in milliseconds.
先確認切換開始時間與路徑，量測恢復可處理命令的時間，再另計命令執行與 Host 排程延遲。 || Establish transition timing and path, then measure readiness separately from execution and host scheduling.
例如假設 PS3.EXLAT=2000 μs、PS0.ENLAT=500 μs，這段轉換的宣告上限為 2500 μs；不能要求完整 Read 也一定在 2500 μs 內完成。 || With hypothetical 2000 μs exit and 500 μs entry, the transition bound is 2500 μs, not a bound on the entire Read.
Host 量到較慢的 CQE 不會直接產生一個「Exit Latency Error」Status；必須先證明超時發生在受規範限制的轉換階段。 || A late CQE does not define an Exit Latency Error status; isolate the bounded transition first.
比對 PSD、實際原始狀態、APST 路徑與量測邊界，而不是只比 Read 總延遲。 || Compare PSDs, actual source state, APST path and measurement boundaries.
先檢查微秒與毫秒是否混用，以及是否把媒體讀取時間算進 EXLAT。 || First check units and whether media-read time was incorrectly included in EXLAT.
''')
q(191,'APST 如何設定、觸發與停用？ || How is APST configured, triggered and disabled?', [], '''
APST 讓 controller 在 I/O 閒置時自動降低功耗，Host 不必為每次閒置另送切換命令。 || APST reduces power during I/O idle periods without a host command for every transition.
每個來源 Power State 有一筆 8-byte entry；整份資料有 32 筆，共 256 bytes。 || Each source state has an eight-byte entry; 32 entries occupy 256 bytes.
確認 Identify.APSTA 與 NPSS，並核對目標 PSD.NOPS。 || Check APSTA, NPSS and the target NOPS bit.
FID0Ch 的 APSTE 啟用整體功能；entry.ITPT 指定閒置毫秒數，ITPS 指定目標。ITPT=0 停用該來源狀態的自動轉換。 || APSTE enables FID0Ch; ITPT specifies idle milliseconds and ITPS the destination. ITPT=0 disables that source-state transition.
填好各來源 entry，Set Features，再 Get Features 核對。沒有 outstanding I/O，且連續閒置時間超過 ITPT，才符合這條轉換的觸發條件。 || Set the table and verify it. A transition requires no outstanding I/O and continuous idle longer than ITPT.
例如 PS0 entry 設 ITPT=2000、ITPS=3，低 Dword 為 0007D018h；APSTE=1 時，PS0 閒置超過 2 s 可轉入受支援的非工作 PS3。 || For hypothetical ITPT=2000 and ITPS=3, the low Dword is 0007D018h; with APSTE=1, PS0 can enter supported non-operational PS3 after over two seconds idle.
ITPT 非零時，ITPS 必須是非工作狀態；指定工作狀態應以 Invalid Field in Command 中止。停用整體功能使用 APSTE=0。 || A nonzero ITPT requires a non-operational target; an operational target should cause Invalid Field in Command. APSTE=0 disables APST globally.
Get 回傳的是設定表，不是每次切換的歷史。若背景工作阻止進入較低功耗狀態，還要核對背景功耗與政策。 || Get returns configuration, not transition history; background work and its power policy may prevent entry.
先檢查設定的是「目前來源狀態」那一筆 entry，還是誤把目標狀態當作表格索引。 || First check that the entry index names the source, not destination, state.
''')
q(192,'量到恢復延遲超過 EXLAT，如何判斷是否違規？ || How should an apparent EXLAT violation be evaluated?', [], '''
要判斷韌體是否超過宣告，必須量到相同的事件邊界，不能把 Host 等待時間全部歸給 controller。 || Conformance requires matching measurement boundaries rather than attributing every host delay to the controller.
先限定一個 controller、一條已知狀態路徑與一次喚醒。 || Isolate one controller, a known state path and one wake transition.
保存 PSD、APST、Power Management、溫度與目前背景操作。 || Snapshot PSDs, APST, Power Management, temperature and background activity.
使用原狀態 EXLAT 與目標 ENLAT；若測的是 RTD3，則是另一套供電恢復與初始化條件，不能沿用 NOPS 退出公式。 || Use source EXLAT and destination ENLAT; RTD3 has different power-restoration and initialization conditions.
先排除命令尚未提交、Host 排程、中斷合併及媒體執行時間，再定位真正的轉換區間。 || Exclude submission delay, host scheduling, interrupt coalescing and media execution before measuring the transition.
在前提一致下，量測可支持「轉換符合／超過宣告」；前提不明時，只能說端到端延遲較高。 || Matching premises support a transition compliance finding; otherwise the evidence establishes only high end-to-end latency.
EXLAT 超出不是要求 controller 回傳某個固定 CQE 的命令參數錯誤。 || Exceeding EXLAT is not an invalid-command condition with a mandated fixed CQE.
用重複的受控量測核對宣告上限，保留時間解析度與量測誤差，不用單次應用程式時間直接定罪。 || Use controlled repeat measurements with timing resolution and uncertainty.
先確認延遲起點是否真的代表 controller 開始離開該 Power State。 || First establish whether the start timestamp marks the actual state exit.
''')
q(193,'HCTM 的 TMT1 與 TMT2 應如何設定？ || How should HCTM TMT1 and TMT2 be configured?', [], '''
HCTM 讓 Host 指定希望 controller 採取散熱措施的溫度，並區分較輕與較重的效能影響。 || HCTM supplies host thermal targets for lighter and heavier mitigation.
以 Composite Temperature 作判斷，作用於目標 controller 的熱管理。 || It controls target-controller thermal management using Composite Temperature.
查 Identify.HCTMA、MNTMT、MXTMT；不是所有 controller 都支援 Host 控制熱管理。 || Check HCTMA and the MNTMT/MXTMT supported range.
FID10h 的 CDW11[31:16] 為 TMT1，[15:0] 為 TMT2，單位都是 Kelvin；0 停用對應部分。 || FID10h CDW11[31:16] is TMT1 and [15:0] TMT2, both Kelvin; zero disables the respective part.
將非零門檻設在宣告範圍；兩者皆非零時必須 TMT1<TMT2。Set 成功後 Get 確認，不要直接填攝氏數字。 || Keep nonzero values in range and TMT1<TMT2 when both are enabled; verify by Get and do not encode Celsius directly.
假設允許 300～360 K，設定 330 K 與 340 K 合法；設定 340 K 與 330 K 則顛倒輕重門檻。 || For a hypothetical 300–360 K range, 330/340 K is valid whereas 340/330 K reverses the thresholds.
非零門檻超出範圍，或兩個啟用門檻不符合先後關係，須回 Invalid Field in Command。 || Out-of-range enabled thresholds or invalid ordering require Invalid Field in Command.
Get 的門檻、SMART 溫度與熱管理累計應一起看；溫度警告 FID04h 另有自己的設定。 || Compare thresholds, SMART temperature and thermal counters; temperature-warning FID04h is separate.
先檢查單位、上下 16 bits 的位置與 0 的停用意義。 || First check units, halfword placement and zero-as-disabled semantics.
''')
q(194,'Controller 何時開始或停止 Thermal Management？ || When does thermal management start and stop?', [], '''
門檻決定何時採取措施，但規範沒有替所有裝置指定相同的降速曲線。 || Thresholds trigger action without prescribing one universal throttling curve.
判斷使用 Composite Temperature，而不是任選一個實體 sensor。 || Decisions use Composite Temperature, not an arbitrary physical sensor.
先確認 HCTM 已啟用的門檻，以及 SMART 的 CTEMP、TMT1TC、TMT2TC 與累計秒數。 || Check enabled thresholds, CTEMP, transition counts and accumulated seconds.
TMT1 啟用且溫度達 TMT1、未達啟用的 TMT2 時，controller 應開始較輕措施；達啟用的 TMT2 時，必須採取措施而不受效能影響限制。 || At enabled TMT1 below enabled TMT2, lighter mitigation should begin; reaching enabled TMT2 shall trigger mitigation regardless of performance impact.
追蹤升溫跨越門檻及降溫恢復的過程。恢復溫度有廠商定義的遲滯，不能要求溫度一低於 TMT2 就立即完全恢復。 || Track rising and falling temperature; vendor-specific hysteresis means crossing below TMT2 need not immediately restore full performance.
可觀察到功率或效能調整，且對應 transition count／time 有一致紀錄；實際措施可由廠商決定。 || Observe consistent mitigation and thermal counters; the specific mechanism is vendor-defined.
低於 TMT2 後仍降速，不足以直接判定錯誤；先核對 TMT1、遲滯及其他熱保護來源。 || Continued throttling below TMT2 is not alone a violation; inspect TMT1, hysteresis and other protection mechanisms.
把 should 與 shall 分開檢查，不把輕度門檻的建議要求提高成重度門檻的強制要求。 || Preserve the different should/shall strengths for the two thresholds.
先確認正在生效的是 HCTM，還是裝置自己的其他熱保護。 || First identify whether HCTM or another protection mechanism caused the behavior.
''')
q(195,'Reset 與 Power Cycle 後，Power／Thermal 設定如何恢復？ || How are power and thermal settings restored?', [], '''
要分開「保存的設定」、「目前設定」與「正在發生的熱或電源狀態」，否則容易把正常恢復誤判成設定遺失。 || Distinguish saved configuration, current configuration and live thermal/power state.
逐一檢查 Power Management、APST、HCTM 與 NOPS Config，不能將它們當成一個 Feature。 || Treat Power Management, APST, HCTM and NOPS Config as separate features.
Get Features SEL=3 查保存能力，SEL=0／1／2 分別觀察 Current、Default、Saved；另查 Feature scope。 || Use SEL=3 for capabilities and SEL=0/1/2 for Current/Default/Saved, with scope.
SV=1 的成功 Set 更新 Saved；SV=0 只改 Current。不可保存的 Feature 依明定的持續性恢復。 || Successful SV=1 updates Saved; SV=0 changes Current only. Non-saveable features follow explicit persistence rules.
重設前保存四種查詢結果，重設後先恢復 Admin Queue，再重新 Get，最後檢查狀態轉換是否符合恢復後的設定。 || Snapshot values before reset, recover Admin access, reread settings and then validate resulting behavior.
Current 應等於該範圍與重設條件所要求的恢復值；不是一定等於重設前最後一次 SV=0 的值。 || Current matches the required restored value, not necessarily the last pre-reset SV=0 setting.
不支援 Save 卻要求 SV=1 時，應使用對應 Feature Not Saveable 等明定錯誤；不能把失敗 Set 當成已保存。 || Unsupported saving follows the specified Feature Not Saveable handling; a failed Set does not establish saved state.
SMART 溫度與累計計數不因 Feature 回到 Default 就必須歸零。 || Restoring feature defaults does not imply clearing temperature or lifetime counters.
先檢查最後一次 Set 的 SV、實際 CQE，以及重設是否涵蓋全部共用範圍。 || First inspect SV, the actual CQE and reset coverage.
''')
q(196,'SMART Critical Warning 的各 bit 代表什麼？ || What do SMART Critical Warning bits mean?', [], '''
Critical Warning 提供現在的警告狀態，讓 Host 判斷是否需要處理容量、溫度、可靠性或唯讀問題。它不是永久鎖存的事件歷史。 || Critical Warning reports current spare, thermal, reliability and read-only concerns; it is not a permanently latched history.
每個 bit 獨立，可同時成立；讀取時的狀態可能與先前 AER 產生時不同。 || Bits are independent and may differ from their state when an earlier AER occurred.
讀 SMART LID02h，並核對 AEC 的 SHCW 啟用遮罩與相關硬體能力。 || Read LID02h and check the AEC SHCW enable mask and applicable hardware capabilities.
bit0 備用容量低於門檻；bit1 溫度達上限或下限；bit2 可靠性降低；bit3 全部媒體唯讀；bit4 揮發記憶體備援失敗；bit5 PMR 唯讀或不可靠；bit6 personality 設定處於未定狀態。bit7 保留。 || Bits 0–6 indicate low spare, temperature condition, degraded reliability, all-media read-only, volatile backup failure, PMR read-only/unreliable and indeterminate personality state; bit 7 is reserved.
先找出設為 1 的 bits，再讀對應欄位與事件資訊。例如 bit1 必須核對上、下溫度門檻，不能一律翻成過熱。 || Decode asserted bits and related fields; bit 1 may indicate either over- or under-temperature.
成功讀取回傳目前狀態；多個 bits 為 1 不代表 Log 格式錯誤。 || A successful read returns the current combination; multiple warnings are valid.
Namespace Write Protection 造成的唯讀不得設定 AMRO；備援不存在時，也不能把無效 VMBF 當作故障證據。 || Namespace Write Protection shall not set AMRO; an inapplicable backup bit is not failure evidence.
用警告類型、相應數值及 AER 發生時間互相核對，而不是要求稍後讀到的 CW 永遠等於事件當時。 || Correlate warning type, values and timing rather than requiring later CW to reproduce the event snapshot.
先檢查 bit 定義是否沿用舊版，漏掉 Base 2.4 的 personality 警告。 || First check revision-specific bit definitions, including the personality warning.
''')
q(197,'Available Spare、Threshold 與 Percentage Used 如何解讀？ || How are spare capacity and percentage used interpreted?', [], '''
三個值分別回答「剩多少備援」、「何時警告」與「估計壽命用了多少」，不能拿同一個百分比公式套用。 || These answer remaining spare, warning threshold and estimated life consumed, not one common percentage formula.
SMART 描述所定義的整體健康範圍；它不是 namespace 的剩餘檔案空間。 || SMART health scope is not free filesystem space in a namespace.
讀 AVSP、AVSPT、PUSED 及 CW.ASCBT；需要分組健康時另查 Endurance Group Log。 || Read AVSP, AVSPT, PUSED and CW.ASCBT; use Endurance Group logs for group-level health.
AVSP 與 AVSPT 為 0～100%；AVSP<AVSPT 才是低於門檻。PUSED 是廠商估算，100 不代表當下必然故障，且允許超過 100；大於 254 表示為 255。 || Spare and threshold range from 0–100%; the warning uses strict less-than. PUSED is a vendor estimate; 100 is not proof of failure, values may exceed 100 and values above 254 encode as 255.
例如 AVSP=8、AVSPT=10 表示已低於門檻；PUSED=105 則表示估計耐用額度已用超過，兩者可以同時存在。 || Hypothetical spare 8 with threshold 10 is low spare, while PUSED=105 indicates estimated endurance consumed beyond 100%.
成功讀取取得估計值；PUSED 在非睡眠期間每個 power-on hour 更新一次，不要求每次 Write 立即改變。 || PUSED is updated once per power-on hour outside sleep, not after every Write.
不能因 PUSED>100 判為非法欄位，也不能因 AVSP=AVSPT 就要求「低於」警告。 || PUSED above 100 is legal; equality does not satisfy a below-threshold condition.
交叉比較警告與 AVSP，而不要用 PUSED 直接推算剩餘 spare。 || Compare the warning with AVSP; do not derive spare directly from PUSED.
先確認讀者是否把 Percentage Used 誤當成使用者容量使用率。 || First rule out confusing endurance usage with allocated user capacity.
''')
q(198,'資料量、命令數、Busy Time、Power Cycles 與 Power On Hours 如何累計？ || How do SMART workload and uptime counters accumulate?', [], '''
這些計數用不同單位描述工作量與使用時間；先理解單位，才能比較兩次快照。 || These counters measure different workload and uptime quantities; units precede comparison.
計數涵蓋 SMART 定義的範圍；多條 queue 的重疊工作時間不能直接相加成 Busy Time。 || Use SMART scope; overlapping queue activity is not added repeatedly to busy time.
讀 DUR、DUW、HRC、HWC、CBT、PWR_CYC 與 POH，並保留快照時間。 || Read data units, host command counts, busy time, power cycles and power-on hours with timestamps.
Data Units 以 1000 個 512-byte units 為單位並向上取整，0 表示未回報。Busy Time 以分鐘計，從 I/O 提交 Doorbell 到 CQE 寫入之間有未完成 I/O 即可能計入；不是等 Host 消費 CQE 才結束。 || Data units count thousands of 512-byte units rounded up; zero means not reported. Busy time counts minutes with outstanding I/O from submission doorbell to CQE posting, not host consumption.
以兩次快照算差，再依單位轉換。Host Read／Write Commands 依命令集定義的已完成命令類別累計；POH 可不含非工作狀態的時間。 || Difference two snapshots, convert units and apply command-set classifications for completed reads/user-data-out; POH may exclude non-operational states.
例如資料量欄增加 2，只支持增加約 2×512000 bytes 的量化刻度；短小操作可能因取整而未立即增加。 || A delta of two data units reflects 512000-byte quantization; a small operation need not immediately change the rounded value.
不能用應用程式 I/O 次數要求 Host Command 計數完全相等，因為合併、重試與命令類型可能不同。 || Application request count need not equal NVMe command count because of merging, retries and classification.
核對 controller 真正完成的命令與計數單位，而不是只比檔案大小或壁鐘時間。 || Compare actual completed commands and units rather than only file size or wall-clock time.
先檢查是否漏掉 ×1000、512 bytes、分鐘與小時之間的換算。 || First check the ×1000, 512-byte, minute and hour conversions.
''')
q(199,'Unexpected Power Losses、媒體錯誤與 Error Log Entries 如何累計？ || How do unexpected power-loss and error counters accumulate?', [], '''
這三項分別記錄失電條件、無法恢復的資料完整性錯誤與已產生的 Error Log entries，不能互相代替。 || These count power-loss conditions, unrecovered integrity errors and generated error entries separately.
它們是生命週期累計，不是目前 Log 裡仍保留多少筆紀錄。 || They are lifetime counters, not current log occupancy.
讀 UPL、MDIE、NEILE，並保存失電前 CSTS.SHST 與是否因 OOB 管理而繼續存取媒體。 || Read UPL, MDIE and NEILE alongside pre-loss SHST and any OOB media activity.
Base 2.4 將舊稱 Unsafe Shutdowns 的欄位稱為 Unexpected Power Losses。主電源失去時，SHST 不是 10b，或媒體因適用的 OOB Ignore Shutdown 操作尚未關閉，才符合規定的累計條件。 || Base 2.4 calls the former Unsafe Shutdowns field Unexpected Power Losses. It increments for main-power loss without SHST=10b or with media still active under the specified OOB Ignore Shutdown condition.
先辨認是否真的失去主電源，再判斷當時狀態；另外以未恢復的完整性錯誤核對 MDIE，以實際新增 Error entry 核對 NEILE。 || Establish actual main-power loss and state; separately correlate unrecovered errors with MDIE and generated entries with NEILE.
Reset 而未失電不增加 UPL；完成 Abrupt Shutdown 且符合可斷電狀態後失電，也不能只因「Abrupt」就要求增加。 || Reset without power loss does not increase UPL; completed abrupt shutdown does not alone require an increment.
一次命令失敗不必然同時增加 MDIE 與 NEILE。Write Uncorrectable 引入的錯誤是否計入 MDIE，規範允許實作選擇。 || One command failure need not increase both counters; inclusion of Write Uncorrectable-induced errors in MDIE is implementation-permitted.
Error entries 被覆寫或重設後建議清除，不會讓生命週期 NEILE 倒退。 || Entry overwrite or recommended clearing after reset does not reduce lifetime NEILE.
先檢查測試到底執行 Shutdown、Reset，還是真的切斷主電源。 || First distinguish shutdown, reset and actual removal of main power.
''')
q(200,'Warning 與 Critical Composite Temperature Time 如何累計？ || How are warning and critical temperature times counted?', [], '''
這兩欄描述處於警告或危急溫度區間的累計時間，不是 HCTM 降速次數。 || These accumulate time in warning/critical temperature ranges, not HCTM transitions.
在工作狀態中，依 Composite Temperature 與 WCTEMP、CCTEMP 判斷，單位為分鐘。 || They use operational-state composite temperature against WCTEMP/CCTEMP in minutes.
讀 Identify.WCTEMP、CCTEMP 與 SMART 的 WCTT、CCTT，並確認適用的溫度遲滯設定。 || Read WCTEMP/CCTEMP and SMART WCTT/CCTT, with applicable hysteresis configuration.
WCTT 對應 WCTEMP≤溫度<CCTEMP 的警告區間；CCTT 對應溫度≥CCTEMP。門檻未實作的零值有指定的零回報規則。 || WCTT covers WCTEMP≤temperature<CCTEMP; CCTT covers temperature≥CCTEMP, with zero-report rules for unimplemented thresholds.
按時間序列確認每段工作狀態及溫度區間，再累計；不要把取樣到一次高溫直接算成一整分鐘。 || Determine the duration in each operational temperature range rather than turning one hot sample into a full minute.
假設持續 2 分鐘處於危急區間，應檢查 CCTT 的變化；不能同時要求這 2 分鐘全部加進警告區間。 || For two hypothetical minutes in the critical range, inspect CCTT rather than demanding the same duration in the warning-only range.
WCTEMP 或 CCTEMP 為 0 時，WCTT 為 0；CCTEMP 為 0 時，CCTT 為 0。零值不能一律解釋為裝置從未過熱。 || WCTT is zero if WCTEMP or CCTEMP is zero; CCTT is zero if CCTEMP is zero. Zero does not universally prove no overheating.
另把 HCTM 的累計秒數分開比較，因為門檻、單位與事件意義都不同。 || Keep HCTM seconds separate because its thresholds, units and meaning differ.
先檢查比較的是溫度區間時間，還是 HCTM 動作時間。 || First identify whether the field measures thermal exposure or HCTM action.
''')
q(201,'多個 Temperature Sensor 與 Composite Temperature 如何比較？ || How do sensor temperatures relate to Composite Temperature?', [], '''
多個 sensor 可觀察不同位置；Composite Temperature 是 controller 用於整體判斷的值，不保證等於其中最高、最低或平均值。 || Sensors observe different locations; Composite Temperature need not equal their maximum, minimum or average.
sensor 位置與 Composite 的計算方式由實作定義；跨產品比較前需知道量測意義。 || Locations and composite computation are implementation-specific.
讀 SMART.CTEMP 與 TSEN1～TSEN8，再查看裝置提供的 sensor 對應說明。 || Read CTEMP and TSEN1–TSEN8 and the device’s sensor mapping.
數值以 Kelvin 表示；TSEN=0 表示未實作，不能當成 0 K 的有效溫度。 || Values are Kelvin; a zero TSEN means unimplemented, not a valid 0 K measurement.
先排除未實作欄位，再轉換成需要的單位；例如 300 K 約為 26.85°C。警告門檻要搭配它所選的 sensor。 || Remove unimplemented fields before conversion; 300 K is about 26.85°C. Pair thresholds with their selected sensors.
Get Log 成功可回傳彼此不同的溫度，差異本身不代表資料損壞。 || Different returned temperatures are valid and do not themselves imply corruption.
不能要求所有 TSEN 都非零，也不能因 Composite 不等於平均值就判定違規。 || Not every TSEN must be implemented, and the composite need not be an average.
把警告、門檻所選 sensor 與該 sensor 的數值一起比對。 || Correlate warnings, selected sensor and that sensor’s reading.
先檢查是否將 0 當有效量測，以及是否選錯警告對應的 sensor。 || First check zero validity and sensor selection.
''')
q(202,'哪些 Health 變化會產生 AER？ || Which health changes generate asynchronous events?', ['aerfull'], '''
健康通知讓 Host 不必持續輪詢，但它仍受支援、啟用及事件遮蔽條件限制。 || Health notifications reduce polling but remain subject to support, enablement and masking.
SMART／Health 事件報告規範定義的警告，不是每次溫度或計數變動都發通知。 || SMART/Health events report defined warnings, not every temperature or counter change.
查 AEC.SHCW、SMART.CW、待處理 AER 數量，以及相關溫度或 spare 門檻。 || Inspect SHCW, CW, outstanding AERs and relevant thresholds.
事件類型與資訊指向相應健康條件，LID 通常指向 SMART；Host 依實際 AER 回覆的 LID 讀取資料。 || Event type/information identify the condition; follow the returned LID to the associated health data.
先掛入 AER，再啟用需要的通知；事件發生後保存 CQE，讀對應 Log 並依 RAE 完成確認，再補送 AER。 || Post requests, enable desired notices, preserve event CQEs, read/acknowledge with RAE and replenish requests.
符合通知條件且有可完成的 AER 時，Host 能取得事件；稍後 CW 已恢復不代表先前通知錯誤。 || Eligible events can complete a request; a subsequently cleared CW does not invalidate an earlier event.
沒有 AER Completion 時，不能直接判定韌體漏報；未啟用、已遮蔽或尚無可用 request 都要先查。 || Missing completion requires checking enablement, masking and available requests before alleging omission.
以事件當時設定與條件核對，不只看事後單一 SMART 快照。 || Compare event-time settings and conditions, not only a later snapshot.
先確認 SHCW 對應 bit 已啟用，且前一次同類事件已按規定確認。 || First verify the relevant SHCW bit and acknowledgment of the previous masked event.
''',{9:'本題討論的就是 SMART／Health AER；事件條件、SHCW、遮蔽狀態及 outstanding request 必須一起判斷。普通計數增加不要求另外發送事件。 || This question concerns SMART/Health AERs: evaluate conditions, SHCW, masking and requests together. Ordinary counter increments do not require events.'})
q(203,'SMART 資料的 Scope 如何判斷？ || How is SMART data scope determined?', [], '''
Scope 決定同一組健康數字描述哪個範圍，避免把總體資料當成指定 namespace 的獨立健康。 || Scope identifies what the health values describe and prevents mistaking aggregate data for per-namespace health.
Base 2.4 的 SMART／Health Log 不提供 namespace-specific 資訊；接受不同 NSID 不表示資料因此成為該 namespace 專屬。 || Base 2.4 SMART/Health does not provide namespace-specific information; acceptance of different NSIDs does not create per-namespace data.
查本版 SMART 定義與 Get Log Page 的選擇規則；需要 Endurance Group 資料時改查相應 Log。 || Use this revision’s SMART and Get Log rules; use the separate log for Endurance Group health.
Get Log Page 的 NSID 與 LID 仍須正確填寫，但每個回傳欄位的實際範圍由定義決定。 || Encode NSID/LID correctly while interpreting each field under its defined scope.
先記錄查詢的 controller 與 NSID，再比較回覆。對不同 NSID 回傳相同 SMART 資料，是本版定義允許且要求理解的行為。 || Record controller/NSID and compare responses; identical data across NSIDs is expected under this revision’s definition.
成功讀取取得整體資訊，不能據此分攤哪個 namespace 消耗多少壽命。 || Successful reads do not allocate endurance consumption to individual namespaces.
不能沿用舊版 namespace-specific SMART 的理解，要求每個 namespace 有不同計數。 || Do not import older namespace-specific assumptions and demand distinct counters.
把 Identify 版本、Log 定義與實際回覆一起核對，避免只憑舊工具標籤判斷。 || Compare revision, log definition and response rather than old tool labels.
先檢查是否把合法 NSID 的接受能力誤當成 per-namespace 計數能力。 || First distinguish accepted NSIDs from per-namespace accounting capability.
''')
q(204,'SMART、實際操作、Error Log 與 PEL 如何交叉驗證？ || How are SMART, operations, errors and PEL cross-checked?', ['pel'], '''
交叉比對要建立合理關係，而不是要求所有資料來源每次都增加一筆。 || Cross-check meaningful relationships rather than demanding one increment in every source per operation.
先固定 controller、操作時間區間與各資料的 scope；不同時間或不同物件不能直接相減。 || Fix controller, time interval and each source’s scope before comparing.
保存支援能力、SMART 前後快照、CQE、Error entries 與可用的 PEL context。 || Preserve capabilities, before/after SMART, CQEs, errors and an available PEL context.
用 SQID／CID 對回命令，以 Error Count 區分紀錄，以 PEL Event Type 與事件資料確認操作；SMART 則依單位與累計條件解讀。 || Correlate command IDs, Error Count and PEL event data while interpreting SMART units and accumulation conditions.
先預測這個操作應改變哪些資料，再執行一次可隔離的情境，最後比較每一條預期關係。 || Predict affected evidence, isolate a scenario and compare each expected relationship.
例如一次正常讀取可增加 Read Commands 與資料量，卻不要求新增 Error entry 或 PEL 命令紀錄。 || A normal Read may increase read/data counters without requiring an error entry or per-command PEL record.
缺少非必要紀錄不能算違規；若 More=1 卻找不到補充資訊，則須進一步檢查覆寫、讀取時序與記錄規則。 || Absence of optional evidence is not a violation; missing advertised More information requires checking overwrite, timing and logging rules.
結論分成「規範要求已滿足」、「明確不符」與「證據不足」，不要把無法觀察寫成已證明失敗。 || Separate compliance, established violation and insufficient evidence.
先檢查每個被期待改變的欄位，是否真的由這個操作觸發。 || First verify that the operation actually triggers each expected field change.
''')
