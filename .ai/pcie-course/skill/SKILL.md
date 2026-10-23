---
name: pcie-spec-teaching
description: Create and revise the PCIe course in JiaChangGit.github.io using guided diagrams, connected specification reading, and natural Taiwan Traditional Chinese. Use for this course's teaching HTML and bilingual articles, with its registered PCIe sources and existing build tools.
---

# PCIe 規格教學

本 skill 用於此專案的 PCIe 系列。依當次使用者授權處理章節；本次完成 Chapter 7–9 三版本與配套 skill／腳本後停止，等待使用者確認教學方式。其他章節維持既有內容，不繼續修訂或新增。不修改其他系列。只讀要求優先於任何產生或發布步驟。

## 開始前

在課程 repository 讀取 `AGENTS.md`、`.ai/pcie-course/curriculum.json`、`source-register.json` 和目標章節的 claim 檔。Chapter 0 的檔名為 `claims.json`、`post.zh.html`、`post.en.html`，其他章節有 `chapterN` 前綴。讀者懂基本程式、CPU／記憶體及位元運算，尚未學過 PCIe。

首次撰寫或修訂時，讀 [authoring.md](references/authoring.md)。它保存使用者已對齊的圖解與中文寫法，不需要重新詢問這些偏好。

## 教學決策

- 開頭先用總覽圖定位本章，再用短段落講重點。前情只回顧本章要用的關係；沿用既有系統與角色，新增假設就近標示。
- 正常流程先走完一次，再說明相關例外。以元件、事件、等待條件串起內容；數值只在解釋欄位或流程需要時使用，仍須正確核算。
- 先給簡短的規格閱讀路線，再隨流程帶讀各 Figure／Table 的本次相關欄位。交代為什麼此時看這張、讀到什麼、如何接到下一步。直接提供閱讀位置，重點是帶讀。
- 圖種取決於問題：角色關係用拓樸，跨元件交換用時序，狀態與條件用狀態圖，等待與分支用流程圖。圖是正文的教學內容；不靠圖數或卡片數判斷完成。
- 完整圖與段落持續可見；逐步功能只強調當下的角色、箭頭與解說。點選角色可定位當下職責，基礎名詞另行展開。離線、無 JavaScript、鍵盤與列印均保留完整內容。
- 中文先明確寫主詞、動作、結果，再接原因和條件。避免用「能不能得出結論」「而不是直接假設」等抽象評論代替實際教學。必要的禁止、例外與未定義語意須保留，不做一律刪除否定詞的替換。
- 每篇、每個語言版本各自計算術語出現次數。英文 SPEC 關鍵字／縮寫前兩次都就近簡短解釋；第二次可只提醒用途。圖中首次出現者在圖旁解釋。中文後文優先使用穩定、自然的中文說法。
- 自問自答用來帶出下一步和解釋原因；中途可有短導讀，章末以完整案例串接。不要新增考試、評分、通過門檻或為測驗而挖空資訊。

## 來源與三版交付

維持 Base 6.0、Firmware 3.3 及來源登記中的版本邊界。技術主張保留來源、Section、Figure／Table、文件頁與 PDF 頁；區分規格規定、作者假設、推演與待查內容。未核對的來源不可補成肯定事實。必要時回到 PDF 表格、圖及註腳核對；來源 PDF 和擷取物不得發布。

完整繁中 HTML 提供分步教學。中英文文章保留相同主線、核心圖與代表案例，兩篇的條件與結論對等；不必複製完整教學的每段補充。保留既有網址、有效錨點、數值案例與來源定位。

## 工具與驗證

使用 repository 的 `scripts/pcie_teaching.py` 建立可維護的導圖元件；契約與 CLI 以該檔及 `scripts/validate_pcie_teaching.py --help` 為準。腳本檢查實際的圖文定位與來源關係，不能證明語句自然或讀者已學會。

1. 編輯 `.ai/pcie-course/` 的 authored 來源；不直接編輯生成頁。
2. 執行教學檢查、`build_pcie_course.py`、其 `--check`、`validate_pcie_course.py`。來源有調整時核對 PDF 與 claims；數值不變也要保留既有驗算。
3. 逐段審閱中文及三版語意，檢查圖上的箭頭、條件與正文。確認兩次術語提醒就在需要處，沒有被來源附註或頁面導航取代。
4. 執行必要測試與 Jekyll build，實際查看桌機、平板、手機及明暗模式；驗證逐步高亮、角色定位、來源展開與離線閱讀。
5. 依本次授權發布。核對同一 commit 的相關 CI 與公開頁內容；回報已完成範圍及實際執行的驗證，不宣稱取得真人學習成效。
