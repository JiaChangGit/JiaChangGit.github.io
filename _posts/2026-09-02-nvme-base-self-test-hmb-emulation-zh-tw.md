---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4：Device Self-test、HMB、Doorbell Emulation 與 Vendor Commands"
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

# NVMe Base 2.4：Device Self-test、HMB、Doorbell Emulation 與 Vendor Commands

用途：供 GitHub Pages 閱讀與 100 分鐘簡報製作；讀者已具備 PCIe 與 NVMe 基礎。

範圍：Base §5.2.6、§5.2.13.1.7、§5.2.30.2.3、§8.1.8、§8.1.29、§8.2.3、§8.2.4，以及 NVM Command Set 1.3 §4.1.4.3；另含建構命令與能力判斷所需的最小 dependency slice。正文只保留 PCIe／memory-based 與通用 NVMe 內容。

## 來源版本

NVM Express Base Specification, Revision 2.4
NVM Express NVM Command Set Specification, Revision 1.3

查證日期：2026-09-02。目前未納入其他 Errata、ECN、Technical Proposal、controller vendor 文件或未提供的 PCI Express Base Specification 原文。

## 閱讀地圖

```text
Discover capability -> Construct command / memory -> Controller background work -> Read completion / log evidence
```

三條工程主線共享同一個原則：先確認 capability 與 ownership boundary，再提交 command 或 MMIO notification，最後用 CQE、log page 與記憶體生命週期證明結果。

## 規範性用語

shall 譯為「必須」，may 譯為「可／得」，should 譯為「宜／建議」，optional 譯為「選用」。本文不提高或降低原文語氣。

## 先學縮寫：完整 Glossary

下列縮寫會在投影片主線使用前先定義。縮寫本身永遠不夠；設計與 Debug 還要保留 owner、width、unit、scope 與 state。

| 縮寫／名詞 | 白話解釋 | 來源 |
|---|---|---|
| `DST` | Device Self-test，用背景 diagnostic segments 檢查 controller 與可選 namespace media 的操作。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.8，文件頁 352-358, 614，PDF 頁 378-384, 640 |
| `OACS.DSTS` | Optional Admin Command Support 的 Device Self-test Supported bit，判斷 command 是否可用。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.8，文件頁 352-358, 614，PDF 頁 378-384, 640 |
| `STC` | Self-test Code，Device Self-test CDW10 中選 short、extended、refresh、vendor-specific 或 abort 的 nibble。 | NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 199-200，PDF 頁 225-226 |
| `DSTP` | Device Self-test Parameter，只有 vendor-specific STC=Eh 時才有 vendor-defined 語意的 CDW15。 | NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 199-200，PDF 頁 225-226 |
| `DSTO` | Device Self-test Options，Identify Controller 中回報 refresh 與 concurrency 選項的欄位。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.8，文件頁 352-358, 614，PDF 頁 378-384, 640 |
| `SDSO` | Single Device Self-test Operation，選擇 subsystem-wide 單一 operation 或 per-controller operation 的 bit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.8，文件頁 352-358, 614，PDF 頁 378-384, 640 |
| `EDSTT` | Extended Device Self-test Time，在 power state 0 下的 extended test 名目完成分鐘數。 | NVME-BASE-2.4 Rev. 2.4，§8.1.8.1-8.1.8.2，文件頁 615-616，PDF 頁 641-642 |
| `DSTOS` | Device Self-test Operation Status，LID 06h 中表示目前 operation 類型的 nibble。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 229-230，PDF 頁 255-256 |
| `DSTCS` | Device Self-test Completion Status，LID 06h 中的 0 到 100 完成百分比。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 229-230，PDF 頁 255-256 |
| `DSTR` | Device Self-test Result，結果 entry 中表示成功、abort 或 segment failure 的 nibble。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 231，PDF 頁 257 |
| `SEGN` | Segment Number，只有 DSTR=7h 時指出第一個失敗 diagnostic segment。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 231，PDF 頁 257 |
| `VDINFO` | Valid Diagnostic Information，分別 gate NSID、FLBA、SCT 與 SC 的 validity bitmap。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 231-232，PDF 頁 257-258 |
| `FVLD` | Failing LBA Valid，決定 FLBA 欄位是否可解讀的 validity bit。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.4.3，文件頁 76，PDF 頁 76 |
| `FLBA` | Failing LBA，NVM Command Set 定義為造成 self-test failure 的其中一個 logical block address。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.4.3，文件頁 76，PDF 頁 76 |
| `POH` | Power On Hours，self-test result 建立時累積的 power-on hours，不含指定 low-power 時間。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7, 8.1.8，文件頁 229-232, 614-616，PDF 頁 255-258, 640-642 |
| `HMB` | Host Memory Buffer，由 host 配置並在 enable 期間交由 controller 專用的 volatile memory ranges。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3, 8.2.4，文件頁 515-516, 744，PDF 頁 541-542, 770 |
| `HMPRE` | Host Memory Buffer Preferred Size，以 4 KiB units 回報 controller 偏好的配置大小。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.2.4，文件頁 357, 362, 744，PDF 頁 383, 388, 770 |
| `HMMIN` | Host Memory Buffer Minimum Size，以 4 KiB units 回報 controller 要求的最低大小。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.2.4，文件頁 357, 362, 744，PDF 頁 383, 388, 770 |
| `HMMINDS` | Host Memory Buffer Minimum Descriptor Entry Size，每個可用 descriptor 的最低 4 KiB-unit 大小。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.2.4，文件頁 357, 362, 744，PDF 頁 383, 388, 770 |
| `HMMAXD` | Host Memory Maximum Descriptor Entries，controller 可使用的 descriptor entry 上限。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.2.4，文件頁 357, 362, 744，PDF 頁 383, 388, 770 |
| `HMDL` | Host Memory Descriptor List，連續存放 16-byte HMB descriptors 的 host-memory array。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3，文件頁 517-518，PDF 頁 543-544 |
| `HMDLEC` | Host Memory Descriptor List Entry Count，HMDL 中有效 entries 的數量。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30, 5.2.30.2.3，文件頁 456-459, 516-518，PDF 頁 482-485, 542-544 |
| `HSIZE` | Host Memory Buffer Size，以 CC.MPS memory-page units 表示的 HMB 總大小。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3，文件頁 516-518，PDF 頁 542-544 |
| `EHM` | Enable Host Memory，啟用或停用 controller 使用 HMB 的 bit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3，文件頁 515-516，PDF 頁 541-542 |
| `MR` | Memory Return，表示 host 歸還完全相同的舊 HMB size、addresses、descriptors 與 contents。 | NVME-BASE-2.4 Rev. 2.4，§8.2.4，文件頁 744，PDF 頁 770 |
| `HMNARE` | Host Memory Non-operational Access Restriction Enable，配置 non-operational HMB access policy 的 bit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3，文件頁 516-519，PDF 頁 542-545 |
| `HMNAR` | Host Memory Non-operational Access Restricted，回報 restriction 此刻是否實際生效的 state bit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3，文件頁 516-519，PDF 頁 542-545 |
| `BADD` | Buffer Address，HMB descriptor 中依 CC.MPS 對齊的 memory-page address。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3，文件頁 517-518，PDF 頁 543-544 |
| `BSIZE` | Buffer Size，HMB descriptor 中以 CC.MPS pages 表示的連續範圍長度。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3，文件頁 517-518，PDF 頁 543-544 |
| `DSTRD` | Doorbell Stride，CAP 中決定相鄰 doorbell register 間距的欄位。 | NVME-BASE-2.4 Rev. 2.4，§3.1.4.1, 8.2.3，文件頁 56, 744，PDF 頁 82, 770 |
| `NDT` | Number of Dwords in Data Transfer，standard vendor-specific format 中的實際 data dword 數。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1, 8.1.29，文件頁 143, 733，PDF 頁 169, 759 |
| `NDM` | Number of Dwords in Metadata Transfer，standard vendor-specific format 中的實際 metadata dword 數。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1, 8.1.29，文件頁 143, 733，PDF 頁 169, 759 |
| `AVSCC` | Admin Vendor Specific Command Configuration，回報 vendor-specific Admin command format 的 Identify field。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.29，文件頁 356, 374, 733，PDF 頁 382, 400, 759 |
| `ICSVSCC` | I/O Command Set Vendor Specific Command Configuration，回報 vendor-specific I/O command format 的 Identify field。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.29，文件頁 356, 374, 733，PDF 頁 382, 400, 759 |
| `VSCF` | Vendor Specific Command Format，AVSCC 中表示 Admin commands 是否使用 Figure 94 的 bit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.29，文件頁 356, 374, 733，PDF 頁 382, 400, 759 |
| `SNVSCF` | Same NVM Vendor Specific Command Format，ICSVSCC 中表示 I/O commands 是否使用 Figure 94 的 bit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.29，文件頁 356, 374, 733，PDF 頁 382, 400, 759 |
| `NSID` | Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。 | NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 199，PDF 頁 225 |
| `CQE` | Completion Queue Entry，CQ 中的一筆完成結果資料結構。 | NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 201，PDF 頁 227 |
| `FID` | Feature Identifier，Get／Set Features 用來選擇功能的 8-bit identifier。 | NVME-BASE-2.4 Rev. 2.4，§5.2.30, 5.2.30.2.3，文件頁 456-459, 516-518，PDF 頁 482-485, 542-544 |
| `SEL` | Select，Get Features 用來選 current、default、saved 或 supported-capabilities view 的欄位。 | NVME-BASE-2.4 Rev. 2.4，§5.2.12, 5.2.30.2.3，文件頁 209-212, 518-519，PDF 頁 235-238, 544-545 |

## Visual Atlas：先用圖建立整體位置

每張教學重畫回答不同問題：Architecture 定位元件、Sequence 顯示 ownership、Decode 把 bits 轉成工程值、State 保留 failure evidence；它們不是 Spec 原圖的複製。

### Visual 01: 先分清三個 boundary：operation、memory ownership、encoded address

**View type:** `architecture`

```text
[Identify capability]
  ├─ [選 engineering track]
  ├─ [提交 command／配置 memory]
  ├─ [controller 進入新狀態]
  ├─ [CQE／log／memory fence]
  └─ [Debug 第一個斷點]
```

**回答的問題：** 這組章節不是同一個 feature。Device Self-test 管背景 diagnostic operation；HMB 管 host memory 的 ownership transfer；DSTRD 與 vendor command format 管 encoded value 如何轉成安全的 memory access。共同方法是先找 capability gate，再找狀態或 ownership 轉換，最後找可觀測證據。

**支援 Figure：** Figure 36, Figure 94, Figure 176, Figure 545

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 201，PDF 頁 227; NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3, 8.2.4，文件頁 515-516, 744，PDF 頁 541-542, 770; NVME-BASE-2.4 Rev. 2.4，§3.1.4.1, 8.2.3，文件頁 56, 744，PDF 頁 82, 770; NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.29，文件頁 356, 374, 733，PDF 頁 382, 400, 759

### Visual 02: Device Self-test：先 gate capability，再提交一個背景 operation

**View type:** `state`

