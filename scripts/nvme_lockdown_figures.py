"""Distinct Lockdown figure lessons with shared, nonduplicated field explanations."""
EXAMPLES = {}
GUIDES = {}
MEMBERS = {}


def example(n, takeaway, worked, en):
    EXAMPLES[n] = dict(takeaway=takeaway, example=worked, en=en)


def group(key, title, relation, numbers, *rows):
    ident = 'lockdown-'+key
    GUIDES[ident] = dict(id=ident,title=title,relation=relation,rows=list(rows))
    for n in numbers:
        MEMBERS[n] = ident


def lesson(f):
    return EXAMPLES[int(f['number'])]


def guide(f):
    return GUIDES[MEMBERS[int(f['number'])]]


example(274,'LSP 同時選查詢種類與格式，不是只有一個「查 Lockdown」的開關。','ELPF=0、CNTTS=1、SCP=2：CDW10 bits 14:8 對應 12h，所以放入命令的部分值是 00001200h。加 LID14h 得 00001214h，還未加 NUMDL。','LSP selects both the list meaning and its format.')
example(275,'只有 ELPF=1 時，LSI 才被本 Log 解讀為 CNTLID。','查控制器 7：LSI=0007h，實際放進 CDW11 高 16 bits 成為 00070000h；FFFFh 才是全體查詢，不是 0。','The log interprets LSI as CNTLID only in enhanced format.')
group('query-fields','先組成問題，再指定要查的控制器','Figure 274 的 bits 位置已經是 CDW10 的位置；Figure 275 則以 16-bit LSI 自身為起點，必須再放到 CDW11 高位。',[274,275],
 ('ELPF：CDW10 bit14','0=Figure276；1=Figure277，後者需 CCFLS 支援。','ELPF=1 不能只更換解析器，也要讓命令確實請求增強格式。'),
 ('CNTTS：CDW10 bits13:12','0=可禁止；1=Admin Queue 已禁止；2=Management Endpoint 已禁止；3 保留。','沒有 Management Endpoint 卻查 2，回 Invalid Field in Command。'),
 ('SCP：CDW10 bits11:8','0=Admin opcode；2=Set Features FID；3=Management Interface opcode；4=其 PCIe opcode；1、5～F 保留。','SCP2 的 06h 是 FID，不是 Admin opcode06h。'),
 ('CNTLID：LSI bits15:0 → CDW11 bits31:16','ELPF1 時指定控制器，FFFFh 查全部；ELPF0 時保留。','CMD11=00070000h 中 0007 是控制器，不是 NUMDU。'))

example(276,'一般 Log 以 byte 長度限制代碼清單，不能掃到保留區。','12 00 00 02 06 07 的 LNGTH=2，只讀 byte4、5 的 06h、07h。若 LNGTH=0，沒有任何有效項目，不把 byte4 的 0 當命令。','The basic log uses a byte count to delimit its code list.')
group('basic-fields','每個代碼的意義來自 header，不來自清單位置','一般格式固定 512bytes；先核對 CS／SS，再讀 LNGTH 個單 byte 代碼。',[276],
 ('CFILA byte0：CS[5:4]、SS[3:0]','回映 CNTTS／SCP；[7:6]保留。CS0 的可禁止清單、CS1 的 Admin 已禁止清單描述全體控制器共同項目。','CFILA12h→CS1、SS2。'),
 ('bytes2:1 保留；LNGTH byte3','LNGTH=n，直接表示清單 byte 數；0=空清單。','n2 不是數量減 1，不可讀 3 筆。'),
 ('CFIL bytes n+3:4','每個值 1byte，由小到大排序；其餘 bytes511:n+4 保留。','索引 0 在 offset4，內容 06h 才是 FID。'))

