"""Unique figure purposes with shared, focused field teaching."""
EXAMPLES={}
GUIDES={}
MEMBERS={}

def example(number,takeaway,worked,en):
    EXAMPLES[number]=dict(takeaway=takeaway,example=worked,en=en)

def group(key,title,relation,numbers,*rows):
    ident='ege-'+key
    GUIDES[ident]=dict(id=ident,title=title,relation=relation,rows=list(rows),headers=['欄位與位置','讀值時要確認什麼','具體例子與判斷'])
    for n in numbers: MEMBERS[n]=ident

def lesson(figure): return EXAMPLES[int(figure['number'])]
def guide(figure): return GUIDES[MEMBERS[int(figure['number'])]]

example(69,'外層虛線框決定耐用度管理的範圍，Set 內外的未配置容量不可混加。',
 '原圖 Set A、B 都在 Group Y 內，而 Set C 在 Group Z 內。Y 裡、A／B 外的灰色區才是未分給 Set 的容量；A 內的灰色區雖尚未配置給 namespace，仍然已屬於 Set A。',
 'The outer group boundary defines shared endurance management; unallocated capacity inside a set differs from unallocated capacity outside all sets.')
group('containment','從外框讀出容量歸屬','Figure 69 是包含關係示意，顏色與面積不是容量數值，也不是資料移動方向。',[69],
 ('Endurance Group Y／Z','虛線外框各包住一個耐用度管理範圍；每個 Group 只屬於一個 domain。','Y 包含兩個 Set，Z 包含一個；不能據此推論每個 Group 必須相同配置。'),
 ('NVM Set A／B／C 與 NS','實線框內的 NS 是 namespace；同一 Set 的儲存屬於相同 Group。','A1 與 B1 的 namespace 不同，卻都在 Y 的耐用度管理範圍內。'),
 ('Unallocated 的所在位置','Group 內、Set 外：未分給任何 Set；Set 內、NS 外：Set 已取得但尚未分給 namespace。','UEGCAP 對應前者；不可把 A、B 內的灰色空間全部當作 Group 未配置容量。'))

example(338,'支援位元、同時等待的 AER 數與 Group ID 上限分別回答不同問題。',
 '若 EGS=1、EGEAN=1、AERL=3、ENDGIDMAX=9，表示支援相關能力、最多 4 個 AER 同時未完成，以及 Group ID 不超過 9；仍不能宣稱現在有 9 個 Group 或 9 個事件。',
 'Support bits, the outstanding-AER limit and the group-identifier ceiling answer different questions; none is the current pending-event count.')
group('controller','只取本篇需要的 Identify Controller 欄位','Figure 338 很長；以下列出本篇需要的 byte 位置與 bit。其他能力位元不是保留，也不應被本篇的遮罩檢查清除。',[338],
 ('CTRATT bytes 99:96，EGS bit 4','1 表示支援 Endurance Groups。測試這個 bit，不要求整個 CTRATT 等於 10h。','CTRATT=30h 仍包含 EGS；另外的 bit 5 不改變 bit 4 的支援判斷。'),
 ('OAES bytes 95:92，EGEAN bit 14','1 表示支援 Endurance Group Event Aggregate Log Page Change Notices。','OAES 的 00004000h 位元為 1 只表示可支援通知，還要用 FID0Bh 啟用。'),
 ('AERL byte 259','同時未完成 AER 的上限採數量減 1 編碼。','3 還原成 4；不是已經發生 3 個事件，也不是要讀 4 筆清單。'),
 ('ENDGIDMAX bytes 341:340','有效 Group ID 的最大值；實際支援的 Group 數小於或等於此值。','上限 9 可用來預留 8+2×9 bytes 清單內容，不表示 ID1～9 都存在。'),
 ('ONCS bytes 521:520，SSFS bit 4','控制是否支援 Set Features 非零 SV 與 Get Features 非零 SEL。','先確認 SSFS 再使用 SEL=3；支援這個命令欄位，也不代表每個 Feature 都可保存。'))

