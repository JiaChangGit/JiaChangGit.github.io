"""Only the required branch of a large referenced structure is taught here."""
OVERRIDES = {}


def context(reports, source, numbers, key, title, relation, *rows):
    for report in reports:
        value = dict(id=source+'-'+key, title=title, relation=relation, rows=list(rows))
        for number in numbers:
            OVERRIDES[(report, source, number)] = value


context(['base-device-self-test'], 'base', [176,177,178,179,180], 'selftest-request', '依目前作業與新要求，逐步判斷接受或中止',
        '先用 DSTO.SDSO 決定「已有測試」是看收到命令的控制器，還是看整個 subsystem，再以 STC 選互動表的一列。NSID 與 DSTP 則分別決定對象及適用參數。',
        ('STC bits 3:0／DSTP','STC=1h、2h、3h 分別是 short、extended、Host-Initiated Refresh；Eh 是廠商測試；Fh 是中止。DSTP 只有 Eh 使用廠商定義，其餘為保留。','要求 short test 時，不能在 DSTP 填一個自訂「測試次數」；此處並沒有這個標準用途。'),
        ('已有作業 + STC=1h／2h／3h','新命令以 Device Self-test in Progress 結束，不會因新命令而排入下一個標準測試。','Extended 正在執行，再送 short：第二筆要求被拒絕，不能把它的 status 當成第一筆測試已發現故障。'),
        ('已有作業 + STC=Fh','依序中止作業、建立最新結果紀錄、更新目前狀態，再成功完成中止命令。','中止命令成功後，應到歷史結果找被中止作業的紀錄，不能把成功 CQE 解釋成測試通過。'),
        ('沒有作業 + STC=1h／2h／3h 或 Fh','啟動要求先驗證參數並建立目前作業；Fh 則成功完成而不修改 log。Eh 的處理由廠商定義。','沒有測試時送 Abort，不會憑空新增一筆測試失敗紀錄。'),
        ('NSID=0h／單一 NSID／FFFFFFFFh','0h 只含控制器，單一值選指定 namespace，FFFFFFFFh 選作業開始時經該控制器可存取的所有已附加 namespaces。Refresh 忽略 NSID。','識別碼 invalid 回 Invalid Namespace or Format；inactive 回 Invalid Field in Command。兩者要按 Base 的有效性及附加關係區分。'))
context(['base-device-self-test'], 'base', [700,701], 'selftest-interactions', '測試區段與 Format 影響範圍如何一起判斷',
        'Figure 700 是測試切分的說明性範例；Figure 701 則是 Format 對測試的中止條件表。前者不要求所有廠商使用相同區段，後者要依 SES 選擇 FNS 或 SENS 分支。',
        ('segment／test performed／failure criteria／SEGN','區段、測試內容與失敗判準描述一次內部檢查；結果紀錄的 SEGN 在有效時指向失敗區段。','SEGN=2 不足以直接推論某顆 NAND die 壞掉，仍需廠商對區段的定義。'),
        ('SES=000b → FNS；SES=001b／010b → SENS','沒有 secure erase 時看 FNS，有 secure erase 時看 SENS；相應位元為 1 時，表中要求中止，不再以兩筆 NSID 的相同與否作限制。','不要同時把 FNS 與 SENS 都當成必要條件，應先由 SES 選對那一欄。'),
        ('單一 Format NSID／單一測試 NSID','相應範圍位元為 0 時，兩個 NSID 相同才落入表中的必須中止條件。','Format NSID=7、測試 NSID=7，與 Format NSID=8、測試 NSID=7 的判斷不同。'),
        ('FFFFFFFFh／Optional','Format 全部 namespace 時中止；單一 Format 對上涵蓋所有 namespace 的測試時，表中部分列是 Optional。','Optional 表示允許中止但不要求中止，不能改寫成一定中止或一定繼續。'))


context(['base-device-self-test'], 'base', [338], 'selftest-capability', '從支援能力決定測試計畫',
        '這份 Identify Controller 結構很長，本篇需要的是測試支援、同時執行限制與延伸測試時間；其他功能欄位不參與這次判讀。',
        ('OACS.DSTS','Device Self-test 支援位元決定能否使用命令。','DSTS=0 時，不能因 LID 06h 有固定編號就假定能啟動測試。'),
        ('DSTO.SDSO','指出 subsystem 的單一 Device Self-test 作業限制。','兩個控制器都支援命令，不等於可各自同時啟動一個作業；仍需確認共享的作業限制。'),
        ('EDSTT','延伸測試完成時間以分鐘表示，供安排測試使用。','EDSTT=10 表示時間資訊是 10 分鐘；它不是目前完成百分比，也不能當作第 10 分鐘必定通過的保證。'))
