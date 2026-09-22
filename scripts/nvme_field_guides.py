"""Authored relationships shared by related figures, with explicit membership.

Groups are rendered once per tutorial. Every figure links to its group, and
every group states what its fields do together instead of repeating a caption.
"""

GUIDES = {}
MEMBERS = {}


def guide(source, numbers, key, title, relation, rows):
    ident = source + '-' + key
    GUIDES[ident] = dict(id=ident, title=title, relation=relation, rows=rows)
    for number in numbers:
        token = (source, int(number))
        if token in MEMBERS:
            raise ValueError(f'Duplicate field guide: {token}')
        MEMBERS[token] = ident


def get(figure):
    if figure['report_id'] == 'base-sq-associations':
        from scripts.nvme_sqa_figures import guide as selected
        return selected(figure)
    if figure['report_id'] == 'base-read-recovery-level':
        from scripts.nvme_rrl_figures import guide as selected
        return selected(figure)
    if figure['report_id'] == 'base-command-feature-lockdown':
        from scripts.nvme_lockdown_figures import guide as selected_guide
        return selected_guide(figure)
    if figure['report_id'] == 'base-flexible-data-placement':
        from scripts.nvme_fdp_figures import guide as selected_guide
        return selected_guide(figure)
    if figure['report_id'] == 'base-directives-streams':
        from scripts.nvme_directives_figures import guide as selected_guide
        return selected_guide(figure)
    if figure['report_id'] == 'admin-io-spec-walkthrough':
        from scripts.nvme_admin_io_figures import guide as selected_guide
        selected = selected_guide(figure)
        if selected:
            return selected
    source = {'NVME-BASE-2.4':'base','NVME-NVM-CS-1.3':'nvm','NVME-PCIE-TRANSPORT-1.4':'pcie'}[figure['source_id']]
    from scripts.nvme_field_guides_context import OVERRIDES
    selected = OVERRIDES.get((figure['report_id'], source, int(figure['number'])))
    if selected:
        return selected
    return GUIDES[MEMBERS[(source, int(figure['number']))]]


def base(numbers, key, title, relation, *rows):
    guide('base', numbers, key, title, relation, list(rows))


base([1,5], 'specs', '把命令放回正確的規格層次',
 '先由主機想做的工作選擇 Admin 或 I/O 命令，再由所選命令集決定命令的細節；傳輸規格說明命令與資料如何經介面往返。這三層需配合閱讀。',
 ('Admin／I/O Command Set','Admin 管理控制器與資源；I/O 命令集定義資料操作。','Identify 查能力與格式後，Read 才使用查到的格式存取資料。'),
 ('Base／Command Set／Transport','Base 提供共同格式與行為，命令集補上操作語意，PCIe Transport 定義本篇的傳輸方式。','同樣的 DPTR 結構可以服務不同命令；buffer 內的資料意義要由命令判斷。'))
base([2,3], 'units', '從欄位的數字算回真正的資料量',
 '每次計算先寫單位，再確認欄位直接保存數量、數量減 1、指数或索引。數值相同並不表示資料量相同。',
 ('byte／word／Dword','分別為 8、16、32 bits；bit 位置與 byte 位置不可互換。','Dword index 10 對應從結構起點算起的 byte offset 40。'),
 ('kB／KiB／從 0 起算的數量','kB 是 1000 bytes，KiB 是 1024 bytes；只有定義為數量減 1 的欄位才先加 1。','NUMD=127 對應 128 Dwords，即 512 bytes；一般 index=127 只選一個項目。'))
base([6,7,73,74], 'queues', '把佇列位置與命令身分分開',
 'SQ 保存待處理命令，CQ 保存完成項目。Head 與 Tail 描述位置，CID 描述命令身分；多個 SQ 可以把完成結果送到同一 CQ，因此結果還需要 SQID。',
 ('SQ Head／SQ Tail','比較已取走與已提交的位置以辨認空、滿及可用空間；位置到達佇列末端會回繞。','深度為 8 時，index 7 的下一個位置是 0；不能用普通整數大小判斷新舊。'),
 ('CQ Head／Phase Tag／SQID＋CID','主機交回已讀取的 CQ 位置；Phase Tag 協助辨認新完成項目，SQID 與 CID 找回原要求。','兩個 SQ 可以都使用 CID=3；回覆必須同時保留 SQID 才不會配錯。'))
base([11,12,13,14,15,67,68,69,70,86,87,88,89], 'storage', '從邏輯空間連到實際容量組織',
 'Namespace 提供主機可定址的資料空間；NVM Set、Endurance Group 與 Reclaim Group 描述不同的儲存組織關係。圖上的包含關係需沿父子層次閱讀，不能由圖形大小推論容量。',
 ('TNVMCAP／UNVMCAP','分別描述 subsystem 的總容量與尚未配置容量；讀值時保留來源指定的容量單位。','先由總量扣除已配置量理解可用空間，不能把 UNVMCAP 當成某個 namespace 的剩餘 LBA。'),
 ('TEGCAP／UEGCAP／MEGCAP','描述 Endurance Group 相關容量；需要知道欄位屬於哪個 group 才能比較。','兩個 group 的未配置容量不能直接當成可任意互換的同一份空間。'),
 ('NVM Set／Reclaim Group／Namespace','NVM Set 與回收組織是不同維度；namespace 的歸屬決定要查哪組能力與容量。','沿圖找出 namespace 所屬的 Endurance Group，再解釋其配置限制。'))
