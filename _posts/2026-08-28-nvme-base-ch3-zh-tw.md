---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4 第 3 章：Controller、Queue、初始化與重設"
date: 2026-08-28
description: "供 GitHub Pages 與 PPT 使用的 NVMe 規格導讀。"
lang: zh-Hant-TW
img: posts/2026/dogMC_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---

# NVMe Base 2.4 第 3 章：Controller、Queue、初始化與重設

用途：供 GitHub Pages 閱讀與 100 分鐘簡報製作；讀者已具備 PCIe 與 NVMe 基礎。

範圍：§3；文件頁 38-138；PDF 頁 64-164。正文只保留 PCIe／memory-based 與通用 NVMe 內容。

## 來源版本

NVM Express Base Specification, Revision 2.4

查證日期：2026-08-29。目前未納入其他 Errata、ECN、Technical Proposal、controller vendor 文件或未提供的 PCI Express Base Specification 原文。

## 閱讀地圖

```text
Properties / CAP -> CC.EN = 1 -> CSTS.RDY = 1 -> Queues active
```

host 先讀能力與設定 Admin queues，再啟用 controller；只有 CSTS.RDY 回報 ready 後才進入正常 queue processing。

## 規範性用語

shall 譯為「必須」，may 譯為「可／得」，should 譯為「宜／建議」，optional 譯為「選用」。本文不提高或降低原文語氣。

## 規格重點

### 1. static controller model

<!-- claim:BASE3-STATIC -->

memory-based controller 必須（shall）只支援 static controller model。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.1, 文件頁 38, PDF 頁 64

### 2. I/O 與 Administrative controller

<!-- claim:BASE3-TYPES -->

本輪只使用 I/O controller 與 Administrative controller：前者可執行使用者資料的 I/O，後者以管理為目的且不支援資料 I/O command。兩者都具有一組 Admin Submission／Completion Queue。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3-3.1.3.2, 文件頁 39-43, PDF 頁 65-69

### 3. 命令與完成順序

<!-- claim:BASE3-ORDER -->

除 fused operation 外，controller 取走的命令與完成沒有一般性的先後保證；若有順序需求，強制該順序是 host 的責任。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3, 文件頁 40, PDF 頁 66

### 4. property 存取寬度

<!-- claim:BASE3-PROPERTY -->

host 必須（shall）以 property 指定的寬度，從 property 起始 offset 存取；memory-based controller 的實際存取規則由 PCIe Transport 補充。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, 文件頁 52-54, PDF 頁 78-80

### 5. NSID 狀態與特殊值

<!-- claim:BASE3-NAMESPACE -->

NSID 0h 無效，FFFFFFFFh 是 broadcast 值；其餘 NSID 還要區分 allocated／unallocated 與 active／inactive，不能只看數字是否落在範圍內。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.1, 文件頁 78-80, PDF 頁 104-106

### 6. 媒體與回收階層

<!-- claim:BASE3-MEDIA -->

NVM Set、Endurance Group、Reclaim Group 與 Reclaim Unit 分別描述容量集合、耐久度管理與回收粒度。是否支援及其 identifier 由 Identify／log page 能力判定。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, 文件頁 80-85, PDF 頁 106-111

### 7. domain 邊界與識別碼

<!-- claim:BASE3-DOMAIN -->

domain 是 NVM subsystem 內的故障／通訊邊界。多 domain subsystem 的 identifier 必須（shall）在該 subsystem 內唯一。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.5, 文件頁 85-88, PDF 頁 111-114

### 8. PCIe queue 建立與 pointer

<!-- claim:BASE3-QUEUE -->

PCIe queue 由 host-addressable memory 中的環形 buffer、head 與 tail pointer 構成。host 建立 I/O Completion Queue 後再建立對應 Submission Queue，並以 doorbell 推進 pointer。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1, 文件頁 88-91, PDF 頁 114-117

### 9. 命令處理與 arbitration

<!-- claim:BASE3-PROCESS -->

command processing 要分開看 ordering、fused／atomic semantics、arbitration 與 outstanding command 上限；priority 屬於 Submission Queue，不是每一筆 command 的獨立欄位。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, 文件頁 101-105, PDF 頁 127-131

### 10. controller 初始化

<!-- claim:BASE3-INIT -->

PCIe 初始化以 CAP 判斷能力與 timeout，設定 AQA／ASQ／ACQ 與 CC，接著等待 CSTS.RDY。ready mode 與 CRTO 會影響 host 等待與錯誤處理。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, 文件頁 105-113, PDF 頁 131-139

### 11. shutdown 狀態流程

<!-- claim:BASE3-SHUTDOWN -->

正常 shutdown 由 host 設定 CC.SHN，controller 透過 CSTS.SHST 回報進度；NVM subsystem shutdown 是更大範圍的處理，不能與單一 controller shutdown 混為一談。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, 文件頁 113-120, PDF 頁 139-146

### 12. reset 層級與影響範圍

<!-- claim:BASE3-RESET -->

NVM Subsystem Reset、Controller Level Reset 與 Queue Level Reset 的影響範圍不同；設計 recovery flow 前先確認哪一層狀態會被清除、queue 是否仍存在。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.7, 文件頁 120-125, PDF 頁 146-151

### 13. capacity model

<!-- claim:BASE3-CAPACITY -->

capacity model 分開追蹤 NVM subsystem、Endurance Group、NVM Set 與 namespace 的可用或配置容量；同一數值不可跨層級直接比較。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.8, 文件頁 125-129, PDF 頁 151-155

### 14. Keep Alive timer

<!-- claim:BASE3-KEEPALIVE -->

Keep Alive 以 KATO／KATT 建立 host 與 controller 的存活監測；本報告只保留 controller 共通與 PCIe 可用的 timer、command 與 timeout 行為。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.9, 文件頁 129-135, PDF 頁 155-161

### 15. firmware update 與 privileged action

<!-- claim:BASE3-FIRMWARE -->

privileged action 會影響其他 host 或 controller；firmware update 分成 image download、commit／activate 與可能的 reset，host 依回報的 activation action 安排流程。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.10-3.11, 文件頁 135-138, PDF 頁 161-164

## Figure 索引

本報告介紹全部 59 張納入範圍的 Figure。100 分鐘簡報以 section 主線與必講 Figure 為主，其餘 Figure 仍完整保留作為附錄。

