# NVMe 報告範圍與雙語查核 — 2026-09-03

原站有 8 份報告，先前指定的 Boot／Telemetry／Sanitize 尚未形成發布成品。本次補為第 9 份，並更新全部中英文 posts 與離線 HTML。使用者已明確授權 commit、push 及 GitHub Pages 發布。

## 交付與問答數量

每份提供中文新手 HTML、中文詳細 HTML、中文 post、英文 post，共 36 個交付檔。問答共 212 組；中文 212 題、英文 212 題，每題有答案及來源定位。

| 報告 | 中文／英文 post | 問答組數 | Claim 數 |
|---|---|---:|---:|
| NVMe Base 2.4 第 1、2 章：規格語言、PCIe 佇列與儲存模型 | [中文](../_posts/2026-08-28-nvme-base-ch1-2-zh-tw.md) / [English](../_posts/2026-08-28-nvme-base-ch1-2-en.md) | 16 | 28 |
| NVMe Base 2.4 第 3 章：Controller、Queue、初始化與重設 | [中文](../_posts/2026-08-28-nvme-base-ch3-zh-tw.md) / [English](../_posts/2026-08-28-nvme-base-ch3-en.md) | 20 | 74 |
| NVMe Base 2.4 第 4 章：SQE、CQE、Status、PRP 與 SGL | [中文](../_posts/2026-08-28-nvme-base-ch4-zh-tw.md) / [English](../_posts/2026-08-28-nvme-base-ch4-en.md) | 20 | 56 |
| NVMe Base 2.4：Firmware Update 與 LID 03h 驗證 | [中文](../_posts/2026-08-31-nvme-base-firmware-log-admin-zh-tw.md) / [English](../_posts/2026-08-31-nvme-base-firmware-log-admin-en.md) | 16 | 53 |
| NVMe Base 2.4：Power／Thermal Features 與 Power Management | [中文](../_posts/2026-09-02-nvme-base-power-thermal-features-zh-tw.md) / [English](../_posts/2026-09-02-nvme-base-power-thermal-features-en.md) | 24 | 55 |
| NVMe Base 2.4：Device Self-test、HMB、Doorbell Emulation 與 Vendor Commands | [中文](../_posts/2026-09-02-nvme-base-self-test-hmb-emulation-zh-tw.md) / [English](../_posts/2026-09-02-nvme-base-self-test-hmb-emulation-en.md) | 28 | 67 |
| NVMe Base 2.4：Device Self-test 與 Namespace Management | [中文](../_posts/2026-09-02-nvme-base-self-test-namespace-management-zh-tw.md) / [English](../_posts/2026-09-02-nvme-base-self-test-namespace-management-en.md) | 32 | 73 |
| NVMe over PCIe Transport 1.4：完整傳輸綁定 | [中文](../_posts/2026-08-28-nvme-pcie-transport-1-4-zh-tw.md) / [English](../_posts/2026-08-28-nvme-pcie-transport-1-4-en.md) | 24 | 93 |
| NVMe 2.4：Boot Partitions、Telemetry 與 Sanitize 完整教學 | [中文](../_posts/2026-09-03-nvme-boot-telemetry-sanitize-zh-tw.md) / [English](../_posts/2026-09-03-nvme-boot-telemetry-sanitize-en.md) | 32 | 118 |

## 新增報告的範圍對照

| 主題 | 核准章節 | 教學內容 |
|---|---|---|
| Boot Partitions | Base 8.1.3；5.2.13.1.21（LID 15h）；5.2.30.1.39（FID 85h） | Property／log 讀取、image update、Set Features／RPMB 保護與 reset |
| Telemetry | Base 8.1.30；5.2.13.1.8、5.2.13.1.9（LID 07h、08h） | Area 大小、capture、RAE、generation、一致性、通知與 persistence |
| Sanitize | Base 8.1.27，排除 8.1.27.6；5.2.13.1.38（LID 81h）；5.2.26；5.2.30.1.16（FID 17h） | Target／資料範圍、方法、參數、policy、七個 states、16 條 transitions、限制及結果證據 |
| NVM Read／驗證 | NVM Command Set 4.1.7；5.12，包含 5.12.1 | Sanitize 後資料值、allocated/deallocated 行為與 Media Verification Read |

重複指定的章節合併一次。排除的是 8.1.27.6；8.1.27.4.6 Media Verification 與 8.1.27.4.7 仍完整保留。新增報告有 38 筆核心結論與 80 張圖表教學（32 張主範圍、48 張相依圖表）。相依教學含直接引用及理解引用所需的前置欄位，限制於本題相關內容。

完整 figure allowlist、文件身分、section、印刷頁、PDF 頁、欄位索引與來源頁雜湊位於 `.ai/nvme-report/figure-table-register.json`。原始 PDF 及全文抽取不進入公開儲存庫。

## 雙語查核與修正

- 比對全部 9 對 posts 的 claim ID 集合、順序、完整正文、來源定位，以及教學表格／步驟結構。617 筆 claim 均有成對中英文。
- 問答由相同成對教學資料產生，檢查 212 組題目順序、完整答案與同報告的來源。額外缺漏／錯序測試可偵測回歸。
- 數值掃描標記 86 處候選差異，逐項核對。大多是中文數字、英文拼字、標點或進位記法差異；實際修正 Namespace Management 英文的前 768 bytes 範圍，補齊 NSZE／NCAP。
- 修正 PCIe AER 教學中文對 severity 處置的表達；SEL 依 Namespace Management 的 create/delete/restore 語境定義。STC 分開解釋 Self-test command code、result status code，以及 NVM Read 的 Storage Tag Check。
- Base Figure 201 與 NVM Command Set Figure 201 使用不同來源身分、claim ID 與 HTML anchor；保留來源版本與圖號，避免同號覆蓋。
- 新增報告核對 BPROF bits 29:10（bit 30 保留）、Telemetry 2.4 的 TCDA=0、SANACT／PREQ 不同命令欄位、NDAS／NDI／NODRM、SPROG 分母 65536、verification 與 deallocation 分支。
- 附件內部發現的 section 0、Figure 311／312 及 AEC .1.5／.1.6 引用錯置，報告標示為內部核對結果，未宣稱為官方勘誤。
- 跨頁 Figure 的證據雜湊改以登記的完整頁碼區間計算，包含沒有重複 caption 的 continuation pages。

## 驗證方式與限制

本機核對兩份來源 PDF 的 SHA-256、80 張圖表的完整來源頁與 caption。執行確定性重建、publish validator、25 項 unittest，以及 git diff --check。GitHub Actions 再執行相同閘門、Jekyll build 與 Pages deploy。

瀏覽器檢查新增教學頁的圖表、重複 anchor、834×1194 的問答展開與來源，以及 desktop 版面。這是 Chromium 的尺寸驗證，未冒稱已在實體 iPad／Safari 測試。雙語結構檢查與人工條件核對不能取代原始規格或實機 conformance testing。

## 重建

```sh
python3 -B scripts/build_nvme_reports.py
python3 -B scripts/validate_nvme_report.py --phase publish
python3 -B -m unittest discover -s tests -p 'test_validate_nvme_report.py' -v
python3 -B scripts/verify_nvme_bts_sources.py --source-dir <local-pdf-directory>
```

本次 shell 與 Git 操作使用 RTK；不需要把來源 PDF 放進 repository。
