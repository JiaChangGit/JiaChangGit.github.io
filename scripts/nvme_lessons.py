"""Authored explanations and topic-specific reading instructions.

The two Chinese passages develop each lesson for independent study. The paired
reading instruction belongs to the figure-reading section in all three editions.
No fallback generates a lesson by repeating field names or source assertions.
"""

LESSONS = {}


def add(key, zh_headers, en_headers, first, second, reading_zh, reading_en):
    LESSONS[key] = dict(headers={'zh': zh_headers.split('|'), 'en': en_headers.split('|')},
                        teaching=[first, second], reading={'zh': reading_zh, 'en': reading_en})


add('nvmcs-foundation', '要讀的資訊|如何解讀|還需要哪一項資訊', 'Information|Interpretation|Additional information needed',
    '作業系統可以要求讀取檔案中的一段資料，但控制器收到的 NVM 命令是針對 namespace 裡的區塊。LBA 用來選區塊；區塊內有多少資料，則由目前採用的格式決定。因此，同樣是讀 8 個區塊，採用 512-byte 與 4096-byte 資料格式時，需要的主機緩衝區大小不同。先把「位置」與「每個位置容納多少資料」分清楚，後面才能看懂命令範圍。',
    'LBADS 儲存的是以 2 為底的指數。例如 0Ch 是十六進位的 12，所以資料大小為 2^12 = 4096 bytes。MS 再告訴我們每個區塊附帶多少 metadata。Format Index 則只是格式清單中的選項編號；它既不是資料大小，也不是緩衝區中的位移。這三種數字可能都很小，計算方式卻完全不同。',
    '規格關係圖先回答由哪份規格定義行為，區塊圖再回答資料如何編址。讀格式表時先找到 Format Index 對應的項目，再分別解讀 LBADS 和 MS。不要把表格中的選項編號直接當作 byte 數。',
    'The specification relationship diagram identifies which document defines a behavior; the block diagram explains addressing. In a format table, first select the entry using Format Index, then interpret LBADS and MS separately. An entry index is not a byte count.')

add('nvmcs-capacity', '容量或操作|描述的範圍或變化|判斷時須注意什麼', 'Capacity or operation|Range or change described|What affects the interpretation',
    'Namespace 的可定址範圍、最多可配置的容量、目前已配置的容量，是三個不同問題。NSZE 決定主機可以使用哪些 LBA；NCAP 描述可配置給資料的區塊數；NUSE 描述已配置的區塊數。它們都以區塊計數，因此換算為 bytes 時還需要所用的區塊格式。',
    '以支援精簡配置的 namespace 為例，NSZE=1000、NCAP=800、NUSE=600。LBA 900 雖然落在 0 到 999 的有效位址範圍內，仍不能只憑位址有效就推論一定能再配置空間。反過來，NUSE=600 也不表示只有 LBA 0 到 599 有資料：已配置的區塊可以分散在整個位址範圍。',
    '容量示意圖的長條比較的是數量，不表示資料一定集中在前端。先用 NSZE 判斷位址是否在範圍內，再以 NCAP、NUSE 理解配置量，最後確認 THINP 所描述的支援能力。',
    'The capacity bars compare quantities, not a contiguous placement of data at the beginning. Use NSZE for the address range, NCAP and NUSE for allocation quantities, and THINP to establish thin-provisioning support.')

add('nvmcs-identify', '查詢選擇值|可以取得的資訊|如何連到其他查詢', 'Query selector|Information returned|Connection to other queries',
    'Identify 並不是一張包含所有答案的大表。主機要先說明想查控制器、某個 namespace，還是某個格式的能力；CNS 等選擇欄位決定回傳哪種結構。讀回來的資料即使都是 4096-byte 緩衝區，也不能互相套用欄位位置，因為每種查詢的結構定義不同。',
    '查目前正在使用的格式，與查尚未選用格式的能力，是兩條不同的閱讀路徑。前者從 namespace 現況找到格式編號，再連到該編號的格式項目；後者直接指定想了解的格式，並結合共同能力。這可以解釋為什麼「控制器支援這個格式」不等於「namespace 現在就使用這個格式」。',
    '先按查詢對象分組閱讀 CNS 表，再連接同一 namespace 的基本與延伸結構。FLBAS 是目前選擇，LBAF／ELBAF 是選項內容，能力位則說明允許哪些選擇；三者不能互相代替。',
    'Group CNS entries by the queried object, then connect the basic and extended structures for that namespace. FLBAS gives the current selection, LBAF/ELBAF describe the options, and capability bits state which choices are supported.')

add('nvmcs-format-list', '格式資料|記錄哪些屬性|如何選取或解讀', 'Format information|Attributes recorded|Selection and interpretation',
    '格式可以看成一組共同生效的屬性：資料大小、metadata 大小、資料保護格式及相關能力。兩個格式的資料部分即使同為 4096 bytes，其他屬性仍可能不同。比較格式時如果只看容量，就會漏掉主機緩衝區配置或保護資訊處理方式的差異。',
    'LBAF 與 ELBAF 是相同格式編號的兩部分說明，應配對閱讀。格式的「數量」與「最後一個編號」也不同：NLBAF 採從 0 起算的數量編碼，必須先加 1 得到共同格式數，才能再接上唯一屬性格式。把編碼值直接當數量，會少算一個選項。',
    '沿同一個 Format Index 配對 LBAF、ELBAF，再看 FLBAS 選中哪一項。讀數量圖時，把欄位原始值、解碼後數量及最後一個 index 分開列出；例如 6 個選項的 index 是 0 到 5。',
    'Pair LBAF and ELBAF at the same Format Index, then locate the selection in FLBAS. Distinguish the encoded count, decoded number of entries, and final index: six options have indices zero through five.')

add('nvmcs-format', '設定欄位|選擇哪種行為|使用前須確認什麼', 'Setting|Behavior selected|Required information before use',
    'Format NVM 選擇的是 namespace 的資料格式與相關處理方式。主機不能任意拼出一組欄位，再假設控制器一定接受；選擇必須落在已回報的格式與能力之內。使用延伸格式時，還要確認主機已透過 Host Behavior Support 宣告可以理解對應格式。',
    '資料保護類型、Guard 寬度與 metadata 傳輸方式，分別由不同欄位決定。PI=1 選的是保護類型，不會單獨把 Guard 改成 64 bits。MSET 則決定資料與 metadata 一起傳輸或分開傳輸。把每個選擇放回它所控制的問題，才知道最後需要什麼緩衝區與檢查方式。',
    '把 Format 的命令欄位與 Identify 的能力欄位成對閱讀：先找允許的格式，再看命令選擇。LBAFEE／ELBAS 處理延伸格式支援，PI 處理保護類型，MSET 處理傳輸配置。',
    'Read Format command selections alongside Identify capabilities: establish the allowed format before selecting it. LBAFEE/ELBAS concern extended-format support, PI selects protection type, and MSET selects the transfer arrangement.')

add('nvmcs-namespace-create', '建立資料或結果|數值描述什麼|必須檢查的規則', 'Creation data or result|Meaning|Rules to check',
    '建立 namespace 時，主機同時描述需要多大的空間，以及這個空間採用什麼格式。NSZE、NCAP 是區塊數，配置粒度卻以 bytes 表示；兩者比較前，要先乘上所選格式的區塊大小。格式、保護資訊與遮罩也必須彼此相容，不能只檢查容量。',
    '配置粒度是一項減少空間浪費的建議，與命令欄位是否合法是不同問題。若容量不是建議粒度的整數倍，控制器實際配置的空間可能包含主機無法定址的部分；只要其他要求都符合，就不能單憑這一點拒絕建立。建立成功後，仍需要 Attachment 才能讓指定控制器存取該 namespace。',
    '建立資料表先讀容量與格式，再讀保護欄位及遮罩；granularity 表另外用來計算配置是否有效率。先確認 GDM 如何把描述子對應到格式，再解讀 ND 的數量編碼。',
    'Read capacity and format in the creation structure before protection fields and masks. The granularity list separately describes efficient allocation. Establish how GDM associates descriptors with formats before decoding the ND count.')

add('nvmcs-metadata', '傳輸配置或位置|主機如何準備緩衝區|格式對它的限制', 'Transfer arrangement or location|Host buffer arrangement|Format constraints',
    '每個區塊的 metadata 必須與該區塊的資料對應。一起傳輸時，緩衝區按「資料 0、metadata 0、資料 1、metadata 1」排列；分開傳輸時，資料放在一個區域，metadata 放在另一個區域。分開只改變傳輸配置，不表示 metadata 可以與另一批區塊配對。',
    '先用 PRACT=0 的例子理解長度：8 個區塊、每個區塊 4096 bytes 資料及 16 bytes metadata，資料合計 32768 bytes，metadata 合計 128 bytes。一起傳輸需要 32896 bytes；分開傳輸則分別準備這兩個長度。後續若要求控制器產生或移除保護資訊，才再依 PRACT 與格式調整傳輸量。',
    '傳輸圖的上下兩種排列描述同一批區塊。逐一對照 Data 0 與 MD 0、Data 1 與 MD 1，再追蹤 DPTR、MPTR 指向哪個緩衝區。PI 位於 metadata 中的位置，與 metadata 是否分開傳輸是兩個不同維度。',
    'The two transfer arrangements represent the same blocks. Match Data 0 with MD 0 and Data 1 with MD 1, then follow DPTR and MPTR to their buffers. PI placement within metadata is separate from whether metadata is transferred in its own buffer.')

add('nvmcs-support-status', '命令或識別值|用途或支援要求|解讀時的上下文', 'Command or identifier|Purpose or support requirement|Interpretation context',
    '主機要使用命令，先要確認控制器類型能處理它，以及相關選用能力是否存在。Opcode 說明要求執行什麼操作；NSID 指出操作對象；完成狀態則說明這次操作的結果。這些資訊相互關聯，卻不能用其中一個值推論另外兩個。',
    '狀態碼也需要上下文。相同 SC 數值搭配不同 SCT，可能代表不同原因；因此讀完成項目時，要同時辨認狀態類別及狀態碼。Copy 的資料方向則是另一個例子：主機傳入的是來源描述子，不是把來源的所有資料讀回來再寫一次。',
    'Opcode 表用來辨認操作及支援要求；狀態表要先選 SCT 再查 SC。FID、LID 與 opcode 屬於不同識別空間，即使數字相同，也不能拿其中一张表解釋另一種命令。',
    'Use opcode tables to identify operations and support requirements. For status tables, select SCT before looking up SC. FIDs, LIDs, and opcodes occupy different identifier spaces, so equal numbers do not imply equal meanings.')

add('nvmcs-read-write', '命令欄位|描述的資料或操作|哪些選擇會改變解讀', 'Command field|Data or operation described|Selections affecting interpretation',
    '一筆 Read 或 Write 要描述起始區塊、區塊數、資料位置與處理選項。SLBA 是第一個區塊，NLB 採從 0 起算的數量編碼，所以 NLB=7 表示 8 個區塊。結束 LBA 是 SLBA+8−1；這裡的減 1 是因為第一個區塊已經算在 8 個之內。',
    '完成命令與資料已具備某種持久化保證，需要依命令選項判斷。主機也必須安排有相依關係的操作；如果想讀取剛寫入的版本，就不能僅因兩筆命令先後放進佇列而假設順序已被保證。FUA 所改變的行為，仍要放在這個命令相依關係下理解。',
    '先把 CDW10、CDW11 組成 SLBA，再把 NLB 換成實際區塊數，算出完整 LBA 範圍及 buffer 長度。最後依 CETYPE、PRACT 等選擇解讀其他欄位，避免把另一種格式的同一 bit 位置照搬過來。',
    'Combine CDW10 and CDW11 into SLBA, decode NLB, and calculate the full LBA range and buffer length. Then interpret the remaining fields under selections such as CETYPE and PRACT, rather than copying meanings from another layout.')

add('nvmcs-order-fused', '操作方式或限制|保證的內容|成立所需的條件', 'Operation or limit|Guarantee|Conditions for that guarantee',
    '考慮「目前資料仍是 A，才更新成 B」的需求。若先送 Compare，收到成功後才送獨立的 Write，另一個寫入者可能在兩筆命令之間修改資料。Compare 的成功只描述當時的比較結果，不會替後面的獨立 Write 保留那個條件。',
    '融合的 Compare-and-Write 把比較與更新連成有條件的原子操作。主機仍需遵守融合命令的提交方式、相同範圍，以及回報的大小和邊界限制。原子性在這裡描述這個操作的不可分割性，不等於任意長度的多筆命令都變成一個交易。',
    '命令順序圖要分開觀察提交、執行與完成。閱讀 fused pair 的格式時，把兩筆命令的範圍並列，再檢查 ACWU／NACWU 及邊界；不要只看到 FUSE 設定就推論大小一定符合。',
    'Distinguish submission, execution, and completion in ordering diagrams. For a fused pair, compare the two ranges and check ACWU/NACWU and boundaries. Setting FUSE alone does not establish that the size is supported.')

