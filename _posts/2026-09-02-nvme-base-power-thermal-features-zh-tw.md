---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4：Power／Thermal Features 與 Power Management"
date: 2026-09-02
description: "供 GitHub Pages 與 PPT 使用的 NVMe 規格導讀。"
lang: zh-Hant-TW
img: posts/2026/dogMC_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---

# NVMe Base 2.4：Power／Thermal Features 與 Power Management

用途：供 GitHub Pages 閱讀與 100 分鐘簡報製作；讀者已具備 PCIe 與 NVMe 基礎。

範圍：§5.2.12、§5.2.30 共通命令、FID 02h／04h／0Ch／10h／11h，以及 §8.1.19～§8.1.19.5；含五張最小 dependency Figure，排除 Power Limit、IIELL、其他 FID 與傳輸專屬內容。正文只保留 PCIe／memory-based 與通用 NVMe 內容。

## 來源版本

NVM Express Base Specification, Revision 2.4

查證日期：2026-09-02。目前未納入其他 Errata、ECN、Technical Proposal、controller vendor 文件或未提供的 PCI Express Base Specification 原文。

## 閱讀地圖

```text
Get capability / value -> Choose host policy -> Set one Feature -> Observe completion / temperature
```

先用 Get Features 區分支援能力與目前值，再依 Power State Descriptor、溫度能力與工作負載選 policy；Set Features 成功後，以 completion、SMART/Health 與實際 latency／temperature 形成驗證閉環。

## 規範性用語

shall 譯為「必須」，may 譯為「可／得」，should 譯為「宜／建議」，optional 譯為「選用」。本文不提高或降低原文語氣。

## 先學縮寫：完整 Glossary

下列縮寫會在投影片主線使用前先定義。縮寫本身永遠不夠；設計與 Debug 還要保留 owner、width、unit、scope 與 state。

| 縮寫／名詞 | 白話解釋 | 來源 |
|---|---|---|
| `FID` | Feature Identifier，Get／Set Features 用來選擇功能的 8-bit identifier。 | NVME-BASE-2.4 Rev. 2.4，§5.2.12，文件頁 209，PDF 頁 235 |
| `SEL` | Select，Get Features 用來選 current、default、saved 或 supported-capabilities view 的欄位。 | NVME-BASE-2.4 Rev. 2.4，§5.2.12，文件頁 209-210，PDF 頁 235-236 |
| `UIDX` | UUID Index，指向 UUID List 位置的 index；0 表示未指定 UUID。 | NVME-BASE-2.4 Rev. 2.4，§5.2.12，文件頁 210，PDF 頁 236 |
| `CHANG` | Changeable，指出 Feature value 是否可由 Set Features 變更的 capability bit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.12.1，文件頁 211-212，PDF 頁 237-238 |
| `NSSPEC` | Namespace Specific，指出 Feature 是否具有 per-namespace scope 的 capability bit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.12.1，文件頁 211-212，PDF 頁 237-238 |
| `SVBL` | Saveable，supported-capabilities result 中指出 Feature 是否可保存的 bit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.12.1，文件頁 211-212，PDF 頁 237-238 |
| `SV` | Save，Set Features 要求 controller 同時保存所設定 value 的 bit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30，文件頁 457，PDF 頁 483 |
| `DPTR` | Data Pointer，SQE 中指出 command data buffer 的欄位。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30，文件頁 456-457，PDF 頁 482-483 |
| `PRP` | Physical Region Page，以 memory page 為單位描述 host-addressable data buffer 的 pointer 格式。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30，文件頁 456-457，PDF 頁 482-483 |
| `CQE` | Completion Queue Entry，CQ 中的一筆完成結果資料結構。 | NVME-BASE-2.4 Rev. 2.4，§5.2.12.2，文件頁 212，PDF 頁 238 |
| `SCT` | Status Code Type，先決定 status 所屬大類，再解讀 SC。 | NVME-BASE-2.4 Rev. 2.4，§5.2.12.2，文件頁 212，PDF 頁 238 |
| `SC` | Status Code，在 SCT 上下文中表示具體完成結果的 code。 | NVME-BASE-2.4 Rev. 2.4，§5.2.12.2，文件頁 212，PDF 頁 238 |
| `PSD` | Power State Descriptor，描述一個 power state 的 power、latency、operational 屬性與 relative performance。 | NVME-BASE-2.4 Rev. 2.4，§8.1.19，文件頁 666-668，PDF 頁 692-694 |
| `PS` | Power State，controller 的功耗／效能 operating point；PS0 是最高 maximum-power state。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.2，文件頁 460-461，PDF 頁 486-487 |
| `NPSS` | Number of Power States Support，以 0's-based 方式回報最高支援 power-state number。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.2，文件頁 460-461，PDF 頁 486-487 |
| `MP` | Maximum Power，一個 power state 的 sustained maximum power。 | NVME-BASE-2.4 Rev. 2.4，§8.1.19，文件頁 666-668，PDF 頁 692-694 |
| `NOPS` | Non-Operational State，Power State Descriptor 中指出該 state 不處理 I/O commands 的 bit。 | NVME-BASE-2.4 Rev. 2.4，§8.1.19，文件頁 667-668，PDF 頁 693-694 |
| `ENLAT` | Entry Latency，進入該 power state 的 maximum latency，單位為 microseconds。 | NVME-BASE-2.4 Rev. 2.4，§8.1.19.1，文件頁 668-669，PDF 頁 694-695 |
| `EXLAT` | Exit Latency，離開該 power state 的 maximum latency，單位為 microseconds。 | NVME-BASE-2.4 Rev. 2.4，§8.1.19.1，文件頁 668-669，PDF 頁 694-695 |
| `IDLP` | Idle Power，依規格 idle 測量條件描述的 typical power。 | NVME-BASE-2.4 Rev. 2.4，§8.1.19，文件頁 666-668，PDF 頁 692-694 |
| `ACTP` | Active Power，在指定 workload 與時間窗下描述的 average active power。 | NVME-BASE-2.4 Rev. 2.4，§8.1.19，文件頁 666-668，PDF 頁 692-694 |
| `WH` | Workload Hint，host 提供給 controller 的 workload category 提示，不是效能保證。 | NVME-BASE-2.4 Rev. 2.4，§8.1.19.3，文件頁 669，PDF 頁 695 |
| `APST` | Autonomous Power State Transition，controller 依 idle timer 自主切到 non-operational state 的機制。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.7，文件頁 468-469，PDF 頁 494-495 |
| `APSTE` | Autonomous Power State Transition Enable，啟用 APST table timer 判斷的 bit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.7，文件頁 468-469，PDF 頁 494-495 |
| `ITPT` | Idle Time Prior to Transition，APST entry 的 idle threshold，單位為 milliseconds。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.7，文件頁 469，PDF 頁 495 |
| `ITPS` | Idle Transition Power State，APST entry 選擇的目標 non-operational power state。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.7，文件頁 469，PDF 頁 495 |
| `NOPPME` | Non-Operational Power State Permissive Mode Enable，控制 controller background work 能否暫時超過 non-operational power limit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.11，文件頁 472-473，PDF 頁 498-499 |
| `TMPSEL` | Temperature Sensor Select，選擇 Composite Temperature 或 sensor 1 到 8 的欄位。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.3.1，文件頁 463-464，PDF 頁 489-490 |
| `THSEL` | Threshold Type Select，選擇 over-temperature 或 under-temperature threshold。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.3.1，文件頁 463-464，PDF 頁 489-490 |
| `TMPTH` | Temperature Threshold，16-bit Kelvin threshold value。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.3.1，文件頁 463-464，PDF 頁 489-490 |
| `TMPTHH` | Temperature Threshold Hysteresis，結束 threshold event 時使用的 Kelvin hysteresis。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.3.1，文件頁 463-464，PDF 頁 489-490 |
| `TTC` | Temperature Threshold Critical Warning，SMART／Health Critical Warning 中的溫度 threshold bit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.3，文件頁 462-463，PDF 頁 488-489 |
| `HCTM` | Host Controlled Thermal Management，host 以 TMT1／TMT2 建立兩階段 controller thermal response。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.10, 8.1.19.5，文件頁 472, 670-671，PDF 頁 498, 696-697 |
| `TMT1` | Thermal Management Temperature 1，較輕度 thermal-management threshold，單位 Kelvin。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.10，文件頁 471-472，PDF 頁 497-498 |
| `TMT2` | Thermal Management Temperature 2，較強 thermal-management threshold，單位 Kelvin。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.10，文件頁 471-472，PDF 頁 497-498 |
| `MNTMT` | Minimum Thermal Management Temperature，HCTM 可設定的最低 Kelvin 值。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.10, 8.1.19.5，文件頁 472, 670-671，PDF 頁 498, 696-697 |
| `MXTMT` | Maximum Thermal Management Temperature，HCTM 可設定的最高 Kelvin 值。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.10, 8.1.19.5，文件頁 472, 670-671，PDF 頁 498, 696-697 |
| `WCTEMP` | Warning Composite Temperature Threshold，Identify Controller 回報的 composite warning threshold。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.3，文件頁 462-463，PDF 頁 488-489 |
| `RTD3E` | Runtime D3 Entry Latency，controller 進入 PCIe D3cold 使用情境的預期時間。 | NVME-BASE-2.4 Rev. 2.4，§8.1.19.4，文件頁 669-670，PDF 頁 695-696 |
| `RTD3R` | Runtime D3 Resume Latency，controller 從 PCIe D3cold 使用情境恢復的預期時間。 | NVME-BASE-2.4 Rev. 2.4，§8.1.19.4，文件頁 669-670，PDF 頁 695-696 |

## Visual Atlas：先用圖建立整體位置

