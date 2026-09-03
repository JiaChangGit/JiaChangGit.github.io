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
[English]({% post_url 2026-08-28-nvme-base-ch3-en %})


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

## 先學縮寫：完整 Glossary

下列縮寫會在投影片主線使用前先定義。縮寫本身永遠不夠；設計與 Debug 還要保留 owner、width、unit、scope 與 state。

| 縮寫／名詞 | 白話解釋 | 來源 |
|---|---|---|
| `controller` | controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。 | NVME-BASE-2.4 Rev. 2.4，§3.1.3-3.1.3.2，文件頁 39-43，PDF 頁 65-69 |
| `I/O controller` | I/O controller，可執行使用者資料 I/O command 的 controller 類型。 | NVME-BASE-2.4 Rev. 2.4，§3.1.3-3.1.3.2，文件頁 39-43，PDF 頁 65-69 |
| `Administrative controller` | Administrative controller，以管理為目的且不執行使用者資料 I/O command 的 controller 類型。 | NVME-BASE-2.4 Rev. 2.4，§3.1.3-3.1.3.2，文件頁 39-43，PDF 頁 65-69 |
| `CAP` | Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 | NVME-BASE-2.4 Rev. 2.4，§3.5.1, 3.5.3-3.5.4，文件頁 105-113，PDF 頁 131-139 |
| `CC` | Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 | NVME-BASE-2.4 Rev. 2.4，§3.5.1, 3.5.3-3.5.4，文件頁 105-113，PDF 頁 131-139 |
| `CSTS` | Controller Status，controller 回報 ready、fatal status 與 shutdown 狀態的 property。 | NVME-BASE-2.4 Rev. 2.4，§3.5.1, 3.5.3-3.5.4，文件頁 105-113，PDF 頁 131-139 |
| `EN` | Enable，CC 中控制 controller enable state 的 bit。 | NVME-BASE-2.4 Rev. 2.4，§3.5.1, 3.5.3-3.5.4，文件頁 105-113，PDF 頁 131-139 |
| `RDY` | Ready，CSTS 中表示 controller 是否已準備正常處理 command 的 bit。 | NVME-BASE-2.4 Rev. 2.4，§3.5.1, 3.5.3-3.5.4，文件頁 105-113，PDF 頁 131-139 |
| `AQA` | Admin Queue Attributes，描述 Admin SQ 與 Admin CQ 大小的 property。 | NVME-BASE-2.4 Rev. 2.4，§3.5.1, 3.5.3-3.5.4，文件頁 105-113，PDF 頁 131-139 |
| `ASQ` | Admin Submission Queue Base Address，Admin SQ 在可定址記憶體中的基底位址。 | NVME-BASE-2.4 Rev. 2.4，§3.5.1, 3.5.3-3.5.4，文件頁 105-113，PDF 頁 131-139 |
| `ACQ` | Admin Completion Queue Base Address，Admin CQ 在可定址記憶體中的基底位址。 | NVME-BASE-2.4 Rev. 2.4，§3.5.1, 3.5.3-3.5.4，文件頁 105-113，PDF 頁 131-139 |
| `NSID` | Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。 | NVME-BASE-2.4 Rev. 2.4，§3.2.1，文件頁 78-80，PDF 頁 104-106 |
| `NSSR` | NVM Subsystem Reset，觸發 NVM subsystem reset 的 property。 | NVME-BASE-2.4 Rev. 2.4，§3.7，文件頁 120-125，PDF 頁 146-151 |
| `NSSD` | NVM Subsystem Shutdown，控制較大範圍 subsystem shutdown 的 property。 | NVME-BASE-2.4 Rev. 2.4，§3.6.1, 3.6.3，文件頁 113-120，PDF 頁 139-146 |
| `SHN` | Shutdown Notification，CC 中由 host 宣告 shutdown 類型的欄位。 | NVME-BASE-2.4 Rev. 2.4，§3.6.1, 3.6.3，文件頁 113-120，PDF 頁 139-146 |
| `SHST` | Shutdown Status，CSTS 中由 controller 回報 shutdown 進度的欄位。 | NVME-BASE-2.4 Rev. 2.4，§3.6.1, 3.6.3，文件頁 113-120，PDF 頁 139-146 |
| `CRTO` | Controller Ready Timeouts，回報特定 ready mode 所需等待時間的 property。 | NVME-BASE-2.4 Rev. 2.4，§3.5.1, 3.5.3-3.5.4，文件頁 105-113，PDF 頁 131-139 |
| `CMB` | Controller Memory Buffer，controller 提供、可放置部分 queue 或資料結構的記憶體區域。 | NVME-BASE-2.4 Rev. 2.4，§3.1.4，文件頁 52-54，PDF 頁 78-80 |
| `PMR` | Persistent Memory Region，由 controller 暴露、具有持久性語意的記憶體區域。 | NVME-BASE-2.4 Rev. 2.4，§3.1.4，文件頁 52-54，PDF 頁 78-80 |
| `BIR` | BAR Indicator Register，指出某個記憶體結構位於哪一個 PCIe BAR。 | NVME-BASE-2.4 Rev. 2.4，§3.1.4，文件頁 52-54，PDF 頁 78-80 |
| `MPS` | Memory Page Size，controller 使用的 memory page 大小設定；影響 queue address 與 PRP 對齊。 | NVME-BASE-2.4 Rev. 2.4，§3.3.1，文件頁 88-91，PDF 頁 114-117 |
| `KATO` | Keep Alive Timeout，host 與 controller 約定的存活逾時設定。 | NVME-BASE-2.4 Rev. 2.4，§3.9，文件頁 129-135，PDF 頁 155-161 |
| `KATT` | Keep Alive Timeout Total，controller 用於偵測逾時的總時間基準。 | NVME-BASE-2.4 Rev. 2.4，§3.9，文件頁 129-135，PDF 頁 155-161 |
| `FDP` | Flexible Data Placement，把資料放置提示與媒體回收管理連結的能力。 | NVME-BASE-2.4 Rev. 2.4，§3.2.2-3.2.4，文件頁 80-85，PDF 頁 106-111 |
| `NVM Set` | NVM Set，把 namespace 與一組共同管理的 NVM 資源建立關聯的容量集合。 | NVME-BASE-2.4 Rev. 2.4，§3.2.2-3.2.4，文件頁 80-85，PDF 頁 106-111 |
| `Endurance Group` | Endurance Group，用於隔離與回報耐久度相關狀態的 NVM 資源群組。 | NVME-BASE-2.4 Rev. 2.4，§3.2.2-3.2.4，文件頁 80-85，PDF 頁 106-111 |
| `Reclaim Group` | Reclaim Group，具有共同回收行為的一組非揮發性儲存資源。 | NVME-BASE-2.4 Rev. 2.4，§3.2.2-3.2.4，文件頁 80-85，PDF 頁 106-111 |
| `Reclaim Unit` | Reclaim Unit，controller 執行媒體回收時使用的較小管理粒度。 | NVME-BASE-2.4 Rev. 2.4，§3.2.2-3.2.4，文件頁 80-85，PDF 頁 106-111 |
| `NVM subsystem` | NVM subsystem，包含 controller、port、namespace 與非揮發性儲存資源的 NVMe 系統邊界。 | NVME-BASE-2.4 Rev. 2.4，§3.2.5，文件頁 85-88，PDF 頁 111-114 |

## Visual Atlas：先用圖建立整體位置

每張教學重畫回答不同問題：Architecture 定位元件、Sequence 顯示 ownership、Decode 把 bits 轉成工程值、State 保留 failure evidence；它們不是 Spec 原圖的複製。

### Visual 01: 先分清 controller 類型、ID 與能力

**View type:** `architecture`

```text
[辨識 controller type]
  ├─ [取得 Controller ID]
  ├─ [查 command/log/feature support row]
  └─ [建立允許操作集合]
```

**回答的問題：** Controller type 回答『能做哪類工作』，Controller ID 回答『這是哪一個 controller』，support-requirement Figure 回答『在這個上下文中 command／log／feature 的支援強度』。Figures 23-32 應連續閱讀，但三種問題不能合併成一個布林值。

**支援 Figure：** Figure 23, Figure 24, Figure 25, Figure 26, Figure 27, Figure 28, Figure 30, Figure 31, Figure 32

**來源：** NVME-BASE-2.4 Rev. 2.4，§3.1.1，文件頁 38，PDF 頁 64; NVME-BASE-2.4 Rev. 2.4，§3.1.3-3.1.3.2，文件頁 39-43，PDF 頁 65-69; NVME-BASE-2.4 Rev. 2.4，§3.1.3，文件頁 40，PDF 頁 66

### Visual 02: 從 CAP 到 CSTS.RDY：初始化是一條有前置條件的狀態機

**View type:** `state`

```text
[讀 CAP／VS] → [配置 AQA、ASQ、ACQ] → [設定 CC 欄位] → [寫 CC.EN=1] → [等待 CSTS.RDY=1 或 timeout]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**回答的問題：** Properties 不是彼此獨立的 register 清單。CAP 先限制 page size、queue 與 timeout 能力；AQA、ASQ、ACQ 建立 Admin queues；CC 選擇設定並以 EN 啟動；最後由 CSTS.RDY 宣告 controller 已能正常處理命令。Figures 33-46 與 Figure 57 應沿這條因果鏈閱讀。

**支援 Figure：** Figure 33, Figure 34, Figure 36, Figure 37, Figure 38, Figure 41, Figure 42, Figure 44, Figure 45, Figure 46, Figure 57

**來源：** NVME-BASE-2.4 Rev. 2.4，§3.1.4，文件頁 52-54，PDF 頁 78-80; NVME-BASE-2.4 Rev. 2.4，§3.5.1, 3.5.3-3.5.4，文件頁 105-113，PDF 頁 131-139

### Visual 03: Ring buffer、doorbell 與 arbitration 要分三層理解

**View type:** `sequence`

```text
Host / software        Shared object        Controller / evidence
Host → Shared: host 寫 SQE
Shared → Controller: host 推進 tail
Controller → Shared: arbiter 選 SQ
Shared → Host: controller 推進 SQ head
Host → Shared: controller 發 CQE
Shared → Controller: host 推進 CQ head
```

**回答的問題：** Figure 73/74 說明 queue 的 empty/full 判定，Figure 80/81 說明多個 SQ 競爭 controller 服務時的 arbitration。前者處理單一 ring 的 head/tail 狀態，後者處理多個 candidate SQ 的選擇；priority 屬於 SQ，不是每筆 command 自帶的獨立優先權。

**支援 Figure：** Figure 73, Figure 74, Figure 80, Figure 81

**來源：** NVME-BASE-2.4 Rev. 2.4，§3.3.1，文件頁 88-91，PDF 頁 114-117; NVME-BASE-2.4 Rev. 2.4，§3.4.1-3.4.5，文件頁 101-105，PDF 頁 127-131; NVME-BASE-2.4 Rev. 2.4，§3.1.3，文件頁 40，PDF 頁 66

### Visual 04: CMB、PMR、capacity 與 namespace 是不同資源視角

**View type:** `architecture`

```text
[辨識資源類型]
  ├─ [由 BIR 找 BAR]
  ├─ [核對 enable/status]
  ├─ [依用途放置資料]
  └─ [另外追蹤 namespace/capacity 階層]
```

**回答的問題：** CMB/PMR properties 描述 controller 暴露的 memory region 位置、能力與狀態；capacity Figures 86-89 描述 NVM subsystem 各層級可用或已配置容量。兩者都談 memory，卻不是同一種空間，也不能用同一個『剩餘容量』欄位合併。

**支援 Figure：** Figure 47, Figure 48, Figure 52, Figure 53, Figure 54, Figure 55, Figure 58, Figure 59, Figure 60, Figure 61, Figure 62, Figure 63, Figure 64, Figure 86, Figure 87, Figure 88, Figure 89

**來源：** NVME-BASE-2.4 Rev. 2.4，§3.1.4，文件頁 52-54，PDF 頁 78-80; NVME-BASE-2.4 Rev. 2.4，§3.8，文件頁 125-129，PDF 頁 151-155; NVME-BASE-2.4 Rev. 2.4，§3.2.2-3.2.4，文件頁 80-85，PDF 頁 106-111

### Visual 05: Shutdown、reset、Keep Alive 與 firmware update 的 recovery 邊界

**View type:** `state`

```text
[辨識事件來源] → [決定影響 scope] → [停止新工作] → [等待狀態／timeout] → [重建被清除的資源] → [驗證可恢復 I/O]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**回答的問題：** Lifecycle 事件的共同問題是『哪一層狀態仍有效』。Normal shutdown 由 CC.SHN/CSTS.SHST 協調，reset 分成 subsystem/controller/queue 層級，Keep Alive 監測 host-controller 存活，firmware activation 又可能要求特定 reset。相同的『暫時無法處理 command』症狀，不代表可以使用相同 recovery。

**支援 Figure：** Figure 43, Figure 56, Figure 84, Figure 85, Figure 90, Figure 91

**來源：** NVME-BASE-2.4 Rev. 2.4，§3.6.1, 3.6.3，文件頁 113-120，PDF 頁 139-146; NVME-BASE-2.4 Rev. 2.4，§3.7，文件頁 120-125，PDF 頁 146-151; NVME-BASE-2.4 Rev. 2.4，§3.9，文件頁 129-135，PDF 頁 155-161; NVME-BASE-2.4 Rev. 2.4，§3.10-3.11，文件頁 135-138，PDF 頁 161-164

## Mental Model 與完整教學流程

以下依工程因果而非 Spec section 排列；相關 Figure 會回到它支援的流程節點，不以編號順序取代教學故事線。

### Module 01: 先分清 controller 類型、ID 與能力

**解釋。** Controller type 回答『能做哪類工作』，Controller ID 回答『這是哪一個 controller』，support-requirement Figure 回答『在這個上下文中 command／log／feature 的支援強度』。Figures 23-32 應連續閱讀，但三種問題不能合併成一個布林值。