```text
[OACS.DSTS=1] → [讀 SDSO／EDSTT] → [選 NSID + STC] → [提交 Admin SQE] → [CQE: start accepted] → [輪詢 LID 06h]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**回答的問題：** Self-test 不是同步 diagnostic RPC。Host 先用 OACS.DSTS、DSTO.SDSO 與 EDSTT 決定支援、concurrency scope 與時間預期，再用 NSID 與 STC 建構 command。Admin CQE 回來時，背景 operation 才剛進入可由 LID 06h 觀察的生命週期。

**支援 Figure：** Figure 93, Figure 176, Figure 177, Figure 178, Figure 179, Figure 180, Figure 338

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.8，文件頁 352-358, 614，PDF 頁 378-384, 640; NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 199，PDF 頁 225; NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 199-200，PDF 頁 225-226; NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 200，PDF 頁 226; NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 201，PDF 頁 227

### Visual 03: LID 06h：把 current operation 與 20 筆 history 分開解碼

**View type:** `decode`

```text
[RAW: Get LID06 564 bytes] → [LOCATE: 讀 DSTOS／DSTCS] → [DECODE: 選 RDS1 newest]
[VALIDATE: 解 DSTC／DSTR] → [APPLY: 依 VDINFO gate fields] → [EVIDENCE: NVM FLBA + timeline]
VALIDATE fail ──→ return to RAW evidence
```

**回答的問題：** log header 的 DSTOS／DSTCS 回答『現在跑到哪裡』；RDS1～RDS20 回答『之前怎麼結束』。result entry 又分成 operation code、result reason、segment、validity bitmap 與 diagnostic payload。NVM Command Set 只在 FVLD=1 時賦予 FLBA 明確的 LBA 語意。

**支援 Figure：** Figure 203, Figure 204, Figure 205, Figure 206, Figure 207, Figure 208, Figure 209, Figure 218, Figure 219, Figure 111, Figure 700, Figure 701

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.13，文件頁 213-216，PDF 頁 239-242; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 229-230，PDF 頁 255-256; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 229-230，PDF 頁 255-256; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 231，PDF 頁 257; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 231-232，PDF 頁 257-258; NVME-NVM-CS-1.3 Rev. 1.3，§4.1.4.3，文件頁 76，PDF 頁 76; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7, 8.1.8，文件頁 229-232, 614-616，PDF 頁 255-258, 640-642

### Visual 04: HMB：enable／disable completion 是 ownership fence

**View type:** `state`

```text
[讀 HMPRE/HMMIN/limits] → [配置 pages + HMDL] → [Set FID0Dh EHM=1] → [controller exclusive use] → [Set EHM=0] → [disable CQE→host reclaim]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**回答的問題：** HMB 的 value 不在『給 controller 一塊 cache』這句話，而在 ownership protocol。Host 配置 pages 與 descriptor list，enable 成功後停止寫入；controller 使用並初始化；host 要回收時先 disable，直到 CQE posted 才重新取得修改權。

**支援 Figure：** Figure 338, Figure 545, Figure 552, Figure 553

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.2.4，文件頁 357, 362, 744，PDF 頁 383, 388, 770; NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3, 8.2.4，文件頁 515-516, 744，PDF 頁 541-542, 770; NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3，文件頁 515-516，PDF 頁 541-542; NVME-BASE-2.4 Rev. 2.4，§8.2.4，文件頁 744，PDF 頁 770

### Visual 05: HMB command 與 descriptor：所有 size、count、address 都要對同一份 page math

**View type:** `decode`

```text
[RAW: CC.MPS→page bytes] → [LOCATE: HMPRE/HMMIN→target bytes] → [DECODE: 切成 aligned ranges]
[VALIDATE: 寫 16-byte entries] → [APPLY: sum(BSIZE)=HSIZE] → [EVIDENCE: 組 CDW11..15]
VALIDATE fail ──→ return to RAW evidence
```

**回答的問題：** HSIZE、BSIZE 與 BADD 都依 CC.MPS；HMPRE／HMMIN／HMMINDS 則依 4 KiB units。兩套 unit 不能混用。HMDL 本身要 16-byte aligned，entries 固定 16 bytes；HMDLEC 是 entry count，不是 0's-based，也不是 byte length。

**支援 Figure：** Figure 197, Figure 198, Figure 200, Figure 463, Figure 464, Figure 466, Figure 545, Figure 546, Figure 547, Figure 548, Figure 549, Figure 550, Figure 551, Figure 552, Figure 553

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.30, 5.2.30.2.3，文件頁 456-459, 516-518，PDF 頁 482-485, 542-544; NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3，文件頁 517-518，PDF 頁 543-544; NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3，文件頁 516-518，PDF 頁 542-544; NVME-BASE-2.4 Rev. 2.4，§5.2.12, 5.2.30.2.3，文件頁 209-212, 518-519，PDF 頁 235-238, 544-545

### Visual 06: HMB 跨 non-operational state、RTD3 與 reset 的三種不同邊界

**View type:** `state`

```text
[HMB enabled] → [optional HMNARE policy] → [non-op→HMNAR state] → [disable before RTD3/reset] → [preserve or replace contents] → [MR=1 exact-match return]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**回答的問題：** HMNARE 是 access policy，HMNAR 是此刻 state；MR 則描述 reset／RTD3 後是否歸還完全相同的舊內容。這三者不能互換。Controller Level Reset 會讓 controller 丟失 HMB assignment，RTD3 前應先 release，而 non-operational restriction 只限制特定 state 下的 access。

**支援 Figure：** Figure 338, Figure 545, Figure 552, Figure 553

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3，文件頁 516-519，PDF 頁 542-545; NVME-BASE-2.4 Rev. 2.4，§8.2.4，文件頁 744，PDF 頁 770; NVME-BASE-2.4 Rev. 2.4，§8.2.4，文件頁 744，PDF 頁 770

### Visual 07: DSTRD 與 NDT／NDM：encoded value 必須先轉成 byte boundary

**View type:** `decode`

```text
[RAW: 讀 capability bit／field] → [LOCATE: 選正確公式] → [DECODE: 轉成 byte stride／length]
[VALIDATE: 檢查 overflow／alignment] → [APPLY: 執行 MMIO／DMA] → [EVIDENCE: 保存 raw+decoded trace]
VALIDATE fail ──→ return to RAW evidence
```

**回答的問題：** software emulator 與 vendor command passthrough 都在處理 untrusted encoded values。DSTRD 要套 2^(2+x) 才是 bytes；NDT／NDM 已是實際 dword count，要乘 4、不能再加 1。正確公式不同，但目的相同：在 MMIO 或 DMA 前先證明 address 與 length。

**支援 Figure：** Figure 36, Figure 93, Figure 94, Figure 338

**來源：** NVME-BASE-2.4 Rev. 2.4，§3.1.4.1, 8.2.3，文件頁 56, 744，PDF 頁 82, 770; NVME-BASE-2.4 Rev. 2.4，§8.2.3，文件頁 744，PDF 頁 770; NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.29，文件頁 356, 374, 733，PDF 頁 382, 400, 759; NVME-BASE-2.4 Rev. 2.4，§4.1.1, 8.1.29，文件頁 143, 733，PDF 頁 169, 759; NVME-BASE-2.4 Rev. 2.4，§4.1.1, 8.1.29，文件頁 143, 733，PDF 頁 169, 759; NVME-BASE-2.4 Rev. 2.4，§5.2.6, 5.2.30.2.3, 8.1.29, 8.2.3，文件頁 199-201, 515-519, 733, 744，PDF 頁 225-227, 541-545, 759, 770

## Mental Model 與完整教學流程

以下依工程因果而非 Spec section 排列；相關 Figure 會回到它支援的流程節點，不以編號順序取代教學故事線。

### Module 01: 先分清三個 boundary：operation、memory ownership、encoded address

**解釋。** 這組章節不是同一個 feature。Device Self-test 管背景 diagnostic operation；HMB 管 host memory 的 ownership transfer；DSTRD 與 vendor command format 管 encoded value 如何轉成安全的 memory access。共同方法是先找 capability gate，再找狀態或 ownership 轉換，最後找可觀測證據。

```text
Identify capability
  ↓
選 engineering track
  ↓
提交 command／配置 memory
  ↓
controller 進入新狀態
  ↓
CQE／log／memory fence
  ↓
Debug 第一個斷點
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Self-test | operation lifecycle | CQE + LID 06h |
| HMB | exclusive ownership lifecycle | Get FID 0Dh + disable CQE |
| Doorbell emulation | encoded byte stride | MMIO address/write trace |
| Vendor command | buffer-length contract | VSCF/SNVSCF + NDT/NDM |

**說明性範例。** 同樣看到 Successful Completion，self-test 只代表 operation 已開始，HMB disable 則代表 ownership 已回到 host。status code 相同，不代表 completion boundary 相同。

**常見誤解／Debug。** 不要把所有內容都寫成『command 成功／失敗』。先標明成功代表哪個 state transition、哪一方此刻擁有 memory，以及還需要哪一個 log 或 Get Features 才能證明後續結果。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 201，PDF 頁 227; NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3, 8.2.4，文件頁 515-516, 744，PDF 頁 541-542, 770; NVME-BASE-2.4 Rev. 2.4，§3.1.4.1, 8.2.3，文件頁 56, 744，PDF 頁 82, 770; NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.29，文件頁 356, 374, 733，PDF 頁 382, 400, 759

**關聯 Figure：** Figure 36, Figure 94, Figure 176, Figure 545

### Module 02: Device Self-test：先 gate capability，再提交一個背景 operation

**解釋。** Self-test 不是同步 diagnostic RPC。Host 先用 OACS.DSTS、DSTO.SDSO 與 EDSTT 決定支援、concurrency scope 與時間預期，再用 NSID 與 STC 建構 command。Admin CQE 回來時，背景 operation 才剛進入可由 LID 06h 觀察的生命週期。

```text
OACS.DSTS=1
  ↓
讀 SDSO／EDSTT
  ↓
選 NSID + STC
  ↓
提交 Admin SQE
  ↓
CQE: start accepted
  ↓
輪詢 LID 06h
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| NSID=0 | 只包含 controller | 不測 namespace media |
| active NSID | 指定 namespace | invalid 與 inactive status 不同 |
| NSID=FFFFFFFFh | 所有 attached／accessible namespaces | 集合以 start 時點為準 |
| STC=Fh | abort current operation | 成功不代表曾有 operation |

**說明性範例。** 啟動 namespace 5 的 short test：NSID=00000005h、STC=1h，因此 CDW10=00000001h、CDW15=0。若立刻再送 extended STC=2h，應預期 command-specific status 1Dh，而不是建立第二個 operation。

**常見誤解／Debug。** 最常見的錯誤是把 CQE timestamp 當完成時間，或在 SDSO=1 時只看單一 controller 的 local state。trace 至少保存 controller ID、NSID、STC、CDW15、CQE status 與後續第一筆 LID 06h。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.8，文件頁 352-358, 614，PDF 頁 378-384, 640; NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 199，PDF 頁 225; NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 199-200，PDF 頁 225-226; NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 200，PDF 頁 226; NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 201，PDF 頁 227

**關聯 Figure：** Figure 93, Figure 176, Figure 177, Figure 178, Figure 179, Figure 180, Figure 338

### Module 03: LID 06h：把 current operation 與 20 筆 history 分開解碼

**解釋。** log header 的 DSTOS／DSTCS 回答『現在跑到哪裡』；RDS1～RDS20 回答『之前怎麼結束』。result entry 又分成 operation code、result reason、segment、validity bitmap 與 diagnostic payload。NVM Command Set 只在 FVLD=1 時賦予 FLBA 明確的 LBA 語意。

```text
Get LID06 564 bytes
  ↓
讀 DSTOS／DSTCS
  ↓
選 RDS1 newest
  ↓
解 DSTC／DSTR
  ↓
依 VDINFO gate fields
  ↓
NVM FLBA + timeline
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| DSTOS/DSTCS | current state/progress | DSTOS=0 時忽略 percentage |
| DSTR=7h + SEGN | 已知第一個 failed segment | 其他 DSTR 忽略 SEGN |
| FVLD + FLBA | 其中一個 failing LBA | 不是所有失敗 LBA 清單 |
| POH + STCT/STC | failure context | 仍需 validity bits |