每張教學重畫回答不同問題：Architecture 定位元件、Sequence 顯示 ownership、Decode 把 bits 轉成工程值、State 保留 failure evidence；它們不是 Spec 原圖的複製。

### Visual 01: 先 Get、再 Set、最後重新觀測

**View type:** `architecture`

```text
[Identify capability gates]
  ├─ [Get SEL=011b]
  ├─ [Get current/default]
  ├─ [選 FID-specific value]
  ├─ [Set + decode CQE]
  └─ [Get again + observe runtime]
```

**回答的問題：** Feature 不是一個單純 register。Host 要先用 SEL=011b 讀 capability，再分別讀 current／default／saved view，確認 scope 與 persistence 後才寫入。Set completion 只證明 command outcome；重新 Get 與 runtime telemetry 才能證明軟體看見的新 policy。

**支援 Figure：** Figure 93, Figure 197, Figure 198, Figure 199, Figure 200, Figure 201, Figure 202, Figure 463, Figure 464, Figure 465, Figure 466

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.12，文件頁 209，PDF 頁 235; NVME-BASE-2.4 Rev. 2.4，§5.2.12，文件頁 209-210，PDF 頁 235-236; NVME-BASE-2.4 Rev. 2.4，§5.2.12.1，文件頁 211-212，PDF 頁 237-238; NVME-BASE-2.4 Rev. 2.4，§5.2.30，文件頁 457，PDF 頁 483; NVME-BASE-2.4 Rev. 2.4，§5.2.30，文件頁 459，PDF 頁 485

### Visual 02: Power state 是 power、latency 與 performance 的多維 operating point

**View type:** `architecture`

```text
[Identify.NPSS]
  ├─ [讀 PSD[0..NPSS]]
  ├─ [分 operational／non-operational]
  ├─ [算 transition budget]
  ├─ [套 workload latency SLO]
  └─ [選 FID 02h PS／WH]
```

**回答的問題：** 只看 state number 無法判斷是否適合 workload。每一個 PSD 要一起讀 MP、NOPS、ENLAT／EXLAT、IDLP／ACTP 與 relative performance。PS 數字增加通常降低 maximum power，但不代表所有 latency 或 throughput 一定以固定比例變差。

**支援 Figure：** Figure 338, Figure 340, Figure 468, Figure 738, Figure 739, Figure 740

**來源：** NVME-BASE-2.4 Rev. 2.4，§8.1.19，文件頁 666-667，PDF 頁 692-693; NVME-BASE-2.4 Rev. 2.4，§8.1.19，文件頁 666-668，PDF 頁 692-694; NVME-BASE-2.4 Rev. 2.4，§8.1.19.1，文件頁 668-669，PDF 頁 694-695; NVME-BASE-2.4 Rev. 2.4，§8.1.19.2，文件頁 668，PDF 頁 694; NVME-BASE-2.4 Rev. 2.4，§8.1.19，文件頁 667-668，PDF 頁 693-694; NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.2，文件頁 460-461，PDF 頁 486-487; NVME-BASE-2.4 Rev. 2.4，§8.1.19.3，文件頁 669，PDF 頁 695

### Visual 03: APST 是由 idle timer 驅動的 state machine

**View type:** `architecture`

```text
[APSTE=1]
  ├─ [I/O 完成後開始 idle]
  ├─ [持續 idle > ITPT]
  ├─ [轉到 ITPS non-operational]
  ├─ [I/O 到達]
  └─ [回到最近 operational PS]
```

**回答的問題：** APST 的 256-byte buffer 不是 performance table，而是 32 個『idle 多久後進哪個 non-operational state』的 rules。APSTE 決定 timer rules 是否生效；每個 ITPT=0 entry 不參與；I/O 到達又會讓 controller 回到最近 operational state。

**支援 Figure：** Figure 463, Figure 475, Figure 476, Figure 477, Figure 478

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.7，文件頁 468-469，PDF 頁 494-495; NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.7，文件頁 469，PDF 頁 495; NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.7，文件頁 469，PDF 頁 495; NVME-BASE-2.4 Rev. 2.4，§8.1.19，文件頁 668，PDF 頁 694; NVME-BASE-2.4 Rev. 2.4，§5.2.30，文件頁 456-457，PDF 頁 482-483

### Visual 04: Temperature Threshold 把 sensor、event 與 clear point 連成一條線

**View type:** `architecture`

```text
[選 Composite／Sensor]
  ├─ [設定 over／under TMPTH]
  ├─ [設定 TMPTHH]
  ├─ [溫度跨 threshold]
  ├─ [TTC + optional AEN]
  └─ [跨 clear point 後結束 event]
```

**回答的問題：** FID 04h 不只是一個溫度數字。TMPSEL 決定讀哪個 sensor，THSEL 決定 over 或 under，TMPTH 決定觸發點，TMPTHH 決定離開 event 的 clear point；SMART/Health.TTC 與 AEC enable 則把 controller 狀態送回 host。

**支援 Figure：** Figure 213, Figure 470, Figure 474

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.3，文件頁 462-463，PDF 頁 488-489; NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.3.1，文件頁 463-464，PDF 頁 489-490; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.3，文件頁 220-225，PDF 頁 246-251

### Visual 05: HCTM 用兩個 threshold 區分輕度與重度 thermal response

**View type:** `architecture`

```text
[讀 HCTMA／MNTMT／MXTMT]
  ├─ [選 TMT1<TMT2]
  ├─ [Set FID10h]
  ├─ [temperature 到 TMT1]
  ├─ [temperature 到 TMT2]
  └─ [讀 SMART counters／latency]
```

**回答的問題：** HCTM 的目的不是指定固定 clock 或固定 power state，而是讓 host 提供 TMT1／TMT2 兩個 temperature boundaries。controller 在 TMT1 優先降低 performance impact，在 TMT2 則必須更積極控制 temperature；實際 hysteresis 與內部動作屬 vendor implementation。

**支援 Figure：** Figure 213, Figure 338, Figure 482, Figure 741

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.10，文件頁 471-472，PDF 頁 497-498; NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.10, 8.1.19.5，文件頁 472, 670-671，PDF 頁 498, 696-697; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.3，文件頁 220-225，PDF 頁 246-251

### Visual 06: 把 policy、state、event 與量測串成可重現的 Debug 證據

**View type:** `architecture`

```text
[capability snapshot]
  ├─ [raw Get／Set commands]
  ├─ [CQE + timestamp]
  ├─ [APST／PS transition]
  ├─ [temperature／TTC／HCTM]
  └─ [I/O latency + recovery decision]
```

**回答的問題：** Power／thermal 問題通常不是一個 bit 錯，而是 capability、policy、transition、background work、thermal event 與 host workload 沒有放在同一條 timeline。FID 11h 的 NOPPME、APST、manual PS、HCTM 與 RTD3 又分別控制不同層次，不能互相替代。

**支援 Figure：** Figure 202, Figure 213, Figure 340, Figure 478, Figure 483

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.7，文件頁 469，PDF 頁 495; NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.11，文件頁 472-473，PDF 頁 498-499; NVME-BASE-2.4 Rev. 2.4，§8.1.19.4，文件頁 669-670，PDF 頁 695-696; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.3，文件頁 220-225，PDF 頁 246-251; NVME-BASE-2.4 Rev. 2.4，§5.2.12.2，文件頁 212，PDF 頁 238

## Mental Model 與完整教學流程

以下依工程因果而非 Spec section 排列；相關 Figure 會回到它支援的流程節點，不以編號順序取代教學故事線。

### Module 01: 先 Get、再 Set、最後重新觀測

**解釋。** Feature 不是一個單純 register。Host 要先用 SEL=011b 讀 capability，再分別讀 current／default／saved view，確認 scope 與 persistence 後才寫入。Set completion 只證明 command outcome；重新 Get 與 runtime telemetry 才能證明軟體看見的新 policy。

```text
Identify capability gates
  ↓
Get SEL=011b
  ↓
Get current/default
  ↓
選 FID-specific value
  ↓
Set + decode CQE
  ↓
Get again + observe runtime
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| SEL=000b | current value | 確認此刻 controller policy |
| SEL=001b | default value | 建立 rollback baseline |
| SEL=010b | saved value | 不等於一定曾經 save |
| SEL=011b | CHANG／NSSPEC／SVBL | 寫入前的 capability gate |

**說明性範例。** 讀 FID 02h current 時 CDW10=00000002h；讀 supported capabilities 時 SEL=3，所以 CDW10=(3×100h)+02h=00000302h。若 CHANG=0，流程在 Set 前停止；若 CHANG=1，再依 NPSS 與 PSD 組合 CDW11。

**常見誤解／Debug。** 不要只印『Get succeeded』。保留原始 CDW10／CDW14、CQE.DW0、SCT／SC／DNR，以及 current/default/saved/capability 哪一個 view；否則同一個 32-bit 回傳值會被錯解成不同語意。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.12，文件頁 209，PDF 頁 235; NVME-BASE-2.4 Rev. 2.4，§5.2.12，文件頁 209-210，PDF 頁 235-236; NVME-BASE-2.4 Rev. 2.4，§5.2.12.1，文件頁 211-212，PDF 頁 237-238; NVME-BASE-2.4 Rev. 2.4，§5.2.30，文件頁 457，PDF 頁 483; NVME-BASE-2.4 Rev. 2.4，§5.2.30，文件頁 459，PDF 頁 485

**關聯 Figure：** Figure 93, Figure 197, Figure 198, Figure 199, Figure 200, Figure 201, Figure 202, Figure 463, Figure 464, Figure 465, Figure 466

### Module 02: Power state 是 power、latency 與 performance 的多維 operating point

**解釋。** 只看 state number 無法判斷是否適合 workload。每一個 PSD 要一起讀 MP、NOPS、ENLAT／EXLAT、IDLP／ACTP 與 relative performance。PS 數字增加通常降低 maximum power，但不代表所有 latency 或 throughput 一定以固定比例變差。

```text
Identify.NPSS
  ↓