```text
辨識 controller type
  ↓
取得 Controller ID
  ↓
查 command/log/feature support row
  ↓
建立允許操作集合
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| I/O controller | 可執行使用者資料 I/O | 仍需逐項查 optional capability |
| Administrative controller | 管理用途、無資料 I/O command | 不能因有 Admin Queue 就當成 I/O controller |
| support marker | 針對 row 與上下文描述強度 | 不能脫離 column／footnote 解讀 |

**說明性範例。** 說明性範例：偵測到一個 Administrative controller 時，軟體仍會建立 Admin SQ/CQ 並執行管理 command，但不應把 namespace data path 掛到它。若只用『存在 Admin Queue』判斷 controller type，I/O 與 Administrative controller 會被錯誤歸成同類。

**常見誤解／Debug。** 能力矩陣解析器要保留 row、column、footnote 與 controller type 四個維度。把 O、M 或條件註記抽成全域 capability，會在另一種 controller 或 command-set context 中得到錯誤結論。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§3.1.1，文件頁 38，PDF 頁 64; NVME-BASE-2.4 Rev. 2.4，§3.1.3-3.1.3.2，文件頁 39-43，PDF 頁 65-69; NVME-BASE-2.4 Rev. 2.4，§3.1.3，文件頁 40，PDF 頁 66

**關聯 Figure：** Figure 23, Figure 24, Figure 25, Figure 26, Figure 27, Figure 28, Figure 30, Figure 31, Figure 32

### Module 02: 從 CAP 到 CSTS.RDY：初始化是一條有前置條件的狀態機

**解釋。** Properties 不是彼此獨立的 register 清單。CAP 先限制 page size、queue 與 timeout 能力；AQA、ASQ、ACQ 建立 Admin queues；CC 選擇設定並以 EN 啟動；最後由 CSTS.RDY 宣告 controller 已能正常處理命令。Figures 33-46 與 Figure 57 應沿這條因果鏈閱讀。

```text
讀 CAP／VS
  ↓
配置 AQA、ASQ、ACQ
  ↓
設定 CC 欄位
  ↓
寫 CC.EN=1
  ↓
等待 CSTS.RDY=1 或 timeout
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| CAP | 能力與界限 | 在寫設定前讀 |
| AQA/ASQ/ACQ | Admin queue 大小與位址 | 需符合 page/alignment 能力 |
| CC | host 選擇與 enable | 寫入值要與 CAP 相容 |
| CSTS | controller 回報狀態 | RDY/CFS/SHST 不可互相替代 |

**說明性範例。** 說明性範例：host 選擇 4 KiB MPS，ASQ 與 ACQ base address 因而必須依該 page size 對齊。寫 CC.EN=1 後，host 以 CAP／CRTO 指定的時間界限等待 CSTS.RDY=1；若 CFS 先出現，流程應進入 error recovery，而不是繼續建立 I/O queues。

**常見誤解／Debug。** 初始化 log 至少保留每次 property access 的 offset、width、raw value 與 timestamp。只記『enable failed』無法分辨不相容設定、位址對齊、CFS 或單純尚未超過 ready timeout。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§3.1.4，文件頁 52-54，PDF 頁 78-80; NVME-BASE-2.4 Rev. 2.4，§3.5.1, 3.5.3-3.5.4，文件頁 105-113，PDF 頁 131-139

**關聯 Figure：** Figure 33, Figure 34, Figure 36, Figure 37, Figure 38, Figure 41, Figure 42, Figure 44, Figure 45, Figure 46, Figure 57

### Module 03: Ring buffer、doorbell 與 arbitration 要分三層理解

**解釋。** Figure 73/74 說明 queue 的 empty/full 判定，Figure 80/81 說明多個 SQ 競爭 controller 服務時的 arbitration。前者處理單一 ring 的 head/tail 狀態，後者處理多個 candidate SQ 的選擇；priority 屬於 SQ，不是每筆 command 自帶的獨立優先權。

```text
host 寫 SQE
  ↓
host 推進 tail
  ↓
arbiter 選 SQ
  ↓
controller 推進 SQ head
  ↓
controller 發 CQE
  ↓
host 推進 CQ head
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| empty | head == tail 且 phase／ownership 符合 empty 定義 | 沒有可取走 entry |
| full | 下一個 tail 會追上尚未釋放 head | host 不得覆寫 entry |
| Round Robin | 候選 SQ 輪流取得服務 | 不代表 command completion 依提交順序 |
| Weighted RR + Urgent | priority class 與 weight 影響選擇 | 仍需依適用設定解讀 |

**說明性範例。** 說明性範例：深度 4 的 SQ 只有四個 slot，但 full/empty 判定還需要 ownership 規則；不能只用 tail-head 的無號差值。若 SQ 1 與 SQ 2 同時有 command，arbiter 先選 SQ 2 也不代表 SQ 2 的 command 一定先完成，因 command 執行時間仍可能不同。

**常見誤解／Debug。** Debug 時分開記錄 software tail、doorbell value、controller-consumed head 與 completion SQHD。四個值混成一個『queue index』會遮蔽 lost doorbell、stale head、slot reuse 與 arbitration starvation 等不同根因。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§3.3.1，文件頁 88-91，PDF 頁 114-117; NVME-BASE-2.4 Rev. 2.4，§3.4.1-3.4.5，文件頁 101-105，PDF 頁 127-131; NVME-BASE-2.4 Rev. 2.4，§3.1.3，文件頁 40，PDF 頁 66

**關聯 Figure：** Figure 73, Figure 74, Figure 80, Figure 81

### Module 04: CMB、PMR、capacity 與 namespace 是不同資源視角

**解釋。** CMB/PMR properties 描述 controller 暴露的 memory region 位置、能力與狀態；capacity Figures 86-89 描述 NVM subsystem 各層級可用或已配置容量。兩者都談 memory，卻不是同一種空間，也不能用同一個『剩餘容量』欄位合併。

```text
辨識資源類型
  ↓
由 BIR 找 BAR
  ↓
核對 enable/status
  ↓
依用途放置資料
  ↓
另外追蹤 namespace/capacity 階層
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| CMB | controller-provided working memory | 是否能放 SQ/CQ/list/data 由能力 bit 決定 |
| PMR | 具有持久性語意的 region | enable、ready、error 與 address control 要一起看 |
| capacity model | subsystem／group／set／namespace 的容量 | 不同層級欄位不可直接相減 |

**說明性範例。** 說明性範例：CMB size 足以容納一個 SQ，不代表 controller 的 namespace 多出同樣容量；前者是 queue/data structure 的放置資源，後者才是 host 可格式化與存取的非揮發性容量。

**常見誤解／Debug。** Memory-map debug 圖至少用不同區塊標 host memory、CMB、PMR 與 namespace media。若 address 屬於 CMB/PMR，還要保留 BIR、BAR base、offset、enable 與 ready 狀態，不能只印最終 CPU virtual address。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§3.1.4，文件頁 52-54，PDF 頁 78-80; NVME-BASE-2.4 Rev. 2.4，§3.8，文件頁 125-129，PDF 頁 151-155; NVME-BASE-2.4 Rev. 2.4，§3.2.2-3.2.4，文件頁 80-85，PDF 頁 106-111

**關聯 Figure：** Figure 47, Figure 48, Figure 52, Figure 53, Figure 54, Figure 55, Figure 58, Figure 59, Figure 60, Figure 61, Figure 62, Figure 63, Figure 64, Figure 86, Figure 87, Figure 88, Figure 89

### Module 05: Shutdown、reset、Keep Alive 與 firmware update 的 recovery 邊界

**解釋。** Lifecycle 事件的共同問題是『哪一層狀態仍有效』。Normal shutdown 由 CC.SHN/CSTS.SHST 協調，reset 分成 subsystem/controller/queue 層級，Keep Alive 監測 host-controller 存活，firmware activation 又可能要求特定 reset。相同的『暫時無法處理 command』症狀，不代表可以使用相同 recovery。

```text
辨識事件來源
  ↓
決定影響 scope
  ↓
停止新工作
  ↓
等待狀態／timeout
  ↓
重建被清除的資源
  ↓
驗證可恢復 I/O
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| normal shutdown | 保護性停止與狀態回報 | 看 SHN/SHST |
| controller reset | controller 層級狀態 | queue 是否保留要依 reset 類型 |
| NVM subsystem reset | 更大 subsystem scope | 可能影響多個 controllers |
| Keep Alive timeout | liveness failure | 不能直接等同 media failure |

**說明性範例。** 說明性範例：host 要做 normal shutdown 時先停止提交新 I/O，設定 CC.SHN，再監看 CSTS.SHST。若等待期間發生 controller fatal status，後續 recovery 應按 reset scope 重建資源，而不是假設 normal shutdown 已完成。

**常見誤解／Debug。** Recovery trace 必須記錄 trigger、scope、開始/完成 timestamp、timeout source 與重建清單。只記『reset device』會讓 queue-level、controller-level 與 subsystem-level state loss 無法區分。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§3.6.1, 3.6.3，文件頁 113-120，PDF 頁 139-146; NVME-BASE-2.4 Rev. 2.4，§3.7，文件頁 120-125，PDF 頁 146-151; NVME-BASE-2.4 Rev. 2.4，§3.9，文件頁 129-135，PDF 頁 155-161; NVME-BASE-2.4 Rev. 2.4，§3.10-3.11，文件頁 135-138，PDF 頁 161-164

**關聯 Figure：** Figure 43, Figure 56, Figure 84, Figure 85, Figure 90, Figure 91

## 可追溯的規格重點

前面的 Mental Model 解釋因果；本節保留每個可追溯結論與 normative 強度，供講者備註與審查。

### 1. static controller model

<!-- claim:BASE3-STATIC -->

memory-based controller 必須（shall）只支援 static controller model。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.1, 文件頁 38, PDF 頁 64

### 2. I/O 與 Administrative controller

<!-- claim:BASE3-TYPES -->

本輪只使用 I/O controller 與 Administrative controller：前者可執行使用者資料的 I/O，後者以管理為目的且不支援資料 I/O command。兩者都具有一組 Admin Submission／Completion Queue。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3-3.1.3.2, 文件頁 39-43, PDF 頁 65-69

### 3. 命令與完成順序

<!-- claim:BASE3-ORDER -->

除 fused operation 外，controller 取走的命令與完成沒有一般性的先後保證；若有順序需求，強制該順序是 host 的責任。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3, 文件頁 40, PDF 頁 66

### 4. property 存取寬度

<!-- claim:BASE3-PROPERTY -->

host 必須（shall）以 property 指定的寬度，從 property 起始 offset 存取；memory-based controller 的實際存取規則由 PCIe Transport 補充。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, 文件頁 52-54, PDF 頁 78-80

### 5. NSID 狀態與特殊值

<!-- claim:BASE3-NAMESPACE -->

NSID 0h 無效，FFFFFFFFh 是 broadcast 值；其餘 NSID 還要區分 allocated／unallocated 與 active／inactive，不能只看數字是否落在範圍內。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.1, 文件頁 78-80, PDF 頁 104-106

### 6. 媒體與回收階層

<!-- claim:BASE3-MEDIA -->

NVM Set、Endurance Group、Reclaim Group 與 Reclaim Unit 分別描述容量集合、耐久度管理與回收粒度。是否支援及其 identifier 由 Identify／log page 能力判定。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, 文件頁 80-85, PDF 頁 106-111

### 7. domain 邊界與識別碼

<!-- claim:BASE3-DOMAIN -->

domain 是 NVM subsystem 內的故障／通訊邊界。多 domain subsystem 的 identifier 必須（shall）在該 subsystem 內唯一。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.5, 文件頁 85-88, PDF 頁 111-114

### 8. PCIe queue 建立與 pointer

<!-- claim:BASE3-QUEUE -->

PCIe queue 由 host-addressable memory 中的環形 buffer、head 與 tail pointer 構成。host 建立 I/O Completion Queue 後再建立對應 Submission Queue，並以 doorbell 推進 pointer。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1, 文件頁 88-91, PDF 頁 114-117

### 9. 命令處理與 arbitration

<!-- claim:BASE3-PROCESS -->

command processing 要分開看 ordering、fused／atomic semantics、arbitration 與 outstanding command 上限；priority 屬於 Submission Queue，不是每一筆 command 的獨立欄位。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, 文件頁 101-105, PDF 頁 127-131

### 10. controller 初始化

<!-- claim:BASE3-INIT -->

PCIe 初始化以 CAP 判斷能力與 timeout，設定 AQA／ASQ／ACQ 與 CC，接著等待 CSTS.RDY。ready mode 與 CRTO 會影響 host 等待與錯誤處理。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, 文件頁 105-113, PDF 頁 131-139

### 11. shutdown 狀態流程

<!-- claim:BASE3-SHUTDOWN -->

正常 shutdown 由 host 設定 CC.SHN，controller 透過 CSTS.SHST 回報進度；NVM subsystem shutdown 是更大範圍的處理，不能與單一 controller shutdown 混為一談。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, 文件頁 113-120, PDF 頁 139-146

### 12. reset 層級與影響範圍

<!-- claim:BASE3-RESET -->

NVM Subsystem Reset、Controller Level Reset 與 Queue Level Reset 的影響範圍不同；設計 recovery flow 前先確認哪一層狀態會被清除、queue 是否仍存在。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.7, 文件頁 120-125, PDF 頁 146-151

### 13. capacity model

<!-- claim:BASE3-CAPACITY -->

capacity model 分開追蹤 NVM subsystem、Endurance Group、NVM Set 與 namespace 的可用或配置容量；同一數值不可跨層級直接比較。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.8, 文件頁 125-129, PDF 頁 151-155

### 14. Keep Alive timer

<!-- claim:BASE3-KEEPALIVE -->

Keep Alive 以 KATO／KATT 建立 host 與 controller 的存活監測；本報告只保留 controller 共通與 PCIe 可用的 timer、command 與 timeout 行為。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.9, 文件頁 129-135, PDF 頁 155-161

### 15. firmware update 與 privileged action

<!-- claim:BASE3-FIRMWARE -->

privileged action 會影響其他 host 或 controller；firmware update 分成 image download、commit／activate 與可能的 reset，host 依回報的 activation action 安排流程。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

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

## Figure／欄位表教學參考

本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。欄位與 keyword 索引來自本機核對過的 PDF。

<a id="section-3-1"></a>

### §3.1

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 23: Controller Types</strong></summary>

<!-- claim:BASE3-FIG-023-CLAIM figure-table:BASE3-FIG-023 -->

**SPEC。** Figure 23〈Controller Types〉：呈現〈Controller Types〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：Controller。

#### 這張 Figure 在完整流程中的位置

Figure 23 位於 §3.1.3，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Controller 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Controller]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Controller` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.3。
2. 依圖中指定的寬度與位置解碼 Controller；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 23 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.3 如何排列 Controller、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 23 對應的 raw value 或 buffer，標出包含 Controller 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Controller，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Controller 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Controller

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3, Figure 23, 文件頁 39, PDF 頁 65

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 24: NVM Subsystem with Three I/O Controllers</strong></summary>

<!-- claim:BASE3-FIG-024-CLAIM figure-table:BASE3-FIG-024 -->

**SPEC。** Figure 24〈NVM Subsystem with Three I/O Controllers〉：呈現〈NVM Subsystem with Three I/O Controllers〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, I/O Controller, Controller。

#### 這張 Figure 在完整流程中的位置

Figure 24 位於 §3.1.3.1，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Subsystem 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NVM Subsystem]
          ↓
