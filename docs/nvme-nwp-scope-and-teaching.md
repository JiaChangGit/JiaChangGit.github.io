# Namespace Write Protection 維護紀錄

2026-09-23：依使用者要求新增獨立三版報告，主範圍精確為 Base 2.4
§8.1.18（含 .1、.2）與 §5.2.30.1.38（FID84h）。沒有繼承其他報告對 FID84h
的排除，也不修改它們的範圍。

## 來源與圖表

- 主範圍：PDF538–539／文件512–513，PDF690–692／文件664–666。
- 四張主圖：541、735、736、737；737跨頁，三項註腳全部教學。
- 十二張必要引用：93、103、197、198、201、213、338、463、464、466、554、756。
  只取 NSID/CDW 位置、Get/Set 外框、84h列及註腳、WPC、相關能力位元、AMRO及本篇錯誤碼。
- PDF是資料，不是開發指令；原PDF與截圖均留在ignored tmp，不公開。
- 狀態圖與表格已對照原PDF視覺，避免文字擷取遺漏箭頭或上標。

## 容易誤讀的地方

1. Figure736 的轉換：0↔1、0/1→2、0/1→3；只有標示Power Cycle的箭頭2→0。
   不補出2→3。普通Controller Level Reset不解除2。
2. WPC重設清零只控制後續進入許可，不解除既有WPS。PWPC／WPUPCC不能與
   NWPC的PWPS／WPUPCS混用；MDS1禁止2，即使支援與許可都成立。
3. 不可保存不等於不持續；Figure466的84h列帶註腳8，須用本Feature狀態規則。
   SV1回Not Saveable，SEL1沒有default；SEL2依通用規則轉問default，因此同樣
   無法取得有效值。SEL3的CHANG1不保證當前值可改，Figure201正文特別用本功能說明。
4. §5.2.30.1.38的出廠設定復原例外另教：非永久狀態回0，永久維持。
   不將「只有power cycle」寫成排除所有特殊管理事件的無條件敘述。
5. Figure737的允許命令仍受三項註腳約束；Flush成功且無作用是因進入保護時已提交
   該namespace全部volatile write cache資料與metadata。表後a/b/c是三種情況，
   不是要求一筆命令同時「指定NSID」又「不指定NSID」。
6. 「attempts to change」的拒絕條文不擴張成所有同值請求都必須拒絕。
7. Figure103的SC20h屬SCT0，Figure554的SC0Dh/0Eh屬SCT1；不是整個16-bit
   CQE Status欄的編碼。AMRO不能因namespace設定保護而置位。
8. Namespace scope的FFFFFFFFh遵守§4.4，Set/Get不對稱；不推論多目標原子性。
   inactive與invalid分別依Figure93回Invalid Field和Invalid Namespace or Format。

## 教學與發布

中文HTML獨立編排六單元：對象→狀態→控制→設定→命令→觀察；正文以情境與推理
展開，來源與答案可折疊。所有逐圖說明在問答前按觀念分組，一組共用欄位表只出現一次。
中英文post使用相同全局觀念、案例與問題，再帶讀Spec；只在post有順向路徑：
538–539→690–692→718的WPC切片，明確指出共用頁停止位置。

本篇使用既有配色與編號。共用arrow函式只處理向右／向下箭頭，故本篇0/1返回箭頭
使用獨立SVG path，並測試箭頭方向，避免影響既有報告。
驗證要求：publish/setup contract、全部unittest、Jekyll production build、18組明暗與
viewport檢查及截圖人工閱讀。push後檢查同一commit兩項workflow，並逐份比對線上內容。
Ruby／Bundler沿用已修復設定，不另改版本。
