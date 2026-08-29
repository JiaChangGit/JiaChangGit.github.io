---
layout: post
read_time: true
show_date: true
title: "NVMe over PCIe Transport 1.4：完整傳輸綁定"
date: 2026-08-28
description: "供 GitHub Pages 與 PPT 使用的 NVMe 規格導讀。"
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---

# NVMe over PCIe Transport 1.4：完整傳輸綁定

用途：供 GitHub Pages 閱讀與 100 分鐘簡報製作；讀者已具備 PCIe 與 NVMe 基礎。

範圍：§1–§3 與 Annex A；文件頁／PDF 頁 1–48。正文只保留 PCIe／memory-based 與通用 NVMe 內容。

## 來源版本

NVM Express NVMe over PCIe Transport Specification, Revision 1.4
NVM Express Base Specification, Revision 2.4

查證日期：2026-08-29。目前未納入其他 Errata、ECN、Technical Proposal、controller vendor 文件或未提供的 PCI Express Base Specification 原文。

## 閱讀地圖

```text
Write SQE -> Ring SQ tail doorbell -> Controller executes -> Read CQE / ring CQ head
```

PCIe transport 以 host memory 的 queue 配合 MMIO doorbell；資料可由 PRP／SGL 指到 host-addressable memory。

## 規範性用語

shall 譯為「必須」，may 譯為「可／得」，should 譯為「宜／建議」，optional 譯為「選用」。本文不提高或降低原文語氣。

## 規格重點

### 1. PCIE14-SCOPE

<!-- claim:PCIE14-SCOPE -->

PCIe Transport 補充 Base Specification，定義 PCIe 專屬資料結構、延伸、要求與行為；通用 NVMe 行為仍由 Base 定義。規格衝突時 Base 的優先序高於 Transport。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, 文件頁 6, PDF 頁 6

### 2. PCIE14-CONVENTION

<!-- claim:PCIE14-CONVENTION -->

本文件沿用 Base 的 conventions；register／property 表格中的 Reset 欄改表示依 PCI 或 PCIe 規格定義之 reset 後欄位值。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.3, 文件頁 6-7, PDF 頁 6-7

### 3. PCIE14-KEYWORDS

<!-- claim:PCIE14-KEYWORDS -->

shall、may 與 should 的語氣仍由 Base 2.4 定義；Transport 摘要不得自行提高或降低規範強度。

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.4.1, 文件頁 2-3, PDF 頁 28-29

### 4. PCIE14-OVERVIEW

<!-- claim:PCIE14-OVERVIEW -->

PCIe transport 使用 memory-mapped I/O 進行資料與 register 存取，並使用 PCIe configuration space 與 message-signaled interrupt。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, 文件頁 8, PDF 頁 8

### 5. PCIE14-MMIO

<!-- claim:PCIE14-MMIO -->

NVMe controller registers 位於 BAR0／BAR1 所指定的 memory space。host 必須（shall）使用 native width 或 aligned 32-bit access，不得發出 locked access；違反時行為未定義。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, 文件頁 9-10, PDF 頁 9-10

### 6. PCIE14-DOORBELL

<!-- claim:PCIE14-DOORBELL -->

SQ tail 與 CQ head doorbell 從 offset 1000h 起，實際 stride 由 CAP.DSTRD 決定；queue identifier y 參與 offset 計算。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, 文件頁 10-11, PDF 頁 10-11

### 7. PCIE14-QUEUE

<!-- claim:PCIE14-QUEUE -->

PCIe 支援多個 Submission Queues 共用一個 Completion Queue。建立 CQ 時若啟用 interrupt，Interrupt Vector 必須（shall）初始化成對應 MSI-X 或 multiple-message MSI vector。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, 文件頁 11, PDF 頁 11

### 8. PCIE14-RESET

<!-- claim:PCIE14-RESET -->

PCIe reset 來源包含 Base 定義的 controller/reset 流程與 PCIe 層級 reset。Recovery 設計要以 reset 類型判斷 controller property、queue 與 PCI configuration state。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.3, 文件頁 11-12, PDF 頁 11-12

### 9. PCIE14-COMMAND

<!-- claim:PCIE14-COMMAND -->

command flow 是：寫 SQE、更新 SQ tail doorbell、controller 取走與執行、寫 CQE、發出 interrupt（若啟用）、host 處理 CQE、更新 CQ head doorbell。doorbell 只通告 pointer，不攜帶 command 本體。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, 文件頁 12-13, PDF 頁 12-13

### 10. PCIE14-INTERRUPT

<!-- claim:PCIE14-INTERRUPT -->

