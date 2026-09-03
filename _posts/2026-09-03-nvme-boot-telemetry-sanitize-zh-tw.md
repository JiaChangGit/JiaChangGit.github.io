---
permalink: /nvme/boot-telemetry-sanitize-zh-tw/
layout: post
read_time: true
show_date: true
title: "NVMe 2.4：Boot Partitions、Telemetry 與 Sanitize 完整教學"
date: 2026-09-03
description: "供 GitHub Pages 與 PPT 使用的 NVMe 規格導讀。"
lang: zh-Hant-TW
img: posts/2026/dogMC_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---
[English]({% post_url 2026-09-03-nvme-boot-telemetry-sanitize-en %})


# NVMe 2.4：Boot Partitions、Telemetry 與 Sanitize 完整教學

用途：供 GitHub Pages 閱讀與 100 分鐘簡報製作；讀者已具備 PCIe 與 NVMe 基礎。

範圍：Base §§8.1.3、8.1.30、8.1.27（排除 8.1.27.6）、5.2.26；LID 15h/07h/08h/81h；FID 85h/17h；NVM §§4.1.7、5.12，以及被引用的必要圖表。正文只保留 PCIe／memory-based 與通用 NVMe 內容。

## 來源版本

NVM Express Base Specification, Revision 2.4
NVM Express NVM Command Set Specification, Revision 1.3

查證日期：2026-09-03。目前未納入其他 Errata、ECN、Technical Proposal、controller vendor 文件或未提供的 PCI Express Base Specification 原文。

## 閱讀地圖

```text
Discover capability -> Read / capture / sanitize -> Track state and evidence -> Verify outcome
```

Boot、Telemetry、Sanitize 分別管理開機映像、診斷快照與 user-data sanitization；它們共享能力、命令與證據的閱讀方法，卻有不同的 scope 與完成條件。

## 規範性用語

shall 譯為「必須」，may 譯為「可／得」，should 譯為「宜／建議」，optional 譯為「選用」。本文不提高或降低原文語氣。

## 先學縮寫：完整 Glossary

下列縮寫會在投影片主線使用前先定義。縮寫本身永遠不夠；設計與 Debug 還要保留 owner、width、unit、scope 與 state。

| 縮寫／名詞 | 白話解釋 | 來源 |
|---|---|---|
| `BPID` | Boot Partition Identifier；選取 0 或 1，與目前 active partition 分開。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.21，文件頁 283-284，PDF 頁 309-310 |
| `BRS` | Boot Read Status；00b 未請求、01b 進行中、10b 成功、11b 錯誤。 | NVME-BASE-2.4 Rev. 2.4，§8.1.3.1，文件頁 586-587，PDF 頁 612-613 |
| `BPCAP` | Boot Partition Capabilities；辨識 Set Features 與 RPMB 保護機制的支援組合。 | NVME-BASE-2.4 Rev. 2.4，§8.1.3.3，文件頁 588-589，PDF 頁 614-615 |
| `BP0WPS` | Boot Partition 0 Write Protection State；FID 85h 的 bits 2:0。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.39，文件頁 513-514，PDF 頁 539-540 |
| `CTHID` | Create Telemetry Host-Initiated Data；07h 的 capture 要求，後續分段讀同一快照要清為 0。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.8，文件頁 232-235，PDF 頁 258-261 |
| `MCDA` | Maximum Created Data Area；支援且要求 capture 時選擇建立的最大 area。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.8，文件頁 232-235，PDF 頁 258-261 |
| `MCDAS` | Maximum Created Data Area Supported；07h 的 LID Specific Parameter bit 0，宣告 MCDA 支援。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.8，文件頁 232-235，PDF 頁 258-261 |
| `ETDAS` | Extended Telemetry Data Area 4 Supported；Host Behavior Support 中由 host 宣告 Area 4 支援。 | NVME-BASE-2.4 Rev. 2.4，§8.1.30; 5.2.30.1.15，文件頁 476,733-734，PDF 頁 502,759-760 |
| `TCDA` | Telemetry Controller-Initiated Data Available；2.4 中表示自上次 RAE=0 acknowledgement 後是否有更新。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.9，文件頁 237，PDF 頁 263 |
| `TCDGN` | Telemetry Controller-Initiated Data Generation Number；8-bit generation，完成更新最後才遞增。 | NVME-BASE-2.4 Rev. 2.4，§8.1.30，文件頁 734-735，PDF 頁 760-761 |
| `RAE` | Retain Asynchronous Event；Telemetry 收集中用 1 保留通知狀態，完成後用 0 acknowledgement。 | NVME-BASE-2.4 Rev. 2.4，§8.1.30，文件頁 734-735，PDF 頁 760-761 |
| `SANACT` | Sanitize Action；決定實際方法、退出 Failure 或退出 Media Verification。 | NVME-BASE-2.4 Rev. 2.4，§5.2.26，文件頁 448-451，PDF 頁 474-477 |
| `AUSE` | Allow Unrestricted Sanitize Exit；選擇失敗時是否允許不經成功重試就退出 Failure。 | NVME-BASE-2.4 Rev. 2.4，§8.1.27.4，文件頁 719-730，PDF 頁 745-756 |
| `NDAS` | No-Deallocate After Sanitize；命令要求，需與 SANICAP.NDI 及 NODRM 一起解讀。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.16; 8.1.27.2-8.1.27.3，文件頁 477-478,715-719，PDF 頁 503-504,741-745 |
| `NODRM` | No-Deallocate Response Mode；FID 17h bit 0，選擇受抑制 NDAS 的 error 或 warning 回應。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.16; 8.1.27.2-8.1.27.3，文件頁 477-478,715-719，PDF 頁 503-504,741-745 |
| `EMVS` | Enter Media Verification State；成功 processing 後要求進入驗證，受方法與 capability 限制。 | NVME-BASE-2.4 Rev. 2.4，§5.2.26，文件頁 449，PDF 頁 475 |
| `PREQ` | Purge Request；與 SPRRS 一起判定 purge 要求與回報；兩種 Sanitize 命令的 bit 位置不同。 | NVME-BASE-2.4 Rev. 2.4，§8.1.27.2-8.1.27.3，文件頁 714-717，PDF 頁 740-743 |
| `SPROG` | Sanitize Progress；raw/65536，僅表示目前量測階段的進度。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.38; 8.1.27.3，文件頁 314-319,718，PDF 頁 340-345,744 |
| `SOS` | Sanitize Operation Status；SSTAT bits 2:0，與目前 SANS state 分開判讀。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.38，文件頁 313-319，PDF 頁 339-345 |
| `MVCNCLD` | Media Verification Canceled；記錄要求的驗證被取消，會影響 processing 後的轉移。 | NVME-BASE-2.4 Rev. 2.4，§8.1.27.4.6-8.1.27.4.7，文件頁 727-730，PDF 頁 753-756 |
| `PRCHK` | Protection Information Check；三個 bits 分別要求 guard、application tag、reference tag 檢查；驗證讀取設 000b。 | NVME-NVM-CS-1.3 Rev. 1.3，§5.12.1，文件頁 174-175，PDF 頁 174-175 |
| `STC` | Storage Tag Check；本報告指 NVM Read 的 storage tag 檢查，驗證讀取設 0。 | NVME-NVM-CS-1.3 Rev. 1.3，§5.12.1，文件頁 174-175，PDF 頁 174-175 |

## Visual Atlas：先用圖建立整體位置

每張教學重畫回答不同問題：Architecture 定位元件、Sequence 顯示 ownership、Decode 把 bits 轉成工程值、State 保留 failure evidence；它們不是 Spec 原圖的複製。

### Visual 01: Boot 的兩條讀取路徑

**View type:** `sequence`

```text
1. CAP.BPS
2. BPINFO active/size
3. BPMBL buffer
4. BPRSEL request
5. BRS result
```

**回答的問題：** 先問 controller 是否已建立 Admin command 環境，再選 property 或 LID 15h。兩條路徑讀同一類 Boot 內容，但回傳格式與狀態觀察點不同。

**支援 Figure：** Figure 36, Figure 49, Figure 50, Figure 51, Figure 279, Figure 280, Figure 679

**來源：** NVME-BASE-2.4 Rev. 2.4，§8.1.3，文件頁 586，PDF 頁 612; NVME-BASE-2.4 Rev. 2.4，§8.1.3.1，文件頁 586-587，PDF 頁 612-613; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.21，文件頁 283-284，PDF 頁 309-310

### Visual 02: 更新與保護的完整生命週期

**View type:** `sequence`

```text
1. Download in order
2. Unlock target
3. Commit CA=110b
4. Read/verify; CA=111b
5. Relock
```

**回答的問題：** 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。

**支援 Figure：** Figure 187, Figure 542, Figure 680, Figure 681, Figure 682, Figure 683, Figure 684, Figure 756, Figure 765, Figure 766

**來源：** NVME-BASE-2.4 Rev. 2.4，§8.1.3.2，文件頁 587-588，PDF 頁 613-614; NVME-BASE-2.4 Rev. 2.4，§8.1.3.2，文件頁 588，PDF 頁 614; NVME-BASE-2.4 Rev. 2.4，§8.1.3.3，文件頁 588-589，PDF 頁 614-615; NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.39，文件頁 513-514，PDF 頁 539-540; NVME-BASE-2.4 Rev. 2.4，§8.1.3.3.1-8.1.3.3.3，文件頁 589-594，PDF 頁 615-620; NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.39; 8.1.3.3.3，文件頁 513-514,593-594，PDF 頁 539-540,619-620

### Visual 03: 從 Last Block 計算快照

**View type:** `decode`

```text
1. Read 512-byte header
2. Check DA4S/ETDAS
3. Decode last blocks
4. Compute inclusive extent
5. Read aligned blocks
```

**回答的問題：** Area 是從同一 block 1 起算的不同大小視圖。先解碼 header，再選擇適用且有資料的最後 area；不要把三個 Last Block 數字相加。

**支援 Figure：** Figure 221, Figure 223, Figure 338, Figure 491, Figure 780, Figure 781

**來源：** NVME-BASE-2.4 Rev. 2.4，§8.1.30; 5.2.13.1.8-5.2.13.1.9，文件頁 232-237,733-737，PDF 頁 258-263,759-763; NVME-BASE-2.4 Rev. 2.4，§8.1.30; 5.2.30.1.15，文件頁 476,733-734，PDF 頁 502,759-760; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.8-5.2.13.1.9，文件頁 232-237，PDF 頁 258-263

### Visual 04: 建立、讀取、確認一致、acknowledge

**View type:** `sequence`

```text
1. Capability / event setup
2. Capture or observe update
3. RAE=1 chunk reads
4. Recheck generation/TCDA
5. 08h RAE=0 acknowledgement
```

**回答的問題：** 07h 的 create 與後續讀取分開；08h 的 capture 由 controller 決定。Host 對兩者都要驗證 generation，並分清事件 acknowledgement 與刪除 payload。

**支援 Figure：** Figure 204, Figure 210, Figure 211, Figure 220, Figure 222, Figure 151, Figure 152, Figure 155, Figure 474

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.8，文件頁 232-235，PDF 頁 258-261; NVME-BASE-2.4 Rev. 2.4，§8.1.30，文件頁 734-735，PDF 頁 760-761; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.9，文件頁 237，PDF 頁 263; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.8-5.2.13.1.9，文件頁 233,235,237，PDF 頁 259,261,263; NVME-BASE-2.4 Rev. 2.4，§8.1.30; 5.2.30.1.6，文件頁 734-735,466-468，PDF 頁 760-761,492-494

### Visual 05: 先定義被清理的 target

**View type:** `architecture`

```text
1. Select target
2. Enumerate user-data locations
3. Check method/support
4. Apply purge requirement
5. Audit permitted evidence
```

**回答的問題：** Sanitize scope 不是『磁碟上所有東西』。以 target、資料來源、是否可能含 user data 判斷；Boot 與診斷機制的交叉關係也從這個範圍開始。

**支援 Figure：** Figure 770, Figure 771, Figure 200, Figure 201

**來源：** NVME-BASE-2.4 Rev. 2.4，§8.1.27，文件頁 711-712，PDF 頁 737-738; NVME-BASE-2.4 Rev. 2.4，§8.1.27，文件頁 711-712，PDF 頁 737-738; NVME-BASE-2.4 Rev. 2.4，§8.1.27.2-8.1.27.3，文件頁 714-717，PDF 頁 740-743; NVME-NVM-CS-1.3 Rev. 1.3，§5.12，文件頁 174，PDF 頁 174

### Visual 06: 命令參數與 capability 組合

**View type:** `decode`

```text
1. SANICAP / target
2. SANACT and modifiers
3. FID 17h policy
4. Preflight and CQE
5. LID 81h operation result
```

**回答的問題：** 先把支援能力、命令要求與 Feature policy 分開。命令接受、operation 成功、符合 no-deallocate 要求是三個需要不同證據的結果。

**支援 Figure：** Figure 338, Figure 451, Figure 452, Figure 453, Figure 454, Figure 492

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.26，文件頁 448-451，PDF 頁 474-477; NVME-BASE-2.4 Rev. 2.4，§8.1.27.1; 5.2.27，文件頁 713,453，PDF 頁 739,479; NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.16; 8.1.27.2-8.1.27.3，文件頁 477-478,715-719，PDF 頁 503-504,741-745; NVME-BASE-2.4 Rev. 2.4，§5.2.26，文件頁 449，PDF 頁 475; NVME-BASE-2.4 Rev. 2.4，§5.2.26; 8.1.27.1，文件頁 449-451,712-714，PDF 頁 475-477,738-740; NVME-BASE-2.4 Rev. 2.4，§5.2.26; 8.1.27.3，文件頁 451,717，PDF 頁 477,743

### Visual 07: 用 state、log、AER 重建背景作業

**View type:** `state`

```text
Idle | A1: AUSE=0 | Restricted Processing
Idle | B1: AUSE=1 | Unrestricted Processing
Restricted Processing | C1: success; no verification | Idle
Restricted Processing | D1: processing fails | Restricted Failure
Restricted Processing | F1: success; EMVS=1; not canceled | Media Verification
Restricted Failure | A2: restricted retry | Restricted Processing
Unrestricted Processing | C2: success; no verification | Idle
Unrestricted Processing | D2: processing fails | Unrestricted Failure
Unrestricted Processing | F2: success; EMVS=1; not canceled | Media Verification
Unrestricted Failure | A3: restricted retry | Restricted Processing
Unrestricted Failure | B2: unrestricted retry | Unrestricted Processing
Unrestricted Failure | E: Exit Failure Mode | Idle
Media Verification | G: exit / applicable reset / cancellation | Post-Verification Deallocation
Post-Verification Deallocation | H: deallocation succeeds | Idle
Post-Verification Deallocation | I1: failure; original AUSE=0 | Restricted Failure
Post-Verification Deallocation | I2: failure; original AUSE=1 | Unrestricted Failure
```

**回答的問題：** 從 Figure 772 的七個 states 出發，逐一把 Figures 773–779 的 transition condition 接上。Status 描述結果，state 描述目前位置，事件描述發生的轉折。

**支援 Figure：** Figure 312, Figure 151, Figure 152, Figure 156, Figure 772, Figure 773, Figure 774, Figure 775, Figure 776, Figure 777, Figure 778, Figure 779

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.26.1; 8.1.27.1，文件頁 451,712-713，PDF 頁 477,738-739; NVME-BASE-2.4 Rev. 2.4，§8.1.27.4，文件頁 719-730，PDF 頁 745-756; NVME-BASE-2.4 Rev. 2.4，§8.1.27.4.6-8.1.27.4.7，文件頁 727-730，PDF 頁 753-756; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.38，文件頁 313-319，PDF 頁 339-345; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.38; 8.1.27.3，文件頁 314-319,718，PDF 頁 340-345,744; NVME-BASE-2.4 Rev. 2.4，§8.1.27.1; 8.1.27.4，文件頁 712-713,720，PDF 頁 738-739,746

### Visual 08: 操作限制與驗證讀取

**View type:** `state`

```text
1. Target/state
2. Admin/I/O permission
3. PRCHK=000b and STC=0
4. Allocated media readable?
5. Data + specific status
```

**回答的問題：** 把 command allowlist 與 NVM Read 特例分開判斷。Host 先辨識 target/state，再確認 PI checking 與 allocation，不能把平常 read 的處理完全套入驗證狀態。

**支援 Figure：** Figure 11, Figure 12, Figure 144, Figure 145, Figure 146, Figure 200, Figure 201, Figure 311

**來源：** NVME-BASE-2.4 Rev. 2.4，§8.1.27.5; 5.1.1-5.1.2，文件頁 178-181,730-732，PDF 頁 204-207,756-758; NVME-BASE-2.4 Rev. 2.4，§8.1.27.5，文件頁 730-732，PDF 頁 756-758; NVME-NVM-CS-1.3 Rev. 1.3，§4.1.7; 5.12，文件頁 113,173-175，PDF 頁 113,173-175; NVME-NVM-CS-1.3 Rev. 1.3，§5.12，文件頁 174，PDF 頁 174; NVME-NVM-CS-1.3 Rev. 1.3，§5.12.1，文件頁 174-175，PDF 頁 174-175; NVME-BASE-2.4 Rev. 2.4，§8.1.3.1; 8.1.27.4.2，文件頁 587,721，PDF 頁 613,747

## Mental Model 與完整教學流程

以下依工程因果而非 Spec section 排列；相關 Figure 會回到它支援的流程節點，不以編號順序取代教學故事線。

### Module 01: Boot 的兩條讀取路徑

**解釋。** 先問 controller 是否已建立 Admin command 環境，再選 property 或 LID 15h。兩條路徑讀同一類 Boot 內容，但回傳格式與狀態觀察點不同。

```text
CAP.BPS
  ↓
BPINFO active/size
  ↓
BPMBL buffer
  ↓
BPRSEL request
  ↓
BRS result
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Properties | BRS 回報讀取狀態 | 不要求 CC.EN=1 |
| LID 15h | 16-byte header + data | 由 Admin command CQE 判斷命令結果 |
| BPID | 選取讀取 partition | 不等於 active ID |
| BPSZ | 每單位 128 KiB | 不是 bytes |

**說明性範例。** BPSZ=2 的 LID 15h 包含 262144 bytes 的 Boot data，加上 16-byte header，共 262160 bytes。讀 BP1 並不把 BP1 設為 active；讀 log 也不會推進 property 的 BRS。

**常見誤解／Debug。** 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§8.1.3，文件頁 586，PDF 頁 612; NVME-BASE-2.4 Rev. 2.4，§8.1.3.1，文件頁 586-587，PDF 頁 612-613; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.21，文件頁 283-284，PDF 頁 309-310

**關聯 Figure：** Figure 36, Figure 49, Figure 50, Figure 51, Figure 279, Figure 280, Figure 679

### Module 02: 更新與保護的完整生命週期

**解釋。** 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。

```text
Download in order
  ↓
Unlock target
  ↓
Commit CA=110b
  ↓
Read/verify; CA=111b
  ↓
Relock
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| FID 85h unlocked | Controller reset 後保留 | Power cycle 後 locked |
| FID 85h until power cycle | 一般 Set 不可解鎖 | 共享 multi-domain partition 不可用 |
| RPMB enabled/unlocked | Controller reset 即 relock | 啟用保護不可撤回 |
| 兩套機制 | 同時只有一套控制 | RPMB enable 是控制權轉移 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解／Debug。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§8.1.3.2，文件頁 587-588，PDF 頁 613-614; NVME-BASE-2.4 Rev. 2.4，§8.1.3.2，文件頁 588，PDF 頁 614; NVME-BASE-2.4 Rev. 2.4，§8.1.3.3，文件頁 588-589，PDF 頁 614-615; NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.39，文件頁 513-514，PDF 頁 539-540; NVME-BASE-2.4 Rev. 2.4，§8.1.3.3.1-8.1.3.3.3，文件頁 589-594，PDF 頁 615-620; NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.39; 8.1.3.3.3，文件頁 513-514,593-594，PDF 頁 539-540,619-620

**關聯 Figure：** Figure 187, Figure 542, Figure 680, Figure 681, Figure 682, Figure 683, Figure 684, Figure 756, Figure 765, Figure 766

### Module 03: 從 Last Block 計算快照

**解釋。** Area 是從同一 block 1 起算的不同大小視圖。先解碼 header，再選擇適用且有資料的最後 area；不要把三個 Last Block 數字相加。

```text
Read 512-byte header
  ↓
Check DA4S/ETDAS
  ↓
Decode last blocks
  ↓
Compute inclusive extent
  ↓
Read aligned blocks
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Area 1 | 1 到 L1 | L1=0 表示沒有資料 |
| Area 2 | 1 到 L2 | L2 >= L1 |
| Area 3 | 1 到 L3 | L3 >= L2 |
| Area 4 | 1 到 L4 | 支援條件另行檢查 |

**說明性範例。** Last Blocks=65/1000/30000 時，Area 3 payload 為 30000×512=15360000 bytes；包含 header 的 log 為 15360512 bytes。0/1000/1000 則表示 Area 1 空、Area 3 沒有超出 Area 2 的新增內容。

**常見誤解／Debug。** LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§8.1.30; 5.2.13.1.8-5.2.13.1.9，文件頁 232-237,733-737，PDF 頁 258-263,759-763; NVME-BASE-2.4 Rev. 2.4，§8.1.30; 5.2.30.1.15，文件頁 476,733-734，PDF 頁 502,759-760; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.8-5.2.13.1.9，文件頁 232-237，PDF 頁 258-263

**關聯 Figure：** Figure 221, Figure 223, Figure 338, Figure 491, Figure 780, Figure 781

### Module 04: 建立、讀取、確認一致、acknowledge

**解釋。** 07h 的 create 與後續讀取分開；08h 的 capture 由 controller 決定。Host 對兩者都要驗證 generation，並分清事件 acknowledgement 與刪除 payload。

```text
Capability / event setup
  ↓
Capture or observe update
  ↓
RAE=1 chunk reads
  ↓
Recheck generation/TCDA
  ↓
08h RAE=0 acknowledgement
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| CTHID=1 | 觸發新 07h capture | 後續分段讀不要再次 create |
| MCDA | 限制建立到哪個 area | 先看 MCDAS |
| RAE=1 | 保留事件 | 不保證沒有其他 reader |
| TCDA=0 | 上次 acknowledgement 後未更新 | 2.4 不等於 payload 消失 |

**說明性範例。** 讀取前 generation=2Ah，讀完變成 2Bh，這批 blocks 不能當成同一 capture 的一致資料。若值保持 2Ah 但 TCDA 被其他 host 清成 0，08h 收集仍需依流程檢查該競態。

**常見誤解／Debug。** 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.8，文件頁 232-235，PDF 頁 258-261; NVME-BASE-2.4 Rev. 2.4，§8.1.30，文件頁 734-735，PDF 頁 760-761; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.9，文件頁 237，PDF 頁 263; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.8-5.2.13.1.9，文件頁 233,235,237，PDF 頁 259,261,263; NVME-BASE-2.4 Rev. 2.4，§8.1.30; 5.2.30.1.6，文件頁 734-735,466-468，PDF 頁 760-761,492-494

**關聯 Figure：** Figure 204, Figure 210, Figure 211, Figure 220, Figure 222, Figure 151, Figure 152, Figure 155, Figure 474

### Module 05: 先定義被清理的 target

**解釋。** Sanitize scope 不是『磁碟上所有東西』。以 target、資料來源、是否可能含 user data 判斷；Boot 與診斷機制的交叉關係也從這個範圍開始。

