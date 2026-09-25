"""Distinct source-figure lessons and shared field explanations, scoped to PEL."""
EXAMPLES={}; GUIDES={}; MEMBERS={}

def example(key,takeaway,worked,en):
    EXAMPLES[key]=dict(takeaway=takeaway,example=worked,en=en)

def group(key,title,relation,figures,*rows):
    ident='pel-'+key
    GUIDES[ident]=dict(id=ident,title=title,relation=relation,rows=list(rows),
        headers=['欄位或表中分類','位置、數值與成立條件','帶入例子後怎麼讀'])
    for f in figures: MEMBERS[f]=ident

def key(figure):return ('B' if figure['source_id']=='NVME-BASE-2.4' else 'N')+figure['number']
def lesson(figure):return EXAMPLES[key(figure)]
def guide(figure):return GUIDES[MEMBERS[key(figure)]]

example('B232','ACT選擇的是context動作，不是想讀哪一種事件。',
 'ACT3成功回RCE1表示沿用已有context；ACT1在同樣已有context時卻回Command Sequence Error。這兩種建立動作不是同義詞，不能只因名稱都含Establish就互換。',
 'ACT selects a context operation, not an event type.')
example('B235','ECRH在Supported Log Pages的能力描述子內，並不放在PEL事件header。',
 'LID0Dh的描述子若LIDSP bit0=1，表示可以使用ACT3與GNUM；這個1不是ACT1，也不是PEL header的RCE1。',
 'ECRH belongs to the Supported Log Pages capability descriptor, not an event header.')
group('actions','四種動作與一個能力位','Figure232使用CDW10內的LSP bits9:8；Figure235使用能力描述子的LIDSP bit0，位置與用途不同。',['B232','B235'],
 ('ACT=0：Read','讀既有context；從LPO指定位置開始。沒有context時回Command Sequence Error。','分段讀取的第二段用ACT0，不重建事件集合。'),
 ('ACT=1：Establish and Read','先決定回報集合與長度，建立context後讀取；已存在時失敗。','NUMD127、LPO0可先讀512-byte header。'),
 ('ACT=2：Release','釋放已有context；沒有也不算錯，不回log data，忽略NUMD與LPO。','不是清除持久事件；配置更大的buffer也不會讓它讀回事件。'),
 ('ACT=3：Establish or reuse + Header','不存在就建立，存在則沿用；均成功回offset0的512 bytes。忽略NUMD與LPO，buffer至少512 bytes。','RCE0是原先不存在；成功之後已建立，接續用ACT0。'),
 ('ECRH與保留位','能力LIDSP bit0=1支援ACT3與GNUM；bits15:1保留。支援PEL且符合Base2.0以上時須為1。ACT所在的LSP bits14:10保留。','先確認支援，不能把能力值寫到命令的錯誤bit位置。'))

example('B233','TLL是整份長度，TNEV是事件筆數，LHL要加20才是header大小。',
 'LHL=492時header=512 bytes；TNEV=0仍有header。若TLL=556而第一筆總長44，就由offset512走到556，剛好到資料尾端，而不是再找第二筆。',
 'TLL measures the report, TNEV counts events, and LHL excludes the first twenty header bytes.')
group('log-header','整份報告的header：先讀長度，再讀來源與支援','所有位置相對log起點；本版header共512 bytes。未展開的識別資料仍佔原位，不能刪掉其bytes後重算後續offset。',['B233'],
 ('LID byte0；TNEV bytes7:4；TLL15:8','LID=0Dh；TNEV是直接筆數；TLL含header的總bytes。bytes3:1保留。','TNEV9代表9筆，不是0-based的10筆。'),
 ('LREV byte16；LHL19:18','本版LREV=03h；byte17保留。header長度=LHL+20，當前LHL=492。','LREV3不能代替事件自己的ETR。'),
 ('TSTMP27:20；POH43:28；PWRCC51:44','TSTMP是context建立時間，格式見Timestamp組。POH為取log時power-on hours，可不含非運作狀態；PWRCC為控制器電源循環次數。','TSTMP與單筆ETSTP回答不同時間；不能把POH當毫秒。'),
 ('VID53:52；SSVID55:54；SN75:56；MN115:76','分別為PCI廠商識別、副系統廠商識別、20-byte序號、40-byte型號。','這些資訊辨認記錄來源，不是某筆事件的NSID。'),
 ('bytes371:116','本篇不展開的識別資料，佔256 bytes；不是保留區，也不是零長度。','GNUM仍從372開始，不得前移到116。'),
 ('GNUM373:372','建立新context且內容相較上一份改變才遞增；FFFFh加1回0。','ACT0多讀幾次不使GNUM每次加1；相等也不意味可忽略context重設條件。'),
 ('RCI377:374：RCE bit18','回報命令處理前是否已有context；RCE0時RCPIT與RCPID清0。bits31:19保留。','ACT3新建成功可回RCE0。'),
 ('RCI：RCPIT bits17:16、RCPID15:0','RCPIT0無既有context資訊；1是subsystem port；2是Management Endpoint，RCPID低byte為其port、高byte0；3保留。','RCPIT2、RCPID0005h是管理入口5，不是控制器CNTLID5。'),
 ('SEB511:480；bytes479:378保留','256-bit支援bitmap。bit1～15依次是SMART、FW、時間、reset、hardware、namespace、format start／complete、sanitize start／complete、Set Feature、telemetry、thermal、verification、CDP；222=DEh廠商、223=DFh TCG。','bit6=1表示支援Namespace Change，不表示目前有6筆事件。'),
 ('SEB與ET10h的來源差異','本版Figure233仍把bits221:16列為保留，但Figure236與後文已定義ET10h。兩處不一致，不能自行宣稱SEB bit16是ET10h能力位。bit0與bits255:224也保留。','可以按ET10h的已定義格式讀取實際事件；不捏造一個尚未定義的能力bit。'))

example('B234','EL已包含VSI；用EHL+3+EL前進，才會落在下一筆事件開頭。',
 '另一個例子：事件起點1024、EHL21、VSIL0、EL12，沒有VSI，ED從1048開始且長12，下一筆1060。此時ED緊接header，不保留一段空的VSI槽位。',
 'EL includes VSI; advance by EHL+3+EL to reach the next record.')
group('event-header','單筆事件的共同外框','以下offset相對這筆事件起點；目前共同header24 bytes，但解析仍依EHL+3。外層EL與內層各資料長度不可互換。',['B234'],
 ('ET0、ETR1、EHL2','ET選種類，ETR選內容版本；EHL只計前3 bytes之後的header長度。','EHL21得到24；ET05／ETR2應用新版硬體事件格式。'),
 ('EHAI3：PIT bits1:0','0未回報port類型；1subsystem port；2Management Endpoint；3未關聯port。Base2.0以上要求非0；bits7:2保留。','PIT3是已明確說無port，不等於舊格式的未回報。'),
 ('CNTLID5:4；ETSTP13:6','CNTLID為建立紀錄的控制器；控制器專屬事件指該控制器，否則是subsystem選定的記錄者。ETSTP為發生時間。','共同header的CNTLID不保證等於ED內每一個描述子的CNTLID。'),
 ('PELPID15:14；19:16保留','PIT0／3時為0；PIT1時為subsystem port ID；PIT2時低byte為管理端點port ID、高byte0。','先讀PIT才能解PELPID；0007h不是必然指namespace7。'),
 ('VSIL21:20；EL23:22','VSIL是廠商附加bytes數；EL是VSI加ED的bytes數。無VSI時VSIL0。','VSIL4、EL20，ED只有16。'),
 ('VSI起點EHL+3；ED起點EHL+3+VSIL','VSI可省略，ED也可不存在；下一筆起點加EHL+3+EL。','ET0E／EL0仍有24-byte共同header，沒有ED，也沒有VSI。'),
 ('TLL、TNEV與未知版本','依長度走訪事件，同時核對筆數與總邊界；未知內容不按已知格式猜欄位。','傳輸可以涵蓋半筆事件，應組合足夠bytes後再讀；不能自行把每筆補成4-byte倍數。'))

example('B236','支援要求與ETR分別回答「要不要有」和「怎麼解」。',
 'ET08的ETR2是新版Format Completion格式，不是第2筆Format事件；ET0E雖沒有ED，仍是有效的選用事件種類。',
 'Support requirements and ETR answer whether a type is required and how to decode it.')