example(277,'增強 header 分開提供總長度、項目數與每筆步距。','NCFID=2、CFIDS=2、SZE=20：16-byte header 後兩筆分別從 16、18 開始。若把 NCFID 當 byte 數，就只會讀到第一筆。','The enhanced header separates total size, item count and descriptor stride.')
example(278,'ACNTL=0 仍是一筆有控制器回報的項目，只是不是全部都有。','全體查詢回 06 00、07 01：06h 只在部分控制器符合，07h 全部符合；還不能由 06 00 知道具體是哪一台。','ACNTL=0 means at least one but not all controllers report the entry.')
group('enhanced-fields','外層 CFIA 說明清單種類，內層 CFIA 說明一筆項目的全體屬性','同名 CFIA 所在結構不同；先確認是 header byte1 還是描述器 byte1。',[277,278],
 ('Header VER byte0／CFIA byte1','VER0；CFIA 的 CS[5:4]與 SS[3:0]回映查詢，[7:6]保留。','Header12h 是 Admin Queue 已禁止 FID，不是 ACNTL 值。'),
 ('Header CNTLID bytes3:2','回映請求；FFFFh 時收錄至少一台控制器回報的項目，其他值選指定控制器。','同樣查 Admin 禁止 FID，FFFFh 與 0007h 是不同範圍。'),
 ('SZE bytes7:4／NCFID9:8／CFIDS11:10','總 byte 數／直接項目數／每筆 byte 數；header15:12 保留。','16+2×2=20bytes，NCFID0 才是空清單。'),
 ('第 i 筆從 16+i×CFIDS 開始','按 CFI 值遞增排列，不能按 ACNTL 或 Controller Identifier 排序。','i1、CFIDS2→offset18。'),
 ('Descriptor CFI byte0／CFIA byte1','CFI 是 SCP 選定種類的代碼；CFIA bit0 為 ACNTL，bits7:1 保留。','06 00 中的 00 不表示 06h 目前全部允許。'),
 ('ACNTL[0]','1=全部控制器回報；0=至少一台但非全部。清單不含每項的控制器名單。','需要找出哪台時，保留同一 CNTTS／SCP，改 CNTLID 逐一查。'))

example(365,'CDW10 的五個選擇共同決定限制，PRHBT 自己不能表達完整意圖。','(1<<16)|(6<<8)|(1<<4)|2=00010612h，代表控制器選擇 1、FID06h、Admin Queue、禁止；這裡的 1 還不是 Controller ID。','Five CDW10 selectors jointly define the restriction; PRHBT alone is insufficient.')
example(366,'CSS 的意義由 CSEL 決定，UIDX 則是另一層廠商定義選擇。','CSEL1、CSS7、UIDX0→CDW14=00070000h。CSEL2 且同樣 CSS7，會改成選 primary7 所屬的 secondary 集合，不是單一 controller7。','CSEL determines the meaning of CSS; UIDX separately selects a vendor definition.')
group('command-fields','把操作、入口、控制器與禁止方向放回各自的位置','Lockdown 使用 opcode24h，沒有資料清單 payload；其他命令專用 Dword 保留。',[365,366],
 ('CDW10 CSEL[19:16]／CDW14 CSS[31:16]','CSEL0 全體且 CSS 保留；1 指定 CSS 控制器；2 指定 CSS primary 的全部 secondaries；Fh 廠商定義；3～E 保留。','CSEL2 不包含 primary 本身；CSS 不是 primary 則回 Invalid Controller Identifier。'),
 ('CDW10 OFI[15:8]／SCP[3:0]','SCP0 解 OFI 為 Admin opcode；2 為 Set Features FID；3、4 為管理介面的兩種命令集；其餘保留。','SCP2、OFI06h 只選 FID06h 的設定操作。'),
 ('CDW10 IFC[6:5]','0=Admin Queue；1=Queue 加 Management Endpoint；2=Management Endpoint；3 保留。','沒有 Endpoint 時 1、2 皆非法；SCP4 搭 IFC0 或 1 也非法。'),
 ('CDW10 PRHBT[4]','1 禁止，0 允許；不改變 OFI、IFC、CSEL 各自選出的範圍。','00010612h 清 bit4→00010602h。'),
 ('CDW14 UIDX[6:0]','SCP2 及相關 UUID 能力成立才選廠商定義；0 不指定；非 SCP2 忽略。','CSS7 與 UIDX2 可共存為 00070002h，不是二選一。'),
 ('命令保留位','CDW10[31:20]、[7]；CDW14[15:7]保留。','例子先將保留位清 0，再加入需要的欄位。'))

