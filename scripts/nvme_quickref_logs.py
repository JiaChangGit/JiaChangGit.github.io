"""Retrieval, log interpretation and PCIe measurement results."""
from scripts.nvme_quickref_data import card

card('B204','Get Log CDW10：讀哪份、讀多少、是否確認事件','Get Log Page|LID|LSP|RAE|NUMDL',[
'同一個log讀取命令可能附帶確認非同步事件的效果。查此表時，同時保留LID、LSP和RAE，不只記錄buffer長度。',
'LID bits7:0選log；LSP bits14:8由該log定義；RAE bit15為保留事件；NUMDL bits31:16是Dwords數量的低16bits，與NUMDU合成後為減1編碼。RAE=0通常在命令成功時確認相應事件，並非刪除所有log內容。',
'一般512-byte讀取需128 Dwords，因此NUMD=127。失敗的Get Log不能視為已確認事件；各log若另定動作或長度規則，應使用該log規則，例如PEL的ACT3。'],[
'A log read may also acknowledge an asynchronous event. Preserve LID, LSP and RAE, not just buffer length.',
'LID bits 7:0 selects the log, LSP bits 14:8 is log-specific, RAE bit 15 retains the event, and NUMDL bits 31:16 supplies the low 16 bits of the minus-one Dword count combined with NUMDU. RAE=0 normally acknowledges the corresponding event on success rather than deleting all log contents.',
'An ordinary 512-byte read needs 128 Dwords, so NUMD=127. A failed read does not acknowledge the event. Log-specific action or length rules, such as PEL ACT=3, override the general case.'],'B205 B232')

card('B205','Get Log CDW11：長度高位與目標識別','NUMDU|LSI|Endurance Group Identifier|Get Log Page',[
'需要讀大型log或指定某個資源對象時，查CDW11。上半部LSI不是NUMD的更多高位。',
'NUMDU bits15:0與CDW10.NUMDL組成32-bit減1Dword數；LSI bits31:16是log-specific identifier，含義由LID決定。一般長度為4×(((NUMDU<<16)|NUMDL)+1) bytes。',
'NUMDU=1、NUMDL=0對應262148bytes，不是65536bytes。LID09h則利用LSI指定Endurance Group，不能把其值誤加到傳輸長度。'],[
'Inspect CDW11 for large reads or resource selection. Its upper LSI half is not an extension of NUMD.',
'NUMDU bits 15:0 combines with CDW10.NUMDL into a 32-bit minus-one Dword count. LSI bits 31:16 is a log-specific identifier. Ordinary transfer size is 4×(((NUMDU<<16)|NUMDL)+1) bytes.',
'NUMDU=1/NUMDL=0 means 262148 bytes, not 65536. For LID=09h, LSI identifies an Endurance Group and must not be included in length arithmetic.'],'B204 B225')

card('B208','Get Log offset：byte 位置或清單 index','OT|LPO|index offset|byte offset|CSI|UIDX',[
'分段讀log位置不對時，先查OT。相同LPO數字可以表示bytes，也可以表示第幾個資料結構；這就是index offset與byte offset的差別。',
'OT bit23為0時，CDW12／13的LPO表示byte offset；為1時表示清單index，需該log支援。CSI bits31:24選相關I/O command set，UIDX bits6:0為UUID index；兩者也有各自使用條件。',
'對支援index的log，LPO=2、OT=1表示index2；OT=0則只是距log起點2bytes，而且還需符合該讀取方式的對齊要求。不能把兩種值直接互換。'],[
'Check OT when chunked reads start at the wrong location. The same LPO can count bytes or data structures: byte offset and index offset are different units.',
'OT bit 23, when clear, interprets CDW12/13.LPO as bytes; OT=1 interprets it as a supported list index. CSI bits 31:24 chooses the applicable command set, while UIDX bits 6:0 selects a UUID index, each subject to its own conditions.',
'For an index-capable log, LPO=2/OT=1 means index 2. OT=0 instead means byte 2 and must also satisfy applicable alignment requirements. Those values are not interchangeable.'],'B211 B204')

