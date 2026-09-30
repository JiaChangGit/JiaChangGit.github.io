"""Identify selectors and high-value field groups."""
from scripts.nvme_quickref_data import card, CARDS

card('B333','Identify CDW10：選資料結構，不是選欄位','Identify|CNS|CNTID|CNS 01h|CNS 00h',[
'當Identify資料被解成不合理的容量或能力時，先回查命令選了哪種結構。不同CNS可能回傳同樣大小的buffer，但各byte意義不同。',
'CNS bits7:0選回傳結構；CNTID bits31:16只用於部分操作；bits15:8保留。不使用CNTID的操作，主機應依規定清0，不能把它當任意controller selector。',
'CNS=01h讀處理此命令的controller資訊；CNS=00h讀NVM namespace資訊。若用01h的byte offset去解析00h，即使buffer長度正確，結論仍可能完全錯誤。'],[
'If Identify data appears to contain impossible capacities or capabilities, check which structure the command selected. Equal buffer sizes do not imply identical byte meanings.',
'CNS bits 7:0 selects the returned structure; CNTID bits 31:16 is used by only some operations; bits 15:8 are reserved. Clear unused CNTID as specified rather than treating it as a universal controller selector.',
'CNS=01h returns information for the controller processing the command; CNS=00h returns NVM namespace data. Applying 01h byte offsets to 00h can produce meaningless results despite a correct buffer length.'],'B336 B338 N123')

card('B336','CNS 總表：查結構及有效參數','CNS|NSID|CNTID|CSI|Identify list',[
'不知道應送哪個Identify操作時，從這張表按查詢對象選CNS。每列同時列出NSID、CNTID、CSI是否使用，不能只抄CNS數字。',
'常用01h為controller、02h為active NSID list、03h為namespace識別描述子；05h／06h是command-set-specific namespace／controller，08h是command-set-independent namespace。10h查allocated NSID list；16h粒度、17h UUID list等列也可由此找到來源。',
'active list與allocated list可能不同：已建立但未附加的namespace，不一定在此controller的active list。查不到時先確認選了哪份清單，而不是直接判定namespace不存在。'],[
'Choose an Identify operation by the object being queried. Each row also states whether NSID, CNTID and CSI are used; copying only the CNS value is insufficient.',
'Common values are 01h controller, 02h active NSID list, 03h namespace identifiers, 05h/06h command-set-specific namespace/controller and 08h command-set-independent namespace.10h lists allocated NSIDs; 16h granularity and 17h UUID-list rows provide further entry points.',
'Active and allocated lists can differ: a created but unattached namespace need not appear in this controller’s active list. Check the selected list before concluding that the namespace does not exist.'],'B333 B342 B346')

card('B338','Identify Controller：能力與限制的主要入口','Identify Controller|MDTS|OACS|ONCS|LPA|ELPE|FRMW|SANICAP|SQES|CQES|SGLS|NPSS',[
'這張跨43頁的大表是controller能力、限制及識別資訊的主要來源。速查時先決定要確認哪一類問題，再用下方欄位頁碼前往；不要從第一頁一路掃到最後。',
'傳輸大小查MDTS，Admin命令支援查OACS，I/O能力查ONCS，log支援與長度查LPA／ELPE，韌體查FRMW，清除查SANICAP。queue entry大小查SQES／CQES，資料指標查SGLS；NPSS與Power State Descriptors則一起解讀電源狀態。',
'MDTS非0時，以CAP.MPSMIN定義的最小頁大小乘2^MDTS；例如最小頁4 KiB、MDTS=5得到128 KiB。MDTS=0表示此欄不限制，不代表其他命令或namespace限制都消失。欄位的O／M／R、controller類型及腳註也屬有效條件。'],[
'This 43-page table is the main source for controller identity, capabilities and limits. Select a question first and use the field-page map below instead of scanning from beginning to end.',
'Use MDTS for transfer size, OACS for Admin commands, ONCS for I/O capabilities, LPA/ELPE for logs, FRMW for firmware and SANICAP for sanitization. SQES/CQES describes entry sizes and SGLS pointer support. Interpret NPSS together with Power State Descriptors.',
'For nonzero MDTS, multiply the minimum page size from CAP.MPSMIN by 2^MDTS:4 KiB and MDTS=5 gives 128 KiB. MDTS=0 removes this field’s limit, not every command or namespace limit. O/M/R markings, controller type and footnotes remain part of applicability.'],'B36 B340 B217 N129')
CARDS['B338']['field_routes']=[
 ('MDTS','傳輸大小上限','Transfer size limit',368,368),
 ('OACS','Admin 命令支援','Admin command support',378,380),
 ('FRMW','韌體槽位與更新能力','Firmware slots and update capabilities',380,381),
 ('LPA','Log page 能力','Log-page capabilities',381,382),
 ('ELPE / NPSS','錯誤項目上限／電源狀態數','Error-entry limit / power-state count',382,382),
 ('SANICAP','Sanitize 能力','Sanitize capabilities',387,388),
 ('SQES / CQES','佇列項目大小','Queue-entry sizes',396,396),
 ('ONCS','I/O 命令與功能支援','I/O command and feature support',397,399),
 ('VWC / AWUN / AWUPF','快取與原子性欄位','Cache and atomicity fields',400,400),
 ('SGLS','SGL 類型與對齊','SGL types and alignment',403,404),
]