add('nvmcs-atomic', '原子性欄位或模式|規定什麼範圍|不能由此推論什麼', 'Atomicity field or mode|Range governed|What it does not establish',
    '原子性描述更新是否可能被觀察到只完成一部分。正常運作與突然斷電是不同情境，所以規格分別回報 normal 與 power-fail 的保證。這不是效能排名，也不是單一命令只要小於某個數量就一定符合；起始位置和是否跨過指定邊界同樣重要。',
    '假設解碼後的邊界大小是 8 個區塊，從 LBA 4 寫 12 個區塊會跨越 LBA 8 的邊界。在允許多段原子性的模式下，可以分成 4–7 與 8–15 兩段理解；每段有保證，並不表示兩段必須同時成功或同時失敗。這個區分能避免把儲存裝置的保證誤當成資料庫交易。',
    '大小表先解碼 AWUN／AWUPF，再依 namespace 欄位及模式選取適用值。邊界圖從 NABO 開始標出每個分界，將實際寫入範圍畫在同一條 LBA 軸上，才能看出是否跨界。',
    'Decode AWUN/AWUPF and select the values applicable to the namespace and mode. On a boundary diagram, mark boundaries from NABO and place the actual write on the same LBA axis to determine which boundaries it crosses.')

add('nvmcs-compare-verify', '命令或大小欄位|實際檢查什麼|結果的解釋範圍', 'Command or size field|What is checked|Meaning of the result',
    'Compare 回答「儲存內容是否等於主機提供的預期內容」，因此主機需要提供比較資料。Verify 回答的是所指定資料的完整性檢查是否通過，不需要把預期資料交給控制器，也不把資料傳回主機。兩者的成功代表不同事情。',
    '例如主機想知道一段空間是否全為 0，可以提供全零資料進行 Compare。單靠 Verify 成功無法得到相同結論，因為一段內容不是全零的資料，也可以通過完整性檢查。讀大小限制時還要注意 variant：同一欄位可能表示建議大小，也可能是不能超過的上限。',
    '比較命令圖時，先找有沒有主機資料 buffer，再找控制器使用什麼作為比較或檢查依據。大小表必須連同 VSL 與 NVMVFYS 閱讀，才知道數值是建議還是上限。',
    'First identify whether a host data buffer is present and what the controller uses as the comparison or checking basis. Read VSL together with NVMVFYS to distinguish a recommended size from a hard limit.')

add('nvmcs-copy', '描述子或行為|資料如何安排|限制及完成結果', 'Descriptor or behavior|Data arrangement|Limits and completion meaning',
    'Copy 讓主機以描述子列出來源範圍，再指定目的起點。控制器負責在儲存空間內複製資料，主機傳輸的是範圍說明。多個來源可以不連續，但目的資料依來源描述子的順序連續排列；目的位置不是每個描述子各自再指定一次。',
    '假設兩段來源各有 4 個區塊，目的從 LBA 100 開始，兩段會對應到 100–103 與 104–107。若操作部分失敗，完成資訊能告訴主機哪些進度已被回報，但不能因此假設後續目的位置一定完全沒有改動。重疊、快速複製要求與原子性都需依使用的描述子格式另外判斷。',
    '先解碼 NR 得到來源描述子數，再逐段解碼 NLB，把長度累加到 SDLBA。對照 MSRC、MSSRL、MCL 時，分清楚它們限制的是來源數、單段長度或總長度；完成 DW0 另讀其回報語意。',
    'Decode NR and each source NLB, then accumulate source lengths from SDLBA. Distinguish source-count, per-source-length, and total-length limits when checking MSRC, MSSRL, and MCL. Interpret completion DW0 under its own progress-reporting rules.')

add('nvmcs-copy-pi', '來源與目的保護格式|如何處理保護資訊|允許這種處理的條件', 'Source and destination PI|PI treatment|Conditions permitting it',
    '複製資料時，來源與目的的保護資訊不一定能逐 byte 原樣搬移。兩端格式相同時，可以依命令選項保留或重新產生；一端有 PI、另一端沒有時，則需要規格允許的插入或移除方式。這些選擇還涉及讀取端與寫入端各自的 PRACT。',
    '特別要分清楚 metadata 是否全部都是 PI。如果 16 bytes metadata 中只有 8 bytes 是 PI，其餘 8 bytes 還有其他用途；移除 PI 不代表可以連其他 metadata 一起丟棄。因此，兩端的資料大小相同，並不足以證明能使用有 PI 與無 PI 之間的轉換特例。',
    '把轉換表當成來源格式與目的格式的交叉比較：先確定兩端是否有 PI，再選讀端／寫端 PRACT 的組合，最後核對 metadata 是否只包含 PI。表中的 0/0、1/1 必須分別對應到兩端。',
    'Read the conversion table as a source/destination comparison: determine PI presence, select the read/write PRACT pair, then check whether metadata contains only PI. Values such as 0/0 and 1/1 refer to the two separate ends.')

add('nvmcs-dsm', '屬性或限制組合|控制器需要如何處理|可否由成功推論已釋放空間', 'Attribute or limit combination|Controller processing|Implications for space release',
    'Dataset Management 讓主機描述一組 LBA 範圍及其使用特性，例如資料不再需要。它與直接搬移資料的 Read、Write 不同，很多資訊具有提示性質。因此必須分開看主機傳入了什麼、控制器必須處理到什麼程度，以及配置狀態最後可能如何改變。',
    '三個限制分別涉及範圍數量、單一範圍大小及總大小。variant 又決定超出限制時的處理方式：不能只讀其中一個上限，就推論整筆命令必須失敗或所有區塊都已被釋放。計算部分可處理的範圍時，也要把第二段只處理一部分的情況算進去。',
    '先讀屬性位，再把每個 range 的長度列出並累加。限制表必須同時看三個 limits 是否為零，以及 variant 的值；完成狀態不能取代對實際配置語意的解讀。',
    'Read the attribute bits, list each range length, and accumulate the total. Interpret the three limits together with their zero/nonzero state and the variant value. Command completion alone does not establish the resulting allocation state.')

add('nvmcs-dealloc', '能力或讀取設定|如何影響讀取結果|判斷時需同時讀什麼', 'Capability or read setting|Effect on reads|Information to read together',
    '區塊被解除配置，描述的是空間配置狀態；它並不直接回答下一次 Read 應回傳哪些 bytes。讀取行為還要看裝置回報的規則，以及主機是否啟用對 deallocated 或 unwritten 區塊的錯誤回報。能力存在與功能已啟用，也要分開確認。',
    '因此，讀到全零可能來自未寫入或解除配置後的回傳規則，不能單憑這次結果推論資料曾被安全清除。若讀取回報錯誤，也可能是主機啟用 DULBE 後所要求的行為。理解錯誤時，要把命令、區塊狀態與設定放在一起。',
    '先查 DAE 是否支援，再查 DULBE 是否啟用。未走錯誤回報分支時，依 DRB 讀取資料回傳規則；若格式有 PI，再用 GDS 等欄位解讀 Guard 與 tags，不能只比較資料區。',
    'Check DAE support and DULBE enablement first. When error reporting does not apply, use DRB for returned data. For formats with PI, interpret Guard and tags using fields such as GDS rather than inspecting only the data area.')

add('nvmcs-zero-uncorrectable', '命令或回傳欄位|改變或回報什麼|確認結果所需的條件', 'Command or result field|Change or result reported|Conditions needed to establish the outcome',
    'Write Uncorrectable 用來標記指定區塊，使後續讀取依規格回報無法修正的資料；Write Zeroes 則要求將指定範圍表現為零值。這兩個命令處理的結果不同，不能只因它們都沒有一般 Write 的資料 buffer，就視為同一種操作。',
    'Write Zeroes 的命令成功，還需要結合命令模式及回傳欄位判斷影響範圍。當主機要求整個 namespace 清零時，LBACZ 是確認整體結果的重要資訊。若回報只代表指定 range，就不能把命令成功延伸成整個 namespace 都已清零。',
    '先依 opcode 分開閱讀兩種命令，再看 Write Zeroes 的 NSZ、DEAC 與保護選項。最後對照 CQE 的 LBACZ；圖上的命令要求和完成回報分別描述「想做什麼」與「確認做到什麼」。',
    'Separate the commands by opcode, then examine NSZ, DEAC, and protection options for Write Zeroes. Finally read LBACZ in the completion. The command request and result describe the requested operation and the established outcome, respectively.')

add('nvmcs-pi-formats', 'Guard 格式|PI 中的空間分配|Storage Tag 大小或遮罩限制', 'Guard format|Space within PI|Storage Tag size or mask constraints',
    'PI 不只有 CRC。它包含 Guard、Application Tag，以及配置給 Storage Tag、Reference Tag 的空間。Guard 寬度選定後，PI 的整體格式也跟著確定；STS 再決定其中多少 bits 分給 Storage Tag，剩餘部分才交給 Reference Tag。',
    '以 64-bit Guard 為例，扣除 Guard 與 Application Tag 後，有 48 bits 可分給兩種 tags。若 STS=18，Storage Tag 使用 18 bits，Reference Tag 使用 30 bits。增加 STS 是重新分配同一塊空間，不會把 PI 自動變大。Qualified PI 還會引入另外的格式及遮罩限制。',
    '格式圖先看 PI 總長度，再分辨固定欄位與由 STS 決定的分界。把 Storage Tag bits 與 Reference Tag bits 相加，應回到該格式的 tag 空間大小；遮罩表則另外說明哪些 bits 參與比較。',
    'Start with total PI length, then separate fixed fields from the boundary selected by STS. Storage Tag and Reference Tag widths must add up to the format’s tag space. Mask tables separately determine which bits participate in comparisons.')

add('nvmcs-crc', 'CRC 或計算範圍|定義或已知結果|比對前須確認什麼', 'CRC or coverage|Definition or known result|What to establish before comparison',
    'CRC 的結果由輸入資料與整套計算參數共同決定。除了多項式，還有初始值、位元反射方式與最後的 XOR。兩個程式即使都宣稱計算 CRC-64，如果採用不同參數，也不應期待得到相同結果。資料進入計算的順序和計算結果的儲存方式也要分開理解。',
    '已知向量可以提供一個有明確輸入和輸出的對照。例如長度同為 4 KiB 的全零資料與全 FFh 資料，因為內容不同，Guard 也不同。比較向量時，必須同時保留輸入長度、輸入內容及輸出表示方式；只列一串十六進位數字，讀者無法知道它如何得到。',
    'CRC 圖表分成計算參數、涵蓋資料及已知向量三部分閱讀。Guard 涵蓋資料及 PI 前的 metadata，不包含 PI 本身。位元圖用來確認輸出如何排列，不用圖上的左右位置猜測整數端序。',
    'Read CRC material as three parts: parameters, covered bytes, and known vectors. Guard covers data and metadata before PI, excluding PI itself. Use the bit layout to establish output placement rather than inferring integer byte order from left/right positions.')

add('nvmcs-tag-layout', '保護格式與 STS|Storage／Reference Tag 放在哪裡|欄位寬度如何分配', 'Protection format and STS|Storage/Reference Tag placement|Width allocation',
    'Tag 在概念上是一個數值，但命令格式可能把它分散在幾個 Dword。閱讀時先確定 Guard 格式與 STS，再決定每段 bits 屬於哪一種 tag。不能把 CDW14 永遠當成完整的 Reference Tag，因為某些格式會把它的高位分給 Storage Tag。',
    '64-bit Guard、STS=18 的例子中，Storage Tag 的高 16 bits 放進 CDW3 的低 16 bits，剩餘 2 bits 放在 CDW14 的高位；Reference Tag 使用 CDW14 其餘 30 bits。先拆分再組合，可以清楚看到哪些 bits 會改變，而不用把十六進位值當成必須記憶的常數。',
    '以選定格式的圖為準，沿每個 tag 的高位到低位追蹤跨 Dword 的部分。用 Storage Tag=12345h 的低 2 bits 和高 16 bits 驗算配置，再把 Reference Tag 放入剩餘 30 bits。',
    'Follow each tag from high to low bits across Dwords in the selected format. Split Storage Tag 12345h into its low two and high sixteen bits to verify placement, then place the Reference Tag in the remaining thirty bits.')