可用模式為 pin-based、single-message MSI、multiple-message MSI 與 MSI-X。規格建議 MSI-X；coalescing 可降低 interrupt rate，但通常增加 latency。Admin CQ 的 interrupt 不宜（should not）延遲。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, 文件頁 13-16, PDF 頁 13-16

### 11. PCIE14-POWER

<!-- claim:PCIE14-POWER -->

host 絕不可（shall never）選擇功耗高於 PCIe slot power limit 的 NVMe power state；違反時 power behavior 未定義。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.6, 文件頁 16, PDF 頁 16

### 12. PCIE14-ERROR

<!-- claim:PCIE14-ERROR -->

NVMe command error 由 CQE status 回報；PCIe transport／link error 則依 PCIe 機制與本文件的 NVMe-specific 要求處理，兩者的 recovery 層級不同。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, 文件頁 16, PDF 頁 16

### 13. PCIE14-CONFIG

<!-- claim:PCIE14-CONFIG -->

§3.8 逐欄定義 NVMe controller 的 PCI header、Power Management、MSI／MSI-X、PCIe capability 與 AER 額外要求。PCI／PCIe 原始欄位語意仍以 PCI-SIG 規格為準。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, 文件頁 16-35, PDF 頁 16-35

### 14. PCIE14-SECURITY

<!-- claim:PCIE14-SECURITY -->

power-loss signaling、confidential computing 與 TDISP 把平台事件或隔離狀態映射到 NVMe controller 行為；實作仍需要本次未提供的外部 PCIe／TDISP 規格。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.8-3.8.10, 文件頁 35-39, PDF 頁 35-39

### 15. PCIE14-EOM

<!-- claim:PCIE14-EOM -->

Physical Interface Receiver Eye Opening Measurement log page 以 header、lane descriptor 與 EOM data 回報量測；host 先查支援與大小，再依 lane／parameter 解析。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, 文件頁 39-46, PDF 頁 39-46

### 16. PCIE14-HOST

<!-- claim:PCIE14-HOST -->

Annex A 是 informative host checklist：提交時先寫 SQE 再 doorbell；完成時以 phase 判斷新 CQE，完成讀取後再推進 CQ head；interrupt handler 要處理同 vector 的所有相關 CQ。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, 文件頁 47-48, PDF 頁 47-48

## Figure 逐圖導讀

本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。

### Figure 1: NVMe Family of Specifications

<!-- claim:PCIE14-FIG-001-CLAIM figure-table:PCIE14-FIG-001 -->

Figure 1〈NVMe Family of Specifications〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。 本報告只解釋圖中的 PCIe／memory-based 部分。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

- 範圍：只介紹 PCIe／memory-based 部分。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, Figure 1, 文件頁 6, PDF 頁 6

### Figure 2: Example of Transport Protocol Layers

<!-- claim:PCIE14-FIG-002-CLAIM figure-table:PCIE14-FIG-002 -->

Figure 2〈Example of Transport Protocol Layers〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, Figure 2, 文件頁 8, PDF 頁 8

### Figure 3: PCI Express Registers

<!-- claim:PCIE14-FIG-003-CLAIM figure-table:PCIE14-FIG-003 -->

Figure 3〈PCI Express Registers〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, Figure 3, 文件頁 9, PDF 頁 9

### Figure 4: PCI Express Specific Controller Property Definitions

<!-- claim:PCIE14-FIG-004-CLAIM figure-table:PCIE14-FIG-004 -->

Figure 4〈PCI Express Specific Controller Property Definitions〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, Figure 4, 文件頁 9-10, PDF 頁 9-10

### Figure 5: Offset (1000h + ((2y) * (4 << CAP.DSTRD))): SQyTDBL – Submission Queue y Tail

<!-- claim:PCIE14-FIG-005-CLAIM figure-table:PCIE14-FIG-005 -->

Figure 5〈Offset (1000h + ((2y) * (4 << CAP.DSTRD))): SQyTDBL – Submission Queue y Tail〉：整理 queue／command 的關係或處理順序。 依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 解決的問題：整理 queue／command 的關係或處理順序。

- 閱讀順序：依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先選一個 queue identifier，沿箭頭追蹤一筆 command 與 completion。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1, Figure 5, 文件頁 10, PDF 頁 10

### Figure 6: Offset (1000h + ((2y + 1) * (4 << CAP.DSTRD))): CQyHDBL – Completion Queue y Head

<!-- claim:PCIE14-FIG-006-CLAIM figure-table:PCIE14-FIG-006 -->

