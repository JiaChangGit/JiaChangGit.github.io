---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4：Firmware Update、Firmware Admin Commands 與 Get Log Page"
date: 2026-08-31
description: "供 GitHub Pages 與 PPT 使用的 NVMe 規格導讀。"
lang: zh-Hant-TW
img: posts/2026/dogMC_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
---

# NVMe Base 2.4：Firmware Update、Firmware Admin Commands 與 Get Log Page

用途：供 GitHub Pages 閱讀與 100 分鐘簡報製作；讀者已具備 PCIe 與 NVMe 基礎。

範圍：§3.11、§5.2.9、§5.2.10、§5.2.13.1-§5.2.13.2、§5.2.13.4；主範圍文件頁 135-138、202-206、212-319、336；另納入正文直接引用的相依 Figure。正文只保留 PCIe／memory-based 與通用 NVMe 內容。

## 來源版本

NVM Express Base Specification, Revision 2.4

查證日期：2026-08-31。目前未納入其他 Errata、ECN、Technical Proposal、controller vendor 文件或未提供的 PCI Express Base Specification 原文。

## 閱讀地圖

```text
Image Download -> Firmware Commit -> Activate / Reset -> Get Log Page
```

host 以 OFST／NUMD 分段下載 image，Firmware Commit 驗證並選擇 slot／activation action；完成 reset 或立即 activation 後，再以 log page 與 asynchronous event 狀態核對結果。

## 規範性用語

shall 譯為「必須」，may 譯為「可／得」，should 譯為「宜／建議」，optional 譯為「選用」。本文不提高或降低原文語氣。

## 規格重點

### 1. 需要 reset 的 firmware update

<!-- claim:BASEFWLOG-FW-RESET -->

需要 reset 的 firmware update 依序為：以一筆以上 Firmware Image Download command 傳送 image、以 Firmware Commit 驗證並放入 firmware slot、執行能觸發指定 activation 的 Controller Level Reset，最後重新初始化 controller 與 I/O queues。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 文件頁 135-136, PDF 頁 161-162

### 2. 立即 activation

<!-- claim:BASEFWLOG-FW-IMMEDIATE -->

Commit Action 011b 表示立即 activation。若 activation 開始，受影響 controller 可在 notice 已啟用時送出 Firmware Activation Starting event；Firmware Commit 在 activation 成功或失敗前保持進行中，不是 background operation。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 文件頁 136-137, PDF 頁 162-163

### 3. activation 失敗與 fallback

<!-- claim:BASEFWLOG-FW-FAILURE -->

立即 activation 若需要其他 reset 或超過 MTFA，controller 以對應 command-specific status 結束；若 image 無法成功載入，controller 必須（shall）回復到最近啟用 slot 的 image 或可用的 baseline read-only image，並以 Firmware Image Load Error event 回報。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 文件頁 136-137, PDF 頁 162-163

### 4. update sequence 串行化

<!-- claim:BASEFWLOG-FW-SEQUENCE -->

host 不宜（should not）重疊 firmware／boot-partition update sequence，且同一 sequence 宜使用同一 controller 或 Management Endpoint。Firmware Commit 完成後的第一筆新 download，以及 commit 完成前發生的 reset，都必須（shall）使 controller 丟棄尚存的已下載部分。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 文件頁 137, PDF 頁 163

### 5. UUID list 跨版本穩定性

<!-- claim:BASEFWLOG-UUID-LIST -->

firmware revision 間的 UUID list 宜維持 slot 穩定：新增項目放在尾端，移除項目以 NVMe Invalid UUID 留在原 slot，既有 invalid slot 不再填入有效 UUID，且不縮短清單。若下載 image 以有效 UUID 取代 invalid UUID 或另一個有效 UUID，controller 必須（shall）要求 reset，所有受影響 controller 都必須一起 reset。

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.11.1, 文件頁 137-138, PDF 頁 163-164

### 6. Firmware Commit 的作用

<!-- claim:BASEFWLOG-COMMIT-PURPOSE -->

Firmware Commit 驗證最後下載的 image，將它放入指定 firmware slot，並依 Commit Action 決定只放置、在後續 reset activation，或立即 activation。domain 內的 controller 共用 firmware slots 與相同 firmware image。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 202-203, PDF 頁 228-229

### 7. Commit Action、slot 與 BPID

<!-- claim:BASEFWLOG-COMMIT-CDW10 -->

CDW10 以 BPID、Commit Action（CA）與 Firmware Slot（FS）描述操作。CA 000b-011b 用於 firmware image；110b-111b 用於 Boot Partition。FS=0h 時，controller 必須（shall）在 slot 1-7 中選擇可用 slot。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 203, PDF 頁 229

### 8. Multiple Update Detected

<!-- claim:BASEFWLOG-COMMIT-MUD -->

Firmware Commit CQE.DW0 的 Multiple Update Detected（MUD）可指出 Management Endpoint 或 Admin Submission Queue 偵測到重疊 update sequence；若 Identify Controller 的 SMUD=0，MUD 必須（shall）為 00b。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, 文件頁 203-204, PDF 頁 229-230

### 9. Firmware Commit status

<!-- claim:BASEFWLOG-COMMIT-STATUS -->

Firmware Commit status 需分開判斷 image／slot 無效、需要 Conventional／NVM Subsystem／Controller Level Reset、超過 MTFA、activation 被禁止、range 重疊與 Boot Partition write lock；成功 commit 不代表 image 已在當下 activation。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, 文件頁 204-205, PDF 頁 230-231

### 10. download range 與順序

<!-- claim:BASEFWLOG-DOWNLOAD-RANGE -->

Firmware Image Download 以 NUMD 與 OFST 定義 0's-based dword range；image 可分段且一般可不依序送出，但 Boot Partition update 必須（shall）依序。host 宜（should）避免 range 重疊，並符合 FWUG 的 alignment 與 granularity。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, 文件頁 205-206, PDF 頁 231-232

### 11. DPTR、NUMD 與 OFST

<!-- claim:BASEFWLOG-DOWNLOAD-FIELDS -->

DPTR 指向本次 portion，CDW10.NUMD 指定 dword 數量減一，CDW11.OFST 指定距 image 起點的 dword offset；包含 image 起點的 portion 必須（shall）使用 OFST=0h。Firmware Image Download 本身不 activation image。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, 文件頁 205-206, PDF 頁 231-232

### 12. Get Log Page command 欄位

<!-- claim:BASEFWLOG-LOG-COMMAND -->

Get Log Page 使用 DPTR 與 CDW10-CDW14。核心 selector／length 欄位為 LID、LSP、RAE、NUMDL／NUMDU、LSI、LPOL／LPOU、CSI、OT 與 UIDX；未由指定 log page 定義的 command-specific 欄位維持 reserved 或依 Figure 208 的規則忽略。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, 文件頁 212-215, PDF 頁 238-241

### 13. transfer length 與 offset

<!-- claim:BASEFWLOG-LOG-LENGTH -->

NUMDL 與 NUMDU 組成 0's-based transfer length。支援 log page offset 時，byte offset 必須（shall）對所有 log page 可用；只有 Supported Log Pages 對該 LID 回報 IOS=1 時才能使用 index offset（OT=1）。超出 log page 或 entry 數量的 offset 必須以 Invalid Field in Command 結束。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, 文件頁 213-215, PDF 頁 239-241

### 14. RAE 與 asynchronous event

<!-- claim:BASEFWLOG-LOG-RAE -->

RAE=0 時，成功完成 Get Log Page 會清除對應 asynchronous event；RAE=1 則保留。若 command 未成功完成，controller 必須（shall）保留 event。與 asynchronous event 無關的 log page，host 通常宜（should）把 RAE 清為 0。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, 文件頁 213, PDF 頁 239

### 15. LID 與資料 scope

<!-- claim:BASEFWLOG-LOG-SCOPE -->

Figure 209 同時定義 LID、CSI 使用方式、資料 scope 與 reference section。NVM subsystem、domain、controller、namespace 的 scope 不可互換；對 subsystem 或 controller scope 的 log page，NSID 除 0h／FFFFFFFFh 外必須（shall）以 Invalid Field in Command 結束。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1, 文件頁 215-217, PDF 頁 241-243

### 16. Supported Log Pages

<!-- claim:BASEFWLOG-LOG-SUPPORT -->

Supported Log Pages（LID 00h）按 command submission interface 回報每個 LID 的支援與效果。LID Supported and Effects data structure 的 SUPP、IOS 與其他 attribute 必須先配合 controller type、I/O Command Set 與 UUID selection 狀態解讀。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.1, 文件頁 217-218, PDF 頁 243-244

### 17. operational log pages

<!-- claim:BASEFWLOG-LOG-OPERATIONS -->

operational log pages 分別處理 Error Information、SMART／Health、Firmware Slot、namespace change、command effects、device self-test、telemetry、Endurance Group、predictable latency 與 ANA。parser 必須先依 Figure 209 決定 scope，再依各 log page header 的 entry count／generation number／data area 邊界解析。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.2-5.2.13.1.13, 文件頁 218-244, PDF 頁 244-270

### 18. Persistent Event Log

<!-- claim:BASEFWLOG-PERSISTENT-EVENT -->

Persistent Event Log 由 log header、event header 與 event-specific data 組成，LSP 控制 establish／read／release context。event length、header length、generation number 與 context identifier 都要先驗證，再依 Event Type 解碼；本報告只保留通用與 PCIe 可用 event。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14, 文件頁 244-266, 268-270, PDF 頁 270-292, 294-296

### 19. capacity、management 與 FDP logs

<!-- claim:BASEFWLOG-LOG-CAPACITY-FDP -->

後段 common log pages 涵蓋 Endurance Group event、Media Unit、capacity configuration、Feature／NVMe-MI effects、lockdown、Boot Partition、management／reachability、device personality 與 FDP。這些資料結構使用不同的 identifier、descriptor count 與 variable-length array，不能共用固定 parser。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.15-5.2.13.1.33, 文件頁 270-301, PDF 頁 296-327

### 20. power、voltage 與 sanitize logs

<!-- claim:BASEFWLOG-LOG-POWER-SANITIZE -->

Power Measurement、Voltage Measurement、Sanitize Namespace Status List、Reservation Notification 與 Sanitize Status 各自定義量測 scale、sensor／target selector、generation 或 state 欄位。量測值必須先套用對應 scale；sanitize 狀態必須配合 target 與 state machine 解讀。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.34-5.2.13.1.38, 文件頁 302-319, PDF 頁 328-345

### 21. PCIe 的 log page 適用方式

<!-- claim:BASEFWLOG-PCIE-LOGS -->

§5.2.13.2 明確指出 memory-based transport model 沒有專屬 log page；PCIe controller 使用 §5.2.13.1 的 common log pages 與各自 capability／scope 規則。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.2, 文件頁 319, PDF 頁 345

### 22. Get Log Page completion

<!-- claim:BASEFWLOG-LOG-COMPLETION -->

Get Log Page 完成後在 Admin Completion Queue 回報結果；command-specific status 區分 Invalid Log Page、Invalid Controller Identifier 與 I/O Command Set Not Supported。保留或未支援 LID 以 Invalid Log Page 回報。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.4, 文件頁 336, PDF 頁 362

### 23. Figure 337／338 交叉引用差異

<!-- claim:BASEFWLOG-XREF-337 -->

來源 §5.2.9 把 Firmware Revision 欄位指向 Figure 337；但 Figure 337 的標題與內容是 Command Set Identifiers，Firmware Revision（FR）實際列於 Figure 338。因本輪沒有額外 Errata，本報告保留此內部交叉引用差異並同時教學兩張 Figure，不自行改寫規格。

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 5.2.14.1-5.2.14.2.1, 文件頁 202, 340, PDF 頁 228, 366

## Figure 索引

本報告介紹全部 146 張納入範圍的 Figure。100 分鐘簡報以 section 主線與必講 Figure 為主，其餘 Figure 仍完整保留作為附錄。其中 29 張位於主章節範圍外，但因指定正文直接引用而納入相依教學。

