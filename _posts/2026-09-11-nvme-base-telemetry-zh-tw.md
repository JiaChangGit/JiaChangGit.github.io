---
permalink: /nvme/telemetry-zh-tw/
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4：Telemetry：資料收集與一致性讀取"
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
[English]({% post_url 2026-09-11-nvme-base-telemetry-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">Telemetry 把裝置收集的內部狀態整理成主機可讀取的紀錄。這篇的重點是取得一份完整且一致的資料：誰建立紀錄、各資料區有多大，以及分段讀取期間紀錄是否已經換成另一份。</span></p>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>先確認誰建立紀錄</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">主機發起與控制器發起的紀錄有不同建立方式；先分清來源，才能正確選擇讀取與確認完成的做法。</span></p></article>
<article><span class="axis-number">02</span><h3>從表頭找出資料範圍</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">先讀表頭，再用資料區邊界決定要讀哪些區段；標準定義位置，廠商資料格式決定如何理解內容。</span></p></article>
<article><span class="axis-number">03</span><h3>確保分段讀到同一份紀錄</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">資料可能分多次取回；要檢查紀錄識別與變更資訊，避免把不同時間的內容拼成一份。</span></p></article>
</div>
<div class="overview-connections"><h3>把主軸連起來</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">先分清主機發起與控制器發起的紀錄，再從 header 得知資料區範圍。讀取多個區段時，要保留同一份紀錄的識別資訊，並依該類紀錄的規則確認讀取完成；資料區位置可由標準解釋，廠商自訂內容則需要相應格式資料。</span></p>
</div>
</section>
<section class="lesson" id="module-telemetry-layout"><h2 id="heading-telemetry-layout"><span class="section-number">01</span> 資料區如何排列與計算大小</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">Area 是從同一 block 1 起算的不同大小視圖。先依欄位換算 header，再選擇適用且有資料的最後 area；不要把三個 Last Block 數字相加。</span></p>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 260" role="img"><title>Telemetry Data Areas 是累積範圍</title><desc>Header 位於 block 0。每個 Data Area 都從 block 1 開始，較大的 Area 包含較小 Area 的資料。</desc><rect x="20" y="20" width="155" height="210" rx="6" class="v-command"/><text x="97.5" y="118.5" text-anchor="middle" font-size="17">Header</text><text x="97.5" y="143.5" text-anchor="middle" font-size="17">Block 0</text><rect x="205" y="20" width="160" height="55" rx="6" class="v-object"/><text x="285.0" y="53.5" text-anchor="middle" font-size="17">Area 1</text><rect x="205" y="95" width="325" height="55" rx="6" class="v-decision"/><text x="367.5" y="128.5" text-anchor="middle" font-size="17">Area 2</text><rect x="205" y="170" width="535" height="55" rx="6" class="v-success"/><text x="472.5" y="203.5" text-anchor="middle" font-size="17">Area 3</text></svg></div><figcaption>Header 位於 block 0。每個 Data Area 都從 block 1 開始，較大的 Area 包含較小 Area 的資料。</figcaption></figure>

<!-- claim:BASETELEMETRY-TEL-MODEL -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">Telemetry 的 header 為 block 0，每個 block 是 512 bytes；所有 Data Areas 都從 block 1 起算。Area 2/3/4 是更大的累積集合，不是接在 Area 1 後的獨立區塊。Last Block 是包含在內的最後 block 編號；payload 格式與大小由廠商定義。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.30; 5.2.13.1.8-5.2.13.1.9</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.13.1.8-5.2.13.1.9, 文件頁 232-237,733-737, PDF 頁 258-263,759-763</p></details>
<div class="table-wrap"><table><caption>資料區如何排列與計算大小</caption><thead><tr><th scope="col">資料區域</th><th scope="col">包含哪些 blocks</th><th scope="col">Last Block 數值的限制</th></tr></thead><tbody><tr><td>Area 1</td><td>1 到 L1</td><td>L1=0 表示沒有資料</td></tr><tr><td>Area 2</td><td>1 到 L2</td><td>L2 &gt;= L1</td></tr><tr><td>Area 3</td><td>1 到 L3</td><td>L3 &gt;= L2</td></tr><tr><td>Area 4</td><td>1 到 L4</td><td>支援條件另行檢查</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">Last Blocks=65/1000/30000 時，Area 3 payload 為 30000×512=15360000 bytes；包含 header 的 log 為 15360512 bytes。0/1000/1000 則表示 Area 1 空、Area 3 沒有超出 Area 2 的新增內容。</span></p></aside>
</section>
<section class="lesson" id="module-telemetry-capture"><h2 id="heading-telemetry-capture"><span class="section-number">02</span> 建立快照、分段讀取與確認完成</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">07h 的 create 與後續讀取分開；08h 的 capture 由 controller 決定。Host 對兩者都要驗證 generation，並分清事件 acknowledgement 與刪除 payload。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div></dl>
<figure><figcaption><strong>讓分段讀取對應同一份資料</strong></figcaption><ol class="flow-steps"><li>讀取 header，記下 generation number。</li><li>依資料範圍分段讀取，沿用同一份快照。</li><li>再次讀取 header，比較 generation number。</li><li>兩次 generation 相符後，才把分段內容視為同一份資料。</li></ol><figcaption>Generation number 用來辨識資料版本；建立新快照與讀取既有快照是不同動作。</figcaption></figure>

<!-- claim:BASETELEMETRY-TEL-CREATE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">LID 07h 的 CTHID 是 CDW10 bit 8；設為 1 要求新 capture，0 不更新該 snapshot。MCDA 是 bits 11:9，只有 MCDAS=1 且 CTHID=1 時適用；001b 至 100b 分別要求建立至 Area 1 至 Area 4，000b 由 controller 決定。MCDAS 來自 Supported Log Pages 的 LID Specific Parameter。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CTHID</dt><dd>Create Telemetry Host-Initiated Data；07h 的 capture 要求，後續分段讀同一快照要清為 0。</dd></div><div><dt>MCDAS</dt><dd>Maximum Created Data Area Supported；07h 的 LID Specific Parameter bit 0，宣告 MCDA 支援。</dd></div><div><dt>MCDA</dt><dd>Maximum Created Data Area；支援且要求 capture 時選擇建立的最大 area。</dd></div><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div><div><dt>LID</dt><dd>Log Page Identifier；指定要讀取哪一種 log page 的編號。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.8</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.8, 文件頁 232-235, PDF 頁 258-261</p></details>
<div class="table-wrap"><table><caption>建立快照、分段讀取與確認完成</caption><thead><tr><th scope="col">快照控制欄位</th><th scope="col">執行或回報的動作</th><th scope="col">分段讀取時須注意什麼</th></tr></thead><tbody><tr><td>CTHID=1</td><td>觸發新 07h capture</td><td>後續分段讀不要再次 create</td></tr><tr><td>MCDA</td><td>限制建立到哪個 area</td><td>先看 MCDAS</td></tr><tr><td>RAE=1</td><td>保留事件</td><td>不保證沒有其他 reader</td></tr><tr><td>TCDA=0</td><td>上次 acknowledgement 後未更新</td><td>2.4 不等於 payload 消失</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>TCDA</dt><dd>Telemetry Controller-Initiated Data Available；2.4 中表示自上次 RAE=0 acknowledgement 後是否有更新。</dd></div><div><dt>RAE</dt><dd>Retain Asynchronous Event；Telemetry 收集中用 1 保留通知狀態，完成後用 0 acknowledgement。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">讀取前 generation=2Ah，讀完變成 2Bh，這批 blocks 不能當成同一 capture 的一致資料。若值保持 2Ah 但 TCDA 被其他 host 清成 0，08h 收集仍需依流程檢查該競態。</span></p></aside>
</section>
<section id="spec-reading"><h2>接著打開 Spec 看什麼</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">以下按概念列出閱讀位置。報告時先用上面的流程說明問題，再打開對應章節看欄位與完整條件。中文教學 HTML 另有本篇全部圖表的逐圖重點、案例與細節。</span></p>
<div class="table-wrap"><table><thead><tr><th scope="col">要說明的觀念</th><th scope="col">Spec 閱讀位置</th></tr></thead><tbody><tr><td>資料區如何排列與計算大小</td><td>Base 2.4 §8.1.30; 5.2.13.1.8-5.2.13.1.9 · Base 2.4 §8.1.30; 5.2.30.1.15 · Base 2.4 §5.2.13.1.8-5.2.13.1.9</td></tr><tr><td>建立快照、分段讀取與確認完成</td><td>Base 2.4 §5.2.13.1.8 · Base 2.4 §8.1.30 · Base 2.4 §5.2.13.1.9 · Base 2.4 §5.2.13.1.8-5.2.13.1.9 · Base 2.4 §8.1.30; 5.2.30.1.6</td></tr></tbody></table></div>
<a class="reading-link" href="/DOCS/nvme-spec-report/base-telemetry/tutorial-zh-tw.html">開啟完整中文教學與逐圖解釋 →</a></section>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:base-telemetry-1 -->
<details class="review-question" id="qa-base-telemetry-1"><summary>1. Area 1 的 Last Block=3，Area 2 的 Last Block=7；Area 2 包含哪些 payload blocks？</summary>
<div data-qa-answer="base-telemetry-1"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">Area 2 包含 blocks 1 到 7，共 7×512=3584 bytes，已包含 Area 1 的 blocks 1 到 3。Header 是 block 0，另占 512 bytes；Last Block 是包含在範圍內的最後編號。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30; 5.2.13.1.8-5.2.13.1.9, 文件頁 232-237,733-737, PDF 頁 258-263,759-763</p>
</details></details>
<!-- qa:base-telemetry-2 -->
<details class="review-question" id="qa-base-telemetry-2"><summary>2. 分段讀完 Telemetry 後，為何還要重讀 header？</summary>
<div data-qa-answer="base-telemetry-2"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">分段期間可能出現另一代 snapshot。重讀 generation 可確認資料是否仍屬同一代；若改變便須重收。Controller-initiated 資料還要檢查 TCDA，避免忽略其他讀取者已確認資料的情況。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.30, 文件頁 734-735, PDF 頁 760-761</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.9, 文件頁 237, PDF 頁 263</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
