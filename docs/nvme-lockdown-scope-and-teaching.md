# Command and Feature Lockdown 維護紀錄

2026-09-16 使用者要求合併 Base §8.1.5、§5.2.13.1.20（LID14h）、§5.2.16。
三版為獨立中文教學 HTML 與內容對等的中英文全局報告。既有16篇範圍不變。

## 範圍與教學

- 10個學習單元：目的、支援層級、目標範圍、查詢、一般Log、增強Log、完整命令、結果、持續性、UUID。
- 全部8張主範圍圖：274～278、365～367。§8.1.5無獨立圖。
- 21張必要引用：28、93、99、101、103、203～208、292、338、347、348、512～514、518、519、782。
- 大型Figure338只取OACS.CFLS／CCFLS；Figure28只取所用Admin opcode；Figure103只取本篇狀態。
- 共用欄位教學集中一處，逐圖仍有獨立重點、算例與來源。前向Spec路徑僅在post。
- 必要背景說明Personality持續性、凍結與認證例外、UUID索引，不延伸認證封包、金鑰操作或其他personality。沒有提供NVMe-MI規格，帶外內容只採Base明載語意。
- Fabrics、Discovery、NQN持續排除；新的指定範圍不更動Admin／I/O篇排除清單。

## 原始規格定位與易錯處

- 主路徑採PDF實際頁305～309 → 431～434 → 623～625；共享頁分別從本篇標題開始，停在5.2.13.1.21、5.2.17、8.1.6之前。
- §8.1.5 PDF624將Lockdown交叉引用誤寫為5.2.15，實際命令是5.2.16。Figure278將Scope Selected縮寫誤寫為CS；header實際欄位是SS。教材使用實際定義定位。
- 一般Log的全體可禁止／Admin已禁止清單與增強CNTLIDFFFFh的至少一台回報清單不同；ACNTL0表示部分而非全部。
- ELPF0不使用LSI.CNTLID；ELPF1要CCFLS。Log CNTTS1/2對應不同介面，不與Lockdown IFC1/2編碼互換。
- CSEL1/2不取得CSEL0在LDPE1下的跨power-cycle持續性。
- LDPE輸入在CDW11，LDPS輸出在CQE DW1；Get DW0另含PPSC／PERFS，不合併成同一狀態。
- CCFLS是OACS13，CFLS是10。命令例子：CDW10 00010612h，允許00010602h，CDW14 00070000h。512-byte一般FID禁止查詢007F1214h。
- LNGTH／NCFID直接計數；NUMD為Dword數減1。增強第二筆byte18不是可直接使用的4-byte對齊GetLog offset；從16取包含它的資料。
- 2-byte描述器不代表每份增強Log都是512bytes。依SZE與CFIDS解析；傳輸超出的尾端不假設填0。
- SC23h屬通用狀態，Lockdown1Fh／28h屬命令特定；介面不支援OFI時，should28h／mayInvalidField保留原文強度。
- 前一篇修正的Ruby3.3／Bundler相容性與全套CI核對流程不變。來源PDF、文字抽取與QA截圖只留忽略目錄，不公開。
