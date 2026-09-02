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

## 先學縮寫：完整 Glossary

下列縮寫會在投影片主線使用前先定義。縮寫本身永遠不夠；設計與 Debug 還要保留 owner、width、unit、scope 與 state。

| 縮寫／名詞 | 白話解釋 | 來源 |
|---|---|---|
| `NVMe` | Non-Volatile Memory Express，主機與非揮發性記憶體子系統之間的介面規範家族。 | NVME-BASE-2.4 Rev. 2.4，§1.1.1，文件頁 1，PDF 頁 27 |
| `NVM` | Non-Volatile Memory，斷電後仍能保存資料的記憶體。 | NVME-BASE-2.4 Rev. 2.4，§1.1.1，文件頁 1，PDF 頁 27 |
| `I/O` | Input/Output，對 namespace 執行資料輸入與輸出的操作類別。 | NVME-BASE-2.4 Rev. 2.4，§2.3.2，文件頁 33，PDF 頁 59 |
| `Admin` | Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。 | NVME-BASE-2.4 Rev. 2.4，§2.3.2，文件頁 33，PDF 頁 59 |
| `SQ` | Submission Queue，主機放入命令的提交佇列。 | NVME-BASE-2.4 Rev. 2.4，§2.1，文件頁 21-23，PDF 頁 47-49 |
| `CQ` | Completion Queue，controller 放入完成結果的完成佇列。 | NVME-BASE-2.4 Rev. 2.4，§2.1，文件頁 21-23，PDF 頁 47-49 |
| `SQE` | Submission Queue Entry，SQ 中的一筆命令資料結構。 | NVME-BASE-2.4 Rev. 2.4，§2.1，文件頁 21-23，PDF 頁 47-49 |
| `CQE` | Completion Queue Entry，CQ 中的一筆完成結果資料結構。 | NVME-BASE-2.4 Rev. 2.4，§2.1，文件頁 21-23，PDF 頁 47-49 |
| `NSID` | Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。 | NVME-BASE-2.4 Rev. 2.4，§2.3.3，文件頁 33-35，PDF 頁 59-61 |
| `NVM subsystem` | NVM subsystem，包含 controller、port、namespace 與非揮發性儲存資源的 NVMe 系統邊界。 | NVME-BASE-2.4 Rev. 2.4，§2.3.1，文件頁 26-33，PDF 頁 52-59 |
| `namespace` | namespace，主機透過 controller 存取的一份已格式化非揮發性容量。 | NVME-BASE-2.4 Rev. 2.4，§2.3.1，文件頁 26-33，PDF 頁 52-59 |
| `NVM Set` | NVM Set，把 namespace 與一組共同管理的 NVM 資源建立關聯的容量集合。 | NVME-BASE-2.4 Rev. 2.4，§2.3.1，文件頁 26-33，PDF 頁 52-59 |
| `Endurance Group` | Endurance Group，用於隔離與回報耐久度相關狀態的 NVM 資源群組。 | NVME-BASE-2.4 Rev. 2.4，§2.3.1，文件頁 26-33，PDF 頁 52-59 |
| `Reclaim Group` | Reclaim Group，具有共同回收行為的一組非揮發性儲存資源。 | NVME-BASE-2.4 Rev. 2.4，§2.3.1，文件頁 26-33，PDF 頁 52-59 |
| `Reclaim Unit` | Reclaim Unit，controller 執行媒體回收時使用的較小管理粒度。 | NVME-BASE-2.4 Rev. 2.4，§2.3.1，文件頁 26-33，PDF 頁 52-59 |
| `SR-IOV` | Single Root I/O Virtualization，讓一個 PCIe 裝置呈現一個 PF 與多個 VF 的虛擬化能力。 | NVME-BASE-2.4 Rev. 2.4，§2.4.1，文件頁 35-37，PDF 頁 61-63 |
| `PF` | Physical Function，具有完整 PCIe 設定能力、可管理相關 VF 的實體功能。 | NVME-BASE-2.4 Rev. 2.4，§2.4.1，文件頁 35-37，PDF 頁 61-63 |
| `VF` | Virtual Function，由 SR-IOV 建立、資源較受限的 PCIe 虛擬功能。 | NVME-BASE-2.4 Rev. 2.4，§2.4.1，文件頁 35-37，PDF 頁 61-63 |
| `Dword` | Double word，四個 bytes、共 32 bits；NVMe command 欄位常以 CDW 編號。 | NVME-BASE-2.4 Rev. 2.4，§1.4.3，文件頁 5，PDF 頁 31 |
| `0's-based` | 0's-based encoding，以 0 表示實際數量 1；解碼公式通常是欄位值加 1。 | NVME-BASE-2.4 Rev. 2.4，§1.4.2，文件頁 3-5，PDF 頁 29-31 |

## Visual Atlas：先用圖建立整體位置

每張教學重畫回答不同問題：Architecture 定位元件、Sequence 顯示 ownership、Decode 把 bits 轉成工程值、State 保留 failure evidence；它們不是 Spec 原圖的複製。

### Visual 01: 先找對規格：不要把文件關係看成 protocol stack

**View type:** `architecture`

```text
[需求：我要做什麼？]
  ├─ [Base：共通機制]
  ├─ [PCIe Transport：記憶體與 register 綁定]
  └─ [I/O Command Set：資料操作語意]
```