Figure 6〈Offset (1000h + ((2y + 1) * (4 << CAP.DSTRD))): CQyHDBL – Completion Queue y Head〉：整理 queue／command 的關係或處理順序。 依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 解決的問題：整理 queue／command 的關係或處理順序。

- 閱讀順序：依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先選一個 queue identifier，沿箭頭追蹤一筆 command 與 completion。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1, Figure 6, 文件頁 10-11, PDF 頁 10-11

### Figure 7: Create I/O Completion Queue – Command Dword 11

<!-- claim:PCIE14-FIG-007-CLAIM figure-table:PCIE14-FIG-007 -->

Figure 7〈Create I/O Completion Queue – Command Dword 11〉：整理 queue／command 的關係或處理順序。 依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 解決的問題：整理 queue／command 的關係或處理順序。

- 閱讀順序：依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先選一個 queue identifier，沿箭頭追蹤一筆 command 與 completion。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, Figure 7, 文件頁 11, PDF 頁 11

### Figure 8: Command Processing

<!-- claim:PCIE14-FIG-008-CLAIM figure-table:PCIE14-FIG-008 -->

Figure 8〈Command Processing〉：整理 queue／command 的關係或處理順序。 依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 解決的問題：整理 queue／command 的關係或處理順序。

- 閱讀順序：依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先選一個 queue identifier，沿箭頭追蹤一筆 command 與 completion。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4.1, Figure 8, 文件頁 13, PDF 頁 13

### Figure 9: Pin Based, Single MSI, and Multiple MSI Behavior

<!-- claim:PCIE14-FIG-009-CLAIM figure-table:PCIE14-FIG-009 -->

Figure 9〈Pin Based, Single MSI, and Multiple MSI Behavior〉：說明 interrupt capability、vector 或通知行為。 分開 capability 是否存在、enable 狀態、vector mapping 與 pending／mask。

- 解決的問題：說明 interrupt capability、vector 或通知行為。

- 閱讀順序：分開 capability 是否存在、enable 狀態、vector mapping 與 pending／mask。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：為兩個 Completion Queues 配置 vector，檢查是否共用及如何服務。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5.1, Figure 9, 文件頁 15, PDF 頁 15

### Figure 10: PCI Express Type 0/1 Common Configuration Space

<!-- claim:PCIE14-FIG-010-CLAIM figure-table:PCIE14-FIG-010 -->

Figure 10〈PCI Express Type 0/1 Common Configuration Space〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8, Figure 10, 文件頁 16-17, PDF 頁 16-17

### Figure 11: Offset 00h: ID - Identifiers

<!-- claim:PCIE14-FIG-011-CLAIM figure-table:PCIE14-FIG-011 -->

Figure 11〈Offset 00h: ID - Identifiers〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.1, Figure 11, 文件頁 17, PDF 頁 17

### Figure 12: Offset 04h: CMD - Command

<!-- claim:PCIE14-FIG-012-CLAIM figure-table:PCIE14-FIG-012 -->

Figure 12〈Offset 04h: CMD - Command〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.2, Figure 12, 文件頁 17, PDF 頁 17

### Figure 13: Offset 06h: STS – Device Status

<!-- claim:PCIE14-FIG-013-CLAIM figure-table:PCIE14-FIG-013 -->

Figure 13〈Offset 06h: STS – Device Status〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.3, Figure 13, 文件頁 18, PDF 頁 18

### Figure 14: Offset 08h: RID - Revision ID

<!-- claim:PCIE14-FIG-014-CLAIM figure-table:PCIE14-FIG-014 -->

Figure 14〈Offset 08h: RID - Revision ID〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.4, Figure 14, 文件頁 18, PDF 頁 18

### Figure 15: Offset 09h: CC - Class Code

<!-- claim:PCIE14-FIG-015-CLAIM figure-table:PCIE14-FIG-015 -->

Figure 15〈Offset 09h: CC - Class Code〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.5, Figure 15, 文件頁 18, PDF 頁 18

### Figure 16: Offset 0Ch: CLS – Cache Line Size

<!-- claim:PCIE14-FIG-016-CLAIM figure-table:PCIE14-FIG-016 -->

Figure 16〈Offset 0Ch: CLS – Cache Line Size〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.6, Figure 16, 文件頁 18, PDF 頁 18

### Figure 17: Offset 0Dh: MLT – Master Latency Timer

<!-- claim:PCIE14-FIG-017-CLAIM figure-table:PCIE14-FIG-017 -->

Figure 17〈Offset 0Dh: MLT – Master Latency Timer〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.7, Figure 17, 文件頁 18, PDF 頁 18

