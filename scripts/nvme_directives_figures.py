"""Every selected figure has its own takeaway/example and a shared field home."""

EXAMPLES = {}
GUIDES = {}
MEMBERS = {}


def example(n, takeaway, worked, en, source='base'):
    EXAMPLES[source, n] = dict(takeaway=takeaway, example=worked, en=en)


def group(key, title, relation, numbers, *rows, source='base'):
    ident = 'streams-' + key
    GUIDES[ident] = dict(id=ident, title=title, relation=relation, rows=list(rows))
    for n in numbers:
        MEMBERS[source, n] = ident


def token(f):
    return ('base' if f['source_id'] == 'NVME-BASE-2.4' else 'nvm', int(f['number']))


def lesson(f):
    return EXAMPLES[token(f)]


def guide(f):
    return GUIDES[MEMBERS[token(f)]]


example(36, 'CAP.MPSMIN 定義 MDTS 所使用的最小記憶體頁大小單位。',
 'MPSMIN=0 對應 2^(12+0)=4096 bytes；MDTS=5 再乘 2^5，得到 128 KiB。MPSMIN 不是 namespace 的 logical block 大小。',
 'CAP.MPSMIN supplies the minimum memory-page unit used by MDTS.')
group('page-unit', '最小記憶體頁與 logical block 是不同單位',
 '這張能力表只取 MPSMIN，讓讀者能自己完成 MDTS 換算；不展開其他控制器寄存器。', [36],
 ('CAP[51:48] MPSMIN', '最小記憶體頁大小為 2^(12+MPSMIN) bytes，供 MDTS 的非零值當基底。', 'MPSMIN=0、MDTS=5 → 4096×32=131072 bytes。'),
 ('記憶體頁大小 vs. logical block 大小', '前者用於傳输上限與記憶體配置；後者用於 SWS、LBA、Write 的資料長度。', '例子中兩者都選 4096 bytes，是設定相同，不代表兩種單位永遠相同。'))
example(143, 'Admin opcode 表用來辨認 Directive Send／Receive，不是用來選某個 Streams 操作。',
 '19h 選 Send、1Ah 選 Receive；接著還要讀 CDW11 的 DTYPE／DOPER，才能知道是 Release、查參數或配置資源。',
 'The Admin opcode table identifies Directive Send/Receive; DTYPE and DOPER still select the operation.')
group('opcodes', '從 Admin 命令入口接到 Directive 操作',
 '這裡只讀 Directive Send 與 Directive Receive 兩列；不把整個 Admin 命令表納入本篇。', [143],
 ('19h／1Ah', '分別是 Directive Send／Directive Receive；opcode 低 bits 的資料方向不保證每個操作實際都有 buffer 傳輸。', 'Allocate Resources 位於 Receive，但實際沒有資料傳輸，結果在 CQE DW0。'),
 ('NSID Used 與支援欄', '兩者使用 NSID；實際合法值依操作定義。是否實作須看 Directives 支援，不能只因表列出 opcode 就假設可用。', 'Identify Return Parameters 不接受 FFFFFFFFh；Enable Streams 對它另有整體範圍。'))


example(702, 'Directive Type 選資訊交換的類型；Identify=00h 和 Streams=01h 在本篇分別負責管理與分組。',
 '主機要查 Streams 是否支援時，先選 Identify 的 00h；不能因為想查 Streams 就直接跳過 Identify 的支援位元向量。表中的 I/O Command Directive 欄表示是否能隨 I/O 命令使用，不代表目前已啟用。',
 'Directive Type selects the exchange: Identify 00h manages capabilities and Streams 01h carries grouping information.')
example(703, 'I/O 的 DSPEC 必須由 DTYPE 解讀：Streams 下是串流編號，未使用 Directive 時沒有這個作用。',
 'Write 的 DTYPE=1、DSPEC=40，表示使用 stream 40；DTYPE=0、DSPEC=40 則不會因為 DSPEC 非零而自動建立 stream 40。',
 'The I/O DTYPE determines whether DSPEC is a Stream Identifier or has no directive meaning.')
