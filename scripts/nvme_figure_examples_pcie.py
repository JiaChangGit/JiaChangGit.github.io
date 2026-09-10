"""PCIe figure-specific explanations; configuration registers retain PCIe context."""
DATA = '''
1|PCIe Transport 補充 NVMe 共通機制在 PCIe 上的存取方式。|解釋 CC、CSTS 的狀態含義時看 Base；說明主機如何透過 PCIe 映射位置存取它們時看 Transport。
2|傳輸層次圖把 NVMe 操作與承載它的 PCIe 機制分開。|同一個 NVMe Read 可能涉及多次 PCIe 交易；不能把一個 TLP 直接當成一筆完整 NVMe 命令。
3|PCIe 暫存器總覽把組態資訊、中斷能力與錯誤回報放在不同區域。|初始化時先找 BAR 與 capability list；讀 NVMe controller property 則走映射後的記憶體空間，兩者不是同一套 offset。
4|Doorbell 依 queue 編號與 DSTRD 交錯排列。|先找 SQ0 Tail、CQ0 Head，再按 stride 找 SQ1 Tail、CQ1 Head；queue 編號每加 1 會跨過兩個 doorbell 位置。
5|SQ Tail Doorbell 通知控制器主機已提交到哪個位置。|DSTRD＝0 時 stride＝4 bytes，SQ1 Tail offset＝1000h＋2×4＝1008h；寫入的是 tail index，不是命令 buffer 位址。
6|CQ Head Doorbell 通知控制器哪些完成項目已被主機消耗。|DSTRD＝0 時 CQ1 Head offset＝1000h＋3×4＝100Ch；主機讀完 CQE 後推進 head，讓相應位置可再次使用。
7|建立 CQ 時選擇其中斷向量，還要符合目前中斷模式能力。|IV＝3 指向量 3；若目前只啟用不足的向量數，不能只因欄位放得下 3 就認定有效。
8|命令處理圖分開 SQ 取命令、資料交換與 CQ 回報結果。|追一次 Write：主機提交 SQE、控制器取得資料並處理、最後寫 CQE；doorbell 更新只代表提交位置改變。
9|Pin、MSI 與多 MSI 模式的通知行為需要分別理解。|多個 CQ 共用一個通知來源時，主機可能需要檢查多個 CQ；中斷本身不攜帶每一筆 NVMe 完成結果。
10|PCIe configuration header 是尋找識別碼、BAR 與 capabilities 的入口。|從 offset 10h 讀 BAR 資訊，與在映射記憶體 offset 1000h 寫 doorbell，是兩個不同位址空間的操作。
11|VID 與 DID 識別 PCIe 廠商與裝置類型。|同一 DID 的兩張卡仍可有不同 serial number；這裡不是替每個 namespace 分配唯一 ID。
12|PCI Command register 控制 PCIe Function 的基本存取能力。|啟用相應記憶體與 bus-master 能力，和啟用 NVMe 的 CC.EN，是不同層的設定，不能互相取代。
13|PCI Device Status 回報 PCI 層的狀態資訊。|此處的狀態不是 NVMe CQE 的 SCT／SC；收到傳輸層問題時，要先辨識是哪一套回報。
14|Revision ID 表示 PCI 裝置修訂識別。|RID 改變不必然等於 NVMe 規格版本改變；規格版本另看對應 Version 欄位。
15|Class Code 以類別、子類別與程式介面識別裝置功能。|此處 CC 是 PCI Class Code，Base 的 CC 是 Controller Configuration；兩個同名縮寫出現在不同空間，用途完全不同。
16|Cache Line Size 欄位依 PCIe 綁定規則解釋。|不要把 CLS 當成 SSD 內部快取大小；即使欄位名稱有 Cache，也不提供 NAND 或 DRAM 容量資訊。
17|Master Latency Timer 是組態 header 中的既定欄位。|讀到此欄位時依本綁定的規則處理，不以名稱推論它限制每筆 NVMe Read 的完成時間。
18|Header Type 說明組態 header 類型及多功能資訊。|發現 multi-function 標記後，枚舉各 Function；不能把同一裝置的所有 Functions 只當成一個 NVMe queue。
19|PCI BIST 是 PCI 組態機制中的自我測試欄位。|它與 NVMe Device Self-test 命令不同，不能把 PCI BIST 的完成碼拿去查 NVMe 的 Self-test Result 格式。
20|BAR0 包含記憶體映射基底的低部與屬性位元。|取 BA 前先去除屬性 bits，再與 BAR1 組合；直接把 BAR0 原值當完整主機位址會混入型別資訊。
21|BAR1 補上 64-bit 記憶體 BAR 的高位元。|基底高部非零時，漏掉 BAR1 會把裝置映射到低 4 GiB 的另一個位置；低部相同不代表同一位址。
22|BAR2 的用途依裝置採用的配置解釋。|先確認這是 Index／Data Pair 還是廠商用途，再讀其欄位；不能假設所有 BAR 都指向同一套 NVMe properties。
23|CardBus CIS Pointer 是組態 header 中保留的既定位置。|看到 CCPTR 不代表 NVMe 裝置真的提供 CardBus 功能；依此 transport 的適用規則解釋它。
24|Subsystem Identifiers 識別產品或 subsystem 的廠商與型號資訊。|同一 VID／DID 的產品可能有不同 SSVID／SSID；兩組 ID 不應只保留其中一組就認為資訊完全等同。
25|Expansion ROM 欄位描述選用的 ROM 映射資訊。|裝置是否提供 ROM 與是否有 NVMe Boot Partitions 是不同能力，不能因 EROM 不存在就推論沒有 Boot Partition。
26|Capabilities Pointer 指向 PCI capability 串列的入口。|先讀 CP 找第一個 capability，再沿 NEXT 找其他項目；不要把每個能力都假設固定出現在相同 offset。
27|Interrupt Information 描述傳統中斷相關組態。|使用 MSI-X 時，通知位址与資料來自相應機制，不能只讀 IPIN／ILINE 就說明所有中斷路由。
28|Minimum Grant 是既定 PCI header 欄位，不是 NVMe 佇列保證。|不能把 GNT 值解釋成 SQ 每輪保證取得的命令數；NVMe 仲裁參數在不同機制中定義。
29|Maximum Latency 欄位不等於每筆儲存 I/O 的延遲上限。|想比較讀取延遲時，不能拿 MLAT 原值當微秒；先按本欄位在 PCIe 綁定中的規則閱讀。
30|Power Management capability 將能力與目前控制狀態分開。|先讀 PC 看支援，再讀 PMCS 看目前設定；能進入某個狀態，和目前已在該狀態，是兩個資訊。
31|Power Management 的 capability header 同時提供識別碼與下一項位置。|確認 CID 後沿 NEXT 找下一個 capability，不能把 NEXT 當成某個電源狀態的值。
32|Power Management 能力 bits 描述可用電源狀態與相關事件能力。|裝置宣告某狀態支援後，主機才依規則選擇；不能只因 PS 欄位有該編碼就假設裝置支援。
33|PMCS 的 PS 與事件 bits 控制、回報 PCI 電源管理。|PCI 電源狀態與 NVMe Power State 是不同層；把 PS 改變後，還要依相應轉換規則理解控制器可用性。
34|MSI capability 把向量控制、通知位址與資料組在一起。|主機配置一組 MSI，既要決定啟用數量，也要提供訊息目的位址與資料；只設 enable 不足以描述完整通知。
35|MSI 識別 header 讓主機在 capability list 中找到 MSI。|由 NEXT 串列定位 MSI 後，其他欄位位置才以 MSICAP 為基底計算，不是永遠從 configuration offset 0 開始。
36|MSI Message Control 區分支援的訊息數與實際啟用數。|裝置最多支援 8 個向量，主機仍可只啟用較少數量；讀 MMC 與 MME 時不要混為一個數字。
37|MSI Message Address 指定中斷訊息寫到的目的位址。|它不是 CQ buffer 位址；CQ 保存完成內容，MSI 位址用於送出通知，兩條資料流分開。
38|64-bit MSI 位址需要 Upper Address 補齊高部。|啟用 64-bit 位址格式時，把 MA 與 MUA 合併後才是完整目的位置；不能在所有格式都假設 MUA 有效。
39|MSI Message Data 是中斷訊息攜帶的資料值。|DATA 與 Message Address 一起描述通知；它不是 NVMe CQE 的 CID，不能直接用來配對完成命令。
40|MSI Mask Bits 可以遮罩相應訊息。|遮罩某個向量後，裝置仍可能產生待處理狀態；遮罩通知不等於讓 CQ 裡的完成項目消失。
41|MSI Pending Bits 記錄相應的待處理訊息狀態。|向量被遮罩期間有事件，pending 可反映待處理情況；主機仍需到 CQ 取得實際命令結果。
42|MSI-X 把向量表與 pending bitmap 放到指定記憶體區域。|先定位 Table 與 PBA，才能理解每個向量的設定及待處理狀態；兩者不一定位於同一個 BAR 區段。
43|MSI-X capability header 用於識別與串接能力清單。|找到 MSI-X 的 CID 後，再以 MSIXCAP 加上相對 offset 讀 MXC、MTAB，避免使用另一個 capability 的基底。
44|MSI-X 控制欄位區分啟用、整體遮罩與表格大小。|TS 原始值 7 表示 8 個 table entries；Function Mask 控制整體通知，不等於刪除向量表內容。
45|MSI-X Table 的 BIR 選 BAR，offset 選 BAR 內位置。|TBIR 指 BAR2、TO 指該 BAR 內的表格起點；不能把 TO 單獨當成主機實體位址。
46|PBA 有自己的 BAR 選擇與 offset。|Table 在 BAR0、PBA 在 BAR2 的配置需要分別定位；不能從 Table 地址加固定距離猜 PBA 在哪裡。
47|PCI Express capability 將裝置能力、控制與連線資訊分組。|先辨識這些欄位屬於 device 還是 link，再把能力值與目前狀態比較，避免把最大能力當實際連線結果。
48|PCIe capability header 提供識別與下一項能力位置。|由 capability list 找到此項後，再讀相對位置的 Device Control；不要把 capability 的 CID 當 NVMe 命令 CID。
49|PCIe Capabilities 欄位描述 port 類型、版本等能力資訊。|判斷裝置角色時讀 DPT；VER 是這個 capability 的版本，不是 NVMe Base Specification 版本。
50|Device Capabilities 描述 Function Level Reset 等硬體能力。|控制器要採用 FLR 前，先確認 FLRC；不能因 NVMe 支援重設，就假設每一種 PCIe 重設方式都可用。
51|Device Control 設定 payload、read request 大小與相關行為。|MPS 限制 PCIe payload 大小，與 NVMe CC.MPS 的記憶體頁大小不同；兩個 MPS 必須先看所在暫存器。
52|Device Status 回報 PCIe 交易相關狀態。|TP 表示交易仍有待處理情況時，不應把它當成 SQ 是否為空的直接判斷；兩個狀態來自不同層。
53|Link Capabilities 描述連線能支援的速度、寬度與省電能力。|支援 x4 不代表目前一定協商為 x4；實際結果到 Link Status 看，不能只讀能力表。
54|Link Control 設定連線層的控制選項。|改變 ASPM 相關設定時，影響的是 PCIe link 行為，不等於直接選擇 NVMe 的某個 power state。
55|Link Status 回報目前協商的連線速度與寬度。|能力支援 x4，但 NLW 回報 x2 時，報告實際連線應寫 x2，並將能力與現況分開呈現。
56|Device Capabilities 2 補充 LTR 等延伸能力。|主機希望使用 LTR 時先看 LTRS，再看控制欄位是否啟用；能力宣告不會自動替主機設定控制 bit。
57|Device Control 2 啟用相應延伸行為及 timeout 設定。|LTRME 與 LTRS 分別是啟用與支援資訊；前者不可脫離後者單獨解釋。
58|AER 把錯誤狀態、遮罩、嚴重度與記錄內容分開。|同一錯誤可以已發生但其回報被遮罩；不能只用遮罩值推論裝置從未出錯。
59|AER extended capability header 提供 ID、版本及下一項位置。|從 extended capability 串列定位 AER 後，再以 AERCAP 計算各狀態暫存器位置；它與一般 capability list 的基底規則不同。
60|Uncorrectable Error Status 記錄不可修正錯誤類型。|看到某個 status bit 後，連同 severity 與 header log 閱讀，不能只記一個「PCIe error」就省略類型。
61|Uncorrectable Error Mask 控制對應錯誤的回報遮罩。|把 mask 設定後不會修好已存在的傳輸問題；它改的是回報處理，不是錯誤原因。
62|Uncorrectable Error Severity 區分對應錯誤的嚴重度。|同一類錯誤是否視為 fatal，要看相應 severity 設定，而不是從 status bit 編號大小猜嚴重程度。
63|Correctable Error Status 記錄可修正錯誤事件。|錯誤已被底層修正，仍可能留下記錄；有 status 不代表某筆 NVMe 資料命令一定失敗。
64|Correctable Error Mask 控制可修正錯誤的回報。|主機調整回報頻率相關策略時要辨識 mask 語意；遮罩可修正錯誤不表示停止底層修正機制。
65|AER Capabilities and Control 描述記錄與檢查功能的能力及設定。|First Error Pointer 用來協助找最先記錄的錯誤；它不是完整事件時間戳，不能直接推算所有錯誤的精確時間差。
66|Header Log 保存出錯交易的標頭資訊。|要理解是哪種 PCIe 交易出問題，先按 HB 欄位重組 header；這裡不是 NVMe SQE 的另一份完整副本。
67|TLP Prefix Log 補充交易前綴資料。|若相關交易使用 prefix，將這份記錄與 Header Log 合讀；單靠前綴不能重建所有使用者資料內容。
68|Printable Eye 範例用字元排列呈現接收端眼圖。|先辨識水平與垂直方向，再看開口範圍；字元畫出的寬度是量測呈現，不能直接把字元數當吞吐量。
69|DEVICE_INTERFACE_REPORT 結構描述裝置介面的相應回報資訊。|閱讀介面報告時按欄位區分描述與範圍，不把它當成一般 NVMe namespace 的 Identify buffer。
70|PCIe 專屬 log 清單提供接收端眼圖量測的入口。|先由 LID 確定要讀 EOM log，再看它的參數及資料格式，不能拿 SMART log 的欄位解釋同樣大小的回覆。
71|EOM log 大小由 header 與實際描述子內容共同決定。|多一條 lane 或較多量測資料時，回覆長度可能增加；不要永遠用只容納一條 lane 的固定 buffer。
72|EOM 的 ACT 與 MQUAL 分別指定量測動作與品質要求。|要讀既有量測結果與要求開始新量測，是不同 ACT 情境；分段讀取時不要意外重啟量測。
73|EOM 的識別參數選擇此次量測相關的目標。|先選定控制器／實體介面相關 ID，再比較回覆；不同目標的眼圖不能只因 lane number 相同就直接合併。
74|EOM log 將整體 header 與各 lane 量測分開。|先讀整體資訊確認回覆範圍，再走各 lane descriptor；不能把第一條 lane 的狀態當成全部 lanes 都完成。
75|EOM Header 提供解讀整份量測結果所需的基本資訊。|主機先核對量測狀態與資料長度，再解析後續項目；取得一個有效 header 不等於每條 lane 都有有效結果。
76|Lane Descriptor 把 lane 編號、狀態與眼圖邊界放在一起。|LN＝2 的 TOP／BTM／LFT／RGT 應與 lane 2 的量測狀態一起看，不能沿用 lane 1 的成功狀態替它背書。
77|眼圖範例協助把數值邊界連回可視的開口形狀。|把 Lane Descriptor 的四個方向對到圖上，觀察哪個方向開口較小；不能把這張接收端量測圖直接當成 SSD IOPS 圖。
'''
LESSONS = {int(n):{'takeaway':takeaway,'example':example} for n,takeaway,example in (line.split('|') for line in DATA.strip().splitlines())}
