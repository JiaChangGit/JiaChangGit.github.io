---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4：Device Self-test 與 Namespace Management"
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
[English]({% post_url 2026-09-02-nvme-base-self-test-namespace-management-en %})


# NVMe Base 2.4：Device Self-test 與 Namespace Management

用途：供 GitHub Pages 閱讀與 100 分鐘簡報製作；讀者已具備 PCIe 與 NVMe 基礎。

範圍：Base §5.2.6、§5.2.13.1.7（僅 LID 06h）、§5.2.24、§5.2.25、§8.1.8、§8.1.17（排除 §8.1.17.3），以及 NVM Command Set 1.3 §2.1.1、§4.1.4.3、§4.1.6、§5.8；另含理解與實作所需的最小 dependency slice。正文只保留 PCIe／memory-based 與通用 NVMe 內容。

## 來源版本

NVM Express Base Specification, Revision 2.4
NVM Express NVM Command Set Specification, Revision 1.3

查證日期：2026-09-02。目前未納入其他 Errata、ECN、Technical Proposal、controller vendor 文件或未提供的 PCI Express Base Specification 原文。

## 閱讀地圖

```text
Discover capability and capacity -> Run self-test / construct namespace -> Observe LID 06h / receive NSID -> Attach, verify, detach, or delete
```

本報告把診斷與配置分成兩條生命週期：Self-test 用 LID 06h 證明背景 operation 的結果；Namespace Management 先建立未附掛 namespace，再用 Controller List 建立可存取關係，最後以 event、Identify 與 CQE 關閉驗證迴路。

## 規範性用語

shall 譯為「必須」，may 譯為「可／得」，should 譯為「宜／建議」，optional 譯為「選用」。本文不提高或降低原文語氣。

## 先學縮寫：完整 Glossary

下列縮寫會在投影片主線使用前先定義。縮寫本身永遠不夠；設計與 Debug 還要保留 owner、width、unit、scope 與 state。

| 縮寫／名詞 | 白話解釋 | 來源 |
|---|---|---|
| `DST` | Device Self-test，用背景 diagnostic segments 檢查 controller 與可選 namespace media 的操作。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.8，文件頁 353-358, 614，PDF 頁 379-384, 640 |
| `OACS.DSTS` | Optional Admin Command Support 的 Device Self-test Supported bit，判斷 command 是否可用。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.8，文件頁 353-358, 614，PDF 頁 379-384, 640 |
| `STC` | Self-test Code 是 Device Self-test CDW10 的動作 nibble；result entry 的 STC 則是 Status Code，須依 SCVLD 判斷有效。 | NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 199-200，PDF 頁 225-226 |
| `DSTP` | Device Self-test Parameter，只有 vendor-specific STC=Eh 時才有 vendor-defined 語意的 CDW15。 | NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 199-200，PDF 頁 225-226 |
| `DSTO` | Device Self-test Options，Identify Controller 中回報 refresh 與 concurrency 選項的欄位。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.8，文件頁 353-358, 614，PDF 頁 379-384, 640 |
| `SDSO` | Single Device Self-test Operation，選擇 subsystem-wide 單一 operation 或 per-controller operation 的 bit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.8，文件頁 353-358, 614，PDF 頁 379-384, 640 |
| `EDSTT` | Extended Device Self-test Time，在 power state 0 下的 extended test 名目完成分鐘數。 | NVME-BASE-2.4 Rev. 2.4，§8.1.8.1-8.1.8.2，文件頁 615-616，PDF 頁 641-642 |
| `LID 06h` | Device Self-test Log Page 的 identifier 06h；同時包含 current operation 與 20 筆歷史結果。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13，文件頁 213-216，PDF 頁 239-242 |
| `DSTOS` | Device Self-test Operation Status，LID 06h 中表示目前 operation 類型的 nibble。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 229-230，PDF 頁 255-256 |
| `DSTCS` | Device Self-test Completion Status，LID 06h 中的 0 到 100 完成百分比。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 229-230，PDF 頁 255-256 |
| `DSTR` | Device Self-test Result，結果 entry 中表示成功、abort 或 segment failure 的 nibble。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 229-232，PDF 頁 255-258 |
| `SEGN` | Segment Number，只有 DSTR=7h 時指出第一個失敗 diagnostic segment。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 229-232，PDF 頁 255-258 |
| `VDINFO` | Valid Diagnostic Information，分別 gate NSID、FLBA、SCT 與 SC 的 validity bitmap。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 231-232，PDF 頁 257-258 |
| `FVLD` | Failing LBA Valid，決定 FLBA 欄位是否可解讀的 validity bit。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.4.3，文件頁 76，PDF 頁 76 |
| `FLBA` | Failing LBA，NVM Command Set 定義為造成 self-test failure 的其中一個 logical block address。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.4.3，文件頁 76，PDF 頁 76 |
| `NSID` | Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。 | NVME-BASE-2.4 Rev. 2.4，§8.1.17，文件頁 660，PDF 頁 686 |
| `OACS.NMS` | Optional Admin Command Support 的 Namespace Management Supported bit；設為 1 才宣告完整 Manage 加 Attach capability。 | NVME-BASE-2.4 Rev. 2.4，§8.1.17，文件頁 660，PDF 頁 686 |
| `NSZE` | Namespace Size，namespace 的總 logical block 數，LBA 範圍為 0 到 NSZE−1。 | NVME-NVM-CS-1.3 Rev. 1.3，§2.1.1，文件頁 13-14，PDF 頁 13-14 |
| `NCAP` | Namespace Capacity，任一時點最多可配置給 namespace 的 logical blocks。 | NVME-NVM-CS-1.3 Rev. 1.3，§2.1.1，文件頁 13-14，PDF 頁 13-14 |
| `NUSE` | Namespace Utilization，目前已配置給 namespace 的 logical blocks。 | NVME-NVM-CS-1.3 Rev. 1.3，§2.1.1，文件頁 13-14，PDF 頁 13-14 |
| `THINP` | Thin Provisioning，NSFEAT 中決定 NCAP 是否可小於 NSZE，以及 controller 是否必須追蹤 NUSE 的 bit。 | NVME-NVM-CS-1.3 Rev. 1.3，§2.1.1，文件頁 13，PDF 頁 13 |
| `CNS` | Controller or Namespace Structure，Identify command 中選擇要回傳哪一種資料結構的欄位。 | NVME-BASE-2.4 Rev. 2.4，§8.1.17.1，文件頁 661-662，PDF 頁 687-688 |
| `DPTR` | Data Pointer，SQE 中指出 command data buffer 的欄位。 | NVME-BASE-2.4 Rev. 2.4，§5.2.25，文件頁 446-448，PDF 頁 472-474 |
| `PRP` | Physical Region Page，以 memory page 為單位描述 host-addressable data buffer 的 pointer 格式。 | NVME-BASE-2.4 Rev. 2.4，§5.2.24，文件頁 444-445，PDF 頁 470-471 |
| `SEL` | Select；Namespace Management 的 create/delete/restore selector，與 Get Features 的 SEL 不同。 | NVME-BASE-2.4 Rev. 2.4，§5.2.25，文件頁 446-448，PDF 頁 472-474 |
| `CSI` | Command Set Identifier，選擇 command 或 log page 所套用的 I/O Command Set context。 | NVME-BASE-2.4 Rev. 2.4，§5.2.25，文件頁 446-448，PDF 頁 472-474 |
| `SIOCS` | Specified I/O Command Set，Base create buffer bytes 0:511 中放置所選 I/O Command Set specific fields 的區域。 | NVME-BASE-2.4 Rev. 2.4，§5.2.25，文件頁 446-448，PDF 頁 472-474 |
| `FLBAS` | Formatted LBA Size，選擇 namespace 使用的 LBA format，並包含 metadata placement 相關控制。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6.4，文件頁 111-113，PDF 頁 111-113 |
| `DPS` | End-to-end Data Protection Type Settings，create 時選擇 Protection Information type 與位置的欄位。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6.2，文件頁 110，PDF 頁 110 |
| `NMIC` | Namespace Multi-path I/O and Namespace Sharing Capabilities，create 時宣告 namespace sharing／multipath 屬性的欄位。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6.4，文件頁 111-113，PDF 頁 111-113 |
| `ANAGRPID` | ANA Group Identifier，namespace 所屬 Asymmetric Namespace Access group 的 identifier；create 值 0 讓 controller 選擇。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6.4，文件頁 111-113，PDF 頁 111-113 |
| `NVMSETID` | NVM Set Identifier，指定建立 namespace 時要從哪個 NVM Set 配置容量。 | NVME-BASE-2.4 Rev. 2.4，§8.1.17，文件頁 661，PDF 頁 687 |
| `ENDGID` | Endurance Group Identifier，指定建立 namespace 時所屬 Endurance Group。 | NVME-BASE-2.4 Rev. 2.4，§8.1.17，文件頁 661，PDF 頁 687 |
| `LBSTM` | Logical Block Storage Tag Mask，create 時指定哪些 Storage Tag bits 被 mask 的 64-bit 欄位。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6.2，文件頁 110，PDF 頁 110 |
| `FDP` | Flexible Data Placement，把資料放置提示與媒體回收管理連結的能力。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6.3，文件頁 110-111，PDF 頁 110-111 |
| `NPHNDLS` | Number of Placement Handles，NVM create payload 中 Placement Handle List 的 entry count，最大 128。 | NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6.3，文件頁 110-111，PDF 頁 110-111 |
| `NSG` | Namespace Size Granularity，以 bytes 表示 controller 偏好的 NSZE allocation granularity。 | NVME-NVM-CS-1.3 Rev. 1.3，§5.8，文件頁 165，PDF 頁 165 |
| `NCG` | Namespace Capacity Granularity，以 bytes 表示 controller 偏好的 NCAP allocation granularity。 | NVME-NVM-CS-1.3 Rev. 1.3，§5.8，文件頁 165，PDF 頁 165 |
| `MAXDNA` | Maximum Domain Namespace Attachments，整個 Domain 內所有 I/O controller attachment 數量總和的上限。 | NVME-BASE-2.4 Rev. 2.4，§5.2.24，文件頁 444-445，PDF 頁 470-471 |
| `MAXCNA` | Maximum I/O Controller Namespace Attachments，單一 I/O controller 可附掛 namespaces 的上限。 | NVME-BASE-2.4 Rev. 2.4，§5.2.24，文件頁 444-445，PDF 頁 470-471 |
| `RDNCS` | Restore Default Namespace Configuration Supported，宣告 Restore Default operation 是否支援的 capability bit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.25.1，文件頁 447-448，PDF 頁 473-474 |
| `DNCS` | Default Namespace Configuration Status，表示目前 namespace configuration 是否等於 active firmware image defaults 的 status bit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.25.1，文件頁 447-448，PDF 頁 473-474 |
| `CQE` | Completion Queue Entry，CQ 中的一筆完成結果資料結構。 | NVME-BASE-2.4 Rev. 2.4，§5.2.25, 8.1.17.1，文件頁 446-448, 662，PDF 頁 472-474, 688 |
| `AER (Admin)` | Asynchronous Event Request，host 預先提交的 Admin command，controller 透過其 CQE 回報 namespace attribute change 等事件。 | NVME-BASE-2.4 Rev. 2.4，§8.1.17.1-8.1.17.2，文件頁 662-663，PDF 頁 688-689 |
| `AEN` | Asynchronous Event Notification，controller 透過已提交 Asynchronous Event Request 回報事件的通知。 | NVME-BASE-2.4 Rev. 2.4，§8.1.17.1-8.1.17.2，文件頁 662-663，PDF 頁 688-689 |

## Visual Atlas：先用圖建立整體位置

每張教學重畫回答不同問題：Architecture 定位元件、Sequence 顯示 ownership、Decode 把 bits 轉成工程值、State 保留 failure evidence；它們不是 Spec 原圖的複製。

### Visual 01: 先分清兩條生命週期：diagnostic evidence 與 namespace provisioning

**View type:** `architecture`

```text
[Capability snapshot]
  ├─ [Self-test operation]
  ├─ [LID 06h evidence]
  ├─ [Namespace create]
  ├─ [Attach relationship]
  └─ [Identify／event verification]
```

**回答的問題：** Device Self-test 與 Namespace Management 都使用 Admin command，但它們改變的物件完全不同。Self-test 建立一個背景 operation，command CQE 只是接受點，最後要靠 LID 06h 證明結果；Namespace Management 建立或移除 namespace object，Create CQE 回傳 NSID，但還要 Attach 才建立 controller access。先分開兩條線，才能理解 completion 為何不是終點。

**支援 Figure：** Figure 93, Figure 176, Figure 218, Figure 445, Figure 450, Figure 155

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 201，PDF 頁 227; NVME-BASE-2.4 Rev. 2.4，§8.1.17，文件頁 660，PDF 頁 686; NVME-BASE-2.4 Rev. 2.4，§5.2.25, 8.1.17.1，文件頁 446-448, 662，PDF 頁 472-474, 688

### Visual 02: Device Self-test：從 capability gate 到 LID 06h result

**View type:** `state`