card('B211','Supported Log Pages：這個 LID 能不能用','LID 00h|LSUPP|IOS|LIDSP|SPEDS',[
'在送特殊log動作或index-offset讀取前，查該LID的能力描述子。知道LID有標準定義，不等於此裝置一定支援。',
'LSUPP bit0表示支援，IOS bit1表示可用index offset，LIDSP bits31:16補此LID特定能力。LSUPP=0時忽略其他欄位；IOS也受Get Log extended-data能力條件限制。',
'LSUPP=1、IOS=0表示可讀此log，但不能送OT=1。PEL的LIDSP還可告知擴充context/header能力，不能把所有LIDSP都當同一種bitmap。'],[
'Inspect the descriptor for a LID before issuing special actions or index-offset reads. A standardized LID is not proof of device support.',
'LSUPP bit 0 advertises support, IOS bit 1 index-offset support, and LIDSP bits 31:16 log-specific capabilities. Ignore other fields when LSUPP is clear. IOS also depends on extended-data support.',
'LSUPP=1 with IOS=0 supports the log but not OT=1. PEL additionally uses LIDSP for extended context/header capabilities; LIDSP does not have one universal meaning across logs.'],'B208 B232')

card('B212','Error Information：把錯誤對回命令與欄位','LID 01h|ECNT|SQID|CID|PEL|BYTLOC|BITLOC|LPVER',[
'CQE的M=1或錯誤事件需要更多資訊時，查此64-byte entry。清單從較新錯誤開始，單筆entry包含命令身分、狀態與可能的參數位置。',
'ECNT bytes7:0是錯誤序號，0表示無效entry；SQID9:8、CID11:10對命令，STS13:12對狀態。Parameter Error Location在15:14，BYTLOC指定SQE byte、BITLOC指定該byte的bit。NSID、CSI、OPC、CSINFO與LPVER進一步限定解讀。',
'BYTLOC=40、BITLOC=3指向SQE byte40的bit3，即CDW10 bit3，不是第40個Dword。不是特定命令的錯誤可用FFFFh表示SQID／CID；這裡PEL是Parameter Error Location，與Persistent Event Log縮寫相同但含義不同。'],[
'Read these 64-byte entries when CQE.M or an error event calls for more detail. Newer errors appear first; each entry can identify a command, status and parameter location.',
'ECNT bytes 7:0 is the error sequence number, with zero denoting an invalid entry. SQID bytes 9:8/CID bytes 11:10 identifies the command; STS bytes 13:12 records status. Parameter Error Location 15:14 contains BYTLOC within the SQE and BITLOC within that byte. NSID, CSI, OPC, CSINFO and LPVER further qualify interpretation.',
'BYTLOC=40/BITLOC=3 means SQE byte 40 bit 3, or CDW10 bit 3, not Dword 40. Non-command-specific errors can use FFFFh SQID/CID. Here PEL means Parameter Error Location, distinct from Persistent Event Log.'],'B101 B93')

card('B213','SMART：警告、累計量、溫度與時間','LID 02h|SMART|CW|CTEMP|DUR|DUW|POH|PUSED|TMT',[
'健康與效能驗證常讀這張表，但它混合目前狀態、終生累計量與不同單位的時間。先分欄位種類，才有意義地比較兩次快照。',
'CW是警告bitmap，CTEMP是Kelvin，PUSED是壽命估計百分比；DUR／DUW以1000×512-byte單位向上取整，0表示未回報。HRC／HWC計命令，CBT計分鐘，POH計小時；thermal管理總時間則以秒計。sensor值0表示未實作。',
'DUR增加1不必然等於剛好傳了512000bytes，因為它是取整後計量。PUSED超過100也不直接等於裝置已故障；需一起看警告、媒體錯誤與具體行為。'],[
'SMART combines current warnings, lifetime counters and durations with different units. Classify a field before comparing snapshots.',
'CW is a warning bitmap, CTEMP Kelvin and PUSED estimated lifetime percentage. DUR/DUW round up in 1000×512-byte units; zero means unreported. HRC/HWC counts commands, CBT minutes, POH hours and thermal-management totals seconds. A zero sensor is unimplemented.',
'A DUR increment of one need not equal exactly 512000 newly transferred bytes because the counter is rounded. PUSED above 100 also does not by itself establish device failure; correlate warnings, media errors and behavior.'],'B482 B225 B233')

