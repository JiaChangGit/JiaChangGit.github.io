---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4 第 4 章：SQE、CQE、Status、PRP 與 SGL"
date: 2026-08-28
description: "供 GitHub Pages 與 PPT 使用的 NVMe 規格導讀。"
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---

# NVMe Base 2.4 第 4 章：SQE、CQE、Status、PRP 與 SGL

用途：供 GitHub Pages 閱讀與 100 分鐘簡報製作；讀者已具備 PCIe 與 NVMe 基礎。

範圍：§4；文件頁 139–175；PDF 頁 165–201。正文只保留 PCIe／memory-based 與通用 NVMe 內容。

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

### 1. BASE4-SQE

<!-- claim:BASE4-SQE -->

Admin 與 I/O common SQE 固定為 64 bytes。CDW0、NSID、data pointer 與 CDW10–15 的通用位置先固定，再由各 command 定義命令專屬內容。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 文件頁 139-143, PDF 頁 165-169

### 2. BASE4-CID

<!-- claim:BASE4-CID -->

CID 與 Submission Queue identifier 的組合用來唯一識別 command；FFFFh 宜（should）避免使用，因 Error Information log 以該值表示錯誤未對應特定 command。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 文件頁 140, PDF 頁 166

### 3. BASE4-PSDT

<!-- claim:BASE4-PSDT -->

CDW0.PSDT 決定 DPTR 解讀為 PRP 或 SGL。NVMe over PCIe 的 Admin command 原則上必須（shall）使用 PRP，除非 command 定義另有規定。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 文件頁 140-142, PDF 頁 166-168

### 4. BASE4-CQE

<!-- claim:BASE4-CQE -->

common CQE 至少 16 bytes；若以多次寫入建立 CQE，Phase Tag 必須（shall）在最後一次寫入更新，避免 host 看到半成品。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, 文件頁 144-145, PDF 頁 170-171

### 5. BASE4-STATUS

<!-- claim:BASE4-STATUS -->

status 要先解 Status Code Type（SCT），再解 Status Code（SC），同時檢查 Do Not Retry（DNR）等控制 bit；數值不能脫離 SCT 單獨解讀。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, 文件頁 145-155, PDF 頁 171-181

### 6. BASE4-PHASE

<!-- claim:BASE4-PHASE -->

Phase Tag 讓 host 判斷環形 Completion Queue slot 是否為新完成項目；host 消費 CQE 後推進 CQ head doorbell，wrap 時預期 phase 翻轉。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.4, 文件頁 155-158, PDF 頁 181-184

### 7. BASE4-PRP

<!-- claim:BASE4-PRP -->

PRP 以固定大小 entry 指向 physical memory page。第一個 entry 可含 page offset；後續 PRP 必須（shall）符合 page alignment，資料長度決定需要幾個 entry。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, 文件頁 158-159, PDF 頁 184-185

### 8. BASE4-SGL

<!-- claim:BASE4-SGL -->

SGL 由一個以上 descriptor／segment 描述資料 buffer。SGL length 必須（shall）大於等於 requested transfer length；本報告只介紹 PCIe 可用的通用 descriptor。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, 文件頁 159-166, PDF 頁 185-192

### 9. BASE4-FEATURE

<!-- claim:BASE4-FEATURE -->

Feature 可能具有 default、saved、current value；saved value 支援與跨 reset／power cycle 的 persistence 由 SSFS 與各 Feature capability 判定。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.4, 文件頁 166-169, PDF 頁 192-195

### 10. BASE4-IDENTIFIER

<!-- claim:BASE4-IDENTIFIER -->

VID／SSVID、SN／MN、IEEE OUI、EUI64、NGUID 與 UUID 的來源、長度與唯一性範圍不同；不能只因外觀相似就互換。此節為 informative。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5, 文件頁 169-172, PDF 頁 195-198

### 11. BASE4-LISTS

<!-- claim:BASE4-LISTS -->

Controller List 與 Namespace List 都先給出數量，再排列 identifier；實作 parser 時，先依格式定義的上限與保留區驗證輸入。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.6, 文件頁 172-173, PDF 頁 198-199

### 12. BASE4-UTF8

<!-- claim:BASE4-UTF8 -->

處理 UTF-8 輸入時要依規格流程驗證編碼、禁止的 code point 與截斷情況；不可把任意 byte sequence 當成有效字串。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.8, 文件頁 175, PDF 頁 201

## Figure 逐圖導讀

本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。

### Figure 92: Command Dword 0

