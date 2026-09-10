---
permalink: /nvme/boot-partitions-zh-tw/
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4：Boot Partitions：讀取、更新與寫入保護"
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
[English]({% post_url 2026-09-11-nvme-base-boot-partitions-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">Boot Partitions 提供存放開機映像的空間。這篇從「還沒建立一般 I/O 佇列時，主機如何取到開機資料」開始，再說明映像更新、選擇啟用的分割區與寫入保護。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>取出開機映像</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">從選擇分割區、指定讀取範圍，到把資料放入主機記憶體，理解開機讀取的完整流程。</span></p></article>
<article><span class="axis-number">02</span><h3>更新並選擇啟用映像</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">傳入新映像、替換分割區內容、選擇啟用分割區，各自解決不同問題。</span></p></article>
<article><span class="axis-number">03</span><h3>保護已寫入的內容</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">比較不同寫入保護狀態，以及重設或斷電後哪些限制仍然保留。</span></p></article>
</div>
<div class="overview-connections"><h3>把主軸連起來</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">讀取時要選對分割區與範圍，並提供接收資料的主機記憶體；更新時則要分清傳入映像、替換內容與選擇啟用分割區。寫入保護限制的是更新行為，其狀態在不同 reset 或斷電條件下的保留方式需要另外判讀。</span></p>
</div>
</section>
<section class="lesson" id="module-boot-read"><h2 id="heading-boot-read"><span class="section-number">01</span> Boot 的兩條讀取路徑</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">先問 controller 是否已建立 Admin command 環境，再選 property 或 LID 15h。兩條路徑讀同一類 Boot 內容，但回傳格式與狀態觀察點不同。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div><div><dt>LID</dt><dd>Log Page Identifier；指定要讀取哪一種 log page 的編號。</dd></div></dl>
<!-- claim:BASEBOOT-BOOT-MODEL -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">Boot Partitions 是選用功能；支援時有兩個等大的 partition，ID 為 0h、1h。Host 可在未建立 queues、未啟用 controller 時透過 properties 讀取。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3, 文件頁 586, PDF 頁 612</p></details>
<div class="table-wrap"><table><caption>Boot 的兩條讀取路徑</caption><thead><tr><th scope="col">讀取路徑或欄位</th><th scope="col">從哪裡取得資料或狀態</th><th scope="col">操作環境與單位</th></tr></thead><tbody><tr><td>Properties</td><td>BRS 回報讀取狀態</td><td>不要求 CC.EN=1</td></tr><tr><td>LID 15h</td><td>16-byte header + data</td><td>由 Admin command CQE 判斷命令結果</td></tr><tr><td>BPID</td><td>選取讀取 partition</td><td>不等於 active ID</td></tr><tr><td>BPSZ</td><td>每單位 128 KiB</td><td>不是 bytes</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>BPID</dt><dd>Boot Partition Identifier；選取 0 或 1，與目前 active partition 分開。</dd></div><div><dt>BPSZ</dt><dd>Boot Partition Size；每單位 128 KiB。</dd></div><div><dt>BRS</dt><dd>Boot Read Status；00b 未請求、01b 進行中、10b 成功、11b 錯誤。</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div><div><dt>CC</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。</dd></div><div><dt>EN</dt><dd>Enable，CC 中控制 controller enable state 的 bit。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">BPSZ=2 的 LID 15h 包含 262144 bytes 的 Boot data，加上 16-byte header，共 262160 bytes。讀 BP1 並不把 BP1 設為 active；讀 log 也不會推進 property 的 BRS。</span></p></aside>
</section>
<section class="lesson" id="module-boot-protection"><h2 id="heading-boot-protection"><span class="section-number">02</span> 映像更新、啟用與寫入保護</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">把 image transfer、partition content、active selection、write protection 分開追蹤。成功下載尚未寫入 Boot Partition；寫入成功也未自動選成 active。</span></p>
<!-- claim:BASEBOOT-BOOT-UPDATE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">Boot image 從開頭依序用 Firmware Image Download 傳送；將目標解鎖後，以 Firmware Commit CA=110b 寫入 BPID 指定的 partition。Host 可讀回驗證，再以 CA=111b 更新 active ID，最後重新上鎖。更新中斷可能留下新舊混合內容，因此宜先驗證再設為 active。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CA</dt><dd>Commit Action，Firmware Commit 中選擇 replace、activate 與 reset policy 的欄位。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, 文件頁 587-588, PDF 頁 613-614</p></details>
<div class="table-wrap"><table><caption>映像更新、啟用與寫入保護</caption><thead><tr><th scope="col">保護機制與狀態</th><th scope="col">哪種操作能改變狀態</th><th scope="col">重設或斷電後的結果</th></tr></thead><tbody><tr><td>FID 85h unlocked</td><td>Controller reset 後保留</td><td>Power cycle 後 locked</td></tr><tr><td>FID 85h until power cycle</td><td>一般 Set 不可解鎖</td><td>共享 multi-domain partition 不可用</td></tr><tr><td>RPMB enabled/unlocked</td><td>Controller reset 即 relock</td><td>啟用保護不可撤回</td></tr><tr><td>兩套機制</td><td>同時只有一套控制</td><td>RPMB enable 是控制權轉移</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>FID</dt><dd>Feature Identifier；指定要讀取或設定哪一項 Feature 的編號。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">保留 BP0 不變、要求 BP1 unlocked 的 FID 85h CDW11 是 (001b &lt;&lt; 3) | 000b = 08h。讀回時 BP0 不會回傳 000b，而會回報它真正的狀態；RPMB 控制時則回報 100b。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div></dl></aside>
</section>
<section id="spec-reading"><h2>接著打開 Spec 看什麼</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">以下按概念列出閱讀位置。報告時先用上面的流程說明問題，再打開對應章節看欄位與完整條件。中文教學 HTML 另有本篇全部圖表的逐圖重點、案例與細節。</span></p>
<div class="table-wrap"><table><thead><tr><th scope="col">要說明的觀念</th><th scope="col">Spec 閱讀位置</th></tr></thead><tbody><tr><td>Boot 的兩條讀取路徑</td><td>Base 2.4 §8.1.3 · Base 2.4 §8.1.3.1 · Base 2.4 §5.2.13.1.21</td></tr><tr><td>映像更新、啟用與寫入保護</td><td>Base 2.4 §8.1.3.2 · Base 2.4 §8.1.3.3 · Base 2.4 §5.2.30.1.39 · Base 2.4 §8.1.3.3.1-8.1.3.3.3 · Base 2.4 §5.2.30.1.39; 8.1.3.3.3</td></tr></tbody></table></div>
<a class="reading-link" href="/DOCS/nvme-spec-report/base-boot-partitions/tutorial-zh-tw.html">開啟完整中文教學與逐圖解釋 →</a></section>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:base-boot-partitions-1 -->
<details class="review-question" id="qa-base-boot-partitions-1"><summary>1. 新 boot image 已寫入 partition，下一次使用的 active partition 就已改變了嗎？</summary>
<div data-qa-answer="base-boot-partitions-1"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">寫入與選擇 active ID 是兩個動作。CA=110b 寫入指定 partition；可讀回確認內容後，再以 CA=111b 選擇 active ID。把兩步分開，才能在切換前確認新 image。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.2, 文件頁 587-588, PDF 頁 613-614</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3, 文件頁 586, PDF 頁 612</p>
</details></details>
<!-- qa:base-boot-partitions-2 -->
<details class="review-question" id="qa-base-boot-partitions-2"><summary>2. Boot Partition 解鎖後，Controller Level Reset 一定會重新上鎖嗎？</summary>
<div data-qa-answer="base-boot-partitions-2"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">要先知道由哪個機制控制。Set Features 的 unlocked 狀態可跨此 reset 保留，但 power cycle 會上鎖；已啟用的 RPMB 保護則在這兩種事件都會重新上鎖。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.39, 文件頁 513-514, PDF 頁 539-540</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.3.3.1-8.1.3.3.3, 文件頁 589-594, PDF 頁 615-620</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