base([16,17,18,19,20,21,22,23,24,25,26,27,65,66,71], 'objects', '識別物件與識別存取路徑',
 '同一個 namespace 可以經不同控制器存取。控制器識別碼、namespace 識別碼、PCIe Function 與 port 各指不同對象，應沿圖上的連接關係逐層追蹤。',
 ('NSID／Controller Identifier','NSID 選資料物件，控制器識別碼選控制器；是否可存取還要看附加關係。','A、B 都能看到 NSID=7 時，Detach A 只改變 A 的存取關係。'),
 ('I/O／Administrative Controller','控制器類型決定適用的命令與資源要求。','先辨認类型，再查命令支援表；不能假定每種控制器都提供一般資料 I/O。'),
 ('Domain／Port／PCIe Function','分別描述資源域、連接位置與 PCIe 裝置功能；多控制器不等於多份 namespace 資料。','兩個控制器共享一個 Boot Partition 時，保護狀態的影響會跨過單一控制器。'))
base([28,30,31,32,84,91,144,145,146], 'support', '支援表的列、欄與註腳必須一起讀',
 '表格先以命令、log 或 Feature 選一列，再以控制器類型或目前狀態選一欄。M／O 等標記及數字註腳說明支援要求與條件，不能將抽出的 O8、M3 當成另一個 NVMe 欄位。',
 ('命令／LID／FID 的列','三者是不同識別空間；選列前先確認目前使用哪一類操作。','Get Log Page 的 LID 與 Set Features 的 FID 即使同為 0Bh，也要查各自的表。'),
 ('控制器類型／處理狀態的欄','控制器類型決定支援要求；清除期間的狀態欄則限制當時接受的操作。','裝置平常支援某命令，並不表示 Restricted Processing 中仍允許執行。'),
 ('條件註腳','說明支援位元、所需能力或例外，需與對應儲存格合讀。','一列標示 optional 時，先查控制器宣告的能力，再決定能否使用。'))
base([33,34,36,41,42,43,44,45,46,56,57], 'initialization', '能力、主機設定與控制器狀態的往返',
 '主機先讀 CAP 選合法設定，建立 Admin 佇列，再寫 CC 啟用；控制器以 CSTS 回報結果。CAP 是可選範圍，CC 是要求值，CSTS 是實際狀態，三者不能互相代替。',
 ('CAP.MPSMIN／MPSMAX → CC.MPS','能力給可支援的記憶體 page 範圍，主機選其中一個 page 大小。','後續 ASQ、ACQ 與資料指標的對齊都要使用選定的 page 大小。'),
 ('AQA.ASQS／ACQS → ASQ.ASQB／ACQ.ACQB','AQA 設定兩個 Admin 佇列的大小；ASQ、ACQ 給它們在主機記憶體的位置。','大小編碼與基底位址分別設定，不能只配置 buffer 就認為控制器已知道位置。'),
 ('CC.EN／CSS／AMS → CSTS.RDY／CFS','主機選命令集、仲裁方式並要求啟用，控制器回報就緒或致命狀態。','CC.EN=1 是要求，仍需等待符合規則的 RDY，才能進入下一階段。'),
 ('CRMS／CRIME／CRTO；SHN／SHST','前一組連接就緒模式與逾時；後一組連接關機要求與進度。','寫入關機要求後依 SHST 確認處理，不能把要求值当作完成結果。'),
 ('CAP.BPS／DSTRD／CMBS／PMRS；NSSR／NSSD','分別用於 Boot 支援、doorbell 間距、記憶體能力與 subsystem 層級控制。','Doorbell 間距由 DSTRD 推算；不使用 doorbell 的教學步驟無須把它當成前提。'))
base([37,38], 'version', '版本的三個部分是一個識別值',
 '版本欄位由 MJR、MNR、TER 組成，分別表示主版本、次版本與修訂部分。查支援規則時應使用完整版本，不把其中一段當成十進位小數。',
 ('MJR／MNR／TER','每段是独立整數欄位；重設值表說明對應規格版本應回報的組合。','2、4、0 表示版本 2.4.0，不能把三個欄位相加來比較。'))
base([39,40], 'interrupt-mask', '設定與清除遮罩是對同一組位元操作',
 'INTMS 與 INTMC 都對應中斷遮罩，但寫入 1 的效果相反；主機寫的是要修改哪些位元，不是完整的新遮罩值。',
 ('IVMS／IVMC','INTMS 寫 1 設定遮罩，INTMC 寫 1 清除遮罩；寫 0 保留相應位元。','只想解除 vector 2 的遮罩時，向清除介面寫對應 bit，不必改掉其他 vectors。'),
 ('中斷模式','哪些遮罩機制適用需依目前使用的中斷模式判斷。','先確認 MSI／MSI-X 等模式，再解讀相關遮罩來源。'))