```text
Select target
  ↓
Enumerate user-data locations
  ↓
Check method/support
  ↓
Apply purge requirement
  ↓
Audit permitted evidence
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Boot/RPMB | 不受 sanitize 影響 | 另由自身管理機制控制 |
| Logs/features | 必要時修改 user data | 不能只檢查 namespace media |
| All namespace sanitizes | 只完成各 target 的工作 | 不能因此宣告 subsystem GDE |
| Crypto Erase | 改 key 並處理未加密資料 | 舊 key 副本也是重要條件 |

**說明性範例。** 即使所有 namespaces 都已 sanitize，CMB 等 subsystem 層級資料仍不能由這個事實證明已完成 subsystem sanitization。相反地，成功 subsystem sanitize 也不會替 Boot Partition 更新或清除開機映像。

**常見誤解／Debug。** 把成功後 read 回零視為唯一成功標準會誤判。先確認方法、是否 deallocate、是否在驗證狀態，再套用 NVM Command Set 定義的結果。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§8.1.27，文件頁 711-712，PDF 頁 737-738; NVME-BASE-2.4 Rev. 2.4，§8.1.27，文件頁 711-712，PDF 頁 737-738; NVME-BASE-2.4 Rev. 2.4，§8.1.27.2-8.1.27.3，文件頁 714-717，PDF 頁 740-743; NVME-NVM-CS-1.3 Rev. 1.3，§5.12，文件頁 174，PDF 頁 174

**關聯 Figure：** Figure 770, Figure 771, Figure 200, Figure 201

### Module 06: 命令參數與 capability 組合

**解釋。** 先把支援能力、命令要求與 Feature policy 分開。命令接受、operation 成功、符合 no-deallocate 要求是三個需要不同證據的結果。

```text
SANICAP / target
  ↓
SANACT and modifiers
  ↓
FID 17h policy
  ↓
Preflight and CQE
  ↓
LID 81h operation result
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| NDAS=1, NDI=0 | 不得因成功 sanitize deallocate | 其他合法條件仍需符合 |
| NDAS=1, NDI=1, NODRM=0 | 命令拒絕 | Invalid Field in Command |
| NDAS=1, NDI=1, NODRM=1 | 允許處理 | 成功可回 SOS=100b |
| EMVS=1 | Subsystem 要 VERS=1 | Block/Crypto + NDAS=0 |

**說明性範例。** SANACT=010b、AUSE=0、EMVS=1、NDAS=0、PREQ=0 的 CDW10 是 0402h。只有支援 VERS/Block Erase 且其他前置條件成立時才適用。另一例：OWPASS=0h 是 16 次，不是『跳過 overwrite』。

**常見誤解／Debug。** Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.26，文件頁 448-451，PDF 頁 474-477; NVME-BASE-2.4 Rev. 2.4，§8.1.27.1; 5.2.27，文件頁 713,453，PDF 頁 739,479; NVME-BASE-2.4 Rev. 2.4，§5.2.30.1.16; 8.1.27.2-8.1.27.3，文件頁 477-478,715-719，PDF 頁 503-504,741-745; NVME-BASE-2.4 Rev. 2.4，§5.2.26，文件頁 449，PDF 頁 475; NVME-BASE-2.4 Rev. 2.4，§5.2.26; 8.1.27.1，文件頁 449-451,712-714，PDF 頁 475-477,738-740; NVME-BASE-2.4 Rev. 2.4，§5.2.26; 8.1.27.3，文件頁 451,717，PDF 頁 477,743

**關聯 Figure：** Figure 338, Figure 451, Figure 452, Figure 453, Figure 454, Figure 492

### Module 07: 用 state、log、AER 重建背景作業

**解釋。** 從 Figure 772 的七個 states 出發，逐一把 Figures 773–779 的 transition condition 接上。Status 描述結果，state 描述目前位置，事件描述發生的轉折。

```text
Idle
  ↓
Restricted/Unrestricted Processing
  ↓
Failure OR Verification
  ↓
Post-Verification Deallocation
  ↓
Idle + final log
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Restricted Failure | 只以 restricted 重試 | Exit Failure Mode 不可解套 |
| Unrestricted Failure | 重試或 Exit Failure Mode | 回 Idle 不會改寫失敗歷史 |
| Media Verification | Processing 已成功 | 整個 operation 仍 Sanitizing |
| Post-Verification Deallocation | SPROG 重新由 0 起算 | 失敗 FAILS=6h |

**說明性範例。** SPROG=8000h 表示目前被量測的階段約 50%。進入 Media Verification 後 SPROG=FFFFh，SOS 仍可為 010b；退出驗證進入 deallocation 又從 0 開始。這不是進度倒退。

**常見誤解／Debug。** 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.26.1; 8.1.27.1，文件頁 451,712-713，PDF 頁 477,738-739; NVME-BASE-2.4 Rev. 2.4，§8.1.27.4，文件頁 719-730，PDF 頁 745-756; NVME-BASE-2.4 Rev. 2.4，§8.1.27.4.6-8.1.27.4.7，文件頁 727-730，PDF 頁 753-756; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.38，文件頁 313-319，PDF 頁 339-345; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.38; 8.1.27.3，文件頁 314-319,718，PDF 頁 340-345,744; NVME-BASE-2.4 Rev. 2.4，§8.1.27.1; 8.1.27.4，文件頁 712-713,720，PDF 頁 738-739,746

**關聯 Figure：** Figure 312, Figure 151, Figure 152, Figure 156, Figure 772, Figure 773, Figure 774, Figure 775, Figure 776, Figure 777, Figure 778, Figure 779

### Module 08: 操作限制與驗證讀取

**解釋。** 把 command allowlist 與 NVM Read 特例分開判斷。Host 先辨識 target/state，再確認 PI checking 與 allocation，不能把平常 read 的處理完全套入驗證狀態。

```text
Target/state
  ↓
Admin/I/O permission
  ↓
PRCHK=000b and STC=0
  ↓
Allocated media readable?
  ↓
Data + specific status
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| PI checking requested | Invalid Field in Command | 驗證讀取不允許此組合 |
| Allocated media readable | 回實際 media data | 可忽略可讀情況的 integrity error |
| Allocated media unreadable | Unrecovered Read Error | 不可假造資料 |
| Deallocated LBA | 依 deallocated/unwritten 規則 | 不是檢查原始 media pattern 的證據 |

**說明性範例。** 驗證讀取 PRCHK=000b、STC=0，所有 allocated LBAs 都能讀取，且沒有其他 abort 原因時，預期 Successful Media Verification Read。只要請求 PI checking，預期分支即改為 Invalid Field in Command。

**常見誤解／Debug。** 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§8.1.27.5; 5.1.1-5.1.2，文件頁 178-181,730-732，PDF 頁 204-207,756-758; NVME-BASE-2.4 Rev. 2.4，§8.1.27.5，文件頁 730-732，PDF 頁 756-758; NVME-NVM-CS-1.3 Rev. 1.3，§4.1.7; 5.12，文件頁 113,173-175，PDF 頁 113,173-175; NVME-NVM-CS-1.3 Rev. 1.3，§5.12，文件頁 174，PDF 頁 174; NVME-NVM-CS-1.3 Rev. 1.3，§5.12.1，文件頁 174-175，PDF 頁 174-175; NVME-BASE-2.4 Rev. 2.4，§8.1.3.1; 8.1.27.4.2，文件頁 587,721，PDF 頁 613,747

**關聯 Figure：** Figure 11, Figure 12, Figure 144, Figure 145, Figure 146, Figure 200, Figure 201, Figure 311

## 可追溯的規格重點

前面的 Mental Model 解釋因果；本節保留每個可追溯結論與 normative 強度，供講者備註與審查。

### 1. 兩個 Boot Partitions

<!-- claim:BASEBTS-BOOT-MODEL -->

Boot Partitions 是選用功能；支援時有兩個等大的 partition，ID 為 0h、1h。Host 可在未建立 queues、未啟用 controller 時透過 properties 讀取。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3, 文件頁 586, PDF 頁 612

### 2. Property 讀取與 BRS

<!-- claim:BASEBTS-BOOT-READ -->

Host 先檢查 CAP.BPS、BPINFO 的 active ID/size，再配置連續 buffer 與 BPMBL，確認沒有讀取進行中後寫入 BPRSEL。BRS=01b 表示傳輸中，10b 表示成功，11b 表示錯誤；讀取中不得 reset、shutdown 或改動 transport-specific properties。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.1, 文件頁 586-587, PDF 頁 612-613

### 3. LID 15h 的另一條讀取路徑

<!-- claim:BASEBTS-BOOT-LOG -->

LID 15h 以 CDW10.LSP 的 BPID 選 partition，回傳 16-byte header 與其後的資料；BPSZ 以 128 KiB 計。此 log 讀取不改變 BPINFO、BPRSEL 或 BPMBL properties。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, 文件頁 283-284, PDF 頁 309-310

### 4. 下載、寫入、驗證、切換

<!-- claim:BASEBTS-BOOT-UPDATE -->

Boot image 從開頭依序用 Firmware Image Download 傳送；將目標解鎖後，以 Firmware Commit CA=110b 寫入 BPID 指定的 partition。Host 可讀回驗證，再以 CA=111b 更新 active ID，最後重新上鎖。更新中斷可能留下新舊混合內容，因此宜先驗證再設為 active。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, 文件頁 587-588, PDF 頁 613-614

### 5. 更新序列的邊界

<!-- claim:BASEBTS-BOOT-SEQUENCE -->

Host 不宜在寫入 Boot Partition 時同時讀取，也不宜重疊 firmware/boot image 更新序列。單一序列宜使用同一 controller 或 Management Endpoint；跨端點提交可能使 Commit 以 Invalid Firmware Image 結束。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, 文件頁 588, PDF 頁 614

### 6. 保護能力與控制權

<!-- claim:BASEBTS-BOOT-CAP -->

BPCAP 回報 Set Features 與 RPMB Boot 保護能力。只有 Set Features 機制或 RPMB 尚未啟用時由 FID 85h 控制；RPMB 保護啟用後由 RPMB 控制。同一時刻只有一套機制控制狀態，共享 partition 的所有 controllers 都須執行其保護。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.3, 文件頁 588-589, PDF 頁 614-615

### 7. FID 85h 逐欄判讀

<!-- claim:BASEBTS-BOOT-FID -->

BP0WPS 位於 CDW11[2:0]，BP1WPS 位於 [5:3]。000b 僅用於 Set 的不改變請求；001b/010b/011b 分別為 unlocked/locked/locked until power cycle；100b 由 Get 回報 RPMB 控制，不能作為 Set 值。此 Feature 不可 save，power cycle 後預設 locked。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39, 文件頁 513-514, PDF 頁 539-540

### 8. 兩套保護的 reset 差異

<!-- claim:BASEBTS-BOOT-RESET -->

Set Features 的 unlocked 狀態跨 Controller Level Reset 保留，但 power cycle 後回到 locked；locked-until-power-cycle 也不能用一般 Set 解開。RPMB 保護啟用後，unlocked 遇 power cycle 或 Controller Level Reset 會回到 locked，且啟用本身不可撤回。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1-8.1.3.3.3, 文件頁 589-594, PDF 頁 615-620

### 9. 保護狀態的拒絕條件

<!-- claim:BASEBTS-BOOT-REJECT -->

嘗試修改 locked-until-power-cycle 或 RPMB 控制中的狀態，FID 85h 以 Feature Not Changeable 拒絕。Multi-domain subsystem 中共享的 partition 不允許 locked-until-power-cycle。兩套機制並存時，只要任一 partition 在該狀態，就不得啟用 RPMB Boot 保護來繞過它。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39; 8.1.3.3.3, 文件頁 513-514,593-594, PDF 頁 539-540,619-620

### 10. Header 與累積式 Data Areas

<!-- claim:BASEBTS-TEL-MODEL -->

Telemetry 的 header 為 block 0，每個 block 是 512 bytes；所有 Data Areas 都從 block 1 起算。Area 2/3/4 是更大的累積集合，不是接在 Area 1 後的獨立區塊。Last Block 是包含在內的最後 block 編號；payload 格式與大小由廠商定義。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.13.1.8-5.2.13.1.9, 文件頁 232-237,733-737, PDF 頁 258-263,759-763

### 11. CTHID 與 MCDA

<!-- claim:BASEBTS-TEL-CREATE -->

LID 07h 的 CTHID 是 CDW10 bit 8；設為 1 要求新 capture，0 不更新該 snapshot。MCDA 是 bits 11:9，只有 MCDAS=1 且 CTHID=1 時適用；001b 至 100b 分別要求建立至 Area 1 至 Area 4，000b 由 controller 決定。MCDAS 來自 Supported Log Pages 的 LID Specific Parameter。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, 文件頁 232-235, PDF 頁 258-261

### 12. Area 4 的雙方支援條件

<!-- claim:BASEBTS-TEL-DA4 -->

Controller 以 LPA.TS 宣告 Telemetry 支援，以 LPA.DA4S 宣告 Area 4；Host 以 FID 16h Host Behavior Support 的 ETDAS=1 宣告支援。DA4S 與 ETDAS 一起決定 Area 4 是否適用；建立 Area 4 時也須建立有資料的 Area 3。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.15, 文件頁 476,733-734, PDF 頁 502,759-760

### 13. Offset、長度與保留範圍

<!-- claim:BASEBTS-TEL-ALIGN -->

讀取 LID 07h/08h 時，offset 與 transfer length 必須是 512 bytes 的倍數，否則回報 Invalid Field in Command。Controller 回傳被要求的 blocks，但超過適用最後 Data Area 邊界的資料不具規格定義的內容。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, 文件頁 232-237, PDF 頁 258-263

### 14. 一致性與完成讀取

<!-- claim:BASEBTS-TEL-CONSISTENCY -->

Host 讀 header 記住 generation，以 RAE=1 分段收集，再重讀 header 比對 generation；不同就重新讀取。讀 08h 還需確認 TCDA 未被其他讀取者清除；完成後用 RAE=0 讀任一部分來 acknowledgement。Generation 是 8-bit，FFh 後回到 0h。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30, 文件頁 734-735, PDF 頁 760-761

### 15. 2.4 的 TCDA=0

<!-- claim:BASEBTS-TEL-TCDA -->

Base 2.4 的 TCDA=0 表示自上次成功 RAE=0 讀取後沒有更新。第一次 capture 前 header 可讀；capture 過後，即使 TCDA=0，仍回傳 header 與目前保存的 internal state。不能把舊版『0 表示只有 header』的解讀沿用至 2.4。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, 文件頁 237, PDF 頁 263

### 16. Snapshot 的保留條件

<!-- claim:BASEBTS-TEL-PERSIST -->

07h 的 snapshot 不變，直到新的 CTHID=1、Firmware Commit 或 power-on reset。08h Areas 1–3 跨所有 resets 保留，Area 4 可跨 Controller Level Resets 保留；08h 的 TCDA、TCDGN 跨 power cycles 與 resets 保留。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, 文件頁 233,235,237, PDF 頁 259,261,263

### 17. Telemetry Notice 的啟用

<!-- claim:BASEBTS-TEL-EVENT -->

Host 以 FID 0Bh 的 TLN bit 10 啟用 Telemetry Log Notices；controller 以 Notice 類型的 Telemetry Log Changed AER 通知，也可由 07h/08h 的 TCDA 得知資料更新。8.1.30 指向 .1.5 的引用錯置；同版的 AEC 實際在 5.2.30.1.6。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.6, 文件頁 734-735,466-468, PDF 頁 760-761,492-494

### 18. Subsystem 與 namespace 的不同範圍

<!-- claim:BASEBTS-SAN-SCOPE -->

Subsystem sanitize 與 namespace sanitize 的資料範圍不同。逐一 sanitize 全部 namespaces 不等同 subsystem sanitize，也不能因此把 subsystem GDE 設為 1。兩者都不影響 Boot Partitions 或 RPMB；含 user data 的 logs/features 則可能必須修改。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27, 文件頁 711-712, PDF 頁 737-738

### 19. 快取與記憶體邊界

<!-- claim:BASEBTS-SAN-MEDIA -->

Sanitize 涵蓋 target 的 allocated/deallocated media 與含其 user data 的快取。Subsystem sanitize 對 CMB queue 內容是否修改由實作定義，其餘 CMB 資料須處理；HMB 不受影響。PMR 必須先 disabled，subsystem sanitize 才可開始，且其資料在處理範圍內；namespace sanitize 不影響 CMB、HMB、PMR 或 PDA。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27, 文件頁 711-712, PDF 頁 737-738

### 20. 三種方法與 clear/purge

<!-- claim:BASEBTS-SAN-METHOD -->

Block Erase 使用媒體特有 erase；Crypto Erase 改變所有相關 media encryption keys，未加密資料另以適合方法處理；Overwrite 寫入 pattern。PREQ/SPRRS 控制 purge 要求與回報；Crypto Erase 遺留舊 key 或應處理的未加密資料時須失敗。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.2-8.1.27.3, 文件頁 714-717, PDF 頁 740-743

### 21. Sanitize 命令編碼

<!-- claim:BASEBTS-SAN-COMMAND -->

CDW10 包含 SANACT[2:0]、AUSE[3]、OWPASS[7:4]、OIPBP[8]、NDAS[9]、EMVS[10]、PREQ[11]；CDW11 是 OVRPAT。SANACT 001b=Exit Failure Mode、010b=Block Erase、011b=Overwrite、100b=Crypto Erase、101b=Exit Media Verification；其他值保留。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, 文件頁 448-451, PDF 頁 474-477

### 22. Sanitize Namespace 不是相同欄位布局

<!-- claim:BASEBTS-SAN-NAMESPACE -->

被主範圍引用的 Figure 454 定義 namespace 命令：SANACT 只允許 001b、100b、101b；AUSE 在 bit 3、PREQ 在 bit 4、EMVS 在 bit 10。它沒有 Overwrite/NDAS 欄位，不可直接複製 subsystem Sanitize 的 CDW10。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 5.2.27, 文件頁 713,453, PDF 頁 739,479

### 23. NDAS、NDI、NODRM 與 NODMMAS

<!-- claim:BASEBTS-SAN-NDAS -->

NDAS 是本次命令的保留配置要求；NDI 表示 controller 是否抑制它。NDAS=1 且 NDI=1 時，FID 17h 的 NODRM=0 使命令以 Invalid Field in Command 拒絕，NODRM=1 可接受並在成功後以 SOS=100b 回報 unexpected deallocation。NODMMAS=10b 則描述適用時的額外 media modification。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.16; 8.1.27.2-8.1.27.3, 文件頁 477-478,715-719, PDF 頁 503-504,741-745

### 24. Media Verification 的命令組合

<!-- claim:BASEBTS-SAN-EMVS -->

Subsystem sanitize 要求 EMVS=1 時，需要 VERS=1、SANACT 為 Block Erase 或 Crypto Erase，且 NDAS=0；Overwrite 或 NDAS=1 的組合以 Invalid Field in Command 拒絕。SANACT=101b 只可在 Media Verification state 使用，並啟動後續 deallocation 而非新的 sanitize。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, 文件頁 449, PDF 頁 475

### 25. 開始前的拒絕條件

<!-- claim:BASEBTS-SAN-PREFLIGHT -->

PMR enabled、namespace write protection、controller suspended 或 pending firmware activation/reset 都可能阻止 subsystem sanitize。若啟動命令不是 Successful Completion，就不開始該 operation、不改 target 的 Sanitize Status，也不改 user data；已能預知的 operation 失敗則宜由後續 log 回報。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.1, 文件頁 449-451,712-714, PDF 頁 475-477,738-740

### 26. CQE 不是 sanitize 完成

<!-- claim:BASEBTS-SAN-BACKGROUND -->

Sanitize 在背景執行。開始 operation 後先更新 LID 81h，再完成啟動命令；Host 需用狀態 log 與事件判定後續進度。執行中的 operation 不能被 abort，並持續跨 reset/power cycle，但 verification 階段可能因指定 reset 被取消。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26.1; 8.1.27.1, 文件頁 451,712-713, PDF 頁 477,738-739

### 27. Overwrite passes 的奇偶

<!-- claim:BASEBTS-SAN-OVERWRITE -->

OWPASS=0h 表示 16 passes。OIPBP=0 時 user data 使用 OVRPAT、PI bytes 為 FFh。OIPBP=1 且總次數為偶數時第一輪使用反相 pattern、PI=00h；奇數時第一輪使用原 pattern、PI=FFh，其後逐輪反相。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.3, 文件頁 451,717, PDF 頁 477,743

### 28. 七個狀態與兩種失敗路徑

<!-- claim:BASEBTS-SAN-STATE -->

每個支援的 target 有一份狀態機。AUSE=0/1 分別進入 Restricted/Unrestricted Processing；失敗落入對應 Failure。Restricted Failure 必須以 restricted sanitize 重試；Unrestricted Failure 可重試或 Exit Failure Mode 回 Idle。Idle 因而不必然表示最後一次 sanitize 成功。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4, 文件頁 719-730, PDF 頁 745-756

### 29. Verification 與 deallocation 的銜接

<!-- claim:BASEBTS-SAN-VERIFY-STATE -->

Processing 成功且 EMVS 要求未被取消時進入 Media Verification。Exit Media Verification、適用 reset 或阻止驗證的 composition change 使 target 進入 Post-Verification Deallocation；成功才回 Idle，失敗依原 AUSE 回 Restricted/Unrestricted Failure，FAILS=6h。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.6-8.1.27.4.7, 文件頁 727-730, PDF 頁 753-756

### 30. LID 81h 的 scope 與狀態

<!-- claim:BASEBTS-SAN-STATUS -->

LID 81h 的 NSID=0h 或 FFFFFFFFh 指 subsystem，allocated NSID 指 namespace。SSTAT 含 SOS、OPC、GDE、MVCNCLD、NDE、PRGD；SSI 含 SANS/FAILS；SCDW10 保存啟動參數。MNSOIP 回報並行 namespace operations 上限，STNSID 識別 namespace target。Log 跨 power cycles/resets 保留。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, 文件頁 313-319, PDF 頁 339-345

### 31. SPROG 與時間估計

<!-- claim:BASEBTS-SAN-PROGRESS -->

SPROG 的比例是 raw/65536，分別表示 Processing 或 Post-Verification Deallocation 的進度，進入這些階段時重設為 0。Media Verification 時可為 FFFFh 而 SOS 仍是 Sanitizing；不能只看 SPROG 判斷完成。時間估計依方法與額外 media modification 分開，FFFFFFFFh 表示未回報。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38; 8.1.27.3, 文件頁 314-319,718, PDF 頁 340-345,744

### 32. 三種 Sanitize 事件

<!-- claim:BASEBTS-SAN-EVENT -->

Sanitize AER 使用 AET=110b、LID=81h，AEI=01h/02h/03h 分別表示 Completed、Completed With Unexpected Deallocation、Entered Media Verification。DW1 的 EVNTSP 為 subsystem 的 0h 或 target NSID。事件要與 log 一起判讀，Completed 不自動代表成功。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 8.1.27.4, 文件頁 712-713,720, PDF 頁 738-739,746

### 33. 執行中的命令限制

<!-- claim:BASEBTS-SAN-RESTRICT -->

Subsystem sanitize 進行中以 Figure 144 判斷允許的 Admin 命令及 log pages；Boot Partition log 在清單內，Telemetry 07h/08h 不在。未被允許的操作受 Sanitize In Progress 限制；namespace sanitize 另依 Figures 145/146 與 target NSID 判斷。Media Verification 的 NVM Read 有特定例外。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.5; 5.1.1-5.1.2, 文件頁 178-181,730-732, PDF 頁 204-207,756-758

### 34. 多 controller、電源與韌體限制