**說明性範例。** 完整 log 是 564 bytes=141 dwords，因此 NUMD=140=008Ch。LSP=0、RAE=0 時 CDW10=008C0006h。若 RDS1.DSTS=17h，high nibble 1h 表示 short test，low nibble 7h 表示已知 failed segment；此時才讀 SEGN。

**常見誤解／Debug。** parser 不得以 FLBA 非零就宣告 media failure。先檢查 DSTR、再檢查 FVLD 與 NSIDVLD，最後依 NVM Command Set 解 bytes 23:16；同時保存 raw 28-byte result，避免 validity 判斷錯後失去原始證據。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.13，文件頁 213-216，PDF 頁 239-242; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 229-230，PDF 頁 255-256; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 229-230，PDF 頁 255-256; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 231，PDF 頁 257; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 231-232，PDF 頁 257-258; NVME-NVM-CS-1.3 Rev. 1.3，§4.1.4.3，文件頁 76，PDF 頁 76; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7, 8.1.8，文件頁 229-232, 614-616，PDF 頁 255-258, 640-642

**關聯 Figure：** Figure 203, Figure 204, Figure 205, Figure 206, Figure 207, Figure 208, Figure 209, Figure 218, Figure 219, Figure 111, Figure 700, Figure 701

### Module 04: HMB：enable／disable completion 是 ownership fence

**解釋。** HMB 的 value 不在『給 controller 一塊 cache』這句話，而在 ownership protocol。Host 配置 pages 與 descriptor list，enable 成功後停止寫入；controller 使用並初始化；host 要回收時先 disable，直到 CQE posted 才重新取得修改權。

```text
讀 HMPRE/HMMIN/limits
  ↓
配置 pages + HMDL
  ↓
Set FID0Dh EHM=1
  ↓
controller exclusive use
  ↓
Set EHM=0
  ↓
disable CQE→host reclaim
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Before enable | host owns and initializes descriptors | validate alignment/count |
| After enable CQE | controller exclusive use | host shall not write |
| Disable in flight | controller may still retrieve data | host still waits |
| After disable CQE | host may modify/reclaim | record fence timestamp |

**說明性範例。** 如果 driver 在送出 EHM=0 後、CQE 到達前就解除 DMA mapping，controller 仍可能依規格取回必要資料；這是 use-after-unmap。正確 fence 是 disable completion，而不是 SQ tail doorbell write。

**常見誤解／Debug。** 把 enable CQE 當作『host 仍可讀寫、controller 只是偶爾使用』會造成 data race。測試應對 HMDL 與每段 pages 建立 write-protection／DMA ownership trace，並在 disable CQE 後才解除。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.2.4，文件頁 357, 362, 744，PDF 頁 383, 388, 770; NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3, 8.2.4，文件頁 515-516, 744，PDF 頁 541-542, 770; NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3，文件頁 515-516，PDF 頁 541-542; NVME-BASE-2.4 Rev. 2.4，§8.2.4，文件頁 744，PDF 頁 770

**關聯 Figure：** Figure 338, Figure 545, Figure 552, Figure 553

### Module 05: HMB command 與 descriptor：所有 size、count、address 都要對同一份 page math

**解釋。** HSIZE、BSIZE 與 BADD 都依 CC.MPS；HMPRE／HMMIN／HMMINDS 則依 4 KiB units。兩套 unit 不能混用。HMDL 本身要 16-byte aligned，entries 固定 16 bytes；HMDLEC 是 entry count，不是 0's-based，也不是 byte length。

```text
CC.MPS→page bytes
  ↓
HMPRE/HMMIN→target bytes
  ↓
切成 aligned ranges
  ↓
寫 16-byte entries
  ↓
sum(BSIZE)=HSIZE
  ↓
組 CDW11..15
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| HMPRE/HMMIN | 4 KiB units | capability request |
| HSIZE/BSIZE | CC.MPS units | configured memory |
| HMDL address | 16-byte aligned | CDW13 low + CDW14 high |
| BADD | CC.MPS aligned | BSIZE=0 entry ignored |

**說明性範例。** CC.MPS=0、HSIZE=64 時是 256 KiB。HMDL=00000012_34567000h、HMDLEC=2，故 CDW13=34567000h、CDW14=00000012h、CDW15=2。兩個 BSIZE=32 的 ranges 各 128 KiB，合計 256 KiB。

**常見誤解／Debug。** 常見錯誤是把 HMPRE 直接填進 HSIZE，而裝置使用 8 KiB CC.MPS；或 HMDLEC=2 卻只 map 一個 16-byte entry。driver 應同時 log capability units、CC.MPS、每個 BADD/BSIZE、sum pages 與 command dwords。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.30, 5.2.30.2.3，文件頁 456-459, 516-518，PDF 頁 482-485, 542-544; NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3，文件頁 517-518，PDF 頁 543-544; NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3，文件頁 516-518，PDF 頁 542-544; NVME-BASE-2.4 Rev. 2.4，§5.2.12, 5.2.30.2.3，文件頁 209-212, 518-519，PDF 頁 235-238, 544-545

**關聯 Figure：** Figure 197, Figure 198, Figure 200, Figure 463, Figure 464, Figure 466, Figure 545, Figure 546, Figure 547, Figure 548, Figure 549, Figure 550, Figure 551, Figure 552, Figure 553

### Module 06: HMB 跨 non-operational state、RTD3 與 reset 的三種不同邊界

**解釋。** HMNARE 是 access policy，HMNAR 是此刻 state；MR 則描述 reset／RTD3 後是否歸還完全相同的舊內容。這三者不能互換。Controller Level Reset 會讓 controller 丟失 HMB assignment，RTD3 前應先 release，而 non-operational restriction 只限制特定 state 下的 access。

```text
HMB enabled
  ↓
optional HMNARE policy
  ↓
non-op→HMNAR state
  ↓
disable before RTD3/reset
  ↓
preserve or replace contents
  ↓
MR=1 exact-match return
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| HMNARE | configured policy | 需要 CTRATT.HMBR |
| HMNAR | current restriction state | 可能因 operational state 而為 0 |
| MR=1 | return identical old HMB | size/address/list/content 全相同 |
| MR=0 | new undefined contents | controller 重新初始化 |

**說明性範例。** resume 後 allocator 給了相同 pages 但 HMDL 搬到新 address，就不能設 MR=1，因為 descriptor-list address 也必須完全相同。此時以 MR=0 當新 allocation 重新 enable。

**常見誤解／Debug。** 不要只 hash data pages；MR validation 還要比較 HSIZE、HMDL address、HMDLEC、每個 descriptor 與全部 HMB contents。另把 NOPPME 當成 HMNARE 開關也是錯誤，規格明確說兩者無影響。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.30.2.3，文件頁 516-519，PDF 頁 542-545; NVME-BASE-2.4 Rev. 2.4，§8.2.4，文件頁 744，PDF 頁 770; NVME-BASE-2.4 Rev. 2.4，§8.2.4，文件頁 744，PDF 頁 770

**關聯 Figure：** Figure 338, Figure 545, Figure 552, Figure 553

### Module 07: DSTRD 與 NDT／NDM：encoded value 必須先轉成 byte boundary

**解釋。** software emulator 與 vendor command passthrough 都在處理 untrusted encoded values。DSTRD 要套 2^(2+x) 才是 bytes；NDT／NDM 已是實際 dword count，要乘 4、不能再加 1。正確公式不同，但目的相同：在 MMIO 或 DMA 前先證明 address 與 length。

```text
讀 capability bit／field
  ↓
選正確公式
  ↓
轉成 byte stride／length
  ↓
檢查 overflow／alignment
  ↓
執行 MMIO／DMA
  ↓
保存 raw+decoded trace
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| DSTRD | 2^(2+x) bytes | 0→4 B；4→64 B |
| NDT | value×4 data bytes | 不是 0's-based |
| NDM | value×4 metadata bytes | 獨立 buffer bound |
| VSCF/SNVSCF | format gate | Admin 與 I/O 分開 |

**說明性範例。** emulator 設 DSTRD=4 得 64-byte stride，可讓每個 doorbell 使用離散 cacheline。vendor command 的 NDT=0100h 則是 256 dwords=1024 bytes，不是 1028 bytes。兩者都要同時保存 raw encoded value 與 decoded bytes。

**常見誤解／Debug。** 同一套 helper 若把所有 NVMe length 都當 0's-based，NDT／NDM 會多配置或多傳 4 bytes；若把 DSTRD 直接乘 4，又會在 DSTRD>0 時算錯。每個欄位的公式必須跟 Figure source 綁定。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§3.1.4.1, 8.2.3，文件頁 56, 744，PDF 頁 82, 770; NVME-BASE-2.4 Rev. 2.4，§8.2.3，文件頁 744，PDF 頁 770; NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.29，文件頁 356, 374, 733，PDF 頁 382, 400, 759; NVME-BASE-2.4 Rev. 2.4，§4.1.1, 8.1.29，文件頁 143, 733，PDF 頁 169, 759; NVME-BASE-2.4 Rev. 2.4，§4.1.1, 8.1.29，文件頁 143, 733，PDF 頁 169, 759; NVME-BASE-2.4 Rev. 2.4，§5.2.6, 5.2.30.2.3, 8.1.29, 8.2.3，文件頁 199-201, 515-519, 733, 744，PDF 頁 225-227, 541-545, 759, 770

**關聯 Figure：** Figure 36, Figure 93, Figure 94, Figure 338

## 可追溯的規格重點

前面的 Mental Model 解釋因果；本節保留每個可追溯結論與 normative 強度，供講者備註與審查。

### 1. 先確認 self-test capability 與 concurrency scope

<!-- claim:BASEDIAGMEM-SELFTEST-GATE -->

啟動 Device Self-test 前，先讀 Identify Controller：OACS.DSTS 判斷 command 是否支援；EDSTT 是 extended operation 在 power state 0 的名目分鐘數；DSTO.SDSO 決定同時只能有一個 subsystem-wide operation，或每個 controller 各一個。這三個欄位回答不同問題。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, 文件頁 352-358, 614, PDF 頁 378-384, 640

### 2. NSID 決定測試涵蓋範圍

<!-- claim:BASEDIAGMEM-SELFTEST-NSID -->

Device Self-test 由收到 command 的 controller 執行。NSID=00000000h 只測 controller；00000001h～FFFFFFFEh 指定一個 namespace；FFFFFFFFh 包含提交當下可由該 controller 存取的所有 attached namespaces。invalid 與 inactive NSID 會得到不同 status。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 199, PDF 頁 225

### 3. STC 與 CDW15 的命令編碼

<!-- claim:BASEDIAGMEM-SELFTEST-STC -->

CDW10.STC[3:0] 選動作：1h=short、2h=extended、3h=Host-Initiated Refresh、Eh=vendor specific、Fh=abort；其餘 encoding reserved。只有 STC=Eh 時 CDW15.DSTP 才是 vendor specific，其他情況 CDW15 reserved。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 199-200, PDF 頁 225-226

### 4. 已有 operation 時的狀態矩陣

<!-- claim:BASEDIAGMEM-SELFTEST-INPROGRESS -->

已有 operation 時，再送 short、extended 或 Host-Initiated Refresh 必須以 Device Self-test in Progress 中止；vendor-specific 新命令的行為仍是 vendor specific。STC=Fh 則依序中止目前 operation、建立最新 result、清除 current status，最後成功完成 command。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 200, PDF 頁 226

### 5. CQE 不等於測試完成

<!-- claim:BASEDIAGMEM-SELFTEST-COMPLETION -->