group('types', '先決定類型，再解讀同一個值',
 '兩張表建立類型與欄位的對應；它們不是命令執行順序，也不是裝置的實際能力清單。', [702, 703],
 ('管理 DTYPE：00h／01h', '00h 選 Identify Directive，01h 選 Streams；DSPEC 與 DOPER 的含義依類型決定。', 'Receive 00h/01h 查支援；Receive 01h/01h 查 Streams 參數。'),
 ('I/O DTYPE：4 bits；00h／01h', 'I/O 只容納 00h–0Fh，上方 4 bits 視為 0；00h 不使用 Directive，01h 使用 Streams。', 'Admin 8-bit 類型欄與 Write 4-bit 類型欄不能直接當作相同位置。'),
 ('I/O DSPEC：01h 類型下的編號', '0001h–FFFFh 是可用串流編號，0h 使該 I/O 如同沒有 Directive。', 'stream 1000 是一個編號，和要寫 1000 blocks 不同。'),
 ('02h／03h–0Eh／0Fh', '02h 是本篇不展開的 Data Placement；03h–0Eh 保留；0Fh 的行為由廠商定義。', '辨認這些值是為了讀懂表的邊界，不據此推論其操作或支援狀態。'))

example(93, '共同格式把命令識別、namespace、資料地址與命令專屬控制欄位分開。',
 'CDW11 的 byte offset 是 11×4=44；這是命令內位置。DPTR 裡的 PRP 地址則指向主機 buffer；它不是「第 44 個 byte 的資料」。',
 'The common command format separates command identity, namespace, data pointers, and command-specific controls.')
example(181, 'Receive 的 DPTR 指主機用來接收回覆資料的記憶體。',
 '讀 Streams 參數前準備 32-byte 有效接收區，DPTR 指向它；成功後從該區讀 MSL／NSSA 等欄位。DPTR 本身不含這些參數。',
 'Directive Receive DPTR identifies the host destination for returned data.')
example(182, 'Receive 的 NUMD 用傳輸 Dword 數量減 1 表示長度。',
 '要讀完整的 4096-byte Identify Directive 結構，NUMD=1023；只讀 32 bytes 則是 7，只能取得開頭的 Supported 向量，讀不到 Enabled 向量。',
 'Directive Receive NUMD encodes the requested Dword count minus one.')
example(183, 'Receive CDW11 的 DTYPE／DOPER 選回覆種類，DSPEC 依該操作決定是否使用。',
 'Streams Get Status 使用 DTYPE=1、DOPER=2、DSPEC=0，即 CDW11=00000102h；不能把 DSPEC 填成要從第幾條串流繼續讀。',
 'Receive CDW11 selects the directive and operation; DSPEC usage depends on that operation.')
example(184, 'Send 的 DPTR 只在操作需要傳送資料時，指出主機來源 buffer。',
 '本篇的 Enable Directive 與兩個 Streams Release 操作都沒有資料傳輸。不能因為 Send 命令格式畫有 DPTR，就額外製造一份串流資料 payload。',
 'Directive Send DPTR is a host-source pointer only when the selected operation transfers a buffer.')
example(185, 'Send 的 NUMD 是有資料傳輸時的長度格式，不是所有 Send 操作都要搬資料。',
 '若某個已定義的操作要送 16 bytes，格式上 NUMD=3；這是長度換算例，不是說本篇的 Release Identifier 需要送 16 bytes。',
 'Send NUMD defines buffered-transfer length; the operation decides whether any transfer occurs.')
example(186, 'Send CDW11 同時選 Directive、動作與必要的特定參數。',
 'Release Identifier 7 使用 DSPEC=7、DTYPE=1、DOPER=1，CDW11=00070101h；Release Resources 用 DOPER=2，不靠 DSPEC 指定要歸還幾個資源。',
 'Send CDW11 combines directive type, operation, and any operation-specific DSPEC value.')
