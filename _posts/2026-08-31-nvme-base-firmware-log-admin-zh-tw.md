---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4：Firmware Update 與 LID 03h 驗證"
date: 2026-09-01
description: "Firmware update 與 LID 03h 的投影片製作稿。"
lang: zh-Hant-TW
img: posts/2026/dogMC_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---

# NVMe Base 2.4：Firmware Update 與 LID 03h 驗證

PPT 製作版。中文版與英文版使用完全相同的 slide modules、claim 順序、計算與來源邊界。

NVM Express Base Specification, Revision 2.4

NVM Express NVMe over PCIe Transport Specification, Revision 1.4 — 僅 §3.3

---

## Slide 01 — 真正要解決的問題

> Download 成功不等於 activation 成功；必須分開追蹤 placement、pending activation、reset 邊界與 activation 後證據。

```text
Download -> Commit / place -> activate now or later -> reset if required -> LID 03h verify
```

---

## Slide 02 — 先教名詞，再看欄位

| 狀態 | 意義 | 證據 |
|---|---|---|
| Downloaded | portions 暫存中 | NUMD／OFST |
| Stored | image 已在 slot | FRSx |
| Pending | 排定下一次 reset | NAFS |
| Active | image 正在執行 | CAFS＋Identify.FR |

---

## Slide 03 — Mental Model 與 capability gate

Firmware slots 屬於 domain。建構 command 前，先讀 FRMW、FWUG、MTFA、MPTFAWR、MDS／DID 與目前 FR。

| 欄位 | 回答的問題 | unit／range |
|---|---|---|
| FRMW | slots、read-only、立即 activation | bits |
| FWUG | chunk granularity／alignment | 4 KiB |
| MTFA | command processing 暫停 | 100 ms |
| MPTFAWR | CA=011b completion estimate | 100 ms |

來源地圖：Figure 338（文件/PDF 340-365/366-391）；Figures 347-348（396/422）。

<details markdown="1">
<summary><strong>講者備註／來源論點</strong></summary>

<!-- claim:BASEFWLOG-MODEL-DOMAIN -->

**[SPEC]** 同一 domain 內的 controllers 共用 firmware slots，且相同 firmware image 會套用到該 domain 的所有 controllers；若不支援 multiple domains，範圍就是整個 NVM subsystem。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 202, PDF 頁 228

<!-- claim:BASEFWLOG-CAP-FR -->

**[SPEC]** Identify Controller 的 FR 是目前 active firmware revision 的 8-byte ASCII string，scope 是 controller 所屬 domain；它與 LID 03h 回報的目前 revision 資訊相同。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 340, PDF 頁 366

<!-- claim:BASEFWLOG-CAP-MDS-ULIST -->

**[SPEC]** CTRATT.MDS 判斷 LID 03h 回傳 domain scope 還是整個 NVM subsystem scope；CTRATT.ULIST 判斷 controller 是否支援 UUID List reporting。MDS=1 時 DID 必須（shall）非零；single-domain subsystem 的 DID 必須（shall）為 0h。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 346, 364, PDF 頁 372, 390

<!-- claim:BASEFWLOG-CAP-FRMW -->

**[SPEC]** FRMW 的 SMUD、FAWR、NOFS 與 FFSRO 分別表示重疊 update 偵測、免 reset activation、domain 支援的 slot 數（1 到 7）以及 slot 1 是否 read-only。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 354, PDF 頁 380

<!-- claim:BASEFWLOG-CAP-MTFA -->

**[SPEC]** MTFA 以 100 ms 為單位，表示 activation 時 controller 暫停處理 commands 的最長時間；支援免 reset activation 時此欄位必須（shall）有效，0h 表示最大時間未定義。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 357, PDF 頁 383

<!-- claim:BASEFWLOG-CAP-FWUG -->

**[SPEC]** FWUG 以 4 KiB 為單位限制 NUMD 與 OFST 的 granularity／alignment：1h=4 KiB、2h=8 KiB、0h=未提供資訊、FFh=可用任何 dword granularity 與 alignment。違反時 controller 可（may）回 Invalid Field in Command。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 359, PDF 頁 385

<!-- claim:BASEFWLOG-CAP-MPTFAWR -->

**[SPEC]** MPTFAWR 以 100 ms 為單位，估算 CA=011b 的 Firmware Commit 從處理到完成所需最大時間，且包含把 image commit 到 slot 的時間；不支援免 reset activation 時必須（shall）為 0h。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 364, PDF 頁 390

</details>

---

## Slide 04 — Download 的本質是 dword ranges

```text
bytes = (NUMD + 1) × 4
byte offset = OFST × 4
```

**範例：**4 KiB=1024 dwords，所以 NUMD=03FFh；從 byte 8192 開始的 portion 使用 OFST=0800h。

來源地圖：Figure 93（文件/PDF 140-142/166-168）；Figures 190-193（205-206/231-232）。

<details markdown="1">
<summary><strong>講者備註／來源論點</strong></summary>

<!-- claim:BASEFWLOG-FW-SEQUENCE -->

**[SPEC]** host 不宜（should not）讓 firmware／Boot Partition update sequences 重疊，且同一 sequence 宜（should）只使用一個 controller 或 Management Endpoint。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 文件頁 137, PDF 頁 163

<!-- claim:BASEFWLOG-DOWNLOAD-RANGE -->

**[SPEC]** Firmware Image Download 可分成多個 portions，firmware image portions 可不依序送達；host 宜（should）避免 ranges 重疊並符合 FWUG。Boot Partition portions 則必須（shall）依序提交。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, 文件頁 205-206, PDF 頁 231-232

<!-- claim:BASEFWLOG-DOWNLOAD-FIELDS -->

**[SPEC]** NVMe over PCIe 的 Admin command 不得使用 SGL，因此 DPTR 以 PRP 指向本次來源 buffer；NUMD 是 0's-based dword count，所以 bytes=(NUMD+1)×4；OFST 是距 image 起點的 dword offset，所以 byte offset=OFST×4。包含 image 起點的 portion 必須（shall）令 OFST=0h。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 5.2.10, 文件頁 140-142, 205-206, PDF 頁 166-168, 231-232

<!-- claim:BASEFWLOG-FW-DISCARD -->

**[SPEC]** Firmware Commit 完成後的第一筆新 Firmware Image Download，以及 download 後、Firmware Commit 完成前發生的 Controller Level Reset，都必須（shall）使 controller 丟棄尚存的已下載 portions。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 5.2.10, 文件頁 137, 205-206, PDF 頁 163, 231-232

</details>

---

## Slide 05 — Commit Action 是狀態轉移

| CA | placement | activation |
|---|---|---|
| 000b | downloaded image → slot | 不 activation |
| 001b | downloaded image → slot | 下次合適 CLR |
| 010b | existing slot | 下次合適 CLR |
| 011b | downloaded／existing slot | 立即；command 等結果 |

來源地圖：Figures 187-189（文件/PDF 203-205/229-231）。

<details markdown="1">
<summary><strong>講者備註／來源論點</strong></summary>

<!-- claim:BASEFWLOG-COMMIT-PURPOSE -->

**[SPEC]** Firmware Commit 驗證最後下載的 image、把它放入 firmware slot，並依 Commit Action 決定只放置、在後續 Controller Level Reset activation，或立即 activation。成功 commit 不等於當下已 active。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 202-203, PDF 頁 228-229

<!-- claim:BASEFWLOG-COMMIT-CDW10 -->

**[SPEC]** CDW10[5:3] 是 CA，CDW10[2:0] 是 FS。CA 000b 只放置；001b 放置並排定下次 CLR activation；010b 排定既有 slot；011b 立即 activation。FS=0h 時 controller 必須（shall）在 slot 1 到 7 中選一個。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 203, PDF 頁 229

