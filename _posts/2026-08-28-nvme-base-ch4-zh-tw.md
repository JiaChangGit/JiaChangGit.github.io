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

## 先學縮寫：完整 Glossary

下列縮寫會在投影片主線使用前先定義。縮寫本身永遠不夠；設計與 Debug 還要保留 owner、width、unit、scope 與 state。

| 縮寫／名詞 | 白話解釋 | 來源 |
|---|---|---|
| `SQE` | Submission Queue Entry，SQ 中的一筆命令資料結構。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1，文件頁 139-143，PDF 頁 165-169 |
| `CQE` | Completion Queue Entry，CQ 中的一筆完成結果資料結構。 | NVME-BASE-2.4 Rev. 2.4，§4.2.1，文件頁 144-145，PDF 頁 170-171 |
| `CDW` | Command Dword，SQE 中以 32-bit 為單位編號的命令欄位。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1，文件頁 139-143，PDF 頁 165-169 |
| `CID` | Command Identifier，與 SQ identifier 合用以辨識 outstanding command。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1，文件頁 140，PDF 頁 166 |
| `SQID` | Submission Queue Identifier，辨識 command 所屬 SQ 的數值。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1，文件頁 140，PDF 頁 166 |
| `NSID` | Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1，文件頁 139-143，PDF 頁 165-169 |
| `PSDT` | PRP or SGL for Data Transfer，CDW0 中決定 DPTR 應按 PRP 或 SGL 解讀的欄位。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1，文件頁 140-142，PDF 頁 166-168 |
| `DPTR` | Data Pointer，SQE 中指出 command data buffer 的欄位。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1，文件頁 140-142，PDF 頁 166-168 |
| `MPTR` | Metadata Pointer，SQE 中指出獨立 metadata buffer 的欄位。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1，文件頁 139-143，PDF 頁 165-169 |
| `PRP` | Physical Region Page，以 memory page 為單位描述 host-addressable data buffer 的 pointer 格式。 | NVME-BASE-2.4 Rev. 2.4，§4.3.1，文件頁 158-159，PDF 頁 184-185 |
| `SGL` | Scatter Gather List，以 descriptor 與 segment 描述一段或多段 data buffer 的格式。 | NVME-BASE-2.4 Rev. 2.4，§4.3.2，文件頁 159-166，PDF 頁 185-192 |
| `SCT` | Status Code Type，先決定 status 所屬大類，再解讀 SC。 | NVME-BASE-2.4 Rev. 2.4，§4.2.3，文件頁 145-155，PDF 頁 171-181 |
| `SC` | Status Code，在 SCT 上下文中表示具體完成結果的 code。 | NVME-BASE-2.4 Rev. 2.4，§4.2.3，文件頁 145-155，PDF 頁 171-181 |
| `DNR` | Do Not Retry，CQE status 中提示以相同 command 重試預期不會成功的 bit。 | NVME-BASE-2.4 Rev. 2.4，§4.2.3，文件頁 145-155，PDF 頁 171-181 |
| `CRD` | Command Retry Delay，status 中選擇 controller 建議重試延遲值的欄位。 | NVME-BASE-2.4 Rev. 2.4，§4.2.3，文件頁 145-155，PDF 頁 171-181 |
| `P` | Phase Tag，讓 host 判斷 CQ slot 是否包含新 completion 的翻轉 bit。 | NVME-BASE-2.4 Rev. 2.4，§4.2.4，文件頁 155-158，PDF 頁 181-184 |
| `PBAO` | Page Base Address and Offset，第一個 PRP entry 中同時包含 page base 與 page 內 offset 的配置。 | NVME-BASE-2.4 Rev. 2.4，§4.3.1，文件頁 158-159，PDF 頁 184-185 |
| `VID` | Vendor ID，由 PCI-SIG 配置、辨識 vendor 的 identifier。 | NVME-BASE-2.4 Rev. 2.4，§4.5，文件頁 169-172，PDF 頁 195-198 |
| `SSVID` | Subsystem Vendor ID，辨識 subsystem vendor 的 PCI identifier。 | NVME-BASE-2.4 Rev. 2.4，§4.5，文件頁 169-172，PDF 頁 195-198 |
| `SN` | Serial Number，辨識一個產品實例的序號字串。 | NVME-BASE-2.4 Rev. 2.4，§4.5，文件頁 169-172，PDF 頁 195-198 |
| `MN` | Model Number，辨識產品型號的字串。 | NVME-BASE-2.4 Rev. 2.4，§4.5，文件頁 169-172，PDF 頁 195-198 |
| `OUI` | Organizationally Unique Identifier，由 IEEE 配置給組織的 identifier 前綴。 | NVME-BASE-2.4 Rev. 2.4，§4.5，文件頁 169-172，PDF 頁 195-198 |
| `EUI64` | 64-bit Extended Unique Identifier，使用 IEEE 配置空間建立的 64-bit identifier。 | NVME-BASE-2.4 Rev. 2.4，§4.5，文件頁 169-172，PDF 頁 195-198 |
| `NGUID` | Namespace Globally Unique Identifier，namespace 的 128-bit 全域識別值。 | NVME-BASE-2.4 Rev. 2.4，§4.5，文件頁 169-172，PDF 頁 195-198 |
| `UUID` | Universally Unique Identifier，128-bit identifier；其實際關聯範圍仍由使用它的資料結構決定。 | NVME-BASE-2.4 Rev. 2.4，§4.5，文件頁 169-172，PDF 頁 195-198 |
| `NAA` | Network Address Authority，WWN 中選擇 identifier 格式與配置方式的 nibble。 | NVME-BASE-2.4 Rev. 2.4，§4.5，文件頁 169-172，PDF 頁 195-198 |
| `WWN` | World Wide Name，用於儲存與網路裝置識別的全域名稱格式。 | NVME-BASE-2.4 Rev. 2.4，§4.5，文件頁 169-172，PDF 頁 195-198 |
| `UTF-8` | Unicode Transformation Format - 8-bit，以一到四個 bytes 編碼 Unicode code point 的文字格式。 | NVME-BASE-2.4 Rev. 2.4，§4.8，文件頁 175，PDF 頁 201 |

## Visual Atlas：先用圖建立整體位置

每張教學重畫回答不同問題：Architecture 定位元件、Sequence 顯示 ownership、Decode 把 bits 轉成工程值、State 保留 failure evidence；它們不是 Spec 原圖的複製。

### Visual 01: 先固定 64-byte SQE 骨架，再套 command-specific 欄位

**View type:** `decode`

```text
[RAW: 清空 64-byte SQE] → [LOCATE: 填 CDW0：OPC/CID/PSDT] → [DECODE: 依 command 填 NSID] → [VALIDATE: 建立 MPTR/DPTR]
VALIDATE fail ──→ return to RAW evidence
```

**回答的問題：** Common SQE 先固定 CDW0、NSID、metadata/data pointer 與 CDW10-15 的位置。OPC 選 command，CID 建立完成關聯，PSDT 決定 DPTR 解讀方式；只有完成這些 common 欄位後，才應進入個別 command 的 CDW10-15 定義。Figures 92-94 是後續所有 command construction 的座標系。

**支援 Figure：** Figure 92, Figure 93, Figure 94

**來源：** NVME-BASE-2.4 Rev. 2.4，§4.1.1，文件頁 139-143，PDF 頁 165-169; NVME-BASE-2.4 Rev. 2.4，§4.1.1，文件頁 140，PDF 頁 166; NVME-BASE-2.4 Rev. 2.4，§4.1.1，文件頁 140-142，PDF 頁 166-168

### Visual 02: CQE 先解 ownership，再解 identity，最後解 status

**View type:** `decode`

```text
[RAW: 檢查 Phase Tag] → [LOCATE: 讀 SQHD/SQID/CID] → [DECODE: 用 SQID/CID 找 command] → [VALIDATE: 解 SCT]
VALIDATE fail ──→ return to RAW evidence
```

**回答的問題：** host 先用 Phase Tag 判斷 CQ slot 是否是新 completion；確定 ownership 後再用 SQID/CID 找回 command，最後以 SCT 選 status 類別並解 SC、DNR、CRD。Figures 97-109 必須按這個順序讀，否則 stale CQE 或錯誤類別會被當成真實 command failure。

**支援 Figure：** Figure 97, Figure 98, Figure 99, Figure 101, Figure 102, Figure 103, Figure 104, Figure 105, Figure 107, Figure 108, Figure 109

**來源：** NVME-BASE-2.4 Rev. 2.4，§4.2.1，文件頁 144-145，PDF 頁 170-171; NVME-BASE-2.4 Rev. 2.4，§4.2.3，文件頁 145-155，PDF 頁 171-181; NVME-BASE-2.4 Rev. 2.4，§4.2.4，文件頁 155-158，PDF 頁 181-184

### Visual 03: PRP 計算：第一頁可有 offset，後續 entry 回到 page boundary

**View type:** `decode`

```text
[RAW: 取得 MPS/page size] → [LOCATE: 算 PRP1 page offset] → [DECODE: 算第一頁可用 bytes] → [VALIDATE: 算 remaining bytes]
VALIDATE fail ──→ return to RAW evidence
```

**回答的問題：** PRP1 可以指向第一個 memory page 內任意 byte，能承載的第一段長度是 page_size - offset。若資料跨過第一頁，PRP2 依剩餘長度代表第二頁或 PRP List；後續 page address 必須符合 page alignment。Figures 110-113 是 address calculation，不只是 pointer 名稱表。

**支援 Figure：** Figure 110, Figure 111, Figure 112, Figure 113

**來源：** NVME-BASE-2.4 Rev. 2.4，§4.3.1，文件頁 158-159，PDF 頁 184-185; NVME-BASE-2.4 Rev. 2.4，§4.1.1，文件頁 140-142，PDF 頁 166-168

### Visual 04: SGL 是 typed descriptor chain，不是另一種 PRP List

**View type:** `decode`

```text
[RAW: 由 PSDT 選 SGL] → [LOCATE: 讀 descriptor type/subtype] → [DECODE: 驗證 length] → [VALIDATE: 若為 data：加入 interval]
VALIDATE fail ──→ return to RAW evidence
```

**回答的問題：** SGL descriptor 同時包含 type/subtype、address 與 length；Data Block 指向資料，Segment／Last Segment 指向更多 descriptors，Bit Bucket 表示資料不需實際放入 memory。Figures 114-125 應先讀 type，再讀該 type 對 address/length 的語意，不能只沿 address 盲走。

**支援 Figure：** Figure 114, Figure 115, Figure 116, Figure 117, Figure 118, Figure 119, Figure 120, Figure 121, Figure 122, Figure 125