### Figure 18: Offset 0Eh: HTYPE – Header Type

<!-- claim:PCIE14-FIG-018-CLAIM figure-table:PCIE14-FIG-018 -->

Figure 18〈Offset 0Eh: HTYPE – Header Type〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.8, Figure 18, 文件頁 19, PDF 頁 19

### Figure 19: Offset 0Fh: BIST – Built-In Self Test (Optional)

<!-- claim:PCIE14-FIG-019-CLAIM figure-table:PCIE14-FIG-019 -->

Figure 19〈Offset 0Fh: BIST – Built-In Self Test (Optional)〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.9, Figure 19, 文件頁 19, PDF 頁 19

### Figure 20: Offset 10h: MLBAR (BAR0) – Memory Register Base Address, lower 32-bits

<!-- claim:PCIE14-FIG-020-CLAIM figure-table:PCIE14-FIG-020 -->

Figure 20〈Offset 10h: MLBAR (BAR0) – Memory Register Base Address, lower 32-bits〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.10, Figure 20, 文件頁 19, PDF 頁 19

### Figure 21: Offset 14h: MUBAR (BAR1) – Memory Register Base Address, upper 32-bits

<!-- claim:PCIE14-FIG-021-CLAIM figure-table:PCIE14-FIG-021 -->

Figure 21〈Offset 14h: MUBAR (BAR1) – Memory Register Base Address, upper 32-bits〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.11, Figure 21, 文件頁 19, PDF 頁 19

### Figure 22: Offset 18h: BAR2 – Index/Data Pair Register Base Address or Vendor Specific

<!-- claim:PCIE14-FIG-022-CLAIM figure-table:PCIE14-FIG-022 -->

Figure 22〈Offset 18h: BAR2 – Index/Data Pair Register Base Address or Vendor Specific〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.12, Figure 22, 文件頁 20, PDF 頁 20

### Figure 23: Offset 28h: CCPTR – CardBus CIS Pointer

<!-- claim:PCIE14-FIG-023-CLAIM figure-table:PCIE14-FIG-023 -->

Figure 23〈Offset 28h: CCPTR – CardBus CIS Pointer〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.16, Figure 23, 文件頁 20, PDF 頁 20

### Figure 24: Offset 2Ch: SS - Subsystem Identifiers

<!-- claim:PCIE14-FIG-024-CLAIM figure-table:PCIE14-FIG-024 -->

Figure 24〈Offset 2Ch: SS - Subsystem Identifiers〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.17, Figure 24, 文件頁 20, PDF 頁 20

### Figure 25: Offset 30h: EROM – Expansion ROM (Optional)

<!-- claim:PCIE14-FIG-025-CLAIM figure-table:PCIE14-FIG-025 -->

Figure 25〈Offset 30h: EROM – Expansion ROM (Optional)〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.18, Figure 25, 文件頁 20, PDF 頁 20

### Figure 26: Offset 34h: CAP – Capabilities Pointer

<!-- claim:PCIE14-FIG-026-CLAIM figure-table:PCIE14-FIG-026 -->

Figure 26〈Offset 34h: CAP – Capabilities Pointer〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.19, Figure 26, 文件頁 21, PDF 頁 21

### Figure 27: Offset 3Ch: INTR - Interrupt Information

<!-- claim:PCIE14-FIG-027-CLAIM figure-table:PCIE14-FIG-027 -->

Figure 27〈Offset 3Ch: INTR - Interrupt Information〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.20, Figure 27, 文件頁 21, PDF 頁 21

### Figure 28: Offset 3Eh: MGNT – Minimum Grant

<!-- claim:PCIE14-FIG-028-CLAIM figure-table:PCIE14-FIG-028 -->

Figure 28〈Offset 3Eh: MGNT – Minimum Grant〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.21, Figure 28, 文件頁 21, PDF 頁 21

### Figure 29: Offset 3Fh: MLAT – Maximum Latency

<!-- claim:PCIE14-FIG-029-CLAIM figure-table:PCIE14-FIG-029 -->

Figure 29〈Offset 3Fh: MLAT – Maximum Latency〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.22, Figure 29, 文件頁 21, PDF 頁 21

### Figure 30: PCI Power Management Capabilities

<!-- claim:PCIE14-FIG-030-CLAIM figure-table:PCIE14-FIG-030 -->

Figure 30〈PCI Power Management Capabilities〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.22, Figure 30, 文件頁 21, PDF 頁 21

### Figure 31: Offset PMCAP: PID - PCI Power Management Capability ID

<!-- claim:PCIE14-FIG-031-CLAIM figure-table:PCIE14-FIG-031 -->