<!-- claim:BASEFWLOG-COMMIT-BOOT -->

**[SPEC]** BPID 與 CA=110b／111b 屬於 Boot Partition：110b 取代指定 partition，111b 將它標成 active；Boot Partition Write Prohibited 是 Firmware Commit 的 command-specific status 之一。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 203-205, PDF 頁 229-231

<!-- claim:BASEFWLOG-COMMIT-MUD -->

**[SPEC]** Firmware Commit CQE.DW0[1:0] 的 MUD 分別回報 Management Endpoint 與 Admin Submission Queue 偵測到的 overlap。若 FRMW.SMUD=0，MUD 必須（shall）為 00b；MUD 在 command 成功或 aborted 時都有效。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 204, PDF 頁 230

<!-- claim:BASEFWLOG-COMMIT-STATUS -->

**[SPEC]** Firmware Commit 的 command-specific status 區分 invalid slot／image、需要 Conventional／NVM Subsystem／Controller Level Reset、MTFA violation、activation prohibited、overlapping range、Boot Partition write prohibited 與 personality incompatibility。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 204-205, PDF 頁 230-231

</details>

---

## Slide 06 — Activation 有四條分支

```text
CA 000b -> stored only
CA 001b / 010b -> pending -> required CLR -> reinitialize
CA 011b -> command in progress -> success or reset-required / time / prohibited status
load failure -> most recently active image -> baseline read-only fallback
```

來源地圖：Figures 155、474（文件/PDF 186/212、466-468/492-494）；Figures 347-348（396/422）。

<details markdown="1">
<summary><strong>講者備註／來源論點</strong></summary>

<!-- claim:BASEFWLOG-FW-RESET -->

**[SPEC]** 需要 reset 的標準流程是：一筆以上 Firmware Image Download、Firmware Commit 驗證並放入 slot、執行能觸發該 activation 的 Controller Level Reset，然後重新初始化 controller 與 I/O queues。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 文件頁 135-136, PDF 頁 161-162

<!-- claim:BASEFWLOG-FW-IMMEDIATE -->

**[SPEC]** CA=011b 要求立即 activation。Firmware Commit 不是 background operation，會保持進行中直到 activation 成功或失敗；若 Firmware Activation notice 已啟用，受影響 controller 可（may）送出 Firmware Activation Starting event。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 文件頁 136, PDF 頁 162

<!-- claim:BASEFWLOG-FW-FAILURE -->

**[SPEC]** 若新 image 無法成功載入，controller 必須（shall）回復到最近 activation 的 slot image；若該 image 也無法載入，則載入可用的 baseline read-only image，並產生 Firmware Image Load Error event。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 文件頁 136-137, PDF 頁 162-163

<!-- claim:BASEFWLOG-RESET-XREF -->

**[SPEC]** NVMe over PCIe Transport 將 Conventional Reset 與 Function Level Reset 分別列為額外的 transport-specific Controller Level Reset 方法；除 Controller Reset 外，Controller Level Reset 會依 PCI Express Base Specification 重設 PCI register space。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.3, 文件頁 11, PDF 頁 11

<!-- claim:BASEFWLOG-UUID-LIST -->

**[SPEC]** firmware revisions 間的 UUID List 宜（should）保持 entry 位置穩定：新增 UUID 宜接在尾端；移除時宜原位改成 NVMe Invalid UUID；不宜重用 invalid entry，也不宜縮短或移除清單。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11.1, 文件頁 137-138, PDF 頁 163-164

<!-- claim:BASEFWLOG-UUID-RESET -->

**[SPEC]** 若 downloaded image 在既有 entry 中，以有效 UUID 取代 NVMe Invalid UUID 或另一個有效 UUID，controller 必須（shall）要求 reset；所有受這個 UUID List 變更影響的 controllers 都必須（shall）reset。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11.1, 文件頁 138, PDF 頁 164

<!-- claim:BASEFWLOG-XREF-337 -->

**[SPEC]** 來源 §5.2.9 將 Firmware Revision 欄位指向 Figure 337；但 Figure 337 是 Command Set Identifiers，FR 實際列在 Figure 338。未取得另行核准的 errata，因此保留並揭露這個來源內部交叉引用差異，不靜默改寫。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 5.2.14.1, 文件頁 202, 340, PDF 頁 228, 366

</details>

---

## Slide 07 — Status 決定 recovery

| SC | 意義 | 正確方向 |
|---|---|---|
| 06h／07h | invalid slot／image | 修正 target／image |
| 0Bh | 需要 Conventional Reset | 不可用 FLR 代替 |
| 10h | 需要 NVM Subsystem Reset | 小範圍 reset 仍跑舊 image |
| 11h | 需要 Controller Level Reset | 下次 CLR activation |
| 12h | maximum-time violation | image 已 commit；可用 CA=010b 排定 |
| 13h／14h | prohibited／overlap | 修正 policy／range |

---

## Slide 08 — 建構 LID 03h command

```text
512 bytes / 4 = 128 dwords
NUMD = 128 - 1 = 127 = 007Fh
CDW10 = NUMDL[31:16] | RAE=0 | LSP=0 | LID=03h
      = 007F0003h
```

來源地圖：Figure 93（文件/PDF 140-142/166-168）；Figures 203-209（213-216/239-242）。

<details markdown="1">
<summary><strong>講者備註／來源論點</strong></summary>

<!-- claim:BASEFWLOG-LOG-COMMAND -->

**[SPEC]** 讀 LID 03h 時，未使用 namespace，因此 NSID 必須（shall）為 0h；DPTR 以 PRP 指向 512-byte destination buffer。必要的 CDW10-CDW14 slice 為 LID=03h、LSP=0、RAE=0、NUMDL/NUMDU 表示 512 bytes、LSI=0、LPOL/LPOU=0、OT=0、UIDX=0；CSI 對 LID 03h 不使用，controller 依 Figure 208 規則忽略。

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 5.2.13, 文件頁 140-142, 212-215, PDF 頁 166-168, 238-241

<!-- claim:BASEFWLOG-LOG-LENGTH -->

**[SPEC]** NUMDL 與 NUMDU 合成 0's-based dword count。LID 03h 固定 512 bytes=128 dwords，因此 NUMD=127=0000007Fh，NUMDL=007Fh、NUMDU=0000h；在 LSP=0、RAE=0 下，CDW10=007F0003h。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, 文件頁 213-215, PDF 頁 239-241

<!-- claim:BASEFWLOG-LOG-RAE -->

**[SPEC]** RAE=0 會在 command 成功時清除對應 asynchronous event，RAE=1 則保留；若 command 未成功，controller 必須（shall）保留 event。Firmware Activation Starting event 要以 RAE=0 讀取 LID 03h 才會清除。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.2, 5.2.13, 文件頁 186, 213, PDF 頁 212, 239

<!-- claim:BASEFWLOG-LOG-OFFSET -->

**[SPEC]** 本報告以完整 512-byte LID 03h、LPOL=LPOU=0、OT=0 為基準。一般 byte offset 必須 dword aligned；超過 log page 大小的 offset 必須（shall）回 Invalid Field in Command。LID 03h 不需要 index-offset 分支。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, 文件頁 214-215, PDF 頁 240-241

<!-- claim:BASEFWLOG-LOG-SCOPE -->

**[SPEC]** Figure 209 的 LID 03h row 指定 CSI=N、scope=Domain／NVM subsystem、reference=§5.2.13.1.4。MDS=1 時回傳處理 command 之 controller 所屬 domain；否則回傳整個 NVM subsystem 的資訊。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, 文件頁 215-216, PDF 頁 241-242

</details>

---

## Slide 09 — 先解 AFI，再讀 revision strings

