---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4 第 1、2 章：規格語言、PCIe 佇列與儲存模型"
date: 2026-08-28
description: "供 GitHub Pages 與 PPT 使用的 NVMe 規格導讀。"
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

### 1. BASE12-FAMILY

<!-- claim:BASE12-FAMILY -->

Base Specification 定義通用 NVMe 協定；Transport Specification 綁定特定傳輸，I/O Command Set Specification 擴充命令與資料結構。這是適用關係，不是協定堆疊。

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.1.1, 文件頁 1, PDF 頁 27

### 2. BASE12-KEYWORDS

<!-- claim:BASE12-KEYWORDS -->

規格的 mandatory、may、optional、reserved、shall、should 各有固定語氣；詳細版保留英文 keyword，不能把 may 或 should 翻成 shall。

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.4.1, 文件頁 2-3, PDF 頁 28-29

### 3. BASE12-NUMBERS

<!-- claim:BASE12-NUMBERS -->

數值的解讀同時包含進位與單位；十六進位使用 h 後綴，二進位使用 b 後綴，十進位可省略 d。十進位與二進位容量前綴代表不同倍率。

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.4.2, 文件頁 3-5, PDF 頁 29-31

### 4. BASE12-DWORD

<!-- claim:BASE12-DWORD -->

NVMe 以 byte、word、dword 表示欄位位置；一個 word 為 2 bytes，一個 dword 為 4 bytes。解欄位時先確認 byte 與 bit 編號。

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.4.3, 文件頁 5, PDF 頁 31

### 5. BASE12-QUEUE

<!-- claim:BASE12-QUEUE -->

PCIe memory-based model 把 Submission Queue 與 Completion Queue 配置在記憶體。多個 I/O Submission Queues 可共用一個 I/O Completion Queue；Admin queue pair 維持一對一。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.1, 文件頁 21-23, PDF 頁 47-49

### 6. BASE12-STORAGE

<!-- claim:BASE12-STORAGE -->

儲存模型用 NVM subsystem、domain、Endurance Group、NVM Set／Reclaim Group、Reclaim Unit 與 namespace 表達包含關係。namespace 是 host 實際透過 controller 存取的格式化容量。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, 文件頁 26-33, PDF 頁 52-59

### 7. BASE12-COMMANDSET

<!-- claim:BASE12-COMMANDSET -->

Admin Command Set 管理 controller 與 queue；I/O Command Set 定義對 namespace 的資料操作。Base 說明通用機制，個別 I/O Command Set Specification 說明命令語意。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.2, 文件頁 33, PDF 頁 59

### 8. BASE12-SUBSYSTEM

<!-- claim:BASE12-SUBSYSTEM -->

controller、port、namespace 與 PCI Function 是不同物件；NSID 是 controller 用來指向 namespace 的 handle，不是 namespace 本身。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.3, 文件頁 33-35, PDF 頁 59-61

### 9. BASE12-MULTIPATH

<!-- claim:BASE12-MULTIPATH -->

multi-path I/O 是同一 host 到同一 namespace 的兩條以上獨立路徑；namespace sharing 是兩個以上 host 經不同 controller 存取同一 shared namespace。兩者都需要至少兩個 controller。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, 文件頁 35-37, PDF 頁 61-63

### 10. BASE12-ASYMMETRY

<!-- claim:BASE12-ASYMMETRY -->

支援多路徑或共享時，各 controller 對同一 namespace 的存取特性不一定相同；host 可依 controller 所回報的狀態選擇路徑。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.4.2, 文件頁 37, PDF 頁 63

## Figure 逐圖導讀

本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。

### Figure 1: NVMe Family of Specifications

<!-- claim:BASE12-FIG-001-CLAIM figure-table:BASE12-FIG-001 -->

Figure 1〈NVMe Family of Specifications〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。 本報告只解釋圖中的 PCIe／memory-based 部分。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

- 範圍：只介紹 PCIe／memory-based 部分。

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.1.1, Figure 1, 文件頁 1, PDF 頁 27

### Figure 2: Decimal and Binary Units

<!-- claim:BASE12-FIG-002-CLAIM figure-table:BASE12-FIG-002 -->

Figure 2〈Decimal and Binary Units〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.4.2, Figure 2, 文件頁 3, PDF 頁 29

### Figure 3: Byte, Word, and Dword Relationships

<!-- claim:BASE12-FIG-003-CLAIM figure-table:BASE12-FIG-003 -->

Figure 3〈Byte, Word, and Dword Relationships〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.4.3, Figure 3, 文件頁 5, PDF 頁 31

### Figure 5: Types of NVMe Command Sets

<!-- claim:BASE12-FIG-005-CLAIM figure-table:BASE12-FIG-005 -->

Figure 5〈Types of NVMe Command Sets〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。 本報告只解釋圖中的 PCIe／memory-based 部分。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

