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
[English]({% post_url 2026-08-28-nvme-pcie-transport-1-4-en %})


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

## 先學縮寫：完整 Glossary

下列縮寫會在投影片主線使用前先定義。縮寫本身永遠不夠；設計與 Debug 還要保留 owner、width、unit、scope 與 state。

| 縮寫／名詞 | 白話解釋 | 來源 |
|---|---|---|
| `PCIe` | PCI Express，NVMe memory-based controller 使用的 transport 與裝置互連。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§2，文件頁 8，PDF 頁 8 |
| `NVMe` | Non-Volatile Memory Express，主機與非揮發性記憶體子系統之間的介面規範家族。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§1.2，文件頁 6，PDF 頁 6 |
| `MMIO` | Memory-Mapped I/O，以 CPU memory access 形式讀寫裝置 register。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.1，文件頁 9-10，PDF 頁 9-10 |
| `BAR` | Base Address Register，PCI configuration space 中用來定位裝置 memory space 的 register。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.1，文件頁 9-10，PDF 頁 9-10 |
| `CAP` | Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.1.2.1-3.1.2.2，文件頁 10-11，PDF 頁 10-11 |
| `DSTRD` | Doorbell Stride，CAP 中決定相鄰 doorbell register 間距的欄位。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.1.2.1-3.1.2.2，文件頁 10-11，PDF 頁 10-11 |
| `SQ` | Submission Queue，主機放入命令的提交佇列。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.4，文件頁 12-13，PDF 頁 12-13 |
| `CQ` | Completion Queue，controller 放入完成結果的完成佇列。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.4，文件頁 12-13，PDF 頁 12-13 |
| `SQE` | Submission Queue Entry，SQ 中的一筆命令資料結構。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.4，文件頁 12-13，PDF 頁 12-13 |
| `CQE` | Completion Queue Entry，CQ 中的一筆完成結果資料結構。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.4，文件頁 12-13，PDF 頁 12-13 |
| `SQyTDBL` | Submission Queue y Tail Doorbell，host 用來公布 SQ y 新 tail 的 MMIO register。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.1.2.1-3.1.2.2，文件頁 10-11，PDF 頁 10-11 |
| `CQyHDBL` | Completion Queue y Head Doorbell，host 用來公布 CQ y 已消費 head 的 MMIO register。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.1.2.1-3.1.2.2，文件頁 10-11，PDF 頁 10-11 |
| `MSI` | Message Signaled Interrupt，透過 memory write message 傳遞 interrupt 的 PCI 機制。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.5，文件頁 13-16，PDF 頁 13-16 |
| `MSI-X` | MSI-X，提供較多 vectors、獨立遮罩與 table 的延伸 message-signaled interrupt 機制。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.5，文件頁 13-16，PDF 頁 13-16 |
| `IV` | Interrupt Vector，Completion Queue 指定的 interrupt vector 編號。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.2，文件頁 11，PDF 頁 11 |
| `FLR` | Function Level Reset，只重設一個 PCIe Function 的 reset 方法。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.3，文件頁 11-12，PDF 頁 11-12 |
| `AER` | Advanced Error Reporting，PCIe 用來分類、遮罩與記錄 link／transaction error 的 capability。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.7，文件頁 16，PDF 頁 16 |
| `TLP` | Transaction Layer Packet，PCIe transaction layer 傳送的 packet。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.7，文件頁 16，PDF 頁 16 |
| `MPS (PCIe)` | Max Payload Size，PCIe Device Control 中限制 TLP payload 大小的設定。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.8.1-3.8.7，文件頁 16-35，PDF 頁 16-35 |
| `MRRS` | Max Read Request Size，PCIe Function 可發出之 read request 的最大大小設定。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.8.1-3.8.7，文件頁 16-35，PDF 頁 16-35 |
| `PMCAP` | Power Management Capability，PCI power-management capability 結構的基底位置。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.8.1-3.8.7，文件頁 16-35，PDF 頁 16-35 |
| `MSICAP` | MSI Capability，MSI capability 結構的基底位置。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.8.1-3.8.7，文件頁 16-35，PDF 頁 16-35 |
| `MSIXCAP` | MSI-X Capability，MSI-X capability 結構的基底位置。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.8.1-3.8.7，文件頁 16-35，PDF 頁 16-35 |
| `PXCAP` | PCI Express Capability，PCIe capability 結構的基底位置。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.8.1-3.8.7，文件頁 16-35，PDF 頁 16-35 |
| `AERCAP` | Advanced Error Reporting Capability，AER extended capability 結構的基底位置。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.8.1-3.8.7，文件頁 16-35，PDF 頁 16-35 |
| `BIR` | BAR Indicator Register，指出某個記憶體結構位於哪一個 PCIe BAR。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.8.1-3.8.7，文件頁 16-35，PDF 頁 16-35 |
| `PBA` | Pending Bit Array，MSI-X 中記錄尚待處理 vector 的 bit array。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.8.1-3.8.7，文件頁 16-35，PDF 頁 16-35 |
| `EOM` | Eye Opening Measurement，量測 PCIe receiver eye opening 的程序與 log data。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.9，文件頁 39-46，PDF 頁 39-46 |
| `TDISP` | TEE Device Interface Security Protocol，平台隔離與裝置介面狀態相關的 PCIe 安全協定。 | NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.8.8-3.8.10，文件頁 35-39，PDF 頁 35-39 |

## Visual Atlas：先用圖建立整體位置

每張教學重畫回答不同問題：Architecture 定位元件、Sequence 顯示 ownership、Decode 把 bits 轉成工程值、State 保留 failure evidence；它們不是 Spec 原圖的複製。

### Visual 01: Base 定義 NVMe，PCIe Transport 定義它如何落在 PCIe 上

**View type:** `architecture`

```text
[Base command/queue/status]
  ├─ [PCIe memory binding]
  ├─ [BAR/MMIO/host memory]
  ├─ [PCIe transaction/link]
  └─ [controller execution]
```

**回答的問題：** Figure 1 說明文件適用關係，Figure 2 再把 protocol responsibility 分層。工程上應把『command 語意』與『如何透過 host memory、MMIO、configuration space、interrupt 傳送』分開查證；Transport 發現衝突時不能改寫 Base。

**支援 Figure：** Figure 1, Figure 2

**來源：** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§1.2，文件頁 6，PDF 頁 6; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§1.3，文件頁 6-7，PDF 頁 6-7; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§2，文件頁 8，PDF 頁 8

### Visual 02: 從 BAR 到 doorbell offset：每一步都保留單位

**View type:** `decode`

```text
[RAW: 讀 BAR0/BAR1] → [LOCATE: 建立 MMIO base] → [DECODE: 讀 CAP.DSTRD]
[VALIDATE: 算 stride=4<<DSTRD] → [APPLY: 帶入 queue y 與 SQ/CQ index] → [EVIDENCE: 以合法 width 存取]
VALIDATE fail ──→ return to RAW evidence
```

**回答的問題：** NVMe controller registers 位於 BAR0/BAR1 指定的 memory space。Doorbell 從 1000h 起，queue y 的 SQ tail 與 CQ head 依 CAP.DSTRD 計算間距。Figures 3-6 要連成 address derivation，而不是四張獨立 register 表。

**支援 Figure：** Figure 3, Figure 4, Figure 5, Figure 6

**來源：** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.1，文件頁 9-10，PDF 頁 9-10; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.1.2.1-3.1.2.2，文件頁 10-11，PDF 頁 10-11

### Visual 03: Figure 8 的八步 command processing 是 ownership handoff

**View type:** `sequence`

```text
Host / software        Shared object        Controller / evidence
Host → Shared: 1 host 寫 SQE
Shared → Controller: 2 host 寫 SQ tail doorbell
Controller → Shared: 3 controller fetch
Shared → Host: 4 execute
Host → Shared: 5 controller 寫 CQE
Shared → Controller: 6 interrupt
```

**回答的問題：** SQE、doorbell、controller fetch、CQE、interrupt 與 CQ head 不是同一個事件的不同名稱，而是 host/controller 之間逐步移交 ownership。正確順序同時決定 memory ordering 與資源何時可重用。

**支援 Figure：** Figure 7, Figure 8

**來源：** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.4，文件頁 12-13，PDF 頁 12-13; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.2，文件頁 11，PDF 頁 11

### Visual 04: Interrupt mode 比較：vector 數量、遮罩與 latency 是三個維度

**View type:** `sequence`

```text
Host / software        Shared object        Controller / evidence
Host → Shared: 選 interrupt capability
Shared → Controller: 配置 enable/vector
Controller → Shared: 建立 CQ 時指定 IV
Shared → Host: controller 產生 interrupt
Host → Shared: host service 所有相關 CQ
Shared → Controller: 必要時調 coalescing
```

**回答的問題：** pin-based、single-message MSI、multiple-message MSI 與 MSI-X 的差異不只效能。它們提供的 vector 數、masking 位置與 capability structure 不同；interrupt coalescing 另外決定多個 completion 何時合併通知。Figure 9 與 Figures 34-46 應配合 queue-to-vector mapping 閱讀。

**支援 Figure：** Figure 9, Figure 34, Figure 35, Figure 36, Figure 37, Figure 38, Figure 39, Figure 40, Figure 41, Figure 42, Figure 43, Figure 44, Figure 45, Figure 46

**來源：** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.5，文件頁 13-16，PDF 頁 13-16; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.2，文件頁 11，PDF 頁 11; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§Annex A，文件頁 47-48，PDF 頁 47-48

### Visual 05: Configuration space 是 capability map；AER 是 transport error map

**View type:** `decode`

```text
[RAW: 讀 Type 0 header] → [LOCATE: 定位 capability chain] → [DECODE: 解析 PM/MSI/MSI-X/PXCAP]
[VALIDATE: 定位 AERCAP] → [APPLY: 讀 status+mask+severity] → [EVIDENCE: 必要時保存 header/TLP prefix]
VALIDATE fail ──→ return to RAW evidence
```

**回答的問題：** Figures 10-67 從 Type 0 header 走到 Power Management、MSI/MSI-X、PCIe capability 與 AER。閱讀順序應先找 capability pointer／extended capability，再以該 capability base 加 offset；AER status/mask/severity/header log 應視為一組，不可只截取單一 error bit。

**支援 Figure：** Figure 10, Figure 11, Figure 12, Figure 13, Figure 14, Figure 15, Figure 16, Figure 17, Figure 18, Figure 19, Figure 20, Figure 21, Figure 22, Figure 23, Figure 24, Figure 25, Figure 26, Figure 27, Figure 28, Figure 29, Figure 30, Figure 31, Figure 32, Figure 33, Figure 34, Figure 35, Figure 36, Figure 37, Figure 38, Figure 39, Figure 40, Figure 41, Figure 42, Figure 43, Figure 44, Figure 45, Figure 46, Figure 47, Figure 48, Figure 49, Figure 50, Figure 51, Figure 52, Figure 53, Figure 54, Figure 55, Figure 56, Figure 57, Figure 58, Figure 59, Figure 60, Figure 61, Figure 62, Figure 63, Figure 64, Figure 65, Figure 66, Figure 67

**來源：** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.8.1-3.8.7，文件頁 16-35，PDF 頁 16-35; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.7，文件頁 16，PDF 頁 16; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.6，文件頁 16，PDF 頁 16

### Visual 06: EOM parser：先 size，再 header，再 lane descriptor

**View type:** `decode`

```text
[RAW: 確認 LID/support] → [LOCATE: 查所需 size] → [DECODE: 配置 buffer 並取 log]
[VALIDATE: 驗證 header/count] → [APPLY: 逐 lane 解析 descriptor] → [EVIDENCE: 依 unit/scale 解 measurement]
VALIDATE fail ──→ return to RAW evidence
```

**回答的問題：** Physical Interface Receiver Eye Opening Measurement log page 是變長資料結構。host 先確認 support 與需要的大小，再讀 specific parameter/identifier、header、lane descriptor 與 measurement data。Figures 70-77 應形成 parser pipeline，而不是把每個欄位表獨立翻譯。

**支援 Figure：** Figure 70, Figure 71, Figure 72, Figure 73, Figure 74, Figure 75, Figure 76, Figure 77

**來源：** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.9，文件頁 39-46，PDF 頁 39-46; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§Annex A，文件頁 47-48，PDF 頁 47-48

## Mental Model 與完整教學流程

以下依工程因果而非 Spec section 排列；相關 Figure 會回到它支援的流程節點，不以編號順序取代教學故事線。

### Module 01: Base 定義 NVMe，PCIe Transport 定義它如何落在 PCIe 上

**解釋。** Figure 1 說明文件適用關係，Figure 2 再把 protocol responsibility 分層。工程上應把『command 語意』與『如何透過 host memory、MMIO、configuration space、interrupt 傳送』分開查證；Transport 發現衝突時不能改寫 Base。

```text
Base command/queue/status
  ↓
PCIe memory binding
  ↓
BAR/MMIO/host memory
  ↓
PCIe transaction/link
  ↓
controller execution
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Base | command 與 completion 的共通語意 | 最高優先序的 NVMe 定義 |
| PCIe Transport | address、register、doorbell、interrupt 綁定 | 補充 PCIe-specific 要求 |
| PCI-SIG 規格 | 原生 PCIe capability/transaction 語意 | 本報告只引用來源明載的 NVMe-specific 部分 |

**說明性範例。** 說明性範例：Firmware Commit 的 CA/FS 與 status code 在 Base 解讀；SQE 放在 host memory、doorbell 位於 BAR0/1 memory space、completion 如何觸發 MSI-X，則由 PCIe Transport 補足。

**常見誤解／Debug。** 設計文件的每個欄位旁標 owner specification。若一個 bug report 把 command status、PCIe AER 與 device register access 混成『NVMe error』，recovery 層級通常也會選錯。

**支援來源：** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§1.2，文件頁 6，PDF 頁 6; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§1.3，文件頁 6-7，PDF 頁 6-7; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§2，文件頁 8，PDF 頁 8

**關聯 Figure：** Figure 1, Figure 2

### Module 02: 從 BAR 到 doorbell offset：每一步都保留單位

**解釋。** NVMe controller registers 位於 BAR0/BAR1 指定的 memory space。Doorbell 從 1000h 起，queue y 的 SQ tail 與 CQ head 依 CAP.DSTRD 計算間距。Figures 3-6 要連成 address derivation，而不是四張獨立 register 表。

```text
讀 BAR0/BAR1
  ↓
建立 MMIO base
  ↓
讀 CAP.DSTRD
  ↓
算 stride=4<<DSTRD
  ↓
帶入 queue y 與 SQ/CQ index
  ↓
以合法 width 存取
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| SQ y tail | 1000h + (2y) × (4 << DSTRD) | host 公布新 SQ tail |
| CQ y head | 1000h + (2y+1) × (4 << DSTRD) | host 公布已消費 CQ head |
| doorbell value | queue pointer | 不含 SQE/CQE 本體 |

**說明性範例。** 說明性範例：DSTRD=1，stride=4<<1=8 bytes。queue 3 的 SQ tail offset =1000h+(6×8)=1030h；CQ head offset =1000h+(7×8)=1038h。兩者只差一個 stride。若把 DSTRD 當成 byte count，所有非零 DSTRD 的 doorbell 位址都會錯。

**常見誤解／Debug。** doorbell trace 保存 BAR base、DSTRD、queue ID、公式中間值、final physical address、written pointer 與 access width。若 only log final virtual address，無法辨別 BAR mapping、stride 或 queue index 哪一步出錯。

**支援來源：** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.1，文件頁 9-10，PDF 頁 9-10; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.1.2.1-3.1.2.2，文件頁 10-11，PDF 頁 10-11

**關聯 Figure：** Figure 3, Figure 4, Figure 5, Figure 6

### Module 03: Figure 8 的八步 command processing 是 ownership handoff

**解釋。** SQE、doorbell、controller fetch、CQE、interrupt 與 CQ head 不是同一個事件的不同名稱，而是 host/controller 之間逐步移交 ownership。正確順序同時決定 memory ordering 與資源何時可重用。

```text
1 host 寫 SQE
  ↓
2 host 寫 SQ tail doorbell
  ↓
3 controller fetch
  ↓
4 execute
  ↓
5 controller 寫 CQE
  ↓
6 interrupt
  ↓
7 host 處理 CQE
  ↓
8 host 寫 CQ head doorbell
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| SQ slot reuse | controller 已消費該 SQE | 由完成資訊的 SQHD 協助追蹤 |
| command buffer reuse | command 已 completion 且資料可見 | 依 command/data direction 核對 |
| CQ slot release | host 已完整消費 CQE | 之後才寫 CQ head doorbell |

**說明性範例。** 說明性範例：host 先寫 doorbell、後補 SQE 的最後一個 dword，controller 可能 fetch 到半成品。另一個方向，host 在讀完 CQE 前先更新 CQ head，controller 可能重用該 CQ slot。兩者都是 ownership 順序錯誤，不是 command opcode 問題。

**常見誤解／Debug。** 時間軸同時記錄 CPU core、SQ tail、doorbell MMIO、SQHD、CQ phase、interrupt vector 與 CQ head。分散在不同 log 的事件需用 CID/SQID 與 timestamp 對齊，才能定位 lost interrupt、stale phase 或 memory-ordering 問題。

**支援來源：** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.4，文件頁 12-13，PDF 頁 12-13; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.2，文件頁 11，PDF 頁 11

**關聯 Figure：** Figure 7, Figure 8

### Module 04: Interrupt mode 比較：vector 數量、遮罩與 latency 是三個維度

**解釋。** pin-based、single-message MSI、multiple-message MSI 與 MSI-X 的差異不只效能。它們提供的 vector 數、masking 位置與 capability structure 不同；interrupt coalescing 另外決定多個 completion 何時合併通知。Figure 9 與 Figures 34-46 應配合 queue-to-vector mapping 閱讀。

```text
選 interrupt capability
  ↓
配置 enable/vector
  ↓
建立 CQ 時指定 IV
  ↓
controller 產生 interrupt
  ↓
host service 所有相關 CQ
  ↓
必要時調 coalescing
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| pin-based | 傳統共享線路 | 共享與 masking 行為不同 |
| single MSI | 單一 message/vector | 多個 CQ 可能共享服務路徑 |
| multiple MSI | 一組連續 messages | 受 MME/MMC 等能力限制 |
| MSI-X | table-based 多 vectors、獨立 mask | 規格建議優先使用 |