Device Self-test command 的 Admin CQE 只證明『啟動／中止動作已被處理』，不是背景測試已完成。command-specific status 1Dh 表示已有 operation in progress；software 必須把 CQE 與後續 LID 06h 分開記錄。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 201, PDF 頁 227

### 6. 背景測試的 suspend／resume 契約

<!-- claim:BASEDIAGMEM-SELFTEST-BACKGROUND -->

Device Self-test 是由 vendor-specific segments 組成的背景工作。若另一個 command 必須暫停測試才能處理，controller 必須（shall）依序 suspend self-test、處理並完成該 command、再 resume self-test；同時可處理哪些 command 則由 vendor 決定。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.8, 文件頁 614, PDF 頁 640

### 7. short 與 extended 的 reset 差異

<!-- claim:BASEDIAGMEM-SELFTEST-TIMING -->

short operation 應（should）在兩分鐘內完成，且 Controller Level Reset 會中止；extended operation 應在 EDSTT 內完成，必須跨 Controller Level Reset 與 power restoration 持續並於之後 resume。兩者不能共用同一套 reset 預期。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, 文件頁 615-616, PDF 頁 641-642

### 8. Format、sanitize 與 abort 條件

<!-- claim:BASEDIAGMEM-SELFTEST-ABORTS -->

short 與 extended 都會被適用的 Format NVM、sanitize start 或 STC=Fh 中止，namespace 從 inventory 移除時則可能（may）中止。Figure 701 顯示 Format 的 NSID 與 secure-erase 選項會改變是否必須中止，不能只看 opcode。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, 文件頁 615-616, PDF 頁 641-642

### 9. 564-byte LID 06h command 計算

<!-- claim:BASEDIAGMEM-SELFTEST-LOG-COMMAND -->

讀取 LID 06h 所需的最小 Get Log Page slice 是：LID=06h、LSP=0、RAE 依事件策略選擇、NUMD 表示 564 bytes、LPOL/LPOU=0、OT=0、CSI=0、UIDX=0。564 bytes=141 dwords，因此 0's-based NUMD=140=008Ch；RAE=0 時 CDW10=008C0006h。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, 文件頁 213-216, PDF 頁 239-242

### 10. current operation 與完成百分比

<!-- claim:BASEDIAGMEM-SELFTEST-CURRENT -->

LID 06h 的 byte 0 以 DSTOS 表示目前 operation，byte 1 的 DSTCS[6:0] 是完成百分比；DSTOS=0 時 host 應忽略 DSTCS。controller 在 operation 完成或被中止時，必須先建立 result entry，之後才能把 in-progress status 清為 0。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-230, PDF 頁 255-256

### 11. 20 筆 newest-first result ring

<!-- claim:BASEDIAGMEM-SELFTEST-HISTORY -->

LID 06h 保留 20 筆、每筆 28 bytes 的結果，RDS1 永遠是最新完成或中止的 operation。未使用 entry 必須讓 DSTR=Fh 且 DSTC=0h，其他欄位由 host 忽略；不能把全零以外的殘值當成歷史結果。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-230, PDF 頁 255-256

### 12. DSTS 與 SEGN 的條件式解碼

<!-- claim:BASEDIAGMEM-SELFTEST-RESULT -->

每筆 DSTS 的高 nibble DSTC 表示原始 self-test code，低 nibble DSTR 表示完成／中止原因。只有 DSTR=7h 時 SEGN 才指出第一個失敗 segment；其他 DSTR 下 SEGN 應忽略。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 231, PDF 頁 257

### 13. VDINFO 是四個獨立 validity gates

<!-- claim:BASEDIAGMEM-SELFTEST-VALIDITY -->

VDINFO 的 NSIDVLD、FVLD、SCTVLD、SCVLD 是四個獨立 validity gates。NSID、FLBA、STCT、STC 只有在對應 bit=1 時才可解讀；先驗證 validity，再讀數值，不能用非零值猜測有效。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 231-232, PDF 頁 257-258

### 14. NVM Command Set 補完 FLBA 語意

<!-- claim:BASEDIAGMEM-SELFTEST-NVM-FLBA -->

Base 將 Figure 219 的 FLBA 留給 I/O Command Set 定義。NVM Command Set 1.3 規定 bytes 23:16 是造成失敗的 logical block address；若有多個失敗 logical blocks，只回其中一個，且僅 FVLD=1 時有效。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, 文件頁 76, PDF 頁 76

### 15. 以三個時間點重建 self-test

<!-- claim:BASEDIAGMEM-SELFTEST-DEBUG -->

Debug 時把 command、current state 與歷史 result 分成三個時間點：保存 STC／NSID／CQE；輪詢 DSTOS／DSTCS；完成後保存 DSTS、SEGN、VDINFO、POH、NSID、FLBA、STCT、STC 與 vendor bytes。這樣才能分辨 command rejection、operation abort 與 media failure。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 8.1.8, 文件頁 229-232, 614-616, PDF 頁 255-258, 640-642

### 16. HMB capability 與 descriptor limits

<!-- claim:BASEDIAGMEM-HMB-CAPABILITY -->

HMPRE=0 表示 HMB 不支援；非零時以 4 KiB units 表示 preferred size，HMMIN 表示 minimum request。HMMINDS 與 HMMAXD 是 descriptor 限制。即使 host 無法提供 HMB，controller 仍必須（shall）正常運作。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.2.4, 文件頁 357, 362, 744, PDF 頁 383, 388, 770

### 17. HMB 是 ownership transfer

<!-- claim:BASEDIAGMEM-HMB-OWNERSHIP -->

HMB 是 host 配置、controller 專用的記憶體租約。Set Features enable 成功後，host 必須（shall）停止寫入 descriptor list 與所有描述的 memory ranges，直到 disable command 完成；這是 ownership transfer，不只是 performance hint。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 8.2.4, 文件頁 515-516, 744, PDF 頁 541-542, 770

### 18. FID 0Dh 的 Set Features layout

<!-- claim:BASEDIAGMEM-HMB-SET-COMMAND -->

Set Features 使用 FID=0Dh；CDW11 放 EHM、MR、HMNARE，CDW12 放 HSIZE，CDW13／14 組成 64-bit HMDL address，CDW15 是 HMDLEC。HMDL address 必須 16-byte aligned；HMDLEC=0 必須回 Invalid Field in Command。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, 5.2.30.2.3, 文件頁 456-459, 516-518, PDF 頁 482-485, 542-544

### 19. HMDL 與 descriptor page math

<!-- claim:BASEDIAGMEM-HMB-DESCRIPTORS -->

HMDL 是連續的 16-byte descriptor array；每個 entry 的 BADD 必須依 CC.MPS memory page size 對齊，BSIZE 以相同 page units 表示連續長度。BSIZE=0 的 entry 由 controller 忽略；HSIZE 應與可用 descriptors 的 page 數相符。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 文件頁 517-518, PDF 頁 543-544

### 20. 256 KiB HMB 完整計算

<!-- claim:BASEDIAGMEM-HMB-NUMERIC -->

說明性範例：CC.MPS=0 代表 4 KiB page；HSIZE=64 代表 256 KiB。若 HMDL=00000012_34567000h、HMDLEC=2，CDW13=34567000h、CDW14=00000012h、CDW15=00000002h。兩個 descriptor 各 BSIZE=32 pages 時，合計正好 64 pages。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 文件頁 516-518, PDF 頁 542-544

### 21. enable／disable 的 completion fence

<!-- claim:BASEDIAGMEM-HMB-SEQUENCE -->

HMB 已 enable 時再次送 EHM=1 必須以 Command Sequence Error 中止；尚未 enable 時送 EHM=0 則成功但不做事。disable completion 前 controller 應取回所需資料；CQE 被 posted 後才表示 host 可安全修改或回收 buffer。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 文件頁 515-516, PDF 頁 541-542

### 22. Get Features 分開讀 policy 與 state

<!-- claim:BASEDIAGMEM-HMB-GET -->

Get Features 使用 FID=0Dh；SEL≠supported-capabilities 成功時，CQE.DW0 回 EHM、HMNARE、HMNAR，data buffer 回 4 KiB Attributes data structure，包括 HSIZE、HMDL address 與 HMDLEC。『已啟用』與『目前正在限制 access』是不同狀態。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, 5.2.30.2.3, 文件頁 209-212, 518-519, PDF 頁 235-238, 544-545

### 23. HMNARE 與 HMNAR 不相同

<!-- claim:BASEDIAGMEM-HMB-NONOP -->

HMNARE 只有 Identify.CTRATT.HMBR=1 時可啟用。HMNARE 是 policy，HMNAR 是 controller 此刻是否真的因 non-operational state 而被限制；Admin commands 與其啟動的 background operations 有明文例外。NOPPME 不改變這項 HMB restriction。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 文件頁 516-519, PDF 頁 542-545

### 24. reset／RTD3 後的 Memory Return

<!-- claim:BASEDIAGMEM-HMB-RESET-RTD3 -->

HMB 不會跨 Controller Level Reset 保存在 controller。reset 後 host 應重新提供資源；若 MR=1 表示歸還先前內容，size、descriptor-list address、descriptor-list contents 與 HMB contents 必須完全相同。RTD3 前宜先 disable，恢復後再依是否保留內容選 MR。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.2.4, 文件頁 744, PDF 頁 770

### 25. surprise removal 的資料正確性

<!-- claim:BASEDIAGMEM-HMB-SURPRISE -->

使用 HMB 時發生 surprise removal，controller 必須（shall）確保不造成 data loss 或 data corruption。這不代表 HMB 內容本身具有持久性，而是裝置不得把內部正確性依賴在 host 一定能先走正常 release 流程。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.2.4, 文件頁 744, PDF 頁 770

### 26. DSTRD encoding 到 cacheline stride

<!-- claim:BASEDIAGMEM-DOORBELL-STRIDE -->

CAP.DSTRD 的實際間距是 2^(2+DSTRD) bytes。DSTRD=0／2／4 分別得到 4／16／64 bytes；software emulation 可用 64-byte stride 把 doorbells 分散到 cacheline，硬體 NVMe interface 的 expected value 是 0h。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, 8.2.3, 文件頁 56, 744, PDF 頁 82, 770

### 27. emulator 的 doorbell 證據鏈

<!-- claim:BASEDIAGMEM-DOORBELL-DEBUG -->

emulator Debug 不只看 doorbell value，也要保存 CAP.DSTRD、計算後 byte stride、queue identifier、被監看的 cacheline 與 write timestamp。把 encoded DSTRD 直接當 bytes 會讓 queue notification 落到錯誤位址。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.2.3, 文件頁 744, PDF 頁 770

### 28. Admin 與 I/O vendor format 分開 gate

<!-- claim:BASEDIAGMEM-VENDOR-GATE -->

standard Vendor Specific command format 是 optional。AVSCC.VSCF 控制 vendor-specific Admin commands；ICSVSCC.SNVSCF 控制 vendor-specific I/O commands。兩個 capability 必須分開讀，不能因其中一個為 1 就假設另一類命令也使用 Figure 94。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.29, 文件頁 356, 374, 733, PDF 頁 382, 400, 759

### 29. Figure 94 的 boundary-safe layout

<!-- claim:BASEDIAGMEM-VENDOR-FORMAT -->

Figure 94 保留 common CDW0、NSID、metadata/data pointers 與 CDW12-CDW15，並把 CDW10／11 定義成 NDT／NDM。若 command 不使用 NSID，必須清為 0；invalid NSID 在使用時必須回 Invalid Namespace or Format，inactive NSID 行為仍是 vendor specific。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 8.1.29, 文件頁 143, 733, PDF 頁 169, 759

### 30. NDT／NDM 是實際 dword count

<!-- claim:BASEDIAGMEM-VENDOR-LENGTH -->