group('envelope', '命令裡的位置、資料的位置、資料的長度',
 '這組圖只定義共用容器，實際 buffer 結構與有無傳輸仍由後面的操作定義決定。', [93, 181, 182, 183, 184, 185, 186],
 ('OPC／CID／NSID', 'OPC 位於 CDW0[7:0]，CID 在 [31:16]，NSID 在 CDW1；命令身分與 namespace 對象分開。', 'Admin OPC=1Ah 表示 Receive，19h 表示 Send；同一個 NSID 可有多筆不同 CID 的要求。'),
 ('DPTR：CDW6–9，128 bits', '使用資料 buffer 時指定主機記憶體；PCIe Admin 用 PRP。它與命令內的欄位 offset 不同。', '接收 32 bytes 時，先準備足夠記憶體，再設定 NUMD=7；兩者共同限制安全的資料範圍。'),
 ('CDW10[31:0] NUMD', '有傳輸時，bytes=(NUMD+1)×4；Receive 超過結構大小不會得到額外資料。', 'NUMD=3 對應 16 bytes；對 32-byte 參數只能讀出前半部。'),
 ('CDW11[31:16] DSPEC／[15:8] DTYPE／[7:0] DOPER', 'CDW11=(DSPEC<<16)|(DTYPE<<8)|DOPER。DSPEC 不使用時不要把它解成長度或位移。', '釋放 stream 7：00070101h；查狀態：00000102h。'),
 ('CDW12／CDW13；其餘保留', '只有所選操作定義的欄位才使用；Enable 的 CDW12 和 Allocate 的 CDW12 是不同格式。', 'Enable CDW12=00000101h；要求 3 個資源的 Allocate CDW12=00000003h。'))

example(537, 'EXHID 選 Host Identifier 的長度，支援能力與其他控制器的非零格式會限制這個選擇。',
 'HIDS=0 卻送 EXHID=1 會被拒絕。若兩種長度皆支援，C1 已使用非零 64-bit 值，C2 要登記 128-bit 值還需通過一致格式檢查。',
 'EXHID selects Host Identifier width, subject to supported widths and subsystem consistency.')
example(538, 'HOSTID 是身分資料；64-bit 模式只使用低 8 bytes，128-bit 模式使用全部 16 bytes。',
 '例示識別值 1122334455667788h 在 64-bit 模式佔 bytes 7:0；bytes 15:8 保留。C1、C2 使用相同非零值才建立同一主機的關聯，兩個 0h 不會。',
 'HOSTID carries the identity: the lower eight bytes in 64-bit mode or all sixteen in extended mode.')
example(197, 'Get Features 的 DPTR 是接收 HOSTID 結構的位置。',
 '讀 FID 81h 的目前值時，不只看 CQE DW0，還要讀 DPTR 指向的 HOSTID buffer；SEL=3 的支援能力查詢則是另一種回覆。',
 'Get Features DPTR identifies the buffer used to return HOSTID for value queries.')
example(198, 'Get Features CDW10 用 FID 選功能、SEL 選查詢種類。',
 'FID=81h、SEL=0 查目前識別值；SEL=3 查可變更、scope 與可保存能力，不能把兩者的 DW0 當成同一結構。',
 'Get Features CDW10 selects the Feature Identifier and the requested value/capability class.')
example(199, 'UIDX 是選擇相關 UUID 的索引，不能拿來存 Host Identifier。',
 '本篇一般 FID 81h 例子不使用 UUID 選擇，UIDX=0；真正的非零 HOSTID 放在資料 buffer。',
 'Get Features UIDX selects an associated UUID when applicable; it is not the Host Identifier.')
example(201, 'SEL=3 的 CQE DW0 回覆 Feature 能力位元，不回覆 HOSTID 的數值。',
 '讀到 SVBL=0 表示不支援保存；它不是 Host Identifier=0h。CHANG 與 NSSPEC 分別回答可變更與 namespace 特定性，也不是串流數量。',
 'With SEL=3, CQE DW0 reports Feature capabilities rather than the numeric HOSTID.')
example(463, 'Set Features 的 DPTR 指向主機提供的 HOSTID。',
 '要登記主機 A，先準備符合 EXHID 長度的身分資料，再由 DPTR 指向該 buffer；FID 81h 的控制值和身分值分開傳遞。',
 'Set Features DPTR locates the host-supplied HOSTID data.')
example(464, 'Set Features 的 SV 控制保存要求，但 FID 81h 本身不允許保存。',
 '本篇用 FID=81h、SV=0；即使 Set 成功，也不能因為它是 Feature 就推論 power cycle 後還有同一值。',
 'Set Features SV requests saving, but Host Identifier is not a saveable Feature.')
example(465, 'Set Features 的 UIDX 選 UUID 關聯，與 CDW11.EXHID 的長度選擇不同。',
 'UIDX=0、EXHID=1 分別表示不選 UUID 與使用 128-bit HOSTID；兩個值位於不同 CDW，不能互換。',
 'Set Features UIDX selects UUID association separately from EXHID width selection.')