**說明性範例。** 說明性範例：CQ 1 與 CQ 2 共用 vector 5。收到 vector 5 時，handler 不能只檢查 CQ 1；它必須處理所有映射到該 vector 的相關 CQs。提高 coalescing threshold 可減少 interrupts，但可能增加 CQE 等待時間。

**常見誤解／Debug。** Interrupt debug 分開檢查 capability enable、CQ IV、MSI/MSI-X mask、pending state、controller CQE 與 host handler。只有『沒有進 ISR』不足以判斷是 controller 沒送、PCIe 沒傳、vector 被 mask 或 handler 漏掃 CQ。

**支援來源：** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.5，文件頁 13-16，PDF 頁 13-16; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.2，文件頁 11，PDF 頁 11; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§Annex A，文件頁 47-48，PDF 頁 47-48

**關聯 Figure：** Figure 9, Figure 34, Figure 35, Figure 36, Figure 37, Figure 38, Figure 39, Figure 40, Figure 41, Figure 42, Figure 43, Figure 44, Figure 45, Figure 46

### Module 05: Configuration space 是 capability map；AER 是 transport error map

**解釋。** Figures 10-67 從 Type 0 header 走到 Power Management、MSI/MSI-X、PCIe capability 與 AER。閱讀順序應先找 capability pointer／extended capability，再以該 capability base 加 offset；AER status/mask/severity/header log 應視為一組，不可只截取單一 error bit。

```text
讀 Type 0 header
  ↓
定位 capability chain
  ↓
解析 PM/MSI/MSI-X/PXCAP
  ↓
定位 AERCAP
  ↓
讀 status+mask+severity
  ↓
必要時保存 header/TLP prefix
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| NVMe CQE status | command 執行結果 | 由 NVMe command context 解 |
| PCIe Device Status | PCIe Function 狀態摘要 | 位於 PCIe capability |
| AER | correctable/uncorrectable transport errors | status、mask、severity、header 一起看 |
| power state | slot limit 與 device power 控制 | 不得選超過 slot power limit 的 NVMe state |

**說明性範例。** 說明性範例：AERUCES 某 bit 被設為 1，先查對應 mask 判斷是否會回報，再查 severity 判斷錯誤嚴重程度及其處置，最後用 header log 取得 transaction context。不能把該 bit 直接翻成某個 NVMe SC。

**常見誤解／Debug。** configuration dump 要保留 capability base，而不只保存 register value。相同 offset 若相對於不同 capability base 會指到不同欄位；AER snapshot 也應在清除 RW1C status 前一次保存完整集合。

**支援來源：** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.8.1-3.8.7，文件頁 16-35，PDF 頁 16-35; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.7，文件頁 16，PDF 頁 16; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.6，文件頁 16，PDF 頁 16

**關聯 Figure：** Figure 10, Figure 11, Figure 12, Figure 13, Figure 14, Figure 15, Figure 16, Figure 17, Figure 18, Figure 19, Figure 20, Figure 21, Figure 22, Figure 23, Figure 24, Figure 25, Figure 26, Figure 27, Figure 28, Figure 29, Figure 30, Figure 31, Figure 32, Figure 33, Figure 34, Figure 35, Figure 36, Figure 37, Figure 38, Figure 39, Figure 40, Figure 41, Figure 42, Figure 43, Figure 44, Figure 45, Figure 46, Figure 47, Figure 48, Figure 49, Figure 50, Figure 51, Figure 52, Figure 53, Figure 54, Figure 55, Figure 56, Figure 57, Figure 58, Figure 59, Figure 60, Figure 61, Figure 62, Figure 63, Figure 64, Figure 65, Figure 66, Figure 67

### Module 06: EOM parser：先 size，再 header，再 lane descriptor

**解釋。** Physical Interface Receiver Eye Opening Measurement log page 是變長資料結構。host 先確認 support 與需要的大小，再讀 specific parameter/identifier、header、lane descriptor 與 measurement data。Figures 70-77 應形成 parser pipeline，而不是把每個欄位表獨立翻譯。

```text
確認 LID/support
  ↓
查所需 size
  ↓
配置 buffer 並取 log
  ↓
驗證 header/count
  ↓
逐 lane 解析 descriptor
  ↓
依 unit/scale 解 measurement
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| specific parameter | 選量測動作與品質/狀態 | 先決定 request context |
| specific identifier | 選 lane/test context | 避免把不同量測混在一起 |
| header | 全域長度與配置 | 所有後續 offset 的基準 |
| lane descriptor | 每 lane 邊界/狀態 | 只在 buffer 內走訪 |

**說明性範例。** 說明性範例：header 宣稱有 8 個 lane descriptors，但 buffer length 只能容納 6 個完整 descriptors。parser 應回報 truncated structure 並停止，不得根據平台預期 lane count 讀過 buffer 結尾。

**常見誤解／Debug。** 保存 request parameter、identifier、returned byte count、header-declared size、lane number 與 measurement status。只有最終 eye 圖不足以重現 selector、length 或 lane mapping 錯誤。

**支援來源：** NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§3.9，文件頁 39-46，PDF 頁 39-46; NVME-PCIE-TRANSPORT-1.4 Rev. 1.4，§Annex A，文件頁 47-48，PDF 頁 47-48

**關聯 Figure：** Figure 70, Figure 71, Figure 72, Figure 73, Figure 74, Figure 75, Figure 76, Figure 77

## 可追溯的規格重點

前面的 Mental Model 解釋因果；本節保留每個可追溯結論與 normative 強度，供講者備註與審查。

### 1. Transport 與 Base 的優先序

<!-- claim:PCIE14-SCOPE -->

PCIe Transport 補充 Base Specification，定義 PCIe 專屬資料結構、延伸、要求與行為；通用 NVMe 行為仍由 Base 定義。規格衝突時 Base 的優先序高於 Transport。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, 文件頁 6, PDF 頁 6

### 2. PCIe Reset 欄定義

<!-- claim:PCIE14-CONVENTION -->

本文件沿用 Base 的 conventions；register／property 表格中的 Reset 欄改表示依 PCI 或 PCIe 規格定義之 reset 後欄位值。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.3, 文件頁 6-7, PDF 頁 6-7

### 3. Transport 規範性用語

<!-- claim:PCIE14-KEYWORDS -->

shall、may 與 should 的語氣仍由 Base 2.4 定義；Transport 摘要不得自行提高或降低規範強度。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §1.4.1, 文件頁 2-3, PDF 頁 28-29

### 4. PCIe transport 概觀

<!-- claim:PCIE14-OVERVIEW -->

PCIe transport 使用 memory-mapped I/O 進行資料與 register 存取，並使用 PCIe configuration space 與 message-signaled interrupt。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, 文件頁 8, PDF 頁 8

### 5. BAR 與 register 存取

<!-- claim:PCIE14-MMIO -->

NVMe controller registers 位於 BAR0／BAR1 所指定的 memory space。host 必須（shall）使用 native width 或 aligned 32-bit access，不得發出 locked access；違反時行為未定義。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, 文件頁 9-10, PDF 頁 9-10

### 6. SQ／CQ doorbell offset

<!-- claim:PCIE14-DOORBELL -->

SQ tail 與 CQ head doorbell 從 offset 1000h 起，實際 stride 由 CAP.DSTRD 決定；queue identifier y 參與 offset 計算。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, 文件頁 10-11, PDF 頁 10-11

### 7. queue 與 interrupt vector

<!-- claim:PCIE14-QUEUE -->

PCIe 支援多個 Submission Queues 共用一個 Completion Queue。建立 CQ 時若啟用 interrupt，Interrupt Vector 必須（shall）初始化成對應 MSI-X 或 multiple-message MSI vector。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, 文件頁 11, PDF 頁 11

### 8. PCIe reset recovery

<!-- claim:PCIE14-RESET -->

PCIe reset 來源包含 Base 定義的 controller/reset 流程與 PCIe 層級 reset。Recovery 設計要以 reset 類型判斷 controller property、queue 與 PCI configuration state。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.3, 文件頁 11-12, PDF 頁 11-12

### 9. PCIe command flow

<!-- claim:PCIE14-COMMAND -->

command flow 是：寫 SQE、更新 SQ tail doorbell、controller 取走與執行、寫 CQE、發出 interrupt（若啟用）、host 處理 CQE、更新 CQ head doorbell。doorbell 只通告 pointer，不攜帶 command 本體。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, 文件頁 12-13, PDF 頁 12-13

### 10. interrupt 模式與延遲

<!-- claim:PCIE14-INTERRUPT -->

可用模式為 pin-based、single-message MSI、multiple-message MSI 與 MSI-X。規格建議 MSI-X；coalescing 可降低 interrupt rate，但通常增加 latency。Admin CQ 的 interrupt 不宜（should not）延遲。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, 文件頁 13-16, PDF 頁 13-16

### 11. slot power limit

<!-- claim:PCIE14-POWER -->

host 絕不可（shall never）選擇功耗高於 PCIe slot power limit 的 NVMe power state；違反時 power behavior 未定義。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.6, 文件頁 16, PDF 頁 16

### 12. NVMe 與 PCIe error 分層

<!-- claim:PCIE14-ERROR -->

NVMe command error 由 CQE status 回報；PCIe transport／link error 則依 PCIe 機制與本文件的 NVMe-specific 要求處理，兩者的 recovery 層級不同。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, 文件頁 16, PDF 頁 16

### 13. PCI configuration requirements

<!-- claim:PCIE14-CONFIG -->

§3.8 逐欄定義 NVMe controller 的 PCI header、Power Management、MSI／MSI-X、PCIe capability 與 AER 額外要求。PCI／PCIe 原始欄位語意仍以 PCI-SIG 規格為準。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, 文件頁 16-35, PDF 頁 16-35

### 14. 平台安全與隔離依賴

<!-- claim:PCIE14-SECURITY -->

power-loss signaling、confidential computing 與 TDISP 把平台事件或隔離狀態映射到 NVMe controller 行為；實作仍需要本次未提供的外部 PCIe／TDISP 規格。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.8-3.8.10, 文件頁 35-39, PDF 頁 35-39

### 15. receiver eye measurement

<!-- claim:PCIE14-EOM -->

Physical Interface Receiver Eye Opening Measurement log page 以 header、lane descriptor 與 EOM data 回報量測；host 先查支援與大小，再依 lane／parameter 解析。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, 文件頁 39-46, PDF 頁 39-46

### 16. host implementation checklist

<!-- claim:PCIE14-HOST -->

Annex A 是 informative host checklist：提交時先寫 SQE 再 doorbell；完成時以 phase 判斷新 CQE，完成讀取後再推進 CQ head；interrupt handler 要處理同 vector 的所有相關 CQ。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

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

## Figure／欄位表教學參考

本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。欄位與 keyword 索引來自本機核對過的 PDF。

<a id="section-1-2"></a>

### §1.2

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 1: NVMe Family of Specifications</strong></summary>

<!-- claim:PCIE14-FIG-001-CLAIM figure-table:PCIE14-FIG-001 -->

**SPEC。** Figure 1〈NVMe Family of Specifications〉：定位〈NVMe Family of Specifications〉在 NVMe 文件與 command set 階層中的位置。 由共通 Base 要求往 transport 與 command set 分支閱讀，並分開核對：NVMe Family。

#### 這張 Figure 在完整流程中的位置

Figure 1 位於 §1.2，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NVMe Family 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

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

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §1.2。
2. 依圖中指定的寬度與位置解碼 NVMe Family；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 1 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §1.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §1.2 如何排列 NVMe Family、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §1.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

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

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, Figure 1, 文件頁 6, PDF 頁 6

</details>

<a id="section-2"></a>

### §2

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 2: Example of Transport Protocol Layers</strong></summary>

<!-- claim:PCIE14-FIG-002-CLAIM figure-table:PCIE14-FIG-002 -->

**SPEC。** Figure 2〈Example of Transport Protocol Layers〉：分開〈Example of Transport Protocol Layers〉中各 protocol layer 的責任。 垂直按 layer、水平按 peer interaction 閱讀，不把 transport rule 歸到 Base layer；來源索引：Transport Protocol Layers。

#### 這張 Figure 在完整流程中的位置

Figure 2 位於 §2，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Transport Protocol Layers 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Transport Protocol Layers]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Transport Protocol Layers` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §2。
2. 依圖中指定的寬度與位置解碼 Transport Protocol Layers；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 2 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §2 如何排列 Transport Protocol Layers、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 2 對應的 raw value 或 buffer，標出包含 Transport Protocol Layers 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Transport Protocol Layers，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Transport Protocol Layers 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Transport Protocol Layers

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, Figure 2, 文件頁 8, PDF 頁 8

</details>

<a id="section-3-1"></a>

### §3.1

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 3: PCI Express Registers</strong></summary>

<!-- claim:PCIE14-FIG-003-CLAIM figure-table:PCIE14-FIG-003 -->

**SPEC。** Figure 3〈PCI Express Registers〉：定義〈PCI Express Registers〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PMCAP, MSICAP, MSIXCAP, MSIX, PXCAP, AERCAP, MSI, MLBAR。

#### 這張 Figure 在完整流程中的位置

Figure 3 位於 §3.1，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 PMCAP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PMCAP]
          ↓
[擷取欄位: MSICAP] → [套用編碼: MSIXCAP]
                                      ↓
[驗證證據: MSIX]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PMCAP` | Power Management Capability，PCI power-management capability 結構的基底位置。 |
| `MSICAP` | MSI Capability，MSI capability 結構的基底位置。 |
| `MSIXCAP` | MSI-X Capability，MSI-X capability 結構的基底位置。 |
| `MSIX` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PXCAP` | PCI Express Capability，PCIe capability 結構的基底位置。 |
| `AERCAP` | Advanced Error Reporting Capability，AER extended capability 結構的基底位置。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1。
2. 依圖中指定的寬度與位置解碼 PMCAP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MSICAP 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 3 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1 如何排列 PMCAP、MSICAP 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 3 對應的 raw value 或 buffer，標出包含 PMCAP 的 bytes 並解碼，再獨立核對 MSICAP。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 PMCAP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 PMCAP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MSICAP 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** PMCAP, MSICAP, MSIXCAP, MSIX, PXCAP, AERCAP, MSI, MLBAR

**來源 keyword 索引：** `shall not`, `shall`, `should`, `may`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, Figure 3, 文件頁 9, PDF 頁 9

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 4: PCI Express Specific Controller Property Definitions</strong></summary>

<!-- claim:PCIE14-FIG-004-CLAIM figure-table:PCIE14-FIG-004 -->

**SPEC。** Figure 4〈PCI Express Specific Controller Property Definitions〉：定義〈PCI Express Specific Controller Property Definitions〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：SQ0TDBL, CAP.DSTRD, CQ0HDBL, SQ1TDBL, CQ1HDBL, SQ2TDBL, CQ2HDBL, Controller。

#### 這張 Figure 在完整流程中的位置

Figure 4 位於 §3.1，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SQ0TDBL 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SQ0TDBL]
          ↓
[擷取欄位: CAP.DSTRD] → [套用編碼: CQ0HDBL]
                                      ↓
[驗證證據: SQ1TDBL]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SQ0TDBL` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CAP.DSTRD` | Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.DSTRD 進一步指定其中的 DSTRD 子欄位。 |
| `CQ0HDBL` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SQ1TDBL` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CQ1HDBL` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SQ2TDBL` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1。
2. 依圖中指定的寬度與位置解碼 SQ0TDBL；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CAP.DSTRD 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 4 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1 如何排列 SQ0TDBL、CAP.DSTRD 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 4 對應的 raw value 或 buffer，標出包含 SQ0TDBL 的 bytes 並解碼，再獨立核對 CAP.DSTRD。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SQ0TDBL，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SQ0TDBL 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CAP.DSTRD 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SQ0TDBL, CAP.DSTRD, CQ0HDBL, SQ1TDBL, CQ1HDBL, SQ2TDBL, CQ2HDBL, Controller

**來源 keyword 索引：** `optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, Figure 4, 文件頁 9-10, PDF 頁 9-10

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 5: Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL - Submission Queue y Tail</strong></summary>

<!-- claim:PCIE14-FIG-005-CLAIM figure-table:PCIE14-FIG-005 -->

**SPEC。** Figure 5〈Offset (1000h + ((2y) * (4 << CAP.DSTRD))): SQyTDBL - Submission Queue y Tail〉：呈現〈Offset (1000h + ((2y) * (4 << CAP.DSTRD))): SQyTDBL - Submission Queue y Tail〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：SQT, CAP.DSTRD, Submission Queue。

#### 這張 Figure 在完整流程中的位置

Figure 5 位於 §3.1.2.1，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SQT 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SQT]
          ↓
[擷取欄位: CAP.DSTRD] → [套用編碼: Submission Queue]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SQT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CAP.DSTRD` | Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.DSTRD 進一步指定其中的 DSTRD 子欄位。 |
| `Submission Queue` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.2.1。
2. 依圖中指定的寬度與位置解碼 SQT；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CAP.DSTRD 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 5 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.2.1 如何排列 SQT、CAP.DSTRD 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.2.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 5 對應的 raw value 或 buffer，標出包含 SQT 的 bytes 並解碼，再獨立核對 CAP.DSTRD。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SQT，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SQT 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CAP.DSTRD 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SQT, CAP.DSTRD, Submission Queue

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1, Figure 5, 文件頁 10, PDF 頁 10

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 6: Offset (1000h + ((2y + 1) * (4 &lt;&lt; CAP.DSTRD))): CQyHDBL - Completion Queue y Head</strong></summary>

<!-- claim:PCIE14-FIG-006-CLAIM figure-table:PCIE14-FIG-006 -->

**SPEC。** Figure 6〈Offset (1000h + ((2y + 1) * (4 << CAP.DSTRD))): CQyHDBL - Completion Queue y Head〉：呈現〈Offset (1000h + ((2y + 1) * (4 << CAP.DSTRD))): CQyHDBL - Completion Queue y Head〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：CQH, CAP.DSTRD, CC.PI, Completion Queue。

#### 這張 Figure 在完整流程中的位置

Figure 6 位於 §3.1.2.1，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CQH 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CQH]
          ↓
[擷取欄位: CAP.DSTRD] → [套用編碼: CC.PI]
                                      ↓
[驗證證據: Completion Queue]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CQH` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CAP.DSTRD` | Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.DSTRD 進一步指定其中的 DSTRD 子欄位。 |
| `CC.PI` | Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.PI 進一步指定其中的 PI 子欄位。 |
| `Completion Queue` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.2.1。
2. 依圖中指定的寬度與位置解碼 CQH；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CAP.DSTRD 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 6 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.1.2.1 如何排列 CQH、CAP.DSTRD 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.2.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 6 對應的 raw value 或 buffer，標出包含 CQH 的 bytes 並解碼，再獨立核對 CAP.DSTRD。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CQH，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CQH 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CAP.DSTRD 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CQH, CAP.DSTRD, CC.PI, Completion Queue

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1, Figure 6, 文件頁 10-11, PDF 頁 10-11

