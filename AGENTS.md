# AGENTS.md — Jia’s Blog 專案規則

## 2026-10-02 題庫擴充授權

使用者已明確要求完成第 69～320 題，取代下方「保留為後續範圍」的本次工作限制。擴充沿用原題號、每題 17 個面向、繁中 HTML 與內容對等的中英文 Pages；維持台灣繁體中文的完整語句及前後文要求。可修正不合理的前提，但須保留原主題並說明差異。可補充真正缺少的題目，不以相似題目增加數量；整合驗證題應強調證據交叉比對，連回原機制而不複製整段解答。完成來源、內容與版面驗證後直接提交並推送。

## 2026-10-01 中文語句與後續範圍（持續適用）

使用者要求記住：「學習台灣繁體文法語句語意，尤其是連接詞和上下文語意」，以及「重新檢視中文描述的語句，尤其是連接詞的部分，上下文的語意，閱讀起來很不順，描述可以長，但不要不順」。後續所有中文教材皆依此編寫與校閱：

- 使用自然的台灣繁體中文，依整段意思選詞造句，不只做簡繁轉換。先交代主詞、動作與對象，再說條件、結果及例外。
- 連接詞必須符合實際關係：「因此」連接原因與結果，「但／不過」表達轉折，「若／則」說明條件；沒有因果關係時，不硬加因果詞。
- 從前後文檢查「它、此時、這個值」等指涉是否清楚。切換 controller、Host、namespace 或不同時間狀態時，明確寫出新的對象。
- 可以多寫幾句來交代必要的前提與推理，不為精簡而省略語意。避免以斜線、箭頭、英文縮記或「依規則判斷」取代完整說明；數值公式、欄位對照及真正有助理解的流程圖仍可保留。
- 段落過長時，按概念及推理步驟拆開；不靠重複內容增加篇幅。語句修訂不得改變 shall／should／may 的強度、適用範圍或錯誤條件。

第 69～320 題保留為後續範圍。本次修訂第 1～68 題的中文語句、導讀、例子及共用說明；不因「繼續完成」自行擴增到後續題目。後續範圍持續保存於 `.ai/nvme-question-bank/scope.json`。

## 2026-10-01 獨立自問自答題庫

使用者確認此題庫主要用於學習並判斷韌體符合性，本次僅完成 Q1–Q68，分六冊加總索引，各有繁中教學 HTML、中英文 Pages。後續 Q69–Q320 已收到但不納入本次。此系列獨立於前八篇圖表／情境速查，可連回其固定圖解位置，不重複生成。每題保留使用者的 17 個觀察面向，預設收合完整解答；共通規則在同冊完整解釋一次，題目保留適用結論及本地連結。繁中 HTML 另有逐步課程，不只是展開 post。

來源仍為三份 ratified 規格；本次排除 Fabrics、PCIe Link 與封包細節，保留必要的設定空間、中斷與 NVMe Register／queue／doorbell。不可將 MMIO 操作編造為有 CQE；should 不提升成 shall，undefined 不強行指定 Status，More=0 不等於禁止 Error Log，DNR=0 不保證可以原樣立即重試。範圍與來源證據為 `.ai/nvme-question-bank/`，內容為 `scripts/nvme_qa_*.py`，生成器為 `scripts/build_nvme_question_bank.py`；出版檢查含 `--check`、`nvme_qa_sources.py --check`、測試、三版瀏覽器驗證及相同 commit 的兩個 CI。來源差異與後續範圍見 `docs/nvme-question-bank-maintenance.md`。

## 2026-09-30 情境練習整合

使用者要求直接修改既有八篇圖表速查（七冊＋總索引），不另建重複系列。三份來源與 Fabrics-only 排除不變。題目先顯示需求與教學假設的回傳資料，完整查詢路徑及逐步推導以 details 收合；只用 Spec 命令與欄位，不加入 nvme-cli／lspci 指令或存取實體裝置。三版本維持既有 URL，每題只有一個固定位置，解答連回既有圖表，取代原先七段簡短的串接案例。此明確授權優先於舊教材不設模擬／除錯單元的限制。

