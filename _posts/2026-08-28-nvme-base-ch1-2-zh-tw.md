---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4 第 1、2 章：規格語言、PCIe 佇列與儲存模型"
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

# NVMe Base 2.4 第 1、2 章：規格語言、PCIe 佇列與儲存模型

用途：供 GitHub Pages 閱讀與 100 分鐘簡報製作；讀者已具備 PCIe 與 NVMe 基礎。

範圍：§1-§2；文件頁 1-37；PDF 頁 27-63。正文只保留 PCIe／memory-based 與通用 NVMe 內容。

## 來源版本

NVM Express Base Specification, Revision 2.4

查證日期：2026-08-29。目前未納入其他 Errata、ECN、Technical Proposal、controller vendor 文件或未提供的 PCI Express Base Specification 原文。

## 閱讀地圖

```text
Host / CPU core -> Submission Queue -> NVMe controller -> Completion Queue
```

命令由 host 放入 Submission Queue；controller 取走並執行，再把完成結果寫入 Completion Queue。

## 規範性用語

shall 譯為「必須」，may 譯為「可／得」，should 譯為「宜／建議」，optional 譯為「選用」。本文不提高或降低原文語氣。

## 規格重點

### 1. NVMe 規格家族的分工

<!-- claim:BASE12-FAMILY -->

Base Specification 定義通用 NVMe 協定；Transport Specification 綁定特定傳輸，I/O Command Set Specification 擴充命令與資料結構。這是適用關係，不是協定堆疊。

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.1.1, 文件頁 1, PDF 頁 27

### 2. 規範性用語的強度

<!-- claim:BASE12-KEYWORDS -->

規格的 mandatory、may、optional、reserved、shall、should 各有固定語氣；詳細版保留英文 keyword，不能把 may 或 should 翻成 shall。

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.4.1, 文件頁 2-3, PDF 頁 28-29

### 3. 進位與容量單位

<!-- claim:BASE12-NUMBERS -->

數值的解讀同時包含進位與單位；十六進位使用 h 後綴，二進位使用 b 後綴，十進位可省略 d。十進位與二進位容量前綴代表不同倍率。

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.4.2, 文件頁 3-5, PDF 頁 29-31

### 4. byte、word 與 dword

<!-- claim:BASE12-DWORD -->

NVMe 以 byte、word、dword 表示欄位位置；一個 word 為 2 bytes，一個 dword 為 4 bytes。解欄位時先確認 byte 與 bit 編號。

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.4.3, 文件頁 5, PDF 頁 31

### 5. PCIe queue pair 模型

<!-- claim:BASE12-QUEUE -->

PCIe memory-based model 把 Submission Queue 與 Completion Queue 配置在記憶體。多個 I/O Submission Queues 可共用一個 I/O Completion Queue；Admin queue pair 維持一對一。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.1, 文件頁 21-23, PDF 頁 47-49

### 6. NVM 儲存階層

<!-- claim:BASE12-STORAGE -->

儲存模型用 NVM subsystem、domain、Endurance Group、NVM Set／Reclaim Group、Reclaim Unit 與 namespace 表達包含關係。namespace 是 host 實際透過 controller 存取的格式化容量。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, 文件頁 26-33, PDF 頁 52-59

### 7. Admin 與 I/O Command Set

<!-- claim:BASE12-COMMANDSET -->

Admin Command Set 管理 controller 與 queue；I/O Command Set 定義對 namespace 的資料操作。Base 說明通用機制，個別 I/O Command Set Specification 說明命令語意。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.2, 文件頁 33, PDF 頁 59

### 8. subsystem 物件與 NSID

<!-- claim:BASE12-SUBSYSTEM -->

controller、port、namespace 與 PCI Function 是不同物件；NSID 是 controller 用來指向 namespace 的 handle，不是 namespace 本身。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.3, 文件頁 33-35, PDF 頁 59-61

### 9. multi-path 與 namespace sharing

<!-- claim:BASE12-MULTIPATH -->