card('B342','Namespace 識別描述子：不要把 NSID 當永久身分','NIDT|NIDL|NID|EUI64|NGUID|UUID|CSI',[
'要辨認兩次查詢或不同controller看到的namespace是否為同一物件，查這張識別描述子表。命令中的NSID是存取用的識別值，不能代替所有長期識別資訊。',
'NIDT byte0選類型，NIDL byte1給NID長度，bytes3:2保留，NID從byte4開始。類型1／2／3／4分別是8-byte EUI64、16-byte NGUID、16-byte UUID、1-byte CSI。每筆總長NIDL+4；NIDL=0表示清單結束。',
'NIDL=16的一筆佔20bytes，下一筆從原起點+20開始，不是+16。CSI描述命令集，不能因為也放在NID位置就當成globally unique identifier。'],[
'Use identification descriptors to compare namespace identity across queries or controllers. An NSID used to address commands is not a substitute for persistent identity information.',
'NIDT byte 0 chooses the type; NIDL byte 1 gives NID length; bytes 3:2 are reserved and NID begins at byte 4. Types 1/2/3/4 contain 8-byte EUI64, 16-byte NGUID, 16-byte UUID and 1-byte CSI. Total size is NIDL+4; NIDL=0 ends the list.',
'An entry with NIDL=16 occupies 20 bytes, so the next starts at the old offset plus 20, not 16. CSI identifies a command set, not a globally unique namespace despite occupying the NID field.'],'B336')

card('B346','Namespace 共通狀態：可用、受保護與儲存歸屬','CNS 08h|NSTAT|NRDY|NSATTR|FPI|ENDGID|NVMSETID|ANAGRPID',[
'查namespace是否ready、是否受寫入保護、屬於哪個資源群組時，使用這份與I/O command set無關的結構。它與NVM CNS00h的byte配置不同。',
'常查NSFEAT byte0、NMIC byte1、RESCAP byte2、FPI byte3；ANAGRPID在bytes7:4，NSATTR在byte8，後面還有NVMSETID、ENDGID與NSTAT。FPI表示剩餘Format百分比，NSATTR.CWP表示目前受寫入保護，NSTAT.NRDY表示namespace是否ready。',
'controller的CSTS.RDY=1而namespace的NRDY=0，可以是media-independent ready流程中的不同層級狀態，不應立刻視為互相矛盾。ENDGID則用來接到對應Endurance Group的健康log。'],[
'Use this command-set-independent structure for namespace readiness, write protection and resource membership. Its byte layout differs from NVM CNS=00h.',
'Common fields are NSFEAT byte 0, NMIC byte 1, RESCAP byte 2, FPI byte 3, ANAGRPID bytes 7:4 and NSATTR byte 8, followed by NVMSETID, ENDGID and NSTAT. FPI reports remaining Format percentage; NSATTR.CWP reports current write protection; NSTAT.NRDY reports namespace readiness.',
'CSTS.RDY=1 with namespace NRDY=0 can describe different readiness levels during media-independent initialization rather than a contradiction. Use ENDGID to select the corresponding Endurance Group health log.'],'B42 B225 B541')