</details>

<a id="section-3-2"></a>

### §3.2

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 7: Create I/O Completion Queue - Command Dword 11</strong></summary>

<!-- claim:PCIE14-FIG-007-CLAIM figure-table:PCIE14-FIG-007 -->

**SPEC。** Figure 7〈Create I/O Completion Queue - Command Dword 11〉：定義 Create I/O Completion Queue 在 CDW11 的 command-specific 欄位。 先定位 CDW11，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：IV, MSI, MSICAP.MC.MME, MSIXCAP.MXC.TS, Completion Queue, Command。

#### 這張 Figure 在完整流程中的位置

Figure 7 位於 §3.2，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 IV 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: IV]
          ↓
[擷取欄位: MSI] → [套用編碼: MSICAP.MC.MME]
                                      ↓
[驗證證據: MSIXCAP.MXC.TS]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `IV` | Interrupt Vector，Completion Queue 指定的 interrupt vector 編號。 |
| `MSI` | Message Signaled Interrupt，透過 memory write message 傳遞 interrupt 的 PCI 機制。 |
| `MSICAP.MC.MME` | MSI Capability，MSI capability 結構的基底位置。 此處的 MSICAP.MC.MME 進一步指定其中的 MC.MME 子欄位。 |
| `MSIXCAP.MXC.TS` | MSI-X Capability，MSI-X capability 結構的基底位置。 此處的 MSIXCAP.MXC.TS 進一步指定其中的 MXC.TS 子欄位。 |
| `Completion Queue` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Command` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.2。
2. 依圖中指定的寬度與位置解碼 IV；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MSI 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 7 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.2 如何排列 IV、MSI 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 7 對應的 raw value 或 buffer，標出包含 IV 的 bytes 並解碼，再獨立核對 MSI。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 IV，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 IV 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MSI 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** IV, MSI, MSICAP.MC.MME, MSIXCAP.MXC.TS, Completion Queue, Command

**來源 keyword 索引：** `shall not`, `shall`, `should`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, Figure 7, 文件頁 11, PDF 頁 11

</details>

<a id="section-3-4"></a>

### §3.4

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 8: Command Processing</strong></summary>

<!-- claim:PCIE14-FIG-008-CLAIM figure-table:PCIE14-FIG-008 -->

**SPEC。** Figure 8〈Command Processing〉：呈現〈Command Processing〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：Command。

#### 這張 Figure 在完整流程中的位置

Figure 8 位於 §3.4.1，在本流程中是「queue」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Command 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 queue／command flow 圖。先標 host 與 controller 的 ownership，再追 head、tail、phase 或 arbitration 的改變；箭頭代表狀態或 ownership 轉移，不自動代表 command 已完成。

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

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.4.1。
2. 依圖中指定的寬度與位置解碼 Command；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 8 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.4.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.4.1 如何排列 Command、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.4.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 8 對應的 raw value 或 buffer，標出包含 Command 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4.1, Figure 8, 文件頁 13, PDF 頁 13

</details>

<a id="section-3-5"></a>

### §3.5

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 9: Pin Based, Single MSI, and Multiple MSI Behavior</strong></summary>

<!-- claim:PCIE14-FIG-009-CLAIM figure-table:PCIE14-FIG-009 -->

**SPEC。** Figure 9〈Pin Based, Single MSI, and Multiple MSI Behavior〉：呈現〈Pin Based, Single MSI, and Multiple MSI Behavior〉中的 interrupt 傳遞或 masking 關係。 分開追蹤 vector／message 來源、mask 狀態與傳遞目的端；來源索引：MSI。

#### 這張 Figure 在完整流程中的位置

Figure 9 位於 §3.5.1，在本流程中是「interrupt」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 MSI 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 interrupt delivery／capability 圖。把 vector source、enable、mask、pending、delivery 與 handler service 分開；interrupt 只通知有工作，CQE 才是 command completion 的資料來源。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MSI]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MSI` | Message Signaled Interrupt，透過 memory write message 傳遞 interrupt 的 PCI 機制。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.5.1。
2. 依圖中指定的寬度與位置解碼 MSI；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 9 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.5.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.5.1 如何排列 MSI、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.5.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 9 對應的 raw value 或 buffer，標出包含 MSI 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 MSI，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 MSI 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** MSI

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5.1, Figure 9, 文件頁 15, PDF 頁 15

</details>

<a id="section-3-8"></a>

### §3.8

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 10: PCI Express Type 0/1 Common Configuration Space</strong></summary>

<!-- claim:PCIE14-FIG-010-CLAIM figure-table:PCIE14-FIG-010 -->

**SPEC。** Figure 10〈PCI Express Type 0/1 Common Configuration Space〉：定義〈PCI Express Type 0/1 Common Configuration Space〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PCI Express Type 0/1 Common Configuration Space。

#### 這張 Figure 在完整流程中的位置

Figure 10 位於 §3.8，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 PCI Express Type 0/1 Common Configuration Space 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PCI Express Type 0/1 Common Configuration Space]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PCI Express Type 0/1 Common Configuration Space` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8。
2. 依圖中指定的寬度與位置解碼 PCI Express Type 0/1 Common Configuration Space；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 10 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8 如何排列 PCI Express Type 0/1 Common Configuration Space、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 10 對應的 raw value 或 buffer，標出包含 PCI Express Type 0/1 Common Configuration Space 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 PCI Express Type 0/1 Common Configuration Space，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 PCI Express Type 0/1 Common Configuration Space 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** PCI Express Type 0/1 Common Configuration Space

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8, Figure 10, 文件頁 16-17, PDF 頁 16-17

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 11: Offset 00h: ID - Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-011-CLAIM figure-table:PCIE14-FIG-011 -->

**SPEC。** Figure 11〈Offset 00h: ID - Identifiers〉：定義 offset 00h 的 ID（Identifiers），並指出軟體在該位置必須分別解碼的欄位。 先定位 ID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ID, DID, VID。

#### 這張 Figure 在完整流程中的位置

Figure 11 位於 §3.8.1.1，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ID]
          ↓
[擷取欄位: DID] → [套用編碼: VID]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `DID` | Domain Identifier，辨識 NVM subsystem 內 domain 的 identifier。 |
| `VID` | Vendor ID，由 PCI-SIG 配置、辨識 vendor 的 identifier。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.1。
2. 依圖中指定的寬度與位置解碼 ID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 DID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 11 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.1 如何排列 ID、DID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 11 對應的 raw value 或 buffer，標出包含 ID 的 bytes 並解碼，再獨立核對 DID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 DID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ID, DID, VID

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.1, Figure 11, 文件頁 17, PDF 頁 17

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 12: Offset 04h: CMD - Command</strong></summary>

<!-- claim:PCIE14-FIG-012-CLAIM figure-table:PCIE14-FIG-012 -->

**SPEC。** Figure 12〈Offset 04h: CMD - Command〉：定義 offset 04h 的 CMD（Command），並指出軟體在該位置必須分別解碼的欄位。 先定位 CMD，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CMD, SIG, ID, FBE, SERR, SEE, IDSEL, ISWCC。

#### 這張 Figure 在完整流程中的位置

Figure 12 位於 §3.8.1.2，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CMD 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CMD]
          ↓
[擷取欄位: SIG] → [套用編碼: ID]
                                      ↓
[驗證證據: FBE]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CMD` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SIG` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FBE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SERR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SEE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.2。
2. 依圖中指定的寬度與位置解碼 CMD；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 SIG 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 12 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.2 如何排列 CMD、SIG 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 12 對應的 raw value 或 buffer，標出包含 CMD 的 bytes 並解碼，再獨立核對 SIG。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CMD，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CMD 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 SIG 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CMD, SIG, ID, FBE, SERR, SEE, IDSEL, ISWCC

**來源 keyword 索引：** `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.2, Figure 12, 文件頁 17, PDF 頁 17

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 13: Offset 06h: STS - Device Status</strong></summary>

<!-- claim:PCIE14-FIG-013-CLAIM figure-table:PCIE14-FIG-013 -->

**SPEC。** Figure 13〈Offset 06h: STS - Device Status〉：定義 offset 06h 的 STS（Device Status），並指出軟體在該位置必須分別解碼的欄位。 先定位 STS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：STS, DPE, SSE, RMA, RTA, STA, DEVSEL, DEVT。

#### 這張 Figure 在完整流程中的位置

Figure 13 位於 §3.8.1.3，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 STS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: STS]
          ↓
[擷取欄位: DPE] → [套用編碼: SSE]
                                      ↓
[驗證證據: RMA]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `STS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `DPE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SSE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `RMA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `RTA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `STA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.3。
2. 依圖中指定的寬度與位置解碼 STS；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 DPE 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 13 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.3 如何排列 STS、DPE 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 13 對應的 raw value 或 buffer，標出包含 STS 的 bytes 並解碼，再獨立核對 DPE。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 STS，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 STS 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 DPE 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** STS, DPE, SSE, RMA, RTA, STA, DEVSEL, DEVT

**來源 keyword 索引：** `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.3, Figure 13, 文件頁 18, PDF 頁 18

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 14: Offset 08h: RID - Revision ID</strong></summary>

<!-- claim:PCIE14-FIG-014-CLAIM figure-table:PCIE14-FIG-014 -->

**SPEC。** Figure 14〈Offset 08h: RID - Revision ID〉：定義 offset 08h 的 RID（Revision ID），並指出軟體在該位置必須分別解碼的欄位。 先定位 RID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：RID, ID。

#### 這張 Figure 在完整流程中的位置

Figure 14 位於 §3.8.1.4，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 RID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: RID]
          ↓
[擷取欄位: ID] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `RID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.4。
2. 依圖中指定的寬度與位置解碼 RID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 ID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 14 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.4 如何排列 RID、ID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 14 對應的 raw value 或 buffer，標出包含 RID 的 bytes 並解碼，再獨立核對 ID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 RID，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 RID 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 ID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** RID, ID

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.4, Figure 14, 文件頁 18, PDF 頁 18

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 15: Offset 09h: CC - Class Code</strong></summary>

<!-- claim:PCIE14-FIG-015-CLAIM figure-table:PCIE14-FIG-015 -->

**SPEC。** Figure 15〈Offset 09h: CC - Class Code〉：定義 offset 09h 的 CC（Class Code），並指出軟體在該位置必須分別解碼的欄位。 先定位 CC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CC, BCC, SCC, PI。

#### 這張 Figure 在完整流程中的位置

Figure 15 位於 §3.8.1.5，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CC 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CC]
          ↓
[擷取欄位: BCC] → [套用編碼: SCC]
                                      ↓
[驗證證據: PI]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CC` | Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 |
| `BCC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SCC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PI` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.5。
2. 依圖中指定的寬度與位置解碼 CC；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 BCC 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 15 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.5 如何排列 CC、BCC 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.5 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 15 對應的 raw value 或 buffer，標出包含 CC 的 bytes 並解碼，再獨立核對 BCC。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CC，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CC 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 BCC 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CC, BCC, SCC, PI

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.5, Figure 15, 文件頁 18, PDF 頁 18

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 16: Offset 0Ch: CLS - Cache Line Size</strong></summary>

<!-- claim:PCIE14-FIG-016-CLAIM figure-table:PCIE14-FIG-016 -->

**SPEC。** Figure 16〈Offset 0Ch: CLS - Cache Line Size〉：定義 offset 0Ch 的 CLS（Cache Line Size），並指出軟體在該位置必須分別解碼的欄位。 先定位 CLS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CLS。

#### 這張 Figure 在完整流程中的位置

Figure 16 位於 §3.8.1.6，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CLS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CLS]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CLS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.6。
2. 依圖中指定的寬度與位置解碼 CLS；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 16 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.6 如何排列 CLS、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.6 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 16 對應的 raw value 或 buffer，標出包含 CLS 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CLS，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CLS 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CLS

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.6, Figure 16, 文件頁 18, PDF 頁 18

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 17: Offset 0Dh: MLT - Master Latency Timer</strong></summary>

<!-- claim:PCIE14-FIG-017-CLAIM figure-table:PCIE14-FIG-017 -->

**SPEC。** Figure 17〈Offset 0Dh: MLT - Master Latency Timer〉：定義 offset 0Dh 的 MLT（Master Latency Timer），並指出軟體在該位置必須分別解碼的欄位。 先定位 MLT，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：MLT。

#### 這張 Figure 在完整流程中的位置

Figure 17 位於 §3.8.1.7，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 MLT 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MLT]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MLT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.7。
2. 依圖中指定的寬度與位置解碼 MLT；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 17 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.7 如何排列 MLT、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.7 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 17 對應的 raw value 或 buffer，標出包含 MLT 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 MLT，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 MLT 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** MLT

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.7, Figure 17, 文件頁 18, PDF 頁 18

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 18: Offset 0Eh: HTYPE - Header Type</strong></summary>

<!-- claim:PCIE14-FIG-018-CLAIM figure-table:PCIE14-FIG-018 -->

**SPEC。** Figure 18〈Offset 0Eh: HTYPE - Header Type〉：定義 offset 0Eh 的 HTYPE（Header Type），並指出軟體在該位置必須分別解碼的欄位。 先定位 HTYPE，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：HTYPE, MFD, HL。

#### 這張 Figure 在完整流程中的位置

Figure 18 位於 §3.8.1.8，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 HTYPE 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: HTYPE]
          ↓
[擷取欄位: MFD] → [套用編碼: HL]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `HTYPE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MFD` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `HL` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.8。
2. 依圖中指定的寬度與位置解碼 HTYPE；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MFD 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 18 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.8 如何排列 HTYPE、MFD 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.8 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 18 對應的 raw value 或 buffer，標出包含 HTYPE 的 bytes 並解碼，再獨立核對 MFD。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 HTYPE，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 HTYPE 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MFD 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** HTYPE, MFD, HL

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.8, Figure 18, 文件頁 19, PDF 頁 19

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 19: Offset 0Fh: BIST - Built-In Self Test (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-019-CLAIM figure-table:PCIE14-FIG-019 -->

**SPEC。** Figure 19〈Offset 0Fh: BIST - Built-In Self Test (Optional)〉：定義 offset 0Fh 的 BIST（Built-In Self Test (Optional)），並指出軟體在該位置必須分別解碼的欄位。 先定位 BIST，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：BIST, BC, SB, SIG, CC。

#### 這張 Figure 在完整流程中的位置

Figure 19 位於 §3.8.1.9，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 BIST 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: BIST]
          ↓
[擷取欄位: BC] → [套用編碼: SB]
                                      ↓
[驗證證據: SIG]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `BIST` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `BC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SB` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SIG` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CC` | Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.9。
2. 依圖中指定的寬度與位置解碼 BIST；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 BC 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 19 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.9 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.9 如何排列 BIST、BC 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.9 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 19 對應的 raw value 或 buffer，標出包含 BIST 的 bytes 並解碼，再獨立核對 BC。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 BIST，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 BIST 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 BC 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** BIST, BC, SB, SIG, CC

**來源 keyword 索引：** `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.9, Figure 19, 文件頁 19, PDF 頁 19

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 20: Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits</strong></summary>

<!-- claim:PCIE14-FIG-020-CLAIM figure-table:PCIE14-FIG-020 -->

**SPEC。** Figure 20〈Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits〉：定義〈Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：BA, PF, TP, RTE, MLBAR, BAR0, SIG。

#### 這張 Figure 在完整流程中的位置

Figure 20 位於 §3.8.1.10，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 BA 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: BA]
          ↓
[擷取欄位: PF] → [套用編碼: TP]
                                      ↓
[驗證證據: RTE]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `BA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PF` | Physical Function，具有完整 PCIe 設定能力、可管理相關 VF 的實體功能。 |
| `TP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `RTE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MLBAR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `BAR0` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.10。
2. 依圖中指定的寬度與位置解碼 BA；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 PF 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 20 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.10 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.10 如何排列 BA、PF 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.10 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 20 對應的 raw value 或 buffer，標出包含 BA 的 bytes 並解碼，再獨立核對 PF。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 BA，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 BA 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 PF 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** BA, PF, TP, RTE, MLBAR, BAR0, SIG

**來源 keyword 索引：** `may`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.10, Figure 20, 文件頁 19, PDF 頁 19

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 21: Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits</strong></summary>

<!-- claim:PCIE14-FIG-021-CLAIM figure-table:PCIE14-FIG-021 -->

**SPEC。** Figure 21〈Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits〉：定義〈Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：BA, MUBAR, BAR1。

#### 這張 Figure 在完整流程中的位置

Figure 21 位於 §3.8.1.11，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 BA 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: BA]
          ↓
[擷取欄位: MUBAR] → [套用編碼: BAR1]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `BA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MUBAR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `BAR1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.11。
2. 依圖中指定的寬度與位置解碼 BA；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MUBAR 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 21 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.11 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.11 如何排列 BA、MUBAR 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.11 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 21 對應的 raw value 或 buffer，標出包含 BA 的 bytes 並解碼，再獨立核對 MUBAR。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 BA，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 BA 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MUBAR 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** BA, MUBAR, BAR1

**來源 keyword 索引：** `may`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.11, Figure 21, 文件頁 19, PDF 頁 19

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 22: Offset 18h: BAR2 - Index/Data Pair Register Base Address or Vendor Specific</strong></summary>

<!-- claim:PCIE14-FIG-022-CLAIM figure-table:PCIE14-FIG-022 -->

**SPEC。** Figure 22〈Offset 18h: BAR2 - Index/Data Pair Register Base Address or Vendor Specific〉：定義 offset 18h 的 BAR2（Index/Data Pair Register Base Address or Vendor Specific），並指出軟體在該位置必須分別解碼的欄位。 先定位 BAR2，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：BA, RTE, BAR2。

#### 這張 Figure 在完整流程中的位置

Figure 22 位於 §3.8.1.12，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 BA 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: BA]
          ↓
[擷取欄位: RTE] → [套用編碼: BAR2]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `BA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `RTE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `BAR2` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.12。
2. 依圖中指定的寬度與位置解碼 BA；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 RTE 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 22 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.12 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.12 如何排列 BA、RTE 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.12 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 22 對應的 raw value 或 buffer，標出包含 BA 的 bytes 並解碼，再獨立核對 RTE。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 BA，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 BA 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 RTE 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** BA, RTE, BAR2

**來源 keyword 索引：** `may`, `optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.12, Figure 22, 文件頁 20, PDF 頁 20

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 23: Offset 28h: CCPTR - CardBus CIS Pointer</strong></summary>