base([47,48,52,53,54,55,58,59,60,61,62,63,64], 'memory', '記憶體區域的位置、用途與可用狀態',
 'CMB 與 PMR 的閱讀順序是支援能力、位址與大小、允許用途、啟用、就緒。主機能映射一段位址，不代表這段位址已能承載任何種類的佇列或資料。',
 ('BIR／CBA／CMSE／CRE','BAR 選擇與基底位址決定映射位置，控制位元決定是否啟用對應功能。','先拼好高低位址並檢查對齊，再依規則啟用，最後讀回狀態。'),
 ('SZ／SZU；WDS／RDS／LISTS／CQS／SQS','大小要搭配單位；用途位元分別描述資料、指標清單與佇列可否放在此區。','支援放讀取資料不會自動表示也支援放 CQ。'),
 ('CBAI／NRDY／ERR／HSTS','狀態指出位址有效性、是否就緒及其他狀況；與控制位元不同。','EN 已設為 1 時，仍需以 NRDY 等狀態確認可用。'),
 ('EBS／SWTP 的數值與單位','彈性緩衝容量及持續寫入吞吐量各有數值和縮放單位，不能混成一個速度。','先換算 buffer bytes 與 bytes/s，再分別討論短暫突發與持續傳輸。'),
 ('PMRWBM／PMRTO／PMRTU','持久化寫入行為與就緒時間各由自己的能力欄位定義。','寫入已送到映射區域後，還要依 PMR 的可見性與持久化規則判斷完成保證。'))
base([80,81], 'arbitration', '仲裁決定下一個取用機會',
 '仲裁圖上的箭頭表示控制器選取 Submission Queue 的順序或資格，不表示每筆命令執行所需的時間，也不保證不同 queue 的完成順序。',
 ('Round Robin／Priority Class','先辨認 queue 所屬類別，再看同類 queue 如何輪流取用。','高優先級的取用機會與單筆命令花費的 media 時間是不同量。'),
 ('Arbitration Burst／權重','Burst 限制一次取用量，權重影響各類別相對機會。','權重比例不能直接當成固定的 IOPS 保證，還需考慮 queue 是否有待處理命令。'))
base([85,90,126,127], 'lifetime', '先界定事件影響的範圍，再看狀態如何保留',
 'Reset、shutdown、power cycle 與逾時偵測是不同事件。圖中的前後狀態要配合受影響的控制器或 subsystem 範圍閱讀。',
 ('Current／Saved／Default','目前生效值、保存值與預設值有不同用途；事件發生後以適用的恢復規則決定 current。','保存過某個值，仍需確認此次 reset 的範圍及功能規則，才能知道它是否成為目前值。'),
 ('KATT／偵測時間','Keep Alive 的計時與檢查時點共同決定何時察覺逾時。','在兩次檢查之間錯過一次更新，實際偵測時間可能超過單一 KATT。'))
base([92,93,94], 'sqe', '同一筆命令的身分、對象與資料方向',
 'CDW0 先選操作與資料指標格式；NSID 選操作對象；DPTR／MPTR 再指向資料。命令專屬 Dwords 的含義由 OPC 與命令集決定。',
 ('OPC／FUSE／CID','OPC 選操作，FUSE 說明融合操作角色，CID 讓完成項目找回原命令。','相同的 CDW10 數值放在 Read 與 Set Features 中，可能完全不是同一種意思。'),
 ('PSDT → DPTR／MPTR','PSDT 決定指標依 PRP 或 SGL 等格式解讀；指標內的數值不可在未選格式時直接當成長度。','主機先選指標格式，再按該格式準備 buffer 描述，最後由命令語意判斷資料方向。'),
 ('NSID／CDW2–CDW15','NSID 與命令專屬欄位共同決定對象、範圍及選項。','Create 的 DPTR 指向建立參數；它不是新 namespace 的實體儲存位址。'),
 ('NDT／NDM／MDPTR','廠商命令使用共同格式時，資料與 metadata 長度各有自己的欄位及指標。','先看廠商命令格式支援宣告，再依長度定義換算，不能把欄位上限直接加 1 後存回同寬整數。'))
base([97,98,99,101,102,103,104,105,107,108,109], 'cqe', '把完成結果對回命令，再解釋狀態',
 '先以 Phase Tag 辨認新完成項目，再用 SQID 與 CID 對回要求。SCT 決定 SC 所屬表格，DNR 與 CRD 補充重試資訊；SQHD 表示提交佇列進度，不能當成這筆命令的資料長度。',
 ('SQID／CID／SQHD','前兩者辨認命令，SQHD 告知控制器的 SQ Head。','一個 CQ 收到多個 SQ 的完成項目時，即使 CID 相同也可由 SQID 區分。'),
 ('SCT → SC','先選 Generic、Command Specific、Media 或 Path 等類別，再查具體碼值。','SC=某個值不能單獨命名錯誤；必須保留它搭配的 SCT。'),
 ('DNR／CRD／CRDT','DNR 與重試延遲資訊影響如何理解重新提交；不能把它們當成原命令已成功。','重試前仍要確認原操作的狀態與副作用，不能只看延遲已經過。'),
 ('DW0／DW1／Phase Tag','前兩個 Dwords 的內容依命令解釋；Phase Tag 隨 CQ 回繞而變化。','Create 成功時 DW0 可回 NSID；同一位置在另一種命令不一定有這種意義。'))
base([110,111,112,113], 'prp', '從第一個 page 的剩餘空間開始計算',
 'PRP1 的 page offset 決定第一頁還能容納多少資料，總長度再決定 PRP2 是下一頁位址還是 PRP List 位址。指標串接與資料是否實體連續是兩個問題。',
 ('Page Base Address／Offset','將位址拆為 page 基底與頁內位移；page 大小以主機所選記憶體 page 設定解讀。','page 為 4096 bytes、offset=3072，第一頁只剩 1024 bytes 可放資料。'),
 ('PRP2／PRP List entries','先扣掉第一頁已涵蓋的長度，再依剩餘量判斷直接指下一頁或使用清單。','傳輸 8192 bytes 且第一頁只剩 1024 bytes 時，還需涵蓋後續 7168 bytes，不能只給一個下一頁。'),
 ('清單串接與對齊','清單中的頁位址及下一段清單各有對齊與最後項目的使用規則。','不能把作為下一張清單指標的位置，又當成一頁實際資料。'))
