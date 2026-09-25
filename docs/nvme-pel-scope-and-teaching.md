# Persistent Event Log 維護紀錄

使用者核准主範圍：Base 2.4 §5.2.13.1.14（LID 0Dh）與 NVM Command Set 1.3 §4.1.4.4。
2026-09-25 新增第 22 篇；三版共使專案交付物增至 66 份。PDF 保留在使用者文件目錄，不發布。

- 主範圍為 Base Figures232–260 與 NVM Figure112，共30張；必要引用31張。
- 中文 HTML 按理解順序編排10個單元、6個不同觀念的問答；27組欄位教學共用說明，不重複逐圖套文。實際組數由 `GUIDES` 管理。
- 中英文 post 使用同一組雙語核心結論、圖表與案例；Base PDF270–296 往前報告，最後只切一次至 NVM PDF76–77。教學 HTML 不放報告翻頁路徑。
- 本次使用者明確指定的完整PEL節包含ET10h。只教exported/underlying物件ID映射，透過本篇 PREREQUISITE_ONLY 的 `background_terms` 記錄必要名詞；不改變Fabrics／Discovery／NQN的全域禁止，也不放寬其他報告。
- Figure233的bytes116–371保留原始佔位，但不公布被全域排除的識別欄位。Figure236、252只呈現本篇適用的PCIe／I/O／Admin資訊。

核對到的來源差異及不可重犯的錯誤：

1. Figure233將SEB bits221:16列保留，但Figure236及§.2.16定義ET10h；不自行宣稱bit16能力。正文揭露這個差異。
2. Figure247的NMCDW10交叉引用寫Figure246，實際命令欄位在Figure446。
3. Figure248的FNA來源敘述混入Identify Namespace；欄位實際在Identify Controller Figure338 byte524。
4. Telemetry事件段落引用Figure253，但TIL內容實際是Figure254。
5. Figure250的SCDW10引用Figure451，但新增namespace目標須使用Figure454。特別是PREQ在namespace命令bit4，在subsystem命令bit11；不得共用解碼。
6. Timestamp資料結構Figure480屬§5.2.30.1.8，不是其他版本的章節號。
7. LHL+20是log header大小，EHL+3是event header大小；EL已含VSIL，不能重複加。事件不保證4-byte倍數，傳輸Dword對齊與紀錄邊界分開。
8. ACT3的RCE0描述原先無context，不是建立失敗。GNUM只有新context內容不同才遞增；不把每次讀取／新增事件都說成加1。
9. NVM112是Base247的byte32／33特化；其來源位置26／29不等於事件offset。Delete All對單一namespace欄位保留，不將零值當有效設定。
10. SPROG FFFFh、Format INFO0、Firmware NFR與requested freeze均不能單獨證明成功；各自對回SOS、FNVMS、activation結果及CDPCE。
11. SMART單位與Telemetry資料區含括關係獨立教學。Base2.4的TCDA0不表示原Telemetry沒有saved state；ET0C只保存header是事件格式本身的限制。
12. PDF目錄與交叉引用不能取代正文／實際檢視器頁碼。Figure258實際在PDF295，Figure260跨295–296。

驗證：來源SHA-256、publish契約、全部單元測試、Jekyll production build、3版×3尺寸×明暗模式、逐圖目的與例子唯一性，以及push後同一commit的Validate／Pages和線上內容比對。CI沿用Ruby3.3.8與既有鎖定Bundler，不恢復不相容的Ruby3.0.7配置。