NDT 與 NDM 是實際 dword 數，不是 0's-based。NDT=00000100h 代表 256 dwords=1024 bytes；driver 可用 NDT／NDM 驗證 application buffer，避免 data 或 metadata transfer overflow。是否支援 standard format 仍先由 VSCF／SNVSCF gate。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 8.1.29, 文件頁 143, 733, PDF 頁 169, 759

### 31. 從第一個 broken boundary 開始 Debug

<!-- claim:BASEDIAGMEM-BOUNDARY-DEBUG -->

三條流程的共同 Debug 原則是找第一個 broken boundary：self-test 比對 command→current status→result；HMB 比對 capability→descriptor math→ownership→disable CQE；emulation／vendor command 比對 capability encoding→byte count／stride→實際 memory access。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 5.2.30.2.3, 8.1.29, 8.2.3, 文件頁 199-201, 515-519, 733, 744, PDF 頁 225-227, 541-545, 759, 770

## Figure 索引

本報告介紹全部 36 張納入範圍的 Figure。100 分鐘簡報以 section 主線與必講 Figure 為主，其餘 Figure 仍完整保留作為附錄。其中 17 張位於主章節範圍外，但因指定正文直接引用而納入相依教學。

- [§4.1](#section-4-1)

- [§5.2](#section-5-2)

- [§8.1](#section-8-1)

- [引用相依 Figure（位於主章節範圍外）](#section-dependency)

## Figure／欄位表教學參考

本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。欄位與 keyword 索引來自本機核對過的 PDF。

<a id="section-4-1"></a>

### §4.1

<details markdown="1">
<summary><strong>Figure 111: Self-test Results Data Structure</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-111-CLAIM figure-table:BASEDIAGMEM-FIG-111 -->

**SPEC。** Figure 111〈Self-test Results Data Structure〉：定義〈Self-test Results Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：FLBA, bytes 23:16, FVLD, one failed logical block。

#### 這張 Figure 在完整流程中的位置

Figure 111 位於 §4.1.4.3，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 FLBA 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: FLBA]
          ↓
[擷取欄位: bytes 23:16] → [套用編碼: FVLD]
                                      ↓
[驗證證據: one failed logical block]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `FLBA` | Failing LBA，NVM Command Set 定義為造成 self-test failure 的其中一個 logical block address。 |
| `bytes 23:16` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FVLD` | Failing LBA Valid，決定 FLBA 欄位是否可解讀的 validity bit。 |
| `one failed logical block` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.1.4.3。
2. 依圖中指定的寬度與位置解碼 FLBA；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 bytes 23:16 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §4.1.4.3 如何排列 FLBA、bytes 23:16 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.1.4.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 111 對應的 raw value 或 buffer，標出包含 FLBA 的 bytes 並解碼，再獨立核對 bytes 23:16。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 FLBA，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 FLBA 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 bytes 23:16 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** FLBA, bytes 23:16, FVLD, one failed logical block

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, Figure 111, 文件頁 76, PDF 頁 76

</details>

<a id="section-5-2"></a>

### §5.2

<details markdown="1">
<summary><strong>Figure 176: Device Self-test Namespace Test Action</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-176-CLAIM figure-table:BASEDIAGMEM-FIG-176 -->

**SPEC。** Figure 176〈Device Self-test Namespace Test Action〉：呈現〈Device Self-test Namespace Test Action〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NSID 00000000h, NSID 00000001h-FFFFFFFEh, NSID FFFFFFFFh。

#### 這張 Figure 在完整流程中的位置

Figure 176 位於 §5.2.6，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NSID 00000000h 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSID 00000000h]
          ↓
[擷取欄位: NSID 00000001h-FFFFFFFEh] → [套用編碼: NSID FFFFFFFFh]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSID 00000000h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NSID 00000001h-FFFFFFFEh` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NSID FFFFFFFFh` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.6。
2. 依圖中指定的寬度與位置解碼 NSID 00000000h；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NSID 00000001h-FFFFFFFEh 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 176 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.6 如何排列 NSID 00000000h、NSID 00000001h-FFFFFFFEh 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.6 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 176 對應的 raw value 或 buffer，標出包含 NSID 00000000h 的 bytes 並解碼，再獨立核對 NSID 00000001h-FFFFFFFEh。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NSID 00000000h，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NSID 00000000h 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NSID 00000001h-FFFFFFFEh 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NSID 00000000h, NSID 00000001h-FFFFFFFEh, NSID FFFFFFFFh

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 176, 文件頁 199, PDF 頁 225

</details>

<details markdown="1">
<summary><strong>Figure 177: Device Self-test - Command Dword 10</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-177-CLAIM figure-table:BASEDIAGMEM-FIG-177 -->

**SPEC。** Figure 177〈Device Self-test - Command Dword 10〉：定義 Device Self-test 在 CDW10 的 command-specific 欄位。 先定位 CDW10，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：STC 1h, STC 2h, STC 3h, STC Eh, STC Fh。

#### 這張 Figure 在完整流程中的位置

Figure 177 位於 §5.2.6，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 STC 1h 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: STC 1h]
          ↓
[擷取欄位: STC 2h] → [套用編碼: STC 3h]
                                      ↓
[驗證證據: STC Eh]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `STC 1h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `STC 2h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `STC 3h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `STC Eh` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `STC Fh` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.6。
2. 依圖中指定的寬度與位置解碼 STC 1h；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 STC 2h 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 177 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.6 如何排列 STC 1h、STC 2h 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.6 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 177 對應的 raw value 或 buffer，標出包含 STC 1h 的 bytes 並解碼，再獨立核對 STC 2h。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 STC 1h，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 STC 1h 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 STC 2h 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** STC 1h, STC 2h, STC 3h, STC Eh, STC Fh

**來源 keyword 索引：** `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 177, 文件頁 199, PDF 頁 225

</details>

<details markdown="1">
<summary><strong>Figure 178: Device Self-test - Command Dword 15</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-178-CLAIM figure-table:BASEDIAGMEM-FIG-178 -->

**SPEC。** Figure 178〈Device Self-test - Command Dword 15〉：定義 Device Self-test 在 CDW15 的 command-specific 欄位。 先定位 CDW15，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：DSTP。

#### 這張 Figure 在完整流程中的位置

Figure 178 位於 §5.2.6，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DSTP 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DSTP]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DSTP` | Device Self-test Parameter，只有 vendor-specific STC=Eh 時才有 vendor-defined 語意的 CDW15。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.6。
2. 依圖中指定的寬度與位置解碼 DSTP；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 178 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.6 如何排列 DSTP、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.6 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 178 對應的 raw value 或 buffer，標出包含 DSTP 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 DSTP，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 DSTP 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** DSTP

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 178, 文件頁 200, PDF 頁 226

</details>

<details markdown="1">
<summary><strong>Figure 179: Device Self-test - Command Processing</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-179-CLAIM figure-table:BASEDIAGMEM-FIG-179 -->

**SPEC。** Figure 179〈Device Self-test - Command Processing〉：呈現〈Device Self-test - Command Processing〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：self-test in progress, new STC, abort, result creation。

#### 這張 Figure 在完整流程中的位置

Figure 179 位於 §5.2.6，在本流程中是「queue」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 self-test in progress 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 queue／command flow 圖。先標 host 與 controller 的 ownership，再追 head、tail、phase 或 arbitration 的改變；箭頭代表狀態或 ownership 轉移，不自動代表 command 已完成。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: self-test in progress]
          ↓
[擷取欄位: new STC] → [套用編碼: abort]
                                      ↓
[驗證證據: result creation]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `self-test in progress` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `new STC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `abort` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `result creation` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.6。
2. 依圖中指定的寬度與位置解碼 self-test in progress；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 new STC 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 179 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.6 如何排列 self-test in progress、new STC 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.6 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 179 對應的 raw value 或 buffer，標出包含 self-test in progress 的 bytes 並解碼，再獨立核對 new STC。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 self-test in progress，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 self-test in progress 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 new STC 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** self-test in progress, new STC, abort, result creation

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 179, 文件頁 200, PDF 頁 226

</details>

<details markdown="1">
<summary><strong>Figure 180: Device Self-test - Command Specific Status Values</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-180-CLAIM figure-table:BASEDIAGMEM-FIG-180 -->

**SPEC。** Figure 180〈Device Self-test - Command Specific Status Values〉：定義〈Device Self-test - Command Specific Status Values〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Device Self-test in Progress, status 1Dh。

#### 這張 Figure 在完整流程中的位置

Figure 180 位於 §5.2.6，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Device Self-test in Progress 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Device Self-test in Progress]
          ↓
[擷取欄位: status 1Dh] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Device Self-test in Progress` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `status 1Dh` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.6。
2. 依圖中指定的寬度與位置解碼 Device Self-test in Progress；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 status 1Dh 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 180 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.6 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.6 如何排列 Device Self-test in Progress、status 1Dh 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.6 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 180 對應的 raw value 或 buffer，標出包含 Device Self-test in Progress 的 bytes 並解碼，再獨立核對 status 1Dh。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Device Self-test in Progress，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Device Self-test in Progress 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 status 1Dh 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Device Self-test in Progress, status 1Dh

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 180, 文件頁 201, PDF 頁 227

</details>

<details markdown="1">
<summary><strong>Figure 218: Device Self-test Log Page</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-218-CLAIM figure-table:BASEDIAGMEM-FIG-218 -->

**SPEC。** Figure 218〈Device Self-test Log Page〉：把〈Device Self-test Log Page〉連到 self-test、host memory、doorbell 或 vendor command 的工程邊界。 先辨認 capability 與 owner，再解碼 DSTOS, DSTCS, RDS1, RDS20, 564 bytes，最後以 completion、log 或 memory lifecycle 證據核對。

#### 這張 Figure 在完整流程中的位置

Figure 218 位於 §5.2.13.1.7，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DSTOS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DSTOS]
          ↓
[擷取欄位: DSTCS] → [套用編碼: RDS1]
                                      ↓
[驗證證據: RDS20]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DSTOS` | Device Self-test Operation Status，LID 06h 中表示目前 operation 類型的 nibble。 |
| `DSTCS` | Device Self-test Completion Status，LID 06h 中的 0 到 100 完成百分比。 |
| `RDS1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `RDS20` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `564 bytes` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.13.1.7。
2. 依圖中指定的寬度與位置解碼 DSTOS；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 DSTCS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 218 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13.1.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.13.1.7 如何排列 DSTOS、DSTCS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.13.1.7 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 218 對應的 raw value 或 buffer，標出包含 DSTOS 的 bytes 並解碼，再獨立核對 DSTCS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 DSTOS，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 DSTOS 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 DSTCS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** DSTOS, DSTCS, RDS1, RDS20, 564 bytes

**來源 keyword 索引：** `shall not`, `shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, Figure 218, 文件頁 230, PDF 頁 256

</details>

<details markdown="1">
<summary><strong>Figure 219: Self-test Result Data Structure</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-219-CLAIM figure-table:BASEDIAGMEM-FIG-219 -->

**SPEC。** Figure 219〈Self-test Result Data Structure〉：定義〈Self-test Result Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DSTC, DSTR, SEGN, VDINFO, POH, NSID, FLBA, STCT, STC, VS。

#### 這張 Figure 在完整流程中的位置

Figure 219 位於 §5.2.13.1.7，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DSTC 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DSTC]
          ↓
[擷取欄位: DSTR] → [套用編碼: SEGN]
                                      ↓
[驗證證據: VDINFO]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DSTC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `DSTR` | Device Self-test Result，結果 entry 中表示成功、abort 或 segment failure 的 nibble。 |
| `SEGN` | Segment Number，只有 DSTR=7h 時指出第一個失敗 diagnostic segment。 |
| `VDINFO` | Valid Diagnostic Information，分別 gate NSID、FLBA、SCT 與 SC 的 validity bitmap。 |
| `POH` | Power On Hours，self-test result 建立時累積的 power-on hours，不含指定 low-power 時間。 |
| `NSID` | Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.13.1.7。
2. 依圖中指定的寬度與位置解碼 DSTC；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 DSTR 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 219 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13.1.7 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.13.1.7 如何排列 DSTC、DSTR 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.13.1.7 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 219 對應的 raw value 或 buffer，標出包含 DSTC 的 bytes 並解碼，再獨立核對 DSTR。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 DSTC，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 DSTC 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 DSTR 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** DSTC, DSTR, SEGN, VDINFO, POH, NSID, FLBA, STCT, STC, VS

**來源 keyword 索引：** `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, Figure 219, 文件頁 231-232, PDF 頁 257-258

</details>

<details markdown="1">
<summary><strong>Figure 545: Host Memory Buffer - Command Dword 11</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-545-CLAIM figure-table:BASEDIAGMEM-FIG-545 -->

**SPEC。** Figure 545〈Host Memory Buffer - Command Dword 11〉：定義 Host Memory Buffer 在 CDW11 的 command-specific 欄位。 先定位 CDW11，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：CTZ, HMNARE, MR, EHM。

#### 這張 Figure 在完整流程中的位置

Figure 545 位於 §5.2.30.2.3，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CTZ 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CTZ]
          ↓
