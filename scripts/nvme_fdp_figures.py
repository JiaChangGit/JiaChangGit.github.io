"""FDP figure lessons; each figure has a distinct takeaway and worked reading."""
EXAMPLES = {}
GUIDES = {}
MEMBERS = {}


def example(n, takeaway, worked, en, source='base'):
    EXAMPLES[source,n] = dict(takeaway=takeaway, example=worked, en=en)


def group(key, title, relation, numbers, *rows, source='base'):
    ident = 'fdp-'+key
    GUIDES[ident] = dict(id=ident,title=title,relation=relation,rows=list(rows))
    for n in numbers:
        MEMBERS[source,n] = ident


def token(f):
    return ('base' if f['source_id']=='NVME-BASE-2.4' else 'nvm',int(f['number']))


def lesson(f):
    return EXAMPLES[token(f)]


def guide(f):
    return GUIDES[MEMBERS[token(f)]]


example(70,'RUH 在每個 Reclaim Group 各參照一個 RU，不是一個 RUH 只有一塊全域媒體。','圖中每條 RUH 橫跨所有 RG，往每個 RG 連一個目前 RU。假設 4 個 RG、4 個 RUH，共有 16 個目前參照；這不代表整個群組總共只有 16 個 RU。','Each RUH references one RU per Reclaim Group, not one global media unit.')
example(730,'NSID 選映射表，PID 選 RGID 與 PHNDL，再由 PHNDL 查到 RUH。','圖中 PHNDL 0 對 RUH 1，PHNDL 1 對 RUH NRUH-1。帶 RGID=2、PHNDL=1 的 Write 要沿第二列接到最上方 RUH，再到 RG2；不要沿 PHNDL 1 直接找 RUH 1。','NSID chooses the mapping, PID supplies RGID and PHNDL, and PHNDL selects the RUH.')
group('model','把資源層次接到一筆寫入','兩張圖沒有規定硬體電路配置；外框表示資源所屬，線表示目前的參照與查表關係。',[70,730],
 ('Endurance Group → RG → RU','RGID 從 0 到 NRG-1；RG 內有多個可輪替使用的 RU。','NRG=4 時 RGID=0、1、2、3；不是 1、2、3、4。'),
 ('RUH 0…NRUH-1 的跨 RG 參照','每個 RUH 在每個 RG 選一個 RU；同時一個 RU 最多給一個 RUH 參照。','RUH 3/RG2 與 RUH 3/RG1 的目前 RU 不同。'),
 ('NSID → PHNDL → RUHID','PHNDL 是 namespace 清單索引，清單內容才是 RUHID。','清單 [1,3] 的 PHNDL 1 對 RUHID 3。'),
 ('寫滿後的箭頭改向','該 RUH 在同一 RG 參照新的空 RU；PID 數字可保持不變。','舊 RU 內仍有效的 LBA 不會因為箭頭改向就消失。'))

example(731,'Initially Isolated 的不同 RUH，搬移後可以在同一 RG 合併資料。','看右側 RU α 的多種來源顏色：X、Y、Z 的舊 RU 資料可以被搬到同一個目的 RU。左側仍各有目前寫入 RU，不能把右側合併誤讀成所有新 Write 都直接混寫。','Initially Isolated data from different RUHs may be combined during relocation within one RG.')
example(732,'Persistently Isolated 允許搬移，但搬移目的 RU 必須維持 RUH 來源分離。','X 的資料可從多個 Previous RU A′ 搬到 RU α；Y 進 RU β，Z 進 RU γ。重點是不同來源的箭頭沒有在同一目的 RU 合流，不是「不能有垃圾回收」。','Persistently Isolated data may move, but destination RUs preserve separation by originating RUH.')
example(295,'RUHT 決定內部搬移後的隔離要求，並非決定 PID 的位元格式。','RUHT=1 是 Initially Isolated、2 是 Persistently Isolated；將 2 誤當成 RGIF=2 會改錯 PID 切割，因為 RGIF 在另一個配置欄位。','RUHT controls isolation after relocation, not the PID bit layout.')
group('isolation','讀來源與目的，不以顏色代替規則','圖中 Previous RU 是同一 RUH 先前寫入過的單位；目的 RU α／β／γ 是搬移目的的圖示名稱，不是要填入命令的值。',[295,731,732],
 ('RUHT：描述器 byte 0','1h 初始隔離；2h 持續隔離；0h、3h～BFh 保留；C0h～FFh 廠商定義。','遇到廠商值不擅自套用 1h 或 2h 的搬移限制。'),
 ('描述器 bytes 3:1','保留；每筆描述器總長 4 bytes。','第 i 筆在配置內的 byte offset 是 64+4×i。'),
 ('相同 RG 與來源 RUH','兩種類型皆在同一 RG 內搬移；RUHT=2 的目的 RU 只含同一 RUH 寫入的資料。','不同 namespace 共用 RUH 時，不能以 RUHT=2 推論 namespace 彼此隔離。'),
 ('目前 RU／Previous RU／搬移目的','三者是不同時點或用途；資料搬走不等於主機發了新 Write。','右側目的 RU 的內部寫入會影響 MBMW，而不增加對應的主機 HBMW。'))