**來源：** NVME-BASE-2.4 Rev. 2.4，§4.3.2，文件頁 159-166，PDF 頁 185-192; NVME-BASE-2.4 Rev. 2.4，§4.1.1，文件頁 140-142，PDF 頁 166-168

### Visual 05: Feature、identifier、list 與 UTF-8 都需要先驗證 scope

**View type:** `decode`

```text
[RAW: 辨識資料種類] → [LOCATE: 取得 width/count] → [DECODE: 確認 authority/scope] → [VALIDATE: 驗證 reserved/padding]
VALIDATE fail ──→ return to RAW evidence
```

**回答的問題：** Feature 的 current/default/saved value 是時間與 persistence scope；VID、SN、EUI64、NGUID、UUID 是 identity scope；Controller/Namespace List 是 count 與 array boundary；UTF-8 是 byte sequence 與 code-point boundary。Figures 126-142 表面分散，實際都在教 parser 不可脫離 scope。

**支援 Figure：** Figure 126, Figure 127, Figure 128, Figure 129, Figure 130, Figure 131, Figure 132, Figure 133, Figure 134, Figure 135, Figure 136, Figure 137, Figure 138, Figure 139, Figure 140, Figure 142

**來源：** NVME-BASE-2.4 Rev. 2.4，§4.4，文件頁 166-169，PDF 頁 192-195; NVME-BASE-2.4 Rev. 2.4，§4.5，文件頁 169-172，PDF 頁 195-198; NVME-BASE-2.4 Rev. 2.4，§4.6，文件頁 172-173，PDF 頁 198-199; NVME-BASE-2.4 Rev. 2.4，§4.8，文件頁 175，PDF 頁 201

## Mental Model 與完整教學流程

以下依工程因果而非 Spec section 排列；相關 Figure 會回到它支援的流程節點，不以編號順序取代教學故事線。

### Module 01: 先固定 64-byte SQE 骨架，再套 command-specific 欄位

**解釋。** Common SQE 先固定 CDW0、NSID、metadata/data pointer 與 CDW10-15 的位置。OPC 選 command，CID 建立完成關聯，PSDT 決定 DPTR 解讀方式；只有完成這些 common 欄位後，才應進入個別 command 的 CDW10-15 定義。Figures 92-94 是後續所有 command construction 的座標系。

```text
清空 64-byte SQE
  ↓
填 CDW0：OPC/CID/PSDT
  ↓
依 command 填 NSID
  ↓
建立 MPTR/DPTR
  ↓
填 CDW10-15
  ↓
最後提交
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| CDW0 | command identity 與 data-pointer selector | 所有 commands 共用 |
| NSID | namespace scope | 不用時必須依 command 定義清零或使用特殊值 |
| MPTR/DPTR | metadata 與 data buffer | 由 PSDT 與 command 規則決定 |
| CDW10-15 | command-specific payload | 不能跨 command 借用語意 |

**說明性範例。** 說明性範例：同一個 CID 可以在不同 SQ 使用，但同一 SQ 內 outstanding command 不可用相同 CID 造成識別衝突。driver 建 SQE 時以 (SQID,CID) 建 tracking key，填完全部欄位並完成必要 memory ordering 後才更新 SQ tail。

**常見誤解／Debug。** 保留 raw 64 bytes 的 SQE dump，並同時印出 decode 後欄位。只保存高階 command object，無法查出 bit shift、endianness、未清 reserved bits 或錯誤 PSDT。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§4.1.1，文件頁 139-143，PDF 頁 165-169; NVME-BASE-2.4 Rev. 2.4，§4.1.1，文件頁 140，PDF 頁 166; NVME-BASE-2.4 Rev. 2.4，§4.1.1，文件頁 140-142，PDF 頁 166-168

**關聯 Figure：** Figure 92, Figure 93, Figure 94

### Module 02: CQE 先解 ownership，再解 identity，最後解 status

**解釋。** host 先用 Phase Tag 判斷 CQ slot 是否是新 completion；確定 ownership 後再用 SQID/CID 找回 command，最後以 SCT 選 status 類別並解 SC、DNR、CRD。Figures 97-109 必須按這個順序讀，否則 stale CQE 或錯誤類別會被當成真實 command failure。

```text
檢查 Phase Tag
  ↓
讀 SQHD/SQID/CID
  ↓
用 SQID/CID 找 command
  ↓
解 SCT
  ↓
解 SC/DNR/CRD
  ↓
推進 CQ head
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| SCT | status 大類 | 一定先解 |
| SC | 類別內具體結果 | 不能脫離 SCT |
| DNR | 同 command 重試預期 | 不是永久硬體故障的同義詞 |
| CRD | 建議 retry delay selector | 只有適用 status 才使用 |

**說明性範例。** 說明性範例：SC 數值 02h 在不同 SCT 下可能屬於不同 status 表。正確 log 應保存完整 status field，再輸出 P、SCT、SC、DNR、CRD 與原始 16-bit value。只印『SC=2』不足以決定 recovery。

**常見誤解／Debug。** CQ wrap bug 常表現成重複完成或 command 永不完成。核對 producer/consumer 預期 phase、CQ head doorbell 與每個 slot 的 raw DW3；不要在驗證 Phase Tag 前讀取其他 CQE 欄位作決策。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§4.2.1，文件頁 144-145，PDF 頁 170-171; NVME-BASE-2.4 Rev. 2.4，§4.2.3，文件頁 145-155，PDF 頁 171-181; NVME-BASE-2.4 Rev. 2.4，§4.2.4，文件頁 155-158，PDF 頁 181-184

**關聯 Figure：** Figure 97, Figure 98, Figure 99, Figure 101, Figure 102, Figure 103, Figure 104, Figure 105, Figure 107, Figure 108, Figure 109

### Module 03: PRP 計算：第一頁可有 offset，後續 entry 回到 page boundary

**解釋。** PRP1 可以指向第一個 memory page 內任意 byte，能承載的第一段長度是 page_size - offset。若資料跨過第一頁，PRP2 依剩餘長度代表第二頁或 PRP List；後續 page address 必須符合 page alignment。Figures 110-113 是 address calculation，不只是 pointer 名稱表。

```text
取得 MPS/page size
  ↓
算 PRP1 page offset
  ↓
算第一頁可用 bytes
  ↓
算 remaining bytes
  ↓
決定 PRP2=page 或 list
  ↓
驗證後續 page alignment
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| 資料不跨第一頁 | 只需 PRP1 | PRP2 不承載下一段 |
| 剩餘資料只需一頁 | PRP2 指第二個 data page | address page-aligned |
| 剩餘資料超過一頁 | PRP2 指 PRP List | list entries 再指 data pages |

**說明性範例。** 說明性範例：page size 4096 bytes，PRP1 offset 1000，transfer 9000 bytes。第一頁可放 4096-1000=3096 bytes，剩 5904 bytes，需要兩個後續 pages；因此 PRP2 應指向至少含兩個 data-page addresses 的 PRP List。

**常見誤解／Debug。** PRP debug dump 要包含 MPS、transfer length、PRP1 offset、每個 entry 的 physical address 與涵蓋 byte interval。只檢查 address 非零，抓不到 list/page 誤判、少一頁或把 virtual address 當 physical address。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§4.3.1，文件頁 158-159，PDF 頁 184-185; NVME-BASE-2.4 Rev. 2.4，§4.1.1，文件頁 140-142，PDF 頁 166-168

**關聯 Figure：** Figure 110, Figure 111, Figure 112, Figure 113

### Module 04: SGL 是 typed descriptor chain，不是另一種 PRP List

**解釋。** SGL descriptor 同時包含 type/subtype、address 與 length；Data Block 指向資料，Segment／Last Segment 指向更多 descriptors，Bit Bucket 表示資料不需實際放入 memory。Figures 114-125 應先讀 type，再讀該 type 對 address/length 的語意，不能只沿 address 盲走。

```text
由 PSDT 選 SGL
  ↓
讀 descriptor type/subtype
  ↓
驗證 length
  ↓
若為 data：加入 interval
  ↓
若為 segment：走訪 descriptors
  ↓
遇 Last Segment 結束
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| PRP | page-based addresses | 第一頁 offset + 後續 page alignment |
| SGL Data Block | address + byte length | 資料區段可用 descriptor 表示 |
| SGL Segment | address + descriptor-list length | 指向下一層 descriptors，不是 data |
| Bit Bucket | 只消耗 transfer length | 不代表可讀寫的 memory buffer |

**說明性範例。** 說明性範例：requested transfer 為 12 KiB，兩個 Data Block descriptors 分別描述 8 KiB 與 4 KiB，總 length 正好覆蓋 request。若第一個 descriptor 實際是 Segment，8 KiB 便是 descriptor list 長度而非 data 長度，parser 的累加結果會完全錯誤。

**常見誤解／Debug。** SGL validator 應同時限制 nesting、descriptor count、總 byte length、overflow 與 loop。每走一步先記 type/subtype，再決定 address 指向 data 或另一串 descriptors；順序顛倒會造成越界或循環。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§4.3.2，文件頁 159-166，PDF 頁 185-192; NVME-BASE-2.4 Rev. 2.4，§4.1.1，文件頁 140-142，PDF 頁 166-168

**關聯 Figure：** Figure 114, Figure 115, Figure 116, Figure 117, Figure 118, Figure 119, Figure 120, Figure 121, Figure 122, Figure 125

### Module 05: Feature、identifier、list 與 UTF-8 都需要先驗證 scope

**解釋。** Feature 的 current/default/saved value 是時間與 persistence scope；VID、SN、EUI64、NGUID、UUID 是 identity scope；Controller/Namespace List 是 count 與 array boundary；UTF-8 是 byte sequence 與 code-point boundary。Figures 126-142 表面分散，實際都在教 parser 不可脫離 scope。