<!-- claim:BASE4-FIG-092-CLAIM figure-table:BASE4-FIG-092 -->

Figure 92〈Command Dword 0〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 92, 文件頁 139-140, PDF 頁 165-166

### Figure 93: Common Command Format

<!-- claim:BASE4-FIG-093-CLAIM figure-table:BASE4-FIG-093 -->

Figure 93〈Common Command Format〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, 文件頁 140-142, PDF 頁 166-168

### Figure 94: Common Command Format – Vendor Specific Commands (Optional)

<!-- claim:BASE4-FIG-094-CLAIM figure-table:BASE4-FIG-094 -->

Figure 94〈Common Command Format – Vendor Specific Commands (Optional)〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 94, 文件頁 143, PDF 頁 169

### Figure 97: Common Completion Queue Entry Layout – Admin and All I/O Command Sets

<!-- claim:BASE4-FIG-097-CLAIM figure-table:BASE4-FIG-097 -->

Figure 97〈Common Completion Queue Entry Layout – Admin and All I/O Command Sets〉：整理 queue／command 的關係或處理順序。 依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 解決的問題：整理 queue／command 的關係或處理順序。

- 閱讀順序：依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先選一個 queue identifier，沿箭頭追蹤一筆 command 與 completion。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 97, 文件頁 144, PDF 頁 170

### Figure 98: Completion Queue Entry: DW 2

<!-- claim:BASE4-FIG-098-CLAIM figure-table:BASE4-FIG-098 -->

Figure 98〈Completion Queue Entry: DW 2〉：整理 queue／command 的關係或處理順序。 依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 解決的問題：整理 queue／command 的關係或處理順序。

- 閱讀順序：依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先選一個 queue identifier，沿箭頭追蹤一筆 command 與 completion。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 98, 文件頁 144, PDF 頁 170

### Figure 99: Completion Queue Entry: DW 3

<!-- claim:BASE4-FIG-099-CLAIM figure-table:BASE4-FIG-099 -->

Figure 99〈Completion Queue Entry: DW 3〉：整理 queue／command 的關係或處理順序。 依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 解決的問題：整理 queue／command 的關係或處理順序。

- 閱讀順序：依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先選一個 queue identifier，沿箭頭追蹤一筆 command 與 completion。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 99, 文件頁 145, PDF 頁 171

### Figure 101: Completion Queue Entry: Status Field

<!-- claim:BASE4-FIG-101-CLAIM figure-table:BASE4-FIG-101 -->

Figure 101〈Completion Queue Entry: Status Field〉：整理 queue／command 的關係或處理順序。 依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 解決的問題：整理 queue／command 的關係或處理順序。

- 閱讀順序：依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先選一個 queue identifier，沿箭頭追蹤一筆 command 與 completion。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 101, 文件頁 145-146, PDF 頁 171-172

### Figure 102: Status Code – Status Code Type Values

<!-- claim:BASE4-FIG-102-CLAIM figure-table:BASE4-FIG-102 -->

Figure 102〈Status Code – Status Code Type Values〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 102, 文件頁 146, PDF 頁 172

### Figure 103: Status Code – Generic Command Status Values

<!-- claim:BASE4-FIG-103-CLAIM figure-table:BASE4-FIG-103 -->

Figure 103〈Status Code – Generic Command Status Values〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 103, 文件頁 147-150, PDF 頁 173-176

### Figure 104: Status Code – Command Specific Status Values

<!-- claim:BASE4-FIG-104-CLAIM figure-table:BASE4-FIG-104 -->

Figure 104〈Status Code – Command Specific Status Values〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 104, 文件頁 151-152, PDF 頁 177-178

### Figure 105: Status Code – Command Specific Status Values, I/O Command Set Specific

<!-- claim:BASE4-FIG-105-CLAIM figure-table:BASE4-FIG-105 -->

Figure 105〈Status Code – Command Specific Status Values, I/O Command Set Specific〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 105, 文件頁 152-153, PDF 頁 178-179

### Figure 107: Status Code – Media and Data Integrity Error Values

<!-- claim:BASE4-FIG-107-CLAIM figure-table:BASE4-FIG-107 -->

Figure 107〈Status Code – Media and Data Integrity Error Values〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 107, 文件頁 154-155, PDF 頁 180-181

### Figure 108: Status Code – Path Related Status Values

<!-- claim:BASE4-FIG-108-CLAIM figure-table:BASE4-FIG-108 -->

Figure 108〈Status Code – Path Related Status Values〉：整理狀態、錯誤或其分類欄位。 先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 解決的問題：整理狀態、錯誤或其分類欄位。

