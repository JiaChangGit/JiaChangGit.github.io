---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4：Firmware Update 與 LID 03h 驗證"
date: 2026-09-01
description: "從 firmware download 到 LID 03h 驗證、可供 GitHub Pages 與 PPT 使用的工程教學。"
lang: zh-Hant-TW
img: posts/2026/dogMC_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---

# NVMe Base 2.4：Firmware Update 與 LID 03h 驗證

本教學建立完整工程模型：能力探測、image download、commit／activation、reset 邊界，以及用 Firmware Slot Information（LID 03h）驗證結果。

## 範圍與來源語意

範圍：§3.11、§3.11.1、§5.2.9、§5.2.10、§5.2.13 的 LID 03h 必要共通欄位、§5.2.13.1.4；主範圍文件頁 135-138、202-206、212-216、225-226，並含最小 dependency slice。

NVM Express Base Specification, Revision 2.4

NVM Express NVMe over PCIe Transport Specification, Revision 1.4 — 僅 §3.3 reset 名稱

排除：其餘 LID、未核准的傳輸專屬內容、NVM Command Set 1.3、Boot Partition 完整功能流程；BPID 與 CA=110b／111b 只保留 cross-reference。

`shall` 是強制要求，`should` 是有偏好的建議，`may` 表示允許選擇，`reserved` 不自行賦義。`[SPEC]` 是忠於來源的轉述；`[解釋]`、`[推論]`、`[說明性範例]` 不新增 requirement。

## Mental Model

```text
Downloaded portions -> committed slot -> current / next active image -> Identify.FR + LID 03h
```

## PART 1 — 先建立 Mental Model：image、slot、domain

**[解釋]** Firmware update 不是把檔案寫進裝置後立刻生效。Downloaded image、slot 內已保存的 image、目前執行中的 image，以及排定在下一次 reset 啟用的 image，是四個要分開追蹤的狀態。

### 先找出 firmware 的共享邊界

<!-- claim:BASEFWLOG-MODEL-DOMAIN -->

**[SPEC]** 同一 domain 內的 controllers 共用 firmware slots，且相同 firmware image 會套用到該 domain 的所有 controllers；若不支援 multiple domains，範圍就是整個 NVM subsystem。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 202, PDF 頁 228

### FR：目前 active revision

<!-- claim:BASEFWLOG-CAP-FR -->

**[SPEC]** Identify Controller 的 FR 是目前 active firmware revision 的 8-byte ASCII string，scope 是 controller 所屬 domain；它與 LID 03h 回報的目前 revision 資訊相同。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 340, PDF 頁 366

### MDS 與 ULIST

<!-- claim:BASEFWLOG-CAP-MDS-ULIST -->

**[SPEC]** CTRATT.MDS 判斷 LID 03h 回傳 domain scope 還是整個 NVM subsystem scope；CTRATT.ULIST 判斷 controller 是否支援 UUID List reporting。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 346, PDF 頁 372

### FRMW：slot 與 activation 能力

<!-- claim:BASEFWLOG-CAP-FRMW -->

**[SPEC]** FRMW 的 SMUD、FAWR、NOFS 與 FFSRO 分別表示重疊 update 偵測、免 reset activation、domain 支援的 slot 數（1 到 7）以及 slot 1 是否 read-only。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 354, PDF 頁 380

### MTFA：暫停 command processing 的時間

<!-- claim:BASEFWLOG-CAP-MTFA -->

**[SPEC]** MTFA 以 100 ms 為單位，表示 activation 時 controller 暫停處理 commands 的最長時間；支援免 reset activation 時此欄位必須（shall）有效，0h 表示最大時間未定義。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 357, PDF 頁 383

### FWUG：download granularity 與 alignment

<!-- claim:BASEFWLOG-CAP-FWUG -->

**[SPEC]** FWUG 以 4 KiB 為單位限制 NUMD 與 OFST 的 granularity／alignment：1h=4 KiB、2h=8 KiB、0h=未提供資訊、FFh=可用任何 dword granularity 與 alignment。違反時 controller 可（may）回 Invalid Field in Command。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 359, PDF 頁 385

### MPTFAWR：立即 activation 的完成時間

<!-- claim:BASEFWLOG-CAP-MPTFAWR -->