context(['base-device-self-test'], 'nvm', [111], 'selftest-flba', '把失敗位置連回有效旗標與 namespace 格式',
        'NVM Figure 111 補上 Base 結果紀錄中 FLBA 的命令集語意。它不另外建立一份測試結果，必須回到同一筆 Base Figure 219 紀錄內判讀。',
        ('VDINFO 的 FLBA Valid → FLBA bytes 23:16','有效旗標成立時，FLBA 才表示造成失敗的一個 logical block。','FLBA=123、有效旗標=0：不能採用 123。有效旗標=1：才可將它作為其中一個失敗位置。'),
        ('NSID／LBA format／FLBA','NSID 確定儲存對象，格式決定該 LBA 代表多少資料；多個失敗區塊可能只回報其中之一。','每個 block 4096 bytes 時，LBA 123 的資料起點是 503808 bytes。這是 logical address 的換算，不是 NAND 實體頁地址。'))
context(['base-namespace-management'], 'base', [36], 'command-set-selection', '確認目前啟用的命令集組合',
        'CAP.CSS 回報控制器支援的命令集選擇方式，CC.CSS 是初始化時的選擇；Namespace Create 的 CSI 則指定這個新 namespace 的命令集。',
        ('CAP.CSS／CC.CSS／Create CSI','先確認控制器支援與目前選擇，再決定建立資料如何解讀。','Create 的 CSI=00h 指 NVM Command Set；不能把 CSI 的 00h 當成 CC.CSS 的通用寫值。'))
context(['base-namespace-management'], 'base', [139], 'controller-list', '清單選控制器，NSID 選儲存物件',
        'Namespace Attachment 的資料指標連到 Controller List。清單中的識別碼與命令 NSID 各選一種對象，不能互換。',
        ('NUMCIDS／Controller Identifier entries','NUMCIDS 是有效控制器項目數；每個 entry 保存一個 Controller Identifier。','NSID=7、NUMCIDS=2、清單為 3 和 5：對 namespace 7 改變它與控制器 3、5 的關係。'),
        ('4096-byte 結構／DPTR／page boundary','傳輸緩衝區要符合 Attachment 對單頁資料的要求；不能只配置有效識別碼佔用的幾個 bytes 就忽略外框。','主機先準備完整清單及其對齊，再把 DPTR 指向它，而不是把第一個控制器編號填進 DPTR。'))
context(['base-namespace-management'], 'base', [338], 'namespace-capability', '建立與還原前要先查的能力',
        '這裡從 Identify Controller 取出 namespace 管理、預設配置還原及配置上限所需欄位。它們限制不同資源，不能拿一個數值代替全部能力檢查。',
        ('OACS.NMS／RDNCS','前者回報 Namespace Management／Attachment 支援，後者回報還原預設 namespace 配置的能力。','能 Create 不代表任何控制器都能 Restore；還原前要另外確認 RDNCS。'),
        ('MAXDNA／MAXCNA','MAXDNA 限制 domain 內合計的 namespace 附加數；MAXCNA 限制單一 I/O controller 的附加數。兩個非零上限分別檢查。','容量仍有剩餘但已達可附加數量上限時，不能只用剩餘 bytes 推論 Attach 會成功。'))
context(['base-namespace-management'], 'base', [155,474], 'namespace-notices', '先啟用通知，再刷新正確的清單',
        '通知指出哪一類資訊可能已改變；它不取代 Identify。Base Figure 474 選通知類別，Figure 155 說明事件所代表的變動。',
        ('NAN bit 8／Attached Namespace Attribute Changed','啟用目前控制器的已附加 namespace 屬性變動通知。','收到事件後，依變動查 active namespace 清單或相關屬性；不能直接由事件數量推算新 NSID。'),
        ('ANSAN bit 19／Allocated Namespace Attribute Changed','啟用已配置 namespace 屬性變動通知，關心的是配置集合。','Create 與 Attach 改變不同集合：CNS 10h 查 allocated，CNS 02h 查 active，查錯清單可能漏掉剛建立但尚未附加的物件。'))
context(['base-boot-partitions'], 'base', [36,338], 'boot-capability', '有 Boot 讀取能力，不等於所有保護機制都支援',
        'CAP.BPS 決定 Boot Partitions 能力；LPA 與 BPCAP 再分別補充 log 讀取及保護方式。multi-domain 是共享配置的判斷條件，不是一種保護狀態。',
        ('CAP.BPS／LPA 的 Boot Partition Log Page Support','先確認 Boot 功能，再確認是否能透過 LID 15h 取得內容。','CAP.BPS=1 不能單獨代替 LPA 的 log 支援檢查。'),
        ('BPCAP','回報 Set Features 與 RPMB Boot 保護能力；啟用哪一個機制還要看目前控制狀態。','同時支援兩套機制時，不是把兩個解鎖命令都送一次；先確認現在由誰控制。'),
        ('CTRATT.MDS／分割區共享關係','MDS=1 且分割區跨控制器共享，才形成這裡的 until-power-cycle 限制條件。','A、B 共享 BP0 的 multi-domain subsystem：不得把 BP0 設為 Write Locked Until Power Cycle；正常讀取 BP0 並未因此被禁止。'))
