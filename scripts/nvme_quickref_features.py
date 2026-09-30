"""Feature selectors, power controls and resource interpretation."""
from scripts.nvme_quickref_data import card

card('B198','Get Features：現在值、預設值、保存值或能力','Get Features|FID|SEL|current|default|saved',[
'讀到的Feature值與剛設定的值不同，先查SEL選了哪種回覆。Get Features不一定是在讀目前設定。',
'FID bits7:0選功能，SEL bits10:8的0／1／2／3分別為Current、Default、Saved、Supported Capabilities。SEL=2但不支援保存或沒有保存值時，依規格按Default處理。',
'同一FID用SEL=3回DW0=4，不代表功能目前設為4；它是能力bitmap，應依Figure201解讀。比較設定前後，要記錄SEL與Feature作用對象。'],[
'If a returned feature value differs from the last write, first check SEL. Get Features does not always read the current setting.',
'FID bits 7:0 selects the feature. SEL bits 10:8 values 0/1/2/3 select Current, Default, Saved or Supported Capabilities. A saved-value request falls back to Default if saving is unsupported or no saved value exists.',
'DW0=4 with SEL=3 is a capability bitmap, not a current feature value of 4. Decode it through Figure 201 and retain SEL and the feature’s target when comparing settings.'],'B201 B464')

card('B201','Feature 能力：可改、可保存及 namespace 範圍','SEL 3|CHANG|NSSPEC|SVBL',[
'這張表只用於Get Features的SEL=3回覆。它回答該Feature有哪些操作能力，不能直接套到SEL=0取得的目前值。',
'DW0 bit2是CHANG、bit1是NSSPEC、bit0是SVBL。NSSPEC=0不直接表示controller scope，還要依Feature定義及effects log。CHANG=1也只表示有可更改屬性，不保證每個已進入的狀態都可解除。',
'DW0=6表示可改、namespace-specific、不可保存。若該功能已進入永久寫入保護，CHANG仍不能被解成「一定能改回未保護」。'],[
'Use this table only for a Get Features SEL=3 response. It reports operations supported by a feature, not the current value returned by SEL=0.',
'DW0 bit 2 is CHANG, bit 1 NSSPEC and bit 0 SVBL. NSSPEC=0 does not by itself mean controller scope; consult the feature and effects log. CHANG=1 indicates changeable attributes, not reversibility of every entered state.',
'DW0=6 means changeable, namespace-specific and not saveable. If permanent write protection has already been entered, CHANG does not promise it can be undone.'],'B198 B541')

card('B464','Set Features：要求生效與要求保存分開','Set Features|SV|FID|Feature Identifier Not Saveable',[
'設定當下生效、重設後卻不同時，用這張表確認是否提出保存要求，再查該Feature本身的持續性規則。',
'FID在bits7:0，SV在bit31；其餘bits30:8保留。SV=1要求保存屬性以跨所有power states與reset持續；若該FID不可保存，命令會以Feature Identifier Not Saveable中止。',
'不能把SV=0直接翻成「下次reset一定清除」。部分功能本來就定義某些狀態持續，是否可保存與目前狀態是否持續是兩個判斷。'],[
'When a setting works immediately but differs after reset, check the save request and then the feature’s persistence rules.',
'FID occupies bits 7:0 and SV bit 31; bits 30:8 are reserved. SV=1 requests saved attributes across all power states and resets. An unsaveable FID returns Feature Identifier Not Saveable.',
'SV=0 does not mean every state must disappear on the next reset. Some features intrinsically retain particular states. Saveability and persistence are separate questions.'],'B201 B466')

card('B466','FID 總表：功能名稱、資料 buffer 與作用範圍','FID|Feature Identifier|scope|persistence|data buffer',[
'只有FID數字或不知道Feature影響哪個對象時，從此表找名稱、範圍及是否使用資料buffer。指向NVM規格的列，表示定義分工，不是該FID沒有作用。',
'表按FID排列，欄位包含Current Setting Persists、Uses Data Buffer、Feature Name及Scope。持續性欄有腳註：其判讀對象是不可保存的Feature，不能拿來推翻可保存功能的Saved值語意。',
'APST FID0Ch需要data buffer保存逐state條目；Power Management FID02h主要由CDW11指定。只複製CDW11而漏掉APST表，無法完整重建當時設定。'],[
'Start here when you have only an FID or need its scope and data-buffer requirement. Rows referring to NVM delegate the definition rather than denoting an inactive FID.',
'Columns cover current-setting persistence, data-buffer usage, name and scope. The persistence-column footnote limits its interpretation to unsaveable features; it does not override Saved-value behavior for saveable ones.',
'APST FID=0Ch uses a data buffer of per-state entries; Power Management FID=02h mainly uses CDW11. Capturing CDW11 without the APST table cannot reconstruct that configuration.'],'B475 B477 B468')

