---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4：Device Self-test、HMB、Doorbell Emulation 與 Vendor Commands"
date: 2026-09-02
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
[English]({% post_url 2026-09-02-nvme-base-self-test-hmb-emulation-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span>本篇涵蓋裝置自我測試、Host Memory Buffer，以及與記憶體和命令格式相關的延伸功能。主線是分清楚功能由誰啟動、資料由誰提供，以及控制器何時仍可使用這些資源。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div></dl>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>自我測試</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span>分清啟動命令、背景測試進度與結果記錄。</p></article>
<article><span class="axis-number">02</span><h3>Host Memory Buffer</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span>理解主機記憶體如何提供給控制器，以及可回收的時機。</p></article>
<article><span class="axis-number">03</span><h3>記憶體與命令延伸</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span>理解 descriptor、Doorbell Emulation 與 vendor command 長度的界線。</p></article>
</div>
<dl class="term-note" aria-label="本段名詞"><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div></dl>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span>主機和控制器各自有記憶體；能夠提供某段記憶體的位址，不代表另一方已停止使用它。這與 OS 中記憶體生命週期的概念相通。</p>
</section>
<section class="lesson" id="module-three-boundaries"><h2 id="heading-three-boundaries"><span class="section-number">01</span> 背景測試、主機記憶體與位址編碼</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span>這組章節不是同一個 feature。Device Self-test 管背景 diagnostic operation；HMB 管 host memory 的 ownership transfer；DSTRD 與 vendor command format 管 encoded value 如何轉成安全的 memory access。共同方法是先找 capability gate，再找狀態或 ownership 轉換，最後找可觀測證據。</p><dl class="term-note" aria-label="本段名詞"><div><dt>DSTRD</dt><dd>Doorbell Stride，CAP 中決定相鄰 doorbell register 間距的欄位。</dd></div><div><dt>HMB</dt><dd>Host Memory Buffer，由 host 配置並在 enable 期間交由 controller 專用的 volatile memory ranges。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASEDIAGMEM-SELFTEST-COMPLETION -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span>Device Self-test command 的 Admin CQE 只證明『啟動／中止動作已被處理』，不是背景測試已完成。command-specific status 1Dh 表示已有 operation in progress；software 必須把 CQE 與後續 LID 06h 分開記錄。</p><dl class="term-note" aria-label="本段名詞"><div><dt>LID 06h</dt><dd>Device Self-test Log Page 的 identifier 06h；同時包含 current operation 與 20 筆歷史結果。</dd></div><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div><div><dt>LID</dt><dd>Log Page Identifier；指定要讀取哪一種 log page 的編號。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 201, PDF 頁 227</p></details>
<!-- claim:BASEDIAGMEM-HMB-OWNERSHIP -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span>HMB 是 host 配置、controller 專用的記憶體租約。Set Features enable 成功後，host 必須（shall）停止寫入 descriptor list 與所有描述的 memory ranges，直到 disable command 完成；這是 ownership transfer，不只是 performance hint。</p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div><div><dt>HMB</dt><dd>Host Memory Buffer，由 host 配置並在 enable 期間交由 controller 專用的 volatile memory ranges。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30.2.3, 8.2.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 8.2.4, 文件頁 515-516, 744, PDF 頁 541-542, 770</p></details>
<!-- claim:BASEDIAGMEM-DOORBELL-STRIDE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.04">01.04.</span>CAP.DSTRD 的實際間距是 2^(2+DSTRD) bytes。DSTRD=0／2／4 分別得到 4／16／64 bytes；software emulation 可用 64-byte stride 把 doorbells 分散到 cacheline，硬體 NVMe interface 的 expected value 是 0h。</p><dl class="term-note" aria-label="本段名詞"><div><dt>DSTRD</dt><dd>Doorbell Stride，CAP 中決定相鄰 doorbell register 間距的欄位。</dd></div><div><dt>NVMe</dt><dd>Non-Volatile Memory Express，主機與非揮發性記憶體子系統之間的介面規範家族。</dd></div><div><dt>CAP</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.4.1, 8.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, 8.2.3, 文件頁 56, 744, PDF 頁 82, 770</p></details>
<!-- claim:BASEDIAGMEM-VENDOR-GATE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.05">01.05.</span>standard Vendor Specific command format 是 optional。AVSCC.VSCF 控制 vendor-specific Admin commands；ICSVSCC.SNVSCF 控制 vendor-specific I/O commands。兩個 capability 必須分開讀，不能因其中一個為 1 就假設另一類命令也使用 Figure 94。</p><dl class="term-note" aria-label="本段名詞"><div><dt>ICSVSCC</dt><dd>I/O Command Set Vendor Specific Command Configuration，回報 vendor-specific I/O command format 的 Identify field。</dd></div><div><dt>SNVSCF</dt><dd>Same NVM Vendor Specific Command Format，ICSVSCC 中表示 I/O commands 是否使用 Figure 94 的 bit。</dd></div><div><dt>AVSCC</dt><dd>Admin Vendor Specific Command Configuration，回報 vendor-specific Admin command format 的 Identify field。</dd></div><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div><div><dt>VSCF</dt><dd>Vendor Specific Command Format，AVSCC 中表示 Admin commands 是否使用 Figure 94 的 bit。</dd></div><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.14.2.1, 8.1.29</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.29, 文件頁 356, 374, 733, PDF 頁 382, 400, 759</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>Self-test</td><td>operation lifecycle</td><td>CQE + LID 06h</td></tr><tr><td>HMB</td><td>exclusive ownership lifecycle</td><td>Get FID 0Dh + disable CQE</td></tr><tr><td>Doorbell emulation</td><td>encoded byte stride</td><td>MMIO address/write trace</td></tr><tr><td>Vendor command</td><td>buffer-length contract</td><td>VSCF/SNVSCF + NDT/NDM</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>LID 06h</dt><dd>Device Self-test Log Page 的 identifier 06h；同時包含 current operation 與 20 筆歷史結果。</dd></div><div><dt>SNVSCF</dt><dd>Same NVM Vendor Specific Command Format，ICSVSCC 中表示 I/O commands 是否使用 Figure 94 的 bit。</dd></div><div><dt>MMIO</dt><dd>Memory-Mapped I/O，以 CPU memory access 形式讀寫裝置 register。</dd></div><div><dt>VSCF</dt><dd>Vendor Specific Command Format，AVSCC 中表示 Admin commands 是否使用 Figure 94 的 bit。</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div><div><dt>FID</dt><dd>Feature Identifier；指定要讀取或設定哪一項 Feature 的編號。</dd></div><div><dt>LID</dt><dd>Log Page Identifier；指定要讀取哪一種 log page 的編號。</dd></div><div><dt>NDM</dt><dd>Number of Dwords in Metadata Transfer，standard vendor-specific format 中的實際 metadata dword 數。</dd></div><div><dt>NDT</dt><dd>Number of Dwords in Data Transfer，standard vendor-specific format 中的實際 data dword 數。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.06">01.06.</span>同樣看到 Successful Completion，self-test 只代表 operation 已開始，HMB disable 則代表 ownership 已回到 host。status code 相同，不代表 completion boundary 相同。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:BASEDIAGMEM-FIG-176 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-176"><summary>Base Figure 176 · Device Self-test Namespace Test Action</summary>
<!-- claim:BASEDIAGMEM-FIG-176-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.07">01.07.</span>Figure 176〈Device Self-test Namespace Test Action〉：呈現〈Device Self-test Namespace Test Action〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 176, 文件頁 199, PDF 頁 225</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-545 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-545"><summary>Base Figure 545 · Host Memory Buffer - Command Dword 11</summary>
<!-- claim:BASEDIAGMEM-FIG-545-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.08">01.08.</span>Figure 545〈Host Memory Buffer - Command Dword 11〉：定義 Host Memory Buffer 在 CDW11 的 command-specific 欄位。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Dword</dt><dd>Dword（Double word）；32 bits，也就是 4 bytes。對比 word=16 bits；例如 zero-based dword count=3 代表 4 個 Dwords，也就是 16 bytes。</dd></div><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 545, 文件頁 516-517, PDF 頁 542-543</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>HMNARE</dt><dd>Host Memory Non-operational Access Restriction Enable，配置 non-operational HMB access policy 的 bit。</dd></div><div><dt>EHM</dt><dd>Enable Host Memory，啟用或停用 controller 使用 HMB 的 bit。</dd></div><div><dt>MR</dt><dd>Memory Return，表示 host 歸還完全相同的舊 HMB size、addresses、descriptors 與 contents。</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-036 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-036"><summary>Base Figure 36 · Offset 0h: CAP - Controller Capabilities</summary>
<!-- claim:BASEDIAGMEM-FIG-036-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.09">01.09.</span>Figure 36〈Offset 0h: CAP - Controller Capabilities〉：定義 offset 0h 的 CAP（Controller Capabilities），並指出軟體在該位置必須分別依欄位換算的欄位。</p><dl class="term-note" aria-label="本段名詞"><div><dt>offset</dt><dd>offset；從指定起點算出的位移。它回答「離起點多遠」，不等於 index。</dd></div><div><dt>CAP</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.4.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, 文件頁 55-58, PDF 頁 81-84</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-094 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-094"><summary>Base Figure 94 · Common Command Format - Vendor Specific Commands (Optional)</summary>
<!-- claim:BASEDIAGMEM-FIG-094-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.10">01.10.</span>Figure 94〈Common Command Format - Vendor Specific Commands (Optional)〉：定義〈Common Command Format - Vendor Specific Commands (Optional)〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §4.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 94, 文件頁 143, PDF 頁 169</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div><div><dt>NDM</dt><dd>Number of Dwords in Metadata Transfer，standard vendor-specific format 中的實際 metadata dword 數。</dd></div><div><dt>NDT</dt><dd>Number of Dwords in Data Transfer，standard vendor-specific format 中的實際 data dword 數。</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-selftest-command-state-machine"><h2 id="heading-selftest-command-state-machine"><span class="section-number">02</span> Device Self-test 的啟動與執行</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span>Self-test 不是同步 diagnostic RPC。Host 先用 OACS.DSTS、DSTO.SDSO 與 EDSTT 決定支援、concurrency scope 與時間預期，再用 NSID 與 STC 建構 command。Admin CQE 回來時，背景 operation 才剛進入可由 LID 06h 觀察的生命週期。</p><dl class="term-note" aria-label="本段名詞"><div><dt>OACS.DSTS</dt><dd>Optional Admin Command Support 的 Device Self-test Supported bit，判斷 command 是否可用。</dd></div><div><dt>EDSTT</dt><dd>Extended Device Self-test Time，在 power state 0 下的 extended test 名目完成分鐘數。</dd></div><div><dt>DSTO</dt><dd>Device Self-test Options，Identify Controller 中回報 refresh 與 concurrency 選項的欄位。</dd></div><div><dt>SDSO</dt><dd>Single Device Self-test Operation，選擇 subsystem-wide 單一 operation 或 per-controller operation 的 bit。</dd></div><div><dt>STC</dt><dd>Self-test Code 是 Device Self-test CDW10 的動作 nibble；result entry 的 STC 則是 Status Code，須依 SCVLD 判斷有效。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASEDIAGMEM-SELFTEST-GATE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span>啟動 Device Self-test 前，先讀 Identify Controller：OACS.DSTS 判斷 command 是否支援；EDSTT 是 extended operation 在 power state 0 的名目分鐘數；DSTO.SDSO 決定同時只能有一個 subsystem-wide operation，或每個 controller 各一個。這三個欄位回答不同問題。</p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div><div><dt>OACS.DSTS</dt><dd>Optional Admin Command Support 的 Device Self-test Supported bit，判斷 command 是否可用。</dd></div><div><dt>EDSTT</dt><dd>Extended Device Self-test Time，在 power state 0 下的 extended test 名目完成分鐘數。</dd></div><div><dt>DSTO</dt><dd>Device Self-test Options，Identify Controller 中回報 refresh 與 concurrency 選項的欄位。</dd></div><div><dt>SDSO</dt><dd>Single Device Self-test Operation，選擇 subsystem-wide 單一 operation 或 per-controller operation 的 bit。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.14.2.1, 8.1.8</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, 文件頁 352-358, 614, PDF 頁 378-384, 640</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-NSID -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span>Device Self-test 由收到 command 的 controller 執行。NSID=00000000h 只測 controller；00000001h～FFFFFFFEh 指定一個 namespace；FFFFFFFFh 包含提交當下可由該 controller 存取的所有 attached namespaces。invalid 與 inactive NSID 會得到不同 status。</p><dl class="term-note" aria-label="本段名詞"><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 199, PDF 頁 225</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-STC -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.04">02.04.</span>CDW10.STC[3:0] 選動作：1h=short、2h=extended、3h=Host-Initiated Refresh、Eh=vendor specific、Fh=abort；其餘 encoding reserved。只有 STC=Eh 時 CDW15.DSTP 才是 vendor specific，其他情況 CDW15 reserved。</p><dl class="term-note" aria-label="本段名詞"><div><dt>DSTP</dt><dd>Device Self-test Parameter，只有 vendor-specific STC=Eh 時才有 vendor-defined 語意的 CDW15。</dd></div><div><dt>STC</dt><dd>Self-test Code 是 Device Self-test CDW10 的動作 nibble；result entry 的 STC 則是 Status Code，須依 SCVLD 判斷有效。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 199-200, PDF 頁 225-226</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-INPROGRESS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.05">02.05.</span>已有 operation 時，再送 short、extended 或 Host-Initiated Refresh 必須以 Device Self-test in Progress 中止；vendor-specific 新命令的行為仍是 vendor specific。STC=Fh 則依序中止目前 operation、建立最新 result、清除 current status，最後成功完成 command。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 200, PDF 頁 226</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>NSID=0</td><td>只包含 controller</td><td>不測 namespace media</td></tr><tr><td>active NSID</td><td>指定 namespace</td><td>invalid 與 inactive status 不同</td></tr><tr><td>NSID=FFFFFFFFh</td><td>所有 attached／accessible namespaces</td><td>集合以 start 時點為準</td></tr><tr><td>STC=Fh</td><td>abort current operation</td><td>成功不代表曾有 operation</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.06">02.06.</span>啟動 namespace 5 的 short test：NSID=00000005h、STC=1h，因此 CDW10=00000001h、CDW15=0。若立刻再送 extended STC=2h，應預期 command-specific status 1Dh，而不是建立第二個 operation。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:BASEDIAGMEM-FIG-177 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-177"><summary>Base Figure 177 · Device Self-test - Command Dword 10</summary>
<!-- claim:BASEDIAGMEM-FIG-177-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.07">02.07.</span>Figure 177〈Device Self-test - Command Dword 10〉：定義 Device Self-test 在 CDW10 的 command-specific 欄位。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Dword</dt><dd>Dword（Double word）；32 bits，也就是 4 bytes。對比 word=16 bits；例如 zero-based dword count=3 代表 4 個 Dwords，也就是 16 bytes。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 177, 文件頁 199, PDF 頁 225</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-178 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-178"><summary>Base Figure 178 · Device Self-test - Command Dword 15</summary>
<!-- claim:BASEDIAGMEM-FIG-178-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.08">02.08.</span>Figure 178〈Device Self-test - Command Dword 15〉：定義 Device Self-test 在 CDW15 的 command-specific 欄位。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 178, 文件頁 200, PDF 頁 226</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>DSTP</dt><dd>Device Self-test Parameter，只有 vendor-specific STC=Eh 時才有 vendor-defined 語意的 CDW15。</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-179 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-179"><summary>Base Figure 179 · Device Self-test - Command Processing</summary>
<!-- claim:BASEDIAGMEM-FIG-179-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.09">02.09.</span>Figure 179〈Device Self-test - Command Processing〉：呈現〈Device Self-test - Command Processing〉中的 queue 或 command 關係。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 179, 文件頁 200, PDF 頁 226</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-180 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-180"><summary>Base Figure 180 · Device Self-test - Command Specific Status Values</summary>
<!-- claim:BASEDIAGMEM-FIG-180-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.10">02.10.</span>Figure 180〈Device Self-test - Command Specific Status Values〉：定義〈Device Self-test - Command Specific Status Values〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 180, 文件頁 201, PDF 頁 227</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-093 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-093"><summary>Base Figure 93 · Common Command Format</summary>
<!-- claim:BASEDIAGMEM-FIG-093-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.11">02.11.</span>Figure 93〈Common Command Format〉：定義〈Common Command Format〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §4.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, 文件頁 140-142, PDF 頁 166-168</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>DPTR</dt><dd>Data Pointer，SQE 中指出 command data buffer 的欄位。</dd></div><div><dt>CID</dt><dd>Command Identifier，與 SQ identifier 合用以辨識 outstanding command。</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-338 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-338"><summary>Base Figure 338 · Identify Controller Data Structure</summary>
<!-- claim:BASEDIAGMEM-FIG-338-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.12">02.12.</span>Figure 338〈Identify Controller Data Structure〉：定義〈Identify Controller Data Structure〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.14.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, 文件頁 340-364, PDF 頁 366-390</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>DSTO.SDSO</dt><dd>Device Self-test Options，Identify Controller 中回報 refresh 與 concurrency 選項的欄位。 此處的 DSTO.SDSO 進一步指定其中的 SDSO 子欄位。</dd></div><div><dt>HMMINDS</dt><dd>Host Memory Buffer Minimum Descriptor Entry Size，每個可用 descriptor 的最低 4 KiB-unit 大小。</dd></div><div><dt>ICSVSCC</dt><dd>I/O Command Set Vendor Specific Command Configuration，回報 vendor-specific I/O command format 的 Identify field。</dd></div><div><dt>HMMAXD</dt><dd>Host Memory Maximum Descriptor Entries，controller 可使用的 descriptor entry 上限。</dd></div><div><dt>AVSCC</dt><dd>Admin Vendor Specific Command Configuration，回報 vendor-specific Admin command format 的 Identify field。</dd></div><div><dt>HMMIN</dt><dd>Host Memory Buffer Minimum Size，以 4 KiB units 回報 controller 要求的最低大小。</dd></div><div><dt>HMPRE</dt><dd>Host Memory Buffer Preferred Size，以 4 KiB units 回報 controller 偏好的配置大小。</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-selftest-observe-results"><h2 id="heading-selftest-observe-results"><span class="section-number">03</span> LID 06h 的目前進度與歷史結果</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span>log header 的 DSTOS／DSTCS 回答『現在跑到哪裡』；RDS1～RDS20 回答『之前怎麼結束』。result entry 又分成 operation code、result reason、segment、validity bitmap 與 diagnostic payload。NVM Command Set 只在 FVLD=1 時賦予 FLBA 明確的 LBA 語意。</p><dl class="term-note" aria-label="本段名詞"><div><dt>DSTCS</dt><dd>Device Self-test Completion Status，LID 06h 中的 0 到 100 完成百分比。</dd></div><div><dt>DSTOS</dt><dd>Device Self-test Operation Status，LID 06h 中表示目前 operation 類型的 nibble。</dd></div><div><dt>FLBA</dt><dd>Failing LBA，NVM Command Set 定義為造成 self-test failure 的其中一個 logical block address。</dd></div><div><dt>FVLD</dt><dd>Failing LBA Valid，決定 FLBA 欄位是否可解讀的 validity bit。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASEDIAGMEM-SELFTEST-LOG-COMMAND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span>讀取 LID 06h 所需的最小 Get Log Page slice 是：LID=06h、LSP=0、RAE 依事件策略選擇、NUMD 表示 564 bytes、LPOL/LPOU=0、OT=0、CSI=0、UIDX=0。564 bytes=141 dwords，因此 0's-based NUMD=140=008Ch；RAE=0 時 CDW10=008C0006h。</p><dl class="term-note" aria-label="本段名詞"><div><dt>0's-based</dt><dd>0's-based encoding，以 0 表示實際數量 1；依欄位換算公式通常是欄位值加 1。</dd></div><div><dt>LPOL</dt><dd>Log Page Offset Lower，Get Log Page byte offset 的低 32 bits。</dd></div><div><dt>LPOU</dt><dd>Log Page Offset Upper，Get Log Page byte offset 的高 32 bits。</dd></div><div><dt>NUMD</dt><dd>Number of Dwords，0's-based transfer dword count；實際 bytes = (NUMD + 1) × 4。</dd></div><div><dt>UIDX</dt><dd>UUID Index，指向 UUID List 位置的 index；0 表示未指定 UUID。</dd></div><div><dt>CSI</dt><dd>I/O Command Set Identifier；選擇 I/O 命令集，NVM Command Set 使用 00h。</dd></div><div><dt>LSP</dt><dd>Log Specific Field，意義由所選 log page 定義的 command selector。</dd></div><div><dt>RAE</dt><dd>Retain Asynchronous Event，Get Log Page 是否保留相關 asynchronous event 的 selector。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, 文件頁 213-216, PDF 頁 239-242</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-CURRENT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.03">03.03.</span>LID 06h 的 byte 0 以 DSTOS 表示目前 operation，byte 1 的 DSTCS[6:0] 是完成百分比；DSTOS=0 時 host 應忽略 DSTCS。controller 在 operation 完成或被中止時，必須先建立 result entry，之後才能把 in-progress status 清為 0。</p><dl class="term-note" aria-label="本段名詞"><div><dt>DSTCS</dt><dd>Device Self-test Completion Status，LID 06h 中的 0 到 100 完成百分比。</dd></div><div><dt>DSTOS</dt><dd>Device Self-test Operation Status，LID 06h 中表示目前 operation 類型的 nibble。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-230, PDF 頁 255-256</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-HISTORY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.04">03.04.</span>LID 06h 保留 20 筆、每筆 28 bytes 的結果，RDS1 永遠是最新完成或中止的 operation。未使用 entry 必須讓 DSTR=Fh 且 DSTC=0h，其他欄位由 host 忽略；不能把全零以外的殘值當成歷史結果。</p><dl class="term-note" aria-label="本段名詞"><div><dt>DSTR</dt><dd>Device Self-test Result，結果 entry 中表示成功、abort 或 segment failure 的 nibble。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-230, PDF 頁 255-256</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-RESULT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.05">03.05.</span>每筆 DSTS 的高 nibble DSTC 表示原始 self-test code，低 nibble DSTR 表示完成／中止原因。只有 DSTR=7h 時 SEGN 才指出第一個失敗 segment；其他 DSTR 下 SEGN 應忽略。</p><dl class="term-note" aria-label="本段名詞"><div><dt>DSTR</dt><dd>Device Self-test Result，結果 entry 中表示成功、abort 或 segment failure 的 nibble。</dd></div><div><dt>SEGN</dt><dd>Segment Number，只有 DSTR=7h 時指出第一個失敗 diagnostic segment。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 231, PDF 頁 257</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-VALIDITY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.06">03.06.</span>VDINFO 的 NSIDVLD、FVLD、SCTVLD、SCVLD 是四個獨立 validity gates。NSID、FLBA、STCT、STC 只有在對應 bit=1 時才可解讀；先驗證 validity，再讀數值，不能用非零值猜測有效。</p><dl class="term-note" aria-label="本段名詞"><div><dt>VDINFO</dt><dd>Valid Diagnostic Information，分別 gate NSID、FLBA、SCT 與 SC 的 validity bitmap。</dd></div><div><dt>FLBA</dt><dd>Failing LBA，NVM Command Set 定義為造成 self-test failure 的其中一個 logical block address。</dd></div><div><dt>FVLD</dt><dd>Failing LBA Valid，決定 FLBA 欄位是否可解讀的 validity bit。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 231-232, PDF 頁 257-258</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-NVM-FLBA -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.07">03.07.</span>Base 將 Figure 219 的 FLBA 留給 I/O Command Set 定義。NVM Command Set 1.3 規定 bytes 23:16 是造成失敗的 logical block address；若有多個失敗 logical blocks，只回其中一個，且僅 FVLD=1 時有效。</p><dl class="term-note" aria-label="本段名詞"><div><dt>logical block</dt><dd>邏輯區塊；namespace 可定址的基本單位，其資料大小由使用中的格式決定。</dd></div><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.4.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, 文件頁 76, PDF 頁 76</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>DSTOS/DSTCS</td><td>current state/progress</td><td>DSTOS=0 時忽略 percentage</td></tr><tr><td>DSTR=7h + SEGN</td><td>已知第一個 failed segment</td><td>其他 DSTR 忽略 SEGN</td></tr><tr><td>FVLD + FLBA</td><td>其中一個 failing LBA</td><td>不是所有失敗 LBA 清單</td></tr><tr><td>POH + STCT/STC</td><td>failure context</td><td>仍需 validity bits</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>SEGN</dt><dd>Segment Number，只有 DSTR=7h 時指出第一個失敗 diagnostic segment。</dd></div><div><dt>POH</dt><dd>Power On Hours，self-test result 建立時累積的 power-on hours，不含指定 low-power 時間。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.08">03.08.</span>完整 log 是 564 bytes=141 dwords，因此 NUMD=140=008Ch。LSP=0、RAE=0 時 CDW10=008C0006h。若 RDS1.DSTS=17h，high nibble 1h 表示 short test，low nibble 7h 表示已知 failed segment；此時才讀 SEGN。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NUMD</dt><dd>Number of Dwords，0's-based transfer dword count；實際 bytes = (NUMD + 1) × 4。</dd></div><div><dt>LSP</dt><dd>Log Specific Field，意義由所選 log page 定義的 command selector。</dd></div><div><dt>RAE</dt><dd>Retain Asynchronous Event，Get Log Page 是否保留相關 asynchronous event 的 selector。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:BASEDIAGMEM-FIG-111 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-111"><summary>NVM Figure 111 · Self-test Results Data Structure</summary>
<!-- claim:BASEDIAGMEM-FIG-111-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.09">03.09.</span>Figure 111〈Self-test Results Data Structure〉：定義〈Self-test Results Data Structure〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.4.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, Figure 111, 文件頁 76, PDF 頁 76</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>logical block</dt><dd>邏輯區塊；namespace 可定址的基本單位，其資料大小由使用中的格式決定。</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-218 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-218"><summary>Base Figure 218 · Device Self-test Log Page</summary>
<!-- claim:BASEDIAGMEM-FIG-218-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.10">03.10.</span>Figure 218〈Device Self-test Log Page〉：把〈Device Self-test Log Page〉連到 self-test、host memory、doorbell 或 vendor command 的工程邊界。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, Figure 218, 文件頁 230, PDF 頁 256</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-219 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-219"><summary>Base Figure 219 · Self-test Result Data Structure</summary>
<!-- claim:BASEDIAGMEM-FIG-219-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.11">03.11.</span>Figure 219〈Self-test Result Data Structure〉：定義〈Self-test Result Data Structure〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, Figure 219, 文件頁 231-232, PDF 頁 257-258</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>VDINFO</dt><dd>Valid Diagnostic Information，分別 gate NSID、FLBA、SCT 與 SC 的 validity bitmap。</dd></div><div><dt>POH</dt><dd>Power On Hours，self-test result 建立時累積的 power-on hours，不含指定 low-power 時間。</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-700 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-700"><summary>Base Figure 700 · Example Device Self-test Operation (Informative)</summary>
<!-- claim:BASEDIAGMEM-FIG-700-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.12">03.12.</span>Figure 700〈Example Device Self-test Operation (Informative)〉：定義〈Example Device Self-test Operation (Informative)〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §8.1.8</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.8, Figure 700, 文件頁 615, PDF 頁 641</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-701 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-701"><summary>Base Figure 701 · Format NVM command Aborting a Device Self-Test Operation</summary>
<!-- claim:BASEDIAGMEM-FIG-701-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.13">03.13.</span>Figure 701〈Format NVM command Aborting a Device Self-Test Operation〉：定義〈Format NVM command Aborting a Device Self-Test Operation〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §8.1.8.1-8.1.8.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, Figure 701, 文件頁 616, PDF 頁 642</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-203 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-203"><summary>Base Figure 203 · Get Log Page - Data Pointer</summary>
<!-- claim:BASEDIAGMEM-FIG-203-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.14">03.14.</span>Figure 203〈Get Log Page - Data Pointer〉：把〈Get Log Page - Data Pointer〉連到 self-test、host memory、doorbell 或 vendor command 的工程邊界。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 203, 文件頁 213, PDF 頁 239</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>DPTR</dt><dd>Data Pointer，SQE 中指出 command data buffer 的欄位。</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-204 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-204"><summary>Base Figure 204 · Get Log Page - Command Dword 10</summary>
<!-- claim:BASEDIAGMEM-FIG-204-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.15">03.15.</span>Figure 204〈Get Log Page - Command Dword 10〉：定義 Get Log Page 在 CDW10 的 command-specific 欄位。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 204, 文件頁 213, PDF 頁 239</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NUMDL</dt><dd>Number of Dwords Lower，Get Log Page 的 NUMD 低 16 bits。</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-205 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-205"><summary>Base Figure 205 · Get Log Page - Command Dword 11</summary>
<!-- claim:BASEDIAGMEM-FIG-205-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.16">03.16.</span>Figure 205〈Get Log Page - Command Dword 11〉：定義 Get Log Page 在 CDW11 的 command-specific 欄位。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 205, 文件頁 214, PDF 頁 240</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NUMDU</dt><dd>Number of Dwords Upper，Get Log Page 的 NUMD 高 16 bits。</dd></div><div><dt>LSI</dt><dd>Log Specific Identifier，意義由所選 log page 定義的 identifier。</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-206 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-206"><summary>Base Figure 206 · Get Log Page - Command Dword 12</summary>
<!-- claim:BASEDIAGMEM-FIG-206-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.17">03.17.</span>Figure 206〈Get Log Page - Command Dword 12〉：定義 Get Log Page 在 CDW12 的 command-specific 欄位。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 206, 文件頁 214, PDF 頁 240</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>LPOL</dt><dd>Log Page Offset Lower，Get Log Page byte offset 的低 32 bits。</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-207 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-207"><summary>Base Figure 207 · Get Log Page - Command Dword 13</summary>
<!-- claim:BASEDIAGMEM-FIG-207-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.18">03.18.</span>Figure 207〈Get Log Page - Command Dword 13〉：定義 Get Log Page 在 CDW13 的 command-specific 欄位。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 207, 文件頁 214, PDF 頁 240</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>LPOU</dt><dd>Log Page Offset Upper，Get Log Page byte offset 的高 32 bits。</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-208 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-208"><summary>Base Figure 208 · Get Log Page - Command Dword 14</summary>
<!-- claim:BASEDIAGMEM-FIG-208-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.19">03.19.</span>Figure 208〈Get Log Page - Command Dword 14〉：定義 Get Log Page 在 CDW14 的 command-specific 欄位。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 208, 文件頁 214-215, PDF 頁 240-241</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>UIDX</dt><dd>UUID Index，指向 UUID List 位置的 index；0 表示未指定 UUID。</dd></div><div><dt>CSI</dt><dd>I/O Command Set Identifier；選擇 I/O 命令集，NVM Command Set 使用 00h。</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-209 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-209"><summary>Base Figure 209 · Get Log Page - Log Page Identifiers</summary>
<!-- claim:BASEDIAGMEM-FIG-209-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.20">03.20.</span>Figure 209〈Get Log Page - Log Page Identifiers〉：定義〈Get Log Page - Log Page Identifiers〉的識別碼組成或數值空間。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 209, 文件頁 215-216, PDF 頁 241-242</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NVM subsystem</dt><dd>NVM subsystem，包含 controller、port、namespace 與非揮發性儲存資源的 NVMe 系統邊界。</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-hmb-ownership-lifecycle"><h2 id="heading-hmb-ownership-lifecycle"><span class="section-number">04</span> HMB 記憶體的提供、使用與收回</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span>HMB 的 value 不在『給 controller 一塊 cache』這句話，而在 ownership protocol。Host 配置 pages 與 descriptor list，enable 成功後停止寫入；controller 使用並初始化；host 要回收時先 disable，直到 CQE posted 才重新取得修改權。</p>
<figure><figcaption><strong>Host Memory Buffer 的使用期間</strong></figcaption><ol class="flow-steps"><li>Host 配置記憶體，建立 descriptor list。</li><li>Host 透過 HMB Feature 將記憶體範圍提供給 controller。</li><li>啟用期間，host 維持描述的記憶體範圍有效。</li><li>停用並完成規格要求的交接後，host 才能回收記憶體。</li></ol><figcaption>記憶體屬於 host，但不能在 controller 仍可使用時提前回收。</figcaption></figure>

<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASEDIAGMEM-HMB-CAPABILITY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span>HMPRE=0 表示 HMB 不支援；非零時以 4 KiB units 表示 preferred size，HMMIN 表示 minimum request。HMMINDS 與 HMMAXD 是 descriptor 限制。即使 host 無法提供 HMB，controller 仍必須（shall）正常運作。</p><dl class="term-note" aria-label="本段名詞"><div><dt>HMMINDS</dt><dd>Host Memory Buffer Minimum Descriptor Entry Size，每個可用 descriptor 的最低 4 KiB-unit 大小。</dd></div><div><dt>HMMAXD</dt><dd>Host Memory Maximum Descriptor Entries，controller 可使用的 descriptor entry 上限。</dd></div><div><dt>HMMIN</dt><dd>Host Memory Buffer Minimum Size，以 4 KiB units 回報 controller 要求的最低大小。</dd></div><div><dt>HMPRE</dt><dd>Host Memory Buffer Preferred Size，以 4 KiB units 回報 controller 偏好的配置大小。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.14.2.1, 8.2.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.2.4, 文件頁 357, 362, 744, PDF 頁 383, 388, 770</p></details>
<!-- claim:BASEDIAGMEM-HMB-SEQUENCE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.03">04.03.</span>HMB 已 enable 時再次送 EHM=1 必須以 Command Sequence Error 中止；尚未 enable 時送 EHM=0 則成功但不做事。disable completion 前 controller 應取回所需資料；CQE 被 posted 後才表示 host 可安全修改或回收 buffer。</p><dl class="term-note" aria-label="本段名詞"><div><dt>EHM</dt><dd>Enable Host Memory，啟用或停用 controller 使用 HMB 的 bit。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 文件頁 515-516, PDF 頁 541-542</p></details>
<!-- claim:BASEDIAGMEM-HMB-SURPRISE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.04">04.04.</span>使用 HMB 時發生 surprise removal，controller 必須（shall）確保不造成 data loss 或 data corruption。這不代表 HMB 內容本身具有持久性，而是裝置不得把內部正確性依賴在 host 一定能先走正常 release 流程。</p><details class="source-note"><summary>來源：Base 2.4 §8.2.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.2.4, 文件頁 744, PDF 頁 770</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>Before enable</td><td>host owns and initializes descriptors</td><td>validate alignment/count</td></tr><tr><td>After enable CQE</td><td>controller exclusive use</td><td>host shall not write</td></tr><tr><td>Disable in flight</td><td>controller may still retrieve data</td><td>host still waits</td></tr><tr><td>After disable CQE</td><td>host may modify/reclaim</td><td>record fence timestamp</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.05">04.05.</span>如果 driver 在送出 EHM=0 後、CQE 到達前就解除 DMA mapping，controller 仍可能依規格取回必要資料；這是 use-after-unmap。正確 fence 是 disable completion，而不是 SQ tail doorbell write。</p><dl class="term-note" aria-label="本段名詞"><div><dt>SQ</dt><dd>Submission Queue，主機放入命令的提交佇列。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:BASEDIAGMEM-FIG-552 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-552"><summary>Base Figure 552 · Host Memory Buffer - Completion Queue Entry Dword 0</summary>
<!-- claim:BASEDIAGMEM-FIG-552-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.06">04.06.</span>Figure 552〈Host Memory Buffer - Completion Queue Entry Dword 0〉：呈現〈Host Memory Buffer - Completion Queue Entry Dword 0〉中的 queue 或 command 關係。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 552, 文件頁 518-519, PDF 頁 544-545</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>HMNARE</dt><dd>Host Memory Non-operational Access Restriction Enable，配置 non-operational HMB access policy 的 bit。</dd></div><div><dt>HMNAR</dt><dd>Host Memory Non-operational Access Restricted，回報 restriction 此刻是否實際生效的 state bit。</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-553 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-553"><summary>Base Figure 553 · Host Memory Buffer - Attributes Data Structure</summary>
<!-- claim:BASEDIAGMEM-FIG-553-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.07">04.07.</span>Figure 553〈Host Memory Buffer - Attributes Data Structure〉：定義〈Host Memory Buffer - Attributes Data Structure〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 553, 文件頁 519, PDF 頁 545</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>HMDLEC</dt><dd>Host Memory Descriptor List Entry Count，HMDL 中有效 entries 的數量。</dd></div><div><dt>HSIZE</dt><dd>Host Memory Buffer Size，以 CC.MPS memory-page units 表示的 HMB 總大小。</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-hmb-command-math"><h2 id="heading-hmb-command-math"><span class="section-number">05</span> HMB 的描述子、大小與位址</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span>HSIZE、BSIZE 與 BADD 都依 CC.MPS；HMPRE／HMMIN／HMMINDS 則依 4 KiB units。兩套 unit 不能混用。HMDL 本身要 16-byte aligned，entries 固定 16 bytes；HMDLEC 是 entry count，不是 0's-based，也不是 byte length。</p><dl class="term-note" aria-label="本段名詞"><div><dt>0's-based</dt><dd>0's-based encoding，以 0 表示實際數量 1；依欄位換算公式通常是欄位值加 1。</dd></div><div><dt>HMDLEC</dt><dd>Host Memory Descriptor List Entry Count，HMDL 中有效 entries 的數量。</dd></div><div><dt>BSIZE</dt><dd>Buffer Size，HMB descriptor 中以 CC.MPS pages 表示的連續範圍長度。</dd></div><div><dt>HSIZE</dt><dd>Host Memory Buffer Size，以 CC.MPS memory-page units 表示的 HMB 總大小。</dd></div><div><dt>BADD</dt><dd>Buffer Address，HMB descriptor 中依 CC.MPS 對齊的 memory-page address。</dd></div><div><dt>HMDL</dt><dd>Host Memory Descriptor List，連續存放 16-byte HMB descriptors 的 host-memory array。</dd></div><div><dt>MPS</dt><dd>Memory Page Size，controller 使用的 memory page 大小設定；影響 queue address 與 PRP 對齊。</dd></div><div><dt>CC</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASEDIAGMEM-HMB-SET-COMMAND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.02">05.02.</span>Set Features 使用 FID=0Dh；CDW11 放 EHM、MR、HMNARE，CDW12 放 HSIZE，CDW13／14 組成 64-bit HMDL address，CDW15 是 HMDLEC。HMDL address 必須 16-byte aligned；HMDLEC=0 必須回 Invalid Field in Command。</p><dl class="term-note" aria-label="本段名詞"><div><dt>HMDL</dt><dd>Host Memory Descriptor List，連續存放 16-byte HMB descriptors 的 host-memory array。</dd></div><div><dt>FID</dt><dd>Feature Identifier；指定要讀取或設定哪一項 Feature 的編號。</dd></div><div><dt>MR</dt><dd>Memory Return，表示 host 歸還完全相同的舊 HMB size、addresses、descriptors 與 contents。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30, 5.2.30.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, 5.2.30.2.3, 文件頁 456-459, 516-518, PDF 頁 482-485, 542-544</p></details>
<!-- claim:BASEDIAGMEM-HMB-DESCRIPTORS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.03">05.03.</span>HMDL 是連續的 16-byte descriptor array；每個 entry 的 BADD 必須依 CC.MPS memory page size 對齊，BSIZE 以相同 page units 表示連續長度。BSIZE=0 的 entry 由 controller 忽略；HSIZE 應與可用 descriptors 的 page 數相符。</p><dl class="term-note" aria-label="本段名詞"><div><dt>BSIZE</dt><dd>Buffer Size，HMB descriptor 中以 CC.MPS pages 表示的連續範圍長度。</dd></div><div><dt>BADD</dt><dd>Buffer Address，HMB descriptor 中依 CC.MPS 對齊的 memory-page address。</dd></div><div><dt>MPS</dt><dd>Memory Page Size，controller 使用的 memory page 大小設定；影響 queue address 與 PRP 對齊。</dd></div><div><dt>CC</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 文件頁 517-518, PDF 頁 543-544</p></details>
<!-- claim:BASEDIAGMEM-HMB-NUMERIC -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.04">05.04.</span>說明性範例：CC.MPS=0 代表 4 KiB page；HSIZE=64 代表 256 KiB。若 HMDL=00000012_34567000h、HMDLEC=2，CDW13=34567000h、CDW14=00000012h、CDW15=00000002h。兩個 descriptor 各 BSIZE=32 pages 時，合計正好 64 pages。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 文件頁 516-518, PDF 頁 542-544</p></details>
<!-- claim:BASEDIAGMEM-HMB-GET -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.05">05.05.</span>Get Features 使用 FID=0Dh；SEL≠supported-capabilities 成功時，CQE.DW0 回 EHM、HMNARE、HMNAR，data buffer 回 4 KiB Attributes data structure，包括 HSIZE、HMDL address 與 HMDLEC。『已啟用』與『目前正在限制 access』是不同狀態。</p><dl class="term-note" aria-label="本段名詞"><div><dt>HMNAR</dt><dd>Host Memory Non-operational Access Restricted，回報 restriction 此刻是否實際生效的 state bit。</dd></div><div><dt>SEL</dt><dd>Select，Get Features 用來選 current、default、saved 或 supported-capabilities view 的欄位。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.12, 5.2.30.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, 5.2.30.2.3, 文件頁 209-212, 518-519, PDF 頁 235-238, 544-545</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>HMPRE/HMMIN</td><td>4 KiB units</td><td>capability request</td></tr><tr><td>HSIZE/BSIZE</td><td>CC.MPS units</td><td>configured memory</td></tr><tr><td>HMDL address</td><td>16-byte aligned</td><td>CDW13 low + CDW14 high</td></tr><tr><td>BADD</td><td>CC.MPS aligned</td><td>BSIZE=0 entry ignored</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="05.06">05.06.</span>CC.MPS=0、HSIZE=64 時是 256 KiB。HMDL=00000012_34567000h、HMDLEC=2，故 CDW13=34567000h、CDW14=00000012h、CDW15=2。兩個 BSIZE=32 的 ranges 各 128 KiB，合計 256 KiB。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:BASEDIAGMEM-FIG-546 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-546"><summary>Base Figure 546 · Host Memory Buffer - Command Dword 12</summary>
<!-- claim:BASEDIAGMEM-FIG-546-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.07">05.07.</span>Figure 546〈Host Memory Buffer - Command Dword 12〉：定義 Host Memory Buffer 在 CDW12 的 command-specific 欄位。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 546, 文件頁 517, PDF 頁 543</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CC.MPS units</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.MPS units 進一步指定其中的 MPS units 子欄位。</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-547 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-547"><summary>Base Figure 547 · Host Memory Buffer - Command Dword 13</summary>
<!-- claim:BASEDIAGMEM-FIG-547-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.08">05.08.</span>Figure 547〈Host Memory Buffer - Command Dword 13〉：定義 Host Memory Buffer 在 CDW13 的 command-specific 欄位。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 547, 文件頁 517, PDF 頁 543</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-548 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-548"><summary>Base Figure 548 · Host Memory Buffer - Command Dword 14</summary>
<!-- claim:BASEDIAGMEM-FIG-548-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.09">05.09.</span>Figure 548〈Host Memory Buffer - Command Dword 14〉：定義 Host Memory Buffer 在 CDW14 的 command-specific 欄位。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 548, 文件頁 517, PDF 頁 543</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-549 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-549"><summary>Base Figure 549 · Host Memory Buffer - Command Dword 15</summary>
<!-- claim:BASEDIAGMEM-FIG-549-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.10">05.10.</span>Figure 549〈Host Memory Buffer - Command Dword 15〉：定義 Host Memory Buffer 在 CDW15 的 command-specific 欄位。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 549, 文件頁 518, PDF 頁 544</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-550 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-550"><summary>Base Figure 550 · Host Memory Buffer - Host Memory Descriptor List</summary>
<!-- claim:BASEDIAGMEM-FIG-550-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.11">05.11.</span>Figure 550〈Host Memory Buffer - Host Memory Descriptor List〉：定義〈Host Memory Buffer - Host Memory Descriptor List〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 550, 文件頁 518, PDF 頁 544</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-551 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-551"><summary>Base Figure 551 · Host Memory Buffer - Host Memory Buffer Descriptor Entry</summary>
<!-- claim:BASEDIAGMEM-FIG-551-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.12">05.12.</span>Figure 551〈Host Memory Buffer - Host Memory Buffer Descriptor Entry〉：定義〈Host Memory Buffer - Host Memory Buffer Descriptor Entry〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, Figure 551, 文件頁 518, PDF 頁 544</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CC.MPS alignment</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.MPS alignment 進一步指定其中的 MPS alignment 子欄位。</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-197 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-197"><summary>Base Figure 197 · Get Features - Data Pointer</summary>
<!-- claim:BASEDIAGMEM-FIG-197-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.13">05.13.</span>Figure 197〈Get Features - Data Pointer〉：把〈Get Features - Data Pointer〉連到 self-test、host memory、doorbell 或 vendor command 的工程邊界。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 197, 文件頁 209, PDF 頁 235</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-198 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-198"><summary>Base Figure 198 · Get Features - Command Dword 10</summary>
<!-- claim:BASEDIAGMEM-FIG-198-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.14">05.14.</span>Figure 198〈Get Features - Command Dword 10〉：定義 Get Features 在 CDW10 的 command-specific 欄位。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 198, 文件頁 209-210, PDF 頁 235-236</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>SEL</dt><dd>Select，Get Features 用來選 current、default、saved 或 supported-capabilities view 的欄位。</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-200 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-200"><summary>Base Figure 200 · Feature Identifiers for Get Features</summary>
<!-- claim:BASEDIAGMEM-FIG-200-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.15">05.15.</span>Figure 200〈Feature Identifiers for Get Features〉：定義〈Feature Identifiers for Get Features〉的識別碼組成或數值空間。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 200, 文件頁 210-211, PDF 頁 236-237</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-463 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-463"><summary>Base Figure 463 · Set Features - Data Pointer</summary>
<!-- claim:BASEDIAGMEM-FIG-463-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.16">05.16.</span>Figure 463〈Set Features - Data Pointer〉：把〈Set Features - Data Pointer〉連到 self-test、host memory、doorbell 或 vendor command 的工程邊界。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.30</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 463, 文件頁 456, PDF 頁 482</p></details>

</details>
<!-- figure-table:BASEDIAGMEM-FIG-464 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-464"><summary>Base Figure 464 · Set Features - Command Dword 10</summary>
<!-- claim:BASEDIAGMEM-FIG-464-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.17">05.17.</span>Figure 464〈Set Features - Command Dword 10〉：定義 Set Features 在 CDW10 的 command-specific 欄位。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.30</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 464, 文件頁 457, PDF 頁 483</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>SV</dt><dd>Save，Set Features 要求 controller 同時保存所設定 value 的 bit。</dd></div></dl>
</details>
<!-- figure-table:BASEDIAGMEM-FIG-466 -->
<details class="field-note" id="figure-BASEDIAGMEM-FIG-466"><summary>Base Figure 466 · Feature Identifiers for Set Features</summary>
<!-- claim:BASEDIAGMEM-FIG-466-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.18">05.18.</span>Figure 466〈Feature Identifiers for Set Features〉：定義〈Feature Identifiers for Set Features〉的識別碼組成或數值空間。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.30</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 466, 文件頁 457-459, PDF 頁 483-485</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-hmb-reset-power"><h2 id="heading-hmb-reset-power"><span class="section-number">06</span> HMB 在電源轉換與 Reset 後的狀態</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.01">06.01.</span>HMNARE 是 access policy，HMNAR 是此刻 state；MR 則描述 reset／RTD3 後是否歸還完全相同的舊內容。這三者不能互換。Controller Level Reset 會讓 controller 丟失 HMB assignment，RTD3 前應先 release，而 non-operational restriction 只限制特定 state 下的 access。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASEDIAGMEM-HMB-NONOP -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.02">06.02.</span>HMNARE 只有 Identify.CTRATT.HMBR=1 時可啟用。HMNARE 是 policy，HMNAR 是 controller 此刻是否真的因 non-operational state 而被限制；Admin commands 與其啟動的 background operations 有明文例外。NOPPME 不改變這項 HMB restriction。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NOPPME</dt><dd>Non-Operational Power State Permissive Mode Enable，控制 controller background work 能否暫時超過 non-operational power limit。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 文件頁 516-519, PDF 頁 542-545</p></details>
<!-- claim:BASEDIAGMEM-HMB-RESET-RTD3 -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.03">06.03.</span>HMB 不會跨 Controller Level Reset 保存在 controller。reset 後 host 應重新提供資源；若 MR=1 表示歸還先前內容，size、descriptor-list address、descriptor-list contents 與 HMB contents 必須完全相同。RTD3 前宜先 disable，恢復後再依是否保留內容選 MR。</p><details class="source-note"><summary>來源：Base 2.4 §8.2.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.2.4, 文件頁 744, PDF 頁 770</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>HMNARE</td><td>configured policy</td><td>需要 CTRATT.HMBR</td></tr><tr><td>HMNAR</td><td>current restriction state</td><td>可能因 operational state 而為 0</td></tr><tr><td>MR=1</td><td>return identical old HMB</td><td>size/address/list/content 全相同</td></tr><tr><td>MR=0</td><td>new undefined contents</td><td>controller 重新初始化</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="06.04">06.04.</span>resume 後 allocator 給了相同 pages 但 HMDL 搬到新 address，就不能設 MR=1，因為 descriptor-list address 也必須完全相同。此時以 MR=0 當新 allocation 重新 enable。</p></aside>
</section>
<section class="lesson" id="module-encoded-boundary-safety"><h2 id="heading-encoded-boundary-safety"><span class="section-number">07</span> DSTRD、NDT 與 NDM 的單位</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.01">07.01.</span>software emulator 與 vendor command passthrough 都在處理 untrusted encoded values。DSTRD 要套 2^(2+x) 才是 bytes；NDT／NDM 已是實際 dword count，要乘 4、不能再加 1。正確公式不同，但目的相同：在 MMIO 或 DMA 前先證明 address 與 length。</p><dl class="term-note" aria-label="本段名詞"><div><dt>MMIO</dt><dd>Memory-Mapped I/O，以 CPU memory access 形式讀寫裝置 register。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASEDIAGMEM-VENDOR-FORMAT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.02">07.02.</span>Figure 94 保留 common CDW0、NSID、metadata/data pointers 與 CDW12-CDW15，並把 CDW10／11 定義成 NDT／NDM。若 command 不使用 NSID，必須清為 0；invalid NSID 在使用時必須回 Invalid Namespace or Format，inactive NSID 行為仍是 vendor specific。</p><dl class="term-note" aria-label="本段名詞"><div><dt>metadata</dt><dd>隨 logical block 儲存的附加資料，可包含資料保護資訊，也可有其他用途。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.1.1, 8.1.29</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 8.1.29, 文件頁 143, 733, PDF 頁 169, 759</p></details>
<!-- claim:BASEDIAGMEM-VENDOR-LENGTH -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.03">07.03.</span>NDT 與 NDM 是實際 dword 數，不是 0's-based。NDT=00000100h 代表 256 dwords=1024 bytes；driver 可用 NDT／NDM 驗證 application buffer，避免 data 或 metadata transfer overflow。是否支援 standard format 仍先由 VSCF／SNVSCF gate。</p><dl class="term-note" aria-label="本段名詞"><div><dt>metadata</dt><dd>隨 logical block 儲存的附加資料，可包含資料保護資訊，也可有其他用途。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.1.1, 8.1.29</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 8.1.29, 文件頁 143, 733, PDF 頁 169, 759</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>DSTRD</td><td>2^(2+x) bytes</td><td>0→4 B；4→64 B</td></tr><tr><td>NDT</td><td>value×4 data bytes</td><td>不是 0's-based</td></tr><tr><td>NDM</td><td>value×4 metadata bytes</td><td>獨立 buffer bound</td></tr><tr><td>VSCF/SNVSCF</td><td>format gate</td><td>Admin 與 I/O 分開</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="07.04">07.04.</span>emulator 設 DSTRD=4 得 64-byte stride，可讓每個 doorbell 使用離散 cacheline。vendor command 的 NDT=0100h 則是 256 dwords=1024 bytes，不是 1028 bytes。兩者都要同時保存 raw encoded value 與 interpret the fields bytes。</p></aside>
</section>
<section id="additional-details"><h2 id="further-mechanisms">補充機制與資料格式</h2>
<!-- claim:BASEDIAGMEM-SELFTEST-BACKGROUND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.01">08.01.</span>Device Self-test 是由 vendor-specific segments 組成的背景工作。若另一個 command 必須暫停測試才能處理，controller 必須（shall）依序 suspend self-test、處理並完成該 command、再 resume self-test；同時可處理哪些 command 則由 vendor 決定。</p><details class="source-note"><summary>來源：Base 2.4 §8.1.8</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.8, 文件頁 614, PDF 頁 640</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-TIMING -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.02">08.02.</span>short operation 應（should）在兩分鐘內完成，且 Controller Level Reset 會中止；extended operation 應在 EDSTT 內完成，必須跨 Controller Level Reset 與 power restoration 持續並於之後 resume。兩者不能共用同一套 reset 預期。</p><details class="source-note"><summary>來源：Base 2.4 §8.1.8.1-8.1.8.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, 文件頁 615-616, PDF 頁 641-642</p></details>
<!-- claim:BASEDIAGMEM-SELFTEST-ABORTS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.03">08.03.</span>short 與 extended 都會被適用的 Format NVM、sanitize start 或 STC=Fh 中止，namespace 從 inventory 移除時則可能（may）中止。Figure 701 顯示 Format 的 NSID 與 secure-erase 選項會改變是否必須中止，不能只看 opcode。</p><details class="source-note"><summary>來源：Base 2.4 §8.1.8.1-8.1.8.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, 文件頁 615-616, PDF 頁 641-642</p></details>
</section>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:base-self-test-hmb-emulation-selftest-progress -->
<details class="review-question" id="qa-base-self-test-hmb-emulation-selftest-progress"><summary>1. Device Self-test 啟動命令成功後，如何知道測試是否還在執行？</summary>
<div data-qa-answer="base-self-test-hmb-emulation-selftest-progress"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="09.01">09.01.</span>啟動 completion 不包含整個測試的最終結果。Device Self-test log 的 current operation 與 completion percentage 描述目前進度；結果紀錄則用於已結束的測試。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 201, PDF 頁 227</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-230, PDF 頁 255-256</p>
</details></details>
<!-- qa:base-self-test-hmb-emulation-flba-valid -->
<details class="review-question" id="qa-base-self-test-hmb-emulation-flba-valid"><summary>2. Self-test result 中 FLBA 看起來是合理地址，就一定可以當作失敗位置嗎？</summary>
<div data-qa-answer="base-self-test-hmb-emulation-flba-valid"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="09.02">09.02.</span>要先檢查對應的 validity bit；未宣告有效時不能依數值推論。即使有效，也可能只描述多個失敗 logical blocks 中的一個，並非完整範圍。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 231-232, PDF 頁 257-258</p>
<p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, 文件頁 76, PDF 頁 76</p>
</details></details>
<!-- qa:base-self-test-hmb-emulation-hmb-ownership -->
<details class="review-question" id="qa-base-self-test-hmb-emulation-hmb-ownership"><summary>3. HMB 記憶體原本由 host 配置，host 是否能在 controller 使用時直接重用？</summary>
<div data-qa-answer="base-self-test-hmb-emulation-hmb-ownership"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="09.03">09.03.</span>不能。提供給 controller 的期間必須維持記憶體與描述資訊有效；應完成規定的停用及交還程序後才回收。實體配置者與目前可使用者是不同概念。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 8.2.4, 文件頁 515-516, 744, PDF 頁 541-542, 770</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 文件頁 515-516, PDF 頁 541-542</p>
</details></details>
<!-- qa:base-self-test-hmb-emulation-hmb-size -->
<details class="review-question" id="qa-base-self-test-hmb-emulation-hmb-size"><summary>4. 知道 HMB descriptor 有 4 筆，就知道總容量了嗎？</summary>
<div data-qa-answer="base-self-test-hmb-emulation-hmb-size"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="09.04">09.04.</span>還需要每筆 buffer size 和 page size。Descriptor 數只計算分段數；總容量是各段 page 數乘 page size 後加總，並需符合 HSIZE 與能力限制。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 文件頁 517-518, PDF 頁 543-544</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 文件頁 516-518, PDF 頁 542-544</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express Base Specification, Revision 2.4</p><p>NVM Express NVM Command Set Specification, Revision 1.3</p></details></footer>
</div>