```text
byte 0: [7 R][6:4 NAFS][3 R][2:0 CAFS]
bytes 1:7: reserved
bytes 8:63: FRS1 ... FRS7 (8 bytes each)
bytes 64:511: reserved
```

**範例：**AFI=21h 代表 NAFS=2、CAFS=1；slot 2 pending，slot 1 仍在執行。

來源地圖：Figure 215（文件/PDF 226/252）。

<details markdown="1">
<summary><strong>講者備註／來源論點</strong></summary>

<!-- claim:BASEFWLOG-LID03-DESCRIPTION -->

**[SPEC]** Firmware Slot Information log page 固定 512 bytes，說明每個支援 slot 內的 firmware revision，並指出 current active slot 與（若 controller 有回報）next active slot。revision 以 ASCII string 表示。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, 文件頁 225-226, PDF 頁 251-252

<!-- claim:BASEFWLOG-LID03-AFI -->

**[SPEC]** byte 0 的 AFI 中，NAFS=bits 6:4、CAFS=bits 2:0；bits 7 與 3 reserved。NAFS 非零表示將於下一次能觸發 activation 的 CLR 啟用該 slot，NAFS=0 表示 controller 未指出 next slot；CAFS 是目前執行 image 的來源 slot。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, 文件頁 226, PDF 頁 252

<!-- claim:BASEFWLOG-LID03-FRS -->

**[SPEC]** FRS1 到 FRS7 位於 bytes 8-63，每格 8 bytes；slot 沒有有效 revision 或不支援時，該 FRS 必須（shall）清為 0h。bytes 1-7 與 64-511 reserved。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, 文件頁 226, PDF 頁 252

</details>

---

## Slide 10 — End-to-End Example

| 階段 | 具體值 | 證據 |
|---|---|---|
| Capability | NOFS=3、FFSRO=1、FWUG=1h | 選可寫 slot 2 |
| Download | NUMD=03FFh；OFST=0／0400h／0800h | 12 KiB transferred |
| Commit | CA=001b、FS=2、CDW10=0000000Ah | slot 2 pending |
| Pre-reset | LID03 CDW10=007F0003h、AFI=21h | CAFS1／NAFS2 |
| Post-reset | CAFS=2、FRS2=Identify.FR | activation verified |

---

## Slide 11 — 從第一個斷掉的邊界開始 Debug

| 症狀 | 第一證據 |
|---|---|
| Download Invalid Field | PRP、NUMD、OFST、FWUG |
| Commit invalid slot | NOFS、FFSRO、FS |
| reset-required SC | 完整 SCT／SC＋實際 reset trace |
| FRS2 valid、CAFS 仍 1 | CA、NAFS、reset type |
| controllers 結果不同 | MDS、DID、processing controller |

---

## Slide 12 — 結論與來源邊界

> 把 firmware update 當成具有 domain scope 的 state machine：command 推進狀態、completion status 選 recovery、LID 03h 證明最後 slot 狀態。

納入：§3.11、§3.11.1、§5.2.9、§5.2.10、§5.2.13 的 LID 03h 必要共通欄位、§5.2.13.1.4；主範圍文件頁 135-138、202-206、212-216、225-226，並含最小 dependency slice

查證日期：2026-09-01。未納入額外 Errata、ECN、vendor 文件或 PCI Express Base Specification 原文。

## 先學縮寫：完整 Glossary

下列縮寫會在投影片主線使用前先定義。縮寫本身永遠不夠；設計與 Debug 還要保留 owner、width、unit、scope 與 state。

| 縮寫／名詞 | 白話解釋 | 來源 |
|---|---|---|
| `LID` | Log Page Identifier，Get Log Page command 用來選擇 log page 的欄位。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1, 5.2.13，文件頁 140-142, 212-215，PDF 頁 166-168, 238-241 |
| `LID 03h` | Firmware Slot Information log page 的 identifier 03h。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.4，文件頁 225-226，PDF 頁 251-252 |
| `AFI` | Active Firmware Info，LID 03h 中同時包含目前 active slot 與下一次 reset 後預定 active slot 的 byte。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.4，文件頁 226，PDF 頁 252 |
| `CAFS` | Current Active Firmware Slot，AFI 低三 bits，指出目前正在執行的 firmware slot。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.4，文件頁 226，PDF 頁 252 |
| `NAFS` | Next Active Firmware Slot，AFI bits 6:4，指出下一次 reset 後預定啟用的 slot；0 表示未排定。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.4，文件頁 226，PDF 頁 252 |
| `FRS` | Firmware Revision for Slot，LID 03h 中每個 slot 的八-byte revision 字串欄位。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.4，文件頁 226，PDF 頁 252 |
| `FR` | Firmware Revision，Identify Controller 回報目前 active firmware revision 的八-byte ASCII 欄位。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.1，文件頁 340，PDF 頁 366 |
| `FRMW` | Firmware Updates，Identify Controller 中回報 slot 數、slot 1 read-only 與 activation 能力的欄位。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.1，文件頁 354，PDF 頁 380 |
| `FWUG` | Firmware Update Granularity，download portion 的 granularity／alignment 能力欄位。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.1，文件頁 359，PDF 頁 385 |
| `MTFA` | Maximum Time for Firmware Activation，activation 可能暫停 command processing 的最長時間。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.1，文件頁 357，PDF 頁 383 |
| `MPTFAWR` | Maximum Processing Time for Firmware Activation Without Reset，立即 activation 不需要 reset 時的最大處理時間。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.1，文件頁 364，PDF 頁 390 |
| `MDS` | Multiple Domain Subsystem，指出 NVM subsystem 是否包含多個 domains 的能力 bit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.1，文件頁 346, 364，PDF 頁 372, 390 |
| `DID` | Domain Identifier，辨識 NVM subsystem 內 domain 的 identifier。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.1，文件頁 346, 364，PDF 頁 372, 390 |
| `ULIST` | UUID List，指出 controller 是否支援 UUID List data structure 的能力 bit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.14.1，文件頁 346, 364，PDF 頁 372, 390 |
| `UUID` | Universally Unique Identifier，128-bit identifier；其實際關聯範圍仍由使用它的資料結構決定。 | NVME-BASE-2.4 Rev. 2.4，§3.11.1，文件頁 137-138，PDF 頁 163-164 |
| `DPTR` | Data Pointer，SQE 中指出 command data buffer 的欄位。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1, 5.2.10，文件頁 140-142, 205-206，PDF 頁 166-168, 231-232 |
| `PRP` | Physical Region Page，以 memory page 為單位描述 host-addressable data buffer 的 pointer 格式。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1, 5.2.10，文件頁 140-142, 205-206，PDF 頁 166-168, 231-232 |
| `NUMD` | Number of Dwords，0's-based transfer dword count；實際 bytes = (NUMD + 1) × 4。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1, 5.2.10，文件頁 140-142, 205-206，PDF 頁 166-168, 231-232 |
| `NUMDL` | Number of Dwords Lower，Get Log Page 的 NUMD 低 16 bits。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1, 5.2.13，文件頁 140-142, 212-215，PDF 頁 166-168, 238-241 |
| `NUMDU` | Number of Dwords Upper，Get Log Page 的 NUMD 高 16 bits。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1, 5.2.13，文件頁 140-142, 212-215，PDF 頁 166-168, 238-241 |
| `OFST` | Offset，Firmware Image Download 中以 dword 為單位的 image-relative offset。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1, 5.2.10，文件頁 140-142, 205-206，PDF 頁 166-168, 231-232 |
| `RAE` | Retain Asynchronous Event，Get Log Page 是否保留相關 asynchronous event 的 selector。 | NVME-BASE-2.4 Rev. 2.4，§5.2.2, 5.2.13，文件頁 186, 213，PDF 頁 212, 239 |
| `LSP` | Log Specific Field，意義由所選 log page 定義的 command selector。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1, 5.2.13，文件頁 140-142, 212-215，PDF 頁 166-168, 238-241 |
| `LSI` | Log Specific Identifier，意義由所選 log page 定義的 identifier。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1, 5.2.13，文件頁 140-142, 212-215，PDF 頁 166-168, 238-241 |
| `LPOL` | Log Page Offset Lower，Get Log Page byte offset 的低 32 bits。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13，文件頁 214-215，PDF 頁 240-241 |
| `LPOU` | Log Page Offset Upper，Get Log Page byte offset 的高 32 bits。 | NVME-BASE-2.4 Rev. 2.4，§5.2.13，文件頁 214-215，PDF 頁 240-241 |
| `CSI` | Command Set Identifier，選擇與 log page 相關的 command set context。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1, 5.2.13，文件頁 140-142, 212-215，PDF 頁 166-168, 238-241 |
| `UIDX` | UUID Index，指向 UUID List 位置的 index；0 表示未指定 UUID。 | NVME-BASE-2.4 Rev. 2.4，§4.1.1, 5.2.13，文件頁 140-142, 212-215，PDF 頁 166-168, 238-241 |
| `CA` | Commit Action，Firmware Commit 中選擇 replace、activate 與 reset policy 的欄位。 | NVME-BASE-2.4 Rev. 2.4，§5.2.9，文件頁 203，PDF 頁 229 |
| `FS` | Firmware Slot，Firmware Commit 中選擇目標 slot 的欄位。 | NVME-BASE-2.4 Rev. 2.4，§5.2.9，文件頁 203，PDF 頁 229 |
| `MUD` | Multiple Update Detected，completion 中指出 controller 偵測到 overlapping firmware update sequence 的 bit。 | NVME-BASE-2.4 Rev. 2.4，§5.2.9，文件頁 204，PDF 頁 230 |
| `SCT` | Status Code Type，先決定 status 所屬大類，再解讀 SC。 | NVME-BASE-2.4 Rev. 2.4，§5.2.9，文件頁 204-205，PDF 頁 230-231 |
| `SC` | Status Code，在 SCT 上下文中表示具體完成結果的 code。 | NVME-BASE-2.4 Rev. 2.4，§5.2.9，文件頁 204-205，PDF 頁 230-231 |
| `CQE` | Completion Queue Entry，CQ 中的一筆完成結果資料結構。 | NVME-BASE-2.4 Rev. 2.4，§5.2.9，文件頁 204-205，PDF 頁 230-231 |
| `AEN` | Asynchronous Event Notification，controller 透過已提交 Asynchronous Event Request 回報事件的通知。 | NVME-BASE-2.4 Rev. 2.4，§5.2.2, 5.2.13，文件頁 186, 213，PDF 頁 212, 239 |