base([114,115,116,117,118,119,120,121,122,125], 'sgl', '描述子先選類型，再解釋位址與長度',
 'SGL 的型別與子型別決定描述子是在描述資料、下一段描述子，或其他受支援行為。LEN 的單位雖然是長度，所指的內容仍由型別決定。',
 ('SGLID／SGLDT／SGLDST','型別與子型別決定此描述子的結構及合法組合。','Data Block 的 ADDR 指向資料；Segment 的 ADDR 指向更多描述子，兩者不能當成相同 buffer。'),
 ('ADDR／LEN','一起描述一段範圍；主機還需檢查總涵蓋長度與命令要求相符。','前段 1024 bytes、後段 3072 bytes 可涵蓋 4096 bytes，但每個描述子仍需符合自身規則。'),
 ('Segment／Last Segment／Bit Bucket','Segment 與 Last Segment 表達清單串接，Bit Bucket 表達特定資料處理方式。','遇到 Last Segment 就按最後一段的規則處理，不再假定有下一段指標。'))
base([128,129,130,131,132,133,134,135,136,137,138,139,140,142,337,347,348], 'identifiers', '辨認識別碼的格式、有效範圍與用途',
 '識別碼、文字欄位與清單索引需要不同解讀方式。先讀來源定義的長度與編碼，再決定要比較整個值、拆出廠商部分，或沿清單尋找指定物件。',
 ('VID／SSVID／SN／MN','前兩者識別廠商與子系統廠商，後兩者是序號與型號文字；不能套用相同的數值或字串規則。','文字欄位的 padding 與編碼要按定義處理，不將固定長度緩衝區一概當成以零結尾的字串。'),
 ('OUI／EUI64／NGUID／UUID','有各自的長度與組成規則；識別物件時保留完整值。','僅有相同 OUI 只能說明共同的組成部分，不代表兩個 namespace 相同。'),
 ('NUMCIDS／Controller List／Namespace List','數量欄位或清單終止規則決定有效項目；識別碼的合法性另行判斷。','NUMCIDS=2 表示讀取兩個有效控制器項目，並非最高控制器識別碼是 2。'),
 ('UIDX／UUID List Entry／IDASSOC','UIDX 選清單項目，項目的識別關聯再決定 UUID 如何使用。','UIDX=2 是選位置，不是把值 2 當成 128-bit UUID。'))

base([151,152,155,156,474], 'events', '事件通知指出要重新讀哪份狀態',
 '先依功能設定允許的事件通知，再由 AER 完成項目辨認事件類型、資訊與相應 log。通知、log 內容及事件確認是流程中的不同步驟。',
 ('AET → AEI → LID','AET 選事件類別，AEI 指出該類別的事件，LID 指引相關紀錄。','收到 Telemetry Log Changed 時，先辨認類別與 log，再讀取紀錄；通知本身不是 payload。'),
 ('EVNTSP','提供事件專屬的補充資訊，依該事件定義解讀。','同一個 DW1 位置在不同事件下，不保證代表相同對象。'),
 ('Notice enable／RAE','前者控制相應通知，RAE 影響讀 log 時是否保留相關事件；兩者目的不同。','計畫分段取回同一份紀錄時，將確認事件的時機放在完整流程中決定。'))
base([176,177,178,179,180,700,701], 'selftest-command', '測試種類、範圍與目前作業共同決定處理方式',
 'STC 選測試或控制動作，NSID 選對象，DSTP 是適用測試的參數。控制器還要結合是否已有作業及其他命令的影響，決定接受、拒絕或中止。',
 ('STC／DSTP','先解讀 STC，再查 DSTP 在該作業下是否有定義；保留編碼不得自行賦予測試種類。','要求 short test 與要求 abort 是不同動作；不能把 STC 數字當成測試次數。'),
 ('NSID=0h／單一 NSID／FFFFFFFFh','分別依命令規則選控制器、單一 namespace 或開始時可存取的 namespaces；Host-Initiated Refresh 忽略 NSID。','NSID=7 未附加到本控制器時，不能因另一個控制器可存取它就認為本要求有效。'),
 ('目前作業／新 STC／結果建立','互動表的起點與輸入共同決定是否留下原作業結果及新要求的狀態。','看到 Device Self-test in Progress，先對照新要求與目前作業，不能當成測試發現媒體錯誤。'),
 ('Format NSID／SES／FNS／SENS','Format 的範圍與動作會影響正在測試的對象；須比較兩者範圍。','Format 的對象與 self-test 對象不相交，和兩者相交時，不應直接套用同一個中止結論。'),
 ('segment／test performed／failure criteria','示例列出一種測試切分方式；informative 範例不要求每個裝置都實作相同 segment。','SEGN 可用於理解哪段失敗，但不能單憑範例推論廠商內部每個測試步驟。'))