example(224,'ENDGID 位於 LSI 內，再由 LSI 放進 CDW11 的高 16 bits。',
 '查 Group7：LSI=0007h、NUMDU=0，所以 CDW11=00070000h。Figure 224 的 bits 15:0 是 LSI 內的位置；不能直接把整個 CDW11 填成 00000007h，後者會改到傳輸長度的高半部。',
 'ENDGID occupies the 16-bit LSI, which in turn occupies the upper half of CDW11; the two coordinate systems must not be confused.')
group('selector','兩層欄位座標：LSI 裡的 ID、命令裡的 LSI','Figure 224 定義 LSI 的內容；Figure 205 定義 LSI 在命令中的位置。配合讀一次即可，不必為兩張圖重複解釋同一個 Group。',[224],
 ('LSI bits 15:0 → ENDGID','選擇 LID09h 要回覆哪個 Group 的資料，使用有效且存在的 Group ID。','0007h 選 Group7；不是 namespace 7，也不是清單第 7 筆。'),
 ('CDW11 bits 31:16 → LSI','在命令層級左移 16 bits；低半部保留給 NUMDU。','(7<<16)|0 = 00070000h。'),
 ('固定 512 bytes 的回覆','每次取得的是指定 Group 的資料結構；LID 仍在 CDW10 選 09h。','從 offset0 取完整資料：128 dwords，NUMD=127。RAE=1 的 CDW10 是 007F8009h。'))

example(225,'先分清狀態、估計、累積量與容量，再按每欄的單位解讀。',
 '同一份資料可以同時有 EGCW=05h、PUSED=103、DUW=3、TEGCAP=1,000,000,000。它們依序是警告遮罩、已用壽命百分比、取整的累積寫入量與精確以 bytes 回報的總容量，不能互相代算。',
 'Interpret state, estimates, cumulative activity and capacity separately; adjacent fields do not necessarily share units or zero semantics.')
