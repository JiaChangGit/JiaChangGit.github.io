"""Purposeful scope, transition, permission and timing illustrations."""
from scripts.nvme_report_extension import bi
from scripts.nvme_reader_visuals import diagram,box,arrow
from scripts.nvme_directives_visuals import table

def illustration(key,lang='zh'):
    if key=='nwp-model':
        return diagram(bi('設定經由控制器送出，保護跟著 namespace','Configure through a controller; enforce at the namespace')[lang],
            bi('A、B 的箭頭都指向同一份namespace7；它們必須遵守相同保護。下方namespace8是另一個設定對象。此圖說明附接關係，不表示命令執行順序。來源：Base §8.1.18。',
               'Both A and B reach the same namespace 7 and must enforce its protection. Namespace 8 is a separate target. Arrows show attachment, not execution order. Source: Base §8.1.18.')[lang],[
             box(20,20,340,85,['Controller A',bi('送出 Set FID84h','Submit Set FID84h')[lang]],'command'),
             box(400,20,340,85,['Controller B',bi('同樣遵守 WPS','Enforce the same WPS')[lang]],'command'),
             arrow(190,105,190,165),arrow(570,105,570,165),
             box(20,165,720,90,['Namespace 7 · WPS=1',bi('所有附接的控制器共同遵守','Enforced by every attached controller')[lang]],'success'),
             box(20,305,720,80,['Namespace 8 · WPS=0',bi('獨立的 namespace 設定','A separate namespace setting')[lang]])],410)
    if key=='nwp-transitions':
        return diagram(bi('四種狀態：先看起點，再看事件','Four states: read the starting state and trigger')[lang],
            bi('普通箭頭為Set Features；通往2、3的箭頭另須能力、WPC及相關配置條件成立。圖中2回到0的箭頭由power cycle觸發，3沒有解除箭頭。為了讓線條清楚，兩條垂直分支分別標明可從0或1出發。來源：Base Figures735／736、§5.2.30.1.38。',
               'Ordinary arrows are Set Features; entry into 2/3 additionally requires support, WPC and applicable configuration conditions. The return arrow from 2 to 0 is triggered by power cycling; 3 has no exit. Both vertical branches explicitly permit starting at 0 or 1. Sources: Base Figures735/736, §5.2.30.1.38.')[lang],[
             box(50,30,275,90,['0 · No Write Protect',bi('建立時的狀態','Initial state')[lang]],'success'),
             box(435,30,275,90,['1 · Write Protect',bi('可由 Set 解除','Reversible by Set')[lang]],'command'),
             arrow(325,55,435,55),
             '<path d="M435,95 L325,95 M332,91 L325,95 L332,99" class="v-line"/>',
             box(30,185,330,65,[bi('從 0 或 1；要求 WPS2','From 0 or 1; request WPS2')[lang]],'command'),
             box(400,185,330,65,[bi('從 0 或 1；要求 WPS3','From 0 or 1; request WPS3')[lang]],'command'),
             arrow(195,250,195,315),arrow(565,250,565,315),
             box(30,315,330,110,['2 · Until Power Cycle',bi('Set 不能改變此狀態','Set cannot change this state')[lang]],'decision'),
             box(400,315,330,110,['3 · Permanent',bi('沒有解除路徑','No release path')[lang]],'decision'),
             arrow(195,425,195,485),
             box(30,485,330,70,['Power cycle → WPS0'],'success'),
             box(400,485,330,70,[bi('power cycle 後仍為 3','Power cycle retains 3')[lang]])],580)
    if key=='nwp-controls':
        return table(bi('相同的數字，放在不同欄位意思不同','The same number has different meanings by field')[lang],
          bi(['觀察到的值','它回答的問題','不能推出的結論'],['Observed value','What it answers','What it does not establish'])[lang],
          bi([['NWPC=03h','支援0／1及2，不支援3','目前已永久保護'],['WPC=03h','允許處理進入2與3的要求','所有namespace已保護'],['WPS=3','這個namespace已永久保護','這是一份支援bitmap'],['MDS=1','多domain；禁止進入2','禁止所有寫入保護']],
             [['NWPC=03h','Supports 0/1 and 2, not 3','Currently permanent'],['WPC=03h','Permits requests to enter 2/3','All namespaces protected'],['WPS=3','This namespace is permanent','A support bitmap'],['MDS=1','Multiple domains; state 2 prohibited','All protection prohibited']])[lang],
          bi('每列獨立示範欄位意義，不是同一台裝置的完整配置。Source：Base Figures338／756／541。',
             'Rows independently illustrate field meanings; they do not describe one complete device configuration. Sources: Base Figures338/756/541.')[lang])
    if key=='nwp-configure':
        return diagram(bi('成功切入保護，包含先把既有快取提交到媒體','Entering protection includes committing cached data')[lang],
          bi('範例採WPS0 → 1、NSID7。主機宜先等舊命令完成；控制器在轉換時提交該namespace的快取資料與metadata。完成後才提交的命令必須用新設定；較早在途的命令不能一概推定。來源：Base §§5.2.30.1、5.2.30.1.38、5.2.30.4。',
             'Example: WPS0 → 1, NSID7. The host should finish earlier commands first; the controller commits associated cached data and metadata during the transition. Commands submitted after success use the new setting; previously outstanding commands are not guaranteed to do so. Sources: Base §§5.2.30.1, 5.2.30.1.38, 5.2.30.4.')[lang],[
          box(20,20,720,70,[bi('主機：先等待前一批命令完成','Host: finish outstanding commands first')[lang]],'command'),arrow(380,90,380,130),
          box(20,130,720,90,['Set · NSID7 · FID84h · SV0','CDW11 = 00000001h'],'command'),arrow(380,220,380,260),
          box(20,260,720,95,[bi('控制器：將此 namespace 的快取提交到媒體','Controller: commit this namespace’s cache to media')[lang],bi('包含 data 與 metadata','Includes data and metadata')[lang]]),arrow(380,355,380,395),
          box(20,395,720,75,[bi('完成設定後，回覆成功 CQE','Complete the update, then return successful CQE')[lang]],'success'),arrow(380,470,380,510),
          box(20,510,720,75,['Get · SEL0 → CQE DW0 = 1',bi('確認目前保護狀態','Confirm current protection')[lang]],'success')],610)
    if key=='nwp-commands':
        return table(bi('命令名稱只是起點，實際動作決定判斷','The name is only the start; inspect the actual action')[lang],
          bi(['命令或情境','是否被寫入保護阻擋','原因'],['Command or case','Protection-related handling','Reason'])[lang],
          bi([['Read／Compare／Verify','正常處理；仍可能有其他錯誤','保護不封鎖這些操作'],['Dataset Management修改受保護媒體','必須失敗','表內命令仍受註腳1約束'],['受保護NSID的Flush','成功且無作用','進入保護時已提交快取'],['Format指向8但也修改受保護的7','Namespace is Write Protected','實際影響包含受保護namespace'],['Sanitize會修改受保護namespace','Namespace is Write Protected','沒有指定NSID也須遵守保護']],
             [['Read/Compare/Verify','Processed normally; other errors remain possible','Protection does not block these operations'],['Dataset Management modifying protected media','Must fail','Listed commands still obey footnote 1'],['Flush for a protected NSID','Success, no effect','Cache committed on entry'],['Format names 8 but also modifies protected 7','Namespace is Write Protected','Actual scope includes a protected namespace'],['Sanitize would modify a protected namespace','Namespace is Write Protected','Absence of an NSID does not bypass protection']])[lang],
          bi('每列示範不同判斷，不構成執行順序。完整允許清單與三項註腳在圖表閱讀區逐組說明。來源：Base Figure737及其後條文。',
             'Rows illustrate separate decisions, not a sequence. The complete allowed list and three footnotes are explained in the figure guide. Source: Base Figure737 and the following text.')[lang])
    if key=='nwp-observe':
        return table(bi('先問正在觀察什麼，再選資料來源','Choose the source for the question being asked')[lang],
          bi(['想回答的問題','查看哪裡','代表性判讀'],['Question','Where to look','Example interpretation'])[lang],
          bi([['namespace7目前是哪種保護？','Get FID84h、SEL0的WPS','1是一般Write Protect'],['裝置是否支援永久保護？','Identify的NWPC bit2','1是支援，不是已進入'],['為何要求改變狀態失敗？','完成狀態＋原狀態／控制條件','WPS2要求0：Feature Not Changeable'],['是否回報全體媒體唯讀警告？','SMART的AMRO','不能只因WPS變化而設1']],
             [['What protects namespace7 now?','WPS from Get FID84h, SEL0','1 means Write Protect'],['Is permanent protection supported?','Identify NWPC bit2','1 advertises support, not activation'],['Why did a state-change request fail?','Completion plus current state/controls','WPS2 to 0: Feature Not Changeable'],['Is an all-media read-only warning reported?','SMART AMRO','A WPS change alone must not assert it']])[lang],
          bi('這些資料可同時存在；它們分別描述設定、能力、一次命令的結果與健康狀況。來源：Base §8.1.18與Figures338／541／554／213。',
             'These observations coexist: configuration, capability, a command result and health are separate facts. Sources: Base §8.1.18 and Figures338/541/554/213.')[lang])
    return ''
