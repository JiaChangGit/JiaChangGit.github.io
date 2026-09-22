"""Focused source-figure teaching for the SQ Associations dependencies."""
EXAMPLES = {}
GUIDES = {}
MEMBERS = {}


def example(number, takeaway, worked, en):
    EXAMPLES[number] = dict(takeaway=takeaway, example=worked, en=en)


def group(key, title, relation, numbers, *rows):
    ident = 'sqa-' + key
    GUIDES[ident] = dict(id=ident, title=title, relation=relation, rows=list(rows))
    for number in numbers:
        MEMBERS[number] = ident


def lesson(figure):
    return EXAMPLES[int(figure['number'])]


def guide(figure):
    return GUIDES[MEMBERS[int(figure['number'])]]


example(67, '先讀 namespace 的包含關係，才知道 SQ 應該服務哪一個 Set。',
 '原圖中 NS A1、A2、A3 都在 NVM Set A 的外框內；若一個 SQ 關聯到 A，它預期承載這三個 namespace 的 I/O。圖上的 Set B 不會因為某筆命令經同一個 CQ 完成，就變成 A 的一部分。',
 'Namespace containment determines the set an SQ should serve; completion destinations do not change storage membership.')
group('membership-fields','儲存外框與命令對象的關係',
 'Figure 67 是儲存配置示意，沒有表示 SQ 或 CQ，也沒有要求每個 Set 的 namespace 數量相等。', [67],
 ('NVM Set A／B／C','外框代表彼此邏輯分開的儲存集合；字母是示意名稱。','實際關聯使用 16-bit Set 識別值，例如 7。'),
 ('NS A1～A3、B1～B2、C1','每個具有已格式化儲存空間的 namespace 完整位於一個 Set。','A1 與 A2 可使用同一個關聯到 A 的 SQ；不需要一個 namespace 獨占一個 SQ。'),
 ('Unallocated','Set 內尚未配置給 namespace 的容量。','它沒有可供一般 I/O 指定的 namespace 對象；不是另一個待選的 Set 或空 SQ。'))

example(338, 'CTRATT 的三個 bit 回答支援能力，沒有回報 SQ 關聯清單或目前工作視窗。',
 '0124h 的相關位元是 bit 8、5、2；0224h 雖然也有 bit 5、2，卻沒有 bit 8，不能當作 SQA 支援。對整個 CTRATT 應使用遮罩，避免其他能力位元干擾判斷。',
 'The three CTRATT bits report support, not a list of queue associations or the current window.')
group('capability-fields','先確認能做，再談是否已做',
 '只取 Figure 338 的 CTRATT bytes 99:96 中 SQA、PLM、NSETS。其餘 bit 不是本篇內容，也不能一律當成保留。',[338],
 ('SQA bit 8','1 支援 SQ Associations；0 不支援。','0124h & 0100h 非零，表示此能力受支援。'),
 ('PLM bit 5','1 支援 Predictable Latency Mode；支援 SQA 時必須同時為 1。','此 bit 不能證明 Set 7 當下已啟用模式。'),
 ('NSETS bit 2','1 支援 NVM Sets；支援 SQA 時必須同時為 1。','只看到 NSETS=1，不足以推論 SQA=1。'),
 ('三者合併檢查','遮罩 0124h=(1<<8)|(1<<5)|(1<<2)，檢查與遮罩相 AND 的結果。','CTRATT=0324h 仍通過三 bit 檢查；額外 bit 9 不改變這個結論。'))

example(751, 'DTWIN 與 NDWIN 表示同一 Set 沿時間經過的不同工作視窗，不是兩個 Set。',
 'Set 7 原本在綠色 DTWIN，之後為準備下一個視窗進入紅色 NDWIN。SQ3 仍可保持關聯 Set 7；視窗改變不代表 SQ3 自動改去 Set 9。原圖沒有時間刻度，不能從方塊寬度算毫秒。',
 'DTWIN and NDWIN are successive operating windows of a set, not two different sets or fixed-duration slots.')