```text
[OACS.DSTS gate] → [選 NSID＋STC] → [Admin CQE：start accepted] → [輪詢 DSTOS／DSTCS] → [RDS1 建立] → [VDINFO gate＋FLBA]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**回答的問題：** 先用 OACS.DSTS、EDSTT 與 DSTO.SDSO 建立支援、時間與 concurrency 預期，再以 NSID 與 STC 建構 command。CQE 到達後輪詢 DSTOS／DSTCS；operation 結束時，先建立 RDS1，再把 current status 清零。這個先後順序讓 software 不會在短暫視窗遺失最後結果。

**支援 Figure：** Figure 176, Figure 177, Figure 178, Figure 179, Figure 180, Figure 203, Figure 204, Figure 205, Figure 206, Figure 207, Figure 208, Figure 209, Figure 218, Figure 219, Figure 111, Figure 700, Figure 701

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.8，文件頁 353-358, 614，PDF 頁 379-384, 640; NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 199，PDF 頁 225; NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 199-200，PDF 頁 225-226; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 229-230，PDF 頁 255-256; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 229-232，PDF 頁 255-258; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 231-232，PDF 頁 257-258; NVME-NVM-CS-1.3 Rev. 1.3，§4.1.4.3，文件頁 76，PDF 頁 76

### Visual 03: 先把三種容量與兩種 granularity 換到同一個 byte model

**View type:** `decode`

```text
[RAW: 讀 LBA format] → [LOCATE: NSZE／NCAP／NUSE blocks] → [DECODE: 乘 LBA bytes]
[VALIDATE: 檢查 NSG／NCG 整除] → [APPLY: 估算 allocation rounding] → [EVIDENCE: 記錄 addressable 與 consumed]
VALIDATE fail ──→ return to RAW evidence
```

**回答的問題：** NSZE、NCAP、NUSE 的單位是 logical blocks；NSG、NCG 的單位是 bytes；controller 實際消耗的 NVM capacity 又可能按 allocation unit 向上取整。比較前必須先乘上選定 LBA size。NSZE≥NCAP≥NUSE 是合法性關係，NSG／NCG divisibility 則是減少浪費的 hint，不能混成同一種 gate。

**支援 Figure：** Figure 123, Figure 132, Figure 133

**來源：** NVME-NVM-CS-1.3 Rev. 1.3，§2.1.1，文件頁 13-14，PDF 頁 13-14; NVME-NVM-CS-1.3 Rev. 1.3，§2.1.1，文件頁 13，PDF 頁 13; NVME-BASE-2.4 Rev. 2.4，§8.1.17，文件頁 661，PDF 頁 687; NVME-NVM-CS-1.3 Rev. 1.3，§5.8，文件頁 165，PDF 頁 165; NVME-NVM-CS-1.3 Rev. 1.3，§5.8，文件頁 165，PDF 頁 165

### Visual 04: Create payload：Base envelope 包住 NVM-specific 512 bytes

**View type:** `decode`

```text
[RAW: SEL=Create、CSI=00h] → [LOCATE: 配置 4096-byte zeroed buffer] → [DECODE: 填 NSZE／NCAP／FLBAS]
[VALIDATE: 填 DPS／NMIC／group IDs] → [APPLY: 驗證 LBSTM／NPHNDLS] → [EVIDENCE: DPTR＋SQE snapshot]
VALIDATE fail ──→ return to RAW evidence
```

**回答的問題：** Base Figure 448 定義 4096-byte envelope，NVM Command Set Figure 134 只定義前 768 bytes 中的 NVM 欄位與 Placement Handle List。Host 先以 SEL／CSI 決定 operation 與 command set，再填 NSZE、NCAP、format、protection、sharing 與 group IDs。Reserved areas 要清零，Protection Information 與 FDP 又各有獨立 capability gate。

**支援 Figure：** Figure 36, Figure 93, Figure 127, Figure 134, Figure 445, Figure 446, Figure 447, Figure 448

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.25，文件頁 446-448，PDF 頁 472-474; NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6.4，文件頁 111-113，PDF 頁 111-113; NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6.2，文件頁 110，PDF 頁 110; NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6.3，文件頁 110-111，PDF 頁 110-111; NVME-BASE-2.4 Rev. 2.4，§8.1.17，文件頁 661，PDF 頁 687

### Visual 05: Namespace lifecycle：Create 只建立 object，Attach 才建立 access

**View type:** `state`

```text
[Unallocated NSID] → [Create→allocated/unattached] → [CQE.DW0 保存 NSID] → [Attach→active on controller] → [Detach→inactive on controller] → [Delete→unallocated]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**回答的問題：** Create、Attach、Detach、Delete 分別改變兩個狀態維度：namespace 是否 allocated，以及某 controller 是否 attached。Create CQE.DW0 回 NSID 後，object 已 allocated 但所有 controller 都未 attached；Attach 的 Controller List 才建立 access。Detach 不刪容量，Delete 才使 NSID unallocated。

**支援 Figure：** Figure 139, Figure 338, Figure 442, Figure 443, Figure 444, Figure 450

**來源：** NVME-BASE-2.4 Rev. 2.4，§8.1.17，文件頁 660，PDF 頁 686; NVME-BASE-2.4 Rev. 2.4，§8.1.17，文件頁 660，PDF 頁 686; NVME-BASE-2.4 Rev. 2.4，§5.2.24，文件頁 444-445，PDF 頁 470-471; NVME-BASE-2.4 Rev. 2.4，§5.2.24，文件頁 444-445，PDF 頁 470-471; NVME-BASE-2.4 Rev. 2.4，§5.2.25, 8.1.17.1，文件頁 446-448, 662，PDF 頁 472-474, 688

### Visual 06: Delete 與 Restore Default：先清空 inventory，再跨 configuration boundary

**View type:** `state`

```text
[先 detach 所有 controllers] → [Delete NSID 或 FFFFFFFFh] → [確認 Allocated list 為空] → [RDNCS=1 gate] → [SEL=2h Restore] → [DNCS=1＋重新 Identify]
timeout / failure ──→ preserve trigger + previous state + evidence
```

**回答的問題：** Delete all 與 Restore Default 是兩個不同 operation。NSID=FFFFFFFFh 的 Delete All 在零個 namespaces 時也成功；Restore Default 則要求 RDNCS capability、SEL=2h，以及 subsystem 中已不存在任何 namespace。成功前 controller 套用 current active firmware image defaults 並設 DNCS=1。

**支援 Figure：** Figure 304, Figure 338, Figure 446, Figure 449, Figure 474

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.25, 8.1.17.1，文件頁 446, 448, 662，PDF 頁 472, 474, 688; NVME-BASE-2.4 Rev. 2.4，§5.2.25.1，文件頁 447-448，PDF 頁 473-474; NVME-BASE-2.4 Rev. 2.4，§8.1.17.1-8.1.17.2，文件頁 662-663，PDF 頁 688-689

### Visual 07: Namespace event：通知只說 inventory 變了，Identify 才說變成什麼

**View type:** `sequence`

```text
Host / software        Shared object        Controller / evidence
Host → Shared: Host 預先提交 AER
Shared → Controller: Create／Attach／Detach／Delete
Controller → Shared: controller 更新 inventory
Shared → Host: AEN CQE posted
Host → Shared: host 依 CNS 重新 Identify
Shared → Controller: 比較 before／after list
```

**回答的問題：** Attached 與 Allocated Namespace Attribute Changed notices 對應不同 inventory。Create 通常改 Allocated list；Attach／Detach 改 Active list；Delete 可能同時改兩者。event code 不是新清單本身，因此 host 收到 AEN 後要依 CNS 重新 Identify。Delete reporting 還要分辨 processing controller 與其他 controllers。

**支援 Figure：** Figure 155, Figure 474

**來源：** NVME-BASE-2.4 Rev. 2.4，§8.1.17，文件頁 660，PDF 頁 686; NVME-BASE-2.4 Rev. 2.4，§8.1.17.1-8.1.17.2，文件頁 662-663，PDF 頁 688-689; NVME-BASE-2.4 Rev. 2.4，§5.2.25, 8.1.17.1，文件頁 446-448, 662，PDF 頁 472-474, 688

### Visual 08: End-to-End：把 capacity、command、object、attachment 與 evidence 放在同一條 timeline

**View type:** `sequence`

```text
Host / software        Shared object        Controller / evidence
Host → Shared: Capability／capacity snapshot
Shared → Controller: raw Create SQE＋buffer
Controller → Shared: CQE.DW0 returned NSID
Shared → Host: raw Attach SQE＋Controller List
Host → Shared: AEN＋Identify refresh
Shared → Controller: I/O／detach／delete outcome
```

**回答的問題：** Namespace bug 很少只是一個欄位錯。create 前的 capability snapshot、4096-byte payload、CQE.DW0、Controller List、attach limits、events 與 post-Identify 必須能串回同一個 NSID 與 controller set。Debug 不從最後的 I/O failure 猜原因，而是找第一個不一致 boundary。

**支援 Figure：** Figure 123, Figure 127, Figure 134, Figure 139, Figure 338, Figure 442, Figure 443, Figure 444, Figure 445, Figure 446, Figure 447, Figure 448, Figure 449, Figure 450

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.24-5.2.25，文件頁 445, 448，PDF 頁 471, 474; NVME-BASE-2.4 Rev. 2.4，§5.2.24-5.2.25, 8.1.17.1，文件頁 444-448, 661-663，PDF 頁 470-474, 687-689; NVME-BASE-2.4 Rev. 2.4，§5.2.24，文件頁 444-445，PDF 頁 470-471; NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6.2，文件頁 110，PDF 頁 110; NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6.3，文件頁 110-111，PDF 頁 110-111

## Mental Model 與完整教學流程

以下依工程因果而非 Spec section 排列；相關 Figure 會回到它支援的流程節點，不以編號順序取代教學故事線。

### Module 01: 先分清兩條生命週期：diagnostic evidence 與 namespace provisioning

**解釋。** Device Self-test 與 Namespace Management 都使用 Admin command，但它們改變的物件完全不同。Self-test 建立一個背景 operation，command CQE 只是接受點，最後要靠 LID 06h 證明結果；Namespace Management 建立或移除 namespace object，Create CQE 回傳 NSID，但還要 Attach 才建立 controller access。先分開兩條線，才能理解 completion 為何不是終點。

```text
Capability snapshot
  ↓
Self-test operation
  ↓
LID 06h evidence
  ↓
Namespace create
  ↓
Attach relationship
  ↓
Identify／event verification
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Self-test object | background operation | CQE→current state→history result |
| Namespace object | allocated capacity + format | Create CQE.DW0→NSID |
| Access relationship | namespace↔controller attachment | Attach CQE→Active NSID list |
| Inventory evidence | Allocated／Active lists | AEN 後重新 Identify |

**說明性範例。** Create 成功回 NSID=7 只證明 namespace 7 已建立；它仍未 attached，不能立刻做 I/O。相反地，Self-test 啟動成功的 CQE 也只證明 operation 已開始，不能把它記成 test passed。兩種 CQE 都要再接下一個證據，但下一個證據不同。

**常見誤解／Debug。** 不要用『Admin command 成功』概括整段流程。trace 必須標出 command 改變的 object、成功所跨越的 boundary，以及仍待取得的 LID、Identify 或 event evidence。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 201，PDF 頁 227; NVME-BASE-2.4 Rev. 2.4，§8.1.17，文件頁 660，PDF 頁 686; NVME-BASE-2.4 Rev. 2.4，§5.2.25, 8.1.17.1，文件頁 446-448, 662，PDF 頁 472-474, 688

**關聯 Figure：** Figure 93, Figure 176, Figure 218, Figure 445, Figure 450, Figure 155

### Module 02: Device Self-test：從 capability gate 到 LID 06h result

**解釋。** 先用 OACS.DSTS、EDSTT 與 DSTO.SDSO 建立支援、時間與 concurrency 預期，再以 NSID 與 STC 建構 command。CQE 到達後輪詢 DSTOS／DSTCS；operation 結束時，先建立 RDS1，再把 current status 清零。這個先後順序讓 software 不會在短暫視窗遺失最後結果。

```text
OACS.DSTS gate
  ↓
選 NSID＋STC
  ↓
Admin CQE：start accepted
  ↓
輪詢 DSTOS／DSTCS
  ↓
RDS1 建立
  ↓
VDINFO gate＋FLBA
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| NSID=0 | controller only | 不包含 namespace media |
| active NSID | 單一 namespace | invalid／inactive status 分開 |
| NSID=FFFFFFFFh | 開始時可存取的 attached set | 集合不是動態追蹤 |
| STC=Fh | abort current operation | 先寫 result 再清 current |

**說明性範例。** 讀完整 LID 06h：564÷4=141 dwords，NUMD=141−1=140=008Ch。RAE=0、LSP=0、LID=06h，因此 CDW10=008C0006h。若 RDS1.DSTS=17h，DSTC=1h 是 short、DSTR=7h 才允許讀 SEGN。

**常見誤解／Debug。** FLBA 非零不是有效證據。先解 DSTR，再查 FVLD／NSIDVLD，最後才套 NVM Command Set bytes 23:16 的 FLBA 語意；同時保存 raw 28-byte entry。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.14.2.1, 8.1.8，文件頁 353-358, 614，PDF 頁 379-384, 640; NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 199，PDF 頁 225; NVME-BASE-2.4 Rev. 2.4，§5.2.6，文件頁 199-200，PDF 頁 225-226; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 229-230，PDF 頁 255-256; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 229-232，PDF 頁 255-258; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.7，文件頁 231-232，PDF 頁 257-258; NVME-NVM-CS-1.3 Rev. 1.3，§4.1.4.3，文件頁 76，PDF 頁 76

**關聯 Figure：** Figure 176, Figure 177, Figure 178, Figure 179, Figure 180, Figure 203, Figure 204, Figure 205, Figure 206, Figure 207, Figure 208, Figure 209, Figure 218, Figure 219, Figure 111, Figure 700, Figure 701

### Module 03: 先把三種容量與兩種 granularity 換到同一個 byte model

**解釋。** NSZE、NCAP、NUSE 的單位是 logical blocks；NSG、NCG 的單位是 bytes；controller 實際消耗的 NVM capacity 又可能按 allocation unit 向上取整。比較前必須先乘上選定 LBA size。NSZE≥NCAP≥NUSE 是合法性關係，NSG／NCG divisibility 則是減少浪費的 hint，不能混成同一種 gate。

```text
讀 LBA format
  ↓
NSZE／NCAP／NUSE blocks
  ↓
乘 LBA bytes
  ↓
檢查 NSG／NCG 整除
  ↓
估算 allocation rounding
  ↓
記錄 addressable 與 consumed
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| NSZE | logical blocks | LBA 0..NSZE−1 |
| NCAP | logical blocks | 最大可配置容量 |
| NUSE | logical blocks | THINP=1 時需追蹤 |
| NSG／NCG | bytes | preferred hint，不是單獨 abort gate |

**說明性範例。** LBA=4 KiB、NSG=1 MiB、NCG=2 MiB。NSZE=NCAP=1024 代表 4 MiB，4 MiB 可整除兩個 hints，且為 fully provisioned。NSZE=NCAP=1000 代表 3,906.25 KiB，無法整除 hints；可能浪費 allocation capacity，但 otherwise-valid create 仍不能只因這點 abort。

**常見誤解／Debug。** 最常見錯誤是拿 NSZE=1024 直接除 NSG=1 MiB，或把 granularity violation 當 Invalid Field。工作紙要明列 raw blocks、LBA bytes、converted bytes、remainder 與 controller allocation unit。

**支援來源：** NVME-NVM-CS-1.3 Rev. 1.3，§2.1.1，文件頁 13-14，PDF 頁 13-14; NVME-NVM-CS-1.3 Rev. 1.3，§2.1.1，文件頁 13，PDF 頁 13; NVME-BASE-2.4 Rev. 2.4，§8.1.17，文件頁 661，PDF 頁 687; NVME-NVM-CS-1.3 Rev. 1.3，§5.8，文件頁 165，PDF 頁 165; NVME-NVM-CS-1.3 Rev. 1.3，§5.8，文件頁 165，PDF 頁 165

**關聯 Figure：** Figure 123, Figure 132, Figure 133

### Module 04: Create payload：Base envelope 包住 NVM-specific 512 bytes

**解釋。** Base Figure 448 定義 4096-byte envelope，NVM Command Set Figure 134 只定義前 768 bytes 中的 NVM 欄位與 Placement Handle List。Host 先以 SEL／CSI 決定 operation 與 command set，再填 NSZE、NCAP、format、protection、sharing 與 group IDs。Reserved areas 要清零，Protection Information 與 FDP 又各有獨立 capability gate。

```text
SEL=Create、CSI=00h
  ↓
配置 4096-byte zeroed buffer
  ↓
填 NSZE／NCAP／FLBAS
  ↓
填 DPS／NMIC／group IDs
  ↓
驗證 LBSTM／NPHNDLS
  ↓
DPTR＋SQE snapshot
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Base 0:511 | SIOCS | NVM-specific create data |
| Base 512:1023 | Reserved | host 清 0 |
| Base 1024:4095 | Vendor Specific | 沒有來源定義就不猜 |
| NVM 512:767 | Placement Handle List | 只在 FDP enable 時驗證 |