base([218,219], 'selftest-result', '目前進度與歷史結果使用不同欄位',
 '先由 log header 讀目前作業，再選一筆結果紀錄。紀錄內先看測試種類與結果，再按有效性旗標讀失敗欄位。',
 ('DSTOS／DSTCS；RDS1–RDS20','前者是目前作業與進度，後者是結果紀錄序列。','目前進度 50% 與最前面的歷史成功結果可以同時存在，兩者未必屬於同一作業。'),
 ('DSTC／DSTR／SEGN／POH','分別描述測試種類、結果、適用的失敗區段與作業時間背景。','先確認作業如何結束，再決定 SEGN 能否用於解釋失敗位置。'),
 ('VDINFO → NSID／FLBA／STCT／STC','有效性旗標決定哪些資訊可信；STCT 與狀態碼需成對解讀。','FLBA Valid=0 時，FLBA 的非零內容不能用來指出故障 LBA。'),
 ('VS','廠商專屬結果需依廠商格式解讀，不沿用其他裝置的定義。','未知 VS bytes 保留原值及來源，不能任意翻成錯誤類別。'))
base([187,188,189,190,191,192,193,215], 'firmware', '位移、傳輸長度、儲存位置與啟用時機',
 'Download 把映像分段交給控制器；Commit 再決定保存或啟用。OFST 是映像中的位置，DPTR 是主機資料的位置，FS／BPID 是目標選擇，四者不可互換。',
 ('DPTR／NUMD／OFST／FWUG','DPTR 指資料，NUMD 是 Dword 數量減 1，OFST 是 Dword 位移，FWUG 描述更新粒度。','4096 bytes 的一段使用 NUMD=1023；接續下一段的 OFST=1024，再檢查粒度及完整範圍。'),
 ('CA／FS／BPID','CA 選動作；一般韌體 slot 與 Boot Partition 有不同目標選擇。','保存映像成功不代表已切換執行版本；Boot 的寫入與選擇 active partition 也分開。'),
 ('MUD／MEFWO／ASQFWO；完成狀態','結果依支援能力及本次更新操作解讀，reset-required 狀態還指出啟用所需事件。','收到要求 reset 的結果後，先辨認所需 reset 類型，再追蹤真正啟用。'),
 ('AFI.CAFS／NAFS → FRS1–FRS7','先找目前 active slot 與下次 active slot，再讀相應版本字串。','FRS2 有新版本而 CAFS 仍是 1，表示新映像可能已存在，但尚不能說它正在執行。'))
base([197,198,199,200,201,202,463,464,465,466], 'features', '查能力、讀取值與寫入值的區別',
 'FID 指功能，Get 的 SEL 指要查哪一種資訊，Set 的 SV 指是否要求保存。支援能力回覆的 bits 與功能值是不同結構。',
 ('FID／UIDX／DPTR','FID 選功能，必要時 UIDX 協助選 UUID，DPTR 傳輸該功能所需的資料結構。','不是每個 Feature 都只靠 CQE DW0 回覆；有 buffer 的功能還需讀其資料格式。'),
 ('SEL=000b／001b／010b／011b','分別要求目前值、預設值、保存值、支援能力。','要確認裝置現在採用什麼值，應讀目前值；保存值不等於正在使用的值。'),
 ('CHANG／NSSPEC／SVBL → SV','能力分別指出可變更、是否與 namespace 有關、可否保存；SV 是主機的保存要求。','SVBL=0 時提出保存要求可能被拒絕；Set 成功也不能一律推論跨 power cycle 保留。'))
base([203,204,205,206,207,208,209,210,211], 'get-log', '同一筆 Get Log Page 的目標、範圍與資料位置',
 '讀 log 先選 LID 與命令集，再解讀該 log 的 LSP／LSI；NUMD 決定本次量，LPO 決定本次起點，DPTR 決定主機接收位置。',
 ('LID／CSI／LSP／LSI','LID 與 CSI 選紀錄種類，LSP、LSI 的含義由所選 log 定義。','LSP 在 Boot 中可含 BPID，在 Telemetry 中有建立 capture 的控制位元，不能跨 log 照搬。'),
 ('NUMDU／NUMDL','先合成 NUMD=(NUMDU<<16)|NUMDL，再計算 (NUMD+1)×4 bytes。','512 bytes 對應 NUMD=127；高低部分不能各自加 1。'),
 ('LPOU／LPOL／OT','高低欄位組成 64-bit offset；OT 決定按 byte 位移或項目索引解讀。','byte-offset 模式下，從 512-byte 表頭後開始讀資料要保留起點差異；index 模式不能直接使用同一個 byte 數。'),
 ('DPTR／RAE','DPTR 給接收記憶體，RAE 控制相關事件的保留行為。','分段讀取先準備每段 buffer，再在恰當時機確認事件，避免中途改變可取得的紀錄。'),
 ('LSUPP／LID Specific Parameter','Supported Log Pages 回報實際支援及 log 專屬能力。','規格列有某個 LID，不代表此裝置一定實作；先查支援再使用進階選項。'))