card('B340','Power State Descriptor：功耗、延遲與可執行 I/O','PSD|NOPS|MP|MXPS|ENLAT|EXLAT|IDLP|IPS|RRT|RRL',[
'比較power states或排查喚醒延遲時，查各state的32-byte描述子。state編號只用來選狀態，不能直接當功耗或效能排名。',
'NOPS bit25區分是否處理I/O；MP bits15:0與MXPS bit24一起換算最大功耗；ENLAT bits63:32、EXLAT95:64以微秒計。IDLP配IPS讀idle功耗；RRT／RRL／RWT／RWL是相對等級。後面另有Active Power、掉電處理時間與頻寬欄位。',
'MP=350、MXPS=0是3.50 W；MXPS=1則是0.035 W。EXLAT=0表示未回報，不能寫成零延遲。選APST目的state前，先看NOPS及有效功耗、延遲值。'],[
'Inspect each 32-byte descriptor when comparing power states or investigating wake latency. State numbers are selectors, not direct power or performance rankings.',
'NOPS bit 25 distinguishes I/O processing. MP bits 15:0 and MXPS bit 24 jointly encode power. ENLAT bits 63:32/EXLAT bits 95:64 use microseconds. IDLP/IPS describes idle power; RRT/RRL/RWT/RWL are relative rankings. Later fields include active power, power-loss timings and bandwidth.',
'MP=350 with MXPS=0 means 3.50 W; MXPS=1 means 0.035 W. EXLAT=0 means unreported, not zero latency. Check NOPS and valid power/latency values before selecting an APST destination.'],'B468 B477')

card('B467','Arbitration：權重不是效能保證','FID 01h|HPW|MPW|LPW|AB|arbitration',[
'比較不同SQ優先級或命令取走節奏時，查此表。但設定權重不保證應用程式獲得固定比例IOPS，還受排程模式與工作負載影響。',
'HPW bits31:24、MPW23:16、LPW15:8是各service class每輪可執行命令數減1。AB bits2:0是單次由一個SQ取命令的上限，按2^AB計，AB=7特別表示無限制。',
'HPW=3代表4個命令，AB=3代表burst上限8個；相同原始值使用不同編碼。先確認CC.AMS使用的排程模式，才有意義地解讀priority權重。'],[
'Use this table for SQ priority and command-fetch behavior. Weights do not guarantee a fixed application IOPS ratio; arbitration mode and workload still matter.',
'HPW bits 31:24, MPW bits 23:16 and LPW bits 15:8 encode per-round class command counts minus one. AB bits 2:0 limits commands fetched at once from one SQ as 2^AB, except AB=7 means unlimited.',
'HPW=3 means four commands while AB=3 means a burst of eight. Identical raw values use different encodings. Confirm CC.AMS before interpreting priority weights.'],'B41')

card('B468','Power Management：指定 state 與 idle 回應限制','FID 02h|PS|WH|IIELL|IIELLSS',[
'主機明確要求切power state時，這張表定義CDW11。它與APST的自動轉換表不同，不能只看到PS值就重建全部自動轉換行為。',
'PS bits4:0選state，WH bits7:5給workload hint；IIELL bits31:16在支援且選operational state時，以100微秒指定idle後I/O額外延遲限制。IIELL的作用範圍另由IIELLSS決定。',
'IIELL=5表示500微秒，不是5毫秒。對non-operational state設定非0 IIELL，在此能力受支援時會因Invalid Field in Command失敗；先由Power State Descriptor確認state種類。'],[
'This CDW11 defines an explicit host-requested power-state transition. It is separate from APST; PS alone does not reconstruct autonomous transitions.',
'PS bits 4:0 selects a state, WH bits 7:5 supplies a workload hint, and IIELL bits 31:16 uses 100-microsecond units for supported idle-exit limits on operational states. IIELLSS determines its scope.',
'IIELL=5 means 500 microseconds, not 5 ms. With the capability supported, a nonzero IIELL for a non-operational state causes Invalid Field in Command. Identify the state type through its descriptor first.'],'B340 B475')