[擷取欄位: I/O Controller] → [套用編碼: Controller]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NVM Subsystem` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `I/O Controller` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Controller` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.3.1。
2. 依圖中指定的寬度與位置解碼 NVM Subsystem；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 I/O Controller 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 24 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.3.1 如何排列 NVM Subsystem、I/O Controller 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.3.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 24 對應的 raw value 或 buffer，標出包含 NVM Subsystem 的 bytes 並解碼，再獨立核對 I/O Controller。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 I/O Controller 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NVM Subsystem, I/O Controller, Controller

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.1, Figure 24, 文件頁 41, PDF 頁 67

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 25: NVM Subsystem with One Administrative and Two I/O Controllers</strong></summary>

<!-- claim:BASE3-FIG-025-CLAIM figure-table:BASE3-FIG-025 -->

**SPEC。** Figure 25〈NVM Subsystem with One Administrative and Two I/O Controllers〉：呈現〈NVM Subsystem with One Administrative and Two I/O Controllers〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, I/O Controller, Controller。

#### 這張 Figure 在完整流程中的位置

Figure 25 位於 §3.1.3.2，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Subsystem 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NVM Subsystem]
          ↓
[擷取欄位: I/O Controller] → [套用編碼: Controller]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NVM Subsystem` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `I/O Controller` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Controller` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.3.2。
2. 依圖中指定的寬度與位置解碼 NVM Subsystem；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 I/O Controller 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 25 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.3.2 如何排列 NVM Subsystem、I/O Controller 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.3.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 25 對應的 raw value 或 buffer，標出包含 NVM Subsystem 的 bytes 並解碼，再獨立核對 I/O Controller。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 I/O Controller 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NVM Subsystem, I/O Controller, Controller

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.2, Figure 25, 文件頁 42, PDF 頁 68

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 26: NVM Subsystem with One Administrative Controller</strong></summary>

<!-- claim:BASE3-FIG-026-CLAIM figure-table:BASE3-FIG-026 -->

**SPEC。** Figure 26〈NVM Subsystem with One Administrative Controller〉：呈現〈NVM Subsystem with One Administrative Controller〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem, Administrative Controller, Controller。

#### 這張 Figure 在完整流程中的位置

Figure 26 位於 §3.1.3.2，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Subsystem 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NVM Subsystem]
          ↓
[擷取欄位: Administrative Controller] → [套用編碼: Controller]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NVM Subsystem` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Administrative Controller` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Controller` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.3.2。
2. 依圖中指定的寬度與位置解碼 NVM Subsystem；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Administrative Controller 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 26 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.3.2 如何排列 NVM Subsystem、Administrative Controller 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.3.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 26 對應的 raw value 或 buffer，標出包含 NVM Subsystem 的 bytes 並解碼，再獨立核對 Administrative Controller。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 Administrative Controller 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NVM Subsystem, Administrative Controller, Controller

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.2, Figure 26, 文件頁 42, PDF 頁 68

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 27: Controller IDs FFF0h to FFFFh</strong></summary>

<!-- claim:BASE3-FIG-027-CLAIM figure-table:BASE3-FIG-027 -->

**SPEC。** Figure 27〈Controller IDs FFF0h to FFFFh〉：定義〈Controller IDs FFF0h to FFFFh〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：Controller, Controller ID。

#### 這張 Figure 在完整流程中的位置

Figure 27 位於 §3.1.3.3，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Controller 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Controller]
          ↓
[擷取欄位: Controller ID] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Controller` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Controller ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.3.3。
2. 依圖中指定的寬度與位置解碼 Controller；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Controller ID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 27 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.3.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.3.3 如何排列 Controller、Controller ID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.3.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 27 對應的 raw value 或 buffer，標出包含 Controller 的 bytes 並解碼，再獨立核對 Controller ID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Controller，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Controller 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Controller ID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Controller, Controller ID

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.3, Figure 27, 文件頁 44, PDF 頁 70

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 28: Admin Command Support Requirements</strong></summary>

<!-- claim:BASE3-FIG-028-CLAIM figure-table:BASE3-FIG-028 -->

**SPEC。** Figure 28〈Admin Command Support Requirements〉：統整〈Admin Command Support Requirements〉指定的支援等級。 先確認 row 與 controller／command-set 上下文，再解讀 support marker；來源索引：MI, O10, O11, Command。

#### 這張 Figure 在完整流程中的位置

Figure 28 位於 §3.1.3.3.3，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 MI 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MI]
          ↓
[擷取欄位: O10] → [套用編碼: O11]
                                      ↓
[驗證證據: Command]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MI` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `O10` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `O11` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Command` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.3.3.3。
2. 依圖中指定的寬度與位置解碼 MI；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 O10 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 28 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.3.3.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.3.3.3 如何排列 MI、O10 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.3.3.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 28 對應的 raw value 或 buffer，標出包含 MI 的 bytes 並解碼，再獨立核對 O10。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 MI，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 MI 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 O10 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** MI, O10, O11, Command

**來源 keyword 索引：** `optional`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.3.3, Figure 28, 文件頁 45-47, PDF 頁 71-73

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 30: Common I/O Command Support Requirements</strong></summary>

<!-- claim:BASE3-FIG-030-CLAIM figure-table:BASE3-FIG-030 -->

**SPEC。** Figure 30〈Common I/O Command Support Requirements〉：統整〈Common I/O Command Support Requirements〉指定的支援等級。 先確認 row 與 controller／command-set 上下文，再解讀 support marker；來源索引：FDPS, Command。

#### 這張 Figure 在完整流程中的位置

Figure 30 位於 §3.1.3.4，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 FDPS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: FDPS]
          ↓
[擷取欄位: Command] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `FDPS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Command` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.3.4。
2. 依圖中指定的寬度與位置解碼 FDPS；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Command 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 30 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.3.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.3.4 如何排列 FDPS、Command 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.3.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 30 對應的 raw value 或 buffer，標出包含 FDPS 的 bytes 並解碼，再獨立核對 Command。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 FDPS，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 FDPS 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Command 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** FDPS, Command

**來源 keyword 索引：** `optional`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.4, Figure 30, 文件頁 47-48, PDF 頁 73-74

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 31: Log Page Support Requirements</strong></summary>

<!-- claim:BASE3-FIG-031-CLAIM figure-table:BASE3-FIG-031 -->

**SPEC。** Figure 31〈Log Page Support Requirements〉：統整〈Log Page Support Requirements〉指定的支援等級。 先確認 row 與 controller／command-set 上下文，再解讀 support marker；來源索引：M3, SMART, O4, O6, O12, O13, FDP, O5。

#### 這張 Figure 在完整流程中的位置

Figure 31 位於 §3.1.3.4，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 M3 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: M3]
          ↓
[擷取欄位: SMART] → [套用編碼: O4]
                                      ↓
[驗證證據: O6]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `M3` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SMART` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `O4` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `O6` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `O12` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `O13` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.3.4。
2. 依圖中指定的寬度與位置解碼 M3；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 SMART 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 31 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.3.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.3.4 如何排列 M3、SMART 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.3.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 31 對應的 raw value 或 buffer，標出包含 M3 的 bytes 並解碼，再獨立核對 SMART。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 M3，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 M3 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 SMART 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** M3, SMART, O4, O6, O12, O13, FDP, O5

**來源 keyword 索引：** `shall`, `optional`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.4, Figure 31, 文件頁 48-50, PDF 頁 74-76

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 32: Feature Support Requirements</strong></summary>

<!-- claim:BASE3-FIG-032-CLAIM figure-table:BASE3-FIG-032 -->

**SPEC。** Figure 32〈Feature Support Requirements〉：統整〈Feature Support Requirements〉指定的支援等級。 先確認 row 與 controller／command-set 上下文，再解讀 support marker；來源索引：LBA, O8, M10, M7, O9, O6, O5, O3。

#### 這張 Figure 在完整流程中的位置

Figure 32 位於 §3.1.3.5，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 LBA 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBA]
          ↓
[擷取欄位: O8] → [套用編碼: M10]
                                      ↓
[驗證證據: M7]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `O8` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `M10` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `M7` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `O9` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `O6` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.3.5。
2. 依圖中指定的寬度與位置解碼 LBA；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 O8 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 32 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.3.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.3.5 如何排列 LBA、O8 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.3.5 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 32 對應的 raw value 或 buffer，標出包含 LBA 的 bytes 並解碼，再獨立核對 O8。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 LBA，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 LBA 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 O8 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** LBA, O8, M10, M7, O9, O6, O5, O3

**來源 keyword 索引：** `optional`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.5, Figure 32, 文件頁 50-52, PDF 頁 76-78

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 33: Property Definition</strong></summary>

<!-- claim:BASE3-FIG-033-CLAIM figure-table:BASE3-FIG-033 -->

**SPEC。** Figure 33〈Property Definition〉：定義〈Property Definition〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：OFST, CAP, VS, M2, INTMS, INTMC, CC, CSTS。

#### 這張 Figure 在完整流程中的位置

Figure 33 位於 §3.1.4，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 OFST 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: OFST]
          ↓
[擷取欄位: CAP] → [套用編碼: VS]
                                      ↓
[驗證證據: M2]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `OFST` | Offset，Firmware Image Download 中以 dword 為單位的 image-relative offset。 |
| `CAP` | Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 |
| `VS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `M2` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `INTMS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `INTMC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4。
2. 依圖中指定的寬度與位置解碼 OFST；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CAP 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 33 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4 如何排列 OFST、CAP 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 33 對應的 raw value 或 buffer，標出包含 OFST 的 bytes 並解碼，再獨立核對 CAP。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 OFST，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 OFST 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CAP 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** OFST, CAP, VS, M2, INTMS, INTMC, CC, CSTS

**來源 keyword 索引：** `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, Figure 33, 文件頁 52-53, PDF 頁 78-79

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 34: Memory-Based Property Definition</strong></summary>

<!-- claim:BASE3-FIG-034-CLAIM figure-table:BASE3-FIG-034 -->

**SPEC。** Figure 34〈Memory-Based Property Definition〉：定義〈Memory-Based Property Definition〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：OFST, CAP.DSTRD。

#### 這張 Figure 在完整流程中的位置

Figure 34 位於 §3.1.4，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 OFST 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: OFST]
          ↓
[擷取欄位: CAP.DSTRD] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `OFST` | Offset，Firmware Image Download 中以 dword 為單位的 image-relative offset。 |
| `CAP.DSTRD` | Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.DSTRD 進一步指定其中的 DSTRD 子欄位。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4。
2. 依圖中指定的寬度與位置解碼 OFST；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CAP.DSTRD 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 34 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4 如何排列 OFST、CAP.DSTRD 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 34 對應的 raw value 或 buffer，標出包含 OFST 的 bytes 並解碼，再獨立核對 CAP.DSTRD。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 OFST，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 OFST 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CAP.DSTRD 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** OFST, CAP.DSTRD

**來源 keyword 索引：** `optional`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, Figure 34, 文件頁 54, PDF 頁 80

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 36: Offset 0h: CAP - Controller Capabilities</strong></summary>

<!-- claim:BASE3-FIG-036-CLAIM figure-table:BASE3-FIG-036 -->

**SPEC。** Figure 36〈Offset 0h: CAP - Controller Capabilities〉：定義 offset 0h 的 CAP（Controller Capabilities），並指出軟體在該位置必須分別解碼的欄位。 先定位 CAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NSSES, CRMS, CRIMS, CRWMS, NSSS, CMBS, PMRS, MPSMAX。

#### 這張 Figure 在完整流程中的位置

Figure 36 位於 §3.1.4.1，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NSSES 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSSES]
          ↓
[擷取欄位: CRMS] → [套用編碼: CRIMS]
                                      ↓
[驗證證據: CRWMS]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSSES` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CRMS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CRIMS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CRWMS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NSSS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMBS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.1。
2. 依圖中指定的寬度與位置解碼 NSSES；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CRMS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 36 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.1 如何排列 NSSES、CRMS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 36 對應的 raw value 或 buffer，標出包含 NSSES 的 bytes 並解碼，再獨立核對 CRMS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NSSES，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NSSES 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CRMS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NSSES, CRMS, CRIMS, CRWMS, NSSS, CMBS, PMRS, MPSMAX