```text
辨識資料種類
  ↓
取得 width/count
  ↓
確認 authority/scope
  ↓
驗證 reserved/padding
  ↓
建立穩定 comparison key
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| VID/SSVID | vendor/subsystem vendor | 配置 authority 不同 |
| SN/MN | 產品 instance/model 字串 | 需依固定欄位與 padding 解讀 |
| EUI64/NGUID/UUID | 不同格式與 uniqueness scope | 不可只因長度相近互換 |
| List | count + identifiers | 先驗證 count 再走訪 |

**說明性範例。** 說明性範例：Namespace List 的 count 宣稱有 5 個 IDs，但實際 buffer 只含 3 個完整 entries。安全 parser 以 buffer length 與格式上限先拒絕，不應因 count 欄位看似合法就讀取第四個 entry。UTF-8 固定欄位也同理：截斷在多-byte character 中間時不能接受半個字元。

**常見誤解／Debug。** identity database 同時保存 value、type、width、source object 與 scope。只存十六進位字串會讓 EUI64、NGUID、UUID 或不同 controller 下的 identifier 發生假相等。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§4.4，文件頁 166-169，PDF 頁 192-195; NVME-BASE-2.4 Rev. 2.4，§4.5，文件頁 169-172，PDF 頁 195-198; NVME-BASE-2.4 Rev. 2.4，§4.6，文件頁 172-173，PDF 頁 198-199; NVME-BASE-2.4 Rev. 2.4，§4.8，文件頁 175，PDF 頁 201

**關聯 Figure：** Figure 126, Figure 127, Figure 128, Figure 129, Figure 130, Figure 131, Figure 132, Figure 133, Figure 134, Figure 135, Figure 136, Figure 137, Figure 138, Figure 139, Figure 140, Figure 142

## 可追溯的規格重點

前面的 Mental Model 解釋因果；本節保留每個可追溯結論與 normative 強度，供講者備註與審查。

### 1. common SQE 配置

<!-- claim:BASE4-SQE -->

Admin 與 I/O common SQE 固定為 64 bytes。CDW0、NSID、data pointer 與 CDW10-15 的通用位置先固定，再由各 command 定義命令專屬內容。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 文件頁 139-143, PDF 頁 165-169

### 2. CID 唯一性

<!-- claim:BASE4-CID -->

CID 與 Submission Queue identifier 的組合用來唯一識別 command；FFFFh 宜（should）避免使用，因 Error Information log 以該值表示錯誤未對應特定 command。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 文件頁 140, PDF 頁 166

### 3. PRP／SGL 選擇

<!-- claim:BASE4-PSDT -->

CDW0.PSDT 決定 DPTR 解讀為 PRP 或 SGL。NVMe over PCIe 的 Admin command 原則上必須（shall）使用 PRP，除非 command 定義另有規定。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 文件頁 140-142, PDF 頁 166-168

### 4. common CQE 與 Phase Tag

<!-- claim:BASE4-CQE -->

common CQE 至少 16 bytes；若以多次寫入建立 CQE，Phase Tag 必須（shall）在最後一次寫入更新，避免 host 看到半成品。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, 文件頁 144-145, PDF 頁 170-171

### 5. SCT、SC 與 DNR

<!-- claim:BASE4-STATUS -->

status 要先解 Status Code Type（SCT），再解 Status Code（SC），同時檢查 Do Not Retry（DNR）等控制 bit；數值不能脫離 SCT 單獨解讀。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, 文件頁 145-155, PDF 頁 171-181

### 6. Completion Queue phase

<!-- claim:BASE4-PHASE -->

Phase Tag 讓 host 判斷環形 Completion Queue slot 是否為新完成項目；host 消費 CQE 後推進 CQ head doorbell，wrap 時預期 phase 翻轉。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.4, 文件頁 155-158, PDF 頁 181-184

### 7. PRP alignment 與 page

<!-- claim:BASE4-PRP -->

PRP 以固定大小 entry 指向 physical memory page。第一個 entry 可含 page offset；後續 PRP 必須（shall）符合 page alignment，資料長度決定需要幾個 entry。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, 文件頁 158-159, PDF 頁 184-185

### 8. SGL descriptor 與 length

<!-- claim:BASE4-SGL -->

SGL 由一個以上 descriptor／segment 描述資料 buffer。SGL length 必須（shall）大於等於 requested transfer length；本報告只介紹 PCIe 可用的通用 descriptor。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, 文件頁 159-166, PDF 頁 185-192

### 9. Feature value 與 persistence

<!-- claim:BASE4-FEATURE -->

Feature 可能具有 default、saved、current value；saved value 支援與跨 reset／power cycle 的 persistence 由 SSFS 與各 Feature capability 判定。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.4, 文件頁 166-169, PDF 頁 192-195

### 10. 全域識別碼的範圍

<!-- claim:BASE4-IDENTIFIER -->

VID／SSVID、SN／MN、IEEE OUI、EUI64、NGUID 與 UUID 的來源、長度與唯一性範圍不同；不能只因外觀相似就互換。此節為 informative。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5, 文件頁 169-172, PDF 頁 195-198

### 11. Controller／Namespace List

<!-- claim:BASE4-LISTS -->

Controller List 與 Namespace List 都先給出數量，再排列 identifier；實作 parser 時，先依格式定義的上限與保留區驗證輸入。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.6, 文件頁 172-173, PDF 頁 198-199

### 12. UTF-8 輸入驗證

<!-- claim:BASE4-UTF8 -->

處理 UTF-8 輸入時要依規格流程驗證編碼、禁止的 code point 與截斷情況；不可把任意 byte sequence 當成有效字串。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

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

## Figure／欄位表教學參考

本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。欄位與 keyword 索引來自本機核對過的 PDF。

<a id="section-4-1"></a>

### §4.1

<details markdown="1">
<summary><strong>Figure 92: Command Dword 0</strong></summary>

<!-- claim:BASE4-FIG-092-CLAIM figure-table:BASE4-FIG-092 -->

**SPEC。** Figure 92〈Command Dword 0〉：定義〈Command Dword 0〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CID, PSDT, FUSE, OPC, FN, DTD, PRP, SGL。

#### 這張 Figure 在完整流程中的位置

Figure 92 位於 §4.1.1，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CID]
          ↓
[擷取欄位: PSDT] → [套用編碼: FUSE]
                                      ↓
[驗證證據: OPC]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CID` | Command Identifier，與 SQ identifier 合用以辨識 outstanding command。 |
| `PSDT` | PRP or SGL for Data Transfer，CDW0 中決定 DPTR 應按 PRP 或 SGL 解讀的欄位。 |
| `FUSE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `OPC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FN` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `DTD` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.1.1。
2. 依圖中指定的寬度與位置解碼 CID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 PSDT 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 92 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.1.1 如何排列 CID、PSDT 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.1.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 92 對應的 raw value 或 buffer，標出包含 CID 的 bytes 並解碼，再獨立核對 PSDT。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CID，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CID 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 PSDT 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CID, PSDT, FUSE, OPC, FN, DTD, PRP, SGL

**來源 keyword 索引：** `shall not`, `should not`, `shall`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 92, 文件頁 139-140, PDF 頁 165-166

</details>

<details markdown="1">
<summary><strong>Figure 93: Common Command Format</strong></summary>

<!-- claim:BASE4-FIG-093-CLAIM figure-table:BASE4-FIG-093 -->

**SPEC。** Figure 93〈Common Command Format〉：定義〈Common Command Format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CDW0, NSID, CDW2, CDW3, MPTR, DPTR, PRP2, PRP1。

#### 這張 Figure 在完整流程中的位置

Figure 93 位於 §4.1.1，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CDW0 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CDW0]
          ↓
[擷取欄位: NSID] → [套用編碼: CDW2]
                                      ↓
[驗證證據: CDW3]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CDW0` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NSID` | Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。 |
| `CDW2` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CDW3` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MPTR` | Metadata Pointer，SQE 中指出獨立 metadata buffer 的欄位。 |
| `DPTR` | Data Pointer，SQE 中指出 command data buffer 的欄位。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.1.1。
2. 依圖中指定的寬度與位置解碼 CDW0；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NSID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 93 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.1.1 如何排列 CDW0、NSID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.1.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 93 對應的 raw value 或 buffer，標出包含 CDW0 的 bytes 並解碼，再獨立核對 NSID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CDW0，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CDW0 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NSID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CDW0, NSID, CDW2, CDW3, MPTR, DPTR, PRP2, PRP1

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, 文件頁 140-142, PDF 頁 166-168

</details>

<details markdown="1">
<summary><strong>Figure 94: Common Command Format - Vendor Specific Commands (Optional)</strong></summary>

<!-- claim:BASE4-FIG-094-CLAIM figure-table:BASE4-FIG-094 -->

**SPEC。** Figure 94〈Common Command Format - Vendor Specific Commands (Optional)〉：定義〈Common Command Format - Vendor Specific Commands (Optional)〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CDW0, NSID, MDPTR, NDT, NDM, CDW12, CDW13, CDW14。

#### 這張 Figure 在完整流程中的位置

Figure 94 位於 §4.1.1，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CDW0 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CDW0]
          ↓
[擷取欄位: NSID] → [套用編碼: MDPTR]
                                      ↓
[驗證證據: NDT]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CDW0` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NSID` | Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。 |
| `MDPTR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NDT` | Number of Dwords in Data Transfer，standard vendor-specific format 中的實際 data dword 數。 |
| `NDM` | Number of Dwords in Metadata Transfer，standard vendor-specific format 中的實際 metadata dword 數。 |
| `CDW12` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.1.1。
2. 依圖中指定的寬度與位置解碼 CDW0；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NSID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 94 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.1.1 如何排列 CDW0、NSID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.1.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 94 對應的 raw value 或 buffer，標出包含 CDW0 的 bytes 並解碼，再獨立核對 NSID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CDW0，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CDW0 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NSID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CDW0, NSID, MDPTR, NDT, NDM, CDW12, CDW13, CDW14

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 94, 文件頁 143, PDF 頁 169

</details>

<a id="section-4-2"></a>

### §4.2

<details markdown="1">
<summary><strong>Figure 97: Common Completion Queue Entry Layout - Admin and All I/O Command Sets</strong></summary>

<!-- claim:BASE4-FIG-097-CLAIM figure-table:BASE4-FIG-097 -->

**SPEC。** Figure 97〈Common Completion Queue Entry Layout - Admin and All I/O Command Sets〉：定義〈Common Completion Queue Entry Layout - Admin and All I/O Command Sets〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DW0, DW1, DW2, SQ, DW3, Command Set, Completion Queue, Command。

#### 這張 Figure 在完整流程中的位置

Figure 97 位於 §4.2.1，在本流程中是「queue」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DW0 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 queue／command flow 圖。先標 host 與 controller 的 ownership，再追 head、tail、phase 或 arbitration 的改變；箭頭代表狀態或 ownership 轉移，不自動代表 command 已完成。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DW0]
          ↓
[擷取欄位: DW1] → [套用編碼: DW2]
                                      ↓
[驗證證據: SQ]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DW0` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `DW1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `DW2` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SQ` | Submission Queue，主機放入命令的提交佇列。 |
| `DW3` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Command Set` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.2.1。
2. 依圖中指定的寬度與位置解碼 DW0；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 DW1 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 97 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.2.1 如何排列 DW0、DW1 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.2.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 97 對應的 raw value 或 buffer，標出包含 DW0 的 bytes 並解碼，再獨立核對 DW1。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 DW0，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 DW0 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 DW1 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** DW0, DW1, DW2, SQ, DW3, Command Set, Completion Queue, Command

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 97, 文件頁 144, PDF 頁 170

</details>

<details markdown="1">
<summary><strong>Figure 98: Completion Queue Entry: DW 2</strong></summary>

<!-- claim:BASE4-FIG-098-CLAIM figure-table:BASE4-FIG-098 -->

**SPEC。** Figure 98〈Completion Queue Entry: DW 2〉：呈現〈Completion Queue Entry: DW 2〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：SQID, SQHD, DW, SQ, CID, Completion Queue。

#### 這張 Figure 在完整流程中的位置

Figure 98 位於 §4.2.1，在本流程中是「queue」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SQID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 queue／command flow 圖。先標 host 與 controller 的 ownership，再追 head、tail、phase 或 arbitration 的改變；箭頭代表狀態或 ownership 轉移，不自動代表 command 已完成。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SQID]
          ↓
[擷取欄位: SQHD] → [套用編碼: DW]
                                      ↓
[驗證證據: SQ]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SQID` | Submission Queue Identifier，辨識 command 所屬 SQ 的數值。 |
| `SQHD` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `DW` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SQ` | Submission Queue，主機放入命令的提交佇列。 |
| `CID` | Command Identifier，與 SQ identifier 合用以辨識 outstanding command。 |
| `Completion Queue` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.2.1。
2. 依圖中指定的寬度與位置解碼 SQID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 SQHD 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 98 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.2.1 如何排列 SQID、SQHD 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.2.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 98 對應的 raw value 或 buffer，標出包含 SQID 的 bytes 並解碼，再獨立核對 SQHD。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SQID，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SQID 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 SQHD 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SQID, SQHD, DW, SQ, CID, Completion Queue

**來源 keyword 索引：** `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 98, 文件頁 144, PDF 頁 170