card('B471','Volatile Write Cache：目前 enable 位','FID 06h|WCE|VWC|volatile cache|Flush',[
'判斷Write完成是否可能只到揮發性cache時，查WCE設定，再結合cache是否存在與命令FUA。WCE不是硬體是否有cache的能力位。',
'CDW11 bit0為WCE，1啟用、0停用，bits31:1保留。實際cache存在性還需依Identify與namespace／FDP配置判斷；Flush與FUA另有各自的非揮發要求。',
'WCE=1不能單獨證明某筆Write只在cache中，因為那筆命令可能FUA=1。比較資料保留結果，需同時保存cache能力、WCE及命令內容。'],[
'Inspect WCE with cache presence and command FUA when assessing whether a Write completion may depend on volatile cache. WCE is not the hardware-presence capability.',
'CDW11 bit 0 enables/disables the cache; bits 31:1 are reserved. Presence also depends on Identify and namespace/FDP configuration. Flush and FUA have their own nonvolatile requirements.',
'WCE=1 does not prove that a particular completed Write exists only in cache: the command may have FUA=1. Preserve capability, WCE and command fields when investigating retention.'],'B338 B346 N71 B294')

card('B472','Number of Queues：主機要求的數量','FID 07h|NSQR|NCQR|queue allocation',[
'初始化要建立多組I/O queues前，用此表解讀主機要求分配的數量。它不是每個queue的深度，也不包括Admin queues。',
'NSQR bits15:0要求SQ數，NCQR bits31:16要求CQ數，兩者都減1編碼；最大可指定原始值FFFEh。此設定應在建立I/O queues前完成，實際分配量由CQE DW0回報。',
'要求8個SQ與4個CQ，CDW11=00030007h。主機不能直接依要求值建立全部queues，而要先讀Figure473的實際結果。'],[
'Use this table for requested I/O queue allocation during initialization. Counts exclude Admin queues and do not describe individual queue depth.',
'NSQR bits 15:0 requests SQs and NCQR bits 31:16 CQs, both minus-one encoded with maximum raw value FFFEh. Configure before creating I/O queues; actual allocation is returned in CQE DW0.',
'Eight SQs and four CQs use CDW11=00030007h. Do not create queues solely from the requested counts; inspect the actual result in Figure 473.'],'B473')

card('B473','Number of Queues：實際分配的數量','NSQA|NCQA|CQE DW0|allocated queues',[
'這張表解Number of Queues的完成回覆，用於確認controller實際保留多少I/O queue資源。要求量與分配量可以不同。',
'DW0的NSQA bits15:0、NCQA bits31:16分別是實際SQ／CQ數減1。它不是queue ID清單，也不表示這些queue已完成Create。',
'DW0=00010003h表示4個SQ、2個CQ。即使先前要求8與4，也要依回覆安排後續建立；分配資源與建立queue是兩個步驟。'],[
'Decode the Number of Queues completion here to learn the actual I/O queue resources allocated. Requested and allocated counts can differ.',
'DW0.NSQA bits 15:0 and NCQA bits 31:16 encode actual SQ/CQ counts minus one. This is neither a queue-ID list nor proof that Create commands have established those queues.',
'DW0=00010003h means four SQs and two CQs. Even after requesting eight and four, use the response for subsequent creation. Allocation and queue creation are separate steps.'],'B472')

card('B475','APST：是否允許自動切換','FID 0Ch|APSTE|APST|autonomous power',[
'設定了idle轉換表卻沒有預期省電行為時，先查APSTE是否開啟。這張表只定義總開關，不包含每個state的等待時間。',
'CDW11 bit0為APSTE，1啟用、0停用，預設0；其他bits保留。每個來源power state的等待條件與目的state另放在APST data structure。',
'APSTE=1不代表立刻進入最低功耗state。仍需該來源state的ITPT非0，並滿足連續idle條件；因此trace應一起保存總開關與對應table entry。'],[
'If an idle-transition table produces no expected power behavior, check APSTE first. This figure defines only the global switch, not per-state delays.',
'CDW11 bit 0 enables APST when one and disables it when zero, the default. Other bits are reserved. Per-source-state timing and destination settings reside in the APST data structure.',
'APSTE=1 does not immediately select the lowest-power state. The source entry needs nonzero ITPT and the continuous-idle condition must be met. Capture both enablement and the relevant entry.'],'B477 B340')