**回答的問題：** 遇到一個 command、register 或資料格式時，第一個問題不是『它在哪一頁』，而是『哪一份規格擁有這個定義』。Base 提供通用協定，Transport 補上 PCIe 綁定，I/O Command Set 再定義 namespace 資料操作。Figure 1 的框線代表適用關係，不代表封包一定逐層穿過這些方塊。

**支援 Figure：** Figure 1, Figure 5

**來源：** NVME-BASE-2.4 Rev. 2.4，§1.1.1，文件頁 1，PDF 頁 27; NVME-BASE-2.4 Rev. 2.4，§2.3.2，文件頁 33，PDF 頁 59

### Visual 02: 先解碼數值，再解讀欄位

**View type:** `decode`

```text
[RAW: 原始 bits] → [LOCATE: 確認 bit/byte 範圍] → [DECODE: 套用 radix 與 endian] → [VALIDATE: 套用 unit／0's-based]
VALIDATE fail ──→ return to RAW evidence
```

**回答的問題：** NVMe 的數字同時帶有進位、單位、寬度、endian 與是否 0's-based 等資訊。欄位值看似相同，只要其中一項不同，實際意義就可能完全不同。Figure 2 與 Figure 3 是後續所有 register、SQE、CQE 與 log page 計算的共同底座。

**支援 Figure：** Figure 2, Figure 3

**來源：** NVME-BASE-2.4 Rev. 2.4，§1.4.2，文件頁 3-5，PDF 頁 29-31; NVME-BASE-2.4 Rev. 2.4，§1.4.3，文件頁 5，PDF 頁 31

### Visual 03: Queue pair 是所有 command flow 的交通規則

**View type:** `sequence`

```text
Host / software        Shared object        Controller / evidence
Host → Shared: host 填 SQE
Shared → Controller: host 公布 SQ tail
Controller → Shared: controller fetch／execute
Shared → Host: controller 寫 CQE
Host → Shared: host 消費 CQE
```

**回答的問題：** host 不把 command 直接寫進 controller。host 先在記憶體中的 SQE 建好命令，再公布新的 SQ tail；controller 取走命令後執行，最後把 CQE 放進 CQ。Figure 6 的 1:1 與 Figure 7 的 n:1 差異在於多個 SQ 是否共用同一個 CQ，不是 command 是否共用同一個 SQE。

**支援 Figure：** Figure 6, Figure 7

**來源：** NVME-BASE-2.4 Rev. 2.4，§2.1，文件頁 21-23，PDF 頁 47-49; NVME-BASE-2.4 Rev. 2.4，§2.3.3，文件頁 33-35，PDF 頁 59-61

### Visual 04: 從 namespace 往上建立儲存與路徑 Mental Model

**View type:** `architecture`

```text
[NVM subsystem]
  ├─ [Domain／Endurance Group]
  ├─ [NVM Set 或 Reclaim Group]
  ├─ [Namespace]
  └─ [Controller-visible NSID]
```

**回答的問題：** namespace 是 host 實際存取的格式化容量，但容量管理、耐久度、回收與路徑都發生在不同層級。Figures 11-18 用 NVM Set 或 Reclaim Group 描述容量包含關係，Figures 19-22 則改看 controller、port、path 與 PCIe Function。兩組圖回答不同問題，不能疊成單一樹狀圖後便認為每層都一對一。

**支援 Figure：** Figure 11, Figure 12, Figure 13, Figure 14, Figure 15, Figure 16, Figure 17, Figure 18, Figure 19, Figure 20, Figure 21, Figure 22

**來源：** NVME-BASE-2.4 Rev. 2.4，§2.3.1，文件頁 26-33，PDF 頁 52-59; NVME-BASE-2.4 Rev. 2.4，§2.3.3，文件頁 33-35，PDF 頁 59-61; NVME-BASE-2.4 Rev. 2.4，§2.4.1，文件頁 35-37，PDF 頁 61-63; NVME-BASE-2.4 Rev. 2.4，§2.4.2，文件頁 37，PDF 頁 63

## Mental Model 與完整教學流程

以下依工程因果而非 Spec section 排列；相關 Figure 會回到它支援的流程節點，不以編號順序取代教學故事線。

### Module 01: 先找對規格：不要把文件關係看成 protocol stack

**解釋。** 遇到一個 command、register 或資料格式時，第一個問題不是『它在哪一頁』，而是『哪一份規格擁有這個定義』。Base 提供通用協定，Transport 補上 PCIe 綁定，I/O Command Set 再定義 namespace 資料操作。Figure 1 的框線代表適用關係，不代表封包一定逐層穿過這些方塊。