card('N123','NVM Namespace：容量、格式、原子性與建議粒度','CNS 00h|NSZE|NCAP|NUSE|FLBAS|DPS|DLFEAT|LBAF|NAWUN|NABSN',[
'容量數字、LBA格式或對齊行為有疑問時，這張表是NVM namespace的主要入口。先分清目前格式、支援格式清單與建議效能參數。',
'NSZE bytes7:0是可定址blocks總數，NCAP15:8是最多可配置量，NUSE23:16是目前配置量。FLBAS byte26選格式，DPS byte29選PI設定，DLFEAT byte33描述deallocate後行為；後續NAWUN／NAWUPF與boundary欄位補原子性，LBAF清單提供各格式大小。',
'NSZE=1000表示LBA0～999；若所選LBADS=12，資料容量是1000×4096=4,096,000 bytes。FLBAS=12h不是18-byte格式，而是format index2加metadata傳輸設定；大小要再讀該LBAF。'],[
'This is the primary NVM namespace lookup for capacity, format and alignment behavior. Distinguish the active format, supported-format list and performance recommendations.',
'NSZE bytes 7:0 counts addressable blocks; NCAP bytes 15:8 gives maximum allocation; NUSE bytes 23:16 current allocation. FLBAS byte 26 selects a format, DPS byte 29 selects PI settings and DLFEAT byte 33 describes deallocation behavior. NAWUN/NAWUPF and boundaries qualify atomicity; LBAF entries provide format sizes.',
'NSZE=1000 means LBAs 0–999. With selected LBADS=12, data capacity is 1000×4096=4,096,000 bytes. FLBAS=12h is not an 18-byte format: it selects index 2 and metadata placement, with sizes obtained from that LBAF.'],'N125 N4 N8 N127')
CARDS['N123']['field_routes']=[
 ('NSZE / NCAP / NUSE / NSFEAT','容量與功能條件','Capacity and feature conditions',85,86),
 ('FLBAS / MC / DPC / DPS','格式與保護設定','Format and protection configuration',86,87),
 ('DLFEAT / NAWUN / NAWUPF','Deallocate 行為與原子單位','Deallocation behavior and atomic units',88,89),
 ('NABSN / NABO / NABSPF','原子性邊界','Atomicity boundaries',89,89),
 ('NPWG / NPWA / NPDG / NPDA','效能建議粒度與對齊','Recommended performance granularity and alignment',90,90),
 ('LBAF','格式清單的位置與數量','Format-list location and count',93,93),
]

card('N125','LBAF：資料大小、metadata 大小與相對效能','LBAF|LBADS|MS|RP',[
'FLBAS已選出format index後，到這張表解該格式的4-byte描述子。它回答每個logical block的資料和metadata各有多大。',
'MS bits15:0直接以bytes表示metadata；LBADS bits23:16是資料bytes的2次方指數，0表示該格式目前不可用；RP bits25:24是指定測試情境下的相對效能等級，不是IOPS數值。',
'LBADS=12、MS=8代表4096-byte資料加8-byte metadata。若採extended LBA，傳輸排列每block共4104 bytes；LBADS不包含這8bytes，也不能把RP=0當作所有工作負載一定最快。'],[
'After FLBAS selects a format index, decode its four-byte LBAF entry here. It gives per-block data and metadata sizes.',
'MS bits 15:0 directly counts metadata bytes. LBADS bits 23:16 is the data-size exponent; zero means the format is currently unavailable. RP bits 25:24 ranks relative performance for the specified workload, not IOPS.',
'LBADS=12 and MS=8 mean 4096 data bytes plus 8 metadata bytes. Extended-LBA placement occupies 4104 bytes per block. LBADS excludes metadata, and RP=0 does not guarantee the fastest result for every workload.'],'N123 N153 N154')

card('N127','NVM 專屬 Namespace：延伸 PI 與格式能力','CNS 05h|CSI 00h|LBSTM|PIC|ELBAF|Storage Tag',[
'需要解32／64-bit Guard、Storage Tag或延伸格式時，CNS00h不夠，還要查這份CNS05h、CSI00h資料。它補充格式能力，不取代目前namespace的FLBAS／DPS。',
'LBSTM提供Storage Tag mask，PIC列保護格式能力；ELBAF陣列對應各format index，描述Guard格式與Storage Tag寬度。相關mask有效性還受保護資訊是否啟用，以及PIC和masking-level能力限制。',
'同一個format index應在LBAF與ELBAF配對：前者提供資料／metadata bytes，後者提供PI內部格式。只看到metadata有16bytes，無法直接判定Guard一定是64bits。'],[
'For 32/64-bit Guard, Storage Tags and extended formats, supplement CNS=00h with this CNS=05h/CSI=00h structure. It adds format capabilities rather than replacing FLBAS/DPS.',
'LBSTM supplies a Storage Tag mask, PIC reports protection-format capabilities, and the ELBAF array describes Guard format and tag width for each format index. Mask applicability also depends on PI enablement, PIC and masking-level capabilities.',
'Match the same index in LBAF and ELBAF: one supplies data/metadata sizes, the other PI layout. Sixteen metadata bytes alone do not establish a 64-bit Guard format.'],'N128 N125 N159')