context(['base-telemetry'], 'base', [338,491], 'telemetry-capability', '讓控制器支援與主機可理解的資料區一致',
        'Identify 回報 Telemetry 與 Area 4 的能力，Host Behavior Support 則宣告主機是否能處理延伸資料區。兩邊條件配合後，Area 4 欄位才按適用規則使用。',
        ('LPA：Telemetry 支援／DA4S','Telemetry 的基本支援與 Data Area 4 支援是不同能力。','能取得 LID 07h 不代表一定能取得 Area 4；先檢查 DA4S。'),
        ('Host Behavior Support.ETDAS','主機以 ETDAS 宣告能理解延伸 Telemetry Data Area。','若控制器支援 Area 4 但主機未作相應宣告，不能直接使用 Area 4 大小推算應讀的最大範圍。'))
context(['base-telemetry'], 'base', [151,152,155,474], 'telemetry-notice', '從資料可用事件走到紀錄讀取',
        'Asynchronous Event Request 留下一筆等待事件的命令；完成資訊指出事件種類與要讀的 log，詳細資料仍在 Telemetry log 內。',
        ('FID 0Bh.TLN bit 10／TCDA 0→1','TLN 決定當 Controller-Initiated Data Available 由 0 變成 1 時是否傳送 Telemetry Log Changed 事件。','停用 TLN 是停用該通知，不能據此認定沒有 Telemetry 資料。'),
        ('AET／AEI／LID／EVNTSP','事件類型、事件資訊與 LID 共同辨認通知；EVNTSP 的解讀取決於事件種類。','收到指向 LID 08h 的通知後，去讀 TCDA、TCDGN 與資料範圍，不把 AER 的完成項目當成完整 capture。'))
context(['base-sanitize'], 'base', [338], 'sanitize-capability', '方法支援、解除配置與清除保證分別檢查',
        'SANICAP 的不同位元回答不同問題：能執行哪種方法、能否保留配置、以及是否支援更進一步的要求與回報。',
        ('CES／BES／OWS','分別回報 Crypto Erase、Block Erase 與 Overwrite 支援。','主機選 SANACT 前，先檢查對應方法位元；不能只看到 SANICAP 非零便使用任意方法。'),
        ('NDI／NODMMAS → NDAS／NODRM／估計時間','NDI 表示 No-Deallocate 是否被禁止；NODMMAS 補充不解除配置時是否還要修改媒體。','NDAS=1 且 NDI=1 時，NODRM 決定拒絕或以警告模式處理；若需要額外媒體修改，再使用對應時間欄位。'),
        ('SPRRS／PREQ','支援 Purge Request and Reporting 時，PREQ 才按清除要求解讀。','SPRRS=1、PREQ=1，而作業未達 Purge 要求時，應依規格回報作業失敗；命令被接受不保證已達此要求。'))
context(['base-sanitize'], 'base', [311], 'reservation-notification', '清除造成的存取狀態變動使用另一份 log',
        'Reservation Notification 回報 reservation 相關事件。本篇引用它是為了解釋清除流程中的存取狀態變動；清除進度仍由 LID 81h 取得。',
        ('Log Page Count／Notification Type／NSID','計數辨認通知紀錄，類型說明 reservation 變動，NSID 指向受影響對象。','通知中的 NSID=7 是要刷新存取狀態的 namespace，不表示 namespace 7 的 Sanitize 已完成 7%。'))