**來源 keyword 索引：** `shall not`, `shall`, `should`, `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, 文件頁 55-58, PDF 頁 81-84

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 37: Specification Version Descriptor</strong></summary>

<!-- claim:BASE3-FIG-037-CLAIM figure-table:BASE3-FIG-037 -->

**SPEC。** Figure 37〈Specification Version Descriptor〉：定義〈Specification Version Descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MJR, MNR, TER。

#### 這張 Figure 在完整流程中的位置

Figure 37 位於 §3.1.4.1，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 MJR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MJR]
          ↓
[擷取欄位: MNR] → [套用編碼: TER]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MJR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MNR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `TER` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.1。
2. 依圖中指定的寬度與位置解碼 MJR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MNR 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 37 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.1 如何排列 MJR、MNR 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 37 對應的 raw value 或 buffer，標出包含 MJR 的 bytes 並解碼，再獨立核對 MNR。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 MJR，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 MJR 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MNR 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** MJR, MNR, TER

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 37, 文件頁 58, PDF 頁 84

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 38: NVM Express Base Specification Version Property Reset Values</strong></summary>

<!-- claim:BASE3-FIG-038-CLAIM figure-table:BASE3-FIG-038 -->

**SPEC。** Figure 38〈NVM Express Base Specification Version Property Reset Values〉：定義〈NVM Express Base Specification Version Property Reset Values〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MJR, MNR, TER。

#### 這張 Figure 在完整流程中的位置

Figure 38 位於 §3.1.4.1，在本流程中是「state」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 MJR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 state／timing 圖。沿箭頭記錄 trigger、觀察者、完成條件與 timeout source。相同狀態名稱若位於不同 reset scope，不能推論保留相同 queue 或 controller state。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MJR]
          ↓
[擷取欄位: MNR] → [套用編碼: TER]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MJR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MNR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `TER` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.1。
2. 依圖中指定的寬度與位置解碼 MJR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MNR 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 38 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.1 如何排列 MJR、MNR 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 38 對應的 raw value 或 buffer，標出包含 MJR 的 bytes 並解碼，再獨立核對 MNR。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 MJR，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 MJR 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MNR 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** MJR, MNR, TER

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 38, 文件頁 58-59, PDF 頁 84-85

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 39: Offset Ch: INTMS - Interrupt Mask Set</strong></summary>

<!-- claim:BASE3-FIG-039-CLAIM figure-table:BASE3-FIG-039 -->

**SPEC。** Figure 39〈Offset Ch: INTMS - Interrupt Mask Set〉：定義 offset Ch 的 INTMS（Interrupt Mask Set），並指出軟體在該位置必須分別解碼的欄位。 先定位 INTMS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：IVMS, INTMS, RWS, MSI, Interrupt。

#### 這張 Figure 在完整流程中的位置

Figure 39 位於 §3.1.4.2，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 IVMS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: IVMS]
          ↓
[擷取欄位: INTMS] → [套用編碼: RWS]
                                      ↓
[驗證證據: MSI]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `IVMS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `INTMS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `RWS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSI` | Message Signaled Interrupt，透過 memory write message 傳遞 interrupt 的 PCI 機制。 |
| `Interrupt` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.2。
2. 依圖中指定的寬度與位置解碼 IVMS；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 INTMS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 39 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.2 如何排列 IVMS、INTMS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 39 對應的 raw value 或 buffer，標出包含 IVMS 的 bytes 並解碼，再獨立核對 INTMS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 IVMS，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 IVMS 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 INTMS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** IVMS, INTMS, RWS, MSI, Interrupt

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.2, Figure 39, 文件頁 59, PDF 頁 85

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 40: Offset 10h: INTMC - Interrupt Mask Clear</strong></summary>

<!-- claim:BASE3-FIG-040-CLAIM figure-table:BASE3-FIG-040 -->

**SPEC。** Figure 40〈Offset 10h: INTMC - Interrupt Mask Clear〉：定義 offset 10h 的 INTMC（Interrupt Mask Clear），並指出軟體在該位置必須分別解碼的欄位。 先定位 INTMC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：IVMC, INTMC, RWC, Interrupt。

#### 這張 Figure 在完整流程中的位置

Figure 40 位於 §3.1.4.2，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 IVMC 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: IVMC]
          ↓
[擷取欄位: INTMC] → [套用編碼: RWC]
                                      ↓
[驗證證據: Interrupt]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `IVMC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `INTMC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `RWC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Interrupt` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.2。
2. 依圖中指定的寬度與位置解碼 IVMC；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 INTMC 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 40 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.2 如何排列 IVMC、INTMC 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 40 對應的 raw value 或 buffer，標出包含 IVMC 的 bytes 並解碼，再獨立核對 INTMC。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 IVMC，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 IVMC 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 INTMC 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** IVMC, INTMC, RWC, Interrupt

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.2, Figure 40, 文件頁 59, PDF 頁 85

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 41: Offset 14h: CC - Controller Configuration</strong></summary>

<!-- claim:BASE3-FIG-041-CLAIM figure-table:BASE3-FIG-041 -->

**SPEC。** Figure 41〈Offset 14h: CC - Controller Configuration〉：定義 offset 14h 的 CC（Controller Configuration），並指出軟體在該位置必須分別解碼的欄位。 先定位 CC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CRIME, SHN, AMS, MPS, CSS, EN, CC, CC.EN。

#### 這張 Figure 在完整流程中的位置

Figure 41 位於 §3.1.4.5，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CRIME 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CRIME]
          ↓
[擷取欄位: SHN] → [套用編碼: AMS]
                                      ↓
[驗證證據: MPS]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CRIME` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SHN` | Shutdown Notification，CC 中由 host 宣告 shutdown 類型的欄位。 |
| `AMS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MPS` | Memory Page Size，controller 使用的 memory page 大小設定；影響 queue address 與 PRP 對齊。 |
| `CSS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `EN` | Enable，CC 中控制 controller enable state 的 bit。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.5。
2. 依圖中指定的寬度與位置解碼 CRIME；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 SHN 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 41 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.5 如何排列 CRIME、SHN 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.5 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 41 對應的 raw value 或 buffer，標出包含 CRIME 的 bytes 並解碼，再獨立核對 SHN。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CRIME，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CRIME 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 SHN 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CRIME, SHN, AMS, MPS, CSS, EN, CC, CC.EN

**來源 keyword 索引：** `shall not`, `shall`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.5, Figure 41, 文件頁 60-63, PDF 頁 86-89

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 42: Offset 1Ch: CSTS - Controller Status</strong></summary>

<!-- claim:BASE3-FIG-042-CLAIM figure-table:BASE3-FIG-042 -->

**SPEC。** Figure 42〈Offset 1Ch: CSTS - Controller Status〉：定義 offset 1Ch 的 CSTS（Controller Status），並指出軟體在該位置必須分別解碼的欄位。 先定位 CSTS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ST, PP, NSSRO, SHST, CLR, CFS, RDY, CSTS。

#### 這張 Figure 在完整流程中的位置

Figure 42 位於 §3.1.4.5，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ST 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ST]
          ↓
[擷取欄位: PP] → [套用編碼: NSSRO]
                                      ↓
[驗證證據: SHST]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ST` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NSSRO` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SHST` | Shutdown Status，CSTS 中由 controller 回報 shutdown 進度的欄位。 |
| `CLR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CFS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.5。
2. 依圖中指定的寬度與位置解碼 ST；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 PP 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 42 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.5 如何排列 ST、PP 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.5 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 42 對應的 raw value 或 buffer，標出包含 ST 的 bytes 並解碼，再獨立核對 PP。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 ST，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 ST 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 PP 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ST, PP, NSSRO, SHST, CLR, CFS, RDY, CSTS

**來源 keyword 索引：** `shall not`, `should not`, `shall`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.5, Figure 42, 文件頁 63-65, PDF 頁 89-91

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 43: Offset 20h: NSSR - NVM Subsystem Reset</strong></summary>

<!-- claim:BASE3-FIG-043-CLAIM figure-table:BASE3-FIG-043 -->

**SPEC。** Figure 43〈Offset 20h: NSSR - NVM Subsystem Reset〉：定義 offset 20h 的 NSSR（NVM Subsystem Reset），並指出軟體在該位置必須分別解碼的欄位。 先定位 NSSR，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NSSRC, NSSR, NVM Subsystem。

#### 這張 Figure 在完整流程中的位置

Figure 43 位於 §3.1.4.6，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NSSRC 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSSRC]
          ↓
[擷取欄位: NSSR] → [套用編碼: NVM Subsystem]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSSRC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NSSR` | NVM Subsystem Reset，觸發 NVM subsystem reset 的 property。 |
| `NVM Subsystem` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.6。
2. 依圖中指定的寬度與位置解碼 NSSRC；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NSSR 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 43 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.6 如何排列 NSSRC、NSSR 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.6 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 43 對應的 raw value 或 buffer，標出包含 NSSRC 的 bytes 並解碼，再獨立核對 NSSR。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NSSRC，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NSSRC 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NSSR 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NSSRC, NSSR, NVM Subsystem

**來源 keyword 索引：** `shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 43, 文件頁 66, PDF 頁 92

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 44: Offset 24h: AQA - Admin Queue Attributes</strong></summary>

<!-- claim:BASE3-FIG-044-CLAIM figure-table:BASE3-FIG-044 -->

**SPEC。** Figure 44〈Offset 24h: AQA - Admin Queue Attributes〉：定義 offset 24h 的 AQA（Admin Queue Attributes），並指出軟體在該位置必須分別解碼的欄位。 先定位 AQA，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ACQS, ASQS, AQA。

#### 這張 Figure 在完整流程中的位置

Figure 44 位於 §3.1.4.6，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ACQS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ACQS]
          ↓
[擷取欄位: ASQS] → [套用編碼: AQA]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ACQS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ASQS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AQA` | Admin Queue Attributes，描述 Admin SQ 與 Admin CQ 大小的 property。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.6。
2. 依圖中指定的寬度與位置解碼 ACQS；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 ASQS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 44 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.6 如何排列 ACQS、ASQS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.6 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 44 對應的 raw value 或 buffer，標出包含 ACQS 的 bytes 並解碼，再獨立核對 ASQS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 ACQS，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 ACQS 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 ASQS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ACQS, ASQS, AQA

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 44, 文件頁 66, PDF 頁 92

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 45: Offset 28h: ASQ - Admin Submission Queue Base Address</strong></summary>

<!-- claim:BASE3-FIG-045-CLAIM figure-table:BASE3-FIG-045 -->

**SPEC。** Figure 45〈Offset 28h: ASQ - Admin Submission Queue Base Address〉：定義 offset 28h 的 ASQ（Admin Submission Queue Base Address），並指出軟體在該位置必須分別解碼的欄位。 先定位 ASQ，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ASQB, ASQ, CC.MPS, Submission Queue。

#### 這張 Figure 在完整流程中的位置

Figure 45 位於 §3.1.4.6，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ASQB 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ASQB]
          ↓
[擷取欄位: ASQ] → [套用編碼: CC.MPS]
                                      ↓
[驗證證據: Submission Queue]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ASQB` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ASQ` | Admin Submission Queue Base Address，Admin SQ 在可定址記憶體中的基底位址。 |
| `CC.MPS` | Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.MPS 進一步指定其中的 MPS 子欄位。 |
| `Submission Queue` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.6。
2. 依圖中指定的寬度與位置解碼 ASQB；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 ASQ 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 45 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.6 如何排列 ASQB、ASQ 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.6 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 45 對應的 raw value 或 buffer，標出包含 ASQB 的 bytes 並解碼，再獨立核對 ASQ。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 ASQB，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 ASQB 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 ASQ 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ASQB, ASQ, CC.MPS, Submission Queue

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 45, 文件頁 66, PDF 頁 92

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 46: Offset 30h: ACQ - Admin Completion Queue Base Address</strong></summary>

<!-- claim:BASE3-FIG-046-CLAIM figure-table:BASE3-FIG-046 -->

**SPEC。** Figure 46〈Offset 30h: ACQ - Admin Completion Queue Base Address〉：定義 offset 30h 的 ACQ（Admin Completion Queue Base Address），並指出軟體在該位置必須分別解碼的欄位。 先定位 ACQ，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ACQB, ACQ, CC.MPS, Completion Queue。

#### 這張 Figure 在完整流程中的位置

Figure 46 位於 §3.1.4.9，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ACQB 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ACQB]
          ↓
[擷取欄位: ACQ] → [套用編碼: CC.MPS]
                                      ↓
[驗證證據: Completion Queue]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ACQB` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ACQ` | Admin Completion Queue Base Address，Admin CQ 在可定址記憶體中的基底位址。 |
| `CC.MPS` | Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.MPS 進一步指定其中的 MPS 子欄位。 |
| `Completion Queue` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.9。
2. 依圖中指定的寬度與位置解碼 ACQB；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 ACQ 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 46 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.9 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.9 如何排列 ACQB、ACQ 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.9 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 46 對應的 raw value 或 buffer，標出包含 ACQB 的 bytes 並解碼，再獨立核對 ACQ。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 ACQB，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 ACQB 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 ACQ 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ACQB, ACQ, CC.MPS, Completion Queue

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.9, Figure 46, 文件頁 67, PDF 頁 93

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 47: Offset 38h: CMBLOC - Controller Memory Buffer Location</strong></summary>

<!-- claim:BASE3-FIG-047-CLAIM figure-table:BASE3-FIG-047 -->

**SPEC。** Figure 47〈Offset 38h: CMBLOC - Controller Memory Buffer Location〉：定義 offset 38h 的 CMBLOC（Controller Memory Buffer Location），並指出軟體在該位置必須分別解碼的欄位。 先定位 CMBLOC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CQMMS, BIR, CMBLOC, CMB, BAR, Controller。

#### 這張 Figure 在完整流程中的位置

Figure 47 位於 §3.1.4.9，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CQMMS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CQMMS]
          ↓
[擷取欄位: BIR] → [套用編碼: CMBLOC]
                                      ↓
[驗證證據: CMB]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CQMMS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `BIR` | BAR Indicator Register，指出某個記憶體結構位於哪一個 PCIe BAR。 |
| `CMBLOC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMB` | Controller Memory Buffer，controller 提供、可放置部分 queue 或資料結構的記憶體區域。 |
| `BAR` | Base Address Register，PCI configuration space 中用來定位裝置 memory space 的 register。 |
| `Controller` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.9。
2. 依圖中指定的寬度與位置解碼 CQMMS；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 BIR 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 47 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.9 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.9 如何排列 CQMMS、BIR 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.9 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 47 對應的 raw value 或 buffer，標出包含 CQMMS 的 bytes 並解碼，再獨立核對 BIR。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CQMMS，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CQMMS 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 BIR 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CQMMS, BIR, CMBLOC, CMB, BAR, Controller

**來源 keyword 索引：** `shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.9, Figure 47, 文件頁 67-68, PDF 頁 93-94

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 48: Offset 3Ch: CMBSZ - Controller Memory Buffer Size</strong></summary>

<!-- claim:BASE3-FIG-048-CLAIM figure-table:BASE3-FIG-048 -->

**SPEC。** Figure 48〈Offset 3Ch: CMBSZ - Controller Memory Buffer Size〉：定義 offset 3Ch 的 CMBSZ（Controller Memory Buffer Size），並指出軟體在該位置必須分別解碼的欄位。 先定位 CMBSZ，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：SZ, SZU, WDS, RDS, LISTS, CQS, SQS, CMBSZ。

#### 這張 Figure 在完整流程中的位置

Figure 48 位於 §3.1.4.11，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SZ 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SZ]
          ↓
[擷取欄位: SZU] → [套用編碼: WDS]
                                      ↓
[驗證證據: RDS]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SZ` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SZU` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `WDS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `RDS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `LISTS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CQS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.11。
2. 依圖中指定的寬度與位置解碼 SZ；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 SZU 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 48 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.11 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.11 如何排列 SZ、SZU 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.11 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 48 對應的 raw value 或 buffer，標出包含 SZ 的 bytes 並解碼，再獨立核對 SZU。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SZ，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SZ 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 SZU 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SZ, SZU, WDS, RDS, LISTS, CQS, SQS, CMBSZ

**來源 keyword 索引：** `shall not`, `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.11, Figure 48, 文件頁 68-69, PDF 頁 94-95

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 49: Offset 40h: BPINFO - Boot Partition Information</strong></summary>

<!-- claim:BASE3-FIG-049-CLAIM figure-table:BASE3-FIG-049 -->

**SPEC。** Figure 49〈Offset 40h: BPINFO - Boot Partition Information〉：定義 offset 40h 的 BPINFO（Boot Partition Information），並指出軟體在該位置必須分別解碼的欄位。 先定位 BPINFO，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ABPID, BRS, BPSZ, BPINFO, ID, BPRSEL.BPID。

#### 這張 Figure 在完整流程中的位置

Figure 49 位於 §3.1.4.12，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ABPID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ABPID]
          ↓
[擷取欄位: BRS] → [套用編碼: BPSZ]
                                      ↓
[驗證證據: BPINFO]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ABPID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `BRS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `BPSZ` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `BPINFO` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `BPRSEL.BPID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.12。
2. 依圖中指定的寬度與位置解碼 ABPID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 BRS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 49 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.12 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.12 如何排列 ABPID、BRS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.12 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 49 對應的 raw value 或 buffer，標出包含 ABPID 的 bytes 並解碼，再獨立核對 BRS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 ABPID，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 ABPID 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 BRS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ABPID, BRS, BPSZ, BPINFO, ID, BPRSEL.BPID

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.12, Figure 49, 文件頁 69, PDF 頁 95

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 50: Offset 44h: BPRSEL - Boot Partition Read Select</strong></summary>