card('B477','APST Entry：從哪個 state、等多久、到哪裡','ITPT|ITPS|APST entry|idle transition',[
'這張表用於解每個來源state的8-byte轉換條目。條目的陣列位置決定來源state，ITPS決定目的state，兩者不能對調。',
'ITPT bits31:8以毫秒表示連續idle門檻，0停用該來源state的轉換；ITPS bits7:3指定目的state。ITPT非0時目的state須為non-operational。高32bits與低3bits保留。',
'來源PS0條目設定ITPT=2000、ITPS=3，低Dword是(2000<<8)|(3<<3)=0007D018h。表示在PS0連續idle超過2000 ms後可依規則到PS3，不是進入PS3後再等2000 ms。'],[
'Decode each eight-byte source-state entry here. Its array index selects the source; ITPS selects the destination. They are not interchangeable.',
'ITPT bits 31:8 is the continuous-idle threshold in milliseconds; zero disables that source entry. ITPS bits 7:3 selects a non-operational destination when ITPT is nonzero. Upper 32 bits and low 3 bits are reserved.',
'For a PS0 entry with ITPT=2000 and ITPS=3, the low Dword is(2000<<8)|(3<<3)=0007D018h. The rule can transition from PS0 to PS3 after more than 2000 ms continuously idle in PS0, not after first entering PS3.'],'B475 B340')

card('B482','HCTM：兩個熱管理門檻','FID 10h|HCTM|TMT1|TMT2|Kelvin|throttling',[
'效能隨溫度下降時，查Host Controlled Thermal Management的門檻。它們是主機要求的管理條件，不等於SMART當下溫度。',
'TMT1 bits31:16為較輕管理門檻，TMT2 bits15:0為較重管理門檻，皆以Kelvin計；0停用該部分。非0值須落在Identify允許範圍；TMT2非0時必須大於TMT1。',
'TMT1=343、TMT2=353約為69.85°C與79.85°C，不是343°C和353°C。是否實際啟動與累計多久，可再查SMART的transition count與total time。'],[
'Inspect Host Controlled Thermal Management thresholds when performance drops with temperature. They are host-selected controls, not current SMART readings.',
'TMT1 bits 31:16 selects the lighter threshold and TMT2 bits 15:0 the heavier one, both in Kelvin; zero disables that part. Nonzero values must fit Identify limits, and nonzero TMT2 must exceed TMT1.',
'TMT1=343 and TMT2=353 are about 69.85°C and 79.85°C, not 343°C/353°C. Use SMART transition counts and total times to investigate actual activity.'],'B213 B338')

card('B543','Interrupt Coalescing：延後中斷的時間與數量','FID 08h|TIME|THR|coalescing|interrupt latency',[
'CQ已有資料但中斷時間較晚時，可用此表核對coalescing設定。它控制中斷聚合，不改變CQE本身的命令status。',
'TIME bits15:8以100微秒為單位，0無延遲；THR bits7:0為建議聚合CQE數減1。任一欄為0時隱含停用coalescing。只適用I/O queues，Admin CQ不支援；每個向量還有自己的設定。',
'TIME=5、THR=7代表500微秒與8筆的建議條件，不是每個I/O必定延遲500微秒。主機持續更新CQ head時，聚合條件可能重啟，因此不能把TIME直接當端到端延遲上限。'],[
'Check coalescing when CQ data exists before its interrupt arrives. It aggregates interrupts without changing command status in CQEs.',
'TIME bits 15:8 uses 100-microsecond units, zero meaning no delay. THR bits 7:0 is the recommended completion threshold minus one. Either field zero implicitly disables coalescing. It applies to I/O queues, not Admin CQ, with additional per-vector configuration.',
'TIME=5/THR=7 specifies recommendations of 500 microseconds and eight entries, not a mandatory 500-microsecond delay per I/O. CQ head updates can restart aggregation conditions, so TIME is not an end-to-end latency bound.'],'P44 P6')