example(293,'配置清單先給整份長度，索引從第 0 筆開始，每筆長度另由 DSZE 決定。','NUMFDPC=1 表示 2 筆；header 16 bytes、第 0 筆 DSZE=80，則第 1 筆從 byte 96 開始。FDPCIDX 要填 1，不是 96。','The configuration list has a total size, zero-based count encoding, and variable-sized indexed descriptors.')
example(294,'一筆配置把可用性、PID 格式、資源數量與大小分開提供。','FDPCV=1、NRG=4、NRUH=4、RGIF=2：可用候選有 4 個 RG、4 個 RUH，PID 高 2 bits 選 RG。RUNS=1 GiB 則是每 RU 名目大小，不是總群組容量。','A configuration separates availability, PID layout, resource counts, and nominal sizes.')
group('configuration','先取完整描述器，再判斷能否使用','Header 與描述器的 offset 都以 bytes 計；清單索引與 RUHID 則是項目編號。共同的保留欄不代表可自由塞入額外參數。',[293,294],
 ('Header NUMFDPC 1:0／VER 2／SZE 7:4','NUMFDPC+1 是配置數；VER=0；SZE 是整份 byte 數。第一筆從 16 開始，header 3 與 15:8 保留。','值 1、有兩筆各 80 bytes，SZE=16+160=176。'),
 ('DSZE 1:0／FDPA byte 2','DSZE 是含補齊的本筆長度。FDPA[7] FDPCV；[4] FDPVWC；[3:0] RGIF；[6:5] 保留。','FDPA=92h 表示有效、帶 volatile cache、RGIF=2。'),
 ('NRG 7:4／NRUH 9:8','直接計數，皆必須非零；前者數 RG，後者數 RUH 描述器。','NRG=4／NRUH=3 不是共 7 個 RU；每個 RUH 橫跨各 RG。'),
 ('MAXPIDS 11:10','Update 的 NPID 編碼最大值，採數量減 1，且小於 NRG×NRUH。','MAXPIDS=7 容許一次 8 個 PID；不等於只准 7 個。'),
 ('NNS 15:12','這份配置容許建立的 namespace 數。MNAN 非零時 NNS≤MNAN；MNAN=0 時 NNS≤NN。','NNS 是容量配置的 namespace 上限，不能拿 PID 的 PHNDL 位元數取代。'),
 ('RUNS 23:16／ERUTL 27:24','RUNS 為每個 RU 名目 bytes；ERUTL 為估計秒數，0 表示未回報。','RUNS=1073741824 是 1 GiB；ERUTL=0 不是 0 秒後必須換 RU。'),
 ('VSS byte 3／RUH list 64 起／VS／PAD','固定 64 bytes，加 4×NRUH、VSS，再補到 8-byte 邊界；PAD 清 0，28:63 保留。','NRUH=3、VSS=1：64+12+1=77，再補 3，DSZE=80。'))

example(296,'RGIF=0 且只有一個 RG 時，PID 的 16 bits 全部是 PHNDL。','NRG=1、RGIF=0、PHNDL=3 → PID=0003h；不要把高位 0 當成另外保留的一段 RGID，這個格式根本沒有切出 RGID。','With one RG and RGIF=0, all sixteen PID bits encode PHNDL.')
example(297,'RGIF 指定 PID 高位 RGID 的寬度，低位餘下部分是 PHNDL。','RGIF=2：RGID 在 bits 15:14，PHNDL 在 13:0；8001h 取出 RGID=2、PHNDL=1。NRG=1 而 RGIF>0 時，高位 RGID 由控制器忽略。','RGIF selects the width of the high RGID bits; the remaining low bits encode PHNDL.')
group('pid','從配置還原 16-bit PID','先查已啟用配置的 RGIF，才知道 bits 的意義；不要以數字看起來小就猜它是 RUHID。',[296,297],
 ('RGIF=0／NRG=1','PHNDL=PID；沒有 RGID 子欄位。','PID=3 指 namespace 的 PHNDL 3，不是 RUHID 3。'),
 ('RGIF=r>0','RGID=PID>>(16-r)；PHNDL=PID & ((1<<(16-r))-1)。','r=2，8001h>>14=2；8001h & 3FFFh=1。'),
 ('RGID 的合法性','一般要求 RGID<NRG；若 NRG=1，即使分配了 RGID bits 也忽略其值。','NRG=3、RGIF=2 可編碼 0～3，但 RGID=3 超出實際數量。'),
 ('PHNDL 的合法性','PHNDL 必須是指定 namespace 實際建立的 handle；欄位能編碼不代表已配置。','13:0 能放 16383，但清單 [1,3] 只有 PHNDL 0、1。'))

example(499,'FID 1Dh 的 CDW11 指定 ENDGID，不是 NSID 或配置索引。','CDW11=2 選群組 2；要選配置 2，應改 CDW12 的 FDPCIDX，不是把两者塞在同一欄。','FID 1Dh CDW11 selects ENDGID, not NSID or the configuration index.')
example(500,'FDPE 與 FDPCIDX 決定要保存的 FDP 狀態，Save 位元另在通用 CDW10。','CDW12=00000101h 選配置索引 1 且啟用；相同十六進位值在 Enable Directive 的 CDW12 有不同含義，因為外層命令與 FID 不同。','FDPE and FDPCIDX select FDP state; the Save bit is in common CDW10.')
group('feature','FDP 設定改變的前提與結果','FID 1Dh 的欄位值會保存；不是用 Delete／Create 資料結構直接開啟 FDP。',[499,500],
 ('CDW11[15:0] ENDGID','Endurance Groups 支援時選目標群組；高 16 bits 保留。','ENDGID=2 不代表 NSID=2 的 namespace。'),
 ('CDW12[15:8] FDPCIDX／[0] FDPE','索引選有效候選；FDPE=1 啟用，0 停用；[31:16]、[7:1] 保留。','索引 1 且啟用 → (1<<8)|1=00000101h。'),
 ('SV 與群組內 namespace','變更只允許 SV=1；群組已有 namespace 時要求不同值，回 Command Sequence Error。','預設值 0；改值前需該群組沒有 namespace。'),
 ('Get 的 SEL≠3／SEL=3','一般值查詢的 CQE DW0 採 Figure 500 格式；SEL=3 是通用支持能力格式。','不能把能力回覆 bit 0 的 saveable 當成 FDPE。'),
 ('成功改值的效果','清 FDP events 和 statistics；資料格式相關 Identify 欄位可能改變。','新配置的統計起點 0，不能沿用舊配置累計直接相減。'))