讀 PSD[0..NPSS]
  ↓
分 operational／non-operational
  ↓
算 transition budget
  ↓
套 workload latency SLO
  ↓
選 FID 02h PS／WH
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| MP | sustained maximum power | 不是瞬間 sample |
| IDLP／ACTP | idle typical／active average | 測量條件不同 |
| ENLAT／EXLAT | 進入／離開 maximum latency | 跨 state 必須相加 |
| RRT/RRL/RWT/RWL | relative throughput／latency | 只在同類 characteristic 比較 |

**說明性範例。** 說明性計算：目前 PS1.EXLAT=100 µs，目標 PS3.ENLAT=2500 µs，直接 transition budget=2600 µs。若 controller 路徑是 PS1→PS2→PS3，還要加入 PS1.EXLAT+PS2.ENLAT 與 PS2.EXLAT+PS3.ENLAT 的每一段，不可仍用 2600 µs。

**常見誤解／Debug。** FID 02h Set 成功只證明 controller 接受 PS。Debug 還要保存 NPSS、完整目標 PSD、設定前 state、WH、CQE timestamp、第一筆 I/O latency；non-operational state 又要檢查 I/O 是否先 drain。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§8.1.19，文件頁 666-667，PDF 頁 692-693; NVME-BASE-2.4 Rev. 2.4，§8.1.19，文件頁 666-668，PDF 頁 692-694; NVME-BASE-2.4 Rev. 2.4，§8.1.19.1，文件頁 668-669，PDF 頁 694-695; NVME-BASE-2.4 Rev. 2.4，§8.1.19.2，文件頁 668，PDF 頁 694; NVME-BASE-2.4 Rev. 2.4，§8.1.19，文件頁 667-668，PDF 頁 693-694; NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.2，文件頁 460-461，PDF 頁 486-487; NVME-BASE-2.4 Rev. 2.4，§8.1.19.3，文件頁 669，PDF 頁 695

**關聯 Figure：** Figure 338, Figure 340, Figure 468, Figure 738, Figure 739, Figure 740

### Module 03: APST 是由 idle timer 驅動的 state machine

**解釋。** APST 的 256-byte buffer 不是 performance table，而是 32 個『idle 多久後進哪個 non-operational state』的 rules。APSTE 決定 timer rules 是否生效；每個 ITPT=0 entry 不參與；I/O 到達又會讓 controller 回到最近 operational state。

```text
APSTE=1
  ↓
I/O 完成後開始 idle
  ↓
持續 idle > ITPT
  ↓
轉到 ITPS non-operational
  ↓
I/O 到達
  ↓
回到最近 operational PS
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| APSTE=0 | 只允許 host-directed entry | table 可存在但 timer 不驅動 |
| APSTE=1 | host 或 timer entry | ITPT 必須連續滿足 |
| NOPPME=0 | background work 不得超過 non-op limits | 可能延後 controller work |
| NOPPME=1 | background work 可暫時提高 power | 上限仍受最後 operational state 限制 |

**說明性範例。** entry 要在 idle 2000 ms 後進 PS3：ITPT=2000=07D0h，放入 bits31:8 得 07D00000h；ITPS=3，放入 bits7:3 得 18h，所以低 dword=07D00018h。其餘 reserved bits 與 entry 高 dword 保持 0，32 entries 合計 256 bytes。

**常見誤解／Debug。** 常見錯誤包括把 ITPT 當 microseconds、把 ITPS 填 operational state、沒有把未使用 entries 清零，或讓 256-byte PRP buffer 跨越不允許的 page boundary。trace 應保留整個 buffer 的 hash 與逐 entry decode。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.7，文件頁 468-469，PDF 頁 494-495; NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.7，文件頁 469，PDF 頁 495; NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.7，文件頁 469，PDF 頁 495; NVME-BASE-2.4 Rev. 2.4，§8.1.19，文件頁 668，PDF 頁 694; NVME-BASE-2.4 Rev. 2.4，§5.2.30，文件頁 456-457，PDF 頁 482-483

**關聯 Figure：** Figure 463, Figure 475, Figure 476, Figure 477, Figure 478

### Module 04: Temperature Threshold 把 sensor、event 與 clear point 連成一條線

**解釋。** FID 04h 不只是一個溫度數字。TMPSEL 決定讀哪個 sensor，THSEL 決定 over 或 under，TMPTH 決定觸發點，TMPTHH 決定離開 event 的 clear point；SMART/Health.TTC 與 AEC enable 則把 controller 狀態送回 host。

```text
選 Composite／Sensor
  ↓
設定 over／under TMPTH
  ↓
設定 TMPTHH
  ↓
溫度跨 threshold
  ↓
TTC + optional AEN
  ↓
跨 clear point 後結束 event
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| TMPSEL | Composite 或 sensor 1-8 | Get 不使用 all-sensors selector |
| THSEL | over／under | 比較方向相反 |
| TMPTH | 觸發 Kelvin | log raw K 及轉換後 °C |
| TMPTHH | clear hysteresis Kelvin | 不是第二個觸發 threshold |

**說明性範例。** Composite over threshold=343 K（約 70 °C）、hysteresis=5 K：TMPSEL=0、THSEL=0、TMPTH=0157h、TMPTHH=5，所以 CDW11=(5<<22)+0157h=01400157h。event 於 ≥343 K 觸發，降到 338 K（約 65 °C）才結束。

**常見誤解／Debug。** 若 AEN 沒出現，不要立刻判定 threshold 沒作用。依序檢查 AEC.TTHRY／SHCW enable、TTC bit、實際 sensor raw Kelvin、threshold type、hysteresis clear point 與 outstanding Asynchronous Event Request。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.3，文件頁 462-463，PDF 頁 488-489; NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.3.1，文件頁 463-464，PDF 頁 489-490; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.3，文件頁 220-225，PDF 頁 246-251

**關聯 Figure：** Figure 213, Figure 470, Figure 474

### Module 05: HCTM 用兩個 threshold 區分輕度與重度 thermal response

**解釋。** HCTM 的目的不是指定固定 clock 或固定 power state，而是讓 host 提供 TMT1／TMT2 兩個 temperature boundaries。controller 在 TMT1 優先降低 performance impact，在 TMT2 則必須更積極控制 temperature；實際 hysteresis 與內部動作屬 vendor implementation。

```text
讀 HCTMA／MNTMT／MXTMT
  ↓
選 TMT1<TMT2
  ↓
Set FID10h
  ↓
temperature 到 TMT1
  ↓
temperature 到 TMT2
  ↓
讀 SMART counters／latency
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| TMT1 | 較輕度控制起點 | 目標是 minimize impact |
| TMT2 | 較強控制起點 | 溫控優先於 impact |
| MNTMT／MXTMT | 合法設定範圍 | 先做 host-side validation |
| SMART counters | transition count／time | 證明 control loop 真的動作 |

**說明性範例。** 若 MNTMT=273 K、MXTMT=373 K，選 TMT1=343 K、TMT2=353 K 合法，CDW11=(0157h<<16)+0161h=01570161h。FID 10h 可 save；若 capability.SVBL=1 且 policy 要保存，CDW10.SV=1、FID=10h，所以 CDW10=80000010h。

**常見誤解／Debug。** TMT1=TMT2、TMT1>TMT2、超出 MNTMT／MXTMT 或把 Celsius 直接寫入 Kelvin 欄位，都應在 host 端先攔截。實機驗證要記錄 ambient、airflow、workload、sensor sampling cadence 與 host latency，否則 performance impact 無法比較。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.10，文件頁 471-472，PDF 頁 497-498; NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.10, 8.1.19.5，文件頁 472, 670-671，PDF 頁 498, 696-697; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.3，文件頁 220-225，PDF 頁 246-251

**關聯 Figure：** Figure 213, Figure 338, Figure 482, Figure 741

### Module 06: 把 policy、state、event 與量測串成可重現的 Debug 證據

**解釋。** Power／thermal 問題通常不是一個 bit 錯，而是 capability、policy、transition、background work、thermal event 與 host workload 沒有放在同一條 timeline。FID 11h 的 NOPPME、APST、manual PS、HCTM 與 RTD3 又分別控制不同層次，不能互相替代。

```text
capability snapshot
  ↓
raw Get／Set commands
  ↓
CQE + timestamp
  ↓
APST／PS transition
  ↓
temperature／TTC／HCTM
  ↓
I/O latency + recovery decision
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Policy plane | FID02/04/0C/10/11 raw values | 證明 host 要求什麼 |
| State plane | PSD、APST timer、I/O return | 證明 controller 在哪個 state |
| Thermal plane | sensor、TTC、HCTM counters | 證明溫控何時介入 |
| Outcome plane | CQE、latency、power／temperature trace | 證明影響與 recovery |

**說明性範例。** 案例：APSTE=1、idle 2 s 後進 PS3，NOPPME=0。3 s 時 controller background work 未提高 power；4 s 的第一筆 read 先觸發回 operational state，latency spike 應與 PS3.EXLAT 對照。若同時溫度跨 TMT1，還要以 HCTM counter 與 sensor timeline 分辨 exit latency 與 thermal throttling。

**常見誤解／Debug。** 不要用單一結果倒推原因。先問 Set 是否成功、Get 是否讀到預期值、APST timer 是否連續滿足、NOPPME 是否允許 background power、temperature 是否跨 TMT1/TMT2，最後才判斷 controller bug。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.7，文件頁 469，PDF 頁 495; NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.11，文件頁 472-473，PDF 頁 498-499; NVME-BASE-2.4 Rev. 2.4，§8.1.19.4，文件頁 669-670，PDF 頁 695-696; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.3，文件頁 220-225，PDF 頁 246-251; NVME-BASE-2.4 Rev. 2.4，§5.2.12.2，文件頁 212，PDF 頁 238

