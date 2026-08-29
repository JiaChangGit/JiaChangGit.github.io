---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4 第 3 章：Controller、Queue、初始化與重設"
date: 2026-08-28
description: "供 GitHub Pages 與 PPT 使用的 NVMe 規格導讀。"
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---

# NVMe Base 2.4 第 3 章：Controller、Queue、初始化與重設

用途：供 GitHub Pages 閱讀與 100 分鐘簡報製作；讀者已具備 PCIe 與 NVMe 基礎。

範圍：§3；文件頁 38–138；PDF 頁 64–164。正文只保留 PCIe／memory-based 與通用 NVMe 內容。

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

### 1. BASE3-STATIC

<!-- claim:BASE3-STATIC -->

memory-based controller 必須（shall）只支援 static controller model。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.1, 文件頁 38, PDF 頁 64

### 2. BASE3-TYPES

<!-- claim:BASE3-TYPES -->

本輪只使用 I/O controller 與 Administrative controller：前者可執行使用者資料的 I/O，後者以管理為目的且不支援資料 I/O command。兩者都具有一組 Admin Submission／Completion Queue。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3-3.1.3.2, 文件頁 39-43, PDF 頁 65-69

### 3. BASE3-ORDER

<!-- claim:BASE3-ORDER -->

除 fused operation 外，controller 取走的命令與完成沒有一般性的先後保證；若有順序需求，強制該順序是 host 的責任。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3, 文件頁 40, PDF 頁 66

### 4. BASE3-PROPERTY

<!-- claim:BASE3-PROPERTY -->

host 必須（shall）以 property 指定的寬度，從 property 起始 offset 存取；memory-based controller 的實際存取規則由 PCIe Transport 補充。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, 文件頁 52-54, PDF 頁 78-80

### 5. BASE3-NAMESPACE

<!-- claim:BASE3-NAMESPACE -->

NSID 0h 無效，FFFFFFFFh 是 broadcast 值；其餘 NSID 還要區分 allocated／unallocated 與 active／inactive，不能只看數字是否落在範圍內。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.1, 文件頁 78-80, PDF 頁 104-106

### 6. BASE3-MEDIA

<!-- claim:BASE3-MEDIA -->

NVM Set、Endurance Group、Reclaim Group 與 Reclaim Unit 分別描述容量集合、耐久度管理與回收粒度。是否支援及其 identifier 由 Identify／log page 能力判定。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, 文件頁 80-85, PDF 頁 106-111

### 7. BASE3-DOMAIN

<!-- claim:BASE3-DOMAIN -->

domain 是 NVM subsystem 內的故障／通訊邊界。多 domain subsystem 的 identifier 必須（shall）在該 subsystem 內唯一。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.5, 文件頁 85-88, PDF 頁 111-114

### 8. BASE3-QUEUE

<!-- claim:BASE3-QUEUE -->

PCIe queue 由 host-addressable memory 中的環形 buffer、head 與 tail pointer 構成。host 建立 I/O Completion Queue 後再建立對應 Submission Queue，並以 doorbell 推進 pointer。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1, 文件頁 88-91, PDF 頁 114-117

### 9. BASE3-PROCESS

<!-- claim:BASE3-PROCESS -->

command processing 要分開看 ordering、fused／atomic semantics、arbitration 與 outstanding command 上限；priority 屬於 Submission Queue，不是每一筆 command 的獨立欄位。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, 文件頁 101-105, PDF 頁 127-131

### 10. BASE3-INIT

<!-- claim:BASE3-INIT -->

PCIe 初始化以 CAP 判斷能力與 timeout，設定 AQA／ASQ／ACQ 與 CC，接著等待 CSTS.RDY。ready mode 與 CRTO 會影響 host 等待與錯誤處理。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, 文件頁 105-113, PDF 頁 131-139

### 11. BASE3-SHUTDOWN

<!-- claim:BASE3-SHUTDOWN -->