group('event-types','把類型、記錄要求與內容版本對照','M/O的前提是支援PEL；本篇只呈現PCIe相關要求。事件子類的記錄門檻與廠商抑制規則仍同時適用。',['B236'],
 ('01h SMART；02h FW；03h Timestamp；04h Reset','01在PCIe情境必備；02～04必備。這四類ETR=1。','必備種類不等於這次TNEV必須含每一種，仍要有相應觸發。'),
 ('05h Hardware；06h Namespace；07h／08h Format','05必備，ETR2；06與07／08在起因命令受支援時必備。06／08用ETR2，07用1。','ETR1的07與ETR2的08不可因同是Format而套相同表。'),
 ('09h／0Ah Sanitize','起因命令受支援時必備，兩者ETR2。','NSID位於新內容裡；讀舊ETR不能直接假設有它。'),
 ('0Bh／0Ch／0Dh／0Eh／0Fh／10h／DEh','均選用、ETR1；依次為Set Feature、Telemetry、Thermal、Verification、CDP、Exported Change、Vendor。','選用指不一定支援；支援後仍須遵守該事件的觸發規則。'),
 ('DFh與保留代碼','DFh選用，其ETR與ED保留給TCG定義。00h、11h～DDh、E0h～FFh保留。','未知碼不解成最近的已知事件；DFh也不套DEh描述子。'))

example('B237','這512 bytes是事件當時的完整SMART資料，不是取PEL當下的健康值。',
 '一份舊事件的POH=1200，今天直接讀SMART是1400，兩者可以都正確；快照各自對應不同時間，不能把差異當欄位位置錯誤。',
 'These 512 bytes are the historical SMART snapshot, not current health at PEL retrieval.')
example('B213','SMART同時有狀態、累計量與時間，零值與單位必須逐欄判斷。',
 'Data Units Read=3代表向上取整後的1000×512-byte計量；Controller Busy Time=3卻是3分鐘。把兩個3放在同一條「使用量」軸會失去意義。',
 'SMART mixes status, counters and durations, each with its own units and zero semantics.')
example('B214','每個溫度sensor是16-bit Kelvin值，0代表沒有實作。',
 'Sensor1=300、Sensor2=0：前者約26.85°C，後者不是−273.15°C的實際測量；sensor位置與精度由廠商決定。',
 'A sensor is a 16-bit Kelvin value; zero means unimplemented, not a physical absolute-zero reading.')
group('smart','從快照外框讀進SMART欄位','Figure237的ED bytes511:0整份依Figure213；這裡按讀值用途分組，不要求以表內順序背誦。保留區不能當成額外sensor。',['B237','B213','B214'],
 ('CW byte0；EGCWS6；INFW7','CW bits0備用容量、1溫度、2可靠度、3全媒體唯讀、4揮發性備援、5持久記憶區唯讀／不可靠、6personality不確定，bit7保留。EGCWS bits0／2／3為任一Group的容量／可靠度／唯讀警告，其餘保留。INFW bit0為輸入電壓過高或過低，其餘保留。','多個警告可同時1；CW不是單選錯誤代碼，也不是單一namespace寫入保護設定。'),
 ('CTEMP2:1；AVSP3；AVSPT4；PUSED5','CTEMP是廠商計算的綜合Kelvin溫度；AVSP／AVSPT為0～100%。PUSED是壽命估計，100不必然失效，可超過100，超過254以255表示，運作時按power-on hour更新。','PUSED105表示估計使用量超過額定基準，不是105%讀取失敗率。'),
 ('DUR47:32；DUW63:48','以1000×512-byte單位向上取整，不含metadata；0表示未回報。','DUR3對應2001～3000個512-byte資料單位，不能宣稱精確1500KiB。'),
 ('HRC79:64；HWC95:80','已完成的Host Read／User Data Out類命令數；具體命令歸類由command set決定。','一次命令可以傳很多blocks；命令計數不能直接換成bytes。'),
 ('CBT111:96；PWRC127:112；POH143:128','CBT以分鐘計控制器忙於I/O的時間；PWRC為電源循環次數；POH以小時計，可能不含非運作狀態。','I/O重疊時CBT不是把每筆命令延遲相加。'),
 ('UPL159:144；MDIE175:160；NEILE191:176','UPL累計非預期斷電；MDIE累計未復原資料完整性錯誤；NEILE是終生Error Information log entries數。','不把NEILE當作這份PEL的TNEV，也不由UPL推算掉電持續多久。'),
 ('WCTT195:192；CCTT199:196','以分鐘計警告／嚴重溫度時間。WCTT一般為WCTEMP≤T<CCTEMP，配置遲滯時含遲滯時間；WCTEMP或CCTEMP為0時WCTT0，CCTEMP0時CCTT0。','CTEMP是溫度，WCTT是時間，不可互相比大小。'),
 ('TSEN1～8：bytes215:200','每個佔2 bytes，0未實作；非0按Kelvin讀，對應Figure214。','第3顆sensor起offset204，index與byte offset不要混淆。'),
 ('TMT1TC219:216／TMT2TC223:220','分別為兩種主機熱管理門檻的轉換次數，32-bit飽和；0可以是未啟用或沒發生。','計數2不是設定溫度2K。'),
 ('TTTMT1 227:224／TTTMT2 231:228','分別以秒計兩種熱管理動作累積時間，32-bit飽和。','這裡60是60秒，與WCTT60分鐘不同。'),
 ('OLEC239:232；IPM243:240','OLEC是向上取整的終生Wh，0未回報、64-bit飽和。IPM bits23:20為測量類型，bits17:16 scale：0未回報、1=0.0001W、2=0.01W、3保留；bits15:0數值。其餘bits保留。','IPM scale2、value350表示3.50W；不能把OLEC與IPM當同單位。'),
 ('保留區與快照頻率','bytes31:8、511:244保留；其他計數通常以128-bit保存，個別欄位上列寬度優先。ET01間隔≤24 power-on hours；虛擬化時對primary controllers記錄。','斷電兩天不等於必須額外新增兩筆每日快照。'))

example('B254','Telemetry事件只複製header，資料區的最後block編號不是事件內的資料。',
 'TIL byte0=08h、TCDA3LB=9：它指向當時Controller-Initiated Telemetry的blocks1～9，但ET0C的ED仍只有512 bytes，沒有那些9個blocks。',
 'The telemetry event copies only the header; advertised data blocks are not included.')
example('B221','Host-Initiated header的scope在byte380，generation在381。',
 'THS=2、THDGN=7表示subsystem範圍的第7代回報標記；THDA1LB=2、THDA2LB=5表示areas分別含blocks1～2與1～5，不能相加成7。',
 'Host-Initiated scope is at byte380 and its generation at381; areas share the same starting block.')
example('B223','Controller-Initiated的scope在381，TCDA是更新是否已確認，不能當資料大小。',
 'Base2.4下TCDA=0可能是主機已確認先前更新，仍可有已擷取資料；不是一看到0就說原Telemetry只有header。這筆PEL本身是否只有header則由ET0C格式決定。',
 'Controller-Initiated scope is at381; TCDA tracks update acknowledgement, not payload size.')
group('telemetry','比較兩種Telemetry header的相同與不同','Figures221／223只取前512 bytes，正好是Figure254保留的TIL；原始後續資料blocks不納入本事件。',['B254','B221','B223'],
 ('LID0；IEEE7:5','LID07h為Host-Initiated，08h為Controller-Initiated；IEEE為能解資料的廠商OUI，0未提供。bytes4:1保留。','先看07／08，才決定byte381應當作generation或scope。'),
 ('DA1LB9:8、DA2LB11:10、DA3LB13:12、DA4LB19:16','皆為512-byte block的最後編號；非空從block1開始。DA2≥DA1、DA3≥DA2；支援DA4時DA4≥DA3。DA1=0表示無資料；15:14保留。','DA3LB9代表資料範圍1～9，不含header block0；資料區是重疊擴大集合。'),
 ('Host header：THS380、THDGN381','THS0未回報、1controller、2subsystem，Base2.0以後版本不允許0，其餘保留。THDGN每次擷取遞增，FFh回0。bytes379:20保留。','THDGN是8-bit，不是PEL的16-bit GNUM。'),
 ('Controller header：TCS381；bytes380:20保留','TCS的0／1／2與THS同義，但位置不同。','不能把Host的THDGN7，套Controller表讀成非法scope7。'),
 ('共同：TCDA382、TCDGN383','TCDA1表示自上次RAE0成功讀取後有更新，0表示沒有未確認更新；Base2.4不能以0推論無saved state。TCDGN每次擷取完成後遞增，FFh回0。Host header只是複製這兩個Controller值。','PEL保留的是事件時副本；讀取PEL不是在確認原08h通知。'),
 ('RID511:384','128-byte廠商原因識別資料，用來辨認當時操作條件；不是通用錯誤文字。','相同RID可協助對照，但其內容解碼與唯一性不能自行保證。'))

