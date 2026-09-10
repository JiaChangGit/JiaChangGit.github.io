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
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">韌體更新包含傳送映像、保存至 slot 與切換執行版本。這篇說明 Firmware Image Download、Firmware Commit 和 Firmware Slot Information 如何一起完成這件事，並分清楚每一步改變了什麼狀態。</span></p>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>能力與更新單位</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">確認可用 slots、寫入限制及下載片段的粒度。</span></p></article>
<article><span class="axis-number">02</span><h3>下載與啟用</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">理解映像範圍、Commit Action 與 reset 的關係。</span></p></article>
<article><span class="axis-number">03</span><h3>執行版本</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">以目前與預定 active slot 區分已保存和正在執行的版本。</span></p></article>
</div>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">Firmware slot 是保存韌體映像的位置；有版本字串不代表該映像正在執行。控制器的能力查詢、命令完成與 slot 資訊必須分別理解。</span></p>
<div class="overview-connections"><h3>把主軸連起來</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.03">00.03.</span><span class="paragraph-text">更新韌體可分成能力確認、映像傳輸、保存與啟用、結果確認。這個順序連接了 Identify 的能力資訊、Download 的長度與偏移、Commit 的選擇，以及 LID 03h 的目前與待啟用版本。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>LID 03h</dt><dd>Firmware Slot Information log page 的 identifier 03h。</dd></div><div><dt>LID</dt><dd>Log Page Identifier；指定要讀取哪一種 log page 的編號。</dd></div></dl>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.04">00.04.</span><span class="paragraph-text">本篇只以 Firmware Slot Information 完成更新結果的閱讀，不延伸成所有 log 的介紹。學完應能解釋為什麼下載成功還不等於新版本正在執行，並能用實際的分段長度與 slot 狀態走完一個例子。</span></p>
</div>
</section>
<section class="lesson" id="module-fw-capability-plan"><h2 id="heading-fw-capability-plan"><span class="section-number">01</span> 更新前的能力與限制</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">Firmware update 不是固定 command recipe。FRMW 決定 slot 與 activation 能力，FWUG 決定 download chunk 的 granularity／alignment，MTFA 與 MPTFAWR 決定 host 能等待多久，MDS／DID 則決定結果影響哪一組 controllers。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>MPTFAWR</dt><dd>Maximum Processing Time for Firmware Activation Without Reset，立即 activation 不需要 reset 時的最大處理時間。</dd></div><div><dt>FRMW</dt><dd>Firmware Updates，Identify Controller 中回報 slot 數、slot 1 read-only 與 activation 能力的欄位。</dd></div><div><dt>FWUG</dt><dd>Firmware Update Granularity，download portion 的 granularity／alignment 能力欄位。</dd></div><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div><div><dt>MTFA</dt><dd>Maximum Time for Firmware Activation，activation 可能暫停 command processing 的最長時間。</dd></div><div><dt>DID</dt><dd>Domain Identifier，辨識 NVM subsystem 內 domain 的 identifier。</dd></div><div><dt>MDS</dt><dd>Multiple Domain Subsystem，指出 NVM subsystem 是否包含多個 domains 的能力 bit。</dd></div></dl>
<!-- claim:BASEFWLOG-CAP-FRMW -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">FRMW 的 SMUD、FAWR、NOFS 與 FFSRO 分別表示重疊 update 偵測、免 reset activation、domain 支援的 slot 數（1 到 7）以及 slot 1 是否 read-only。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.14.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.1, 文件頁 354, PDF 頁 380</p></details>
<div class="table-wrap"><table><caption>更新前的能力與限制</caption><thead><tr><th scope="col">更新能力</th><th scope="col">決定哪項選擇</th><th scope="col">何時使用這項資訊</th></tr></thead><tbody><tr><td>FRMW</td><td>可用 slots、slot 1 read-only、activation 能力</td><td>選 FS 與 CA 前先讀</td></tr><tr><td>FWUG</td><td>download portion 的粒度與對齊</td><td>先換成 bytes，再切 image</td></tr><tr><td>MTFA／MPTFAWR</td><td>可能暫停與立即 activation 的時間界線</td><td>timeout 不可寫死</td></tr><tr><td>MDS／DID</td><td>firmware slots 的共享 domain</td><td>不可只用 PCI Function 當 scope</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>portion</dt><dd>傳輸分段；一次 firmware download 所送的一段連續資料。</dd></div><div><dt>CA</dt><dd>Commit Action，Firmware Commit 中選擇 replace、activate 與 reset policy 的欄位。</dd></div><div><dt>FS</dt><dd>Firmware Slot，Firmware Commit 中選擇目標 slot 的欄位。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">若 FWUG 依欄位換算為 4 KiB，12 KiB image 可切成三個 4 KiB portions；最後一筆不是任意長度的尾包。計畫還要先確認 slot 2 合法且不是 read-only，並依 activation path 選擇 timeout。</span></p></aside>
</section>
<section class="lesson" id="module-fw-download-geometry"><h2 id="heading-fw-download-geometry"><span class="section-number">02</span> Download 的長度、偏移與分段</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">Firmware Download 的 NUMD 是 zero-based 長度，OFST 是從 image 起點計算的 dword offset。用 index-offset 對比來讀：index 選哪個項目，offset 表示離起點多遠；兩個數值都不能脫離欄位定義換算。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>index-offset</dt><dd>index-offset 對比；index 選取項目，offset 計算位置。例如 Format Index=2 選第 2 個格式，而 OFST=256 表示從 image 起點位移 256 個 Dwords。</dd></div><div><dt>zero-based</dt><dd>zero-based；數值從 0 開始計算，因此 raw=3 代表第 4 個項目或 4 個單位，實際含義仍要看欄位定義。</dd></div><div><dt>offset</dt><dd>offset；從指定起點算出的位移。它回答「離起點多遠」，不等於 index。</dd></div><div><dt>Dword</dt><dd>Dword（Double word）；32 bits，也就是 4 bytes。對比 word=16 bits；例如 zero-based dword count=3 代表 4 個 Dwords，也就是 16 bytes。</dd></div><div><dt>index</dt><dd>index；用來選取清單中的項目或格式。它回答「選哪一項」，不是「離起點多遠」。</dd></div><div><dt>NUMD</dt><dd>Number of Dwords，0's-based transfer dword count；實際 bytes = (NUMD + 1) × 4。</dd></div><div><dt>OFST</dt><dd>Offset，Firmware Image Download 中以 dword 為單位的 image-relative offset。</dd></div></dl>
<!-- claim:BASEFWLOG-DOWNLOAD-RANGE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">Firmware Image Download 可分成多個 portions，firmware image portions 可不依序送達；host 宜（should）避免 ranges 重疊並符合 FWUG。Boot Partition portions 則必須（shall）依序提交。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.10</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, 文件頁 205-206, PDF 頁 231-232</p></details>
<div class="table-wrap"><table><caption>Download 的長度、偏移與分段</caption><thead><tr><th scope="col">傳輸欄位</th><th scope="col">描述哪段位置或長度</th><th scope="col">從 bytes 如何換算</th></tr></thead><tbody><tr><td>DPTR</td><td>本筆 transfer 的 host buffer</td><td>地址有效不代表 length 正確</td></tr><tr><td>NUMD</td><td>本筆 dword 數的 0's-based encoding</td><td>4096 bytes → 1024 dwords → 03FFh</td></tr><tr><td>OFST</td><td>image 起點的 dword offset</td><td>第二個 4 KiB portion 為 1024 dwords</td></tr><tr><td>FWUG</td><td>每段映像的起點對齊與長度粒度要求</td><td>全 image 與每筆 portion 分開檢查</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>0's-based</dt><dd>0's-based encoding，以 0 表示實際數量 1；依欄位換算公式通常是欄位值加 1。</dd></div><div><dt>DPTR</dt><dd>Data Pointer，SQE 中指出 command data buffer 的欄位。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">12 KiB image、4 KiB chunks：portion 0 使用 NUMD=03FFh、OFST=00000000h；portion 1 使用 NUMD=03FFh、OFST=00000400h；portion 2 使用 NUMD=03FFh、OFST=00000800h。三筆 completion 都成功後才可 Commit。</span></p></aside>
</section>
<section class="lesson" id="module-fw-commit-state"><h2 id="heading-fw-commit-state"><span class="section-number">03</span> Commit 的儲存與啟用選擇</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">Commit Action（CA）不是成功／失敗旗標；它同時決定 replace、activate 與 reset boundary。Firmware Slot（FS）選擇目標 slot，CQE status 決定下一步是驗證、執行特定 reset、等待，還是停止。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div></dl>
<figure><figcaption><strong>下載、保存與啟用分別改變什麼</strong></figcaption><ol class="flow-steps"><li>Firmware Image Download：傳送映像的各個片段。</li><li>Firmware Commit：依 CA 選擇保存至 slot 與啟用方式。</li><li>需要 reset 的啟用：在指定 reset 發生後切換執行版本。</li><li>Firmware Slot Information：分開查看目前執行 slot 與下次預定 slot。</li></ol><figcaption>下載完成、映像已保存、版本正在執行，是不同狀態。</figcaption></figure>

