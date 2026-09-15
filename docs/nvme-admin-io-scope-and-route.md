# Admin／I/O 整合報告的來源與路徑維護

依使用者 2026-09-13 指示新增一份整合報告，保留既有 13 篇；此篇提供中文教學 HTML
及內容對等的中英文 Pages。全站為 14 篇、42 個交付檔。

## 核准範圍

`.ai/nvme-report/admin-io-route.json` 保存完整排除清單、納入的 FID／LID／CNS、
PDF 書籤位置、29 個報告停留點、249 張主範圍 Figure 及 1 張必要引用 Figure。`nvme_admin_io_scope.py`
用章節邊界和 selector 檢查範圍，不能以純字串前綴把 §5.2.10 誤判為 §5.2.1 的子節。

- Base：第 5、7 章扣除使用者列出的章節與 selector；以前報過的專題不再額外扣除。第 7 章只保留
  Flush 及共用 opcode 表的 Flush 列。
- NVM：只納入使用者指定的 §3.3.1–3.3.8、§4.1.1、§4.1.2、§4.1.3.1、§4.1.3.2、
  §4.1.3.4、§4.1.4.1、§4.1.4.2、§4.1.5、§5.6 及其子節。
- 不再套用舊專題的 except。Base 第 8 章不是此篇主範圍；必要引用依具體教學用途登記，不等於整章納入。
- Fabrics、Discovery、NQN 不作必要背景。共用表內的排除功能列不展開；保留的 AER
  事件欄位仍解釋有效條件與單位，不因此加入排除 Feature 的配置流程。

必要的 queue／buffer／power／PI／atomicity 名詞，分別在 scope.json 登記為
PREREQUISITE_ONLY；不增加 PDF 報告停留點，也不擴張成整章教學。

## 頁碼核對與避免繞路

採本機原始 PDF 的 outline destinations 及正文標題位置，不採 Base 印刷目錄列出的
舊頁碼。例如 Identify 實際位於 PDF 362／印刷 336，印刷目錄的 334 不是實際目的地。
Base 正文 PDF 頁 = 印刷頁 + 26；NVM 的兩者一致。

依 Base 第 5 章 → 第 7 章 → NVM 指定章節往後讀，只切換一次文件。
每站記錄起點與「哪個標題前停止」，不是把整張 PDF 頁納入：

- B18：PDF 539 從 §5.2.30.1.39 的 Boot 保護開始，再接 PCIe Features。
- B19：PDF 545 跳過 §5.2.30.3，讀同頁 §5.2.30.4。
- N05：PDF 76 讀 §4.1.4.1、§4.1.4.2，遇到 §4.1.4.3 立即停止。
- 空的父標題 Base §5.2.13.2 及子項已排除的 §5.2.14.3，不另外設停留點。

原始 PDF、原文擷取與工作中的 source captions 均留在公開 Git 以外。清冊只保留
章節／頁碼／標題、欄位索引與摘要證據 hash。網站列原檔名與實際頁碼，由讀者打開
自己持有的 Spec；不公開 PDF，也不加入無法在網頁使用的本機檔案連結。

## 易混淆欄位的查證紀錄

- Read 的 NLB 是 block 數減 1；DSM range 的 LLB 是直接 block 數。LBA Range Type
  又使用零起算 NLB；Set CDW11.NUM 是描述子數減 1，Get 忽略請求 NUM，由 CQE 回報 NUM。
- Figure 192 的 NLBAF 是零起算，NULBAF 是直接數量。NLBAF=2、NULBAF=2 共 5 個格式；
  不是直接將原始值相加得到 4。Figure 193 區分共用／非共用能力群，不是僅區分基礎／延伸 entry。
- Base LID 12h 回報 FSUPP、UDCC、NCC、NIC、CCC、USS、FSP；可保存與可變更能力屬
  Get Features SEL=011b，不能加進 LID 12h 的 entry。