## Visual Atlas：先用圖建立整體位置

每張教學重畫回答不同問題：Architecture 定位元件、Sequence 顯示 ownership、Decode 把 bits 轉成工程值、State 保留 failure evidence；它們不是 Spec 原圖的複製。

### Visual 01: 先讀能力，再決定 firmware update 計畫

**View type:** `architecture`

```text
[Identify Controller snapshot]
  ├─ [FRMW：slot／activation]
  ├─ [FWUG：chunk／alignment]
  ├─ [MTFA／MPTFAWR：timeout]
  ├─ [MDS／DID：sharing scope]
  └─ [產生合法更新計畫]
```

**回答的問題：** Firmware update 不是固定 command recipe。FRMW 決定 slot 與 activation 能力，FWUG 決定 download chunk 的 granularity／alignment，MTFA 與 MPTFAWR 決定 host 能等待多久，MDS／DID 則決定結果影響哪一組 controllers。

**支援 Figure：** Figure 337, Figure 338

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.14.1，文件頁 354，PDF 頁 380; NVME-BASE-2.4 Rev. 2.4，§5.2.14.1，文件頁 359，PDF 頁 385; NVME-BASE-2.4 Rev. 2.4，§5.2.14.1，文件頁 357，PDF 頁 383; NVME-BASE-2.4 Rev. 2.4，§5.2.14.1，文件頁 364，PDF 頁 390; NVME-BASE-2.4 Rev. 2.4，§5.2.14.1，文件頁 346, 364，PDF 頁 372, 390

### Visual 02: Download 是 byte range 幾何，不是把檔案直接丟給 controller

**View type:** `architecture`

```text
[image bytes]
  ├─ [依 FWUG 切 portions]
  ├─ [bytes ÷ 4 → dwords]
  ├─ [NUMD = dwords - 1]
  ├─ [OFST = 已送 bytes ÷ 4]
  └─ [CQE success 後前進]
```

**回答的問題：** 每筆 Firmware Image Download 都用 DPTR 指向 host buffer，再用 0's-based NUMD 表示 transfer dwords、用 OFST 表示 image-relative dword offset。host 必須同時證明 buffer、length、offset、FWUG 與前後 portions 沒有 gap／overlap。

**支援 Figure：** Figure 93, Figure 190, Figure 191, Figure 192, Figure 193

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.10，文件頁 205-206，PDF 頁 231-232; NVME-BASE-2.4 Rev. 2.4，§4.1.1, 5.2.10，文件頁 140-142, 205-206，PDF 頁 166-168, 231-232

### Visual 03: Commit 把 downloaded portions 轉成 slot state 與 activation policy

**View type:** `architecture`

```text
[downloaded portions 完整]
  ├─ [填 CA／FS]
  ├─ [controller 驗證 image]
  ├─ [放入 slot／排定或立即 activation]
  ├─ [解完整 SCT／SC／MUD]
  └─ [依 status 選 reset／verify／stop]
```

**回答的問題：** Commit Action（CA）不是成功／失敗旗標；它同時決定 replace、activate 與 reset boundary。Firmware Slot（FS）選擇目標 slot，CQE status 決定下一步是驗證、執行特定 reset、等待，還是停止。

**支援 Figure：** Figure 187, Figure 188, Figure 189

**來源：** NVME-BASE-2.4 Rev. 2.4，§5.2.9，文件頁 202-203，PDF 頁 228-229; NVME-BASE-2.4 Rev. 2.4，§5.2.9，文件頁 203，PDF 頁 229; NVME-BASE-2.4 Rev. 2.4，§5.2.9，文件頁 204，PDF 頁 230; NVME-BASE-2.4 Rev. 2.4，§5.2.9，文件頁 204-205，PDF 頁 230-231

### Visual 04: LID 03h 驗證不是只讀一個版本字串

**View type:** `architecture`

```text
[建立 Get Log Page SQE]
  ├─ [LID=03h／NUMD=127]
  ├─ [讀滿 512-byte buffer]
  ├─ [AFI → CAFS／NAFS]
  ├─ [FRS1-FRS7 逐 slot 解碼]
  └─ [與 Identify.FR／預期 domain 比對]
```

**回答的問題：** Get Log Page 先用 common command 欄位建立 512-byte transfer，再以 LID=03h 選 Firmware Slot Information。AFI 同時拆成 CAFS 與 NAFS，FRS1-FRS7 表示各 slots 的 revision；最後還要用 Identify.FR 與 domain scope 交叉確認。

**支援 Figure：** Figure 203, Figure 204, Figure 205, Figure 206, Figure 207, Figure 208, Figure 209, Figure 215, Figure 338