正常 shutdown 由 host 設定 CC.SHN，controller 透過 CSTS.SHST 回報進度；NVM subsystem shutdown 是更大範圍的處理，不能與單一 controller shutdown 混為一談。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, 文件頁 113-120, PDF 頁 139-146

### 12. BASE3-RESET

<!-- claim:BASE3-RESET -->

NVM Subsystem Reset、Controller Level Reset 與 Queue Level Reset 的影響範圍不同；設計 recovery flow 前先確認哪一層狀態會被清除、queue 是否仍存在。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.7, 文件頁 120-125, PDF 頁 146-151

### 13. BASE3-CAPACITY

<!-- claim:BASE3-CAPACITY -->

capacity model 分開追蹤 NVM subsystem、Endurance Group、NVM Set 與 namespace 的可用或配置容量；同一數值不可跨層級直接比較。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.8, 文件頁 125-129, PDF 頁 151-155

### 14. BASE3-KEEPALIVE

<!-- claim:BASE3-KEEPALIVE -->

Keep Alive 以 KATO／KATT 建立 host 與 controller 的存活監測；本報告只保留 controller 共通與 PCIe 可用的 timer、command 與 timeout 行為。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.9, 文件頁 129-135, PDF 頁 155-161

### 15. BASE3-FIRMWARE

<!-- claim:BASE3-FIRMWARE -->

privileged action 會影響其他 host 或 controller；firmware update 分成 image download、commit／activate 與可能的 reset，host 依回報的 activation action 安排流程。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.10-3.11, 文件頁 135-138, PDF 頁 161-164

## Figure 逐圖導讀

本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。

### Figure 23: Controller Types

<!-- claim:BASE3-FIG-023-CLAIM figure-table:BASE3-FIG-023 -->

Figure 23〈Controller Types〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。 本報告只解釋圖中的 PCIe／memory-based 部分。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

- 範圍：只介紹 PCIe／memory-based 部分。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3, Figure 23, 文件頁 39, PDF 頁 65

### Figure 24: NVM Subsystem with Three I/O Controllers

<!-- claim:BASE3-FIG-024-CLAIM figure-table:BASE3-FIG-024 -->

Figure 24〈NVM Subsystem with Three I/O Controllers〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.1, Figure 24, 文件頁 41, PDF 頁 67

### Figure 25: NVM Subsystem with One Administrative and Two I/O Controllers

<!-- claim:BASE3-FIG-025-CLAIM figure-table:BASE3-FIG-025 -->

Figure 25〈NVM Subsystem with One Administrative and Two I/O Controllers〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.2, Figure 25, 文件頁 42, PDF 頁 68

### Figure 26: NVM Subsystem with One Administrative Controller

<!-- claim:BASE3-FIG-026-CLAIM figure-table:BASE3-FIG-026 -->

Figure 26〈NVM Subsystem with One Administrative Controller〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.2, Figure 26, 文件頁 42, PDF 頁 68

### Figure 27: Controller IDs FFF0h to FFFFh

<!-- claim:BASE3-FIG-027-CLAIM figure-table:BASE3-FIG-027 -->

Figure 27〈Controller IDs FFF0h to FFFFh〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.3, Figure 27, 文件頁 44, PDF 頁 70

### Figure 28: Admin Command Support Requirements

<!-- claim:BASE3-FIG-028-CLAIM figure-table:BASE3-FIG-028 -->

Figure 28〈Admin Command Support Requirements〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。 本報告只解釋圖中的 PCIe／memory-based 部分。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

- 範圍：只介紹 PCIe／memory-based 部分。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.3.3, Figure 28, 文件頁 45-47, PDF 頁 71-73

### Figure 30: Common I/O Command Support Requirements

<!-- claim:BASE3-FIG-030-CLAIM figure-table:BASE3-FIG-030 -->