base([338], 'identify-controller', '能力欄位是後續操作的前提',
 'Identify Controller 的同一張結構表包含多種功能。每篇只使用與該篇操作直接相關的欄位，沿「能力→命令選擇→結果」連接，不把整張表當成一次必須背完的清單。',
 ('支援位元與功能屬性','支援位元先決定能否使用；功能屬性再限定操作範圍、數量或特殊行為。','Self-test 先看 OACS.DSTS，再看 DSTO 與 EDSTT；Namespace Management 則看 OACS.NMS 等欄位。'),
 ('數量上限與時間資訊','先確認數量是否直接計數或從 0 起算，以及時間的單位。','EDSTT 是延伸測試時間資訊，不能當成成功判斷；MAXCNA 則限制控制器可附加的數量。'),
 ('本篇使用的能力分支','Boot 查 BPCAP 及相關配置，Telemetry 查 LPA，Sanitize 查 SANICAP；欄位位置相近不代表功能互相依賴。','讀到 SANICAP 的支援值後，才選對應的清除方法；不以 Boot 支援推論清除能力。'))
base([340,468,738,739,740], 'power-state', '先確認狀態用途，再比較功率與延遲',
 'NPSS 指出最高支援的狀態編號；PSD 描述每個狀態的性質；Power Management 命令選狀態與 workload hint。狀態編號不是功率單位。',
 ('PS／NOPS／WH','PS 選狀態，NOPS 指出是否 non-operational，WH 給工作負載提示。','WH 不直接指定 IOPS；選 non-operational 狀態後，恢復服務需依狀態轉換規則。'),
 ('MP／MPS；IDLP／IPS；ACTP／APS／APW','功率數值需搭配比例及測量條件；最大功率、典型閒置功率與平均活動功率不可混比。','原始值相同但比例不同時，實際功率不同；先換成相同單位再比較。'),
 ('ENLAT／EXLAT','以微秒描述進入與離開該狀態的延遲界限。','由 A 直接到 B 時，先考慮 A 的 EXLAT 與 B 的 ENLAT，而不是把 B 的兩個數字相加。'),
 ('RRT／RRL／RWT／RWL','各自提供相對讀寫吞吐與延遲指標；同類數值之間才有可比性。','不能把相對效能值 3 解釋成 3 微秒或 3 倍 IOPS。'))
base([475,476,477,478,483], 'apst', '一個 APST entry 對應目前狀態的閒置規則',
 '先確認 APST 支援與 APSTE，再以目前 power state 的編號找到該 entry；ITPT 給等待條件，ITPS 給目標 non-operational state。I/O 到達與背景工作另依規則處理。',
 ('APSTE／32 entries／256 bytes','APSTE 控制自動轉換是否啟用；每筆 entry 8 bytes，由 power-state index 選取。','PS0 的 entry 存在，不代表控制器只會使用第一筆；目前狀態決定適用項目。'),
 ('ITPT bits 31:8／ITPS bits 7:3','ITPT 以 ms 表示閒置時間；ITPS 是狀態編號。ITPT=0 停用該 entry。','2000 ms、目標 PS3 的低 Dword=(2000<<8)|(3<<3)=0007D018h。'),
 ('NOPPME／APSTE','NOPPME 影響 non-operational 狀態內的背景工作功率行為，APSTE 影響自動進入狀態。','允許背景工作並不等於把 APST 關閉；要分別判斷進入條件和進入後行為。'),
 ('進出延遲與目前 I/O','恢復處理需要走回適用 operational state，並計入轉換延遲。','閒置時省下的功率，要與下一次 I/O 的等待成本一起評估。'))
base([213,470,482,741], 'thermal', '溫度觀察、事件門檻與熱管理控制',
 'SMART 提供觀察值與累計資訊，Temperature Threshold 決定事件判斷，HCTM 決定主機設定的熱管理門檻。溫度相同，不表示這三種資料都代表相同狀態。',
 ('TMPSEL／THSEL／TMPTH／TMPTHH','先選感測來源及超過或低於門檻的類型，再解讀門檻值及 hysteresis 值。','比較前統一溫度單位，不能把 Celsius 直接填入要求 Kelvin 的欄位。'),
 ('TMT1／TMT2／hysteresis','兩個熱管理門檻須符合支援範圍與順序；回復行為還需配合控制器定義。','溫度下降後的恢復點不一定等於升溫時開始限制的那個點。'),
 ('Composite Temperature／Sensors／累計時間與次數','即時溫度、各感測器讀值與過去累計統計回答不同問題。','目前溫度已下降，歷史 throttling 累計時間仍可保留；這不是欄位互相矛盾。'))
base([545,546,547,548,549,550,551,552,553], 'hmb', '描述記憶體清單與交接使用權',
 '主機配置記憶體、建立描述子，再以 HMB Feature 提供清單。總容量、描述子數量、每段位址與每段大小都要互相一致。',
 ('EHM／MR／CTZ／HMNARE','啟用、記憶體返回及相關可選行為需依各 bit 的條件配合使用。','重新提供原記憶體與提供新記憶體是不同情境，不能一概保留原內容假設。'),
 ('HSIZE／HMDLEC','總容量依 CC.MPS 的 page 單位解讀；HMDLEC 是清單中的描述子數。','總容量為 16 pages，不代表必須有 16 個描述子；一個描述子可以描述多個 pages。'),
 ('HMDLUA／HMDLLA；BADD／BSIZE','高低欄位組成清單位址；每個描述子的 BADD 與 BSIZE 再給出實際記憶體段。','清單位址要求與資料區域 page 對齊分別檢查，不能用其中一個通過替代另一個。'),
 ('HMNAR 與主機回收','完成回覆的相關狀態與使用權交接連在一起。','控制器仍可使用記憶體時，主機不能提前把相同範圍拿去保存其他資料。'))