**說明性範例。** 建立 4 MiB namespace：LBA=4096 bytes、NSZE=NCAP=1024，因此 bytes 7:0 與 15:8 都寫 0000000000000400h。NVMSETID=0、ENDGID=5 表示由 Endurance Group 5 內選 NVM Set；反過來 NVMSETID=7、ENDGID=0 是 Invalid Field。

**常見誤解／Debug。** 不要只 dump Figure 134 的欄位值。Debug 還要保存 host 使用的 LBA format capability、LBAFEE、Figure 127 masking limits、FDP enable state、完整 4096-byte buffer 與 reserved-byte scan。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.25，文件頁 446-448，PDF 頁 472-474; NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6.4，文件頁 111-113，PDF 頁 111-113; NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6.2，文件頁 110，PDF 頁 110; NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6.3，文件頁 110-111，PDF 頁 110-111; NVME-BASE-2.4 Rev. 2.4，§8.1.17，文件頁 661，PDF 頁 687

**關聯 Figure：** Figure 36, Figure 93, Figure 127, Figure 134, Figure 445, Figure 446, Figure 447, Figure 448

### Module 05: Namespace lifecycle：Create 只建立 object，Attach 才建立 access

**解釋。** Create、Attach、Detach、Delete 分別改變兩個狀態維度：namespace 是否 allocated，以及某 controller 是否 attached。Create CQE.DW0 回 NSID 後，object 已 allocated 但所有 controller 都未 attached；Attach 的 Controller List 才建立 access。Detach 不刪容量，Delete 才使 NSID unallocated。

```text
Unallocated NSID
  ↓
Create→allocated/unattached
  ↓
CQE.DW0 保存 NSID
  ↓
Attach→active on controller
  ↓
Detach→inactive on controller
  ↓
Delete→unallocated
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Create | object／capacity | 不自動 attach |
| Attach | access relationship | Controller List 可含多個 CNTLID |
| Detach | controller-local active state | namespace 仍 allocated |
| Delete | subsystem inventory | NSID 變 unallocated |

**說明性範例。** Create 回 NSID=7。Controller List 的 NUMCIDS 與 entries 指定 controllers 3、5；Attach 成功後 NSID 7 對 3、5 active。再只 detach controller 3，NSID 7 對 3 inactive、對 5 仍 active，namespace 本身仍 allocated。

**常見誤解／Debug。** NSID 數值相同不代表每個 controller 的 active state 相同。inventory 與 I/O trace 都要帶 controller ID；attach limit 還要分開核對 Domain MAXDNA 與 per-controller MAXCNA。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§8.1.17，文件頁 660，PDF 頁 686; NVME-BASE-2.4 Rev. 2.4，§8.1.17，文件頁 660，PDF 頁 686; NVME-BASE-2.4 Rev. 2.4，§5.2.24，文件頁 444-445，PDF 頁 470-471; NVME-BASE-2.4 Rev. 2.4，§5.2.24，文件頁 444-445，PDF 頁 470-471; NVME-BASE-2.4 Rev. 2.4，§5.2.25, 8.1.17.1，文件頁 446-448, 662，PDF 頁 472-474, 688

**關聯 Figure：** Figure 139, Figure 338, Figure 442, Figure 443, Figure 444, Figure 450

### Module 06: Delete 與 Restore Default：先清空 inventory，再跨 configuration boundary

**解釋。** Delete all 與 Restore Default 是兩個不同 operation。NSID=FFFFFFFFh 的 Delete All 在零個 namespaces 時也成功；Restore Default 則要求 RDNCS capability、SEL=2h，以及 subsystem 中已不存在任何 namespace。成功前 controller 套用 current active firmware image defaults 並設 DNCS=1。

```text
先 detach 所有 controllers
  ↓
Delete NSID 或 FFFFFFFFh
  ↓
確認 Allocated list 為空
  ↓
RDNCS=1 gate
  ↓
SEL=2h Restore
  ↓
DNCS=1＋重新 Identify
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Delete one | NSID=target | 成功後 object 消失 |
| Delete all | NSID=FFFFFFFFh | zero namespace 仍成功 |
| Restore | SEL=2h、NSID ignored | 剩餘 namespace→Sequence Error |
| Post-condition | DNCS=1 | 仍要重新 Identify actual defaults |

**說明性範例。** 先 detach NSID 7，再 Delete 7；讀 Allocated Namespace ID list 確認為空。若 RDNCS=1，送 SEL=2h、NSID=0。CQE success 後讀 DNCS=1，最後重新列舉 default namespaces；DNCS 是狀態證據，不是 default layout 的完整描述。

**常見誤解／Debug。** 不能用 Delete All CQE 直接推論 Restore 已完成，也不能只看 DNCS 猜 default NSZE／format。每一步都保存 operation selector、inventory snapshot、CQE 與 post-Identify。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.25, 8.1.17.1，文件頁 446, 448, 662，PDF 頁 472, 474, 688; NVME-BASE-2.4 Rev. 2.4，§5.2.25.1，文件頁 447-448，PDF 頁 473-474; NVME-BASE-2.4 Rev. 2.4，§8.1.17.1-8.1.17.2，文件頁 662-663，PDF 頁 688-689

**關聯 Figure：** Figure 304, Figure 338, Figure 446, Figure 449, Figure 474

### Module 07: Namespace event：通知只說 inventory 變了，Identify 才說變成什麼

**解釋。** Attached 與 Allocated Namespace Attribute Changed notices 對應不同 inventory。Create 通常改 Allocated list；Attach／Detach 改 Active list；Delete 可能同時改兩者。event code 不是新清單本身，因此 host 收到 AEN 後要依 CNS 重新 Identify。Delete reporting 還要分辨 processing controller 與其他 controllers。

```text
Host 預先提交 AER
  ↓
Create／Attach／Detach／Delete
  ↓
controller 更新 inventory
  ↓
AEN CQE posted
  ↓
host 依 CNS 重新 Identify
  ↓
比較 before／after list
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| CNS 02h | Active Namespace ID list | Attached notice |
| CNS 10h | Allocated Namespace ID list | Allocated notice |
| Create | Allocated change | 新 NSID 尚未 active |
| Delete | Allocated＋可能 Active | processing controller 規則不同 |

**說明性範例。** Controller 3 處理 attached NSID 7 的 Delete。其他已啟用 notice 的 controllers 依 §8.1.17.2 回報；processing controller 的要求不同。host 不應只計算 event 數量，而要為每個 controller 保存 before/after Active 與 Allocated lists。

**常見誤解／Debug。** 常見誤解是把 AEN 當成 inventory delta。AEN 只觸發 refresh；真正 authoritative data 是後續 Identify result。若漏 event，也可由 before/after inventory 差異定位，但不能反向捏造未收到的通知。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§8.1.17，文件頁 660，PDF 頁 686; NVME-BASE-2.4 Rev. 2.4，§8.1.17.1-8.1.17.2，文件頁 662-663，PDF 頁 688-689; NVME-BASE-2.4 Rev. 2.4，§5.2.25, 8.1.17.1，文件頁 446-448, 662，PDF 頁 472-474, 688

**關聯 Figure：** Figure 155, Figure 474

### Module 08: End-to-End：把 capacity、command、object、attachment 與 evidence 放在同一條 timeline

**解釋。** Namespace bug 很少只是一個欄位錯。create 前的 capability snapshot、4096-byte payload、CQE.DW0、Controller List、attach limits、events 與 post-Identify 必須能串回同一個 NSID 與 controller set。Debug 不從最後的 I/O failure 猜原因，而是找第一個不一致 boundary。

```text
Capability／capacity snapshot
  ↓
raw Create SQE＋buffer
  ↓
CQE.DW0 returned NSID
  ↓
raw Attach SQE＋Controller List
  ↓
AEN＋Identify refresh
  ↓