- [§5.2](#section-5-2)

- [引用相依 Figure（位於主章節範圍外）](#section-dependency)

## Figure 逐圖導讀

指定正文沒有引用任何編號 Table。本範圍的規格以 Figure 編號同時涵蓋示意圖與欄位表；本文不重製原圖。欄位與 keyword 索引來自本機核對過的 PDF。

<a id="section-5-2"></a>

### §5.2

<details markdown="1">
<summary><strong>Figure 187: Firmware Commit – Command Dword 10</strong></summary>

<!-- claim:BASEFWLOG-FIG-187-CLAIM figure-table:BASEFWLOG-FIG-187 -->

Figure 187〈Firmware Commit – Command Dword 10〉：定義〈Firmware Commit – Command Dword 10〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：BPID, CA, FS, ID, BPINFO.ABPID, Command。

- 解決的問題：定義〈Firmware Commit – Command Dword 10〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：BPID, CA, FS, ID, BPINFO.ABPID, Command。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 BPID 作為 parser 的第一個檢查點，再用 CA 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：BPID, CA, FS, ID, BPINFO.ABPID, Command

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, Figure 187, 文件頁 203, PDF 頁 229

</details>

<details markdown="1">
<summary><strong>Figure 188: Firmware Commit – Completion Queue Entry Dword 0</strong></summary>

<!-- claim:BASEFWLOG-FIG-188-CLAIM figure-table:BASEFWLOG-FIG-188 -->

Figure 188〈Firmware Commit – Completion Queue Entry Dword 0〉：呈現〈Firmware Commit – Completion Queue Entry Dword 0〉中的 queue 或 command 關係。 沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：MUD, Completion Queue。

- 解決的問題：呈現〈Firmware Commit – Completion Queue Entry Dword 0〉中的 queue 或 command 關係。

- 閱讀順序：沿 host、SQ、controller、CQ 的擁有者與方向閱讀，並分開追蹤：MUD, Completion Queue。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：沿 Figure 188 追蹤一筆 command，以 MUD 與 Completion Queue 作為擁有者或 pointer 變動檢查點。 此例不新增規格要求。

- 來源欄位索引：MUD, Completion Queue

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 188, 文件頁 204, PDF 頁 230

</details>

<details markdown="1">
<summary><strong>Figure 189: Firmware Commit – Command Specific Status Values</strong></summary>

<!-- claim:BASEFWLOG-FIG-189-CLAIM figure-table:BASEFWLOG-FIG-189 -->

Figure 189〈Firmware Commit – Command Specific Status Values〉：定義〈Firmware Commit – Command Specific Status Values〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MTFA, Command。

- 解決的問題：定義〈Firmware Commit – Command Specific Status Values〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MTFA, Command。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 MTFA 作為 parser 的第一個檢查點，再用 Command 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：MTFA, Command

- 來源 keyword 索引：`shall`, `should`, `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 189, 文件頁 204-205, PDF 頁 230-231

</details>

<details markdown="1">
<summary><strong>Figure 190: Firmware Image Download – Data Pointer</strong></summary>

<!-- claim:BASEFWLOG-FIG-190-CLAIM figure-table:BASEFWLOG-FIG-190 -->

Figure 190〈Firmware Image Download – Data Pointer〉：定義〈Firmware Image Download – Data Pointer〉如何指出本命令的來源或目的 buffer。 先判斷 pointer type 與 address，再核對 transfer length 和 alignment；來源欄位索引：DPTR。

- 解決的問題：定義〈Firmware Image Download – Data Pointer〉如何指出本命令的來源或目的 buffer。

- 閱讀順序：先判斷 pointer type 與 address，再核對 transfer length 和 alignment；來源欄位索引：DPTR。

- 條件與限制：來源 keyword 索引：`should`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先驗證 DPTR 所代表的 pointer 形式，再核對 引用條件 對應的邊界，通過後才開始 transfer。 此例不新增規格要求。

- 來源欄位索引：DPTR

- 來源 keyword 索引：`should`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 190, 文件頁 205, PDF 頁 231

</details>

<details markdown="1">
<summary><strong>Figure 191: Firmware Image Download – Command Dword 10</strong></summary>

<!-- claim:BASEFWLOG-FIG-191-CLAIM figure-table:BASEFWLOG-FIG-191 -->

Figure 191〈Firmware Image Download – Command Dword 10〉：定義〈Firmware Image Download – Command Dword 10〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NUMD, FWUG, Command。

- 解決的問題：定義〈Firmware Image Download – Command Dword 10〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NUMD, FWUG, Command。

- 條件與限制：來源 keyword 索引：`may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 NUMD 作為 parser 的第一個檢查點，再用 FWUG 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：NUMD, FWUG, Command

- 來源 keyword 索引：`may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 191, 文件頁 205, PDF 頁 231

</details>

<details markdown="1">
<summary><strong>Figure 192: Firmware Image Download – Command Dword 11</strong></summary>

<!-- claim:BASEFWLOG-FIG-192-CLAIM figure-table:BASEFWLOG-FIG-192 -->

Figure 192〈Firmware Image Download – Command Dword 11〉：定義〈Firmware Image Download – Command Dword 11〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：OFST, FWUG。

- 解決的問題：定義〈Firmware Image Download – Command Dword 11〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：OFST, FWUG。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：以 OFST 作為 parser 的第一個檢查點，再用 FWUG 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：OFST, FWUG

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 192, 文件頁 206, PDF 頁 232

</details>

<details markdown="1">
<summary><strong>Figure 193: Firmware Image Download – Command Specific Status Values</strong></summary>

<!-- claim:BASEFWLOG-FIG-193-CLAIM figure-table:BASEFWLOG-FIG-193 -->

Figure 193〈Firmware Image Download – Command Specific Status Values〉：定義〈Firmware Image Download – Command Specific Status Values〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Overlapping Range。

- 解決的問題：定義〈Firmware Image Download – Command Specific Status Values〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：Overlapping Range。

- 條件與限制：來源 keyword 索引：`may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 Overlapping Range 作為 parser 的第一個檢查點，再用 引用條件 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：Overlapping Range

- 來源 keyword 索引：`may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 193, 文件頁 206, PDF 頁 232

</details>

<details markdown="1">
<summary><strong>Figure 203: Get Log Page – Data Pointer</strong></summary>

<!-- claim:BASEFWLOG-FIG-203-CLAIM figure-table:BASEFWLOG-FIG-203 -->

Figure 203〈Get Log Page – Data Pointer〉：定義〈Get Log Page – Data Pointer〉如何指出本命令的來源或目的 buffer。 先判斷 pointer type 與 address，再核對 transfer length 和 alignment；來源欄位索引：DPTR。

- 解決的問題：定義〈Get Log Page – Data Pointer〉如何指出本命令的來源或目的 buffer。

- 閱讀順序：先判斷 pointer type 與 address，再核對 transfer length 和 alignment；來源欄位索引：DPTR。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：先驗證 DPTR 所代表的 pointer 形式，再核對 引用條件 對應的邊界，通過後才開始 transfer。 此例不新增規格要求。

- 來源欄位索引：DPTR

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 203, 文件頁 213, PDF 頁 239

</details>

<details markdown="1">
<summary><strong>Figure 204: Get Log Page – Command Dword 10</strong></summary>

<!-- claim:BASEFWLOG-FIG-204-CLAIM figure-table:BASEFWLOG-FIG-204 -->

Figure 204〈Get Log Page – Command Dword 10〉：定義〈Get Log Page – Command Dword 10〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：NUMDL, RAE, LSP, LID, NUMDU, Command。

- 解決的問題：定義〈Get Log Page – Command Dword 10〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：NUMDL, RAE, LSP, LID, NUMDU, Command。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 NUMDL，再以 RAE 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：NUMDL, RAE, LSP, LID, NUMDU, Command

- 來源 keyword 索引：`shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 204, 文件頁 213, PDF 頁 239

</details>

<details markdown="1">
<summary><strong>Figure 205: Get Log Page – Command Dword 11</strong></summary>

<!-- claim:BASEFWLOG-FIG-205-CLAIM figure-table:BASEFWLOG-FIG-205 -->

Figure 205〈Get Log Page – Command Dword 11〉：定義〈Get Log Page – Command Dword 11〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LSI, NUMDU, Command。

- 解決的問題：定義〈Get Log Page – Command Dword 11〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LSI, NUMDU, Command。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 LSI，再以 NUMDU 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：LSI, NUMDU, Command

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 205, 文件頁 214, PDF 頁 240

</details>

<details markdown="1">
<summary><strong>Figure 206: Get Log Page – Command Dword 12</strong></summary>

<!-- claim:BASEFWLOG-FIG-206-CLAIM figure-table:BASEFWLOG-FIG-206 -->

Figure 206〈Get Log Page – Command Dword 12〉：定義〈Get Log Page – Command Dword 12〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LPOL, OT, LPOU, IOS, LID, Command。

- 解決的問題：定義〈Get Log Page – Command Dword 12〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LPOL, OT, LPOU, IOS, LID, Command。

- 條件與限制：來源 keyword 索引：`shall`, `may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 LPOL，再以 OT 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：LPOL, OT, LPOU, IOS, LID, Command

- 來源 keyword 索引：`shall`, `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 206, 文件頁 214, PDF 頁 240

</details>

<details markdown="1">
<summary><strong>Figure 207: Get Log Page – Command Dword 13</strong></summary>

<!-- claim:BASEFWLOG-FIG-207-CLAIM figure-table:BASEFWLOG-FIG-207 -->

Figure 207〈Get Log Page – Command Dword 13〉：定義〈Get Log Page – Command Dword 13〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LPOU, UUID, Command。

- 解決的問題：定義〈Get Log Page – Command Dword 13〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LPOU, UUID, Command。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：先讀 LPOU，再以 UUID 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：LPOU, UUID, Command

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 207, 文件頁 214, PDF 頁 240

</details>

<details markdown="1">
<summary><strong>Figure 208: Get Log Page – Command Dword 14</strong></summary>

<!-- claim:BASEFWLOG-FIG-208-CLAIM figure-table:BASEFWLOG-FIG-208 -->

Figure 208〈Get Log Page – Command Dword 14〉：定義〈Get Log Page – Command Dword 14〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CSI, CC.CSS, Command。

- 解決的問題：定義〈Get Log Page – Command Dword 14〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CSI, CC.CSS, Command。

- 條件與限制：來源 keyword 索引：`shall`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 CSI，再以 CC.CSS 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：CSI, CC.CSS, Command

- 來源 keyword 索引：`shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 208, 文件頁 214-215, PDF 頁 240-241

</details>

<details markdown="1">
<summary><strong>Figure 209: Get Log Page – Log Page Identifiers</strong></summary>

<!-- claim:BASEFWLOG-FIG-209-CLAIM figure-table:BASEFWLOG-FIG-209 -->

Figure 209〈Get Log Page – Log Page Identifiers〉：定義〈Get Log Page – Log Page Identifiers〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CSI8, SMART, MI, FDP, SDSO, DSTO, UUID, MDS。

- 解決的問題：定義〈Get Log Page – Log Page Identifiers〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CSI8, SMART, MI, FDP, SDSO, DSTO, UUID, MDS。

- 條件與限制：來源 keyword 索引：`may`, `optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 本報告只解釋 PCIe／memory-based 部分。

- 說明性範例（informative example）：先讀 CSI8，再以 SMART 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：CSI8, SMART, MI, FDP, SDSO, DSTO, UUID, MDS

- 來源 keyword 索引：`may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 209, 文件頁 215-216, PDF 頁 241-242

</details>

<details markdown="1">
<summary><strong>Figure 210: Supported Log Pages Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-210-CLAIM figure-table:BASEFWLOG-FIG-210 -->

Figure 210〈Supported Log Pages Log Page〉：定義〈Supported Log Pages Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LIDS0, LIDS1, LIDS254, LIDS255, LID。

- 解決的問題：定義〈Supported Log Pages Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LIDS0, LIDS1, LIDS254, LIDS255, LID。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：先讀 LIDS0，再以 LIDS1 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：LIDS0, LIDS1, LIDS254, LIDS255, LID

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.1, Figure 210, 文件頁 217, PDF 頁 243

</details>

<details markdown="1">
<summary><strong>Figure 211: LID Supported and Effects Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-211-CLAIM figure-table:BASEFWLOG-FIG-211 -->

Figure 211〈LID Supported and Effects Data Structure〉：定義〈LID Supported and Effects Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：LIDSP, IOS, LSUPP, LID, OT, SPEDS, PA。

- 解決的問題：定義〈LID Supported and Effects Data Structure〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：LIDSP, IOS, LSUPP, LID, OT, SPEDS, PA。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 LIDSP 作為 parser 的第一個檢查點，再用 IOS 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：LIDSP, IOS, LSUPP, LID, OT, SPEDS, PA

- 來源 keyword 索引：`shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.1, Figure 211, 文件頁 217-218, PDF 頁 243-244

</details>

<details markdown="1">
<summary><strong>Figure 212: Error Information Log Entry Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-212-CLAIM figure-table:BASEFWLOG-FIG-212 -->

Figure 212〈Error Information Log Entry Data Structure〉：定義〈Error Information Log Entry Data Structure〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：ECNT, SQID, CID, STS, STATUS, PEL, BITLOC, BYTLOC。

- 解決的問題：定義〈Error Information Log Entry Data Structure〉所表示的 status／error 分類。

- 閱讀順序：先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：ECNT, SQID, CID, STS, STATUS, PEL, BITLOC, BYTLOC。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：收到一筆狀態時先辨認 ECNT，再檢查 SQID，不可脫離類別單看數值。 此例不新增規格要求。

- 來源欄位索引：ECNT, SQID, CID, STS, STATUS, PEL, BITLOC, BYTLOC

- 來源 keyword 索引：`shall`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.2, Figure 212, 文件頁 218-220, PDF 頁 244-246

</details>

<details markdown="1">
<summary><strong>Figure 213: SMART / Health Information Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-213-CLAIM figure-table:BASEFWLOG-FIG-213 -->

Figure 213〈SMART / Health Information Log Page〉：定義〈SMART / Health Information Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CW, IPS, PMRRO, VMBF, AMRO, NDR, TTC, ASCBT。

- 解決的問題：定義〈SMART / Health Information Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CW, IPS, PMRRO, VMBF, AMRO, NDR, TTC, ASCBT。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 CW，再以 IPS 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：CW, IPS, PMRRO, VMBF, AMRO, NDR, TTC, ASCBT

- 來源 keyword 索引：`shall not`, `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, Figure 213, 文件頁 221-225, PDF 頁 247-251

</details>

<details markdown="1">
<summary><strong>Figure 214: Temperature Sensor Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-214-CLAIM figure-table:BASEFWLOG-FIG-214 -->

Figure 214〈Temperature Sensor Data Structure〉：定義〈Temperature Sensor Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TST。

- 解決的問題：定義〈Temperature Sensor Data Structure〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TST。

- 條件與限制：來源 keyword 索引：`may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 TST 作為 parser 的第一個檢查點，再用 引用條件 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：TST

- 來源 keyword 索引：`may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, Figure 214, 文件頁 225, PDF 頁 251

</details>

<details markdown="1">
<summary><strong>Figure 215: Firmware Slot Information Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-215-CLAIM figure-table:BASEFWLOG-FIG-215 -->

Figure 215〈Firmware Slot Information Log Page〉：定義〈Firmware Slot Information Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：AFI, NAFS, CAFS, FRS1, FRS2, FRS3, FRS4, FRS5。

- 解決的問題：定義〈Firmware Slot Information Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：AFI, NAFS, CAFS, FRS1, FRS2, FRS3, FRS4, FRS5。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 AFI，再以 NAFS 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：AFI, NAFS, CAFS, FRS1, FRS2, FRS3, FRS4, FRS5

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, Figure 215, 文件頁 226, PDF 頁 252

</details>

<details markdown="1">
<summary><strong>Figure 216: Commands Supported and Effects Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-216-CLAIM figure-table:BASEFWLOG-FIG-216 -->

Figure 216〈Commands Supported and Effects Log Page〉：定義〈Commands Supported and Effects Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：ACS0, ACS1, ACS254, ACS255, IOCS0, IOCS1, IOCS254, IOCS255。

- 解決的問題：定義〈Commands Supported and Effects Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：ACS0, ACS1, ACS254, ACS255, IOCS0, IOCS1, IOCS254, IOCS255。

- 條件與限制：來源 keyword 索引：`should`, `may`, `optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 ACS0，再以 ACS1 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：ACS0, ACS1, ACS254, ACS255, IOCS0, IOCS1, IOCS254, IOCS255

- 來源 keyword 索引：`should`, `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.6, Figure 216, 文件頁 227, PDF 頁 253

</details>

<details markdown="1">
<summary><strong>Figure 217: Commands Supported and Effects Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-217-CLAIM figure-table:BASEFWLOG-FIG-217 -->

Figure 217〈Commands Supported and Effects Data Structure〉：定義〈Commands Supported and Effects Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CSP, NSSCPE, DSCPE, EGSCPE, NSETSCPE, CSCPE, NSCPE, USS。

- 解決的問題：定義〈Commands Supported and Effects Data Structure〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CSP, NSSCPE, DSCPE, EGSCPE, NSETSCPE, CSCPE, NSCPE, USS。

- 條件與限制：來源 keyword 索引：`should not`, `shall`, `should`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 CSP 作為 parser 的第一個檢查點，再用 NSSCPE 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：CSP, NSSCPE, DSCPE, EGSCPE, NSETSCPE, CSCPE, NSCPE, USS

- 來源 keyword 索引：`should not`, `shall`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.6, Figure 217, 文件頁 228-229, PDF 頁 254-255

</details>

<details markdown="1">
<summary><strong>Figure 218: Device Self-test Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-218-CLAIM figure-table:BASEFWLOG-FIG-218 -->

Figure 218〈Device Self-test Log Page〉：定義〈Device Self-test Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CDSTO, DSTOS, CDSTC, DSTCS, RDS1, RDS2, RDS19, RDS20。

- 解決的問題：定義〈Device Self-test Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CDSTO, DSTOS, CDSTC, DSTCS, RDS1, RDS2, RDS19, RDS20。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `should`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 CDSTO，再以 DSTOS 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：CDSTO, DSTOS, CDSTC, DSTCS, RDS1, RDS2, RDS19, RDS20

- 來源 keyword 索引：`shall not`, `shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, Figure 218, 文件頁 230, PDF 頁 256

</details>

<details markdown="1">
<summary><strong>Figure 219: Self-test Result Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-219-CLAIM figure-table:BASEFWLOG-FIG-219 -->

Figure 219〈Self-test Result Data Structure〉：定義〈Self-test Result Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DSTS, DSTC, DSTR, SEGN, VDINFO, SCVLD, SCTVLD, FVLD。

- 解決的問題：定義〈Self-test Result Data Structure〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DSTS, DSTC, DSTR, SEGN, VDINFO, SCVLD, SCTVLD, FVLD。

- 條件與限制：來源 keyword 索引：`should`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 DSTS 作為 parser 的第一個檢查點，再用 DSTC 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：DSTS, DSTC, DSTR, SEGN, VDINFO, SCVLD, SCTVLD, FVLD

- 來源 keyword 索引：`should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, Figure 219, 文件頁 231-232, PDF 頁 257-258

</details>

<details markdown="1">
<summary><strong>Figure 220: Telemetry Host-Initiated Log Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-220-CLAIM figure-table:BASEFWLOG-FIG-220 -->

Figure 220〈Telemetry Host-Initiated Log Specific Parameter Field〉：定義〈Telemetry Host-Initiated Log Specific Parameter Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MCDA, CTHID, MCDAS, LID, DA4S, ETDAS。

- 解決的問題：定義〈Telemetry Host-Initiated Log Specific Parameter Field〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MCDA, CTHID, MCDAS, LID, DA4S, ETDAS。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 MCDA 作為 parser 的第一個檢查點，再用 CTHID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：MCDA, CTHID, MCDAS, LID, DA4S, ETDAS

- 來源 keyword 索引：`shall not`, `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, Figure 220, 文件頁 232-233, PDF 頁 258-259

</details>

<details markdown="1">
<summary><strong>Figure 221: Telemetry Host-Initiated Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-221-CLAIM figure-table:BASEFWLOG-FIG-221 -->

Figure 221〈Telemetry Host-Initiated Log Page〉：定義〈Telemetry Host-Initiated Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LID, IEEE, THDA1LB, THDA2LB, THDA3LB, THDA4LB, THS, THDGN。

- 解決的問題：定義〈Telemetry Host-Initiated Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LID, IEEE, THDA1LB, THDA2LB, THDA3LB, THDA4LB, THS, THDGN。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `should`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 LID，再以 IEEE 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：LID, IEEE, THDA1LB, THDA2LB, THDA3LB, THDA4LB, THS, THDGN

- 來源 keyword 索引：`shall not`, `shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, Figure 221, 文件頁 234-235, PDF 頁 260-261

</details>

<details markdown="1">
<summary><strong>Figure 222: Telemetry Host-Initiated Log Page - LID Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-222-CLAIM figure-table:BASEFWLOG-FIG-222 -->

Figure 222〈Telemetry Host-Initiated Log Page - LID Specific Parameter Field〉：定義〈Telemetry Host-Initiated Log Page - LID Specific Parameter Field〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：MCDAS, LID。

- 解決的問題：定義〈Telemetry Host-Initiated Log Page - LID Specific Parameter Field〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：MCDAS, LID。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 MCDAS，再以 LID 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：MCDAS, LID

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, Figure 222, 文件頁 235, PDF 頁 261

</details>

<details markdown="1">
<summary><strong>Figure 223: Telemetry Controller-Initiated Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-223-CLAIM figure-table:BASEFWLOG-FIG-223 -->

Figure 223〈Telemetry Controller-Initiated Log Page〉：定義〈Telemetry Controller-Initiated Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LID, IEEE, TCDA1LB, TCDA2LB, TCDA3LB, TCDA4LB, TCS, TCDA。

- 解決的問題：定義〈Telemetry Controller-Initiated Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LID, IEEE, TCDA1LB, TCDA2LB, TCDA3LB, TCDA4LB, TCS, TCDA。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `should`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 LID，再以 IEEE 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：LID, IEEE, TCDA1LB, TCDA2LB, TCDA3LB, TCDA4LB, TCS, TCDA

- 來源 keyword 索引：`shall not`, `shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, Figure 223, 文件頁 236-237, PDF 頁 262-263

</details>

<details markdown="1">
<summary><strong>Figure 224: Endurance Group Identifier - Log Specific Identifier</strong></summary>

<!-- claim:BASEFWLOG-FIG-224-CLAIM figure-table:BASEFWLOG-FIG-224 -->

Figure 224〈Endurance Group Identifier - Log Specific Identifier〉：定義〈Endurance Group Identifier - Log Specific Identifier〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：ENDGID, Endurance Group。

- 解決的問題：定義〈Endurance Group Identifier - Log Specific Identifier〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：ENDGID, Endurance Group。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依定義寬度解析 ENDGID，再核對 Endurance Group 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：ENDGID, Endurance Group

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.10, Figure 224, 文件頁 237, PDF 頁 263

</details>

<details markdown="1">
<summary><strong>Figure 225: Endurance Group Information Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-225-CLAIM figure-table:BASEFWLOG-FIG-225 -->

Figure 225〈Endurance Group Information Log Page〉：定義〈Endurance Group Information Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：EGCW, EGRO, EGDR, EGASB, EGFEAT, AVSP, AVSPT, PUSED。

- 解決的問題：定義〈Endurance Group Information Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：EGCW, EGRO, EGDR, EGASB, EGFEAT, AVSP, AVSPT, PUSED。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 EGCW，再以 EGRO 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：EGCW, EGRO, EGDR, EGASB, EGFEAT, AVSP, AVSPT, PUSED

- 來源 keyword 索引：`shall not`, `shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.10, Figure 225, 文件頁 238-239, PDF 頁 264-265

</details>

<details markdown="1">
<summary><strong>Figure 226: NVM Set Identifier – Log Specific Identifier</strong></summary>

<!-- claim:BASEFWLOG-FIG-226-CLAIM figure-table:BASEFWLOG-FIG-226 -->

Figure 226〈NVM Set Identifier – Log Specific Identifier〉：定義〈NVM Set Identifier – Log Specific Identifier〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NVMSETID, NVM Set。

- 解決的問題：定義〈NVM Set Identifier – Log Specific Identifier〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：NVMSETID, NVM Set。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：依定義寬度解析 NVMSETID，再核對 NVM Set 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：NVMSETID, NVM Set

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.11, Figure 226, 文件頁 240, PDF 頁 266

</details>

<details markdown="1">
<summary><strong>Figure 227: Predictable Latency Per NVM Set Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-227-CLAIM figure-table:BASEFWLOG-FIG-227 -->

Figure 227〈Predictable Latency Per NVM Set Log Page〉：定義〈Predictable Latency Per NVM Set Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：STSNVMS, PLMW, ETYP, DEAT, MVEAT, DTWRT, DTWWT, DTWTM。

- 解決的問題：定義〈Predictable Latency Per NVM Set Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：STSNVMS, PLMW, ETYP, DEAT, MVEAT, DTWRT, DTWWT, DTWTM。

- 條件與限制：來源 keyword 索引：`may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 STSNVMS，再以 PLMW 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：STSNVMS, PLMW, ETYP, DEAT, MVEAT, DTWRT, DTWWT, DTWTM

- 來源 keyword 索引：`may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.11, Figure 227, 文件頁 240-241, PDF 頁 266-267

</details>

<details markdown="1">
<summary><strong>Figure 228: Predictable Latency Event Aggregate Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-228-CLAIM figure-table:BASEFWLOG-FIG-228 -->

Figure 228〈Predictable Latency Event Aggregate Log Page〉：定義〈Predictable Latency Event Aggregate Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：NUMENT, NEMENT。

- 解決的問題：定義〈Predictable Latency Event Aggregate Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：NUMENT, NEMENT。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：先讀 NUMENT，再以 NEMENT 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：NUMENT, NEMENT

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.12, Figure 228, 文件頁 241, PDF 頁 267

</details>

<details markdown="1">
<summary><strong>Figure 229: Asymmetric Namespace Access Log Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-229-CLAIM figure-table:BASEFWLOG-FIG-229 -->

Figure 229〈Asymmetric Namespace Access Log Specific Parameter Field〉：定義〈Asymmetric Namespace Access Log Specific Parameter Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：RGO, ANA, NSID, Namespace。

- 解決的問題：定義〈Asymmetric Namespace Access Log Specific Parameter Field〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：RGO, ANA, NSID, Namespace。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 RGO 作為 parser 的第一個檢查點，再用 ANA 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：RGO, ANA, NSID, Namespace

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.13, Figure 229, 文件頁 242, PDF 頁 268

</details>

<details markdown="1">
<summary><strong>Figure 230: Asymmetric Namespace Access Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-230-CLAIM figure-table:BASEFWLOG-FIG-230 -->

Figure 230〈Asymmetric Namespace Access Log Page〉：定義〈Asymmetric Namespace Access Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CHGC, NAGD, ANA, NSID, Namespace。

- 解決的問題：定義〈Asymmetric Namespace Access Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CHGC, NAGD, ANA, NSID, Namespace。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 CHGC，再以 NAGD 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：CHGC, NAGD, ANA, NSID, Namespace

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.13, Figure 230, 文件頁 242-243, PDF 頁 268-269

</details>

<details markdown="1">
<summary><strong>Figure 231: ANA Group Descriptor format</strong></summary>

<!-- claim:BASEFWLOG-FIG-231-CLAIM figure-table:BASEFWLOG-FIG-231 -->

Figure 231〈ANA Group Descriptor format〉：定義〈ANA Group Descriptor format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：AGID, NNV, CHGC, ANASA, ANAS, ANA, ID, NSID。

- 解決的問題：定義〈ANA Group Descriptor format〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：AGID, NNV, CHGC, ANASA, ANAS, ANA, ID, NSID。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 AGID 作為 parser 的第一個檢查點，再用 NNV 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：AGID, NNV, CHGC, ANASA, ANAS, ANA, ID, NSID

- 來源 keyword 索引：`shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.13, Figure 231, 文件頁 243-244, PDF 頁 269-270

</details>

<details markdown="1">
<summary><strong>Figure 232: Persistent Event Log Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-232-CLAIM figure-table:BASEFWLOG-FIG-232 -->

Figure 232〈Persistent Event Log Specific Parameter Field〉：定義〈Persistent Event Log Specific Parameter Field〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：ACT, LPOU, LPOL, NUMDU, NUMDL。

- 解決的問題：定義〈Persistent Event Log Specific Parameter Field〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：ACT, LPOU, LPOL, NUMDU, NUMDL。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先辨認 ACT，以 LPOU 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：ACT, LPOU, LPOL, NUMDU, NUMDL

- 來源 keyword 索引：`shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14, Figure 232, 文件頁 246, PDF 頁 272

</details>

<details markdown="1">
<summary><strong>Figure 233: Persistent Event Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-233-CLAIM figure-table:BASEFWLOG-FIG-233 -->

Figure 233〈Persistent Event Log Page〉：定義〈Persistent Event Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LID, TNEV, TLL, LREV, LHL, TSTMP, POH, PWRCC。

- 解決的問題：定義〈Persistent Event Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LID, TNEV, TLL, LREV, LHL, TSTMP, POH, PWRCC。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 LID，再以 TNEV 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：LID, TNEV, TLL, LREV, LHL, TSTMP, POH, PWRCC

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14, Figure 233, 文件頁 247-249, PDF 頁 273-275

</details>

<details markdown="1">
<summary><strong>Figure 234: Persistent Event Format</strong></summary>

<!-- claim:BASEFWLOG-FIG-234-CLAIM figure-table:BASEFWLOG-FIG-234 -->

Figure 234〈Persistent Event Format〉：定義〈Persistent Event Format〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：ET, EHAI, PIT, CNTLID, ETSTP, PELPID, VSIL, EL。

- 解決的問題：定義〈Persistent Event Format〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：ET, EHAI, PIT, CNTLID, ETSTP, PELPID, VSIL, EL。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先辨認 ET，以 EHAI 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：ET, EHAI, PIT, CNTLID, ETSTP, PELPID, VSIL, EL

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14, Figure 234, 文件頁 249-250, PDF 頁 275-276

</details>

<details markdown="1">
<summary><strong>Figure 235: Persistent Event LID Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-235-CLAIM figure-table:BASEFWLOG-FIG-235 -->

Figure 235〈Persistent Event LID Specific Parameter Field〉：定義〈Persistent Event LID Specific Parameter Field〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：ECRH, LID。

- 解決的問題：定義〈Persistent Event LID Specific Parameter Field〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：ECRH, LID。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先辨認 ECRH，以 LID 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：ECRH, LID

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14, Figure 235, 文件頁 251, PDF 頁 277

</details>

<details markdown="1">
<summary><strong>Figure 236: Persistent Event Log Event Types</strong></summary>

<!-- claim:BASEFWLOG-FIG-236-CLAIM figure-table:BASEFWLOG-FIG-236 -->

Figure 236〈Persistent Event Log Event Types〉：定義〈Persistent Event Log Event Types〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：M1, NOTE, SMART, TCG。

- 解決的問題：定義〈Persistent Event Log Event Types〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：M1, NOTE, SMART, TCG。

- 條件與限制：來源 keyword 索引：`optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先辨認 M1，以 NOTE 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：M1, NOTE, SMART, TCG

- 來源 keyword 索引：`optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14, Figure 236, 文件頁 251, PDF 頁 277

</details>

<details markdown="1">
<summary><strong>Figure 237: SMART / Health Log Snapshot Event Data Format (Event Type 01h)</strong></summary>

<!-- claim:BASEFWLOG-FIG-237-CLAIM figure-table:BASEFWLOG-FIG-237 -->

Figure 237〈SMART / Health Log Snapshot Event Data Format (Event Type 01h)〉：定義〈SMART / Health Log Snapshot Event Data Format (Event Type 01h)〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：ED, SMART。

- 解決的問題：定義〈SMART / Health Log Snapshot Event Data Format (Event Type 01h)〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：ED, SMART。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：先辨認 ED，以 SMART 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：ED, SMART

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 237, 文件頁 252, PDF 頁 278

</details>

<details markdown="1">
<summary><strong>Figure 238: Firmware Commit Event Data Format (Event Type 02h)</strong></summary>

<!-- claim:BASEFWLOG-FIG-238-CLAIM figure-table:BASEFWLOG-FIG-238 -->

Figure 238〈Firmware Commit Event Data Format (Event Type 02h)〉：定義〈Firmware Commit Event Data Format (Event Type 02h)〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：OFR, NFR, FCA, FSLT, STCTFCC, SRFCC, VAFCRC。

- 解決的問題：定義〈Firmware Commit Event Data Format (Event Type 02h)〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：OFR, NFR, FCA, FSLT, STCTFCC, SRFCC, VAFCRC。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：先辨認 OFR，以 NFR 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：OFR, NFR, FCA, FSLT, STCTFCC, SRFCC, VAFCRC

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 238, 文件頁 252, PDF 頁 278

</details>

<details markdown="1">
<summary><strong>Figure 239: Timestamp Change Event Format (Event Type 03h)</strong></summary>

<!-- claim:BASEFWLOG-FIG-239-CLAIM figure-table:BASEFWLOG-FIG-239 -->

Figure 239〈Timestamp Change Event Format (Event Type 03h)〉：定義〈Timestamp Change Event Format (Event Type 03h)〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：PTSTP, MSR。

- 解決的問題：定義〈Timestamp Change Event Format (Event Type 03h)〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：PTSTP, MSR。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：先辨認 PTSTP，以 MSR 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：PTSTP, MSR

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 239, 文件頁 253, PDF 頁 279

</details>

<details markdown="1">
<summary><strong>Figure 240: Power-on or Reset Event (Event Type 04h)</strong></summary>

<!-- claim:BASEFWLOG-FIG-240-CLAIM figure-table:BASEFWLOG-FIG-240 -->

Figure 240〈Power-on or Reset Event (Event Type 04h)〉：定義〈Power-on or Reset Event (Event Type 04h)〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：FREV, RIL, CC.EN, EL, VSIL。

- 解決的問題：定義〈Power-on or Reset Event (Event Type 04h)〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：FREV, RIL, CC.EN, EL, VSIL。

- 條件與限制：來源 keyword 索引：`shall`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先辨認 FREV，以 RIL 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：FREV, RIL, CC.EN, EL, VSIL

- 來源 keyword 索引：`shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 240, 文件頁 253, PDF 頁 279

</details>

<details markdown="1">
<summary><strong>Figure 241: Controller Reset Information descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-241-CLAIM figure-table:BASEFWLOG-FIG-241 -->

Figure 241〈Controller Reset Information descriptor〉：定義〈Controller Reset Information descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CNTLID, FA, OIP, RDNF, CPWRC, POM, CTSTP, ID。

- 解決的問題：定義〈Controller Reset Information descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CNTLID, FA, OIP, RDNF, CPWRC, POM, CTSTP, ID。

- 條件與限制：來源 keyword 索引：`may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 CNTLID 作為 parser 的第一個檢查點，再用 FA 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：CNTLID, FA, OIP, RDNF, CPWRC, POM, CTSTP, ID

- 來源 keyword 索引：`may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 241, 文件頁 253-254, PDF 頁 279-280

</details>

<details markdown="1">
<summary><strong>Figure 242: NVM Subsystem Hardware Error Event Format (Event Type 05h)</strong></summary>

<!-- claim:BASEFWLOG-FIG-242-CLAIM figure-table:BASEFWLOG-FIG-242 -->

Figure 242〈NVM Subsystem Hardware Error Event Format (Event Type 05h)〉：定義〈NVM Subsystem Hardware Error Event Format (Event Type 05h)〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：NSHEEC, AHEI, NVM Subsystem。

- 解決的問題：定義〈NVM Subsystem Hardware Error Event Format (Event Type 05h)〉所表示的 status／error 分類。

- 閱讀順序：先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：NSHEEC, AHEI, NVM Subsystem。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：收到一筆狀態時先辨認 NSHEEC，再檢查 AHEI，不可脫離類別單看數值。 此例不新增規格要求。

- 來源欄位索引：NSHEEC, AHEI, NVM Subsystem

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 242, 文件頁 254, PDF 頁 280

</details>

<details markdown="1">
<summary><strong>Figure 243: NVM Subsystem Hardware Error Event Codes</strong></summary>

<!-- claim:BASEFWLOG-FIG-243-CLAIM figure-table:BASEFWLOG-FIG-243 -->

Figure 243〈NVM Subsystem Hardware Error Event Codes〉：定義〈NVM Subsystem Hardware Error Event Codes〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：EGCW, EGID, SMART, CSTS.CFS, CRTO.CRWMT, CC.CRIME, CRTO.CRIMT, CC.EN。

- 解決的問題：定義〈NVM Subsystem Hardware Error Event Codes〉所表示的 status／error 分類。

- 閱讀順序：先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：EGCW, EGID, SMART, CSTS.CFS, CRTO.CRWMT, CC.CRIME, CRTO.CRIMT, CC.EN。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：收到一筆狀態時先辨認 EGCW，再檢查 EGID，不可脫離類別單看數值。 此例不新增規格要求。

- 來源欄位索引：EGCW, EGID, SMART, CSTS.CFS, CRTO.CRWMT, CC.CRIME, CRTO.CRIMT, CC.EN

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 243, 文件頁 254-256, PDF 頁 280-282

</details>

<details markdown="1">
<summary><strong>Figure 244: Additional Hardware Error Information for Unexpected Power Loss Errors</strong></summary>

<!-- claim:BASEFWLOG-FIG-244-CLAIM figure-table:BASEFWLOG-FIG-244 -->

Figure 244〈Additional Hardware Error Information for Unexpected Power Loss Errors〉：定義〈Additional Hardware Error Information for Unexpected Power Loss Errors〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：UPL, UPLI, UPLOA, SMART, CSTS.SHST。

- 解決的問題：定義〈Additional Hardware Error Information for Unexpected Power Loss Errors〉所表示的 status／error 分類。

- 閱讀順序：先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：UPL, UPLI, UPLOA, SMART, CSTS.SHST。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：收到一筆狀態時先辨認 UPL，再檢查 UPLI，不可脫離類別單看數值。 此例不新增規格要求。

- 來源欄位索引：UPL, UPLI, UPLOA, SMART, CSTS.SHST

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 244, 文件頁 256, PDF 頁 282

</details>

<details markdown="1">
<summary><strong>Figure 245: Additional Hardware Error Information for correctable and uncorrectable PCIe errors</strong></summary>

<!-- claim:BASEFWLOG-FIG-245-CLAIM figure-table:BASEFWLOG-FIG-245 -->

Figure 245〈Additional Hardware Error Information for correctable and uncorrectable PCIe errors〉：定義〈Additional Hardware Error Information for correctable and uncorrectable PCIe errors〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：PCIEAS, PCIEAERS, PCIe AER Error Status, PCIe AER Error Mask。

- 解決的問題：定義〈Additional Hardware Error Information for correctable and uncorrectable PCIe errors〉所表示的 status／error 分類。

- 閱讀順序：先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：PCIEAS, PCIEAERS, PCIe AER Error Status, PCIe AER Error Mask。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：收到一筆狀態時先辨認 PCIEAS，再檢查 PCIEAERS，不可脫離類別單看數值。 此例不新增規格要求。

- 來源欄位索引：PCIEAS, PCIEAERS, PCIe AER Error Status, PCIe AER Error Mask

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 245, 文件頁 256-257, PDF 頁 282-283

</details>

<details markdown="1">
<summary><strong>Figure 246: Additional Hardware Error Information for Controller Ready Timeout</strong></summary>

<!-- claim:BASEFWLOG-FIG-246-CLAIM figure-table:BASEFWLOG-FIG-246 -->

Figure 246〈Additional Hardware Error Information for Controller Ready Timeout〉：定義〈Additional Hardware Error Information for Controller Ready Timeout〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：CST, CNR, ACMNR, NNR, CRIME, CRTO.CRWMT, CC.CRIME, CRTO.CRIMT。

- 解決的問題：定義〈Additional Hardware Error Information for Controller Ready Timeout〉所表示的 status／error 分類。

- 閱讀順序：先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：CST, CNR, ACMNR, NNR, CRIME, CRTO.CRWMT, CC.CRIME, CRTO.CRIMT。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：收到一筆狀態時先辨認 CST，再檢查 CNR，不可脫離類別單看數值。 此例不新增規格要求。

- 來源欄位索引：CST, CNR, ACMNR, NNR, CRIME, CRTO.CRWMT, CC.CRIME, CRTO.CRIMT

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 246, 文件頁 258, PDF 頁 284

</details>

<details markdown="1">
<summary><strong>Figure 247: Change Namespace Event Data Format (Event Type 06h)</strong></summary>

<!-- claim:BASEFWLOG-FIG-247-CLAIM figure-table:BASEFWLOG-FIG-247 -->

Figure 247〈Change Namespace Event Data Format (Event Type 06h)〉：定義〈Change Namespace Event Data Format (Event Type 06h)〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：NMCDW10, NSZE, NCAP, FLBAS, DPS, NMIC, ANAGRPID, NVMSETID。

- 解決的問題：定義〈Change Namespace Event Data Format (Event Type 06h)〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：NMCDW10, NSZE, NCAP, FLBAS, DPS, NMIC, ANAGRPID, NVMSETID。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先辨認 NMCDW10，以 NSZE 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：NMCDW10, NSZE, NCAP, FLBAS, DPS, NMIC, ANAGRPID, NVMSETID

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 247, 文件頁 258-259, PDF 頁 284-285

</details>

<details markdown="1">
<summary><strong>Figure 248: Format NVM Start Event Data Format (Event Type 07h)</strong></summary>

<!-- claim:BASEFWLOG-FIG-248-CLAIM figure-table:BASEFWLOG-FIG-248 -->

Figure 248〈Format NVM Start Event Data Format (Event Type 07h)〉：定義〈Format NVM Start Event Data Format (Event Type 07h)〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：NSID, FNA, FMCDW10, CDW10。

- 解決的問題：定義〈Format NVM Start Event Data Format (Event Type 07h)〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：NSID, FNA, FMCDW10, CDW10。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先辨認 NSID，以 FNA 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：NSID, FNA, FMCDW10, CDW10

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 248, 文件頁 260, PDF 頁 286

</details>

<details markdown="1">
<summary><strong>Figure 249: Format NVM Completion Event Data Format (Event Type 08h)</strong></summary>

<!-- claim:BASEFWLOG-FIG-249-CLAIM figure-table:BASEFWLOG-FIG-249 -->

Figure 249〈Format NVM Completion Event Data Format (Event Type 08h)〉：定義〈Format NVM Completion Event Data Format (Event Type 08h)〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：NSID, SFPI, FNVMS, INCPLTF, FNVME, CINFO, INFO, STATUS。

- 解決的問題：定義〈Format NVM Completion Event Data Format (Event Type 08h)〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：NSID, SFPI, FNVMS, INCPLTF, FNVME, CINFO, INFO, STATUS。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先辨認 NSID，以 SFPI 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：NSID, SFPI, FNVMS, INCPLTF, FNVME, CINFO, INFO, STATUS

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 249, 文件頁 260-261, PDF 頁 286-287

</details>

<details markdown="1">
<summary><strong>Figure 250: Sanitize Start Event Data Format (Event Type 09h)</strong></summary>

<!-- claim:BASEFWLOG-FIG-250-CLAIM figure-table:BASEFWLOG-FIG-250 -->

Figure 250〈Sanitize Start Event Data Format (Event Type 09h)〉：定義〈Sanitize Start Event Data Format (Event Type 09h)〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：SCDW10, SCDW11, NSID, SANICAP, CDW10, CDW11。

- 解決的問題：定義〈Sanitize Start Event Data Format (Event Type 09h)〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：SCDW10, SCDW11, NSID, SANICAP, CDW10, CDW11。

- 條件與限制：來源 keyword 索引：`shall`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先辨認 SCDW10，以 SCDW11 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：SCDW10, SCDW11, NSID, SANICAP, CDW10, CDW11

- 來源 keyword 索引：`shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 250, 文件頁 261, PDF 頁 287

</details>

<details markdown="1">
<summary><strong>Figure 251: Sanitize Completion Event Data Format (Event Type 0Ah)</strong></summary>

<!-- claim:BASEFWLOG-FIG-251-CLAIM figure-table:BASEFWLOG-FIG-251 -->

Figure 251〈Sanitize Completion Event Data Format (Event Type 0Ah)〉：定義〈Sanitize Completion Event Data Format (Event Type 0Ah)〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：SPROG, SSTAT, CINFO, NSID。

- 解決的問題：定義〈Sanitize Completion Event Data Format (Event Type 0Ah)〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：SPROG, SSTAT, CINFO, NSID。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先辨認 SPROG，以 SSTAT 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：SPROG, SSTAT, CINFO, NSID

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 251, 文件頁 261-262, PDF 頁 287-288

</details>

<details markdown="1">
<summary><strong>Figure 252: Feature Persistent Event Logging Requirements</strong></summary>

<!-- claim:BASEFWLOG-FIG-252-CLAIM figure-table:BASEFWLOG-FIG-252 -->

Figure 252〈Feature Persistent Event Logging Requirements〉：定義〈Feature Persistent Event Logging Requirements〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：PE, NR。

- 解決的問題：定義〈Feature Persistent Event Logging Requirements〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：PE, NR。

- 條件與限制：來源 keyword 索引：`optional`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先辨認 PE，以 NR 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：PE, NR

- 來源 keyword 索引：`optional`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 252, 文件頁 262-263, PDF 頁 288-289

</details>

<details markdown="1">
<summary><strong>Figure 253: Set Feature Event Data Format</strong></summary>

<!-- claim:BASEFWLOG-FIG-253-CLAIM figure-table:BASEFWLOG-FIG-253 -->

Figure 253〈Set Feature Event Data Format〉：定義〈Set Feature Event Data Format〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：SFEL, MBC, LCCDW0, DWC, CDWS, MBUF, CCDW0。

- 解決的問題：定義〈Set Feature Event Data Format〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：SFEL, MBC, LCCDW0, DWC, CDWS, MBUF, CCDW0。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先辨認 SFEL，以 MBC 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：SFEL, MBC, LCCDW0, DWC, CDWS, MBUF, CCDW0

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 253, 文件頁 264, PDF 頁 290

</details>

<details markdown="1">
<summary><strong>Figure 254: Telemetry Log Created Event Data Format (Event Type 0Ch)</strong></summary>

<!-- claim:BASEFWLOG-FIG-254-CLAIM figure-table:BASEFWLOG-FIG-254 -->

Figure 254〈Telemetry Log Created Event Data Format (Event Type 0Ch)〉：定義〈Telemetry Log Created Event Data Format (Event Type 0Ch)〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：TIL。

- 解決的問題：定義〈Telemetry Log Created Event Data Format (Event Type 0Ch)〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：TIL。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：先辨認 TIL，以 引用條件 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：TIL

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 254, 文件頁 264, PDF 頁 290

</details>

<details markdown="1">
<summary><strong>Figure 255: Thermal Excursion Event Data Format (Event Type 0Dh)</strong></summary>

<!-- claim:BASEFWLOG-FIG-255-CLAIM figure-table:BASEFWLOG-FIG-255 -->

Figure 255〈Thermal Excursion Event Data Format (Event Type 0Dh)〉：定義〈Thermal Excursion Event Data Format (Event Type 0Dh)〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：OTMP, THRESH, WCTEMP, CCTEMP, TMT1, TMT2。

- 解決的問題：定義〈Thermal Excursion Event Data Format (Event Type 0Dh)〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：OTMP, THRESH, WCTEMP, CCTEMP, TMT1, TMT2。

- 條件與限制：來源 keyword 索引：`may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先辨認 OTMP，以 THRESH 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：OTMP, THRESH, WCTEMP, CCTEMP, TMT1, TMT2

- 來源 keyword 索引：`may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 255, 文件頁 265-266, PDF 頁 291-292

</details>

<details markdown="1">
<summary><strong>Figure 256: CDP Change Event Data Format (Event Type 0Fh)</strong></summary>

<!-- claim:BASEFWLOG-FIG-256-CLAIM figure-table:BASEFWLOG-FIG-256 -->

Figure 256〈CDP Change Event Data Format (Event Type 0Fh)〉：定義〈CDP Change Event Data Format (Event Type 0Fh)〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：PS, CDPRFS, CDPCE, PERID, PED, CDP, EL。

- 解決的問題：定義〈CDP Change Event Data Format (Event Type 0Fh)〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：PS, CDPRFS, CDPCE, PERID, PED, CDP, EL。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先辨認 PS，以 CDPRFS 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：PS, CDPRFS, CDPCE, PERID, PED, CDP, EL

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 256, 文件頁 267, PDF 頁 293

</details>

<details markdown="1">
<summary><strong>Figure 258: Vendor Specific Event Format (Event Type DEh)</strong></summary>

<!-- claim:BASEFWLOG-FIG-258-CLAIM figure-table:BASEFWLOG-FIG-258 -->

Figure 258〈Vendor Specific Event Format (Event Type DEh)〉：定義〈Vendor Specific Event Format (Event Type DEh)〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：EL, VSIL。

- 解決的問題：定義〈Vendor Specific Event Format (Event Type DEh)〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：EL, VSIL。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：先辨認 EL，以 VSIL 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：EL, VSIL

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 258, 文件頁 269, PDF 頁 295

</details>

<details markdown="1">
<summary><strong>Figure 259: Vendor Specific Event Descriptor Format</strong></summary>

<!-- claim:BASEFWLOG-FIG-259-CLAIM figure-table:BASEFWLOG-FIG-259 -->

Figure 259〈Vendor Specific Event Descriptor Format〉：定義〈Vendor Specific Event Descriptor Format〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：VSEC, VSEDT, UIDX, VSEDL, VSED, UUID。

- 解決的問題：定義〈Vendor Specific Event Descriptor Format〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：VSEC, VSEDT, UIDX, VSEDL, VSED, UUID。

- 條件與限制：來源 keyword 索引：`should`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先辨認 VSEC，以 VSEDT 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：VSEC, VSEDT, UIDX, VSEDL, VSED, UUID

- 來源 keyword 索引：`should`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 259, 文件頁 269, PDF 頁 295

</details>

<details markdown="1">
<summary><strong>Figure 260: Vendor Specific Event Data Type Codes</strong></summary>

<!-- claim:BASEFWLOG-FIG-260-CLAIM figure-table:BASEFWLOG-FIG-260 -->

Figure 260〈Vendor Specific Event Data Type Codes〉：定義〈Vendor Specific Event Data Type Codes〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：ASCII。

- 解決的問題：定義〈Vendor Specific Event Data Type Codes〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：ASCII。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先辨認 ASCII，以 引用條件 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：ASCII

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.14.2, Figure 260, 文件頁 269-270, PDF 頁 295-296

</details>

<details markdown="1">
<summary><strong>Figure 261: Endurance Group Event Aggregate Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-261-CLAIM figure-table:BASEFWLOG-FIG-261 -->

Figure 261〈Endurance Group Event Aggregate Log Page〉：定義〈Endurance Group Event Aggregate Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：NUMENT, Endurance Group。

- 解決的問題：定義〈Endurance Group Event Aggregate Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：NUMENT, Endurance Group。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：先讀 NUMENT，再以 Endurance Group 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：NUMENT, Endurance Group

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.15, Figure 261, 文件頁 270, PDF 頁 296

</details>

<details markdown="1">
<summary><strong>Figure 262: Domain Identifier – Log Specific Identifier</strong></summary>

<!-- claim:BASEFWLOG-FIG-262-CLAIM figure-table:BASEFWLOG-FIG-262 -->

Figure 262〈Domain Identifier – Log Specific Identifier〉：定義〈Domain Identifier – Log Specific Identifier〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：DID, Domain。

- 解決的問題：定義〈Domain Identifier – Log Specific Identifier〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：DID, Domain。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依定義寬度解析 DID，再核對 Domain 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：DID, Domain

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.16, Figure 262, 文件頁 271, PDF 頁 297

</details>

<details markdown="1">
<summary><strong>Figure 263: Media Unit Status Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-263-CLAIM figure-table:BASEFWLOG-FIG-263 -->

Figure 263〈Media Unit Status Log Page〉：定義〈Media Unit Status Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：NMU, CCHANS, SELC, NOTE, ENDGID, NVMSETID, MUCS。

- 解決的問題：定義〈Media Unit Status Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：NMU, CCHANS, SELC, NOTE, ENDGID, NVMSETID, MUCS。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 NMU，再以 CCHANS 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：NMU, CCHANS, SELC, NOTE, ENDGID, NVMSETID, MUCS

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.16, Figure 263, 文件頁 271, PDF 頁 297

</details>

<details markdown="1">
<summary><strong>Figure 264: Media Unit Status Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-264-CLAIM figure-table:BASEFWLOG-FIG-264 -->

Figure 264〈Media Unit Status Descriptor〉：定義〈Media Unit Status Descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MUID, DID, ENDGID, NVMSETID, CAF, AVSP, PUSED, CIO。

- 解決的問題：定義〈Media Unit Status Descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MUID, DID, ENDGID, NVMSETID, CAF, AVSP, PUSED, CIO。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 MUID 作為 parser 的第一個檢查點，再用 DID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：MUID, DID, ENDGID, NVMSETID, CAF, AVSP, PUSED, CIO

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.16, Figure 264, 文件頁 272, PDF 頁 298

</details>

<details markdown="1">
<summary><strong>Figure 265: Supported Capacity Configuration List Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-265-CLAIM figure-table:BASEFWLOG-FIG-265 -->

Figure 265〈Supported Capacity Configuration List Log Page〉：定義〈Supported Capacity Configuration List Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：SCCN, NOTE。

- 解決的問題：定義〈Supported Capacity Configuration List Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：SCCN, NOTE。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 SCCN，再以 NOTE 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：SCCN, NOTE

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.17, Figure 265, 文件頁 273, PDF 頁 299

</details>

<details markdown="1">
<summary><strong>Figure 266: Capacity Configuration Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-266-CLAIM figure-table:BASEFWLOG-FIG-266 -->

Figure 266〈Capacity Configuration Descriptor〉：定義〈Capacity Configuration Descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CCID, DID, EGCN, NOTE。

- 解決的問題：定義〈Capacity Configuration Descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CCID, DID, EGCN, NOTE。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 CCID 作為 parser 的第一個檢查點，再用 DID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：CCID, DID, EGCN, NOTE

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.17, Figure 266, 文件頁 273-274, PDF 頁 299-300

</details>

<details markdown="1">
<summary><strong>Figure 267: Endurance Group Configuration Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-267-CLAIM figure-table:BASEFWLOG-FIG-267 -->

Figure 267〈Endurance Group Configuration Descriptor〉：定義〈Endurance Group Configuration Descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ENDGID, CADJF, TEGCAP, SEGCAP, EE, EGSETS, EGCHANS, NOTE。

- 解決的問題：定義〈Endurance Group Configuration Descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ENDGID, CADJF, TEGCAP, SEGCAP, EE, EGSETS, EGCHANS, NOTE。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 ENDGID 作為 parser 的第一個檢查點，再用 CADJF 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：ENDGID, CADJF, TEGCAP, SEGCAP, EE, EGSETS, EGCHANS, NOTE

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.17, Figure 267, 文件頁 274-275, PDF 頁 300-301

</details>

<details markdown="1">
<summary><strong>Figure 268: Channel Configuration Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-268-CLAIM figure-table:BASEFWLOG-FIG-268 -->

Figure 268〈Channel Configuration Descriptor〉：定義〈Channel Configuration Descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CHID, CHMUS, NOTE。

- 解決的問題：定義〈Channel Configuration Descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CHID, CHMUS, NOTE。

- 條件與限制：來源 keyword 索引：`may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 CHID 作為 parser 的第一個檢查點，再用 CHMUS 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：CHID, CHMUS, NOTE

- 來源 keyword 索引：`may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.17, Figure 268, 文件頁 275, PDF 頁 301

</details>

<details markdown="1">
<summary><strong>Figure 269: Media Unit Configuration Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-269-CLAIM figure-table:BASEFWLOG-FIG-269 -->

Figure 269〈Media Unit Configuration Descriptor〉：定義〈Media Unit Configuration Descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MUID, MUDL。

- 解決的問題：定義〈Media Unit Configuration Descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MUID, MUDL。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 MUID 作為 parser 的第一個檢查點，再用 MUDL 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：MUID, MUDL

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.17, Figure 269, 文件頁 276, PDF 頁 302

</details>

<details markdown="1">
<summary><strong>Figure 270: Feature Identifiers Effects Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-270-CLAIM figure-table:BASEFWLOG-FIG-270 -->

Figure 270〈Feature Identifiers Effects Log Page〉：定義〈Feature Identifiers Effects Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：FIS0, FIS1, FIS254, FIS255, FID。

- 解決的問題：定義〈Feature Identifiers Effects Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：FIS0, FIS1, FIS254, FIS255, FID。

- 條件與限制：來源 keyword 索引：`optional`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 FIS0，再以 FIS1 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：FIS0, FIS1, FIS254, FIS255, FID

- 來源 keyword 索引：`optional`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.18, Figure 270, 文件頁 276, PDF 頁 302

</details>

<details markdown="1">
<summary><strong>Figure 271: FID Supported and Effects Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-271-CLAIM figure-table:BASEFWLOG-FIG-271 -->

Figure 271〈FID Supported and Effects Data Structure〉：定義〈FID Supported and Effects Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：FSP, RUHS, CDQSCP, NSSCPE, DSCPE, EGSCPE, NSETSCPE, CSCPE。

- 解決的問題：定義〈FID Supported and Effects Data Structure〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：FSP, RUHS, CDQSCP, NSSCPE, DSCPE, EGSCPE, NSETSCPE, CSCPE。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 FSP 作為 parser 的第一個檢查點，再用 RUHS 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：FSP, RUHS, CDQSCP, NSSCPE, DSCPE, EGSCPE, NSETSCPE, CSCPE

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.18, Figure 271, 文件頁 277-278, PDF 頁 303-304

</details>

<details markdown="1">
<summary><strong>Figure 272: NVMe-MI Commands Supported and Effects Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-272-CLAIM figure-table:BASEFWLOG-FIG-272 -->

Figure 272〈NVMe-MI Commands Supported and Effects Log Page〉：定義〈NVMe-MI Commands Supported and Effects Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：MICS0, MICS1, MICS254, MICS255, MI, Command。

- 解決的問題：定義〈NVMe-MI Commands Supported and Effects Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：MICS0, MICS1, MICS254, MICS255, MI, Command。

- 條件與限制：來源 keyword 索引：`optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 MICS0，再以 MICS1 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：MICS0, MICS1, MICS254, MICS255, MI, Command

- 來源 keyword 索引：`optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.19, Figure 272, 文件頁 278, PDF 頁 304

</details>

<details markdown="1">
<summary><strong>Figure 273: NVMe-MI Commands Supported and Effects Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-273-CLAIM figure-table:BASEFWLOG-FIG-273 -->

Figure 273〈NVMe-MI Commands Supported and Effects Data Structure〉：定義〈NVMe-MI Commands Supported and Effects Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CSP, NSSCPE, DSCPE, EGSCPE, NSETSCPE, CSCPE, NSCPE, CCC。

- 解決的問題：定義〈NVMe-MI Commands Supported and Effects Data Structure〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CSP, NSSCPE, DSCPE, EGSCPE, NSETSCPE, CSCPE, NSCPE, CCC。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 CSP 作為 parser 的第一個檢查點，再用 NSSCPE 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：CSP, NSSCPE, DSCPE, EGSCPE, NSETSCPE, CSCPE, NSCPE, CCC

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.19, Figure 273, 文件頁 279, PDF 頁 305

</details>

<details markdown="1">
<summary><strong>Figure 274: Command and Feature Lockdown Log Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-274-CLAIM figure-table:BASEFWLOG-FIG-274 -->

Figure 274〈Command and Feature Lockdown Log Specific Parameter Field〉：定義〈Command and Feature Lockdown Log Specific Parameter Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ELPF, CNTTS, SCP, Command。

- 解決的問題：定義〈Command and Feature Lockdown Log Specific Parameter Field〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：ELPF, CNTTS, SCP, Command。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 ELPF 作為 parser 的第一個檢查點，再用 CNTTS 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：ELPF, CNTTS, SCP, Command

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.20, Figure 274, 文件頁 280, PDF 頁 306

</details>

<details markdown="1">
<summary><strong>Figure 275: Controller Identifier - Log Specific Identifier</strong></summary>

<!-- claim:BASEFWLOG-FIG-275-CLAIM figure-table:BASEFWLOG-FIG-275 -->

Figure 275〈Controller Identifier - Log Specific Identifier〉：定義〈Controller Identifier - Log Specific Identifier〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：CNTLID, ELPF, UUID, Controller, Controller ID。

- 解決的問題：定義〈Controller Identifier - Log Specific Identifier〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：CNTLID, ELPF, UUID, Controller, Controller ID。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：依定義寬度解析 CNTLID，再核對 ELPF 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：CNTLID, ELPF, UUID, Controller, Controller ID

- 來源 keyword 索引：`shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.20, Figure 275, 文件頁 280, PDF 頁 306

</details>

<details markdown="1">
<summary><strong>Figure 276: Command and Feature Lockdown Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-276-CLAIM figure-table:BASEFWLOG-FIG-276 -->

Figure 276〈Command and Feature Lockdown Log Page〉：定義〈Command and Feature Lockdown Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CFILA, CS, SS, LNGTH, CFIL, CFI, Command。

- 解決的問題：定義〈Command and Feature Lockdown Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CFILA, CS, SS, LNGTH, CFIL, CFI, Command。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 CFILA，再以 CS 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：CFILA, CS, SS, LNGTH, CFIL, CFI, Command

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.20, Figure 276, 文件頁 281, PDF 頁 307

</details>

<details markdown="1">
<summary><strong>Figure 277: Command and Feature Lockdown Log Page – Enhanced</strong></summary>

<!-- claim:BASEFWLOG-FIG-277-CLAIM figure-table:BASEFWLOG-FIG-277 -->

Figure 277〈Command and Feature Lockdown Log Page – Enhanced〉：定義〈Command and Feature Lockdown Log Page – Enhanced〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：VER, CFIA, CS, SS, CNTLID, SZE, NCFID, CFIDS。

- 解決的問題：定義〈Command and Feature Lockdown Log Page – Enhanced〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：VER, CFIA, CS, SS, CNTLID, SZE, NCFID, CFIDS。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 VER，再以 CFIA 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：VER, CFIA, CS, SS, CNTLID, SZE, NCFID, CFIDS

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.20, Figure 277, 文件頁 282-283, PDF 頁 308-309

</details>

<details markdown="1">
<summary><strong>Figure 278: Command and Feature Identifier Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-278-CLAIM figure-table:BASEFWLOG-FIG-278 -->

Figure 278〈Command and Feature Identifier Descriptor〉：定義〈Command and Feature Identifier Descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CFI, CFIA, ACNTL, CS, CNTLID, Command。

- 解決的問題：定義〈Command and Feature Identifier Descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CFI, CFIA, ACNTL, CS, CNTLID, Command。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 CFI 作為 parser 的第一個檢查點，再用 CFIA 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：CFI, CFIA, ACNTL, CS, CNTLID, Command

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.20, Figure 278, 文件頁 283, PDF 頁 309

</details>

<details markdown="1">
<summary><strong>Figure 279: Boot Partition Log Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-279-CLAIM figure-table:BASEFWLOG-FIG-279 -->

Figure 279〈Boot Partition Log Specific Parameter Field〉：定義〈Boot Partition Log Specific Parameter Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：BPID。

- 解決的問題：定義〈Boot Partition Log Specific Parameter Field〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：BPID。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 BPID 作為 parser 的第一個檢查點，再用 引用條件 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：BPID

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, Figure 279, 文件頁 283, PDF 頁 309

</details>

<details markdown="1">
<summary><strong>Figure 280: Boot Partition Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-280-CLAIM figure-table:BASEFWLOG-FIG-280 -->

Figure 280〈Boot Partition Log Page〉：定義〈Boot Partition Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LID, BPINFO, ABPID, BPSZ, BPD, ID。

- 解決的問題：定義〈Boot Partition Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LID, BPINFO, ABPID, BPSZ, BPD, ID。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 LID，再以 BPINFO 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：LID, BPINFO, ABPID, BPSZ, BPD, ID

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.21, Figure 280, 文件頁 284, PDF 頁 310

</details>

<details markdown="1">
<summary><strong>Figure 281: Rotational Media Information Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-281-CLAIM figure-table:BASEFWLOG-FIG-281 -->

Figure 281〈Rotational Media Information Log Page〉：定義〈Rotational Media Information Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：ENDGID, NUMA, NRS, SPINC, FSPINC, LDC, FLDC。

- 解決的問題：定義〈Rotational Media Information Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：ENDGID, NUMA, NRS, SPINC, FSPINC, LDC, FLDC。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 ENDGID，再以 NUMA 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：ENDGID, NUMA, NRS, SPINC, FSPINC, LDC, FLDC

- 來源 keyword 索引：`shall not`, `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.22, Figure 281, 文件頁 284-285, PDF 頁 310-311

</details>

<details markdown="1">
<summary><strong>Figure 282: Dispersed Namespace Participating NVM Subsystems Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-282-CLAIM figure-table:BASEFWLOG-FIG-282 -->

Figure 282〈Dispersed Namespace Participating NVM Subsystems Log Page〉：定義〈Dispersed Namespace Participating NVM Subsystems Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：GENCTR, NUMPSUB, NVM Subsystem, Namespace。

- 解決的問題：定義〈Dispersed Namespace Participating NVM Subsystems Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：GENCTR, NUMPSUB, NVM Subsystem, Namespace。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 GENCTR，再以 NUMPSUB 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：GENCTR, NUMPSUB, NVM Subsystem, Namespace

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.23, Figure 282, 文件頁 285-286, PDF 頁 311-312

</details>

<details markdown="1">
<summary><strong>Figure 283: Management Address List – Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-283-CLAIM figure-table:BASEFWLOG-FIG-283 -->

Figure 283〈Management Address List – Log Page〉：定義〈Management Address List – Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：MAD0, MAD1, MAD7。

- 解決的問題：定義〈Management Address List – Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：MAD0, MAD1, MAD7。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 MAD0，再以 MAD1 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：MAD0, MAD1, MAD7

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.24, Figure 283, 文件頁 286, PDF 頁 312

</details>

<details markdown="1">
<summary><strong>Figure 284: Management Address Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-284-CLAIM figure-table:BASEFWLOG-FIG-284 -->

Figure 284〈Management Address Descriptor〉：定義〈Management Address Descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MAT, MADRS, SSD, URI, RFC, UTF。

- 解決的問題：定義〈Management Address Descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：MAT, MADRS, SSD, URI, RFC, UTF。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 MAT 作為 parser 的第一個檢查點，再用 MADRS 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：MAT, MADRS, SSD, URI, RFC, UTF

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.24, Figure 284, 文件頁 286, PDF 頁 312

</details>

<details markdown="1">
<summary><strong>Figure 285: Reachability Groups Log Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-285-CLAIM figure-table:BASEFWLOG-FIG-285 -->

Figure 285〈Reachability Groups Log Specific Parameter Field〉：定義〈Reachability Groups Log Specific Parameter Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：RGO, NSID。

- 解決的問題：定義〈Reachability Groups Log Specific Parameter Field〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：RGO, NSID。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 RGO 作為 parser 的第一個檢查點，再用 NSID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：RGO, NSID

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.25, Figure 285, 文件頁 287, PDF 頁 313

</details>

<details markdown="1">
<summary><strong>Figure 286: Reachability Groups Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-286-CLAIM figure-table:BASEFWLOG-FIG-286 -->

Figure 286〈Reachability Groups Log Page〉：定義〈Reachability Groups Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CHNGC, NRGD, NSID。

- 解決的問題：定義〈Reachability Groups Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CHNGC, NRGD, NSID。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 CHNGC，再以 NRGD 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：CHNGC, NRGD, NSID

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.25, Figure 286, 文件頁 287-288, PDF 頁 313-314

</details>

<details markdown="1">
<summary><strong>Figure 287: Reachability Group Descriptor format</strong></summary>

<!-- claim:BASEFWLOG-FIG-287-CLAIM figure-table:BASEFWLOG-FIG-287 -->

Figure 287〈Reachability Group Descriptor format〉：定義〈Reachability Group Descriptor format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：RGID, NNID, CHNGC, ID, NSID, RGO。

- 解決的問題：定義〈Reachability Group Descriptor format〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：RGID, NNID, CHNGC, ID, NSID, RGO。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 RGID 作為 parser 的第一個檢查點，再用 NNID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：RGID, NNID, CHNGC, ID, NSID, RGO

- 來源 keyword 索引：`shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.25, Figure 287, 文件頁 288, PDF 頁 314

</details>

<details markdown="1">
<summary><strong>Figure 288: Reachability Associations Log Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-288-CLAIM figure-table:BASEFWLOG-FIG-288 -->

Figure 288〈Reachability Associations Log Specific Parameter Field〉：定義〈Reachability Associations Log Specific Parameter Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：RAO, RGID。

- 解決的問題：定義〈Reachability Associations Log Specific Parameter Field〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：RAO, RGID。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 RAO 作為 parser 的第一個檢查點，再用 RGID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：RAO, RGID

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.26, Figure 288, 文件頁 289, PDF 頁 315

</details>

<details markdown="1">
<summary><strong>Figure 289: Reachability Associations Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-289-CLAIM figure-table:BASEFWLOG-FIG-289 -->

Figure 289〈Reachability Associations Log Page〉：定義〈Reachability Associations Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CHNGC, NRAD。

- 解決的問題：定義〈Reachability Associations Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：CHNGC, NRAD。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 CHNGC，再以 NRAD 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：CHNGC, NRAD

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.26, Figure 289, 文件頁 289, PDF 頁 315

</details>

<details markdown="1">
<summary><strong>Figure 290: Reachability Association Descriptor format</strong></summary>

<!-- claim:BASEFWLOG-FIG-290-CLAIM figure-table:BASEFWLOG-FIG-290 -->

Figure 290〈Reachability Association Descriptor format〉：定義〈Reachability Association Descriptor format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：RASID, NRID, CHNGC, RAC, ID, RGID, RAO。

- 解決的問題：定義〈Reachability Association Descriptor format〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：RASID, NRID, CHNGC, RAC, ID, RGID, RAO。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 RASID 作為 parser 的第一個檢查點，再用 NRID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：RASID, NRID, CHNGC, RAC, ID, RGID, RAO

- 來源 keyword 索引：`shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.26, Figure 290, 文件頁 290, PDF 頁 316

</details>

<details markdown="1">
<summary><strong>Figure 291: Device Personalities Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-291-CLAIM figure-table:BASEFWLOG-FIG-291 -->

Figure 291〈Device Personalities Log Page〉：定義〈Device Personalities Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：NUMP, CDPLPV, DPLPHL, CDPLPS, CDP, PPS。

- 解決的問題：定義〈Device Personalities Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：NUMP, CDPLPV, DPLPHL, CDPLPS, CDP, PPS。

- 條件與限制：來源 keyword 索引：`shall`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 NUMP，再以 CDPLPV 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：NUMP, CDPLPV, DPLPHL, CDPLPS, CDP, PPS

- 來源 keyword 索引：`shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.28, Figure 291, 文件頁 291, PDF 頁 317

</details>

<details markdown="1">
<summary><strong>Figure 292: Personality Properties Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-292-CLAIM figure-table:BASEFWLOG-FIG-292 -->

Figure 292〈Personality Properties Data Structure〉：定義〈Personality Properties Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PPS, PERID, MRSTT, AUS, PKAS, PCAS, PSCUDE, CDP。

- 解決的問題：定義〈Personality Properties Data Structure〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PPS, PERID, MRSTT, AUS, PKAS, PCAS, PSCUDE, CDP。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 PPS 作為 parser 的第一個檢查點，再用 PERID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：PPS, PERID, MRSTT, AUS, PKAS, PCAS, PSCUDE, CDP

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.28, Figure 292, 文件頁 291-293, PDF 頁 317-319

</details>

<details markdown="1">
<summary><strong>Figure 293: FDP Configurations Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-293-CLAIM figure-table:BASEFWLOG-FIG-293 -->

Figure 293〈FDP Configurations Log Page〉：定義〈FDP Configurations Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：VER, SZE, FDP, UMFDPC。

- 解決的問題：定義〈FDP Configurations Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：VER, SZE, FDP, UMFDPC。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 VER，再以 SZE 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：VER, SZE, FDP, UMFDPC

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.29, Figure 293, 文件頁 293, PDF 頁 319

</details>

<details markdown="1">
<summary><strong>Figure 294: FDP Configuration Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-294-CLAIM figure-table:BASEFWLOG-FIG-294 -->

Figure 294〈FDP Configuration Descriptor〉：定義〈FDP Configuration Descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DSZE, FDPA, FDPCV, FDPVWC, RGIF, VSS, NRG, NRUH。

- 解決的問題：定義〈FDP Configuration Descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DSZE, FDPA, FDPCV, FDPVWC, RGIF, VSS, NRG, NRUH。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 DSZE 作為 parser 的第一個檢查點，再用 FDPA 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：DSZE, FDPA, FDPCV, FDPVWC, RGIF, VSS, NRG, NRUH

- 來源 keyword 索引：`shall`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.29, Figure 294, 文件頁 293-295, PDF 頁 319-321

</details>

<details markdown="1">
<summary><strong>Figure 295: Reclaim Unit Handle Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-295-CLAIM figure-table:BASEFWLOG-FIG-295 -->

Figure 295〈Reclaim Unit Handle Descriptor〉：定義〈Reclaim Unit Handle Descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：RUHT, FDP, NRG, RGIF, Reclaim Unit。

- 解決的問題：定義〈Reclaim Unit Handle Descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：RUHT, FDP, NRG, RGIF, Reclaim Unit。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 RUHT 作為 parser 的第一個檢查點，再用 FDP 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：RUHT, FDP, NRG, RGIF, Reclaim Unit

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.29, Figure 295, 文件頁 295, PDF 頁 321

</details>

<details markdown="1">
<summary><strong>Figure 296: Placement Identifier Format without Reclaim Group Identifier</strong></summary>

<!-- claim:BASEFWLOG-FIG-296-CLAIM figure-table:BASEFWLOG-FIG-296 -->

Figure 296〈Placement Identifier Format without Reclaim Group Identifier〉：定義〈Placement Identifier Format without Reclaim Group Identifier〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PHNDL, Reclaim Group。

- 解決的問題：定義〈Placement Identifier Format without Reclaim Group Identifier〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PHNDL, Reclaim Group。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。

- 說明性範例（informative example）：以 PHNDL 作為 parser 的第一個檢查點，再用 Reclaim Group 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：PHNDL, Reclaim Group

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.29, Figure 296, 文件頁 295, PDF 頁 321

</details>

<details markdown="1">
<summary><strong>Figure 297: Placement Identifier Format with a non-zero RGIF</strong></summary>

<!-- claim:BASEFWLOG-FIG-297-CLAIM figure-table:BASEFWLOG-FIG-297 -->

Figure 297〈Placement Identifier Format with a non-zero RGIF〉：定義〈Placement Identifier Format with a non-zero RGIF〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：RGID, PHNDL, RGIF, NRG。

- 解決的問題：定義〈Placement Identifier Format with a non-zero RGIF〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：RGID, PHNDL, RGIF, NRG。

- 條件與限制：來源 keyword 索引：`shall`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 RGID 作為 parser 的第一個檢查點，再用 PHNDL 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：RGID, PHNDL, RGIF, NRG

- 來源 keyword 索引：`shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.29, Figure 297, 文件頁 296, PDF 頁 322

</details>

<details markdown="1">
<summary><strong>Figure 298: Reclaim Unit Handle Usage Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-298-CLAIM figure-table:BASEFWLOG-FIG-298 -->

Figure 298〈Reclaim Unit Handle Usage Log Page〉：定義〈Reclaim Unit Handle Usage Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：NRUH, FDP, Reclaim Unit。

- 解決的問題：定義〈Reclaim Unit Handle Usage Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：NRUH, FDP, Reclaim Unit。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 NRUH，再以 FDP 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：NRUH, FDP, Reclaim Unit

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.30, Figure 298, 文件頁 296, PDF 頁 322

</details>

<details markdown="1">
<summary><strong>Figure 299: Reclaim Unit Handle Usage Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-299-CLAIM figure-table:BASEFWLOG-FIG-299 -->

Figure 299〈Reclaim Unit Handle Usage Descriptor〉：定義〈Reclaim Unit Handle Usage Descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：RUHA, Reclaim Unit。

- 解決的問題：定義〈Reclaim Unit Handle Usage Descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：RUHA, Reclaim Unit。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 RUHA 作為 parser 的第一個檢查點，再用 Reclaim Unit 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：RUHA, Reclaim Unit

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.30, Figure 299, 文件頁 296-297, PDF 頁 322-323

</details>

<details markdown="1">
<summary><strong>Figure 300: FDP Statistics Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-300-CLAIM figure-table:BASEFWLOG-FIG-300 -->

Figure 300〈FDP Statistics Log Page〉：定義〈FDP Statistics Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：HBMW, MBMW, MBE, FDP。

- 解決的問題：定義〈FDP Statistics Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：HBMW, MBMW, MBE, FDP。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 HBMW，再以 MBMW 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：HBMW, MBMW, MBE, FDP

- 來源 keyword 索引：`shall not`, `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.31, Figure 300, 文件頁 297, PDF 頁 323

</details>

<details markdown="1">
<summary><strong>Figure 301: Command Dword 10 – Log Specific Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-301-CLAIM figure-table:BASEFWLOG-FIG-301 -->

Figure 301〈Command Dword 10 – Log Specific Field〉：定義〈Command Dword 10 – Log Specific Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：FDPET, FDP, Command。

- 解決的問題：定義〈Command Dword 10 – Log Specific Field〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：FDPET, FDP, Command。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 FDPET 作為 parser 的第一個檢查點，再用 FDP 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：FDPET, FDP, Command

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.32, Figure 301, 文件頁 298, PDF 頁 324

</details>

<details markdown="1">
<summary><strong>Figure 302: FDP Events Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-302-CLAIM figure-table:BASEFWLOG-FIG-302 -->

Figure 302〈FDP Events Log Page〉：定義〈FDP Events Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：NUMFDPE, FDP, NUMFDPC。

- 解決的問題：定義〈FDP Events Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：NUMFDPE, FDP, NUMFDPC。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 NUMFDPE，再以 FDP 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：NUMFDPE, FDP, NUMFDPC

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.32, Figure 302, 文件頁 298, PDF 頁 324

</details>

<details markdown="1">
<summary><strong>Figure 303: FDP Event</strong></summary>

<!-- claim:BASEFWLOG-FIG-303-CLAIM figure-table:BASEFWLOG-FIG-303 -->

Figure 303〈FDP Event〉：定義〈FDP Event〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：ETYP, FDPEF, LV, NSIDV, PIV, PID, ETMSP, NSID。

- 解決的問題：定義〈FDP Event〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：ETYP, FDPEF, LV, NSIDV, PIV, PID, ETMSP, NSID。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `may`, `optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先辨認 ETYP，以 FDPEF 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：ETYP, FDPEF, LV, NSIDV, PIV, PID, ETMSP, NSID

- 來源 keyword 索引：`shall`, `should`, `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.32, Figure 303, 文件頁 299-300, PDF 頁 325-326

</details>

<details markdown="1">
<summary><strong>Figure 304: Manufacturer Default Configuration Status Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-304-CLAIM figure-table:BASEFWLOG-FIG-304 -->

Figure 304〈Manufacturer Default Configuration Status Log Page〉：定義〈Manufacturer Default Configuration Status Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：MDCSV, MDCS, DCCS, DNCS, DSCS, RDCCS, RDNCS, RDSCS。

- 解決的問題：定義〈Manufacturer Default Configuration Status Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：MDCSV, MDCS, DCCS, DNCS, DSCS, RDCCS, RDNCS, RDSCS。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 MDCSV，再以 MDCS 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：MDCSV, MDCS, DCCS, DNCS, DSCS, RDCCS, RDNCS, RDSCS

- 來源 keyword 索引：`shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.33, Figure 304, 文件頁 301-302, PDF 頁 327-328

</details>

<details markdown="1">
<summary><strong>Figure 305: Power Measurement Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-305-CLAIM figure-table:BASEFWLOG-FIG-305 -->

Figure 305〈Power Measurement Log Page〉：定義〈Power Measurement Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：VER, PMGN, PMA, PMT, PHDO, MIPWRTS, EPF, NCPDF。

- 解決的問題：定義〈Power Measurement Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：VER, PMGN, PMA, PMT, PHDO, MIPWRTS, EPF, NCPDF。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `should`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 VER，再以 PMGN 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：VER, PMGN, PMA, PMT, PHDO, MIPWRTS, EPF, NCPDF

- 來源 keyword 索引：`shall not`, `shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.34, Figure 305, 文件頁 303-306, PDF 頁 329-332

</details>

<details markdown="1">
<summary><strong>Figure 306: Power Histogram Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-306-CLAIM figure-table:BASEFWLOG-FIG-306 -->

Figure 306〈Power Histogram Descriptor〉：定義〈Power Histogram Descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PHBC, PHBLT, PWRS, PWRV, PMT, PHBS, PMC。

- 解決的問題：定義〈Power Histogram Descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PHBC, PHBLT, PWRS, PWRV, PMT, PHBS, PMC。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 PHBC 作為 parser 的第一個檢查點，再用 PHBLT 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：PHBC, PHBLT, PWRS, PWRV, PMT, PHBS, PMC

- 來源 keyword 索引：`shall not`, `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.34, Figure 306, 文件頁 306, PDF 頁 332

</details>

<details markdown="1">
<summary><strong>Figure 307: Voltage Measurement Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-307-CLAIM figure-table:BASEFWLOG-FIG-307 -->

Figure 307〈Voltage Measurement Log Page〉：定義〈Voltage Measurement Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：VMGN, VMA, VMC, VSM, IVOLTS, VME, VSI, VSSS。

- 解決的問題：定義〈Voltage Measurement Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：VMGN, VMA, VMC, VSM, IVOLTS, VME, VSI, VSSS。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `should`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 VMGN，再以 VMA 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：VMGN, VMA, VMC, VSM, IVOLTS, VME, VSI, VSSS

- 來源 keyword 索引：`shall not`, `shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.35, Figure 307, 文件頁 307-311, PDF 頁 333-337

</details>

<details markdown="1">
<summary><strong>Figure 308: Interval Voltage Measurement Descriptor</strong></summary>

<!-- claim:BASEFWLOG-FIG-308-CLAIM figure-table:BASEFWLOG-FIG-308 -->

Figure 308〈Interval Voltage Measurement Descriptor〉：定義〈Interval Voltage Measurement Descriptor〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：IVOLM, NCVM, VOLV, VME, VOLSS。

- 解決的問題：定義〈Interval Voltage Measurement Descriptor〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：IVOLM, NCVM, VOLV, VME, VOLSS。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 IVOLM 作為 parser 的第一個檢查點，再用 NCVM 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：IVOLM, NCVM, VOLV, VME, VOLSS

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.35, Figure 308, 文件頁 311, PDF 頁 337

</details>

<details markdown="1">
<summary><strong>Figure 309: Sanitize Namespace Status List Log Specific Parameter Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-309-CLAIM figure-table:BASEFWLOG-FIG-309 -->

Figure 309〈Sanitize Namespace Status List Log Specific Parameter Field〉：定義〈Sanitize Namespace Status List Log Specific Parameter Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NLT, NSID, CSTS.RDY, Namespace。

- 解決的問題：定義〈Sanitize Namespace Status List Log Specific Parameter Field〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NLT, NSID, CSTS.RDY, Namespace。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：以 NLT 作為 parser 的第一個檢查點，再用 NSID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：NLT, NSID, CSTS.RDY, Namespace

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.36, Figure 309, 文件頁 311-312, PDF 頁 337-338

</details>

<details markdown="1">
<summary><strong>Figure 310: Sanitize Namespace Status List Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-310-CLAIM figure-table:BASEFWLOG-FIG-310 -->

Figure 310〈Sanitize Namespace Status List Log Page〉：定義〈Sanitize Namespace Status List Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：GENCTR, NUMNSID, NSID, Namespace。

- 解決的問題：定義〈Sanitize Namespace Status List Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：GENCTR, NUMNSID, NSID, Namespace。

- 條件與限制：來源 keyword 索引：`shall`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 GENCTR，再以 NUMNSID 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：GENCTR, NUMNSID, NSID, Namespace

- 來源 keyword 索引：`shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.36, Figure 310, 文件頁 312, PDF 頁 338

</details>

<details markdown="1">
<summary><strong>Figure 311: Reservation Notification Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-311-CLAIM figure-table:BASEFWLOG-FIG-311 -->

Figure 311〈Reservation Notification Log Page〉：定義〈Reservation Notification Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LPC, RNLPT, NALP, NSID, ID。

- 解決的問題：定義〈Reservation Notification Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：LPC, RNLPT, NALP, NSID, ID。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 LPC，再以 RNLPT 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：LPC, RNLPT, NALP, NSID, ID

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.37, Figure 311, 文件頁 313, PDF 頁 339

</details>

<details markdown="1">
<summary><strong>Figure 312: Sanitize Status Log Page</strong></summary>

<!-- claim:BASEFWLOG-FIG-312-CLAIM figure-table:BASEFWLOG-FIG-312 -->

Figure 312〈Sanitize Status Log Page〉：定義〈Sanitize Status Log Page〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：SPROG, OPC, SOS, SCDW10, ETO, ETBE, ETCE, ETODMM。

- 解決的問題：定義〈Sanitize Status Log Page〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：SPROG, OPC, SOS, SCDW10, ETO, ETBE, ETCE, ETODMM。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 SPROG，再以 OPC 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：SPROG, OPC, SOS, SCDW10, ETO, ETBE, ETCE, ETODMM

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, Figure 312, 文件頁 314-319, PDF 頁 340-345

</details>

<details markdown="1">
<summary><strong>Figure 331: Get Log Page – Command Specific Status Values</strong></summary>

<!-- claim:BASEFWLOG-FIG-331-CLAIM figure-table:BASEFWLOG-FIG-331 -->

Figure 331〈Get Log Page – Command Specific Status Values〉：定義〈Get Log Page – Command Specific Status Values〉的回傳配置與 selector／scope 上下文。 先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：Invalid Log Page, Invalid Controller Identifier, I/O Command Set Not Supported。

- 解決的問題：定義〈Get Log Page – Command Specific Status Values〉的回傳配置與 selector／scope 上下文。

- 閱讀順序：先讀固定 header 與 scope，驗證 count／length 後，再依序走訪 entry 或 data area；來源欄位索引：Invalid Log Page, Invalid Controller Identifier, I/O Command Set Not Supported。

- 條件與限制：來源 keyword 索引：`may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。

- 說明性範例（informative example）：先讀 Invalid Log Page，再以 Invalid Controller Identifier 作為獨立的大小或 identity 檢查點，且不得解析超過實際回傳的 byte。 此例不新增規格要求。

- 來源欄位索引：Invalid Log Page, Invalid Controller Identifier, I/O Command Set Not Supported

- 來源 keyword 索引：`may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.3.6, Figure 331, 文件頁 336, PDF 頁 362

</details>

<a id="section-dependency"></a>

### 引用相依 Figure（位於主章節範圍外）

<details markdown="1">
<summary><strong>Figure 70: Flexible Data Placement Logical View of Non-Volatile Storage</strong></summary>

<!-- claim:BASEFWLOG-FIG-070-CLAIM figure-table:BASEFWLOG-FIG-070 -->

Figure 70〈Flexible Data Placement Logical View of Non-Volatile Storage〉：呈現〈Flexible Data Placement Logical View of Non-Volatile Storage〉中的物件或容量關係。 將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：Endurance Group, Reclaim Group, Reclaim Unit, Reclaim Unit Handle。

- 解決的問題：呈現〈Flexible Data Placement Logical View of Non-Volatile Storage〉中的物件或容量關係。

- 閱讀順序：將邏輯 identifier、controller、namespace、port 與容量容器分開；來源索引：Endurance Group, Reclaim Group, Reclaim Unit, Reclaim Unit Handle。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。 這是 §5.2.13.1.29, §5.2.13.1.30 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：選擇 Endurance Group 標示的一個物件，再追到 Reclaim Group，過程中不把 identifier 當成物件本身。 此例不新增規格要求。

- 來源欄位索引：Endurance Group, Reclaim Group, Reclaim Unit, Reclaim Unit Handle

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.2.4, Figure 70, 文件頁 85, PDF 頁 111

</details>

<details markdown="1">
<summary><strong>Figure 84: Admin Commands Permitted to Return a Status Code of Admin Command Media Not Ready</strong></summary>

<!-- claim:BASEFWLOG-FIG-084-CLAIM figure-table:BASEFWLOG-FIG-084 -->

Figure 84〈Admin Commands Permitted to Return a Status Code of Admin Command Media Not Ready〉：定義〈Admin Commands Permitted to Return a Status Code of Admin Command Media Not Ready〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：LBA, CAP.CRMS, CAP.CRMS.CRWMS, CAP.CRMS.CRIMS, CC.CRIME, Status Code, Command。

- 解決的問題：定義〈Admin Commands Permitted to Return a Status Code of Admin Command Media Not Ready〉所表示的 status／error 分類。

- 閱讀順序：先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：LBA, CAP.CRMS, CAP.CRMS.CRWMS, CAP.CRMS.CRIMS, CC.CRIME, Status Code, Command。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.13.1.3 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：收到一筆狀態時先辨認 LBA，再檢查 CAP.CRMS，不可脫離類別單看數值。 此例不新增規格要求。

- 來源欄位索引：LBA, CAP.CRMS, CAP.CRMS.CRWMS, CAP.CRMS.CRIMS, CC.CRIME, Status Code, Command

- 來源 keyword 索引：`shall`, `should`, `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §3.5.3, Figure 84, 文件頁 110-111, PDF 頁 136-137

</details>

<details markdown="1">
<summary><strong>Figure 93: Common Command Format</strong></summary>

<!-- claim:BASEFWLOG-FIG-093-CLAIM figure-table:BASEFWLOG-FIG-093 -->

Figure 93〈Common Command Format〉：定義〈Common Command Format〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CDW0, NSID, CDW2, CDW3, MPTR, DPTR, PRP2, PRP1。

- 解決的問題：定義〈Common Command Format〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：CDW0, NSID, CDW2, CDW3, MPTR, DPTR, PRP2, PRP1。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.10, §5.2.13 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：以 CDW0 作為 parser 的第一個檢查點，再用 NSID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：CDW0, NSID, CDW2, CDW3, MPTR, DPTR, PRP2, PRP1

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, 文件頁 140-142, PDF 頁 166-168

</details>

<details markdown="1">
<summary><strong>Figure 101: Completion Queue Entry: Status Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-101-CLAIM figure-table:BASEFWLOG-FIG-101 -->

Figure 101〈Completion Queue Entry: Status Field〉：定義〈Completion Queue Entry: Status Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DNR, CRD, SCT, SC, ACRE, CRDT1, CRDT2, CRDT3。

- 解決的問題：定義〈Completion Queue Entry: Status Field〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：DNR, CRD, SCT, SC, ACRE, CRDT1, CRDT2, CRDT3。

- 條件與限制：來源 keyword 索引：`should not`, `should`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.13.1.2, §5.2.13.1.14 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：以 DNR 作為 parser 的第一個檢查點，再用 CRD 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：DNR, CRD, SCT, SC, ACRE, CRDT1, CRDT2, CRDT3

- 來源 keyword 索引：`should not`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 101, 文件頁 145-146, PDF 頁 171-172

</details>

<details markdown="1">
<summary><strong>Figure 102: Status Code – Status Code Type Values</strong></summary>

<!-- claim:BASEFWLOG-FIG-102-CLAIM figure-table:BASEFWLOG-FIG-102 -->

Figure 102〈Status Code – Status Code Type Values〉：定義〈Status Code – Status Code Type Values〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：SC, Status Code。

- 解決的問題：定義〈Status Code – Status Code Type Values〉所表示的 status／error 分類。

- 閱讀順序：先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：SC, Status Code。

- 條件與限制：來源 keyword 索引：`shall`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.13.1.14 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：收到一筆狀態時先辨認 SC，再檢查 Status Code，不可脫離類別單看數值。 此例不新增規格要求。

- 來源欄位索引：SC, Status Code

- 來源 keyword 索引：`shall`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 102, 文件頁 146, PDF 頁 172

</details>

<details markdown="1">
<summary><strong>Figure 107: Status Code – Media and Data Integrity Error Values</strong></summary>

<!-- claim:BASEFWLOG-FIG-107-CLAIM figure-table:BASEFWLOG-FIG-107 -->

Figure 107〈Status Code – Media and Data Integrity Error Values〉：定義〈Status Code – Media and Data Integrity Error Values〉所表示的 status／error 分類。 先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：TCG, SCT, Status Code。

- 解決的問題：定義〈Status Code – Media and Data Integrity Error Values〉所表示的 status／error 分類。

- 閱讀順序：先判斷類別，再解個別 code 或 flag；保留值不自行賦義。來源欄位索引：TCG, SCT, Status Code。

- 條件與限制：來源 keyword 索引：`should`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.13.1.14.2.5 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：收到一筆狀態時先辨認 TCG，再檢查 SCT，不可脫離類別單看數值。 此例不新增規格要求。

- 來源欄位索引：TCG, SCT, Status Code

- 來源 keyword 索引：`should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 107, 文件頁 154-155, PDF 頁 180-181

</details>

<details markdown="1">
<summary><strong>Figure 155: Asynchronous Event Information – Notice</strong></summary>

<!-- claim:BASEFWLOG-FIG-155-CLAIM figure-table:BASEFWLOG-FIG-155 -->

Figure 155〈Asynchronous Event Information – Notice〉：定義〈Asynchronous Event Information – Notice〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：Firmware Activation Starting, CSTS.PP, Firmware Slot Information, RAE。

- 解決的問題：定義〈Asynchronous Event Information – Notice〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：Firmware Activation Starting, CSTS.PP, Firmware Slot Information, RAE。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `may`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §3.11, §5.2.30.1.6 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。 只取 firmware activation notice、CSTS.PP 與以 Firmware Slot Information log 清除事件的關係。

- 說明性範例（informative example）：先辨認 Firmware Activation Starting，以 CSTS.PP 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：Firmware Activation Starting, CSTS.PP, Firmware Slot Information, RAE

- 來源 keyword 索引：`shall not`, `shall`, `may`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 155, 文件頁 186, PDF 頁 212

</details>

<details markdown="1">
<summary><strong>Figure 195: Format NVM – Command Dword 10</strong></summary>

<!-- claim:BASEFWLOG-FIG-195-CLAIM figure-table:BASEFWLOG-FIG-195 -->

Figure 195〈Format NVM – Command Dword 10〉：定義〈Format NVM – Command Dword 10〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：LBAFU, SES, PIL, PI, MSET, LBA, LBAFEE, NOTE。

- 解決的問題：定義〈Format NVM – Command Dword 10〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：LBAFU, SES, PIL, PI, MSET, LBA, LBAFEE, NOTE。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.13.1.14.2.7 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：以 LBAFU 作為 parser 的第一個檢查點，再用 SES 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：LBAFU, SES, PIL, PI, MSET, LBA, LBAFEE, NOTE

- 來源 keyword 索引：`shall`, `should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.11, Figure 195, 文件頁 208, PDF 頁 234

</details>

<details markdown="1">
<summary><strong>Figure 337: Command Set Identifiers</strong></summary>

<!-- claim:BASEFWLOG-FIG-337-CLAIM figure-table:BASEFWLOG-FIG-337 -->

Figure 337〈Command Set Identifiers〉：定義〈Command Set Identifiers〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：Command Set, Command。

- 解決的問題：定義〈Command Set Identifiers〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：Command Set, Command。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.9, §5.2.13 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。 §5.2.9 的正文指向 Figure 337，但 Figure 337 實際列的是 Command Set Identifier；firmware 欄位位於 Figure 338。

- 說明性範例（informative example）：依定義寬度解析 Command Set，再核對 Command 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：Command Set, Command

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, Figure 337, 文件頁 340, PDF 頁 366

</details>

<details markdown="1">
<summary><strong>Figure 338: Identify – Identify Controller Data Structure, I/O Command Set Independent</strong></summary>

<!-- claim:BASEFWLOG-FIG-338-CLAIM figure-table:BASEFWLOG-FIG-338 -->

Figure 338〈Identify – Identify Controller Data Structure, I/O Command Set Independent〉：定義〈Identify – Identify Controller Data Structure, I/O Command Set Independent〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：VID, SSVID, SN, MN, FR, FRMW, SMUD, FAWR。

- 解決的問題：定義〈Identify – Identify Controller Data Structure, I/O Command Set Independent〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：VID, SSVID, SN, MN, FR, FRMW, SMUD, FAWR。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `may`, `optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §3.11, §5.2.9, §5.2.10, §5.2.13 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。 只取 firmware update 需要的 FR、FRMW／SMUD／FAWR、MTFA 與 FWUG；其餘 Identify Controller 欄位不展開。

- 說明性範例（informative example）：以 VID 作為 parser 的第一個檢查點，再用 SSVID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：VID, SSVID, SN, MN, FR, FRMW, SMUD, FAWR

- 來源 keyword 索引：`shall`, `should`, `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, 文件頁 340-359, PDF 頁 366-385

</details>

<details markdown="1">
<summary><strong>Figure 339: Identify – Voltage Sensor Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-339-CLAIM figure-table:BASEFWLOG-FIG-339 -->

Figure 339〈Identify – Voltage Sensor Data Structure〉：定義〈Identify – Voltage Sensor Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：IVMSR, VSRS, VSRV, VOLSS, PIT, PISL, PISV, VSEN1。

- 解決的問題：定義〈Identify – Voltage Sensor Data Structure〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：IVMSR, VSRS, VSRV, VOLSS, PIT, PISL, PISV, VSEN1。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.13.1.35 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：以 IVMSR 作為 parser 的第一個檢查點，再用 VSRS 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：IVMSR, VSRS, VSRV, VOLSS, PIT, PISL, PISV, VSEN1

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 339, 文件頁 383, PDF 頁 409

</details>

<details markdown="1">
<summary><strong>Figure 346: Identify – I/O Command Set Independent Identify Namespace Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-346-CLAIM figure-table:BASEFWLOG-FIG-346 -->

Figure 346〈Identify – I/O Command Set Independent Identify Namespace Data Structure〉：定義〈Identify – I/O Command Set Independent Identify Namespace Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NSFEAT, VWCNP, RMEDIA, UIDREUSE, NMIC, DISNS, SHRNS, RESCAP。

- 解決的問題：定義〈Identify – I/O Command Set Independent Identify Namespace Data Structure〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：NSFEAT, VWCNP, RMEDIA, UIDREUSE, NMIC, DISNS, SHRNS, RESCAP。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `may`, `optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.13.1.14.2.6 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：以 NSFEAT 作為 parser 的第一個檢查點，再用 VWCNP 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：NSFEAT, VWCNP, RMEDIA, UIDREUSE, NMIC, DISNS, SHRNS, RESCAP

- 來源 keyword 索引：`shall`, `should`, `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.8, Figure 346, 文件頁 391-394, PDF 頁 417-420

</details>

<details markdown="1">
<summary><strong>Figure 347: UUID List</strong></summary>

<!-- claim:BASEFWLOG-FIG-347-CLAIM figure-table:BASEFWLOG-FIG-347 -->

Figure 347〈UUID List〉：定義〈UUID List〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：UUID1, UUID2, UUID126, UUID127, UUID。

- 解決的問題：定義〈UUID List〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：UUID1, UUID2, UUID126, UUID127, UUID。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §3.11.1 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。 用於 §3.11.1 的 UUID list slot 穩定性與不得縮短清單的規則。

- 說明性範例（informative example）：依定義寬度解析 UUID1，再核對 UUID2 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：UUID1, UUID2, UUID126, UUID127, UUID

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.14, Figure 347, 文件頁 396, PDF 頁 422

</details>

<details markdown="1">
<summary><strong>Figure 348: UUID List Entry</strong></summary>

<!-- claim:BASEFWLOG-FIG-348-CLAIM figure-table:BASEFWLOG-FIG-348 -->

Figure 348〈UUID List Entry〉：定義〈UUID List Entry〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：ULEH, IDASSOC, UUID, ID, RFC。

- 解決的問題：定義〈UUID List Entry〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：ULEH, IDASSOC, UUID, ID, RFC。

- 條件與限制：來源 keyword 索引：`reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §3.11.1 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。 用於判斷 UUID list entry 是空值、NVMe Invalid UUID 或有效 UUID。

- 說明性範例（informative example）：依定義寬度解析 ULEH，再核對 IDASSOC 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：ULEH, IDASSOC, UUID, ID, RFC

- 來源 keyword 索引：`reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.14, Figure 348, 文件頁 396, PDF 頁 422

</details>

<details markdown="1">
<summary><strong>Figure 448: Namespace Management – Data Structure for Create</strong></summary>

<!-- claim:BASEFWLOG-FIG-448-CLAIM figure-table:BASEFWLOG-FIG-448 -->

Figure 448〈Namespace Management – Data Structure for Create〉：定義〈Namespace Management – Data Structure for Create〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：SIOCS, VS, RDNCS, CSS, DNCS, Namespace。

- 解決的問題：定義〈Namespace Management – Data Structure for Create〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：SIOCS, VS, RDNCS, CSS, DNCS, Namespace。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.13.1.14.2.6 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：以 SIOCS 作為 parser 的第一個檢查點，再用 VS 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：SIOCS, VS, RDNCS, CSS, DNCS, Namespace

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 448, 文件頁 447, PDF 頁 473

</details>

<details markdown="1">
<summary><strong>Figure 451: Sanitize – Command Dword 10</strong></summary>

<!-- claim:BASEFWLOG-FIG-451-CLAIM figure-table:BASEFWLOG-FIG-451 -->

Figure 451〈Sanitize – Command Dword 10〉：定義〈Sanitize – Command Dword 10〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PREQ, EMVS, NDAS, OIPBP, OWPASS, AUSE, SANACT, IEEE。

- 解決的問題：定義〈Sanitize – Command Dword 10〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：PREQ, EMVS, NDAS, OIPBP, OWPASS, AUSE, SANACT, IEEE。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `should`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.13.1.14.2.9, §5.2.13.1.38 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：以 PREQ 作為 parser 的第一個檢查點，再用 EMVS 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：PREQ, EMVS, NDAS, OIPBP, OWPASS, AUSE, SANACT, IEEE

- 來源 keyword 索引：`shall not`, `shall`, `should`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 451, 文件頁 450-451, PDF 頁 476-477

</details>

<details markdown="1">
<summary><strong>Figure 452: Sanitize – Command Dword 11</strong></summary>

<!-- claim:BASEFWLOG-FIG-452-CLAIM figure-table:BASEFWLOG-FIG-452 -->

Figure 452〈Sanitize – Command Dword 11〉：定義〈Sanitize – Command Dword 11〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：OVRPAT, SCT, Command。

- 解決的問題：定義〈Sanitize – Command Dword 11〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：OVRPAT, SCT, Command。

- 條件與限制：來源 keyword 索引：`shall`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.13.1.14.2.9, §5.2.13.1.38 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：以 OVRPAT 作為 parser 的第一個檢查點，再用 SCT 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：OVRPAT, SCT, Command

- 來源 keyword 索引：`shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 452, 文件頁 451, PDF 頁 477

</details>

<details markdown="1">
<summary><strong>Figure 466: Set Features – Feature Identifiers</strong></summary>

<!-- claim:BASEFWLOG-FIG-466-CLAIM figure-table:BASEFWLOG-FIG-466 -->

Figure 466〈Set Features – Feature Identifiers〉：定義〈Set Features – Feature Identifiers〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：ID, MR, UUID。

- 解決的問題：定義〈Set Features – Feature Identifiers〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：ID, MR, UUID。

- 條件與限制：來源 keyword 索引：`shall`, `should`, `may`, `optional`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.13.1.18 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：依定義寬度解析 ID，再核對 MR 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：ID, MR, UUID

- 來源 keyword 索引：`shall`, `should`, `may`, `optional`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 466, 文件頁 457-459, PDF 頁 483-485

</details>

<details markdown="1">
<summary><strong>Figure 474: Asynchronous Event Configuration – Command Dword 11</strong></summary>

<!-- claim:BASEFWLOG-FIG-474-CLAIM figure-table:BASEFWLOG-FIG-474 -->

Figure 474〈Asynchronous Event Configuration – Command Dword 11〉：定義〈Asynchronous Event Configuration – Command Dword 11〉所表示的 event record、event 分類或記錄條件。 先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：ZDCN, RLCCN, ANSAN, RGRP0, RASSN, TTHRY, NNSSHDN, EGEALCN。

- 解決的問題：定義〈Asynchronous Event Configuration – Command Dword 11〉所表示的 event record、event 分類或記錄條件。

- 閱讀順序：先判斷 Event Type 與 record length，再解 event-specific data；來源欄位索引：ZDCN, RLCCN, ANSAN, RGRP0, RASSN, TTHRY, NNSSHDN, EGEALCN。

- 條件與限制：來源 keyword 索引：`shall not`, `shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §3.11 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。 只取 Firmware Activation Notices enable bit，對應 §3.11 的 activation-starting event。

- 說明性範例（informative example）：先辨認 ZDCN，以 RLCCN 驗證 record 邊界，再只解析該 Event Type 定義的資料。 此例不新增規格要求。

- 來源欄位索引：ZDCN, RLCCN, ANSAN, RGRP0, RASSN, TTHRY, NNSSHDN, EGEALCN

- 來源 keyword 索引：`shall not`, `shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.6, Figure 474, 文件頁 466-468, PDF 頁 492-494

</details>

<details markdown="1">
<summary><strong>Figure 480: Timestamp – Data Structure for Get Features</strong></summary>

<!-- claim:BASEFWLOG-FIG-480-CLAIM figure-table:BASEFWLOG-FIG-480 -->

Figure 480〈Timestamp – Data Structure for Get Features〉：定義〈Timestamp – Data Structure for Get Features〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TSTMP, TSTMPS, TSTMPO, SYNC。

- 解決的問題：定義〈Timestamp – Data Structure for Get Features〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：TSTMP, TSTMPS, TSTMPO, SYNC。

- 條件與限制：來源 keyword 索引：`should`, `may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.13.1.14 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：以 TSTMP 作為 parser 的第一個檢查點，再用 TSTMPS 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：TSTMP, TSTMPS, TSTMPO, SYNC

- 來源 keyword 索引：`should`, `may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.8, Figure 480, 文件頁 470-471, PDF 頁 496-497

</details>

<details markdown="1">
<summary><strong>Figure 512: Personality Identifier List</strong></summary>

<!-- claim:BASEFWLOG-FIG-512-CLAIM figure-table:BASEFWLOG-FIG-512 -->

Figure 512〈Personality Identifier List〉：定義〈Personality Identifier List〉的識別碼組成或數值空間。 分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：Manufacturing Default, Security, Lockdown Persistence, All Personalities。

- 解決的問題：定義〈Personality Identifier List〉的識別碼組成或數值空間。

- 閱讀順序：分開數值寬度、核發來源、唯一性範圍與保留值；來源索引：Manufacturing Default, Security, Lockdown Persistence, All Personalities。

- 條件與限制：來源 keyword 索引：`may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.13.1.28 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：依定義寬度解析 Manufacturing Default，再核對 Security 的唯一性範圍後才把它當成 identity key。 此例不新增規格要求。

- 來源欄位索引：Manufacturing Default, Security, Lockdown Persistence, All Personalities

- 來源 keyword 索引：`may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.25, Figure 512, 文件頁 485, PDF 頁 511

</details>

<details markdown="1">
<summary><strong>Figure 527: Start Voltage Measurements Data Structure</strong></summary>

<!-- claim:BASEFWLOG-FIG-527-CLAIM figure-table:BASEFWLOG-FIG-527 -->

Figure 527〈Start Voltage Measurements Data Structure〉：定義〈Start Voltage Measurements Data Structure〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：LVOLTA, VMLT, VSSEL, SVMT, LVOLT, LOVT, LUVT, VOLSS。

- 解決的問題：定義〈Start Voltage Measurements Data Structure〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：LVOLTA, VMLT, VSSEL, SVMT, LVOLT, LOVT, LUVT, VOLSS。

- 條件與限制：來源 keyword 索引：`shall`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.13.1.35 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：以 LVOLTA 作為 parser 的第一個檢查點，再用 VMLT 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：LVOLTA, VMLT, VSSEL, SVMT, LVOLT, LOVT, LUVT, VOLSS

- 來源 keyword 索引：`shall`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.30, Figure 527, 文件頁 502, PDF 頁 528

</details>

<details markdown="1">
<summary><strong>Figure 656: Management Operation Specific – Reclaim Unit Handle Update Operation</strong></summary>

<!-- claim:BASEFWLOG-FIG-656-CLAIM figure-table:BASEFWLOG-FIG-656 -->

Figure 656〈Management Operation Specific – Reclaim Unit Handle Update Operation〉：定義〈Management Operation Specific – Reclaim Unit Handle Update Operation〉所表示的 operation 或 state progression。 依序追蹤 request、state、transition condition 與 completion；來源欄位索引：NPID, MAXPIDS, NRG, NRUH, Placement Identifier。

- 解決的問題：定義〈Management Operation Specific – Reclaim Unit Handle Update Operation〉所表示的 operation 或 state progression。

- 閱讀順序：依序追蹤 request、state、transition condition 與 completion；來源欄位索引：NPID, MAXPIDS, NRG, NRUH, Placement Identifier。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。 這是 §5.2.13.1.29 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：從 NPID 開始，只有在引用條文的 transition condition 成立時，才移到 MAXPIDS 所對應的 state。 此例不新增規格要求。

- 來源欄位索引：NPID, MAXPIDS, NRG, NRUH, Placement Identifier

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §7.4.1, Figure 656, 文件頁 570, PDF 頁 596

</details>

<details markdown="1">
<summary><strong>Figure 745: Power Measurement Types</strong></summary>

<!-- claim:BASEFWLOG-FIG-745-CLAIM figure-table:BASEFWLOG-FIG-745 -->

Figure 745〈Power Measurement Types〉：定義〈Power Measurement Types〉中的列舉值、measurement scale 或 sensor selector。 先解 selector／code，再套用對應 unit、scale 或 reserved-value rule；來源欄位索引：0h, NVM subsystem total power, CSTS.SHST。

- 解決的問題：定義〈Power Measurement Types〉中的列舉值、measurement scale 或 sensor selector。

- 閱讀順序：先解 selector／code，再套用對應 unit、scale 或 reserved-value rule；來源欄位索引：0h, NVM subsystem total power, CSTS.SHST。

- 條件與限制：來源 keyword 索引：`may`, `reserved`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.13.1.34 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：先解碼 0h，再套用 NVM subsystem total power 選定的解讀方式；保留值不得自行賦義。 此例不新增規格要求。

- 來源欄位索引：0h, NVM subsystem total power, CSTS.SHST

- 來源 keyword 索引：`may`, `reserved`

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.20, Figure 745, 文件頁 678, PDF 頁 704

</details>

<details markdown="1">
<summary><strong>Figure 746: Power Measurement and Reporting Capabilities</strong></summary>

<!-- claim:BASEFWLOG-FIG-746-CLAIM figure-table:BASEFWLOG-FIG-746 -->

Figure 746〈Power Measurement and Reporting Capabilities〉：定義〈Power Measurement and Reporting Capabilities〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：IPM, SMART, OLEC。

- 解決的問題：定義〈Power Measurement and Reporting Capabilities〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：IPM, SMART, OLEC。

- 條件與限制：來源 keyword 索引：`shall`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.13.1.34 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：以 IPM 作為 parser 的第一個檢查點，再用 SMART 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：IPM, SMART, OLEC

- 來源 keyword 索引：`shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.20, Figure 746, 文件頁 678, PDF 頁 704

</details>

<details markdown="1">
<summary><strong>Figure 747: Power Scale</strong></summary>

<!-- claim:BASEFWLOG-FIG-747-CLAIM figure-table:BASEFWLOG-FIG-747 -->

Figure 747〈Power Scale〉：定義〈Power Scale〉中的列舉值、measurement scale 或 sensor selector。 先解 selector／code，再套用對應 unit、scale 或 reserved-value rule；來源欄位索引：01b = 0.0001 W, 10b = 0.01 W。

- 解決的問題：定義〈Power Scale〉中的列舉值、measurement scale 或 sensor selector。

- 閱讀順序：先解 selector／code，再套用對應 unit、scale 或 reserved-value rule；來源欄位索引：01b = 0.0001 W, 10b = 0.01 W。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。 這是 §5.2.13.1.34 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：先解碼 01b = 0.0001 W，再套用 10b = 0.01 W 選定的解讀方式；保留值不得自行賦義。 此例不新增規格要求。

- 來源欄位索引：01b = 0.0001 W, 10b = 0.01 W

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.20, Figure 747, 文件頁 679, PDF 頁 705

</details>

<details markdown="1">
<summary><strong>Figure 772: Sanitize Operation State Machine</strong></summary>

<!-- claim:BASEFWLOG-FIG-772-CLAIM figure-table:BASEFWLOG-FIG-772 -->

Figure 772〈Sanitize Operation State Machine〉：定義〈Sanitize Operation State Machine〉所表示的 operation 或 state progression。 依序追蹤 request、state、transition condition 與 completion；來源欄位索引：SANS, Idle, Restricted Processing, Unrestricted Processing, Media Verification。

- 解決的問題：定義〈Sanitize Operation State Machine〉所表示的 operation 或 state progression。

- 閱讀順序：依序追蹤 request、state、transition condition 與 completion；來源欄位索引：SANS, Idle, Restricted Processing, Unrestricted Processing, Media Verification。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。 這是 §5.2.13.1.38 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：從 SANS 開始，只有在引用條文的 transition condition 成立時，才移到 Idle 所對應的 state。 此例不新增規格要求。

- 來源欄位索引：SANS, Idle, Restricted Processing, Unrestricted Processing, Media Verification

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.4, Figure 772, 文件頁 720, PDF 頁 746

</details>

<details markdown="1">
<summary><strong>Figure 782: UUID Index Field</strong></summary>

<!-- claim:BASEFWLOG-FIG-782-CLAIM figure-table:BASEFWLOG-FIG-782 -->

Figure 782〈UUID Index Field〉：定義〈UUID Index Field〉的實際配置或數值關係。 依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：UIDX, UUID。

- 解決的問題：定義〈UUID Index Field〉的實際配置或數值關係。

- 閱讀順序：依 byte／bit 順序、length、access type 與保留區閱讀；來源欄位索引：UIDX, UUID。

- 條件與限制：來源 keyword 索引：`shall`。索引用來定位規範性語句，不取代各欄位所附的完整條件。 這是 §5.2.13 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：以 UIDX 作為 parser 的第一個檢查點，再用 UUID 獨立檢查另一個邊界。 此例不新增規格要求。

- 來源欄位索引：UIDX, UUID

- 來源 keyword 索引：`shall`

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.31.2, Figure 782, 文件頁 738, PDF 頁 764

</details>

<details markdown="1">
<summary><strong>Figure 783: Voltage Sensors</strong></summary>

<!-- claim:BASEFWLOG-FIG-783-CLAIM figure-table:BASEFWLOG-FIG-783 -->

Figure 783〈Voltage Sensors〉：定義〈Voltage Sensors〉中的列舉值、measurement scale 或 sensor selector。 先解 selector／code，再套用對應 unit、scale 或 reserved-value rule；來源欄位索引：VSEN1, VSEN2, VSEN3, VSEN4。

- 解決的問題：定義〈Voltage Sensors〉中的列舉值、measurement scale 或 sensor selector。

- 閱讀順序：先解 selector／code，再套用對應 unit、scale 或 reserved-value rule；來源欄位索引：VSEN1, VSEN2, VSEN3, VSEN4。

- 條件與限制：這張 Figure 主要提供結構或說明；本導讀不把圖示關係提升為新的規格要求。 這是 §5.2.13.1.35 直接引用的範圍外相依 Figure；此處只教學指定章節需要的元素。

- 說明性範例（informative example）：先解碼 VSEN1，再套用 VSEN2 選定的解讀方式；保留值不得自行賦義。 此例不新增規格要求。

- 來源欄位索引：VSEN1, VSEN2, VSEN3, VSEN4

- 來源 keyword 索引：none

> 來源：NVME-BASE-2.4, Rev. 2.4, §8.1.32, Figure 783, 文件頁 740, PDF 頁 766

</details>

## 使用與限制

製作 PPT 時以 claim ID 作為追溯鍵。來源 revision、Errata 集合或核准範圍改變時，必須重新核對受影響 claim。
