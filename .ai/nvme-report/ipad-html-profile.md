# iPad／Desktop Responsive HTML 閱讀相容性規格

本規格以 11 吋 iPad Pro 第 3 代（M1）與 12.9 吋 iPad Pro 第 5 代（M1）為主要閱讀裝置，同時支援一般 desktop browser。Apple 的 iPadOS 26 相容清單包含這兩個世代，因此產物採用 Safari 17.2 已具備、並在 Safari 26.x 持續改善的標準 HTML／CSS；較新的功能只能 progressive enhancement，不能成為閱讀必要條件。每篇只維護一份由淺入深的 responsive 中文教學 HTML，不建立 iPad／desktop 內容副本。

## 權威相容性依據

- Apple：iPadOS 26 支援 11 吋 iPad Pro 第 3 代與 12.9 吋 iPad Pro 第 5 代：<https://support.apple.com/guide/ipad/ipad213a25b2/ipados>
- Apple UI Design：主要內容不應要求使用者縮放或整頁水平捲動；觸控目標至少 44 × 44 points：<https://developer.apple.com/design/tips/>
- Apple Accessibility：介面不可只靠顏色傳達資訊，文字需支援放大且控制項要有足夠 hit target：<https://developer.apple.com/design/human-interface-guidelines/accessibility>
- Apple Color：顏色應維持一致語意並同時在 Light／Dark appearance 保有可讀對比：<https://developer.apple.com/design/human-interface-guidelines/color>
- MDN Responsive Design：以 flexible grid、media query 與 responsive media 讓同一內容適應不同 viewport：<https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design>
- W3C WCAG 2.2 Use of Color：顏色不得是傳達狀態與操作意義的唯一視覺手段：<https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html>
- WebKit Safari 15：支援依 `prefers-color-scheme` 指定 light／dark `theme-color`：<https://webkit.org/blog/11989/new-webkit-features-in-safari-15/>
- WebKit Safari 17.2：`details` 的 `name` attribute 可建立無 JavaScript 的互斥 accordion：<https://webkit.org/blog/14787/webkit-features-in-safari-17-2/>
- WebKit Safari 18.4：改善 `details`／`summary` 的語意與輔助技術支援：<https://webkit.org/blog/16574/webkit-features-in-safari-18-4/>
- WebKit Safari 26.2：Find in Page 可自動展開命中內容所在的 closed `details`：<https://webkit.org/blog/17640/webkit-features-for-safari-26-2/>

## 必須使用的閱讀能力

- UTF-8、`lang="zh-Hant-TW"`、`viewport-fit=cover` 與 `width=device-width`。
- 一份內嵌 stylesheet；禁止 JavaScript、外部 stylesheet、外部字型、`iframe`、`object` 與 `embed`。
- `nav`、`main`、`section`、`article`、`aside`、`figure`、`figcaption`、`details`、`summary` 等語意結構。
- 至少一個 skip link；鍵盤焦點使用 `:focus-visible`，不能移除 outline。
- 所有可點擊的 anchor 與 `summary` 觸控高度至少 44px。
- 正文字級至少 16px、預設 17px，line-height 至少 1.65；使用系統字型並設定 `-webkit-text-size-adjust: 100%`。
- iPad 主內容寬度介於 760px 到 900px；desktop 可放寬至 1180px，長段落仍限制約 80 字元。portrait、landscape 與 desktop 都不得造成 page-level horizontal overflow。
- table 包在獨立的 horizontal-scroll container，並以 sticky first column／header 協助對照；表格仍須有文字標題與欄位名稱。
- inline SVG 必須 responsive，含 `<title>` 與 `<desc>`；色彩以 CSS variable 控制，並另有形狀、線型與文字標籤。
- Light／Dark Mode 使用 `prefers-color-scheme`；另外支援 `prefers-reduced-motion`、print 與 `forced-colors` 的可讀 fallback。
- sticky navigation 必須考慮 `env(safe-area-inset-top)`；anchor target 要有 `scroll-margin-top`，不能被導覽列蓋住。
- 11 吋 iPad portrait／landscape 使用單欄正文；viewport 達 1200px 的 desktop 可加側邊目錄或較寬的圖表，長段落仍維持易讀寬度。

## 允許的無 JavaScript 互動

- `<details><summary>`：完整來源、必要延伸解釋與結尾答案的展開／收合。名詞定義放在首次出現段落下方，不以收合術語總表代替。
- 同群組 `<details name="…">`：在 Safari 17.2 以上形成互斥 accordion；舊版本忽略 `name` 時仍可正常閱讀。
- anchor navigation、`:target` highlight 與無法再拆分的 table swipe；Visual Atlas 不使用橫向 carousel。
- Safari Find in Page：不得把標題、來源或關鍵字只畫進 SVG；它們仍須存在於可搜尋文字。

## 不採用的能力

- 不採用需要 JavaScript 的全文搜尋、scrollspy、theme switch、modal、canvas 或動態圖表。
- 不依賴 Safari 26 才有的 `popover` command、Grid Lanes 或 View Transition；這些不是閱讀必要條件。
- 不以 hover 顯示唯一資訊；Apple Pencil／trackpad hover 只能是附加效果。
- 不以超大 fixed sidebar 壓縮 portrait viewport，也不使用固定 viewport height。

## NVMe 教學版面

開頭先說主題、重要性與主軸，以適合的總覽圖或表協助建立關係；正文依讀者理解順序由淺入深；結尾用少量不同概念的問題及答案鞏固知識。每篇均能單獨閱讀。

參考使用者提供的 2 份 HTML，以清楚層級、留白、藍／青綠重點、欄位圖、狀態圖、範圍關係與比較表表達。只在圖表能補足理解時使用；不強制固定圖種，不要求每張規格 Figure 重畫、工作紙、例子及 Debug 分支。

名詞及縮寫在首次出現的段落下方說明，圖中首次出現者就在圖下說明。數字、位元範圍、編碼與單位維持原樣。圖的節點直接標實際元件／欄位／狀態；不需要額外印出製圖角色或無對象的 Locate／Decode。

短來源放在相關內容附近，完整 citation 可以收合。claim ID、製作流程及檢查記錄只放 HTML 註解或內部文件，不顯示在正文。

## 圖表可讀性

藍與青綠為主要重點色，其他色彩少量區分條件或例外。顏色、形狀、線型與文字一起表達含義，不依賴顏色辨識。圖中需說明元件關係、箭頭方向及轉換條件；connector 避開文字與節點。

欄位圖保留 bit／byte 範圍、offset 與 reserved gap；若圖形比例經簡化，明確標註範圍，不暗示錯誤的大小比例。比較表說明真正差異，數值例子呈現輸入、推算與結果，不與正文整段重複。