Figure 30〈Common I/O Command Support Requirements〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。 本報告只解釋圖中的 PCIe／memory-based 部分。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

- 範圍：只介紹 PCIe／memory-based 部分。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.4, Figure 30, 文件頁 47-48, PDF 頁 73-74

### Figure 31: Log Page Support Requirements

<!-- claim:BASE3-FIG-031-CLAIM figure-table:BASE3-FIG-031 -->

Figure 31〈Log Page Support Requirements〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。 本報告只解釋圖中的 PCIe／memory-based 部分。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

- 範圍：只介紹 PCIe／memory-based 部分。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.4, Figure 31, 文件頁 48-50, PDF 頁 74-76

### Figure 32: Feature Support Requirements

<!-- claim:BASE3-FIG-032-CLAIM figure-table:BASE3-FIG-032 -->

Figure 32〈Feature Support Requirements〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。 本報告只解釋圖中的 PCIe／memory-based 部分。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

- 範圍：只介紹 PCIe／memory-based 部分。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.5, Figure 32, 文件頁 50-52, PDF 頁 76-78

### Figure 33: Property Definition

<!-- claim:BASE3-FIG-033-CLAIM figure-table:BASE3-FIG-033 -->

Figure 33〈Property Definition〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。 本報告只解釋圖中的 PCIe／memory-based 部分。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

- 範圍：只介紹 PCIe／memory-based 部分。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, Figure 33, 文件頁 52-53, PDF 頁 78-79

### Figure 34: Memory-Based Property Definition

<!-- claim:BASE3-FIG-034-CLAIM figure-table:BASE3-FIG-034 -->

Figure 34〈Memory-Based Property Definition〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, Figure 34, 文件頁 54, PDF 頁 80

### Figure 36: Offset 0h: CAP – Controller Capabilities

<!-- claim:BASE3-FIG-036-CLAIM figure-table:BASE3-FIG-036 -->

Figure 36〈Offset 0h: CAP – Controller Capabilities〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, 文件頁 55-58, PDF 頁 81-84

### Figure 37: Specification Version Descriptor

<!-- claim:BASE3-FIG-037-CLAIM figure-table:BASE3-FIG-037 -->

Figure 37〈Specification Version Descriptor〉：說明資料 buffer 如何由 PRP／SGL 結構描述。 逐一核對 address、offset、length、alignment 與下一層 pointer。

- 解決的問題：說明資料 buffer 如何由 PRP／SGL 結構描述。

- 閱讀順序：逐一核對 address、offset、length、alignment 與下一層 pointer。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：用跨兩個 memory page 的 buffer 檢查第一個 offset 與後續 alignment。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 37, 文件頁 58, PDF 頁 84

### Figure 38: NVM Express Base Specification Version Property Reset Values

<!-- claim:BASE3-FIG-038-CLAIM figure-table:BASE3-FIG-038 -->

Figure 38〈NVM Express Base Specification Version Property Reset Values〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 38, 文件頁 58-59, PDF 頁 84-85

### Figure 39: Offset Ch: INTMS – Interrupt Mask Set

<!-- claim:BASE3-FIG-039-CLAIM figure-table:BASE3-FIG-039 -->

Figure 39〈Offset Ch: INTMS – Interrupt Mask Set〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.2, Figure 39, 文件頁 59, PDF 頁 85

### Figure 40: Offset 10h: INTMC – Interrupt Mask Clear

<!-- claim:BASE3-FIG-040-CLAIM figure-table:BASE3-FIG-040 -->

Figure 40〈Offset 10h: INTMC – Interrupt Mask Clear〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.2, Figure 40, 文件頁 59, PDF 頁 85

### Figure 41: Offset 14h: CC – Controller Configuration

<!-- claim:BASE3-FIG-041-CLAIM figure-table:BASE3-FIG-041 -->

Figure 41〈Offset 14h: CC – Controller Configuration〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.5, Figure 41, 文件頁 60-63, PDF 頁 86-89