**關聯 Figure：** Figure 202, Figure 213, Figure 340, Figure 478, Figure 483

## 可追溯的規格重點

前面的 Mental Model 解釋因果；本節保留每個可追溯結論與 normative 強度，供講者備註與審查。

### 1. 先讀後寫：Feature 能力盤點

<!-- claim:BASEPOWER-READ-FIRST -->

Get Features 是讀取 Feature 屬性的 Admin command。工程流程不應從寫入猜測開始，而要先辨認 FID、查 capability，再取得 current／default／saved value。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, 文件頁 209, PDF 頁 235

### 2. SEL 與 FID

<!-- claim:BASEPOWER-GET-SELECT -->

CDW10.SEL 選擇 current=000b、default=001b、saved=010b 或 supported capabilities=011b；CDW10.FID 選 Feature。其餘 SEL encoding reserved。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, 文件頁 209-210, PDF 頁 235-236

### 3. saved value fallback

<!-- claim:BASEPOWER-GET-SAVED -->

若要求 saved value，但 controller 不支援 saved value 或尚無 saved value，controller 會以 default value 運作。這不是『讀取成功就代表曾經儲存』。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, 文件頁 210, PDF 頁 236

### 4. UIDX 使用條件

<!-- claim:BASEPOWER-GET-UIDX -->

CDW14.UIDX 只有在 controller 支援 UUID List 且該 Feature 需要 UUID 關聯時才有意義；未使用時保留為 0。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, 文件頁 210, PDF 頁 236

### 5. CHANG／NSSPEC／SVBL

<!-- claim:BASEPOWER-GET-CAP -->

SEL=011b 時，CQE.DW0 以 CHANG、NSSPEC、SVBL 回報是否可變更、是否 namespace-specific、是否可 save。這三個 capability bits 與 Feature value 是兩種不同資料，不能混解。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12.1, 文件頁 211-212, PDF 頁 237-238

### 6. Get Features failure evidence

<!-- claim:BASEPOWER-GET-STATUS -->

若 Get Features 指定不適用的 Controller Identifier，command-specific status 1Fh 是 Invalid Controller Identifier。Debug 要同時保存 SCT、SC、DNR、CDW10、CDW14 與 target controller。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, 文件頁 212, PDF 頁 238

### 7. Set Features data buffer

<!-- claim:BASEPOWER-SET-DPTR -->

Set Features 的 DPTR 只在所選 Feature 定義 data structure 時使用。以 PRP 指向 buffer 時，該 data buffer 不得跨越超過一個 memory page boundary，因 PRP2 不能在此指向 PRP List。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, 文件頁 456-457, PDF 頁 482-483

### 8. SV 與 saveability

<!-- claim:BASEPOWER-SET-SAVE -->

CDW10.SV=1 要求把值保存為跨 reset／power cycle 可用的 saved value；若 Feature 不可 save，controller 會回 Feature Identifier Not Saveable。先讀 SVBL，再決定是否設 SV。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, 文件頁 457, PDF 頁 483

### 9. 成功後的切換邊界

<!-- claim:BASEPOWER-SET-AFTER -->

Set Features 成功後，後續 commands 必須（shall）使用新設定。若軟體需要讓一批 commands 一致套用舊值或新值，host 宜（should）先讓既有 in-flight commands 完成，再切換。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, 文件頁 459, PDF 頁 485

### 10. 五個 FID 的 scope／persistence

<!-- claim:BASEPOWER-FID-SCOPE -->

本報告五個 FID 的 scope 都是 Controller。FID 02h、04h、0Ch、11h 不支援 save；FID 10h 支援 save。只有 FID 0Ch 需要 256-byte data structure。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, 文件頁 457-459, PDF 頁 483-485

### 11. power state 編號與上限

<!-- claim:BASEPOWER-POWER-STATES -->

controller 必須（shall）至少支援一個 power state，最多可（may）支援 32 個，編號從 0 連續排列。PS0 的 maximum power 最高；後續 state 的 maximum power 不得高於前一個 state。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19, 文件頁 666-667, PDF 頁 692-693

### 12. Power State Descriptor mental model

<!-- claim:BASEPOWER-POWER-METRICS -->

Power State Descriptor（PSD）把 maximum power、operational/non-operational、entry/exit latency、idle/active power 與 relative performance 放在同一份描述。MP 是 sustained maximum；IDLP 與 ACTP 是不同測量情境，不能拿單次瞬間功耗互相比。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19, 文件頁 666-668, PDF 頁 692-694

### 13. entry／exit latency 計算

<!-- claim:BASEPOWER-TRANSITION -->

從舊 state 直接切到新 state 的最大 transition time，是舊 state 的 EXLAT 加上新 state 的 ENLAT。若 controller 內部經過多個 state，則每一段 transition time 相加。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19.1, 文件頁 668-669, PDF 頁 694-695

### 14. relative performance 解讀

<!-- claim:BASEPOWER-RELATIVE -->

Relative Read／Write Throughput 與 Latency 都是『值越小越好』，但只可在相同 characteristic 內比較；throughput code 不能與 latency code 混成一個總分。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19.2, 文件頁 668, PDF 頁 694

### 15. non-operational 不等於關機

<!-- claim:BASEPOWER-NONOP -->

non-operational power state 不處理 I/O commands，但仍可能處理 property、PMR、CMB、Admin／background 或 transport-specific access。『non-operational』不是 controller 關機。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19, 文件頁 667-668, PDF 頁 693-694

### 16. I/O 觸發 operational return

<!-- claim:BASEPOWER-NONOP-IO -->

host 在手動切入 non-operational state 前宜（should）先 drain I/O。若 I/O command 到達，controller 會自主回到最近使用的 operational state，再處理 I/O。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19, 文件頁 668, PDF 頁 694

### 17. FID 02h：手動 power state

<!-- claim:BASEPOWER-FID02 -->

FID 02h 用 CDW11.PS[4:0] 選 power state、WH[7:5] 提供 workload hint。指定的 PS 必須（shall）在 Identify Controller.NPSS 宣告範圍內；不支援的 PS 應（should）以 Invalid Field in Command 中止。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.2, 文件頁 460-461, PDF 頁 486-487

### 18. Workload Hint

<!-- claim:BASEPOWER-WORKLOAD -->

WH=000b 表示未知 workload；001b 對應先 idle、再做 32 筆 random 1 MiB writes、再 idle 的情境；010b 對應 80,000 筆 sequential 128 KiB writes。011b～111b reserved。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19.3, 文件頁 669, PDF 頁 695

### 19. RTD3E／RTD3R 邊界

<!-- claim:BASEPOWER-RTD3 -->

RTD3E 與 RTD3R 分別描述進入與恢復時間，供 PCIe D3cold 使用情境評估 idle break-even；NVMe 文字明確說這不是 D3hot 的時間。PCIe D-state 的完整原始行為不在目前提供來源內，不能據此自行補寫。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19.4, 文件頁 669-670, PDF 頁 695-696

### 20. FID 04h：temperature threshold

<!-- claim:BASEPOWER-FID04 -->

FID 04h 可為 Composite Temperature 與最多八個實作的 temperature sensors 設 over／under threshold。溫度以 Kelvin 編碼；到達 over threshold 或低於等於 under threshold 時，SMART/Health 的 Temperature Threshold critical warning 可能觸發 asynchronous event。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3, 文件頁 462-463, PDF 頁 488-489

### 21. temperature hysteresis

<!-- claim:BASEPOWER-HYST -->

Figure 470 的 TMPSEL 選 sensor、THSEL 選 over/under、TMPTH 是 threshold、TMPTHH 是 hysteresis。over event 在溫度降到 threshold−hysteresis 時結束；under event在溫度升到 threshold+hysteresis 時結束。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3.1, 文件頁 463-464, PDF 頁 489-490

### 22. FID 0Ch：APST enable

<!-- claim:BASEPOWER-FID0C -->

FID 0Ch 的 APSTE=1 啟用 Autonomous Power State Transition（APST）；預設值是 0。啟用只表示 controller 可依 APST table 的 idle timer 自主切換，並不保證一定進入任何特定 state。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, 文件頁 468-469, PDF 頁 494-495

### 23. APST 256-byte table

<!-- claim:BASEPOWER-APST-ENTRY -->

APST data structure 固定 256 bytes，共 32 個 8-byte entries。每格 ITPT[31:8] 是毫秒 idle threshold，ITPS[7:3] 是目標 non-operational state；ITPT=0 會停用該 entry。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, 文件頁 469, PDF 頁 495

### 24. APSTE × NOPPME

<!-- claim:BASEPOWER-APST-NOPPME -->

APSTE 控制 timer-based entry，NOPPME 控制 controller-initiated background operation 是否可暫時超過 non-operational limit。兩者是兩個正交開關：不要把『可自主進 state』誤解成『可為背景工作提高 power』。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, 文件頁 469, PDF 頁 495

### 25. FID 10h：TMT1／TMT2

<!-- claim:BASEPOWER-FID10 -->

FID 10h 的 TMT1[31:16] 是較輕度 thermal management threshold，TMT2[15:0] 是較重度 threshold，單位都是 Kelvin；0h 分別停用對應 threshold。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, 文件頁 471-472, PDF 頁 497-498

### 26. HCTM control loop

<!-- claim:BASEPOWER-HCTM -->

非零 TMT1 必須（shall）小於 TMT2，且兩者必須落在 MNTMT～MXTMT 內；否則回 Invalid Field in Command。達 TMT1 時 controller 採降低影響的動作，達 TMT2 時採更強動作；hysteresis 由 vendor 決定。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, 8.1.19.5, 文件頁 472, 670-671, PDF 頁 498, 696-697