<!-- claim:PCIE14-FIG-023-CLAIM figure-table:PCIE14-FIG-023 -->

**SPEC。** Figure 23〈Offset 28h: CCPTR - CardBus CIS Pointer〉：定義 offset 28h 的 CCPTR（CardBus CIS Pointer），並指出軟體在該位置必須分別解碼的欄位。 先定位 CCPTR，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CCPTR, CIS。

#### 這張 Figure 在完整流程中的位置

Figure 23 位於 §3.8.1.16，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CCPTR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CCPTR]
          ↓
[擷取欄位: CIS] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CCPTR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CIS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.16。
2. 依圖中指定的寬度與位置解碼 CCPTR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CIS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 23 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.16 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.16 如何排列 CCPTR、CIS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.16 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 23 對應的 raw value 或 buffer，標出包含 CCPTR 的 bytes 並解碼，再獨立核對 CIS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CCPTR，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CCPTR 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CIS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CCPTR, CIS

**來源 keyword 索引：** `shall`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.16, Figure 23, 文件頁 20, PDF 頁 20

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 24: Offset 2Ch: SS - Subsystem Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-024-CLAIM figure-table:PCIE14-FIG-024 -->

**SPEC。** Figure 24〈Offset 2Ch: SS - Subsystem Identifiers〉：定義 offset 2Ch 的 SS（Subsystem Identifiers），並指出軟體在該位置必須分別解碼的欄位。 先定位 SS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：SSID, SSVID, SS, ID。

#### 這張 Figure 在完整流程中的位置

Figure 24 位於 §3.8.1.17，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SSID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SSID]
          ↓
[擷取欄位: SSVID] → [套用編碼: SS]
                                      ↓
[驗證證據: ID]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SSID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SSVID` | Subsystem Vendor ID，辨識 subsystem vendor 的 PCI identifier。 |
| `SS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.17。
2. 依圖中指定的寬度與位置解碼 SSID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 SSVID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 24 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.17 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.17 如何排列 SSID、SSVID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.17 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 24 對應的 raw value 或 buffer，標出包含 SSID 的 bytes 並解碼，再獨立核對 SSVID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SSID，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SSID 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 SSVID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SSID, SSVID, SS, ID

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.17, Figure 24, 文件頁 20, PDF 頁 20

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 25: Offset 30h: EROM - Expansion ROM (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-025-CLAIM figure-table:PCIE14-FIG-025 -->

**SPEC。** Figure 25〈Offset 30h: EROM - Expansion ROM (Optional)〉：定義 offset 30h 的 EROM（Expansion ROM (Optional)），並指出軟體在該位置必須分別解碼的欄位。 先定位 EROM，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：RBA, EROM, ROM。

#### 這張 Figure 在完整流程中的位置

Figure 25 位於 §3.8.1.18，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 RBA 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: RBA]
          ↓
[擷取欄位: EROM] → [套用編碼: ROM]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `RBA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `EROM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ROM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.18。
2. 依圖中指定的寬度與位置解碼 RBA；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 EROM 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 25 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.18 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.18 如何排列 RBA、EROM 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.18 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 25 對應的 raw value 或 buffer，標出包含 RBA 的 bytes 並解碼，再獨立核對 EROM。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 RBA，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 RBA 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 EROM 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** RBA, EROM, ROM

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.18, Figure 25, 文件頁 20, PDF 頁 20

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 26: Offset 34h: CAP - Capabilities Pointer</strong></summary>

<!-- claim:PCIE14-FIG-026-CLAIM figure-table:PCIE14-FIG-026 -->

**SPEC。** Figure 26〈Offset 34h: CAP - Capabilities Pointer〉：定義 offset 34h 的 CAP（Capabilities Pointer），並指出軟體在該位置必須分別解碼的欄位。 先定位 CAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CP, CAP。

#### 這張 Figure 在完整流程中的位置

Figure 26 位於 §3.8.1.19，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CP]
          ↓
[擷取欄位: CAP] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CAP` | Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.19。
2. 依圖中指定的寬度與位置解碼 CP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CAP 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 26 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.19 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.19 如何排列 CP、CAP 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.19 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 26 對應的 raw value 或 buffer，標出包含 CP 的 bytes 並解碼，再獨立核對 CAP。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CAP 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CP, CAP

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.19, Figure 26, 文件頁 21, PDF 頁 21

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 27: Offset 3Ch: INTR - Interrupt Information</strong></summary>

<!-- claim:PCIE14-FIG-027-CLAIM figure-table:PCIE14-FIG-027 -->

**SPEC。** Figure 27〈Offset 3Ch: INTR - Interrupt Information〉：定義 offset 3Ch 的 INTR（Interrupt Information），並指出軟體在該位置必須分別解碼的欄位。 先定位 INTR，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：IPIN, ILINE, INTR, Interrupt。

#### 這張 Figure 在完整流程中的位置

Figure 27 位於 §3.8.1.20，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 IPIN 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: IPIN]
          ↓
[擷取欄位: ILINE] → [套用編碼: INTR]
                                      ↓
[驗證證據: Interrupt]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `IPIN` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ILINE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `INTR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Interrupt` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.20。
2. 依圖中指定的寬度與位置解碼 IPIN；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 ILINE 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 27 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.20 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.20 如何排列 IPIN、ILINE 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.20 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 27 對應的 raw value 或 buffer，標出包含 IPIN 的 bytes 並解碼，再獨立核對 ILINE。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 IPIN，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 IPIN 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 ILINE 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** IPIN, ILINE, INTR, Interrupt

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.20, Figure 27, 文件頁 21, PDF 頁 21

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 28: Offset 3Eh: MGNT - Minimum Grant</strong></summary>

<!-- claim:PCIE14-FIG-028-CLAIM figure-table:PCIE14-FIG-028 -->

**SPEC。** Figure 28〈Offset 3Eh: MGNT - Minimum Grant〉：定義 offset 3Eh 的 MGNT（Minimum Grant），並指出軟體在該位置必須分別解碼的欄位。 先定位 MGNT，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：GNT, MGNT。

#### 這張 Figure 在完整流程中的位置

Figure 28 位於 §3.8.1.21，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 GNT 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: GNT]
          ↓
[擷取欄位: MGNT] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `GNT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MGNT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.21。
2. 依圖中指定的寬度與位置解碼 GNT；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MGNT 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 28 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.21 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.21 如何排列 GNT、MGNT 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.21 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 28 對應的 raw value 或 buffer，標出包含 GNT 的 bytes 並解碼，再獨立核對 MGNT。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 GNT，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 GNT 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MGNT 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** GNT, MGNT

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.21, Figure 28, 文件頁 21, PDF 頁 21

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 29: Offset 3Fh: MLAT - Maximum Latency</strong></summary>

<!-- claim:PCIE14-FIG-029-CLAIM figure-table:PCIE14-FIG-029 -->

**SPEC。** Figure 29〈Offset 3Fh: MLAT - Maximum Latency〉：定義 offset 3Fh 的 MLAT（Maximum Latency），並指出軟體在該位置必須分別解碼的欄位。 先定位 MLAT，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：LAT, MLAT, CC。

#### 這張 Figure 在完整流程中的位置

Figure 29 位於 §3.8.1.22，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 LAT 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LAT]
          ↓
[擷取欄位: MLAT] → [套用編碼: CC]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LAT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MLAT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CC` | Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.22。
2. 依圖中指定的寬度與位置解碼 LAT；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MLAT 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 29 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.22 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.22 如何排列 LAT、MLAT 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.22 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 29 對應的 raw value 或 buffer，標出包含 LAT 的 bytes 並解碼，再獨立核對 MLAT。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 LAT，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 LAT 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MLAT 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** LAT, MLAT, CC

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.22, Figure 29, 文件頁 21, PDF 頁 21

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 30: PCI Power Management Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-030-CLAIM figure-table:PCIE14-FIG-030 -->

**SPEC。** Figure 30〈PCI Power Management Capabilities〉：定義〈PCI Power Management Capabilities〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PMCAP, PID, ID, PC, PMCS。

#### 這張 Figure 在完整流程中的位置

Figure 30 位於 §3.8.1.22，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 PMCAP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PMCAP]
          ↓
[擷取欄位: PID] → [套用編碼: ID]
                                      ↓
[驗證證據: PC]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PMCAP` | Power Management Capability，PCI power-management capability 結構的基底位置。 |
| `PID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMCS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.1.22。
2. 依圖中指定的寬度與位置解碼 PMCAP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 PID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 30 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.1.22 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.1.22 如何排列 PMCAP、PID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.1.22 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 30 對應的 raw value 或 buffer，標出包含 PMCAP 的 bytes 並解碼，再獨立核對 PID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 PMCAP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 PMCAP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 PID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** PMCAP, PID, ID, PC, PMCS

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.22, Figure 30, 文件頁 21, PDF 頁 21

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 31: Offset PMCAP: PID - PCI Power Management Capability ID</strong></summary>

<!-- claim:PCIE14-FIG-031-CLAIM figure-table:PCIE14-FIG-031 -->

**SPEC。** Figure 31〈Offset PMCAP: PID - PCI Power Management Capability ID〉：定義 offset PMCAP 的 PID（PCI Power Management Capability ID），並指出軟體在該位置必須分別解碼的欄位。 先定位 PID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NEXT, CID, PMCAP, PID, ID。

#### 這張 Figure 在完整流程中的位置

Figure 31 位於 §3.8.2.1，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NEXT 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NEXT]
          ↓
[擷取欄位: CID] → [套用編碼: PMCAP]
                                      ↓
[驗證證據: PID]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NEXT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CID` | Command Identifier，與 SQ identifier 合用以辨識 outstanding command。 |
| `PMCAP` | Power Management Capability，PCI power-management capability 結構的基底位置。 |
| `PID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.2.1。
2. 依圖中指定的寬度與位置解碼 NEXT；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 31 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.2.1 如何排列 NEXT、CID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.2.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 31 對應的 raw value 或 buffer，標出包含 NEXT 的 bytes 並解碼，再獨立核對 CID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NEXT，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NEXT 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NEXT, CID, PMCAP, PID, ID

**來源 keyword 索引：** `may`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.1, Figure 31, 文件頁 21, PDF 頁 21

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 32: Offset PMCAP + 2h: PC - PCI Power Management Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-032-CLAIM figure-table:PCIE14-FIG-032 -->

**SPEC。** Figure 32〈Offset PMCAP + 2h: PC - PCI Power Management Capabilities〉：定義 offset PMCAP + 2h 的 PC（PCI Power Management Capabilities），並指出軟體在該位置必須分別解碼的欄位。 先定位 PC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PSUP, D2S, D1S, AUXC, DSI, PMEC, VS, PMCAP。

#### 這張 Figure 在完整流程中的位置

Figure 32 位於 §3.8.2.2，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 PSUP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PSUP]
          ↓
[擷取欄位: D2S] → [套用編碼: D1S]
                                      ↓
[驗證證據: AUXC]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PSUP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `D2S` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `D1S` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AUXC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `DSI` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMEC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.2.2。
2. 依圖中指定的寬度與位置解碼 PSUP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 D2S 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 32 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.2.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.2.2 如何排列 PSUP、D2S 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.2.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 32 對應的 raw value 或 buffer，標出包含 PSUP 的 bytes 並解碼，再獨立核對 D2S。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 PSUP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 PSUP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 D2S 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** PSUP, D2S, D1S, AUXC, DSI, PMEC, VS, PMCAP

**來源 keyword 索引：** `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.2, Figure 32, 文件頁 22, PDF 頁 22

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 33: Offset PMCAP + 4h: PMCS - PCI Power Management Control and Status</strong></summary>

<!-- claim:PCIE14-FIG-033-CLAIM figure-table:PCIE14-FIG-033 -->

**SPEC。** Figure 33〈Offset PMCAP + 4h: PMCS - PCI Power Management Control and Status〉：定義 offset PMCAP + 4h 的 PMCS（PCI Power Management Control and Status），並指出軟體在該位置必須分別解碼的欄位。 先定位 PMCS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PMES, DSC, DSE, PMEE, NSFRST, PS, PMCAP, PMCS。

#### 這張 Figure 在完整流程中的位置

Figure 33 位於 §3.8.2.3，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 PMES 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PMES]
          ↓
[擷取欄位: DSC] → [套用編碼: DSE]
                                      ↓
[驗證證據: PMEE]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PMES` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `DSC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `DSE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMEE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NSFRST` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PS` | Power State，controller 的功耗／效能 operating point；PS0 是最高 maximum-power state。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.2.3。
2. 依圖中指定的寬度與位置解碼 PMES；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 DSC 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 33 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.2.3 如何排列 PMES、DSC 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.2.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 33 對應的 raw value 或 buffer，標出包含 PMES 的 bytes 並解碼，再獨立核對 DSC。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 PMES，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 PMES 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 DSC 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** PMES, DSC, DSE, PMEE, NSFRST, PS, PMCAP, PMCS

**來源 keyword 索引：** `optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.3, Figure 33, 文件頁 22, PDF 頁 22

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 34: Message Signaled Interrupt Capability (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-034-CLAIM figure-table:PCIE14-FIG-034 -->

**SPEC。** Figure 34〈Message Signaled Interrupt Capability (Optional)〉：定義〈Message Signaled Interrupt Capability (Optional)〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MSICAP, MID, ID, MC, MA, MUA, MD, MMASK。

#### 這張 Figure 在完整流程中的位置

Figure 34 位於 §3.8.2.3，在本流程中是「interrupt」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 MSICAP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 interrupt delivery／capability 圖。把 vector source、enable、mask、pending、delivery 與 handler service 分開；interrupt 只通知有工作，CQE 才是 command completion 的資料來源。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MSICAP]
          ↓
[擷取欄位: MID] → [套用編碼: ID]
                                      ↓
[驗證證據: MC]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MSICAP` | MSI Capability，MSI capability 結構的基底位置。 |
| `MID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MUA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.2.3。
2. 依圖中指定的寬度與位置解碼 MSICAP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 34 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.2.3 如何排列 MSICAP、MID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.2.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 34 對應的 raw value 或 buffer，標出包含 MSICAP 的 bytes 並解碼，再獨立核對 MID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 MSICAP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 MSICAP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** MSICAP, MID, ID, MC, MA, MUA, MD, MMASK

**來源 keyword 索引：** `optional`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.3, Figure 34, 文件頁 22, PDF 頁 22

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 35: Offset MSICAP: MID - Message Signaled Interrupt Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-035-CLAIM figure-table:PCIE14-FIG-035 -->

**SPEC。** Figure 35〈Offset MSICAP: MID - Message Signaled Interrupt Identifiers〉：定義 offset MSICAP 的 MID（Message Signaled Interrupt Identifiers），並指出軟體在該位置必須分別解碼的欄位。 先定位 MID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NEXT, CID, MSICAP, MID, ID, MSI, Interrupt。

#### 這張 Figure 在完整流程中的位置

Figure 35 位於 §3.8.3.1，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NEXT 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NEXT]
          ↓
[擷取欄位: CID] → [套用編碼: MSICAP]
                                      ↓
[驗證證據: MID]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NEXT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CID` | Command Identifier，與 SQ identifier 合用以辨識 outstanding command。 |
| `MSICAP` | MSI Capability，MSI capability 結構的基底位置。 |
| `MID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSI` | Message Signaled Interrupt，透過 memory write message 傳遞 interrupt 的 PCI 機制。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.3.1。
2. 依圖中指定的寬度與位置解碼 NEXT；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 35 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.3.1 如何排列 NEXT、CID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.3.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 35 對應的 raw value 或 buffer，標出包含 NEXT 的 bytes 並解碼，再獨立核對 CID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NEXT，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NEXT 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NEXT, CID, MSICAP, MID, ID, MSI, Interrupt

**來源 keyword 索引：** `may`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.1, Figure 35, 文件頁 23, PDF 頁 23

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 36: Offset MSICAP + 2h: MC - Message Signaled Interrupt Message Control</strong></summary>

<!-- claim:PCIE14-FIG-036-CLAIM figure-table:PCIE14-FIG-036 -->

**SPEC。** Figure 36〈Offset MSICAP + 2h: MC - Message Signaled Interrupt Message Control〉：定義 offset MSICAP + 2h 的 MC（Message Signaled Interrupt Message Control），並指出軟體在該位置必須分別解碼的欄位。 先定位 MC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PVM, C64, MME, MMC, MSIE, MSICAP, MC, MSI。

#### 這張 Figure 在完整流程中的位置

Figure 36 位於 §3.8.3.2，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 PVM 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PVM]
          ↓
[擷取欄位: C64] → [套用編碼: MME]
                                      ↓
[驗證證據: MMC]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PVM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `C64` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MME` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MMC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSIE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSICAP` | MSI Capability，MSI capability 結構的基底位置。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.3.2。
2. 依圖中指定的寬度與位置解碼 PVM；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 C64 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 36 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.3.2 如何排列 PVM、C64 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.3.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 36 對應的 raw value 或 buffer，標出包含 PVM 的 bytes 並解碼，再獨立核對 C64。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 PVM，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 PVM 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 C64 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** PVM, C64, MME, MMC, MSIE, MSICAP, MC, MSI

**來源 keyword 索引：** `shall`, `should`, `may`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.2, Figure 36, 文件頁 23, PDF 頁 23

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 37: Offset MSICAP + 4h: MA - Message Signaled Interrupt Message Address</strong></summary>

<!-- claim:PCIE14-FIG-037-CLAIM figure-table:PCIE14-FIG-037 -->

**SPEC。** Figure 37〈Offset MSICAP + 4h: MA - Message Signaled Interrupt Message Address〉：定義 offset MSICAP + 4h 的 MA（Message Signaled Interrupt Message Address），並指出軟體在該位置必須分別解碼的欄位。 先定位 MA，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：ADDR, MSICAP, MA, SIG, Interrupt。

#### 這張 Figure 在完整流程中的位置

Figure 37 位於 §3.8.3.3，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ADDR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ADDR]
          ↓
[擷取欄位: MSICAP] → [套用編碼: MA]
                                      ↓
[驗證證據: SIG]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ADDR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSICAP` | MSI Capability，MSI capability 結構的基底位置。 |
| `MA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SIG` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Interrupt` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.3.3。
2. 依圖中指定的寬度與位置解碼 ADDR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MSICAP 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 37 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.3.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.3.3 如何排列 ADDR、MSICAP 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.3.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 37 對應的 raw value 或 buffer，標出包含 ADDR 的 bytes 並解碼，再獨立核對 MSICAP。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 MSICAP 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ADDR, MSICAP, MA, SIG, Interrupt

**來源 keyword 索引：** `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.3, Figure 37, 文件頁 23, PDF 頁 23

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 38: Offset MSICAP + 8h: MUA - Message Signaled Interrupt Upper Address</strong></summary>

