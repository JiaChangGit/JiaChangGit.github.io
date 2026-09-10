"""Independent takeaways and scenarios for the included Base figures."""
DATA = '''
1|規格家族把共同機制、傳輸與命令語意分工定義。|追一筆 PCIe Read 時，Base 回答命令長什麼樣，PCIe Transport 回答如何傳遞，NVM Command Set 回答讀取的資料與保護行為。
2|十進位與二進位容量前綴使用不同倍率。|1 MB＝1000000 bytes，1 MiB＝1048576 bytes；數字都寫 1，容量仍不相同。
3|Byte、Word、Dword 是不同大小的單位。|64-byte SQE 有 16 個 Dwords；CDW10 的起點在 10×4＝40 bytes，不是 byte 10。
5|Admin 與 I/O Command Set 分別管理裝置與操作 namespace 資料。|建立 I/O queue 是管理工作；對 namespace 發出 Read 則屬資料操作。兩者共用命令機制，但用途不同。
6|一對一佇列映射讓一個 SQ 的結果送到指定 CQ。|SQ1 送出的兩筆命令都回到 CQ1；結果出現順序仍不一定等於提交順序，需要用識別資訊配對。
7|多個 SQ 可以把完成結果送到同一個 CQ。|SQ1 與 SQ2 的 CID 都可有值 5；共用 CQ 收到結果時，必須連同 SQID 判斷結果屬於哪一筆。
11|簡單 NVM Set 階層把 namespace 與容量集合放在同一張關係圖。|沿一個 namespace 向上追所屬的 NVM Set 與 Endurance Group，就能指出容量和耐久度管理各位於哪一層。
12|一個 Reclaim Group 可以提供資料回收所使用的資源。|選一個 namespace 的資料放置位置，沿圖找所使用的回收群組；namespace 名稱與回收單位不是一對一同義詞。
13|多個 Reclaim Groups 讓放置位置需要同時辨識群組。|同樣的回收單位編號放在不同群組中，不應直接當成同一個位置；沿群組與單位兩層讀圖。
14|較複雜的 NVM Set 階層展示多個容量集合如何共存。|先選定一個 Endurance Group，再比較其中的 NVM Sets；不要把圖上並列的所有集合都當成同一份可互換容量。
15|多個回收群組與其他儲存層級需要分別追蹤。|先從要管理的 namespace 出發，依圖追到放置與回收資源；只看方塊距離不能推論共享或包含關係。
16|單一 namespace 的例子把控制器介面與儲存空間分開。|主機透過控制器存取 namespace，即使兩者各只有一個，也不代表控制器就是 namespace。
17|兩個 namespace 可以經由同一套裝置介面提供不同儲存空間。|主機選 NSID 1 或 2 會指向不同 namespace，不是切換同一 namespace 裡的兩個檔案。
18|複雜 subsystem 圖用來追蹤控制器、連接埠與 namespace 的關係。|選一個 host 要用的 namespace，沿線確認可經哪些控制器到達；不是圖中每個控制器都必然連到每個 namespace。
19|同一控制器可以讓主機存取兩個 namespace。|Read 的命令機制相同，但 NSID 不同會選到不同容量與格式；不能沿用另一個 namespace 的 LBA 大小。
20|兩個控制器可以共用一個連接埠。|主機看到兩個控制器時，不應直接推論存在兩條實體連線；圖將介面物件數與 port 數分開。
21|兩個連接埠提供與單一 port 不同的連接關係。|與 Figure 20 比較時，先保留控制器數相同，再觀察 port 由 1 變 2，理解路徑結構到底改變在哪裡。
22|SR-IOV 把 PCIe Function 與控制器介面對應起來。|作業系統使用不同 Function 時，仍需辨識各自的控制器與資源關係；多個 Function 不表示有多套獨立 NAND。
23|控制器類型決定它以資料 I/O 或管理為主要角色。|I/O controller 可以處理 namespace 資料命令；Administrative controller 有管理用途，但不能因此推論也可執行一般 Read。
24|多個 I/O controllers 讓同一 subsystem 提供多個資料介面。|對圖中的某個 namespace，分別追查每個控制器是否附加它；控制器都屬於同一 subsystem，仍可能有不同可存取範圍。
25|管理控制器與 I/O controllers 可以分工共存。|管理程式使用 Administrative controller 取得管理資訊，資料路徑則使用 I/O controller；先說明角色，再介紹各自命令。
26|只有 Administrative controller 的配置仍是管理介面。|即使主機能送出 Admin command，也不能推論這個介面已提供一般 namespace Read／Write 路徑。
27|部分 Controller ID 值有特殊用途，不能視為普通控制器編號。|在控制器清單看到接近 FFFFh 的值時，先依這張表查用途；不要直接把它當成裝置上真的有第 65535 個控制器。
28|Admin 命令支援要求需要連同表格註腳閱讀。|某列為 optional 且帶條件註記時，先確認條件是否成立，再查 Identify 能力；表內列出命令並不表示裝置已實作。
30|共通 I/O 命令的要求與個別命令集能力一起決定可用操作。|使用與資料放置有關的操作前，先看支援要求，再查相應功能是否存在，不以操作碼表取代能力判斷。
31|Log Page 支援表描述哪些紀錄在何種條件下需要提供。|一個健康狀態 log 與一個選用功能 log，可能有不同支援要求；先看列與註腳，再選要讀的 LID。
32|Feature 支援表區分功能存在、控制器類型與附加條件。|某 Feature 在 I/O controller 有條件支援，並不代表在管理控制器也有相同作用範圍。
33|Property 總表提供各暫存器的位置與存取概要。|要讀 CSTS，先在總表找到 offset，再到 CSTS 欄位表解釋 RDY；總表與欄位表回答不同層次的問題。
34|記憶體介面的 property 空間也包含依 stride 排列的 doorbells。|QID 改變時，doorbell offset 依 CAP.DSTRD 推進；不能把所有佇列都寫入同一個固定暫存器位置。
36|CAP 描述控制器能力，主機設定必須落在其支援範圍。|設定記憶體頁大小前，先比對 MPSMIN 與 MPSMAX；主機偏好的頁大小不一定就是控制器接受的大小。
37|版本描述子由主版、次版與修訂版組成。|MJR＝2、MNR＝4、TER＝0 組成版本 2.4.0；三個欄位不應當成單一十進位流水號。
38|版本 property 的 reset 值對應規格版本的編碼方式。|對照 Version property 與版本描述表時，先拆開各欄位再比較，不能只比字串長度。
39|INTMS 以寫入位元來設定中斷遮罩。|要遮罩某個向量，寫入它對應的 bit；讀寫這種 set 寄存器的語意，不等同把整個遮罩暫存器覆寫成相同數值。
40|INTMC 用來清除對應中斷遮罩位元。|解除上一張圖所設定的遮罩時，使用 clear 語意的位元；不能因名稱相近就將 INTMS 的寫入當成解除操作。
41|CC 是主機選擇控制器運作設定的地方。|完成佇列與格式設定後設 EN＝1；是否已能正常使用，還要到 CSTS 看 RDY，不能只讀回 EN。
42|CSTS 回報控制器目前狀態，不是主機的設定要求。|CC.EN 已是 1、CSTS.RDY 仍是 0，表示主機已要求啟用但控制器尚未回報 ready；兩者並不矛盾。
43|NSSR 觸發的是 subsystem 層級重設。|若多個控制器屬於同一 subsystem，評估 NSSR 時要考慮整體影響，不能把它當成單一 I/O queue 的重設。
44|AQA 分別設定 Admin SQ 與 CQ 的項目數。|ASQS＝63 表示 64 個 SQ entries；ACQS 有自己的欄位，不能直接以 SQ 長度取代 CQ 長度。
45|ASQ 保存 Admin Submission Queue 的主機記憶體基底位址。|命令從這個位址開始按 entry 大小排列；ASQ 不是下一筆命令的 CID，也不會隨每次提交而改成 tail 值。
46|ACQ 保存 Admin Completion Queue 的主機記憶體基底位址。|主機讀完成項目時，在 ACQ 所指環形空間依 head 前進；更新 head 不等於修改 ACQ 基底。
47|CMBLOC 說明控制器記憶體 buffer 映射到哪個 BAR 及位置。|主機必須先找到該 BAR 的實際位址，再按 CMBLOC 定位；欄位中的 BAR 編號不是主機可直接讀寫的實體位址。
48|CMBSZ 同時描述 CMB 大小與允許用途。|看到 CMB 有足夠容量，仍要查 SQS、CQS 等用途 bits；大小足夠不代表可以任意把 SQ、CQ 或資料都放進去。
49|BPINFO 把啟用分割區、讀取狀態與大小放在一起回報。|主機要求讀 Partition 1 後，BRS 用來觀察讀取狀態；ABPID 仍是啟用分割區資訊，不能拿它替代此次讀取選擇。
50|BPRSEL 指定 Boot Partition 讀取的目標、起点與長度。|要讀 Partition 1 的一段資料，BPID 選 1，BPROF 與 BPRSZ 按欄位單位設定；三者合起來才是一個完整讀取範圍。
51|BPMBL 提供接收 Boot Partition 資料的主機記憶體位置。|BPRSEL 選的是裝置上的來源區段，BPMBL 選的是主機目的 buffer；相同的數字在兩處代表不同位址空間。
52|CMBMSC 控制 CMB 記憶體空間的映射與啟用。|選好 CBA 後，仍要依 CRE、CMSE 的規則啟用；提供一個非零位址不等於控制器已接受映射。
53|CMBSTS 回報 CMB 位址設定是否被判為無效。|設定 CMBMSC 後若 CBAI 表示位址不合法，就不能只因 CBA 已寫入而認定這塊記憶體可用。
54|CMBEBS 用大小與單位描述彈性緩衝能力。|兩個裝置報同樣數值、卻使用不同 CMBSZU 時，實際 bytes 不同；先換算再比較可吸收的資料量。
55|CMBSWTP 描述 CMB 可持續接收寫入的能力。|短時間寫入能被 buffer 吸收，不代表長時間速率也相同；將這張表的 sustained throughput 與前一張 buffer 大小分開理解。
56|NSSD 用於要求 NVM subsystem shutdown。|單一控制器的 CC.SHN 與 subsystem 的 NSSD 影響對象不同；先決定要關閉哪一層，再使用相應機制。
57|CRTO 為不同 ready 模式提供等待時間資訊。|若選擇不同 CC.CRIME 模式，主機需配合對應 timeout；不能永遠只用一個固定等待時間。
58|PMRCAP 描述 Persistent Memory Region 的支援、映射與時間參數。|打算使用 PMR 前，先確認支援的讀寫與記憶體映射方式，再解 timeout 單位，不從暫存器存在推論所有能力皆可用。
59|PMRCTL 的 EN 是啟用 PMR 的要求。|設 EN＝1 後，仍需觀察 PMRSTS.NRDY；與控制器啟用相同，提出要求與可用狀態分別由不同欄位表達。
60|PMRSTS 回報 PMR 是否 ready 及是否有錯誤。|NRDY 尚未清除時，主機不能把已設定 EN 當成可正常使用的唯一依據。
61|PMREBS 描述 PMR 彈性緩衝大小。|換算 PMRSZU 與大小值後得到可緩衝 bytes，再與預計的突發資料量比較；它不是持續頻寬數值。
62|PMRSWTP 描述 PMR 持續寫入吞吐量。|相同 buffer 大小的兩個 PMR，若持續吞吐量不同，在長時間寫入下仍會有不同表現。
63|PMRMSCL 保存 PMR 映射位址的低部與控制欄位。|組合 CBA 時要把控制 bits 與位址 bits 分開；不能把整個暫存器原值直接當成完整實體位址。
64|PMRMSCU 補齊 PMR 映射位址的高部。|主機位址超過低 32-bit 可表示範圍時，必須連同高部合併；只讀低部會指向另一個位置。
65|有效 NSID 還要區分是否已配置及是否附加到控制器。|NSID 3 在有效範圍內卻尚未建立 namespace 時屬 unallocated；已建立但未附加到控制器 A 時，對 A 仍是 inactive。
66|NSID 分類圖把數值範圍、配置狀態與附加關係分成不同層。|若 NN＝8，NSID 9 屬 invalid；NSID 3 可能 valid 但 inactive。兩者都不能直接作正常資料存取，原因卻不同。
67|namespace 與 NVM Set 的對應說明容量集合的歸屬。|選一個 namespace 沿圖找到 NVM Set，再看相鄰 namespace 是否同屬該集合，不能只用 NSID 相近推論關係。
68|NVM Set aware 命令需要理解其集合層級作用範圍。|命令作用於某個 NVM Set 時，先辨識該集合包含的 namespace；不要以單一 NSID 的效果代表全部集合。
69|另一種 NVM Set 配置用來比較 namespace 如何分布。|把 Figure 67 與這張圖的 namespace 歸屬並排看，重點是關係改變，而不是方塊畫得比較大就有較多容量。
70|FDP 邏輯視圖把資料放置與回收資源分開表達。|主機選擇放置識別碼後，沿圖追到對應回收群組和資源；namespace 的 LBA 不會因此直接變成 NAND 實體位址。
71|Domain 圖說明 subsystem 內可分開考慮的範圍。|某個 domain 的事件或資源資訊，不能直接當成其他 domain 同步發生；先沿圖確認物件所屬。
73|環形佇列的空狀態由 head 與 tail 的關係判斷。|主機尚未提交新命令時 head 與 tail 相等；相等代表沒有待處理項目，不是表示 buffer 的所有 bytes 都是零。
74|環形佇列的滿狀態需要保留可辨識空、滿的配置。|在只能容納下一筆之前檢查 tail 再前進是否追上 head；不能因實體 buffer 還有某些舊資料就認為仍有空位。
80|Round Robin 仲裁輪流給各 SQ 取得服務的機會。|SQ1 持續有命令、SQ2 只有少量命令時，按圖追每次輪到哪個 queue；仲裁選擇與命令完成先後仍是不同事情。
81|Weighted Round Robin 依優先類別與權重分配服務機會。|提高某類 queue 權重會影響仲裁分配，但不能把它解釋成每一筆命令都有獨立 priority 欄位。
84|部分 Admin 命令在媒體尚未 ready 時有特定回覆規則。|控制器介面 ready 與媒體能處理某種命令可能是不同階段；先看 ready 模式，再查這張表對該命令的規定。
85|Shutdown 圖把主機要求與控制器處理的互動串起來。|主機提出 shutdown 後，沿狀態回報等待完成，不能把「已送出要求」當成「可以立刻切斷電源」。
86|簡單 subsystem 範例提供容量模型的起始配置。|先固定只有圖中這些元件，再閱讀容量數字；後面更複雜的配置會增加層級，不能沿用一個總量代表每層。
87|垂直組織的範例強調沿層級追蹤容量。|從 namespace 向上追到集合和 subsystem，逐層確認數值代表配置量還是可用量，不直接把不同層的欄位相減。
88|雙 NAND 配置展示不同儲存資源如何組成 subsystem。|圖中有兩組 NAND，不代表對主機一定呈現兩個相同大小的 namespace；先追實際對應關係。
89|容量欄位的意義取決於 subsystem 或 Endurance Group 層級。|TNVMCAP 與 UNVMCAP 描述整體容量及未配置量；要比較某個 Endurance Group，則使用相應群組欄位。
90|Keep Alive timeout 的偵測延遲受計時觀察時點影響。|一次更新剛好落在計時檢查前後，可能造成不同的偵測時刻；圖說明為何不能把 KATT 直接當成精確偵測時間。
91|Privileged action 可能影響其他控制器或主機使用的狀態。|韌體切換或 namespace 配置變更不一定只影響送出命令的程序；先確認作用範圍，再談協調需求。
92|CDW0 把操作碼、資料指標類型、融合設定與命令識別放在一起。|兩筆命令 OPC 相同但 CID 不同，代表相同操作的兩個請求；不能把 CID 當成操作種類。
93|共通 SQE 固定各命令共用欄位的位置。|同樣在 CDW10，Read 與管理命令可以有完全不同含義；先依 OPC 選命令，再查專屬欄位表。
94|廠商命令格式另以 NDT、NDM 表達傳輸長度資訊。|若依欄位定義 NDT＝16 個 Dwords，資料長度為 64 bytes；此值不能套用別的命令從零起算的加 1 規則。
97|CQE 把命令結果、佇列資訊與識別碼組成完成紀錄。|先用 SQID 與 CID 找回原命令，再解 status 與命令專屬結果；DW0 並非每種命令都代表相同東西。
98|CQE DW2 回報來源 SQ 與該 SQ 的 head 資訊。|SQID 指向 SQ2、SQHD 已前進時，主機可理解控制器消耗進度；它不表示其他所有命令都已完成。
99|CQE DW3 同時帶有命令識別碼與完成狀態。|找到 CID 7 的回覆後，仍要讀 STATUS；識別到這筆命令並不等於它成功執行。
101|Status 欄位必須把類型、代碼與附加控制資訊一起解釋。|相同 SC 數值搭配不同 SCT 可以有不同意思；DNR 也不能從 SC 名稱猜出，必須看實際 bit。
102|SCT 先把狀態分成通用、命令專屬等類別。|先看到 SCT＝1，再去查命令專屬狀態；若忽略 SCT 直接在通用表找同值，可能得到錯誤原因。
103|通用狀態表描述跨命令可出現的共同錯誤。|Invalid Field in Command 表示有欄位不符合要求，但哪個欄位仍須回到該命令定義，不是表格會直接告訴你修改哪個 byte。
104|命令專屬狀態表必須和發出命令的種類連用。|Namespace Insufficient Capacity 應連回建立 namespace 所需容量；不能拿它解釋一般 Read 超出 LBA 範圍。
105|I/O Command Set 專屬狀態要再到相應命令集規格解釋。|Base 提供共用分類，NVM Command Set 補上資料操作的具體含義；兩份規格在這裡接續。
107|媒體與資料完整性狀態指出資料讀寫或檢查的結果。|Guard Check Error 與 Compare Failure 都與資料有關，但前者是保護檢查、後者是內容不符，不應用同一句「資料錯誤」帶過。
108|路徑相關狀態描述透過目前控制器到資料的存取情況。|某條路徑不適合存取時，不一定表示 namespace 資料已損毀；要依狀態與可用路徑判斷。
109|Phase Tag 隨 CQ 繞回而改變，幫助辨識新完成項目。|主機把一輪 entries 讀完回到 slot 0 時，期待的 phase 已翻轉，因此舊 CQE 不會被再次當成新結果。
110|PRP entry 是有固定位元配置的記憶體指標。|先按圖取出位址相關位元，再配合頁大小判斷它指向哪一頁；不能把 64-bit entry 當成資料長度。
111|PRP 的頁基底與頁內 offset 共同形成第一段資料位置。|4 KiB 頁、offset＝128 時，第一頁剩餘 4096−128＝3968 bytes；是否需要下一個 PRP 由總長度決定。
112|連續實體頁面仍可用 PRP List 逐頁描述。|三個資料頁位址相鄰，PRP entries 也各指一頁；連續排列不表示可以把三頁壓成一個只含長度的 PRP。
113|不連續實體頁面可由 PRP List 組成連續的傳輸資料。|第一頁在位址 A、第二頁在 B，主機資料順序由 list 順序決定，不要求 A 和 B 的實體位址相鄰。
114|SGL 錯誤條件涵蓋描述子格式與傳輸長度等不同問題。|描述子型別合法但總長度不足，與型別本身不受支援不同；先確定問題出在哪一層。
115|SGL Segment 是一組描述子的容器。|一個 segment 裡可有多個 data descriptors，不能把 segment 的 byte 長度直接當成使用者資料長度。
116|Generic SGL Descriptor 固定型別欄位的位置。|先讀 SGLID 判斷 descriptor 類型，再解其餘 bytes；同一位置在資料描述子與 segment 描述子中指向不同對象。
117|SGL Descriptor Type 決定這個項目描述資料還是另一組描述子。|Data Block 指向資料，Segment 指向描述子清單；把後者當成資料會把清單內容誤作使用者 payload。
118|Descriptor Subtype 進一步限定同一型別的解釋。|主型別相同仍要查看 subtype 是否適用於 PCIe 情境，不只比對 descriptor 第一層分類。
119|Data Block descriptor 用位址與長度描述一段資料。|ADDR 指向主機 buffer、LEN＝4096 表示這段有 4096 bytes；它不同於 PRP 依頁大小隱含覆蓋長度。
120|Bit Bucket descriptor 表示資料流中要丟棄的部分。|只需保留某段 Read 資料時，可依允許規則讓不需要的部分進 bit bucket；LEN 仍要計入整筆資料流的覆蓋範圍。
121|Segment descriptor 指向下一組 SGL 描述子。|LEN 描述下一組 descriptor 占用的 bytes，不能把它當成下一段使用者資料的 bytes。
122|Last Segment descriptor 表示最後一組描述子的連結。|走到最後一組後應按此型別結束後續連結，不因 buffer 後面還有資料就繼續解成另一個 segment。
125|SGL Read 範例把多個 descriptor 串成一筆完整傳輸。|沿箭頭累計每段資料長度，遇到 segment 先走到描述子清單，遇到 data block 才累計使用者資料。
126|整個 subsystem reset 後，Feature 目前值 依保存與預設規則恢復。|重設前暫時修改的 目前值 不一定保留；要看 保存值與預設值 的選擇條件，不能只讀重設前的值。
127|只重設 subsystem 的部分範圍時，Feature 恢復行為可能不同。|將 Figure 126 的全部重設改成部分控制器重設，先確認 Feature scope 是否涵蓋未重設的物件，再沿表判斷 目前值。
128|VID 與 SSVID 分別識別廠商與 subsystem 廠商。|兩台裝置 VID 相同，並不代表 SSVID 或產品配置相同；這些不是 namespace 的唯一識別碼。
129|Serial Number 與 Model Number 是字元資料欄位。|顯示型號時依欄位長度及字元規則處理，不能把固定長度字串讀成一個整數。
130|IEEE OUI 提供識別碼中的組織分配部分。|相同 OUI 的不同裝置仍需要其他位元區分；OUI 本身不是完整裝置唯一識別碼。
131|EUI64 的 MA-L 格式把組織與延伸識別部分分開。|先依圖切開組織部分及廠商分配部分，再理解完整 64-bit 識別碼；不把其中一半當成完整值。
132|OUI 在 EUI64 中有固定的分配位置。|比較兩個 EUI64 時，可先看 OUI 是否相同，再看其餘位元；OUI 相同不代表兩個 namespace 相同。
133|延伸識別欄位補足 EUI64 的個別識別資訊。|同一組織分配的兩個 ID，可以只在延伸部分不同；比較時必須保留全部位元。
134|MA-L 與 WWN 的相似排列不表示它們可以直接互換。|看到相近的十六進位外觀時，仍先辨識格式與分配規則，不只按字串長度判斷識別碼種類。
135|NGUID 提供 namespace 的全域識別資訊。|NSID 可能因配置而改變，辨識是否同一 namespace 時可以依支援情況使用 NGUID；兩者回答不同問題。
136|NGUID 的 OUI 與廠商部分有各自位置。|比較完整 NGUID 時，把組織部分與其餘識別資訊一起保留，不能只用 OUI 當資料庫唯一鍵。
137|NGUID 的欄位排列需要按完整格式解釋。|讀出 128-bit 值後先維持原本 byte 順序，再按圖拆欄位，避免把一個合法 ID 顯示成另一種排列。
138|NGUID 與 WWN 的結構對照用來理解相似處與不同處。|把相似欄位並排看可以幫助定位，但格式標記和完整位元仍要保留，不用 WWN 的欄位解釋直接取代 NGUID。
139|Controller List 先列數量，再列要操作的控制器識別碼。|Attach 到控制器 A 與 B 時，清單含 2 個 Controller IDs；命令 NSID 指 namespace，清單則指定哪些控制器。
140|Namespace List 是識別碼清單，不包含每個 namespace 的全部屬性。|從清單取得 NSID 3 後，還需相應 Identify 資料才能知道它的格式與容量。
142|UTF-8 輸入處理需要區分 byte 序列與字元。|一個中文字通常占多個 bytes；限制 byte 長度時，不能用相同數值當成可容納字元數，也不能截斷字元中間的 bytes。
144|Subsystem Sanitize 期間的 Admin 命令限制依命令與清除狀態而定。|想讀 Boot Partition log 時，先查這一列在目前清除情境是否允許，不把其他 log 的許可套用過來。
145|Namespace Sanitize 對所有控制器的管理操作有共同限制。|清除某個 namespace 時，另一控制器送出的管理操作也可能受影響；限制範圍不只送出清除命令的控制器。
146|與正在清除的 namespace 有關的控制器還有額外限制。|比較附加該 namespace 與未附加它的控制器時，先套用共同限制，再看這張表的條件是否成立。
151|AER 完成的 DW0 指出事件類型、事件資訊與相關 log。|收到通知後，以 AET 分類、AEI 看具體事件，再用 LID 找後續資料；單看 LID 不足以知道發生什麼事。
152|AER 的 DW1 提供事件專用的補充資訊。|同一個 EVNTSP 數值在不同事件中不一定同義；先由 DW0 辨識事件，再按該事件解釋 DW1。
155|Notice 類事件告知主機有狀態或配置變更。|收到 Firmware Activation Starting 通知，表示切換流程開始；要確認目前韌體仍須讀對應狀態及 log，而非把通知當完成證明。
156|I/O Command Set 事件用不同通知區分清除完成與進入驗證。|Entered Media Verification State 與 Sanitize Operation Completed 不是同一事件；前者表示還有驗證階段的存取規則需要遵守。
176|Self-test 的 NSID 選擇測試對象，invalid 與 inactive 分別表示不同問題。|假設 NN＝8，NSID 9 無效；NSID 3 若尚未配置或未附加到此控制器，則為 inactive。0h 在此命令特別表示只測控制器，Host-Initiated Refresh 忽略 NSID。
177|STC 選擇短測試、延伸測試、Refresh、廠商測試或中止。|想執行短測試填 1h，想中止正在執行的測試填 Fh；這個選擇器不是測試目前完成百分比。
178|DSTP 只在廠商自訂 Self-test 情境提供參數。|STC＝Eh 時依廠商定義解釋 DSTP；短測試時不能把 DSTP 當成主機指定的測試秒數。
179|Self-test 命令處理取決於是否已有測試在執行。|沒有測試時送 Abort 可以成功但不新增測試結果；有測試時送 Abort 則會中止並記錄結果，兩種成功有不同效果。
180|Device Self-test in Progress 表示已有測試，新的要求未能開始。|收到此狀態後，先讀目前測試資訊；它不是新測試的通過結果，也不是說裝置的資料一定壞掉。
187|Firmware Commit 的 CA 選動作，FS 或 BPID 指相關目標。|更新 Boot Partition 時先按 CA 選替換或啟用相關動作，再看 BPID；不要把一般 firmware slot 的 FS 當成 boot partition 編號。
188|Firmware Commit 回覆中的旗標描述特定更新偵測結果。|命令完成後，仍應逐個解讀 MUD 等回覆位元；不能用一個非零 DW0 直接推論「韌體版本已切換」。
189|Firmware Commit 狀態區分映像、slot 與需要重設等條件。|回覆需要 reset 的啟用條件，與 Invalid Firmware Image 是不同結果；前者需要安排流程，後者先檢查映像。
190|Firmware Image Download 的 DPTR 指向此次傳入的映像區段。|分兩次傳映像時，第二次 DPTR 可以指另一段主機 buffer；映像內的目的偏移另由 OFST 指定。
191|Firmware Download 的 NUMD 以 Dwords 且從零起算表示長度。|傳入 4096 bytes 時共有 1024 Dwords，NUMD＝1023；若直接填 4096，單位及編碼都會錯。
192|Firmware Download 的 OFST 指定映像中的 Dword 偏移。|接續前面 4096 bytes 的區段，OFST＝1024；它不是主機記憶體位址，也不是接續區段的 byte 長度。
193|Overlapping Range 狀態指出傳入的映像區段發生不允許的重疊。|第一段覆蓋前 4096 bytes，第二段卻又從 byte 2048 開始時，需要按下載規則檢查重疊，不能只核對兩個 buffer 各自長度。
197|Get Features 的 DPTR 是需要資料結構時的回傳位置。|查詢一個會回傳資料 buffer 的 Feature，先準備相應大小的目的空間；不是每個 Feature 都只靠 CQE DW0 回傳全部內容。
198|Get Features 的 FID 選功能，SEL 選要查目前值、預設值等資訊。|查 current 與查 saved 可以回不同內容；兩次 FID 相同不表示查詢完全相同。
199|Get Features 的 UIDX 在使用 UUID 選擇時提供索引。|UIDX 是 UUID List 中的位置，不是把 128-bit UUID 直接塞進命令欄位；使用前先確認該索引對應誰。
200|Get Features 清單列出 FID 與該功能回傳形式。|先由想查的功能找到 FID，再看需要 CQE 結果還是資料結構；不能用上一個 Feature 的接收格式讀下一個。
201|Supported Capabilities 回覆把可修改、namespace 範圍與可保存能力分開。|CHANG 表示可修改，SVBL 表示可保存；支援其中一項，不代表另一項也成立。
202|Get Features 的命令專屬錯誤指出查詢目標等要求不成立。|回覆 Invalid Controller Identifier 時，應確認指定控制器識別碼，不把它解釋成 Feature 數值本身超出範圍。
203|Get Log Page 的 DPTR 指向主機接收 log 資料的空間。|同樣是 512-byte buffer，LID 不同會得到不同結構；DPTR 只提供位置，不會決定 log 類型。
204|Get Log Page 的 CDW10 選擇 log、低位長度及相關控制參數。|讀取 512 bytes 共 128 Dwords，長度原始值為 127；同時填正確 LID，才能知道回來的是哪一份紀錄。
205|CDW11 提供長度高位與 log 特定識別資訊。|NUMDU 非零時總長度需與 NUMDL 合併後再加 1；不能把兩個長度欄位各加 1 再相加。
206|LPOL 是 log offset 的低 32 bits，單位還要看 offset 模式。|byte-offset 模式下讀下一段 512 bytes，LPOL 設 512；index-offset 模式則以項目索引解釋，數字 512 不再表示相同位置。
207|LPOU 補齊較大 log offset 的高 32 bits。|完整 offset＝00000001_00000000h 時，LPOU＝1、LPOL＝0；只讀 LPOL 會誤以為從開頭開始。
208|CDW14 的 CSI、OT、UIDX 決定命令集、offset 模式與相關選擇。|相同 LPOL＝4，在 byte-offset 與 index-offset 下表示不同事物；先看 OT 才能正確解讀位置。
209|LID 清單把紀錄編號與其命令集、範圍連在一起。|先依本篇所需的紀錄選取清單中的對應列，再看 CSI 與作用範圍；編號只選紀錄種類，完整欄位排列仍到該 log 的結構表閱讀。
210|Supported Log Pages 列出裝置實際支援哪些紀錄。|規格定義某個 LID，但裝置沒有支援時，不能把表中定義當成裝置能力；先查支援清單。
211|每個 LID 的支援與效果描述子補上紀錄特性。|LSUPP 表示是否支援，LID-specific parameter 另描述相應特性；不能只看一個 bit 就推論全部參數可用。
213|SMART／Health log 把溫度、健康狀態與累計統計分開回報。|Composite Temperature 與個別感測器溫度不同，HCTM 累計計數又是另一種單位；不能把整張表全部當成即時溫度。
215|Firmware Slot log 以啟用資訊連到各 slot 的韌體版本。|先讀 AFI 所指 slot，再讀對應 FRS；其他 slot 存有映像，不代表它目前已在執行。
218|Self-test log 同時保存目前作業狀態與歷史結果。|目前進度 50% 表示正在執行的測試；最前面的歷史結果可能屬於前一次已結束測試，兩者不要混成同一次結果。
219|Self-test Result 的有效標記決定哪些失敗欄位可以解讀。|先看 VDINFO，再決定 NSID、FLBA 或狀態欄位是否有效；欄位有非零內容不代表它在這次結果中有效。
220|Host-Initiated Telemetry 的參數選擇是否建立新資料及收集範圍。|想分段讀同一份紀錄時，不應每段都要求重新建立，否則可能把不同時間的資料接在一起。
221|Host-Initiated Telemetry header 給出各資料區終點與紀錄版本。|讀完第一段後若 generation 資訊改變，就要重新確認是否仍為同一份紀錄，不能僅按 byte offset 繼續串接。
222|MCDAS 回報主機發起 Telemetry 支援的收集資料區能力。|打算要求較大的資料區前，先查支援能力，再設 MCDA；要求欄位與支援欄位不能互相取代。
223|Controller-Initiated Telemetry 由控制器建立並回報可讀取狀態。|TCDA 表示有相應資料可供取得時，主機還要依 TCDGN 等資訊讀完同一份紀錄並遵守確認規則。
279|Boot Partition log 的參數用 BPID 選要讀的分割區。|同一 LID 配 BPID＝0 或 1 會選到不同 partition；LID 指紀錄種類，BPID 才指此次目標。
280|Boot Partition log 先回報 header，再提供分割區資料。|讀回 buffer 後先找 BPD 的開始位置；不能把 header 內容當成開機映像的第一段 bytes。
304|DNCS 表示目前 namespace 配置是否仍符合韌體預設配置。|還原預設配置成功後 DNCS 設定；後續又建立或刪除 namespace 改變配置時，就不能仍把先前的預設狀態當成現在狀態。
311|Reservation Notification log 描述保留狀態相關通知。|收到通知後先看通知種類與計數，確認是否需要重新讀取保留狀態；通知紀錄本身不是完整使用者資料。
312|Sanitize Status 將進度、狀態與啟動命令資訊放在同一份紀錄。|SPROG 看起來很接近完成時，仍須讀 SSTAT 判斷成功、失敗或其他狀態；不能只以百分比作完成證明。
337|CSI 指定 namespace 使用哪一套 I/O Command Set。|CSI＝00h 對應 NVM Command Set；這個數值不是 NSID，也不是某個 Read 操作碼。
338|Identify Controller 先告知能力與限制，主機再決定可使用的操作。|規格列出某選用命令時，先查相應支援欄位再發出要求；「命令有定義」與「這台控制器支援」是不同證據。
340|Power State Descriptor 同時描述功率、性能特性及進出延遲。|低功率狀態可能有較長 EXLAT；挑選省電狀態時，不能只比較 MP 而忽略下一次 I/O 等待多久。
346|與命令集無關的 Identify Namespace 提供共享、屬性與路徑相關資訊。|先知道某 NSID 對應的 namespace 是否共享，再解釋控制器間的存取關係；LBA 資料大小則仍需命令集專屬格式資訊。
347|UUID List 用索引連到完整 UUID。|命令 UIDX＝2 時，先查第 2 個有效項目；數字 2 不是 UUID 本身，也不是 namespace 編號。
348|UUID List Entry 包含 UUID 與其關聯資訊。|兩個項目即使位元長度相同，仍要讀 IDASSOC 才知道與誰關聯，不直接以出現順序猜用途。
442|Attachment 的 DPTR 指向要附加或分離的控制器清單。|NSID＝3、清單只有控制器 A，表示改變 namespace 3 與 A 的關係，不是建立新的 namespace 3。
443|Attachment 的 SEL 選擇 Attach 或 Detach。|SEL＝0h 建立附加關係，SEL＝1h 移除關係；Detach 不會像 Delete 一樣刪除 namespace 物件。
444|Attachment 狀態描述附加關係、控制器清單與限制是否成立。|「已經附加」與「清單中的控制器不合法」是不同問題；先看是哪一個關係或輸入不符合要求。
445|Namespace Create 的 DPTR 指向 4096-byte 建立資料。|主機想建立新 namespace，將容量和格式放在 payload，DPTR 只提供 payload 的位置；不是提供未來 namespace 的資料位址。
446|CDW10 的 SEL 選擇建立、刪除或還原預設 namespace 配置。|Create 用 SEL＝0h，Delete 用 1h，Restore Default 用 2h；bits 3:0 放選擇值，bits 31:4 保留。Delete 的目標另由 NSID 指定。
447|CDW11 的 CSI 只在 Create 時指定新 namespace 的命令集。|建立 NVM namespace 時，SEL＝0h 且 CSI＝00h；CSI 位於 bits 31:24。Delete 或 Restore 時此欄位保留，不能用來指定 namespace 編號。
448|Create buffer 把命令集專屬資料、保留區與廠商區分開。|bytes 0～511 依所選命令集解釋，512～1023 保留，1024～4095 為廠商區；不能把整個 buffer 都當成連續 LBA 資料。
449|Create 失敗原因可能是格式、容量或識別碼資源，而非同一種空間不足。|還有未配置 bytes，卻已用完允許的 namespace 數量時，仍可能無法建立；NSID Unavailable 與 Insufficient Capacity 要分開。
450|Create 成功後 CQE DW0 回傳控制器分配的新 NSID。|回傳 NSID＝3 表示 namespace 3 已建立，主機還要透過 Attachment 附加到控制器，才能依該控制器的存取路徑使用它。
451|Sanitize 的 SANACT 決定方法，其他參數依方法才有意義。|選 Overwrite 後才解 OWPASS、OIPBP；OWPASS＝0 特別表示 16 輪，不是零輪。換成 Crypto Erase 時不能照搬 overwrite 參數。
452|OVRPAT 指定 Overwrite 使用的 32-bit pattern。|OVRPAT＝A5A5A5A5h 時，還要配合 OIPBP 與輪數判斷各輪是否反相；它不是進度或清除後資料量。
453|啟動 Sanitize 的命令失敗與背景清除失敗是不同階段。|命令因 PMR Enabled 被拒絕時，清除可能尚未開始；背景作業稍後失敗則要讀 Sanitize Status，不能只看啟動 CQE。
454|Sanitize Namespace 的欄位與 subsystem Sanitize 不完全相同。|Namespace 命令的 PREQ 在 bit 4，且不含 subsystem 命令的 Overwrite 參數；不能把同一 CDW10 原值直接換操作碼重送。
463|Set Features 的 DPTR 提供需要傳入的功能資料。|設定 HMB 時傳入描述子相關資料，與單純只在 CDW11 放一個開關不同；先看該 Feature 是否使用資料 buffer。
464|Set Features 的 FID 選功能，SV 表示是否要求保存。|主機要求 SV＝1 前先確認 Feature 可保存；設定成功與重設後仍保留，是需要分別核對的行為。
465|Set Features 的 UIDX 用於相應 UUID 關聯的選擇。|若使用 UUID List 的某一項，先確認索引對應與適用規則；UIDX 不是 Set Features 的新 FID。
466|Set Features 的識別碼清單指引每種功能的專屬欄位。|FID 02h 的 CDW11 是 Power Management，FID 0Ch 的相同位置是 APST；欄位位置相同不表示內容相同。
468|Power Management 的 PS 選狀態，WH 提供工作負載提示。|選 PS 3 前先確認該 power state 存在；WH 描述負載特性，不會替控制器新增一個 PS 3。
470|溫度門檻要同時指定感測器、方向、門檻值與遲滯。|對同一感測器設定高溫門檻與低溫門檻時，THSEL 不同；不能只用一個 TMPTH 數值描述兩種觸發條件。
474|Asynchronous Event Configuration 各 bit 選擇對應的通知類別。|主機啟用本篇需要的通知時，只設定對應的事件 bit；一種通知已啟用，不會自動啟用其他通知。
475|APSTE 控制是否啟用自動 power state 轉換。|主機準備好 APST 表之後才啟用 APSTE；開關本身不包含「閒置多久、轉去哪個 state」的完整策略。
476|APST 表按目前 power state 索引到各自的轉換項目。|有 32 個 entries、每個 8 bytes，共 256 bytes；第 3 個 state 的 entry 不等於「下一個一定轉去 state 3」。
477|APST entry 把閒置等待時間 ITPT 與目標 state ITPS 分開編碼。|ITPT＝2000 ms、ITPS＝3 時，低 Dword 為 (2000<<8)＋(3<<3)＝0007D018h；時間在 bits 31:8，state 在 bits 7:3。
478|APST 與 NOPPME 的互動取決於進入狀態的方式。|主機直接指定非操作狀態，與 APST timer 自動進入同名狀態，可能有不同背景處理規則；按表中進入方式讀對应列。
482|HCTM 用 TMT1 與 TMT2 指定兩個熱管理門檻。|先標出兩個門檻在溫度軸上的順序，再看進入與解除條件；不能把 TMT2 當成第二個感測器編號。
483|NOPPME 控制非操作 power state 下的相應行為許可。|允許某些背景行為，不代表該狀態因此變成一般可處理 I/O 的操作狀態；仍要看 power state 定義。
491|Host Behavior Support 告知控制器主機能處理哪些延伸行為。|裝置支援某功能與主機宣告已能使用它不同；先確認能力，再看主機是否按對應欄位啟用相容行為。
492|Sanitize Config 的 NODRM 控制相應的清除後配置行為。|需要判斷 NDAS 的效果時，連同 NODRM 與 SANICAP 閱讀；不能只看命令中的一個 bit 就推論所有資料是否重新配置。
542|Boot Partition Write Protection Config 分別設定兩個分割區的保護狀態。|Partition 0 鎖定而 Partition 1 未鎖定是可分別描述的配置；不能只用一個「Boot 已鎖」句子忽略目標分割區。
545|HMB 控制欄位分別表示啟用、記憶體返回及相關要求。|EHM 啟用 HMB，MR 涉及先前記憶體返回的情境；兩個 bit 不是「新記憶體地址」與「舊地址」的編碼。
546|HMB 的 HSIZE 以控制器設定的記憶體頁大小計算。|CC.MPS 對應 4096 bytes、HSIZE＝16 時，提供 65536 bytes；HSIZE 不是描述子數量。
547|HMDLLA 提供 HMB 描述子清單位址的低部。|16-byte 對齊的清單位址，其低 4 bits 必為零；這是清單的對齊，不代表每個資料 buffer 只需 16-byte 對齊。
548|HMDLUA 補齊描述子清單位址的高部。|清單位址＝00000001_00001000h 時，高部為 1、低部為 1000h；只設定低部會指到不同記憶體。
549|HMDLEC 指定 HMB 描述子清單包含多少項目。|HMDLEC＝2 表示清單有 2 個 entries；它不直接表示只有 2 個資料頁，因每個 entry 可以描述多頁。
550|HMB Descriptor List 由固定大小 entries 組成。|2 個 16-byte entries 共占 32 bytes；清單本身的大小與它們描述的 HMB 總容量是不同數量。
551|每個 HMB 描述子用基底位址和頁數描述一段記憶體。|BSIZE＝8、頁大小 4 KiB 時，該項描述 32 KiB；BADD 指起點，不能把 BSIZE 當成 byte 長度。
552|HMB 完成回覆中的 HMNAR 要連回此次要求的條件。|收到非零回覆前先確認 HMNARE 與 EHM 的設定；不能把任意 DW0 值都當成實際配置頁數。
553|HMB Attributes 回報目前採用的大小及描述子清單資訊。|讀回 HSIZE、HMDLAL／HMDLAU、HMDLEC 後，可與先前設定分別對照；成功設定命令的 CQE 不包含這份完整屬性表。
561|Track Send 的管理操作由 MO 與操作專屬參數一起決定。|選擇 Log User Data Changes 操作後，MOS 才按其動作欄位解釋，不能將另一種管理操作的參數直接套用。
562|LACT 選擇使用者資料變更紀錄的動作。|要開始或停止某種紀錄行為時，依 LACT 選項處理；它不是變更了多少個 LBA 的計數。
563|CDQID 把變更追蹤操作連到指定的 Controller Data Queue。|先建立並辨識目標 queue，再在命令指定其 ID；CDQID 不表示此次要搬移的 namespace。
679|Boot Partition 圖連起裝置分割區與主機接收 buffer。|沿一次讀取追 Partition 0 或 1 到主機記憶體的資料方向，分清來源、讀取選擇與目的位址。
680|Set Features 保護狀態圖用狀態與轉移說明何時能解除鎖定。|Write Locked 與 Write Locked Until Power Cycle 不能同樣用一般解鎖要求處理；先辨識目前狀態，再沿允許箭頭走。
681|Set Features 保護狀態定義補上 reset 與斷電的影響。|比較 Controller Level Reset 與 power cycle 後的鎖定狀態，不能只說「重開機會解鎖」而不交代是哪一種事件。
682|RPMB 保護狀態圖另外描述認證設定的啟用與鎖定。|RPMB protection 尚未啟用與已啟用但未鎖定，是不同狀態；先分清管理方式，再談是否允許寫入。
683|RPMB 保護狀態定義說明其保存及控制方式。|與 Figure 681 並排比較時，看相同 reset 是否保留同一種狀態，不因兩張表都有 Locked 就當成完全等效。
684|整體 Boot 保護模型說明 Set Features 與 RPMB 狀態如何共同決定結果。|兩種來源的狀態不同時，先按圖判斷目前由哪一套控制關係生效，不能直接把兩個數值取較大者當最終狀態。
700|Self-test 範例示意分段測試與失敗判斷的關係。|沿某一 segment 看測試內容與失敗條件，再看結果如何記錄；此圖是說明性例子，不要求每家控制器都用相同內部測試順序。
701|Format NVM 是否中止 Self-test 取決於作用範圍與格式化條件。|格式化另一個不在測試範圍內的 namespace，不能只憑「有 Format 命令」就推論測試必須中止；按 NSID、SES 等條件交叉查表。
712|Streams 參數分別描述寫入大小與配置粒度。|使用 SWS 規劃一次寫入長度後，仍要看 SGS 的配置關係；兩者不同單位或作用不能混成一個「建議大小」。
738|Power Management 總覽區分主機直接選擇與自動轉換。|工作負載降低時，主機可直接要求 state，或設定 APST 讓閒置條件觸發；兩條路徑需要不同的設定資訊。
739|功耗數值與轉換延遲共同描述 power state 特性。|比較 PS1 與 PS2 時，較省電的狀態若離開延遲更長，下一筆 I/O 的等待成本也要納入說明。
740|Workload Hint 告訴控制器預期負載，並非指定命令排程順序。|WH＝001b 與另一個允許值用來描述不同負載特性；不能把 WH 當成 SQ priority 或保證吞吐量。
741|熱管理圖用溫度門檻與遲滯解釋限速的進出。|溫度剛從門檻上方降回附近時，不一定立刻解除限制；沿遲滯區間讀圖可理解為何狀態不反覆抖動。
756|RPMB Device Configuration Block 保存 Boot 保護的設定資訊。|讀到 protection enable 與 protection state 時要分開理解：啟用管理機制與把特定 partition 鎖定不是同一欄位。
757|RPMB Message Type 分辨不同要求與回覆。|Configuration Block Read 的 request 與 response 使用各自類型值；不能只因都含配置資料就當成相同訊息。
758|RPMB Operation Result 區分認證、計數器等操作結果。|Authentication Failure 表示認證不成立，Counter Failure 則與計數器條件有關；兩者不是不同名稱的同一種失敗。
760|RPMB Data Frame 把訊息類型、nonce、計數器與認證資料分區放置。|讀取回覆時先辨識 Message Type，再檢查該操作需要的 nonce／認證資訊；不能把所有欄位在所有操作中都視為有效。
761|RPMB Key 流程描述認證金鑰設定與結果取得的次序。|先有金鑰設定要求，再讀取相應結果；送出資料的傳輸完成不等於金鑰設定成功。
762|Read Write Counter 流程用 nonce 與認證回覆取得目前計數器。|主機用本次 nonce 對照回覆，確認回覆對應這次要求；僅看到一個較大的 counter 不足以證明回覆新鮮。
765|Authenticated Configuration Write 把計數器、寫入與結果確認串成流程。|主機準備認證寫入後，仍按流程取得 operation result；不能把資料已送達當成保護設定已更新。
766|Authenticated Configuration Read 以本次 nonce 與認證資訊確認讀取結果。|讀到 Boot protection 狀態後，先確認回覆屬於這次要求，再用它判斷是否允許更新分割區。
770|清除範圍隨 subsystem 或 namespace 目標而不同。|清除一個 namespace，不能推論其他 namespace、Boot Partition 或其他列出的區域全部同時被清除；按目標欄逐項看。
771|Overwrite 每輪的 pattern 取決於初值、反相設定與輪數。|初值 A5A5A5A5h、相應反相條件成立時，反相值為 5A5A5A5Ah；依輪次追圖，不能只記最後一次寫入的名稱。
772|Sanitize 狀態圖把處理、失敗、驗證及後續配置分開。|同樣回到可接受命令的情況，可能經成功完成或退出失敗模式；沿箭頭保留原因，不能只看終點名稱。
773|Idle 的離開條件依要求及 AUSE 選擇不同處理路徑。|同一清除方法分別設定 AUSE＝0、1，沿 A1、B1 看進入哪一個 processing state；方法與失敗限制選擇是不同參數。
774|Restricted Processing 的下一步由成功、失敗及驗證條件決定。|清除成功且需要媒體驗證時，沿驗證分支；發生失敗則沿另一條路徑，不把兩者都說成「處理結束」。
775|Restricted Failure 的恢復必須滿足該狀態允許的要求。|失敗後再次要求清除前，先看 A2 的條件；不能按 Idle 的可接受命令清單推論目前也相同。
776|Unrestricted Processing 有自己的成功、失敗與驗證轉移。|與 Figure 774 比較時，把相同清除結果放進兩種狀態，觀察後續限制如何不同，而不是重複背一樣的成功定義。
777|Unrestricted Failure 可以依允許的要求重試或退出失敗模式。|Exit Failure Mode 讓狀態改變，不等於先前失敗的清除突然成功；仍要保留失敗結果的含義。
778|Media Verification 的退出與 reset 有明確轉移條件。|驗證讀取完成後，依允許機制離開；若期間發生 reset，沿對應箭頭看下一狀態，不能假設永遠保留在驗證中。
779|Post-Verification Deallocation 的結果決定最終轉移。|已完成媒體驗證仍可能需要後續 deallocation；觀察 H、I1、I2 的條件，不能在進入此狀態時就宣布整個流程結束。
780|Telemetry 各資料區終點以 Last Block 描述，可由相鄰終點相減得大小。|DA1 最後 block＝65、DA2＝1000 時，DA2 有 1000−65＝935 blocks，即 478720 bytes；不用再加一次 header。
781|未填入的資料區可由相同或零的終點表示。|DA1 終點為 0、DA2 為 1000 時，資料區 2 從 header 後開始，占 1000×512＝512000 bytes；不能憑「第二區」就假設前面一定有第一區資料。
'''
LESSONS = {int(n):{'takeaway':takeaway,'example':example} for n,takeaway,example in (line.split('|') for line in DATA.strip().splitlines())}