<!-- claim:BASEFWLOG-COMMIT-PURPOSE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span><span class="paragraph-text">Firmware Commit 驗證最後下載的 image、把它放入 firmware slot，並依 Commit Action 決定只放置、在後續 Controller Level Reset activation，或立即 activation。成功 commit 不等於當下已 active。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.9</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 202-203, PDF 頁 228-229</p></details>
<div class="table-wrap"><table><caption>Commit 的儲存與啟用選擇</caption><thead><tr><th scope="col">Commit 欄位或結果</th><th scope="col">選擇或確認的動作</th><th scope="col">如何判斷啟用階段</th></tr></thead><tbody><tr><td>CA</td><td>replace 與 activation 行為</td><td>不可只記十進位值</td></tr><tr><td>FS</td><td>目標 firmware slot</td><td>0 可能代表 controller 選 slot，依定義判讀</td></tr><tr><td>SCT／SC</td><td>成功、reset scope 或失敗原因</td><td>0Bh、10h、11h 的 reset scope 不同</td></tr><tr><td>MUD</td><td>重疊 update sequence 證據</td><td>即使 abort 也可能有效</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div><div><dt>MUD</dt><dd>Multiple Update Detected，completion 中指出 controller 偵測到 overlapping firmware update sequence 的 bit。</dd></div><div><dt>SCT</dt><dd>Status Code Type；指定完成狀態碼所屬類別，需與 SC 一起解讀。</dd></div><div><dt>SC</dt><dd>Status Code；指定所選 SCT 類別中的完成結果。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.03">03.03.</span><span class="paragraph-text">若 completion 回報 Firmware Activation Requires Controller Level Reset，Commit 本身可已成功，但 image 尚未成為 current active firmware。software 應記錄 status、執行正確 reset，再以 Identify.FR 與 LID 03h 驗證。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>FR</dt><dd>Firmware Revision，Identify Controller 回報目前 active firmware revision 的八-byte ASCII 欄位。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-fw-lid03-proof"><h2 id="heading-fw-lid03-proof"><span class="section-number">04</span> LID 03h 的目前與待啟用版本</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">Get Log Page 先用 common command 欄位建立 512-byte transfer，再以 LID=03h 選 Firmware Slot Information。AFI 同時拆成 CAFS 與 NAFS，FRS1-FRS7 表示各 slots 的 revision；最後還要用 Identify.FR 與 domain scope 交叉確認。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CAFS</dt><dd>Current Active Firmware Slot，AFI 低三 bits，指出目前正在執行的 firmware slot。</dd></div><div><dt>NAFS</dt><dd>Next Active Firmware Slot，AFI bits 6:4，指出下一次 reset 後預定啟用的 slot；0 表示未排定。</dd></div><div><dt>AFI</dt><dd>Active Firmware Info，LID 03h 中同時包含目前 active slot 與下一次 reset 後預定 active slot 的 byte。</dd></div></dl>
<!-- claim:BASEFWLOG-LOG-COMMAND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">讀 LID 03h 時，未使用 namespace，因此 NSID 必須（shall）為 0h；DPTR 以 PRP 指向 512-byte destination buffer。必要的 CDW10-CDW14 slice 為 LID=03h、LSP=0、RAE=0、NUMDL/NUMDU 表示 512 bytes、LSI=0、LPOL/LPOU=0、OT=0、UIDX=0；CSI 對 LID 03h 不使用，controller 依 Figure 208 規則忽略。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div><div><dt>NUMDL</dt><dd>Number of Dwords Lower，Get Log Page 的 NUMD 低 16 bits。</dd></div><div><dt>NUMDU</dt><dd>Number of Dwords Upper，Get Log Page 的 NUMD 高 16 bits。</dd></div><div><dt>LPOL</dt><dd>Log Page Offset Lower，Get Log Page byte offset 的低 32 bits。</dd></div><div><dt>LPOU</dt><dd>Log Page Offset Upper，Get Log Page byte offset 的高 32 bits。</dd></div><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div><div><dt>UIDX</dt><dd>UUID Index，指向 UUID List 位置的 index；0 表示未指定 UUID。</dd></div><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div><div><dt>CSI</dt><dd>I/O Command Set Identifier；選擇 I/O 命令集，NVM Command Set 使用 00h。</dd></div><div><dt>LSI</dt><dd>Log Specific Identifier，意義由所選 log page 定義的 identifier。</dd></div><div><dt>LSP</dt><dd>Log Specific Field，意義由所選 log page 定義的 command selector。</dd></div><div><dt>PRP</dt><dd>Physical Region Page，以 memory page 為單位描述 host-addressable data buffer 的 pointer 格式。</dd></div><div><dt>RAE</dt><dd>Retain Asynchronous Event，Get Log Page 是否保留相關 asynchronous event 的 selector。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.1.1, 5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 5.2.13, 文件頁 140-142, 212-215, PDF 頁 166-168, 238-241</p></details>
<div class="table-wrap"><table><caption>LID 03h 的目前與待啟用版本</caption><thead><tr><th scope="col">版本或 slot 欄位</th><th scope="col">描述哪個時點</th><th scope="col">如何與其他欄位對照</th></tr></thead><tbody><tr><td>CAFS</td><td>目前執行中的 slot</td><td>它不是 next-reset intent</td></tr><tr><td>NAFS</td><td>下一個 reset 後預定 active slot</td><td>0 表示未排定</td></tr><tr><td>FRSx</td><td>slot x 的 8-byte revision</td><td>全 0h 不是 ASCII 字串</td></tr><tr><td>Identify.FR</td><td>目前 active revision 的獨立觀察</td><td>與 CAFS 對應 FRSx 交叉確認</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.03">04.03.</span><span class="paragraph-text">AFI=22h 時，CAFS=2、NAFS=2；表示 slot 2 現在 active，且 reset 後仍預定 slot 2。若 CAFS=1、NAFS=2，代表 activation 尚未跨過 reset boundary。此依欄位換算是說明性範例，仍須以 Figure 215 的 bit 定義核對。</span></p></aside>
</section>
<section id="spec-reading"><h2>接著打開 Spec 看什麼</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span><span class="paragraph-text">以下按概念列出閱讀位置。報告時先用上面的流程說明問題，再打開對應章節看欄位與完整條件。中文教學 HTML 另有本篇全部圖表的逐圖重點、案例與細節。</span></p>
<div class="table-wrap"><table><thead><tr><th scope="col">要說明的觀念</th><th scope="col">Spec 閱讀位置</th></tr></thead><tbody><tr><td>更新前的能力與限制</td><td>Base 2.4 §5.2.14.1</td></tr><tr><td>Download 的長度、偏移與分段</td><td>Base 2.4 §5.2.10 · Base 2.4 §4.1.1, 5.2.10</td></tr><tr><td>Commit 的儲存與啟用選擇</td><td>Base 2.4 §5.2.9</td></tr><tr><td>LID 03h 的目前與待啟用版本</td><td>Base 2.4 §4.1.1, 5.2.13 · Base 2.4 §5.2.13 · Base 2.4 §5.2.13.1.4 · Base 2.4 §5.2.14.1</td></tr></tbody></table></div>
<a class="reading-link" href="/DOCS/nvme-spec-report/base-admin-fw-logs/tutorial-zh-tw.html">開啟完整中文教學與逐圖解釋 →</a></section>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:base-admin-fw-logs-download-activate -->
<details class="review-question" id="qa-base-admin-fw-logs-download-activate"><summary>1. Firmware Image Download 完成後，controller 是否已執行新韌體？</summary>
<div data-qa-answer="base-admin-fw-logs-download-activate"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="06.01">06.01.</span><span class="paragraph-text">Download 是傳送 image；Commit 才依 action 決定保存或啟用，且啟用可能需要指定 reset。要結合 Commit 結果與 slot 資訊確認目前執行版本。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.10, 文件頁 205-206, PDF 頁 231-232</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 202-203, PDF 頁 228-229</p>
</details></details>
<!-- qa:base-admin-fw-logs-download-units -->
<details class="review-question" id="qa-base-admin-fw-logs-download-units"><summary>2. NUMD=255 與 OFST=256 分別描述什麼？</summary>
<div data-qa-answer="base-admin-fw-logs-download-units"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="06.02">06.02.</span><span class="paragraph-text">NUMD 是 zero-based dword 長度，表示這次傳送 256 dwords，也就是 1024 bytes；OFST 是從 image 起點算的 dword offset，表示起點在 1024 bytes。相同數量附近的值，編碼用途不同。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 5.2.10, 文件頁 140-142, 205-206, PDF 頁 166-168, 231-232</p>
</details></details>
<!-- qa:base-admin-fw-logs-slot-version -->
<details class="review-question" id="qa-base-admin-fw-logs-slot-version"><summary>3. 某 slot 的 FRS 顯示新版本，能否單憑這一點宣告它正在執行？</summary>
<div data-qa-answer="base-admin-fw-logs-slot-version"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="06.03">06.03.</span><span class="paragraph-text">FRS 描述 slot 中的 revision；還需看 active slot 與 next-active slot 資訊。已儲存、目前執行和下次啟用可以指向不同狀態。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, 文件頁 226, PDF 頁 252</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.4, 文件頁 226, PDF 頁 252</p>
</details></details>
<!-- qa:base-admin-fw-logs-firmware-domain -->
<details class="review-question" id="qa-base-admin-fw-logs-firmware-domain"><summary>4. 為何不能總把 firmware update 視為單一 controller 的私有變更？</summary>
<div data-qa-answer="base-admin-fw-logs-firmware-domain"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="06.04">06.04.</span><span class="paragraph-text">Firmware 的作用範圍可能涉及共用的 domain 或 NVM subsystem 資源。先建立 controller 與更新範圍的關係，才能理解其他 controllers 受到的影響。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.9, 文件頁 202, PDF 頁 228</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express Base Specification, Revision 2.4</p><p>NVM Express NVMe over PCIe Transport Specification, Revision 1.4</p></details></footer>
</div>