example(367,'Lockdown 的 1Fh／28h 描述設定命令失敗，不是後續操作受限制的 23h。','CSEL2 配非 primary 的 CSS→1Fh；目標 OFI 不可禁止→28h。兩者都先辨認 SCT=1，再讀 SC。','Lockdown-specific 1Fh/28h describe failed configuration, not the later prohibited-command status.')
example(103,'通用 SC=23h 指出命令因現有 Lockdown 限制而中止。','設定成功後送被限制的 Set Features，讀到 SCT0、SC23h；不是在說 LID23h，也不是 Lockdown opcode23h。','Generic SC=23h reports a command rejected by an existing Lockdown prohibition.')
example(99,'CQE DW3 先將命令身分與狀態分開，避免把兩次操作的完成結果配錯。','CID10 是 Lockdown、CID11 是後續 Set Features；CID10 成功而 CID11 回限制錯誤，符合先設定再攔截的流程。','CQE DW3 separates command identity from status so completions can be matched correctly.')
example(101,'SC 要搭 SCT 判斷，不能只看一個十六進位錯誤碼。','DW3 中 SCT bits27:25=0、SC bits24:17=23h 時，才是通用 Lockdown 禁止狀態；Phase Tag 不屬於 SC。','Interpret SC together with SCT; the phase tag is not part of the status code.')
group('status-fields','先辨認完成的命令，再辨認錯誤種類與原因','以下 bits 以 CQE DW3 為起點；只有本篇需要的通用與命令特定代碼列入教學。',[367,103,99,101],
 ('DW3 CID[15:0]／P[16]／STATUS[31:17]','CID 配合 SQ Identifier 對回命令；P 辨認新完成項，STATUS 才是處理結果。','同一輪有查詢與 Lockdown 時，不把查詢成功當設定成功。'),
 ('SC[24:17]／SCT[27:25]','SCT0 為 Generic，SCT1 為 Command Specific；SC 提供該類別的代碼。','SCT0/23h=現有限制；SCT1/28h=不能建立要求的限制。'),
 ('DNR[31]／M[30]／CRD[29:28]','DNR1 表示原命令重送預期仍失敗；M1 表示另有錯誤資訊；CRD 只有 DNR0 且主機 ACRE1 時依 0 或 CRDT1～3 選重試延遲，其餘情況保留。它們不是 SC 高位。','不能因為延遲一段時間就假設禁止狀態自動解除。'),
 ('SC1Fh、28h：SCT1','無效 Controller Identifier／Prohibition of Command Execution Not Supported。','OFI 不可禁止必須 28h；某個所選介面不支援該 OFI 時應回 28h，也可回 Invalid Field。'),
 ('SC23h、02h：SCT0','Command Prohibited by Command and Feature Lockdown／Invalid Field in Command。','後者檢查欄位或組合，不代表成功套用禁止。'))

example(338,'OACS 的兩個能力位元分別保證基本範圍與控制器擴充範圍。','bytes256、257 讀到 00 24，合成 2400h；bits13、10 均 1，因此可用基本功能、CSEL1/2 及 ELPF1。其他 OACS 位元本例不作推論。','OACS distinguishes basic Lockdown from controller-scoped support.')
example(28,'Lockdown 是獨立的 Admin 命令，OFI 是它要管理的目標。','送 Lockdown 時外層 OPC=24h；如果要禁止 Set Features 的 FID06h，06h 放 OFI 且 SCP2，不能把外層 OPC 改 06h。','Lockdown has its own Admin opcode; OFI identifies its target.')
example(93,'命令外框、目標操作與回傳 buffer 屬於不同層次。','Get Log 用 OPC02h 及 DPTR 收資料；Lockdown 用 OPC24h 及 CDW10/14 改狀態。CID 用於辨識各筆完成，並非控制器編號。','The command envelope, target operation and returned data buffer are separate layers.')
group('capability-fields','只讀建立本篇操作入口所需的共同欄位','Identify Controller 不整份複製；本篇 OACS 與必要的 UUID 能力依各欄位局部閱讀。',[338,28,93],
 ('OACS bytes257:256：CFLS[10]／CCFLS[13]','基本能力／控制器範圍能力；CCFLS1 要求 CFLS1。','2400h=(1<<13)|(1<<10)，不代表所有 OFI 都可禁止。'),
 ('OPC：SQE CDW0[7:0]','Lockdown24h；Get Log Page02h；Set Features09h；Get Features0Ah。','整個 Set Features opcode09h 與單一 FID06h 是不同目標。'),
 ('CID：SQE CDW0[31:16]','主機指派命令編號，用於完成配對。','CID7 與 CSS7 即使數字相同，也分別代表命令和控制器。'),
 ('DPTR／命令專用 CDW','需要收 Log 時 DPTR 提供資料 buffer；Lockdown 本身只使用 CDW10、14 的專用參數。','LNGTH 或 NCFID 在回傳 buffer 內，不在 Lockdown 的 CQE 內。'))