- 閱讀順序：先讀類型與控制 bit，再在正確類型下解讀 code；保留值不自行賦義。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：以一筆失敗 CQE 為例，先解 SCT，再解 SC 與 DNR。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3.3, Figure 108, 文件頁 155, PDF 頁 181

### Figure 109: Phase Tag bit Transition Example

<!-- claim:BASE4-FIG-109-CLAIM figure-table:BASE4-FIG-109 -->

Figure 109〈Phase Tag bit Transition Example〉：整理 queue／command 的關係或處理順序。 依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 解決的問題：整理 queue／command 的關係或處理順序。

- 閱讀順序：依 host、SQ、controller、CQ 與 pointer／phase 的方向閱讀。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：先選一個 queue identifier，沿箭頭追蹤一筆 command 與 completion。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.4, Figure 109, 文件頁 156-157, PDF 頁 182-183

### Figure 110: PRP Entry Layout

<!-- claim:BASE4-FIG-110-CLAIM figure-table:BASE4-FIG-110 -->

Figure 110〈PRP Entry Layout〉：說明資料 buffer 如何由 PRP／SGL 結構描述。 逐一核對 address、offset、length、alignment 與下一層 pointer。

- 解決的問題：說明資料 buffer 如何由 PRP／SGL 結構描述。

- 閱讀順序：逐一核對 address、offset、length、alignment 與下一層 pointer。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：用跨兩個 memory page 的 buffer 檢查第一個 offset 與後續 alignment。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 110, 文件頁 158, PDF 頁 184

### Figure 111: PRP Entry – Page Base Address and Offset

<!-- claim:BASE4-FIG-111-CLAIM figure-table:BASE4-FIG-111 -->

Figure 111〈PRP Entry – Page Base Address and Offset〉：說明資料 buffer 如何由 PRP／SGL 結構描述。 逐一核對 address、offset、length、alignment 與下一層 pointer。

- 解決的問題：說明資料 buffer 如何由 PRP／SGL 結構描述。

- 閱讀順序：逐一核對 address、offset、length、alignment 與下一層 pointer。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：用跨兩個 memory page 的 buffer 檢查第一個 offset 與後續 alignment。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 111, 文件頁 158, PDF 頁 184

### Figure 112: PRP List Layout for Physically Contiguous Memory Pages

<!-- claim:BASE4-FIG-112-CLAIM figure-table:BASE4-FIG-112 -->

Figure 112〈PRP List Layout for Physically Contiguous Memory Pages〉：說明資料 buffer 如何由 PRP／SGL 結構描述。 逐一核對 address、offset、length、alignment 與下一層 pointer。

- 解決的問題：說明資料 buffer 如何由 PRP／SGL 結構描述。

- 閱讀順序：逐一核對 address、offset、length、alignment 與下一層 pointer。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：用跨兩個 memory page 的 buffer 檢查第一個 offset 與後續 alignment。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 112, 文件頁 159, PDF 頁 185

### Figure 113: PRP List Layout for Physically Non-Contiguous Memory Pages

<!-- claim:BASE4-FIG-113-CLAIM figure-table:BASE4-FIG-113 -->

Figure 113〈PRP List Layout for Physically Non-Contiguous Memory Pages〉：說明資料 buffer 如何由 PRP／SGL 結構描述。 逐一核對 address、offset、length、alignment 與下一層 pointer。

- 解決的問題：說明資料 buffer 如何由 PRP／SGL 結構描述。

- 閱讀順序：逐一核對 address、offset、length、alignment 與下一層 pointer。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：用跨兩個 memory page 的 buffer 檢查第一個 offset 與後續 alignment。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 113, 文件頁 159, PDF 頁 185

### Figure 114: SGL Validation Error Conditions

<!-- claim:BASE4-FIG-114-CLAIM figure-table:BASE4-FIG-114 -->

Figure 114〈SGL Validation Error Conditions〉：說明資料 buffer 如何由 PRP／SGL 結構描述。 逐一核對 address、offset、length、alignment 與下一層 pointer。

- 解決的問題：說明資料 buffer 如何由 PRP／SGL 結構描述。

- 閱讀順序：逐一核對 address、offset、length、alignment 與下一層 pointer。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：用跨兩個 memory page 的 buffer 檢查第一個 offset 與後續 alignment。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 114, 文件頁 161, PDF 頁 187

### Figure 115: SGL Segment