### Figure 42: Offset 1Ch: CSTS – Controller Status

<!-- claim:BASE3-FIG-042-CLAIM figure-table:BASE3-FIG-042 -->

Figure 42〈Offset 1Ch: CSTS – Controller Status〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.5, Figure 42, 文件頁 63-65, PDF 頁 89-91

### Figure 43: Offset 20h: NSSR – NVM Subsystem Reset

<!-- claim:BASE3-FIG-043-CLAIM figure-table:BASE3-FIG-043 -->

Figure 43〈Offset 20h: NSSR – NVM Subsystem Reset〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 43, 文件頁 66, PDF 頁 92

### Figure 44: Offset 24h: AQA – Admin Queue Attributes

<!-- claim:BASE3-FIG-044-CLAIM figure-table:BASE3-FIG-044 -->

Figure 44〈Offset 24h: AQA – Admin Queue Attributes〉：整理 queue／command 的關係或處理順序。 依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 解決的問題：整理 queue／command 的關係或處理順序。

- 閱讀順序：依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先選一個 queue identifier，沿箭頭追蹤一筆 command 與 completion。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 44, 文件頁 66, PDF 頁 92

### Figure 45: Offset 28h: ASQ – Admin Submission Queue Base Address

<!-- claim:BASE3-FIG-045-CLAIM figure-table:BASE3-FIG-045 -->

Figure 45〈Offset 28h: ASQ – Admin Submission Queue Base Address〉：整理 queue／command 的關係或處理順序。 依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 解決的問題：整理 queue／command 的關係或處理順序。

- 閱讀順序：依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先選一個 queue identifier，沿箭頭追蹤一筆 command 與 completion。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 45, 文件頁 66, PDF 頁 92

### Figure 46: Offset 30h: ACQ – Admin Completion Queue Base Address

<!-- claim:BASE3-FIG-046-CLAIM figure-table:BASE3-FIG-046 -->

Figure 46〈Offset 30h: ACQ – Admin Completion Queue Base Address〉：整理 queue／command 的關係或處理順序。 依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 解決的問題：整理 queue／command 的關係或處理順序。

- 閱讀順序：依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先選一個 queue identifier，沿箭頭追蹤一筆 command 與 completion。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.9, Figure 46, 文件頁 67, PDF 頁 93

### Figure 47: Offset 38h: CMBLOC – Controller Memory Buffer Location

<!-- claim:BASE3-FIG-047-CLAIM figure-table:BASE3-FIG-047 -->

Figure 47〈Offset 38h: CMBLOC – Controller Memory Buffer Location〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.9, Figure 47, 文件頁 67-68, PDF 頁 93-94

### Figure 48: Offset 3Ch: CMBSZ – Controller Memory Buffer Size

<!-- claim:BASE3-FIG-048-CLAIM figure-table:BASE3-FIG-048 -->

Figure 48〈Offset 3Ch: CMBSZ – Controller Memory Buffer Size〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.11, Figure 48, 文件頁 68-69, PDF 頁 94-95

### Figure 49: Offset 40h: BPINFO – Boot Partition Information

<!-- claim:BASE3-FIG-049-CLAIM figure-table:BASE3-FIG-049 -->

Figure 49〈Offset 40h: BPINFO – Boot Partition Information〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.12, Figure 49, 文件頁 69, PDF 頁 95

### Figure 50: Offset 44h: BPRSEL – Boot Partition Read Select

<!-- claim:BASE3-FIG-050-CLAIM figure-table:BASE3-FIG-050 -->

Figure 50〈Offset 44h: BPRSEL – Boot Partition Read Select〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.12, Figure 50, 文件頁 69-70, PDF 頁 95-96

### Figure 51: Offset 48h: BPMBL – Boot Partition Memory Buffer Location

<!-- claim:BASE3-FIG-051-CLAIM figure-table:BASE3-FIG-051 -->