example('B255','THRESH決定事件類型，OTMP只是相對門檻的溫差。',
 'THRESH01h、WCTEMP343K、OTMP5表示往上越過warning時高出5K；THRESHB0h則是往下跨under-threshold，不能也一律用加法。',
 'THRESH selects the thermal event; OTMP is a difference relative to the relevant threshold.')
group('thermal','門檻事件的兩個bytes','OTMP在byte0，THRESH在byte1；相對差值不是從0K起算。起因與門檻要一起讀。',['B255'],
 ('THRESH01h／02h','往上跨WCTEMP／CCTEMP到大於等於門檻；除頻率限制外須記錄。','warning門檻343K、OTMP5，可得到348K。'),
 ('03h／04h／05h','TMT1較輕、TMT2較重的熱管理開始，或廠商熱管理開始；可記錄。','05h門檻由廠商決定，未知門檻就無法只靠差值算絕對溫度。'),
 ('88h／89h','88h由過熱或過冷回到正常區間；89h在原先未到WCTEMP的情況下停止熱管理。','「回正常」與「停止一種管理動作」是不同條件。'),
 ('B0h；F0h～FFh','B0h由高於under-threshold往下到小於等於門檻；F0h～FFh廠商自訂，其他未列值保留。','低溫跨門檻要考慮方向，不能把OTMP都加到WCTEMP。'),
 ('OTMP','門檻與測量溫度的絕對差，單位Kelvin。','差5K等於差5°C；絕對348K才換成74.85°C。'))

example('B238','韌體事件保留提交要求與完成狀態；NFR不是已啟用版本的證明。',
 'OFR=A、NFR=B、FCA=1，描述替換並選擇下次reset啟用B。即使提交成功，也還要等對應啟用時點，不能把B當成事件當下正在執行的版本。',
 'The firmware event records a commit request and completion, not proof that NFR is already active.')
group('firmware','韌體提交的要求與結果','Figure238的ED長22 bytes；版本欄是8-byte版本資料，不能把它們當整數比較新舊。',['B238'],
 ('OFR7:0；NFR15:8','OFR為原先active版本，NFR為要求提交的新版本。','版本B字樣出現在NFR，只證明請求的版本。'),
 ('FCA16；FSLT17','FCA為Commit Action；FSLT為slot。0取代不啟用、1取代並下次reset啟用、2選既有slot下次reset啟用、3立即啟用；6／7為Boot Partition相關動作，4／5保留。','FCA1與FCA3的啟用時點不同。slot0在命令中讓控制器選slot，不是編號0的固定槽。'),
 ('STCTFCC18；SRFCC19；VAFCRC21:20','前兩者為該次Firmware Commit的SCT與SC；最後為廠商補充Firmware Commit結果碼，0表示無附加資訊。','SCT1、SC10h表示提交成功但需要subsystem reset；不是通用的成功且已啟用。'))
example('B239','PTSTP是變更前，外層ETSTP是變更後，MSR才是從reset起算的間隔。',
 'PTSTP=90000ms、新ETSTP=5000ms、MSR=100000ms可以描述主機把時鐘調小；不能因90000大於5000就把事件順序顛倒。',
 'PTSTP is the previous time, the enclosing ETSTP is the new time, and MSR measures time since reset.')
example('B480','48-bit毫秒值需要連同Origin與SYNC讀，不能一律當UTC。',
 'Timestamp value5000、Origin0表示從reset後的時間基準計到5秒；Origin1才表示主機設過時間，但主機設的值也不保證是真實UTC。',
 'Interpret the 48-bit millisecond value with Origin and SYNC rather than assuming UTC.')
group('timestamps','把數值、起點和是否連續計時分開','Figure239只存前一時間與MSR；事件後時間在共同header。Figure480同時解釋TSTMP、ETSTP、PTSTP與CTSTP。',['B239','B480'],
 ('Timestamp bytes5:0','48-bit毫秒值，計數回捲依2^48範圍；不能只讀低32bits。','5000ms=5秒；換算成日期前必須知道時間起點。'),
 ('byte6 bits3:1：Origin','0從controller reset後的起點；1主機曾設定；其他值保留。','Origin1表示來源方式，不是時鐘校準保證。'),
 ('byte6 bit0：SYNC','0計時連續；1可能有暫停計時區間。bits7:4及byte7保留。','SYNC1的兩筆差1000ms，不一定等於真實世界剛好過1秒。'),
 ('Figure239 PTSTP7:0、MSR15:8','PTSTP用上述8-byte格式；MSR是距Controller Level Reset的毫秒數，不是另一份Timestamp結構。','MSR的高byte不能按Origin／SYNC讀。'))

example('B240','FREV後面接的是多份reset描述子，不是只有一個controller狀態。',
 '若ED長80 bytes，扣掉8-byte FREV還有72，正好放2份36-byte描述子。外層VSI不在這80-byte ED裡，不能再扣一次。',
 'FREV is followed by a list of reset descriptors, potentially covering several controllers.')
example('B241','FA描述這個controller的韌體啟用結果，POM則是累積通電時間。',
 '兩個描述子CNTLID1／2可以各有不同CPWRC與CTSTP。FA=2表示該控制器啟用失敗，POM=3600000表示累計約1小時的毫秒表示法，不是reset耗時1小時。',
 'FA describes firmware activation for this controller; POM is lifetime power-on time, not reset latency.')
group('reset','先定清單長度，再逐控制器讀','Figure240的RIL是清單；Figure241是清單內每個36-byte項目。數量=(EL−VSIL−8)/36，前提是內容符合此ETR格式。',['B240','B241'],
 ('FREV：ED bytes7:0','CC.EN由0到1時即將生效的韌體版本。後面所有bytes為RIL。','若版本A仍有效，不因先前NFR寫B就改報B。'),
 ('描述子CNTLID1:0、FA2','CNTLID辨認控制器；FA0沒啟用、1啟用成功、2啟用失敗，其餘保留。','FA0不是「啟用失敗」；表示沒有做這個動作。'),
 ('OIP3：RDNF bit0','記錄reset時是否有Format NVM進行中；bits7:1與bytes15:4保留。','RDNF1只說當時在進行，不回報Format最終結果。'),
 ('CPWRC19:16；POM27:20','電源循環次數與累積power-on milliseconds；POM可能略過非運作狀態，解析度由廠商決定。','POM若只按小時更新，會以3600000的倍數呈現。'),
 ('CTSTP35:28','各控制器的power-on／reset事件時間，使用Timestamp格式。','不同控制器的CTSTP數字不能不看時鐘來源就比較先後。'))

example('B247','先看NMCDW10的動作與NSID，才能決定容量和格式欄位是否有效。',
 'SEL1且NSIDFFFFFFFFh表示刪除全部；此時讀到NSZE0不能解成刪除一個0-block namespace，因為這個單一namespace欄位在該情境是保留。',
 'The management action and NSID determine whether capacity and format fields are meaningful.')
example('N112','NVM只補定事件byte32／33的來源與格式，沒有再加一個namespace header。',
 '單一Delete事件的byte32複製NVM Identify byte26，byte33複製Identify byte29；若用舊位置在事件byte26／29找它們，會錯讀NCAP。',
 'NVM specializes event bytes32/33 without adding another namespace header.')
example('N123','FLBAS的格式編號與metadata方式共用一個byte，DPS另外選PI類型。',
 'FLBAS32h：若支援超過16個格式，index=(1×16)+2=18，bit4=1表示延伸LBA；若只支援16個以內，應忽略FIDXU，不可硬讀成格式18。',
 'FLBAS packs the format index and metadata mode; DPS separately selects protection information.')
example('N134','Create輸入與事件輸出的位置不同，而且不是整個輸入buffer都會留在事件裡。',
 '主機在Create資料byte26寫FLBAS12h，事件把它放到byte32；Create資料裡較後方的Placement Handle List不會因此自動出現在48-byte Namespace Change ED。',
 'Create inputs move to different offsets in the event; the entire input buffer is not preserved.')
example('B446','SEL是低4-bit的管理動作，不是NSID，也不是Get Features的SEL。',
 'NMCDW10=00000001h表示Delete；要刪一個或全部還得讀NSID。數字1不代表namespace1。',
 'The low four-bit SEL is a management action, distinct from NSID and Get Features selection.')
