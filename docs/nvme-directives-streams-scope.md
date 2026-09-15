# Directives／Streams 專篇範圍與核對紀錄

2026-09-15 使用者指定：Base 2.4 §8.1.9（排除 §8.1.9.4）、§5.2.7、§5.2.8、§5.2.30.1.35（FID 81h），加 NVM Command Set 1.3 §5.13。沿用既有 Fabrics 全部排除要求，因此 Host Identifier 保留共同規則與 PCIe §5.2.30.1.35.1，不包含 .35.2。

這是新增專篇，不更改 Admin／I/O 整合篇的排除項。共 15 篇、45 份交付物；本篇的中文 HTML 有獨立課程，中英文 post 以對等的全局說明、例子與單向 Spec 路徑報告。

主範圍含 Base Figures 181–186、537–538、702–715，共 22 張。必要引用 15 張：Base 36、93、143、197–199、201、212、338、463–465，以及 NVM 70–72。必要引用只教命令與 Feature 的欄位、能力前提、錯誤參數位置及 Write／Streams 的連接，不擴大為來源整章。逐圖來源、必要性及教學歸屬登記於 scope.json 與 figure-table-register.json。

實際 PDF 檢視器路徑：Base 227–228 → 534–536 → 642–646 → 646–653 → NVM 175。共同頁面在下一個排除標題前停止；Base 653 的 §8.1.9.4 不讀。原 PDF 部分目錄的頁碼與正文不一致，使用正文與 PDF 頁碼核對，不從目錄推算。路徑只出現在 post。

核對中特別保留的條件：

- Enable 的外層 CDW11.DTYPE=00h 選 Identify，CDW12.DTYPE=01h 才選 Streams。§8.1.9.3 在互斥啟用限制中的文字不宜拿來覆寫 Figures 704／706 的明確編碼。若拒絕產生 Error Information 紀錄，原文要求 PEL 指 DOPER；本篇以 byte offset 44 解釋。
- NSSA 是未專用配置的資源池大小；NSSO 計其中開啟數。不能把 NSSA 寫成完全閒置數。
- Allocate 請求 NSR 與回覆 NSA 是直接計數；NUMD／NLB 才使用數量減 1。
- 空間不足時的串流替換與忽略提示，不表示 Write 的資料被丟棄。
- Release Identifier、Release Resources、停用、Format、刪除／寫入保護各有不同效果，不把 Format 釋放編號擴成一定歸還專用資源。
- 0h Host Identifier 不跨控制器建立共同主機關聯，改成非零值不移轉舊資源；CTRATT.RHII=0 是未回報，不能當作肯定支援零值 reservation。
- Streams 的 SDIRCLR=0 需連同同一主機仍有已啟用控制器的例外閱讀。

PDF 原檔、原文擷取及瀏覽器驗證截圖只留在私有本機路徑，不加入 Git 或 Pages。公開內容使用自行撰寫的解釋、重新設計的關係圖與精確來源定位。