<!-- claim:BASE3-FIG-050-CLAIM figure-table:BASE3-FIG-050 -->

**SPEC。** Figure 50〈Offset 44h: BPRSEL - Boot Partition Read Select〉：定義 offset 44h 的 BPRSEL（Boot Partition Read Select），並指出軟體在該位置必須分別解碼的欄位。 先定位 BPRSEL，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：BPID, BPROF, BPRSZ, BPRSEL。

#### 這張 Figure 在完整流程中的位置

Figure 50 位於 §3.1.4.12，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 BPID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: BPID]
          ↓
[擷取欄位: BPROF] → [套用編碼: BPRSZ]
                                      ↓
[驗證證據: BPRSEL]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `BPID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `BPROF` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `BPRSZ` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `BPRSEL` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.12。
2. 依圖中指定的寬度與位置解碼 BPID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 BPROF 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 50 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.12 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.12 如何排列 BPID、BPROF 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.12 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 50 對應的 raw value 或 buffer，標出包含 BPID 的 bytes 並解碼，再獨立核對 BPROF。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 BPID，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 BPID 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 BPROF 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** BPID, BPROF, BPRSZ, BPRSEL

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.12, Figure 50, 文件頁 69-70, PDF 頁 95-96

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 51: Offset 48h: BPMBL - Boot Partition Memory Buffer Location</strong></summary>

<!-- claim:BASE3-FIG-051-CLAIM figure-table:BASE3-FIG-051 -->

**SPEC。** Figure 51〈Offset 48h: BPMBL - Boot Partition Memory Buffer Location〉：定義 offset 48h 的 BPMBL（Boot Partition Memory Buffer Location），並指出軟體在該位置必須分別解碼的欄位。 先定位 BPMBL，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：BMBBA, BPMBL。

#### 這張 Figure 在完整流程中的位置

Figure 51 位於 §3.1.4.14，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 BMBBA 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: BMBBA]
          ↓
[擷取欄位: BPMBL] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `BMBBA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `BPMBL` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.14。
2. 依圖中指定的寬度與位置解碼 BMBBA；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 BPMBL 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 51 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.14 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.14 如何排列 BMBBA、BPMBL 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.14 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 51 對應的 raw value 或 buffer，標出包含 BMBBA 的 bytes 並解碼，再獨立核對 BPMBL。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 BMBBA，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 BMBBA 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 BPMBL 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** BMBBA, BPMBL

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 51, 文件頁 70, PDF 頁 96

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 52: Offset 50h: CMBMSC - Controller Memory Buffer Memory Space Control</strong></summary>

<!-- claim:BASE3-FIG-052-CLAIM figure-table:BASE3-FIG-052 -->

**SPEC。** Figure 52〈Offset 50h: CMBMSC - Controller Memory Buffer Memory Space Control〉：定義 offset 50h 的 CMBMSC（Controller Memory Buffer Memory Space Control），並指出軟體在該位置必須分別解碼的欄位。 先定位 CMBMSC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CBA, CMSE, CRE, CMBMSC, CMBSMSC.CRE, CMBLOC, CMBSZ, Controller。

#### 這張 Figure 在完整流程中的位置

Figure 52 位於 §3.1.4.14，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CBA 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CBA]
          ↓
[擷取欄位: CMSE] → [套用編碼: CRE]
                                      ↓
[驗證證據: CMBMSC]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CBA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMSE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CRE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMBMSC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMBSMSC.CRE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMBLOC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.14。
2. 依圖中指定的寬度與位置解碼 CBA；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CMSE 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 52 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.14 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.14 如何排列 CBA、CMSE 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.14 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 52 對應的 raw value 或 buffer，標出包含 CBA 的 bytes 並解碼，再獨立核對 CMSE。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CBA，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CBA 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CMSE 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CBA, CMSE, CRE, CMBMSC, CMBSMSC.CRE, CMBLOC, CMBSZ, Controller

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 52, 文件頁 70-71, PDF 頁 96-97

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 53: Offset 58h: CMBSTS - Controller Memory Buffer Status</strong></summary>

<!-- claim:BASE3-FIG-053-CLAIM figure-table:BASE3-FIG-053 -->

**SPEC。** Figure 53〈Offset 58h: CMBSTS - Controller Memory Buffer Status〉：定義 offset 58h 的 CMBSTS（Controller Memory Buffer Status），並指出軟體在該位置必須分別解碼的欄位。 先定位 CMBSTS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CBAI, CMBSTS, CMBMSC.CBA, CMBMSC.CRE, CMBMSC.CMSE, Controller。

#### 這張 Figure 在完整流程中的位置

Figure 53 位於 §3.1.4.16，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CBAI 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CBAI]
          ↓
[擷取欄位: CMBSTS] → [套用編碼: CMBMSC.CBA]
                                      ↓
[驗證證據: CMBMSC.CRE]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CBAI` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMBSTS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMBMSC.CBA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMBMSC.CRE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMBMSC.CMSE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Controller` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.16。
2. 依圖中指定的寬度與位置解碼 CBAI；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CMBSTS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 53 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.16 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.16 如何排列 CBAI、CMBSTS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.16 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 53 對應的 raw value 或 buffer，標出包含 CBAI 的 bytes 並解碼，再獨立核對 CMBSTS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CBAI，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CBAI 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CMBSTS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CBAI, CMBSTS, CMBMSC.CBA, CMBMSC.CRE, CMBMSC.CMSE, Controller

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.16, Figure 53, 文件頁 71, PDF 頁 97

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 54: Offset 5Ch: CMBEBS - Controller Memory Buffer Elasticity Buffer Size</strong></summary>

<!-- claim:BASE3-FIG-054-CLAIM figure-table:BASE3-FIG-054 -->

**SPEC。** Figure 54〈Offset 5Ch: CMBEBS - Controller Memory Buffer Elasticity Buffer Size〉：定義 offset 5Ch 的 CMBEBS（Controller Memory Buffer Elasticity Buffer Size），並指出軟體在該位置必須分別解碼的欄位。 先定位 CMBEBS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CMBWBZ, CMBRBB, CMBSZU, CMBEBS, CMB, Controller。

#### 這張 Figure 在完整流程中的位置

Figure 54 位於 §3.1.4.16，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CMBWBZ 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CMBWBZ]
          ↓
[擷取欄位: CMBRBB] → [套用編碼: CMBSZU]
                                      ↓
[驗證證據: CMBEBS]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CMBWBZ` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMBRBB` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMBSZU` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMBEBS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMB` | Controller Memory Buffer，controller 提供、可放置部分 queue 或資料結構的記憶體區域。 |
| `Controller` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.16。
2. 依圖中指定的寬度與位置解碼 CMBWBZ；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CMBRBB 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 54 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.16 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.16 如何排列 CMBWBZ、CMBRBB 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.16 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 54 對應的 raw value 或 buffer，標出包含 CMBWBZ 的 bytes 並解碼，再獨立核對 CMBRBB。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CMBWBZ，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CMBWBZ 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CMBRBB 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CMBWBZ, CMBRBB, CMBSZU, CMBEBS, CMB, Controller

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.16, Figure 54, 文件頁 71, PDF 頁 97

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 55: Offset 60h: CMBSWTP - Controller Memory Buffer Sustained Write Throughput</strong></summary>

<!-- claim:BASE3-FIG-055-CLAIM figure-table:BASE3-FIG-055 -->

**SPEC。** Figure 55〈Offset 60h: CMBSWTP - Controller Memory Buffer Sustained Write Throughput〉：定義 offset 60h 的 CMBSWTP（Controller Memory Buffer Sustained Write Throughput），並指出軟體在該位置必須分別解碼的欄位。 先定位 CMBSWTP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CMBSWTV, CMBSWTU, CMBSWTP, CMB, TLP, MPS, PXDC, Controller。

#### 這張 Figure 在完整流程中的位置

Figure 55 位於 §3.1.4.19，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CMBSWTV 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CMBSWTV]
          ↓
[擷取欄位: CMBSWTU] → [套用編碼: CMBSWTP]
                                      ↓
[驗證證據: CMB]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CMBSWTV` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMBSWTU` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMBSWTP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMB` | Controller Memory Buffer，controller 提供、可放置部分 queue 或資料結構的記憶體區域。 |
| `TLP` | Transaction Layer Packet，PCIe transaction layer 傳送的 packet。 |
| `MPS` | Memory Page Size，controller 使用的 memory page 大小設定；影響 queue address 與 PRP 對齊。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.19。
2. 依圖中指定的寬度與位置解碼 CMBSWTV；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CMBSWTU 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 55 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.19 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.19 如何排列 CMBSWTV、CMBSWTU 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.19 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 55 對應的 raw value 或 buffer，標出包含 CMBSWTV 的 bytes 並解碼，再獨立核對 CMBSWTU。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CMBSWTV，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CMBSWTV 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CMBSWTU 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CMBSWTV, CMBSWTU, CMBSWTP, CMB, TLP, MPS, PXDC, Controller

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.19, Figure 55, 文件頁 72, PDF 頁 98

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 56: Offset 64h: NSSD - NVM Subsystem Shutdown</strong></summary>

<!-- claim:BASE3-FIG-056-CLAIM figure-table:BASE3-FIG-056 -->

**SPEC。** Figure 56〈Offset 64h: NSSD - NVM Subsystem Shutdown〉：定義 offset 64h 的 NSSD（NVM Subsystem Shutdown），並指出軟體在該位置必須分別解碼的欄位。 先定位 NSSD，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NSSC, NSSD, CAP.CPS, NVM Subsystem。

#### 這張 Figure 在完整流程中的位置

Figure 56 位於 §3.1.4.19，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NSSC 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSSC]
          ↓
[擷取欄位: NSSD] → [套用編碼: CAP.CPS]
                                      ↓
[驗證證據: NVM Subsystem]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSSC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NSSD` | NVM Subsystem Shutdown，控制較大範圍 subsystem shutdown 的 property。 |
| `CAP.CPS` | Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.CPS 進一步指定其中的 CPS 子欄位。 |
| `NVM Subsystem` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.19。
2. 依圖中指定的寬度與位置解碼 NSSC；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NSSD 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 56 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.19 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.19 如何排列 NSSC、NSSD 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.19 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 56 對應的 raw value 或 buffer，標出包含 NSSC 的 bytes 並解碼，再獨立核對 NSSD。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NSSC，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NSSC 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NSSD 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NSSC, NSSD, CAP.CPS, NVM Subsystem

**來源 keyword 索引：** `shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.19, Figure 56, 文件頁 72, PDF 頁 98

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 57: Offset 68h: CRTO - Controller Ready Timeouts</strong></summary>

<!-- claim:BASE3-FIG-057-CLAIM figure-table:BASE3-FIG-057 -->

**SPEC。** Figure 57〈Offset 68h: CRTO - Controller Ready Timeouts〉：定義 offset 68h 的 CRTO（Controller Ready Timeouts），並指出軟體在該位置必須分別解碼的欄位。 先定位 CRTO，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CRIMT, CRWMT, CRTO, CAP.CRMS.CRIMS, CC.EN, CC.CRIME, CRTO.CRIMT, Controller。

#### 這張 Figure 在完整流程中的位置

Figure 57 位於 §3.1.4.21，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CRIMT 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CRIMT]
          ↓
[擷取欄位: CRWMT] → [套用編碼: CRTO]
                                      ↓
[驗證證據: CAP.CRMS.CRIMS]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CRIMT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CRWMT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CRTO` | Controller Ready Timeouts，回報特定 ready mode 所需等待時間的 property。 |
| `CAP.CRMS.CRIMS` | Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.CRMS.CRIMS 進一步指定其中的 CRMS.CRIMS 子欄位。 |
| `CC.EN` | Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.EN 進一步指定其中的 EN 子欄位。 |
| `CC.CRIME` | Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.CRIME 進一步指定其中的 CRIME 子欄位。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.21。
2. 依圖中指定的寬度與位置解碼 CRIMT；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CRWMT 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 57 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.21 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.21 如何排列 CRIMT、CRWMT 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.21 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 57 對應的 raw value 或 buffer，標出包含 CRIMT 的 bytes 並解碼，再獨立核對 CRWMT。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CRIMT，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CRIMT 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CRWMT 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CRIMT, CRWMT, CRTO, CAP.CRMS.CRIMS, CC.EN, CC.CRIME, CRTO.CRIMT, Controller

**來源 keyword 索引：** `should not`, `shall`, `should`, `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.21, Figure 57, 文件頁 73, PDF 頁 99

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 58: Offset E00h: PMRCAP - Persistent Memory Region Capabilities</strong></summary>

<!-- claim:BASE3-FIG-058-CLAIM figure-table:BASE3-FIG-058 -->

**SPEC。** Figure 58〈Offset E00h: PMRCAP - Persistent Memory Region Capabilities〉：定義 offset E00h 的 PMRCAP（Persistent Memory Region Capabilities），並指出軟體在該位置必須分別解碼的欄位。 先定位 PMRCAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CMSS, PMRTO, PMRWBM, CPMTSTSR, CMR, PMRTU, BIR, WDS。

#### 這張 Figure 在完整流程中的位置

Figure 58 位於 §3.1.4.21，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CMSS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CMSS]
          ↓
[擷取欄位: PMRTO] → [套用編碼: PMRWBM]
                                      ↓
[驗證證據: CPMTSTSR]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CMSS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMRTO` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMRWBM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CPMTSTSR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMRTU` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.21。
2. 依圖中指定的寬度與位置解碼 CMSS；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 PMRTO 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 58 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.21 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.21 如何排列 CMSS、PMRTO 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.21 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 58 對應的 raw value 或 buffer，標出包含 CMSS 的 bytes 並解碼，再獨立核對 PMRTO。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CMSS，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CMSS 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 PMRTO 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CMSS, PMRTO, PMRWBM, CPMTSTSR, CMR, PMRTU, BIR, WDS

**來源 keyword 索引：** `shall not`, `shall`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.21, Figure 58, 文件頁 73-74, PDF 頁 99-100

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 59: Offset E04h: PMRCTL - Persistent Memory Region Control</strong></summary>

<!-- claim:BASE3-FIG-059-CLAIM figure-table:BASE3-FIG-059 -->

**SPEC。** Figure 59〈Offset E04h: PMRCTL - Persistent Memory Region Control〉：定義 offset E04h 的 PMRCTL（Persistent Memory Region Control），並指出軟體在該位置必須分別解碼的欄位。 先定位 PMRCTL，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：EN, PMRCTL, PMRSTS.NRDY。

#### 這張 Figure 在完整流程中的位置

Figure 59 位於 §3.1.4.22，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 EN 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: EN]
          ↓
[擷取欄位: PMRCTL] → [套用編碼: PMRSTS.NRDY]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `EN` | Enable，CC 中控制 controller enable state 的 bit。 |
| `PMRCTL` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMRSTS.NRDY` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.22。
2. 依圖中指定的寬度與位置解碼 EN；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 PMRCTL 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 59 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.22 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.22 如何排列 EN、PMRCTL 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.22 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 59 對應的 raw value 或 buffer，標出包含 EN 的 bytes 並解碼，再獨立核對 PMRCTL。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 EN，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 EN 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 PMRCTL 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** EN, PMRCTL, PMRSTS.NRDY

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.22, Figure 59, 文件頁 74, PDF 頁 100

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 60: Offset E08h: PMRSTS - Persistent Memory Region Status</strong></summary>