group('hostid', '一筆 FID 81h 請求：選功能、選長度、提供身分',
 'Get／Set Features 共通圖只取本篇需要的欄位。Host Identifier 的值、格式與目前狀態共同決定是否可登記。', [197, 198, 199, 201, 463, 464, 465, 537, 538],
 ('FID：CDW10[7:0]；Get SEL：[10:8]', 'FID=81h；SEL=0／1／2／3 分別選目前／預設／保存／支援能力。FID 81h 不存在可保存值。', '讀目前 HOSTID 選 SEL=0；查功能能力才選 SEL=3。'),
 ('Set SV：CDW10[31]；UIDX：CDW14[6:0]', 'SV 表示保存要求；本例 SV=0。UIDX=0 不選 UUID，與 HOSTID 無關。其餘保留位元不可當作附加識別值。', 'FID 81h 的基本 Set CDW10=00000081h；HOSTID 不放進 CDW10。'),
 ('SEL=3 CQE DW0：CHANG[2]、NSSPEC[1]、SVBL[0]', '三個 bit 分別說功能是否可改、是否 namespace 特定、是否可保存。Feature 能力不是 Feature 的目前值。', 'SVBL=0 只表示不可保存，不能據此判斷目前 HOSTID 是否已初始化。'),
 ('EXHID：CDW11[0]；[31:1] 保留', '0 選 64-bit；1 選 128-bit。須符合裝置支援及已有非零 Host Identifier 的一致格式要求。', '主機要用 128-bit，先確認 CTRATT.HIDS=1；不能靠把 buffer 加長就略過能力檢查。'),
 ('HOSTID：bytes 15:0', '64-bit 用 bytes 7:0，其餘保留；128-bit 用整欄。非零目前值不能以另一筆 Set 直接覆寫。', '目前為非零 A，再 Set 成 B，回 Command Sequence Error。'),
 ('0h、相同非零值、saved value', '0h 不關聯其他控制器；相同非零值代表共同主機；PCIe 預設 0h 且此 Feature 不可保存。', '先用 0h 配置資源，再登記 A，不會自動讓那些資源變成 A 的配置。'))

example(338, 'DIRS、HIDS 與 MDTS 分別回答 Directives 支援、128-bit 身分支援、傳輸上限。',
 'DIRS=1 還需要 Identify Directive 查 SDIRS；HIDS=1 才支援 EXHID=1；MDTS=5、最小頁 4 KiB 時，最大傳輸為 128 KiB。三者不能相互推論。',
 'DIRS, HIDS, and MDTS independently describe Directives support, 128-bit identity support, and maximum transfer size.')
group('capabilities', '從 Identify Controller 只取會影響本篇判斷的能力',
 'Figure 338 是很長的結構；本篇只追蹤下列欄位，不要求讀者把整張表一次背完。文件頁 342、345、347、353 提供本篇所用欄位。', [338],
 ('OACS：bytes 257:256，DIRS bit 5', '1 表示支援 Directives，並伴隨 Send／Receive／Identify Directive 的支援。', 'DIRS=1 不代表 SDIRS=1，仍要查 Streams 的個別支援。'),
 ('CTRATT：bytes 99:96，HIDS bit 0', '1 表示支援 128-bit Host Identifier。它不是目前 EXHID 或 HOSTID 的值。', '能力支援 128-bit，不等於主機已登記一個 128-bit 非零身分。'),
 ('CTRATT.RHII bit 18', '1 表示使用 reservations 需要非零 Host Identifier；0 表示未回報這項要求，不能直接推論所有零值情境都支援。', 'RHII 是 reservation 的身分要求；Streams 使用自己的 NSSC.SRNZID，不能把兩個 bit 互換。'),
 ('MDTS：byte 77', '非零值表示最小頁大小×2^MDTS；0h 表示沒有此最大值限制。頁大小另由 CAP.MPSMIN 定義。', '最小頁 4 KiB、MDTS=5 → 128 KiB；和換成 bytes 後的 SWS 比較。'))

example(704, 'Identify Directive 的 DOPER=01h，在 Receive 是查參數，在 Send 是啟用或停用。',
 '讀能力用 Receive 00h/01h；啟用 Streams 用 Send 00h/01h，然後以 CDW12 選 Streams。操作碼相同不表示動作相同。',
 'For the Identify Directive, DOPER=01h means Return Parameters on Receive and Enable Directive on Send.')
