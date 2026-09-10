# NVMe 報告控制資料

此目錄保存來源身分、核准範圍、claim、Figure／Table coverage 與 39 個輸出的契約。
它不保存 PDF 原文。一般重建只讀取此目錄中的追蹤資料，不需要 PDF，也不會把規格原文
帶進 GitHub Pages。

## 唯一資料來源與重建流程

- `scope.json`：13 份報告與排除範圍的唯一資料來源；主題與必要背景都需來源登記。
- `figure-table-register.json`：Figure 編號、標題、頁碼、範圍狀態與精簡證據索引的唯一資料來源。報告若在 `scope.json` 宣告 `included_figure_ids`，該 allowlist 是實際發布集合；清冊中其他舊證據列只供追溯，不得出現在輸出。
- `claims.json`：由產生器重建；不手動維護。
- `output-contract.json`：39 個輸出路徑與格式要求。

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

1. `setup`：驗證來源登記、13 份報告、39 個輸出路徑與規則骨架。
2. `publish`：要求範圍已核准、claim 與 Figure／Table 清冊完整、39 個輸出存在且通過檢查。
3. `auto`：`scope.json` 的 `production_status` 為 `ready_for_publish` 時執行
   `publish`，否則執行 `setup`。

## 範圍規則

`scope.json` 預設為 `EXCLUDE`。教學必要背景可以補充，需記錄來源及用途；不因補充自動納入整章。`interpretation_sources` 只用於解讀 keyword、優先序與頁碼，不代表該段落
自動成為報告內容。

## Claim 最小欄位

`claims.json` 中每筆 claim 至少需要：

- `id`：穩定識別字，例如 `NVME-C-0001`；
- `report_id`、`source_id`、`revision`、`section`；
- `figure`、`table`：不適用時為 `null`；
- `printed_pages`、`pdf_pages`；
- `normative_keyword`：`mandatory`、`may`、`optional`、`reserved`、`shall`、
  `shall not`、`should`、`should not`、`none` 之一；
- `zh_tw` 與 `en`：同一技術結論的兩種語言；
- `citation_zh_tw` 與 `citation_en`：輸出中必須逐字出現的完整來源定位；
- `scope_entry_id`：對應已核准範圍。

輸出以 `<!-- claim:NVME-C-0001 -->` 或 HTML `data-claim-id="NVME-C-0001"`
標記 claim。標記可供驗證器比對；讀者看到的正文仍須有完整來源定位。

Figure／Table 使用 `<!-- figure-table:<ID> -->` 或 HTML
`data-figure-table-id="<ID>"` 標記，驗證器會核對清冊宣告的輸出是否真的介紹該項目。

## 教學與覆蓋

每篇只發布中文教學 HTML、中文 post、英文 post。教學 HTML 由淺入深；post 用全局觀念、流程及代表案例銜接 Spec，中英文對等。主題總覽在正文前，知識鞏固在結尾。每一筆已核准結論只呈現一次，Figure 文字說明放在相關主題下；圖表按教學需要選用，不再每張 Figure 配一套固定工作紙。

`nvme_reader.py` 負責閱讀結構，`nvme_reader_context.py` 保存各篇開頭與主軸，`nvme_reader_visuals.py` 提供有具體對象的教學圖，`nvme_review_bank.py` 保存成對問答。共用視覺來源是 `assets/css/nvme-reader.css`，獨立 HTML 內嵌同份 CSS。

先更新最新主題：

```text
python3 -B scripts/build_nvme_reports.py --reports nvm-command-set-1.3 base-boot-partitions base-telemetry base-sanitize
```

全部重建不傳參數，產生順序也是新篇優先。完成全量產出後才執行 publish 驗證與提交。除 Fabrics／Discovery／NQN 外，範圍外背景（含原排除主題）可在理解主題所需時加入，需登記具體必要性及來源，不自動擴張全部章節。


2026-09-11：中文 HTML 完整介紹每張範圍內圖表；中英文 Pages 使用全局主軸、流程及代表案例，並銜接 Spec。Fabrics 永久排除，包括必要背景。新圖表內容在 nvme_figure_examples_base.py、nvme_figure_examples_nvm.py、nvme_figure_examples_pcie.py；缺少逐圖重點或案例會阻止發布。舊合輯只在 _pages 保留原網址的新篇導覽，不再出現在文章清單。