<!-- claim:BASE3-FIG-060-CLAIM figure-table:BASE3-FIG-060 -->

**SPEC。** Figure 60〈Offset E08h: PMRSTS - Persistent Memory Region Status〉：定義 offset E08h 的 PMRSTS（Persistent Memory Region Status），並指出軟體在該位置必須分別解碼的欄位。 先定位 PMRSTS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CBAI, HSTS, NRDY, ERR, PMRSTS, PMRMSCU.CBA, PMRMSCL.CBA, PMRCAP.CMSS。

#### 這張 Figure 在完整流程中的位置

Figure 60 位於 §3.1.4.23，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CBAI 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CBAI]
          ↓
[擷取欄位: HSTS] → [套用編碼: NRDY]
                                      ↓
[驗證證據: ERR]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CBAI` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `HSTS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NRDY` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ERR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMRSTS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMRMSCU.CBA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.23。
2. 依圖中指定的寬度與位置解碼 CBAI；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 HSTS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 60 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.23 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.23 如何排列 CBAI、HSTS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.23 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 60 對應的 raw value 或 buffer，標出包含 CBAI 的 bytes 並解碼，再獨立核對 HSTS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CBAI，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CBAI 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 HSTS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CBAI, HSTS, NRDY, ERR, PMRSTS, PMRMSCU.CBA, PMRMSCL.CBA, PMRCAP.CMSS

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.23, Figure 60, 文件頁 75, PDF 頁 101

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 61: Offset E0Ch: PMREBS - Persistent Memory Region Elasticity Buffer Size</strong></summary>

<!-- claim:BASE3-FIG-061-CLAIM figure-table:BASE3-FIG-061 -->

**SPEC。** Figure 61〈Offset E0Ch: PMREBS - Persistent Memory Region Elasticity Buffer Size〉：定義 offset E0Ch 的 PMREBS（Persistent Memory Region Elasticity Buffer Size），並指出軟體在該位置必須分別解碼的欄位。 先定位 PMREBS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PMRWBZ, PMRRBB, PMRSZU, PMREBS, PMR。

#### 這張 Figure 在完整流程中的位置

Figure 61 位於 §3.1.4.24，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 PMRWBZ 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PMRWBZ]
          ↓
[擷取欄位: PMRRBB] → [套用編碼: PMRSZU]
                                      ↓
[驗證證據: PMREBS]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PMRWBZ` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMRRBB` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMRSZU` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMREBS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMR` | Persistent Memory Region，由 controller 暴露、具有持久性語意的記憶體區域。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.24。
2. 依圖中指定的寬度與位置解碼 PMRWBZ；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 PMRRBB 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 61 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.24 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.24 如何排列 PMRWBZ、PMRRBB 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.24 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 61 對應的 raw value 或 buffer，標出包含 PMRWBZ 的 bytes 並解碼，再獨立核對 PMRRBB。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 PMRWBZ，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 PMRWBZ 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 PMRRBB 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** PMRWBZ, PMRRBB, PMRSZU, PMREBS, PMR

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.24, Figure 61, 文件頁 76, PDF 頁 102

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 62: Offset E10h: PMRSWTP - Persistent Memory Region Sustained Write Throughput</strong></summary>

<!-- claim:BASE3-FIG-062-CLAIM figure-table:BASE3-FIG-062 -->

**SPEC。** Figure 62〈Offset E10h: PMRSWTP - Persistent Memory Region Sustained Write Throughput〉：定義 offset E10h 的 PMRSWTP（Persistent Memory Region Sustained Write Throughput），並指出軟體在該位置必須分別解碼的欄位。 先定位 PMRSWTP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PMRSWTV, PMRSWTU, PMRSWTP, PMR, TLP, MPS, PXDC。

#### 這張 Figure 在完整流程中的位置

Figure 62 位於 §3.1.4.24，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 PMRSWTV 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PMRSWTV]
          ↓
[擷取欄位: PMRSWTU] → [套用編碼: PMRSWTP]
                                      ↓
[驗證證據: PMR]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PMRSWTV` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMRSWTU` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMRSWTP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMR` | Persistent Memory Region，由 controller 暴露、具有持久性語意的記憶體區域。 |
| `TLP` | Transaction Layer Packet，PCIe transaction layer 傳送的 packet。 |
| `MPS` | Memory Page Size，controller 使用的 memory page 大小設定；影響 queue address 與 PRP 對齊。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.24。
2. 依圖中指定的寬度與位置解碼 PMRSWTV；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 PMRSWTU 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 62 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.24 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.24 如何排列 PMRSWTV、PMRSWTU 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.24 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 62 對應的 raw value 或 buffer，標出包含 PMRSWTV 的 bytes 並解碼，再獨立核對 PMRSWTU。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 PMRSWTV，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 PMRSWTV 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 PMRSWTU 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** PMRSWTV, PMRSWTU, PMRSWTP, PMR, TLP, MPS, PXDC

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.24, Figure 62, 文件頁 76, PDF 頁 102

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 63: Offset E14h: PMRMSCL - Persistent Memory Region Memory Space Control Lower</strong></summary>

<!-- claim:BASE3-FIG-063-CLAIM figure-table:BASE3-FIG-063 -->

**SPEC。** Figure 63〈Offset E14h: PMRMSCL - Persistent Memory Region Memory Space Control Lower〉：定義 offset E14h 的 PMRMSCL（Persistent Memory Region Memory Space Control Lower），並指出軟體在該位置必須分別解碼的欄位。 先定位 PMRMSCL，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CBA, CMSE, PMRMSCL, PMRMSCU.CBA。

#### 這張 Figure 在完整流程中的位置

Figure 63 位於 §3.1.4.26，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CBA 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CBA]
          ↓
[擷取欄位: CMSE] → [套用編碼: PMRMSCL]
                                      ↓
[驗證證據: PMRMSCU.CBA]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CBA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMSE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMRMSCL` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMRMSCU.CBA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.26。
2. 依圖中指定的寬度與位置解碼 CBA；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CMSE 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 63 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.26 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.26 如何排列 CBA、CMSE 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.26 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 63 對應的 raw value 或 buffer，標出包含 CBA 的 bytes 並解碼，再獨立核對 CMSE。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CBA，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CBA 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CMSE 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CBA, CMSE, PMRMSCL, PMRMSCU.CBA

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.26, Figure 63, 文件頁 77, PDF 頁 103

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 64: Offset E18h: PMRMSCU - Persistent Memory Region Memory Space Control Upper</strong></summary>

<!-- claim:BASE3-FIG-064-CLAIM figure-table:BASE3-FIG-064 -->

**SPEC。** Figure 64〈Offset E18h: PMRMSCU - Persistent Memory Region Memory Space Control Upper〉：定義 offset E18h 的 PMRMSCU（Persistent Memory Region Memory Space Control Upper），並指出軟體在該位置必須分別解碼的欄位。 先定位 PMRMSCU，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CBA, PMRMSCU。

#### 這張 Figure 在完整流程中的位置

Figure 64 位於 §3.1.4.26，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CBA 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CBA]
          ↓
[擷取欄位: PMRMSCU] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CBA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMRMSCU` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.26。
2. 依圖中指定的寬度與位置解碼 CBA；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 PMRMSCU 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 64 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.26 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.4.26 如何排列 CBA、PMRMSCU 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.26 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 64 對應的 raw value 或 buffer，標出包含 CBA 的 bytes 並解碼，再獨立核對 PMRMSCU。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CBA，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CBA 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 PMRMSCU 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CBA, PMRMSCU

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.26, Figure 64, 文件頁 77, PDF 頁 103

</details>

<a id="section-3-2"></a>

### §3.2

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 65: NSID Types and Relationship to Namespace</strong></summary>

<!-- claim:BASE3-FIG-065-CLAIM figure-table:BASE3-FIG-065 -->

**SPEC。** Figure 65〈NSID Types and Relationship to Namespace〉：定義〈NSID Types and Relationship to Namespace〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NSID, Namespace。

#### 這張 Figure 在完整流程中的位置

Figure 65 位於 §3.2.1，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NSID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSID]
          ↓
[擷取欄位: Namespace] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSID` | Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。 |
| `Namespace` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.2.1。
2. 依圖中指定的寬度與位置解碼 NSID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Namespace 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 65 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.2.1 如何排列 NSID、Namespace 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.2.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 65 對應的 raw value 或 buffer，標出包含 NSID 的 bytes 並解碼，再獨立核對 Namespace。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NSID，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NSID 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Namespace 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NSID, Namespace

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.1, Figure 65, 文件頁 78-79, PDF 頁 104-105

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 66: NSID Types</strong></summary>

<!-- claim:BASE3-FIG-066-CLAIM figure-table:BASE3-FIG-066 -->

**SPEC。** Figure 66〈NSID Types〉：定義〈NSID Types〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NSID。

#### 這張 Figure 在完整流程中的位置

Figure 66 位於 §3.2.1.5，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NSID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSID]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSID` | Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.2.1.5。
2. 依圖中指定的寬度與位置解碼 NSID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 66 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.2.1.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.2.1.5 如何排列 NSID、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.2.1.5 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 66 對應的 raw value 或 buffer，標出包含 NSID 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NSID，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NSID 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NSID

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.1.5, Figure 66, 文件頁 79, PDF 頁 105

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 67: NVM Sets and Associated Namespaces</strong></summary>

<!-- claim:BASE3-FIG-067-CLAIM figure-table:BASE3-FIG-067 -->

**SPEC。** Figure 67〈NVM Sets and Associated Namespaces〉：呈現〈NVM Sets and Associated Namespaces〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Set, Namespace。

#### 這張 Figure 在完整流程中的位置

Figure 67 位於 §3.2.2，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Set 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NVM Set]
          ↓
[擷取欄位: Namespace] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NVM Set` | NVM Set，把 namespace 與一組共同管理的 NVM 資源建立關聯的容量集合。 |
| `Namespace` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.2.2。
2. 依圖中指定的寬度與位置解碼 NVM Set；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Namespace 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 67 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.2.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.2.2 如何排列 NVM Set、Namespace 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.2.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 67 對應的 raw value 或 buffer，標出包含 NVM Set 的 bytes 並解碼，再獨立核對 Namespace。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NVM Set，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NVM Set 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Namespace 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NVM Set, Namespace

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2, Figure 67, 文件頁 81, PDF 頁 107

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 68: NVM Set Aware Admin Commands</strong></summary>

<!-- claim:BASE3-FIG-068-CLAIM figure-table:BASE3-FIG-068 -->

**SPEC。** Figure 68〈NVM Set Aware Admin Commands〉：呈現〈NVM Set Aware Admin Commands〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Set, Command。

#### 這張 Figure 在完整流程中的位置

Figure 68 位於 §3.2.2，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Set 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NVM Set]
          ↓
[擷取欄位: Command] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NVM Set` | NVM Set，把 namespace 與一組共同管理的 NVM 資源建立關聯的容量集合。 |
| `Command` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.2.2。
2. 依圖中指定的寬度與位置解碼 NVM Set；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Command 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 68 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.2.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.2.2 如何排列 NVM Set、Command 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.2.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 68 對應的 raw value 或 buffer，標出包含 NVM Set 的 bytes 並解碼，再獨立核對 Command。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NVM Set，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NVM Set 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Command 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NVM Set, Command

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2, Figure 68, 文件頁 81, PDF 頁 107

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 69: NVM Sets and Associated Namespaces</strong></summary>

<!-- claim:BASE3-FIG-069-CLAIM figure-table:BASE3-FIG-069 -->

**SPEC。** Figure 69〈NVM Sets and Associated Namespaces〉：呈現〈NVM Sets and Associated Namespaces〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Set, Namespace。

#### 這張 Figure 在完整流程中的位置

Figure 69 位於 §3.2.3，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Set 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NVM Set]
          ↓
[擷取欄位: Namespace] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NVM Set` | NVM Set，把 namespace 與一組共同管理的 NVM 資源建立關聯的容量集合。 |
| `Namespace` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.2.3。
2. 依圖中指定的寬度與位置解碼 NVM Set；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Namespace 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 69 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.2.3 如何排列 NVM Set、Namespace 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.2.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 69 對應的 raw value 或 buffer，標出包含 NVM Set 的 bytes 並解碼，再獨立核對 Namespace。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NVM Set，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NVM Set 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Namespace 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NVM Set, Namespace

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.3, Figure 69, 文件頁 83, PDF 頁 109

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 70: Flexible Data Placement Logical View of Non-Volatile Storage</strong></summary>

<!-- claim:BASE3-FIG-070-CLAIM figure-table:BASE3-FIG-070 -->

**SPEC。** Figure 70〈Flexible Data Placement Logical View of Non-Volatile Storage〉：呈現〈Flexible Data Placement Logical View of Non-Volatile Storage〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：Flexible Data Placement Logical View of Non-Volatile Storage。

#### 這張 Figure 在完整流程中的位置

Figure 70 位於 §3.2.4，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Flexible Data Placement Logical View of Non-Volatile Storage 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Flexible Data Placement Logical View of Non-Volatile Storage]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Flexible Data Placement Logical View of Non-Volatile Storage` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.2.4。
2. 依圖中指定的寬度與位置解碼 Flexible Data Placement Logical View of Non-Volatile Storage；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 70 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.2.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.2.4 如何排列 Flexible Data Placement Logical View of Non-Volatile Storage、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.2.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 70 對應的 raw value 或 buffer，標出包含 Flexible Data Placement Logical View of Non-Volatile Storage 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Flexible Data Placement Logical View of Non-Volatile Storage，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Flexible Data Placement Logical View of Non-Volatile Storage 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Flexible Data Placement Logical View of Non-Volatile Storage

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.4, Figure 70, 文件頁 85, PDF 頁 111

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 71: Example 1 Domain Structure</strong></summary>

<!-- claim:BASE3-FIG-071-CLAIM figure-table:BASE3-FIG-071 -->

**SPEC。** Figure 71〈Example 1 Domain Structure〉：定義〈Example 1 Domain Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Domain。

#### 這張 Figure 在完整流程中的位置