**[SPEC]** MPTFAWR 以 100 ms 為單位，估算 CA=011b 的 Firmware Commit 從處理到完成所需最大時間，且包含把 image commit 到 slot 的時間；不支援免 reset activation 時必須（shall）為 0h。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 364, PDF 頁 390

**[推論]** 工程上應把 domain 當作 firmware 狀態的共享鍵。只記錄 PCI Function 或 controller ID，可能把同一組 shared slots 誤判成多套獨立 firmware。

## PART 2 — 建立 Download Sequence：切片、對齊、失效條件

**[解釋]** Image 可以分段傳送，但 controller 看到的是 dword range，不是檔名或檔案 offset。每一段都要同時滿足 buffer、0's-based length、image-relative offset 與 FWUG。

### update sequence 應以串行方式規劃

<!-- claim:BASEFWLOG-FW-SEQUENCE -->

**[SPEC]** host 不宜（should not）讓 firmware／Boot Partition update sequences 重疊，且同一 sequence 宜（should）只使用一個 controller 或 Management Endpoint。SMUD 與 MUD 是偵測／回報能力，不是允許重疊的保證。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 文件頁 137, PDF 頁 163

### portion 順序、overlap 與 FWUG

<!-- claim:BASEFWLOG-DOWNLOAD-RANGE -->

**[SPEC]** Firmware Image Download 可分成多個 portions，firmware image portions 可不依序送達；host 宜（should）避免 ranges 重疊並符合 FWUG。Boot Partition portions 則必須（shall）依序提交。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, 文件頁 205-206, PDF 頁 231-232

### DPTR、NUMD、OFST 與實際 bytes

<!-- claim:BASEFWLOG-DOWNLOAD-FIELDS -->

**[SPEC]** DPTR 指向本次來源 buffer；NUMD 是 0's-based dword count，所以 bytes=(NUMD+1)×4；OFST 是距 image 起點的 dword offset，所以 byte offset=OFST×4。包含 image 起點的 portion 必須（shall）令 OFST=0h。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, 文件頁 205-206, PDF 頁 231-232

### downloaded portions 何時失效

<!-- claim:BASEFWLOG-FW-DISCARD -->

**[SPEC]** Firmware Commit 完成後的第一筆新 Firmware Image Download，以及 download 後、Firmware Commit 完成前發生的 Controller Level Reset，都必須（shall）使 controller 丟棄尚存的已下載 portions。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 5.2.10, 文件頁 137, 205-206, PDF 頁 163, 231-232

**[推論]** driver 應在送出 command 前用 byte interval 檢查 overlap，再轉成 NUMD／OFST；若先轉成 0's-based 欄位才檢查，最容易發生 off-by-one。

## PART 3 — Commit 與 Activation：CA 決定狀態轉移

**[解釋]** Firmware Commit 同時承擔驗證、slot placement 與 activation policy。最重要的判斷不是「command 成功了嗎」，而是成功後 image 位於哪個 slot、是否已 active、還欠哪一種 reset。

### Firmware Commit 的真正作用

<!-- claim:BASEFWLOG-COMMIT-PURPOSE -->

**[SPEC]** Firmware Commit 驗證最後下載的 image、把它放入 firmware slot，並依 Commit Action 決定只放置、在後續 Controller Level Reset activation，或立即 activation。成功 commit 不等於當下已 active。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 202-203, PDF 頁 228-229

### CA 與 FS 的決策矩陣

<!-- claim:BASEFWLOG-COMMIT-CDW10 -->

**[SPEC]** CDW10[5:3] 是 CA，CDW10[2:0] 是 FS。CA 000b 只放置；001b 放置並排定下次 CLR activation；010b 排定既有 slot；011b 立即 activation。FS=0h 時 controller 必須（shall）在 slot 1 到 7 中選一個。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 203, PDF 頁 229

### Boot Partition cross-reference 邊界

<!-- claim:BASEFWLOG-COMMIT-BOOT -->

**[SPEC]** BPID 與 CA=110b／111b 屬於 Boot Partition：110b 取代指定 partition，111b 將它標成 active；Boot Partition Write Prohibited 是 Firmware Commit 的 command-specific status 之一。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 203-205, PDF 頁 229-231

### MUD：重疊 sequence 的證據

<!-- claim:BASEFWLOG-COMMIT-MUD -->

**[SPEC]** Firmware Commit CQE.DW0[1:0] 的 MUD 分別回報 Management Endpoint 與 Admin Submission Queue 偵測到的 overlap。若 FRMW.SMUD=0，MUD 必須（shall）為 00b；MUD 在 command 成功或 aborted 時都有效。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 204, PDF 頁 230