<!-- claim:PCIE14-FIG-038-CLAIM figure-table:PCIE14-FIG-038 -->

**SPEC。** Figure 38〈Offset MSICAP + 8h: MUA - Message Signaled Interrupt Upper Address〉：定義 offset MSICAP + 8h 的 MUA（Message Signaled Interrupt Upper Address），並指出軟體在該位置必須分別解碼的欄位。 先定位 MUA，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：UADDR, MSICAP, MUA, MSI, Interrupt。

#### 這張 Figure 在完整流程中的位置

Figure 38 位於 §3.8.3.4，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 UADDR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: UADDR]
          ↓
[擷取欄位: MSICAP] → [套用編碼: MUA]
                                      ↓
[驗證證據: MSI]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `UADDR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSICAP` | MSI Capability，MSI capability 結構的基底位置。 |
| `MUA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSI` | Message Signaled Interrupt，透過 memory write message 傳遞 interrupt 的 PCI 機制。 |
| `Interrupt` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.3.4。
2. 依圖中指定的寬度與位置解碼 UADDR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MSICAP 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 38 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.3.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.3.4 如何排列 UADDR、MSICAP 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.3.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 38 對應的 raw value 或 buffer，標出包含 UADDR 的 bytes 並解碼，再獨立核對 MSICAP。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 UADDR，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 UADDR 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MSICAP 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** UADDR, MSICAP, MUA, MSI, Interrupt

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.4, Figure 38, 文件頁 23, PDF 頁 23

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 39: Offset MSICAP + Ch: MD - Message Signaled Interrupt Message Data</strong></summary>

<!-- claim:PCIE14-FIG-039-CLAIM figure-table:PCIE14-FIG-039 -->

**SPEC。** Figure 39〈Offset MSICAP + Ch: MD - Message Signaled Interrupt Message Data〉：定義 offset MSICAP + Ch 的 MD（Message Signaled Interrupt Message Data），並指出軟體在該位置必須分別解碼的欄位。 先定位 MD，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：DATA, MSICAP, MD, MSI, AD, Interrupt。

#### 這張 Figure 在完整流程中的位置

Figure 39 位於 §3.8.3.5，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DATA 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DATA]
          ↓
[擷取欄位: MSICAP] → [套用編碼: MD]
                                      ↓
[驗證證據: MSI]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DATA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSICAP` | MSI Capability，MSI capability 結構的基底位置。 |
| `MD` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSI` | Message Signaled Interrupt，透過 memory write message 傳遞 interrupt 的 PCI 機制。 |
| `AD` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Interrupt` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.3.5。
2. 依圖中指定的寬度與位置解碼 DATA；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MSICAP 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 39 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.3.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.3.5 如何排列 DATA、MSICAP 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.3.5 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 39 對應的 raw value 或 buffer，標出包含 DATA 的 bytes 並解碼，再獨立核對 MSICAP。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 DATA，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 DATA 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MSICAP 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** DATA, MSICAP, MD, MSI, AD, Interrupt

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.5, Figure 39, 文件頁 23, PDF 頁 23

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 40: Offset MSICAP + 10h: MMASK - Message Signaled Interrupt Mask Bits (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-040-CLAIM figure-table:PCIE14-FIG-040 -->

**SPEC。** Figure 40〈Offset MSICAP + 10h: MMASK - Message Signaled Interrupt Mask Bits (Optional)〉：定義 offset MSICAP + 10h 的 MMASK（Message Signaled Interrupt Mask Bits (Optional)），並指出軟體在該位置必須分別解碼的欄位。 先定位 MMASK，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：MASK, MSICAP, MMASK, Interrupt。

#### 這張 Figure 在完整流程中的位置

Figure 40 位於 §3.8.3.6，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 MASK 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MASK]
          ↓
[擷取欄位: MSICAP] → [套用編碼: MMASK]
                                      ↓
[驗證證據: Interrupt]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MASK` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSICAP` | MSI Capability，MSI capability 結構的基底位置。 |
| `MMASK` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Interrupt` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.3.6。
2. 依圖中指定的寬度與位置解碼 MASK；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MSICAP 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 40 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.3.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.3.6 如何排列 MASK、MSICAP 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.3.6 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 40 對應的 raw value 或 buffer，標出包含 MASK 的 bytes 並解碼，再獨立核對 MSICAP。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 MASK，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 MASK 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MSICAP 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** MASK, MSICAP, MMASK, Interrupt

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.6, Figure 40, 文件頁 24, PDF 頁 24

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 41: Offset MSICAP + 14h: MPEND - Message Signaled Interrupt Pending Bits (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-041-CLAIM figure-table:PCIE14-FIG-041 -->

**SPEC。** Figure 41〈Offset MSICAP + 14h: MPEND - Message Signaled Interrupt Pending Bits (Optional)〉：定義 offset MSICAP + 14h 的 MPEND（Message Signaled Interrupt Pending Bits (Optional)），並指出軟體在該位置必須分別解碼的欄位。 先定位 MPEND，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PEND, MSICAP, MPEND, MSIX, Interrupt。

#### 這張 Figure 在完整流程中的位置

Figure 41 位於 §3.8.3.7，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 PEND 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PEND]
          ↓
[擷取欄位: MSICAP] → [套用編碼: MPEND]
                                      ↓
[驗證證據: MSIX]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PEND` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSICAP` | MSI Capability，MSI capability 結構的基底位置。 |
| `MPEND` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSIX` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Interrupt` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.3.7。
2. 依圖中指定的寬度與位置解碼 PEND；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MSICAP 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 41 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.3.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.3.7 如何排列 PEND、MSICAP 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.3.7 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 41 對應的 raw value 或 buffer，標出包含 PEND 的 bytes 並解碼，再獨立核對 MSICAP。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 PEND，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 PEND 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MSICAP 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** PEND, MSICAP, MPEND, MSIX, Interrupt

**來源 keyword 索引：** `optional`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.7, Figure 41, 文件頁 24, PDF 頁 24

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 42: MSI-X Capability (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-042-CLAIM figure-table:PCIE14-FIG-042 -->

**SPEC。** Figure 42〈MSI-X Capability (Optional)〉：定義〈MSI-X Capability (Optional)〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MSIX, MSIXCAP, MXID, ID, MXC, MTAB, BIR, MPBA。

#### 這張 Figure 在完整流程中的位置

Figure 42 位於 §3.8.3.7，在本流程中是「interrupt」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 MSIX 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 interrupt delivery／capability 圖。把 vector source、enable、mask、pending、delivery 與 handler service 分開；interrupt 只通知有工作，CQE 才是 command completion 的資料來源。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MSIX]
          ↓
[擷取欄位: MSIXCAP] → [套用編碼: MXID]
                                      ↓
[驗證證據: ID]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MSIX` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSIXCAP` | MSI-X Capability，MSI-X capability 結構的基底位置。 |
| `MXID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MXC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MTAB` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.3.7。
2. 依圖中指定的寬度與位置解碼 MSIX；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MSIXCAP 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 42 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.3.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.3.7 如何排列 MSIX、MSIXCAP 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.3.7 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 42 對應的 raw value 或 buffer，標出包含 MSIX 的 bytes 並解碼，再獨立核對 MSIXCAP。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 MSIX，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 MSIX 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MSIXCAP 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** MSIX, MSIXCAP, MXID, ID, MXC, MTAB, BIR, MPBA

**來源 keyword 索引：** `shall not`, `shall`, `should`, `may`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.7, Figure 42, 文件頁 24, PDF 頁 24

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 43: Offset MSIXCAP: MXID - MSI-X Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-043-CLAIM figure-table:PCIE14-FIG-043 -->

**SPEC。** Figure 43〈Offset MSIXCAP: MXID - MSI-X Identifiers〉：定義 offset MSIXCAP 的 MXID（MSI-X Identifiers），並指出軟體在該位置必須分別解碼的欄位。 先定位 MXID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NEXT, CID, MSIXCAP, MXID, MSIX, ID。

#### 這張 Figure 在完整流程中的位置

Figure 43 位於 §3.8.4.1，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NEXT 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NEXT]
          ↓
[擷取欄位: CID] → [套用編碼: MSIXCAP]
                                      ↓
[驗證證據: MXID]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NEXT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CID` | Command Identifier，與 SQ identifier 合用以辨識 outstanding command。 |
| `MSIXCAP` | MSI-X Capability，MSI-X capability 結構的基底位置。 |
| `MXID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSIX` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.4.1。
2. 依圖中指定的寬度與位置解碼 NEXT；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 43 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.4.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.4.1 如何排列 NEXT、CID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.4.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 43 對應的 raw value 或 buffer，標出包含 NEXT 的 bytes 並解碼，再獨立核對 CID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NEXT，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NEXT 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NEXT, CID, MSIXCAP, MXID, MSIX, ID

**來源 keyword 索引：** `may`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.1, Figure 43, 文件頁 24, PDF 頁 24

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 44: Offset MSIXCAP + 2h: MXC - MSI-X Message Control</strong></summary>

<!-- claim:PCIE14-FIG-044-CLAIM figure-table:PCIE14-FIG-044 -->

**SPEC。** Figure 44〈Offset MSIXCAP + 2h: MXC - MSI-X Message Control〉：定義 offset MSIXCAP + 2h 的 MXC（MSI-X Message Control），並指出軟體在該位置必須分別解碼的欄位。 先定位 MXC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：MXE, FM, TS, MSIXCAP, MXC, MSIX, MSI, SIG。

#### 這張 Figure 在完整流程中的位置

Figure 44 位於 §3.8.4.2，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 MXE 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MXE]
          ↓
[擷取欄位: FM] → [套用編碼: TS]
                                      ↓
[驗證證據: MSIXCAP]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MXE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `TS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSIXCAP` | MSI-X Capability，MSI-X capability 結構的基底位置。 |
| `MXC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSIX` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.4.2。
2. 依圖中指定的寬度與位置解碼 MXE；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 FM 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 44 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.4.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.4.2 如何排列 MXE、FM 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.4.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 44 對應的 raw value 或 buffer，標出包含 MXE 的 bytes 並解碼，再獨立核對 FM。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 MXE，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 MXE 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 FM 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** MXE, FM, TS, MSIXCAP, MXC, MSIX, MSI, SIG

**來源 keyword 索引：** `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.2, Figure 44, 文件頁 24-25, PDF 頁 24-25

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 45: Offset MSIXCAP + 4h: MTAB - MSI-X Table Offset / Table BIR</strong></summary>

<!-- claim:PCIE14-FIG-045-CLAIM figure-table:PCIE14-FIG-045 -->

**SPEC。** Figure 45〈Offset MSIXCAP + 4h: MTAB - MSI-X Table Offset / Table BIR〉：定義 offset MSIXCAP + 4h 的 MTAB（MSI-X Table Offset / Table BIR），並指出軟體在該位置必須分別解碼的欄位。 先定位 MTAB，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：TO, TBIR, MSIXCAP, MTAB, MSIX, BIR, MSI, BAR。

#### 這張 Figure 在完整流程中的位置

Figure 45 位於 §3.8.4.3，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 TO 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TO]
          ↓
[擷取欄位: TBIR] → [套用編碼: MSIXCAP]
                                      ↓
[驗證證據: MTAB]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TO` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `TBIR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSIXCAP` | MSI-X Capability，MSI-X capability 結構的基底位置。 |
| `MTAB` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSIX` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `BIR` | BAR Indicator Register，指出某個記憶體結構位於哪一個 PCIe BAR。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.4.3。
2. 依圖中指定的寬度與位置解碼 TO；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 TBIR 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 45 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.4.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.4.3 如何排列 TO、TBIR 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.4.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 45 對應的 raw value 或 buffer，標出包含 TO 的 bytes 並解碼，再獨立核對 TBIR。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 TO，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 TO 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 TBIR 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** TO, TBIR, MSIXCAP, MTAB, MSIX, BIR, MSI, BAR

**來源 keyword 索引：** `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.3, Figure 45, 文件頁 25, PDF 頁 25

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 46: Offset MSIXCAP + 8h: MPBA - MSI-X PBA Offset / PBA BIR</strong></summary>

<!-- claim:PCIE14-FIG-046-CLAIM figure-table:PCIE14-FIG-046 -->

**SPEC。** Figure 46〈Offset MSIXCAP + 8h: MPBA - MSI-X PBA Offset / PBA BIR〉：定義 offset MSIXCAP + 8h 的 MPBA（MSI-X PBA Offset / PBA BIR），並指出軟體在該位置必須分別解碼的欄位。 先定位 MPBA，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PBAO, PBIR, MSIXCAP, MPBA, MSIX, PBA, BIR, MSI。

#### 這張 Figure 在完整流程中的位置

Figure 46 位於 §3.8.4.4，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 PBAO 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PBAO]
          ↓
[擷取欄位: PBIR] → [套用編碼: MSIXCAP]
                                      ↓
[驗證證據: MPBA]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PBAO` | Page Base Address and Offset，第一個 PRP entry 中同時包含 page base 與 page 內 offset 的配置。 |
| `PBIR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSIXCAP` | MSI-X Capability，MSI-X capability 結構的基底位置。 |
| `MPBA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSIX` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PBA` | Pending Bit Array，MSI-X 中記錄尚待處理 vector 的 bit array。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.4.4。
2. 依圖中指定的寬度與位置解碼 PBAO；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 PBIR 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 46 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.4.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.4.4 如何排列 PBAO、PBIR 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.4.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 46 對應的 raw value 或 buffer，標出包含 PBAO 的 bytes 並解碼，再獨立核對 PBIR。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 PBIR 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** PBAO, PBIR, MSIXCAP, MPBA, MSIX, PBA, BIR, MSI

**來源 keyword 索引：** `may`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.4, Figure 46, 文件頁 25, PDF 頁 25

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 47: PCI Express Capability</strong></summary>

<!-- claim:PCIE14-FIG-047-CLAIM figure-table:PCIE14-FIG-047 -->

**SPEC。** Figure 47〈PCI Express Capability〉：定義〈PCI Express Capability〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PXCAP, PXID, ID, PXDCAP, PXDC, PXDS, PXLCAP, PXLC。

#### 這張 Figure 在完整流程中的位置

Figure 47 位於 §3.8.5，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 PXCAP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PXCAP]
          ↓
[擷取欄位: PXID] → [套用編碼: ID]
                                      ↓
[驗證證據: PXDCAP]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PXCAP` | PCI Express Capability，PCIe capability 結構的基底位置。 |
| `PXID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PXDCAP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PXDC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PXDS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.5。
2. 依圖中指定的寬度與位置解碼 PXCAP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 PXID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 47 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.5 如何排列 PXCAP、PXID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.5 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 47 對應的 raw value 或 buffer，標出包含 PXCAP 的 bytes 並解碼，再獨立核對 PXID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 PXCAP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 PXCAP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 PXID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** PXCAP, PXID, ID, PXDCAP, PXDC, PXDS, PXLCAP, PXLC

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5, Figure 47, 文件頁 26, PDF 頁 26

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 48: Offset PXCAP: PXID - PCI Express Capability ID</strong></summary>

<!-- claim:PCIE14-FIG-048-CLAIM figure-table:PCIE14-FIG-048 -->

**SPEC。** Figure 48〈Offset PXCAP: PXID - PCI Express Capability ID〉：定義 offset PXCAP 的 PXID（PCI Express Capability ID），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NEXT, CID, PXCAP, PXID, ID。

#### 這張 Figure 在完整流程中的位置

Figure 48 位於 §3.8.5.1，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NEXT 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NEXT]
          ↓
[擷取欄位: CID] → [套用編碼: PXCAP]
                                      ↓
[驗證證據: PXID]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NEXT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CID` | Command Identifier，與 SQ identifier 合用以辨識 outstanding command。 |
| `PXCAP` | PCI Express Capability，PCIe capability 結構的基底位置。 |
| `PXID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.5.1。
2. 依圖中指定的寬度與位置解碼 NEXT；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 48 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.5.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.5.1 如何排列 NEXT、CID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.5.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 48 對應的 raw value 或 buffer，標出包含 NEXT 的 bytes 並解碼，再獨立核對 CID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NEXT，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NEXT 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NEXT, CID, PXCAP, PXID, ID

**來源 keyword 索引：** `may`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.1, Figure 48, 文件頁 26, PDF 頁 26

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 49: Offset PXCAP + 2h: PXCAP - PCI Express Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-049-CLAIM figure-table:PCIE14-FIG-049 -->

**SPEC。** Figure 49〈Offset PXCAP + 2h: PXCAP - PCI Express Capabilities〉：定義 offset PXCAP + 2h 的 PXCAP（PCI Express Capabilities），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXCAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：IMN, SI, DPT, VER, PXCAP, SIG, MSI。

#### 這張 Figure 在完整流程中的位置

Figure 49 位於 §3.8.5.2，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 IMN 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: IMN]
          ↓
[擷取欄位: SI] → [套用編碼: DPT]
                                      ↓
[驗證證據: VER]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `IMN` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SI` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `DPT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `VER` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PXCAP` | PCI Express Capability，PCIe capability 結構的基底位置。 |
| `SIG` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.5.2。
2. 依圖中指定的寬度與位置解碼 IMN；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 SI 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 49 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.5.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.5.2 如何排列 IMN、SI 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.5.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 49 對應的 raw value 或 buffer，標出包含 IMN 的 bytes 並解碼，再獨立核對 SI。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 IMN，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 IMN 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 SI 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** IMN, SI, DPT, VER, PXCAP, SIG, MSI

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.2, Figure 49, 文件頁 26, PDF 頁 26

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 50: Offset PXCAP + 4h: PXDCAP - PCI Express Device Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-050-CLAIM figure-table:PCIE14-FIG-050 -->

**SPEC。** Figure 50〈Offset PXCAP + 4h: PXDCAP - PCI Express Device Capabilities〉：定義 offset PXCAP + 4h 的 PXDCAP（PCI Express Device Capabilities），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXDCAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：FLRC, CSPLS, CSPLV, RER, L1L, L0SL, ETFS, PFS。

#### 這張 Figure 在完整流程中的位置

Figure 50 位於 §3.8.5.3，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 FLRC 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: FLRC]
          ↓