group('health-fields','完整讀懂 512-byte Endurance Group Information','Figure 225 跨 PDF264～265。先讀前 8 bytes 的狀態，再讀從 byte32 開始的 16-byte 數值。所有 byte 位置都相對本 log 起點；多 byte 整數依低位元組在前的表示方式讀取。',[225],
 ('EGCW byte 0：bits 0／2／3','EGASB：備用容量低於門檻；EGDR：重大媒體或內部錯誤造成可靠度下降；EGRO：整組 namespace 因非寫入保護設定的原因唯讀。','05h=0101b 表示前兩種警告；0Dh 則連唯讀也成立。這是處理讀 log 當時的狀態。'),
 ('EGCW 保留 bits 1、7:4','不是新的可選警告；不得在 FID18h 啟用其對應 mask bit。','0Fh 包含保留 bit1；要選全部已定義警告，使用 0Dh。'),
 ('EGFEAT byte 1，EGRMEDIA bit 0','1 表示資料儲存在旋轉媒體，0 表示不是旋轉媒體；bits 7:1 保留。','它描述媒體種類，不是健康程度，也不是警告 bit。SSD 情境不能把 1 解成「SSD 正常」。'),
 ('AVSP byte 3／AVSPT byte 4','剩餘備用容量與其門檻均為正規化百分比；門檻的 101～255 保留。低於門檻才符合此警告條件。','AVSP8、AVSPT10：8<10；AVSP10 與 AVSPT10 相等，不是低於。'),
 ('PUSED byte 5','廠商估計的生命週期已使用百分比，可超過 100；超過 254 以 255 表示。非 sleep 時每通電小時更新。','103 不表示 103% 儲存空間被佔用，也不自動等於唯讀；255 不能反推精確原始百分比。'),
 ('DID bytes 7:6','Group 所屬 domain 的識別值；支援多 domain 時必須非零，0 表示不支援多 domain。','DID=2、ENDGID=7 同時存在不矛盾：一個選管理範圍，一個選範圍內的 Group。'),
 ('EE bytes 47:32','整個 Group 生命週期可寫入 byte 數的估計，假設 write amplification=1；十億 bytes 向上取整，0 不回報。','EE=1000 是取整後的總壽命估計，不是還可再寫 1000 GB 的保證。'),
 ('DUR bytes 63:48','累積讀取 byte 數，不含控制器內部讀取；十億 bytes 向上取整，0 不回報。','DUR=2 的區間為 1,000,000,001～2,000,000,000 bytes；垃圾回收內部讀取不另加進此欄。'),
 ('DUW bytes 79:64','累積寫入 byte 數，不含控制器內部寫入；十億 bytes 向上取整，0 不回報。','DUW=3 不是 3 個 dword、3 個命令或 3 GiB。'),
 ('MUW bytes 95:80','主機加控制器內部寫入總量；十億 bytes 向上取整，0 不回報。','MUW=5 而 DUW=3 可以反映內部工作量，但取整讓 5/3 不是精確寫入放大率。'),
 ('HRC bytes 111:96','已完成的 Endurance Group Host Read Commands 筆數，成員由所用 I/O Command Set 定義。','1000 代表命令計數，不是 1000 GB；不從這個欄位假設每筆長度相同。'),
 ('HWC bytes 127:112','已完成的 User Data Out Commands 筆數，分類同樣由所用 I/O Command Set 定義。','一筆搬移更多資料的命令仍是一筆，不能要求 HWC 和 DUW 相等。'),
 ('MDIE bytes 143:128','未恢復的資料完整性錯誤次數，例如無法修正的 ECC、CRC 檢查失敗或 LBA tag 不符。','這是累積次數；現在 EGCW 為 0 不會據此把歷史 MDIE 歸零。'),
 ('NEILE bytes 159:144','控制器生命週期內，屬於這個 Group 的 Error Information Log 項目數。','計數值 20 不代表現在的 Error Information log 還保留完整 20 筆，也不等於 MDIE 必須為 20。'),
 ('TEGCAP bytes 175:160','Group 總 NVM 容量，單位是 bytes；0 表示不回報。','1,000,000,000 直接是一十億 bytes，不再乘十億。'),
 ('UEGCAP bytes 191:176','Group 中尚未配置給 NVM Set 的 NVM 容量，單位 bytes；0 表示不回報。','0 不能證明未配置空間已耗盡；Set 內未建 namespace 的空間也不是本欄的同一概念。'),
 ('保留區 byte 2、bytes 31:8、511:192','這些位置不提供上述屬性；保留區使下一個欄位仍位於規定的 offset。','EE 從 byte32 開始，不能因為 DID 在 byte7 結束，就從 byte8 讀 EE。'))

example(213,'SMART 的 Critical Warning 和單組 EGCW 有對應 bit，但觀察範圍不同。',
 '所有 Group 的 EGDR bit2 都為 1 時，SMART byte0 的 NDR bit2 必須為 1。若只有 Group7 為 1，不能僅憑這條規則就斷言所有 Group 都有可靠度下降。',
 'SMART Critical Warning uses corresponding bits at a broader scope; the all-groups propagation rule must not be read backward.')
group('smart','只比較警告的對應，不展開整份 SMART log','Figure 213 本篇只用 byte0 的 bits 0、2、3 來對照 Figure 225。其他欄位有自己的規則，不能把 LID09h 的十億-byte 單位套過去。',[213],
 ('bit0：ASCBT ↔ EGASB','兩者都是備用容量低於門檻的警告，分別位於 SMART CW 與單組 EGCW。','先確認正在讀的是哪一份 log，再對照同一類警告。'),
 ('bit2：NDR ↔ EGDR','可靠度下降的對應位元；所有 Group 都設定同一 bit 時，SMART 對應 bit 必須設定。','Group7 有、Group9 沒有，不符合「所有 Group」條件。'),
 ('bit3：AMRO ↔ EGRO','唯讀條件仍需排除 namespace write protection 狀態變更所造成的唯讀。','把軟體設定為唯讀與媒體原因的唯讀分開，不只看最終能否寫入。'))