Figure 31〈Offset PMCAP: PID - PCI Power Management Capability ID〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.1, Figure 31, 文件頁 21, PDF 頁 21

### Figure 32: Offset PMCAP + 2h: PC – PCI Power Management Capabilities

<!-- claim:PCIE14-FIG-032-CLAIM figure-table:PCIE14-FIG-032 -->

Figure 32〈Offset PMCAP + 2h: PC – PCI Power Management Capabilities〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.2, Figure 32, 文件頁 22, PDF 頁 22

### Figure 33: Offset PMCAP + 4h: PMCS – PCI Power Management Control and Status

<!-- claim:PCIE14-FIG-033-CLAIM figure-table:PCIE14-FIG-033 -->

Figure 33〈Offset PMCAP + 4h: PMCS – PCI Power Management Control and Status〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.3, Figure 33, 文件頁 22, PDF 頁 22

### Figure 34: Message Signaled Interrupt Capability (Optional)

<!-- claim:PCIE14-FIG-034-CLAIM figure-table:PCIE14-FIG-034 -->

Figure 34〈Message Signaled Interrupt Capability (Optional)〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.3, Figure 34, 文件頁 22, PDF 頁 22

### Figure 35: Offset MSICAP: MID – Message Signaled Interrupt Identifiers

<!-- claim:PCIE14-FIG-035-CLAIM figure-table:PCIE14-FIG-035 -->

Figure 35〈Offset MSICAP: MID – Message Signaled Interrupt Identifiers〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.1, Figure 35, 文件頁 23, PDF 頁 23

### Figure 36: Offset MSICAP + 2h: MC – Message Signaled Interrupt Message Control

<!-- claim:PCIE14-FIG-036-CLAIM figure-table:PCIE14-FIG-036 -->

Figure 36〈Offset MSICAP + 2h: MC – Message Signaled Interrupt Message Control〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.2, Figure 36, 文件頁 23, PDF 頁 23

### Figure 37: Offset MSICAP + 4h: MA – Message Signaled Interrupt Message Address

<!-- claim:PCIE14-FIG-037-CLAIM figure-table:PCIE14-FIG-037 -->

Figure 37〈Offset MSICAP + 4h: MA – Message Signaled Interrupt Message Address〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.3, Figure 37, 文件頁 23, PDF 頁 23

### Figure 38: Offset MSICAP + 8h: MUA – Message Signaled Interrupt Upper Address

<!-- claim:PCIE14-FIG-038-CLAIM figure-table:PCIE14-FIG-038 -->

Figure 38〈Offset MSICAP + 8h: MUA – Message Signaled Interrupt Upper Address〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.4, Figure 38, 文件頁 23, PDF 頁 23

### Figure 39: Offset MSICAP + Ch: MD – Message Signaled Interrupt Message Data

<!-- claim:PCIE14-FIG-039-CLAIM figure-table:PCIE14-FIG-039 -->

Figure 39〈Offset MSICAP + Ch: MD – Message Signaled Interrupt Message Data〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.5, Figure 39, 文件頁 23, PDF 頁 23

### Figure 40: Offset MSICAP + 10h: MMASK – Message Signaled Interrupt Mask Bits (Optional)

<!-- claim:PCIE14-FIG-040-CLAIM figure-table:PCIE14-FIG-040 -->

Figure 40〈Offset MSICAP + 10h: MMASK – Message Signaled Interrupt Mask Bits (Optional)〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.6, Figure 40, 文件頁 24, PDF 頁 24

### Figure 41: Offset MSICAP + 14h: MPEND – Message Signaled Interrupt Pending Bits (Optional)

<!-- claim:PCIE14-FIG-041-CLAIM figure-table:PCIE14-FIG-041 -->

Figure 41〈Offset MSICAP + 14h: MPEND – Message Signaled Interrupt Pending Bits (Optional)〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.7, Figure 41, 文件頁 24, PDF 頁 24

### Figure 42: MSI-X Capability (Optional)

<!-- claim:PCIE14-FIG-042-CLAIM figure-table:PCIE14-FIG-042 -->

Figure 42〈MSI-X Capability (Optional)〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.7, Figure 42, 文件頁 24, PDF 頁 24

### Figure 43: Offset MSIXCAP: MXID – MSI-X Identifiers

<!-- claim:PCIE14-FIG-043-CLAIM figure-table:PCIE14-FIG-043 -->

Figure 43〈Offset MSIXCAP: MXID – MSI-X Identifiers〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.1, Figure 43, 文件頁 24, PDF 頁 24