context(['base-sanitize'], 'base', [312], 'sanitize-status', '把作業狀態、要求參數與時間估計接起來',
        '同一份 log 同時保留狀態與補充資訊。讀取順序是目標、狀態、有效欄位、數值；不要從一個進度值直接跳到「資料已清除」的結論。',
        ('SSTAT.SOS／SPROG','SOS 區分從未開始、完成、進行中、失敗及非預期解除配置。SPROG 依有效條件表示進度。','SOS=010b 仍可能處於 Media Verification 或 Post-Verification Deallocation，不能說清除後的完整流程已結束。'),
        ('SSTAT.OPC／GDE／NDE／MVCNCLD／PRGD','OPC 是已完成覆寫次數；GDE 與 NDE 分別涉及 subsystem 與 namespace 資料狀態；MVCNCLD 記錄驗證是否取消；PRGD 在有效條件下回報 Purge 結果。','覆寫次數已達要求時，仍要讀 SOS 與後續狀態，不能只靠 OPC 宣告回到 Idle。'),
        ('SCDW10','保存啟動相關作業的命令 CDW10，讓狀態與 SANACT、NDAS、EMVS 等原始要求對得上。','先前選 Overwrite 時才把 OPC 當覆寫 pass 數；不要用 Crypto Erase 的紀錄解釋它。'),
        ('ETO／ETBE／ETCE／ETODMM／ETBENMM／ETCENMM／ETPVDS','時間以秒表示；依方法、NDAS 與 NODMMAS 選欄位，驗證後解除配置另有估計。ETO 以 16 passes 為基礎。','FFFFFFFFh 表示未回報時間，不能換算成數十年的剩餘等待；估計也不取代實際完成狀態。'),
        ('SSI.SANS／FAILS／VERS','支援驗證狀態資訊時，SANS 回報目前狀態；FAILS 在 SOS 指出失敗時補充失敗發生的狀態。','SANS 與 FAILS 的數字可能不同，因為前者是現在，後者是失敗發生時。'),
        ('MNSOIP／STNSID','MNSOIP 是允許同時執行的 namespace sanitize 作業數上限；STNSID 確認此次查詢目標。','MNSOIP=4 不表示現在有 4 個作業。查 subsystem 時 STNSID=0；查 namespace 時 STNSID 回應要求的 NSID。'))
context(['base-sanitize'], 'base', [451,452,453,454,492], 'sanitize-options', '每個選項會在哪一階段改變結果',
        'SANACT 先決定動作，再判斷其他位元是否適用。Sanitize Namespace 的欄位集合較小，不能複製整份 subsystem 命令參數而不檢查。',
        ('SANACT／AUSE','SANACT 選方法或控制動作；AUSE 決定失敗後的受限處理路徑。','同樣的 Block Erase，AUSE 選擇不同會走向不同失敗狀態；它不改變方法本身。'),
        ('OWPASS bits 7:4／OIPBP／OVRPAT','OWPASS=0 表示 16 passes，其餘非零編碼直接表示 pass 數；OIPBP=1 還要依總 pass 數的奇偶決定第一遍樣式。','要求 2 passes、樣式 00000000h、反相=1：第一遍 FFFFFFFFh，第二遍 00000000h，最後一遍回到指定樣式。'),
        ('PREQ／SPRRS','PREQ 提出 Purge 要求；SPRRS=0 時該位元為保留位元。','SPRRS=1 且 PREQ=1，若未達規定的 Purge 保證，作業應失敗；不能只靠讀回零來替代這項判斷。'),
        ('NDAS／SANICAP.NDI／FID 17h.NODRM','只有 NDI=1 且要求 NDAS=1 時，NODRM 才決定該衝突的回應。','NODRM=0：Invalid Field in Command；NODRM=1：處理命令，成功時 SOS=100b，告知仍發生解除配置。NDI=0 時 NODRM 不影響行為。'),
        ('EMVS／GDE／後續狀態','EMVS 要求在 sanitize processing 成功後進入 Media Verification；它是要求值，GDE 與狀態是結果資訊。','EMVS=1 不能直接當成現在已進入驗證，仍需查詢 SANS。'),
        ('PMR enabled／pending firmware activation／controller suspended','這些條件可能阻止開始 subsystem Sanitize，各自有命令專屬狀態。','PMR 尚啟用與韌體待 reset 是不同原因；後者還需分辨所要求的 reset 類型。'))

context(['base-sanitize'], 'base', [772,773,775,777], 'sanitize-entry-failure', '先選處理模式，再理解失敗後可走的路',
        '總狀態圖的箭頭代號要對回 transition 表。AUSE 決定 restricted 或 unrestricted 路徑；Idle 是狀態，不是每一種情況下都代表最近一次清除成功。',
        ('A1／B1：Idle → Processing','AUSE=0 走 Restricted Processing，AUSE=1 走 Unrestricted Processing；開始時 SPROG 清為 0，MVCNCLD 清為 0。','同樣的方法可以走不同完成模式；先前進度 80% 不能延用到新作業。'),
        ('A2：Restricted Failure → Restricted Processing','失敗後要以 AUSE=0 開始後續清除，不能用 Exit Failure Mode 直接回 Idle，也不能改成 AUSE=1 迴避限制。','受限失敗後送 Exit Failure Mode，依目標得到 Sanitize Failed 或 Sanitize Namespace Failed。'),
        ('A3／B2：Unrestricted Failure → Processing','可用 AUSE=0 重新進入 Restricted Processing，或 AUSE=1 進入 Unrestricted Processing。','選 A3 是重新開始受限模式的清除，不表示上一次資料已被成功清除。'),
        ('E：Unrestricted Failure → Idle','Exit Failure Mode 可以讓狀態回 Idle，命令成功表示完成這項退出動作。','因此只讀 SANS=Idle 不足以證明 sanitize 成功；還要讀 SOS 的最近作業結果。'))