card('B217','Command Effects：支援與執行影響','LID 05h|CSUPP|LBCC|NCC|NIC|CCC|CSE|CSER|CSP',[
'操作前要知道會改資料、namespace清單還是controller能力，查這張effects描述子。它提供能力與協調建議，不是某次命令已造成哪些改動的歷史紀錄。',
'CSUPP bit0為支援；LBCC1、NCC2、NIC3、CCC4分別表示可能改資料、單一namespace能力、namespace inventory與controller能力。CSE bits18:16及CSER15:14給提交／執行建議；CSP31:20描述可能作用範圍。',
'NIC=1表示操作可能改變namespace清單，成功後應考慮重新查詢；不能由此推論剛剛一定新增一個namespace。理解非0 CSER的主機應依其較新建議判讀，而非把CSE與CSER不加區分地疊加。'],[
'Consult this descriptor before an operation that may change data, namespace inventory or controller capabilities. It describes potential effects and coordination guidance, not a historical result.',
'CSUPP bit 0 reports support; LBCC bit 1, NCC bit 2, NIC bit 3 and CCC bit 4 indicate possible changes to data, one namespace’s capabilities, inventory and controller capabilities. CSE bits 18:16 and CSER bits 15:14 give submission/execution guidance; CSP bits 31:20 gives potential scope.',
'NIC=1 suggests rediscovering namespace inventory after the operation, not that one namespace was definitely added. Hosts understanding a nonzero CSER use its newer guidance rather than indiscriminately combining it with CSE.'],'B338 B446')

card('B221','Host Telemetry：header 與累積資料區邊界','LID 07h|Telemetry Host-Initiated|THDA1LB|THDGN|THS',[
'擷取host-initiated telemetry後，用此header決定資料區大小和本次版本。資料payload通常由廠商定義，header提供可共同判讀的外框。',
'前512bytes為header；DA1／2／3／4 Last Block指出各區最後的512-byte block編號，資料從block1開始，區域是累積擴大的集合。THS在byte380、THDGN381；382／383另帶controller telemetry的狀態與generation副本。',
'DA1LB=2、DA2LB=5代表區域1含blocks1～2，區域2含1～5，不是另外接5blocks。分段讀取要保留generation及擷取操作，避免把不同時點資料拼在一起。'],[
'Use this header to determine host-initiated telemetry boundaries and generation. Vendor-defined payloads sit inside a commonly interpretable envelope.',
'The first 512 bytes form the header. Data Area 1/2/3/4 Last Block fields identify final 512-byte block indices; data starts at block 1 and areas are cumulative. THS is byte 380, THDGN is byte 381; bytes 382/383 copy controller-telemetry availability/generation.',
'DA1LB=2 and DA2LB=5 mean blocks 1–2 and 1–5, not two blocks followed by five more. Preserve generation and capture actions across chunked retrieval to avoid combining different captures.'],'B223 B204')

card('B223','Controller Telemetry：更新通知與 generation','LID 08h|TCDA|TCDGN|TCS|Telemetry Controller-Initiated',[
'controller主動保存telemetry時，這張header用於判斷回報範圍、未確認更新與資料版本。不要把通知狀態當資料長度。',
'TCS在byte381，TCDA382，TCDGN383；各data-area last-block欄仍描述累積範圍。Base2.4的TCDA表示自上次成功RAE=0確認後是否有更新，TCDGN則追蹤擷取代數。',
'TCDA=0可以是先前更新已確認，不足以證明沒有saved telemetry資料。把LID07h的byte381當TCS也會讀錯，因為07h在此位置是THDGN。'],[
'This header describes controller-captured telemetry scope, unacknowledged updates and generation. Notification state is not payload length.',
'TCS is byte 381, TCDA byte 382 and TCDGN byte 383; area last-block fields still describe cumulative extents. In Base 2.4, TCDA tracks updates since a successful RAE=0 acknowledgement, while TCDGN tracks captures.',
'TCDA=0 can mean a previous update was acknowledged; it does not establish absence of saved telemetry. Byte 381 in LID=07h is THDGN, so decoding it as this header’s TCS is also incorrect.'],'B221 B204')

card('B225','Endurance Group：逐組健康與容量','LID 09h|Endurance Group|CW|AVSP|PUSED|ENDGID',[
'controller的總體SMART不能完整回答每個Endurance Group的健康狀況時，查LID09h。先用LSI指定group，避免比較到不同群組。',
'內容包括Critical Warning、Available Spare／Threshold、Percentage Used、資料讀寫及媒體寫入累計量、錯誤數與容量欄位。每個欄位的計量不同，Group的ENDGID可由namespace Identify找到。',
'同一controller下group1出現警告，不表示group2同時有相同警告。比較兩份log時先固定ENDGID與時間；讀取確認通知，也不代表原健康問題已被修復。'],[
'Use LID=09h when aggregate SMART cannot answer health questions for each Endurance Group. Select the group through LSI before comparing reports.',
'Fields include Critical Warning, Available Spare/Threshold, Percentage Used, data/media-write counters, errors and capacity. Units differ by field. Namespace Identify provides its ENDGID.',
'A warning for group 1 does not mean group 2 has the same warning. Fix ENDGID and observation time when comparing logs. Acknowledging a notification does not repair the underlying condition.'],'B205 B346 B213')