<!-- claim:BASEBTS-SAN-POWER -->

Sanitize 開始時 controllers 更新 target log 並暫停 autonomous power state management。依 target 中止受影響 I/O/self-test、釋放相關 streams；進行中不得 activation 新 firmware。Subsystem operation 也阻止 PMR enable 與 PDA access。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.5, 文件頁 730-732, PDF 頁 756-758

### 35. NVM Command Set 的補充位置

<!-- claim:BASEBTS-NVM-BRIDGE -->

NVM 4.1.7 沿用 Base 的 Sanitize command；5.12 補充允許的 Admin 行為、sanitize 後的資料值與 Media Verification Read。Error Information 的 LBA 要回傳 0，其他含 user data 的欄位仍依 Base 處理。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.7; 5.12, 文件頁 113,173-175, PDF 頁 113,173-175

### 36. Sanitize 後不一定讀到零

<!-- claim:BASEBTS-NVM-VALUES -->

成功後 audit 讀到的值：Block Erase 為 vendor-specific，Crypto Erase 為 indeterminate，Overwrite 依 Base 的 pattern 機制。若已 deallocate，讀取另依 Deallocated or Unwritten Logical Blocks 規則；未 deallocate 且啟用 PI checking 的讀取可能發生 PI check error。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12, 文件頁 174, PDF 頁 174

### 37. Media Verification Read 的三條分支

<!-- claim:BASEBTS-NVM-VERIFY -->

Media Verification Read 不要求 PI checking，即 PRCHK=000b 且 STC=0。Allocated media 能讀時回傳實際資料並忽略可讀情況下的 integrity errors，未被其他錯誤中止就以 Successful Media Verification Read 完成；不能讀取 allocated media 時回 Unrecovered Read Error。指定 PI checking 則回 Invalid Field in Command。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12.1, 文件頁 174-175, PDF 頁 174-175

### 38. 原稿交叉引用的核對

<!-- claim:BASEBTS-SOURCE-XREF -->

原稿 Boot log 的 section 0 可由同版 LID 15h 定位到 5.2.13.1.21。SPROG 段落寫 Figure 311，但該圖實際為 Reservation Notification；SPROG 定義在 Figure 312。這是附件內部核對的疑似引用錯置，不宣稱為官方勘誤。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.1; 8.1.27.4.2, 文件頁 587,721, PDF 頁 613,747

## Figure 索引

本報告介紹全部 80 張納入範圍的 Figure。100 分鐘簡報以 section 主線與必講 Figure 為主，其餘 Figure 仍完整保留作為附錄。其中 48 張位於主章節範圍外，但因指定正文直接引用而納入相依教學。

- [§5.12](#section-5-12)

- [§5.2](#section-5-2)

- [§8.1](#section-8-1)

- [引用相依 Figure（位於主章節範圍外）](#section-dependency)

## Figure／欄位表教學參考

本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。欄位與 keyword 索引來自本機核對過的 PDF。

<a id="section-5-12"></a>

### §5.12

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 200: Sanitize Operations - Admin Commands Allowed</strong></summary>

<!-- claim:BASEBTS-NVMCS-FIG-200-CLAIM figure-table:BASEBTS-NVMCS-FIG-200 -->

**SPEC。** Figure 200〈Sanitize Operations - Admin Commands Allowed〉：NVM Command Set 補充 sanitize 期間的 Error Information 行為，LBA 回 0；同號的 Base Figure 200 是另一張表，不可混用。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

NVM Command Set 補充 sanitize 期間的 Error Information 行為，LBA 回 0；同號的 Base Figure 200 是另一張表，不可混用。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Get Log Page]
          ↓
[擷取欄位: Error Information] → [套用編碼: LBA]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Get Log Page` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Error Information` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `LBA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-NVM-CS-1.3、§5.12、Figure 200；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 command allowlist 與 NVM Read 特例分開判斷。Host 先辨識 target/state，再確認 PI checking 與 allocation，不能把平常 read 的處理完全套入驗證狀態。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 200 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.12 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | NVM Command Set 補充 sanitize 期間的 Error Information 行為，LBA 回 0；同號的 Base Figure 200 是另一張表，不可混用。 |
| 邊界 | 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。 |

**說明性範例。** 驗證讀取 PRCHK=000b、STC=0，所有 allocated LBAs 都能讀取，且沒有其他 abort 原因時，預期 Successful Media Verification Read。只要請求 PI checking，預期分支即改為 Invalid Field in Command。

**常見誤解。** 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Get Log Page, Error Information, LBA

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12, Figure 200, 文件頁 173, PDF 頁 173

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 201: Sanitize Operation Types - User Data Values</strong></summary>

<!-- claim:BASEBTS-NVMCS-FIG-201-CLAIM figure-table:BASEBTS-NVMCS-FIG-201 -->

**SPEC。** Figure 201〈Sanitize Operation Types - User Data Values〉：三種方法的 audit data values 分別是 vendor-specific、indeterminate、依 Overwrite 機制；若已 deallocate 則讀取依另一套規則。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

三種方法的 audit data values 分別是 vendor-specific、indeterminate、依 Overwrite 機制；若已 deallocate 則讀取依另一套規則。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Block Erase]
          ↓
[擷取欄位: Crypto Erase] → [套用編碼: Overwrite]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Block Erase` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Crypto Erase` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Overwrite` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-NVM-CS-1.3、§5.12、Figure 201；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. Sanitize scope 不是『磁碟上所有東西』。以 target、資料來源、是否可能含 user data 判斷；Boot 與診斷機制的交叉關係也從這個範圍開始。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 201 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.12 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 三種方法的 audit data values 分別是 vendor-specific、indeterminate、依 Overwrite 機制；若已 deallocate 則讀取依另一套規則。 |
| 邊界 | 把成功後 read 回零視為唯一成功標準會誤判。先確認方法、是否 deallocate、是否在驗證狀態，再套用 NVM Command Set 定義的結果。 |

**說明性範例。** 即使所有 namespaces 都已 sanitize，CMB 等 subsystem 層級資料仍不能由這個事實證明已完成 subsystem sanitization。相反地，成功 subsystem sanitize 也不會替 Boot Partition 更新或清除開機映像。

**常見誤解。** 把成功後 read 回零視為唯一成功標準會誤判。先確認方法、是否 deallocate、是否在驗證狀態，再套用 NVM Command Set 定義的結果。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 把成功後 read 回零視為唯一成功標準會誤判。先確認方法、是否 deallocate、是否在驗證狀態，再套用 NVM Command Set 定義的結果。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Block Erase, Crypto Erase, Overwrite

**來源 keyword 索引：** shall not, shall, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12, Figure 201, 文件頁 174, PDF 頁 174

</details>

<a id="section-5-2"></a>

### §5.2

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 220: Telemetry Host-Initiated Log Specific Parameter Field</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-220-CLAIM figure-table:BASEBTS-BASE-FIG-220 -->

**SPEC。** Figure 220〈Telemetry Host-Initiated Log Specific Parameter Field〉：CTHID 位於 CDW10 bit 8，MCDA 位於 bits 11:9。MCDAS=1 且 CTHID=1 才套用 MCDA；後續讀同一 snapshot 用 CTHID=0。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CTHID 位於 CDW10 bit 8，MCDA 位於 bits 11:9。MCDAS=1 且 CTHID=1 才套用 MCDA；後續讀同一 snapshot 用 CTHID=0。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CTHID]
          ↓
[擷取欄位: MCDA] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CTHID` | Create Telemetry Host-Initiated Data；07h 的 capture 要求，後續分段讀同一快照要清為 0。 |
| `MCDA` | Maximum Created Data Area；支援且要求 capture 時選擇建立的最大 area。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.13.1.8、Figure 220；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 07h 的 create 與後續讀取分開；08h 的 capture 由 controller 決定。Host 對兩者都要驗證 generation，並分清事件 acknowledgement 與刪除 payload。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 220 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13.1.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | CTHID 位於 CDW10 bit 8，MCDA 位於 bits 11:9。MCDAS=1 且 CTHID=1 才套用 MCDA；後續讀同一 snapshot 用 CTHID=0。 |
| 邊界 | 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。 |

**說明性範例。** 讀取前 generation=2Ah，讀完變成 2Bh，這批 blocks 不能當成同一 capture 的一致資料。若值保持 2Ah 但 TCDA 被其他 host 清成 0，08h 收集仍需依流程檢查該競態。

**常見誤解。** 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** CTHID, MCDA

**來源 keyword 索引：** shall not, shall, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, Figure 220, 文件頁 232-233, PDF 頁 258-259

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 221: Telemetry Host-Initiated Log Page</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-221-CLAIM figure-table:BASEBTS-BASE-FIG-221 -->

**SPEC。** Figure 221〈Telemetry Host-Initiated Log Page〉：07h 的 Last Blocks 在 bytes 8–19，THS 在 380、THDGN 在 381、TCDA/TCDGN 在 382/383；RID 在 384–511。先讀 header，再按累積 area 大小讀 payload。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

07h 的 Last Blocks 在 bytes 8–19，THS 在 380、THDGN 在 381、TCDA/TCDGN 在 382/383；RID 在 384–511。先讀 header，再按累積 area 大小讀 payload。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: THDA1LB]
          ↓
[擷取欄位: THDA2LB] → [套用編碼: THDA3LB]
                                      ↓
[驗證證據: THDA4LB]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `THDA1LB` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `THDA2LB` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `THDA3LB` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `THDA4LB` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `THS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `THDGN` | Telemetry Host-Initiated Data Generation Number；用來比對分段讀取是否仍屬同一快照。 |
| `TCDA` | Telemetry Controller-Initiated Data Available；2.4 中表示自上次 RAE=0 acknowledgement 後是否有更新。 |
| `TCDGN` | Telemetry Controller-Initiated Data Generation Number；8-bit generation，完成更新最後才遞增。 |
| `RID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.13.1.8、Figure 221；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. Area 是從同一 block 1 起算的不同大小視圖。先解碼 header，再選擇適用且有資料的最後 area；不要把三個 Last Block 數字相加。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 221 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13.1.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 07h 的 Last Blocks 在 bytes 8–19，THS 在 380、THDGN 在 381、TCDA/TCDGN 在 382/383；RID 在 384–511。先讀 header，再按累積 area 大小讀 payload。 |
| 邊界 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

**說明性範例。** Last Blocks=65/1000/30000 時，Area 3 payload 為 30000×512=15360000 bytes；包含 header 的 log 為 15360512 bytes。0/1000/1000 則表示 Area 1 空、Area 3 沒有超出 Area 2 的新增內容。

**常見誤解。** LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** THDA1LB, THDA2LB, THDA3LB, THDA4LB, THS, THDGN, TCDA, TCDGN, RID

**來源 keyword 索引：** shall not, shall, should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, Figure 221, 文件頁 234-235, PDF 頁 260-261

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 222: Telemetry Host-Initiated Log Page - LID Specific Parameter Field</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-222-CLAIM figure-table:BASEBTS-BASE-FIG-222 -->

**SPEC。** Figure 222〈Telemetry Host-Initiated Log Page - LID Specific Parameter Field〉：LID Specific Parameter bit 0 是 MCDAS；它宣告是否支援 MCDA，不表示已建立到哪一個 area。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

LID Specific Parameter bit 0 是 MCDAS；它宣告是否支援 MCDA，不表示已建立到哪一個 area。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MCDAS]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MCDAS` | Maximum Created Data Area Supported；07h 的 LID Specific Parameter bit 0，宣告 MCDA 支援。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.13.1.8、Figure 222；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 07h 的 create 與後續讀取分開；08h 的 capture 由 controller 決定。Host 對兩者都要驗證 generation，並分清事件 acknowledgement 與刪除 payload。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 222 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13.1.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | LID Specific Parameter bit 0 是 MCDAS；它宣告是否支援 MCDA，不表示已建立到哪一個 area。 |
| 邊界 | 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。 |

**說明性範例。** 讀取前 generation=2Ah，讀完變成 2Bh，這批 blocks 不能當成同一 capture 的一致資料。若值保持 2Ah 但 TCDA 被其他 host 清成 0，08h 收集仍需依流程檢查該競態。

**常見誤解。** 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** MCDAS

**來源 keyword 索引：** shall, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, Figure 222, 文件頁 235, PDF 頁 261

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 223: Telemetry Controller-Initiated Log Page</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-223-CLAIM figure-table:BASEBTS-BASE-FIG-223 -->

**SPEC。** Figure 223〈Telemetry Controller-Initiated Log Page〉：08h 的 TCS 在 byte 381；TCDA/TCDGN 位於 382/383。TCDGN 在資料更新最後才增加，讀完重讀 header 比對；TCDA=0 採 2.4 的 acknowledgement 後未更新語義。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

08h 的 TCS 在 byte 381；TCDA/TCDGN 位於 382/383。TCDGN 在資料更新最後才增加，讀完重讀 header 比對；TCDA=0 採 2.4 的 acknowledgement 後未更新語義。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TCDA1LB]
          ↓
[擷取欄位: TCDA2LB] → [套用編碼: TCDA3LB]
                                      ↓
[驗證證據: TCDA4LB]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TCDA1LB` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `TCDA2LB` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `TCDA3LB` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `TCDA4LB` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `TCS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `TCDA` | Telemetry Controller-Initiated Data Available；2.4 中表示自上次 RAE=0 acknowledgement 後是否有更新。 |
| `TCDGN` | Telemetry Controller-Initiated Data Generation Number；8-bit generation，完成更新最後才遞增。 |
| `RID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.13.1.9、Figure 223；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 07h 的 create 與後續讀取分開；08h 的 capture 由 controller 決定。Host 對兩者都要驗證 generation，並分清事件 acknowledgement 與刪除 payload。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 223 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13.1.9 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 08h 的 TCS 在 byte 381；TCDA/TCDGN 位於 382/383。TCDGN 在資料更新最後才增加，讀完重讀 header 比對；TCDA=0 採 2.4 的 acknowledgement 後未更新語義。 |
| 邊界 | 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。 |

**說明性範例。** 讀取前 generation=2Ah，讀完變成 2Bh，這批 blocks 不能當成同一 capture 的一致資料。若值保持 2Ah 但 TCDA 被其他 host 清成 0，08h 收集仍需依流程檢查該競態。

**常見誤解。** 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** TCDA1LB, TCDA2LB, TCDA3LB, TCDA4LB, TCS, TCDA, TCDGN, RID

**來源 keyword 索引：** shall not, shall, should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, Figure 223, 文件頁 236-237, PDF 頁 262-263

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 279: Boot Partition Log Specific Parameter Field</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-279-CLAIM figure-table:BASEBTS-BASE-FIG-279 -->

**SPEC。** Figure 279〈Boot Partition Log Specific Parameter Field〉：LID 15h 使用 CDW10 bit 8 選 BPID，其他 LSP bits 保留；同一 bit 在 07h 卻是 CTHID。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

LID 15h 使用 CDW10 bit 8 選 BPID，其他 LSP bits 保留；同一 bit 在 07h 卻是 CTHID。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: BPID]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `BPID` | Boot Partition Identifier；選取 0 或 1，與目前 active partition 分開。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.13.1.21、Figure 279；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 先問 controller 是否已建立 Admin command 環境，再選 property 或 LID 15h。兩條路徑讀同一類 Boot 內容，但回傳格式與狀態觀察點不同。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 279 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13.1.21 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | LID 15h 使用 CDW10 bit 8 選 BPID，其他 LSP bits 保留；同一 bit 在 07h 卻是 CTHID。 |
| 邊界 | 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。 |

**說明性範例。** BPSZ=2 的 LID 15h 包含 262144 bytes 的 Boot data，加上 16-byte header，共 262160 bytes。讀 BP1 並不把 BP1 設為 active；讀 log 也不會推進 property 的 BRS。

**常見誤解。** 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** BPID

**來源 keyword 索引：** shall, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, Figure 279, 文件頁 283, PDF 頁 309

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 280: Boot Partition Log Page</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-280-CLAIM figure-table:BASEBTS-BASE-FIG-280 -->

**SPEC。** Figure 280〈Boot Partition Log Page〉：Header bytes 0–15；BPINFO 在 bytes 4–7，ABPID 是 bit 31，BPSZ 是 bits 14:0。BPD 從 byte 16 起，長度為 BPSZ×128 KiB。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Header bytes 0–15；BPINFO 在 bytes 4–7，ABPID 是 bit 31，BPSZ 是 bits 14:0。BPD 從 byte 16 起，長度為 BPSZ×128 KiB。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LID]
          ↓
[擷取欄位: BPINFO] → [套用編碼: ABPID]
                                      ↓
[驗證證據: BPSZ]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LID` | Log Page Identifier，Get Log Page command 用來選擇 log page 的欄位。 |
| `BPINFO` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ABPID` | Active Boot Partition ID；指出目前選為啟動映像的 partition。 |
| `BPSZ` | Boot Partition Size；每單位 128 KiB。 |
| `BPD` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.13.1.21、Figure 280；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 先問 controller 是否已建立 Admin command 環境，再選 property 或 LID 15h。兩條路徑讀同一類 Boot 內容，但回傳格式與狀態觀察點不同。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 280 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13.1.21 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Header bytes 0–15；BPINFO 在 bytes 4–7，ABPID 是 bit 31，BPSZ 是 bits 14:0。BPD 從 byte 16 起，長度為 BPSZ×128 KiB。 |
| 邊界 | 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。 |

**說明性範例。** BPSZ=2 的 LID 15h 包含 262144 bytes 的 Boot data，加上 16-byte header，共 262160 bytes。讀 BP1 並不把 BP1 設為 active；讀 log 也不會推進 property 的 BRS。

**常見誤解。** 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** LID, BPINFO, ABPID, BPSZ, BPD

**來源 keyword 索引：** shall not, should not, shall, should, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, Figure 280, 文件頁 284, PDF 頁 310

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 312: Sanitize Status Log Page</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-312-CLAIM figure-table:BASEBTS-BASE-FIG-312 -->

**SPEC。** Figure 312〈Sanitize Status Log Page〉：512-byte log：SPROG[1:0]、SSTAT[3:2]、SCDW10[7:4]、時間估計[35:8]、SSI[36]、MNSOIP[43:40]、STNSID[47:44]。先用 NSID 決定 target，再一起讀 SOS/SANS/FAILS 與進度。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

512-byte log：SPROG[1:0]、SSTAT[3:2]、SCDW10[7:4]、時間估計[35:8]、SSI[36]、MNSOIP[43:40]、STNSID[47:44]。先用 NSID 決定 target，再一起讀 SOS/SANS/FAILS 與進度。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SPROG]
          ↓
[擷取欄位: SSTAT] → [套用編碼: SCDW10]
                                      ↓
[驗證證據: ETO]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SPROG` | Sanitize Progress；raw/65536，僅表示目前量測階段的進度。 |
| `SSTAT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SCDW10` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ETO` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ETPVDS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SSI` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MNSOIP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `STNSID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.13.1.38、Figure 312；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 從 Figure 772 的七個 states 出發，逐一把 Figures 773–779 的 transition condition 接上。Status 描述結果，state 描述目前位置，事件描述發生的轉折。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 312 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13.1.38 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 512-byte log：SPROG[1:0]、SSTAT[3:2]、SCDW10[7:4]、時間估計[35:8]、SSI[36]、MNSOIP[43:40]、STNSID[47:44]。先用 NSID 決定 target，再一起讀 SOS/SANS/FAILS 與進度。 |
| 邊界 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

**說明性範例。** SPROG=8000h 表示目前被量測的階段約 50%。進入 Media Verification 後 SPROG=FFFFh，SOS 仍可為 010b；退出驗證進入 deallocation 又從 0 開始。這不是進度倒退。

**常見誤解。** 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** SPROG, SSTAT, SCDW10, ETO, ETPVDS, SSI, MNSOIP, STNSID

**來源 keyword 索引：** shall, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, Figure 312, 文件頁 314-319, PDF 頁 340-345

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 451: Sanitize - Command Dword 10</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-451-CLAIM figure-table:BASEBTS-BASE-FIG-451 -->

**SPEC。** Figure 451〈Sanitize - Command Dword 10〉：由 SANACT 決定操作，再依方法解讀其餘 bits；OWPASS=0 是 16，EMVS 不能搭配 Overwrite/NDAS=1。PREQ bit 11 與 namespace 命令不同。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

由 SANACT 決定操作，再依方法解讀其餘 bits；OWPASS=0 是 16，EMVS 不能搭配 Overwrite/NDAS=1。PREQ bit 11 與 namespace 命令不同。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SANACT]
          ↓
[擷取欄位: AUSE] → [套用編碼: OWPASS]
                                      ↓
[驗證證據: OIPBP]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SANACT` | Sanitize Action；決定實際方法、退出 Failure 或退出 Media Verification。 |
| `AUSE` | Allow Unrestricted Sanitize Exit；選擇失敗時是否允許不經成功重試就退出 Failure。 |
| `OWPASS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `OIPBP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NDAS` | No-Deallocate After Sanitize；命令要求，需與 SANICAP.NDI 及 NODRM 一起解讀。 |
| `EMVS` | Enter Media Verification State；成功 processing 後要求進入驗證，受方法與 capability 限制。 |
| `PREQ` | Purge Request；與 SPRRS 一起判定 purge 要求與回報；兩種 Sanitize 命令的 bit 位置不同。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.26、Figure 451；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 先把支援能力、命令要求與 Feature policy 分開。命令接受、operation 成功、符合 no-deallocate 要求是三個需要不同證據的結果。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 451 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.26 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 由 SANACT 決定操作，再依方法解讀其餘 bits；OWPASS=0 是 16，EMVS 不能搭配 Overwrite/NDAS=1。PREQ bit 11 與 namespace 命令不同。 |
| 邊界 | Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。 |

**說明性範例。** SANACT=010b、AUSE=0、EMVS=1、NDAS=0、PREQ=0 的 CDW10 是 0402h。只有支援 VERS/Block Erase 且其他前置條件成立時才適用。另一例：OWPASS=0h 是 16 次，不是『跳過 overwrite』。

**常見誤解。** Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** SANACT, AUSE, OWPASS, OIPBP, NDAS, EMVS, PREQ

**來源 keyword 索引：** shall not, should not, shall, should, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 451, 文件頁 450-451, PDF 頁 476-477

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 452: Sanitize - Command Dword 11</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-452-CLAIM figure-table:BASEBTS-BASE-FIG-452 -->

**SPEC。** Figure 452〈Sanitize - Command Dword 11〉：CDW11 的 32-bit OVRPAT 僅在 Overwrite 適用；搭配 OIPBP 與 pass 奇偶才可推導每一輪寫入 pattern。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW11 的 32-bit OVRPAT 僅在 Overwrite 適用；搭配 OIPBP 與 pass 奇偶才可推導每一輪寫入 pattern。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: OVRPAT]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `OVRPAT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.26、Figure 452；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 先把支援能力、命令要求與 Feature policy 分開。命令接受、operation 成功、符合 no-deallocate 要求是三個需要不同證據的結果。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 452 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.26 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | CDW11 的 32-bit OVRPAT 僅在 Overwrite 適用；搭配 OIPBP 與 pass 奇偶才可推導每一輪寫入 pattern。 |
| 邊界 | Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。 |

**說明性範例。** SANACT=010b、AUSE=0、EMVS=1、NDAS=0、PREQ=0 的 CDW10 是 0402h。只有支援 VERS/Block Erase 且其他前置條件成立時才適用。另一例：OWPASS=0h 是 16 次，不是『跳過 overwrite』。

**常見誤解。** Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** OVRPAT

**來源 keyword 索引：** shall, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 452, 文件頁 451, PDF 頁 477

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 453: Sanitize - Command Specific Status Values</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-453-CLAIM figure-table:BASEBTS-BASE-FIG-453 -->

**SPEC。** Figure 453〈Sanitize - Command Specific Status Values〉：這些是啟動命令的 command-specific failure；與稍後背景作業的 Sanitize Failed/SOS 分開記錄。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

這些是啟動命令的 command-specific failure；與稍後背景作業的 Sanitize Failed/SOS 分開記錄。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Firmware Activation Requires Reset]
          ↓