group('namespace-fields','從Create／Identify來源對到48-byte事件','Figure247給位置與來源，NVM112補byte32／33；NVM123與134只取本事件用到的欄位，不展開整份長結構。',['B247','N112','N123','N134','B446'],
 ('NMCDW10 ED3:0；SEL bits3:0','0Create、1Delete、2Restore Default Namespace Configuration，3～15保留；bits31:4保留。','Restore有其命令碼，但本事件表的Create／Delete取值規則不應擅自擴寫成Restore後所有欄位的快照。'),
 ('NSZE ED15:8；NCAP31:24','Create取主機值；單一Delete取該namespace值；Delete All保留。皆以logical blocks計，NCAP是可配置上限，NSZE是可定址範圍大小。ED7:4、23:16保留。','NSZE1000與NCAP800不是1000bytes與800bytes。'),
 ('FLBAS ED32 ← NVM來源byte26','bit7保留；bits6:5為FIDXU，bits3:0為FIDXL。超過16種格式時index=(FIDXU<<4)|FIDXL；≤16時應忽略FIDXU。bit4 MTELBA選延伸LBA或分開buffer，無metadata時不適用。','12h是index2、metadata延伸傳輸，不是18-byte LBA。'),
 ('DPS ED33 ← NVM來源byte29','bits2:0 PIT：0未啟用、1／2／3各PI類型、4～7保留；bit3 PIP選metadata前／後，NVM1.3要求0放尾端；bits7:4保留。','01h啟用Type1並放尾端。這裡的PIT不是事件header的Port Identifier Type。'),
 ('兩欄取值時機','FLBAS／DPS在Create取主機指定值、單一Delete取Identify值、Delete All保留；不拿目前新建同號namespace的Identify代替歷史值。','原NSID7刪除後再次分配7，今天的格式可能與舊事件不同。'),
 ('NMIC ED34；ED35保留','低bit表示是否可共享於多控制器；取Create輸入或單一Delete的namespace值，Delete All保留。','共享能力不等於目前有幾個控制器附接。'),
 ('ANAGRPID ED39:36','Create主機有指定取指定值，否則取控制器實際選擇；單一Delete取當時值，Delete All保留；不支援時0。','ID是存取狀態群組識別，並非容量或namespace計數。'),
 ('NVMSETID ED41:40；ENDGID43:42','Create取主機指定，單一Delete取namespace值，Delete All保留；Create來源的0可表示由控制器決定。','事件保留的輸入0不等於裝置內必然有一個編號0的實體。'),
 ('NSID ED47:44','Create為成功分配的新ID；單一Delete為被刪除ID；Delete All為FFFFFFFFh。','成功Create記錄物件建立，不證明主機已完成Attachment。'),
 ('來源位置與未保存內容','NVM來源NSZE7:0、NCAP15:8、NMIC30、ANAGRPID95:92、NVMSETID101:100、ENDGID103:102。其他Create專屬欄位不在此48-byte事件格式中。','只對照表列欄位，不把來源buffer的所有保留間隔照搬進事件。'))

example('B248','Format開始事件保存已通過參數驗證的要求與當時能力，還沒有修改結果。',
 'NSID7、FNA.FNS1表示這次格式操作可影響全部namespace，不是只改7。FMCDW10選格式，不能把NSID7當format index7。',
 'The Format-start event preserves a validated request and capabilities, before modification results exist.')
example('B249','完成事件的INCPLTF和FNVME一起區分「改過資料卻失敗」。',
 'FNVMS=03h表示INCPLTF1、FNVME1；即使SFPI0，也不是成功。若INFO0，還要考慮根本沒有CQE可保存的情況，不能用零推翻失敗旗標。',
 'INCPLTF and FNVME distinguish a failed operation that already modified data.')
example('B195','Format index被拆成高低欄位，SES則另選安全清除動作。',
 'LBAFU1、LBAFL2在extension有效時選index18；SES1另表示User Data Erase。不能把bits13:9合成一個更大的格式號。',
 'Format index spans upper/lower fields; SES separately selects secure erase.')
example('N91','NVM補定Format命令的bits8:4，沒有改變Base的SES和格式編號位置。',
 'MSET1、PI1、PIL0組成低位的30h，再加format index2得到32h；這是Format CDW10，不是事件FLBAS32h的意思。',
 'NVM defines Format command bits8:4 without changing Base SES or index positions.')
group('format','開始參數與完成結果分別解讀','Figure248 ED共12 bytes，249新版ED也12 bytes，但相同offset並不是相同欄位。Figures195／NVM91只用來解保存的FMCDW10。',['B248','B249','B195','N91'],
 ('Start：NSID3:0、FNA4、FMCDW10 11:8','NSID為命令目標，FNA保存Identify Controller能力，bytes7:5保留。','FNA是控制器能力，不能拿目前Identify Namespace某個同offset的byte替代。'),
 ('FNA bits3:0','bit3 FNVMBS=1反而不支援FFFFFFFFh；bit2 CRYES為crypto erase支援；bit1 SENS控制secure erase是否影響全部；bit0 FNS控制一般format是否影響全部。bits7:4保留。','支援廣播與實際format影響全部是兩個問題。'),
 ('FMCDW10：LBAFU13:12、LBAFL3:0','format index=(upper<<4)|lower；Host Behavior LBAFEE0時忽略upper。bits31:14保留。','要知道歷史LBAFEE條件，才可把upper1與lower2解成18。'),
 ('FMCDW10 SES11:9','0不要求安全清除；1User Data Erase，結果內容不保證全0；2Crypto Erase刪除金鑰；3～7保留。','SES1不保證採某一種物理擦除演算法，已加密資料可使用crypto erase完成。'),
 ('NVM FMCDW10 PIL8、PI7:5、MSET4','PIL需0把PI放metadata尾端；PI0關閉、1／2／3類型、4～7保留；MSET1metadata延伸傳輸，0分開，metadata大小0時忽略。','CDW10=32h是index2、PI1、MSET1；FLBAS32h則是另一個編碼。'),
 ('Complete：NSID3:0、SFPI4','SFPI為操作期間最小剩餘百分比；全體namespace操作強制0。','它是剩多少，不是做完多少；不以0獨立判斷成功。'),
 ('FNVMS5：INCPLTF bit1、FNVME bit0','INCPLTF1表示已修改資料卻失敗，此時FNVME也須1；FNVME0表示成功，bits7:2保留。','03h是部分或全部資料已改動的失敗，不能安全假設資料原樣不變。'),
 ('CINFO7:6；INFO9:8；11:10保留','CINFO廠商補充；INFO bits15:1保存CQE status若存在，無CQE時0；bit0可能保存Phase。','先看FNVMS，再解INFO；INFO0不單獨證明成功。'))

example('B250','Sanitize Start保存啟動參數與清除對象，不回報完成進度。',
 'NSIDFFFFFFFFh、SCDW10的SANACT2表示整個subsystem的block erase起始事件；SANICAP是當時能力，不是清除進度的bitmap。',
 'Sanitize Start preserves initiation parameters and target, not completion progress.')
example('B251','Sanitize Completion要讀SOS；SPROG最大值不等於成功。',
 'NSID7、SOS3、SPROGFFFFh仍表示namespace7的清除失敗；CINFO只有在知道廠商定義時才能進一步解原因。',
 'Sanitize Completion requires SOS; maximum SPROG does not establish success.')
example('B451','SANACT先選清除方法，OWPASS與OIPBP只在overwrite有意義。',
 'SANACT3、OWPASS0代表overwrite16次，不是0次；若SANACT2則忽略OWPASS，不能再報「block erase做16次」。',
 'SANACT selects the method; overwrite pass count and inversion apply only to overwrite.')
example('B452','SCDW11保存overwrite pattern，不是byte長度或完成碼。',
 'SCDW11=AAAAAAAAh、OIPBP1表示overwrite輪次間反相pattern；若動作不是overwrite，不能把這個數字解成有用的清除參數。',
 'SCDW11 is the overwrite pattern, not a transfer length or completion code.')
example('B312','SSTAT把作業結果、覆寫輪次、驗證與清除範圍狀態放在不同bits。',
 'SOS1搭GDE0並不矛盾：清除可以成功，後來又有資料寫入。PEL裡的副本只反映完成事件當時，不能當今天GDE的值。',
 'SSTAT separates outcome, overwrite passes, verification and erased-scope state.')
