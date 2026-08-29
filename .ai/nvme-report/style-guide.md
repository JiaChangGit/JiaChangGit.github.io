# NVMe 報告文字與圖表風格

本文件定義四個版本共同的寫法。目標是工程內訓講義，不使用 AI 自稱或宣傳式文字。

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

## 每張規格 Figure／Table 的介紹順序

1. 這張圖或表解決什麼問題。
2. 如何閱讀各區塊、欄位、bit 或箭頭。
3. 哪些條件是 `shall`、`may`、`should` 或 `optional`。
4. 提供一個說明性範例，並標明不是新增規格要求。
5. 列出保留值、錯誤、例外、跨規格依賴與未提供來源。
6. 列 section、Figure／Table number、文件頁與 PDF 頁。

## 100 分鐘報告的暫定節奏

四份主題共用 100 分鐘時，預設保留 5 分鐘說明範圍與版本、10 分鐘建立 Base 與 PCIe
Transport 的關係、70 分鐘講四份核准主題與重點 Figure、10 分鐘整合範例、5 分鐘總結。
Markdown 與詳細 HTML 保留全部納入 Figure 作為附錄查閱；口頭報告依 Figure 索引挑選
主線，不以逐張朗讀取代說明。
