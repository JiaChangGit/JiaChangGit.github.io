"""Purposeful Lockdown process, scope, byte-layout and persistence comparisons."""
from scripts.nvme_reader_visuals import diagram, box, arrow, steps
from scripts.nvme_directives_visuals import table
from scripts.nvme_lockdown_content import bi


def illustration(key, lang='zh'):
    if key=='lockdown-model':
        return steps(bi('從意圖到可確認的限制','From intent to a verified restriction')[lang],bi([
          '先說清楚：要限制哪個操作、接收介面與控制器集合。',
          'Identify 查 CFLS／CCFLS，再讀 LID14h 的可禁止清單。',
          'Lockdown 填 SCP、OFI、IFC、CSEL／CSS、PRHBT，等完成。',
          '用相同範圍讀 LID14h 的目前禁止清單，確認設定結果。',
          '後續符合條件的命令被拒絕；解除與 power cycle 另依持續性規則判斷。'],[
          'Specify the operation, incoming interface and controller set.',
          'Check CFLS/CCFLS, then read the eligible-item list in LID14h.',
          'Submit Lockdown with the selectors and PRHBT; await completion.',
          'Read current prohibitions for the same scope to verify the result.',
          'Matching later commands are rejected; allowance and power cycles follow lifecycle rules.'])[lang],
          bi('查詢取得資訊；Lockdown 改變狀態；後續命令才接受限制檢查。來源：Base §8.1.5、§5.2.16。','Queries observe, Lockdown changes state, and later commands encounter the restriction. Sources: Base §§8.1.5, 5.2.16.')[lang])
    if key=='lockdown-targets':
        return table(bi('只改一個選擇，觀察受影響範圍','Change one selector to see its effect')[lang],
          bi(['固定條件','改變的欄位','限制涵蓋的對象'],['Fixed conditions','Changed selector','Affected target'])[lang],bi([
          ['FID06h、Admin Queue','CSEL0','全部控制器'],
          ['FID06h、Admin Queue','CSEL1、CSS7','控制器 7'],
          ['FID06h、Admin Queue','CSEL2、CSS7','primary7 所屬 secondaries，非 primary7 本身'],
          ['FID06h、controller7','IFC 由 0 改 2','從 Admin Queue 改為 Management Endpoint']],
          [['FID06h, Admin Queue','CSEL0','All controllers'],['FID06h, Admin Queue','CSEL1, CSS7','Controller7'],
           ['FID06h, Admin Queue','CSEL2, CSS7','Secondaries of primary7, excluding primary7 itself'],
           ['FID06h, controller7','IFC0 → IFC2','Management Endpoint instead of Admin Queue']])[lang],
          bi('每列假設相關能力與入口均受支援；這些選擇分別管控制器集合與接收入口。來源：Base Figures365、366。','Each row assumes the required capabilities and interfaces. Controller selection and incoming interface are independent dimensions. Sources: Base Figures365/366.')[lang])
    if key=='lockdown-basic':
        return table(bi('把 6 個 bytes 分成 header 與有效清單','Split six bytes into header and valid list')[lang],
          bi(['byte offset','範例值','如何解讀'],['Byte offset','Example value','Interpretation'])[lang],bi([
          ['0','12h','CS1：Admin 已禁止；SS2：FID'],['1～2','00 00','保留，不是清單內容'],
          ['3','02h','LNGTH=2，直接計數'],['4～5','06 07','2 筆 FID：06h、07h'],['6～511','保留','不解析為其他 FID']],
          [['0','12h','CS1: Admin prohibited; SS2: FID'],['1–2','00 00','Reserved, not list contents'],
           ['3','02h','LNGTH=2, a direct count'],['4–5','06 07','Two FIDs: 06h and07h'],['6–511','Reserved','Do not parse as additional FIDs']])[lang],
          bi('索引 0、offset4、FID06h 是第幾筆、存在哪、代表什麼的三種答案。來源：Base Figure276。','Index0, offset4 and FID06h answer three different questions: which entry, where it resides, and what it means. Source: Base Figure276.')[lang])
    if key=='lockdown-enhanced':
        return diagram(bi('A／B 的禁止狀態，如何變成兩種 Log','How A/B state produces the two log formats')[lang],
          bi('固定查 SCP2、CNTTS1；假設 subsystem 只有 A、B。全體增強清單保留 06h 的部分控制器資訊，一般格式只留下全體共同的 07h。來源：Base Figures276～278。',
             'Fix SCP2 and CNTTS1 and assume only A/B exist. The enhanced all-controller list retains partial-controller prohibitions for06h; basic format retains only common item07h. Sources: Base Figures276–278.')[lang],[
          box(20,20,345,90,[bi('控制器 A 目前禁止','Controller A prohibits')[lang],'FID 06h, 07h'],'command'),
          box(395,20,345,90,[bi('控制器 B 目前禁止','Controller B prohibits')[lang],'FID 07h'],'command'),
          arrow(190,110,190,175),arrow(565,110,565,175),
          box(20,175,720,75,[bi('相同 SCP／CNTTS，改變回覆格式','Same SCP/CNTTS, different response format')[lang]]),
          arrow(190,250,190,315),arrow(565,250,565,315),
          box(20,315,345,110,[bi('一般 ELPF0','Basic ELPF0')[lang],'LNGTH=1 → 07h']),
          box(395,315,345,110,['ELPF1 / CNTLID=FFFFh','06h: ACNTL0','07h: ACNTL1'],'success')],450)
    if key=='lockdown-command':
        return diagram(bi('同一目標：禁止與允許只差 bit4','Same target: prohibit and allow differ at bit4')[lang],
          bi('假設功能、controller7 與 FID06h 均符合條件，且 Lockdown 入口可執行。低位 SCP2 選 FID；高位 CSEL1 仍需 CDW14 的 CSS7 提供實際編號。來源：Base Figures365、366。',
             'Assumes capability, controller7, FID06h eligibility and an allowed Lockdown path. SCP2 selects FIDs; CSEL1 needs CSS7 in CDW14 to identify the controller. Sources: Base Figures365/366.')[lang],[
          box(20,20,720,80,['OPC=24h · CSEL1 · OFI06h · IFC0 · SCP2','CSS7 → CDW14=00070000h'],'command'),
          arrow(190,100,190,175),arrow(565,100,565,175),
          box(20,175,345,90,['PRHBT=1',bi('禁止：00010612h','Prohibit: 00010612h')[lang]]),
          box(395,175,345,90,['PRHBT=0',bi('允許：00010602h','Allow: 00010602h')[lang]],'success'),
          box(20,330,720,60,[bi('每次成功後，按相同目標讀回 LID14h','After success, query LID14h for the same target')[lang]])],415)
    if key=='lockdown-persistence':
        return table(bi('一個 subsystem power cycle 之後，哪些限制保留？','Which prohibitions survive one subsystem power cycle?')[lang],
          bi(['建立限制時的 CSEL','Lockdown Persistence','斷電循環後的規則'],['CSEL used to prohibit','Lockdown Persistence','Rule after the power cycle'])[lang],bi([
          ['0：全部控制器','已啟用','保留，後續 Lockdown 可解除'],['0：全部控制器','已停用','原禁止不跨 power cycle 保留'],
          ['1：單一控制器','任一狀態','不因 LDPE1 而跨 power cycle 保留'],['2：指定 primary 的 secondaries','任一狀態','同樣在 power cycle 或後續解除時結束']],
          [['0: all controllers','Enabled','Persists; subsequent Lockdown can allow'],['0: all controllers','Disabled','Does not persist across the power cycle'],
           ['1: one controller','Either state','LDPE1 does not grant power-cycle persistence'],['2: a primary’s secondaries','Either state','Ends at a power cycle or subsequent allowance']])[lang],
          bi('比較的是 power cycle；不能把一般 Controller Reset 代入這一欄。凍結與認證例外則在正文另行說明其條件。來源：Base §8.1.5。','This compares power cycles, not ordinary Controller Resets. The prose separately explains freeze and authentication conditions. Source: Base §8.1.5.')[lang])
    return ''