example(650,'Receive 的 DPTR 指向主機接收狀態的 buffer。','272-byte Status 結構會回到這個 buffer；PID 清單不是放在 DPTR 的數值本身。','Receive DPTR points to the host buffer that receives status.')
example(651,'Receive 的 MO=01h 要每個 PHNDL 在每個 RG 的狀態。','2 PHNDL×4 RG=8 筆；CDW10=00000001h。MO=0 是 No action，不能把 0 當成第一個 PHNDL。','Receive MO=01h requests each namespace PHNDL across all RGs.')
example(652,'Receive 的 NUMD 是 4-byte 傳輸單位數減 1。','272 bytes/4-1=67=43h，所以 CDW11=00000043h；NUMD 不是描述器數 8。','Receive NUMD encodes four-byte transfer units minus one.')
example(653,'RUH Status header 的 NRUHSD 計描述器，每筆內容由 NVM 規格定義。','NRUHSD=8 → 16-byte header 加 256 bytes 描述器。第 0 筆從 16 開始，第 7 筆從 240 開始，最後 byte 是 271。','RUH Status has a descriptor count and a sixteen-byte header; NVM defines each descriptor.')
group('receive','一筆查詢的命令、外框與截斷規則','Receive 用於讀取 namespace 可用 PID 的即時狀態；共用規則集中在此，NVM 描述器欄位另有詳細說明。',[650,651,652,653],
 ('DPTR 127:0／CDW10 MO[7:0]','DPTR 按 PRP 或 SGL 指接收記憶體；MO=1 選 Status，0 No action，FFh 廠商；其他保留。','本例固定 MO=1，其餘未定義的命令特定欄清 0。'),
 ('CDW10 MOS[31:16]／[15:8]','Status 沒有定義 MOS，故保留；[15:8] 也保留。','不能用 MOS=2 指定只讀 RG2。'),
 ('CDW11 NUMD[31:0]','傳輸 bytes=(NUMD+1)×4。短傳前段；Status 特別允許超出結構後以 0 補足。','要求 288 bytes 但結構 272 bytes，最後 16 bytes 填 0。'),
 ('Header bytes 15:14 NRUHSD／13:0 保留','NRUHSD 直接計數；第 i 筆起點 16+32×i。','NUMD=3 只讀 16-byte header；不能據此宣稱取得全部描述器。'),
 ('NSID／FDP 狀態／快照','NSID 0、FFFFFFFFh 拒絕；FDP 停用拒絕。每筆反映其處理時點，未必含 outstanding I/O。','先前查的 RUAMW 不會替下一筆 Write 預留容量。'))

example(21,'NVM Status 描述器把 PID 映射、剩餘秒數與可寫 blocks 放在各自欄位。','PID=8001h、RUHID=3、EARUTR=20、RUAMW=6：在本例是 RG2 的 PH1→RUH3，估計還有 20 秒、可寫 6 blocks。20 與 6 不能相加成容量。','NVM status separates PID mapping, remaining seconds, and writable logical blocks.',source='nvm')
group('status-fields','每筆 32-byte 狀態如何連到寫入決策','NVM 排序先 PHNDL 再 RGID；相同 PHNDL 的多筆狀態一起讀，才看得出各 RG 的差異。',[21],
 ('PID bytes 1:0／RUHID 3:2','PID 依目前 RGIF 分解；RUHID 是 PHNDL 的映射結果。','PID=8001h 可對 RUHID=3；兩欄不需要數值相等。'),
 ('EARUTR 7:4','當時目前 RU 可維持參照的估計剩餘秒數；0 未回報。','ERUTL=60、EARUTR=20 是配置上限估計與剩餘估計。'),
 ('RUAMW 15:8','當時可寫入媒體的 logical blocks；換算 bytes 可比 RUNS 大或小。','6×4096=24576 bytes；不是 6×RUNS。'),
 ('保留 31:16／狀態變動','保留不作新欄位；RUAMW 可因 Reset／Flush 改變或不變。','不能把回覆中保留 0 bytes 當成額外 0-capacity 描述器。'),source='nvm')

example(654,'Send 的 DPTR 指向主機提供的 PID 清單，資料方向與 Receive 相反。','更新 2 個 PID 的來源 buffer 是 4 bytes；它不是接收 32-byte Status 描述器的空間。','Send DPTR points to the host-supplied PID list, reversing Receive’s direction.')
example(655,'Send 的 MO=01h 選 Update，與 Receive 的相同 MO 數值代表不同動作。','CDW10 低 byte=01h，在 Send 是換空 RU，在 Receive 是讀狀態。辨認命令入口後再讀 MO。','Send MO=01h means Update, whereas Receive MO=01h means Status.')
example(656,'Update 的 NPID 是 MOS 內的數量減 1，上限來自目前配置。','2 個 PID → NPID=1，再放入 CDW10 bits 31:16 得 00010000h，與 MO=1 合成 00010001h；MAXPIDS=7 表示最多 8 個。','Update NPID is the zero-based count inside MOS, bounded by the active configuration.')
example(657,'Update buffer 每 2 bytes 是一個 PID，清單內容不含 RUH Status 描述器。','8000h、8001h 用 little-endian 依序放成 00 80 01 80；最後一筆從 2×NPID 開始。不要把 NPID=1 誤讀為清單只有 1 筆。','Each two-byte Update entry is a PID; it is not a status descriptor.')
group('send','Update 的長度、有效性與部分更新','先由 NPID 得清單數量，逐個 PID 用 namespace 映射驗證；成功完成才代表此操作完成，但失敗不能保證完全沒有改動。',[654,655,656,657],
 ('CDW10 MO[7:0]／MOS[31:16]','MO=1 Update；MOS 全部 16 bits 是 NPID。MO=0 No action、FFh 廠商；[15:8] 保留。','CDW10=(NPID<<16)|1。'),
 ('NPID 與 MAXPIDS','NPID≤min(MAXPIDS,NRG×NRUH)；配置另要求 MAXPIDS<NRG×NRUH，因此它已是較小上限。','NRG=4、NRUH=4、MAXPIDS=7，NPID 最大 7，清單最多 8 筆。'),
 ('DPTR／清單位址','K=NPID+1；buffer 大小 2×K；第 i 項在 2×i。Send 沒有 NUMD。','K=2、NPID=1，讀 4 bytes，不是 (1+1)×4。'),
 ('原 RU 有資料／原 RU 為空','有資料必須換到另一空 RU；已空可換或保留。','Update 不是 Deallocate，也不保證舊資料被擦除。'),
 ('非法 PID／失敗／重疊 Write','非法或超上限回 Invalid Field；失敗可能部分更新。重疊 Write 可使用更新前或後的 RU。','要求批次邊界時，先協調相關 I/O 並等待完成，再更新及發下一批。'))

