---
permalink: /nvme/nvm-command-set-1-3-zh-tw/
layout: post
read_time: true
show_date: true
title: "NVM Command Set 1.3：完整獨立教學與工程查詢"
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
[English]({% post_url 2026-09-03-nvme-nvm-command-set-1-3-en %})


# NVM Command Set 1.3：完整獨立教學與工程查詢

用途：供 GitHub Pages 閱讀與 100 分鐘簡報製作；讀者已具備 PCIe 與 NVMe 基礎。

範圍：NVM Command Set 1.3 第 1–5 章與 Appendix A，以及必要 Base 相依圖表；各節只保留本機／PCIe 與傳輸無關的共同語意，包含 §5.4 的 memory-based 範本。正文只保留 PCIe／memory-based 與通用 NVMe 內容。

## 來源版本

NVM Express NVM Command Set Specification, Revision 1.3
NVM Express Base Specification, Revision 2.4

查證日期：2026-09-03。目前未納入其他 Errata、ECN、Technical Proposal、controller vendor 文件或未提供的 PCI Express Base Specification 原文。

## 閱讀地圖

```text
Namespace and format -> Command and limits -> Protection and placement -> Completion and evidence
```

先辨識 namespace 與資料格式，再建立命令；依支援能力套用完整性、配置與管理規則，最後以 CQE、Identify、log 與事件查核結果。

## 規範性用語

shall 譯為「必須」，may 譯為「可／得」，should 譯為「宜／建議」，optional 譯為「選用」。本文不提高或降低原文語氣。

## 先學縮寫：完整 Glossary

下列縮寫會在投影片主線使用前先定義。縮寫本身永遠不夠；設計與 Debug 還要保留 owner、width、unit、scope 與 state。

| 縮寫／名詞 | 白話解釋 | 來源 |
|---|---|---|
| `LBA` | Logical Block Address；以所選格式的 block 為單位。 | NVME-NVM-CS-1.3 Rev. 1.3，§1.1-1.6; 4.1.3.9; 4.1.4.8; 4.1.5，文件頁 9-12,73-75,79-83，PDF 頁 9-12,73-75,79-83 |
| `NSZE` | Namespace Size；可定址 logical blocks 總數。 | NVME-NVM-CS-1.3 Rev. 1.3，§2.1.1; 4.1.5.1，文件頁 13-14,85-93，PDF 頁 13-14,85-93 |
| `NCAP` | Namespace Capacity；同時可配置 logical blocks 最大數量。 | NVME-NVM-CS-1.3 Rev. 1.3，§2.1.1; 4.1.5.1，文件頁 13-14,85-93，PDF 頁 13-14,85-93 |
| `NUSE` | Namespace Utilization；目前配置 logical blocks 數量。 | NVME-NVM-CS-1.3 Rev. 1.3，§2.1.1; 4.1.5.1，文件頁 13-14,85-93，PDF 頁 13-14,85-93 |
| `AWUN` | Atomic Write Unit Normal；controller 正常原子寫入大小的 0-based 欄位。 | NVME-NVM-CS-1.3 Rev. 1.3，§2.1.4; 4.1.3.4; 5.9，文件頁 15-21,66-67,165，PDF 頁 15-21,66-67,165 |
| `AWUPF` | Atomic Write Unit Power Fail；失敗條件原子大小的0-based欄位。 | NVME-NVM-CS-1.3 Rev. 1.3，§2.1.4; 4.1.3.4; 5.9，文件頁 15-21,66-67,165，PDF 頁 15-21,66-67,165 |
| `NLB` | Number of Logical Blocks；本報告命令／status descriptors 的該欄為 0-based。DSM 的 LLB 另為1-based。 | NVME-NVM-CS-1.3 Rev. 1.3，§3.3.4; 3.3.6，文件頁 48-51,53-56，PDF 頁 48-51,53-56 |
| `PRACT` | Protection Information Action；依命令與 MS 選擇 PI 處理。 | NVME-NVM-CS-1.3 Rev. 1.3，§2.1.5; 5.3.2-5.3.3，文件頁 21-22,141-152，PDF 頁 21-22,141-152 |
| `PRCHK` | Protection Information Check；Guard、Application、Reference 的檢查 bits。 | NVME-NVM-CS-1.3 Rev. 1.3，§2.1.5; 5.3.2-5.3.3，文件頁 21-22,141-152，PDF 頁 21-22,141-152 |
| `STC` | Storage Tag Check；獨立於三位元 PRCHK，STS=0 時忽略。 | NVME-NVM-CS-1.3 Rev. 1.3，§2.1.5; 5.3.2-5.3.3，文件頁 21-22,141-152，PDF 頁 21-22,141-152 |
| `STS` | Storage Tag Size；固定 Storage/Reference Space 中的高位 bit 數。 | NVME-NVM-CS-1.3 Rev. 1.3，§5.3.1; 4.1.5.3，文件頁 97-102,130-138，PDF 頁 97-102,130-138 |
| `LBADS` | LBA Data Size 的 exponent；資料 bytes=2^LBADS，0表示目前不可用。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.5.1; 4.1.5.3; 5.6，文件頁 85-94,96-102,160-162，PDF 頁 85-94,96-102,160-162 |
| `NLBAF` | 共同屬性 LBA formats 數的 0-based 欄位。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.5.1; 4.1.5.3; 5.6，文件頁 85-94,96-102,160-162，PDF 頁 85-94,96-102,160-162 |
| `NULBAF` | Unique Attribute LBA Formats 的實際數量；可以為0。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.5.1; 4.1.5.3; 5.6，文件頁 85-94,96-102,160-162，PDF 頁 85-94,96-102,160-162 |
| `LBAFEE` | Host 的 LBA Format Extension Enable 宣告。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.2; 4.1.3.7，文件頁 62-63,68-69，PDF 頁 62-63,68-69 |
| `DULBE` | Deallocated or Unwritten Logical Block Error Enable，需 namespace DAE 支援。 | NVME-NVM-CS-1.3 Rev. 1.3，§3.3.3.2.1; 4.1.3.3，文件頁 47-48,66，PDF 頁 47-48,66 |
| `DMRL` | Dataset Management Ranges Limit，實際 range 數上限。 | NVME-NVM-CS-1.3 Rev. 1.3，§3.3.3，文件頁 44-48，PDF 頁 44-48 |
| `FCO` | Fast Copy Only；要求適用來源以 fast copy 方法執行。 | NVME-NVM-CS-1.3 Rev. 1.3，§3.3.2，文件頁 30-44，PDF 頁 30-44 |
| `NSZ` | Namespace Zeroes；要求全 namespace 清零，需額外 capability 與 DEAC 條件。 | NVME-NVM-CS-1.3 Rev. 1.3，§3.3.7-3.3.8，文件頁 56-61，PDF 頁 56-61 |
| `LBACZ` | LBAs Cleared to Zero；成功 NSZ 命令的範圍確認 bit。 | NVME-NVM-CS-1.3 Rev. 1.3，§3.3.7-3.3.8，文件頁 56-61，PDF 頁 56-61 |
| `ATYPE` | Get LBA Status Action Type；02h allocated，10h scan，11h tracked。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.3.6; 4.1.4.5; 4.2.1; 5.2.1，文件頁 67-68,77-79,114-122，PDF 頁 67-68,77-79,114-122 |
| `CMPC` | Completion Condition；描述 Get LBA Status 是否已完成所要求的範圍。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.3.6; 4.1.4.5; 4.2.1; 5.2.1，文件頁 67-68,77-79,114-122，PDF 頁 67-68,77-79,114-122 |
| `BWSF` | Bandwidth Scale Factor；需乘 bandwidth value，單位為 MiB/s 或 GiB/s。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.3.9; 4.1.5.4; 5.10，文件頁 73-75,106,165-168，PDF 頁 73-75,106,165-168 |
| `GC` | Rate Limiting log 的 32-bit Generation Count，用於分段讀取一致性。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.4.8; 5.10.3，文件頁 79-83,168-172，PDF 頁 79-83,168-172 |
| `ESA` | Entry Sequence Attribute；LBA Migration Queue 的 start／stop／suspend／full 標記。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.8; 5.7，文件頁 113-114,162-164，PDF 頁 113-114,162-164 |
| `KPIODAAG` | Key Per I/O Data Access Alignment and Granularity；0-based blocks。 | NVME-NVM-CS-1.3 Rev. 1.3，§5.5; 4.1.5，文件頁 91-92,105,160，PDF 頁 91-92,105,160 |
| `SWS` | Stream Write Size；NVM command-set 單位為 logical blocks。 | NVME-NVM-CS-1.3 Rev. 1.3，§5.2.2.3; 5.13，文件頁 128-129,175，PDF 頁 128-129,175 |

## Visual Atlas：先用圖建立整體位置

每張教學重畫回答不同問題：Architecture 定位元件、Sequence 顯示 ownership、Decode 把 bits 轉成工程值、State 保留 failure evidence；它們不是 Spec 原圖的複製。

### Visual 01: 閱讀地圖與單位

**View type:** `architecture`

```text
1. Namespace
2. Format
3. Command
4. Completion
5. Evidence
```

**回答的問題：** 本份從 namespace 與資料格式一路走到命令完成、資料完整性及管理證據。主線可分四堂各約 25 分鐘；逐圖附錄與問答供課後查詢。章節 1 的名詞與引用慣例也是範圍的一部分。

**支援 Figure：** Figure 1, Figure 2

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§1.1-1.6; 4.1.3.9; 4.1.4.8; 4.1.5，文件頁 9-12,73-75,79-83，PDF 頁 9-12,73-75,79-83

### Visual 02: Namespace 容量與配置狀態

**View type:** `architecture`

```text
1. NSID
2. NSZE
3. NCAP
4. NUSE
5. Allocation
```

**回答的問題：** 先區分 logical address space 與實際配置，再分析寫入及 deallocate。讀取值與 allocation 狀態回答不同問題。

**支援 Figure：** Figure 123

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§2.1.1; 4.1.5.1，文件頁 13-14,85-93，PDF 頁 13-14,85-93

### Visual 03: 命令順序與 Compare-and-Write

**View type:** `architecture`

```text
1. Host dependency
2. Compare
3. Match gate
4. Write
5. Two CQEs
```

**回答的問題：** 先說明何時要排序，再判斷是否需要條件式更新。Fused 保護同一 LBA range 的比對與更新，原子大小仍須另外檢查。

**支援 Figure：** Figure 3

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§2.1.2-2.1.3，文件頁 14-15，PDF 頁 14-15

### Visual 04: 正常、斷電與多段原子性

**View type:** `architecture`

```text
1. NSABP
2. Decode size
3. Check boundaries
4. MAM or single
5. Failure outcome
```

**回答的問題：** 把大小、起始對齊、NSABP 與 MAM 一起讀。Atomicity 與資料已進入 nonvolatile media 是不同檢查項目，FUA／Flush 也不建立其他命令的排序。

**支援 Figure：** Figure 4, Figure 5, Figure 6, Figure 7, Figure 8, Figure 9, Figure 10

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§2.1.4; 4.1.3.4; 5.9，文件頁 15-21,66-67,165，PDF 頁 15-21,66-67,165

### Visual 05: 能力探索、Opcode 與狀態

**View type:** `architecture`

```text
1. Controller type
2. Capability
3. Opcode and NSID
4. SCT plus SC
5. Recovery
```

**回答的問題：** 從 controller 類型開始建立命令、Feature、log 的能力矩陣。資料指標指向的可能是使用者資料，也可能只是控制 descriptor。

**支援 Figure：** Figure 13, Figure 14, Figure 15, Figure 16, Figure 17, Figure 18, Figure 19, Figure 20, Figure 22

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§2.2; 3.1; 3.3，文件頁 22-27，PDF 頁 22-27

### Visual 06: Read／Write 的資料與完成條件

**View type:** `architecture`

```text
1. Range
2. Buffer layout
3. PI and FUA
4. Execute
5. CQE
```

**回答的問題：** 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。

**支援 Figure：** Figure 50, Figure 51, Figure 52, Figure 53, Figure 54, Figure 55, Figure 56, Figure 57, Figure 58, Figure 59, Figure 67, Figure 68, Figure 69, Figure 70, Figure 71, Figure 72, Figure 73, Figure 74, Figure 75, Figure 76

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§3.3.4; 3.3.6，文件頁 48-51,53-56，PDF 頁 48-51,53-56

### Visual 07: Compare 與 Verify 解決不同問題

**View type:** `architecture`

```text
1. Question
2. Compare or Verify
3. PRACT and checks
4. Size gate
5. Status
```

**回答的問題：** 比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。

**支援 Figure：** Figure 23, Figure 24, Figure 25, Figure 26, Figure 27, Figure 28, Figure 29, Figure 30, Figure 31, Figure 60, Figure 61, Figure 62, Figure 63, Figure 64, Figure 65, Figure 66

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§3.3.1; 3.3.5，文件頁 27-30,51-53，PDF 頁 27-30,51-53

### Visual 08: Copy：描述來源、連續目的與部分失敗

**View type:** `architecture`

```text
1. Descriptors
2. Destination range
3. Limits and overlap
4. Copy
5. Partial-result CQE
```

**回答的問題：** 先計算展開後的目的區間，再檢查格式、長度限制、重疊與 atomicity。Copy 可少用 host 資料傳輸，但不是無條件的 transaction。

**支援 Figure：** Figure 32, Figure 33, Figure 34, Figure 35, Figure 36, Figure 37, Figure 38, Figure 39, Figure 40, Figure 41, Figure 42, Figure 43

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§3.3.2，文件頁 30-44，PDF 頁 30-44

### Visual 09: Copy 的 PI 格式相容與轉換

**View type:** `architecture`

```text
1. Source PI
2. Destination PI
3. Matching or corresponding
4. PRACT pair
5. Check and transform
```

**回答的問題：** 以來源與目的是否有 PI 建立四種情況，再決定 PRINFOR.PRACT 與 PRINFOW.PRACT。每個 source 都必須符合選定模式。

**支援 Figure：** Figure 177, Figure 178, Figure 179, Figure 180, Figure 181, Figure 182

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§3.3.2.3-3.3.2.4; 5.3.2.5，文件頁 40-43,146-150，PDF 頁 40-43,146-150

### Visual 10: Dataset Management 與三種 processing limits

**View type:** `architecture`

```text
1. 16-byte ranges
2. Three limits
3. NVMDSMSV
4. Process hints
5. Allocation evidence
```

**回答的問題：** 先計算每個 block 是否同時通過三種 limit，再套用 NVMDSMSV。範圍與 hints 的合法性、處理義務以及實際媒體動作分開判斷。

**支援 Figure：** Figure 44, Figure 45, Figure 46, Figure 47, Figure 48, Figure 49

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§3.3.3，文件頁 44-48，PDF 頁 44-48

### Visual 11: Deallocated／unwritten 讀取規則

**View type:** `architecture`

```text
1. DAE
2. DULBE
3. DRB
4. PI values
5. Deterministic read
```

**回答的問題：** 先判斷是否允許成功讀取，再解釋成功回傳的 bytes。Allocation status、DRB 與 PI 有各自的條件。

**支援 Figure：** 

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§3.3.3.2.1; 4.1.3.3，文件頁 47-48,66，PDF 頁 47-48,66

### Visual 12: Write Uncorrectable、Write Zeroes 與整體清零

**View type:** `architecture`

```text
1. Operation
2. Range or NSZ
3. PI and limits
4. Execute
5. LBACZ and status
```

**回答的問題：** 這兩個命令沒有 host user-data payload，但會改變 namespace 語意。先辨識範圍模式，再分配 PI 與 size-limit 檢查。

**支援 Figure：** Figure 77, Figure 78, Figure 79, Figure 80, Figure 81, Figure 82, Figure 83, Figure 84, Figure 85, Figure 86, Figure 87, Figure 88, Figure 89

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§3.3.7-3.3.8，文件頁 56-61，PDF 頁 56-61

### Visual 13: Format、Host Behavior 與延伸 LBA

**View type:** `architecture`

```text
1. ELBAS
2. LBAFEE
3. LBAF and ELBAF
4. PI and metadata
5. Re-identify
```

**回答的問題：** 格式切換會改變 block 數與欄位適用性，建立 buffer 前要重新 Identify。能力列表與目前格式不能混用。

**支援 Figure：** Figure 91, Figure 101

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.2; 4.1.3.7，文件頁 62-63,68-69，PDF 頁 62-63,68-69

### Visual 14: 基本 Features 的作用域與例外

**View type:** `architecture`

```text
1. Scope
2. Units
3. Select or Set
4. Persistence
5. Returned value
```

**回答的問題：** 讀 Feature 時先辨識 scope、unit 與可儲存條件。Get、Set、Supported Capabilities 回覆也不能套用同一 payload 解碼。

**支援 Figure：** Figure 92, Figure 93, Figure 94, Figure 95, Figure 96, Figure 97, Figure 98

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.3.1-4.1.3.4，文件頁 64-67，PDF 頁 64-67

### Visual 15: Identify：同一 namespace 的多份資料結構

**View type:** `architecture`

```text
1. CNS and CSI
2. NSID or FIDX
3. Independent structure
4. NVM structures
5. Combine capabilities
```

**回答的問題：** 每次查詢都寫出 CNS、CSI、NSID、Format Index 的角色。不同查詢回零有不同含義，不能一律解讀為不存在或不支援。

**支援 Figure：** Figure 122, Figure 126, Figure 129, Figure 130, Figure 131

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.5，文件頁 83-110，PDF 頁 83-110

### Visual 16: LBAF、ELBAF 與唯一屬性格式

**View type:** `architecture`

```text
1. NLBAF plus NULBAF
2. Format Index
3. LBAF
4. ELBAF
5. Availability
```

**回答的問題：** 基本 entry 給資料／metadata 大小與相對效能，extended entry 給 PI 格式與 Storage Tag 分配。Unique-attribute entries 要個別查詢，不能沿用共同能力。

**支援 Figure：** Figure 124, Figure 125, Figure 127, Figure 128, Figure 192, Figure 193

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.5.1; 4.1.5.3; 5.6，文件頁 85-94,96-102,160-162，PDF 頁 85-94,96-102,160-162

### Visual 17: 建立 namespace：格式、mask 與 granularity

**View type:** `architecture`

```text
1. Format capability
2. NSZE and NCAP
3. PI and LBSTM
4. Placement handles
5. Create result
```

**回答的問題：** 先取得 Format Index 能力再填 host-specified fields；不可直接把整份 Identify Namespace 原封不動當作 create payload。

**支援 Figure：** Figure 132, Figure 133, Figure 134

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6; 4.1.5.8; 5.8，文件頁 108,110-113,165，PDF 頁 108,110-113,165

### Visual 18: FDP：placement、RUH 與可觀測數據

**View type:** `architecture`

```text
1. Create placement
2. PID and RUHID
3. Handle status
4. Statistics
5. Media event
```

**回答的問題：** 建立時決定 placement 關係，執行時看 handle status，事後再用 statistics／events 解釋媒體搬移。三種資料不能互相代替。

**支援 Figure：** Figure 21, Figure 116

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§3.2.1; 4.1.4.6-4.1.4.7; 4.1.6.3，文件頁 26,79,110-113，PDF 頁 26,79,110-113

### Visual 19: AER、SMART 與錯誤記錄的 NVM 補充

**View type:** `architecture`

```text
1. Notice enable
2. AER
3. Log scope
4. Validity and units
5. Correlate evidence
```

**回答的問題：** 用事件找調查方向，再用正確 scope 的 log 與 command set 定義解碼。統計數據也要依命令分類，不能只按 opcode 名稱猜。

**支援 Figure：** Figure 90, Figure 99, Figure 109, Figure 110, Figure 111, Figure 112

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§1.4.2; 4.1.1; 4.1.3.5; 4.1.4.1-4.1.4.4，文件頁 10-11,62,67,75-77，PDF 頁 10-11,62,67,75-77

### Visual 20: LBA Status：通知、掃描與修復流程

**View type:** `architecture`

```text
1. LID 0Eh
2. ATYPE
3. Range and MNDW
4. CMPC and descriptors
5. Recover and recheck
```

**回答的問題：** 讀到 potentially unrecoverable 不是每個 block 一定無法讀取。先辨識 ATYPE，再檢查 buffer 是否足夠與 completion condition，最後安排資料修復。

**支援 Figure：** Figure 100, Figure 113, Figure 114, Figure 115, Figure 135, Figure 136, Figure 137, Figure 138, Figure 139, Figure 140, Figure 142, Figure 143, Figure 144

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.3.6; 4.1.4.5; 4.2.1; 5.2.1，文件頁 67-68,77-79,114-122，PDF 頁 67-68,77-79,114-122

### Visual 21: Performance Characteristics 的屬性模型

**View type:** `architecture`

```text
1. Scope
2. ATTRI
3. Current default saved
4. PAID and length
5. Interpretation
```

**回答的問題：** 此 Feature 回報或管理效能屬性，不能把標準 latency 級別當成對任意 workload 的服務保證。

**支援 Figure：** Figure 102, Figure 103, Figure 104, Figure 105

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.3.8，文件頁 69-73，PDF 頁 69-73

### Visual 22: Rate Limiting 的設定欄位

**View type:** `architecture`

```text
1. Supported targets
2. HLS and SLS
3. TGT and TID
4. Limits and ratios
5. Set and Get
```

**回答的問題：** 先從 LID 28h 取得支援 target，再檢查 HLS／SLS 與 soft-controller 數量。把 host 請求限制和裝置可達能力分開記錄。

**支援 Figure：** Figure 106, Figure 107, Figure 108

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.3.9; 4.1.5.4; 5.10，文件頁 73-75,106,165-168，PDF 頁 73-75,106,165-168

### Visual 23: Rate Limiting log 是能力圖

**View type:** `architecture`

```text
1. Header and GC
2. Port offsets
3. Controller offsets
4. Shared storage nodes
5. Bounds and bottleneck
```

**回答的問題：** 先做結構邊界檢查，再分析 bandwidth bottleneck。Port 的能力與共同 Endurance Group 的能力不同，不能把所有數字直接相加。

**支援 Figure：** Figure 117, Figure 118, Figure 119, Figure 120, Figure 121, Figure 195, Figure 196, Figure 197, Figure 198

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.4.8; 5.10.3，文件頁 79-83,168-172，PDF 頁 79-83,168-172

### Visual 24: Hard／Soft 與 token-bucket 算例

**View type:** `architecture`

```text
1. Capabilities
2. Configured limits
3. Actual demand
4. Token admission
5. Completion
```

**回答的問題：** 用能力、limits、實際 demand 三個值判讀結果。設定比例不等於任何時刻都固定吞吐；內部資源與工作負載仍會改變觀測值。

**支援 Figure：** Figure 202

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.10.1-5.10.2; Appendix A，文件頁 166-168,176-177，PDF 頁 166-168,176-177

### Visual 25: 對齊、granularity 與效能提示

**View type:** `architecture`

```text
1. Support bits
2. Decode units
3. Align start
4. Choose length
5. Measure workload
```

**回答的問題：** 先把 raw 欄位轉成 blocks，再評估 start alignment 與 length granularity。只滿足其中一項可能仍引發 read-modify-write。

**支援 Figure：** Figure 145, Figure 146, Figure 147, Figure 148, Figure 149, Figure 150, Figure 151

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.2.2，文件頁 122-129，PDF 頁 122-129

### Visual 26: Metadata 傳輸與 PI 的位置

**View type:** `architecture`

```text
1. Namespace format
2. Data region
3. Metadata region
4. PI suffix
5. Buffer lengths
```

**回答的問題：** Metadata 不一定全是 PI。先標示 data、非 PI metadata 與 PI 三個區域，再計算 host buffer 大小與 CRC coverage。

**支援 Figure：** Figure 153, Figure 154

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§2.1.6; 5.2.3; 5.3，文件頁 22,129-131，PDF 頁 22,129-131

### Visual 27: 16／32／64b Guard 與 Qualified PI

**View type:** `architecture`

```text
1. DPS type
2. PIF or QPIF
3. Guard size
4. STS split
5. Mask capability
```

**回答的問題：** 先由 PIF 決定格式；PIF=11b 才由 QPIF 決定 Guard width，並受 QPIFS 與 STMLA 條件限制。Protection type 仍由 DPS 決定。

**支援 Figure：** Figure 155, Figure 156, Figure 157, Figure 159, Figure 164, Figure 165

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.3.1; 4.1.5.3，文件頁 97-102,130-138，PDF 頁 97-102,130-138

### Visual 28: CRC 參數、位元順序與已知向量

**View type:** `architecture`

```text
1. Data and metadata
2. Initialization
3. Polynomial and reflection
4. Final XOR
5. Known vectors
```

**回答的問題：** CRC 的 polynomial、初值、reflection、final XOR 與儲存順序必須一起核對。用已知向量驗證後才接進 PI parser。

**支援 Figure：** Figure 158, Figure 160, Figure 161, Figure 162, Figure 163

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.3.1.1-5.3.1.3，文件頁 131-137，PDF 頁 131-137

### Visual 29: Storage／Reference Tag 的 Dword 封裝

**View type:** `architecture`

```text
1. PI space width
2. STS
3. Storage and reference
4. CDW2 and CDW3
5. CDW14
```

**回答的問題：** 先決定總 space 大小，再切 tag，最後拆到命令 Dwords。不要因 tag 的名稱相似就把 Write 的值與 Read 的 expected 值交換。

**支援 Figure：** Figure 166, Figure 167, Figure 168, Figure 169, Figure 170, Figure 171, Figure 172, Figure 173

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.3.1.4，文件頁 137-141，PDF 頁 137-141

### Visual 30: PRACT 與 PRCHK／STC 的組合

**View type:** `architecture`

```text
1. PI enabled
2. PRACT
3. Metadata size
4. PRCHK and STC
5. Status
```

**回答的問題：** 先檢查 namespace 是否啟用 PI，再依命令方向及 metadata 大小選處理分支。Checking bits 與可能的特殊停用值放在最後判斷。

**支援 Figure：** Figure 11, Figure 12, Figure 174, Figure 175, Figure 176

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§2.1.5; 5.3.2-5.3.3，文件頁 21-22,141-152，PDF 頁 21-22,141-152

### Visual 31: ANA 與 Reservations 的 NVM 行為

**View type:** `architecture`

```text
1. Namespace
2. ANA state
3. Reservation type
4. Holder and registrant
5. Command permission
```

**回答的問題：** 同一 namespace 的可達性與存取權限要分開檢查；不能將路徑狀態等同 reservation ownership。

**支援 Figure：** Figure 141, Figure 199

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.1; 5.11，文件頁 119,172-173，PDF 頁 119,172-173

### Visual 32: LBA Migration Queue 與變更追蹤

**View type:** `architecture`

```text
1. Track Send
2. Changes take effect
3. Range entries
4. Phase and sequence
5. Full or stop
```

**回答的問題：** 這個 queue 保存變更範圍與序列標記，不保存完整新資料。Host 讀 entry 後仍需以適當 I/O 取得資料，並處理滿 queue 的停止邊界。

**支援 Figure：** Figure 194

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.8; 5.7，文件頁 113-114,162-164，PDF 頁 113-114,162-164

### Visual 33: Sanitize 與 Media Verification 的 NVM 規則

**View type:** `architecture`

```text
1. Target and state
2. LID81h
3. Allocation
4. Verification Read
5. Result interpretation
```

**回答的問題：** 先辨識 target、operation state 與 allocation，再決定可以驗證什麼。命令 CQE 與 sanitize operation 完成分別由不同證據表示。

**支援 Figure：** Figure 200, Figure 201

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.7; 5.12，文件頁 113,173-175，PDF 頁 113,173-175

### Visual 34: Key Per I/O 的 NVM 對齊約束

**View type:** `architecture`

```text
1. Capability
2. Namespace enablement
3. CETYPE and CEV
4. KPIODAAG
5. Status
```

**回答的問題：** 先從 KPIOCAP 與 namespace status 判斷適用，再解讀 CETYPE／CEV 的 command extension。金鑰建立及管理不由這份 NVM 補充完整定義。

**支援 Figure：** 

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.5; 4.1.5，文件頁 91-92,105,160，PDF 頁 91-92,105,160

### Visual 35: Streams 的 NVM 單位與優先順序

**View type:** `architecture`

```text
1. SWS blocks
2. SGS multiplier
3. Stream granularity
4. Namespace hints
5. Workload
```

**回答的問題：** 用兩層大小模型解釋 Stream Write Size 與較大的 stream granularity。它們可能和 namespace hints 成整數倍，但規格不保證每個 namespace 都如此。

**支援 Figure：** Figure 152

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.2.2.3; 5.13，文件頁 128-129,175，PDF 頁 128-129,175

### Visual 36: Memory-based 資源匯出範本

**View type:** `architecture`

```text
1. Underlying capability
2. Template and TR
3. IDs 0 and 1
4. Set once
5. Reported interface
```

**回答的問題：** 範本固定的相容性介面與 underlying 裝置能力是兩層。先確認 namespace 格式相容，再設定不超過 underlying 能力的限制；沒有被範本開放的能力不能自行宣告。

**支援 Figure：** Figure 183, Figure 184, Figure 185, Figure 186, Figure 187, Figure 188, Figure 189, Figure 190

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.4.1-5.4.1.1，文件頁 152-159，PDF 頁 152-159

### Visual 37: 匯出狀態的長度與一致性

**View type:** `architecture`

```text
1. Current features
2. CP evidence
3. NVMECSS dwords
4. Bounds
5. Nested VER
```

**回答的問題：** 先讀固定 64-byte header，再檢查可變長度與 suspension 證據。Configuration state 與執行中 state 的用途和設定限制不同，不能共用 payload parser。

**支援 Figure：** Figure 191

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.4.1.2，文件頁 159-160，PDF 頁 159-160

## Mental Model 與完整教學流程

以下依工程因果而非 Spec section 排列；相關 Figure 會回到它支援的流程節點，不以編號順序取代教學故事線。

### Module 01: 閱讀地圖與單位

**解釋。** 本份從 namespace 與資料格式一路走到命令完成、資料完整性及管理證據。主線可分四堂各約 25 分鐘；逐圖附錄與問答供課後查詢。章節 1 的名詞與引用慣例也是範圍的一部分。

```text
Namespace
  ↓
Format
  ↓
Command
  ↓
Completion
  ↓
Evidence
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| LBADS | data bytes = 2^LBADS | 另加 MS 才是 logical block size |
| Format Index | 同時選 LBAF 與 ELBAF | 不能只看資料大小 |
| Specification family | 通用機制由 Base 定義 | 相依欄位另以 Base 來源標示 |

**說明性範例。** LBADS=0Ch、MS=16 時，資料為 4096 bytes，含 metadata 的 logical block 是 4112 bytes。FID 28h 與 LID 28h 雖相同，前者設定限制，後者回報能力圖。

**常見誤解／Debug。** 本報告的算例是教學推導；不把示意數值寫成裝置必須具備的能力。對規格的 should、may 與 shall 保留不同強度。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§1.1-1.6; 4.1.3.9; 4.1.4.8; 4.1.5，文件頁 9-12,73-75,79-83，PDF 頁 9-12,73-75,79-83

**關聯 Figure：** Figure 1, Figure 2

### Module 02: Namespace 容量與配置狀態

**解釋。** 先區分 logical address space 與實際配置，再分析寫入及 deallocate。讀取值與 allocation 狀態回答不同問題。

```text
NSID
  ↓
NSZE
  ↓
NCAP
  ↓
NUSE
  ↓
Allocation
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| NSZE | 有效 LBA 為 0 到 NSZE−1 | LBA 越界與容量不足不同 |
| THINP | 支援時須追蹤 NUSE | 不支援時可固定回 NCAP |
| Allocation | Write、Copy 寫入端及 WU 可配置 | Read／Verify 不改 deallocation 狀態 |

**說明性範例。** NSZE=1000、NCAP=800、NUSE=600 可是合法 thin namespace。LBA 900 在可定址範圍內，但新增配置仍受 800-block capacity 限制。

**常見誤解／Debug。** ANA 狀態可使 NUSE／NVMCAP 回零；不可僅憑回零宣告資料已刪除。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§2.1.1; 4.1.5.1，文件頁 13-14,85-93，PDF 頁 13-14,85-93

**關聯 Figure：** Figure 123

### Module 03: 命令順序與 Compare-and-Write

**解釋。** 先說明何時要排序，再判斷是否需要條件式更新。Fused 保護同一 LBA range 的比對與更新，原子大小仍須另外檢查。

```text
Host dependency
  ↓
Compare
  ↓
Match gate
  ↓
Write
  ↓
Two CQEs
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Ordinary I/O | 同 LBA 的 Read／Write 完成先後無保證 | host 以完成相依控制 |
| Fused pair | Compare 與 Write 的 range 相同 | 範圍不符 should 拒絕 |
| ACWU / NACWU | 限制 fused atomic update 大小 | 還要遵守 atomic boundaries |

**說明性範例。** Host 想「目前值等於 A 才更新 B」時，獨立 Compare 成功後再送 Write 中間仍可能插入別人的寫入；符合大小與邊界的 fused pair 才提供此操作所需的條件式原子更新。

**常見誤解／Debug。** Write 失敗不會回頭改寫 Compare 已得到的 completion status；必須檢查兩個 CQE。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§2.1.2-2.1.3，文件頁 14-15，PDF 頁 14-15

**關聯 Figure：** Figure 3

### Module 04: 正常、斷電與多段原子性

**解釋。** 把大小、起始對齊、NSABP 與 MAM 一起讀。Atomicity 與資料已進入 nonvolatile media 是不同檢查項目，FUA／Flush 也不建立其他命令的排序。

```text
NSABP
  ↓
Decode size
  ↓
Check boundaries
  ↓
MAM or single
  ↓
Failure outcome
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| AWUN / AWUPF | 大小採 0-based 編碼 | AWUPF 不大於 AWUN |
| NABO / NABSN / NABSPF | 邊界在 offset + k × size | 需依各欄位解碼與未回報規則 |
| MAM | 每個 atomic subrange 獨立保證 | fused 仍用 Single 模式 |
| FID 0Ah.DN | DN=1 可不遵守 normal atomicity | 仍須遵守 power-fail 保證 |

**說明性範例。** 假設解碼後 boundary size=8 blocks、offset=0，從 LBA 4 寫 12 blocks 跨成 [4..7] 與 [8..15]。MAM 下各段原子，不能將兩段當作一個 transaction。原始 AWUN=7h 才代表 8 blocks。

**常見誤解／Debug。** 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§2.1.4; 4.1.3.4; 5.9，文件頁 15-21,66-67,165，PDF 頁 15-21,66-67,165

**關聯 Figure：** Figure 4, Figure 5, Figure 6, Figure 7, Figure 8, Figure 9, Figure 10

### Module 05: 能力探索、Opcode 與狀態

**解釋。** 從 controller 類型開始建立命令、Feature、log 的能力矩陣。資料指標指向的可能是使用者資料，也可能只是控制 descriptor。

```text
Controller type
  ↓
Capability
  ↓
Opcode and NSID
  ↓
SCT plus SC
  ↓
Recovery
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Read 02h / Write 01h | 必要 I/O 命令 | Administrative controller 不處理 I/O |
| Get LBA Status 86h | 選用 Admin 命令 | I/O controller 適用能力 |
| SC 80h | 依 SCT 區分 LBA Out of Range 等 | 同時記錄 opcode、NSID、SCT、SC、DNR |
| FID / LID | 05h、0Ah 為必要 NVM Features | 功能支援不等於要求寫入 Persistent Event Log |

**說明性範例。** Copy opcode=19h 的低 bits 是 01b，因 host 傳入 source descriptors；並不表示需要把整份待複製資料從 host 再傳一次。

**常見誤解／Debug。** FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§2.2; 3.1; 3.3，文件頁 22-27，PDF 頁 22-27

**關聯 Figure：** Figure 13, Figure 14, Figure 15, Figure 16, Figure 17, Figure 18, Figure 19, Figure 20, Figure 22

### Module 06: Read／Write 的資料與完成條件

**解釋。** 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。

```text
Range
  ↓
Buffer layout
  ↓
PI and FUA
  ↓
Execute
  ↓
CQE
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| CDW10 / CDW11 | SLBA 低／高 32 bits | NLB=0 仍有一個 block |
| CDW12 | LR、FUA、PRINFO、STC、CETYPE、NLB | Read 的 DTYPE 區是 reserved |
| CDW13 | CETYPE 決定 DSM 或 CEV 解讀 | Write 另含 DTYPE／DSPEC |
| MPTR | 單獨傳 metadata 時使用 | 不可把一部分 metadata 分到兩種機制 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解／Debug。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§3.3.4; 3.3.6，文件頁 48-51,53-56，PDF 頁 48-51,53-56

**關聯 Figure：** Figure 50, Figure 51, Figure 52, Figure 53, Figure 54, Figure 55, Figure 56, Figure 57, Figure 58, Figure 59, Figure 67, Figure 68, Figure 69, Figure 70, Figure 71, Figure 72, Figure 73, Figure 74, Figure 75, Figure 76

### Module 07: Compare 與 Verify 解決不同問題

**解釋。** 比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。

```text
Question
  ↓
Compare or Verify
  ↓
PRACT and checks
  ↓
Size gate
  ↓
Status
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Compare | miscompare 回 Compare Failure | host 與 media 兩側 PI 可分別檢查 |
| Verify | 沒有資料 buffer 傳輸 | 驗證量仍計入 Data Units Read |
| VSL / NVMVFYS | variant 決定建議大小或硬上限 | 非零 VSL 以 2^n × minimum page size 表示 |

**說明性範例。** 要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。

**常見誤解／Debug。** Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§3.3.1; 3.3.5，文件頁 27-30,51-53，PDF 頁 27-30,51-53

**關聯 Figure：** Figure 23, Figure 24, Figure 25, Figure 26, Figure 27, Figure 28, Figure 29, Figure 30, Figure 31, Figure 60, Figure 61, Figure 62, Figure 63, Figure 64, Figure 65, Figure 66

### Module 08: Copy：描述來源、連續目的與部分失敗

**解釋。** 先計算展開後的目的區間，再檢查格式、長度限制、重疊與 atomicity。Copy 可少用 host 資料傳輸，但不是無條件的 transaction。

```text
Descriptors
  ↓
Destination range
  ↓
Limits and overlap
  ↓
Copy
  ↓
Partial-result CQE
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| NR / NLB | source count 與各範圍 block count 都是 0-based | 檢查 MSRC、MSSRL、MCL |
| FCO | 2h/3h 可要求 fast copy only | Fast Copy Not Possible 再看 DNR |
| Overlap | 2h/3h 禁止同 namespace source 與 destination 重疊 | 0h/1h 重疊結果需依原子條件另讀 |
| NVMCSA | 1.3 將目的寫入視為單一 write command | 仍受 MAM、大小及 boundary 限制 |

**說明性範例。** 兩個 source descriptors 的 NLB 都是 3，SDLBA=100：第一段寫 100..103、第二段寫 104..107，共 8 blocks。若 DW0=1，不能據此保證第二段或更後面完全未修改。

**常見誤解／Debug。** FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§3.3.2，文件頁 30-44，PDF 頁 30-44

**關聯 Figure：** Figure 32, Figure 33, Figure 34, Figure 35, Figure 36, Figure 37, Figure 38, Figure 39, Figure 40, Figure 41, Figure 42, Figure 43

### Module 09: Copy 的 PI 格式相容與轉換

**解釋。** 以來源與目的是否有 PI 建立四種情況，再決定 PRINFOR.PRACT 與 PRINFOW.PRACT。每個 source 都必須符合選定模式。

```text
Source PI
  ↓
Destination PI
  ↓
Matching or corresponding
  ↓
PRACT pair
  ↓
Check and transform
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| PI → PI, 0/0 | matching formats：pass-through | 保護檢查仍由 checking bits 控制 |
| PI → PI, 1/1 | matching formats：replace | 讀端檢查，寫端產生 PI |
| No PI → PI | corresponding formats 且 write PRACT=1：insert | 目的 metadata 不得包含其他用途 |
| PI → No PI | corresponding formats 且 read PRACT=1：strip | 來源 metadata 只能是 PI |

**說明性範例。** 4096+8 bytes 的 16b PI namespace 可在符合 corresponding 條件時轉到 4096+0 bytes；4096+16 bytes 且其中 8 bytes 是額外 metadata，不能走這個 strip 特例。

**常見誤解／Debug。** §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§3.3.2.3-3.3.2.4; 5.3.2.5，文件頁 40-43,146-150，PDF 頁 40-43,146-150

**關聯 Figure：** Figure 177, Figure 178, Figure 179, Figure 180, Figure 181, Figure 182

### Module 10: Dataset Management 與三種 processing limits

**解釋。** 先計算每個 block 是否同時通過三種 limit，再套用 NVMDSMSV。範圍與 hints 的合法性、處理義務以及實際媒體動作分開判斷。

```text
16-byte ranges
  ↓
Three limits
  ↓
NVMDSMSV
  ↓
Process hints
  ↓
Allocation evidence
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| AD / IDW / IDR | deallocate／整體寫入／整體讀取 hints | 可組合使用 |
| Limits nonzero, variant=0 | 超過任一 limit 回 Command Size Limit Exceeded | 全部符合則須處理 attributes |
| Limits nonzero, variant=1 | 宜處理符合 limits 的部分 | 不以此原因回 Size Limit Exceeded |
| All limits=0 | variant=1：不回報 limits；variant=0：不支援 | 三欄需全零或全非零 |

**說明性範例。** DMRL=2、DMSL=1048，range 0 有 1024 blocks、range 1 有 512，且 DMRSL 不限制：variant=1 時前段與後段前 24 blocks 符合 limits。這不等於保證 1048 blocks 都已釋放。

**常見誤解／Debug。** 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§3.3.3，文件頁 44-48，PDF 頁 44-48

**關聯 Figure：** Figure 44, Figure 45, Figure 46, Figure 47, Figure 48, Figure 49

### Module 11: Deallocated／unwritten 讀取規則

**解釋。** 先判斷是否允許成功讀取，再解釋成功回傳的 bytes。Allocation status、DRB 與 PI 有各自的條件。

```text
DAE
  ↓
DULBE
  ↓
DRB
  ↓
PI values
  ↓
Deterministic read
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| DAE / DULBE | DAE 是 capability，DULBE 是啟用 | DULBE 預設 0 |
| DRB=000b | 不是任意舊資料 | 依 §3.3.3.2.1 為零或 FFh |
| PI after deallocation | tag bytes 回 FFh；Guard 為 FFh 或 CRC | 配合 DLFEAT.GDS |

**說明性範例。** 一次 Read 全零不能證明 sanitize 成功，可能只是 deallocated 的 DRB。反過來 DULBE 啟用後讀取報錯，也不能單凭此錯誤認定媒體故障。

**常見誤解／Debug。** Read／Verify 成功不會使該 block 變回 allocated；重新寫入才會改變這個狀態。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§3.3.3.2.1; 4.1.3.3，文件頁 47-48,66，PDF 頁 47-48,66

**關聯 Figure：** 

### Module 12: Write Uncorrectable、Write Zeroes 與整體清零

**解釋。** 這兩個命令沒有 host user-data payload，但會改變 namespace 語意。先辨識範圍模式，再分配 PI 與 size-limit 檢查。

```text
Operation
  ↓
Range or NSZ
  ↓
PI and limits
  ↓
Execute
  ↓
LBACZ and status
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Write Uncorrectable | 標記 block 後，讀取可能報 Unrecovered Read Error | WUSL 與 NVMWUSV 需成對看 |
| Write Zeroes PI | PRCHK=000b、STC=0 | PRACT=1 宜用於產生有效 PI |
| WZSL / WZDSL | 依 DEAC 選適用 limit | NSZ=1 不受這兩欄限制 |
| LBACZ | 成功 NSZ 命令回 1 才表示全 namespace | 回 0 是指定 range |

**說明性範例。** Host 送 NSZ=1 後得到 Successful Completion 與 LBACZ=0，必須判為僅 range 被清零；舊 controller 可能忽略不支援的 NSZ。不能將 command success 自動升格為整個 namespace 清零。

**常見誤解／Debug。** DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§3.3.7-3.3.8，文件頁 56-61，PDF 頁 56-61

**關聯 Figure：** Figure 77, Figure 78, Figure 79, Figure 80, Figure 81, Figure 82, Figure 83, Figure 84, Figure 85, Figure 86, Figure 87, Figure 88, Figure 89

### Module 13: Format、Host Behavior 與延伸 LBA

**解釋。** 格式切換會改變 block 數與欄位適用性，建立 buffer 前要重新 Identify。能力列表與目前格式不能混用。

```text
ELBAS
  ↓
LBAFEE
  ↓
LBAF and ELBAF
  ↓
PI and metadata
  ↓
Re-identify
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| PI / PIL | PI=0 關閉，1/2/3 選 protection type | 本版 PIL 必須 0，PI 位於末端 |
| MSET | 1：extended LBA；0：separate metadata | MS=0 時忽略 |
| LBAFEE | FID 16h byte 2，合法值 0／1 | 配合 ELBAS 決定延伸格式 |
| STS | Format 不提供自由改成非零 STS 的方法 | 新配置可由 namespace create 建立 |

**說明性範例。** 要使用 64b Guard、MS=16 的格式，先確認 ELBAS、LBAFEE=1、對應 LBAF／ELBAF 及 PI capability。不能只設定 Format 的 PI=1 就宣告 64b Guard。

**常見誤解／Debug。** PI type 1/2/3 與 Guard width 16/32/64 是不同維度。格式變更後 NSZE／NCAP 可改變，舊 LBA Range Type hints 也可能需重設。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.2; 4.1.3.7，文件頁 62-63,68-69，PDF 頁 62-63,68-69

**關聯 Figure：** Figure 91, Figure 101

### Module 14: 基本 Features 的作用域與例外

**解釋。** 讀 Feature 時先辨識 scope、unit 與可儲存條件。Get、Set、Supported Capabilities 回覆也不能套用同一 payload 解碼。

```text
Scope
  ↓
Units
  ↓
Select or Set
  ↓
Persistence
  ↓
Returned value
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| FID 03h | 4096-byte contiguous buffer；最多 64 個 64-byte entries | NUM 是 0-based；新 Set 取代前一次 |
| FID 05h.TLER | 100 ms 單位，從 error recovery 開始計時 | 0 代表不設 timeout；適用 LR 命令 |
| FID 03h attributes | Hide／Overwriteable 是 host 使用提示 | 不是安全隔離或資料保護機制 |
| FID 02h extension | idle exit 參考 NPWG-sized Read | 其他命令可超過該 latency limit |

**說明性範例。** TLER=5 表示 error recovery 的 500 ms 限制，並不是從 SQ submit 起算的整筆命令 500 ms deadline。LBA Range Type 的 NUM=0 表示一個 entry。

**常見誤解／Debug。** Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.3.1-4.1.3.4，文件頁 64-67，PDF 頁 64-67

**關聯 Figure：** Figure 92, Figure 93, Figure 94, Figure 95, Figure 96, Figure 97, Figure 98

### Module 15: Identify：同一 namespace 的多份資料結構

**解釋。** 每次查詢都寫出 CNS、CSI、NSID、Format Index 的角色。不同查詢回零有不同含義，不能一律解讀為不存在或不支援。

```text
CNS and CSI
  ↓
NSID or FIDX
  ↓
Independent structure
  ↓
NVM structures
  ↓
Combine capabilities
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| CNS 00h / 05h | namespace 的 NVM 基本／延伸欄位 | FLBAS 決定目前 FIDX；MC／DPC 是能力 |
| CNS 01h / 06h | AWUN 等通用位置與 NVM 專屬限制 | 06h 的 VSL／WZSL 等需結合 variant bits |
| CNS 11h / 1Bh | allocated namespace 資訊 | 不等同 active namespace 查詢 |
| CNS 09h / 0Ah | 以 FIDX 查能力 | Common=No 欄位清零 |
| CNS 16h | namespace granularity list | GDM 決定 descriptor 如何對應 format |

**說明性範例。** NSID=7 的目前格式需讀 FLBAS 再取同 index 的 LBAF 與 ELBAF。查尚未建立的 FIDX=3 能力，使用 09h／0Ah、CSI=0、NSID=0、FIDX=3，另結合 CNS08h 的共同能力。

**常見誤解／Debug。** §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.5，文件頁 83-110，PDF 頁 83-110

**關聯 Figure：** Figure 122, Figure 126, Figure 129, Figure 130, Figure 131

### Module 16: LBAF、ELBAF 與唯一屬性格式

**解釋。** 基本 entry 給資料／metadata 大小與相對效能，extended entry 給 PI 格式與 Storage Tag 分配。Unique-attribute entries 要個別查詢，不能沿用共同能力。

```text
NLBAF plus NULBAF
  ↓
Format Index
  ↓
LBAF
  ↓
ELBAF
  ↓
Availability
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| LBAF | LBADS、MS、RP | RP 是指定 workload 的相對級別 |
| ELBAF | PIF、QPIF、STS | QPIF 只在 qualified type 下適用 |
| FLBAS | FIDXU 與 FIDXL 組成 index | MTELBA 是另一個 metadata bit |
| NULBAF | 追加在共同格式之後 | 09h／0Ah 能讀各自能力 |

**說明性範例。** raw NLBAF=3、NULBAF=2：有 4 個共同格式及 2 個唯一屬性格式，共 6 個，合法 index 為 0..5。Figure 192 圖示採概念数量，不能直接代入未解碼的 raw NLBAF。

**常見誤解／Debug。** LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.5.1; 4.1.5.3; 5.6，文件頁 85-94,96-102,160-162，PDF 頁 85-94,96-102,160-162

**關聯 Figure：** Figure 124, Figure 125, Figure 127, Figure 128, Figure 192, Figure 193

### Module 17: 建立 namespace：格式、mask 與 granularity

**解釋。** 先取得 Format Index 能力再填 host-specified fields；不可直接把整份 Identify Namespace 原封不動當作 create payload。

```text
Format capability
  ↓
NSZE and NCAP
  ↓
PI and LBSTM
  ↓
Placement handles
  ↓
Create result
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| NSZE / NCAP | 值以 logical blocks 指定 | 與 bytes granularity 比較前先換算 |
| LBSTM | 需符合 PIC／PIFA mask 約束 | 不符回 Invalid Field in Command |
| GDM / ND | GDM=0 使用 descriptor 0 對全部格式 | ND 是 0-based |
| Completion | 成功 create 後已按指定屬性 format | attachment 是另一個管理動作 |

**說明性範例。** 假設 NSG=1 MiB、NCG=1 MiB、logical block size=4096，NSZE=NCAP=256 的容量可完整定址；若改成 257，granularity hints 可能造成額外不可定址配置，但本身不是拒絕理由。

**常見誤解／Debug。** Masking Not Supported 代表 Storage Tag mask 有效 bits 全為 1；不是全零。不支援或未啟用 FDP 時，placement 欄位也不能套用啟用後的語意。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6; 4.1.5.8; 5.8，文件頁 108,110-113,165，PDF 頁 108,110-113,165

**關聯 Figure：** Figure 132, Figure 133, Figure 134

### Module 18: FDP：placement、RUH 與可觀測數據

**解釋。** 建立時決定 placement 關係，執行時看 handle status，事後再用 statistics／events 解釋媒體搬移。三種資料不能互相代替。

```text
Create placement
  ↓
PID and RUHID
  ↓
Handle status
  ↓
Statistics
  ↓
Media event
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| NPHNDLS | 最多 128，且不超過 configuration 的 RUH 數 | 0 有 controller 選擇與共享規則 |
| EARUTR / RUAMW | 剩餘秒數估計／可寫 logical blocks | EARUTR=0 未回報；不是保證壽命 |
| LID 22h | HBMW／MBMW 含 NVM 指定寫入類命令 | 含 Copy 寫入端、Zeroes、Uncorrectable |
| LID 23h event 0h | LBAV 控制 LBA 有效性 | NLBAM=FFFFh 表示至少 FFFFh |

**說明性範例。** 兩個 namespaces 共享 RUH 5，第一個使用 FIDX=2，第二個 create 指定 FIDX=3，即使資料大小同為 4 KiB，也不符合共享 RUH 的 Format Index 條件。

**常見誤解／Debug。** Media Reallocated event 的 LBA 是搬移集合中的一個 LBA，並不是完整清單；LBAV=0 時必須忽略。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§3.2.1; 4.1.4.6-4.1.4.7; 4.1.6.3，文件頁 26,79,110-113，PDF 頁 26,79,110-113

**關聯 Figure：** Figure 21, Figure 116

### Module 19: AER、SMART 與錯誤記錄的 NVM 補充

**解釋。** 用事件找調查方向，再用正確 scope 的 log 與 command set 定義解碼。統計數據也要依命令分類，不能只按 opcode 名稱猜。

```text
Notice enable
  ↓
AER
  ↓
Log scope
  ↓
Validity and units
  ↓
Correlate evidence
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| LBASIN / RLCCN | FID0Bh bits 13／22 | 分別啟用 LBA Status／Rate Limiting notices |
| SMART units | 先換算 512-byte units，再套 Base counter 編碼 | 不是每個 4 KiB block 加一個 Data Unit |
| Read categories | Data Units Read 含 Verify；Host Read 含 Copy | Compare、Read 為兩類共同項 |
| Persistent Event 06h | create／single-delete 有 FLBAS、DPS | delete-all 時這兩欄 reserved |

**說明性範例。** 一個 Self-test FLBA=100、valid=1 的紀錄只能定位一個失敗 LBA，不能據此宣告其他 LBAs 全部正常。Error Information LBA=100 的「最低」語意也不能直接套到 FLBA。

**常見誤解／Debug。** Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§1.4.2; 4.1.1; 4.1.3.5; 4.1.4.1-4.1.4.4，文件頁 10-11,62,67,75-77，PDF 頁 10-11,62,67,75-77

**關聯 Figure：** Figure 90, Figure 99, Figure 109, Figure 110, Figure 111, Figure 112

### Module 20: LBA Status：通知、掃描與修復流程

**解釋。** 讀到 potentially unrecoverable 不是每個 block 一定無法讀取。先辨識 ATYPE，再檢查 buffer 是否足夠與 completion condition，最後安排資料修復。

```text
LID 0Eh
  ↓
ATYPE
  ↓
Range and MNDW
  ↓
CMPC and descriptors
  ↓
Recover and recheck
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| MNDW / RL | MNDW 是 0-based dwords；RL=0 到 NSZE−1 | 不是 RL=0 查一個 block |
| NLSD / CMPC | 實際 descriptor 數／完成原因 | CMPC=1 尚有資料或 scan 未完成；2 完成 |
| LSIPI / LSIRI | 100 ms 單位；poll interval 不可由 host 改 | Set 回傳最接近支援值 |
| RAE / LSGC | RAE=1 分段讀，RAE=0 清事件並允許更新 | 重讀 header 檢查 generation |
| TLBAAG | 02h 可用較大 allocation granularity | 混合 allocated／deallocated unit 會整段回 allocated |

**說明性範例。** log 有 NLSLNE=0 但 ESTULB 非零時，不能當作沒有問題，宜檢查 attached namespaces 的完整 LBA 範圍。取得可疑 LBAs 後，可從其他可靠來源恢復並寫回；後續查詢會移除成功重寫且未再偵測的項目。

**常見誤解／Debug。** CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.3.6; 4.1.4.5; 4.2.1; 5.2.1，文件頁 67-68,77-79,114-122，PDF 頁 67-68,77-79,114-122

**關聯 Figure：** Figure 100, Figure 113, Figure 114, Figure 115, Figure 135, Figure 136, Figure 137, Figure 138, Figure 139, Figure 140, Figure 142, Figure 143, Figure 144

### Module 21: Performance Characteristics 的屬性模型

**解釋。** 此 Feature 回報或管理效能屬性，不能把標準 latency 級別當成對任意 workload 的服務保證。

```text
Scope
  ↓
ATTRI
  ↓
Current default saved
  ↓
PAID and length
  ↓
Interpretation
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| R4KARL | 標準化 4 KiB random read 的平均 latency 區間 | 00h 是未回報 |
| MSVSPA / USVSPA | 可 save 總數／剩餘數 | index 可不連續 |
| PAID / ATTRL | 128-bit identifier／有效 vendor bytes | ATTRL 最大 FE0h |
| RVSPA | 刪除 saved value 後取 default | 此操作不使用 data buffer 內容 |

**說明性範例。** R4KARL=0Eh 表示 50 μs ≤ 平均 latency <100 μs，並非 14 μs。讀 C0h list 時應使 ATTRTYP 與 Get 的 SEL 一致，再用 PAID 解釋 vendor payload。

**常見誤解／Debug。** Set ATTRI=00h 或 C0h 會回 Invalid Field in Command。Vendor bytes 的意義需要廠商定義，不能自行推測成標準欄位。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.3.8，文件頁 69-73，PDF 頁 69-73

**關聯 Figure：** Figure 102, Figure 103, Figure 104, Figure 105

### Module 22: Rate Limiting 的設定欄位

**解釋。** 先從 LID 28h 取得支援 target，再檢查 HLS／SLS 與 soft-controller 數量。把 host 請求限制和裝置可達能力分開記錄。

```text
Supported targets
  ↓
HLS and SLS
  ↓
TGT and TID
  ↓
Limits and ratios
  ↓
Set and Get
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| TGT / TID | CDW11[23:16]／[15:0] | TGT=0 才是標準 controller target |
| RLC | RLE bit15；RLM=0 Hard、1 Soft | 支援 Soft 必須也支援 Hard |
| BWSF | 0/1/2 = 1/10/100 MiB/s；3/4/5 = 1/10/100 GiB/s | 值乘 scale 才是 bandwidth |
| WRIOPSR / WRBWR | write 分子除 read 分母 | 兩者的各 ratio bytes 均需非零 |

**說明性範例。** BWSF=1、TBWV=50 表示 500 MiB/s。WBWV 與 WIOPS 控制寫入部分，總量還會按 WRBWR／WRIOPSR 加權；不能把 total 限制只當 read limit。

**常見誤解／Debug。** 未替某 target 設 limits 時，其 limits 是 vendor-specific；不能把缺少設定解讀為無限制。§5.10 開頭的 Hard／Soft 小節引用對調，正確是 5.10.1 Hard、5.10.2 Soft。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.3.9; 4.1.5.4; 5.10，文件頁 73-75,106,165-168，PDF 頁 73-75,106,165-168

**關聯 Figure：** Figure 106, Figure 107, Figure 108

### Module 23: Rate Limiting log 是能力圖

**解釋。** 先做結構邊界檢查，再分析 bandwidth bottleneck。Port 的能力與共同 Endurance Group 的能力不同，不能把所有數字直接相加。

```text
Header and GC
  ↓
Port offsets
  ↓
Controller offsets
  ↓
Shared storage nodes
  ↓
Bounds and bottleneck
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| LPL / offsets | 長度與指標皆有 dword 單位 | byte offset = dword offset ×4 |
| NP / NC / NST | 都是 0-based counts | NNSMAD 是實際數量 |
| SC / SI | subsystem／domain／EG／namespace 及其 ID | 依 scope 解讀，避免共享節點重算 |
| RLMA | 最大 read/write bandwidth／IOPS | workload 需符合相關 size／queue-depth 條件 |

**說明性範例。** 兩個 PCIe ports 都能使用一個 Endurance Group，若 EG 的 bandwidth 已被 controller 0 用滿，controller 1 不會因多一個 port 就多一份媒體頻寬。相同 EG 能力可由兩個 controller 指向同一 descriptor。

**常見誤解／Debug。** Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.4.8; 5.10.3，文件頁 79-83,168-172，PDF 頁 79-83,168-172

**關聯 Figure：** Figure 117, Figure 118, Figure 119, Figure 120, Figure 121, Figure 195, Figure 196, Figure 197, Figure 198

### Module 24: Hard／Soft 與 token-bucket 算例

**解釋。** 用能力、limits、實際 demand 三個值判讀結果。設定比例不等於任何時刻都固定吞吐；內部資源與工作負載仍會改變觀測值。

```text
Capabilities
  ↓
Configured limits
  ↓
Actual demand
  ↓
Token admission
  ↓
Completion
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Hard | 有需求且資源不足時按比例分享 | 設定上限不是最低效能保證 |
| Soft | 可使用閒置額度 | 多個 soft targets 依 limits 比例分享 |
| Write tokens | total bytes × WRBWR；write bytes；total IOPS × WRIOPSR；write IOPS 1 | 四個 buckets 各自檢查 |
| Read tokens | total bytes 及 total IOPS 1 | 不扣 write-only buckets |

**說明性範例。** 教學設定：4 KiB Write，WRBWR=2、WRIOPSR=3，分別消耗 total-bandwidth 8 KiB、write-bandwidth 4 KiB、total-IOPS 3、write-IOPS 1。4 KiB Read 只消耗 total-bandwidth 4 KiB 與 total-IOPS 1。

**常見誤解／Debug。** Token 不足時延後處理而非丟棄命令；可以處理部分，但不得在整筆處理完前先送 completion。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.10.1-5.10.2; Appendix A，文件頁 166-168,176-177，PDF 頁 166-168,176-177

**關聯 Figure：** Figure 202

### Module 25: 對齊、granularity 與效能提示

**解釋。** 先把 raw 欄位轉成 blocks，再評估 start alignment 與 length granularity。只滿足其中一項可能仍引發 read-modify-write。

```text
Support bits
  ↓
Decode units
  ↓
Align start
  ↓
Choose length
  ↓
Measure workload
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| NPWG / NPWA | 長度與起點同時符合 | 先看 NSFEAT.OPTPERF |
| NPRG / NPRA / NORS | 適用讀取最佳化 | 先看 OPTRPERF |
| NPDG / NPDGL | deallocate granularity 的不同欄位 | 用 OPTPERF 決定；Large 不一律加一 |
| NOIOB / NABO | 最佳 I/O boundary 與 atomic offset 不同 | 可分割 I/O 以符合多種條件 |

**說明性範例。** 解碼後 NPWG=8、NPWA=8。寫 LBA 8..15 同時符合；寫 9..16 雖然也是 8 blocks，仍跨兩個 granularity units，可能需要讀取兩端舊資料。

**常見誤解／Debug。** 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.2.2，文件頁 122-129，PDF 頁 122-129

**關聯 Figure：** Figure 145, Figure 146, Figure 147, Figure 148, Figure 149, Figure 150, Figure 151

### Module 26: Metadata 傳輸與 PI 的位置

**解釋。** Metadata 不一定全是 PI。先標示 data、非 PI metadata 與 PI 三個區域，再計算 host buffer 大小與 CRC coverage。

```text
Namespace format
  ↓
Data region
  ↓
Metadata region
  ↓
PI suffix
  ↓
Buffer lengths
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Extended LBA | DPTR 指向 data+metadata 交錯序列 | MSET／MTELBA 反映此選擇 |
| Separate buffer | DPTR 給 data，MPTR 給 metadata | PRP metadata 需 physically contiguous；SGL 可分散 |
| PI location | 本版有效格式的 PI 在 metadata 末端 | CRC 包含之前的非 PI metadata |

**說明性範例。** 8 blocks、data=4096、MS=16、PRACT=0：extended buffer 為 32896 bytes；separate 模式 data buffer=32768、metadata buffer=128 bytes。

**常見誤解／Debug。** PI 在末端的位置規則與「metadata 是否 separate」是獨立維度；不能以 DIX／DIF 名稱省略 namespace format 設定。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§2.1.6; 5.2.3; 5.3，文件頁 22,129-131，PDF 頁 22,129-131

**關聯 Figure：** Figure 153, Figure 154

### Module 27: 16／32／64b Guard 與 Qualified PI

**解釋。** 先由 PIF 決定格式；PIF=11b 才由 QPIF 決定 Guard width，並受 QPIFS 與 STMLA 條件限制。Protection type 仍由 DPS 決定。

```text
DPS type
  ↓
PIF or QPIF
  ↓
Guard size
  ↓
STS split
  ↓
Mask capability
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| 16b Guard | 2-byte Guard + 2-byte App + 4-byte space | STS=0..32 |
| 32b Guard | 4-byte Guard + 2-byte App + 10-byte space | STS=16..64 |
| 64b Guard | 8-byte Guard + 2-byte App + 6-byte space | STS=0..48 |
| STMLA | bit mask／byte mask／no mask | qualified type 與 QPIFS 共同決定適用 |

**說明性範例。** 64b Guard、STS=18：48-bit space 中高 18 bits 是 Storage Tag、低 30 bits 是 Reference Tag。PI 總大小仍為 16 bytes，不會因 STS 增加而變大。

**常見誤解／Debug。** 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.3.1; 4.1.5.3，文件頁 97-102,130-138，PDF 頁 97-102,130-138

**關聯 Figure：** Figure 155, Figure 156, Figure 157, Figure 159, Figure 164, Figure 165

### Module 28: CRC 參數、位元順序與已知向量

**解釋。** CRC 的 polynomial、初值、reflection、final XOR 與儲存順序必須一起核對。用已知向量驗證後才接進 PI parser。

```text
Data and metadata
  ↓
Initialization
  ↓
Polynomial and reflection
  ↓
Final XOR
  ↓
Known vectors
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| CRC-16 | SBC-4 定義的 Guard CRC | NVM 不支援 DIX 的 optional IP checksum |
| CRC-32C | polynomial 1EDC6F41h | 4 KiB zero vector → 98F94189h |
| CRC-64/NVME | 反射式 register 算例 123456789 → AE8B14860A799888h | 4 KiB zero vector → 6482D367EB22B64Eh |
| Coverage | data + PI 前的 metadata | 排除 PI 本身 |

**說明性範例。** CRC-64 的 4 KiB 全 FFh 向量結果為 C0DDBA7302ECA3ACh。若 zero vector 正確而 incrementing-byte vector 不符，要檢查 byte／bit 順序，不能只改 polynomial 硬湊。

**常見誤解／Debug。** Figure 161 列 Check=11199E506128D175h；常見 LSB-first register 對 123456789 算得 AE8B14860A799888h，兩者互為 64-bit 反轉。Figure 163 的四個 4 KiB 向量則直接符合該 register 結果。須明示表示差異，不因單一 Check 差異改 polynomial；CRC 也不是密碼學認證。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.3.1.1-5.3.1.3，文件頁 131-137，PDF 頁 131-137

**關聯 Figure：** Figure 158, Figure 160, Figure 161, Figure 162, Figure 163

### Module 29: Storage／Reference Tag 的 Dword 封裝

**解釋。** 先決定總 space 大小，再切 tag，最後拆到命令 Dwords。不要因 tag 的名稱相似就把 Write 的值與 Read 的 expected 值交換。

```text
PI space width
  ↓
STS
  ↓
Storage and reference
  ↓
CDW2 and CDW3
  ↓
CDW14
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| 16b Guard, STS=0 | CDW14 為 32-bit reference | CDW2／3 對此 tag 忽略 |
| 32b Guard, STS=32 | CDW2 low16 + CDW3 high16 是 Storage | CDW3 low16 + CDW14 為 48-bit Reference |
| 64b Guard, STS=18 | CDW3 low16 + CDW14 high2 是 Storage | CDW14 low30 是 Reference |

**說明性範例。** 64b Guard、STS=18、Storage Tag=0x12345、Reference Tag=0x2A：CDW3 low16=0x48D1，CDW14=(1<<30)|0x2A=0x4000002A。Read 使用相同布局的 expected tags。

**常見誤解／Debug。** Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.3.1.4，文件頁 137-141，PDF 頁 137-141

**關聯 Figure：** Figure 166, Figure 167, Figure 168, Figure 169, Figure 170, Figure 171, Figure 172, Figure 173

### Module 30: PRACT 與 PRCHK／STC 的組合

**解釋。** 先檢查 namespace 是否啟用 PI，再依命令方向及 metadata 大小選處理分支。Checking bits 與可能的特殊停用值放在最後判斷。

```text
PI enabled
  ↓
PRACT
  ↓
Metadata size
  ↓
PRCHK and STC
  ↓
Status
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Write, PRACT=1 | MS=PI 時插入；MS>PI 時取代 PI | 此生成分支忽略 PRCHK／STC |
| Read, PRACT=1 | 先做要求的檢查；MS=PI 才移除 | MS>PI 仍回 metadata 與 PI |
| Type 1 / Type 2 | Reference 每個 block 遞增 | Type1 初值須等於對應 SLBA 低 bits |
| Type 3 | 不宜比對 computed reference | 若因 RTCHK 拒絕，使用 Invalid Protection Information |
| Disable sentinels | Type 1／2：Application Tag=FFFFh 時停用所有 PI checks；Type 3 另要求 Reference Tag（若有）也全一 | 不受 PRCHK／STC 設定影響 |
| Masks | mask bit=0 不比較 | Storage mask 另受 STMLA 約束 |

**說明性範例。** 16b Guard、MS=16、Read PRACT=1：host 仍接收 16 bytes metadata；若 MS=8，則 host 只接收 data。相同 PRACT 在不同 MS 下造成不同 buffer 大小。

**常見誤解／Debug。** STC 在本份指 Storage Tag Check；不要沿用 Self-test Code 的縮寫解釋。Compare 的兩條輸入路徑都可能執行 PI checking，但 PI bytes 不納入一般 metadata 比對。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§2.1.5; 5.3.2-5.3.3，文件頁 21-22,141-152，PDF 頁 21-22,141-152

**關聯 Figure：** Figure 11, Figure 12, Figure 174, Figure 175, Figure 176

### Module 31: ANA 與 Reservations 的 NVM 行為

**解釋。** 同一 namespace 的可達性與存取權限要分開檢查；不能將路徑狀態等同 reservation ownership。

```text
Namespace
  ↓
ANA state
  ↓
Reservation type
  ↓
Holder and registrant
  ↓
Command permission
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| ANA Identify | Inaccessible／Persistent Loss 下 NUSE、NVMCAP 回零 | 不是 media 被清空 |
| ANA FID05h | Get 的 Inaccessible／Persistent Loss／Change 受限 | 使用對應 ANA status |
| Write Exclusive / Exclusive Access | 非 holder：前者允許 read-like；後者 read／write-like 都衝突 | 兩者的非 holder write-like 都衝突 |
| Registrants Only / All Registrants | Write Exclusive 類允許所有人 read、registrants write；Exclusive Access 類僅 registrants read／write | Copy 每個 source 用 read 權限，destination 用 write 權限 |
| Reservations | 分 read-like、write-like 命令查矩陣 | holder、registrant 與 type 必須一起看 |

**說明性範例。** 同一 SSD 的兩個 PCIe controllers 可共享 namespace。Controller 1 的路徑可用，仍可能因 reservation 類型與自身 registration 狀態而無法 Write；Read 是否允許需另外查表。

**常見誤解／Debug。** 不能僅憑存在 Reservation 就一律封鎖所有非 holder 的 I/O；Write Exclusive 與 Exclusive Access 等類型的讀取規則不同。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.1; 5.11，文件頁 119,172-173，PDF 頁 119,172-173

**關聯 Figure：** Figure 141, Figure 199

### Module 32: LBA Migration Queue 與變更追蹤

**解釋。** 這個 queue 保存變更範圍與序列標記，不保存完整新資料。Host 讀 entry 後仍需以適當 I/O 取得資料，並處理滿 queue 的停止邊界。

```text
Track Send
  ↓
Changes take effect
  ↓
Range entries
  ↓
Phase and sequence
  ↓
Full or stop
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| LBACIR | 00：range；01：整個 namespace；10：無 range | 先判斷欄位是否有效 |
| ESA | 001 start／resume；010 stop；011 suspend；111 full | full 表示 logging 已停止 |
| DLBA / CDQP | deallocated 標記／entry phase | DLBA=0 仍可能描述 deallocate 類修改 |
| RALBAS | 開始命令處理期間的變更可由 ATYPE02h 補齊 | start／stop marker 不要求先於 Track Send CQE |

**說明性範例。** 三筆連續 Write 可合併成一個 range entry；所以 queue entry 數不等於寫入命令數。ESA=111b 後，host 不能假設後續每次修改仍持續記錄。

**常見誤解／Debug。** 此處教學為 NVM 的 LBA 變更追蹤；不藉此展開其他傳輸協定或資源匯出格式。重新開始追蹤前要處理 queue 容量與資料一致性。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.8; 5.7，文件頁 113-114,162-164，PDF 頁 113-114,162-164

**關聯 Figure：** Figure 194

### Module 33: Sanitize 與 Media Verification 的 NVM 規則

**解釋。** 先辨識 target、operation state 與 allocation，再決定可以驗證什麼。命令 CQE 與 sanitize operation 完成分別由不同證據表示。

```text
Target and state
  ↓
LID81h
  ↓
Allocation
  ↓
Verification Read
  ↓
Result interpretation
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| LID81h | 追蹤 operation status／progress | 啟動命令成功不是 operation 完成 |
| Error Information | sanitize 期間 NVM LBA 欄位回 0 | 僅此 NVM 補充，仍須遵守 Base command allowlist |
| Media Verification Read | PRCHK=000b、STC=0 | 要求 checking 則 Invalid Field in Command |
| Allocated media | 可讀則回實際資料；不可讀則錯誤 | 符合條件回 Successful Media Verification Read |

**說明性範例。** Media Verification state 中，Read 不要求 PI checking 且 allocated media 可讀時，可以忽略讀得出資料的 integrity error 並回特定成功狀態；同一 LBA 連續讀值仍 may 不同。不能用平常 Read 的固定值假設評估它。

**常見誤解／Debug。** Sanitize 之後讀零不是充分的成功證據，也不是所有方法都應回零。Namespace sanitize 與 subsystem sanitize 的 scope 不可互換。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§4.1.7; 5.12，文件頁 113,173-175，PDF 頁 113,173-175

**關聯 Figure：** Figure 200, Figure 201

### Module 34: Key Per I/O 的 NVM 對齊約束

**解釋。** 先從 KPIOCAP 與 namespace status 判斷適用，再解讀 CETYPE／CEV 的 command extension。金鑰建立及管理不由這份 NVM 補充完整定義。

```text
Capability
  ↓
Namespace enablement
  ↓
CETYPE and CEV
  ↓
KPIODAAG
  ↓
Status
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| KPIOCAP | 支援與 subsystem／namespace scope | 不能只看單一 enable bit |
| KPIOSNS / KPIOENS | namespace 支援／啟用 | 未支援時 enable 必須為 0 |
| KPIODAAG | 0-based logical-block granularity | 起點及長度都必須符合 |

**說明性範例。** raw KPIODAAG=7 代表 8-block granularity。SLBA=16、length=8 符合；SLBA=17 或 length=7 都不符合，即使其他 PI 欄位完全正確也不能使用。

**常見誤解／Debug。** Invalid Key Tag 與 alignment 的 Invalid Field in Command 需要不同調查方向；不能將 key-tag 拒絕都歸類為 PI checksum 錯誤。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.5; 4.1.5，文件頁 91-92,105,160，PDF 頁 91-92,105,160

**關聯 Figure：** 

### Module 35: Streams 的 NVM 單位與優先順序

**解釋。** 用兩層大小模型解釋 Stream Write Size 與較大的 stream granularity。它們可能和 namespace hints 成整數倍，但規格不保證每個 namespace 都如此。

```text
SWS blocks
  ↓
SGS multiplier
  ↓
Stream granularity
  ↓
Namespace hints
  ↓
Workload
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| SWS | 建議寫入大小，以 blocks 計 | 宜為 NPWG 的倍數 |
| SGS × SWS | stream granularity 的長度 | 適用 stream deallocate 對齊／長度 |
| Priority | 用 Streams 時優先 Streams attributes | 未使用則用 namespace hints |

**說明性範例。** 解碼後 SWS=8 blocks、SGS=4，stream granularity 是 32 blocks。8-block Write 可符合 SWS，但一個完整 granularity-unit 的 deallocate 長度是 32 blocks。

**常見誤解／Debug。** Streams hints、FDP placement 與 namespace atomicity 是不同概念；不能只因尺寸相等就推論是同一個內部媒體單位。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.2.2.3; 5.13，文件頁 128-129,175，PDF 頁 128-129,175

**關聯 Figure：** Figure 152

### Module 36: Memory-based 資源匯出範本

**解釋。** 範本固定的相容性介面與 underlying 裝置能力是兩層。先確認 namespace 格式相容，再設定不超過 underlying 能力的限制；沒有被範本開放的能力不能自行宣告。

```text
Underlying capability
  ↓
Template and TR
  ↓
IDs 0 and 1
  ↓
Set once
  ↓
Reported interface
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Identity and version | CAP.CSS=1、VS=020300h；NVM VER=010200h | 範本固定 Base 2.3／NVM 1.2，不隨本 PDF 版本自動升級 |
| Controller limits | MDTS、RAB、NCQS、NSQS、MQES、AWUN／AWUPF 受 underlying 限制 | NCQS／NSQS 是 0-based |
| Namespace compatibility | LBAF0 的 LBADS／MS 必須相同，MS=0；DPS／KPIOENS／CWP 必須為零 | controller 負責 Format Index remapping |
| Observable defaults | Error entries 與 SMART 為零；firmware active slot=1 | 支援清單、Feature defaults 與 Identify exceptions 另有固定規則 |

**說明性範例。** Underlying NCQS=7 可支援 8 queues，範本設定 NCQS=3 表示最多 4 queues；不能把 raw 3 誤解成 3 queues。Namespace 的 NGUID 為零時，NUUID 必須提供有效 UUID。

**常見誤解／Debug。** Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.4.1-5.4.1.1，文件頁 152-159，PDF 頁 152-159

**關聯 Figure：** Figure 183, Figure 184, Figure 185, Figure 186, Figure 187, Figure 188, Figure 189, Figure 190

### Module 37: 匯出狀態的長度與一致性

**解釋。** 先讀固定 64-byte header，再檢查可變長度與 suspension 證據。Configuration state 與執行中 state 的用途和設定限制不同，不能共用 payload parser。

```text
Current features
  ↓
CP evidence
  ↓
NVMECSS dwords
  ↓
Bounds
  ↓
Nested VER
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Feature values | 保存 arbitration、power、temperature、error recovery、queues、interrupt、atomicity 與 AEC | 是 current values，不是 Figure 187 defaults |
| CSATTR.CP | 1 表示整段處理期間 suspended | 0 不保證完全沒有 suspension |
| NVMECSS | 總長度 = 64 + 4 × NVMECSS bytes | 0 時 NVMECS 欄位不存在 |

**說明性範例。** NVMECSS=16 時，NVMECS 有 64 bytes，整個結構有 128 bytes；先檢查乘法、加法與接收 buffer bounds，再解碼內層 VER。

**常見誤解／Debug。** 這是 memory-based controller state 的教學；沒有完整 state 與 suspension 證據時，不從單一 Feature value 推論整個 subsystem 已安全移轉。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§5.4.1.2，文件頁 159-160，PDF 頁 159-160

**關聯 Figure：** Figure 191

## 可追溯的規格重點

前面的 Mental Model 解釋因果；本節保留每個可追溯結論與 normative 強度，供講者備註與審查。

### 1. 閱讀地圖與單位

<!-- claim:NVMCS13-FOUNDATION -->

NVM Command Set 補充 Base 的 logical-block 語意；logical block data size 不含 metadata，logical block size 則包含。NVM 的 CSI 是 00h，命令、Feature、log 與 Identify 的相同數字分屬不同識別空間。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §1.1-1.6; 4.1.3.9; 4.1.4.8; 4.1.5, 文件頁 9-12,73-75,79-83, PDF 頁 9-12,73-75,79-83

### 2. Namespace 容量與配置狀態

<!-- claim:NVMCS13-CAPACITY -->

NSZE ≥ NCAP ≥ NUSE；NSZE 定義可定址範圍，NCAP 限制同時配置的 blocks，NUSE 計算目前已配置 blocks。THINP=0 時 NCAP=NSZE；NVMCAP 以 bytes 計，不能直接當成 NSZE 乘資料大小。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1; 4.1.5.1, 文件頁 13-14,85-93, PDF 頁 13-14,85-93

### 3. 命令順序與 Compare-and-Write

<!-- claim:NVMCS13-ORDER-FUSED -->

一般命令不因同在一個 SQ 就取得 LBA 相依順序；host 必須建立必要順序。Fused Compare-and-Write 先比對，成功才寫入；Compare 失敗則 Write 以 Failed Fused Command 類別中止。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.2-2.1.3, 文件頁 14-15, PDF 頁 14-15

### 4. 正常、斷電與多段原子性

<!-- claim:NVMCS13-ATOMIC -->

AWUN／NAWUN 與 AWUPF／NAWUPF 分別描述正常及失敗條件原子性。Single Atomicity Mode 跨 boundary 不保證整筆原子；Multiple Atomicity Mode 在每個 boundary 切成各自原子的 subranges，並不承諾整筆一起成功。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4; 4.1.3.4; 5.9, 文件頁 15-21,66-67,165, PDF 頁 15-21,66-67,165

### 5. 能力探索、Opcode 與狀態

<!-- claim:NVMCS13-SUPPORT-STATUS -->

NVM I/O controller 必須支援 Read 與 Write；其他列出的 NVM 命令依各能力條件判斷。Opcode 低兩 bits 表示資料傳輸方向，狀態值必須連同 SCT 解讀，不能只用 SC 數值查錯誤。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.2; 3.1; 3.3, 文件頁 22-27, PDF 頁 22-27

### 6. Read／Write 的資料與完成條件

<!-- claim:NVMCS13-READ-WRITE -->

Read／Write 以 SLBA 與 0-based NLB 指定連續範圍。Read 的 DPTR 是目的 buffer，Write 的 DPTR 是來源 buffer；FUA=1 要求使用 nonvolatile media，並沒有隱含其他命令的順序。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4; 3.3.6, 文件頁 48-51,53-56, PDF 頁 48-51,53-56

### 7. Compare 與 Verify 解決不同問題

<!-- claim:NVMCS13-COMPARE-VERIFY -->

Compare 比較媒體資料與 host 提供的 buffer；Verify 檢查已儲存資料完整性而不把資料或 metadata 回傳 host。兩者要求 PRACT=0；Verify 與 Read 偵測到的失敗不必使用相同錯誤碼。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1; 3.3.5, 文件頁 27-30,51-53, PDF 頁 27-30,51-53

### 8. Copy：描述來源、連續目的與部分失敗

<!-- claim:NVMCS13-COPY -->

Copy 把一個或多個 source ranges 依 descriptor 順序接成單一連續目的範圍。Format 0h/1h 來源與目的在同一 namespace；2h/3h 帶 SNSID，需 controller 支援與 host 啟用。失敗 CQE DW0 是最低未成功 source index，後面的 ranges 仍可能已複製。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, 文件頁 30-44, PDF 頁 30-44

### 9. Copy 的 PI 格式相容與轉換

<!-- claim:NVMCS13-COPY-PI -->

Copy 的 matching formats 要比對資料大小、metadata 大小、DPS、PIFA、有效 LBSTM、PIF／QPIF 與 STS。Corresponding PI formats 只容許有 PI 的一方 metadata 全為 PI，另一方完全沒有 metadata；不能拿 Copy 任意轉換資料格式。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2.3-3.3.2.4; 5.3.2.5, 文件頁 40-43,146-150, PDF 頁 40-43,146-150

### 10. Dataset Management 與三種 processing limits

<!-- claim:NVMCS13-DSM -->

Dataset Management 是 advisory：處理 attributes 不等於一定執行 deallocate。NR 是 0-based，16-byte descriptor 的 LLB 是 1-based；DMRL、DMRSL、DMSL 分別約束 range 數、單一 range 長度與總長度。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, 文件頁 44-48, PDF 頁 44-48

### 11. Deallocated／unwritten 讀取規則

<!-- claim:NVMCS13-DEALLOC -->

支援且啟用 DULBE 時，Copy、Read、Verify、Compare 存取 deallocated／unwritten blocks 會失敗。未啟用時，DRB=001b 回零、010b 回 FFh、000b 可選其一；同 block 在下一次寫入前的回值須保持 deterministic。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3.2.1; 4.1.3.3, 文件頁 47-48,66, PDF 頁 47-48,66

### 12. Write Uncorrectable、Write Zeroes 與整體清零

<!-- claim:NVMCS13-ZERO-UNCORRECTABLE -->

Write Uncorrectable 將範圍標為無法修復的讀取錯誤；Write Zeroes 使成功的後續讀取資料及非 PI metadata 回零。NSZ=1 的整個 namespace 清零需 NSZS、DEAC=1 與零值 deallocation read behavior，且 host 應檢查 CQE.LBACZ。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7-3.3.8, 文件頁 56-61, PDF 頁 56-61

### 13. Format、Host Behavior 與延伸 LBA

<!-- claim:NVMCS13-FORMAT -->

Format NVM 選取已支援的 Format Index、PI type 與 metadata 傳輸方式。延伸 PI 及超過 legacy 16 個 entries 的 LBA formats 需檢查 controller ELBAS 與 host LBAFEE；沒有 host 啟用不可直接使用。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.2; 4.1.3.7, 文件頁 62-63,68-69, PDF 頁 62-63,68-69

### 14. 基本 Features 的作用域與例外

<!-- claim:NVMCS13-BASIC-FEATURES -->

FID 03h 描述 namespace LBA ranges，05h 控制 namespace error recovery，0Ah 控制 controller normal atomicity。Power Management 的 NVM 補充以 NPWG 大小的 Read 作為 Idle I/O Exit Latency Limit 的參考命令。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.1-4.1.3.4, 文件頁 64-67, PDF 頁 64-67

### 15. Identify：同一 namespace 的多份資料結構

<!-- claim:NVMCS13-IDENTIFY -->

NVM CSI=00h。完整 namespace 資訊需結合 CNS 08h 的 command-set-independent 結構、CNS 00h 的 NVM 結構與 CNS 05h／CSI 00h 的 NVM 延伸結構；CNS 01h 與 06h 則提供 controller 資訊。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5, 文件頁 83-110, PDF 頁 83-110

### 16. LBAF、ELBAF 與唯一屬性格式

<!-- claim:NVMCS13-FORMAT-LIST -->

LBAF 與 ELBAF 以同一 Format Index 配對；總 format 數為 raw NLBAF+1+NULBAF。NLBAF 是 0-based、NULBAF 是實際數量。有效 index 還要檢查 LBADS：值 0 表示該支援格式目前不可用。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1; 4.1.5.3; 5.6, 文件頁 85-94,96-102,160-162, PDF 頁 85-94,96-102,160-162

### 17. 建立 namespace：格式、mask 與 granularity

<!-- claim:NVMCS13-NAMESPACE-CREATE -->

Namespace create 的 NVM payload 指定 NSZE、NCAP、FLBAS、DPS、LBSTM 與 placement handles。Namespace Size／Capacity Granularity 以 bytes 回報且是 hints；不符合 granularity 但其他條件合法時，不得僅因此拒絕 create。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6; 4.1.5.8; 5.8, 文件頁 108,110-113,165, PDF 頁 108,110-113,165

### 18. FDP：placement、RUH 與可觀測數據

<!-- claim:NVMCS13-FDP -->

FDP namespace 的 placement handles 對應 Reclaim Unit Handles。共享 RUH 的 namespaces 必須使用相同 Format Index；host 指定的 handle list 不得重複 RUHID。RUH Status descriptors 先依 Placement Handle、再依 Reclaim Group Identifier 排序。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.2.1; 4.1.4.6-4.1.4.7; 4.1.6.3, 文件頁 26,79,110-113, PDF 頁 26,79,110-113

### 19. AER、SMART 與錯誤記錄的 NVM 補充

<!-- claim:NVMCS13-LOG-EVENTS -->

NUSE 的頻繁改變及 ANA 造成的 capacity 回報變動不產生 Namespace Attribute Changed 事件。Error Information 的 LBA 指最低發生錯誤的 LBA；Self-test FLBA 只在 valid bit 設定時有效，且可只代表多個失敗 blocks 中的一個。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §1.4.2; 4.1.1; 4.1.3.5; 4.1.4.1-4.1.4.4, 文件頁 10-11,62,67,75-77, PDF 頁 10-11,62,67,75-77

### 20. LBA Status：通知、掃描與修復流程

<!-- claim:NVMCS13-LBA-STATUS -->

LID 0Eh 先指出值得調查的 namespace ranges；Get LBA Status 再回詳細 descriptors。ATYPE=02h 回 tracked allocated LBAs，10h 掃描並回 tracked／untracked 候選，11h 只回 tracked 候選且不做 foreground scan。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.6; 4.1.4.5; 4.2.1; 5.2.1, 文件頁 67-68,77-79,114-122, PDF 頁 67-68,77-79,114-122

### 21. Performance Characteristics 的屬性模型

<!-- claim:NVMCS13-PERFORMANCE-FEATURE -->

FID 1Ch 用 ATTRI 選屬性：00h 為只讀標準效能，C0h 為只讀 identifier list，C1h..FFh 為 vendor attributes。Current、Default、Saved 是不同視圖，RVSPA 用來移除指定 vendor attribute 的 saved value。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, 文件頁 69-73, PDF 頁 69-73

### 22. Rate Limiting 的設定欄位

<!-- claim:NVMCS13-RATE-CONFIG -->

FID 28h 以 TGT／TID 選 target，1024-byte buffer 指定 enable、mode、bandwidth、IOPS 與 write/read ratios。TGT=0 指 controller，不能指定 Admin controller 或保留 ID。此 Feature 必須可 save。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.9; 4.1.5.4; 5.10, 文件頁 73-75,106,165-168, PDF 頁 73-75,106,165-168

### 23. Rate Limiting log 是能力圖

<!-- claim:NVMCS13-RATE-GRAPH -->

LID 28h 以 log 起點為基準的 dword offsets 連接 port、controller 與 storage-medium access descriptors；descriptor 可共享，不能假設為固定順序陣列。分段讀取後應重讀 GC，改變時重收整份資料。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8; 5.10.3, 文件頁 79-83,168-172, PDF 頁 79-83,168-172

### 24. Hard／Soft 與 token-bucket 算例

<!-- claim:NVMCS13-RATE-MODES -->

Hard Limit 設 ceiling，Soft Limit 可利用未用 bandwidth／IOPS；資源不足時依設定比例分配。Appendix A 是多個 token buckets 的實作範例，不要求所有 controllers 採用相同內部實作。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.10.1-5.10.2; Appendix A, 文件頁 166-168,176-177, PDF 頁 166-168,176-177

### 25. 對齊、granularity 與效能提示

<!-- claim:NVMCS13-ALIGNMENT -->

NPWG／NPWA、NPRG／NPRA 分別描述寫入與讀取的建議大小及對齊，NOWS／NORS 描述最佳大小。這些 performance hints 不取代 atomic boundaries、命令硬限制或格式規則。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, 文件頁 122-129, PDF 頁 122-129

### 26. Metadata 傳輸與 PI 的位置

<!-- claim:NVMCS13-METADATA -->

每個 namespace 在 format 時選一種 metadata 傳輸機制：與 data 相連形成 extended LBA，或由 MPTR 指向 separate buffer。不能把 metadata 分拆到兩種機制；寫入時 metadata 必須與其 logical block 原子寫入。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.6; 5.2.3; 5.3, 文件頁 22,129-131, PDF 頁 22,129-131

### 27. 16／32／64b Guard 與 Qualified PI

<!-- claim:NVMCS13-PI-FORMATS -->

16b Guard PI 共 8 bytes；32b 與 64b Guard PI 各 16 bytes。Application Tag 固定 16 bits，Storage/Reference Space 分別為 32、80、48 bits。32b／64b 格式限 logical block data size 至少 4 KiB。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1; 4.1.5.3, 文件頁 97-102,130-138, PDF 頁 97-102,130-138

### 28. CRC 參數、位元順序與已知向量

<!-- claim:NVMCS13-CRC -->

32b Guard 使用 CRC-32C；64b Guard 使用 NVM Express 64b CRC，polynomial AD93D23594C93659h、全一 Init／XorOut、RefIn／RefOut=true。不能只用「CRC64」名稱選任意 polynomial。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.1-5.3.1.3, 文件頁 131-137, PDF 頁 131-137

### 29. Storage／Reference Tag 的 Dword 封裝

<!-- claim:NVMCS13-TAG-LAYOUT -->

Storage Tag 使用 Storage/Reference Space 的高 STS bits，其餘低 bits 是 Reference Tag。命令以 CDW2、CDW3、CDW14 的最多 80 bits 傳入實際或 expected tags；不同 Guard 格式使用不同子集合。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, 文件頁 137-141, PDF 頁 137-141

### 30. PRACT 與 PRCHK／STC 的組合

<!-- claim:NVMCS13-PI-CHECKING -->

PRACT 決定 PI 的傳遞、插入、移除或取代；PRCHK 的 Guard／Application／Reference bits 與獨立 STC 決定檢查要求。PRACT=1 且 MS>PI size 時，Read 仍傳回全部 metadata，不能一律解讀為刪除 PI。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5; 5.3.2-5.3.3, 文件頁 21-22,141-152, PDF 頁 21-22,141-152

### 31. ANA 與 Reservations 的 NVM 行為

<!-- claim:NVMCS13-ANA-RESERVATIONS -->

ANA 狀態會限制指定 Features 並改變 capacity 回報；Reservations 則依 reservation type、holder 與 registration 狀態決定各命令是否允許。這些共用 namespace 能力可適用於 PCIe 多 controller 情境。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.1; 5.11, 文件頁 119,172-173, PDF 頁 119,172-173

### 32. LBA Migration Queue 與變更追蹤

<!-- claim:NVMCS13-MIGRATION-QUEUE -->

Track Send 啟用 LBA Migration Queue 後，controller 可聚合邏輯 block 修改或 deallocation 記錄。Entry 只在所報命令效果生效後發布，可早於該命令 CQE；queue entry 與 I/O completion 是不同時間點。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.8; 5.7, 文件頁 113-114,162-164, PDF 頁 113-114,162-164

### 33. Sanitize 與 Media Verification 的 NVM 規則

<!-- claim:NVMCS13-SANITIZE -->

NVM Sanitize 命令採 Base 定義，背景 operation 的資料語意由 §5.12 補充。成功後 Block Erase 回值由廠商定義、Crypto Erase 回值不確定、Overwrite 依 pattern 規則；若 block 已 deallocate，則改用 deallocated-read 規則。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.7; 5.12, 文件頁 113,173-175, PDF 頁 113,173-175

### 34. Key Per I/O 的 NVM 對齊約束

<!-- claim:NVMCS13-KEY-PER-IO -->

Key Per I/O 的 NVM 補充要求使用 key tag 的命令符合 KPIODAAG 的 LBA 起點對齊與長度 granularity；不符合時回 Invalid Field in Command。Capability、namespace enablement 與 key 管理是不同層次。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.5; 4.1.5, 文件頁 91-92,105,160, PDF 頁 91-92,105,160

### 35. Streams 的 NVM 單位與優先順序

<!-- claim:NVMCS13-STREAMS -->

NVM 的 Stream Write Size 以 logical blocks 表示；stream granularity length 是 SGS 乘解碼後 SWS blocks。使用 Streams 時，host 宜依 SGS／SWS 的建議處理 write／deallocate，再協調 namespace hints。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2.3; 5.13, 文件頁 128-129,175, PDF 頁 128-129,175

### 36. Memory-based 資源匯出範本

<!-- claim:NVMCS13-EXPORT-TEMPLATE -->

Reference Exported NVM Subsystem Template 是選用的 memory-based 範本，限定一個 controller（ID 0h）及一個 namespace（ID 1h）。建立時必須設 TR=1；configuration state 只能以一筆命令設定一次，重複設定回 Command Sequence Error。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4.1-5.4.1.1, 文件頁 152-159, PDF 頁 152-159

### 37. 匯出狀態的長度與一致性

<!-- claim:NVMCS13-EXPORT-STATE -->

Reference Exported NVM Subsystem State 保存目前 Feature values 與 controller state。CSATTR.CP=1 表示整段 Migration Receive 處理期間 controller 都處於 suspended；NVMECSS 以 dwords 指出可變 NVMECS 長度，內層 VER 固定為 1h。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4.1.2, 文件頁 159-160, PDF 頁 159-160

## Figure 索引

本報告介紹全部 220 張納入範圍的 Figure。100 分鐘簡報以 section 主線與必講 Figure 為主，其餘 Figure 仍完整保留作為附錄。其中 18 張位於主章節範圍外，但因指定正文直接引用而納入相依教學。

- [§1.1](#section-1-1)

- [§1.5](#section-1-5)

- [§2.1](#section-2-1)

- [§2.2](#section-2-2)

- [§3.1](#section-3-1)

- [§3.2](#section-3-2)

- [§3.3](#section-3-3)

- [§4.1](#section-4-1)

- [§4.2](#section-4-2)

- [§5.1](#section-5-1)

- [§5.2](#section-5-2)

- [§5.3](#section-5-3)

- [§5.4](#section-5-4)

- [§5.6](#section-5-6)

- [§5.7](#section-5-7)

- [§5.10](#section-5-10)

- [§5.11](#section-5-11)

- [§5.12](#section-5-12)

- [§Appendix A](#section-appendix-a)

- [引用相依 Figure（位於主章節範圍外）](#section-dependency)

## Figure／欄位表教學參考

本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。欄位與 keyword 索引來自本機核對過的 PDF。

<a id="section-1-1"></a>

### §1.1

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 1: NVMe Family of Specifications</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-001-CLAIM figure-table:NVMCS13-NVM-FIG-001 -->

**SPEC。** Figure 1〈NVMe Family of Specifications〉：依功能層分開閱讀：Base 給共同機制，PCIe 給本機 transport，NVM 給 logical-block 命令語意；這是保留範圍的家族關係重畫。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

依功能層分開閱讀：Base 給共同機制，PCIe 給本機 transport，NVM 給 logical-block 命令語意；這是保留範圍的家族關係重畫。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Base, PCIe Transport, NVM Command Set — 依功能層分開閱讀：Base 給共同機制，PCIe 給本機 transport，NVM 給 logical-block 命令語意；這是保留範圍的家族關係重畫。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 依功能層分開閱讀：Base 給共同機制，PCIe 給本機 transport，NVM 給 logical-block 命令語意；這是保留範圍的家族關係重畫。
3. 本份從 namespace 與資料格式一路走到命令完成、資料完整性及管理證據。主線可分四堂各約 25 分鐘；逐圖附錄與問答供課後查詢。章節 1 的名詞與引用慣例也是範圍的一部分。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 1 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 依功能層分開閱讀：Base 給共同機制，PCIe 給本機 transport，NVM 給 logical-block 命令語意；這是保留範圍的家族關係重畫。 |
| 邊界 | 本報告的算例是教學推導；不把示意數值寫成裝置必須具備的能力。對規格的 should、may 與 shall 保留不同強度。 |

**說明性範例。** LBADS=0Ch、MS=16 時，資料為 4096 bytes，含 metadata 的 logical block 是 4112 bytes。FID 28h 與 LID 28h 雖相同，前者設定限制，後者回報能力圖。

**常見誤解。** 本報告的算例是教學推導；不把示意數值寫成裝置必須具備的能力。對規格的 should、may 與 shall 保留不同強度。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 本報告的算例是教學推導；不把示意數值寫成裝置必須具備的能力。對規格的 should、may 與 shall 保留不同強度。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Base, PCIe Transport, NVM Command Set

**來源 keyword 索引：** shall

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §1.1, Figure 1, 文件頁 9, PDF 頁 9

</details>

<a id="section-1-5"></a>

### §1.5

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 2: Acronym definitions</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-002-CLAIM figure-table:NVMCS13-NVM-FIG-002 -->

**SPEC。** Figure 2〈Acronym definitions〉：LBA 是 logical block 的位址，不是 byte offset；要換成資料 bytes，還需所選格式的 LBADS。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

LBA 是 logical block 的位址，不是 byte offset；要換成資料 bytes，還需所選格式的 LBADS。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBA]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBA` | Logical Block Address；以所選格式的 block 為單位。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. LBA 是 logical block 的位址，不是 byte offset；要換成資料 bytes，還需所選格式的 LBADS。
3. 本份從 namespace 與資料格式一路走到命令完成、資料完整性及管理證據。主線可分四堂各約 25 分鐘；逐圖附錄與問答供課後查詢。章節 1 的名詞與引用慣例也是範圍的一部分。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 2 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §1.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | LBA 是 logical block 的位址，不是 byte offset；要換成資料 bytes，還需所選格式的 LBADS。 |
| 邊界 | 本報告的算例是教學推導；不把示意數值寫成裝置必須具備的能力。對規格的 should、may 與 shall 保留不同強度。 |

**說明性範例。** LBADS=0Ch、MS=16 時，資料為 4096 bytes，含 metadata 的 logical block 是 4112 bytes。FID 28h 與 LID 28h 雖相同，前者設定限制，後者回報能力圖。

**常見誤解。** 本報告的算例是教學推導；不把示意數值寫成裝置必須具備的能力。對規格的 should、may 與 shall 保留不同強度。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 本報告的算例是教學推導；不把示意數值寫成裝置必須具備的能力。對規格的 should、may 與 shall 保留不同強度。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LBA

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §1.5, Figure 2, 文件頁 11, PDF 頁 11

</details>

<a id="section-2-1"></a>

### §2.1

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 3: Supported Fused Operations</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-003-CLAIM figure-table:NVMCS13-NVM-FIG-003 -->

**SPEC。** Figure 3〈Supported Fused Operations〉：先 Compare 成功才執行同 range 的 Write；兩個 CQE 分別表示比對與寫入結果，並須檢查 fused atomicity limits。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

先 Compare 成功才執行同 range 的 Write；兩個 CQE 分別表示比對與寫入結果，並須檢查 fused atomicity limits。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Compare, Write, Match — 先 Compare 成功才執行同 range 的 Write；兩個 CQE 分別表示比對與寫入結果，並須檢查 fused atomicity limits。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 先 Compare 成功才執行同 range 的 Write；兩個 CQE 分別表示比對與寫入結果，並須檢查 fused atomicity limits。
3. 先說明何時要排序，再判斷是否需要條件式更新。Fused 保護同一 LBA range 的比對與更新，原子大小仍須另外檢查。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 3 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.1.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 先 Compare 成功才執行同 range 的 Write；兩個 CQE 分別表示比對與寫入結果，並須檢查 fused atomicity limits。 |
| 邊界 | Write 失敗不會回頭改寫 Compare 已得到的 completion status；必須檢查兩個 CQE。 |

**說明性範例。** Host 想「目前值等於 A 才更新 B」時，獨立 Compare 成功後再送 Write 中間仍可能插入別人的寫入；符合大小與邊界的 fused pair 才提供此操作所需的條件式原子更新。

**常見誤解。** Write 失敗不會回頭改寫 Compare 已得到的 completion status；必須檢查兩個 CQE。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Write 失敗不會回頭改寫 Compare 已得到的 completion status；必須檢查兩個 CQE。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Compare, Write, Match

**來源 keyword 索引：** shall, should, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.3, Figure 3, 文件頁 14, PDF 頁 14

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 4: Atomicity Parameters for Single Atomicity Mode</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-004-CLAIM figure-table:NVMCS13-NVM-FIG-004 -->

**SPEC。** Figure 4〈Atomicity Parameters for Single Atomicity Mode〉：先用 NSABP 選 controller 或 namespace 值，再解碼 0-based 大小及 namespace 的零值繼承規則；不可把每個 raw 0 都解釋成一個 block。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

先用 NSABP 選 controller 或 namespace 值，再解碼 0-based 大小及 namespace 的零值繼承規則；不可把每個 raw 0 都解釋成一個 block。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: AWUN]
          ↓
[擷取欄位: AWUPF] → [套用編碼: ACWU]
                                      ↓
[驗證證據: NAWUN]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `AWUN` | Atomic Write Unit Normal；controller 正常原子寫入大小的 0-based 欄位。 |
| `AWUPF` | Atomic Write Unit Power Fail；失敗條件原子大小的0-based欄位。 |
| `ACWU` | Namespace normal／power-fail／compare-and-write 或 controller compare-and-write 原子大小；0-based。 |
| `NAWUN` | Namespace normal／power-fail／compare-and-write 或 controller compare-and-write 原子大小；0-based。 |
| `NAWUPF` | Namespace normal／power-fail／compare-and-write 或 controller compare-and-write 原子大小；0-based。 |
| `NACWU` | Namespace normal／power-fail／compare-and-write 或 controller compare-and-write 原子大小；0-based。 |
| `NABSN` | Normal／power-fail atomic boundary size；0 值與 NSABP 支援要依欄位定義判讀。 |
| `NABSPF` | Normal／power-fail atomic boundary size；0 值與 NSABP 支援要依欄位定義判讀。 |
| `NABO` | Namespace Atomic Boundary Offset；決定第一個 boundary 的位置。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 先用 NSABP 選 controller 或 namespace 值，再解碼 0-based 大小及 namespace 的零值繼承規則；不可把每個 raw 0 都解釋成一個 block。
3. 把大小、起始對齊、NSABP 與 MAM 一起讀。Atomicity 與資料已進入 nonvolatile media 是不同檢查項目，FUA／Flush 也不建立其他命令的排序。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 4 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 先用 NSABP 選 controller 或 namespace 值，再解碼 0-based 大小及 namespace 的零值繼承規則；不可把每個 raw 0 都解釋成一個 block。 |
| 邊界 | 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。 |

**說明性範例。** 假設解碼後 boundary size=8 blocks、offset=0，從 LBA 4 寫 12 blocks 跨成 [4..7] 與 [8..15]。MAM 下各段原子，不能將兩段當作一個 transaction。原始 AWUN=7h 才代表 8 blocks。

**常見誤解。** 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** AWUN, AWUPF, ACWU, NAWUN, NAWUPF, NACWU, NABSN, NABSPF, NABO

**來源 keyword 索引：** shall not, shall, should, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 4, 文件頁 15-16, PDF 頁 15-16

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 5: AWUN/NAWUN Example Results</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-005-CLAIM figure-table:NVMCS13-NVM-FIG-005 -->

**SPEC。** Figure 5〈AWUN/NAWUN Example Results〉：本圖討論正常運作下重疊寫入的可觀測結果；將 write size 與解碼後 AWUN 比較，再看讀取是否落在相同 atomic unit。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

本圖討論正常運作下重疊寫入的可觀測結果；將 write size 與解碼後 AWUN 比較，再看讀取是否落在相同 atomic unit。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: AWUN]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `AWUN` | Atomic Write Unit Normal；controller 正常原子寫入大小的 0-based 欄位。 |
| `相關欄位` | Overlapping writes, Read result — 本圖討論正常運作下重疊寫入的可觀測結果；將 write size 與解碼後 AWUN 比較，再看讀取是否落在相同 atomic unit。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 本圖討論正常運作下重疊寫入的可觀測結果；將 write size 與解碼後 AWUN 比較，再看讀取是否落在相同 atomic unit。
3. 把大小、起始對齊、NSABP 與 MAM 一起讀。Atomicity 與資料已進入 nonvolatile media 是不同檢查項目，FUA／Flush 也不建立其他命令的排序。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 5 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 本圖討論正常運作下重疊寫入的可觀測結果；將 write size 與解碼後 AWUN 比較，再看讀取是否落在相同 atomic unit。 |
| 邊界 | 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。 |

**說明性範例。** 假設解碼後 boundary size=8 blocks、offset=0，從 LBA 4 寫 12 blocks 跨成 [4..7] 與 [8..15]。MAM 下各段原子，不能將兩段當作一個 transaction。原始 AWUN=7h 才代表 8 blocks。

**常見誤解。** 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Overlapping writes, Read result, AWUN

**來源 keyword 索引：** may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 5, 文件頁 17, PDF 頁 17

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 6: AWUPF/NAWUPF Example Initial State of NVM</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-006-CLAIM figure-table:NVMCS13-NVM-FIG-006 -->

**SPEC。** Figure 6〈AWUPF/NAWUPF Example Initial State of NVM〉：先保存失敗前的媒體內容與此次 write 範圍，這個 initial state 是下一張 failure-result 表的前提。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

先保存失敗前的媒體內容與此次 write 範圍，這個 initial state 是下一張 failure-result 表的前提。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: AWUPF]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `AWUPF` | Atomic Write Unit Power Fail；失敗條件原子大小的0-based欄位。 |
| `相關欄位` | Old data, New write — 先保存失敗前的媒體內容與此次 write 範圍，這個 initial state 是下一張 failure-result 表的前提。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 先保存失敗前的媒體內容與此次 write 範圍，這個 initial state 是下一張 failure-result 表的前提。
3. 把大小、起始對齊、NSABP 與 MAM 一起讀。Atomicity 與資料已進入 nonvolatile media 是不同檢查項目，FUA／Flush 也不建立其他命令的排序。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 6 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 先保存失敗前的媒體內容與此次 write 範圍，這個 initial state 是下一張 failure-result 表的前提。 |
| 邊界 | 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。 |

**說明性範例。** 假設解碼後 boundary size=8 blocks、offset=0，從 LBA 4 寫 12 blocks 跨成 [4..7] 與 [8..15]。MAM 下各段原子，不能將兩段當作一個 transaction。原始 AWUN=7h 才代表 8 blocks。

**常見誤解。** 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Old data, New write, AWUPF

**來源 keyword 索引：** shall

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 6, 文件頁 18, PDF 頁 18

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 7: AWUPF/NAWUPF Example Final State of NVM</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-007-CLAIM figure-table:NVMCS13-NVM-FIG-007 -->

**SPEC。** Figure 7〈AWUPF/NAWUPF Example Final State of NVM〉：把 power-fail 原子大小內的舊資料保留保證，與超過大小時可能 torn write 的結果分開；未完成寫入不能當作全新資料。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

把 power-fail 原子大小內的舊資料保留保證，與超過大小時可能 torn write 的結果分開；未完成寫入不能當作全新資料。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: AWUPF]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `AWUPF` | Atomic Write Unit Power Fail；失敗條件原子大小的0-based欄位。 |
| `相關欄位` | Old data, Torn write — 把 power-fail 原子大小內的舊資料保留保證，與超過大小時可能 torn write 的結果分開；未完成寫入不能當作全新資料。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 把 power-fail 原子大小內的舊資料保留保證，與超過大小時可能 torn write 的結果分開；未完成寫入不能當作全新資料。
3. 把大小、起始對齊、NSABP 與 MAM 一起讀。Atomicity 與資料已進入 nonvolatile media 是不同檢查項目，FUA／Flush 也不建立其他命令的排序。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 7 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 把 power-fail 原子大小內的舊資料保留保證，與超過大小時可能 torn write 的結果分開；未完成寫入不能當作全新資料。 |
| 邊界 | 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。 |

**說明性範例。** 假設解碼後 boundary size=8 blocks、offset=0，從 LBA 4 寫 12 blocks 跨成 [4..7] 與 [8..15]。MAM 下各段原子，不能將兩段當作一個 transaction。原始 AWUN=7h 才代表 8 blocks。

**常見誤解。** 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Old data, Torn write, AWUPF

**來源 keyword 索引：** shall

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 7, 文件頁 18, PDF 頁 18

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 8: Atomic Boundaries Example</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-008-CLAIM figure-table:NVMCS13-NVM-FIG-008 -->

**SPEC。** Figure 8〈Atomic Boundaries Example〉：在數線標出 offset+k×boundary size；長度小於 atomic size 仍可能因起點而跨 boundary。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

在數線標出 offset+k×boundary size；長度小於 atomic size 仍可能因起點而跨 boundary。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NABO]
          ↓
[擷取欄位: NABSN] → [套用編碼: NABSPF]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NABO` | Namespace Atomic Boundary Offset；決定第一個 boundary 的位置。 |
| `NABSN` | Normal／power-fail atomic boundary size；0 值與 NSABP 支援要依欄位定義判讀。 |
| `NABSPF` | Normal／power-fail atomic boundary size；0 值與 NSABP 支援要依欄位定義判讀。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 在數線標出 offset+k×boundary size；長度小於 atomic size 仍可能因起點而跨 boundary。
3. 把大小、起始對齊、NSABP 與 MAM 一起讀。Atomicity 與資料已進入 nonvolatile media 是不同檢查項目，FUA／Flush 也不建立其他命令的排序。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 8 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 在數線標出 offset+k×boundary size；長度小於 atomic size 仍可能因起點而跨 boundary。 |
| 邊界 | 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。 |

**說明性範例。** 假設解碼後 boundary size=8 blocks、offset=0，從 LBA 4 寫 12 blocks 跨成 [4..7] 與 [8..15]。MAM 下各段原子，不能將兩段當作一個 transaction。原始 AWUN=7h 才代表 8 blocks。

**常見誤解。** 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NABO, NABSN, NABSPF

**來源 keyword 索引：** shall, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 8, 文件頁 19, PDF 頁 19

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 9: Atomicity Parameter Differences for Multiple Atomicity Mode</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-009-CLAIM figure-table:NVMCS13-NVM-FIG-009 -->

**SPEC。** Figure 9〈Atomicity Parameter Differences for Multiple Atomicity Mode〉：Multiple 模式將適用 normal／power-fail size 與兩種 boundary size 對齊成相同值；fused 比對寫入仍遵守 Single 模式。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Multiple 模式將適用 normal／power-fail size 與兩種 boundary size 對齊成相同值；fused 比對寫入仍遵守 Single 模式。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MAM]
          ↓
[擷取欄位: NAWUN] → [套用編碼: NAWUPF]
                                      ↓
[驗證證據: NABSN]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MAM` | Multiple Atomicity Mode；跨 boundary 的命令分成各自原子的 subranges。 |
| `NAWUN` | Namespace normal／power-fail／compare-and-write 或 controller compare-and-write 原子大小；0-based。 |
| `NAWUPF` | Namespace normal／power-fail／compare-and-write 或 controller compare-and-write 原子大小；0-based。 |
| `NABSN` | Normal／power-fail atomic boundary size；0 值與 NSABP 支援要依欄位定義判讀。 |
| `NABSPF` | Normal／power-fail atomic boundary size；0 值與 NSABP 支援要依欄位定義判讀。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Multiple 模式將適用 normal／power-fail size 與兩種 boundary size 對齊成相同值；fused 比對寫入仍遵守 Single 模式。
3. 把大小、起始對齊、NSABP 與 MAM 一起讀。Atomicity 與資料已進入 nonvolatile media 是不同檢查項目，FUA／Flush 也不建立其他命令的排序。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 9 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Multiple 模式將適用 normal／power-fail size 與兩種 boundary size 對齊成相同值；fused 比對寫入仍遵守 Single 模式。 |
| 邊界 | 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。 |

**說明性範例。** 假設解碼後 boundary size=8 blocks、offset=0，從 LBA 4 寫 12 blocks 跨成 [4..7] 與 [8..15]。MAM 下各段原子，不能將兩段當作一個 transaction。原始 AWUN=7h 才代表 8 blocks。

**常見誤解。** 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** MAM, NAWUN, NAWUPF, NABSN, NABSPF

**來源 keyword 索引：** shall, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 9, 文件頁 20, PDF 頁 20

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 10: Multiple Atomicity Example</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-010-CLAIM figure-table:NVMCS13-NVM-FIG-010 -->

**SPEC。** Figure 10〈Multiple Atomicity Example〉：Single 模式要分開的 A/B/C，在 Multiple 模式可由 D 覆蓋，但保證仍以每個切出的 subrange 為單位，不是 D 整體 transaction。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Single 模式要分開的 A/B/C，在 Multiple 模式可由 D 覆蓋，但保證仍以每個切出的 subrange 為單位，不是 D 整體 transaction。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Write A, Write B, Write C, Write D, Atomic subranges — Single 模式要分開的 A/B/C，在 Multiple 模式可由 D 覆蓋，但保證仍以每個切出的 subrange 為單位，不是 D 整體 transaction。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Single 模式要分開的 A/B/C，在 Multiple 模式可由 D 覆蓋，但保證仍以每個切出的 subrange 為單位，不是 D 整體 transaction。
3. 把大小、起始對齊、NSABP 與 MAM 一起讀。Atomicity 與資料已進入 nonvolatile media 是不同檢查項目，FUA／Flush 也不建立其他命令的排序。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 10 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Single 模式要分開的 A/B/C，在 Multiple 模式可由 D 覆蓋，但保證仍以每個切出的 subrange 為單位，不是 D 整體 transaction。 |
| 邊界 | 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。 |

**說明性範例。** 假設解碼後 boundary size=8 blocks、offset=0，從 LBA 4 寫 12 blocks 跨成 [4..7] 與 [8..15]。MAM 下各段原子，不能將兩段當作一個 transaction。原始 AWUN=7h 才代表 8 blocks。

**常見誤解。** 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Write A, Write B, Write C, Write D, Atomic subranges

**來源 keyword 索引：** shall, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 10, 文件頁 21, PDF 頁 21

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 11: Protection Information Field Definition</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-011-CLAIM figure-table:NVMCS13-NVM-FIG-011 -->

**SPEC。** Figure 11〈Protection Information Field Definition〉：PRACT 是 action，PRCHK 是三種檢查的 bit mask。PRACT=1 時先比較 MS 與 PI size，才能知道資料是否 strip／insert 或維持 metadata 大小。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

PRACT 是 action，PRCHK 是三種檢查的 bit mask。PRACT=1 時先比較 MS 與 PI size，才能知道資料是否 strip／insert 或維持 metadata 大小。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

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
| `PRACT` | Protection Information Action；依命令與 MS 選擇 PI 處理。 |
| `PRCHK` | Protection Information Check；Guard、Application、Reference 的檢查 bits。 |
| `GRDCHK` | PRCHK 的 Guard／Application／Reference 檢查選擇；另須套用 PI 特殊停用值規則。 |
| `ATCHK` | PRCHK 的 Guard／Application／Reference 檢查選擇；另須套用 PI 特殊停用值規則。 |
| `RTCHK` | PRCHK 的 Guard／Application／Reference 檢查選擇；另須套用 PI 特殊停用值規則。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. PRACT 是 action，PRCHK 是三種檢查的 bit mask。PRACT=1 時先比較 MS 與 PI size，才能知道資料是否 strip／insert 或維持 metadata 大小。
3. 先檢查 namespace 是否啟用 PI，再依命令方向及 metadata 大小選處理分支。Checking bits 與可能的特殊停用值放在最後判斷。
4. 套用下方情境，保存原命令、target 與結果。

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
| 判讀 | PRACT 是 action，PRCHK 是三種檢查的 bit mask。PRACT=1 時先比較 MS 與 PI size，才能知道資料是否 strip／insert 或維持 metadata 大小。 |
| 邊界 | STC 在本份指 Storage Tag Check；不要沿用 Self-test Code 的縮寫解釋。Compare 的兩條輸入路徑都可能執行 PI checking，但 PI bytes 不納入一般 metadata 比對。 |

**說明性範例。** 16b Guard、MS=16、Read PRACT=1：host 仍接收 16 bytes metadata；若 MS=8，則 host 只接收 data。相同 PRACT 在不同 MS 下造成不同 buffer 大小。

**常見誤解。** STC 在本份指 Storage Tag Check；不要沿用 Self-test Code 的縮寫解釋。Compare 的兩條輸入路徑都可能執行 PI checking，但 PI bytes 不納入一般 metadata 比對。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | STC 在本份指 Storage Tag Check；不要沿用 Self-test Code 的縮寫解釋。Compare 的兩條輸入路徑都可能執行 PI checking，但 PI bytes 不納入一般 metadata 比對。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** PRACT, PRCHK, GRDCHK, ATCHK, RTCHK

**來源 keyword 索引：** shall not, shall, may, optional, mandatory

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5, Figure 11, 文件頁 21-22, PDF 頁 21-22

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 12: Storage Tag Check Definition</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-012-CLAIM figure-table:NVMCS13-NVM-FIG-012 -->

**SPEC。** Figure 12〈Storage Tag Check Definition〉：STC 啟用 Storage Tag checking；STS=0 時沒有 Storage Tag，controller 忽略 STC。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

STC 啟用 Storage Tag checking；STS=0 時沒有 Storage Tag，controller 忽略 STC。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: STC]
          ↓
[擷取欄位: STS] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `STC` | Storage Tag Check；獨立於三位元 PRCHK，STS=0 時忽略。 |
| `STS` | Storage Tag Size；固定 Storage/Reference Space 中的高位 bit 數。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. STC 啟用 Storage Tag checking；STS=0 時沒有 Storage Tag，controller 忽略 STC。
3. 先檢查 namespace 是否啟用 PI，再依命令方向及 metadata 大小選處理分支。Checking bits 與可能的特殊停用值放在最後判斷。
4. 套用下方情境，保存原命令、target 與結果。

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
| 判讀 | STC 啟用 Storage Tag checking；STS=0 時沒有 Storage Tag，controller 忽略 STC。 |
| 邊界 | STC 在本份指 Storage Tag Check；不要沿用 Self-test Code 的縮寫解釋。Compare 的兩條輸入路徑都可能執行 PI checking，但 PI bytes 不納入一般 metadata 比對。 |

**說明性範例。** 16b Guard、MS=16、Read PRACT=1：host 仍接收 16 bytes metadata；若 MS=8，則 host 只接收 data。相同 PRACT 在不同 MS 下造成不同 buffer 大小。

**常見誤解。** STC 在本份指 Storage Tag Check；不要沿用 Self-test Code 的縮寫解釋。Compare 的兩條輸入路徑都可能執行 PI checking，但 PI bytes 不納入一般 metadata 比對。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | STC 在本份指 Storage Tag Check；不要沿用 Self-test Code 的縮寫解釋。Compare 的兩條輸入路徑都可能執行 PI checking，但 PI bytes 不納入一般 metadata 比對。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** STC, STS

**來源 keyword 索引：** shall not, shall, may, optional, mandatory

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5, Figure 12, 文件頁 22, PDF 頁 22

</details>

<a id="section-2-2"></a>

### §2.2

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 13: NVM Command Set Admin Command Support</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-013-CLAIM figure-table:NVMCS13-NVM-FIG-013 -->

**SPEC。** Figure 13〈NVM Command Set Admin Command Support〉：Get LBA Status 86h 對 I/O controller 是 optional、對 Administrative controller 禁止；本工作表只保留這兩欄。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Get LBA Status 86h 對 I/O controller 是 optional、對 Administrative controller 禁止；本工作表只保留這兩欄。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Get LBA Status, I/O controller, Administrative controller — Get LBA Status 86h 對 I/O controller 是 optional、對 Administrative controller 禁止；本工作表只保留這兩欄。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Get LBA Status 86h 對 I/O controller 是 optional、對 Administrative controller 禁止；本工作表只保留這兩欄。
3. 從 controller 類型開始建立命令、Feature、log 的能力矩陣。資料指標指向的可能是使用者資料，也可能只是控制 descriptor。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 13 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Get LBA Status 86h 對 I/O controller 是 optional、對 Administrative controller 禁止；本工作表只保留這兩欄。 |
| 邊界 | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

**說明性範例。** Copy opcode=19h 的低 bits 是 01b，因 host 傳入 source descriptors；並不表示需要把整份待複製資料從 host 再傳一次。

**常見誤解。** FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Get LBA Status, I/O controller, Administrative controller

**來源 keyword 索引：** optional, mandatory

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.2.1, Figure 13, 文件頁 23, PDF 頁 23

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 14: I/O Controller – NVM Command Set I/O Command Support</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-014-CLAIM figure-table:NVMCS13-NVM-FIG-014 -->

**SPEC。** Figure 14〈I/O Controller – NVM Command Set I/O Command Support〉：Read／Write 是 mandatory；Compare、Verify、Copy、Write Zeroes、Write Uncorrectable 等須檢查各自能力，不能用表列存在代替支援宣告。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Read／Write 是 mandatory；Compare、Verify、Copy、Write Zeroes、Write Uncorrectable 等須檢查各自能力，不能用表列存在代替支援宣告。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Read, Write, Optional commands — Read／Write 是 mandatory；Compare、Verify、Copy、Write Zeroes、Write Uncorrectable 等須檢查各自能力，不能用表列存在代替支援宣告。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Read／Write 是 mandatory；Compare、Verify、Copy、Write Zeroes、Write Uncorrectable 等須檢查各自能力，不能用表列存在代替支援宣告。
3. 從 controller 類型開始建立命令、Feature、log 的能力矩陣。資料指標指向的可能是使用者資料，也可能只是控制 descriptor。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 14 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Read／Write 是 mandatory；Compare、Verify、Copy、Write Zeroes、Write Uncorrectable 等須檢查各自能力，不能用表列存在代替支援宣告。 |
| 邊界 | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

**說明性範例。** Copy opcode=19h 的低 bits 是 01b，因 host 傳入 source descriptors；並不表示需要把整份待複製資料從 host 再傳一次。

**常見誤解。** FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Read, Write, Optional commands

**來源 keyword 索引：** optional, mandatory

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.2.1, Figure 14, 文件頁 23, PDF 頁 23

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 15: NVM Command Set Log Page Support</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-015-CLAIM figure-table:NVMCS13-NVM-FIG-015 -->

**SPEC。** Figure 15〈NVM Command Set Log Page Support〉：0Eh 為 I/O controller 的 optional log；28h 對 I/O 與 Administrative controllers 都是 optional。支援與作用域另查 log 定義。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

0Eh 為 I/O controller 的 optional log；28h 對 I/O 與 Administrative controllers 都是 optional。支援與作用域另查 log 定義。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | LID 0Eh, LID 28h — 0Eh 為 I/O controller 的 optional log；28h 對 I/O 與 Administrative controllers 都是 optional。支援與作用域另查 log 定義。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 0Eh 為 I/O controller 的 optional log；28h 對 I/O 與 Administrative controllers 都是 optional。支援與作用域另查 log 定義。
3. 從 controller 類型開始建立命令、Feature、log 的能力矩陣。資料指標指向的可能是使用者資料，也可能只是控制 descriptor。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 15 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.2.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 0Eh 為 I/O controller 的 optional log；28h 對 I/O 與 Administrative controllers 都是 optional。支援與作用域另查 log 定義。 |
| 邊界 | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

**說明性範例。** Copy opcode=19h 的低 bits 是 01b，因 host 傳入 source descriptors；並不表示需要把整份待複製資料從 host 再傳一次。

**常見誤解。** FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LID 0Eh, LID 28h

**來源 keyword 索引：** optional, mandatory

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.2.2, Figure 15, 文件頁 23, PDF 頁 23

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 16: NVM Command Set Feature Support</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-016-CLAIM figure-table:NVMCS13-NVM-FIG-016 -->

**SPEC。** Figure 16〈NVM Command Set Feature Support〉：將各 Feature 的 support row 與 controller 類型對照；Administrative controller 的 Performance Characteristics 不允許 namespace scope。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

將各 Feature 的 support row 與 controller 類型對照；Administrative controller 的 Performance Characteristics 不允許 namespace scope。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | FID 03h, FID 05h, FID 0Ah, FID 15h, FID 1Ch, FID 28h — 將各 Feature 的 support row 與 controller 類型對照；Administrative controller 的 Performance Characteristics 不允許 namespace scope。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 將各 Feature 的 support row 與 controller 類型對照；Administrative controller 的 Performance Characteristics 不允許 namespace scope。
3. 從 controller 類型開始建立命令、Feature、log 的能力矩陣。資料指標指向的可能是使用者資料，也可能只是控制 descriptor。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 16 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 將各 Feature 的 support row 與 controller 類型對照；Administrative controller 的 Performance Characteristics 不允許 namespace scope。 |
| 邊界 | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

**說明性範例。** Copy opcode=19h 的低 bits 是 01b，因 host 傳入 source descriptors；並不表示需要把整份待複製資料從 host 再傳一次。

**常見誤解。** FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** FID 03h, FID 05h, FID 0Ah, FID 15h, FID 1Ch, FID 28h

**來源 keyword 索引：** optional, mandatory

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.2.3, Figure 16, 文件頁 23-24, PDF 頁 23-24

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 17: NVM Command Set Feature Logged in Persistent Event Log Page Requirement</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-017-CLAIM figure-table:NVMCS13-NVM-FIG-017 -->

**SPEC。** Figure 17〈NVM Command Set Feature Logged in Persistent Event Log Page Requirement〉：此表是是否將 Feature 更新寫入 Persistent Event Log 的要求；03h 的 NR 不是禁止使用該 Feature，也不是其他 Features 的支援等級。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

此表是是否將 Feature 更新寫入 Persistent Event Log 的要求；03h 的 NR 不是禁止使用該 Feature，也不是其他 Features 的支援等級。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Persistent Event Log, Optional, Not recommended — 此表是是否將 Feature 更新寫入 Persistent Event Log 的要求；03h 的 NR 不是禁止使用該 Feature，也不是其他 Features 的支援等級。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 此表是是否將 Feature 更新寫入 Persistent Event Log 的要求；03h 的 NR 不是禁止使用該 Feature，也不是其他 Features 的支援等級。
3. 從 controller 類型開始建立命令、Feature、log 的能力矩陣。資料指標指向的可能是使用者資料，也可能只是控制 descriptor。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 17 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §2.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 此表是是否將 Feature 更新寫入 Persistent Event Log 的要求；03h 的 NR 不是禁止使用該 Feature，也不是其他 Features 的支援等級。 |
| 邊界 | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

**說明性範例。** Copy opcode=19h 的低 bits 是 01b，因 host 傳入 source descriptors；並不表示需要把整份待複製資料從 host 再傳一次。

**常見誤解。** FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Persistent Event Log, Optional, Not recommended

**來源 keyword 索引：** optional, mandatory

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.2.3, Figure 17, 文件頁 24, PDF 頁 24

</details>

<a id="section-3-1"></a>

### §3.1

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 18: Status Code – Generic Command Status Values</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-018-CLAIM figure-table:NVMCS13-NVM-FIG-018 -->

**SPEC。** Figure 18〈Status Code – Generic Command Status Values〉：Generic status 80h 是 LBA Out of Range，81h 是 Capacity Exceeded；解碼前保留 SCT，並分別核對 NSZE 與 NCAP／NUSE。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Generic status 80h 是 LBA Out of Range，81h 是 Capacity Exceeded；解碼前保留 SCT，並分別核對 NSZE 與 NCAP／NUSE。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SCT]
          ↓
[擷取欄位: SC] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SCT` | Status Code Type 與 Status Code；兩欄共同識別錯誤，單看 SC 可能誤判。 |
| `SC` | Status Code Type 與 Status Code；兩欄共同識別錯誤，單看 SC 可能誤判。 |
| `相關欄位` | LBA Out of Range, Capacity Exceeded — Generic status 80h 是 LBA Out of Range，81h 是 Capacity Exceeded；解碼前保留 SCT，並分別核對 NSZE 與 NCAP／NUSE。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Generic status 80h 是 LBA Out of Range，81h 是 Capacity Exceeded；解碼前保留 SCT，並分別核對 NSZE 與 NCAP／NUSE。
3. 從 controller 類型開始建立命令、Feature、log 的能力矩陣。資料指標指向的可能是使用者資料，也可能只是控制 descriptor。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 18 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Generic status 80h 是 LBA Out of Range，81h 是 Capacity Exceeded；解碼前保留 SCT，並分別核對 NSZE 與 NCAP／NUSE。 |
| 邊界 | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

**說明性範例。** Copy opcode=19h 的低 bits 是 01b，因 host 傳入 source descriptors；並不表示需要把整份待複製資料從 host 再傳一次。

**常見誤解。** FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SCT, SC, LBA Out of Range, Capacity Exceeded

**來源 keyword 索引：** may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.1.2, Figure 18, 文件頁 25, PDF 頁 25

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 19: Status Code – Command Specific Status Values</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-019-CLAIM figure-table:NVMCS13-NVM-FIG-019 -->

**SPEC。** Figure 19〈Status Code – Command Specific Status Values〉：用 opcode 與 SCT=1 找對應 command-specific status；例如 Copy 的格式／重疊錯誤與 Read 的 PI 錯誤有不同適用集合。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

用 opcode 與 SCT=1 找對應 command-specific status；例如 Copy 的格式／重疊錯誤與 Read 的 PI 錯誤有不同適用集合。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | SCT=1, Command-specific status — 用 opcode 與 SCT=1 找對應 command-specific status；例如 Copy 的格式／重疊錯誤與 Read 的 PI 錯誤有不同適用集合。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 用 opcode 與 SCT=1 找對應 command-specific status；例如 Copy 的格式／重疊錯誤與 Read 的 PI 錯誤有不同適用集合。
3. 從 controller 類型開始建立命令、Feature、log 的能力矩陣。資料指標指向的可能是使用者資料，也可能只是控制 descriptor。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 19 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 用 opcode 與 SCT=1 找對應 command-specific status；例如 Copy 的格式／重疊錯誤與 Read 的 PI 錯誤有不同適用集合。 |
| 邊界 | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

**說明性範例。** Copy opcode=19h 的低 bits 是 01b，因 host 傳入 source descriptors；並不表示需要把整份待複製資料從 host 再傳一次。

**常見誤解。** FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SCT=1, Command-specific status

**來源 keyword 索引：** may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.1.2, Figure 19, 文件頁 25, PDF 頁 25

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 20: Status Code – Media and Data Integrity Error Values</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-020-CLAIM figure-table:NVMCS13-NVM-FIG-020 -->

**SPEC。** Figure 20〈Status Code – Media and Data Integrity Error Values〉：Media/Data Integrity 類型含 Compare miscompare 與 deallocated/unwritten 存取錯誤；後者要回查 DULBE，而非直接判為壞媒體。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Media/Data Integrity 類型含 Compare miscompare 與 deallocated/unwritten 存取錯誤；後者要回查 DULBE，而非直接判為壞媒體。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Compare Failure, Deallocated or Unwritten Logical Block — Media/Data Integrity 類型含 Compare miscompare 與 deallocated/unwritten 存取錯誤；後者要回查 DULBE，而非直接判為壞媒體。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Media/Data Integrity 類型含 Compare miscompare 與 deallocated/unwritten 存取錯誤；後者要回查 DULBE，而非直接判為壞媒體。
3. 從 controller 類型開始建立命令、Feature、log 的能力矩陣。資料指標指向的可能是使用者資料，也可能只是控制 descriptor。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 20 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.1.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Media/Data Integrity 類型含 Compare miscompare 與 deallocated/unwritten 存取錯誤；後者要回查 DULBE，而非直接判為壞媒體。 |
| 邊界 | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

**說明性範例。** Copy opcode=19h 的低 bits 是 01b，因 host 傳入 source descriptors；並不表示需要把整份待複製資料從 host 再傳一次。

**常見誤解。** FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Compare Failure, Deallocated or Unwritten Logical Block

**來源 keyword 索引：** shall, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.1.2, Figure 20, 文件頁 26, PDF 頁 26

</details>

<a id="section-3-2"></a>

### §3.2

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 21: Reclaim Unit Handle Status Descriptor</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-021-CLAIM figure-table:NVMCS13-NVM-FIG-021 -->

**SPEC。** Figure 21〈Reclaim Unit Handle Status Descriptor〉：以 PID 找 Placement Handle／Reclaim Group，再解讀 RUHID、剩餘時間估計及可寫 blocks；RUAMW 不是固定的 nominal RU size。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

以 PID 找 Placement Handle／Reclaim Group，再解讀 RUHID、剩餘時間估計及可寫 blocks；RUAMW 不是固定的 nominal RU size。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | PID, RUHID, EARUTR, RUAMW — 以 PID 找 Placement Handle／Reclaim Group，再解讀 RUHID、剩餘時間估計及可寫 blocks；RUAMW 不是固定的 nominal RU size。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 以 PID 找 Placement Handle／Reclaim Group，再解讀 RUHID、剩餘時間估計及可寫 blocks；RUAMW 不是固定的 nominal RU size。
3. 建立時決定 placement 關係，執行時看 handle status，事後再用 statistics／events 解釋媒體搬移。三種資料不能互相代替。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 21 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.2.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 以 PID 找 Placement Handle／Reclaim Group，再解讀 RUHID、剩餘時間估計及可寫 blocks；RUAMW 不是固定的 nominal RU size。 |
| 邊界 | Media Reallocated event 的 LBA 是搬移集合中的一個 LBA，並不是完整清單；LBAV=0 時必須忽略。 |

**說明性範例。** 兩個 namespaces 共享 RUH 5，第一個使用 FIDX=2，第二個 create 指定 FIDX=3，即使資料大小同為 4 KiB，也不符合共享 RUH 的 Format Index 條件。

**常見誤解。** Media Reallocated event 的 LBA 是搬移集合中的一個 LBA，並不是完整清單；LBAV=0 時必須忽略。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Media Reallocated event 的 LBA 是搬移集合中的一個 LBA，並不是完整清單；LBAV=0 時必須忽略。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** PID, RUHID, EARUTR, RUAMW

**來源 keyword 索引：** shall, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.2.1.1, Figure 21, 文件頁 26, PDF 頁 26

</details>

<a id="section-3-3"></a>

### §3.3

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 22: Opcodes for NVM Commands</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-022-CLAIM figure-table:NVMCS13-NVM-FIG-022 -->

**SPEC。** Figure 22〈Opcodes for NVM Commands〉：Opcode 低兩 bits 指示資料傳輸方向；Copy 的 host-to-controller 是 descriptors。除特別註明的命令外，不能使用 broadcast NSID。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Opcode 低兩 bits 指示資料傳輸方向；Copy 的 host-to-controller 是 descriptors。除特別註明的命令外，不能使用 broadcast NSID。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSID]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSID` | Namespace 識別碼；SNSID 選 Copy 來源，ENSID 選匯出 namespace，合法值受個別命令約束。 |
| `相關欄位` | Opcode, Transfer direction — Opcode 低兩 bits 指示資料傳輸方向；Copy 的 host-to-controller 是 descriptors。除特別註明的命令外，不能使用 broadcast NSID。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Opcode 低兩 bits 指示資料傳輸方向；Copy 的 host-to-controller 是 descriptors。除特別註明的命令外，不能使用 broadcast NSID。
3. 從 controller 類型開始建立命令、Feature、log 的能力矩陣。資料指標指向的可能是使用者資料，也可能只是控制 descriptor。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 22 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Opcode 低兩 bits 指示資料傳輸方向；Copy 的 host-to-controller 是 descriptors。除特別註明的命令外，不能使用 broadcast NSID。 |
| 邊界 | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

**說明性範例。** Copy opcode=19h 的低 bits 是 01b，因 host 傳入 source descriptors；並不表示需要把整份待複製資料從 host 再傳一次。

**常見誤解。** FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Opcode, NSID, Transfer direction

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3, Figure 22, 文件頁 27, PDF 頁 27

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 23: Compare – Metadata Pointer</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-023-CLAIM figure-table:NVMCS13-NVM-FIG-023 -->

**SPEC。** Figure 23〈Compare – Metadata Pointer〉：MPTR 只在所選格式使用 separate metadata 時提供 metadata 位置；先核對 PSDT／metadata 格式，不能把它當成 user-data buffer。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

MPTR 只在所選格式使用 separate metadata 時提供 metadata 位置；先核對 PSDT／metadata 格式，不能把它當成 user-data buffer。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MPTR]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MPTR` | Separate metadata 的指標；metadata placement 由 namespace format 與命令欄位決定。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. MPTR 只在所選格式使用 separate metadata 時提供 metadata 位置；先核對 PSDT／metadata 格式，不能把它當成 user-data buffer。
3. 比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 23 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | MPTR 只在所選格式使用 separate metadata 時提供 metadata 位置；先核對 PSDT／metadata 格式，不能把它當成 user-data buffer。 |
| 邊界 | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

**說明性範例。** 要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。

**常見誤解。** Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** MPTR

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 23, 文件頁 28, PDF 頁 28

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 24: Compare – Data Pointer</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-024-CLAIM figure-table:NVMCS13-NVM-FIG-024 -->

**SPEC。** Figure 24〈Compare – Data Pointer〉：這裡的 DPTR 指向 host 輸入資料：Compare 的 expected data 或 Write 的新資料；PRP／SGL 由 common command format 決定。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

這裡的 DPTR 指向 host 輸入資料：Compare 的 expected data 或 Write 的新資料；PRP／SGL 由 common command format 決定。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

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
| `DPTR` | 命令 data pointer；Read 是目的、Write 是來源、Copy／DSM 指向 descriptors。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 這裡的 DPTR 指向 host 輸入資料：Compare 的 expected data 或 Write 的新資料；PRP／SGL 由 common command format 決定。
3. 比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 24 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 這裡的 DPTR 指向 host 輸入資料：Compare 的 expected data 或 Write 的新資料；PRP／SGL 由 common command format 決定。 |
| 邊界 | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

**說明性範例。** 要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。

**常見誤解。** Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DPTR

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 24, 文件頁 28, PDF 頁 28

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 25: Compare – Command Dword 2 and Dword 3</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-025-CLAIM figure-table:NVMCS13-NVM-FIG-025 -->

**SPEC。** Figure 25〈Compare – Command Dword 2 and Dword 3〉：CDW2／3 的 upper tags 要和 CDW14 lower tags 合併，再依 PI 格式與 STS 拆成 expected storage／reference；unused bits 依格式忽略。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW2／3 的 upper tags 要和 CDW14 lower tags 合併，再依 PI 格式與 STS 拆成 expected storage／reference；unused bits 依格式忽略。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ELBTU]
          ↓
[擷取欄位: ELBTL] → [套用編碼: ELBST]
                                      ↓
[驗證證據: EILBRT]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ELBTU` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `ELBTL` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `ELBST` | Logical Block Storage Tag／Expected Logical Block Storage Tag；寬度由 STS 決定。 |
| `EILBRT` | Initial Logical Block Reference Tag／expected 初值；Type 1／2 依 block 遞增並在欄位寬度處回捲。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW2／3 的 upper tags 要和 CDW14 lower tags 合併，再依 PI 格式與 STS 拆成 expected storage／reference；unused bits 依格式忽略。
3. 比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 25 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW2／3 的 upper tags 要和 CDW14 lower tags 合併，再依 PI 格式與 STS 拆成 expected storage／reference；unused bits 依格式忽略。 |
| 邊界 | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

**說明性範例。** 要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。

**常見誤解。** Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** ELBTU, ELBTL, ELBST, EILBRT

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 25, 文件頁 28, PDF 頁 28

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 26: Compare – Command Dword 10 and Command Dword 11</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-026-CLAIM figure-table:NVMCS13-NVM-FIG-026 -->

**SPEC。** Figure 26〈Compare – Command Dword 10 and Command Dword 11〉：64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SLBA]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SLBA` | 範圍起始 LBA；SDLBA 選 Copy 目的，DSLBA 是 Get LBA Status descriptor 的起點。 |
| `相關欄位` | CDW10, CDW11 — 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。
3. 比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 26 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 |
| 邊界 | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

**說明性範例。** 要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。

**常見誤解。** Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SLBA, CDW10, CDW11

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 26, 文件頁 28, PDF 頁 28

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 27: Compare – Command Dword 12</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-027-CLAIM figure-table:NVMCS13-NVM-FIG-027 -->

**SPEC。** Figure 27〈Compare – Command Dword 12〉：CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LR]
          ↓
[擷取欄位: FUA] → [套用編碼: PRINFO]
                                      ↓
[驗證證據: STC]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LR` | Limited Retry；指定受 Error Recovery policy 約束的重試行為。 |
| `FUA` | Force Unit Access；要求 nonvolatile-media 語意，不自動建立其他命令的順序。 |
| `PRINFO` | PRACT 與 PRCHK 的組合欄位；Copy 的 R／W 版本分別控制讀端／寫端。 |
| `STC` | Storage Tag Check；獨立於三位元 PRCHK，STS=0 時忽略。 |
| `CETYPE` | Command Extension Type／Value；Type 先決定 Value 的用途，不能固定當作 DSM hints。 |
| `NLB` | Number of Logical Blocks；本報告命令／status descriptors 的該欄為 0-based。DSM 的 LLB 另為1-based。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。
3. 比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 27 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。 |
| 邊界 | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

**說明性範例。** 要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。

**常見誤解。** Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LR, FUA, PRINFO, STC, CETYPE, NLB

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 27, 文件頁 28-29, PDF 頁 28-29

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 28: Compare - Command Dword 13 if CETYPE is non-zero</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-028-CLAIM figure-table:NVMCS13-NVM-FIG-028 -->

**SPEC。** Figure 28〈Compare - Command Dword 13 if CETYPE is non-zero〉：CETYPE 非零時 CDW13 low16 解讀為 CEV；CETYPE=0 的 layout 另有定義或 reserved，不能同時塞 DSM hints。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CETYPE 非零時 CDW13 low16 解讀為 CEV；CETYPE=0 的 layout 另有定義或 reserved，不能同時塞 DSM hints。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CETYPE]
          ↓
[擷取欄位: CEV] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CETYPE` | Command Extension Type／Value；Type 先決定 Value 的用途，不能固定當作 DSM hints。 |
| `CEV` | Command Extension Type／Value；Type 先決定 Value 的用途，不能固定當作 DSM hints。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CETYPE 非零時 CDW13 low16 解讀為 CEV；CETYPE=0 的 layout 另有定義或 reserved，不能同時塞 DSM hints。
3. 比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 28 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CETYPE 非零時 CDW13 low16 解讀為 CEV；CETYPE=0 的 layout 另有定義或 reserved，不能同時塞 DSM hints。 |
| 邊界 | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

**說明性範例。** 要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。

**常見誤解。** Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** CETYPE, CEV

**來源 keyword 索引：** shall, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 28, 文件頁 29, PDF 頁 29

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 29: Compare – Command Dword 14</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-029-CLAIM figure-table:NVMCS13-NVM-FIG-029 -->

**SPEC。** Figure 29〈Compare – Command Dword 14〉：CDW14 是 expected-tag 空間低 32 bits；它未必全是 Reference Tag，STS 可能占用其中高 bits。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW14 是 expected-tag 空間低 32 bits；它未必全是 Reference Tag，STS 可能占用其中高 bits。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ELBTL]
          ↓
[擷取欄位: ELBTU] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ELBTL` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `ELBTU` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW14 是 expected-tag 空間低 32 bits；它未必全是 Reference Tag，STS 可能占用其中高 bits。
3. 比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 29 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW14 是 expected-tag 空間低 32 bits；它未必全是 Reference Tag，STS 可能占用其中高 bits。 |
| 邊界 | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

**說明性範例。** 要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。

**常見誤解。** Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** ELBTL, ELBTU

**來源 keyword 索引：** shall, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 29, 文件頁 29, PDF 頁 29

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 30: Compare – Command Dword 15</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-030-CLAIM figure-table:NVMCS13-NVM-FIG-030 -->

**SPEC。** Figure 30〈Compare – Command Dword 15〉：CDW15 high16 是 Application Tag mask，low16 是 expected tag；mask bit=0 表示不比較該位，不是要求 tag bit=0。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW15 high16 是 Application Tag mask，low16 是 expected tag；mask bit=0 表示不比較該位，不是要求 tag bit=0。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ELBATM]
          ↓
[擷取欄位: ELBAT] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ELBATM` | Tag comparison mask；bit=0 排除比較，Storage mask 額外受支援與對齊限制。 |
| `ELBAT` | Logical Block Application Tag／expected tag；16-bit，checking 與 mask 及停用值規則共同決定。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW15 high16 是 Application Tag mask，low16 是 expected tag；mask bit=0 表示不比較該位，不是要求 tag bit=0。
3. 比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 30 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW15 high16 是 Application Tag mask，low16 是 expected tag；mask bit=0 表示不比較該位，不是要求 tag bit=0。 |
| 邊界 | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

**說明性範例。** 要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。

**常見誤解。** Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** ELBATM, ELBAT

**來源 keyword 索引：** shall, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 30, 文件頁 29, PDF 頁 29

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 31: Compare – Command Specific Status Values</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-031-CLAIM figure-table:NVMCS13-NVM-FIG-031 -->

**SPEC。** Figure 31〈Compare – Command Specific Status Values〉：把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SCT]
          ↓
[擷取欄位: SC] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SCT` | Status Code Type 與 Status Code；兩欄共同識別錯誤，單看 SC 可能誤判。 |
| `SC` | Status Code Type 與 Status Code；兩欄共同識別錯誤，單看 SC 可能誤判。 |
| `相關欄位` | Command-specific error — 把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。
3. 比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 31 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。 |
| 邊界 | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

**說明性範例。** 要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。

**常見誤解。** Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SCT, SC, Command-specific error

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 31, 文件頁 30, PDF 頁 30

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 32: Copy – Data Pointer</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-032-CLAIM figure-table:NVMCS13-NVM-FIG-032 -->

**SPEC。** Figure 32〈Copy – Data Pointer〉：DPTR 指向 descriptors，而不是待複製或 deallocate 的 user data；buffer 長度需由 descriptor size 與解碼後 range count 計算。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

DPTR 指向 descriptors，而不是待複製或 deallocate 的 user data；buffer 長度需由 descriptor size 與解碼後 range count 計算。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

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
| `DPTR` | 命令 data pointer；Read 是目的、Write 是來源、Copy／DSM 指向 descriptors。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. DPTR 指向 descriptors，而不是待複製或 deallocate 的 user data；buffer 長度需由 descriptor size 與解碼後 range count 計算。
3. 先計算展開後的目的區間，再檢查格式、長度限制、重疊與 atomicity。Copy 可少用 host 資料傳輸，但不是無條件的 transaction。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 32 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | DPTR 指向 descriptors，而不是待複製或 deallocate 的 user data；buffer 長度需由 descriptor size 與解碼後 range count 計算。 |
| 邊界 | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

**說明性範例。** 兩個 source descriptors 的 NLB 都是 3，SDLBA=100：第一段寫 100..103、第二段寫 104..107，共 8 blocks。若 DW0=1，不能據此保證第二段或更後面完全未修改。

**常見誤解。** FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DPTR

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 32, 文件頁 30, PDF 頁 30

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 33: Copy – Command Dword 2 and Dword 3</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-033-CLAIM figure-table:NVMCS13-NVM-FIG-033 -->

**SPEC。** Figure 33〈Copy – Command Dword 2 and Dword 3〉：Upper／lower tag 欄位組成寫入端的 Storage 與初始 Reference Tag；Copy 的這組 command fields 屬於 destination，source expectations 在 descriptors。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Upper／lower tag 欄位組成寫入端的 Storage 與初始 Reference Tag；Copy 的這組 command fields 屬於 destination，source expectations 在 descriptors。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBTU]
          ↓
[擷取欄位: LBTL] → [套用編碼: LBST]
                                      ↓
[驗證證據: ILBRT]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBTU` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `LBTL` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `LBST` | Logical Block Storage Tag／Expected Logical Block Storage Tag；寬度由 STS 決定。 |
| `ILBRT` | Initial Logical Block Reference Tag／expected 初值；Type 1／2 依 block 遞增並在欄位寬度處回捲。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Upper／lower tag 欄位組成寫入端的 Storage 與初始 Reference Tag；Copy 的這組 command fields 屬於 destination，source expectations 在 descriptors。
3. 先計算展開後的目的區間，再檢查格式、長度限制、重疊與 atomicity。Copy 可少用 host 資料傳輸，但不是無條件的 transaction。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 33 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Upper／lower tag 欄位組成寫入端的 Storage 與初始 Reference Tag；Copy 的這組 command fields 屬於 destination，source expectations 在 descriptors。 |
| 邊界 | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

**說明性範例。** 兩個 source descriptors 的 NLB 都是 3，SDLBA=100：第一段寫 100..103、第二段寫 104..107，共 8 blocks。若 DW0=1，不能據此保證第二段或更後面完全未修改。

**常見誤解。** FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LBTU, LBTL, LBST, ILBRT

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 33, 文件頁 30, PDF 頁 30

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 34: Copy – Command Dword 10 and Command Dword 11</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-034-CLAIM figure-table:NVMCS13-NVM-FIG-034 -->

**SPEC。** Figure 34〈Copy – Command Dword 10 and Command Dword 11〉：SDLBA 指第一個 destination block，後續來源按 descriptor 順序連接；它不會為每個 source range 重新歸零。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

SDLBA 指第一個 destination block，後續來源按 descriptor 順序連接；它不會為每個 source range 重新歸零。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SDLBA]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SDLBA` | 範圍起始 LBA；SDLBA 選 Copy 目的，DSLBA 是 Get LBA Status descriptor 的起點。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. SDLBA 指第一個 destination block，後續來源按 descriptor 順序連接；它不會為每個 source range 重新歸零。
3. 先計算展開後的目的區間，再檢查格式、長度限制、重疊與 atomicity。Copy 可少用 host 資料傳輸，但不是無條件的 transaction。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 34 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | SDLBA 指第一個 destination block，後續來源按 descriptor 順序連接；它不會為每個 source range 重新歸零。 |
| 邊界 | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

**說明性範例。** 兩個 source descriptors 的 NLB 都是 3，SDLBA=100：第一段寫 100..103、第二段寫 104..107，共 8 blocks。若 DW0=1，不能據此保證第二段或更後面完全未修改。

**常見誤解。** FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SDLBA

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 34, 文件頁 30, PDF 頁 30

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 35: Copy – Command Dword 12</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-035-CLAIM figure-table:NVMCS13-NVM-FIG-035 -->

**SPEC。** Figure 35〈Copy – Command Dword 12〉：Copy 在同一 CDW12 分開讀端／寫端 PI、descriptor format 與 0-based range count。STCRS 的正確能力定義在 Figure 127；本圖指 Figure 115 的文字引用錯置。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Copy 在同一 CDW12 分開讀端／寫端 PI、descriptor format 與 0-based range count。STCRS 的正確能力定義在 Figure 127；本圖指 Figure 115 的文字引用錯置。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PRINFOW]
          ↓
[擷取欄位: PRINFOR] → [套用編碼: STCR]
                                      ↓
[驗證證據: STCW]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PRINFOW` | PRACT 與 PRCHK 的組合欄位；Copy 的 R／W 版本分別控制讀端／寫端。 |
| `PRINFOR` | PRACT 與 PRCHK 的組合欄位；Copy 的 R／W 版本分別控制讀端／寫端。 |
| `STCR` | Copy 讀端／寫端的 Storage Tag Check；依兩側 STS 與 PI 處理分支判斷有效性。 |
| `STCW` | Copy 讀端／寫端的 Storage Tag Check；依兩側 STS 與 PI 處理分支判斷有效性。 |
| `DESFMT` | Copy Source Range Entry 格式 selector；同時影響 descriptor 大小、來源 NSID 與 PI tag layout。 |
| `NR` | Range count 的 0-based 欄位；實際 descriptors 數為 NR+1。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Copy 在同一 CDW12 分開讀端／寫端 PI、descriptor format 與 0-based range count。STCRS 的正確能力定義在 Figure 127；本圖指 Figure 115 的文字引用錯置。
3. 先計算展開後的目的區間，再檢查格式、長度限制、重疊與 atomicity。Copy 可少用 host 資料傳輸，但不是無條件的 transaction。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 35 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Copy 在同一 CDW12 分開讀端／寫端 PI、descriptor format 與 0-based range count。STCRS 的正確能力定義在 Figure 127；本圖指 Figure 115 的文字引用錯置。 |
| 邊界 | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

**說明性範例。** 兩個 source descriptors 的 NLB 都是 3，SDLBA=100：第一段寫 100..103、第二段寫 104..107，共 8 blocks。若 DW0=1，不能據此保證第二段或更後面完全未修改。

**常見誤解。** FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** PRINFOW, PRINFOR, STCR, STCW, DESFMT, NR

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 35, 文件頁 30-31, PDF 頁 30-31

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 36: Copy – Command Dword 13</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-036-CLAIM figure-table:NVMCS13-NVM-FIG-036 -->

**SPEC。** Figure 36〈Copy – Command Dword 13〉：CDW13 high16 保存 Directive Specific，low16 依 CETYPE 保存 CEV；Directive 與 command extension 是獨立欄位。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW13 high16 保存 Directive Specific，low16 依 CETYPE 保存 CEV；Directive 與 command extension 是獨立欄位。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DSPEC]
          ↓
[擷取欄位: CEV] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DSPEC` | Directive Type／Specific 欄位；Directive 類型決定 Specific 的內容與 placement 效果。 |
| `CEV` | Command Extension Type／Value；Type 先決定 Value 的用途，不能固定當作 DSM hints。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW13 high16 保存 Directive Specific，low16 依 CETYPE 保存 CEV；Directive 與 command extension 是獨立欄位。
3. 先計算展開後的目的區間，再檢查格式、長度限制、重疊與 atomicity。Copy 可少用 host 資料傳輸，但不是無條件的 transaction。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 36 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW13 high16 保存 Directive Specific，low16 依 CETYPE 保存 CEV；Directive 與 command extension 是獨立欄位。 |
| 邊界 | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

**說明性範例。** 兩個 source descriptors 的 NLB 都是 3，SDLBA=100：第一段寫 100..103、第二段寫 104..107，共 8 blocks。若 DW0=1，不能據此保證第二段或更後面完全未修改。

**常見誤解。** FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DSPEC, CEV

**來源 keyword 索引：** shall, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 36, 文件頁 31, PDF 頁 31

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 37: Copy – Command Dword 14</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-037-CLAIM figure-table:NVMCS13-NVM-FIG-037 -->

**SPEC。** Figure 37〈Copy – Command Dword 14〉：CDW14 提供寫入 tags 的低 32 bits；依 STS 將 space 分割，不能把高位 Storage Tag 全部丟棄。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW14 提供寫入 tags 的低 32 bits；依 STS 將 space 分割，不能把高位 Storage Tag 全部丟棄。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBTL]
          ↓
[擷取欄位: LBST] → [套用編碼: ILBRT]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBTL` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `LBST` | Logical Block Storage Tag／Expected Logical Block Storage Tag；寬度由 STS 決定。 |
| `ILBRT` | Initial Logical Block Reference Tag／expected 初值；Type 1／2 依 block 遞增並在欄位寬度處回捲。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW14 提供寫入 tags 的低 32 bits；依 STS 將 space 分割，不能把高位 Storage Tag 全部丟棄。
3. 先計算展開後的目的區間，再檢查格式、長度限制、重疊與 atomicity。Copy 可少用 host 資料傳輸，但不是無條件的 transaction。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 37 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW14 提供寫入 tags 的低 32 bits；依 STS 將 space 分割，不能把高位 Storage Tag 全部丟棄。 |
| 邊界 | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

**說明性範例。** 兩個 source descriptors 的 NLB 都是 3，SDLBA=100：第一段寫 100..103、第二段寫 104..107，共 8 blocks。若 DW0=1，不能據此保證第二段或更後面完全未修改。

**常見誤解。** FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LBTL, LBST, ILBRT

**來源 keyword 索引：** shall, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 37, 文件頁 31, PDF 頁 31

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 38: Copy – Command Dword 15</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-038-CLAIM figure-table:NVMCS13-NVM-FIG-038 -->

**SPEC。** Figure 38〈Copy – Command Dword 15〉：Application Tag mask 與 tag 分別在 CDW15 high16／low16；Copy 使用於寫入目的端，來源端有獨立 expected 欄位。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Application Tag mask 與 tag 分別在 CDW15 high16／low16；Copy 使用於寫入目的端，來源端有獨立 expected 欄位。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBATM]
          ↓
[擷取欄位: LBAT] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBATM` | Tag comparison mask；bit=0 排除比較，Storage mask 額外受支援與對齊限制。 |
| `LBAT` | Logical Block Application Tag／expected tag；16-bit，checking 與 mask 及停用值規則共同決定。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Application Tag mask 與 tag 分別在 CDW15 high16／low16；Copy 使用於寫入目的端，來源端有獨立 expected 欄位。
3. 先計算展開後的目的區間，再檢查格式、長度限制、重疊與 atomicity。Copy 可少用 host 資料傳輸，但不是無條件的 transaction。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 38 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Application Tag mask 與 tag 分別在 CDW15 high16／low16；Copy 使用於寫入目的端，來源端有獨立 expected 欄位。 |
| 邊界 | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

**說明性範例。** 兩個 source descriptors 的 NLB 都是 3，SDLBA=100：第一段寫 100..103、第二段寫 104..107，共 8 blocks。若 DW0=1，不能據此保證第二段或更後面完全未修改。

**常見誤解。** FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LBATM, LBAT

**來源 keyword 索引：** shall, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 38, 文件頁 32, PDF 頁 32

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 39: Copy – Copy Descriptor Formats</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-039-CLAIM figure-table:NVMCS13-NVM-FIG-039 -->

**SPEC。** Figure 39〈Copy – Copy Descriptor Formats〉：0h/2h 搭配 8-byte PI、1h/3h 搭配 16-byte PI；2h/3h 有 SNSID。4h 指向另一 command set 的 Memory Copy 定義，這份 NVM 文件沒有其完整 descriptor layout。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

0h/2h 搭配 8-byte PI、1h/3h 搭配 16-byte PI；2h/3h 有 SNSID。4h 指向另一 command set 的 Memory Copy 定義，這份 NVM 文件沒有其完整 descriptor layout。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DESFMT]
          ↓
[擷取欄位: SNSID] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DESFMT` | Copy Source Range Entry 格式 selector；同時影響 descriptor 大小、來源 NSID 與 PI tag layout。 |
| `SNSID` | Namespace 識別碼；SNSID 選 Copy 來源，ENSID 選匯出 namespace，合法值受個別命令約束。 |
| `相關欄位` | PI size — 0h/2h 搭配 8-byte PI、1h/3h 搭配 16-byte PI；2h/3h 有 SNSID。4h 指向另一 command set 的 Memory Copy 定義，這份 NVM 文件沒有其完整 descriptor layout。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 0h/2h 搭配 8-byte PI、1h/3h 搭配 16-byte PI；2h/3h 有 SNSID。4h 指向另一 command set 的 Memory Copy 定義，這份 NVM 文件沒有其完整 descriptor layout。
3. 先計算展開後的目的區間，再檢查格式、長度限制、重疊與 atomicity。Copy 可少用 host 資料傳輸，但不是無條件的 transaction。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 39 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 0h/2h 搭配 8-byte PI、1h/3h 搭配 16-byte PI；2h/3h 有 SNSID。4h 指向另一 command set 的 Memory Copy 定義，這份 NVM 文件沒有其完整 descriptor layout。 |
| 邊界 | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

**說明性範例。** 兩個 source descriptors 的 NLB 都是 3，SDLBA=100：第一段寫 100..103、第二段寫 104..107，共 8 blocks。若 DW0=1，不能據此保證第二段或更後面完全未修改。

**常見誤解。** FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DESFMT, SNSID, PI size

**來源 keyword 索引：** shall, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 39, 文件頁 32, PDF 頁 32

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 40: Copy – Source Range Entries Copy Descriptor Format 0h and Format 2h</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-040-CLAIM figure-table:NVMCS13-NVM-FIG-040 -->

**SPEC。** Figure 40〈Copy – Source Range Entries Copy Descriptor Format 0h and Format 2h〉：0h/2h 每個 source entry 32 bytes；0h 的 SNSID／FCO 位置 reserved，2h 可使用。NLB 先加一，再累加至 destination length。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

0h/2h 每個 source entry 32 bytes；0h 的 SNSID／FCO 位置 reserved，2h 可使用。NLB 先加一，再累加至 destination length。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SNSID]
          ↓
[擷取欄位: SLBA] → [套用編碼: NLB]
                                      ↓
[驗證證據: ELBT]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SNSID` | Namespace 識別碼；SNSID 選 Copy 來源，ENSID 選匯出 namespace，合法值受個別命令約束。 |
| `SLBA` | 範圍起始 LBA；SDLBA 選 Copy 目的，DSLBA 是 Get LBA Status descriptor 的起點。 |
| `NLB` | Number of Logical Blocks；本報告命令／status descriptors 的該欄為 0-based。DSM 的 LLB 另為1-based。 |
| `ELBT` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `ELBAT` | Logical Block Application Tag／expected tag；16-bit，checking 與 mask 及停用值規則共同決定。 |
| `ELBATM` | Tag comparison mask；bit=0 排除比較，Storage mask 額外受支援與對齊限制。 |
| `FCO` | Fast Copy Only；要求適用來源以 fast copy 方法執行。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 0h/2h 每個 source entry 32 bytes；0h 的 SNSID／FCO 位置 reserved，2h 可使用。NLB 先加一，再累加至 destination length。
3. 先計算展開後的目的區間，再檢查格式、長度限制、重疊與 atomicity。Copy 可少用 host 資料傳輸，但不是無條件的 transaction。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 40 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 0h/2h 每個 source entry 32 bytes；0h 的 SNSID／FCO 位置 reserved，2h 可使用。NLB 先加一，再累加至 destination length。 |
| 邊界 | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

**說明性範例。** 兩個 source descriptors 的 NLB 都是 3，SDLBA=100：第一段寫 100..103、第二段寫 104..107，共 8 blocks。若 DW0=1，不能據此保證第二段或更後面完全未修改。

**常見誤解。** FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SNSID, SLBA, NLB, ELBT, ELBAT, ELBATM, FCO

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 40, 文件頁 33-34, PDF 頁 33-34

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 41: Copy – Source Range Entries Copy Descriptor Format 1h and Format 3h</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-041-CLAIM figure-table:NVMCS13-NVM-FIG-041 -->

**SPEC。** Figure 41〈Copy – Source Range Entries Copy Descriptor Format 1h and Format 3h〉：1h/3h 每個 source entry 40 bytes，以較大的 tags 支援 16-byte PI；3h 帶 SNSID／FCO，不能用 32-byte stride 解析。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

1h/3h 每個 source entry 40 bytes，以較大的 tags 支援 16-byte PI；3h 帶 SNSID／FCO，不能用 32-byte stride 解析。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SNSID]
          ↓
[擷取欄位: SLBA] → [套用編碼: NLB]
                                      ↓
[驗證證據: ELBTU]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SNSID` | Namespace 識別碼；SNSID 選 Copy 來源，ENSID 選匯出 namespace，合法值受個別命令約束。 |
| `SLBA` | 範圍起始 LBA；SDLBA 選 Copy 目的，DSLBA 是 Get LBA Status descriptor 的起點。 |
| `NLB` | Number of Logical Blocks；本報告命令／status descriptors 的該欄為 0-based。DSM 的 LLB 另為1-based。 |
| `ELBTU` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `ELBTL` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `FCO` | Fast Copy Only；要求適用來源以 fast copy 方法執行。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 1h/3h 每個 source entry 40 bytes，以較大的 tags 支援 16-byte PI；3h 帶 SNSID／FCO，不能用 32-byte stride 解析。
3. 先計算展開後的目的區間，再檢查格式、長度限制、重疊與 atomicity。Copy 可少用 host 資料傳輸，但不是無條件的 transaction。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 41 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 1h/3h 每個 source entry 40 bytes，以較大的 tags 支援 16-byte PI；3h 帶 SNSID／FCO，不能用 32-byte stride 解析。 |
| 邊界 | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

**說明性範例。** 兩個 source descriptors 的 NLB 都是 3，SDLBA=100：第一段寫 100..103、第二段寫 104..107，共 8 blocks。若 DW0=1，不能據此保證第二段或更後面完全未修改。

**常見誤解。** FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SNSID, SLBA, NLB, ELBTU, ELBTL, FCO

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 41, 文件頁 35-36, PDF 頁 35-36

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 42: Source LBA and Destination LBA Relationship Example</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-042-CLAIM figure-table:NVMCS13-NVM-FIG-042 -->

**SPEC。** Figure 42〈Source LBA and Destination LBA Relationship Example〉：依 source descriptor 順序把各段長度相加，產生連續 destination；圖中的加總是 block 數，不能直接累加 raw NLB 而漏掉每段的一。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

依 source descriptor 順序把各段長度相加，產生連續 destination；圖中的加總是 block 數，不能直接累加 raw NLB 而漏掉每段的一。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SDLBA]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SDLBA` | 範圍起始 LBA；SDLBA 選 Copy 目的，DSLBA 是 Get LBA Status descriptor 的起點。 |
| `相關欄位` | Source ranges, Destination offsets — 依 source descriptor 順序把各段長度相加，產生連續 destination；圖中的加總是 block 數，不能直接累加 raw NLB 而漏掉每段的一。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 依 source descriptor 順序把各段長度相加，產生連續 destination；圖中的加總是 block 數，不能直接累加 raw NLB 而漏掉每段的一。
3. 先計算展開後的目的區間，再檢查格式、長度限制、重疊與 atomicity。Copy 可少用 host 資料傳輸，但不是無條件的 transaction。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 42 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 依 source descriptor 順序把各段長度相加，產生連續 destination；圖中的加總是 block 數，不能直接累加 raw NLB 而漏掉每段的一。 |
| 邊界 | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

**說明性範例。** 兩個 source descriptors 的 NLB 都是 3，SDLBA=100：第一段寫 100..103、第二段寫 104..107，共 8 blocks。若 DW0=1，不能據此保證第二段或更後面完全未修改。

**常見誤解。** FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Source ranges, SDLBA, Destination offsets

**來源 keyword 索引：** shall, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 42, 文件頁 38, PDF 頁 38

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 43: Copy – Command Specific Status Values</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-043-CLAIM figure-table:NVMCS13-NVM-FIG-043 -->

**SPEC。** Figure 43〈Copy – Command Specific Status Values〉：Copy 錯誤要合看 CQE DW0 的最低失敗 source index；後續 entries 可能已處理，不能假設回滾。FCO 失敗再依 DNR 判斷重試。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Copy 錯誤要合看 CQE DW0 的最低失敗 source index；後續 entries 可能已處理，不能假設回滾。FCO 失敗再依 DNR 判斷重試。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Fast Copy Not Possible, Overlapping I/O Range, Insufficient Resources — Copy 錯誤要合看 CQE DW0 的最低失敗 source index；後續 entries 可能已處理，不能假設回滾。FCO 失敗再依 DNR 判斷重試。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Copy 錯誤要合看 CQE DW0 的最低失敗 source index；後續 entries 可能已處理，不能假設回滾。FCO 失敗再依 DNR 判斷重試。
3. 先計算展開後的目的區間，再檢查格式、長度限制、重疊與 atomicity。Copy 可少用 host 資料傳輸，但不是無條件的 transaction。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 43 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Copy 錯誤要合看 CQE DW0 的最低失敗 source index；後續 entries 可能已處理，不能假設回滾。FCO 失敗再依 DNR 判斷重試。 |
| 邊界 | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

**說明性範例。** 兩個 source descriptors 的 NLB 都是 3，SDLBA=100：第一段寫 100..103、第二段寫 104..107，共 8 blocks。若 DW0=1，不能據此保證第二段或更後面完全未修改。

**常見誤解。** FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Fast Copy Not Possible, Overlapping I/O Range, Insufficient Resources

**來源 keyword 索引：** shall not, shall, should not, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 43, 文件頁 43-44, PDF 頁 43-44

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 44: Dataset Management – Data Pointer</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-044-CLAIM figure-table:NVMCS13-NVM-FIG-044 -->

**SPEC。** Figure 44〈Dataset Management – Data Pointer〉：DPTR 指向 descriptors，而不是待複製或 deallocate 的 user data；buffer 長度需由 descriptor size 與解碼後 range count 計算。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

DPTR 指向 descriptors，而不是待複製或 deallocate 的 user data；buffer 長度需由 descriptor size 與解碼後 range count 計算。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

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
| `DPTR` | 命令 data pointer；Read 是目的、Write 是來源、Copy／DSM 指向 descriptors。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. DPTR 指向 descriptors，而不是待複製或 deallocate 的 user data；buffer 長度需由 descriptor size 與解碼後 range count 計算。
3. 先計算每個 block 是否同時通過三種 limit，再套用 NVMDSMSV。範圍與 hints 的合法性、處理義務以及實際媒體動作分開判斷。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 44 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | DPTR 指向 descriptors，而不是待複製或 deallocate 的 user data；buffer 長度需由 descriptor size 與解碼後 range count 計算。 |
| 邊界 | 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。 |

**說明性範例。** DMRL=2、DMSL=1048，range 0 有 1024 blocks、range 1 有 512，且 DMRSL 不限制：variant=1 時前段與後段前 24 blocks 符合 limits。這不等於保證 1048 blocks 都已釋放。

**常見誤解。** 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DPTR

**來源 keyword 索引：** should not, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, Figure 44, 文件頁 44, PDF 頁 44

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 45: Dataset Management – Command Dword 10</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-045-CLAIM figure-table:NVMCS13-NVM-FIG-045 -->

**SPEC。** Figure 45〈Dataset Management – Command Dword 10〉：CDW10 low8 的 NR 是 0-based，最大 FFh 表示 256 個 ranges；這與 DMRL 的 1-based limit 不同。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW10 low8 的 NR 是 0-based，最大 FFh 表示 256 個 ranges；這與 DMRL 的 1-based limit 不同。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NR]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NR` | Range count 的 0-based 欄位；實際 descriptors 數為 NR+1。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW10 low8 的 NR 是 0-based，最大 FFh 表示 256 個 ranges；這與 DMRL 的 1-based limit 不同。
3. 先計算每個 block 是否同時通過三種 limit，再套用 NVMDSMSV。範圍與 hints 的合法性、處理義務以及實際媒體動作分開判斷。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 45 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW10 low8 的 NR 是 0-based，最大 FFh 表示 256 個 ranges；這與 DMRL 的 1-based limit 不同。 |
| 邊界 | 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。 |

**說明性範例。** DMRL=2、DMSL=1048，range 0 有 1024 blocks、range 1 有 512，且 DMRSL 不限制：variant=1 時前段與後段前 24 blocks 符合 limits。這不等於保證 1048 blocks 都已釋放。

**常見誤解。** 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NR

**來源 keyword 索引：** should not, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, Figure 45, 文件頁 44, PDF 頁 44

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 46: Dataset Management – Command Dword 11</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-046-CLAIM figure-table:NVMCS13-NVM-FIG-046 -->

**SPEC。** Figure 46〈Dataset Management – Command Dword 11〉：CDW11 bits2/1/0 分別是 deallocate、integral write、integral read hints；處理 AD 不代表一定釋放。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW11 bits2/1/0 分別是 deallocate、integral write、integral read hints；處理 AD 不代表一定釋放。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | AD, IDW, IDR — CDW11 bits2/1/0 分別是 deallocate、integral write、integral read hints；處理 AD 不代表一定釋放。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW11 bits2/1/0 分別是 deallocate、integral write、integral read hints；處理 AD 不代表一定釋放。
3. 先計算每個 block 是否同時通過三種 limit，再套用 NVMDSMSV。範圍與 hints 的合法性、處理義務以及實際媒體動作分開判斷。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 46 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW11 bits2/1/0 分別是 deallocate、integral write、integral read hints；處理 AD 不代表一定釋放。 |
| 邊界 | 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。 |

**說明性範例。** DMRL=2、DMSL=1048，range 0 有 1024 blocks、range 1 有 512，且 DMRSL 不限制：variant=1 時前段與後段前 24 blocks 符合 limits。這不等於保證 1048 blocks 都已釋放。

**常見誤解。** 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** AD, IDW, IDR

**來源 keyword 索引：** should not, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, Figure 46, 文件頁 44-45, PDF 頁 44-45

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 47: Dataset Management – Range Definition</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-047-CLAIM figure-table:NVMCS13-NVM-FIG-047 -->

**SPEC。** Figure 47〈Dataset Management – Range Definition〉：每筆 16 bytes：CATTR、1-based LLB、64-bit SLBA；256 筆需要 4096 bytes。不要沿用 NLB 的加一解碼。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

每筆 16 bytes：CATTR、1-based LLB、64-bit SLBA；256 筆需要 4096 bytes。不要沿用 NLB 的加一解碼。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LLB]
          ↓
[擷取欄位: SLBA] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LLB` | DSM 的 Length in Logical Blocks；1-based，與 Read／Write 的 NLB 編碼不同。 |
| `SLBA` | 範圍起始 LBA；SDLBA 選 Copy 目的，DSLBA 是 Get LBA Status descriptor 的起點。 |
| `相關欄位` | CATTR — 每筆 16 bytes：CATTR、1-based LLB、64-bit SLBA；256 筆需要 4096 bytes。不要沿用 NLB 的加一解碼。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 每筆 16 bytes：CATTR、1-based LLB、64-bit SLBA；256 筆需要 4096 bytes。不要沿用 NLB 的加一解碼。
3. 先計算每個 block 是否同時通過三種 limit，再套用 NVMDSMSV。範圍與 hints 的合法性、處理義務以及實際媒體動作分開判斷。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 47 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 每筆 16 bytes：CATTR、1-based LLB、64-bit SLBA；256 筆需要 4096 bytes。不要沿用 NLB 的加一解碼。 |
| 邊界 | 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。 |

**說明性範例。** DMRL=2、DMSL=1048，range 0 有 1024 blocks、range 1 有 512，且 DMRSL 不限制：variant=1 時前段與後段前 24 blocks 符合 limits。這不等於保證 1048 blocks 都已釋放。

**常見誤解。** 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** CATTR, LLB, SLBA

**來源 keyword 索引：** should, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, Figure 47, 文件頁 45, PDF 頁 45

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 48: Dataset Management – Context Attributes</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-048-CLAIM figure-table:NVMCS13-NVM-FIG-048 -->

**SPEC。** Figure 48〈Dataset Management – Context Attributes〉：這些 context attributes 描述預期 workload；即使 host hints 不精確，controller 仍須維持資料完整性。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

這些 context attributes 描述預期 workload；即使 host hints 不精確，controller 仍須維持資料完整性。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | CASZE, WPREP, SWR, SRR, AL, AF — 這些 context attributes 描述預期 workload；即使 host hints 不精確，controller 仍須維持資料完整性。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 這些 context attributes 描述預期 workload；即使 host hints 不精確，controller 仍須維持資料完整性。
3. 先計算每個 block 是否同時通過三種 limit，再套用 NVMDSMSV。範圍與 hints 的合法性、處理義務以及實際媒體動作分開判斷。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 48 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 這些 context attributes 描述預期 workload；即使 host hints 不精確，controller 仍須維持資料完整性。 |
| 邊界 | 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。 |

**說明性範例。** DMRL=2、DMSL=1048，range 0 有 1024 blocks、range 1 有 512，且 DMRSL 不限制：variant=1 時前段與後段前 24 blocks 符合 limits。這不等於保證 1048 blocks 都已釋放。

**常見誤解。** 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** CASZE, WPREP, SWR, SRR, AL, AF

**來源 keyword 索引：** should, optional, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, Figure 48, 文件頁 47, PDF 頁 47

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 49: Dataset Management – Command Specific Status Values</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-049-CLAIM figure-table:NVMCS13-NVM-FIG-049 -->

**SPEC。** Figure 49〈Dataset Management – Command Specific Status Values〉：DSM 的 size-limit error 受 NVMDSMSV 影響；variant=1 不得因 processing limits 回報該錯誤。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

DSM 的 size-limit error 受 NVMDSMSV 影響；variant=1 不得因 processing limits 回報該錯誤。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Conflicting Attributes, Command Size Limit Exceeded — DSM 的 size-limit error 受 NVMDSMSV 影響；variant=1 不得因 processing limits 回報該錯誤。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. DSM 的 size-limit error 受 NVMDSMSV 影響；variant=1 不得因 processing limits 回報該錯誤。
3. 先計算每個 block 是否同時通過三種 limit，再套用 NVMDSMSV。範圍與 hints 的合法性、處理義務以及實際媒體動作分開判斷。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 49 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | DSM 的 size-limit error 受 NVMDSMSV 影響；variant=1 不得因 processing limits 回報該錯誤。 |
| 邊界 | 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。 |

**說明性範例。** DMRL=2、DMSL=1048，range 0 有 1024 blocks、range 1 有 512，且 DMRSL 不限制：variant=1 時前段與後段前 24 blocks 符合 limits。這不等於保證 1048 blocks 都已釋放。

**常見誤解。** 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Conflicting Attributes, Command Size Limit Exceeded

**來源 keyword 索引：** shall not, shall, may, optional

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, Figure 49, 文件頁 48, PDF 頁 48

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 50: Read – Metadata Pointer</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-050-CLAIM figure-table:NVMCS13-NVM-FIG-050 -->

**SPEC。** Figure 50〈Read – Metadata Pointer〉：MPTR 只在所選格式使用 separate metadata 時提供 metadata 位置；先核對 PSDT／metadata 格式，不能把它當成 user-data buffer。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

MPTR 只在所選格式使用 separate metadata 時提供 metadata 位置；先核對 PSDT／metadata 格式，不能把它當成 user-data buffer。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MPTR]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MPTR` | Separate metadata 的指標；metadata placement 由 namespace format 與命令欄位決定。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. MPTR 只在所選格式使用 separate metadata 時提供 metadata 位置；先核對 PSDT／metadata 格式，不能把它當成 user-data buffer。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 50 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | MPTR 只在所選格式使用 separate metadata 時提供 metadata 位置；先核對 PSDT／metadata 格式，不能把它當成 user-data buffer。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** MPTR

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 50, 文件頁 49, PDF 頁 49

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 51: Read – Data Pointer</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-051-CLAIM figure-table:NVMCS13-NVM-FIG-051 -->

**SPEC。** Figure 51〈Read – Data Pointer〉：DPTR 是 controller 回傳資料的 host 目的位置；Read 回 data，Get LBA Status 回 descriptor list，兩者不可共用 payload parser。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

DPTR 是 controller 回傳資料的 host 目的位置；Read 回 data，Get LBA Status 回 descriptor list，兩者不可共用 payload parser。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

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
| `DPTR` | 命令 data pointer；Read 是目的、Write 是來源、Copy／DSM 指向 descriptors。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. DPTR 是 controller 回傳資料的 host 目的位置；Read 回 data，Get LBA Status 回 descriptor list，兩者不可共用 payload parser。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 51 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | DPTR 是 controller 回傳資料的 host 目的位置；Read 回 data，Get LBA Status 回 descriptor list，兩者不可共用 payload parser。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DPTR

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 51, 文件頁 49, PDF 頁 49

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 52: Read – Command Dword 2 and Dword 3</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-052-CLAIM figure-table:NVMCS13-NVM-FIG-052 -->

**SPEC。** Figure 52〈Read – Command Dword 2 and Dword 3〉：CDW2／3 的 upper tags 要和 CDW14 lower tags 合併，再依 PI 格式與 STS 拆成 expected storage／reference；unused bits 依格式忽略。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW2／3 的 upper tags 要和 CDW14 lower tags 合併，再依 PI 格式與 STS 拆成 expected storage／reference；unused bits 依格式忽略。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ELBTU]
          ↓
[擷取欄位: ELBTL] → [套用編碼: ELBST]
                                      ↓
[驗證證據: EILBRT]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ELBTU` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `ELBTL` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `ELBST` | Logical Block Storage Tag／Expected Logical Block Storage Tag；寬度由 STS 決定。 |
| `EILBRT` | Initial Logical Block Reference Tag／expected 初值；Type 1／2 依 block 遞增並在欄位寬度處回捲。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW2／3 的 upper tags 要和 CDW14 lower tags 合併，再依 PI 格式與 STS 拆成 expected storage／reference；unused bits 依格式忽略。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 52 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW2／3 的 upper tags 要和 CDW14 lower tags 合併，再依 PI 格式與 STS 拆成 expected storage／reference；unused bits 依格式忽略。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** ELBTU, ELBTL, ELBST, EILBRT

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 52, 文件頁 49, PDF 頁 49

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 53: Read – Command Dword 10 and Command Dword 11</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-053-CLAIM figure-table:NVMCS13-NVM-FIG-053 -->

**SPEC。** Figure 53〈Read – Command Dword 10 and Command Dword 11〉：64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SLBA]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SLBA` | 範圍起始 LBA；SDLBA 選 Copy 目的，DSLBA 是 Get LBA Status descriptor 的起點。 |
| `相關欄位` | CDW10, CDW11 — 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 53 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SLBA, CDW10, CDW11

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 53, 文件頁 49, PDF 頁 49

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 54: Read – Command Dword 12</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-054-CLAIM figure-table:NVMCS13-NVM-FIG-054 -->

**SPEC。** Figure 54〈Read – Command Dword 12〉：CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LR]
          ↓
[擷取欄位: FUA] → [套用編碼: PRINFO]
                                      ↓
[驗證證據: STC]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LR` | Limited Retry；指定受 Error Recovery policy 約束的重試行為。 |
| `FUA` | Force Unit Access；要求 nonvolatile-media 語意，不自動建立其他命令的順序。 |
| `PRINFO` | PRACT 與 PRCHK 的組合欄位；Copy 的 R／W 版本分別控制讀端／寫端。 |
| `STC` | Storage Tag Check；獨立於三位元 PRCHK，STS=0 時忽略。 |
| `CETYPE` | Command Extension Type／Value；Type 先決定 Value 的用途，不能固定當作 DSM hints。 |
| `NLB` | Number of Logical Blocks；本報告命令／status descriptors 的該欄為 0-based。DSM 的 LLB 另為1-based。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 54 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LR, FUA, PRINFO, STC, CETYPE, NLB

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 54, 文件頁 49, PDF 頁 49

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 55: Read – Command Dword 13 if CETYPE is cleared to 0h</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-055-CLAIM figure-table:NVMCS13-NVM-FIG-055 -->

**SPEC。** Figure 55〈Read – Command Dword 13 if CETYPE is cleared to 0h〉：Read 在 CETYPE=0 才用 CDW13 low8 提供 DSM hints；one-time／speculative read 是 access-frequency hints，不保證 controller 一定改變 cache 策略。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Read 在 CETYPE=0 才用 CDW13 low8 提供 DSM hints；one-time／speculative read 是 access-frequency hints，不保證 controller 一定改變 cache 策略。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | DSM, INCPRS, SEQREQ, AL, AF — Read 在 CETYPE=0 才用 CDW13 low8 提供 DSM hints；one-time／speculative read 是 access-frequency hints，不保證 controller 一定改變 cache 策略。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Read 在 CETYPE=0 才用 CDW13 low8 提供 DSM hints；one-time／speculative read 是 access-frequency hints，不保證 controller 一定改變 cache 策略。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 55 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Read 在 CETYPE=0 才用 CDW13 low8 提供 DSM hints；one-time／speculative read 是 access-frequency hints，不保證 controller 一定改變 cache 策略。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DSM, INCPRS, SEQREQ, AL, AF

**來源 keyword 索引：** reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 55, 文件頁 50, PDF 頁 50

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 56: Read - Command Dword 13 if CETYPE is non-zero</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-056-CLAIM figure-table:NVMCS13-NVM-FIG-056 -->

**SPEC。** Figure 56〈Read - Command Dword 13 if CETYPE is non-zero〉：CETYPE 非零時 CDW13 low16 解讀為 CEV；CETYPE=0 的 layout 另有定義或 reserved，不能同時塞 DSM hints。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CETYPE 非零時 CDW13 low16 解讀為 CEV；CETYPE=0 的 layout 另有定義或 reserved，不能同時塞 DSM hints。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CETYPE]
          ↓
[擷取欄位: CEV] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CETYPE` | Command Extension Type／Value；Type 先決定 Value 的用途，不能固定當作 DSM hints。 |
| `CEV` | Command Extension Type／Value；Type 先決定 Value 的用途，不能固定當作 DSM hints。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CETYPE 非零時 CDW13 low16 解讀為 CEV；CETYPE=0 的 layout 另有定義或 reserved，不能同時塞 DSM hints。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 56 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CETYPE 非零時 CDW13 low16 解讀為 CEV；CETYPE=0 的 layout 另有定義或 reserved，不能同時塞 DSM hints。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** CETYPE, CEV

**來源 keyword 索引：** reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 56, 文件頁 50, PDF 頁 50

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 57: Read – Command Dword 14</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-057-CLAIM figure-table:NVMCS13-NVM-FIG-057 -->

**SPEC。** Figure 57〈Read – Command Dword 14〉：CDW14 是 expected-tag 空間低 32 bits；它未必全是 Reference Tag，STS 可能占用其中高 bits。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW14 是 expected-tag 空間低 32 bits；它未必全是 Reference Tag，STS 可能占用其中高 bits。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ELBTL]
          ↓
[擷取欄位: ELBTU] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ELBTL` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `ELBTU` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW14 是 expected-tag 空間低 32 bits；它未必全是 Reference Tag，STS 可能占用其中高 bits。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 57 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW14 是 expected-tag 空間低 32 bits；它未必全是 Reference Tag，STS 可能占用其中高 bits。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** ELBTL, ELBTU

**來源 keyword 索引：** reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 57, 文件頁 50, PDF 頁 50

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 58: Read – Command Dword 15</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-058-CLAIM figure-table:NVMCS13-NVM-FIG-058 -->

**SPEC。** Figure 58〈Read – Command Dword 15〉：CDW15 high16 是 Application Tag mask，low16 是 expected tag；mask bit=0 表示不比較該位，不是要求 tag bit=0。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW15 high16 是 Application Tag mask，low16 是 expected tag；mask bit=0 表示不比較該位，不是要求 tag bit=0。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ELBATM]
          ↓
[擷取欄位: ELBAT] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ELBATM` | Tag comparison mask；bit=0 排除比較，Storage mask 額外受支援與對齊限制。 |
| `ELBAT` | Logical Block Application Tag／expected tag；16-bit，checking 與 mask 及停用值規則共同決定。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW15 high16 是 Application Tag mask，low16 是 expected tag；mask bit=0 表示不比較該位，不是要求 tag bit=0。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 58 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW15 high16 是 Application Tag mask，low16 是 expected tag；mask bit=0 表示不比較該位，不是要求 tag bit=0。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** ELBATM, ELBAT

**來源 keyword 索引：** shall, may, optional

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 58, 文件頁 51, PDF 頁 51

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 59: Read – Command Specific Status Values</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-059-CLAIM figure-table:NVMCS13-NVM-FIG-059 -->

**SPEC。** Figure 59〈Read – Command Specific Status Values〉：把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SCT]
          ↓
[擷取欄位: SC] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SCT` | Status Code Type 與 Status Code；兩欄共同識別錯誤，單看 SC 可能誤判。 |
| `SC` | Status Code Type 與 Status Code；兩欄共同識別錯誤，單看 SC 可能誤判。 |
| `相關欄位` | Command-specific error — 把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 59 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SCT, SC, Command-specific error

**來源 keyword 索引：** shall, may, optional

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 59, 文件頁 51, PDF 頁 51

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 60: Verify – Command Dword 2 and Dword 3</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-060-CLAIM figure-table:NVMCS13-NVM-FIG-060 -->

**SPEC。** Figure 60〈Verify – Command Dword 2 and Dword 3〉：CDW2／3 的 upper tags 要和 CDW14 lower tags 合併，再依 PI 格式與 STS 拆成 expected storage／reference；unused bits 依格式忽略。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW2／3 的 upper tags 要和 CDW14 lower tags 合併，再依 PI 格式與 STS 拆成 expected storage／reference；unused bits 依格式忽略。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ELBTU]
          ↓
[擷取欄位: ELBTL] → [套用編碼: ELBST]
                                      ↓
[驗證證據: EILBRT]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ELBTU` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `ELBTL` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `ELBST` | Logical Block Storage Tag／Expected Logical Block Storage Tag；寬度由 STS 決定。 |
| `EILBRT` | Initial Logical Block Reference Tag／expected 初值；Type 1／2 依 block 遞增並在欄位寬度處回捲。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW2／3 的 upper tags 要和 CDW14 lower tags 合併，再依 PI 格式與 STS 拆成 expected storage／reference；unused bits 依格式忽略。
3. 比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 60 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW2／3 的 upper tags 要和 CDW14 lower tags 合併，再依 PI 格式與 STS 拆成 expected storage／reference；unused bits 依格式忽略。 |
| 邊界 | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

**說明性範例。** 要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。

**常見誤解。** Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** ELBTU, ELBTL, ELBST, EILBRT

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 60, 文件頁 52, PDF 頁 52

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 61: Verify – Command Dword 10 and Command Dword 11</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-061-CLAIM figure-table:NVMCS13-NVM-FIG-061 -->

**SPEC。** Figure 61〈Verify – Command Dword 10 and Command Dword 11〉：64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SLBA]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SLBA` | 範圍起始 LBA；SDLBA 選 Copy 目的，DSLBA 是 Get LBA Status descriptor 的起點。 |
| `相關欄位` | CDW10, CDW11 — 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。
3. 比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 61 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 |
| 邊界 | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

**說明性範例。** 要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。

**常見誤解。** Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SLBA, CDW10, CDW11

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 61, 文件頁 52, PDF 頁 52

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 62: Verify – Command Dword 12</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-062-CLAIM figure-table:NVMCS13-NVM-FIG-062 -->

**SPEC。** Figure 62〈Verify – Command Dword 12〉：CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LR]
          ↓
[擷取欄位: FUA] → [套用編碼: PRINFO]
                                      ↓
[驗證證據: STC]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LR` | Limited Retry；指定受 Error Recovery policy 約束的重試行為。 |
| `FUA` | Force Unit Access；要求 nonvolatile-media 語意，不自動建立其他命令的順序。 |
| `PRINFO` | PRACT 與 PRCHK 的組合欄位；Copy 的 R／W 版本分別控制讀端／寫端。 |
| `STC` | Storage Tag Check；獨立於三位元 PRCHK，STS=0 時忽略。 |
| `CETYPE` | Command Extension Type／Value；Type 先決定 Value 的用途，不能固定當作 DSM hints。 |
| `NLB` | Number of Logical Blocks；本報告命令／status descriptors 的該欄為 0-based。DSM 的 LLB 另為1-based。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。
3. 比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 62 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。 |
| 邊界 | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

**說明性範例。** 要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。

**常見誤解。** Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LR, FUA, PRINFO, STC, CETYPE, NLB

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 62, 文件頁 52, PDF 頁 52

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 63: Verify - Command Dword 13 if CETYPE is non-zero</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-063-CLAIM figure-table:NVMCS13-NVM-FIG-063 -->

**SPEC。** Figure 63〈Verify - Command Dword 13 if CETYPE is non-zero〉：CETYPE 非零時 CDW13 low16 解讀為 CEV；CETYPE=0 的 layout 另有定義或 reserved，不能同時塞 DSM hints。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CETYPE 非零時 CDW13 low16 解讀為 CEV；CETYPE=0 的 layout 另有定義或 reserved，不能同時塞 DSM hints。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CETYPE]
          ↓
[擷取欄位: CEV] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CETYPE` | Command Extension Type／Value；Type 先決定 Value 的用途，不能固定當作 DSM hints。 |
| `CEV` | Command Extension Type／Value；Type 先決定 Value 的用途，不能固定當作 DSM hints。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CETYPE 非零時 CDW13 low16 解讀為 CEV；CETYPE=0 的 layout 另有定義或 reserved，不能同時塞 DSM hints。
3. 比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 63 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CETYPE 非零時 CDW13 low16 解讀為 CEV；CETYPE=0 的 layout 另有定義或 reserved，不能同時塞 DSM hints。 |
| 邊界 | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

**說明性範例。** 要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。

**常見誤解。** Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** CETYPE, CEV

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 63, 文件頁 52, PDF 頁 52

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 64: Verify – Command Dword 14</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-064-CLAIM figure-table:NVMCS13-NVM-FIG-064 -->

**SPEC。** Figure 64〈Verify – Command Dword 14〉：CDW14 是 expected-tag 空間低 32 bits；它未必全是 Reference Tag，STS 可能占用其中高 bits。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW14 是 expected-tag 空間低 32 bits；它未必全是 Reference Tag，STS 可能占用其中高 bits。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ELBTL]
          ↓
[擷取欄位: ELBTU] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ELBTL` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `ELBTU` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW14 是 expected-tag 空間低 32 bits；它未必全是 Reference Tag，STS 可能占用其中高 bits。
3. 比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 64 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW14 是 expected-tag 空間低 32 bits；它未必全是 Reference Tag，STS 可能占用其中高 bits。 |
| 邊界 | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

**說明性範例。** 要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。

**常見誤解。** Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** ELBTL, ELBTU

**來源 keyword 索引：** may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 64, 文件頁 53, PDF 頁 53

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 65: Verify – Command Dword 15</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-065-CLAIM figure-table:NVMCS13-NVM-FIG-065 -->

**SPEC。** Figure 65〈Verify – Command Dword 15〉：CDW15 high16 是 Application Tag mask，low16 是 expected tag；mask bit=0 表示不比較該位，不是要求 tag bit=0。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW15 high16 是 Application Tag mask，low16 是 expected tag；mask bit=0 表示不比較該位，不是要求 tag bit=0。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ELBATM]
          ↓
[擷取欄位: ELBAT] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ELBATM` | Tag comparison mask；bit=0 排除比較，Storage mask 額外受支援與對齊限制。 |
| `ELBAT` | Logical Block Application Tag／expected tag；16-bit，checking 與 mask 及停用值規則共同決定。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW15 high16 是 Application Tag mask，low16 是 expected tag；mask bit=0 表示不比較該位，不是要求 tag bit=0。
3. 比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 65 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW15 high16 是 Application Tag mask，low16 是 expected tag；mask bit=0 表示不比較該位，不是要求 tag bit=0。 |
| 邊界 | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

**說明性範例。** 要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。

**常見誤解。** Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** ELBATM, ELBAT

**來源 keyword 索引：** may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 65, 文件頁 53, PDF 頁 53

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 66: Verify – Command Specific Status Values</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-066-CLAIM figure-table:NVMCS13-NVM-FIG-066 -->

**SPEC。** Figure 66〈Verify – Command Specific Status Values〉：把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SCT]
          ↓
[擷取欄位: SC] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SCT` | Status Code Type 與 Status Code；兩欄共同識別錯誤，單看 SC 可能誤判。 |
| `SC` | Status Code Type 與 Status Code；兩欄共同識別錯誤，單看 SC 可能誤判。 |
| `相關欄位` | Command-specific error — 把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。
3. 比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 66 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。 |
| 邊界 | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

**說明性範例。** 要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。

**常見誤解。** Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SCT, SC, Command-specific error

**來源 keyword 索引：** may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 66, 文件頁 53, PDF 頁 53

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 67: Write – Metadata Pointer</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-067-CLAIM figure-table:NVMCS13-NVM-FIG-067 -->

**SPEC。** Figure 67〈Write – Metadata Pointer〉：MPTR 只在所選格式使用 separate metadata 時提供 metadata 位置；先核對 PSDT／metadata 格式，不能把它當成 user-data buffer。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

MPTR 只在所選格式使用 separate metadata 時提供 metadata 位置；先核對 PSDT／metadata 格式，不能把它當成 user-data buffer。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MPTR]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MPTR` | Separate metadata 的指標；metadata placement 由 namespace format 與命令欄位決定。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. MPTR 只在所選格式使用 separate metadata 時提供 metadata 位置；先核對 PSDT／metadata 格式，不能把它當成 user-data buffer。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 67 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | MPTR 只在所選格式使用 separate metadata 時提供 metadata 位置；先核對 PSDT／metadata 格式，不能把它當成 user-data buffer。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** MPTR

**來源 keyword 索引：** may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 67, 文件頁 53, PDF 頁 53

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 68: Write – Data Pointer</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-068-CLAIM figure-table:NVMCS13-NVM-FIG-068 -->

**SPEC。** Figure 68〈Write – Data Pointer〉：這裡的 DPTR 指向 host 輸入資料：Compare 的 expected data 或 Write 的新資料；PRP／SGL 由 common command format 決定。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

這裡的 DPTR 指向 host 輸入資料：Compare 的 expected data 或 Write 的新資料；PRP／SGL 由 common command format 決定。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

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
| `DPTR` | 命令 data pointer；Read 是目的、Write 是來源、Copy／DSM 指向 descriptors。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 這裡的 DPTR 指向 host 輸入資料：Compare 的 expected data 或 Write 的新資料；PRP／SGL 由 common command format 決定。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 68 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 這裡的 DPTR 指向 host 輸入資料：Compare 的 expected data 或 Write 的新資料；PRP／SGL 由 common command format 決定。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DPTR

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 68, 文件頁 54, PDF 頁 54

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 69: Write – Command Dword 2 and Dword 3</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-069-CLAIM figure-table:NVMCS13-NVM-FIG-069 -->

**SPEC。** Figure 69〈Write – Command Dword 2 and Dword 3〉：Upper／lower tag 欄位組成寫入端的 Storage 與初始 Reference Tag；Copy 的這組 command fields 屬於 destination，source expectations 在 descriptors。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Upper／lower tag 欄位組成寫入端的 Storage 與初始 Reference Tag；Copy 的這組 command fields 屬於 destination，source expectations 在 descriptors。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBTU]
          ↓
[擷取欄位: LBTL] → [套用編碼: LBST]
                                      ↓
[驗證證據: ILBRT]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBTU` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `LBTL` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `LBST` | Logical Block Storage Tag／Expected Logical Block Storage Tag；寬度由 STS 決定。 |
| `ILBRT` | Initial Logical Block Reference Tag／expected 初值；Type 1／2 依 block 遞增並在欄位寬度處回捲。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Upper／lower tag 欄位組成寫入端的 Storage 與初始 Reference Tag；Copy 的這組 command fields 屬於 destination，source expectations 在 descriptors。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 69 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Upper／lower tag 欄位組成寫入端的 Storage 與初始 Reference Tag；Copy 的這組 command fields 屬於 destination，source expectations 在 descriptors。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LBTU, LBTL, LBST, ILBRT

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 69, 文件頁 54, PDF 頁 54

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 70: Write – Command Dword 10 and Command Dword 11</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-070-CLAIM figure-table:NVMCS13-NVM-FIG-070 -->

**SPEC。** Figure 70〈Write – Command Dword 10 and Command Dword 11〉：64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SLBA]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SLBA` | 範圍起始 LBA；SDLBA 選 Copy 目的，DSLBA 是 Get LBA Status descriptor 的起點。 |
| `相關欄位` | CDW10, CDW11 — 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 70 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SLBA, CDW10, CDW11

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 70, 文件頁 54, PDF 頁 54

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 71: Write – Command Dword 12</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-071-CLAIM figure-table:NVMCS13-NVM-FIG-071 -->

**SPEC。** Figure 71〈Write – Command Dword 12〉：CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LR]
          ↓
[擷取欄位: FUA] → [套用編碼: PRINFO]
                                      ↓
[驗證證據: STC]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LR` | Limited Retry；指定受 Error Recovery policy 約束的重試行為。 |
| `FUA` | Force Unit Access；要求 nonvolatile-media 語意，不自動建立其他命令的順序。 |
| `PRINFO` | PRACT 與 PRCHK 的組合欄位；Copy 的 R／W 版本分別控制讀端／寫端。 |
| `STC` | Storage Tag Check；獨立於三位元 PRCHK，STS=0 時忽略。 |
| `CETYPE` | Command Extension Type／Value；Type 先決定 Value 的用途，不能固定當作 DSM hints。 |
| `NLB` | Number of Logical Blocks；本報告命令／status descriptors 的該欄為 0-based。DSM 的 LLB 另為1-based。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 71 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LR, FUA, PRINFO, STC, CETYPE, NLB

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 71, 文件頁 54, PDF 頁 54

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 72: Write – Command Dword 13 if CETYPE is cleared to 0h</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-072-CLAIM figure-table:NVMCS13-NVM-FIG-072 -->

**SPEC。** Figure 72〈Write – Command Dword 13 if CETYPE is cleared to 0h〉：Write 的 CETYPE=0 layout 包含 high16 DSPEC 與 low8 DSM；不要與 CETYPE 非零的 CEV layout 混寫。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Write 的 CETYPE=0 layout 包含 high16 DSPEC 與 low8 DSM；不要與 CETYPE 非零的 CEV layout 混寫。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DSPEC]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DSPEC` | Directive Type／Specific 欄位；Directive 類型決定 Specific 的內容與 placement 效果。 |
| `相關欄位` | DSM — Write 的 CETYPE=0 layout 包含 high16 DSPEC 與 low8 DSM；不要與 CETYPE 非零的 CEV layout 混寫。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Write 的 CETYPE=0 layout 包含 high16 DSPEC 與 low8 DSM；不要與 CETYPE 非零的 CEV layout 混寫。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 72 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Write 的 CETYPE=0 layout 包含 high16 DSPEC 與 low8 DSM；不要與 CETYPE 非零的 CEV layout 混寫。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DSPEC, DSM

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 72, 文件頁 54-55, PDF 頁 54-55

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 73: Write - Command Dword 13 if CETYPE is non-zero</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-073-CLAIM figure-table:NVMCS13-NVM-FIG-073 -->

**SPEC。** Figure 73〈Write - Command Dword 13 if CETYPE is non-zero〉：CDW13 high16 保存 Directive Specific，low16 依 CETYPE 保存 CEV；Directive 與 command extension 是獨立欄位。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW13 high16 保存 Directive Specific，low16 依 CETYPE 保存 CEV；Directive 與 command extension 是獨立欄位。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DSPEC]
          ↓
[擷取欄位: CEV] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DSPEC` | Directive Type／Specific 欄位；Directive 類型決定 Specific 的內容與 placement 效果。 |
| `CEV` | Command Extension Type／Value；Type 先決定 Value 的用途，不能固定當作 DSM hints。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW13 high16 保存 Directive Specific，low16 依 CETYPE 保存 CEV；Directive 與 command extension 是獨立欄位。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 73 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW13 high16 保存 Directive Specific，low16 依 CETYPE 保存 CEV；Directive 與 command extension 是獨立欄位。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DSPEC, CEV

**來源 keyword 索引：** reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 73, 文件頁 55, PDF 頁 55

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 74: Write – Command Dword 14</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-074-CLAIM figure-table:NVMCS13-NVM-FIG-074 -->

**SPEC。** Figure 74〈Write – Command Dword 14〉：CDW14 提供寫入 tags 的低 32 bits；依 STS 將 space 分割，不能把高位 Storage Tag 全部丟棄。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW14 提供寫入 tags 的低 32 bits；依 STS 將 space 分割，不能把高位 Storage Tag 全部丟棄。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBTL]
          ↓
[擷取欄位: LBST] → [套用編碼: ILBRT]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBTL` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `LBST` | Logical Block Storage Tag／Expected Logical Block Storage Tag；寬度由 STS 決定。 |
| `ILBRT` | Initial Logical Block Reference Tag／expected 初值；Type 1／2 依 block 遞增並在欄位寬度處回捲。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW14 提供寫入 tags 的低 32 bits；依 STS 將 space 分割，不能把高位 Storage Tag 全部丟棄。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 74 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW14 提供寫入 tags 的低 32 bits；依 STS 將 space 分割，不能把高位 Storage Tag 全部丟棄。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LBTL, LBST, ILBRT

**來源 keyword 索引：** reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 74, 文件頁 55, PDF 頁 55

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 75: Write – Command Dword 15</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-075-CLAIM figure-table:NVMCS13-NVM-FIG-075 -->

**SPEC。** Figure 75〈Write – Command Dword 15〉：Application Tag mask 與 tag 分別在 CDW15 high16／low16；Copy 使用於寫入目的端，來源端有獨立 expected 欄位。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Application Tag mask 與 tag 分別在 CDW15 high16／low16；Copy 使用於寫入目的端，來源端有獨立 expected 欄位。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBATM]
          ↓
[擷取欄位: LBAT] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBATM` | Tag comparison mask；bit=0 排除比較，Storage mask 額外受支援與對齊限制。 |
| `LBAT` | Logical Block Application Tag／expected tag；16-bit，checking 與 mask 及停用值規則共同決定。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Application Tag mask 與 tag 分別在 CDW15 high16／low16；Copy 使用於寫入目的端，來源端有獨立 expected 欄位。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 75 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Application Tag mask 與 tag 分別在 CDW15 high16／low16；Copy 使用於寫入目的端，來源端有獨立 expected 欄位。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LBATM, LBAT

**來源 keyword 索引：** reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 75, 文件頁 55, PDF 頁 55

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 76: Write – Command Specific Status Values</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-076-CLAIM figure-table:NVMCS13-NVM-FIG-076 -->

**SPEC。** Figure 76〈Write – Command Specific Status Values〉：把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SCT]
          ↓
[擷取欄位: SC] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SCT` | Status Code Type 與 Status Code；兩欄共同識別錯誤，單看 SC 可能誤判。 |
| `SC` | Status Code Type 與 Status Code；兩欄共同識別錯誤，單看 SC 可能誤判。 |
| `相關欄位` | Command-specific error — 把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 76 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SCT, SC, Command-specific error

**來源 keyword 索引：** shall not, shall, may, optional, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 76, 文件頁 56, PDF 頁 56

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 77: Write Uncorrectable – Command Dword 10 and Command Dword 11</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-077-CLAIM figure-table:NVMCS13-NVM-FIG-077 -->

**SPEC。** Figure 77〈Write Uncorrectable – Command Dword 10 and Command Dword 11〉：64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SLBA]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SLBA` | 範圍起始 LBA；SDLBA 選 Copy 目的，DSLBA 是 Get LBA Status descriptor 的起點。 |
| `相關欄位` | CDW10, CDW11 — 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。
3. 這兩個命令沒有 host user-data payload，但會改變 namespace 語意。先辨識範圍模式，再分配 PI 與 size-limit 檢查。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 77 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 |
| 邊界 | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

**說明性範例。** Host 送 NSZ=1 後得到 Successful Completion 與 LBACZ=0，必須判為僅 range 被清零；舊 controller 可能忽略不支援的 NSZ。不能將 command success 自動升格為整個 namespace 清零。

**常見誤解。** DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SLBA, CDW10, CDW11

**來源 keyword 索引：** shall not, shall, may, optional, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7, Figure 77, 文件頁 56, PDF 頁 56

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 78: Write Uncorrectable – Command Dword 12</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-078-CLAIM figure-table:NVMCS13-NVM-FIG-078 -->

**SPEC。** Figure 78〈Write Uncorrectable – Command Dword 12〉：Write Uncorrectable 的 CDW12 保留 Directive Type 與 0-based NLB；沒有 Read／Write 的 FUA／PRINFO 欄位，不能直接複用那些命令。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Write Uncorrectable 的 CDW12 保留 Directive Type 與 0-based NLB；沒有 Read／Write 的 FUA／PRINFO 欄位，不能直接複用那些命令。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DTYPE]
          ↓
[擷取欄位: NLB] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DTYPE` | Directive Type／Specific 欄位；Directive 類型決定 Specific 的內容與 placement 效果。 |
| `NLB` | Number of Logical Blocks；本報告命令／status descriptors 的該欄為 0-based。DSM 的 LLB 另為1-based。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Write Uncorrectable 的 CDW12 保留 Directive Type 與 0-based NLB；沒有 Read／Write 的 FUA／PRINFO 欄位，不能直接複用那些命令。
3. 這兩個命令沒有 host user-data payload，但會改變 namespace 語意。先辨識範圍模式，再分配 PI 與 size-limit 檢查。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 78 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Write Uncorrectable 的 CDW12 保留 Directive Type 與 0-based NLB；沒有 Read／Write 的 FUA／PRINFO 欄位，不能直接複用那些命令。 |
| 邊界 | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

**說明性範例。** Host 送 NSZ=1 後得到 Successful Completion 與 LBACZ=0，必須判為僅 range 被清零；舊 controller 可能忽略不支援的 NSZ。不能將 command success 自動升格為整個 namespace 清零。

**常見誤解。** DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DTYPE, NLB

**來源 keyword 索引：** shall not, shall, may, optional, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7, Figure 78, 文件頁 56, PDF 頁 56

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 79: Write Uncorrectable – Command Dword 13</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-079-CLAIM figure-table:NVMCS13-NVM-FIG-079 -->

**SPEC。** Figure 79〈Write Uncorrectable – Command Dword 13〉：此 CDW13 layout 只使用 high16 DSPEC，low16 reserved；保留位不是額外的 tag 或長度空間。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

此 CDW13 layout 只使用 high16 DSPEC，low16 reserved；保留位不是額外的 tag 或長度空間。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DSPEC]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DSPEC` | Directive Type／Specific 欄位；Directive 類型決定 Specific 的內容與 placement 效果。 |
| `相關欄位` | Reserved — 此 CDW13 layout 只使用 high16 DSPEC，low16 reserved；保留位不是額外的 tag 或長度空間。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 此 CDW13 layout 只使用 high16 DSPEC，low16 reserved；保留位不是額外的 tag 或長度空間。
3. 這兩個命令沒有 host user-data payload，但會改變 namespace 語意。先辨識範圍模式，再分配 PI 與 size-limit 檢查。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 79 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 此 CDW13 layout 只使用 high16 DSPEC，low16 reserved；保留位不是額外的 tag 或長度空間。 |
| 邊界 | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

**說明性範例。** Host 送 NSZ=1 後得到 Successful Completion 與 LBACZ=0，必須判為僅 range 被清零；舊 controller 可能忽略不支援的 NSZ。不能將 command success 自動升格為整個 namespace 清零。

**常見誤解。** DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DSPEC, Reserved

**來源 keyword 索引：** shall not, shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7, Figure 79, 文件頁 57, PDF 頁 57

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 80: Write Uncorrectable – Command Specific Status Values</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-080-CLAIM figure-table:NVMCS13-NVM-FIG-080 -->

**SPEC。** Figure 80〈Write Uncorrectable – Command Specific Status Values〉：Write Uncorrectable 的本表只列 Attempted Write to Read Only Range；不能把其他命令的 PI 狀態集合套進來。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Write Uncorrectable 的本表只列 Attempted Write to Read Only Range；不能把其他命令的 PI 狀態集合套進來。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Attempted Write to Read Only Range — Write Uncorrectable 的本表只列 Attempted Write to Read Only Range；不能把其他命令的 PI 狀態集合套進來。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Write Uncorrectable 的本表只列 Attempted Write to Read Only Range；不能把其他命令的 PI 狀態集合套進來。
3. 這兩個命令沒有 host user-data payload，但會改變 namespace 語意。先辨識範圍模式，再分配 PI 與 size-limit 檢查。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 80 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Write Uncorrectable 的本表只列 Attempted Write to Read Only Range；不能把其他命令的 PI 狀態集合套進來。 |
| 邊界 | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

**說明性範例。** Host 送 NSZ=1 後得到 Successful Completion 與 LBACZ=0，必須判為僅 range 被清零；舊 controller 可能忽略不支援的 NSZ。不能將 command success 自動升格為整個 namespace 清零。

**常見誤解。** DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Attempted Write to Read Only Range

**來源 keyword 索引：** shall not, shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7, Figure 80, 文件頁 57, PDF 頁 57

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 81: Write Zeroes – Command Dword 2 and Dword 3</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-081-CLAIM figure-table:NVMCS13-NVM-FIG-081 -->

**SPEC。** Figure 81〈Write Zeroes – Command Dword 2 and Dword 3〉：Upper／lower tag 欄位組成寫入端的 Storage 與初始 Reference Tag；Copy 的這組 command fields 屬於 destination，source expectations 在 descriptors。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Upper／lower tag 欄位組成寫入端的 Storage 與初始 Reference Tag；Copy 的這組 command fields 屬於 destination，source expectations 在 descriptors。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBTU]
          ↓
[擷取欄位: LBTL] → [套用編碼: LBST]
                                      ↓
[驗證證據: ILBRT]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBTU` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `LBTL` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `LBST` | Logical Block Storage Tag／Expected Logical Block Storage Tag；寬度由 STS 決定。 |
| `ILBRT` | Initial Logical Block Reference Tag／expected 初值；Type 1／2 依 block 遞增並在欄位寬度處回捲。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Upper／lower tag 欄位組成寫入端的 Storage 與初始 Reference Tag；Copy 的這組 command fields 屬於 destination，source expectations 在 descriptors。
3. 這兩個命令沒有 host user-data payload，但會改變 namespace 語意。先辨識範圍模式，再分配 PI 與 size-limit 檢查。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 81 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Upper／lower tag 欄位組成寫入端的 Storage 與初始 Reference Tag；Copy 的這組 command fields 屬於 destination，source expectations 在 descriptors。 |
| 邊界 | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

**說明性範例。** Host 送 NSZ=1 後得到 Successful Completion 與 LBACZ=0，必須判為僅 range 被清零；舊 controller 可能忽略不支援的 NSZ。不能將 command success 自動升格為整個 namespace 清零。

**常見誤解。** DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LBTU, LBTL, LBST, ILBRT

**來源 keyword 索引：** shall, should, may, optional, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 81, 文件頁 59, PDF 頁 59

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 82: Write Zeroes – Command Dword 10 and Command Dword 11</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-082-CLAIM figure-table:NVMCS13-NVM-FIG-082 -->

**SPEC。** Figure 82〈Write Zeroes – Command Dword 10 and Command Dword 11〉：64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SLBA]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SLBA` | 範圍起始 LBA；SDLBA 選 Copy 目的，DSLBA 是 Get LBA Status descriptor 的起點。 |
| `相關欄位` | CDW10, CDW11 — 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。
3. 這兩個命令沒有 host user-data payload，但會改變 namespace 語意。先辨識範圍模式，再分配 PI 與 size-limit 檢查。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 82 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 |
| 邊界 | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

**說明性範例。** Host 送 NSZ=1 後得到 Successful Completion 與 LBACZ=0，必須判為僅 range 被清零；舊 controller 可能忽略不支援的 NSZ。不能將 command success 自動升格為整個 namespace 清零。

**常見誤解。** DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SLBA, CDW10, CDW11

**來源 keyword 索引：** shall, should, may, optional, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 82, 文件頁 59, PDF 頁 59

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 83: Write Zeroes – Command Dword 12</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-083-CLAIM figure-table:NVMCS13-NVM-FIG-083 -->

**SPEC。** Figure 83〈Write Zeroes – Command Dword 12〉：NSZ 在 bit23，DEAC 在 bit25，因此這裡 DTYPE 只有 bits22:20。PRCHK=000b、STC=0；整個 namespace 模式還要 NSZS 與零值讀取條件。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

NSZ 在 bit23，DEAC 在 bit25，因此這裡 DTYPE 只有 bits22:20。PRCHK=000b、STC=0；整個 namespace 模式還要 NSZS 與零值讀取條件。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSZ]
          ↓
[擷取欄位: DEAC] → [套用編碼: PRINFO]
                                      ↓
[驗證證據: STC]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSZ` | Namespace Zeroes；要求全 namespace 清零，需額外 capability 與 DEAC 條件。 |
| `DEAC` | Write Zeroes 的 deallocate 選擇；與 namespace 支援、NSZ、回讀規則一起判讀。 |
| `PRINFO` | PRACT 與 PRCHK 的組合欄位；Copy 的 R／W 版本分別控制讀端／寫端。 |
| `STC` | Storage Tag Check；獨立於三位元 PRCHK，STS=0 時忽略。 |
| `DTYPE` | Directive Type／Specific 欄位；Directive 類型決定 Specific 的內容與 placement 效果。 |
| `NLB` | Number of Logical Blocks；本報告命令／status descriptors 的該欄為 0-based。DSM 的 LLB 另為1-based。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. NSZ 在 bit23，DEAC 在 bit25，因此這裡 DTYPE 只有 bits22:20。PRCHK=000b、STC=0；整個 namespace 模式還要 NSZS 與零值讀取條件。
3. 這兩個命令沒有 host user-data payload，但會改變 namespace 語意。先辨識範圍模式，再分配 PI 與 size-limit 檢查。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 83 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | NSZ 在 bit23，DEAC 在 bit25，因此這裡 DTYPE 只有 bits22:20。PRCHK=000b、STC=0；整個 namespace 模式還要 NSZS 與零值讀取條件。 |
| 邊界 | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

**說明性範例。** Host 送 NSZ=1 後得到 Successful Completion 與 LBACZ=0，必須判為僅 range 被清零；舊 controller 可能忽略不支援的 NSZ。不能將 command success 自動升格為整個 namespace 清零。

**常見誤解。** DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NSZ, DEAC, PRINFO, STC, DTYPE, NLB

**來源 keyword 索引：** shall, should, may, optional, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 83, 文件頁 59-60, PDF 頁 59-60

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 84: Write Zeroes – Command Dword 13 if CETYPE is cleared to 0h</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-084-CLAIM figure-table:NVMCS13-NVM-FIG-084 -->

**SPEC。** Figure 84〈Write Zeroes – Command Dword 13 if CETYPE is cleared to 0h〉：此 CDW13 layout 只使用 high16 DSPEC，low16 reserved；保留位不是額外的 tag 或長度空間。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

此 CDW13 layout 只使用 high16 DSPEC，low16 reserved；保留位不是額外的 tag 或長度空間。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DSPEC]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DSPEC` | Directive Type／Specific 欄位；Directive 類型決定 Specific 的內容與 placement 效果。 |
| `相關欄位` | Reserved — 此 CDW13 layout 只使用 high16 DSPEC，low16 reserved；保留位不是額外的 tag 或長度空間。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 此 CDW13 layout 只使用 high16 DSPEC，low16 reserved；保留位不是額外的 tag 或長度空間。
3. 這兩個命令沒有 host user-data payload，但會改變 namespace 語意。先辨識範圍模式，再分配 PI 與 size-limit 檢查。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 84 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 此 CDW13 layout 只使用 high16 DSPEC，low16 reserved；保留位不是額外的 tag 或長度空間。 |
| 邊界 | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

**說明性範例。** Host 送 NSZ=1 後得到 Successful Completion 與 LBACZ=0，必須判為僅 range 被清零；舊 controller 可能忽略不支援的 NSZ。不能將 command success 自動升格為整個 namespace 清零。

**常見誤解。** DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DSPEC, Reserved

**來源 keyword 索引：** shall, should, optional, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 84, 文件頁 60, PDF 頁 60

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 85: Write Zeroes – Command Dword 13 if CETYPE is non-zero</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-085-CLAIM figure-table:NVMCS13-NVM-FIG-085 -->

**SPEC。** Figure 85〈Write Zeroes – Command Dword 13 if CETYPE is non-zero〉：CDW13 high16 保存 Directive Specific，low16 依 CETYPE 保存 CEV；Directive 與 command extension 是獨立欄位。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW13 high16 保存 Directive Specific，low16 依 CETYPE 保存 CEV；Directive 與 command extension 是獨立欄位。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DSPEC]
          ↓
[擷取欄位: CEV] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DSPEC` | Directive Type／Specific 欄位；Directive 類型決定 Specific 的內容與 placement 效果。 |
| `CEV` | Command Extension Type／Value；Type 先決定 Value 的用途，不能固定當作 DSM hints。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW13 high16 保存 Directive Specific，low16 依 CETYPE 保存 CEV；Directive 與 command extension 是獨立欄位。
3. 這兩個命令沒有 host user-data payload，但會改變 namespace 語意。先辨識範圍模式，再分配 PI 與 size-limit 檢查。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 85 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW13 high16 保存 Directive Specific，low16 依 CETYPE 保存 CEV；Directive 與 command extension 是獨立欄位。 |
| 邊界 | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

**說明性範例。** Host 送 NSZ=1 後得到 Successful Completion 與 LBACZ=0，必須判為僅 range 被清零；舊 controller 可能忽略不支援的 NSZ。不能將 command success 自動升格為整個 namespace 清零。

**常見誤解。** DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DSPEC, CEV

**來源 keyword 索引：** shall, should, optional, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 85, 文件頁 60, PDF 頁 60

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 86: Write Zeroes – Command Dword 14</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-086-CLAIM figure-table:NVMCS13-NVM-FIG-086 -->

**SPEC。** Figure 86〈Write Zeroes – Command Dword 14〉：CDW14 提供寫入 tags 的低 32 bits；依 STS 將 space 分割，不能把高位 Storage Tag 全部丟棄。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW14 提供寫入 tags 的低 32 bits；依 STS 將 space 分割，不能把高位 Storage Tag 全部丟棄。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBTL]
          ↓
[擷取欄位: LBST] → [套用編碼: ILBRT]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBTL` | Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。 |
| `LBST` | Logical Block Storage Tag／Expected Logical Block Storage Tag；寬度由 STS 決定。 |
| `ILBRT` | Initial Logical Block Reference Tag／expected 初值；Type 1／2 依 block 遞增並在欄位寬度處回捲。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW14 提供寫入 tags 的低 32 bits；依 STS 將 space 分割，不能把高位 Storage Tag 全部丟棄。
3. 這兩個命令沒有 host user-data payload，但會改變 namespace 語意。先辨識範圍模式，再分配 PI 與 size-limit 檢查。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 86 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDW14 提供寫入 tags 的低 32 bits；依 STS 將 space 分割，不能把高位 Storage Tag 全部丟棄。 |
| 邊界 | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

**說明性範例。** Host 送 NSZ=1 後得到 Successful Completion 與 LBACZ=0，必須判為僅 range 被清零；舊 controller 可能忽略不支援的 NSZ。不能將 command success 自動升格為整個 namespace 清零。

**常見誤解。** DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LBTL, LBST, ILBRT

**來源 keyword 索引：** shall, should, optional, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 86, 文件頁 60, PDF 頁 60

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 87: Write Zeroes – Command Dword 15</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-087-CLAIM figure-table:NVMCS13-NVM-FIG-087 -->

**SPEC。** Figure 87〈Write Zeroes – Command Dword 15〉：Application Tag mask 與 tag 分別在 CDW15 high16／low16；Copy 使用於寫入目的端，來源端有獨立 expected 欄位。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Application Tag mask 與 tag 分別在 CDW15 high16／low16；Copy 使用於寫入目的端，來源端有獨立 expected 欄位。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBATM]
          ↓
[擷取欄位: LBAT] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBATM` | Tag comparison mask；bit=0 排除比較，Storage mask 額外受支援與對齊限制。 |
| `LBAT` | Logical Block Application Tag／expected tag；16-bit，checking 與 mask 及停用值規則共同決定。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Application Tag mask 與 tag 分別在 CDW15 high16／low16；Copy 使用於寫入目的端，來源端有獨立 expected 欄位。
3. 這兩個命令沒有 host user-data payload，但會改變 namespace 語意。先辨識範圍模式，再分配 PI 與 size-limit 檢查。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 87 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Application Tag mask 與 tag 分別在 CDW15 high16／low16；Copy 使用於寫入目的端，來源端有獨立 expected 欄位。 |
| 邊界 | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

**說明性範例。** Host 送 NSZ=1 後得到 Successful Completion 與 LBACZ=0，必須判為僅 range 被清零；舊 controller 可能忽略不支援的 NSZ。不能將 command success 自動升格為整個 namespace 清零。

**常見誤解。** DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LBATM, LBAT

**來源 keyword 索引：** shall, should, optional, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 87, 文件頁 60, PDF 頁 60

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 88: Write Zeroes – Completion Queue Entry Dword 0</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-088-CLAIM figure-table:NVMCS13-NVM-FIG-088 -->

**SPEC。** Figure 88〈Write Zeroes – Completion Queue Entry Dword 0〉：只在 NSZ=1 且 Successful Completion 下，LBACZ=1 證明整個 namespace 已清零；0 只表示命令 range。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

只在 NSZ=1 且 Successful Completion 下，LBACZ=1 證明整個 namespace 已清零；0 只表示命令 range。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBACZ]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBACZ` | LBAs Cleared to Zero；成功 NSZ 命令的範圍確認 bit。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 只在 NSZ=1 且 Successful Completion 下，LBACZ=1 證明整個 namespace 已清零；0 只表示命令 range。
3. 這兩個命令沒有 host user-data payload，但會改變 namespace 語意。先辨識範圍模式，再分配 PI 與 size-limit 檢查。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 88 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 只在 NSZ=1 且 Successful Completion 下，LBACZ=1 證明整個 namespace 已清零；0 只表示命令 range。 |
| 邊界 | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

**說明性範例。** Host 送 NSZ=1 後得到 Successful Completion 與 LBACZ=0，必須判為僅 range 被清零；舊 controller 可能忽略不支援的 NSZ。不能將 command success 自動升格為整個 namespace 清零。

**常見誤解。** DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LBACZ

**來源 keyword 索引：** shall not, shall, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 88, 文件頁 61, PDF 頁 61

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 89: Write Zeroes – Command Specific Status Values</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-089-CLAIM figure-table:NVMCS13-NVM-FIG-089 -->

**SPEC。** Figure 89〈Write Zeroes – Command Specific Status Values〉：把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SCT]
          ↓
[擷取欄位: SC] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SCT` | Status Code Type 與 Status Code；兩欄共同識別錯誤，單看 SC 可能誤判。 |
| `SC` | Status Code Type 與 Status Code；兩欄共同識別錯誤，單看 SC 可能誤判。 |
| `相關欄位` | Command-specific error — 把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。
3. 這兩個命令沒有 host user-data payload，但會改變 namespace 語意。先辨識範圍模式，再分配 PI 與 size-limit 檢查。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 89 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §3.3.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。 |
| 邊界 | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

**說明性範例。** Host 送 NSZ=1 後得到 Successful Completion 與 LBACZ=0，必須判為僅 range 被清零；舊 controller 可能忽略不支援的 NSZ。不能將 command success 自動升格為整個 namespace 清零。

**常見誤解。** DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SCT, SC, Command-specific error

**來源 keyword 索引：** shall not, shall, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 89, 文件頁 61, PDF 頁 61

</details>

<a id="section-4-1"></a>

### §4.1

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 90: Asynchronous Event Information – Notice</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-090-CLAIM figure-table:NVMCS13-NVM-FIG-090 -->

**SPEC。** Figure 90〈Asynchronous Event Information – Notice〉：分別辨識 namespace attribute、LBA Status 與 Rate Limiting notices；NUSE 與 ANA capacity 特例不產生 attribute-change 通知。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

分別辨識 namespace attribute、LBA Status 與 Rate Limiting notices；NUSE 與 ANA capacity 特例不產生 attribute-change 通知。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Notice 00h, Notice 05h, Notice 09h, Notice 0Ah — 分別辨識 namespace attribute、LBA Status 與 Rate Limiting notices；NUSE 與 ANA capacity 特例不產生 attribute-change 通知。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 分別辨識 namespace attribute、LBA Status 與 Rate Limiting notices；NUSE 與 ANA capacity 特例不產生 attribute-change 通知。
3. 用事件找調查方向，再用正確 scope 的 log 與 command set 定義解碼。統計數據也要依命令分類，不能只按 opcode 名稱猜。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 90 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 分別辨識 namespace attribute、LBA Status 與 Rate Limiting notices；NUSE 與 ANA capacity 特例不產生 attribute-change 通知。 |
| 邊界 | Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。 |

**說明性範例。** 一個 Self-test FLBA=100、valid=1 的紀錄只能定位一個失敗 LBA，不能據此宣告其他 LBAs 全部正常。Error Information LBA=100 的「最低」語意也不能直接套到 FLBA。

**常見誤解。** Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Notice 00h, Notice 05h, Notice 09h, Notice 0Ah

**來源 keyword 索引：** shall not, shall, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.1, Figure 90, 文件頁 62, PDF 頁 62

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 91: Format NVM – Command Dword 10 – NVM Command Set Specific Fields</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-091-CLAIM figure-table:NVMCS13-NVM-FIG-091 -->

**SPEC。** Figure 91〈Format NVM – Command Dword 10 – NVM Command Set Specific Fields〉：PI 選 protection type，MSET 選 metadata transfer；本版 PIL=0。Guard width 另由 LBAF／ELBAF 決定。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

PI 選 protection type，MSET 選 metadata transfer；本版 PIL=0。Guard width 另由 LBAF／ELBAF 決定。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PIL]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PIL` | Protection Information Location；用來判斷 PI 在 metadata 前端或後端，需遵守所選 Guard 格式限制。 |
| `相關欄位` | PI, MSET — PI 選 protection type，MSET 選 metadata transfer；本版 PIL=0。Guard width 另由 LBAF／ELBAF 決定。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. PI 選 protection type，MSET 選 metadata transfer；本版 PIL=0。Guard width 另由 LBAF／ELBAF 決定。
3. 格式切換會改變 block 數與欄位適用性，建立 buffer 前要重新 Identify。能力列表與目前格式不能混用。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 91 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | PI 選 protection type，MSET 選 metadata transfer；本版 PIL=0。Guard width 另由 LBAF／ELBAF 決定。 |
| 邊界 | PI type 1/2/3 與 Guard width 16/32/64 是不同維度。格式變更後 NSZE／NCAP 可改變，舊 LBA Range Type hints 也可能需重設。 |

**說明性範例。** 要使用 64b Guard、MS=16 的格式，先確認 ELBAS、LBAFEE=1、對應 LBAF／ELBAF 及 PI capability。不能只設定 Format 的 PI=1 就宣告 64b Guard。

**常見誤解。** PI type 1/2/3 與 Guard width 16/32/64 是不同維度。格式變更後 NSZE／NCAP 可改變，舊 LBA Range Type hints 也可能需重設。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | PI type 1/2/3 與 Guard width 16/32/64 是不同維度。格式變更後 NSZE／NCAP 可改變，舊 LBA Range Type hints 也可能需重設。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** PIL, PI, MSET

**來源 keyword 索引：** shall, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.2, Figure 91, 文件頁 63, PDF 頁 63

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 92: Feature Identifiers – NVM Command Set</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-092-CLAIM figure-table:NVMCS13-NVM-FIG-092 -->

**SPEC。** Figure 92〈Feature Identifiers – NVM Command Set〉：讀 scope 與 buffer 需求，再看 persistence 註腳；對 saveable Feature 不使用本表 nonsaveable persistence 欄。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

讀 scope 與 buffer 需求，再看 persistence 註腳；對 saveable Feature 不使用本表 nonsaveable persistence 欄。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: FID]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `FID` | 分別選 Feature、log page、I/O command set 與 Identify 回傳資料結構；數值不能跨識別空間混用。 |
| `相關欄位` | Scope, Persistence — 讀 scope 與 buffer 需求，再看 persistence 註腳；對 saveable Feature 不使用本表 nonsaveable persistence 欄。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 讀 scope 與 buffer 需求，再看 persistence 註腳；對 saveable Feature 不使用本表 nonsaveable persistence 欄。
3. 讀 Feature 時先辨識 scope、unit 與可儲存條件。Get、Set、Supported Capabilities 回覆也不能套用同一 payload 解碼。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 92 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 讀 scope 與 buffer 需求，再看 persistence 註腳；對 saveable Feature 不使用本表 nonsaveable persistence 欄。 |
| 邊界 | Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。 |

**說明性範例。** TLER=5 表示 error recovery 的 500 ms 限制，並不是從 SQ submit 起算的整筆命令 500 ms deadline。LBA Range Type 的 NUM=0 表示一個 entry。

**常見誤解。** Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** FID, Scope, Persistence

**來源 keyword 索引：** shall, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3, Figure 92, 文件頁 64, PDF 頁 64

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 93: Set Features – Command Specific Status Values</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-093-CLAIM figure-table:NVMCS13-NVM-FIG-093 -->

**SPEC。** Figure 93〈Set Features – Command Specific Status Values〉：只有 controller 實際檢查 LBA Range Type 且發現 overlap 時才必須回此錯誤；不可假設成功 Set 已完成全面驗證。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

只有 controller 實際檢查 LBA Range Type 且發現 overlap 時才必須回此錯誤；不可假設成功 Set 已完成全面驗證。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Overlapping Range — 只有 controller 實際檢查 LBA Range Type 且發現 overlap 時才必須回此錯誤；不可假設成功 Set 已完成全面驗證。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 只有 controller 實際檢查 LBA Range Type 且發現 overlap 時才必須回此錯誤；不可假設成功 Set 已完成全面驗證。
3. 讀 Feature 時先辨識 scope、unit 與可儲存條件。Get、Set、Supported Capabilities 回覆也不能套用同一 payload 解碼。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 93 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 只有 controller 實際檢查 LBA Range Type 且發現 overlap 時才必須回此錯誤；不可假設成功 Set 已完成全面驗證。 |
| 邊界 | Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。 |

**說明性範例。** TLER=5 表示 error recovery 的 500 ms 限制，並不是從 SQ submit 起算的整筆命令 500 ms deadline。LBA Range Type 的 NUM=0 表示一個 entry。

**常見誤解。** Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Overlapping Range

**來源 keyword 索引：** shall, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3, Figure 93, 文件頁 64, PDF 頁 64

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 94: LBA Range Type – Command Dword 11</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-094-CLAIM figure-table:NVMCS13-NVM-FIG-094 -->

**SPEC。** Figure 94〈LBA Range Type – Command Dword 11〉：NUM low6 是 0-based：Set 時指定有效 entries，Get 時從 CQE DW0 讀實際回傳 entries；兩者都不是 byte count。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

NUM low6 是 0-based：Set 時指定有效 entries，Get 時從 CQE DW0 讀實際回傳 entries；兩者都不是 byte count。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | NUM — NUM low6 是 0-based：Set 時指定有效 entries，Get 時從 CQE DW0 讀實際回傳 entries；兩者都不是 byte count。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. NUM low6 是 0-based：Set 時指定有效 entries，Get 時從 CQE DW0 讀實際回傳 entries；兩者都不是 byte count。
3. 讀 Feature 時先辨識 scope、unit 與可儲存條件。Get、Set、Supported Capabilities 回覆也不能套用同一 payload 解碼。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 94 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | NUM low6 是 0-based：Set 時指定有效 entries，Get 時從 CQE DW0 讀實際回傳 entries；兩者都不是 byte count。 |
| 邊界 | Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。 |

**說明性範例。** TLER=5 表示 error recovery 的 500 ms 限制，並不是從 SQ submit 起算的整筆命令 500 ms deadline。LBA Range Type 的 NUM=0 表示一個 entry。

**常見誤解。** Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NUM

**來源 keyword 索引：** shall, should not, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.2, Figure 94, 文件頁 65, PDF 頁 65

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 95: LBA Range Type – Completion Queue Entry Dword 0</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-095-CLAIM figure-table:NVMCS13-NVM-FIG-095 -->

**SPEC。** Figure 95〈LBA Range Type – Completion Queue Entry Dword 0〉：NUM low6 是 0-based：Set 時指定有效 entries，Get 時從 CQE DW0 讀實際回傳 entries；兩者都不是 byte count。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

NUM low6 是 0-based：Set 時指定有效 entries，Get 時從 CQE DW0 讀實際回傳 entries；兩者都不是 byte count。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | NUM — NUM low6 是 0-based：Set 時指定有效 entries，Get 時從 CQE DW0 讀實際回傳 entries；兩者都不是 byte count。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. NUM low6 是 0-based：Set 時指定有效 entries，Get 時從 CQE DW0 讀實際回傳 entries；兩者都不是 byte count。
3. 讀 Feature 時先辨識 scope、unit 與可儲存條件。Get、Set、Supported Capabilities 回覆也不能套用同一 payload 解碼。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 95 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | NUM low6 是 0-based：Set 時指定有效 entries，Get 時從 CQE DW0 讀實際回傳 entries；兩者都不是 byte count。 |
| 邊界 | Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。 |

**說明性範例。** TLER=5 表示 error recovery 的 500 ms 限制，並不是從 SQ submit 起算的整筆命令 500 ms deadline。LBA Range Type 的 NUM=0 表示一個 entry。

**常見誤解。** Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NUM

**來源 keyword 索引：** shall, should not, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.2, Figure 95, 文件頁 65, PDF 頁 65

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 96: LBA Range Type – Data Structure Entry</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-096-CLAIM figure-table:NVMCS13-NVM-FIG-096 -->

**SPEC。** Figure 96〈LBA Range Type – Data Structure Entry〉：64-byte entry 分開描述用途、host hints 與 range；SLBA／NLB 是 logical blocks，GUID 是識別欄位，不是授權。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

64-byte entry 分開描述用途、host hints 與 range；SLBA／NLB 是 logical blocks，GUID 是識別欄位，不是授權。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SLBA]
          ↓
[擷取欄位: NLB] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SLBA` | 範圍起始 LBA；SDLBA 選 Copy 目的，DSLBA 是 Get LBA Status descriptor 的起點。 |
| `NLB` | Number of Logical Blocks；本報告命令／status descriptors 的該欄為 0-based。DSM 的 LLB 另為1-based。 |
| `相關欄位` | Type, ATTRB, GUID — 64-byte entry 分開描述用途、host hints 與 range；SLBA／NLB 是 logical blocks，GUID 是識別欄位，不是授權。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 64-byte entry 分開描述用途、host hints 與 range；SLBA／NLB 是 logical blocks，GUID 是識別欄位，不是授權。
3. 讀 Feature 時先辨識 scope、unit 與可儲存條件。Get、Set、Supported Capabilities 回覆也不能套用同一 payload 解碼。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 96 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.3.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 64-byte entry 分開描述用途、host hints 與 range；SLBA／NLB 是 logical blocks，GUID 是識別欄位，不是授權。 |
| 邊界 | Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。 |

**說明性範例。** TLER=5 表示 error recovery 的 500 ms 限制，並不是從 SQ submit 起算的整筆命令 500 ms deadline。LBA Range Type 的 NUM=0 表示一個 entry。

**常見誤解。** Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Type, ATTRB, SLBA, NLB, GUID

**來源 keyword 索引：** shall, should not, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.2, Figure 96, 文件頁 65-66, PDF 頁 65-66

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 97: Error Recovery – Command Dword 11</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-097-CLAIM figure-table:NVMCS13-NVM-FIG-097 -->

**SPEC。** Figure 97〈Error Recovery – Command Dword 11〉：DULBE 是 bit16，TLER low16 以 100 ms 計；TLER=0 表示不限制 retry timeout，須由 recovery 起點計時。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

DULBE 是 bit16，TLER low16 以 100 ms 計；TLER=0 表示不限制 retry timeout，須由 recovery 起點計時。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DULBE]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DULBE` | Deallocated or Unwritten Logical Block Error Enable，需 namespace DAE 支援。 |
| `相關欄位` | TLER — DULBE 是 bit16，TLER low16 以 100 ms 計；TLER=0 表示不限制 retry timeout，須由 recovery 起點計時。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. DULBE 是 bit16，TLER low16 以 100 ms 計；TLER=0 表示不限制 retry timeout，須由 recovery 起點計時。
3. 讀 Feature 時先辨識 scope、unit 與可儲存條件。Get、Set、Supported Capabilities 回覆也不能套用同一 payload 解碼。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 97 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.3.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | DULBE 是 bit16，TLER low16 以 100 ms 計；TLER=0 表示不限制 retry timeout，須由 recovery 起點計時。 |
| 邊界 | Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。 |

**說明性範例。** TLER=5 表示 error recovery 的 500 ms 限制，並不是從 SQ submit 起算的整筆命令 500 ms deadline。LBA Range Type 的 NUM=0 表示一個 entry。

**常見誤解。** Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DULBE, TLER

**來源 keyword 索引：** shall, should not, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.3, Figure 97, 文件頁 66, PDF 頁 66

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 98: Write Atomicity Normal – Command Dword 11</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-098-CLAIM figure-table:NVMCS13-NVM-FIG-098 -->

**SPEC。** Figure 98〈Write Atomicity Normal – Command Dword 11〉：DN=1 只解除 normal atomicity 保證，power-fail atomicity 仍須遵守；這是 controller-scoped Feature。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

DN=1 只解除 normal atomicity 保證，power-fail atomicity 仍須遵守；這是 controller-scoped Feature。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DN]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DN` | Write Atomicity Normal 的 Disable Normal；不免除 power-fail atomicity。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. DN=1 只解除 normal atomicity 保證，power-fail atomicity 仍須遵守；這是 controller-scoped Feature。
3. 讀 Feature 時先辨識 scope、unit 與可儲存條件。Get、Set、Supported Capabilities 回覆也不能套用同一 payload 解碼。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 98 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.3.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | DN=1 只解除 normal atomicity 保證，power-fail atomicity 仍須遵守；這是 controller-scoped Feature。 |
| 邊界 | Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。 |

**說明性範例。** TLER=5 表示 error recovery 的 500 ms 限制，並不是從 SQ submit 起算的整筆命令 500 ms deadline。LBA Range Type 的 NUM=0 表示一個 entry。

**常見誤解。** Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DN

**來源 keyword 索引：** shall not, shall, should not, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.4, Figure 98, 文件頁 66-67, PDF 頁 66-67

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 99: Asynchronous Event Configuration – NVM Command Set specific Bit Definitions</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-099-CLAIM figure-table:NVMCS13-NVM-FIG-099 -->

**SPEC。** Figure 99〈Asynchronous Event Configuration – NVM Command Set specific Bit Definitions〉：bits13／22 分別控制 LBA Status 與 Rate Limiting notices；取得 log 和清除事件還須依各 log 的 RAE 流程。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

bits13／22 分別控制 LBA Status 與 Rate Limiting notices；取得 log 和清除事件還須依各 log 的 RAE 流程。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | LBASIN, RLCCN — bits13／22 分別控制 LBA Status 與 Rate Limiting notices；取得 log 和清除事件還須依各 log 的 RAE 流程。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. bits13／22 分別控制 LBA Status 與 Rate Limiting notices；取得 log 和清除事件還須依各 log 的 RAE 流程。
3. 用事件找調查方向，再用正確 scope 的 log 與 command set 定義解碼。統計數據也要依命令分類，不能只按 opcode 名稱猜。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 99 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.3.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | bits13／22 分別控制 LBA Status 與 Rate Limiting notices；取得 log 和清除事件還須依各 log 的 RAE 流程。 |
| 邊界 | Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。 |

**說明性範例。** 一個 Self-test FLBA=100、valid=1 的紀錄只能定位一個失敗 LBA，不能據此宣告其他 LBAs 全部正常。Error Information LBA=100 的「最低」語意也不能直接套到 FLBA。

**常見誤解。** Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LBASIN, RLCCN

**來源 keyword 索引：** shall not, shall, should not, should, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.5, Figure 99, 文件頁 67, PDF 頁 67

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 100: LBA Status Information Attributes – Command Dword 11</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-100-CLAIM figure-table:NVMCS13-NVM-FIG-100 -->

**SPEC。** Figure 100〈LBA Status Information Attributes – Command Dword 11〉：high16 LSIPI 是不可改的 poll interval，low16 LSIRI 是 report interval；兩者均為 100 ms 單位，Set 回傳最接近可支援值。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

high16 LSIPI 是不可改的 poll interval，low16 LSIRI 是 report interval；兩者均為 100 ms 單位，Set 回傳最接近可支援值。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | LSIPI, LSIRI — high16 LSIPI 是不可改的 poll interval，low16 LSIRI 是 report interval；兩者均為 100 ms 單位，Set 回傳最接近可支援值。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. high16 LSIPI 是不可改的 poll interval，low16 LSIRI 是 report interval；兩者均為 100 ms 單位，Set 回傳最接近可支援值。
3. 讀到 potentially unrecoverable 不是每個 block 一定無法讀取。先辨識 ATYPE，再檢查 buffer 是否足夠與 completion condition，最後安排資料修復。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 100 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.3.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | high16 LSIPI 是不可改的 poll interval，low16 LSIRI 是 report interval；兩者均為 100 ms 單位，Set 回傳最接近可支援值。 |
| 邊界 | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

**說明性範例。** log 有 NLSLNE=0 但 ESTULB 非零時，不能當作沒有問題，宜檢查 attached namespaces 的完整 LBA 範圍。取得可疑 LBAs 後，可從其他可靠來源恢復並寫回；後續查詢會移除成功重寫且未再偵測的項目。

**常見誤解。** CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LSIPI, LSIRI

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.6, Figure 100, 文件頁 68, PDF 頁 68

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 101: Host Behavior Support – Data Structure</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-101-CLAIM figure-table:NVMCS13-NVM-FIG-101 -->

**SPEC。** Figure 101〈Host Behavior Support – Data Structure〉：Host Behavior Support byte2 的 LBAFEE 允許 host 宣告延伸 LBA formats；只允許 0／1，並需對照 controller ELBAS。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Host Behavior Support byte2 的 LBAFEE 允許 host 宣告延伸 LBA formats；只允許 0／1，並需對照 controller ELBAS。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBAFEE]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBAFEE` | Host 的 LBA Format Extension Enable 宣告。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Host Behavior Support byte2 的 LBAFEE 允許 host 宣告延伸 LBA formats；只允許 0／1，並需對照 controller ELBAS。
3. 格式切換會改變 block 數與欄位適用性，建立 buffer 前要重新 Identify。能力列表與目前格式不能混用。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 101 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.3.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Host Behavior Support byte2 的 LBAFEE 允許 host 宣告延伸 LBA formats；只允許 0／1，並需對照 controller ELBAS。 |
| 邊界 | PI type 1/2/3 與 Guard width 16/32/64 是不同維度。格式變更後 NSZE／NCAP 可改變，舊 LBA Range Type hints 也可能需重設。 |

**說明性範例。** 要使用 64b Guard、MS=16 的格式，先確認 ELBAS、LBAFEE=1、對應 LBAF／ELBAF 及 PI capability。不能只設定 Format 的 PI=1 就宣告 64b Guard。

**常見誤解。** PI type 1/2/3 與 Guard width 16/32/64 是不同維度。格式變更後 NSZE／NCAP 可改變，舊 LBA Range Type hints 也可能需重設。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | PI type 1/2/3 與 Guard width 16/32/64 是不同維度。格式變更後 NSZE／NCAP 可改變，舊 LBA Range Type hints 也可能需重設。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LBAFEE

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.7, Figure 101, 文件頁 68, PDF 頁 68

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 102: Performance Characteristics – Command Dword 11</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-102-CLAIM figure-table:NVMCS13-NVM-FIG-102 -->

**SPEC。** Figure 102〈Performance Characteristics – Command Dword 11〉：ATTRI low8 選擇標準、list 或 vendor attribute；bit8 RVSPA 刪除 saved vendor value，並非刪除整個 Feature。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

ATTRI low8 選擇標準、list 或 vendor attribute；bit8 RVSPA 刪除 saved vendor value，並非刪除整個 Feature。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | RVSPA, ATTRI — ATTRI low8 選擇標準、list 或 vendor attribute；bit8 RVSPA 刪除 saved vendor value，並非刪除整個 Feature。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. ATTRI low8 選擇標準、list 或 vendor attribute；bit8 RVSPA 刪除 saved vendor value，並非刪除整個 Feature。
3. 此 Feature 回報或管理效能屬性，不能把標準 latency 級別當成對任意 workload 的服務保證。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 102 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.3.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | ATTRI low8 選擇標準、list 或 vendor attribute；bit8 RVSPA 刪除 saved vendor value，並非刪除整個 Feature。 |
| 邊界 | Set ATTRI=00h 或 C0h 會回 Invalid Field in Command。Vendor bytes 的意義需要廠商定義，不能自行推測成標準欄位。 |

**說明性範例。** R4KARL=0Eh 表示 50 μs ≤ 平均 latency <100 μs，並非 14 μs。讀 C0h list 時應使 ATTRTYP 與 Get 的 SEL 一致，再用 PAID 解釋 vendor payload。

**常見誤解。** Set ATTRI=00h 或 C0h 會回 Invalid Field in Command。Vendor bytes 的意義需要廠商定義，不能自行推測成標準欄位。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Set ATTRI=00h 或 C0h 會回 Invalid Field in Command。Vendor bytes 的意義需要廠商定義，不能自行推測成標準欄位。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** RVSPA, ATTRI

**來源 keyword 索引：** shall not, shall, optional, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, Figure 102, 文件頁 69, PDF 頁 69

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 103: Performance Characteristics – Standard Performance Attribute</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-103-CLAIM figure-table:NVMCS13-NVM-FIG-103 -->

**SPEC。** Figure 103〈Performance Characteristics – Standard Performance Attribute〉：R4KARL 是 latency bucket 而非直接時間；0Eh 是 50–100 μs 的半開區間，00h 為未回報。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

R4KARL 是 latency bucket 而非直接時間；0Eh 是 50–100 μs 的半開區間，00h 為未回報。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | R4KARL — R4KARL 是 latency bucket 而非直接時間；0Eh 是 50–100 μs 的半開區間，00h 為未回報。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. R4KARL 是 latency bucket 而非直接時間；0Eh 是 50–100 μs 的半開區間，00h 為未回報。
3. 此 Feature 回報或管理效能屬性，不能把標準 latency 級別當成對任意 workload 的服務保證。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 103 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.3.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | R4KARL 是 latency bucket 而非直接時間；0Eh 是 50–100 μs 的半開區間，00h 為未回報。 |
| 邊界 | Set ATTRI=00h 或 C0h 會回 Invalid Field in Command。Vendor bytes 的意義需要廠商定義，不能自行推測成標準欄位。 |

**說明性範例。** R4KARL=0Eh 表示 50 μs ≤ 平均 latency <100 μs，並非 14 μs。讀 C0h list 時應使 ATTRTYP 與 Get 的 SEL 一致，再用 PAID 解釋 vendor payload。

**常見誤解。** Set ATTRI=00h 或 C0h 會回 Invalid Field in Command。Vendor bytes 的意義需要廠商定義，不能自行推測成標準欄位。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Set ATTRI=00h 或 C0h 會回 Invalid Field in Command。Vendor bytes 的意義需要廠商定義，不能自行推測成標準欄位。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** R4KARL

**來源 keyword 索引：** reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, Figure 103, 文件頁 71, PDF 頁 71

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 104: Performance Characteristics – Performance Attribute Identifier List</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-104-CLAIM figure-table:NVMCS13-NVM-FIG-104 -->

**SPEC。** Figure 104〈Performance Characteristics – Performance Attribute Identifier List〉：ATTRTYP 應與 Get SEL 相符；用 MSVSPA／USVSPA 看 saved slots，再以每個 128-bit PAID 辨識 payload，不假設 slots 連續。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

ATTRTYP 應與 Get SEL 相符；用 MSVSPA／USVSPA 看 saved slots，再以每個 128-bit PAID 辨識 payload，不假設 slots 連續。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | ATTRTYP, MSVSPA, USVSPA, PAID — ATTRTYP 應與 Get SEL 相符；用 MSVSPA／USVSPA 看 saved slots，再以每個 128-bit PAID 辨識 payload，不假設 slots 連續。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. ATTRTYP 應與 Get SEL 相符；用 MSVSPA／USVSPA 看 saved slots，再以每個 128-bit PAID 辨識 payload，不假設 slots 連續。
3. 此 Feature 回報或管理效能屬性，不能把標準 latency 級別當成對任意 workload 的服務保證。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 104 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.3.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | ATTRTYP 應與 Get SEL 相符；用 MSVSPA／USVSPA 看 saved slots，再以每個 128-bit PAID 辨識 payload，不假設 slots 連續。 |
| 邊界 | Set ATTRI=00h 或 C0h 會回 Invalid Field in Command。Vendor bytes 的意義需要廠商定義，不能自行推測成標準欄位。 |

**說明性範例。** R4KARL=0Eh 表示 50 μs ≤ 平均 latency <100 μs，並非 14 μs。讀 C0h list 時應使 ATTRTYP 與 Get 的 SEL 一致，再用 PAID 解釋 vendor payload。

**常見誤解。** Set ATTRI=00h 或 C0h 會回 Invalid Field in Command。Vendor bytes 的意義需要廠商定義，不能自行推測成標準欄位。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Set ATTRI=00h 或 C0h 會回 Invalid Field in Command。Vendor bytes 的意義需要廠商定義，不能自行推測成標準欄位。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** ATTRTYP, MSVSPA, USVSPA, PAID

**來源 keyword 索引：** shall, may, optional, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, Figure 104, 文件頁 72, PDF 頁 72

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 105: Performance Characteristics – Vendor Specific Performance Attribute</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-105-CLAIM figure-table:NVMCS13-NVM-FIG-105 -->

**SPEC。** Figure 105〈Performance Characteristics – Vendor Specific Performance Attribute〉：PAID 指出 vendor payload 的定義，ATTRL 限制有效 VS bytes，最大 FE0h；未知 PAID 不應由標準表格猜測。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

PAID 指出 vendor payload 的定義，ATTRL 限制有效 VS bytes，最大 FE0h；未知 PAID 不應由標準表格猜測。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | PAID, ATTRL, VS — PAID 指出 vendor payload 的定義，ATTRL 限制有效 VS bytes，最大 FE0h；未知 PAID 不應由標準表格猜測。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. PAID 指出 vendor payload 的定義，ATTRL 限制有效 VS bytes，最大 FE0h；未知 PAID 不應由標準表格猜測。
3. 此 Feature 回報或管理效能屬性，不能把標準 latency 級別當成對任意 workload 的服務保證。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 105 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.3.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | PAID 指出 vendor payload 的定義，ATTRL 限制有效 VS bytes，最大 FE0h；未知 PAID 不應由標準表格猜測。 |
| 邊界 | Set ATTRI=00h 或 C0h 會回 Invalid Field in Command。Vendor bytes 的意義需要廠商定義，不能自行推測成標準欄位。 |

**說明性範例。** R4KARL=0Eh 表示 50 μs ≤ 平均 latency <100 μs，並非 14 μs。讀 C0h list 時應使 ATTRTYP 與 Get 的 SEL 一致，再用 PAID 解釋 vendor payload。

**常見誤解。** Set ATTRI=00h 或 C0h 會回 Invalid Field in Command。Vendor bytes 的意義需要廠商定義，不能自行推測成標準欄位。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Set ATTRI=00h 或 C0h 會回 Invalid Field in Command。Vendor bytes 的意義需要廠商定義，不能自行推測成標準欄位。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** PAID, ATTRL, VS

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, Figure 105, 文件頁 73, PDF 頁 73

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 106: Rate Limits – Command Dword 11</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-106-CLAIM figure-table:NVMCS13-NVM-FIG-106 -->

**SPEC。** Figure 106〈Rate Limits – Command Dword 11〉：先辨識 TGT 再解讀 TID；TGT=0 使用 controller ID，不能指定 Admin controller、無效 ID 或 FFFDh..FFFFh。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

先辨識 TGT 再解讀 TID；TGT=0 使用 controller ID，不能指定 Admin controller、無效 ID 或 FFFDh..FFFFh。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TGT]
          ↓
[擷取欄位: TID] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TGT` | Rate Limiting Target／Target Identifier；先選作用域，再解讀 target ID。 |
| `TID` | Rate Limiting Target／Target Identifier；先選作用域，再解讀 target ID。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 先辨識 TGT 再解讀 TID；TGT=0 使用 controller ID，不能指定 Admin controller、無效 ID 或 FFFDh..FFFFh。
3. 先從 LID 28h 取得支援 target，再檢查 HLS／SLS 與 soft-controller 數量。把 host 請求限制和裝置可達能力分開記錄。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 106 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.3.9 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 先辨識 TGT 再解讀 TID；TGT=0 使用 controller ID，不能指定 Admin controller、無效 ID 或 FFFDh..FFFFh。 |
| 邊界 | 未替某 target 設 limits 時，其 limits 是 vendor-specific；不能把缺少設定解讀為無限制。§5.10 開頭的 Hard／Soft 小節引用對調，正確是 5.10.1 Hard、5.10.2 Soft。 |

**說明性範例。** BWSF=1、TBWV=50 表示 500 MiB/s。WBWV 與 WIOPS 控制寫入部分，總量還會按 WRBWR／WRIOPSR 加權；不能把 total 限制只當 read limit。

**常見誤解。** 未替某 target 設 limits 時，其 limits 是 vendor-specific；不能把缺少設定解讀為無限制。§5.10 開頭的 Hard／Soft 小節引用對調，正確是 5.10.1 Hard、5.10.2 Soft。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 未替某 target 設 limits 時，其 limits 是 vendor-specific；不能把缺少設定解讀為無限制。§5.10 開頭的 Hard／Soft 小節引用對調，正確是 5.10.1 Hard、5.10.2 Soft。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** TGT, TID

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.9, Figure 106, 文件頁 73, PDF 頁 73

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 107: Rate Limiting – Data Buffer</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-107-CLAIM figure-table:NVMCS13-NVM-FIG-107 -->

**SPEC。** Figure 107〈Rate Limiting – Data Buffer〉：1024-byte 設定分出 enable/mode、兩種 bandwidth、兩種 IOPS 與兩個 write/read ratios；加權 total consumption 與 write-only consumption 分開計。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

1024-byte 設定分出 enable/mode、兩種 bandwidth、兩種 IOPS 與兩個 write/read ratios；加權 total consumption 與 write-only consumption 分開計。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: BWSF]
          ↓
[擷取欄位: TBWV] → [套用編碼: WBWV]
                                      ↓
[驗證證據: TIOPS]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `BWSF` | Bandwidth Scale Factor；需乘 bandwidth value，單位為 MiB/s 或 GiB/s。 |
| `TBWV` | Total／Write Bandwidth Value 與 Total／Write IOPS limits；bandwidth 另乘 BWSF。 |
| `WBWV` | Total／Write Bandwidth Value 與 Total／Write IOPS limits；bandwidth 另乘 BWSF。 |
| `TIOPS` | Total／Write Bandwidth Value 與 Total／Write IOPS limits；bandwidth 另乘 BWSF。 |
| `WIOPS` | Total／Write Bandwidth Value 與 Total／Write IOPS limits；bandwidth 另乘 BWSF。 |
| `WRIOPSR` | Write-to-Read Bandwidth／IOPS Ratio；計算寫入對 total budget 的權重。 |
| `WRBWR` | Write-to-Read Bandwidth／IOPS Ratio；計算寫入對 total budget 的權重。 |
| `相關欄位` | RLE, RLM — 1024-byte 設定分出 enable/mode、兩種 bandwidth、兩種 IOPS 與兩個 write/read ratios；加權 total consumption 與 write-only consumption 分開計。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 1024-byte 設定分出 enable/mode、兩種 bandwidth、兩種 IOPS 與兩個 write/read ratios；加權 total consumption 與 write-only consumption 分開計。
3. 先從 LID 28h 取得支援 target，再檢查 HLS／SLS 與 soft-controller 數量。把 host 請求限制和裝置可達能力分開記錄。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 107 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.3.9 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 1024-byte 設定分出 enable/mode、兩種 bandwidth、兩種 IOPS 與兩個 write/read ratios；加權 total consumption 與 write-only consumption 分開計。 |
| 邊界 | 未替某 target 設 limits 時，其 limits 是 vendor-specific；不能把缺少設定解讀為無限制。§5.10 開頭的 Hard／Soft 小節引用對調，正確是 5.10.1 Hard、5.10.2 Soft。 |

**說明性範例。** BWSF=1、TBWV=50 表示 500 MiB/s。WBWV 與 WIOPS 控制寫入部分，總量還會按 WRBWR／WRIOPSR 加權；不能把 total 限制只當 read limit。

**常見誤解。** 未替某 target 設 limits 時，其 limits 是 vendor-specific；不能把缺少設定解讀為無限制。§5.10 開頭的 Hard／Soft 小節引用對調，正確是 5.10.1 Hard、5.10.2 Soft。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 未替某 target 設 limits 時，其 limits 是 vendor-specific；不能把缺少設定解讀為無限制。§5.10 開頭的 Hard／Soft 小節引用對調，正確是 5.10.1 Hard、5.10.2 Soft。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** RLE, RLM, BWSF, TBWV, WBWV, TIOPS, WIOPS, WRIOPSR, WRBWR

**來源 keyword 索引：** shall, may, optional, mandatory, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.9, Figure 107, 文件頁 74-75, PDF 頁 74-75

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 108: Bandwidth Scale Factors</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-108-CLAIM figure-table:NVMCS13-NVM-FIG-108 -->

**SPEC。** Figure 108〈Bandwidth Scale Factors〉：共同 scale 表供設定、maximum 與 available bandwidth 使用；0..2 是 MiB/s 階梯，3..5 是 GiB/s 階梯。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

共同 scale 表供設定、maximum 與 available bandwidth 使用；0..2 是 MiB/s 階梯，3..5 是 GiB/s 階梯。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: BWSF]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `BWSF` | Bandwidth Scale Factor；需乘 bandwidth value，單位為 MiB/s 或 GiB/s。 |
| `相關欄位` | MBSF, ABWSF — 共同 scale 表供設定、maximum 與 available bandwidth 使用；0..2 是 MiB/s 階梯，3..5 是 GiB/s 階梯。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 共同 scale 表供設定、maximum 與 available bandwidth 使用；0..2 是 MiB/s 階梯，3..5 是 GiB/s 階梯。
3. 先從 LID 28h 取得支援 target，再檢查 HLS／SLS 與 soft-controller 數量。把 host 請求限制和裝置可達能力分開記錄。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 108 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.3.9 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 共同 scale 表供設定、maximum 與 available bandwidth 使用；0..2 是 MiB/s 階梯，3..5 是 GiB/s 階梯。 |
| 邊界 | 未替某 target 設 limits 時，其 limits 是 vendor-specific；不能把缺少設定解讀為無限制。§5.10 開頭的 Hard／Soft 小節引用對調，正確是 5.10.1 Hard、5.10.2 Soft。 |

**說明性範例。** BWSF=1、TBWV=50 表示 500 MiB/s。WBWV 與 WIOPS 控制寫入部分，總量還會按 WRBWR／WRIOPSR 加權；不能把 total 限制只當 read limit。

**常見誤解。** 未替某 target 設 limits 時，其 limits 是 vendor-specific；不能把缺少設定解讀為無限制。§5.10 開頭的 Hard／Soft 小節引用對調，正確是 5.10.1 Hard、5.10.2 Soft。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 未替某 target 設 limits 時，其 limits 是 vendor-specific；不能把缺少設定解讀為無限制。§5.10 開頭的 Hard／Soft 小節引用對調，正確是 5.10.1 Hard、5.10.2 Soft。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** BWSF, MBSF, ABWSF

**來源 keyword 索引：** shall, may, optional, mandatory, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.9, Figure 108, 文件頁 75, PDF 頁 75

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 109: Get Log Page – Log Page Identifiers</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-109-CLAIM figure-table:NVMCS13-NVM-FIG-109 -->

**SPEC。** Figure 109〈Get Log Page – Log Page Identifiers〉：log 表列出 NVM 補充及 scope／CSI；28h 使用 CSI，restore-to-default 欄也不能當成一般 reset persistence。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

log 表列出 NVM 補充及 scope／CSI；28h 使用 CSI，restore-to-default 欄也不能當成一般 reset persistence。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LID]
          ↓
[擷取欄位: CSI] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LID` | 分別選 Feature、log page、I/O command set 與 Identify 回傳資料結構；數值不能跨識別空間混用。 |
| `CSI` | 分別選 Feature、log page、I/O command set 與 Identify 回傳資料結構；數值不能跨識別空間混用。 |
| `相關欄位` | Scope, Restore behavior — log 表列出 NVM 補充及 scope／CSI；28h 使用 CSI，restore-to-default 欄也不能當成一般 reset persistence。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. log 表列出 NVM 補充及 scope／CSI；28h 使用 CSI，restore-to-default 欄也不能當成一般 reset persistence。
3. 用事件找調查方向，再用正確 scope 的 log 與 command set 定義解碼。統計數據也要依命令分類，不能只按 opcode 名稱猜。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 109 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | log 表列出 NVM 補充及 scope／CSI；28h 使用 CSI，restore-to-default 欄也不能當成一般 reset persistence。 |
| 邊界 | Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。 |

**說明性範例。** 一個 Self-test FLBA=100、valid=1 的紀錄只能定位一個失敗 LBA，不能據此宣告其他 LBAs 全部正常。Error Information LBA=100 的「最低」語意也不能直接套到 FLBA。

**常見誤解。** Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LID, CSI, Scope, Restore behavior

**來源 keyword 索引：** shall, may, optional, mandatory, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4, Figure 109, 文件頁 75-76, PDF 頁 75-76

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 110: Error Information Log Entry Data Structure – User Data</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-110-CLAIM figure-table:NVMCS13-NVM-FIG-110 -->

**SPEC。** Figure 110〈Error Information Log Entry Data Structure – User Data〉：Error Information bytes23:16 是適用時最低錯誤 LBA；需與原命令與 namespace 相連，不當成全 subsystem 的 byte address。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Error Information bytes23:16 是適用時最低錯誤 LBA；需與原命令與 namespace 相連，不當成全 subsystem 的 byte address。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBA]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBA` | Logical Block Address；以所選格式的 block 為單位。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Error Information bytes23:16 是適用時最低錯誤 LBA；需與原命令與 namespace 相連，不當成全 subsystem 的 byte address。
3. 用事件找調查方向，再用正確 scope 的 log 與 command set 定義解碼。統計數據也要依命令分類，不能只按 opcode 名稱猜。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 110 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.4.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Error Information bytes23:16 是適用時最低錯誤 LBA；需與原命令與 namespace 相連，不當成全 subsystem 的 byte address。 |
| 邊界 | Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。 |

**說明性範例。** 一個 Self-test FLBA=100、valid=1 的紀錄只能定位一個失敗 LBA，不能據此宣告其他 LBAs 全部正常。Error Information LBA=100 的「最低」語意也不能直接套到 FLBA。

**常見誤解。** Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LBA

**來源 keyword 索引：** shall

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.1, Figure 110, 文件頁 76, PDF 頁 76

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 111: Self-test Results Data Structure</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-111-CLAIM figure-table:NVMCS13-NVM-FIG-111 -->

**SPEC。** Figure 111〈Self-test Results Data Structure〉：FLBA 只有 valid bit=1 時可用；多個失敗 blocks 時只需回一個，與 Error Information 的最低 LBA 定義不同。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

FLBA 只有 valid bit=1 時可用；多個失敗 blocks 時只需回一個，與 Error Information 的最低 LBA 定義不同。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | FLBA, FLBA Valid — FLBA 只有 valid bit=1 時可用；多個失敗 blocks 時只需回一個，與 Error Information 的最低 LBA 定義不同。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. FLBA 只有 valid bit=1 時可用；多個失敗 blocks 時只需回一個，與 Error Information 的最低 LBA 定義不同。
3. 用事件找調查方向，再用正確 scope 的 log 與 command set 定義解碼。統計數據也要依命令分類，不能只按 opcode 名稱猜。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 111 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.4.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | FLBA 只有 valid bit=1 時可用；多個失敗 blocks 時只需回一個，與 Error Information 的最低 LBA 定義不同。 |
| 邊界 | Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。 |

**說明性範例。** 一個 Self-test FLBA=100、valid=1 的紀錄只能定位一個失敗 LBA，不能據此宣告其他 LBAs 全部正常。Error Information LBA=100 的「最低」語意也不能直接套到 FLBA。

**常見誤解。** Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** FLBA, FLBA Valid

**來源 keyword 索引：** shall

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, Figure 111, 文件頁 76, PDF 頁 76

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 112: Change Namespace Event Data Format (Event Type 06h)</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-112-CLAIM figure-table:NVMCS13-NVM-FIG-112 -->

**SPEC。** Figure 112〈Change Namespace Event Data Format (Event Type 06h)〉：create 取 host-specified values，single delete 取被刪 namespace 的 Identify 值；delete all 時兩欄 reserved。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

create 取 host-specified values，single delete 取被刪 namespace 的 Identify 值；delete all 時兩欄 reserved。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | FLBAS, DPS — create 取 host-specified values，single delete 取被刪 namespace 的 Identify 值；delete all 時兩欄 reserved。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. create 取 host-specified values，single delete 取被刪 namespace 的 Identify 值；delete all 時兩欄 reserved。
3. 用事件找調查方向，再用正確 scope 的 log 與 command set 定義解碼。統計數據也要依命令分類，不能只按 opcode 名稱猜。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 112 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.4.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | create 取 host-specified values，single delete 取被刪 namespace 的 Identify 值；delete all 時兩欄 reserved。 |
| 邊界 | Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。 |

**說明性範例。** 一個 Self-test FLBA=100、valid=1 的紀錄只能定位一個失敗 LBA，不能據此宣告其他 LBAs 全部正常。Error Information LBA=100 的「最低」語意也不能直接套到 FLBA。

**常見誤解。** Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** FLBAS, DPS

**來源 keyword 索引：** shall not, shall, should not, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.4, Figure 112, 文件頁 77, PDF 頁 77

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 113: LBA Status Information Log Page</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-113-CLAIM figure-table:NVMCS13-NVM-FIG-113 -->

**SPEC。** Figure 113〈LBA Status Information Log Page〉：先讀 bytes 長度與 namespace-element 數；NLSLNE=0 且 ESTULB 非零仍有需調查範圍，LSGC 是 16-bit 可回繞 counter。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

先讀 bytes 長度與 namespace-element 數；NLSLNE=0 且 ESTULB 非零仍有需調查範圍，LSGC 是 16-bit 可回繞 counter。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | LSLPLEN, NLSLNE, ESTULB, LSGC — 先讀 bytes 長度與 namespace-element 數；NLSLNE=0 且 ESTULB 非零仍有需調查範圍，LSGC 是 16-bit 可回繞 counter。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 先讀 bytes 長度與 namespace-element 數；NLSLNE=0 且 ESTULB 非零仍有需調查範圍，LSGC 是 16-bit 可回繞 counter。
3. 讀到 potentially unrecoverable 不是每個 block 一定無法讀取。先辨識 ATYPE，再檢查 buffer 是否足夠與 completion condition，最後安排資料修復。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 113 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.4.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 先讀 bytes 長度與 namespace-element 數；NLSLNE=0 且 ESTULB 非零仍有需調查範圍，LSGC 是 16-bit 可回繞 counter。 |
| 邊界 | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

**說明性範例。** log 有 NLSLNE=0 但 ESTULB 非零時，不能當作沒有問題，宜檢查 attached namespaces 的完整 LBA 範圍。取得可疑 LBAs 後，可從其他可靠來源恢復並寫回；後續查詢會移除成功重寫且未再偵測的項目。

**常見誤解。** CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LSLPLEN, NLSLNE, ESTULB, LSGC

**來源 keyword 索引：** shall not, shall, should not, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.5, Figure 113, 文件頁 77-78, PDF 頁 77-78

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 114: LBA Status Log Namespace Element</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-114-CLAIM figure-table:NVMCS13-NVM-FIG-114 -->

**SPEC。** Figure 114〈LBA Status Log Namespace Element〉：NEID 定位 namespace，RATYPE 建議後續 Get LBA Status 的 ATYPE；NLRD=FFFFFFFFh 表示無 range list 且宜檢查全 namespace。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

NEID 定位 namespace，RATYPE 建議後續 Get LBA Status 的 ATYPE；NLRD=FFFFFFFFh 表示無 range list 且宜檢查全 namespace。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | NEID, NLRD, RATYPE — NEID 定位 namespace，RATYPE 建議後續 Get LBA Status 的 ATYPE；NLRD=FFFFFFFFh 表示無 range list 且宜檢查全 namespace。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. NEID 定位 namespace，RATYPE 建議後續 Get LBA Status 的 ATYPE；NLRD=FFFFFFFFh 表示無 range list 且宜檢查全 namespace。
3. 讀到 potentially unrecoverable 不是每個 block 一定無法讀取。先辨識 ATYPE，再檢查 buffer 是否足夠與 completion condition，最後安排資料修復。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 114 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.4.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | NEID 定位 namespace，RATYPE 建議後續 Get LBA Status 的 ATYPE；NLRD=FFFFFFFFh 表示無 range list 且宜檢查全 namespace。 |
| 邊界 | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

**說明性範例。** log 有 NLSLNE=0 但 ESTULB 非零時，不能當作沒有問題，宜檢查 attached namespaces 的完整 LBA 範圍。取得可疑 LBAs 後，可從其他可靠來源恢復並寫回；後續查詢會移除成功重寫且未再偵測的項目。

**常見誤解。** CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NEID, NLRD, RATYPE

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.5, Figure 114, 文件頁 78, PDF 頁 78

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 115: LBA Range Descriptor</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-115-CLAIM figure-table:NVMCS13-NVM-FIG-115 -->

**SPEC。** Figure 115〈LBA Range Descriptor〉：每筆 16-byte range 用 RSLBA 與 0-based RNLB；它是 log 提供的粗範圍，還不是 Get LBA Status 的最終 status descriptor。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

每筆 16-byte range 用 RSLBA 與 0-based RNLB；它是 log 提供的粗範圍，還不是 Get LBA Status 的最終 status descriptor。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: RNLB]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `RNLB` | LBA Status log 的 Range Number of Logical Blocks；0-based。 |
| `相關欄位` | RSLBA — 每筆 16-byte range 用 RSLBA 與 0-based RNLB；它是 log 提供的粗範圍，還不是 Get LBA Status 的最終 status descriptor。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 每筆 16-byte range 用 RSLBA 與 0-based RNLB；它是 log 提供的粗範圍，還不是 Get LBA Status 的最終 status descriptor。
3. 讀到 potentially unrecoverable 不是每個 block 一定無法讀取。先辨識 ATYPE，再檢查 buffer 是否足夠與 completion condition，最後安排資料修復。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 115 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.4.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 每筆 16-byte range 用 RSLBA 與 0-based RNLB；它是 log 提供的粗範圍，還不是 Get LBA Status 的最終 status descriptor。 |
| 邊界 | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

**說明性範例。** log 有 NLSLNE=0 但 ESTULB 非零時，不能當作沒有問題，宜檢查 attached namespaces 的完整 LBA 範圍。取得可疑 LBAs 後，可從其他可靠來源恢復並寫回；後續查詢會移除成功重寫且未再偵測的項目。

**常見誤解。** CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** RSLBA, RNLB

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.5, Figure 115, 文件頁 78, PDF 頁 78

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 116: Media Reallocated - Event Type Specific Data Structure</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-116-CLAIM figure-table:NVMCS13-NVM-FIG-116 -->

**SPEC。** Figure 116〈Media Reallocated - Event Type Specific Data Structure〉：先驗 LBAV 再使用 LBA；NLBAM=0 未回報數量、FFFFh 表示至少該數量，不是一定恰好搬移 65535 blocks。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

先驗 LBAV 再使用 LBA；NLBAM=0 未回報數量、FFFFh 表示至少該數量，不是一定恰好搬移 65535 blocks。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBAV]
          ↓
[擷取欄位: LBA] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBAV` | LBA Valid 與 LBA Range Status；先驗資料是否有效，再依 Action Type 解讀狀態。 |
| `LBA` | Logical Block Address；以所選格式的 block 為單位。 |
| `相關欄位` | NLBAM — 先驗 LBAV 再使用 LBA；NLBAM=0 未回報數量、FFFFh 表示至少該數量，不是一定恰好搬移 65535 blocks。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 先驗 LBAV 再使用 LBA；NLBAM=0 未回報數量、FFFFh 表示至少該數量，不是一定恰好搬移 65535 blocks。
3. 建立時決定 placement 關係，執行時看 handle status，事後再用 statistics／events 解釋媒體搬移。三種資料不能互相代替。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 116 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.4.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 先驗 LBAV 再使用 LBA；NLBAM=0 未回報數量、FFFFh 表示至少該數量，不是一定恰好搬移 65535 blocks。 |
| 邊界 | Media Reallocated event 的 LBA 是搬移集合中的一個 LBA，並不是完整清單；LBAV=0 時必須忽略。 |

**說明性範例。** 兩個 namespaces 共享 RUH 5，第一個使用 FIDX=2，第二個 create 指定 FIDX=3，即使資料大小同為 4 KiB，也不符合共享 RUH 的 Format Index 條件。

**常見誤解。** Media Reallocated event 的 LBA 是搬移集合中的一個 LBA，並不是完整清單；LBAV=0 時必須忽略。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Media Reallocated event 的 LBA 是搬移集合中的一個 LBA，並不是完整清單；LBAV=0 時必須忽略。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LBAV, NLBAM, LBA

**來源 keyword 索引：** shall not, shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.7, Figure 116, 文件頁 79, PDF 頁 79

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 117: Rate Limiting Log Page</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-117-CLAIM figure-table:NVMCS13-NVM-FIG-117 -->

**SPEC。** Figure 117〈Rate Limiting Log Page〉：NP／NST 是 0-based，LPL 是 dwords，port 指標也以 log 起點的 dwords 表示；讀完整 log 後重驗 GC。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

NP／NST 是 0-based，LPL 是 dwords，port 指標也以 log 起點的 dwords 表示；讀完整 log 後重驗 GC。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NP]
          ↓
[擷取欄位: LPL] → [套用編碼: GC]
                                      ↓
[驗證證據: 相關欄位]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NP` | Rate Limiting log 的 port／controller 數，皆採 0-based。 |
| `LPL` | Rate Limiting Log Page Length；單位是 dwords，讀取 bytes 前乘 4 並檢查邊界。 |
| `GC` | Rate Limiting log 的 32-bit Generation Count，用於分段讀取一致性。 |
| `相關欄位` | NST, Port offsets — NP／NST 是 0-based，LPL 是 dwords，port 指標也以 log 起點的 dwords 表示；讀完整 log 後重驗 GC。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. NP／NST 是 0-based，LPL 是 dwords，port 指標也以 log 起點的 dwords 表示；讀完整 log 後重驗 GC。
3. 先做結構邊界檢查，再分析 bandwidth bottleneck。Port 的能力與共同 Endurance Group 的能力不同，不能把所有數字直接相加。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 117 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.4.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | NP／NST 是 0-based，LPL 是 dwords，port 指標也以 log 起點的 dwords 表示；讀完整 log 後重驗 GC。 |
| 邊界 | Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。 |

**說明性範例。** 兩個 PCIe ports 都能使用一個 Endurance Group，若 EG 的 bandwidth 已被 controller 0 用滿，controller 1 不會因多一個 port 就多一份媒體頻寬。相同 EG 能力可由兩個 controller 指向同一 descriptor。

**常見誤解。** Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NP, LPL, GC, NST, Port offsets

**來源 keyword 索引：** shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8, Figure 117, 文件頁 80, PDF 頁 80

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 118: Rate Limiting Port Descriptor</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-118-CLAIM figure-table:NVMCS13-NVM-FIG-118 -->

**SPEC。** Figure 118〈Rate Limiting Port Descriptor〉：port descriptor 的 available 指尚未分配額度，與 RLMA 的 maximum 不同；controller-list offset 仍相對整份 log。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

port descriptor 的 available 指尚未分配額度，與 RLMA 的 maximum 不同；controller-list offset 仍相對整份 log。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NC]
          ↓
[擷取欄位: RLMA] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NC` | Rate Limiting log 的 port／controller 數，皆採 0-based。 |
| `RLMA` | Rate Limiting Maximum Access；所述 port、controller 或 storage access 的最大能力，不是目前流量。 |
| `相關欄位` | PORTID, ARBWV, AWBWV, ARIOPS, AWIOPS — port descriptor 的 available 指尚未分配額度，與 RLMA 的 maximum 不同；controller-list offset 仍相對整份 log。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. port descriptor 的 available 指尚未分配額度，與 RLMA 的 maximum 不同；controller-list offset 仍相對整份 log。
3. 先做結構邊界檢查，再分析 bandwidth bottleneck。Port 的能力與共同 Endurance Group 的能力不同，不能把所有數字直接相加。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 118 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.4.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | port descriptor 的 available 指尚未分配額度，與 RLMA 的 maximum 不同；controller-list offset 仍相對整份 log。 |
| 邊界 | Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。 |

**說明性範例。** 兩個 PCIe ports 都能使用一個 Endurance Group，若 EG 的 bandwidth 已被 controller 0 用滿，controller 1 不會因多一個 port 就多一份媒體頻寬。相同 EG 能力可由兩個 controller 指向同一 descriptor。

**常見誤解。** Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** PORTID, NC, RLMA, ARBWV, AWBWV, ARIOPS, AWIOPS

**來源 keyword 索引：** shall not, shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8, Figure 118, 文件頁 80-81, PDF 頁 80-81

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 119: Rate Limiting Controller Descriptor</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-119-CLAIM figure-table:NVMCS13-NVM-FIG-119 -->

**SPEC。** Figure 119〈Rate Limiting Controller Descriptor〉：controller descriptor 以實際 NNSMAD 指出 access descriptors 數；這個 count 不採 NP／NC 的加一規則。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

controller descriptor 以實際 NNSMAD 指出 access descriptors 數；這個 count 不採 NP／NC 的加一規則。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NNSMAD]
          ↓
[擷取欄位: RLMA] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NNSMAD` | Non-Volatile Storage Medium Access Descriptors 數；實際數量，零表示此節點沒有下游 descriptors。 |
| `RLMA` | Rate Limiting Maximum Access；所述 port、controller 或 storage access 的最大能力，不是目前流量。 |
| `相關欄位` | CNTLID, Access offsets — controller descriptor 以實際 NNSMAD 指出 access descriptors 數；這個 count 不採 NP／NC 的加一規則。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. controller descriptor 以實際 NNSMAD 指出 access descriptors 數；這個 count 不採 NP／NC 的加一規則。
3. 先做結構邊界檢查，再分析 bandwidth bottleneck。Port 的能力與共同 Endurance Group 的能力不同，不能把所有數字直接相加。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 119 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.4.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | controller descriptor 以實際 NNSMAD 指出 access descriptors 數；這個 count 不採 NP／NC 的加一規則。 |
| 邊界 | Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。 |

**說明性範例。** 兩個 PCIe ports 都能使用一個 Endurance Group，若 EG 的 bandwidth 已被 controller 0 用滿，controller 1 不會因多一個 port 就多一份媒體頻寬。相同 EG 能力可由兩個 controller 指向同一 descriptor。

**常見誤解。** Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** CNTLID, NNSMAD, RLMA, Access offsets

**來源 keyword 索引：** shall not, shall, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8, Figure 119, 文件頁 81, PDF 頁 81

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 120: Non-Volatile Storage Medium Access Descriptor</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-120-CLAIM figure-table:NVMCS13-NVM-FIG-120 -->

**SPEC。** Figure 120〈Non-Volatile Storage Medium Access Descriptor〉：先以 SC 選 scope 再解讀 SI 與巢狀 access list；本表 SI 說明仍提 NSET 且 byte 例子錯置，應以 SC 與表列 bytes7:4 定位。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

先以 SC 選 scope 再解讀 SI 與巢狀 access list；本表 SI 說明仍提 NSET 且 byte 例子錯置，應以 SC 與表列 bytes7:4 定位。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SC]
          ↓
[擷取欄位: NNSMAD] → [套用編碼: RLMA]
                                      ↓
[驗證證據: 相關欄位]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SC` | Status Code Type 與 Status Code；兩欄共同識別錯誤，單看 SC 可能誤判。 |
| `NNSMAD` | Non-Volatile Storage Medium Access Descriptors 數；實際數量，零表示此節點沒有下游 descriptors。 |
| `RLMA` | Rate Limiting Maximum Access；所述 port、controller 或 storage access 的最大能力，不是目前流量。 |
| `相關欄位` | SI — 先以 SC 選 scope 再解讀 SI 與巢狀 access list；本表 SI 說明仍提 NSET 且 byte 例子錯置，應以 SC 與表列 bytes7:4 定位。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 先以 SC 選 scope 再解讀 SI 與巢狀 access list；本表 SI 說明仍提 NSET 且 byte 例子錯置，應以 SC 與表列 bytes7:4 定位。
3. 先做結構邊界檢查，再分析 bandwidth bottleneck。Port 的能力與共同 Endurance Group 的能力不同，不能把所有數字直接相加。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 120 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.4.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 先以 SC 選 scope 再解讀 SI 與巢狀 access list；本表 SI 說明仍提 NSET 且 byte 例子錯置，應以 SC 與表列 bytes7:4 定位。 |
| 邊界 | Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。 |

**說明性範例。** 兩個 PCIe ports 都能使用一個 Endurance Group，若 EG 的 bandwidth 已被 controller 0 用滿，controller 1 不會因多一個 port 就多一份媒體頻寬。相同 EG 能力可由兩個 controller 指向同一 descriptor。

**常見誤解。** Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SC, SI, NNSMAD, RLMA

**來源 keyword 索引：** shall not, shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8, Figure 120, 文件頁 81-82, PDF 頁 81-82

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 121: Rate Limiting Maximum Access Descriptor</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-121-CLAIM figure-table:NVMCS13-NVM-FIG-121 -->

**SPEC。** Figure 121〈Rate Limiting Maximum Access Descriptor〉：以 MBSF 轉 bandwidth；四個 maximum 需配合 workload size 與 queue depth，不能當成任意 workload 的最低保證。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

以 MBSF 轉 bandwidth；四個 maximum 需配合 workload size 與 queue depth，不能當成任意 workload 的最低保證。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | MBSF, MRBWV, MWBWV, MRIOPS, MWIOPS — 以 MBSF 轉 bandwidth；四個 maximum 需配合 workload size 與 queue depth，不能當成任意 workload 的最低保證。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 以 MBSF 轉 bandwidth；四個 maximum 需配合 workload size 與 queue depth，不能當成任意 workload 的最低保證。
3. 先做結構邊界檢查，再分析 bandwidth bottleneck。Port 的能力與共同 Endurance Group 的能力不同，不能把所有數字直接相加。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 121 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.4.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 以 MBSF 轉 bandwidth；四個 maximum 需配合 workload size 與 queue depth，不能當成任意 workload 的最低保證。 |
| 邊界 | Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。 |

**說明性範例。** 兩個 PCIe ports 都能使用一個 Endurance Group，若 EG 的 bandwidth 已被 controller 0 用滿，controller 1 不會因多一個 port 就多一份媒體頻寬。相同 EG 能力可由兩個 controller 指向同一 descriptor。

**常見誤解。** Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** MBSF, MRBWV, MWBWV, MRIOPS, MWIOPS

**來源 keyword 索引：** shall not, shall, should, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8, Figure 121, 文件頁 82-83, PDF 頁 82-83

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 122: CNS Values</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-122-CLAIM figure-table:NVMCS13-NVM-FIG-122 -->

**SPEC。** Figure 122〈CNS Values〉：以 CNS 選資料結構，再看 NSID／CSI 是否使用；00h、05h、08h 的 namespace 資訊互補，09h／0Ah 用 FIDX。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

以 CNS 選資料結構，再看 NSID／CSI 是否使用；00h、05h、08h 的 namespace 資訊互補，09h／0Ah 用 FIDX。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CNS]
          ↓
[擷取欄位: NSID] → [套用編碼: CSI]
                                      ↓
[驗證證據: 相關欄位]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CNS` | 分別選 Feature、log page、I/O command set 與 Identify 回傳資料結構；數值不能跨識別空間混用。 |
| `NSID` | Namespace 識別碼；SNSID 選 Copy 來源，ENSID 選匯出 namespace，合法值受個別命令約束。 |
| `CSI` | 分別選 Feature、log page、I/O command set 與 Identify 回傳資料結構；數值不能跨識別空間混用。 |
| `相關欄位` | CNTID — 以 CNS 選資料結構，再看 NSID／CSI 是否使用；00h、05h、08h 的 namespace 資訊互補，09h／0Ah 用 FIDX。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 以 CNS 選資料結構，再看 NSID／CSI 是否使用；00h、05h、08h 的 namespace 資訊互補，09h／0Ah 用 FIDX。
3. 每次查詢都寫出 CNS、CSI、NSID、Format Index 的角色。不同查詢回零有不同含義，不能一律解讀為不存在或不支援。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 122 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 以 CNS 選資料結構，再看 NSID／CSI 是否使用；00h、05h、08h 的 namespace 資訊互補，09h／0Ah 用 FIDX。 |
| 邊界 | §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。 |

**說明性範例。** NSID=7 的目前格式需讀 FLBAS 再取同 index 的 LBAF 與 ELBAF。查尚未建立的 FIDX=3 能力，使用 09h／0Ah、CSI=0、NSID=0、FIDX=3，另結合 CNS08h 的共同能力。

**常見誤解。** §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** CNS, NSID, CSI, CNTID

**來源 keyword 索引：** shall not, shall, may, optional, mandatory

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5, Figure 122, 文件頁 83-84, PDF 頁 83-84

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 123: Identify – Identify Namespace Data Structure, NVM Command Set</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-123-CLAIM figure-table:NVMCS13-NVM-FIG-123 -->

**SPEC。** Figure 123〈Identify – Identify Namespace Data Structure, NVM Command Set〉：把這張跨頁資料結構分成容量、格式能力／目前格式、deallocation、atomicity、performance、Copy limits 與識別資料七組；每組先看 capability gate 再使用數值。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

把這張跨頁資料結構分成容量、格式能力／目前格式、deallocation、atomicity、performance、Copy limits 與識別資料七組；每組先看 capability gate 再使用數值。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSZE]
          ↓
[擷取欄位: NCAP] → [套用編碼: NUSE]
                                      ↓
[驗證證據: NLBAF]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSZE` | Namespace Size；可定址 logical blocks 總數。 |
| `NCAP` | Namespace Capacity；同時可配置 logical blocks 最大數量。 |
| `NUSE` | Namespace Utilization；目前配置 logical blocks 數量。 |
| `NLBAF` | 共同屬性 LBA formats 數的 0-based 欄位。 |
| `相關欄位` | NSFEAT, FLBAS, MC, DPC, DPS, DLFEAT, Atomicity, Performance hints, Copy limits, Identifiers — 把這張跨頁資料結構分成容量、格式能力／目前格式、deallocation、atomicity、performance、Copy limits 與識別資料七組；每組先看 capability gate 再使用數值。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 把這張跨頁資料結構分成容量、格式能力／目前格式、deallocation、atomicity、performance、Copy limits 與識別資料七組；每組先看 capability gate 再使用數值。
3. 先區分 logical address space 與實際配置，再分析寫入及 deallocate。讀取值與 allocation 狀態回答不同問題。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 123 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.5.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 把這張跨頁資料結構分成容量、格式能力／目前格式、deallocation、atomicity、performance、Copy limits 與識別資料七組；每組先看 capability gate 再使用數值。 |
| 邊界 | ANA 狀態可使 NUSE／NVMCAP 回零；不可僅憑回零宣告資料已刪除。 |

**說明性範例。** NSZE=1000、NCAP=800、NUSE=600 可是合法 thin namespace。LBA 900 在可定址範圍內，但新增配置仍受 800-block capacity 限制。

**常見誤解。** ANA 狀態可使 NUSE／NVMCAP 回零；不可僅憑回零宣告資料已刪除。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | ANA 狀態可使 NUSE／NVMCAP 回零；不可僅憑回零宣告資料已刪除。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NSZE, NCAP, NUSE, NSFEAT, NLBAF, FLBAS, MC, DPC, DPS, DLFEAT, Atomicity, Performance hints, Copy limits, Identifiers

**來源 keyword 索引：** shall not, shall, should, may, optional, mandatory, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1, Figure 123, 文件頁 85-93, PDF 頁 85-93

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 124: Namespace Alignment and Granularity Attributes</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-124-CLAIM figure-table:NVMCS13-NVM-FIG-124 -->

**SPEC。** Figure 124〈Namespace Alignment and Granularity Attributes〉：OPTPERF 是 2-bit selector：不同值啟用不同 small／large deallocate 欄位組；不是一個通用的 performance enabled bit。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

OPTPERF 是 2-bit selector：不同值啟用不同 small／large deallocate 欄位組；不是一個通用的 performance enabled bit。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | OPTPERF, NPWG, NPWA, NPDG, NPDGL, NPDAL, NOWS — OPTPERF 是 2-bit selector：不同值啟用不同 small／large deallocate 欄位組；不是一個通用的 performance enabled bit。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. OPTPERF 是 2-bit selector：不同值啟用不同 small／large deallocate 欄位組；不是一個通用的 performance enabled bit。
3. 基本 entry 給資料／metadata 大小與相對效能，extended entry 給 PI 格式與 Storage Tag 分配。Unique-attribute entries 要個別查詢，不能沿用共同能力。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 124 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.5.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | OPTPERF 是 2-bit selector：不同值啟用不同 small／large deallocate 欄位組；不是一個通用的 performance enabled bit。 |
| 邊界 | LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。 |

**說明性範例。** raw NLBAF=3、NULBAF=2：有 4 個共同格式及 2 個唯一屬性格式，共 6 個，合法 index 為 0..5。Figure 192 圖示採概念数量，不能直接代入未解碼的 raw NLBAF。

**常見誤解。** LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** OPTPERF, NPWG, NPWA, NPDG, NPDGL, NPDAL, NOWS

**來源 keyword 索引：** shall, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1, Figure 124, 文件頁 94, PDF 頁 94

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 125: LBA Format Data Structure, NVM Command Set Specific</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-125-CLAIM figure-table:NVMCS13-NVM-FIG-125 -->

**SPEC。** Figure 125〈LBA Format Data Structure, NVM Command Set Specific〉：LBADS 為 exponent，MS 為實際 metadata bytes，RP 為相對效能級別；LBADS=0 是目前不可用，不能解成一個 byte 或 512 bytes。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

LBADS 為 exponent，MS 為實際 metadata bytes，RP 為相對效能級別；LBADS=0 是目前不可用，不能解成一個 byte 或 512 bytes。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBADS]
          ↓
[擷取欄位: MS] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBADS` | LBA Data Size 的 exponent；資料 bytes=2^LBADS，0表示目前不可用。 |
| `MS` | 每個 logical block 的 metadata bytes；與 PI size 比較以判斷 PRACT 的傳輸效果。 |
| `相關欄位` | RP — LBADS 為 exponent，MS 為實際 metadata bytes，RP 為相對效能級別；LBADS=0 是目前不可用，不能解成一個 byte 或 512 bytes。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. LBADS 為 exponent，MS 為實際 metadata bytes，RP 為相對效能級別；LBADS=0 是目前不可用，不能解成一個 byte 或 512 bytes。
3. 基本 entry 給資料／metadata 大小與相對效能，extended entry 給 PI 格式與 Storage Tag 分配。Unique-attribute entries 要個別查詢，不能沿用共同能力。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 125 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.5.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | LBADS 為 exponent，MS 為實際 metadata bytes，RP 為相對效能級別；LBADS=0 是目前不可用，不能解成一個 byte 或 512 bytes。 |
| 邊界 | LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。 |

**說明性範例。** raw NLBAF=3、NULBAF=2：有 4 個共同格式及 2 個唯一屬性格式，共 6 個，合法 index 為 0..5。Figure 192 圖示採概念数量，不能直接代入未解碼的 raw NLBAF。

**常見誤解。** LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LBADS, MS, RP

**來源 keyword 索引：** shall, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1, Figure 125, 文件頁 94, PDF 頁 94

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 126: Identify – Identify Controller data structure, NVM Command Set Specific Fields</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-126-CLAIM figure-table:NVMCS13-NVM-FIG-126 -->

**SPEC。** Figure 126〈Identify – Identify Controller data structure, NVM Command Set Specific Fields〉：controller atomicity 值供適用 namespaces 使用；namespace capability 可覆寫，AWUPF 不大於 AWUN，ACWU 專供 fused Compare-and-Write。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

controller atomicity 值供適用 namespaces 使用；namespace capability 可覆寫，AWUPF 不大於 AWUN，ACWU 專供 fused Compare-and-Write。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: AWUN]
          ↓
[擷取欄位: AWUPF] → [套用編碼: ACWU]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `AWUN` | Atomic Write Unit Normal；controller 正常原子寫入大小的 0-based 欄位。 |
| `AWUPF` | Atomic Write Unit Power Fail；失敗條件原子大小的0-based欄位。 |
| `ACWU` | Namespace normal／power-fail／compare-and-write 或 controller compare-and-write 原子大小；0-based。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. controller atomicity 值供適用 namespaces 使用；namespace capability 可覆寫，AWUPF 不大於 AWUN，ACWU 專供 fused Compare-and-Write。
3. 每次查詢都寫出 CNS、CSI、NSID、Format Index 的角色。不同查詢回零有不同含義，不能一律解讀為不存在或不支援。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 126 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.5.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | controller atomicity 值供適用 namespaces 使用；namespace capability 可覆寫，AWUPF 不大於 AWUN，ACWU 專供 fused Compare-and-Write。 |
| 邊界 | §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。 |

**說明性範例。** NSID=7 的目前格式需讀 FLBAS 再取同 index 的 LBAF 與 ELBAF。查尚未建立的 FIDX=3 能力，使用 09h／0Ah、CSI=0、NSID=0、FIDX=3，另結合 CNS08h 的共同能力。

**常見誤解。** §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** AWUN, AWUPF, ACWU

**來源 keyword 索引：** shall, may, optional, mandatory, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.2, Figure 126, 文件頁 94-96, PDF 頁 94-96

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 127: NVM Command Set I/O Command Set Specific Identify Namespace Data Structure</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-127-CLAIM figure-table:NVMCS13-NVM-FIG-127 -->

**SPEC。** Figure 127〈NVM Command Set I/O Command Set Specific Identify Namespace Data Structure〉：延伸 namespace 結構把 PI／mask 能力、每-format ELBAF 與性能／allocation hints 分開；NPRG／NPRA／NORS 受 OPTRPERF 限制。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

延伸 namespace 結構把 PI／mask 能力、每-format ELBAF 與性能／allocation hints 分開；NPRG／NPRA／NORS 受 OPTRPERF 限制。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBSTM]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBSTM` | Tag comparison mask；bit=0 排除比較，Storage mask 額外受支援與對齊限制。 |
| `相關欄位` | PIC, PIFA, ELBAF, NPDGL, NPRG, NPRA, NORS, NPDAL, LBAPSS, TLBAAG — 延伸 namespace 結構把 PI／mask 能力、每-format ELBAF 與性能／allocation hints 分開；NPRG／NPRA／NORS 受 OPTRPERF 限制。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 延伸 namespace 結構把 PI／mask 能力、每-format ELBAF 與性能／allocation hints 分開；NPRG／NPRA／NORS 受 OPTRPERF 限制。
3. 基本 entry 給資料／metadata 大小與相對效能，extended entry 給 PI 格式與 Storage Tag 分配。Unique-attribute entries 要個別查詢，不能沿用共同能力。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 127 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.5.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 延伸 namespace 結構把 PI／mask 能力、每-format ELBAF 與性能／allocation hints 分開；NPRG／NPRA／NORS 受 OPTRPERF 限制。 |
| 邊界 | LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。 |

**說明性範例。** raw NLBAF=3、NULBAF=2：有 4 個共同格式及 2 個唯一屬性格式，共 6 個，合法 index 為 0..5。Figure 192 圖示採概念数量，不能直接代入未解碼的 raw NLBAF。

**常見誤解。** LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LBSTM, PIC, PIFA, ELBAF, NPDGL, NPRG, NPRA, NORS, NPDAL, LBAPSS, TLBAAG

**來源 keyword 索引：** shall, should, may, optional, mandatory, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.3, Figure 127, 文件頁 97-101, PDF 頁 97-101

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 128: Extended LBA Format Data Structure, NVM Command Set Specific</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-128-CLAIM figure-table:NVMCS13-NVM-FIG-128 -->

**SPEC。** Figure 128〈Extended LBA Format Data Structure, NVM Command Set Specific〉：PIF=11b 且支援 QPIFS 才使用 QPIF；STS 是 bits count，切分固定寬度的 Storage/Reference Space，沒有增大 PI。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

PIF=11b 且支援 QPIFS 才使用 QPIF；STS 是 bits count，切分固定寬度的 Storage/Reference Space，沒有增大 PI。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: QPIF]
          ↓
[擷取欄位: PIF] → [套用編碼: STS]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `QPIF` | Protection Information Format selector；PIF 選一般格式，QPIF 提供 Qualified PI 的格式能力。 |
| `PIF` | Protection Information Format selector；PIF 選一般格式，QPIF 提供 Qualified PI 的格式能力。 |
| `STS` | Storage Tag Size；固定 Storage/Reference Space 中的高位 bit 數。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. PIF=11b 且支援 QPIFS 才使用 QPIF；STS 是 bits count，切分固定寬度的 Storage/Reference Space，沒有增大 PI。
3. 基本 entry 給資料／metadata 大小與相對效能，extended entry 給 PI 格式與 Storage Tag 分配。Unique-attribute entries 要個別查詢，不能沿用共同能力。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 128 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.5.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | PIF=11b 且支援 QPIFS 才使用 QPIF；STS 是 bits count，切分固定寬度的 Storage/Reference Space，沒有增大 PI。 |
| 邊界 | LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。 |

**說明性範例。** raw NLBAF=3、NULBAF=2：有 4 個共同格式及 2 個唯一屬性格式，共 6 個，合法 index 為 0..5。Figure 192 圖示採概念数量，不能直接代入未解碼的 raw NLBAF。

**常見誤解。** LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** QPIF, PIF, STS

**來源 keyword 索引：** shall not, shall, should, may, optional, mandatory, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.3, Figure 128, 文件頁 101-102, PDF 頁 101-102

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 129: I/O Command Set Specific Identify Controller Data Structure for the NVM Command Set</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-129-CLAIM figure-table:NVMCS13-NVM-FIG-129 -->

**SPEC。** Figure 129〈I/O Command Set Specific Identify Controller Data Structure for the NVM Command Set〉：本表實際延伸到文件頁106，不能只讀有 caption 的103頁。Size limits 要結合 ONCS variants；SLMC 是 0-based，VER 為 command-set 版本。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

本表實際延伸到文件頁106，不能只讀有 caption 的103頁。Size limits 要結合 ONCS variants；SLMC 是 0-based，VER 為 command-set 版本。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: VSL]
          ↓
[擷取欄位: WZSL] → [套用編碼: WUSL]
                                      ↓
[驗證證據: DMRL]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `VSL` | Verify／Write Zeroes／Write Uncorrectable 大小限制；非零值使用 exponent 與 minimum page size。 |
| `WZSL` | Verify／Write Zeroes／Write Uncorrectable 大小限制；非零值使用 exponent 與 minimum page size。 |
| `WUSL` | Verify／Write Zeroes／Write Uncorrectable 大小限制；非零值使用 exponent 與 minimum page size。 |
| `DMRL` | Dataset Management Ranges Limit，實際 range 數上限。 |
| `DMRSL` | DSM 單一 range／全命令 blocks 的 processing limit；與 DMRL 的 range 數限制分開。 |
| `DMSL` | DSM 單一 range／全命令 blocks 的 processing limit；與 DMRL 的 range 數限制分開。 |
| `WZDSL` | Write Zeroes with Deallocate 的專用大小限制；不可直接沿用 WZSL。 |
| `相關欄位` | KPIOCAP, AOCS, VER, LBAMQF, RLA, SLMC — 本表實際延伸到文件頁106，不能只讀有 caption 的103頁。Size limits 要結合 ONCS variants；SLMC 是 0-based，VER 為 command-set 版本。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 本表實際延伸到文件頁106，不能只讀有 caption 的103頁。Size limits 要結合 ONCS variants；SLMC 是 0-based，VER 為 command-set 版本。
3. 每次查詢都寫出 CNS、CSI、NSID、Format Index 的角色。不同查詢回零有不同含義，不能一律解讀為不存在或不支援。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 129 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.5.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 本表實際延伸到文件頁106，不能只讀有 caption 的103頁。Size limits 要結合 ONCS variants；SLMC 是 0-based，VER 為 command-set 版本。 |
| 邊界 | §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。 |

**說明性範例。** NSID=7 的目前格式需讀 FLBAS 再取同 index 的 LBAF 與 ELBAF。查尚未建立的 FIDX=3 能力，使用 09h／0Ah、CSI=0、NSID=0、FIDX=3，另結合 CNS08h 的共同能力。

**常見誤解。** §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** VSL, WZSL, WUSL, DMRL, DMRSL, DMSL, KPIOCAP, WZDSL, AOCS, VER, LBAMQF, RLA, SLMC

**來源 keyword 索引：** shall, should, optional, mandatory, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.4, Figure 129, 文件頁 103-106, PDF 頁 103-106

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 130: NVM Command Set Specification Version Descriptor Field Values</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-130-CLAIM figure-table:NVMCS13-NVM-FIG-130 -->

**SPEC。** Figure 130〈NVM Command Set Specification Version Descriptor Field Values〉：1.3 對應 MJR=1、MNR=3、TER=0；此為 NVM command-set version，與 Base version 另記。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

1.3 對應 MJR=1、MNR=3、TER=0；此為 NVM command-set version，與 Base version 另記。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | MJR, MNR, TER — 1.3 對應 MJR=1、MNR=3、TER=0；此為 NVM command-set version，與 Base version 另記。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 1.3 對應 MJR=1、MNR=3、TER=0；此為 NVM command-set version，與 Base version 另記。
3. 每次查詢都寫出 CNS、CSI、NSID、Format Index 的角色。不同查詢回零有不同含義，不能一律解讀為不存在或不支援。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 130 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.5.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 1.3 對應 MJR=1、MNR=3、TER=0；此為 NVM command-set version，與 Base version 另記。 |
| 邊界 | §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。 |

**說明性範例。** NSID=7 的目前格式需讀 FLBAS 再取同 index 的 LBAF 與 ELBAF。查尚未建立的 FIDX=3 能力，使用 09h／0Ah、CSI=0、NSID=0、FIDX=3，另結合 CNS08h 的共同能力。

**常見誤解。** §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** MJR, MNR, TER

**來源 keyword 索引：** shall

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.4, Figure 130, 文件頁 107, PDF 頁 107

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 131: Command Dword 11 - CNS Specific Identifiers</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-131-CLAIM figure-table:NVMCS13-NVM-FIG-131 -->

**SPEC。** Figure 131〈Command Dword 11 - CNS Specific Identifiers〉：CNS09h／0Ah 的 CDW11 low16 是 Format Index，不能同時當成某個 namespace ID；CSI 另選 command set。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CNS09h／0Ah 的 CDW11 low16 是 Format Index，不能同時當成某個 namespace ID；CSI 另選 command set。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | FIDX — CNS09h／0Ah 的 CDW11 low16 是 Format Index，不能同時當成某個 namespace ID；CSI 另選 command set。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CNS09h／0Ah 的 CDW11 low16 是 Format Index，不能同時當成某個 namespace ID；CSI 另選 command set。
3. 每次查詢都寫出 CNS、CSI、NSID、Format Index 的角色。不同查詢回零有不同含義，不能一律解讀為不存在或不支援。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 131 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.5.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CNS09h／0Ah 的 CDW11 low16 是 Format Index，不能同時當成某個 namespace ID；CSI 另選 command set。 |
| 邊界 | §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。 |

**說明性範例。** NSID=7 的目前格式需讀 FLBAS 再取同 index 的 LBAF 與 ELBAF。查尚未建立的 FIDX=3 能力，使用 09h／0Ah、CSI=0、NSID=0、FIDX=3，另結合 CNS08h 的共同能力。

**常見誤解。** §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** FIDX

**來源 keyword 索引：** shall

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.5, Figure 131, 文件頁 107, PDF 頁 107

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 132: Namespace Granularity List</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-132-CLAIM figure-table:NVMCS13-NVM-FIG-132 -->

**SPEC。** Figure 132〈Namespace Granularity List〉：GDM=0 時 descriptor0 套全部格式，ND=0；GDM=1 以相同 index 對應 format。ND 是 0-based，支援數量受 LBAFEE 影響。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

GDM=0 時 descriptor0 套全部格式，ND=0；GDM=1 以相同 index 對應 format。ND 是 0-based，支援數量受 LBAFEE 影響。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | GDM, ND, NGD — GDM=0 時 descriptor0 套全部格式，ND=0；GDM=1 以相同 index 對應 format。ND 是 0-based，支援數量受 LBAFEE 影響。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. GDM=0 時 descriptor0 套全部格式，ND=0；GDM=1 以相同 index 對應 format。ND 是 0-based，支援數量受 LBAFEE 影響。
3. 先取得 Format Index 能力再填 host-specified fields；不可直接把整份 Identify Namespace 原封不動當作 create payload。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 132 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.5.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | GDM=0 時 descriptor0 套全部格式，ND=0；GDM=1 以相同 index 對應 format。ND 是 0-based，支援數量受 LBAFEE 影響。 |
| 邊界 | Masking Not Supported 代表 Storage Tag mask 有效 bits 全為 1；不是全零。不支援或未啟用 FDP 時，placement 欄位也不能套用啟用後的語意。 |

**說明性範例。** 假設 NSG=1 MiB、NCG=1 MiB、logical block size=4096，NSZE=NCAP=256 的容量可完整定址；若改成 257，granularity hints 可能造成額外不可定址配置，但本身不是拒絕理由。

**常見誤解。** Masking Not Supported 代表 Storage Tag mask 有效 bits 全為 1；不是全零。不支援或未啟用 FDP 時，placement 欄位也不能套用啟用後的語意。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Masking Not Supported 代表 Storage Tag mask 有效 bits 全為 1；不是全零。不支援或未啟用 FDP 時，placement 欄位也不能套用啟用後的語意。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** GDM, ND, NGD

**來源 keyword 索引：** shall, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.8, Figure 132, 文件頁 108, PDF 頁 108

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 133: Namespace Granularity Descriptor</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-133-CLAIM figure-table:NVMCS13-NVM-FIG-133 -->

**SPEC。** Figure 133〈Namespace Granularity Descriptor〉：NSG／NCG 以 bytes 表示 preferred allocation granularity；0 表示未回報，不能拿來做除法或要求 namespace 大小為零。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

NSG／NCG 以 bytes 表示 preferred allocation granularity；0 表示未回報，不能拿來做除法或要求 namespace 大小為零。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | NSG, NCG — NSG／NCG 以 bytes 表示 preferred allocation granularity；0 表示未回報，不能拿來做除法或要求 namespace 大小為零。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. NSG／NCG 以 bytes 表示 preferred allocation granularity；0 表示未回報，不能拿來做除法或要求 namespace 大小為零。
3. 先取得 Format Index 能力再填 host-specified fields；不可直接把整份 Identify Namespace 原封不動當作 create payload。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 133 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.5.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | NSG／NCG 以 bytes 表示 preferred allocation granularity；0 表示未回報，不能拿來做除法或要求 namespace 大小為零。 |
| 邊界 | Masking Not Supported 代表 Storage Tag mask 有效 bits 全為 1；不是全零。不支援或未啟用 FDP 時，placement 欄位也不能套用啟用後的語意。 |

**說明性範例。** 假設 NSG=1 MiB、NCG=1 MiB、logical block size=4096，NSZE=NCAP=256 的容量可完整定址；若改成 257，granularity hints 可能造成額外不可定址配置，但本身不是拒絕理由。

**常見誤解。** Masking Not Supported 代表 Storage Tag mask 有效 bits 全為 1；不是全零。不支援或未啟用 FDP 時，placement 欄位也不能套用啟用後的語意。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Masking Not Supported 代表 Storage Tag mask 有效 bits 全為 1；不是全零。不支援或未啟用 FDP 時，placement 欄位也不能套用啟用後的語意。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NSG, NCG

**來源 keyword 索引：** shall, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.8, Figure 133, 文件頁 108, PDF 頁 108

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 134: Namespace Management – Host Specified Fields</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-134-CLAIM figure-table:NVMCS13-NVM-FIG-134 -->

**SPEC。** Figure 134〈Namespace Management – Host Specified Fields〉：Create payload 只有指定欄位可由 host 填寫；LBSTM／placement list 不在基本 Identify 相同區段，不能直接 memcpy 整份 Identify 結構。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Create payload 只有指定欄位可由 host 填寫；LBSTM／placement list 不在基本 Identify 相同區段，不能直接 memcpy 整份 Identify 結構。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSZE]
          ↓
[擷取欄位: NCAP] → [套用編碼: LBSTM]
                                      ↓
[驗證證據: 相關欄位]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSZE` | Namespace Size；可定址 logical blocks 總數。 |
| `NCAP` | Namespace Capacity；同時可配置 logical blocks 最大數量。 |
| `LBSTM` | Tag comparison mask；bit=0 排除比較，Storage mask 額外受支援與對齊限制。 |
| `相關欄位` | FLBAS, DPS, NMIC, ANAGRPID, NVMSETID, ENDGID, NPHNDLS, RUH list — Create payload 只有指定欄位可由 host 填寫；LBSTM／placement list 不在基本 Identify 相同區段，不能直接 memcpy 整份 Identify 結構。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Create payload 只有指定欄位可由 host 填寫；LBSTM／placement list 不在基本 Identify 相同區段，不能直接 memcpy 整份 Identify 結構。
3. 先取得 Format Index 能力再填 host-specified fields；不可直接把整份 Identify Namespace 原封不動當作 create payload。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 134 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.1.6.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Create payload 只有指定欄位可由 host 填寫；LBSTM／placement list 不在基本 Identify 相同區段，不能直接 memcpy 整份 Identify 結構。 |
| 邊界 | Masking Not Supported 代表 Storage Tag mask 有效 bits 全為 1；不是全零。不支援或未啟用 FDP 時，placement 欄位也不能套用啟用後的語意。 |

**說明性範例。** 假設 NSG=1 MiB、NCG=1 MiB、logical block size=4096，NSZE=NCAP=256 的容量可完整定址；若改成 257，granularity hints 可能造成額外不可定址配置，但本身不是拒絕理由。

**常見誤解。** Masking Not Supported 代表 Storage Tag mask 有效 bits 全為 1；不是全零。不支援或未啟用 FDP 時，placement 欄位也不能套用啟用後的語意。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Masking Not Supported 代表 Storage Tag mask 有效 bits 全為 1；不是全零。不支援或未啟用 FDP 時，placement 欄位也不能套用啟用後的語意。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NSZE, NCAP, FLBAS, DPS, NMIC, ANAGRPID, NVMSETID, ENDGID, LBSTM, NPHNDLS, RUH list

**來源 keyword 索引：** shall, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.4, Figure 134, 文件頁 112-113, PDF 頁 112-113

</details>

<a id="section-4-2"></a>

### §4.2

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 135: Get LBA Status – Data Pointer</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-135-CLAIM figure-table:NVMCS13-NVM-FIG-135 -->

**SPEC。** Figure 135〈Get LBA Status – Data Pointer〉：DPTR 是 controller 回傳資料的 host 目的位置；Read 回 data，Get LBA Status 回 descriptor list，兩者不可共用 payload parser。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

DPTR 是 controller 回傳資料的 host 目的位置；Read 回 data，Get LBA Status 回 descriptor list，兩者不可共用 payload parser。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

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
| `DPTR` | 命令 data pointer；Read 是目的、Write 是來源、Copy／DSM 指向 descriptors。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. DPTR 是 controller 回傳資料的 host 目的位置；Read 回 data，Get LBA Status 回 descriptor list，兩者不可共用 payload parser。
3. 讀到 potentially unrecoverable 不是每個 block 一定無法讀取。先辨識 ATYPE，再檢查 buffer 是否足夠與 completion condition，最後安排資料修復。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 135 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | DPTR 是 controller 回傳資料的 host 目的位置；Read 回 data，Get LBA Status 回 descriptor list，兩者不可共用 payload parser。 |
| 邊界 | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

**說明性範例。** log 有 NLSLNE=0 但 ESTULB 非零時，不能當作沒有問題，宜檢查 attached namespaces 的完整 LBA 範圍。取得可疑 LBAs 後，可從其他可靠來源恢復並寫回；後續查詢會移除成功重寫且未再偵測的項目。

**常見誤解。** CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DPTR

**來源 keyword 索引：** shall, optional, mandatory, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.2.1, Figure 135, 文件頁 114, PDF 頁 114

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 136: Get LBA Status – Command Dword 10 and Command Dword 11</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-136-CLAIM figure-table:NVMCS13-NVM-FIG-136 -->

**SPEC。** Figure 136〈Get LBA Status – Command Dword 10 and Command Dword 11〉：64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SLBA]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SLBA` | 範圍起始 LBA；SDLBA 選 Copy 目的，DSLBA 是 Get LBA Status descriptor 的起點。 |
| `相關欄位` | CDW10, CDW11 — 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。
3. 讀到 potentially unrecoverable 不是每個 block 一定無法讀取。先辨識 ATYPE，再檢查 buffer 是否足夠與 completion condition，最後安排資料修復。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 136 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。 |
| 邊界 | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

**說明性範例。** log 有 NLSLNE=0 但 ESTULB 非零時，不能當作沒有問題，宜檢查 attached namespaces 的完整 LBA 範圍。取得可疑 LBAs 後，可從其他可靠來源恢復並寫回；後續查詢會移除成功重寫且未再偵測的項目。

**常見誤解。** CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SLBA, CDW10, CDW11

**來源 keyword 索引：** shall, optional, mandatory, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.2.1, Figure 136, 文件頁 114, PDF 頁 114

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 137: Get LBA Status – Command Dword 12</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-137-CLAIM figure-table:NVMCS13-NVM-FIG-137 -->

**SPEC。** Figure 137〈Get LBA Status – Command Dword 12〉：MNDW 是 0-based 最大 dword 數；buffer bytes=(MNDW+1)×4，實際回量再看 NLSD。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

MNDW 是 0-based 最大 dword 數；buffer bytes=(MNDW+1)×4，實際回量再看 NLSD。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MNDW]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MNDW` | Maximum Number of Dwords；限制 Get LBA Status 回傳資料長度。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. MNDW 是 0-based 最大 dword 數；buffer bytes=(MNDW+1)×4，實際回量再看 NLSD。
3. 讀到 potentially unrecoverable 不是每個 block 一定無法讀取。先辨識 ATYPE，再檢查 buffer 是否足夠與 completion condition，最後安排資料修復。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 137 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | MNDW 是 0-based 最大 dword 數；buffer bytes=(MNDW+1)×4，實際回量再看 NLSD。 |
| 邊界 | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

**說明性範例。** log 有 NLSLNE=0 但 ESTULB 非零時，不能當作沒有問題，宜檢查 attached namespaces 的完整 LBA 範圍。取得可疑 LBAs 後，可從其他可靠來源恢復並寫回；後續查詢會移除成功重寫且未再偵測的項目。

**常見誤解。** CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** MNDW

**來源 keyword 索引：** shall, optional, mandatory, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.2.1, Figure 137, 文件頁 114, PDF 頁 114

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 138: Get LBA Status – Command Dword 13</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-138-CLAIM figure-table:NVMCS13-NVM-FIG-138 -->

**SPEC。** Figure 138〈Get LBA Status – Command Dword 13〉：ATYPE=02h／10h／11h 選 allocated／scan／tracked 行為；RL=0 是從 SLBA 到 namespace 最後 LBA，不是零長度。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

ATYPE=02h／10h／11h 選 allocated／scan／tracked 行為；RL=0 是從 SLBA 到 namespace 最後 LBA，不是零長度。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ATYPE]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ATYPE` | Get LBA Status Action Type；02h allocated，10h scan，11h tracked。 |
| `相關欄位` | RL — ATYPE=02h／10h／11h 選 allocated／scan／tracked 行為；RL=0 是從 SLBA 到 namespace 最後 LBA，不是零長度。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. ATYPE=02h／10h／11h 選 allocated／scan／tracked 行為；RL=0 是從 SLBA 到 namespace 最後 LBA，不是零長度。
3. 讀到 potentially unrecoverable 不是每個 block 一定無法讀取。先辨識 ATYPE，再檢查 buffer 是否足夠與 completion condition，最後安排資料修復。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 138 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | ATYPE=02h／10h／11h 選 allocated／scan／tracked 行為；RL=0 是從 SLBA 到 namespace 最後 LBA，不是零長度。 |
| 邊界 | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

**說明性範例。** log 有 NLSLNE=0 但 ESTULB 非零時，不能當作沒有問題，宜檢查 attached namespaces 的完整 LBA 範圍。取得可疑 LBAs 後，可從其他可靠來源恢復並寫回；後續查詢會移除成功重寫且未再偵測的項目。

**常見誤解。** CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** ATYPE, RL

**來源 keyword 索引：** shall not, shall, may, optional, mandatory, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.2.1, Figure 138, 文件頁 114-115, PDF 頁 114-115

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 139: LBA Status Descriptor List</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-139-CLAIM figure-table:NVMCS13-NVM-FIG-139 -->

**SPEC。** Figure 139〈LBA Status Descriptor List〉：8-byte header 後跟 16-byte descriptors；NLSD 是實際數量。CMPC=1 表示資訊尚未完整，即使 CQE 已成功。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

8-byte header 後跟 16-byte descriptors；NLSD 是實際數量。CMPC=1 表示資訊尚未完整，即使 CQE 已成功。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NLSD]
          ↓
[擷取欄位: CMPC] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NLSD` | Number of LBA Status Descriptors；實際 descriptor 數量。 |
| `CMPC` | Completion Condition；描述 Get LBA Status 是否已完成所要求的範圍。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 8-byte header 後跟 16-byte descriptors；NLSD 是實際數量。CMPC=1 表示資訊尚未完整，即使 CQE 已成功。
3. 讀到 potentially unrecoverable 不是每個 block 一定無法讀取。先辨識 ATYPE，再檢查 buffer 是否足夠與 completion condition，最後安排資料修復。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 139 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 8-byte header 後跟 16-byte descriptors；NLSD 是實際數量。CMPC=1 表示資訊尚未完整，即使 CQE 已成功。 |
| 邊界 | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

**說明性範例。** log 有 NLSLNE=0 但 ESTULB 非零時，不能當作沒有問題，宜檢查 attached namespaces 的完整 LBA 範圍。取得可疑 LBAs 後，可從其他可靠來源恢復並寫回；後續查詢會移除成功重寫且未再偵測的項目。

**常見誤解。** CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NLSD, CMPC

**來源 keyword 索引：** shall, should not, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.2.1, Figure 139, 文件頁 116-117, PDF 頁 116-117

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 140: LBA Status Descriptor Entry</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-140-CLAIM figure-table:NVMCS13-NVM-FIG-140 -->

**SPEC。** Figure 140〈LBA Status Descriptor Entry〉：NLB 是 0-based；LBARS=010b 適用 ATYPE02h，表示至少一個 block 已配置，不表示每個 block 都獨立配置。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

NLB 是 0-based；LBARS=010b 適用 ATYPE02h，表示至少一個 block 已配置，不表示每個 block 都獨立配置。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DSLBA]
          ↓
[擷取欄位: NLB] → [套用編碼: LBARS]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DSLBA` | 範圍起始 LBA；SDLBA 選 Copy 目的，DSLBA 是 Get LBA Status descriptor 的起點。 |
| `NLB` | Number of Logical Blocks；本報告命令／status descriptors 的該欄為 0-based。DSM 的 LLB 另為1-based。 |
| `LBARS` | LBA Valid 與 LBA Range Status；先驗資料是否有效，再依 Action Type 解讀狀態。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. NLB 是 0-based；LBARS=010b 適用 ATYPE02h，表示至少一個 block 已配置，不表示每個 block 都獨立配置。
3. 讀到 potentially unrecoverable 不是每個 block 一定無法讀取。先辨識 ATYPE，再檢查 buffer 是否足夠與 completion condition，最後安排資料修復。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 140 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §4.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | NLB 是 0-based；LBARS=010b 適用 ATYPE02h，表示至少一個 block 已配置，不表示每個 block 都獨立配置。 |
| 邊界 | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

**說明性範例。** log 有 NLSLNE=0 但 ESTULB 非零時，不能當作沒有問題，宜檢查 attached namespaces 的完整 LBA 範圍。取得可疑 LBAs 後，可從其他可靠來源恢復並寫回；後續查詢會移除成功重寫且未再偵測的項目。

**常見誤解。** CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DSLBA, NLB, LBARS

**來源 keyword 索引：** shall, should not, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.2.1, Figure 140, 文件頁 117-118, PDF 頁 117-118

</details>

<a id="section-5-1"></a>

### §5.1

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 141: ANA effects on NVM Command Set Command Processing</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-141-CLAIM figure-table:NVMCS13-NVM-FIG-141 -->

**SPEC。** Figure 141〈ANA effects on NVM Command Set Command Processing〉：按 command 與 ANA state 交叉查：FID05h 的 Get／Set 限制列並不完全相同，Identify 的容量回零只描述報告值。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

按 command 與 ANA state 交叉查：FID05h 的 Get／Set 限制列並不完全相同，Identify 的容量回零只描述報告值。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NUSE]
          ↓
[擷取欄位: NVMCAP] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NUSE` | Namespace Utilization；目前配置 logical blocks 數量。 |
| `NVMCAP` | NVM Capacity；以 bytes 計，不能與 NSZE／NCAP 的 logical-block 數直接比較。 |
| `相關欄位` | ANA state, FID 05h — 按 command 與 ANA state 交叉查：FID05h 的 Get／Set 限制列並不完全相同，Identify 的容量回零只描述報告值。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 按 command 與 ANA state 交叉查：FID05h 的 Get／Set 限制列並不完全相同，Identify 的容量回零只描述報告值。
3. 同一 namespace 的可達性與存取權限要分開檢查；不能將路徑狀態等同 reservation ownership。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 141 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 按 command 與 ANA state 交叉查：FID05h 的 Get／Set 限制列並不完全相同，Identify 的容量回零只描述報告值。 |
| 邊界 | 不能僅憑存在 Reservation 就一律封鎖所有非 holder 的 I/O；Write Exclusive 與 Exclusive Access 等類型的讀取規則不同。 |

**說明性範例。** 同一 SSD 的兩個 PCIe controllers 可共享 namespace。Controller 1 的路徑可用，仍可能因 reservation 類型與自身 registration 狀態而無法 Write；Read 是否允許需另外查表。

**常見誤解。** 不能僅憑存在 Reservation 就一律封鎖所有非 holder 的 I/O；Write Exclusive 與 Exclusive Access 等類型的讀取規則不同。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 不能僅憑存在 Reservation 就一律封鎖所有非 holder 的 I/O；Write Exclusive 與 Exclusive Access 等類型的讀取規則不同。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** ANA state, FID 05h, NUSE, NVMCAP

**來源 keyword 索引：** shall not, shall, may, optional

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.1, Figure 141, 文件頁 119, PDF 頁 119

</details>

<a id="section-5-2"></a>

### §5.2

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 142: Example LBA Status Log Namespace Element returned by LBA Status Information</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-142-CLAIM figure-table:NVMCS13-NVM-FIG-142 -->

**SPEC。** Figure 142〈Example LBA Status Log Namespace Element returned by LBA Status Information〉：示例 namespace element 指出兩段候選 ranges 與 RATYPE=11h；這是後續查詢輸入，不是每個候選 block 的最終診斷。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

示例 namespace element 指出兩段候選 ranges 與 RATYPE=11h；這是後續查詢輸入，不是每個候選 block 的最終診斷。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: RNLB]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `RNLB` | LBA Status log 的 Range Number of Logical Blocks；0-based。 |
| `相關欄位` | NEID, NLRD, RATYPE, RSLBA — 示例 namespace element 指出兩段候選 ranges 與 RATYPE=11h；這是後續查詢輸入，不是每個候選 block 的最終診斷。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 示例 namespace element 指出兩段候選 ranges 與 RATYPE=11h；這是後續查詢輸入，不是每個候選 block 的最終診斷。
3. 讀到 potentially unrecoverable 不是每個 block 一定無法讀取。先辨識 ATYPE，再檢查 buffer 是否足夠與 completion condition，最後安排資料修復。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 142 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 示例 namespace element 指出兩段候選 ranges 與 RATYPE=11h；這是後續查詢輸入，不是每個候選 block 的最終診斷。 |
| 邊界 | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

**說明性範例。** log 有 NLSLNE=0 但 ESTULB 非零時，不能當作沒有問題，宜檢查 attached namespaces 的完整 LBA 範圍。取得可疑 LBAs 後，可從其他可靠來源恢復並寫回；後續查詢會移除成功重寫且未再偵測的項目。

**常見誤解。** CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NEID, NLRD, RATYPE, RSLBA, RNLB

**來源 keyword 索引：** reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.1, Figure 142, 文件頁 121, PDF 頁 121

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 143: Example Get LBA Status Descriptors for LBA Range Descriptor 0</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-143-CLAIM figure-table:NVMCS13-NVM-FIG-143 -->

**SPEC。** Figure 143〈Example Get LBA Status Descriptors for LBA Range Descriptor 0〉：同一 log range 可由後續 Get LBA Status 產生不同數量的精細 descriptors；以實際 NLSD、NLB 與 CMPC 判斷是否需要續查。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

同一 log range 可由後續 Get LBA Status 產生不同數量的精細 descriptors；以實際 NLSD、NLB 與 CMPC 判斷是否需要續查。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NLSD]
          ↓
[擷取欄位: DSLBA] → [套用編碼: NLB]
                                      ↓
[驗證證據: CMPC]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NLSD` | Number of LBA Status Descriptors；實際 descriptor 數量。 |
| `DSLBA` | 範圍起始 LBA；SDLBA 選 Copy 目的，DSLBA 是 Get LBA Status descriptor 的起點。 |
| `NLB` | Number of Logical Blocks；本報告命令／status descriptors 的該欄為 0-based。DSM 的 LLB 另為1-based。 |
| `CMPC` | Completion Condition；描述 Get LBA Status 是否已完成所要求的範圍。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 同一 log range 可由後續 Get LBA Status 產生不同數量的精細 descriptors；以實際 NLSD、NLB 與 CMPC 判斷是否需要續查。
3. 讀到 potentially unrecoverable 不是每個 block 一定無法讀取。先辨識 ATYPE，再檢查 buffer 是否足夠與 completion condition，最後安排資料修復。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 143 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 同一 log range 可由後續 Get LBA Status 產生不同數量的精細 descriptors；以實際 NLSD、NLB 與 CMPC 判斷是否需要續查。 |
| 邊界 | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

**說明性範例。** log 有 NLSLNE=0 但 ESTULB 非零時，不能當作沒有問題，宜檢查 attached namespaces 的完整 LBA 範圍。取得可疑 LBAs 後，可從其他可靠來源恢復並寫回；後續查詢會移除成功重寫且未再偵測的項目。

**常見誤解。** CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NLSD, DSLBA, NLB, CMPC

**來源 keyword 索引：** reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.1, Figure 143, 文件頁 121, PDF 頁 121

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 144: Example Get LBA Status Descriptors for LBA Range Descriptor 1</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-144-CLAIM figure-table:NVMCS13-NVM-FIG-144 -->

**SPEC。** Figure 144〈Example Get LBA Status Descriptors for LBA Range Descriptor 1〉：同一 log range 可由後續 Get LBA Status 產生不同數量的精細 descriptors；以實際 NLSD、NLB 與 CMPC 判斷是否需要續查。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

同一 log range 可由後續 Get LBA Status 產生不同數量的精細 descriptors；以實際 NLSD、NLB 與 CMPC 判斷是否需要續查。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NLSD]
          ↓
[擷取欄位: DSLBA] → [套用編碼: NLB]
                                      ↓
[驗證證據: CMPC]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NLSD` | Number of LBA Status Descriptors；實際 descriptor 數量。 |
| `DSLBA` | 範圍起始 LBA；SDLBA 選 Copy 目的，DSLBA 是 Get LBA Status descriptor 的起點。 |
| `NLB` | Number of Logical Blocks；本報告命令／status descriptors 的該欄為 0-based。DSM 的 LLB 另為1-based。 |
| `CMPC` | Completion Condition；描述 Get LBA Status 是否已完成所要求的範圍。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 同一 log range 可由後續 Get LBA Status 產生不同數量的精細 descriptors；以實際 NLSD、NLB 與 CMPC 判斷是否需要續查。
3. 讀到 potentially unrecoverable 不是每個 block 一定無法讀取。先辨識 ATYPE，再檢查 buffer 是否足夠與 completion condition，最後安排資料修復。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 144 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 同一 log range 可由後續 Get LBA Status 產生不同數量的精細 descriptors；以實際 NLSD、NLB 與 CMPC 判斷是否需要續查。 |
| 邊界 | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

**說明性範例。** log 有 NLSLNE=0 但 ESTULB 非零時，不能當作沒有問題，宜檢查 attached namespaces 的完整 LBA 範圍。取得可疑 LBAs 後，可從其他可靠來源恢復並寫回；後續查詢會移除成功重寫且未再偵測的項目。

**常見誤解。** CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NLSD, DSLBA, NLB, CMPC

**來源 keyword 索引：** shall, should, may, optional, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.1, Figure 144, 文件頁 121-122, PDF 頁 121-122

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 145: An example namespace with four NOIOBs</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-145-CLAIM figure-table:NVMCS13-NVM-FIG-145 -->

**SPEC。** Figure 145〈An example namespace with four NOIOBs〉：最佳 I/O boundary 的示意獨立於 atomic boundary；跨線命令可分割以符合建議，但分割本身會增加命令數。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

最佳 I/O boundary 的示意獨立於 atomic boundary；跨線命令可分割以符合建議，但分割本身會增加命令數。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | NOIOB, Conformant range, Crossing range — 最佳 I/O boundary 的示意獨立於 atomic boundary；跨線命令可分割以符合建議，但分割本身會增加命令數。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 最佳 I/O boundary 的示意獨立於 atomic boundary；跨線命令可分割以符合建議，但分割本身會增加命令數。
3. 先把 raw 欄位轉成 blocks，再評估 start alignment 與 length granularity。只滿足其中一項可能仍引發 read-modify-write。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 145 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 最佳 I/O boundary 的示意獨立於 atomic boundary；跨線命令可分割以符合建議，但分割本身會增加命令數。 |
| 邊界 | 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。 |

**說明性範例。** 解碼後 NPWG=8、NPWA=8。寫 LBA 8..15 同時符合；寫 9..16 雖然也是 8 blocks，仍跨兩個 granularity units，可能需要讀取兩端舊資料。

**常見誤解。** 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NOIOB, Conformant range, Crossing range

**來源 keyword 索引：** should, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 145, 文件頁 124, PDF 頁 124

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 146: Example namespace illustrating a potential NABO and NABSN</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-146-CLAIM figure-table:NVMCS13-NVM-FIG-146 -->

**SPEC。** Figure 146〈Example namespace illustrating a potential NABO and NABSN〉：在 namespace 起點之外另標 atomic offset；不能把所有 boundaries 都預設從 LBA0 開始。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

在 namespace 起點之外另標 atomic offset；不能把所有 boundaries 都預設從 LBA0 開始。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NABO]
          ↓
[擷取欄位: NABSN] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NABO` | Namespace Atomic Boundary Offset；決定第一個 boundary 的位置。 |
| `NABSN` | Normal／power-fail atomic boundary size；0 值與 NSABP 支援要依欄位定義判讀。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 在 namespace 起點之外另標 atomic offset；不能把所有 boundaries 都預設從 LBA0 開始。
3. 先把 raw 欄位轉成 blocks，再評估 start alignment 與 length granularity。只滿足其中一項可能仍引發 read-modify-write。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 146 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 在 namespace 起點之外另標 atomic offset；不能把所有 boundaries 都預設從 LBA0 開始。 |
| 邊界 | 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。 |

**說明性範例。** 解碼後 NPWG=8、NPWA=8。寫 LBA 8..15 同時符合；寫 9..16 雖然也是 8 blocks，仍跨兩個 granularity units，可能需要讀取兩端舊資料。

**常見誤解。** 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NABO, NABSN

**來源 keyword 索引：** should, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 146, 文件頁 124, PDF 頁 124

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 147: Example namespace broken down to illustrate potential NPWA and NPWG settings</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-147-CLAIM figure-table:NVMCS13-NVM-FIG-147 -->

**SPEC。** Figure 147〈Example namespace broken down to illustrate potential NPWA and NPWG settings〉：NPWA 指起點，NPWG 指長度 granularity；示意的 8 blocks 是解碼後大小，並非 raw field=8。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

NPWA 指起點，NPWG 指長度 granularity；示意的 8 blocks 是解碼後大小，並非 raw field=8。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | NPWA, NPWG — NPWA 指起點，NPWG 指長度 granularity；示意的 8 blocks 是解碼後大小，並非 raw field=8。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. NPWA 指起點，NPWG 指長度 granularity；示意的 8 blocks 是解碼後大小，並非 raw field=8。
3. 先把 raw 欄位轉成 blocks，再評估 start alignment 與 length granularity。只滿足其中一項可能仍引發 read-modify-write。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 147 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | NPWA 指起點，NPWG 指長度 granularity；示意的 8 blocks 是解碼後大小，並非 raw field=8。 |
| 邊界 | 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。 |

**說明性範例。** 解碼後 NPWG=8、NPWA=8。寫 LBA 8..15 同時符合；寫 9..16 雖然也是 8 blocks，仍跨兩個 granularity units，可能需要讀取兩端舊資料。

**常見誤解。** 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NPWA, NPWG

**來源 keyword 索引：** may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 147, 文件頁 125, PDF 頁 125

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 148: Example namespace broken down to illustrate potential NPRA and NPRG settings</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-148-CLAIM figure-table:NVMCS13-NVM-FIG-148 -->

**SPEC。** Figure 148〈Example namespace broken down to illustrate potential NPRA and NPRG settings〉：讀取 alignment 與 granularity 分開，示例為 4-block alignment 與 8-block granularity；較短且錯位的讀取可能影響效能。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

讀取 alignment 與 granularity 分開，示例為 4-block alignment 與 8-block granularity；較短且錯位的讀取可能影響效能。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | NPRA, NPRG — 讀取 alignment 與 granularity 分開，示例為 4-block alignment 與 8-block granularity；較短且錯位的讀取可能影響效能。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 讀取 alignment 與 granularity 分開，示例為 4-block alignment 與 8-block granularity；較短且錯位的讀取可能影響效能。
3. 先把 raw 欄位轉成 blocks，再評估 start alignment 與 length granularity。只滿足其中一項可能仍引發 read-modify-write。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 148 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 讀取 alignment 與 granularity 分開，示例為 4-block alignment 與 8-block granularity；較短且錯位的讀取可能影響效能。 |
| 邊界 | 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。 |

**說明性範例。** 解碼後 NPWG=8、NPWA=8。寫 LBA 8..15 同時符合；寫 9..16 雖然也是 8 blocks，仍跨兩個 granularity units，可能需要讀取兩端舊資料。

**常見誤解。** 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NPRA, NPRG

**來源 keyword 索引：** should, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 148, 文件頁 126, PDF 頁 126

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 149: Non-conformant Write Impact</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-149-CLAIM figure-table:NVMCS13-NVM-FIG-149 -->

**SPEC。** Figure 149〈Non-conformant Write Impact〉：只更新 8-block unit 中的 3 blocks，示例需讀回前後共 5 blocks 舊資料再合成；這是可能的 read-modify-write 成本。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

只更新 8-block unit 中的 3 blocks，示例需讀回前後共 5 blocks 舊資料再合成；這是可能的 read-modify-write 成本。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Old prefix, New data, Old suffix — 只更新 8-block unit 中的 3 blocks，示例需讀回前後共 5 blocks 舊資料再合成；這是可能的 read-modify-write 成本。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 只更新 8-block unit 中的 3 blocks，示例需讀回前後共 5 blocks 舊資料再合成；這是可能的 read-modify-write 成本。
3. 先把 raw 欄位轉成 blocks，再評估 start alignment 與 length granularity。只滿足其中一項可能仍引發 read-modify-write。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 149 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 只更新 8-block unit 中的 3 blocks，示例需讀回前後共 5 blocks 舊資料再合成；這是可能的 read-modify-write 成本。 |
| 邊界 | 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。 |

**說明性範例。** 解碼後 NPWG=8、NPWA=8。寫 LBA 8..15 同時符合；寫 9..16 雖然也是 8 blocks，仍跨兩個 granularity units，可能需要讀取兩端舊資料。

**常見誤解。** 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Old prefix, New data, Old suffix

**來源 keyword 索引：** may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 149, 文件頁 127, PDF 頁 127

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 150: Host write I/O command following NPWA and NPWG</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-150-CLAIM figure-table:NVMCS13-NVM-FIG-150 -->

**SPEC。** Figure 150〈Host write I/O command following NPWA and NPWG〉：示意同時滿足 NPWA 與 NPWG 的範圍，可避免範例中的頭尾補讀；不是對所有硬體保證沒有任何內部讀取。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

示意同時滿足 NPWA 與 NPWG 的範圍，可避免範例中的頭尾補讀；不是對所有硬體保證沒有任何內部讀取。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Aligned start, Full granularity — 示意同時滿足 NPWA 與 NPWG 的範圍，可避免範例中的頭尾補讀；不是對所有硬體保證沒有任何內部讀取。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 示意同時滿足 NPWA 與 NPWG 的範圍，可避免範例中的頭尾補讀；不是對所有硬體保證沒有任何內部讀取。
3. 先把 raw 欄位轉成 blocks，再評估 start alignment 與 length granularity。只滿足其中一項可能仍引發 read-modify-write。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 150 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 示意同時滿足 NPWA 與 NPWG 的範圍，可避免範例中的頭尾補讀；不是對所有硬體保證沒有任何內部讀取。 |
| 邊界 | 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。 |

**說明性範例。** 解碼後 NPWG=8、NPWA=8。寫 LBA 8..15 同時符合；寫 9..16 雖然也是 8 blocks，仍跨兩個 granularity units，可能需要讀取兩端舊資料。

**常見誤解。** 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Aligned start, Full granularity

**來源 keyword 索引：** may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 150, 文件頁 127, PDF 頁 127

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 151: Host write I/O command following NPWG but not NPWA attributes</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-151-CLAIM figure-table:NVMCS13-NVM-FIG-151 -->

**SPEC。** Figure 151〈Host write I/O command following NPWG but not NPWA attributes〉：長度剛好一個 NPWG，起點仍可能錯位而觸及兩個 units；只檢查 length modulo NPWG 不足。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

長度剛好一個 NPWG，起點仍可能錯位而觸及兩個 units；只檢查 length modulo NPWG 不足。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Misaligned start, Full length — 長度剛好一個 NPWG，起點仍可能錯位而觸及兩個 units；只檢查 length modulo NPWG 不足。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 長度剛好一個 NPWG，起點仍可能錯位而觸及兩個 units；只檢查 length modulo NPWG 不足。
3. 先把 raw 欄位轉成 blocks，再評估 start alignment 與 length granularity。只滿足其中一項可能仍引發 read-modify-write。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 151 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 長度剛好一個 NPWG，起點仍可能錯位而觸及兩個 units；只檢查 length modulo NPWG 不足。 |
| 邊界 | 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。 |

**說明性範例。** 解碼後 NPWG=8、NPWA=8。寫 LBA 8..15 同時符合；寫 9..16 雖然也是 8 blocks，仍跨兩個 granularity units，可能需要讀取兩端舊資料。

**常見誤解。** 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Misaligned start, Full length

**來源 keyword 索引：** should, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 151, 文件頁 128, PDF 頁 128

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 152: Two streams composed of SGS and SWS</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-152-CLAIM figure-table:NVMCS13-NVM-FIG-152 -->

**SPEC。** Figure 152〈Two streams composed of SGS and SWS〉：以 SGS 個 SWS units 組成 stream granularity；寫入依 SWS、stream deallocate 依較大 granularity 協調。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

以 SGS 個 SWS units 組成 stream granularity；寫入依 SWS、stream deallocate 依較大 granularity 協調。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SWS]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SWS` | Stream Write Size；NVM command-set 單位為 logical blocks。 |
| `相關欄位` | SGS, Stream granularity — 以 SGS 個 SWS units 組成 stream granularity；寫入依 SWS、stream deallocate 依較大 granularity 協調。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 以 SGS 個 SWS units 組成 stream granularity；寫入依 SWS、stream deallocate 依較大 granularity 協調。
3. 用兩層大小模型解釋 Stream Write Size 與較大的 stream granularity。它們可能和 namespace hints 成整數倍，但規格不保證每個 namespace 都如此。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 152 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 以 SGS 個 SWS units 組成 stream granularity；寫入依 SWS、stream deallocate 依較大 granularity 協調。 |
| 邊界 | Streams hints、FDP placement 與 namespace atomicity 是不同概念；不能只因尺寸相等就推論是同一個內部媒體單位。 |

**說明性範例。** 解碼後 SWS=8 blocks、SGS=4，stream granularity 是 32 blocks。8-block Write 可符合 SWS，但一個完整 granularity-unit 的 deallocate 長度是 32 blocks。

**常見誤解。** Streams hints、FDP placement 與 namespace atomicity 是不同概念；不能只因尺寸相等就推論是同一個內部媒體單位。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Streams hints、FDP placement 與 namespace atomicity 是不同概念；不能只因尺寸相等就推論是同一個內部媒體單位。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SGS, SWS, Stream granularity

**來源 keyword 索引：** should, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 152, 文件頁 128, PDF 頁 128

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 153: Metadata – Contiguous with LBA Data, Forming Extended LBA</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-153-CLAIM figure-table:NVMCS13-NVM-FIG-153 -->

**SPEC。** Figure 153〈Metadata – Contiguous with LBA Data, Forming Extended LBA〉：extended LBA 依序排列每個 block 的 data 後接 metadata；不可把全部 data 排完才接全部 metadata。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

extended LBA 依序排列每個 block 的 data 後接 metadata；不可把全部 data 排完才接全部 metadata。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DPTR]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DPTR` | 命令 data pointer；Read 是目的、Write 是來源、Copy／DSM 指向 descriptors。 |
| `相關欄位` | Data, Metadata — extended LBA 依序排列每個 block 的 data 後接 metadata；不可把全部 data 排完才接全部 metadata。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. extended LBA 依序排列每個 block 的 data 後接 metadata；不可把全部 data 排完才接全部 metadata。
3. Metadata 不一定全是 PI。先標示 data、非 PI metadata 與 PI 三個區域，再計算 host buffer 大小與 CRC coverage。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 153 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | extended LBA 依序排列每個 block 的 data 後接 metadata；不可把全部 data 排完才接全部 metadata。 |
| 邊界 | PI 在末端的位置規則與「metadata 是否 separate」是獨立維度；不能以 DIX／DIF 名稱省略 namespace format 設定。 |

**說明性範例。** 8 blocks、data=4096、MS=16、PRACT=0：extended buffer 為 32896 bytes；separate 模式 data buffer=32768、metadata buffer=128 bytes。

**常見誤解。** PI 在末端的位置規則與「metadata 是否 separate」是獨立維度；不能以 DIX／DIF 名稱省略 namespace format 設定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | PI 在末端的位置規則與「metadata 是否 separate」是獨立維度；不能以 DIX／DIF 名稱省略 namespace format 設定。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Data, Metadata, DPTR

**來源 keyword 索引：** should, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.3, Figure 153, 文件頁 129, PDF 頁 129

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 154: Metadata – Transferred as Separate Buffer</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-154-CLAIM figure-table:NVMCS13-NVM-FIG-154 -->

**SPEC。** Figure 154〈Metadata – Transferred as Separate Buffer〉：separate 模式保留 data 與 metadata 兩個 buffer 並保持 block 對應；不是把 metadata 任意重排成無序清單。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

separate 模式保留 data 與 metadata 兩個 buffer 並保持 block 對應；不是把 metadata 任意重排成無序清單。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MPTR]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MPTR` | Separate metadata 的指標；metadata placement 由 namespace format 與命令欄位決定。 |
| `相關欄位` | Data buffer, Metadata buffer — separate 模式保留 data 與 metadata 兩個 buffer 並保持 block 對應；不是把 metadata 任意重排成無序清單。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. separate 模式保留 data 與 metadata 兩個 buffer 並保持 block 對應；不是把 metadata 任意重排成無序清單。
3. Metadata 不一定全是 PI。先標示 data、非 PI metadata 與 PI 三個區域，再計算 host buffer 大小與 CRC coverage。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 154 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | separate 模式保留 data 與 metadata 兩個 buffer 並保持 block 對應；不是把 metadata 任意重排成無序清單。 |
| 邊界 | PI 在末端的位置規則與「metadata 是否 separate」是獨立維度；不能以 DIX／DIF 名稱省略 namespace format 設定。 |

**說明性範例。** 8 blocks、data=4096、MS=16、PRACT=0：extended buffer 為 32896 bytes；separate 模式 data buffer=32768、metadata buffer=128 bytes。

**常見誤解。** PI 在末端的位置規則與「metadata 是否 separate」是獨立維度；不能以 DIX／DIF 名稱省略 namespace format 設定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | PI 在末端的位置規則與「metadata 是否 separate」是獨立維度；不能以 DIX／DIF 名稱省略 namespace format 設定。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Data buffer, Metadata buffer, MPTR

**來源 keyword 索引：** shall, may, optional

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.3, Figure 154, 文件頁 130, PDF 頁 130

</details>

<a id="section-5-3"></a>

### §5.3

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 155: 16b Guard Protection Information Format when STS field is cleared to 0h</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-155-CLAIM figure-table:NVMCS13-NVM-FIG-155 -->

**SPEC。** Figure 155〈16b Guard Protection Information Format when STS field is cleared to 0h〉：STS=0 的 8-byte PI 由 16-bit Guard、16-bit Application 與 32-bit Reference 組成，各欄位依圖採高位在前。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

STS=0 的 8-byte PI 由 16-bit Guard、16-bit Application 與 32-bit Reference 組成，各欄位依圖採高位在前。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Guard16, Application16, Reference32 — STS=0 的 8-byte PI 由 16-bit Guard、16-bit Application 與 32-bit Reference 組成，各欄位依圖採高位在前。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. STS=0 的 8-byte PI 由 16-bit Guard、16-bit Application 與 32-bit Reference 組成，各欄位依圖採高位在前。
3. 先由 PIF 決定格式；PIF=11b 才由 QPIF 決定 Guard width，並受 QPIFS 與 STMLA 條件限制。Protection type 仍由 DPS 決定。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 155 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | STS=0 的 8-byte PI 由 16-bit Guard、16-bit Application 與 32-bit Reference 組成，各欄位依圖採高位在前。 |
| 邊界 | 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。 |

**說明性範例。** 64b Guard、STS=18：48-bit space 中高 18 bits 是 Storage Tag、低 30 bits 是 Reference Tag。PI 總大小仍為 16 bytes，不會因 STS 增加而變大。

**常見誤解。** 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Guard16, Application16, Reference32

**來源 keyword 索引：** may, optional

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.1, Figure 155, 文件頁 131, PDF 頁 131

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 156: 16b Guard Protection Information Format with non-zero STS</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-156-CLAIM figure-table:NVMCS13-NVM-FIG-156 -->

**SPEC。** Figure 156〈16b Guard Protection Information Format with non-zero STS〉：加入 Storage Tag 後仍維持 8 bytes；只把原先的 32-bit Reference space 切開，不在末端追加新 bytes。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

加入 Storage Tag 後仍維持 8 bytes；只把原先的 32-bit Reference space 切開，不在末端追加新 bytes。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Guard16, Application16, StorageReference32 — 加入 Storage Tag 後仍維持 8 bytes；只把原先的 32-bit Reference space 切開，不在末端追加新 bytes。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 加入 Storage Tag 後仍維持 8 bytes；只把原先的 32-bit Reference space 切開，不在末端追加新 bytes。
3. 先由 PIF 決定格式；PIF=11b 才由 QPIF 決定 Guard width，並受 QPIFS 與 STMLA 條件限制。Protection type 仍由 DPS 決定。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 156 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 加入 Storage Tag 後仍維持 8 bytes；只把原先的 32-bit Reference space 切開，不在末端追加新 bytes。 |
| 邊界 | 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。 |

**說明性範例。** 64b Guard、STS=18：48-bit space 中高 18 bits 是 Storage Tag、低 30 bits 是 Reference Tag。PI 總大小仍為 16 bytes，不會因 STS 增加而變大。

**常見誤解。** 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Guard16, Application16, StorageReference32

**來源 keyword 索引：** shall

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.1, Figure 156, 文件頁 132, PDF 頁 132

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 157: 32b Guard Protection Information Format</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-157-CLAIM figure-table:NVMCS13-NVM-FIG-157 -->

**SPEC。** Figure 157〈32b Guard Protection Information Format〉：32b Guard 的 16-byte PI 留 80 bits 給 Storage／Reference；STS 至少 16，Reference 至少保留 16 bits。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

32b Guard 的 16-byte PI 留 80 bits 給 Storage／Reference；STS 至少 16，Reference 至少保留 16 bits。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Guard32, Application16, StorageReference80 — 32b Guard 的 16-byte PI 留 80 bits 給 Storage／Reference；STS 至少 16，Reference 至少保留 16 bits。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 32b Guard 的 16-byte PI 留 80 bits 給 Storage／Reference；STS 至少 16，Reference 至少保留 16 bits。
3. 先由 PIF 決定格式；PIF=11b 才由 QPIF 決定 Guard width，並受 QPIFS 與 STMLA 條件限制。Protection type 仍由 DPS 決定。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 157 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 32b Guard 的 16-byte PI 留 80 bits 給 Storage／Reference；STS 至少 16，Reference 至少保留 16 bits。 |
| 邊界 | 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。 |

**說明性範例。** 64b Guard、STS=18：48-bit space 中高 18 bits 是 Storage Tag、低 30 bits 是 Reference Tag。PI 總大小仍為 16 bytes，不會因 STS 增加而變大。

**常見誤解。** 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Guard32, Application16, StorageReference80

**來源 keyword 索引：** shall

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.2, Figure 157, 文件頁 133, PDF 頁 133

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 158: 32b CRC Test Cases for 4 KiB Logical Block with no Metadata</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-158-CLAIM figure-table:NVMCS13-NVM-FIG-158 -->

**SPEC。** Figure 158〈32b CRC Test Cases for 4 KiB Logical Block with no Metadata〉：用四組 4 KiB vectors 驗證 CRC32C，而非只驗證全零；incrementing／decrementing patterns 更容易找出順序錯誤。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

用四組 4 KiB vectors 驗證 CRC32C，而非只驗證全零；incrementing／decrementing patterns 更容易找出順序錯誤。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Zero vector, FF vector, Incrementing bytes, CRC32C — 用四組 4 KiB vectors 驗證 CRC32C，而非只驗證全零；incrementing／decrementing patterns 更容易找出順序錯誤。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 用四組 4 KiB vectors 驗證 CRC32C，而非只驗證全零；incrementing／decrementing patterns 更容易找出順序錯誤。
3. CRC 的 polynomial、初值、reflection、final XOR 與儲存順序必須一起核對。用已知向量驗證後才接進 PI parser。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 158 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 用四組 4 KiB vectors 驗證 CRC32C，而非只驗證全零；incrementing／decrementing patterns 更容易找出順序錯誤。 |
| 邊界 | Figure 161 列 Check=11199E506128D175h；常見 LSB-first register 對 123456789 算得 AE8B14860A799888h，兩者互為 64-bit 反轉。Figure 163 的四個 4 KiB 向量則直接符合該 register 結果。須明示表示差異，不因單一 Check 差異改 polynomial；CRC 也不是密碼學認證。 |

**說明性範例。** CRC-64 的 4 KiB 全 FFh 向量結果為 C0DDBA7302ECA3ACh。若 zero vector 正確而 incrementing-byte vector 不符，要檢查 byte／bit 順序，不能只改 polynomial 硬湊。

**常見誤解。** Figure 161 列 Check=11199E506128D175h；常見 LSB-first register 對 123456789 算得 AE8B14860A799888h，兩者互為 64-bit 反轉。Figure 163 的四個 4 KiB 向量則直接符合該 register 結果。須明示表示差異，不因單一 Check 差異改 polynomial；CRC 也不是密碼學認證。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 161 列 Check=11199E506128D175h；常見 LSB-first register 對 123456789 算得 AE8B14860A799888h，兩者互為 64-bit 反轉。Figure 163 的四個 4 KiB 向量則直接符合該 register 結果。須明示表示差異，不因單一 Check 差異改 polynomial；CRC 也不是密碼學認證。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Zero vector, FF vector, Incrementing bytes, CRC32C

**來源 keyword 索引：** shall

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.2, Figure 158, 文件頁 133, PDF 頁 133

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 159: 64b Guard Protection Information Format</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-159-CLAIM figure-table:NVMCS13-NVM-FIG-159 -->

**SPEC。** Figure 159〈64b Guard Protection Information Format〉：64b Guard 的 PI 雖與 32b Guard 同為 16 bytes，Storage／Reference 只剩 48 bits；不能複用 80-bit 切分。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

64b Guard 的 PI 雖與 32b Guard 同為 16 bytes，Storage／Reference 只剩 48 bits；不能複用 80-bit 切分。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Guard64, Application16, StorageReference48 — 64b Guard 的 PI 雖與 32b Guard 同為 16 bytes，Storage／Reference 只剩 48 bits；不能複用 80-bit 切分。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 64b Guard 的 PI 雖與 32b Guard 同為 16 bytes，Storage／Reference 只剩 48 bits；不能複用 80-bit 切分。
3. 先由 PIF 決定格式；PIF=11b 才由 QPIF 決定 Guard width，並受 QPIFS 與 STMLA 條件限制。Protection type 仍由 DPS 決定。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 159 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 64b Guard 的 PI 雖與 32b Guard 同為 16 bytes，Storage／Reference 只剩 48 bits；不能複用 80-bit 切分。 |
| 邊界 | 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。 |

**說明性範例。** 64b Guard、STS=18：48-bit space 中高 18 bits 是 Storage Tag、低 30 bits 是 Reference Tag。PI 總大小仍為 16 bytes，不會因 STS 增加而變大。

**常見誤解。** 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Guard64, Application16, StorageReference48

**來源 keyword 索引：** shall

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.3, Figure 159, 文件頁 134, PDF 頁 134

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 160: 64b CRC Polynomials</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-160-CLAIM figure-table:NVMCS13-NVM-FIG-160 -->

**SPEC。** Figure 160〈64b CRC Polynomials〉：以 GF(2) 的 polynomial remainder 解釋 CRC；實際 NVM CRC64 仍需套用後續 Figure161 的 init、reflection 與 XOR 參數。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

以 GF(2) 的 polynomial remainder 解釋 CRC；實際 NVM CRC64 仍需套用後續 Figure161 的 init、reflection 與 XOR 參數。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | F(x), G(x), R(x), CRC checking — 以 GF(2) 的 polynomial remainder 解釋 CRC；實際 NVM CRC64 仍需套用後續 Figure161 的 init、reflection 與 XOR 參數。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 以 GF(2) 的 polynomial remainder 解釋 CRC；實際 NVM CRC64 仍需套用後續 Figure161 的 init、reflection 與 XOR 參數。
3. CRC 的 polynomial、初值、reflection、final XOR 與儲存順序必須一起核對。用已知向量驗證後才接進 PI parser。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 160 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 以 GF(2) 的 polynomial remainder 解釋 CRC；實際 NVM CRC64 仍需套用後續 Figure161 的 init、reflection 與 XOR 參數。 |
| 邊界 | Figure 161 列 Check=11199E506128D175h；常見 LSB-first register 對 123456789 算得 AE8B14860A799888h，兩者互為 64-bit 反轉。Figure 163 的四個 4 KiB 向量則直接符合該 register 結果。須明示表示差異，不因單一 Check 差異改 polynomial；CRC 也不是密碼學認證。 |

**說明性範例。** CRC-64 的 4 KiB 全 FFh 向量結果為 C0DDBA7302ECA3ACh。若 zero vector 正確而 incrementing-byte vector 不符，要檢查 byte／bit 順序，不能只改 polynomial 硬湊。

**常見誤解。** Figure 161 列 Check=11199E506128D175h；常見 LSB-first register 對 123456789 算得 AE8B14860A799888h，兩者互為 64-bit 反轉。Figure 163 的四個 4 KiB 向量則直接符合該 register 結果。須明示表示差異，不因單一 Check 差異改 polynomial；CRC 也不是密碼學認證。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 161 列 Check=11199E506128D175h；常見 LSB-first register 對 123456789 算得 AE8B14860A799888h，兩者互為 64-bit 反轉。Figure 163 的四個 4 KiB 向量則直接符合該 register 結果。須明示表示差異，不因單一 Check 差異改 polynomial；CRC 也不是密碼學認證。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** F(x), G(x), R(x), CRC checking

**來源 keyword 索引：** shall, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.3, Figure 160, 文件頁 134-135, PDF 頁 134-135

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 161: 64-bit CRC Rocksoft Model Parameters</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-161-CLAIM figure-table:NVMCS13-NVM-FIG-161 -->

**SPEC。** Figure 161〈64-bit CRC Rocksoft Model Parameters〉：完整參數組才辨識 NVM CRC64：Poly=AD93D23594C93659h、Init／XorOut 全一、RefIn／RefOut=true。此圖 Check=11199E506128D175h 是常見 LSB-first register 結果 AE8B14860A799888h 的 64-bit 反轉；以 Figure 163 向量交叉驗證表示方式。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

完整參數組才辨識 NVM CRC64：Poly=AD93D23594C93659h、Init／XorOut 全一、RefIn／RefOut=true。此圖 Check=11199E506128D175h 是常見 LSB-first register 結果 AE8B14860A799888h 的 64-bit 反轉；以 Figure 163 向量交叉驗證表示方式。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Width64, Poly, Init, RefIn, RefOut, XorOut, Check — 完整參數組才辨識 NVM CRC64：Poly=AD93D23594C93659h、Init／XorOut 全一、RefIn／RefOut=true。此圖 Check=11199E506128D175h 是常見 LSB-first register 結果 AE8B14860A799888h 的 64-bit 反轉；以 Figure 163 向量交叉驗證表示方式。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 完整參數組才辨識 NVM CRC64：Poly=AD93D23594C93659h、Init／XorOut 全一、RefIn／RefOut=true。此圖 Check=11199E506128D175h 是常見 LSB-first register 結果 AE8B14860A799888h 的 64-bit 反轉；以 Figure 163 向量交叉驗證表示方式。
3. CRC 的 polynomial、初值、reflection、final XOR 與儲存順序必須一起核對。用已知向量驗證後才接進 PI parser。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 161 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 完整參數組才辨識 NVM CRC64：Poly=AD93D23594C93659h、Init／XorOut 全一、RefIn／RefOut=true。此圖 Check=11199E506128D175h 是常見 LSB-first register 結果 AE8B14860A799888h 的 64-bit 反轉；以 Figure 163 向量交叉驗證表示方式。 |
| 邊界 | Figure 161 列 Check=11199E506128D175h；常見 LSB-first register 對 123456789 算得 AE8B14860A799888h，兩者互為 64-bit 反轉。Figure 163 的四個 4 KiB 向量則直接符合該 register 結果。須明示表示差異，不因單一 Check 差異改 polynomial；CRC 也不是密碼學認證。 |

**說明性範例。** CRC-64 的 4 KiB 全 FFh 向量結果為 C0DDBA7302ECA3ACh。若 zero vector 正確而 incrementing-byte vector 不符，要檢查 byte／bit 順序，不能只改 polynomial 硬湊。

**常見誤解。** Figure 161 列 Check=11199E506128D175h；常見 LSB-first register 對 123456789 算得 AE8B14860A799888h，兩者互為 64-bit 反轉。Figure 163 的四個 4 KiB 向量則直接符合該 register 結果。須明示表示差異，不因單一 Check 差異改 polynomial；CRC 也不是密碼學認證。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 161 列 Check=11199E506128D175h；常見 LSB-first register 對 123456789 算得 AE8B14860A799888h，兩者互為 64-bit 反轉。Figure 163 的四個 4 KiB 向量則直接符合該 register 結果。須明示表示差異，不因單一 Check 差異改 polynomial；CRC 也不是密碼學認證。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Width64, Poly, Init, RefIn, RefOut, XorOut, Check

**來源 keyword 索引：** shall, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.3, Figure 161, 文件頁 136, PDF 頁 136

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 162: Logical Block and Metadata Example</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-162-CLAIM figure-table:NVMCS13-NVM-FIG-162 -->

**SPEC。** Figure 162〈Logical Block and Metadata Example〉：逐 byte 的 bits 0..7 對應 reflected input；不要把圖中顯示順序誤當 host integer 的原生 endian。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

逐 byte 的 bits 0..7 對應 reflected input；不要把圖中顯示順序誤當 host integer 的原生 endian。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Byte order, Reflected bits, Message body — 逐 byte 的 bits 0..7 對應 reflected input；不要把圖中顯示順序誤當 host integer 的原生 endian。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 逐 byte 的 bits 0..7 對應 reflected input；不要把圖中顯示順序誤當 host integer 的原生 endian。
3. CRC 的 polynomial、初值、reflection、final XOR 與儲存順序必須一起核對。用已知向量驗證後才接進 PI parser。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 162 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 逐 byte 的 bits 0..7 對應 reflected input；不要把圖中顯示順序誤當 host integer 的原生 endian。 |
| 邊界 | Figure 161 列 Check=11199E506128D175h；常見 LSB-first register 對 123456789 算得 AE8B14860A799888h，兩者互為 64-bit 反轉。Figure 163 的四個 4 KiB 向量則直接符合該 register 結果。須明示表示差異，不因單一 Check 差異改 polynomial；CRC 也不是密碼學認證。 |

**說明性範例。** CRC-64 的 4 KiB 全 FFh 向量結果為 C0DDBA7302ECA3ACh。若 zero vector 正確而 incrementing-byte vector 不符，要檢查 byte／bit 順序，不能只改 polynomial 硬湊。

**常見誤解。** Figure 161 列 Check=11199E506128D175h；常見 LSB-first register 對 123456789 算得 AE8B14860A799888h，兩者互為 64-bit 反轉。Figure 163 的四個 4 KiB 向量則直接符合該 register 結果。須明示表示差異，不因單一 Check 差異改 polynomial；CRC 也不是密碼學認證。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 161 列 Check=11199E506128D175h；常見 LSB-first register 對 123456789 算得 AE8B14860A799888h，兩者互為 64-bit 反轉。Figure 163 的四個 4 KiB 向量則直接符合該 register 結果。須明示表示差異，不因單一 Check 差異改 polynomial；CRC 也不是密碼學認證。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Byte order, Reflected bits, Message body

**來源 keyword 索引：** shall, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.3, Figure 162, 文件頁 136, PDF 頁 136

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 163: 64b CRC Test Cases for 4 KiB Logical Block with no Metadata</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-163-CLAIM figure-table:NVMCS13-NVM-FIG-163 -->

**SPEC。** Figure 163〈64b CRC Test Cases for 4 KiB Logical Block with no Metadata〉：核對四組 CRC64 vectors 與 command-set 指定參數；十六進位分組樣式不改變數值，但不可自行補或刪除 hex digits。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

核對四組 CRC64 vectors 與 command-set 指定參數；十六進位分組樣式不改變數值，但不可自行補或刪除 hex digits。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Zero vector, FF vector, Incrementing bytes, CRC64 — 核對四組 CRC64 vectors 與 command-set 指定參數；十六進位分組樣式不改變數值，但不可自行補或刪除 hex digits。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 核對四組 CRC64 vectors 與 command-set 指定參數；十六進位分組樣式不改變數值，但不可自行補或刪除 hex digits。
3. CRC 的 polynomial、初值、reflection、final XOR 與儲存順序必須一起核對。用已知向量驗證後才接進 PI parser。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 163 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 核對四組 CRC64 vectors 與 command-set 指定參數；十六進位分組樣式不改變數值，但不可自行補或刪除 hex digits。 |
| 邊界 | Figure 161 列 Check=11199E506128D175h；常見 LSB-first register 對 123456789 算得 AE8B14860A799888h，兩者互為 64-bit 反轉。Figure 163 的四個 4 KiB 向量則直接符合該 register 結果。須明示表示差異，不因單一 Check 差異改 polynomial；CRC 也不是密碼學認證。 |

**說明性範例。** CRC-64 的 4 KiB 全 FFh 向量結果為 C0DDBA7302ECA3ACh。若 zero vector 正確而 incrementing-byte vector 不符，要檢查 byte／bit 順序，不能只改 polynomial 硬湊。

**常見誤解。** Figure 161 列 Check=11199E506128D175h；常見 LSB-first register 對 123456789 算得 AE8B14860A799888h，兩者互為 64-bit 反轉。Figure 163 的四個 4 KiB 向量則直接符合該 register 結果。須明示表示差異，不因單一 Check 差異改 polynomial；CRC 也不是密碼學認證。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 161 列 Check=11199E506128D175h；常見 LSB-first register 對 123456789 算得 AE8B14860A799888h，兩者互為 64-bit 反轉。Figure 163 的四個 4 KiB 向量則直接符合該 register 結果。須明示表示差異，不因單一 Check 差異改 polynomial；CRC 也不是密碼學認證。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Zero vector, FF vector, Incrementing bytes, CRC64

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.3, Figure 163, 文件頁 137, PDF 頁 137

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 164: Storage and Reference Space Separation</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-164-CLAIM figure-table:NVMCS13-NVM-FIG-164 -->

**SPEC。** Figure 164〈Storage and Reference Space Separation〉：高 STS bits 是 Storage Tag，低剩餘 bits 是 Reference Tag；某一側可依合法 STS 不存在。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

高 STS bits 是 Storage Tag，低剩餘 bits 是 Reference Tag；某一側可依合法 STS 不存在。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: STS]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `STS` | Storage Tag Size；固定 Storage/Reference Space 中的高位 bit 數。 |
| `相關欄位` | Storage Tag, Reference Tag — 高 STS bits 是 Storage Tag，低剩餘 bits 是 Reference Tag；某一側可依合法 STS 不存在。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 高 STS bits 是 Storage Tag，低剩餘 bits 是 Reference Tag；某一側可依合法 STS 不存在。
3. 先由 PIF 決定格式；PIF=11b 才由 QPIF 決定 Guard width，並受 QPIFS 與 STMLA 條件限制。Protection type 仍由 DPS 決定。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 164 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 高 STS bits 是 Storage Tag，低剩餘 bits 是 Reference Tag；某一側可依合法 STS 不存在。 |
| 邊界 | 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。 |

**說明性範例。** 64b Guard、STS=18：48-bit space 中高 18 bits 是 Storage Tag、低 30 bits 是 Reference Tag。PI 總大小仍為 16 bytes，不會因 STS 增加而變大。

**常見誤解。** 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** STS, Storage Tag, Reference Tag

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 164, 文件頁 137, PDF 頁 137

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 165: LBST and LBRT Minimum and Maximum Sizes</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-165-CLAIM figure-table:NVMCS13-NVM-FIG-165 -->

**SPEC。** Figure 165〈LBST and LBRT Minimum and Maximum Sizes〉：以各格式總 space 減 STS 得 Reference width：32b Guard 是 80−STS，並不是 32−STS。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

以各格式總 space 減 STS 得 Reference width：32b Guard 是 80−STS，並不是 32−STS。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: STS]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `STS` | Storage Tag Size；固定 Storage/Reference Space 中的高位 bit 數。 |
| `相關欄位` | PI format, Tag width — 以各格式總 space 減 STS 得 Reference width：32b Guard 是 80−STS，並不是 32−STS。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 以各格式總 space 減 STS 得 Reference width：32b Guard 是 80−STS，並不是 32−STS。
3. 先由 PIF 決定格式；PIF=11b 才由 QPIF 決定 Guard width，並受 QPIFS 與 STMLA 條件限制。Protection type 仍由 DPS 決定。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 165 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 以各格式總 space 減 STS 得 Reference width：32b Guard 是 80−STS，並不是 32−STS。 |
| 邊界 | 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。 |

**說明性範例。** 64b Guard、STS=18：48-bit space 中高 18 bits 是 Storage Tag、低 30 bits 是 Reference Tag。PI 總大小仍為 16 bytes，不會因 STS 增加而變大。

**常見誤解。** 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** PI format, STS, Tag width

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 165, 文件頁 138, PDF 頁 138

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 166: LBST, ELBST, ILBRT, and EILBRT fields Format in Command Dwords</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-166-CLAIM figure-table:NVMCS13-NVM-FIG-166 -->

**SPEC。** Figure 166〈LBST, ELBST, ILBRT, and EILBRT fields Format in Command Dwords〉：用最多 80-bit 的抽象 space 連接三個 Dwords；依 PI format 先去掉 unused bits，再切 storage／reference。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

用最多 80-bit 的抽象 space 連接三個 Dwords；依 PI format 先去掉 unused bits，再切 storage／reference。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | CDW2, CDW3, CDW14, StorageReferenceSpace — 用最多 80-bit 的抽象 space 連接三個 Dwords；依 PI format 先去掉 unused bits，再切 storage／reference。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 用最多 80-bit 的抽象 space 連接三個 Dwords；依 PI format 先去掉 unused bits，再切 storage／reference。
3. 先決定總 space 大小，再切 tag，最後拆到命令 Dwords。不要因 tag 的名稱相似就把 Write 的值與 Read 的 expected 值交換。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 166 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 用最多 80-bit 的抽象 space 連接三個 Dwords；依 PI format 先去掉 unused bits，再切 storage／reference。 |
| 邊界 | Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。 |

**說明性範例。** 64b Guard、STS=18、Storage Tag=0x12345、Reference Tag=0x2A：CDW3 low16=0x48D1，CDW14=(1<<30)|0x2A=0x4000002A。Read 使用相同布局的 expected tags。

**常見誤解。** Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** CDW2, CDW3, CDW14, StorageReferenceSpace

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 166, 文件頁 138, PDF 頁 138

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 167: I/O Command LBST, ELBST, ILBRT, and EILBRT fields Format</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-167-CLAIM figure-table:NVMCS13-NVM-FIG-167 -->

**SPEC。** Figure 167〈I/O Command LBST, ELBST, ILBRT, and EILBRT fields Format〉：此表列出每個 Guard 格式實際使用的命令 bits；unused 不等於可自行定義的新欄位。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

此表列出每個 Guard 格式實際使用的命令 bits；unused 不等於可自行定義的新欄位。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | PI format, Used bits, Ignored bits — 此表列出每個 Guard 格式實際使用的命令 bits；unused 不等於可自行定義的新欄位。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 此表列出每個 Guard 格式實際使用的命令 bits；unused 不等於可自行定義的新欄位。
3. 先決定總 space 大小，再切 tag，最後拆到命令 Dwords。不要因 tag 的名稱相似就把 Write 的值與 Read 的 expected 值交換。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 167 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 此表列出每個 Guard 格式實際使用的命令 bits；unused 不等於可自行定義的新欄位。 |
| 邊界 | Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。 |

**說明性範例。** 64b Guard、STS=18、Storage Tag=0x12345、Reference Tag=0x2A：CDW3 low16=0x48D1，CDW14=(1<<30)|0x2A=0x4000002A。Read 使用相同布局的 expected tags。

**常見誤解。** Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** PI format, Used bits, Ignored bits

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 167, 文件頁 139, PDF 頁 139

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 168: 16b Guard Protection Information Write Command Example</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-168-CLAIM figure-table:NVMCS13-NVM-FIG-168 -->

**SPEC。** Figure 168〈16b Guard Protection Information Write Command Example〉：16b Guard 且 STS=0 時只有 CDW14 的 32-bit initial／expected reference；範例 LBADS 應依 Figure125 的 exponent 定義判讀。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

16b Guard 且 STS=0 時只有 CDW14 的 32-bit initial／expected reference；範例 LBADS 應依 Figure125 的 exponent 定義判讀。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | STS=0, CDW14, Reference32 — 16b Guard 且 STS=0 時只有 CDW14 的 32-bit initial／expected reference；範例 LBADS 應依 Figure125 的 exponent 定義判讀。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 16b Guard 且 STS=0 時只有 CDW14 的 32-bit initial／expected reference；範例 LBADS 應依 Figure125 的 exponent 定義判讀。
3. 先決定總 space 大小，再切 tag，最後拆到命令 Dwords。不要因 tag 的名稱相似就把 Write 的值與 Read 的 expected 值交換。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 168 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 16b Guard 且 STS=0 時只有 CDW14 的 32-bit initial／expected reference；範例 LBADS 應依 Figure125 的 exponent 定義判讀。 |
| 邊界 | Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。 |

**說明性範例。** 64b Guard、STS=18、Storage Tag=0x12345、Reference Tag=0x2A：CDW3 low16=0x48D1，CDW14=(1<<30)|0x2A=0x4000002A。Read 使用相同布局的 expected tags。

**常見誤解。** Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** STS=0, CDW14, Reference32

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 168, 文件頁 139, PDF 頁 139

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 169: 16b Guard Protection Information Read Command Example</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-169-CLAIM figure-table:NVMCS13-NVM-FIG-169 -->

**SPEC。** Figure 169〈16b Guard Protection Information Read Command Example〉：16b Guard 且 STS=0 時只有 CDW14 的 32-bit initial／expected reference；範例 LBADS 應依 Figure125 的 exponent 定義判讀。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

16b Guard 且 STS=0 時只有 CDW14 的 32-bit initial／expected reference；範例 LBADS 應依 Figure125 的 exponent 定義判讀。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | STS=0, CDW14, Reference32 — 16b Guard 且 STS=0 時只有 CDW14 的 32-bit initial／expected reference；範例 LBADS 應依 Figure125 的 exponent 定義判讀。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 16b Guard 且 STS=0 時只有 CDW14 的 32-bit initial／expected reference；範例 LBADS 應依 Figure125 的 exponent 定義判讀。
3. 先決定總 space 大小，再切 tag，最後拆到命令 Dwords。不要因 tag 的名稱相似就把 Write 的值與 Read 的 expected 值交換。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 169 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 16b Guard 且 STS=0 時只有 CDW14 的 32-bit initial／expected reference；範例 LBADS 應依 Figure125 的 exponent 定義判讀。 |
| 邊界 | Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。 |

**說明性範例。** 64b Guard、STS=18、Storage Tag=0x12345、Reference Tag=0x2A：CDW3 low16=0x48D1，CDW14=(1<<30)|0x2A=0x4000002A。Read 使用相同布局的 expected tags。

**常見誤解。** Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** STS=0, CDW14, Reference32

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 169, 文件頁 139-140, PDF 頁 139-140

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 170: 32b Guard Protection Information Write Command Example</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-170-CLAIM figure-table:NVMCS13-NVM-FIG-170 -->

**SPEC。** Figure 170〈32b Guard Protection Information Write Command Example〉：STS=32 的 80-bit space 先放 Storage32 再放 Reference48；CDW3 high16 屬 Storage、low16 屬 Reference。Figure171 的重疊 range 需交叉查 Figure166／170。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

STS=32 的 80-bit space 先放 Storage32 再放 Reference48；CDW3 high16 屬 Storage、low16 屬 Reference。Figure171 的重疊 range 需交叉查 Figure166／170。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Storage32, Reference48, CDW2, CDW3, CDW14 — STS=32 的 80-bit space 先放 Storage32 再放 Reference48；CDW3 high16 屬 Storage、low16 屬 Reference。Figure171 的重疊 range 需交叉查 Figure166／170。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. STS=32 的 80-bit space 先放 Storage32 再放 Reference48；CDW3 high16 屬 Storage、low16 屬 Reference。Figure171 的重疊 range 需交叉查 Figure166／170。
3. 先決定總 space 大小，再切 tag，最後拆到命令 Dwords。不要因 tag 的名稱相似就把 Write 的值與 Read 的 expected 值交換。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 170 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | STS=32 的 80-bit space 先放 Storage32 再放 Reference48；CDW3 high16 屬 Storage、low16 屬 Reference。Figure171 的重疊 range 需交叉查 Figure166／170。 |
| 邊界 | Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。 |

**說明性範例。** 64b Guard、STS=18、Storage Tag=0x12345、Reference Tag=0x2A：CDW3 low16=0x48D1，CDW14=(1<<30)|0x2A=0x4000002A。Read 使用相同布局的 expected tags。

**常見誤解。** Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Storage32, Reference48, CDW2, CDW3, CDW14

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 170, 文件頁 140, PDF 頁 140

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 171: 32b Guard Protection Information Read Command Example</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-171-CLAIM figure-table:NVMCS13-NVM-FIG-171 -->

**SPEC。** Figure 171〈32b Guard Protection Information Read Command Example〉：STS=32 的 80-bit space 先放 Storage32 再放 Reference48；CDW3 high16 屬 Storage、low16 屬 Reference。Figure171 的重疊 range 需交叉查 Figure166／170。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

STS=32 的 80-bit space 先放 Storage32 再放 Reference48；CDW3 high16 屬 Storage、low16 屬 Reference。Figure171 的重疊 range 需交叉查 Figure166／170。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Storage32, Reference48, CDW2, CDW3, CDW14 — STS=32 的 80-bit space 先放 Storage32 再放 Reference48；CDW3 high16 屬 Storage、low16 屬 Reference。Figure171 的重疊 range 需交叉查 Figure166／170。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. STS=32 的 80-bit space 先放 Storage32 再放 Reference48；CDW3 high16 屬 Storage、low16 屬 Reference。Figure171 的重疊 range 需交叉查 Figure166／170。
3. 先決定總 space 大小，再切 tag，最後拆到命令 Dwords。不要因 tag 的名稱相似就把 Write 的值與 Read 的 expected 值交換。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 171 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | STS=32 的 80-bit space 先放 Storage32 再放 Reference48；CDW3 high16 屬 Storage、low16 屬 Reference。Figure171 的重疊 range 需交叉查 Figure166／170。 |
| 邊界 | Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。 |

**說明性範例。** 64b Guard、STS=18、Storage Tag=0x12345、Reference Tag=0x2A：CDW3 low16=0x48D1，CDW14=(1<<30)|0x2A=0x4000002A。Read 使用相同布局的 expected tags。

**常見誤解。** Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Storage32, Reference48, CDW2, CDW3, CDW14

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 171, 文件頁 140, PDF 頁 140

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 172: 64b Guard Protection Information Write Command Example</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-172-CLAIM figure-table:NVMCS13-NVM-FIG-172 -->

**SPEC。** Figure 172〈64b Guard Protection Information Write Command Example〉：48-bit space 且 STS=18 時，Storage 低2 bits 進 CDW14 high2，其餘 Reference30 佔 CDW14 low30。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

48-bit space 且 STS=18 時，Storage 低2 bits 進 CDW14 high2，其餘 Reference30 佔 CDW14 low30。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Storage18, Reference30, CDW3, CDW14 — 48-bit space 且 STS=18 時，Storage 低2 bits 進 CDW14 high2，其餘 Reference30 佔 CDW14 low30。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 48-bit space 且 STS=18 時，Storage 低2 bits 進 CDW14 high2，其餘 Reference30 佔 CDW14 low30。
3. 先決定總 space 大小，再切 tag，最後拆到命令 Dwords。不要因 tag 的名稱相似就把 Write 的值與 Read 的 expected 值交換。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 172 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 48-bit space 且 STS=18 時，Storage 低2 bits 進 CDW14 high2，其餘 Reference30 佔 CDW14 low30。 |
| 邊界 | Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。 |

**說明性範例。** 64b Guard、STS=18、Storage Tag=0x12345、Reference Tag=0x2A：CDW3 low16=0x48D1，CDW14=(1<<30)|0x2A=0x4000002A。Read 使用相同布局的 expected tags。

**常見誤解。** Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Storage18, Reference30, CDW3, CDW14

**來源 keyword 索引：** may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 172, 文件頁 141, PDF 頁 141

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 173: 64b Guard Protection Information Read Command Example</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-173-CLAIM figure-table:NVMCS13-NVM-FIG-173 -->

**SPEC。** Figure 173〈64b Guard Protection Information Read Command Example〉：48-bit space 且 STS=18 時，Storage 低2 bits 進 CDW14 high2，其餘 Reference30 佔 CDW14 low30。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

48-bit space 且 STS=18 時，Storage 低2 bits 進 CDW14 high2，其餘 Reference30 佔 CDW14 low30。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Storage18, Reference30, CDW3, CDW14 — 48-bit space 且 STS=18 時，Storage 低2 bits 進 CDW14 high2，其餘 Reference30 佔 CDW14 low30。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 48-bit space 且 STS=18 時，Storage 低2 bits 進 CDW14 high2，其餘 Reference30 佔 CDW14 low30。
3. 先決定總 space 大小，再切 tag，最後拆到命令 Dwords。不要因 tag 的名稱相似就把 Write 的值與 Read 的 expected 值交換。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 173 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 48-bit space 且 STS=18 時，Storage 低2 bits 進 CDW14 high2，其餘 Reference30 佔 CDW14 low30。 |
| 邊界 | Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。 |

**說明性範例。** 64b Guard、STS=18、Storage Tag=0x12345、Reference Tag=0x2A：CDW3 low16=0x48D1，CDW14=(1<<30)|0x2A=0x4000002A。Read 使用相同布局的 expected tags。

**常見誤解。** Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Storage18, Reference30, CDW3, CDW14

**來源 keyword 索引：** may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 173, 文件頁 141, PDF 頁 141

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 174: Write Command 16b Guard Protection Information Processing</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-174-CLAIM figure-table:NVMCS13-NVM-FIG-174 -->

**SPEC。** Figure 174〈Write Command 16b Guard Protection Information Processing〉：Write PRACT=0 保留 host PI；PRACT=1 在 MS=PI 時插入、MS>PI 時取代。生成 PI 的分支忽略 checking bits。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Write PRACT=0 保留 host PI；PRACT=1 在 MS=PI 時插入、MS>PI 時取代。生成 PI 的分支忽略 checking bits。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PRACT]
          ↓
[擷取欄位: MS] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PRACT` | Protection Information Action；依命令與 MS 選擇 PI 處理。 |
| `MS` | 每個 logical block 的 metadata bytes；與 PI size 比較以判斷 PRACT 的傳輸效果。 |
| `相關欄位` | Write, PI — Write PRACT=0 保留 host PI；PRACT=1 在 MS=PI 時插入、MS>PI 時取代。生成 PI 的分支忽略 checking bits。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Write PRACT=0 保留 host PI；PRACT=1 在 MS=PI 時插入、MS>PI 時取代。生成 PI 的分支忽略 checking bits。
3. 先檢查 namespace 是否啟用 PI，再依命令方向及 metadata 大小選處理分支。Checking bits 與可能的特殊停用值放在最後判斷。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 174 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.2.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Write PRACT=0 保留 host PI；PRACT=1 在 MS=PI 時插入、MS>PI 時取代。生成 PI 的分支忽略 checking bits。 |
| 邊界 | STC 在本份指 Storage Tag Check；不要沿用 Self-test Code 的縮寫解釋。Compare 的兩條輸入路徑都可能執行 PI checking，但 PI bytes 不納入一般 metadata 比對。 |

**說明性範例。** 16b Guard、MS=16、Read PRACT=1：host 仍接收 16 bytes metadata；若 MS=8，則 host 只接收 data。相同 PRACT 在不同 MS 下造成不同 buffer 大小。

**常見誤解。** STC 在本份指 Storage Tag Check；不要沿用 Self-test Code 的縮寫解釋。Compare 的兩條輸入路徑都可能執行 PI checking，但 PI bytes 不納入一般 metadata 比對。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | STC 在本份指 Storage Tag Check；不要沿用 Self-test Code 的縮寫解釋。Compare 的兩條輸入路徑都可能執行 PI checking，但 PI bytes 不納入一般 metadata 比對。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Write, PRACT, MS, PI

**來源 keyword 索引：** may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.1, Figure 174, 文件頁 143, PDF 頁 143

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 175: Read 16b Guard Command Protection Information Processing</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-175-CLAIM figure-table:NVMCS13-NVM-FIG-175 -->

**SPEC。** Figure 175〈Read 16b Guard Command Protection Information Processing〉：Read 先依要求檢查；PRACT=1 且 MS=PI 才 strip，MS>PI 則仍把 PI 隨 metadata 回傳。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Read 先依要求檢查；PRACT=1 且 MS=PI 才 strip，MS>PI 則仍把 PI 隨 metadata 回傳。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: PRACT]
          ↓
[擷取欄位: MS] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `PRACT` | Protection Information Action；依命令與 MS 選擇 PI 處理。 |
| `MS` | 每個 logical block 的 metadata bytes；與 PI size 比較以判斷 PRACT 的傳輸效果。 |
| `相關欄位` | Read, PI — Read 先依要求檢查；PRACT=1 且 MS=PI 才 strip，MS>PI 則仍把 PI 隨 metadata 回傳。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Read 先依要求檢查；PRACT=1 且 MS=PI 才 strip，MS>PI 則仍把 PI 隨 metadata 回傳。
3. 先檢查 namespace 是否啟用 PI，再依命令方向及 metadata 大小選處理分支。Checking bits 與可能的特殊停用值放在最後判斷。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 175 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.2.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Read 先依要求檢查；PRACT=1 且 MS=PI 才 strip，MS>PI 則仍把 PI 隨 metadata 回傳。 |
| 邊界 | STC 在本份指 Storage Tag Check；不要沿用 Self-test Code 的縮寫解釋。Compare 的兩條輸入路徑都可能執行 PI checking，但 PI bytes 不納入一般 metadata 比對。 |

**說明性範例。** 16b Guard、MS=16、Read PRACT=1：host 仍接收 16 bytes metadata；若 MS=8，則 host 只接收 data。相同 PRACT 在不同 MS 下造成不同 buffer 大小。

**常見誤解。** STC 在本份指 Storage Tag Check；不要沿用 Self-test Code 的縮寫解釋。Compare 的兩條輸入路徑都可能執行 PI checking，但 PI bytes 不納入一般 metadata 比對。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | STC 在本份指 Storage Tag Check；不要沿用 Self-test Code 的縮寫解釋。Compare 的兩條輸入路徑都可能執行 PI checking，但 PI bytes 不納入一般 metadata 比對。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Read, PRACT, MS, PI

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.2, Figure 175, 文件頁 145, PDF 頁 145

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 176: Protection Information Processing for Compare</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-176-CLAIM figure-table:NVMCS13-NVM-FIG-176 -->

**SPEC。** Figure 176〈Protection Information Processing for Compare〉：Compare 的 host 與 media 輸入各有 PI checking；一般比較涵蓋 data 與非 PI metadata，不能只比對 PI 就宣告內容相同。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Compare 的 host 與 media 輸入各有 PI checking；一般比較涵蓋 data 與非 PI metadata，不能只比對 PI 就宣告內容相同。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Host input, Media input, PI checks, Compare — Compare 的 host 與 media 輸入各有 PI checking；一般比較涵蓋 data 與非 PI metadata，不能只比對 PI 就宣告內容相同。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Compare 的 host 與 media 輸入各有 PI checking；一般比較涵蓋 data 與非 PI metadata，不能只比對 PI 就宣告內容相同。
3. 先檢查 namespace 是否啟用 PI，再依命令方向及 metadata 大小選處理分支。Checking bits 與可能的特殊停用值放在最後判斷。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 176 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.2.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Compare 的 host 與 media 輸入各有 PI checking；一般比較涵蓋 data 與非 PI metadata，不能只比對 PI 就宣告內容相同。 |
| 邊界 | STC 在本份指 Storage Tag Check；不要沿用 Self-test Code 的縮寫解釋。Compare 的兩條輸入路徑都可能執行 PI checking，但 PI bytes 不納入一般 metadata 比對。 |

**說明性範例。** 16b Guard、MS=16、Read PRACT=1：host 仍接收 16 bytes metadata；若 MS=8，則 host 只接收 data。相同 PRACT 在不同 MS 下造成不同 buffer 大小。

**常見誤解。** STC 在本份指 Storage Tag Check；不要沿用 Self-test Code 的縮寫解釋。Compare 的兩條輸入路徑都可能執行 PI checking，但 PI bytes 不納入一般 metadata 比對。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | STC 在本份指 Storage Tag Check；不要沿用 Self-test Code 的縮寫解釋。Compare 的兩條輸入路徑都可能執行 PI checking，但 PI bytes 不納入一般 metadata 比對。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Host input, Media input, PI checks, Compare

**來源 keyword 索引：** may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.4, Figure 176, 文件頁 146, PDF 頁 146

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 177: PI Processing for Copy MD=8 Pass-through</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-177-CLAIM figure-table:NVMCS13-NVM-FIG-177 -->

**SPEC。** Figure 177〈PI Processing for Copy MD=8 Pass-through〉：這兩圖是 matching PI formats 的 pass-through：讀／寫 PRACT 都為0；metadata 大小不同的兩個例子仍須保留各自 layout。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

這兩圖是 matching PI formats 的 pass-through：讀／寫 PRACT 都為0；metadata 大小不同的兩個例子仍須保留各自 layout。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | PRINFOR.PRACT=0, PRINFOW.PRACT=0, Pass-through — 這兩圖是 matching PI formats 的 pass-through：讀／寫 PRACT 都為0；metadata 大小不同的兩個例子仍須保留各自 layout。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 這兩圖是 matching PI formats 的 pass-through：讀／寫 PRACT 都為0；metadata 大小不同的兩個例子仍須保留各自 layout。
3. 以來源與目的是否有 PI 建立四種情況，再決定 PRINFOR.PRACT 與 PRINFOW.PRACT。每個 source 都必須符合選定模式。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 177 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.2.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 這兩圖是 matching PI formats 的 pass-through：讀／寫 PRACT 都為0；metadata 大小不同的兩個例子仍須保留各自 layout。 |
| 邊界 | §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。 |

**說明性範例。** 4096+8 bytes 的 16b PI namespace 可在符合 corresponding 條件時轉到 4096+0 bytes；4096+16 bytes 且其中 8 bytes 是額外 metadata，不能走這個 strip 特例。

**常見誤解。** §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** PRINFOR.PRACT=0, PRINFOW.PRACT=0, Pass-through

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.5, Figure 177, 文件頁 147, PDF 頁 147

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 178: PI Processing for Copy MD=16 Pass-through</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-178-CLAIM figure-table:NVMCS13-NVM-FIG-178 -->

**SPEC。** Figure 178〈PI Processing for Copy MD=16 Pass-through〉：這兩圖是 matching PI formats 的 pass-through：讀／寫 PRACT 都為0；metadata 大小不同的兩個例子仍須保留各自 layout。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

這兩圖是 matching PI formats 的 pass-through：讀／寫 PRACT 都為0；metadata 大小不同的兩個例子仍須保留各自 layout。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | PRINFOR.PRACT=0, PRINFOW.PRACT=0, Pass-through — 這兩圖是 matching PI formats 的 pass-through：讀／寫 PRACT 都為0；metadata 大小不同的兩個例子仍須保留各自 layout。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 這兩圖是 matching PI formats 的 pass-through：讀／寫 PRACT 都為0；metadata 大小不同的兩個例子仍須保留各自 layout。
3. 以來源與目的是否有 PI 建立四種情況，再決定 PRINFOR.PRACT 與 PRINFOW.PRACT。每個 source 都必須符合選定模式。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 178 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.2.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 這兩圖是 matching PI formats 的 pass-through：讀／寫 PRACT 都為0；metadata 大小不同的兩個例子仍須保留各自 layout。 |
| 邊界 | §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。 |

**說明性範例。** 4096+8 bytes 的 16b PI namespace 可在符合 corresponding 條件時轉到 4096+0 bytes；4096+16 bytes 且其中 8 bytes 是額外 metadata，不能走這個 strip 特例。

**常見誤解。** §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** PRINFOR.PRACT=0, PRINFOW.PRACT=0, Pass-through

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.5, Figure 178, 文件頁 147, PDF 頁 147

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 179: PI Processing for Copy MD=8 Replace</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-179-CLAIM figure-table:NVMCS13-NVM-FIG-179 -->

**SPEC。** Figure 179〈PI Processing for Copy MD=8 Replace〉：這兩圖是 matching PI formats 的 replace：讀／寫 PRACT 都為1；來源 PI 檢查與目的 PI 產生有不同角色。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

這兩圖是 matching PI formats 的 replace：讀／寫 PRACT 都為1；來源 PI 檢查與目的 PI 產生有不同角色。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | PRINFOR.PRACT=1, PRINFOW.PRACT=1, Replace — 這兩圖是 matching PI formats 的 replace：讀／寫 PRACT 都為1；來源 PI 檢查與目的 PI 產生有不同角色。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 這兩圖是 matching PI formats 的 replace：讀／寫 PRACT 都為1；來源 PI 檢查與目的 PI 產生有不同角色。
3. 以來源與目的是否有 PI 建立四種情況，再決定 PRINFOR.PRACT 與 PRINFOW.PRACT。每個 source 都必須符合選定模式。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 179 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.2.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 這兩圖是 matching PI formats 的 replace：讀／寫 PRACT 都為1；來源 PI 檢查與目的 PI 產生有不同角色。 |
| 邊界 | §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。 |

**說明性範例。** 4096+8 bytes 的 16b PI namespace 可在符合 corresponding 條件時轉到 4096+0 bytes；4096+16 bytes 且其中 8 bytes 是額外 metadata，不能走這個 strip 特例。

**常見誤解。** §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** PRINFOR.PRACT=1, PRINFOW.PRACT=1, Replace

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.5, Figure 179, 文件頁 148, PDF 頁 148

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 180: PI Processing for Copy MD=16 Replace</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-180-CLAIM figure-table:NVMCS13-NVM-FIG-180 -->

**SPEC。** Figure 180〈PI Processing for Copy MD=16 Replace〉：這兩圖是 matching PI formats 的 replace：讀／寫 PRACT 都為1；來源 PI 檢查與目的 PI 產生有不同角色。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

這兩圖是 matching PI formats 的 replace：讀／寫 PRACT 都為1；來源 PI 檢查與目的 PI 產生有不同角色。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | PRINFOR.PRACT=1, PRINFOW.PRACT=1, Replace — 這兩圖是 matching PI formats 的 replace：讀／寫 PRACT 都為1；來源 PI 檢查與目的 PI 產生有不同角色。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 這兩圖是 matching PI formats 的 replace：讀／寫 PRACT 都為1；來源 PI 檢查與目的 PI 產生有不同角色。
3. 以來源與目的是否有 PI 建立四種情況，再決定 PRINFOR.PRACT 與 PRINFOW.PRACT。每個 source 都必須符合選定模式。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 180 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.2.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 這兩圖是 matching PI formats 的 replace：讀／寫 PRACT 都為1；來源 PI 檢查與目的 PI 產生有不同角色。 |
| 邊界 | §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。 |

**說明性範例。** 4096+8 bytes 的 16b PI namespace 可在符合 corresponding 條件時轉到 4096+0 bytes；4096+16 bytes 且其中 8 bytes 是額外 metadata，不能走這個 strip 特例。

**常見誤解。** §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** PRINFOR.PRACT=1, PRINFOW.PRACT=1, Replace

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.5, Figure 180, 文件頁 148, PDF 頁 148

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 181: PI Processing for Copy MD=8 Insert</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-181-CLAIM figure-table:NVMCS13-NVM-FIG-181 -->

**SPEC。** Figure 181〈PI Processing for Copy MD=8 Insert〉：只有 corresponding PI formats 且 destination metadata 全為 PI 時使用 insert 特例，write PRACT 必須1。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

只有 corresponding PI formats 且 destination metadata 全為 PI 時使用 insert 特例，write PRACT 必須1。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Source no PI, Destination PI, Insert — 只有 corresponding PI formats 且 destination metadata 全為 PI 時使用 insert 特例，write PRACT 必須1。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 只有 corresponding PI formats 且 destination metadata 全為 PI 時使用 insert 特例，write PRACT 必須1。
3. 以來源與目的是否有 PI 建立四種情況，再決定 PRINFOR.PRACT 與 PRINFOW.PRACT。每個 source 都必須符合選定模式。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 181 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.2.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 只有 corresponding PI formats 且 destination metadata 全為 PI 時使用 insert 特例，write PRACT 必須1。 |
| 邊界 | §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。 |

**說明性範例。** 4096+8 bytes 的 16b PI namespace 可在符合 corresponding 條件時轉到 4096+0 bytes；4096+16 bytes 且其中 8 bytes 是額外 metadata，不能走這個 strip 特例。

**常見誤解。** §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Source no PI, Destination PI, Insert

**來源 keyword 索引：** should

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.5, Figure 181, 文件頁 149, PDF 頁 149

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 182: PI Processing for Copy MD=8 Strip</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-182-CLAIM figure-table:NVMCS13-NVM-FIG-182 -->

**SPEC。** Figure 182〈PI Processing for Copy MD=8 Strip〉：只有 corresponding PI formats 且 source metadata 全為 PI 時使用 strip 特例，read PRACT 必須1。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

只有 corresponding PI formats 且 source metadata 全為 PI 時使用 strip 特例，read PRACT 必須1。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Source PI, Destination no PI, Strip — 只有 corresponding PI formats 且 source metadata 全為 PI 時使用 strip 特例，read PRACT 必須1。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 只有 corresponding PI formats 且 source metadata 全為 PI 時使用 strip 特例，read PRACT 必須1。
3. 以來源與目的是否有 PI 建立四種情況，再決定 PRINFOR.PRACT 與 PRINFOW.PRACT。每個 source 都必須符合選定模式。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 182 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.3.2.5 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 只有 corresponding PI formats 且 source metadata 全為 PI 時使用 strip 特例，read PRACT 必須1。 |
| 邊界 | §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。 |

**說明性範例。** 4096+8 bytes 的 16b PI namespace 可在符合 corresponding 條件時轉到 4096+0 bytes；4096+16 bytes 且其中 8 bytes 是額外 metadata，不能走這個 strip 特例。

**常見誤解。** §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | §5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Source PI, Destination no PI, Strip

**來源 keyword 索引：** should

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.5, Figure 182, 文件頁 149, PDF 頁 149

</details>

<a id="section-5-4"></a>

### §5.4

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 183: Reference Exported Configuration State</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-183-CLAIM figure-table:NVMCS13-NVM-FIG-183 -->

**SPEC。** Figure 183〈Reference Exported Configuration State〉：先分固定 364-byte controller configuration 與 48-byte namespace configuration；總長 412 bytes，僅能單筆設定一次。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

先分固定 364-byte controller configuration 與 48-byte namespace configuration；總長 412 bytes，僅能單筆設定一次。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: RECCS]
          ↓
[擷取欄位: RENSCS] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `RECCS` | Reference Exported Controller／Namespace Configuration State；分別是 364／48 bytes。 |
| `RENSCS` | Reference Exported Controller／Namespace Configuration State；分別是 364／48 bytes。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 先分固定 364-byte controller configuration 與 48-byte namespace configuration；總長 412 bytes，僅能單筆設定一次。
3. 範本固定的相容性介面與 underlying 裝置能力是兩層。先確認 namespace 格式相容，再設定不超過 underlying 能力的限制；沒有被範本開放的能力不能自行宣告。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 183 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 先分固定 364-byte controller configuration 與 48-byte namespace configuration；總長 412 bytes，僅能單筆設定一次。 |
| 邊界 | Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。 |

**說明性範例。** Underlying NCQS=7 可支援 8 queues，範本設定 NCQS=3 表示最多 4 queues；不能把 raw 3 誤解成 3 queues。Namespace 的 NGUID 為零時，NUUID 必須提供有效 UUID。

**常見誤解。** Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** RECCS, RENSCS

**來源 keyword 索引：** shall, mandatory

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 183, 文件頁 153, PDF 頁 153

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 184: Reference Controller Capabilities Register Values</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-184-CLAIM figure-table:NVMCS13-NVM-FIG-184 -->

**SPEC。** Figure 184〈Reference Controller Capabilities Register Values〉：未列出的 CAP bits 清零；CSS 表示僅 NVM，TO=FFh 表示 127.5 秒，queues 要 physically contiguous，MQES 受 underlying 限制。圖中 CQE 名稱對應 contiguous-queue 欄位。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

未列出的 CAP bits 清零；CSS 表示僅 NVM，TO=FFh 表示 127.5 秒，queues 要 physically contiguous，MQES 受 underlying 限制。圖中 CQE 名稱對應 contiguous-queue 欄位。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: TO]
          ↓
[擷取欄位: MQES] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `TO` | CAP Timeout；每單位 500 ms，FFh 為 127.5 秒。 |
| `MQES` | 支援的 completion／submission queue 數與 queue entries；先解 0-based，再核對 underlying 上限。 |
| `相關欄位` | CSS, CQR — 未列出的 CAP bits 清零；CSS 表示僅 NVM，TO=FFh 表示 127.5 秒，queues 要 physically contiguous，MQES 受 underlying 限制。圖中 CQE 名稱對應 contiguous-queue 欄位。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 未列出的 CAP bits 清零；CSS 表示僅 NVM，TO=FFh 表示 127.5 秒，queues 要 physically contiguous，MQES 受 underlying 限制。圖中 CQE 名稱對應 contiguous-queue 欄位。
3. 範本固定的相容性介面與 underlying 裝置能力是兩層。先確認 namespace 格式相容，再設定不超過 underlying 能力的限制；沒有被範本開放的能力不能自行宣告。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 184 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 未列出的 CAP bits 清零；CSS 表示僅 NVM，TO=FFh 表示 127.5 秒，queues 要 physically contiguous，MQES 受 underlying 限制。圖中 CQE 名稱對應 contiguous-queue 欄位。 |
| 邊界 | Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。 |

**說明性範例。** Underlying NCQS=7 可支援 8 queues，範本設定 NCQS=3 表示最多 4 queues；不能把 raw 3 誤解成 3 queues。Namespace 的 NGUID 為零時，NUUID 必須提供有效 UUID。

**常見誤解。** Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** CSS, TO, CQR, MQES

**來源 keyword 索引：** shall, mandatory

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 184, 文件頁 153, PDF 頁 153

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 185: Reference Version Register Values</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-185-CLAIM figure-table:NVMCS13-NVM-FIG-185 -->

**SPEC。** Figure 185〈Reference Version Register Values〉：範本的 VS 固定 020300h，即 2.3.0；不要因手上的 Base 版本為 2.4 就改成 2.4。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

範本的 VS 固定 020300h，即 2.3.0；不要因手上的 Base 版本為 2.4 就改成 2.4。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | MJR, MNR, TER — 範本的 VS 固定 020300h，即 2.3.0；不要因手上的 Base 版本為 2.4 就改成 2.4。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 範本的 VS 固定 020300h，即 2.3.0；不要因手上的 Base 版本為 2.4 就改成 2.4。
3. 範本固定的相容性介面與 underlying 裝置能力是兩層。先確認 namespace 格式相容，再設定不超過 underlying 能力的限制；沒有被範本開放的能力不能自行宣告。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 185 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 範本的 VS 固定 020300h，即 2.3.0；不要因手上的 Base 版本為 2.4 就改成 2.4。 |
| 邊界 | Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。 |

**說明性範例。** Underlying NCQS=7 可支援 8 queues，範本設定 NCQS=3 表示最多 4 queues；不能把 raw 3 誤解成 3 queues。Namespace 的 NGUID 為零時，NUUID 必須提供有效 UUID。

**常見誤解。** Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** MJR, MNR, TER

**來源 keyword 索引：** shall, mandatory

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 185, 文件頁 153, PDF 頁 153

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 186: Reference Firmware Slot Information Log Page</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-186-CLAIM figure-table:NVMCS13-NVM-FIG-186 -->

**SPEC。** Figure 186〈Reference Firmware Slot Information Log Page〉：Active firmware slot 固定為 1；其餘 firmware log 值依零值規則及 configuration state 的 FR exception。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Active firmware slot 固定為 1；其餘 firmware log 值依零值規則及 configuration state 的 FR exception。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | AFI, FRS1 — Active firmware slot 固定為 1；其餘 firmware log 值依零值規則及 configuration state 的 FR exception。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Active firmware slot 固定為 1；其餘 firmware log 值依零值規則及 configuration state 的 FR exception。
3. 範本固定的相容性介面與 underlying 裝置能力是兩層。先確認 namespace 格式相容，再設定不超過 underlying 能力的限制；沒有被範本開放的能力不能自行宣告。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 186 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Active firmware slot 固定為 1；其餘 firmware log 值依零值規則及 configuration state 的 FR exception。 |
| 邊界 | Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。 |

**說明性範例。** Underlying NCQS=7 可支援 8 queues，範本設定 NCQS=3 表示最多 4 queues；不能把 raw 3 誤解成 3 queues。Namespace 的 NGUID 為零時，NUUID 必須提供有效 UUID。

**常見誤解。** Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** AFI, FRS1

**來源 keyword 索引：** shall

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 186, 文件頁 154, PDF 頁 154

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 187: Reference Feature Default Values</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-187-CLAIM figure-table:NVMCS13-NVM-FIG-187 -->

**SPEC。** Figure 187〈Reference Feature Default Values〉：Composite over／under 預設 FFFFh／0；IV=0 的 CD=1，其他 IV 的 CD=0。Number of Queues 取決於請求與配置結果，不是固定零。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Composite over／under 預設 FFFFh／0；IV=0 的 CD=1，其他 IV 的 CD=0。Number of Queues 取決於請求與配置結果，不是固定零。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NCQS]
          ↓
[擷取欄位: NSQS] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NCQS` | 支援的 completion／submission queue 數與 queue entries；先解 0-based，再核對 underlying 上限。 |
| `NSQS` | 支援的 completion／submission queue 數與 queue entries；先解 0-based，再核對 underlying 上限。 |
| `相關欄位` | TMPSEL, THSEL, TMPTH, IV, CD — Composite over／under 預設 FFFFh／0；IV=0 的 CD=1，其他 IV 的 CD=0。Number of Queues 取決於請求與配置結果，不是固定零。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Composite over／under 預設 FFFFh／0；IV=0 的 CD=1，其他 IV 的 CD=0。Number of Queues 取決於請求與配置結果，不是固定零。
3. 範本固定的相容性介面與 underlying 裝置能力是兩層。先確認 namespace 格式相容，再設定不超過 underlying 能力的限制；沒有被範本開放的能力不能自行宣告。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 187 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Composite over／under 預設 FFFFh／0；IV=0 的 CD=1，其他 IV 的 CD=0。Number of Queues 取決於請求與配置結果，不是固定零。 |
| 邊界 | Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。 |

**說明性範例。** Underlying NCQS=7 可支援 8 queues，範本設定 NCQS=3 表示最多 4 queues；不能把 raw 3 誤解成 3 queues。Namespace 的 NGUID 為零時，NUUID 必須提供有效 UUID。

**常見誤解。** Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** TMPSEL, THSEL, TMPTH, IV, CD, NCQS, NSQS

**來源 keyword 索引：** shall

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 187, 文件頁 155, PDF 頁 155

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 188: Reference Identify Controller or Namespace Data Structures</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-188-CLAIM figure-table:NVMCS13-NVM-FIG-188 -->

**SPEC。** Figure 188〈Reference Identify Controller or Namespace Data Structures〉：Identify 只開放列出的 exceptions：NCAP=NSZE、SQES=66h 為 64-byte SQE、CQES=44h 為 16-byte CQE；CNS06h 的 NVM VER 固定 1.2.0。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Identify 只開放列出的 exceptions：NCAP=NSZE、SQES=66h 為 64-byte SQE、CQES=44h 為 16-byte CQE；CNS06h 的 NVM VER 固定 1.2.0。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSZE]
          ↓
[擷取欄位: NCAP] → [套用編碼: SQES]
                                      ↓
[驗證證據: CQES]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSZE` | Namespace Size；可定址 logical blocks 總數。 |
| `NCAP` | Namespace Capacity；同時可配置 logical blocks 最大數量。 |
| `SQES` | Submission／Completion Queue Entry Size；nibbles 以 2 的次方表示最小／最大 bytes。 |
| `CQES` | Submission／Completion Queue Entry Size；nibbles 以 2 的次方表示最小／最大 bytes。 |
| `相關欄位` | NSFEAT, VER, NGUID, UUID — Identify 只開放列出的 exceptions：NCAP=NSZE、SQES=66h 為 64-byte SQE、CQES=44h 為 16-byte CQE；CNS06h 的 NVM VER 固定 1.2.0。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Identify 只開放列出的 exceptions：NCAP=NSZE、SQES=66h 為 64-byte SQE、CQES=44h 為 16-byte CQE；CNS06h 的 NVM VER 固定 1.2.0。
3. 範本固定的相容性介面與 underlying 裝置能力是兩層。先確認 namespace 格式相容，再設定不超過 underlying 能力的限制；沒有被範本開放的能力不能自行宣告。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 188 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Identify 只開放列出的 exceptions：NCAP=NSZE、SQES=66h 為 64-byte SQE、CQES=44h 為 16-byte CQE；CNS06h 的 NVM VER 固定 1.2.0。 |
| 邊界 | Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。 |

**說明性範例。** Underlying NCQS=7 可支援 8 queues，範本設定 NCQS=3 表示最多 4 queues；不能把 raw 3 誤解成 3 queues。Namespace 的 NGUID 為零時，NUUID 必須提供有效 UUID。

**常見誤解。** Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NSZE, NCAP, NSFEAT, VER, SQES, CQES, NGUID, UUID

**來源 keyword 索引：** shall, should

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 188, 文件頁 156, PDF 頁 156

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 189: Reference Exported Controller Configuration State</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-189-CLAIM figure-table:NVMCS13-NVM-FIG-189 -->

**SPEC。** Figure 189〈Reference Exported Controller Configuration State〉：本機欄位 slice：ECNTLID=0，限制值不得超過 underlying；NCQS／NSQS 先解 0-based。WZS／DSMS 需對應底層能力與所報 Commands Supported and Effects。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

本機欄位 slice：ECNTLID=0，限制值不得超過 underlying；NCQS／NSQS 先解 0-based。WZS／DSMS 需對應底層能力與所報 Commands Supported and Effects。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MDTS]
          ↓
[擷取欄位: NCQS] → [套用編碼: NSQS]
                                      ↓
[驗證證據: MQES]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MDTS` | Maximum Data Transfer Size；以 minimum page size 為基準的 exponent；零有特定無限制語意。 |
| `NCQS` | 支援的 completion／submission queue 數與 queue entries；先解 0-based，再核對 underlying 上限。 |
| `NSQS` | 支援的 completion／submission queue 數與 queue entries；先解 0-based，再核對 underlying 上限。 |
| `MQES` | 支援的 completion／submission queue 數與 queue entries；先解 0-based，再核對 underlying 上限。 |
| `ONCS` | Optional NVM Commands Supported；包含能力及 variant，需結合 NVM Identify 的 limits。 |
| `AWUN` | Atomic Write Unit Normal；controller 正常原子寫入大小的 0-based 欄位。 |
| `AWUPF` | Atomic Write Unit Power Fail；失敗條件原子大小的0-based欄位。 |
| `相關欄位` | ECNTLID, RAB — 本機欄位 slice：ECNTLID=0，限制值不得超過 underlying；NCQS／NSQS 先解 0-based。WZS／DSMS 需對應底層能力與所報 Commands Supported and Effects。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 本機欄位 slice：ECNTLID=0，限制值不得超過 underlying；NCQS／NSQS 先解 0-based。WZS／DSMS 需對應底層能力與所報 Commands Supported and Effects。
3. 範本固定的相容性介面與 underlying 裝置能力是兩層。先確認 namespace 格式相容，再設定不超過 underlying 能力的限制；沒有被範本開放的能力不能自行宣告。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 189 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 本機欄位 slice：ECNTLID=0，限制值不得超過 underlying；NCQS／NSQS 先解 0-based。WZS／DSMS 需對應底層能力與所報 Commands Supported and Effects。 |
| 邊界 | Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。 |

**說明性範例。** Underlying NCQS=7 可支援 8 queues，範本設定 NCQS=3 表示最多 4 queues；不能把 raw 3 誤解成 3 queues。Namespace 的 NGUID 為零時，NUUID 必須提供有效 UUID。

**常見誤解。** Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** ECNTLID, MDTS, RAB, NCQS, NSQS, MQES, ONCS, AWUN, AWUPF

**來源 keyword 索引：** shall, may, optional, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 189, 文件頁 157-158, PDF 頁 157-158

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 190: Reference Exported Controller Configuration State</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-190-CLAIM figure-table:NVMCS13-NVM-FIG-190 -->

**SPEC。** Figure 190〈Reference Exported Controller Configuration State〉：caption 雖寫 Controller，內容是 namespace：ENSID=1、MS=0、RP=0；LBADS 必須與 underlying 相同。NGUID=0 時 NUUID 必須有效。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

caption 雖寫 Controller，內容是 namespace：ENSID=1、MS=0、RP=0；LBADS 必須與 underlying 相同。NGUID=0 時 NUUID 必須有效。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ENSID]
          ↓
[擷取欄位: NAWUN] → [套用編碼: NAWUPF]
                                      ↓
[驗證證據: 相關欄位]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ENSID` | Namespace 識別碼；SNSID 選 Copy 來源，ENSID 選匯出 namespace，合法值受個別命令約束。 |
| `NAWUN` | Namespace normal／power-fail／compare-and-write 或 controller compare-and-write 原子大小；0-based。 |
| `NAWUPF` | Namespace normal／power-fail／compare-and-write 或 controller compare-and-write 原子大小；0-based。 |
| `相關欄位` | LBAF0, NGUID, NUUID — caption 雖寫 Controller，內容是 namespace：ENSID=1、MS=0、RP=0；LBADS 必須與 underlying 相同。NGUID=0 時 NUUID 必須有效。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. caption 雖寫 Controller，內容是 namespace：ENSID=1、MS=0、RP=0；LBADS 必須與 underlying 相同。NGUID=0 時 NUUID 必須有效。
3. 範本固定的相容性介面與 underlying 裝置能力是兩層。先確認 namespace 格式相容，再設定不超過 underlying 能力的限制；沒有被範本開放的能力不能自行宣告。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 190 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | caption 雖寫 Controller，內容是 namespace：ENSID=1、MS=0、RP=0；LBADS 必須與 underlying 相同。NGUID=0 時 NUUID 必須有效。 |
| 邊界 | Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。 |

**說明性範例。** Underlying NCQS=7 可支援 8 queues，範本設定 NCQS=3 表示最多 4 queues；不能把 raw 3 誤解成 3 queues。Namespace 的 NGUID 為零時，NUUID 必須提供有效 UUID。

**常見誤解。** Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** ENSID, LBAF0, NAWUN, NAWUPF, NGUID, NUUID

**來源 keyword 索引：** shall, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 190, 文件頁 158-159, PDF 頁 158-159

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 191: Reference Exported NVM Subsystem State</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-191-CLAIM figure-table:NVMCS13-NVM-FIG-191 -->

**SPEC。** Figure 191〈Reference Exported NVM Subsystem State〉：固定 header 為 64 bytes，後接 NVMECSS×4 bytes 的 NVMECS；零長度時欄位不存在。CP=1 只證明整段 Receive 期間 suspended，內層 VER 須為 1h。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

固定 header 為 64 bytes，後接 NVMECSS×4 bytes 的 NVMECS；零長度時欄位不存在。CP=1 只證明整段 Receive 期間 suspended，內層 VER 須為 1h。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CSATTR.CP]
          ↓
[擷取欄位: NVMECSS] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CSATTR.CP` | Controller Suspended；1 表示整段 Migration Receive 處理期間皆 suspended。 |
| `NVMECSS` | NVMe Controller State Size；單位 dwords，0 時可變 state 欄位不存在。 |
| `相關欄位` | Feature values, NVMECS — 固定 header 為 64 bytes，後接 NVMECSS×4 bytes 的 NVMECS；零長度時欄位不存在。CP=1 只證明整段 Receive 期間 suspended，內層 VER 須為 1h。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 固定 header 為 64 bytes，後接 NVMECSS×4 bytes 的 NVMECS；零長度時欄位不存在。CP=1 只證明整段 Receive 期間 suspended，內層 VER 須為 1h。
3. 先讀固定 64-byte header，再檢查可變長度與 suspension 證據。Configuration state 與執行中 state 的用途和設定限制不同，不能共用 payload parser。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 191 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 固定 header 為 64 bytes，後接 NVMECSS×4 bytes 的 NVMECS；零長度時欄位不存在。CP=1 只證明整段 Receive 期間 suspended，內層 VER 須為 1h。 |
| 邊界 | 這是 memory-based controller state 的教學；沒有完整 state 與 suspension 證據時，不從單一 Feature value 推論整個 subsystem 已安全移轉。 |

**說明性範例。** NVMECSS=16 時，NVMECS 有 64 bytes，整個結構有 128 bytes；先檢查乘法、加法與接收 buffer bounds，再解碼內層 VER。

**常見誤解。** 這是 memory-based controller state 的教學；沒有完整 state 與 suspension 證據時，不從單一 Feature value 推論整個 subsystem 已安全移轉。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 這是 memory-based controller state 的教學；沒有完整 state 與 suspension 證據時，不從單一 Feature value 推論整個 subsystem 已安全移轉。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Feature values, CSATTR.CP, NVMECSS, NVMECS

**來源 keyword 索引：** shall, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 191, 文件頁 159-160, PDF 頁 159-160

</details>

<a id="section-5-6"></a>

### §5.6

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 192: LBA Format List Structure</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-192-CLAIM figure-table:NVMCS13-NVM-FIG-192 -->

**SPEC。** Figure 192〈LBA Format List Structure〉：先把 raw NLBAF 加1成共同格式數，再加 NULBAF；unique attributes 區緊接在共同區之後。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

先把 raw NLBAF 加1成共同格式數，再加 NULBAF；unique attributes 區緊接在共同區之後。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NLBAF]
          ↓
[擷取欄位: NULBAF] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NLBAF` | 共同屬性 LBA formats 數的 0-based 欄位。 |
| `NULBAF` | Unique Attribute LBA Formats 的實際數量；可以為0。 |
| `相關欄位` | Format Index — 先把 raw NLBAF 加1成共同格式數，再加 NULBAF；unique attributes 區緊接在共同區之後。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 先把 raw NLBAF 加1成共同格式數，再加 NULBAF；unique attributes 區緊接在共同區之後。
3. 基本 entry 給資料／metadata 大小與相對效能，extended entry 給 PI 格式與 Storage Tag 分配。Unique-attribute entries 要個別查詢，不能沿用共同能力。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 192 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 先把 raw NLBAF 加1成共同格式數，再加 NULBAF；unique attributes 區緊接在共同區之後。 |
| 邊界 | LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。 |

**說明性範例。** raw NLBAF=3、NULBAF=2：有 4 個共同格式及 2 個唯一屬性格式，共 6 個，合法 index 為 0..5。Figure 192 圖示採概念数量，不能直接代入未解碼的 raw NLBAF。

**常見誤解。** LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NLBAF, NULBAF, Format Index

**來源 keyword 索引：** should

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.6, Figure 192, 文件頁 161, PDF 頁 161

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 193: LBA Format List Entries Applicability to Identify Command CNS Value</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-193-CLAIM figure-table:NVMCS13-NVM-FIG-193 -->

**SPEC。** Figure 193〈LBA Format List Entries Applicability to Identify Command CNS Value〉：共同能力查詢與 per-format 查詢覆蓋的格式集合不同；09h／0Ah 可查 NULBAF 定義的 unique-attribute entries。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

共同能力查詢與 per-format 查詢覆蓋的格式集合不同；09h／0Ah 可查 NULBAF 定義的 unique-attribute entries。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | CNS00h, CNS05h, CNS08h, CNS09h, CNS0Ah — 共同能力查詢與 per-format 查詢覆蓋的格式集合不同；09h／0Ah 可查 NULBAF 定義的 unique-attribute entries。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 共同能力查詢與 per-format 查詢覆蓋的格式集合不同；09h／0Ah 可查 NULBAF 定義的 unique-attribute entries。
3. 基本 entry 給資料／metadata 大小與相對效能，extended entry 給 PI 格式與 Storage Tag 分配。Unique-attribute entries 要個別查詢，不能沿用共同能力。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 193 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 共同能力查詢與 per-format 查詢覆蓋的格式集合不同；09h／0Ah 可查 NULBAF 定義的 unique-attribute entries。 |
| 邊界 | LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。 |

**說明性範例。** raw NLBAF=3、NULBAF=2：有 4 個共同格式及 2 個唯一屬性格式，共 6 個，合法 index 為 0..5。Figure 192 圖示採概念数量，不能直接代入未解碼的 raw NLBAF。

**常見誤解。** LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** CNS00h, CNS05h, CNS08h, CNS09h, CNS0Ah

**來源 keyword 索引：** shall, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.6, Figure 193, 文件頁 162, PDF 頁 162

</details>

<a id="section-5-7"></a>

### §5.7

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 194: LBA Migration Queue Entry Type 0</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-194-CLAIM figure-table:NVMCS13-NVM-FIG-194 -->

**SPEC。** Figure 194〈LBA Migration Queue Entry Type 0〉：32-byte entry 最後一 byte 含範圍有效性、deallocation、sequence 與 phase；先看 LBACIR 再用 SLBA／NLB，NLB 是0-based。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

32-byte entry 最後一 byte 含範圍有效性、deallocation、sequence 與 phase；先看 LBACIR 再用 SLBA／NLB，NLB 是0-based。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSID]
          ↓
[擷取欄位: NLB] → [套用編碼: SLBA]
                                      ↓
[驗證證據: LBACIR]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSID` | Namespace 識別碼；SNSID 選 Copy 來源，ENSID 選匯出 namespace，合法值受個別命令約束。 |
| `NLB` | Number of Logical Blocks；本報告命令／status descriptors 的該欄為 0-based。DSM 的 LLB 另為1-based。 |
| `SLBA` | 範圍起始 LBA；SDLBA 選 Copy 目的，DSLBA 是 Get LBA Status descriptor 的起點。 |
| `LBACIR` | LBA Change Indication Range；指定 range、整個 namespace 或無 range 的 entry 解讀。 |
| `DLBA` | Controller Data Queue Phase 與 Deallocated LBA 標記；分別判別新 entry 與 deallocation 提示。 |
| `ESA` | Entry Sequence Attribute；LBA Migration Queue 的 start／stop／suspend／full 標記。 |
| `CDQP` | Controller Data Queue Phase 與 Deallocated LBA 標記；分別判別新 entry 與 deallocation 提示。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 32-byte entry 最後一 byte 含範圍有效性、deallocation、sequence 與 phase；先看 LBACIR 再用 SLBA／NLB，NLB 是0-based。
3. 這個 queue 保存變更範圍與序列標記，不保存完整新資料。Host 讀 entry 後仍需以適當 I/O 取得資料，並處理滿 queue 的停止邊界。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 194 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 32-byte entry 最後一 byte 含範圍有效性、deallocation、sequence 與 phase；先看 LBACIR 再用 SLBA／NLB，NLB 是0-based。 |
| 邊界 | 此處教學為 NVM 的 LBA 變更追蹤；不藉此展開其他傳輸協定或資源匯出格式。重新開始追蹤前要處理 queue 容量與資料一致性。 |

**說明性範例。** 三筆連續 Write 可合併成一個 range entry；所以 queue entry 數不等於寫入命令數。ESA=111b 後，host 不能假設後續每次修改仍持續記錄。

**常見誤解。** 此處教學為 NVM 的 LBA 變更追蹤；不藉此展開其他傳輸協定或資源匯出格式。重新開始追蹤前要處理 queue 容量與資料一致性。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 此處教學為 NVM 的 LBA 變更追蹤；不藉此展開其他傳輸協定或資源匯出格式。重新開始追蹤前要處理 queue 容量與資料一致性。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NSID, NLB, SLBA, LBACIR, DLBA, ESA, CDQP

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.7, Figure 194, 文件頁 163-164, PDF 頁 163-164

</details>

<a id="section-5-10"></a>

### §5.10

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 195: Port Graph Example</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-195-CLAIM figure-table:NVMCS13-NVM-FIG-195 -->

**SPEC。** Figure 195〈Port Graph Example〉：這是共享節點的 graph，不是單一樹；同一 EG 可被兩個 controllers 引用，且不能因此重算共享媒體能力。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

這是共享節點的 graph，不是單一樹；同一 EG 可被兩個 controllers 引用，且不能因此重算共享媒體能力。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Port, Controller0, Controller1, EnduranceGroup1, EnduranceGroup2 — 這是共享節點的 graph，不是單一樹；同一 EG 可被兩個 controllers 引用，且不能因此重算共享媒體能力。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 這是共享節點的 graph，不是單一樹；同一 EG 可被兩個 controllers 引用，且不能因此重算共享媒體能力。
3. 先做結構邊界檢查，再分析 bandwidth bottleneck。Port 的能力與共同 Endurance Group 的能力不同，不能把所有數字直接相加。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 195 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.10.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 這是共享節點的 graph，不是單一樹；同一 EG 可被兩個 controllers 引用，且不能因此重算共享媒體能力。 |
| 邊界 | Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。 |

**說明性範例。** 兩個 PCIe ports 都能使用一個 Endurance Group，若 EG 的 bandwidth 已被 controller 0 用滿，controller 1 不會因多一個 port 就多一份媒體頻寬。相同 EG 能力可由兩個 controller 指向同一 descriptor。

**常見誤解。** Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Port, Controller0, Controller1, EnduranceGroup1, EnduranceGroup2

**來源 keyword 索引：** shall, should

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.10.3, Figure 195, 文件頁 169, PDF 頁 169

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 196: Rate Limiting Log Page Example</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-196-CLAIM figure-table:NVMCS13-NVM-FIG-196 -->

**SPEC。** Figure 196〈Rate Limiting Log Page Example〉：以 Figure195 重畫關係；來源示例把 dword offset299 寫成 byte1916，但299×4=1196，且其他範圍也不一致，必須做 bounds 檢查。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

以 Figure195 重畫關係；來源示例把 dword offset299 寫成 byte1916，但299×4=1196，且其他範圍也不一致，必須做 bounds 檢查。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LPL]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LPL` | Rate Limiting Log Page Length；單位是 dwords，讀取 bytes 前乘 4 並檢查邊界。 |
| `相關欄位` | Dword offsets, Byte ranges, Shared descriptors — 以 Figure195 重畫關係；來源示例把 dword offset299 寫成 byte1916，但299×4=1196，且其他範圍也不一致，必須做 bounds 檢查。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 以 Figure195 重畫關係；來源示例把 dword offset299 寫成 byte1916，但299×4=1196，且其他範圍也不一致，必須做 bounds 檢查。
3. 先做結構邊界檢查，再分析 bandwidth bottleneck。Port 的能力與共同 Endurance Group 的能力不同，不能把所有數字直接相加。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 196 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.10.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 以 Figure195 重畫關係；來源示例把 dword offset299 寫成 byte1916，但299×4=1196，且其他範圍也不一致，必須做 bounds 檢查。 |
| 邊界 | Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。 |

**說明性範例。** 兩個 PCIe ports 都能使用一個 Endurance Group，若 EG 的 bandwidth 已被 controller 0 用滿，controller 1 不會因多一個 port 就多一份媒體頻寬。相同 EG 能力可由兩個 controller 指向同一 descriptor。

**常見誤解。** Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Dword offsets, Byte ranges, LPL, Shared descriptors

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.10.3, Figure 196, 文件頁 169-170, PDF 頁 169-170

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 197: Example Dual Port PCIe NVMe SSD</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-197-CLAIM figure-table:NVMCS13-NVM-FIG-197 -->

**SPEC。** Figure 197〈Example Dual Port PCIe NVMe SSD〉：雙 port 的 transport 能力不會複製 shared EG 的媒體能力；由同一 storage bottleneck 解釋競爭。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

雙 port 的 transport 能力不會複製 shared EG 的媒體能力；由同一 storage bottleneck 解釋競爭。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | PCIe Port0, PCIe Port1, Shared Endurance Group — 雙 port 的 transport 能力不會複製 shared EG 的媒體能力；由同一 storage bottleneck 解釋競爭。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 雙 port 的 transport 能力不會複製 shared EG 的媒體能力；由同一 storage bottleneck 解釋競爭。
3. 先做結構邊界檢查，再分析 bandwidth bottleneck。Port 的能力與共同 Endurance Group 的能力不同，不能把所有數字直接相加。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 197 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.10.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 雙 port 的 transport 能力不會複製 shared EG 的媒體能力；由同一 storage bottleneck 解釋競爭。 |
| 邊界 | Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。 |

**說明性範例。** 兩個 PCIe ports 都能使用一個 Endurance Group，若 EG 的 bandwidth 已被 controller 0 用滿，controller 1 不會因多一個 port 就多一份媒體頻寬。相同 EG 能力可由兩個 controller 指向同一 descriptor。

**常見誤解。** Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** PCIe Port0, PCIe Port1, Shared Endurance Group

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.10.3, Figure 197, 文件頁 171, PDF 頁 171

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 198: Dual Port PCIe NVMe SSD Rate Limiting Log Page Example</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-198-CLAIM figure-table:NVMCS13-NVM-FIG-198 -->

**SPEC。** Figure 198〈Dual Port PCIe NVMe SSD Rate Limiting Log Page Example〉：保留双 port 共用一個 storage node 的關係；原範例 LPL=570 dwords 但列出超出2280 bytes的結構，因此不可當成有效輸入樣本。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

保留双 port 共用一個 storage node 的關係；原範例 LPL=570 dwords 但列出超出2280 bytes的結構，因此不可當成有效輸入樣本。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LPL]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LPL` | Rate Limiting Log Page Length；單位是 dwords，讀取 bytes 前乘 4 並檢查邊界。 |
| `相關欄位` | Port descriptors, Controller descriptors, Shared access — 保留双 port 共用一個 storage node 的關係；原範例 LPL=570 dwords 但列出超出2280 bytes的結構，因此不可當成有效輸入樣本。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 保留双 port 共用一個 storage node 的關係；原範例 LPL=570 dwords 但列出超出2280 bytes的結構，因此不可當成有效輸入樣本。
3. 先做結構邊界檢查，再分析 bandwidth bottleneck。Port 的能力與共同 Endurance Group 的能力不同，不能把所有數字直接相加。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 198 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.10.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 保留双 port 共用一個 storage node 的關係；原範例 LPL=570 dwords 但列出超出2280 bytes的結構，因此不可當成有效輸入樣本。 |
| 邊界 | Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。 |

**說明性範例。** 兩個 PCIe ports 都能使用一個 Endurance Group，若 EG 的 bandwidth 已被 controller 0 用滿，controller 1 不會因多一個 port 就多一份媒體頻寬。相同 EG 能力可由兩個 controller 指向同一 descriptor。

**常見誤解。** Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Port descriptors, Controller descriptors, Shared access, LPL

**來源 keyword 索引：** reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.10.3, Figure 198, 文件頁 171-172, PDF 頁 171-172

</details>

<a id="section-5-11"></a>

### §5.11

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 199: Command Behavior in the Presence of a Reservation</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-199-CLAIM figure-table:NVMCS13-NVM-FIG-199 -->

**SPEC。** Figure 199〈Command Behavior in the Presence of a Reservation〉：逐列區分 read-like／write-like 命令，再按 holder／registration 與 reservation type 判斷；不可把所有非 holder 視為相同。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

逐列區分 read-like／write-like 命令，再按 holder／registration 與 reservation type 判斷；不可把所有非 holder 視為相同。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Reservation type, Holder, Registrant, Command — 逐列區分 read-like／write-like 命令，再按 holder／registration 與 reservation type 判斷；不可把所有非 holder 視為相同。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 逐列區分 read-like／write-like 命令，再按 holder／registration 與 reservation type 判斷；不可把所有非 holder 視為相同。
3. 同一 namespace 的可達性與存取權限要分開檢查；不能將路徑狀態等同 reservation ownership。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 199 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.11 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 逐列區分 read-like／write-like 命令，再按 holder／registration 與 reservation type 判斷；不可把所有非 holder 視為相同。 |
| 邊界 | 不能僅憑存在 Reservation 就一律封鎖所有非 holder 的 I/O；Write Exclusive 與 Exclusive Access 等類型的讀取規則不同。 |

**說明性範例。** 同一 SSD 的兩個 PCIe controllers 可共享 namespace。Controller 1 的路徑可用，仍可能因 reservation 類型與自身 registration 狀態而無法 Write；Read 是否允許需另外查表。

**常見誤解。** 不能僅憑存在 Reservation 就一律封鎖所有非 holder 的 I/O；Write Exclusive 與 Exclusive Access 等類型的讀取規則不同。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 不能僅憑存在 Reservation 就一律封鎖所有非 holder 的 I/O；Write Exclusive 與 Exclusive Access 等類型的讀取規則不同。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Reservation type, Holder, Registrant, Command

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.11, Figure 199, 文件頁 173, PDF 頁 173

</details>

<a id="section-5-12"></a>

### §5.12

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 200: Sanitize Operations – Admin Commands Allowed</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-200-CLAIM figure-table:NVMCS13-NVM-FIG-200 -->

**SPEC。** Figure 200〈Sanitize Operations – Admin Commands Allowed〉：NVM 這張 Figure200 補充 sanitize 期間 Error Information 的 LBA 回0；它不是 Base 同號的 Feature 表，也不能取代 Base 的允許命令清單。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

NVM 這張 Figure200 補充 sanitize 期間 Error Information 的 LBA 回0；它不是 Base 同號的 Feature 表，也不能取代 Base 的允許命令清單。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBA]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBA` | Logical Block Address；以所選格式的 block 為單位。 |
| `相關欄位` | Get Log Page, Error Information — NVM 這張 Figure200 補充 sanitize 期間 Error Information 的 LBA 回0；它不是 Base 同號的 Feature 表，也不能取代 Base 的允許命令清單。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. NVM 這張 Figure200 補充 sanitize 期間 Error Information 的 LBA 回0；它不是 Base 同號的 Feature 表，也不能取代 Base 的允許命令清單。
3. 先辨識 target、operation state 與 allocation，再決定可以驗證什麼。命令 CQE 與 sanitize operation 完成分別由不同證據表示。
4. 套用下方情境，保存原命令、target 與結果。

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
| 判讀 | NVM 這張 Figure200 補充 sanitize 期間 Error Information 的 LBA 回0；它不是 Base 同號的 Feature 表，也不能取代 Base 的允許命令清單。 |
| 邊界 | Sanitize 之後讀零不是充分的成功證據，也不是所有方法都應回零。Namespace sanitize 與 subsystem sanitize 的 scope 不可互換。 |

**說明性範例。** Media Verification state 中，Read 不要求 PI checking 且 allocated media 可讀時，可以忽略讀得出資料的 integrity error 並回特定成功狀態；同一 LBA 連續讀值仍 may 不同。不能用平常 Read 的固定值假設評估它。

**常見誤解。** Sanitize 之後讀零不是充分的成功證據，也不是所有方法都應回零。Namespace sanitize 與 subsystem sanitize 的 scope 不可互換。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Sanitize 之後讀零不是充分的成功證據，也不是所有方法都應回零。Namespace sanitize 與 subsystem sanitize 的 scope 不可互換。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Get Log Page, Error Information, LBA

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12, Figure 200, 文件頁 173, PDF 頁 173

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 201: Sanitize Operation Types – User Data Values</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-201-CLAIM figure-table:NVMCS13-NVM-FIG-201 -->

**SPEC。** Figure 201〈Sanitize Operation Types – User Data Values〉：保留已配置 media 的成功 sanitize 回值依方法不同；若已 deallocate，改採 deallocated-read 規則，不將任何方法一概寫成全零。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

保留已配置 media 的成功 sanitize 回值依方法不同；若已 deallocate，改採 deallocated-read 規則，不將任何方法一概寫成全零。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Block Erase, Crypto Erase, Overwrite — 保留已配置 media 的成功 sanitize 回值依方法不同；若已 deallocate，改採 deallocated-read 規則，不將任何方法一概寫成全零。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 保留已配置 media 的成功 sanitize 回值依方法不同；若已 deallocate，改採 deallocated-read 規則，不將任何方法一概寫成全零。
3. 先辨識 target、operation state 與 allocation，再決定可以驗證什麼。命令 CQE 與 sanitize operation 完成分別由不同證據表示。
4. 套用下方情境，保存原命令、target 與結果。

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
| 判讀 | 保留已配置 media 的成功 sanitize 回值依方法不同；若已 deallocate，改採 deallocated-read 規則，不將任何方法一概寫成全零。 |
| 邊界 | Sanitize 之後讀零不是充分的成功證據，也不是所有方法都應回零。Namespace sanitize 與 subsystem sanitize 的 scope 不可互換。 |

**說明性範例。** Media Verification state 中，Read 不要求 PI checking 且 allocated media 可讀時，可以忽略讀得出資料的 integrity error 並回特定成功狀態；同一 LBA 連續讀值仍 may 不同。不能用平常 Read 的固定值假設評估它。

**常見誤解。** Sanitize 之後讀零不是充分的成功證據，也不是所有方法都應回零。Namespace sanitize 與 subsystem sanitize 的 scope 不可互換。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Sanitize 之後讀零不是充分的成功證據，也不是所有方法都應回零。Namespace sanitize 與 subsystem sanitize 的 scope 不可互換。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Block Erase, Crypto Erase, Overwrite

**來源 keyword 索引：** shall not, shall, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12, Figure 201, 文件頁 174, PDF 頁 174

</details>

<a id="section-appendix-a"></a>

### §Appendix A

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 202: Example Token Bucket</strong></summary>

<!-- claim:NVMCS13-NVM-FIG-202-CLAIM figure-table:NVMCS13-NVM-FIG-202 -->

**SPEC。** Figure 202〈Example Token Bucket〉：Token 不足讓命令等候；可處理部分但整筆完成才發布 CQE。此圖為 informative implementation example，不是唯一排程演算法。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Token 不足讓命令等候；可處理部分但整筆完成才發布 CQE。此圖為 informative implementation example，不是唯一排程演算法。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Token supply, Queued commands, Admission, Internal resource — Token 不足讓命令等候；可處理部分但整筆完成才發布 CQE。此圖為 informative implementation example，不是唯一排程演算法。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Token 不足讓命令等候；可處理部分但整筆完成才發布 CQE。此圖為 informative implementation example，不是唯一排程演算法。
3. 用能力、limits、實際 demand 三個值判讀結果。設定比例不等於任何時刻都固定吞吐；內部資源與工作負載仍會改變觀測值。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 202 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §Appendix A 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Token 不足讓命令等候；可處理部分但整筆完成才發布 CQE。此圖為 informative implementation example，不是唯一排程演算法。 |
| 邊界 | Token 不足時延後處理而非丟棄命令；可以處理部分，但不得在整筆處理完前先送 completion。 |

**說明性範例。** 教學設定：4 KiB Write，WRBWR=2、WRIOPSR=3，分別消耗 total-bandwidth 8 KiB、write-bandwidth 4 KiB、total-IOPS 3、write-IOPS 1。4 KiB Read 只消耗 total-bandwidth 4 KiB 與 total-IOPS 1。

**常見誤解。** Token 不足時延後處理而非丟棄命令；可以處理部分，但不得在整筆處理完前先送 completion。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Token 不足時延後處理而非丟棄命令；可以處理部分，但不得在整筆處理完前先送 completion。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Token supply, Queued commands, Admission, Internal resource

**來源 keyword 索引：** should, may

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §Appendix A, Figure 202, 文件頁 176, PDF 頁 176

</details>

<a id="section-dependency"></a>

### 引用相依 Figure（位於主章節範圍外）

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 93: Common Command Format</strong></summary>

<!-- claim:NVMCS13-BASE-FIG-093-CLAIM figure-table:NVMCS13-BASE-FIG-093 -->

**SPEC。** Figure 93〈Common Command Format〉：Common SQE 將 namespace、data pointers 與 command-specific Dwords 分開；NVM 章節只補充相應 command fields。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Common SQE 將 namespace、data pointers 與 command-specific Dwords 分開；NVM 章節只補充相應 command fields。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSID]
          ↓
[擷取欄位: MPTR] → [套用編碼: DPTR]
                                      ↓
[驗證證據: 相關欄位]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSID` | Namespace 識別碼；SNSID 選 Copy 來源，ENSID 選匯出 namespace，合法值受個別命令約束。 |
| `MPTR` | Separate metadata 的指標；metadata placement 由 namespace format 與命令欄位決定。 |
| `DPTR` | 命令 data pointer；Read 是目的、Write 是來源、Copy／DSM 指向 descriptors。 |
| `相關欄位` | OPC, CDW10-15 — Common SQE 將 namespace、data pointers 與 command-specific Dwords 分開；NVM 章節只補充相應 command fields。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Common SQE 將 namespace、data pointers 與 command-specific Dwords 分開；NVM 章節只補充相應 command fields。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

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
| 判讀 | Common SQE 將 namespace、data pointers 與 command-specific Dwords 分開；NVM 章節只補充相應 command fields。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** OPC, NSID, MPTR, DPTR, CDW10-15

**來源 keyword 索引：** shall not, shall, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, 文件頁 140-142, PDF 頁 166-168

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 97: Common Completion Queue Entry Layout – Admin and All I/O Command Sets</strong></summary>

<!-- claim:NVMCS13-BASE-FIG-097-CLAIM figure-table:NVMCS13-BASE-FIG-097 -->

**SPEC。** Figure 97〈Common Completion Queue Entry Layout – Admin and All I/O Command Sets〉：CQE 的 command-specific result 與共同 queue／status 資訊各有位置；Copy DW0 與 Write Zeroes DW0 使用不同意義。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CQE 的 command-specific result 與共同 queue／status 資訊各有位置；Copy DW0 與 Write Zeroes DW0 使用不同意義。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | DW0, DW1, SQHD, SQID, CID, Status — CQE 的 command-specific result 與共同 queue／status 資訊各有位置；Copy DW0 與 Write Zeroes DW0 使用不同意義。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CQE 的 command-specific result 與共同 queue／status 資訊各有位置；Copy DW0 與 Write Zeroes DW0 使用不同意義。
3. 從 controller 類型開始建立命令、Feature、log 的能力矩陣。資料指標指向的可能是使用者資料，也可能只是控制 descriptor。
4. 套用下方情境，保存原命令、target 與結果。

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
| 判讀 | CQE 的 command-specific result 與共同 queue／status 資訊各有位置；Copy DW0 與 Write Zeroes DW0 使用不同意義。 |
| 邊界 | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

**說明性範例。** Copy opcode=19h 的低 bits 是 01b，因 host 傳入 source descriptors；並不表示需要把整份待複製資料從 host 再傳一次。

**常見誤解。** FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** DW0, DW1, SQHD, SQID, CID, Status

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 97, 文件頁 144, PDF 頁 170

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 98: Completion Queue Entry: DW 2</strong></summary>

<!-- claim:NVMCS13-BASE-FIG-098-CLAIM figure-table:NVMCS13-BASE-FIG-098 -->

**SPEC。** Figure 98〈Completion Queue Entry: DW 2〉：DW2 的 SQHD／SQID 回報對應 submission queue 資訊，不能當作此次命令已傳輸的 byte count。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

DW2 的 SQHD／SQID 回報對應 submission queue 資訊，不能當作此次命令已傳輸的 byte count。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | SQHD, SQID — DW2 的 SQHD／SQID 回報對應 submission queue 資訊，不能當作此次命令已傳輸的 byte count。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. DW2 的 SQHD／SQID 回報對應 submission queue 資訊，不能當作此次命令已傳輸的 byte count。
3. 從 controller 類型開始建立命令、Feature、log 的能力矩陣。資料指標指向的可能是使用者資料，也可能只是控制 descriptor。
4. 套用下方情境，保存原命令、target 與結果。

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
| 判讀 | DW2 的 SQHD／SQID 回報對應 submission queue 資訊，不能當作此次命令已傳輸的 byte count。 |
| 邊界 | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

**說明性範例。** Copy opcode=19h 的低 bits 是 01b，因 host 傳入 source descriptors；並不表示需要把整份待複製資料從 host 再傳一次。

**常見誤解。** FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SQHD, SQID

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 98, 文件頁 144, PDF 頁 170

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 99: Completion Queue Entry: DW 3</strong></summary>

<!-- claim:NVMCS13-BASE-FIG-099-CLAIM figure-table:NVMCS13-BASE-FIG-099 -->

**SPEC。** Figure 99〈Completion Queue Entry: DW 3〉：DW3 以 CID 配回命令、Status 判定結果；command-specific DW0 不取代 status。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

DW3 以 CID 配回命令、Status 判定結果；command-specific DW0 不取代 status。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | CID, Status — DW3 以 CID 配回命令、Status 判定結果；command-specific DW0 不取代 status。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. DW3 以 CID 配回命令、Status 判定結果；command-specific DW0 不取代 status。
3. 從 controller 類型開始建立命令、Feature、log 的能力矩陣。資料指標指向的可能是使用者資料，也可能只是控制 descriptor。
4. 套用下方情境，保存原命令、target 與結果。

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
| 判讀 | DW3 以 CID 配回命令、Status 判定結果；command-specific DW0 不取代 status。 |
| 邊界 | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

**說明性範例。** Copy opcode=19h 的低 bits 是 01b，因 host 傳入 source descriptors；並不表示需要把整份待複製資料從 host 再傳一次。

**常見誤解。** FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** CID, Status

**來源 keyword 索引：** should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 99, 文件頁 145, PDF 頁 171

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 101: Completion Queue Entry: Status Field</strong></summary>

<!-- claim:NVMCS13-BASE-FIG-101-CLAIM figure-table:NVMCS13-BASE-FIG-101 -->

**SPEC。** Figure 101〈Completion Queue Entry: Status Field〉：Status 要一併解讀 SCT／SC，DNR 用於重試判斷，phase 用於辨識新 completion；它們回答不同問題。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Status 要一併解讀 SCT／SC，DNR 用於重試判斷，phase 用於辨識新 completion；它們回答不同問題。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SCT]
          ↓
[擷取欄位: SC] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SCT` | Status Code Type 與 Status Code；兩欄共同識別錯誤，單看 SC 可能誤判。 |
| `SC` | Status Code Type 與 Status Code；兩欄共同識別錯誤，單看 SC 可能誤判。 |
| `相關欄位` | DNR, P — Status 要一併解讀 SCT／SC，DNR 用於重試判斷，phase 用於辨識新 completion；它們回答不同問題。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Status 要一併解讀 SCT／SC，DNR 用於重試判斷，phase 用於辨識新 completion；它們回答不同問題。
3. 從 controller 類型開始建立命令、Feature、log 的能力矩陣。資料指標指向的可能是使用者資料，也可能只是控制 descriptor。
4. 套用下方情境，保存原命令、target 與結果。

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
| 判讀 | Status 要一併解讀 SCT／SC，DNR 用於重試判斷，phase 用於辨識新 completion；它們回答不同問題。 |
| 邊界 | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

**說明性範例。** Copy opcode=19h 的低 bits 是 01b，因 host 傳入 source descriptors；並不表示需要把整份待複製資料從 host 再傳一次。

**常見誤解。** FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SCT, SC, DNR, P

**來源 keyword 索引：** shall, should not, should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 101, 文件頁 145-146, PDF 頁 171-172

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 110: PRP Entry Layout</strong></summary>

<!-- claim:NVMCS13-BASE-FIG-110-CLAIM figure-table:NVMCS13-BASE-FIG-110 -->

**SPEC。** Figure 110〈PRP Entry Layout〉：PRP layout 包含頁基址與首筆 offset；NVM payload 可能是 data 或 descriptor list，不能由 pointer 類型推定內容。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

PRP layout 包含頁基址與首筆 offset；NVM payload 可能是 data 或 descriptor list，不能由 pointer 類型推定內容。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | PRP, Page base, Offset — PRP layout 包含頁基址與首筆 offset；NVM payload 可能是 data 或 descriptor list，不能由 pointer 類型推定內容。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. PRP layout 包含頁基址與首筆 offset；NVM payload 可能是 data 或 descriptor list，不能由 pointer 類型推定內容。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

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
| 判讀 | PRP layout 包含頁基址與首筆 offset；NVM payload 可能是 data 或 descriptor list，不能由 pointer 類型推定內容。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** PRP, Page base, Offset

**來源 keyword 索引：** shall, may

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 110, 文件頁 158, PDF 頁 184

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 111: PRP Entry – Page Base Address and Offset</strong></summary>

<!-- claim:NVMCS13-BASE-FIG-111-CLAIM figure-table:NVMCS13-BASE-FIG-111 -->

**SPEC。** Figure 111〈PRP Entry – Page Base Address and Offset〉：頁大小決定 base／offset 切分。計算第一頁剩餘空間後才決定後續 PRP pages。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

頁大小決定 base／offset 切分。計算第一頁剩餘空間後才決定後續 PRP pages。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | Page size, PRP offset — 頁大小決定 base／offset 切分。計算第一頁剩餘空間後才決定後續 PRP pages。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 頁大小決定 base／offset 切分。計算第一頁剩餘空間後才決定後續 PRP pages。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

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
| 判讀 | 頁大小決定 base／offset 切分。計算第一頁剩餘空間後才決定後續 PRP pages。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** Page size, PRP offset

**來源 keyword 索引：** shall, may

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 111, 文件頁 158, PDF 頁 184

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 116: Generic SGL Descriptor Format</strong></summary>

<!-- claim:NVMCS13-BASE-FIG-116-CLAIM figure-table:NVMCS13-BASE-FIG-116 -->

**SPEC。** Figure 116〈Generic SGL Descriptor Format〉：本機 SGL descriptor 用 address、length 與 type 描述 buffer；保留 generic layout，不展開其他 transport 的 descriptor types。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

本機 SGL descriptor 用 address、length 與 type 描述 buffer；保留 generic layout，不展開其他 transport 的 descriptor types。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | SGL descriptor, Address, Length, Type — 本機 SGL descriptor 用 address、length 與 type 描述 buffer；保留 generic layout，不展開其他 transport 的 descriptor types。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 本機 SGL descriptor 用 address、length 與 type 描述 buffer；保留 generic layout，不展開其他 transport 的 descriptor types。
3. 把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。
4. 套用下方情境，保存原命令、target 與結果。

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
| 判讀 | 本機 SGL descriptor 用 address、length 與 type 描述 buffer；保留 generic layout，不展開其他 transport 的 descriptor types。 |
| 邊界 | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

**說明性範例。** SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

**常見誤解。** CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SGL descriptor, Address, Length, Type

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 116, 文件頁 161, PDF 頁 187

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 312: Sanitize Status Log Page</strong></summary>

<!-- claim:NVMCS13-BASE-FIG-312-CLAIM figure-table:NVMCS13-BASE-FIG-312 -->

**SPEC。** Figure 312〈Sanitize Status Log Page〉：Sanitize Status 提供 operation 的進度、結果、起始命令及 state；成功的啟動 CQE 無法取代這份 log。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Sanitize Status 提供 operation 的進度、結果、起始命令及 state；成功的啟動 CQE 無法取代這份 log。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | SPROG, SSTAT, SCDW10, SANS — Sanitize Status 提供 operation 的進度、結果、起始命令及 state；成功的啟動 CQE 無法取代這份 log。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Sanitize Status 提供 operation 的進度、結果、起始命令及 state；成功的啟動 CQE 無法取代這份 log。
3. 先辨識 target、operation state 與 allocation，再決定可以驗證什麼。命令 CQE 與 sanitize operation 完成分別由不同證據表示。
4. 套用下方情境，保存原命令、target 與結果。

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
| 判讀 | Sanitize Status 提供 operation 的進度、結果、起始命令及 state；成功的啟動 CQE 無法取代這份 log。 |
| 邊界 | Sanitize 之後讀零不是充分的成功證據，也不是所有方法都應回零。Namespace sanitize 與 subsystem sanitize 的 scope 不可互換。 |

**說明性範例。** Media Verification state 中，Read 不要求 PI checking 且 allocated media 可讀時，可以忽略讀得出資料的 integrity error 並回特定成功狀態；同一 LBA 連續讀值仍 may 不同。不能用平常 Read 的固定值假設評估它。

**常見誤解。** Sanitize 之後讀零不是充分的成功證據，也不是所有方法都應回零。Namespace sanitize 與 subsystem sanitize 的 scope 不可互換。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Sanitize 之後讀零不是充分的成功證據，也不是所有方法都應回零。Namespace sanitize 與 subsystem sanitize 的 scope 不可互換。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SPROG, SSTAT, SCDW10, SANS

**來源 keyword 索引：** shall, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, Figure 312, 文件頁 314-319, PDF 頁 340-345

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 338: Identify – Identify Controller Data Structure, I/O Command Set Independent</strong></summary>

<!-- claim:NVMCS13-BASE-FIG-338-CLAIM figure-table:NVMCS13-BASE-FIG-338 -->

**SPEC。** Figure 338〈Identify – Identify Controller Data Structure, I/O Command Set Independent〉：NVM 需要 Base Identify 的 ONCS variants、CTRATT.ELBAS／MEM、MDTS 與 SANICAP 等能力；本 slice 不展開其餘跨頁欄位。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

NVM 需要 Base Identify 的 ONCS variants、CTRATT.ELBAS／MEM、MDTS 與 SANICAP 等能力；本 slice 不展開其餘跨頁欄位。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ONCS]
          ↓
[擷取欄位: MDTS] → [套用編碼: 相關欄位]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ONCS` | Optional NVM Commands Supported；包含能力及 variant，需結合 NVM Identify 的 limits。 |
| `MDTS` | Maximum Data Transfer Size；以 minimum page size 為基準的 exponent；零有特定無限制語意。 |
| `相關欄位` | CTRATT, SANICAP — NVM 需要 Base Identify 的 ONCS variants、CTRATT.ELBAS／MEM、MDTS 與 SANICAP 等能力；本 slice 不展開其餘跨頁欄位。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. NVM 需要 Base Identify 的 ONCS variants、CTRATT.ELBAS／MEM、MDTS 與 SANICAP 等能力；本 slice 不展開其餘跨頁欄位。
3. 每次查詢都寫出 CNS、CSI、NSID、Format Index 的角色。不同查詢回零有不同含義，不能一律解讀為不存在或不支援。
4. 套用下方情境，保存原命令、target 與結果。

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
| 判讀 | NVM 需要 Base Identify 的 ONCS variants、CTRATT.ELBAS／MEM、MDTS 與 SANICAP 等能力；本 slice 不展開其餘跨頁欄位。 |
| 邊界 | §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。 |

**說明性範例。** NSID=7 的目前格式需讀 FLBAS 再取同 index 的 LBAF 與 ELBAF。查尚未建立的 FIDX=3 能力，使用 09h／0Ah、CSI=0、NSID=0、FIDX=3，另結合 CNS08h 的共同能力。

**常見誤解。** §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** ONCS, CTRATT, MDTS, SANICAP

**來源 keyword 索引：** shall not, shall, should not, should, may, optional, mandatory, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, 文件頁 340-382, PDF 頁 366-408

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 346: Identify – I/O Command Set Independent Identify Namespace Data Structure</strong></summary>

<!-- claim:NVMCS13-BASE-FIG-346-CLAIM figure-table:NVMCS13-BASE-FIG-346 -->

**SPEC。** Figure 346〈Identify – I/O Command Set Independent Identify Namespace Data Structure〉：CNS08h 提供 command-set-independent namespace 屬性，與 NVM CNS00h／05h 組合；不應只依其中一份結構推論全部能力。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CNS08h 提供 command-set-independent namespace 屬性，與 NVM CNS00h／05h 組合；不應只依其中一份結構推論全部能力。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSID]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSID` | Namespace 識別碼；SNSID 選 Copy 來源，ENSID 選匯出 namespace，合法值受個別命令約束。 |
| `相關欄位` | NSATTR, NMIC, RESCAP, ANAGRPID — CNS08h 提供 command-set-independent namespace 屬性，與 NVM CNS00h／05h 組合；不應只依其中一份結構推論全部能力。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CNS08h 提供 command-set-independent namespace 屬性，與 NVM CNS00h／05h 組合；不應只依其中一份結構推論全部能力。
3. 每次查詢都寫出 CNS、CSI、NSID、Format Index 的角色。不同查詢回零有不同含義，不能一律解讀為不存在或不支援。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 346 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.14.2.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CNS08h 提供 command-set-independent namespace 屬性，與 NVM CNS00h／05h 組合；不應只依其中一份結構推論全部能力。 |
| 邊界 | §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。 |

**說明性範例。** NSID=7 的目前格式需讀 FLBAS 再取同 index 的 LBAF 與 ELBAF。查尚未建立的 FIDX=3 能力，使用 09h／0Ah、CSI=0、NSID=0、FIDX=3，另結合 CNS08h 的共同能力。

**常見誤解。** §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | §4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** NSID, NSATTR, NMIC, RESCAP, ANAGRPID

**來源 keyword 索引：** shall, should, may, optional, mandatory, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.8, Figure 346, 文件頁 391-394, PDF 頁 417-420

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 451: Sanitize – Command Dword 10</strong></summary>

<!-- claim:NVMCS13-BASE-FIG-451-CLAIM figure-table:NVMCS13-BASE-FIG-451 -->

**SPEC。** Figure 451〈Sanitize – Command Dword 10〉：Subsystem Sanitize 的 CDW10 分開方法及修飾 bits；本教學只把 NVM §4.1.7 的 Base 命令相依補齊。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Subsystem Sanitize 的 CDW10 分開方法及修飾 bits；本教學只把 NVM §4.1.7 的 Base 命令相依補齊。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | SANACT, AUSE, NDAS, EMVS, PREQ — Subsystem Sanitize 的 CDW10 分開方法及修飾 bits；本教學只把 NVM §4.1.7 的 Base 命令相依補齊。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Subsystem Sanitize 的 CDW10 分開方法及修飾 bits；本教學只把 NVM §4.1.7 的 Base 命令相依補齊。
3. 先辨識 target、operation state 與 allocation，再決定可以驗證什麼。命令 CQE 與 sanitize operation 完成分別由不同證據表示。
4. 套用下方情境，保存原命令、target 與結果。

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
| 判讀 | Subsystem Sanitize 的 CDW10 分開方法及修飾 bits；本教學只把 NVM §4.1.7 的 Base 命令相依補齊。 |
| 邊界 | Sanitize 之後讀零不是充分的成功證據，也不是所有方法都應回零。Namespace sanitize 與 subsystem sanitize 的 scope 不可互換。 |

**說明性範例。** Media Verification state 中，Read 不要求 PI checking 且 allocated media 可讀時，可以忽略讀得出資料的 integrity error 並回特定成功狀態；同一 LBA 連續讀值仍 may 不同。不能用平常 Read 的固定值假設評估它。

**常見誤解。** Sanitize 之後讀零不是充分的成功證據，也不是所有方法都應回零。Namespace sanitize 與 subsystem sanitize 的 scope 不可互換。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Sanitize 之後讀零不是充分的成功證據，也不是所有方法都應回零。Namespace sanitize 與 subsystem sanitize 的 scope 不可互換。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SANACT, AUSE, NDAS, EMVS, PREQ

**來源 keyword 索引：** shall not, shall, should not, should, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 451, 文件頁 450-451, PDF 頁 476-477

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 452: Sanitize – Command Dword 11</strong></summary>

<!-- claim:NVMCS13-BASE-FIG-452-CLAIM figure-table:NVMCS13-BASE-FIG-452 -->

**SPEC。** Figure 452〈Sanitize – Command Dword 11〉：CDW11 的 OVRPAT 是 Overwrite pattern；不是所有 SANACT 都使用此值，也不能套用於 Crypto Erase 的讀值預期。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDW11 的 OVRPAT 是 Overwrite pattern；不是所有 SANACT 都使用此值，也不能套用於 Crypto Erase 的讀值預期。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | OVRPAT — CDW11 的 OVRPAT 是 Overwrite pattern；不是所有 SANACT 都使用此值，也不能套用於 Crypto Erase 的讀值預期。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDW11 的 OVRPAT 是 Overwrite pattern；不是所有 SANACT 都使用此值，也不能套用於 Crypto Erase 的讀值預期。
3. 先辨識 target、operation state 與 allocation，再決定可以驗證什麼。命令 CQE 與 sanitize operation 完成分別由不同證據表示。
4. 套用下方情境，保存原命令、target 與結果。

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
| 判讀 | CDW11 的 OVRPAT 是 Overwrite pattern；不是所有 SANACT 都使用此值，也不能套用於 Crypto Erase 的讀值預期。 |
| 邊界 | Sanitize 之後讀零不是充分的成功證據，也不是所有方法都應回零。Namespace sanitize 與 subsystem sanitize 的 scope 不可互換。 |

**說明性範例。** Media Verification state 中，Read 不要求 PI checking 且 allocated media 可讀時，可以忽略讀得出資料的 integrity error 並回特定成功狀態；同一 LBA 連續讀值仍 may 不同。不能用平常 Read 的固定值假設評估它。

**常見誤解。** Sanitize 之後讀零不是充分的成功證據，也不是所有方法都應回零。Namespace sanitize 與 subsystem sanitize 的 scope 不可互換。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Sanitize 之後讀零不是充分的成功證據，也不是所有方法都應回零。Namespace sanitize 與 subsystem sanitize 的 scope 不可互換。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** OVRPAT

**來源 keyword 索引：** shall, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 452, 文件頁 451, PDF 頁 477

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 491: Host Behavior Support – Data Structure</strong></summary>

<!-- claim:NVMCS13-BASE-FIG-491-CLAIM figure-table:NVMCS13-BASE-FIG-491 -->

**SPEC。** Figure 491〈Host Behavior Support – Data Structure〉：Host Behavior Support 的 CFD2E／CFD3E 宣告 host 接受 Copy formats2h／3h；controller CDF support 與 host enablement 是兩項門檻。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Host Behavior Support 的 CFD2E／CFD3E 宣告 host 接受 Copy formats2h／3h；controller CDF support 與 host enablement 是兩項門檻。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | CFD2E, CFD3E — Host Behavior Support 的 CFD2E／CFD3E 宣告 host 接受 Copy formats2h／3h；controller CDF support 與 host enablement 是兩項門檻。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Host Behavior Support 的 CFD2E／CFD3E 宣告 host 接受 Copy formats2h／3h；controller CDF support 與 host enablement 是兩項門檻。
3. 先計算展開後的目的區間，再檢查格式、長度限制、重疊與 atomicity。Copy 可少用 host 資料傳輸，但不是無條件的 transaction。
4. 套用下方情境，保存原命令、target 與結果。

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
| 判讀 | Host Behavior Support 的 CFD2E／CFD3E 宣告 host 接受 Copy formats2h／3h；controller CDF support 與 host enablement 是兩項門檻。 |
| 邊界 | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

**說明性範例。** 兩個 source descriptors 的 NLB 都是 3，SDLBA=100：第一段寫 100..103、第二段寫 104..107，共 8 blocks。若 DW0=1，不能據此保證第二段或更後面完全未修改。

**常見誤解。** FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** CFD2E, CFD3E

**來源 keyword 索引：** shall not, shall, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.15, Figure 491, 文件頁 476-477, PDF 頁 502-503

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 561: Track Send – Command Dword 10</strong></summary>

<!-- claim:NVMCS13-BASE-FIG-561-CLAIM figure-table:NVMCS13-BASE-FIG-561 -->

**SPEC。** Figure 561〈Track Send – Command Dword 10〉：Track Send CDW10 先選 management operation，MOS 再依 operation 解讀；NVM 的本範圍使用 Log User Data Changes。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

Track Send CDW10 先選 management operation，MOS 再依 operation 解讀；NVM 的本範圍使用 Log User Data Changes。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | MOS, MO — Track Send CDW10 先選 management operation，MOS 再依 operation 解讀；NVM 的本範圍使用 Log User Data Changes。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. Track Send CDW10 先選 management operation，MOS 再依 operation 解讀；NVM 的本範圍使用 Log User Data Changes。
3. 這個 queue 保存變更範圍與序列標記，不保存完整新資料。Host 讀 entry 後仍需以適當 I/O 取得資料，並處理滿 queue 的停止邊界。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 561 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.32 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | Track Send CDW10 先選 management operation，MOS 再依 operation 解讀；NVM 的本範圍使用 Log User Data Changes。 |
| 邊界 | 此處教學為 NVM 的 LBA 變更追蹤；不藉此展開其他傳輸協定或資源匯出格式。重新開始追蹤前要處理 queue 容量與資料一致性。 |

**說明性範例。** 三筆連續 Write 可合併成一個 range entry；所以 queue entry 數不等於寫入命令數。ESA=111b 後，host 不能假設後續每次修改仍持續記錄。

**常見誤解。** 此處教學為 NVM 的 LBA 變更追蹤；不藉此展開其他傳輸協定或資源匯出格式。重新開始追蹤前要處理 queue 容量與資料一致性。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 此處教學為 NVM 的 LBA 變更追蹤；不藉此展開其他傳輸協定或資源匯出格式。重新開始追蹤前要處理 queue 容量與資料一致性。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** MOS, MO

**來源 keyword 索引：** shall, optional, mandatory, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.32, Figure 561, 文件頁 523, PDF 頁 549

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 562: Log User Data Changes – Management Operation Specific Field</strong></summary>

<!-- claim:NVMCS13-BASE-FIG-562-CLAIM figure-table:NVMCS13-BASE-FIG-562 -->

**SPEC。** Figure 562〈Log User Data Changes – Management Operation Specific Field〉：LACT 控制開始／停止 user-data changes logging；必須配合 CDQID 指定已建立的 LBA Migration Queue。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

LACT 控制開始／停止 user-data changes logging；必須配合 CDQID 指定已建立的 LBA Migration Queue。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | LACT — LACT 控制開始／停止 user-data changes logging；必須配合 CDQID 指定已建立的 LBA Migration Queue。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. LACT 控制開始／停止 user-data changes logging；必須配合 CDQID 指定已建立的 LBA Migration Queue。
3. 這個 queue 保存變更範圍與序列標記，不保存完整新資料。Host 讀 entry 後仍需以適當 I/O 取得資料，並處理滿 queue 的停止邊界。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 562 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.32.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | LACT 控制開始／停止 user-data changes logging；必須配合 CDQID 指定已建立的 LBA Migration Queue。 |
| 邊界 | 此處教學為 NVM 的 LBA 變更追蹤；不藉此展開其他傳輸協定或資源匯出格式。重新開始追蹤前要處理 queue 容量與資料一致性。 |

**說明性範例。** 三筆連續 Write 可合併成一個 range entry；所以 queue entry 數不等於寫入命令數。ESA=111b 後，host 不能假設後續每次修改仍持續記錄。

**常見誤解。** 此處教學為 NVM 的 LBA 變更追蹤；不藉此展開其他傳輸協定或資源匯出格式。重新開始追蹤前要處理 queue 容量與資料一致性。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 此處教學為 NVM 的 LBA 變更追蹤；不藉此展開其他傳輸協定或資源匯出格式。重新開始追蹤前要處理 queue 容量與資料一致性。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** LACT

**來源 keyword 索引：** shall, optional, mandatory, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.32.1.1, Figure 562, 文件頁 523, PDF 頁 549

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 563: Log User Data Changes – Command Dword 11</strong></summary>

<!-- claim:NVMCS13-BASE-FIG-563-CLAIM figure-table:NVMCS13-BASE-FIG-563 -->

**SPEC。** Figure 563〈Log User Data Changes – Command Dword 11〉：CDQID 是 controller data queue identifier；不是 NSID 或 SQID，識別此次變更記錄送往哪個 queue。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

CDQID 是 controller data queue identifier；不是 NSID 或 SQID，識別此次變更記錄送往哪個 queue。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 相關欄位]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `相關欄位` | CDQID — CDQID 是 controller data queue identifier；不是 NSID 或 SQID，識別此次變更記錄送往哪個 queue。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. CDQID 是 controller data queue identifier；不是 NSID 或 SQID，識別此次變更記錄送往哪個 queue。
3. 這個 queue 保存變更範圍與序列標記，不保存完整新資料。Host 讀 entry 後仍需以適當 I/O 取得資料，並處理滿 queue 的停止邊界。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 563 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.32.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | CDQID 是 controller data queue identifier；不是 NSID 或 SQID，識別此次變更記錄送往哪個 queue。 |
| 邊界 | 此處教學為 NVM 的 LBA 變更追蹤；不藉此展開其他傳輸協定或資源匯出格式。重新開始追蹤前要處理 queue 容量與資料一致性。 |

**說明性範例。** 三筆連續 Write 可合併成一個 range entry；所以 queue entry 數不等於寫入命令數。ESA=111b 後，host 不能假設後續每次修改仍持續記錄。

**常見誤解。** 此處教學為 NVM 的 LBA 變更追蹤；不藉此展開其他傳輸協定或資源匯出格式。重新開始追蹤前要處理 queue 容量與資料一致性。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | 此處教學為 NVM 的 LBA 變更追蹤；不藉此展開其他傳輸協定或資源匯出格式。重新開始追蹤前要處理 queue 容量與資料一致性。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** CDQID

**來源 keyword 索引：** shall, optional, mandatory, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.32.1.1, Figure 563, 文件頁 523, PDF 頁 549

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 712: Streams Directive – Return Parameters Data Structure</strong></summary>

<!-- claim:NVMCS13-BASE-FIG-712-CLAIM figure-table:NVMCS13-BASE-FIG-712 -->

**SPEC。** Figure 712〈Streams Directive – Return Parameters Data Structure〉：只讀 Streams Return Parameters 的 SWS／SGS 相依 slice；NVM §5.13 將 SWS 的 command-set 單位定義為 logical blocks。 依下列來源欄位逐項解碼。

#### 這張 Figure 在完整流程中的位置

只讀 Streams Return Parameters 的 SWS／SGS 相依 slice；NVM §5.13 將 SWS 的 command-set 單位定義為 logical blocks。

依本來源與版本重整欄位關係，配合解碼案例閱讀。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SWS]
          ↓
[擷取欄位: 相關欄位] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SWS` | Stream Write Size；NVM command-set 單位為 logical blocks。 |
| `相關欄位` | SGS — 只讀 Streams Return Parameters 的 SWS／SGS 相依 slice；NVM §5.13 將 SWS 的 command-set 單位定義為 logical blocks。 |

#### 照這個順序讀，不要直接跳到數值

1. 定位引用的完整跨頁範圍，區分 raw 值與解碼後單位。
2. 只讀 Streams Return Parameters 的 SWS／SGS 相依 slice；NVM §5.13 將 SWS 的 command-set 單位定義為 logical blocks。
3. 用兩層大小模型解釋 Stream Write Size 與較大的 stream granularity。它們可能和 namespace hints 成整數倍，但規格不保證每個 namespace 都如此。
4. 套用下方情境，保存原命令、target 與結果。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 712 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.9.3.1.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 判讀 | 只讀 Streams Return Parameters 的 SWS／SGS 相依 slice；NVM §5.13 將 SWS 的 command-set 單位定義為 logical blocks。 |
| 邊界 | Streams hints、FDP placement 與 namespace atomicity 是不同概念；不能只因尺寸相等就推論是同一個內部媒體單位。 |

**說明性範例。** 解碼後 SWS=8 blocks、SGS=4，stream granularity 是 32 blocks。8-block Write 可符合 SWS，但一個完整 granularity-unit 的 deallocate 長度是 32 blocks。

**常見誤解。** Streams hints、FDP placement 與 namespace atomicity 是不同概念；不能只因尺寸相等就推論是同一個內部媒體單位。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| Debug | Streams hints、FDP placement 與 namespace atomicity 是不同概念；不能只因尺寸相等就推論是同一個內部媒體單位。 |

#### 讀完後應能回答

1. 哪個欄位改變會使本例結果不同？
2. 此處是規範要求、支援能力，還是 informative example？

**來源欄位索引：** SWS, SGS

**來源 keyword 索引：** shall, should, may, reserved

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.9.3.1.1, Figure 712, 文件頁 624-625, PDF 頁 650-651

</details>

## 使用與限制

製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata 集合或核准範圍改變時，必須重新核對受影響 claim。

## 自問自答：規則、比較、案例與排錯

以下 148 題均附答案，針對本報告範圍複習。每題保留對應教學單元的來源；數值案例與排錯建議屬說明性內容。

### Q01. 「閱讀地圖與單位」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-foundation-lead -->

**答。**

本份從 namespace 與資料格式一路走到命令完成、資料完整性及管理證據。主線可分四堂各約 25 分鐘；逐圖附錄與問答供課後查詢。章節 1 的名詞與引用慣例也是範圍的一部分。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §1.1-1.6; 4.1.3.9; 4.1.4.8; 4.1.5, 文件頁 9-12,73-75,79-83, PDF 頁 9-12,73-75,79-83

### Q02. 「閱讀地圖與單位」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-foundation-rows -->

**答。**

- LBADS — data bytes = 2^LBADS — 另加 MS 才是 logical block size
- Format Index — 同時選 LBAF 與 ELBAF — 不能只看資料大小
- Specification family — 通用機制由 Base 定義 — 相依欄位另以 Base 來源標示

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §1.1-1.6; 4.1.3.9; 4.1.4.8; 4.1.5, 文件頁 9-12,73-75,79-83, PDF 頁 9-12,73-75,79-83

### Q03. 「閱讀地圖與單位」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-foundation-example -->

**答。**

LBADS=0Ch、MS=16 時，資料為 4096 bytes，含 metadata 的 logical block 是 4112 bytes。FID 28h 與 LID 28h 雖相同，前者設定限制，後者回報能力圖。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §1.1-1.6; 4.1.3.9; 4.1.4.8; 4.1.5, 文件頁 9-12,73-75,79-83, PDF 頁 9-12,73-75,79-83

### Q04. 「閱讀地圖與單位」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-foundation-pitfall -->

**答。**

本報告的算例是教學推導；不把示意數值寫成裝置必須具備的能力。對規格的 should、may 與 shall 保留不同強度。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §1.1-1.6; 4.1.3.9; 4.1.4.8; 4.1.5, 文件頁 9-12,73-75,79-83, PDF 頁 9-12,73-75,79-83

### Q05. 「Namespace 容量與配置狀態」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-capacity-lead -->

**答。**

先區分 logical address space 與實際配置，再分析寫入及 deallocate。讀取值與 allocation 狀態回答不同問題。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1; 4.1.5.1, 文件頁 13-14,85-93, PDF 頁 13-14,85-93

### Q06. 「Namespace 容量與配置狀態」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-capacity-rows -->

**答。**

- NSZE — 有效 LBA 為 0 到 NSZE−1 — LBA 越界與容量不足不同
- THINP — 支援時須追蹤 NUSE — 不支援時可固定回 NCAP
- Allocation — Write、Copy 寫入端及 WU 可配置 — Read／Verify 不改 deallocation 狀態

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1; 4.1.5.1, 文件頁 13-14,85-93, PDF 頁 13-14,85-93

### Q07. 「Namespace 容量與配置狀態」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-capacity-example -->

**答。**

NSZE=1000、NCAP=800、NUSE=600 可是合法 thin namespace。LBA 900 在可定址範圍內，但新增配置仍受 800-block capacity 限制。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1; 4.1.5.1, 文件頁 13-14,85-93, PDF 頁 13-14,85-93

### Q08. 「Namespace 容量與配置狀態」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-capacity-pitfall -->

**答。**

ANA 狀態可使 NUSE／NVMCAP 回零；不可僅憑回零宣告資料已刪除。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1; 4.1.5.1, 文件頁 13-14,85-93, PDF 頁 13-14,85-93

### Q09. 「命令順序與 Compare-and-Write」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-order-fused-lead -->

**答。**

先說明何時要排序，再判斷是否需要條件式更新。Fused 保護同一 LBA range 的比對與更新，原子大小仍須另外檢查。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.2-2.1.3, 文件頁 14-15, PDF 頁 14-15

### Q10. 「命令順序與 Compare-and-Write」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-order-fused-rows -->

**答。**

- Ordinary I/O — 同 LBA 的 Read／Write 完成先後無保證 — host 以完成相依控制
- Fused pair — Compare 與 Write 的 range 相同 — 範圍不符 should 拒絕
- ACWU / NACWU — 限制 fused atomic update 大小 — 還要遵守 atomic boundaries

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.2-2.1.3, 文件頁 14-15, PDF 頁 14-15

### Q11. 「命令順序與 Compare-and-Write」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-order-fused-example -->

**答。**

Host 想「目前值等於 A 才更新 B」時，獨立 Compare 成功後再送 Write 中間仍可能插入別人的寫入；符合大小與邊界的 fused pair 才提供此操作所需的條件式原子更新。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.2-2.1.3, 文件頁 14-15, PDF 頁 14-15

### Q12. 「命令順序與 Compare-and-Write」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-order-fused-pitfall -->

**答。**

Write 失敗不會回頭改寫 Compare 已得到的 completion status；必須檢查兩個 CQE。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.2-2.1.3, 文件頁 14-15, PDF 頁 14-15

### Q13. 「正常、斷電與多段原子性」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-atomic-lead -->

**答。**

把大小、起始對齊、NSABP 與 MAM 一起讀。Atomicity 與資料已進入 nonvolatile media 是不同檢查項目，FUA／Flush 也不建立其他命令的排序。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4; 4.1.3.4; 5.9, 文件頁 15-21,66-67,165, PDF 頁 15-21,66-67,165

### Q14. 「正常、斷電與多段原子性」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-atomic-rows -->

**答。**

- AWUN / AWUPF — 大小採 0-based 編碼 — AWUPF 不大於 AWUN
- NABO / NABSN / NABSPF — 邊界在 offset + k × size — 需依各欄位解碼與未回報規則
- MAM — 每個 atomic subrange 獨立保證 — fused 仍用 Single 模式
- FID 0Ah.DN — DN=1 可不遵守 normal atomicity — 仍須遵守 power-fail 保證

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4; 4.1.3.4; 5.9, 文件頁 15-21,66-67,165, PDF 頁 15-21,66-67,165

### Q15. 「正常、斷電與多段原子性」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-atomic-example -->

**答。**

假設解碼後 boundary size=8 blocks、offset=0，從 LBA 4 寫 12 blocks 跨成 [4..7] 與 [8..15]。MAM 下各段原子，不能將兩段當作一個 transaction。原始 AWUN=7h 才代表 8 blocks。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4; 4.1.3.4; 5.9, 文件頁 15-21,66-67,165, PDF 頁 15-21,66-67,165

### Q16. 「正常、斷電與多段原子性」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-atomic-pitfall -->

**答。**

不要把 §3.3.2.2 範例的「NAWUN=8h 表示 8 blocks」照抄；0-based 欄位與示意的已解碼大小必須區分。寫入失敗也可能完成 DMA，不能用 buffer 傳輸完成推論媒體成功。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4; 4.1.3.4; 5.9, 文件頁 15-21,66-67,165, PDF 頁 15-21,66-67,165

### Q17. 「能力探索、Opcode 與狀態」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-support-status-lead -->

**答。**

從 controller 類型開始建立命令、Feature、log 的能力矩陣。資料指標指向的可能是使用者資料，也可能只是控制 descriptor。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.2; 3.1; 3.3, 文件頁 22-27, PDF 頁 22-27

### Q18. 「能力探索、Opcode 與狀態」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-support-status-rows -->

**答。**

- Read 02h / Write 01h — 必要 I/O 命令 — Administrative controller 不處理 I/O
- Get LBA Status 86h — 選用 Admin 命令 — I/O controller 適用能力
- SC 80h — 依 SCT 區分 LBA Out of Range 等 — 同時記錄 opcode、NSID、SCT、SC、DNR
- FID / LID — 05h、0Ah 為必要 NVM Features — 功能支援不等於要求寫入 Persistent Event Log

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.2; 3.1; 3.3, 文件頁 22-27, PDF 頁 22-27

### Q19. 「能力探索、Opcode 與狀態」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-support-status-example -->

**答。**

Copy opcode=19h 的低 bits 是 01b，因 host 傳入 source descriptors；並不表示需要把整份待複製資料從 host 再傳一次。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.2; 3.1; 3.3, 文件頁 22-27, PDF 頁 22-27

### Q20. 「能力探索、Opcode 與狀態」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-support-status-pitfall -->

**答。**

FFFF FFFFh NSID 不是所有命令都接受；Figure 22 只有特別註明的 Flush／Cancel 路徑可支援。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.2; 3.1; 3.3, 文件頁 22-27, PDF 頁 22-27

### Q21. 「Read／Write 的資料與完成條件」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-read-write-lead -->

**答。**

把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4; 3.3.6, 文件頁 48-51,53-56, PDF 頁 48-51,53-56

### Q22. 「Read／Write 的資料與完成條件」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-read-write-rows -->

**答。**

- CDW10 / CDW11 — SLBA 低／高 32 bits — NLB=0 仍有一個 block
- CDW12 — LR、FUA、PRINFO、STC、CETYPE、NLB — Read 的 DTYPE 區是 reserved
- CDW13 — CETYPE 決定 DSM 或 CEV 解讀 — Write 另含 DTYPE／DSPEC
- MPTR — 單獨傳 metadata 時使用 — 不可把一部分 metadata 分到兩種機制

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4; 3.3.6, 文件頁 48-51,53-56, PDF 頁 48-51,53-56

### Q23. 「Read／Write 的資料與完成條件」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-read-write-example -->

**答。**

SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4; 3.3.6, 文件頁 48-51,53-56, PDF 頁 48-51,53-56

### Q24. 「Read／Write 的資料與完成條件」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-read-write-pitfall -->

**答。**

CQE 失敗時保存 SCT／SC 與 range，不能用 FUA 或成功 DMA 取代 CQE 結果。CETYPE 非零時也不能將 CDW13 低 bits 當作 DSM hints。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4; 3.3.6, 文件頁 48-51,53-56, PDF 頁 48-51,53-56

### Q25. 「Compare 與 Verify 解決不同問題」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-compare-verify-lead -->

**答。**

比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1; 3.3.5, 文件頁 27-30,51-53, PDF 頁 27-30,51-53

### Q26. 「Compare 與 Verify 解決不同問題」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-compare-verify-rows -->

**答。**

- Compare — miscompare 回 Compare Failure — host 與 media 兩側 PI 可分別檢查
- Verify — 沒有資料 buffer 傳輸 — 驗證量仍計入 Data Units Read
- VSL / NVMVFYS — variant 決定建議大小或硬上限 — 非零 VSL 以 2^n × minimum page size 表示

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1; 3.3.5, 文件頁 27-30,51-53, PDF 頁 27-30,51-53

### Q27. 「Compare 與 Verify 解決不同問題」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-compare-verify-example -->

**答。**

要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1; 3.3.5, 文件頁 27-30,51-53, PDF 頁 27-30,51-53

### Q28. 「Compare 與 Verify 解決不同問題」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-compare-verify-pitfall -->

**答。**

Verify 指定 PRACT=1 會回 Invalid Field in Command。把 Verify 寫成零長度 Read 或把 Compare 當成傳出資料都會錯誤配置 buffer。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1; 3.3.5, 文件頁 27-30,51-53, PDF 頁 27-30,51-53

### Q29. 「Copy：描述來源、連續目的與部分失敗」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-copy-lead -->

**答。**

先計算展開後的目的區間，再檢查格式、長度限制、重疊與 atomicity。Copy 可少用 host 資料傳輸，但不是無條件的 transaction。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, 文件頁 30-44, PDF 頁 30-44

### Q30. 「Copy：描述來源、連續目的與部分失敗」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-copy-rows -->

**答。**

- NR / NLB — source count 與各範圍 block count 都是 0-based — 檢查 MSRC、MSSRL、MCL
- FCO — 2h/3h 可要求 fast copy only — Fast Copy Not Possible 再看 DNR
- Overlap — 2h/3h 禁止同 namespace source 與 destination 重疊 — 0h/1h 重疊結果需依原子條件另讀
- NVMCSA — 1.3 將目的寫入視為單一 write command — 仍受 MAM、大小及 boundary 限制

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, 文件頁 30-44, PDF 頁 30-44

### Q31. 「Copy：描述來源、連續目的與部分失敗」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-copy-example -->

**答。**

兩個 source descriptors 的 NLB 都是 3，SDLBA=100：第一段寫 100..103、第二段寫 104..107，共 8 blocks。若 DW0=1，不能據此保證第二段或更後面完全未修改。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, 文件頁 30-44, PDF 頁 30-44

### Q32. 「Copy：描述來源、連續目的與部分失敗」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-copy-pitfall -->

**答。**

FCO 是對方法的限制，非每次 latency 保證。原子欄位 FFFFh 最多表示 65536 blocks，Copy 能超過此大小，不能據此宣告所有 Copy 都原子。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, 文件頁 30-44, PDF 頁 30-44

### Q33. 「Copy 的 PI 格式相容與轉換」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-copy-pi-lead -->

**答。**

以來源與目的是否有 PI 建立四種情況，再決定 PRINFOR.PRACT 與 PRINFOW.PRACT。每個 source 都必須符合選定模式。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2.3-3.3.2.4; 5.3.2.5, 文件頁 40-43,146-150, PDF 頁 40-43,146-150

### Q34. 「Copy 的 PI 格式相容與轉換」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-copy-pi-rows -->

**答。**

- PI → PI, 0/0 — matching formats：pass-through — 保護檢查仍由 checking bits 控制
- PI → PI, 1/1 — matching formats：replace — 讀端檢查，寫端產生 PI
- No PI → PI — corresponding formats 且 write PRACT=1：insert — 目的 metadata 不得包含其他用途
- PI → No PI — corresponding formats 且 read PRACT=1：strip — 來源 metadata 只能是 PI

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2.3-3.3.2.4; 5.3.2.5, 文件頁 40-43,146-150, PDF 頁 40-43,146-150

### Q35. 「Copy 的 PI 格式相容與轉換」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-copy-pi-example -->

**答。**

4096+8 bytes 的 16b PI namespace 可在符合 corresponding 條件時轉到 4096+0 bytes；4096+16 bytes 且其中 8 bytes 是額外 metadata，不能走這個 strip 特例。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2.3-3.3.2.4; 5.3.2.5, 文件頁 40-43,146-150, PDF 頁 40-43,146-150

### Q36. 「Copy 的 PI 格式相容與轉換」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-copy-pi-pitfall -->

**答。**

§5.3.2.5.1／.2 將 Figures 177–180 的引用對調；以各圖實際標題與 §3.3.2.4.2 的 0/0 pass-through、1/1 replace 規則交叉核對。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2.3-3.3.2.4; 5.3.2.5, 文件頁 40-43,146-150, PDF 頁 40-43,146-150

### Q37. 「Dataset Management 與三種 processing limits」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-dsm-lead -->

**答。**

先計算每個 block 是否同時通過三種 limit，再套用 NVMDSMSV。範圍與 hints 的合法性、處理義務以及實際媒體動作分開判斷。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, 文件頁 44-48, PDF 頁 44-48

### Q38. 「Dataset Management 與三種 processing limits」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-dsm-rows -->

**答。**

- AD / IDW / IDR — deallocate／整體寫入／整體讀取 hints — 可組合使用
- Limits nonzero, variant=0 — 超過任一 limit 回 Command Size Limit Exceeded — 全部符合則須處理 attributes
- Limits nonzero, variant=1 — 宜處理符合 limits 的部分 — 不以此原因回 Size Limit Exceeded
- All limits=0 — variant=1：不回報 limits；variant=0：不支援 — 三欄需全零或全非零

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, 文件頁 44-48, PDF 頁 44-48

### Q39. 「Dataset Management 與三種 processing limits」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-dsm-example -->

**答。**

DMRL=2、DMSL=1048，range 0 有 1024 blocks、range 1 有 512，且 DMRSL 不限制：variant=1 時前段與後段前 24 blocks 符合 limits。這不等於保證 1048 blocks 都已釋放。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, 文件頁 44-48, PDF 頁 44-48

### Q40. 「Dataset Management 與三種 processing limits」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-dsm-pitfall -->

**答。**

不要把 Write 的 NLB encoder 套到 DSM 的 LLB。以 0-based 寫入 LLB 會少描述一個 block；LLB=0 也不代表一個 block。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, 文件頁 44-48, PDF 頁 44-48

### Q41. 「Deallocated／unwritten 讀取規則」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-dealloc-lead -->

**答。**

先判斷是否允許成功讀取，再解釋成功回傳的 bytes。Allocation status、DRB 與 PI 有各自的條件。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3.2.1; 4.1.3.3, 文件頁 47-48,66, PDF 頁 47-48,66

### Q42. 「Deallocated／unwritten 讀取規則」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-dealloc-rows -->

**答。**

- DAE / DULBE — DAE 是 capability，DULBE 是啟用 — DULBE 預設 0
- DRB=000b — 不是任意舊資料 — 依 §3.3.3.2.1 為零或 FFh
- PI after deallocation — tag bytes 回 FFh；Guard 為 FFh 或 CRC — 配合 DLFEAT.GDS

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3.2.1; 4.1.3.3, 文件頁 47-48,66, PDF 頁 47-48,66

### Q43. 「Deallocated／unwritten 讀取規則」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-dealloc-example -->

**答。**

一次 Read 全零不能證明 sanitize 成功，可能只是 deallocated 的 DRB。反過來 DULBE 啟用後讀取報錯，也不能單凭此錯誤認定媒體故障。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3.2.1; 4.1.3.3, 文件頁 47-48,66, PDF 頁 47-48,66

### Q44. 「Deallocated／unwritten 讀取規則」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-dealloc-pitfall -->

**答。**

Read／Verify 成功不會使該 block 變回 allocated；重新寫入才會改變這個狀態。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3.2.1; 4.1.3.3, 文件頁 47-48,66, PDF 頁 47-48,66

### Q45. 「Write Uncorrectable、Write Zeroes 與整體清零」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-zero-uncorrectable-lead -->

**答。**

這兩個命令沒有 host user-data payload，但會改變 namespace 語意。先辨識範圍模式，再分配 PI 與 size-limit 檢查。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7-3.3.8, 文件頁 56-61, PDF 頁 56-61

### Q46. 「Write Uncorrectable、Write Zeroes 與整體清零」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-zero-uncorrectable-rows -->

**答。**

- Write Uncorrectable — 標記 block 後，讀取可能報 Unrecovered Read Error — WUSL 與 NVMWUSV 需成對看
- Write Zeroes PI — PRCHK=000b、STC=0 — PRACT=1 宜用於產生有效 PI
- WZSL / WZDSL — 依 DEAC 選適用 limit — NSZ=1 不受這兩欄限制
- LBACZ — 成功 NSZ 命令回 1 才表示全 namespace — 回 0 是指定 range

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7-3.3.8, 文件頁 56-61, PDF 頁 56-61

### Q47. 「Write Uncorrectable、Write Zeroes 與整體清零」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-zero-uncorrectable-example -->

**答。**

Host 送 NSZ=1 後得到 Successful Completion 與 LBACZ=0，必須判為僅 range 被清零；舊 controller 可能忽略不支援的 NSZ。不能將 command success 自動升格為整個 namespace 清零。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7-3.3.8, 文件頁 56-61, PDF 頁 56-61

### Q48. 「Write Uncorrectable、Write Zeroes 與整體清零」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-zero-uncorrectable-pitfall -->

**答。**

DEAC=0 不是禁止 deallocate：只要 zero-read 條件成立，controller 仍 may deallocate。失敗的 Write Zeroes 也可能已清掉部分內容。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7-3.3.8, 文件頁 56-61, PDF 頁 56-61

### Q49. 「Format、Host Behavior 與延伸 LBA」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-format-lead -->

**答。**

格式切換會改變 block 數與欄位適用性，建立 buffer 前要重新 Identify。能力列表與目前格式不能混用。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.2; 4.1.3.7, 文件頁 62-63,68-69, PDF 頁 62-63,68-69

### Q50. 「Format、Host Behavior 與延伸 LBA」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-format-rows -->

**答。**

- PI / PIL — PI=0 關閉，1/2/3 選 protection type — 本版 PIL 必須 0，PI 位於末端
- MSET — 1：extended LBA；0：separate metadata — MS=0 時忽略
- LBAFEE — FID 16h byte 2，合法值 0／1 — 配合 ELBAS 決定延伸格式
- STS — Format 不提供自由改成非零 STS 的方法 — 新配置可由 namespace create 建立

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.2; 4.1.3.7, 文件頁 62-63,68-69, PDF 頁 62-63,68-69

### Q51. 「Format、Host Behavior 與延伸 LBA」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-format-example -->

**答。**

要使用 64b Guard、MS=16 的格式，先確認 ELBAS、LBAFEE=1、對應 LBAF／ELBAF 及 PI capability。不能只設定 Format 的 PI=1 就宣告 64b Guard。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.2; 4.1.3.7, 文件頁 62-63,68-69, PDF 頁 62-63,68-69

### Q52. 「Format、Host Behavior 與延伸 LBA」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-format-pitfall -->

**答。**

PI type 1/2/3 與 Guard width 16/32/64 是不同維度。格式變更後 NSZE／NCAP 可改變，舊 LBA Range Type hints 也可能需重設。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.2; 4.1.3.7, 文件頁 62-63,68-69, PDF 頁 62-63,68-69

### Q53. 「基本 Features 的作用域與例外」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-basic-features-lead -->

**答。**

讀 Feature 時先辨識 scope、unit 與可儲存條件。Get、Set、Supported Capabilities 回覆也不能套用同一 payload 解碼。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.1-4.1.3.4, 文件頁 64-67, PDF 頁 64-67

### Q54. 「基本 Features 的作用域與例外」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-basic-features-rows -->

**答。**

- FID 03h — 4096-byte contiguous buffer；最多 64 個 64-byte entries — NUM 是 0-based；新 Set 取代前一次
- FID 05h.TLER — 100 ms 單位，從 error recovery 開始計時 — 0 代表不設 timeout；適用 LR 命令
- FID 03h attributes — Hide／Overwriteable 是 host 使用提示 — 不是安全隔離或資料保護機制
- FID 02h extension — idle exit 參考 NPWG-sized Read — 其他命令可超過該 latency limit

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.1-4.1.3.4, 文件頁 64-67, PDF 頁 64-67

### Q55. 「基本 Features 的作用域與例外」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-basic-features-example -->

**答。**

TLER=5 表示 error recovery 的 500 ms 限制，並不是從 SQ submit 起算的整筆命令 500 ms deadline。LBA Range Type 的 NUM=0 表示一個 entry。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.1-4.1.3.4, 文件頁 64-67, PDF 頁 64-67

### Q56. 「基本 Features 的作用域與例外」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-basic-features-pitfall -->

**答。**

Figure 92 的 persistence 欄只適用於不可 save 的 Feature；可 save 時應依 saved/default 規則處理。Controller 也不必驗證 LBA Range Type 每個欄位，不能依成功 Set 推論範圍完全合理。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.1-4.1.3.4, 文件頁 64-67, PDF 頁 64-67

### Q57. 「Identify：同一 namespace 的多份資料結構」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-identify-lead -->

**答。**

每次查詢都寫出 CNS、CSI、NSID、Format Index 的角色。不同查詢回零有不同含義，不能一律解讀為不存在或不支援。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5, 文件頁 83-110, PDF 頁 83-110

### Q58. 「Identify：同一 namespace 的多份資料結構」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-identify-rows -->

**答。**

- CNS 00h / 05h — namespace 的 NVM 基本／延伸欄位 — FLBAS 決定目前 FIDX；MC／DPC 是能力
- CNS 01h / 06h — AWUN 等通用位置與 NVM 專屬限制 — 06h 的 VSL／WZSL 等需結合 variant bits
- CNS 11h / 1Bh — allocated namespace 資訊 — 不等同 active namespace 查詢
- CNS 09h / 0Ah — 以 FIDX 查能力 — Common=No 欄位清零
- CNS 16h — namespace granularity list — GDM 決定 descriptor 如何對應 format

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5, 文件頁 83-110, PDF 頁 83-110

### Q59. 「Identify：同一 namespace 的多份資料結構」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-identify-example -->

**答。**

NSID=7 的目前格式需讀 FLBAS 再取同 index 的 LBAF 與 ELBAF。查尚未建立的 FIDX=3 能力，使用 09h／0Ah、CSI=0、NSID=0、FIDX=3，另結合 CNS08h 的共同能力。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5, 文件頁 83-110, PDF 頁 83-110

### Q60. 「Identify：同一 namespace 的多份資料結構」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-identify-pitfall -->

**答。**

§4.1.5.10.1 的 zoned namespace 字樣與本段 NVM 上下文不一致；教學以 CSI=00h 的 NVM namespace 解讀，並保留來源位置供查核。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5, 文件頁 83-110, PDF 頁 83-110

### Q61. 「LBAF、ELBAF 與唯一屬性格式」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-format-list-lead -->

**答。**

基本 entry 給資料／metadata 大小與相對效能，extended entry 給 PI 格式與 Storage Tag 分配。Unique-attribute entries 要個別查詢，不能沿用共同能力。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1; 4.1.5.3; 5.6, 文件頁 85-94,96-102,160-162, PDF 頁 85-94,96-102,160-162

### Q62. 「LBAF、ELBAF 與唯一屬性格式」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-format-list-rows -->

**答。**

- LBAF — LBADS、MS、RP — RP 是指定 workload 的相對級別
- ELBAF — PIF、QPIF、STS — QPIF 只在 qualified type 下適用
- FLBAS — FIDXU 與 FIDXL 組成 index — MTELBA 是另一個 metadata bit
- NULBAF — 追加在共同格式之後 — 09h／0Ah 能讀各自能力

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1; 4.1.5.3; 5.6, 文件頁 85-94,96-102,160-162, PDF 頁 85-94,96-102,160-162

### Q63. 「LBAF、ELBAF 與唯一屬性格式」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-format-list-example -->

**答。**

raw NLBAF=3、NULBAF=2：有 4 個共同格式及 2 個唯一屬性格式，共 6 個，合法 index 為 0..5。Figure 192 圖示採概念数量，不能直接代入未解碼的 raw NLBAF。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1; 4.1.5.3; 5.6, 文件頁 85-94,96-102,160-162, PDF 頁 85-94,96-102,160-162

### Q64. 「LBAF、ELBAF 與唯一屬性格式」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-format-list-pitfall -->

**答。**

LBADS=9 才是 512 bytes，LBADS=12 是 4096 bytes。§5.3.1.4.1 範例把 LBADS=0 寫成 512 bytes 是來源矛盾，不應用來產生命令。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1; 4.1.5.3; 5.6, 文件頁 85-94,96-102,160-162, PDF 頁 85-94,96-102,160-162

### Q65. 「建立 namespace：格式、mask 與 granularity」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-namespace-create-lead -->

**答。**

先取得 Format Index 能力再填 host-specified fields；不可直接把整份 Identify Namespace 原封不動當作 create payload。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6; 4.1.5.8; 5.8, 文件頁 108,110-113,165, PDF 頁 108,110-113,165

### Q66. 「建立 namespace：格式、mask 與 granularity」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-namespace-create-rows -->

**答。**

- NSZE / NCAP — 值以 logical blocks 指定 — 與 bytes granularity 比較前先換算
- LBSTM — 需符合 PIC／PIFA mask 約束 — 不符回 Invalid Field in Command
- GDM / ND — GDM=0 使用 descriptor 0 對全部格式 — ND 是 0-based
- Completion — 成功 create 後已按指定屬性 format — attachment 是另一個管理動作

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6; 4.1.5.8; 5.8, 文件頁 108,110-113,165, PDF 頁 108,110-113,165

### Q67. 「建立 namespace：格式、mask 與 granularity」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-namespace-create-example -->

**答。**

假設 NSG=1 MiB、NCG=1 MiB、logical block size=4096，NSZE=NCAP=256 的容量可完整定址；若改成 257，granularity hints 可能造成額外不可定址配置，但本身不是拒絕理由。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6; 4.1.5.8; 5.8, 文件頁 108,110-113,165, PDF 頁 108,110-113,165

### Q68. 「建立 namespace：格式、mask 與 granularity」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-namespace-create-pitfall -->

**答。**

Masking Not Supported 代表 Storage Tag mask 有效 bits 全為 1；不是全零。不支援或未啟用 FDP 時，placement 欄位也不能套用啟用後的語意。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6; 4.1.5.8; 5.8, 文件頁 108,110-113,165, PDF 頁 108,110-113,165

### Q69. 「FDP：placement、RUH 與可觀測數據」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-fdp-lead -->

**答。**

建立時決定 placement 關係，執行時看 handle status，事後再用 statistics／events 解釋媒體搬移。三種資料不能互相代替。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.2.1; 4.1.4.6-4.1.4.7; 4.1.6.3, 文件頁 26,79,110-113, PDF 頁 26,79,110-113

### Q70. 「FDP：placement、RUH 與可觀測數據」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-fdp-rows -->

**答。**

- NPHNDLS — 最多 128，且不超過 configuration 的 RUH 數 — 0 有 controller 選擇與共享規則
- EARUTR / RUAMW — 剩餘秒數估計／可寫 logical blocks — EARUTR=0 未回報；不是保證壽命
- LID 22h — HBMW／MBMW 含 NVM 指定寫入類命令 — 含 Copy 寫入端、Zeroes、Uncorrectable
- LID 23h event 0h — LBAV 控制 LBA 有效性 — NLBAM=FFFFh 表示至少 FFFFh

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.2.1; 4.1.4.6-4.1.4.7; 4.1.6.3, 文件頁 26,79,110-113, PDF 頁 26,79,110-113

### Q71. 「FDP：placement、RUH 與可觀測數據」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-fdp-example -->

**答。**

兩個 namespaces 共享 RUH 5，第一個使用 FIDX=2，第二個 create 指定 FIDX=3，即使資料大小同為 4 KiB，也不符合共享 RUH 的 Format Index 條件。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.2.1; 4.1.4.6-4.1.4.7; 4.1.6.3, 文件頁 26,79,110-113, PDF 頁 26,79,110-113

### Q72. 「FDP：placement、RUH 與可觀測數據」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-fdp-pitfall -->

**答。**

Media Reallocated event 的 LBA 是搬移集合中的一個 LBA，並不是完整清單；LBAV=0 時必須忽略。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.2.1; 4.1.4.6-4.1.4.7; 4.1.6.3, 文件頁 26,79,110-113, PDF 頁 26,79,110-113

### Q73. 「AER、SMART 與錯誤記錄的 NVM 補充」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-log-events-lead -->

**答。**

用事件找調查方向，再用正確 scope 的 log 與 command set 定義解碼。統計數據也要依命令分類，不能只按 opcode 名稱猜。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §1.4.2; 4.1.1; 4.1.3.5; 4.1.4.1-4.1.4.4, 文件頁 10-11,62,67,75-77, PDF 頁 10-11,62,67,75-77

### Q74. 「AER、SMART 與錯誤記錄的 NVM 補充」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-log-events-rows -->

**答。**

- LBASIN / RLCCN — FID0Bh bits 13／22 — 分別啟用 LBA Status／Rate Limiting notices
- SMART units — 先換算 512-byte units，再套 Base counter 編碼 — 不是每個 4 KiB block 加一個 Data Unit
- Read categories — Data Units Read 含 Verify；Host Read 含 Copy — Compare、Read 為兩類共同項
- Persistent Event 06h — create／single-delete 有 FLBAS、DPS — delete-all 時這兩欄 reserved

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §1.4.2; 4.1.1; 4.1.3.5; 4.1.4.1-4.1.4.4, 文件頁 10-11,62,67,75-77, PDF 頁 10-11,62,67,75-77

### Q75. 「AER、SMART 與錯誤記錄的 NVM 補充」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-log-events-example -->

**答。**

一個 Self-test FLBA=100、valid=1 的紀錄只能定位一個失敗 LBA，不能據此宣告其他 LBAs 全部正常。Error Information LBA=100 的「最低」語意也不能直接套到 FLBA。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §1.4.2; 4.1.1; 4.1.3.5; 4.1.4.1-4.1.4.4, 文件頁 10-11,62,67,75-77, PDF 頁 10-11,62,67,75-77

### Q76. 「AER、SMART 與錯誤記錄的 NVM 補充」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-log-events-pitfall -->

**答。**

Rate Limiting log 使用 CSI，其他表列 logs 多不使用；不要把相同 LID 的不同 command-set 定義混合。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §1.4.2; 4.1.1; 4.1.3.5; 4.1.4.1-4.1.4.4, 文件頁 10-11,62,67,75-77, PDF 頁 10-11,62,67,75-77

### Q77. 「LBA Status：通知、掃描與修復流程」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-lba-status-lead -->

**答。**

讀到 potentially unrecoverable 不是每個 block 一定無法讀取。先辨識 ATYPE，再檢查 buffer 是否足夠與 completion condition，最後安排資料修復。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.6; 4.1.4.5; 4.2.1; 5.2.1, 文件頁 67-68,77-79,114-122, PDF 頁 67-68,77-79,114-122

### Q78. 「LBA Status：通知、掃描與修復流程」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-lba-status-rows -->

**答。**

- MNDW / RL — MNDW 是 0-based dwords；RL=0 到 NSZE−1 — 不是 RL=0 查一個 block
- NLSD / CMPC — 實際 descriptor 數／完成原因 — CMPC=1 尚有資料或 scan 未完成；2 完成
- LSIPI / LSIRI — 100 ms 單位；poll interval 不可由 host 改 — Set 回傳最接近支援值
- RAE / LSGC — RAE=1 分段讀，RAE=0 清事件並允許更新 — 重讀 header 檢查 generation
- TLBAAG — 02h 可用較大 allocation granularity — 混合 allocated／deallocated unit 會整段回 allocated

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.6; 4.1.4.5; 4.2.1; 5.2.1, 文件頁 67-68,77-79,114-122, PDF 頁 67-68,77-79,114-122

### Q79. 「LBA Status：通知、掃描與修復流程」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-lba-status-example -->

**答。**

log 有 NLSLNE=0 但 ESTULB 非零時，不能當作沒有問題，宜檢查 attached namespaces 的完整 LBA 範圍。取得可疑 LBAs 後，可從其他可靠來源恢復並寫回；後續查詢會移除成功重寫且未再偵測的項目。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.6; 4.1.4.5; 4.2.1; 5.2.1, 文件頁 67-68,77-79,114-122, PDF 頁 67-68,77-79,114-122

### Q80. 「LBA Status：通知、掃描與修復流程」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-lba-status-pitfall -->

**答。**

CMPC=1 的 command success 不是全範圍掃描完成。Log 的 RNLB 與詳細 descriptor 的 NLB 都是 0-based，NLSD 卻是實際筆數。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.6; 4.1.4.5; 4.2.1; 5.2.1, 文件頁 67-68,77-79,114-122, PDF 頁 67-68,77-79,114-122

### Q81. 「Performance Characteristics 的屬性模型」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-performance-feature-lead -->

**答。**

此 Feature 回報或管理效能屬性，不能把標準 latency 級別當成對任意 workload 的服務保證。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, 文件頁 69-73, PDF 頁 69-73

### Q82. 「Performance Characteristics 的屬性模型」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-performance-feature-rows -->

**答。**

- R4KARL — 標準化 4 KiB random read 的平均 latency 區間 — 00h 是未回報
- MSVSPA / USVSPA — 可 save 總數／剩餘數 — index 可不連續
- PAID / ATTRL — 128-bit identifier／有效 vendor bytes — ATTRL 最大 FE0h
- RVSPA — 刪除 saved value 後取 default — 此操作不使用 data buffer 內容

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, 文件頁 69-73, PDF 頁 69-73

### Q83. 「Performance Characteristics 的屬性模型」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-performance-feature-example -->

**答。**

R4KARL=0Eh 表示 50 μs ≤ 平均 latency <100 μs，並非 14 μs。讀 C0h list 時應使 ATTRTYP 與 Get 的 SEL 一致，再用 PAID 解釋 vendor payload。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, 文件頁 69-73, PDF 頁 69-73

### Q84. 「Performance Characteristics 的屬性模型」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-performance-feature-pitfall -->

**答。**

Set ATTRI=00h 或 C0h 會回 Invalid Field in Command。Vendor bytes 的意義需要廠商定義，不能自行推測成標準欄位。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, 文件頁 69-73, PDF 頁 69-73

### Q85. 「Rate Limiting 的設定欄位」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-rate-config-lead -->

**答。**

先從 LID 28h 取得支援 target，再檢查 HLS／SLS 與 soft-controller 數量。把 host 請求限制和裝置可達能力分開記錄。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.9; 4.1.5.4; 5.10, 文件頁 73-75,106,165-168, PDF 頁 73-75,106,165-168

### Q86. 「Rate Limiting 的設定欄位」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-rate-config-rows -->

**答。**

- TGT / TID — CDW11[23:16]／[15:0] — TGT=0 才是標準 controller target
- RLC — RLE bit15；RLM=0 Hard、1 Soft — 支援 Soft 必須也支援 Hard
- BWSF — 0/1/2 = 1/10/100 MiB/s；3/4/5 = 1/10/100 GiB/s — 值乘 scale 才是 bandwidth
- WRIOPSR / WRBWR — write 分子除 read 分母 — 兩者的各 ratio bytes 均需非零

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.9; 4.1.5.4; 5.10, 文件頁 73-75,106,165-168, PDF 頁 73-75,106,165-168

### Q87. 「Rate Limiting 的設定欄位」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-rate-config-example -->

**答。**

BWSF=1、TBWV=50 表示 500 MiB/s。WBWV 與 WIOPS 控制寫入部分，總量還會按 WRBWR／WRIOPSR 加權；不能把 total 限制只當 read limit。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.9; 4.1.5.4; 5.10, 文件頁 73-75,106,165-168, PDF 頁 73-75,106,165-168

### Q88. 「Rate Limiting 的設定欄位」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-rate-config-pitfall -->

**答。**

未替某 target 設 limits 時，其 limits 是 vendor-specific；不能把缺少設定解讀為無限制。§5.10 開頭的 Hard／Soft 小節引用對調，正確是 5.10.1 Hard、5.10.2 Soft。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.9; 4.1.5.4; 5.10, 文件頁 73-75,106,165-168, PDF 頁 73-75,106,165-168

### Q89. 「Rate Limiting log 是能力圖」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-rate-graph-lead -->

**答。**

先做結構邊界檢查，再分析 bandwidth bottleneck。Port 的能力與共同 Endurance Group 的能力不同，不能把所有數字直接相加。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8; 5.10.3, 文件頁 79-83,168-172, PDF 頁 79-83,168-172

### Q90. 「Rate Limiting log 是能力圖」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-rate-graph-rows -->

**答。**

- LPL / offsets — 長度與指標皆有 dword 單位 — byte offset = dword offset ×4
- NP / NC / NST — 都是 0-based counts — NNSMAD 是實際數量
- SC / SI — subsystem／domain／EG／namespace 及其 ID — 依 scope 解讀，避免共享節點重算
- RLMA — 最大 read/write bandwidth／IOPS — workload 需符合相關 size／queue-depth 條件

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8; 5.10.3, 文件頁 79-83,168-172, PDF 頁 79-83,168-172

### Q91. 「Rate Limiting log 是能力圖」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-rate-graph-example -->

**答。**

兩個 PCIe ports 都能使用一個 Endurance Group，若 EG 的 bandwidth 已被 controller 0 用滿，controller 1 不會因多一個 port 就多一份媒體頻寬。相同 EG 能力可由兩個 controller 指向同一 descriptor。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8; 5.10.3, 文件頁 79-83,168-172, PDF 頁 79-83,168-172

### Q92. 「Rate Limiting log 是能力圖」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-rate-graph-pitfall -->

**答。**

Figures 196／198 的範例 offsets、byte ranges 與 LPL 有內部矛盾。本報告重畫關係並用 offset×4、descriptor length、LPL bounds 校驗，不把原範例當可直接執行的 binary fixture。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8; 5.10.3, 文件頁 79-83,168-172, PDF 頁 79-83,168-172

### Q93. 「Hard／Soft 與 token-bucket 算例」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-rate-modes-lead -->

**答。**

用能力、limits、實際 demand 三個值判讀結果。設定比例不等於任何時刻都固定吞吐；內部資源與工作負載仍會改變觀測值。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.10.1-5.10.2; Appendix A, 文件頁 166-168,176-177, PDF 頁 166-168,176-177

### Q94. 「Hard／Soft 與 token-bucket 算例」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-rate-modes-rows -->

**答。**

- Hard — 有需求且資源不足時按比例分享 — 設定上限不是最低效能保證
- Soft — 可使用閒置額度 — 多個 soft targets 依 limits 比例分享
- Write tokens — total bytes × WRBWR；write bytes；total IOPS × WRIOPSR；write IOPS 1 — 四個 buckets 各自檢查
- Read tokens — total bytes 及 total IOPS 1 — 不扣 write-only buckets

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.10.1-5.10.2; Appendix A, 文件頁 166-168,176-177, PDF 頁 166-168,176-177

### Q95. 「Hard／Soft 與 token-bucket 算例」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-rate-modes-example -->

**答。**

教學設定：4 KiB Write，WRBWR=2、WRIOPSR=3，分別消耗 total-bandwidth 8 KiB、write-bandwidth 4 KiB、total-IOPS 3、write-IOPS 1。4 KiB Read 只消耗 total-bandwidth 4 KiB 與 total-IOPS 1。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.10.1-5.10.2; Appendix A, 文件頁 166-168,176-177, PDF 頁 166-168,176-177

### Q96. 「Hard／Soft 與 token-bucket 算例」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-rate-modes-pitfall -->

**答。**

Token 不足時延後處理而非丟棄命令；可以處理部分，但不得在整筆處理完前先送 completion。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.10.1-5.10.2; Appendix A, 文件頁 166-168,176-177, PDF 頁 166-168,176-177

### Q97. 「對齊、granularity 與效能提示」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-alignment-lead -->

**答。**

先把 raw 欄位轉成 blocks，再評估 start alignment 與 length granularity。只滿足其中一項可能仍引發 read-modify-write。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, 文件頁 122-129, PDF 頁 122-129

### Q98. 「對齊、granularity 與效能提示」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-alignment-rows -->

**答。**

- NPWG / NPWA — 長度與起點同時符合 — 先看 NSFEAT.OPTPERF
- NPRG / NPRA / NORS — 適用讀取最佳化 — 先看 OPTRPERF
- NPDG / NPDGL — deallocate granularity 的不同欄位 — 用 OPTPERF 決定；Large 不一律加一
- NOIOB / NABO — 最佳 I/O boundary 與 atomic offset 不同 — 可分割 I/O 以符合多種條件

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, 文件頁 122-129, PDF 頁 122-129

### Q99. 「對齊、granularity 與效能提示」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-alignment-example -->

**答。**

解碼後 NPWG=8、NPWA=8。寫 LBA 8..15 同時符合；寫 9..16 雖然也是 8 blocks，仍跨兩個 granularity units，可能需要讀取兩端舊資料。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, 文件頁 122-129, PDF 頁 122-129

### Q100. 「對齊、granularity 與效能提示」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-alignment-pitfall -->

**答。**

來源圖的 read-modify-write 是可能機制，不是每台 SSD 一定執行的內部流程。Namespace 重新 format 後，舊的 alignment hints 可能失效。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, 文件頁 122-129, PDF 頁 122-129

### Q101. 「Metadata 傳輸與 PI 的位置」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-metadata-lead -->

**答。**

Metadata 不一定全是 PI。先標示 data、非 PI metadata 與 PI 三個區域，再計算 host buffer 大小與 CRC coverage。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.6; 5.2.3; 5.3, 文件頁 22,129-131, PDF 頁 22,129-131

### Q102. 「Metadata 傳輸與 PI 的位置」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-metadata-rows -->

**答。**

- Extended LBA — DPTR 指向 data+metadata 交錯序列 — MSET／MTELBA 反映此選擇
- Separate buffer — DPTR 給 data，MPTR 給 metadata — PRP metadata 需 physically contiguous；SGL 可分散
- PI location — 本版有效格式的 PI 在 metadata 末端 — CRC 包含之前的非 PI metadata

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.6; 5.2.3; 5.3, 文件頁 22,129-131, PDF 頁 22,129-131

### Q103. 「Metadata 傳輸與 PI 的位置」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-metadata-example -->

**答。**

8 blocks、data=4096、MS=16、PRACT=0：extended buffer 為 32896 bytes；separate 模式 data buffer=32768、metadata buffer=128 bytes。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.6; 5.2.3; 5.3, 文件頁 22,129-131, PDF 頁 22,129-131

### Q104. 「Metadata 傳輸與 PI 的位置」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-metadata-pitfall -->

**答。**

PI 在末端的位置規則與「metadata 是否 separate」是獨立維度；不能以 DIX／DIF 名稱省略 namespace format 設定。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.6; 5.2.3; 5.3, 文件頁 22,129-131, PDF 頁 22,129-131

### Q105. 「16／32／64b Guard 與 Qualified PI」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-pi-formats-lead -->

**答。**

先由 PIF 決定格式；PIF=11b 才由 QPIF 決定 Guard width，並受 QPIFS 與 STMLA 條件限制。Protection type 仍由 DPS 決定。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1; 4.1.5.3, 文件頁 97-102,130-138, PDF 頁 97-102,130-138

### Q106. 「16／32／64b Guard 與 Qualified PI」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-pi-formats-rows -->

**答。**

- 16b Guard — 2-byte Guard + 2-byte App + 4-byte space — STS=0..32
- 32b Guard — 4-byte Guard + 2-byte App + 10-byte space — STS=16..64
- 64b Guard — 8-byte Guard + 2-byte App + 6-byte space — STS=0..48
- STMLA — bit mask／byte mask／no mask — qualified type 與 QPIFS 共同決定適用

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1; 4.1.5.3, 文件頁 97-102,130-138, PDF 頁 97-102,130-138

### Q107. 「16／32／64b Guard 與 Qualified PI」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-pi-formats-example -->

**答。**

64b Guard、STS=18：48-bit space 中高 18 bits 是 Storage Tag、低 30 bits 是 Reference Tag。PI 總大小仍為 16 bytes，不會因 STS 增加而變大。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1; 4.1.5.3, 文件頁 97-102,130-138, PDF 頁 97-102,130-138

### Q108. 「16／32／64b Guard 與 Qualified PI」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-pi-formats-pitfall -->

**答。**

本版保留 qualified type，不能把 PIF=11b 一概當 reserved。STS 等於整個 space 時 Reference Tag 不存在；STS=0 時 Storage Tag 不存在。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1; 4.1.5.3, 文件頁 97-102,130-138, PDF 頁 97-102,130-138

### Q109. 「CRC 參數、位元順序與已知向量」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-crc-lead -->

**答。**

CRC 的 polynomial、初值、reflection、final XOR 與儲存順序必須一起核對。用已知向量驗證後才接進 PI parser。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.1-5.3.1.3, 文件頁 131-137, PDF 頁 131-137

### Q110. 「CRC 參數、位元順序與已知向量」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-crc-rows -->

**答。**

- CRC-16 — SBC-4 定義的 Guard CRC — NVM 不支援 DIX 的 optional IP checksum
- CRC-32C — polynomial 1EDC6F41h — 4 KiB zero vector → 98F94189h
- CRC-64/NVME — 反射式 register 算例 123456789 → AE8B14860A799888h — 4 KiB zero vector → 6482D367EB22B64Eh
- Coverage — data + PI 前的 metadata — 排除 PI 本身

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.1-5.3.1.3, 文件頁 131-137, PDF 頁 131-137

### Q111. 「CRC 參數、位元順序與已知向量」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-crc-example -->

**答。**

CRC-64 的 4 KiB 全 FFh 向量結果為 C0DDBA7302ECA3ACh。若 zero vector 正確而 incrementing-byte vector 不符，要檢查 byte／bit 順序，不能只改 polynomial 硬湊。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.1-5.3.1.3, 文件頁 131-137, PDF 頁 131-137

### Q112. 「CRC 參數、位元順序與已知向量」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-crc-pitfall -->

**答。**

Figure 161 列 Check=11199E506128D175h；常見 LSB-first register 對 123456789 算得 AE8B14860A799888h，兩者互為 64-bit 反轉。Figure 163 的四個 4 KiB 向量則直接符合該 register 結果。須明示表示差異，不因單一 Check 差異改 polynomial；CRC 也不是密碼學認證。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.1-5.3.1.3, 文件頁 131-137, PDF 頁 131-137

### Q113. 「Storage／Reference Tag 的 Dword 封裝」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-tag-layout-lead -->

**答。**

先決定總 space 大小，再切 tag，最後拆到命令 Dwords。不要因 tag 的名稱相似就把 Write 的值與 Read 的 expected 值交換。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, 文件頁 137-141, PDF 頁 137-141

### Q114. 「Storage／Reference Tag 的 Dword 封裝」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-tag-layout-rows -->

**答。**

- 16b Guard, STS=0 — CDW14 為 32-bit reference — CDW2／3 對此 tag 忽略
- 32b Guard, STS=32 — CDW2 low16 + CDW3 high16 是 Storage — CDW3 low16 + CDW14 為 48-bit Reference
- 64b Guard, STS=18 — CDW3 low16 + CDW14 high2 是 Storage — CDW14 low30 是 Reference

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, 文件頁 137-141, PDF 頁 137-141

### Q115. 「Storage／Reference Tag 的 Dword 封裝」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-tag-layout-example -->

**答。**

64b Guard、STS=18、Storage Tag=0x12345、Reference Tag=0x2A：CDW3 low16=0x48D1，CDW14=(1<<30)|0x2A=0x4000002A。Read 使用相同布局的 expected tags。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, 文件頁 137-141, PDF 頁 137-141

### Q116. 「Storage／Reference Tag 的 Dword 封裝」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-tag-layout-pitfall -->

**答。**

Figure 171 對 CDW3 的 Storage Tag bit range 與下一列重疊；以 Figure 166 與對稱的 Figure 170 判讀為 high16，並記錄這是來源矛盾的工程解讀。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, 文件頁 137-141, PDF 頁 137-141

### Q117. 「PRACT 與 PRCHK／STC 的組合」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-pi-checking-lead -->

**答。**

先檢查 namespace 是否啟用 PI，再依命令方向及 metadata 大小選處理分支。Checking bits 與可能的特殊停用值放在最後判斷。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5; 5.3.2-5.3.3, 文件頁 21-22,141-152, PDF 頁 21-22,141-152

### Q118. 「PRACT 與 PRCHK／STC 的組合」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-pi-checking-rows -->

**答。**

- Write, PRACT=1 — MS=PI 時插入；MS>PI 時取代 PI — 此生成分支忽略 PRCHK／STC
- Read, PRACT=1 — 先做要求的檢查；MS=PI 才移除 — MS>PI 仍回 metadata 與 PI
- Type 1 / Type 2 — Reference 每個 block 遞增 — Type1 初值須等於對應 SLBA 低 bits
- Type 3 — 不宜比對 computed reference — 若因 RTCHK 拒絕，使用 Invalid Protection Information
- Disable sentinels — Type 1／2：Application Tag=FFFFh 時停用所有 PI checks；Type 3 另要求 Reference Tag（若有）也全一 — 不受 PRCHK／STC 設定影響
- Masks — mask bit=0 不比較 — Storage mask 另受 STMLA 約束

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5; 5.3.2-5.3.3, 文件頁 21-22,141-152, PDF 頁 21-22,141-152

### Q119. 「PRACT 與 PRCHK／STC 的組合」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-pi-checking-example -->

**答。**

16b Guard、MS=16、Read PRACT=1：host 仍接收 16 bytes metadata；若 MS=8，則 host 只接收 data。相同 PRACT 在不同 MS 下造成不同 buffer 大小。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5; 5.3.2-5.3.3, 文件頁 21-22,141-152, PDF 頁 21-22,141-152

### Q120. 「PRACT 與 PRCHK／STC 的組合」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-pi-checking-pitfall -->

**答。**

STC 在本份指 Storage Tag Check；不要沿用 Self-test Code 的縮寫解釋。Compare 的兩條輸入路徑都可能執行 PI checking，但 PI bytes 不納入一般 metadata 比對。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5; 5.3.2-5.3.3, 文件頁 21-22,141-152, PDF 頁 21-22,141-152

### Q121. 「ANA 與 Reservations 的 NVM 行為」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-ana-reservations-lead -->

**答。**

同一 namespace 的可達性與存取權限要分開檢查；不能將路徑狀態等同 reservation ownership。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.1; 5.11, 文件頁 119,172-173, PDF 頁 119,172-173

### Q122. 「ANA 與 Reservations 的 NVM 行為」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-ana-reservations-rows -->

**答。**

- ANA Identify — Inaccessible／Persistent Loss 下 NUSE、NVMCAP 回零 — 不是 media 被清空
- ANA FID05h — Get 的 Inaccessible／Persistent Loss／Change 受限 — 使用對應 ANA status
- Write Exclusive / Exclusive Access — 非 holder：前者允許 read-like；後者 read／write-like 都衝突 — 兩者的非 holder write-like 都衝突
- Registrants Only / All Registrants — Write Exclusive 類允許所有人 read、registrants write；Exclusive Access 類僅 registrants read／write — Copy 每個 source 用 read 權限，destination 用 write 權限
- Reservations — 分 read-like、write-like 命令查矩陣 — holder、registrant 與 type 必須一起看

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.1; 5.11, 文件頁 119,172-173, PDF 頁 119,172-173

### Q123. 「ANA 與 Reservations 的 NVM 行為」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-ana-reservations-example -->

**答。**

同一 SSD 的兩個 PCIe controllers 可共享 namespace。Controller 1 的路徑可用，仍可能因 reservation 類型與自身 registration 狀態而無法 Write；Read 是否允許需另外查表。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.1; 5.11, 文件頁 119,172-173, PDF 頁 119,172-173

### Q124. 「ANA 與 Reservations 的 NVM 行為」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-ana-reservations-pitfall -->

**答。**

不能僅憑存在 Reservation 就一律封鎖所有非 holder 的 I/O；Write Exclusive 與 Exclusive Access 等類型的讀取規則不同。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.1; 5.11, 文件頁 119,172-173, PDF 頁 119,172-173

### Q125. 「LBA Migration Queue 與變更追蹤」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-migration-queue-lead -->

**答。**

這個 queue 保存變更範圍與序列標記，不保存完整新資料。Host 讀 entry 後仍需以適當 I/O 取得資料，並處理滿 queue 的停止邊界。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.8; 5.7, 文件頁 113-114,162-164, PDF 頁 113-114,162-164

### Q126. 「LBA Migration Queue 與變更追蹤」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-migration-queue-rows -->

**答。**

- LBACIR — 00：range；01：整個 namespace；10：無 range — 先判斷欄位是否有效
- ESA — 001 start／resume；010 stop；011 suspend；111 full — full 表示 logging 已停止
- DLBA / CDQP — deallocated 標記／entry phase — DLBA=0 仍可能描述 deallocate 類修改
- RALBAS — 開始命令處理期間的變更可由 ATYPE02h 補齊 — start／stop marker 不要求先於 Track Send CQE

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.8; 5.7, 文件頁 113-114,162-164, PDF 頁 113-114,162-164

### Q127. 「LBA Migration Queue 與變更追蹤」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-migration-queue-example -->

**答。**

三筆連續 Write 可合併成一個 range entry；所以 queue entry 數不等於寫入命令數。ESA=111b 後，host 不能假設後續每次修改仍持續記錄。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.8; 5.7, 文件頁 113-114,162-164, PDF 頁 113-114,162-164

### Q128. 「LBA Migration Queue 與變更追蹤」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-migration-queue-pitfall -->

**答。**

此處教學為 NVM 的 LBA 變更追蹤；不藉此展開其他傳輸協定或資源匯出格式。重新開始追蹤前要處理 queue 容量與資料一致性。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.8; 5.7, 文件頁 113-114,162-164, PDF 頁 113-114,162-164

### Q129. 「Sanitize 與 Media Verification 的 NVM 規則」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-sanitize-lead -->

**答。**

先辨識 target、operation state 與 allocation，再決定可以驗證什麼。命令 CQE 與 sanitize operation 完成分別由不同證據表示。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.7; 5.12, 文件頁 113,173-175, PDF 頁 113,173-175

### Q130. 「Sanitize 與 Media Verification 的 NVM 規則」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-sanitize-rows -->

**答。**

- LID81h — 追蹤 operation status／progress — 啟動命令成功不是 operation 完成
- Error Information — sanitize 期間 NVM LBA 欄位回 0 — 僅此 NVM 補充，仍須遵守 Base command allowlist
- Media Verification Read — PRCHK=000b、STC=0 — 要求 checking 則 Invalid Field in Command
- Allocated media — 可讀則回實際資料；不可讀則錯誤 — 符合條件回 Successful Media Verification Read

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.7; 5.12, 文件頁 113,173-175, PDF 頁 113,173-175

### Q131. 「Sanitize 與 Media Verification 的 NVM 規則」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-sanitize-example -->

**答。**

Media Verification state 中，Read 不要求 PI checking 且 allocated media 可讀時，可以忽略讀得出資料的 integrity error 並回特定成功狀態；同一 LBA 連續讀值仍 may 不同。不能用平常 Read 的固定值假設評估它。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.7; 5.12, 文件頁 113,173-175, PDF 頁 113,173-175

### Q132. 「Sanitize 與 Media Verification 的 NVM 規則」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-sanitize-pitfall -->

**答。**

Sanitize 之後讀零不是充分的成功證據，也不是所有方法都應回零。Namespace sanitize 與 subsystem sanitize 的 scope 不可互換。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.7; 5.12, 文件頁 113,173-175, PDF 頁 113,173-175

### Q133. 「Key Per I/O 的 NVM 對齊約束」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-key-per-io-lead -->

**答。**

先從 KPIOCAP 與 namespace status 判斷適用，再解讀 CETYPE／CEV 的 command extension。金鑰建立及管理不由這份 NVM 補充完整定義。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.5; 4.1.5, 文件頁 91-92,105,160, PDF 頁 91-92,105,160

### Q134. 「Key Per I/O 的 NVM 對齊約束」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-key-per-io-rows -->

**答。**

- KPIOCAP — 支援與 subsystem／namespace scope — 不能只看單一 enable bit
- KPIOSNS / KPIOENS — namespace 支援／啟用 — 未支援時 enable 必須為 0
- KPIODAAG — 0-based logical-block granularity — 起點及長度都必須符合

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.5; 4.1.5, 文件頁 91-92,105,160, PDF 頁 91-92,105,160

### Q135. 「Key Per I/O 的 NVM 對齊約束」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-key-per-io-example -->

**答。**

raw KPIODAAG=7 代表 8-block granularity。SLBA=16、length=8 符合；SLBA=17 或 length=7 都不符合，即使其他 PI 欄位完全正確也不能使用。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.5; 4.1.5, 文件頁 91-92,105,160, PDF 頁 91-92,105,160

### Q136. 「Key Per I/O 的 NVM 對齊約束」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-key-per-io-pitfall -->

**答。**

Invalid Key Tag 與 alignment 的 Invalid Field in Command 需要不同調查方向；不能將 key-tag 拒絕都歸類為 PI checksum 錯誤。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.5; 4.1.5, 文件頁 91-92,105,160, PDF 頁 91-92,105,160

### Q137. 「Streams 的 NVM 單位與優先順序」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-streams-lead -->

**答。**

用兩層大小模型解釋 Stream Write Size 與較大的 stream granularity。它們可能和 namespace hints 成整數倍，但規格不保證每個 namespace 都如此。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2.3; 5.13, 文件頁 128-129,175, PDF 頁 128-129,175

### Q138. 「Streams 的 NVM 單位與優先順序」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-streams-rows -->

**答。**

- SWS — 建議寫入大小，以 blocks 計 — 宜為 NPWG 的倍數
- SGS × SWS — stream granularity 的長度 — 適用 stream deallocate 對齊／長度
- Priority — 用 Streams 時優先 Streams attributes — 未使用則用 namespace hints

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2.3; 5.13, 文件頁 128-129,175, PDF 頁 128-129,175

### Q139. 「Streams 的 NVM 單位與優先順序」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-streams-example -->

**答。**

解碼後 SWS=8 blocks、SGS=4，stream granularity 是 32 blocks。8-block Write 可符合 SWS，但一個完整 granularity-unit 的 deallocate 長度是 32 blocks。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2.3; 5.13, 文件頁 128-129,175, PDF 頁 128-129,175

### Q140. 「Streams 的 NVM 單位與優先順序」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-streams-pitfall -->

**答。**

Streams hints、FDP placement 與 namespace atomicity 是不同概念；不能只因尺寸相等就推論是同一個內部媒體單位。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2.3; 5.13, 文件頁 128-129,175, PDF 頁 128-129,175

### Q141. 「Memory-based 資源匯出範本」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-export-template-lead -->

**答。**

範本固定的相容性介面與 underlying 裝置能力是兩層。先確認 namespace 格式相容，再設定不超過 underlying 能力的限制；沒有被範本開放的能力不能自行宣告。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4.1-5.4.1.1, 文件頁 152-159, PDF 頁 152-159

### Q142. 「Memory-based 資源匯出範本」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-export-template-rows -->

**答。**

- Identity and version — CAP.CSS=1、VS=020300h；NVM VER=010200h — 範本固定 Base 2.3／NVM 1.2，不隨本 PDF 版本自動升級
- Controller limits — MDTS、RAB、NCQS、NSQS、MQES、AWUN／AWUPF 受 underlying 限制 — NCQS／NSQS 是 0-based
- Namespace compatibility — LBAF0 的 LBADS／MS 必須相同，MS=0；DPS／KPIOENS／CWP 必須為零 — controller 負責 Format Index remapping
- Observable defaults — Error entries 與 SMART 為零；firmware active slot=1 — 支援清單、Feature defaults 與 Identify exceptions 另有固定規則

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4.1-5.4.1.1, 文件頁 152-159, PDF 頁 152-159

### Q143. 「Memory-based 資源匯出範本」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-export-template-example -->

**答。**

Underlying NCQS=7 可支援 8 queues，範本設定 NCQS=3 表示最多 4 queues；不能把 raw 3 誤解成 3 queues。Namespace 的 NGUID 為零時，NUUID 必須提供有效 UUID。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4.1-5.4.1.1, 文件頁 152-159, PDF 頁 152-159

### Q144. 「Memory-based 資源匯出範本」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-export-template-pitfall -->

**答。**

Figure 190 的 caption 寫 Controller，但 payload 是 namespace configuration；依 ENSID、LBAF0、NGUID 與 NUUID 判讀。Figure 189 僅教核准的本機欄位；其餘身分欄位不展開。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4.1-5.4.1.1, 文件頁 152-159, PDF 頁 152-159

### Q145. 「匯出狀態的長度與一致性」的核心判讀規則是什麼？

<!-- qa:nvm-command-set-1.3-nvmcs-export-state-lead -->

**答。**

先讀固定 64-byte header，再檢查可變長度與 suspension 證據。Configuration state 與執行中 state 的用途和設定限制不同，不能共用 payload parser。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4.1.2, 文件頁 159-160, PDF 頁 159-160

### Q146. 「匯出狀態的長度與一致性」中，哪些概念或條件必須分開比較？

<!-- qa:nvm-command-set-1.3-nvmcs-export-state-rows -->

**答。**

- Feature values — 保存 arbitration、power、temperature、error recovery、queues、interrupt、atomicity 與 AEC — 是 current values，不是 Figure 187 defaults
- CSATTR.CP — 1 表示整段處理期間 suspended — 0 不保證完全沒有 suspension
- NVMECSS — 總長度 = 64 + 4 × NVMECSS bytes — 0 時 NVMECS 欄位不存在

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4.1.2, 文件頁 159-160, PDF 頁 159-160

### Q147. 「匯出狀態的長度與一致性」如何套用到具體數值或操作情境？

<!-- qa:nvm-command-set-1.3-nvmcs-export-state-example -->

**答。**

NVMECSS=16 時，NVMECS 有 64 bytes，整個結構有 128 bytes；先檢查乘法、加法與接收 buffer bounds，再解碼內層 VER。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4.1.2, 文件頁 159-160, PDF 頁 159-160

### Q148. 「匯出狀態的長度與一致性」最容易出現什麼誤判？如何排查？

<!-- qa:nvm-command-set-1.3-nvmcs-export-state-pitfall -->

**答。**

這是 memory-based controller state 的教學；沒有完整 state 與 suspension 證據時，不從單一 Feature value 推論整個 subsystem 已安全移轉。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4.1.2, 文件頁 159-160, PDF 頁 159-160