group('window-fields','沿時間讀兩種視窗與切換條件',
 '本篇只補 Figure 751 所需的模式背景；SQA 的選用提示不能代替模式啟用與視窗條件。',[751],
 ('綠色 DTWIN','Set 能提供確定性讀寫延遲；仍需符合該視窗的工作量與時間限制。','兩個關聯同 Set 的 SQ 要共同計入該 Set 的負載。'),
 ('紅色 NDWIN','準備後續 DTWIN 所需的工作使 Set 無法提供確定性讀寫延遲。','例如進行媒體背景操作；不是主機必須把資料移到另一個 Set。'),
 ('橫向交替與 Legend','時間由左往右，圖例把顏色對應到狀態；未給固定週期或長度。','DTWIN 畫得較長，不代表它固定是 NDWIN 的某個倍數。'),
 ('DTWIN → NDWIN','主機可要求切換；操作屬性超過典型或最大值，或發生 Deterministic Excursion 時，Set 可自行轉入 NDWIN。','有關聯而且送對 SQ，仍不能忽略視窗的讀取量、寫入量與時間條件。'))

example(333, 'CDW10 的 CNS 選擇要問哪個問題，CNTID 不是 namespace 的編號。',
 '查 Set List 用 CDW10=00000004h，查 namespace 歸屬用 00000008h。後者的 NSID=21 放在共同命令的 NSID 欄，不能填到 CDW10 高 16 bits 的 CNTID。',
 'CNS in CDW10 chooses the question; CNTID is not a namespace identifier.')
example(334, 'CDW11 低 16 bits 的意思由 CNS 決定，不是每次 Identify 都在選 Set。',
 'CNS=04h、CDW11=00000007h 表示從 Set ID 7 開始列舉；換成 CNS=08h 查 NSID21 的歸屬時，不再把 7 填成篩選條件，CNSSID 在該選項未定義。',
 'CDW11’s low 16 bits depend on CNS; they are not a set selector for every Identify query.')
example(336, '先用 CNS 列選回覆結構，再用 Y／N 判斷 NSID、CNTID、CSI 是否參與這次查詢。',
 '01h 問控制器能力，04h 問 Set 清單，08h 問指定 namespace。只有這三列中的 08h 對 NSID 標 Y；不可因為 Identify 命令帶有 NSID 欄，就認為所有選項都使用它。',
 'Choose the response using the CNS row, then read Y/N for whether each selector is used.')
group('identify-command-fields','同一個 Identify 命令的三種查詢',
 '只取 CNS 01h／04h／08h，以及命令中解釋這三種查詢所需的欄位。',[333,334,336],
 ('Figure 333：CNS bits 7:0','01h 回控制器資料；04h 回 Set 清單；08h 回指定 namespace 的跨命令集共用資料。','三者沒有相同的回覆布局，不能把 04h 的回覆當 08h 解。'),
 ('Figure 333：CNTID bits 31:16','這三種 CNS 都不使用 CNTID；主機必須清 0，控制器必須忽略。bits 15:8 保留。','要查 NSID21，填共同 NSID 欄；不是 CNTID=21。'),
 ('Figure 334：CSI bits 31:24','三種 CNS 均不使用 CSI；主機宜清 0，控制器宜忽略。若非零，控制器可回 Invalid Field in Command。','相容的組合在此填 0；不能因「不使用」就隨意留下其他值。'),
 ('Figure 334：CNSSID bits 15:0','CNS=04h 用作清單起始 Set ID；01h／08h 未定義，屬保留。bits 23:16 保留。','04h 配 7 是找 ID≥7；08h 的目標由 NSID 決定。'),
 ('Figure 336：O／M 與 Y／N','O／M 為選用／必備支援；Y／N 為該輸入欄是否使用。01h、08h 為 M，04h 為 O。','04h 的 O 不等於主機可以忽略回覆內容；支援 SQA 的情境需要 Set 資訊。'),
 ('NSID 欄與回覆','01h／04h 不用 NSID；08h 使用 NSID，對 active NSID 回傳對應資料。','本例依序查 11、12、21，得到 7、7、9；不是只做一次查詢就取得整張 namespace 對照。'))