add('nvmcs-pi-checking', '操作或保護條件|控制器如何處理 PI|對檢查或傳輸量的影響', 'Operation or protection condition|Controller PI handling|Effect on checking or transfer size',
    'PRACT 描述控制器如何處理 PI，PRCHK、STC 等欄位則描述要求哪些檢查。這兩組選擇解決不同問題：資料中要不要由控制器產生或移除 PI，不等於哪些 tags 一定會被比較。讀命令時還要分清楚方向，Read 與 Write 對相同 PRACT 的處理不同。',
    'Metadata 大小也會改變結果。Read PRACT=1 時，如果 metadata 只有 PI，可以移除 PI 後只回傳資料；如果 metadata 還有其他內容，就需依該分支回傳。這正是為什麼主機不能只看 PRACT 決定 buffer 長度，還必須讀出 MS 和 PI 格式。',
    '處理流程先按 Read／Write 分支，再檢查 PRACT、MS 與 PI 大小，最後判斷要求的檢查及停用檢查的特殊值。Mask=0 的位不參與比較；不要把遮罩數值當作期待的 tag 值。',
    'Branch first by Read/Write, then by PRACT and the relationship between MS and PI size. Apply requested checks and check-disabling sentinel rules afterward. A zero mask bit excludes a comparison bit; the mask is not the expected tag value.')

add('nvmcs-basic-features', 'Feature 或欄位|設定的行為與單位|作用範圍或例外', 'Feature or field|Behavior and unit|Scope or exception',
    'Feature 會改變控制器或 namespace 的某項行為，但每個 Feature 的資料格式、作用對象與保存方式都可能不同。設定前先確認是在改整個控制器還是某個 namespace，再看值放在命令欄位或另傳資料結構。相同 Get／Set Features 命令不表示資料結構可以共用。',
    'TLER 是從錯誤復原開始計時的限制。TLER=5 對應 500 ms，並不是從主機提交命令那刻開始的整體期限。LBA Range Type 的用途提示也是類似的區分：告訴軟體一段空間的用途，不會因此提供權限隔離或保證資料不被覆寫。',
    'Feature 總表先看 FID、作用對象及是否需要 buffer，再閱讀各 FID 的欄位。時間欄位要連同單位和計時起點解讀；描述子數量則先確認是否採從 0 起算的編碼。',
    'In Feature tables, identify FID, scope, and buffer requirements before reading individual layouts. Interpret time fields with both units and timing origin; decode descriptor counts according to their zero-based or direct-count definitions.')

add('nvmcs-log-events', '事件或計數|記錄及啟用方式|哪些解讀容易混淆', 'Event or counter|Recording or enablement|Distinctions to preserve',
    '事件通知是提醒主機有事需要查看，log 則提供可以閱讀的內容。事件設定、事件回報與取得 log 是不同步驟，不能因讀到某種 log 就假設相關通知已啟用。NVM Command Set 另外補充某些計數應納入哪些命令，以及欄位如何解讀。',
    '計數的名字相似，也可能採不同統計口徑。例如 Verify 沒有把資料傳回主機，仍可能納入指定的讀取資料量計數。錯誤位置同樣如此：Self-test 的 FLBA 可指出其中一個失敗區塊，不能套用另一個 log 對「最低失敗 LBA」的定義。',
    '通知表先對照事件種類與啟用位，再連到對應 log。讀計數表時分開列出納入的命令及單位換算；讀錯誤位置時先檢查有效旗標，並保留該 log 對位置的定義。',
    'Connect event types and enable bits to their logs. For counters, distinguish included commands from unit conversions. For error locations, check validity first and retain the location semantics defined by that particular log.')

add('nvmcs-lba-status', '查詢或回報欄位|數值代表什麼|讀取時的判斷', 'Query or result field|Meaning|Reading decision',
    'LBA Status 讓主機了解特定範圍或已記錄的 LBA 狀況。主機要求的查詢範圍、控制器實際掃描到哪裡，以及這次 buffer 裡放得下多少描述子，是三個不同限制。因此，取得一批結果不一定代表整個查詢已完成。',
    '可變長度的結果與分段讀取還需要版本一致性。如果讀到一半資料更新，前後兩段可能不再屬於同一份記錄。讀取流程因此需要結合 generation、保留事件的設定與最後的確認，而不是單純從 offset 0 一直增加到結尾。',
    '查詢圖先解讀 SLBA、RL 與 MNDW，再用 NLSD 決定有效描述子數，用 CMPC 判斷完成原因。讀 log 時沿 LSGC、RAE 的流程追蹤同一版本，避免把沒有完整掃描當成沒有需處理的 LBA。',
    'Decode SLBA, RL, and MNDW for the query. Use NLSD for valid descriptors and CMPC for the completion reason. Follow LSGC and RAE when reading the log so an incomplete scan is not mistaken for an absence of reportable LBAs.')

add('nvmcs-sanitize', '清除狀態或讀取方式|控制器回報什麼|允許的檢查與結果', 'Sanitize state or read mode|Controller report|Permitted checks and results',
    'Sanitize 的啟動命令可以先完成，清除作業仍在背景執行。主機需要另外讀取狀態與進度，才能知道作業是否成功結束。一般 Read 的資料保護規則，也不能直接套用到清除後的 Media Verification 狀態。',
    'Media Verification 的目的是讓主機觀察清除後的媒體資料，因此指定 Read 的允許檢查與回傳狀態有特別規定。理解這一段時，要先確定控制器所處狀態，再解讀命令結果。只看到「成功」或看到全零資料，都不能跳過狀態與操作範圍的判斷。',
    '把 Sanitize 命令、LID 81h 狀態，以及 Media Verification Read 的欄位分開閱讀。先確認作業階段，再套用該階段允許的命令與 PI 檢查規則；狀態圖中的轉移不是一般 Read 自動觸發的保證。',
    'Separate the Sanitize command, LID 81h status, and Media Verification Read fields. Establish the operation phase before applying its permitted commands and PI checking rules; state transitions cannot be inferred from an ordinary Read alone.')

add('nvmcs-alignment', '效能提示欄位|建議的長度或起點|何時解讀這組欄位', 'Performance hint|Recommended length or start|When the fields apply',
    '對齊描述起點是否落在指定邊界上；粒度描述長度是否以指定單位成組。兩筆寫入可以同樣長，卻因起點不同而跨過不同數量的內部處理單位。所以只把 I/O 長度調成建議大小，未必同時符合起點對齊要求。',
    '例如建議單位是 8 個區塊，LBA 8–15 正好涵蓋一個單位，LBA 9–16 則橫跨兩個單位。後者仍是 8 個區塊，但控制器可能需要處理兩端的其他資料。這些欄位提供效能建議；原子性與 Key Per I/O 的必要對齊要求，仍要各自判斷。',
    '在同一条 LBA 軸上畫出建議邊界及操作範圍，分別檢查起點與長度。欄位表先讀 OPTPERF／OPTRPERF，確認哪組欄位有效，再依各欄位定義處理加 1 或直接值。',
    'Place recommended boundaries and the operation range on one LBA axis, checking start and length separately. Read OPTPERF/OPTRPERF before choosing the valid fields, then use each field’s own direct-value or plus-one encoding.')

add('nvmcs-performance-feature', '效能屬性欄位|回報或設定的內容|解讀所需的尺度或識別', 'Performance attribute|Reported or configured information|Scale or identity needed',
    'Performance Characteristics 用來描述或選擇效能相關屬性。標準欄位可能用區間編碼表示效能，而不是直接填入時間。廠商屬性則需要識別碼決定資料如何解讀，不能因為它放在標準結構內，就假設每個 byte 都有標準定義。',
    '例如 R4KARL=0Eh 不是 14 μs，而是代表指定測試條件下的一個平均延遲區間。比較兩個裝置前，要先確認採用相同屬性及測試條件。保存屬性的槽位數量與識別碼也不同；有剩餘空位不代表已用索引一定連續。',
    '先用屬性種類選擇格式，再按 R4KARL 對照延遲區間表。廠商資料先讀 PAID，再以 ATTRL 限定有效長度；清單的總容量、剩餘容量與實際項目需要分開閱讀。',
    'Select the layout by attribute type, then map R4KARL through the latency-interval table. For vendor data, identify PAID and bound valid data with ATTRL. Separate list capacity, remaining capacity, and actual entries.')

add('nvmcs-rate-config', '限制設定欄位|指定的對象或數值|如何換成實際限制', 'Rate setting|Target or value specified|Conversion to an actual limit',
    'Rate Limiting 先要選定限制誰，再設定限制多少。控制器識別值只有在相對應的目標種類下才具有該意義，因此 TGT 和 TID 必須一起讀。設定內容又分成總頻寬、寫入頻寬、總 IOPS 與寫入 IOPS，不能把四個值混成單一速度。',
    '頻寬值需要乘上 BWSF 選定的尺度。例如尺度為每單位 10 MiB/s，數值 50 才代表 500 MiB/s。寫入對總額度的消耗還可能經過比例加權，所以「傳了 4 KiB」與「扣了 4 KiB 的總頻寬額度」不一定相同。',
    '設定結構先讀 TGT／TID 與 RLE／RLM，再配對 BWSF 和各頻寬值。把寫入與總量分開列出，最後解讀 WRBWR、WRIOPSR 的分子與分母，避免只看一個 byte。',
    'Read TGT/TID and RLE/RLM before pairing BWSF with bandwidth values. Separate write-only limits from total limits, then interpret both numerator and denominator bytes in WRBWR and WRIOPSR.')

add('nvmcs-rate-modes', '模式或命令|如何分享或消耗額度|理解這個結果的限制', 'Mode or command|Sharing or consumption of credits|Limits on interpretation',
    '速率限制可以用累積與扣除額度理解：時間經過時額度補充，操作執行時消耗額度。Read 和 Write 會消耗的額度種類不同；Write 既要檢查總量，也要檢查寫入專用的限制。只剩其中一種額度，並不代表這次 Write 一定能執行。',
    'Hard 與 Soft 的差別還涉及閒置資源如何分享。設定的數值是限制及分享規則的一部分，不是保證任何工作負載都能達到該速度。計算時先把一筆 I/O 的四種消耗列出，再討論模式如何分配資源，會比只畫一個桶更容易看出限制。',
    '算例按 total bandwidth、write bandwidth、total IOPS、write IOPS 四欄閱讀。4 KiB Write 搭配頻寬權重 2、IOPS 權重 3，消耗依序為 8 KiB、4 KiB、3、1；Read 不消耗寫入專用額度。',
    'Read the example across total bandwidth, write bandwidth, total IOPS, and write IOPS. A 4 KiB Write with bandwidth weight two and IOPS weight three consumes 8 KiB, 4 KiB, three, and one respectively. Reads do not consume write-only credits.')

add('nvmcs-rate-graph', '能力圖欄位|描述哪種關係或尺度|讀取時須避免的誤解', 'Capability-graph field|Relationship or scale|Interpretation to avoid',
    'Rate Limiting log 描述的不是一張把所有速度相加就能得到總量的表。多個控制器或連接埠可能共用同一組媒體資源；因此資料結構需要表示「誰連到哪個資源」，讓主機知道哪些能力其實來自同一個來源。',
    '例如兩個控制器都能使用同一個 Endurance Group。若其中一個已占用該組媒體的頻寬，另一個不會因為走不同連接埠就憑空多出相同頻寬。閱讀描述子時，重複指向同一個資源的關係應保留，不能把每次引用都當成獨立資源。',
    '先以 LPL 確定長度，再把 Dword offsets 乘 4 找到描述子。依 SC 解讀 SI 所辨認的物件，沿父子引用建立資源關係；同一資源被多次引用時，不重複累加其能力。',
    'Establish length from LPL and multiply Dword offsets by four to locate descriptors. Interpret SI under SC and follow parent/child references. Multiple references to the same resource must not multiply its capability.')

add('nvmcs-fdp', 'FDP 欄位或記錄|描述的配置與活動|數值的有效性或限制', 'FDP field or record|Placement or activity described|Validity or limit',
    'FDP 讓主機參與資料放置的選擇，目的是把不同使用特性的資料安排到適合的回收單位。主機使用 handle 表達選擇，並不是直接指定 NAND 的實體位址。理解 FDP 時，要把 namespace 使用的格式、handle 與底層回收資源的關係連起來。',
    '回報的剩餘可寫量與估計時間，可以協助觀察資源狀況，但它們有各自的單位及未回報值。共享同一個 RUH 的 namespace 還必須符合格式條件；資料大小同為 4 KiB，不足以證明兩種 Format Index 可以互換。',
    '先辨認 namespace 的 handle 如何對應 RUH，再閱讀狀態與統計。EARUTR 是秒數估計，RUAMW 是區塊數；事件中的 LBA 只有在 LBAV 指示有效時才可使用。',
    'Identify the namespace-handle-to-RUH relationship before reading status and statistics. EARUTR is an estimated time in seconds and RUAMW is a block count. An event LBA is usable only when LBAV marks it valid.')