### 27. FID 11h：background power permission

<!-- claim:BASEPOWER-FID11 -->

FID 11h 的 NOPPME=1 允許 controller-initiated background operation 暫時把 power 提高到不超過最後一個 operational state 的上限；NOPPME=0 時，這類工作不得超過目前 non-operational state limits。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.11, 文件頁 472-473, PDF 頁 498-499

### 28. SMART／Health 驗證閉環

<!-- claim:BASEPOWER-OBSERVE -->

設定完成不是驗證終點。SMART/Health 應同時觀察 Composite Temperature、TTC critical warning、warning temperature time、HCTM transition counters 與已實作 sensor readings，再對照 CQE 與 host latency。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, 文件頁 220-225, PDF 頁 246-251

## Figure 索引

本報告介紹全部 27 張納入範圍的 Figure。100 分鐘簡報以 section 主線與必講 Figure 為主，其餘 Figure 仍完整保留作為附錄。其中 5 張位於主章節範圍外，但因指定正文直接引用而納入相依教學。

- [§5.2](#section-5-2)

- [§8.1](#section-8-1)

- [引用相依 Figure（位於主章節範圍外）](#section-dependency)

## Figure／欄位表教學參考

本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。欄位與 keyword 索引來自本機核對過的 PDF。

<a id="section-5-2"></a>

### §5.2

<details markdown="1">
<summary><strong>Figure 197: Get Features – Data Pointer</strong></summary>

<!-- claim:BASEPOWER-FIG-197-CLAIM figure-table:BASEPOWER-FIG-197 -->

**SPEC。** Figure 197〈Get Features – Data Pointer〉：呈現〈Get Features – Data Pointer〉所描述的 power／thermal 控制關係。 依序追蹤 selector、state 或 threshold、transition condition 與觀測證據；來源欄位索引：DPTR, PRP1, PRP2。

#### 這張 Figure 在完整流程中的位置

Figure 197 位於 §5.2.12，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DPTR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DPTR]
          ↓
[擷取欄位: PRP1] → [套用編碼: PRP2]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DPTR` | Data Pointer，SQE 中指出 command data buffer 的欄位。 |
| `PRP1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PRP2` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.12。
2. 依圖中指定的寬度與位置解碼 DPTR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 PRP1 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 197 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.12 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.12 如何排列 DPTR、PRP1 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.12 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 197 對應的 raw value 或 buffer，標出包含 DPTR 的 bytes 並解碼，再獨立核對 PRP1。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 DPTR，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 DPTR 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 PRP1 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** DPTR, PRP1, PRP2

**來源 keyword 索引：** `shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 197, 文件頁 209, PDF 頁 235

</details>

<details markdown="1">
<summary><strong>Figure 198: Get Features – Command Dword 10</strong></summary>

<!-- claim:BASEPOWER-FIG-198-CLAIM figure-table:BASEPOWER-FIG-198 -->

**SPEC。** Figure 198〈Get Features – Command Dword 10〉：定義〈Get Features – Command Dword 10〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：SEL, FID。

#### 這張 Figure 在完整流程中的位置

Figure 198 位於 §5.2.12，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SEL 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SEL]
          ↓
[擷取欄位: FID] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SEL` | Select，Get Features 用來選 current、default、saved 或 supported-capabilities view 的欄位。 |
| `FID` | Feature Identifier，Get／Set Features 用來選擇功能的 8-bit identifier。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.12。
2. 依圖中指定的寬度與位置解碼 SEL；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 FID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 198 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.12 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.12 如何排列 SEL、FID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.12 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 198 對應的 raw value 或 buffer，標出包含 SEL 的 bytes 並解碼，再獨立核對 FID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SEL，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SEL 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 FID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SEL, FID

**來源 keyword 索引：** `shall`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 198, 文件頁 209-210, PDF 頁 235-236

</details>

<details markdown="1">
<summary><strong>Figure 199: Get Features – Command Dword 14</strong></summary>

<!-- claim:BASEPOWER-FIG-199-CLAIM figure-table:BASEPOWER-FIG-199 -->

**SPEC。** Figure 199〈Get Features – Command Dword 14〉：定義〈Get Features – Command Dword 14〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：UIDX。

#### 這張 Figure 在完整流程中的位置

Figure 199 位於 §5.2.12，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 UIDX 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: UIDX]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `UIDX` | UUID Index，指向 UUID List 位置的 index；0 表示未指定 UUID。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.12。
2. 依圖中指定的寬度與位置解碼 UIDX；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 199 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.12 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.12 如何排列 UIDX、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.12 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 199 對應的 raw value 或 buffer，標出包含 UIDX 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 UIDX，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 UIDX 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** UIDX

**來源 keyword 索引：** `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 199, 文件頁 210, PDF 頁 236

</details>

<details markdown="1">
<summary><strong>Figure 200: Feature Identifiers for Get Features</strong></summary>

<!-- claim:BASEPOWER-FIG-200-CLAIM figure-table:BASEPOWER-FIG-200 -->

**SPEC。** Figure 200〈Feature Identifiers for Get Features〉：定義〈Feature Identifiers for Get Features〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：FID 02h, FID 04h, FID 0Ch, FID 10h, FID 11h。

#### 這張 Figure 在完整流程中的位置

Figure 200 位於 §5.2.12，在本流程中是「identifier」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 FID 02h 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 identifier 格式圖。先記錄 width 與 encoding，再辨識 issuing authority、uniqueness scope、reserved value 與有效生命週期；不要把長度相同的 identifiers 當成可互換。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: FID 02h]
          ↓
[擷取欄位: FID 04h] → [套用編碼: FID 0Ch]
                                      ↓
[驗證證據: FID 10h]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `FID 02h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FID 04h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FID 0Ch` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FID 10h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FID 11h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.12。
2. 依圖中指定的寬度與位置解碼 FID 02h；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 FID 04h 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 200 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.12 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.12 如何排列 FID 02h、FID 04h 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.12 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 200 對應的 raw value 或 buffer，標出包含 FID 02h 的 bytes 並解碼，再獨立核對 FID 04h。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 FID 02h，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 FID 02h 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 FID 04h 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** FID 02h, FID 04h, FID 0Ch, FID 10h, FID 11h

**來源 keyword 索引：** `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 200, 文件頁 210-211, PDF 頁 236-237

</details>

<details markdown="1">
<summary><strong>Figure 201: Get Features – Select Supported Capabilities</strong></summary>

<!-- claim:BASEPOWER-FIG-201-CLAIM figure-table:BASEPOWER-FIG-201 -->

**SPEC。** Figure 201〈Get Features – Select Supported Capabilities〉：定義〈Get Features – Select Supported Capabilities〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CHANG, NSSPEC, SVBL。

#### 這張 Figure 在完整流程中的位置

Figure 201 位於 §5.2.12.2，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CHANG 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CHANG]
          ↓
[擷取欄位: NSSPEC] → [套用編碼: SVBL]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CHANG` | Changeable，指出 Feature value 是否可由 Set Features 變更的 capability bit。 |
| `NSSPEC` | Namespace Specific，指出 Feature 是否具有 per-namespace scope 的 capability bit。 |
| `SVBL` | Saveable，supported-capabilities result 中指出 Feature 是否可保存的 bit。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.12.2。
2. 依圖中指定的寬度與位置解碼 CHANG；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NSSPEC 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 201 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.12.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.12.2 如何排列 CHANG、NSSPEC 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.12.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 201 對應的 raw value 或 buffer，標出包含 CHANG 的 bytes 並解碼，再獨立核對 NSSPEC。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CHANG，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CHANG 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NSSPEC 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CHANG, NSSPEC, SVBL

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, Figure 201, 文件頁 212, PDF 頁 238

</details>

<details markdown="1">
<summary><strong>Figure 202: Get Features – Command Specific Status Values</strong></summary>

<!-- claim:BASEPOWER-FIG-202-CLAIM figure-table:BASEPOWER-FIG-202 -->

**SPEC。** Figure 202〈Get Features – Command Specific Status Values〉：定義〈Get Features – Command Specific Status Values〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Invalid Controller Identifier。

#### 這張 Figure 在完整流程中的位置

Figure 202 位於 §5.2.12.2，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Invalid Controller Identifier 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Invalid Controller Identifier]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Invalid Controller Identifier` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.12.2。
2. 依圖中指定的寬度與位置解碼 Invalid Controller Identifier；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 202 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.12.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.12.2 如何排列 Invalid Controller Identifier、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.12.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 202 對應的 raw value 或 buffer，標出包含 Invalid Controller Identifier 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Invalid Controller Identifier，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Invalid Controller Identifier 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Invalid Controller Identifier

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, Figure 202, 文件頁 212, PDF 頁 238

</details>

<details markdown="1">
<summary><strong>Figure 463: Set Features – Data Pointer</strong></summary>

<!-- claim:BASEPOWER-FIG-463-CLAIM figure-table:BASEPOWER-FIG-463 -->

**SPEC。** Figure 463〈Set Features – Data Pointer〉：呈現〈Set Features – Data Pointer〉所描述的 power／thermal 控制關係。 依序追蹤 selector、state 或 threshold、transition condition 與觀測證據；來源欄位索引：DPTR, PRP1, PRP2。

#### 這張 Figure 在完整流程中的位置

Figure 463 位於 §5.2.30，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DPTR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DPTR]
          ↓
[擷取欄位: PRP1] → [套用編碼: PRP2]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DPTR` | Data Pointer，SQE 中指出 command data buffer 的欄位。 |
| `PRP1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PRP2` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30。
2. 依圖中指定的寬度與位置解碼 DPTR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 PRP1 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 463 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30 如何排列 DPTR、PRP1 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 463 對應的 raw value 或 buffer，標出包含 DPTR 的 bytes 並解碼，再獨立核對 PRP1。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 DPTR，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 DPTR 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 PRP1 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** DPTR, PRP1, PRP2