Figure 51〈Offset 48h: BPMBL – Boot Partition Memory Buffer Location〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 51, 文件頁 70, PDF 頁 96

### Figure 52: Offset 50h: CMBMSC – Controller Memory Buffer Memory Space Control

<!-- claim:BASE3-FIG-052-CLAIM figure-table:BASE3-FIG-052 -->

Figure 52〈Offset 50h: CMBMSC – Controller Memory Buffer Memory Space Control〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 52, 文件頁 70-71, PDF 頁 96-97

### Figure 53: Offset 58h: CMBSTS – Controller Memory Buffer Status

<!-- claim:BASE3-FIG-053-CLAIM figure-table:BASE3-FIG-053 -->

Figure 53〈Offset 58h: CMBSTS – Controller Memory Buffer Status〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.16, Figure 53, 文件頁 71, PDF 頁 97

### Figure 54: Offset 5Ch: CMBEBS – Controller Memory Buffer Elasticity Buffer Size

<!-- claim:BASE3-FIG-054-CLAIM figure-table:BASE3-FIG-054 -->

Figure 54〈Offset 5Ch: CMBEBS – Controller Memory Buffer Elasticity Buffer Size〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.16, Figure 54, 文件頁 71, PDF 頁 97

### Figure 55: Offset 60h: CMBSWTP – Controller Memory Buffer Sustained Write Throughput

<!-- claim:BASE3-FIG-055-CLAIM figure-table:BASE3-FIG-055 -->

Figure 55〈Offset 60h: CMBSWTP – Controller Memory Buffer Sustained Write Throughput〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.19, Figure 55, 文件頁 72, PDF 頁 98

### Figure 56: Offset 64h: NSSD – NVM Subsystem Shutdown

<!-- claim:BASE3-FIG-056-CLAIM figure-table:BASE3-FIG-056 -->

Figure 56〈Offset 64h: NSSD – NVM Subsystem Shutdown〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.19, Figure 56, 文件頁 72, PDF 頁 98

### Figure 57: Offset 68h: CRTO – Controller Ready Timeouts

<!-- claim:BASE3-FIG-057-CLAIM figure-table:BASE3-FIG-057 -->

Figure 57〈Offset 68h: CRTO – Controller Ready Timeouts〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.21, Figure 57, 文件頁 73, PDF 頁 99

### Figure 58: Offset E00h: PMRCAP – Persistent Memory Region Capabilities

<!-- claim:BASE3-FIG-058-CLAIM figure-table:BASE3-FIG-058 -->

Figure 58〈Offset E00h: PMRCAP – Persistent Memory Region Capabilities〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.21, Figure 58, 文件頁 73-74, PDF 頁 99-100

### Figure 59: Offset E04h: PMRCTL – Persistent Memory Region Control

<!-- claim:BASE3-FIG-059-CLAIM figure-table:BASE3-FIG-059 -->

Figure 59〈Offset E04h: PMRCTL – Persistent Memory Region Control〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.22, Figure 59, 文件頁 74, PDF 頁 100

### Figure 60: Offset E08h: PMRSTS – Persistent Memory Region Status

<!-- claim:BASE3-FIG-060-CLAIM figure-table:BASE3-FIG-060 -->

Figure 60〈Offset E08h: PMRSTS – Persistent Memory Region Status〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.23, Figure 60, 文件頁 75, PDF 頁 101

### Figure 61: Offset E0Ch: PMREBS – Persistent Memory Region Elasticity Buffer Size

<!-- claim:BASE3-FIG-061-CLAIM figure-table:BASE3-FIG-061 -->

Figure 61〈Offset E0Ch: PMREBS – Persistent Memory Region Elasticity Buffer Size〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.24, Figure 61, 文件頁 76, PDF 頁 102

### Figure 62: Offset E10h: PMRSWTP – Persistent Memory Region Sustained Write Throughput

