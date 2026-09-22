# SQ Associations 範圍與維護

2026-09-22 使用者指定 Base §8.1.28，沿用三版與驗證後提交／push 授權。

- 主範圍位於 Base 2.4 PDF 758–759（印刷頁 732–733），從 SQ Associations
  標題開始，到 §8.1.29 前停止。本節沒有獨立編號 Figure／Table。
- 15 張必要引用已登記為 dependency／scope-reduced。Figures 67、338、751
  支援物件與模式背景；333、334、336、343–346 支援查詢和歸屬；575–579
  支援 PCIe 的 SQ 建立。長表只讀明列欄位，Fabrics 一律排除。
- 中文 HTML 按用途、能力、清單、建立、分流進階；每張依賴圖有獨立重點、
  算例與共同欄位教學連結。中英文 post 採相同全局結構，另有順向 Spec 路徑。
- 主範圍對 PLM 的交叉引用寫成 §8.1.20.1，Identify CTRATT 也有舊號引用；
  以本版實際標題定位為 §8.1.21，操作規則為 §8.1.21.1。不可直接照搬舊號。
- SQ Associations 是選用提示；PLM 不依賴使用 SQA。SQA 支援必須搭配
  CTRATT.NSETS 與 CTRATT.PLM；0124h 是相關遮罩，不是整欄的唯一合法值。
- Create I/O SQ 的 NVMSETID=0 明確表示無特定關聯。不得套用別的命令對 Set 0
  的保留規則。SQA 支援且非零 Set 不在清單時，命令必須回 Invalid Field。
- 後續錯誤分流違反主機操作規則，可能影響 PLM；本節沒有定義必定拒絕此類
  I/O 的錯誤碼，不能改寫成存取控制或隔離保證。
- NUMENT 是直接筆數，Entry i 起點為 128+i×128；NSETID 是儲存在 entry
  裡的識別值。R4KRT 的 100 ns 單位及 DTWIN／每 Set 一筆在途命令條件要一起教。
- SQ3／64 entries／CQ2／Set 7／PC1 範例為 003F0003h、00020001h、
  00000007h；round robin 忽略 QPRIO。建立這條 Admin 命令的完成回 Admin CQ，
  和建立後 SQ3 的 I/O 完成回 CQ2 分開。
- 不重複引用同一教學段套給多張 Figure；狀態、識別值與容量不能混成表格同一欄。

驗證應涵蓋命令反解、Set 清單位移、能力遮罩、15 張圖的獨立教學與來源、雙語
一致性及 post 專用路徑。發布前檢查 iPad／desktop 與明暗模式、全部既有報告
不變性，以及同一提交的報告驗證與 Pages 部署，最後比較線上實際內容。