example(493,'高 8-bit mask 選警告，低 16-bit ID 選 Group；兩者都不是實際健康狀態。',
 '00050007h 解為 mask05h、Group7。Get Features 的目前值回覆如果也是這個數字，只證明通知設定如此，不表示 Group7 此刻已發生 05h 警告。',
 'The mask selects warning causes and the identifier selects the group; reading back this feature reports configuration, not actual health.')
example(464,'SV 決定是否要求保存，FID 才決定要設定哪項功能。',
 '本例採 SV=0，所以 Set Features CDW10=00000018h。不能為了「啟用通知」就把 SV 設成 1；SV 是保存要求，不是啟用 bit。',
 'SV requests persistence and FID selects the feature; setting SV is not how event reporting is enabled.')
example(198,'SEL 改變查詢種類，也可能改變完成結果的格式。',
 'Get Features CDW10=00000018h 查目前設定；00000318h 查支援能力，前提是控制器支援非零 SEL。兩者都查 FID18h，但不能用同一套 DW0 欄位解碼。',
 'SEL chooses the query kind and can change the completion format; current attributes and supported capabilities require different decoders.')
example(201,'能力回覆的低 3 bits 不包含 ENDGID 或 EGCW。',
 'SEL3 成功回 DW0=4：CHANG=1、NSSPEC=0、SVBL=0，表示可變更、不是 namespace 專屬且不可保存；0 在 NSSPEC 不代表必然是 controller scope。',
 'The low three capability bits describe changeability, namespace specificity and saveability; they do not contain ENDGID or EGCW.')
example(466,'18h 的範圍是 Group，0Bh 的範圍是 controller；持續性 No 要搭配註腳2。',
 '設定 Group7 的 FID18h 不會設定 Group9。若 FID18h 不可保存，表內 No 表示目前值不跨斷電與重設保留；若可保存，該欄不適用，要用保存規則。',
 'FID18h is group-scoped and FID0Bh controller-scoped; the persistence column applies only when a feature is not saveable.')
group('feature-fields','設定、查回與保存能力放在同一組看','Figures 493／464／198／201／466 描述同一功能在不同命令階段的欄位；以下共用一次，避免反覆抄同一個 mask 例子。',[493,464,198,201,466],
 ('Figure493：CDW11 bits 15:0','ENDGID 指定存在的 Group；0 時 EGCW 不使用，沒有全體設定語意。不存在的 Group 使 Set／Get Features 必須失敗。','Group7 與 Group9 分別設定；不用 0 或 ENDGIDMAX 代指全部。'),
 ('bits23:16：EGCW／bits31:24 保留','EGCW 的 0／2／3 bits 對應實際警告；啟用保留 bit 必須回 Invalid Field in Command。','05h 選兩種；0Dh 選三種；0Fh 多了保留 bit1，無效。'),
 ('Get Features 的 Figure493 格式回覆','SEL≠3 且成功時，命令中的 EGCW 不使用；CQE DW0 回屬性。','查 Group7 送 CDW11=00000007h，不必在輸入重填目前 mask。'),
 ('Figure464：CDW10 FID7:0、SV31','SV=0 不要求保存；SV=1 需控制器支援，且此 Feature 可保存，否則有 Feature Identifier Not Saveable 的規則。bits30:8 保留。','本例00000018h 只選 FID18h，不要求持續性；不使用資料 buffer 來傳 mask。'),
 ('Figure198：CDW10 SEL10:8、FID7:0','SEL0目前、1預設、2保存、3能力；其他值保留，bits31:11 保留。SEL2 沒有保存值或不可保存時按預設值處理。','00000318h 是能力查詢，須先確認 ONCS.SSFS。'),
 ('Figure201：DW0 bits2／1／0','CHANG 表可變更、NSSPEC 表 namespace 專屬、SVBL 表可保存。NSSPEC=0 時範圍由 Feature 定義；bits31:3 保留。','FID18h 的範圍是 Group，不能由 NSSPEC0 推成整個 controller。'),
 ('Figure466：18h／0Bh 兩列與註腳2','18h 是 Group scope，0Bh 是 controller scope；兩者均不使用屬性資料 buffer。No 持續性只在不可保存時解讀。','先查 SVBL，再判斷 No 的適用情況；可保存時改看 saved／default／current 的規則。'))