<!-- claim:BASE3-FIG-062-CLAIM figure-table:BASE3-FIG-062 -->

Figure 62〈Offset E10h: PMRSWTP – Persistent Memory Region Sustained Write Throughput〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.24, Figure 62, 文件頁 76, PDF 頁 102

### Figure 63: Offset E14h: PMRMSCL – Persistent Memory Region Memory Space Control Lower

<!-- claim:BASE3-FIG-063-CLAIM figure-table:BASE3-FIG-063 -->

Figure 63〈Offset E14h: PMRMSCL – Persistent Memory Region Memory Space Control Lower〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.26, Figure 63, 文件頁 77, PDF 頁 103

### Figure 64: Offset E18h: PMRMSCU – Persistent Memory Region Memory Space Control Upper

<!-- claim:BASE3-FIG-064-CLAIM figure-table:BASE3-FIG-064 -->

Figure 64〈Offset E18h: PMRMSCU – Persistent Memory Region Memory Space Control Upper〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.26, Figure 64, 文件頁 77, PDF 頁 103

### Figure 65: NSID Types and Relationship to Namespace

<!-- claim:BASE3-FIG-065-CLAIM figure-table:BASE3-FIG-065 -->

Figure 65〈NSID Types and Relationship to Namespace〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.1, Figure 65, 文件頁 78-79, PDF 頁 104-105

### Figure 66: NSID Types

<!-- claim:BASE3-FIG-066-CLAIM figure-table:BASE3-FIG-066 -->

Figure 66〈NSID Types〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.1.5, Figure 66, 文件頁 79, PDF 頁 105

### Figure 67: NVM Sets and Associated Namespaces

<!-- claim:BASE3-FIG-067-CLAIM figure-table:BASE3-FIG-067 -->

Figure 67〈NVM Sets and Associated Namespaces〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2, Figure 67, 文件頁 81, PDF 頁 107

### Figure 68: NVM Set Aware Admin Commands

<!-- claim:BASE3-FIG-068-CLAIM figure-table:BASE3-FIG-068 -->

Figure 68〈NVM Set Aware Admin Commands〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2, Figure 68, 文件頁 81, PDF 頁 107

### Figure 69: NVM Sets and Associated Namespaces

<!-- claim:BASE3-FIG-069-CLAIM figure-table:BASE3-FIG-069 -->

Figure 69〈NVM Sets and Associated Namespaces〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.3, Figure 69, 文件頁 83, PDF 頁 109

### Figure 70: Flexible Data Placement Logical View of Non-Volatile Storage

<!-- claim:BASE3-FIG-070-CLAIM figure-table:BASE3-FIG-070 -->

Figure 70〈Flexible Data Placement Logical View of Non-Volatile Storage〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.4, Figure 70, 文件頁 85, PDF 頁 111

### Figure 71: Example 1 Domain Structure

<!-- claim:BASE3-FIG-071-CLAIM figure-table:BASE3-FIG-071 -->

Figure 71〈Example 1 Domain Structure〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.5.1, Figure 71, 文件頁 86, PDF 頁 112

### Figure 73: Empty Queue Definition

<!-- claim:BASE3-FIG-073-CLAIM figure-table:BASE3-FIG-073 -->

Figure 73〈Empty Queue Definition〉：整理 queue／command 的關係或處理順序。 依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 解決的問題：整理 queue／command 的關係或處理順序。

- 閱讀順序：依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先選一個 queue identifier，沿箭頭追蹤一筆 command 與 completion。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1.4, Figure 73, 文件頁 91, PDF 頁 117

### Figure 74: Full Queue Definition

<!-- claim:BASE3-FIG-074-CLAIM figure-table:BASE3-FIG-074 -->

Figure 74〈Full Queue Definition〉：整理 queue／command 的關係或處理順序。 依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 解決的問題：整理 queue／command 的關係或處理順序。