I/O／detach／delete outcome
```

#### 比較：這些概念差在哪裡

| 項目 | 它回答什麼 | Engineer 注意事項 |
|---|---|---|
| Create Invalid Format | FLBAS／DPS／LBSTM／LBAFEE | 先找 format gate |
| Insufficient Capacity | NSZE／NCAP、unallocated bytes、group IDs | 分 logical 與 consumed |
| Attach limit | MAXDNA／MAXCNA＋before counts | Domain 與 controller 分開 |
| I/O inactive NSID | Attach CQE、Active list、controller ID | Create success 不夠 |

**說明性範例。** 案例：Create 回 NSID 7，Attach 卻回 27h。先查 controller 5 的 MAXCNA 與 Domain MAXDNA before-count；若 per-controller 已達上限，就不應修改 create payload或重送 I/O。正確 recovery 是選別的 controller、detach 其他 namespace，或停止並回報 capacity policy。

**常見誤解／Debug。** 不要只記 human-readable status。保存 SCT／SC／DNR、raw SQE、buffer hash、returned NSID、controller list、timestamp 與 before/after inventories，才能重算是哪一個 gate 拒絕。

**支援來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.24-5.2.25，文件頁 445, 448，PDF 頁 471, 474; NVME-BASE-2.4 Rev. 2.4，§5.2.24-5.2.25, 8.1.17.1，文件頁 444-448, 661-663，PDF 頁 470-474, 687-689; NVME-BASE-2.4 Rev. 2.4，§5.2.24，文件頁 444-445，PDF 頁 470-471; NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6.2，文件頁 110，PDF 頁 110; NVME-NVM-CS-1.3 Rev. 1.3，§4.1.6.3，文件頁 110-111，PDF 頁 110-111

**關聯 Figure：** Figure 123, Figure 127, Figure 134, Figure 139, Figure 338, Figure 442, Figure 443, Figure 444, Figure 445, Figure 446, Figure 447, Figure 448, Figure 449, Figure 450

## 可追溯的規格重點

前面的 Mental Model 解釋因果；本節保留每個可追溯結論與 normative 強度，供講者備註與審查。

### 1. 先確認 Self-test capability 與 concurrency scope

<!-- claim:BASENSMGMT-SELFTEST-GATE -->

啟動 Device Self-test 前先讀 Identify Controller：OACS.DSTS 判斷 command 是否支援；EDSTT 是 extended operation 在 power state 0 的名目分鐘數；DSTO.SDSO 決定同時只有一個 subsystem-wide operation，或每個 controller 各一個。三者分別是支援、時間與 concurrency scope。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, 文件頁 353-358, 614, PDF 頁 379-384, 640

### 2. NSID 決定 Self-test 涵蓋範圍

<!-- claim:BASENSMGMT-SELFTEST-NSID -->

Device Self-test 由收到 command 的 controller 執行。NSID=00000000h 只測 controller；00000001h～FFFFFFFEh 指定一個 active namespace；FFFFFFFFh 包含提交當下該 controller 可存取的所有 attached namespaces。invalid 與 inactive NSID 是不同錯誤。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 199, PDF 頁 225

### 3. STC 與 CDW15 的命令編碼

<!-- claim:BASENSMGMT-SELFTEST-STC -->

CDW10.STC[3:0] 選動作：1h=short、2h=extended、3h=Host-Initiated Refresh、Eh=vendor specific、Fh=abort；其餘 encoding reserved。只有 STC=Eh 時 CDW15.DSTP 才是 vendor specific，其他 STC 下 CDW15 reserved。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 199-200, PDF 頁 225-226

### 4. operation in progress 的命令矩陣

<!-- claim:BASENSMGMT-SELFTEST-INPROGRESS -->

已有 operation 時，再送 short、extended 或 Host-Initiated Refresh 必須以 Device Self-test in Progress 中止；STC=Fh 則依序中止目前 operation、建立最新 result、清除 current status，再成功完成 abort command。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 200, PDF 頁 226

### 5. CQE 不等於背景測試完成

<!-- claim:BASENSMGMT-SELFTEST-COMPLETION -->

Device Self-test 的 Admin CQE 只證明啟動或中止動作已被處理，不代表背景測試完成。software 必須把 command CQE、LID 06h current state 與最後 result entry 當成三個不同時間點。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 201, PDF 頁 227

### 6. 背景測試的 suspend／resume 契約

<!-- claim:BASENSMGMT-SELFTEST-BACKGROUND -->

Device Self-test 是由 vendor-specific segments 組成的背景工作。若處理另一個 command 必須暫停測試，controller 必須（shall）依序 suspend self-test、處理並完成該 command、再 resume self-test；可同時處理哪些 command 仍由 vendor 決定。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.8, 文件頁 614, PDF 頁 640

### 7. short 與 extended 的 reset 差異

<!-- claim:BASENSMGMT-SELFTEST-TIMING -->

short operation 應（should）在兩分鐘內完成，Controller Level Reset 會中止；extended operation 應在 EDSTT 內完成，必須跨 Controller Level Reset 與 power restoration 持續並於之後 resume。兩種測試不能共用同一套 reset 預期。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, 文件頁 615-616, PDF 頁 641-642

### 8. Format、sanitize 與 abort 條件

<!-- claim:BASENSMGMT-SELFTEST-ABORTS -->

short 與 extended 都會被適用的 Format NVM、sanitize start 或 STC=Fh 中止，namespace 從 inventory 移除時則可能（may）中止。Figure 701 顯示必須同時看 Format NSID、secure-erase 選項與 Self-test NSID。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, 文件頁 615-616, PDF 頁 641-642

### 9. 564-byte LID 06h command 計算

<!-- claim:BASENSMGMT-SELFTEST-LOG-COMMAND -->

完整讀取 LID 06h 使用 564 bytes=141 dwords，因此 0's-based NUMD=140=008Ch；LID=06h、LSP=0、LPOL/LPOU=0、OT=0、CSI=0、UIDX=0。RAE=0 時 CDW10=008C0006h。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, 文件頁 213-216, PDF 頁 239-242

### 10. current operation 與完成百分比

<!-- claim:BASENSMGMT-SELFTEST-CURRENT -->

LID 06h byte 0 的 DSTOS 表示目前 operation，byte 1 的 DSTCS[6:0] 是完成百分比；DSTOS=0 時 host 應忽略 DSTCS。operation 完成或中止時，controller 必須先建立 result entry，再把 in-progress status 清為 0。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-230, PDF 頁 255-256

### 11. 20 筆 newest-first result history

<!-- claim:BASENSMGMT-SELFTEST-HISTORY -->

LID 06h 保留 20 筆、每筆 28 bytes 的結果，RDS1 是最新一筆。DSTS 高 nibble DSTC 記原始 self-test code，低 nibble DSTR 記完成或中止原因；只有 DSTR=7h 時 SEGN 才可解讀。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-232, PDF 頁 255-258

### 12. 先驗證 validity bit 再讀欄位

<!-- claim:BASENSMGMT-SELFTEST-VALIDITY -->

VDINFO 的 NSIDVLD、FVLD、SCTVLD、SCVLD 是四個獨立 validity gates。NSID、FLBA、STCT、STC 只有在對應 bit=1 時才可讀；parser 不得以欄位非零猜測有效。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 231-232, PDF 頁 257-258

### 13. NVM Command Set 補完 FLBA 語意

<!-- claim:BASENSMGMT-SELFTEST-NVM-FLBA -->

NVM Command Set 1.3 將 result bytes 23:16 定義為造成失敗的 logical block address。若多個 logical blocks 失敗，只回其中一個，而且僅在 FVLD=1 時有效。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, 文件頁 76, PDF 頁 76

### 14. NSZE、NCAP、NUSE 的容量不等式

<!-- claim:BASENSMGMT-CAPACITY-MODEL -->

Namespace Size（NSZE）是 LBA 0 到 n−1 的總 logical blocks；Namespace Capacity（NCAP）是任一時點最多可配置的 blocks；Namespace Utilization（NUSE）是目前已配置 blocks。永遠遵守 NSZE ≥ NCAP ≥ NUSE。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, 文件頁 13-14, PDF 頁 13-14

### 15. THINP 決定 NCAP／NUSE 回報責任

<!-- claim:BASENSMGMT-THIN-PROVISIONING -->

NSFEAT.THINP=1 時，controller 可（may）回報 NCAP<NSZE，並必須（shall）追蹤 NUSE。THINP=0 時，controller 必須回報 NCAP=NSZE，且可讓 NUSE 永遠等於 NCAP。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, 文件頁 13, PDF 頁 13

### 16. 完整 capability 是 Manage 加 Attach

<!-- claim:BASENSMGMT-NSMGMT-CAPABILITY -->

完整 Namespace Management capability 由 Namespace Management command 與 Namespace Attachment command 組成。支援時 controller 必須支援兩者、設 OACS.NMS=1、支援 Attached Namespace Attribute Changed event；Allocated event 為 should，Namespace Granularity 與 Restore Default 為 may。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686

### 17. allocated、active、inactive、unallocated

<!-- claim:BASENSMGMT-NSID-LIFECYCLE -->

create 成功後 namespace 已 allocated 但尚未 attached，因此對 controller 尚非 active。detach 使該 controller 上的 NSID 變 inactive；delete 使 subsystem 中的 NSID 變 unallocated。受影響的 outstanding 或後續 commands 依 inactive NSID 處理。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686

### 18. create 前的 capability／capacity 盤點

<!-- claim:BASENSMGMT-CREATE-PREFLIGHT -->

create 前先以 NSID=FFFFFFFFh、CNS=00h 讀 common namespace capabilities；若支援，再用 CNS=16h 讀 Namespace Granularity，並確認可用 capacity。這三步完成後才建立 4096-byte create buffer。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17.1, 文件頁 661-662, PDF 頁 687-688

### 19. Base 4096-byte create envelope

<!-- claim:BASENSMGMT-CREATE-BASE-COMMAND -->

Create 使用 NSID=0、SEL=0h 與 CSI=00h（NVM Command Set）。DPTR 指向 4096-byte data structure：bytes 0:511 是 I/O Command Set specific、512:1023 reserved、1024:4095 vendor specific。reserved bytes 由 host 清為 0。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 文件頁 446-448, PDF 頁 472-474

### 20. NVM host-specified create fields

<!-- claim:BASENSMGMT-CREATE-NVM-PAYLOAD -->

NVM create payload 的主要 host-specified fields 是 NSZE、NCAP、FLBAS、DPS、NMIC、ANAGRPID、NVMSETID、ENDGID、LBSTM、NPHNDLS 與 Placement Handle List。成功 create 後，namespace 依這些屬性格式化；未使用的 reserved fields 應清為 0。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.4, 文件頁 111-113, PDF 頁 111-113

### 21. Protection Information 與 LBSTM gates

<!-- claim:BASENSMGMT-PROTECTION-VALIDATION -->

End-to-end Data Protection 設定在 create 時套用。LBAFEE 未啟用時，特定 16-bit STS 非零、32-bit 或 64-bit Guard Protection Information 組合必須以 Invalid Namespace or Format 中止；LBSTM 不符合 Figure 127 capability 時則回 Invalid Field in Command。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, 文件頁 110, PDF 頁 110

### 22. FDP Placement Handle validation

<!-- claim:BASENSMGMT-FDP-VALIDATION -->

只有指定 Endurance Group 已啟用 Flexible Data Placement（FDP）且 SEL=Create 時，NPHNDLS 與 Placement Handle List 才參與驗證。NPHNDLS 不得大於支援的 Reclaim Unit Handles 或 128；重複、越界、格式不相容或無可用 handle 會導向 Invalid Placement Handle List 或 Invalid Format。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, 文件頁 110-111, PDF 頁 110-111

### 23. NVMSETID／ENDGID 決策矩陣

<!-- claim:BASENSMGMT-GROUP-SELECTION -->

NVMSETID／ENDGID 的決策矩陣為：兩者 0 由 controller 選兩者；NVMSETID=0、ENDGID≠0 時由指定 Endurance Group 內選 NVM Set；NVMSETID≠0、ENDGID=0 必須 Invalid Field；兩者非 0 時只有該 NVM Set 確實屬於指定 Endurance Group 才可配置。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 661, PDF 頁 687

### 24. requested size 不等於 capacity consumption

<!-- claim:BASENSMGMT-ALLOCATION-ROUNDING -->

controller 可（may）按內部 allocation unit 把實際消耗容量向上取整。Spec 範例中，32 blocks×4 KiB=128 KiB 的 namespace，在 1 MiB allocation unit 下可消耗 1 MiB；因此 capacity consumption 不一定等於 logical block size×block count。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 661, PDF 頁 687

### 25. NSG／NCG 是配置提示而非合法性門檻

<!-- claim:BASENSMGMT-GRANULARITY-HINTS -->

Namespace Granularity 的 NSG 與 NCG 都是 byte-unit hints。若 NSZE×LBA size 可整除 NSG、NCAP×LBA size 可整除 NCG 且 NSZE=NCAP，配置為 fully provisioned 且全部容量可由 LBA 定址；不符合 hint 可能浪費容量，但 otherwise-valid create 不得只因違反 hint 被中止。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.8, 文件頁 165, PDF 頁 165

### 26. Controller List 建立 access relationship

<!-- claim:BASENSMGMT-ATTACH-COMMAND -->

Namespace Attachment 的 DPTR 指向 4096-byte Controller List；SEL=0h attach、SEL=1h detach。以 PRP 指向此 buffer 時不得使用 PRP List，因 buffer 不可跨越超過一個 memory-page boundary。attach／detach 狀態跨所有 reset events 保留。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, 文件頁 444-445, PDF 頁 470-471

### 27. MAXDNA 與 MAXCNA 是兩層 limits

<!-- claim:BASENSMGMT-ATTACH-LIMITS -->

attach 前分別核對 Domain aggregate MAXDNA 與每個 I/O controller 的 MAXCNA；非零 limit 被超過時回 Namespace Attachment Limit Exceeded。還要核對 I/O Command Set support／enable state，不能把所有 attach failure 都歸成同一種 status。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, 文件頁 444-445, PDF 頁 470-471

### 28. CQE.DW0 回 NSID，但尚未 attached

<!-- claim:BASENSMGMT-CREATE-COMPLETION -->

Create 成功時 controller 選擇可用 NSID，CQE.DW0 回傳該 NSID；此刻 namespace 尚未 attached。software 必須先保存 returned NSID，再以 Namespace Attachment 建立 controller access，不能在 create CQE 後直接送 I/O。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446-448, 662, PDF 頁 472-474, 688

### 29. detach 後再 delete 的可控流程

<!-- claim:BASENSMGMT-DELETE -->

Delete 的 NSID 指定已建立 namespace；FFFFFFFFh 表示 delete all，即使目前零個 namespaces 也成功。delete 會使 namespace 從 subsystem 消失並具有 detach side effect；host 應先 detach 所有 controllers，讓 event 與 outstanding-I/O 行為更可控。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446, 448, 662, PDF 頁 472, 474, 688

### 30. RDNCS、delete-all 與 DNCS

<!-- claim:BASENSMGMT-RESTORE-DEFAULT -->

Restore Default 使用 SEL=2h，NSID 應為 0 且 controller 會忽略它。先讀 RDNCS，刪除 subsystem 中所有 namespaces，再送 restore；若仍有 namespace，回 Command Sequence Error。成功前 controller 必須套用 current active firmware image 的 default configuration 並設 DNCS=1。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25.1, 文件頁 447-448, PDF 頁 473-474

### 31. 用 command-specific status 定位 failure gate

<!-- claim:BASENSMGMT-COMMAND-STATUS -->

Debug 要保留 command-specific status：Attachment 可回 already attached 18h、private 19h、not attached 1Ah、Controller List invalid 1Ch、ANA attach failed 25h、limit 27h、I/O Command Set 29h／2Ah；Management 可回 Invalid Format 0Ah、insufficient capacity 15h、NSID unavailable 16h、thin provisioning unsupported 1Bh、ANA group invalid 24h。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, 文件頁 445, 448, PDF 頁 471, 474

### 32. AER 後重新 Identify inventory

<!-- claim:BASENSMGMT-NAMESPACE-EVENTS -->

create 改變 Allocated Namespace ID list；attach／detach 改變 Active Namespace ID list；delete 可能同時改變兩者。啟用對應 notice 時，host 收到 asynchronous event 後應重新 Identify，而不是只用 event code 猜新 inventory。§8.1.17.2 對處理 delete 的 controller 與其他 controllers 規定不同 event reporting。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, 文件頁 662-663, PDF 頁 688-689

### 33. 4 KiB LBA 的 NSG／NCG 計算

<!-- claim:BASENSMGMT-GRANULARITY-EXAMPLE -->

說明性範例：LBA=4 KiB、NSG=1 MiB（256 LBAs）、NCG=2 MiB（512 LBAs）。NSZE=NCAP=1024 同時滿足兩種 granularity；NSZE=1000、NCAP=1000 不滿足 NSG／NCG 整除，但若其他欄位都合法，controller 不得只因這個 hint violation 中止 create。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.8, 文件頁 165, PDF 頁 165

### 34. 從第一個生命週期邊界開始 Debug

<!-- claim:BASENSMGMT-END-TO-END-DEBUG -->

完整 trace 至少保存：OACS.NMS／limits、common Identify 與 granularity snapshot、4096-byte create buffer、raw SQE、CQE.DW0 NSID、Controller List、attach CQE、AER、重新 Identify 結果，以及 detach／delete 後的 inactive／unallocated 狀態。第一個不一致的 boundary 才是 Debug 起點。

**解釋。** 把本結論放回教學流程：先確認物件與 scope，再核對 capability 與 state，最後才轉成 software decision。欄位存在不等於功能已啟用，成功 completion 也不自動代表下一個 lifecycle 階段已完成。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, 8.1.17.1, 文件頁 444-448, 661-663, PDF 頁 470-474, 687-689

## Figure 索引

本報告介紹全部 39 張納入範圍的 Figure。100 分鐘簡報以 section 主線與必講 Figure 為主，其餘 Figure 仍完整保留作為附錄。其中 19 張位於主章節範圍外，但因指定正文直接引用而納入相依教學。

- [§4.1](#section-4-1)

- [§5.2](#section-5-2)

- [§8.1](#section-8-1)

- [引用相依 Figure（位於主章節範圍外）](#section-dependency)

## Figure／欄位表教學參考

本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。欄位與 keyword 索引來自本機核對過的 PDF。

<a id="section-4-1"></a>

### §4.1

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 111: Self-test Results Data Structure</strong></summary>

<!-- claim:BASENSMGMT-FIG-111-CLAIM figure-table:BASENSMGMT-FIG-111 -->

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

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 134: Namespace Management - Host Specified Fields</strong></summary>

<!-- claim:BASENSMGMT-FIG-134-CLAIM figure-table:BASENSMGMT-FIG-134 -->

**SPEC。** Figure 134〈Namespace Management - Host Specified Fields〉：定義〈Namespace Management - Host Specified Fields〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NSZE, NCAP, FLBAS, DPS, NMIC, ANAGRPID, NVMSETID, ENDGID, LBSTM, NPHNDLS, Placement Handle List。

#### 這張 Figure 在完整流程中的位置

Figure 134 位於 §4.1.6.4，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NSZE 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSZE]
          ↓
[擷取欄位: NCAP] → [套用編碼: FLBAS]
                                      ↓
[驗證證據: DPS]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSZE` | Namespace Size，namespace 的總 logical block 數，LBA 範圍為 0 到 NSZE−1。 |
| `NCAP` | Namespace Capacity，任一時點最多可配置給 namespace 的 logical blocks。 |
| `FLBAS` | Formatted LBA Size，選擇 namespace 使用的 LBA format，並包含 metadata placement 相關控制。 |
| `DPS` | End-to-end Data Protection Type Settings，create 時選擇 Protection Information type 與位置的欄位。 |
| `NMIC` | Namespace Multi-path I/O and Namespace Sharing Capabilities，create 時宣告 namespace sharing／multipath 屬性的欄位。 |
| `ANAGRPID` | ANA Group Identifier，namespace 所屬 Asymmetric Namespace Access group 的 identifier；create 值 0 讓 controller 選擇。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.1.6.4。
2. 依圖中指定的寬度與位置解碼 NSZE；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NCAP 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §4.1.6.4 如何排列 NSZE、NCAP 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.1.6.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 134 對應的 raw value 或 buffer，標出包含 NSZE 的 bytes 並解碼，再獨立核對 NCAP。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NSZE，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NSZE 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NCAP 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NSZE, NCAP, FLBAS, DPS, NMIC, ANAGRPID, NVMSETID, ENDGID, LBSTM, NPHNDLS, Placement Handle List

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.4, Figure 134, 文件頁 112-113, PDF 頁 112-113

</details>

<a id="section-5-2"></a>

### §5.2

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 176: Device Self-test Namespace Test Action</strong></summary>

<!-- claim:BASENSMGMT-FIG-176-CLAIM figure-table:BASENSMGMT-FIG-176 -->

**SPEC。** Figure 176〈Device Self-test Namespace Test Action〉：呈現〈Device Self-test Namespace Test Action〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NSID 00000000h, active NSID, NSID FFFFFFFFh。

#### 這張 Figure 在完整流程中的位置

Figure 176 位於 §5.2.6，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NSID 00000000h 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSID 00000000h]
          ↓
[擷取欄位: active NSID] → [套用編碼: NSID FFFFFFFFh]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSID 00000000h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `active NSID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NSID FFFFFFFFh` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.6。
2. 依圖中指定的寬度與位置解碼 NSID 00000000h；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 active NSID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
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
| 這張圖回答 | §5.2.6 如何排列 NSID 00000000h、active NSID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.6 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 176 對應的 raw value 或 buffer，標出包含 NSID 00000000h 的 bytes 並解碼，再獨立核對 active NSID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 active NSID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NSID 00000000h, active NSID, NSID FFFFFFFFh

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 176, 文件頁 199, PDF 頁 225

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 177: Device Self-test - Command Dword 10</strong></summary>

<!-- claim:BASENSMGMT-FIG-177-CLAIM figure-table:BASENSMGMT-FIG-177 -->

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
<summary><strong>NVME-BASE-2.4 — Figure 178: Device Self-test - Command Dword 15</strong></summary>

<!-- claim:BASENSMGMT-FIG-178-CLAIM figure-table:BASENSMGMT-FIG-178 -->

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
<summary><strong>NVME-BASE-2.4 — Figure 179: Device Self-test - Command Processing</strong></summary>

<!-- claim:BASENSMGMT-FIG-179-CLAIM figure-table:BASENSMGMT-FIG-179 -->