[擷取欄位: CSPLS] → [套用編碼: CSPLV]
                                      ↓
[驗證證據: RER]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `FLRC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CSPLS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CSPLV` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `RER` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `L1L` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `L0SL` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.5.3。
2. 依圖中指定的寬度與位置解碼 FLRC；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CSPLS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 50 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.5.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.5.3 如何排列 FLRC、CSPLS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.5.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 50 對應的 raw value 或 buffer，標出包含 FLRC 的 bytes 並解碼，再獨立核對 CSPLS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 FLRC，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 FLRC 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CSPLS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** FLRC, CSPLS, CSPLV, RER, L1L, L0SL, ETFS, PFS

**來源 keyword 索引：** `shall`, `may`, `optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.3, Figure 50, 文件頁 26-27, PDF 頁 26-27

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 51: Offset PXCAP + 8h: PXDC - PCI Express Device Control</strong></summary>

<!-- claim:PCIE14-FIG-051-CLAIM figure-table:PCIE14-FIG-051 -->

**SPEC。** Figure 51〈Offset PXCAP + 8h: PXDC - PCI Express Device Control〉：定義 offset PXCAP + 8h 的 PXDC（PCI Express Device Control），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXDC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：IFLR, MRRS, ENS, APPME, PFE, ETE, MPS, ERO。

#### 這張 Figure 在完整流程中的位置

Figure 51 位於 §3.8.5.4，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 IFLR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: IFLR]
          ↓
[擷取欄位: MRRS] → [套用編碼: ENS]
                                      ↓
[驗證證據: APPME]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `IFLR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MRRS` | Max Read Request Size，PCIe Function 可發出之 read request 的最大大小設定。 |
| `ENS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `APPME` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PFE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ETE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.5.4。
2. 依圖中指定的寬度與位置解碼 IFLR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MRRS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 51 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.5.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.5.4 如何排列 IFLR、MRRS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.5.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 51 對應的 raw value 或 buffer，標出包含 IFLR 的 bytes 並解碼，再獨立核對 MRRS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 IFLR，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 IFLR 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MRRS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** IFLR, MRRS, ENS, APPME, PFE, ETE, MPS, ERO

**來源 keyword 索引：** `shall not`, `shall`, `may`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.4, Figure 51, 文件頁 27-28, PDF 頁 27-28

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 52: Offset PXCAP + Ah: PXDS - PCI Express Device Status</strong></summary>

<!-- claim:PCIE14-FIG-052-CLAIM figure-table:PCIE14-FIG-052 -->

**SPEC。** Figure 52〈Offset PXCAP + Ah: PXDS - PCI Express Device Status〉：定義 offset PXCAP + Ah 的 PXDS（PCI Express Device Status），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXDS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：TP, APD, URD, FED, NFED, CED, PXCAP, PXDS。

#### 這張 Figure 在完整流程中的位置

Figure 52 位於 §3.8.5.5，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 TP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TP]
          ↓
[擷取欄位: APD] → [套用編碼: URD]
                                      ↓
[驗證證據: FED]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `APD` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `URD` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FED` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NFED` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CED` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.5.5。
2. 依圖中指定的寬度與位置解碼 TP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 APD 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 52 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.5.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.5.5 如何排列 TP、APD 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.5.5 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 52 對應的 raw value 或 buffer，標出包含 TP 的 bytes 並解碼，再獨立核對 APD。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 TP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 TP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 APD 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** TP, APD, URD, FED, NFED, CED, PXCAP, PXDS

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.5, Figure 52, 文件頁 28, PDF 頁 28

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 53: Offset PXCAP + Ch: PXLCAP - PCI Express Link Capabilities</strong></summary>

<!-- claim:PCIE14-FIG-053-CLAIM figure-table:PCIE14-FIG-053 -->

**SPEC。** Figure 53〈Offset PXCAP + Ch: PXLCAP - PCI Express Link Capabilities〉：定義 offset PXCAP + Ch 的 PXLCAP（PCI Express Link Capabilities），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXLCAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：PN, AOC, LBNC, DLLLA, SDERC, CPM, L1EL, L0SEL。

#### 這張 Figure 在完整流程中的位置

Figure 53 位於 §3.8.5.6，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 PN 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PN]
          ↓
[擷取欄位: AOC] → [套用編碼: LBNC]
                                      ↓
[驗證證據: DLLLA]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PN` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AOC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `LBNC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `DLLLA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SDERC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CPM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.5.6。
2. 依圖中指定的寬度與位置解碼 PN；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 AOC 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 53 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.5.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.5.6 如何排列 PN、AOC 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.5.6 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 53 對應的 raw value 或 buffer，標出包含 PN 的 bytes 並解碼，再獨立核對 AOC。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 PN，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 PN 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 AOC 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** PN, AOC, LBNC, DLLLA, SDERC, CPM, L1EL, L0SEL

**來源 keyword 索引：** `shall not`, `shall`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.6, Figure 53, 文件頁 28-29, PDF 頁 28-29

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 54: Offset PXCAP + 10h: PXLC - PCI Express Link Control</strong></summary>

<!-- claim:PCIE14-FIG-054-CLAIM figure-table:PCIE14-FIG-054 -->

**SPEC。** Figure 54〈Offset PXCAP + 10h: PXLC - PCI Express Link Control〉：定義 offset PXCAP + 10h 的 PXLC（PCI Express Link Control），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXLC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：HAWD, ECPM, ES, CCC, RCB, ASPMC, PXCAP, PXLC。

#### 這張 Figure 在完整流程中的位置

Figure 54 位於 §3.8.5.7，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 HAWD 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: HAWD]
          ↓
[擷取欄位: ECPM] → [套用編碼: ES]
                                      ↓
[驗證證據: CCC]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `HAWD` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ECPM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ES` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CCC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `RCB` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ASPMC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.5.7。
2. 依圖中指定的寬度與位置解碼 HAWD；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 ECPM 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 54 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.5.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.5.7 如何排列 HAWD、ECPM 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.5.7 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 54 對應的 raw value 或 buffer，標出包含 HAWD 的 bytes 並解碼，再獨立核對 ECPM。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 HAWD，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 HAWD 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 ECPM 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** HAWD, ECPM, ES, CCC, RCB, ASPMC, PXCAP, PXLC

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.7, Figure 54, 文件頁 29, PDF 頁 29

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 55: Offset PXCAP + 12h: PXLS - PCI Express Link Status</strong></summary>

<!-- claim:PCIE14-FIG-055-CLAIM figure-table:PCIE14-FIG-055 -->

**SPEC。** Figure 55〈Offset PXCAP + 12h: PXLS - PCI Express Link Status〉：定義 offset PXCAP + 12h 的 PXLS（PCI Express Link Status），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXLS，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：SCC, NLW, CLS, PXCAP, PXLS, SIG。

#### 這張 Figure 在完整流程中的位置

Figure 55 位於 §3.8.5.8，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SCC 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SCC]
          ↓
[擷取欄位: NLW] → [套用編碼: CLS]
                                      ↓
[驗證證據: PXCAP]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SCC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NLW` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CLS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PXCAP` | PCI Express Capability，PCIe capability 結構的基底位置。 |
| `PXLS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SIG` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.5.8。
2. 依圖中指定的寬度與位置解碼 SCC；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NLW 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 55 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.5.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.5.8 如何排列 SCC、NLW 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.5.8 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 55 對應的 raw value 或 buffer，標出包含 SCC 的 bytes 並解碼，再獨立核對 NLW。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SCC，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SCC 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NLW 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SCC, NLW, CLS, PXCAP, PXLS, SIG

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.8, Figure 55, 文件頁 29, PDF 頁 29

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 56: Offset PXCAP + 24h: PXDCAP2 - PCI Express Device Capabilities 2</strong></summary>

<!-- claim:PCIE14-FIG-056-CLAIM figure-table:PCIE14-FIG-056 -->

**SPEC。** Figure 56〈Offset PXCAP + 24h: PXDCAP2 - PCI Express Device Capabilities 2〉：定義 offset PXCAP + 24h 的 PXDCAP2（PCI Express Device Capabilities 2），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXDCAP2，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：MEETP, EETPS, EFFS, OBFFS, TPHCS, LTRS, NPRPR, AORS。

#### 這張 Figure 在完整流程中的位置

Figure 56 位於 §3.8.5.9，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 MEETP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MEETP]
          ↓
[擷取欄位: EETPS] → [套用編碼: EFFS]
                                      ↓
[驗證證據: OBFFS]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MEETP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `EETPS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `EFFS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `OBFFS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `TPHCS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `LTRS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.5.9。
2. 依圖中指定的寬度與位置解碼 MEETP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 EETPS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 56 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.5.9 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.5.9 如何排列 MEETP、EETPS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.5.9 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 56 對應的 raw value 或 buffer，標出包含 MEETP 的 bytes 並解碼，再獨立核對 EETPS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 MEETP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 MEETP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 EETPS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** MEETP, EETPS, EFFS, OBFFS, TPHCS, LTRS, NPRPR, AORS

**來源 keyword 索引：** `shall`, `optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.9, Figure 56, 文件頁 30, PDF 頁 30

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 57: Offset PXCAP + 28h: PXDC2 - PCI Express Device Control 2</strong></summary>

<!-- claim:PCIE14-FIG-057-CLAIM figure-table:PCIE14-FIG-057 -->

**SPEC。** Figure 57〈Offset PXCAP + 28h: PXDC2 - PCI Express Device Control 2〉：定義 offset PXCAP + 28h 的 PXDC2（PCI Express Device Control 2），並指出軟體在該位置必須分別解碼的欄位。 先定位 PXDC2，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：OBFFE, LTRME, CTD, CTV, PXCAP, PXDC2, SIG, OBFF。

#### 這張 Figure 在完整流程中的位置

Figure 57 位於 §3.8.5.10，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 OBFFE 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: OBFFE]
          ↓
[擷取欄位: LTRME] → [套用編碼: CTD]
                                      ↓
[驗證證據: CTV]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `OBFFE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `LTRME` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CTD` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CTV` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PXCAP` | PCI Express Capability，PCIe capability 結構的基底位置。 |
| `PXDC2` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.5.10。
2. 依圖中指定的寬度與位置解碼 OBFFE；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 LTRME 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 57 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.5.10 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.5.10 如何排列 OBFFE、LTRME 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.5.10 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 57 對應的 raw value 或 buffer，標出包含 OBFFE 的 bytes 並解碼，再獨立核對 LTRME。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 OBFFE，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 OBFFE 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 LTRME 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** OBFFE, LTRME, CTD, CTV, PXCAP, PXDC2, SIG, OBFF

**來源 keyword 索引：** `may`, `optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.10, Figure 57, 文件頁 30-31, PDF 頁 30-31

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 58: Advanced Error Reporting Capability (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-058-CLAIM figure-table:PCIE14-FIG-058 -->

**SPEC。** Figure 58〈Advanced Error Reporting Capability (Optional)〉：定義〈Advanced Error Reporting Capability (Optional)〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：AERCAP, AERID, AER, ID, AERUCES, AERUCEM, AERUCESEV, AERCES。

#### 這張 Figure 在完整流程中的位置

Figure 58 位於 §3.8.5.10，在本流程中是「status」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 AERCAP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 status／error 分類表。先確定 status 所在資料結構與類別，再解 individual code、控制 bit 與 retry 指示。Reserved value 維持未定義；不要因名稱相似便映射到另一層 error code。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: AERCAP]
          ↓
[擷取欄位: AERID] → [套用編碼: AER]
                                      ↓
[驗證證據: ID]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `AERCAP` | Advanced Error Reporting Capability，AER extended capability 結構的基底位置。 |
| `AERID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AER` | Advanced Error Reporting，PCIe 用來分類、遮罩與記錄 link／transaction error 的 capability。 |
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AERUCES` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AERUCEM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.5.10。
2. 依圖中指定的寬度與位置解碼 AERCAP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 AERID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 58 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.5.10 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.5.10 如何排列 AERCAP、AERID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.5.10 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 58 對應的 raw value 或 buffer，標出包含 AERCAP 的 bytes 並解碼，再獨立核對 AERID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 AERCAP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 AERCAP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 AERID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** AERCAP, AERID, AER, ID, AERUCES, AERUCEM, AERUCESEV, AERCES

**來源 keyword 索引：** `optional`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.10, Figure 58, 文件頁 31, PDF 頁 31

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 59: Offset AERCAP: AERID - AER Capability ID</strong></summary>

<!-- claim:PCIE14-FIG-059-CLAIM figure-table:PCIE14-FIG-059 -->

**SPEC。** Figure 59〈Offset AERCAP: AERID - AER Capability ID〉：定義 offset AERCAP 的 AERID（AER Capability ID），並指出軟體在該位置必須分別解碼的欄位。 先定位 AERID，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：NEXT, CVER, CID, AERCAP, AERID, AER, ID。

#### 這張 Figure 在完整流程中的位置

Figure 59 位於 §3.8.6.1，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NEXT 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NEXT]
          ↓
[擷取欄位: CVER] → [套用編碼: CID]
                                      ↓
[驗證證據: AERCAP]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NEXT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CVER` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CID` | Command Identifier，與 SQ identifier 合用以辨識 outstanding command。 |
| `AERCAP` | Advanced Error Reporting Capability，AER extended capability 結構的基底位置。 |
| `AERID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AER` | Advanced Error Reporting，PCIe 用來分類、遮罩與記錄 link／transaction error 的 capability。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.6.1。
2. 依圖中指定的寬度與位置解碼 NEXT；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CVER 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 59 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.6.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.6.1 如何排列 NEXT、CVER 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.6.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 59 對應的 raw value 或 buffer，標出包含 NEXT 的 bytes 並解碼，再獨立核對 CVER。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NEXT，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NEXT 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CVER 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NEXT, CVER, CID, AERCAP, AERID, AER, ID

**來源 keyword 索引：** `may`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.1, Figure 59, 文件頁 31, PDF 頁 31

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 60: Offset AERCAP + 4: AERUCES - AER Uncorrectable Error Status Register</strong></summary>

<!-- claim:PCIE14-FIG-060-CLAIM figure-table:PCIE14-FIG-060 -->

**SPEC。** Figure 60〈Offset AERCAP + 4: AERUCES - AER Uncorrectable Error Status Register〉：定義 offset AERCAP + 4 的 AERUCES（AER Uncorrectable Error Status Register），並指出軟體在該位置必須分別解碼的欄位。 先定位 AERUCES，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：TPBES, AOEBS, MCBTS, UIES, ACSVS, ECRCES, ROS, CAS。

#### 這張 Figure 在完整流程中的位置

Figure 60 位於 §3.8.6.2，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 TPBES 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TPBES]
          ↓
[擷取欄位: AOEBS] → [套用編碼: MCBTS]
                                      ↓
[驗證證據: UIES]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TPBES` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AOEBS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MCBTS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `UIES` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ACSVS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ECRCES` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.6.2。
2. 依圖中指定的寬度與位置解碼 TPBES；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 AOEBS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 60 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.6.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.6.2 如何排列 TPBES、AOEBS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.6.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 60 對應的 raw value 或 buffer，標出包含 TPBES 的 bytes 並解碼，再獨立核對 AOEBS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 TPBES，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 TPBES 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 AOEBS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** TPBES, AOEBS, MCBTS, UIES, ACSVS, ECRCES, ROS, CAS

**來源 keyword 索引：** `optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.2, Figure 60, 文件頁 31-32, PDF 頁 31-32

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 61: Offset AERCAP + 8: AERUCEM - AER Uncorrectable Error Mask Register</strong></summary>

<!-- claim:PCIE14-FIG-061-CLAIM figure-table:PCIE14-FIG-061 -->

**SPEC。** Figure 61〈Offset AERCAP + 8: AERUCEM - AER Uncorrectable Error Mask Register〉：定義 offset AERCAP + 8 的 AERUCEM（AER Uncorrectable Error Mask Register），並指出軟體在該位置必須分別解碼的欄位。 先定位 AERUCEM，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：TPBEM, AOEBM, MCBTM, UIEM, ACSVM, ECRCEM, ROM, CAM。

#### 這張 Figure 在完整流程中的位置

Figure 61 位於 §3.8.6.3，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 TPBEM 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TPBEM]
          ↓
[擷取欄位: AOEBM] → [套用編碼: MCBTM]
                                      ↓
[驗證證據: UIEM]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TPBEM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AOEBM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MCBTM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `UIEM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ACSVM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ECRCEM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.6.3。
2. 依圖中指定的寬度與位置解碼 TPBEM；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 AOEBM 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 61 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.6.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.6.3 如何排列 TPBEM、AOEBM 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.6.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 61 對應的 raw value 或 buffer，標出包含 TPBEM 的 bytes 並解碼，再獨立核對 AOEBM。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 TPBEM，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 TPBEM 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 AOEBM 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** TPBEM, AOEBM, MCBTM, UIEM, ACSVM, ECRCEM, ROM, CAM

**來源 keyword 索引：** `optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.3, Figure 61, 文件頁 32, PDF 頁 32

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 62: Offset AERCAP + Ch: AERUCESEV - AER Uncorrectable Error Severity Register</strong></summary>

<!-- claim:PCIE14-FIG-062-CLAIM figure-table:PCIE14-FIG-062 -->

**SPEC。** Figure 62〈Offset AERCAP + Ch: AERUCESEV - AER Uncorrectable Error Severity Register〉：定義 offset AERCAP + Ch 的 AERUCESEV（AER Uncorrectable Error Severity Register），並指出軟體在該位置必須分別解碼的欄位。 先定位 AERUCESEV，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：TPBESEV, AOEBSEV, MCBTSEV, UIESEV, ACSVSEV, ECRCESEV, ROSEV, CASEV。

#### 這張 Figure 在完整流程中的位置

Figure 62 位於 §3.8.6.4，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 TPBESEV 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TPBESEV]
          ↓
[擷取欄位: AOEBSEV] → [套用編碼: MCBTSEV]
                                      ↓
[驗證證據: UIESEV]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TPBESEV` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AOEBSEV` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MCBTSEV` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `UIESEV` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ACSVSEV` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ECRCESEV` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.6.4。
2. 依圖中指定的寬度與位置解碼 TPBESEV；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 AOEBSEV 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 62 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.6.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.6.4 如何排列 TPBESEV、AOEBSEV 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.6.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 62 對應的 raw value 或 buffer，標出包含 TPBESEV 的 bytes 並解碼，再獨立核對 AOEBSEV。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 TPBESEV，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 TPBESEV 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 AOEBSEV 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** TPBESEV, AOEBSEV, MCBTSEV, UIESEV, ACSVSEV, ECRCESEV, ROSEV, CASEV

**來源 keyword 索引：** `optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.4, Figure 62, 文件頁 32-33, PDF 頁 32-33

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 63: Offset AERCAP + 10h: AERCES - AER Correctable Error Status Register</strong></summary>