example(343, '清單的起點是 Set 識別值下限，而且包含等於該值的 entry。',
 '可存取的 Set 為 7、9、37，要求起點 9 會從 9 開始，不會跳過它。若上一批最後值為 37，下一批可從 38 查；不是把「已讀 31 筆」直接當下一個 Set ID。',
 'The starting identifier is an inclusive lower bound, not an entry index or page number.')
example(344, 'NUMENT 是直接筆數，entry 位置則由固定 header 與 128-byte 步距計算。',
 'NUMENT=2 時只讀 Entry 0、1。Entry 1 起點=128+1×128=256，結束=383；剩餘補零不能再被當成有效 Set。NUMENT=0 就沒有 entry，不是 1 筆。',
 'NUMENT is a direct count; record locations use a 128-byte header and 128-byte stride.')
example(345, '同一筆 entry 同時有識別值、效能參考與儲存容量，必須分開使用。',
 '假設 NSETID=9、R4KRT=120、TNVMSC=1,048,576,000。9 可用於建立 SQ 關聯；120 代表特定測量條件下典型 12 μs；容量則是 bytes，不能拿來設定 SQ 深度。',
 'One entry combines identity, performance references and storage capacity; the values have different uses and units.')
group('set-list-fields','先找 entry，再讀其中的實際 Set ID',
 'Figure 343 選清單起點，344 定位一筆資料，345 才讀該 Set 的欄位。清單依 ID 排序，只包含處理查詢的控制器可存取的 Set。',[343,344,345],
 ('Figure 343：CDW11 bits 15:0','NVMSETID 是起始識別值，下限為含等號的 ≥。最大值 FFFFh；繼續列舉時不可回繞。','上一筆為 37，下一次可從 38 開始；可能直接取得 100，ID 不必連續。'),
 ('Figure 344：byte 0／bytes 127:1','NUMENT=0～31；其餘 header 保留。','31 筆加 header 為 128+31×128=4096 bytes。'),
 ('Figure 344：Entry i','i 是從 0 起算的 index；起點 128+i×128，末位為起點+127。','i=1 對應 byte offset 256，不能把 256 當作 Set ID。'),
 ('Figure 345：NSETID bytes 1:0／ENDGID bytes 3:2','前者識別本 Set；後者指出其耐用度群組。這裡的 byte 位置都相對 entry 起點。','Entry 1 的 NSETID 在整份清單 bytes 257:256；ENDGID 在 259:258。'),
 ('R4KRT bytes 11:8','每單位 100 ns；僅指 DTWIN 中、每個 Set 只有 1 筆 outstanding 命令時的 4 KiB 隨機讀取典型時間。','120×100 ns=12 μs，是典型值。兩個 SQ 同屬一 Set、各有 1 筆未完成，合計是 2，已非此測量條件。'),
 ('OWS bytes 15:12','最佳寫入大小以 bytes 表示；0 表示未指定。不同 namespace 格式不能共用 OWS 時，此欄宜為 0。','OWS=65536 表示 64 KiB，並非 65536 個 logical blocks，也不是允許的 SQ 項目數。'),
 ('TNVMSC bytes 31:16／UNVMSC bytes 47:32','均是 16-byte 容量值、單位為 bytes：一個是總容量，一個是未配置容量。','總容量 1,000,000、未配置 250,000，說明有部分空間尚未分給 namespace；與 64-entry SQ 的記憶體無關。'),
 ('entry 的保留區','bytes 7:4 與 127:48 不提供本篇可使用的屬性；保留區不納入容量或時間換算。','解析下一筆時直接移動 128 bytes，不能把最後一個已知欄位結尾當下一筆起點。'))

example(346, '查特定 NSID 的 NVMSETID，才能把 I/O 對象接到正確的 Set。',
 'CNS=08h、NSID21 的回覆在 bytes 11:10 為 09 00，解為 Set 9。若把 NSID 改成 FFFFFFFFh，這是能力查詢；若查詢成功，這個不回報的欄位為 0，不能拿來判斷 NSID21 的歸屬。',
 'NVMSETID for a specific active NSID supplies membership; an all-namespaces capability query does not.')
