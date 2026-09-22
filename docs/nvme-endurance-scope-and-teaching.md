# Endurance Group Information／Event Aggregate／Configuration 維護紀錄

2026-09-22 使用者要求完成 Base §5.2.13.1.10（LID09h）、
§5.2.13.1.15（LID0Fh）、§5.2.30.1.17（FID18h）。
主範圍只有這三節，4 張主範圍圖是 Figures 224、225、261、493；
16 張必要引用限制到範圍、命令封裝、能力、通知與確認相關欄位。
來源 PDF 保持私有。NVM §1.4.2.1／§1.4.2.10 只補 HRC／HWC 分類，
不新增 NVM 命令格式或其他專題。所有 Fabrics 內容排除。

教學先建立 Group 觀察範圍，再教警告、數值換算、設定、清單與事件生命週期。
HTML 自成完整課程；兩篇 post 主軸、例子、問題一致，最後才提供順向 PDF 路徑。
共用欄位解說只放一处，各 Figure 另有不同的重點與算例。

必須保留的核對結果：

- LID09h 的 EGCW 是讀取當時狀態；FID18h 同名欄位是選擇遮罩。
  有效警告 bits 0、2、3，全部選擇為0Dh，0Fh會誤啟用保留bit1。
- Group7／mask05h 的 FID18h CDW11=00050007h；Get Log Page
  的 Group7 則是 LSI7，CDW11=00070000h，兩種 CDW11 不可混用。
- LID0Fh/RAE0 清除 aggregate-change notice；LID09h/Group/RAE0
  成功才確認該組事件並移除清單項目。RAE1與失敗讀取都保留事件。
  確認事件不是媒體修復；持續條件的再次通知政策要在確認前考慮。
- AER Notice 為 AET2、AEI06h、LID0Fh，DW0=000F0602h。
  此回覆沒有 ENDGID；清單可能代表多組。
- FID0Bh 的 EGEALCN bit14 是 controller 通知選擇；FID18h 是逐 Group
  警告選擇，還要有未完成 AER。兩種 Feature 範圍不同。
- Figures 209 的 Restore to Default Content 是註腳9定義的
  **回復出廠預設內容**，不是一般 reset 或 power cycle。
  09h=N、0Fh=Y 不可拿來推一般 reset 行為。
- Figure466 持續性欄只適用不可保存的 Feature；不得把 No 解成
  FID18h 所有實作都禁止保存。先確認 ONCS.SSFS、SEL3 的 SVBL。
- EE/DUR/DUW/MUW 的單位為十億 bytes、向上取整；0為未回報。
  TEGCAP/UEGCAP 是 bytes、0同樣未回報。HRC/HWC是命令數。
  不將量化後MUW/DUW宣稱為精確寫入放大率。
- NVM 的 HRC 分類為 Compare、Copy、Read、Verify；HWC分類為Copy、Write。
  Base表內通用命令類別不是「必須與主機搬資料」的意思。
- NUMENT直接計數；Entry1在byte8，0-based index i在8+2i。
  [1,2,7]共14-byte內容、16-byte傳輸、NUMD3；尾端0不是Group0。
  ENDGIDMAX是最大ID而非Group總數，也非目前待處理數。
- Figure225全欄均教學，包括EGFEAT媒體種類、DID、各16-byte計數器、
  保留區與零值差異。相關SMART圖只取byte0的bits0、2、3。
- Base §3.2.3 的舊交叉引用把 FID0Bh 指向 §5.2.30.1.5；正文實際
  標題是 §5.2.30.1.6。本篇使用已核實的章節，不把舊引用複製進文章。

驗證：原有報告交付物及範圍紀錄應保持不變。新例子測試驗證bit位移、
byte layout、round-up區間與確認語意；瀏覽器檢查三版、三種尺寸、明暗模式。
發布必須確認同一commit的內容驗證與Pages部署都成功，再逐份比對線上內容。