<!-- claim:PCIE14-FIG-063-CLAIM figure-table:PCIE14-FIG-063 -->

**SPEC。** Figure 63〈Offset AERCAP + 10h: AERCES - AER Correctable Error Status Register〉：定義 offset AERCAP + 10h 的 AERCES（AER Correctable Error Status Register），並指出軟體在該位置必須分別解碼的欄位。 先定位 AERCES，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：HLOS, CIES, AERCAP, AERCES, AER, SIG, RWC, ANFES。

#### 這張 Figure 在完整流程中的位置

Figure 63 位於 §3.8.6.5，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 HLOS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: HLOS]
          ↓
[擷取欄位: CIES] → [套用編碼: AERCAP]
                                      ↓
[驗證證據: AERCES]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `HLOS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CIES` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AERCAP` | Advanced Error Reporting Capability，AER extended capability 結構的基底位置。 |
| `AERCES` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AER` | Advanced Error Reporting，PCIe 用來分類、遮罩與記錄 link／transaction error 的 capability。 |
| `SIG` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.6.5。
2. 依圖中指定的寬度與位置解碼 HLOS；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CIES 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 63 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.6.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.6.5 如何排列 HLOS、CIES 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.6.5 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 63 對應的 raw value 或 buffer，標出包含 HLOS 的 bytes 並解碼，再獨立核對 CIES。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 HLOS，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 HLOS 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CIES 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** HLOS, CIES, AERCAP, AERCES, AER, SIG, RWC, ANFES

**來源 keyword 索引：** `optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.5, Figure 63, 文件頁 33, PDF 頁 33

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 64: Offset AERCAP + 14h: AERCEM - AER Correctable Error Mask Register</strong></summary>

<!-- claim:PCIE14-FIG-064-CLAIM figure-table:PCIE14-FIG-064 -->

**SPEC。** Figure 64〈Offset AERCAP + 14h: AERCEM - AER Correctable Error Mask Register〉：定義 offset AERCAP + 14h 的 AERCEM（AER Correctable Error Mask Register），並指出軟體在該位置必須分別解碼的欄位。 先定位 AERCEM，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：HLOM, CIEM, AERCAP, AERCEM, AER, SIG, ANFEM, RTM。

#### 這張 Figure 在完整流程中的位置

Figure 64 位於 §3.8.6.6，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 HLOM 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: HLOM]
          ↓
[擷取欄位: CIEM] → [套用編碼: AERCAP]
                                      ↓
[驗證證據: AERCEM]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `HLOM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CIEM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AERCAP` | Advanced Error Reporting Capability，AER extended capability 結構的基底位置。 |
| `AERCEM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AER` | Advanced Error Reporting，PCIe 用來分類、遮罩與記錄 link／transaction error 的 capability。 |
| `SIG` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.6.6。
2. 依圖中指定的寬度與位置解碼 HLOM；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CIEM 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 64 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.6.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.6.6 如何排列 HLOM、CIEM 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.6.6 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 64 對應的 raw value 或 buffer，標出包含 HLOM 的 bytes 並解碼，再獨立核對 CIEM。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 HLOM，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 HLOM 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CIEM 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** HLOM, CIEM, AERCAP, AERCEM, AER, SIG, ANFEM, RTM

**來源 keyword 索引：** `optional`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.6, Figure 64, 文件頁 33, PDF 頁 33

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 65: Offset AERCAP + 18h: AERCC - AER Capabilities and Control Register</strong></summary>

<!-- claim:PCIE14-FIG-065-CLAIM figure-table:PCIE14-FIG-065 -->

**SPEC。** Figure 65〈Offset AERCAP + 18h: AERCC - AER Capabilities and Control Register〉：定義 offset AERCAP + 18h 的 AERCC（AER Capabilities and Control Register），並指出軟體在該位置必須分別解碼的欄位。 先定位 AERCC，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：TPLP, MHRE, MHRC, ECE, ECC, EGE, EGC, FEP。

#### 這張 Figure 在完整流程中的位置

Figure 65 位於 §3.8.6.7，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 TPLP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TPLP]
          ↓
[擷取欄位: MHRE] → [套用編碼: MHRC]
                                      ↓
[驗證證據: ECE]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TPLP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MHRE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MHRC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ECE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ECC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `EGE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.6.7。
2. 依圖中指定的寬度與位置解碼 TPLP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MHRE 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 65 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.6.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.6.7 如何排列 TPLP、MHRE 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.6.7 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 65 對應的 raw value 或 buffer，標出包含 TPLP 的 bytes 並解碼，再獨立核對 MHRE。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 TPLP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 TPLP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MHRE 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** TPLP, MHRE, MHRC, ECE, ECC, EGE, EGC, FEP

**來源 keyword 索引：** `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.7, Figure 65, 文件頁 34, PDF 頁 34

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 66: Offset AERCAP + 1Ch: AERHL - AER Header Log Register</strong></summary>

<!-- claim:PCIE14-FIG-066-CLAIM figure-table:PCIE14-FIG-066 -->

**SPEC。** Figure 66〈Offset AERCAP + 1Ch: AERHL - AER Header Log Register〉：定義 offset AERCAP + 1Ch 的 AERHL（AER Header Log Register），並指出軟體在該位置必須分別解碼的欄位。 先定位 AERHL，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：AERCAP, AERHL, AER, HB3, HB2, HB1, HB0, HB7。

#### 這張 Figure 在完整流程中的位置

Figure 66 位於 §3.8.6.8，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 AERCAP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: AERCAP]
          ↓
[擷取欄位: AERHL] → [套用編碼: AER]
                                      ↓
[驗證證據: HB3]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `AERCAP` | Advanced Error Reporting Capability，AER extended capability 結構的基底位置。 |
| `AERHL` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AER` | Advanced Error Reporting，PCIe 用來分類、遮罩與記錄 link／transaction error 的 capability。 |
| `HB3` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `HB2` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `HB1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.6.8。
2. 依圖中指定的寬度與位置解碼 AERCAP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 AERHL 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 66 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.6.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.6.8 如何排列 AERCAP、AERHL 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.6.8 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 66 對應的 raw value 或 buffer，標出包含 AERCAP 的 bytes 並解碼，再獨立核對 AERHL。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 AERCAP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 AERCAP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 AERHL 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** AERCAP, AERHL, AER, HB3, HB2, HB1, HB0, HB7

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.8, Figure 66, 文件頁 34, PDF 頁 34

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 67: Offset AERCAP + 38h: AERTLP - AER TLP Prefix Log Register (Optional)</strong></summary>

<!-- claim:PCIE14-FIG-067-CLAIM figure-table:PCIE14-FIG-067 -->

**SPEC。** Figure 67〈Offset AERCAP + 38h: AERTLP - AER TLP Prefix Log Register (Optional)〉：定義 offset AERCAP + 38h 的 AERTLP（AER TLP Prefix Log Register (Optional)），並指出軟體在該位置必須分別解碼的欄位。 先定位 AERTLP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：AERCAP, AERTLP, AER, TLP, TPL1B3, TPL1B2, TPL1B1, TPL1B0。

#### 這張 Figure 在完整流程中的位置

Figure 67 位於 §3.8.6.9，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 AERCAP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: AERCAP]
          ↓
[擷取欄位: AERTLP] → [套用編碼: AER]
                                      ↓
[驗證證據: TLP]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `AERCAP` | Advanced Error Reporting Capability，AER extended capability 結構的基底位置。 |
| `AERTLP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AER` | Advanced Error Reporting，PCIe 用來分類、遮罩與記錄 link／transaction error 的 capability。 |
| `TLP` | Transaction Layer Packet，PCIe transaction layer 傳送的 packet。 |
| `TPL1B3` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `TPL1B2` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.6.9。
2. 依圖中指定的寬度與位置解碼 AERCAP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 AERTLP 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 67 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.6.9 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.6.9 如何排列 AERCAP、AERTLP 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.6.9 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 67 對應的 raw value 或 buffer，標出包含 AERCAP 的 bytes 並解碼，再獨立核對 AERTLP。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 AERCAP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 AERCAP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 AERTLP 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** AERCAP, AERTLP, AER, TLP, TPL1B3, TPL1B2, TPL1B1, TPL1B0

**來源 keyword 索引：** `shall`, `may`, `optional`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.9, Figure 67, 文件頁 35, PDF 頁 35

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 68: Example of an Eve Diagram in the Printable Eye Field</strong></summary>

<!-- claim:PCIE14-FIG-068-CLAIM figure-table:PCIE14-FIG-068 -->

**SPEC。** Figure 68〈Example of an Eve Diagram in the Printable Eye Field〉：定義〈Example of an Eve Diagram in the Printable Eye Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TEE, VM, OS, TDISP, SR, IOV, SIOV, MI。

#### 這張 Figure 在完整流程中的位置

Figure 68 位於 §3.8.9，在本流程中是「measurement」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 TEE 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張量測資料圖。先確認 support、request selector 與 returned length，再解析 header、descriptor、unit 與 scale；只對實際回傳且完整的 lane／entry 產生結果。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TEE]
          ↓
[擷取欄位: VM] → [套用編碼: OS]
                                      ↓
[驗證證據: TDISP]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TEE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `VM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `OS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `TDISP` | TEE Device Interface Security Protocol，平台隔離與裝置介面狀態相關的 PCIe 安全協定。 |
| `SR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `IOV` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.9。
2. 依圖中指定的寬度與位置解碼 TEE；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 VM 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 68 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.9 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.9 如何排列 TEE、VM 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.9 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 68 對應的 raw value 或 buffer，標出包含 TEE 的 bytes 並解碼，再獨立核對 VM。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 TEE，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 TEE 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 VM 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** TEE, VM, OS, TDISP, SR, IOV, SIOV, MI

**來源 keyword 索引：** `shall`, `may`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.9, Figure 68, 文件頁 37, PDF 頁 37

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 69: NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure</strong></summary>

<!-- claim:PCIE14-FIG-069-CLAIM figure-table:PCIE14-FIG-069 -->

**SPEC。** Figure 69〈NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure〉：定義〈NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TDISP。

#### 這張 Figure 在完整流程中的位置

Figure 69 位於 §3.8.10，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 TDISP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TDISP]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TDISP` | TEE Device Interface Security Protocol，平台隔離與裝置介面狀態相關的 PCIe 安全協定。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.8.10。
2. 依圖中指定的寬度與位置解碼 TDISP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 69 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.8.10 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.8.10 如何排列 TDISP、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.8.10 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 69 對應的 raw value 或 buffer，標出包含 TDISP 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 TDISP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 TDISP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** TDISP

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.10, Figure 69, 文件頁 38-39, PDF 頁 38-39

</details>

<a id="section-3-9"></a>

### §3.9

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 70: Get Log Page - Log Page Identifiers</strong></summary>

<!-- claim:PCIE14-FIG-070-CLAIM figure-table:PCIE14-FIG-070 -->

**SPEC。** Figure 70〈Get Log Page - Log Page Identifiers〉：定義〈Get Log Page - Log Page Identifiers〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：CSI1, CSI。

#### 這張 Figure 在完整流程中的位置

Figure 70 位於 §3.9，在本流程中是「identifier」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CSI1 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 identifier 格式圖。先記錄 width 與 encoding，再辨識 issuing authority、uniqueness scope、reserved value 與有效生命週期；不要把長度相同的 identifiers 當成可互換。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CSI1]
          ↓
[擷取欄位: CSI] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CSI1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CSI` | Command Set Identifier，選擇 command 或 log page 所套用的 I/O Command Set context。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.9。
2. 依圖中指定的寬度與位置解碼 CSI1；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CSI 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 70 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.9 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.9 如何排列 CSI1、CSI 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.9 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 70 對應的 raw value 或 buffer，標出包含 CSI1 的 bytes 並解碼，再獨立核對 CSI。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CSI1，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CSI1 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CSI 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CSI1, CSI

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, Figure 70, 文件頁 39, PDF 頁 39

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 71: Size of Physical Interface Receiver Eye Opening Measurement Log Page</strong></summary>

<!-- claim:PCIE14-FIG-071-CLAIM figure-table:PCIE14-FIG-071 -->

**SPEC。** Figure 71〈Size of Physical Interface Receiver Eye Opening Measurement Log Page〉：呈現〈Size of Physical Interface Receiver Eye Opening Measurement Log Page〉中的 receiver-eye measurement 資訊。 先確認支援與回傳長度，再解 lane、parameter、header 或 descriptor；來源索引：Size of Physical Interface Receiver Eye Opening Measurement Log Page。

#### 這張 Figure 在完整流程中的位置

Figure 71 位於 §3.9.1.1，在本流程中是「measurement」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Size of Physical Interface Receiver Eye Opening Measurement Log Page 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張量測資料圖。先確認 support、request selector 與 returned length，再解析 header、descriptor、unit 與 scale；只對實際回傳且完整的 lane／entry 產生結果。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Size of Physical Interface Receiver Eye Opening Measurement Log Page]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Size of Physical Interface Receiver Eye Opening Measurement Log Page` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.9.1.1。
2. 依圖中指定的寬度與位置解碼 Size of Physical Interface Receiver Eye Opening Measurement Log Page；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 71 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.9.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.9.1.1 如何排列 Size of Physical Interface Receiver Eye Opening Measurement Log Page、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.9.1.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 71 對應的 raw value 或 buffer，標出包含 Size of Physical Interface Receiver Eye Opening Measurement Log Page 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Size of Physical Interface Receiver Eye Opening Measurement Log Page，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Size of Physical Interface Receiver Eye Opening Measurement Log Page 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Size of Physical Interface Receiver Eye Opening Measurement Log Page

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 71, 文件頁 40, PDF 頁 40

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 72: Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field</strong></summary>

<!-- claim:PCIE14-FIG-072-CLAIM figure-table:PCIE14-FIG-072 -->

**SPEC。** Figure 72〈Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field〉：定義〈Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ACT, MQUAL, LPOU, LPOL, EOM, EOMIP。

#### 這張 Figure 在完整流程中的位置

Figure 72 位於 §3.9.1.1，在本流程中是「measurement」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ACT 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張量測資料圖。先確認 support、request selector 與 returned length，再解析 header、descriptor、unit 與 scale；只對實際回傳且完整的 lane／entry 產生結果。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ACT]
          ↓
[擷取欄位: MQUAL] → [套用編碼: LPOU]
                                      ↓
[驗證證據: LPOL]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ACT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MQUAL` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `LPOU` | Log Page Offset Upper，Get Log Page byte offset 的高 32 bits。 |
| `LPOL` | Log Page Offset Lower，Get Log Page byte offset 的低 32 bits。 |
| `EOM` | Eye Opening Measurement，量測 PCIe receiver eye opening 的程序與 log data。 |
| `EOMIP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.9.1.1。
2. 依圖中指定的寬度與位置解碼 ACT；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MQUAL 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 72 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.9.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.9.1.1 如何排列 ACT、MQUAL 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.9.1.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 72 對應的 raw value 或 buffer，標出包含 ACT 的 bytes 並解碼，再獨立核對 MQUAL。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 ACT，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 ACT 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MQUAL 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ACT, MQUAL, LPOU, LPOL, EOM, EOMIP

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 72, 文件頁 40-41, PDF 頁 40-41

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 73: Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field</strong></summary>

<!-- claim:PCIE14-FIG-073-CLAIM figure-table:PCIE14-FIG-073 -->

**SPEC。** Figure 73〈Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field〉：定義〈Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TC, ID, EOM。

#### 這張 Figure 在完整流程中的位置

Figure 73 位於 §3.9.1.1，在本流程中是「identifier」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 TC 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 identifier 格式圖。先記錄 width 與 encoding，再辨識 issuing authority、uniqueness scope、reserved value 與有效生命週期；不要把長度相同的 identifiers 當成可互換。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TC]
          ↓
[擷取欄位: ID] → [套用編碼: EOM]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `EOM` | Eye Opening Measurement，量測 PCIe receiver eye opening 的程序與 log data。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.9.1.1。
2. 依圖中指定的寬度與位置解碼 TC；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 ID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 73 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.9.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.9.1.1 如何排列 TC、ID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.9.1.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 73 對應的 raw value 或 buffer，標出包含 TC 的 bytes 並解碼，再獨立核對 ID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 TC，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 TC 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 ID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** TC, ID, EOM

**來源 keyword 索引：** `shall`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 73, 文件頁 41, PDF 頁 41

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 74: Physical Interface Receiver Eye Opening Measurement Log Page</strong></summary>

<!-- claim:PCIE14-FIG-074-CLAIM figure-table:PCIE14-FIG-074 -->

**SPEC。** Figure 74〈Physical Interface Receiver Eye Opening Measurement Log Page〉：呈現〈Physical Interface Receiver Eye Opening Measurement Log Page〉中的 receiver-eye measurement 資訊。 先確認支援與回傳長度，再解 lane、parameter、header 或 descriptor；來源索引：Physical Interface Receiver Eye Opening Measurement Log Page。

#### 這張 Figure 在完整流程中的位置

Figure 74 位於 §3.9.1.1，在本流程中是「measurement」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Physical Interface Receiver Eye Opening Measurement Log Page 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張量測資料圖。先確認 support、request selector 與 returned length，再解析 header、descriptor、unit 與 scale；只對實際回傳且完整的 lane／entry 產生結果。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Physical Interface Receiver Eye Opening Measurement Log Page]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Physical Interface Receiver Eye Opening Measurement Log Page` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.9.1.1。
2. 依圖中指定的寬度與位置解碼 Physical Interface Receiver Eye Opening Measurement Log Page；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 74 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.9.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.9.1.1 如何排列 Physical Interface Receiver Eye Opening Measurement Log Page、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.9.1.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 74 對應的 raw value 或 buffer，標出包含 Physical Interface Receiver Eye Opening Measurement Log Page 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Physical Interface Receiver Eye Opening Measurement Log Page，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Physical Interface Receiver Eye Opening Measurement Log Page 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Physical Interface Receiver Eye Opening Measurement Log Page

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 74, 文件頁 41, PDF 頁 41

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 75: EOM Header</strong></summary>

<!-- claim:PCIE14-FIG-075-CLAIM figure-table:PCIE14-FIG-075 -->