group('namespace-fields','回覆條件與相鄰兩種歸屬',
 '僅解釋 Figure 346 的 NVMSETID／ENDGID、查詢 NSID 與 Reported 欄，其他 namespace 屬性不影響此處的 Set 路由。',[346],
 ('CNS=08h／active NSID','查詢指定且目前可透過該控制器存取的 namespace，才回對應資料。inactive NSID 回全零結構。','全零回覆不能直接當成「這是一個正常的 Set 0 namespace」。'),
 ('NVMSETID bytes 11:10','NSID≠FFFFFFFFh 時表示 namespace 所屬 Set；不支援 NVM Sets 或沒有已格式化儲存空間時清 0。','本例為 09 00 → 0009h；選 SQ5，而不是因 NSID21 就找 SQ21。'),
 ('ENDGID bytes 13:12','同樣在特定 NSID 下指出其 Endurance Group；不支援該能力或無已格式化儲存空間時清 0。','同一個 Group 可能包含多個 Set，Group 相同不能代替 Set 相同。'),
 ('Reported：No','這兩個欄位在成功的 NSID=FFFFFFFFh 能力查詢中不回報歸屬，回覆為 0。不支援 Namespace Management 時，該查詢可被以 Invalid Namespace or Format 中止。','要路由 NSID21 的 I/O，重新查 21；不能用 FFFFFFFFh 的共同能力代替。'))

example(575, 'PRP1 的內容由 PC 決定，描述的是 SQ 記憶體，不是 namespace 資料位置。',
 'PC=1、4 KiB 記憶體頁時，00100000h 是對齊的 SQ 基底範例；00100080h 帶有 128-byte offset，違反這個對齊要求。PC=0 時則要把 PRP1 解成頁面清單的位址。',
 'PC determines whether PRP1 names contiguous queue memory or a PRP List; neither is a namespace address.')
example(576, 'QSIZE 選數量、QID 選名稱，64 筆 SQ3 要編成 003F0003h。',
 '高 16 bits 003Fh=63，還原筆數為 63+1=64；低 16 bits 0003h 選 SQ3。若高半部直接填 64，要求的會是 65 筆，而不是把 SQ3 改名成 SQ64。',
 'QSIZE encodes count minus one, while QID names the queue: 003F0003h creates a 64-entry SQ3.')
example(577, 'CQID 決定後續 I/O 的完成去處；PC 與 QPRIO 分別影響記憶體描述與仲裁。',
 '00020001h 表示 CQ2、PC=1、QPRIO=00b。若採一般 round robin，QPRIO 被忽略，不能只看 00b 就宣稱這個 SQ 享有 Urgent 優先級。',
 'CQID selects the completion destination; PC describes memory and QPRIO matters only under its specified arbitration mechanism.')
example(578, 'NVMSETID 在建立 SQ 時提供 Set 關聯，0 在這個命令明確表示沒有特定關聯。',
 '支援 SQA 且清單含 7 時，CDW12=00000007h 要求關聯 Set 7；改成 0 則沒有特定關聯。清單沒有 99 卻填 99，必須回 Invalid Field in Command。',
 'NVMSETID supplies the set association at creation; zero explicitly means no specific association in this command.')
example(579, '建立命令的錯誤值要搭配錯誤類別與觸發欄位，不能當作後續 I/O 的分流檢查表。',
 'CQ2 在合法編號範圍內卻未建立，對應 Completion Queue Invalid（此表 0h）；SQID3 已被使用，對應 Invalid Queue Identifier（1h）。不存在的 Set 使用 Figure 578 的 Invalid Field 規則，並不是這張表的 0h。',
 'Creation status values must be read with their status category and triggering fields; they do not specify later I/O routing validation.')
