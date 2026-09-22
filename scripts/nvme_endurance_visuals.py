"""Relationship, numerical and temporal views supporting six lessons."""
from scripts.nvme_report_extension import bi
from scripts.nvme_reader_visuals import diagram, box, arrow
from scripts.nvme_directives_visuals import table

def illustration(key,lang='zh'):
    if key=='ege-model':
        return diagram(bi('一個設定，兩種查詢：從條件走到資料','One configuration, two queries: from condition to data')[lang],
          bi('沿箭頭讀：符合已啟用的警告，Group 識別值才列入清單；主機取出 ID，再查該組健康資料。通知主機還有 FID0Bh 與 AER 的條件，後文再接上。來源：Base §§5.2.13.1.10、5.2.13.1.15、5.2.30.1.17。',
          'Follow the arrows: an enabled warning adds the group ID to the list; the host uses that ID to query its health data. Host notification also requires FID0Bh and AER, covered later. Sources: Base §§5.2.13.1.10, 5.2.13.1.15, 5.2.30.1.17.')[lang],[
          box(20,20,720,85,['FID18h · ENDGID7 · mask05h',bi('選擇備用容量與可靠度警告','Select spare and reliability warnings')[lang]],'command'),
          arrow(380,105,380,155),
          box(20,155,720,85,['LID0Fh · [7]',bi('清單只指出要查看哪一組','The list identifies which group needs inspection')[lang]]),
          arrow(380,240,380,290),
          box(20,290,720,100,['LID09h · LSI=7 · 512 bytes',bi('讀警告、壽命估計、流量與容量','Read warnings, wear estimates, traffic and capacity')[lang]],'success')],415)
    if key=='ege-health':
        return table(bi('EGCW=05h 時，哪些結論有依據？','Which conclusions follow from EGCW=05h?')[lang],
          bi(['觀察項目','本例判讀','不能代替的判斷'],['Observation','Interpretation','Not established'])[lang],
          bi([['bit0=1；AVSP8 < AVSPT10','備用容量低於門檻','壽命只剩8%'],['bit2=1','Group 可靠度下降','所有其他 Group 都相同'],['bit3=0','此欄未回報整組唯讀警告','所有 namespace 都一定可以寫'],['PUSED=103','已超過估計耐用度的100%','媒體已故障，或剩餘容量為負']],
             [['bit0=1; AVSP8 < AVSPT10','Spare below threshold','Only 8% of life remains'],['bit2=1','Group reliability degraded','Every other group is affected'],['bit3=0','No group-wide read-only warning here','Every namespace must be writable'],['PUSED=103','More than 100% estimated endurance used','Media failure or negative free capacity']])[lang],
          bi('狀態 bit 與百分比要一起看，但各自回答不同問題。bit3=0 並未排除 namespace 自己的寫入保護設定。來源：Base Figure 225。',
          'State bits and percentages answer different questions. A clear bit3 does not rule out namespace write protection. Source: Base Figure 225.')[lang])
    if key=='ege-traffic':
        return table(bi('同樣是數字 3，單位決定它的意思','The value 3 means different things in different fields')[lang],
          bi(['欄位','數值3代表什麼','若是0'],['Field','Meaning of 3','Meaning of zero'])[lang],
          bi([['DUR／DUW／MUW','2,000,000,001～3,000,000,000 bytes','未回報這項數值'],['HRC／HWC','3 筆已完成的對應類別命令','計數為0'],['TEGCAP／UEGCAP','3 bytes（僅示範單位）','未回報容量'],['NUMENT（LID0Fh）','清單有3筆','清單沒有項目']],
             [['DUR/DUW/MUW','2,000,000,001–3,000,000,000 bytes','Not reported'],['HRC/HWC','3 completed commands of the defined class','Count is zero'],['TEGCAP/UEGCAP','3 bytes (unit illustration only)','Capacity not reported'],['NUMENT (LID0Fh)','3 list entries','No entries']])[lang],
          bi('TEGCAP=3 只用來比較單位，不暗示裝置真的採3-byte容量。資料量是十億 bytes 向上取整；容量和命令次數沒有這個倍率。來源：Base Figures 225／261。',
          'TEGCAP=3 illustrates the unit, not a practical device size. Traffic rounds up in billions of bytes; capacities and counts do not use that multiplier. Sources: Base Figures 225/261.')[lang])
    if key=='ege-configure':
        return diagram(bi('先選每組的警告，再開控制器通知','Select per-group warnings, then enable controller notification')[lang],
          bi('兩個設定的範圍不同。上層決定是否新增 Group 項目，下層決定是否把新增動作通知主機；底下的 AER 才承接通知結果。來源：Base Figures 493／474、§5.2.2。',
          'The settings have different scopes: the first selects causes for adding group entries; the second enables a host notice for additions. An outstanding AER carries the result. Sources: Base Figures 493/474, §5.2.2.')[lang],[
          box(20,20,720,90,['FID18h · Group7',bi('CDW11 = 00050007h；警告 bit0 + bit2','CDW11 = 00050007h; warning bits 0 + 2')[lang]],'command'),
          arrow(380,110,380,155),
          box(20,155,720,75,[bi('已啟用的警告成立 → 0Fh 新增 Group7','Enabled warning true → add group7 to 0Fh')[lang]]),
          arrow(380,230,380,275),
          box(20,275,720,80,['FID0Bh · controller',bi('EGEALCN bit14=1；允許通知','EGEALCN bit14=1; enable the notice')[lang]],'command'),
          arrow(380,355,380,400),
          box(20,400,720,80,['AER → CQE DW0 = 000F0602h',bi('通知含 log 與事件類型；Group ID 在清單裡','Notice gives log and event type; group IDs are in the list')[lang]],'success')],505)
    if key=='ege-aggregate':
        return table(bi('把 16-byte 回覆拆開，只有3筆ID','Decode a 16-byte response containing only three IDs')[lang],
          bi(['byte位置','資料內容','讀者應取得的值'],['Byte position','Data','Decoded value'])[lang],
          bi([['0～7','03 00 00 00 00 00 00 00','NUMENT=3'],['8～9','01 00','Entry1：ENDGID1'],['10～11','02 00','Entry2：ENDGID2'],['12～13','07 00','Entry3：ENDGID7'],['14～15','00 00','尾端補零；不是Entry4']],
             [['0–7','03 00 00 00 00 00 00 00','NUMENT=3'],['8–9','01 00','Entry1: ENDGID1'],['10–11','02 00','Entry2: ENDGID2'],['12–13','07 00','Entry3: ENDGID7'],['14–15','00 00','Padding, not Entry4']])[lang],
          bi('說明性範例：14 bytes 有效內容，4個dword傳輸，NUMD=3。Group7 所在 offset12 是位置，不是識別值。來源：Base Figures 261／204。',
          'Illustration: 14 meaningful bytes, four transferred dwords, NUMD=3. Offset12 locates group7; it is not its identifier. Sources: Base Figures 261/204.')[lang])
    if key=='ege-service':
        return diagram(bi('逐組確認與清單通知確認，改變的狀態不同','Group acknowledgement and notice acknowledgement affect different state')[lang],
          bi('先假設過程中沒有新事件，並已處理持續警告的再次通知政策。每個框同時列出動作與結果；RAE1只查看，RAE0成功才確認。來源：Base §§5.2.2、5.2.13.1.15、3.2.3。',
          'Assume no new events during this illustration and that persistent-condition reporting has been addressed. Each box pairs an action with its result. RAE1 inspects; successful RAE0 reads acknowledge. Sources: Base §§5.2.2, 5.2.13.1.15, 3.2.3.')[lang],[
          box(20,20,720,85,['AER notice → read 0Fh, RAE1',bi('取得 [7]；保留通知與清單項目','Read [7]; retain notice and entry')[lang]]),arrow(380,105,380,150),
          box(20,150,720,85,['read 09h / Group7, RAE1',bi('取得當下健康資料；項目仍在','Read current health data; entry remains')[lang]]),arrow(380,235,380,280),
          box(20,280,720,85,['read 09h / Group7, RAE0 → success',bi('確認 Group7 事件；移除 [7]','Acknowledge group7; remove its entry')[lang]],'command'),arrow(380,365,380,410),
          box(20,410,720,85,['read 0Fh, RAE0 → success',bi('確認清單變更通知；查看最新清單','Acknowledge aggregate notice; inspect the returned list')[lang]],'success')],520)
    return ''
