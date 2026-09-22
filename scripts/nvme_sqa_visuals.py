"""Purposeful views of membership, operating state, identifiers and routing."""
from scripts.nvme_report_extension import bi
from scripts.nvme_reader_visuals import diagram, box, arrow
from scripts.nvme_directives_visuals import table


def illustration(key, lang='zh'):
    if key == 'sqa-model':
        return diagram(bi('儲存歸屬、工作提示、完成路徑各有一條關係','Storage membership, queue hints and completion paths')[lang],
            bi('由上往下追蹤。上層是 namespace 的儲存歸屬；中層表示主機為各 SQ 選擇相符的 Set；下層只表示完成結果匯入同一 CQ。這些連線不表示把 namespace 容量搬進主機佇列。來源：Base §3.2.2、§3.3、§5.3.2、§8.1.28。',
               'Follow top to bottom: namespace membership, the matching set chosen for each SQ, then the shared destination for completions. The links do not move namespace storage into host queues. Sources: Base §§3.2.2, 3.3, 5.3.2 and 8.1.28.')[lang], [
            box(20,20,345,100,['NVM Set 7','A: NSID11 · B: NSID12']),
            box(395,20,345,100,['NVM Set 9','C: NSID21']),
            arrow(192,120,192,190),arrow(567,120,567,190),
            box(20,190,345,100,['SQ3 + SQ4','NVMSETID = 7'],'command'),
            box(395,190,345,100,['SQ5','NVMSETID = 9'],'command'),
            arrow(192,290,192,360),arrow(567,290,567,360),
            box(20,360,720,85,['CQ2',bi('完成結果共用；Set 歸屬維持不變','Shared completions; set membership unchanged')[lang]],'success')],470)
    if key == 'sqa-support':
        return table(bi('同一個控制器，三種問題要分別回答','Three separate questions about one controller')[lang],
            bi(['觀察到的資訊','足以說明什麼','還不能據此推出什麼'],['Observation','What it establishes','What it does not establish'])[lang],
            bi([
                ['CTRATT 三個 bit 為 1','控制器支援 SQA、NVM Sets、PLM','Set 7 現在已啟用模式'],
                ['Set 7 已啟用模式','該 Set 使用模式的工作視窗規則','此刻必定在 DTWIN'],
                ['Set 7 目前在 DTWIN','現在能在符合條件時提供確定性延遲','主機可無限增加工作量，或保證全部 PCIe 延遲'],
                ['SQ3 已關聯 Set 7','控制器收到此 SQ 的預定用途','主機之後一定送對每筆 I/O']],
                [['Three CTRATT bits are one','SQA, NVM Sets and PLM are supported','Mode is currently enabled for set 7'],
                 ['Mode enabled for set 7','Operating-window rules apply to that set','The set must currently be in DTWIN'],
                 ['Set 7 is in DTWIN','Deterministic latency under its conditions','Unlimited workload or a bound on all PCIe latency'],
                 ['SQ3 associated with set 7','The controller received the queue hint','Every later I/O is necessarily routed correctly']])[lang],
            bi('由支援走到實際效果，中間仍有設定、視窗及主機分流條件。來源：Base §8.1.28、§8.1.21、Figure 338。',
               'Support, configuration, window state and host routing remain distinct. Sources: Base §§8.1.28, 8.1.21 and Figure 338.')[lang])
    if key == 'sqa-inventory':
        return table(bi('清單位置不是 Set 識別值','List position is not a set identifier')[lang],
            bi(['清單內的索引','整份清單的 byte 範圍','entry 內的 NSETID','建立 SQ 時使用'],
               ['List index','Byte range in the list','NSETID inside the entry','Use at SQ creation'])[lang],
            bi([['0','128～255','7','CDW12=00000007h'],['1','256～383','9','CDW12=00000009h']],
               [['0','128–255','7','CDW12=00000007h'],['1','256–383','9','CDW12=00000009h']])[lang],
            bi('說明性範例 NUMENT=2。先用位置找到資料，再從資料取識別值；不要把左邊的 0／1 或 128／256 填成 Set ID。來源：Base Figures 344／345／578。',
               'Illustrative NUMENT=2: use the position to find the record, then read its identifier. Do not encode indices 0/1 or offsets 128/256 as set IDs. Sources: Base Figures 344/345/578.')[lang])
    if key == 'sqa-create':
        return table(bi('把 64-entry SQ3 的建立參數拆開檢查','Check the parameters for a 64-entry SQ3')[lang],
            bi(['命令位置','本例如何組成','送出的值'],['Command location','Composition in this example','Encoded value'])[lang],
            bi([
                ['CDW10','高 16 bits：64−1=63；低 16 bits：QID3','003F0003h'],
                ['CDW11','高 16 bits：CQID2；PC=1；QPRIO=0','00020001h'],
                ['CDW12','低 16 bits：Set 7；高 16 bits 保留','00000007h'],
                ['PRP1','4 KiB 對齊、已配置的連續主機記憶體','0000000000100000h']],
                [['CDW10','Upper 16: 64−1=63; lower 16: QID3','003F0003h'],
                 ['CDW11','Upper 16: CQID2; PC=1; QPRIO=0','00020001h'],
                 ['CDW12','Lower 16: set 7; upper 16 reserved','00000007h'],
                 ['PRP1','Allocated contiguous host memory, 4 KiB aligned','0000000000100000h']])[lang],
            bi('前提：CQ2 已建立，Set 7 可用且支援 SQA，控制器已初始化且支援此佇列深度；採 round robin，所以 QPRIO 被忽略。來源：Base §5.3.2、Figures 575～578。',
               'Assumes existing CQ2, available set 7, SQA support, initialized controller and sufficient depth. Round-robin arbitration ignores QPRIO. Sources: Base §5.3.2 and Figures 575–578.')[lang])
    if key == 'sqa-routing':
        return diagram(bi('以命令的 NSID 選 SQ，而不是以 CQID 選儲存空間','Select an SQ from NSID; CQID does not select storage')[lang],
            bi('本例只追蹤 NSID21。SQ3 即使較空，也不符合 Set 9 的提示；兩個 SQ 共用 CQ2 不會改變這個判斷。來源：Base §8.1.28、Figures 346／578。',
               'Follow NSID21. A less busy SQ3 still has the wrong set hint; sharing CQ2 does not change the decision. Sources: Base §8.1.28 and Figures 346/578.')[lang],[
            box(20,20,720,70,['I/O · NSID21']),arrow(380,90,380,145),
            box(20,145,720,85,['Identify namespace → NVMSETID = 9',bi('先確認資料對象的儲存歸屬','First establish storage membership')[lang]],'command'),
            arrow(190,230,190,295),arrow(565,230,565,295),
            box(20,295,345,105,['SQ5 → Set 9',bi('相符：使用 SQ5','Match: use SQ5')[lang]],'success'),
            box(395,295,345,105,['SQ3 → Set 7',bi('不符：不要選 SQ3','Mismatch: do not select SQ3')[lang]],'decision')],430)
    return ''
