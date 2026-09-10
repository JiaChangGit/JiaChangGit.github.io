---
permalink: /nvme/hmb-emulation-zh-tw/
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4：HMB、Doorbell Emulation 與 Vendor Commands"
date: 2026-09-11
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
[English]({% post_url 2026-09-11-nvme-base-hmb-emulation-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">這篇說明主機如何把記憶體提供給控制器，以及如何理解 doorbell 位址與廠商命令長度。共同問題是：哪一方可以使用這塊記憶體、何時可以收回，以及欄位中的數值究竟用什麼單位。</span></p>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>把主機記憶體借給控制器</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">HMB 的重點是記憶體使用權：如何提供、允許使用，以及何時能收回。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>HMB</dt><dd>Host Memory Buffer，由 host 配置並在 enable 期間交由 controller 專用的 volatile memory ranges。</dd></div></dl></article>
<article><span class="axis-number">02</span><h3>處理容量與生命週期</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">用容量換算理解描述項，再比較電源轉換和重設對記憶體使用的影響。</span></p></article>
<article><span class="axis-number">03</span><h3>讀懂另兩種編碼</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">Doorbell Emulation 與廠商命令分別用位址和長度算例說明；它們是另外的介面機制。</span></p></article>
</div>
<div class="overview-connections"><h3>把主軸連起來</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">HMB 的提供、使用與收回形成一個完整流程；電源轉換與 reset 會影響這個流程。Doorbell Emulation 與 Vendor Commands 另以位址和長度算例說明，不把它們當成 HMB 的必要步驟。</span></p>
</div>
</section>
<section class="lesson" id="module-hmb-ownership-lifecycle"><h2 id="heading-hmb-ownership-lifecycle"><span class="section-number">01</span> HMB 記憶體的提供、使用與收回</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">HMB 的 value 不在『給 controller 一塊 cache』這句話，而在 ownership protocol。Host 配置 pages 與 descriptor list，enable 成功後停止寫入；controller 使用並初始化；host 要回收時先 disable，直到 CQE posted 才重新取得修改權。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div></dl>
<figure><figcaption><strong>Host Memory Buffer 的使用期間</strong></figcaption><ol class="flow-steps"><li>Host 配置記憶體，建立 descriptor list。</li><li>Host 透過 HMB Feature 將記憶體範圍提供給 controller。</li><li>啟用期間，host 維持描述的記憶體範圍有效。</li><li>停用並完成規格要求的交接後，host 才能回收記憶體。</li></ol><figcaption>記憶體屬於 host，但不能在 controller 仍可使用時提前回收。</figcaption></figure>

<!-- claim:BASEHMB-HMB-CAPABILITY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">HMPRE=0 表示 HMB 不支援；非零時以 4 KiB units 表示 preferred size，HMMIN 表示 minimum request。HMMINDS 與 HMMAXD 是 descriptor 限制。即使 host 無法提供 HMB，controller 仍必須（shall）正常運作。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>HMMINDS</dt><dd>Host Memory Buffer Minimum Descriptor Entry Size，每個可用 descriptor 的最低 4 KiB-unit 大小。</dd></div><div><dt>HMMAXD</dt><dd>Host Memory Maximum Descriptor Entries，controller 可使用的 descriptor entry 上限。</dd></div><div><dt>HMMIN</dt><dd>Host Memory Buffer Minimum Size，以 4 KiB units 回報 controller 要求的最低大小。</dd></div><div><dt>HMPRE</dt><dd>Host Memory Buffer Preferred Size，以 4 KiB units 回報 controller 偏好的配置大小。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.14.2.1, 8.2.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.2.4, 文件頁 357, 362, 744, PDF 頁 383, 388, 770</p></details>
<div class="table-wrap"><table><caption>HMB 記憶體的提供、使用與收回</caption><thead><tr><th scope="col">HMB 使用階段</th><th scope="col">哪一方可以使用記憶體</th><th scope="col">進入下一階段的條件</th></tr></thead><tbody><tr><td>啟用之前</td><td>主機配置記憶體並初始化描述子</td><td>先核對位址對齊和描述子數量</td></tr><tr><td>啟用命令完成後</td><td>控制器專用；主機不得修改</td><td>host shall not write</td></tr><tr><td>停用命令尚未完成</td><td>控制器仍可取回必要資料</td><td>主機仍須等停用完成</td></tr><tr><td>停用命令完成後</td><td>主機可修改或收回記憶體</td><td>停用完成後才可修改或回收</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">把啟用及停用放在時間線上：啟用完成後，控制器可使用主機提供的區域；送出 EHM=0 只是要求停止使用。在停用完成回報到達之前，這些區域仍保持有效。停用完成後，主機才可以修改或回收。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>EHM</dt><dd>Enable Host Memory，啟用或停用 controller 使用 HMB 的 bit。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-hmb-command-math"><h2 id="heading-hmb-command-math"><span class="section-number">02</span> HMB 的描述子、大小與位址</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">HSIZE、BSIZE 與 BADD 都依 CC.MPS；HMPRE／HMMIN／HMMINDS 則依 4 KiB units。兩套 unit 不能混用。HMDL 本身要 16-byte aligned，entries 固定 16 bytes；HMDLEC 是 entry count，不是 0's-based，也不是 byte length。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>0's-based</dt><dd>0's-based encoding，以 0 表示實際數量 1；依欄位換算公式通常是欄位值加 1。</dd></div><div><dt>HMDLEC</dt><dd>Host Memory Descriptor List Entry Count，HMDL 中有效 entries 的數量。</dd></div><div><dt>BSIZE</dt><dd>Buffer Size，HMB descriptor 中以 CC.MPS pages 表示的連續範圍長度。</dd></div><div><dt>HSIZE</dt><dd>Host Memory Buffer Size，以 CC.MPS memory-page units 表示的 HMB 總大小。</dd></div><div><dt>BADD</dt><dd>Buffer Address，HMB descriptor 中依 CC.MPS 對齊的 memory-page address。</dd></div><div><dt>HMDL</dt><dd>Host Memory Descriptor List，連續存放 16-byte HMB descriptors 的 host-memory array。</dd></div><div><dt>MPS</dt><dd>Memory Page Size，controller 使用的 memory page 大小設定；影響 queue address 與 PRP 對齊。</dd></div><div><dt>CC</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。</dd></div></dl>
<!-- claim:BASEHMB-HMB-SET-COMMAND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">Set Features 使用 FID=0Dh；CDW11 放 EHM、MR、HMNARE，CDW12 放 HSIZE，CDW13／14 組成 64-bit HMDL address，CDW15 是 HMDLEC。HMDL address 必須 16-byte aligned；HMDLEC=0 必須回 Invalid Field in Command。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>HMNARE</dt><dd>Host Memory Non-operational Access Restriction Enable，配置 non-operational HMB access policy 的 bit。</dd></div><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div><div><dt>FID</dt><dd>Feature Identifier；指定要讀取或設定哪一項 Feature 的編號。</dd></div><div><dt>MR</dt><dd>Memory Return，表示 host 歸還完全相同的舊 HMB size、addresses、descriptors 與 contents。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30, 5.2.30.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, 5.2.30.2.3, 文件頁 456-459, 516-518, PDF 頁 482-485, 542-544</p></details>
<div class="table-wrap"><table><caption>HMB 的描述子、大小與位址</caption><thead><tr><th scope="col">大小或位址欄位</th><th scope="col">使用的單位或對齊</th><th scope="col">描述的資源</th></tr></thead><tbody><tr><td>HMPRE/HMMIN</td><td>4 KiB units</td><td>capability request</td></tr><tr><td>HSIZE/BSIZE</td><td>CC.MPS units</td><td>configured memory</td></tr><tr><td>HMDL address</td><td>16-byte aligned</td><td>CDW13 low + CDW14 high</td></tr><tr><td>BADD</td><td>CC.MPS aligned</td><td>BSIZE=0 entry ignored</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">CC.MPS=0、HSIZE=64 時是 256 KiB。HMDL=00000012_34567000h、HMDLEC=2，故 CDW13=34567000h、CDW14=00000012h、CDW15=2。兩個 BSIZE=32 的 ranges 各 128 KiB，合計 256 KiB。</span></p></aside>
</section>
<section class="lesson" id="module-hmb-reset-power"><h2 id="heading-hmb-reset-power"><span class="section-number">03</span> HMB 在電源轉換與 Reset 後的狀態</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">HMNARE 是 access policy，HMNAR 是此刻 state；MR 則描述 reset／RTD3 後是否歸還完全相同的舊內容。這三者不能互換。Controller Level Reset 會讓 controller 丟失 HMB assignment，RTD3 前應先 release，而 non-operational restriction 只限制特定 state 下的 access。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>HMNAR</dt><dd>Host Memory Non-operational Access Restricted，回報 restriction 此刻是否實際生效的 state bit。</dd></div></dl>
<!-- claim:BASEHMB-HMB-NONOP -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span><span class="paragraph-text">HMNARE 只有 Identify.CTRATT.HMBR=1 時可啟用。HMNARE 是 policy，HMNAR 是 controller 此刻是否真的因 non-operational state 而被限制；Admin commands 與其啟動的 background operations 有明文例外。NOPPME 不改變這項 HMB restriction。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NOPPME</dt><dd>Non-Operational Power State Permissive Mode Enable，控制 controller background work 能否暫時超過 non-operational power limit。</dd></div><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 文件頁 516-519, PDF 頁 542-545</p></details>
<div class="table-wrap"><table><caption>HMB 在電源轉換與 Reset 後的狀態</caption><thead><tr><th scope="col">HMB 狀態或設定</th><th scope="col">描述的限制或記憶體來源</th><th scope="col">何時可以採用這個值</th></tr></thead><tbody><tr><td>HMNARE</td><td>設定的使用政策</td><td>需要 CTRATT.HMBR</td></tr><tr><td>HMNAR</td><td>目前生效的限制狀態</td><td>可能因 operational state 而為 0</td></tr><tr><td>MR=1</td><td>交回符合相同條件的原有 HMB</td><td>size/address/list/content 全相同</td></tr><tr><td>MR=0</td><td>新提供的記憶體，內容尚未初始化</td><td>controller 重新初始化</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.03">03.03.</span><span class="paragraph-text">resume 後 allocator 給了相同 pages 但 HMDL 搬到新 address，就不能設 MR=1，因為 descriptor-list address 也必須完全相同。此時以 MR=0 當新 allocation 重新 enable。</span></p></aside>
</section>
<section class="lesson" id="module-encoded-boundary-safety"><h2 id="heading-encoded-boundary-safety"><span class="section-number">04</span> DSTRD、NDT 與 NDM 的單位</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">software emulator 與 vendor command passthrough 都在處理 untrusted encoded values。DSTRD 要套 2^(2+x) 才是 bytes；NDT／NDM 已是實際 dword count，要乘 4、不能再加 1。正確公式不同，但目的相同：在 MMIO 或 DMA 前先證明 address 與 length。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>DSTRD</dt><dd>Doorbell Stride，CAP 中決定相鄰 doorbell register 間距的欄位。</dd></div><div><dt>Dword</dt><dd>Dword（Double word）；32 bits，也就是 4 bytes。對比 word=16 bits；例如 zero-based dword count=3 代表 4 個 Dwords，也就是 16 bytes。</dd></div><div><dt>MMIO</dt><dd>Memory-Mapped I/O，以 CPU memory access 形式讀寫裝置 register。</dd></div><div><dt>NDM</dt><dd>Number of Dwords in Metadata Transfer，standard vendor-specific format 中的實際 metadata dword 數。</dd></div><div><dt>NDT</dt><dd>Number of Dwords in Data Transfer，standard vendor-specific format 中的實際 data dword 數。</dd></div></dl>
<!-- claim:BASEHMB-DOORBELL-STRIDE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">CAP.DSTRD 的實際間距是 2^(2+DSTRD) bytes。DSTRD=0／2／4 分別得到 4／16／64 bytes；software emulation 可用 64-byte stride 把 doorbells 分散到 cacheline，硬體 NVMe interface 的 expected value 是 0h。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express，主機與非揮發性記憶體子系統之間的介面規範家族。</dd></div><div><dt>CAP</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.4.1, 8.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, 8.2.3, 文件頁 56, 744, PDF 頁 82, 770</p></details>
<div class="table-wrap"><table><caption>DSTRD、NDT 與 NDM 的單位</caption><thead><tr><th scope="col">位址或長度欄位</th><th scope="col">換算公式</th><th scope="col">該值作用於哪個對象</th></tr></thead><tbody><tr><td>DSTRD</td><td>2^(2+x) bytes</td><td>0→4 B；4→64 B</td></tr><tr><td>NDT</td><td>value×4 data bytes</td><td>不是 0's-based</td></tr><tr><td>NDM</td><td>value×4 metadata bytes</td><td>獨立 buffer bound</td></tr><tr><td>VSCF/SNVSCF</td><td>格式選用條件</td><td>Admin 與 I/O 分開</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>metadata</dt><dd>隨 logical block 儲存的附加資料，可包含資料保護資訊，也可有其他用途。</dd></div><div><dt>SNVSCF</dt><dd>Same NVM Vendor Specific Command Format，ICSVSCC 中表示 I/O commands 是否使用 Figure 94 的 bit。</dd></div><div><dt>VSCF</dt><dd>Vendor Specific Command Format，AVSCC 中表示 Admin commands 是否使用 Figure 94 的 bit。</dd></div><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.03">04.03.</span><span class="paragraph-text">emulator 設 DSTRD=4 得 64-byte stride，可讓每個 doorbell 使用離散 cacheline。vendor command 的 NDT=0100h 則是 256 dwords=1024 bytes，不是 1028 bytes。兩者都要同時保存 raw encoded value 與 換算後的 byte 數。</span></p></aside>
</section>
<section id="spec-reading"><h2>接著打開 Spec 看什麼</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span><span class="paragraph-text">以下按概念列出閱讀位置。報告時先用上面的流程說明問題，再打開對應章節看欄位與完整條件。中文教學 HTML 另有本篇全部圖表的逐圖重點、案例與細節。</span></p>
<div class="table-wrap"><table><thead><tr><th scope="col">要說明的觀念</th><th scope="col">Spec 閱讀位置</th></tr></thead><tbody><tr><td>HMB 記憶體的提供、使用與收回</td><td>Base 2.4 §5.2.14.2.1, 8.2.4 · Base 2.4 §5.2.30.2.3, 8.2.4 · Base 2.4 §5.2.30.2.3 · Base 2.4 §8.2.4</td></tr><tr><td>HMB 的描述子、大小與位址</td><td>Base 2.4 §5.2.30, 5.2.30.2.3 · Base 2.4 §5.2.30.2.3 · Base 2.4 §5.2.12, 5.2.30.2.3</td></tr><tr><td>HMB 在電源轉換與 Reset 後的狀態</td><td>Base 2.4 §5.2.30.2.3 · Base 2.4 §8.2.4</td></tr><tr><td>DSTRD、NDT 與 NDM 的單位</td><td>Base 2.4 §3.1.4.1, 8.2.3 · Base 2.4 §5.2.14.2.1, 8.1.29 · Base 2.4 §4.1.1, 8.1.29</td></tr></tbody></table></div>
<a class="reading-link" href="/DOCS/nvme-spec-report/base-hmb-emulation/tutorial-zh-tw.html">開啟完整中文教學與逐圖解釋 →</a></section>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:base-hmb-emulation-1 -->
<details class="review-question" id="qa-base-hmb-emulation-1"><summary>1. HMB 記憶體原本由 host 配置，host 是否能在 controller 使用時直接重用？</summary>
<div data-qa-answer="base-hmb-emulation-1"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="06.01">06.01.</span><span class="paragraph-text">不能。提供給 controller 的期間必須維持記憶體與描述資訊有效；應完成規定的停用及交還程序後才回收。實體配置者與目前可使用者是不同概念。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 8.2.4, 文件頁 515-516, 744, PDF 頁 541-542, 770</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 文件頁 515-516, PDF 頁 541-542</p>
</details></details>
<!-- qa:base-hmb-emulation-2 -->
<details class="review-question" id="qa-base-hmb-emulation-2"><summary>2. 知道 HMB descriptor 有 4 筆，就知道總容量了嗎？</summary>
<div data-qa-answer="base-hmb-emulation-2"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="06.02">06.02.</span><span class="paragraph-text">還需要每筆 buffer size 和 page size。Descriptor 數只計算分段數；總容量是各段 page 數乘 page size 後加總，並需符合 HSIZE 與能力限制。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 文件頁 517-518, PDF 頁 543-544</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.2.3, 文件頁 516-518, PDF 頁 542-544</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