**SPEC。** Figure 179〈Device Self-test - Command Processing〉：呈現〈Device Self-test - Command Processing〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：self-test in progress, abort, result creation。

#### 這張 Figure 在完整流程中的位置

Figure 179 位於 §5.2.6，在本流程中是「queue」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 self-test in progress 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 queue／command flow 圖。先標 host 與 controller 的 ownership，再追 head、tail、phase 或 arbitration 的改變；箭頭代表狀態或 ownership 轉移，不自動代表 command 已完成。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: self-test in progress]
          ↓
[擷取欄位: abort] → [套用編碼: result creation]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `self-test in progress` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `abort` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `result creation` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.6。
2. 依圖中指定的寬度與位置解碼 self-test in progress；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 abort 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
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
| 這張圖回答 | §5.2.6 如何排列 self-test in progress、abort 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.6 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 179 對應的 raw value 或 buffer，標出包含 self-test in progress 的 bytes 並解碼，再獨立核對 abort。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 abort 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** self-test in progress, abort, result creation

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 179, 文件頁 200, PDF 頁 226

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 180: Device Self-test - Command Specific Status Values</strong></summary>

<!-- claim:BASENSMGMT-FIG-180-CLAIM figure-table:BASENSMGMT-FIG-180 -->

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
<summary><strong>NVME-BASE-2.4 — Figure 218: Device Self-test Log Page</strong></summary>

<!-- claim:BASENSMGMT-FIG-218-CLAIM figure-table:BASENSMGMT-FIG-218 -->

**SPEC。** Figure 218〈Device Self-test Log Page〉：把〈Device Self-test Log Page〉連到 Self-test 證據路徑或 namespace lifecycle。 先確認物件與 lifecycle state，再解碼 DSTOS, DSTCS, RDS1-RDS20, 564 bytes，最後以 CQE、log、event 或 Identify snapshot 驗證下一個 transition。

#### 這張 Figure 在完整流程中的位置

Figure 218 位於 §5.2.13.1.7，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DSTOS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DSTOS]
          ↓
[擷取欄位: DSTCS] → [套用編碼: RDS1-RDS20]
                                      ↓
[驗證證據: 564 bytes]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DSTOS` | Device Self-test Operation Status，LID 06h 中表示目前 operation 類型的 nibble。 |
| `DSTCS` | Device Self-test Completion Status，LID 06h 中的 0 到 100 完成百分比。 |
| `RDS1-RDS20` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
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

**來源欄位索引：** DSTOS, DSTCS, RDS1-RDS20, 564 bytes

**來源 keyword 索引：** `shall not`, `shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, Figure 218, 文件頁 230, PDF 頁 256

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 219: Self-test Result Data Structure</strong></summary>

<!-- claim:BASENSMGMT-FIG-219-CLAIM figure-table:BASENSMGMT-FIG-219 -->

**SPEC。** Figure 219〈Self-test Result Data Structure〉：定義〈Self-test Result Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DSTC, DSTR, SEGN, VDINFO, NSID, FLBA, STCT, STC。

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
| `NSID` | Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。 |
| `FLBA` | Failing LBA，NVM Command Set 定義為造成 self-test failure 的其中一個 logical block address。 |

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

**來源欄位索引：** DSTC, DSTR, SEGN, VDINFO, NSID, FLBA, STCT, STC

**來源 keyword 索引：** `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, Figure 219, 文件頁 231-232, PDF 頁 257-258

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 442: Namespace Attachment - Data Pointer</strong></summary>

<!-- claim:BASENSMGMT-FIG-442-CLAIM figure-table:BASENSMGMT-FIG-442 -->

**SPEC。** Figure 442〈Namespace Attachment - Data Pointer〉：呈現〈Namespace Attachment - Data Pointer〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：DPTR, Controller List, one page boundary。

#### 這張 Figure 在完整流程中的位置

Figure 442 位於 §5.2.24，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DPTR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DPTR]
          ↓
[擷取欄位: Controller List] → [套用編碼: one page boundary]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DPTR` | Data Pointer，SQE 中指出 command data buffer 的欄位。 |
| `Controller List` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `one page boundary` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.24。
2. 依圖中指定的寬度與位置解碼 DPTR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Controller List 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 442 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.24 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.24 如何排列 DPTR、Controller List 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.24 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 442 對應的 raw value 或 buffer，標出包含 DPTR 的 bytes 並解碼，再獨立核對 Controller List。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 Controller List 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** DPTR, Controller List, one page boundary

**來源 keyword 索引：** `shall not`, `shall`, `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, Figure 442, 文件頁 445, PDF 頁 471

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 443: Namespace Attachment - Command Dword 10</strong></summary>

<!-- claim:BASENSMGMT-FIG-443-CLAIM figure-table:BASENSMGMT-FIG-443 -->

**SPEC。** Figure 443〈Namespace Attachment - Command Dword 10〉：定義 Namespace Attachment 在 CDW10 的 command-specific 欄位。 先定位 CDW10，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：SEL 0h Attach, SEL 1h Detach。

#### 這張 Figure 在完整流程中的位置

Figure 443 位於 §5.2.24，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SEL 0h Attach 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SEL 0h Attach]
          ↓
[擷取欄位: SEL 1h Detach] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SEL 0h Attach` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SEL 1h Detach` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.24。
2. 依圖中指定的寬度與位置解碼 SEL 0h Attach；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 SEL 1h Detach 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 443 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.24 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.24 如何排列 SEL 0h Attach、SEL 1h Detach 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.24 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 443 對應的 raw value 或 buffer，標出包含 SEL 0h Attach 的 bytes 並解碼，再獨立核對 SEL 1h Detach。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SEL 0h Attach，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SEL 0h Attach 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 SEL 1h Detach 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SEL 0h Attach, SEL 1h Detach

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, Figure 443, 文件頁 445, PDF 頁 471

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 444: Namespace Attachment - Command Specific Status Values</strong></summary>

<!-- claim:BASENSMGMT-FIG-444-CLAIM figure-table:BASENSMGMT-FIG-444 -->

**SPEC。** Figure 444〈Namespace Attachment - Command Specific Status Values〉：定義〈Namespace Attachment - Command Specific Status Values〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：status 18h-1Ch, status 25h, status 27h, status 29h-2Ah。

#### 這張 Figure 在完整流程中的位置

Figure 444 位於 §5.2.24，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 status 18h-1Ch 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: status 18h-1Ch]
          ↓
[擷取欄位: status 25h] → [套用編碼: status 27h]
                                      ↓
[驗證證據: status 29h-2Ah]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `status 18h-1Ch` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `status 25h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `status 27h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `status 29h-2Ah` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.24。
2. 依圖中指定的寬度與位置解碼 status 18h-1Ch；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 status 25h 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 444 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.24 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.24 如何排列 status 18h-1Ch、status 25h 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.24 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 444 對應的 raw value 或 buffer，標出包含 status 18h-1Ch 的 bytes 並解碼，再獨立核對 status 25h。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 status 18h-1Ch，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 status 18h-1Ch 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 status 25h 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** status 18h-1Ch, status 25h, status 27h, status 29h-2Ah

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, Figure 444, 文件頁 445, PDF 頁 471

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 445: Namespace Management - Data Pointer</strong></summary>

<!-- claim:BASENSMGMT-FIG-445-CLAIM figure-table:BASENSMGMT-FIG-445 -->

**SPEC。** Figure 445〈Namespace Management - Data Pointer〉：呈現〈Namespace Management - Data Pointer〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：DPTR, 4096-byte create buffer。

#### 這張 Figure 在完整流程中的位置

Figure 445 位於 §5.2.25，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DPTR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DPTR]
          ↓
[擷取欄位: 4096-byte create buffer] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DPTR` | Data Pointer，SQE 中指出 command data buffer 的欄位。 |
| `4096-byte create buffer` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.25。
2. 依圖中指定的寬度與位置解碼 DPTR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 4096-byte create buffer 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 445 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.25 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.25 如何排列 DPTR、4096-byte create buffer 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.25 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 445 對應的 raw value 或 buffer，標出包含 DPTR 的 bytes 並解碼，再獨立核對 4096-byte create buffer。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 4096-byte create buffer 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** DPTR, 4096-byte create buffer

**來源 keyword 索引：** `shall not`, `shall`, `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 445, 文件頁 446, PDF 頁 472

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 446: Namespace Management - Command Dword 10</strong></summary>

<!-- claim:BASENSMGMT-FIG-446-CLAIM figure-table:BASENSMGMT-FIG-446 -->

**SPEC。** Figure 446〈Namespace Management - Command Dword 10〉：定義 Namespace Management 在 CDW10 的 command-specific 欄位。 先定位 CDW10，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：SEL 0h Create, SEL 1h Delete, SEL 2h Restore。

#### 這張 Figure 在完整流程中的位置

Figure 446 位於 §5.2.25，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SEL 0h Create 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SEL 0h Create]
          ↓
[擷取欄位: SEL 1h Delete] → [套用編碼: SEL 2h Restore]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SEL 0h Create` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SEL 1h Delete` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SEL 2h Restore` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.25。
2. 依圖中指定的寬度與位置解碼 SEL 0h Create；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 SEL 1h Delete 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 446 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.25 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.25 如何排列 SEL 0h Create、SEL 1h Delete 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.25 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 446 對應的 raw value 或 buffer，標出包含 SEL 0h Create 的 bytes 並解碼，再獨立核對 SEL 1h Delete。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SEL 0h Create，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SEL 0h Create 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 SEL 1h Delete 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SEL 0h Create, SEL 1h Delete, SEL 2h Restore

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 446, 文件頁 446-447, PDF 頁 472-473

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 447: Namespace Management - Command Dword 11</strong></summary>

<!-- claim:BASENSMGMT-FIG-447-CLAIM figure-table:BASENSMGMT-FIG-447 -->

**SPEC。** Figure 447〈Namespace Management - Command Dword 11〉：定義 Namespace Management 在 CDW11 的 command-specific 欄位。 先定位 CDW11，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：CSI, NVM Command Set 00h。

#### 這張 Figure 在完整流程中的位置

Figure 447 位於 §5.2.25，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CSI 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CSI]
          ↓
[擷取欄位: NVM Command Set 00h] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CSI` | Command Set Identifier，選擇 command 或 log page 所套用的 I/O Command Set context。 |
| `NVM Command Set 00h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.25。
2. 依圖中指定的寬度與位置解碼 CSI；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NVM Command Set 00h 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 447 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.25 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.25 如何排列 CSI、NVM Command Set 00h 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.25 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 447 對應的 raw value 或 buffer，標出包含 CSI 的 bytes 並解碼，再獨立核對 NVM Command Set 00h。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 NVM Command Set 00h 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CSI, NVM Command Set 00h

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 447, 文件頁 447, PDF 頁 473

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 448: Namespace Management - Data Structure for Create</strong></summary>

<!-- claim:BASENSMGMT-FIG-448-CLAIM figure-table:BASENSMGMT-FIG-448 -->

**SPEC。** Figure 448〈Namespace Management - Data Structure for Create〉：定義〈Namespace Management - Data Structure for Create〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：SIOCS bytes 0:511, reserved bytes 512:1023, VS bytes 1024:4095。

#### 這張 Figure 在完整流程中的位置

Figure 448 位於 §5.2.25，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 SIOCS bytes 0:511 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: SIOCS bytes 0:511]
          ↓
[擷取欄位: reserved bytes 512:1023] → [套用編碼: VS bytes 1024:4095]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `SIOCS bytes 0:511` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `reserved bytes 512:1023` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `VS bytes 1024:4095` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.25。
2. 依圖中指定的寬度與位置解碼 SIOCS bytes 0:511；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 reserved bytes 512:1023 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 448 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.25 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.25 如何排列 SIOCS bytes 0:511、reserved bytes 512:1023 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.25 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 448 對應的 raw value 或 buffer，標出包含 SIOCS bytes 0:511 的 bytes 並解碼，再獨立核對 reserved bytes 512:1023。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 SIOCS bytes 0:511，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 SIOCS bytes 0:511 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 reserved bytes 512:1023 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** SIOCS bytes 0:511, reserved bytes 512:1023, VS bytes 1024:4095

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 448, 文件頁 447, PDF 頁 473

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 449: Namespace Management - Command Specific Status Values</strong></summary>

<!-- claim:BASENSMGMT-FIG-449-CLAIM figure-table:BASENSMGMT-FIG-449 -->

**SPEC。** Figure 449〈Namespace Management - Command Specific Status Values〉：定義〈Namespace Management - Command Specific Status Values〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Invalid Format, Insufficient Capacity, NSID Unavailable, Thin Provisioning Not Supported。

#### 這張 Figure 在完整流程中的位置

Figure 449 位於 §5.2.25，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Invalid Format 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Invalid Format]
          ↓
[擷取欄位: Insufficient Capacity] → [套用編碼: NSID Unavailable]
                                      ↓
[驗證證據: Thin Provisioning Not Supported]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Invalid Format` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Insufficient Capacity` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NSID Unavailable` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Thin Provisioning Not Supported` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.25。
2. 依圖中指定的寬度與位置解碼 Invalid Format；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Insufficient Capacity 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 449 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.25 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.25 如何排列 Invalid Format、Insufficient Capacity 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.25 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 449 對應的 raw value 或 buffer，標出包含 Invalid Format 的 bytes 並解碼，再獨立核對 Insufficient Capacity。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Invalid Format，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Invalid Format 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Insufficient Capacity 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Invalid Format, Insufficient Capacity, NSID Unavailable, Thin Provisioning Not Supported

**來源 keyword 索引：** `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 449, 文件頁 448, PDF 頁 474

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 450: Namespace Management - Completion Queue Entry Dword 0</strong></summary>

<!-- claim:BASENSMGMT-FIG-450-CLAIM figure-table:BASENSMGMT-FIG-450 -->

**SPEC。** Figure 450〈Namespace Management - Completion Queue Entry Dword 0〉：呈現〈Namespace Management - Completion Queue Entry Dword 0〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：CQE DW0, created NSID。

#### 這張 Figure 在完整流程中的位置

Figure 450 位於 §5.2.25，在本流程中是「queue」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CQE DW0 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 queue／command flow 圖。先標 host 與 controller 的 ownership，再追 head、tail、phase 或 arbitration 的改變；箭頭代表狀態或 ownership 轉移，不自動代表 command 已完成。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CQE DW0]
          ↓
[擷取欄位: created NSID] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CQE DW0` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `created NSID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.25。
2. 依圖中指定的寬度與位置解碼 CQE DW0；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 created NSID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 450 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.25 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.25 如何排列 CQE DW0、created NSID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.25 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 450 對應的 raw value 或 buffer，標出包含 CQE DW0 的 bytes 並解碼，再獨立核對 created NSID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CQE DW0，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CQE DW0 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 created NSID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CQE DW0, created NSID

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 450, 文件頁 448, PDF 頁 474

</details>

<a id="section-8-1"></a>

### §8.1

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 700: Example Device Self-test Operation (Informative)</strong></summary>

<!-- claim:BASENSMGMT-FIG-700-CLAIM figure-table:BASENSMGMT-FIG-700 -->

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
<summary><strong>NVME-BASE-2.4 — Figure 701: Format NVM command Aborting a Device Self-Test Operation</strong></summary>

<!-- claim:BASENSMGMT-FIG-701-CLAIM figure-table:BASENSMGMT-FIG-701 -->

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
<summary><strong>NVME-BASE-2.4 — Figure 36: Offset 0h: CAP - Controller Capabilities</strong></summary>

<!-- claim:BASENSMGMT-FIG-036-CLAIM figure-table:BASENSMGMT-FIG-036 -->

**SPEC。** Figure 36〈Offset 0h: CAP - Controller Capabilities〉：定義 offset 0h 的 CAP（Controller Capabilities），並指出軟體在該位置必須分別解碼的欄位。 先定位 CAP，再把 bit range 對到 access type、reset value 與欄位語意；來源欄位索引：CSS, active I/O Command Set。

#### 這張 Figure 在完整流程中的位置

Figure 36 位於 §3.1.4.1，在本流程中是「register」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 CSS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 register／property 欄位表。先由 base offset 定位，再核對 access width、reset value 與 bit range；最後才把 bit value 轉成狀態或能力。讀表時把整個 register snapshot 留著，避免只擷取單一 bit 而失去相鄰條件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: CSS]
          ↓
[擷取欄位: active I/O Command Set] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `CSS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `active I/O Command Set` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §3.1.4.1。
2. 依圖中指定的寬度與位置解碼 CSS；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 active I/O Command Set 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
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
| 這張圖回答 | §3.1.4.1 如何排列 CSS、active I/O Command Set 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §3.1.4.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 36 對應的 raw value 或 buffer，標出包含 CSS 的 bytes 並解碼，再獨立核對 active I/O Command Set。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 CSS，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 CSS 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 active I/O Command Set 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** CSS, active I/O Command Set