card('B545','HMB：啟用、新配置或返還原記憶體','FID 0Dh|HMB|EHM|MR|HMNARE',[
'重設或電源切換後重新啟用Host Memory Buffer時，查MR和EHM，避免把重新配置的記憶體宣稱成原封不動返還。HMB是提供controller使用的host記憶體。',
'EHM bit0為啟用，MR bit1表示返還先前的同一份HMB；HMNARE bit2在支援時限制non-operational state存取，仍有Admin處理例外。bit3必須清0。MR=1要求size、descriptor地址／內容及buffer內容與停用前一致。',
'若重新配置後清掉了buffer，即使實體地址剛好一樣，也不能使用MR=1宣稱原內容仍在。EHM=0時CDW12～15被忽略，不能拿那些bytes推論已啟用的大小。'],[
'When re-enabling Host Memory Buffer after reset or power changes, inspect MR/EHM so newly allocated memory is not represented as an intact return. HMB is host memory supplied for controller use.',
'EHM bit 0 enables the HMB when set, MR bit 1 declares return of the prior HMB, and HMNARE bit 2 restricts supported non-operational access with Admin-related exceptions. Bit 3 must be zero. MR=1 requires identical size, descriptor address/content and buffer content.',
'If reallocation cleared the buffer, the same physical address does not justify MR=1. With EHM=0, CDW12–15 are ignored, so their bytes do not establish an enabled allocation.'],'B338')

card('B294','FDP Configuration：配置大小、資源數與 PID 切割','LID 20h|FDP|DSZE|FDPCV|RGIF|NRG|NRUH|RUNS|ERUTL',[
'解FDP資源配置或Placement Identifier前，查目前配置描述子。PID不是固定格式的任意數字，Reclaim Group與Placement Handle的切割取決於RGIF。',
'DSZE bytes1:0給整個描述子大小；FDPA byte2含FDPCV有效位、FDPVWC及RGIF。NRG bytes7:4、NRUH9:8是直接數量，MAXPIDS11:10則減1編碼。RUNS23:16是nominal bytes，ERUTL27:24是秒，0表示未回報。',
'NRUH=4表示4個handle描述子，不是5個；MAXPIDS=3才對應最多4個placement identifiers。變長清單後還可能有vendor bytes及padding，走到下一份configuration應依DSZE。'],[
'Check the active FDP configuration before decoding resource counts or Placement Identifiers. RGIF determines the split between Reclaim Group and Placement Handle in a PID.',
'DSZE bytes 1:0 gives descriptor size. FDPA byte 2 contains FDPCV validity, FDPVWC and RGIF. NRG bytes 7:4/NRUH bytes 9:8 are direct counts; MAXPIDS bytes 11:10 is minus-one encoded. RUNS bytes 23:16 counts nominal bytes; ERUTL bytes 27:24 seconds, with zero unreported.',
'NRUH=4 means four handle descriptors, not five; MAXPIDS=3 corresponds to four placement identifiers. Vendor bytes and padding may follow the list, so use DSZE to find the next configuration.'],'N21 N71')

card('N21','RUH Status：目前剩餘可寫量','RUH|PID|RUHID|EARUTR|RUAMW|I/O Management Receive',[
'想知道某個placement指向的Reclaim Unit目前還可寫多少，查這張NVM專屬status描述子。它是當下回報，不能用nominal容量直接取代。',
'PID bytes1:0、RUHID3:2對應placement與handle；EARUTR7:4是估計剩餘秒數，0表示未回報；RUAMW15:8是目前可寫入的logical blocks。後16bytes保留。',
'RUAMW=1000且格式4 KiB，表示4,096,000bytes的blocks計量；它可小於或大於RUNS所報nominal bytes。EARUTR=0不表示Reclaim Unit已立刻過期。'],[
'Use this NVM-specific status descriptor to inspect currently writable capacity in the Reclaim Unit referenced by a placement. Nominal capacity is not a substitute for this snapshot.',
'PID bytes 1:0 and RUHID bytes 3:2 identify placement and handle. EARUTR bytes 7:4 estimates remaining seconds, with zero unreported. RUAMW bytes 15:8 counts currently writable logical blocks. The remaining 16 bytes are reserved.',
'RUAMW=1000 with 4 KiB blocks means 4,096,000 bytes in block units and can differ in either direction from RUNS nominal capacity. EARUTR=0 does not mean immediate expiration.'],'B294 N125')