Figure 71 位於 §3.2.5.1，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Domain 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Domain]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Domain` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.2.5.1。
2. 依圖中指定的寬度與位置解碼 Domain；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 71 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.2.5.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.2.5.1 如何排列 Domain、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.2.5.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 71 對應的 raw value 或 buffer，標出包含 Domain 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Domain，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Domain 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Domain

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.5.1, Figure 71, 文件頁 86, PDF 頁 112

</details>

<a id="section-3-3"></a>

### §3.3

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 73: Empty Queue Definition</strong></summary>

<!-- claim:BASE3-FIG-073-CLAIM figure-table:BASE3-FIG-073 -->

**SPEC。** Figure 73〈Empty Queue Definition〉：定義〈Empty Queue Definition〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Empty Queue Definition。

#### 這張 Figure 在完整流程中的位置

Figure 73 位於 §3.3.1.4，在本流程中是「queue」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Empty Queue Definition 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 queue／command flow 圖。先標 host 與 controller 的 ownership，再追 head、tail、phase 或 arbitration 的改變；箭頭代表狀態或 ownership 轉移，不自動代表 command 已完成。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Empty Queue Definition]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Empty Queue Definition` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.3.1.4。
2. 依圖中指定的寬度與位置解碼 Empty Queue Definition；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 73 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.3.1.4 如何排列 Empty Queue Definition、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.3.1.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 73 對應的 raw value 或 buffer，標出包含 Empty Queue Definition 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Empty Queue Definition，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Empty Queue Definition 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Empty Queue Definition

**來源 keyword 索引：** `shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1.4, Figure 73, 文件頁 91, PDF 頁 117

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 74: Full Queue Definition</strong></summary>

<!-- claim:BASE3-FIG-074-CLAIM figure-table:BASE3-FIG-074 -->

**SPEC。** Figure 74〈Full Queue Definition〉：定義〈Full Queue Definition〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Full Queue Definition。

#### 這張 Figure 在完整流程中的位置

Figure 74 位於 §3.3.1.4，在本流程中是「queue」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Full Queue Definition 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 queue／command flow 圖。先標 host 與 controller 的 ownership，再追 head、tail、phase 或 arbitration 的改變；箭頭代表狀態或 ownership 轉移，不自動代表 command 已完成。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Full Queue Definition]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Full Queue Definition` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.3.1.4。
2. 依圖中指定的寬度與位置解碼 Full Queue Definition；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 74 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.3.1.4 如何排列 Full Queue Definition、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.3.1.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 74 對應的 raw value 或 buffer，標出包含 Full Queue Definition 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Full Queue Definition，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Full Queue Definition 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Full Queue Definition

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1.4, Figure 74, 文件頁 91, PDF 頁 117

</details>

<a id="section-3-4"></a>

### §3.4

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 80: Round Robin Arbitration</strong></summary>

<!-- claim:BASE3-FIG-080-CLAIM figure-table:BASE3-FIG-080 -->

**SPEC。** Figure 80〈Round Robin Arbitration〉：呈現〈Round Robin Arbitration〉如何在多個 Submission Queue 間選擇工作。 分別追蹤 priority class、服務順序與 arbiter 選出下一筆 command 的時點；來源索引：Round Robin Arbitration。

#### 這張 Figure 在完整流程中的位置

Figure 80 位於 §3.4.4，在本流程中是「queue」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Round Robin Arbitration 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 queue／command flow 圖。先標 host 與 controller 的 ownership，再追 head、tail、phase 或 arbitration 的改變；箭頭代表狀態或 ownership 轉移，不自動代表 command 已完成。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Round Robin Arbitration]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Round Robin Arbitration` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.4.4。
2. 依圖中指定的寬度與位置解碼 Round Robin Arbitration；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 80 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.4.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.4.4 如何排列 Round Robin Arbitration、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.4.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 80 對應的 raw value 或 buffer，標出包含 Round Robin Arbitration 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Round Robin Arbitration，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Round Robin Arbitration 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Round Robin Arbitration

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.4.4, Figure 80, 文件頁 103, PDF 頁 129

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 81: Weighted Round Robin with Urgent Priority Class Arbitration</strong></summary>

<!-- claim:BASE3-FIG-081-CLAIM figure-table:BASE3-FIG-081 -->

**SPEC。** Figure 81〈Weighted Round Robin with Urgent Priority Class Arbitration〉：呈現〈Weighted Round Robin with Urgent Priority Class Arbitration〉如何在多個 Submission Queue 間選擇工作。 分別追蹤 priority class、服務順序與 arbiter 選出下一筆 command 的時點；來源索引：Weighted Round Robin with Urgent Priority Class Arbitration。

#### 這張 Figure 在完整流程中的位置

Figure 81 位於 §3.4.4.2，在本流程中是「queue」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Weighted Round Robin with Urgent Priority Class Arbitration 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 queue／command flow 圖。先標 host 與 controller 的 ownership，再追 head、tail、phase 或 arbitration 的改變；箭頭代表狀態或 ownership 轉移，不自動代表 command 已完成。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Weighted Round Robin with Urgent Priority Class Arbitration]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Weighted Round Robin with Urgent Priority Class Arbitration` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.4.4.2。
2. 依圖中指定的寬度與位置解碼 Weighted Round Robin with Urgent Priority Class Arbitration；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 81 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.4.4.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.4.4.2 如何排列 Weighted Round Robin with Urgent Priority Class Arbitration、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.4.4.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 81 對應的 raw value 或 buffer，標出包含 Weighted Round Robin with Urgent Priority Class Arbitration 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Weighted Round Robin with Urgent Priority Class Arbitration，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Weighted Round Robin with Urgent Priority Class Arbitration 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Weighted Round Robin with Urgent Priority Class Arbitration

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.4.4.2, Figure 81, 文件頁 104, PDF 頁 130

</details>

<a id="section-3-5"></a>

### §3.5

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 84: Admin Commands Permitted to Return a Status Code of Admin Command Media Not</strong></summary>

<!-- claim:BASE3-FIG-084-CLAIM figure-table:BASE3-FIG-084 -->

**SPEC。** Figure 84〈Admin Commands Permitted to Return a Status Code of Admin Command Media Not〉：定義〈Admin Commands Permitted to Return a Status Code of Admin Command Media Not〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：LBA, TCG, CAP.CRMS, CAP.CRMS.CRWMS, CAP.CRMS.CRIMS, CC.CRIME, Status Code, Command。

#### 這張 Figure 在完整流程中的位置

Figure 84 位於 §3.5.3，在本流程中是「status」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 LBA 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 status／error 分類表。先確定 status 所在資料結構與類別，再解 individual code、控制 bit 與 retry 指示。Reserved value 維持未定義；不要因名稱相似便映射到另一層 error code。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBA]
          ↓
[擷取欄位: TCG] → [套用編碼: CAP.CRMS]
                                      ↓
[驗證證據: CAP.CRMS.CRWMS]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `TCG` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CAP.CRMS` | Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.CRMS 進一步指定其中的 CRMS 子欄位。 |
| `CAP.CRMS.CRWMS` | Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.CRMS.CRWMS 進一步指定其中的 CRMS.CRWMS 子欄位。 |
| `CAP.CRMS.CRIMS` | Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.CRMS.CRIMS 進一步指定其中的 CRMS.CRIMS 子欄位。 |
| `CC.CRIME` | Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.CRIME 進一步指定其中的 CRIME 子欄位。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.5.3。
2. 依圖中指定的寬度與位置解碼 LBA；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 TCG 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 84 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.5.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.5.3 如何排列 LBA、TCG 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.5.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 84 對應的 raw value 或 buffer，標出包含 LBA 的 bytes 並解碼，再獨立核對 TCG。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 LBA，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 LBA 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 TCG 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** LBA, TCG, CAP.CRMS, CAP.CRMS.CRWMS, CAP.CRMS.CRIMS, CC.CRIME, Status Code, Command

**來源 keyword 索引：** `shall`, `should`, `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.5.3, Figure 84, 文件頁 110-111, PDF 頁 136-137

</details>

<a id="section-3-6"></a>

### §3.6

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 85: Shutdown Processing Interactions</strong></summary>

<!-- claim:BASE3-FIG-085-CLAIM figure-table:BASE3-FIG-085 -->

**SPEC。** Figure 85〈Shutdown Processing Interactions〉：呈現〈Shutdown Processing Interactions〉的狀態或時間推進關係。 依箭頭順序追蹤 state 或 time bound，並標出每個 transition 的觀察者；來源索引：Shutdown Processing Interactions。

#### 這張 Figure 在完整流程中的位置

Figure 85 位於 §3.6，在本流程中是「state」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Shutdown Processing Interactions 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 state／timing 圖。沿箭頭記錄 trigger、觀察者、完成條件與 timeout source。相同狀態名稱若位於不同 reset scope，不能推論保留相同 queue 或 controller state。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Shutdown Processing Interactions]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Shutdown Processing Interactions` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.6。
2. 依圖中指定的寬度與位置解碼 Shutdown Processing Interactions；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 85 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.6 如何排列 Shutdown Processing Interactions、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.6 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 85 對應的 raw value 或 buffer，標出包含 Shutdown Processing Interactions 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Shutdown Processing Interactions，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Shutdown Processing Interactions 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Shutdown Processing Interactions

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.6, Figure 85, 文件頁 113, PDF 頁 139

</details>

<a id="section-3-8"></a>

### §3.8

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 86: Simple NVM Subsystem</strong></summary>

<!-- claim:BASE3-FIG-086-CLAIM figure-table:BASE3-FIG-086 -->

**SPEC。** Figure 86〈Simple NVM Subsystem〉：呈現〈Simple NVM Subsystem〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem。

#### 這張 Figure 在完整流程中的位置

Figure 86 位於 §3.8.2，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Subsystem 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

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

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.2。
2. 依圖中指定的寬度與位置解碼 NVM Subsystem；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 86 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.2 如何排列 NVM Subsystem、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 86 對應的 raw value 或 buffer，標出包含 NVM Subsystem 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.8.2, Figure 86, 文件頁 126, PDF 頁 152

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 87: Vertically-Organized NVM Subsystem</strong></summary>

<!-- claim:BASE3-FIG-087-CLAIM figure-table:BASE3-FIG-087 -->

**SPEC。** Figure 87〈Vertically-Organized NVM Subsystem〉：呈現〈Vertically-Organized NVM Subsystem〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NVM Subsystem。

#### 這張 Figure 在完整流程中的位置

Figure 87 位於 §3.8.2.2，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVM Subsystem 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

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

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.2.2。
2. 依圖中指定的寬度與位置解碼 NVM Subsystem；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 87 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.2.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.2.2 如何排列 NVM Subsystem、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.2.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 87 對應的 raw value 或 buffer，標出包含 NVM Subsystem 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.8.2.2, Figure 87, 文件頁 127, PDF 頁 153

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 88: Horizontally-Organized Dual NAND NVM Subsystem</strong></summary>

<!-- claim:BASE3-FIG-088-CLAIM figure-table:BASE3-FIG-088 -->

**SPEC。** Figure 88〈Horizontally-Organized Dual NAND NVM Subsystem〉：呈現〈Horizontally-Organized Dual NAND NVM Subsystem〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NAND, NVM Subsystem。

#### 這張 Figure 在完整流程中的位置

Figure 88 位於 §3.8.2.3，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NAND 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NAND]
          ↓
[擷取欄位: NVM Subsystem] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NAND` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NVM Subsystem` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.2.3。
2. 依圖中指定的寬度與位置解碼 NAND；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NVM Subsystem 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 88 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.2.3 如何排列 NAND、NVM Subsystem 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.2.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 88 對應的 raw value 或 buffer，標出包含 NAND 的 bytes 並解碼，再獨立核對 NVM Subsystem。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NAND，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NAND 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NVM Subsystem 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NAND, NVM Subsystem

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.8.2.3, Figure 88, 文件頁 128, PDF 頁 154

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 89: Capacity Information Field Usage</strong></summary>

<!-- claim:BASE3-FIG-089-CLAIM figure-table:BASE3-FIG-089 -->

**SPEC。** Figure 89〈Capacity Information Field Usage〉：定義〈Capacity Information Field Usage〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TNVMCAP, UNVMCAP, MEGCAP, TEGCAP, UEGCAP。

#### 這張 Figure 在完整流程中的位置

Figure 89 位於 §3.8.3，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 TNVMCAP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TNVMCAP]
          ↓
[擷取欄位: UNVMCAP] → [套用編碼: MEGCAP]
                                      ↓
[驗證證據: TEGCAP]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TNVMCAP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `UNVMCAP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MEGCAP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `TEGCAP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `UEGCAP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.3。
2. 依圖中指定的寬度與位置解碼 TNVMCAP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 UNVMCAP 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 89 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.3 如何排列 TNVMCAP、UNVMCAP 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 89 對應的 raw value 或 buffer，標出包含 TNVMCAP 的 bytes 並解碼，再獨立核對 UNVMCAP。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 TNVMCAP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 TNVMCAP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 UNVMCAP 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** TNVMCAP, UNVMCAP, MEGCAP, TEGCAP, UEGCAP

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.8.3, Figure 89, 文件頁 129, PDF 頁 155

</details>

<a id="section-3-9"></a>

### §3.9

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 90: Detecting Timeout Takes up to 2 * KATT</strong></summary>

<!-- claim:BASE3-FIG-090-CLAIM figure-table:BASE3-FIG-090 -->

**SPEC。** Figure 90〈Detecting Timeout Takes up to 2 * KATT〉：呈現〈Detecting Timeout Takes up to 2 * KATT〉的狀態或時間推進關係。 依箭頭順序追蹤 state 或 time bound，並標出每個 transition 的觀察者；來源索引：KATT。

#### 這張 Figure 在完整流程中的位置

Figure 90 位於 §3.9.4.1，在本流程中是「state」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 KATT 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 state／timing 圖。沿箭頭記錄 trigger、觀察者、完成條件與 timeout source。相同狀態名稱若位於不同 reset scope，不能推論保留相同 queue 或 controller state。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: KATT]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `KATT` | Keep Alive Timeout Total，controller 用於偵測逾時的總時間基準。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.9.4.1。
2. 依圖中指定的寬度與位置解碼 KATT；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 90 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.9.4.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.9.4.1 如何排列 KATT、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.9.4.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 90 對應的 raw value 或 buffer，標出包含 KATT 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 KATT，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 KATT 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** KATT

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.9.4.1, Figure 90, 文件頁 133, PDF 頁 159

</details>

<a id="section-3-10"></a>

### §3.10

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 91: Example Privileged Action Admin Commands</strong></summary>

<!-- claim:BASE3-FIG-091-CLAIM figure-table:BASE3-FIG-091 -->

**SPEC。** Figure 91〈Example Privileged Action Admin Commands〉：界定〈Example Privileged Action Admin Commands〉所示的 privileged operation 邊界。 分開發出 command 的主體，以及授權該操作的 privilege／controller state；來源索引：Command。

#### 這張 Figure 在完整流程中的位置

