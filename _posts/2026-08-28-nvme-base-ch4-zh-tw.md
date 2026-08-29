---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4 第 4 章：SQE、CQE、Status、PRP 與 SGL"
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

# NVMe Base 2.4 第 4 章：SQE、CQE、Status、PRP 與 SGL

用途：供 GitHub Pages 閱讀與 100 分鐘簡報製作；讀者已具備 PCIe 與 NVMe 基礎。

範圍：§4；文件頁 139-175；PDF 頁 165-201。正文只保留 PCIe／memory-based 與通用 NVMe 內容。

## 來源版本

NVM Express Base Specification, Revision 2.4

查證日期：2026-08-29。目前未納入其他 Errata、ECN、Technical Proposal、controller vendor 文件或未提供的 PCI Express Base Specification 原文。

## 閱讀地圖

```text
64-byte SQE -> PRP or SGL -> Command execution -> 16-byte+ CQE
```

SQE 以 CID 與 SQID 識別 command，data pointer 描述 buffer；CQE 回報 SQ head、SQID、CID、phase 與 status。

## 規範性用語

shall 譯為「必須」，may 譯為「可／得」，should 譯為「宜／建議」，optional 譯為「選用」。本文不提高或降低原文語氣。

## 規格重點

### 1. common SQE 配置

<!-- claim:BASE4-SQE -->

Admin 與 I/O common SQE 固定為 64 bytes。CDW0、NSID、data pointer 與 CDW10-15 的通用位置先固定，再由各 command 定義命令專屬內容。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 文件頁 139-143, PDF 頁 165-169

### 2. CID 唯一性

<!-- claim:BASE4-CID -->

CID 與 Submission Queue identifier 的組合用來唯一識別 command；FFFFh 宜（should）避免使用，因 Error Information log 以該值表示錯誤未對應特定 command。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 文件頁 140, PDF 頁 166

### 3. PRP／SGL 選擇

<!-- claim:BASE4-PSDT -->

CDW0.PSDT 決定 DPTR 解讀為 PRP 或 SGL。NVMe over PCIe 的 Admin command 原則上必須（shall）使用 PRP，除非 command 定義另有規定。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 文件頁 140-142, PDF 頁 166-168

### 4. common CQE 與 Phase Tag

<!-- claim:BASE4-CQE -->

common CQE 至少 16 bytes；若以多次寫入建立 CQE，Phase Tag 必須（shall）在最後一次寫入更新，避免 host 看到半成品。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, 文件頁 144-145, PDF 頁 170-171

### 5. SCT、SC 與 DNR

<!-- claim:BASE4-STATUS -->

status 要先解 Status Code Type（SCT），再解 Status Code（SC），同時檢查 Do Not Retry（DNR）等控制 bit；數值不能脫離 SCT 單獨解讀。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, 文件頁 145-155, PDF 頁 171-181

### 6. Completion Queue phase

<!-- claim:BASE4-PHASE -->

Phase Tag 讓 host 判斷環形 Completion Queue slot 是否為新完成項目；host 消費 CQE 後推進 CQ head doorbell，wrap 時預期 phase 翻轉。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.4, 文件頁 155-158, PDF 頁 181-184

### 7. PRP alignment 與 page

<!-- claim:BASE4-PRP -->

PRP 以固定大小 entry 指向 physical memory page。第一個 entry 可含 page offset；後續 PRP 必須（shall）符合 page alignment，資料長度決定需要幾個 entry。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, 文件頁 158-159, PDF 頁 184-185

### 8. SGL descriptor 與 length

<!-- claim:BASE4-SGL -->

SGL 由一個以上 descriptor／segment 描述資料 buffer。SGL length 必須（shall）大於等於 requested transfer length；本報告只介紹 PCIe 可用的通用 descriptor。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, 文件頁 159-166, PDF 頁 185-192

### 9. Feature value 與 persistence

<!-- claim:BASE4-FEATURE -->

Feature 可能具有 default、saved、current value；saved value 支援與跨 reset／power cycle 的 persistence 由 SSFS 與各 Feature capability 判定。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.4, 文件頁 166-169, PDF 頁 192-195

### 10. 全域識別碼的範圍

<!-- claim:BASE4-IDENTIFIER -->

VID／SSVID、SN／MN、IEEE OUI、EUI64、NGUID 與 UUID 的來源、長度與唯一性範圍不同；不能只因外觀相似就互換。此節為 informative。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5, 文件頁 169-172, PDF 頁 195-198

### 11. Controller／Namespace List

<!-- claim:BASE4-LISTS -->

Controller List 與 Namespace List 都先給出數量，再排列 identifier；實作 parser 時，先依格式定義的上限與保留區驗證輸入。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.6, 文件頁 172-173, PDF 頁 198-199

### 12. UTF-8 輸入驗證

<!-- claim:BASE4-UTF8 -->

處理 UTF-8 輸入時要依規格流程驗證編碼、禁止的 code point 與截斷情況；不可把任意 byte sequence 當成有效字串。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.8, 文件頁 175, PDF 頁 201