example(705, 'Supported、Enabled、跨 reset 保留是三份獨立的位元向量。',
 'SDIRS=1、SDIRE=0 表示裝置有能力但這個 namespace 還沒啟用；SDIRCLR=0 又是另一個問題，不能把它當成不支援。',
 'Supported, Enabled, and persistence across resets are three independent bit vectors.')
example(706, 'Enable 的 CDW12 選目標 Directive 與開關，外層仍由 Identify Directive 承接。',
 'CDW12=00000101h 是 target DTYPE=1、ENDIR=1；00000100h 是停用同一類型；00000001h 不是「啟用第一種類型」，而是非法地要求改變 Identify。',
 'Enable CDW12 selects the target directive and ENDIR while the outer command uses the Identify Directive.')
example(707, 'Enable 可能因為沒有足夠資源而回 Stream Resource Allocation Failed。',
 'SDIRS=1 只能證明支援，不能保證此刻啟用一定成功。收到 command-specific status 7Fh，要按「啟用 Streams 的資源不足」理解，不是 NUMD=7Fh。',
 'Stream Resource Allocation Failed can report insufficient resources while enabling Streams.')
group('enable', '能力位元如何連到啟用要求',
 '先讀能力，再發正確的 Identify 操作；位元位置從各向量起點計算，不是全部從結構 byte 0 計算。', [704, 705, 706, 707],
 ('4096-byte 回覆：bytes 31:0／63:32／95:64', '依序是 Supported、Enabled、Persistent Across Controller Level Resets；bytes 4095:96 保留。', '讀 64 bytes 只有前兩組，尚未取得第三組。'),
 ('各向量 bit 0／1', 'bit 0 是 Identify，bit 1 是 Streams。Identify 的支援與啟用位元固定 1；Streams 的支援／啟用分開回報，跨 reset 保留狀態的 SDIRCLR 固定 0。', 'SDIRE 位於 byte 32 的 bit 1；SDIRCLR 位於 byte 64 的 bit 1。'),
 ('各向量 bit 2／15；其他保留', 'bit 2 描述本篇不展開的 Data Placement，bit 15 描述廠商類型。支援／啟用／保留使用相同 bit 位置，意義由向量決定。', 'VSDIRCLR 表示廠商類型是否跨 reset 保留，不能把廠商結論套到 Streams；DPDIRCLR 在支援該類型時為 1。'),
 ('Identify 的 IDIRCLR bit 0', '主機不能改變 Identify 的啟用狀態，因此其保留位元為 0；不是 reset 後不再支援 Identify。', '重設後仍從 Identify Directive 查詢其餘類型。'),
 ('CDW11 DTYPE=00h／DOPER=01h；CDW12 DTYPE[15:8]／ENDIR[0]', '外層選 Identify 的 Enable；內層 01h 選 Streams。CDW12[31:16] 與 [7:1] 保留。', '啟用：CDW11=00000001h，CDW12=00000101h；沒有資料 buffer。'),
 ('NSID／Host Identifier／SRNZID', '啟用狀態跟 namespace 與主機關聯；SRNZID=1 時，Host Identifier 必須先非零。', '單一 namespace 使用其 NSID；Streams 啟用的 FFFFFFFFh 是 subsystem 範圍，不能誤當為查詢的通用值。'),
 ('失敗條件與狀態', '不支援的類型或非法目標為 Invalid Field in Command；未初始化的必要身分為 Host Identifier Not Initialized；資源不足可為 command-specific 7Fh。', '先確認哪一個操作失敗，再解釋 status，不能只讀數值 7Fh。'))

example(212, 'Parameter Error Location 指命令參數的 byte／bit 位置，不是資料 LBA。',
 'Streams 的互斥啟用限制若產生 Error Information 紀錄，§8.1.9.3 指定 PEL 指向 DOPER。DOPER 位於 CDW11 的低 byte，因此 byte offset=44、bit offset=0，PEL=002Ch。',
 'Parameter Error Location identifies a command-field byte/bit location, not a data LBA.')