group('sanitize-fields','讀出清除的對象、要求與結果','先以subsystem目標解Figures451／452的啟動參數，namespace目標另用Figure454；Figure312取SPROG／SSTAT，供250／251事件解碼。ET0E無ED的規則見共同外框與事件類型組。',['B250','B251','B451','B452','B312'],
 ('Start ED：SANICAP3:0、SCDW10 7:4、SCDW11 11:8、NSID15:12','前三欄保存當時控制器能力與原始命令Dwords；NSID為單一目標或FFFFFFFFh整個subsystem。','ET09新版ED16 bytes；讀舊ETR前不能先假設尾端有NSID。'),
 ('SCDW10 SANACT2:0、AUSE3','SANACT1退出failure、2block erase、3overwrite、4crypto erase、5退出verification；0／6／7保留。AUSE1選unrestricted處理，0restricted；非啟動動作忽略。','開始事件是進入處理狀態；不把所有SANACT代碼都當成會觸發start。'),
 ('SCDW10 OWPASS7:4、OIPBP8、SCDW11 OVRPAT31:0','overwrite次數1～15直接表示、0表示16；OIPBP1各次間反相pattern，OVRPAT為32-bit pattern。非overwrite忽略這些欄。','OWPASS2且patternAAAAAAAAh的反相值為55555555h。'),
 ('SCDW10 NDAS9、EMVS10、PREQ11','NDAS要求清除後不deallocate，仍受SANICAP.NDI與回應模式影響；EMVS要求成功後進verification；PREQ要求Purge結果，須支援SPRRS。bits31:12保留。','NDAS1不是無條件保留allocation；EMVS1也不是已進驗證的證明。'),
 ('Complete ED：SPROG1:0、SSTAT3:2、CINFO5:4、NSID11:8','CINFO為廠商結果補充，bytes7:6保留。SPROG進度刻度n/65536，Media Verification或非SOS2時為FFFFh。','8000h在可用的處理進度情境是50%；FFFFh須先讀SOS與狀態。'),
 ('SSTAT SOS2:0、OPC7:3','SOS0未曾sanitize、1成功、2處理中含verification／post-verification、3失敗、4成功但未預期deallocate，5～7保留。OPC是完成的overwrite輪次；非overwrite或namespace目標為0。','OPC2表示已完成2輪，不是要求做2輪；要求看OWPASS。'),
 ('SSTAT GDE8、MVCNCLD9、NDE10','GDE描述自出廠或最近成功subsystem sanitize後未再寫user data且未啟用PMR；MVCNCLD描述EMVS驗證因配置變更或相關reset被取消；NDE在namespace目標描述自建立或最近成功涵蓋該namespace清除後未再寫user data。','GDE／NDE是不同範圍，不能拿某namespace的NDE1推論整個subsystem無資料。'),
 ('SSTAT PRGD11、15:12保留','只有SPRRS受支援、PREQ1且SOS1的成功條件下才依Purge結果回報；其餘為0。','PRGD0不能脫離能力、請求與SOS就判斷作業失敗。'))

example('B454','Namespace Sanitize的PREQ在bit4，不在一般Sanitize的bit11。',
 'namespace目標的SCDW10=0000041Ch：SANACT4、AUSE1、PREQ1、EMVS1；bit4不是要求overwrite1次。這是依命令種類選格式的必要差別。',
 'Namespace Sanitize places PREQ at bit4 rather than ordinary Sanitize bit11.')
group('namespace-sanitize','同樣的SCDW10名稱，不同目標要換格式','Figure250同時記錄namespace與subsystem清除。遇到namespace目標，要補用Figure454解原始命令，不把Figure451的overwrite欄位套過來。',['B454'],
 ('SANACT2:0','1退出failure，4啟動namespace crypto erase，5退出verification；其他值保留。','不把值2／3解成namespace block erase／overwrite。'),
 ('AUSE3；PREQ4；EMVS10','AUSE1unrestricted、0restricted；PREQ要求Purge、須SPRRS支援；EMVS1要求成功後進驗證。非啟動動作忽略AUSE／EMVS。','41Ch=400h+10h+8h+4h，與一般Sanitize bit11的PREQ不同。'),
 ('保留欄位','bits9:5、31:11保留；此命令沒有overwrite pattern用途的CDW11。','不從保留的SCDW11數值推論曾執行overwrite。'))

example('B242','ET05的ED先有子類代碼，再有由子類選定的AHEI。',
 'ED前2 bytes=0008h、後面AHEI17 bytes：可按unexpected-power-loss結構解。若前2 bytes改為000Bh，同一批17 bytes就不能仍照電源事件讀。',
 'ET05 ED starts with a subtype code that determines its AHEI layout.')
example('B243','子類表是格式分派表，不是錯誤嚴重程度由小排到大。',
 '06h用Critical Warning，0Ah用完整CQE，0Bh用ready-timeout狀態；數字0Bh比06h大，不代表前者一定比較嚴重。',
 'The subtype table selects layouts, not a numeric ranking of severity.')
group('hardware-codes','先用子類找到正確的證據格式','Figure242：NSHEEC bytes1:0，bytes3:2保留，AHEI從4起。ETR2中未能提供的欄位依規則為0，除非該欄另有指定。子類支援由廠商決定。',['B242','B243'],
 ('01h／02h／03h：PCIe錯誤','分別是correctable、uncorrectable non-fatal、uncorrectable fatal；AHEI用Figure245。','先分correctable與uncorrectable，才能選狀態／mask register。'),
 ('04h：PCIe link status change','因嘗試修正不可靠link而改變；AHEI是PCIe Link Status register快照，不是Figure245整份結構。','這個數值保存連線狀態，不能解成UPL計數或套AER各slot。'),
 ('05h：PCIe link not active；09h：fatal status','05是非預期離開Data Link Active；09是CSTS.CFS設1。兩者沒有AHEI。','ED只含4-byte共同前綴也可以是完整事件。'),
 ('06h：Critical Warning','AHEI為SMART byte0的Critical Warning格式，在事件發生時的值。','值04h表示可靠度警告bit2，不是錯誤子類04h。'),
 ('07h：Endurance Group warning','AHEI byte0為該Group警告、byte1保留、bytes3:2為Group ID；值反映加入log時狀態。','Group ID3不是TNEV3；不同Group可能有不同警告。'),
 ('08h：Unexpected Power Loss','AHEI依Figure244。','用128-bit累計UPL與特殊情境位元解讀，不按PCIe表。'),
 ('0Ah：Media/Data Integrity','AHEI為完整CQE；Access Denied SC86h與Deallocated/Unwritten SC87h不在此觸發類型。','CQE帶命令識別與狀態，不是出錯LBA清單。'),
 ('0Bh：Controller Ready Timeout Exceeded','AHEI依Figure246。00h及0Ch～FFFFh未定義的碼不按已知格式解讀。','先檢查外框長度再交給對應表，未知子類仍保留原始bytes。'))

example('B244','UPLOA只標一種帶外管理造成的特殊掉電條件，不是所有非預期掉電的總開關。',
 'UPL=12、UPLOA=0：已記錄到累計第12次非預期掉電，只是未標示該特殊情境。不能因UPLOA0把這次事件改判正常shutdown。',
 'UPLOA marks a specific out-of-band condition, not whether all unexpected power loss occurred.')
group('power-loss','累計次數與特定情境分開','Figure244的offset相對AHEI起點，不是ED或事件起點。',['B244'],
 ('UPL bytes15:0','128-bit累計非預期掉電次數，值為事件當時所記。','不要只讀低4 bytes，或把它當掉電發生的Timestamp。'),
 ('UPLI byte16：UPLOA bit0','僅在SHST01／10且主電源掉落、媒體因Ignore Shutdown1的帶外Admin操作仍未shutdown時設1。bits7:1保留。','SHST10不是在所有情況都保證媒體當下已不用電；此bit描述明確的例外條件。'))

example('B245','PCIEAERS決定AER資訊能否讀；error code再決定correctable或uncorrectable的register。',
 'NSHEEC01h且PCIEAERS1時讀correctable狀態與mask；NSHEEC03h改用uncorrectable。PCIEAERS0時後面的AER區可以省略或清零，不應把零報為「PCIe沒有錯」。',
 'PCIEAERS gates AER data, while the subtype selects correctable or uncorrectable registers.')
group('pcie-errors','把快照槽位與原始PCIe register分開','此處AER指PCIe Advanced Error Reporting，不是NVMe的Asynchronous Event Request。Figure245定義保存位置；原PCIe register的逐bit意義不是由這張NVMe表定義。',['B245'],
 ('PCIEDSR1:0；PCIEAS2 bit0 PCIEAERS','前者保存Device Status；後者1表示報AER，0表示AER區省略或清零。PCIEAS bits7:1及bytes15:3保留。','事件存在且AERS0仍可有Device Status，不能推成無錯誤。'),
 ('PCIEAES31:16；PCIEAEM47:32','各佔16-byte保存槽位，分別為所選correctable／uncorrectable的Error Status與Mask register內容。','slot寬度不表示原生register就是128bits；status和mask不能互換。'),
 ('PCIEAHLR63:48；PCIEATPLR79:64','分別為Header Log與TLP Prefix Log register快照，存在與內容依支援。','沒有實作的prefix資料不能解成16-byte全零的有效封包。'),
 ('AHEI解讀邊界','先確定子類和PCIEAERS，再保留各register原始值；本NVMe外框未提供的PCIe bit碼不能自行命名為某個link速率或故障原因。','能確定「哪個register在何時被保存」，不憑這張外框表捏造逐bit含義。'))