</details>

<details markdown="1">
<summary><strong>Figure 99: Completion Queue Entry: DW 3</strong></summary>

<!-- claim:BASE4-FIG-099-CLAIM figure-table:BASE4-FIG-099 -->

**SPEC。** Figure 99〈Completion Queue Entry: DW 3〉：呈現〈Completion Queue Entry: DW 3〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：STATUS, CID, DW, SQ, Completion Queue。

#### 這張 Figure 在完整流程中的位置

Figure 99 位於 §4.2.1，在本流程中是「queue」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 STATUS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 queue／command flow 圖。先標 host 與 controller 的 ownership，再追 head、tail、phase 或 arbitration 的改變；箭頭代表狀態或 ownership 轉移，不自動代表 command 已完成。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: STATUS]
          ↓
[擷取欄位: CID] → [套用編碼: DW]
                                      ↓
[驗證證據: SQ]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `STATUS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CID` | Command Identifier，與 SQ identifier 合用以辨識 outstanding command。 |
| `DW` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SQ` | Submission Queue，主機放入命令的提交佇列。 |
| `Completion Queue` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.2.1。
2. 依圖中指定的寬度與位置解碼 STATUS；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 99 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.2.1 如何排列 STATUS、CID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.2.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 99 對應的 raw value 或 buffer，標出包含 STATUS 的 bytes 並解碼，再獨立核對 CID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 STATUS，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 STATUS 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** STATUS, CID, DW, SQ, Completion Queue

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 99, 文件頁 145, PDF 頁 171

</details>

<details markdown="1">
<summary><strong>Figure 101: Completion Queue Entry: Status Field</strong></summary>

<!-- claim:BASE4-FIG-101-CLAIM figure-table:BASE4-FIG-101 -->

**SPEC。** Figure 101〈Completion Queue Entry: Status Field〉：定義〈Completion Queue Entry: Status Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DNR, CRD, SCT, SC, ACRE, CRDT1, CRDT2, CRDT3。

#### 這張 Figure 在完整流程中的位置

Figure 101 位於 §4.2.3，在本流程中是「queue」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DNR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 queue／command flow 圖。先標 host 與 controller 的 ownership，再追 head、tail、phase 或 arbitration 的改變；箭頭代表狀態或 ownership 轉移，不自動代表 command 已完成。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DNR]
          ↓
[擷取欄位: CRD] → [套用編碼: SCT]
                                      ↓
[驗證證據: SC]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DNR` | Do Not Retry，CQE status 中提示以相同 command 重試預期不會成功的 bit。 |
| `CRD` | Command Retry Delay，status 中選擇 controller 建議重試延遲值的欄位。 |
| `SCT` | Status Code Type，先決定 status 所屬大類，再解讀 SC。 |
| `SC` | Status Code，在 SCT 上下文中表示具體完成結果的 code。 |
| `ACRE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CRDT1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.2.3。
2. 依圖中指定的寬度與位置解碼 DNR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CRD 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 101 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.2.3 如何排列 DNR、CRD 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.2.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 101 對應的 raw value 或 buffer，標出包含 DNR 的 bytes 並解碼，再獨立核對 CRD。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 DNR，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 DNR 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CRD 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** DNR, CRD, SCT, SC, ACRE, CRDT1, CRDT2, CRDT3

**來源 keyword 索引：** `should not`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 101, 文件頁 145-146, PDF 頁 171-172

</details>

<details markdown="1">
<summary><strong>Figure 102: Status Code - Status Code Type Values</strong></summary>

<!-- claim:BASE4-FIG-102-CLAIM figure-table:BASE4-FIG-102 -->

**SPEC。** Figure 102〈Status Code - Status Code Type Values〉：定義〈Status Code - Status Code Type Values〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：SC, Status Code。

#### 這張 Figure 在完整流程中的位置

Figure 102 位於 §4.2.3，在本流程中是「status」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SC 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 status／error 分類表。先確定 status 所在資料結構與類別，再解 individual code、控制 bit 與 retry 指示。Reserved value 維持未定義；不要因名稱相似便映射到另一層 error code。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SC]
          ↓
[擷取欄位: Status Code] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SC` | Status Code，在 SCT 上下文中表示具體完成結果的 code。 |
| `Status Code` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.2.3。
2. 依圖中指定的寬度與位置解碼 SC；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Status Code 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 102 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.2.3 如何排列 SC、Status Code 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.2.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 102 對應的 raw value 或 buffer，標出包含 SC 的 bytes 並解碼，再獨立核對 Status Code。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SC，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SC 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Status Code 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SC, Status Code

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 102, 文件頁 146, PDF 頁 172

</details>

<details markdown="1">
<summary><strong>Figure 103: Status Code - Generic Command Status Values</strong></summary>

<!-- claim:BASE4-FIG-103-CLAIM figure-table:BASE4-FIG-103 -->

**SPEC。** Figure 103〈Status Code - Generic Command Status Values〉：定義〈Status Code - Generic Command Status Values〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：ID, SQ, TCG, SGL, PRP, ZNS, RACQA, CMB。

#### 這張 Figure 在完整流程中的位置

Figure 103 位於 §4.2.3，在本流程中是「status」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 status／error 分類表。先確定 status 所在資料結構與類別，再解 individual code、控制 bit 與 retry 指示。Reserved value 維持未定義；不要因名稱相似便映射到另一層 error code。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ID]
          ↓
[擷取欄位: SQ] → [套用編碼: TCG]
                                      ↓
[驗證證據: SGL]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SQ` | Submission Queue，主機放入命令的提交佇列。 |
| `TCG` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGL` | Scatter Gather List，以 descriptor 與 segment 描述一段或多段 data buffer 的格式。 |
| `PRP` | Physical Region Page，以 memory page 為單位描述 host-addressable data buffer 的 pointer 格式。 |
| `ZNS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.2.3。
2. 依圖中指定的寬度與位置解碼 ID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 SQ 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 103 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.2.3 如何排列 ID、SQ 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.2.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 103 對應的 raw value 或 buffer，標出包含 ID 的 bytes 並解碼，再獨立核對 SQ。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 ID，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 ID 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 SQ 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ID, SQ, TCG, SGL, PRP, ZNS, RACQA, CMB

**來源 keyword 索引：** `shall not`, `shall`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 103, 文件頁 147-150, PDF 頁 173-176

</details>

<details markdown="1">
<summary><strong>Figure 104: Status Code - Command Specific Status Values</strong></summary>

<!-- claim:BASE4-FIG-104-CLAIM figure-table:BASE4-FIG-104 -->

**SPEC。** Figure 104〈Status Code - Command Specific Status Values〉：定義〈Status Code - Command Specific Status Values〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：ANA, NOTE, Status Code, Command。

#### 這張 Figure 在完整流程中的位置

Figure 104 位於 §4.2.3.2，在本流程中是「status」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ANA 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 status／error 分類表。先確定 status 所在資料結構與類別，再解 individual code、控制 bit 與 retry 指示。Reserved value 維持未定義；不要因名稱相似便映射到另一層 error code。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ANA]
          ↓
[擷取欄位: NOTE] → [套用編碼: Status Code]
                                      ↓
[驗證證據: Command]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ANA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NOTE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Status Code` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Command` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.2.3.2。
2. 依圖中指定的寬度與位置解碼 ANA；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NOTE 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 104 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.2.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.2.3.2 如何排列 ANA、NOTE 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.2.3.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 104 對應的 raw value 或 buffer，標出包含 ANA 的 bytes 並解碼，再獨立核對 NOTE。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 ANA，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 ANA 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NOTE 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ANA, NOTE, Status Code, Command

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 104, 文件頁 151-152, PDF 頁 177-178

</details>

<details markdown="1">
<summary><strong>Figure 105: Status Code - Command Specific Status Values, I/O Command Set Specific</strong></summary>

<!-- claim:BASE4-FIG-105-CLAIM figure-table:BASE4-FIG-105 -->

**SPEC。** Figure 105〈Status Code - Command Specific Status Values, I/O Command Set Specific〉：定義〈Status Code - Command Specific Status Values, I/O Command Set Specific〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：ID, Command Set, Status Code, Command。

#### 這張 Figure 在完整流程中的位置

Figure 105 位於 §4.2.3.2，在本流程中是「status」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 status／error 分類表。先確定 status 所在資料結構與類別，再解 individual code、控制 bit 與 retry 指示。Reserved value 維持未定義；不要因名稱相似便映射到另一層 error code。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ID]
          ↓
[擷取欄位: Command Set] → [套用編碼: Status Code]
                                      ↓
[驗證證據: Command]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Command Set` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Status Code` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Command` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.2.3.2。
2. 依圖中指定的寬度與位置解碼 ID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Command Set 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 105 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.2.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.2.3.2 如何排列 ID、Command Set 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.2.3.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 105 對應的 raw value 或 buffer，標出包含 ID 的 bytes 並解碼，再獨立核對 Command Set。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 ID，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 ID 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Command Set 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ID, Command Set, Status Code, Command

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 105, 文件頁 152-153, PDF 頁 178-179

</details>

<details markdown="1">
<summary><strong>Figure 107: Status Code - Media and Data Integrity Error Values</strong></summary>

<!-- claim:BASE4-FIG-107-CLAIM figure-table:BASE4-FIG-107 -->