### status 決定下一個 recovery 動作

<!-- claim:BASEFWLOG-COMMIT-STATUS -->

**[SPEC]** Firmware Commit 的 command-specific status 區分 invalid slot／image、需要 Conventional／NVM Subsystem／Controller Level Reset、MTFA violation、activation prohibited、overlapping range、Boot Partition write prohibited 與 personality incompatibility。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 204-205, PDF 頁 230-231

### 需要 reset 的完整流程

<!-- claim:BASEFWLOG-FW-RESET -->

**[SPEC]** 需要 reset 的標準流程是：一筆以上 Firmware Image Download、Firmware Commit 驗證並放入 slot、執行能觸發該 activation 的 Controller Level Reset，然後重新初始化 controller 與 I/O queues。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 文件頁 135-136, PDF 頁 161-162

### 立即 activation 不是背景工作

<!-- claim:BASEFWLOG-FW-IMMEDIATE -->

**[SPEC]** CA=011b 要求立即 activation。Firmware Commit 不是 background operation，會保持進行中直到 activation 成功或失敗；若 Firmware Activation notice 已啟用，受影響 controller 可（may）送出 Firmware Activation Starting event。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 文件頁 136, PDF 頁 162

### 載入失敗與 fallback

<!-- claim:BASEFWLOG-FW-FAILURE -->

**[SPEC]** 若新 image 無法成功載入，controller 必須（shall）回復到最近 activation 的 slot image；若該 image 也無法載入，則載入可用的 baseline read-only image，並產生 Firmware Image Load Error event。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 文件頁 136-137, PDF 頁 162-163

### PCIe reset 名稱不能混用

<!-- claim:BASEFWLOG-RESET-XREF -->

**[SPEC]** Conventional Reset 與 Function Level Reset 是 NVMe over PCIe Transport 定義的 PCIe-specific Controller Level Reset 方法。Base 的 Firmware Commit status 引用這些名稱時，應按 Transport §3.3 選擇 reset，不可把 FLR 與 Conventional Reset 視為同一件事。

> 來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.3, 文件頁 11, PDF 頁 11

### UUID List 的位置穩定性

<!-- claim:BASEFWLOG-UUID-LIST -->

**[SPEC]** firmware revisions 間的 UUID List 宜（should）保持 entry 位置穩定：新增 UUID 宜接在尾端；移除時宜原位改成 NVMe Invalid UUID；不宜重用 invalid entry，也不宜縮短或移除清單。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11.1, 文件頁 137-138, PDF 頁 163-164

### UUID 變更造成的 reset 邊界

<!-- claim:BASEFWLOG-UUID-RESET -->

**[SPEC]** 若 downloaded image 在既有 entry 中，以有效 UUID 取代 NVMe Invalid UUID 或另一個有效 UUID，controller 必須（shall）要求 reset；所有受這個 UUID List 變更影響的 controllers 都必須（shall）reset。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11.1, 文件頁 138, PDF 頁 164

### Figure 337／338 交叉引用差異

<!-- claim:BASEFWLOG-XREF-337 -->

**[SPEC]** 來源 §5.2.9 將 Firmware Revision 欄位指向 Figure 337；但 Figure 337 是 Command Set Identifiers，FR 實際列在 Figure 338。未取得另行核准的 errata，因此保留並揭露這個來源內部交叉引用差異，不靜默改寫。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 5.2.14.1, 文件頁 202, 340, PDF 頁 228, 366

**[推論]** recovery code 應以完整 SCT／SC 分流，而不是只判斷 success／failure。回報需要 Conventional Reset 時，用 FLR 取代並不能滿足該狀態所指示的 activation 邊界。

## PART 4 — 用 LID 03h 驗證：從 command 到 512-byte layout

**[解釋]** LID 03h 是 firmware workflow 的觀測面：AFI 回答 current／next active slot，FRS1-FRS7 回答各 slot 保存的 revision。它不替代 Firmware Commit completion，也不告訴 host 該用哪一種 reset。

### LID 03h 的最小 command slice

<!-- claim:BASEFWLOG-LOG-COMMAND -->