card('B232','Persistent Event Log：建立、讀取與釋放 context','LID 0Dh|ACT|context|ACT 3|PEL',[
'分多次讀持久事件時，用ACT管理reporting context，也就是這次固定下來供讀取的事件集合。context不是事件種類。',
'ACT=0讀既有context，1建立並讀取，2釋放，3在必要時建立或沿用並讀header。ACT1遇到已存在context會出錯；ACT3成功時固定回offset0的512-byte header，忽略一般NUMD／LPO長度位置，buffer仍須足夠。',
'ACT3回RCE=0表示處理命令前尚無context，不表示建立失敗。成功後接ACT0讀事件即可；再送ACT1反而可能得到Command Sequence Error。'],[
'ACT manages a reporting context: the fixed event set used for a multipart Persistent Event Log retrieval. It does not select an event type.',
'ACT=0 reads an existing context, 1 establishes and reads, 2 releases, and 3 establishes if needed or reuses it and reads the header. ACT=1 fails if a context exists. ACT=3 returns the 512-byte header at offset 0 regardless of ordinary NUMD/LPO settings, requiring an adequate buffer.',
'RCE=0 after successful ACT=3 means no context existed before processing, not creation failure. Continue with ACT=0; issuing ACT=1 can instead produce Command Sequence Error.'],'B233 B234')

card('B233','Persistent Event header：總長、筆數與讀取版本','TLL|TNEV|LHL|LREV|GNUM|RCE|SEB',[
'開始走訪持久事件前，先從header取得總長與版本。log header版本、generation及單筆event revision是不同欄位。',
'TNEV bytes7:4為事件筆數，TLL15:8為整份bytes，LREV16為版本，LHL19:18加20才是header長度。GNUM373:372用於識別新建立且內容不同的report；RCI含RCE。SEB511:480則表示事件種類支援，不是目前有哪些事件。',
'LHL=492得到512-byte header；TNEV=0仍有header。分段讀取需比對context與GNUM，但相同generation不應被當成跨reset資料必定相同的無限期保證。'],[
'Read total length and version before walking persistent events. Log revision, generation and individual event revision are distinct fields.',
'TNEV bytes 7:4 counts events, TLL bytes 15:8 counts total bytes, LREV byte 16 gives revision and LHL bytes 19:18 plus 20 gives header size. GNUM bytes 373:372 tracks newly established reports with changed content; RCI includes RCE. SEB bytes 511:480 describes supported event types, not present events.',
'LHL=492 gives a 512-byte header even when TNEV=0. Correlate context and GNUM across chunks; equal generation is not an indefinite guarantee across resets.'],'B232 B234')

card('B234','Persistent Event：下一筆從哪裡開始','ET|ETR|EHL|VSIL|EL|VSI|ED|ETSTP',[
'持久事件長度可變，這張表是逐筆走訪的關鍵。先由header決定事件邊界，再按種類解內容，不使用固定stride。',
'ET byte0選種類，ETR1選內容版本，EHL2加3是共同header長度；VSIL bytes21:20給vendor資訊長度，EL23:22包含VSI與Event Data。下一筆起點=目前起點+EHL+3+EL，ED長度=EL−VSIL。',
'起點512、EHL21、VSIL4、EL20時，header24bytes，ED16bytes，下一筆在556。若再把VSIL加一次會走到560而錯位；也不能擅自讓每筆補到4-byte倍數。'],[
'Persistent events are variable length. Use this table to establish record boundaries before type-specific decoding rather than using a fixed stride.',
'ET at byte 0 selects the event type; ETR at byte 1 selects the payload revision. The value in EHL at byte 2, plus 3, gives the common-header size. VSIL bytes 21:20 counts vendor information; EL bytes 23:22 includes both VSI and Event Data. Next=start+EHL+3+EL; ED length=EL−VSIL.',
'At start 512 with EHL=21, VSIL=4 and EL=20, the header is 24 bytes, ED=16 bytes and next record starts at 556. Adding VSIL again incorrectly reaches 560. Do not independently pad each record to four bytes.'],'B233 B236')