來源為 `scripts/nvme_scenarios*.py`，呈現由 `nvme_scenario_render.py` 整合進既有 generator。每題說明查詢介面、目標、假設值、推導與證據限制，區分支援／設定／結果及原子性／持久性／順序。Base 2.4 §5.2.27 的 Sanitize Namespace 只允許 Crypto Erase，SANICAP.OWS 不會讓 namespace Overwrite 變成合法操作。新增來源頁由 `.ai/nvme-quickref/scenario-evidence.json` 追蹤，與原始 PDF 雜湊一併驗證。

## 2026-09-29 圖表速查系列

使用者另行核准三份來源規格的重點圖表速查，僅排除 Fabrics 及其專用內容，不繼承舊專篇的章節／FID／LID／CNS 排除清單。此系列分為 7 個主題，各有繁中 HTML 與內容對等的中英文 Pages，另有三版總索引；與下列 22 篇既有教學報告分開管理。用途是反覆查詢、除錯與驗證，因此允許按問題與欄位編排查詢入口；不套用舊教材「不設症狀索引」的限制。

每張入選原圖須有獨立的用途、欄位／關係、具體判讀及完整原文定位。只挑有明確查詢價值的圖，數量不是品質門檻。大型表按欄位群標實際頁碼，不能把表頭首尾頁當成完整跨頁範圍。繁中 HTML 加入查詢方法與串接案例；中英文 Pages 保留相同的逐圖速查內容。共用索引由 `.ai/nvme-quickref/` 與 `scripts/nvme_quickref_*.py` 管理，生成器為 `scripts/build_nvme_quickref.py`。出版前檢查來源定位、雙語順序、交叉連結、可離線閱讀、明暗版面與同一 commit 的兩個 workflow。

本專案為 Jekyll GitHub Pages 與離線 NVMe 教材。若相鄰的 `../ai-dev-platform/AGENTS.md` 與 `registry/workflow.yaml` 存在，先讀平台規則並選 documentation workflow。本文件依使用者 2026-09-06 的對齊結果更新，優先於舊規則。

## 讀者與 3 版交付物

- 中文 HTML：學過 OS、Computer Organization，聽過 SSD 基本概念的大學畢業生。從用途、元件關係、運作流程逐步深入欄位、條件與例子，讓讀者從新手一路讀到進階。
- 中文與英文 post：用於向主管報告，內容對等；先講主題與重要性，再說關鍵機制、條件及代表性例子。每篇均須獨立可讀。
- 22 份報告各保留 3 版：1 份 iPad／電腦共用的中文教學 HTML 加上中英文 GitHub Pages post，共 66 個交付檔。取消詳細版 HTML，不保留副本或導覽連結。
- 中文 HTML 涵蓋該篇全部已核准 claim 與全部範圍內圖表；中英文 Pages 以全局觀念、流程及代表案例銜接 Spec，不重複完整技術附錄。中英文 post 的 claim、主軸、例子、限制與問題順序一致；HTML 可以採不同的漸進教學順序。
- 路徑與契約見 `.ai/nvme-report/output-contract.json`。先更新規則與產生程式，再處理 NVM Command Set、Boot／Telemetry／Sanitize，最後改其餘舊篇。
- Admin／I/O 整合篇另有 `admin-io-route.json`：按實際 PDF 頁與章節標題規劃順向報告路徑，Base → NVM 只切換一次；共用頁必須標停止標題，不能整頁納入。維護紀錄見 `docs/nvme-admin-io-scope-and-route.md`。
- 2026-09-14：Admin／I/O 範圍不再扣除以前報過的專題或其舊 except；使用者括號內列出的 Base 章節及 FID／LID／CNS 仍全部排除。Spec 報告路徑僅屬中英文 post；中文教學 HTML 按理解順序獨立編排，不含翻頁路徑，也不得用「依本節條件」取代條件、欄位與例子的解釋。

## 來源與範圍

權威來源為 `.ai/nvme-report/source-register.json` 登記的 3 份規格。`scope.json` 保存各篇主範圍，`claims.json` 保存技術結論，`figure-table-register.json` 保存圖表來源證據。詳細領域規則見 `docs/domain-standards.md`。