**來源：** NVME-BASE-2.4 Rev. 2.4，§4.1.1, 5.2.13，文件頁 140-142, 212-215，PDF 頁 166-168, 238-241; NVME-BASE-2.4 Rev. 2.4，§5.2.13，文件頁 213-215，PDF 頁 239-241; NVME-BASE-2.4 Rev. 2.4，§5.2.13，文件頁 215-216，PDF 頁 241-242; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.4，文件頁 226，PDF 頁 252; NVME-BASE-2.4 Rev. 2.4，§5.2.13.1.4，文件頁 226，PDF 頁 252; NVME-BASE-2.4 Rev. 2.4，§5.2.14.1，文件頁 340，PDF 頁 366

## Appendix A — Supporting Figure / Field Reference

Figure 是主流程的可追溯證據，不是文章骨架。dependency entries 只取理解所需切片；Figure 209 只保留 LID 03h row。

<details markdown="1">
<summary><strong>Figure 187: Firmware Commit – Command Dword 10</strong></summary>

<!-- claim:BASEFWLOG-FIG-187-CLAIM figure-table:BASEFWLOG-FIG-187 -->

**SPEC。** Figure 187〈Firmware Commit – Command Dword 10〉：定義〈Firmware Commit – Command Dword 10〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：BPID, CA, FS。

#### 這張 Figure 在完整流程中的位置

Figure 187 位於 §5.2.9，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 BPID 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: BPID]
          ↓
[擷取欄位: CA] → [套用編碼: FS]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `BPID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CA` | Commit Action，Firmware Commit 中選擇 replace、activate 與 reset policy 的欄位。 |
| `FS` | Firmware Slot，Firmware Commit 中選擇目標 slot 的欄位。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.9。
2. 依圖中指定的寬度與位置解碼 BPID；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CA 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §5.2.9 如何排列 BPID、CA 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.9 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 187 對應的 raw value 或 buffer，標出包含 BPID 的 bytes 並解碼，再獨立核對 CA。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 CA 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** BPID, CA, FS

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, Figure 187, 文件頁 203, PDF 頁 229

</details>

<details markdown="1">
<summary><strong>Figure 188: Firmware Commit – Completion Queue Entry Dword 0</strong></summary>

<!-- claim:BASEFWLOG-FIG-188-CLAIM figure-table:BASEFWLOG-FIG-188 -->

**SPEC。** Figure 188〈Firmware Commit – Completion Queue Entry Dword 0〉：呈現〈Firmware Commit – Completion Queue Entry Dword 0〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：MUD, MEFWO, ASQFWO。

#### 這張 Figure 在完整流程中的位置

Figure 188 位於 §5.2.9.1，在本流程中是「queue」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 MUD 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 queue／command flow 圖。先標 host 與 controller 的 ownership，再追 head、tail、phase 或 arbitration 的改變；箭頭代表狀態或 ownership 轉移，不自動代表 command 已完成。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: MUD]
          ↓
[擷取欄位: MEFWO] → [套用編碼: ASQFWO]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `MUD` | Multiple Update Detected，completion 中指出 controller 偵測到 overlapping firmware update sequence 的 bit。 |
| `MEFWO` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `ASQFWO` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.9.1。
2. 依圖中指定的寬度與位置解碼 MUD；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MEFWO 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §5.2.9.1 如何排列 MUD、MEFWO 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.9.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 188 對應的 raw value 或 buffer，標出包含 MUD 的 bytes 並解碼，再獨立核對 MEFWO。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 MUD，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 MUD 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MEFWO 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** MUD, MEFWO, ASQFWO

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 188, 文件頁 204, PDF 頁 230

</details>

<details markdown="1">
<summary><strong>Figure 189: Firmware Commit – Command Specific Status Values</strong></summary>

<!-- claim:BASEFWLOG-FIG-189-CLAIM figure-table:BASEFWLOG-FIG-189 -->

**SPEC。** Figure 189〈Firmware Commit – Command Specific Status Values〉：定義〈Firmware Commit – Command Specific Status Values〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Invalid Firmware Slot, Invalid Firmware Image, reset-required status, MTFA, Overlapping Range。

#### 這張 Figure 在完整流程中的位置

Figure 189 位於 §5.2.9.1，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Invalid Firmware Slot 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Invalid Firmware Slot]
          ↓
[擷取欄位: Invalid Firmware Image] → [套用編碼: reset-required status]
                                      ↓
[驗證證據: MTFA]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Invalid Firmware Slot` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Invalid Firmware Image` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `reset-required status` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MTFA` | Maximum Time for Firmware Activation，activation 可能暫停 command processing 的最長時間。 |
| `Overlapping Range` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.9.1。
2. 依圖中指定的寬度與位置解碼 Invalid Firmware Slot；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 Invalid Firmware Image 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §5.2.9.1 如何排列 Invalid Firmware Slot、Invalid Firmware Image 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.9.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 189 對應的 raw value 或 buffer，標出包含 Invalid Firmware Slot 的 bytes 並解碼，再獨立核對 Invalid Firmware Image。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Invalid Firmware Slot，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Invalid Firmware Slot 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 Invalid Firmware Image 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Invalid Firmware Slot, Invalid Firmware Image, reset-required status, MTFA, Overlapping Range

**來源 keyword 索引：** `shall`, `should`, `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 189, 文件頁 204-205, PDF 頁 230-231

</details>

<details markdown="1">
<summary><strong>Figure 190: Firmware Image Download – Data Pointer</strong></summary>

<!-- claim:BASEFWLOG-FIG-190-CLAIM figure-table:BASEFWLOG-FIG-190 -->

**SPEC。** Figure 190〈Firmware Image Download – Data Pointer〉：定義〈Firmware Image Download – Data Pointer〉如何指出本命令的來源或目的 buffer。 先判斷 pointer type 與 address，再核對 transfer length 和 alignment；來源欄位索引：DPTR。

#### 這張 Figure 在完整流程中的位置

Figure 190 位於 §5.2.10，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DPTR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

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

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.10。
2. 依圖中指定的寬度與位置解碼 DPTR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §5.2.10 如何排列 DPTR、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.10 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 190 對應的 raw value 或 buffer，標出包含 DPTR 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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

**來源 keyword 索引：** `should`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 190, 文件頁 205, PDF 頁 231

</details>

<details markdown="1">
<summary><strong>Figure 191: Firmware Image Download – Command Dword 10</strong></summary>

<!-- claim:BASEFWLOG-FIG-191-CLAIM figure-table:BASEFWLOG-FIG-191 -->

**SPEC。** Figure 191〈Firmware Image Download – Command Dword 10〉：定義〈Firmware Image Download – Command Dword 10〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NUMD, FWUG。

#### 這張 Figure 在完整流程中的位置

Figure 191 位於 §5.2.10，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NUMD 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NUMD]
          ↓
[擷取欄位: FWUG] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NUMD` | Number of Dwords，0's-based transfer dword count；實際 bytes = (NUMD + 1) × 4。 |
| `FWUG` | Firmware Update Granularity，download portion 的 granularity／alignment 能力欄位。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.10。
2. 依圖中指定的寬度與位置解碼 NUMD；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 FWUG 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §5.2.10 如何排列 NUMD、FWUG 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.10 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 191 對應的 raw value 或 buffer，標出包含 NUMD 的 bytes 並解碼，再獨立核對 FWUG。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 NUMD，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 NUMD 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 FWUG 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** NUMD, FWUG

**來源 keyword 索引：** `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 191, 文件頁 205, PDF 頁 231

</details>

<details markdown="1">
<summary><strong>Figure 192: Firmware Image Download – Command Dword 11</strong></summary>

<!-- claim:BASEFWLOG-FIG-192-CLAIM figure-table:BASEFWLOG-FIG-192 -->

**SPEC。** Figure 192〈Firmware Image Download – Command Dword 11〉：定義〈Firmware Image Download – Command Dword 11〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：OFST, FWUG。