- 閱讀順序：依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先選一個 queue identifier，沿箭頭追蹤一筆 command 與 completion。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1.4, Figure 74, 文件頁 91, PDF 頁 117

### Figure 80: Round Robin Arbitration

<!-- claim:BASE3-FIG-080-CLAIM figure-table:BASE3-FIG-080 -->

Figure 80〈Round Robin Arbitration〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.4.4, Figure 80, 文件頁 103, PDF 頁 129

### Figure 81: Weighted Round Robin with Urgent Priority Class Arbitration

<!-- claim:BASE3-FIG-081-CLAIM figure-table:BASE3-FIG-081 -->

Figure 81〈Weighted Round Robin with Urgent Priority Class Arbitration〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.4.4.2, Figure 81, 文件頁 104, PDF 頁 130

### Figure 84: Admin Commands Permitted to Return a Status Code of Admin Command Media Not

<!-- claim:BASE3-FIG-084-CLAIM figure-table:BASE3-FIG-084 -->

Figure 84〈Admin Commands Permitted to Return a Status Code of Admin Command Media Not〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。 本報告只解釋圖中的 PCIe／memory-based 部分。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

- 範圍：只介紹 PCIe／memory-based 部分。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.5.3, Figure 84, 文件頁 110-111, PDF 頁 136-137

### Figure 85: Shutdown Processing Interactions

<!-- claim:BASE3-FIG-085-CLAIM figure-table:BASE3-FIG-085 -->

Figure 85〈Shutdown Processing Interactions〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。 本報告只解釋圖中的 PCIe／memory-based 部分。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

- 範圍：只介紹 PCIe／memory-based 部分。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.6, Figure 85, 文件頁 113, PDF 頁 139

### Figure 86: Simple NVM Subsystem

<!-- claim:BASE3-FIG-086-CLAIM figure-table:BASE3-FIG-086 -->

Figure 86〈Simple NVM Subsystem〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.8.2, Figure 86, 文件頁 126, PDF 頁 152

### Figure 87: Vertically-Organized NVM Subsystem

<!-- claim:BASE3-FIG-087-CLAIM figure-table:BASE3-FIG-087 -->

Figure 87〈Vertically-Organized NVM Subsystem〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.8.2.2, Figure 87, 文件頁 127, PDF 頁 153

### Figure 88: Horizontally-Organized Dual NAND NVM Subsystem

<!-- claim:BASE3-FIG-088-CLAIM figure-table:BASE3-FIG-088 -->

Figure 88〈Horizontally-Organized Dual NAND NVM Subsystem〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.8.2.3, Figure 88, 文件頁 128, PDF 頁 154

### Figure 89: Capacity Information Field Usage

<!-- claim:BASE3-FIG-089-CLAIM figure-table:BASE3-FIG-089 -->

Figure 89〈Capacity Information Field Usage〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.8.3, Figure 89, 文件頁 129, PDF 頁 155

### Figure 90: Detecting Timeout Takes up to 2 * KATT

<!-- claim:BASE3-FIG-090-CLAIM figure-table:BASE3-FIG-090 -->

Figure 90〈Detecting Timeout Takes up to 2 * KATT〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。 本報告只解釋圖中的 PCIe／memory-based 部分。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

- 範圍：只介紹 PCIe／memory-based 部分。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.9.4.1, Figure 90, 文件頁 133, PDF 頁 159

### Figure 91: Example Privileged Action Admin Commands

<!-- claim:BASE3-FIG-091-CLAIM figure-table:BASE3-FIG-091 -->

Figure 91〈Example Privileged Action Admin Commands〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。 本報告只解釋圖中的 PCIe／memory-based 部分。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

- 範圍：只介紹 PCIe／memory-based 部分。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.10, Figure 91, 文件頁 135, PDF 頁 161

## 使用與限制

製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata 集合或核准範圍改變時，必須重新核對受影響 claim。
