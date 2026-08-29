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

在範圍核准後再分配實際章節。預設保留 5 分鐘說明範圍與版本、10 分鐘建立三份
規格的關係、70 分鐘講核准主題與 Figure／Table、10 分鐘整合範例、5 分鐘總結。