**來源 keyword 索引：** `shall not`, `shall`, `should`, `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, 文件頁 55-58, PDF 頁 81-84

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 93: Common Command Format</strong></summary>

<!-- claim:BASENSMGMT-FIG-093-CLAIM figure-table:BASENSMGMT-FIG-093 -->

**SPEC。** Figure 93〈Common Command Format〉：定義〈Common Command Format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：OPC, NSID, DPTR, CDW10-CDW15。

#### 這張 Figure 在完整流程中的位置

Figure 93 位於 §4.1.1，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 OPC 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: OPC]
          ↓
[擷取欄位: NSID] → [套用編碼: DPTR]
                                      ↓
[驗證證據: CDW10-CDW15]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `OPC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NSID` | Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。 |
| `DPTR` | Data Pointer，SQE 中指出 command data buffer 的欄位。 |
| `CDW10-CDW15` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.1.1。
2. 依圖中指定的寬度與位置解碼 OPC；縮寫本身不能用來猜 unit、reset value 或 encoding。
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
| 這張圖回答 | §4.1.1 如何排列 OPC、NSID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.1.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 93 對應的 raw value 或 buffer，標出包含 OPC 的 bytes 並解碼，再獨立核對 NSID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 NSID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** OPC, NSID, DPTR, CDW10-CDW15

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, 文件頁 140-142, PDF 頁 166-168

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 123: Identify - Identify Namespace Data Structure, NVM Command Set</strong></summary>

<!-- claim:BASENSMGMT-FIG-123-CLAIM figure-table:BASENSMGMT-FIG-123 -->

**SPEC。** Figure 123〈Identify - Identify Namespace Data Structure, NVM Command Set〉：定義〈Identify - Identify Namespace Data Structure, NVM Command Set〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NSZE, NCAP, NUSE, NSFEAT.THINP, FLBAS, DPS, NMIC。

#### 這張 Figure 在完整流程中的位置

Figure 123 位於 §4.1.5.1，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NSZE 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSZE]
          ↓
[擷取欄位: NCAP] → [套用編碼: NUSE]
                                      ↓
[驗證證據: NSFEAT.THINP]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSZE` | Namespace Size，namespace 的總 logical block 數，LBA 範圍為 0 到 NSZE−1。 |
| `NCAP` | Namespace Capacity，任一時點最多可配置給 namespace 的 logical blocks。 |
| `NUSE` | Namespace Utilization，目前已配置給 namespace 的 logical blocks。 |
| `NSFEAT.THINP` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FLBAS` | Formatted LBA Size，選擇 namespace 使用的 LBA format，並包含 metadata placement 相關控制。 |
| `DPS` | End-to-end Data Protection Type Settings，create 時選擇 Protection Information type 與位置的欄位。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.1.5.1。
2. 依圖中指定的寬度與位置解碼 NSZE；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NCAP 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §4.1.5.1 如何排列 NSZE、NCAP 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.1.5.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 123 對應的 raw value 或 buffer，標出包含 NSZE 的 bytes 並解碼，再獨立核對 NCAP。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NSZE，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NSZE 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NCAP 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NSZE, NCAP, NUSE, NSFEAT.THINP, FLBAS, DPS, NMIC

**來源 keyword 索引：** `shall not`, `shall`, `should`, `may`, `optional`, `reserved`

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1, Figure 123, 文件頁 85-87, PDF 頁 85-87

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 127: NVM Command Set I/O Command Set Specific Identify Namespace Data Structure</strong></summary>

<!-- claim:BASENSMGMT-FIG-127-CLAIM figure-table:BASENSMGMT-FIG-127 -->

**SPEC。** Figure 127〈NVM Command Set I/O Command Set Specific Identify Namespace Data Structure〉：定義〈NVM Command Set I/O Command Set Specific Identify Namespace Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：LBSTM, Storage Tag Masking Level, LBAFEE。

#### 這張 Figure 在完整流程中的位置

Figure 127 位於 §4.1.5.3，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 LBSTM 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LBSTM]
          ↓
[擷取欄位: Storage Tag Masking Level] → [套用編碼: LBAFEE]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LBSTM` | Logical Block Storage Tag Mask，create 時指定哪些 Storage Tag bits 被 mask 的 64-bit 欄位。 |
| `Storage Tag Masking Level` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `LBAFEE` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.1.5.3。
2. 依圖中指定的寬度與位置解碼 LBSTM；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Storage Tag Masking Level 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §4.1.5.3 如何排列 LBSTM、Storage Tag Masking Level 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.1.5.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 127 對應的 raw value 或 buffer，標出包含 LBSTM 的 bytes 並解碼，再獨立核對 Storage Tag Masking Level。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 LBSTM，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 LBSTM 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Storage Tag Masking Level 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** LBSTM, Storage Tag Masking Level, LBAFEE

**來源 keyword 索引：** `shall`, `should`, `may`, `optional`, `reserved`

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.3, Figure 127, 文件頁 97-101, PDF 頁 97-101

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 132: Namespace Granularity List</strong></summary>

<!-- claim:BASENSMGMT-FIG-132-CLAIM figure-table:BASENSMGMT-FIG-132 -->

**SPEC。** Figure 132〈Namespace Granularity List〉：呈現〈Namespace Granularity List〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：NGA.GDM, ND, NGD0-NGD63, CNS 16h。

#### 這張 Figure 在完整流程中的位置

Figure 132 位於 §4.1.5.8，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NGA.GDM 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NGA.GDM]
          ↓
[擷取欄位: ND] → [套用編碼: NGD0-NGD63]
                                      ↓
[驗證證據: CNS 16h]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NGA.GDM` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ND` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NGD0-NGD63` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CNS 16h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.1.5.8。
2. 依圖中指定的寬度與位置解碼 NGA.GDM；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 ND 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §4.1.5.8 如何排列 NGA.GDM、ND 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.1.5.8 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 132 對應的 raw value 或 buffer，標出包含 NGA.GDM 的 bytes 並解碼，再獨立核對 ND。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NGA.GDM，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NGA.GDM 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 ND 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NGA.GDM, ND, NGD0-NGD63, CNS 16h

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.8, Figure 132, 文件頁 108, PDF 頁 108

</details>

<details markdown="1">
<summary><strong>NVME-NVM-CS-1.3 — Figure 133: Namespace Granularity Descriptor</strong></summary>

<!-- claim:BASENSMGMT-FIG-133-CLAIM figure-table:BASENSMGMT-FIG-133 -->

**SPEC。** Figure 133〈Namespace Granularity Descriptor〉：定義〈Namespace Granularity Descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NSG bytes 7:0, NCG bytes 15:8, byte units。

#### 這張 Figure 在完整流程中的位置

Figure 133 位於 §4.1.5.8，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NSG bytes 7:0 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NSG bytes 7:0]
          ↓
[擷取欄位: NCG bytes 15:8] → [套用編碼: byte units]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NSG bytes 7:0` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NCG bytes 15:8` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `byte units` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.1.5.8。
2. 依圖中指定的寬度與位置解碼 NSG bytes 7:0；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NCG bytes 15:8 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §4.1.5.8 如何排列 NSG bytes 7:0、NCG bytes 15:8 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.1.5.8 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 133 對應的 raw value 或 buffer，標出包含 NSG bytes 7:0 的 bytes 並解碼，再獨立核對 NCG bytes 15:8。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NSG bytes 7:0，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NSG bytes 7:0 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NCG bytes 15:8 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NSG bytes 7:0, NCG bytes 15:8, byte units

**來源 keyword 索引：** none

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.8, Figure 133, 文件頁 108, PDF 頁 108

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 139: Controller List Format</strong></summary>

<!-- claim:BASENSMGMT-FIG-139-CLAIM figure-table:BASENSMGMT-FIG-139 -->

**SPEC。** Figure 139〈Controller List Format〉：定義〈Controller List Format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NUMCIDS, Controller Identifier list, 4096 bytes。

#### 這張 Figure 在完整流程中的位置

Figure 139 位於 §4.6.1，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NUMCIDS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NUMCIDS]
          ↓
[擷取欄位: Controller Identifier list] → [套用編碼: 4096 bytes]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NUMCIDS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Controller Identifier list` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `4096 bytes` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.6.1。
2. 依圖中指定的寬度與位置解碼 NUMCIDS；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Controller Identifier list 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
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
| 這張圖回答 | §4.6.1 如何排列 NUMCIDS、Controller Identifier list 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.6.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 139 對應的 raw value 或 buffer，標出包含 NUMCIDS 的 bytes 並解碼，再獨立核對 Controller Identifier list。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 Controller Identifier list 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NUMCIDS, Controller Identifier list, 4096 bytes

**來源 keyword 索引：** `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.6.1, Figure 139, 文件頁 172, PDF 頁 198

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 155: Asynchronous Event Information - Notice</strong></summary>

<!-- claim:BASENSMGMT-FIG-155-CLAIM figure-table:BASENSMGMT-FIG-155 -->

**SPEC。** Figure 155〈Asynchronous Event Information - Notice〉：定義〈Asynchronous Event Information - Notice〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Attached Namespace Attribute Changed, Allocated Namespace Attribute Changed, CNS 02h, CNS 10h。

#### 這張 Figure 在完整流程中的位置

Figure 155 位於 §5.2.2.1，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Attached Namespace Attribute Changed 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Attached Namespace Attribute Changed]
          ↓
[擷取欄位: Allocated Namespace Attribute Changed] → [套用編碼: CNS 02h]
                                      ↓
[驗證證據: CNS 10h]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Attached Namespace Attribute Changed` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Allocated Namespace Attribute Changed` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CNS 02h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CNS 10h` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.2.1。
2. 依圖中指定的寬度與位置解碼 Attached Namespace Attribute Changed；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Allocated Namespace Attribute Changed 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §5.2.2.1 如何排列 Attached Namespace Attribute Changed、Allocated Namespace Attribute Changed 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.2.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 155 對應的 raw value 或 buffer，標出包含 Attached Namespace Attribute Changed 的 bytes 並解碼，再獨立核對 Allocated Namespace Attribute Changed。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Attached Namespace Attribute Changed，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Attached Namespace Attribute Changed 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Allocated Namespace Attribute Changed 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Attached Namespace Attribute Changed, Allocated Namespace Attribute Changed, CNS 02h, CNS 10h

**來源 keyword 索引：** `shall not`, `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 155, 文件頁 186, PDF 頁 212

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 203: Get Log Page - Data Pointer</strong></summary>

<!-- claim:BASENSMGMT-FIG-203-CLAIM figure-table:BASENSMGMT-FIG-203 -->

**SPEC。** Figure 203〈Get Log Page - Data Pointer〉：把〈Get Log Page - Data Pointer〉連到 Self-test 證據路徑或 namespace lifecycle。 先確認物件與 lifecycle state，再解碼 DPTR, LID 06h destination buffer，最後以 CQE、log、event 或 Identify snapshot 驗證下一個 transition。

#### 這張 Figure 在完整流程中的位置

Figure 203 位於 §5.2.13，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DPTR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DPTR]
          ↓
[擷取欄位: LID 06h destination buffer] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DPTR` | Data Pointer，SQE 中指出 command data buffer 的欄位。 |
| `LID 06h destination buffer` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.13。
2. 依圖中指定的寬度與位置解碼 DPTR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 LID 06h destination buffer 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
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
| 這張圖回答 | §5.2.13 如何排列 DPTR、LID 06h destination buffer 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.13 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 203 對應的 raw value 或 buffer，標出包含 DPTR 的 bytes 並解碼，再獨立核對 LID 06h destination buffer。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 LID 06h destination buffer 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** DPTR, LID 06h destination buffer

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 203, 文件頁 213, PDF 頁 239

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 204: Get Log Page - Command Dword 10</strong></summary>

<!-- claim:BASENSMGMT-FIG-204-CLAIM figure-table:BASENSMGMT-FIG-204 -->

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
<summary><strong>NVME-BASE-2.4 — Figure 205: Get Log Page - Command Dword 11</strong></summary>

<!-- claim:BASENSMGMT-FIG-205-CLAIM figure-table:BASENSMGMT-FIG-205 -->

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
<summary><strong>NVME-BASE-2.4 — Figure 206: Get Log Page - Command Dword 12</strong></summary>

<!-- claim:BASENSMGMT-FIG-206-CLAIM figure-table:BASENSMGMT-FIG-206 -->

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
<summary><strong>NVME-BASE-2.4 — Figure 207: Get Log Page - Command Dword 13</strong></summary>

<!-- claim:BASENSMGMT-FIG-207-CLAIM figure-table:BASENSMGMT-FIG-207 -->

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
<summary><strong>NVME-BASE-2.4 — Figure 208: Get Log Page - Command Dword 14</strong></summary>

<!-- claim:BASENSMGMT-FIG-208-CLAIM figure-table:BASENSMGMT-FIG-208 -->

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
<summary><strong>NVME-BASE-2.4 — Figure 209: Get Log Page - Log Page Identifiers</strong></summary>

<!-- claim:BASENSMGMT-FIG-209-CLAIM figure-table:BASENSMGMT-FIG-209 -->

**SPEC。** Figure 209〈Get Log Page - Log Page Identifiers〉：定義〈Get Log Page - Log Page Identifiers〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：LID 06h, CSI = N, Controller / Domain / NVM subsystem, Device Self-test。

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

**來源欄位索引：** LID 06h, CSI = N, Controller / Domain / NVM subsystem, Device Self-test

