# 編輯與工具

Repository 的 `.ai/spec-teaching/scope.json` 限定可處理的文章，任何新篇先建立來源與涵蓋登記。腳本位於 `scripts/`，以各自的 `--help` 查看參數。下載包的 `USAGE.md` 與 `project-snapshot/` 保存該版工具、authored 來源及資料快照；它不是整個 Jekyll 網站。

## 編輯入口

- PCIe：`.ai/pcie-course/curriculum.json`、各章 authored HTML、claim、`walks/` 與來源登記。Chapter 0 post 檔名沒有 chapter0 前綴。以 `build_pcie_course.py` 產生三版；`pcie_teaching.py` 更新逐步圖的 authored 區塊。
- NVMe 自問自答：`scripts/nvme_qa_*.py` 保存題目、教學、案例、呈現與來源，`build_nvme_question_bank.py` 整合三版。保留 Q1–Q328，不恢復固定 17 項回答模板。
- NVMe 圖表情境：`nvme_quickref_*.py`、`nvme_scenarios*.py`、`nvme_scenario_render.py`，由 `build_nvme_quickref.py` 整合。117 張圖及 45 個情境維持原本固定位置。
- 兩篇 NVMe 專篇：由 `.ai/nvme-report/output-contract.json` 中的 `pcie-transport-1.4`、`nvm-command-set-1.3` 定位三版。使用 `build_nvme_reports.py --reports pcie-transport-1.4 nvm-command-set-1.3` 限定輸出，保留其他專篇、共用 claims 與 landing page；相關索引的必要文字另外維護。

`spec_terms.py` 在 PCIe、NVMe 題庫與圖表系列的前兩次使用處插入可見說明；兩篇專篇沿用 `nvme_reader.py` 的上下文名詞處理。歧義縮寫、欄位全名與正文因果仍須人工校閱。必要時在 authored 來源中直接解釋，避免將多種含義硬塞進同一個字典。

## 原始依據

PCIe 來源與 claim 位於 `.ai/pcie-course/`；NVMe 在 `.ai/nvme-report/source-register.json`、`.ai/nvme-question-bank/`、`.ai/nvme-quickref/`。依登記的 PDF 版本核對。新增或變更來源回到原 PDF 檢查圖、表、註腳及完整條件，不只比較文字快取。

`extract_spec_outline.py` 產生的項目一律為待核對。已有 claim 命中某章節，也不等於完整教過該章節。建立全規格對照表後，逐項記錄教學位置、涵蓋深度與待補內容。

## 驗證

先跑 scoped inventory 和各 builder 的 `--check`；來源、算例與雙語依原有檢查核對。`run_project_checks.py` 只執行只讀檢查，省略會改寫其他 NVMe 報告的主 builder。

`validate_pcie_examples.py` 重算新增進階章的作者算例，檢查三版的可見數值；它不確認假設是否符合實際裝置。專篇若變更了 claim 的呈現文字，應在隔離副本用完整 builder 核對相應登記，並比對範圍外產物，不能直接把其他報告重建差異納入本輪。

`audit_spec_teaching.py` 只讀頁面，列出預設收合的主解說、來源名稱疑義及其他需人工查看的地方。它不自動改寫文字、不給學習分數，也不把單字出現視為已解釋。`validate_public_teaching.py` 檢查公開檔案邊界、主要教材的本機路徑與離線主動內容；Jekyll 建置後加 `--site-dir` 核對輸出。

實際校閱中文與三版語意，檢查圖的箭頭、條件和下一步。瀏覽器檢查涵蓋桌機、平板、手機、明暗、鍵盤、無 JavaScript、列印與跨頁定位。完成後，依當次授權提交及發布，核對同一 commit 的相關 CI 與公開內容。

以 `package_spec_teaching_toolkit.py --destination <儲存庫外新目錄> --output <儲存庫外新ZIP>` 建立下載包，再用 `verify_teaching_bundle.py --zip <ZIP>` 核對 manifest。封裝不會覆寫既有包、安裝 skill 或發布；來源 PDF、擷取全文、私密資料及 QA 產物不納入。
