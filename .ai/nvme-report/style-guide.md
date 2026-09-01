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

## iPad HTML

- 使用短段落、窄表格、`nav`、`main`、`section`、`figure`、`figcaption`、`details` 等語意標籤。
- 不使用 CSS、JavaScript、外部字型或外部資源；文件在瀏覽器預設樣式下仍須具備清楚層級。
- 每張 Figure 以 `details` 收合，並提供依章節分組的 Figure 索引與返回連結，避免長頁面迷航。
- 每張表格以四欄內為原則。欄位過多時拆成「欄位定義」「條件」「例子」多張表。
- Unicode 圖示只用於固定語意：`[必須]`、`[允許]`、`[建議]`、`[注意]`，不作裝飾。
- inline SVG 必須有 `title`／`desc` 或等效替代文字，並在圖說列出來源 claim。

## Figure／Table 作為支援證據

主教學先依「問題、Mental Model、流程、欄位、範例、錯誤與 Debug」組織。Figure／Table
放在首次支援該概念的位置，或集中於 Detailed Reference／Appendix；不得以 Figure 順序取代
教學故事線。每筆 Figure／Table reference 仍須說明用途、讀法、適用的 normative keyword、
限制及來源 section／頁碼。

第五份 firmware update 報告參考 Claude Code 工程文件的資訊設計：Hero／scope、Mental
Model、PART 層級、固定語意標記、bit-field、sequence、decision flow、章末統整與 Appendix。
由於離線 HTML 絕對禁止 CSS／JavaScript，視覺呈現改用語意 HTML、`details`、anchor、
四欄內 table 與單色 `currentColor` inline SVG；不模擬固定側欄、搜尋、scrollspy 或 theme
button。

## 100 分鐘報告的暫定節奏

五份主題共用 100 分鐘時，預設保留 5 分鐘說明範圍與版本、10 分鐘建立 Base 與 PCIe
Transport 的關係、70 分鐘講五份核准主題與重點 Figure、10 分鐘整合範例、5 分鐘總結。
Markdown 與詳細 HTML 保留全部納入 Figure 作為附錄查閱；口頭報告依 Figure 索引挑選
主線，不以逐張朗讀取代說明。
