# iPad HTML 閱讀相容性規格

本規格以 11 吋 iPad Pro 第 3 代（M1）與 12.9 吋 iPad Pro 第 5 代（M1）為主要閱讀裝置。Apple 的 iPadOS 26 相容清單包含這兩個世代，因此產物採用 Safari 17.2 已具備、並在 Safari 26.x 持續改善的標準 HTML／CSS；較新的功能只能 progressive enhancement，不能成為閱讀必要條件。

## 權威相容性依據

- Apple：iPadOS 26 支援 11 吋 iPad Pro 第 3 代與 12.9 吋 iPad Pro 第 5 代：<https://support.apple.com/guide/ipad/ipad213a25b2/ipados>
- Apple UI Design：主要內容不應要求使用者縮放或整頁水平捲動；觸控目標至少 44 × 44 points：<https://developer.apple.com/design/tips/>
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
- 主內容寬度介於 760px 到 900px；portrait 與 landscape 都不得造成 page-level horizontal overflow。
- table 包在獨立的 horizontal-scroll container，並以 sticky first column／header 協助對照；表格仍須有文字標題與欄位名稱。
- inline SVG 必須 responsive，含 `<title>` 與 `<desc>`；色彩以 CSS variable 控制，並另有形狀、線型與文字標籤。
- Light／Dark Mode 使用 `prefers-color-scheme`；另外支援 `prefers-reduced-motion`、print 與 `forced-colors` 的可讀 fallback。
- sticky navigation 必須考慮 `env(safe-area-inset-top)`；anchor target 要有 `scroll-margin-top`，不能被導覽列蓋住。

## 允許的無 JavaScript 互動

- `<details><summary>`：Figure、Appendix、Glossary 與查詢卡片的展開／收合。
- 同群組 `<details name="…">`：在 Safari 17.2 以上形成互斥 accordion；舊版本忽略 `name` 時仍可正常閱讀。
- anchor navigation、`:target` highlight、橫向 scroll-snap 視覺卡片與 table swipe。
- Safari Find in Page：不得把標題、來源或關鍵字只畫進 SVG；它們仍須存在於可搜尋文字。

## 不採用的能力

- 不採用需要 JavaScript 的全文搜尋、scrollspy、theme switch、modal、canvas 或動態圖表。
- 不依賴 Safari 26 才有的 `popover` command、Grid Lanes 或 View Transition；這些不是閱讀必要條件。
- 不以 hover 顯示唯一資訊；Apple Pencil／trackpad hover 只能是附加效果。
- 不以超大 fixed sidebar 壓縮 portrait viewport，也不使用固定 viewport height。

## NVMe 教學版面最低構成

每個大主題至少包含：一張系統位置圖、一張完整流程或 sequence、一張比較表、一個具體數值或狀態範例、一個 failure／Debug 分支，以及可追溯來源。每張納入或引用的 Spec Figure／欄位表至少包含：教學重畫、縮寫、讀圖順序、欄位解碼工作紙、能回答／不能回答、例子、Debug 與 section／文件頁／PDF 頁。