example(298,'Usage 的項目索引就是 RUHID，每筆 8 bytes。','NRUH=4 時，header 8 bytes 加 4×8=32 bytes，總共 40 bytes；RUHID 3 的描述器從 byte 32 開始。','Usage entries are indexed by RUHID and are eight bytes each.')
example(299,'RUHA 0／1／2 是配置來源分類，不是 namespace 個數。','RUHA=2 表示 controller-selected；即使 5 個 namespace 共用該 RUH，值仍是 2。整份清單最多 1 筆分類為 2。','RUHA values classify allocation origin rather than count namespaces.')
group('usage','用清單位置與分類判斷配置來源','這份 log 不細分每個 RG 的剩餘量，也不描述 RU 是否已擦除。',[298,299],
 ('Header NRUH 1:0／7:2 保留','NRUH=目前配置的 RUH 數，直接計數且非零。','4 表示 RUHID 0～3。'),
 ('第 i 筆位置 8+8×i','描述器 byte 0 是 RUHA，bytes 7:1 保留。','RUH2 起點 24；offset 24 不等於 RUHID 24。'),
 ('RUHA=0／1／2','未用／主機明確選用／控制器選用；其他值保留。','主機清單 [1,3] 可讓項目 1、3 分類為 1。'),
 ('LSI.ENDGID／NSID','選群組；FDP 啟用時 NSID 保留，停用時回 FDP Disabled。','不能用 NSID 篩到只有一個 namespace 的清單。'))

example(300,'FDP Statistics 的三個 128-bit 計數分別記主機寫入、全部媒體寫入與擦除。','ΔHBMW=100 GiB、ΔMBMW=150 GiB、ΔMBE=200 GiB；寫入比值是 1.5，不是 (150+200)/100=3.5。','Three 128-bit counters separately track host writes, all media writes, and erasures.')
group('statistics','先對齊計數範圍與期間再計算','單位是 bytes，包含規格所定義的 user data 與 metadata；不是 SMART 使用的其他量化單位。',[300],
 ('HBMW bytes 15:0','128-bit 主機寫入量，不含 controller internal writes。','Write Zeroes 沒有等量主機 payload 也不能從統計排除。'),
 ('MBMW 31:16／MBE 47:32','MBMW 含主機與控制器相關寫入；MBE 是擦除量。','內部搬移增加 MBMW，不是把 MBE 加回主機寫入。'),
 ('飽和／清零／保留 63:48','到 2^128-1 不回繞；改 FID 1Dh 值清 0；firmware update 不清零。','前後跨配置改值時，不作普通差分。'),
 ('NVM 計入的命令','User Data Out Commands，加 Write Zeroes、Write Uncorrectable。','它是規格定義的邏輯寫入計量，不是只量 PCIe DMA bytes。'),
 ('量測期間與比值','同一群組、同一配置期間，ΔHBMW>0 且未飽和時才算 ΔMBMW/ΔHBMW。','100→150 GiB 的增量是 50 GiB，不是取結束絕對值代替增量。'))

example(501,'Get FDP Events 的 CQE DW0.NOET 是 buffer 回傳項目數。','NOET=3 表示 3 個 2-byte supported descriptors，共 6 bytes；不是只讀 3 bytes，也不是已發生了 3 件事件。','Get FDP Events CQE NOET counts returned supported-type descriptors.')
example(502,'CDW11 用 PHNDL 選 RUH，Set 時 NOET 再告訴控制器有幾個事件類型。','PHNDL=1、NOET=3 → 00030001h；Get 忽略 NOET，不能靠把它填 1 只要求第一種事件。','CDW11 selects PHNDL and, on Set, the number of event types.')
example(503,'FDPEE 是此次 Set 清單的共同開關，不是啟用 FDP 的 FDPE。','CDW12=1 配清單 [00h,03h]，表示啟用這兩種事件；不會因此更換群組的 FDP 配置。','FDPEE controls the supplied event-type list, not FDP configuration enablement.')
example(504,'Set buffer 每個 byte 只列一個事件類型。','00 03 80 是 3 種事件；不要送成 00 01 03 01 80 01，後者是誤把 Get 描述器格式拿來當 Set 請求。','Set uses one byte per event type rather than Get’s two-byte descriptors.')
example(505,'Get buffer 每個支持項目有事件值與屬性，依事件值遞增。','00 01 03 00 80 01：00h 啟用、03h 停用、80h 啟用；此處 00h 出現兩種角色，要按每 2 bytes 分組讀。','Get returns sorted two-byte supported-type entries containing a type and attributes.')
example(506,'每個 supported descriptor 的 FDPEE 只回答該事件目前是否啟用。','事件 03h 的 descriptor=03 00，表示支持但停用；沒有出現在支持清單的事件，不能只用缺少開關推論成同一種停用狀態。','A supported descriptor’s FDPEE reports enablement of that specific event type.')
group('event-feature','把 Get 的查詢結果與 Set 的事件清單分開','FID 1Eh 以 NSID／PHNDL 間接選 RUH；共用 RUH 的 namespace 共用設定效果。',[501,502,503,504,505,506],
 ('CQE DW0.NOET[7:0]','一般 Get 回支持項目數，直接計數；[31:8] 保留。','3 項×2 bytes=6 bytes。'),
 ('CDW11[23:16] NOET／[15:0] PHNDL','NOET 對 Set 有效，Get 忽略；PHNDL 兩者均用。[31:24] 保留。','PHNDL 無效，Get 和 Set 都回 Invalid Field。'),
 ('CDW12[0] FDPEE','1 啟用所列類型，0 停用；Get 忽略；[31:1] 保留。','Set 停用一組類型不表示刪除整份歷史 log。'),
 ('Set 1 byte／Get 2 bytes','Set 只送 event type；Get byte 0 是 FDPET，byte 1 的 bit 0 是 FDPEE，其餘保留。','Get 的 03 00 是「03h 支持、停用」，不是 03h 和 00h 兩種請求。'),
 ('可保存／FDP Disabled／共享','可保存；FDP 停用時拒絕 Get／Set。共享 RUH 的事件設定會相互影響。','A/PH1 與 B/PH0 對 RUH3，透過任一映射設定都指同一 RUH。'))