**SPEC。** Figure 75〈EOM Header〉：呈現〈EOM Header〉中的 receiver-eye measurement 資訊。 先確認支援與回傳長度，再解 lane、parameter、header 或 descriptor；來源索引：EOM。

#### 這張 Figure 在完整流程中的位置

Figure 75 位於 §3.9.1.1，在本流程中是「measurement」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 EOM 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張量測資料圖。先確認 support、request selector 與 returned length，再解析 header、descriptor、unit 與 scale；只對實際回傳且完整的 lane／entry 產生結果。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: EOM]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `EOM` | Eye Opening Measurement，量測 PCIe receiver eye opening 的程序與 log data。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.9.1.1。
2. 依圖中指定的寬度與位置解碼 EOM；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 75 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.9.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.9.1.1 如何排列 EOM、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.9.1.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 75 對應的 raw value 或 buffer，標出包含 EOM 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 EOM，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 EOM 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** EOM

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 75, 文件頁 42-43, PDF 頁 42-43

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 76: EOM Lane Descriptor</strong></summary>

<!-- claim:PCIE14-FIG-076-CLAIM figure-table:PCIE14-FIG-076 -->

**SPEC。** Figure 76〈EOM Lane Descriptor〉：定義〈EOM Lane Descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MSTAT, MSCS, LN, EYE, TOP, BTM, LFT, RGT。

#### 這張 Figure 在完整流程中的位置

Figure 76 位於 §3.9.1.1，在本流程中是「measurement」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 MSTAT 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張量測資料圖。先確認 support、request selector 與 returned length，再解析 header、descriptor、unit 與 scale；只對實際回傳且完整的 lane／entry 產生結果。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MSTAT]
          ↓
[擷取欄位: MSCS] → [套用編碼: LN]
                                      ↓
[驗證證據: EYE]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MSTAT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MSCS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `LN` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `EYE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `TOP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `BTM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.9.1.1。
2. 依圖中指定的寬度與位置解碼 MSTAT；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MSCS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 76 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.9.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.9.1.1 如何排列 MSTAT、MSCS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.9.1.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 76 對應的 raw value 或 buffer，標出包含 MSTAT 的 bytes 並解碼，再獨立核對 MSCS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 MSTAT，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 MSTAT 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MSCS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** MSTAT, MSCS, LN, EYE, TOP, BTM, LFT, RGT

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 76, 文件頁 43-45, PDF 頁 43-45

</details>

<details markdown="1">
<summary><strong>NVME-PCIE-TRANSPORT-1.4 — Figure 77: Example of an Eve Diagram in the Printable Eye Field</strong></summary>

<!-- claim:PCIE14-FIG-077-CLAIM figure-table:PCIE14-FIG-077 -->

**SPEC。** Figure 77〈Example of an Eve Diagram in the Printable Eye Field〉：定義〈Example of an Eve Diagram in the Printable Eye Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Example of an Eve Diagram in the Printable Eye Field。

#### 這張 Figure 在完整流程中的位置

Figure 77 位於 §3.9.1.1，在本流程中是「measurement」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Example of an Eve Diagram in the Printable Eye Field 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張量測資料圖。先確認 support、request selector 與 returned length，再解析 header、descriptor、unit 與 scale；只對實際回傳且完整的 lane／entry 產生結果。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Example of an Eve Diagram in the Printable Eye Field]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Example of an Eve Diagram in the Printable Eye Field` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.9.1.1。
2. 依圖中指定的寬度與位置解碼 Example of an Eve Diagram in the Printable Eye Field；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 77 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.9.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §3.9.1.1 如何排列 Example of an Eve Diagram in the Printable Eye Field、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.9.1.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 77 對應的 raw value 或 buffer，標出包含 Example of an Eve Diagram in the Printable Eye Field 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Example of an Eve Diagram in the Printable Eye Field，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Example of an Eve Diagram in the Printable Eye Field 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Example of an Eve Diagram in the Printable Eye Field

**來源 keyword 索引：** none

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 77, 文件頁 46, PDF 頁 46

</details>

## 使用與限制

製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata 集合或核准範圍改變時，必須重新核對受影響 claim。

## 自問自答：規則、比較、案例與排錯

以下 24 題均附答案，針對本報告範圍複習。每題保留對應教學單元的來源；數值案例與排錯建議屬說明性內容。

### Q01. 「Base 定義 NVMe，PCIe Transport 定義它如何落在 PCIe 上」的核心判讀規則是什麼？

<!-- qa:pcie-transport-1.4-layers-lead -->

**答。**

Figure 1 說明文件適用關係，Figure 2 再把 protocol responsibility 分層。工程上應把『command 語意』與『如何透過 host memory、MMIO、configuration space、interrupt 傳送』分開查證；Transport 發現衝突時不能改寫 Base。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, 文件頁 6, PDF 頁 6; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.3, 文件頁 6-7, PDF 頁 6-7; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, 文件頁 8, PDF 頁 8

### Q02. 「Base 定義 NVMe，PCIe Transport 定義它如何落在 PCIe 上」中，哪些概念或條件必須分開比較？

<!-- qa:pcie-transport-1.4-layers-rows -->

**答。**

- Base — command 與 completion 的共通語意 — 最高優先序的 NVMe 定義
- PCIe Transport — address、register、doorbell、interrupt 綁定 — 補充 PCIe-specific 要求
- PCI-SIG 規格 — 原生 PCIe capability/transaction 語意 — 本報告只引用來源明載的 NVMe-specific 部分

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, 文件頁 6, PDF 頁 6; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.3, 文件頁 6-7, PDF 頁 6-7; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, 文件頁 8, PDF 頁 8

### Q03. 「Base 定義 NVMe，PCIe Transport 定義它如何落在 PCIe 上」如何套用到具體數值或操作情境？

<!-- qa:pcie-transport-1.4-layers-example -->

**答。**

說明性範例：Firmware Commit 的 CA/FS 與 status code 在 Base 解讀；SQE 放在 host memory、doorbell 位於 BAR0/1 memory space、completion 如何觸發 MSI-X，則由 PCIe Transport 補足。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, 文件頁 6, PDF 頁 6; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.3, 文件頁 6-7, PDF 頁 6-7; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, 文件頁 8, PDF 頁 8

### Q04. 「Base 定義 NVMe，PCIe Transport 定義它如何落在 PCIe 上」最容易出現什麼誤判？如何排查？

<!-- qa:pcie-transport-1.4-layers-pitfall -->

**答。**

設計文件的每個欄位旁標 owner specification。若一個 bug report 把 command status、PCIe AER 與 device register access 混成『NVMe error』，recovery 層級通常也會選錯。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, 文件頁 6, PDF 頁 6; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.3, 文件頁 6-7, PDF 頁 6-7; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, 文件頁 8, PDF 頁 8

### Q05. 「從 BAR 到 doorbell offset：每一步都保留單位」的核心判讀規則是什麼？

<!-- qa:pcie-transport-1.4-mmio-doorbell-lead -->

**答。**

NVMe controller registers 位於 BAR0/BAR1 指定的 memory space。Doorbell 從 1000h 起，queue y 的 SQ tail 與 CQ head 依 CAP.DSTRD 計算間距。Figures 3-6 要連成 address derivation，而不是四張獨立 register 表。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, 文件頁 9-10, PDF 頁 9-10; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, 文件頁 10-11, PDF 頁 10-11

### Q06. 「從 BAR 到 doorbell offset：每一步都保留單位」中，哪些概念或條件必須分開比較？

<!-- qa:pcie-transport-1.4-mmio-doorbell-rows -->

**答。**

- SQ y tail — 1000h + (2y) × (4 << DSTRD) — host 公布新 SQ tail
- CQ y head — 1000h + (2y+1) × (4 << DSTRD) — host 公布已消費 CQ head
- doorbell value — queue pointer — 不含 SQE/CQE 本體

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, 文件頁 9-10, PDF 頁 9-10; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, 文件頁 10-11, PDF 頁 10-11

### Q07. 「從 BAR 到 doorbell offset：每一步都保留單位」如何套用到具體數值或操作情境？

<!-- qa:pcie-transport-1.4-mmio-doorbell-example -->

**答。**

說明性範例：DSTRD=1，stride=4<<1=8 bytes。queue 3 的 SQ tail offset =1000h+(6×8)=1030h；CQ head offset =1000h+(7×8)=1038h。兩者只差一個 stride。若把 DSTRD 當成 byte count，所有非零 DSTRD 的 doorbell 位址都會錯。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, 文件頁 9-10, PDF 頁 9-10; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, 文件頁 10-11, PDF 頁 10-11

### Q08. 「從 BAR 到 doorbell offset：每一步都保留單位」最容易出現什麼誤判？如何排查？

<!-- qa:pcie-transport-1.4-mmio-doorbell-pitfall -->

**答。**

doorbell trace 保存 BAR base、DSTRD、queue ID、公式中間值、final physical address、written pointer 與 access width。若 only log final virtual address，無法辨別 BAR mapping、stride 或 queue index 哪一步出錯。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, 文件頁 9-10, PDF 頁 9-10; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, 文件頁 10-11, PDF 頁 10-11

### Q09. 「Figure 8 的八步 command processing 是 ownership handoff」的核心判讀規則是什麼？

<!-- qa:pcie-transport-1.4-command-lead -->

**答。**

SQE、doorbell、controller fetch、CQE、interrupt 與 CQ head 不是同一個事件的不同名稱，而是 host/controller 之間逐步移交 ownership。正確順序同時決定 memory ordering 與資源何時可重用。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, 文件頁 12-13, PDF 頁 12-13; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, 文件頁 11, PDF 頁 11

### Q10. 「Figure 8 的八步 command processing 是 ownership handoff」中，哪些概念或條件必須分開比較？

<!-- qa:pcie-transport-1.4-command-rows -->

**答。**

- SQ slot reuse — controller 已消費該 SQE — 由完成資訊的 SQHD 協助追蹤
- command buffer reuse — command 已 completion 且資料可見 — 依 command/data direction 核對
- CQ slot release — host 已完整消費 CQE — 之後才寫 CQ head doorbell

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, 文件頁 12-13, PDF 頁 12-13; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, 文件頁 11, PDF 頁 11

### Q11. 「Figure 8 的八步 command processing 是 ownership handoff」如何套用到具體數值或操作情境？

<!-- qa:pcie-transport-1.4-command-example -->

**答。**

說明性範例：host 先寫 doorbell、後補 SQE 的最後一個 dword，controller 可能 fetch 到半成品。另一個方向，host 在讀完 CQE 前先更新 CQ head，controller 可能重用該 CQ slot。兩者都是 ownership 順序錯誤，不是 command opcode 問題。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, 文件頁 12-13, PDF 頁 12-13; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, 文件頁 11, PDF 頁 11

### Q12. 「Figure 8 的八步 command processing 是 ownership handoff」最容易出現什麼誤判？如何排查？

<!-- qa:pcie-transport-1.4-command-pitfall -->

**答。**

時間軸同時記錄 CPU core、SQ tail、doorbell MMIO、SQHD、CQ phase、interrupt vector 與 CQ head。分散在不同 log 的事件需用 CID/SQID 與 timestamp 對齊，才能定位 lost interrupt、stale phase 或 memory-ordering 問題。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, 文件頁 12-13, PDF 頁 12-13; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, 文件頁 11, PDF 頁 11

### Q13. 「Interrupt mode 比較：vector 數量、遮罩與 latency 是三個維度」的核心判讀規則是什麼？

<!-- qa:pcie-transport-1.4-interrupts-lead -->

**答。**

pin-based、single-message MSI、multiple-message MSI 與 MSI-X 的差異不只效能。它們提供的 vector 數、masking 位置與 capability structure 不同；interrupt coalescing 另外決定多個 completion 何時合併通知。Figure 9 與 Figures 34-46 應配合 queue-to-vector mapping 閱讀。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, 文件頁 13-16, PDF 頁 13-16; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, 文件頁 11, PDF 頁 11; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, 文件頁 47-48, PDF 頁 47-48

### Q14. 「Interrupt mode 比較：vector 數量、遮罩與 latency 是三個維度」中，哪些概念或條件必須分開比較？

<!-- qa:pcie-transport-1.4-interrupts-rows -->

**答。**

- pin-based — 傳統共享線路 — 共享與 masking 行為不同
- single MSI — 單一 message/vector — 多個 CQ 可能共享服務路徑
- multiple MSI — 一組連續 messages — 受 MME/MMC 等能力限制
- MSI-X — table-based 多 vectors、獨立 mask — 規格建議優先使用

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, 文件頁 13-16, PDF 頁 13-16; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, 文件頁 11, PDF 頁 11; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, 文件頁 47-48, PDF 頁 47-48

### Q15. 「Interrupt mode 比較：vector 數量、遮罩與 latency 是三個維度」如何套用到具體數值或操作情境？

<!-- qa:pcie-transport-1.4-interrupts-example -->

**答。**

說明性範例：CQ 1 與 CQ 2 共用 vector 5。收到 vector 5 時，handler 不能只檢查 CQ 1；它必須處理所有映射到該 vector 的相關 CQs。提高 coalescing threshold 可減少 interrupts，但可能增加 CQE 等待時間。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, 文件頁 13-16, PDF 頁 13-16; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, 文件頁 11, PDF 頁 11; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, 文件頁 47-48, PDF 頁 47-48

### Q16. 「Interrupt mode 比較：vector 數量、遮罩與 latency 是三個維度」最容易出現什麼誤判？如何排查？

<!-- qa:pcie-transport-1.4-interrupts-pitfall -->

**答。**

Interrupt debug 分開檢查 capability enable、CQ IV、MSI/MSI-X mask、pending state、controller CQE 與 host handler。只有『沒有進 ISR』不足以判斷是 controller 沒送、PCIe 沒傳、vector 被 mask 或 handler 漏掃 CQ。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, 文件頁 13-16, PDF 頁 13-16; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, 文件頁 11, PDF 頁 11; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, 文件頁 47-48, PDF 頁 47-48

### Q17. 「Configuration space 是 capability map；AER 是 transport error map」的核心判讀規則是什麼？

<!-- qa:pcie-transport-1.4-config-error-lead -->

**答。**

Figures 10-67 從 Type 0 header 走到 Power Management、MSI/MSI-X、PCIe capability 與 AER。閱讀順序應先找 capability pointer／extended capability，再以該 capability base 加 offset；AER status/mask/severity/header log 應視為一組，不可只截取單一 error bit。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, 文件頁 16-35, PDF 頁 16-35; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, 文件頁 16, PDF 頁 16; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.6, 文件頁 16, PDF 頁 16

### Q18. 「Configuration space 是 capability map；AER 是 transport error map」中，哪些概念或條件必須分開比較？

<!-- qa:pcie-transport-1.4-config-error-rows -->

**答。**

- NVMe CQE status — command 執行結果 — 由 NVMe command context 解
- PCIe Device Status — PCIe Function 狀態摘要 — 位於 PCIe capability
- AER — correctable/uncorrectable transport errors — status、mask、severity、header 一起看
- power state — slot limit 與 device power 控制 — 不得選超過 slot power limit 的 NVMe state

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, 文件頁 16-35, PDF 頁 16-35; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, 文件頁 16, PDF 頁 16; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.6, 文件頁 16, PDF 頁 16

### Q19. 「Configuration space 是 capability map；AER 是 transport error map」如何套用到具體數值或操作情境？

<!-- qa:pcie-transport-1.4-config-error-example -->

**答。**

說明性範例：AERUCES 某 bit 被設為 1，先查對應 mask 判斷是否會回報，再查 severity 判斷錯誤嚴重程度及其處置，最後用 header log 取得 transaction context。不能把該 bit 直接翻成某個 NVMe SC。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, 文件頁 16-35, PDF 頁 16-35; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, 文件頁 16, PDF 頁 16; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.6, 文件頁 16, PDF 頁 16

### Q20. 「Configuration space 是 capability map；AER 是 transport error map」最容易出現什麼誤判？如何排查？

<!-- qa:pcie-transport-1.4-config-error-pitfall -->

**答。**

configuration dump 要保留 capability base，而不只保存 register value。相同 offset 若相對於不同 capability base 會指到不同欄位；AER snapshot 也應在清除 RW1C status 前一次保存完整集合。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, 文件頁 16-35, PDF 頁 16-35; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, 文件頁 16, PDF 頁 16; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.6, 文件頁 16, PDF 頁 16

### Q21. 「EOM parser：先 size，再 header，再 lane descriptor」的核心判讀規則是什麼？

<!-- qa:pcie-transport-1.4-eom-lead -->

**答。**

Physical Interface Receiver Eye Opening Measurement log page 是變長資料結構。host 先確認 support 與需要的大小，再讀 specific parameter/identifier、header、lane descriptor 與 measurement data。Figures 70-77 應形成 parser pipeline，而不是把每個欄位表獨立翻譯。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, 文件頁 39-46, PDF 頁 39-46; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, 文件頁 47-48, PDF 頁 47-48

### Q22. 「EOM parser：先 size，再 header，再 lane descriptor」中，哪些概念或條件必須分開比較？

<!-- qa:pcie-transport-1.4-eom-rows -->

**答。**

- specific parameter — 選量測動作與品質/狀態 — 先決定 request context
- specific identifier — 選 lane/test context — 避免把不同量測混在一起
- header — 全域長度與配置 — 所有後續 offset 的基準
- lane descriptor — 每 lane 邊界/狀態 — 只在 buffer 內走訪

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, 文件頁 39-46, PDF 頁 39-46; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, 文件頁 47-48, PDF 頁 47-48

### Q23. 「EOM parser：先 size，再 header，再 lane descriptor」如何套用到具體數值或操作情境？

<!-- qa:pcie-transport-1.4-eom-example -->

**答。**

說明性範例：header 宣稱有 8 個 lane descriptors，但 buffer length 只能容納 6 個完整 descriptors。parser 應回報 truncated structure 並停止，不得根據平台預期 lane count 讀過 buffer 結尾。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, 文件頁 39-46, PDF 頁 39-46; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, 文件頁 47-48, PDF 頁 47-48

### Q24. 「EOM parser：先 size，再 header，再 lane descriptor」最容易出現什麼誤判？如何排查？

<!-- qa:pcie-transport-1.4-eom-pitfall -->

**答。**

保存 request parameter、identifier、returned byte count、header-declared size、lane number 與 measurement status。只有最終 eye 圖不足以重現 selector、length 或 lane mapping 錯誤。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, 文件頁 39-46, PDF 頁 39-46; 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, 文件頁 47-48, PDF 頁 47-48
