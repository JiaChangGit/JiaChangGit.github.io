"""Purposeful FDP diagrams and comparisons, shared by equivalent overview posts."""
from scripts.nvme_reader_visuals import diagram, box, arrow, steps
from scripts.nvme_directives_visuals import table
from scripts.nvme_fdp_content import bi


def illustration(key, lang='zh'):
    if key == 'fdp-model':
        return diagram(bi('一筆 Write 的兩個選擇','The two choices within one Write')[lang],
          bi('LBA 決定邏輯位置；PID 透過 namespace 的映射選目前的 RU。圖中 RU A 是說明用名稱，不是可填進命令的地址。來源：Base 70、730。',
             'LBA selects the logical address. PID follows the namespace mapping to a current RU. RU A is an illustrative label, not a command address. Sources: Base 70/730.')[lang], [
          box(20,20,720,60,['Write · NSID A · LBA 128 · PID 8001h'],'command'),
          box(20,135,280,75,['LBA 128',bi('namespace 邏輯位置','Namespace logical address')[lang]]),
          box(335,135,405,75,['RGIF = 2 → RGID 2 / PHNDL 1']),
          arrow(160,80,160,135),arrow(530,80,530,135),
          box(335,265,405,75,[bi('A 的映射表：PH1 → RUH3','A mapping: PH1 → RUH3')[lang]]),
          arrow(530,210,530,265),
          box(335,395,405,75,['RUH3 / RG2 → RU A',bi('目前寫入的回收單位','Current write destination')[lang]],'success'),
          arrow(530,340,530,395)],500)
    if key == 'fdp-isolation':
        return table(bi('同一 RG 內：只改隔離類型，觀察搬移目的','Same RG: changing only the isolation type')[lang],
          bi(['RUH 類型','X、Y 的新資料','控制器搬移 X、Y 舊資料後'],['RUH type','New data from X and Y','After relocating old X/Y data'])[lang],
          bi([['Initially Isolated','不同 RU','允許進同一個目的 RU'],['Persistently Isolated','不同 RU','X、Y 必須保留不同目的 RU']],
             [['Initially Isolated','Separate RUs','May share a destination RU'],['Persistently Isolated','Separate RUs','Must retain separate destination RUs']])[lang],
          bi('兩種都允許在同一 RG 內搬移；差別在不同 RUH 的資料能否合併，不是能否搬移。來源：Base 295、731、732。',
             'Both allow relocation within the same RG. The difference is whether data from different RUHs can be combined. Sources: Base 295/731/732.')[lang])
    if key == 'fdp-config':
        return diagram(bi('8001h 如何變成 RG 2 與 PH 1','How 8001h selects RG 2 and PH 1')[lang],
          bi('說明性配置 RGIF=2。方塊寬度為排版調整，以標示的 bits 為準；解出 PH 後還要查 namespace 映射。來源：Base 294、297。',
             'Illustrative RGIF=2. Box widths aid layout; labels define actual bit widths. PH still requires the namespace mapping. Sources: Base 294/297.')[lang],[
          box(20,20,720,60,['PID = 8001h = 1000 0000 0000 0001b'],'command'),
          box(20,140,275,85,['bits 15:14','10b → RGID 2']),
          box(320,140,420,85,['bits 13:0','00 0000 0000 0001b → PHNDL 1']),
          arrow(160,80,160,140),arrow(530,80,530,140),
          box(20,285,720,65,[bi('查 namespace A：PH1 → RUH3，再選 RG2','Look up A: PH1 → RUH3, then select RG2')[lang]],'success')],380)
    if key == 'fdp-enable':
        return steps(bi('先建立配置，再讓 Write 使用它','Configure before using placement in Writes')[lang],bi([
          '查 FDPS → LID20h 選目前有效的配置。',
          '準備好目標 Endurance Group：修改 FID1Dh 前必須沒有 namespace。',
          'Set FID1Dh、SV=1，填 ENDGID、FDPCIDX、FDPE。',
          '重新查資料格式 → Create namespace，建立 PHNDL→RUHID。',
          '設定所需事件 → 對 namespace 啟用 Data Placement Directive → 查狀態與 cache。',
          'Write 使用 PID；後續以 Status、Update、Statistics、Events 觀察並管理。'],[
          'Check FDPS and choose a currently valid configuration from LID20h.',
          'Prepare the Endurance Group: no namespaces may remain before changing FID1Dh.',
          'Set FID1Dh with SV=1, ENDGID, FDPCIDX and FDPE.',
          'Refresh data formats, then create namespaces with PHNDL→RUHID mappings.',
          'Configure events, enable the namespace Data Placement Directive, and inspect status/cache.',
          'Use PIDs in Writes; observe and manage with Status, Update, Statistics and Events.'])[lang],
          bi('這是設定依存關係；namespace 的資料處理必須先完成，不能把群組改配置當成無條件切換。來源：Base §8.1.12.2。',
             'This is an ordering of configuration dependencies. Existing namespace data must be handled before reconfiguration. Source: Base §8.1.12.2.')[lang])
    if key == 'fdp-directive':
        return table(bi('命令名字相似，目標卻不同','Similar command names, different targets')[lang],
          bi(['目的','入口與選擇','改變或取得什麼'],['Purpose','Command and selector','State changed or returned'])[lang],
          bi([['群組啟用 FDP','Set Features / FID1Dh','Endurance Group 的配置'],['namespace 使用 PID','Directive Send / Identify / Enable target02h','Data Placement 啟用狀態'],['查每個 PID 狀態','I/O Management Receive / MO1','映射、剩餘量、估計時間'],['改到空 RU','I/O Management Send / MO1','所列 PID 的目前 RU 參照']],
             [['Enable FDP for a group','Set Features / FID1Dh','Endurance Group configuration'],['Use explicit PIDs','Directive Send / Identify / Enable target02h','Data Placement enablement'],['Inspect PID state','I/O Management Receive / MO1','Mapping, capacity, remaining time'],['Select an empty RU','I/O Management Send / MO1','Current RU references of listed PIDs']])[lang],
          bi('Data Placement 自身沒有 Directive Send／Receive 操作，管理 RU 要走 I/O Management。來源：Base §8.1.9.4、§7.3–7.4。',
             'Data Placement has no direct Directive Send/Receive operations; RU management uses I/O Management. Sources: Base §8.1.9.4 and §§7.3–7.4.')[lang])
    if key == 'fdp-status':
        return table(bi('同一個 PH，跨 4 個 RG 的狀態可能不同','One PH can have different state across four RGs')[lang],
          ['PID / PH / RG','RUHID','RUAMW (blocks)','EARUTR (s)'],
          [['0001h / 1 / 0','3','8','30'],['4001h / 1 / 1','3','4','15'],['8001h / 1 / 2','3','6','20'],['C001h / 1 / 3','3','0','0']],
          bi('RGIF=2 的說明性快照，並非容量保留。最後一列 RUAMW=0 是無剩餘可寫 blocks；EARUTR=0 則是未回報時間，兩個 0 意義不同。來源：NVM 21。',
             'Illustrative RGIF=2 snapshot, not a capacity reservation. In the last row, RUAMW=0 means no available blocks, while EARUTR=0 means no time reported. Source: NVM 21.')[lang])
    if key == 'fdp-update':
        return diagram(bi('相同 PID，切換的是目前 RU','Same PID, a different current RU')[lang],
          bi('先協調並完成相關 I/O，再 Update 並等完成，才能讓下一批有明確的操作邊界；若重疊處理，Write 可落在切換前或後。舊 RU 的資料仍需按其生命週期管理。來源：Base §7.4.1.1。',
             'Coordinate and complete relevant I/O before Update, then await Update completion before the next batch. Concurrent Writes may use either RU. Old data retains its own lifecycle. Source: Base §7.4.1.1.')[lang],[
          box(20,20,310,80,['PID 8001h → RU A',bi('已寫入這一批資料','Current batch written')[lang]],'command'),
          box(420,20,320,80,['PID 8001h → RU B',bi('空 RU 接下一批','Empty RU for next batch')[lang]],'success'),
          arrow(330,60,420,60),
          box(20,165,720,60,[bi('Update：改參照；PH1 → RUH3 的映射不變','Update changes the reference; PH1 → RUH3 stays')[lang]]),
          box(20,280,720,65,[bi('RU A 的有效 LBA 不會因為 Update 就消失','Valid LBAs in RU A do not disappear on Update')[lang]])],370)
    if key == 'fdp-event-record':
        return table(bi('先看有效位，再決定哪些數字可用','Check validity before using values')[lang],
          bi(['位元','為 1 時可讀','為 0 時怎麼處理'],['Flag','Valid when one','Interpretation when zero'])[lang],
          bi([['PIV','PID；03h事件為主機原值','PID 保留'],['NSIDV','NSID','NSID 清0並忽略'],['LV','RGID 與 RUHID','兩欄清0並忽略'],['LBAV（80h NVM 擴充）','其中一個被搬移 LBA','LBA 清0並忽略']],
             [['PIV','PID; original input for type03h','PID reserved'],['NSIDV','NSID','NSID zero and ignored'],['LV','RGID and RUHID','Both zero and ignored'],['LBAV (80h NVM extension)','One relocated LBA','LBA zero and ignored']])[lang],
          bi('欄位清 0 不代表真的選到了 0 號物件；要先確認有效位。來源：Base 303、NVM 116。',
             'A zeroed field does not identify object zero unless its validity permits that interpretation. Sources: Base 303 and NVM 116.')[lang])
    if key == 'fdp-lifetime':
        return table(bi('結束一批資料時，3 種操作各改什麼','Three operations at a data-lifecycle boundary')[lang],
          bi(['操作','主要改變','不能由此推論'],['Operation','Primary change','What it does not establish'])[lang],
          bi([['RUH Update','未來寫入使用的 RU 參照','舊資料已失效或已擦除'],['DSM / AD=1','向控制器提供不再需要的 LBA 範圍','立即擦除，或改了 PH→RUH 映射'],['變更 FID1Dh','群組 FDP 配置；清事件與統計','可在現有 namespace 尚存時任意切換']],
             [['RUH Update','RU reference for future writes','Old data invalidation or erasure'],['DSM / AD=1','Ranges no longer needed by the host','Immediate erasure or a PH→RUH remapping'],['Change FID1Dh','Group configuration; clears events/statistics','Arbitrary reconfiguration with namespaces still present']])[lang],
          bi('用「誰、改了什麼、何時生效」讀操作，比把它們都叫回收更清楚。來源：Base §7.4、§8.1.12、NVM §3.3.3。',
             'Separate the object and effect of each operation rather than treating them as one reclamation action. Sources: Base §7.4, §8.1.12 and NVM §3.3.3.')[lang])
    return ''