group('create-command-fields','把建立命令的參數拆成四個問題',
 '這裡以一般主機記憶體為前提，Figures 575～579 分別回答「佇列放哪、多少項、結果送哪、服務哪個 Set」。相關條件在此共用一次。',[575,576,577,578,579],
 ('Figure 575：PRP1 bits 63:0／PC','PC=1 指向實體連續 SQ 的基底；PC=0 指向 PRP List。兩者按 CC.MPS 對齊且 offset 必須為 0，非連續佇列的每個 PRP 也須為 0。','任一非零 offset 時，控制器宜回 PRP Offset Invalid。4 KiB 頁的基底範例是 00100000h。'),
 ('PRP List 的生命週期','若採 PC=0，主機必須維持清單位置及值，直到對應 Delete I/O SQ 成功或控制器重設。','建立成功不代表清單立即可改寫；控制器之後仍可能用它存取 SQ。'),
 ('Figure 576：QSIZE bits 31:16','深度採項目數減 1；0 或大於支援值時，控制器宜回 Invalid Queue Size。','64 筆填 003Fh；還需先完成 CC.IOSQES 初始化，並符合 CAP.MQES。'),
 ('Figure 576：QID bits 15:0','為新 SQ 指定編號，不得超過 Number of Queues 回報範圍；0、超出範圍或已使用時宜回 Invalid Queue Identifier。','SQ3 尚未建立且配置允許編號 3，才使用 QID=3。'),
 ('Figure 577：CQID bits 31:16','0 或超出支援範圍時必須回 Invalid Queue Identifier；範圍內但尚未建立時必須回 Completion Queue Invalid。','I/O 完成送 CQ2；Create I/O SQ 這條 Admin 命令本身的完成結果仍送 Admin CQ。'),
 ('QPRIO bits 2:1／PC bit 0','加權輪詢且含 Urgent class 時，00／01／10／11 分別為 Urgent／High／Medium／Low；其他仲裁必須忽略 QPRIO。PC=0 且 CAP.CQR=1 時宜回 Invalid Field。','round robin、CQ2、PC1 合成 00020001h，不表示設定了 Urgent 仲裁。bits 15:3 保留。'),
 ('Figure 578：NVMSETID bits 15:0','0 或 SQA 不受支援：沒有特定關聯。支援 SQA 且非零值不在 Set List：必須以 Invalid Field in Command 中止。','選 Set 7 填 00000007h；高 16 bits 保留。NSID 在建立命令中不負責選這個 Set。'),
 ('Figure 579：命令專用 0h／1h／2h','依序表示完成佇列未建立、佇列編號無效、佇列深度或項目大小初始化條件不符。','此表 0h 是命令專用狀態碼，不等於通用狀態類別的成功碼；需連同類別解讀。'))

SOURCES = {
 67: ('3.2.2','107','model','NVM Sets and Associated Namespaces'),
 338: ('5.2.14.2.1','370-372','support','Identify – Identify Controller Data Structure, I/O Command Set Independent'),
 751: ('8.1.21','708-709','support','Deterministic and Non-Deterministic Windows'),
 333: ('5.2.14','363','inventory','Identify – Command Dword 10'),
 334: ('5.2.14','363','inventory','Identify – Command Dword 11'),
 336: ('5.2.14','364-365','inventory','Identify – CNS Values'),
 343: ('5.2.14.2.4','414','inventory','Command Dword 11 - CNS Specific Identifier'),
 344: ('5.2.14.2.4','415','inventory','NVM Set List'),
 345: ('5.2.14.2.4','415','inventory','NVM Set Attributes Entry'),
 346: ('5.2.14.2.8','416,419','inventory','I/O Command Set Independent Identify Namespace Data Structure'),
 575: ('5.3.2','555','create','Create I/O Submission Queue – PRP Entry 1'),
 576: ('5.3.2','555','create','Create I/O Submission Queue – Command Dword 10'),
 577: ('5.3.2','555-556','create','Create I/O Submission Queue – Command Dword 11'),
 578: ('5.3.2','556','create','Create I/O Submission Queue – Command Dword 12'),
 579: ('5.3.2','556-557','create','Create I/O Submission Queue – Command Specific Status Values'),
}