## Figure 索引

本報告介紹全部 44 張納入範圍的 Figure。100 分鐘簡報以 section 主線與必講 Figure 為主，其餘 Figure 仍完整保留作為附錄。

- [§4.1](#section-4-1)

- [§4.2](#section-4-2)

- [§4.3](#section-4-3)

- [§4.4](#section-4-4)

- [§4.5](#section-4-5)

- [§4.6](#section-4-6)

- [§4.8](#section-4-8)

## Figure 逐圖導讀

本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。欄位與 keyword 索引來自本機核對過的 PDF。

<a id="section-4-1"></a>

### §4.1

<details markdown="1">
<summary><strong>Figure 92: Command Dword 0</strong></summary>

<!-- claim:BASE4-FIG-092-CLAIM figure-table:BASE4-FIG-092 -->

Figure 92〈Command Dword 0〉：定義〈Command Dword 0〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CID, PSDT, FUSE, OPC, FN, DTD, PRP, SGL。

- 解決的問題：定義〈Command Dword 0〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CID, PSDT, FUSE, OPC, FN, DTD, PRP, SGL。

- 條件與限制：來源 keyword 索引：`shall not`, `should not`, `shall`, `should`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 CID 作為 parser 的第一個檢查點，再用 PSDT 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：CID, PSDT, FUSE, OPC, FN, DTD, PRP, SGL

- 來源 keyword 索引：`shall not`, `should not`, `shall`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 92, 文件頁 139-140, PDF 頁 165-166

</details>

<details markdown="1">
<summary><strong>Figure 93: Common Command Format</strong></summary>

<!-- claim:BASE4-FIG-093-CLAIM figure-table:BASE4-FIG-093 -->

Figure 93〈Common Command Format〉：定義〈Common Command Format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CDW0, NSID, CDW2, CDW3, MPTR, DPTR, PRP2, PRP1。

- 解決的問題：定義〈Common Command Format〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CDW0, NSID, CDW2, CDW3, MPTR, DPTR, PRP2, PRP1。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 CDW0 作為 parser 的第一個檢查點，再用 NSID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：CDW0, NSID, CDW2, CDW3, MPTR, DPTR, PRP2, PRP1

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, 文件頁 140-142, PDF 頁 166-168

</details>

<details markdown="1">
<summary><strong>Figure 94: Common Command Format - Vendor Specific Commands (Optional)</strong></summary>

<!-- claim:BASE4-FIG-094-CLAIM figure-table:BASE4-FIG-094 -->

Figure 94〈Common Command Format - Vendor Specific Commands (Optional)〉：定義〈Common Command Format - Vendor Specific Commands (Optional)〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CDW0, NSID, MDPTR, NDT, NDM, CDW12, CDW13, CDW14。

- 解決的問題：定義〈Common Command Format - Vendor Specific Commands (Optional)〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CDW0, NSID, MDPTR, NDT, NDM, CDW12, CDW13, CDW14。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 CDW0 作為 parser 的第一個檢查點，再用 NSID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：CDW0, NSID, MDPTR, NDT, NDM, CDW12, CDW13, CDW14

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 94, 文件頁 143, PDF 頁 169

</details>

<a id="section-4-2"></a>

### §4.2

<details markdown="1">
<summary><strong>Figure 97: Common Completion Queue Entry Layout - Admin and All I/O Command Sets</strong></summary>

<!-- claim:BASE4-FIG-097-CLAIM figure-table:BASE4-FIG-097 -->

Figure 97〈Common Completion Queue Entry Layout - Admin and All I/O Command Sets〉：定義〈Common Completion Queue Entry Layout - Admin and All I/O Command Sets〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DW0, DW1, DW2, SQ, DW3, Command Set, Completion Queue, Command。

- 解決的問題：定義〈Common Completion Queue Entry Layout - Admin and All I/O Command Sets〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DW0, DW1, DW2, SQ, DW3, Command Set, Completion Queue, Command。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：以 DW0 作為 parser 的第一個檢查點，再用 DW1 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：DW0, DW1, DW2, SQ, DW3, Command Set, Completion Queue, Command

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 97, 文件頁 144, PDF 頁 170

</details>

<details markdown="1">
<summary><strong>Figure 98: Completion Queue Entry: DW 2</strong></summary>

<!-- claim:BASE4-FIG-098-CLAIM figure-table:BASE4-FIG-098 -->

Figure 98〈Completion Queue Entry: DW 2〉：呈現〈Completion Queue Entry: DW 2〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：SQID, SQHD, DW, SQ, CID, Completion Queue。

- 解決的問題：呈現〈Completion Queue Entry: DW 2〉中的 queue 或 command 關係。

- 閱讀順序：沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：SQID, SQHD, DW, SQ, CID, Completion Queue。

- 條件與限制：來源 keyword 索引：`may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：沿 Figure 98 追蹤一筆 command，以 SQID 與 SQHD 作為擁有者或 pointer 變動檢查點。 此例不新增規格要求。

- 來源欄位索引：SQID, SQHD, DW, SQ, CID, Completion Queue

- 來源 keyword 索引：`may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 98, 文件頁 144, PDF 頁 170

</details>

<details markdown="1">
<summary><strong>Figure 99: Completion Queue Entry: DW 3</strong></summary>

<!-- claim:BASE4-FIG-099-CLAIM figure-table:BASE4-FIG-099 -->

Figure 99〈Completion Queue Entry: DW 3〉：呈現〈Completion Queue Entry: DW 3〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：STATUS, CID, DW, SQ, Completion Queue。

- 解決的問題：呈現〈Completion Queue Entry: DW 3〉中的 queue 或 command 關係。

- 閱讀順序：沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：STATUS, CID, DW, SQ, Completion Queue。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：沿 Figure 99 追蹤一筆 command，以 STATUS 與 CID 作為擁有者或 pointer 變動檢查點。 此例不新增規格要求。

- 來源欄位索引：STATUS, CID, DW, SQ, Completion Queue

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 99, 文件頁 145, PDF 頁 171

</details>

<details markdown="1">
<summary><strong>Figure 101: Completion Queue Entry: Status Field</strong></summary>

<!-- claim:BASE4-FIG-101-CLAIM figure-table:BASE4-FIG-101 -->

Figure 101〈Completion Queue Entry: Status Field〉：定義〈Completion Queue Entry: Status Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DNR, CRD, SCT, SC, ACRE, CRDT1, CRDT2, CRDT3。

- 解決的問題：定義〈Completion Queue Entry: Status Field〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DNR, CRD, SCT, SC, ACRE, CRDT1, CRDT2, CRDT3。

- 條件與限制：來源 keyword 索引：`should not`, `should`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 DNR 作為 parser 的第一個檢查點，再用 CRD 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：DNR, CRD, SCT, SC, ACRE, CRDT1, CRDT2, CRDT3

- 來源 keyword 索引：`should not`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 101, 文件頁 145-146, PDF 頁 171-172

</details>

<details markdown="1">
<summary><strong>Figure 102: Status Code - Status Code Type Values</strong></summary>

<!-- claim:BASE4-FIG-102-CLAIM figure-table:BASE4-FIG-102 -->

Figure 102〈Status Code - Status Code Type Values〉：定義〈Status Code - Status Code Type Values〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：SC, Status Code。

- 解決的問題：定義〈Status Code - Status Code Type Values〉所表示的 status／error 分類。

- 閱讀順序：先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：SC, Status Code。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：收到一筆狀態時先辨認 SC，再檢查 Status Code，不可脫離類別單看數值。 此例不新增規格要求。

- 來源欄位索引：SC, Status Code

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 102, 文件頁 146, PDF 頁 172

</details>

<details markdown="1">
<summary><strong>Figure 103: Status Code - Generic Command Status Values</strong></summary>

<!-- claim:BASE4-FIG-103-CLAIM figure-table:BASE4-FIG-103 -->

Figure 103〈Status Code - Generic Command Status Values〉：定義〈Status Code - Generic Command Status Values〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：ID, SQ, TCG, SGL, PRP, ZNS, RACQA, CMB。

- 解決的問題：定義〈Status Code - Generic Command Status Values〉所表示的 status／error 分類。

- 閱讀順序：先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：ID, SQ, TCG, SGL, PRP, ZNS, RACQA, CMB。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `should`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：收到一筆狀態時先辨認 ID，再檢查 SQ，不可脫離類別單看數值。 此例不新增規格要求。

- 來源欄位索引：ID, SQ, TCG, SGL, PRP, ZNS, RACQA, CMB

- 來源 keyword 索引：`shall not`, `shall`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 103, 文件頁 147-150, PDF 頁 173-176

</details>

<details markdown="1">
<summary><strong>Figure 104: Status Code - Command Specific Status Values</strong></summary>

<!-- claim:BASE4-FIG-104-CLAIM figure-table:BASE4-FIG-104 -->

Figure 104〈Status Code - Command Specific Status Values〉：定義〈Status Code - Command Specific Status Values〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：ANA, NOTE, Status Code, Command。

- 解決的問題：定義〈Status Code - Command Specific Status Values〉所表示的 status／error 分類。

- 閱讀順序：先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：ANA, NOTE, Status Code, Command。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：收到一筆狀態時先辨認 ANA，再檢查 NOTE，不可脫離類別單看數值。 此例不新增規格要求。

- 來源欄位索引：ANA, NOTE, Status Code, Command

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 104, 文件頁 151-152, PDF 頁 177-178

</details>

<details markdown="1">
<summary><strong>Figure 105: Status Code - Command Specific Status Values, I/O Command Set Specific</strong></summary>

<!-- claim:BASE4-FIG-105-CLAIM figure-table:BASE4-FIG-105 -->

Figure 105〈Status Code - Command Specific Status Values, I/O Command Set Specific〉：定義〈Status Code - Command Specific Status Values, I/O Command Set Specific〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：ID, Command Set, Status Code, Command。

- 解決的問題：定義〈Status Code - Command Specific Status Values, I/O Command Set Specific〉所表示的 status／error 分類。

- 閱讀順序：先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：ID, Command Set, Status Code, Command。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：收到一筆狀態時先辨認 ID，再檢查 Command Set，不可脫離類別單看數值。 此例不新增規格要求。

- 來源欄位索引：ID, Command Set, Status Code, Command

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 105, 文件頁 152-153, PDF 頁 178-179

</details>

<details markdown="1">
<summary><strong>Figure 107: Status Code - Media and Data Integrity Error Values</strong></summary>

<!-- claim:BASE4-FIG-107-CLAIM figure-table:BASE4-FIG-107 -->

Figure 107〈Status Code - Media and Data Integrity Error Values〉：定義〈Status Code - Media and Data Integrity Error Values〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：TCG, SCT, Status Code。

- 解決的問題：定義〈Status Code - Media and Data Integrity Error Values〉所表示的 status／error 分類。

- 閱讀順序：先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：TCG, SCT, Status Code。

- 條件與限制：來源 keyword 索引：`should`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：收到一筆狀態時先辨認 TCG，再檢查 SCT，不可脫離類別單看數值。 此例不新增規格要求。

- 來源欄位索引：TCG, SCT, Status Code

- 來源 keyword 索引：`should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 107, 文件頁 154-155, PDF 頁 180-181

</details>

<details markdown="1">
<summary><strong>Figure 108: Status Code - Path Related Status Values</strong></summary>

<!-- claim:BASE4-FIG-108-CLAIM figure-table:BASE4-FIG-108 -->

Figure 108〈Status Code - Path Related Status Values〉：定義〈Status Code - Path Related Status Values〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：DNR, ANA, Status Code。

- 解決的問題：定義〈Status Code - Path Related Status Values〉所表示的 status／error 分類。

- 閱讀順序：先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：DNR, ANA, Status Code。

- 條件與限制：來源 keyword 索引：`should not`, `should`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：收到一筆狀態時先辨認 DNR，再檢查 ANA，不可脫離類別單看數值。 此例不新增規格要求。

- 來源欄位索引：DNR, ANA, Status Code

- 來源 keyword 索引：`should not`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3.3, Figure 108, 文件頁 155, PDF 頁 181

</details>

<details markdown="1">
<summary><strong>Figure 109: Phase Tag bit Transition Example</strong></summary>

<!-- claim:BASE4-FIG-109-CLAIM figure-table:BASE4-FIG-109 -->

Figure 109〈Phase Tag bit Transition Example〉：呈現〈Phase Tag bit Transition Example〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：Phase Tag。

- 解決的問題：呈現〈Phase Tag bit Transition Example〉中的 queue 或 command 關係。

- 閱讀順序：沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：Phase Tag。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：沿 Figure 109 追蹤一筆 command，以 Phase Tag 與 引用條件 作為擁有者或 pointer 變動檢查點。 此例不新增規格要求。

- 來源欄位索引：Phase Tag

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.4, Figure 109, 文件頁 156-157, PDF 頁 182-183

</details>

<a id="section-4-3"></a>

### §4.3

<details markdown="1">
<summary><strong>Figure 110: PRP Entry Layout</strong></summary>

<!-- claim:BASE4-FIG-110-CLAIM figure-table:BASE4-FIG-110 -->

Figure 110〈PRP Entry Layout〉：定義〈PRP Entry Layout〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PRP。

- 解決的問題：定義〈PRP Entry Layout〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PRP。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：以 PRP 作為 parser 的第一個檢查點，再用 引用條件 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：PRP

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 110, 文件頁 158, PDF 頁 184

</details>

<details markdown="1">
<summary><strong>Figure 111: PRP Entry - Page Base Address and Offset</strong></summary>

<!-- claim:BASE4-FIG-111-CLAIM figure-table:BASE4-FIG-111 -->

Figure 111〈PRP Entry - Page Base Address and Offset〉：呈現〈PRP Entry - Page Base Address and Offset〉如何把 transfer 對映到 host memory。 依序追蹤 address、length、page／segment boundary 與下一個 entry 的連結；來源索引：PBAO, PRP。

- 解決的問題：呈現〈PRP Entry - Page Base Address and Offset〉如何把 transfer 對映到 host memory。

- 閱讀順序：依序追蹤 address、length、page／segment boundary 與下一個 entry 的連結；來源索引：PBAO, PRP。

- 條件與限制：來源 keyword 索引：`shall`, `may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：從 PBAO 所示位置開始對映 transfer，再核對 PRP 的邊界或下一個元素後才繼續。 此例不新增規格要求。

- 來源欄位索引：PBAO, PRP

- 來源 keyword 索引：`shall`, `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 111, 文件頁 158, PDF 頁 184

</details>

<details markdown="1">
<summary><strong>Figure 112: PRP List Layout for Physically Contiguous Memory Pages</strong></summary>

<!-- claim:BASE4-FIG-112-CLAIM figure-table:BASE4-FIG-112 -->

Figure 112〈PRP List Layout for Physically Contiguous Memory Pages〉：定義〈PRP List Layout for Physically Contiguous Memory Pages〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PRP, Memory Page。

- 解決的問題：定義〈PRP List Layout for Physically Contiguous Memory Pages〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PRP, Memory Page。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：以 PRP 作為 parser 的第一個檢查點，再用 Memory Page 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：PRP, Memory Page

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 112, 文件頁 159, PDF 頁 185

</details>

<details markdown="1">
<summary><strong>Figure 113: PRP List Layout for Physically Non-Contiguous Memory Pages</strong></summary>

<!-- claim:BASE4-FIG-113-CLAIM figure-table:BASE4-FIG-113 -->

Figure 113〈PRP List Layout for Physically Non-Contiguous Memory Pages〉：定義〈PRP List Layout for Physically Non-Contiguous Memory Pages〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PRP, CC.MPS, Memory Page。

- 解決的問題：定義〈PRP List Layout for Physically Non-Contiguous Memory Pages〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PRP, CC.MPS, Memory Page。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 PRP 作為 parser 的第一個檢查點，再用 CC.MPS 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：PRP, CC.MPS, Memory Page

- 來源 keyword 索引：`shall`, `should`, `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 113, 文件頁 159, PDF 頁 185

</details>

<details markdown="1">
<summary><strong>Figure 114: SGL Validation Error Conditions</strong></summary>

<!-- claim:BASE4-FIG-114-CLAIM figure-table:BASE4-FIG-114 -->

Figure 114〈SGL Validation Error Conditions〉：定義〈SGL Validation Error Conditions〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：SGL。

- 解決的問題：定義〈SGL Validation Error Conditions〉所表示的 status／error 分類。

- 閱讀順序：先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：SGL。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：收到一筆狀態時先辨認 SGL，再檢查 引用條件，不可脫離類別單看數值。 此例不新增規格要求。

- 來源欄位索引：SGL

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 114, 文件頁 161, PDF 頁 187

</details>

<details markdown="1">
<summary><strong>Figure 115: SGL Segment</strong></summary>

<!-- claim:BASE4-FIG-115-CLAIM figure-table:BASE4-FIG-115 -->

Figure 115〈SGL Segment〉：呈現〈SGL Segment〉如何把 transfer 對映到 host memory。 依序追蹤 address、length、page／segment boundary 與下一個 entry 的連結；來源索引：SGL。

- 解決的問題：呈現〈SGL Segment〉如何把 transfer 對映到 host memory。

- 閱讀順序：依序追蹤 address、length、page／segment boundary 與下一個 entry 的連結；來源索引：SGL。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：從 SGL 所示位置開始對映 transfer，再核對 引用條件 的邊界或下一個元素後才繼續。 此例不新增規格要求。

- 來源欄位索引：SGL

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 115, 文件頁 161, PDF 頁 187

</details>

<details markdown="1">
<summary><strong>Figure 116: Generic SGL Descriptor Format</strong></summary>

<!-- claim:BASE4-FIG-116-CLAIM figure-table:BASE4-FIG-116 -->

Figure 116〈Generic SGL Descriptor Format〉：定義〈Generic SGL Descriptor Format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DTS, SGLID, SGLDT, SGLDST, SGL, NULL。

- 解決的問題：定義〈Generic SGL Descriptor Format〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DTS, SGLID, SGLDT, SGLDST, SGL, NULL。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 DTS 作為 parser 的第一個檢查點，再用 SGLID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：DTS, SGLID, SGLDT, SGLDST, SGL, NULL

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 116, 文件頁 161, PDF 頁 187

</details>

<details markdown="1">
<summary><strong>Figure 117: SGL Descriptor Type</strong></summary>

<!-- claim:BASE4-FIG-117-CLAIM figure-table:BASE4-FIG-117 -->

Figure 117〈SGL Descriptor Type〉：定義〈SGL Descriptor Type〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：SGL。

- 解決的問題：定義〈SGL Descriptor Type〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：SGL。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 本報告只解釋 PCIe／memory-based 部分。

- 說明性範例（informative example）：以 SGL 作為 parser 的第一個檢查點，再用 引用條件 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：SGL

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 117, 文件頁 161-162, PDF 頁 187-188

</details>

<details markdown="1">
<summary><strong>Figure 118: SGL Descriptor Sub Type Values</strong></summary>

<!-- claim:BASE4-FIG-118-CLAIM figure-table:BASE4-FIG-118 -->

Figure 118〈SGL Descriptor Sub Type Values〉：定義〈SGL Descriptor Sub Type Values〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：SGL。

- 解決的問題：定義〈SGL Descriptor Sub Type Values〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：SGL。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 本報告只解釋 PCIe／memory-based 部分。

- 說明性範例（informative example）：以 SGL 作為 parser 的第一個檢查點，再用 引用條件 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：SGL

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 118, 文件頁 162, PDF 頁 188

</details>

<details markdown="1">
<summary><strong>Figure 119: SGL Data Block descriptor</strong></summary>

<!-- claim:BASE4-FIG-119-CLAIM figure-table:BASE4-FIG-119 -->

Figure 119〈SGL Data Block descriptor〉：定義〈SGL Data Block descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ADDR, LEN, SGLID, SGLDT, SGLDST, SGL, SGLS。

- 解決的問題：定義〈SGL Data Block descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ADDR, LEN, SGLID, SGLDT, SGLDST, SGL, SGLS。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 ADDR 作為 parser 的第一個檢查點，再用 LEN 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：ADDR, LEN, SGLID, SGLDT, SGLDST, SGL, SGLS

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 119, 文件頁 162-163, PDF 頁 188-189

</details>

<details markdown="1">
<summary><strong>Figure 120: SGL Bit Bucket descriptor</strong></summary>

<!-- claim:BASE4-FIG-120-CLAIM figure-table:BASE4-FIG-120 -->

Figure 120〈SGL Bit Bucket descriptor〉：定義〈SGL Bit Bucket descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：LEN, SGLID, SGLDT, SGLDST, SGL, NLB。

- 解決的問題：定義〈SGL Bit Bucket descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：LEN, SGLID, SGLDT, SGLDST, SGL, NLB。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 LEN 作為 parser 的第一個檢查點，再用 SGLID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：LEN, SGLID, SGLDT, SGLDST, SGL, NLB

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 120, 文件頁 163, PDF 頁 189

</details>

<details markdown="1">
<summary><strong>Figure 121: SGL Segment descriptor</strong></summary>

<!-- claim:BASE4-FIG-121-CLAIM figure-table:BASE4-FIG-121 -->

Figure 121〈SGL Segment descriptor〉：定義〈SGL Segment descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ADDR, LEN, SGLID, SGLDT, SGDST, SGL。

- 解決的問題：定義〈SGL Segment descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ADDR, LEN, SGLID, SGLDT, SGDST, SGL。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 ADDR 作為 parser 的第一個檢查點，再用 LEN 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：ADDR, LEN, SGLID, SGLDT, SGDST, SGL

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 121, 文件頁 163, PDF 頁 189

</details>

<details markdown="1">
<summary><strong>Figure 122: SGL Last Segment descriptor</strong></summary>

<!-- claim:BASE4-FIG-122-CLAIM figure-table:BASE4-FIG-122 -->

Figure 122〈SGL Last Segment descriptor〉：定義〈SGL Last Segment descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ADDR, LEN, SGLID, SGLDT, SGLDST, SGL。

- 解決的問題：定義〈SGL Last Segment descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ADDR, LEN, SGLID, SGLDT, SGLDST, SGL。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 ADDR 作為 parser 的第一個檢查點，再用 LEN 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：ADDR, LEN, SGLID, SGLDT, SGLDST, SGL

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 122, 文件頁 164, PDF 頁 190

</details>

<details markdown="1">
<summary><strong>Figure 125: SGL Read Example</strong></summary>

<!-- claim:BASE4-FIG-125-CLAIM figure-table:BASE4-FIG-125 -->

Figure 125〈SGL Read Example〉：呈現〈SGL Read Example〉如何把 transfer 對映到 host memory。 依序追蹤 address、length、page／segment boundary 與下一個 entry 的連結；來源索引：SGL。

- 解決的問題：呈現〈SGL Read Example〉如何把 transfer 對映到 host memory。

- 閱讀順序：依序追蹤 address、length、page／segment boundary 與下一個 entry 的連結；來源索引：SGL。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：從 SGL 所示位置開始對映 transfer，再核對 引用條件 的邊界或下一個元素後才繼續。 此例不新增規格要求。

- 來源欄位索引：SGL

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2.1, Figure 125, 文件頁 166, PDF 頁 192

</details>

<a id="section-4-4"></a>

### §4.4

<details markdown="1">
<summary><strong>Figure 126: Current Value after Reset with Scope of Entire NVM Subsystem</strong></summary>

<!-- claim:BASE4-FIG-126-CLAIM figure-table:BASE4-FIG-126 -->

Figure 126〈Current Value after Reset with Scope of Entire NVM Subsystem〉：呈現〈Current Value after Reset with Scope of Entire NVM Subsystem〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem。

- 解決的問題：呈現〈Current Value after Reset with Scope of Entire NVM Subsystem〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Subsystem 標示的一個物件，再追到 引用條件，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Subsystem

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.4, Figure 126, 文件頁 167, PDF 頁 193

</details>

<details markdown="1">
<summary><strong>Figure 127: Current Value after Reset with Scope of Subset of the NVM Subsystem</strong></summary>

<!-- claim:BASE4-FIG-127-CLAIM figure-table:BASE4-FIG-127 -->

Figure 127〈Current Value after Reset with Scope of Subset of the NVM Subsystem〉：呈現〈Current Value after Reset with Scope of Subset of the NVM Subsystem〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem。

- 解決的問題：呈現〈Current Value after Reset with Scope of Subset of the NVM Subsystem〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 NVM Subsystem 標示的一個物件，再追到 引用條件，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：NVM Subsystem

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.4, Figure 127, 文件頁 168, PDF 頁 194

</details>

<a id="section-4-5"></a>

### §4.5

<details markdown="1">
<summary><strong>Figure 128: PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)</strong></summary>

<!-- claim:BASE4-FIG-128-CLAIM figure-table:BASE4-FIG-128 -->

Figure 128〈PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)〉：呈現〈PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：ID, VID, SSVID。

- 解決的問題：呈現〈PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：ID, VID, SSVID。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：選擇 ID 標示的一個物件，再追到 VID，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：ID, VID, SSVID

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.1, Figure 128, 文件頁 169, PDF 頁 195

</details>

<details markdown="1">
<summary><strong>Figure 129: Serial Number (SN) and Model Number (MN)</strong></summary>

<!-- claim:BASE4-FIG-129-CLAIM figure-table:BASE4-FIG-129 -->

Figure 129〈Serial Number (SN) and Model Number (MN)〉：定義〈Serial Number (SN) and Model Number (MN)〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：SN, MN。

- 解決的問題：定義〈Serial Number (SN) and Model Number (MN)〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：SN, MN。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依定義寬度解析 SN，再核對 MN 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：SN, MN

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.2, Figure 129, 文件頁 170, PDF 頁 196

</details>

<details markdown="1">
<summary><strong>Figure 130: IEEE OUI Identifier (IEEE)</strong></summary>

<!-- claim:BASE4-FIG-130-CLAIM figure-table:BASE4-FIG-130 -->

Figure 130〈IEEE OUI Identifier (IEEE)〉：定義〈IEEE OUI Identifier (IEEE)〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：IEEE, OUI。

- 解決的問題：定義〈IEEE OUI Identifier (IEEE)〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：IEEE, OUI。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依定義寬度解析 IEEE，再核對 OUI 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：IEEE, OUI

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.3, Figure 130, 文件頁 170, PDF 頁 196

</details>

<details markdown="1">
<summary><strong>Figure 131: IEEE Extended Unique Identifier (EUI64), MA-L Format</strong></summary>

<!-- claim:BASE4-FIG-131-CLAIM figure-table:BASE4-FIG-131 -->

Figure 131〈IEEE Extended Unique Identifier (EUI64), MA-L Format〉：定義〈IEEE Extended Unique Identifier (EUI64), MA-L Format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：IEEE, EUI64, MA, EUI, OUI。

- 解決的問題：定義〈IEEE Extended Unique Identifier (EUI64), MA-L Format〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：IEEE, EUI64, MA, EUI, OUI。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：以 IEEE 作為 parser 的第一個檢查點，再用 EUI64 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：IEEE, EUI64, MA, EUI, OUI

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 131, 文件頁 170, PDF 頁 196

</details>

<details markdown="1">
<summary><strong>Figure 132: IEEE Extended Unique Identifier (EUI64), OUI Identifier</strong></summary>

<!-- claim:BASE4-FIG-132-CLAIM figure-table:BASE4-FIG-132 -->

Figure 132〈IEEE Extended Unique Identifier (EUI64), OUI Identifier〉：定義〈IEEE Extended Unique Identifier (EUI64), OUI Identifier〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：IEEE, EUI64, OUI。

- 解決的問題：定義〈IEEE Extended Unique Identifier (EUI64), OUI Identifier〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：IEEE, EUI64, OUI。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依定義寬度解析 IEEE，再核對 EUI64 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：IEEE, EUI64, OUI

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 132, 文件頁 170, PDF 頁 196

</details>

<details markdown="1">
<summary><strong>Figure 133: IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)</strong></summary>

<!-- claim:BASE4-FIG-133-CLAIM figure-table:BASE4-FIG-133 -->

Figure 133〈IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)〉：定義〈IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：IEEE, EUI64, ID, MA, WWN, NAA。

- 解決的問題：定義〈IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：IEEE, EUI64, ID, MA, WWN, NAA。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依定義寬度解析 IEEE，再核對 EUI64 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：IEEE, EUI64, ID, MA, WWN, NAA

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 133, 文件頁 170-171, PDF 頁 196-197

</details>

<details markdown="1">
<summary><strong>Figure 134: MA-L similarity to WWN</strong></summary>

<!-- claim:BASE4-FIG-134-CLAIM figure-table:BASE4-FIG-134 -->

Figure 134〈MA-L similarity to WWN〉：定義〈MA-L similarity to WWN〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：MA, WWN。

- 解決的問題：定義〈MA-L similarity to WWN〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：MA, WWN。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依定義寬度解析 MA，再核對 WWN 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：MA, WWN

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 134, 文件頁 171, PDF 頁 197

</details>

<details markdown="1">
<summary><strong>Figure 135: Namespace Globally Unique Identifier (NGUID)</strong></summary>

<!-- claim:BASE4-FIG-135-CLAIM figure-table:BASE4-FIG-135 -->

Figure 135〈Namespace Globally Unique Identifier (NGUID)〉：定義〈Namespace Globally Unique Identifier (NGUID)〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NGUID, Namespace。

- 解決的問題：定義〈Namespace Globally Unique Identifier (NGUID)〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NGUID, Namespace。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依定義寬度解析 NGUID，再核對 Namespace 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：NGUID, Namespace

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 135, 文件頁 171, PDF 頁 197

</details>

<details markdown="1">
<summary><strong>Figure 136: Namespace Globally Unique Identifier (NGUID), OUI</strong></summary>

<!-- claim:BASE4-FIG-136-CLAIM figure-table:BASE4-FIG-136 -->

Figure 136〈Namespace Globally Unique Identifier (NGUID), OUI〉：定義〈Namespace Globally Unique Identifier (NGUID), OUI〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NGUID, OUI, VSP, ID, Namespace。

- 解決的問題：定義〈Namespace Globally Unique Identifier (NGUID), OUI〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NGUID, OUI, VSP, ID, Namespace。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依定義寬度解析 NGUID，再核對 OUI 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：NGUID, OUI, VSP, ID, Namespace

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 136, 文件頁 171, PDF 頁 197

</details>

<details markdown="1">
<summary><strong>Figure 137: Namespace Globally Unique Identifier</strong></summary>

<!-- claim:BASE4-FIG-137-CLAIM figure-table:BASE4-FIG-137 -->

Figure 137〈Namespace Globally Unique Identifier〉：定義〈Namespace Globally Unique Identifier〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NGUID, WWN, IEEE, NAA, Namespace。

- 解決的問題：定義〈Namespace Globally Unique Identifier〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NGUID, WWN, IEEE, NAA, Namespace。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依定義寬度解析 NGUID，再核對 WWN 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：NGUID, WWN, IEEE, NAA, Namespace

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 137, 文件頁 171, PDF 頁 197

</details>

<details markdown="1">
<summary><strong>Figure 138: Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN</strong></summary>

<!-- claim:BASE4-FIG-138-CLAIM figure-table:BASE4-FIG-138 -->

Figure 138〈Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN〉：定義〈Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NGUID, WWN, OUI, NAA, Namespace。

- 解決的問題：定義〈Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NGUID, WWN, OUI, NAA, Namespace。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依定義寬度解析 NGUID，再核對 WWN 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：NGUID, WWN, OUI, NAA, Namespace

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 138, 文件頁 171, PDF 頁 197

</details>

<a id="section-4-6"></a>

### §4.6

<details markdown="1">
<summary><strong>Figure 139: Controller List Format</strong></summary>

<!-- claim:BASE4-FIG-139-CLAIM figure-table:BASE4-FIG-139 -->

Figure 139〈Controller List Format〉：定義〈Controller List Format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NUMCIDS, Controller。

- 解決的問題：定義〈Controller List Format〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NUMCIDS, Controller。

- 條件與限制：來源 keyword 索引：`may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 NUMCIDS 作為 parser 的第一個檢查點，再用 Controller 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：NUMCIDS, Controller

- 來源 keyword 索引：`may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.6.1, Figure 139, 文件頁 172, PDF 頁 198

</details>

<details markdown="1">
<summary><strong>Figure 140: Namespace List Format</strong></summary>

<!-- claim:BASE4-FIG-140-CLAIM figure-table:BASE4-FIG-140 -->

Figure 140〈Namespace List Format〉：定義〈Namespace List Format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ID, Namespace。

- 解決的問題：定義〈Namespace List Format〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ID, Namespace。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：以 ID 作為 parser 的第一個檢查點，再用 Namespace 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：ID, Namespace

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.6.2, Figure 140, 文件頁 172, PDF 頁 198

</details>

<a id="section-4-8"></a>

### §4.8

<details markdown="1">
<summary><strong>Figure 142: UTF-8 Input Processing</strong></summary>

<!-- claim:BASE4-FIG-142-CLAIM figure-table:BASE4-FIG-142 -->

Figure 142〈UTF-8 Input Processing〉：呈現〈UTF-8 Input Processing〉要求的輸入驗證順序。 依序執行 decoding、禁止 code point 與 truncation 檢查；來源索引：UTF。

- 解決的問題：呈現〈UTF-8 Input Processing〉要求的輸入驗證順序。

- 閱讀順序：依序執行 decoding、禁止 code point 與 truncation 檢查；來源索引：UTF。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：先驗證 UTF；若 引用條件 對應的檢查失敗，就在接受字串前拒絕輸入。 此例不新增規格要求。

- 來源欄位索引：UTF

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.8, Figure 142, 文件頁 175, PDF 頁 201

</details>

## 使用與限制

製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata 集合或核准範圍改變時，必須重新核對受影響 claim。