**來源 keyword 索引：** `shall not`, `shall`, `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 463, 文件頁 456, PDF 頁 482

</details>

<details markdown="1">
<summary><strong>Figure 464: Set Features – Command Dword 10</strong></summary>

<!-- claim:BASEPOWER-FIG-464-CLAIM figure-table:BASEPOWER-FIG-464 -->

**SPEC。** Figure 464〈Set Features – Command Dword 10〉：定義〈Set Features – Command Dword 10〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：SV, FID。

#### 這張 Figure 在完整流程中的位置

Figure 464 位於 §5.2.30，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SV 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SV]
          ↓
[擷取欄位: FID] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SV` | Save，Set Features 要求 controller 同時保存所設定 value 的 bit。 |
| `FID` | Feature Identifier，Get／Set Features 用來選擇功能的 8-bit identifier。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30。
2. 依圖中指定的寬度與位置解碼 SV；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 FID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 464 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30 如何排列 SV、FID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 464 對應的 raw value 或 buffer，標出包含 SV 的 bytes 並解碼，再獨立核對 FID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SV，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SV 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 FID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SV, FID

**來源 keyword 索引：** `shall`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 464, 文件頁 457, PDF 頁 483

</details>

<details markdown="1">
<summary><strong>Figure 465: Set Features – Command Dword 14</strong></summary>

<!-- claim:BASEPOWER-FIG-465-CLAIM figure-table:BASEPOWER-FIG-465 -->

**SPEC。** Figure 465〈Set Features – Command Dword 14〉：定義〈Set Features – Command Dword 14〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：UIDX。

#### 這張 Figure 在完整流程中的位置

Figure 465 位於 §5.2.30，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 UIDX 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: UIDX]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `UIDX` | UUID Index，指向 UUID List 位置的 index；0 表示未指定 UUID。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30。
2. 依圖中指定的寬度與位置解碼 UIDX；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 465 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30 如何排列 UIDX、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 465 對應的 raw value 或 buffer，標出包含 UIDX 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 UIDX，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 UIDX 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** UIDX

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 465, 文件頁 457, PDF 頁 483

</details>

<details markdown="1">
<summary><strong>Figure 466: Feature Identifiers for Set Features</strong></summary>

<!-- claim:BASEPOWER-FIG-466-CLAIM figure-table:BASEPOWER-FIG-466 -->

**SPEC。** Figure 466〈Feature Identifiers for Set Features〉：定義〈Feature Identifiers for Set Features〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：FID 02h, FID 04h, FID 0Ch, FID 10h, FID 11h。

#### 這張 Figure 在完整流程中的位置

Figure 466 位於 §5.2.30，在本流程中是「identifier」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 FID 02h 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 identifier 格式圖。先記錄 width 與 encoding，再辨識 issuing authority、uniqueness scope、reserved value 與有效生命週期；不要把長度相同的 identifiers 當成可互換。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: FID 02h]
          ↓
[擷取欄位: FID 04h] → [套用編碼: FID 0Ch]
                                      ↓
[驗證證據: FID 10h]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `FID 02h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FID 04h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FID 0Ch` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FID 10h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FID 11h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30。
2. 依圖中指定的寬度與位置解碼 FID 02h；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 FID 04h 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 466 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30 如何排列 FID 02h、FID 04h 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 466 對應的 raw value 或 buffer，標出包含 FID 02h 的 bytes 並解碼，再獨立核對 FID 04h。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 FID 02h，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 FID 02h 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 FID 04h 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** FID 02h, FID 04h, FID 0Ch, FID 10h, FID 11h

**來源 keyword 索引：** `shall`, `should`, `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 466, 文件頁 457-459, PDF 頁 483-485

</details>

<details markdown="1">
<summary><strong>Figure 468: Power Management – Command Dword 11</strong></summary>

<!-- claim:BASEPOWER-FIG-468-CLAIM figure-table:BASEPOWER-FIG-468 -->

**SPEC。** Figure 468〈Power Management – Command Dword 11〉：定義〈Power Management – Command Dword 11〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：WH, PS。

#### 這張 Figure 在完整流程中的位置

Figure 468 位於 §5.2.30.1.2，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 WH 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: WH]
          ↓
[擷取欄位: PS] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `WH` | Workload Hint，host 提供給 controller 的 workload category 提示，不是效能保證。 |
| `PS` | Power State，controller 的功耗／效能 operating point；PS0 是最高 maximum-power state。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.1.2。
2. 依圖中指定的寬度與位置解碼 WH；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 PS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 468 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.1.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30.1.2 如何排列 WH、PS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.1.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 468 對應的 raw value 或 buffer，標出包含 WH 的 bytes 並解碼，再獨立核對 PS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 WH，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 WH 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 PS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** WH, PS

**來源 keyword 索引：** `shall not`, `shall`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.2, Figure 468, 文件頁 461, PDF 頁 487

</details>

<details markdown="1">
<summary><strong>Figure 470: Temperature Threshold – Command Dword 11</strong></summary>

<!-- claim:BASEPOWER-FIG-470-CLAIM figure-table:BASEPOWER-FIG-470 -->

**SPEC。** Figure 470〈Temperature Threshold – Command Dword 11〉：定義〈Temperature Threshold – Command Dword 11〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TMPTHH, THSEL, TMPSEL, TMPTH。

#### 這張 Figure 在完整流程中的位置

Figure 470 位於 §5.2.30.1.3.1，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 TMPTHH 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TMPTHH]
          ↓
[擷取欄位: THSEL] → [套用編碼: TMPSEL]
                                      ↓
[驗證證據: TMPTH]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TMPTHH` | Temperature Threshold Hysteresis，結束 threshold event 時使用的 Kelvin hysteresis。 |
| `THSEL` | Threshold Type Select，選擇 over-temperature 或 under-temperature threshold。 |
| `TMPSEL` | Temperature Sensor Select，選擇 Composite Temperature 或 sensor 1 到 8 的欄位。 |
| `TMPTH` | Temperature Threshold，16-bit Kelvin threshold value。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.1.3.1。
2. 依圖中指定的寬度與位置解碼 TMPTHH；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 THSEL 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 470 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.1.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30.1.3.1 如何排列 TMPTHH、THSEL 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.1.3.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 470 對應的 raw value 或 buffer，標出包含 TMPTHH 的 bytes 並解碼，再獨立核對 THSEL。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 TMPTHH，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 TMPTHH 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 THSEL 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** TMPTHH, THSEL, TMPSEL, TMPTH

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3.1, Figure 470, 文件頁 463-464, PDF 頁 489-490

</details>

<details markdown="1">
<summary><strong>Figure 475: Autonomous Power State Transition – Command Dword 11</strong></summary>

<!-- claim:BASEPOWER-FIG-475-CLAIM figure-table:BASEPOWER-FIG-475 -->

**SPEC。** Figure 475〈Autonomous Power State Transition – Command Dword 11〉：定義〈Autonomous Power State Transition – Command Dword 11〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：APSTE。

#### 這張 Figure 在完整流程中的位置

Figure 475 位於 §5.2.30.1.7，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 APSTE 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: APSTE]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `APSTE` | Autonomous Power State Transition Enable，啟用 APST table timer 判斷的 bit。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.1.7。
2. 依圖中指定的寬度與位置解碼 APSTE；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 475 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.1.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30.1.7 如何排列 APSTE、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.1.7 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 475 對應的 raw value 或 buffer，標出包含 APSTE 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 APSTE，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 APSTE 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** APSTE

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, Figure 475, 文件頁 468, PDF 頁 494

</details>

<details markdown="1">
<summary><strong>Figure 476: Autonomous Power State Transition Data Structure</strong></summary>

<!-- claim:BASEPOWER-FIG-476-CLAIM figure-table:BASEPOWER-FIG-476 -->

**SPEC。** Figure 476〈Autonomous Power State Transition Data Structure〉：定義〈Autonomous Power State Transition Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：32 entries, 256 bytes。

#### 這張 Figure 在完整流程中的位置

Figure 476 位於 §5.2.30.1.7，在本流程中是「state」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 32 entries 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 state／timing 圖。沿箭頭記錄 trigger、觀察者、完成條件與 timeout source。相同狀態名稱若位於不同 reset scope，不能推論保留相同 queue 或 controller state。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 32 entries]
          ↓
[擷取欄位: 256 bytes] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `32 entries` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `256 bytes` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.1.7。
2. 依圖中指定的寬度與位置解碼 32 entries；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 256 bytes 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 476 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.1.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30.1.7 如何排列 32 entries、256 bytes 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.1.7 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 476 對應的 raw value 或 buffer，標出包含 32 entries 的 bytes 並解碼，再獨立核對 256 bytes。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 32 entries，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 32 entries 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 256 bytes 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** 32 entries, 256 bytes

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, Figure 476, 文件頁 469, PDF 頁 495

</details>

<details markdown="1">
<summary><strong>Figure 477: Autonomous Power State Transition Entry</strong></summary>

<!-- claim:BASEPOWER-FIG-477-CLAIM figure-table:BASEPOWER-FIG-477 -->

**SPEC。** Figure 477〈Autonomous Power State Transition Entry〉：呈現〈Autonomous Power State Transition Entry〉的狀態或時間推進關係。 依箭頭順序追蹤 state 或 time bound，並標出每個 transition 的觀察者；來源索引：ITPT, ITPS。

#### 這張 Figure 在完整流程中的位置