group('error-location', '把錯誤位置對回原命令欄位',
 '本篇只取 Figure 212 的 PEL。它是 §8.1.9.3 對特定拒絕情境的必要引用，不展開其他 Error Information 欄位或額外錯誤排查流程。', [212],
 ('PEL：Error Entry bytes 15:14', '適用時指向出錯參數的最低有效 byte／bit；不是特定命令的錯誤時，必須設為 FFFFh。', '先確認紀錄確實對應此筆命令，才對回原 SQE。'),
 ('PEL.BYTLOC[7:0]／BITLOC[10:8]', '前者是命令內 byte offset，後者是該 byte 中的 bit offset；PEL[15:11] 保留。', 'CDW11 的位置是 11×4=44；DOPER 從 bit 0 開始，因此 PEL=44=002Ch。'),
 ('啟用限制與欄位編碼', '若 namespace 所屬群組已啟用 Flexible Data Placement，Streams 不得啟用；若因該拒絕建立紀錄，規則要求指出 DOPER。', '這項錯誤定位要求不改變 Figures 704／706 的 Enable 編碼：外層仍是 Identify，CDW12 才選 Streams。'))

example(708, '一個 Stream Granularity 由多個 SWS 單位組成，完整串流又可跨多個 granularity 單位。',
 'SWS=8 blocks、SGS=4 時，一個 granularity 是 32 blocks。上層圖有「first／last」不代表主機只能送第一筆和最後一筆 Write；它是在畫大小的組成。',
 'A stream-granularity unit contains multiple SWS units, and a complete stream can span multiple granularity units.')
group('sizes', '把圖中的大小統一成 logical blocks 與 bytes',
 'Figure 708 沒有地址與時間軸，它是大小關係圖；欄位值見 Figure 712，SWS 單位見 NVM §5.13。', [708],
 ('SWS first…last → 一個 Stream Granularity', 'SGS 的數值是包含多少個 SWS；SGS×SWS 才是 logical block 數。', '8 blocks/SWS × 4 SWS = 32 blocks；4096 bytes/block 時是 128 KiB。'),
 ('SGS first…last → Complete Stream', '完整串流可包含多個粒度單位，並不是只有一筆命令大小。', '同一 stream 可以由多筆符合 SWS 的 Write 持續增加資料。'),
 ('Write 對齊／解除配置對齊', 'Write 起點與長度用 SWS 比較；對相關資料的解除配置建議使用換算後的 Stream Granularity。', 'LBA 136 是 8 的倍數卻不是 32 的倍數；兩種最佳化條件不同。'))

example(709, 'Streams 的五種管理操作，依命令方向和 DOPER 選擇，各自回答不同問題。',
 '想知道開了哪些編號用 Receive/02h；想取得專用容量用 Receive/03h；兩者都不是 Send/01h 的結束單一編號。',
 'The five Streams management operations are selected by command direction and DOPER.')
example(711, 'Streams 的 7Fh 表示無法提供專用資源且沒有可用的 subsystem 資源。',
 '要求專用資源沒拿到時，要分清：可能失敗回 7Fh，也可能因仍有共用資源而成功回 NSA=0。兩者不是同一結果。',
 'Streams status 7Fh reports failure to allocate exclusive resources with no subsystem resources available.')
example(712, 'Return Parameters 把上限、資源池、主機可見配置與大小提示放在不同欄位。',
 'MSL=8、NSSA=5、NSSO=2、NSA=3、NSO=1 時，5 是非專用資源池大小，2 是其中開啟數，3 是本例專用配置，1 是本例已開啟數。不能把 5 當成完全閒置的資源數。',
 'Return Parameters separates subsystem limits and pool usage, host-visible allocation, and size hints.')
example(714, 'NSR 直接保存主機要求的專用資源數量，不使用數量減 1 的編碼。',
 '要求 4 個資源填 CDW12=00000004h；如果習慣性減 1 填 3，控制器看到的就是要求 3 個。',
 'NSR is the direct requested allocation count, not a zero-based count.')
example(715, 'Allocate 的 CQE DW0.NSA 回實際配置數量，不能只看成功狀態或原始 NSR。',
 'NSR=4、成功 CQE 的 NSA=3，表示實際取得 3 個專用資源；NSA=0 則要按可使用 subsystem 資源的分支理解。',
 'Allocation CQE DW0.NSA reports the actual grant rather than echoing NSR.')