**SPEC。** Figure 107〈Status Code - Media and Data Integrity Error Values〉：定義〈Status Code - Media and Data Integrity Error Values〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：TCG, SCT, Status Code。

#### 這張 Figure 在完整流程中的位置

Figure 107 位於 §4.2.3.2，在本流程中是「status」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 TCG 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 status／error 分類表。先確定 status 所在資料結構與類別，再解 individual code、控制 bit 與 retry 指示。Reserved value 維持未定義；不要因名稱相似便映射到另一層 error code。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TCG]
          ↓
[擷取欄位: SCT] → [套用編碼: Status Code]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TCG` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SCT` | Status Code Type，先決定 status 所屬大類，再解讀 SC。 |
| `Status Code` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.2.3.2。
2. 依圖中指定的寬度與位置解碼 TCG；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 SCT 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 107 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.2.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.2.3.2 如何排列 TCG、SCT 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.2.3.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 107 對應的 raw value 或 buffer，標出包含 TCG 的 bytes 並解碼，再獨立核對 SCT。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 TCG，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 TCG 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 SCT 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** TCG, SCT, Status Code

**來源 keyword 索引：** `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 107, 文件頁 154-155, PDF 頁 180-181

</details>

<details markdown="1">
<summary><strong>Figure 108: Status Code - Path Related Status Values</strong></summary>

<!-- claim:BASE4-FIG-108-CLAIM figure-table:BASE4-FIG-108 -->

**SPEC。** Figure 108〈Status Code - Path Related Status Values〉：定義〈Status Code - Path Related Status Values〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：DNR, ANA, Status Code。

#### 這張 Figure 在完整流程中的位置

Figure 108 位於 §4.2.3.3，在本流程中是「status」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DNR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 status／error 分類表。先確定 status 所在資料結構與類別，再解 individual code、控制 bit 與 retry 指示。Reserved value 維持未定義；不要因名稱相似便映射到另一層 error code。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DNR]
          ↓
[擷取欄位: ANA] → [套用編碼: Status Code]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DNR` | Do Not Retry，CQE status 中提示以相同 command 重試預期不會成功的 bit。 |
| `ANA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Status Code` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.2.3.3。
2. 依圖中指定的寬度與位置解碼 DNR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 ANA 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 108 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.2.3.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.2.3.3 如何排列 DNR、ANA 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.2.3.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 108 對應的 raw value 或 buffer，標出包含 DNR 的 bytes 並解碼，再獨立核對 ANA。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 DNR，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 DNR 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 ANA 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** DNR, ANA, Status Code

**來源 keyword 索引：** `should not`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3.3, Figure 108, 文件頁 155, PDF 頁 181

</details>

<details markdown="1">
<summary><strong>Figure 109: Phase Tag bit Transition Example</strong></summary>

<!-- claim:BASE4-FIG-109-CLAIM figure-table:BASE4-FIG-109 -->

**SPEC。** Figure 109〈Phase Tag bit Transition Example〉：呈現〈Phase Tag bit Transition Example〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：Phase Tag。

#### 這張 Figure 在完整流程中的位置

Figure 109 位於 §4.2.4，在本流程中是「queue」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Phase Tag 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 queue／command flow 圖。先標 host 與 controller 的 ownership，再追 head、tail、phase 或 arbitration 的改變；箭頭代表狀態或 ownership 轉移，不自動代表 command 已完成。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Phase Tag]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Phase Tag` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.2.4。
2. 依圖中指定的寬度與位置解碼 Phase Tag；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 109 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.2.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.2.4 如何排列 Phase Tag、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.2.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 109 對應的 raw value 或 buffer，標出包含 Phase Tag 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Phase Tag，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Phase Tag 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Phase Tag

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.4, Figure 109, 文件頁 156-157, PDF 頁 182-183

</details>

<a id="section-4-3"></a>

### §4.3

<details markdown="1">
<summary><strong>Figure 110: PRP Entry Layout</strong></summary>

<!-- claim:BASE4-FIG-110-CLAIM figure-table:BASE4-FIG-110 -->

**SPEC。** Figure 110〈PRP Entry Layout〉：定義〈PRP Entry Layout〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PRP。

#### 這張 Figure 在完整流程中的位置

Figure 110 位於 §4.3.1，在本流程中是「memory」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 PRP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 data-buffer mapping 圖。閱讀順序是 pointer type、address、length、page/segment boundary、下一個 entry。每一步都要維護已涵蓋的 byte interval，才能檢查 overlap、gap、overflow 與 alignment。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PRP]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PRP` | Physical Region Page，以 memory page 為單位描述 host-addressable data buffer 的 pointer 格式。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.3.1。
2. 依圖中指定的寬度與位置解碼 PRP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 110 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.3.1 如何排列 PRP、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.3.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 110 對應的 raw value 或 buffer，標出包含 PRP 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 PRP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 PRP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** PRP

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 110, 文件頁 158, PDF 頁 184

</details>

<details markdown="1">
<summary><strong>Figure 111: PRP Entry - Page Base Address and Offset</strong></summary>

<!-- claim:BASE4-FIG-111-CLAIM figure-table:BASE4-FIG-111 -->

**SPEC。** Figure 111〈PRP Entry - Page Base Address and Offset〉：呈現〈PRP Entry - Page Base Address and Offset〉如何把 transfer 對映到 host memory。 依序追蹤 address、length、page／segment boundary 與下一個 entry 的連結；來源索引：PBAO, PRP。

#### 這張 Figure 在完整流程中的位置

Figure 111 位於 §4.3.1，在本流程中是「memory」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 PBAO 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 data-buffer mapping 圖。閱讀順序是 pointer type、address、length、page/segment boundary、下一個 entry。每一步都要維護已涵蓋的 byte interval，才能檢查 overlap、gap、overflow 與 alignment。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PBAO]
          ↓
[擷取欄位: PRP] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PBAO` | Page Base Address and Offset，第一個 PRP entry 中同時包含 page base 與 page 內 offset 的配置。 |
| `PRP` | Physical Region Page，以 memory page 為單位描述 host-addressable data buffer 的 pointer 格式。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.3.1。
2. 依圖中指定的寬度與位置解碼 PBAO；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 PRP 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 111 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.3.1 如何排列 PBAO、PRP 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.3.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 111 對應的 raw value 或 buffer，標出包含 PBAO 的 bytes 並解碼，再獨立核對 PRP。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 PBAO，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 PBAO 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 PRP 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** PBAO, PRP

**來源 keyword 索引：** `shall`, `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 111, 文件頁 158, PDF 頁 184

</details>

<details markdown="1">
<summary><strong>Figure 112: PRP List Layout for Physically Contiguous Memory Pages</strong></summary>

<!-- claim:BASE4-FIG-112-CLAIM figure-table:BASE4-FIG-112 -->

**SPEC。** Figure 112〈PRP List Layout for Physically Contiguous Memory Pages〉：定義〈PRP List Layout for Physically Contiguous Memory Pages〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PRP, Memory Page。

#### 這張 Figure 在完整流程中的位置

Figure 112 位於 §4.3.1，在本流程中是「memory」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 PRP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 data-buffer mapping 圖。閱讀順序是 pointer type、address、length、page/segment boundary、下一個 entry。每一步都要維護已涵蓋的 byte interval，才能檢查 overlap、gap、overflow 與 alignment。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PRP]
          ↓
[擷取欄位: Memory Page] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PRP` | Physical Region Page，以 memory page 為單位描述 host-addressable data buffer 的 pointer 格式。 |
| `Memory Page` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.3.1。
2. 依圖中指定的寬度與位置解碼 PRP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Memory Page 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 112 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.3.1 如何排列 PRP、Memory Page 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.3.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 112 對應的 raw value 或 buffer，標出包含 PRP 的 bytes 並解碼，再獨立核對 Memory Page。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 PRP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 PRP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Memory Page 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** PRP, Memory Page

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 112, 文件頁 159, PDF 頁 185

</details>

<details markdown="1">
<summary><strong>Figure 113: PRP List Layout for Physically Non-Contiguous Memory Pages</strong></summary>

<!-- claim:BASE4-FIG-113-CLAIM figure-table:BASE4-FIG-113 -->

**SPEC。** Figure 113〈PRP List Layout for Physically Non-Contiguous Memory Pages〉：定義〈PRP List Layout for Physically Non-Contiguous Memory Pages〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PRP, CC.MPS, Memory Page。

#### 這張 Figure 在完整流程中的位置

Figure 113 位於 §4.3.1，在本流程中是「memory」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 PRP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 data-buffer mapping 圖。閱讀順序是 pointer type、address、length、page/segment boundary、下一個 entry。每一步都要維護已涵蓋的 byte interval，才能檢查 overlap、gap、overflow 與 alignment。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PRP]
          ↓
[擷取欄位: CC.MPS] → [套用編碼: Memory Page]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PRP` | Physical Region Page，以 memory page 為單位描述 host-addressable data buffer 的 pointer 格式。 |
| `CC.MPS` | Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.MPS 進一步指定其中的 MPS 子欄位。 |
| `Memory Page` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.3.1。
2. 依圖中指定的寬度與位置解碼 PRP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CC.MPS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 113 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.3.1 如何排列 PRP、CC.MPS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.3.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 113 對應的 raw value 或 buffer，標出包含 PRP 的 bytes 並解碼，再獨立核對 CC.MPS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 PRP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 PRP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CC.MPS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** PRP, CC.MPS, Memory Page

**來源 keyword 索引：** `shall`, `should`, `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 113, 文件頁 159, PDF 頁 185

</details>

<details markdown="1">
<summary><strong>Figure 114: SGL Validation Error Conditions</strong></summary>

<!-- claim:BASE4-FIG-114-CLAIM figure-table:BASE4-FIG-114 -->

**SPEC。** Figure 114〈SGL Validation Error Conditions〉：定義〈SGL Validation Error Conditions〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：SGL。

#### 這張 Figure 在完整流程中的位置

Figure 114 位於 §4.3.2，在本流程中是「status」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SGL 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 status／error 分類表。先確定 status 所在資料結構與類別，再解 individual code、控制 bit 與 retry 指示。Reserved value 維持未定義；不要因名稱相似便映射到另一層 error code。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SGL]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SGL` | Scatter Gather List，以 descriptor 與 segment 描述一段或多段 data buffer 的格式。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.3.2。
2. 依圖中指定的寬度與位置解碼 SGL；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 114 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.3.2 如何排列 SGL、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.3.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 114 對應的 raw value 或 buffer，標出包含 SGL 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SGL，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SGL 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SGL

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 114, 文件頁 161, PDF 頁 187

</details>

<details markdown="1">
<summary><strong>Figure 115: SGL Segment</strong></summary>

<!-- claim:BASE4-FIG-115-CLAIM figure-table:BASE4-FIG-115 -->