add('nvmcs-streams', 'Streams 提示|換算出的操作單位|與其他提示的關係', 'Streams hint|Resulting operation unit|Relationship to other hints',
    'Streams 讓主機以資料流的方式表達資料關係。規格回報的 SWS 與 SGS 幫助主機選擇寫入及解除配置的大小，但兩個數值描述的層次不同。SWS 先以區塊表示建議寫入單位，SGS 再表示一個 stream granularity 包含多少個這樣的單位。',
    '若 SWS=8、SGS=4，寫入單位是 8 個區塊，較大的粒度單位則是 32 個區塊。一次 8-block Write 符合前者，不代表同長度的解除配置也涵蓋完整粒度。使用 Streams 時，相關提示與一般 namespace 提示的優先關係也要一起考慮。',
    '先標示 SWS 的區塊單位，再計算 SGS×SWS。把寫入大小與解除配置範圍放到這兩個尺度下比較，不要把 SGS 直接當成區塊數。',
    'Establish SWS in blocks, then calculate SGS times SWS. Compare writes and deallocation ranges against their respective scales; SGS alone is not a block count.')

add('nvmcs-ana-reservations', '路徑狀態或保留類型|對讀寫或回報的影響|還需確認的身分與對象', 'Path state or reservation type|Effect on I/O or reporting|Identity and target to check',
    '可以透過某個控制器看到 namespace，不代表每一種命令都能使用。ANA 描述路徑與存取狀態，Reservations 則依保留類型及主機身分決定哪些存取會衝突。這是兩組不同條件，必須各自成立，不能用其中一組通過代替另一組。',
    '例如路徑可用時，非保留持有者的 Write 仍可能衝突，而 Read 是否允許取決於保留類型。Copy 甚至同時涉及多個來源的讀取權限與目的的寫入權限。閱讀權限矩陣時，要先把命令分成讀取類或寫入類，再核對主機身分。',
    'ANA 表用來判斷路徑狀態及某些回報欄位的特殊值；Reservation 矩陣則以保留類型、holder／registrant 身分與命令類別交叉查讀。NUSE 回零的狀態例外，不代表媒體內容已清空。',
    'Use ANA tables for path state and state-specific field values. Read reservation matrices by reservation type, holder/registrant identity, and command category. A state-specific zero NUSE does not establish that media data was erased.')

add('nvmcs-key-per-io', '能力或對齊欄位|描述的支援與設定|操作必須符合什麼', 'Capability or alignment field|Support or setting described|Operation requirement',
    'Key Per I/O 的相關欄位同時涉及能力、啟用狀態與資料存取的對齊要求。支援某個功能只是第一步，使用時還要確認 namespace 的設定和這筆 I/O 的範圍都符合要求。這些必要條件與一般效能提示的強度不同。',
    'KPIODAAG 採從 0 起算的粒度編碼，因此原始值 7 表示 8 個區塊。起點 16、長度 8 都落在這個單位上；起點改為 17 或長度改為 7，就不符合。檢查長度時應使用實際區塊數，而不是直接拿命令中尚未加 1 的 NLB 比較。',
    '先依 KPIOCAP 及 namespace 支援／啟用欄位確認可用性，再解碼 KPIODAAG。對齊圖同時標出起始 LBA 和結束位置，以實際長度檢查整數倍。',
    'Establish availability from KPIOCAP and namespace support/enable fields, then decode KPIODAAG. Mark the starting LBA and end on the alignment diagram and check multiples using the actual block count.')

add('nvmcs-migration-queue', '追蹤欄位或事件|描述的範圍及狀態|讀取記錄時的限制', 'Tracking field or event|Range or state described|Limits when reading records',
    '變更追蹤記錄的是哪些 LBA 範圍發生需要追蹤的變化，不是原始命令的逐筆副本。多個相鄰寫入可以合併成一段記錄，因此不能用 queue entry 數量反推寫入命令數。讀取一筆 entry 前，也必須先判斷它是否包含有效的 range。',
    '佇列還會記錄開始、停止、暫停與已滿等狀態。佇列已滿時，後续變更不一定還能記錄；只看見先前完整的 entries，不能推論後面沒有變更。追蹤命令完成與記錄中的狀態標記，也需要依規格定義分開理解先後关系。',
    '先用 LBACIR 決定這筆記錄是範圍、整個 namespace 或沒有 range，再看 ESA 狀態。CDQP 用來識別新 entry，DLBA 描述解除配置相關資訊；不能只讀 LBA 欄位就忽略有效性與狀態。',
    'Use LBACIR to distinguish a range, the whole namespace, or no range, then read ESA. CDQP identifies new entries and DLBA conveys deallocation-related information. Range values alone do not establish validity or logging state.')

add('nvmcs-export-template', '範本項目|規定的對外值或相容條件|與底層資源的關係', 'Template item|Advertised value or compatibility rule|Relationship to underlying resources',
    '資源匯出範本描述控制器應向外呈現哪些能力和資料，並限制這些值與底層資源的關係。對外回報可以受範本約束，不能任意超過實際可提供的資源。這裡討論的是已納入範圍的 memory-based 資料結構及規則。',
    '範本中的版本欄位有自己的指定值，不會因閱讀的規格 PDF 版本較新就自動變更。佇列數也要依欄位編碼解碼後比較：原始 NCQS=7 代表 8 個，NCQS=3 代表 4 個。Namespace 的格式相容性則還要看資料、metadata 及相關設定，不能只比較名稱。',
    '先區分範本固定值與受底層上限限制的值，再逐項比對版本、佇列數與 namespace 格式。對外 Format Index 可以重新對應，但對應後的格式仍須符合範本指定的相容條件。',
    'Separate fixed template values from values bounded by underlying resources, then compare versions, queue counts, and namespace formats. Advertised Format Index values may be remapped, but the mapped formats must meet the template’s compatibility requirements.')

add('nvmcs-export-state', '狀態欄位|保存或描述什麼|長度及一致性如何判斷', 'State field|Saved or described information|Length and consistency interpretation',
    '配置資料描述資源被安排成什麼樣子，執行中狀態則記錄當下使用哪些設定。兩者可能都有 Feature 名稱，但一個描述範本或配置，另一個描述目前值。恢復或解讀狀態時，如果把預設值當成目前值，就會失去原本的執行設定。',
    '可變長度結構先有固定 64-byte header，再接 NVMECSS 指定的內容；NVMECSS 的單位是 Dword。因此值為 16 時，後段是 64 bytes，整體為 128 bytes。長度正確還不等於狀態一定一致，CSATTR.CP 另外回報處理期間的暫停條件。',
    '布局圖先把固定 header 與可變內容分開，使用 64+4×NVMECSS 計算總長度。內層版本決定內容格式，CSATTR.CP 決定可以推論的暫停條件；這三種資訊各回答不同問題。',
    'Separate the fixed header and variable contents, calculating total bytes as 64+4×NVMECSS. The nested version selects the content format, while CSATTR.CP describes the suspension condition. Length, version, and consistency are separate questions.')

add('boot-read', '讀取路徑或欄位|從哪裡取得資料或狀態|操作環境與單位', 'Read path or field|Where data or status is obtained|Operating context and unit',
    'Boot Partition 提供開機映像的儲存空間。開機早期可能還沒有建立一般 Admin 命令所需的環境，因此規格提供由 properties 控制的讀取路徑。當 Admin 命令環境已可使用，也可以透過 Get Log Page 取得 Boot Partition 資料。兩條路徑的啟動方式和完成狀態不同。',
    '讀取哪個 partition，與哪個 partition 被選為 active，是不同選擇。主機可以讀 BP1 來了解其映像，而不改變 active partition。計算 log 長度時，BPSZ 先乘 128 KiB 得到 Boot data 長度，再加上 16-byte header；同樣大小的 data 不表示整個傳輸緩衝區也只有那麼大。',
    'Properties 路徑依序連接 CAP.BPS、BPINFO、BPRSEL、BPMBL：支援能力、狀態、讀取選擇、主機緩衝區。LID 15h 則分開讀 header 與 data，並以 Admin CQE 解讀這筆命令的結果。',
    'For the property path, connect CAP.BPS, BPINFO, BPRSEL, and BPMBL as support, status, read selection, and host buffer. For LID 15h, distinguish header from data and use the Admin CQE for the command result.')

add('boot-protection', '保護機制與狀態|哪種操作能改變狀態|重設或斷電後的結果', 'Protection mechanism and state|Operations changing it|Result of reset or power cycling',
    '更新開機映像同時涉及內容更新及寫入保護。Download 傳送資料，Commit 選擇保存與啟用行為，保護設定則決定哪些修改被允許。把這些動作畫在同一條時間線上，才能看出「已下載」「已寫入 partition」「已被選為 active」不是同一個時刻。',
    'FID 85h 與 RPMB 控制的保護機制，具有不同的解鎖方式及狀態保留規則。主機不能把其中一套的重設行為套到另一套。RPMB 訊息還包含驗證和計數相關欄位，用來確認要求是否符合該機制；這些欄位不是一般 Boot data 的一部分。',
    '保護狀態表先選定 FID 85h 或 RPMB 控制，再沿「目前狀態→允許的操作→重設／斷電後狀態」閱讀。RPMB frame 與訊息流程應配對看，分清要求、回應、計數器和驗證資料各自的位置。',
    'Choose FID 85h or RPMB control before following current state, allowed operation, and state after reset or power cycling. Read RPMB frames alongside message flows to distinguish requests, responses, counters, and authentication data.')

add('telemetry-layout', '資料區域|包含哪些 blocks|Last Block 數值的限制', 'Data area|Included blocks|Last Block constraints',
    'Telemetry 把裝置收集的狀態資料放在可讀取的 log 中。Block 0 是 header，後面的資料以 512-byte block 編號。每個 Data Area 的 Last Block 是最後一個編號，不是額外增加的長度；因此 Area 2、Area 3 的範圍包含前面較小 Area 的內容。',
    '如果 Area 1 到 block 65、Area 2 到 block 1000，Area 2 的資料量是 1000×512 bytes，不是 (65+1000)×512。要連 header 一起讀，再加 512 bytes。兩個 Area 的 Last Block 相同，表示後一個 Area 沒有增加範圍，而不是兩份不同位置的等長資料。',
    '把 header 放在 block 0，再讓各 Area 的長條都從 block 1 開始。比較終點而不累加長條；計算新增部分時才使用兩個 Last Block 的差。Area 4 的存在還需查對應支援能力。',
    'Place the header at block zero and start every data-area bar at block one. Compare endpoints rather than summing bars; subtract Last Block values only when calculating the added portion. Check support separately for Area 4.')

add('telemetry-capture', '快照控制欄位|執行或回報的動作|分段讀取時須注意什麼', 'Snapshot-control field|Action or report|Consideration during chunked reads',
    '一份 Telemetry 資料可能比單次傳輸大，需要分成多段讀取。主機真正需要的是同一份快照的各段資料，而不是不同時間各取一段再拼在一起。因此要先區分建立新快照與讀取既有快照，並用 generation 等欄位確認資料版本。',
    '例如讀第一段時 generation 是 2Ah，最後再讀 header 已變成 2Bh，就不能把前後資料當成同一次收集。RAE 可以保留事件，但不代表其他讀取者不存在，也不等於替這份資料上鎖。Host-Initiated 與 Controller-Initiated 兩條流程的確認條件，需要各自閱讀。',
    '先選 07h 或 08h 流程，再區分建立、讀取和確認事件的步驟。07h 後續分段不再重複觸發建立；08h 同時檢查 generation 和資料可用狀態，不能只靠 generation 相等就忽略其他主機的確認操作。',
    'Select the 07h or 08h flow, then separate creation, reading, and event acknowledgement. Subsequent 07h chunks must not repeatedly trigger creation. For 08h, check generation and data-availability state; equal generations do not eliminate acknowledgement races with other hosts.')

add('sanitize-scope', '清除對象或方法|包含或排除哪些資料|可據此確認的範圍', 'Target or method|Included or excluded data|Scope of the resulting conclusion',
    '開始清除前，首先要回答「要清除哪個範圍」。Namespace 和 NVM subsystem 是不同層級：對各 namespace 逐一完成清除，不能單凭這些結果證明所有 subsystem 層級的使用者資料都已處理。控制器記憶體與其他可能含使用者資料的位置，也有各自規則。',
    'Sanitize 同時存在明確的排除對象，例如 Boot Partition 與 RPMB。成功完成清除不會替主機更新或清空開機映像。Crypto Erase 則要處理讓舊資料可解密的金鑰及相關資料；閱讀時不能只把它理解成變更一個目前使用的金鑰欄位。',
    '範圍圖先分 subsystem、namespace 及明確排除區域，再把清除方法放到正確對象上。GDE 等整體狀態的判斷必須使用其定義的範圍，不能由較小範圍的成功結果直接推論。',
    'Separate subsystem, namespace, and explicitly excluded regions before applying a sanitize method. Interpret aggregate status such as GDE at its defined scope rather than inferring it from successful smaller-scope operations.')