```text
需求：我要做什麼？
  ↓
Base：共通機制
  ↓
PCIe Transport：記憶體與 register 綁定
  ↓
I/O Command Set：資料操作語意
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Base | 共通 command、queue、status 與資料結構 | 不要假設它定義所有 PCIe register 細節 |
| PCIe Transport | BAR、MMIO、doorbell、interrupt 與 PCIe-specific 行為 | 衝突時不能覆蓋 Base |
| I/O Command Set | 特定 namespace I/O command 與延伸資料結構 | 不負責重新定義 transport |

**說明性範例。** 要實作 Firmware Image Download：先在 Base 找 command 欄位與 completion status，再到 PCIe Transport 確認 Admin command 的資料指標與 memory access 限制。若未閱讀 I/O Command Set，仍可理解此 Admin command；反過來只讀 PCIe Transport 則得不到完整 command 語意。

**常見誤解／Debug。** 常見錯誤是看到 Figure 1 的上下位置便推論『上層一定呼叫下層』。正確做法是把每一個技術論點標成 owner、extension 或 binding，再引用真正擁有 normative requirement 的來源。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§1.1.1，文件頁 1，PDF 頁 27; NVME-BASE-2.4 Rev. 2.4，§2.3.2，文件頁 33，PDF 頁 59

**關聯 Figure：** Figure 1, Figure 5

### Module 02: 先解碼數值，再解讀欄位

**解釋。** NVMe 的數字同時帶有進位、單位、寬度、endian 與是否 0's-based 等資訊。欄位值看似相同，只要其中一項不同，實際意義就可能完全不同。Figure 2 與 Figure 3 是後續所有 register、SQE、CQE 與 log page 計算的共同底座。

```text
原始 bits
  ↓
確認 bit/byte 範圍
  ↓
套用 radix 與 endian
  ↓
套用 unit／0's-based
  ↓
得到工程值
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| 1000 | 十進位 1000 | 若無 b/h 後綴則按十進位 |
| 1000b | 二進位 8 | b 是 radix，不是 bit 單位 |
| 1000h | 十六進位 4096 | 常見於 offset 與 register value |
| NUMD=0 | 實際 1 dword | 只有欄位明載 0's-based 才加 1 |

**說明性範例。** 說明性範例：一個 512-byte transfer 含 512 ÷ 4 = 128 dwords。若 NUMD 是 0's-based，編碼值為 128 - 1 = 127 = 007Fh。若錯把 007Fh 當成 byte count，buffer 會短少；若忘記減 1，controller 會被要求傳輸 129 dwords。

**常見誤解／Debug。** Debug 時把五項資訊寫在同一行：raw value、bit range、radix、unit、encoding rule。只印出十進位結果而沒有原始 hex，通常不足以定位 off-by-one、byte swap 或單位錯誤。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§1.4.2，文件頁 3-5，PDF 頁 29-31; NVME-BASE-2.4 Rev. 2.4，§1.4.3，文件頁 5，PDF 頁 31

**關聯 Figure：** Figure 2, Figure 3

### Module 03: Queue pair 是所有 command flow 的交通規則

**解釋。** host 不把 command 直接寫進 controller。host 先在記憶體中的 SQE 建好命令，再公布新的 SQ tail；controller 取走命令後執行，最後把 CQE 放進 CQ。Figure 6 的 1:1 與 Figure 7 的 n:1 差異在於多個 SQ 是否共用同一個 CQ，不是 command 是否共用同一個 SQE。

```text
host 填 SQE
  ↓
host 公布 SQ tail
  ↓
controller fetch／execute
  ↓
controller 寫 CQE
  ↓
host 消費 CQE
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Admin queue pair | 一個 Admin SQ 對一個 Admin CQ | 初始化與管理路徑 |
| I/O 1:1 | 一個 I/O SQ 對一個 I/O CQ | 追蹤簡單、隔離清楚 |
| I/O n:1 | 多個 I/O SQ 共用一個 I/O CQ | 完成路徑整併，仍以 SQID/CID 找回命令 |

**說明性範例。** 說明性範例：SQ 3 與 SQ 4 共用 CQ 2。兩筆 command 都使用 CID 5 仍可區分，因唯一鍵是 (SQID, CID)：(3,5) 與 (4,5)。只用 CID 建 outstanding-command map，會把其中一筆 completion 配錯。

**常見誤解／Debug。** Queue bug 要分三個 ownership：誰寫 entry、誰推進 pointer、誰能重用 slot。把『doorbell 已寫』誤當成『command 已完成』，或在 CQE 尚未消費前重用資源，都是典型生命週期錯誤。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§2.1，文件頁 21-23，PDF 頁 47-49; NVME-BASE-2.4 Rev. 2.4，§2.3.3，文件頁 33-35，PDF 頁 59-61

**關聯 Figure：** Figure 6, Figure 7

### Module 04: 從 namespace 往上建立儲存與路徑 Mental Model

**解釋。** namespace 是 host 實際存取的格式化容量，但容量管理、耐久度、回收與路徑都發生在不同層級。Figures 11-18 用 NVM Set 或 Reclaim Group 描述容量包含關係，Figures 19-22 則改看 controller、port、path 與 PCIe Function。兩組圖回答不同問題，不能疊成單一樹狀圖後便認為每層都一對一。

```text
NVM subsystem
  ↓
Domain／Endurance Group
  ↓
NVM Set 或 Reclaim Group
  ↓
Namespace
  ↓
Controller-visible NSID
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| multi-path I/O | 同一 host、同一 namespace、兩條以上獨立路徑 | 重點是 path redundancy |
| namespace sharing | 兩個以上 hosts 存取同一 shared namespace | 重點是 host ownership 與 coordination |
| SR-IOV | 一個 PCIe 裝置呈現 PF/VF | PCIe Function 不必等同獨立 subsystem |