**SPEC。** Figure 115〈SGL Segment〉：呈現〈SGL Segment〉如何把 transfer 對映到 host memory。 依序追蹤 address、length、page／segment boundary 與下一個 entry 的連結；來源索引：SGL。

#### 這張 Figure 在完整流程中的位置

Figure 115 位於 §4.3.2，在本流程中是「memory」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SGL 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 data-buffer mapping 圖。閱讀順序是 pointer type、address、length、page/segment boundary、下一個 entry。每一步都要維護已涵蓋的 byte interval，才能檢查 overlap、gap、overflow 與 alignment。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SGL]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SGL` | Scatter Gather List，以 descriptor 與 segment 描述一段或多段 data buffer 的格式。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.3.2。
2. 依圖中指定的寬度與位置解碼 SGL；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 115 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.3.2 如何排列 SGL、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.3.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 115 對應的 raw value 或 buffer，標出包含 SGL 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SGL，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SGL 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SGL

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 115, 文件頁 161, PDF 頁 187

</details>

<details markdown="1">
<summary><strong>Figure 116: Generic SGL Descriptor Format</strong></summary>

<!-- claim:BASE4-FIG-116-CLAIM figure-table:BASE4-FIG-116 -->

**SPEC。** Figure 116〈Generic SGL Descriptor Format〉：定義〈Generic SGL Descriptor Format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DTS, SGLID, SGLDT, SGLDST, SGL, NULL。

#### 這張 Figure 在完整流程中的位置

Figure 116 位於 §4.3.2，在本流程中是「memory」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DTS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 data-buffer mapping 圖。閱讀順序是 pointer type、address、length、page/segment boundary、下一個 entry。每一步都要維護已涵蓋的 byte interval，才能檢查 overlap、gap、overflow 與 alignment。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DTS]
          ↓
[擷取欄位: SGLID] → [套用編碼: SGLDT]
                                      ↓
[驗證證據: SGLDST]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DTS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGLID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGLDT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGLDST` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGL` | Scatter Gather List，以 descriptor 與 segment 描述一段或多段 data buffer 的格式。 |
| `NULL` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.3.2。
2. 依圖中指定的寬度與位置解碼 DTS；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 SGLID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 116 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.3.2 如何排列 DTS、SGLID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.3.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 116 對應的 raw value 或 buffer，標出包含 DTS 的 bytes 並解碼，再獨立核對 SGLID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 DTS，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 DTS 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 SGLID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** DTS, SGLID, SGLDT, SGLDST, SGL, NULL

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 116, 文件頁 161, PDF 頁 187

</details>

<details markdown="1">
<summary><strong>Figure 117: SGL Descriptor Type</strong></summary>

<!-- claim:BASE4-FIG-117-CLAIM figure-table:BASE4-FIG-117 -->

**SPEC。** Figure 117〈SGL Descriptor Type〉：定義〈SGL Descriptor Type〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：SGL。

#### 這張 Figure 在完整流程中的位置

Figure 117 位於 §4.3.2，在本流程中是「memory」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SGL 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 data-buffer mapping 圖。閱讀順序是 pointer type、address、length、page/segment boundary、下一個 entry。每一步都要維護已涵蓋的 byte interval，才能檢查 overlap、gap、overflow 與 alignment。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SGL]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SGL` | Scatter Gather List，以 descriptor 與 segment 描述一段或多段 data buffer 的格式。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.3.2。
2. 依圖中指定的寬度與位置解碼 SGL；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 117 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.3.2 如何排列 SGL、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.3.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 117 對應的 raw value 或 buffer，標出包含 SGL 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SGL，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SGL 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SGL

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 117, 文件頁 161-162, PDF 頁 187-188

</details>

<details markdown="1">
<summary><strong>Figure 118: SGL Descriptor Sub Type Values</strong></summary>

<!-- claim:BASE4-FIG-118-CLAIM figure-table:BASE4-FIG-118 -->

**SPEC。** Figure 118〈SGL Descriptor Sub Type Values〉：定義〈SGL Descriptor Sub Type Values〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：SGL。

#### 這張 Figure 在完整流程中的位置

Figure 118 位於 §4.3.2，在本流程中是「memory」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SGL 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 data-buffer mapping 圖。閱讀順序是 pointer type、address、length、page/segment boundary、下一個 entry。每一步都要維護已涵蓋的 byte interval，才能檢查 overlap、gap、overflow 與 alignment。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SGL]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SGL` | Scatter Gather List，以 descriptor 與 segment 描述一段或多段 data buffer 的格式。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.3.2。
2. 依圖中指定的寬度與位置解碼 SGL；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 118 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.3.2 如何排列 SGL、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.3.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 118 對應的 raw value 或 buffer，標出包含 SGL 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SGL，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SGL 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SGL

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 118, 文件頁 162, PDF 頁 188

</details>

<details markdown="1">
<summary><strong>Figure 119: SGL Data Block descriptor</strong></summary>

<!-- claim:BASE4-FIG-119-CLAIM figure-table:BASE4-FIG-119 -->

**SPEC。** Figure 119〈SGL Data Block descriptor〉：定義〈SGL Data Block descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ADDR, LEN, SGLID, SGLDT, SGLDST, SGL, SGLS。

#### 這張 Figure 在完整流程中的位置

Figure 119 位於 §4.3.2，在本流程中是「memory」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ADDR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 data-buffer mapping 圖。閱讀順序是 pointer type、address、length、page/segment boundary、下一個 entry。每一步都要維護已涵蓋的 byte interval，才能檢查 overlap、gap、overflow 與 alignment。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ADDR]
          ↓
[擷取欄位: LEN] → [套用編碼: SGLID]
                                      ↓
[驗證證據: SGLDT]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ADDR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `LEN` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGLID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGLDT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGLDST` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGL` | Scatter Gather List，以 descriptor 與 segment 描述一段或多段 data buffer 的格式。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.3.2。
2. 依圖中指定的寬度與位置解碼 ADDR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 LEN 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 119 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.3.2 如何排列 ADDR、LEN 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.3.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 119 對應的 raw value 或 buffer，標出包含 ADDR 的 bytes 並解碼，再獨立核對 LEN。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 ADDR，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 ADDR 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 LEN 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ADDR, LEN, SGLID, SGLDT, SGLDST, SGL, SGLS

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 119, 文件頁 162-163, PDF 頁 188-189

</details>

<details markdown="1">
<summary><strong>Figure 120: SGL Bit Bucket descriptor</strong></summary>

<!-- claim:BASE4-FIG-120-CLAIM figure-table:BASE4-FIG-120 -->

**SPEC。** Figure 120〈SGL Bit Bucket descriptor〉：定義〈SGL Bit Bucket descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：LEN, SGLID, SGLDT, SGLDST, SGL, NLB。

#### 這張 Figure 在完整流程中的位置

Figure 120 位於 §4.3.2，在本流程中是「memory」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 LEN 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 data-buffer mapping 圖。閱讀順序是 pointer type、address、length、page/segment boundary、下一個 entry。每一步都要維護已涵蓋的 byte interval，才能檢查 overlap、gap、overflow 與 alignment。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LEN]
          ↓
[擷取欄位: SGLID] → [套用編碼: SGLDT]
                                      ↓
[驗證證據: SGLDST]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LEN` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGLID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGLDT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGLDST` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGL` | Scatter Gather List，以 descriptor 與 segment 描述一段或多段 data buffer 的格式。 |
| `NLB` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.3.2。
2. 依圖中指定的寬度與位置解碼 LEN；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 SGLID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 120 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.3.2 如何排列 LEN、SGLID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.3.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 120 對應的 raw value 或 buffer，標出包含 LEN 的 bytes 並解碼，再獨立核對 SGLID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 LEN，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 LEN 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 SGLID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** LEN, SGLID, SGLDT, SGLDST, SGL, NLB

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 120, 文件頁 163, PDF 頁 189

</details>

<details markdown="1">
<summary><strong>Figure 121: SGL Segment descriptor</strong></summary>

<!-- claim:BASE4-FIG-121-CLAIM figure-table:BASE4-FIG-121 -->

**SPEC。** Figure 121〈SGL Segment descriptor〉：定義〈SGL Segment descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ADDR, LEN, SGLID, SGLDT, SGDST, SGL。

#### 這張 Figure 在完整流程中的位置

Figure 121 位於 §4.3.2，在本流程中是「memory」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ADDR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 data-buffer mapping 圖。閱讀順序是 pointer type、address、length、page/segment boundary、下一個 entry。每一步都要維護已涵蓋的 byte interval，才能檢查 overlap、gap、overflow 與 alignment。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ADDR]
          ↓
[擷取欄位: LEN] → [套用編碼: SGLID]
                                      ↓
[驗證證據: SGLDT]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ADDR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `LEN` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGLID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGLDT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGDST` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGL` | Scatter Gather List，以 descriptor 與 segment 描述一段或多段 data buffer 的格式。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.3.2。
2. 依圖中指定的寬度與位置解碼 ADDR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 LEN 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 121 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.3.2 如何排列 ADDR、LEN 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.3.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 121 對應的 raw value 或 buffer，標出包含 ADDR 的 bytes 並解碼，再獨立核對 LEN。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 ADDR，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 ADDR 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 LEN 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ADDR, LEN, SGLID, SGLDT, SGDST, SGL

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 121, 文件頁 163, PDF 頁 189

</details>

<details markdown="1">
<summary><strong>Figure 122: SGL Last Segment descriptor</strong></summary>

<!-- claim:BASE4-FIG-122-CLAIM figure-table:BASE4-FIG-122 -->

**SPEC。** Figure 122〈SGL Last Segment descriptor〉：定義〈SGL Last Segment descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ADDR, LEN, SGLID, SGLDT, SGLDST, SGL。

#### 這張 Figure 在完整流程中的位置

Figure 122 位於 §4.3.2，在本流程中是「memory」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ADDR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 data-buffer mapping 圖。閱讀順序是 pointer type、address、length、page/segment boundary、下一個 entry。每一步都要維護已涵蓋的 byte interval，才能檢查 overlap、gap、overflow 與 alignment。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ADDR]
          ↓
[擷取欄位: LEN] → [套用編碼: SGLID]
                                      ↓
[驗證證據: SGLDT]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ADDR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `LEN` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGLID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGLDT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGLDST` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGL` | Scatter Gather List，以 descriptor 與 segment 描述一段或多段 data buffer 的格式。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.3.2。
2. 依圖中指定的寬度與位置解碼 ADDR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 LEN 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 122 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.3.2 如何排列 ADDR、LEN 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.3.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 122 對應的 raw value 或 buffer，標出包含 ADDR 的 bytes 並解碼，再獨立核對 LEN。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 ADDR，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 ADDR 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 LEN 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ADDR, LEN, SGLID, SGLDT, SGLDST, SGL

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 122, 文件頁 164, PDF 頁 190