**[SPEC]** 讀 LID 03h 時只需要 DPTR 與 CDW10-CDW14 的必要 slice：LID=03h、LSP=0、RAE=0、NUMDL/NUMDU 表示 512 bytes、LSI=0、LPOL/LPOU=0、OT=0、UIDX=0；CSI 對 LID 03h 不使用，controller 依 Figure 208 規則忽略。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, 文件頁 212-215, PDF 頁 238-241

### 512 bytes 的實際 command 計算

<!-- claim:BASEFWLOG-LOG-LENGTH -->

**[SPEC]** NUMDL 與 NUMDU 合成 0's-based dword count。LID 03h 固定 512 bytes=128 dwords，因此 NUMD=127=0000007Fh，NUMDL=007Fh、NUMDU=0000h；在 LSP=0、RAE=0 下，CDW10=007F0003h。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, 文件頁 213-215, PDF 頁 239-241

### RAE 的事件副作用

<!-- claim:BASEFWLOG-LOG-RAE -->

**[SPEC]** RAE=0 會在 command 成功時清除對應 asynchronous event，RAE=1 則保留；若 command 未成功，controller 必須（shall）保留 event。Firmware Activation Starting event 要以 RAE=0 讀取 LID 03h 才會清除。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.2, 5.2.13, 文件頁 186, 213, PDF 頁 212, 239

### 完整讀取與 offset 邊界

<!-- claim:BASEFWLOG-LOG-OFFSET -->

**[SPEC]** 本報告以完整 512-byte LID 03h、LPOL=LPOU=0、OT=0 為基準。一般 byte offset 必須 dword aligned；超過 log page 大小的 offset 必須（shall）回 Invalid Field in Command。LID 03h 不需要 index-offset 分支。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, 文件頁 214-215, PDF 頁 240-241

### LID 03h 的 domain／subsystem scope

<!-- claim:BASEFWLOG-LOG-SCOPE -->

**[SPEC]** Figure 209 的 LID 03h row 指定 CSI=N、scope=Domain／NVM subsystem、reference=§5.2.13.1.4。MDS=1 時回傳處理 command 之 controller 所屬 domain；否則回傳整個 NVM subsystem 的資訊。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, 文件頁 215-216, PDF 頁 241-242

### LID 03h 回答的問題

<!-- claim:BASEFWLOG-LID03-DESCRIPTION -->

**[SPEC]** Firmware Slot Information log page 固定 512 bytes，說明每個支援 slot 內的 firmware revision，並指出 current active slot 與（若 controller 有回報）next active slot。revision 以 ASCII string 表示。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, 文件頁 225-226, PDF 頁 251-252

### AFI：current 與 next active slot

<!-- claim:BASEFWLOG-LID03-AFI -->

**[SPEC]** byte 0 的 AFI 中，NAFS=bits 6:4、CAFS=bits 2:0；bits 7 與 3 reserved。NAFS 非零表示將於下一次能觸發 activation 的 CLR 啟用該 slot，NAFS=0 表示 controller 未指出 next slot；CAFS 是目前執行 image 的來源 slot。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, 文件頁 226, PDF 頁 252

### FRS1-FRS7 與 reserved 區

<!-- claim:BASEFWLOG-LID03-FRS -->

**[SPEC]** FRS1 到 FRS7 位於 bytes 8-63，每格 8 bytes；slot 沒有有效 revision 或不支援時，該 FRS 必須（shall）清為 0h。bytes 1-7 與 64-511 reserved，parser 不應把 reserved bytes 當成額外 slots。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, 文件頁 226, PDF 頁 252

**[推論]** 驗證時要同時比對 Identify.FR、LID 03h 的 CAFS 與對應 FRSx。只比 ASCII revision 可能在兩個 slots 恰好含相同字串時失去 slot 身分。

## End-to-End Example：12 KiB image，slot 2，下次 CLR 啟用

**[說明性範例]** 假設 NOFS=3、FFSRO=1、FWUG=1h、CAFS=1，選可寫的 slot 2。12 KiB 切成三個 4 KiB portions；每段 1024 dwords，所以 NUMD=1023=000003FFh，OFST 依序是 00000000h、00000400h、00000800h。以 CA=001b、FS=010b commit，CDW10=0000000Ah。Reset 前完整讀 512-byte LID 03h：NUMD=127、CDW10=007F0003h；AFI=21h 解成 NAFS=2、CAFS=1。執行要求的 reset、重新初始化，再一起驗證 CAFS=2、FRS2 與 Identify.FR。