Figure 477 位於 §5.2.30.1.7，在本流程中是「state」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ITPT 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 state／timing 圖。沿箭頭記錄 trigger、觀察者、完成條件與 timeout source。相同狀態名稱若位於不同 reset scope，不能推論保留相同 queue 或 controller state。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ITPT]
          ↓
[擷取欄位: ITPS] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ITPT` | Idle Time Prior to Transition，APST entry 的 idle threshold，單位為 milliseconds。 |
| `ITPS` | Idle Transition Power State，APST entry 選擇的目標 non-operational power state。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.1.7。
2. 依圖中指定的寬度與位置解碼 ITPT；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 ITPS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 477 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.1.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30.1.7 如何排列 ITPT、ITPS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.1.7 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 477 對應的 raw value 或 buffer，標出包含 ITPT 的 bytes 並解碼，再獨立核對 ITPS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 ITPT，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 ITPT 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 ITPS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ITPT, ITPS

**來源 keyword 索引：** `should not`, `shall`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, Figure 477, 文件頁 469, PDF 頁 495

</details>

<details markdown="1">
<summary><strong>Figure 478: APST and NOPPME Interaction</strong></summary>

<!-- claim:BASEPOWER-FIG-478-CLAIM figure-table:BASEPOWER-FIG-478 -->

**SPEC。** Figure 478〈APST and NOPPME Interaction〉：呈現〈APST and NOPPME Interaction〉所描述的 power／thermal 控制關係。 依序追蹤 selector、state 或 threshold、transition condition 與觀測證據；來源欄位索引：APSTE, NOPPME, host entry, timer entry, background operations。

#### 這張 Figure 在完整流程中的位置

Figure 478 位於 §5.2.30.1.7，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 APSTE 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: APSTE]
          ↓
[擷取欄位: NOPPME] → [套用編碼: host entry]
                                      ↓
[驗證證據: timer entry]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `APSTE` | Autonomous Power State Transition Enable，啟用 APST table timer 判斷的 bit。 |
| `NOPPME` | Non-Operational Power State Permissive Mode Enable，控制 controller background work 能否暫時超過 non-operational power limit。 |
| `host entry` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `timer entry` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `background operations` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.1.7。
2. 依圖中指定的寬度與位置解碼 APSTE；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NOPPME 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 478 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.1.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30.1.7 如何排列 APSTE、NOPPME 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.1.7 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 478 對應的 raw value 或 buffer，標出包含 APSTE 的 bytes 並解碼，再獨立核對 NOPPME。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 APSTE，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 APSTE 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NOPPME 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** APSTE, NOPPME, host entry, timer entry, background operations

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, Figure 478, 文件頁 469, PDF 頁 495

</details>

<details markdown="1">
<summary><strong>Figure 482: Host Controlled Thermal Management – Command Dword 11</strong></summary>

<!-- claim:BASEPOWER-FIG-482-CLAIM figure-table:BASEPOWER-FIG-482 -->

**SPEC。** Figure 482〈Host Controlled Thermal Management – Command Dword 11〉：定義〈Host Controlled Thermal Management – Command Dword 11〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TMT1, TMT2。

#### 這張 Figure 在完整流程中的位置

Figure 482 位於 §5.2.30.1.10，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 TMT1 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TMT1]
          ↓
[擷取欄位: TMT2] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TMT1` | Thermal Management Temperature 1，較輕度 thermal-management threshold，單位 Kelvin。 |
| `TMT2` | Thermal Management Temperature 2，較強 thermal-management threshold，單位 Kelvin。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.1.10。
2. 依圖中指定的寬度與位置解碼 TMT1；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 TMT2 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 482 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.1.10 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30.1.10 如何排列 TMT1、TMT2 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.1.10 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 482 對應的 raw value 或 buffer，標出包含 TMT1 的 bytes 並解碼，再獨立核對 TMT2。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 TMT1，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 TMT1 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 TMT2 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** TMT1, TMT2

**來源 keyword 索引：** `shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, Figure 482, 文件頁 472, PDF 頁 498

</details>

<details markdown="1">
<summary><strong>Figure 483: Non-Operational Power State Configuration – Command Dword 11</strong></summary>

<!-- claim:BASEPOWER-FIG-483-CLAIM figure-table:BASEPOWER-FIG-483 -->

**SPEC。** Figure 483〈Non-Operational Power State Configuration – Command Dword 11〉：定義〈Non-Operational Power State Configuration – Command Dword 11〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NOPPME。

#### 這張 Figure 在完整流程中的位置

Figure 483 位於 §5.2.30.1.11，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NOPPME 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NOPPME]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NOPPME` | Non-Operational Power State Permissive Mode Enable，控制 controller background work 能否暫時超過 non-operational power limit。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.1.11。
2. 依圖中指定的寬度與位置解碼 NOPPME；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 483 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.1.11 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30.1.11 如何排列 NOPPME、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.1.11 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 483 對應的 raw value 或 buffer，標出包含 NOPPME 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NOPPME，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NOPPME 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NOPPME

**來源 keyword 索引：** `shall not`, `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.11, Figure 483, 文件頁 472-473, PDF 頁 498-499

</details>

<a id="section-8-1"></a>

### §8.1

<details markdown="1">
<summary><strong>Figure 738: Power Management Overview</strong></summary>

<!-- claim:BASEPOWER-FIG-738-CLAIM figure-table:BASEPOWER-FIG-738 -->

**SPEC。** Figure 738〈Power Management Overview〉：呈現〈Power Management Overview〉所描述的 power／thermal 控制關係。 依序追蹤 selector、state 或 threshold、transition condition 與觀測證據；來源欄位索引：Static Power Management, Dynamic Power Management, Power State Descriptor。

#### 這張 Figure 在完整流程中的位置

Figure 738 位於 §8.1.19，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Static Power Management 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Static Power Management]
          ↓
[擷取欄位: Dynamic Power Management] → [套用編碼: Power State Descriptor]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Static Power Management` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Dynamic Power Management` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Power State Descriptor` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §8.1.19。
2. 依圖中指定的寬度與位置解碼 Static Power Management；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Dynamic Power Management 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 738 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.19 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §8.1.19 如何排列 Static Power Management、Dynamic Power Management 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §8.1.19 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 738 對應的 raw value 或 buffer，標出包含 Static Power Management 的 bytes 並解碼，再獨立核對 Dynamic Power Management。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Static Power Management，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Static Power Management 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Dynamic Power Management 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Static Power Management, Dynamic Power Management, Power State Descriptor

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19, Figure 738, 文件頁 666, PDF 頁 692

</details>

<details markdown="1">
<summary><strong>Figure 739: Power State Characteristics</strong></summary>

<!-- claim:BASEPOWER-FIG-739-CLAIM figure-table:BASEPOWER-FIG-739 -->

**SPEC。** Figure 739〈Power State Characteristics〉：呈現〈Power State Characteristics〉的狀態或時間推進關係。 依箭頭順序追蹤 state 或 time bound，並標出每個 transition 的觀察者；來源索引：MP, IDLP, ACTP, ENLAT, EXLAT。

#### 這張 Figure 在完整流程中的位置

Figure 739 位於 §8.1.19，在本流程中是「state」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 MP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 state／timing 圖。沿箭頭記錄 trigger、觀察者、完成條件與 timeout source。相同狀態名稱若位於不同 reset scope，不能推論保留相同 queue 或 controller state。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MP]
          ↓
[擷取欄位: IDLP] → [套用編碼: ACTP]
                                      ↓
[驗證證據: ENLAT]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MP` | Maximum Power，一個 power state 的 sustained maximum power。 |
| `IDLP` | Idle Power，依規格 idle 測量條件描述的 typical power。 |
| `ACTP` | Active Power，在指定 workload 與時間窗下描述的 average active power。 |
| `ENLAT` | Entry Latency，進入該 power state 的 maximum latency，單位為 microseconds。 |
| `EXLAT` | Exit Latency，離開該 power state 的 maximum latency，單位為 microseconds。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §8.1.19。
2. 依圖中指定的寬度與位置解碼 MP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 IDLP 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 739 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.19 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §8.1.19 如何排列 MP、IDLP 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §8.1.19 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 739 對應的 raw value 或 buffer，標出包含 MP 的 bytes 並解碼，再獨立核對 IDLP。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 MP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 MP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 IDLP 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** MP, IDLP, ACTP, ENLAT, EXLAT

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19, Figure 739, 文件頁 667, PDF 頁 693

</details>

<details markdown="1">
<summary><strong>Figure 740: Workload Hints</strong></summary>

<!-- claim:BASEPOWER-FIG-740-CLAIM figure-table:BASEPOWER-FIG-740 -->

**SPEC。** Figure 740〈Workload Hints〉：呈現〈Workload Hints〉所描述的 power／thermal 控制關係。 依序追蹤 selector、state 或 threshold、transition condition 與觀測證據；來源欄位索引：WH 000b, WH 001b, WH 010b。

#### 這張 Figure 在完整流程中的位置

Figure 740 位於 §8.1.19.3，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 WH 000b 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: WH 000b]
          ↓
[擷取欄位: WH 001b] → [套用編碼: WH 010b]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `WH 000b` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `WH 001b` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `WH 010b` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §8.1.19.3。
2. 依圖中指定的寬度與位置解碼 WH 000b；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 WH 001b 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 740 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.19.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §8.1.19.3 如何排列 WH 000b、WH 001b 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §8.1.19.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 740 對應的 raw value 或 buffer，標出包含 WH 000b 的 bytes 並解碼，再獨立核對 WH 001b。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 WH 000b，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 WH 000b 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 WH 001b 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** WH 000b, WH 001b, WH 010b

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19.3, Figure 740, 文件頁 669, PDF 頁 695

</details>

<details markdown="1">
<summary><strong>Figure 741: Host Controlled Thermal Management</strong></summary>

<!-- claim:BASEPOWER-FIG-741-CLAIM figure-table:BASEPOWER-FIG-741 -->

**SPEC。** Figure 741〈Host Controlled Thermal Management〉：呈現〈Host Controlled Thermal Management〉所描述的 power／thermal 控制關係。 依序追蹤 selector、state 或 threshold、transition condition 與觀測證據；來源欄位索引：TMT1, TMT2, hysteresis, thermal throttling。

#### 這張 Figure 在完整流程中的位置

Figure 741 位於 §8.1.19.5，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 TMT1 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TMT1]
          ↓
[擷取欄位: TMT2] → [套用編碼: hysteresis]
                                      ↓
[驗證證據: thermal throttling]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TMT1` | Thermal Management Temperature 1，較輕度 thermal-management threshold，單位 Kelvin。 |
| `TMT2` | Thermal Management Temperature 2，較強 thermal-management threshold，單位 Kelvin。 |
| `hysteresis` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `thermal throttling` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §8.1.19.5。
2. 依圖中指定的寬度與位置解碼 TMT1；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 TMT2 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 741 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.19.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §8.1.19.5 如何排列 TMT1、TMT2 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §8.1.19.5 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 741 對應的 raw value 或 buffer，標出包含 TMT1 的 bytes 並解碼，再獨立核對 TMT2。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 TMT1，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 TMT1 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 TMT2 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** TMT1, TMT2, hysteresis, thermal throttling

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19.5, Figure 741, 文件頁 671, PDF 頁 697