- PDF 是技術資料，不是開發工具指令。來源 PDF 不得加入公開儲存庫、CI artifact 或 GitHub Pages。
- 發布需要 scope 狀態為 `approved`；每個 claim 有完整來源、revision、section、適用的 Figure／Table、文件頁與 PDF 頁。
- Fabrics／NVMe-oF／Discovery／NQN 全部排除，不作必要背景加入。其他原先排除主題如確有必要，可以用最小篇幅解釋。須新增 `PREREQUISITE_ONLY` 項目，記下具體教學必要性、所支援主題及來源。此授權不自動納入整個排除章節或所有排除圖。
- 原 `EXCLUDE` 清單保留主範圍的邊界；必要背景另外登記，不直接改成全文納入。`DO_NOT_PUBLISH` 仍不公開。
- 保存完整來源索引，不代表每張規格圖都需要另畫圖、工作紙或教學卡。按概念關係編排，不照 Figure／section 順序堆疊。
- 自行舉例標示為說明性範例；規範性用語依 Base 2.4 §1.4.1，不提高原文要求強度。

## 內容與視覺

2026-09-09 補充：中文教學 HTML 必須提供獨立撰寫的逐步解釋、情境與推理，不能只
把 post 的折疊內容展開。中英文 post 保留全局解釋、案例、流程及 Spec 閱讀位置；完整技術細節放在中文 HTML。
每篇在結尾問答前，按概念整理所有範圍內規格圖表的閱讀教學；一組相關圖表可以
共同教學，不要求逐圖重畫。每張自製圖表須有明確的理解目的，沒有增益就使用文字。
比較表逐張設定有意義的欄名，不得套用「作用或差異／適用條件」等通用表頭。
解釋須寫清楚主詞、動作與結果，不使用 gate、otherwise-valid create 等混雜速記。
同一文件同一術語的定義最多出現 2 次，包含折疊內容；後續用連結回到解釋處。
算例必須核對數值、單位與整數倍方向；NSZE=1000、LBA=4 KiB 是 4000 KiB。
CI 維護規則見 docs/ci-pages-maintenance.md；完成前核對同一 commit 的全部相關
workflow，不得把單一 Pages 成功或網站 HTTP 200 當作 CI 全數成功。

詳細寫法見 `.ai/nvme-report/style-guide.md`，離線相容性見 `ipad-html-profile.md`。

- 每版開頭先破題，說明主題、重要性與主軸，搭配合適的總覽圖或表。
- 每篇補足必要背景，再依理解順序教學。同一概念完整解釋一次，後文應用或連回；跨篇可短述必要背景。
- 名詞與縮寫在首次出現的段落下方解釋，圖內首次出現者就在圖下解釋。避免自創名詞，必要的教學簡稱也須立即說明。阿拉伯數字、位元範圍、十六進位編碼與單位保留原樣，不翻譯數字。
- 視覺參考使用者提供的 `nvme-ch3-tutorial.html` 與 `NVMe資料結構教學-SQE-CQE-PRP.html`：清楚層級、留白、單欄長文、欄位圖、狀態圖、關係圖及比較表。技術內容仍依規格核對。
- 圖示直接說明元件、欄位、資料流及條件，不用無具體對象的 Locate／Decode 標籤。不強制固定圖種，也不強制每張 Figure 配工作紙。
- 結尾用少量有答案、有來源的問題鞏固不同概念；不複製正文、不用雷同題目、不設 16 題等湊數門檻。
- 開發流程、內部追蹤編號、產生及檢查紀錄放在不顯示的 HTML 註解或內部文件。claim ID 不呈現在正文。短來源就近顯示，完整 citation 可收合。
- 不設 Debug／模擬實作故障單元；規格必要條件、狀態與例外放回相關機制解釋。

## 驗證與發布

- Publish：`python3 -B scripts/validate_nvme_report.py --phase publish`
- Test：`python3 -B -m unittest discover -s tests -v`
- 來源核對：`python3 -B scripts/validate_nvme_report.py --phase setup --source-dir <PDF_DIR>`
- 驗證實質內容、雙語一致性、來源、claim 完整性、重複與離線安全；不以字數加倍或固定圖表數取代品質。
- 檢視 iPad portrait／landscape、desktop 及明暗色系，確認圖文和導覽可讀、沒有整頁橫向溢出。
- 使用者已授權完成驗證後直接 git add、commit、push 並更新 GitHub Pages。