example(474,'bit14 控制清單新增項目的通知，不取代每 Group 的警告選擇。',
 'FID18h 已替 Group7 啟用 mask05h，但 FID0Bh bit14=0，清單仍可記下該組待處理事件；主機沒有因此取得這種新增通知。只在要啟用這一類通知且其他 bit 全0 的例子，CDW11 才是 00004000h。',
 'FID0Bh bit14 enables aggregate-entry-addition notices; it does not replace the per-group warning selection in FID18h.')
group('notice-enable','兩層選擇的最後一層：是否通知主機','Figure 474 只取 EGEALCN bit14；其他 bit 是其他事件的選擇，既有設定不應因本篇示例而被清除。',[474],
 ('EGEALCN bit14=1','有 Group 項目新增至 LID0Fh 時，啟用這類主機通知；主機仍需提供 AER 接收。','配合 FID18h 才能從指定警告走到通知；不是只開任一個就完成設定。'),
 ('EGEALCN bit14=0','控制器不得送這種清單變更通知；此 bit 不負責清除 Group 的實際警告。','主機仍可主動查已支援的 log，輪詢不需要等 AER 完成。'),
 ('支援檢查','若要求 bit14=1，但 CTRATT.EGS=0 或 OAES.EGEAN=0，必須以 Invalid Field in Command 中止。','先測兩個能力 bit，再修改通知設定；支援、啟用與目前事件各自不同。'))

example(261,'NUMENT 決定有幾筆，2-byte 內容才決定要查哪個 Group。',
 '3 筆清單的 header 是 03 00 00 00 00 00 00 00，後接 01 00、02 00、07 00。第 3 筆起點為 byte12，內容是 7；補到 16-byte 傳輸的尾端零不是第 4 筆。',
 'NUMENT gives the count, while each two-byte entry supplies a group identifier; alignment padding is not another entry.')
group('aggregate-fields','用 [1,2,7] 讀出 header、項目與長度','Figure 261 不包含時間戳記、警告內容或每組事件次數。清單按識別值排序，所以要保留「筆數、位置、內容」三層意思。',[261],
 ('NUMENT bytes7:0','8-byte 直接計數，0 表沒有待處理項目；最大筆數受 ENDGIDMAX 限制。','NUMENT3 就是 3 筆，不加1；ENDGIDMAX9 不表示本次有9筆。'),
 ('Entry k，k從1起算','規格位置是 bytes(2×k+7):(2×k+6)，每筆是一個16-bit ENDGID。','k3→bytes13:12，讀出7；最大ID不一定等於筆數。'),
 ('程式 index i，i從0起算','起點 offset=8+2×i，與規格 Entry k 的 k=i+1 對應。','i2→offset12；ID7 位於該處，不是 index7。'),
 ('傳輸尾端補齊','內容8+2×NUMENT bytes；傳輸向上補4-byte整數倍，NUMD=傳輸bytes/4−1。此log尾端外補0。','NUMENT3→14 bytes→16 bytes→NUMD3；只解析3筆。'),
 ('移除單組項目的條件','成功讀取那一組 LID09h，且RAE=0；不是只讀彙整清單。','09h/7 成功確認後移除7，不代替1或2的處理。'))

example(204,'NUMDL 選傳多少、RAE 選是否確認、LID 選哪種 log，三者不可混讀。',
 '讀512 bytes LID09h、RAE1：NUMDL=127，因此 CDW10=007F8009h。改成007F0009h只把RAE清0，沒有減少回覆資料量。',
 'NUMDL controls length, RAE controls acknowledgement and LID selects the log; clearing RAE does not shorten the transfer.')
