# NVMe 報告文字與圖表風格

本文件定義每份報告四個版本共同的寫法。目標是工程內訓講義，不使用 AI 自稱或宣傳式文字。

## 中文

- 使用台灣繁體中文；第一次出現的關鍵詞補英文，例如「提交佇列（Submission Queue, SQ）」。
- 先寫結論或適用條件，再說原因、流程與例子。
- 主詞要明確區分 host、controller、NVM subsystem、namespace 與 PCIe Function。
- `shall`、`may`、`should` 不得互換；詳細版保留英文 keyword。
- 避免「讓我們」「其實很簡單」「輕鬆理解」「值得注意的是」等無資訊量開場。
- 不使用「身為 AI」「我認為」「以下為您整理」等工具口吻。

## English

- Use the same claim IDs, scope, ordering, figures, tables, examples, and caveats as the Chinese Markdown.
- Preserve NVMe normative keywords verbatim. Do not strengthen `may` or `should` into `shall`.
- Translate the verified claim, not the Chinese sentence structure.
- Prefer direct technical prose with an explicit subject and condition.

## iPad／Desktop Responsive HTML

- 裝置、Safari baseline、觸控與 accessibility 的硬性條件見 `ipad-html-profile.md`。
- 使用短段落、窄表格、`nav`、`main`、`section`、`figure`、`figcaption`、`details` 等語意標籤。
- 允許單一內嵌 CSS；不使用 JavaScript、外部 stylesheet、外部字型或外部資源。CSS 必須同時支援 iPad／desktop、`prefers-color-scheme` Light／Dark Mode 與列印。
- 每個用途只維護一份 responsive HTML：同一檔在 11 吋 iPad portrait／landscape 採單欄閱讀，viewport 達 1200px 的 desktop 才放寬至約 1180px 並使用兩欄 Visual Atlas。不得為裝置另製內容副本。
- iPad 正文寬度維持約 760～900px；desktop 可放寬視覺索引，但自然段落維持最多約 80 字元寬。table 外層可獨立水平捲動，不得讓整頁 overflow。
- 建立固定視覺語意：SPEC=藍、解釋=青綠、推論=紫、範例=綠、注意／錯誤=橘紅；同時保留文字標籤，不能只靠顏色傳達資訊。
- 每張 Figure 以 `details` 收合，並提供依章節分組的 Figure 索引與返回連結，避免長頁面迷航。
- 每張表格以四欄內為原則。欄位過多時拆成「欄位定義」「條件」「例子」多張表。
- Unicode 圖示只用於固定語意：`[必須]`、`[允許]`、`[建議]`、`[注意]`，不作裝飾。
- inline SVG 必須有 `title`／`desc` 或等效替代文字，並在圖說列出來源 claim。
- 圖示依問題選型：Architecture 說明元件位置、Sequence 說明 actor 交握、State Machine 說明狀態轉移、Decision Flow 說明 failure branch、Bit-field／Memory Layout 說明 offset 與位元。不可用同一種直線流程圖代替全部關係。
- 每個 learning module 至少同時提供「主流程視圖」與「驗證／失敗視圖」；每張 Figure card 要有一張簡化教學視圖，以及 Input／Decode／Validate／Evidence 工作紙。
- Visual Atlas 在 iPad 採垂直單欄，避免卡片只露出一半；desktop 才排成雙欄。所有重要內容保留為可搜尋文字。
- Requirement 顏色另行區分：`shall`／`shall not`=紅、`should`=黃、`may`=藍灰、`reserved`=灰；每一種仍顯示文字 badge。

### 固定圖形與色彩語法

所有報告使用同一組「角色」而非每頁自行選色：藍色圓角矩形是 Request／Input，青綠色圓角矩形是 Object／State，紫色 gate 是 Rule／Decision，綠色雙框是 Valid／Evidence，橘色虛線框是 Warning／Failure。每個節點仍須印出角色文字；黑灰實線只表示正常資料流，橘色虛線只表示 failure／recovery，不能單靠顏色辨識。

- Architecture／Dependency：採上到下的 parent → bus → children 佈局；connector 先畫、node 後畫，線不得穿越文字或其他 node。
- Sequence／Ownership：actor header 與 lifeline 分離，訊息箭頭位於 lane 之間，訊息標籤有不透明背景。
- State／Failure：狀態沿時間軸排列，正常轉移用灰色實線，failure／timeout loop 用橘色虛線且與正常路徑分開。
- Decode／Memory Layout：保持 bit／byte 比例、offset 與 reserved gap；reserved 必須同時有 `R`／`Reserved` 文字和虛線外框。
- 流程圖只回答先後順序；比較用 table；具體數值以 example box 呈現。不可用同一種直線節點圖假裝 Architecture、State 與 Decode。

### 四種交付用途

- 新手 HTML：從縮寫、Mental Model、完整流程、具體例子、常見誤解到 Debug；Spec Figure 以「怎麼讀」為主。
- 詳細 HTML：以機制索引、normative keyword、欄位 boundary、Input／Decode／Validate／Evidence 與症狀索引為主，不重複教學故事。
- 中文／英文 Markdown：是 PPT 腳本；兩版 slide 順序、claim ID、Figure、例子與 caveat 完全一致，只改語言。
- 四種版本共同保留可追溯來源、正確專有名詞、規範性強度與非 AI 口吻；不得為追求版面而刪除必要 dependency slice。

## Figure／Table 作為支援證據

主教學先依「問題、Mental Model、流程、欄位、範例、錯誤與 Debug」組織。Figure／Table
放在首次支援該概念的位置，或集中於 Detailed Reference／Appendix；不得以 Figure 順序取代
教學故事線。每筆 Figure／Table reference 仍須說明用途、讀法、適用的 normative keyword、
限制及來源 section／頁碼。

七份報告都參考 Claude Code 工程文件的資訊設計：Hero／scope、Mental
Model、PART 層級、固定語意標記、bit-field、sequence、decision flow、章末統整與 Appendix。
離線 HTML 以內嵌 CSS、語意 HTML、`details`、anchor、四欄內 table 與 inline SVG 呈現；
仍不使用 JavaScript，不模擬搜尋、scrollspy 或 theme button。

## 100 分鐘報告的暫定節奏

七份主題共用 100 分鐘時，預設保留 5 分鐘說明範圍與版本、10 分鐘建立 Base 與 PCIe
Transport 的關係、70 分鐘講七份核准主題與重點 Figure、10 分鐘整合範例、5 分鐘總結。
Markdown 與詳細 HTML 保留全部納入 Figure 作為附錄查閱；口頭報告依 Figure 索引挑選
主線，不以逐張朗讀取代說明。