example('B246','CRIME保存當時ready模式，其他位元描述各範圍是否超過等待限制。',
 'CST=0Bh：CNR1、ACMNR0、NNR1、CRIME1。控制器等待使用CRIMT，namespace等待仍用CRWMT；不能因同一byte就認為兩者共用相同timeout。',
 'CRIME captures ready mode; other bits describe which readiness deadlines were exceeded.')
group('ready-timeout','同一啟用時點，兩種等待尺度','AHEI byte0為CST；bytes3:1保留。計時從CC.EN 0→1啟用控制器開始，CRTO是Controller Ready Timeouts。',['B246'],
 ('CST bit3：CNR','控制器未能在模式所選時間內無錯處理至少一筆命令；CRIME0用CRWMT，1用CRIMT。','CNR1不是說每個namespace都一定壞掉。'),
 ('bit2 ACMNR；bit1 NNR','ACMNR表示至少一筆Admin命令所需媒體未在CRWMT內就緒；NNR表示至少一個附接namespace未在CRWMT內就緒。','兩位可以獨立觀察，Admin所需媒體與namespace範圍不同。'),
 ('bit0 CRIME；bits7:4保留','保存事件時CC.CRIME：0連同media就緒模式，1media獨立模式。','CRIME是模式，不是另一個錯誤；CST1只設模式位。'))

example('B252','每一格說的是Feature事件的記錄政策，不是在宣告能否使用Feature。',
 'FID14h在I/O欄P、Admin欄O；選錯控制器類型就會把選用記錄讀成禁止。Timestamp0Eh的P另有ET03處理，不能推論不支援時間設定。',
 'Each cell specifies feature-event logging policy, not whether the feature itself is supported.')
group('feature-policy','以控制器類型和FID讀記錄政策','本表只呈現I/O與Admin兩欄。O選用、P禁止、NR不建議；M代表必備但這些列沒有M。成功且改值、又支援該Feature記錄時須記；同值成功時可記。',['B252'],
 ('I/O O；Admin P','01h Arbitration、06h Volatile Write Cache、07h Number of Queues、13h Predictable Latency Mode Config、19h I/O Command Set Profile、1Ah Spinup Control、1Dh Flexible Data Placement、1Eh其Events、82h Reservation Notification Mask、83h Reservation Persistence。','同一FID不能略過控制器類型直接說一定可記。'),
 ('I/O P；Admin O','14h Predictable Latency Mode Window。','P限制本事件種類的記錄，不是要求把已存在記錄刪除。'),
 ('兩欄P；兩欄NR','0Eh Timestamp為P。02h Power Management、0Bh Asynchronous Event Configuration、80h Software Progress Marker為NR。','NR比禁止寬，不可改寫成must not。'),
 ('兩欄O：中斷、熱管理與記憶體','04h Temperature Threshold、08h Interrupt Coalescing、09h Interrupt Vector Configuration、0Ch Autonomous Power State Transition、0Dh Host Memory Buffer、0Fh Keep Alive Timer、10h Host Controlled Thermal Management、11h Non-Operational Power State Config、12h Read Recovery Level Config。','O不是說每台裝置都會保留這類歷史。'),
 ('兩欄O：設定與電源','16h Host Behavior、17h Sanitize Config、18h Endurance Group Event Config、1Bh Power Loss Signaling、1Fh Namespace Admin Label、21h Controller Data Queue、22h CDP、23h Power Limit、24h Power Threshold、25h Power Measurement、26h Voltage Threshold、27h Voltage Measurement。','這裡只分類記錄政策，各Feature的參數不能共用一套CDW11格式。'),
 ('兩欄O：管理資料與保護','78h Embedded Management Controller Address、79h Host Management Agent Address、7Dh Enhanced Controller Metadata、7Eh Controller Metadata、7Fh Namespace Metadata、81h Host Identifier、84h Namespace Write Protection Config、85h Boot Partition Write Protection Config。','Metadata這幾個FID是管理屬性，不是FLBAS控制的每LBA metadata。'),
 ('Command Set自訂列','03h、05h、0Ah、15h、1Ch、20h、28h：Base把政策交給對應command set。','不要把空白／引用另一份表猜成O或P；本篇NVM§4.1.4.4沒有重定義這些列。'))

example('B253','DWC算Dwords、MBC算bytes、LCCDW0只決定是否再有4 bytes。',
 'SFEL0008000Bh：DWC3、MBC8、LCCDW01。ED是28 bytes，最後4 bytes在offset24；不是把DWC3先加1再乘4。',
 'DWC counts Dwords, MBC counts bytes, and LCCDW0 adds an optional four-byte result.')
group('feature-layout','沿長度找到命令、buffer與完成值','所有offset相對ED；SFEL本身先佔4 bytes。不要把這裡的直接計數DWC套用Get Log NUMD的0-based規則。',['B253'],
 ('SFEL3:0：DWC2:0','有效1～6，0／7保留；保存CDW10起連續Dwords，直到最高非保留CDW，中間保留CDW也算進去。','DWC3表示CDW10、11、12，不是CDW10～13。'),
 ('SFEL：LCCDW0 bit3；MBC31:16','bit3=1表示保存完成DW0；MBC為buffer bytes數，0沒有buffer；bits15:4保留。','0008000Bh的8是8 bytes，不是8Dwords。'),
 ('CDWS起4；MBUF起4+4DWC','CDWS長4DWC；MBUF長MBC。','DWC3時MBUF從16開始；MBC0時後續欄位緊接16。'),
 ('CCDW0起4+4DWC+MBC','只在LCCDW01時存在，長4；ED總長4+4DWC+MBC+4×LCCDW0。','它不是CQE的Status或全部16-byte CQE。'))

example('B256','PS的requested freeze與change error要合讀，PED再依PERID解。',
 'PS=03h表示要求freeze且變更有錯誤；不能因bit1=1就報告已成功freeze。PED從12開始，不是把保留的bytes11:2當設定值。',
 'Read requested freeze alongside change error, then interpret PED by PERID.')
group('personality','把請求、錯誤與personality專屬資料分開','Figure256是ET0F獨立格式，不套Set Feature的SFEL。Manufacturing Default要求只產生一筆相關事件。',['B256'],
 ('PS0：CDPRFS bit1、CDPCE bit0','bit1為要求的freeze狀態，bit0表示personality change error；bits7:2保留。','03h不是「兩種personality已成功凍結」。'),
 ('PERID1；bytes11:2保留','PERID選personality；設定、更改freeze狀態及安全條件自動freeze可觸發此事件。','PERID是識別值，不是數量。'),
 ('PED由12起，長EL−VSIL−12','保存該personality的Set Features資料buffer，具體結構依PERID而異；本共同表不定義所有personality的內部bits。','可以定位保存資料，但不能拿另一PERID的payload欄位照套。'))

example('B257','EEID與UEID分別是呈現出去與底層的識別值，寬度還要看OTYP。',
 'ESUBID2、OTYP2、EEID5、UEID42表示新增Exported namespace5對應Underlying namespace42；兩個不同數字不是錯誤，而是映射兩端。',
 'EEID and UEID identify exported and underlying objects, with widths selected by OTYP.')
group('export-mapping','只讀實體變更紀錄中的映射','ET10的ED16 bytes。此處只教物件、動作與ID關係，不展開建立或傳輸流程。',['B257'],
 ('ESUBID1:0；OTYP2','ESUBID識別被改變的exported subsystem；OTYP0建立、1刪除subsystem；2加namespace、3刪namespace；4加controller、5刪controller；6加port、7刪port；8允許主機清單改變、9限制存取改變，其他保留。','OTYP4時EEID5是一個controller ID，不能仍稱namespace5。'),
 ('bytes7:3保留；EEID11:8','namespace動作2／3用32-bit ID；0／1／8／9的低16bits是exported subsystem ID，4／5是controller ID，6／7是port ID，各自高16bits保留。','namespace ID可以大於65535，不該把EEID一律截成16-bit。'),
 ('UEID15:12','0／1／8／9動作清0；2／3底層namespace32-bit；4／5底層controller低16；6／7底層port低16，其餘高位保留。','建立subsystem時UEID0不是底層namespace0，而是該動作規定的零值。'))

example('B258','ETDE的ED是描述子串列，描述子數量由長度走到末端而得。',
 '第一描述子11 bytes、第二14 bytes，ED共25。清單沒有另一個固定的「兩筆」count欄位；先讀各VSEDL才能找到第二筆與結尾。',
 'ETDE ED is a descriptor list whose end follows from lengths, not a separate count field.')