**說明性範例。** 說明性範例：host A 經 controller 1 與 controller 2 都能存取 namespace X，這是 multi-path。host B 也經 controller 2 存取同一 namespace X，才同時構成 namespace sharing。NSID 在兩個 controller 上可能不同，因此跨 controller 比對時應先確認 namespace identity，而不是直接比較 NSID 數值。

**常見誤解／Debug。** Debug 圖上同時標出 object ID、owner 與 scope。『controller 看得到 NSID』只表示存在一條存取關係，不表示該 controller 擁有底層媒體，也不表示另一個 controller 使用相同 NSID。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§2.3.1，文件頁 26-33，PDF 頁 52-59; NVME-BASE-2.4 Rev. 2.4，§2.3.3，文件頁 33-35，PDF 頁 59-61; NVME-BASE-2.4 Rev. 2.4，§2.4.1，文件頁 35-37，PDF 頁 61-63; NVME-BASE-2.4 Rev. 2.4，§2.4.2，文件頁 37，PDF 頁 63

**關聯 Figure：** Figure 11, Figure 12, Figure 13, Figure 14, Figure 15, Figure 16, Figure 17, Figure 18, Figure 19, Figure 20, Figure 21, Figure 22

## 可追溯的規格重點

前面的 Mental Model 解釋因果；本節保留每個可追溯結論與 normative 強度，供講者備註與審查。

### 1. NVMe 規格家族的分工

<!-- claim:BASE12-FAMILY -->

Base Specification 定義通用 NVMe 協定；Transport Specification 綁定特定傳輸，I/O Command Set Specification 擴充命令與資料結構。這是適用關係，不是協定堆疊。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.1.1, 文件頁 1, PDF 頁 27

### 2. 規範性用語的強度

<!-- claim:BASE12-KEYWORDS -->

規格的 mandatory、may、optional、reserved、shall、should 各有固定語氣；詳細版保留英文 keyword，不能把 may 或 should 翻成 shall。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.4.1, 文件頁 2-3, PDF 頁 28-29

### 3. 進位與容量單位

<!-- claim:BASE12-NUMBERS -->

數值的解讀同時包含進位與單位；十六進位使用 h 後綴，二進位使用 b 後綴，十進位可省略 d。十進位與二進位容量前綴代表不同倍率。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.4.2, 文件頁 3-5, PDF 頁 29-31

### 4. byte、word 與 dword

<!-- claim:BASE12-DWORD -->

NVMe 以 byte、word、dword 表示欄位位置；一個 word 為 2 bytes，一個 dword 為 4 bytes。解欄位時先確認 byte 與 bit 編號。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.4.3, 文件頁 5, PDF 頁 31

### 5. PCIe queue pair 模型

<!-- claim:BASE12-QUEUE -->

PCIe memory-based model 把 Submission Queue 與 Completion Queue 配置在記憶體。多個 I/O Submission Queues 可共用一個 I/O Completion Queue；Admin queue pair 維持一對一。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.1, 文件頁 21-23, PDF 頁 47-49

### 6. NVM 儲存階層

<!-- claim:BASE12-STORAGE -->

儲存模型用 NVM subsystem、domain、Endurance Group、NVM Set／Reclaim Group、Reclaim Unit 與 namespace 表達包含關係。namespace 是 host 實際透過 controller 存取的格式化容量。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, 文件頁 26-33, PDF 頁 52-59

### 7. Admin 與 I/O Command Set

<!-- claim:BASE12-COMMANDSET -->

Admin Command Set 管理 controller 與 queue；I/O Command Set 定義對 namespace 的資料操作。Base 說明通用機制，個別 I/O Command Set Specification 說明命令語意。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.2, 文件頁 33, PDF 頁 59

### 8. subsystem 物件與 NSID

<!-- claim:BASE12-SUBSYSTEM -->

controller、port、namespace 與 PCI Function 是不同物件；NSID 是 controller 用來指向 namespace 的 handle，不是 namespace 本身。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.3, 文件頁 33-35, PDF 頁 59-61

### 9. multi-path 與 namespace sharing

<!-- claim:BASE12-MULTIPATH -->

multi-path I/O 是同一 host 到同一 namespace 的兩條以上獨立路徑；namespace sharing 是兩個以上 host 經不同 controller 存取同一 shared namespace。兩者都需要至少兩個 controller。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, 文件頁 35-37, PDF 頁 61-63

### 10. 非對稱路徑特性

<!-- claim:BASE12-ASYMMETRY -->

支援多路徑或共享時，各 controller 對同一 namespace 的存取特性不一定相同；host 可依 controller 所回報的狀態選擇路徑。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.4.2, 文件頁 37, PDF 頁 63

## Figure 索引

本報告介紹全部 18 張納入範圍的 Figure。100 分鐘簡報以 section 主線與必講 Figure 為主，其餘 Figure 仍完整保留作為附錄。