### Figure 44: Offset MSIXCAP + 2h: MXC – MSI-X Message Control

<!-- claim:PCIE14-FIG-044-CLAIM figure-table:PCIE14-FIG-044 -->

Figure 44〈Offset MSIXCAP + 2h: MXC – MSI-X Message Control〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.2, Figure 44, 文件頁 24-25, PDF 頁 24-25

### Figure 45: Offset MSIXCAP + 4h: MTAB – MSI-X Table Offset / Table BIR

<!-- claim:PCIE14-FIG-045-CLAIM figure-table:PCIE14-FIG-045 -->

Figure 45〈Offset MSIXCAP + 4h: MTAB – MSI-X Table Offset / Table BIR〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.3, Figure 45, 文件頁 25, PDF 頁 25

### Figure 46: Offset MSIXCAP + 8h: MPBA – MSI-X PBA Offset / PBA BIR

<!-- claim:PCIE14-FIG-046-CLAIM figure-table:PCIE14-FIG-046 -->

Figure 46〈Offset MSIXCAP + 8h: MPBA – MSI-X PBA Offset / PBA BIR〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.4, Figure 46, 文件頁 25, PDF 頁 25

### Figure 47: PCI Express Capability

<!-- claim:PCIE14-FIG-047-CLAIM figure-table:PCIE14-FIG-047 -->

Figure 47〈PCI Express Capability〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5, Figure 47, 文件頁 26, PDF 頁 26

### Figure 48: Offset PXCAP: PXID – PCI Express Capability ID

<!-- claim:PCIE14-FIG-048-CLAIM figure-table:PCIE14-FIG-048 -->

Figure 48〈Offset PXCAP: PXID – PCI Express Capability ID〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.1, Figure 48, 文件頁 26, PDF 頁 26

### Figure 49: Offset PXCAP + 2h: PXCAP – PCI Express Capabilities

<!-- claim:PCIE14-FIG-049-CLAIM figure-table:PCIE14-FIG-049 -->

Figure 49〈Offset PXCAP + 2h: PXCAP – PCI Express Capabilities〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.2, Figure 49, 文件頁 26, PDF 頁 26

### Figure 50: Offset PXCAP + 4h: PXDCAP – PCI Express Device Capabilities

<!-- claim:PCIE14-FIG-050-CLAIM figure-table:PCIE14-FIG-050 -->

Figure 50〈Offset PXCAP + 4h: PXDCAP – PCI Express Device Capabilities〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.3, Figure 50, 文件頁 26-27, PDF 頁 26-27

### Figure 51: Offset PXCAP + 8h: PXDC – PCI Express Device Control

<!-- claim:PCIE14-FIG-051-CLAIM figure-table:PCIE14-FIG-051 -->

Figure 51〈Offset PXCAP + 8h: PXDC – PCI Express Device Control〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.4, Figure 51, 文件頁 27-28, PDF 頁 27-28

### Figure 52: Offset PXCAP + Ah: PXDS – PCI Express Device Status

<!-- claim:PCIE14-FIG-052-CLAIM figure-table:PCIE14-FIG-052 -->

Figure 52〈Offset PXCAP + Ah: PXDS – PCI Express Device Status〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.5, Figure 52, 文件頁 28, PDF 頁 28

### Figure 53: Offset PXCAP + Ch: PXLCAP – PCI Express Link Capabilities

<!-- claim:PCIE14-FIG-053-CLAIM figure-table:PCIE14-FIG-053 -->

Figure 53〈Offset PXCAP + Ch: PXLCAP – PCI Express Link Capabilities〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.6, Figure 53, 文件頁 28-29, PDF 頁 28-29

### Figure 54: Offset PXCAP + 10h: PXLC – PCI Express Link Control

<!-- claim:PCIE14-FIG-054-CLAIM figure-table:PCIE14-FIG-054 -->

Figure 54〈Offset PXCAP + 10h: PXLC – PCI Express Link Control〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.7, Figure 54, 文件頁 29, PDF 頁 29

### Figure 55: Offset PXCAP + 12h: PXLS – PCI Express Link Status

<!-- claim:PCIE14-FIG-055-CLAIM figure-table:PCIE14-FIG-055 -->

Figure 55〈Offset PXCAP + 12h: PXLS – PCI Express Link Status〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.8, Figure 55, 文件頁 29, PDF 頁 29

### Figure 56: Offset PXCAP + 24h: PXDCAP2 – PCI Express Device Capabilities 2

<!-- claim:PCIE14-FIG-056-CLAIM figure-table:PCIE14-FIG-056 -->