base([304,346,442,443,444,445,446,447,448,449,450], 'namespace', '建立資料物件與建立存取關係',
 'Namespace Management 管理物件是否存在，Namespace Attachment 管理控制器能否存取。兩種命令各有 SEL，其編碼必須放在各自命令內解讀。',
 ('Management SEL／CSI／DPTR','SEL 選 Create、Delete 或 Restore；Create 的 CSI 決定建立資料格式，DPTR 給資料位置。','Management SEL=0h 是 Create，Attachment SEL=0h 是 Attach；數值相同但動作不同。'),
 ('Create payload → NSZE／NCAP／FLBAS 等欄位','Base 定義共同傳輸結構，所選命令集補上主機設定；命令集延伸部分須以更具體的定義解讀。','使用 NVM Command Set 時，需把 Base Figure 448 與 NVM Figure 134 合讀，包含 Placement Handle List。'),
 ('CQE DW0／NSID','Create 成功回傳已建立 namespace 的識別碼，後續管理與 I/O 以它選物件。','回傳 NSID=7 不能單獨證明任何控制器已附加到它。'),
 ('Attachment DPTR／Controller List／NUMCIDS','清單選控制器，NSID 選 namespace；SEL 決定附加或分離。','NUMCIDS=2、列 A 與 B，表示對兩個控制器建立或移除關係。'),
 ('DNCS／ANAGRPID／NVMSETID／ENDGID','DNCS 回報預設配置狀態；另外三者說明 namespace 的資源歸屬。','Restore Default 後仍需重新 Identify 實際配置，不能只拿 DNCS=1 推論 namespace 的容量。'),
 ('命令專屬錯誤','格式、容量、識別碼及附加限制是不同檢查條件。','Insufficient Capacity 與 NSID Unavailable 分別指出空間與識別碼資源問題，不應合併成同一種失敗。'))
base([49,50,51,279,280,679], 'boot-read', '同時標出映像座標與主機記憶體座標',
 'Properties 路徑與 LID 15h 路徑都讀 Boot Partition，但要求與完成證據不同；兩條路徑的位移起點也應分別標示。',
 ('ABPID／BPSZ／BRS','分別給 active partition、以 128 KiB 為單位的分割區大小及 Properties 讀取狀態；ABPID 不等於本次目標 BPID。','目前 active 是 BP0 時，主機仍可能指定讀取 BP1。'),
 ('BPID／BPROF／BPRSZ','BPID 選目標分割區；BPROF 與 BPRSZ 分別以 4 KiB 為單位指定起點與讀取量。','先用起點加長度檢查未超出 BPSZ，再提供主機接收位置。'),
 ('BMBBA','指向接收開機資料的主機記憶體；與 HMB Feature 借給控制器的記憶體用途不同。','圖上標為 Host Memory Buffer 的接收區，不代表必須先啟用 Host Memory Buffer Feature。'),
 ('LID 15h 的 BPID／BPINFO／BPD','log 先有表頭，再有 Boot Partition Data；Get Log Page 的 offset 從 log 起點計算。','讀映像 offset 0 的資料時，需考慮它在 log 內位於表頭之後，不能直接把兩種 offset 畫在同一起點。'))
base([542,680,681,682,683,684,756,757,758,760,761,762,765,766], 'boot-protect', '把保護機制、分割區狀態與操作結果分開',
 '先判斷目前由 Set Features 或 RPMB 控制，再選 BP0 或 BP1。讀值、要求變更、重設後保留與驗證操作分別有自己的規則。',
 ('BP0WPS bits 2:0／BP1WPS bits 5:3','兩個 3-bit 欄位獨立描述分割區狀態。','只要求解鎖 BP1 並保留 BP0，CDW11=(001b<<3)|000b=08h。'),
 ('000b／001b／010b／011b／100b','依序為 Set 不改變、解鎖、鎖定、鎖到 power cycle，以及 Get 回報 RPMB 控制；不是所有編碼都能同時用於 Set 與 Get。','Get 不回 000b；Set 指定 100b 會是 Invalid Field in Command。'),
 ('Controller Level Reset／power cycle','Set Features 的解鎖可跨 controller reset；power cycle 會回 locked。RPMB 啟用後，兩種事件都會使已解鎖分割區重新鎖定。','要恢復寫入，先看是哪個機制控制，再採用對應的解鎖操作。'),
 ('Write Locked Until Power Cycle／CTRATT.MDS／共享關係','目前狀態與裝置配置一起限制是否可變更；multi-domain 且跨控制器共享的分割區禁止使用此狀態。','A、B 共享 BP0，將 BP0 設 011b 的要求會回 Feature Not Changeable；不能以只重設 A 來解除。'),
 ('RPMB Enable／各分割區 Write Protection bits','啟用機制與分割區鎖定是不同層次；啟用後不能停用機制，但可依驗證流程變更各分割區保護狀態。','FID 85h 回 100b 表示應改走 RPMB 控制，不表示所有分割區永遠不可解鎖。'),
 ('Request/Response／Result／Counter／Nonce／MAC','訊息類型選操作，Result 回報結果，Counter 與 Nonce 配合驗證避免把舊回覆當成新操作結果。','Configuration Write 後依流程取回結果；Configuration Read 要核對驗證資訊，不能只看到有資料就認定操作成功。'))