- [§1.1](#section-1-1)

- [§1.4](#section-1-4)

- [§2](#section-2)

- [§2.1](#section-2-1)

- [§2.3](#section-2-3)

- [§2.4](#section-2-4)

## Figure／欄位表教學參考

本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。欄位與 keyword 索引來自本機核對過的 PDF。

<a id="section-1-1"></a>

### §1.1

<details markdown="1">
<summary><strong>Figure 1: NVMe Family of Specifications</strong></summary>

<!-- claim:BASE12-FIG-001-CLAIM figure-table:BASE12-FIG-001 -->

**SPEC。** Figure 1〈NVMe Family of Specifications〉：定位〈NVMe Family of Specifications〉在 NVMe 文件與 command set 階層中的位置。 由共通 Base 要求往 transport 與 command set 分支閱讀，並分開核對：NVMe Family。

#### 這張 Figure 在完整流程中的位置

Figure 1 位於 §1.1.1，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVMe Family 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NVMe Family]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NVMe Family` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §1.1.1。
2. 依圖中指定的寬度與位置解碼 NVMe Family；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 1 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §1.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §1.1.1 如何排列 NVMe Family、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §1.1.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 1 對應的 raw value 或 buffer，標出包含 NVMe Family 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NVMe Family，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NVMe Family 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NVMe Family

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.1.1, Figure 1, 文件頁 1, PDF 頁 27

</details>

<a id="section-1-4"></a>

### §1.4

<details markdown="1">
<summary><strong>Figure 2: Decimal and Binary Units</strong></summary>

<!-- claim:BASE12-FIG-002-CLAIM figure-table:BASE12-FIG-002 -->

**SPEC。** Figure 2〈Decimal and Binary Units〉：定義〈Decimal and Binary Units〉使用的數值單位或 byte 寬度慣例。 分開十進位與二進位單位，並保留 byte／word／Dword 邊界；來源索引：Decimal and Binary Units。

#### 這張 Figure 在完整流程中的位置

Figure 2 位於 §1.4.2，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Decimal and Binary Units 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Decimal and Binary Units]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Decimal and Binary Units` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §1.4.2。
2. 依圖中指定的寬度與位置解碼 Decimal and Binary Units；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 2 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §1.4.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §1.4.2 如何排列 Decimal and Binary Units、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §1.4.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 2 對應的 raw value 或 buffer，標出包含 Decimal and Binary Units 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Decimal and Binary Units，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Decimal and Binary Units 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Decimal and Binary Units

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.4.2, Figure 2, 文件頁 3, PDF 頁 29

</details>

<details markdown="1">
<summary><strong>Figure 3: Byte, Word, and Dword Relationships</strong></summary>

<!-- claim:BASE12-FIG-003-CLAIM figure-table:BASE12-FIG-003 -->

**SPEC。** Figure 3〈Byte, Word, and Dword Relationships〉：定義〈Byte, Word, and Dword Relationships〉使用的數值單位或 byte 寬度慣例。 分開十進位與二進位單位，並保留 byte／word／Dword 邊界；來源索引：Byte, Word, and Dword Relationships。

#### 這張 Figure 在完整流程中的位置

Figure 3 位於 §1.4.3，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Byte, Word, and Dword Relationships 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Byte, Word, and Dword Relationships]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Byte, Word, and Dword Relationships` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §1.4.3。
2. 依圖中指定的寬度與位置解碼 Byte, Word, and Dword Relationships；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 3 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §1.4.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §1.4.3 如何排列 Byte, Word, and Dword Relationships、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §1.4.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 3 對應的 raw value 或 buffer，標出包含 Byte, Word, and Dword Relationships 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Byte, Word, and Dword Relationships，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Byte, Word, and Dword Relationships 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Byte, Word, and Dword Relationships

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.4.3, Figure 3, 文件頁 5, PDF 頁 31

</details>

<a id="section-2"></a>

### §2

<details markdown="1">
<summary><strong>Figure 5: Types of NVMe Command Sets</strong></summary>

<!-- claim:BASE12-FIG-005-CLAIM figure-table:BASE12-FIG-005 -->

**SPEC。** Figure 5〈Types of NVMe Command Sets〉：定位〈Types of NVMe Command Sets〉在 NVMe 文件與 command set 階層中的位置。 由共通 Base 要求往 transport 與 command set 分支閱讀，並分開核對：Command Set, Command。

#### 這張 Figure 在完整流程中的位置

Figure 5 位於 §2，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Command Set 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Command Set]
          ↓
[擷取欄位: Command] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Command Set` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Command` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §2。
2. 依圖中指定的寬度與位置解碼 Command Set；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Command 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 5 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §2 如何排列 Command Set、Command 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 5 對應的 raw value 或 buffer，標出包含 Command Set 的 bytes 並解碼，再獨立核對 Command。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Command Set，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Command Set 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Command 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Command Set, Command

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2, Figure 5, 文件頁 21, PDF 頁 47

</details>

<a id="section-2-1"></a>

### §2.1

<details markdown="1">
<summary><strong>Figure 6: Queue Pair Example, 1:1 Mapping</strong></summary>

<!-- claim:BASE12-FIG-006-CLAIM figure-table:BASE12-FIG-006 -->

**SPEC。** Figure 6〈Queue Pair Example, 1:1 Mapping〉：呈現〈Queue Pair Example, 1:1 Mapping〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：Queue Pair, 1:1。

#### 這張 Figure 在完整流程中的位置

Figure 6 位於 §2.1，在本流程中是「queue」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Queue Pair 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 queue／command flow 圖。先標 host 與 controller 的 ownership，再追 head、tail、phase 或 arbitration 的改變；箭頭代表狀態或 ownership 轉移，不自動代表 command 已完成。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Queue Pair]
          ↓
[擷取欄位: 1:1] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Queue Pair` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `1:1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §2.1。
2. 依圖中指定的寬度與位置解碼 Queue Pair；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 1:1 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 6 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §2.1 如何排列 Queue Pair、1:1 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §2.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 6 對應的 raw value 或 buffer，標出包含 Queue Pair 的 bytes 並解碼，再獨立核對 1:1。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Queue Pair，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Queue Pair 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 1:1 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Queue Pair, 1:1

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.1, Figure 6, 文件頁 22, PDF 頁 48

</details>

<details markdown="1">
<summary><strong>Figure 7: Queue Pair Example, n:1 Mapping</strong></summary>

<!-- claim:BASE12-FIG-007-CLAIM figure-table:BASE12-FIG-007 -->

**SPEC。** Figure 7〈Queue Pair Example, n:1 Mapping〉：呈現〈Queue Pair Example, n:1 Mapping〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：Queue Pair。

#### 這張 Figure 在完整流程中的位置

Figure 7 位於 §2.1，在本流程中是「queue」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Queue Pair 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 queue／command flow 圖。先標 host 與 controller 的 ownership，再追 head、tail、phase 或 arbitration 的改變；箭頭代表狀態或 ownership 轉移，不自動代表 command 已完成。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Queue Pair]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Queue Pair` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §2.1。
2. 依圖中指定的寬度與位置解碼 Queue Pair；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 7 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §2.1 如何排列 Queue Pair、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §2.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 7 對應的 raw value 或 buffer，標出包含 Queue Pair 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Queue Pair，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Queue Pair 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Queue Pair

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.1, Figure 7, 文件頁 22, PDF 頁 48

</details>

<a id="section-2-3"></a>

### §2.3

<details markdown="1">
<summary><strong>Figure 11: Simple NVM Storage Hierarchy with NVM Sets</strong></summary>

<!-- claim:BASE12-FIG-011-CLAIM figure-table:BASE12-FIG-011 -->

**SPEC。** Figure 11〈Simple NVM Storage Hierarchy with NVM Sets〉：呈現〈Simple NVM Storage Hierarchy with NVM Sets〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Storage Hierarchy, NVM Set。

#### 這張 Figure 在完整流程中的位置

Figure 11 位於 §2.3.1，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Storage Hierarchy 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NVM Storage Hierarchy]
          ↓
[擷取欄位: NVM Set] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NVM Storage Hierarchy` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NVM Set` | NVM Set，把 namespace 與一組共同管理的 NVM 資源建立關聯的容量集合。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §2.3.1。
2. 依圖中指定的寬度與位置解碼 NVM Storage Hierarchy；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NVM Set 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 11 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §2.3.1 如何排列 NVM Storage Hierarchy、NVM Set 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §2.3.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 11 對應的 raw value 或 buffer，標出包含 NVM Storage Hierarchy 的 bytes 並解碼，再獨立核對 NVM Set。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NVM Storage Hierarchy，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NVM Storage Hierarchy 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NVM Set 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NVM Storage Hierarchy, NVM Set

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 11, 文件頁 27, PDF 頁 53

</details>

<details markdown="1">
<summary><strong>Figure 12: Simple NVM Storage Hierarchy with One Reclaim Group</strong></summary>

<!-- claim:BASE12-FIG-012-CLAIM figure-table:BASE12-FIG-012 -->

**SPEC。** Figure 12〈Simple NVM Storage Hierarchy with One Reclaim Group〉：呈現〈Simple NVM Storage Hierarchy with One Reclaim Group〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Storage Hierarchy, Reclaim Group。

#### 這張 Figure 在完整流程中的位置

Figure 12 位於 §2.3.1，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Storage Hierarchy 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NVM Storage Hierarchy]
          ↓
[擷取欄位: Reclaim Group] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NVM Storage Hierarchy` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Reclaim Group` | Reclaim Group，具有共同回收行為的一組非揮發性儲存資源。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §2.3.1。
2. 依圖中指定的寬度與位置解碼 NVM Storage Hierarchy；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Reclaim Group 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 12 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §2.3.1 如何排列 NVM Storage Hierarchy、Reclaim Group 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §2.3.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 12 對應的 raw value 或 buffer，標出包含 NVM Storage Hierarchy 的 bytes 並解碼，再獨立核對 Reclaim Group。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NVM Storage Hierarchy，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NVM Storage Hierarchy 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Reclaim Group 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NVM Storage Hierarchy, Reclaim Group

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 12, 文件頁 28, PDF 頁 54

</details>

<details markdown="1">
<summary><strong>Figure 13: Simple NVM Storage Hierarchy with Multiple Reclaim Groups</strong></summary>

<!-- claim:BASE12-FIG-013-CLAIM figure-table:BASE12-FIG-013 -->

**SPEC。** Figure 13〈Simple NVM Storage Hierarchy with Multiple Reclaim Groups〉：呈現〈Simple NVM Storage Hierarchy with Multiple Reclaim Groups〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Storage Hierarchy, Reclaim Group。

#### 這張 Figure 在完整流程中的位置

Figure 13 位於 §2.3.1，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Storage Hierarchy 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NVM Storage Hierarchy]
          ↓
[擷取欄位: Reclaim Group] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NVM Storage Hierarchy` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Reclaim Group` | Reclaim Group，具有共同回收行為的一組非揮發性儲存資源。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §2.3.1。
2. 依圖中指定的寬度與位置解碼 NVM Storage Hierarchy；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Reclaim Group 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 13 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §2.3.1 如何排列 NVM Storage Hierarchy、Reclaim Group 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §2.3.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 13 對應的 raw value 或 buffer，標出包含 NVM Storage Hierarchy 的 bytes 並解碼，再獨立核對 Reclaim Group。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NVM Storage Hierarchy，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NVM Storage Hierarchy 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Reclaim Group 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NVM Storage Hierarchy, Reclaim Group

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 13, 文件頁 29, PDF 頁 55

</details>

<details markdown="1">
<summary><strong>Figure 14: Complex NVM Storage Hierarchy with NVM Sets</strong></summary>

<!-- claim:BASE12-FIG-014-CLAIM figure-table:BASE12-FIG-014 -->

**SPEC。** Figure 14〈Complex NVM Storage Hierarchy with NVM Sets〉：呈現〈Complex NVM Storage Hierarchy with NVM Sets〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Storage Hierarchy, NVM Set。

#### 這張 Figure 在完整流程中的位置

Figure 14 位於 §2.3.1，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Storage Hierarchy 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NVM Storage Hierarchy]
          ↓