card('B236','Persistent Event 類型：去哪個內容格式查','ET|ETR|Firmware Event|Namespace Change|Sanitize Event',[
'共同event header解完後，用此表按ET找到內容格式。它也列出記錄要求和版本，適合查「這個ET代表什麼」及「應套哪版格式」。',
'常用01h健康快照、02h韌體、04hreset、05h硬體、06hnamespace、07h／08h Format開始／完成、09h／0Ah Sanitize開始／完成、0Bh設定、0Ch Telemetry、0Dh溫度。支援要求還受起因命令與控制器條件影響。',
'看見ET0Ah只能先辨認Sanitize完成事件類型，成功與否仍看其payload的結果狀態。ETR不是事件計數；支援某種類型也不保證此次report一定包含該類事件。'],[
'After decoding the common header, route ET to the payload format here. The table also gives revisions and logging requirements.',
'Common types include 01h health, 02h firmware, 04h reset, 05h hardware, 06h namespace, 07h/08h Format start/completion, 09h/0Ah Sanitize start/completion, 0Bh feature changes, 0Ch telemetry and 0Dh thermal events. Requirements depend on triggering-command and controller conditions.',
'ET=0Ah identifies a Sanitize-completion event, not success; inspect its payload result. ETR is not an event count, and supporting a type does not guarantee its presence in this report.'],'B234 B312')

card('P75','PCIe EOM Header：量測完成了嗎、有多少描述子','LID 19h|EOM|EOMIP|EDGN|HSIZE|RSZ|DS|ND|EPL',[
'需要接收端眼圖資料時，先查Eye Opening Measurement header，確認量測是否完成、版本與資料長度。不能看到log有回覆就直接分析眼圖。',
'EOMIP byte1的0／1／2為未啟動、進行中、已完成；HSIZE bytes3:2為64，RSZ7:4為log bytes，EDGN8為generation，LREV9本版為3。DS bytes23:20給描述子大小，ND25:24給筆數；ODP決定可選眼圖資料是否存在。',
'ND是實際回傳描述子數，不能只用lane數當迴圈上限；每lane可能有多個eye。先確認EOMIP=2，再按DS前進，並保留量測時的link資訊。'],[
'Before analyzing receiver-eye data, inspect the Eye Opening Measurement header for completion, revision and length. A successful log response alone does not establish a completed measurement.',
'EOMIP byte 1 values 0/1/2 mean not started/in progress/completed. HSIZE bytes 3:2 is 64, RSZ bytes 7:4 total bytes, EDGN byte 8 generation and LREV byte 9 is 3 here. DS bytes 23:20 gives descriptor size, ND bytes 25:24 count, and ODP controls optional eye data.',
'ND is the actual descriptor count; lane count alone is not a loop bound because a lane can have multiple eyes. Confirm EOMIP=2, advance by DS and preserve the measurement-time link information.'],'P76 P55')

card('P76','EOM Lane Descriptor：眼圖外框與資料限制','MSTAT|LN|EYE|NROWS|NCOLS|EDLEN|Printable Eye|BER',[
'每份描述子對應一個lane的一個eye。查此表可把量測對象、成功狀態與可列印圖形對上，避免把不同lane或eye混在一起。',
'MSTAT byte1的bit0為量測成功，LN2為lane、EYE3為eye；TOP／BTM／LFT／RGT描述圖形邊界，NROWS13:12與NCOLS15:14給字元矩陣大小，EDLEN19:16給vendor eye data長度。Printable Eye從byte32開始，是否存在看header ODP。',
'若NROWS=5、NCOLS=7，字元矩陣佔35bytes；若它存在，後面的Eye Data從67開始。可列印的0／1形狀不足以判定signal integrity，還需電壓、時間尺度、BER門檻等量測資訊。'],[
'Each descriptor describes one eye on one lane. Match measurement identity, success and printable shape without mixing lanes or eyes.',
'MSTAT byte 1 bit 0 indicates success, LN byte 2 lane and EYE byte 3 eye. TOP/BTM/LFT/RGT describe boundaries. NROWS bytes 13:12 and NCOLS bytes 15:14 size the character matrix; EDLEN bytes 19:16 sizes vendor eye data. Printable Eye begins at 32 when present according to ODP.',
'NROWS=5 and NCOLS=7 occupy 35 matrix bytes; when present, subsequent Eye Data starts at 67. A printable 0/1 shape alone cannot establish signal integrity without voltage/time resolution, BER thresholds and other measurement information.'],'P75')