base([220,221,222,223,780,781], 'telemetry', '建立要求、紀錄身分與累積資料區',
 '先選 Host-Initiated 或 Controller-Initiated log，再由 header 規劃範圍並保留紀錄識別。資料區終點、資料是否可用及版本資訊共同決定能否組成完整 capture。',
 ('CTHID／MCDA／MCDAS','CTHID 要求建立，MCDAS 回報是否支援建立範圍選擇，MCDA 選想建立到哪個 Area。','分段讀既有紀錄時不反覆設 CTHID=1；MCDA 的使用還需符合支援條件。'),
 ('THDA1LB–THDA4LB／TCDA1LB–TCDA4LB','各 Area 的含終點 block 編號；每個 Area 都從 block 1 開始。','終點 65 表示資料量 65×512 bytes；加上 header 才是 66×512 bytes。'),
 ('THDGN／TCDGN／TCDA','generation number 辨認版本；TCDA 指控制器發起資料是否可用。','兩次讀 header 的 generation 不同時，不能直接把中間取得的各段視為同一份紀錄。'),
 ('THS／TCS／RID','scope 與 Reason Identifier 補充紀錄範圍及建立原因；廠商定義部分仍需相應格式。','知道資料區大小不會自動知道 payload 每個 byte 的用途；RID 也不能被當成一般 NVMe status code。'),
 ('Last Block=0／相同終點','要結合各 Area 的可用規則解釋沒有新增範圍的情形。','Area 1=0、Area 2=1000 時，不可把 Area 2 的 1000 又加到 Area 1 後方。'))
base([311,312,451,452,453,454,492,770,771,772,773,774,775,776,777,778,779], 'sanitize', '目標、方法、狀態與後續讀取的關係',
 '先決定作用範圍，再選 SANACT 及適用參數；成功 CQE 之後，仍要沿 LID 81h 與狀態圖確認作業及後續處理。',
 ('SANACT／NSID／作用範圍表','整個 subsystem 與指定 namespace 的命令有不同目標；不同資料類別也需依範圍表判斷。','不能把 Sanitize Namespace 的完成結果直接當成所有 Boot、CMB、PMR 資料均已清除的證明。'),
 ('OVRPAT／OWPASS／OIPBP','在 Overwrite 方法下配合決定樣式、pass 數及 pass 間反相；OWPASS=0 有特別定義。','先列出每個 pass 的樣式，再解釋資料與 PI 的處理，不用泛用的數量加 1 規則。'),
 ('AUSE／PREQ／NDAS／NODRM／EMVS','分別影響失敗後限制、相關要求、解除配置及進入驗證等行為；需依動作與支援條件讀。','EMVS 是要求後續驗證的選項，不是目前已在驗證的狀態旗標。'),
 ('SSTAT／SPROG／SCDW10／估計時間','先查結果狀態，再使用適用的進度及時間欄位；SCDW10 協助對回操作設定。','進度值不能脫離狀態使用；命令被接受與清除已完成要分別確認。'),
 ('SSI／MNSOIP／STNSID','SSI 補充狀態；MNSOIP 是允許同時執行的作業數上限；STNSID 確認查詢目標。','MNSOIP=4 不表示目前有 4 個作業；STNSID=0 表示查詢 subsystem。'),
 ('A1–I2／MVCNCLD／FAILS','狀態表用箭頭代號連回起點、事件、條件及終點；驗證後是否解除配置也有條件。','沿 Media Verification 離開時，先確認觸發事件及 MVCNCLD，再決定下一站，而非只看箭頭方向。'),
 ('Reservation Notification／Log Page Count／Notification Type','必要引用用來解釋相關操作造成的 reservation 變動通知；其 log 與 Sanitize Status 不同。','應由通知類型判斷要更新的存取狀態，不把通知計數當成清除完成百分比。'))
base([491], 'host-behavior', '控制器支援與主機能理解的格式需要配合',
 'Host Behavior Support 是主機對可處理行為或格式的宣告。控制器本身支援某功能，不足以推論主機已能解釋該功能的進階資料結構。',
 ('LBAFEE／ETDAS／CDF2E／CDF3E','分別連到延伸 LBA 格式、Telemetry Area 4 及 Copy 描述子格式；每篇只使用所需分支。','使用需要延伸格式的 namespace 建立設定前，先確認主機相應宣告已成立。'))
base([561,562,563], 'track', '把追蹤管理動作連到結果佇列',
 'Track Send 的管理操作選擇、操作專屬參數與目標資料佇列共同決定追蹤如何啟動或停止。',
 ('MO／MOS／LACT','先由 MO 選管理操作，再解讀 MOS 及其中的啟停選擇。','要求開始記錄與要求停止記錄是兩個事件，不能用同一個 LACT 值解釋。'),
 ('CDQID','選已建立的控制器資料佇列；追蹤結果會依該佇列格式回報。','Track Send 的成功 CQE 與資料佇列中後續產生的紀錄分別觀察。'))
base([712], 'streams', '串流提示的寫入大小與群組大小',
 'Streams 參數提供主機安排寫入的提示，需與 namespace 格式及串流的識別使用方式一起讀。',
 ('SWS／SGS','分別描述串流寫入大小與群組大小，按來源規定單位換算。','先把提示換成 logical blocks 或 bytes，再比較一批實際寫入的範圍，不能把兩個數字當成串流數量。'))

from scripts.nvme_field_guides_nvm import install as install_nvm
from scripts.nvme_field_guides_pcie import install as install_pcie
install_nvm(guide)
install_pcie(guide)