group('resources', '五個數量欄位，分別在數什麼',
 'Return Parameters 是 32 bytes。先分欄位的作用範圍，再比較數值；不能把同名的 NSA 回覆與請求 NSR 混為一個值。', [709, 711, 712, 714, 715],
 ('MSL bytes 1:0／NSSA 3:2／NSSO 5:4', 'MSL 是 subsystem 同時開啟上限；NSSA 是未專用配置的資源池大小；NSSO 是使用該池的開啟串流數。', 'MSL=8，專用配置總數為 3，則池有 5；其中用掉 2 時，NSSA 仍是 5、NSSO 是 2。'),
 ('NSSC byte 6：SRNZID[1]／SSID[0]', 'SRNZID 決定啟用前是否必須有非零主機身分；SSID 決定不同非零主機是否可共享編號。', 'SRNZID=1、SSID=0 同時表示必須初始化身分、不同主機的同號串流分開。'),
 ('SWS bytes 19:16／SGS 21:20', 'SWS 在 NVM 以 logical blocks 計；SGS 以 SWS 計。SWS 可能因重新格式化改變。', 'SWS=8、SGS=4 → 32 blocks；不是 8+4，也不是 4 bytes。'),
 ('NSA bytes 23:22／NSO 25:24', 'NSA 是指定 namespace 在本次主機關聯下的專用配置數；NSO 是同一可見範圍的開啟數。SSID 影響可見的主機集合。', '先配置 3 尚未寫入時，NSA=3、NSO=0 完全合理。'),
 ('NSID=FFFFFFFFh 的 Return Parameters', 'subsystem 欄位仍回覆；共同適用的 namespace 值可回覆，其他 namespace 特定欄位清 0；SWS 無法單一表示時可為 0、SGS 可為 0。', '此時 NSA=0 不足以證明每一個 namespace 都沒有專用配置；需要查特定 NSID。'),
 ('NSR：CDW12[15:0] → NSA：CQE DW0[15:0]', '兩者都是直接計數，實際授予可小於要求。兩個 Dword 的高 16 bits 保留；本操作沒有資料傳輸。', 'NSR=4 得 NSA=3 時，之後以 3 安排追蹤容量。'),
 ('既有專用配置／配置失敗', '已有配置再申請會回 Invalid Field in Command；要改數量先全部釋放，再請求完整新數量。', '從 3 改 5 不能只再送 NSR=2；也不能把 7Fh 失敗當成成功取得 0 個的分支。'),
 ('保留區 bytes 15:7、31:26；NSSC[7:2]', '這些位置不提供本篇定義的參數；不要拿殘留 buffer 值當成更多資源欄位。', '從 32-byte 結構外讀到舊的非零資料，不是額外的 Streams 能力。'))

example(710, '共享判斷先固定 namespace，再看相同非零 Host Identifier 與 SSID。',
 '原圖 C1、C2 皆屬 A，C3 屬 B、C4 屬 C，四條路徑都用編號 1。SSID=0 得到 A／B／C 三組，SSID=1 才合成同一組；圖上的 a、b、c、d 是路徑標示。',
 'Figure 710 groups equal stream numbers by namespace, nonzero Host Identifier, and SSID.')
group('sharing', '四條路徑，為什麼可能是三條串流或一條串流',
 '圖內 controller 數量和 stream 數量沒有固定的一比一關係；原圖所有路徑都連到同一 namespace。', [710],
 ('Host A → Controllers 1、2', '相同非零 Host Identifier A 代表同一主機，對共同 namespace 的同號串流共享。', '兩條路徑各送一筆 stream 1 的 Write，仍屬同一串流。'),
 ('Host B／Host C → Controllers 3、4', '不同非零身分是否合併，由 NSSC.SSID 決定。SSID=0 不合併；SSID=1 合併同一 namespace 的同號串流。', '固定同號 1：SSID=0 為 3 組，SSID=1 為 1 組。'),
 ('NSID 與 0h 身分邊界', '改成不同 namespace 就不能沿用同一組；0h 也不加入非零身分共享。', '即使 SSID=1，C4 的身分改為 0h，不能仍把它當成原先共同串流的一條路徑。'))

example(70, 'Write 的 SLBA 是資料寫入起點，不是串流編號。',
 'SLBA=128，CDW10=00000080h、CDW11=0；stream 7 另放 DSPEC。這筆寫入從 LBA 128 開始，不會因 stream=7 改成 LBA 7。',
 'Write SLBA specifies the destination start independently of the Stream Identifier.', source='nvm')