example(301,'Log 請求的 FDPET bit 選 host 或 controller events，與事件記錄的 ETYP 不同。','CDW10 bit 8=1 看 host 類；bit 8=0 看 controller 類。不能把 ETYP=80h 填入這個 1-bit 選擇欄來篩單一事件。','The request FDPET bit selects host versus controller events, not a particular ETYP.')
example(302,'FDP Events 是 64-byte header 加 64-byte 記錄，依發生先後排列。','NUMFDPE=2 時讀 header 後第 1、2 筆：offset 64、128；兩筆 timestamp 數值逆序也不應交換，因為來源時鐘可能重設。','FDP Events has a sixty-four-byte header and records in occurrence order.')
example(303,'事件識別欄位只有在對應有效位成立時才有報告意義。','FDPEF=05h：PIV=1、LV=1、NSIDV=0。可以讀 PID 與 RGID/RUHID，NSID 必須忽略；不能因 NSID=0 就說事件發生在 namespace 0。','Event identifier fields are meaningful only under their associated validity flags.')
group('events','原因先讀 ETYP，位置再讀有效位','一次回覆不混 host／controller；每筆 64 bytes，事件類型決定 ETSP 是否有格式可解釋。',[301,302,303],
 ('CDW10[8] FDPET／[14:9] 保留','1 host，0 controller；LSI.ENDGID 指群組。','讀兩類需各一次 Get Log Page；不能把兩次當成同一個原子快照。'),
 ('Header NUMFDPE 3:0／63:4 保留','直接計數；第 i 筆起點 64+64×i；4096-byte log 物理上最多 63 筆。','2 筆從 64、128 開始，之後的 bytes 不作第三筆。'),
 ('ETYP byte 0','00h未寫滿就Update；01h超過時間；02h reset改RUH；03h非法PID；80h搬資料；81h隱式改參照。','70h～7Fh、F0h～FFh 為廠商事件；其他保留值不代入標準事件解法。'),
 ('FDPEF byte 1：PIV[0]／NSIDV[1]／LV[2]','依序控制 PID、NSID、RGID與RUHID；[7:3] 保留。','00h 表示這些位置資訊沒有有效報告，不是所有位置都真的為 0。'),
 ('PID 3:2／NSID 15:12','PID 在 PIV=0 時保留；NSIDV=0 時 NSID 清0並忽略。02h 事件這兩欄保留。','03h事件的 PID 是主機送出的原值；不是控制器另選的 PID。'),
 ('ETMSP 11:4／ETSP 31:16','ETMSP 依 Timestamp 格式；ETSP 只有事件指定使用時才解讀。','80h 的 ETSP 接 NVM 116，00h～03h、81h 不使用它。'),
 ('RGID 33:32／RUHID 35:34','LV=0 時清0並忽略；03h且有效時回控制器實際另選的位置。','主機錯的 PID 與回報的 RUHID 不相等可以是正常結果。'),
 ('Reserved 39:36／VS 63:40','VS 可用於任何事件，不限廠商事件；無廠商定義時不能編造欄位含義。','標準 80h 仍可能帶 VS；它不是 NVM ETSP 的延伸欄位。'),
 ('容量上限／先後順序','滿了丟最舊；按發生先後回報，timestamp 可因初始化不同而逆序。','看不到事件可能因未啟用、被覆蓋或改配置後清空。'))

example(116,'Media Reallocated 的 NLBAM 是搬移量，LBA 是其中一個位置而不是範圍起點。','LBAV=1、NLBAM=8、LBA=100 只表示 100 是其中一個被搬的 LBA，不能畫成連續 100～107。NLBAM=FFFFh 表示至少 65535 個。','Media Reallocated reports a moved count and one example LBA, not a contiguous range.',source='nvm')
group('media-event','把 16-byte NVM 擴充放回 Base 事件的 ETSP','以下相對位置從 ETSP 起點算；Base 事件中的 ETSP 起於 byte 16。Media Reallocated 的外層事件值按 Base 303 為 80h。',[116],
 ('SEF byte 0，LBAV bit 0','LBAV=1 才可讀 LBA；[7:1] 保留；byte 1 保留。','在整筆事件中，LBAV 位於 byte16 bit0。'),
 ('NLBAM bytes 3:2','直接計數；0未回報數量，FFFFh代表65535或更多。','整筆事件中的 bytes19:18，不是NUMFDPE。'),
 ('LBA 11:4','其中一個被搬移的LBA；LBAV=0時清0並忽略。PIV=1時外層PID指原始寫入所用handle。','整筆事件 bytes27:20；不能從這一個值還原整批不連續範圍。'),
 ('Reserved 15:12／外層有效位','最後4 bytes保留；NSID、PID有效性仍由Base FDPEF判斷。','LBAV=1也不能讓外層NSIDV=0的NSID突然有效。'),source='nvm')

# Necessary references are scoped field slices, not additional full chapters.
example(93,'命令欄位與主機 buffer 是兩個位置，DPTR 只是把它們連起來。','NSID 位於命令 bytes7:4；DPTR 位於 bytes39:24；CDW10 從 byte40 開始。把 buffer 的第一個 PID 填在 CDW10，會變成錯誤的 MO／MOS。','Command fields and the host buffer are separate; DPTR connects them.')
group('command-envelope','讀位置前先確定是命令內還是 buffer 內','只取本篇所需的 NSID、DPTR、CDW 位置與 PRP／SGL 選擇；不展開完整 SQE 結構。',[93],
 ('NSID bytes7:4／DPTR bytes39:24','NSID 選 namespace；DPTR 根據 CDW0.PSDT 解讀為 PRP1/2 或 SGL descriptor。','Receive 的 DPTR 指目的記憶體，Send 指來源記憶體。'),
 ('CDW k 的 byte offset=4×k','CDW10在40、CDW11在44、CDW12在48、CDW13在52。','CDW10 bit8是命令 byte41 bit0，不是 buffer byte8。'),
 ('little-endian 與 bit 範圍','多 byte 整數低有效 byte 在前；bit欄仍按規格高低位標示。','PID=8001h 存成 01 80；不要把位元圖的左右順序當成記憶體 byte 順序。'))