#### 這張 Figure 在完整流程中的位置

Figure 192 位於 §5.2.10，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 OFST 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: OFST]
          ↓
[擷取欄位: FWUG] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `OFST` | Offset，Firmware Image Download 中以 dword 為單位的 image-relative offset。 |
| `FWUG` | Firmware Update Granularity，download portion 的 granularity／alignment 能力欄位。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.10。
2. 依圖中指定的寬度與位置解碼 OFST；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 FWUG 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §5.2.10 如何排列 OFST、FWUG 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.10 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 192 對應的 raw value 或 buffer，標出包含 OFST 的 bytes 並解碼，再獨立核對 FWUG。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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
2. 能否說明為什麼 FWUG 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** OFST, FWUG

**來源 keyword 索引：** none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 192, 文件頁 206, PDF 頁 232

</details>

<details markdown="1">
<summary><strong>Figure 193: Firmware Image Download – Command Specific Status Values</strong></summary>

<!-- claim:BASEFWLOG-FIG-193-CLAIM figure-table:BASEFWLOG-FIG-193 -->

**SPEC。** Figure 193〈Firmware Image Download – Command Specific Status Values〉：定義〈Firmware Image Download – Command Specific Status Values〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Overlapping Range。

#### 這張 Figure 在完整流程中的位置

Figure 193 位於 §5.2.10，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Overlapping Range 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

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

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.10。
2. 依圖中指定的寬度與位置解碼 Overlapping Range；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

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
| 這張圖回答 | §5.2.10 如何排列 Overlapping Range、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.10 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 193 對應的 raw value 或 buffer，標出包含 Overlapping Range 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Overlapping Range，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Overlapping Range 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Overlapping Range

**來源 keyword 索引：** `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 193, 文件頁 206, PDF 頁 232

</details>

<details markdown="1">
<summary><strong>Figure 203: Get Log Page – Data Pointer</strong></summary>

<!-- claim:BASEFWLOG-FIG-203-CLAIM figure-table:BASEFWLOG-FIG-203 -->

**SPEC。** Figure 203〈Get Log Page – Data Pointer〉：定義〈Get Log Page – Data Pointer〉如何指出本命令的來源或目的 buffer。 先判斷 pointer type 與 address，再核對 transfer length 和 alignment；來源欄位索引：DPTR。

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
<summary><strong>Figure 204: Get Log Page – Command Dword 10</strong></summary>

<!-- claim:BASEFWLOG-FIG-204-CLAIM figure-table:BASEFWLOG-FIG-204 -->

**SPEC。** Figure 204〈Get Log Page – Command Dword 10〉：定義〈Get Log Page – Command Dword 10〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：NUMDL, RAE, LSP, LID。

#### 這張 Figure 在完整流程中的位置

Figure 204 位於 §5.2.13，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 NUMDL 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: NUMDL]
          ↓
[擷取欄位: RAE] → [套用編碼: LSP]
                                      ↓
[驗證證據: LID]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `NUMDL` | Number of Dwords Lower，Get Log Page 的 NUMD 低 16 bits。 |
| `RAE` | Retain Asynchronous Event，Get Log Page 是否保留相關 asynchronous event 的 selector。 |
| `LSP` | Log Specific Field，意義由所選 log page 定義的 command selector。 |
| `LID` | Log Page Identifier，Get Log Page command 用來選擇 log page 的欄位。 |

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

**來源欄位索引：** NUMDL, RAE, LSP, LID

**來源 keyword 索引：** `shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 204, 文件頁 213, PDF 頁 239

</details>

<details markdown="1">
<summary><strong>Figure 205: Get Log Page – Command Dword 11</strong></summary>

<!-- claim:BASEFWLOG-FIG-205-CLAIM figure-table:BASEFWLOG-FIG-205 -->

**SPEC。** Figure 205〈Get Log Page – Command Dword 11〉：定義〈Get Log Page – Command Dword 11〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LSI, NUMDU。

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
<summary><strong>Figure 206: Get Log Page – Command Dword 12</strong></summary>

<!-- claim:BASEFWLOG-FIG-206-CLAIM figure-table:BASEFWLOG-FIG-206 -->

**SPEC。** Figure 206〈Get Log Page – Command Dword 12〉：定義〈Get Log Page – Command Dword 12〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LPOL, OT。

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
<summary><strong>Figure 207: Get Log Page – Command Dword 13</strong></summary>

<!-- claim:BASEFWLOG-FIG-207-CLAIM figure-table:BASEFWLOG-FIG-207 -->

**SPEC。** Figure 207〈Get Log Page – Command Dword 13〉：定義〈Get Log Page – Command Dword 13〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LPOU。

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
<summary><strong>Figure 208: Get Log Page – Command Dword 14</strong></summary>

<!-- claim:BASEFWLOG-FIG-208-CLAIM figure-table:BASEFWLOG-FIG-208 -->

**SPEC。** Figure 208〈Get Log Page – Command Dword 14〉：定義〈Get Log Page – Command Dword 14〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CSI, OT, UIDX。

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
| `CSI` | Command Set Identifier，選擇與 log page 相關的 command set context。 |
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
<summary><strong>Figure 209: Get Log Page – Log Page Identifiers</strong></summary>

<!-- claim:BASEFWLOG-FIG-209-CLAIM figure-table:BASEFWLOG-FIG-209 -->

**SPEC。** Figure 209〈Get Log Page – Log Page Identifiers〉：定義〈Get Log Page – Log Page Identifiers〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LID 03h, CSI = N, Domain / NVM subsystem, Firmware Slot Information, §5.2.13.1.4, MDS。

#### 這張 Figure 在完整流程中的位置

Figure 209 位於 §5.2.13，在本流程中是「identifier」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 LID 03h 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 identifier 格式圖。先記錄 width 與 encoding，再辨識 issuing authority、uniqueness scope、reserved value 與有效生命週期；不要把長度相同的 identifiers 當成可互換。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: LID 03h]
          ↓
[擷取欄位: CSI = N] → [套用編碼: Domain / NVM subsystem]
                                      ↓
[驗證證據: Firmware Slot Information]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `LID 03h` | Firmware Slot Information log page 的 identifier 03h。 |
| `CSI = N` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Domain / NVM subsystem` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `Firmware Slot Information` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `§5.2.13.1.4` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `MDS` | Multiple Domain Subsystem，指出 NVM subsystem 是否包含多個 domains 的能力 bit。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.13。
2. 依圖中指定的寬度與位置解碼 LID 03h；縮寫本身不能用來猜 unit、reset value 或 encoding。
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
| 這張圖回答 | §5.2.13 如何排列 LID 03h、CSI = N 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.13 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 209 對應的 raw value 或 buffer，標出包含 LID 03h 的 bytes 並解碼，再獨立核對 CSI = N。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 LID 03h，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 LID 03h 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CSI = N 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** LID 03h, CSI = N, Domain / NVM subsystem, Firmware Slot Information, §5.2.13.1.4, MDS

**來源 keyword 索引：** `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 209, 文件頁 215-216, PDF 頁 241-242

</details>

<details markdown="1">
<summary><strong>Figure 215: Firmware Slot Information Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-215-CLAIM figure-table:BASEFWLOG-FIG-215 -->

**SPEC。** Figure 215〈Firmware Slot Information Log Page〉：定義〈Firmware Slot Information Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：AFI, NAFS, CAFS, FRS1, FRS2, FRS3, FRS4, FRS5, FRS6, FRS7, Reserved bytes 1:7 and 64:511。

#### 這張 Figure 在完整流程中的位置

Figure 215 位於 §5.2.13.1.4，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 AFI 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: AFI]
          ↓
[擷取欄位: NAFS] → [套用編碼: CAFS]
                                      ↓