example(203,'Log 資料經 DPTR 回主機記憶體，CQE 回的是完成結果。','主機配置 512-byte buffer 並送 Get Log；完成成功後再讀 buffer 的 CFILA 與 LNGTH，不能把 CQE DW0 當這份清單。','DPTR identifies the host buffer receiving the log; the CQE reports completion.')
example(204,'NUMDL 計 Dword 數減 1，LSP 另決定 Log 的問題。','讀 512bytes→NUMDL127=007Fh；LSP12h 查目前禁止 FID，LID14h，合成 CDW10=007F1214h。','NUMDL encodes Dword count minus one while LSP selects the log query.')
example(205,'LSI 與 NUMDU 共用 CDW11，但不是同一個長度欄位。','增強查 controller7、傳輸不足 65537Dwords：CDW11=00070000h，高位 7 是 CNTLID，低位 0 是 NUMDU。','CDW11 combines a log-specific identifier with the high portion of the transfer count.')
example(206,'LPOL 選起讀位置，不能代替清單的項目數。','OT0、LPOL16 從 byte16 開始；一般清單索引 0 在 byte4，增強清單索引 0 在 byte16，不能共用同一個換算。','LPOL specifies where reading starts, independently of item counts.')
example(207,'LPOU 是同一個 64-bit 起點的高位，不是第二段 buffer 的起點。','起點 16bytes→LPOU0、LPOL16；不能把 NUMDU127 放 LPOU，否則會請求完全不同的 offset。','LPOU extends the same 64-bit starting offset rather than selecting another buffer.')
example(208,'OT 選 offset 單位，UIDX 選廠商定義，兩者不能混用。','OT0 且 UIDX2 時 CDW14 低位 2 代表 UUID List 第 2 項；LPOL 仍以 bytes 計，不會因 UIDX 非零變成 index-offset。','OT chooses offset units; UIDX independently selects a vendor definition.')
group('log-envelope','把 Log 的種類、長度、起點與接收 buffer 分開','範例採 OT0 且已知裝置支援所需長度與 offset；未定義的尾端資料不當作有效記錄。',[203,204,205,206,207,208],
 ('DPTR','主機提供可接收資料的 buffer；大小需容納要求的傳輸。','不是把 Log 放在 Lockdown 的資料指標。'),
 ('CDW10 NUMDL[31:16]／RAE[15]／LSP[14:8]／LID[7:0]','NUMDL 是計數低 16bits；RAE 控制相關非同步事件是否保留，本例 0；LSP 依 274；LID14h。','512/4-1=127，不能用 LNGTH2 代替 NUMDL。'),
 ('CDW11 LSI[31:16]／NUMDU[15:0]','LSI 依 275；合成 NUMD=(NUMDU<<16)|NUMDL，傳輸 bytes=(NUMD+1)×4。','LSIFFFFh 查全體控制器，不表示傳 65536Dwords。'),
 ('CDW12 LPOL／CDW13 LPOU','OT0 時合成 64-bit byte offset，需 4-byte 對齊；超出 Log 大小會拒絕。','要讀增強第二筆 offset18，不能直接作為未對齊的 Get Log 起點；可從 16 讀取包含它的 Dwords。'),
 ('CDW14 OT[23]／UIDX[6:0]／CSI[31:24]','OT0 為 bytes；OT1 是需支援的項目索引。UIDX 依 UUID 規則。CSI 有自己的 I/O 命令集選擇規則，不是 SCP。bits22:7 保留。','本篇以 NVM 情境 CSI0、OT0 作例，絕不以 CSI2 代替 SCP2。'),
 ('請求長度超過 Log 末端','回完整 Log 後，多出的 Dwords 結果未定義，除非該 Log 另有規定；不能假設填 0。','SZE18bytes 以 20-byte 傳輸容納時，只依 SZE 與 NCFID 讀有效內容。'))