card('N128','ELBAF：Guard 格式與 Storage Tag 位數','ELBAF|PIF|QPIF|STS|QPIFS',[
'查PI資料為何解析錯位時，用這張表確定Guard格式以及Storage／Reference區域如何切割。STS在這裡是Storage Tag Size，不能當成status。',
'STS bits6:0指定Storage Tag位數；PIF bits8:7選16／32／64-bit Guard或qualified格式；只有PIF=11b且相關能力成立時，才使用QPIF bits12:9。PI未啟用時，不能依這些欄位推論實際傳輸含有PI。',
'PIF=10b、STS=16表示64-bit Guard格式，其中48-bit Storage／Reference區的高16bits給Storage Tag，剩32bits給Reference Tag。16、32、64-bit Guard允許的STS範圍不同，不能任意套同一個遮罩。'],[
'Use ELBAF to resolve Guard format and the split between Storage and Reference Tags. STS here means Storage Tag Size, not status.',
'STS bits 6:0 gives Storage Tag width. PIF bits 8:7 selects 16/32/64-bit Guard or a qualified format. QPIF bits 12:9 applies only with PIF=11b and the required capability. These fields do not establish transmitted PI when PI is disabled.',
'PIF=10b and STS=16 selects 64-bit Guard with 16 high bits of its 48-bit Storage/Reference space assigned to Storage Tag and 32 remaining for Reference Tag. Allowed STS ranges differ across Guard formats.'],'N127 N155 N157 N159')

card('N129','NVM 專屬 Controller：命令大小限制及其有效條件','CNS 06h|CSI 00h|VSL|WZSL|WUSL|DMRL|DMRSL|DMSL|NVMDSMSV',[
'Verify、Write Zeroes或Dataset Management因大小被拒絕時，查這份CNS06h、CSI00h結構。Base的MDTS不是每個命令唯一的大小限制。',
'VSL／WZSL／WUSL是以最小記憶體頁為基礎的指數式大小；DMRL是range數，DMRSL是單一range的blocks，DMSL是合計blocks。ONCS內各命令的support-variant bits會改變欄位是強制上限還是建議值，也會改變0的含義。',
'例如DMRL=0且NVMDSMSV=1表示未回報建議range數上限；NVMDSMSV=0時，DMRL=0則表示不支援Dataset Management。不能把所有0都翻成「無限制」。'],[
'Consult this CNS=06h/CSI=00h structure when Verify, Write Zeroes or Dataset Management encounters a size limit. Base MDTS is not every command’s sole constraint.',
'VSL/WZSL/WUSL use minimum-memory-page-based exponential sizes. DMRL counts ranges, DMRSL blocks per range and DMSL total blocks. ONCS support-variant bits determine whether limits are mandatory or recommended and change zero semantics.',
'DMRL=0 with NVMDSMSV=1 means no recommended range-count limit is reported. With NVMDSMSV=0, DMRL=0 means Dataset Management is unsupported. Do not translate every zero as unlimited.'],'B338 N47 N83')
CARDS['N129']['field_routes']=[
 ('VSL / WZSL','Verify／Write Zeroes 大小','Verify / Write Zeroes sizes',103,103),
 ('WUSL / DMRL / DMRSL','Write Uncorrectable 與 DSM range 限制','Write Uncorrectable and DSM range limits',104,104),
 ('DMSL / KPIOCAP / WZDSL','總 blocks、金鑰能力、deallocate 大小','Total blocks, key capabilities, deallocate size',105,105),
 ('AOCS / VER / RLA','Admin 能力、版本與速率限制能力','Admin support, version and rate-limit capabilities',106,106),
]
