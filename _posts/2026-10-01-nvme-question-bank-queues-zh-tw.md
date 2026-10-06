---
layout: post
title: "NVMe 自問自答題庫：Admin Queue 與 I/O Queue"
date: 2026-10-01 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/queues/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/queues/en/">English</a><a href="/DOCS/nvme-question-bank/queues.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q10–Q21</p><h1>Admin Queue 與 I/O Queue</h1><p class="qr-intro">Host 準備的 queue 記憶體、controller 分配的 queue 配額，以及已成功建立的 queue，是三種不同資訊。本冊先說明 SQ 與 CQ 的依賴關係，再討論大小、識別碼、刪除及重設，讓你能判斷何時可以使用 queue，以及何時能安全回收記憶體。</p><p>先練習，再展開解答。各題依需要使用文字、欄位判讀、比較或流程說明，不要求相同的回答項目。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>一條 CQ、兩條 SQ：先建立依賴對象，刪除時則反過來</h2><p class="qa-takeaway">SQ 的命令要透過關聯的 CQ 回報完成。因此，只要仍有 SQ 使用某條 CQ，就不能先刪除那條 CQ。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">觀察層次</th><th scope="col">教學假設</th><th scope="col">可以推論什麼</th></tr></thead><tbody><tr><td>數量配額</td><td>FID07h 回 NSQA=3、NCQA=1</td><td>可建立 4 條 I/O SQ、2 條 I/O CQ；這時還沒有建立 queue</td></tr><tr><td>單一 queue 深度</td><td>Create CQ：QID=1、QSIZE=7</td><td>共有 8 個位置；環狀 queue 須保留一格，用來區分已滿與空佇列</td></tr><tr><td>依賴關係</td><td>SQ1.CQID=1；SQ2.CQID=1</td><td>先建 CQ1，再建 SQ1、SQ2</td></tr><tr><td>回收順序</td><td>刪 SQ1、SQ2，各自等成功完成</td><td>最後再刪 CQ1，並在各 queue 的使用期間結束後回收對應記憶體</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>假設 SQ1 已刪除，但 SQ2 仍存在。這時不能刪除 CQ1，因為 SQ2 還要使用它回報命令結果。另外，SQ1 刪除完成只結束 SQ1 的使用期間，不表示仍由 SQ2 使用的資料 buffer 也可以回收。</p>
<p class="qa-citations">來源：<a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-010">Q10 · Admin Submission Queue 與 Admin Completion Queue 如何透過 AQA、ASQ 及 ACQ 建立？</a></li>
<li><a href="#q-011">Q11 · Admin Queue 與 I/O Queue 的 Size、Base Address 及 Memory Page 對齊有哪些要求？</a></li>
<li><a href="#q-012">Q12 · Host 如何建立 I/O Completion Queue 與 I/O Submission Queue？兩者必須遵守什麼建立順序？</a></li>
<li><a href="#q-013">Q13 · 多個 SQ 共用一個 CQ 與每個 SQ 使用獨立 CQ 有什麼差異？</a></li>
<li><a href="#q-014">Q14 · Host 如何確認 Controller 支援 Physically Contiguous 或其他 Queue 形式？</a></li>
<li><a href="#q-015">Q15 · QID 重複、QID 為 0、CQID 不存在、Queue Size 超過 CAP.MQES 或 Interrupt Vector 非法時，Controller 應如何回應？</a></li>
<li><a href="#q-016">Q16 · Number of Queues Feature 回傳的數值與實際可建立的 Queue 數量有什麼關係？</a></li>
<li><a href="#q-017">Q17 · Host 刪除 I/O Queue 時，SQ 與 CQ 的相依關係如何限制刪除順序？</a></li>
<li><a href="#q-018">Q18 · 刪除不存在的 Queue、仍被 SQ 使用的 CQ 或仍有 Outstanding Command 的 SQ 時，應如何處理？</a></li>
<li><a href="#q-019">Q19 · Queue 刪除後，Controller 是否還能存取原 Queue Memory 或回報原 Queue 的 Completion？</a></li>
<li><a href="#q-020">Q20 · Queue Level Reset 的影響範圍是什麼？Outstanding Command 應如何處理？</a></li>
<li><a href="#q-021">Q21 · Controller Reset 後，原有 I/O Queue 是否有效？Host 需要重新執行哪些操作？</a></li>
</ol></section>
<article class="qa-question" id="q-010" data-question="10" data-answer-kind="process"><h2><a class="qa-qid" href="#q-010">Q10</a> Admin Submission Queue 與 Admin Completion Queue 如何透過 AQA、ASQ 及 ACQ 建立？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-010-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-010-a-01">Create I/O Queue 本身也是 Admin 命令，所以必須先有可用的 Admin Queue，才能建立 I/O Queue。這也是 Admin Queue 需要透過 Register 配置，而不能依賴尚未建立的命令通道來建立自己的原因。</p><div class="qa-sections">
<section class="qa-section" id="q-010-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-010-a-02"></span><p>每個 controller 有 QID=0 的 Admin SQ／CQ；這不是一般 I/O QID。</p>
<span class="qa-anchor" id="q-010-a-03"></span><p>AQA 指定 Admin SQ 與 CQ 各自的長度，ASQ 與 ACQ 則提供各自的實體起始位址。這兩條 queue 必須使用實體連續的記憶體，不能套用 Create I/O Queue 中 PC=0 的 PRP list 建立方式。</p>
<span class="qa-anchor" id="q-010-a-04"></span><p>ASQS、ACQS 均為 zero-based；64 entries 寫 63。Admin SQE 64 bytes、CQE 16 bytes；兩條 queue 可以有不同長度。</p>
</section>
<section class="qa-section" id="q-010-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-010-a-05"></span><p>Host 先配置並初始化記憶體，再於 EN=0 時寫入 AQA、ASQ、ACQ，並把 Admin CQ 的 Phase 初始化為 0。完成 CC 設定後啟用 controller，等到 RDY=1，才提交第一筆 Admin 命令。</p>
<span class="qa-anchor" id="q-010-a-06"></span><p>Host 應能透過 Admin SQ 提交 Identify，並在 Admin CQ 收到 CID 相符的完成結果。ACQ 與 interrupt vector 0 關聯，但 Host 也可以輪詢 Phase 來辨認完成，不一定要等待中斷通知。</p>
</section>
<section class="qa-section" id="q-010-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-010-a-07"></span><p>size=0 編碼的是一個位置，不是停用 queue 的合法方式；以這種配置啟用 controller，結果屬於 undefined behavior。此外，Delete I/O Queue 只用來刪除 I/O Queue，不能用來刪除 Admin Queue。</p>
<span class="qa-anchor" id="q-010-a-16"></span><p>應同時核對 AQA 的長度、實際配置的記憶體與第一筆 CQE。即使 Register 回讀值正確，也還不能證明 controller 真的能存取 Host 提供的記憶體。</p>
</section>
</div>
<span class="qa-anchor" id="q-010-a-17"></span><span class="qa-anchor" id="q-010-a-08"></span><span class="qa-anchor" id="q-010-a-09"></span><span class="qa-anchor" id="q-010-a-10"></span><span class="qa-anchor" id="q-010-a-11"></span><span class="qa-anchor" id="q-010-a-12"></span><span class="qa-anchor" id="q-010-a-13"></span><span class="qa-anchor" id="q-010-a-14"></span><span class="qa-anchor" id="q-010-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-adminreg">Base 2.4 §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</a> · <a href="#ref-init">Base 2.4 §3.5.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-011" data-question="11" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-011">Q11</a> Admin Queue 與 I/O Queue 的 Size、Base Address 及 Memory Page 對齊有哪些要求？</h2>
<p class="qa-prompt">先試著說明欄位的單位與編碼，再用一組數值推導結果。</p>
<details class="qa-answer" id="q-011-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-011-a-01">配置 queue 時，必須分清 entry 數量、每筆 entry 的 bytes 數，以及需要幾個記憶體頁面。這些數量的單位不同；混用時，queue 就可能超出實際配置的記憶體範圍。</p><div class="qa-sections">
<section class="qa-section" id="q-011-s-01" data-answer-section="1"><h3><span>1.</span> 先確認資料的來源與範圍</h3>
<span class="qa-anchor" id="q-011-a-02"></span><p>對齊與大小規則會因 queue 類型及記憶體位置而異。Admin Queue、一般 I/O Queue，以及能力允許時放在 CMB 的 queue，必須分別確認，不能把其中一種配置的規則直接套到其他配置。</p>
<span class="qa-anchor" id="q-011-a-03"></span><p>Admin Queue 的長度限制來自 AQA；I/O Queue 則要核對 CAP.MQES、CQR 與 CC.IOSQES／IOCQES。如果使用 CMB，還須確認 CMBSZ 的 queue 支援能力，以及 CMBLOC.CQDA／CQPDS 定義的例外。</p>
</section>
<section class="qa-section" id="q-011-s-02" data-answer-section="2"><h3><span>2.</span> 欄位、單位與判讀例子</h3>
<span class="qa-anchor" id="q-011-a-04"></span><p>Queue 長度欄位編碼的是 entry 數量減 1。在一般配置中，queue 的基底位址，以及非連續 queue 的各個 PRP 頁面，都要依 CC.MPS 對齊，PRP1 的 offset 則為 0。</p>
<span class="qa-anchor" id="q-011-a-05"></span><p>先決定 queue 有幾個位置、每筆 entry 有多大，再算出所需 bytes 數並配置頁面。如果支援非連續配置，接著建立 PRP list，最後提交 Create 命令。Queue 仍有效時，Host 不得任意修改這份 PRP list。</p>
<span class="qa-anchor" id="q-011-a-06"></span><p>每條 queue 至少需要 2 個位置。Admin Queue 最多有 4096 個位置，I/O Queue 則最多有 min(65536, MQES+1) 個。為了分辨 Full 與 Empty，環狀 queue 還必須保留一個位置不使用。</p>
</section>
<section class="qa-section" id="q-011-s-03" data-answer-section="3"><h3><span>3.</span> 判讀時要保留的條件</h3>
<span class="qa-anchor" id="q-011-a-07"></span><p>I/O queue 大小非法時，回報 Invalid Queue Size（1/02h）；PRP offset 非零時，應回報 PRP Offset Invalid（0/13h）。若 PC 設定違反 CQR 要求，則要分別確認 Create SQ 與 Create CQ 使用的是建議還是強制回覆，不能把兩者的要求強度視為相同。</p>
<span class="qa-anchor" id="q-011-a-16"></span><p>例如，同樣有 128 個位置，NVM SQ 需要 8192 bytes，而 CQ 只需要 2048 bytes。兩者的 QSIZE 雖然都是 127，每筆 entry 的大小卻不同，因此不能只憑 QSIZE 相同，就把所需的記憶體容量算成同一個數值。</p>
</section>
</div>
<span class="qa-anchor" id="q-011-a-17"></span><span class="qa-anchor" id="q-011-a-08"></span><span class="qa-anchor" id="q-011-a-09"></span><span class="qa-anchor" id="q-011-a-10"></span><span class="qa-anchor" id="q-011-a-11"></span><span class="qa-anchor" id="q-011-a-12"></span><span class="qa-anchor" id="q-011-a-13"></span><span class="qa-anchor" id="q-011-a-14"></span><span class="qa-anchor" id="q-011-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-adminreg">Base 2.4 §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</a> · <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-qattr">Base 2.4 §3.3.3–3.4.1</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-012" data-question="12" data-answer-kind="process"><h2><a class="qa-qid" href="#q-012">Q12</a> Host 如何建立 I/O Completion Queue 與 I/O Submission Queue？兩者必須遵守什麼建立順序？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-012-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-012-a-01">SQ 中的命令需要一個有效的 CQ 來回報完成，所以 Host 必須先建立 CQ，才能建立指向它的 SQ。這是物件之間的依賴要求，不只是效能上的建議。</p><div class="qa-sections">
<section class="qa-section" id="q-012-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-012-a-02"></span><p>一個 SQ 在建立時指定其 CQ；多個 SQ 可以指向同一個已存在的 CQ。</p>
<span class="qa-anchor" id="q-012-a-03"></span><p>建立 queue 前，先取得 Number of Queues 配額，再確認 CAP.MQES／CQR、entry 大小與可用的 interrupt vector 範圍。後續 Create 命令的參數必須符合這些限制。</p>
<span class="qa-anchor" id="q-012-a-04"></span><p>Create CQ 用 PRP1、QID、QSIZE、PC、IEN、IV；Create SQ 加上 CQID、QPRIO、NVMSETID。NVMSETID=0 表示沒有指定 Set 關聯。</p>
</section>
<section class="qa-section" id="q-012-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-012-a-05"></span>
<span class="qa-anchor" id="q-012-a-06"></span>
<span class="qa-anchor" id="q-012-a-17"></span>
<figure class="qa-flow" id="q-012-flow"><figcaption>先有 CQ，SQ 才能引用它</figcaption>
<p>箭頭表示必須等前一步完成，不能只依命令提交順序推定物件已經存在。</p><ol class="qa-flow-steps">
<li class="qa-flow-step"><strong>準備 CQ 記憶體</strong><p>依大小與對齊要求配置，並初始化每個 CQE 的 Phase。</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>Create I/O CQ → 等 Admin CQ 回報成功</strong><p>這筆 Create 的完成結果出現在 Admin CQ，不在正在建立的 I/O CQ。</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>Create I/O SQ → 等 Admin CQ 回報成功</strong><p>CQID 指向已成功建立的 CQ；兩筆 Create 的成功 Status 都是 SCT=0、SC=00h。</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>開始 I/O</strong><p>兩步都成功後，才填入 I/O SQE 並更新 SQ Tail Doorbell。</p></li>
</ol><p class="qa-flow-conclusion">若 Create CQ 失敗，就還沒有可供這條 SQ 使用的 CQ。先處理失敗原因；「Create CQ 已提交」不能替代「Create CQ 已成功」。</p></figure>
</section>
<section class="qa-section" id="q-012-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-012-a-07"></span><p>CQID 在支援範圍內但未建立，回 Completion Queue Invalid（1/00h）；CQID=0 或超界回 Invalid Queue Identifier（1/01h）。</p>
<span class="qa-anchor" id="q-012-a-16"></span><p>應確認 Create SQ 的 CQID 與 Host 保存的 SQ→CQ 對照一致。Create CQ 成功只代表該 CQ 已存在，並不會自動把所有 SQ 都連到它。</p>
</section>
</div>
<span class="qa-anchor" id="q-012-a-08"></span><span class="qa-anchor" id="q-012-a-09"></span><span class="qa-anchor" id="q-012-a-10"></span><span class="qa-anchor" id="q-012-a-11"></span><span class="qa-anchor" id="q-012-a-12"></span><span class="qa-anchor" id="q-012-a-13"></span><span class="qa-anchor" id="q-012-a-14"></span><span class="qa-anchor" id="q-012-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-013" data-question="13" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-013">Q13</a> 多個 SQ 共用一個 CQ 與每個 SQ 使用獨立 CQ 有什麼差異？</h2>
<p class="qa-prompt">先說出比較對象最重要的差別，並舉一個不能互相代用的例子。</p>
<details class="qa-answer" id="q-013-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-013-a-01">共用 CQ 可以減少 CQ 資源用量，但也會把多條 SQ 的完成流量集中到同一處。因此，選擇共用或獨立 CQ 時，要考慮資源用量與完成處理能否互相隔離。</p><div class="qa-sections">
<section class="qa-section" id="q-013-s-01" data-answer-section="1"><h3><span>1.</span> 差別在哪裡</h3>
<span class="qa-anchor" id="q-013-a-02"></span><p>多條 SQ 共用的是 CQ 的完成位置及相關通知資源。各條 SQ 仍各自管理 CID，所以不會因此變成共用同一個命令識別空間。</p>
<span class="qa-anchor" id="q-013-a-04"></span><p>Host 以 CQE 的 SQID 與 CID 找到原命令，再以 SQHD 更新該 SQ 已被 controller 消費到的位置。</p>
</section>
<section class="qa-section" id="q-013-s-02" data-answer-section="2"><h3><span>2.</span> 如何選擇與確認</h3>
<span class="qa-anchor" id="q-013-a-03"></span><p>Number of Queues 分別回傳 SQ 與 CQ 的配額；Create SQ 的 CQID 指出它使用哪條 CQ；Create CQ 的 IEN 與 IV 則設定中斷通知。這三組欄位分別處理數量、關聯及通知。</p>
<span class="qa-anchor" id="q-013-a-05"></span><p>先建立 CQ，再建立多條 SQ，並讓它們的 CQID 指向同一個 CQ。Host 讀取 CQE 時，先以 SQID 找出來源 SQ，再處理該命令的完成；處理完畢後，更新共用 CQ 的 Head。</p>
<span class="qa-anchor" id="q-013-a-06"></span><p>例如，SQ1/CID7 與 SQ2/CID7 可以同時存在，Host 必須把回覆各自對回正確的 SQ。這不代表同一條 SQ 也可以在命令尚未完成時，重複使用同一個 CID。</p>
</section>
<section class="qa-section" id="q-013-s-03" data-answer-section="3"><h3><span>3.</span> 哪些結論不能互相套用</h3>
<span class="qa-anchor" id="q-013-a-07"></span><p>合法地共用 CQ 不會造成錯誤。若 Create SQ 指定不存在的 CQID，則使用該命令定義的錯誤 Status。至於共用 CQ 已滿，應按空間不足的處理規則判斷，不能把它當成每條 SQ 都要回報 Invalid Queue Size。</p>
<span class="qa-anchor" id="q-013-a-16"></span><p>應一起觀察 CQ 可用的位置數、各 SQ 的完成流量，以及 Host 處理完成的速度。只知道建立了多少條 SQ，還不足以判斷共用 CQ 是否成為瓶頸。</p>
</section>
</div>
<span class="qa-anchor" id="q-013-a-17"></span><span class="qa-anchor" id="q-013-a-08"></span><span class="qa-anchor" id="q-013-a-09"></span><span class="qa-anchor" id="q-013-a-10"></span><span class="qa-anchor" id="q-013-a-11"></span><span class="qa-anchor" id="q-013-a-12"></span><span class="qa-anchor" id="q-013-a-13"></span><span class="qa-anchor" id="q-013-a-14"></span><span class="qa-anchor" id="q-013-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-014" data-question="14" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-014">Q14</a> Host 如何確認 Controller 支援 Physically Contiguous 或其他 Queue 形式？</h2>
<p class="qa-prompt">先選查詢介面與目標，再說明哪個回傳欄位能支持你的結論。</p>
<details class="qa-answer" id="q-014-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-014-a-01">Host 必須用 controller 支援的方式描述 queue 記憶體。尤其要注意，程式看到的虛擬位址即使連續，底層實體記憶體也不一定連續。</p><div class="qa-sections">
<section class="qa-section" id="q-014-s-01" data-answer-section="1"><h3><span>1.</span> 要查哪個對象、哪份資料</h3>
<span class="qa-anchor" id="q-014-a-02"></span><p>Admin Queue 一律要求實體記憶體連續。I/O Queue 能否使用實體不連續的頁面，則取決於 CAP.CQR，以及 queue 配置在哪一種記憶體中。</p>
<span class="qa-anchor" id="q-014-a-03"></span><p>CQR=1 要求實體連續；CQR=0 允許 I/O 使用非連續頁面。放在 CMB 時還要查 CMBSZ.SQS／CQS、CMBLOC.CQPDS／CQDA。</p>
<span class="qa-anchor" id="q-014-a-04"></span><p>PC 決定 PRP1 的解讀方式：PC=1 時，PRP1 直接指向 queue 的基底位址；PC=0 時，PRP1 指向描述各個 queue 頁面的 PRP list。這裡不能套用一般資料傳輸中 PRP2 的判斷方式。</p>
</section>
<section class="qa-section" id="q-014-s-02" data-answer-section="2"><h3><span>2.</span> 查詢順序與回覆判讀</h3>
<span class="qa-anchor" id="q-014-a-05"></span><p>Host 先確認記憶體位置與支援能力，再建立完整且符合對齊要求的頁面清單，最後提交 Create。Queue 仍在使用期間，清單的位置與內容都必須保留，直到 Delete 成功或重設終止該 queue 為止。</p>
<span class="qa-anchor" id="q-014-a-06"></span><p>建立成功後，controller 應能按照所選的記憶體形式讀取 SQE 或寫入 CQE。不過，Create 成功並不表示 Host 可以在 queue 使用中重新排列頁面。</p>
</section>
<section class="qa-section" id="q-014-s-03" data-answer-section="3"><h3><span>3.</span> 證據不足或不一致時怎麼判斷</h3>
<span class="qa-anchor" id="q-014-a-07"></span><p>CQR=1 且 PC=0：Create CQ 必須（shall）回 Invalid Field（0/02h），Create SQ 的對應要求為建議（should）回覆；不支援的 CMB 用法可能為 Invalid Use of Controller Memory Buffer（0/12h）。</p>
<span class="qa-anchor" id="q-014-a-16"></span><p>驗證時，要把 CAP.CQR、Create 命令的 PC、PRP1 指向的內容，以及實際頁面配置一起核對。只確認 Create 回報成功，還不足以證明 Host 對這些欄位的解讀正確。</p>
<span class="qa-anchor" id="q-014-a-17"></span><p>先確認 PRP1 應該指向 queue 本體，還是 PRP list。如果把兩者弄反，即使位址可存取，controller 讀到的內容仍不是它預期的資料結構。</p>
</section>
</div>
<span class="qa-anchor" id="q-014-a-08"></span><span class="qa-anchor" id="q-014-a-09"></span><span class="qa-anchor" id="q-014-a-10"></span><span class="qa-anchor" id="q-014-a-11"></span><span class="qa-anchor" id="q-014-a-12"></span><span class="qa-anchor" id="q-014-a-13"></span><span class="qa-anchor" id="q-014-a-14"></span><span class="qa-anchor" id="q-014-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-adminreg">Base 2.4 §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-015" data-question="15" data-answer-kind="error"><h2><a class="qa-qid" href="#q-015">Q15</a> QID 重複、QID 為 0、CQID 不存在、Queue Size 超過 CAP.MQES 或 Interrupt Vector 非法時，Controller 應如何回應？</h2>
<p class="qa-prompt">先區分失敗條件，再判斷是否有規範明定的回報結果。</p>
<details class="qa-answer" id="q-015-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-015-a-01">不同的參數錯誤有各自適用的 Status。這題要練習根據錯誤欄位與狀態選擇正確結果，避免把所有情況都歸成 Invalid Field。</p><div class="qa-sections">
<section class="qa-section" id="q-015-s-01" data-answer-section="1"><h3><span>1.</span> 先區分是哪一種失敗</h3>
<span class="qa-anchor" id="q-015-a-02"></span><p>這裡檢查的是透過 Admin Queue 提交的 Create I/O Queue 命令。判斷 QID 是否重複時，SQ 與 CQ 各有自己的識別空間，必須在相同類型內比較。</p>
<span class="qa-anchor" id="q-015-a-04"></span><p>重點檢查 QID、CQID、QSIZE 與 IV，這些參數位於 CDW10／11。同時確認 IOSQES 與 IOCQES 已正確初始化，避免將 entry 大小設定錯誤誤認為個別 queue 參數的問題。</p>
<span class="qa-anchor" id="q-015-a-07"></span><p>同類 QID 重複／0／超範圍：1/01h；QSIZE=0 或超支援：1/02h；合法範圍內 CQID 未建立：1/00h；CQID=0／超界：1/01h；非法 IV：1/08h。多個錯誤同時成立時，除特別規定外由實作選擇回哪個。</p>
</section>
<section class="qa-section" id="q-015-s-02" data-answer-section="2"><h3><span>2.</span> 用哪些資料確認原因</h3>
<span class="qa-anchor" id="q-015-a-03"></span><p>CAP.MQES、Number of Queues 回覆和 PCIe interrupt 配置是合法範圍的依據。</p>
<span class="qa-anchor" id="q-015-a-05"></span><p>先建立一組合法的參數作為比較基準，再一次只改一個條件，例如重複的 QID 或未建立的 CQID。若一筆命令同時有多個錯誤，controller 可能先回報其中另一個錯誤，讓測試結果難以判讀。</p>
</section>
<section class="qa-section" id="q-015-s-03" data-answer-section="3"><h3><span>3.</span> 結果與後續驗證</h3>
<span class="qa-anchor" id="q-015-a-06"></span><p>合法參數回成功並建立指定 queue；失敗後不能把該 QID 當成已建立。</p>
<span class="qa-anchor" id="q-015-a-16"></span><p>若 Error Information Log 有對應紀錄，可用 Parameter Error Location 找出錯誤欄位。但在沒有 More=1 的保證時，不能只因命令失敗，就要求一定新增一筆 Error Information entry。</p>
<span class="qa-anchor" id="q-015-a-17"></span><p>先確認測例確實只有一個非法條件，再核對預期的 SCT。這類命令專用錯誤通常要以 SCT=1 搭配 SC 判讀，不能只比較 SC 數字。</p>
</section>
</div>
<span class="qa-anchor" id="q-015-a-08"></span><span class="qa-anchor" id="q-015-a-09"></span><span class="qa-anchor" id="q-015-a-10"></span><span class="qa-anchor" id="q-015-a-11"></span><span class="qa-anchor" id="q-015-a-12"></span><span class="qa-anchor" id="q-015-a-13"></span><span class="qa-anchor" id="q-015-a-14"></span><span class="qa-anchor" id="q-015-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-irq">PCIe Transport 1.4 §3.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-016" data-question="16" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-016">Q16</a> Number of Queues Feature 回傳的數值與實際可建立的 Queue 數量有什麼關係？</h2>
<p class="qa-prompt">先試著說明欄位的單位與編碼，再用一組數值推導結果。</p>
<details class="qa-answer" id="q-016-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-016-a-01">Host 先向 controller 取得 I/O SQ 與 CQ 的數量配額，再依配額建立 queue。配額只說明可建立的數量，既不代表 queue 已建立，也不代表每條 queue 的深度。</p><div class="qa-sections">
<section class="qa-section" id="q-016-s-01" data-answer-section="1"><h3><span>1.</span> 先確認資料的來源與範圍</h3>
<span class="qa-anchor" id="q-016-a-02"></span><p>FID 07h 作用於 controller，不包含 Admin SQ／CQ。</p>
<span class="qa-anchor" id="q-016-a-03"></span><p>實際分配數量應以 Set Features FID 07h 成功回覆的 CQE DW0 為準，之後也可用 Get Features 讀回。CAP.MQES 則回答另一個問題：每條 I/O Queue 最多可以有幾個 entry。</p>
</section>
<section class="qa-section" id="q-016-s-02" data-answer-section="2"><h3><span>2.</span> 欄位、單位與判讀例子</h3>
<span class="qa-anchor" id="q-016-a-04"></span><p>CDW11 的 NSQR／NCQR 與 DW0 的 NSQA／NCQA 都是 zero-based；回覆可能比要求少，也可能因配置單位而較多。</p>
<span class="qa-anchor" id="q-016-a-05"></span><p>Host 必須在 CLR 之後、任何 I/O Queue 建立之前設定 Number of Queues。第一筆成功的 Set 決定這一輪的配額；直到下一次 CLR 發生前，分配數量都不再改變。</p>
<span class="qa-anchor" id="q-016-a-06"></span><p>例如，DW0=00030007h 表示分配了 4 個 CQ 與 8 個 SQ 的配額。Host 仍須逐一送出 Create 才能建立它們，而 CQ、SQ 的合法 QID 範圍分別依各自配額判斷。</p>
</section>
<section class="qa-section" id="q-016-s-03" data-answer-section="3"><h3><span>3.</span> 重設或斷電時，要確認什麼</h3>
<span class="qa-anchor" id="q-016-a-12"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">觸發方式</th><th scope="col">這項操作或狀態會如何變化</th></tr></thead><tbody><tr><td>Controller Reset 後是否保留或繼續？</td><td>Controller Level Reset 後，第一筆成功的 Set FID07h 會重新配置 queue 數量。Host 應使用這次的回覆重建 I/O queue，不能直接沿用前一次的配額。</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-016-s-04" data-answer-section="4"><h3><span>4.</span> 判讀時要保留的條件</h3>
<span class="qa-anchor" id="q-016-a-07"></span><p>若已建立 I/O Queue 才送出 Set，controller 必須回傳 Command Sequence Error（0/0Ch）。若要求值為 FFFFh，則建議回傳 Invalid Field（0/02h）。在尚未建立 queue 的情況下，再次送出 Set 應可成功，但不改變第一筆成功 Set 所決定的配額。</p>
<span class="qa-anchor" id="q-016-a-16"></span><p>應分別保存回覆的配額、目前已建立的 queue 清單，以及 MQES 限制。Get Features 回報的是配額，不能將它解讀成目前實際存在的 queue 數量。</p>
</section>
</div>
<span class="qa-anchor" id="q-016-a-17"></span><span class="qa-anchor" id="q-016-a-08"></span><span class="qa-anchor" id="q-016-a-09"></span><span class="qa-anchor" id="q-016-a-10"></span><span class="qa-anchor" id="q-016-a-11"></span><span class="qa-anchor" id="q-016-a-13"></span><span class="qa-anchor" id="q-016-a-14"></span><span class="qa-anchor" id="q-016-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-017" data-question="17" data-answer-kind="process"><h2><a class="qa-qid" href="#q-017">Q17</a> Host 刪除 I/O Queue 時，SQ 與 CQ 的相依關係如何限制刪除順序？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-017-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-017-a-01">Host 必須先刪除依賴 CQ 的 SQ，才能刪除該 CQ。這個順序可避免 SQ 還有命令需要回報時，完成結果的目的地卻已不存在。</p><div class="qa-sections">
<section class="qa-section" id="q-017-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-017-a-02"></span><p>一個 CQ 可能同時被多條 SQ 使用，因此要先刪除所有指向它的 SQ。只刪除與 CQ 具有相同 QID 的 SQ，並不足以滿足這個條件。</p>
<span class="qa-anchor" id="q-017-a-03"></span><p>使用 Host 在 Create SQ 時保存的 SQ→CQID 對照；Number of Queues 不提供這張連線清單。</p>
<span class="qa-anchor" id="q-017-a-04"></span><p>Delete I/O SQ／CQ 的 CDW10.QID 指定對象；它們都透過 Admin SQ 提交。</p>
</section>
<section class="qa-section" id="q-017-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-017-a-05"></span><p>Host 先停止向目標 SQ 提交新命令，並適當等待既有命令處理完畢。接著逐一送出 Delete SQ 並等待成功，處理仍需讀取的舊完成結果，最後才送出 Delete CQ。</p>
<span class="qa-anchor" id="q-017-a-06"></span><p>Delete SQ 成功，表示該 SQ 的命令處理已到達規範定義的終止點。Delete CQ 成功後，Host 才能收回該 CQ 的 PRP list 與 queue 資源；兩個完成點不能互相代替。</p>
</section>
<section class="qa-section" id="q-017-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-017-a-07"></span><p>尚有相關 SQ 時 Delete CQ 必須回 Invalid Queue Deletion（1/0Ch）；QID=0 或非法對象回 Invalid Queue Identifier（1/01h）。</p>
<span class="qa-anchor" id="q-017-a-16"></span><p>應比較 Delete 成功回覆與記憶體釋放的先後時間。只要刪除命令尚未成功，Host 就不能僅憑「已送出 Delete」而提前回收裝置可能仍會存取的記憶體。</p>
</section>
</div>
<span class="qa-anchor" id="q-017-a-17"></span><span class="qa-anchor" id="q-017-a-08"></span><span class="qa-anchor" id="q-017-a-09"></span><span class="qa-anchor" id="q-017-a-10"></span><span class="qa-anchor" id="q-017-a-11"></span><span class="qa-anchor" id="q-017-a-12"></span><span class="qa-anchor" id="q-017-a-13"></span><span class="qa-anchor" id="q-017-a-14"></span><span class="qa-anchor" id="q-017-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-018" data-question="18" data-answer-kind="error"><h2><a class="qa-qid" href="#q-018">Q18</a> 刪除不存在的 Queue、仍被 SQ 使用的 CQ 或仍有 Outstanding Command 的 SQ 時，應如何處理？</h2>
<p class="qa-prompt">先區分失敗條件，再判斷是否有規範明定的回報結果。</p>
<details class="qa-answer" id="q-018-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-018-a-01">仍有未完成命令，不會直接讓 Delete SQ 變成非法操作。判斷時應分清楚：刪除要求本身不合法，與合法刪除導致原命令終止，是兩種不同情況。</p><div class="qa-sections">
<section class="qa-section" id="q-018-s-01" data-answer-section="1"><h3><span>1.</span> 先區分是哪一種失敗</h3>
<span class="qa-anchor" id="q-018-a-02"></span><p>刪除 SQ 會影響該 SQ 中尚未完成的 I/O。刪除 CQ 則另有前提：所有依賴它的 SQ 都必須已被刪除，才能繼續進行。</p>
<span class="qa-anchor" id="q-018-a-04"></span><p>Delete 的 QID 必須有效且不為 0；目標 I/O 命令仍以各自 SQID／CID 辨識。</p>
<span class="qa-anchor" id="q-018-a-07"></span><p>QID 非法時回報 1/01h；CQ 仍被 SQ 使用時回報 1/0Ch。原 I/O 命令若因刪除 SQ 而中止，可以透過 CQE 回報 Command Aborted due to SQ Deletion（0/08h），也可能在 Delete 成功時依規則形成隱含完成，沒有各自的 CQE。</p>
</section>
<section class="qa-section" id="q-018-s-02" data-answer-section="2"><h3><span>2.</span> 用哪些資料確認原因</h3>
<span class="qa-anchor" id="q-018-a-03"></span><p>先檢查 Host 記錄的 queue 建立與刪除結果，以及尚未完成的命令。這些是目前的執行狀態，不能只靠 Identify 的選配能力位得知。</p>
<span class="qa-anchor" id="q-018-a-05"></span><p>正常拆除時，Host 先等待既有工作完成，再刪除 queue。如果目的是中止工作而直接刪除 SQ，則在 Delete 成功後，將仍未收到 CQE 的原命令視為已隱含中止。</p>
</section>
<section class="qa-section" id="q-018-s-03" data-answer-section="3"><h3><span>3.</span> 結果與後續驗證</h3>
<span class="qa-anchor" id="q-018-a-06"></span><p>在 Delete SQ 成功之前，原命令可能正常完成，也可能收到表示中止的 CQE。但是 Delete SQ 一旦成功，controller 就不得再為那些原 SQ 命令寫入新的 completion。</p>
<span class="qa-anchor" id="q-018-a-16"></span><p>驗證時，應把已收到 CQE 的命令，以及 Delete 成功後被視為隱含中止的命令，一起納入統計。不能只計算實際 CQE，並要求每筆原命令都一定有獨立回覆。</p>
<span class="qa-anchor" id="q-018-a-17"></span><p>先檢查 Delete SQ 是否已成功完成；在它還 outstanding 時，不能宣布所有原命令已停止。</p>
</section>
</div>
<span class="qa-anchor" id="q-018-a-08"></span><span class="qa-anchor" id="q-018-a-09"></span><span class="qa-anchor" id="q-018-a-10"></span><span class="qa-anchor" id="q-018-a-11"></span><span class="qa-anchor" id="q-018-a-12"></span><span class="qa-anchor" id="q-018-a-13"></span><span class="qa-anchor" id="q-018-a-14"></span><span class="qa-anchor" id="q-018-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-019" data-question="19" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-019">Q19</a> Queue 刪除後，Controller 是否還能存取原 Queue Memory 或回報原 Queue 的 Completion？</h2>
<p class="qa-prompt">先用自己的話解釋機制，再舉一個常見誤解。</p>
<details class="qa-answer" id="q-019-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-019-a-01">刪除 queue 後能否回收記憶體，取決於刪除是否已成功完成。判斷違規存取時，也必須區分：CQE 是先前已寫入、只是 Host 較晚讀到，還是真的在刪除成功後才寫入。</p><div class="qa-sections">
<section class="qa-section" id="q-019-s-01" data-answer-section="1"><h3><span>1.</span> 機制與適用範圍</h3>
<span class="qa-anchor" id="q-019-a-02"></span><p>刪除 SQ 不會一併刪除它使用的 CQ。如果 CQ 仍存在，其中先前已寫入的完成結果，仍可能等待 Host 處理。</p>
<span class="qa-anchor" id="q-019-a-04"></span><p>Host 需要追蹤被刪除的 QID、關聯 CQID、PRP list 位址，以及記憶體何時可回收。即使同一位址稍後用來建立新 queue，也必須能分辨它屬於哪一輪配置。</p>
</section>
<section class="qa-section" id="q-019-s-02" data-answer-section="2"><h3><span>2.</span> 用操作與結果理解</h3>
<span class="qa-anchor" id="q-019-a-03"></span><p>以 Admin CQ 回報 Delete 成功的時點，判斷 queue 的刪除是否完成。Host 送出 Delete 的時間，或自行設定的 timeout 到期，都不能代替這個完成結果。</p>
<span class="qa-anchor" id="q-019-a-05"></span><p>先停止提交新命令，再送出 Delete 並等待成功，之後才回收對應的 queue 記憶體與 PRP list。若只刪除 SQ，而 CQ 仍存在，Host 還須處理其中先前已寫入的完成結果。</p>
<span class="qa-anchor" id="q-019-a-06"></span><p>Delete SQ 成功後，controller 不得再為原 SQ 的命令新增 completion。Delete CQ 成功後，Host 可釋放其 PRP list 與記憶體，controller 也不能再把已刪除的 queue 當作可存取的 DMA 目標。</p>
</section>
<section class="qa-section" id="q-019-s-03" data-answer-section="3"><h3><span>3.</span> 容易誤判的地方</h3>
<span class="qa-anchor" id="q-019-a-07"></span><p>若 Delete 本身失敗或沒有完成，不能推論記憶體已可收回。逾時不是另一種 Successful Completion。</p>
<span class="qa-anchor" id="q-019-a-16"></span><p>應一併核對 CQE 的寫入時間、Phase、Delete 完成時間，以及 Host 實際讀取 CQE 的時間。Host 較晚處理到舊 CQE，並不等於 controller 在刪除成功後才違規寫入。</p>
</section>
</div>
<span class="qa-anchor" id="q-019-a-17"></span><span class="qa-anchor" id="q-019-a-08"></span><span class="qa-anchor" id="q-019-a-09"></span><span class="qa-anchor" id="q-019-a-10"></span><span class="qa-anchor" id="q-019-a-11"></span><span class="qa-anchor" id="q-019-a-12"></span><span class="qa-anchor" id="q-019-a-13"></span><span class="qa-anchor" id="q-019-a-14"></span><span class="qa-anchor" id="q-019-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-020" data-question="20" data-answer-kind="process"><h2><a class="qa-qid" href="#q-020">Q20</a> Queue Level Reset 的影響範圍是什麼？Outstanding Command 應如何處理？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-020-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-020-a-01">Queue Level Reset 可在不重設整個 controller 的情況下，重新建立 I/O Queue。對 PCIe 而言，這個流程是刪除後再建立 queue，並沒有另一個專用的 Reset opcode。</p><div class="qa-sections">
<section class="qa-section" id="q-020-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-020-a-02"></span><p>影響範圍包括目標 queue，以及重建時必須一併處理的相關 queue。例如，若要重建 CQ，就要先刪除所有使用它的 SQ；等 CQ 重建完成後，再重建這些 SQ。</p>
<span class="qa-anchor" id="q-020-a-03"></span><p>依既有 SQ 與 CQ 的關聯，以及 Create／Delete 的順序規則執行。這個流程不依靠另一個獨立的 Queue Reset Feature。</p>
<span class="qa-anchor" id="q-020-a-04"></span><p>流程會使用 Delete SQ／CQ 與 Create CQ／SQ。雖然 QID 可以重用，但新 queue 的記憶體與指標都屬於新一輪配置，不能接續上一輪的命令狀態。</p>
</section>
<section class="qa-section" id="q-020-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-020-a-05"></span><p>正常情況下，Host 先讓既有工作完成，再刪除 queue。若必須中止工作，則依 Delete SQ 的明確或隱含完成規則處理。重建時先初始化新 CQ 的 Phase，建立 CQ，最後才建立依賴它的 SQ。</p>
<span class="qa-anchor" id="q-020-a-06"></span><p>重建成功後新命令可執行，原 outstanding 命令不會自動搬入新 SQ。</p>
</section>
<section class="qa-section" id="q-020-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-020-a-07"></span><p>若 CQ 仍被 SQ 使用就嘗試刪除，會遇到 1/0Ch；若沒有有效 CQ 就建立 SQ，則依 CQID 的錯誤條件回覆。Queue Level Reset 是由這些命令組成的流程，本身沒有額外、統一的 Status。</p>
<span class="qa-anchor" id="q-020-a-16"></span><p>核對刪除／建立順序與新舊 CID 對照，並檢查其他獨立 queue 是否保持正常。</p>
</section>
</div>
<span class="qa-anchor" id="q-020-a-17"></span><span class="qa-anchor" id="q-020-a-08"></span><span class="qa-anchor" id="q-020-a-09"></span><span class="qa-anchor" id="q-020-a-10"></span><span class="qa-anchor" id="q-020-a-11"></span><span class="qa-anchor" id="q-020-a-12"></span><span class="qa-anchor" id="q-020-a-13"></span><span class="qa-anchor" id="q-020-a-14"></span><span class="qa-anchor" id="q-020-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-021" data-question="21" data-answer-kind="process"><h2><a class="qa-qid" href="#q-021">Q21</a> Controller Reset 後，原有 I/O Queue 是否有效？Host 需要重新執行哪些操作？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-021-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-021-a-01">Host 必須把重設前的命令與恢復後的新命令分開追蹤，才能避免把記憶體中殘留的 completion 誤認成新命令的結果。</p><div class="qa-sections">
<section class="qa-section" id="q-021-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-021-a-02"></span><p>Controller Level Reset 刪除該 controller 的全部 I/O SQ／CQ；不同於只刪除一條 SQ。</p>
<span class="qa-anchor" id="q-021-a-03"></span><p>恢復後應重新查詢必要的 Identify 資訊，並確認 Number of Queues 配額、entry 大小與中斷設定。不能未經確認，就假設上一輪設定仍可直接使用。</p>
<span class="qa-anchor" id="q-021-a-04"></span><p>重建流程需要先設定 Admin Queue Register 與 CC，再視需要使用 Get／Set Features，最後以 Create CQ／SQ 建立 I/O 通道。這些步驟共同構成恢復流程，不能只做其中一部分。</p>
</section>
<section class="qa-section" id="q-021-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-021-a-05"></span><p>Host 先確認 RDY=0，初始化 Admin CQ 的 Phase 與 CC，再啟用 controller 並等待就緒。接著恢復必要的 Feature、設定 Number of Queues，依序建立 CQ、SQ。只有完成上述步驟後，才能允許新的 I/O 提交。</p>
<span class="qa-anchor" id="q-021-a-06"></span><p>每筆 Create 都必須先在 Admin CQ 成功完成，對應的新 queue 才能使用。即使沿用相同 QID 或位址，也不能跳過這個完成確認。</p>
</section>
<section class="qa-section" id="q-021-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-021-a-07"></span><p>直接更新舊 queue 的 Doorbell，不是合法的恢復流程，不能要求 controller 繼續處理該 queue。若是在重新建立 queue 時命令失敗，則依對應 Create 命令的 Status 處理。</p>
<span class="qa-anchor" id="q-021-a-16"></span><p>Host 應保存重設前後的 queue 建立紀錄與命令對照，用來區分新舊配置。這是 Host 自行管理的追蹤資訊，不是要求在 NVMe 傳輸格式中新增欄位。</p>
</section>
</div>
<span class="qa-anchor" id="q-021-a-17"></span><span class="qa-anchor" id="q-021-a-08"></span><span class="qa-anchor" id="q-021-a-09"></span><span class="qa-anchor" id="q-021-a-10"></span><span class="qa-anchor" id="q-021-a-11"></span><span class="qa-anchor" id="q-021-a-12"></span><span class="qa-anchor" id="q-021-a-13"></span><span class="qa-anchor" id="q-021-a-14"></span><span class="qa-anchor" id="q-021-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-init">Base 2.4 §3.5.1</a> · <a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>