[擷取欄位: PMR Enabled] → [套用編碼: Controller Suspended]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Firmware Activation Requires Reset` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PMR Enabled` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Controller Suspended` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.26、Figure 453；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 先把支援能力、命令要求與 Feature policy 分開。命令接受、operation 成功、符合 no-deallocate 要求是三個需要不同證據的結果。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 453 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.26 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 這些是啟動命令的 command-specific failure；與稍後背景作業的 Sanitize Failed/SOS 分開記錄。 |
| 邊界 | Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。 |

**說明性範例。** SANACT=010b、AUSE=0、EMVS=1、NDAS=0、PREQ=0 的 CDW10 是 0402h。只有支援 VERS/Block Erase 且其他前置條件成立時才適用。另一例：OWPASS=0h 是 16 次，不是『跳過 overwrite』。

**常見誤解。** Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Firmware Activation Requires Reset, PMR Enabled, Controller Suspended

**來源 keyword 索引：** shall, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 453, 文件頁 451, PDF 頁 477

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 492: Sanitize Config - Command Dword 11</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-492-CLAIM figure-table:BASEBTS-BASE-FIG-492 -->

**SPEC。** Figure 492〈Sanitize Config - Command Dword 11〉：FID 17h CDW11 bit 0 是 NODRM；只有 NDI=1 且命令 NDAS=1 才影響 error/warning response。不是每次 sanitize 都必須設定的開關。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

FID 17h CDW11 bit 0 是 NODRM；只有 NDI=1 且命令 NDAS=1 才影響 error/warning response。不是每次 sanitize 都必須設定的開關。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NODRM]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NODRM` | No-Deallocate Response Mode；FID 17h bit 0，選擇受抑制 NDAS 的 error 或 warning 回應。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.30.1.16、Figure 492；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 先把支援能力、命令要求與 Feature policy 分開。命令接受、operation 成功、符合 no-deallocate 要求是三個需要不同證據的結果。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 492 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.1.16 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | FID 17h CDW11 bit 0 是 NODRM；只有 NDI=1 且命令 NDAS=1 才影響 error/warning response。不是每次 sanitize 都必須設定的開關。 |
| 邊界 | Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。 |

**說明性範例。** SANACT=010b、AUSE=0、EMVS=1、NDAS=0、PREQ=0 的 CDW10 是 0402h。只有支援 VERS/Block Erase 且其他前置條件成立時才適用。另一例：OWPASS=0h 是 16 次，不是『跳過 overwrite』。

**常見誤解。** Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** NODRM

**來源 keyword 索引：** shall, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.16, Figure 492, 文件頁 477-478, PDF 頁 503-504

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 542: Boot Partition Write Protection Config - Command Dword 11</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-542-CLAIM figure-table:BASEBTS-BASE-FIG-542 -->

**SPEC。** Figure 542〈Boot Partition Write Protection Config - Command Dword 11〉：兩個 3-bit state 欄位獨立設定；000b 只表示 Set 不改變，Get 需回實際狀態，100b 只回報 RPMB 控制。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

兩個 3-bit state 欄位獨立設定；000b 只表示 Set 不改變，Get 需回實際狀態，100b 只回報 RPMB 控制。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: BP0WPS]
          ↓
[擷取欄位: BP1WPS] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `BP0WPS` | Boot Partition 0 Write Protection State；FID 85h 的 bits 2:0。 |
| `BP1WPS` | Boot Partition 1 Write Protection State；FID 85h 的 bits 5:3。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.30.1.39、Figure 542；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 542 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.1.39 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 兩個 3-bit state 欄位獨立設定；000b 只表示 Set 不改變，Get 需回實際狀態，100b 只回報 RPMB 控制。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** BP0WPS, BP1WPS

**來源 keyword 索引：** shall not, shall, should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39, Figure 542, 文件頁 513-514, PDF 頁 539-540

</details>

<a id="section-8-1"></a>

### §8.1

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 679: Boot Partition Overview</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-679-CLAIM figure-table:BASEBTS-BASE-FIG-679 -->

**SPEC。** Figure 679〈Boot Partition Overview〉：把兩個等大的 Boot Partitions 與此次 host 讀取 buffer 分開；active ID 選擇啟動映像，不限制 host 只能讀 active partition。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

把兩個等大的 Boot Partitions 與此次 host 讀取 buffer 分開；active ID 選擇啟動映像，不限制 host 只能讀 active partition。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Boot Partition 0]
          ↓
[擷取欄位: Boot Partition 1] → [套用編碼: Host Memory Buffer]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Boot Partition 0` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Boot Partition 1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Host Memory Buffer` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.3.1、Figure 679；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 先問 controller 是否已建立 Admin command 環境，再選 property 或 LID 15h。兩條路徑讀同一類 Boot 內容，但回傳格式與狀態觀察點不同。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 679 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 把兩個等大的 Boot Partitions 與此次 host 讀取 buffer 分開；active ID 選擇啟動映像，不限制 host 只能讀 active partition。 |
| 邊界 | 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。 |

**說明性範例。** BPSZ=2 的 LID 15h 包含 262144 bytes 的 Boot data，加上 16-byte header，共 262160 bytes。讀 BP1 並不把 BP1 設為 active；讀 log 也不會推進 property 的 BRS。

**常見誤解。** 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Boot Partition 0, Boot Partition 1, Host Memory Buffer

**來源 keyword 索引：** shall not, shall, should, may

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.1, Figure 679, 文件頁 587, PDF 頁 613

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 680: Set Features Boot Partition Write Protection State Machine Model</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-680-CLAIM figure-table:BASEBTS-BASE-FIG-680 -->

**SPEC。** Figure 680〈Set Features Boot Partition Write Protection State Machine Model〉：Set Features 在 unlocked/locked 間切換，兩者可進入 locked-until-power-cycle；power cycle 回 locked。Locked-until-power-cycle 沒有一般 Set 解鎖箭頭。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Set Features 在 unlocked/locked 間切換，兩者可進入 locked-until-power-cycle；power cycle 回 locked。Locked-until-power-cycle 沒有一般 Set 解鎖箭頭。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Write Unlocked]
          ↓
[擷取欄位: Write Locked] → [套用編碼: Write Locked Until Power Cycle]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Write Unlocked` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Write Locked` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Write Locked Until Power Cycle` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.3.3.1、Figure 680；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 680 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.3.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Set Features 在 unlocked/locked 間切換，兩者可進入 locked-until-power-cycle；power cycle 回 locked。Locked-until-power-cycle 沒有一般 Set 解鎖箭頭。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Write Unlocked, Write Locked, Write Locked Until Power Cycle

**來源 keyword 索引：** shall

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1, Figure 680, 文件頁 589, PDF 頁 615

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 681: Set Features Boot Partition Write Protection State Definitions</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-681-CLAIM figure-table:BASEBTS-BASE-FIG-681 -->

**SPEC。** Figure 681〈Set Features Boot Partition Write Protection State Definitions〉：逐列比較三個 state：controller reset 保留它們；power cycle 後 unlocked 與 until-power-cycle 都變 locked。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

逐列比較三個 state：controller reset 保留它們；power cycle 後 unlocked 與 until-power-cycle 都變 locked。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Power Cycles]
          ↓
[擷取欄位: Controller Level Resets] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Power Cycles` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Controller Level Resets` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.3.3.1、Figure 681；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 681 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.3.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 逐列比較三個 state：controller reset 保留它們；power cycle 後 unlocked 與 until-power-cycle 都變 locked。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Power Cycles, Controller Level Resets

**來源 keyword 索引：** may

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1, Figure 681, 文件頁 590, PDF 頁 616

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 682: RPMB Boot Partition Write Protection State Machine Model</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-682-CLAIM figure-table:BASEBTS-BASE-FIG-682 -->

**SPEC。** Figure 682〈RPMB Boot Partition Write Protection State Machine Model〉：RPMB enable 之前與之後是不同區域；啟用後以 authenticated configuration write 解鎖/上鎖，reset 會回 locked。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

RPMB enable 之前與之後是不同區域；啟用後以 authenticated configuration write 解鎖/上鎖，reset 會回 locked。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: RPMB Disabled]
          ↓
[擷取欄位: RPMB Enabled] → [套用編碼: Write Locked]
                                      ↓
[驗證證據: Write Unlocked]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `RPMB Disabled` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `RPMB Enabled` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Write Locked` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Write Unlocked` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.3.3.2、Figure 682；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 682 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.3.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | RPMB enable 之前與之後是不同區域；啟用後以 authenticated configuration write 解鎖/上鎖，reset 會回 locked。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** RPMB Disabled, RPMB Enabled, Write Locked, Write Unlocked

**來源 keyword 索引：** shall

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.2, Figure 682, 文件頁 591, PDF 頁 617

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 683: RPMB Boot Partition Write Protection State Definitions</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-683-CLAIM figure-table:BASEBTS-BASE-FIG-683 -->

**SPEC。** Figure 683〈RPMB Boot Partition Write Protection State Definitions〉：RPMB-only 且保護尚未啟用時 unlocked 可保留；保護啟用後 unlocked 不跨 reset/power cycle。雙機制支援時還要套用 Figure 684 的預設與控制權。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

RPMB-only 且保護尚未啟用時 unlocked 可保留；保護啟用後 unlocked 不跨 reset/power cycle。雙機制支援時還要套用 Figure 684 的預設與控制權。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: RPMB Protection Enabled]
          ↓
[擷取欄位: Persistence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `RPMB Protection Enabled` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Persistence` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.3.3.2、Figure 683；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 683 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.3.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | RPMB-only 且保護尚未啟用時 unlocked 可保留；保護啟用後 unlocked 不跨 reset/power cycle。雙機制支援時還要套用 Figure 684 的預設與控制權。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** RPMB Protection Enabled, Persistence

**來源 keyword 索引：** shall

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.2, Figure 683, 文件頁 591, PDF 頁 617

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 684: Boot Partition Write Protection State Machine Model</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-684-CLAIM figure-table:BASEBTS-BASE-FIG-684 -->

**SPEC。** Figure 684〈Boot Partition Write Protection State Machine Model〉：先沿 Set Features 區追蹤狀態，再經 enable gate 轉移到 RPMB；不能從 until-power-cycle bypass 到 RPMB。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

先沿 Set Features 區追蹤狀態，再經 enable gate 轉移到 RPMB；不能從 until-power-cycle bypass 到 RPMB。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Set Features Owner]
          ↓
[擷取欄位: RPMB Owner] → [套用編碼: Enable Gate]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Set Features Owner` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `RPMB Owner` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Enable Gate` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.3.3.3、Figure 684；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 684 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.3.3.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 先沿 Set Features 區追蹤狀態，再經 enable gate 轉移到 RPMB；不能從 until-power-cycle bypass 到 RPMB。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Set Features Owner, RPMB Owner, Enable Gate

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.3, Figure 684, 文件頁 593, PDF 頁 619

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 770: Sanitization Operation Scope Based on Sanitize Operation</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-770-CLAIM figure-table:BASEBTS-BASE-FIG-770 -->

**SPEC。** Figure 770〈Sanitization Operation Scope Based on Sanitize Operation〉：每一資料類別分別看兩種 target：Boot/RPMB 不動，user-data locations 要處理，CMB/PMR/PDA 的差異不可被『全部 namespaces』概括。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

每一資料類別分別看兩種 target：Boot/RPMB 不動，user-data locations 要處理，CMB/PMR/PDA 的差異不可被『全部 namespaces』概括。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Subsystem Target]
          ↓
[擷取欄位: Namespace Target] → [套用編碼: User Data]
                                      ↓
[驗證證據: Boot Partition]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Subsystem Target` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Namespace Target` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `User Data` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Boot Partition` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CMB` | Controller Memory Buffer，controller 提供、可放置部分 queue 或資料結構的記憶體區域。 |
| `PMR` | Persistent Memory Region，由 controller 暴露、具有持久性語意的記憶體區域。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.27、Figure 770；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. Sanitize scope 不是『磁碟上所有東西』。以 target、資料來源、是否可能含 user data 判斷；Boot 與診斷機制的交叉關係也從這個範圍開始。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 770 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.27 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 每一資料類別分別看兩種 target：Boot/RPMB 不動，user-data locations 要處理，CMB/PMR/PDA 的差異不可被『全部 namespaces』概括。 |
| 邊界 | 把成功後 read 回零視為唯一成功標準會誤判。先確認方法、是否 deallocate、是否在驗證狀態，再套用 NVM Command Set 定義的結果。 |

**說明性範例。** 即使所有 namespaces 都已 sanitize，CMB 等 subsystem 層級資料仍不能由這個事實證明已完成 subsystem sanitization。相反地，成功 subsystem sanitize 也不會替 Boot Partition 更新或清除開機映像。

**常見誤解。** 把成功後 read 回零視為唯一成功標準會誤判。先確認方法、是否 deallocate、是否在驗證狀態，再套用 NVM Command Set 定義的結果。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 把成功後 read 回零視為唯一成功標準會誤判。先確認方法、是否 deallocate、是否在驗證狀態，再套用 NVM Command Set 定義的結果。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Subsystem Target, Namespace Target, User Data, Boot Partition, CMB, PMR

**來源 keyword 索引：** shall not, shall, may, optional

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27, Figure 770, 文件頁 711-712, PDF 頁 737-738

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 771: Sanitize Operations - Overwrite Mechanism</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-771-CLAIM figure-table:BASEBTS-BASE-FIG-771 -->

**SPEC。** Figure 771〈Sanitize Operations - Overwrite Mechanism〉：用 total pass 奇偶決定第一輪是否反相，再逐輪反相；PI bytes 也有 FFh/00h 規則。不能只看最後的 OVRPAT。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

用 total pass 奇偶決定第一輪是否反相，再逐輪反相；PI bytes 也有 FFh/00h 規則。不能只看最後的 OVRPAT。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: OIPBP]
          ↓
[擷取欄位: OWPASS] → [套用編碼: OVRPAT]
                                      ↓
[驗證證據: PI]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `OIPBP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `OWPASS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `OVRPAT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PI` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.27.3、Figure 771；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 先把支援能力、命令要求與 Feature policy 分開。命令接受、operation 成功、符合 no-deallocate 要求是三個需要不同證據的結果。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 771 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.27.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 用 total pass 奇偶決定第一輪是否反相，再逐輪反相；PI bytes 也有 FFh/00h 規則。不能只看最後的 OVRPAT。 |
| 邊界 | Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。 |

**說明性範例。** SANACT=010b、AUSE=0、EMVS=1、NDAS=0、PREQ=0 的 CDW10 是 0402h。只有支援 VERS/Block Erase 且其他前置條件成立時才適用。另一例：OWPASS=0h 是 16 次，不是『跳過 overwrite』。

**常見誤解。** Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** OIPBP, OWPASS, OVRPAT, PI

**來源 keyword 索引：** shall, may

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.3, Figure 771, 文件頁 717, PDF 頁 743

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 772: Sanitize Operation State Machine</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-772-CLAIM figure-table:BASEBTS-BASE-FIG-772 -->

**SPEC。** Figure 772〈Sanitize Operation State Machine〉：七個 state 以 AUSE 分出兩條 processing/failure 路徑，EMVS 接到 verification，再經 deallocation 返回；逐條配合 Figures 773–779 判讀。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

七個 state 以 AUSE 分出兩條 processing/failure 路徑，EMVS 接到 verification，再經 deallocation 返回；逐條配合 Figures 773–779 判讀。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Idle]
          ↓
[擷取欄位: Restricted Processing] → [套用編碼: Restricted Failure]
                                      ↓
[驗證證據: Unrestricted Processing]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Idle` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Restricted Processing` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Restricted Failure` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Unrestricted Processing` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Unrestricted Failure` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Media Verification` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Post-Verification Deallocation` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.27.4、Figure 772；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 從 Figure 772 的七個 states 出發，逐一把 Figures 773–779 的 transition condition 接上。Status 描述結果，state 描述目前位置，事件描述發生的轉折。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 772 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.27.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 七個 state 以 AUSE 分出兩條 processing/failure 路徑，EMVS 接到 verification，再經 deallocation 返回；逐條配合 Figures 773–779 判讀。 |
| 邊界 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

**說明性範例。** SPROG=8000h 表示目前被量測的階段約 50%。進入 Media Verification 後 SPROG=FFFFh，SOS 仍可為 010b；退出驗證進入 deallocation 又從 0 開始。這不是進度倒退。

**常見誤解。** 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Idle, Restricted Processing, Restricted Failure, Unrestricted Processing, Unrestricted Failure, Media Verification, Post-Verification Deallocation

**來源 keyword 索引：** shall

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4, Figure 772, 文件頁 720, PDF 頁 746

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 773: Idle State Transition Conditions</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-773-CLAIM figure-table:BASEBTS-BASE-FIG-773 -->

**SPEC。** Figure 773〈Idle State Transition Conditions〉：Idle 的 A1/B1 分別進 Restricted/Unrestricted Processing；進入時清 SPROG 與 MVCNCLD，不代表 operation 已完成。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Idle 的 A1/B1 分別進 Restricted/Unrestricted Processing；進入時清 SPROG 與 MVCNCLD，不代表 operation 已完成。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: A1]
          ↓
[擷取欄位: AUSE=0] → [套用編碼: B1]
                                      ↓
[驗證證據: AUSE=1]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `A1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AUSE=0` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `B1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AUSE=1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.27.4.1、Figure 773；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 從 Figure 772 的七個 states 出發，逐一把 Figures 773–779 的 transition condition 接上。Status 描述結果，state 描述目前位置，事件描述發生的轉折。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 773 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.27.4.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Idle 的 A1/B1 分別進 Restricted/Unrestricted Processing；進入時清 SPROG 與 MVCNCLD，不代表 operation 已完成。 |
| 邊界 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

**說明性範例。** SPROG=8000h 表示目前被量測的階段約 50%。進入 Media Verification 後 SPROG=FFFFh，SOS 仍可為 010b；退出驗證進入 deallocation 又從 0 開始。這不是進度倒退。

**常見誤解。** 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** A1, AUSE=0, B1, AUSE=1

**來源 keyword 索引：** shall not, shall, should

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.1, Figure 773, 文件頁 721, PDF 頁 747

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 774: Restricted Processing State Transition Conditions</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-774-CLAIM figure-table:BASEBTS-BASE-FIG-774 -->

**SPEC。** Figure 774〈Restricted Processing State Transition Conditions〉：Restricted Processing 成功可 C1 回 Idle 或 F1 進 Verification，取決於 EMVS/MVCNCLD；D1 表示 processing 失敗。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Restricted Processing 成功可 C1 回 Idle 或 F1 進 Verification，取決於 EMVS/MVCNCLD；D1 表示 processing 失敗。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: C1]
          ↓
[擷取欄位: D1] → [套用編碼: F1]
                                      ↓
[驗證證據: EMVS]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `C1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `D1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `F1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `EMVS` | Enter Media Verification State；成功 processing 後要求進入驗證，受方法與 capability 限制。 |
| `MVCNCLD` | Media Verification Canceled；記錄要求的驗證被取消，會影響 processing 後的轉移。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.27.4.2、Figure 774；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 從 Figure 772 的七個 states 出發，逐一把 Figures 773–779 的 transition condition 接上。Status 描述結果，state 描述目前位置，事件描述發生的轉折。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 774 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.27.4.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Restricted Processing 成功可 C1 回 Idle 或 F1 進 Verification，取決於 EMVS/MVCNCLD；D1 表示 processing 失敗。 |
| 邊界 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

**說明性範例。** SPROG=8000h 表示目前被量測的階段約 50%。進入 Media Verification 後 SPROG=FFFFh，SOS 仍可為 010b；退出驗證進入 deallocation 又從 0 開始。這不是進度倒退。

**常見誤解。** 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** C1, D1, F1, EMVS, MVCNCLD

**來源 keyword 索引：** shall

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.2, Figure 774, 文件頁 722, PDF 頁 748

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 775: Restricted Failure State Transition Conditions</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-775-CLAIM figure-table:BASEBTS-BASE-FIG-775 -->

**SPEC。** Figure 775〈Restricted Failure State Transition Conditions〉：Restricted Failure 只有 A2 重進 Restricted Processing 的恢復路徑；Exit Failure Mode 與 AUSE=1 不能取代成功的 restricted retry。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Restricted Failure 只有 A2 重進 Restricted Processing 的恢復路徑；Exit Failure Mode 與 AUSE=1 不能取代成功的 restricted retry。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: A2]
          ↓
[擷取欄位: Restricted Retry] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `A2` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Restricted Retry` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.27.4.3、Figure 775；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 從 Figure 772 的七個 states 出發，逐一把 Figures 773–779 的 transition condition 接上。Status 描述結果，state 描述目前位置，事件描述發生的轉折。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 775 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.27.4.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Restricted Failure 只有 A2 重進 Restricted Processing 的恢復路徑；Exit Failure Mode 與 AUSE=1 不能取代成功的 restricted retry。 |
| 邊界 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

**說明性範例。** SPROG=8000h 表示目前被量測的階段約 50%。進入 Media Verification 後 SPROG=FFFFh，SOS 仍可為 010b；退出驗證進入 deallocation 又從 0 開始。這不是進度倒退。

**常見誤解。** 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** A2, Restricted Retry

**來源 keyword 索引：** shall, should

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.3, Figure 775, 文件頁 724, PDF 頁 750

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 776: Unrestricted Processing State Transition Conditions</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-776-CLAIM figure-table:BASEBTS-BASE-FIG-776 -->

**SPEC。** Figure 776〈Unrestricted Processing State Transition Conditions〉：Unrestricted Processing 的 C2/D2/F2 對應成功回 Idle、失敗、進入 Verification；不是允許一般 I/O 不受限制。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Unrestricted Processing 的 C2/D2/F2 對應成功回 Idle、失敗、進入 Verification；不是允許一般 I/O 不受限制。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: C2]
          ↓
[擷取欄位: D2] → [套用編碼: F2]
                                      ↓
[驗證證據: EMVS]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `C2` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `D2` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `F2` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `EMVS` | Enter Media Verification State；成功 processing 後要求進入驗證，受方法與 capability 限制。 |
| `MVCNCLD` | Media Verification Canceled；記錄要求的驗證被取消，會影響 processing 後的轉移。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.27.4.4、Figure 776；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 從 Figure 772 的七個 states 出發，逐一把 Figures 773–779 的 transition condition 接上。Status 描述結果，state 描述目前位置，事件描述發生的轉折。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 776 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.27.4.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Unrestricted Processing 的 C2/D2/F2 對應成功回 Idle、失敗、進入 Verification；不是允許一般 I/O 不受限制。 |
| 邊界 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

**說明性範例。** SPROG=8000h 表示目前被量測的階段約 50%。進入 Media Verification 後 SPROG=FFFFh，SOS 仍可為 010b；退出驗證進入 deallocation 又從 0 開始。這不是進度倒退。

**常見誤解。** 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** C2, D2, F2, EMVS, MVCNCLD

**來源 keyword 索引：** shall

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.4, Figure 776, 文件頁 725, PDF 頁 751

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 777: Unrestricted Failure State Transition Conditions</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-777-CLAIM figure-table:BASEBTS-BASE-FIG-777 -->