Figure 56〈Offset PXCAP + 24h: PXDCAP2 – PCI Express Device Capabilities 2〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.9, Figure 56, 文件頁 30, PDF 頁 30

### Figure 57: Offset PXCAP + 28h: PXDC2 – PCI Express Device Control 2

<!-- claim:PCIE14-FIG-057-CLAIM figure-table:PCIE14-FIG-057 -->

Figure 57〈Offset PXCAP + 28h: PXDC2 – PCI Express Device Control 2〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.10, Figure 57, 文件頁 30-31, PDF 頁 30-31

### Figure 58: Advanced Error Reporting Capability (Optional)

<!-- claim:PCIE14-FIG-058-CLAIM figure-table:PCIE14-FIG-058 -->

Figure 58〈Advanced Error Reporting Capability (Optional)〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.10, Figure 58, 文件頁 31, PDF 頁 31

### Figure 59: Offset AERCAP: AERID – AER Capability ID

<!-- claim:PCIE14-FIG-059-CLAIM figure-table:PCIE14-FIG-059 -->

Figure 59〈Offset AERCAP: AERID – AER Capability ID〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.1, Figure 59, 文件頁 31, PDF 頁 31

### Figure 60: Offset AERCAP + 4: AERUCES – AER Uncorrectable Error Status Register

<!-- claim:PCIE14-FIG-060-CLAIM figure-table:PCIE14-FIG-060 -->

Figure 60〈Offset AERCAP + 4: AERUCES – AER Uncorrectable Error Status Register〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.2, Figure 60, 文件頁 31-32, PDF 頁 31-32

### Figure 61: Offset AERCAP + 8: AERUCEM – AER Uncorrectable Error Mask Register

<!-- claim:PCIE14-FIG-061-CLAIM figure-table:PCIE14-FIG-061 -->

Figure 61〈Offset AERCAP + 8: AERUCEM – AER Uncorrectable Error Mask Register〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.3, Figure 61, 文件頁 32, PDF 頁 32

### Figure 62: Offset AERCAP + Ch: AERUCESEV – AER Uncorrectable Error Severity Register

<!-- claim:PCIE14-FIG-062-CLAIM figure-table:PCIE14-FIG-062 -->

Figure 62〈Offset AERCAP + Ch: AERUCESEV – AER Uncorrectable Error Severity Register〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.4, Figure 62, 文件頁 32-33, PDF 頁 32-33

### Figure 63: Offset AERCAP + 10h: AERCES – AER Correctable Error Status Register

<!-- claim:PCIE14-FIG-063-CLAIM figure-table:PCIE14-FIG-063 -->

Figure 63〈Offset AERCAP + 10h: AERCES – AER Correctable Error Status Register〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.5, Figure 63, 文件頁 33, PDF 頁 33

### Figure 64: Offset AERCAP + 14h: AERCEM – AER Correctable Error Mask Register

<!-- claim:PCIE14-FIG-064-CLAIM figure-table:PCIE14-FIG-064 -->

Figure 64〈Offset AERCAP + 14h: AERCEM – AER Correctable Error Mask Register〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.6, Figure 64, 文件頁 33, PDF 頁 33

### Figure 65: Offset AERCAP + 18h: AERCC – AER Capabilities and Control Register

<!-- claim:PCIE14-FIG-065-CLAIM figure-table:PCIE14-FIG-065 -->

Figure 65〈Offset AERCAP + 18h: AERCC – AER Capabilities and Control Register〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.7, Figure 65, 文件頁 34, PDF 頁 34

### Figure 66: Offset AERCAP + 1Ch: AERHL – AER Header Log Register

<!-- claim:PCIE14-FIG-066-CLAIM figure-table:PCIE14-FIG-066 -->

Figure 66〈Offset AERCAP + 1Ch: AERHL – AER Header Log Register〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.8, Figure 66, 文件頁 34, PDF 頁 34

### Figure 67: Offset AERCAP + 38h: AERTLP – AER TLP Prefix Log Register (Optional)

<!-- claim:PCIE14-FIG-067-CLAIM figure-table:PCIE14-FIG-067 -->

Figure 67〈Offset AERCAP + 38h: AERTLP – AER TLP Prefix Log Register (Optional)〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.9, Figure 67, 文件頁 35, PDF 頁 35

### Figure 68: Example of an Eve Diagram in the Printable Eye Field

<!-- claim:PCIE14-FIG-068-CLAIM figure-table:PCIE14-FIG-068 -->

Figure 68〈Example of an Eve Diagram in the Printable Eye Field〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.9, Figure 68, 文件頁 37, PDF 頁 37