**來源 keyword 索引：** `shall`, `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 209, 文件頁 215-216, PDF 頁 241-242

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 304: Manufacturer Default Configuration Status Log Page</strong></summary>

<!-- claim:BASENSMGMT-FIG-304-CLAIM figure-table:BASENSMGMT-FIG-304 -->

**SPEC。** Figure 304〈Manufacturer Default Configuration Status Log Page〉：把〈Manufacturer Default Configuration Status Log Page〉連到 Self-test 證據路徑或 namespace lifecycle。 先確認物件與 lifecycle state，再解碼 DNCS, default namespace configuration status，最後以 CQE、log、event 或 Identify snapshot 驗證下一個 transition。

#### 這張 Figure 在完整流程中的位置

Figure 304 位於 §5.2.13.1.31，在本流程中是「relationship」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DNCS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這張圖用來說明特定關係或範例。先辨識每個元件的類型與 owner，再沿連線判斷是資料流、控制流、包含關係或條件關係；圖形位置本身不新增 normative requirement。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DNCS]
          ↓
[擷取欄位: default namespace configuration status] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DNCS` | Default Namespace Configuration Status，表示目前 namespace configuration 是否等於 active firmware image defaults 的 status bit。 |
| `default namespace configuration status` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.13.1.31。
2. 依圖中指定的寬度與位置解碼 DNCS；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 default namespace configuration status 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 304 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13.1.31 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.13.1.31 如何排列 DNCS、default namespace configuration status 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.13.1.31 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 304 對應的 raw value 或 buffer，標出包含 DNCS 的 bytes 並解碼，再獨立核對 default namespace configuration status。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 DNCS，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 DNCS 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 default namespace configuration status 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** DNCS, default namespace configuration status

**來源 keyword 索引：** `shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.31, Figure 304, 文件頁 301-302, PDF 頁 327-328

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 338: Identify Controller Data Structure</strong></summary>

<!-- claim:BASENSMGMT-FIG-338-CLAIM figure-table:BASENSMGMT-FIG-338 -->

**SPEC。** Figure 338〈Identify Controller Data Structure〉：定義〈Identify Controller Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：OACS.DSTS, EDSTT, DSTO.SDSO, OACS.NMS, RDNCS, MAXDNA, MAXCNA。

#### 這張 Figure 在完整流程中的位置

Figure 338 位於 §5.2.14.2.1，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 OACS.DSTS 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: OACS.DSTS]
          ↓
[擷取欄位: EDSTT] → [套用編碼: DSTO.SDSO]
                                      ↓
[驗證證據: OACS.NMS]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `OACS.DSTS` | Optional Admin Command Support 的 Device Self-test Supported bit，判斷 command 是否可用。 |
| `EDSTT` | Extended Device Self-test Time，在 power state 0 下的 extended test 名目完成分鐘數。 |
| `DSTO.SDSO` | Device Self-test Options，Identify Controller 中回報 refresh 與 concurrency 選項的欄位。 此處的 DSTO.SDSO 進一步指定其中的 SDSO 子欄位。 |
| `OACS.NMS` | Optional Admin Command Support 的 Namespace Management Supported bit；設為 1 才宣告完整 Manage 加 Attach capability。 |
| `RDNCS` | Restore Default Namespace Configuration Supported，宣告 Restore Default operation 是否支援的 capability bit。 |
| `MAXDNA` | Maximum Domain Namespace Attachments，整個 Domain 內所有 I/O controller attachment 數量總和的上限。 |

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

**來源欄位索引：** OACS.DSTS, EDSTT, DSTO.SDSO, OACS.NMS, RDNCS, MAXDNA, MAXCNA

**來源 keyword 索引：** `shall not`, `should not`, `shall`, `should`, `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, 文件頁 340, 353, 365, 378, PDF 頁 366, 379, 391, 404

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 346: Identify - I/O Command Set Independent Identify Namespace Data Structure</strong></summary>

<!-- claim:BASENSMGMT-FIG-346-CLAIM figure-table:BASENSMGMT-FIG-346 -->

**SPEC。** Figure 346〈Identify - I/O Command Set Independent Identify Namespace Data Structure〉：定義〈Identify - I/O Command Set Independent Identify Namespace Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ANAGRPID, NVMSETID, ENDGID。

#### 這張 Figure 在完整流程中的位置

Figure 346 位於 §5.2.14.2.3，在本流程中是「hierarchy」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ANAGRPID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 object／capacity 關係圖。分開『包含』、『可存取』、『以 identifier 指向』與『共享』四種關係。相鄰方塊不一定一對一，identifier 也不等於被指向的實體或邏輯物件。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ANAGRPID]
          ↓
[擷取欄位: NVMSETID] → [套用編碼: ENDGID]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ANAGRPID` | ANA Group Identifier，namespace 所屬 Asymmetric Namespace Access group 的 identifier；create 值 0 讓 controller 選擇。 |
| `NVMSETID` | NVM Set Identifier，指定建立 namespace 時要從哪個 NVM Set 配置容量。 |
| `ENDGID` | Endurance Group Identifier，指定建立 namespace 時所屬 Endurance Group。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.14.2.3。
2. 依圖中指定的寬度與位置解碼 ANAGRPID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NVMSETID 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 346 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.14.2.3 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.14.2.3 如何排列 ANAGRPID、NVMSETID 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.14.2.3 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 346 對應的 raw value 或 buffer，標出包含 ANAGRPID 的 bytes 並解碼，再獨立核對 NVMSETID。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 ANAGRPID，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 ANAGRPID 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NVMSETID 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ANAGRPID, NVMSETID, ENDGID

**來源 keyword 索引：** `shall`, `should`, `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.3, Figure 346, 文件頁 391-394, PDF 頁 417-420

</details>

<details markdown="1">
<summary><strong>NVME-BASE-2.4 — Figure 474: Asynchronous Event Configuration - Command Dword 11</strong></summary>

<!-- claim:BASENSMGMT-FIG-474-CLAIM figure-table:BASENSMGMT-FIG-474 -->

**SPEC。** Figure 474〈Asynchronous Event Configuration - Command Dword 11〉：定義 Asynchronous Event Configuration 在 CDW11 的 command-specific 欄位。 先定位 CDW11，再依本命令定義解碼，不借用其他 command 的語意；來源欄位索引：Attached Namespace Attribute Notices, Allocated Namespace Attribute Notices。

#### 這張 Figure 在完整流程中的位置

Figure 474 位於 §5.2.30.1.6，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Attached Namespace Attribute Notices 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Attached Namespace Attribute Notices]
          ↓
[擷取欄位: Allocated Namespace Attribute Notices] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Attached Namespace Attribute Notices` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Allocated Namespace Attribute Notices` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.1.6。
2. 依圖中指定的寬度與位置解碼 Attached Namespace Attribute Notices；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Allocated Namespace Attribute Notices 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
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
| 這張圖回答 | §5.2.30.1.6 如何排列 Attached Namespace Attribute Notices、Allocated Namespace Attribute Notices 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.1.6 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 474 對應的 raw value 或 buffer，標出包含 Attached Namespace Attribute Notices 的 bytes 並解碼，再獨立核對 Allocated Namespace Attribute Notices。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Attached Namespace Attribute Notices，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Attached Namespace Attribute Notices 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Allocated Namespace Attribute Notices 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Attached Namespace Attribute Notices, Allocated Namespace Attribute Notices