**SPEC。** Figure 777〈Unrestricted Failure State Transition Conditions〉：Unrestricted Failure 可 A3 restricted retry、B2 unrestricted retry，或 E Exit Failure Mode 到 Idle；E 不能當成 sanitize 成功證據。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Unrestricted Failure 可 A3 restricted retry、B2 unrestricted retry，或 E Exit Failure Mode 到 Idle；E 不能當成 sanitize 成功證據。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: A3]
          ↓
[擷取欄位: B2] → [套用編碼: E]
                                      ↓
[驗證證據: Exit Failure Mode]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `A3` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `B2` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `E` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Exit Failure Mode` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.27.4.5、Figure 777；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 從 Figure 772 的七個 states 出發，逐一把 Figures 773–779 的 transition condition 接上。Status 描述結果，state 描述目前位置，事件描述發生的轉折。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 777 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.27.4.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Unrestricted Failure 可 A3 restricted retry、B2 unrestricted retry，或 E Exit Failure Mode 到 Idle；E 不能當成 sanitize 成功證據。 |
| 邊界 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

**說明性範例。** SPROG=8000h 表示目前被量測的階段約 50%。進入 Media Verification 後 SPROG=FFFFh，SOS 仍可為 010b；退出驗證進入 deallocation 又從 0 開始。這不是進度倒退。

**常見誤解。** 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** A3, B2, E, Exit Failure Mode

**來源 keyword 索引：** shall

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.5, Figure 777, 文件頁 727, PDF 頁 753

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 778: Media Verification State Transition Conditions</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-778-CLAIM figure-table:BASEBTS-BASE-FIG-778 -->

**SPEC。** Figure 778〈Media Verification State Transition Conditions〉：G 進 Post-Verification Deallocation：由退出動作、指定 reset 或阻止 verification 的 composition change 觸發；取消驗證須對照 MVCNCLD。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

G 進 Post-Verification Deallocation：由退出動作、指定 reset 或阻止 verification 的 composition change 觸發；取消驗證須對照 MVCNCLD。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: G]
          ↓
[擷取欄位: Exit Media Verification] → [套用編碼: Reset]
                                      ↓
[驗證證據: MVCNCLD]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `G` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Exit Media Verification` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Reset` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MVCNCLD` | Media Verification Canceled；記錄要求的驗證被取消，會影響 processing 後的轉移。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.27.4.6、Figure 778；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 從 Figure 772 的七個 states 出發，逐一把 Figures 773–779 的 transition condition 接上。Status 描述結果，state 描述目前位置，事件描述發生的轉折。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 778 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.27.4.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | G 進 Post-Verification Deallocation：由退出動作、指定 reset 或阻止 verification 的 composition change 觸發；取消驗證須對照 MVCNCLD。 |
| 邊界 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

**說明性範例。** SPROG=8000h 表示目前被量測的階段約 50%。進入 Media Verification 後 SPROG=FFFFh，SOS 仍可為 010b；退出驗證進入 deallocation 又從 0 開始。這不是進度倒退。

**常見誤解。** 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** G, Exit Media Verification, Reset, MVCNCLD

**來源 keyword 索引：** shall

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.6, Figure 778, 文件頁 728, PDF 頁 754

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 779: Post-Verification Deallocation state Transition Conditions</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-779-CLAIM figure-table:BASEBTS-BASE-FIG-779 -->

**SPEC。** Figure 779〈Post-Verification Deallocation state Transition Conditions〉：Deallocation 成功走 H 到 Idle；失敗依原 AUSE 走 I1/I2 到 Failure，FAILS 記 6h，與 processing 失敗的來源區分。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Deallocation 成功走 H 到 Idle；失敗依原 AUSE 走 I1/I2 到 Failure，FAILS 記 6h，與 processing 失敗的來源區分。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: H]
          ↓
[擷取欄位: I1] → [套用編碼: I2]
                                      ↓
[驗證證據: FAILS]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `H` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `I1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `I2` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FAILS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.27.4.7、Figure 779；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 從 Figure 772 的七個 states 出發，逐一把 Figures 773–779 的 transition condition 接上。Status 描述結果，state 描述目前位置，事件描述發生的轉折。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 779 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.27.4.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Deallocation 成功走 H 到 Idle；失敗依原 AUSE 走 I1/I2 到 Failure，FAILS 記 6h，與 processing 失敗的來源區分。 |
| 邊界 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

**說明性範例。** SPROG=8000h 表示目前被量測的階段約 50%。進入 Media Verification 後 SPROG=FFFFh，SOS 仍可為 010b；退出驗證進入 deallocation 又從 0 開始。這不是進度倒退。

**常見誤解。** 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** H, I1, I2, FAILS

**來源 keyword 索引：** shall

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.7, Figure 779, 文件頁 729, PDF 頁 755

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 780: Telemetry Log Example - All Data Areas Populated</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-780-CLAIM figure-table:BASEBTS-BASE-FIG-780 -->

**SPEC。** Figure 780〈Telemetry Log Example - All Data Areas Populated〉：65/1000/30000 的三個 areas 共享前綴；Area 3 包含 Area 1 與 2，不把長度相加。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

65/1000/30000 的三個 areas 共享前綴；Area 3 包含 Area 1 與 2，不把長度相加。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Last Block 65]
          ↓
[擷取欄位: Last Block 1000] → [套用編碼: Last Block 30000]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Last Block 65` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Last Block 1000` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Last Block 30000` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.30、Figure 780；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. Area 是從同一 block 1 起算的不同大小視圖。先解碼 header，再選擇適用且有資料的最後 area；不要把三個 Last Block 數字相加。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 780 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.30 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 65/1000/30000 的三個 areas 共享前綴；Area 3 包含 Area 1 與 2，不把長度相加。 |
| 邊界 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

**說明性範例。** Last Blocks=65/1000/30000 時，Area 3 payload 為 30000×512=15360000 bytes；包含 header 的 log 為 15360512 bytes。0/1000/1000 則表示 Area 1 空、Area 3 沒有超出 Area 2 的新增內容。

**常見誤解。** LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Last Block 65, Last Block 1000, Last Block 30000

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30, Figure 780, 文件頁 736, PDF 頁 762

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 781: Telemetry Log Example - Data Area 2 Populated</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-781-CLAIM figure-table:BASEBTS-BASE-FIG-781 -->

**SPEC。** Figure 781〈Telemetry Log Example - Data Area 2 Populated〉：0/1000/1000 表示 Area 1 空、Area 2 有資料、Area 3 無新增資料；Area 3 的視圖仍涵蓋與 Area 2 相同的 blocks。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

0/1000/1000 表示 Area 1 空、Area 2 有資料、Area 3 無新增資料；Area 3 的視圖仍涵蓋與 Area 2 相同的 blocks。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Last Block 0]
          ↓
[擷取欄位: Last Block 1000] → [套用編碼: Equal Endpoints]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Last Block 0` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Last Block 1000` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Equal Endpoints` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.30、Figure 781；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. Area 是從同一 block 1 起算的不同大小視圖。先解碼 header，再選擇適用且有資料的最後 area；不要把三個 Last Block 數字相加。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 781 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.30 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 0/1000/1000 表示 Area 1 空、Area 2 有資料、Area 3 無新增資料；Area 3 的視圖仍涵蓋與 Area 2 相同的 blocks。 |
| 邊界 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

**說明性範例。** Last Blocks=65/1000/30000 時，Area 3 payload 為 30000×512=15360000 bytes；包含 header 的 log 為 15360512 bytes。0/1000/1000 則表示 Area 1 空、Area 3 沒有超出 Area 2 的新增內容。

**常見誤解。** LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Last Block 0, Last Block 1000, Equal Endpoints

**來源 keyword 索引：** may

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30, Figure 781, 文件頁 737, PDF 頁 763

</details>

<a id="section-dependency"></a>

### 引用相依 Figure（位於主章節範圍外）

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 11: Protection Information Field Definition</strong></summary>

<!-- claim:BASEBTS-NVMCS-FIG-011-CLAIM figure-table:BASEBTS-NVMCS-FIG-011 -->

**SPEC。** Figure 11〈Protection Information Field Definition〉：PRACT 處理 PI 傳遞，PRCHK 的三個 bits 分別要求 Guard/Application/Reference Tag checking；Media Verification 明確要求 PRCHK=000b。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

PRACT 處理 PI 傳遞，PRCHK 的三個 bits 分別要求 Guard/Application/Reference Tag checking；Media Verification 明確要求 PRCHK=000b。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PRACT]
          ↓
[擷取欄位: PRCHK] → [套用編碼: GRDCHK]
                                      ↓
[驗證證據: ATCHK]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PRACT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PRCHK` | Protection Information Check；三個 bits 分別要求 guard、application tag、reference tag 檢查；驗證讀取設 000b。 |
| `GRDCHK` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ATCHK` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `RTCHK` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-NVM-CS-1.3、§2.1.5、Figure 11；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 command allowlist 與 NVM Read 特例分開判斷。Host 先辨識 target/state，再確認 PI checking 與 allocation，不能把平常 read 的處理完全套入驗證狀態。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 11 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.1.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | PRACT 處理 PI 傳遞，PRCHK 的三個 bits 分別要求 Guard/Application/Reference Tag checking；Media Verification 明確要求 PRCHK=000b。 |
| 邊界 | 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。 |

**說明性範例。** 驗證讀取 PRCHK=000b、STC=0，所有 allocated LBAs 都能讀取，且沒有其他 abort 原因時，預期 Successful Media Verification Read。只要請求 PI checking，預期分支即改為 Invalid Field in Command。

**常見誤解。** 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** PRACT, PRCHK, GRDCHK, ATCHK, RTCHK

**來源 keyword 索引：** shall not, shall, may, optional

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5, Figure 11, 文件頁 21-22, PDF 頁 21-22

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 12: Storage Tag Check Definition</strong></summary>

<!-- claim:BASEBTS-NVMCS-FIG-012-CLAIM figure-table:BASEBTS-NVMCS-FIG-012 -->

**SPEC。** Figure 12〈Storage Tag Check Definition〉：此處 STC 是 Storage Tag Check，不是另一報告的 Self-test Code；驗證 Read 要求 STC=0。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

此處 STC 是 Storage Tag Check，不是另一報告的 Self-test Code；驗證 Read 要求 STC=0。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: STC]
          ↓
[擷取欄位: Storage Tag] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `STC` | Storage Tag Check；本報告指 NVM Read 的 storage tag 檢查，驗證讀取設 0。 |
| `Storage Tag` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-NVM-CS-1.3、§2.1.5、Figure 12；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 command allowlist 與 NVM Read 特例分開判斷。Host 先辨識 target/state，再確認 PI checking 與 allocation，不能把平常 read 的處理完全套入驗證狀態。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 12 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.1.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 此處 STC 是 Storage Tag Check，不是另一報告的 Self-test Code；驗證 Read 要求 STC=0。 |
| 邊界 | 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。 |

**說明性範例。** 驗證讀取 PRCHK=000b、STC=0，所有 allocated LBAs 都能讀取，且沒有其他 abort 原因時，預期 Successful Media Verification Read。只要請求 PI checking，預期分支即改為 Invalid Field in Command。

**常見誤解。** 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** STC, Storage Tag

**來源 keyword 索引：** shall not, shall, may, optional

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5, Figure 12, 文件頁 22, PDF 頁 22

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 36: Offset 0h: CAP - Controller Capabilities</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-036-CLAIM figure-table:BASEBTS-BASE-FIG-036 -->

**SPEC。** Figure 36〈Offset 0h: CAP - Controller Capabilities〉：先查 BPS 再使用 Boot properties；支援 Boot 不代表已啟用 controller。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

先查 BPS 再使用 Boot properties；支援 Boot 不代表已啟用 controller。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CAP.BPS]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CAP.BPS` | Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.BPS 進一步指定其中的 BPS 子欄位。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§3.1.4.1、Figure 36；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 先問 controller 是否已建立 Admin command 環境，再選 property 或 LID 15h。兩條路徑讀同一類 Boot 內容，但回傳格式與狀態觀察點不同。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

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
| 規則 | 先查 BPS 再使用 Boot properties；支援 Boot 不代表已啟用 controller。 |
| 邊界 | 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。 |

**說明性範例。** BPSZ=2 的 LID 15h 包含 262144 bytes 的 Boot data，加上 16-byte header，共 262160 bytes。讀 BP1 並不把 BP1 設為 active；讀 log 也不會推進 property 的 BRS。

**常見誤解。** 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** CAP.BPS

**來源 keyword 索引：** shall not, shall, should, may, optional, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, 文件頁 55-58, PDF 頁 81-84

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 49: Offset 40h: BPINFO - Boot Partition Information</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-049-CLAIM figure-table:BASEBTS-BASE-FIG-049 -->

**SPEC。** Figure 49〈Offset 40h: BPINFO - Boot Partition Information〉：ABPID 指 active partition，BPSZ 使用 128 KiB，BRS 依 00b/01b/10b/11b 區分未請求、傳輸中、成功與錯誤。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

ABPID 指 active partition，BPSZ 使用 128 KiB，BRS 依 00b/01b/10b/11b 區分未請求、傳輸中、成功與錯誤。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ABPID]
          ↓
[擷取欄位: BPSZ] → [套用編碼: BRS]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ABPID` | Active Boot Partition ID；指出目前選為啟動映像的 partition。 |
| `BPSZ` | Boot Partition Size；每單位 128 KiB。 |
| `BRS` | Boot Read Status；00b 未請求、01b 進行中、10b 成功、11b 錯誤。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§3.1.4.13、Figure 49；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 先問 controller 是否已建立 Admin command 環境，再選 property 或 LID 15h。兩條路徑讀同一類 Boot 內容，但回傳格式與狀態觀察點不同。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 49 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.13 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | ABPID 指 active partition，BPSZ 使用 128 KiB，BRS 依 00b/01b/10b/11b 區分未請求、傳輸中、成功與錯誤。 |
| 邊界 | 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。 |

**說明性範例。** BPSZ=2 的 LID 15h 包含 262144 bytes 的 Boot data，加上 16-byte header，共 262160 bytes。讀 BP1 並不把 BP1 設為 active；讀 log 也不會推進 property 的 BRS。

**常見誤解。** 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** ABPID, BPSZ, BRS

**來源 keyword 索引：** shall not, shall, optional, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.13, Figure 49, 文件頁 69, PDF 頁 95

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 50: Offset 44h: BPRSEL - Boot Partition Read Select</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-050-CLAIM figure-table:BASEBTS-BASE-FIG-050 -->

**SPEC。** Figure 50〈Offset 44h: BPRSEL - Boot Partition Read Select〉：BPRSEL bit 31 是 BPID、bit 30 保留，[29:10] 是以 4 KiB 計的 BPROF，[9:0] 是以 4 KiB 計的 BPRSZ；寫入會觸發讀取。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

BPRSEL bit 31 是 BPID、bit 30 保留，[29:10] 是以 4 KiB 計的 BPROF，[9:0] 是以 4 KiB 計的 BPRSZ；寫入會觸發讀取。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: BPID]
          ↓
[擷取欄位: BPRSZ] → [套用編碼: BPROF]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `BPID` | Boot Partition Identifier；選取 0 或 1，與目前 active partition 分開。 |
| `BPRSZ` | Boot Partition Read Size；以 4 KiB 為單位，不能套用 BPSZ 的單位。 |
| `BPROF` | Boot Partition Read Offset；BPRSEL bits 29:10，以 4 KiB 為單位；bit 30 保留。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§3.1.4.14、Figure 50；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 先問 controller 是否已建立 Admin command 環境，再選 property 或 LID 15h。兩條路徑讀同一類 Boot 內容，但回傳格式與狀態觀察點不同。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 50 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.14 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | BPRSEL bit 31 是 BPID、bit 30 保留，[29:10] 是以 4 KiB 計的 BPROF，[9:0] 是以 4 KiB 計的 BPRSZ；寫入會觸發讀取。 |
| 邊界 | 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。 |

**說明性範例。** BPSZ=2 的 LID 15h 包含 262144 bytes 的 Boot data，加上 16-byte header，共 262160 bytes。讀 BP1 並不把 BP1 設為 active；讀 log 也不會推進 property 的 BRS。

**常見誤解。** 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** BPID, BPRSZ, BPROF

**來源 keyword 索引：** shall not, shall, optional, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 50, 文件頁 69-70, PDF 頁 95-96

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 51: Offset 48h: BPMBL - Boot Partition Memory Buffer Location</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-051-CLAIM figure-table:BASEBTS-BASE-FIG-051 -->

**SPEC。** Figure 51〈Offset 48h: BPMBL - Boot Partition Memory Buffer Location〉：BPMBL[63:12] 提供 Boot Memory Buffer 基底位址，低 12 bits 保留；先確認 host buffer 的連續性與對齊。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

BPMBL[63:12] 提供 Boot Memory Buffer 基底位址，低 12 bits 保留；先確認 host buffer 的連續性與對齊。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: BMBBA]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `BMBBA` | Boot Memory Buffer Base Address；BPMBL bits 63:12，低 12 bits 保留。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§3.1.4.15、Figure 51；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 先問 controller 是否已建立 Admin command 環境，再選 property 或 LID 15h。兩條路徑讀同一類 Boot 內容，但回傳格式與狀態觀察點不同。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 51 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.4.15 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | BPMBL[63:12] 提供 Boot Memory Buffer 基底位址，低 12 bits 保留；先確認 host buffer 的連續性與對齊。 |
| 邊界 | 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。 |

**說明性範例。** BPSZ=2 的 LID 15h 包含 262144 bytes 的 Boot data，加上 16-byte header，共 262160 bytes。讀 BP1 並不把 BP1 設為 active；讀 log 也不會推進 property 的 BRS。

**常見誤解。** 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** BMBBA

**來源 keyword 索引：** shall not, shall, optional, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.15, Figure 51, 文件頁 70, PDF 頁 96

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 144: NVM Subsystem Sanitize Operations and Format NVM Command - Admin</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-144-CLAIM figure-table:BASEBTS-BASE-FIG-144 -->

**SPEC。** Figure 144〈NVM Subsystem Sanitize Operations and Format NVM Command - Admin〉：比較 Sanitize 欄的命令白名單及各命令限制；Boot log 可讀，Telemetry 07h/08h 未被列入。只使用通用與 memory-based 命令列。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

比較 Sanitize 欄的命令白名單及各命令限制；Boot log 可讀，Telemetry 07h/08h 未被列入。只使用通用與 memory-based 命令列。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Get Log Page]
          ↓
[擷取欄位: Boot Partition] → [套用編碼: Sanitize Status]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Get Log Page` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Boot Partition` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Sanitize Status` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.1.1、Figure 144；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 command allowlist 與 NVM Read 特例分開判斷。Host 先辨識 target/state，再確認 PI checking 與 allocation，不能把平常 read 的處理完全套入驗證狀態。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 144 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 比較 Sanitize 欄的命令白名單及各命令限制；Boot log 可讀，Telemetry 07h/08h 未被列入。只使用通用與 memory-based 命令列。 |
| 邊界 | 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。 |

**說明性範例。** 驗證讀取 PRCHK=000b、STC=0，所有 allocated LBAs 都能讀取，且沒有其他 abort 原因時，預期 Successful Media Verification Read。只要請求 PI checking，預期分支即改為 Invalid Field in Command。

**常見誤解。** 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Get Log Page, Boot Partition, Sanitize Status

**來源 keyword 索引：** shall, should, may

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.1.1, Figure 144, 文件頁 178-179, PDF 頁 204-205

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 145: Namespace Sanitize Operations - Admin Command Restrictions, All Controllers</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-145-CLAIM figure-table:BASEBTS-BASE-FIG-145 -->

**SPEC。** Figure 145〈Namespace Sanitize Operations - Admin Command Restrictions, All Controllers〉：這張表約束所有 controllers：例如拒絕刪除正被 sanitize 的 namespace，並限制 firmware update；先套用 target 關係再判斷 status。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

這張表約束所有 controllers：例如拒絕刪除正被 sanitize 的 namespace，並限制 firmware update；先套用 target 關係再判斷 status。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Set Features]
          ↓
[擷取欄位: Namespace Management] → [套用編碼: Firmware Commit]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Set Features` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Namespace Management` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Firmware Commit` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.1.2、Figure 145；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 command allowlist 與 NVM Read 特例分開判斷。Host 先辨識 target/state，再確認 PI checking 與 allocation，不能把平常 read 的處理完全套入驗證狀態。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 145 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.1.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 這張表約束所有 controllers：例如拒絕刪除正被 sanitize 的 namespace，並限制 firmware update；先套用 target 關係再判斷 status。 |
| 邊界 | 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。 |

**說明性範例。** 驗證讀取 PRCHK=000b、STC=0，所有 allocated LBAs 都能讀取，且沒有其他 abort 原因時，預期 Successful Media Verification Read。只要請求 PI checking，預期分支即改為 Invalid Field in Command。

**常見誤解。** 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Set Features, Namespace Management, Firmware Commit

**來源 keyword 索引：** shall

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.1.2, Figure 145, 文件頁 179-180, PDF 頁 205-206

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 146: Namespace Sanitize Operations - Admin Command Restrictions if Sanitizing</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-146-CLAIM figure-table:BASEBTS-BASE-FIG-146 -->

**SPEC。** Figure 146〈Namespace Sanitize Operations - Admin Command Restrictions if Sanitizing〉：這張表補充有 attached sanitizing namespace 的 controllers；不能把所有 controller 與只有 attached controller 的限制混為一談。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

這張表補充有 attached sanitizing namespace 的 controllers；不能把所有 controller 與只有 attached controller 的限制混為一談。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Attached Namespace]
          ↓
[擷取欄位: Admin command restrictions] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Attached Namespace` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Admin command restrictions` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.1.2、Figure 146；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 command allowlist 與 NVM Read 特例分開判斷。Host 先辨識 target/state，再確認 PI checking 與 allocation，不能把平常 read 的處理完全套入驗證狀態。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 146 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.1.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 這張表補充有 attached sanitizing namespace 的 controllers；不能把所有 controller 與只有 attached controller 的限制混為一談。 |
| 邊界 | 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。 |

**說明性範例。** 驗證讀取 PRCHK=000b、STC=0，所有 allocated LBAs 都能讀取，且沒有其他 abort 原因時，預期 Successful Media Verification Read。只要請求 PI checking，預期分支即改為 Invalid Field in Command。

**常見誤解。** 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Attached Namespace, Admin command restrictions

**來源 keyword 索引：** should not, shall, should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.1.2, Figure 146, 文件頁 180-181, PDF 頁 206-207

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 151: Asynchronous Event Request - Completion Queue Entry Dword 0</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-151-CLAIM figure-table:BASEBTS-BASE-FIG-151 -->

**SPEC。** Figure 151〈Asynchronous Event Request - Completion Queue Entry Dword 0〉：CQE DW0[23:16] 是 LID、[15:8] 是 AEI、[2:0] 是 AET；Sanitize 用 LID 81h/AET 110b，Telemetry 使用 Notice 類型。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CQE DW0[23:16] 是 LID、[15:8] 是 AEI、[2:0] 是 AET；Sanitize 用 LID 81h/AET 110b，Telemetry 使用 Notice 類型。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LID]
          ↓
[擷取欄位: AEI] → [套用編碼: AET]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LID` | Log Page Identifier，Get Log Page command 用來選擇 log page 的欄位。 |
| `AEI` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `AET` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.2.1、Figure 151；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 從 Figure 772 的七個 states 出發，逐一把 Figures 773–779 的 transition condition 接上。Status 描述結果，state 描述目前位置，事件描述發生的轉折。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 151 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | CQE DW0[23:16] 是 LID、[15:8] 是 AEI、[2:0] 是 AET；Sanitize 用 LID 81h/AET 110b，Telemetry 使用 Notice 類型。 |
| 邊界 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