## Debug Decision Flow

| 症狀 | 第一證據 | 常見錯誤 | 下一步 |
|---|---|---|---|
| Download Invalid Field | NUMD、OFST、FWUG | 把 NUMD 當直接 count | 重算 byte intervals |
| Invalid Firmware Slot | NOFS、FFSRO、FS | 假設 slot 1 可寫 | 改用支援且可寫 slot |
| reset-required status | 完整 SCT／SC | 把所有 reset 視為相同 | 依 status 與 PCIe §3.3 |
| LID 03h 未更新 | MDS／DID、controller、AFI | 假設 slots 各 controller 獨立 | 在同一 domain 核對 |
| FRSx 為零 | NOFS、slot validity、buffer offset | 當成空字串 revision | 視為 unsupported／no valid revision |

## Appendix A — Supporting Figure / Field Reference

Figure 是主流程的可追溯證據，不是文章骨架。dependency entries 只取理解所需切片；Figure 209 只保留 LID 03h row。

<details markdown="1">
<summary><strong>Figure 187: Firmware Commit – Command Dword 10</strong> — 主範圍證據</summary>

<!-- claim:BASEFWLOG-FIG-187-CLAIM figure-table:BASEFWLOG-FIG-187 -->

**[SPEC]** Figure 187〈Firmware Commit – Command Dword 10〉：定義〈Firmware Commit – Command Dword 10〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：BPID, CA, FS。

**[解釋]** 定義〈Firmware Commit – Command Dword 10〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：BPID, CA, FS。

來源欄位索引：BPID, CA, FS

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, Figure 187, 文件頁 203, PDF 頁 229

</details>

<details markdown="1">
<summary><strong>Figure 188: Firmware Commit – Completion Queue Entry Dword 0</strong> — 主範圍證據</summary>

<!-- claim:BASEFWLOG-FIG-188-CLAIM figure-table:BASEFWLOG-FIG-188 -->

**[SPEC]** Figure 188〈Firmware Commit – Completion Queue Entry Dword 0〉：呈現〈Firmware Commit – Completion Queue Entry Dword 0〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：MUD, MEFWO, ASQFWO。

**[解釋]** 呈現〈Firmware Commit – Completion Queue Entry Dword 0〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：MUD, MEFWO, ASQFWO。

來源欄位索引：MUD, MEFWO, ASQFWO

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 188, 文件頁 204, PDF 頁 230

</details>

<details markdown="1">
<summary><strong>Figure 189: Firmware Commit – Command Specific Status Values</strong> — 主範圍證據</summary>

<!-- claim:BASEFWLOG-FIG-189-CLAIM figure-table:BASEFWLOG-FIG-189 -->

**[SPEC]** Figure 189〈Firmware Commit – Command Specific Status Values〉：定義〈Firmware Commit – Command Specific Status Values〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Invalid Firmware Slot, Invalid Firmware Image, reset-required status, MTFA, Overlapping Range。

**[解釋]** 定義〈Firmware Commit – Command Specific Status Values〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Invalid Firmware Slot, Invalid Firmware Image, reset-required status, MTFA, Overlapping Range。

來源欄位索引：Invalid Firmware Slot, Invalid Firmware Image, reset-required status, MTFA, Overlapping Range

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 189, 文件頁 204-205, PDF 頁 230-231

</details>

<details markdown="1">
<summary><strong>Figure 190: Firmware Image Download – Data Pointer</strong> — 主範圍證據</summary>

<!-- claim:BASEFWLOG-FIG-190-CLAIM figure-table:BASEFWLOG-FIG-190 -->

**[SPEC]** Figure 190〈Firmware Image Download – Data Pointer〉：定義〈Firmware Image Download – Data Pointer〉如何指出本命令的來源或目的 buffer。 先判斷 pointer type 與 address，再核對 transfer length 和 alignment；來源欄位索引：DPTR。

**[解釋]** 定義〈Firmware Image Download – Data Pointer〉如何指出本命令的來源或目的 buffer。 先判斷 pointer type 與 address，再核對 transfer length 和 alignment；來源欄位索引：DPTR。

來源欄位索引：DPTR

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 190, 文件頁 205, PDF 頁 231

</details>

<details markdown="1">
<summary><strong>Figure 191: Firmware Image Download – Command Dword 10</strong> — 主範圍證據</summary>

