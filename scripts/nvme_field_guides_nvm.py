"""NVM Command Set field relationships, written for the local tutorial."""

def install(guide):
    def n(nums, key, title, relation, *rows):
        guide('nvm', nums, key, title, relation, list(rows))

    n([1,2], 'foundation', '先確定命令、格式與單位',
      'NVM 命令以 logical blocks 描述資料；Base 定義共同命令格式，PCIe Transport 定義傳輸，NVM Command Set 決定資料操作與格式。',
      ('LBA／logical block size','LBA 選位置，格式決定每個位置包含多少資料。','相同的 8 個 blocks，512-byte 與 4096-byte 格式分別需要 4096 與 32768 bytes 資料。'),
      ('欄位名稱／縮寫','先分辨它是識別碼、數量、位移或能力，才選擇解讀方式。','Format Index 選一種格式；LBADS 是大小的指數，兩個值不能直接互換。'))
    n([3,4,5,6,7,8,9,10,98,126,146], 'atomic', '把保證範圍、對齊邊界與失效情境分開',
      '正常操作與斷電情境各有原子性參數。先確認採用控制器或 namespace 的參數，再把命令的整段範圍放到原子邊界上判斷。',
      ('AWUN／NAWUN；AWUPF／NAWUPF；ACWU／NACWU','分別對應正常寫入、斷電情境與融合 Compare/Write 的保證上限；有效選擇依 namespace 能力。','支援 8-block 的正常原子寫入，不代表斷電時也保證相同的 8 blocks。'),
      ('NABSN／NABSPF／NABO','邊界大小與起點決定一段 I/O 是否跨界，與單筆長度上限一起檢查。','長度雖未超過原子單位，起點若靠近邊界，結束位置仍可能落到下一段。'),
      ('MAM／DN','多重原子模式與正常原子性停用選擇有各自條件。','多重模式下應畫出可獨立保證的子範圍，不能沿用整筆命令全有或全無的結論。'),
      ('Compare／Write／FUSE','融合操作需符合配對與範圍規則，Compare 的結果影響 Write 是否執行。','先前內容不符預期時，不能把後面的 Write 當成獨立無條件寫入。'))
    n([11,12,174,175,176,177,178,179,180,181,182], 'pi-processing', '先決定傳輸哪些資料，再決定檢查與產生哪些 PI',
      'PRACT 選資料保護處理方式，PRCHK 的各 bit 選檢查項目；格式、metadata 大小與命令方向共同決定實際傳輸量。',
      ('PRACT／MS／PI size','結合所選格式判斷 PI 是隨資料傳輸，還是由控制器插入或移除。','MS 大於 PI 大小時，移除 PI 不代表整份 metadata 都消失。'),
      ('GRDCHK／ATCHK／RTCHK／STC','Guard、Application Tag、Reference Tag 及 Storage Tag 的檢查分別選擇。','只選 Guard 檢查，不可宣稱同時驗證了所有 tag 的關聯。'),
      ('PRINFOR／PRINFOW；STCR／STCW','Copy 的來源讀取與目的寫入可有不同處理；兩端的選擇需要成對閱讀。','來源有 PI、目的沒有 PI 的 Strip，與來源沒有 PI、目的需要 PI 的 Insert，資料流方向相反。'),
      ('來源資料／主機資料／比較結果','Compare 先依設定處理與檢查，再比較指定資料；錯誤可來自不同階段。','PI 檢查失敗與資料比較不相等，不能合成同一種 Compare Failure。'))
    n([13,14,15,16,17,18,19,20,22,31,59,66,76,80,89,92,93,109,141,199,200], 'support', '從操作與狀態選出正確的規則列',
      '先辨認命令、控制器類型及目前狀態，再讀支援或限制。狀態碼還要配 SCT，不能只看 SC 的數字。',
      ('Opcode／NSID／資料方向','Opcode 選操作，NSID 選對象，方向決定主機提供或接收什麼。','Copy 的主機傳入資料是描述子清單，並非整份來源資料。'),
      ('SCT／SC','狀態類別決定使用哪份狀態表；同一類別內再判斷原因。','LBA Out of Range 針對位址範圍，Capacity Exceeded 針對配置容量，不應混為一談。'),
      ('支援標記／適用註腳','需要结合可選能力、控制器種類與目前操作的限制。','控制器平常支援 Read，不代表清除的每一種受限狀態都允許同樣行為。'),
      ('ANA／Reservation type／Holder／Registrant','路徑狀態與主機的存取資格分別影響操作；逐項配合命令種類判斷。','同一 namespace 對兩個主機可有不同存取資格，不能只用 NSID 相同推論结果相同。'))
    n([23,24,50,51,67,68,153,154], 'buffers', '資料與 metadata 用同一個區塊順序配對',
      '先依格式選交錯或分開傳輸，再由區塊數計算各緩衝區大小。DPTR 與 MPTR 的角色由傳輸配置及命令方向決定。',
      ('DPTR／MPTR／FLBAS','資料指標與 metadata 指標的適用性由格式及傳輸方式決定。','分開傳輸時，Data 0 必須對應 Metadata 0；分成兩個 buffer 不會改變配對順序。'),
      ('區塊數×資料大小／區塊數×MS','先計算兩部分，再依 PRACT 等處理調整實際傳輸量。','PRACT=0、8 blocks、4096 bytes 資料與 16 bytes metadata，兩部分是 32768 與 128 bytes。'))
    n([25,29,30,33,37,38,52,57,58,60,64,65,69,74,75,81,86,87,155,156,157,159,164,165,166,167,168,169,170,171,172,173], 'tags', '由 PI 格式決定 tag 的位數與命令位置',
      '先確認 Guard 格式及 STS，再計算 Storage Tag 與 Reference Tag 的位數。命令中的高低欄位組合成 tag 空間，而不是各自獨立的位址。',
      ('PIF／QPIF／STS','Guard 格式決定可用 tag 空間，STS 分配其中的 Storage Tag 位數。','64b Guard 的合併空間為 48 bits；STS=18 時 Reference Tag 使用其餘 30 bits。'),
      ('LBST／ELBST／ILBRT／EILBRT','寫入的 tag 與檢查時的 expected tag 有不同角色；起始 Reference Tag 依命令和類型推進。','Read 的預期 tag 用來比對，不能把它當成控制器必定回傳的資料值。'),
      ('CDW2／CDW3／CDW14；ELBTU／ELBTL','按格式把高低部分放到指定位置，未使用或忽略的 bits 依圖中規則處理。','STS=18 時先做 (StorageTag<<30)|ReferenceTag，再拆高低 Dwords；不能按十六進位字串任意切段。'),
      ('LBAT／ELBAT／ELBATM／LBSTM','Application Tag、預期值與遮罩、Storage Tag 遮罩分別服務不同檢查。','先選擇哪些 bits 參與比對，再解釋比較結果；遮罩不是要寫入媒體的另一份資料。'))
    n([26,27,28,53,54,55,56,61,62,63,70,71,72,73,77,78,79,82,83,84,85,88], 'io-range', '從命令欄位還原一筆完整 I/O',
      '先合成起始 LBA、解出實際區塊數，再檢查範圍、格式與處理選項。CDW13 的解讀方式會因 CETYPE 等選擇而改變。',
      ('CDW10／CDW11 → SLBA；NLB','兩個 Dwords 合成起點；NLB 是區塊數減 1，終點為 SLBA+NLB。','SLBA=100、NLB=7 表示 LBA 100–107，共 8 blocks。'),
      ('LR／FUA／PRINFO／STC','分別影響錯誤恢復、持久化相關行為及 PI 檢查；保留各自適用條件。','設定 FUA 不會自動排序另一個 queue 的命令；資料相依仍需主機安排。'),
      ('CETYPE／CEV／DSM／DTYPE／DSPEC','先由命令格式選擇欄位的含義，再讀提示或命令擴充內容。','CETYPE 非零時，不能再把同一 CDW13 位置套成 CETYPE=0 的 DSM hints。'),
      ('DEAC／NSZ／LBACZ','Write Zeroes 的選項與回傳量需結合命令結果解讀。','解除配置、回傳零值與指定範圍確實被處理是不同問題，不能只看 buffer 全零。'))
    n([32,34,35,36,39,40,41,42,43], 'copy', '把多個來源範圍依序接到目的地',
      'Copy 的 DPTR 指向來源描述子；SDLBA 是目的起點。每個描述子先選來源 namespace 與範圍，再把各段長度依序累加到目的位置。',
      ('DESFMT／NR／DPTR','DESFMT 決定描述子版型，NR 是描述子數量減 1，DPTR 給清單位置。','NR=1 代表兩個描述子；格式不同時，不能沿用同一個描述子長度解析清單。'),
      ('SNSID／SLBA／NLB → SDLBA','來源可由描述子選 namespace；各段實際長度決定下一段目的位置。','第一段 3 blocks、第二段 2 blocks、SDLBA=100，目的依序是 100–102 與 103–104。'),
      ('FCO／能力與命令專屬狀態','快速複製要求需要支援與資源條件；相關錯誤指出哪個要求未成立。','Fast Copy Not Possible 與來源範圍重疊是不同條件，不能只稱為「Copy 不支援」。'),
      ('PRINFOR／PRINFOW／STCR／STCW','兩端保護資訊處理分開選擇，再對照來源與目的格式。','目的位置改變時，要重新檢查 Reference Tag 的生成與檢查方式。'))
    n([44,45,46,47,48,49], 'dsm', '清單數量、範圍長度與使用提示各有單位',
      'Dataset Management 傳入一份範圍清單。命令選共同動作，描述子給個別範圍及用途提示；不同欄位的數量編碼不能互相套用。',
      ('DPTR／NR／AD／IDW／IDR','DPTR 指清單，NR 是描述子數減 1；其他 bits 指解除配置或完整讀寫等屬性。','NR=1 需要兩個範圍描述子，但每段涵蓋多少 blocks 要另讀描述子。'),
      ('SLBA／LLB／CATTR','SLBA 是起點，LLB 直接表示 logical blocks 數；CATTR 是該範圍的上下文屬性。','LLB=8 表示 8 blocks，不能套用一般 Read 的 NLB+1 規則變成 9。'),
      ('CASZE／WPREP／SWR／SRR／AL／AF','是存取大小、讀寫方式與頻率等提示；不是實際讀寫完成結果。','提示順序讀取，不會替主機執行 Read，也不能當成所有後續 I/O 的強制排序。'))
    n([90,99,100,110,111,112,113,114,115,116,135,136,137,138,139,140,142,143,144], 'status-log', '狀態紀錄中的範圍、有效性與後續查詢',
      '先辨認紀錄種類與對象，再使用相應的有效性、數量及範圍欄位。通知資料可能只提供查詢起點，完整狀態需要後續命令取得。',
      ('FLBA／FLBA Valid；LBA／LBAV／NLBAM','不同紀錄對失敗位置或重配置範圍有各自有效性與數量規則。','Self-test 的 FLBA Valid=0 時忽略 FLBA；有效時也只指出一個失敗 block，不是完整錯誤列表。'),
      ('LSLPLEN／NLSLNE／NEID／NLRD／RATYPE','外層給 log 長度與 namespace 元素數，內層再給對象及範圍描述子數。','不能把 NLSLNE 當成 LBA 數；每個 namespace 元素仍需讀自己的範圍清單。'),
      ('RSLBA／RNLB；SLBA／RL／ATYPE／MNDW','log 給建議查詢範圍，Get LBA Status 選行為與回傳空間限制。','收到範圍後，依剩餘範圍與可接收長度安排查詢，不能假設一次回覆必定涵蓋全部。'),
      ('NLSD／CMPC／DSLBA／NLB／LBARS','數量決定有效描述子，完成條件決定是否還需查詢，描述子指出範圍狀態。','先看 CMPC 再判斷查詢是否完整；有一筆描述子不代表其餘 LBA 都無問題。'),
      ('LBASIN／RLCCN／LSIPI／LSIRI／LSGC','事件設定、產生或回報間隔與 generation 各司其職。','更新設定不代表立刻產生一份完整新 log；讀取時仍要辨認版本與有效範圍。'))
    n([91,101,122,123,125,127,128,129,130,131,192,193], 'format-identify', '把目前格式、候選格式與能力連起來',
      '先用 CNS 及對象識別選回覆結構，再由 Format Index 配對格式資料。基本 Identify、命令集專屬 Identify 與延伸格式共同決定合法設定。',
      ('CNS／NSID／CSI／CNTID／FIDX','分別選結構、namespace、命令集、控制器與候選格式；依 CNS 定義決定哪些有效。','查目前格式與查尚未使用的候選格式，是不同查詢，不能把兩份資料當成同一現況。'),
      ('FLBAS／NLBAF／NULBAF／LBAF／ELBAF','先解出有效格式清單，再沿同一 Format Index 配對基本與延伸欄位。','FLBAS 選中 index 2 時，應讀同一 index 的 LBAF 與 ELBAF，不把數值 2 當成每 block 2 bytes。'),
      ('LBADS／MS／RP；PIF／QPIF／STS','資料大小為 2^LBADS bytes；MS 給 metadata 大小；延伸欄位補上保護格式與 tag 寬度。','LBADS=12、MS=16 表示 4096 bytes 資料及 16 bytes metadata，接著依 PI 格式計算 tag。'),
      ('MC／DPC／DPS／PIC／PIFA／LBAFEE','能力描述可選項，目前設定與主機宣告決定真正使用哪種配置。','控制器支援延伸 PI，不代表主機在未宣告相應能力時就可直接建立該格式。'),
      ('VSL／WZSL／WUSL／DMRL／DMRSL／DMSL／WZDSL','各自限制不同命令的長度、描述子數或處理量，先辨認目標命令與單位。','Copy 的來源範圍限制不能拿來當 Write Zeroes 的單筆長度限制。'),
      ('NSZE／NCAP／NUSE；NSFEAT／DLFEAT','容量量與能力、解除配置後讀取行為共同描述 namespace。','NUSE=600 不代表只有 LBA 0–599 有資料；配置可以分散在整個有效範圍。'))
    n([132,133,134], 'namespace-create', '建立設定需同時符合格式與容量規則',
      '先選格式，再換算 NSZE、NCAP，配對粒度描述子，最後檢查資料保護及啟用中的 FDP 設定。粒度是配置效率提示，其他合法性要求仍需獨立滿足。',
      ('NGA.GDM／ND／NGD → NSG／NCG','GDM 決定格式到描述子的對應，ND 是描述子數減 1；NSG、NCG 以 bytes 給建議粒度。','NSZE=250、每 block 4096 bytes 是 1000 KiB；與 1 MiB 粒度比較前，先統一單位。'),
      ('NSZE／NCAP／FLBAS／DPS／NMIC','容量、格式、保護與共享設定共同形成新 namespace。','NCAP 的 byte 值依 FLBAS 選中的資料大小換算；不能另用另一個格式的 block size。'),
      ('ANAGRPID／NVMSETID／ENDGID','說明資源歸屬；零值及不支援時的處理需依各欄位規則。','FDP 在指定 Endurance Group 啟用時，還須遵守其與 NVM Set 的限制。'),
      ('LBSTM／LBAFEE／格式能力','主機提供的 Storage Tag mask 與延伸格式設定需符合 Identify 及 Host Behavior Support。','不能只因容量夠就忽略不相容的 PI 或遮罩設定。'),
      ('NPHNDLS／Placement Handle List／RUH','數量決定清單有效項目，清單把 Placement Handle 對應到 Reclaim Unit Handle。','NPHNDLS=0 由控制器依規則選 handle；非零清單需檢查範圍、重複值與共享格式一致性。'))
    n([94,95,96,97], 'basic-features', 'Feature 的選擇值與功能資料分開解讀',
      'Get 或 Set Features 選定功能後，才依該功能的 buffer、命令 Dword 或 CQE 解釋回覆。',
      ('NUM／Type／ATTRB／SLBA／NLB／GUID','LBA Range Type 的數量選擇與每個範圍的類型、範圍、識別分開。','先解出有效項目數，再逐項檢查範圍，不能只讀第一個項目代表所有 LBAs。'),
      ('DULBE／TLER','Error Recovery 的解除配置讀取錯誤選擇與恢復時間限制各自影響行為。','開啟 DULBE 後，解除配置 LBA 的讀取結果要依相應規則判斷；TLER 不是 buffer 傳輸長度。'))
    n([102,103,104,105], 'performance', '效能屬性先辨認種類與長度',
      '先選 PAID 或屬性查詢，再依標準或廠商格式解釋資料。支援清單與實際效能值使用不同結構。',
      ('ATTRI／RVSPA／PAID／ATTRTYP','選想讀的屬性，並辨認它屬標準或廠商種類。','PAID 是識別碼，不是延遲數值；先選中屬性才能知道回覆的單位。'),
      ('MSVSPA／USVSPA／ATTRL／VS','清單支援與資料長度決定可讀範圍；廠商 payload 需要相應格式。','ATTRL 限定屬性資料大小，不代表其中每個 byte 都有標準定義。'),
      ('R4KARL','標準屬性以指定的存取條件描述延遲。','比較兩個結果前先確認都是相同 4 KiB 隨機讀條件，不能直接套用到任意 workload。'))
    n([106,107,108,117,118,119,120,121,195,196,197,198,202], 'rate', '限制設定與共享資源圖一起判讀',
      '先沿 port、controller、儲存媒體存取描述子的關係找到受限對象，再用模式與比例把欄位換成可比較的速率。',
      ('TGT／TID／RLE／RLM','前兩者選目標，後兩者選啟用與模式；不同模式下的數值可能表示限制或相對權重。','權重 2 不等於 2 MiB/s；必須先確認 RLM 再做解釋。'),
      ('BWSF／MBSF／ABWSF；TBWV／WBWV／TIOPS／WIOPS','頻寬值先搭配比例，IOPS 則是操作數速率；總量與寫入量分別限制。','4 KiB 的 1000 IOPS 對應 4,096,000 bytes/s；換成 128 KiB I/O 後，相同 IOPS 需要不同頻寬。'),
      ('NP／NC／NNSMAD／LPL／offsets／GC','數量、長度與位移描述變長資料結構，GC 協助辨認版本。','offset 以 Dwords 表示時先乘 4，再與 LPL 換成相同單位做範圍檢查。'),
      ('PORTID／CNTLID／SC／SI／RLMA','識別 port、控制器及存取範圍，並連到最大可用量描述。','兩個 port 指向同一 Endurance Group 時，不能將共享的最大容量或速率重複當成兩份獨立資源。'),
      ('Token supply／消耗／等待','權杖累積與每筆命令消耗決定何時可執行；內部資源仍可能造成額外等待。','有足夠權杖表示通過速率限制，不代表其他資源也立即可用。'))
    n([124,145,147,148,149,150,151,152], 'alignment', '起點對齊、長度粒度與邊界是三次判斷',
      '先依對齊偏移找到合法或建議起點，再以粒度檢查長度，最後看是否跨越相關邊界。欄位若只是效能提示，不能提高成命令必須遵守的要求。',
      ('NPWA／NPWG；NPRA／NPRG','分別對應寫入與讀取的起點對齊及粒度，保留各欄位的數量編碼規則。','長度是粒度整數倍，但起點偏移一個 block，仍可能未符合對齊提示。'),
      ('NPDG／NPDGL／NPDAL／NOWS／NORS','解除配置與最佳讀寫大小分別有自己的提示或限制，先辨認動作再使用。','讀取的最佳大小不能直接當成解除配置描述子的最大範圍。'),
      ('NOIOB／NABO／NABSN；SWS／SGS','I/O 邊界、原子邊界與串流大小是不同維度。','即使寫入符合 NPWG，仍需另查是否跨過要保證的原子邊界。'))
    n([158,160,161,162,163], 'crc', '輸入 bytes、位元順序與 CRC 參數共同決定結果',
      '先確定要計算哪些資料及 metadata，再套用指定多項式、初值、反射與最後 XOR；相同多項式不保證得到相同 CRC。',
      ('Width／Poly／Init／RefIn／RefOut／XorOut','完整參數組決定演算法；檢查時還需確認輸入與輸出表示方式。','改變 RefIn 卻沿用原本測試值，結果不同不表示資料本身改變。'),
      ('F(x)／G(x)／R(x)','分別描述訊息、多項式及餘數等數學關係；與實際 byte 順序配合。','先把輸入資料順序固定，再將數學表示對回執行步驟。'),
      ('Zero／FF／遞增 bytes 測試向量','每種向量固定資料長度與每個 byte 的內容，適合驗證完整參數組。','4 KiB 的全零向量不等於空輸入；長度也會影響 CRC。'))
    n([21], 'fdp', 'Placement Handle 如何對應到回收資源',
      '先由主機使用的 Placement Identifier 找到 Reclaim Unit Handle，再解釋該 handle 的狀態與可用資訊。',
      ('PID／RUHID','前者選資料放置，後者識別相應回收資源；需要查映射才能互相連接。','PID 的數字不一定等於 RUHID，不能以相同數值直接配對。'),
      ('EARUTR／RUAMW','分別提供該 handle 的時間與可寫量資訊，按來源單位解讀。','可寫量不能換成剩餘時間，除非另外有已知的寫入速率與適用假設。'))
    n([183,184,185,186,187,188,189,190,191], 'reference-model', '用參考組態理解狀態如何被描述',
      '這組圖是規格定義的參考組態及狀態資料。區分固定模型值、可配置值與目前狀態，才能知道哪些值應帶入後續命令解讀。',
      ('CSS／TO／CQR／MQES；MJR／MNR／TER','能力與版本值限定參考模型所描述的行為。','MQES 的編碼需要按佇列大小規則解讀，不能當成實際已建立的 queue 數量。'),
      ('NSZE／NCAP／LBAF／AWUN／NAWUN／NGUID／UUID','分別描述容量、格式、原子性與物件識別，保留控制器與 namespace 層級差異。','複製一個 namespace 的格式設定，不會讓新物件自動取得相同身分。'),
      ('NCQS／NSQS／Feature values／CSATTR.CP','佇列與 Feature 狀態描述目前或參考設定，需與支援能力分開。','支援的 queue 上限與當前設定的 queue 數量不是同一個欄位。'))
    n([194], 'migration', '一筆變更紀錄如何描述來源與目的範圍',
      '先讀 entry 類型，再用 NSID、SLBA 與 NLB 找到受影響範圍；其他欄位依此類型指出資料或儲存位置關係。',
      ('NSID／SLBA／NLB','命名 namespace 與 logical block 範圍；數量依 entry 定義解讀。','同一個 SLBA 放在不同 NSID 下，是不同資料範圍。'),
      ('LBACIR／DLBA／ESA／CDQP','提供內容或目的位置等資訊，哪些欄位有效由 entry 類型及旗標決定。','沒有對應有效條件時，不能把殘留的 DLBA 直接當成這次資料的新位置。'))
    n([201], 'sanitize-data', '清除後讀值要結合所用方法與配置狀態',
      '先確認清除方法及操作完成，再依是否解除配置、資料格式與命令選项解釋後續讀取。',
      ('Block Erase／Crypto Erase／Overwrite','各方法對 user data 的處理不同，完成保證及後續讀值按相應列判斷。','Overwrite 的樣式與 Block Erase 的讀值不可直接交換解釋。'),
      ('Data／Metadata／PI／解除配置','資料與保護資訊可能有不同處理條件；解除配置也會影響讀取行為。','讀到零值只是一次讀取結果，還需要狀態紀錄證明清除作業已完成。'))