</details>

<details markdown="1">
<summary><strong>Figure 125: SGL Read Example</strong></summary>

<!-- claim:BASE4-FIG-125-CLAIM figure-table:BASE4-FIG-125 -->

**SPEC。** Figure 125〈SGL Read Example〉：呈現〈SGL Read Example〉如何把 transfer 對映到 host memory。 依序追蹤 address、length、page／segment boundary 與下一個 entry 的連結；來源索引：SGL。

#### 這張 Figure 在完整流程中的位置

Figure 125 位於 §4.3.2.1，在本流程中是「memory」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SGL 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 data-buffer mapping 圖。閱讀順序是 pointer type、address、length、page/segment boundary、下一個 entry。每一步都要維護已涵蓋的 byte interval，才能檢查 overlap、gap、overflow 與 alignment。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SGL]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SGL` | Scatter Gather List，以 descriptor 與 segment 描述一段或多段 data buffer 的格式。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.3.2.1。
2. 依圖中指定的寬度與位置解碼 SGL；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 125 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.3.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.3.2.1 如何排列 SGL、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.3.2.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 125 對應的 raw value 或 buffer，標出包含 SGL 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SGL，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SGL 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SGL

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2.1, Figure 125, 文件頁 166, PDF 頁 192

</details>

<a id="section-4-4"></a>

### §4.4

<details markdown="1">
<summary><strong>Figure 126: Current Value after Reset with Scope of Entire NVM Subsystem</strong></summary>

<!-- claim:BASE4-FIG-126-CLAIM figure-table:BASE4-FIG-126 -->

**SPEC。** Figure 126〈Current Value after Reset with Scope of Entire NVM Subsystem〉：呈現〈Current Value after Reset with Scope of Entire NVM Subsystem〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem。

#### 這張 Figure 在完整流程中的位置

Figure 126 位於 §4.4，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Subsystem 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NVM Subsystem]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NVM Subsystem` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.4。
2. 依圖中指定的寬度與位置解碼 NVM Subsystem；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 126 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.4 如何排列 NVM Subsystem、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 126 對應的 raw value 或 buffer，標出包含 NVM Subsystem 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NVM Subsystem，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NVM Subsystem 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NVM Subsystem

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.4, Figure 126, 文件頁 167, PDF 頁 193

</details>

<details markdown="1">
<summary><strong>Figure 127: Current Value after Reset with Scope of Subset of the NVM Subsystem</strong></summary>

<!-- claim:BASE4-FIG-127-CLAIM figure-table:BASE4-FIG-127 -->

**SPEC。** Figure 127〈Current Value after Reset with Scope of Subset of the NVM Subsystem〉：呈現〈Current Value after Reset with Scope of Subset of the NVM Subsystem〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem。

#### 這張 Figure 在完整流程中的位置

Figure 127 位於 §4.4，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Subsystem 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NVM Subsystem]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NVM Subsystem` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.4。
2. 依圖中指定的寬度與位置解碼 NVM Subsystem；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 127 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.4 如何排列 NVM Subsystem、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 127 對應的 raw value 或 buffer，標出包含 NVM Subsystem 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NVM Subsystem，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NVM Subsystem 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NVM Subsystem

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.4, Figure 127, 文件頁 168, PDF 頁 194

</details>

<a id="section-4-5"></a>

### §4.5

<details markdown="1">
<summary><strong>Figure 128: PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)</strong></summary>

<!-- claim:BASE4-FIG-128-CLAIM figure-table:BASE4-FIG-128 -->

**SPEC。** Figure 128〈PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)〉：呈現〈PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：ID, VID, SSVID。

#### 這張 Figure 在完整流程中的位置

Figure 128 位於 §4.5.1，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ID]
          ↓
[擷取欄位: VID] → [套用編碼: SSVID]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `VID` | Vendor ID，由 PCI-SIG 配置、辨識 vendor 的 identifier。 |
| `SSVID` | Subsystem Vendor ID，辨識 subsystem vendor 的 PCI identifier。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.5.1。
2. 依圖中指定的寬度與位置解碼 ID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 VID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 128 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.5.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.5.1 如何排列 ID、VID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.5.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 128 對應的 raw value 或 buffer，標出包含 ID 的 bytes 並解碼，再獨立核對 VID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 ID，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 ID 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 VID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ID, VID, SSVID

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.1, Figure 128, 文件頁 169, PDF 頁 195

</details>

<details markdown="1">
<summary><strong>Figure 129: Serial Number (SN) and Model Number (MN)</strong></summary>

<!-- claim:BASE4-FIG-129-CLAIM figure-table:BASE4-FIG-129 -->

**SPEC。** Figure 129〈Serial Number (SN) and Model Number (MN)〉：定義〈Serial Number (SN) and Model Number (MN)〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：SN, MN。

#### 這張 Figure 在完整流程中的位置

Figure 129 位於 §4.5.2，在本流程中是「identifier」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SN 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 identifier 格式圖。先記錄 width 與 encoding，再辨識 issuing authority、uniqueness scope、reserved value 與有效生命週期；不要把長度相同的 identifiers 當成可互換。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SN]
          ↓
[擷取欄位: MN] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SN` | Serial Number，辨識一個產品實例的序號字串。 |
| `MN` | Model Number，辨識產品型號的字串。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.5.2。
2. 依圖中指定的寬度與位置解碼 SN；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MN 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 129 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.5.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.5.2 如何排列 SN、MN 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.5.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 129 對應的 raw value 或 buffer，標出包含 SN 的 bytes 並解碼，再獨立核對 MN。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SN，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SN 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MN 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SN, MN

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.2, Figure 129, 文件頁 170, PDF 頁 196

</details>

<details markdown="1">
<summary><strong>Figure 130: IEEE OUI Identifier (IEEE)</strong></summary>

<!-- claim:BASE4-FIG-130-CLAIM figure-table:BASE4-FIG-130 -->

**SPEC。** Figure 130〈IEEE OUI Identifier (IEEE)〉：定義〈IEEE OUI Identifier (IEEE)〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：IEEE, OUI。

#### 這張 Figure 在完整流程中的位置

Figure 130 位於 §4.5.3，在本流程中是「identifier」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 IEEE 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 identifier 格式圖。先記錄 width 與 encoding，再辨識 issuing authority、uniqueness scope、reserved value 與有效生命週期；不要把長度相同的 identifiers 當成可互換。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: IEEE]
          ↓
[擷取欄位: OUI] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `IEEE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `OUI` | Organizationally Unique Identifier，由 IEEE 配置給組織的 identifier 前綴。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.5.3。
2. 依圖中指定的寬度與位置解碼 IEEE；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 OUI 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 130 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.5.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.5.3 如何排列 IEEE、OUI 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.5.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 130 對應的 raw value 或 buffer，標出包含 IEEE 的 bytes 並解碼，再獨立核對 OUI。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 IEEE，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 IEEE 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 OUI 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** IEEE, OUI

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.3, Figure 130, 文件頁 170, PDF 頁 196

</details>

<details markdown="1">
<summary><strong>Figure 131: IEEE Extended Unique Identifier (EUI64), MA-L Format</strong></summary>

<!-- claim:BASE4-FIG-131-CLAIM figure-table:BASE4-FIG-131 -->

**SPEC。** Figure 131〈IEEE Extended Unique Identifier (EUI64), MA-L Format〉：定義〈IEEE Extended Unique Identifier (EUI64), MA-L Format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：IEEE, EUI64, MA, EUI, OUI。

#### 這張 Figure 在完整流程中的位置

Figure 131 位於 §4.5.4，在本流程中是「identifier」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 IEEE 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 identifier 格式圖。先記錄 width 與 encoding，再辨識 issuing authority、uniqueness scope、reserved value 與有效生命週期；不要把長度相同的 identifiers 當成可互換。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: IEEE]
          ↓
[擷取欄位: EUI64] → [套用編碼: MA]
                                      ↓
[驗證證據: EUI]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `IEEE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `EUI64` | 64-bit Extended Unique Identifier，使用 IEEE 配置空間建立的 64-bit identifier。 |
| `MA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `EUI` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `OUI` | Organizationally Unique Identifier，由 IEEE 配置給組織的 identifier 前綴。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.5.4。
2. 依圖中指定的寬度與位置解碼 IEEE；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 EUI64 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 131 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.5.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.5.4 如何排列 IEEE、EUI64 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.5.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 131 對應的 raw value 或 buffer，標出包含 IEEE 的 bytes 並解碼，再獨立核對 EUI64。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 IEEE，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 IEEE 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 EUI64 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** IEEE, EUI64, MA, EUI, OUI

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 131, 文件頁 170, PDF 頁 196

</details>

<details markdown="1">
<summary><strong>Figure 132: IEEE Extended Unique Identifier (EUI64), OUI Identifier</strong></summary>

<!-- claim:BASE4-FIG-132-CLAIM figure-table:BASE4-FIG-132 -->

**SPEC。** Figure 132〈IEEE Extended Unique Identifier (EUI64), OUI Identifier〉：定義〈IEEE Extended Unique Identifier (EUI64), OUI Identifier〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：IEEE, EUI64, OUI。

#### 這張 Figure 在完整流程中的位置

Figure 132 位於 §4.5.4，在本流程中是「identifier」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 IEEE 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 identifier 格式圖。先記錄 width 與 encoding，再辨識 issuing authority、uniqueness scope、reserved value 與有效生命週期；不要把長度相同的 identifiers 當成可互換。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: IEEE]
          ↓
[擷取欄位: EUI64] → [套用編碼: OUI]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `IEEE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `EUI64` | 64-bit Extended Unique Identifier，使用 IEEE 配置空間建立的 64-bit identifier。 |
| `OUI` | Organizationally Unique Identifier，由 IEEE 配置給組織的 identifier 前綴。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.5.4。
2. 依圖中指定的寬度與位置解碼 IEEE；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 EUI64 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 132 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.5.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.5.4 如何排列 IEEE、EUI64 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.5.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 132 對應的 raw value 或 buffer，標出包含 IEEE 的 bytes 並解碼，再獨立核對 EUI64。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 IEEE，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 IEEE 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 EUI64 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** IEEE, EUI64, OUI

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 132, 文件頁 170, PDF 頁 196

</details>

<details markdown="1">
<summary><strong>Figure 133: IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)</strong></summary>

<!-- claim:BASE4-FIG-133-CLAIM figure-table:BASE4-FIG-133 -->

**SPEC。** Figure 133〈IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)〉：定義〈IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：IEEE, EUI64, ID, MA, WWN, NAA。

#### 這張 Figure 在完整流程中的位置