[擷取欄位: NVM Set] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NVM Storage Hierarchy` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NVM Set` | NVM Set，把 namespace 與一組共同管理的 NVM 資源建立關聯的容量集合。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §2.3.1。
2. 依圖中指定的寬度與位置解碼 NVM Storage Hierarchy；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NVM Set 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 14 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §2.3.1 如何排列 NVM Storage Hierarchy、NVM Set 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §2.3.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 14 對應的 raw value 或 buffer，標出包含 NVM Storage Hierarchy 的 bytes 並解碼，再獨立核對 NVM Set。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NVM Storage Hierarchy，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NVM Storage Hierarchy 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NVM Set 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NVM Storage Hierarchy, NVM Set

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 14, 文件頁 30, PDF 頁 56

</details>

<details markdown="1">
<summary><strong>Figure 15: Complex NVM Storage Hierarchy with Multiple Reclaim Groups</strong></summary>

<!-- claim:BASE12-FIG-015-CLAIM figure-table:BASE12-FIG-015 -->

**SPEC。** Figure 15〈Complex NVM Storage Hierarchy with Multiple Reclaim Groups〉：呈現〈Complex NVM Storage Hierarchy with Multiple Reclaim Groups〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Storage Hierarchy, Reclaim Group。

#### 這張 Figure 在完整流程中的位置