[擷取欄位: HMNARE] → [套用編碼: MR]
                                      ↓
[驗證證據: EHM]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CTZ` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `HMNARE` | Host Memory Non-operational Access Restriction Enable，配置 non-operational HMB access policy 的 bit。 |
| `MR` | Memory Return，表示 host 歸還完全相同的舊 HMB size、addresses、descriptors 與 contents。 |
| `EHM` | Enable Host Memory，啟用或停用 controller 使用 HMB 的 bit。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.2.3。
2. 依圖中指定的寬度與位置解碼 CTZ；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 HMNARE 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 545 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30.2.3 如何排列 CTZ、HMNARE 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.2.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 545 對應的 raw value 或 buffer，標出包含 CTZ 的 bytes 並解碼，再獨立核對 HMNARE。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CTZ，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CTZ 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 HMNARE 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CTZ, HMNARE, MR, EHM

**來源 keyword 索引：** `shall not`, `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 545, 文件頁 516-517, PDF 頁 542-543

</details>

<details markdown="1">
<summary><strong>Figure 546: Host Memory Buffer - Command Dword 12</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-546-CLAIM figure-table:BASEDIAGMEM-FIG-546 -->

**SPEC。** Figure 546〈Host Memory Buffer - Command Dword 12〉：定義 Host Memory Buffer 在 CDW12 的 command-specific 欄位。 先定位 CDW12，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：HSIZE, CC.MPS units。

#### 這張 Figure 在完整流程中的位置

Figure 546 位於 §5.2.30.2.3，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 HSIZE 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: HSIZE]
          ↓
[擷取欄位: CC.MPS units] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `HSIZE` | Host Memory Buffer Size，以 CC.MPS memory-page units 表示的 HMB 總大小。 |
| `CC.MPS units` | Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.MPS units 進一步指定其中的 MPS units 子欄位。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.2.3。
2. 依圖中指定的寬度與位置解碼 HSIZE；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CC.MPS units 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 546 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30.2.3 如何排列 HSIZE、CC.MPS units 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.2.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 546 對應的 raw value 或 buffer，標出包含 HSIZE 的 bytes 並解碼，再獨立核對 CC.MPS units。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 HSIZE，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 HSIZE 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CC.MPS units 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** HSIZE, CC.MPS units

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 546, 文件頁 517, PDF 頁 543

</details>

<details markdown="1">
<summary><strong>Figure 547: Host Memory Buffer - Command Dword 13</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-547-CLAIM figure-table:BASEDIAGMEM-FIG-547 -->

**SPEC。** Figure 547〈Host Memory Buffer - Command Dword 13〉：定義 Host Memory Buffer 在 CDW13 的 command-specific 欄位。 先定位 CDW13，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：HMDLLA, 16-byte alignment。

#### 這張 Figure 在完整流程中的位置

Figure 547 位於 §5.2.30.2.3，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 HMDLLA 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: HMDLLA]
          ↓
[擷取欄位: 16-byte alignment] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `HMDLLA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `16-byte alignment` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.2.3。
2. 依圖中指定的寬度與位置解碼 HMDLLA；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 16-byte alignment 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 547 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30.2.3 如何排列 HMDLLA、16-byte alignment 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.2.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 547 對應的 raw value 或 buffer，標出包含 HMDLLA 的 bytes 並解碼，再獨立核對 16-byte alignment。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 HMDLLA，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 HMDLLA 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 16-byte alignment 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** HMDLLA, 16-byte alignment

**來源 keyword 索引：** `shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 547, 文件頁 517, PDF 頁 543

</details>

<details markdown="1">
<summary><strong>Figure 548: Host Memory Buffer - Command Dword 14</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-548-CLAIM figure-table:BASEDIAGMEM-FIG-548 -->

**SPEC。** Figure 548〈Host Memory Buffer - Command Dword 14〉：定義 Host Memory Buffer 在 CDW14 的 command-specific 欄位。 先定位 CDW14，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：HMDLUA。

#### 這張 Figure 在完整流程中的位置

Figure 548 位於 §5.2.30.2.3，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 HMDLUA 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: HMDLUA]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `HMDLUA` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.2.3。
2. 依圖中指定的寬度與位置解碼 HMDLUA；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 548 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30.2.3 如何排列 HMDLUA、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.2.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 548 對應的 raw value 或 buffer，標出包含 HMDLUA 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 HMDLUA，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 HMDLUA 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** HMDLUA

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 548, 文件頁 517, PDF 頁 543

</details>

<details markdown="1">
<summary><strong>Figure 549: Host Memory Buffer - Command Dword 15</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-549-CLAIM figure-table:BASEDIAGMEM-FIG-549 -->

**SPEC。** Figure 549〈Host Memory Buffer - Command Dword 15〉：定義 Host Memory Buffer 在 CDW15 的 command-specific 欄位。 先定位 CDW15，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：HMDLEC。

#### 這張 Figure 在完整流程中的位置

Figure 549 位於 §5.2.30.2.3，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 HMDLEC 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: HMDLEC]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `HMDLEC` | Host Memory Descriptor List Entry Count，HMDL 中有效 entries 的數量。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.2.3。
2. 依圖中指定的寬度與位置解碼 HMDLEC；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 549 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30.2.3 如何排列 HMDLEC、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.2.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 549 對應的 raw value 或 buffer，標出包含 HMDLEC 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 HMDLEC，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 HMDLEC 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** HMDLEC

**來源 keyword 索引：** `shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 549, 文件頁 518, PDF 頁 544

</details>

<details markdown="1">
<summary><strong>Figure 550: Host Memory Buffer - Host Memory Descriptor List</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-550-CLAIM figure-table:BASEDIAGMEM-FIG-550 -->

**SPEC。** Figure 550〈Host Memory Buffer - Host Memory Descriptor List〉：定義〈Host Memory Buffer - Host Memory Descriptor List〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：16-byte descriptor entries, HMDLEC。

#### 這張 Figure 在完整流程中的位置

Figure 550 位於 §5.2.30.2.3，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 16-byte descriptor entries 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: 16-byte descriptor entries]
          ↓
[擷取欄位: HMDLEC] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `16-byte descriptor entries` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `HMDLEC` | Host Memory Descriptor List Entry Count，HMDL 中有效 entries 的數量。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.2.3。
2. 依圖中指定的寬度與位置解碼 16-byte descriptor entries；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 HMDLEC 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 550 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30.2.3 如何排列 16-byte descriptor entries、HMDLEC 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.2.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 550 對應的 raw value 或 buffer，標出包含 16-byte descriptor entries 的 bytes 並解碼，再獨立核對 HMDLEC。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 16-byte descriptor entries，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 16-byte descriptor entries 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 HMDLEC 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** 16-byte descriptor entries, HMDLEC

**來源 keyword 索引：** `shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 550, 文件頁 518, PDF 頁 544

</details>

<details markdown="1">
<summary><strong>Figure 551: Host Memory Buffer - Host Memory Buffer Descriptor Entry</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-551-CLAIM figure-table:BASEDIAGMEM-FIG-551 -->

**SPEC。** Figure 551〈Host Memory Buffer - Host Memory Buffer Descriptor Entry〉：定義〈Host Memory Buffer - Host Memory Buffer Descriptor Entry〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：BADD, BSIZE, CC.MPS alignment。

#### 這張 Figure 在完整流程中的位置

Figure 551 位於 §5.2.30.2.3，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 BADD 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: BADD]
          ↓
[擷取欄位: BSIZE] → [套用編碼: CC.MPS alignment]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `BADD` | Buffer Address，HMB descriptor 中依 CC.MPS 對齊的 memory-page address。 |
| `BSIZE` | Buffer Size，HMB descriptor 中以 CC.MPS pages 表示的連續範圍長度。 |
| `CC.MPS alignment` | Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.MPS alignment 進一步指定其中的 MPS alignment 子欄位。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.2.3。
2. 依圖中指定的寬度與位置解碼 BADD；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 BSIZE 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 551 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30.2.3 如何排列 BADD、BSIZE 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.2.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 551 對應的 raw value 或 buffer，標出包含 BADD 的 bytes 並解碼，再獨立核對 BSIZE。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 BADD，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 BADD 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 BSIZE 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** BADD, BSIZE, CC.MPS alignment

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 551, 文件頁 518, PDF 頁 544

</details>

<details markdown="1">
<summary><strong>Figure 552: Host Memory Buffer - Completion Queue Entry Dword 0</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-552-CLAIM figure-table:BASEDIAGMEM-FIG-552 -->

**SPEC。** Figure 552〈Host Memory Buffer - Completion Queue Entry Dword 0〉：呈現〈Host Memory Buffer - Completion Queue Entry Dword 0〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：HMNAR, HMNARE, EHM。

#### 這張 Figure 在完整流程中的位置

Figure 552 位於 §5.2.30.2.3，在本流程中是「queue」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 HMNAR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 queue／command flow 圖。先標 host 與 controller 的 ownership，再追 head、tail、phase 或 arbitration 的改變；箭頭代表狀態或 ownership 轉移，不自動代表 command 已完成。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: HMNAR]
          ↓
[擷取欄位: HMNARE] → [套用編碼: EHM]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `HMNAR` | Host Memory Non-operational Access Restricted，回報 restriction 此刻是否實際生效的 state bit。 |
| `HMNARE` | Host Memory Non-operational Access Restriction Enable，配置 non-operational HMB access policy 的 bit。 |
| `EHM` | Enable Host Memory，啟用或停用 controller 使用 HMB 的 bit。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.2.3。
2. 依圖中指定的寬度與位置解碼 HMNAR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 HMNARE 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 552 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30.2.3 如何排列 HMNAR、HMNARE 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.2.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 552 對應的 raw value 或 buffer，標出包含 HMNAR 的 bytes 並解碼，再獨立核對 HMNARE。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 HMNAR，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 HMNAR 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 HMNARE 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** HMNAR, HMNARE, EHM

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 552, 文件頁 518-519, PDF 頁 544-545

</details>

<details markdown="1">
<summary><strong>Figure 553: Host Memory Buffer - Attributes Data Structure</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-553-CLAIM figure-table:BASEDIAGMEM-FIG-553 -->