add('sanitize-command', '命令與能力組合|控制器如何處理|完成或拒絕的原因', 'Command and capability combination|Controller handling|Reason for acceptance or rejection',
    'Sanitize 命令的欄位不是彼此獨立的開關。SANACT 選擇操作，其他位元則提出解除配置、失敗後存取或媒體驗證等要求；控制器是否允許某個組合，還取決於它回報的能力。判斷命令是否合法時，要把一組條件一起看。',
    '例如 NDAS 描述主機對成功清除後解除配置的要求，NDI 和 NODRM 則參與判斷這個要求如何處理。把這些值逐列並排，才能看出為何只改一個能力或設定，結果就不同。Overwrite 次數也有特殊編碼，OWPASS=0h 代表 16 次，不能按一般整數理解成不執行。',
    '先讀 Sanitize 支援方法，再依 SANACT 選分支。條件表一次固定其他欄位，只改 NDAS、NDI 或 NODRM 中一項，觀察結果；EMVS 的支援與方法限制另行核對。',
    'Establish supported sanitize methods and branch by SANACT. In the combination table, hold other fields fixed while changing NDAS, NDI, or NODRM to see why the result changes. Check EMVS support and method restrictions separately.')

add('sanitize-state', '作業階段|可以採取的後續動作|進度與歷史如何回報', 'Operation phase|Allowed subsequent action|Progress and history reporting',
    'Sanitize 不是一個只有「開始／結束」的動作。作業可能經過處理、媒體驗證及驗證後解除配置，也可能進入不同失敗狀態。命令完成表示啟動要求得到處理，背景作業狀態則回答清除目前走到哪一個階段。',
    '進度欄位描述的是目前被量測的階段，不能一律當成整個作業只會遞增的百分比。某個階段完成後，下一階段可能從 0 重新計算。失敗後回到 Idle 也不會自動把失敗歷史改寫成成功；應分別閱讀當前狀態與上次結果。',
    '沿狀態圖辨認每個轉移所要求的動作，再將 SOS、SPROG 和失敗階段配對閱讀。Restricted 與 Unrestricted Failure 的可用出口不同；Media Verification 時的滿進度值也不能單獨證明整個 operation 已結束。',
    'Read each state transition with its triggering action, then interpret SOS, SPROG, and failure phase together. Restricted and Unrestricted Failure have different exits. Full progress during Media Verification alone does not establish completion of the entire operation.')

add('sanitize-read', '驗證讀取條件|回傳內容或狀態|這個結果能說明什麼', 'Verification-read condition|Returned content or status|What the result establishes',
    '媒體驗證期間的 Read 用來觀察清除後的內容，因此不能沿用一般資料完整性讀取的全部假設。主機要求 PI 檢查會走到不同結果；對仍已配置的媒體，也要分成資料能讀出與不能讀出兩種情況。',
    '若讀取的是已解除配置的 LBA，控制器可能依 deallocated／unwritten 規則回傳資料。這種回傳值無法直接證明原本媒體上的資料模式。因此驗證結果必須連同 LBA 配置狀態、控制器目前作業階段和命令檢查選項解釋。',
    '先檢查是否處於 Media Verification，再依 PI 檢查要求及 allocated／deallocated 分支閱讀結果表。表中的特定成功狀態與一般 Successful Completion 要分辨，且不能用解除配置後的回傳值代替實體媒體觀察。',
    'Establish Media Verification state, then branch by requested PI checks and allocated/deallocated status. Distinguish the specific verification success status from ordinary Successful Completion, and do not treat deallocated return values as direct observation of physical media.')

add('family', '規格文件|負責定義的內容|與其他規格如何分工', 'Specification|Content defined|Relationship to other specifications',
    '第一次讀 NVMe，容易把它當成一本規格就能說完的介面。實際上，命令的共同格式、命令對資料做什麼，以及命令如何經由某種連接方式交換，被分在不同文件。先理解這個分工，才能知道遇到問題時要查哪一份，而不是在單一章節裡找所有答案。',
    '以讀取資料為例，NVM Command Set 解釋 Read 的區塊範圍與資料處理；Base 提供提交及完成的共同機制；PCIe Transport 解釋本機控制器如何利用 PCIe 存取佇列與通知。這些內容共同組成一次操作，閱讀順序可以從操作情境出發，再回到相關欄位。',
    '規格家族图用來連接責任，箭頭不是命令執行順序。先用一個操作分類「共同格式」「命令行為」「傳輸方式」，再對照三份規格的位置。',
    'The specification-family diagram connects responsibilities; its arrows are not an execution sequence. Classify an operation into common format, command behavior, and transport mechanism before locating the corresponding documents.')

add('objects', '存取方式|涉及的主機與儲存對象|它解決什麼問題', 'Access arrangement|Hosts and storage objects involved|Problem addressed',
    'Namespace 是主機可存取的儲存空間，controller 是處理命令的控制器，NVM subsystem 則包含相關控制器與非揮發性儲存資源。它們不是同一個物件的三種名稱。一個 namespace 可以透過不同控制器被存取，因此看見兩條路徑，不一定表示有兩份資料。',
    '多路徑先關心同一主機是否有多條路到同一份儲存空間；共享則關心是否有多個主機存取同一份空間。兩種情況可以同時存在。辨認時應先畫出主機、控制器與 namespace 的連線，再確認儲存對象的身分，不能只數裝置名稱或比較一個局部識別值。',
    '關係圖先找 namespace，再沿線回到能存取它的 controllers 和 hosts。兩條線通往同一物件表示多條路徑；兩個 hosts 指向同一物件表示共享。SR-IOV 图另外描述 PCIe Function 的呈現方式。',
    'Locate the namespace first, then follow connections to controllers and hosts. Multiple paths to one object are distinct from multiple hosts sharing that object. SR-IOV diagrams separately describe the presentation of PCIe Functions.')

add('queues', '佇列配置|SQ 與 CQ 的對應|如何辨認完成的命令', 'Queue arrangement|SQ-to-CQ relationship|Identifying a completed command',
    '提交佇列放主機提出的命令，完成佇列放控制器回報的結果。主機寫好命令後，以 Doorbell 公布新的佇列位置；控制器執行後寫入完成項目。Doorbell 傳達位置更新，並不承載整份命令資料。這個分工可以避免把通知動作誤認為資料傳輸本身。',
    '多個 I/O SQ 可以共用一個 CQ，因此完成項目需要足夠資訊辨認原命令。例如 SQ 3 與 SQ 4 都有 CID=5 的命令，完成時仍可由 SQID 與 CID 的組合分辨。CQ 告訴主機的是每筆命令的結果，並不保證結果排列順序與提交順序相同。',
    '佇列圖分開標示存放命令與结果的位置，沿主機→SQ→控制器→CQ→主機閱讀。再看 SQ／CQ 的配對圖，確認完成項目中的 SQID、CID 如何指回原來的命令。',
    'Distinguish command and result storage, then follow host→SQ→controller→CQ→host. In queue-association diagrams, use SQID and CID in each completion to trace it to the originating command.')

add('numbers', '欄位或表示法|換算後的值|採用這種解讀的依據', 'Field or notation|Decoded value|Basis for the interpretation',
    '規格中的數字要同時讀三件事：進位、編碼方式、單位。1000、1000b、1000h 的外觀接近，數值卻分別是十進位的 1000、8、4096。即使數值解對了，也還要知道它代表 bytes、Dwords、區塊數，或只是某個選項的編號。',
    '再以 512-byte 傳輸為例：先除以每個 Dword 的 4 bytes，得到 128 Dwords；若 NUMD 採從 0 起算的數量編碼，寫入值才是 127。這是先換單位、再編碼的兩步。反向閱讀時應先加 1 解碼，再乘 4 還原 bytes；不是所有數量欄位都需要加 1。',
    '閱讀數值表時，把原始表示、實際數量及單位排成不同欄。Index 選第幾個項目；offset 表示離起點多遠。只有知道每個項目大小及起點，才能把 index 轉成 offset。',
    'Keep raw notation, actual count, and unit in separate columns. An index selects an entry; an offset measures distance from an origin. Converting an index into an offset requires the entry size and the origin.')

add('identity', '控制器類型或標示|可以處理的工作|支援能力如何確認', 'Controller type or marker|Work it can perform|How support is established',
    '控制器類型先決定它負責哪些工作。I/O controller 能處理使用者資料 I/O；Administrative controller 負責管理用途。兩者都可能有 Admin Queue，所以不能因為找到管理佇列，就推論這個控制器也能接受資料讀寫。',
    '同一類型內，選用功能仍可能不同。規格表中的支援標示，必須連同它所在的列、欄與註腳閱讀，才能知道是一定要支援、可以選擇支援，或在某種條件下才適用。控制器識別碼用來辨認對象，也不會單獨證明它具有哪種能力。',
    '先按 controller type 選表格欄，再看每項命令或功能的支援標示。識別碼表回答「是哪一個」，能力表回答「能做什麼」；兩者要在同一控制器的上下文中連接。',
    'Select the controller-type column before reading support markers for commands and features. Identifier tables answer which controller; capability tables answer what it supports. Connect both within the same controller context.')

add('properties-init', 'Property 或設定|主機與控制器各自提供什麼|初始化時的先後關係', 'Property or setting|Host/controller contribution|Order during initialization',
    '初始化是一段由雙方配合的流程。主機先讀能力，選擇相容設定，準備 Admin 佇列記憶體及大小，再要求控制器啟用。控制器完成自己的準備後，才以 RDY 回報可使用。主機寫入 enable 位，只代表提出要求，並不表示控制器已立即就緒。',
    'CAP、CC、CSTS 分別描述能力、主機選擇與控制器狀態。把它們當成不同角色的資訊，才不會用「支援某種 page size」推論目前已使用它，或用「已要求啟用」推論 RDY 已成立。時間上限及錯誤狀態也是初始化條件的一部分。',
    '沿能力→佇列配置→啟用→就緒的順序連接 CAP、AQA／ASQ／ACQ、CC、CSTS。寄存器布局图中的 offset 是定位欄位，狀態圖中的箭頭才描述條件成立後的轉移。',
    'Connect CAP, AQA/ASQ/ACQ, CC, and CSTS as capabilities, queue configuration, enablement, and readiness. Offsets locate fields in register layouts; arrows in the state diagram describe conditional transitions.')

add('queue-arbitration', '佇列狀態或選取方式|它決定什麼|不能由此推論什麼', 'Queue state or arbitration|Decision governed|What it does not determine',
    '環狀佇列的 head、tail 用來追蹤哪些位置已被使用或釋放。索引走到末端後會回到開頭，因此同一個 slot 會被反覆使用；不能只看到某個索引數值，就把它當成命令累積總數。空與滿的判斷也必須依该佇列的規則進行。',
    'Arbitration 決定控制器下一步從哪些候選 SQ 選工作，不保證每筆工作花一樣時間。即使某筆命令先被選中，另一筆較短的命令仍可能先完成。閱讀優先級與權重時，要分清楚服務選擇、命令執行、完成回報三件事。',
    '先用環形圖追蹤 head／tail 移動及位置釋放，再閱讀 Round Robin 或權重選擇流程。佇列位置圖與仲裁圖回答不同問題，不用其中一張推論完成順序。',
    'Use ring diagrams for head/tail movement and slot release, then read round-robin or weighted selection flows. Queue-position diagrams and arbitration diagrams answer different questions; neither alone establishes completion order.')

add('memory-capacity', '記憶體或容量層級|提供哪種資源|使用或比較前的確認', 'Memory or capacity level|Resource provided|Checks before use or comparison',
    'Controller Memory Buffer 與 Persistent Memory Region 是控制器提供的記憶體資源，namespace 則是主機進行區塊存取的儲存空間。即使大小都能換成 bytes，也不能直接把三者相加當成可格式化容量。它們的用途、存取方式與狀態要求不同。',
    '例如 CMB 足以放下一個提交佇列，還要確認控制器允許把 SQ 放在其中。容量足夠解決的是「放不放得下」，能力位解決的是「允不允許這樣用」。在 subsystem、Endurance Group、NVM Set 與 namespace 的容量關係中，也應先確認層級，再理解哪些值可以比較。',
    '資源關係圖先區分工作記憶體和區塊儲存容量，再沿 subsystem 到各群組及 namespace 的關係閱讀。CMB／PMR 欄位則配對位置、大小、允許用途、啟用及就緒狀態。',
    'Separate working-memory resources from block-storage capacity, then follow subsystem, group, and namespace relationships. For CMB/PMR fields, connect location, size, permitted uses, enablement, and readiness.')

add('lifecycle', '停止或重設事件|影響的對象與目的|判斷完成或保留狀態的資訊', 'Shutdown or reset event|Target and purpose|Completion or state-retention evidence',
    '正常關機、控制器重設與 subsystem 重設，影響範圍和目的不同。正常關機提供受控的停止流程；重設則改變指定範圍的狀態。當一個 subsystem 有多個控制器時，範圍的差別尤其重要，不能把只針對一個控制器的動作當成整體重設。',
    '狀態保留也要逐項閱讀。某個設定跨 controller reset 保留，不代表它跨 power cycle 也保留；佇列能否繼續使用同樣要看事件定義。主機提出 shutdown 要求後，還需查看控制器回報的階段，才能確認停止流程走到哪裡。',
    '先選事件類型與範圍，再以保留表逐項看設定及資源的結果。關機狀態圖配對 SHN 的要求和 SHST 的回報；不要把重設後某個初始值當成上次關機成功的證明。',
    'Choose the event and scope before reading state-retention tables. Pair SHN requests with SHST reports in shutdown diagrams. A reset value does not establish that the preceding shutdown completed successfully.')