context(['base-sanitize'], 'base', [774,776], 'sanitize-processing-exit', '處理結束後，成功、失敗與驗證分三條路',
        'Restricted 與 Unrestricted Processing 的成功分支使用相同的 EMVS／MVCNCLD 條件；失敗時才分別進入不同的 Failure state。',
        ('C1／C2 → Idle','處理成功且 EMVS=0，或 EMVS=1 但 MVCNCLD=1 且要求的解除配置成功完成時，回到 Idle。','原本要求驗證但後來被取消，不能省略解除配置條件就直接宣告回 Idle。'),
        ('F1／F2 → Media Verification','處理成功、EMVS=1 且 MVCNCLD=0，才進入驗證。','兩個條件要一起成立：只看命令 EMVS=1，仍不知道驗證是否被後續事件取消。'),
        ('D1／D2 → Failure；SSI.FAILS','處理失敗時，依原模式進入 Restricted 或 Unrestricted Failure；FAILS 分別記 1h 或 3h，指出失敗發生在 processing。','目前 SANS 是 Failure，但 FAILS 是 Processing，這是目前狀態與失敗來源的差別。'),
        ('GDE／NDE／SANS／事件通知','成功轉移依 subsystem 或 namespace 目標更新相應 log 與資料狀態，並傳送相應完成或進入驗證事件。','清除單一 namespace 不能直接把其他 namespace 的 NDE 一起當成已更新。'))
context(['base-sanitize'], 'base', [778,779], 'sanitize-verification-exit', '驗證結束後，還有解除配置的完成點',
        'Media Verification 允許依命令集規則讀取來驗證清除。離開此狀態後，必須追蹤 Post-Verification Deallocation，不能將退出驗證命令的成功回覆當成所有後續工作完成。',
        ('G：Media Verification → Post-Verification Deallocation','指定目標的 Exit Media Verification、適用的 NVM Subsystem Reset／transport reset，或使驗證無法繼續的組態變動都可能觸發此轉移。','namespace 目標要檢查被 reset 的控制器與該 namespace 的附加關係，不能將任何控制器 reset 一概視為同一條件。'),
        ('SPROG／MVCNCLD','轉入後續解除配置時 SPROG 清為 0；適用的 reset 或組態變動也會設 MVCNCLD。','進度從先前數值回到 0，可能是開始新階段；先讀 SANS，再判斷是不是同一階段倒退。'),
        ('H → Idle','成功解除配置該目標中所有已配置的 user-data media 後才回 Idle。','只收到 Exit Media Verification 的成功 CQE，仍需等待這個背景階段的結果。'),
        ('I1／I2 → Failure','解除配置失敗時，依啟動作業的 AUSE=0 或 1 分別回 Restricted 或 Unrestricted Failure。','同樣是後續解除配置失敗，允許的退出／重試路徑仍由原本模式決定；不能隨意選較寬鬆的 failure state。'))

context(['base-namespace-management'], 'nvm', [123,127,134], 'namespace-payload', '把建立資料、格式能力與資源配置逐項配對',
        'NVM Figure 134 列出主機在 Create 時提出的設定；Figure 123 與 Figure 127 提供欄位語意及格式能力。這些結構需要對照閱讀，但不是三份可以相加的建立 buffer。',
        ('NSZE／NCAP／FLBAS／NSFEAT.THINP','FLBAS 選格式，所以容量值必須乘所選格式的資料 bytes；THINP 等能力影響容量要求。NUSE 是查詢到的使用量，不由此 Create payload 指定。','NSZE=250、4 KiB/block 是 1000 KiB；換成 512-byte 格式後，不能繼續沿用同一 byte 容量結論。'),
        ('DPS／LBAFEE／LBSTM／Storage Tag Masking Level','DPS 選保護配置，LBAFEE 決定進階格式是否可用；LBSTM 必須符合允許遮罩與層級限制。','32b／64b Guard 或帶非零 STS 的 16b Guard 建立要求，若 LBAFEE 未設 1，回 Invalid Namespace or Format；遮罩要求不符則是 Invalid Field in Command。'),
        ('NMIC／ANAGRPID／NVMSETID／ENDGID','共享能力與資源歸屬要配合支援條件。後三者填 0 表示由控制器決定，未支援對應功能時忽略。','ENDGID 還決定要檢查哪個 Endurance Group 的 FDP 狀態；FDP 啟用時不支援 NVM Sets。'),
        ('NPHNDLS／Placement Handle List','FDP 啟用時，非零 NPHNDLS 不得超過支援 RUH 數或 128；清單值需在範圍內、不得重複。','支援 4 個 RUH 時，2 筆清單 [1,3] 數量及範圍符合這兩項要求；[1,1] 重複、[1,4] 超出索引範圍，仍須另檢查資源占用與格式。'),
        ('NPHNDLS=0／控制器選定的 RUH','首次此類配置由控制器選未被非零清單 namespace 使用的 RUH；既有 NPHNDLS=0 namespaces 則依規則共享同一個 RUH。','0 不是沒有 handle。主機後來提出非零清單時，也不能占用這個由控制器為零清單配置保留的 RUH。'),
        ('共享 RUH／Format Index／Reserved','共享 RUH 的 namespaces 必須使用相同 user-data Format Index；FDP 未啟用時依表註作保留欄位處理，不能把控制器忽略欄位理解成主機可以填任意值。','RUH 已由 Format Index 2 的 namespace 使用，新 namespace 指定 Format Index 3 卻共用它，會是 Invalid Format。'))