**SPEC。** Figure 553〈Host Memory Buffer - Attributes Data Structure〉：定義〈Host Memory Buffer - Attributes Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：HSIZE, HMDLAL, HMDLAU, HMDLEC, 4096 bytes。

#### 這張 Figure 在完整流程中的位置

Figure 553 位於 §5.2.30.2.3，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 HSIZE 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: HSIZE]
          ↓
[擷取欄位: HMDLAL] → [套用編碼: HMDLAU]
                                      ↓
[驗證證據: HMDLEC]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `HSIZE` | Host Memory Buffer Size，以 CC.MPS memory-page units 表示的 HMB 總大小。 |
| `HMDLAL` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `HMDLAU` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `HMDLEC` | Host Memory Descriptor List Entry Count，HMDL 中有效 entries 的數量。 |
| `4096 bytes` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.2.3。
2. 依圖中指定的寬度與位置解碼 HSIZE；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 HMDLAL 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 553 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.30.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.30.2.3 如何排列 HSIZE、HMDLAL 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.2.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 553 對應的 raw value 或 buffer，標出包含 HSIZE 的 bytes 並解碼，再獨立核對 HMDLAL。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 HSIZE，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 HSIZE 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 HMDLAL 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** HSIZE, HMDLAL, HMDLAU, HMDLEC, 4096 bytes

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 553, 文件頁 519, PDF 頁 545

</details>

<a id="section-8-1"></a>

### §8.1

<details markdown="1">
<summary><strong>Figure 700: Example Device Self-test Operation (Informative)</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-700-CLAIM figure-table:BASEDIAGMEM-FIG-700 -->

**SPEC。** Figure 700〈Example Device Self-test Operation (Informative)〉：定義〈Example Device Self-test Operation (Informative)〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：segment, test performed, failure criteria, informative。

#### 這張 Figure 在完整流程中的位置

Figure 700 位於 §8.1.8，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 segment 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: segment]
          ↓
[擷取欄位: test performed] → [套用編碼: failure criteria]
                                      ↓
[驗證證據: informative]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `segment` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `test performed` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `failure criteria` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `informative` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §8.1.8。
2. 依圖中指定的寬度與位置解碼 segment；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 test performed 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 700 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.8 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §8.1.8 如何排列 segment、test performed 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §8.1.8 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 700 對應的 raw value 或 buffer，標出包含 segment 的 bytes 並解碼，再獨立核對 test performed。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 segment，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 segment 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 test performed 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** segment, test performed, failure criteria, informative

**來源 keyword 索引：** `shall`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.8, Figure 700, 文件頁 615, PDF 頁 641

</details>

<details markdown="1">
<summary><strong>Figure 701: Format NVM command Aborting a Device Self-Test Operation</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-701-CLAIM figure-table:BASEDIAGMEM-FIG-701 -->

**SPEC。** Figure 701〈Format NVM command Aborting a Device Self-Test Operation〉：定義〈Format NVM command Aborting a Device Self-Test Operation〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：SES, FNS, SENS, Format NSID, Self-test NSID, abort decision。

#### 這張 Figure 在完整流程中的位置

Figure 701 位於 §8.1.8.1-8.1.8.2，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SES 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SES]
          ↓
[擷取欄位: FNS] → [套用編碼: SENS]
                                      ↓
[驗證證據: Format NSID]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SES` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FNS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SENS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Format NSID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Self-test NSID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `abort decision` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §8.1.8.1-8.1.8.2。
2. 依圖中指定的寬度與位置解碼 SES；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 FNS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 701 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §8.1.8.1-8.1.8.2 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §8.1.8.1-8.1.8.2 如何排列 SES、FNS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §8.1.8.1-8.1.8.2 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 701 對應的 raw value 或 buffer，標出包含 SES 的 bytes 並解碼，再獨立核對 FNS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SES，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SES 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 FNS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SES, FNS, SENS, Format NSID, Self-test NSID, abort decision

**來源 keyword 索引：** `shall`, `should`, `may`, `optional`

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, Figure 701, 文件頁 616, PDF 頁 642

</details>

<a id="section-dependency"></a>

### 引用相依 Figure（位於主章節範圍外）

<details markdown="1">
<summary><strong>Figure 36: Offset 0h: CAP - Controller Capabilities</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-036-CLAIM figure-table:BASEDIAGMEM-FIG-036 -->

**SPEC。** Figure 36〈Offset 0h: CAP - Controller Capabilities〉：定義 offset 0h 的 CAP（Controller Capabilities），並指出軟體在該位置必須分別解碼的欄位。 先定位 CAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：DSTRD, 2^(2+DSTRD) bytes。

#### 這張 Figure 在完整流程中的位置

Figure 36 位於 §3.1.4.1，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DSTRD 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DSTRD]
          ↓
[擷取欄位: 2^(2+DSTRD) bytes] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DSTRD` | Doorbell Stride，CAP 中決定相鄰 doorbell register 間距的欄位。 |
| `2^(2+DSTRD) bytes` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.1。
2. 依圖中指定的寬度與位置解碼 DSTRD；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 2^(2+DSTRD) bytes 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
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
| 這張圖回答 | §3.1.4.1 如何排列 DSTRD、2^(2+DSTRD) bytes 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 36 對應的 raw value 或 buffer，標出包含 DSTRD 的 bytes 並解碼，再獨立核對 2^(2+DSTRD) bytes。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 DSTRD，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 DSTRD 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 2^(2+DSTRD) bytes 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** DSTRD, 2^(2+DSTRD) bytes

**來源 keyword 索引：** `shall not`, `shall`, `should`, `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, 文件頁 55-58, PDF 頁 81-84

</details>

<details markdown="1">
<summary><strong>Figure 93: Common Command Format</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-093-CLAIM figure-table:BASEDIAGMEM-FIG-093 -->

**SPEC。** Figure 93〈Common Command Format〉：定義〈Common Command Format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：OPC, CID, NSID, DPTR, CDW10-CDW15。

#### 這張 Figure 在完整流程中的位置

Figure 93 位於 §4.1.1，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 OPC 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: OPC]
          ↓
[擷取欄位: CID] → [套用編碼: NSID]
                                      ↓
[驗證證據: DPTR]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `OPC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CID` | Command Identifier，與 SQ identifier 合用以辨識 outstanding command。 |
| `NSID` | Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。 |
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

**來源欄位索引：** OPC, CID, NSID, DPTR, CDW10-CDW15

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, 文件頁 140-142, PDF 頁 166-168

</details>

<details markdown="1">
<summary><strong>Figure 94: Common Command Format - Vendor Specific Commands (Optional)</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-094-CLAIM figure-table:BASEDIAGMEM-FIG-094 -->

**SPEC。** Figure 94〈Common Command Format - Vendor Specific Commands (Optional)〉：定義〈Common Command Format - Vendor Specific Commands (Optional)〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NSID, MDPTR, NDT, NDM, CDW12-CDW15。

#### 這張 Figure 在完整流程中的位置

Figure 94 位於 §4.1.1，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NSID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSID]
          ↓
[擷取欄位: MDPTR] → [套用編碼: NDT]
                                      ↓
[驗證證據: NDM]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSID` | Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。 |
| `MDPTR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NDT` | Number of Dwords in Data Transfer，standard vendor-specific format 中的實際 data dword 數。 |
| `NDM` | Number of Dwords in Metadata Transfer，standard vendor-specific format 中的實際 metadata dword 數。 |
| `CDW12-CDW15` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.1.1。
2. 依圖中指定的寬度與位置解碼 NSID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MDPTR 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
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
| 這張圖回答 | §4.1.1 如何排列 NSID、MDPTR 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.1.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 94 對應的 raw value 或 buffer，標出包含 NSID 的 bytes 並解碼，再獨立核對 MDPTR。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 MDPTR 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NSID, MDPTR, NDT, NDM, CDW12-CDW15

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 94, 文件頁 143, PDF 頁 169

</details>

<details markdown="1">
<summary><strong>Figure 197: Get Features - Data Pointer</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-197-CLAIM figure-table:BASEDIAGMEM-FIG-197 -->

**SPEC。** Figure 197〈Get Features - Data Pointer〉：把〈Get Features - Data Pointer〉連到 self-test、host memory、doorbell 或 vendor command 的工程邊界。 先辨認 capability 與 owner，再解碼 DPTR, PRP1, PRP2，最後以 completion、log 或 memory lifecycle 證據核對。

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
<summary><strong>Figure 198: Get Features - Command Dword 10</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-198-CLAIM figure-table:BASEDIAGMEM-FIG-198 -->

**SPEC。** Figure 198〈Get Features - Command Dword 10〉：定義 Get Features 在 CDW10 的 command-specific 欄位。 先定位 CDW10，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：SEL, FID。

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
<summary><strong>Figure 200: Feature Identifiers for Get Features</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-200-CLAIM figure-table:BASEDIAGMEM-FIG-200 -->

**SPEC。** Figure 200〈Feature Identifiers for Get Features〉：定義〈Feature Identifiers for Get Features〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：FID 0Dh, Controller scope, data buffer。

#### 這張 Figure 在完整流程中的位置

Figure 200 位於 §5.2.12，在本流程中是「identifier」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 FID 0Dh 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 identifier 格式圖。先記錄 width 與 encoding，再辨識 issuing authority、uniqueness scope、reserved value 與有效生命週期；不要把長度相同的 identifiers 當成可互換。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: FID 0Dh]
          ↓
[擷取欄位: Controller scope] → [套用編碼: data buffer]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `FID 0Dh` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Controller scope` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `data buffer` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.12。
2. 依圖中指定的寬度與位置解碼 FID 0Dh；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Controller scope 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
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
| 這張圖回答 | §5.2.12 如何排列 FID 0Dh、Controller scope 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.12 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 200 對應的 raw value 或 buffer，標出包含 FID 0Dh 的 bytes 並解碼，再獨立核對 Controller scope。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 FID 0Dh，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 FID 0Dh 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Controller scope 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** FID 0Dh, Controller scope, data buffer

**來源 keyword 索引：** `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 200, 文件頁 210-211, PDF 頁 236-237

</details>

<details markdown="1">
<summary><strong>Figure 203: Get Log Page - Data Pointer</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-203-CLAIM figure-table:BASEDIAGMEM-FIG-203 -->

**SPEC。** Figure 203〈Get Log Page - Data Pointer〉：把〈Get Log Page - Data Pointer〉連到 self-test、host memory、doorbell 或 vendor command 的工程邊界。 先辨認 capability 與 owner，再解碼 DPTR，最後以 completion、log 或 memory lifecycle 證據核對。

#### 這張 Figure 在完整流程中的位置

Figure 203 位於 §5.2.13，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DPTR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

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

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.13。
2. 依圖中指定的寬度與位置解碼 DPTR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §5.2.13 如何排列 DPTR、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.13 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 203 對應的 raw value 或 buffer，標出包含 DPTR 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** DPTR

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 203, 文件頁 213, PDF 頁 239

</details>

<details markdown="1">
<summary><strong>Figure 204: Get Log Page - Command Dword 10</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-204-CLAIM figure-table:BASEDIAGMEM-FIG-204 -->

**SPEC。** Figure 204〈Get Log Page - Command Dword 10〉：定義 Get Log Page 在 CDW10 的 command-specific 欄位。 先定位 CDW10，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：NUMDL, RAE, LSP, LID 06h。

#### 這張 Figure 在完整流程中的位置

Figure 204 位於 §5.2.13，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NUMDL 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NUMDL]
          ↓
[擷取欄位: RAE] → [套用編碼: LSP]
                                      ↓