add('sqe', 'SQE 區域|主機在這裡描述什麼|如何選擇正確的欄位定義', 'SQE region|Information provided by the host|Selecting the right field definition',
    'SQE 是控制器要讀取的一份命令資料結構。共用欄位先告訴控制器這是哪種命令、命令識別值和對象，命令專用欄位再補充操作參數。資料指標則指向另外的緩衝區；命令本身與它要傳輸的資料，不必放在同一個位置。',
    '相同 Dword 編號在不同命令中可能有不同用途。因此先認出 opcode，再查該命令對 CDW10–15 的定義。CID 則與提交佇列身分合用，讓完成結果找回原命令；它不是 namespace 的位址，也不指定資料緩衝區。',
    '共用布局圖先找 CDW0、NSID、MPTR／DPTR 與命令專用區域，再看 CDW0 的 bit 範圍。圖塊為方便閱讀而調整寬度時，以標註的 bits 為準，不能拿像素寬度計算欄位大小。',
    'Locate CDW0, NSID, MPTR/DPTR, and the command-specific region in the common layout before reading CDW0 bit ranges. When boxes are sized for legibility, labeled bits rather than pixel widths determine field size.')

add('cqe-status', '完成狀態欄位|回答哪個問題|解讀時還需哪些資訊', 'Completion-status field|Question answered|Other required information',
    '主機讀取 CQE 時，先要知道這個位置是否包含新完成項目，再辨認它屬於哪筆命令，最後才解釋結果。Phase Tag、SQID／CID、SCT／SC 分別參與這三個問題。單独讀出一個狀態碼，缺少命令和類別，就容易查到錯的狀態定義。',
    'DNR 描述以相同命令重試是否預期能成功，不等於永久硬體故障診斷。CRD 在適用時提供重試延遲選擇，也不是所有狀態都通用的等待時間。這些補充欄位應在辨認主要結果後閱讀，而不是取代主要結果。',
    '完成布局圖按「新項目→原命令→結果」閱讀：先確認 P，再連接 SQID、CID，最後用 SCT 選狀態表並查 SC。DNR、CRD 接在主要結果後解釋。',
    'Read completion layouts as new entry, originating command, and result: check P, connect SQID/CID, then select the status table with SCT and look up SC. Interpret DNR and CRD after the primary result.')

add('prp', '資料跨頁情況|PRP2 的解讀方式|指標與對齊要求', 'Page-span case|Meaning of PRP2|Pointer and alignment requirement',
    'PRP 用記憶體頁描述資料位置。第一個指標可以從頁內某個 offset 開始，因此第一頁可用空間是 page size 減掉 offset。剩下多少資料，才決定 PRP2 是不使用、直接指向另一個資料頁，還是指向一份列出更多頁位址的 PRP List。',
    '例如 page size 是 4096 bytes、第一個 offset 是 512 bytes，第一頁還有 3584 bytes。若傳輸 6000 bytes，剩餘 2416 bytes 可放在另一頁，PRP2 指向該資料頁；若傳輸 10000 bytes，剩餘 6416 bytes 需要兩頁，PRP2 就需要指向 PRP List。下一頁的位址不必緊接第一頁的實體位址。',
    '先算第一頁剩餘量，再算未覆蓋的資料長度，用這個結果選 PRP2 分支。沿 PRP List 圖中的箭頭辨認「清單所在頁」和「資料頁」，兩者的用途不同。',
    'Calculate space remaining in the first page, then the uncovered transfer length, and select the PRP2 case. Follow list arrows while distinguishing a page holding list entries from pages holding transferred data.')

add('sgl', '指標或描述子種類|位址與長度描述什麼|沿指標會找到什麼', 'Pointer or descriptor type|Meaning of address and length|Object reached by following the pointer',
    'SGL 以描述子列出資料區段。每個描述子除了位址與長度，還有類型，用來決定應把它解讀成資料，還是另一段描述子清單。同樣一個 Length 欄位，若描述子是 Data Block，就描述資料 bytes；若是 Segment，則描述清單本身的大小。',
    '假設 12 KiB 資料分散成 8 KiB 與 4 KiB 兩段，可以用兩個 Data Block 描述子表示。若這兩個描述子放在另外一段清單，指向清單的 Segment 描述子長度應依描述子總大小計算，不能填 12 KiB。先辨認指向的物件，再換算長度，是閱讀這類圖的關鍵。',
    '每次沿箭頭前先讀 descriptor type，區分目的地是 data 還是 descriptor list。加總傳輸資料量只計入相應的資料描述，不能把存放清單的 bytes 也當作使用者資料。',
    'Read descriptor type before following each arrow to distinguish data from another descriptor list. When totaling transferred data, do not count bytes occupied by the descriptor list as user data.')

add('identity-text', '識別欄位或清單|辨認的對象與格式|長度及數量如何解讀', 'Identifier or list|Object and format identified|Length and count interpretation',
    '識別資料可能是固定長度的數值，也可能是字串或清單。它們解決的問題不同：廠商 ID 辨認廠商，型號與序號描述產品，namespace 的全域識別值用來辨認儲存對象。長度相同或外觀看起來都是十六進位，並不表示可以互換。',
    '清單也不一定都從數量欄位開始。Controller List 先放 NUMCIDS，再列控制器 IDs；Namespace List 直接排列 NSIDs，未使用位置依規則填零。字串則要分開計算字元數與 bytes，例如「中」以 UTF-8 編碼占 3 bytes，而不是 1 byte。',
    '識別格式圖先看對象、寬度及字串填補規則。Controller List 依 NUMCIDS 讀有效項目；Namespace List 依自己的結構和零值規則讀取，不借用另一張清單的 header 格式。',
    'Read object identity, width, and string-padding rules first. Use NUMCIDS for valid Controller List entries. Read a Namespace List under its own structure and zero-value rules rather than borrowing another list’s header format.')

add('fw-capability-plan', '更新能力|決定哪項選擇|何時使用這項資訊', 'Update capability|Choice it constrains|When it is used',
    '韌體更新前，主機需要知道裝置提供幾個 slot、哪些 slot 可以寫入，以及新映像可以如何啟用。Slot 是保存映像的位置，active slot 才是目前執行的版本。即使裝置提供多個位置，也不能直接假設 slot 1 可覆寫或任何映像都可以立即啟用。',
    '傳输安排還要考慮粒度與時間限制。FWUG 約束映像片段的大小和對齊，啟用時間欄位則描述不同階段允許的時間。若多個控制器共用同一個 firmware domain，更新計畫也要以共享範圍理解，不能把每個 PCIe Function 都當成互不相關的韌體副本。',
    '從 Identify 的 FRMW 選可用 slot 與啟用方式，再讀 FWUG 和相應時間欄位。Domain 關係圖回答哪些控制器共享 slots；它不能由單一 PCIe Function 編號推得。',
    'Use FRMW to select a writable slot and activation method, then read FWUG and the relevant timing fields. Domain diagrams establish which controllers share slots; a PCIe Function number alone does not establish that relationship.')

add('fw-download-geometry', '傳輸欄位|描述哪段位置或長度|從 bytes 如何換算', 'Transfer field|Position or length described|Conversion from bytes',
    'Download 每次傳輸映像中的一段資料，需要同時描述主機緩衝區的位置、本段長度，以及它在整個映像中的位置。DPTR 是主機記憶體位置，OFST 是映像中的偏移；即使兩者都像位址，也屬於不同空間。',
    '一段 4096-byte 資料等於 1024 Dwords，因此 NUMD 的編碼值為 1023，也就是 03FFh。第二段的映像偏移是 4096 bytes，所以 OFST=1024=0400h；OFST 直接表示位移，不像 NUMD 需要減 1。用這個對比，可以同時看懂長度與偏移為何不能共用換算方式。',
    '把映像畫成連續區間，逐段列出起點 bytes、長度 bytes、OFST 與 NUMD。各段邊界再核對 FWUG；主機 buffer 的 DPTR 不參與映像 offset 的累加。',
    'Represent the image as contiguous ranges and list each start, byte length, OFST, and NUMD. Check range boundaries against FWUG. The host buffer’s DPTR is separate from accumulated offsets within the image.')

add('fw-commit-state', 'Commit 欄位或結果|選擇或確認的動作|如何判斷啟用階段', 'Commit field or result|Selected or established action|Determining the activation stage',
    '映像下載完成後，Commit 才決定如何保存和啟用。CA 指定動作，FS 指定 slot；不同動作可能只保存、安排後續啟用，或依能力執行不需重設的啟用。因此 Download 的完成資訊，無法取代 Commit 的結果。',
    '某些完成狀態是在告訴主機還需要哪一種重設才能啟用映像，不能一概解讀成映像內容無效。反過來，slot 已經保存新版本，也不表示目前正在執行它。應把傳輸完成、slot 內容和 active 版本放在時間線上分別確認。',
    'CA 表先看動作，再與 FS 和控制器能力配對。完成狀態表把映像拒絕、所需重設和一般完成分開；MUD 則另外描述重疊更新資訊，不用它代替啟用結果。',
    'Select the action in the CA table and pair it with FS and capabilities. Distinguish image rejection, required reset, and ordinary completion in status tables. MUD separately reports overlapping-update information, not the activation outcome.')

add('fw-lid03-proof', '版本或 slot 欄位|描述哪個時點|如何與其他欄位對照', 'Revision or slot field|Time/state described|Cross-check with other fields',
    'Firmware Slot Information 把「目前執行」和「下次預定執行」分成兩個欄位。CAFS 是現在的 slot，NAFS 是下次重設後預定啟用的 slot；FRS 則記錄各 slot 的版本字串。讀到一個新版本字串，只證明該位置回報該版本，還要看它是否被選為目前執行。',
    '例如 CAFS=1、NAFS=2，表示目前與預定版本不同；如果 CAFS=2、NAFS=2，則現在已是 slot 2，後續也預定使用它。Identify.FR 提供目前版本的另一個觀察位置。事件通知可以提醒版本相關狀態變化，但最後仍要閱讀實際欄位。',
    '先拆開 AFI 中的 CAFS 與 NAFS，再以 slot 編號找到 FRSx，最後與 Identify.FR 對照。UUID 選擇及通知欄位只用於本次 LID 03h 的存取與事件關係，不改變版本欄位的意義。',
    'Separate CAFS and NAFS in AFI, use the slot number to find FRSx, and compare the current revision with Identify.FR. UUID selection and notice fields support access/event handling for LID 03h without changing revision semantics.')

add('feature-read-set-loop', 'Get Features 選擇值|要求讀取什麼|可用來做哪種判斷', 'Get Features selector|Requested information|Decision it supports',
    '同一個 Feature 可以有目前值、預設值及保存值。主機讀取時需要用 SEL 說明想查哪一種；讀到保存值不代表它就是目前正在使用的值。支援能力查詢則另外告訴主機這個 Feature 是否可變更、可保存，以及作用對象是否與 namespace 有關。',
    '設定流程應先確認可變更，再選擇符合控制器能力的值。是否保存是另一個選擇，不能因為 Set 成功就假設下次重設或斷電後仍會使用它。這個讀取與設定的共同流程，會被後面各個電源及溫度 Feature 使用。',
    'Get Features 的 CDW10 同時含 FID 與 SEL。先以 FID 選功能，再用 SEL 選 current、default、saved 或 supported capabilities；不要把支援旗標的回傳格式當成一般設定值。',
    'CDW10 contains both FID and SEL. Select the Feature with FID and current, default, saved, or supported-capabilities information with SEL. Capability flags use a different interpretation from ordinary Feature values.')

add('power-state-mental-model', '電源狀態屬性|描述的功耗或效能|比較時需要的條件', 'Power-state attribute|Power or performance described|Conditions for comparison',
    '電源狀態描述的不只是消耗多少電。每個狀態還可能有不同的服務能力與進出延遲，因此更省電的選擇，可能讓下一次 I/O 等更久。Operational 與 non-operational 狀態也有不同工作條件，不能只按數字大小假設功能一致。',
    'ENLAT 描述進入一個狀態的延遲，EXLAT 描述離開的延遲。由 PS1 轉到 PS3 時，若走直接路徑，需要考慮 PS1 的離開時間和 PS3 的進入時間；若途經其他狀態，就逐段計算。相對效能值則用於相同類別的比较，不是直接的 IOPS 或微秒數。',
    'Power State Descriptor 先看 operational 性質，再分組讀功率、進出延遲與相對效能。功率尺度和測量條件要與數值一起看，不能把典型值和最大值放在同一欄直接排名。',
    'Read the operational attribute first, then power, transition latencies, and relative performance as separate groups. Interpret power scales and measurement conditions with their values rather than ranking typical and maximum values as equivalent measurements.')

