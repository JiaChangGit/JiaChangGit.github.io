---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4：Firmware Update 與 LID 03h 驗證"
date: 2026-09-01
description: "從主題主軸到關鍵機制、條件與例子的 NVMe 技術報告。"
lang: zh-Hant-TW
img: posts/2026/dogMC_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
nvme_notes: true
---
[English]({% post_url 2026-08-31-nvme-base-firmware-log-admin-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="opening">韌體更新包含傳送映像、保存至 slot 與切換執行版本。這篇說明 Firmware Image Download、Firmware Commit 和 Firmware Slot Information 如何一起完成這件事，並分清楚每一步改變了什麼狀態。</p>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>能力與更新單位</h3><p>確認可用 slots、寫入限制及下載片段的粒度。</p></article>
<article><span class="axis-number">02</span><h3>下載與啟用</h3><p>理解映像範圍、Commit Action 與 reset 的關係。</p></article>
<article><span class="axis-number">03</span><h3>執行版本</h3><p>以目前與預定 active slot 區分已保存和正在執行的版本。</p></article>
</div>

<p>Firmware slot 是保存韌體映像的位置；有版本字串不代表該映像正在執行。控制器的能力查詢、命令完成與 slot 資訊必須分別理解。</p>
</section>
<section class="lesson" id="module-fw-capability-plan"><h2 id="heading-fw-capability-plan"><span class="section-number">01</span> 更新前的能力與限制</h2>
<p>Firmware update 不是固定 command recipe。FRMW 決定 slot 與 activation 能力，FWUG 決定 download chunk 的 granularity／alignment，MTFA 與 MPTFAWR 決定 host 能等待多久，MDS／DID 則決定結果影響哪一組 controllers。</p><dl class="term-note" aria-label="本段名詞"><div><dt>MPTFAWR</dt><dd>Maximum Processing Time for Firmware Activation Without Reset，立即 activation 不需要 reset 時的最大處理時間。</dd></div><div><dt>FRMW</dt><dd>Firmware Updates，Identify Controller 中回報 slot 數、slot 1 read-only 與 activation 能力的欄位。</dd></div><div><dt>FWUG</dt><dd>Firmware Update Granularity，download portion 的 granularity／alignment 能力欄位。</dd></div><div><dt>MTFA</dt><dd>Maximum Time for Firmware Activation，activation 可能暫停 command processing 的最長時間。</dd></div><div><dt>DID</dt><dd>Domain Identifier，辨識 NVM subsystem 內 domain 的 identifier。</dd></div><div><dt>MDS</dt><dd>Multiple Domain Subsystem，指出 NVM subsystem 是否包含多個 domains 的能力 bit。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASEFWLOG-CAP-FRMW -->
<p>FRMW 的 SMUD、FAWR、NOFS 與 FFSRO 分別表示重疊 update 偵測、免 reset activation、domain 支援的 slot 數（1 到 7）以及 slot 1 是否 read-only。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.14.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 354, PDF 頁 380</p></details>
<!-- claim:BASEFWLOG-CAP-FWUG -->
<p>FWUG 以 4 KiB 為單位限制 NUMD 與 OFST 的 granularity／alignment：1h=4 KiB、2h=8 KiB、0h=未提供資訊、FFh=可用任何 dword granularity 與 alignment。違反時 controller 可（may）回 Invalid Field in Command。</p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div><div><dt>NUMD</dt><dd>Number of Dwords，0's-based transfer dword count；實際 bytes = (NUMD + 1) × 4。</dd></div><div><dt>OFST</dt><dd>Offset，Firmware Image Download 中以 dword 為單位的 image-relative offset。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.14.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 359, PDF 頁 385</p></details>
<!-- claim:BASEFWLOG-CAP-MTFA -->
<p>MTFA 以 100 ms 為單位，表示 activation 時 controller 暫停處理 commands 的最長時間；支援免 reset activation 時此欄位必須（shall）有效，0h 表示最大時間未定義。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.14.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 357, PDF 頁 383</p></details>
<!-- claim:BASEFWLOG-CAP-MPTFAWR -->
<p>MPTFAWR 以 100 ms 為單位，估算 CA=011b 的 Firmware Commit 從處理到完成所需最大時間，且包含把 image commit 到 slot 的時間；不支援免 reset activation 時必須（shall）為 0h。</p><dl class="term-note" aria-label="本段名詞"><div><dt>CA</dt><dd>Commit Action，Firmware Commit 中選擇 replace、activate 與 reset policy 的欄位。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.14.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 364, PDF 頁 390</p></details>
<!-- claim:BASEFWLOG-CAP-MDS-ULIST -->
<p>CTRATT.MDS 判斷 LID 03h 回傳 domain scope 還是整個 NVM subsystem scope；CTRATT.ULIST 判斷 controller 是否支援 UUID List reporting。MDS=1 時 DID 必須（shall）非零；single-domain subsystem 的 DID 必須（shall）為 0h。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NVM subsystem</dt><dd>NVM subsystem，包含 controller、port、namespace 與非揮發性儲存資源的 NVMe 系統邊界。</dd></div><div><dt>LID 03h</dt><dd>Firmware Slot Information log page 的 identifier 03h。</dd></div><div><dt>ULIST</dt><dd>UUID List，指出 controller 是否支援 UUID List data structure 的能力 bit。</dd></div><div><dt>UUID</dt><dd>Universally Unique Identifier，128-bit identifier；其實際關聯範圍仍由使用它的資料結構決定。</dd></div><div><dt>LID</dt><dd>Log Page Identifier，Get Log Page command 用來選擇 log page 的欄位。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.14.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 346, 364, PDF 頁 372, 390</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>FRMW</td><td>可用 slots、slot 1 read-only、activation 能力</td><td>選 FS 與 CA 前先讀</td></tr><tr><td>FWUG</td><td>download portion 的粒度與對齊</td><td>先換成 bytes，再切 image</td></tr><tr><td>MTFA／MPTFAWR</td><td>可能暫停與立即 activation 的時間界線</td><td>timeout 不可寫死</td></tr><tr><td>MDS／DID</td><td>firmware slots 的共享 domain</td><td>不可只用 PCI Function 當 scope</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>CA</dt><dd>Commit Action，Firmware Commit 中選擇 replace、activate 與 reset policy 的欄位。</dd></div><div><dt>FS</dt><dd>Firmware Slot，Firmware Commit 中選擇目標 slot 的欄位。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p>若 FWUG 解碼為 4 KiB，12 KiB image 可切成三個 4 KiB portions；最後一筆不是任意長度的尾包。計畫還要先確認 slot 2 合法且不是 read-only，並依 activation path 選擇 timeout。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:BASEFWLOG-FIG-337 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-337"><summary>Base Figure 337 · Command Set Identifiers</summary>
<!-- claim:BASEFWLOG-FIG-337-CLAIM -->
<p>Figure 337〈Command Set Identifiers〉：定義〈Command Set Identifiers〉的識別碼組成或數值空間。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.14.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, Figure 337, 文件頁 340, PDF 頁 366</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-338 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-338"><summary>Base Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</summary>
<!-- claim:BASEFWLOG-FIG-338-CLAIM -->
<p>Figure 338〈Identify – Identify Controller Data Structure, I/O Command Set Independent〉：定義〈Identify – Identify Controller Data Structure, I/O Command Set Independent〉的實際配置或數值關係。</p><dl class="term-note" aria-label="本段名詞"><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.14.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, 文件頁 340-364, PDF 頁 366-390</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>ULIST</dt><dd>UUID List，指出 controller 是否支援 UUID List data structure 的能力 bit。</dd></div><div><dt>FR</dt><dd>Firmware Revision，Identify Controller 回報目前 active firmware revision 的八-byte ASCII 欄位。</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-fw-download-geometry"><h2 id="heading-fw-download-geometry"><span class="section-number">02</span> Download 的長度、偏移與分段</h2>
<p>每筆 Firmware Image Download 都用 DPTR 指向 host buffer，再用 0's-based NUMD 表示 transfer dwords、用 OFST 表示 image-relative dword offset。host 必須同時證明 buffer、length、offset、FWUG 與前後 portions 沒有 gap／overlap。</p><dl class="term-note" aria-label="本段名詞"><div><dt>0's-based</dt><dd>0's-based encoding，以 0 表示實際數量 1；解碼公式通常是欄位值加 1。</dd></div><div><dt>DPTR</dt><dd>Data Pointer，SQE 中指出 command data buffer 的欄位。</dd></div><div><dt>NUMD</dt><dd>Number of Dwords，0's-based transfer dword count；實際 bytes = (NUMD + 1) × 4。</dd></div><div><dt>OFST</dt><dd>Offset，Firmware Image Download 中以 dword 為單位的 image-relative offset。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASEFWLOG-DOWNLOAD-RANGE -->
<p>Firmware Image Download 可分成多個 portions，firmware image portions 可不依序送達；host 宜（should）避免 ranges 重疊並符合 FWUG。Boot Partition portions 則必須（shall）依序提交。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.10</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, 文件頁 205-206, PDF 頁 231-232</p></details>
<!-- claim:BASEFWLOG-DOWNLOAD-FIELDS -->
<p>NVMe over PCIe 的 Admin command 不得使用 SGL，因此 DPTR 以 PRP 指向本次來源 buffer；NUMD 是 0's-based dword count，所以 bytes=(NUMD+1)×4；OFST 是距 image 起點的 dword offset，所以 byte offset=OFST×4。包含 image 起點的 portion 必須（shall）令 OFST=0h。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div><div><dt>NVMe</dt><dd>Non-Volatile Memory Express，主機與非揮發性記憶體子系統之間的介面規範家族。</dd></div><div><dt>PCIe</dt><dd>PCI Express，NVMe memory-based controller 使用的 transport 與裝置互連。</dd></div><div><dt>PRP</dt><dd>Physical Region Page，以 memory page 為單位描述 host-addressable data buffer 的 pointer 格式。</dd></div><div><dt>SGL</dt><dd>Scatter Gather List，以 descriptor 與 segment 描述一段或多段 data buffer 的格式。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.1.1, 5.2.10</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 5.2.10, 文件頁 140-142, 205-206, PDF 頁 166-168, 231-232</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>DPTR</td><td>本筆 transfer 的 host buffer</td><td>地址有效不代表 length 正確</td></tr><tr><td>NUMD</td><td>本筆 dword 數的 0's-based encoding</td><td>4096 bytes → 1024 dwords → 03FFh</td></tr><tr><td>OFST</td><td>image 起點的 dword offset</td><td>第二個 4 KiB portion 為 1024 dwords</td></tr><tr><td>FWUG</td><td>portion alignment／granularity gate</td><td>全 image 與每筆 portion 分開檢查</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p>12 KiB image、4 KiB chunks：portion 0 使用 NUMD=03FFh、OFST=00000000h；portion 1 使用 NUMD=03FFh、OFST=00000400h；portion 2 使用 NUMD=03FFh、OFST=00000800h。三筆 completion 都成功後才可 Commit。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:BASEFWLOG-FIG-190 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-190"><summary>Base Figure 190 · Firmware Image Download – Data Pointer</summary>
<!-- claim:BASEFWLOG-FIG-190-CLAIM -->
<p>Figure 190〈Firmware Image Download – Data Pointer〉：定義〈Firmware Image Download – Data Pointer〉如何指出本命令的來源或目的 buffer。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.10</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 190, 文件頁 205, PDF 頁 231</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-191 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-191"><summary>Base Figure 191 · Firmware Image Download – Command Dword 10</summary>
<!-- claim:BASEFWLOG-FIG-191-CLAIM -->
<p>Figure 191〈Firmware Image Download – Command Dword 10〉：定義〈Firmware Image Download – Command Dword 10〉的實際配置或數值關係。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Dword</dt><dd>Double word，四個 bytes、共 32 bits；NVMe command 欄位常以 CDW 編號。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.10</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 191, 文件頁 205, PDF 頁 231</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-192 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-192"><summary>Base Figure 192 · Firmware Image Download – Command Dword 11</summary>
<!-- claim:BASEFWLOG-FIG-192-CLAIM -->
<p>Figure 192〈Firmware Image Download – Command Dword 11〉：定義〈Firmware Image Download – Command Dword 11〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.10</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 192, 文件頁 206, PDF 頁 232</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-193 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-193"><summary>Base Figure 193 · Firmware Image Download – Command Specific Status Values</summary>
<!-- claim:BASEFWLOG-FIG-193-CLAIM -->
<p>Figure 193〈Firmware Image Download – Command Specific Status Values〉：定義〈Firmware Image Download – Command Specific Status Values〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.10</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, Figure 193, 文件頁 206, PDF 頁 232</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-093 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-093"><summary>Base Figure 93 · Common Command Format</summary>
<!-- claim:BASEFWLOG-FIG-093-CLAIM -->
<p>Figure 93〈Common Command Format〉：定義〈Common Command Format〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §4.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, 文件頁 140-142, PDF 頁 166-168</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-fw-commit-state"><h2 id="heading-fw-commit-state"><span class="section-number">03</span> Commit 的儲存與啟用選擇</h2>
<p>Commit Action（CA）不是成功／失敗旗標；它同時決定 replace、activate 與 reset boundary。Firmware Slot（FS）選擇目標 slot，CQE status 決定下一步是驗證、執行特定 reset、等待，還是停止。</p><dl class="term-note" aria-label="本段名詞"><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div></dl>
<figure><figcaption><strong>下載、保存與啟用分別改變什麼</strong></figcaption><ol class="flow-steps"><li>Firmware Image Download：傳送映像的各個片段。</li><li>Firmware Commit：依 CA 選擇保存至 slot 與啟用方式。</li><li>需要 reset 的啟用：在指定 reset 發生後切換執行版本。</li><li>Firmware Slot Information：分開查看目前執行 slot 與下次預定 slot。</li></ol><figcaption>下載完成、映像已保存、版本正在執行，是不同狀態。</figcaption></figure>

<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASEFWLOG-COMMIT-PURPOSE -->
<p>Firmware Commit 驗證最後下載的 image、把它放入 firmware slot，並依 Commit Action 決定只放置、在後續 Controller Level Reset activation，或立即 activation。成功 commit 不等於當下已 active。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.9</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 202-203, PDF 頁 228-229</p></details>
<!-- claim:BASEFWLOG-COMMIT-CDW10 -->
<p>CDW10[5:3] 是 CA，CDW10[2:0] 是 FS。CA 000b 只放置；001b 放置並排定下次 CLR activation；010b 排定既有 slot；011b 立即 activation。FS=0h 時 controller 必須（shall）在 slot 1 到 7 中選一個。</p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.9</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 203, PDF 頁 229</p></details>
<!-- claim:BASEFWLOG-COMMIT-MUD -->
<p>Firmware Commit CQE.DW0[1:0] 的 MUD 分別回報 Management Endpoint 與 Admin Submission Queue 偵測到的 overlap。若 FRMW.SMUD=0，MUD 必須（shall）為 00b；MUD 在 command 成功或 aborted 時都有效。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div><div><dt>MUD</dt><dd>Multiple Update Detected，completion 中指出 controller 偵測到 overlapping firmware update sequence 的 bit。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.9</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 204, PDF 頁 230</p></details>
<!-- claim:BASEFWLOG-COMMIT-STATUS -->
<p>Firmware Commit 的 command-specific status 區分 invalid slot／image、需要 Conventional／NVM Subsystem／Controller Level Reset、MTFA violation、activation prohibited、overlapping range、Boot Partition write prohibited 與 personality incompatibility。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.9</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 204-205, PDF 頁 230-231</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>CA</td><td>replace 與 activation 行為</td><td>不可只記十進位值</td></tr><tr><td>FS</td><td>目標 firmware slot</td><td>0 可能代表 controller 選 slot，依定義判讀</td></tr><tr><td>SCT／SC</td><td>成功、reset scope 或失敗原因</td><td>0Bh、10h、11h 的 reset scope 不同</td></tr><tr><td>MUD</td><td>重疊 update sequence 證據</td><td>即使 abort 也可能有效</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div><div><dt>MUD</dt><dd>Multiple Update Detected，completion 中指出 controller 偵測到 overlapping firmware update sequence 的 bit。</dd></div><div><dt>SCT</dt><dd>Status Code Type，先決定 status 所屬大類，再解讀 SC。</dd></div><div><dt>SC</dt><dd>Status Code，在 SCT 上下文中表示具體完成結果的 code。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p>若 completion 回報 Firmware Activation Requires Controller Level Reset，Commit 本身可已成功，但 image 尚未成為 current active firmware。software 應記錄 status、執行正確 reset，再以 Identify.FR 與 LID 03h 驗證。</p><dl class="term-note" aria-label="本段名詞"><div><dt>LID 03h</dt><dd>Firmware Slot Information log page 的 identifier 03h。</dd></div><div><dt>LID</dt><dd>Log Page Identifier，Get Log Page command 用來選擇 log page 的欄位。</dd></div><div><dt>FR</dt><dd>Firmware Revision，Identify Controller 回報目前 active firmware revision 的八-byte ASCII 欄位。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:BASEFWLOG-FIG-187 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-187"><summary>Base Figure 187 · Firmware Commit – Command Dword 10</summary>
<!-- claim:BASEFWLOG-FIG-187-CLAIM -->
<p>Figure 187〈Firmware Commit – Command Dword 10〉：定義〈Firmware Commit – Command Dword 10〉的實際配置或數值關係。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Dword</dt><dd>Double word，四個 bytes、共 32 bits；NVMe command 欄位常以 CDW 編號。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.9</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, Figure 187, 文件頁 203, PDF 頁 229</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-188 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-188"><summary>Base Figure 188 · Firmware Commit – Completion Queue Entry Dword 0</summary>
<!-- claim:BASEFWLOG-FIG-188-CLAIM -->
<p>Figure 188〈Firmware Commit – Completion Queue Entry Dword 0〉：呈現〈Firmware Commit – Completion Queue Entry Dword 0〉中的 queue 或 command 關係。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.9.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 188, 文件頁 204, PDF 頁 230</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-189 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-189"><summary>Base Figure 189 · Firmware Commit – Command Specific Status Values</summary>
<!-- claim:BASEFWLOG-FIG-189-CLAIM -->
<p>Figure 189〈Firmware Commit – Command Specific Status Values〉：定義〈Firmware Commit – Command Specific Status Values〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.9.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9.1, Figure 189, 文件頁 204-205, PDF 頁 230-231</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-fw-lid03-proof"><h2 id="heading-fw-lid03-proof"><span class="section-number">04</span> LID 03h 的目前與待啟用版本</h2>
<p>Get Log Page 先用 common command 欄位建立 512-byte transfer，再以 LID=03h 選 Firmware Slot Information。AFI 同時拆成 CAFS 與 NAFS，FRS1-FRS7 表示各 slots 的 revision；最後還要用 Identify.FR 與 domain scope 交叉確認。</p><dl class="term-note" aria-label="本段名詞"><div><dt>CAFS</dt><dd>Current Active Firmware Slot，AFI 低三 bits，指出目前正在執行的 firmware slot。</dd></div><div><dt>NAFS</dt><dd>Next Active Firmware Slot，AFI bits 6:4，指出下一次 reset 後預定啟用的 slot；0 表示未排定。</dd></div><div><dt>AFI</dt><dd>Active Firmware Info，LID 03h 中同時包含目前 active slot 與下一次 reset 後預定 active slot 的 byte。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASEFWLOG-LOG-COMMAND -->
<p>讀 LID 03h 時，未使用 namespace，因此 NSID 必須（shall）為 0h；DPTR 以 PRP 指向 512-byte destination buffer。必要的 CDW10-CDW14 slice 為 LID=03h、LSP=0、RAE=0、NUMDL/NUMDU 表示 512 bytes、LSI=0、LPOL/LPOU=0、OT=0、UIDX=0；CSI 對 LID 03h 不使用，controller 依 Figure 208 規則忽略。</p><dl class="term-note" aria-label="本段名詞"><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div><div><dt>NUMDL</dt><dd>Number of Dwords Lower，Get Log Page 的 NUMD 低 16 bits。</dd></div><div><dt>NUMDU</dt><dd>Number of Dwords Upper，Get Log Page 的 NUMD 高 16 bits。</dd></div><div><dt>LPOL</dt><dd>Log Page Offset Lower，Get Log Page byte offset 的低 32 bits。</dd></div><div><dt>LPOU</dt><dd>Log Page Offset Upper，Get Log Page byte offset 的高 32 bits。</dd></div><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div><div><dt>UIDX</dt><dd>UUID Index，指向 UUID List 位置的 index；0 表示未指定 UUID。</dd></div><div><dt>CSI</dt><dd>Command Set Identifier，選擇 command 或 log page 所套用的 I/O Command Set context。</dd></div><div><dt>LSI</dt><dd>Log Specific Identifier，意義由所選 log page 定義的 identifier。</dd></div><div><dt>LSP</dt><dd>Log Specific Field，意義由所選 log page 定義的 command selector。</dd></div><div><dt>PRP</dt><dd>Physical Region Page，以 memory page 為單位描述 host-addressable data buffer 的 pointer 格式。</dd></div><div><dt>RAE</dt><dd>Retain Asynchronous Event，Get Log Page 是否保留相關 asynchronous event 的 selector。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.1.1, 5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 5.2.13, 文件頁 140-142, 212-215, PDF 頁 166-168, 238-241</p></details>
<!-- claim:BASEFWLOG-LOG-LENGTH -->
<p>NUMDL 與 NUMDU 合成 0's-based dword count。LID 03h 固定 512 bytes=128 dwords，因此 NUMD=127=0000007Fh，NUMDL=007Fh、NUMDU=0000h；在 LSP=0、RAE=0 下，CDW10=007F0003h。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, 文件頁 213-215, PDF 頁 239-241</p></details>
<!-- claim:BASEFWLOG-LOG-SCOPE -->
<p>Figure 209 的 LID 03h row 指定 CSI=N、scope=Domain／NVM subsystem、reference=§5.2.13.1.4。MDS=1 時回傳處理 command 之 controller 所屬 domain；否則回傳整個 NVM subsystem 的資訊。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NVM subsystem</dt><dd>NVM subsystem，包含 controller、port、namespace 與非揮發性儲存資源的 NVMe 系統邊界。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, 文件頁 215-216, PDF 頁 241-242</p></details>
<!-- claim:BASEFWLOG-LID03-AFI -->
<p>byte 0 的 AFI 中，NAFS=bits 6:4、CAFS=bits 2:0；bits 7 與 3 reserved。NAFS 非零表示將於下一次能觸發 activation 的 CLR 啟用該 slot，NAFS=0 表示 controller 未指出 next slot；CAFS 是目前執行 image 的來源 slot。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, 文件頁 226, PDF 頁 252</p></details>
<!-- claim:BASEFWLOG-LID03-FRS -->
<p>FRS1 到 FRS7 位於 bytes 8-63，每格 8 bytes；slot 沒有有效 revision 或不支援時，該 FRS 必須（shall）清為 0h。bytes 1-7 與 64-511 reserved。</p><dl class="term-note" aria-label="本段名詞"><div><dt>FRS</dt><dd>Firmware Revision for Slot，LID 03h 中每個 slot 的八-byte revision 字串欄位。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, 文件頁 226, PDF 頁 252</p></details>
<!-- claim:BASEFWLOG-CAP-FR -->
<p>Identify Controller 的 FR 是目前 active firmware revision 的 8-byte ASCII string，scope 是 controller 所屬 domain；它與 LID 03h 回報的目前 revision 資訊相同。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.14.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 340, PDF 頁 366</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>CAFS</td><td>目前執行中的 slot</td><td>它不是 next-reset intent</td></tr><tr><td>NAFS</td><td>下一個 reset 後預定 active slot</td><td>0 表示未排定</td></tr><tr><td>FRSx</td><td>slot x 的 8-byte revision</td><td>全 0h 不是 ASCII 字串</td></tr><tr><td>Identify.FR</td><td>目前 active revision 的獨立觀察</td><td>與 CAFS 對應 FRSx 交叉確認</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p>AFI=22h 時，CAFS=2、NAFS=2；表示 slot 2 現在 active，且 reset 後仍預定 slot 2。若 CAFS=1、NAFS=2，代表 activation 尚未跨過 reset boundary。此解碼是說明性範例，仍須以 Figure 215 的 bit 定義核對。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:BASEFWLOG-FIG-203 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-203"><summary>Base Figure 203 · Get Log Page – Data Pointer</summary>
<!-- claim:BASEFWLOG-FIG-203-CLAIM -->
<p>Figure 203〈Get Log Page – Data Pointer〉：定義〈Get Log Page – Data Pointer〉如何指出本命令的來源或目的 buffer。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 203, 文件頁 213, PDF 頁 239</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-204 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-204"><summary>Base Figure 204 · Get Log Page – Command Dword 10</summary>
<!-- claim:BASEFWLOG-FIG-204-CLAIM -->
<p>Figure 204〈Get Log Page – Command Dword 10〉：定義〈Get Log Page – Command Dword 10〉的回傳配置與 selector／scope 上下文。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Dword</dt><dd>Double word，四個 bytes、共 32 bits；NVMe command 欄位常以 CDW 編號。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 204, 文件頁 213, PDF 頁 239</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NUMDL</dt><dd>Number of Dwords Lower，Get Log Page 的 NUMD 低 16 bits。</dd></div><div><dt>LSP</dt><dd>Log Specific Field，意義由所選 log page 定義的 command selector。</dd></div><div><dt>RAE</dt><dd>Retain Asynchronous Event，Get Log Page 是否保留相關 asynchronous event 的 selector。</dd></div></dl>
</details>
<!-- figure-table:BASEFWLOG-FIG-205 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-205"><summary>Base Figure 205 · Get Log Page – Command Dword 11</summary>
<!-- claim:BASEFWLOG-FIG-205-CLAIM -->
<p>Figure 205〈Get Log Page – Command Dword 11〉：定義〈Get Log Page – Command Dword 11〉的回傳配置與 selector／scope 上下文。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 205, 文件頁 214, PDF 頁 240</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NUMDU</dt><dd>Number of Dwords Upper，Get Log Page 的 NUMD 高 16 bits。</dd></div><div><dt>LSI</dt><dd>Log Specific Identifier，意義由所選 log page 定義的 identifier。</dd></div></dl>
</details>
<!-- figure-table:BASEFWLOG-FIG-206 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-206"><summary>Base Figure 206 · Get Log Page – Command Dword 12</summary>
<!-- claim:BASEFWLOG-FIG-206-CLAIM -->
<p>Figure 206〈Get Log Page – Command Dword 12〉：定義〈Get Log Page – Command Dword 12〉的回傳配置與 selector／scope 上下文。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 206, 文件頁 214, PDF 頁 240</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>LPOL</dt><dd>Log Page Offset Lower，Get Log Page byte offset 的低 32 bits。</dd></div></dl>
</details>
<!-- figure-table:BASEFWLOG-FIG-207 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-207"><summary>Base Figure 207 · Get Log Page – Command Dword 13</summary>
<!-- claim:BASEFWLOG-FIG-207-CLAIM -->
<p>Figure 207〈Get Log Page – Command Dword 13〉：定義〈Get Log Page – Command Dword 13〉的回傳配置與 selector／scope 上下文。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 207, 文件頁 214, PDF 頁 240</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>LPOU</dt><dd>Log Page Offset Upper，Get Log Page byte offset 的高 32 bits。</dd></div></dl>
</details>
<!-- figure-table:BASEFWLOG-FIG-208 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-208"><summary>Base Figure 208 · Get Log Page – Command Dword 14</summary>
<!-- claim:BASEFWLOG-FIG-208-CLAIM -->
<p>Figure 208〈Get Log Page – Command Dword 14〉：定義〈Get Log Page – Command Dword 14〉的回傳配置與 selector／scope 上下文。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 208, 文件頁 214-215, PDF 頁 240-241</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>UIDX</dt><dd>UUID Index，指向 UUID List 位置的 index；0 表示未指定 UUID。</dd></div><div><dt>CSI</dt><dd>Command Set Identifier，選擇 command 或 log page 所套用的 I/O Command Set context。</dd></div></dl>
</details>
<!-- figure-table:BASEFWLOG-FIG-209 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-209"><summary>Base Figure 209 · Get Log Page – Log Page Identifiers</summary>
<!-- claim:BASEFWLOG-FIG-209-CLAIM -->
<p>Figure 209〈Get Log Page – Log Page Identifiers〉：定義〈Get Log Page – Log Page Identifiers〉的回傳配置與 selector／scope 上下文。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 209, 文件頁 215-216, PDF 頁 241-242</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NVM subsystem</dt><dd>NVM subsystem，包含 controller、port、namespace 與非揮發性儲存資源的 NVMe 系統邊界。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl>
</details>
<!-- figure-table:BASEFWLOG-FIG-215 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-215"><summary>Base Figure 215 · Firmware Slot Information Log Page</summary>
<!-- claim:BASEFWLOG-FIG-215-CLAIM -->
<p>Figure 215〈Firmware Slot Information Log Page〉：定義〈Firmware Slot Information Log Page〉的回傳配置與 selector／scope 上下文。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, Figure 215, 文件頁 226, PDF 頁 252</p></details>

</details>
</details>
</section>
<section id="additional-details"><h2 id="further-mechanisms">補充機制與資料格式</h2>
<!-- claim:BASEFWLOG-MODEL-DOMAIN -->
<p>同一 domain 內的 controllers 共用 firmware slots，且相同 firmware image 會套用到該 domain 的所有 controllers；若不支援 multiple domains，範圍就是整個 NVM subsystem。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NVM subsystem</dt><dd>NVM subsystem，包含 controller、port、namespace 與非揮發性儲存資源的 NVMe 系統邊界。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.9</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 202, PDF 頁 228</p></details>
<!-- claim:BASEFWLOG-FW-RESET -->
<p>需要 reset 的標準流程是：一筆以上 Firmware Image Download、Firmware Commit 驗證並放入 slot、執行能觸發該 activation 的 Controller Level Reset，然後重新初始化 controller 與 I/O queues。</p><dl class="term-note" aria-label="本段名詞"><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.11</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 文件頁 135-136, PDF 頁 161-162</p></details>
<!-- claim:BASEFWLOG-FW-IMMEDIATE -->
<p>CA=011b 要求立即 activation。Firmware Commit 不是 background operation，會保持進行中直到 activation 成功或失敗；若 Firmware Activation notice 已啟用，受影響 controller 可（may）送出 Firmware Activation Starting event。</p><details class="source-note"><summary>來源：Base 2.4 §3.11</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 文件頁 136, PDF 頁 162</p></details>
<!-- claim:BASEFWLOG-FW-FAILURE -->
<p>若新 image 無法成功載入，controller 必須（shall）回復到最近 activation 的 slot image；若該 image 也無法載入，則載入可用的 baseline read-only image，並產生 Firmware Image Load Error event。</p><details class="source-note"><summary>來源：Base 2.4 §3.11</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 文件頁 136-137, PDF 頁 162-163</p></details>
<!-- claim:BASEFWLOG-FW-SEQUENCE -->
<p>host 不宜（should not）讓 firmware／Boot Partition update sequences 重疊，且同一 sequence 宜（should）只使用一個 controller 或 Management Endpoint。</p><details class="source-note"><summary>來源：Base 2.4 §3.11</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 文件頁 137, PDF 頁 163</p></details>
<!-- claim:BASEFWLOG-FW-DISCARD -->
<p>Firmware Commit 完成後的第一筆新 Firmware Image Download，以及 download 後、Firmware Commit 完成前發生的 Controller Level Reset，都必須（shall）使 controller 丟棄尚存的已下載 portions。</p><details class="source-note"><summary>來源：Base 2.4 §3.11, 5.2.10</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.11, 5.2.10, 文件頁 137, 205-206, PDF 頁 163, 231-232</p></details>
<!-- claim:BASEFWLOG-UUID-LIST -->
<p>firmware revisions 間的 UUID List 宜（should）保持 entry 位置穩定：新增 UUID 宜接在尾端；移除時宜原位改成 NVMe Invalid UUID；不宜重用 invalid entry，也不宜縮短或移除清單。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express，主機與非揮發性記憶體子系統之間的介面規範家族。</dd></div><div><dt>UUID</dt><dd>Universally Unique Identifier，128-bit identifier；其實際關聯範圍仍由使用它的資料結構決定。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.11.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.11.1, 文件頁 137-138, PDF 頁 163-164</p></details>
<!-- claim:BASEFWLOG-UUID-RESET -->
<p>若 downloaded image 在既有 entry 中，以有效 UUID 取代 NVMe Invalid UUID 或另一個有效 UUID，controller 必須（shall）要求 reset；所有受這個 UUID List 變更影響的 controllers 都必須（shall）reset。</p><details class="source-note"><summary>來源：Base 2.4 §3.11.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.11.1, 文件頁 138, PDF 頁 164</p></details>
<!-- claim:BASEFWLOG-COMMIT-BOOT -->
<p>BPID 與 CA=110b／111b 屬於 Boot Partition：110b 取代指定 partition，111b 將它標成 active；Boot Partition Write Prohibited 是 Firmware Commit 的 command-specific status 之一。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.9</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 203-205, PDF 頁 229-231</p></details>
<!-- claim:BASEFWLOG-LOG-RAE -->
<p>RAE=0 會在 command 成功時清除對應 asynchronous event，RAE=1 則保留；若 command 未成功，controller 必須（shall）保留 event。Firmware Activation Starting event 要以 RAE=0 讀取 LID 03h 才會清除。</p><dl class="term-note" aria-label="本段名詞"><div><dt>RAE</dt><dd>Retain Asynchronous Event，Get Log Page 是否保留相關 asynchronous event 的 selector。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.2, 5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.2, 5.2.13, 文件頁 186, 213, PDF 頁 212, 239</p></details>
<!-- claim:BASEFWLOG-LOG-OFFSET -->
<p>本報告以完整 512-byte LID 03h、LPOL=LPOU=0、OT=0 為基準。一般 byte offset 必須 dword aligned；超過 log page 大小的 offset 必須（shall）回 Invalid Field in Command。LID 03h 不需要 index-offset 分支。</p><dl class="term-note" aria-label="本段名詞"><div><dt>LPOL</dt><dd>Log Page Offset Lower，Get Log Page byte offset 的低 32 bits。</dd></div><div><dt>LPOU</dt><dd>Log Page Offset Upper，Get Log Page byte offset 的高 32 bits。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, 文件頁 214-215, PDF 頁 240-241</p></details>
<!-- claim:BASEFWLOG-LID03-DESCRIPTION -->
<p>Firmware Slot Information log page 固定 512 bytes，說明每個支援 slot 內的 firmware revision，並指出 current active slot 與（若 controller 有回報）next active slot。revision 以 ASCII string 表示。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, 文件頁 225-226, PDF 頁 251-252</p></details>
<!-- claim:BASEFWLOG-RESET-XREF -->
<p>NVMe over PCIe Transport 將 Conventional Reset 與 Function Level Reset 分別列為額外的 transport-specific Controller Level Reset 方法；除 Controller Reset 外，Controller Level Reset 會依 PCI Express Base Specification 重設 PCI register space。</p><dl class="term-note" aria-label="本段名詞"><div><dt>PCIe</dt><dd>PCI Express，NVMe memory-based controller 使用的 transport 與裝置互連。</dd></div></dl><details class="source-note"><summary>來源：PCIe Transport 1.4 §3.3</summary><p>來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.3, 文件頁 11, PDF 頁 11</p></details>
<!-- claim:BASEFWLOG-XREF-337 -->
<p>來源 §5.2.9 將 Firmware Revision 欄位指向 Figure 337；但 Figure 337 是 Command Set Identifiers，FR 實際列在 Figure 338。未取得另行核准的 errata，因此保留並揭露這個來源內部交叉引用差異，不靜默改寫。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.9, 5.2.14.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 5.2.14.1, 文件頁 202, 340, PDF 頁 228, 366</p></details>
<!-- figure-table:BASEFWLOG-FIG-155 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-155"><summary>Base Figure 155 · Asynchronous Event Information – Notice</summary>
<!-- claim:BASEFWLOG-FIG-155-CLAIM -->
<p>Figure 155〈Asynchronous Event Information – Notice〉：定義〈Asynchronous Event Information – Notice〉所表示的 event record、event 分類或記錄條件。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 155, 文件頁 186, PDF 頁 212</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CSTS.PP</dt><dd>Controller Status，controller 回報 ready、fatal status 與 shutdown 狀態的 property。 此處的 CSTS.PP 進一步指定其中的 PP 子欄位。</dd></div><div><dt>CSTS</dt><dd>Controller Status，controller 回報 ready、fatal status 與 shutdown 狀態的 property。</dd></div></dl>
</details>
<!-- figure-table:BASEFWLOG-FIG-347 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-347"><summary>Base Figure 347 · UUID List</summary>
<!-- claim:BASEFWLOG-FIG-347-CLAIM -->
<p>Figure 347〈UUID List〉：定義〈UUID List〉的識別碼組成或數值空間。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.14.2.14</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.14, Figure 347, 文件頁 396, PDF 頁 422</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-348 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-348"><summary>Base Figure 348 · UUID List Entry</summary>
<!-- claim:BASEFWLOG-FIG-348-CLAIM -->
<p>Figure 348〈UUID List Entry〉：定義〈UUID List Entry〉的識別碼組成或數值空間。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.14.2.14</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.14, Figure 348, 文件頁 396, PDF 頁 422</p></details>

</details>
<!-- figure-table:BASEFWLOG-FIG-474 -->
<details class="field-note" id="figure-BASEFWLOG-FIG-474"><summary>Base Figure 474 · Asynchronous Event Configuration – Command Dword 11</summary>
<!-- claim:BASEFWLOG-FIG-474-CLAIM -->
<p>Figure 474〈Asynchronous Event Configuration – Command Dword 11〉：定義〈Asynchronous Event Configuration – Command Dword 11〉所表示的 event record、event 分類或記錄條件。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Dword</dt><dd>Double word，四個 bytes、共 32 bits；NVMe command 欄位常以 CDW 編號。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.6, Figure 474, 文件頁 466-468, PDF 頁 492-494</p></details>

</details>
</section>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:base-admin-fw-logs-download-activate -->
<details class="review-question" id="qa-base-admin-fw-logs-download-activate"><summary>1. Firmware Image Download 完成後，controller 是否已執行新韌體？</summary>
<div data-qa-answer="base-admin-fw-logs-download-activate"><p>Download 是傳送 image；Commit 才依 action 決定保存或啟用，且啟用可能需要指定 reset。要結合 Commit 結果與 slot 資訊確認目前執行版本。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, 文件頁 205-206, PDF 頁 231-232</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 202-203, PDF 頁 228-229</p>
</details></details>
<!-- qa:base-admin-fw-logs-download-units -->
<details class="review-question" id="qa-base-admin-fw-logs-download-units"><summary>2. NUMD=255 與 OFST=256 分別描述什麼？</summary>
<div data-qa-answer="base-admin-fw-logs-download-units"><p>NUMD 是 zero-based dword 長度，表示這次傳送 256 dwords，也就是 1024 bytes；OFST 是從 image 起點算的 dword offset，表示起點在 1024 bytes。相同數量附近的值，編碼用途不同。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 5.2.10, 文件頁 140-142, 205-206, PDF 頁 166-168, 231-232</p>
</details></details>
<!-- qa:base-admin-fw-logs-slot-version -->
<details class="review-question" id="qa-base-admin-fw-logs-slot-version"><summary>3. 某 slot 的 FRS 顯示新版本，能否單憑這一點宣告它正在執行？</summary>
<div data-qa-answer="base-admin-fw-logs-slot-version"><p>FRS 描述 slot 中的 revision；還需看 active slot 與 next-active slot 資訊。已儲存、目前執行和下次啟用可以指向不同狀態。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, 文件頁 226, PDF 頁 252</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, 文件頁 226, PDF 頁 252</p>
</details></details>
<!-- qa:base-admin-fw-logs-firmware-domain -->
<details class="review-question" id="qa-base-admin-fw-logs-firmware-domain"><summary>4. 為何不能總把 firmware update 視為單一 controller 的私有變更？</summary>
<div data-qa-answer="base-admin-fw-logs-firmware-domain"><p>Firmware 的作用範圍可能涉及共用的 domain 或 NVM subsystem 資源。先建立 controller 與更新範圍的關係，才能理解其他 controllers 受到的影響。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 202, PDF 頁 228</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express Base Specification, Revision 2.4</p><p>NVM Express NVMe over PCIe Transport Specification, Revision 1.4</p></details></footer>
</div>
