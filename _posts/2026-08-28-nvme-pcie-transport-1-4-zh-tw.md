---
layout: post
read_time: true
show_date: true
title: "NVMe over PCIe Transport 1.4：完整傳輸綁定"
date: 2026-08-28
description: "供 GitHub Pages 與 PPT 使用的 NVMe 規格導讀。"
lang: zh-Hant-TW
img: posts/2026/lion_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---

# NVMe over PCIe Transport 1.4：完整傳輸綁定

用途：供 GitHub Pages 閱讀與 100 分鐘簡報製作；讀者已具備 PCIe 與 NVMe 基礎。

範圍：§1-§3 與 Annex A；文件頁／PDF 頁 1-48。正文只保留 PCIe／memory-based 與通用 NVMe 內容。

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

### 1. Transport 與 Base 的優先序

<!-- claim:PCIE14-SCOPE -->

PCIe Transport 補充 Base Specification，定義 PCIe 專屬資料結構、延伸、要求與行為；通用 NVMe 行為仍由 Base 定義。規格衝突時 Base 的優先序高於 Transport。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, 文件頁 6, PDF 頁 6

### 2. PCIe Reset 欄定義

<!-- claim:PCIE14-CONVENTION -->

本文件沿用 Base 的 conventions；register／property 表格中的 Reset 欄改表示依 PCI 或 PCIe 規格定義之 reset 後欄位值。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.3, 文件頁 6-7, PDF 頁 6-7

### 3. Transport 規範性用語

<!-- claim:PCIE14-KEYWORDS -->

shall、may 與 should 的語氣仍由 Base 2.4 定義；Transport 摘要不得自行提高或降低規範強度。

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.4.1, 文件頁 2-3, PDF 頁 28-29

### 4. PCIe transport 概觀

<!-- claim:PCIE14-OVERVIEW -->

PCIe transport 使用 memory-mapped I/O 進行資料與 register 存取，並使用 PCIe configuration space 與 message-signaled interrupt。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, 文件頁 8, PDF 頁 8

### 5. BAR 與 register 存取

<!-- claim:PCIE14-MMIO -->

NVMe controller registers 位於 BAR0／BAR1 所指定的 memory space。host 必須（shall）使用 native width 或 aligned 32-bit access，不得發出 locked access；違反時行為未定義。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, 文件頁 9-10, PDF 頁 9-10

### 6. SQ／CQ doorbell offset

<!-- claim:PCIE14-DOORBELL -->

SQ tail 與 CQ head doorbell 從 offset 1000h 起，實際 stride 由 CAP.DSTRD 決定；queue identifier y 參與 offset 計算。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, 文件頁 10-11, PDF 頁 10-11

### 7. queue 與 interrupt vector

<!-- claim:PCIE14-QUEUE -->

PCIe 支援多個 Submission Queues 共用一個 Completion Queue。建立 CQ 時若啟用 interrupt，Interrupt Vector 必須（shall）初始化成對應 MSI-X 或 multiple-message MSI vector。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, 文件頁 11, PDF 頁 11

### 8. PCIe reset recovery

<!-- claim:PCIE14-RESET -->

PCIe reset 來源包含 Base 定義的 controller/reset 流程與 PCIe 層級 reset。Recovery 設計要以 reset 類型判斷 controller property、queue 與 PCI configuration state。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.3, 文件頁 11-12, PDF 頁 11-12

### 9. PCIe command flow

<!-- claim:PCIE14-COMMAND -->

command flow 是：寫 SQE、更新 SQ tail doorbell、controller 取走與執行、寫 CQE、發出 interrupt（若啟用）、host 處理 CQE、更新 CQ head doorbell。doorbell 只通告 pointer，不攜帶 command 本體。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, 文件頁 12-13, PDF 頁 12-13

### 10. interrupt 模式與延遲

<!-- claim:PCIE14-INTERRUPT -->

可用模式為 pin-based、single-message MSI、multiple-message MSI 與 MSI-X。規格建議 MSI-X；coalescing 可降低 interrupt rate，但通常增加 latency。Admin CQ 的 interrupt 不宜（should not）延遲。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, 文件頁 13-16, PDF 頁 13-16

### 11. slot power limit

<!-- claim:PCIE14-POWER -->

host 絕不可（shall never）選擇功耗高於 PCIe slot power limit 的 NVMe power state；違反時 power behavior 未定義。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.6, 文件頁 16, PDF 頁 16

### 12. NVMe 與 PCIe error 分層

<!-- claim:PCIE14-ERROR -->

NVMe command error 由 CQE status 回報；PCIe transport／link error 則依 PCIe 機制與本文件的 NVMe-specific 要求處理，兩者的 recovery 層級不同。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, 文件頁 16, PDF 頁 16

### 13. PCI configuration requirements

<!-- claim:PCIE14-CONFIG -->

§3.8 逐欄定義 NVMe controller 的 PCI header、Power Management、MSI／MSI-X、PCIe capability 與 AER 額外要求。PCI／PCIe 原始欄位語意仍以 PCI-SIG 規格為準。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, 文件頁 16-35, PDF 頁 16-35

### 14. 平台安全與隔離依賴

<!-- claim:PCIE14-SECURITY -->

power-loss signaling、confidential computing 與 TDISP 把平台事件或隔離狀態映射到 NVMe controller 行為；實作仍需要本次未提供的外部 PCIe／TDISP 規格。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.8-3.8.10, 文件頁 35-39, PDF 頁 35-39

### 15. receiver eye measurement

<!-- claim:PCIE14-EOM -->

Physical Interface Receiver Eye Opening Measurement log page 以 header、lane descriptor 與 EOM data 回報量測；host 先查支援與大小，再依 lane／parameter 解析。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, 文件頁 39-46, PDF 頁 39-46

### 16. host implementation checklist

<!-- claim:PCIE14-HOST -->

Annex A 是 informative host checklist：提交時先寫 SQE 再 doorbell；完成時以 phase 判斷新 CQE，完成讀取後再推進 CQ head；interrupt handler 要處理同 vector 的所有相關 CQ。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, 文件頁 47-48, PDF 頁 47-48

## Figure 索引

本報告介紹全部 77 張納入範圍的 Figure。100 分鐘簡報以 section 主線與必講 Figure 為主，其餘 Figure 仍完整保留作為附錄。