<!-- claim:BASE4-FIG-115-CLAIM figure-table:BASE4-FIG-115 -->

Figure 115〈SGL Segment〉：說明資料 buffer 如何由 PRP／SGL 結構描述。 逐一核對 address、offset、length、alignment 與下一層 pointer。

- 解決的問題：說明資料 buffer 如何由 PRP／SGL 結構描述。

- 閱讀順序：逐一核對 address、offset、length、alignment 與下一層 pointer。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：用跨兩個 memory page 的 buffer 檢查第一個 offset 與後續 alignment。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 115, 文件頁 161, PDF 頁 187

### Figure 116: Generic SGL Descriptor Format

<!-- claim:BASE4-FIG-116-CLAIM figure-table:BASE4-FIG-116 -->

Figure 116〈Generic SGL Descriptor Format〉：說明資料 buffer 如何由 PRP／SGL 結構描述。 逐一核對 address、offset、length、alignment 與下一層 pointer。

- 解決的問題：說明資料 buffer 如何由 PRP／SGL 結構描述。

- 閱讀順序：逐一核對 address、offset、length、alignment 與下一層 pointer。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：用跨兩個 memory page 的 buffer 檢查第一個 offset 與後續 alignment。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 116, 文件頁 161, PDF 頁 187

### Figure 117: SGL Descriptor Type

<!-- claim:BASE4-FIG-117-CLAIM figure-table:BASE4-FIG-117 -->

Figure 117〈SGL Descriptor Type〉：說明資料 buffer 如何由 PRP／SGL 結構描述。 逐一核對 address、offset、length、alignment 與下一層 pointer。 本報告只解釋圖中的 PCIe／memory-based 部分。

- 解決的問題：說明資料 buffer 如何由 PRP／SGL 結構描述。

- 閱讀順序：逐一核對 address、offset、length、alignment 與下一層 pointer。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：用跨兩個 memory page 的 buffer 檢查第一個 offset 與後續 alignment。此例不新增規格要求。

- 範圍：只介紹 PCIe／memory-based 部分。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 117, 文件頁 161-162, PDF 頁 187-188

### Figure 118: SGL Descriptor Sub Type Values

<!-- claim:BASE4-FIG-118-CLAIM figure-table:BASE4-FIG-118 -->

Figure 118〈SGL Descriptor Sub Type Values〉：說明資料 buffer 如何由 PRP／SGL 結構描述。 逐一核對 address、offset、length、alignment 與下一層 pointer。 本報告只解釋圖中的 PCIe／memory-based 部分。

- 解決的問題：說明資料 buffer 如何由 PRP／SGL 結構描述。

- 閱讀順序：逐一核對 address、offset、length、alignment 與下一層 pointer。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：用跨兩個 memory page 的 buffer 檢查第一個 offset 與後續 alignment。此例不新增規格要求。

- 範圍：只介紹 PCIe／memory-based 部分。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 118, 文件頁 162, PDF 頁 188

### Figure 119: SGL Data Block descriptor

<!-- claim:BASE4-FIG-119-CLAIM figure-table:BASE4-FIG-119 -->

Figure 119〈SGL Data Block descriptor〉：說明資料 buffer 如何由 PRP／SGL 結構描述。 逐一核對 address、offset、length、alignment 與下一層 pointer。

- 解決的問題：說明資料 buffer 如何由 PRP／SGL 結構描述。

- 閱讀順序：逐一核對 address、offset、length、alignment 與下一層 pointer。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：用跨兩個 memory page 的 buffer 檢查第一個 offset 與後續 alignment。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 119, 文件頁 162-163, PDF 頁 188-189

### Figure 120: SGL Bit Bucket descriptor

<!-- claim:BASE4-FIG-120-CLAIM figure-table:BASE4-FIG-120 -->

Figure 120〈SGL Bit Bucket descriptor〉：說明資料 buffer 如何由 PRP／SGL 結構描述。 逐一核對 address、offset、length、alignment 與下一層 pointer。

- 解決的問題：說明資料 buffer 如何由 PRP／SGL 結構描述。

- 閱讀順序：逐一核對 address、offset、length、alignment 與下一層 pointer。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：用跨兩個 memory page 的 buffer 檢查第一個 offset 與後續 alignment。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 120, 文件頁 163, PDF 頁 189

### Figure 121: SGL Segment descriptor

<!-- claim:BASE4-FIG-121-CLAIM figure-table:BASE4-FIG-121 -->

Figure 121〈SGL Segment descriptor〉：說明資料 buffer 如何由 PRP／SGL 結構描述。 逐一核對 address、offset、length、alignment 與下一層 pointer。

