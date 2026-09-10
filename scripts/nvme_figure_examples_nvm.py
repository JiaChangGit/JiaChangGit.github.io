"""Figure-specific Chinese teaching, keyed by source Figure number.

Examples are explanatory scenarios, not additional normative requirements.
"""
DATA = '''
1|三份規格分別回答共通協定、傳輸方式與資料操作的問題。|要解釋一次 Read，先在 NVM 規格看讀取語意，到 Base 看 SQE 與資料指標，再到 PCIe Transport 看佇列與 doorbell 如何存取。
2|LBA 是資料區塊的編號，換成 byte 位置還需要區塊大小。|每個 logical block 有 4096 bytes 時，LBA 3 的資料起點是 3×4096＝12288 bytes；數字 3 本身不是 3 bytes。
3|融合的 Compare 與 Write 把比對結果當成是否更新的條件。|媒體原本為 A，主機要求「若仍為 A 就改成 B」；比對失敗時不能繼續寫 B，否則會覆蓋別人的更新。
4|原子性參數要先選控制器或 namespace 的值，再換算實際大小。|若適用的 AWUN 原始值為 7，大小是 8 個 blocks；若 namespace 欄位使用零值繼承規則，不能把該零直接當成 1 block。
5|正常運作下的重疊寫入結果取決於原子大小與讀寫範圍。|把一次寫入分成「原子保證內」與「跨出保證」兩種長度，再沿表中的讀取範圍比較可能看到的舊、新資料組合。
6|斷電結果表必須先有明確的寫入前資料與此次更新範圍。|假設某段原本都是 A，這次打算改為 B；先在圖上標出哪些 blocks 本來就是 A，哪些是這次命令要改的，才能讀下一張表。
7|斷電時的資料保證依寫入是否符合 power-fail 原子範圍而變化。|寫入中途斷電後，沿表中對應的寫入大小與完成情況讀結果；不能把「命令尚未完成」直接理解成全部更新都已保存。
8|寫入長度足夠小，仍可能因起點位置而跨越原子邊界。|教學例：邊界每 8 blocks 一次，LBA 7 起寫 2 blocks 會跨界；LBA 4 起寫 2 blocks 則不會。兩筆長度相同，位置不同。
9|Multiple 模式把較大寫入分成符合參數的原子子範圍。|一筆寫入跨越 3 個原子單位時，應逐個單位討論保證；不能把 3 個單位合稱為一次全有或全無的交易。
10|圖中的大命令 D 對應多個子範圍，方便比較兩種原子模式。|先把 A、B、C 各覆蓋的範圍畫在同一條 LBA 軸上，再看 D 如何一次涵蓋它們；比較的是提交方式與各段保證，不是命令名稱。
11|PRACT 決定 PI 的處理方式，PRCHK 決定要進行哪些檢查。|同樣 PRACT＝1，metadata 大小等於 PI 大小或大於 PI 大小時，傳輸的內容可能不同；要沿表中相應列追資料，而非只看 PRACT。
12|Storage Tag 是否存在，決定 STC 檢查要求是否有對象。|STS＝0 表示沒有 Storage Tag，因此設定 STC 也不會憑空產生一個要比對的 tag；改成非零 STS 後才有對應位元。
13|Admin 命令支援表要同時看命令列與控制器種類。|Get LBA Status 對 I/O controller 是選用功能，對 Administrative controller 則禁止；不能因為看到命令名稱就認為每種控制器都能執行。
14|I/O 命令清單區分必備操作與需要另查能力的操作。|Read、Write 是基本命令；打算使用 Copy 前，仍要確認控制器支援 Copy 及需要的格式。
15|Log 清單說明不同控制器可支援哪些紀錄。|要讀 LID 0Eh，先查這一列對目前控制器是否適用，再查裝置實際支援情況；LID 數字不是通用於所有情境的保證。
16|Feature 支援程度與設定作用範圍是兩個不同資訊。|即使 Performance Characteristics 對某類控制器可用，仍要確認是否允許以 namespace 作為設定對象。
17|Feature 更新是否記入事件紀錄，不等於 Feature 能不能使用。|LBA Range Type 的紀錄建議標成 NR，意思是此類更新不建議記入該紀錄，並非禁止使用這個 Feature。
18|LBA 超出可定址範圍與容量不足有不同回覆。|NSZE＝1000 時，存取 LBA 1000 已越界；在合法 LBA 範圍內分配更多資料卻超過容量，則是另一種問題。
19|命令專屬狀態要連同命令種類解釋。|Copy 回覆範圍重疊時，應檢查來源及目的範圍；不能拿 Read 的狀態表替它解釋同一個數值。
20|完整性錯誤可能是資料不符或區塊配置狀態，不一定是媒體損壞。|Compare Failure 表示資料與主機提供的預期內容不同；Deallocated or Unwritten Logical Block 則要連回該區塊狀態與 DULBE 設定。
21|FDP 回覆把放置識別碼連到可寫入資源及其剩餘量。|比較兩個回覆項目時，先確認 PID 指向哪個放置位置，再比較 RUAMW；數值較小代表剩餘可寫 blocks 較少，不是固定 RU 容量較小。
22|操作碼中的傳輸方向描述主機與控制器之間交換的資料。|Copy 雖然在裝置內搬移使用者資料，主機仍要傳入來源描述子，所以命令的傳輸方向不能只從「複製」二字推測。
23|Compare 的 MPTR 指向要一起比較的獨立 metadata。|若資料與 metadata 分開傳輸，預期使用者資料放在 DPTR 所指區域，預期 metadata 則放在 MPTR 所指區域。
24|Compare 的 DPTR 提供預期內容，供控制器與媒體資料比較。|主機把預期值 A 放進輸入 buffer；命令比較媒體是否也為 A，不會把這個 buffer 當成一般 Read 的輸出目的地。
25|Compare 的高位 tag 欄位要與 CDW14 合併才能形成完整預期值。|某種 PI 格式使用超過 32 bits 的 tag 空間時，只填 CDW14 會缺少高位；應先組出完整 tag，再按圖拆入各欄位。
26|Compare 的 SLBA 指定比較範圍起點。|比較從 LBA 16 開始的資料時，CDW10 放 16、CDW11 放 0；要比較幾個 blocks 由另一個欄位決定。
27|Compare 的長度與保護檢查選項放在同一個命令字中。|比較 4 blocks 時，NLB 填 3；同時核對 PRACT 必須為 0，不能以 Read 的 PI 傳輸設定直接照搬。
28|Compare 的 CDW13 在啟用命令擴充時承載擴充值。|CETYPE 非零時依對應擴充解釋 CEV；若 CETYPE＝0，不能把相同低位元當成有效擴充值。
29|Compare 的 CDW14 是預期 tag 空間的低 32 bits。|若 STS 分走部分位元，這 32 bits 就不全是 Reference Tag；先依格式分隔，再比較對應的預期值。
30|Compare 的 Application Tag mask 決定哪些位元參與比對。|預期 tag 為 12ABh、mask 為 FF00h 時，比對著重高 8 bits；低 8 bits 不會因 mask 為零而被要求等於零。
31|Compare 的設定錯誤與實際資料比對失敗需要分開理解。|PI 格式設定不成立時，尚未進入有效的資料比較；Compare Failure 則表示比較已發現內容不相同。
32|Copy 的 DPTR 指向來源範圍描述子。|要複製來源 LBA 100～103，buffer 中放的是來源起點、長度等描述，不必把這 4 blocks 的使用者資料先讀回主機。
33|Copy 命令本身的高位 tag 描述目的端資料保護。|來源端的預期 tag 從來源描述子取得，目的端要寫入的 tag 則由命令欄位提供；兩者可能不同。
34|Copy 的 SDLBA 是串接所有來源範圍後的目的起點。|來源兩段各有 2 blocks，目的從 LBA 1000 開始，第二段接在 LBA 1002，不會再從 1000 寫一次。
35|Copy 分別指定讀端與寫端 PI 行為，並選擇描述子格式。|來源需要檢查、目的需要重新產生 PI 時，分別看 PRINFOR 與 PRINFOW；NR＝1 表示有 2 個來源範圍。
36|Copy 的 CDW13 分別容納 Directive 資訊與命令擴充資訊。|使用 Directive 時讀高 16 bits 的 DSPEC；命令擴充是否使用低 16 bits 的 CEV，仍由 CETYPE 決定。
37|Copy 的 CDW14 補齊目的端 tag 的低位元。|目的起點改變時，要重新核對初始 Reference Tag；不能直接把第一個來源描述子的 tag 當成目的 tag。
38|Copy 的 LBAT 和 LBATM 描述目的端 Application Tag。|若只關心某些 tag 位元，先列出要保留或比對的位元，再依圖理解 mask；mask 與 tag 值不能互換。
39|Copy 描述子格式決定來源 namespace 與 PI 資訊如何表示。|需要指定另一個來源 namespace 時，先選支援 SNSID 的格式；不能只在不含該欄位的格式後面自行加上 NSID。
40|Format 0h 與 2h 的來源項目使用相應的較短 tag 表示。|填入一段來源時，先確定格式是否包含 SNSID，再設定 SLBA 與 NLB；相同 byte 位置須依選定格式閱讀。
41|Format 1h 與 3h 為較大的 tag 空間提供高、低欄位。|預期 tag 超過低 32 bits 時，將完整值拆入 ELBTU、ELBTL；省略高位就不再是原本的預期值。
42|多個來源範圍按描述子順序連續寫入目的範圍。|第一段長 3 blocks、第二段長 2 blocks，SDLBA＝20 時，兩段目的分別是 20～22 與 23～24。
43|Copy 失敗原因可以來自範圍、資源或快速複製條件。|來源與目的發生不允許的重疊，和要求 Fast Copy 卻無法滿足，是不同條件；先依狀態找要重新檢查的部分。
44|Dataset Management 傳入的是範圍清單，不是那些範圍內的資料。|要提示兩段資料的使用方式，只需傳入兩個描述子，無須把兩段使用者資料放入 DPTR buffer。
45|Dataset Management 的 NR 採從零起算的範圍數。|NR＝0 表示 1 個範圍，NR＝2 表示 3 個範圍；配置清單大小時先加 1，再乘描述子大小。
46|AD、IDW、IDR 表示主機對所列範圍提出的管理資訊。|主機不再需要某段資料時可提出 deallocate；這與只告知讀寫特性不同，不能把所有 bits 都解釋成「刪除」。
47|每個 Dataset Management 描述子都有自己的起點、長度與屬性。|兩段不連續的 LBA 範圍要用兩個項目表示；不能只把總長度相加，否則中間未指定的區域也會被涵蓋。
48|Context Attributes 描述預期的存取方式，供控制器參考。|循序讀取與隨機讀取可給不同提示；這些提示不會替主機建立命令完成順序。
49|Dataset Management 的錯誤表區分屬性衝突與命令大小限制。|一份清單可能每段都合法，卻因總數超過上限而不被接受；這與同一命令給出衝突屬性不同。
50|Read 的 MPTR 是獨立 metadata 的接收位置。|若讀回 2 blocks 且每個有 8 bytes metadata，metadata buffer 需要容納對應的 16 bytes；資料 buffer 另由 DPTR 指定。
51|Read 的 DPTR 指向主機接收使用者資料的空間。|讀取 2 個 4 KiB blocks，需要能接收 8192 bytes 的資料區；命令欄位中的 LBA 不等於這個主機記憶體位址。
52|Read 的高位預期 tag 要與低位欄位一起解釋。|讀取使用 80-bit tag 空間的格式時，不能只檢查 CDW14；CDW2、CDW3 也參與表示預期內容。
53|Read 的起始 LBA 跨越兩個 32-bit 命令字。|SLBA＝00000001_00000020h 時，CDW10＝20h、CDW11＝1h；把兩個字接反會讀到完全不同的位置。
54|Read 的 NLB 決定長度，其餘 bits 決定這次讀取的行為。|NLB＝7 代表 8 blocks；若每個為 4096 bytes，使用者資料共 32768 bytes，metadata 大小另依格式計算。
55|未使用命令擴充時，Read 的 CDW13 可以描述存取提示。|主機預期接著循序讀更多資料，可按支援規則提供提示；提示不是保證控制器一定預先讀取多少資料。
56|使用命令擴充時，Read 的低 16 bits 依 CEV 解釋。|從 CETYPE＝0 改成非零值後，不能沿用上一張表的低位元含義，必須切換到擴充定義。
57|Read 的 CDW14 提供低位預期 Storage／Reference Tag 空間。|STS＝0 的 16b Guard 格式下，這裡可對應完整 32-bit 預期 Reference Tag；STS 非零時須重新分隔。
58|Read 可以只檢查 Application Tag 中 mask 指定的部分。|mask＝FFFFh 表示所有 16 bits 都參與相應比較；mask＝0000h 則排除這些位元，不代表媒體 tag 必須全零。
59|Read 的命令專屬錯誤指出請求是否符合該命令要求。|讀取設定與 namespace 的 PI 格式不相容時，應先修正格式理解；不要把它與媒體上的 Guard Check Error 合成同一結果。
60|Verify 的高位 tag 提供媒體檢查的預期值。|Verify 雖不把資料讀回主機，仍可需要預期 tag；沒有輸出資料 buffer 並不表示不檢查資料保護。
61|Verify 用 SLBA 指定要檢查的起點。|要檢查 LBA 200～203，起點填 200，長度由 NLB 表達；不需要提供一份預期使用者資料作逐 byte 比較。
62|Verify 的長度與檢查選項決定此次驗證範圍。|NLB＝3 表示檢查 4 blocks，並按 Verify 的要求使用 PRACT＝0；不能把 Read 的 PI 處理方式原封不動搬過來。
63|Verify 的命令擴充欄位只在相應 CETYPE 下有意義。|同一個低 16-bit 數值放在不同 CETYPE 中，可能表示不同內容；報告時須把選擇器和值一起說明。
64|Verify 的 CDW14 是預期 tag 的低位部分。|若格式還用到 CDW2／3，讀者應先合併再拆分 Storage Tag 與 Reference Tag，避免只驗證了低位。
65|Verify 的 Application Tag mask 用來選擇檢查位元。|只檢查高位的 mask 與檢查全部位元會得到不同的通過條件；mask 是比較範圍，不是另一份資料。
66|Verify 的回覆要依驗證命令的狀態集合閱讀。|命令成功表示要求的驗證已完成，不能推論媒體內容與主機心中某份資料相同；若要比較已知內容，需使用 Compare。
67|Write 的 MPTR 提供要寫入的獨立 metadata。|主機的新使用者資料與對應 metadata 放在不同 buffer 時，要讓兩者指向相同順序的 logical blocks。
68|Write 的 DPTR 指向主機準備寫入的新資料。|要把 LBA 8～9 改成 B，主機 buffer 放 B，SLBA 放 8；資料內容與媒體位置分別由不同欄位提供。
69|Write 的高位 tag 是要建立的目的端保護資訊的一部分。|先依 PI 格式組出 Storage／Reference Tag，再拆到命令字；不能因為高位目前是零，就假設所有格式都不用這些欄位。
70|Write 的 SLBA 只表示媒體目的起點。|SLBA＝100、NLB＝1 表示更新 LBA 100 和 101；DPTR 另外指出新資料在主機記憶體的哪裡。
71|Write 的長度、FUA 與 PI 選項各自控制不同事項。|8-block Write 用 NLB＝7；設定 FUA 影響持久化要求，並不自動保證其他佇列中的命令先完成。
72|一般 Write 的 CDW13 把 Directive 資訊與資料集提示分開。|使用 Streams 等 Directive 時先辨識高位 DSPEC；低位 DSM 提示仍有自己的含義，不是同一個編號。
73|擴充 Write 的 CDW13 以 CEV 取代相應的一般低位解釋。|CETYPE 非零後，保留高位 Directive 資訊時仍須按擴充定義設定低位，不把 DSM 提示塞進 CEV。
74|Write 的 CDW14 提供初始 tag 的低位部分。|連續寫入多個 blocks 時，先確認第一個 block 的 tag 初值，再依所用保護類型理解後續值。
75|Write 的 Application Tag 與 mask 是不同的欄位。|LBAT 提供 tag 內容，LBATM 指定相應處理的位元範圍；不能把 FFFFh mask 當成要寫入 FFFFh tag。
76|Write 的命令專屬狀態協助區分配置不符與寫入目標限制。|嘗試寫入唯讀範圍時，重點是存取規則；它與 tag 配置不合法屬於不同原因。
77|Write Uncorrectable 指定之後應呈現不可修正狀態的 LBA 起點。|指定 LBA 40 起的範圍時，命令沒有要求主機提供一份損壞資料內容；它設定的是媒體對外呈現的行為。
78|Write Uncorrectable 的 NLB 決定標記多少 blocks。|NLB＝0 表示 1 block；不能把它理解成空操作而忽略對該 LBA 後續讀取的影響。
79|Write Uncorrectable 的 Directive 資訊只在指定用途下解釋。|若沒有啟用相應 Directive，就不能自行把 DSPEC 當成額外的 LBA 或長度；其適用性需回看 DTYPE。
80|唯讀範圍也限制 Write Uncorrectable。|即使這個命令不傳入使用者資料，它仍改變目標區塊的可讀行為，因此不能因「沒有資料 buffer」就忽略唯讀限制。
81|Write Zeroes 的高位 tag 仍需依目的格式設定。|使用資料保護的 namespace 中，寫零資料也有相應 tag；使用者資料全零不代表所有保護欄位也都填零。
82|Write Zeroes 的 SLBA 指定清零範圍起點。|從 LBA 64 開始清零 8 blocks，起點和長度分別設定；命令不需要主機傳入 8 blocks 的零資料 buffer。
83|Write Zeroes 的清零範圍、deallocate 與保護選項要一起閱讀。|要求讀回零，與要求繼續保留配置，是不同問題；要連同 DEAC 及相關支援條件判斷。
84|未啟用命令擴充的 Write Zeroes 使用一般 Directive 欄位。|設定 DSPEC 前先確認 DTYPE；不能把保留的低位元拿來表示額外清零長度。
85|啟用命令擴充後，Write Zeroes 的低位元改由 CEV 定義。|同一筆命令從一般模式改用擴充模式時，先更換對 CDW13 的解釋，再填參數。
86|Write Zeroes 的低位 tag 初值與全零資料內容是兩件事。|資料全部設為零時，Reference Tag 仍需符合目的位置與保護類型；不能以全零使用者資料推導 tag 必為零。
87|Write Zeroes 的 Application Tag 欄位描述保護資訊。|若系統使用特定 Application Tag 識別資料類別，清零資料後仍須按命令及格式規則處理這個 tag。
88|Write Zeroes 的完成資訊可回報實際清零的 LBA 數量。|使用允許部分處理的情境時，將 LBACZ 與要求範圍對照，不能只看成功狀態就假設整段都已處理。
89|Write Zeroes 的錯誤要連回清零、配置與保護設定。|相同 LBA 範圍可能因 PI 設定不同而不被接受；先依命令專屬狀態找條件，而非改成一般 Write 就認為語意等同。
90|非同步通知告知狀態已變，詳細內容還需讀對應資料。|收到 LBA Status Information 相關通知後，再讀相應 log；通知本身不包含所有受影響的 LBA 清單。
91|Format NVM 決定 PI 類型與 metadata 的傳輸安排。|兩個格式都使用 4 KiB 資料，仍可能因 PI 與 MSET 不同而需要不同的 I/O buffer 排列。
92|Feature 表把設定識別碼、作用範圍及保存特性放在一起比較。|對 namespace 的設定不應直接當成整個控制器設定；報告某項 Feature 時要說出改變的是哪個物件。
93|Set Features 的重疊範圍錯誤有其特定 Feature 上下文。|設定兩個不能互相重疊的 LBA ranges 時，即使各自起點和長度合法，合在一起仍可能衝突。
94|LBA Range Type 的 NUM 指示這次提供的項目數。|NUM 原始值為 1 時要按該欄位的從零起算規則準備 2 個項目，不是只配置 1 個描述子。
95|完成回覆中的 NUM 要在回覆語境中解釋。|把要求的 range 數與回覆欄位分開記錄，才能知道控制器實際回報多少項；兩個欄位名稱相同不代表傳輸方向相同。
96|LBA Range Type 項目把範圍與資料用途資訊放在一起。|同一 namespace 可有不同用途的兩段範圍，每段分別記錄 SLBA、NLB、Type 與屬性，而非替整個 namespace 只填一個 Type。
97|Error Recovery 把恢復時間限制與未配置區塊的讀取行為分開設定。|DULBE 影響讀取 deallocated blocks 時是否回報錯誤；TLER 則處理恢復時間，兩者不會互相取代。
98|Write Atomicity Normal 的 DN 會影響正常寫入原子性要求的使用。|比較 DN 設定前後時，仍要保留 power-fail 參數；正常運作的設定不能當成斷電保證的總開關。
99|事件設定 bits 決定主機希望收到哪些 NVM 通知。|只啟用 LBA Status Information 通知，不表示 Rate Limiting 變更通知也自動啟用；每種通知各看自己的 bit。
100|LBA Status Information 的屬性設定控制相關回報行為。|主機希望調整資訊產生或回報的節奏時，應分別理解 LSIPI 與 LSIRI，不把兩個 interval 當成同一計時器。
101|LBAFEE 告知主機使用擴充的 LBA Format 機制。|要存取超出傳統格式索引表示範圍的格式前，先確認並設定主機行為，不能只把較大索引塞入舊欄位。
102|Performance Characteristics 先選屬性，再解釋其值。|讀取標準延遲屬性與讀取廠商屬性時，ATTRI 指向的格式不同；不能拿同一個數字直接比較。
103|標準效能屬性提供規定情境下的特性值。|看到 4 KiB 平均讀取延遲時，要連同其定義的工作負載理解；它不是任何佇列深度下每筆 Read 的固定耗時。
104|屬性識別碼清單用來尋找裝置支援哪些效能描述。|先從清單找到可用 PAID，再讀該屬性的內容；不能因為支援查詢清單就推論每個廠商屬性都存在。
105|廠商效能屬性需要自己的識別碼及資料長度。|兩個屬性可能回傳不同長度；先看 ATTRL 再理解 payload，不能把上一個屬性的排列套到下一個。
106|Rate Limits 的 TGT 與 TID 共同指定限制施加在哪裡。|同樣 TID＝1，若 TGT 選的物件類型不同，就可能是完全不同的資源；必須成對記錄。
107|Rate Limiting buffer 分別設定頻寬、IOPS 與模式。|大量 4 KiB I/O 可能先碰到 IOPS 上限；大區塊 I/O 則可能先碰到頻寬上限，因此兩種限制都要看。
108|頻寬欄位的數值必須乘上對應 scale factor 才有實際單位。|同樣 raw 值 100，在不同 BWSF 下代表不同頻寬；比較兩個設定前先換成相同單位。
109|NVM Log 清單把 LID 與命令集及作用範圍連起來。|查某個 LID 時，同時確認 CSI 與目標 scope，避免把另一種命令集的同號紀錄當成這一份。
110|Error Information 中的 LBA 是發生問題的資料位置。|若回覆指向 LBA 32，先依該 namespace 的 block 大小換算位置；不能把 32 當成主機 buffer 的 byte offset。
111|Self-test 的 FLBA 只有在有效性標記成立時才是有效故障位置。|紀錄中即使保留一個非零 FLBA，若對應有效 bit 沒有設定，就不能據此指認那個 LBA 壞掉。
112|Namespace 變更事件可記錄格式與資料保護設定的變化。|原本不帶 PI 的 namespace 改成帶 PI 時，閱讀 FLBAS 與 DPS 的新值才能重新準備正確 buffer。
113|LBA Status Information 的 header 描述清單長度與 namespace 項目。|一份 log 含多個 namespace 時，先讀 NLSLNE 與總長度，再逐個走訪，不能把整個 buffer 都當成同一個範圍清單。
114|每個 namespace element 指出後面有多少範圍描述子。|NEID 指向某個 namespace、NLRD 指示後續項目數；換到下一個 namespace 前先消耗這一組的描述子。
115|LBA Range Descriptor 用起點與數量表示一段範圍。|把 RSLBA 與依定義解釋後的 RNLB 畫在 LBA 軸上，可以直接看出它與鄰近範圍是否相接。
116|Media Reallocated 事件先用有效標記決定是否能解讀 LBA。|事件回報重新配置數量，但 LBAV 未成立時，不能把後面的 LBA 欄位當成精確位置。
117|Rate Limiting Log 是有長度和連結位置的多層資料。|先讀 LPL 與 port 數，再沿 offset 找各層描述子；不要假設每種裝置都使用固定數量和固定順序。
118|Port Descriptor 描述單一 port 的限制與控制器關係。|雙 port 裝置中，Port 0 的可用頻寬不必等於 Port 1；先各自讀 PORTID 與限制，再追所連控制器。
119|Controller Descriptor 連到該控制器能使用的儲存媒體資源。|同一 port 下有兩個控制器時，分別沿各自 offset 找存取描述子，不把 port 的上限當成每個控制器各有一份。
120|媒體存取描述子用 SC 與 SI 指出限制所屬的物件。|此處 SC 是 Scope，並非 CQE 的 Status Code；先選定範圍類型，才能知道 SI＝1 指的是哪個實體。
121|Maximum Access Descriptor 說明資源的最大存取能力。|比較主機設定的限制值與資源最大值前，先把頻寬 scale 換成同一單位；設定值和硬體最大值來源不同。
122|Identify 的 CNS 選擇器決定回傳哪種資料結構。|CNS 相同時，NSID、CSI 等相依欄位仍要正確；不能只憑回傳長度推斷這是控制器還是 namespace 資料。
123|Identify Namespace 同時描述容量、格式與資料操作能力。|NSZE＝1000、NCAP＝800、NUSE＝600 分別表示可定址、最多可配置與目前已配置；換算 bytes 還要讀使用中的 LBA 格式。
124|對齊與粒度屬性分別描述起點位置和操作長度。|長度是粒度整數倍，但起點偏移 1 block 的寫入，仍可能不符合對齊建議；要分開比較兩個條件。
125|LBA Format 用 LBADS 與 MS 描述資料和 metadata 大小。|LBADS＝12 表示 2^12＝4096 bytes 資料；MS＝8 表示另有 8 bytes metadata，而不是資料大小變成 2^8。
126|控制器層的原子性欄位提供適用於相應 namespace 的基準。|AWUN 原始值 3 對應 4 blocks，但是否使用此值還要看 namespace 是否提供覆寫參數。
127|命令集專屬 Identify Namespace 補充 PI、格式與效能屬性。|基礎 Identify 已知每個 block 有 4 KiB，仍要到這裡看 ELBAF／PI 能力，才能完成 tag 的配置。
128|Extended LBA Format 描述保護格式及 Storage Tag 分配。|兩個格式即使 LBADS 相同，只要 PIF 或 STS 不同，就可能使用不同的 Guard 大小及 tag 位元配置。
129|命令集專屬控制器資料列出各種命令的能力與大小限制。|支援 Write Zeroes 不代表可以一次清零任意長度；仍須依 WZSL 等相應欄位計算上限。
130|版本描述子把主、次與修訂版本分開編碼。|讀到 MJR＝1、MNR＝3、TER＝0，應組成 1.3.0，而不是把三欄相加或當成容量值。
131|FIDX 為需要格式索引的 Identify 查詢指定目標格式。|要看索引 20 的格式，先使用支援該查詢的 CNS，再用 FIDX 指向 20；格式數量和格式索引不是同一欄。
132|Namespace Granularity List 說明有哪些配置粒度描述子。|先看模式與描述子數，再選符合情境的描述子；不能永遠只讀第一個 NSG／NCG。
133|NSG 與 NCG 分別提供 namespace 大小及容量的粒度提示。|若 NSG＝1 MiB、每個 block＝4 KiB，NSZE＝250 對應 1000 KiB，不是 1 MiB 的整數倍；這可能影響配置效率，但不能單憑未遵循提示就否決其他方面合法的 Create。
134|Create payload 把主機選擇的容量、格式與放置參數交給控制器。|建立 1000 個 4 KiB blocks 的 namespace，先選對格式，再填 NSZE／NCAP；1000 代表 blocks，不是 1000 bytes。
135|Get LBA Status 的 DPTR 是狀態描述子的接收 buffer。|主機想知道一段 LBA 的狀態，回來的是描述清單，不是該段的使用者資料。
136|Get LBA Status 的 SLBA 決定從哪裡開始查詢。|從 LBA 500 開始查詢，不代表回覆一定涵蓋後面全部 namespace；實際返回範圍還取決於命令限制與完成資訊。
137|MNDW 限制這次 Get LBA Status 能回傳多少資料。|接收 buffer 較小時，要把要求長度設在可容納範圍內，再依結果判斷是否需要繼續查詢。
138|ATYPE 與 RL 指定要執行的狀態查詢方式及範圍限制。|查詢方式改變後，控制器需要檢查或回報的內容可能不同；先說明想解決的問題，再選 ATYPE。
139|狀態清單 header 說明項目數以及查詢是否完整。|即使有成功回傳描述子，也應看 CMPC，確認是否已完成所需查詢，不能只以 buffer 非空判定完整。
140|每個狀態描述子將一段 LBA 範圍與其狀態連在一起。|一段可讀、一段有不同狀態時，兩段可分成不同項目；不能只用第一個 LBARS 代表整份回覆。
141|ANA 狀態對不同 NVM 命令有不同影響。|同一 namespace 的資料 I/O 與管理資訊讀取不一定同受限制；依命令列和目前 ANA 狀態交叉查表。
142|Log 先告訴主機哪些 namespace 範圍值得進一步查詢。|讀到一個 namespace 的兩段範圍後，把每段分別帶到 Get LBA Status；不要把 log 中的粗範圍當成最終逐段狀態。
143|第一個範圍的 Get LBA Status 回覆展示較細的狀態切分。|沿 Figure 142 的第一段範圍，逐個對照這張圖的 DSLBA 與 NLB，看控制器如何把同一查詢範圍分成多個項目。
144|第二個範圍的回覆要獨立閱讀完成資訊與描述子。|不能沿用前一次查詢的 NLSD 或 CMPC；每次回覆都有自己的項目數與完整性資訊。
145|NOIOB 邊界用來比較操作是否跨越最佳化邊界。|教學例：邊界每 8 blocks 一次，從 LBA 6 讀 4 blocks 會跨界，從 LBA 8 讀 4 blocks 則不跨界。
146|NABO 與 NABSN 一起決定原子邊界的位置。|若只知道邊界間距而忽略第一個偏移，畫出的所有邊界都可能錯位；先標起始偏移，再按間距往後標。
147|NPWA 與 NPWG 分別描述寫入起點及長度的偏好。|一筆長 8 blocks 的寫入可符合粒度，卻因從 LBA 1 開始而不符合對齊；兩個建議需要同時看。
148|NPRA 與 NPRG 對讀取提供相應的對齊與粒度資訊。|讀取長度從 4 blocks 增為 8 blocks，不一定解決起點未對齊的問題；要把兩個變因分開調整。
149|未符合建議的局部更新可能需要保留前後舊資料。|只更新一個較大單位中間的部分時，前綴與後綴仍要保持原值；圖用這些額外處理說明可能的寫入成本。
150|符合起點對齊與完整粒度的寫入可減少局部更新情境。|先對照寫入起點是否落在 NPWA 建議位置，再看長度是否涵蓋完整 NPWG 單位，兩者都成立才對應這張圖。
151|長度符合粒度，仍可能因起點偏移而影響多個單位。|把 Figure 150 的寫入整體向右移 1 block，長度沒有變，但頭尾可能都需要處理未更新的舊資料。
152|不同 Streams 可以由不同的寫入與配置粒度描述。|比較兩個 stream 時，把各自 SWS 和 SGS 標在其資料排列上，不能把其中一個 stream 的建議套給另一個。
153|Extended LBA 把每個 block 的資料與 metadata 相鄰傳輸。|2 個 4096-byte 資料 blocks、各帶 8-byte metadata，排列是資料0、metadata0、資料1、metadata1，共 8208 bytes。
154|Separate metadata 使用資料與 metadata 兩個對應 buffer。|相同的 2 blocks 改用分離方式後，資料 buffer 為 8192 bytes，metadata buffer 為 16 bytes；兩者的 block 順序必須一致。
155|STS＝0 的 16b Guard 格式保留完整 32-bit Reference Tag。|8-byte PI 分成 2-byte Guard、2-byte Application Tag、4-byte Reference Tag；此格式中沒有 Storage Tag 位元。
156|非零 STS 從 32-bit tag 空間中分出 Storage Tag。|若 STS＝8，Storage Tag 用 8 bits，剩餘 Reference Tag 為 24 bits；兩者總和仍是 32 bits。
157|32b Guard 格式提供較大的 Storage／Reference Tag 空間。|16-byte PI 中 Guard 4 bytes、Application Tag 2 bytes，餘下 10 bytes＝80 bits 供兩種 tag 分配。
158|CRC32C 測試向量用已知資料對照預期 Guard 計算結果。|4096 個零 bytes 的向量對應 98F94189h；這是固定輸入的核對值，不是任意 4 KiB 資料都應得到的結果。
159|64b Guard 格式的 tag 空間與 32b Guard 格式不同。|16-byte PI 中 Guard 佔 8 bytes、Application Tag 佔 2 bytes，剩下 6 bytes＝48 bits 作為 Storage／Reference Tag 空間。
160|CRC 多項式表定義計算所使用的數學規則。|兩個演算法即使都輸出 64 bits，只要多項式不同，就不能用同一組預期值驗證；先確認使用哪一個定義。
161|Rocksoft 參數完整指定 CRC64 的初始化、反射與最後處理。|只知道 Poly 還不夠；Init、RefIn、RefOut、XorOut 任一不同，同一串 bytes 也可能得到不同結果。
162|CRC 的輸入順序包含 byte 排列及每個 byte 的位元處理方向。|先按圖排列 logical block 與 metadata，再按反射規則处理；不能先把整段資料反轉，再假設等同逐 byte 位元反射。
163|CRC64 測試向量讓資料排列與計算參數可被實際核對。|4096 個零 bytes 對應 6482D367EB22B64Eh；改成全部 FFh 後，預期結果也會改變。
164|STS 決定連續 tag 空間中哪部分屬於 Storage Tag。|48-bit tag 空間、STS＝18 時，剩下 30 bits 是 Reference Tag；先做 48−18，再按圖找各部分。
165|不同 PI 格式允許的 tag 寬度有各自上、下限。|想配置 40-bit Reference Tag 時，先檢查所用 PI 格式是否提供足夠空間，不能僅因命令有多個字就認為一定放得下。
166|命令中的 tag 可能分散在 CDW2、CDW3 與 CDW14。|將完整 tag 當成一個整數後，再依圖切出高、中、低部分，可避免把資料結構中的連續位元誤認為命令內也連續。
167|同一套命令欄位在不同 PI 格式下有不同有效位元。|從 16b Guard 切換成 64b Guard 後，重新核對哪些位元有效；上一種格式被忽略的高位，在新格式中可能已有用途。
168|16b Guard Write 範例從初始 Reference Tag 建立寫入端保護。|STS＝0 時，先將初始 Reference Tag 放入 CDW14，再沿圖看第一個 block 的保護資訊如何產生。
169|16b Guard Read 範例用預期 Reference Tag 檢查讀出的資料。|把 Figure 168 寫入的同一範圍讀回時，主機提供對應預期值；這是檢查既有 PI，不是重新選一個寫入 tag。
170|32b Guard Write 範例展示 80-bit tag 如何分散到命令字。|Storage Tag 32 bits、Reference Tag 48 bits 加起來為 80 bits；逐段對照 CDW2、CDW3、CDW14，不能只保留低 32 bits。
171|32b Guard Read 範例以相同格式拆分預期 tag。|保持 Figure 170 的格式和 STS，再把讀取端預期 tag 放到相對應欄位，才能與媒體上的同一結構比較。
172|64b Guard Write 範例把 18-bit Storage Tag 與 30-bit Reference Tag 合併。|教學值 Storage＝12345h、Reference＝2Ah，合併為 12345h×2^30＋2Ah；低 32 bits 為 4000002Ah，高部為 48D1h。
173|64b Guard Read 範例需要保留跨命令字的預期 tag。|沿用上一例時，若只填低部 4000002Ah 而漏掉高部 48D1h，就不再表示同一個預期 Storage Tag。
174|Write 的 PI 流程依 PRACT 與 metadata 大小決定傳入或產生哪些資料。|metadata 剛好只有 PI，與另含其他 metadata 的情況要走不同分支；先標明主機實際傳了什麼，再追控制器處理。
175|Read 的 PI 流程決定哪些保護資訊會回到主機。|讀取前先比較 MS 與 PI 大小，再沿 PRACT 對應分支看 PI 是否移除；不能只從 Read 名稱推論回傳 buffer 排列。
176|Compare 同時涉及主機預期內容與媒體讀出內容。|主機提供 A、媒體為 B 時，即使兩邊各自 PI 都合法，資料比較仍可能失敗；完整性通過與內容相同是不同條件。
177|8-byte PI 的 Copy pass-through 讓保護資訊隨資料傳遞。|PRINFOR.PRACT＝0、PRINFOW.PRACT＝0 時沿圖追來源 PI 到目的端，不在中間自行插入重新產生步驟。
178|16-byte PI 的 Copy pass-through 保留較大的 PI 結構。|與 Figure 177 比較時，先將每個 block 的 PI 從 8 bytes 換成 16 bytes，再看資料與 PI 的對應，不能沿用 8-byte 欄位切法。
179|8-byte PI 的 Copy replace 分開處理來源檢查與目的 PI 產生。|讀端和寫端 PRACT 都為 1 時，沿圖看舊 PI 在哪裡移除、新 PI 在哪裡產生，而非把原 PI 原封不動複製。
180|16-byte PI 的 Copy replace 使用目的格式重新建立較大的 PI。|來源、目的都帶 16-byte PI 時，仍須用目的端 tag 設定產生新保護資訊；大小相同不表示內容也相同。
181|Copy insert 用在來源無 PI、目的需要 PI 的資料轉換。|來源只有使用者資料，目的每個 block 需要 8-byte PI；沿寫端流程看控制器如何補上目的保護資訊。
182|Copy strip 用在來源帶 PI、目的不保留 PI 的轉換。|來源的 8-byte PI 仍按規則參與讀端處理，但不成為目的使用者資料的一部分；移除 PI 不是少複製使用者資料。
183|參考配置狀態把控制器與 namespace 的設定分成不同部分。|閱讀本機記憶體介面範本時，先分開 RECCS 與 RENSCS，再看各自包含哪些設定；不要把整份範本當成單一 namespace 的資料。
184|範本中的 CAP 值是該參考配置的能力設定。|範本列出特定 MQES 時，它描述這個範本的佇列能力，不能推論所有實體 NVMe 裝置都具有相同值。
185|範本版本值說明參考配置使用的版本編碼。|先辨識 MJR、MNR、TER，再與實際裝置回報版本分開；範本中的版本不是裝置查詢結果。
186|範本 Firmware Slot 紀錄展示固定參考配置的韌體資訊。|用 AFI 找啟用 slot，再讀相應 FRS；這是示範欄位如何對應，不是建議把同一版本字串寫入所有裝置。
187|Feature 預設值屬於參考配置的初始狀態。|若後續改變中斷或佇列設定，不能仍把表中的預設值當成目前值；先分清 default 與 current。
188|範本 Identify 結構把容量、格式與識別資訊放到相应欄位。|建立一份參考 namespace 狀態時，同時核對 NSZE／NCAP、格式及識別碼，避免只改容量卻沿用不相符的其他欄位。
189|控制器配置狀態記錄佇列與命令能力等控制器層資訊。|NCQS、NSQS 與 MQES 分別涉及佇列數量及每個佇列的容量；三個數字不能互相代用。
190|Namespace 配置狀態記錄格式、原子性與識別資訊。|同一控制器下的兩個 namespace 可以有不同 LBA 格式或原子性參數，應分別保存各自的描述。
191|整體參考狀態由設定值與狀態資料共同組成。|只有一份 Identify 範本，仍不足以代表完整狀態；還要依圖中關係理解 Feature 值與各狀態結構的角色。
192|LBA Format List 把格式數量與每筆格式索引分開表示。|格式索引 20 不代表總共有 20 筆；先依 NLBAF／NULBAF 讀清單，再找到對應 Format Index。
193|不同 CNS 查詢會呈現不同範圍的格式清單項目。|使用 CNS 00h 與較新的格式查詢時，先查這張適用表，避免把第一種查詢的截取方式套給另一種。
194|LBA Migration Queue Entry 同時指出搬移來源、目的與完成相關資訊。|同一筆項目中，SLBA 是來源位置、DLBA 是目的位置；兩者都是 LBA，卻不能因單位相同就互換。
195|Port Graph 用連線表達 port、controller 與共享儲存資源。|兩個控制器連到同一 Endurance Group 時，圖中只有一份共享資源；不能把它的頻寬上限算成兩份相加。
196|Rate Limiting Log 範例把關係圖轉成帶 offset 的實際資料。|若描述子 offset 以 Dword 為單位，數值 16 對應 64 bytes；先換算再定位，不能直接跳到第 16 byte。
197|雙 port PCIe 裝置可以經不同入口共用同一儲存資源。|Port 0 和 Port 1 都在傳輸時，總吞吐量可能受共同 Endurance Group 限制；入口數增加不代表媒體能力倍增。
198|雙 port 的 log 範例展示兩條路徑如何引用共同描述子。|沿兩個 port 的 offset 走到底，若都指向同一存取描述子，就只計算一份共享限制，不複製成兩個獨立資源。
199|Reservation 對命令的限制取決於保留類型及主機身分。|同一 Read 或 Write，對 holder、已註冊但非 holder、未註冊主機可能有不同結果；先固定命令，再逐欄比較身分。
200|Sanitize 期間仍可執行哪些 Admin 命令，要按作業情境查表。|清除進行中想讀 Get Log Page，需看這張表及該 log 的條件；不能以「正在清除」推論所有管理命令都停止。
201|清除方法不同，清除後可觀察到的使用者資料值也不同。|Overwrite 的內容與 pattern 及輪數有關；Crypto Erase 不應被口頭簡化成「全部 bytes 寫零」。
202|Token Bucket 用代幣供給與消耗說明速率限制。|教學例：每秒補充 100 個代幣、每筆操作消耗 1 個，平均供給限制長期速率；桶內累積的代幣仍可能容許短時間突發。這是說明性模型。
'''

LESSONS = {int(n):{'takeaway':takeaway,'example':example} for n,takeaway,example in (line.split('|') for line in DATA.strip().splitlines())}