</details>

<a id="section-dependency"></a>

### 引用相依 Figure（位於主章節範圍外）

<details markdown="1">
<summary><strong>Figure 93: Common Command Format</strong></summary>

<!-- claim:BASEPOWER-FIG-093-CLAIM figure-table:BASEPOWER-FIG-093 -->

**SPEC。** Figure 93〈Common Command Format〉：定義〈Common Command Format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：OPC, CID, NSID, MPTR, DPTR, CDW10-CDW15。

#### 這張 Figure 在完整流程中的位置

Figure 93 位於 §4.1.1，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 OPC 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: OPC]
          ↓
[擷取欄位: CID] → [套用編碼: NSID]
                                      ↓
[驗證證據: MPTR]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `OPC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CID` | Command Identifier，與 SQ identifier 合用以辨識 outstanding command。 |
| `NSID` | Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。 |
| `MPTR` | Metadata Pointer，SQE 中指出獨立 metadata buffer 的欄位。 |
| `DPTR` | Data Pointer，SQE 中指出 command data buffer 的欄位。 |
| `CDW10-CDW15` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.1.1。
2. 依圖中指定的寬度與位置解碼 OPC；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
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
| 這張圖回答 | §4.1.1 如何排列 OPC、CID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.1.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 93 對應的 raw value 或 buffer，標出包含 OPC 的 bytes 並解碼，再獨立核對 CID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 OPC，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 OPC 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** OPC, CID, NSID, MPTR, DPTR, CDW10-CDW15

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, 文件頁 140-142, PDF 頁 166-168

</details>

<details markdown="1">
<summary><strong>Figure 213: SMART / Health Information Log</strong></summary>

<!-- claim:BASEPOWER-FIG-213-CLAIM figure-table:BASEPOWER-FIG-213 -->

**SPEC。** Figure 213〈SMART / Health Information Log〉：定義〈SMART / Health Information Log〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Composite Temperature, TTC, Temperature Sensor, HCTM counters。

#### 這張 Figure 在完整流程中的位置

Figure 213 位於 §5.2.13.1.3，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Composite Temperature 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Composite Temperature]
          ↓
[擷取欄位: TTC] → [套用編碼: Temperature Sensor]
                                      ↓
[驗證證據: HCTM counters]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Composite Temperature` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `TTC` | Temperature Threshold Critical Warning，SMART／Health Critical Warning 中的溫度 threshold bit。 |
| `Temperature Sensor` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `HCTM counters` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.13.1.3。
2. 依圖中指定的寬度與位置解碼 Composite Temperature；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 TTC 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 213 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13.1.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.13.1.3 如何排列 Composite Temperature、TTC 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.13.1.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 213 對應的 raw value 或 buffer，標出包含 Composite Temperature 的 bytes 並解碼，再獨立核對 TTC。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Composite Temperature，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Composite Temperature 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 TTC 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Composite Temperature, TTC, Temperature Sensor, HCTM counters

**來源 keyword 索引：** `shall not`, `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, Figure 213, 文件頁 220-225, PDF 頁 246-251

</details>

<details markdown="1">
<summary><strong>Figure 338: Identify Controller Data Structure</strong></summary>

<!-- claim:BASEPOWER-FIG-338-CLAIM figure-table:BASEPOWER-FIG-338 -->

**SPEC。** Figure 338〈Identify Controller Data Structure〉：定義〈Identify Controller Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NPSS, APSTA, HCTMA, WCTEMP, MNTMT, MXTMT, RTD3E, RTD3R。

#### 這張 Figure 在完整流程中的位置

Figure 338 位於 §5.2.14.2.1，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NPSS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NPSS]
          ↓
[擷取欄位: APSTA] → [套用編碼: HCTMA]
                                      ↓
[驗證證據: WCTEMP]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NPSS` | Number of Power States Support，以 0's-based 方式回報最高支援 power-state number。 |
| `APSTA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `HCTMA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `WCTEMP` | Warning Composite Temperature Threshold，Identify Controller 回報的 composite warning threshold。 |
| `MNTMT` | Minimum Thermal Management Temperature，HCTM 可設定的最低 Kelvin 值。 |
| `MXTMT` | Maximum Thermal Management Temperature，HCTM 可設定的最高 Kelvin 值。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.14.2.1。
2. 依圖中指定的寬度與位置解碼 NPSS；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 APSTA 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 338 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.14.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.14.2.1 如何排列 NPSS、APSTA 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.14.2.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 338 對應的 raw value 或 buffer，標出包含 NPSS 的 bytes 並解碼，再獨立核對 APSTA。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NPSS，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NPSS 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 APSTA 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NPSS, APSTA, HCTMA, WCTEMP, MNTMT, MXTMT, RTD3E, RTD3R

**來源 keyword 索引：** `shall not`, `should not`, `shall`, `should`, `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, 文件頁 340-364, PDF 頁 366-390

</details>

<details markdown="1">
<summary><strong>Figure 340: Power State Descriptor Data Structure</strong></summary>

<!-- claim:BASEPOWER-FIG-340-CLAIM figure-table:BASEPOWER-FIG-340 -->

**SPEC。** Figure 340〈Power State Descriptor Data Structure〉：定義〈Power State Descriptor Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MP, NOPS, ENLAT, EXLAT, IDLP, ACTP, RRT/RRL, RWT/RWL。

#### 這張 Figure 在完整流程中的位置

Figure 340 位於 §5.2.14.2.2，在本流程中是「state」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 MP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 state／timing 圖。沿箭頭記錄 trigger、觀察者、完成條件與 timeout source。相同狀態名稱若位於不同 reset scope，不能推論保留相同 queue 或 controller state。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MP]
          ↓
[擷取欄位: NOPS] → [套用編碼: ENLAT]
                                      ↓
[驗證證據: EXLAT]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MP` | Maximum Power，一個 power state 的 sustained maximum power。 |
| `NOPS` | Non-Operational State，Power State Descriptor 中指出該 state 不處理 I/O commands 的 bit。 |
| `ENLAT` | Entry Latency，進入該 power state 的 maximum latency，單位為 microseconds。 |
| `EXLAT` | Exit Latency，離開該 power state 的 maximum latency，單位為 microseconds。 |
| `IDLP` | Idle Power，依規格 idle 測量條件描述的 typical power。 |
| `ACTP` | Active Power，在指定 workload 與時間窗下描述的 average active power。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.14.2.2。
2. 依圖中指定的寬度與位置解碼 MP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NOPS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 340 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.14.2.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.14.2.2 如何排列 MP、NOPS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.14.2.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 340 對應的 raw value 或 buffer，標出包含 MP 的 bytes 並解碼，再獨立核對 NOPS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 MP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 MP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NOPS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** MP, NOPS, ENLAT, EXLAT, IDLP, ACTP, RRT/RRL, RWT/RWL

**來源 keyword 索引：** `shall not`, `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.2, Figure 340, 文件頁 383-386, PDF 頁 409-412

</details>

<details markdown="1">
<summary><strong>Figure 474: Asynchronous Event Configuration – Command Dword 11</strong></summary>

<!-- claim:BASEPOWER-FIG-474-CLAIM figure-table:BASEPOWER-FIG-474 -->

**SPEC。** Figure 474〈Asynchronous Event Configuration – Command Dword 11〉：定義〈Asynchronous Event Configuration – Command Dword 11〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TTHRY, SHCW。

#### 這張 Figure 在完整流程中的位置

Figure 474 位於 §5.2.30.1.6，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 TTHRY 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TTHRY]
          ↓
[擷取欄位: SHCW] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TTHRY` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SHCW` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.1.6。
2. 依圖中指定的寬度與位置解碼 TTHRY；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 SHCW 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 474 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.1.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30.1.6 如何排列 TTHRY、SHCW 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.1.6 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 474 對應的 raw value 或 buffer，標出包含 TTHRY 的 bytes 並解碼，再獨立核對 SHCW。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 TTHRY，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 TTHRY 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 SHCW 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** TTHRY, SHCW

**來源 keyword 索引：** `shall not`, `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.6, Figure 474, 文件頁 466-468, PDF 頁 492-494

</details>

## 使用與限制

製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata 集合或核准範圍改變時，必須重新核對受影響 claim。