[驗證證據: FRS1]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `AFI` | Active Firmware Info，LID 03h 中同時包含目前 active slot 與下一次 reset 後預定 active slot 的 byte。 |
| `NAFS` | Next Active Firmware Slot，AFI bits 6:4，指出下一次 reset 後預定啟用的 slot；0 表示未排定。 |
| `CAFS` | Current Active Firmware Slot，AFI 低三 bits，指出目前正在執行的 firmware slot。 |
| `FRS1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FRS2` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FRS3` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.13.1.4。
2. 依圖中指定的寬度與位置解碼 AFI；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 NAFS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 215 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.13.1.4 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.13.1.4 如何排列 AFI、NAFS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.13.1.4 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 215 對應的 raw value 或 buffer，標出包含 AFI 的 bytes 並解碼，再獨立核對 NAFS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 AFI，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 AFI 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 NAFS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** AFI, NAFS, CAFS, FRS1, FRS2, FRS3, FRS4, FRS5, FRS6, FRS7, Reserved bytes 1:7 and 64:511

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, Figure 215, 文件頁 226, PDF 頁 252

</details>

<details markdown="1">
<summary><strong>Figure 93: Common Command Format</strong></summary>

<!-- claim:BASEFWLOG-FIG-093-CLAIM figure-table:BASEFWLOG-FIG-093 -->

**SPEC。** Figure 93〈Common Command Format〉：定義〈Common Command Format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DPTR, PRP1, PRP2, SGL1。

#### 這張 Figure 在完整流程中的位置

Figure 93 位於 §4.1.1，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 DPTR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: DPTR]
          ↓
[擷取欄位: PRP1] → [套用編碼: PRP2]
                                      ↓
[驗證證據: SGL1]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `DPTR` | Data Pointer，SQE 中指出 command data buffer 的欄位。 |
| `PRP1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `PRP2` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `SGL1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §4.1.1。
2. 依圖中指定的寬度與位置解碼 DPTR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 PRP1 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
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
| 這張圖回答 | §4.1.1 如何排列 DPTR、PRP1 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §4.1.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 93 對應的 raw value 或 buffer，標出包含 DPTR 的 bytes 並解碼，再獨立核對 PRP1。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

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

**來源欄位索引：** DPTR, PRP1, PRP2, SGL1

**來源 keyword 索引：** `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, 文件頁 140-142, PDF 頁 166-168

</details>

<details markdown="1">
<summary><strong>Figure 155: Asynchronous Event Information – Notice</strong></summary>

<!-- claim:BASEFWLOG-FIG-155-CLAIM figure-table:BASEFWLOG-FIG-155 -->

**SPEC。** Figure 155〈Asynchronous Event Information – Notice〉：定義〈Asynchronous Event Information – Notice〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：Firmware Activation Starting, CSTS.PP, Firmware Slot Information, RAE。

#### 這張 Figure 在完整流程中的位置

Figure 155 位於 §5.2.2.1，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Firmware Activation Starting 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Firmware Activation Starting]
          ↓
[擷取欄位: CSTS.PP] → [套用編碼: Firmware Slot Information]
                                      ↓
[驗證證據: RAE]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Firmware Activation Starting` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `CSTS.PP` | Controller Status，controller 回報 ready、fatal status 與 shutdown 狀態的 property。 此處的 CSTS.PP 進一步指定其中的 PP 子欄位。 |
| `Firmware Slot Information` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `RAE` | Retain Asynchronous Event，Get Log Page 是否保留相關 asynchronous event 的 selector。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.2.1。
2. 依圖中指定的寬度與位置解碼 Firmware Activation Starting；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 CSTS.PP 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
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
| 這張圖回答 | §5.2.2.1 如何排列 Firmware Activation Starting、CSTS.PP 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.2.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 155 對應的 raw value 或 buffer，標出包含 Firmware Activation Starting 的 bytes 並解碼，再獨立核對 CSTS.PP。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Firmware Activation Starting，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Firmware Activation Starting 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 CSTS.PP 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Firmware Activation Starting, CSTS.PP, Firmware Slot Information, RAE

**來源 keyword 索引：** `shall not`, `shall`, `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 155, 文件頁 186, PDF 頁 212

</details>

<details markdown="1">
<summary><strong>Figure 337: Command Set Identifiers</strong></summary>

<!-- claim:BASEFWLOG-FIG-337-CLAIM figure-table:BASEFWLOG-FIG-337 -->

**SPEC。** Figure 337〈Command Set Identifiers〉：定義〈Command Set Identifiers〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：Command Set Identifier。

#### 這張 Figure 在完整流程中的位置

Figure 337 位於 §5.2.14.1，在本流程中是「identifier」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Command Set Identifier 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 identifier 格式圖。先記錄 width 與 encoding，再辨識 issuing authority、uniqueness scope、reserved value 與有效生命週期；不要把長度相同的 identifiers 當成可互換。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Command Set Identifier]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Command Set Identifier` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.14.1。
2. 依圖中指定的寬度與位置解碼 Command Set Identifier；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 337 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.14.1 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.14.1 如何排列 Command Set Identifier、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.14.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 337 對應的 raw value 或 buffer，標出包含 Command Set Identifier 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Command Set Identifier，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Command Set Identifier 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Command Set Identifier

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, Figure 337, 文件頁 340, PDF 頁 366

</details>

<details markdown="1">
<summary><strong>Figure 338: Identify – Identify Controller Data Structure, I/O Command Set Independent</strong></summary>

<!-- claim:BASEFWLOG-FIG-338-CLAIM figure-table:BASEFWLOG-FIG-338 -->

**SPEC。** Figure 338〈Identify – Identify Controller Data Structure, I/O Command Set Independent〉：定義〈Identify – Identify Controller Data Structure, I/O Command Set Independent〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：FR, MDS, ULIST, SMUD, FAWR, NOFS, FFSRO, MTFA, FWUG, DID, MPTFAWR。

#### 這張 Figure 在完整流程中的位置

Figure 338 位於 §5.2.14.2.1，在本流程中是「layout」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 FR 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張結構／能力欄位表。先用結構 base 與 offset 定位，依 byte/bit 順序讀取，再把 capability gate、value encoding 與 reserved area 分開。表中的存在不等於功能一定支援。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: FR]
          ↓
[擷取欄位: MDS] → [套用編碼: ULIST]
                                      ↓
[驗證證據: SMUD]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `FR` | Firmware Revision，Identify Controller 回報目前 active firmware revision 的八-byte ASCII 欄位。 |
| `MDS` | Multiple Domain Subsystem，指出 NVM subsystem 是否包含多個 domains 的能力 bit。 |
| `ULIST` | UUID List，指出 controller 是否支援 UUID List data structure 的能力 bit。 |
| `SMUD` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `FAWR` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NOFS` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.14.2.1。
2. 依圖中指定的寬度與位置解碼 FR；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 MDS 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
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
| 這張圖回答 | §5.2.14.2.1 如何排列 FR、MDS 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.14.2.1 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 338 對應的 raw value 或 buffer，標出包含 FR 的 bytes 並解碼，再獨立核對 MDS。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 FR，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 FR 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 MDS 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** FR, MDS, ULIST, SMUD, FAWR, NOFS, FFSRO, MTFA, FWUG, DID, MPTFAWR