<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-cap"><strong>Base 2.4 · §3.1.4 (CAP, VS)</strong><br>文件頁 54–59 · PDF 80–85 · Figure 36–37</li>
<li id="ref-adminreg"><strong>Base 2.4 · §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</strong><br>文件頁 66–68 · PDF 92–94 · Figure 44–47</li>
<li id="ref-queue"><strong>Base 2.4 · §3.3.1</strong><br>文件頁 88–91 · PDF 114–117 · Figure 73–74</li>
<li id="ref-qattr"><strong>Base 2.4 · §3.3.3–3.4.1</strong><br>文件頁 101 · PDF 127</li>
<li id="ref-init"><strong>Base 2.4 · §3.5.1</strong><br>文件頁 105–106 · PDF 131–132</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>文件頁 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>文件頁 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-featureeffects"><strong>Base 2.4 · §5.2.13.1.18</strong><br>文件頁 276–278 · PDF 302–304 · Figure 270–271</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>文件頁 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-number"><strong>Base 2.4 · §5.2.30.1.5</strong><br>文件頁 465–466 · PDF 491–492 · Figure 472–473</li>
<li id="ref-create"><strong>Base 2.4 · §5.3.1–5.3.2</strong><br>文件頁 527–531 · PDF 553–557 · Figure 571–579</li>
<li id="ref-delete"><strong>Base 2.4 · §5.3.3–5.3.4</strong><br>文件頁 531–532 · PDF 557–558 · Figure 580–583</li>
<li id="ref-fatal"><strong>Base 2.4 · §9.1–9.6.1</strong><br>文件頁 825–826 · PDF 851–852</li>
<li id="ref-irq"><strong>PCIe Transport 1.4 · §3.5</strong><br>文件頁 13–16 · PDF 13–16 · Figure 9</li>
</ul><h3>需要看欄位圖時</h3><p>以下連結可開啟對應的圖表教學，查閱欄位及判讀方式。每張圖保留固定的教學位置，方便之後反覆查詢。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b44">Base 2.4 Figure 44 · Offset 24h: AQA – Admin Queue Attributes</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b45">Base 2.4 Figure 45 · Offset 28h: ASQ – Admin Submission Queue Base Address</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b46">Base 2.4 Figure 46 · Offset 30h: ACQ – Admin Completion Queue Base Address</a></li>
<li><a href="/nvme/figure-reference/features/zh-tw/#figure-b473">Base 2.4 Figure 473 · Number of Queues – Completion Queue Entry Dword 0</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/queues/en/">English</a><a href="/DOCS/nvme-question-bank/queues.html">繁中教學 HTML</a></nav>
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