context(['base-namespace-management'], 'nvm', [132,133], 'namespace-granularity', '先選描述子，再用 bytes 比較粒度',
        '粒度清單回答特定格式偏好的配置步幅。NGA.GDM 決定格式到描述子的對應，ND 決定有效數量，NSG 與 NCG 才提供 size、capacity 的 byte 粒度。',
        ('NGA.GDM／ND／Format Index','GDM=0 時 descriptor 0 適用全部格式且 ND=0；GDM=1 時，描述子 index 對應同一 Format Index。ND 是數量減 1。','GDM=1、ND=3 表示 4 個有效描述子；使用 Format Index 2 時讀 descriptor 2，而非挑最大的粒度。'),
        ('LBAFEE／16 或 64 個描述子','Host Behavior Support 的延伸格式宣告決定最多回報 16 或 64 個粒度描述子；清單後方未用項目不代表更多有效格式。','即使傳輸 buffer 足夠長，也不能越過 ND 所界定的有效項目使用數值。'),
        ('NSG／NCG／0h','NSG 用於 size、NCG 用於 capacity，單位都是 bytes；0h 表示未回報粒度。','NSZE=1000、4 KiB/block 得到 4000 KiB，不是 1 MiB 的整數倍；此差異是配置效率提示，不是單獨拒絕有效 Create 的理由。'))

context(['base-hmb-emulation'], 'base', [338], 'hmb-capability', '記憶體建議、最小要求與描述子限制',
        'Identify 提供主機規劃 HMB 所需的大小與描述子限制；AVSCC 與 ICSVSCC 則是本篇另一主題的廠商命令格式能力，不能當成 HMB 啟用條件。',
        ('HMPRE／HMMIN','偏好與最小容量使用固定 4 KiB 單位；實際 HSIZE 使用 CC.MPS 指定的頁大小。','HMPRE=64 是 256 KiB；若 page 是 8 KiB，提供同樣容量的 HSIZE 是 32。'),
        ('HMMINDS／HMMAXD','分別限制描述子所描述區域的最小大小與清單描述子數量；仍需按各欄位的零值及有效性規則使用。','總容量已達要求，但被切成過多小區域，仍可能不符合描述子限制。'),
        ('CTRATT.HMBR／HMNARE／HMNAR','能力決定是否支援 non-operational 狀態下的 HMB 存取限制；設定政策與目前限制狀態分別觀察。','能力存在不等於目前限制已生效；也不能把主機發起的 Admin 作業與控制器自主活動混為一類。'),
        ('AVSCC.VSCF／ICSVSCC.SNVSCF','分別描述 Admin 與 I/O 廠商命令採用的格式約定。','先辨認命令種類和支援格式，再使用對應長度欄位；不能因 Admin 有標準格式就推論 I/O 廠商命令相同。'))
context(['base-power-features'], 'base', [338], 'power-capability', '從可選狀態數到可設定的熱管理範圍',
        '讀 Power State Descriptor 前，先由 Identify 確認狀態數、自動轉移支援與熱管理能力；這些欄位負責告訴主機後面哪些設定有意義。',
        ('NPSS／APSTA','NPSS 是支援狀態數減 1；APSTA 回報 APST 能力。','NPSS=3 表示 PS0–PS3 共 4 個狀態，但仍要看每個描述子的 NOPS，才能知道哪些可以當 ITPS。'),
        ('HCTMA／MNTMT／MXTMT','HCTMA 回報 HCTM 支援，最小與最大溫度界定可設定的門檻，單位是 Kelvin。','設定 TMT1、TMT2 前先確認它們在此範圍內，再檢查相對順序及停用值規則。'),
        ('WCTEMP／溫度事件門檻','警告複合溫度資訊與主機設定的事件／管理門檻用途不同。','不要把 WCTEMP 原值直接當成全部感測器的 TMT1；先確定要控制或觀察哪一項。'),
        ('RTD3E／RTD3R','分別提供進入 RTD3 與恢復所需的預估延遲資訊；不等於某個 NVMe PS 的 ENLAT／EXLAT。','考慮移除主要電源時，比較兩段延遲與預期閒置時間；不能把 D3cold 當成 PS3 的別名。'))