Figure 91 位於 §3.10，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Command 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Command]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Command` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.10。
2. 依圖中指定的寬度與位置解碼 Command；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 91 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.10 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.10 如何排列 Command、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.10 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 91 對應的 raw value 或 buffer，標出包含 Command 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Command，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Command 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Command

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.10, Figure 91, 文件頁 135, PDF 頁 161

</details>

## 使用與限制

製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata 集合或核准範圍改變時，必須重新核對受影響 claim。

## 自問自答：規則、比較、案例與排錯

以下 20 題均附答案，針對本報告範圍複習。每題保留對應教學單元的來源；數值案例與排錯建議屬說明性內容。

### Q01. 「先分清 controller 類型、ID 與能力」的核心判讀規則是什麼？

<!-- qa:base-ch3-identity-lead -->

**答。**

Controller type 回答『能做哪類工作』，Controller ID 回答『這是哪一個 controller』，support-requirement Figure 回答『在這個上下文中 command／log／feature 的支援強度』。Figures 23-32 應連續閱讀，但三種問題不能合併成一個布林值。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.1, 文件頁 38, PDF 頁 64; 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3-3.1.3.2, 文件頁 39-43, PDF 頁 65-69; 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3, 文件頁 40, PDF 頁 66

### Q02. 「先分清 controller 類型、ID 與能力」中，哪些概念或條件必須分開比較？

<!-- qa:base-ch3-identity-rows -->

**答。**

- I/O controller — 可執行使用者資料 I/O — 仍需逐項查 optional capability
- Administrative controller — 管理用途、無資料 I/O command — 不能因有 Admin Queue 就當成 I/O controller
- support marker — 針對 row 與上下文描述強度 — 不能脫離 column／footnote 解讀

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.1, 文件頁 38, PDF 頁 64; 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3-3.1.3.2, 文件頁 39-43, PDF 頁 65-69; 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3, 文件頁 40, PDF 頁 66

### Q03. 「先分清 controller 類型、ID 與能力」如何套用到具體數值或操作情境？

<!-- qa:base-ch3-identity-example -->

**答。**

說明性範例：偵測到一個 Administrative controller 時，軟體仍會建立 Admin SQ/CQ 並執行管理 command，但不應把 namespace data path 掛到它。若只用『存在 Admin Queue』判斷 controller type，I/O 與 Administrative controller 會被錯誤歸成同類。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.1, 文件頁 38, PDF 頁 64; 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3-3.1.3.2, 文件頁 39-43, PDF 頁 65-69; 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3, 文件頁 40, PDF 頁 66

### Q04. 「先分清 controller 類型、ID 與能力」最容易出現什麼誤判？如何排查？

<!-- qa:base-ch3-identity-pitfall -->

**答。**

能力矩陣解析器要保留 row、column、footnote 與 controller type 四個維度。把 O、M 或條件註記抽成全域 capability，會在另一種 controller 或 command-set context 中得到錯誤結論。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.1, 文件頁 38, PDF 頁 64; 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3-3.1.3.2, 文件頁 39-43, PDF 頁 65-69; 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3, 文件頁 40, PDF 頁 66

### Q05. 「從 CAP 到 CSTS.RDY：初始化是一條有前置條件的狀態機」的核心判讀規則是什麼？

<!-- qa:base-ch3-properties-init-lead -->

**答。**

Properties 不是彼此獨立的 register 清單。CAP 先限制 page size、queue 與 timeout 能力；AQA、ASQ、ACQ 建立 Admin queues；CC 選擇設定並以 EN 啟動；最後由 CSTS.RDY 宣告 controller 已能正常處理命令。Figures 33-46 與 Figure 57 應沿這條因果鏈閱讀。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, 文件頁 52-54, PDF 頁 78-80; 來源：NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, 文件頁 105-113, PDF 頁 131-139

### Q06. 「從 CAP 到 CSTS.RDY：初始化是一條有前置條件的狀態機」中，哪些概念或條件必須分開比較？

<!-- qa:base-ch3-properties-init-rows -->

**答。**

- CAP — 能力與界限 — 在寫設定前讀
- AQA/ASQ/ACQ — Admin queue 大小與位址 — 需符合 page/alignment 能力
- CC — host 選擇與 enable — 寫入值要與 CAP 相容
- CSTS — controller 回報狀態 — RDY/CFS/SHST 不可互相替代

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, 文件頁 52-54, PDF 頁 78-80; 來源：NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, 文件頁 105-113, PDF 頁 131-139

### Q07. 「從 CAP 到 CSTS.RDY：初始化是一條有前置條件的狀態機」如何套用到具體數值或操作情境？

<!-- qa:base-ch3-properties-init-example -->

**答。**

說明性範例：host 選擇 4 KiB MPS，ASQ 與 ACQ base address 因而必須依該 page size 對齊。寫 CC.EN=1 後，host 以 CAP／CRTO 指定的時間界限等待 CSTS.RDY=1；若 CFS 先出現，流程應進入 error recovery，而不是繼續建立 I/O queues。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, 文件頁 52-54, PDF 頁 78-80; 來源：NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, 文件頁 105-113, PDF 頁 131-139

### Q08. 「從 CAP 到 CSTS.RDY：初始化是一條有前置條件的狀態機」最容易出現什麼誤判？如何排查？

<!-- qa:base-ch3-properties-init-pitfall -->

**答。**

初始化 log 至少保留每次 property access 的 offset、width、raw value 與 timestamp。只記『enable failed』無法分辨不相容設定、位址對齊、CFS 或單純尚未超過 ready timeout。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, 文件頁 52-54, PDF 頁 78-80; 來源：NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, 文件頁 105-113, PDF 頁 131-139

### Q09. 「Ring buffer、doorbell 與 arbitration 要分三層理解」的核心判讀規則是什麼？

<!-- qa:base-ch3-queue-arbitration-lead -->

**答。**

Figure 73/74 說明 queue 的 empty/full 判定，Figure 80/81 說明多個 SQ 競爭 controller 服務時的 arbitration。前者處理單一 ring 的 head/tail 狀態，後者處理多個 candidate SQ 的選擇；priority 屬於 SQ，不是每筆 command 自帶的獨立優先權。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1, 文件頁 88-91, PDF 頁 114-117; 來源：NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, 文件頁 101-105, PDF 頁 127-131; 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3, 文件頁 40, PDF 頁 66

### Q10. 「Ring buffer、doorbell 與 arbitration 要分三層理解」中，哪些概念或條件必須分開比較？

<!-- qa:base-ch3-queue-arbitration-rows -->

**答。**

- empty — head == tail 且 phase／ownership 符合 empty 定義 — 沒有可取走 entry
- full — 下一個 tail 會追上尚未釋放 head — host 不得覆寫 entry
- Round Robin — 候選 SQ 輪流取得服務 — 不代表 command completion 依提交順序
- Weighted RR + Urgent — priority class 與 weight 影響選擇 — 仍需依適用設定解讀

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1, 文件頁 88-91, PDF 頁 114-117; 來源：NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, 文件頁 101-105, PDF 頁 127-131; 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3, 文件頁 40, PDF 頁 66

### Q11. 「Ring buffer、doorbell 與 arbitration 要分三層理解」如何套用到具體數值或操作情境？

<!-- qa:base-ch3-queue-arbitration-example -->

**答。**

說明性範例：深度 4 的 SQ 只有四個 slot，但 full/empty 判定還需要 ownership 規則；不能只用 tail-head 的無號差值。若 SQ 1 與 SQ 2 同時有 command，arbiter 先選 SQ 2 也不代表 SQ 2 的 command 一定先完成，因 command 執行時間仍可能不同。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1, 文件頁 88-91, PDF 頁 114-117; 來源：NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, 文件頁 101-105, PDF 頁 127-131; 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3, 文件頁 40, PDF 頁 66

### Q12. 「Ring buffer、doorbell 與 arbitration 要分三層理解」最容易出現什麼誤判？如何排查？

<!-- qa:base-ch3-queue-arbitration-pitfall -->

**答。**

Debug 時分開記錄 software tail、doorbell value、controller-consumed head 與 completion SQHD。四個值混成一個『queue index』會遮蔽 lost doorbell、stale head、slot reuse 與 arbitration starvation 等不同根因。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1, 文件頁 88-91, PDF 頁 114-117; 來源：NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, 文件頁 101-105, PDF 頁 127-131; 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3, 文件頁 40, PDF 頁 66

### Q13. 「CMB、PMR、capacity 與 namespace 是不同資源視角」的核心判讀規則是什麼？

<!-- qa:base-ch3-memory-capacity-lead -->

**答。**

CMB/PMR properties 描述 controller 暴露的 memory region 位置、能力與狀態；capacity Figures 86-89 描述 NVM subsystem 各層級可用或已配置容量。兩者都談 memory，卻不是同一種空間，也不能用同一個『剩餘容量』欄位合併。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, 文件頁 52-54, PDF 頁 78-80; 來源：NVME-BASE-2.4, Rev. 2.4, §3.8, 文件頁 125-129, PDF 頁 151-155; 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, 文件頁 80-85, PDF 頁 106-111

### Q14. 「CMB、PMR、capacity 與 namespace 是不同資源視角」中，哪些概念或條件必須分開比較？

<!-- qa:base-ch3-memory-capacity-rows -->

**答。**

- CMB — controller-provided working memory — 是否能放 SQ/CQ/list/data 由能力 bit 決定
- PMR — 具有持久性語意的 region — enable、ready、error 與 address control 要一起看
- capacity model — subsystem／group／set／namespace 的容量 — 不同層級欄位不可直接相減

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, 文件頁 52-54, PDF 頁 78-80; 來源：NVME-BASE-2.4, Rev. 2.4, §3.8, 文件頁 125-129, PDF 頁 151-155; 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, 文件頁 80-85, PDF 頁 106-111

### Q15. 「CMB、PMR、capacity 與 namespace 是不同資源視角」如何套用到具體數值或操作情境？

<!-- qa:base-ch3-memory-capacity-example -->

**答。**

說明性範例：CMB size 足以容納一個 SQ，不代表 controller 的 namespace 多出同樣容量；前者是 queue/data structure 的放置資源，後者才是 host 可格式化與存取的非揮發性容量。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, 文件頁 52-54, PDF 頁 78-80; 來源：NVME-BASE-2.4, Rev. 2.4, §3.8, 文件頁 125-129, PDF 頁 151-155; 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, 文件頁 80-85, PDF 頁 106-111

### Q16. 「CMB、PMR、capacity 與 namespace 是不同資源視角」最容易出現什麼誤判？如何排查？

<!-- qa:base-ch3-memory-capacity-pitfall -->

**答。**

Memory-map debug 圖至少用不同區塊標 host memory、CMB、PMR 與 namespace media。若 address 屬於 CMB/PMR，還要保留 BIR、BAR base、offset、enable 與 ready 狀態，不能只印最終 CPU virtual address。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, 文件頁 52-54, PDF 頁 78-80; 來源：NVME-BASE-2.4, Rev. 2.4, §3.8, 文件頁 125-129, PDF 頁 151-155; 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, 文件頁 80-85, PDF 頁 106-111

### Q17. 「Shutdown、reset、Keep Alive 與 firmware update 的 recovery 邊界」的核心判讀規則是什麼？

<!-- qa:base-ch3-lifecycle-lead -->

**答。**

Lifecycle 事件的共同問題是『哪一層狀態仍有效』。Normal shutdown 由 CC.SHN/CSTS.SHST 協調，reset 分成 subsystem/controller/queue 層級，Keep Alive 監測 host-controller 存活，firmware activation 又可能要求特定 reset。相同的『暫時無法處理 command』症狀，不代表可以使用相同 recovery。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, 文件頁 113-120, PDF 頁 139-146; 來源：NVME-BASE-2.4, Rev. 2.4, §3.7, 文件頁 120-125, PDF 頁 146-151; 來源：NVME-BASE-2.4, Rev. 2.4, §3.9, 文件頁 129-135, PDF 頁 155-161; 來源：NVME-BASE-2.4, Rev. 2.4, §3.10-3.11, 文件頁 135-138, PDF 頁 161-164

### Q18. 「Shutdown、reset、Keep Alive 與 firmware update 的 recovery 邊界」中，哪些概念或條件必須分開比較？

<!-- qa:base-ch3-lifecycle-rows -->

**答。**

- normal shutdown — 保護性停止與狀態回報 — 看 SHN/SHST
- controller reset — controller 層級狀態 — queue 是否保留要依 reset 類型
- NVM subsystem reset — 更大 subsystem scope — 可能影響多個 controllers
- Keep Alive timeout — liveness failure — 不能直接等同 media failure

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, 文件頁 113-120, PDF 頁 139-146; 來源：NVME-BASE-2.4, Rev. 2.4, §3.7, 文件頁 120-125, PDF 頁 146-151; 來源：NVME-BASE-2.4, Rev. 2.4, §3.9, 文件頁 129-135, PDF 頁 155-161; 來源：NVME-BASE-2.4, Rev. 2.4, §3.10-3.11, 文件頁 135-138, PDF 頁 161-164

### Q19. 「Shutdown、reset、Keep Alive 與 firmware update 的 recovery 邊界」如何套用到具體數值或操作情境？

<!-- qa:base-ch3-lifecycle-example -->

**答。**

說明性範例：host 要做 normal shutdown 時先停止提交新 I/O，設定 CC.SHN，再監看 CSTS.SHST。若等待期間發生 controller fatal status，後續 recovery 應按 reset scope 重建資源，而不是假設 normal shutdown 已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, 文件頁 113-120, PDF 頁 139-146; 來源：NVME-BASE-2.4, Rev. 2.4, §3.7, 文件頁 120-125, PDF 頁 146-151; 來源：NVME-BASE-2.4, Rev. 2.4, §3.9, 文件頁 129-135, PDF 頁 155-161; 來源：NVME-BASE-2.4, Rev. 2.4, §3.10-3.11, 文件頁 135-138, PDF 頁 161-164

### Q20. 「Shutdown、reset、Keep Alive 與 firmware update 的 recovery 邊界」最容易出現什麼誤判？如何排查？

<!-- qa:base-ch3-lifecycle-pitfall -->

**答。**

Recovery trace 必須記錄 trigger、scope、開始/完成 timestamp、timeout source 與重建清單。只記『reset device』會讓 queue-level、controller-level 與 subsystem-level state loss 無法區分。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, 文件頁 113-120, PDF 頁 139-146; 來源：NVME-BASE-2.4, Rev. 2.4, §3.7, 文件頁 120-125, PDF 頁 146-151; 來源：NVME-BASE-2.4, Rev. 2.4, §3.9, 文件頁 129-135, PDF 頁 155-161; 來源：NVME-BASE-2.4, Rev. 2.4, §3.10-3.11, 文件頁 135-138, PDF 頁 161-164
