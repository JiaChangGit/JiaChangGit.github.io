"""PCIe register relationships, kept beside the figures that use them."""


def install(guide):
    def p(numbers, key, title, relation, *rows):
        guide('pcie', numbers, key, title, relation, list(rows))

    p([1,2,3,4,8], 'transport', '從命令的意思走到 PCIe 上的實際傳送',
      '命令集決定 Read 要做什麼，Base 定義 SQE、CQE 等共同結構；PCIe Transport 再把佇列、MMIO 與中斷接起來。讀分層圖時，沿一筆命令穿過各層，便能看出每層負責的工作。',
      ('SQE／DMA／CQE','主機先在可供控制器存取的記憶體放好命令，控制器取走命令並搬運資料，最後寫回完成項目。','Read 的資料進入 DPTR 指向的 buffer；CQE 則回到 CQ，兩者不是同一份資料。'),
      ('Controller Properties／PCI Configuration Space','PCI 組態空間負責辨識與配置裝置，BAR 指向 NVMe 暫存器所在的 MMIO 空間。','先從組態空間取得 BAR，再以該基底加上 NVMe property offset 找到暫存器。'))
    p([5,6], 'doorbell', '由佇列編號算出 Doorbell 位址',
      'SQ Tail 與 CQ Head Doorbell 交錯排列。CAP.DSTRD 決定相鄰 Doorbell 的 byte 距離，佇列編號 y 決定要選哪一對；寫入值則是新的佇列索引。',
      ('CAP.DSTRD／y','間距是 4 << DSTRD bytes，SQ 使用 2y，CQ 使用 2y+1。','DSTRD=0、y=2：SQ offset=1000h+4×4=1010h，CQ offset=1014h。'),
      ('SQT／CQH','SQT 通告已提交到哪裡；CQH 通告主機已消費到哪裡。','寫入 Doorbell 的 3 是佇列索引 3，不是要控制器移動 3 bytes，也不是命令完成碼。'))
    p([7,9,27,34,35,36,37,38,39,40,41,42,43,44,45,46], 'interrupts', '從 CQ 找到中斷向量與訊息',
      '先選中斷機制，再由 Create I/O CQ 的 IV 連到向量。MSI 的訊息設定位於 capability；MSI-X 用表格保存各向量的位址、資料及遮罩。向量是通知路徑，CQE 才保存命令結果。',
      ('IV／MME／MMC','MSI 的 MMC 回報能力、MME 選已啟用向量數；IV 不能超出實際可用範圍。','裝置能支援多個向量，不表示驅動程式已啟用全部向量。'),
      ('MA／MUA／MD／C64','MA 與必要的 MUA 組合訊息目的位址，MD 是寫往該位址的資料；C64 決定位址結構。','控制器以訊息寫入觸發中斷，主機再讀 CQ；不能把 MD 當成 NVMe status。'),
      ('PVM／MMASK／MPEND','能力決定是否有逐向量遮罩；MASK 控制通知，PEND 表示被遮罩期間待處理的通知。','解除遮罩前仍需按照所用機制處理 pending，不能假設遮罩會清除 CQE。'),
      ('MXE／FM／TS','MSI-X enable、整體遮罩與表格大小共同決定哪些向量可使用；TS 是從 0 起算的大小編碼。','TS=3 對應 4 個 table entries；其中某筆仍可能被單獨遮罩。'),
      ('TBIR／TO／PBIR／PBAO','BIR 選 BAR，offset 選該 BAR 空間中的 Table 或 Pending Bit Array。','若 Table 與 PBA 選不同 BAR，必須分別加到各自基底，不能沿用同一個地址。'),
      ('IPIN／ILINE／NEXT／CID','傳統中斷資訊與 capability 串列提供不同機制的入口；NEXT 串起 capability，CID 辨識類型。','先沿 capability 串列確認 MSI-X 是否存在，再讀它的 MXC；不要依固定絕對 offset 猜位置。'))
    p(list(range(10,27))+[28,29], 'configuration', '先辨識裝置，再配置可存取的資源',
      '組態空間圖是一張地圖：識別欄位讓軟體選擇驅動程式，BAR 描述 MMIO 資源，Command 控制存取方式，Status 記錄裝置狀況。舊式 PCI 相容欄位仍在版面中，但不代表 NVMe 要用它們處理 I/O。',
      ('VID／DID／RID／SSVID／SSID','廠商、裝置、revision 與 subsystem 識別分別描述不同層次。','同樣的 DID 可以出現在不同板卡配置；不能只由它推論 firmware 版本。'),
      ('BCC／SCC／PI／HTYPE','Class Code 辨識裝置類別及介面，Header Type 決定後續組態版面。','這裡的 PI 是 Programming Interface，不是資料保護資訊 Protection Information。'),
      ('CMD／STS','Command 中的存取控制與 bus mastering 等位元決定裝置可以採取的動作；Status 記錄條件及錯誤。','改變控制位元與清除可寫 1 清除的狀態位元是不同操作，不能對整個區塊任意回寫讀值。'),
      ('MLBAR／MUBAR／BA／TP／PF／RTE','64-bit 記憶體 BAR 由高低部分組合，低位的型別屬性不屬於基底地址。','先遮去 BAR0 的屬性位元，再與 BAR1 組成基底，最後加上 NVMe register offset。'),
      ('BAR2／EROM／RBA／CAP.CP','其他 BAR、選用 ROM 與 capability pointer 各有自己的用途及存在條件。','CAP.CP 指向 capability 串列，與 NVMe CAP controller property 是兩個不同位置。'),
      ('BIST／CLS／MLT／CCPTR／MGNT／MLAT','依各圖的固定值、選用性及存取屬性讀取相容欄位；PCI BIST 與 NVMe Device Self-test 不是同一個命令機制。','欄位存在於 PCI header，不足以證明控制器支援 NVMe 延伸自我測試。'))
    p([30,31,32,33], 'pci-power', 'PCI 電源狀態與 NVMe Power State 分開讀',
      'PCI Power Management capability 先回報支援哪些 PCI D-states，再透過 PMCS 控制狀態及喚醒事件；NVMe 的 PS0、PS1 則由另一組命令與描述子管理。',
      ('PC.D1S／D2S／PSUP／PMCS.PS','能力與要求狀態要配合，不能選未支援的狀態。','PMCS.PS 的 D3 編碼不是 NVMe PS3；兩者的數字碰巧相同不代表同一層。'),
      ('PMEE／PMES／NSFRST','PME Enable 控制事件通知，PME Status 記錄事件，重設相關欄位補充狀態轉移後的行為。','通知被停用不表示事件狀態從來沒有成立；讀值與清除規則分別查表。'))
    p(list(range(47,58)), 'link-device', '支援上限、要求設定與實際鏈路結果',
      'Capability 說明能做什麼，Control 說明軟體選了什麼，Status 說明目前發生什麼。把三者並排，就能避免用宣告上限代替實際速度或寬度。',
      ('PFS／MPS／MRRS','支援的 payload 上限、選定 payload 大小及最大 read request 大小影響不同交易。','MRRS 的 read request 大小不等於每一個返回 completion 都有同樣大小。'),
      ('FLRC／IFLR／TP','能力決定能否發動 Function Level Reset，控制位元提出要求，Transaction Pending 補充未完成交易狀態。','支援 FLR 與目前已執行過 FLR 是不同結論。'),
      ('PXLCAP／PXLC／PXLS.NLW／CLS','鏈路能力、ASPM 等控制及協商出的寬度速度需要一起看。','支援 x4 的裝置目前 NLW=x2 時，要以 x2 說明此次連線。'),
      ('L0SL／L1L／L0SEL／L1EL／ASPMC','裝置可接受延遲與鏈路退出延遲配合省電狀態控制。','較深省電狀態要計入退出時間，不能只比較活動功耗。'),
      ('PXDS.CED／NFED／FED／URD','狀態分開記錄可修正、非致命、致命及不支援要求等情況，完整原因可再對照 AER。','PCIe 錯誤狀態不會直接等同 CQE 的 SC。'),
      ('PXDCAP2／PXDC2：LTR、OBFF、Completion Timeout','第 2 組能力與控制延續相同配對：先確認支援，再解讀啟用及數值選擇。','有 LTRS 才能依對應條件使用 LTRME；不能看到控制位元就省略能力檢查。'))
    p(list(range(58,68)), 'aer', '把錯誤是否發生、是否通報與嚴重程度分開',
      'AER 用相同錯誤類型在多張暫存器表中對齊。Status 記錄發生，Mask 決定通報，Severity 決定不可修正錯誤的分類；Header Log 則保留相關交易的內容。',
      ('AERUCES／AERUCEM／AERUCESEV','以同一個錯誤位元位置讀 status、mask、severity，不能把三張表當成三種獨立錯誤。','例如 Completion Timeout：先查是否發生，再查是否被遮罩，最後查 fatal／non-fatal 分類。'),
      ('AERCES／AERCEM','可修正錯誤也把記錄與遮罩分開，清除 status 要遵循 RWC 等存取屬性。','遮罩一種錯誤不代表從硬體上消除造成錯誤的條件。'),
      ('FEP／MHRC／MHRE／ECC／ECE／EGC／EGE','第一筆錯誤指標、多重 header 記錄，以及 ECRC 檢查／產生的能力和啟用位元補充診斷關係。','先有對應 capability，再解讀 enable；不能把 enable=0 當作不支援。'),
      ('HB0–HB7／TPL prefix','Header Log 與選用 Prefix Log 保存封包相關片段，需按有效性及 log 格式重組。','這是 PCIe 交易資訊，不是 NVMe Error Information Log 的一筆紀錄。'))
    p([68,70,71,72,73,74,75,76,77], 'eye', '從量測要求走到每條 Lane 的眼圖',
      '先送出量測動作，再讀表頭確認結果與總長度，最後依 descriptor 大小逐條讀 Lane。眼圖代表接收端訊號餘裕；有效狀態與量測條件必須和圖一起保存。',
      ('ACT／MQUAL／TC／EOMIP','動作、品質與目標控制量測；進行中狀態決定結果是否已可使用。','發動量測後，先確認完成，再使用本次 lane descriptors；不能把舊結果當成新量測。'),
      ('Header／descriptor count／descriptor size','表頭給出解析整份 log 所需的大小與數量；Get Log offset 指向 log 內位置。','取得表頭後計算下一段的 offset 與長度，避免把 Printable Eye 區誤認成下一個 descriptor。'),
      ('LN／MSTAT／MSCS／TOP／BTM／LFT／RGT','Lane number 指定對象，狀態與量測步數影響數值是否可用，四個方向描述開口邊界。','比較兩條 lane 前先確認量測成功及相同條件，再比較上下左右的餘裕。'),
      ('EYE／Printable Eye','圖形是量測資料的呈現；座標、字元格式與縮放需依來源說明讀取。','圖看起來較寬不一定代表不同測試條件下的訊號更好，先核對量測尺度。'))
    p([69], 'interface-report', '裝置介面回報中的範圍與內容',
      '這份報告把處理當時的 NVMe 控制器設定與狀態記錄下來，並提供佇列狀態的雜湊。先確認格式版本，再將每個快照欄位連回它所代表的 property。',
      ('TNI／TI.VER','TNI 固定為 4E564D65h，VER=1h 辨認此資料結構版本。','先確認識別值與版本，再讀後面的位元配置；版本不是 firmware revision。'),
      ('IOCQESV／IOSQESV／MPSV／CSSV','保存當時佇列項目大小、記憶體頁大小與命令集選擇欄位的值，需按各原始欄位編碼換算。','IOSQESV=6 表示項目大小編碼對應 64 bytes，不是 6 bytes。'),
      ('STV／SHSTV／SHNV／ENV／ACPS','前四者保存關機與啟用狀態；ACPS 另描述從最近 controller reset 到 CONFIG_LOCKED 之間的 Admin 命令處理狀況。','ACPS=1 包含未處理 Admin 命令及相應 head／tail 為 0 的條件，不能只讀 ENV 就代替這段歷史。'),
      ('AQV／ASV／ACV／CV／PMV／PCV','分別對回 AQA、ASQ、ACQ、CMBMSC、PMRMSC、PMRCTL 的回報值。','以報告規定的欄位寬度及版本讀取快照，不將整段 bytes 直接當作一般 MMIO 空間重新映射。'),
      ('CU／VU／QH','CU、VU 指出產生 Queue Hash 所採用的 Controller State 格式；QH 對依序串接的相關欄位計算 SHA-384。','比較兩個 QH 前先確認它們使用的狀態格式及時點；QH 不會直接列出哪筆命令完成。'))