context(['base-admin-fw-logs'], 'base', [338], 'firmware-capability', '把更新策略連到裝置實際提供的能力',
        '規劃更新時要一起查可用 slot、更新粒度與啟用方式。版本字串只描述目前回報的版本，不能代替能力檢查。',
        ('FR／FRMW.NOFS／FFSRO／FAWR','FR 是版本資訊；NOFS 是 slot 數，FFSRO 說明第一個 slot 的唯讀性，FAWR 描述不需 reset 的啟用能力。','有多個 slot 不表示第一個一定可覆寫，也不保證任意映像都能立即啟用。'),
        ('FWUG／MDTS／MTFA','更新粒度、最大傳輸量與最大啟用時間涉及不同階段。','分段大小先受傳輸與粒度限制；不能把啟用時間 MTFA 拿來算 Download 每段 bytes。'),
        ('MDS／DID／SMUD／MPTFAWR','多 domain 的識別、同步更新支援及多次更新後啟用的相關能力，決定是否需要協調多個控制器。','存在多個 domain 時，不能只由其中一個 controller 的版本回報推論整個 subsystem 已同步完成更新。'))
context(['base-admin-fw-logs'], 'base', [155,474], 'firmware-notice', '啟用通知提醒主機觀察版本切換',
        'FID 0Bh 的 Firmware Activation Notices 控制對應通知，事件代表韌體啟用正在開始；目前 active slot 與版本仍需由 LID 03h 重新確認。',
        ('FAN bit 9／Firmware Activation Starting','啟用相應通知後，適用事件告知主機啟用活動開始。','收到事件並不代表新的 firmware 已完成所有必要的 reset 或切換，仍需沿啟用流程查看。'))
context(['base-admin-fw-logs'], 'base', [347,348], 'firmware-uuid', '查詢 log 時，UUID 的清單位置與值分開',
        '需要 UUID 選擇的命令，以 UIDX 選 Identify 回傳的清單項目；UUID List 與其中的 Entry 結構共同定義這個對應。',
        ('UIDX／UUID List Entry／IDASSOC／UUID','索引選項目，識別關聯指出項目的用途，128-bit UUID 是項目所保存的識別值。','UIDX=2 不等於 UUID=2；應找到該項目的完整 UUID 與關聯，再決定是否適用本次查詢。'))
context(['base-boot-partitions'], 'base', [187,188,189,190,191,192,193], 'boot-update-fields', '從下載片段走到指定 Boot Partition',
        '這裡只使用 Firmware Download／Commit 與 Boot 更新有關的分支。下載的來源記憶體、完整映像中的位置、目標分割區與啟用選擇是不同座標。',
        ('DPTR／NUMD／OFST','資料指標指本次主機 buffer；NUMD 是傳輸 Dword 數減 1；OFST 是完整映像中的 Dword 位移。','傳 4096 bytes 用 NUMD=1023，接續下一段的 OFST 增加 1024。'),
        ('CA=110b／BPID','將下載內容替換指定 Boot Partition 的內容，仍需滿足寫入保護、映像與下載順序等要求。','BPID=1 選 BP1；若它仍受寫入保護，不能因 Download 成功就推論 BP1 已被改寫。'),
        ('CA=111b／BPID／ABPID','選 active Boot Partition 是另一個 Commit 動作，與替換內容分開。','先替換 BP1 再選它為 active；讀回 ABPID 確认啟用選擇，與讀回映像核對內容是不同觀察。'),
        ('MUD／命令專屬狀態','完成資訊需按動作與能力判讀；Boot Partition Write Prohibited、Invalid Firmware Image 與下載 Overlapping Range 分別針對不同條件。','同樣未完成預期更新，可能是分割區保護、映像驗證或傳輸範圍問題，不能全歸為「映像壞掉」。'))
context(['base-sanitize'], 'base', [151,152,156], 'sanitize-events', '事件引導主機讀取作業的詳細狀態',
        'Asynchronous Event 的完成資訊指出事件種類與相關 log；Sanitize Status 才提供目標、作業狀態與原始要求等內容。',
        ('AET／AEI／LID／EVNTSP','事件類別、事件資訊及 log identifier 一起指向相應結果；事件專屬資訊依該種類定義讀取。','收到清除相關事件後，先確認所指目標及 LID 81h 的狀態，不從 AER 的 Successful Completion 直接推論清除成功。'),
        ('Operation Completed／Unexpected Deallocation／Entered Media Verification','這三種事件區分作業結束、非預期解除配置及進入驗證階段。','Entered Media Verification 代表接下來可依規則驗證，與已回到 Idle 的完成通知不同。'))