**說明性範例。** SPROG=8000h 表示目前被量測的階段約 50%。進入 Media Verification 後 SPROG=FFFFh，SOS 仍可為 010b；退出驗證進入 deallocation 又從 0 開始。這不是進度倒退。

**常見誤解。** 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** LID, AEI, AET

**來源 keyword 索引：** shall not, shall, should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 151, 文件頁 184-185, PDF 頁 210-211

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 152: Asynchronous Event Request - Completion Queue Entry Dword 1</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-152-CLAIM figure-table:BASEBTS-BASE-FIG-152 -->

**SPEC。** Figure 152〈Asynchronous Event Request - Completion Queue Entry Dword 1〉：AER DW1 是 event-specific parameter；Sanitize 以 0h 指 subsystem，以 NSID 指 namespace，不能把它讀成進度。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

AER DW1 是 event-specific parameter；Sanitize 以 0h 指 subsystem，以 NSID 指 namespace，不能把它讀成進度。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: EVNTSP]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `EVNTSP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.2.1、Figure 152；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 從 Figure 772 的七個 states 出發，逐一把 Figures 773–779 的 transition condition 接上。Status 描述結果，state 描述目前位置，事件描述發生的轉折。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 152 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | AER DW1 是 event-specific parameter；Sanitize 以 0h 指 subsystem，以 NSID 指 namespace，不能把它讀成進度。 |
| 邊界 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

**說明性範例。** SPROG=8000h 表示目前被量測的階段約 50%。進入 Media Verification 後 SPROG=FFFFh，SOS 仍可為 010b；退出驗證進入 deallocation 又從 0 開始。這不是進度倒退。

**常見誤解。** 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** EVNTSP

**來源 keyword 索引：** shall not, shall, should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 152, 文件頁 185, PDF 頁 211

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 155: Asynchronous Event Information - Notice</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-155-CLAIM figure-table:BASEBTS-BASE-FIG-155 -->

**SPEC。** Figure 155〈Asynchronous Event Information - Notice〉：只取 Telemetry Log Changed Notice：用事件定位 08h，再讀 log；事件不包含診斷 payload。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

只取 Telemetry Log Changed Notice：用事件定位 08h，再讀 log；事件不包含診斷 payload。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Telemetry Log Changed]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Telemetry Log Changed` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.2.1、Figure 155；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 07h 的 create 與後續讀取分開；08h 的 capture 由 controller 決定。Host 對兩者都要驗證 generation，並分清事件 acknowledgement 與刪除 payload。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 155 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 只取 Telemetry Log Changed Notice：用事件定位 08h，再讀 log；事件不包含診斷 payload。 |
| 邊界 | 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。 |

**說明性範例。** 讀取前 generation=2Ah，讀完變成 2Bh，這批 blocks 不能當成同一 capture 的一致資料。若值保持 2Ah 但 TCDA 被其他 host 清成 0，08h 收集仍需依流程檢查該競態。

**常見誤解。** 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Telemetry Log Changed

**來源 keyword 索引：** shall not, shall, should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 155, 文件頁 186-189, PDF 頁 212-215

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 156: Asynchronous Event Information - I/O Command Specific Status</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-156-CLAIM figure-table:BASEBTS-BASE-FIG-156 -->

**SPEC。** Figure 156〈Asynchronous Event Information - I/O Command Specific Status〉：01h/02h/03h 三種 Sanitize AEI 必須與 SOS/SANS 一起看；Entered Media Verification 不是 operation 全部完成。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

01h/02h/03h 三種 Sanitize AEI 必須與 SOS/SANS 一起看；Entered Media Verification 不是 operation 全部完成。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Sanitize Operation Completed]
          ↓
[擷取欄位: Unexpected Deallocation] → [套用編碼: Entered Media Verification]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Sanitize Operation Completed` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Unexpected Deallocation` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Entered Media Verification` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.2.1、Figure 156；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 從 Figure 772 的七個 states 出發，逐一把 Figures 773–779 的 transition condition 接上。Status 描述結果，state 描述目前位置，事件描述發生的轉折。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 156 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 01h/02h/03h 三種 Sanitize AEI 必須與 SOS/SANS 一起看；Entered Media Verification 不是 operation 全部完成。 |
| 邊界 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

**說明性範例。** SPROG=8000h 表示目前被量測的階段約 50%。進入 Media Verification 後 SPROG=FFFFh，SOS 仍可為 010b；退出驗證進入 deallocation 又從 0 開始。這不是進度倒退。

**常見誤解。** 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Sanitize Operation Completed, Unexpected Deallocation, Entered Media Verification

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 156, 文件頁 189-190, PDF 頁 215-216

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 187: Firmware Commit - Command Dword 10</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-187-CLAIM figure-table:BASEBTS-BASE-FIG-187 -->

**SPEC。** Figure 187〈Firmware Commit - Command Dword 10〉：Boot 更新只取 BPID 與 CA=110b/111b：前者替換 partition 內容，後者更新 active ID；兩個動作分開。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Boot 更新只取 BPID 與 CA=110b/111b：前者替換 partition 內容，後者更新 active ID；兩個動作分開。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: BPID]
          ↓
[擷取欄位: CA] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `BPID` | Boot Partition Identifier；選取 0 或 1，與目前 active partition 分開。 |
| `CA` | Commit Action，Firmware Commit 中選擇 replace、activate 與 reset policy 的欄位。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.9、Figure 187；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 187 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.9 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Boot 更新只取 BPID 與 CA=110b/111b：前者替換 partition 內容，後者更新 active ID；兩個動作分開。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** BPID, CA

**來源 keyword 索引：** shall, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, Figure 187, 文件頁 203, PDF 頁 229

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 188: Firmware Commit - Completion Queue Entry Dword 0</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-188-CLAIM figure-table:BASEBTS-BASE-FIG-188 -->

**SPEC。** Figure 188〈Firmware Commit - Completion Queue Entry Dword 0〉：MUD 是重疊更新偵測的 completion 證據；仍需遵守單一 image sequence 的 controller/endpoint 邊界。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

MUD 是重疊更新偵測的 completion 證據；仍需遵守單一 image sequence 的 controller/endpoint 邊界。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MUD]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MUD` | Multiple Update Detected，completion 中指出 controller 偵測到 overlapping firmware update sequence 的 bit。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.9.1、Figure 188；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 188 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.9.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | MUD 是重疊更新偵測的 completion 證據；仍需遵守單一 image sequence 的 controller/endpoint 邊界。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** MUD

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 188, 文件頁 204, PDF 頁 230

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 189: Firmware Commit - Command Specific Status Values</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-189-CLAIM figure-table:BASEBTS-BASE-FIG-189 -->

**SPEC。** Figure 189〈Firmware Commit - Command Specific Status Values〉：Boot Partition Write Prohibited 指向保護狀態；Invalid Firmware Image 指向 image/sequence 驗證。分辨 status 後才選重試步驟。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Boot Partition Write Prohibited 指向保護狀態；Invalid Firmware Image 指向 image/sequence 驗證。分辨 status 後才選重試步驟。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Boot Partition Write Prohibited]
          ↓
[擷取欄位: Invalid Firmware Image] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Boot Partition Write Prohibited` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Invalid Firmware Image` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.9.1、Figure 189；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 189 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.9.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Boot Partition Write Prohibited 指向保護狀態；Invalid Firmware Image 指向 image/sequence 驗證。分辨 status 後才選重試步驟。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Boot Partition Write Prohibited, Invalid Firmware Image

**來源 keyword 索引：** should not, shall, should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 189, 文件頁 204-205, PDF 頁 230-231

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 190: Firmware Image Download - Data Pointer</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-190-CLAIM figure-table:BASEBTS-BASE-FIG-190 -->

**SPEC。** Figure 190〈Firmware Image Download - Data Pointer〉：Download 的 DPTR 指向此次 image portion 的 host buffer；資料指標不代表目標 Boot Partition 位址。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Download 的 DPTR 指向此次 image portion 的 host buffer；資料指標不代表目標 Boot Partition 位址。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DPTR]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DPTR` | Data Pointer，SQE 中指出 command data buffer 的欄位。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.10、Figure 190；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 190 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.10 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Download 的 DPTR 指向此次 image portion 的 host buffer；資料指標不代表目標 Boot Partition 位址。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** DPTR

**來源 keyword 索引：** should not, shall, should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 190, 文件頁 205, PDF 頁 231

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 191: Firmware Image Download - Command Dword 10</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-191-CLAIM figure-table:BASEBTS-BASE-FIG-191 -->

**SPEC。** Figure 191〈Firmware Image Download - Command Dword 10〉：NUMD 是此次 portion 的 zero-based dword count：512 bytes 編為 127，並須另外符合 Download 的 alignment/granularity 規則。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

NUMD 是此次 portion 的 zero-based dword count：512 bytes 編為 127，並須另外符合 Download 的 alignment/granularity 規則。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NUMD]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NUMD` | Number of Dwords，0's-based transfer dword count；實際 bytes = (NUMD + 1) × 4。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.10、Figure 191；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 191 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.10 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | NUMD 是此次 portion 的 zero-based dword count：512 bytes 編為 127，並須另外符合 Download 的 alignment/granularity 規則。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** NUMD

**來源 keyword 索引：** should not, shall, should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 191, 文件頁 205, PDF 頁 231

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 192: Firmware Image Download - Command Dword 11</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-192-CLAIM figure-table:BASEBTS-BASE-FIG-192 -->

**SPEC。** Figure 192〈Firmware Image Download - Command Dword 11〉：OFST 用 dword 表示 image offset；Boot image 需從開頭依序傳送，不能借用一般 firmware portion 的其他排序假設。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

OFST 用 dword 表示 image offset；Boot image 需從開頭依序傳送，不能借用一般 firmware portion 的其他排序假設。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: OFST]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `OFST` | Offset，Firmware Image Download 中以 dword 為單位的 image-relative offset。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.10、Figure 192；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 192 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.10 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | OFST 用 dword 表示 image offset；Boot image 需從開頭依序傳送，不能借用一般 firmware portion 的其他排序假設。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** OFST

**來源 keyword 索引：** shall not, shall, may

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 192, 文件頁 206, PDF 頁 232

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 193: Firmware Image Download - Command Specific Status Values</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-193-CLAIM figure-table:BASEBTS-BASE-FIG-193 -->

**SPEC。** Figure 193〈Firmware Image Download - Command Specific Status Values〉：Overlapping Range 是 download portion 重疊的 status；保留每段 offset 與 length 才能重建錯誤區間。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Overlapping Range 是 download portion 重疊的 status；保留每段 offset 與 length 才能重建錯誤區間。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Overlapping Range]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Overlapping Range` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.10、Figure 193；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 193 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.10 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Overlapping Range 是 download portion 重疊的 status；保留每段 offset 與 length 才能重建錯誤區間。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Overlapping Range

**來源 keyword 索引：** shall not, shall, may

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 193, 文件頁 206, PDF 頁 232

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 198: Get Features - Command Dword 10</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-198-CLAIM figure-table:BASEBTS-BASE-FIG-198 -->

**SPEC。** Figure 198〈Get Features - Command Dword 10〉：Get Features 以 FID 指定 feature，SEL 指定 current/default/saved/capabilities；FID 85h、17h 的值與 capability 不可混讀。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Get Features 以 FID 指定 feature，SEL 指定 current/default/saved/capabilities；FID 85h、17h 的值與 capability 不可混讀。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: FID]
          ↓
[擷取欄位: SEL] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `FID` | Feature Identifier，Get／Set Features 用來選擇功能的 8-bit identifier。 |
| `SEL` | Select，Get Features 用來選 current、default、saved 或 supported-capabilities view 的欄位。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.12、Figure 198；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

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
| 規則 | Get Features 以 FID 指定 feature，SEL 指定 current/default/saved/capabilities；FID 85h、17h 的值與 capability 不可混讀。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** FID, SEL

**來源 keyword 索引：** shall, may, optional, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 198, 文件頁 209-210, PDF 頁 235-236

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 199: Get Features - Command Dword 14</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-199-CLAIM figure-table:BASEBTS-BASE-FIG-199 -->

**SPEC。** Figure 199〈Get Features - Command Dword 14〉：CDW14 的 UUID Index 是共用 feature 介面的一部分；本報告的標準 FID 不需自創 vendor UUID 對應。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW14 的 UUID Index 是共用 feature 介面的一部分；本報告的標準 FID 不需自創 vendor UUID 對應。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: UUID Index]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `UUID Index` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.12、Figure 199；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

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
| 規則 | CDW14 的 UUID Index 是共用 feature 介面的一部分；本報告的標準 FID 不需自創 vendor UUID 對應。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** UUID Index

**來源 keyword 索引：** shall, may, optional, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 199, 文件頁 210, PDF 頁 236

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 201: Completion Queue Entry Dword 0 when Select is set to 11b</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-201-CLAIM figure-table:BASEBTS-BASE-FIG-201 -->

**SPEC。** Figure 201〈Completion Queue Entry Dword 0 when Select is set to 11b〉：SEL=011b 回傳的 bits 2/1/0 分別是 changeable/namespace-specific/saveable；不是 BP0WPS 或 NODRM 的當前值。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

SEL=011b 回傳的 bits 2/1/0 分別是 changeable/namespace-specific/saveable；不是 BP0WPS 或 NODRM 的當前值。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

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

1. 確認 NVME-BASE-2.4、§5.2.12.2、Figure 201；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

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
| 規則 | SEL=011b 回傳的 bits 2/1/0 分別是 changeable/namespace-specific/saveable；不是 BP0WPS 或 NODRM 的當前值。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** CHANG, NSSPEC, SVBL

**來源 keyword 索引：** may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, Figure 201, 文件頁 212, PDF 頁 238

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 203: Get Log Page - Data Pointer</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-203-CLAIM figure-table:BASEBTS-BASE-FIG-203 -->

**SPEC。** Figure 203〈Get Log Page - Data Pointer〉：Get Log Page 的 data pointer 指向接收 buffer；buffer 必須容納 encoded NUMD 所要求的資料。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Get Log Page 的 data pointer 指向接收 buffer；buffer 必須容納 encoded NUMD 所要求的資料。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DPTR]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DPTR` | Data Pointer，SQE 中指出 command data buffer 的欄位。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.13、Figure 203；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. Area 是從同一 block 1 起算的不同大小視圖。先解碼 header，再選擇適用且有資料的最後 area；不要把三個 Last Block 數字相加。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 203 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Get Log Page 的 data pointer 指向接收 buffer；buffer 必須容納 encoded NUMD 所要求的資料。 |
| 邊界 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

**說明性範例。** Last Blocks=65/1000/30000 時，Area 3 payload 為 30000×512=15360000 bytes；包含 header 的 log 為 15360512 bytes。0/1000/1000 則表示 Area 1 空、Area 3 沒有超出 Area 2 的新增內容。

**常見誤解。** LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** DPTR

**來源 keyword 索引：** shall, should, optional, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 203, 文件頁 213, PDF 頁 239

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 204: Get Log Page - Command Dword 10</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-204-CLAIM figure-table:BASEBTS-BASE-FIG-204 -->

**SPEC。** Figure 204〈Get Log Page - Command Dword 10〉：CDW10[7:0]=LID，[14:8]=LSP，[15]=RAE，[31:16]=NUMDL；LID 決定 LSP 是 Boot BPID 或 Telemetry capture controls。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW10[7:0]=LID，[14:8]=LSP，[15]=RAE，[31:16]=NUMDL；LID 決定 LSP 是 Boot BPID 或 Telemetry capture controls。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LID]
          ↓
[擷取欄位: LSP] → [套用編碼: RAE]
                                      ↓
[驗證證據: NUMDL]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LID` | Log Page Identifier，Get Log Page command 用來選擇 log page 的欄位。 |
| `LSP` | Log Specific Field，意義由所選 log page 定義的 command selector。 |
| `RAE` | Retain Asynchronous Event；Telemetry 收集中用 1 保留通知狀態，完成後用 0 acknowledgement。 |
| `NUMDL` | Number of Dwords Lower，Get Log Page 的 NUMD 低 16 bits。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.13、Figure 204；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 07h 的 create 與後續讀取分開；08h 的 capture 由 controller 決定。Host 對兩者都要驗證 generation，並分清事件 acknowledgement 與刪除 payload。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 204 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | CDW10[7:0]=LID，[14:8]=LSP，[15]=RAE，[31:16]=NUMDL；LID 決定 LSP 是 Boot BPID 或 Telemetry capture controls。 |
| 邊界 | 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。 |

**說明性範例。** 讀取前 generation=2Ah，讀完變成 2Bh，這批 blocks 不能當成同一 capture 的一致資料。若值保持 2Ah 但 TCDA 被其他 host 清成 0，08h 收集仍需依流程檢查該競態。

**常見誤解。** 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** LID, LSP, RAE, NUMDL

**來源 keyword 索引：** shall, should, optional, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 204, 文件頁 213, PDF 頁 239

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 205: Get Log Page - Command Dword 11</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-205-CLAIM figure-table:BASEBTS-BASE-FIG-205 -->

**SPEC。** Figure 205〈Get Log Page - Command Dword 11〉：NUMDU 與 NUMDL 組成 zero-based dword count；LSI 是另一個 log-specific selector，不是 LSP。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

NUMDU 與 NUMDL 組成 zero-based dword count；LSI 是另一個 log-specific selector，不是 LSP。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NUMDU]
          ↓
[擷取欄位: LSI] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NUMDU` | Number of Dwords Upper，Get Log Page 的 NUMD 高 16 bits。 |
| `LSI` | Log Specific Identifier，意義由所選 log page 定義的 identifier。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.13、Figure 205；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. Area 是從同一 block 1 起算的不同大小視圖。先解碼 header，再選擇適用且有資料的最後 area；不要把三個 Last Block 數字相加。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 205 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | NUMDU 與 NUMDL 組成 zero-based dword count；LSI 是另一個 log-specific selector，不是 LSP。 |
| 邊界 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

**說明性範例。** Last Blocks=65/1000/30000 時，Area 3 payload 為 30000×512=15360000 bytes；包含 header 的 log 為 15360512 bytes。0/1000/1000 則表示 Area 1 空、Area 3 沒有超出 Area 2 的新增內容。

**常見誤解。** LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** NUMDU, LSI

**來源 keyword 索引：** shall, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 205, 文件頁 214, PDF 頁 240

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 206: Get Log Page - Command Dword 12</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-206-CLAIM figure-table:BASEBTS-BASE-FIG-206 -->

**SPEC。** Figure 206〈Get Log Page - Command Dword 12〉：LPO 低 32 bits 位於 CDW12；Telemetry byte offset 必須以 512-byte blocks 對齊。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

LPO 低 32 bits 位於 CDW12；Telemetry byte offset 必須以 512-byte blocks 對齊。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LPOL]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LPOL` | Log Page Offset Lower，Get Log Page byte offset 的低 32 bits。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.13、Figure 206；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. Area 是從同一 block 1 起算的不同大小視圖。先解碼 header，再選擇適用且有資料的最後 area；不要把三個 Last Block 數字相加。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 206 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | LPO 低 32 bits 位於 CDW12；Telemetry byte offset 必須以 512-byte blocks 對齊。 |
| 邊界 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

**說明性範例。** Last Blocks=65/1000/30000 時，Area 3 payload 為 30000×512=15360000 bytes；包含 header 的 log 為 15360512 bytes。0/1000/1000 則表示 Area 1 空、Area 3 沒有超出 Area 2 的新增內容。

**常見誤解。** LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** LPOL

**來源 keyword 索引：** shall, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 206, 文件頁 214, PDF 頁 240

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 207: Get Log Page - Command Dword 13</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-207-CLAIM figure-table:BASEBTS-BASE-FIG-207 -->

**SPEC。** Figure 207〈Get Log Page - Command Dword 13〉：LPO 高 32 bits 位於 CDW13；不可先截斷為 32-bit 再計算大型 log 的 offset。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

LPO 高 32 bits 位於 CDW13；不可先截斷為 32-bit 再計算大型 log 的 offset。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LPOU]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LPOU` | Log Page Offset Upper，Get Log Page byte offset 的高 32 bits。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.13、Figure 207；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. Area 是從同一 block 1 起算的不同大小視圖。先解碼 header，再選擇適用且有資料的最後 area；不要把三個 Last Block 數字相加。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 207 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | LPO 高 32 bits 位於 CDW13；不可先截斷為 32-bit 再計算大型 log 的 offset。 |
| 邊界 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

**說明性範例。** Last Blocks=65/1000/30000 時，Area 3 payload 為 30000×512=15360000 bytes；包含 header 的 log 為 15360512 bytes。0/1000/1000 則表示 Area 1 空、Area 3 沒有超出 Area 2 的新增內容。

**常見誤解。** LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** LPOU

**來源 keyword 索引：** shall, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 207, 文件頁 214, PDF 頁 240

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 208: Get Log Page - Command Dword 14</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-208-CLAIM figure-table:BASEBTS-BASE-FIG-208 -->

**SPEC。** Figure 208〈Get Log Page - Command Dword 14〉：CDW14 的 CSI/OT/UUID Index 是共用解碼上下文；先遵守該 LID 的 offset 語義，不能把 byte offset 誤作 index。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW14 的 CSI/OT/UUID Index 是共用解碼上下文；先遵守該 LID 的 offset 語義，不能把 byte offset 誤作 index。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CSI]
          ↓
[擷取欄位: OT] → [套用編碼: UUID Index]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CSI` | Command Set Identifier，選擇 command 或 log page 所套用的 I/O Command Set context。 |
| `OT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `UUID Index` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.13、Figure 208；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. Area 是從同一 block 1 起算的不同大小視圖。先解碼 header，再選擇適用且有資料的最後 area；不要把三個 Last Block 數字相加。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 208 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | CDW14 的 CSI/OT/UUID Index 是共用解碼上下文；先遵守該 LID 的 offset 語義，不能把 byte offset 誤作 index。 |
| 邊界 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

**說明性範例。** Last Blocks=65/1000/30000 時，Area 3 payload 為 30000×512=15360000 bytes；包含 header 的 log 為 15360512 bytes。0/1000/1000 則表示 Area 1 空、Area 3 沒有超出 Area 2 的新增內容。

**常見誤解。** LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** CSI, OT, UUID Index

**來源 keyword 索引：** shall, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 208, 文件頁 214-215, PDF 頁 240-241

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 209: Get Log Page - Log Page Identifiers</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-209-CLAIM figure-table:BASEBTS-BASE-FIG-209 -->

**SPEC。** Figure 209〈Get Log Page - Log Page Identifiers〉：僅取 07h、08h、15h、81h 四列；每列把 log ID 與其章節相連，不延伸其他 log 的教學。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

僅取 07h、08h、15h、81h 四列；每列把 log ID 與其章節相連，不延伸其他 log 的教學。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LID 07h]
          ↓
[擷取欄位: LID 08h] → [套用編碼: LID 15h]
                                      ↓
