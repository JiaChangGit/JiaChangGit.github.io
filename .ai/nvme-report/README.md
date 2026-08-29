# NVMe 報告控制資料

此目錄保存來源身分、核准範圍、claim、Figure／Table coverage 與 16 個輸出的契約。
它不保存 PDF 原文。一般重建只讀取此目錄中的追蹤資料，不需要 PDF，也不會把規格原文
帶進 GitHub Pages。

## 唯一資料來源與重建流程

- `scope.json`：四份報告與排除範圍的唯一資料來源；未列入 `INCLUDE` 的內容一律不發佈。
- `figure-table-register.json`：Figure 編號、標題、頁碼、範圍狀態與精簡證據索引的唯一資料來源。
- `claims.json`：由產生器重建；不手動維護。
- `output-contract.json`：16 個輸出路徑與格式要求。

一般內容更新後，依序執行：

```text
python3 -B scripts/build_nvme_reports.py
python3 -B scripts/validate_nvme_report.py --phase publish
python3 -B -m unittest discover -s tests -v
```

產生器是 deterministic：輸入未改變時，連續執行不應產生 Git diff。GitHub Actions 也會
重建成品並以 `git diff --exit-code` 檢查是否忘記提交衍生檔。

## 從本機 PDF 更新 Figure 證據

只有來源 PDF 或納入範圍改變時才需要執行此段。PDF 必須留在 Git 之外：

```text
python3 -m pip install -r requirements-nvme-report.txt
python3 -B scripts/extract_nvme_source_text.py --source-dir <PDF 所在目錄>
python3 -B scripts/update_nvme_figure_evidence.py
python3 -B scripts/build_nvme_reports.py
```

擷取文字寫入已忽略的 `tmp/pdfs/nvme-report/`。`update_nvme_figure_evidence.py` 只把
`key_items`、`source_keywords` 與 `evidence_digest` 寫回追蹤清冊，不保存規格段落。
`source_keywords` 表示該 Figure 附近來源區塊出現哪些規範性關鍵字，只能作為查核索引，
不能脫離原條件直接解讀成對整張 Figure 的要求。

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

驗證器還會核對 claim 的完整正文與順序，而不只檢查隱藏標記；中英文 Markdown 必須
具有相同 claim 集合與排列。輸出不得出現 Fabrics、message-based transport、Discovery
controller、capsule 或 NQN 等本輪排除主題，也不得留下「待補」式佔位文字。
