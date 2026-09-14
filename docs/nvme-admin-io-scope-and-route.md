# Admin／I/O 整合報告的來源與路徑維護

依使用者 2026-09-13 指示新增一份整合報告，保留既有 13 篇；此篇提供中文教學 HTML
及內容對等的中英文 Pages。全站為 14 篇、42 個交付檔。

## 核准範圍

`.ai/nvme-report/admin-io-route.json` 保存完整排除清單、納入的 FID／LID／CNS、
PDF 書籤位置、24 個報告停留點及 221 張範圍內 Figure。`nvme_admin_io_scope.py`
用章節邊界和 selector 檢查範圍，不能以純字串前綴把 §5.2.10 誤判為 §5.2.1 的子節。

- Base：第 5、7 章扣除使用者列出的章節、selector 及五篇既有專題。第 7 章只保留
  Flush 及共用 opcode 表的 Flush 列。
- NVM：只納入使用者指定的 §3.3.1–3.3.8、§4.1.1、§4.1.2、§4.1.3.1、§4.1.3.2、
  §4.1.3.4、§4.1.4.1、§4.1.4.2、§4.1.5、§5.6 及其子節。
- 原來兩處 except（Base §8.1.17.3、§8.1.27.6）依然排除。
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

- B13：PDF 540 的 §5.2.30.2 才開始，頁面上方的 Boot 保護內容不屬此篇。
- B14：PDF 545 跳過 §5.2.30.3，讀同頁 §5.2.30.4。
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
- 同名縮寫在本篇按命令語境解釋：AER 是 Asynchronous Event Request，STC 是 Storage Tag Check；
  CC.MPS 與 Power State Descriptor.MPS 分別指 memory page 與功率倍率。詞庫不得從其他篇套入錯誤意思。
- Software Progress Marker 的 PBSLC 是 pre-boot software load count，不是進度百分比。

## 重建與驗證

內容集中在 `nvme_admin_io_content.py`；本篇縮小範圍的逐圖教學在
`nvme_admin_io_figures.py`，不覆寫其他篇的完整教學。`nvme_admin_io.py` 安裝課程、
中英文主軸、比較表、流程圖、問答和 PDF 報告路徑。

按既有 build → publish validator → unittest → Jekyll → 明暗色系／iPad／desktop
順序驗證。發布檢查同時比對 3 版的實際路徑、禁止頁碼倒退、核對所有 selector 排除項目
及 Figure 的範圍和頁碼。推送後須確認同一 commit 的兩個 workflow 與部署內容。