[驗證證據: LID 81h]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LID 07h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `LID 08h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `LID 15h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `LID 81h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.13、Figure 209；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. Area 是從同一 block 1 起算的不同大小視圖。先解碼 header，再選擇適用且有資料的最後 area；不要把三個 Last Block 數字相加。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 209 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 僅取 07h、08h、15h、81h 四列；每列把 log ID 與其章節相連，不延伸其他 log 的教學。 |
| 邊界 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

**說明性範例。** Last Blocks=65/1000/30000 時，Area 3 payload 為 30000×512=15360000 bytes；包含 header 的 log 為 15360512 bytes。0/1000/1000 則表示 Area 1 空、Area 3 沒有超出 Area 2 的新增內容。

**常見誤解。** LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** LID 07h, LID 08h, LID 15h, LID 81h

**來源 keyword 索引：** may, optional, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 209, 文件頁 215-216, PDF 頁 241-242

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 210: Supported Log Pages Log Page</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-210-CLAIM figure-table:BASEBTS-BASE-FIG-210 -->

**SPEC。** Figure 210〈Supported Log Pages Log Page〉：Supported Log Pages 依 LID 提供 descriptor；07h descriptor 是 MCDAS 的查詢入口。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Supported Log Pages 依 LID 提供 descriptor；07h descriptor 是 MCDAS 的查詢入口。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Supported Log Pages]
          ↓
[擷取欄位: LID Support and Effects] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Supported Log Pages` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `LID Support and Effects` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.13.1.1、Figure 210；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 07h 的 create 與後續讀取分開；08h 的 capture 由 controller 決定。Host 對兩者都要驗證 generation，並分清事件 acknowledgement 與刪除 payload。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 210 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Supported Log Pages 依 LID 提供 descriptor；07h descriptor 是 MCDAS 的查詢入口。 |
| 邊界 | 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。 |

**說明性範例。** 讀取前 generation=2Ah，讀完變成 2Bh，這批 blocks 不能當成同一 capture 的一致資料。若值保持 2Ah 但 TCDA 被其他 host 清成 0，08h 收集仍需依流程檢查該競態。

**常見誤解。** 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Supported Log Pages, LID Support and Effects

**來源 keyword 索引：** shall, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.1, Figure 210, 文件頁 217, PDF 頁 243

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 211: LID Supported and Effects Data Structure</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-211-CLAIM figure-table:BASEBTS-BASE-FIG-211 -->

**SPEC。** Figure 211〈LID Supported and Effects Data Structure〉：先查 LSUPP 再解該 LID 的 specific parameter；MCDAS 的 bit 0 是此 parameter 的內容，不是 CTHID。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

先查 LSUPP 再解該 LID 的 specific parameter；MCDAS 的 bit 0 是此 parameter 的內容，不是 CTHID。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LSUPP]
          ↓
[擷取欄位: LID Specific Parameter] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LSUPP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `LID Specific Parameter` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.13.1.1、Figure 211；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 07h 的 create 與後續讀取分開；08h 的 capture 由 controller 決定。Host 對兩者都要驗證 generation，並分清事件 acknowledgement 與刪除 payload。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 211 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 先查 LSUPP 再解該 LID 的 specific parameter；MCDAS 的 bit 0 是此 parameter 的內容，不是 CTHID。 |
| 邊界 | 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。 |

**說明性範例。** 讀取前 generation=2Ah，讀完變成 2Bh，這批 blocks 不能當成同一 capture 的一致資料。若值保持 2Ah 但 TCDA 被其他 host 清成 0，08h 收集仍需依流程檢查該競態。

**常見誤解。** 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** LSUPP, LID Specific Parameter

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.1, Figure 211, 文件頁 217-218, PDF 頁 243-244

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 311: Reservation Notification Log Page</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-311-CLAIM figure-table:BASEBTS-BASE-FIG-311 -->

**SPEC。** Figure 311〈Reservation Notification Log Page〉：這是 Reservation Notification 的通知資料結構，回報通知計數與類型等；不含 SPROG。8.1.27.4.2 的引用疑似錯置，進度應對照 Figure 312。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

這是 Reservation Notification 的通知資料結構，回報通知計數與類型等；不含 SPROG。8.1.27.4.2 的引用疑似錯置，進度應對照 Figure 312。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Reservation Notification]
          ↓
[擷取欄位: Log Page Count] → [套用編碼: Notification Type]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Reservation Notification` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Log Page Count` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Notification Type` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.13.1.37、Figure 311；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 command allowlist 與 NVM Read 特例分開判斷。Host 先辨識 target/state，再確認 PI checking 與 allocation，不能把平常 read 的處理完全套入驗證狀態。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 311 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13.1.37 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 這是 Reservation Notification 的通知資料結構，回報通知計數與類型等；不含 SPROG。8.1.27.4.2 的引用疑似錯置，進度應對照 Figure 312。 |
| 邊界 | 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。 |

**說明性範例。** 驗證讀取 PRCHK=000b、STC=0，所有 allocated LBAs 都能讀取，且沒有其他 abort 原因時，預期 Successful Media Verification Read。只要請求 PI checking，預期分支即改為 Invalid Field in Command。

**常見誤解。** 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Reservation Notification, Log Page Count, Notification Type

**來源 keyword 索引：** shall, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.37, Figure 311, 文件頁 313, PDF 頁 339

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 338: Identify - Identify Controller Data Structure, I/O Command Set Independent</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-338-CLAIM figure-table:BASEBTS-BASE-FIG-338 -->

**SPEC。** Figure 338〈Identify - Identify Controller Data Structure, I/O Command Set Independent〉：只解本題欄位：BPCAP byte 102，LPA byte 261，SANICAP bytes 328–331，以及 CTRATT 的 MDS；SANICAP 分開檢查方法、VERS/NVERS、SPRRS、NDI 與 NODMMAS。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

只解本題欄位：BPCAP byte 102，LPA byte 261，SANICAP bytes 328–331，以及 CTRATT 的 MDS；SANICAP 分開檢查方法、VERS/NVERS、SPRRS、NDI 與 NODMMAS。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: BPCAP]
          ↓
[擷取欄位: LPA] → [套用編碼: SANICAP]
                                      ↓
[驗證證據: CTRATT]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `BPCAP` | Boot Partition Capabilities；辨識 Set Features 與 RPMB 保護機制的支援組合。 |
| `LPA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SANICAP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CTRATT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.14.2.1、Figure 338；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 先把支援能力、命令要求與 Feature policy 分開。命令接受、operation 成功、符合 no-deallocate 要求是三個需要不同證據的結果。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

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
| 規則 | 只解本題欄位：BPCAP byte 102，LPA byte 261，SANICAP bytes 328–331，以及 CTRATT 的 MDS；SANICAP 分開檢查方法、VERS/NVERS、SPRRS、NDI 與 NODMMAS。 |
| 邊界 | Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。 |

**說明性範例。** SANACT=010b、AUSE=0、EMVS=1、NDAS=0、PREQ=0 的 CDW10 是 0402h。只有支援 VERS/Block Erase 且其他前置條件成立時才適用。另一例：OWPASS=0h 是 16 次，不是『跳過 overwrite』。

**常見誤解。** Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** BPCAP, LPA, SANICAP, CTRATT

**來源 keyword 索引：** shall not, should not, shall, should, may, optional, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, 文件頁 340-382, PDF 頁 366-408

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 454: Sanitize Namespace - Command Dword 10</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-454-CLAIM figure-table:BASEBTS-BASE-FIG-454 -->

**SPEC。** Figure 454〈Sanitize Namespace - Command Dword 10〉：Namespace CDW10 只有 Exit Failure/Crypto Erase/Exit Verification；PREQ 在 bit 4，EMVS 在 bit 10，無 NDAS 或 Overwrite 參數。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Namespace CDW10 只有 Exit Failure/Crypto Erase/Exit Verification；PREQ 在 bit 4，EMVS 在 bit 10，無 NDAS 或 Overwrite 參數。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SANACT]
          ↓
[擷取欄位: AUSE] → [套用編碼: PREQ]
                                      ↓
[驗證證據: EMVS]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SANACT` | Sanitize Action；決定實際方法、退出 Failure 或退出 Media Verification。 |
| `AUSE` | Allow Unrestricted Sanitize Exit；選擇失敗時是否允許不經成功重試就退出 Failure。 |
| `PREQ` | Purge Request；與 SPRRS 一起判定 purge 要求與回報；兩種 Sanitize 命令的 bit 位置不同。 |
| `EMVS` | Enter Media Verification State；成功 processing 後要求進入驗證，受方法與 capability 限制。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.27、Figure 454；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 先把支援能力、命令要求與 Feature policy 分開。命令接受、operation 成功、符合 no-deallocate 要求是三個需要不同證據的結果。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 454 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.27 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Namespace CDW10 只有 Exit Failure/Crypto Erase/Exit Verification；PREQ 在 bit 4，EMVS 在 bit 10，無 NDAS 或 Overwrite 參數。 |
| 邊界 | Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。 |

**說明性範例。** SANACT=010b、AUSE=0、EMVS=1、NDAS=0、PREQ=0 的 CDW10 是 0402h。只有支援 VERS/Block Erase 且其他前置條件成立時才適用。另一例：OWPASS=0h 是 16 次，不是『跳過 overwrite』。

**常見誤解。** Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** SANACT, AUSE, PREQ, EMVS

**來源 keyword 索引：** shall not, should not, shall, should, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.27, Figure 454, 文件頁 453, PDF 頁 479

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 464: Set Features - Command Dword 10</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-464-CLAIM figure-table:BASEBTS-BASE-FIG-464 -->

**SPEC。** Figure 464〈Set Features - Command Dword 10〉：Set Features 的 FID 決定 CDW11 解法；SV 是保存要求，不能因設定成功就推論 power cycle 後仍保留。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Set Features 的 FID 決定 CDW11 解法；SV 是保存要求，不能因設定成功就推論 power cycle 後仍保留。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: FID]
          ↓
[擷取欄位: SV] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `FID` | Feature Identifier，Get／Set Features 用來選擇功能的 8-bit identifier。 |
| `SV` | Save，Set Features 要求 controller 同時保存所設定 value 的 bit。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.30、Figure 464；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

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
| 規則 | Set Features 的 FID 決定 CDW11 解法；SV 是保存要求，不能因設定成功就推論 power cycle 後仍保留。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** FID, SV

**來源 keyword 索引：** shall, optional, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 464, 文件頁 457, PDF 頁 483

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 465: Set Features - Command Dword 14</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-465-CLAIM figure-table:BASEBTS-BASE-FIG-465 -->

**SPEC。** Figure 465〈Set Features - Command Dword 14〉：Set 的 UUID Index 使用條件與 feature identity 一起判斷；本題標準 FIDs 不擴成 vendor feature protocol。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Set 的 UUID Index 使用條件與 feature identity 一起判斷；本題標準 FIDs 不擴成 vendor feature protocol。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: UUID Index]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `UUID Index` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.30、Figure 465；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

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
| 規則 | Set 的 UUID Index 使用條件與 feature identity 一起判斷；本題標準 FIDs 不擴成 vendor feature protocol。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** UUID Index

**來源 keyword 索引：** shall, optional, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 465, 文件頁 457, PDF 頁 483

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 466: Set Features - Feature Identifiers</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-466-CLAIM figure-table:BASEBTS-BASE-FIG-466 -->

**SPEC。** Figure 466〈Set Features - Feature Identifiers〉：只看 Boot protection、Sanitize Config、AEC、Host Behavior Support 的 feature rows 與 scope；FID 17h 是 subsystem policy。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

只看 Boot protection、Sanitize Config、AEC、Host Behavior Support 的 feature rows 與 scope；FID 17h 是 subsystem policy。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: FID 85h]
          ↓
[擷取欄位: FID 17h] → [套用編碼: FID 0Bh]
                                      ↓
[驗證證據: FID 16h]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `FID 85h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FID 17h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FID 0Bh` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FID 16h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.30、Figure 466；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 先把支援能力、命令要求與 Feature policy 分開。命令接受、operation 成功、符合 no-deallocate 要求是三個需要不同證據的結果。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

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
| 規則 | 只看 Boot protection、Sanitize Config、AEC、Host Behavior Support 的 feature rows 與 scope；FID 17h 是 subsystem policy。 |
| 邊界 | Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。 |

**說明性範例。** SANACT=010b、AUSE=0、EMVS=1、NDAS=0、PREQ=0 的 CDW10 是 0402h。只有支援 VERS/Block Erase 且其他前置條件成立時才適用。另一例：OWPASS=0h 是 16 次，不是『跳過 overwrite』。

**常見誤解。** Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** FID 85h, FID 17h, FID 0Bh, FID 16h

**來源 keyword 索引：** shall, should, may, optional, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 466, 文件頁 457-459, PDF 頁 483-485

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 474: Asynchronous Event Configuration - Command Dword 11</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-474-CLAIM figure-table:BASEBTS-BASE-FIG-474 -->

**SPEC。** Figure 474〈Asynchronous Event Configuration - Command Dword 11〉：只取 bit 10 TLN：TCDA 從 0h 變 1h 且 TLN enabled 時發送 Telemetry Log Changed；此表在 5.2.30.1.6。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

只取 bit 10 TLN：TCDA 從 0h 變 1h 且 TLN enabled 時發送 Telemetry Log Changed；此表在 5.2.30.1.6。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TLN]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TLN` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.30.1.6、Figure 474；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 07h 的 create 與後續讀取分開；08h 的 capture 由 controller 決定。Host 對兩者都要驗證 generation，並分清事件 acknowledgement 與刪除 payload。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

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
| 規則 | 只取 bit 10 TLN：TCDA 從 0h 變 1h 且 TLN enabled 時發送 Telemetry Log Changed；此表在 5.2.30.1.6。 |
| 邊界 | 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。 |

**說明性範例。** 讀取前 generation=2Ah，讀完變成 2Bh，這批 blocks 不能當成同一 capture 的一致資料。若值保持 2Ah 但 TCDA 被其他 host 清成 0，08h 收集仍需依流程檢查該競態。

**常見誤解。** 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** TLN

**來源 keyword 索引：** shall not, shall, may, optional, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.6, Figure 474, 文件頁 466-468, PDF 頁 492-494

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 491: Host Behavior Support - Data Structure</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-491-CLAIM figure-table:BASEBTS-BASE-FIG-491 -->

**SPEC。** Figure 491〈Host Behavior Support - Data Structure〉：Host Behavior Support byte 1 的 ETDAS=1 表示 host 支援 Area 4；仍需 controller 的 DA4S。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Host Behavior Support byte 1 的 ETDAS=1 表示 host 支援 Area 4；仍需 controller 的 DA4S。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ETDAS]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ETDAS` | Extended Telemetry Data Area 4 Supported；Host Behavior Support 中由 host 宣告 Area 4 支援。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§5.2.30.1.15、Figure 491；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. Area 是從同一 block 1 起算的不同大小視圖。先解碼 header，再選擇適用且有資料的最後 area；不要把三個 Last Block 數字相加。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 491 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.1.15 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Host Behavior Support byte 1 的 ETDAS=1 表示 host 支援 Area 4；仍需 controller 的 DA4S。 |
| 邊界 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

**說明性範例。** Last Blocks=65/1000/30000 時，Area 3 payload 為 30000×512=15360000 bytes；包含 header 的 log 為 15360512 bytes。0/1000/1000 則表示 Area 1 空、Area 3 沒有超出 Area 2 的新增內容。

**常見誤解。** LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** ETDAS

**來源 keyword 索引：** shall not, shall, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.15, Figure 491, 文件頁 476-477, PDF 頁 502-503

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 756: RPMB Device Configuration Block Data Structure</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-756-CLAIM figure-table:BASEBTS-BASE-FIG-756 -->

**SPEC。** Figure 756〈RPMB Device Configuration Block Data Structure〉：Device Configuration Block 分開保存啟用保護與每個 partition 的鎖定控制；啟用後拒絕關閉 RPMB Boot 保護的寫入。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Device Configuration Block 分開保存啟用保護與每個 partition 的鎖定控制；啟用後拒絕關閉 RPMB Boot 保護的寫入。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Boot Partition Write Protection Enable]
          ↓
[擷取欄位: Boot Partition Write Protection] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Boot Partition Write Protection Enable` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Boot Partition Write Protection` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.24、Figure 756；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 756 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.24 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Device Configuration Block 分開保存啟用保護與每個 partition 的鎖定控制；啟用後拒絕關閉 RPMB Boot 保護的寫入。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Boot Partition Write Protection Enable, Boot Partition Write Protection

**來源 keyword 索引：** shall not, shall, should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.24, Figure 756, 文件頁 691-692, PDF 頁 717-718

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 757: RPMB Request and Response Message Types</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-757-CLAIM figure-table:BASEBTS-BASE-FIG-757 -->

**SPEC。** Figure 757〈RPMB Request and Response Message Types〉：只追蹤 Boot 所需的 authenticated configuration read/write message types；message type 必須與預期 response 配對。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

只追蹤 Boot 所需的 authenticated configuration read/write message types；message type 必須與預期 response 配對。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Authenticated Device Configuration Block Read]
          ↓
[擷取欄位: Authenticated Device Configuration Block Write] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Authenticated Device Configuration Block Read` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Authenticated Device Configuration Block Write` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.24、Figure 757；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 757 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.24 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 只追蹤 Boot 所需的 authenticated configuration read/write message types；message type 必須與預期 response 配對。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Authenticated Device Configuration Block Read, Authenticated Device Configuration Block Write

**來源 keyword 索引：** shall, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.24, Figure 757, 文件頁 692-693, PDF 頁 718-719

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 758: RPMB Operation Result</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-758-CLAIM figure-table:BASEBTS-BASE-FIG-758 -->

**SPEC。** Figure 758〈RPMB Operation Result〉：Operation Result 區分成功、認證與 counter 等失敗；傳輸命令完成不等於 RPMB 寫入已成功。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Operation Result 區分成功、認證與 counter 等失敗；傳輸命令完成不等於 RPMB 寫入已成功。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Result]
          ↓
[擷取欄位: Authentication Failure] → [套用編碼: Counter Failure]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Result` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Authentication Failure` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Counter Failure` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.24、Figure 758；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 758 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.24 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Operation Result 區分成功、認證與 counter 等失敗；傳輸命令完成不等於 RPMB 寫入已成功。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Result, Authentication Failure, Counter Failure

**來源 keyword 索引：** may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.24, Figure 758, 文件頁 693, PDF 頁 719

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 760: RPMB Data Frame</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-760-CLAIM figure-table:BASEBTS-BASE-FIG-760 -->

**SPEC。** Figure 760〈RPMB Data Frame〉：Frame 的 message type、counter、nonce、result 與 authentication 是驗證回應的不同證據；不能只看資料 payload。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Frame 的 message type、counter、nonce、result 與 authentication 是驗證回應的不同證據；不能只看資料 payload。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Message Type]
          ↓
[擷取欄位: Result] → [套用編碼: Write Counter]
                                      ↓
[驗證證據: Nonce]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Message Type` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Result` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Write Counter` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Nonce` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Authentication` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.24、Figure 760；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 760 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.24 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Frame 的 message type、counter、nonce、result 與 authentication 是驗證回應的不同證據；不能只看資料 payload。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Message Type, Result, Write Counter, Nonce, Authentication

**來源 keyword 索引：** shall not, shall, optional

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.24, Figure 760, 文件頁 694, PDF 頁 720

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 761: RPMB - Authentication Key Data Flow</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-761-CLAIM figure-table:BASEBTS-BASE-FIG-761 -->

**SPEC。** Figure 761〈RPMB - Authentication Key Data Flow〉：Authentication key 的設定是 authenticated configuration 流程的前置背景；需核對 programming result，不把送出 key 當成成功。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Authentication key 的設定是 authenticated configuration 流程的前置背景；需核對 programming result，不把送出 key 當成成功。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Authentication Key]
          ↓
[擷取欄位: Program Result] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Authentication Key` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Program Result` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.24.2.1、Figure 761；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 761 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.24.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Authentication key 的設定是 authenticated configuration 流程的前置背景；需核對 programming result，不把送出 key 當成成功。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Authentication Key, Program Result

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.24.2.1, Figure 761, 文件頁 695-696, PDF 頁 721-722

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 762: RPMB - Read Write Counter Value Flow</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-762-CLAIM figure-table:BASEBTS-BASE-FIG-762 -->

**SPEC。** Figure 762〈RPMB - Read Write Counter Value Flow〉：先取得並驗證 write counter，配合 nonce/authentication 確認回應，再構造受保護的 configuration write。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

先取得並驗證 write counter，配合 nonce/authentication 確認回應，再構造受保護的 configuration write。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Write Counter]
          ↓
[擷取欄位: Nonce] → [套用編碼: Authenticated Response]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Write Counter` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Nonce` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Authenticated Response` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.24.2.2、Figure 762；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 762 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.24.2.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | 先取得並驗證 write counter，配合 nonce/authentication 確認回應，再構造受保護的 configuration write。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Write Counter, Nonce, Authenticated Response

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.24.2.2, Figure 762, 文件頁 696, PDF 頁 722

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 765: RPMB - Authenticated Device Configuration Block Write Flow</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-765-CLAIM figure-table:BASEBTS-BASE-FIG-765 -->

**SPEC。** Figure 765〈RPMB - Authenticated Device Configuration Block Write Flow〉：Authenticated configuration write 後需核對 result；此流程變更 Boot 保護狀態，不是 Firmware Commit 寫入 image 的流程。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Authenticated configuration write 後需核對 result；此流程變更 Boot 保護狀態，不是 Firmware Commit 寫入 image 的流程。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Configuration Write]
          ↓
[擷取欄位: Counter] → [套用編碼: Result Read]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Configuration Write` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Counter` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Result Read` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.24.3、Figure 765；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 765 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.24.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Authenticated configuration write 後需核對 result；此流程變更 Boot 保護狀態，不是 Firmware Commit 寫入 image 的流程。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Configuration Write, Counter, Result Read

**來源 keyword 索引：** should

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.24.3, Figure 765, 文件頁 700, PDF 頁 726

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 766: RPMB - Authenticated Device Configuration Block Read Flow</strong></summary>

<!-- claim:BASEBTS-BASE-FIG-766-CLAIM figure-table:BASEBTS-BASE-FIG-766 -->

**SPEC。** Figure 766〈RPMB - Authenticated Device Configuration Block Read Flow〉：Authenticated configuration read 取得可驗證的保護設定，用以確認哪一套機制目前控制 partition。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Authenticated configuration read 取得可驗證的保護設定，用以確認哪一套機制目前控制 partition。

下列欄位限定於此來源文件與此 Figure；範例將欄位連回完整操作。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Configuration Read]
          ↓
[擷取欄位: Nonce] → [套用編碼: Authentication]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Configuration Read` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Nonce` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Authentication` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 確認 NVME-BASE-2.4、§8.1.24.4、Figure 766；不同文件的同號 Figure 是不同來源。
2. 將上方欄位／狀態規則套用到保存的原始輸入。
3. 把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。
4. 用具體情境比對觀測結果，保留引用位置與 target 身分。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 766 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.24.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 規則 | Authenticated configuration read 取得可驗證的保護設定，用以確認哪一套機制目前控制 partition。 |
| 邊界 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

**說明性範例。** 保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

**常見誤解。** 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 症狀／修正 | 用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。 |

#### 讀完後應能回答

1. 哪些本文件的欄位支持這個判斷？
2. 哪個 capability、target 或 state 會改變範例結果？

**來源欄位索引：** Configuration Read, Nonce, Authentication

**來源 keyword 索引：** shall not, shall, may

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.24.4, Figure 766, 文件頁 701, PDF 頁 727

</details>

## 使用與限制

製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata 集合或核准範圍改變時，必須重新核對受影響 claim。

## 自問自答：規則、比較、案例與排錯

以下 32 題均附答案，針對本報告範圍複習。每題保留對應教學單元的來源；數值案例與排錯建議屬說明性內容。

### Q01. 「Boot 的兩條讀取路徑」的核心判讀規則是什麼？

<!-- qa:base-boot-telemetry-sanitize-boot-read-lead -->

**答。**

