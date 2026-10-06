---
layout: post
title: "NVMe 自問自答題庫：PRP 與 SGL"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/pointers/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/pointers/en/">English</a><a href="/DOCS/nvme-question-bank/pointers.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q276–Q285</p><h1>PRP 與 SGL</h1><p class="qr-intro">資料指標描述的是記憶體配置。本冊先算 PRP 跨頁，再讀 SGL 的 descriptor 關係，最後把格式錯誤與傳輸失敗分開。</p><p>先練習，再展開解答。各題依需要使用文字、欄位判讀、比較或流程說明，不要求相同的回答項目。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>4KiB 頁面，PRP1 從 offset1024 開始</h2><p class="qa-takeaway">PRP2 類型由跨頁數決定；不能只用資料總長是否大於一頁判斷。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">資料長度</th><th scope="col">第一頁之後剩餘</th><th scope="col">PRP2 用途</th></tr></thead><tbody><tr><td>2048bytes</td><td>0</td><td>保留不用</td></tr><tr><td>4096bytes</td><td>1024 bytes</td><td>直接指第二頁</td></tr><tr><td>8192bytes</td><td>5120 bytes</td><td>指 PRP List</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>SGL Last Segment.LEN=32 描述 2 筆 16-byte descriptors；實際 payload 多長，要讀這兩筆 Data Block.LEN。不要把 descriptor 清單大小當成資料大小。</p>
<p class="qa-citations">來源：<a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-276">Q276 · PRP1 如何描述第一頁的資料？</a></li>
<li><a href="#q-277">Q277 · PRP2 何時是第二頁，何時是清單？</a></li>
<li><a href="#q-278">Q278 · PRP List 如何串接多頁？</a></li>
<li><a href="#q-279">Q279 · PRP 位址、Offset 與 List 有哪些對齊要求？</a></li>
<li><a href="#q-280">Q280 · PRP 為 0、位址無效或鏈結錯誤時，能指定同一種錯誤嗎？</a></li>
<li><a href="#q-281">Q281 · SGL Data Block、Segment 與 Last Segment 如何配合？</a></li>
<li><a href="#q-282">Q282 · SGL 位址、長度、數量與類型錯誤如何區分？</a></li>
<li><a href="#q-283">Q283 · Identify 的 SGL 能力如何限制合法用法？</a></li>
<li><a href="#q-284">Q284 · Data Pointer 錯誤與 Data Transfer Error 有何不同？</a></li>
<li><a href="#q-285">Q285 · PRP／SGL 錯誤如何與 CQE 及 Error Information 對回？</a></li>
</ol></section>
<article class="qa-question" id="q-276" data-question="276" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-276">Q276</a> PRP1 如何描述第一頁的資料？</h2>
<p class="qa-prompt">先試著說明欄位的單位與編碼，再用一組數值推導結果。</p>
<details class="qa-answer" id="q-276-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-276-a-01">PRP 將連續的命令資料分配到記憶體頁面；第一筆指標也描述資料在第一頁從哪個位置開始。</p><div class="qa-sections">
<section class="qa-section" id="q-276-s-01" data-answer-section="1"><h3><span>1.</span> 先確認資料的來源與範圍</h3>
<span class="qa-anchor" id="q-276-a-02"></span><p>這裡的頁面是 CC.MPS 決定的記憶體頁面，不是 SSD 的 NAND page，也不是 namespace 的 LBA。</p>
<span class="qa-anchor" id="q-276-a-03"></span><p>先讀 CAP.MPSMIN／MPSMAX 與已設定的 CC.MPS，頁面大小是 2^(12+MPS) bytes。</p>
</section>
<section class="qa-section" id="q-276-s-02" data-answer-section="2"><h3><span>2.</span> 欄位、單位與判讀例子</h3>
<span class="qa-anchor" id="q-276-a-04"></span><p>一般資料傳輸的 PRP1 分成頁基底與頁內 offset，offset 最低兩位須為 0；特殊命令可另定義 PRP1 為清單指標。</p>
<span class="qa-anchor" id="q-276-a-05"></span><p>先算第一頁剩餘容量 P−offset，再與命令資料長度比較，決定是否需要 PRP2。</p>
<span class="qa-anchor" id="q-276-a-06"></span><p>假設 P=4096、offset=1024、資料 2048 bytes，第一頁可容納 3072 bytes，因此 PRP1 已足夠，PRP2 保留不用。</p>
</section>
<section class="qa-section" id="q-276-s-03" data-answer-section="3"><h3><span>3.</span> 判讀時要保留的條件</h3>
<span class="qa-anchor" id="q-276-a-07"></span><p>Create Queue 對 PRP1 有 page-aligned 要求，不能套一般資料第一頁可帶 offset 的規則。</p>
<span class="qa-anchor" id="q-276-a-16"></span><p>用資料長度、offset 與頁面大小一起驗證；只看長度小於一頁仍可能跨頁。</p>
</section>
</div>
<span class="qa-anchor" id="q-276-a-17"></span><span class="qa-anchor" id="q-276-a-08"></span><span class="qa-anchor" id="q-276-a-09"></span><span class="qa-anchor" id="q-276-a-10"></span><span class="qa-anchor" id="q-276-a-11"></span><span class="qa-anchor" id="q-276-a-12"></span><span class="qa-anchor" id="q-276-a-13"></span><span class="qa-anchor" id="q-276-a-14"></span><span class="qa-anchor" id="q-276-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-277" data-question="277" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-277">Q277</a> PRP2 何時是第二頁，何時是清單？</h2>
<p class="qa-prompt">先用自己的話解釋機制，再舉一個常見誤解。</p>
<details class="qa-answer" id="q-277-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-277-a-01">PRP2 的意義由跨越的記憶體頁面邊界數決定，沒有另外一個「這是清單」旗標。</p><div class="qa-sections">
<section class="qa-section" id="q-277-s-01" data-answer-section="1"><h3><span>1.</span> 機制與適用範圍</h3>
<span class="qa-anchor" id="q-277-a-02"></span><p>適用於採一般 PRP 資料配置的命令；命令專用定義優先。</p>
</section>
<section class="qa-section" id="q-277-s-02" data-answer-section="2"><h3><span>2.</span> 用操作與結果理解</h3>
<span class="qa-anchor" id="q-277-a-03"></span><p>從 CC.MPS、PRP1 offset 與完整資料長度算需要幾頁。</p>
<span class="qa-anchor" id="q-277-a-04"></span>
<span class="qa-anchor" id="q-277-a-05"></span>
<span class="qa-anchor" id="q-277-a-06"></span>
<span class="qa-anchor" id="q-277-a-17"></span>
<figure class="qa-flow" id="q-277-flow"><figcaption>由剩餘長度決定 PRP2 的意義</figcaption>
<p>先算第一頁可放多少資料：頁面大小 P 減去 PRP1 的頁內 offset。剩餘長度 R 就是總長度扣掉已由第一頁描述的資料。</p><ol class="qa-flow-steps">
<li class="qa-flow-branch"><strong>R=0：只需要第一頁</strong><p>PRP2 為保留欄位，不需要另一個資料頁。</p></li>
<li class="qa-flow-branch"><strong>0&lt;R≤P：再一頁就夠</strong><p>PRP2 直接指向第二個資料頁。</p></li>
<li class="qa-flow-branch"><strong>R&gt;P：還需要至少兩個資料頁</strong><p>PRP2 指向 PRP List，由清單列出後續資料頁位址。</p></li>
</ol><p class="qa-flow-conclusion">三列是互斥分支。教學假設 P=4096、offset=1024，第一頁容量為 3072 bytes：傳輸 4096 bytes 時 R=1024，PRP2 指資料頁；傳輸 8192 bytes 時 R=5120，PRP2 指清單。PRP2 沒有獨立的類型旗標，不能只看它非零就猜用途。</p></figure>
</section>
<section class="qa-section" id="q-277-s-03" data-answer-section="3"><h3><span>3.</span> 容易誤判的地方</h3>
<span class="qa-anchor" id="q-277-a-07"></span><p>類型選錯可能使 controller 把資料 bytes 當成位址；不能期待一定在所有錯誤傳輸前檢出。</p>
<span class="qa-anchor" id="q-277-a-16"></span><p>檢查 PRP2 指向內容與推導的類型一致，而非只檢查它是不是非零。</p>
</section>
</div>
<span class="qa-anchor" id="q-277-a-08"></span><span class="qa-anchor" id="q-277-a-09"></span><span class="qa-anchor" id="q-277-a-10"></span><span class="qa-anchor" id="q-277-a-11"></span><span class="qa-anchor" id="q-277-a-12"></span><span class="qa-anchor" id="q-277-a-13"></span><span class="qa-anchor" id="q-277-a-14"></span><span class="qa-anchor" id="q-277-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-278" data-question="278" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-278">Q278</a> PRP List 如何串接多頁？</h2>
<p class="qa-prompt">先試著說明欄位的單位與編碼，再用一組數值推導結果。</p>
<details class="qa-answer" id="q-278-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-278-a-01">清單頁存放資料頁位址；資料多到清單本身也放不下時，才需要串接下一個清單頁。</p><div class="qa-sections">
<section class="qa-section" id="q-278-s-01" data-answer-section="1"><h3><span>1.</span> 先確認資料的來源與範圍</h3>
<span class="qa-anchor" id="q-278-a-02"></span><p>清單描述尚未由命令內 PRP 描述的資料，不得重複第一頁。</p>
<span class="qa-anchor" id="q-278-a-03"></span><p>以 CC.MPS 與每個 PRP entry 的 8-byte 大小，算清單可放幾筆。</p>
</section>
<section class="qa-section" id="q-278-s-02" data-answer-section="2"><h3><span>2.</span> 欄位、單位與判讀例子</h3>
<span class="qa-anchor" id="q-278-a-04"></span><p>若仍需下一個清單頁，目前頁的最後一筆改放下一頁清單位址；後續清單頁必須 page-aligned。</p>
<span class="qa-anchor" id="q-278-a-05"></span><p>逐頁填滿必要 entries，只有還有資料需要描述時才使用鏈結；不能保留無意義的空洞。</p>
<span class="qa-anchor" id="q-278-a-06"></span><p>4KiB 且從頁首開始的清單有 512 格；非最後頁最多 511 個資料頁位址加 1 個鏈結，最後頁才可全放 512 個資料頁。</p>
</section>
<section class="qa-section" id="q-278-s-03" data-answer-section="3"><h3><span>3.</span> 判讀時要保留的條件</h3>
<span class="qa-anchor" id="q-278-a-07"></span><p>最後一格是不是鏈結由剩餘資料量決定；不能把每頁最後一格一律當資料，或一律當鏈結。</p>
<span class="qa-anchor" id="q-278-a-16"></span><p>Host 要保留清單直到命令完成；描述 queue 的清單則需保留到 queue 刪除成功或 controller reset。</p>
</section>
</div>
<span class="qa-anchor" id="q-278-a-17"></span><span class="qa-anchor" id="q-278-a-08"></span><span class="qa-anchor" id="q-278-a-09"></span><span class="qa-anchor" id="q-278-a-10"></span><span class="qa-anchor" id="q-278-a-11"></span><span class="qa-anchor" id="q-278-a-12"></span><span class="qa-anchor" id="q-278-a-13"></span><span class="qa-anchor" id="q-278-a-14"></span><span class="qa-anchor" id="q-278-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-279" data-question="279" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-279">Q279</a> PRP 位址、Offset 與 List 有哪些對齊要求？</h2>
<p class="qa-prompt">先試著說明欄位的單位與編碼，再用一組數值推導結果。</p>
<details class="qa-answer" id="q-279-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-279-a-01">資料起點與清單起點的對齊要求不同，不能只使用一個「所有指標皆 4KiB 對齊」規則。</p><div class="qa-sections">
<section class="qa-section" id="q-279-s-01" data-answer-section="1"><h3><span>1.</span> 先確認資料的來源與範圍</h3>
<span class="qa-anchor" id="q-279-a-02"></span><p>對齊依目前 CC.MPS 及指標角色判斷，不依作業系統恰好使用的頁面大小。</p>
<span class="qa-anchor" id="q-279-a-03"></span><p>確認第一筆資料、命令內第一個清單指標、清單內資料位址或後續清單鏈結是哪一種。</p>
</section>
<section class="qa-section" id="q-279-s-02" data-answer-section="2"><h3><span>2.</span> 欄位、單位與判讀例子</h3>
<span class="qa-anchor" id="q-279-a-04"></span><p>一般 PRP1 可帶 Dword-aligned offset；第一個 PRP List 指標需 Qword 對齊且可有頁內 offset；後續資料頁與鏈結頁需 page-aligned。</p>
<span class="qa-anchor" id="q-279-a-05"></span><p>先檢查對齊，再算第一個清單頁從起點到頁尾還容納多少 entries。</p>
<span class="qa-anchor" id="q-279-a-06"></span><p>4KiB 頁內清單起點 offset=4080，可放 2 筆；若仍需串接，其中最後 1 筆必須作鏈結。</p>
</section>
<section class="qa-section" id="q-279-s-03" data-answer-section="3"><h3><span>3.</span> 判讀時要保留的條件</h3>
<span class="qa-anchor" id="q-279-a-07"></span><p>資料 PRP 最低兩位非零時可回 PRP Offset Invalid；若未回錯，須視為兩位清零。後續頁 offset 非零則規範建議回此錯誤，不能把 should 升成必然。</p>
<span class="qa-anchor" id="q-279-a-16"></span><p>Host 仍必須送合法對齊；controller 可以容錯不代表 Host 的要求就消失。</p>
</section>
</div>
<span class="qa-anchor" id="q-279-a-17"></span><span class="qa-anchor" id="q-279-a-08"></span><span class="qa-anchor" id="q-279-a-09"></span><span class="qa-anchor" id="q-279-a-10"></span><span class="qa-anchor" id="q-279-a-11"></span><span class="qa-anchor" id="q-279-a-12"></span><span class="qa-anchor" id="q-279-a-13"></span><span class="qa-anchor" id="q-279-a-14"></span><span class="qa-anchor" id="q-279-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-280" data-question="280" data-answer-kind="error"><h2><a class="qa-qid" href="#q-280">Q280</a> PRP 為 0、位址無效或鏈結錯誤時，能指定同一種錯誤嗎？</h2>
<p class="qa-prompt">先區分失敗條件，再判斷是否有規範明定的回報結果。</p>
<details class="qa-answer" id="q-280-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-280-a-01">0 是位址數值，不是 NVMe 為所有 PRP 定義的通用空指標；是否能存取還取決於實際記憶體映射。</p><div class="qa-sections">
<section class="qa-section" id="q-280-s-01" data-answer-section="1"><h3><span>1.</span> 先區分是哪一種失敗</h3>
<span class="qa-anchor" id="q-280-a-02"></span><p>先區分欄位格式錯誤、描述長度錯誤與實際資料搬移失敗。</p>
<span class="qa-anchor" id="q-280-a-04"></span><p>非法 offset 可對應 PRP Offset Invalid；格式合法但 DMA 存取失敗可能對應 Data Transfer Error，不能只憑位址 0 判定。</p>
<span class="qa-anchor" id="q-280-a-07"></span><p>規範沒有替每種循環鏈結或不可存取位址規定唯一可預測 CQE；若命令通道受破壞，也不能保證取得 CQE。</p>
</section>
<section class="qa-section" id="q-280-s-02" data-answer-section="2"><h3><span>2.</span> 用哪些資料確認原因</h3>
<span class="qa-anchor" id="q-280-a-03"></span><p>核對 CC.MPS、PRP 角色、需要的頁數與 Host 提供的有效記憶體範圍。</p>
<span class="qa-anchor" id="q-280-a-05"></span><p>建立一個合法基準，再只改一處；先查清單是否指向預期頁，再檢查整個傳輸所需範圍。</p>
</section>
<section class="qa-section" id="q-280-s-03" data-answer-section="3"><h3><span>3.</span> 結果與後續驗證</h3>
<span class="qa-anchor" id="q-280-a-06"></span><p>合法且可存取的配置可正常完成；保留的 PRP2 即使為 0，也不構成缺少資料頁。</p>
<span class="qa-anchor" id="q-280-a-16"></span><p>保存原 SQE、清單快照與位址配置，避免出錯後 Host 改寫清單，導致證據已不同。</p>
<span class="qa-anchor" id="q-280-a-17"></span><p>先確認指標真的被命令使用，而非保留欄位或未走到的清單部分。</p>
</section>
</div>
<span class="qa-anchor" id="q-280-a-08"></span><span class="qa-anchor" id="q-280-a-09"></span><span class="qa-anchor" id="q-280-a-10"></span><span class="qa-anchor" id="q-280-a-11"></span><span class="qa-anchor" id="q-280-a-12"></span><span class="qa-anchor" id="q-280-a-13"></span><span class="qa-anchor" id="q-280-a-14"></span><span class="qa-anchor" id="q-280-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-281" data-question="281" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-281">Q281</a> SGL Data Block、Segment 與 Last Segment 如何配合？</h2>
<p class="qa-prompt">先說出比較對象最重要的差別，並舉一個不能互相代用的例子。</p>
<details class="qa-answer" id="q-281-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-281-a-01">Data Block 描述資料位址與長度；Segment 類型描述下一段 descriptor 清單，而不是資料本身。</p><div class="qa-sections">
<section class="qa-section" id="q-281-s-01" data-answer-section="1"><h3><span>1.</span> 差別在哪裡</h3>
<span class="qa-anchor" id="q-281-a-02"></span><p>SGL 用於支援它的 PCIe I/O 命令；PCIe Admin 命令不得使用 SGL。</p>
<span class="qa-anchor" id="q-281-a-04"></span><p>每個 descriptor16 bytes；Data Block 類型 0h，Segment2h，Last Segment3h。Segment 的 LEN 是下一段清單的 bytes。</p>
</section>
<section class="qa-section" id="q-281-s-02" data-answer-section="2"><h3><span>2.</span> 如何選擇與確認</h3>
<span class="qa-anchor" id="q-281-a-03"></span><p>先確認 Identify.SGLS，再看 CDW0.PSDT 的 data／metadata 配置。</p>
<span class="qa-anchor" id="q-281-a-05"></span><p>只有一個資料區塊時，可直接放在命令 SGL1；多區塊時，SGL1 指向清單，再逐筆讀 Data Block。</p>
<span class="qa-anchor" id="q-281-a-06"></span><p>例如 Last Segment.LEN=32，代表下一段有 2 個 descriptors，不代表命令只傳 32 bytes；實際資料量看那兩筆 Data Block.LEN。</p>
</section>
<section class="qa-section" id="q-281-s-03" data-answer-section="3"><h3><span>3.</span> 哪些結論不能互相套用</h3>
<span class="qa-anchor" id="q-281-a-07"></span><p>鏈結 descriptor 只能在目前段最後一筆；Last Segment 指向的最後段不得再含任何鏈結 descriptor。</p>
<span class="qa-anchor" id="q-281-a-16"></span><p>分開計算 descriptor bytes 與 payload bytes，才能核對清單完整性及命令長度。</p>
</section>
</div>
<span class="qa-anchor" id="q-281-a-17"></span><span class="qa-anchor" id="q-281-a-08"></span><span class="qa-anchor" id="q-281-a-09"></span><span class="qa-anchor" id="q-281-a-10"></span><span class="qa-anchor" id="q-281-a-11"></span><span class="qa-anchor" id="q-281-a-12"></span><span class="qa-anchor" id="q-281-a-13"></span><span class="qa-anchor" id="q-281-a-14"></span><span class="qa-anchor" id="q-281-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-282" data-question="282" data-answer-kind="error"><h2><a class="qa-qid" href="#q-282">Q282</a> SGL 位址、長度、數量與類型錯誤如何區分？</h2>
<p class="qa-prompt">先區分失敗條件，再判斷是否有規範明定的回報結果。</p>
<details class="qa-answer" id="q-282-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-282-a-01">不同 SGL 錯誤指出不同的壞掉環節，不能全部簡化成 Invalid Field。</p><div class="qa-sections">
<section class="qa-section" id="q-282-s-01" data-answer-section="1"><h3><span>1.</span> 先區分是哪一種失敗</h3>
<span class="qa-anchor" id="q-282-a-02"></span><p>分開 data SGL 與 metadata SGL，兩者長度錯誤有不同 Status。</p>
<span class="qa-anchor" id="q-282-a-04"></span><p>Segment 位址需 Qword 對齊，LEN 非零且為 16 倍數；Data Block.LEN=0 合法，代表不傳資料。</p>
<span class="qa-anchor" id="q-282-a-07"></span><p>鏈結不在最後一筆須 0/0Eh；最後段再鏈結須 0/0Dh；不支援類型須 0/11h；資料／metadata 過短分別須 0/0Fh、0/10h。</p>
</section>
<section class="qa-section" id="q-282-s-02" data-answer-section="2"><h3><span>2.</span> 用哪些資料確認原因</h3>
<span class="qa-anchor" id="q-282-a-03"></span><p>查 SGLS 的對齊、LLDTS 及支援 descriptor 類型，再核對命令要求長度。</p>
<span class="qa-anchor" id="q-282-a-05"></span><p>沿鏈逐段核對邊界、最後一筆位置、type/subtype，以及全部有效資料長度。</p>
</section>
<section class="qa-section" id="q-282-s-03" data-answer-section="3"><h3><span>3.</span> 結果與後續驗證</h3>
<span class="qa-anchor" id="q-282-a-06"></span><p>SGL 至少要涵蓋要求的資料量；LLDTS=1 允許較長，仍只按命令要求傳輸。</p>
<span class="qa-anchor" id="q-282-a-16"></span><p>LLDTS=0 的過長清單建議不要因此中止；若因此中止，建議用對應長度錯誤。對齊錯誤還須保留各欄定義的 may／should 強度。</p>
<span class="qa-anchor" id="q-282-a-17"></span><p>先找第一個能以結構證明的違規，不憑最終資料不對就猜 descriptor 類型錯誤。</p>
</section>
</div>
<span class="qa-anchor" id="q-282-a-08"></span><span class="qa-anchor" id="q-282-a-09"></span><span class="qa-anchor" id="q-282-a-10"></span><span class="qa-anchor" id="q-282-a-11"></span><span class="qa-anchor" id="q-282-a-12"></span><span class="qa-anchor" id="q-282-a-13"></span><span class="qa-anchor" id="q-282-a-14"></span><span class="qa-anchor" id="q-282-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-283" data-question="283" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-283">Q283</a> Identify 的 SGL 能力如何限制合法用法？</h2>
<p class="qa-prompt">先選查詢介面與目標，再說明哪個回傳欄位能支持你的結論。</p>
<details class="qa-answer" id="q-283-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-283-a-01">SGL 支援不是只有一個 yes/no；資料對齊、額外類型、metadata 與較長清單都有各自能力。</p><div class="qa-sections">
<section class="qa-section" id="q-283-s-01" data-answer-section="1"><h3><span>1.</span> 要查哪個對象、哪份資料</h3>
<span class="qa-anchor" id="q-283-a-02"></span><p>能力還須配合傳輸與命令種類；Base 表列某個類型，不等於所有 PCIe 命令都可使用。</p>
<span class="qa-anchor" id="q-283-a-03"></span><p>SGLS[1:0]=00 不支援、01 支援且 Data Block 無對齊粒度限制、10 要求 Dword 對齊與粒度。</p>
<span class="qa-anchor" id="q-283-a-04"></span><p>LLDTS 控制較長清單，SBBDS 控制 Bit Bucket，MSDS 與 MBA 控制 metadata 配置；SDT 是建議 descriptor 數。</p>
</section>
<section class="qa-section" id="q-283-s-02" data-answer-section="2"><h3><span>2.</span> 查詢順序與回覆判讀</h3>
<span class="qa-anchor" id="q-283-a-05"></span><p>先選合法 PSDT，再只使用已宣告且 PCIe 允許的 type/subtype；Offset subtype 不能因看到其他傳輸定義就套用。</p>
<span class="qa-anchor" id="q-283-a-06"></span><p>SGLS=10b 時，Data Block 位址與長度須是 4-byte 倍數；這不表示每個資料區塊都要 page-aligned。</p>
</section>
<section class="qa-section" id="q-283-s-03" data-answer-section="3"><h3><span>3.</span> 證據不足或不一致時怎麼判斷</h3>
<span class="qa-anchor" id="q-283-a-07"></span><p>超過 SDT 可能降低效能，但 SDT 不是一律拒絕命令的硬上限；不得把 capsule 專用欄位當成 PCIe 清單上限。</p>
<span class="qa-anchor" id="q-283-a-16"></span><p>支援宣告與合法描述資料必須一致；Admin 命令的 SGL 禁用規則仍優先。</p>
<span class="qa-anchor" id="q-283-a-17"></span><p>先完整解碼 SGLS，而不是只看整個欄位非零。</p>
</section>
</div>
<span class="qa-anchor" id="q-283-a-08"></span><span class="qa-anchor" id="q-283-a-09"></span><span class="qa-anchor" id="q-283-a-10"></span><span class="qa-anchor" id="q-283-a-11"></span><span class="qa-anchor" id="q-283-a-12"></span><span class="qa-anchor" id="q-283-a-13"></span><span class="qa-anchor" id="q-283-a-14"></span><span class="qa-anchor" id="q-283-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-284" data-question="284" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-284">Q284</a> Data Pointer 錯誤與 Data Transfer Error 有何不同？</h2>
<p class="qa-prompt">先說出比較對象最重要的差別，並舉一個不能互相代用的例子。</p>
<details class="qa-answer" id="q-284-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-284-a-01">Pointer 錯誤表示描述方法不合法；Transfer Error 表示資料或 metadata 搬移失敗，兩者不能用同一個原因解釋。</p><div class="qa-sections">
<section class="qa-section" id="q-284-s-01" data-answer-section="1"><h3><span>1.</span> 差別在哪裡</h3>
<span class="qa-anchor" id="q-284-a-02"></span><p>錯誤可能在清單檢查或實際存取時才被發現，時間不同。</p>
<span class="qa-anchor" id="q-284-a-04"></span><p>記錄 PSDT、指標、長度、SCT／SC、SQID、CID；Error Information 的 PEL 是 Parameter Error Location，不是 Persistent Event Log。</p>
</section>
<section class="qa-section" id="q-284-s-02" data-answer-section="2"><h3><span>2.</span> 如何選擇與確認</h3>
<span class="qa-anchor" id="q-284-a-03"></span><p>先檢查 PRP／SGL 規則與完整範圍，再核對當時記憶體是否仍有效。</p>
<span class="qa-anchor" id="q-284-a-05"></span><p>先排除 Host 提早回收 buffer，再檢查合法位址是否能被 controller 存取。</p>
<span class="qa-anchor" id="q-284-a-06"></span><p>格式合法、範圍完整且搬移成功，仍需命令本身完成才有 Success；指標合法不代表媒體操作一定成功。</p>
</section>
<section class="qa-section" id="q-284-s-03" data-answer-section="3"><h3><span>3.</span> 哪些結論不能互相套用</h3>
<span class="qa-anchor" id="q-284-a-07"></span><p>Data Transfer Error 為 0/04h；PRP Offset 與各 SGL 結構錯誤則用各自 Status，不能把所有傳輸錯誤一律定為 Host 格式錯誤。</p>
<span class="qa-anchor" id="q-284-a-16"></span><p>SGL 可以先傳輸合法部分，之後才發現另一筆錯誤；失敗 CQE 不證明 buffer 完全未修改。</p>
</section>
</div>
<span class="qa-anchor" id="q-284-a-17"></span><span class="qa-anchor" id="q-284-a-08"></span><span class="qa-anchor" id="q-284-a-09"></span><span class="qa-anchor" id="q-284-a-10"></span><span class="qa-anchor" id="q-284-a-11"></span><span class="qa-anchor" id="q-284-a-12"></span><span class="qa-anchor" id="q-284-a-13"></span><span class="qa-anchor" id="q-284-a-14"></span><span class="qa-anchor" id="q-284-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-285" data-question="285" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-285">Q285</a> PRP／SGL 錯誤如何與 CQE 及 Error Information 對回？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-285-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-285-a-01">把錯誤對回原命令，才能知道哪個指標或資料範圍需要修正。</p><div class="qa-sections">
<section class="qa-section" id="q-285-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-285-a-02"></span><p>使用同一 controller、同一 queue 使用期間及相同 SQID／CID；CID 可能重用，單看數字不夠。</p>
<span class="qa-anchor" id="q-285-a-03"></span><p>保存 CQE 的 SCT、SC、DNR、More，再依適用規則讀 Error Information。</p>
<span class="qa-anchor" id="q-285-a-04"></span><p>Error Count、SQID、CID、Status 與 Parameter Error Location 可協助比對；無法指出欄位時，需保留其無效／未指定表示。</p>
</section>
<section class="qa-section" id="q-285-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-285-a-17"></span><p>先保存原命令與清單，避免重試時覆寫唯一能定位問題的內容。</p>
<span class="qa-anchor" id="q-285-a-05"></span><p>先對命令身分與狀態，再判讀 byte／bit 位置；清單內容在 Host memory 時，不能硬把每個錯誤都映成 SQE 某一 bit。</p>
</section>
<section class="qa-section" id="q-285-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-285-a-06"></span><p>找到相符紀錄後，可將原始欄位、違規條件與實際 Status 放在一起驗證。</p>
<span class="qa-anchor" id="q-285-a-07"></span><p>More=0 不證明一定沒有 Error entry；也不是每個失敗命令都要求新增 entry。DNR=0 更不代表可用同一個壞清單直接重試。</p>
<span class="qa-anchor" id="q-285-a-16"></span><p>若記錄已被覆蓋或重設後清除，說明證據不足；不能將缺少歷史紀錄當成原命令合法。</p>
</section>
<section class="qa-section" id="q-285-s-04" data-answer-section="4"><h3><span>4.</span> 錯誤完成與紀錄要如何對照</h3>
<span class="qa-anchor" id="q-285-a-08"></span><p>只有收到 CQE，才有 DNR 與 More 可供判讀。 <a class="qa-rule-link" href="#common-command-8">完整條件見本冊說明</a></p>
<span class="qa-anchor" id="q-285-a-10"></span><p>成功 CQE 不會單憑成功這件事，就要求新增 Error Information entry。 <a class="qa-rule-link" href="#common-command-10">完整條件見本冊說明</a></p>
</section>
</div>
<span class="qa-anchor" id="q-285-a-09"></span><span class="qa-anchor" id="q-285-a-11"></span><span class="qa-anchor" id="q-285-a-12"></span><span class="qa-anchor" id="q-285-a-13"></span><span class="qa-anchor" id="q-285-a-14"></span><span class="qa-anchor" id="q-285-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-sgls">Base 2.4 §5.2.14.2.1 (SGLS)</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-command-8"><h3>命令完成、事件與紀錄 · DNR 與 More 應如何設定？</h3><p>只有收到 CQE，才有 DNR 與 More 可供判讀。DNR=1 表示相同命令即使重送到此 NVM subsystem 的任一 controller，仍預期會失敗；DNR=0 則只表示可能成功。除非個別錯誤條件另有明定，不能只看 Status 名稱就要求 DNR=1。More=1 表示 Error Information Log 有這筆命令的補充資訊。SCT=SC=0 時，DNR 應為 0。</p></article>
<article id="common-command-10"><h3>命令完成、事件與紀錄 · 是否更新 Error Information Log 或其他 Log？</h3><p>成功 CQE 不會單憑成功這件事，就要求新增 Error Information entry。若錯誤 CQE 的 More=1，則讀取 LID01h，並以 SQID、CID 及 Error Count 關聯紀錄。其他非成功 CQE 是否需要新增 entry，仍須依記錄規則判斷，不能直接以失敗次數推算。至於操作造成的狀態變化，則用本題列出的查詢介面重新確認。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-pointers"><strong>Base 2.4 · §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</strong><br>文件頁 140–142, 158–164 · PDF 166–168, 184–190 · Figure 93, 110–122</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-sgls"><strong>Base 2.4 · §5.2.14.2.1 (SGLS)</strong><br>文件頁 377–378 · PDF 403–404 · Figure 338</li>
<li id="ref-create"><strong>Base 2.4 · §5.3.1–5.3.2</strong><br>文件頁 527–531 · PDF 553–557 · Figure 571–579</li>
<li id="ref-retirement"><strong>PCIe Transport 1.4 · §3.4 (Command Related Resource Retirement)</strong><br>文件頁 13 · PDF 13</li>
</ul><h3>需要看欄位圖時</h3><p>以下連結可開啟對應的圖表教學，查閱欄位及判讀方式。每張圖保留固定的教學位置，方便之後反覆查詢。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/pointers/en/">English</a><a href="/DOCS/nvme-question-bank/pointers.html">繁中教學 HTML</a></nav>
</div>
<script>
(function(){
 const root=document.querySelector('.nvme-qa'); if(!root)return;
 root.querySelectorAll('.qa-controls').forEach(x=>x.hidden=false);
 root.querySelectorAll('[data-expand]').forEach(b=>b.addEventListener('click',()=>root.querySelectorAll('.qa-answer').forEach(d=>d.open=b.dataset.expand==='true')));
 const input=root.querySelector('#qa-search'),items=[...root.querySelectorAll('.qa-question,.qa-search-item')],output=root.querySelector('#qa-count');
 if(input)input.addEventListener('input',()=>{const q=input.value.trim().toLowerCase();let n=0;items.forEach(el=>{el.hidden=!el.textContent.toLowerCase().includes(q);if(!el.hidden)n++;});output.textContent=n+' / '+items.length;});
 function reveal(){let el=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(el){for(let p=el;p;p=p.parentElement){if(p.tagName==='DETAILS')p.open=true;}el.hidden=false;}}
 addEventListener('hashchange',reveal);reveal();
 let printState=[];addEventListener('beforeprint',()=>{printState=[...root.querySelectorAll('details')].map(d=>[d,d.open]);printState.forEach(([d])=>d.open=true);});addEventListener('afterprint',()=>printState.forEach(([d,open])=>d.open=open));
 const toggle=root.querySelector('[data-theme-toggle]');if(toggle)toggle.addEventListener('click',()=>{const dark=document.documentElement.dataset.theme?document.documentElement.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;document.documentElement.dataset.theme=dark?'light':'dark';});
})();
</script>