multi-path I/O 是同一 host 到同一 namespace 的兩條以上獨立路徑；namespace sharing 是兩個以上 host 經不同 controller 存取同一 shared namespace。兩者都需要至少兩個 controller。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, 文件頁 35-37, PDF 頁 61-63

### 10. 非對稱路徑特性

<!-- claim:BASE12-ASYMMETRY -->

支援多路徑或共享時，各 controller 對同一 namespace 的存取特性不一定相同；host 可依 controller 所回報的狀態選擇路徑。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.4.2, 文件頁 37, PDF 頁 63

## Figure 索引

本報告介紹全部 18 張納入範圍的 Figure。100 分鐘簡報以 section 主線與必講 Figure 為主，其餘 Figure 仍完整保留作為附錄。

- [§1.1](#section-1-1)

- [§1.4](#section-1-4)

- [§2](#section-2)

- [§2.1](#section-2-1)

- [§2.3](#section-2-3)

- [§2.4](#section-2-4)

## Figure 逐圖導讀

本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。欄位與 keyword 索引來自本機核對過的 PDF。

<a id="section-1-1"></a>

### §1.1

<details markdown="1">
<summary><strong>Figure 1: NVMe Family of Specifications</strong></summary>

<!-- claim:BASE12-FIG-001-CLAIM figure-table:BASE12-FIG-001 -->

Figure 1〈NVMe Family of Specifications〉：定位〈NVMe Family of Specifications〉在 NVMe 文件與 command set 階層中的位置。 由共通 Base 要求往 transport 與 command set 分支閱讀，並分開核對：NVMe Family。

- 解決的問題：定位〈NVMe Family of Specifications〉在 NVMe 文件與 command set 階層中的位置。

- 閱讀順序：由共通 Base 要求往 transport 與 command set 分支閱讀，並分開核對：NVMe Family。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。 本報告只解釋 PCIe／memory-based 部分。

- 說明性範例（informative example）：先從 NVMe Family 出發，再沿包含 引用條件 的分支找定義來源，不假設每一層都重複定義同一要求。 此例不新增規格要求。

- 來源欄位索引：NVMe Family

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.1.1, Figure 1, 文件頁 1, PDF 頁 27

</details>

<a id="section-1-4"></a>

### §1.4

<details markdown="1">
<summary><strong>Figure 2: Decimal and Binary Units</strong></summary>

<!-- claim:BASE12-FIG-002-CLAIM figure-table:BASE12-FIG-002 -->

Figure 2〈Decimal and Binary Units〉：定義〈Decimal and Binary Units〉使用的數值單位或 byte 寬度慣例。 分開十進位與二進位單位，並保留 byte／word／Dword 邊界；來源索引：Decimal and Binary Units。

- 解決的問題：定義〈Decimal and Binary Units〉使用的數值單位或 byte 寬度慣例。

- 閱讀順序：分開十進位與二進位單位，並保留 byte／word／Dword 邊界；來源索引：Decimal and Binary Units。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：先依 Decimal and Binary Units 正規化一個數值，再用 引用條件 核對儲存寬度後才進行比較。 此例不新增規格要求。

- 來源欄位索引：Decimal and Binary Units

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.4.2, Figure 2, 文件頁 3, PDF 頁 29

</details>

<details markdown="1">
<summary><strong>Figure 3: Byte, Word, and Dword Relationships</strong></summary>

<!-- claim:BASE12-FIG-003-CLAIM figure-table:BASE12-FIG-003 -->

Figure 3〈Byte, Word, and Dword Relationships〉：定義〈Byte, Word, and Dword Relationships〉使用的數值單位或 byte 寬度慣例。 分開十進位與二進位單位，並保留 byte／word／Dword 邊界；來源索引：Byte, Word, and Dword Relationships。

- 解決的問題：定義〈Byte, Word, and Dword Relationships〉使用的數值單位或 byte 寬度慣例。

- 閱讀順序：分開十進位與二進位單位，並保留 byte／word／Dword 邊界；來源索引：Byte, Word, and Dword Relationships。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：先依 Byte, Word, and Dword Relationships 正規化一個數值，再用 引用條件 核對儲存寬度後才進行比較。 此例不新增規格要求。

- 來源欄位索引：Byte, Word, and Dword Relationships

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.4.3, Figure 3, 文件頁 5, PDF 頁 31

</details>

<a id="section-2"></a>

### §2

<details markdown="1">
<summary><strong>Figure 5: Types of NVMe Command Sets</strong></summary>

<!-- claim:BASE12-FIG-005-CLAIM figure-table:BASE12-FIG-005 -->

Figure 5〈Types of NVMe Command Sets〉：定位〈Types of NVMe Command Sets〉在 NVMe 文件與 command set 階層中的位置。 由共通 Base 要求往 transport 與 command set 分支閱讀，並分開核對：Command Set, Command。

- 解決的問題：定位〈Types of NVMe Command Sets〉在 NVMe 文件與 command set 階層中的位置。

- 閱讀順序：由共通 Base 要求往 transport 與 command set 分支閱讀，並分開核對：Command Set, Command。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。 本報告只解釋 PCIe／memory-based 部分。

- 說明性範例（informative example）：先從 Command Set 出發，再沿包含 Command 的分支找定義來源，不假設每一層都重複定義同一要求。 此例不新增規格要求。

- 來源欄位索引：Command Set, Command

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2, Figure 5, 文件頁 21, PDF 頁 47

</details>

<a id="section-2-1"></a>

### §2.1

<details markdown="1">
<summary><strong>Figure 6: Queue Pair Example, 1:1 Mapping</strong></summary>

<!-- claim:BASE12-FIG-006-CLAIM figure-table:BASE12-FIG-006 -->

Figure 6〈Queue Pair Example, 1:1 Mapping〉：呈現〈Queue Pair Example, 1:1 Mapping〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：Queue Pair, 1:1。

- 解決的問題：呈現〈Queue Pair Example, 1:1 Mapping〉中的 queue 或 command 關係。

- 閱讀順序：沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：Queue Pair, 1:1。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：沿 Figure 6 追蹤一筆 command，以 Queue Pair 與 1:1 作為擁有者或 pointer 變動檢查點。 此例不新增規格要求。

- 來源欄位索引：Queue Pair, 1:1

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.1, Figure 6, 文件頁 22, PDF 頁 48

</details>

<details markdown="1">
<summary><strong>Figure 7: Queue Pair Example, n:1 Mapping</strong></summary>

<!-- claim:BASE12-FIG-007-CLAIM figure-table:BASE12-FIG-007 -->

Figure 7〈Queue Pair Example, n:1 Mapping〉：呈現〈Queue Pair Example, n:1 Mapping〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：Queue Pair。

- 解決的問題：呈現〈Queue Pair Example, n:1 Mapping〉中的 queue 或 command 關係。

- 閱讀順序：沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：Queue Pair。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：沿 Figure 7 追蹤一筆 command，以 Queue Pair 與 引用條件 作為擁有者或 pointer 變動檢查點。 此例不新增規格要求。

- 來源欄位索引：Queue Pair

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.1, Figure 7, 文件頁 22, PDF 頁 48

</details>

<a id="section-2-3"></a>

### §2.3

<details markdown="1">
<summary><strong>Figure 11: Simple NVM Storage Hierarchy with NVM Sets</strong></summary>

<!-- claim:BASE12-FIG-011-CLAIM figure-table:BASE12-FIG-011 -->

Figure 11〈Simple NVM Storage Hierarchy with NVM Sets〉：呈現〈Simple NVM Storage Hierarchy with NVM Sets〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Storage Hierarchy, NVM Set。

- 解決的問題：呈現〈Simple NVM Storage Hierarchy with NVM Sets〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Storage Hierarchy, NVM Set。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Storage Hierarchy 標示的一個物件，再追到 NVM Set，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Storage Hierarchy, NVM Set

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 11, 文件頁 27, PDF 頁 53

</details>

<details markdown="1">
<summary><strong>Figure 12: Simple NVM Storage Hierarchy with One Reclaim Group</strong></summary>

<!-- claim:BASE12-FIG-012-CLAIM figure-table:BASE12-FIG-012 -->

Figure 12〈Simple NVM Storage Hierarchy with One Reclaim Group〉：呈現〈Simple NVM Storage Hierarchy with One Reclaim Group〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Storage Hierarchy, Reclaim Group。

- 解決的問題：呈現〈Simple NVM Storage Hierarchy with One Reclaim Group〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Storage Hierarchy, Reclaim Group。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Storage Hierarchy 標示的一個物件，再追到 Reclaim Group，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Storage Hierarchy, Reclaim Group

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 12, 文件頁 28, PDF 頁 54

</details>

<details markdown="1">
<summary><strong>Figure 13: Simple NVM Storage Hierarchy with Multiple Reclaim Groups</strong></summary>

<!-- claim:BASE12-FIG-013-CLAIM figure-table:BASE12-FIG-013 -->

Figure 13〈Simple NVM Storage Hierarchy with Multiple Reclaim Groups〉：呈現〈Simple NVM Storage Hierarchy with Multiple Reclaim Groups〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Storage Hierarchy, Reclaim Group。

- 解決的問題：呈現〈Simple NVM Storage Hierarchy with Multiple Reclaim Groups〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Storage Hierarchy, Reclaim Group。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Storage Hierarchy 標示的一個物件，再追到 Reclaim Group，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Storage Hierarchy, Reclaim Group

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 13, 文件頁 29, PDF 頁 55

</details>

<details markdown="1">
<summary><strong>Figure 14: Complex NVM Storage Hierarchy with NVM Sets</strong></summary>

<!-- claim:BASE12-FIG-014-CLAIM figure-table:BASE12-FIG-014 -->

Figure 14〈Complex NVM Storage Hierarchy with NVM Sets〉：呈現〈Complex NVM Storage Hierarchy with NVM Sets〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Storage Hierarchy, NVM Set。

- 解決的問題：呈現〈Complex NVM Storage Hierarchy with NVM Sets〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Storage Hierarchy, NVM Set。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Storage Hierarchy 標示的一個物件，再追到 NVM Set，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Storage Hierarchy, NVM Set

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 14, 文件頁 30, PDF 頁 56

</details>

<details markdown="1">
<summary><strong>Figure 15: Complex NVM Storage Hierarchy with Multiple Reclaim Groups</strong></summary>

<!-- claim:BASE12-FIG-015-CLAIM figure-table:BASE12-FIG-015 -->

Figure 15〈Complex NVM Storage Hierarchy with Multiple Reclaim Groups〉：呈現〈Complex NVM Storage Hierarchy with Multiple Reclaim Groups〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Storage Hierarchy, Reclaim Group。

- 解決的問題：呈現〈Complex NVM Storage Hierarchy with Multiple Reclaim Groups〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Storage Hierarchy, Reclaim Group。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Storage Hierarchy 標示的一個物件，再追到 Reclaim Group，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Storage Hierarchy, Reclaim Group

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 15, 文件頁 31, PDF 頁 57

</details>

<details markdown="1">
<summary><strong>Figure 16: Single-Namespace NVM Subsystem</strong></summary>

<!-- claim:BASE12-FIG-016-CLAIM figure-table:BASE12-FIG-016 -->

Figure 16〈Single-Namespace NVM Subsystem〉：呈現〈Single-Namespace NVM Subsystem〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, Namespace。

- 解決的問題：呈現〈Single-Namespace NVM Subsystem〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, Namespace。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Subsystem 標示的一個物件，再追到 Namespace，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Subsystem, Namespace

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 16, 文件頁 32, PDF 頁 58

</details>

<details markdown="1">
<summary><strong>Figure 17: Two-Namespace NVM Subsystem</strong></summary>

<!-- claim:BASE12-FIG-017-CLAIM figure-table:BASE12-FIG-017 -->

Figure 17〈Two-Namespace NVM Subsystem〉：呈現〈Two-Namespace NVM Subsystem〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, Namespace。

- 解決的問題：呈現〈Two-Namespace NVM Subsystem〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, Namespace。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Subsystem 標示的一個物件，再追到 Namespace，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Subsystem, Namespace

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 17, 文件頁 33, PDF 頁 59

</details>

<details markdown="1">
<summary><strong>Figure 18: Complex NVM Subsystem</strong></summary>

<!-- claim:BASE12-FIG-018-CLAIM figure-table:BASE12-FIG-018 -->

Figure 18〈Complex NVM Subsystem〉：呈現〈Complex NVM Subsystem〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem。

- 解決的問題：呈現〈Complex NVM Subsystem〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Subsystem 標示的一個物件，再追到 引用條件，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Subsystem

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 18, 文件頁 34, PDF 頁 60

</details>

<a id="section-2-4"></a>

### §2.4

<details markdown="1">
<summary><strong>Figure 19: NVM Express Controller with Two Namespaces</strong></summary>

<!-- claim:BASE12-FIG-019-CLAIM figure-table:BASE12-FIG-019 -->

Figure 19〈NVM Express Controller with Two Namespaces〉：呈現〈NVM Express Controller with Two Namespaces〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：Namespace, Controller。

- 解決的問題：呈現〈NVM Express Controller with Two Namespaces〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：Namespace, Controller。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 Namespace 標示的一個物件，再追到 Controller，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：Namespace, Controller

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 19, 文件頁 35, PDF 頁 61

</details>

<details markdown="1">
<summary><strong>Figure 20: NVM Subsystem with Two Controllers and One Port</strong></summary>

<!-- claim:BASE12-FIG-020-CLAIM figure-table:BASE12-FIG-020 -->

Figure 20〈NVM Subsystem with Two Controllers and One Port〉：呈現〈NVM Subsystem with Two Controllers and One Port〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, Controller。

- 解決的問題：呈現〈NVM Subsystem with Two Controllers and One Port〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, Controller。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Subsystem 標示的一個物件，再追到 Controller，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Subsystem, Controller

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 20, 文件頁 35, PDF 頁 61

</details>

<details markdown="1">
<summary><strong>Figure 21: NVM Subsystem with Two Controllers and Two Ports</strong></summary>

<!-- claim:BASE12-FIG-021-CLAIM figure-table:BASE12-FIG-021 -->

Figure 21〈NVM Subsystem with Two Controllers and Two Ports〉：呈現〈NVM Subsystem with Two Controllers and Two Ports〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, Controller。

- 解決的問題：呈現〈NVM Subsystem with Two Controllers and Two Ports〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, Controller。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Subsystem 標示的一個物件，再追到 Controller，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Subsystem, Controller

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 21, 文件頁 36, PDF 頁 62

</details>

<details markdown="1">
<summary><strong>Figure 22: PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)</strong></summary>

<!-- claim:BASE12-FIG-022-CLAIM figure-table:BASE12-FIG-022 -->

Figure 22〈PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)〉：呈現〈PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)〉中 Physical Function 與 Virtual Function 的關係。 分開 PCIe Function identity、controller ownership 與 shared device resource；來源索引：SR, IOV。

- 解決的問題：呈現〈PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)〉中 Physical Function 與 Virtual Function 的關係。

- 閱讀順序：分開 PCIe Function identity、controller ownership 與 shared device resource；來源索引：SR, IOV。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：從 SR 所代表的 Function 出發，再追到 IOV，不要把 shared resource 誤當成 private resource。 此例不新增規格要求。

- 來源欄位索引：SR, IOV

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 22, 文件頁 37, PDF 頁 63

</details>

## 使用與限制

製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata 集合或核准範圍改變時，必須重新核對受影響 claim。