### Figure 69: NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure

<!-- claim:PCIE14-FIG-069-CLAIM figure-table:PCIE14-FIG-069 -->

Figure 69〈NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.10, Figure 69, 文件頁 38-39, PDF 頁 38-39

### Figure 70: Get Log Page – Log Page Identifiers

<!-- claim:PCIE14-FIG-070-CLAIM figure-table:PCIE14-FIG-070 -->

Figure 70〈Get Log Page – Log Page Identifiers〉：整理 identifier 或 list 的 byte layout 與範圍。 先確認長度、byte order、數量欄位、唯一性範圍與保留區。

- 解決的問題：整理 identifier 或 list 的 byte layout 與範圍。

- 閱讀順序：先確認長度、byte order、數量欄位、唯一性範圍與保留區。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：parser 先驗證 count 與長度，再逐筆讀取 identifier。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, Figure 70, 文件頁 39, PDF 頁 39

### Figure 71: Size of Physical Interface Receiver Eye Opening Measurement Log Page

<!-- claim:PCIE14-FIG-071-CLAIM figure-table:PCIE14-FIG-071 -->

Figure 71〈Size of Physical Interface Receiver Eye Opening Measurement Log Page〉：整理 receiver eye measurement 的輸入、輸出或資料格式。 先讀支援與大小，再依 lane、parameter、header 與 descriptor 解碼。

- 解決的問題：整理 receiver eye measurement 的輸入、輸出或資料格式。

- 閱讀順序：先讀支援與大小，再依 lane、parameter、header 與 descriptor 解碼。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先查回報長度，再只解析完整存在的 lane descriptor。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 71, 文件頁 40, PDF 頁 40

### Figure 72: Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field

<!-- claim:PCIE14-FIG-072-CLAIM figure-table:PCIE14-FIG-072 -->

Figure 72〈Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 72, 文件頁 40-41, PDF 頁 40-41

### Figure 73: Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field

<!-- claim:PCIE14-FIG-073-CLAIM figure-table:PCIE14-FIG-073 -->

Figure 73〈Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 73, 文件頁 41, PDF 頁 41

### Figure 74: Physical Interface Receiver Eye Opening Measurement Log Page

<!-- claim:PCIE14-FIG-074-CLAIM figure-table:PCIE14-FIG-074 -->

Figure 74〈Physical Interface Receiver Eye Opening Measurement Log Page〉：整理 receiver eye measurement 的輸入、輸出或資料格式。 先讀支援與大小，再依 lane、parameter、header 與 descriptor 解碼。

- 解決的問題：整理 receiver eye measurement 的輸入、輸出或資料格式。

- 閱讀順序：先讀支援與大小，再依 lane、parameter、header 與 descriptor 解碼。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先查回報長度，再只解析完整存在的 lane descriptor。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 74, 文件頁 41, PDF 頁 41

### Figure 75: EOM Header

<!-- claim:PCIE14-FIG-075-CLAIM figure-table:PCIE14-FIG-075 -->

Figure 75〈EOM Header〉：整理 receiver eye measurement 的輸入、輸出或資料格式。 先讀支援與大小，再依 lane、parameter、header 與 descriptor 解碼。

- 解決的問題：整理 receiver eye measurement 的輸入、輸出或資料格式。

- 閱讀順序：先讀支援與大小，再依 lane、parameter、header 與 descriptor 解碼。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先查回報長度，再只解析完整存在的 lane descriptor。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 75, 文件頁 42-43, PDF 頁 42-43

### Figure 76: EOM Lane Descriptor

<!-- claim:PCIE14-FIG-076-CLAIM figure-table:PCIE14-FIG-076 -->

Figure 76〈EOM Lane Descriptor〉：說明資料 buffer 如何由 PRP／SGL 結構描述。 逐一核對 address、offset、length、alignment 與下一層 pointer。

- 解決的問題：說明資料 buffer 如何由 PRP／SGL 結構描述。

- 閱讀順序：逐一核對 address、offset、length、alignment 與下一層 pointer。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：用跨兩個 memory page 的 buffer 檢查第一個 offset 與後續 alignment。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 76, 文件頁 43-45, PDF 頁 43-45

### Figure 77: Example of an Eve Diagram in the Printable Eye Field

<!-- claim:PCIE14-FIG-077-CLAIM figure-table:PCIE14-FIG-077 -->

Figure 77〈Example of an Eve Diagram in the Printable Eye Field〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 77, 文件頁 46, PDF 頁 46

## 使用與限制

製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata 集合或核准範圍改變時，必須重新核對受影響 claim。