example(186,'Directive Send 外層由 DTYPE／DOPER 選管理操作，目標類型另在 CDW12。','CDW11=00000001h 選 Identify/Enable；CDW12=00000201h 才選 Data Placement。外層 DTYPE=02h 沒有已定義的操作。','Directive Send CDW11 selects the outer operation; CDW12 separately selects the enable target.')
example(705,'Data Placement 的支援、啟用、跨 reset 保留分屬三份位元向量。','DPDIRS=1、DPDIRE=0 代表支持但尚未啟用；DPDIRCLR=1 表示該啟用狀態跨 Controller Level Reset 保留。這不保證 RUH 參照沒有變化。','Data Placement support, enablement and reset persistence occupy separate vectors.')
example(706,'Enable 的 target DTYPE=02h 配 ENDIR=1，得到 CDW12=00000201h。','00000200h 是停用 Data Placement；00000001h 是企圖改變 Identify 的狀態，不能把它當作通用啟用任何類型。','Enable target DTYPE=02h and ENDIR=1 encode CDW12=00000201h.')
group('directive-fields','兩個 DTYPE 與 3 個狀態位元','必要背景取 Identify Directive 的通用 Enable 與 Data Placement 位元；不展開 Streams 資源操作。',[186,705,706],
 ('CDW11 DSPEC[31:16]／DTYPE[15:8]／DOPER[7:0]','Enable 的 DSPEC 不使用；DTYPE=0選Identify，DOPER=1選Enable。','示例CDW11=1；不能直接對Data Placement發Send/Receive。'),
 ('CDW12 DTYPE[15:8]／ENDIR[0]','目標DTYPE=2；ENDIR=1啟用、0停用；其他bits保留。','啟用值=(2<<8)|1=201h。'),
 ('回覆 bytes31:0／63:32／95:64','分別支持、啟用、跨Controller Level Reset保留；Data Placement在每個向量bit2。','byte0 bit2為DPDIRS；byte32 bit2為DPDIRE；byte64 bit2為DPDIRCLR。'),
 ('NSID／主機關聯','Data Placement Enable不接受FFFFFFFFh；共享namespace在相同非零Host Identifier的控制器之間共享啟用狀態。','選具體namespace，不能從FID1Dh的群組範圍推論Enable也能群組廣播。'),
 ('4096-byte回覆的其餘欄','本篇只用Data Placement的bit2；其他類型不展開，bytes4095:96保留。','讀96 bytes才涵蓋三個向量，不要只讀32就宣稱取得啟用狀態。'))

example(198,'Get Features 的 SEL 選目前值、預設值、保存值或支援能力。','查FID1Dh目前配置用SEL=0；SEL=3的CQE是能力位，不是FDPE／FDPCIDX。','Get Features SEL distinguishes current, default, saved values and supported capabilities.')
example(201,'SEL=3 的 CQE 描述 saveable 等能力，不是某個 Feature 的實際設定值。','DW0 bit0=1表示可保存；不能由這個bit說FDP已啟用，後者要用FID1Dh值查詢。','SEL=3 CQE reports capabilities such as saveability, not the feature’s active value.')
example(464,'Set Features 的 SV 在 CDW10 bit31，與 FID 的低8 bits 分開。','FID=1Dh且SV=1 → 8000001Dh；將SV錯放在CDW12會改到Feature屬性或保留位。','Set Features puts SV in CDW10 bit31, separate from the low-byte FID.')
group('feature-envelope','先由通用欄選 Feature 與查詢種類','僅解釋本篇FID1Dh、1Eh需要的選擇；UIDX未指定UUID時為0，不展開UUID機制。',[198,201,464],
 ('Get CDW10 FID[7:0]／SEL[10:8]','SEL=0目前、1預設、2保存、3支援能力；其他值保留。','FID1Dh/SEL0的DW0採Base500，FID1Eh/SEL0的資料在buffer。'),
 ('Set CDW10 FID[7:0]／SV[31]','SV=1要求保存；具體Feature可以增加保存要求，1Dh就要求改值時SV=1。','8000001Dh選FDP並保存；其餘命令屬性另讀CDW11/12。'),
 ('SEL3 CQE bits0／1／2','分別saveable、namespace-specific、changeable能力；其他bits保留。','能力與範圍仍要結合Feature定義，不能把bit1當成NSID數值。'))

example(204,'Get Log Page CDW10 同時選 LID、特定選項與傳輸長度低位。','完整讀4096-byte FDP host events：NUMDL=1023、FDPET=1、LID=23h，其他選項0，CDW10=03FF0123h。','Get Log Page CDW10 selects LID, log-specific options, and the low transfer count.')
example(205,'Get Log Page CDW11 的高16 bits 是 LSI，低16 bits 是 NUMDU。','ENDGID=2、NUMDU=0 → CDW11=00020000h；不是00000002h，後者改的是傳輸長度高位。','Get Log Page CDW11 places LSI above NUMDU.')
example(206,'LPOL 提供 log 起讀 offset 的低32 bits，與配置清單索引不同。','要從byte96續讀配置資料，在OT=0時LPOL=96；要啟用配置索引1仍填FDPCIDX=1。','LPOL is the low offset word, distinct from a configuration-list index.')
example(207,'LPOU 是同一個64-bit offset 的高32 bits，不是另一段長度。','小型FDP logs從起點或byte96讀取，LPOU=0；不要把NUMD放進這裡。','LPOU is the high word of the same offset, not another length.')
example(208,'OT 決定 offset 類型；本篇 byte offset 範例固定 OT=0。','OT=0、LPOL=96表示第96 byte；不是第96個FDP descriptor。CSI／UIDX仍按所選命令集與識別使用。','OT selects the offset type; this report’s byte-offset examples use OT=0.')
example(224,'FDP 四份 log 以 LSI 的 ENDGID 選群組。','讀群組2的LID21h，ENDGID=2在LSI低16bits，也就是整個CDW11高16bits。表內bit15:0是相對LSI的位置。','The four FDP logs use LSI.ENDGID to select their Endurance Group.')
group('log-envelope','把局部欄位放回整個 Get Log Page 命令','同樣寫bits15:0，可能是在LSI子欄位內，也可能在整個CDW；必須先看表題。',[204,205,206,207,208,224],
 ('CDW10 LID[7:0]／LSP[14:8]／RAE[15]／NUMDL[31:16]','LID選20h～23h；LID23h的LSP最低bit是FDPET；NUMDL是NUMD低16bits。','4KiB=1024 Dwords → NUMD=1023，不是4096。'),
 ('CDW11 LSI[31:16]／NUMDU[15:0]','LSI對FDP logs解讀為ENDGID；NUMDU是傳輸Dword數減1的高16bits。','NUMD=(NUMDU<<16)|NUMDL。ENDGID=2只影響高16bits的LSI。'),
 ('CDW12 LPOL／CDW13 LPOU','合成offset=(LPOU<<32)|LPOL；本篇OT=0以bytes計，須按Dword對齊。','offset96可用；不是從第96筆開始。'),
 ('CDW14 OT[23]／CSI[31:24]／UIDX[6:0]','本篇採OT=0、NVM CSI=0、UIDX=0，其他保留；不在本篇使用index offset。','將欄位固定才可直接對照本文完整命令算例。'),
 ('DPTR／NSID／群組','DPTR指接收buffer；LID21h～23h在FDP啟用群組中NSID保留。','查群組狀態不等於選了某個namespace；Status命令的NSID規則另外看。'))

