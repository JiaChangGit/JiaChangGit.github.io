# NVM Command Set 1.3 獨立報告：範圍與查核

使用者要求將 NVM Command Set 單獨製作一份報告，允許與既有報告重疊，並排除
Fabrics。本次按所提供的 Revision 1.3 全文建立獨立教材，保留既有中文教學 HTML、
中文詳細 HTML、中英文 post 與附答案問答的交付方式；先前 git add／commit／push
及直接發布 GitHub Pages 的授權適用。

## 交付入口

- [中文 post](https://jiachanggit.github.io/nvme/nvm-command-set-1-3-zh-tw/)
- [English post](https://jiachanggit.github.io/nvme/nvm-command-set-1-3-en/)
- [中文教學 HTML](../DOCS/nvme-spec-report/nvm-command-set-1.3/tutorial-zh-tw.html)
- [中文詳細 HTML](../DOCS/nvme-spec-report/nvm-command-set-1.3/detailed-spec-zh-tw.html)

本份有 37 個教學單元、148 題成對問答、257 筆可定位的 claims，以及 220 張圖表工作紙。
其中 202 張來自 NVM Command Set、18 張是 Base 必要相依圖表。四份交付物均保留完整
圖表工作紙與問答；100 分鐘口頭報告以核心流程為主，附錄供延伸閱讀。全系列現在為
10 份報告、40 個交付檔。

## 範圍對照

| NVM 章節 | 教學內容 | 文件／PDF 頁 |
| --- | --- | --- |
| 1 | 規格家族、單位、識別空間與閱讀方式 | 9–12 |
| 2 | Namespace、容量、順序、fused、atomicity、metadata、支援矩陣 | 13–24 |
| 3 | 狀態、FDP RUH、Compare、Copy、DSM、Read、Verify、Write、WU、Write Zeroes | 25–61 |
| 4.1.1–4.1.3 | AER、Format、NVM Features、Performance、Rate Limiting 設定 | 62–75 |
| 4.1.4–4.1.5 | Logs、Identify、多份 namespace 結構與格式能力 | 75–110 |
| 4.1.6–4.2 | Namespace Management、Sanitize、Track Send、Get LBA Status | 110–118 |
| 5.1–5.2 | ANA、LBA Status 流程、alignment、granularity、metadata placement | 119–130 |
| 5.3 | PI 格式、CRC、Storage／Reference Tag、PRACT／PRCHK／STC | 130–152 |
| 5.4 | Memory-based resource export template、configuration 與 runtime state | 152–160 |
| 5.5–5.9 | Key Per I/O、LBA Format list、LBA Migration Queue、namespace granularity、錯誤處理 | 160–165 |
| 5.10–5.13 | Hard／Soft limits、能力圖、Reservations、Sanitize、Streams | 165–175 |
| Appendix A | 多 token buckets、讀寫權重、部分執行與 CQE 邊界 | 176–177 |

排除 Fabrics、Discovery、message-based transport／shutdown、capsules、NQN 等內容。
Figures 1、13、15、16、17 的混合矩陣只保留核准部分。§5.4 首段明確限定 memory-based
controllers，因此不能因為名稱有 Exported 就整節排除；Figure 189 的 NQN 欄位仍排除。
同樣保留 §5.7 本機 LBA Migration Queue。驗證器僅對這份新報告放行
“Exported NVM Subsystem” 範本名稱，其他排除詞仍拒絕，且有回歸測試。

Base 相依 Figure：93、97、98、99、101、110、111、116、312、338、346、451、452、491、
561、562、563、712。只教 common SQE／CQE、PRP／SGL、能力探索、Host Behavior、
Sanitize、Track Send、Streams 所需欄位；每張另列 Base 的章節與印刷／PDF 頁碼。

## 來源身分與原文矛盾的處理

來源為使用者提供的 NVM Command Set 1.3（177 頁）及 Base 2.4（870 個 PDF 頁面）。
來源 SHA-256、每張 Figure 的完整跨頁 digest 與 caption 均已核對。NVM 印刷頁等於
PDF 頁；Base 的本範圍 PDF 頁比印刷頁多 26。Figure 129 的證據含 103–106 頁，
包含未重印 caption 的 continuation。PDF、文字擷取及 source screenshots 不進 Git。

以下是對所提供版本的教學查核，**不是官方 errata**。正文同時保留原文定位及判讀理由：

| 定位 | 發現 | 教材處理 |
| --- | --- | --- |
| §3.3.2.2 | 範例將 NAWUN=8h 對應 8 blocks | 區分 raw 0-based 值；8 blocks 的 raw 值為 7h |
| Figure 35 | STCRS 引用 Figure 115 | 指向實際能力定義 Figure 127 |
| Figure 120 | SI 的描述／欄位位置不一致 | 依 SC 與實際 bytes 7:4 判讀 |
| §4.1.5.10.1 | NVM CSI 00h 的脈絡混入 zoned namespace 用語 | 以該節 NVM 查詢語境說明，不擴成 Zoned 教材 |
| §5.3.1.4.1 | 範例將 LBADS=0 對應 512 bytes | 512 bytes 的 exponent 是 9；LBADS=0 有未可用語意 |
| Figure 171 | CDW3 Storage／Reference bit range 重疊 | 以 Figures 166、170 交叉定位 Storage 為高 16 bits；標示工程解讀 |
| §5.3.2.5.1／.2 | Figures 177–180 引用對調 | 按實際 caption 及 Copy 的 0/0 pass-through、1/1 replace 條件判讀 |
| Figure 161 | Check 與慣用 LSB-first register 數值表示不同 | 11199E506128D175h 與 AE8B14860A799888h 互為 64-bit 反轉；並核對 Figure 163 |
| §5.4／Figure 190 | 範本版本較舊；namespace payload caption 寫 Controller | 保留範本固定 Base 2.3／NVM 1.2；依 ENSID／LBAF0／NGUID／NUUID 解碼 |
| §5.10 | Hard／Soft 小節交叉引用錯置 | 按實際 §5.10.1 Hard、§5.10.2 Soft 標題及規則教學 |
| Figures 196／198 | 部分 dword offsets、byte 算例與 LPL 不一致 | 重畫關係圖，不把示例直接當 parser fixture；要求乘 4 與 bounds 檢查 |

CRC 使用獨立 bitwise 程式核算。CRC-32C 的 4 KiB 零值為 98F94189h；CRC-64 的
4 KiB zero／FF／incrementing／decrementing 向量分別為 6482D367EB22B64Eh、
C0DDBA7302ECA3ACh、3E729F5F6750449Ch、9A2DF64B8E9E517Eh，符合 Figure 163。
另驗證 64b Guard／STS=18 的 tag packing 算例：Storage=12345h、Reference=2Ah，
得到 CDW3 low16=48D1h、CDW14=4000002Ah。

## 雙語、排版與重建查核

中英文由同一份成對內容來源產生，核對相同 claim ID、正文、來源、排列，以及
148 題的題序、答案、比較表、案例與引用。中文與英文各自完整呈現條件與例外，
包括 PI disable sentinels、Copy 部分失敗、deallocated reads、reservation permissions
及 sanitize 後的讀值。來源 claim 的實際段落也受驗證，不只比對隱藏 ID。

自繪圖解涵蓋 atomic subranges、Copy destination ordering、metadata placement、
tag packing、export state 長度、Rate Limiting shared graphs 及 token-bucket 分支。
Browser 實際檢查兩份 HTML 與展開圖表；1280px viewport 無整頁水平溢位，正文為
17px，詳細版含 220 張 Figure、148 題，所有 anchor ID 唯一。原生 details、觸控目標、
Light／Dark 對比、iPad responsive CSS 與離線限制由共用契約檢查；未宣稱在實體 iPad
Safari 上重新測試。

```text
python3 -B scripts/build_nvme_reports.py
python3 -B scripts/verify_nvme_bts_sources.py --source-dir <本機 PDF 目錄> --report-id nvm-command-set-1.3
python3 -B scripts/validate_nvme_report.py --phase publish
python3 -B -m unittest discover -s tests -p test_validate_nvme_report.py -v
git diff --check
```

結果：40 個成品重建完成；來源身分與 220 張圖的 caption／完整頁面 digest 通過；
publish 契約與 27 項測試通過，包括 deterministic rebuild、完整範圍、雙語問答、
排除範圍、CRC 與 tag packing。Jekyll build 及 Pages 部署由儲存庫的 GitHub Actions
在 push 後執行。

未提供的 SBC、SLM、TCG 文件只說明其介面相依，不補造外部 payload 或規則。規格
內容一律作為技術資料，沒有將文件中的文字當作工具或發布指令。