example('B259','每個描述子有6-byte前綴，VSEDL只計後面的資料。',
 'VSEDL5代表描述子總長11，下一筆從本筆起點加11；若只加5，會落在第一筆前綴尚未結束的位置。',
 'Each descriptor has a six-byte prefix excluded from VSEDL.')
example('B260','相同bytes可以因VSEDT不同而有完全不同的讀法。',
 '8個FFh在VSEDT4是有號64-bit二補數−1；在VSEDT3只是廠商binary資料，不能擅自選有號整數或byte order。',
 'Identical bytes can mean different things under different VSEDT types.')
group('vendor','描述子串列、前綴與型別逐層解','Figure258是串列，259是一筆，260選資料型別。UUID Index選擇相應的vendor事件，廠商自行定義的事件仍可回報；不得把索引當全域事件序號。',['B258','B259','B260'],
 ('VSEC1:0；VSEDT2；UIDX3','VSEC為同類vendor事件一致使用的碼；VSEDT選型別；UIDX為事件發生時使用的UUID Index。','沒有vendor碼表，不能把VSEC0010h直接翻成過熱。'),
 ('VSEDL5:4；VSED從6起','VSEDL只計資料，下一描述子前進6+VSEDL；整個串列不得超過ED邊界。','名稱TEMP含零結尾5bytes，描述子11bytes。'),
 ('VSEDT1：Event Name；2：ASCII String','皆以零字元結尾；有Event Name時必須第一描述子，名稱與相應事件碼保持一致。','字串長度包含終止零，不是只計可見字元。'),
 ('VSEDT3：Binary；4：Signed Integer','binary的byte order由廠商定義；integer為64-bit有號二補數。0與5～FFh保留。','型別4應是8-byte內容，不能把任意長度資料截短硬解。'),
 ('與VSI、TCG的界線','這一組只解ETDE的ED；共同外框VSI是另一段。ETDF的ETR／ED由TCG保留定義，不沿用這份描述子格式。','外框可保留並跳過未知內容，不代表已知其中安全事件的語意。'))

example('B338','Identify提供的是能力與上限；事件內保存的副本則反映當時值。',
 'LPA bit4=1但PELS4，不表示只有4筆事件；它表示支援PEL且最大256KiB。當時保存的SANICAP和今天查到的能力，也不應不加區別地互換。',
 'Identify supplies capabilities and limits; copies embedded in events describe the captured state.')
group('capabilities','只補PEL事件用到的Identify欄位','Figure338是長表，本篇只取LPA／PELS、溫度門檻、FNA及SANICAP；其他能力未因此全部納入。',['B338'],
 ('LPA byte261：PES bit4、LPEDS bit2','PES1支援PEL；LPEDS1支援extended Get Log長度與offset。PELS bytes355:352以64KiB為單位表示最大PEL大小。','PELS4=4×65536=262144 bytes，不是TLL固定值。'),
 ('WCTEMP267:266；CCTEMP269:268','警告與嚴重綜合溫度門檻，Kelvin；0未提供門檻，Base1.2以上應回非零。','讀THRESH1／2時選相應門檻，不把這兩個值加在一起。'),
 ('FNA byte524','來源是Identify Controller；bits3:0的完整作用在Format欄位組統一說明。','Figure248保存的FNA只佔一byte，不是Namespace Identify整份資料。'),
 ('SANICAP331:328：bits2:0','OWS bit2、BES bit1、CES bit0分別支援overwrite、block erase、crypto erase。','值6支援overwrite與block erase，不支援crypto erase。'),
 ('SANICAP bits3／4／5','VERS bit3為subsystem驗證狀態支援；NVERS bit4為namespace驗證支援；SPRRS bit5為Purge要求／回報支援；bits28:6保留。','VERS與NVERS不互相代替；PREQ只有SPRRS支援時才有定義。'),
 ('SANICAP NDI bit29','1表示NDAS不一定可保留allocation：回應模式NODRM1時仍deallocate；NODRM0或無該Feature時，NDAS1被拒絕。NDI0支援NDAS；NDAS0時NDI不改變處理。','Start保存NDAS1，不足以單獨斷言作業後一定沒deallocate。'),
 ('SANICAP NODMMAS31:30','描述NDAS1時清除處理是否另外修改媒體：0舊版／不支援時未定義，1不額外修改，2會額外修改，3保留。','這是額外媒體修改行為，不是某一種sanitize方法的成功碼。'))

for k,t,w,e in [
 ('B203','DPTR指向接收資料的buffer，不是PEL內的事件offset。','主機buffer位址可以很大，讀log offset0仍從header開始；ACT3至少準備512-byte可寫入空間。','DPTR addresses host output memory rather than selecting an offset inside PEL.'),
 ('B204','NUMDL用Dwords且從0計數，LSP則放本log的ACT。','NUMDL127、ACT1、LID0Dh合成007F010Dh；把512直接放NUMDL會要求2052 bytes。','NUMDL is a zero-based Dword count, while LSP carries the log-specific action.'),
 ('B205','NUMDU補長度高位，LSI是另一個log專屬選擇欄。','NUMDU1、NUMDL0代表65537Dwords而非65536；本篇PEL沒有把LSI定義成NSID或event type。','NUMDU extends length; LSI is a separate log-specific selector.'),
 ('B206','OT0時LPOL是byte位置，OT1才是表內項目編號。','offset512寫00000200h；不是512÷4=128。NUMD用Dwords不表示offset也用Dwords。','With OT0, LPOL is a byte position, not a Dword count or entry index.'),
 ('B207','LPOU是同一個64-bit位置的高32bits，不是第二個獨立offset。','LPOU1、LPOL0表示4294967296-byte位置；不是第1筆事件。一般小型PEL讀取高位為0。','LPOU supplies the upper half of one 64-bit position.'),
 ('B208','OT與UIDX各有用途，CSI也不是PEL事件種類。','OT0、UIDX0可按byte讀標準資料；不可以把ET06寫CSI6，期待只回Namespace Change。','OT and UIDX select offset interpretation and UUID context, not event type.'),
 ('B209','LID0Dh屬subsystem範圍，不由CSI挑事件格式。','同一subsystem內，不把NSID7當成只取namespace7事件的filter；此log要求NSID0或FFFFFFFFh。','LID0Dh has subsystem scope and does not use CSI as an event-format selector.'),
 ('B210','支援清單每LID固定4bytes，可用LID算出描述子位置。','0Dh=13，因此PEL能力描述子起點13×4=52；52是byte offset，不是LID52。','The supported-log list has four bytes per LID, making descriptor location computable.'),
 ('B211','先確認LSUPP，再看IOS與LIDSP，不能把未支援列的其他bits當能力。','描述子00010001h是LSUPP1、IOS0、LIDSP1：支援PEL與ECRH，但未宣告index offset。','Check LSUPP before interpreting IOS and log-specific capability bits.'),
]:example(k,t,w,e)
group('get-log','外層命令怎麼組成一次讀取','Figures203～211只取PEL所需格式與LID0Dh列。byte offset、Dword計數、事件index是三種不同單位。',['B203','B204','B205','B206','B207','B208','B209','B210','B211'],
 ('DPTR；NSID','DPTR指向主機接收buffer；subsystem範圍只用NSID0或FFFFFFFFh，其他值回Invalid Field in Command。','NSID7不能拿來篩選只看namespace7的事件。'),
 ('CDW10 NUMDL31:16、RAE15、LSP14:8、LID7:0','LID0Dh；LSP低2bits即ACT；RAE控制相應非同步事件確認，非此用途時應0。','命令裡ACT在bits9:8；ECRH能力則是另一個資料結構的bit。'),
 ('CDW11 NUMDU15:0、LSI31:16','NUMD=(NUMDU<<16)|NUMDL，bytes=4×(NUMD+1)。PEL未定義LSI作篩選。無extended支援時使用舊有低12-bit長度限制。','512bytes→NUMD127；NUMD128→516bytes。'),
 ('CDW12 LPOL、CDW13 LPOU','合成64-bit位置；OT0時以bytes計、低2bits0保持Dword對齊。ACT2／3特例忽略此位置。','讀第512byte開始用LPO512；一筆事件可以跨兩次傳輸。'),
 ('CDW14 OT23、CSI31:24、UIDX6:0','OT0為byte、1為index且須該log的IOS支援與定義；PEL的CSI不使用。UIDX0未選UUID，1～127選清單項目；bits22:7保留。','不因log含很多事件就自行假設index模式可用；本篇流程固定OT0。'),
 ('Supported Log Pages bytes55:52','LID0Dh第13項；每項4bytes，LSUPP bit0先判斷支援，IOS bit1判斷index offset，LIDSP31:16放ECRH等專屬能力；bits15:2保留。','00010001h把ECRH放bit16，不能把它寫成bit0而覆蓋LSUPP。'),
 ('Figure209的Restore to Default Content欄','PEL列為N，描述指定的出廠設定復原，不是一般reset的通用持續性欄。','跨power cycle／reset保留的依據是PEL正文，不能只讀這個N。'))