example(270,'FID Effects log 用 FID×4 找對應項目，支援能力與作用範圍各自回報。','FID1Dh項目在byte116，1Eh在byte120；不是把這兩個byte offset當成Feature Identifier。','FID Effects entries sit at FID×4 and separately report support and effects.')
example(271,'Feature 的作用範圍能指向 Endurance Group 或 RUH，而非一律是 namespace。','FDP1Dh對Endurance Group；Events1Eh透過namespace的PHNDL改RUH。FSP=0表示沒回報範圍，不表示所有範圍皆適用。','Feature scope can identify an Endurance Group or RUH instead of a namespace.')
group('effects','用最小欄位確認支援與共享範圍','FDP支援時也必須支援這份log。本篇只取1Dh／1Eh兩項的支持位與範圍；其餘effects不展開。',[270,271],
 ('項目位置=4×FID','每FID固定4bytes；1Dh=29，1Eh=30。','29×4=116；30×4=120。'),
 ('FSUPP bit0／FSP[31:20]','FSUPP回支援；FSP非零時僅1bit為1，0代表未回報。','支持不表示當前FDPE或FDPEE=1。'),
 ('FSP內EGSCPE bit3／RUHS bit7','對應整個Dword bits23／27；分別為Endurance Group與RUH範圍。','別把局部bit7當成整個Dword bit7。'))

example(338,'FDPS、SSFS、VWCP 與 namespace 上限各回答不同能力問題。','FDPS=1表示支持FDP；VWCP=1卻可能有VWCNP=1的namespace；MNAN=8則是namespace數量上限，不是8個RUH。','FDPS, SSFS, VWCP and namespace limits answer different capability questions.')
group('controller','長 Identify 表只取 FDP 使用的欄位','對照位置分散在指定PDF頁；這里逐項說明讀法，不要求從數十頁的大表自行找結論。',[338],
 ('CTRATT bytes99:96，FDPS bit19','1支持FDP；Fixed Capacity Management支援時FDPS必須0。','FDPS不是FID1Dh的FDPE。'),
 ('ONCS bytes521:520，NVMDSMSV bit2','1表示支持DSM並以限制欄位回報可選限制；0時支持與否由非零DMRL／DMRSL／DMSL判斷。','先看支持，再看範圍限制，不能由某欄0直接推論無上限。'),
 ('ONCS bytes521:520，SSFS bit4','支持Set的Save與Get的非零Select；FDP1Dh的改值要求仍是SV=1。','不要用支持能力取代目前設定查詢。'),
 ('VWC byte525，VWCP bit0','有配置報FDPVWC=1時，controller的VWCP也為1；某namespace仍可另報沒cache。','搭配Base346.NSFEAT.VWCNP判斷特定namespace。'),
 ('MNAN bytes543:540／NN519:516','MNAN非零給支持namespace數上限；為0時上限≤NN。NN本身是有效NSID最大值。','NRUH=4不能推論最多4個namespace。'))
example(346,'VWCNP 讓主機知道特定 namespace 沒有 volatile write cache。','VWCNP=1時忽略controller的VWCP；VWCNP=0時才依VWCP判斷。不是VWCNP=0就必定有cache。','VWCNP identifies a namespace without a volatile write cache despite controller-level advertising.')
group('cache','把群組配置、控制器與 namespace 的 cache 資訊對上','只取CNS08h中NSFEAT.VWCNP及其與Flush的必要關係；不展開整份Identify Namespace。',[346],
 ('NSFEAT byte0，VWCNP bit5','1=此namespace沒有volatile cache，忽略VWCP；0=依controller VWCP。','VWCP=1、VWCNP=1：此namespace仍沒有cache。'),
 ('FDPVWC／VWCNP／Flush','配置是否帶cache、namespace是否不帶cache分層判斷；無cache或未啟用cache時Flush不產生資料提交效果。','Update成功不是Flush成功，也不是媒體已擦除。'))

example(480,'事件的8-byte時間包含時間值和時鐘來源，不能只拿整個值排序。','TSTMPO=0、TSTMP=500是reset後約500ms；TSTMPO=1則由主機設定值加計時而來。兩筆數字大小不直接代表跨reset先後。','The eight-byte event timestamp includes a value and origin attributes, not one sortable integer.')
group('timestamp','事件時間的相對位置與意義','ETMSP在事件bytes11:4，以下位置先以8-byte Timestamp結構起點計算。',[480],
 ('TSTMP bytes5:0','48-bit毫秒值；來源0按最近reset，來源1按主機設定值再累加。','事件中的TSTMP實際位於bytes9:4。'),
 ('TSTMPS byte6：TSTMPO[3:1]／SYNC[0]','來源0=reset初始化，1=主機設定；SYNC=1表示可能停止計時過；[7:4]保留。','事件byte10=02h表示origin1且連續計時，不能把02h當事件類型。'),
 ('byte7保留／清單順序','保留byte不作時間高位；事件仍按發生先後列出。','保留原始列表次序，可避免跨reset按數字排序顛倒因果。'))