- [§3.1](#section-3-1)

- [§3.2](#section-3-2)

- [§3.3](#section-3-3)

- [§3.4](#section-3-4)

- [§3.5](#section-3-5)

- [§3.6](#section-3-6)

- [§3.8](#section-3-8)

- [§3.9](#section-3-9)

- [§3.10](#section-3-10)

## Figure 逐圖導讀

本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。欄位與 keyword 索引來自本機核對過的 PDF。

<a id="section-3-1"></a>

### §3.1

<details markdown="1">
<summary><strong>Figure 23: Controller Types</strong></summary>

<!-- claim:BASE3-FIG-023-CLAIM figure-table:BASE3-FIG-023 -->

Figure 23〈Controller Types〉：呈現〈Controller Types〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：Controller。

- 解決的問題：呈現〈Controller Types〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：Controller。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。 本報告只解釋 PCIe／memory-based 部分。

- 說明性範例（informative example）：選擇 Controller 標示的一個物件，再追到 引用條件，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：Controller

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3, Figure 23, 文件頁 39, PDF 頁 65

</details>

<details markdown="1">
<summary><strong>Figure 24: NVM Subsystem with Three I/O Controllers</strong></summary>

<!-- claim:BASE3-FIG-024-CLAIM figure-table:BASE3-FIG-024 -->

Figure 24〈NVM Subsystem with Three I/O Controllers〉：呈現〈NVM Subsystem with Three I/O Controllers〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, I/O Controller, Controller。

- 解決的問題：呈現〈NVM Subsystem with Three I/O Controllers〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, I/O Controller, Controller。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Subsystem 標示的一個物件，再追到 I/O Controller，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Subsystem, I/O Controller, Controller

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.1, Figure 24, 文件頁 41, PDF 頁 67

</details>

<details markdown="1">
<summary><strong>Figure 25: NVM Subsystem with One Administrative and Two I/O Controllers</strong></summary>

<!-- claim:BASE3-FIG-025-CLAIM figure-table:BASE3-FIG-025 -->

Figure 25〈NVM Subsystem with One Administrative and Two I/O Controllers〉：呈現〈NVM Subsystem with One Administrative and Two I/O Controllers〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, I/O Controller, Controller。

- 解決的問題：呈現〈NVM Subsystem with One Administrative and Two I/O Controllers〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, I/O Controller, Controller。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Subsystem 標示的一個物件，再追到 I/O Controller，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Subsystem, I/O Controller, Controller

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.2, Figure 25, 文件頁 42, PDF 頁 68

</details>

<details markdown="1">
<summary><strong>Figure 26: NVM Subsystem with One Administrative Controller</strong></summary>

<!-- claim:BASE3-FIG-026-CLAIM figure-table:BASE3-FIG-026 -->

Figure 26〈NVM Subsystem with One Administrative Controller〉：呈現〈NVM Subsystem with One Administrative Controller〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, Administrative Controller, Controller。

- 解決的問題：呈現〈NVM Subsystem with One Administrative Controller〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, Administrative Controller, Controller。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Subsystem 標示的一個物件，再追到 Administrative Controller，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Subsystem, Administrative Controller, Controller

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.2, Figure 26, 文件頁 42, PDF 頁 68

</details>

<details markdown="1">
<summary><strong>Figure 27: Controller IDs FFF0h to FFFFh</strong></summary>

<!-- claim:BASE3-FIG-027-CLAIM figure-table:BASE3-FIG-027 -->

Figure 27〈Controller IDs FFF0h to FFFFh〉：定義〈Controller IDs FFF0h to FFFFh〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：Controller, Controller ID。

- 解決的問題：定義〈Controller IDs FFF0h to FFFFh〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：Controller, Controller ID。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依定義寬度解析 Controller，再核對 Controller ID 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：Controller, Controller ID

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.3, Figure 27, 文件頁 44, PDF 頁 70

</details>

<details markdown="1">
<summary><strong>Figure 28: Admin Command Support Requirements</strong></summary>

<!-- claim:BASE3-FIG-028-CLAIM figure-table:BASE3-FIG-028 -->

Figure 28〈Admin Command Support Requirements〉：統整〈Admin Command Support Requirements〉指定的支援等級。 先確認 row 與 controller／command-set 上下文，再解讀 support marker；來源索引：MI, O10, O11, Command。

- 解決的問題：統整〈Admin Command Support Requirements〉指定的支援等級。

- 閱讀順序：先確認 row 與 controller／command-set 上下文，再解讀 support marker；來源索引：MI, O10, O11, Command。

- 條件與限制：來源 keyword 索引：`optional`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 本報告只解釋 PCIe／memory-based 部分。

- 說明性範例（informative example）：先在適用 row 查找 MI，再核對 O10 所代表的上下文，最後才判斷必須或選用。 此例不新增規格要求。

- 來源欄位索引：MI, O10, O11, Command

- 來源 keyword 索引：`optional`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.3.3, Figure 28, 文件頁 45-47, PDF 頁 71-73

</details>

<details markdown="1">
<summary><strong>Figure 30: Common I/O Command Support Requirements</strong></summary>

<!-- claim:BASE3-FIG-030-CLAIM figure-table:BASE3-FIG-030 -->

Figure 30〈Common I/O Command Support Requirements〉：統整〈Common I/O Command Support Requirements〉指定的支援等級。 先確認 row 與 controller／command-set 上下文，再解讀 support marker；來源索引：FDPS, Command。

- 解決的問題：統整〈Common I/O Command Support Requirements〉指定的支援等級。

- 閱讀順序：先確認 row 與 controller／command-set 上下文，再解讀 support marker；來源索引：FDPS, Command。

- 條件與限制：來源 keyword 索引：`optional`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 本報告只解釋 PCIe／memory-based 部分。

- 說明性範例（informative example）：先在適用 row 查找 FDPS，再核對 Command 所代表的上下文，最後才判斷必須或選用。 此例不新增規格要求。

- 來源欄位索引：FDPS, Command

- 來源 keyword 索引：`optional`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.4, Figure 30, 文件頁 47-48, PDF 頁 73-74

</details>

<details markdown="1">
<summary><strong>Figure 31: Log Page Support Requirements</strong></summary>

<!-- claim:BASE3-FIG-031-CLAIM figure-table:BASE3-FIG-031 -->

Figure 31〈Log Page Support Requirements〉：統整〈Log Page Support Requirements〉指定的支援等級。 先確認 row 與 controller／command-set 上下文，再解讀 support marker；來源索引：M3, SMART, O4, O6, O12, O13, FDP, O5。

- 解決的問題：統整〈Log Page Support Requirements〉指定的支援等級。

- 閱讀順序：先確認 row 與 controller／command-set 上下文，再解讀 support marker；來源索引：M3, SMART, O4, O6, O12, O13, FDP, O5。

- 條件與限制：來源 keyword 索引：`shall`, `optional`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 本報告只解釋 PCIe／memory-based 部分。

- 說明性範例（informative example）：先在適用 row 查找 M3，再核對 SMART 所代表的上下文，最後才判斷必須或選用。 此例不新增規格要求。

- 來源欄位索引：M3, SMART, O4, O6, O12, O13, FDP, O5

- 來源 keyword 索引：`shall`, `optional`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.4, Figure 31, 文件頁 48-50, PDF 頁 74-76

</details>

<details markdown="1">
<summary><strong>Figure 32: Feature Support Requirements</strong></summary>

<!-- claim:BASE3-FIG-032-CLAIM figure-table:BASE3-FIG-032 -->

Figure 32〈Feature Support Requirements〉：統整〈Feature Support Requirements〉指定的支援等級。 先確認 row 與 controller／command-set 上下文，再解讀 support marker；來源索引：LBA, O8, M10, M7, O9, O6, O5, O3。

- 解決的問題：統整〈Feature Support Requirements〉指定的支援等級。

- 閱讀順序：先確認 row 與 controller／command-set 上下文，再解讀 support marker；來源索引：LBA, O8, M10, M7, O9, O6, O5, O3。

- 條件與限制：來源 keyword 索引：`optional`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 本報告只解釋 PCIe／memory-based 部分。

- 說明性範例（informative example）：先在適用 row 查找 LBA，再核對 O8 所代表的上下文，最後才判斷必須或選用。 此例不新增規格要求。

- 來源欄位索引：LBA, O8, M10, M7, O9, O6, O5, O3

- 來源 keyword 索引：`optional`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.5, Figure 32, 文件頁 50-52, PDF 頁 76-78

</details>

<details markdown="1">
<summary><strong>Figure 33: Property Definition</strong></summary>

<!-- claim:BASE3-FIG-033-CLAIM figure-table:BASE3-FIG-033 -->

Figure 33〈Property Definition〉：定義〈Property Definition〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：OFST, CAP, VS, M2, INTMS, INTMC, CC, CSTS。

- 解決的問題：定義〈Property Definition〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：OFST, CAP, VS, M2, INTMS, INTMC, CC, CSTS。

- 條件與限制：來源 keyword 索引：`optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 本報告只解釋 PCIe／memory-based 部分。

- 說明性範例（informative example）：以 OFST 作為 parser 的第一個檢查點，再用 CAP 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：OFST, CAP, VS, M2, INTMS, INTMC, CC, CSTS

- 來源 keyword 索引：`optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, Figure 33, 文件頁 52-53, PDF 頁 78-79

</details>

<details markdown="1">
<summary><strong>Figure 34: Memory-Based Property Definition</strong></summary>

<!-- claim:BASE3-FIG-034-CLAIM figure-table:BASE3-FIG-034 -->

Figure 34〈Memory-Based Property Definition〉：定義〈Memory-Based Property Definition〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：OFST, CAP.DSTRD。

- 解決的問題：定義〈Memory-Based Property Definition〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：OFST, CAP.DSTRD。

- 條件與限制：來源 keyword 索引：`optional`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 OFST 作為 parser 的第一個檢查點，再用 CAP.DSTRD 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：OFST, CAP.DSTRD

- 來源 keyword 索引：`optional`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, Figure 34, 文件頁 54, PDF 頁 80

</details>

<details markdown="1">
<summary><strong>Figure 36: Offset 0h: CAP - Controller Capabilities</strong></summary>

<!-- claim:BASE3-FIG-036-CLAIM figure-table:BASE3-FIG-036 -->

Figure 36〈Offset 0h: CAP - Controller Capabilities〉：定義 offset 0h 的 CAP（Controller Capabilities），並指出軟體在該位置必須分別解碼的欄位。 先定位 CAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NSSES, CRMS, CRIMS, CRWMS, NSSS, CMBS, PMRS, MPSMAX。

- 解決的問題：定義 offset 0h 的 CAP（Controller Capabilities），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 CAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NSSES, CRMS, CRIMS, CRWMS, NSSS, CMBS, PMRS, MPSMAX。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `should`, `may`, `optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 CAP，先獨立驗證 NSSES，再驗證 CRMS，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：NSSES, CRMS, CRIMS, CRWMS, NSSS, CMBS, PMRS, MPSMAX

- 來源 keyword 索引：`shall not`, `shall`, `should`, `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, 文件頁 55-58, PDF 頁 81-84

</details>

<details markdown="1">
<summary><strong>Figure 37: Specification Version Descriptor</strong></summary>

<!-- claim:BASE3-FIG-037-CLAIM figure-table:BASE3-FIG-037 -->

Figure 37〈Specification Version Descriptor〉：定義〈Specification Version Descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MJR, MNR, TER。

- 解決的問題：定義〈Specification Version Descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MJR, MNR, TER。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：以 MJR 作為 parser 的第一個檢查點，再用 MNR 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：MJR, MNR, TER

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 37, 文件頁 58, PDF 頁 84

</details>

<details markdown="1">
<summary><strong>Figure 38: NVM Express Base Specification Version Property Reset Values</strong></summary>

<!-- claim:BASE3-FIG-038-CLAIM figure-table:BASE3-FIG-038 -->

Figure 38〈NVM Express Base Specification Version Property Reset Values〉：定義〈NVM Express Base Specification Version Property Reset Values〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MJR, MNR, TER。

- 解決的問題：定義〈NVM Express Base Specification Version Property Reset Values〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MJR, MNR, TER。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：以 MJR 作為 parser 的第一個檢查點，再用 MNR 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：MJR, MNR, TER

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 38, 文件頁 58-59, PDF 頁 84-85

</details>

<details markdown="1">
<summary><strong>Figure 39: Offset Ch: INTMS - Interrupt Mask Set</strong></summary>

<!-- claim:BASE3-FIG-039-CLAIM figure-table:BASE3-FIG-039 -->

Figure 39〈Offset Ch: INTMS - Interrupt Mask Set〉：定義 offset Ch 的 INTMS（Interrupt Mask Set），並指出軟體在該位置必須分別解碼的欄位。 先定位 INTMS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：IVMS, INTMS, RWS, MSI, Interrupt。

- 解決的問題：定義 offset Ch 的 INTMS（Interrupt Mask Set），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 INTMS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：IVMS, INTMS, RWS, MSI, Interrupt。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 INTMS，先獨立驗證 IVMS，再驗證 INTMS，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：IVMS, INTMS, RWS, MSI, Interrupt

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.2, Figure 39, 文件頁 59, PDF 頁 85

</details>

<details markdown="1">
<summary><strong>Figure 40: Offset 10h: INTMC - Interrupt Mask Clear</strong></summary>

<!-- claim:BASE3-FIG-040-CLAIM figure-table:BASE3-FIG-040 -->

Figure 40〈Offset 10h: INTMC - Interrupt Mask Clear〉：定義 offset 10h 的 INTMC（Interrupt Mask Clear），並指出軟體在該位置必須分別解碼的欄位。 先定位 INTMC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：IVMC, INTMC, RWC, Interrupt。

- 解決的問題：定義 offset 10h 的 INTMC（Interrupt Mask Clear），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 INTMC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：IVMC, INTMC, RWC, Interrupt。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 INTMC，先獨立驗證 IVMC，再驗證 INTMC，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：IVMC, INTMC, RWC, Interrupt

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.2, Figure 40, 文件頁 59, PDF 頁 85

</details>

<details markdown="1">
<summary><strong>Figure 41: Offset 14h: CC - Controller Configuration</strong></summary>

<!-- claim:BASE3-FIG-041-CLAIM figure-table:BASE3-FIG-041 -->

Figure 41〈Offset 14h: CC - Controller Configuration〉：定義 offset 14h 的 CC（Controller Configuration），並指出軟體在該位置必須分別解碼的欄位。 先定位 CC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CRIME, SHN, AMS, MPS, CSS, EN, CC, CC.EN。

- 解決的問題：定義 offset 14h 的 CC（Controller Configuration），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 CC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CRIME, SHN, AMS, MPS, CSS, EN, CC, CC.EN。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `should`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 CC，先獨立驗證 CRIME，再驗證 SHN，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：CRIME, SHN, AMS, MPS, CSS, EN, CC, CC.EN

- 來源 keyword 索引：`shall not`, `shall`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.5, Figure 41, 文件頁 60-63, PDF 頁 86-89

</details>

<details markdown="1">
<summary><strong>Figure 42: Offset 1Ch: CSTS - Controller Status</strong></summary>

<!-- claim:BASE3-FIG-042-CLAIM figure-table:BASE3-FIG-042 -->

Figure 42〈Offset 1Ch: CSTS - Controller Status〉：定義 offset 1Ch 的 CSTS（Controller Status），並指出軟體在該位置必須分別解碼的欄位。 先定位 CSTS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ST, PP, NSSRO, SHST, CLR, CFS, RDY, CSTS。

- 解決的問題：定義 offset 1Ch 的 CSTS（Controller Status），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 CSTS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ST, PP, NSSRO, SHST, CLR, CFS, RDY, CSTS。

- 條件與限制：來源 keyword 索引：`shall not`, `should not`, `shall`, `should`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 CSTS，先獨立驗證 ST，再驗證 PP，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：ST, PP, NSSRO, SHST, CLR, CFS, RDY, CSTS

- 來源 keyword 索引：`shall not`, `should not`, `shall`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.5, Figure 42, 文件頁 63-65, PDF 頁 89-91

</details>

<details markdown="1">
<summary><strong>Figure 43: Offset 20h: NSSR - NVM Subsystem Reset</strong></summary>

<!-- claim:BASE3-FIG-043-CLAIM figure-table:BASE3-FIG-043 -->

Figure 43〈Offset 20h: NSSR - NVM Subsystem Reset〉：定義 offset 20h 的 NSSR（NVM Subsystem Reset），並指出軟體在該位置必須分別解碼的欄位。 先定位 NSSR，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NSSRC, NSSR, NVM Subsystem。

- 解決的問題：定義 offset 20h 的 NSSR（NVM Subsystem Reset），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 NSSR，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NSSRC, NSSR, NVM Subsystem。

- 條件與限制：來源 keyword 索引：`shall`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 NSSR，先獨立驗證 NSSRC，再驗證 NSSR，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：NSSRC, NSSR, NVM Subsystem

- 來源 keyword 索引：`shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 43, 文件頁 66, PDF 頁 92

</details>

<details markdown="1">
<summary><strong>Figure 44: Offset 24h: AQA - Admin Queue Attributes</strong></summary>

<!-- claim:BASE3-FIG-044-CLAIM figure-table:BASE3-FIG-044 -->

Figure 44〈Offset 24h: AQA - Admin Queue Attributes〉：定義 offset 24h 的 AQA（Admin Queue Attributes），並指出軟體在該位置必須分別解碼的欄位。 先定位 AQA，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ACQS, ASQS, AQA。

- 解決的問題：定義 offset 24h 的 AQA（Admin Queue Attributes），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 AQA，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ACQS, ASQS, AQA。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 AQA，先獨立驗證 ACQS，再驗證 ASQS，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：ACQS, ASQS, AQA

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 44, 文件頁 66, PDF 頁 92

</details>

<details markdown="1">
<summary><strong>Figure 45: Offset 28h: ASQ - Admin Submission Queue Base Address</strong></summary>

<!-- claim:BASE3-FIG-045-CLAIM figure-table:BASE3-FIG-045 -->

Figure 45〈Offset 28h: ASQ - Admin Submission Queue Base Address〉：定義 offset 28h 的 ASQ（Admin Submission Queue Base Address），並指出軟體在該位置必須分別解碼的欄位。 先定位 ASQ，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ASQB, ASQ, CC.MPS, Submission Queue。

- 解決的問題：定義 offset 28h 的 ASQ（Admin Submission Queue Base Address），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 ASQ，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ASQB, ASQ, CC.MPS, Submission Queue。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 ASQ，先獨立驗證 ASQB，再驗證 ASQ，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：ASQB, ASQ, CC.MPS, Submission Queue

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 45, 文件頁 66, PDF 頁 92

</details>

<details markdown="1">
<summary><strong>Figure 46: Offset 30h: ACQ - Admin Completion Queue Base Address</strong></summary>

<!-- claim:BASE3-FIG-046-CLAIM figure-table:BASE3-FIG-046 -->

Figure 46〈Offset 30h: ACQ - Admin Completion Queue Base Address〉：定義 offset 30h 的 ACQ（Admin Completion Queue Base Address），並指出軟體在該位置必須分別解碼的欄位。 先定位 ACQ，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ACQB, ACQ, CC.MPS, Completion Queue。

- 解決的問題：定義 offset 30h 的 ACQ（Admin Completion Queue Base Address），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 ACQ，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ACQB, ACQ, CC.MPS, Completion Queue。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 ACQ，先獨立驗證 ACQB，再驗證 ACQ，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：ACQB, ACQ, CC.MPS, Completion Queue

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.9, Figure 46, 文件頁 67, PDF 頁 93

</details>

<details markdown="1">
<summary><strong>Figure 47: Offset 38h: CMBLOC - Controller Memory Buffer Location</strong></summary>

<!-- claim:BASE3-FIG-047-CLAIM figure-table:BASE3-FIG-047 -->

Figure 47〈Offset 38h: CMBLOC - Controller Memory Buffer Location〉：定義 offset 38h 的 CMBLOC（Controller Memory Buffer Location），並指出軟體在該位置必須分別解碼的欄位。 先定位 CMBLOC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CQMMS, BIR, CMBLOC, CMB, BAR, Controller。

- 解決的問題：定義 offset 38h 的 CMBLOC（Controller Memory Buffer Location），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 CMBLOC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CQMMS, BIR, CMBLOC, CMB, BAR, Controller。

- 條件與限制：來源 keyword 索引：`shall`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 CMBLOC，先獨立驗證 CQMMS，再驗證 BIR，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：CQMMS, BIR, CMBLOC, CMB, BAR, Controller

- 來源 keyword 索引：`shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.9, Figure 47, 文件頁 67-68, PDF 頁 93-94

</details>

<details markdown="1">
<summary><strong>Figure 48: Offset 3Ch: CMBSZ - Controller Memory Buffer Size</strong></summary>

<!-- claim:BASE3-FIG-048-CLAIM figure-table:BASE3-FIG-048 -->

Figure 48〈Offset 3Ch: CMBSZ - Controller Memory Buffer Size〉：定義 offset 3Ch 的 CMBSZ（Controller Memory Buffer Size），並指出軟體在該位置必須分別解碼的欄位。 先定位 CMBSZ，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：SZ, SZU, WDS, RDS, LISTS, CQS, SQS, CMBSZ。

- 解決的問題：定義 offset 3Ch 的 CMBSZ（Controller Memory Buffer Size），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 CMBSZ，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：SZ, SZU, WDS, RDS, LISTS, CQS, SQS, CMBSZ。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 CMBSZ，先獨立驗證 SZ，再驗證 SZU，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：SZ, SZU, WDS, RDS, LISTS, CQS, SQS, CMBSZ

- 來源 keyword 索引：`shall not`, `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.11, Figure 48, 文件頁 68-69, PDF 頁 94-95

</details>

<details markdown="1">
<summary><strong>Figure 49: Offset 40h: BPINFO - Boot Partition Information</strong></summary>

<!-- claim:BASE3-FIG-049-CLAIM figure-table:BASE3-FIG-049 -->

Figure 49〈Offset 40h: BPINFO - Boot Partition Information〉：定義 offset 40h 的 BPINFO（Boot Partition Information），並指出軟體在該位置必須分別解碼的欄位。 先定位 BPINFO，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ABPID, BRS, BPSZ, BPINFO, ID, BPRSEL.BPID。

- 解決的問題：定義 offset 40h 的 BPINFO（Boot Partition Information），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 BPINFO，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ABPID, BRS, BPSZ, BPINFO, ID, BPRSEL.BPID。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 BPINFO，先獨立驗證 ABPID，再驗證 BRS，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：ABPID, BRS, BPSZ, BPINFO, ID, BPRSEL.BPID

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.12, Figure 49, 文件頁 69, PDF 頁 95

</details>

<details markdown="1">
<summary><strong>Figure 50: Offset 44h: BPRSEL - Boot Partition Read Select</strong></summary>

<!-- claim:BASE3-FIG-050-CLAIM figure-table:BASE3-FIG-050 -->

Figure 50〈Offset 44h: BPRSEL - Boot Partition Read Select〉：定義 offset 44h 的 BPRSEL（Boot Partition Read Select），並指出軟體在該位置必須分別解碼的欄位。 先定位 BPRSEL，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：BPID, BPROF, BPRSZ, BPRSEL。

- 解決的問題：定義 offset 44h 的 BPRSEL（Boot Partition Read Select），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 BPRSEL，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：BPID, BPROF, BPRSZ, BPRSEL。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 BPRSEL，先獨立驗證 BPID，再驗證 BPROF，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：BPID, BPROF, BPRSZ, BPRSEL

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.12, Figure 50, 文件頁 69-70, PDF 頁 95-96

</details>

<details markdown="1">
<summary><strong>Figure 51: Offset 48h: BPMBL - Boot Partition Memory Buffer Location</strong></summary>

<!-- claim:BASE3-FIG-051-CLAIM figure-table:BASE3-FIG-051 -->

Figure 51〈Offset 48h: BPMBL - Boot Partition Memory Buffer Location〉：定義 offset 48h 的 BPMBL（Boot Partition Memory Buffer Location），並指出軟體在該位置必須分別解碼的欄位。 先定位 BPMBL，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：BMBBA, BPMBL。

- 解決的問題：定義 offset 48h 的 BPMBL（Boot Partition Memory Buffer Location），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 BPMBL，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：BMBBA, BPMBL。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 BPMBL，先獨立驗證 BMBBA，再驗證 BPMBL，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：BMBBA, BPMBL

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 51, 文件頁 70, PDF 頁 96

</details>

<details markdown="1">
<summary><strong>Figure 52: Offset 50h: CMBMSC - Controller Memory Buffer Memory Space Control</strong></summary>

<!-- claim:BASE3-FIG-052-CLAIM figure-table:BASE3-FIG-052 -->

Figure 52〈Offset 50h: CMBMSC - Controller Memory Buffer Memory Space Control〉：定義 offset 50h 的 CMBMSC（Controller Memory Buffer Memory Space Control），並指出軟體在該位置必須分別解碼的欄位。 先定位 CMBMSC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CBA, CMSE, CRE, CMBMSC, CMBSMSC.CRE, CMBLOC, CMBSZ, Controller。

- 解決的問題：定義 offset 50h 的 CMBMSC（Controller Memory Buffer Memory Space Control），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 CMBMSC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CBA, CMSE, CRE, CMBMSC, CMBSMSC.CRE, CMBLOC, CMBSZ, Controller。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 CMBMSC，先獨立驗證 CBA，再驗證 CMSE，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：CBA, CMSE, CRE, CMBMSC, CMBSMSC.CRE, CMBLOC, CMBSZ, Controller

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 52, 文件頁 70-71, PDF 頁 96-97

</details>

<details markdown="1">
<summary><strong>Figure 53: Offset 58h: CMBSTS - Controller Memory Buffer Status</strong></summary>

<!-- claim:BASE3-FIG-053-CLAIM figure-table:BASE3-FIG-053 -->

Figure 53〈Offset 58h: CMBSTS - Controller Memory Buffer Status〉：定義 offset 58h 的 CMBSTS（Controller Memory Buffer Status），並指出軟體在該位置必須分別解碼的欄位。 先定位 CMBSTS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CBAI, CMBSTS, CMBMSC.CBA, CMBMSC.CRE, CMBMSC.CMSE, Controller。

- 解決的問題：定義 offset 58h 的 CMBSTS（Controller Memory Buffer Status），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 CMBSTS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CBAI, CMBSTS, CMBMSC.CBA, CMBMSC.CRE, CMBMSC.CMSE, Controller。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 CMBSTS，先獨立驗證 CBAI，再驗證 CMBSTS，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：CBAI, CMBSTS, CMBMSC.CBA, CMBMSC.CRE, CMBMSC.CMSE, Controller

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.16, Figure 53, 文件頁 71, PDF 頁 97

</details>

<details markdown="1">
<summary><strong>Figure 54: Offset 5Ch: CMBEBS - Controller Memory Buffer Elasticity Buffer Size</strong></summary>

<!-- claim:BASE3-FIG-054-CLAIM figure-table:BASE3-FIG-054 -->

Figure 54〈Offset 5Ch: CMBEBS - Controller Memory Buffer Elasticity Buffer Size〉：定義 offset 5Ch 的 CMBEBS（Controller Memory Buffer Elasticity Buffer Size），並指出軟體在該位置必須分別解碼的欄位。 先定位 CMBEBS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CMBWBZ, CMBRBB, CMBSZU, CMBEBS, CMB, Controller。

- 解決的問題：定義 offset 5Ch 的 CMBEBS（Controller Memory Buffer Elasticity Buffer Size），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 CMBEBS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CMBWBZ, CMBRBB, CMBSZU, CMBEBS, CMB, Controller。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 CMBEBS，先獨立驗證 CMBWBZ，再驗證 CMBRBB，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：CMBWBZ, CMBRBB, CMBSZU, CMBEBS, CMB, Controller

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.16, Figure 54, 文件頁 71, PDF 頁 97

</details>

<details markdown="1">
<summary><strong>Figure 55: Offset 60h: CMBSWTP - Controller Memory Buffer Sustained Write Throughput</strong></summary>

<!-- claim:BASE3-FIG-055-CLAIM figure-table:BASE3-FIG-055 -->

Figure 55〈Offset 60h: CMBSWTP - Controller Memory Buffer Sustained Write Throughput〉：定義 offset 60h 的 CMBSWTP（Controller Memory Buffer Sustained Write Throughput），並指出軟體在該位置必須分別解碼的欄位。 先定位 CMBSWTP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CMBSWTV, CMBSWTU, CMBSWTP, CMB, TLP, MPS, PXDC, Controller。

- 解決的問題：定義 offset 60h 的 CMBSWTP（Controller Memory Buffer Sustained Write Throughput），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 CMBSWTP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CMBSWTV, CMBSWTU, CMBSWTP, CMB, TLP, MPS, PXDC, Controller。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 CMBSWTP，先獨立驗證 CMBSWTV，再驗證 CMBSWTU，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：CMBSWTV, CMBSWTU, CMBSWTP, CMB, TLP, MPS, PXDC, Controller

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.19, Figure 55, 文件頁 72, PDF 頁 98

</details>

<details markdown="1">
<summary><strong>Figure 56: Offset 64h: NSSD - NVM Subsystem Shutdown</strong></summary>

<!-- claim:BASE3-FIG-056-CLAIM figure-table:BASE3-FIG-056 -->

Figure 56〈Offset 64h: NSSD - NVM Subsystem Shutdown〉：定義 offset 64h 的 NSSD（NVM Subsystem Shutdown），並指出軟體在該位置必須分別解碼的欄位。 先定位 NSSD，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NSSC, NSSD, CAP.CPS, NVM Subsystem。

- 解決的問題：定義 offset 64h 的 NSSD（NVM Subsystem Shutdown），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 NSSD，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NSSC, NSSD, CAP.CPS, NVM Subsystem。

- 條件與限制：來源 keyword 索引：`shall`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 NSSD，先獨立驗證 NSSC，再驗證 NSSD，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：NSSC, NSSD, CAP.CPS, NVM Subsystem

- 來源 keyword 索引：`shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.19, Figure 56, 文件頁 72, PDF 頁 98

</details>

<details markdown="1">
<summary><strong>Figure 57: Offset 68h: CRTO - Controller Ready Timeouts</strong></summary>

<!-- claim:BASE3-FIG-057-CLAIM figure-table:BASE3-FIG-057 -->

Figure 57〈Offset 68h: CRTO - Controller Ready Timeouts〉：定義 offset 68h 的 CRTO（Controller Ready Timeouts），並指出軟體在該位置必須分別解碼的欄位。 先定位 CRTO，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CRIMT, CRWMT, CRTO, CAP.CRMS.CRIMS, CC.EN, CC.CRIME, CRTO.CRIMT, Controller。

- 解決的問題：定義 offset 68h 的 CRTO（Controller Ready Timeouts），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 CRTO，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CRIMT, CRWMT, CRTO, CAP.CRMS.CRIMS, CC.EN, CC.CRIME, CRTO.CRIMT, Controller。

- 條件與限制：來源 keyword 索引：`should not`, `shall`, `should`, `may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 CRTO，先獨立驗證 CRIMT，再驗證 CRWMT，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：CRIMT, CRWMT, CRTO, CAP.CRMS.CRIMS, CC.EN, CC.CRIME, CRTO.CRIMT, Controller

- 來源 keyword 索引：`should not`, `shall`, `should`, `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.21, Figure 57, 文件頁 73, PDF 頁 99

</details>

<details markdown="1">
<summary><strong>Figure 58: Offset E00h: PMRCAP - Persistent Memory Region Capabilities</strong></summary>

<!-- claim:BASE3-FIG-058-CLAIM figure-table:BASE3-FIG-058 -->

Figure 58〈Offset E00h: PMRCAP - Persistent Memory Region Capabilities〉：定義 offset E00h 的 PMRCAP（Persistent Memory Region Capabilities），並指出軟體在該位置必須分別解碼的欄位。 先定位 PMRCAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CMSS, PMRTO, PMRWBM, CPMTSTSR, CMR, PMRTU, BIR, WDS。

- 解決的問題：定義 offset E00h 的 PMRCAP（Persistent Memory Region Capabilities），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PMRCAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CMSS, PMRTO, PMRWBM, CPMTSTSR, CMR, PMRTU, BIR, WDS。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `should`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PMRCAP，先獨立驗證 CMSS，再驗證 PMRTO，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：CMSS, PMRTO, PMRWBM, CPMTSTSR, CMR, PMRTU, BIR, WDS

- 來源 keyword 索引：`shall not`, `shall`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.21, Figure 58, 文件頁 73-74, PDF 頁 99-100

</details>

<details markdown="1">
<summary><strong>Figure 59: Offset E04h: PMRCTL - Persistent Memory Region Control</strong></summary>

<!-- claim:BASE3-FIG-059-CLAIM figure-table:BASE3-FIG-059 -->

Figure 59〈Offset E04h: PMRCTL - Persistent Memory Region Control〉：定義 offset E04h 的 PMRCTL（Persistent Memory Region Control），並指出軟體在該位置必須分別解碼的欄位。 先定位 PMRCTL，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：EN, PMRCTL, PMRSTS.NRDY。

- 解決的問題：定義 offset E04h 的 PMRCTL（Persistent Memory Region Control），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PMRCTL，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：EN, PMRCTL, PMRSTS.NRDY。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PMRCTL，先獨立驗證 EN，再驗證 PMRCTL，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：EN, PMRCTL, PMRSTS.NRDY

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.22, Figure 59, 文件頁 74, PDF 頁 100

</details>

<details markdown="1">
<summary><strong>Figure 60: Offset E08h: PMRSTS - Persistent Memory Region Status</strong></summary>

<!-- claim:BASE3-FIG-060-CLAIM figure-table:BASE3-FIG-060 -->

Figure 60〈Offset E08h: PMRSTS - Persistent Memory Region Status〉：定義 offset E08h 的 PMRSTS（Persistent Memory Region Status），並指出軟體在該位置必須分別解碼的欄位。 先定位 PMRSTS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CBAI, HSTS, NRDY, ERR, PMRSTS, PMRMSCU.CBA, PMRMSCL.CBA, PMRCAP.CMSS。

- 解決的問題：定義 offset E08h 的 PMRSTS（Persistent Memory Region Status），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PMRSTS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CBAI, HSTS, NRDY, ERR, PMRSTS, PMRMSCU.CBA, PMRMSCL.CBA, PMRCAP.CMSS。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PMRSTS，先獨立驗證 CBAI，再驗證 HSTS，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：CBAI, HSTS, NRDY, ERR, PMRSTS, PMRMSCU.CBA, PMRMSCL.CBA, PMRCAP.CMSS

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.23, Figure 60, 文件頁 75, PDF 頁 101

</details>

<details markdown="1">
<summary><strong>Figure 61: Offset E0Ch: PMREBS - Persistent Memory Region Elasticity Buffer Size</strong></summary>

<!-- claim:BASE3-FIG-061-CLAIM figure-table:BASE3-FIG-061 -->

Figure 61〈Offset E0Ch: PMREBS - Persistent Memory Region Elasticity Buffer Size〉：定義 offset E0Ch 的 PMREBS（Persistent Memory Region Elasticity Buffer Size），並指出軟體在該位置必須分別解碼的欄位。 先定位 PMREBS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PMRWBZ, PMRRBB, PMRSZU, PMREBS, PMR。

- 解決的問題：定義 offset E0Ch 的 PMREBS（Persistent Memory Region Elasticity Buffer Size），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PMREBS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PMRWBZ, PMRRBB, PMRSZU, PMREBS, PMR。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PMREBS，先獨立驗證 PMRWBZ，再驗證 PMRRBB，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：PMRWBZ, PMRRBB, PMRSZU, PMREBS, PMR

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.24, Figure 61, 文件頁 76, PDF 頁 102

</details>

<details markdown="1">
<summary><strong>Figure 62: Offset E10h: PMRSWTP - Persistent Memory Region Sustained Write Throughput</strong></summary>

<!-- claim:BASE3-FIG-062-CLAIM figure-table:BASE3-FIG-062 -->

Figure 62〈Offset E10h: PMRSWTP - Persistent Memory Region Sustained Write Throughput〉：定義 offset E10h 的 PMRSWTP（Persistent Memory Region Sustained Write Throughput），並指出軟體在該位置必須分別解碼的欄位。 先定位 PMRSWTP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PMRSWTV, PMRSWTU, PMRSWTP, PMR, TLP, MPS, PXDC。

- 解決的問題：定義 offset E10h 的 PMRSWTP（Persistent Memory Region Sustained Write Throughput），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PMRSWTP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PMRSWTV, PMRSWTU, PMRSWTP, PMR, TLP, MPS, PXDC。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PMRSWTP，先獨立驗證 PMRSWTV，再驗證 PMRSWTU，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：PMRSWTV, PMRSWTU, PMRSWTP, PMR, TLP, MPS, PXDC

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.24, Figure 62, 文件頁 76, PDF 頁 102

</details>

<details markdown="1">
<summary><strong>Figure 63: Offset E14h: PMRMSCL - Persistent Memory Region Memory Space Control Lower</strong></summary>

<!-- claim:BASE3-FIG-063-CLAIM figure-table:BASE3-FIG-063 -->

Figure 63〈Offset E14h: PMRMSCL - Persistent Memory Region Memory Space Control Lower〉：定義 offset E14h 的 PMRMSCL（Persistent Memory Region Memory Space Control Lower），並指出軟體在該位置必須分別解碼的欄位。 先定位 PMRMSCL，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CBA, CMSE, PMRMSCL, PMRMSCU.CBA。

- 解決的問題：定義 offset E14h 的 PMRMSCL（Persistent Memory Region Memory Space Control Lower），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PMRMSCL，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CBA, CMSE, PMRMSCL, PMRMSCU.CBA。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依規定寬度讀取 PMRMSCL，先獨立驗證 CBA，再驗證 CMSE，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：CBA, CMSE, PMRMSCL, PMRMSCU.CBA

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.26, Figure 63, 文件頁 77, PDF 頁 103

</details>

<details markdown="1">
<summary><strong>Figure 64: Offset E18h: PMRMSCU - Persistent Memory Region Memory Space Control Upper</strong></summary>

<!-- claim:BASE3-FIG-064-CLAIM figure-table:BASE3-FIG-064 -->

Figure 64〈Offset E18h: PMRMSCU - Persistent Memory Region Memory Space Control Upper〉：定義 offset E18h 的 PMRMSCU（Persistent Memory Region Memory Space Control Upper），並指出軟體在該位置必須分別解碼的欄位。 先定位 PMRMSCU，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CBA, PMRMSCU。

- 解決的問題：定義 offset E18h 的 PMRMSCU（Persistent Memory Region Memory Space Control Upper），並指出軟體在該位置必須分別解碼的欄位。

- 閱讀順序：先定位 PMRMSCU，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CBA, PMRMSCU。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依規定寬度讀取 PMRMSCU，先獨立驗證 CBA，再驗證 PMRMSCU，確認後才使用欄位值。 此例不新增規格要求。

- 來源欄位索引：CBA, PMRMSCU

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.26, Figure 64, 文件頁 77, PDF 頁 103

</details>

<a id="section-3-2"></a>

### §3.2

<details markdown="1">
<summary><strong>Figure 65: NSID Types and Relationship to Namespace</strong></summary>

<!-- claim:BASE3-FIG-065-CLAIM figure-table:BASE3-FIG-065 -->

Figure 65〈NSID Types and Relationship to Namespace〉：定義〈NSID Types and Relationship to Namespace〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NSID, Namespace。

- 解決的問題：定義〈NSID Types and Relationship to Namespace〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NSID, Namespace。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依定義寬度解析 NSID，再核對 Namespace 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：NSID, Namespace

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.1, Figure 65, 文件頁 78-79, PDF 頁 104-105

</details>

<details markdown="1">
<summary><strong>Figure 66: NSID Types</strong></summary>

<!-- claim:BASE3-FIG-066-CLAIM figure-table:BASE3-FIG-066 -->

Figure 66〈NSID Types〉：定義〈NSID Types〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NSID。

- 解決的問題：定義〈NSID Types〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NSID。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依定義寬度解析 NSID，再核對 引用條件 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：NSID

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.1.5, Figure 66, 文件頁 79, PDF 頁 105

</details>

<details markdown="1">
<summary><strong>Figure 67: NVM Sets and Associated Namespaces</strong></summary>

<!-- claim:BASE3-FIG-067-CLAIM figure-table:BASE3-FIG-067 -->

Figure 67〈NVM Sets and Associated Namespaces〉：呈現〈NVM Sets and Associated Namespaces〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Set, Namespace。

- 解決的問題：呈現〈NVM Sets and Associated Namespaces〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Set, Namespace。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Set 標示的一個物件，再追到 Namespace，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Set, Namespace

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2, Figure 67, 文件頁 81, PDF 頁 107

</details>

<details markdown="1">
<summary><strong>Figure 68: NVM Set Aware Admin Commands</strong></summary>

<!-- claim:BASE3-FIG-068-CLAIM figure-table:BASE3-FIG-068 -->

Figure 68〈NVM Set Aware Admin Commands〉：呈現〈NVM Set Aware Admin Commands〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Set, Command。

- 解決的問題：呈現〈NVM Set Aware Admin Commands〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Set, Command。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Set 標示的一個物件，再追到 Command，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Set, Command

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2, Figure 68, 文件頁 81, PDF 頁 107

</details>

<details markdown="1">
<summary><strong>Figure 69: NVM Sets and Associated Namespaces</strong></summary>

<!-- claim:BASE3-FIG-069-CLAIM figure-table:BASE3-FIG-069 -->

Figure 69〈NVM Sets and Associated Namespaces〉：呈現〈NVM Sets and Associated Namespaces〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Set, Namespace。

- 解決的問題：呈現〈NVM Sets and Associated Namespaces〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Set, Namespace。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Set 標示的一個物件，再追到 Namespace，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Set, Namespace

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.3, Figure 69, 文件頁 83, PDF 頁 109

</details>

<details markdown="1">
<summary><strong>Figure 70: Flexible Data Placement Logical View of Non-Volatile Storage</strong></summary>

<!-- claim:BASE3-FIG-070-CLAIM figure-table:BASE3-FIG-070 -->

Figure 70〈Flexible Data Placement Logical View of Non-Volatile Storage〉：呈現〈Flexible Data Placement Logical View of Non-Volatile Storage〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：Flexible Data Placement Logical View of Non-Volatile Storage。

- 解決的問題：呈現〈Flexible Data Placement Logical View of Non-Volatile Storage〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：Flexible Data Placement Logical View of Non-Volatile Storage。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 Flexible Data Placement Logical View of Non-Volatile Storage 標示的一個物件，再追到 引用條件，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：Flexible Data Placement Logical View of Non-Volatile Storage

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.4, Figure 70, 文件頁 85, PDF 頁 111

</details>

<details markdown="1">
<summary><strong>Figure 71: Example 1 Domain Structure</strong></summary>

<!-- claim:BASE3-FIG-071-CLAIM figure-table:BASE3-FIG-071 -->

Figure 71〈Example 1 Domain Structure〉：定義〈Example 1 Domain Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Domain。

- 解決的問題：定義〈Example 1 Domain Structure〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Domain。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：以 Domain 作為 parser 的第一個檢查點，再用 引用條件 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：Domain

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.5.1, Figure 71, 文件頁 86, PDF 頁 112

</details>

<a id="section-3-3"></a>

### §3.3

<details markdown="1">
<summary><strong>Figure 73: Empty Queue Definition</strong></summary>

<!-- claim:BASE3-FIG-073-CLAIM figure-table:BASE3-FIG-073 -->

Figure 73〈Empty Queue Definition〉：定義〈Empty Queue Definition〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Empty Queue Definition。

- 解決的問題：定義〈Empty Queue Definition〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Empty Queue Definition。

- 條件與限制：來源 keyword 索引：`shall`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 Empty Queue Definition 作為 parser 的第一個檢查點，再用 引用條件 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：Empty Queue Definition

- 來源 keyword 索引：`shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1.4, Figure 73, 文件頁 91, PDF 頁 117

</details>

<details markdown="1">
<summary><strong>Figure 74: Full Queue Definition</strong></summary>

<!-- claim:BASE3-FIG-074-CLAIM figure-table:BASE3-FIG-074 -->

Figure 74〈Full Queue Definition〉：定義〈Full Queue Definition〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Full Queue Definition。

- 解決的問題：定義〈Full Queue Definition〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Full Queue Definition。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：以 Full Queue Definition 作為 parser 的第一個檢查點，再用 引用條件 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：Full Queue Definition

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1.4, Figure 74, 文件頁 91, PDF 頁 117

</details>

<a id="section-3-4"></a>

### §3.4

<details markdown="1">
<summary><strong>Figure 80: Round Robin Arbitration</strong></summary>

<!-- claim:BASE3-FIG-080-CLAIM figure-table:BASE3-FIG-080 -->

Figure 80〈Round Robin Arbitration〉：呈現〈Round Robin Arbitration〉如何在多個 Submission Queue 間選擇工作。 分別追蹤 priority class、服務順序與 arbiter 選出下一筆 command 的時點；來源索引：Round Robin Arbitration。

- 解決的問題：呈現〈Round Robin Arbitration〉如何在多個 Submission Queue 間選擇工作。

- 閱讀順序：分別追蹤 priority class、服務順序與 arbiter 選出下一筆 command 的時點；來源索引：Round Robin Arbitration。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：比較 Round Robin Arbitration 與 引用條件 所代表的 queue，再只推進由規定 arbitration rule 選中的 queue。 此例不新增規格要求。

- 來源欄位索引：Round Robin Arbitration

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.4.4, Figure 80, 文件頁 103, PDF 頁 129

</details>

<details markdown="1">
<summary><strong>Figure 81: Weighted Round Robin with Urgent Priority Class Arbitration</strong></summary>

<!-- claim:BASE3-FIG-081-CLAIM figure-table:BASE3-FIG-081 -->

Figure 81〈Weighted Round Robin with Urgent Priority Class Arbitration〉：呈現〈Weighted Round Robin with Urgent Priority Class Arbitration〉如何在多個 Submission Queue 間選擇工作。 分別追蹤 priority class、服務順序與 arbiter 選出下一筆 command 的時點；來源索引：Weighted Round Robin with Urgent Priority Class Arbitration。

- 解決的問題：呈現〈Weighted Round Robin with Urgent Priority Class Arbitration〉如何在多個 Submission Queue 間選擇工作。

- 閱讀順序：分別追蹤 priority class、服務順序與 arbiter 選出下一筆 command 的時點；來源索引：Weighted Round Robin with Urgent Priority Class Arbitration。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：比較 Weighted Round Robin with Urgent Priority Class Arbitration 與 引用條件 所代表的 queue，再只推進由規定 arbitration rule 選中的 queue。 此例不新增規格要求。

- 來源欄位索引：Weighted Round Robin with Urgent Priority Class Arbitration

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.4.4.2, Figure 81, 文件頁 104, PDF 頁 130

</details>

<a id="section-3-5"></a>

### §3.5

<details markdown="1">
<summary><strong>Figure 84: Admin Commands Permitted to Return a Status Code of Admin Command Media Not</strong></summary>

<!-- claim:BASE3-FIG-084-CLAIM figure-table:BASE3-FIG-084 -->

Figure 84〈Admin Commands Permitted to Return a Status Code of Admin Command Media Not〉：定義〈Admin Commands Permitted to Return a Status Code of Admin Command Media Not〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：LBA, TCG, CAP.CRMS, CAP.CRMS.CRWMS, CAP.CRMS.CRIMS, CC.CRIME, Status Code, Command。

- 解決的問題：定義〈Admin Commands Permitted to Return a Status Code of Admin Command Media Not〉所表示的 status／error 分類。

- 閱讀順序：先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：LBA, TCG, CAP.CRMS, CAP.CRMS.CRWMS, CAP.CRMS.CRIMS, CC.CRIME, Status Code, Command。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 本報告只解釋 PCIe／memory-based 部分。

- 說明性範例（informative example）：收到一筆狀態時先辨認 LBA，再檢查 TCG，不可脫離類別單看數值。 此例不新增規格要求。

- 來源欄位索引：LBA, TCG, CAP.CRMS, CAP.CRMS.CRWMS, CAP.CRMS.CRIMS, CC.CRIME, Status Code, Command

- 來源 keyword 索引：`shall`, `should`, `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.5.3, Figure 84, 文件頁 110-111, PDF 頁 136-137

</details>

<a id="section-3-6"></a>

### §3.6

<details markdown="1">
<summary><strong>Figure 85: Shutdown Processing Interactions</strong></summary>

<!-- claim:BASE3-FIG-085-CLAIM figure-table:BASE3-FIG-085 -->

Figure 85〈Shutdown Processing Interactions〉：呈現〈Shutdown Processing Interactions〉的狀態或時間推進關係。 依箭頭順序追蹤 state 或 time bound，並標出每個 transition 的觀察者；來源索引：Shutdown Processing Interactions。

- 解決的問題：呈現〈Shutdown Processing Interactions〉的狀態或時間推進關係。

- 閱讀順序：依箭頭順序追蹤 state 或 time bound，並標出每個 transition 的觀察者；來源索引：Shutdown Processing Interactions。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。 本報告只解釋 PCIe／memory-based 部分。

- 說明性範例（informative example）：從 Shutdown Processing Interactions 開始，記錄到達 引用條件 的 transition，只在規定邊界判斷 timeout 或 reset 行為。 此例不新增規格要求。

- 來源欄位索引：Shutdown Processing Interactions

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.6, Figure 85, 文件頁 113, PDF 頁 139

</details>

<a id="section-3-8"></a>

### §3.8

<details markdown="1">
<summary><strong>Figure 86: Simple NVM Subsystem</strong></summary>

<!-- claim:BASE3-FIG-086-CLAIM figure-table:BASE3-FIG-086 -->

Figure 86〈Simple NVM Subsystem〉：呈現〈Simple NVM Subsystem〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem。

- 解決的問題：呈現〈Simple NVM Subsystem〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Subsystem 標示的一個物件，再追到 引用條件，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Subsystem

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.8.2, Figure 86, 文件頁 126, PDF 頁 152

</details>

<details markdown="1">
<summary><strong>Figure 87: Vertically-Organized NVM Subsystem</strong></summary>

<!-- claim:BASE3-FIG-087-CLAIM figure-table:BASE3-FIG-087 -->

Figure 87〈Vertically-Organized NVM Subsystem〉：呈現〈Vertically-Organized NVM Subsystem〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem。

- 解決的問題：呈現〈Vertically-Organized NVM Subsystem〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Subsystem 標示的一個物件，再追到 引用條件，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Subsystem

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.8.2.2, Figure 87, 文件頁 127, PDF 頁 153

</details>

<details markdown="1">
<summary><strong>Figure 88: Horizontally-Organized Dual NAND NVM Subsystem</strong></summary>

<!-- claim:BASE3-FIG-088-CLAIM figure-table:BASE3-FIG-088 -->

Figure 88〈Horizontally-Organized Dual NAND NVM Subsystem〉：呈現〈Horizontally-Organized Dual NAND NVM Subsystem〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NAND, NVM Subsystem。

- 解決的問題：呈現〈Horizontally-Organized Dual NAND NVM Subsystem〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NAND, NVM Subsystem。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NAND 標示的一個物件，再追到 NVM Subsystem，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NAND, NVM Subsystem

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.8.2.3, Figure 88, 文件頁 128, PDF 頁 154

</details>

<details markdown="1">
<summary><strong>Figure 89: Capacity Information Field Usage</strong></summary>

<!-- claim:BASE3-FIG-089-CLAIM figure-table:BASE3-FIG-089 -->

Figure 89〈Capacity Information Field Usage〉：定義〈Capacity Information Field Usage〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TNVMCAP, UNVMCAP, MEGCAP, TEGCAP, UEGCAP。

- 解決的問題：定義〈Capacity Information Field Usage〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TNVMCAP, UNVMCAP, MEGCAP, TEGCAP, UEGCAP。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：以 TNVMCAP 作為 parser 的第一個檢查點，再用 UNVMCAP 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：TNVMCAP, UNVMCAP, MEGCAP, TEGCAP, UEGCAP

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.8.3, Figure 89, 文件頁 129, PDF 頁 155

</details>

<a id="section-3-9"></a>

### §3.9

<details markdown="1">
<summary><strong>Figure 90: Detecting Timeout Takes up to 2 * KATT</strong></summary>

<!-- claim:BASE3-FIG-090-CLAIM figure-table:BASE3-FIG-090 -->

Figure 90〈Detecting Timeout Takes up to 2 * KATT〉：呈現〈Detecting Timeout Takes up to 2 * KATT〉的狀態或時間推進關係。 依箭頭順序追蹤 state 或 time bound，並標出每個 transition 的觀察者；來源索引：KATT。

- 解決的問題：呈現〈Detecting Timeout Takes up to 2 * KATT〉的狀態或時間推進關係。

- 閱讀順序：依箭頭順序追蹤 state 或 time bound，並標出每個 transition 的觀察者；來源索引：KATT。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。 本報告只解釋 PCIe／memory-based 部分。

- 說明性範例（informative example）：從 KATT 開始，記錄到達 引用條件 的 transition，只在規定邊界判斷 timeout 或 reset 行為。 此例不新增規格要求。

- 來源欄位索引：KATT

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.9.4.1, Figure 90, 文件頁 133, PDF 頁 159

</details>

<a id="section-3-10"></a>

### §3.10

<details markdown="1">
<summary><strong>Figure 91: Example Privileged Action Admin Commands</strong></summary>

<!-- claim:BASE3-FIG-091-CLAIM figure-table:BASE3-FIG-091 -->

Figure 91〈Example Privileged Action Admin Commands〉：界定〈Example Privileged Action Admin Commands〉所示的 privileged operation 邊界。 分開發出 command 的主體，以及授權該操作的 privilege／controller state；來源索引：Command。

- 解決的問題：界定〈Example Privileged Action Admin Commands〉所示的 privileged operation 邊界。

- 閱讀順序：分開發出 command 的主體，以及授權該操作的 privilege／controller state；來源索引：Command。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。 本報告只解釋 PCIe／memory-based 部分。

- 說明性範例（informative example）：先核對 Command，再確認 引用條件 對應的授權條件成立後才發出操作。 此例不新增規格要求。

- 來源欄位索引：Command

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.10, Figure 91, 文件頁 135, PDF 頁 161

</details>

## 使用與限制

製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata 集合或核准範圍改變時，必須重新核對受影響 claim。