example(205,'CDW11 上半部的識別值與下半部的長度各有自己的數值。',
 '09h/Group7 使用00070000h：LSI7、NUMDU0。0Fh 沒有定義用LSI選單一Group，不能把相同00070000h拿來表示只取清單裡的7。',
 'CDW11 separates the log-specific identifier from the upper transfer-count bits; LID0Fh does not use LSI to filter one group.')
example(206,'byte offset 是從資料開頭跳過多少 bytes，不能拿 Group ID 當位置。',
 '讀LID09h的DUW可定位byte64；不是因Group7就從offset7開始。要從開頭取完整512 bytes，本例LPOL=0。',
 'A byte offset is a distance from the data start, not a group identifier; full LID09h reads begin at offset zero.')
example(207,'LPOU 接在 LPOL 上方組成一個位置，不是第二段回覆長度。',
 'LPOL=64、LPOU=0表示byte64；若LPOU=1，位置變成4,294,967,360，已遠超這份512-byte資料。',
 'LPOU forms the upper half of one offset, not another length; setting it changes the position by multiples of 2^32.')
example(208,'OT 決定位置的單位；本篇用 byte offset，不假設支援 index offset。',
 '本例CDW14=0，OT0表示byte位置。index2的entry位於byte12，不能只把LPOL填2而仍保留OT0；那會變成未對齊的byte位置。',
 'OT determines the offset unit. The examples use byte offsets and do not assume index-offset support.')
example(209,'09h 和 0Fh 的資料範圍與回復出廠預設內容的屬性不同，不能因為相鄰就當作相同 log。',
 '此表09h的Restore to Default Content為N，0Fh為Y。它不是說09h每個欄位永遠不變，而是區分是否回復出廠預設內容；不是一般reset規則。兩列CSI均為N，不用CSI選另一種格式。',
 'LID09h and LID0Fh differ in restore-to-default behavior; both ignore CSI, and a No restore entry does not make live health fields immutable.')
group('getlog-fields','讀取命令：先選資料，再設定長度與確認方式','Figures 204～209 共用這組命令欄位解釋。例子從offset0讀取，以已配置且足夠大的主機接收緩衝區接收資料，不展開記憶體頁描述機制。',[204,205,206,207,208,209],
 ('Figure204：NUMDL31:16／RAE15','NUMDL與NUMDU合成數量減1。RAE1保留、RAE0成功後確認；若失敗，事件必須保留。','512/4−1=127；RAE1不等於取消讀取或少傳1個dword。'),
 ('LSP14:8／LID7:0','LID09h與0Fh各選一種資料；沒有定義的LSP是保留。','本例LSP0，09h單組、0Fh待處理清單。'),
 ('Figure205：LSI31:16／NUMDU15:0','09h的LSI依Figure224選ENDGID；0Fh未定義LSI選組。NUMDU是NUMD高16bits。','512-byte讀取NUMDU0；不得把7填到低半部而誤增傳輸量。'),
 ('Figure206：LPOL31:0','OT0表示byte offset低32bits，需4-byte對齊；超過log大小的offset必須失敗。未對齊時可報Invalid Field；若不報，需視低2bits為0。','本例全頁讀offset0。定位DUW是byte64；offset7不是合法對齊。'),
 ('Figure207：LPOU31:0','offset高32bits，完整位置為LPOU×2^32+LPOL。','本篇小型資料以0為高半部，與NUMDU的長度用途不同。'),
 ('Figure208：OT23、CSI31:24','OT0是byte；OT1是index，需該log另行支援且定義entry。本篇不假設此能力。09h／0Fh不使用CSI。','CDW14=0選byte模式；UIDX6:0本例0表示不選UUID，bits22:7保留。'),
 ('Figure209：09h／0Fh兩列','資料為domain／subsystem範圍：多domain時對應接收命令控制器所在domain；單domain時相當於subsystem。CSI欄N表示不使用。','LID09h內仍用ENDGID選特定Group；scope不是忽略Group選擇。'),
 ('Restore to Default Content欄','09h=N、0Fh=Y；註腳9限定為回復出廠預設內容，不能拿來判斷Feature是否saveable。','此欄不定義一般斷電或reset的結果；清單空也不能證明媒體恢復。'))