- 範圍：只介紹 PCIe／memory-based 部分。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2, Figure 5, 文件頁 21, PDF 頁 47

### Figure 6: Queue Pair Example, 1:1 Mapping

<!-- claim:BASE12-FIG-006-CLAIM figure-table:BASE12-FIG-006 -->

Figure 6〈Queue Pair Example, 1:1 Mapping〉：整理 queue／command 的關係或處理順序。 依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 解決的問題：整理 queue／command 的關係或處理順序。

- 閱讀順序：依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先選一個 queue identifier，沿箭頭追蹤一筆 command 與 completion。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.1, Figure 6, 文件頁 22, PDF 頁 48

### Figure 7: Queue Pair Example, n:1 Mapping

<!-- claim:BASE12-FIG-007-CLAIM figure-table:BASE12-FIG-007 -->

Figure 7〈Queue Pair Example, n:1 Mapping〉：整理 queue／command 的關係或處理順序。 依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 解決的問題：整理 queue／command 的關係或處理順序。

- 閱讀順序：依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先選一個 queue identifier，沿箭頭追蹤一筆 command 與 completion。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.1, Figure 7, 文件頁 22, PDF 頁 48

### Figure 11: Simple NVM Storage Hierarchy with NVM Sets

<!-- claim:BASE12-FIG-011-CLAIM figure-table:BASE12-FIG-011 -->

Figure 11〈Simple NVM Storage Hierarchy with NVM Sets〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 11, 文件頁 27, PDF 頁 53

### Figure 12: Simple NVM Storage Hierarchy with One Reclaim Group

<!-- claim:BASE12-FIG-012-CLAIM figure-table:BASE12-FIG-012 -->

Figure 12〈Simple NVM Storage Hierarchy with One Reclaim Group〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 12, 文件頁 28, PDF 頁 54

### Figure 13: Simple NVM Storage Hierarchy with Multiple Reclaim Groups

<!-- claim:BASE12-FIG-013-CLAIM figure-table:BASE12-FIG-013 -->

Figure 13〈Simple NVM Storage Hierarchy with Multiple Reclaim Groups〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 13, 文件頁 29, PDF 頁 55

### Figure 14: Complex NVM Storage Hierarchy with NVM Sets

<!-- claim:BASE12-FIG-014-CLAIM figure-table:BASE12-FIG-014 -->

Figure 14〈Complex NVM Storage Hierarchy with NVM Sets〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 14, 文件頁 30, PDF 頁 56

### Figure 15: Complex NVM Storage Hierarchy with Multiple Reclaim Groups

<!-- claim:BASE12-FIG-015-CLAIM figure-table:BASE12-FIG-015 -->

Figure 15〈Complex NVM Storage Hierarchy with Multiple Reclaim Groups〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 15, 文件頁 31, PDF 頁 57

### Figure 16: Single-Namespace NVM Subsystem

<!-- claim:BASE12-FIG-016-CLAIM figure-table:BASE12-FIG-016 -->

Figure 16〈Single-Namespace NVM Subsystem〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 16, 文件頁 32, PDF 頁 58

### Figure 17: Two-Namespace NVM Subsystem

<!-- claim:BASE12-FIG-017-CLAIM figure-table:BASE12-FIG-017 -->

Figure 17〈Two-Namespace NVM Subsystem〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 17, 文件頁 33, PDF 頁 59

### Figure 18: Complex NVM Subsystem

<!-- claim:BASE12-FIG-018-CLAIM figure-table:BASE12-FIG-018 -->

Figure 18〈Complex NVM Subsystem〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 18, 文件頁 34, PDF 頁 60

### Figure 19: NVM Express Controller with Two Namespaces

<!-- claim:BASE12-FIG-019-CLAIM figure-table:BASE12-FIG-019 -->

Figure 19〈NVM Express Controller with Two Namespaces〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 19, 文件頁 35, PDF 頁 61

### Figure 20: NVM Subsystem with Two Controllers and One Port

<!-- claim:BASE12-FIG-020-CLAIM figure-table:BASE12-FIG-020 -->

Figure 20〈NVM Subsystem with Two Controllers and One Port〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 20, 文件頁 35, PDF 頁 61

### Figure 21: NVM Subsystem with Two Controllers and Two Ports

<!-- claim:BASE12-FIG-021-CLAIM figure-table:BASE12-FIG-021 -->

Figure 21〈NVM Subsystem with Two Controllers and Two Ports〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 21, 文件頁 36, PDF 頁 62

### Figure 22: PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)

<!-- claim:BASE12-FIG-022-CLAIM figure-table:BASE12-FIG-022 -->

Figure 22〈PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 22, 文件頁 37, PDF 頁 63

## 使用與限制

製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata 集合或核准範圍改變時，必須重新核對受影響 claim。