example(71, 'Write CDW12 把 DTYPE、CETYPE 與 NLB 放在不同 bit 範圍。',
 '本例 DTYPE=1、CETYPE=0、NLB=7，其他示範位元為 0，得到 00100007h。NLB 的 7 表示 8 blocks；不是要求 7 個串流。',
 'Write CDW12 separates directive type, command extension selection, and zero-based block count.', source='nvm')
example(72, 'CETYPE=0 時，Write CDW13 的高 16 bits 是 DSPEC，低位的 DSM 屬性是另一組提示。',
 'DSPEC=7、DSM=0 得 CDW13=00070000h；DSM=0 只表示不提供這些屬性資訊，不會取消高 16 bits 的 stream 7。',
 'For CETYPE=0, Write CDW13 places DSPEC in the upper sixteen bits, independently of DSM attributes.', source='nvm')
group('write', 'Write 的地址、數量與串流標記如何組合',
 '本組是必要引用，只教一般 CETYPE=0 Write 連到 Streams 的欄位，以及讀表時必須分開的其他提示。其他完整 Write 功能不在這裡重講。', [70, 71, 72],
 ('SLBA：CDW10／11', '低 32 bits 在 CDW10，高 32 bits 在 CDW11，合成 64-bit 起始 logical block address。', 'SLBA=128、NLB=7 → LBA 128–135。'),
 ('CDW12 DTYPE[23:20]／CETYPE[19:16]／NLB[15:0]', 'DTYPE=1 是 Streams；本例 CETYPE=0；NLB 保存 blocks−1。其他 Write 控制位元依其功能處理，不由 stream 編號決定。', 'DTYPE=1、NLB=7 → 本例 CDW12=00100007h。'),
 ('CDW13 DSPEC[31:16]／保留[15:8]／DSM[7:0]', 'DSPEC 指串流編號；低 8 bits 的 DSM 是額外工作負載提示，不是 Dataset Management 命令本身。', 'stream 40 放在高 16 bits；本例 DSM=0，表示不額外提供這些屬性資訊。'),
 ('DSM 的 INCPRS[7]／SEQREQ[6]／AL[5:4]／AF[3:0]', '分別描述不可壓縮、連續寫入請求、預期延遲與頻率；全 0 表示未提供相關資訊，和 DSPEC 獨立。', '是否提供順序寫入提示，不會改變同一 namespace 上 stream 7 的身分判斷。'),
 ('FUA 與資料持久保存', 'FUA 位於 CDW12[30]，它的持久保存要求獨立於 DTYPE；Streams 本身不新增排序或持久性保證。', '本例 FUA=0，不能把「有 stream」當成「已強制寫到非揮發媒體」。'), source='nvm')

example(713, 'Get Status 先提供開啟數量，接著按數值由小到大列出 Stream Identifier。',
 'OSC=3、後續 7／40／1000 共需要 2+3×2=8 bytes，NUMD=1 可取得這個前綴。若 OSC 比可容納數更多，這次讀取就是部分清單。',
 'Get Status returns an open count followed by numerically sorted Stream Identifiers.')
group('status', '清單的數量、位置與身分範圍',
 '這張表的 SID1、SID2 是「第幾個回覆欄位」，不是要求它的值必須是 1、2；每個欄位皆為 2 bytes。', [713],
 ('OSC bytes 1:0', '直接表示目前開啟數量；與 NSID／Host Identifier／SSID 選到的可見範圍一起解讀。', 'OSC=3、SID1=7、SID2=40、SID3=1000 → 3 條串流，最高編號不是數量。'),
 ('SIDk：byte offset 2×k，k 從 1 起算', '每筆 2 bytes，依數值遞增；第 1 筆位於 bytes 3:2，最後可至 bytes 131071:131070。', '第 3 筆從 offset 6 開始，占 bytes 7:6；這裡的 index 和 identifier 不同。'),
 ('NUMD 與有效前綴', '總結構上限 131072 bytes；可按需要讀前綴，但至少要有 OSC 才知道清單是否完整。傳輸長度以 4 bytes 為單位。', '要容納 4 個編號需要 10 bytes，向上取 12 bytes，NUMD=2；只解讀實際有效的 4 筆。'),
 ('NSID=FFFFFFFFh／SSID', '整體查詢只列使用非專用 subsystem 資源的編號，跨 namespace 的重複值只回一次；特定 NSID 查詢依主機可見範圍回覆。', 'namespace 1 與 2 的共用資源都開啟 7，整體清單只列一個 7，不能用它分辨兩個 namespace 的細節。'))