example('B187','CA／FS先從命令bit欄取值，再分別放入韌體事件的整個bytes。',
 'Firmware Commit CDW10=0Ah：CA1、FS2；事件FCA=1、FSLT=2。不能把整個0Ah直接當FCA10。',
 'CA and FS are extracted from command bits before being stored as separate event bytes.')
example('B189','需要reset的完成碼可表示提交成功，但啟用尚待指定reset。',
 'SCT1、SC10h要求NVM Subsystem Reset，不能以一次Controller Reset就保證啟用；這也解釋為什麼後續ET04仍值得檢查。',
 'A reset-required completion may mean successful commitment but deferred activation.')
for k in ['B187','B189']:MEMBERS[k]='pel-firmware'
GUIDES['pel-firmware']['rows'].extend([
 ('原命令CA bits5:3、FS2:0、BPID31','CA與FS提取後放到事件FCA、FSLT。BPID只供Boot Partition動作，bits30:6保留；事件未另設BPID欄。','0Ah=(1<<3)|2，因此FCA1、slot2。'),
 ('SCT1的相關activation完成碼','SC0Bh需Conventional Reset；10h需Subsystem Reset；11h需Controller Level Reset；12h表示啟用超過MTFA限制、未啟用。這些碼不同於SCT0／SC0。','不把任何含reset字樣的結果統稱同一種重設即可。')])

for k,t,w,e in [
 ('B97','完整CQE至少16bytes，命令專屬回覆與通用狀態分開。','硬體子類0Ah保存CQE時，DW0不一定是出錯LBA；它仍按原命令定義。','A full CQE separates command-specific results from common completion metadata.'),
 ('B98','SQID與SQHD各回答命令從哪個queue來與當時消耗到哪裡。','SQID3、SQHD8不是namespace3與第8筆PEL事件；SQHD是建立CQE當時的queue head。','SQID identifies the source queue; SQHD captures its consumption position.'),
 ('B99','CID要配SQID識別命令，Phase只用來辨認queue entry更新。','CID7可以在不同SQ各自出現；不能只用CID7把兩筆歷史CQE視為同一命令。','Combine CID with SQID; Phase describes queue-entry freshness rather than operation success.'),
 ('B101','Status先拆SCT與SC，再讀重試及更多資訊位元。','SCT2／SC80h與SCT0／SC80h不能只因SC相同就翻成同一錯誤；DNR0也不是重試保證成功。','Decode SCT/SC together, then retry and additional-information flags.'),
]:example(k,t,w,e)
group('completion','保存的CQE怎麼接到事件結果','Figures97～99只取PCIe共同CQE；Figure101的bit號相對CQE DW3。Format INFO則保存高半部，包括Status與可能的Phase。',['B97','B98','B99','B101'],
 ('CQE bytes7:0：DW0／DW1','兩者依原命令定義，未使用者保留。','Set Feature事件可只保留DW0，硬體子類0Ah則保存整份CQE。'),
 ('DW2：SQID31:16、SQHD15:0','對應CQE bytes11:10與9:8，識別SQ與建立completion時的SQ head。','它們不是NSID或PEL offset。'),
 ('DW3：CID15:0、P16、STATUS31:17','CID配SQID辨識命令；P為Phase Tag；Status不包含P。','Phase1不等於命令成功。'),
 ('DW3：SC24:17、SCT27:25','SC是類型內的碼，SCT選類型；SCT0／SC0表示成功。','解Format INFO時位址已右移16bits，所以SC在INFO8:1、SCT在11:9。'),
 ('DW3 DNR31、M30、CRD29:28','DNR1相同命令重送預期仍失敗；M1有額外Error Information；CRD只在DNR0且ACRE1有意義，0不延遲，1～3選CRDT1～3等待值，其餘情況保留。','CRD2是選第2個等待參數，不是固定2秒；DNR0只說可能成功。'))

example('B745','Power Measurement Type說明量哪個對象，不決定Watt縮放倍率。',
 'IPM.PMT0為subsystem總功率，PMTCh為廠商定義；scale2才表示每單位0.01W。把PMT0看成未回報會漏掉有效測量。',
 'Power Measurement Type selects the measured object, independently of the Watt scale.')
group('power-type','辨認功率測量的對象','Figure745只補SMART IPM的PMT。其他power measurement機制不在本篇展開。',['B745'],
 ('PMT0；1h～Bh；Ch～Fh','0為subsystem總功率；1～B保留；C～F廠商自訂。','是否有回報由IPM scale判斷，PMT0本身是有效類型。'))

# key: (section, actual PDF viewer pages, teaching unit). Primary tables use
# the exact requested sections; all other rows are bounded dependencies.
SOURCES={
 'B232':('5.2.13.1.14','272','context'),
 'B233':('5.2.13.1.14','273-275','layout'),
 'B234':('5.2.13.1.14','275-276','layout'),
 'B235':('5.2.13.1.14.1','277','context'),
 'B236':('5.2.13.1.14.2','277','purpose'),
 'B237':('5.2.13.1.14.2.1','278','health'),
 'B238':('5.2.13.1.14.2.2','278','time'),
 'B239':('5.2.13.1.14.2.3','279','time'),
 'B240':('5.2.13.1.14.2.4','279','time'),
 'B241':('5.2.13.1.14.2.4','279-280','time'),
 'B242':('5.2.13.1.14.2.5','280','hardware'),
 'B243':('5.2.13.1.14.2.5','280-281','hardware'),
 'B244':('5.2.13.1.14.2.5','282','hardware'),
 'B245':('5.2.13.1.14.2.5','282-283','hardware'),
 'B246':('5.2.13.1.14.2.5','284','hardware'),
 'B247':('5.2.13.1.14.2.6','284-285','namespace'),
 'B248':('5.2.13.1.14.2.7','286','namespace'),
 'B249':('5.2.13.1.14.2.8','286-287','namespace'),
 'B250':('5.2.13.1.14.2.9','287','sanitize'),
 'B251':('5.2.13.1.14.2.10','287-288','sanitize'),
 'B252':('5.2.13.1.14.2.11','288-289','features'),
 'B253':('5.2.13.1.14.2.11','290','features'),
 'B254':('5.2.13.1.14.2.12','290','health'),
 'B255':('5.2.13.1.14.2.13','291-292','health'),
 'B256':('5.2.13.1.14.2.15','293','features'),
 'B257':('5.2.13.1.14.2.16','293-294','extensions'),
 'B258':('5.2.13.1.14.2.17','295','extensions'),
 'B259':('5.2.13.1.14.2.17','295','extensions'),
 'B260':('5.2.13.1.14.2.17','295-296','extensions'),
 'N112':('4.1.4.4','77','namespace'),
 'B338':('5.2.14.2.1','381,383,387-388,390,399','purpose'),
 'B203':('5.2.13','239','context'), 'B204':('5.2.13','239','context'),
 'B205':('5.2.13','240','context'), 'B206':('5.2.13','240','context'),
 'B207':('5.2.13','240','context'), 'B208':('5.2.13','240-241','context'),
 'B209':('5.2.13','241-243','context'),
 'B210':('5.2.13.1.1','243','context'), 'B211':('5.2.13.1.1','243-244','context'),
 'B213':('5.2.13.1.3','247-251','health'), 'B214':('5.2.13.1.3','251','health'),
 'B221':('5.2.13.1.8','260','health'), 'B223':('5.2.13.1.9','262-263','health'),
 'B480':('5.2.30.1.8','496-497','time'),
 'B187':('5.2.9','229','time'), 'B189':('5.2.9','230','time'),
 'B446':('5.2.25','472-473','namespace'),
 'N123':('4.1.5.1','85-87','namespace'), 'N134':('4.1.6','112-113','namespace'),
 'B195':('5.2.11','234-235','namespace'), 'N91':('4.1.1','63','namespace'),
 'B451':('5.2.26','476','sanitize'), 'B452':('5.2.26','477','sanitize'),
 'B454':('5.2.27','479','sanitize'), 'B312':('5.2.13.1.38','340-342','sanitize'),
 'B97':('4.2.1','170','hardware'), 'B98':('4.2.1','170','hardware'),
 'B99':('4.2.1','171','hardware'), 'B101':('4.2.3','171-172','hardware'),
 'B745':('8.1.20','704','health'),
}