example(151,'AER 完成值給你事件類型與下一份 log，不含這次是哪個 ENDGID。',
 '000F0602h 的 bits23:16是0Fh，15:8是06h，2:0是2。低值2表示Notice，不是Group2；要讀0Fh才能知道實際Group。',
 'The AER completion identifies the notice and associated log, not an ENDGID; AET=2 means Notice, not group 2.')
example(155,'Notice 的 06h 指定清除清單變更通知的方法，與移除單組項目不同。',
 'AET2、AEI06h對應Endurance Group Event Aggregate Log Page Change；成功讀0Fh且RAE0清除此notice。即使讀到[7]並完成這個動作，也還需要09h/7來確認Group7。',
 'Notice code 06h names aggregate-change acknowledgement through LID0Fh; that acknowledgement does not remove individual group entries.')
group('aer-fields','通知的三個欄位，兩個不同的確認對象','Figures 151／155 只讀本篇Notice的格式與06h這列；其他事件不展開。規格把通知類型與清單中各組事件分開管理。',[151,155],
 ('Figure151：AET bits2:0','010b表示Notice；bits7:3及31:24保留。','000F0602h最低3bits為2，沒有編入Group ID。'),
 ('AEI bits15:8／LID bits23:16','AEI06h指明清單新增事件，LID0Fh指定要讀的log。','通知可以代表一組或多組新增項目；不能從單一CQE推算NUMENT。'),
 ('Figure155：Notice06h的確認','成功讀0Fh且RAE0清除這個notice，允許之後相關通知繼續被報告。','清單中每個Group仍需依09h的規則處理，讀0Fh不是逐組確認的捷徑。'))

# section, source PDF pages (focused for large figures), lesson unit, title.
SOURCES={
 69:('3.2.3','109','model','NVM Sets and Associated Namespaces'),
 338:('5.2.14.2.1','368-372,379,388,397-398','model','Identify – Identify Controller Data Structure, I/O Command Set Independent'),
 224:('5.2.13.1.10','263','model','Endurance Group Identifier - Log Specific Identifier'),
 225:('5.2.13.1.10','264-265','health','Endurance Group Information Log Page'),
 213:('5.2.13.1.3','247','health','SMART / Health Information Log Page'),
 493:('5.2.30.1.17','504','configure','Endurance Group Event Configuration – Command Dword 11'),
 198:('5.2.12','235-236','configure','Get Features – Command Dword 10'),
 201:('5.2.12.2','238','configure','Completion Queue Entry Dword 0 when Select is set to 11b'),
 464:('5.2.30','483','configure','Set Features – Command Dword 10'),
 466:('5.2.30.1','484-485','configure','Set Features – Feature Identifiers'),
 474:('5.2.30.1.6','493','configure','Asynchronous Event Configuration – Command Dword 11'),
 261:('5.2.13.1.15','296','aggregate','Endurance Group Event Aggregate Log Page'),
 204:('5.2.13','239','aggregate','Get Log Page – Command Dword 10'),
 205:('5.2.13','240','aggregate','Get Log Page – Command Dword 11'),
 206:('5.2.13','240','aggregate','Get Log Page – Command Dword 12'),
 207:('5.2.13','240','aggregate','Get Log Page – Command Dword 13'),
 208:('5.2.13','240-241','aggregate','Get Log Page – Command Dword 14'),
 209:('5.2.13','241-242','aggregate','Get Log Page – Log Page Identifiers'),
 151:('5.2.2','210-211','service','Asynchronous Event Request – Completion Queue Entry Dword 0'),
 155:('5.2.2','213','service','Asynchronous Event Information – Notice'),
}
PRIMARY={224,225,261,493}
