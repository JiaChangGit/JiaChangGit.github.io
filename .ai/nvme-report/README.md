# NVMe 報告控制資料

此目錄保存來源身分、核准範圍、claim、Figure／Table coverage 與 16 個輸出的契約。
它不保存 PDF 原文。任何產生內容的工具都應先讀這個目錄，再只讀取已核准範圍。

## 執行階段

1. `setup`：驗證來源登記、四份報告、16 個輸出路徑與規則骨架。
2. `publish`：要求範圍已核准、claim 與 Figure／Table 清冊完整、16 個輸出存在且通過檢查。
3. `auto`：`scope.json` 的 `production_status` 為 `ready_for_publish` 時執行
   `publish`，否則執行 `setup`。

## 範圍規則

`scope.json` 預設為 `EXCLUDE`。使用者尚未指定的章節不得載入長上下文，也不得出現在
報告或 PPT。`interpretation_sources` 只用於解讀 keyword、優先序與頁碼，不代表該段落
自動成為報告內容。

## Claim 最小欄位

`claims.json` 中每筆 claim 至少需要：

- `id`：穩定識別字，例如 `NVME-C-0001`；
- `report_id`、`source_id`、`revision`、`section`；
- `figure`、`table`：不適用時為 `null`；
- `printed_pages`、`pdf_pages`；
- `normative_keyword`：`mandatory`、`may`、`optional`、`reserved`、`shall`、
  `should`、`none` 之一；
- `zh_tw` 與 `en`：同一技術結論的兩種語言；
- `citation_zh_tw` 與 `citation_en`：輸出中必須逐字出現的完整來源定位；
- `scope_entry_id`：對應已核准範圍。

輸出以 `<!-- claim:NVME-C-0001 -->` 或 HTML `data-claim-id="NVME-C-0001"`
標記 claim。標記可供驗證器比對；讀者看到的正文仍須有完整來源定位。

Figure／Table 使用 `<!-- figure-table:<ID> -->` 或 HTML
`data-figure-table-id="<ID>"` 標記，驗證器會核對清冊宣告的輸出是否真的介紹該項目。

## Figure／Table coverage

納入範圍內的每張 Figure 與每個 Table 都要登記在
`figure-table-register.json`。詳細 HTML 與中英文 Markdown 必須逐一介紹：

1. 目的與讀法；
2. 欄位或元件關係；
3. 重要條件與 normative keyword；
4. 一個不超出規格的例子；
5. 限制、例外與來源頁碼。

本輪四種版本都介紹每張納入的 Figure；新手 HTML 使用較白話的判讀檢查點，詳細
HTML 額外顯示 claim ID 與 normative keyword。明確排除的 Figure 只留在內部清冊，
不會進入報告或 PPT。