Figure 133 位於 §4.5.4，在本流程中是「identifier」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 IEEE 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 identifier 格式圖。先記錄 width 與 encoding，再辨識 issuing authority、uniqueness scope、reserved value 與有效生命週期；不要把長度相同的 identifiers 當成可互換。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: IEEE]
          ↓
[擷取欄位: EUI64] → [套用編碼: ID]
                                      ↓
[驗證證據: MA]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `IEEE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `EUI64` | 64-bit Extended Unique Identifier，使用 IEEE 配置空間建立的 64-bit identifier。 |
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `WWN` | World Wide Name，用於儲存與網路裝置識別的全域名稱格式。 |
| `NAA` | Network Address Authority，WWN 中選擇 identifier 格式與配置方式的 nibble。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.5.4。
2. 依圖中指定的寬度與位置解碼 IEEE；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 EUI64 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 133 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.5.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.5.4 如何排列 IEEE、EUI64 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.5.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 133 對應的 raw value 或 buffer，標出包含 IEEE 的 bytes 並解碼，再獨立核對 EUI64。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 IEEE，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 IEEE 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 EUI64 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** IEEE, EUI64, ID, MA, WWN, NAA

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 133, 文件頁 170-171, PDF 頁 196-197

</details>

<details markdown="1">
<summary><strong>Figure 134: MA-L similarity to WWN</strong></summary>

<!-- claim:BASE4-FIG-134-CLAIM figure-table:BASE4-FIG-134 -->

**SPEC。** Figure 134〈MA-L similarity to WWN〉：定義〈MA-L similarity to WWN〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：MA, WWN。

#### 這張 Figure 在完整流程中的位置

Figure 134 位於 §4.5.4，在本流程中是「identifier」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 MA 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 identifier 格式圖。先記錄 width 與 encoding，再辨識 issuing authority、uniqueness scope、reserved value 與有效生命週期；不要把長度相同的 identifiers 當成可互換。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MA]
          ↓
[擷取欄位: WWN] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `WWN` | World Wide Name，用於儲存與網路裝置識別的全域名稱格式。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.5.4。
2. 依圖中指定的寬度與位置解碼 MA；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 WWN 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 134 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.5.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.5.4 如何排列 MA、WWN 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.5.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 134 對應的 raw value 或 buffer，標出包含 MA 的 bytes 並解碼，再獨立核對 WWN。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 MA，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 MA 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 WWN 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** MA, WWN

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 134, 文件頁 171, PDF 頁 197

</details>

<details markdown="1">
<summary><strong>Figure 135: Namespace Globally Unique Identifier (NGUID)</strong></summary>

<!-- claim:BASE4-FIG-135-CLAIM figure-table:BASE4-FIG-135 -->

**SPEC。** Figure 135〈Namespace Globally Unique Identifier (NGUID)〉：定義〈Namespace Globally Unique Identifier (NGUID)〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NGUID, Namespace。

#### 這張 Figure 在完整流程中的位置

Figure 135 位於 §4.5.5，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NGUID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NGUID]
          ↓
[擷取欄位: Namespace] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NGUID` | Namespace Globally Unique Identifier，namespace 的 128-bit 全域識別值。 |
| `Namespace` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.5.5。
2. 依圖中指定的寬度與位置解碼 NGUID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Namespace 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 135 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.5.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.5.5 如何排列 NGUID、Namespace 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.5.5 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 135 對應的 raw value 或 buffer，標出包含 NGUID 的 bytes 並解碼，再獨立核對 Namespace。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NGUID，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NGUID 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Namespace 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NGUID, Namespace

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 135, 文件頁 171, PDF 頁 197

</details>

<details markdown="1">
<summary><strong>Figure 136: Namespace Globally Unique Identifier (NGUID), OUI</strong></summary>

<!-- claim:BASE4-FIG-136-CLAIM figure-table:BASE4-FIG-136 -->

**SPEC。** Figure 136〈Namespace Globally Unique Identifier (NGUID), OUI〉：定義〈Namespace Globally Unique Identifier (NGUID), OUI〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NGUID, OUI, VSP, ID, Namespace。

#### 這張 Figure 在完整流程中的位置

Figure 136 位於 §4.5.5，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NGUID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NGUID]
          ↓
[擷取欄位: OUI] → [套用編碼: VSP]
                                      ↓
[驗證證據: ID]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NGUID` | Namespace Globally Unique Identifier，namespace 的 128-bit 全域識別值。 |
| `OUI` | Organizationally Unique Identifier，由 IEEE 配置給組織的 identifier 前綴。 |
| `VSP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Namespace` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.5.5。
2. 依圖中指定的寬度與位置解碼 NGUID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 OUI 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 136 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.5.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.5.5 如何排列 NGUID、OUI 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.5.5 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 136 對應的 raw value 或 buffer，標出包含 NGUID 的 bytes 並解碼，再獨立核對 OUI。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NGUID，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NGUID 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 OUI 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NGUID, OUI, VSP, ID, Namespace

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 136, 文件頁 171, PDF 頁 197

</details>

<details markdown="1">
<summary><strong>Figure 137: Namespace Globally Unique Identifier</strong></summary>

<!-- claim:BASE4-FIG-137-CLAIM figure-table:BASE4-FIG-137 -->

**SPEC。** Figure 137〈Namespace Globally Unique Identifier〉：定義〈Namespace Globally Unique Identifier〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NGUID, WWN, IEEE, NAA, Namespace。

#### 這張 Figure 在完整流程中的位置

Figure 137 位於 §4.5.5，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NGUID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NGUID]
          ↓
[擷取欄位: WWN] → [套用編碼: IEEE]
                                      ↓
[驗證證據: NAA]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NGUID` | Namespace Globally Unique Identifier，namespace 的 128-bit 全域識別值。 |
| `WWN` | World Wide Name，用於儲存與網路裝置識別的全域名稱格式。 |
| `IEEE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NAA` | Network Address Authority，WWN 中選擇 identifier 格式與配置方式的 nibble。 |
| `Namespace` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.5.5。
2. 依圖中指定的寬度與位置解碼 NGUID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 WWN 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 137 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.5.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.5.5 如何排列 NGUID、WWN 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.5.5 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 137 對應的 raw value 或 buffer，標出包含 NGUID 的 bytes 並解碼，再獨立核對 WWN。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NGUID，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NGUID 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 WWN 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NGUID, WWN, IEEE, NAA, Namespace

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 137, 文件頁 171, PDF 頁 197

</details>

<details markdown="1">
<summary><strong>Figure 138: Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN</strong></summary>

<!-- claim:BASE4-FIG-138-CLAIM figure-table:BASE4-FIG-138 -->

**SPEC。** Figure 138〈Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN〉：定義〈Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NGUID, WWN, OUI, NAA, Namespace。

#### 這張 Figure 在完整流程中的位置

Figure 138 位於 §4.5.5，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NGUID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NGUID]
          ↓
[擷取欄位: WWN] → [套用編碼: OUI]
                                      ↓
[驗證證據: NAA]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NGUID` | Namespace Globally Unique Identifier，namespace 的 128-bit 全域識別值。 |
| `WWN` | World Wide Name，用於儲存與網路裝置識別的全域名稱格式。 |
| `OUI` | Organizationally Unique Identifier，由 IEEE 配置給組織的 identifier 前綴。 |
| `NAA` | Network Address Authority，WWN 中選擇 identifier 格式與配置方式的 nibble。 |
| `Namespace` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.5.5。
2. 依圖中指定的寬度與位置解碼 NGUID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 WWN 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 138 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.5.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.5.5 如何排列 NGUID、WWN 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.5.5 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 138 對應的 raw value 或 buffer，標出包含 NGUID 的 bytes 並解碼，再獨立核對 WWN。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NGUID，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NGUID 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 WWN 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NGUID, WWN, OUI, NAA, Namespace

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 138, 文件頁 171, PDF 頁 197

</details>

<a id="section-4-6"></a>

### §4.6

<details markdown="1">
<summary><strong>Figure 139: Controller List Format</strong></summary>

<!-- claim:BASE4-FIG-139-CLAIM figure-table:BASE4-FIG-139 -->

**SPEC。** Figure 139〈Controller List Format〉：定義〈Controller List Format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NUMCIDS, Controller。

#### 這張 Figure 在完整流程中的位置

Figure 139 位於 §4.6.1，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NUMCIDS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NUMCIDS]
          ↓
[擷取欄位: Controller] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NUMCIDS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Controller` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.6.1。
2. 依圖中指定的寬度與位置解碼 NUMCIDS；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Controller 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 139 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.6.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.6.1 如何排列 NUMCIDS、Controller 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.6.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 139 對應的 raw value 或 buffer，標出包含 NUMCIDS 的 bytes 並解碼，再獨立核對 Controller。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NUMCIDS，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NUMCIDS 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Controller 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NUMCIDS, Controller

**來源 keyword 索引：** `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.6.1, Figure 139, 文件頁 172, PDF 頁 198

</details>

<details markdown="1">
<summary><strong>Figure 140: Namespace List Format</strong></summary>

<!-- claim:BASE4-FIG-140-CLAIM figure-table:BASE4-FIG-140 -->

**SPEC。** Figure 140〈Namespace List Format〉：定義〈Namespace List Format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ID, Namespace。

#### 這張 Figure 在完整流程中的位置

Figure 140 位於 §4.6.2，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ID]
          ↓
[擷取欄位: Namespace] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Namespace` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.6.2。
2. 依圖中指定的寬度與位置解碼 ID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Namespace 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 140 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.6.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.6.2 如何排列 ID、Namespace 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.6.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 140 對應的 raw value 或 buffer，標出包含 ID 的 bytes 並解碼，再獨立核對 Namespace。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 ID，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 ID 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Namespace 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ID, Namespace

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.6.2, Figure 140, 文件頁 172, PDF 頁 198

</details>

<a id="section-4-8"></a>

### §4.8

<details markdown="1">
<summary><strong>Figure 142: UTF-8 Input Processing</strong></summary>

<!-- claim:BASE4-FIG-142-CLAIM figure-table:BASE4-FIG-142 -->

**SPEC。** Figure 142〈UTF-8 Input Processing〉：呈現〈UTF-8 Input Processing〉要求的輸入驗證順序。 依序執行 decoding、禁止 code point 與 truncation 檢查；來源索引：UTF。

#### 這張 Figure 在完整流程中的位置

Figure 142 位於 §4.8，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 UTF 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: UTF]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `UTF` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.8。
2. 依圖中指定的寬度與位置解碼 UTF；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 142 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §4.8 如何排列 UTF、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.8 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 142 對應的 raw value 或 buffer，標出包含 UTF 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 UTF，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 UTF 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** UTF

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.8, Figure 142, 文件頁 175, PDF 頁 201

</details>

## 使用與限制

製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata 集合或核准範圍改變時，必須重新核對受影響 claim。