- [§1.2](#section-1-2)

- [§2](#section-2)

- [§3.1](#section-3-1)

- [§3.2](#section-3-2)

- [§3.4](#section-3-4)

- [§3.5](#section-3-5)

- [§3.8](#section-3-8)

- [§3.9](#section-3-9)

## Figure 逐圖導讀

本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。欄位與 keyword 索引來自本機核對過的 PDF。

<a id="section-1-2"></a>

### §1.2

<details markdown="1">
<summary><strong>Figure 1: NVMe Family of Specifications</strong></summary>

<!-- claim:PCIE14-FIG-001-CLAIM figure-table:PCIE14-FIG-001 -->

Figure 1〈NVMe Family of Specifications〉：定位〈NVMe Family of Specifications〉在 NVMe 文件與 command set 階層中的位置。 由共通 Base 要求往 transport 與 command set 分支閱讀，並分開核對：NVMe Family。

- 解決的問題：定位〈NVMe Family of Specifications〉在 NVMe 文件與 command set 階層中的位置。

- 閱讀順序：由共通 Base 要求往 transport 與 command set 分支閱讀，並分開核對：NVMe Family。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。 本報告只解釋 PCIe／memory-based 部分。

- 說明性範例（informative example）：先從 NVMe Family 出發，再沿包含 引用條件 的分支找定義來源，不假設每一層都重複定義同一要求。 此例不新增規格要求。

- 來源欄位索引：NVMe Family

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, Figure 1, 文件頁 6, PDF 頁 6

</details>

<a id="section-2"></a>

### §2

<details markdown="1">
<summary><strong>Figure 2: Example of Transport Protocol Layers</strong></summary>

<!-- claim:PCIE14-FIG-002-CLAIM figure-table:PCIE14-FIG-002 -->

Figure 2〈Example of Transport Protocol Layers〉：分開〈Example of Transport Protocol Layers〉中各 protocol layer 的責任。 垂直按 layer、水平按 peer interaction 閱讀，不把 transport rule 歸到 Base layer；來源索引：Transport Protocol Layers。

- 解決的問題：分開〈Example of Transport Protocol Layers〉中各 protocol layer 的責任。

- 閱讀順序：垂直按 layer、水平按 peer interaction 閱讀，不把 transport rule 歸到 Base layer；來源索引：Transport Protocol Layers。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：先從 Transport Protocol Layers 出發，再沿操作追到 引用條件，最後引用真正定義該行為的 layer。 此例不新增規格要求。

- 來源欄位索引：Transport Protocol Layers

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, Figure 2, 文件頁 8, PDF 頁 8

</details>

<a id="section-3-1"></a>

### §3.1

<details markdown="1">
<summary><strong>Figure 3: PCI Express Registers</strong></summary>

<!-- claim:PCIE14-FIG-003-CLAIM figure-table:PCIE14-FIG-003 -->

Figure 3〈PCI Express Registers〉：定義〈PCI Express Registers〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PMCAP, MSICAP, MSIXCAP, MSIX, PXCAP, AERCAP, MSI, MLBAR。

- 解決的問題：定義〈PCI Express Registers〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PMCAP, MSICAP, MSIXCAP, MSIX, PXCAP, AERCAP, MSI, MLBAR。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `should`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 PMCAP 作為 parser 的第一個檢查點，再用 MSICAP 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：PMCAP, MSICAP, MSIXCAP, MSIX, PXCAP, AERCAP, MSI, MLBAR

- 來源 keyword 索引：`shall not`, `shall`, `should`, `may`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, Figure 3, 文件頁 9, PDF 頁 9

</details>

<details markdown="1">
<summary><strong>Figure 4: PCI Express Specific Controller Property Definitions</strong></summary>

<!-- claim:PCIE14-FIG-004-CLAIM figure-table:PCIE14-FIG-004 -->

Figure 4〈PCI Express Specific Controller Property Definitions〉：定義〈PCI Express Specific Controller Property Definitions〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：SQ0TDBL, CAP.DSTRD, CQ0HDBL, SQ1TDBL, CQ1HDBL, SQ2TDBL, CQ2HDBL, Controller。

- 解決的問題：定義〈PCI Express Specific Controller Property Definitions〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：SQ0TDBL, CAP.DSTRD, CQ0HDBL, SQ1TDBL, CQ1HDBL, SQ2TDBL, CQ2HDBL, Controller。

- 條件與限制：來源 keyword 索引：`optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 SQ0TDBL 作為 parser 的第一個檢查點，再用 CAP.DSTRD 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：SQ0TDBL, CAP.DSTRD, CQ0HDBL, SQ1TDBL, CQ1HDBL, SQ2TDBL, CQ2HDBL, Controller

- 來源 keyword 索引：`optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, Figure 4, 文件頁 9-10, PDF 頁 9-10

</details>

<details markdown="1">
<summary><strong>Figure 5: Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL - Submission Queue y Tail</strong></summary>

<!-- claim:PCIE14-FIG-005-CLAIM figure-table:PCIE14-FIG-005 -->

Figure 5〈Offset (1000h + ((2y) * (4 << CAP.DSTRD))): SQyTDBL - Submission Queue y Tail〉：呈現〈Offset (1000h + ((2y) * (4 << CAP.DSTRD))): SQyTDBL - Submission Queue y Tail〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：SQT, CAP.DSTRD, Submission Queue。

- 解決的問題：呈現〈Offset (1000h + ((2y) * (4 << CAP.DSTRD))): SQyTDBL - Submission Queue y Tail〉中的 queue 或 command 關係。

- 閱讀順序：沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：SQT, CAP.DSTRD, Submission Queue。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：沿 Figure 5 追蹤一筆 command，以 SQT 與 CAP.DSTRD 作為擁有者或 pointer 變動檢查點。 此例不新增規格要求。

- 來源欄位索引：SQT, CAP.DSTRD, Submission Queue

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1, Figure 5, 文件頁 10, PDF 頁 10

</details>

<details markdown="1">
<summary><strong>Figure 6: Offset (1000h + ((2y + 1) * (4 &lt;&lt; CAP.DSTRD))): CQyHDBL - Completion Queue y Head</strong></summary>

<!-- claim:PCIE14-FIG-006-CLAIM figure-table:PCIE14-FIG-006 -->

Figure 6〈Offset (1000h + ((2y + 1) * (4 << CAP.DSTRD))): CQyHDBL - Completion Queue y Head〉：呈現〈Offset (1000h + ((2y + 1) * (4 << CAP.DSTRD))): CQyHDBL - Completion Queue y Head〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：CQH, CAP.DSTRD, CC.PI, Completion Queue。

- 解決的問題：呈現〈Offset (1000h + ((2y + 1) * (4 << CAP.DSTRD))): CQyHDBL - Completion Queue y Head〉中的 queue 或 command 關係。

- 閱讀順序：沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：CQH, CAP.DSTRD, CC.PI, Completion Queue。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：沿 Figure 6 追蹤一筆 command，以 CQH 與 CAP.DSTRD 作為擁有者或 pointer 變動檢查點。 此例不新增規格要求。

- 來源欄位索引：CQH, CAP.DSTRD, CC.PI, Completion Queue

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1, Figure 6, 文件頁 10-11, PDF 頁 10-11

</details>

<a id="section-3-2"></a>

### §3.2

<details markdown="1">
<summary><strong>Figure 7: Create I/O Completion Queue - Command Dword 11</strong></summary>

<!-- claim:PCIE14-FIG-007-CLAIM figure-table:PCIE14-FIG-007 -->

Figure 7〈Create I/O Completion Queue - Command Dword 11〉：定義 Create I/O Completion Queue 在 CDW11 的 command-specific 欄位。 先定位 CDW11，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：IV, MSI, MSICAP.MC.MME, MSIXCAP.MXC.TS, Completion Queue, Command。

- 解決的問題：定義 Create I/O Completion Queue 在 CDW11 的 command-specific 欄位。

- 閱讀順序：先定位 CDW11，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：IV, MSI, MSICAP.MC.MME, MSIXCAP.MXC.TS, Completion Queue, Command。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `should`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：建立一筆 Create I/O Completion Queue，設定 IV 後再獨立驗證 MSI，確認完成才更新 Submission Queue doorbell。 此例不新增規格要求。

- 來源欄位索引：IV, MSI, MSICAP.MC.MME, MSIXCAP.MXC.TS, Completion Queue, Command

- 來源 keyword 索引：`shall not`, `shall`, `should`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, Figure 7, 文件頁 11, PDF 頁 11

</details>

<a id="section-3-4"></a>

### §3.4

<details markdown="1">
<summary><strong>Figure 8: Command Processing</strong></summary>

<!-- claim:PCIE14-FIG-008-CLAIM figure-table:PCIE14-FIG-008 -->

Figure 8〈Command Processing〉：呈現〈Command Processing〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：Command。

- 解決的問題：呈現〈Command Processing〉中的 queue 或 command 關係。

- 閱讀順序：沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：Command。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：沿 Figure 8 追蹤一筆 command，以 Command 與 引用條件 作為擁有者或 pointer 變動檢查點。 此例不新增規格要求。

- 來源欄位索引：Command

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4.1, Figure 8, 文件頁 13, PDF 頁 13

</details>

<a id="section-3-5"></a>

### §3.5

<details markdown="1">
<summary><strong>Figure 9: Pin Based, Single MSI, and Multiple MSI Behavior</strong></summary>

<!-- claim:PCIE14-FIG-009-CLAIM figure-table:PCIE14-FIG-009 -->

Figure 9〈Pin Based, Single MSI, and Multiple MSI Behavior〉：呈現〈Pin Based, Single MSI, and Multiple MSI Behavior〉中的 interrupt 傳遞或 masking 關係。 分開追蹤 vector／message 來源、mask 狀態與傳遞目的端；來源索引：MSI。

- 解決的問題：呈現〈Pin Based, Single MSI, and Multiple MSI Behavior〉中的 interrupt 傳遞或 masking 關係。

- 閱讀順序：分開追蹤 vector／message 來源、mask 狀態與傳遞目的端；來源索引：MSI。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選定 MSI 所代表的來源，再確認 引用條件 對應的 mask 或 vector 條件後才預期 interrupt 送達。 此例不新增規格要求。

- 來源欄位索引：MSI

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5.1, Figure 9, 文件頁 15, PDF 頁 15

</details>

<a id="section-3-8"></a>

### §3.8

<details markdown="1">
<summary><strong>Figure 10: PCI Express Type 0/1 Common Configuration Space</strong></summary>

<!-- claim:PCIE14-FIG-010-CLAIM figure-table:PCIE14-FIG-010 -->

Figure 10〈PCI Express Type 0/1 Common Configuration Space〉：定義〈PCI Express Type 0/1 Common Configuration Space〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PCI Express Type 0/1 Common Configuration Space。

- 解決的問題：定義〈PCI Express Type 0/1 Common Configuration Space〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PCI Express Type 0/1 Common Configuration Space。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：以 PCI Express Type 0/1 Common Configuration Space 作為 parser 的第一個檢查點，再用 引用條件 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：PCI Express Type 0/1 Common Configuration Space

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8, Figure 10, 文件頁 16-17, PDF 頁 16-17

</details>

<details markdown="1">
<summary><strong>Figure 11: Offset 00h: ID - Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-011-CLAIM figure-table:PCIE14-FIG-011 -->

Figure 11〈Offset 00h: ID - Identifiers〉：定義 offset 00h 的 ID（Identifiers），並指出軟體在該位置必須分別解碼的欄位。 先定位 ID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ID, DID, VID。

- 解決的問題：定義 offset 00h 的 ID（Identifiers），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 ID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ID, DID, VID。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 ID，先獨立驗證 ID，再驗證 DID，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：ID, DID, VID

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.1, Figure 11, 文件頁 17, PDF 頁 17

</details>

<details markdown="1">
<summary><strong>Figure 12: Offset 04h: CMD - Command</strong></summary>

<!-- claim:PCIE14-FIG-012-CLAIM figure-table:PCIE14-FIG-012 -->

Figure 12〈Offset 04h: CMD - Command〉：定義 offset 04h 的 CMD（Command），並指出軟體在該位置必須分別解碼的欄位。 先定位 CMD，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CMD, SIG, ID, FBE, SERR, SEE, IDSEL, ISWCC。

- 解決的問題：定義 offset 04h 的 CMD（Command），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 CMD，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CMD, SIG, ID, FBE, SERR, SEE, IDSEL, ISWCC。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 CMD，先獨立驗證 CMD，再驗證 SIG，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：CMD, SIG, ID, FBE, SERR, SEE, IDSEL, ISWCC

- 來源 keyword 索引：`reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.2, Figure 12, 文件頁 17, PDF 頁 17

</details>

<details markdown="1">
<summary><strong>Figure 13: Offset 06h: STS - Device Status</strong></summary>

<!-- claim:PCIE14-FIG-013-CLAIM figure-table:PCIE14-FIG-013 -->

Figure 13〈Offset 06h: STS - Device Status〉：定義 offset 06h 的 STS（Device Status），並指出軟體在該位置必須分別解碼的欄位。 先定位 STS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：STS, DPE, SSE, RMA, RTA, STA, DEVSEL, DEVT。

- 解決的問題：定義 offset 06h 的 STS（Device Status），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 STS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：STS, DPE, SSE, RMA, RTA, STA, DEVSEL, DEVT。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 STS，先獨立驗證 STS，再驗證 DPE，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：STS, DPE, SSE, RMA, RTA, STA, DEVSEL, DEVT

- 來源 keyword 索引：`reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.3, Figure 13, 文件頁 18, PDF 頁 18

</details>

<details markdown="1">
<summary><strong>Figure 14: Offset 08h: RID - Revision ID</strong></summary>

<!-- claim:PCIE14-FIG-014-CLAIM figure-table:PCIE14-FIG-014 -->

Figure 14〈Offset 08h: RID - Revision ID〉：定義 offset 08h 的 RID（Revision ID），並指出軟體在該位置必須分別解碼的欄位。 先定位 RID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：RID, ID。

- 解決的問題：定義 offset 08h 的 RID（Revision ID），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 RID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：RID, ID。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 RID，先獨立驗證 RID，再驗證 ID，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：RID, ID

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.4, Figure 14, 文件頁 18, PDF 頁 18

</details>

<details markdown="1">
<summary><strong>Figure 15: Offset 09h: CC - Class Code</strong></summary>

<!-- claim:PCIE14-FIG-015-CLAIM figure-table:PCIE14-FIG-015 -->

Figure 15〈Offset 09h: CC - Class Code〉：定義 offset 09h 的 CC（Class Code），並指出軟體在該位置必須分別解碼的欄位。 先定位 CC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CC, BCC, SCC, PI。

- 解決的問題：定義 offset 09h 的 CC（Class Code），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 CC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CC, BCC, SCC, PI。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 CC，先獨立驗證 CC，再驗證 BCC，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：CC, BCC, SCC, PI

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.5, Figure 15, 文件頁 18, PDF 頁 18

</details>

<details markdown="1">
<summary><strong>Figure 16: Offset 0Ch: CLS - Cache Line Size</strong></summary>

<!-- claim:PCIE14-FIG-016-CLAIM figure-table:PCIE14-FIG-016 -->

Figure 16〈Offset 0Ch: CLS - Cache Line Size〉：定義 offset 0Ch 的 CLS（Cache Line Size），並指出軟體在該位置必須分別解碼的欄位。 先定位 CLS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CLS。

- 解決的問題：定義 offset 0Ch 的 CLS（Cache Line Size），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 CLS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CLS。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 CLS，先獨立驗證 CLS，再驗證 引用條件，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：CLS

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.6, Figure 16, 文件頁 18, PDF 頁 18

</details>

<details markdown="1">
<summary><strong>Figure 17: Offset 0Dh: MLT - Master Latency Timer</strong></summary>

<!-- claim:PCIE14-FIG-017-CLAIM figure-table:PCIE14-FIG-017 -->

Figure 17〈Offset 0Dh: MLT - Master Latency Timer〉：定義 offset 0Dh 的 MLT（Master Latency Timer），並指出軟體在該位置必須分別解碼的欄位。 先定位 MLT，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：MLT。

- 解決的問題：定義 offset 0Dh 的 MLT（Master Latency Timer），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 MLT，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：MLT。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 MLT，先獨立驗證 MLT，再驗證 引用條件，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：MLT

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.7, Figure 17, 文件頁 18, PDF 頁 18

</details>

<details markdown="1">
<summary><strong>Figure 18: Offset 0Eh: HTYPE - Header Type</strong></summary>

<!-- claim:PCIE14-FIG-018-CLAIM figure-table:PCIE14-FIG-018 -->

Figure 18〈Offset 0Eh: HTYPE - Header Type〉：定義 offset 0Eh 的 HTYPE（Header Type），並指出軟體在該位置必須分別解碼的欄位。 先定位 HTYPE，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：HTYPE, MFD, HL。

- 解決的問題：定義 offset 0Eh 的 HTYPE（Header Type），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 HTYPE，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：HTYPE, MFD, HL。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 HTYPE，先獨立驗證 HTYPE，再驗證 MFD，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：HTYPE, MFD, HL

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.8, Figure 18, 文件頁 19, PDF 頁 19

</details>

<details markdown="1">
<summary><strong>Figure 19: Offset 0Fh: BIST - Built-In Self Test (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-019-CLAIM figure-table:PCIE14-FIG-019 -->

Figure 19〈Offset 0Fh: BIST - Built-In Self Test (Optional)〉：定義 offset 0Fh 的 BIST（Built-In Self Test (Optional)），並指出軟體在該位置必須分別解碼的欄位。 先定位 BIST，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：BIST, BC, SB, SIG, CC。

- 解決的問題：定義 offset 0Fh 的 BIST（Built-In Self Test (Optional)），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 BIST，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：BIST, BC, SB, SIG, CC。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 BIST，先獨立驗證 BIST，再驗證 BC，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：BIST, BC, SB, SIG, CC

- 來源 keyword 索引：`reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.9, Figure 19, 文件頁 19, PDF 頁 19

</details>

<details markdown="1">
<summary><strong>Figure 20: Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits</strong></summary>

<!-- claim:PCIE14-FIG-020-CLAIM figure-table:PCIE14-FIG-020 -->

Figure 20〈Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits〉：定義〈Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：BA, PF, TP, RTE, MLBAR, BAR0, SIG。

- 解決的問題：定義〈Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：BA, PF, TP, RTE, MLBAR, BAR0, SIG。

- 條件與限制：來源 keyword 索引：`may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 BA 作為 parser 的第一個檢查點，再用 PF 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：BA, PF, TP, RTE, MLBAR, BAR0, SIG

- 來源 keyword 索引：`may`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.10, Figure 20, 文件頁 19, PDF 頁 19

</details>

<details markdown="1">
<summary><strong>Figure 21: Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits</strong></summary>

<!-- claim:PCIE14-FIG-021-CLAIM figure-table:PCIE14-FIG-021 -->

Figure 21〈Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits〉：定義〈Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：BA, MUBAR, BAR1。

- 解決的問題：定義〈Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：BA, MUBAR, BAR1。

- 條件與限制：來源 keyword 索引：`may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 BA 作為 parser 的第一個檢查點，再用 MUBAR 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：BA, MUBAR, BAR1

- 來源 keyword 索引：`may`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.11, Figure 21, 文件頁 19, PDF 頁 19

</details>

<details markdown="1">
<summary><strong>Figure 22: Offset 18h: BAR2 - Index/Data Pair Register Base Address or Vendor Specific</strong></summary>

<!-- claim:PCIE14-FIG-022-CLAIM figure-table:PCIE14-FIG-022 -->

Figure 22〈Offset 18h: BAR2 - Index/Data Pair Register Base Address or Vendor Specific〉：定義 offset 18h 的 BAR2（Index/Data Pair Register Base Address or Vendor Specific），並指出軟體在該位置必須分別解碼的欄位。 先定位 BAR2，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：BA, RTE, BAR2。

- 解決的問題：定義 offset 18h 的 BAR2（Index/Data Pair Register Base Address or Vendor Specific），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 BAR2，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：BA, RTE, BAR2。

- 條件與限制：來源 keyword 索引：`may`, `optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 BAR2，先獨立驗證 BA，再驗證 RTE，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：BA, RTE, BAR2

- 來源 keyword 索引：`may`, `optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.12, Figure 22, 文件頁 20, PDF 頁 20

</details>

<details markdown="1">
<summary><strong>Figure 23: Offset 28h: CCPTR - CardBus CIS Pointer</strong></summary>

<!-- claim:PCIE14-FIG-023-CLAIM figure-table:PCIE14-FIG-023 -->

Figure 23〈Offset 28h: CCPTR - CardBus CIS Pointer〉：定義 offset 28h 的 CCPTR（CardBus CIS Pointer），並指出軟體在該位置必須分別解碼的欄位。 先定位 CCPTR，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CCPTR, CIS。

- 解決的問題：定義 offset 28h 的 CCPTR（CardBus CIS Pointer），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 CCPTR，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CCPTR, CIS。

- 條件與限制：來源 keyword 索引：`shall`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 CCPTR，先獨立驗證 CCPTR，再驗證 CIS，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：CCPTR, CIS

- 來源 keyword 索引：`shall`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.16, Figure 23, 文件頁 20, PDF 頁 20

</details>

<details markdown="1">
<summary><strong>Figure 24: Offset 2Ch: SS - Subsystem Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-024-CLAIM figure-table:PCIE14-FIG-024 -->

Figure 24〈Offset 2Ch: SS - Subsystem Identifiers〉：定義 offset 2Ch 的 SS（Subsystem Identifiers），並指出軟體在該位置必須分別解碼的欄位。 先定位 SS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：SSID, SSVID, SS, ID。

- 解決的問題：定義 offset 2Ch 的 SS（Subsystem Identifiers），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 SS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：SSID, SSVID, SS, ID。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 SS，先獨立驗證 SSID，再驗證 SSVID，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：SSID, SSVID, SS, ID

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.17, Figure 24, 文件頁 20, PDF 頁 20

</details>

<details markdown="1">
<summary><strong>Figure 25: Offset 30h: EROM - Expansion ROM (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-025-CLAIM figure-table:PCIE14-FIG-025 -->

Figure 25〈Offset 30h: EROM - Expansion ROM (Optional)〉：定義 offset 30h 的 EROM（Expansion ROM (Optional)），並指出軟體在該位置必須分別解碼的欄位。 先定位 EROM，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：RBA, EROM, ROM。

- 解決的問題：定義 offset 30h 的 EROM（Expansion ROM (Optional)），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 EROM，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：RBA, EROM, ROM。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 EROM，先獨立驗證 RBA，再驗證 EROM，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：RBA, EROM, ROM

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.18, Figure 25, 文件頁 20, PDF 頁 20

</details>

<details markdown="1">
<summary><strong>Figure 26: Offset 34h: CAP - Capabilities Pointer</strong></summary>

<!-- claim:PCIE14-FIG-026-CLAIM figure-table:PCIE14-FIG-026 -->

Figure 26〈Offset 34h: CAP - Capabilities Pointer〉：定義 offset 34h 的 CAP（Capabilities Pointer），並指出軟體在該位置必須分別解碼的欄位。 先定位 CAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CP, CAP。

- 解決的問題：定義 offset 34h 的 CAP（Capabilities Pointer），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 CAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CP, CAP。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 CAP，先獨立驗證 CP，再驗證 CAP，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：CP, CAP

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.19, Figure 26, 文件頁 21, PDF 頁 21

</details>

<details markdown="1">
<summary><strong>Figure 27: Offset 3Ch: INTR - Interrupt Information</strong></summary>

<!-- claim:PCIE14-FIG-027-CLAIM figure-table:PCIE14-FIG-027 -->

Figure 27〈Offset 3Ch: INTR - Interrupt Information〉：定義 offset 3Ch 的 INTR（Interrupt Information），並指出軟體在該位置必須分別解碼的欄位。 先定位 INTR，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：IPIN, ILINE, INTR, Interrupt。

- 解決的問題：定義 offset 3Ch 的 INTR（Interrupt Information），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 INTR，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：IPIN, ILINE, INTR, Interrupt。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 INTR，先獨立驗證 IPIN，再驗證 ILINE，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：IPIN, ILINE, INTR, Interrupt

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.20, Figure 27, 文件頁 21, PDF 頁 21

</details>

<details markdown="1">
<summary><strong>Figure 28: Offset 3Eh: MGNT - Minimum Grant</strong></summary>

<!-- claim:PCIE14-FIG-028-CLAIM figure-table:PCIE14-FIG-028 -->

Figure 28〈Offset 3Eh: MGNT - Minimum Grant〉：定義 offset 3Eh 的 MGNT（Minimum Grant），並指出軟體在該位置必須分別解碼的欄位。 先定位 MGNT，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：GNT, MGNT。

- 解決的問題：定義 offset 3Eh 的 MGNT（Minimum Grant），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 MGNT，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：GNT, MGNT。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 MGNT，先獨立驗證 GNT，再驗證 MGNT，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：GNT, MGNT

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.21, Figure 28, 文件頁 21, PDF 頁 21

</details>

<details markdown="1">
<summary><strong>Figure 29: Offset 3Fh: MLAT - Maximum Latency</strong></summary>

<!-- claim:PCIE14-FIG-029-CLAIM figure-table:PCIE14-FIG-029 -->

Figure 29〈Offset 3Fh: MLAT - Maximum Latency〉：定義 offset 3Fh 的 MLAT（Maximum Latency），並指出軟體在該位置必須分別解碼的欄位。 先定位 MLAT，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：LAT, MLAT, CC。

- 解決的問題：定義 offset 3Fh 的 MLAT（Maximum Latency），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 MLAT，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：LAT, MLAT, CC。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 MLAT，先獨立驗證 LAT，再驗證 MLAT，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：LAT, MLAT, CC

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.22, Figure 29, 文件頁 21, PDF 頁 21

</details>

<details markdown="1">
<summary><strong>Figure 30: PCI Power Management Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-030-CLAIM figure-table:PCIE14-FIG-030 -->

Figure 30〈PCI Power Management Capabilities〉：定義〈PCI Power Management Capabilities〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PMCAP, PID, ID, PC, PMCS。

- 解決的問題：定義〈PCI Power Management Capabilities〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PMCAP, PID, ID, PC, PMCS。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：以 PMCAP 作為 parser 的第一個檢查點，再用 PID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：PMCAP, PID, ID, PC, PMCS

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.22, Figure 30, 文件頁 21, PDF 頁 21

</details>

<details markdown="1">
<summary><strong>Figure 31: Offset PMCAP: PID - PCI Power Management Capability ID</strong></summary>

<!-- claim:PCIE14-FIG-031-CLAIM figure-table:PCIE14-FIG-031 -->

Figure 31〈Offset PMCAP: PID - PCI Power Management Capability ID〉：定義 offset PMCAP 的 PID（PCI Power Management Capability ID），並指出軟體在該位置必須分別解碼的欄位。 先定位 PID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NEXT, CID, PMCAP, PID, ID。

- 解決的問題：定義 offset PMCAP 的 PID（PCI Power Management Capability ID），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NEXT, CID, PMCAP, PID, ID。

- 條件與限制：來源 keyword 索引：`may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PID，先獨立驗證 NEXT，再驗證 CID，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：NEXT, CID, PMCAP, PID, ID

- 來源 keyword 索引：`may`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.1, Figure 31, 文件頁 21, PDF 頁 21

</details>

<details markdown="1">
<summary><strong>Figure 32: Offset PMCAP + 2h: PC - PCI Power Management Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-032-CLAIM figure-table:PCIE14-FIG-032 -->

Figure 32〈Offset PMCAP + 2h: PC - PCI Power Management Capabilities〉：定義 offset PMCAP + 2h 的 PC（PCI Power Management Capabilities），並指出軟體在該位置必須分別解碼的欄位。 先定位 PC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PSUP, D2S, D1S, AUXC, DSI, PMEC, VS, PMCAP。

- 解決的問題：定義 offset PMCAP + 2h 的 PC（PCI Power Management Capabilities），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PSUP, D2S, D1S, AUXC, DSI, PMEC, VS, PMCAP。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PC，先獨立驗證 PSUP，再驗證 D2S，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：PSUP, D2S, D1S, AUXC, DSI, PMEC, VS, PMCAP

- 來源 keyword 索引：`reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.2, Figure 32, 文件頁 22, PDF 頁 22

</details>

<details markdown="1">
<summary><strong>Figure 33: Offset PMCAP + 4h: PMCS - PCI Power Management Control and Status</strong></summary>

<!-- claim:PCIE14-FIG-033-CLAIM figure-table:PCIE14-FIG-033 -->

Figure 33〈Offset PMCAP + 4h: PMCS - PCI Power Management Control and Status〉：定義 offset PMCAP + 4h 的 PMCS（PCI Power Management Control and Status），並指出軟體在該位置必須分別解碼的欄位。 先定位 PMCS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PMES, DSC, DSE, PMEE, NSFRST, PS, PMCAP, PMCS。

- 解決的問題：定義 offset PMCAP + 4h 的 PMCS（PCI Power Management Control and Status），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PMCS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PMES, DSC, DSE, PMEE, NSFRST, PS, PMCAP, PMCS。

- 條件與限制：來源 keyword 索引：`optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PMCS，先獨立驗證 PMES，再驗證 DSC，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：PMES, DSC, DSE, PMEE, NSFRST, PS, PMCAP, PMCS

- 來源 keyword 索引：`optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.3, Figure 33, 文件頁 22, PDF 頁 22

</details>

<details markdown="1">
<summary><strong>Figure 34: Message Signaled Interrupt Capability (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-034-CLAIM figure-table:PCIE14-FIG-034 -->

Figure 34〈Message Signaled Interrupt Capability (Optional)〉：定義〈Message Signaled Interrupt Capability (Optional)〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MSICAP, MID, ID, MC, MA, MUA, MD, MMASK。

- 解決的問題：定義〈Message Signaled Interrupt Capability (Optional)〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MSICAP, MID, ID, MC, MA, MUA, MD, MMASK。

- 條件與限制：來源 keyword 索引：`optional`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 MSICAP 作為 parser 的第一個檢查點，再用 MID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：MSICAP, MID, ID, MC, MA, MUA, MD, MMASK

- 來源 keyword 索引：`optional`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.3, Figure 34, 文件頁 22, PDF 頁 22

</details>

<details markdown="1">
<summary><strong>Figure 35: Offset MSICAP: MID - Message Signaled Interrupt Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-035-CLAIM figure-table:PCIE14-FIG-035 -->

Figure 35〈Offset MSICAP: MID - Message Signaled Interrupt Identifiers〉：定義 offset MSICAP 的 MID（Message Signaled Interrupt Identifiers），並指出軟體在該位置必須分別解碼的欄位。 先定位 MID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NEXT, CID, MSICAP, MID, ID, MSI, Interrupt。

- 解決的問題：定義 offset MSICAP 的 MID（Message Signaled Interrupt Identifiers），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 MID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NEXT, CID, MSICAP, MID, ID, MSI, Interrupt。

- 條件與限制：來源 keyword 索引：`may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 MID，先獨立驗證 NEXT，再驗證 CID，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：NEXT, CID, MSICAP, MID, ID, MSI, Interrupt

- 來源 keyword 索引：`may`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.1, Figure 35, 文件頁 23, PDF 頁 23

</details>

<details markdown="1">
<summary><strong>Figure 36: Offset MSICAP + 2h: MC - Message Signaled Interrupt Message Control</strong></summary>

<!-- claim:PCIE14-FIG-036-CLAIM figure-table:PCIE14-FIG-036 -->

Figure 36〈Offset MSICAP + 2h: MC - Message Signaled Interrupt Message Control〉：定義 offset MSICAP + 2h 的 MC（Message Signaled Interrupt Message Control），並指出軟體在該位置必須分別解碼的欄位。 先定位 MC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PVM, C64, MME, MMC, MSIE, MSICAP, MC, MSI。

- 解決的問題：定義 offset MSICAP + 2h 的 MC（Message Signaled Interrupt Message Control），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 MC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PVM, C64, MME, MMC, MSIE, MSICAP, MC, MSI。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 MC，先獨立驗證 PVM，再驗證 C64，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：PVM, C64, MME, MMC, MSIE, MSICAP, MC, MSI

- 來源 keyword 索引：`shall`, `should`, `may`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.2, Figure 36, 文件頁 23, PDF 頁 23

</details>

<details markdown="1">
<summary><strong>Figure 37: Offset MSICAP + 4h: MA - Message Signaled Interrupt Message Address</strong></summary>

<!-- claim:PCIE14-FIG-037-CLAIM figure-table:PCIE14-FIG-037 -->

Figure 37〈Offset MSICAP + 4h: MA - Message Signaled Interrupt Message Address〉：定義 offset MSICAP + 4h 的 MA（Message Signaled Interrupt Message Address），並指出軟體在該位置必須分別解碼的欄位。 先定位 MA，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ADDR, MSICAP, MA, SIG, Interrupt。

- 解決的問題：定義 offset MSICAP + 4h 的 MA（Message Signaled Interrupt Message Address），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 MA，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ADDR, MSICAP, MA, SIG, Interrupt。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 MA，先獨立驗證 ADDR，再驗證 MSICAP，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：ADDR, MSICAP, MA, SIG, Interrupt

- 來源 keyword 索引：`reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.3, Figure 37, 文件頁 23, PDF 頁 23

</details>

<details markdown="1">
<summary><strong>Figure 38: Offset MSICAP + 8h: MUA - Message Signaled Interrupt Upper Address</strong></summary>

<!-- claim:PCIE14-FIG-038-CLAIM figure-table:PCIE14-FIG-038 -->

Figure 38〈Offset MSICAP + 8h: MUA - Message Signaled Interrupt Upper Address〉：定義 offset MSICAP + 8h 的 MUA（Message Signaled Interrupt Upper Address），並指出軟體在該位置必須分別解碼的欄位。 先定位 MUA，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：UADDR, MSICAP, MUA, MSI, Interrupt。

- 解決的問題：定義 offset MSICAP + 8h 的 MUA（Message Signaled Interrupt Upper Address），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 MUA，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：UADDR, MSICAP, MUA, MSI, Interrupt。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 MUA，先獨立驗證 UADDR，再驗證 MSICAP，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：UADDR, MSICAP, MUA, MSI, Interrupt

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.4, Figure 38, 文件頁 23, PDF 頁 23

</details>

<details markdown="1">
<summary><strong>Figure 39: Offset MSICAP + Ch: MD - Message Signaled Interrupt Message Data</strong></summary>

<!-- claim:PCIE14-FIG-039-CLAIM figure-table:PCIE14-FIG-039 -->

Figure 39〈Offset MSICAP + Ch: MD - Message Signaled Interrupt Message Data〉：定義 offset MSICAP + Ch 的 MD（Message Signaled Interrupt Message Data），並指出軟體在該位置必須分別解碼的欄位。 先定位 MD，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：DATA, MSICAP, MD, MSI, AD, Interrupt。

- 解決的問題：定義 offset MSICAP + Ch 的 MD（Message Signaled Interrupt Message Data），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 MD，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：DATA, MSICAP, MD, MSI, AD, Interrupt。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 MD，先獨立驗證 DATA，再驗證 MSICAP，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：DATA, MSICAP, MD, MSI, AD, Interrupt

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.5, Figure 39, 文件頁 23, PDF 頁 23

</details>

<details markdown="1">
<summary><strong>Figure 40: Offset MSICAP + 10h: MMASK - Message Signaled Interrupt Mask Bits (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-040-CLAIM figure-table:PCIE14-FIG-040 -->

Figure 40〈Offset MSICAP + 10h: MMASK - Message Signaled Interrupt Mask Bits (Optional)〉：定義 offset MSICAP + 10h 的 MMASK（Message Signaled Interrupt Mask Bits (Optional)），並指出軟體在該位置必須分別解碼的欄位。 先定位 MMASK，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：MASK, MSICAP, MMASK, Interrupt。

- 解決的問題：定義 offset MSICAP + 10h 的 MMASK（Message Signaled Interrupt Mask Bits (Optional)），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 MMASK，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：MASK, MSICAP, MMASK, Interrupt。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 MMASK，先獨立驗證 MASK，再驗證 MSICAP，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：MASK, MSICAP, MMASK, Interrupt

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.6, Figure 40, 文件頁 24, PDF 頁 24

</details>

<details markdown="1">
<summary><strong>Figure 41: Offset MSICAP + 14h: MPEND - Message Signaled Interrupt Pending Bits (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-041-CLAIM figure-table:PCIE14-FIG-041 -->

Figure 41〈Offset MSICAP + 14h: MPEND - Message Signaled Interrupt Pending Bits (Optional)〉：定義 offset MSICAP + 14h 的 MPEND（Message Signaled Interrupt Pending Bits (Optional)），並指出軟體在該位置必須分別解碼的欄位。 先定位 MPEND，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PEND, MSICAP, MPEND, MSIX, Interrupt。

- 解決的問題：定義 offset MSICAP + 14h 的 MPEND（Message Signaled Interrupt Pending Bits (Optional)），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 MPEND，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PEND, MSICAP, MPEND, MSIX, Interrupt。

- 條件與限制：來源 keyword 索引：`optional`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 MPEND，先獨立驗證 PEND，再驗證 MSICAP，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：PEND, MSICAP, MPEND, MSIX, Interrupt

- 來源 keyword 索引：`optional`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.7, Figure 41, 文件頁 24, PDF 頁 24

</details>

<details markdown="1">
<summary><strong>Figure 42: MSI-X Capability (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-042-CLAIM figure-table:PCIE14-FIG-042 -->

Figure 42〈MSI-X Capability (Optional)〉：定義〈MSI-X Capability (Optional)〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MSIX, MSIXCAP, MXID, ID, MXC, MTAB, BIR, MPBA。

- 解決的問題：定義〈MSI-X Capability (Optional)〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MSIX, MSIXCAP, MXID, ID, MXC, MTAB, BIR, MPBA。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `should`, `may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 MSIX 作為 parser 的第一個檢查點，再用 MSIXCAP 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：MSIX, MSIXCAP, MXID, ID, MXC, MTAB, BIR, MPBA

- 來源 keyword 索引：`shall not`, `shall`, `should`, `may`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.7, Figure 42, 文件頁 24, PDF 頁 24

</details>

<details markdown="1">
<summary><strong>Figure 43: Offset MSIXCAP: MXID - MSI-X Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-043-CLAIM figure-table:PCIE14-FIG-043 -->

Figure 43〈Offset MSIXCAP: MXID - MSI-X Identifiers〉：定義 offset MSIXCAP 的 MXID（MSI-X Identifiers），並指出軟體在該位置必須分別解碼的欄位。 先定位 MXID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NEXT, CID, MSIXCAP, MXID, MSIX, ID。

- 解決的問題：定義 offset MSIXCAP 的 MXID（MSI-X Identifiers），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 MXID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NEXT, CID, MSIXCAP, MXID, MSIX, ID。

- 條件與限制：來源 keyword 索引：`may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 MXID，先獨立驗證 NEXT，再驗證 CID，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：NEXT, CID, MSIXCAP, MXID, MSIX, ID

- 來源 keyword 索引：`may`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.1, Figure 43, 文件頁 24, PDF 頁 24

</details>

<details markdown="1">
<summary><strong>Figure 44: Offset MSIXCAP + 2h: MXC - MSI-X Message Control</strong></summary>

<!-- claim:PCIE14-FIG-044-CLAIM figure-table:PCIE14-FIG-044 -->

Figure 44〈Offset MSIXCAP + 2h: MXC - MSI-X Message Control〉：定義 offset MSIXCAP + 2h 的 MXC（MSI-X Message Control），並指出軟體在該位置必須分別解碼的欄位。 先定位 MXC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：MXE, FM, TS, MSIXCAP, MXC, MSIX, MSI, SIG。

- 解決的問題：定義 offset MSIXCAP + 2h 的 MXC（MSI-X Message Control），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 MXC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：MXE, FM, TS, MSIXCAP, MXC, MSIX, MSI, SIG。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 MXC，先獨立驗證 MXE，再驗證 FM，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：MXE, FM, TS, MSIXCAP, MXC, MSIX, MSI, SIG

- 來源 keyword 索引：`reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.2, Figure 44, 文件頁 24-25, PDF 頁 24-25

</details>

<details markdown="1">
<summary><strong>Figure 45: Offset MSIXCAP + 4h: MTAB - MSI-X Table Offset / Table BIR</strong></summary>

<!-- claim:PCIE14-FIG-045-CLAIM figure-table:PCIE14-FIG-045 -->

Figure 45〈Offset MSIXCAP + 4h: MTAB - MSI-X Table Offset / Table BIR〉：定義 offset MSIXCAP + 4h 的 MTAB（MSI-X Table Offset / Table BIR），並指出軟體在該位置必須分別解碼的欄位。 先定位 MTAB，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：TO, TBIR, MSIXCAP, MTAB, MSIX, BIR, MSI, BAR。

- 解決的問題：定義 offset MSIXCAP + 4h 的 MTAB（MSI-X Table Offset / Table BIR），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 MTAB，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：TO, TBIR, MSIXCAP, MTAB, MSIX, BIR, MSI, BAR。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 MTAB，先獨立驗證 TO，再驗證 TBIR，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：TO, TBIR, MSIXCAP, MTAB, MSIX, BIR, MSI, BAR

- 來源 keyword 索引：`reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.3, Figure 45, 文件頁 25, PDF 頁 25

</details>

<details markdown="1">
<summary><strong>Figure 46: Offset MSIXCAP + 8h: MPBA - MSI-X PBA Offset / PBA BIR</strong></summary>

<!-- claim:PCIE14-FIG-046-CLAIM figure-table:PCIE14-FIG-046 -->

Figure 46〈Offset MSIXCAP + 8h: MPBA - MSI-X PBA Offset / PBA BIR〉：定義 offset MSIXCAP + 8h 的 MPBA（MSI-X PBA Offset / PBA BIR），並指出軟體在該位置必須分別解碼的欄位。 先定位 MPBA，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PBAO, PBIR, MSIXCAP, MPBA, MSIX, PBA, BIR, MSI。

- 解決的問題：定義 offset MSIXCAP + 8h 的 MPBA（MSI-X PBA Offset / PBA BIR），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 MPBA，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PBAO, PBIR, MSIXCAP, MPBA, MSIX, PBA, BIR, MSI。

- 條件與限制：來源 keyword 索引：`may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 MPBA，先獨立驗證 PBAO，再驗證 PBIR，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：PBAO, PBIR, MSIXCAP, MPBA, MSIX, PBA, BIR, MSI

- 來源 keyword 索引：`may`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.4, Figure 46, 文件頁 25, PDF 頁 25

</details>

<details markdown="1">
<summary><strong>Figure 47: PCI Express Capability</strong></summary>

<!-- claim:PCIE14-FIG-047-CLAIM figure-table:PCIE14-FIG-047 -->

Figure 47〈PCI Express Capability〉：定義〈PCI Express Capability〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PXCAP, PXID, ID, PXDCAP, PXDC, PXDS, PXLCAP, PXLC。

- 解決的問題：定義〈PCI Express Capability〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PXCAP, PXID, ID, PXDCAP, PXDC, PXDS, PXLCAP, PXLC。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：以 PXCAP 作為 parser 的第一個檢查點，再用 PXID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：PXCAP, PXID, ID, PXDCAP, PXDC, PXDS, PXLCAP, PXLC

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5, Figure 47, 文件頁 26, PDF 頁 26

</details>

<details markdown="1">
<summary><strong>Figure 48: Offset PXCAP: PXID - PCI Express Capability ID</strong></summary>

<!-- claim:PCIE14-FIG-048-CLAIM figure-table:PCIE14-FIG-048 -->

Figure 48〈Offset PXCAP: PXID - PCI Express Capability ID〉：定義 offset PXCAP 的 PXID（PCI Express Capability ID），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NEXT, CID, PXCAP, PXID, ID。

- 解決的問題：定義 offset PXCAP 的 PXID（PCI Express Capability ID），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PXID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NEXT, CID, PXCAP, PXID, ID。

- 條件與限制：來源 keyword 索引：`may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PXID，先獨立驗證 NEXT，再驗證 CID，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：NEXT, CID, PXCAP, PXID, ID

- 來源 keyword 索引：`may`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.1, Figure 48, 文件頁 26, PDF 頁 26

</details>

<details markdown="1">
<summary><strong>Figure 49: Offset PXCAP + 2h: PXCAP - PCI Express Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-049-CLAIM figure-table:PCIE14-FIG-049 -->

Figure 49〈Offset PXCAP + 2h: PXCAP - PCI Express Capabilities〉：定義 offset PXCAP + 2h 的 PXCAP（PCI Express Capabilities），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXCAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：IMN, SI, DPT, VER, PXCAP, SIG, MSI。

- 解決的問題：定義 offset PXCAP + 2h 的 PXCAP（PCI Express Capabilities），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PXCAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：IMN, SI, DPT, VER, PXCAP, SIG, MSI。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PXCAP，先獨立驗證 IMN，再驗證 SI，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：IMN, SI, DPT, VER, PXCAP, SIG, MSI

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.2, Figure 49, 文件頁 26, PDF 頁 26

</details>

<details markdown="1">
<summary><strong>Figure 50: Offset PXCAP + 4h: PXDCAP - PCI Express Device Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-050-CLAIM figure-table:PCIE14-FIG-050 -->

Figure 50〈Offset PXCAP + 4h: PXDCAP - PCI Express Device Capabilities〉：定義 offset PXCAP + 4h 的 PXDCAP（PCI Express Device Capabilities），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXDCAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：FLRC, CSPLS, CSPLV, RER, L1L, L0SL, ETFS, PFS。

- 解決的問題：定義 offset PXCAP + 4h 的 PXDCAP（PCI Express Device Capabilities），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PXDCAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：FLRC, CSPLS, CSPLV, RER, L1L, L0SL, ETFS, PFS。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PXDCAP，先獨立驗證 FLRC，再驗證 CSPLS，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：FLRC, CSPLS, CSPLV, RER, L1L, L0SL, ETFS, PFS

- 來源 keyword 索引：`shall`, `may`, `optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.3, Figure 50, 文件頁 26-27, PDF 頁 26-27

</details>

<details markdown="1">
<summary><strong>Figure 51: Offset PXCAP + 8h: PXDC - PCI Express Device Control</strong></summary>

<!-- claim:PCIE14-FIG-051-CLAIM figure-table:PCIE14-FIG-051 -->

Figure 51〈Offset PXCAP + 8h: PXDC - PCI Express Device Control〉：定義 offset PXCAP + 8h 的 PXDC（PCI Express Device Control），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXDC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：IFLR, MRRS, ENS, APPME, PFE, ETE, MPS, ERO。

- 解決的問題：定義 offset PXCAP + 8h 的 PXDC（PCI Express Device Control），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PXDC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：IFLR, MRRS, ENS, APPME, PFE, ETE, MPS, ERO。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PXDC，先獨立驗證 IFLR，再驗證 MRRS，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：IFLR, MRRS, ENS, APPME, PFE, ETE, MPS, ERO

- 來源 keyword 索引：`shall not`, `shall`, `may`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.4, Figure 51, 文件頁 27-28, PDF 頁 27-28

</details>

<details markdown="1">
<summary><strong>Figure 52: Offset PXCAP + Ah: PXDS - PCI Express Device Status</strong></summary>

<!-- claim:PCIE14-FIG-052-CLAIM figure-table:PCIE14-FIG-052 -->

Figure 52〈Offset PXCAP + Ah: PXDS - PCI Express Device Status〉：定義 offset PXCAP + Ah 的 PXDS（PCI Express Device Status），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXDS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：TP, APD, URD, FED, NFED, CED, PXCAP, PXDS。

- 解決的問題：定義 offset PXCAP + Ah 的 PXDS（PCI Express Device Status），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PXDS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：TP, APD, URD, FED, NFED, CED, PXCAP, PXDS。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PXDS，先獨立驗證 TP，再驗證 APD，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：TP, APD, URD, FED, NFED, CED, PXCAP, PXDS

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.5, Figure 52, 文件頁 28, PDF 頁 28

</details>

<details markdown="1">
<summary><strong>Figure 53: Offset PXCAP + Ch: PXLCAP - PCI Express Link Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-053-CLAIM figure-table:PCIE14-FIG-053 -->

Figure 53〈Offset PXCAP + Ch: PXLCAP - PCI Express Link Capabilities〉：定義 offset PXCAP + Ch 的 PXLCAP（PCI Express Link Capabilities），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXLCAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PN, AOC, LBNC, DLLLA, SDERC, CPM, L1EL, L0SEL。

- 解決的問題：定義 offset PXCAP + Ch 的 PXLCAP（PCI Express Link Capabilities），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PXLCAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PN, AOC, LBNC, DLLLA, SDERC, CPM, L1EL, L0SEL。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PXLCAP，先獨立驗證 PN，再驗證 AOC，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：PN, AOC, LBNC, DLLLA, SDERC, CPM, L1EL, L0SEL

- 來源 keyword 索引：`shall not`, `shall`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.6, Figure 53, 文件頁 28-29, PDF 頁 28-29

</details>

<details markdown="1">
<summary><strong>Figure 54: Offset PXCAP + 10h: PXLC - PCI Express Link Control</strong></summary>

<!-- claim:PCIE14-FIG-054-CLAIM figure-table:PCIE14-FIG-054 -->

Figure 54〈Offset PXCAP + 10h: PXLC - PCI Express Link Control〉：定義 offset PXCAP + 10h 的 PXLC（PCI Express Link Control），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXLC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：HAWD, ECPM, ES, CCC, RCB, ASPMC, PXCAP, PXLC。

- 解決的問題：定義 offset PXCAP + 10h 的 PXLC（PCI Express Link Control），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PXLC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：HAWD, ECPM, ES, CCC, RCB, ASPMC, PXCAP, PXLC。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PXLC，先獨立驗證 HAWD，再驗證 ECPM，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：HAWD, ECPM, ES, CCC, RCB, ASPMC, PXCAP, PXLC

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.7, Figure 54, 文件頁 29, PDF 頁 29

</details>

<details markdown="1">
<summary><strong>Figure 55: Offset PXCAP + 12h: PXLS - PCI Express Link Status</strong></summary>

<!-- claim:PCIE14-FIG-055-CLAIM figure-table:PCIE14-FIG-055 -->

Figure 55〈Offset PXCAP + 12h: PXLS - PCI Express Link Status〉：定義 offset PXCAP + 12h 的 PXLS（PCI Express Link Status），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXLS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：SCC, NLW, CLS, PXCAP, PXLS, SIG。

- 解決的問題：定義 offset PXCAP + 12h 的 PXLS（PCI Express Link Status），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PXLS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：SCC, NLW, CLS, PXCAP, PXLS, SIG。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PXLS，先獨立驗證 SCC，再驗證 NLW，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：SCC, NLW, CLS, PXCAP, PXLS, SIG

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.8, Figure 55, 文件頁 29, PDF 頁 29

</details>

<details markdown="1">
<summary><strong>Figure 56: Offset PXCAP + 24h: PXDCAP2 - PCI Express Device Capabilities 2</strong></summary>

<!-- claim:PCIE14-FIG-056-CLAIM figure-table:PCIE14-FIG-056 -->

Figure 56〈Offset PXCAP + 24h: PXDCAP2 - PCI Express Device Capabilities 2〉：定義 offset PXCAP + 24h 的 PXDCAP2（PCI Express Device Capabilities 2），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXDCAP2，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：MEETP, EETPS, EFFS, OBFFS, TPHCS, LTRS, NPRPR, AORS。

- 解決的問題：定義 offset PXCAP + 24h 的 PXDCAP2（PCI Express Device Capabilities 2），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PXDCAP2，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：MEETP, EETPS, EFFS, OBFFS, TPHCS, LTRS, NPRPR, AORS。

- 條件與限制：來源 keyword 索引：`shall`, `optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PXDCAP2，先獨立驗證 MEETP，再驗證 EETPS，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：MEETP, EETPS, EFFS, OBFFS, TPHCS, LTRS, NPRPR, AORS

- 來源 keyword 索引：`shall`, `optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.9, Figure 56, 文件頁 30, PDF 頁 30

</details>

<details markdown="1">
<summary><strong>Figure 57: Offset PXCAP + 28h: PXDC2 - PCI Express Device Control 2</strong></summary>

<!-- claim:PCIE14-FIG-057-CLAIM figure-table:PCIE14-FIG-057 -->

Figure 57〈Offset PXCAP + 28h: PXDC2 - PCI Express Device Control 2〉：定義 offset PXCAP + 28h 的 PXDC2（PCI Express Device Control 2），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXDC2，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：OBFFE, LTRME, CTD, CTV, PXCAP, PXDC2, SIG, OBFF。

- 解決的問題：定義 offset PXCAP + 28h 的 PXDC2（PCI Express Device Control 2），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PXDC2，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：OBFFE, LTRME, CTD, CTV, PXCAP, PXDC2, SIG, OBFF。

- 條件與限制：來源 keyword 索引：`may`, `optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PXDC2，先獨立驗證 OBFFE，再驗證 LTRME，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：OBFFE, LTRME, CTD, CTV, PXCAP, PXDC2, SIG, OBFF

- 來源 keyword 索引：`may`, `optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.10, Figure 57, 文件頁 30-31, PDF 頁 30-31

</details>

<details markdown="1">
<summary><strong>Figure 58: Advanced Error Reporting Capability (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-058-CLAIM figure-table:PCIE14-FIG-058 -->

Figure 58〈Advanced Error Reporting Capability (Optional)〉：定義〈Advanced Error Reporting Capability (Optional)〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：AERCAP, AERID, AER, ID, AERUCES, AERUCEM, AERUCESEV, AERCES。

- 解決的問題：定義〈Advanced Error Reporting Capability (Optional)〉所表示的 status／error 分類。

- 閱讀順序：先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：AERCAP, AERID, AER, ID, AERUCES, AERUCEM, AERUCESEV, AERCES。

- 條件與限制：來源 keyword 索引：`optional`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：收到一筆狀態時先辨認 AERCAP，再檢查 AERID，不可脫離類別單看數值。 此例不新增規格要求。

- 來源欄位索引：AERCAP, AERID, AER, ID, AERUCES, AERUCEM, AERUCESEV, AERCES

- 來源 keyword 索引：`optional`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.10, Figure 58, 文件頁 31, PDF 頁 31

</details>

<details markdown="1">
<summary><strong>Figure 59: Offset AERCAP: AERID - AER Capability ID</strong></summary>

<!-- claim:PCIE14-FIG-059-CLAIM figure-table:PCIE14-FIG-059 -->

Figure 59〈Offset AERCAP: AERID - AER Capability ID〉：定義 offset AERCAP 的 AERID（AER Capability ID），並指出軟體在該位置必須分別解碼的欄位。 先定位 AERID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NEXT, CVER, CID, AERCAP, AERID, AER, ID。

- 解決的問題：定義 offset AERCAP 的 AERID（AER Capability ID），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 AERID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NEXT, CVER, CID, AERCAP, AERID, AER, ID。

- 條件與限制：來源 keyword 索引：`may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 AERID，先獨立驗證 NEXT，再驗證 CVER，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：NEXT, CVER, CID, AERCAP, AERID, AER, ID

- 來源 keyword 索引：`may`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.1, Figure 59, 文件頁 31, PDF 頁 31

</details>

<details markdown="1">
<summary><strong>Figure 60: Offset AERCAP + 4: AERUCES - AER Uncorrectable Error Status Register</strong></summary>

<!-- claim:PCIE14-FIG-060-CLAIM figure-table:PCIE14-FIG-060 -->

Figure 60〈Offset AERCAP + 4: AERUCES - AER Uncorrectable Error Status Register〉：定義 offset AERCAP + 4 的 AERUCES（AER Uncorrectable Error Status Register），並指出軟體在該位置必須分別解碼的欄位。 先定位 AERUCES，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：TPBES, AOEBS, MCBTS, UIES, ACSVS, ECRCES, ROS, CAS。

- 解決的問題：定義 offset AERCAP + 4 的 AERUCES（AER Uncorrectable Error Status Register），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 AERUCES，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：TPBES, AOEBS, MCBTS, UIES, ACSVS, ECRCES, ROS, CAS。

- 條件與限制：來源 keyword 索引：`optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 AERUCES，先獨立驗證 TPBES，再驗證 AOEBS，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：TPBES, AOEBS, MCBTS, UIES, ACSVS, ECRCES, ROS, CAS

- 來源 keyword 索引：`optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.2, Figure 60, 文件頁 31-32, PDF 頁 31-32

</details>

<details markdown="1">
<summary><strong>Figure 61: Offset AERCAP + 8: AERUCEM - AER Uncorrectable Error Mask Register</strong></summary>

<!-- claim:PCIE14-FIG-061-CLAIM figure-table:PCIE14-FIG-061 -->

Figure 61〈Offset AERCAP + 8: AERUCEM - AER Uncorrectable Error Mask Register〉：定義 offset AERCAP + 8 的 AERUCEM（AER Uncorrectable Error Mask Register），並指出軟體在該位置必須分別解碼的欄位。 先定位 AERUCEM，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：TPBEM, AOEBM, MCBTM, UIEM, ACSVM, ECRCEM, ROM, CAM。

- 解決的問題：定義 offset AERCAP + 8 的 AERUCEM（AER Uncorrectable Error Mask Register），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 AERUCEM，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：TPBEM, AOEBM, MCBTM, UIEM, ACSVM, ECRCEM, ROM, CAM。

- 條件與限制：來源 keyword 索引：`optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 AERUCEM，先獨立驗證 TPBEM，再驗證 AOEBM，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：TPBEM, AOEBM, MCBTM, UIEM, ACSVM, ECRCEM, ROM, CAM

- 來源 keyword 索引：`optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.3, Figure 61, 文件頁 32, PDF 頁 32

</details>

<details markdown="1">
<summary><strong>Figure 62: Offset AERCAP + Ch: AERUCESEV - AER Uncorrectable Error Severity Register</strong></summary>

<!-- claim:PCIE14-FIG-062-CLAIM figure-table:PCIE14-FIG-062 -->

Figure 62〈Offset AERCAP + Ch: AERUCESEV - AER Uncorrectable Error Severity Register〉：定義 offset AERCAP + Ch 的 AERUCESEV（AER Uncorrectable Error Severity Register），並指出軟體在該位置必須分別解碼的欄位。 先定位 AERUCESEV，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：TPBESEV, AOEBSEV, MCBTSEV, UIESEV, ACSVSEV, ECRCESEV, ROSEV, CASEV。

- 解決的問題：定義 offset AERCAP + Ch 的 AERUCESEV（AER Uncorrectable Error Severity Register），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 AERUCESEV，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：TPBESEV, AOEBSEV, MCBTSEV, UIESEV, ACSVSEV, ECRCESEV, ROSEV, CASEV。

- 條件與限制：來源 keyword 索引：`optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 AERUCESEV，先獨立驗證 TPBESEV，再驗證 AOEBSEV，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：TPBESEV, AOEBSEV, MCBTSEV, UIESEV, ACSVSEV, ECRCESEV, ROSEV, CASEV

- 來源 keyword 索引：`optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.4, Figure 62, 文件頁 32-33, PDF 頁 32-33

</details>

<details markdown="1">
<summary><strong>Figure 63: Offset AERCAP + 10h: AERCES - AER Correctable Error Status Register</strong></summary>

<!-- claim:PCIE14-FIG-063-CLAIM figure-table:PCIE14-FIG-063 -->

Figure 63〈Offset AERCAP + 10h: AERCES - AER Correctable Error Status Register〉：定義 offset AERCAP + 10h 的 AERCES（AER Correctable Error Status Register），並指出軟體在該位置必須分別解碼的欄位。 先定位 AERCES，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：HLOS, CIES, AERCAP, AERCES, AER, SIG, RWC, ANFES。

- 解決的問題：定義 offset AERCAP + 10h 的 AERCES（AER Correctable Error Status Register），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 AERCES，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：HLOS, CIES, AERCAP, AERCES, AER, SIG, RWC, ANFES。

- 條件與限制：來源 keyword 索引：`optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 AERCES，先獨立驗證 HLOS，再驗證 CIES，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：HLOS, CIES, AERCAP, AERCES, AER, SIG, RWC, ANFES

- 來源 keyword 索引：`optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.5, Figure 63, 文件頁 33, PDF 頁 33

</details>

<details markdown="1">
<summary><strong>Figure 64: Offset AERCAP + 14h: AERCEM - AER Correctable Error Mask Register</strong></summary>

<!-- claim:PCIE14-FIG-064-CLAIM figure-table:PCIE14-FIG-064 -->

Figure 64〈Offset AERCAP + 14h: AERCEM - AER Correctable Error Mask Register〉：定義 offset AERCAP + 14h 的 AERCEM（AER Correctable Error Mask Register），並指出軟體在該位置必須分別解碼的欄位。 先定位 AERCEM，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：HLOM, CIEM, AERCAP, AERCEM, AER, SIG, ANFEM, RTM。

- 解決的問題：定義 offset AERCAP + 14h 的 AERCEM（AER Correctable Error Mask Register），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 AERCEM，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：HLOM, CIEM, AERCAP, AERCEM, AER, SIG, ANFEM, RTM。

- 條件與限制：來源 keyword 索引：`optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 AERCEM，先獨立驗證 HLOM，再驗證 CIEM，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：HLOM, CIEM, AERCAP, AERCEM, AER, SIG, ANFEM, RTM

- 來源 keyword 索引：`optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.6, Figure 64, 文件頁 33, PDF 頁 33

</details>

<details markdown="1">
<summary><strong>Figure 65: Offset AERCAP + 18h: AERCC - AER Capabilities and Control Register</strong></summary>

<!-- claim:PCIE14-FIG-065-CLAIM figure-table:PCIE14-FIG-065 -->

Figure 65〈Offset AERCAP + 18h: AERCC - AER Capabilities and Control Register〉：定義 offset AERCAP + 18h 的 AERCC（AER Capabilities and Control Register），並指出軟體在該位置必須分別解碼的欄位。 先定位 AERCC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：TPLP, MHRE, MHRC, ECE, ECC, EGE, EGC, FEP。

- 解決的問題：定義 offset AERCAP + 18h 的 AERCC（AER Capabilities and Control Register），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 AERCC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：TPLP, MHRE, MHRC, ECE, ECC, EGE, EGC, FEP。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 AERCC，先獨立驗證 TPLP，再驗證 MHRE，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：TPLP, MHRE, MHRC, ECE, ECC, EGE, EGC, FEP

- 來源 keyword 索引：`reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.7, Figure 65, 文件頁 34, PDF 頁 34

</details>

<details markdown="1">
<summary><strong>Figure 66: Offset AERCAP + 1Ch: AERHL - AER Header Log Register</strong></summary>

<!-- claim:PCIE14-FIG-066-CLAIM figure-table:PCIE14-FIG-066 -->

Figure 66〈Offset AERCAP + 1Ch: AERHL - AER Header Log Register〉：定義 offset AERCAP + 1Ch 的 AERHL（AER Header Log Register），並指出軟體在該位置必須分別解碼的欄位。 先定位 AERHL，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：AERCAP, AERHL, AER, HB3, HB2, HB1, HB0, HB7。

- 解決的問題：定義 offset AERCAP + 1Ch 的 AERHL（AER Header Log Register），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 AERHL，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：AERCAP, AERHL, AER, HB3, HB2, HB1, HB0, HB7。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 AERHL，先獨立驗證 AERCAP，再驗證 AERHL，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：AERCAP, AERHL, AER, HB3, HB2, HB1, HB0, HB7

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.8, Figure 66, 文件頁 34, PDF 頁 34

</details>

<details markdown="1">
<summary><strong>Figure 67: Offset AERCAP + 38h: AERTLP - AER TLP Prefix Log Register (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-067-CLAIM figure-table:PCIE14-FIG-067 -->

Figure 67〈Offset AERCAP + 38h: AERTLP - AER TLP Prefix Log Register (Optional)〉：定義 offset AERCAP + 38h 的 AERTLP（AER TLP Prefix Log Register (Optional)），並指出軟體在該位置必須分別解碼的欄位。 先定位 AERTLP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：AERCAP, AERTLP, AER, TLP, TPL1B3, TPL1B2, TPL1B1, TPL1B0。

- 解決的問題：定義 offset AERCAP + 38h 的 AERTLP（AER TLP Prefix Log Register (Optional)），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 AERTLP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：AERCAP, AERTLP, AER, TLP, TPL1B3, TPL1B2, TPL1B1, TPL1B0。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `optional`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 AERTLP，先獨立驗證 AERCAP，再驗證 AERTLP，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：AERCAP, AERTLP, AER, TLP, TPL1B3, TPL1B2, TPL1B1, TPL1B0

- 來源 keyword 索引：`shall`, `may`, `optional`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.9, Figure 67, 文件頁 35, PDF 頁 35

</details>

<details markdown="1">
<summary><strong>Figure 68: Example of an Eve Diagram in the Printable Eye Field</strong></summary>

<!-- claim:PCIE14-FIG-068-CLAIM figure-table:PCIE14-FIG-068 -->

Figure 68〈Example of an Eve Diagram in the Printable Eye Field〉：定義〈Example of an Eve Diagram in the Printable Eye Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TEE, VM, OS, TDISP, SR, IOV, SIOV, MI。

- 解決的問題：定義〈Example of an Eve Diagram in the Printable Eye Field〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TEE, VM, OS, TDISP, SR, IOV, SIOV, MI。

- 條件與限制：來源 keyword 索引：`shall`, `may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 原始 Figure caption 使用「Eve」；section 上下文說明的是 receiver eye。此處保留原 caption 以利追溯。

- 說明性範例（informative example）：以 TEE 作為 parser 的第一個檢查點，再用 VM 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：TEE, VM, OS, TDISP, SR, IOV, SIOV, MI

- 來源 keyword 索引：`shall`, `may`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.9, Figure 68, 文件頁 37, PDF 頁 37

</details>

<details markdown="1">
<summary><strong>Figure 69: NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure</strong></summary>

<!-- claim:PCIE14-FIG-069-CLAIM figure-table:PCIE14-FIG-069 -->

Figure 69〈NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure〉：定義〈NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TDISP。

- 解決的問題：定義〈NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TDISP。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：以 TDISP 作為 parser 的第一個檢查點，再用 引用條件 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：TDISP

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.10, Figure 69, 文件頁 38-39, PDF 頁 38-39

</details>

<a id="section-3-9"></a>

### §3.9

<details markdown="1">
<summary><strong>Figure 70: Get Log Page - Log Page Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-070-CLAIM figure-table:PCIE14-FIG-070 -->

Figure 70〈Get Log Page - Log Page Identifiers〉：定義〈Get Log Page - Log Page Identifiers〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：CSI1, CSI。

- 解決的問題：定義〈Get Log Page - Log Page Identifiers〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：CSI1, CSI。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依定義寬度解析 CSI1，再核對 CSI 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：CSI1, CSI

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, Figure 70, 文件頁 39, PDF 頁 39

</details>

<details markdown="1">
<summary><strong>Figure 71: Size of Physical Interface Receiver Eye Opening Measurement Log Page</strong></summary>

<!-- claim:PCIE14-FIG-071-CLAIM figure-table:PCIE14-FIG-071 -->

Figure 71〈Size of Physical Interface Receiver Eye Opening Measurement Log Page〉：呈現〈Size of Physical Interface Receiver Eye Opening Measurement Log Page〉中的 receiver-eye measurement 資訊。 先確認支援與回傳長度，再解 lane、parameter、header 或 descriptor；來源索引：Size of Physical Interface Receiver Eye Opening Measurement Log Page。

- 解決的問題：呈現〈Size of Physical Interface Receiver Eye Opening Measurement Log Page〉中的 receiver-eye measurement 資訊。

- 閱讀順序：先確認支援與回傳長度，再解 lane、parameter、header 或 descriptor；來源索引：Size of Physical Interface Receiver Eye Opening Measurement Log Page。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：先確認 Size of Physical Interface Receiver Eye Opening Measurement Log Page 已存在，只有在回傳結構長度足夠時才繼續解析 引用條件。 此例不新增規格要求。

- 來源欄位索引：Size of Physical Interface Receiver Eye Opening Measurement Log Page

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 71, 文件頁 40, PDF 頁 40

</details>

<details markdown="1">
<summary><strong>Figure 72: Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field</strong></summary>

<!-- claim:PCIE14-FIG-072-CLAIM figure-table:PCIE14-FIG-072 -->

Figure 72〈Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field〉：定義〈Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ACT, MQUAL, LPOU, LPOL, EOM, EOMIP。

- 解決的問題：定義〈Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ACT, MQUAL, LPOU, LPOL, EOM, EOMIP。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 ACT 作為 parser 的第一個檢查點，再用 MQUAL 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：ACT, MQUAL, LPOU, LPOL, EOM, EOMIP

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 72, 文件頁 40-41, PDF 頁 40-41

</details>

<details markdown="1">
<summary><strong>Figure 73: Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field</strong></summary>

<!-- claim:PCIE14-FIG-073-CLAIM figure-table:PCIE14-FIG-073 -->

Figure 73〈Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field〉：定義〈Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TC, ID, EOM。

- 解決的問題：定義〈Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TC, ID, EOM。

- 條件與限制：來源 keyword 索引：`shall`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 TC 作為 parser 的第一個檢查點，再用 ID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：TC, ID, EOM

- 來源 keyword 索引：`shall`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 73, 文件頁 41, PDF 頁 41

</details>

<details markdown="1">
<summary><strong>Figure 74: Physical Interface Receiver Eye Opening Measurement Log Page</strong></summary>

<!-- claim:PCIE14-FIG-074-CLAIM figure-table:PCIE14-FIG-074 -->

Figure 74〈Physical Interface Receiver Eye Opening Measurement Log Page〉：呈現〈Physical Interface Receiver Eye Opening Measurement Log Page〉中的 receiver-eye measurement 資訊。 先確認支援與回傳長度，再解 lane、parameter、header 或 descriptor；來源索引：Physical Interface Receiver Eye Opening Measurement Log Page。

- 解決的問題：呈現〈Physical Interface Receiver Eye Opening Measurement Log Page〉中的 receiver-eye measurement 資訊。

- 閱讀順序：先確認支援與回傳長度，再解 lane、parameter、header 或 descriptor；來源索引：Physical Interface Receiver Eye Opening Measurement Log Page。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：先確認 Physical Interface Receiver Eye Opening Measurement Log Page 已存在，只有在回傳結構長度足夠時才繼續解析 引用條件。 此例不新增規格要求。

- 來源欄位索引：Physical Interface Receiver Eye Opening Measurement Log Page

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 74, 文件頁 41, PDF 頁 41

</details>

<details markdown="1">
<summary><strong>Figure 75: EOM Header</strong></summary>

<!-- claim:PCIE14-FIG-075-CLAIM figure-table:PCIE14-FIG-075 -->

Figure 75〈EOM Header〉：呈現〈EOM Header〉中的 receiver-eye measurement 資訊。 先確認支援與回傳長度，再解 lane、parameter、header 或 descriptor；來源索引：EOM。

- 解決的問題：呈現〈EOM Header〉中的 receiver-eye measurement 資訊。

- 閱讀順序：先確認支援與回傳長度，再解 lane、parameter、header 或 descriptor；來源索引：EOM。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：先確認 EOM 已存在，只有在回傳結構長度足夠時才繼續解析 引用條件。 此例不新增規格要求。

- 來源欄位索引：EOM

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 75, 文件頁 42-43, PDF 頁 42-43

</details>

<details markdown="1">
<summary><strong>Figure 76: EOM Lane Descriptor</strong></summary>

<!-- claim:PCIE14-FIG-076-CLAIM figure-table:PCIE14-FIG-076 -->

Figure 76〈EOM Lane Descriptor〉：定義〈EOM Lane Descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MSTAT, MSCS, LN, EYE, TOP, BTM, LFT, RGT。

- 解決的問題：定義〈EOM Lane Descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MSTAT, MSCS, LN, EYE, TOP, BTM, LFT, RGT。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 MSTAT 作為 parser 的第一個檢查點，再用 MSCS 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：MSTAT, MSCS, LN, EYE, TOP, BTM, LFT, RGT

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 76, 文件頁 43-45, PDF 頁 43-45

</details>

<details markdown="1">
<summary><strong>Figure 77: Example of an Eve Diagram in the Printable Eye Field</strong></summary>

<!-- claim:PCIE14-FIG-077-CLAIM figure-table:PCIE14-FIG-077 -->

Figure 77〈Example of an Eve Diagram in the Printable Eye Field〉：定義〈Example of an Eve Diagram in the Printable Eye Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Example of an Eve Diagram in the Printable Eye Field。

- 解決的問題：定義〈Example of an Eve Diagram in the Printable Eye Field〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Example of an Eve Diagram in the Printable Eye Field。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。 原始 Figure caption 使用「Eve」；section 上下文說明的是 receiver eye。此處保留原 caption 以利追溯。

- 說明性範例（informative example）：以 Example of an Eve Diagram in the Printable Eye Field 作為 parser 的第一個檢查點，再用 引用條件 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：Example of an Eve Diagram in the Printable Eye Field

- 來源 keyword 索引：none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 77, 文件頁 46, PDF 頁 46

</details>

## 使用與限制

製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata 集合或核准範圍改變時，必須重新核對受影響 claim。