<!-- claim:BASEFWLOG-FIG-191-CLAIM figure-table:BASEFWLOG-FIG-191 -->

**[SPEC]** Figure 191〈Firmware Image Download – Command Dword 10〉：定義〈Firmware Image Download – Command Dword 10〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NUMD, FWUG。

**[解釋]** 定義〈Firmware Image Download – Command Dword 10〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NUMD, FWUG。

來源欄位索引：NUMD, FWUG

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 191, 文件頁 205, PDF 頁 231

</details>

<details markdown="1">
<summary><strong>Figure 192: Firmware Image Download – Command Dword 11</strong> — 主範圍證據</summary>

<!-- claim:BASEFWLOG-FIG-192-CLAIM figure-table:BASEFWLOG-FIG-192 -->

**[SPEC]** Figure 192〈Firmware Image Download – Command Dword 11〉：定義〈Firmware Image Download – Command Dword 11〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：OFST, FWUG。

**[解釋]** 定義〈Firmware Image Download – Command Dword 11〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：OFST, FWUG。

來源欄位索引：OFST, FWUG

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 192, 文件頁 206, PDF 頁 232

</details>

<details markdown="1">
<summary><strong>Figure 193: Firmware Image Download – Command Specific Status Values</strong> — 主範圍證據</summary>

<!-- claim:BASEFWLOG-FIG-193-CLAIM figure-table:BASEFWLOG-FIG-193 -->

**[SPEC]** Figure 193〈Firmware Image Download – Command Specific Status Values〉：定義〈Firmware Image Download – Command Specific Status Values〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Overlapping Range。

**[解釋]** 定義〈Firmware Image Download – Command Specific Status Values〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Overlapping Range。

來源欄位索引：Overlapping Range

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 193, 文件頁 206, PDF 頁 232

</details>

<details markdown="1">
<summary><strong>Figure 203: Get Log Page – Data Pointer</strong> — 主範圍證據</summary>

<!-- claim:BASEFWLOG-FIG-203-CLAIM figure-table:BASEFWLOG-FIG-203 -->

**[SPEC]** Figure 203〈Get Log Page – Data Pointer〉：定義〈Get Log Page – Data Pointer〉如何指出本命令的來源或目的 buffer。 先判斷 pointer type 與 address，再核對 transfer length 和 alignment；來源欄位索引：DPTR。

**[解釋]** 定義〈Get Log Page – Data Pointer〉如何指出本命令的來源或目的 buffer。 先判斷 pointer type 與 address，再核對 transfer length 和 alignment；來源欄位索引：DPTR。

來源欄位索引：DPTR

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 203, 文件頁 213, PDF 頁 239

</details>

<details markdown="1">
<summary><strong>Figure 204: Get Log Page – Command Dword 10</strong> — 主範圍證據</summary>

<!-- claim:BASEFWLOG-FIG-204-CLAIM figure-table:BASEFWLOG-FIG-204 -->

**[SPEC]** Figure 204〈Get Log Page – Command Dword 10〉：定義〈Get Log Page – Command Dword 10〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：NUMDL, RAE, LSP, LID。

**[解釋]** 定義〈Get Log Page – Command Dword 10〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：NUMDL, RAE, LSP, LID。

來源欄位索引：NUMDL, RAE, LSP, LID

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 204, 文件頁 213, PDF 頁 239

</details>

<details markdown="1">
<summary><strong>Figure 205: Get Log Page – Command Dword 11</strong> — 主範圍證據</summary>

<!-- claim:BASEFWLOG-FIG-205-CLAIM figure-table:BASEFWLOG-FIG-205 -->

**[SPEC]** Figure 205〈Get Log Page – Command Dword 11〉：定義〈Get Log Page – Command Dword 11〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LSI, NUMDU。

**[解釋]** 定義〈Get Log Page – Command Dword 11〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LSI, NUMDU。

來源欄位索引：LSI, NUMDU

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 205, 文件頁 214, PDF 頁 240

</details>

<details markdown="1">
<summary><strong>Figure 206: Get Log Page – Command Dword 12</strong> — 主範圍證據</summary>

<!-- claim:BASEFWLOG-FIG-206-CLAIM figure-table:BASEFWLOG-FIG-206 -->

**[SPEC]** Figure 206〈Get Log Page – Command Dword 12〉：定義〈Get Log Page – Command Dword 12〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LPOL, OT。