Figure 15 位於 §2.3.1，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Storage Hierarchy 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NVM Storage Hierarchy]
          ↓
[擷取欄位: Reclaim Group] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NVM Storage Hierarchy` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Reclaim Group` | Reclaim Group，具有共同回收行為的一組非揮發性儲存資源。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §2.3.1。
2. 依圖中指定的寬度與位置解碼 NVM Storage Hierarchy；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Reclaim Group 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 15 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §2.3.1 如何排列 NVM Storage Hierarchy、Reclaim Group 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §2.3.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 15 對應的 raw value 或 buffer，標出包含 NVM Storage Hierarchy 的 bytes 並解碼，再獨立核對 Reclaim Group。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NVM Storage Hierarchy，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NVM Storage Hierarchy 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Reclaim Group 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NVM Storage Hierarchy, Reclaim Group

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 15, 文件頁 31, PDF 頁 57

</details>

<details markdown="1">
<summary><strong>Figure 16: Single-Namespace NVM Subsystem</strong></summary>

<!-- claim:BASE12-FIG-016-CLAIM figure-table:BASE12-FIG-016 -->

**SPEC。** Figure 16〈Single-Namespace NVM Subsystem〉：呈現〈Single-Namespace NVM Subsystem〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, Namespace。

#### 這張 Figure 在完整流程中的位置

Figure 16 位於 §2.3.3，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Subsystem 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NVM Subsystem]
          ↓
[擷取欄位: Namespace] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NVM Subsystem` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Namespace` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §2.3.3。
2. 依圖中指定的寬度與位置解碼 NVM Subsystem；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Namespace 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 16 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.3.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §2.3.3 如何排列 NVM Subsystem、Namespace 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §2.3.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 16 對應的 raw value 或 buffer，標出包含 NVM Subsystem 的 bytes 並解碼，再獨立核對 Namespace。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 Namespace 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NVM Subsystem, Namespace

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 16, 文件頁 32, PDF 頁 58

</details>

<details markdown="1">
<summary><strong>Figure 17: Two-Namespace NVM Subsystem</strong></summary>

<!-- claim:BASE12-FIG-017-CLAIM figure-table:BASE12-FIG-017 -->

**SPEC。** Figure 17〈Two-Namespace NVM Subsystem〉：呈現〈Two-Namespace NVM Subsystem〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, Namespace。

#### 這張 Figure 在完整流程中的位置

Figure 17 位於 §2.3.3，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Subsystem 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NVM Subsystem]
          ↓
[擷取欄位: Namespace] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NVM Subsystem` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Namespace` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §2.3.3。
2. 依圖中指定的寬度與位置解碼 NVM Subsystem；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Namespace 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 17 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.3.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §2.3.3 如何排列 NVM Subsystem、Namespace 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §2.3.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 17 對應的 raw value 或 buffer，標出包含 NVM Subsystem 的 bytes 並解碼，再獨立核對 Namespace。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 Namespace 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NVM Subsystem, Namespace

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 17, 文件頁 33, PDF 頁 59