先問 controller 是否已建立 Admin command 環境，再選 property 或 LID 15h。兩條路徑讀同一類 Boot 內容，但回傳格式與狀態觀察點不同。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3, 文件頁 586, PDF 頁 612; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.1, 文件頁 586-587, PDF 頁 612-613; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, 文件頁 283-284, PDF 頁 309-310

### Q02. 「Boot 的兩條讀取路徑」中，哪些概念或條件必須分開比較？

<!-- qa:base-boot-telemetry-sanitize-boot-read-rows -->

**答。**

- Properties — BRS 回報讀取狀態 — 不要求 CC.EN=1
- LID 15h — 16-byte header + data — 由 Admin command CQE 判斷命令結果
- BPID — 選取讀取 partition — 不等於 active ID
- BPSZ — 每單位 128 KiB — 不是 bytes

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3, 文件頁 586, PDF 頁 612; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.1, 文件頁 586-587, PDF 頁 612-613; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, 文件頁 283-284, PDF 頁 309-310

### Q03. 「Boot 的兩條讀取路徑」如何套用到具體數值或操作情境？

<!-- qa:base-boot-telemetry-sanitize-boot-read-example -->

**答。**

BPSZ=2 的 LID 15h 包含 262144 bytes 的 Boot data，加上 16-byte header，共 262160 bytes。讀 BP1 並不把 BP1 設為 active；讀 log 也不會推進 property 的 BRS。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3, 文件頁 586, PDF 頁 612; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.1, 文件頁 586-587, PDF 頁 612-613; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, 文件頁 283-284, PDF 頁 309-310

### Q04. 「Boot 的兩條讀取路徑」最容易出現什麼誤判？如何排查？

<!-- qa:base-boot-telemetry-sanitize-boot-read-pitfall -->

**答。**

若 property 讀取未完成，先檢查 BRS 與 buffer，不能用 reset 當作允許的正常完成步驟。LID 15h 的 BPINFO 是回傳欄位，讀它不會改動同名 property。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3, 文件頁 586, PDF 頁 612; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.1, 文件頁 586-587, PDF 頁 612-613; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, 文件頁 283-284, PDF 頁 309-310

### Q05. 「更新與保護的完整生命週期」的核心判讀規則是什麼？

<!-- qa:base-boot-telemetry-sanitize-boot-protection-lead -->

**答。**

把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, 文件頁 587-588, PDF 頁 613-614; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, 文件頁 588, PDF 頁 614; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.3, 文件頁 588-589, PDF 頁 614-615; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39, 文件頁 513-514, PDF 頁 539-540; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1-8.1.3.3.3, 文件頁 589-594, PDF 頁 615-620; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39; 8.1.3.3.3, 文件頁 513-514,593-594, PDF 頁 539-540,619-620

### Q06. 「更新與保護的完整生命週期」中，哪些概念或條件必須分開比較？

<!-- qa:base-boot-telemetry-sanitize-boot-protection-rows -->

**答。**

- FID 85h unlocked — Controller reset 後保留 — Power cycle 後 locked
- FID 85h until power cycle — 一般 Set 不可解鎖 — 共享 multi-domain partition 不可用
- RPMB enabled/unlocked — Controller reset 即 relock — 啟用保護不可撤回
- 兩套機制 — 同時只有一套控制 — RPMB enable 是控制權轉移

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, 文件頁 587-588, PDF 頁 613-614; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, 文件頁 588, PDF 頁 614; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.3, 文件頁 588-589, PDF 頁 614-615; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39, 文件頁 513-514, PDF 頁 539-540; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1-8.1.3.3.3, 文件頁 589-594, PDF 頁 615-620; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39; 8.1.3.3.3, 文件頁 513-514,593-594, PDF 頁 539-540,619-620

### Q07. 「更新與保護的完整生命週期」如何套用到具體數值或操作情境？

<!-- qa:base-boot-telemetry-sanitize-boot-protection-example -->

**答。**

保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b << 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, 文件頁 587-588, PDF 頁 613-614; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, 文件頁 588, PDF 頁 614; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.3, 文件頁 588-589, PDF 頁 614-615; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39, 文件頁 513-514, PDF 頁 539-540; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1-8.1.3.3.3, 文件頁 589-594, PDF 頁 615-620; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39; 8.1.3.3.3, 文件頁 513-514,593-594, PDF 頁 539-540,619-620

### Q08. 「更新與保護的完整生命週期」最容易出現什麼誤判？如何排查？

<!-- qa:base-boot-telemetry-sanitize-boot-protection-pitfall -->

**答。**

用相同 reset 測試兩套機制時，預期結果不同。也要保留 power-cycle/reset 類型，否則無法證明 relock 是正常行為或錯誤。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, 文件頁 587-588, PDF 頁 613-614; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, 文件頁 588, PDF 頁 614; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.3, 文件頁 588-589, PDF 頁 614-615; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39, 文件頁 513-514, PDF 頁 539-540; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1-8.1.3.3.3, 文件頁 589-594, PDF 頁 615-620; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39; 8.1.3.3.3, 文件頁 513-514,593-594, PDF 頁 539-540,619-620

### Q09. 「從 Last Block 計算快照」的核心判讀規則是什麼？

<!-- qa:base-boot-telemetry-sanitize-telemetry-layout-lead -->

**答。**

Area 是從同一 block 1 起算的不同大小視圖。先解碼 header，再選擇適用且有資料的最後 area；不要把三個 Last Block 數字相加。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.13.1.8-5.2.13.1.9, 文件頁 232-237,733-737, PDF 頁 258-263,759-763; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.15, 文件頁 476,733-734, PDF 頁 502,759-760; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, 文件頁 232-237, PDF 頁 258-263

### Q10. 「從 Last Block 計算快照」中，哪些概念或條件必須分開比較？

<!-- qa:base-boot-telemetry-sanitize-telemetry-layout-rows -->

**答。**

- Area 1 — 1 到 L1 — L1=0 表示沒有資料
- Area 2 — 1 到 L2 — L2 >= L1
- Area 3 — 1 到 L3 — L3 >= L2
- Area 4 — 1 到 L4 — 支援條件另行檢查

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.13.1.8-5.2.13.1.9, 文件頁 232-237,733-737, PDF 頁 258-263,759-763; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.15, 文件頁 476,733-734, PDF 頁 502,759-760; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, 文件頁 232-237, PDF 頁 258-263

### Q11. 「從 Last Block 計算快照」如何套用到具體數值或操作情境？

<!-- qa:base-boot-telemetry-sanitize-telemetry-layout-example -->

**答。**

Last Blocks=65/1000/30000 時，Area 3 payload 為 30000×512=15360000 bytes；包含 header 的 log 為 15360512 bytes。0/1000/1000 則表示 Area 1 空、Area 3 沒有超出 Area 2 的新增內容。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.13.1.8-5.2.13.1.9, 文件頁 232-237,733-737, PDF 頁 258-263,759-763; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.15, 文件頁 476,733-734, PDF 頁 502,759-760; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, 文件頁 232-237, PDF 頁 258-263

### Q12. 「從 Last Block 計算快照」最容易出現什麼誤判？如何排查？

<!-- qa:base-boot-telemetry-sanitize-telemetry-layout-pitfall -->

**答。**

LID 07h 的 THS 與 LID 08h 的 TCS 位置不同；不能把一份 header 的 offset 套在另一份。Snapshot payload 由廠商定義，不能把未知 bytes 解碼成假設的診斷欄位。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.13.1.8-5.2.13.1.9, 文件頁 232-237,733-737, PDF 頁 258-263,759-763; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.15, 文件頁 476,733-734, PDF 頁 502,759-760; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, 文件頁 232-237, PDF 頁 258-263

### Q13. 「建立、讀取、確認一致、acknowledge」的核心判讀規則是什麼？

<!-- qa:base-boot-telemetry-sanitize-telemetry-capture-lead -->

**答。**

07h 的 create 與後續讀取分開；08h 的 capture 由 controller 決定。Host 對兩者都要驗證 generation，並分清事件 acknowledgement 與刪除 payload。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, 文件頁 232-235, PDF 頁 258-261; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30, 文件頁 734-735, PDF 頁 760-761; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, 文件頁 237, PDF 頁 263; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, 文件頁 233,235,237, PDF 頁 259,261,263; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.6, 文件頁 734-735,466-468, PDF 頁 760-761,492-494

### Q14. 「建立、讀取、確認一致、acknowledge」中，哪些概念或條件必須分開比較？

<!-- qa:base-boot-telemetry-sanitize-telemetry-capture-rows -->

**答。**

- CTHID=1 — 觸發新 07h capture — 後續分段讀不要再次 create
- MCDA — 限制建立到哪個 area — 先看 MCDAS
- RAE=1 — 保留事件 — 不保證沒有其他 reader
- TCDA=0 — 上次 acknowledgement 後未更新 — 2.4 不等於 payload 消失

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, 文件頁 232-235, PDF 頁 258-261; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30, 文件頁 734-735, PDF 頁 760-761; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, 文件頁 237, PDF 頁 263; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, 文件頁 233,235,237, PDF 頁 259,261,263; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.6, 文件頁 734-735,466-468, PDF 頁 760-761,492-494

### Q15. 「建立、讀取、確認一致、acknowledge」如何套用到具體數值或操作情境？

<!-- qa:base-boot-telemetry-sanitize-telemetry-capture-example -->

**答。**

讀取前 generation=2Ah，讀完變成 2Bh，這批 blocks 不能當成同一 capture 的一致資料。若值保持 2Ah 但 TCDA 被其他 host 清成 0，08h 收集仍需依流程檢查該競態。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, 文件頁 232-235, PDF 頁 258-261; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30, 文件頁 734-735, PDF 頁 760-761; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, 文件頁 237, PDF 頁 263; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, 文件頁 233,235,237, PDF 頁 259,261,263; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.6, 文件頁 734-735,466-468, PDF 頁 760-761,492-494

### Q16. 「建立、讀取、確認一致、acknowledge」最容易出現什麼誤判？如何排查？

<!-- qa:base-boot-telemetry-sanitize-telemetry-capture-pitfall -->

**答。**

不要把 RAE=0 寫成『刪除 snapshot』，也不要把 AER 當成 payload 本身。事件只提供收集觸發與定位，資料仍由 Get Log Page 取得。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, 文件頁 232-235, PDF 頁 258-261; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30, 文件頁 734-735, PDF 頁 760-761; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, 文件頁 237, PDF 頁 263; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8-5.2.13.1.9, 文件頁 233,235,237, PDF 頁 259,261,263; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.30.1.6, 文件頁 734-735,466-468, PDF 頁 760-761,492-494

### Q17. 「先定義被清理的 target」的核心判讀規則是什麼？

<!-- qa:base-boot-telemetry-sanitize-sanitize-scope-lead -->

**答。**

Sanitize scope 不是『磁碟上所有東西』。以 target、資料來源、是否可能含 user data 判斷；Boot 與診斷機制的交叉關係也從這個範圍開始。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27, 文件頁 711-712, PDF 頁 737-738; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27, 文件頁 711-712, PDF 頁 737-738; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.2-8.1.27.3, 文件頁 714-717, PDF 頁 740-743; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12, 文件頁 174, PDF 頁 174

### Q18. 「先定義被清理的 target」中，哪些概念或條件必須分開比較？

<!-- qa:base-boot-telemetry-sanitize-sanitize-scope-rows -->

**答。**

- Boot/RPMB — 不受 sanitize 影響 — 另由自身管理機制控制
- Logs/features — 必要時修改 user data — 不能只檢查 namespace media
- All namespace sanitizes — 只完成各 target 的工作 — 不能因此宣告 subsystem GDE
- Crypto Erase — 改 key 並處理未加密資料 — 舊 key 副本也是重要條件

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27, 文件頁 711-712, PDF 頁 737-738; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27, 文件頁 711-712, PDF 頁 737-738; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.2-8.1.27.3, 文件頁 714-717, PDF 頁 740-743; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12, 文件頁 174, PDF 頁 174

### Q19. 「先定義被清理的 target」如何套用到具體數值或操作情境？

<!-- qa:base-boot-telemetry-sanitize-sanitize-scope-example -->

**答。**

即使所有 namespaces 都已 sanitize，CMB 等 subsystem 層級資料仍不能由這個事實證明已完成 subsystem sanitization。相反地，成功 subsystem sanitize 也不會替 Boot Partition 更新或清除開機映像。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27, 文件頁 711-712, PDF 頁 737-738; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27, 文件頁 711-712, PDF 頁 737-738; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.2-8.1.27.3, 文件頁 714-717, PDF 頁 740-743; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12, 文件頁 174, PDF 頁 174

### Q20. 「先定義被清理的 target」最容易出現什麼誤判？如何排查？

<!-- qa:base-boot-telemetry-sanitize-sanitize-scope-pitfall -->

**答。**

把成功後 read 回零視為唯一成功標準會誤判。先確認方法、是否 deallocate、是否在驗證狀態，再套用 NVM Command Set 定義的結果。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27, 文件頁 711-712, PDF 頁 737-738; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27, 文件頁 711-712, PDF 頁 737-738; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.2-8.1.27.3, 文件頁 714-717, PDF 頁 740-743; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12, 文件頁 174, PDF 頁 174

### Q21. 「命令參數與 capability 組合」的核心判讀規則是什麼？

<!-- qa:base-boot-telemetry-sanitize-sanitize-command-lead -->

**答。**

先把支援能力、命令要求與 Feature policy 分開。命令接受、operation 成功、符合 no-deallocate 要求是三個需要不同證據的結果。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, 文件頁 448-451, PDF 頁 474-477; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 5.2.27, 文件頁 713,453, PDF 頁 739,479; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.16; 8.1.27.2-8.1.27.3, 文件頁 477-478,715-719, PDF 頁 503-504,741-745; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, 文件頁 449, PDF 頁 475; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.1, 文件頁 449-451,712-714, PDF 頁 475-477,738-740; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.3, 文件頁 451,717, PDF 頁 477,743

### Q22. 「命令參數與 capability 組合」中，哪些概念或條件必須分開比較？

<!-- qa:base-boot-telemetry-sanitize-sanitize-command-rows -->

**答。**

- NDAS=1, NDI=0 — 不得因成功 sanitize deallocate — 其他合法條件仍需符合
- NDAS=1, NDI=1, NODRM=0 — 命令拒絕 — Invalid Field in Command
- NDAS=1, NDI=1, NODRM=1 — 允許處理 — 成功可回 SOS=100b
- EMVS=1 — Subsystem 要 VERS=1 — Block/Crypto + NDAS=0

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, 文件頁 448-451, PDF 頁 474-477; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 5.2.27, 文件頁 713,453, PDF 頁 739,479; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.16; 8.1.27.2-8.1.27.3, 文件頁 477-478,715-719, PDF 頁 503-504,741-745; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, 文件頁 449, PDF 頁 475; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.1, 文件頁 449-451,712-714, PDF 頁 475-477,738-740; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.3, 文件頁 451,717, PDF 頁 477,743

### Q23. 「命令參數與 capability 組合」如何套用到具體數值或操作情境？

<!-- qa:base-boot-telemetry-sanitize-sanitize-command-example -->

**答。**

SANACT=010b、AUSE=0、EMVS=1、NDAS=0、PREQ=0 的 CDW10 是 0402h。只有支援 VERS/Block Erase 且其他前置條件成立時才適用。另一例：OWPASS=0h 是 16 次，不是『跳過 overwrite』。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, 文件頁 448-451, PDF 頁 474-477; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 5.2.27, 文件頁 713,453, PDF 頁 739,479; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.16; 8.1.27.2-8.1.27.3, 文件頁 477-478,715-719, PDF 頁 503-504,741-745; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, 文件頁 449, PDF 頁 475; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.1, 文件頁 449-451,712-714, PDF 頁 475-477,738-740; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.3, 文件頁 451,717, PDF 頁 477,743

### Q24. 「命令參數與 capability 組合」最容易出現什麼誤判？如何排查？

<!-- qa:base-boot-telemetry-sanitize-sanitize-command-pitfall -->

**答。**

Figure 454 的 PREQ 在 bit 4，Figure 451 則在 bit 11。兩種命令若共用未分型的 builder，容易在 namespace 命令寫入 reserved bits。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, 文件頁 448-451, PDF 頁 474-477; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 5.2.27, 文件頁 713,453, PDF 頁 739,479; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.16; 8.1.27.2-8.1.27.3, 文件頁 477-478,715-719, PDF 頁 503-504,741-745; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, 文件頁 449, PDF 頁 475; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.1, 文件頁 449-451,712-714, PDF 頁 475-477,738-740; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26; 8.1.27.3, 文件頁 451,717, PDF 頁 477,743

### Q25. 「用 state、log、AER 重建背景作業」的核心判讀規則是什麼？

<!-- qa:base-boot-telemetry-sanitize-sanitize-state-lead -->

**答。**

從 Figure 772 的七個 states 出發，逐一把 Figures 773–779 的 transition condition 接上。Status 描述結果，state 描述目前位置，事件描述發生的轉折。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26.1; 8.1.27.1, 文件頁 451,712-713, PDF 頁 477,738-739; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4, 文件頁 719-730, PDF 頁 745-756; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.6-8.1.27.4.7, 文件頁 727-730, PDF 頁 753-756; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, 文件頁 313-319, PDF 頁 339-345; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38; 8.1.27.3, 文件頁 314-319,718, PDF 頁 340-345,744; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 8.1.27.4, 文件頁 712-713,720, PDF 頁 738-739,746

### Q26. 「用 state、log、AER 重建背景作業」中，哪些概念或條件必須分開比較？

<!-- qa:base-boot-telemetry-sanitize-sanitize-state-rows -->

**答。**

- Restricted Failure — 只以 restricted 重試 — Exit Failure Mode 不可解套
- Unrestricted Failure — 重試或 Exit Failure Mode — 回 Idle 不會改寫失敗歷史
- Media Verification — Processing 已成功 — 整個 operation 仍 Sanitizing
- Post-Verification Deallocation — SPROG 重新由 0 起算 — 失敗 FAILS=6h

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26.1; 8.1.27.1, 文件頁 451,712-713, PDF 頁 477,738-739; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4, 文件頁 719-730, PDF 頁 745-756; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.6-8.1.27.4.7, 文件頁 727-730, PDF 頁 753-756; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, 文件頁 313-319, PDF 頁 339-345; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38; 8.1.27.3, 文件頁 314-319,718, PDF 頁 340-345,744; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 8.1.27.4, 文件頁 712-713,720, PDF 頁 738-739,746

### Q27. 「用 state、log、AER 重建背景作業」如何套用到具體數值或操作情境？

<!-- qa:base-boot-telemetry-sanitize-sanitize-state-example -->

**答。**

SPROG=8000h 表示目前被量測的階段約 50%。進入 Media Verification 後 SPROG=FFFFh，SOS 仍可為 010b；退出驗證進入 deallocation 又從 0 開始。這不是進度倒退。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26.1; 8.1.27.1, 文件頁 451,712-713, PDF 頁 477,738-739; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4, 文件頁 719-730, PDF 頁 745-756; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.6-8.1.27.4.7, 文件頁 727-730, PDF 頁 753-756; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, 文件頁 313-319, PDF 頁 339-345; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38; 8.1.27.3, 文件頁 314-319,718, PDF 頁 340-345,744; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 8.1.27.4, 文件頁 712-713,720, PDF 頁 738-739,746

### Q28. 「用 state、log、AER 重建背景作業」最容易出現什麼誤判？如何排查？

<!-- qa:base-boot-telemetry-sanitize-sanitize-state-pitfall -->

**答。**

保存 SCDW10、SOS、SANS、FAILS、MVCNCLD 與事件 timestamp。只記錄『完成事件』會把成功、失敗及進入驗證混成同一結論。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26.1; 8.1.27.1, 文件頁 451,712-713, PDF 頁 477,738-739; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4, 文件頁 719-730, PDF 頁 745-756; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4.6-8.1.27.4.7, 文件頁 727-730, PDF 頁 753-756; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, 文件頁 313-319, PDF 頁 339-345; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38; 8.1.27.3, 文件頁 314-319,718, PDF 頁 340-345,744; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.1; 8.1.27.4, 文件頁 712-713,720, PDF 頁 738-739,746

### Q29. 「操作限制與驗證讀取」的核心判讀規則是什麼？

<!-- qa:base-boot-telemetry-sanitize-sanitize-read-lead -->

**答。**

把 command allowlist 與 NVM Read 特例分開判斷。Host 先辨識 target/state，再確認 PI checking 與 allocation，不能把平常 read 的處理完全套入驗證狀態。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.5; 5.1.1-5.1.2, 文件頁 178-181,730-732, PDF 頁 204-207,756-758; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.5, 文件頁 730-732, PDF 頁 756-758; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.7; 5.12, 文件頁 113,173-175, PDF 頁 113,173-175; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12, 文件頁 174, PDF 頁 174; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12.1, 文件頁 174-175, PDF 頁 174-175; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.1; 8.1.27.4.2, 文件頁 587,721, PDF 頁 613,747

### Q30. 「操作限制與驗證讀取」中，哪些概念或條件必須分開比較？

<!-- qa:base-boot-telemetry-sanitize-sanitize-read-rows -->

**答。**

- PI checking requested — Invalid Field in Command — 驗證讀取不允許此組合
- Allocated media readable — 回實際 media data — 可忽略可讀情況的 integrity error
- Allocated media unreadable — Unrecovered Read Error — 不可假造資料
- Deallocated LBA — 依 deallocated/unwritten 規則 — 不是檢查原始 media pattern 的證據

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.5; 5.1.1-5.1.2, 文件頁 178-181,730-732, PDF 頁 204-207,756-758; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.5, 文件頁 730-732, PDF 頁 756-758; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.7; 5.12, 文件頁 113,173-175, PDF 頁 113,173-175; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12, 文件頁 174, PDF 頁 174; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12.1, 文件頁 174-175, PDF 頁 174-175; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.1; 8.1.27.4.2, 文件頁 587,721, PDF 頁 613,747

### Q31. 「操作限制與驗證讀取」如何套用到具體數值或操作情境？

<!-- qa:base-boot-telemetry-sanitize-sanitize-read-example -->

**答。**

驗證讀取 PRCHK=000b、STC=0，所有 allocated LBAs 都能讀取，且沒有其他 abort 原因時，預期 Successful Media Verification Read。只要請求 PI checking，預期分支即改為 Invalid Field in Command。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.5; 5.1.1-5.1.2, 文件頁 178-181,730-732, PDF 頁 204-207,756-758; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.5, 文件頁 730-732, PDF 頁 756-758; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.7; 5.12, 文件頁 113,173-175, PDF 頁 113,173-175; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12, 文件頁 174, PDF 頁 174; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12.1, 文件頁 174-175, PDF 頁 174-175; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.1; 8.1.27.4.2, 文件頁 587,721, PDF 頁 613,747

### Q32. 「操作限制與驗證讀取」最容易出現什麼誤判？如何排查？

<!-- qa:base-boot-telemetry-sanitize-sanitize-read-pitfall -->

**答。**

不要在 subsystem sanitize 期間假設所有 Get Log Page 都允許；07h/08h 不在 Figure 144 清單。Namespace sanitize 的限制必須另外以 attached/target 範圍判斷。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.5; 5.1.1-5.1.2, 文件頁 178-181,730-732, PDF 頁 204-207,756-758; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.5, 文件頁 730-732, PDF 頁 756-758; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.7; 5.12, 文件頁 113,173-175, PDF 頁 113,173-175; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12, 文件頁 174, PDF 頁 174; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12.1, 文件頁 174-175, PDF 頁 174-175; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.1; 8.1.27.4.2, 文件頁 587,721, PDF 頁 613,747