- 解決的問題：說明資料 buffer 如何由 PRP／SGL 結構描述。

- 閱讀順序：逐一核對 address、offset、length、alignment 與下一層 pointer。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：用跨兩個 memory page 的 buffer 檢查第一個 offset 與後續 alignment。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 121, 文件頁 163, PDF 頁 189

### Figure 122: SGL Last Segment descriptor

<!-- claim:BASE4-FIG-122-CLAIM figure-table:BASE4-FIG-122 -->

Figure 122〈SGL Last Segment descriptor〉：說明資料 buffer 如何由 PRP／SGL 結構描述。 逐一核對 address、offset、length、alignment 與下一層 pointer。

- 解決的問題：說明資料 buffer 如何由 PRP／SGL 結構描述。

- 閱讀順序：逐一核對 address、offset、length、alignment 與下一層 pointer。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：用跨兩個 memory page 的 buffer 檢查第一個 offset 與後續 alignment。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 122, 文件頁 164, PDF 頁 190

### Figure 125: SGL Read Example

<!-- claim:BASE4-FIG-125-CLAIM figure-table:BASE4-FIG-125 -->

Figure 125〈SGL Read Example〉：說明資料 buffer 如何由 PRP／SGL 結構描述。 逐一核對 address、offset、length、alignment 與下一層 pointer。

- 解決的問題：說明資料 buffer 如何由 PRP／SGL 結構描述。

- 閱讀順序：逐一核對 address、offset、length、alignment 與下一層 pointer。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：用跨兩個 memory page 的 buffer 檢查第一個 offset 與後續 alignment。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2.1, Figure 125, 文件頁 166, PDF 頁 192

### Figure 126: Current Value after Reset with Scope of Entire NVM Subsystem

<!-- claim:BASE4-FIG-126-CLAIM figure-table:BASE4-FIG-126 -->

Figure 126〈Current Value after Reset with Scope of Entire NVM Subsystem〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.4, Figure 126, 文件頁 167, PDF 頁 193

### Figure 127: Current Value after Reset with Scope of Subset of the NVM Subsystem

<!-- claim:BASE4-FIG-127-CLAIM figure-table:BASE4-FIG-127 -->

Figure 127〈Current Value after Reset with Scope of Subset of the NVM Subsystem〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.4, Figure 127, 文件頁 168, PDF 頁 194

### Figure 128: PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)

<!-- claim:BASE4-FIG-128-CLAIM figure-table:BASE4-FIG-128 -->

Figure 128〈PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.1, Figure 128, 文件頁 169, PDF 頁 195

### Figure 129: Serial Number (SN) and Model Number (MN)

<!-- claim:BASE4-FIG-129-CLAIM figure-table:BASE4-FIG-129 -->

Figure 129〈Serial Number (SN) and Model Number (MN)〉：整理 identifier 或 list 的 byte layout 與範圍。 先確認長度、byte order、數量欄位、唯一性範圍與保留區。

- 解決的問題：整理 identifier 或 list 的 byte layout 與範圍。

- 閱讀順序：先確認長度、byte order、數量欄位、唯一性範圍與保留區。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：parser 先驗證 count 與長度，再逐筆讀取 identifier。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.2, Figure 129, 文件頁 170, PDF 頁 196

### Figure 130: IEEE OUI Identifier (IEEE)

<!-- claim:BASE4-FIG-130-CLAIM figure-table:BASE4-FIG-130 -->

Figure 130〈IEEE OUI Identifier (IEEE)〉：整理 identifier 或 list 的 byte layout 與範圍。 先確認長度、byte order、數量欄位、唯一性範圍與保留區。

- 解決的問題：整理 identifier 或 list 的 byte layout 與範圍。

- 閱讀順序：先確認長度、byte order、數量欄位、唯一性範圍與保留區。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：parser 先驗證 count 與長度，再逐筆讀取 identifier。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.3, Figure 130, 文件頁 170, PDF 頁 196

### Figure 131: IEEE Extended Unique Identifier (EUI64), MA-L Format

<!-- claim:BASE4-FIG-131-CLAIM figure-table:BASE4-FIG-131 -->

Figure 131〈IEEE Extended Unique Identifier (EUI64), MA-L Format〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 131, 文件頁 170, PDF 頁 196

### Figure 132: IEEE Extended Unique Identifier (EUI64), OUI Identifier

<!-- claim:BASE4-FIG-132-CLAIM figure-table:BASE4-FIG-132 -->