</details>

<details markdown="1">
<summary><strong>Figure 18: Complex NVM Subsystem</strong></summary>

<!-- claim:BASE12-FIG-018-CLAIM figure-table:BASE12-FIG-018 -->

**SPEC。** Figure 18〈Complex NVM Subsystem〉：呈現〈Complex NVM Subsystem〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem。

#### 這張 Figure 在完整流程中的位置

Figure 18 位於 §2.3.3，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Subsystem 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

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

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §2.3.3。
2. 依圖中指定的寬度與位置解碼 NVM Subsystem；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 18 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.3.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §2.3.3 如何排列 NVM Subsystem、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §2.3.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 18 對應的 raw value 或 buffer，標出包含 NVM Subsystem 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 18, 文件頁 34, PDF 頁 60

</details>

<a id="section-2-4"></a>

### §2.4

<details markdown="1">
<summary><strong>Figure 19: NVM Express Controller with Two Namespaces</strong></summary>

<!-- claim:BASE12-FIG-019-CLAIM figure-table:BASE12-FIG-019 -->

**SPEC。** Figure 19〈NVM Express Controller with Two Namespaces〉：呈現〈NVM Express Controller with Two Namespaces〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：Namespace, Controller。

#### 這張 Figure 在完整流程中的位置

Figure 19 位於 §2.4.1，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Namespace 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Namespace]
          ↓
[擷取欄位: Controller] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Namespace` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Controller` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §2.4.1。
2. 依圖中指定的寬度與位置解碼 Namespace；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Controller 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 19 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.4.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §2.4.1 如何排列 Namespace、Controller 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §2.4.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 19 對應的 raw value 或 buffer，標出包含 Namespace 的 bytes 並解碼，再獨立核對 Controller。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Namespace，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Namespace 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Controller 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Namespace, Controller

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 19, 文件頁 35, PDF 頁 61

</details>

<details markdown="1">
<summary><strong>Figure 20: NVM Subsystem with Two Controllers and One Port</strong></summary>

<!-- claim:BASE12-FIG-020-CLAIM figure-table:BASE12-FIG-020 -->

**SPEC。** Figure 20〈NVM Subsystem with Two Controllers and One Port〉：呈現〈NVM Subsystem with Two Controllers and One Port〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, Controller。

#### 這張 Figure 在完整流程中的位置

Figure 20 位於 §2.4.1，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Subsystem 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NVM Subsystem]
          ↓
[擷取欄位: Controller] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NVM Subsystem` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Controller` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §2.4.1。
2. 依圖中指定的寬度與位置解碼 NVM Subsystem；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Controller 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 20 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.4.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §2.4.1 如何排列 NVM Subsystem、Controller 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §2.4.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 20 對應的 raw value 或 buffer，標出包含 NVM Subsystem 的 bytes 並解碼，再獨立核對 Controller。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 Controller 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NVM Subsystem, Controller

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 20, 文件頁 35, PDF 頁 61

</details>

<details markdown="1">
<summary><strong>Figure 21: NVM Subsystem with Two Controllers and Two Ports</strong></summary>

<!-- claim:BASE12-FIG-021-CLAIM figure-table:BASE12-FIG-021 -->

**SPEC。** Figure 21〈NVM Subsystem with Two Controllers and Two Ports〉：呈現〈NVM Subsystem with Two Controllers and Two Ports〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, Controller。

#### 這張 Figure 在完整流程中的位置

Figure 21 位於 §2.4.1，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Subsystem 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NVM Subsystem]
          ↓
[擷取欄位: Controller] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NVM Subsystem` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Controller` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §2.4.1。
2. 依圖中指定的寬度與位置解碼 NVM Subsystem；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Controller 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 21 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.4.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §2.4.1 如何排列 NVM Subsystem、Controller 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §2.4.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 21 對應的 raw value 或 buffer，標出包含 NVM Subsystem 的 bytes 並解碼，再獨立核對 Controller。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 Controller 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NVM Subsystem, Controller

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 21, 文件頁 36, PDF 頁 62

</details>

<details markdown="1">
<summary><strong>Figure 22: PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)</strong></summary>

<!-- claim:BASE12-FIG-022-CLAIM figure-table:BASE12-FIG-022 -->

**SPEC。** Figure 22〈PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)〉：呈現〈PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)〉中 Physical Function 與 Virtual Function 的關係。 分開 PCIe Function identity、controller ownership 與 shared device resource；來源索引：SR, IOV。

#### 這張 Figure 在完整流程中的位置

Figure 22 位於 §2.4.1，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SR]
          ↓
[擷取欄位: IOV] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `IOV` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §2.4.1。
2. 依圖中指定的寬度與位置解碼 SR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 IOV 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 22 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.4.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §2.4.1 如何排列 SR、IOV 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §2.4.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 22 對應的 raw value 或 buffer，標出包含 SR 的 bytes 並解碼，再獨立核對 IOV。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SR，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SR 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 IOV 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SR, IOV

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 22, 文件頁 37, PDF 頁 63

</details>

## 使用與限制

製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata 集合或核准範圍改變時，必須重新核對受影響 claim。
