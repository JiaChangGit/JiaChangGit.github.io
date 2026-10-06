---
layout: post
title: "NVMe 自問自答題庫：Keep Alive"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/keep-alive/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/keep-alive/en/">English</a><a href="/DOCS/nvme-question-bank/keep-alive.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q217–Q222</p><h1>Keep Alive</h1><p class="qr-intro">Keep Alive 用來偵測 Host 是否仍維持連線活動，在 PCIe 上屬選配。本冊分開命令模式與流量模式，說明何時開始計時及到期後的結果。</p><p>先練習，再展開解答。各題依需要使用文字、欄位判讀、比較或流程說明，不要求相同的回答項目。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>兩種模式，兩種重新計時依據</h2><p class="qa-takeaway">一筆命令長期 outstanding，不等於每個流量區間都有新活動。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">條件</th><th scope="col">查詢或動作</th><th scope="col">判讀</th></tr></thead><tbody><tr><td>支援與粒度</td><td>KAS、TBKAS</td><td>KAS 單位 100 ms；模式另確認</td></tr><tr><td>逾時設定</td><td>FID0Fh.KATO</td><td>要求值可能向上調整</td></tr><tr><td>命令模式</td><td>成功 Keep Alive／KATO Set</td><td>依成功操作重新計時</td></tr><tr><td>流量模式</td><td>區間內取得命令</td><td>不能只看仍有 outstanding</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>KAS=2 表示 200ms 粒度；KATO 要求 250ms 時需向上配合粒度。Host 應讀回實際值，用它安排後續活動，而不是堅持回值必須等於 250。</p>
<p class="qa-citations">來源：<a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-feature">Base 2.4 §4.4</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-217">Q217 · PCIe Host 如何確認 Keep Alive 支援？</a></li>
<li><a href="#q-218">Q218 · Keep Alive Timer 如何設定、調整與停用？</a></li>
<li><a href="#q-219">Q219 · Host 如何在 Timer 到期前維持 Keep Alive？</a></li>
<li><a href="#q-220">Q220 · Keep Alive Timeout 後，Controller 必須做哪些清理？</a></li>
<li><a href="#q-221">Q221 · Controller Reset 後，是否要重新設定 Keep Alive？</a></li>
<li><a href="#q-222">Q222 · Command Based 與 Traffic Based Keep Alive 有何不同？</a></li>
</ol></section>
<article class="qa-question" id="q-217" data-question="217" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-217">Q217</a> PCIe Host 如何確認 Keep Alive 支援？</h2>
<p class="qa-prompt">先選查詢介面與目標，再說明哪個回傳欄位能支持你的結論。</p>
<details class="qa-answer" id="q-217-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-217-a-01">Keep Alive 是通訊存活監測，不是每筆 I/O 的執行期限。PCIe 不要求所有 SSD 都啟用它。</p><div class="qa-sections">
<section class="qa-section" id="q-217-s-01" data-answer-section="1"><h3><span>1.</span> 要查哪個對象、哪份資料</h3>
<span class="qa-anchor" id="q-217-a-02"></span><p>每個 controller 各自有 Timer，不能以另一個 controller 的活動替代。</p>
<span class="qa-anchor" id="q-217-a-03"></span><p>Identify.KAS 非零表示支援，並給出以 100 ms 為單位的設定粒度；CTRATT.TBKAS 表示 Traffic Based 模式。</p>
<span class="qa-anchor" id="q-217-a-04"></span><p>支援 Timer 就必須支援 Keep Alive 命令；設定透過 FID0Fh.KATO，單位為毫秒。</p>
</section>
<section class="qa-section" id="q-217-s-02" data-answer-section="2"><h3><span>2.</span> 查詢順序與回覆判讀</h3>
<span class="qa-anchor" id="q-217-a-05"></span><p>先讀 KAS，再判斷模式及需要的 KATO，最後 Get 確認實際採用值。</p>
<span class="qa-anchor" id="q-217-a-06"></span><p>PCIe 的預設 KATO=0，即停用；支援能力非零與目前有啟用，是不同資訊。</p>
</section>
<section class="qa-section" id="q-217-s-03" data-answer-section="3"><h3><span>3.</span> 證據不足或不一致時怎麼判斷</h3>
<span class="qa-anchor" id="q-217-a-07"></span><p>KAS=0 時不能要求它接受 Keep Alive 或 Timer 設定；依實際不支援的 Opcode／Feature 回應判讀。</p>
<span class="qa-anchor" id="q-217-a-16"></span><p>KAS、TBKAS、Commands Supported and Effects 與實際 FID 行為需一致。</p>
<span class="qa-anchor" id="q-217-a-17"></span><p>先檢查是否誤把 PCIe 的選配能力當成所有裝置的必要功能。</p>
</section>
</div>
<span class="qa-anchor" id="q-217-a-08"></span><span class="qa-anchor" id="q-217-a-09"></span><span class="qa-anchor" id="q-217-a-10"></span><span class="qa-anchor" id="q-217-a-11"></span><span class="qa-anchor" id="q-217-a-12"></span><span class="qa-anchor" id="q-217-a-13"></span><span class="qa-anchor" id="q-217-a-14"></span><span class="qa-anchor" id="q-217-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-218" data-question="218" data-answer-kind="process"><h2><a class="qa-qid" href="#q-218">Q218</a> Keep Alive Timer 如何設定、調整與停用？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-218-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-218-a-01">Host 設定可容忍的通訊空窗；controller 依支援粒度採用可實作的值。</p><div class="qa-sections">
<section class="qa-section" id="q-218-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-218-a-02"></span><p>設定作用於此 controller，不是整個 subsystem 的共同 I/O timeout。</p>
<span class="qa-anchor" id="q-218-a-03"></span><p>先讀 KAS 與目前 FID0Fh.KATO，並確認 Feature 的保存能力。</p>
<span class="qa-anchor" id="q-218-a-04"></span><p>Set Features CDW11.KATO 指定毫秒；controller 必須向上取到 KAS 的粒度。非零值低於實作最小值時，採最小值。</p>
</section>
<section class="qa-section" id="q-218-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-218-a-05"></span><p>Set 成功後 Get 讀實際值，再更新 Host 的發送排程；PCIe 可設 KATO=0 停用。</p>
<span class="qa-anchor" id="q-218-a-06"></span><p>例如 KAS=10 表示 1000 ms 粒度，要求 1500 ms 會向上成 2000 ms，前提是沒有更大的最小值。</p>
</section>
<section class="qa-section" id="q-218-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-218-a-07"></span><p>若要求超過適用傳輸允許的最大值，回 Keep Alive Timeout Invalid 且保留原設定；不能自行替 PCIe 編造固定最大限制。</p>
<span class="qa-anchor" id="q-218-a-16"></span><p>Get 的回值可合法大於要求值；只有確認粒度與最小值後，才能判定調整是否不合理。</p>
</section>
</div>
<span class="qa-anchor" id="q-218-a-17"></span><span class="qa-anchor" id="q-218-a-08"></span><span class="qa-anchor" id="q-218-a-09"></span><span class="qa-anchor" id="q-218-a-10"></span><span class="qa-anchor" id="q-218-a-11"></span><span class="qa-anchor" id="q-218-a-12"></span><span class="qa-anchor" id="q-218-a-13"></span><span class="qa-anchor" id="q-218-a-14"></span><span class="qa-anchor" id="q-218-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-219" data-question="219" data-answer-kind="process"><h2><a class="qa-qid" href="#q-219">Q219</a> Host 如何在 Timer 到期前維持 Keep Alive？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-219-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-219-a-01">預留時間餘裕，才能容納排程、命令處理與傳輸延遲；在最後一刻送出不代表 controller 已及時處理。</p><div class="qa-sections">
<section class="qa-section" id="q-219-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-219-a-02"></span><p>只有 EN=1、RDY=1、SHN=00b、SHST=00b 且 KATO 非零時 Timer 才 active。</p>
<span class="qa-anchor" id="q-219-a-03"></span><p>讀實際 KATO，並確認 Command Based 或 Traffic Based 模式。</p>
<span class="qa-anchor" id="q-219-a-04"></span><p>Command Based 的 controller 在 Keep Alive 成功完成，或成功設定非零 KATO 時重新計時；普通 Read 不會替代它。</p>
</section>
<section class="qa-section" id="q-219-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-219-a-05"></span><p>Host 建議每 KATT/2 送 Keep Alive，並在 Admin SQ 保留可提交空間；調整 KATO 成功後也更新排程。</p>
<span class="qa-anchor" id="q-219-a-06"></span><p>持續收到成功 Completion 能證明這條通訊路徑仍能往返；不是證明每筆媒體操作都已完成。</p>
</section>
<section class="qa-section" id="q-219-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-219-a-07"></span><p>Keep Alive 自己長時間沒有 Completion 時，Host 依其送出後 KATT 的判斷與恢復規則處理，不能無限補送來掩蓋失聯。</p>
<span class="qa-anchor" id="q-219-a-16"></span><p>把 Host 送出、controller 完成與 Host 收到的時間分開，才能解釋兩端觀察差異。</p>
</section>
</div>
<span class="qa-anchor" id="q-219-a-17"></span><span class="qa-anchor" id="q-219-a-08"></span><span class="qa-anchor" id="q-219-a-09"></span><span class="qa-anchor" id="q-219-a-10"></span><span class="qa-anchor" id="q-219-a-11"></span><span class="qa-anchor" id="q-219-a-12"></span><span class="qa-anchor" id="q-219-a-13"></span><span class="qa-anchor" id="q-219-a-14"></span><span class="qa-anchor" id="q-219-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-220" data-question="220" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-220">Q220</a> Keep Alive Timeout 後，Controller 必須做哪些清理？</h2>
<p class="qa-prompt">先指明重設或中斷的方式，再分別判斷設定、進行中的操作與資料。</p>
<details class="qa-answer" id="q-220-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-220-a-01">Timeout 清理讓失去可靠通訊的 controller 停止繼續處理命令，降低 Host 轉移工作後仍有舊操作進行的風險。</p><div class="qa-sections">
<section class="qa-section" id="q-220-s-01" data-answer-section="1"><h3><span>1.</span> 先界定觸發方式與影響對象</h3>
<span class="qa-anchor" id="q-220-a-02"></span><p>本題只列 PCIe 適用動作；它不刪 namespace、不執行 Sanitize，也不承諾回復已寫入資料。</p>
<span class="qa-anchor" id="q-220-a-03"></span><p>查 Identify.CQT、CSTS.CFS 與 Error Information，並保留 outstanding 清單。</p>
</section>
<section class="qa-section" id="q-220-s-02" data-answer-section="2"><h3><span>2.</span> 哪些狀態改變，恢復後怎麼處理</h3>
<span class="qa-anchor" id="q-220-a-04"></span><p>規範要求在 CQT 內記錄 Keep Alive Timeout Expired、停止命令處理，並設 CSTS.CFS=1。</p>
<span class="qa-anchor" id="q-220-a-05"></span><p>Host 停止提交到該路徑，保存可取得的狀態，再依通訊恢復與 Reset 流程重建。</p>
<span class="qa-anchor" id="q-220-a-06"></span><p>完成清理表示停止處理；不代表每筆 outstanding 都會取得成功或錯誤 CQE。</p>
</section>
<section class="qa-section" id="q-220-s-03" data-answer-section="3"><h3><span>3.</span> 如何驗證保留或恢復結果</h3>
<span class="qa-anchor" id="q-220-a-07"></span><p>不能以 Keep Alive Timeout 直接指定舊 Write「沒有執行」，也不能假設所有舊命令可以安全原樣重送。</p>
<span class="qa-anchor" id="q-220-a-16"></span><p>CFS、Error entry 與清理時間應一致，資料操作則另查實際效果與重試相依性。</p>
<span class="qa-anchor" id="q-220-a-17"></span><p>先確認逾時是 Host 自己判斷，還是 controller 已偵測並完成清理。</p>
</section>
</div>
<span class="qa-anchor" id="q-220-a-08"></span><span class="qa-anchor" id="q-220-a-09"></span><span class="qa-anchor" id="q-220-a-10"></span><span class="qa-anchor" id="q-220-a-11"></span><span class="qa-anchor" id="q-220-a-12"></span><span class="qa-anchor" id="q-220-a-13"></span><span class="qa-anchor" id="q-220-a-14"></span><span class="qa-anchor" id="q-220-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-221" data-question="221" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-221">Q221</a> Controller Reset 後，是否要重新設定 Keep Alive？</h2>
<p class="qa-prompt">先指明重設或中斷的方式，再分別判斷設定、進行中的操作與資料。</p>
<details class="qa-answer" id="q-221-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-221-a-01">Reset 結束舊命令環境，但 Timer 的恢復還取決於 Feature 保存與持續性，不能只因記得舊 KATO 就直接沿用排程。</p><div class="qa-sections">
<section class="qa-section" id="q-221-s-01" data-answer-section="1"><h3><span>1.</span> 先界定觸發方式與影響對象</h3>
<span class="qa-anchor" id="q-221-a-02"></span><p>針對被重設的 controller，重新確認設定與 Timer active 條件。</p>
<span class="qa-anchor" id="q-221-a-03"></span><p>查恢復後 Current KATO、支援能力及適用的 Saved／Default 規則。</p>
</section>
<section class="qa-section" id="q-221-s-02" data-answer-section="2"><h3><span>2.</span> 哪些狀態改變，恢復後怎麼處理</h3>
<span class="qa-anchor" id="q-221-a-04"></span><p>Timer 在 EN／RDY／SHN／SHST 任一條件不符時 inactive；再次由 inactive 轉 active 時初始化為有效 KATO。</p>
<span class="qa-anchor" id="q-221-a-05"></span><p>完成初始化，Get 確認 KATO；若為 0 而 Host 需要啟用，再 Set 非零值並讀回，然後重啟 Host 維護排程。</p>
<span class="qa-anchor" id="q-221-a-06"></span><p>Host 排程與 controller 的實際值、模式及新使用期間一致。</p>
</section>
<section class="qa-section" id="q-221-s-03" data-answer-section="3"><h3><span>3.</span> 如何驗證保留或恢復結果</h3>
<span class="qa-anchor" id="q-221-a-07"></span><p>Reset 前尚未完成的 Keep Alive 不能拿舊 CQE bytes 當成 Reset 後成功的存活證據。</p>
<span class="qa-anchor" id="q-221-a-16"></span><p>重設前後比較的是設定恢復規則，不是要求倒數值接續到最後一毫秒。</p>
<span class="qa-anchor" id="q-221-a-17"></span><p>先讀 Current KATO，再決定是否需要重設值，避免把「必須重查」誤寫成所有裝置都「必須重設同一值」。</p>
</section>
</div>
<span class="qa-anchor" id="q-221-a-08"></span><span class="qa-anchor" id="q-221-a-09"></span><span class="qa-anchor" id="q-221-a-10"></span><span class="qa-anchor" id="q-221-a-11"></span><span class="qa-anchor" id="q-221-a-12"></span><span class="qa-anchor" id="q-221-a-13"></span><span class="qa-anchor" id="q-221-a-14"></span><span class="qa-anchor" id="q-221-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-222" data-question="222" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-222">Q222</a> Command Based 與 Traffic Based Keep Alive 有何不同？</h2>
<p class="qa-prompt">先說出比較對象最重要的差別，並舉一個不能互相代用的例子。</p>
<details class="qa-answer" id="q-222-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-222-a-01">兩種方式判斷存活的證據不同：前者靠專用命令，後者可利用一般命令流量。</p><div class="qa-sections">
<section class="qa-section" id="q-222-s-01" data-answer-section="1"><h3><span>1.</span> 差別在哪裡</h3>
<span class="qa-anchor" id="q-222-a-02"></span><p>模式由支援 Keep Alive 的 controller.TBKAS 決定，不是 Host 任意忽略專用命令就算啟用 Traffic Based。</p>
<span class="qa-anchor" id="q-222-a-04"></span><p>Traffic Based 的 controller 看每個 KATT 區間是否曾 fetched Admin 或 I/O command；Host 則用已提交且已處理 Completion 的活動作為省略 Keep Alive 的證據。</p>
</section>
<section class="qa-section" id="q-222-s-02" data-answer-section="2"><h3><span>2.</span> 如何選擇與確認</h3>
<span class="qa-anchor" id="q-222-a-03"></span><p>確認 KAS 非零與 CTRATT.TBKAS；TBKAS=0 使用 Command Based。</p>
<span class="qa-anchor" id="q-222-a-05"></span><p>Host 在 Traffic Based 模式建議每 KATT/4 檢查是否需送專用命令；沒有足夠活動時仍送 Keep Alive。</p>
<span class="qa-anchor" id="q-222-a-06"></span><p>一個區間有取得命令，controller 可開始下一區間，因此最後一次 fetched 後到偵測 Timeout 可能接近 2×KATT。</p>
</section>
<section class="qa-section" id="q-222-s-03" data-answer-section="3"><h3><span>3.</span> 哪些結論不能互相套用</h3>
<span class="qa-anchor" id="q-222-a-07"></span><p>不能要求 Traffic Based 在最後一筆命令後剛好 KATT 就一定 Timeout，也不能只因一筆長命令仍 outstanding 就認為每個後續區間都有新流量。</p>
<span class="qa-anchor" id="q-222-a-16"></span><p>依 fetched、completed 與區間邊界核對，不把「Host 已寫 SQE」當成 controller 已取得。</p>
</section>
</div>
<span class="qa-anchor" id="q-222-a-17"></span><span class="qa-anchor" id="q-222-a-08"></span><span class="qa-anchor" id="q-222-a-09"></span><span class="qa-anchor" id="q-222-a-10"></span><span class="qa-anchor" id="q-222-a-11"></span><span class="qa-anchor" id="q-222-a-12"></span><span class="qa-anchor" id="q-222-a-13"></span><span class="qa-anchor" id="q-222-a-14"></span><span class="qa-anchor" id="q-222-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>

<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-keepalive"><strong>Base 2.4 · §3.9 (common and PCIe rules), 5.2.30.1.9</strong><br>文件頁 129–135, 471 · PDF 155–161, 497 · Figure 481</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>文件頁 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>文件頁 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>文件頁 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-commrecovery"><strong>Base 2.4 · §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</strong><br>文件頁 825–828 · PDF 851–854</li>
</ul><h3>需要看欄位圖時</h3><p>以下連結可開啟對應的圖表教學，查閱欄位及判讀方式。每張圖保留固定的教學位置，方便之後反覆查詢。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/keep-alive/en/">English</a><a href="/DOCS/nvme-question-bank/keep-alive.html">繁中教學 HTML</a></nav>
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