[驗證證據: LID 06h]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NUMDL` | Number of Dwords Lower，Get Log Page 的 NUMD 低 16 bits。 |
| `RAE` | Retain Asynchronous Event，Get Log Page 是否保留相關 asynchronous event 的 selector。 |
| `LSP` | Log Specific Field，意義由所選 log page 定義的 command selector。 |
| `LID 06h` | Device Self-test Log Page 的 identifier 06h；同時包含 current operation 與 20 筆歷史結果。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.13。
2. 依圖中指定的寬度與位置解碼 NUMDL；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 RAE 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §5.2.13 如何排列 NUMDL、RAE 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.13 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 204 對應的 raw value 或 buffer，標出包含 NUMDL 的 bytes 並解碼，再獨立核對 RAE。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NUMDL，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NUMDL 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 RAE 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NUMDL, RAE, LSP, LID 06h

**來源 keyword 索引：** `shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 204, 文件頁 213, PDF 頁 239

</details>

<details markdown="1">
<summary><strong>Figure 205: Get Log Page - Command Dword 11</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-205-CLAIM figure-table:BASEDIAGMEM-FIG-205 -->

**SPEC。** Figure 205〈Get Log Page - Command Dword 11〉：定義 Get Log Page 在 CDW11 的 command-specific 欄位。 先定位 CDW11，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：LSI, NUMDU。

#### 這張 Figure 在完整流程中的位置

Figure 205 位於 §5.2.13，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 LSI 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LSI]
          ↓
[擷取欄位: NUMDU] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LSI` | Log Specific Identifier，意義由所選 log page 定義的 identifier。 |
| `NUMDU` | Number of Dwords Upper，Get Log Page 的 NUMD 高 16 bits。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.13。
2. 依圖中指定的寬度與位置解碼 LSI；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NUMDU 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §5.2.13 如何排列 LSI、NUMDU 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.13 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 205 對應的 raw value 或 buffer，標出包含 LSI 的 bytes 並解碼，再獨立核對 NUMDU。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 LSI，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 LSI 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NUMDU 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** LSI, NUMDU

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 205, 文件頁 214, PDF 頁 240

</details>

<details markdown="1">
<summary><strong>Figure 206: Get Log Page - Command Dword 12</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-206-CLAIM figure-table:BASEDIAGMEM-FIG-206 -->

**SPEC。** Figure 206〈Get Log Page - Command Dword 12〉：定義 Get Log Page 在 CDW12 的 command-specific 欄位。 先定位 CDW12，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：LPOL, OT。

#### 這張 Figure 在完整流程中的位置

Figure 206 位於 §5.2.13，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 LPOL 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LPOL]
          ↓
[擷取欄位: OT] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LPOL` | Log Page Offset Lower，Get Log Page byte offset 的低 32 bits。 |
| `OT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.13。
2. 依圖中指定的寬度與位置解碼 LPOL；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 OT 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §5.2.13 如何排列 LPOL、OT 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.13 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 206 對應的 raw value 或 buffer，標出包含 LPOL 的 bytes 並解碼，再獨立核對 OT。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 LPOL，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 LPOL 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 OT 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** LPOL, OT

**來源 keyword 索引：** `shall`, `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 206, 文件頁 214, PDF 頁 240

</details>

<details markdown="1">
<summary><strong>Figure 207: Get Log Page - Command Dword 13</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-207-CLAIM figure-table:BASEDIAGMEM-FIG-207 -->

**SPEC。** Figure 207〈Get Log Page - Command Dword 13〉：定義 Get Log Page 在 CDW13 的 command-specific 欄位。 先定位 CDW13，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：LPOU。

#### 這張 Figure 在完整流程中的位置

Figure 207 位於 §5.2.13，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 LPOU 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

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

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.13。
2. 依圖中指定的寬度與位置解碼 LPOU；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §5.2.13 如何排列 LPOU、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.13 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 207 對應的 raw value 或 buffer，標出包含 LPOU 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 LPOU，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 LPOU 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** LPOU

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 207, 文件頁 214, PDF 頁 240

</details>

<details markdown="1">
<summary><strong>Figure 208: Get Log Page - Command Dword 14</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-208-CLAIM figure-table:BASEDIAGMEM-FIG-208 -->

**SPEC。** Figure 208〈Get Log Page - Command Dword 14〉：定義 Get Log Page 在 CDW14 的 command-specific 欄位。 先定位 CDW14，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：CSI, OT, UIDX。

#### 這張 Figure 在完整流程中的位置

Figure 208 位於 §5.2.13，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CSI 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CSI]
          ↓
[擷取欄位: OT] → [套用編碼: UIDX]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CSI` | Command Set Identifier，選擇 command 或 log page 所套用的 I/O Command Set context。 |
| `OT` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `UIDX` | UUID Index，指向 UUID List 位置的 index；0 表示未指定 UUID。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.13。
2. 依圖中指定的寬度與位置解碼 CSI；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 OT 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §5.2.13 如何排列 CSI、OT 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.13 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 208 對應的 raw value 或 buffer，標出包含 CSI 的 bytes 並解碼，再獨立核對 OT。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CSI，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CSI 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 OT 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CSI, OT, UIDX

**來源 keyword 索引：** `shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 208, 文件頁 214-215, PDF 頁 240-241

</details>

<details markdown="1">
<summary><strong>Figure 209: Get Log Page - Log Page Identifiers</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-209-CLAIM figure-table:BASEDIAGMEM-FIG-209 -->

**SPEC。** Figure 209〈Get Log Page - Log Page Identifiers〉：定義〈Get Log Page - Log Page Identifiers〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：LID 06h, CSI = N, Controller / Domain / NVM subsystem, Device Self-test, §5.2.13.1.7。

#### 這張 Figure 在完整流程中的位置

Figure 209 位於 §5.2.13，在本流程中是「identifier」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 LID 06h 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 identifier 格式圖。先記錄 width 與 encoding，再辨識 issuing authority、uniqueness scope、reserved value 與有效生命週期；不要把長度相同的 identifiers 當成可互換。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LID 06h]
          ↓
[擷取欄位: CSI = N] → [套用編碼: Controller / Domain / NVM subsystem]
                                      ↓
[驗證證據: Device Self-test]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LID 06h` | Device Self-test Log Page 的 identifier 06h；同時包含 current operation 與 20 筆歷史結果。 |
| `CSI = N` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Controller / Domain / NVM subsystem` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Device Self-test` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `§5.2.13.1.7` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.13。
2. 依圖中指定的寬度與位置解碼 LID 06h；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CSI = N 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §5.2.13 如何排列 LID 06h、CSI = N 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.13 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 209 對應的 raw value 或 buffer，標出包含 LID 06h 的 bytes 並解碼，再獨立核對 CSI = N。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 LID 06h，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 LID 06h 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CSI = N 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** LID 06h, CSI = N, Controller / Domain / NVM subsystem, Device Self-test, §5.2.13.1.7

**來源 keyword 索引：** `shall`, `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 209, 文件頁 215-216, PDF 頁 241-242

</details>

<details markdown="1">
<summary><strong>Figure 338: Identify Controller Data Structure</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-338-CLAIM figure-table:BASEDIAGMEM-FIG-338 -->

**SPEC。** Figure 338〈Identify Controller Data Structure〉：定義〈Identify Controller Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：OACS.DSTS, EDSTT, DSTO.SDSO, HMPRE, HMMIN, HMMINDS, HMMAXD, CTRATT.HMBR, AVSCC.VSCF, ICSVSCC.SNVSCF。

#### 這張 Figure 在完整流程中的位置

Figure 338 位於 §5.2.14.2.1，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 OACS.DSTS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: OACS.DSTS]
          ↓
[擷取欄位: EDSTT] → [套用編碼: DSTO.SDSO]
                                      ↓
[驗證證據: HMPRE]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `OACS.DSTS` | Optional Admin Command Support 的 Device Self-test Supported bit，判斷 command 是否可用。 |
| `EDSTT` | Extended Device Self-test Time，在 power state 0 下的 extended test 名目完成分鐘數。 |
| `DSTO.SDSO` | Device Self-test Options，Identify Controller 中回報 refresh 與 concurrency 選項的欄位。 此處的 DSTO.SDSO 進一步指定其中的 SDSO 子欄位。 |
| `HMPRE` | Host Memory Buffer Preferred Size，以 4 KiB units 回報 controller 偏好的配置大小。 |
| `HMMIN` | Host Memory Buffer Minimum Size，以 4 KiB units 回報 controller 要求的最低大小。 |
| `HMMINDS` | Host Memory Buffer Minimum Descriptor Entry Size，每個可用 descriptor 的最低 4 KiB-unit 大小。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.14.2.1。
2. 依圖中指定的寬度與位置解碼 OACS.DSTS；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 EDSTT 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
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
| 這張圖回答 | §5.2.14.2.1 如何排列 OACS.DSTS、EDSTT 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.14.2.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 338 對應的 raw value 或 buffer，標出包含 OACS.DSTS 的 bytes 並解碼，再獨立核對 EDSTT。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 OACS.DSTS，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 OACS.DSTS 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 EDSTT 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** OACS.DSTS, EDSTT, DSTO.SDSO, HMPRE, HMMIN, HMMINDS, HMMAXD, CTRATT.HMBR, AVSCC.VSCF, ICSVSCC.SNVSCF

**來源 keyword 索引：** `shall not`, `should not`, `shall`, `should`, `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, 文件頁 340-364, PDF 頁 366-390

</details>

<details markdown="1">
<summary><strong>Figure 463: Set Features - Data Pointer</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-463-CLAIM figure-table:BASEDIAGMEM-FIG-463 -->

**SPEC。** Figure 463〈Set Features - Data Pointer〉：把〈Set Features - Data Pointer〉連到 self-test、host memory、doorbell 或 vendor command 的工程邊界。 先辨認 capability 與 owner，再解碼 DPTR, PRP1, PRP2，最後以 completion、log 或 memory lifecycle 證據核對。

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
<summary><strong>Figure 464: Set Features - Command Dword 10</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-464-CLAIM figure-table:BASEDIAGMEM-FIG-464 -->

**SPEC。** Figure 464〈Set Features - Command Dword 10〉：定義 Set Features 在 CDW10 的 command-specific 欄位。 先定位 CDW10，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：SV, FID。

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
<summary><strong>Figure 466: Feature Identifiers for Set Features</strong></summary>

<!-- claim:BASEDIAGMEM-FIG-466-CLAIM figure-table:BASEDIAGMEM-FIG-466 -->

**SPEC。** Figure 466〈Feature Identifiers for Set Features〉：定義〈Feature Identifiers for Set Features〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：FID 0Dh, Controller scope, saveable, changeable。

#### 這張 Figure 在完整流程中的位置

Figure 466 位於 §5.2.30，在本流程中是「identifier」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 FID 0Dh 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 identifier 格式圖。先記錄 width 與 encoding，再辨識 issuing authority、uniqueness scope、reserved value 與有效生命週期；不要把長度相同的 identifiers 當成可互換。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: FID 0Dh]
          ↓
[擷取欄位: Controller scope] → [套用編碼: saveable]
                                      ↓
[驗證證據: changeable]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `FID 0Dh` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Controller scope` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `saveable` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `changeable` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30。
2. 依圖中指定的寬度與位置解碼 FID 0Dh；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Controller scope 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
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
| 這張圖回答 | §5.2.30 如何排列 FID 0Dh、Controller scope 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 466 對應的 raw value 或 buffer，標出包含 FID 0Dh 的 bytes 並解碼，再獨立核對 Controller scope。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 FID 0Dh，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 FID 0Dh 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Controller scope 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** FID 0Dh, Controller scope, saveable, changeable

**來源 keyword 索引：** `shall`, `should`, `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 466, 文件頁 457-459, PDF 頁 483-485

</details>

## 使用與限制

製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata 集合或核准範圍改變時，必須重新核對受影響 claim。