Figure 132〈IEEE Extended Unique Identifier (EUI64), OUI Identifier〉：整理 identifier 或 list 的 byte layout 與範圍。 先確認長度、byte order、數量欄位、唯一性範圍與保留區。

- 解決的問題：整理 identifier 或 list 的 byte layout 與範圍。

- 閱讀順序：先確認長度、byte order、數量欄位、唯一性範圍與保留區。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：parser 先驗證 count 與長度，再逐筆讀取 identifier。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 132, 文件頁 170, PDF 頁 196

### Figure 133: IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)

<!-- claim:BASE4-FIG-133-CLAIM figure-table:BASE4-FIG-133 -->

Figure 133〈IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)〉：整理 identifier 或 list 的 byte layout 與範圍。 先確認長度、byte order、數量欄位、唯一性範圍與保留區。

- 解決的問題：整理 identifier 或 list 的 byte layout 與範圍。

- 閱讀順序：先確認長度、byte order、數量欄位、唯一性範圍與保留區。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：parser 先驗證 count 與長度，再逐筆讀取 identifier。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 133, 文件頁 170-171, PDF 頁 196-197

### Figure 134: MA-L similarity to WWN

<!-- claim:BASE4-FIG-134-CLAIM figure-table:BASE4-FIG-134 -->

Figure 134〈MA-L similarity to WWN〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 134, 文件頁 171, PDF 頁 197

### Figure 135: Namespace Globally Unique Identifier (NGUID)

<!-- claim:BASE4-FIG-135-CLAIM figure-table:BASE4-FIG-135 -->

Figure 135〈Namespace Globally Unique Identifier (NGUID)〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 135, 文件頁 171, PDF 頁 197

### Figure 136: Namespace Globally Unique Identifier (NGUID), OUI

<!-- claim:BASE4-FIG-136-CLAIM figure-table:BASE4-FIG-136 -->

Figure 136〈Namespace Globally Unique Identifier (NGUID), OUI〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 136, 文件頁 171, PDF 頁 197

### Figure 137: Namespace Globally Unique Identifier

<!-- claim:BASE4-FIG-137-CLAIM figure-table:BASE4-FIG-137 -->

Figure 137〈Namespace Globally Unique Identifier〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 137, 文件頁 171, PDF 頁 197

### Figure 138: Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN

<!-- claim:BASE4-FIG-138-CLAIM figure-table:BASE4-FIG-138 -->

Figure 138〈Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN〉：說明 subsystem 物件的包含、連接或容量關係。 分開辨認 controller、port、namespace、identifier 與容量階層。

- 解決的問題：說明 subsystem 物件的包含、連接或容量關係。

- 閱讀順序：分開辨認 controller、port、namespace、identifier 與容量階層。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：替單一 namespace 標出其 NSID、controller 與所屬容量階層。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 138, 文件頁 171, PDF 頁 197

### Figure 139: Controller List Format

<!-- claim:BASE4-FIG-139-CLAIM figure-table:BASE4-FIG-139 -->

Figure 139〈Controller List Format〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.6.1, Figure 139, 文件頁 172, PDF 頁 198

### Figure 140: Namespace List Format

<!-- claim:BASE4-FIG-140-CLAIM figure-table:BASE4-FIG-140 -->

Figure 140〈Namespace List Format〉：整理欄位、位元或 register 配置。 由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 解決的問題：整理欄位、位元或 register 配置。

- 閱讀順序：由 offset／byte／bit 範圍對到名稱、存取型別、reset 與條件。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：讀取前先確認 capability，再以欄位寬度與遮罩解碼。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.6.2, Figure 140, 文件頁 172, PDF 頁 198

### Figure 142: UTF-8 Input Processing

<!-- claim:BASE4-FIG-142-CLAIM figure-table:BASE4-FIG-142 -->

Figure 142〈UTF-8 Input Processing〉：提供本節概念、支援條件或範例的結構化索引。 先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 解決的問題：提供本節概念、支援條件或範例的結構化索引。

- 閱讀順序：先看標題所指物件，再對照相鄰文字的條件、圖例與例外。

- 規範語氣：本導讀不新增 shall／may／should；實際強度以同節文字與欄位描述為準。

- 說明性範例（informative example）：選一個具體 controller 設定，逐項對照圖中的關係。此例不新增規格要求。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.8, Figure 142, 文件頁 175, PDF 頁 201

## 使用與限制

製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata 集合或核准範圍改變時，必須重新核對受影響 claim。