example(518,'LDPE 是全體限制的跨 power-cycle 設定，不是立即禁止某個 OFI。','CDW11 bit0=1 要求啟用 Lockdown Persistence；仍需另外的 Lockdown 命令指定要禁止哪個 FID 或 opcode。','LDPE enables persistence for all-controller prohibitions; it does not select an OFI.')
example(519,'LDPS 回在 CQE DW1，顯示目前持續性狀態。','查 PERID02h，DW1=1 代表持續性啟用；這不是目前禁止 1 個 FID，也不是 ACNTL1。','LDPS in CQE DW1 reports current persistence state, not a prohibited-item count.')
example(512,'PERID02h 是 FID22h 裡的一種 personality，不是 FID02h。','先選 Configurable Device Personality Feature22h，再用 PERID02h 選 Lockdown Persistence；這種 personality 不使用資料 buffer。','PERID02h selects a personality within FID22h, not Feature02h.')
example(513,'改設定與凍結是獨立位元，PERID 選擇它們操作的對象。','CHPS1、PERFS0、PERID02h→CDW13=00000202h；只代表本例請求改設定且保持未凍結，不能用於直接解凍已凍結對象。','CHPS changes settings, PERFS requests freezing and PERID chooses the personality.')
example(514,'DW0 回待生效與凍結狀態，不能只讀 DW1 的 LDPS 就省略它。','DW0=00000302h 表示 PERID02h、PERFS1、PPSC1；可能仍有待生效變更，PERFS 也可表示待凍結，不可一律當成所有設定都已完成。','DW0 reports pending and freeze state separately from the persistence value in DW1.')
example(292,'Personality Properties 的 AUS 說明能否認證解凍，MRSTT 說明設定所需的 reset 條件。','PERID02h 的 AUS=02h 表示支援 Programmable Key Authentication；MRSTT4 表示需 main power cycle。AUS 的 2 不是 PERID2，也不是兩個方法都支援。','AUS describes authenticated unfreeze support and MRSTT describes the reset required for a change.')
group('persistence-fields','讀目前狀態、待生效狀態與支援能力，三者不能互相代替','只教 Lockdown 持續性必需的 Personality02h；不展開其他 personality 設定或認證封包。',[518,519,512,513,514,292],
 ('FID22h／PERID02h','前者選 Configurable Device Personality；後者選 Lockdown Persistence，這個 personality 無額外 data buffer。','FID 與 PERID 各占自己的欄位，不能互換。'),
 ('Set CDW11 LDPE[0]／Get CQE DW1 LDPS[0]','設定跨 power-cycle 持續性／回報目前狀態；各自 bits31:1 保留。','只把 LDPE1 套用到 CSEL0 的全體禁止持續性規則。'),
 ('CDW13 CHPS[9]／PERFS[8]／PERID[7:0]','Set 的 CHPS1 請求改設定，0 不改；PERFS1 請求凍結，0 不是已凍結對象的通用解凍方法。Get 忽略 CHPS/PERFS。','對尚未凍結的 PERID02h 要求改設定可示範 202h；不代表已完成所有能力與重設條件。'),
 ('Get CQE DW0 PMDSS[10]／PPSC[9]／PERFS[8]／PERID[7:0]','選 PERID02h 時：是否製造預設／是否有待變更／凍結或待凍結／對象；高位保留。','PPSC1 表示不能把請求接受與設定已生效當成同一件事。'),
 ('Properties PPS byte0／PERID byte1／MRSTT byte2','PPS5bytes；PERID 辨認對象；MRSTT0 無 reset、1 Controller Level、2 排除 Controller Reset 的 Limited Controller Level、3 subsystem reset、4 main power cycle。','MRSTT0 的變更須在 Set 成功前套用；非零需滿足對應 reset 條件。'),
 ('Properties AUS byte3','bit0 PCAS 支援 Physical Credential Authentication；bit1 PKAS 支援 Programmable Key Authentication；高位保留，0 表示沒有認證解凍方法。','AUS2 只設 bit1，不是兩個 bit 都 1。'),
 ('Properties byte4 PSCUDE[0]','表示改此 personality 是否可能影響 user data；[7:1]保留。','不是目前有多少命令被禁止，也不是凍結狀態。'),
 ('已啟用持續性時的命令互動','若未凍結或無認證解凍支援，不准禁止 Set Features 或 FID22h；若任一 personality 支持認證解凍，允許指定 CDP Authentication/SPSP0002h 的 Security Send/Receive。','不把特定認證用途的例外擴張到所有 Security 操作。'))

