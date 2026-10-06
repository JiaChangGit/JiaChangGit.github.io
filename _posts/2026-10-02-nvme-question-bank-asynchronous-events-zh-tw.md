---
layout: post
title: "NVMe 自問自答題庫：Asynchronous Event Request"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/asynchronous-events/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/asynchronous-events/en/">English</a><a href="/DOCS/nvme-question-bank/asynchronous-events.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q82–Q92</p><h1>Asynchronous Event Request</h1><p class="qr-intro">AER 讓 Host 先留下等待通知的請求，controller 有事件時才完成它。先理解請求、事件、Log 與確認的關係，再處理多事件、遮蔽與重新掛入。</p><p>先練習，再展開解答。各題依需要使用文字、欄位判讀、比較或流程說明，不要求相同的回答項目。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>通知完成後，工作還沒結束</h2><p class="qa-takeaway">AER 回報事件線索；詳細內容與目前狀態仍要讀相應 Log。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">階段</th><th scope="col">Host 或 Controller 動作</th><th scope="col">需要保存的資訊</th></tr></thead><tbody><tr><td>事前</td><td>Host 提交 AER</td><td>請求 CID 與上限 AERL+1</td></tr><tr><td>事件發生</td><td>Controller 完成適用請求</td><td>Type、Information、LID</td></tr><tr><td>查證</td><td>Host 讀對應 Log</td><td>selector、RAE 與原始內容</td></tr><tr><td>繼續接收</td><td>Host 重新掛 AER</td><td>新的 outstanding 請求</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>假設 AERL=3，允許上限是 4 筆。完成一筆後，Host 可補回一筆；不能把已完成但未補掛的請求仍算成可接收下一事件的空間。</p>
<p class="qa-citations">來源：<a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-082">Q82 · Host 為什麼需要預先送出 Asynchronous Event Request？沒有事件時為何保持 Outstanding？</a></li>
<li><a href="#q-083">Q83 · 事件發生後，Host 如何從 AER Completion 取得事件種類與 Log 位置？</a></li>
<li><a href="#q-084">Q84 · Host 處理事件後，為什麼需要讀取對應 Log 並重新送出 AER？</a></li>
<li><a href="#q-085">Q85 · AER Request 數量超過 Controller 上限時，應如何回應？</a></li>
<li><a href="#q-086">Q86 · 沒有掛入 AER 時發生事件，Controller 如何保留與回報？</a></li>
<li><a href="#q-087">Q87 · 多個相同或不同事件同時發生時，Controller 如何合併與回報？</a></li>
<li><a href="#q-088">Q88 · Asynchronous Event Configuration 如何啟用或遮蔽特定事件？</a></li>
<li><a href="#q-089">Q89 · SMART、Namespace、Firmware、Telemetry、Sanitize、Self-test 與 PEL 各有哪些通知條件？</a></li>
<li><a href="#q-090">Q90 · Host 讀取 Log 後，事件如何清除或保留？</a></li>
<li><a href="#q-091">Q91 · AER 能否被 Abort？Reset 時尚未完成的 Request 如何處理？</a></li>
<li><a href="#q-092">Q92 · AER 已完成，但對應 Log 看不到預期資訊時，應如何定位？</a></li>
</ol></section>
<article class="qa-question" id="q-082" data-question="82" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-082">Q82</a> Host 為什麼需要預先送出 Asynchronous Event Request？沒有事件時為何保持 Outstanding？</h2>
<p class="qa-prompt">先用自己的話解釋機制，再舉一個常見誤解。</p>
<details class="qa-answer" id="q-082-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-082-a-01">AER 提供 controller 可使用的通知回覆機會。controller 不能在沒有對應 Request 的情況下，任意產生一筆一般 AER completion，因此 Host 先提交 Request，等待日後事件。</p><div class="qa-sections">
<section class="qa-section" id="q-082-s-01" data-answer-section="1"><h3><span>1.</span> 機制與適用範圍</h3>
<span class="qa-anchor" id="q-082-a-02"></span><p>每筆 AER 屬於提交它的 controller 與 Admin Queue。它等待的是事件，不是對某個 namespace 執行讀寫。</p>
<span class="qa-anchor" id="q-082-a-04"></span><p>AER 的命令特定欄位都是 Reserved；Host 仍需分配 Admin SQ 中唯一的 CID。事件發生後，DW0 的 AET／AEI／LID 與必要的 DW1 描述結果。</p>
</section>
<section class="qa-section" id="q-082-s-02" data-answer-section="2"><h3><span>2.</span> 用操作與結果理解</h3>
<span class="qa-anchor" id="q-082-a-03"></span><p>Identify.AERL+1 是同時未完成 Request 的上限。選配通知另查 OAES 與 FID0Bh，不能把 AERL 當成事件種類數。</p>
<span class="qa-anchor" id="q-082-a-05"></span><p>完成初始化及通知設定後，提交不超過上限的 AER。收到事件時保存回覆，處理並確認事件，再補上 Request，維持可用的通知機會。</p>
<span class="qa-anchor" id="q-082-a-06"></span><p>沒有事件時長時間保持 outstanding 是正常行為，Host 不應替 AER 設一般命令 timeout。它不需要定期回成功來證明自己仍存在。</p>
</section>
<section class="qa-section" id="q-082-s-03" data-answer-section="3"><h3><span>3.</span> 容易誤判的地方</h3>
<span class="qa-anchor" id="q-082-a-07"></span><p>超過並行上限時，會涉及 Asynchronous Event Request Limit Exceeded（1/05h）。尚未有事件而未完成，則不是 Command Timeout 的規範錯誤結果。</p>
<span class="qa-anchor" id="q-082-a-16"></span><p>比對 Host 尚未完成的 AER 數、AERL、通知設定與事件條件，而不是只計算命令已等待幾秒。</p>
</section>
</div>
<span class="qa-anchor" id="q-082-a-17"></span><span class="qa-anchor" id="q-082-a-08"></span><span class="qa-anchor" id="q-082-a-09"></span><span class="qa-anchor" id="q-082-a-10"></span><span class="qa-anchor" id="q-082-a-11"></span><span class="qa-anchor" id="q-082-a-12"></span><span class="qa-anchor" id="q-082-a-13"></span><span class="qa-anchor" id="q-082-a-14"></span><span class="qa-anchor" id="q-082-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-083" data-question="83" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-083">Q83</a> 事件發生後，Host 如何從 AER Completion 取得事件種類與 Log 位置？</h2>
<p class="qa-prompt">先試著說明欄位的單位與編碼，再用一組數值推導結果。</p>
<details class="qa-answer" id="q-083-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-083-a-01">Completion 的成功 Status 只表示 AER 正常完成；真正的通知內容放在命令特定結果中。必須再解析事件欄位，才能知道要讀哪張 Log。</p><div class="qa-sections">
<section class="qa-section" id="q-083-s-01" data-answer-section="1"><h3><span>1.</span> 先確認資料的來源與範圍</h3>
<span class="qa-anchor" id="q-083-a-02"></span><p>以 AER 的 SQID 與 CID 找到原 Request，再解讀這個 controller 回報的事件。不能把另一筆普通 Admin 命令的 DW0 當成 AER 格式。</p>
<span class="qa-anchor" id="q-083-a-03"></span><p>支援的事件種類由能力及 Figure 153～160 等事件表定義。先解 AET，再用它選 AEI 的對應表。</p>
</section>
<section class="qa-section" id="q-083-s-02" data-answer-section="2"><h3><span>2.</span> 欄位、單位與判讀例子</h3>
<span class="qa-anchor" id="q-083-a-04"></span><p>DW0 bits2:0 是 AET、bits15:8 是 AEI、bits23:16 是 LID。DW1 是事件特定參數；若事件沒有定義它，不能自行當成 NSID。</p>
<span class="qa-anchor" id="q-083-a-05"></span><p>先驗 CQE 的 Phase 與命令身分，再解 SCT／SC。正常 AER completion 才進一步解事件內容，依事件表讀取 Log 或執行對應處理。</p>
<span class="qa-anchor" id="q-083-a-06"></span><p>例如 AET=Notice、AEI=Firmware Activation Starting，指向 Firmware Slot Information；它表示開始啟用，不表示新韌體已啟用完成。Sanitize 的事件也要搭配 DW1 的 target 定義。</p>
</section>
<section class="qa-section" id="q-083-s-03" data-answer-section="3"><h3><span>3.</span> 判讀時要保留的條件</h3>
<span class="qa-anchor" id="q-083-a-07"></span><p>若 AER 本身以 1/05h 等錯誤完成，不能把 DW0 任意解成正常事件。AEI 的相同數值在不同 AET 下也可能代表不同事情。</p>
<span class="qa-anchor" id="q-083-a-16"></span><p>保存完整 CQE 與後續 Log，核對事件所指的 LID 及 target，而不是只保留翻譯過的一行訊息。</p>
</section>
</div>
<span class="qa-anchor" id="q-083-a-17"></span><span class="qa-anchor" id="q-083-a-08"></span><span class="qa-anchor" id="q-083-a-09"></span><span class="qa-anchor" id="q-083-a-10"></span><span class="qa-anchor" id="q-083-a-11"></span><span class="qa-anchor" id="q-083-a-12"></span><span class="qa-anchor" id="q-083-a-13"></span><span class="qa-anchor" id="q-083-a-14"></span><span class="qa-anchor" id="q-083-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-084" data-question="84" data-answer-kind="process"><h2><a class="qa-qid" href="#q-084">Q84</a> Host 處理事件後，為什麼需要讀取對應 Log 並重新送出 AER？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-084-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-084-a-01">讀取 Log 用來了解並確認事件；重新提交 AER 則提供下一次回報機會。兩個動作目的不同，少做其中一個都可能讓後續通知看似停止。</p><div class="qa-sections">
<section class="qa-section" id="q-084-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-084-a-02"></span><p>一般事件回報後，相關事件類型會被自動遮蔽，直到 Host 按規則確認。Immediate 與 One-Shot 另有規則，不能套用相同清除流程。</p>
<span class="qa-anchor" id="q-084-a-03"></span><p>確認此事件對應的 LID、RAE 規則與通知啟用狀態。AERL 只限制等待中的 Request，不能解除事件遮蔽。</p>
<span class="qa-anchor" id="q-084-a-04"></span><p>一般使用 Get Log Page 並以 RAE=0 確認；RAE=1 保留事件。新的 AER 是另一個 Admin 命令，必須有自己的有效 CID。</p>
</section>
<section class="qa-section" id="q-084-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-084-a-05"></span>
<span class="qa-anchor" id="q-084-a-06"></span>
<span class="qa-anchor" id="q-084-a-17"></span>
<figure class="qa-flow" id="q-084-flow"><figcaption>事件確認與補上 AER 是兩件事</figcaption>
<p>這是一般需透過 Log 確認的事件路徑；Immediate 與 One-Shot 須另依各自規則處理。</p><ol class="qa-flow-steps">
<li class="qa-flow-step"><strong>收到 AER Completion → 保存通知</strong><p>先記錄事件種類、資訊與 LID，再讀取所需診斷內容。</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>依事件規則確認</strong><p>通常以成功的 Get Log Page、RAE=0 確認。RAE=1 是保留；讀取失敗也不能當作已確認。</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>維持等待中的 AER</strong><p>重新提供 Request，才能接收後續回報；補 Request 本身不會確認上一個事件。</p></li>
</ol><p class="qa-flow-conclusion">若警告條件持續存在，確認後仍可能再通知。確認前應考慮門檻或通知設定，避免反覆回報；檢查時分開確認「資訊已保存、事件已確認、Request 仍在等待」。</p></figure>
</section>
<section class="qa-section" id="q-084-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-084-a-07"></span><p>讀取失敗時事件必須保留，不能把嘗試過 RAE=0 當成清除成功。若是 One-Shot，則在回報時已清除，應依該事件處理。</p>
<span class="qa-anchor" id="q-084-a-16"></span><p>檢查三件事是否都完成：事件資訊已保存、確認動作成功、仍有 AER 等待。它們不是同一個成功碼能證明的事情。</p>
</section>
</div>
<span class="qa-anchor" id="q-084-a-08"></span><span class="qa-anchor" id="q-084-a-09"></span><span class="qa-anchor" id="q-084-a-10"></span><span class="qa-anchor" id="q-084-a-11"></span><span class="qa-anchor" id="q-084-a-12"></span><span class="qa-anchor" id="q-084-a-13"></span><span class="qa-anchor" id="q-084-a-14"></span><span class="qa-anchor" id="q-084-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-085" data-question="85" data-answer-kind="error"><h2><a class="qa-qid" href="#q-085">Q85</a> AER Request 數量超過 Controller 上限時，應如何回應？</h2>
<p class="qa-prompt">先區分失敗條件，再判斷是否有規範明定的回報結果。</p>
<details class="qa-answer" id="q-085-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-085-a-01">AER 上限限制 controller 必須維護的等待命令數，避免 Host 無限制占用回報資源。這個數量與內部可能發生多少事件不同。</p><div class="qa-sections">
<section class="qa-section" id="q-085-s-01" data-answer-section="1"><h3><span>1.</span> 先區分是哪一種失敗</h3>
<span class="qa-anchor" id="q-085-a-02"></span><p>上限適用此 controller 同時 outstanding 的 AER，不是整個 subsystem 曾提交過的累計數。</p>
<span class="qa-anchor" id="q-085-a-04"></span><p>Host 追蹤每個 AER 的 CID、提交與完成時間。已完成的 Request 不再占用 outstanding 名額，補送前須先更新追蹤紀錄。</p>
<span class="qa-anchor" id="q-085-a-07"></span><p>超過上限的命令對應 Asynchronous Event Request Limit Exceeded（SCT=1, SC=05h）。不要將它與 Abort Command Limit Exceeded（1/03h）混用。</p>
</section>
<section class="qa-section" id="q-085-s-02" data-answer-section="2"><h3><span>2.</span> 用哪些資料確認原因</h3>
<span class="qa-anchor" id="q-085-a-03"></span><p>Identify.AERL 是 zero-based，實際上限為 AERL+1。例如 AERL=3，最多同時保留 4 筆未完成 AER。</p>
<span class="qa-anchor" id="q-085-a-05"></span><p>先讀 AERL，再建立不超過上限的等待集合。驗證超限行為時，只額外提交一筆，並排除同時有事件完成 Request 的競爭情況。</p>
</section>
<section class="qa-section" id="q-085-s-03" data-answer-section="3"><h3><span>3.</span> 結果與後續驗證</h3>
<span class="qa-anchor" id="q-085-a-06"></span><p>合法上限內且沒有事件時，Request 正常等待。若同時有一筆完成，後來提交的新 Request 可能仍在合法上限內，不能只看總提交次數判斷。</p>
<span class="qa-anchor" id="q-085-a-16"></span><p>將 AERL+1 與每個時間點的未完成數比對，並保存回報事件造成的名額變化。</p>
<span class="qa-anchor" id="q-085-a-17"></span><p>先確認 AERL 已加 1，且 Host 沒把已完成 Request 繼續算在等待集合中。</p>
</section>
</div>
<span class="qa-anchor" id="q-085-a-08"></span><span class="qa-anchor" id="q-085-a-09"></span><span class="qa-anchor" id="q-085-a-10"></span><span class="qa-anchor" id="q-085-a-11"></span><span class="qa-anchor" id="q-085-a-12"></span><span class="qa-anchor" id="q-085-a-13"></span><span class="qa-anchor" id="q-085-a-14"></span><span class="qa-anchor" id="q-085-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-086" data-question="86" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-086">Q86</a> 沒有掛入 AER 時發生事件，Controller 如何保留與回報？</h2>
<p class="qa-prompt">先用自己的話解釋機制，再舉一個常見誤解。</p>
<details class="qa-answer" id="q-086-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-086-a-01">這题区分事件發生與通知送達。沒有 Request，不表示事件一定沒發生；但也不能要求每種事件都永久排隊等待。</p><div class="qa-sections">
<section class="qa-section" id="q-086-s-01" data-answer-section="1"><h3><span>1.</span> 機制與適用範圍</h3>
<span class="qa-anchor" id="q-086-a-02"></span><p>一般事件、Immediate 與 One-Shot 的規則不同；還要確認事件原本已啟用，且不是被遮蔽的重複通知。</p>
<span class="qa-anchor" id="q-086-a-04"></span><p>一般 pending event 保存的是事件資訊，後續用 AER CQE 的 AET／AEI／LID 回覆。Immediate 必須在發生時已有 Request，否則不得回報。</p>
</section>
<section class="qa-section" id="q-086-s-02" data-answer-section="2"><h3><span>2.</span> 用操作與結果理解</h3>
<span class="qa-anchor" id="q-086-a-03"></span><p>檢查 OAES、FID0Bh、事件種類及 AER outstanding 紀錄。是否支援某個 Log，不足以證明所有相關事件都啟用。</p>
<span class="qa-anchor" id="q-086-a-05"></span><p>建立無 Request 的受控期間，再觸發已啟用的一般事件，之後送 AER。期間若成功讀 Log 清除事件，或發生 CLR，就不能再要求後續一定收到原通知。</p>
<span class="qa-anchor" id="q-086-a-06"></span><p>對一般已啟用事件，規範建議保留資訊供下一個 Request 回覆；這是 should，不是對所有種類的無條件永久保留要求。</p>
</section>
<section class="qa-section" id="q-086-s-03" data-answer-section="3"><h3><span>3.</span> 容易誤判的地方</h3>
<span class="qa-anchor" id="q-086-a-07"></span><p>沒有 Request 不會因此產生一筆超限或失敗 CQE。Immediate 未回報若符合上述條件，是規範要求，不能判為遺失事件的韌體缺陷。</p>
<span class="qa-anchor" id="q-086-a-16"></span><p>比對事件時間、Request 時間、Log 確認及 CLR。只有把這些時間排清楚，才知道通知是否仍應存在。</p>
</section>
</div>
<span class="qa-anchor" id="q-086-a-17"></span><span class="qa-anchor" id="q-086-a-08"></span><span class="qa-anchor" id="q-086-a-09"></span><span class="qa-anchor" id="q-086-a-10"></span><span class="qa-anchor" id="q-086-a-11"></span><span class="qa-anchor" id="q-086-a-12"></span><span class="qa-anchor" id="q-086-a-13"></span><span class="qa-anchor" id="q-086-a-14"></span><span class="qa-anchor" id="q-086-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-087" data-question="87" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-087">Q87</a> 多個相同或不同事件同時發生時，Controller 如何合併與回報？</h2>
<p class="qa-prompt">先用自己的話解釋機制，再舉一個常見誤解。</p>
<details class="qa-answer" id="q-087-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-087-a-01">通知機制避免每次狀態變動都占用一筆 Request，但仍要讓 Host 找到需要處理的資訊。事件次數、Log entries 與 AER completions 不一定一對一。</p><div class="qa-sections">
<section class="qa-section" id="q-087-s-01" data-answer-section="1"><h3><span>1.</span> 機制與適用範圍</h3>
<span class="qa-anchor" id="q-087-a-02"></span><p>相同 event type 且回覆內容相同的事件，可以合併；不同種類或不同回覆則有待回報的排隊建議。回報後的自動遮蔽也會影響後續通知。</p>
<span class="qa-anchor" id="q-087-a-04"></span><p>以 AET、AEI、LID 及事件特定參數比較回覆，不要只比 AEI。相同 AEI 在不同類型中可能不是同一事件。</p>
</section>
<section class="qa-section" id="q-087-s-02" data-answer-section="2"><h3><span>2.</span> 用操作與結果理解</h3>
<span class="qa-anchor" id="q-087-a-03"></span><p>先確認每種事件受支援並啟用，並記錄可用 AER 數。只有一筆 Request 時，不能期待多個事件同時各回一筆 completion。</p>
<span class="qa-anchor" id="q-087-a-05"></span><p>先觸發已知事件集合，逐筆接收並保存回覆，依規則讀 Log 與補 Request。確認後再觀察新的事件，避免把仍被遮蔽的通知當成未偵測。</p>
<span class="qa-anchor" id="q-087-a-06"></span><p>相同回覆合併成一筆是 may；保留不同回覆的佇列是 should。規範沒有因此保證 AER 完成順序能還原所有內部事件的精確時間線。</p>
</section>
<section class="qa-section" id="q-087-s-03" data-answer-section="3"><h3><span>3.</span> 容易誤判的地方</h3>
<span class="qa-anchor" id="q-087-a-07"></span><p>合法合併不應被判為少回 completion 的錯誤。若 Host 同時送入過多 AER，則另依 1/05h 處理，與事件合併無關。</p>
<span class="qa-anchor" id="q-087-a-16"></span><p>用 Log 的紀錄或 generation 補充通知，而不是把 AER 數量直接當成故障發生次數。</p>
</section>
</div>
<span class="qa-anchor" id="q-087-a-17"></span><span class="qa-anchor" id="q-087-a-08"></span><span class="qa-anchor" id="q-087-a-09"></span><span class="qa-anchor" id="q-087-a-10"></span><span class="qa-anchor" id="q-087-a-11"></span><span class="qa-anchor" id="q-087-a-12"></span><span class="qa-anchor" id="q-087-a-13"></span><span class="qa-anchor" id="q-087-a-14"></span><span class="qa-anchor" id="q-087-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-088" data-question="88" data-answer-kind="process"><h2><a class="qa-qid" href="#q-088">Q88</a> Asynchronous Event Configuration 如何啟用或遮蔽特定事件？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-088-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-088-a-01">FID0Bh 選擇 Host 希望接收的適用通知。這是通知政策，不會消除裝置已發生的健康問題，也不會自動提交 AER。</p><div class="qa-sections">
<section class="qa-section" id="q-088-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-088-a-02"></span><p>設定以 controller 為操作對象，控制指定的 SMART 與選配事件通知。它不是所有 Error 類型事件的總開關。</p>
<span class="qa-anchor" id="q-088-a-03"></span><p>讀 OAES 與相關能力，確認想啟用的事件受支援，再查 FID0Bh Current。設定支援和當下事件是否仍被遮蔽，是不同狀態。</p>
<span class="qa-anchor" id="q-088-a-04"></span><p>Set Features.CDW11 的各 bit 選擇事件通知；Get Features 讀回 Current。這份 bitmap 不是 AER completion 的 AET／AEI 編碼。</p>
</section>
<section class="qa-section" id="q-088-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-088-a-05"></span><p>先設定合法的啟用值並等待成功，再讀回確認，確保有 AER 等待，最後建立事件條件。若條件在啟用前已成立，仍須依 Feature 的既有條件規則判斷。</p>
<span class="qa-anchor" id="q-088-a-06"></span><p>成功表示設定已完成；Host 是否收到通知，還取決於事件條件、遮蔽與 Request。停用通知不代表該警告位一定清零。</p>
</section>
<section class="qa-section" id="q-088-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-088-a-07"></span><p>啟用不支援的事件，必須回 Invalid Field（0/02h）。沒有 AER 而暫時收不到通知，不是 Set Features 的失敗 Status。</p>
<span class="qa-anchor" id="q-088-a-16"></span><p>一起比對能力、Current mask、實際警告及 AER。只確認 Set 成功，不足以判斷通知路徑全部正常。</p>
</section>
</div>
<span class="qa-anchor" id="q-088-a-17"></span><span class="qa-anchor" id="q-088-a-08"></span><span class="qa-anchor" id="q-088-a-09"></span><span class="qa-anchor" id="q-088-a-10"></span><span class="qa-anchor" id="q-088-a-11"></span><span class="qa-anchor" id="q-088-a-12"></span><span class="qa-anchor" id="q-088-a-13"></span><span class="qa-anchor" id="q-088-a-14"></span><span class="qa-anchor" id="q-088-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-089" data-question="89" data-answer-kind="events"><h2><a class="qa-qid" href="#q-089">Q89</a> SMART、Namespace、Firmware、Telemetry、Sanitize、Self-test 與 PEL 各有哪些通知條件？</h2>
<p class="qa-prompt">先說明事件成立的條件，再區分通知、事件確認與紀錄。</p>
<details class="qa-answer" id="q-089-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-089-a-01">這题要校正「每個功能完成都會有一種 AER」的假設。事件必須有規範定義，不能只因功能有 Log，就自行增加完成通知。</p><div class="qa-sections">
<section class="qa-section" id="q-089-s-01" data-answer-section="1"><h3><span>1.</span> 事件何時成立、由誰觀察</h3>
<span class="qa-anchor" id="q-089-a-02"></span><p>事件可能描述 controller 健康、namespace 變更、韌體啟用或 sanitization target。不同 scope 的事件要讀不同資料，不只看接收它的 controller。</p>
<span class="qa-anchor" id="q-089-a-03"></span><p>用 OAES、FID0Bh 與事件表確認選配通知。Device Self-test 支援位與 PEL 支援位，不會自動宣告一個通用的 Self-test Completed 或 PEL Changed AER。</p>
<span class="qa-anchor" id="q-089-a-04"></span><p>SMART 類型使用 02h；namespace 變更依 Attached／Allocated 分別關聯 04h／1Ch；Firmware Activation Starting 關聯 03h；Telemetry Changed 關聯 08h；Sanitize 類型關聯 81h。</p>
</section>
<section class="qa-section" id="q-089-s-02" data-answer-section="2"><h3><span>2.</span> 通知、讀取與確認的關係</h3>
<span class="qa-anchor" id="q-089-a-05"></span><p>先辨認事件條件，再找對應 Log。Self-test 正常完成應查 06h 的結果；若另符合 Diagnostic Failure 的錯誤條件，才依該 Error 事件處理，不能將兩者等同。</p>
<span class="qa-anchor" id="q-089-a-06"></span><p>Sanitize 有完成、非預期 deallocation 與進入 Media Verification 等不同事件，不可全部翻成清除成功。Firmware Activation Starting 也只表示開始，不是最終啟用成功。</p>
</section>
<section class="qa-section" id="q-089-s-03" data-answer-section="3"><h3><span>3.</span> 沒有通知或紀錄時怎麼判斷</h3>
<span class="qa-anchor" id="q-089-a-07"></span><p>某個操作沒有規定完成 AER 時，沒收到通知不是 Status 錯誤。判定漏報前，必須指出具體事件定義、支援、啟用及 Request 條件。</p>
<span class="qa-anchor" id="q-089-a-16"></span><p>將實際操作結果、專用 Log 與 AER 條件分開核對，再以 PEL 的獨立支援事件補充歷史，不要求三者一對一。</p>
<span class="qa-anchor" id="q-089-a-17"></span><p>先檢查期待的事件是否真的在本版規格中有定義，而不是由功能名稱推測。</p>
</section>
<section class="qa-section" id="q-089-s-04" data-answer-section="4"><h3><span>4.</span> Asynchronous Event 的通知條件</h3>
<span class="qa-anchor" id="q-089-a-09"></span><p>AER 的正常用途就是讓 controller 以完成這筆 Request 的方式回報事件。 <a class="qa-rule-link" href="#common-aer_request-9">完整條件見本冊說明</a></p>
</section>
</div>
<span class="qa-anchor" id="q-089-a-08"></span><span class="qa-anchor" id="q-089-a-10"></span><span class="qa-anchor" id="q-089-a-11"></span><span class="qa-anchor" id="q-089-a-12"></span><span class="qa-anchor" id="q-089-a-13"></span><span class="qa-anchor" id="q-089-a-14"></span><span class="qa-anchor" id="q-089-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-090" data-question="90" data-answer-kind="process"><h2><a class="qa-qid" href="#q-090">Q90</a> Host 讀取 Log 後，事件如何清除或保留？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-090-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-090-a-01">事件確認控制後續通知是否重新開放，不是刪除全部歷史或修復根本原因。清除通知後，原警告可能仍存在。</p><div class="qa-sections">
<section class="qa-section" id="q-090-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-090-a-02"></span><p>以該事件指定的 Log 與目標為準；讀取另一張 Log，或另一個 namespace 的資料，不一定確認目前這個事件。</p>
<span class="qa-anchor" id="q-090-a-03"></span><p>先看事件是否採一般讀 Log 確認，還是 Immediate／One-Shot 的特殊方式。只有適用的事件才用 RAE 判讀。</p>
<span class="qa-anchor" id="q-090-a-04"></span><p>RAE=0 表示成功完成後清除對應事件；RAE=1 表示保留。LID、NSID 與其他選擇欄位仍要符合事件對應的 Log 規則。</p>
</section>
<section class="qa-section" id="q-090-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-090-a-05"></span><p>保存通知與原狀態，按需以 RAE=1 讀取，再以適用的 RAE=0 成功讀取確認。不要把任意片段讀取都當成每種 Log 通用的確認方法。</p>
<span class="qa-anchor" id="q-090-a-06"></span><p>成功確認後，事件遮蔽依其規則解除；若狀態持續，後續通知仍可能再次出現。RAE 保留的是事件，不是保證回傳資料從此凍結。</p>
</section>
<section class="qa-section" id="q-090-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-090-a-07"></span><p>Get 失敗時，事件必須保留。不能因 Host 寫了 RAE=0，就在 CQE 顯示失敗時仍要求事件消失。</p>
<span class="qa-anchor" id="q-090-a-16"></span><p>比對成功 CQE 的時間、RAE、事件 mask 與後續通知。讀取時與事件發生時的即時值可能不同，不代表確認動作錯誤。</p>
</section>
</div>
<span class="qa-anchor" id="q-090-a-17"></span><span class="qa-anchor" id="q-090-a-08"></span><span class="qa-anchor" id="q-090-a-09"></span><span class="qa-anchor" id="q-090-a-10"></span><span class="qa-anchor" id="q-090-a-11"></span><span class="qa-anchor" id="q-090-a-12"></span><span class="qa-anchor" id="q-090-a-13"></span><span class="qa-anchor" id="q-090-a-14"></span><span class="qa-anchor" id="q-090-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-091" data-question="91" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-091">Q91</a> AER 能否被 Abort？Reset 時尚未完成的 Request 如何處理？</h2>
<p class="qa-prompt">先指明重設或中斷的方式，再分別判斷設定、進行中的操作與資料。</p>
<details class="qa-answer" id="q-091-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-091-a-01">AER 雖然沒有一般 timeout，仍是有 CID 的 Admin 命令。Host 停止使用事件通道時，要分清楚針對單筆 Request 的 Abort，與重設整個 controller 的處理。</p><div class="qa-sections">
<section class="qa-section" id="q-091-s-01" data-answer-section="1"><h3><span>1.</span> 先界定觸發方式與影響對象</h3>
<span class="qa-anchor" id="q-091-a-02"></span><p>Abort 以 SQID=0 與目標 AER 的 CID 指定它；Controller Reset 則影響此 controller 的全部 outstanding AER。</p>
<span class="qa-anchor" id="q-091-a-03"></span><p>Abort 的並行上限由 ACL+1 決定，與 AERL+1 不同。沒有特殊的 AER Abort 成功保證，仍要依 Abort 結果判斷。</p>
</section>
<section class="qa-section" id="q-091-s-02" data-answer-section="2"><h3><span>2.</span> 哪些狀態改變，恢復後怎麼處理</h3>
<span class="qa-anchor" id="q-091-a-04"></span><p>保留 Abort 自己的 CID、目標 CID，以及 CQE.DW0 的 IANP。IANP=0 表示已執行 immediate abort；IANP=1 不代表目標從此不會被 deferred abort。</p>
<span class="qa-anchor" id="q-091-a-05"></span><p>送出 Abort 後，分別處理 Abort 與目標 Request 的結果。如果改採 Reset，則依重設規則終止舊追蹤，恢復後建立新的 AER，不能等待重設中止的舊 Request 回 CQE。</p>
<span class="qa-anchor" id="q-091-a-06"></span><p>Abort 可能和事件完成競爭：目標可能先正常回報事件。真正被 Abort 的目標回 Command Abort Requested；被 Controller Reset 中止的 AER 則不得回 CQE，兩種情況不同。</p>
</section>
<section class="qa-section" id="q-091-s-03" data-answer-section="3"><h3><span>3.</span> 重設或斷電時，要確認什麼</h3>
<span class="qa-anchor" id="q-091-a-12"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">觸發方式</th><th scope="col">這項操作或狀態會如何變化</th></tr></thead><tbody><tr><td>Controller Reset 後是否保留或繼續？</td><td>Controller Reset 會中止尚未完成的 AER，而且這些被重設中止的 Request 不得回傳 CQE。Controller Level Reset 也會清除尚未通知的 pending event；Host 恢復後重新提交 AER，並依各 Log 的保留規則查詢狀態。</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-091-s-04" data-answer-section="4"><h3><span>4.</span> 如何驗證保留或恢復結果</h3>
<span class="qa-anchor" id="q-091-a-07"></span><p>Abort 超限可回 Abort Command Limit Exceeded（1/03h）。目標已完成或未找到時，不能一律要求 Abort 本身失敗；應讀 IANP，並確認是否已有目標 completion。</p>
<span class="qa-anchor" id="q-091-a-16"></span><p>核對同一 Admin Queue 使用期間內的 CID，避免 Reset 後重用 CID 時，把新 Request 當成舊 Abort 的目標。</p>
<span class="qa-anchor" id="q-091-a-17"></span><p>先辨認 Request 是由 Abort 結束、事件完成，還是被 Reset 中止，再決定應不應有 CQE。</p>
</section>
</div>
<span class="qa-anchor" id="q-091-a-08"></span><span class="qa-anchor" id="q-091-a-09"></span><span class="qa-anchor" id="q-091-a-10"></span><span class="qa-anchor" id="q-091-a-11"></span><span class="qa-anchor" id="q-091-a-13"></span><span class="qa-anchor" id="q-091-a-14"></span><span class="qa-anchor" id="q-091-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-092" data-question="92" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-092">Q92</a> AER 已完成，但對應 Log 看不到預期資訊時，應如何定位？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-092-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-092-a-01">通知描述曾發生的條件，Log 則可能描述目前狀態或有限歷史，因此兩者不一定是同一時點的副本。先找出資料類型，才能判斷是真的不一致。</p><div class="qa-sections">
<section class="qa-section" id="q-092-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-092-a-02"></span><p>固定 controller、事件 target 與讀取介面。共用資源的狀態可能已由另一個 Host 讀取或確認，不能只看本地程式紀錄。</p>
<span class="qa-anchor" id="q-092-a-03"></span><p>核對 AET／AEI 的規範定義與 LID，再查支援能力及 Log 的更新、清除與保留規則。不要先假設每個事件都新增一筆 entry。</p>
<span class="qa-anchor" id="q-092-a-04"></span><p>保留原 CQE、RAE、LID、NSID、LSI、讀取時間與有效欄位。SMART Critical Warning 反映處理 Get 時的狀態，可能已不同於事件發生時。</p>
</section>
<section class="qa-section" id="q-092-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-092-a-17"></span><p>先檢查 Log 是即時狀態還是事件歷史，這決定它是否必須保留事件當時的數值。</p>
<span class="qa-anchor" id="q-092-a-05"></span><p>先排除讀錯 Log 或對象，再檢查其他讀取、重設、generation 變化及 transient condition 已恢復。最後才比對規範是否要求仍能查到特定資訊。</p>
</section>
<section class="qa-section" id="q-092-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-092-a-06"></span><p>例如溫度曾達門檻而觸發事件，稍後讀 SMART 時溫度已降低，兩者可以同時正確。相反地，More=1 的命令錯誤應有可關聯的補充資訊，須用相應規則檢查。</p>
<span class="qa-anchor" id="q-092-a-07"></span><p>沒有預期資料不會自動改變已成功的 AER Status。若後續 Get 失敗，保留那筆命令的獨立錯誤，不能把兩筆結果混成一個。</p>
<span class="qa-anchor" id="q-092-a-16"></span><p>完整結論要指出事件條件、Log 的資料時點及所有中間動作。只有在保留前提都成立時仍缺少必要資訊，才形成可驗證的矛盾。</p>
</section>
</div>
<span class="qa-anchor" id="q-092-a-08"></span><span class="qa-anchor" id="q-092-a-09"></span><span class="qa-anchor" id="q-092-a-10"></span><span class="qa-anchor" id="q-092-a-11"></span><span class="qa-anchor" id="q-092-a-12"></span><span class="qa-anchor" id="q-092-a-13"></span><span class="qa-anchor" id="q-092-a-14"></span><span class="qa-anchor" id="q-092-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-aer_request-9"><h3>本主題的共用條件 · 是否產生 Asynchronous Event？</h3><p>AER 的正常用途就是讓 controller 以完成這筆 Request 的方式回報事件。必須分清楚事件本身、通知是否啟用、是否被遮蔽，以及是否還有 Request 可用；送出 AER 不會替 Host 啟用所有選配事件。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>文件頁 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-abort"><strong>Base 2.4 · §5.2.1</strong><br>文件頁 181–182 · PDF 207–208 · Figure 147–149</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>文件頁 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-getlog"><strong>Base 2.4 · §5.2.13–5.2.13.1.1</strong><br>文件頁 212–218 · PDF 238–244 · Figure 203–211</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-smart"><strong>Base 2.4 · §5.2.13.1.3</strong><br>文件頁 220–225 · PDF 246–251 · Figure 213–214</li>
<li id="ref-dstlog"><strong>Base 2.4 · §5.2.13.1.7</strong><br>文件頁 229–232 · PDF 255–258 · Figure 218–219</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>文件頁 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-aec"><strong>Base 2.4 · §5.2.30.1.6</strong><br>文件頁 466–468 · PDF 492–494 · Figure 474</li>
</ul><h3>需要看欄位圖時</h3><p>以下連結可開啟對應的圖表教學，查閱欄位及判讀方式。每張圖保留固定的教學位置，方便之後反覆查詢。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/asynchronous-events/en/">English</a><a href="/DOCS/nvme-question-bank/asynchronous-events.html">繁中教學 HTML</a></nav>
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