**來源 keyword 索引：** `shall not`, `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.6, Figure 474, 文件頁 466-468, PDF 頁 492-494

</details>

## 使用與限制

製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata 集合或核准範圍改變時，必須重新核對受影響 claim。

## 自問自答：規則、比較、案例與排錯

以下 32 題均附答案，針對本報告範圍複習。每題保留對應教學單元的來源；數值案例與排錯建議屬說明性內容。

### Q01. 「先分清兩條生命週期：diagnostic evidence 與 namespace provisioning」的核心判讀規則是什麼？

<!-- qa:base-self-test-namespace-management-diagnostic-and-provisioning-lead -->

**答。**

Device Self-test 與 Namespace Management 都使用 Admin command，但它們改變的物件完全不同。Self-test 建立一個背景 operation，command CQE 只是接受點，最後要靠 LID 06h 證明結果；Namespace Management 建立或移除 namespace object，Create CQE 回傳 NSID，但還要 Attach 才建立 controller access。先分開兩條線，才能理解 completion 為何不是終點。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 201, PDF 頁 227; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446-448, 662, PDF 頁 472-474, 688

### Q02. 「先分清兩條生命週期：diagnostic evidence 與 namespace provisioning」中，哪些概念或條件必須分開比較？

<!-- qa:base-self-test-namespace-management-diagnostic-and-provisioning-rows -->

**答。**

- Self-test object — background operation — CQE→current state→history result
- Namespace object — allocated capacity + format — Create CQE.DW0→NSID
- Access relationship — namespace↔controller attachment — Attach CQE→Active NSID list
- Inventory evidence — Allocated／Active lists — AEN 後重新 Identify

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 201, PDF 頁 227; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446-448, 662, PDF 頁 472-474, 688

### Q03. 「先分清兩條生命週期：diagnostic evidence 與 namespace provisioning」如何套用到具體數值或操作情境？

<!-- qa:base-self-test-namespace-management-diagnostic-and-provisioning-example -->

**答。**

Create 成功回 NSID=7 只證明 namespace 7 已建立；它仍未 attached，不能立刻做 I/O。相反地，Self-test 啟動成功的 CQE 也只證明 operation 已開始，不能把它記成 test passed。兩種 CQE 都要再接下一個證據，但下一個證據不同。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 201, PDF 頁 227; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446-448, 662, PDF 頁 472-474, 688

### Q04. 「先分清兩條生命週期：diagnostic evidence 與 namespace provisioning」最容易出現什麼誤判？如何排查？

<!-- qa:base-self-test-namespace-management-diagnostic-and-provisioning-pitfall -->

**答。**

不要用『Admin command 成功』概括整段流程。trace 必須標出 command 改變的 object、成功所跨越的 boundary，以及仍待取得的 LID、Identify 或 event evidence。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 201, PDF 頁 227; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446-448, 662, PDF 頁 472-474, 688

### Q05. 「Device Self-test：從 capability gate 到 LID 06h result」的核心判讀規則是什麼？

<!-- qa:base-self-test-namespace-management-selftest-command-state-machine-lead -->

**答。**

先用 OACS.DSTS、EDSTT 與 DSTO.SDSO 建立支援、時間與 concurrency 預期，再以 NSID 與 STC 建構 command。CQE 到達後輪詢 DSTOS／DSTCS；operation 結束時，先建立 RDS1，再把 current status 清零。這個先後順序讓 software 不會在短暫視窗遺失最後結果。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, 文件頁 353-358, 614, PDF 頁 379-384, 640; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 199, PDF 頁 225; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 199-200, PDF 頁 225-226; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-230, PDF 頁 255-256; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-232, PDF 頁 255-258; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 231-232, PDF 頁 257-258; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, 文件頁 76, PDF 頁 76

### Q06. 「Device Self-test：從 capability gate 到 LID 06h result」中，哪些概念或條件必須分開比較？

<!-- qa:base-self-test-namespace-management-selftest-command-state-machine-rows -->

**答。**

- NSID=0 — controller only — 不包含 namespace media
- active NSID — 單一 namespace — invalid／inactive status 分開
- NSID=FFFFFFFFh — 開始時可存取的 attached set — 集合不是動態追蹤
- STC=Fh — abort current operation — 先寫 result 再清 current

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, 文件頁 353-358, 614, PDF 頁 379-384, 640; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 199, PDF 頁 225; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 199-200, PDF 頁 225-226; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-230, PDF 頁 255-256; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-232, PDF 頁 255-258; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 231-232, PDF 頁 257-258; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, 文件頁 76, PDF 頁 76

### Q07. 「Device Self-test：從 capability gate 到 LID 06h result」如何套用到具體數值或操作情境？

<!-- qa:base-self-test-namespace-management-selftest-command-state-machine-example -->

**答。**

讀完整 LID 06h：564÷4=141 dwords，NUMD=141−1=140=008Ch。RAE=0、LSP=0、LID=06h，因此 CDW10=008C0006h。若 RDS1.DSTS=17h，DSTC=1h 是 short、DSTR=7h 才允許讀 SEGN。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, 文件頁 353-358, 614, PDF 頁 379-384, 640; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 199, PDF 頁 225; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 199-200, PDF 頁 225-226; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-230, PDF 頁 255-256; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-232, PDF 頁 255-258; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 231-232, PDF 頁 257-258; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, 文件頁 76, PDF 頁 76

### Q08. 「Device Self-test：從 capability gate 到 LID 06h result」最容易出現什麼誤判？如何排查？

<!-- qa:base-self-test-namespace-management-selftest-command-state-machine-pitfall -->

**答。**

FLBA 非零不是有效證據。先解 DSTR，再查 FVLD／NSIDVLD，最後才套 NVM Command Set bytes 23:16 的 FLBA 語意；同時保存 raw 28-byte entry。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, 文件頁 353-358, 614, PDF 頁 379-384, 640; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 199, PDF 頁 225; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 199-200, PDF 頁 225-226; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-230, PDF 頁 255-256; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-232, PDF 頁 255-258; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 231-232, PDF 頁 257-258; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, 文件頁 76, PDF 頁 76

### Q09. 「先把三種容量與兩種 granularity 換到同一個 byte model」的核心判讀規則是什麼？

<!-- qa:base-self-test-namespace-management-capacity-granularity-math-lead -->

**答。**

NSZE、NCAP、NUSE 的單位是 logical blocks；NSG、NCG 的單位是 bytes；controller 實際消耗的 NVM capacity 又可能按 allocation unit 向上取整。比較前必須先乘上選定 LBA size。NSZE≥NCAP≥NUSE 是合法性關係，NSG／NCG divisibility 則是減少浪費的 hint，不能混成同一種 gate。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, 文件頁 13-14, PDF 頁 13-14; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, 文件頁 13, PDF 頁 13; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 661, PDF 頁 687; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.8, 文件頁 165, PDF 頁 165; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.8, 文件頁 165, PDF 頁 165

### Q10. 「先把三種容量與兩種 granularity 換到同一個 byte model」中，哪些概念或條件必須分開比較？

<!-- qa:base-self-test-namespace-management-capacity-granularity-math-rows -->

**答。**

- NSZE — logical blocks — LBA 0..NSZE−1
- NCAP — logical blocks — 最大可配置容量
- NUSE — logical blocks — THINP=1 時需追蹤
- NSG／NCG — bytes — preferred hint，不是單獨 abort gate

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, 文件頁 13-14, PDF 頁 13-14; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, 文件頁 13, PDF 頁 13; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 661, PDF 頁 687; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.8, 文件頁 165, PDF 頁 165; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.8, 文件頁 165, PDF 頁 165

### Q11. 「先把三種容量與兩種 granularity 換到同一個 byte model」如何套用到具體數值或操作情境？

<!-- qa:base-self-test-namespace-management-capacity-granularity-math-example -->

**答。**

LBA=4 KiB、NSG=1 MiB、NCG=2 MiB。NSZE=NCAP=1024 代表 4 MiB，4 MiB 可整除兩個 hints，且為 fully provisioned。NSZE=NCAP=1000 代表 3,906.25 KiB，無法整除 hints；可能浪費 allocation capacity，但 otherwise-valid create 仍不能只因這點 abort。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, 文件頁 13-14, PDF 頁 13-14; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, 文件頁 13, PDF 頁 13; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 661, PDF 頁 687; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.8, 文件頁 165, PDF 頁 165; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.8, 文件頁 165, PDF 頁 165

### Q12. 「先把三種容量與兩種 granularity 換到同一個 byte model」最容易出現什麼誤判？如何排查？

<!-- qa:base-self-test-namespace-management-capacity-granularity-math-pitfall -->

**答。**

最常見錯誤是拿 NSZE=1024 直接除 NSG=1 MiB，或把 granularity violation 當 Invalid Field。工作紙要明列 raw blocks、LBA bytes、converted bytes、remainder 與 controller allocation unit。

> 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, 文件頁 13-14, PDF 頁 13-14; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, 文件頁 13, PDF 頁 13; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 661, PDF 頁 687; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.8, 文件頁 165, PDF 頁 165; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.8, 文件頁 165, PDF 頁 165

### Q13. 「Create payload：Base envelope 包住 NVM-specific 512 bytes」的核心判讀規則是什麼？

<!-- qa:base-self-test-namespace-management-namespace-create-payload-lead -->

**答。**

Base Figure 448 定義 4096-byte envelope，NVM Command Set Figure 134 只定義前 768 bytes 中的 NVM 欄位與 Placement Handle List。Host 先以 SEL／CSI 決定 operation 與 command set，再填 NSZE、NCAP、format、protection、sharing 與 group IDs。Reserved areas 要清零，Protection Information 與 FDP 又各有獨立 capability gate。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 文件頁 446-448, PDF 頁 472-474; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.4, 文件頁 111-113, PDF 頁 111-113; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, 文件頁 110, PDF 頁 110; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, 文件頁 110-111, PDF 頁 110-111; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 661, PDF 頁 687

### Q14. 「Create payload：Base envelope 包住 NVM-specific 512 bytes」中，哪些概念或條件必須分開比較？

<!-- qa:base-self-test-namespace-management-namespace-create-payload-rows -->

**答。**

- Base 0:511 — SIOCS — NVM-specific create data
- Base 512:1023 — Reserved — host 清 0
- Base 1024:4095 — Vendor Specific — 沒有來源定義就不猜
- NVM 512:767 — Placement Handle List — 只在 FDP enable 時驗證

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 文件頁 446-448, PDF 頁 472-474; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.4, 文件頁 111-113, PDF 頁 111-113; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, 文件頁 110, PDF 頁 110; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, 文件頁 110-111, PDF 頁 110-111; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 661, PDF 頁 687

### Q15. 「Create payload：Base envelope 包住 NVM-specific 512 bytes」如何套用到具體數值或操作情境？

<!-- qa:base-self-test-namespace-management-namespace-create-payload-example -->

**答。**

建立 4 MiB namespace：LBA=4096 bytes、NSZE=NCAP=1024，因此 bytes 7:0 與 15:8 都寫 0000000000000400h。NVMSETID=0、ENDGID=5 表示由 Endurance Group 5 內選 NVM Set；反過來 NVMSETID=7、ENDGID=0 是 Invalid Field。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 文件頁 446-448, PDF 頁 472-474; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.4, 文件頁 111-113, PDF 頁 111-113; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, 文件頁 110, PDF 頁 110; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, 文件頁 110-111, PDF 頁 110-111; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 661, PDF 頁 687

### Q16. 「Create payload：Base envelope 包住 NVM-specific 512 bytes」最容易出現什麼誤判？如何排查？

<!-- qa:base-self-test-namespace-management-namespace-create-payload-pitfall -->

**答。**

不要只 dump Figure 134 的欄位值。Debug 還要保存 host 使用的 LBA format capability、LBAFEE、Figure 127 masking limits、FDP enable state、完整 4096-byte buffer 與 reserved-byte scan。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 文件頁 446-448, PDF 頁 472-474; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.4, 文件頁 111-113, PDF 頁 111-113; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, 文件頁 110, PDF 頁 110; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, 文件頁 110-111, PDF 頁 110-111; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 661, PDF 頁 687

### Q17. 「Namespace lifecycle：Create 只建立 object，Attach 才建立 access」的核心判讀規則是什麼？

<!-- qa:base-self-test-namespace-management-namespace-lifecycle-lead -->

**答。**

Create、Attach、Detach、Delete 分別改變兩個狀態維度：namespace 是否 allocated，以及某 controller 是否 attached。Create CQE.DW0 回 NSID 後，object 已 allocated 但所有 controller 都未 attached；Attach 的 Controller List 才建立 access。Detach 不刪容量，Delete 才使 NSID unallocated。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, 文件頁 444-445, PDF 頁 470-471; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, 文件頁 444-445, PDF 頁 470-471; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446-448, 662, PDF 頁 472-474, 688

### Q18. 「Namespace lifecycle：Create 只建立 object，Attach 才建立 access」中，哪些概念或條件必須分開比較？

<!-- qa:base-self-test-namespace-management-namespace-lifecycle-rows -->

**答。**

- Create — object／capacity — 不自動 attach
- Attach — access relationship — Controller List 可含多個 CNTLID
- Detach — controller-local active state — namespace 仍 allocated
- Delete — subsystem inventory — NSID 變 unallocated

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, 文件頁 444-445, PDF 頁 470-471; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, 文件頁 444-445, PDF 頁 470-471; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446-448, 662, PDF 頁 472-474, 688

### Q19. 「Namespace lifecycle：Create 只建立 object，Attach 才建立 access」如何套用到具體數值或操作情境？

<!-- qa:base-self-test-namespace-management-namespace-lifecycle-example -->

**答。**

Create 回 NSID=7。Controller List 的 NUMCIDS 與 entries 指定 controllers 3、5；Attach 成功後 NSID 7 對 3、5 active。再只 detach controller 3，NSID 7 對 3 inactive、對 5 仍 active，namespace 本身仍 allocated。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, 文件頁 444-445, PDF 頁 470-471; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, 文件頁 444-445, PDF 頁 470-471; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446-448, 662, PDF 頁 472-474, 688

### Q20. 「Namespace lifecycle：Create 只建立 object，Attach 才建立 access」最容易出現什麼誤判？如何排查？

<!-- qa:base-self-test-namespace-management-namespace-lifecycle-pitfall -->

**答。**

NSID 數值相同不代表每個 controller 的 active state 相同。inventory 與 I/O trace 都要帶 controller ID；attach limit 還要分開核對 Domain MAXDNA 與 per-controller MAXCNA。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, 文件頁 444-445, PDF 頁 470-471; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, 文件頁 444-445, PDF 頁 470-471; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446-448, 662, PDF 頁 472-474, 688

### Q21. 「Delete 與 Restore Default：先清空 inventory，再跨 configuration boundary」的核心判讀規則是什麼？

<!-- qa:base-self-test-namespace-management-delete-restore-state-lead -->

**答。**

Delete all 與 Restore Default 是兩個不同 operation。NSID=FFFFFFFFh 的 Delete All 在零個 namespaces 時也成功；Restore Default 則要求 RDNCS capability、SEL=2h，以及 subsystem 中已不存在任何 namespace。成功前 controller 套用 current active firmware image defaults 並設 DNCS=1。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446, 448, 662, PDF 頁 472, 474, 688; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25.1, 文件頁 447-448, PDF 頁 473-474; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, 文件頁 662-663, PDF 頁 688-689

### Q22. 「Delete 與 Restore Default：先清空 inventory，再跨 configuration boundary」中，哪些概念或條件必須分開比較？

<!-- qa:base-self-test-namespace-management-delete-restore-state-rows -->

**答。**

- Delete one — NSID=target — 成功後 object 消失
- Delete all — NSID=FFFFFFFFh — zero namespace 仍成功
- Restore — SEL=2h、NSID ignored — 剩餘 namespace→Sequence Error
- Post-condition — DNCS=1 — 仍要重新 Identify actual defaults

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446, 448, 662, PDF 頁 472, 474, 688; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25.1, 文件頁 447-448, PDF 頁 473-474; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, 文件頁 662-663, PDF 頁 688-689

### Q23. 「Delete 與 Restore Default：先清空 inventory，再跨 configuration boundary」如何套用到具體數值或操作情境？

<!-- qa:base-self-test-namespace-management-delete-restore-state-example -->

**答。**

先 detach NSID 7，再 Delete 7；讀 Allocated Namespace ID list 確認為空。若 RDNCS=1，送 SEL=2h、NSID=0。CQE success 後讀 DNCS=1，最後重新列舉 default namespaces；DNCS 是狀態證據，不是 default layout 的完整描述。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446, 448, 662, PDF 頁 472, 474, 688; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25.1, 文件頁 447-448, PDF 頁 473-474; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, 文件頁 662-663, PDF 頁 688-689

### Q24. 「Delete 與 Restore Default：先清空 inventory，再跨 configuration boundary」最容易出現什麼誤判？如何排查？

<!-- qa:base-self-test-namespace-management-delete-restore-state-pitfall -->

**答。**

不能用 Delete All CQE 直接推論 Restore 已完成，也不能只看 DNCS 猜 default NSZE／format。每一步都保存 operation selector、inventory snapshot、CQE 與 post-Identify。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446, 448, 662, PDF 頁 472, 474, 688; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25.1, 文件頁 447-448, PDF 頁 473-474; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, 文件頁 662-663, PDF 頁 688-689

### Q25. 「Namespace event：通知只說 inventory 變了，Identify 才說變成什麼」的核心判讀規則是什麼？

<!-- qa:base-self-test-namespace-management-namespace-events-lead -->

**答。**

Attached 與 Allocated Namespace Attribute Changed notices 對應不同 inventory。Create 通常改 Allocated list；Attach／Detach 改 Active list；Delete 可能同時改兩者。event code 不是新清單本身，因此 host 收到 AEN 後要依 CNS 重新 Identify。Delete reporting 還要分辨 processing controller 與其他 controllers。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, 文件頁 662-663, PDF 頁 688-689; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446-448, 662, PDF 頁 472-474, 688

### Q26. 「Namespace event：通知只說 inventory 變了，Identify 才說變成什麼」中，哪些概念或條件必須分開比較？

<!-- qa:base-self-test-namespace-management-namespace-events-rows -->

**答。**

- CNS 02h — Active Namespace ID list — Attached notice
- CNS 10h — Allocated Namespace ID list — Allocated notice
- Create — Allocated change — 新 NSID 尚未 active
- Delete — Allocated＋可能 Active — processing controller 規則不同

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, 文件頁 662-663, PDF 頁 688-689; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446-448, 662, PDF 頁 472-474, 688

### Q27. 「Namespace event：通知只說 inventory 變了，Identify 才說變成什麼」如何套用到具體數值或操作情境？

<!-- qa:base-self-test-namespace-management-namespace-events-example -->

**答。**

Controller 3 處理 attached NSID 7 的 Delete。其他已啟用 notice 的 controllers 依 §8.1.17.2 回報；processing controller 的要求不同。host 不應只計算 event 數量，而要為每個 controller 保存 before/after Active 與 Allocated lists。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, 文件頁 662-663, PDF 頁 688-689; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446-448, 662, PDF 頁 472-474, 688

### Q28. 「Namespace event：通知只說 inventory 變了，Identify 才說變成什麼」最容易出現什麼誤判？如何排查？

<!-- qa:base-self-test-namespace-management-namespace-events-pitfall -->

**答。**

常見誤解是把 AEN 當成 inventory delta。AEN 只觸發 refresh；真正 authoritative data 是後續 Identify result。若漏 event，也可由 before/after inventory 差異定位，但不能反向捏造未收到的通知。

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686; 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, 文件頁 662-663, PDF 頁 688-689; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446-448, 662, PDF 頁 472-474, 688

### Q29. 「End-to-End：把 capacity、command、object、attachment 與 evidence 放在同一條 timeline」的核心判讀規則是什麼？

<!-- qa:base-self-test-namespace-management-namespace-end-to-end-debug-lead -->

**答。**

Namespace bug 很少只是一個欄位錯。create 前的 capability snapshot、4096-byte payload、CQE.DW0、Controller List、attach limits、events 與 post-Identify 必須能串回同一個 NSID 與 controller set。Debug 不從最後的 I/O failure 猜原因，而是找第一個不一致 boundary。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, 文件頁 445, 448, PDF 頁 471, 474; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, 8.1.17.1, 文件頁 444-448, 661-663, PDF 頁 470-474, 687-689; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, 文件頁 444-445, PDF 頁 470-471; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, 文件頁 110, PDF 頁 110; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, 文件頁 110-111, PDF 頁 110-111

### Q30. 「End-to-End：把 capacity、command、object、attachment 與 evidence 放在同一條 timeline」中，哪些概念或條件必須分開比較？

<!-- qa:base-self-test-namespace-management-namespace-end-to-end-debug-rows -->

**答。**

- Create Invalid Format — FLBAS／DPS／LBSTM／LBAFEE — 先找 format gate
- Insufficient Capacity — NSZE／NCAP、unallocated bytes、group IDs — 分 logical 與 consumed
- Attach limit — MAXDNA／MAXCNA＋before counts — Domain 與 controller 分開
- I/O inactive NSID — Attach CQE、Active list、controller ID — Create success 不夠

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, 文件頁 445, 448, PDF 頁 471, 474; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, 8.1.17.1, 文件頁 444-448, 661-663, PDF 頁 470-474, 687-689; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, 文件頁 444-445, PDF 頁 470-471; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, 文件頁 110, PDF 頁 110; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, 文件頁 110-111, PDF 頁 110-111

### Q31. 「End-to-End：把 capacity、command、object、attachment 與 evidence 放在同一條 timeline」如何套用到具體數值或操作情境？

<!-- qa:base-self-test-namespace-management-namespace-end-to-end-debug-example -->

**答。**

案例：Create 回 NSID 7，Attach 卻回 27h。先查 controller 5 的 MAXCNA 與 Domain MAXDNA before-count；若 per-controller 已達上限，就不應修改 create payload或重送 I/O。正確 recovery 是選別的 controller、detach 其他 namespace，或停止並回報 capacity policy。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, 文件頁 445, 448, PDF 頁 471, 474; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, 8.1.17.1, 文件頁 444-448, 661-663, PDF 頁 470-474, 687-689; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, 文件頁 444-445, PDF 頁 470-471; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, 文件頁 110, PDF 頁 110; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, 文件頁 110-111, PDF 頁 110-111

### Q32. 「End-to-End：把 capacity、command、object、attachment 與 evidence 放在同一條 timeline」最容易出現什麼誤判？如何排查？

<!-- qa:base-self-test-namespace-management-namespace-end-to-end-debug-pitfall -->

**答。**

不要只記 human-readable status。保存 SCT／SC／DNR、raw SQE、buffer hash、returned NSID、controller list、timestamp 與 before/after inventories，才能重算是哪一個 gate 拒絕。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, 文件頁 445, 448, PDF 頁 471, 474; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, 8.1.17.1, 文件頁 444-448, 661-663, PDF 頁 470-474, 687-689; 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, 文件頁 444-445, PDF 頁 470-471; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, 文件頁 110, PDF 頁 110; 來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, 文件頁 110-111, PDF 頁 110-111