**[解釋]** 定義〈Get Log Page – Command Dword 12〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LPOL, OT。

來源欄位索引：LPOL, OT

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 206, 文件頁 214, PDF 頁 240

</details>

<details markdown="1">
<summary><strong>Figure 207: Get Log Page – Command Dword 13</strong> — 主範圍證據</summary>

<!-- claim:BASEFWLOG-FIG-207-CLAIM figure-table:BASEFWLOG-FIG-207 -->

**[SPEC]** Figure 207〈Get Log Page – Command Dword 13〉：定義〈Get Log Page – Command Dword 13〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LPOU。

**[解釋]** 定義〈Get Log Page – Command Dword 13〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LPOU。

來源欄位索引：LPOU

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 207, 文件頁 214, PDF 頁 240

</details>

<details markdown="1">
<summary><strong>Figure 208: Get Log Page – Command Dword 14</strong> — 主範圍證據</summary>

<!-- claim:BASEFWLOG-FIG-208-CLAIM figure-table:BASEFWLOG-FIG-208 -->

**[SPEC]** Figure 208〈Get Log Page – Command Dword 14〉：定義〈Get Log Page – Command Dword 14〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CSI, OT, UIDX。

**[解釋]** 定義〈Get Log Page – Command Dword 14〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CSI, OT, UIDX。

來源欄位索引：CSI, OT, UIDX

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 208, 文件頁 214-215, PDF 頁 240-241

</details>

<details markdown="1">
<summary><strong>Figure 209: Get Log Page – Log Page Identifiers</strong> — 主範圍證據</summary>

<!-- claim:BASEFWLOG-FIG-209-CLAIM figure-table:BASEFWLOG-FIG-209 -->

**[SPEC]** Figure 209〈Get Log Page – Log Page Identifiers〉：定義〈Get Log Page – Log Page Identifiers〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LID 03h, CSI = N, Domain / NVM subsystem, Firmware Slot Information, §5.2.13.1.4, MDS。

**[解釋]** 定義〈Get Log Page – Log Page Identifiers〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LID 03h, CSI = N, Domain / NVM subsystem, Firmware Slot Information, §5.2.13.1.4, MDS。

來源欄位索引：LID 03h, CSI = N, Domain / NVM subsystem, Firmware Slot Information, §5.2.13.1.4, MDS

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 209, 文件頁 215-216, PDF 頁 241-242

</details>

<details markdown="1">
<summary><strong>Figure 215: Firmware Slot Information Log Page</strong> — 主範圍證據</summary>

<!-- claim:BASEFWLOG-FIG-215-CLAIM figure-table:BASEFWLOG-FIG-215 -->

**[SPEC]** Figure 215〈Firmware Slot Information Log Page〉：定義〈Firmware Slot Information Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：AFI, NAFS, CAFS, FRS1, FRS2, FRS3, FRS4, FRS5, FRS6, FRS7, Reserved bytes 1:7 and 64:511。

**[解釋]** 定義〈Firmware Slot Information Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：AFI, NAFS, CAFS, FRS1, FRS2, FRS3, FRS4, FRS5, FRS6, FRS7, Reserved bytes 1:7 and 64:511。

來源欄位索引：AFI, NAFS, CAFS, FRS1, FRS2, FRS3, FRS4, FRS5, FRS6, FRS7, Reserved bytes 1:7 and 64:511

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, Figure 215, 文件頁 226, PDF 頁 252

</details>

<details markdown="1">
<summary><strong>Figure 93: Common Command Format</strong> — 最小相依切片</summary>

<!-- claim:BASEFWLOG-FIG-093-CLAIM figure-table:BASEFWLOG-FIG-093 -->

**[SPEC]** Figure 93〈Common Command Format〉：定義〈Common Command Format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DPTR, PRP1, PRP2, SGL1。

**[解釋]** 定義〈Common Command Format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DPTR, PRP1, PRP2, SGL1。

來源欄位索引：DPTR, PRP1, PRP2, SGL1

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, 文件頁 140-142, PDF 頁 166-168

</details>

<details markdown="1">
<summary><strong>Figure 155: Asynchronous Event Information – Notice</strong> — 最小相依切片</summary>

<!-- claim:BASEFWLOG-FIG-155-CLAIM figure-table:BASEFWLOG-FIG-155 -->