- One Shot 事件在回報時清除；不是關閉事件通知設定。Immediate 事件發生時若沒有
  outstanding AER，不會留到之後補報。
- Flush 保證範圍涵蓋提交前已完成命令，不自動包含當時仍在執行的 Write。
  VWC.FB=11b 支援對所有 attached namespaces broadcast；10b 拒絕，00b 為舊行為未定義。
- NVM Figure 127 的縮寫為 PIC；Figure 110 的 LBA 是適用錯誤中的最低編號 LBA。
- 同名縮寫在本篇按命令語境解釋：AER 是 Asynchronous Event Request，STC 依上下文分 Storage Tag Check、Self-test Code 與 Self-test 結果的 Status Code；
  CC.MPS 與 Power State Descriptor.MPS 分別指 memory page 與功率倍率。詞庫不得從其他篇套入錯誤意思。
- Software Progress Marker 的 PBSLC 是 pre-boot software load count，不是進度百分比。

## 重建與驗證

中英文概述位於 `nvme_admin_io_content.py`，新增專題在 `nvme_admin_io_added_topics.py`；中文獨立教學在 `nvme_admin_io_deep_course.py`，學習圖示在 `nvme_admin_io_visuals.py`。本篇逐圖教學在
`nvme_admin_io_figures.py` 與 `nvme_admin_io_figure_revision.py`，不覆寫其他篇的完整教學。`nvme_admin_io.py` 安裝課程、
中英文主軸、比較表、流程圖、問答和 PDF 報告路徑。

按既有 build → publish validator → unittest → Jekyll → 明暗色系／iPad／desktop
順序驗證。發布檢查比對中英文 post 的實際路徑，確認中文 HTML 不含報告路徑、禁止頁碼倒退、核對所有 selector 排除項目
及 Figure 的範圍和頁碼。推送後須確認同一 commit 的兩個 workflow 與部署內容。

## 2026-09-14 範圍與教學修正

使用者已確認「括號的都要排除」；保留章節、FID、LID、CNS 的列舉排除，取消因以前報過而扣除的條件。五個專題在 Base 第 5 章內的命令、Log 與 Feature 均補回。NVM Figure 134 以 referenced_dependency 單獨納入，教會 Base Figure 448 引用的 Create payload；不加入主報告路徑，也不擴張成 NVM §4.1.6 全文。

中文 HTML 依能力、格式、佇列、資料操作、設定及維護編為 30 單元，與 Spec 翻頁無關。中英文 post 仍先建立全局，再按 B01–B22 → N01–N07 開 Spec，僅切換一次文件。HTML 的目錄與正文順序必須相同。

必須保留的具體判讀：

- PCIe Underlying Namespace entry 的 CNTLID 必須為 0 且忽略，不能用它建立 controller 對應；CNSSID 是開始索引，最多回 12 筆，GENCTR 驗證版本。
- Security Receive 的待取回覆可能無法跨 communication loss／Controller Level Reset 保留。
- Delete SQ 成功後不再送出其舊命令完成狀態；未有 CQE 的舊命令隱含以 SQ Deletion 中止。
- DSM 的 IDR／IDW 是整段讀寫意圖，AD 是解除配置要求；三者不改變 NR／LLB，且 NVMDSMSV 決定超量處理。
- NVM §4.1.3.1 補的是 IIELL 的 Read 工作量基準，不能寫成另一份 workload hint 說明。
- Write Zeroes 的 LBACZ 是結果旗標，不是已處理 block 數；Copy 的失敗 DW0 是最低未成功來源索引，也不是已完成量。
- NVM Create 的 Figure 134 對 bytes 512–767 定義 Placement Handle List，優先於 Base 共同表的保留區。

46 項標準函式庫測試及發布契約涵蓋修正後的選擇清單、圖表覆蓋、目錄順序、欄位算例和中英文對等。不要為測試引入 CI 未安裝的 HTML parsing 相依套件。