add('apst-state-machine', 'APST 或背景工作設定|控制器如何進入或使用狀態|受哪些條件限制', 'APST or background-work setting|State-entry or use behavior|Constraints',
    'APST 讓主機設定閒置多久後進入哪個較省電狀態，控制器再依連續閒置時間執行。表格存在不代表計時器已啟動，還要看 APSTE 是否啟用。主機直接指定狀態與由閒置計時器觸發，則是兩種進入方式。',
    'ITPT 記錄等待的閒置時間，ITPS 指定目標狀態。進入 non-operational 狀態後，背景工作能否暫時使用較高功率，還受 NOPPME 等規則控制。理解 APST 時應把節電、背景工作和恢復服務的延遲一起看，不能只把等待時間越短視為越好。',
    'APST entry 圖先解讀 ITPT 與 ITPS，再連到被選 Power State Descriptor。以 2000 ms、PS3 為例，ITPT 放入 bits31:8，ITPS 放入 bits7:3；時間值移位與目標狀態編碼分開驗算。',
    'Decode ITPT and ITPS in the APST entry and connect the selected target to its Power State Descriptor. For 2000 ms and PS3, place ITPT in bits31:8 and ITPS in bits7:3, verifying the shifted time and target-state encoding separately.')

add('temperature-event-loop', '門檻欄位|選擇或設定什麼|事件觸發與解除如何判斷', 'Threshold field|Selection or setting|Event assertion and clearing',
    '溫度門檻先要指定感測器，再選擇高溫或低溫方向。相同溫度值若套到不同感測器或比較方向，代表的事件也不同。TMPTH 使用 Kelvin；為了日常閱讀可以換算成攝氏，但編碼與比較仍要依原始單位進行。',
    'Hysteresis 讓事件解除的溫度與觸發溫度不同，避免溫度在門檻附近小幅波動時反覆切換。以高溫門檻為例，降溫後需符合解除條件，不能只看到低於觸發值就忽略遲滯設定。通知描述的是溫度事件，並不等於 HCTM 已採取某一級熱控制。',
    '先看 TMPSEL 與 THSEL，再配對 TMPTH、TMPTHH。在溫度軸上分別標出觸發和解除位置，用規格的比較符號確認邊界，並與 SMART 的感測器讀值對照。',
    'Select TMPSEL and THSEL before pairing TMPTH with TMPTHH. Mark assertion and clearing points separately on a temperature axis, retaining the specified comparison operators, and relate them to SMART sensor values.')

add('hctm-control-loop', '熱管理欄位或統計|設定或觀察的內容|使用前需確認什麼', 'Thermal-management field or statistic|Setting or observation|Required checks',
    'HCTM 讓主機提供兩級熱管理門檻。較低門檻著重減少對效能的影響，較高門檻允許更積極地控制溫度；這不是兩個感測器，也不是事件通知的觸發和解除溫度。主機需要在控制器允許的範圍內設定兩者。',
    '設定成功只能確認控制器接受這組值，不表示當時溫度已經觸發控制。轉換次數與累計時間可以幫助觀察曾經發生的熱管理活動，但它們是歷史統計，不能單獨當作目前正在節流的證明。讀目前值、即時溫度和統計時要分清時間意義。',
    '將 TMT1、TMT2 放在同一條溫度軸，再用 MNTMT、MXTMT 檢查允許範圍。SMART 中的次數和時間對應控制活動的累計紀錄，不與門檻設定值混讀。',
    'Place TMT1 and TMT2 on one temperature axis and check their permitted range with MNTMT/MXTMT. SMART counts and times are accumulated records of control activity, separate from the configured thresholds.')

add('three-boundaries', '功能|主機與控制器交換什麼|用哪個結果確認下一步', 'Function|Host/controller interaction|Result needed for the next step',
    '這篇包含的功能並非依序執行的一套流程，而是用來理解幾種不同的控制器工作。Self-test 啟動背景診斷；HMB 借用主機記憶體；Doorbell Emulation 與廠商自訂命令則需要特定的位址與長度編碼。先分清工作內容，後面才能解釋完成狀態。',
    '例如 Self-test 啟動成功後，測試還在進行；HMB 停用成功後，主機才可以依規則收回記憶體。兩筆命令都可能回成功，確認的事件卻不同。理解這個差別，比單獨記住某個 opcode 或狀態數值更能串起整篇內容。',
    '功能對照表用來選擇後續應讀的結果：Self-test 連到 LID 06h，HMB 連到使用期間與停用完成，位址／長度編碼則連到其欄位單位。不要把這些不同功能畫成一條必須依序執行的箭頭。',
    'Use the comparison to select the next result: LID 06h for Self-test, lifetime and disable completion for HMB, and field units for address/length encodings. These functions are not one mandatory execution sequence.')

add('selftest-command-state-machine', '測試對象或控制值|涵蓋的範圍或動作|執行與結果的規則', 'Test target or control|Scope or action|Execution and result rules',
    'Device Self-test 啟動的是背景測試。主機用 STC 選短測試、延伸測試或中止，用 NSID 選對象；命令完成後還需要查詢進度與結果。測試對象在開始時決定，因此不能因稍後增加了可存取 namespace，就假設它自動加入既有測試。',
    'NSID=0、指定 namespace、所有可存取的 attached namespaces，代表不同範圍。最後的結果也需要先看結果種類，再判斷哪些附加欄位有效。失敗 segment 或 LBA 並非每筆結果都提供，不能因欄位裡有數字就直接採用。',
    '命令格式先讀 NSID 與 STC，再沿狀態流程找到 LID 06h。結果布局先拆開測試種類與結果碼，再依 SEGN、FVLD 等有效性條件決定要讀哪些細節。',
    'Read NSID and STC in the command, then follow the state flow to LID 06h. Separate test type from result code in result entries and use SEGN/FVLD validity rules to determine which details are meaningful.')

add('selftest-observe-results', '進度或歷史欄位|描述什麼資訊|何時可以使用這個欄位', 'Progress or history field|Information described|When the field is valid',
    'Self-test log 同時包含現在執行中的狀態與先前完成的結果。主機想知道測試是否仍在執行，先看 current operation；想知道測試通過與否，則讀歷史結果。百分比欄位只有在相應狀態下才有意義，不能把沒有測試時的數值當成進度。',
    '結果描述子可能記錄 segment、LBA、執行時數或相關狀態，但每項都有使用條件。FLBA 若有效，可以指出其中一個失敗位置；它不是完整的壞區清單，也不能保證沒有被列出的區塊都正常。這些限制需要在讀數值之前先理解。',
    '先分開 log 的 current header 與歷史結果描述子。DSTS 中測試種類和結果碼分開讀，再以结果種類及有效位決定 SEGN、FLBA 等欄位是否有效；NUMD 計算則使用整個所需傳輸長度。',
    'Separate the current-operation header from historical descriptors. Decode test type and result code in DSTS, then apply result/validity rules before using SEGN or FLBA. Calculate NUMD from the full required transfer length.')

add('hmb-ownership-lifecycle', 'HMB 使用階段|哪一方可以使用記憶體|進入下一階段的條件', 'HMB lifetime stage|Permitted memory user|Condition for the next stage',
    'HMB 是主機提供給控制器使用的記憶體。主機先配置區域和描述子，再以 Feature 將它交給控制器；啟用期間，主機必須維持這些記憶體有效，不能當成一般空閒記憶體重新分配。配置者仍是主機，但可使用的時機受 HMB 規則限制。',
    '停用要求已提交與停用命令已完成，是兩個不同時刻。在中間這段時間，控制器仍可能取回必要資料，因此主機不能提前收回區域。只有到規格定義的交接完成點，才可以修改或回收；這也是 HMB 的完成狀態與背景測試啟動成功不同之處。',
    '沿時間線標出 enable 完成、disable 提交與 disable 完成，對每個區間註明主機和控制器的使用權限。描述子中的位址在整個使用期間都必須保持有效，而不是只在送命令時有效。',
    'Mark enable completion, disable submission, and disable completion on a timeline, identifying permitted access in each interval. Descriptor addresses must remain valid throughout the permitted controller-use period, not merely when the command is submitted.')

add('hmb-command-math', '大小或位址欄位|使用的單位或對齊|描述的資源', 'Size or address field|Unit or alignment|Resource described',
    'HMB 的能力值與實際配置值不是全部使用同一單位。HMPRE、HMMIN 使用 4 KiB 單位；HSIZE、BSIZE 使用 CC.MPS 所指定的記憶體頁大小。計算總量時，先把每種欄位換成 bytes，再比較建議值、下限及實際提供量。',
    '描述子清單列出每個區域的起點與大小。清單本身有自己的位址及對齊要求，清單內的記憶體區域也有另外的對齊要求。兩個 BSIZE=32 的區域，在 page size=4096 bytes 時各有 128 KiB，合計 256 KiB；這個加總再與 HSIZE 對照。',
    '命令圖先組合清單的高低位址及 HMDLEC，再讀每個 BADD／BSIZE。把 4 KiB 單位和 CC.MPS 頁單位分兩欄列出，確認換成 bytes 後總量一致。',
    'Combine the descriptor-list address halves and read HMDLEC before following BADD/BSIZE entries. Keep fixed 4 KiB units separate from CC.MPS page units and compare totals only after converting them into bytes.')

add('hmb-reset-power', 'HMB 狀態或設定|描述的限制或記憶體來源|何時可以採用這個值', 'HMB state or setting|Restriction or memory source|When the value applies',
    '電源轉換與重設後，主機需要確認原本提供的 HMB 是否仍符合再次使用的條件。設定的限制政策與目前限制是否生效，分別由不同欄位表示；控制器處於不同電源狀態時，兩者的數值可能不同，而不代表設定被遺失。',
    'MR=1 表示交回符合規格要求的原有 HMB，不只是「容量一樣」。記憶體範圍、描述子清單位置和內容等都要符合相同條件。若提供了一份新配置，即使大小相等，也不能直接用原有記憶體的方式宣告，因為控制器需要重新建立對其內容的理解。',
    '保留規則先按電源或重設事件分組，再分別讀政策欄位 HMNARE、目前狀態 HMNAR，以及 MR 對記憶體一致性的要求。相同容量與相同記憶體配置必須分開判斷。',
    'Group retention rules by power/reset event, then distinguish configured policy HMNARE, current state HMNAR, and MR’s memory-identity requirements. Equal capacity does not establish an identical memory configuration.')

add('encoded-boundary-safety', '位址或長度欄位|換算公式|該值作用於哪個對象', 'Address or length field|Conversion|Object governed',
    'DSTRD、NDT 與 NDM 都是編碼值，但換算方式不同。DSTRD 決定相鄰 Doorbell 的間距，使用指數關係；NDT 與 NDM 則以 Dword 計算資料與 metadata 的傳輸量。它們看起來都像長度，不能共用「全部加 1」或「全部直接當 bytes」的規則。',
    '例如 DSTRD=4 得到 4×2^4=64 bytes 的間距。NDT=0100h 則是 256 Dwords，也就是 1024 bytes，沒有加 1。廠商自訂命令還要先確認採用哪種標準格式及適用能力；長度欄位只描述傳輸量，不能據此猜測廠商資料的內容。',
    '換算表逐列寫出欄位原始值、公式和 bytes。DSTRD 連回 Doorbell 位址，NDT／NDM 分別連回 data／metadata buffer；VSCF／SNVSCF 先決定適用的命令格式。',
    'For each field, retain the encoded value, conversion formula, and resulting bytes. DSTRD connects to doorbell addresses, while NDT/NDM connect to data/metadata buffers. VSCF/SNVSCF establish the applicable command format first.')

add('diagnostic-and-provisioning', '管理對象|主機要建立或觀察什麼|用哪個結果接續操作', 'Managed object|What the host establishes or observes|Result used for the next operation',
    '裝置自我測試與 namespace 管理都使用管理命令，但工作目標不同。測試啟動一項背景診斷；建立 namespace 則配置一份儲存物件。知道這個差別，才能決定收到命令成功後，下一步應讀測試結果，還是建立存取關係。',
    'Create 成功會提供 namespace 的識別值，但尚未自動將它附加到每個控制器。測試啟動成功也不表示測試已通過。因此本篇依「對象→命令→後續狀態」組織，而不是把所有成功完成都視為工作已全部結束。',
    '先用關係表選對象：測試、儲存物件、控制器的存取關係或清單。再追蹤對應的完成資訊及後續查詢，避免用 Self-test 的完成語意解釋 Namespace Create。',
    'Select the object first: a test, storage object, controller-access relationship, or inventory. Follow its completion and subsequent query rather than applying Self-test completion semantics to Namespace Create.')

