"""Independently authored lessons for Endurance Group health and event handling."""
from scripts.nvme_report_extension import bi


def claim(zh, en, section, pages, background=False):
    return dict(text=bi(zh,en),section=section,pages=pages,background=background)


UNITS = [
dict(key='model',title=bi('先確認正在觀察哪一組儲存空間','Establish which storage group is being observed'),claims=[
 claim('LID 09h 提供指定 Endurance Group 的 512-byte 資料；LID 0Fh 彙整有待處理事件的 Group 識別值；FID 18h 則逐組選擇要回報的警告。三者分別回答「現在如何」、「哪些組需要查看」與「哪些情況需要列入清單」。',
 'LID 09h returns 512 bytes for one Endurance Group. LID 0Fh lists group identifiers with pending events. FID 18h selects warnings per group. They answer, respectively, what the group reports now, which groups need attention and which conditions should add a list entry.','5.2.13.1.10, 5.2.13.1.15, 5.2.30.1.17','263-265,296,504'),
 claim('Endurance Group 可以包含分配給零個或多個 NVM Set 的容量。每個 Set 只屬於一個 Group；同 Group 的多個 Set 共同管理耐用度。每個 Group 只屬於一個 domain，16-bit ENDGID 在整個 NVM subsystem 內唯一，0 不是有效 Group 識別值。',
 'An Endurance Group may contain capacity allocated to zero or more NVM Sets. Each set belongs to one group, and sets in a group share endurance management. A group belongs to one domain. Its 16-bit ENDGID is unique within the NVM subsystem; zero is not a valid group identifier.','3.2.3','108-110',True)],
 example=bi('說明性範例：Group 7 包含 Set A、B；Group 9 包含 Set C。Group 7 的警告需要用 ENDGID=7 查詢，不能把 Set B 的編號或某個 namespace 的 NSID 填進去。',
 'Illustrative example: group 7 contains sets A/B and group 9 contains set C. Query a warning for group 7 with ENDGID=7, not the identifier of set B or a namespace NSID.'),
 steps=[
 ('從管理目的理解分組','想像同一個裝置提供數個 namespace，主機可以分別讀寫它們，但底層耐用度不一定各自獨立管理。Endurance Group 把「哪些儲存容量一起管理耐用度」明確分組。因此一個 Group 的健康資料，不能直接當成其中單一 namespace 的專屬統計，也不能當成整台裝置所有儲存空間的統計。'),
 ('把容量與識別值連起來','本文使用 Group 7／9 作為例子。Group 7 的 Set A、B 可以各有數個 namespace；Group 9 的 Set C 則使用另一份耐用度管理範圍。查詢 Group 7 時，Log Specific Identifier 要放 Group 的 ENDGID=7。編號只用來指定對象，數值 7 不表示容量、清單中第 7 筆或第 7 個 namespace。'),
 ('未配置容量也分層','Group 內尚未分配給任何 Set 的容量，才是 unallocated Endurance Group capacity。已分給 Set、但 Set 尚未拿來建立 namespace 的容量，仍屬於那個 Set；不能再把它全部加進 Group 的未配置容量。原規格圖中的灰色空間位於哪一層外框內，正是判斷兩者的關鍵。'),
 ('先查支援，再解讀清單','Identify Controller 的 CTRATT.EGS bit 4 表示 Endurance Groups 支援；OAES.EGEAN bit 14 表示這類清單變更通知的支援。支援 Group 時必須支援 LID 09h；若 subsystem 支援超過一個 Group，還必須支援 LID 0Fh。只有一組時不能反過來推論 LID 0Fh 一定不支援。未支援 Groups 時，命令中的 Group 欄位被忽略，回傳資料的 Group 識別欄位清 0；這不代表存在 Group 0。'),
 ('一次記住三個操作的分工','接下來先學會讀懂單組資料，再設定通知條件，最後沿著通知找到各組的資料。這樣在收到 LID 0Fh 清單時，便知道清單只負責指路，真正的警告、累積讀寫量與容量仍要到 LID 09h 查。')],
 reading=bi('先對照三個操作的輸入與輸出，再讀 Figure 69 的外框。能力欄與識別值上限集中在 Figure 338 的必要欄位教學。','Compare the inputs and outputs of the three operations, then the containment boundaries in Figure 69. The focused Figure 338 lesson covers capability bits and the identifier ceiling.')),

dict(key='health',title=bi('讀懂當下警告，不把估計壽命當作故障宣判','Read current warnings without treating estimated wear as failure'),claims=[
 claim('LID 09h 的 EGCW 是處理 Get Log Page 當時的警告狀態，可能已不同於通知發生時。bit 0 表示備用容量低於門檻，bit 2 表示可靠度下降，bit 3 表示整組 namespace 因非寫入保護設定的原因進入唯讀；bit 1 與 bits 7:4 保留。PUSED=100 表示估計耐用度已用完，並不直接表示媒體故障。',
 'EGCW in LID 09h describes warnings when Get Log Page is processed, which may differ from the notification-time state. Bit 0 means spare below threshold, bit 2 degraded reliability, and bit 3 group-wide read-only for reasons other than namespace write-protection settings. Bit 1 and bits 7:4 are reserved. PUSED=100 means estimated endurance consumed, not necessarily media failure.','5.2.13.1.10','264'),
 claim('當 subsystem 內所有 Endurance Group 的同一個警告 bit 都是 1，SMART / Health Information 的對應 Critical Warning bit 必須為 1。這條規則不能倒推成「單一 Group 的警告一定代表整個 subsystem 已有相同狀態」。',
 'If the same warning bit is set in every Endurance Group in the subsystem, the corresponding SMART / Health Critical Warning bit must be set. This does not make a warning in one group evidence that every group is in that state.','5.2.13.1.10','264')],
 example=bi('Group 7 回報 EGCW=05h、AVSP=8、AVSPT=10、PUSED=103：8% 低於 10%，且可靠度下降；bit 3 沒有設定。103% 是壽命估計已超過 100%，不能拿它代替「唯讀」判斷。',
 'Group 7 reports EGCW=05h, AVSP=8, AVSPT=10 and PUSED=103: spare is 8%, below 10%, and reliability is degraded; bit 3 is clear. The 103% wear estimate does not establish a read-only condition.'),
 steps=[
 ('先拆 bit，再找數值佐證','EGCW 不是一個互斥的錯誤代碼，而是可以同時成立的多個警告。05h 的二進位低 4 bits 是 0101b，表示 bit 2 與 bit 0 同時為 1。先列出兩個警告，再用 AVSP 與 AVSPT 檢查備用容量；不要把 05h 讀成「第 5 種錯誤」。'),
 ('備用空間和已用壽命不能相減','AVSP=8 表示剩餘備用容量的正規化百分比；AVSPT=10 表示比較門檻。低於是嚴格小於，所以 8<10 符合，10=10 並不符合「低於」這個條件。PUSED 則是廠商依據使用狀況與壽命模型做的估計，不是 100−AVSP。PUSED 可以大於 100，超過 254 的百分比一律以 255 表示；控制器不在 sleep state 時，每個通電小時更新一次。'),
 ('唯讀警告有明確原因限制','EGRO=1 表示這個 Group 的所有 namespace 因其他原因進入唯讀，例如媒體可靠度相關的保護行為。若唯讀完全來自 namespace write protection 狀態的改變，控制器不得因此設定 EGRO。單看「不能寫」的外觀不足以判定 bit 3，還要分清原因。'),
 ('警告、歷史次數與通知各有時間意義','EGCW 回答讀取當時的狀態。累積錯誤次數回答曾經發生多少次。非同步通知則告訴主機曾有需要注意的條件。通知到主機開始讀 log 之間，狀態可能變化；因此收到通知卻讀到 EGCW=0，不能直接判定控制器送了假通知，也不能用這份 log 還原通知當時的全部狀態。'),
 ('先看局部，再看整體','假設 Group 7 的 EGDR=1、Group 9 的 EGDR=0，就只確定 Group 7 回報可靠度下降。當兩組都為 1 時，規格才用「所有 Group 同一 bit 皆為 1」的規則要求對應 SMART 警告為 1。SMART log 自身還有其他規則與欄位，不應把單組結果自行擴大成全域結論。')],
 reading=bi('Figure 225 的 byte 0 要逐 bit 看；bytes 3～5 要逐欄區分百分比的意義。下方欄位教學也交代 EGFEAT、DID、保留區與 SMART 對應。','Read byte 0 bit by bit and distinguish the percentages at bytes 3–5. The field guide also covers EGFEAT, DID, reserved areas and the SMART relationship.')),

dict(key='traffic',title=bi('把累積量、命令次數與容量分開換算','Separate cumulative traffic, command counts and capacity'),claims=[
 claim('LID 09h 的 EE、DUR、DUW、MUW 以 1,000,000,000 bytes 為單位並向上取整，0 表示不回報該值。DUR／DUW 不包含控制器內部作業的讀寫，MUW 包含主機與控制器的寫入。HRC／HWC 是已完成命令數；TEGCAP／UEGCAP 是以 bytes 表示的容量，0 同樣表示不回報，不能當作測得的零容量。',
 'EE, DUR, DUW and MUW in LID 09h use units of 1,000,000,000 bytes, rounded up; zero means not reported. DUR/DUW exclude internal controller operations, while MUW includes host and controller writes. HRC/HWC count completed commands. TEGCAP/UEGCAP are byte capacities, with zero likewise meaning not reported rather than a measured zero capacity.','5.2.13.1.10','264-265'),
 dict(text=bi('以 NVM Command Set 為例，HRC 的命令類別包含 Compare、Copy、Read、Verify；HWC 的 User Data Out 類別包含 Copy、Write。讀取資料不一定把資料傳回主機，寫入資料也不一定由主機傳入；因此 Copy 可以同時涉及兩種統計分類。',
 'For the NVM Command Set, HRC covers Compare, Copy, Read and Verify, while the User Data Out class for HWC covers Copy and Write. Reading need not return data to the host and writing need not transfer data from the host, so Copy can participate in both classes.'),section='1.4.2.1, 1.4.2.10',pages='10-11',source_id='NVME-NVM-CS-1.3',scope_entry_id='EGE-NVM-PREREQUISITES',background=True)],
 example=bi('DUW=3 的意思是 2,000,000,001～3,000,000,000 bytes，不是精確 3 GB。若 MUW=5，直接算 5÷3 只能得到量化後的粗略比值；不能宣稱實際寫入放大率精確等於 1.667。',
 'DUW=3 represents 2,000,000,001–3,000,000,000 bytes, not exactly 3 GB. If MUW=5, dividing 5 by 3 gives only a coarse ratio of quantized values, not an exact write-amplification factor of 1.667.'),
 steps=[
 ('先問數字在數什麼','512-byte 回覆裡放了不同種類的數字。EE 是對總壽命可寫入量的估計；DUR／DUW／MUW 是已發生的累積資料量；HRC／HWC 是命令筆數；TEGCAP／UEGCAP 是可儲存容量。把這四類放在同一個「容量」欄相互比較，會把已使用量、可用空間與工作次數混在一起。'),
 ('向上取整會留下範圍','對正數 n，原始 byte 數落在 (n−1)×1,000,000,000+1 到 n×1,000,000,000。讀到 1，不代表恰好寫了十億 bytes，也可能只寫了一部分；讀到 3，才知道超過二十億而未超過三十億。此處的十億是十進位，不是 1 GiB=1,073,741,824 bytes。'),
 ('把主機寫入和媒體工作量對照','主機寫入資料後，控制器可能為垃圾回收搬移仍有效的資料。DUW 不把這些內部寫入計入，MUW 則計入，因此兩欄能幫助理解內部工作量。可是兩者都已向上取整，小數字的誤差比例很大。用同一觀察時間的非零欄位比較，仍只能得到粗略關係；若任何一欄為 0，就連「有回報量」的前提都不成立。'),
 ('壽命估計不能直接變成剩餘空間','EE 是假設寫入放大為 1 時、整個 Group 一生可寫入總 byte 數的估計，不是目前剩餘寫入配額。把 EE−DUW 叫做保證的剩餘壽命沒有依據，也不能拿來替代 PUSED。TEGCAP 則回答 Group 有多少 NVM 容量；UEGCAP 回答其中尚未配置給 Set 的容量，兩者用原始 bytes，沒有十億倍換算。'),
 ('命令分類和傳輸方向要分開','以 NVM Command Set 而言，HRC 包含 Compare、Copy、Read、Verify，HWC 則包含 Copy、Write。Compare 比較、Verify 驗證與 Copy 複製都涉及讀取，但不因此把完整讀取資料送回主機；Copy 的目的端寫入也不需要主機重新傳入資料。所以不能只數「有資料傳回主機」的命令來算 HRC，也不能把 HWC 只當成 Write 次數。'),
 ('命令與錯誤次數要按各自定義讀','1 筆命令可以搬很多 bytes，所以命令數無法直接換算 DUW。MDIE 計算未恢復資料完整性錯誤；NEILE 計算控制器生命週期內、屬於這個 Group 的 Error Information Log 項目。一次錯誤事件的分類與紀錄方式不同，兩欄沒有必須相等的規則。')],
 reading=bi('Figure 225 跨兩頁；先讀每欄的單位與 0 的意義，再讀數值。欄位教學逐一列出位置、統計對象與例子。','Figure 225 spans two pages. Establish each field’s unit and zero semantics before interpreting its value; the guide gives positions, counting scope and examples.')),

dict(key='configure',title=bi('選擇哪些警告要列入事件清單','Choose which warnings should add a pending entry'),claims=[
 claim('FID 18h 的 CDW11 低 16 bits 指定 ENDGID，bits 23:16 是 EGCW 通知選擇遮罩，逐 bit 對應 LID 09h 的警告。啟用時若條件已成立，也會產生事件。設定保留警告 bit 或指定不存在的 Group，必須以 Invalid Field in Command 中止；ENDGID=0 不表示全體 Group，這時 EGCW 不使用。',
 'FID 18h uses CDW11 bits 15:0 for ENDGID and bits 23:16 for the EGCW selection mask, matching LID 09h warnings bit by bit. An already-true condition generates an event when enabled. Enabling a reserved warning bit or selecting a nonexistent group must cause Invalid Field in Command. ENDGID=0 is not an all-groups selector; EGCW is unused in that case.','5.2.30.1.17','504'),
 claim('Get Features 在 SEL≠011b 且成功時，忽略命令中 EGCW 的輸入，以 CQE DW0 回傳 Figure 493 格式的屬性。SEL=011b 回覆的是 Feature 能力格式，不能當成目前警告選擇。FID 18h 決定逐組列入清單的原因；FID 0Bh 的 bit 14 另外控制清單新增項目時是否通知主機。',
 'On successful Get Features with SEL other than 011b, input EGCW is unused and CQE DW0 returns attributes in the Figure 493 format. SEL=011b instead returns feature capabilities, not the current warning mask. FID 18h selects per-group list triggers; FID 0Bh bit 14 separately enables host notification when entries are added.','5.2.30.1.17, 5.2.12, 5.2.30.1.6','236-238,492-493,504',True)],
 example=bi('要為 Group 7 啟用備用容量與可靠度兩種警告，EGCW mask=05h，所以 Set Features FID=18h、CDW11=00050007h。若只關閉可靠度警告但保留備用容量警告，就改成 00010007h；這不會修復已存在的可靠度問題。',
 'For group 7, enable spare and reliability warnings with mask 05h: Set Features FID=18h, CDW11=00050007h. To disable reliability reporting while retaining spare reporting, use 00010007h; that change does not repair degraded reliability.'),
 steps=[
 ('同名 EGCW，先看它出現在哪裡','LID 09h 的 EGCW 是控制器回報的實際狀態。FID 18h 的 EGCW 則是主機設定的選擇遮罩：1 表示對應警告成立時要列入事件清單，0 表示不因這一類警告新增項目。把 mask 設為 0 不會清除 log 的警告，也不會把媒體變健康。'),
 ('用一個完整數字看懂編碼','本例 bit 2 與 bit 0 都啟用，mask=00000101b=05h。把 mask 左移 16 bits，再加上 ENDGID=7，得到 (05h<<16)|0007h=00050007h。高 8 bits 保留。本篇三種警告全部啟用時是 0Dh，而不是 0Fh，因為 bit 1 保留；對應 Group 7 的完整數字是 000D0007h。'),
 ('每一組各自設定，不能拿 0 當全部','Group 7 的設定不會自動套到 Group 9，主機要分別送命令。Figure 493 明確說 ENDGID=0 時 EGCW 不使用，並沒有提供廣播給所有 Group 的語意；此外，章節要求不存在的 Group 識別值使 Set／Get Features 失敗。因此例子一律使用已確認存在的非零 ID，也不把最大識別值以下每個數字都當成存在。'),
 ('查回設定和查能力是兩次不同解讀','Get Features FID18h、SEL=0、CDW11=00000007h 查目前屬性。成功時看 CQE DW0 的低 16 bits 確認對象、bits 23:16 讀目前 mask；命令中原先填入的 EGCW 不作設定。若 SEL=3，DW0 低 3 bits 變成 Changeable、NS Specific、Saveable；例如 4 代表可變更而不可保存，絕不能把 4 當作 Group 4。SEL=2 在沒有保存值或不可保存時按預設值處理。'),
 ('把清單選擇和通知啟用分開','若需要主動通知，還要在支援的控制器上啟用 FID0Bh 的 EGEALCN bit 14，並提交 Asynchronous Event Request 等待控制器完成回覆。FID18h 是每 Group 的選擇；FID0Bh 是控制器的通知設定。本文只補這個 bit，不改動其他通知選擇。設定後是否跨重設保存，應查 Saveable 能力；Figure 466 的 No 只在該 Feature 不可保存時適用，不能據此宣稱所有裝置都禁止保存。')],
 reading=bi('先讀 Figure 493 的高低欄位，再對照 Get Features 的 SEL 與 FID0Bh bit 14。三個設定各有自己的範圍與輸出格式。','Read the high and low fields in Figure 493, then compare SEL and FID 0Bh bit 14. Each setting has its own scope and result format.')),

dict(key='aggregate',title=bi('從清單找到 Group，而不是從序號猜 Group','Find groups from list values rather than list positions'),claims=[
 claim('LID 0Fh 是依 ENDGID 遞增排列的待處理清單，不是事件時間序列。前 8 bytes 是 NUMENT，之後每筆 2 bytes。NUMENT 直接表示筆數；最大筆數受 ENDGIDMAX 限制。超過這份 log 結尾的傳輸資料必須補零；只有 NUMENT 指定的項目才是有效清單內容。',
 'LID 0Fh is a pending list sorted by ENDGID, not a chronological event history. NUMENT occupies the first eight bytes, followed by two-byte entries. NUMENT is a direct count bounded by ENDGIDMAX. Transfers beyond the log end must return zero padding; only the entries indicated by NUMENT belong to the list.','5.2.13.1.15','296')],
 example=bi('Group 7、1、2 先後發生事件，清單仍是 [1,2,7]，NUMENT=3。有效資料共 8+2×3=14 bytes；以 dword 傳輸要取 16 bytes，NUMD=16÷4−1=3。最後 2 bytes 的零不代表 Group 0。',
 'Events occur for groups 7, 1 and 2, but the list is [1,2,7] with NUMENT=3. Meaningful data occupies 8+2×3=14 bytes. A dword-granular transfer uses 16 bytes and NUMD=16/4−1=3. The final two zero bytes are not group 0.'),
 steps=[
 ('先看筆數，再看識別值','NUMENT 是 64-bit 直接計數，不採數量減 1。NUMENT=0 表示目前沒有項目；NUMENT=3 就解析 3 個 16-bit ID。清單回答哪些 Group 有啟用且待處理的事件，不提供每組的警告 bit、事件次數或時間戳記。這些不能從列表順序猜出來。'),
 ('項目序號、位置與 ID 是三件事','規格以 Entry 1 稱第一筆，位於 bytes 9:8。若程式用從 0 起算的 index i，該筆的 byte offset 是 8+2×i。例子的第 3 筆為 index=2、offset=12、ENDGID=7。12 只是從 log 開頭數過來的 byte 位置；要查細節，必須取出內容 7 作為 LID09h 的 LSI。'),
 ('把長度補到可傳輸的單位','header 是 8 bytes，每筆是 2 bytes，3 筆合計 14 bytes。Get Log Page 以 4-byte dword 為單位，因此要求 4 個 dword，也就是 16 bytes；數量編碼填 3。這份 log 特別規定尾端外的資料補 0，所以不必把多出的兩個零解成額外 entry。這個補零保證不能自行套到所有其他 log page。'),
 ('最大 ID 不是目前筆數','若 ENDGIDMAX=9，代表合法識別值的上限是 9，實際 Group 數與待處理筆數都可能較少，而且 ID 可以不連續。為清單準備最大空間，可用 8+2×9=26 bytes，再向上補到 28 bytes，NUMD=6。回覆若 NUMENT=3，仍只解析 3 筆；剩餘傳輸空間不是額外 6 組。'),
 ('分段讀取時不要假設內容凍結','可以先讀 header 估算資料長度，再讀完整清單；兩個命令之間可能新增或移除項目，因此第二次回覆的 NUMENT 才是該份回覆應使用的筆數。若它超過本次緩衝區可容納項目，就加大後重讀，不能越界解析。這是主機讀取策略；Figure 261 本身沒有提供 generation number，不能聲稱分段資料一定來自同一時刻。')],
 reading=bi('Figure 261 的 8-byte header、2-byte entry 與 NUMD 的 4-byte 傳輸單位要分開看。下面也用 512-byte LID09h 對比兩種 log 的長度。','Separate the eight-byte header, two-byte entries and four-byte transfer unit in Figure 261. The guide contrasts this layout with the fixed 512-byte LID 09h.')),

dict(key='service',title=bi('走完通知、讀取與確認的完整流程','Complete the notification, inspection and acknowledgement sequence'),claims=[
 claim('成功讀取某 Group 的 LID 09h 且 RAE=0，會清除該 Group 的待處理事件並移除它在 LID 0Fh 的項目。RAE=1 保留事件，讀取失敗也必須保留。讀取 LID 0Fh 且 RAE=0 則清除清單變更通知，不能代替逐組的 LID09h 確認；確認事件不代表造成警告的狀態已消失。',
 'A successful LID 09h read with RAE=0 clears that group’s pending events and removes its LID 0Fh entry. RAE=1 retains the event, as must a failed read. Reading LID 0Fh with RAE=0 clears the aggregate-change notification; it does not replace per-group LID 09h acknowledgement. Acknowledging an event does not establish that its underlying condition has disappeared.','5.2.13.1.15, 3.2.3, 5.2.13, 5.2.2','110,209-213,239,296',True),
 claim('非同步通知透過完成主機預先提交的 AER 回報。此事件的 CQE DW0 為 AET=2、AEI=06h、LID=0Fh，並未包含 ENDGID。持續存在的警告可能在確認後再次被回報；主機宜在確認前調整相應門檻或遮罩，避免相同狀態反覆通知。',
 'A notification completes a host-posted AER. This notice encodes AET=2, AEI=06h and LID=0Fh in CQE DW0; it does not carry ENDGID. Persistent conditions can be reported again after acknowledgement. The host should adjust the relevant threshold or mask before clearing an event to avoid repeated reporting of an unchanged condition.','5.2.2','209-213',True)],
 example=bi('本例只追蹤 Group 7：收到 000F0602h 通知後先以 RAE=1 讀 0Fh，再以 RAE=1 讀 09h/ENDGID7。完成處理後以 RAE=0 成功讀 09h/7，移除該組項目；再以 RAE=0 讀 0Fh，確認清單變更通知。若這次清單又有其他 Group，繼續處理它們。',
 'For group 7, receive notice 000F0602h, inspect 0Fh with RAE=1, then 09h/ENDGID7 with RAE=1. After handling the condition, successfully read 09h/7 with RAE=0 to remove its entry, then read 0Fh with RAE=0 to acknowledge the aggregate-change notice. Process any other groups returned by that read.'),
 steps=[
 ('AER 是主機先留下的通知要求','主機預先提交 AER；控制器有事件時才完成它。這不是主機每隔幾秒讀一份 log，也不是控制器自行新增主機命令。通知完成後，主機需補送 AER 才能持續接收，未完成數量受 AERL+1 限制；不應替等待事件的 AER 設一般命令逾時。'),
 ('先保留事件，取得要處理的資訊','收到 CQE DW0=000F0602h，拆成 LID0Fh、AEI06h、AET2，知道要讀彙整清單。以 RAE=1 讀取便能先查看而不確認通知；拿到 Group7 後，再以 RAE=1 查它的 512-byte LID09h。這時讀到的是當下狀態，主機應把有用的數值留下，再決定怎麼處理。'),
 ('確認有兩個不同對象','第一個確認對象是「Group7 的待處理事件」：成功讀 09h/7 且 RAE=0，會移除清單裡的 7。第二個是「0Fh 有新增項目」的通知：成功讀 0Fh 且 RAE=0 才清除這個 notice。只做第二步，清單中的 7 仍可能存在；只讀另一組 09h/9，也不會代替 Group7 的確認。'),
 ('持續警告要先決定是否繼續接收','若 Group7 的可靠度持續下降，RAE=0 並不修復媒體。主機可以在記錄與處理後，以 FID18h 關閉這一類反覆通知、保留其他警告，再確認事件。這是通知政策的例子，不能把關閉通知稱為修復。日後重新啟用該 bit 時，若條件仍成立，事件會再送出。'),
 ('把併發更新當作正常運作','本例為了容易看懂，先假設處理期間沒有新事件；真實運作可能同時有其他 Group 新增項目。最後那次 RAE=0 讀 0Fh 同樣會回傳清單，主機應查看內容，而不是讀完就丟掉。空清單只表示此時沒有列出的待處理項目，不是整台裝置的健康證明；這份格式沒有提供跨多次讀取的原子快照。')],
 reading=bi('先沿時序看每次讀取的 LID、ENDGID 與 RAE，再看兩個不同的清除動作。Figure 151／155 解釋通知為什麼不直接告訴你是哪一組。','Follow LID, ENDGID and RAE for each read, then distinguish the two acknowledgements. Figures 151/155 explain why the notice does not directly identify a group.')),
]