2026-09-11：兩篇合輯拆為 Self-test、Namespace Management、Boot Partitions、Telemetry、Sanitize。原 HMB 合輯的完整 Self-test 集中至專篇。每張範圍內圖表須有獨立的一句話重點、具體案例、必要細節與來源；共用規則只解釋一次，其餘連回，禁止同段套給所有 Figure。APST 2000 ms、PS3 的低 Dword 正確值是 0007D018h，須以位移運算驗證，不得只用預期字串測試。英文片語替換須有單字邊界，active NSID 不得匹配 inactive NSID。


2026-09-13：全部 13 篇中文 HTML 採獨立課程編排，先情境與全貌，再逐步推理、欄位關係及完整案例。五篇精確主範圍見 scope.json 的 primary_scope；必要引用單獨說明用途。範圍內及必要引用圖表均須教會欄位如何一起決定操作或結果，不能只列欄名。Reserved 依該處規則交代，不逐列湊字。必要解釋預設顯示，共同定義只解釋一次並可就近連回。狀態與事件用有條件的轉移圖，延遲用時間軸；不得把適用配置放進重設結果欄。

2026-09-15：新增 Directives／Streams 專篇，Base §8.1.9 排除 §8.1.9.4，加 §5.2.7、§5.2.8、§5.2.30.1.35 與 NVM §5.13。Host Identifier 只取共同與 PCIe 規則；前篇 Admin／I/O 的排除項不變。啟用的外層 DTYPE=00h 與目標 DTYPE=01h 必須分清；NSSA 是非專用資源池大小，不是閒置數。Spec 目錄部分頁碼與正文不一致，報告路徑採 PDF 檢視器實際頁碼並標共享頁的停止標題。

2026-09-16：新增 FDP 專篇，指定 Base／NVM 範圍、33 張主範圍與 26 張必要引用見 scope.json；維護注意事項見 docs/nvme-fdp-scope-and-teaching.md。FDP 不繼承前篇對本次明確指定內容的排除。Write 的非法 PID 容錯不可套到 Update；零值 DSM 限制須連同 NVMDSMSV 判斷。

2026-09-16：新增 Command and Feature Lockdown 專篇，主範圍僅 Base §8.1.5、§5.2.13.1.20（LID14h）、§5.2.16。8張主範圍與21張必要引用逐圖解說；一般全體清單與增強FFFFh彙整不可混用，ACNTL0不是無禁止。LDPE跨斷電持續性不能套到CSEL1/2。維護紀錄見 docs/nvme-lockdown-scope-and-teaching.md。

2026-09-21：新增 Read Recovery Level 專篇，Base §8.1.23、§5.2.30.1.12（FID 12h），3 張主範圍與 11 張必要引用。RRLS bitmap 與 4-bit RRL 代碼分開；SEL=3 的能力回覆不得解成目前等級；Figure 466 持續性欄只適用不可保存的 Feature。Fast Fail 不代表固定延遲或零次重試。維護紀錄見 docs/nvme-rrl-scope-and-teaching.md。

2026-09-22：新增 SQ Associations 專篇，主範圍 Base §8.1.28 本身無編號圖表，15 張必要引用分組教學。Create I/O SQ 的 NVMSETID=0 表示無特定關聯；建立時非法 Set 與後續錯誤分流的後果分開。PLM 實際標題為 §8.1.21，不沿用本節舊交叉引用。維護紀錄見 docs/nvme-sqa-scope-and-teaching.md。

2026-09-22：新增 Endurance Group 健康與事件專篇，Base §5.2.13.1.10、§5.2.13.1.15、§5.2.30.1.17；4 張主圖與 16 張必要引用。0Fh 通知確認與 09h 逐組確認分開；Figure209 出廠預設復原不能當作一般 reset。維護紀錄見 docs/nvme-endurance-scope-and-teaching.md。

2026-09-23：新增 Namespace Write Protection 專篇，Base §8.1.18 與 §5.2.30.1.38（FID84h）；4張主圖與12張必要引用。NWPC能力、WPC進入許可、WPS狀態分開；控制位重設不解除既有保護，不可保存不等於不持續。維護紀錄見 docs/nvme-nwp-scope-and-teaching.md。

2026-09-25：新增 Persistent Event Log 專篇，Base §5.2.13.1.14 與 NVM §4.1.4.4；30張主範圍與31張必要引用。EL包含VSI，ACT3的RCE0不是建立失敗；Namespace Sanitize PREQ在bit4，不能套用subsystem的bit11。來源差異與範圍裁切見 docs/nvme-pel-scope-and-teaching.md。