example(134,'Namespace 的 PHNDL 是清單索引，該位置的2-byte值才是RUHID。','NPHNDLS=2且清單bytes512～515=01 00 03 00，得到PH0→RUH1、PH1→RUH3；不會建立PH3。','Namespace PHNDLs are list indices whose two-byte values are RUHIDs.',source='nvm')
group('namespace-fields','只讀FDP建立映射需要的欄位','必要引用包含NVM§4.1.6.3的完整映射限制；其他建立namespace能力不在此複製成另一篇。',[134],
 ('ENDGID bytes103:102','選FDP所屬群組；CSI需NVM00h。','群組設定與namespace的Placement Handle List必須匹配。'),
 ('NPHNDLS bytes393:392','直接計數，非零時≤min(NRUH,128)；0請controller選唯一PH0。','值2是2個，不是3個；與NUMFDPC的編碼不同。'),
 ('List bytes512起，每項2bytes','第i項起點512+2×i，內容RUHID<NRUH，不許同一list重複。','[1,3]合法候選；[1,1]回Invalid Placement Handle List。'),
 ('controller-selected與host-selected','NPHNDLS=0的namespace共用一個controller選的RUH，該RUH不能再被host明確列入。','無可供controller選用的RUH時，不會偷偷共用host選定的RUH。'),
 ('共享格式／NVM Set','共享RUH需相同Format Index，否則Invalid Format；FDP群組不支持NVM Sets。','只看每block的4096 data bytes相同，不足以證明全部格式相同。'),source='nvm')

example(70,'Write 的 SLBA 是64-bit邏輯起點，跟PID的RGID無關。','LBA128 → CDW10=80h、CDW11=0；即使PID=8001h，不能把CDW11改成2來代表RG2。','Write SLBA is the logical starting address, independent of PID RGID.',source='nvm')
example(71,'Write CDW12分別承載NLB、CETYPE與DTYPE，各有自己的bits。','8blocks、CETYPE0、DTYPE2，其他選項0 → 00200007h；NLB是7，不是8。','Write CDW12 separately encodes NLB, CETYPE and DTYPE.',source='nvm')
example(72,'CETYPE=0時，Write CDW13的高16bits才是DSPEC。','PID8001h → CDW13=80010000h，低位DSM提示本例0。不要把8001h放低16bits，那不是DSPEC。','For CETYPE=0, Write CDW13 carries DSPEC in its high sixteen bits.',source='nvm')
group('write-fields','把邏輯地址、長度、放置與持久化分開','只用CETYPE=0的普通Write帶PID範例；沒有替非零CETYPE推導欄位。',[70,71,72],
 ('SLBA：CDW10低32／CDW11高32','64-bit namespace邏輯起點；不參與PHNDL→RUH映射。','128=00000000_00000080h。'),
 ('CDW12 NLB[15:0]／CETYPE[19:16]／DTYPE[23:20]','NLB=blocks-1；本例CETYPE0、DTYPE2。','(2<<20)|7=00200007h。'),
 ('CDW13 DSPEC[31:16]／DSM[7:0]','CETYPE0時DSPEC放16-bitPID；DSM是另外的資料集提示，[15:8]保留。','8001h<<16=80010000h；沒有暗示DSM的值也應8001h。'),
 ('CDW12 FUA bit30','FUA控制該Write的非揮發提交要求；FDP沒有改掉這層語意。','本篇0值範例沒要求FUA，不能據成功完成就忽略cache狀態。'),source='nvm')

example(45,'DSM 的 NR 計16-byte範圍項目數減1。','2個不連續範圍 → NR=1，buffer=32bytes；不是2個PID，也不是2blocks。','DSM NR encodes the number of sixteen-byte ranges minus one.',source='nvm')
example(46,'DSM 的 AD 位表示可解除配置的資料範圍，不是切換RUH。','CDW11=4只設AD，讓controller可解除提供的LBA ranges；它不包含PID，也不保證立即擦除媒體。','DSM AD marks deallocation ranges rather than switching an RUH.',source='nvm')
example(47,'DSM 的每個範圍需要自己的SLBA與直接計數長度。','(SLBA100,LLB8)和(SLBA1000,LLB4)是兩筆；Write NLB減1的習慣不能套成LLB7、3。','Each DSM range has its own SLBA and directly encoded block length.',source='nvm')
example(129,'DSM 三個限制分別管範圍數、單一範圍長度與整個命令長度。','DMRL=2、DMRSL=8、DMSL=10：兩筆8與4blocks雖各自不超8，但總共12超過10，需要分批安排。','DSM limits independently bound range count, per-range size and total command size.',source='nvm')
group('deallocation','按原來的邏輯範圍交代資料不再需要','這些是FDP資料生命週期的必要背景；DSM屬advisory，不能把它畫成收到就必定擦除。',[45,46,47,129],
 ('NR CDW10[7:0]／AD CDW11[2]','NR=range數-1，最多256項；AD=1提供解除配置資訊。','2ranges→NR1、AD命令值4。'),
 ('Range CATTR bytes3:0／LLB7:4／SLBA15:8','每筆16bytes；LLB直接計數；CATTR為附加提示，本例0。','第一筆SLBA100、LLB8；下一筆獨立從offset16開始。'),
 ('NVM Identify Controller：DMRL byte3／DMRSL bytes7:4／DMSL bytes15:8','非零時分別限制range數、單range blocks、總blocks；超出部分可能不處理。NVMDSMSV=1時0表示未回報該限制；NVMDSMSV=0時0表示不支持命令，不能一律當作無上限。','2個ranges共12blocks，DMSL10時不能以「只有2項」推論完整處理。'),
 ('解除配置與隔離／擦除','提供失效LBA範圍可協助回收；不保證立即回收、不等同Sanitize、也不改PHNDL映射。','同一PID已指到新RU時，仍需知道舊批次的LBA範圍。'),source='nvm')