**來源 keyword 索引：** `shall not`, `shall`, `should`, `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, 文件頁 340-364, PDF 頁 366-390

</details>

<details markdown="1">
<summary><strong>Figure 347: UUID List</strong></summary>

<!-- claim:BASEFWLOG-FIG-347-CLAIM figure-table:BASEFWLOG-FIG-347 -->

**SPEC。** Figure 347〈UUID List〉：定義〈UUID List〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：UUID1, UUID2, UUID126, UUID127, NVMe Invalid UUID。

#### 這張 Figure 在完整流程中的位置

Figure 347 位於 §5.2.14.2.14，在本流程中是「identifier」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 UUID1 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 identifier 格式圖。先記錄 width 與 encoding，再辨識 issuing authority、uniqueness scope、reserved value 與有效生命週期；不要把長度相同的 identifiers 當成可互換。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: UUID1]
          ↓
[擷取欄位: UUID2] → [套用編碼: UUID126]
                                      ↓
[驗證證據: UUID127]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `UUID1` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `UUID2` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `UUID126` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `UUID127` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `NVMe Invalid UUID` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.14.2.14。
2. 依圖中指定的寬度與位置解碼 UUID1；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 UUID2 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 347 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.14.2.14 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.14.2.14 如何排列 UUID1、UUID2 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.14.2.14 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 347 對應的 raw value 或 buffer，標出包含 UUID1 的 bytes 並解碼，再獨立核對 UUID2。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 UUID1，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 UUID1 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 UUID2 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** UUID1, UUID2, UUID126, UUID127, NVMe Invalid UUID

**來源 keyword 索引：** `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.14, Figure 347, 文件頁 396, PDF 頁 422

</details>

<details markdown="1">
<summary><strong>Figure 348: UUID List Entry</strong></summary>

<!-- claim:BASEFWLOG-FIG-348-CLAIM figure-table:BASEFWLOG-FIG-348 -->

**SPEC。** Figure 348〈UUID List Entry〉：定義〈UUID List Entry〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：ULEH, IDASSOC, UUID。

#### 這張 Figure 在完整流程中的位置

Figure 348 位於 §5.2.14.2.14，在本流程中是「identifier」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 ULEH 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 identifier 格式圖。先記錄 width 與 encoding，再辨識 issuing authority、uniqueness scope、reserved value 與有效生命週期；不要把長度相同的 identifiers 當成可互換。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: ULEH]
          ↓
[擷取欄位: IDASSOC] → [套用編碼: UUID]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `ULEH` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `IDASSOC` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |
| `UUID` | Universally Unique Identifier，128-bit identifier；其實際關聯範圍仍由使用它的資料結構決定。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.14.2.14。
2. 依圖中指定的寬度與位置解碼 ULEH；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 IDASSOC 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
4. 保留值維持未解讀；把結果轉成 software state 前，先保存 raw bytes 或完整 register value。

#### Input → Decode → Validate → Evidence 工作紙

| 階段 | 要記錄什麼 | 停止條件 |
|---|---|---|
| Input | Figure 348 對應的完整 raw register／buffer／CQE snapshot | 來源物件、scope 或 snapshot 時機不明 |
| Decode | 來源欄位、byte／bit range、unit 與 encoding rule | 任一邊界、單位或編碼尚未確認 |
| Validate | §5.2.14.2.14 前後條件、capability gate、實際 length／state | reserved、越界、unsupported 或互斥條件衝突 |
| Evidence | raw value、decoded value、decision、timestamp 與 owner | 只有結論、沒有可重算證據 |

#### 這張圖能回答什麼，不能回答什麼

| 判讀層級 | 內容 |
|---|---|
| 這張圖回答 | §5.2.14.2.14 如何排列 ULEH、IDASSOC 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.14.2.14 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 348 對應的 raw value 或 buffer，標出包含 ULEH 的 bytes 並解碼，再獨立核對 IDASSOC。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 ULEH，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 ULEH 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 IDASSOC 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** ULEH, IDASSOC, UUID

**來源 keyword 索引：** `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.14, Figure 348, 文件頁 396, PDF 頁 422

</details>

<details markdown="1">
<summary><strong>Figure 474: Asynchronous Event Configuration – Command Dword 11</strong></summary>

<!-- claim:BASEFWLOG-FIG-474-CLAIM figure-table:BASEFWLOG-FIG-474 -->

**SPEC。** Figure 474〈Asynchronous Event Configuration – Command Dword 11〉：定義〈Asynchronous Event Configuration – Command Dword 11〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：Firmware Activation Notices。

#### 這張 Figure 在完整流程中的位置

Figure 474 位於 §5.2.30.1.6，在本流程中是「command」檢查點。先由主教學確認 owner 與物件層級，再用本圖把 Firmware Activation Notices 轉成可驗證的欄位；Figure 支援引用段落，但不能取代前後 normative 文字。

這是一張 command construction 欄位表。先建立 common SQE，再定位指定 CDW，依 bit range 填值，清除 reserved bits，最後配合 transfer length、buffer 與 completion status 驗證。欄位名稱相同也不代表不同 command 具有相同語意。

#### 教學重畫（非 Spec 原圖）

```text
[定位來源: Firmware Activation Notices]
          ↓
[擷取欄位: evidence] → [套用編碼: evidence]
                                      ↓
[驗證證據: evidence]
```

#### 讀圖前先懂這些縮寫／欄位

| 縮寫／欄位 | 白話解釋 |
|---|---|
| `Firmware Activation Notices` | 這是本 Figure 內的來源欄位名稱；使用前要回到引用 Figure 核對 bit range、編碼值與適用條件。 |

#### 照這個順序讀，不要直接跳到數值

1. 先由 caption 找到資料結構、register、queue 或物件，並確認目前適用的上下文確實是 §5.2.30.1.6。
2. 依圖中指定的寬度與位置解碼 Firmware Activation Notices；縮寫本身不能用來猜 unit、reset value 或 encoding。
3. 把 引用條件 當成獨立條件交叉檢查，再以實際 buffer 長度與 capability gate 驗證 count、address、selector 或 state。
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
| 這張圖回答 | §5.2.30.1.6 如何排列 Firmware Activation Notices、引用條件 與其他來源欄位。 |
| 這張圖不回答 | optional capability 是否已實作、command 是否完成，或另一個 scope 的同名值是否相等。 |
| 還要交叉檢查 | §5.2.30.1.6 前後文字、啟用此結構的 capability，以及實際 transfer／register width。 |

**說明性範例。** 說明性範例（informative example）：保存 Figure 474 對應的 raw value 或 buffer，標出包含 Firmware Activation Notices 的 bytes 並解碼，再獨立核對 引用條件。若任一欄位超出實際回傳邊界、選到 reserved encoding，或與 capability context 衝突，parser／command builder 應停止並指出精確欄位，不可用猜測的 default 繼續。此例只示範驗證方法，不新增規格要求。

**常見誤解。** 常見誤讀是：Figure 中出現 Firmware Activation Notices，便代表 capability 一定開啟或欄位值一定有效。layout 只定義適用時的位置與解法；support、state、command outcome 與 scope 仍要由各自 gate 和前後 requirement 判定。

#### Debug 對照表

| 症狀 | 先查什麼 |
|---|---|
| 數值不符 | 檢查 byte/bit range、endian、radix、0's-based 與 unit。 |
| 偶發錯誤 | 檢查 ownership、更新順序、snapshot 時機，以及物件是否由多個 actors 共享。 |
| parser 越界 | 走訪下一個 entry 前，用實際回傳 bytes 核對宣告 count/length。 |
| status 不預期 | 保留完整 category 與 context，不只印單一數字 code。 |

#### 讀完後應能回答

1. 能否展開 Firmware Activation Notices 的意思，並說出它的 unit 或 object scope？
2. 能否說明為什麼 引用條件 必須獨立檢查？
3. 能否指出哪一份 raw evidence 可區分 encoding bug 與 controller 真實狀態？

**來源欄位索引：** Firmware Activation Notices

**來源 keyword 索引：** `shall not`, `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.6, Figure 474, 文件頁 466-468, PDF 頁 492-494

</details>