example(782,'UIDX 只指定 UUID 清單位置，0 代表不指定。','UIDX2 對第 2 項 UUID；如果那項 UUID 全 0 或對本資訊不受支援，就回 Invalid Field，而不是自動換第 1 項。','UIDX selects a UUID List position, with zero meaning no UUID selected.')
example(347,'UUID List 從索引 1 開始，前 32bytes 保留，不能把 offset0 當第一項。','索引 2 的 entry 起點=32×2=64；命令仍填 UIDX2。清單最多 126 個非零項，127 項強制清 0。','The UUID List starts at index one after a reserved 32-byte region.')
example(348,'一個 32-byte entry 裡，UUID 本體只占後 16bytes。','索引 2 的 entry 從 64 開始；header 在 64，UUID 在 80～95。IDASSOC 只描述廠商關聯，不能用來代替 128-bit UUID。','The UUID occupies the final sixteen bytes of each thirty-two-byte entry.')
group('uuid-fields','把命令索引接到清單，再接到 UUID 本體','只讀廠商 FID 定義選擇所需的索引與格式；不將 UUID 當作權限憑證或密碼。',[782,347,348],
 ('UIDX bits6:0','0 不指定 UUID；非零指向 UUID List 有效項目，還需該資訊支援該 UUID。','C0h 是 FID 候選值，不可能原封不動放進 7-bit UIDX。'),
 ('List bytes31:0／entry i at32×i','前 32bytes 保留，i=1～126 可含有效項目；第 127 項清 0。','i2→offset64，和 UIDX2 的單位不同。'),
 ('Entry ULEH byte0，IDASSOC[1:0]','0 未回報關聯；1 與 PCI Vendor ID 廠商相關；2 與 PCI Subsystem Vendor ID 廠商相關；3 保留。高位及 bytes15:1 保留。','IDASSOC1 不是 UUID List 索引 1。'),
 ('Entry UUID bytes31:16','128-bit UUID；全 0、NVMe Invalid UUID 或不支持該資訊的 UUID 不可作有效選擇。','第 2 項 UUID 的實際 bytes 是 80～95；命令不傳這 16bytes，只傳索引。'))

# Primary coverage is exact. Dependencies are limited to the named fields taught above.
SOURCES = {
 274:('5.2.13.1.20','306','query'),275:('5.2.13.1.20','306','query'),
 276:('5.2.13.1.20','307','basic'),277:('5.2.13.1.20','308-309','enhanced'),278:('5.2.13.1.20','309','enhanced'),
 365:('5.2.16','431-432','command'),366:('5.2.16','433','command'),367:('5.2.16','434','result'),
 28:('3.1.3','71-72','model'),93:('4.1.1','166-168','model'),338:('5.2.14.2.1','378','capability'),
 203:('5.2.13','239','query'),204:('5.2.13','239','query'),205:('5.2.13','240','query'),
 206:('5.2.13','240','query'),207:('5.2.13','240','query'),208:('5.2.13','240-241','query'),
 99:('4.2.1','171','result'),101:('4.2.3','171-172','result'),103:('4.2.3.1','173,175','result'),
 292:('5.2.13.1.28','317-319','persistence'),512:('5.2.30.1.25','511','persistence'),513:('5.2.30.1.25','511-512','persistence'),
 514:('5.2.30.1.25','512-513','persistence'),518:('5.2.30.1.25.4','519','persistence'),519:('5.2.30.1.25.4','520','persistence'),
 782:('8.1.31.2','764','uuid'),347:('5.2.14.2.14','422','uuid'),348:('5.2.14.2.14','422','uuid'),
}
PRIMARY = {274,275,276,277,278,365,366,367}