context(['nvm-command-set-1.3'], 'base', [338], 'nvm-capability', '由共同 Identify 結構查 NVM 操作的前提',
        'Base Identify Controller 提供跨命令使用的能力與限制；NVM 命令集的 Identify 結構再補上格式與命令專屬能力。兩份資料需要按同一控制器配對。',
        ('ONCS','各位元回報特定選用 NVM 命令或功能的支援，應按所選操作檢查相應位元。','Compare 支援不能替代 Copy 支援；不能只看 ONCS 非零就使用所有選用命令。'),
        ('MDTS／CAP.MPSMIN','非零 MDTS 以最小 memory page 大小為基礎計算最大傳輸量，與 namespace 的 LBA 大小不同。','MDTS=5、最小 page=4096 bytes，最大傳輸量是 4096×2^5=128 KiB；再換成所選格式的 blocks。'),
        ('CTRATT／SANICAP','前者提供控制器屬性，後者提供清除方法及相關能力；命令專屬設定要沿對應位元分支確認。','準備 Crypto Erase 時查 CES，再依目標與後續要求檢查其餘條件；不由支援 Block Erase 推論其他方法。'))

context(['base-sanitize'], 'base', [770], 'sanitize-targets', '沿資料所在位置，比較兩種清除目標',
        '先選 subsystem 或單一 namespace，再沿表的資料類別逐列比較。對每個 namespace 都執行清除，仍不等同執行一次 subsystem 清除。',
        ('已配置與已解除配置的媒體','subsystem 涵蓋整體相應媒體；namespace 涵蓋配置給目標使用、以及先前配置給它後又解除配置的媒體。','只看目前 LBA 對應的配置不足以理解範圍，先前已解除配置的資料也需要依此規則處理。'),
        ('volatile／non-volatile caches／其他內部 buffers','兩種目標都要處理對應 user data；namespace 範圍依曾對該目標讀寫的資料限定。','資料暫存在內部 buffer，不會因尚未寫入最終媒體就自動落在清除範圍之外。'),
        ('不可寫媒體／不可改寫的 subsystem 資訊','含 user data 但不能寫入的媒體仍需達到不可取回要求；序號等不可寫 subsystem 資訊則不受影響。','「不可寫」不是所有資料的免除條件：含舊 user data 的區域與裝置序號是兩個不同類別。'),
        ('Features／Log pages','依功能及目標需要修改相關資訊，避免從它們恢復 user data；namespace 的 Purge Namespace Metadata 與 Namespace Admin Label 另有指定處理。','不能只清除一般 Read 的資料區，卻忽略可能留在 log 或功能值裡的 user data。'),
        ('Boot／HMB／Firmware／security credentials／RPMB','這些列不因 Sanitize 自動變成已清除；規格對 Boot、HMB、firmware、認證資訊等列有無影響的界線。','subsystem Sanitize 成功不表示 Boot 映像被抹除，不能用它代替 Boot 更新。'),
        ('CMB／PMR／NVMe-MI PDA','namespace 清除不影響這三類；subsystem 清除修改 CMB 中非佇列資料，佇列是否修改由實作決定，PMR 與 PDA 資料另在相應範圍內。','PMR 必須先停用才允許開始 subsystem Sanitize；逐一清除 namespaces 不能替代這項 PMR 資料處理。'))
context(['base-sanitize'], 'base', [771], 'sanitize-overwrite-passes', '從第一遍樣式推到最後一遍與 PI',
        '這張表同時使用反相選項、總遍數的奇偶、目前是第幾遍，以及資料是否為 PI。第一遍並非所有情況都使用命令給的樣式。',
        ('OIPBP=0','每一遍的 user data 都使用指定 Overwrite Pattern，PI 的每個 byte 設為 FFh。','OVRPAT=12345678h 時，增加 pass 數不會在相鄰 passes 之間自動反相。'),
        ('OIPBP=1／總遍數為偶數','第一遍 user data 使用指定樣式的反相，PI bytes 從 00h 開始；後續每遍將前一遍各 bit 反相。','OVRPAT=00000000h、2 passes：user data 為 FFFFFFFFh→00000000h；PI byte 為 00h→FFh。'),
        ('OIPBP=1／總遍數為奇數','第一遍 user data 使用指定樣式，PI bytes 從 FFh 開始；後續同樣逐遍反相。','OVRPAT=00000000h、3 passes：user data 為 00000000h→FFFFFFFFh→00000000h；PI byte 為 FFh→00h→FFh。'),
        ('最後一遍／metadata 中的 PI','奇偶規則讓最後一遍回到指定 user-data 樣式，PI bytes 為 FFh；非 PI 的 user-data 部分按另一欄處理。','不要把 user-data 的 32-bit OVRPAT 直接套到所有 PI bytes，兩欄的起始規則不同。'))