add('capacity-granularity-math', '容量欄位|使用的單位|這個數值描述什麼', 'Capacity field|Unit|Quantity described',
    'NSZE 是可定址的區塊數，NCAP 是可配置容量，NUSE 是目前配置量；NSG、NCG 則提供以 bytes 表示的建議粒度。這些欄位要先換到相同單位才能比較。容量關係屬於規格要求，是否符合粒度建議則影響配置是否有效率，兩者的判斷目的不同。',
    '每區塊 4 KiB 時，1024 個區塊是 4 MiB，1000 個區塊是 4000 KiB，也就是 3.90625 MiB。後者不是 1 MiB 或 2 MiB 的整數倍，可能需要配置部分主機無法定址的空間；但其他要求都符合時，不能只因未符合這項建議而拒絕建立。',
    '容量圖比較 NSZE、NCAP、NUSE 的數量，粒度表則以 bytes 比較。先列出區塊數×區塊大小，再計算對 NSG、NCG 的餘數；不要直接拿區塊數除以 byte 粒度。',
    'Capacity diagrams compare NSZE, NCAP, and NUSE quantities; granularity tables compare bytes. Multiply block counts by block size before calculating remainders for NSG and NCG. Never divide a raw block count by a byte granularity.')

add('namespace-create-payload', '資料區域與解讀格式|該區域的用途|欄位有效的條件', 'Region and interpretation|Purpose|Conditions for field validity',
    'Namespace Create 的資料 buffer 同時涉及 Base 定義的共通外框與所選 I/O Command Set 的解讀方式。讀布局時要先確認現在看的是哪一層格式，不能把另一層同一 byte 範圍的標示直接搬過來。NVM 專用資料再描述容量、格式與保護設定。',
    '某些欄位只有功能啟用時才使用，例如 FDP 的 Placement Handle List。資料出現在固定位置，不表示任何情況下都要填入。建立前應依所選功能檢查欄位組合，並區分有標準定義的部分、保留區與廠商定義區域。',
    '先從 Base 的資料外框進入 NVM 專用解讀，再對照相同 offset 的欄位。容量值按所選格式換算，Placement Handle List 按 FDP 啟用條件讀取；表中的不同列不是互相獨立且可以相加的 buffer。',
    'Move from the Base data envelope to the NVM-specific interpretation, comparing fields at the same offsets. Convert capacity with the selected format and read the Placement Handle List under FDP enablement rules. Rows describing different interpretations are not separate buffers to add together.')

add('namespace-lifecycle', '管理動作|改變哪個物件或關係|操作後仍保留什麼', 'Management action|Object or relationship changed|What remains afterward',
    'Create 建立儲存物件，Attach 建立它與控制器之間的存取關係。Detach 移除某個關係，Delete 才移除物件。因此 namespace 可以存在卻尚未連到控制器，也可以只從某個控制器分離，但仍由另一個控制器存取。',
    '例如 NSID 7 已連到控制器 3 和 5。只對控制器 3 執行 Detach，並不刪除 namespace，也不自動移除控制器 5 的連接。觀察結果時要分別查 allocated 清單及每個控制器的 active 清單，不能用其中一份清單代表全部關係。',
    '生命週期圖用實線物件表示 namespace，用連線表示 attachment。Create／Delete 改變物件，Attach／Detach 改變連線；Controller List 指定要改哪些控制器的關係。',
    'Represent a namespace as an object and attachments as connections. Create/Delete change the object; Attach/Detach change connections. The Controller List selects which controllers’ relationships are changed.')

add('delete-restore-state', '刪除或恢復動作|命令如何選對象|完成後如何確認配置', 'Deletion or restoration|Target selection|Establishing the resulting configuration',
    '刪除 namespace 與恢復預設配置是不同操作。Delete 先移除指定儲存物件；Restore 再要求裝置回到所定義的預設配置，且有自己支援能力與執行順序的要求。不能把 Restore 當成任何狀態下都可使用的重設按鈕。',
    'DNCS 回報是否處於預設 namespace 配置，但它不是完整的預設清單。即使 Restore 成功，主機仍要重新查詢實際存在的 namespace 與格式，才能重新建立對儲存空間的理解。成功狀態與配置內容是互補資訊。',
    '先區分單一 Delete、Delete all 與 Restore 的 SEL／NSID 用法，再沿流程核對剩餘 namespace 及支援能力。結果圖把 DNCS 和重新取得的 namespace 清單並列閱讀。',
    'Distinguish SEL/NSID usage for single deletion, Delete all, and Restore, then check remaining namespaces and support along the flow. Read DNCS together with a refreshed namespace inventory.')

add('namespace-events', '通知或清單|描述哪種配置變化|應重新查詢什麼', 'Notice or inventory|Change described|Information to refresh',
    '通知的用途是提醒主機配置可能改變，不是直接交付完整的新配置。Create 會改變已配置物件的集合，Attach 則改變某個控制器的可存取集合，因此它們引發的觀察需求不同。主機收到通知後，要查相應清單。',
    '同一個 namespace 變化，對處理命令的控制器與其他控制器可能有不同通知規則。不能只計算收到幾個事件就推論變更多寡。讀者應關心的是哪一份原本的資訊可能過期，以及哪個查詢能重建正確的物件與存取關係。',
    '事件圖從 Create／Attach／Detach／Delete 出發，分別連到 Allocated 和 Active 清單。CNS 02h 和 CNS 10h 查不同集合；namespace 的獨立屬性查詢則補足清單沒有提供的內容。',
    'Connect Create/Attach/Detach/Delete events to Allocated and Active inventories separately. CNS 02h and CNS 10h query different sets; independent namespace attribute queries provide information not contained in the lists.')

add('layers', '規格層次|負責的行為|本篇如何使用它', 'Specification layer|Behavior defined|Use in this report',
    'PCIe Transport 把 NVMe 的共同命令機制落實到 PCIe 連接方式。主機可以透過記憶體映射的暫存器設定控制器及更新 Doorbell，控制器則依傳輸規則存取主機記憶體中的命令與資料。這讓「提交命令」成為實際的記憶體及通知操作。',
    '命令要做什麼仍由 Base 或對應 Command Set 定義。PCIe 的錯誤狀態、組態能力和中斷格式則屬於另一層資訊。閱讀時要分開辨認操作結果和傳輸環境，才不會把某個 PCIe 狀態直接翻成 NVMe 命令狀態碼。',
    '層次圖先區分命令語意、NVMe 在 PCIe 上的綁定及 PCIe 原生能力。用一筆命令依次找出 SQE、主機 buffer、Doorbell 和中斷的位置，而不是把三份規格當成依序執行的程式。',
    'Separate command semantics, the NVMe-to-PCIe binding, and native PCIe capabilities. Trace one command through SQE, host buffer, doorbell, and interrupt locations rather than treating the documents as sequential execution stages.')

add('mmio-doorbell', 'Doorbell 或寫入值|位址或內容如何計算|主機用它通知什麼', 'Doorbell or written value|Address or value calculation|Host notification conveyed',
    'BAR 讓主機找到裝置的記憶體映射空間，Doorbell 則位於其中的指定 offset。每組佇列有 SQ Tail 和 CQ Head 的 Doorbell，它們交錯排列；DSTRD 決定相鄰 Doorbell 的間距。因此 queue ID 與 SQ／CQ 的種類都參與位址計算。',
    'DSTRD=1 時，間距是 4×2^1=8 bytes。Queue 3 的 SQ Tail 使用第 6 個間距，CQ Head 使用第 7 個間距，所以 offset 分別是 1030h 和 1038h。寫入 Doorbell 的數值是新的佇列位置，不是這個 offset，也不是 SQE 或 CQE 的資料內容。',
    '位址表把 BAR 基底、1000h 起點、queue ID 和 stride 分開計算。先找對暫存器，再解讀寫入的 head／tail 值，避免混淆暫存器位址與暫存器內容。',
    'Calculate the BAR base, 1000h origin, queue ID, and stride separately. Locate the register before interpreting the head/tail value written to it; register address and register contents are different quantities.')

add('command', '需要重用的資源|何時不再由原操作使用|主機應觀察的資訊', 'Resource to reuse|When prior use ends|Host observation',
    'PCIe 上的一次命令交換包含資料結構寫入及位置通知。主機先讓完整 SQE 可被控制器看見，再更新 SQ Tail Doorbell。控制器處理命令及資料後，寫入 CQE；主機讀完結果，再以 CQ Head Doorbell 釋放完成佇列位置。',
    'SQ slot、命令資料 buffer 和 CQ slot 各有不同使用期間。控制器已取走某個 SQE，不等於它已完成對資料 buffer 的存取；主機讀到 CQE，也要依完成與可見性規則再重用相關資源。把三者分開追蹤，可以理解為什麼只有一個 head 或 tail 值不足以描述全部資源狀態。',
    '交換流程分三條線看：SQE 的發布與取得、data buffer 的使用、CQE 的寫入與釋放。SQHD 協助追蹤 SQ 消費位置，SQID／CID 辨認完成命令，CQ Head 則釋放完成位置。',
    'Read three lifetimes: SQE publication/fetch, data-buffer use, and CQE production/release. SQHD helps track SQ consumption, SQID/CID identify the completed command, and CQ Head releases completion slots.')

add('interrupts', '中斷方式|通知與遮罩如何安排|影響的資源或限制', 'Interrupt mechanism|Notification and masking arrangement|Resources or limits affected',
    '中斷通知主機有工作需要處理，完成資料本身仍在 CQ 中。一個中斷向量可能對應多個 CQ，所以收到通知後要查看相關佇列，而不是假設一個通知一定只代表一筆命令。主機也可以在適用安排下輪詢 CQ，通知方式與結果存放位置是不同問題。',
    '中斷合併可以减少通知次數，但也可能讓已產生的完成項目等待較久才被通知。這是通知成本與回應時間之間的取捨。比較 MSI、MSI-X 等方式時，應看向量配置、共享及遮罩如何管理，不以名稱判斷命令執行速度。',
    '先把 CQ 連到使用的 vector，再讀該中斷方式的 enable、mask 與 table。收到共用向量時沿所有相關連線查 CQ；合併門檻改變的是通知時機，不是 CQE 的狀態意義。',
    'Connect CQs to vectors before reading enable, mask, and table fields for the chosen interrupt mechanism. For shared vectors, follow all associated CQs. Coalescing changes notification timing, not the meaning of CQE status.')

add('config-error', '回報層次或能力|描述的事件或資源|必須連同哪些資訊閱讀', 'Reporting layer or capability|Event or resource described|Information needed alongside it',
    'Configuration Space 描述 PCIe 裝置呈現的能力與設定。它與 NVMe 的命令結構不同：CQE 回報某筆命令的結果，PCIe 狀態描述連接或 Function 的事件。遇到一個錯誤位時，要先確認它來自哪一層，才能找到正確的解釋。',
    '錯誤紀錄中的狀態、遮罩、嚴重程度與相關交易資訊各有用途。某個狀態位被設起來，不會自動決定是否已通知主機，或對應哪個 NVMe SC。裝置介面回報結構則描述另一種配置資訊，也必須以自己的長度與欄位格式閱讀。',
    '先辨認 PCIe capability 的種類，再將 status、mask、severity 和 header log 配對。TDISP 的 DEVICE_INTERFACE_REPORT 依其欄位布局閱讀，不能套用錯誤 log 或 NVMe CQE 的解讀方式。',
    'Identify the PCIe capability, then pair status, mask, severity, and header-log information. Read TDISP DEVICE_INTERFACE_REPORT under its own layout rather than applying error-log or NVMe CQE formats.')

add('eom', '量測資料區域|描述的量測與位置|比較前須先確認什麼', 'Measurement region|Measurement or location described|Checks before comparison',
    '接收端眼圖量測用來描述接收端在不同量測條件下取得的結果。這份報告的重點是如何讀懂 NVMe 提供的量測資料結構，而不是用眼圖外觀直接估算 SSD 的 IOPS。Lane 身分、量測設定和資料格式不同時，結果不能直接比較。',
    'Header 描述整体長度與布局，lane descriptor 再帶到個別 lane 的結果。Printable Eye 是可供人閱讀的一種呈現方式，不是另一條實體 lane，也不能把字元數當成品質分數。要比較兩條 lanes，先確認量測條件與座標尺度相同。',
    '從 header 讀出結果布局，再循 lane descriptor 到量測資料。眼圖先看量測尺度和圖例，確認每個位置表示什麼；Printable Eye 與數值結果對應閱讀，不以圖上開口的像素寬度推論未定義的效能。',
    'Read the result layout from the header and follow lane descriptors to measurement data. Establish scales and legends before interpreting positions. Relate Printable Eye to numeric results rather than inferring unspecified performance from pixel widths.')