**[SPEC]** Figure 155〈Asynchronous Event Information – Notice〉：定義〈Asynchronous Event Information – Notice〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：Firmware Activation Starting, CSTS.PP, Firmware Slot Information, RAE。

**[解釋]** 定義〈Asynchronous Event Information – Notice〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：Firmware Activation Starting, CSTS.PP, Firmware Slot Information, RAE。

來源欄位索引：Firmware Activation Starting, CSTS.PP, Firmware Slot Information, RAE

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 155, 文件頁 186, PDF 頁 212

</details>

<details markdown="1">
<summary><strong>Figure 337: Command Set Identifiers</strong> — 最小相依切片</summary>

<!-- claim:BASEFWLOG-FIG-337-CLAIM figure-table:BASEFWLOG-FIG-337 -->

**[SPEC]** Figure 337〈Command Set Identifiers〉：定義〈Command Set Identifiers〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：Command Set Identifier。

**[解釋]** 定義〈Command Set Identifiers〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：Command Set Identifier。

來源欄位索引：Command Set Identifier

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, Figure 337, 文件頁 340, PDF 頁 366

</details>

<details markdown="1">
<summary><strong>Figure 338: Identify – Identify Controller Data Structure, I/O Command Set Independent</strong> — 最小相依切片</summary>

<!-- claim:BASEFWLOG-FIG-338-CLAIM figure-table:BASEFWLOG-FIG-338 -->

**[SPEC]** Figure 338〈Identify – Identify Controller Data Structure, I/O Command Set Independent〉：定義〈Identify – Identify Controller Data Structure, I/O Command Set Independent〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：FR, MDS, ULIST, SMUD, FAWR, NOFS, FFSRO, MTFA, FWUG, DID, MPTFAWR。

**[解釋]** 定義〈Identify – Identify Controller Data Structure, I/O Command Set Independent〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：FR, MDS, ULIST, SMUD, FAWR, NOFS, FFSRO, MTFA, FWUG, DID, MPTFAWR。

來源欄位索引：FR, MDS, ULIST, SMUD, FAWR, NOFS, FFSRO, MTFA, FWUG, DID, MPTFAWR

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, 文件頁 340-364, PDF 頁 366-390

</details>

<details markdown="1">
<summary><strong>Figure 347: UUID List</strong> — 最小相依切片</summary>

<!-- claim:BASEFWLOG-FIG-347-CLAIM figure-table:BASEFWLOG-FIG-347 -->

**[SPEC]** Figure 347〈UUID List〉：定義〈UUID List〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：UUID1, UUID2, UUID126, UUID127, NVMe Invalid UUID。

**[解釋]** 定義〈UUID List〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：UUID1, UUID2, UUID126, UUID127, NVMe Invalid UUID。

來源欄位索引：UUID1, UUID2, UUID126, UUID127, NVMe Invalid UUID

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.14, Figure 347, 文件頁 396, PDF 頁 422

</details>

<details markdown="1">
<summary><strong>Figure 348: UUID List Entry</strong> — 最小相依切片</summary>

<!-- claim:BASEFWLOG-FIG-348-CLAIM figure-table:BASEFWLOG-FIG-348 -->

**[SPEC]** Figure 348〈UUID List Entry〉：定義〈UUID List Entry〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：ULEH, IDASSOC, UUID。

**[解釋]** 定義〈UUID List Entry〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：ULEH, IDASSOC, UUID。

來源欄位索引：ULEH, IDASSOC, UUID

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.14, Figure 348, 文件頁 396, PDF 頁 422

</details>

<details markdown="1">
<summary><strong>Figure 474: Asynchronous Event Configuration – Command Dword 11</strong> — 最小相依切片</summary>

<!-- claim:BASEFWLOG-FIG-474-CLAIM figure-table:BASEFWLOG-FIG-474 -->

**[SPEC]** Figure 474〈Asynchronous Event Configuration – Command Dword 11〉：定義〈Asynchronous Event Configuration – Command Dword 11〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：Firmware Activation Notices。

**[解釋]** 定義〈Asynchronous Event Configuration – Command Dword 11〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：Firmware Activation Notices。

來源欄位索引：Firmware Activation Notices

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.6, Figure 474, 文件頁 466-468, PDF 頁 492-494

</details>

## 限制

查證日期：2026-09-01。未納入其他 Errata、ECN、Technical Proposal、controller vendor 文件或 PCI Express Base Specification 原文。核准來源集合改變時，應依 claim ID 重查。
