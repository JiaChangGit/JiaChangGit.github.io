---
layout: post
title: "NVMe 自問自答題庫：Namespace Management、Attachment 與保護"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/namespace-management/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/namespace-management/en/">English</a><a href="/DOCS/nvme-question-bank/namespace-management.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q157–Q173</p><h1>Namespace Management、Attachment 與保護</h1><p class="qr-intro">建立 namespace、讓 controller 能存取它，以及限制寫入，是三組獨立狀態。本冊用同一物件從建立到刪除的流程，把三者接起來。</p><p>先練習，再展開解答。各題依需要使用文字、欄位判讀、比較或流程說明，不要求相同的回答項目。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>存在、可見、可寫分別確認</h2><p class="qa-takeaway">Create 成功不會自動完成 Attachment。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">問題</th><th scope="col">主要證據</th><th scope="col">下一步</th></tr></thead><tbody><tr><td>是否存在</td><td>Allocated List、Create CQE.NSID</td><td>確認格式與容量</td></tr><tr><td>此路徑能否存取</td><td>Active List、Controller List</td><td>確認 Ready 與路徑狀態</td></tr><tr><td>是否能改資料</td><td>NWPC、WPC、FID84h.WPS</td><td>依狀態檢查命令限制</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>Allocated={1,2}、ControllerA.Active={1} 只表示 2 尚未在 A 的 active 清單。它可能仍存在，甚至已附加 B；不能直接判定 namespace2 被刪除。</p>
<p class="qa-citations">來源：<a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-157">Q157 · 如何確認 Namespace Management 與 Attachment 支援？</a></li>
<li><a href="#q-158">Q158 · 建立 Namespace 時 NSZE、NCAP、Format 與 Thin Provisioning 如何設定？</a></li>
<li><a href="#q-159">Q159 · Create Namespace 容量不足或參數不合法如何回應？</a></li>
<li><a href="#q-160">Q160 · Create 後 Allocated Namespace List 如何更新？</a></li>
<li><a href="#q-161">Q161 · Attach／Detach 如何指定 Controller？</a></li>
<li><a href="#q-162">Q162 · Attach／Detach 後 Active List 與 Controller List 如何互相驗證？</a></li>
<li><a href="#q-163">Q163 · 重複 Attach、非法 Controller 或未 Attach 就 Detach 如何回應？</a></li>
<li><a href="#q-164">Q164 · Detach 時還有 Outstanding Command，應如何處理？</a></li>
<li><a href="#q-165">Q165 · Detach 後再送 Namespace Command 應得到什麼？</a></li>
<li><a href="#q-166">Q166 · 刪除不存在或仍 Attached 的 Namespace 如何處理？</a></li>
<li><a href="#q-167">Q167 · Namespace 變更後哪些事件與 Log 應更新？</a></li>
<li><a href="#q-168">Q168 · Changed Namespace List 超過容量如何表示？</a></li>
<li><a href="#q-169">Q169 · Reset 或 Power Cycle 後 Namespace 配置與 Attachment 是否保留？</a></li>
<li><a href="#q-170">Q170 · Private 與 Shared Namespace 有何差別？</a></li>
<li><a href="#q-171">Q171 · 三種 Write Protection 模式與進入條件有何不同？</a></li>
<li><a href="#q-172">Q172 · Write Protection 在 Reset 與 Power Cycle 後如何保留？</a></li>
<li><a href="#q-173">Q173 · Write Protection 如何影響 Format、Sanitize 與 Namespace Management？</a></li>
</ol></section>
<article class="qa-question" id="q-157" data-question="157" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-157">Q157</a> 如何確認 Namespace Management 與 Attachment 支援？</h2>
<p class="qa-prompt">先選查詢介面與目標，再說明哪個回傳欄位能支持你的結論。</p>
<details class="qa-answer" id="q-157-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-157-a-01">Management 建立／刪除 namespace，Attachment 決定哪些 controller 能使用它。這兩項能力相關，但不完全等價。</p><div class="qa-sections">
<section class="qa-section" id="q-157-s-01" data-answer-section="1"><h3><span>1.</span> 要查哪個對象、哪份資料</h3>
<span class="qa-anchor" id="q-157-a-02"></span><p>配置存在於 subsystem；active 存取則以各 controller 為準。</p>
<span class="qa-anchor" id="q-157-a-03"></span><p>Identify.OACS.NMS=1 表示支援 Management，也必須支援 Attachment；NMS=0 的 controller 仍可能單獨支援 Attachment，應查 Command Effects。</p>
<span class="qa-anchor" id="q-157-a-04"></span><p>Namespace Management Opcode0Dh，Attachment15h；前者 SEL 選建立／刪除／恢復，後者選 Attach／Detach。</p>
</section>
<section class="qa-section" id="q-157-s-02" data-answer-section="2"><h3><span>2.</span> 查詢順序與回覆判讀</h3>
<span class="qa-anchor" id="q-157-a-05"></span><p>先確認命令支援，再探索 namespace 與 controller 清單，最後建立需要的管理操作。</p>
<span class="qa-anchor" id="q-157-a-06"></span><p>宣告 NMS 後，兩種命令及相關變更通知能力應符合要求；單獨 Attachment 支援不代表可建立新 namespace。</p>
</section>
<section class="qa-section" id="q-157-s-03" data-answer-section="3"><h3><span>3.</span> 證據不足或不一致時怎麼判斷</h3>
<span class="qa-anchor" id="q-157-a-07"></span><p>不支援命令用相應 Opcode 錯誤；支援命令但不支援 Restore Default 操作用 Invalid Field，不能把整個 Management 判成不支援。</p>
<span class="qa-anchor" id="q-157-a-16"></span><p>交叉比對 OACS、Effects.CSUPP 及合法操作，不只看一個位元。</p>
<span class="qa-anchor" id="q-157-a-17"></span><p>先確認是否誤把 NMS=0 解成 Attachment 一定不支援。</p>
</section>
</div>
<span class="qa-anchor" id="q-157-a-08"></span><span class="qa-anchor" id="q-157-a-09"></span><span class="qa-anchor" id="q-157-a-10"></span><span class="qa-anchor" id="q-157-a-11"></span><span class="qa-anchor" id="q-157-a-12"></span><span class="qa-anchor" id="q-157-a-13"></span><span class="qa-anchor" id="q-157-a-14"></span><span class="qa-anchor" id="q-157-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-158" data-question="158" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-158">Q158</a> 建立 Namespace 時 NSZE、NCAP、Format 與 Thin Provisioning 如何設定？</h2>
<p class="qa-prompt">先試著說明欄位的單位與編碼，再用一組數值推導結果。</p>
<details class="qa-answer" id="q-158-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-158-a-01">NSZE 決定可定址範圍，NCAP 決定可配置的 logical blocks；兩者都使用選定格式的 block 單位，不是 bytes。</p><div class="qa-sections">
<section class="qa-section" id="q-158-s-01" data-answer-section="1"><h3><span>1.</span> 先確認資料的來源與範圍</h3>
<span class="qa-anchor" id="q-158-a-02"></span><p>建立新 namespace 會消耗其 NVM Set／Endurance Group 的容量，但尚未附加任何 controller。</p>
<span class="qa-anchor" id="q-158-a-03"></span><p>查共同 namespace 能力、格式清單、thin provisioning 支援與未配置容量；有 granularity 資訊時一併使用。</p>
</section>
<section class="qa-section" id="q-158-s-02" data-answer-section="2"><h3><span>2.</span> 欄位、單位與判讀例子</h3>
<span class="qa-anchor" id="q-158-a-04"></span><p>填 NSZE、NCAP、FLBAS、DPS、NMIC 及需要的資源 IDs。NCAP 不得大於 NSZE；使用小於 NSZE 的 NCAP 需要相應 thin provisioning 支援。</p>
<span class="qa-anchor" id="q-158-a-05"></span><p>先選格式再換算 blocks。假設 1000 個 4KiB blocks，就是 4000KiB 使用者容量；實際 NVM allocation 可能因配置單位而更大。</p>
<span class="qa-anchor" id="q-158-a-06"></span><p>Create 成功 CQE.DW0 回 NSID，並以指定屬性格式化；再查 Identify 確認，之後才 Attach。</p>
</section>
<section class="qa-section" id="q-158-s-03" data-answer-section="3"><h3><span>3.</span> 判讀時要保留的條件</h3>
<span class="qa-anchor" id="q-158-a-07"></span><p>非法格式回 Invalid Format；不支援 thin provisioning 有專屬狀態；資源不足另分容量與 NSID 上限。</p>
<span class="qa-anchor" id="q-158-a-16"></span><p>比較要求的 blocks／格式與回報的 NSZE／NCAP／NVMCAP，不要求它們有相同單位或數值。</p>
</section>
</div>
<span class="qa-anchor" id="q-158-a-17"></span><span class="qa-anchor" id="q-158-a-08"></span><span class="qa-anchor" id="q-158-a-09"></span><span class="qa-anchor" id="q-158-a-10"></span><span class="qa-anchor" id="q-158-a-11"></span><span class="qa-anchor" id="q-158-a-12"></span><span class="qa-anchor" id="q-158-a-13"></span><span class="qa-anchor" id="q-158-a-14"></span><span class="qa-anchor" id="q-158-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-159" data-question="159" data-answer-kind="error"><h2><a class="qa-qid" href="#q-159">Q159</a> Create Namespace 容量不足或參數不合法如何回應？</h2>
<p class="qa-prompt">先區分失敗條件，再判斷是否有規範明定的回報結果。</p>
<details class="qa-answer" id="q-159-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-159-a-01">失敗原因可以是容量、識別碼數量、格式或資源歸屬。分清它們才知道縮小容量、刪除其他 namespace 或改格式是否有用。</p><div class="qa-sections">
<section class="qa-section" id="q-159-s-01" data-answer-section="1"><h3><span>1.</span> 先區分是哪一種失敗</h3>
<span class="qa-anchor" id="q-159-a-02"></span><p>容量依所選資源池判斷，不能把其他 Endurance Group 的剩餘空間直接當成可用。</p>
<span class="qa-anchor" id="q-159-a-04"></span><p>1/15h 是 Namespace Insufficient Capacity，1/16h 是 Namespace Identifier Unavailable，1/0Ah 是 Invalid Format，1/1Bh 是 Thin Provisioning Not Supported。</p>
<span class="qa-anchor" id="q-159-a-07"></span><p>沒有遵循 granularity 的偏好倍數可能浪費 allocation capacity，但不應只因未符合偏好就拒絕原本合法的 Create。</p>
</section>
<section class="qa-section" id="q-159-s-02" data-answer-section="2"><h3><span>2.</span> 用哪些資料確認原因</h3>
<span class="qa-anchor" id="q-159-a-03"></span><p>讀未配置容量、NN／MNAN 的適用定義、格式與 granularity，以及 NVM Set／EG 清單。</p>
<span class="qa-anchor" id="q-159-a-05"></span><p>以合法基準逐項改參數；容量不足時讀 Error Information.CSINFO 的所需未配置容量 bytes，再決定修正。</p>
</section>
<section class="qa-section" id="q-159-s-03" data-answer-section="3"><h3><span>3.</span> 結果與後續驗證</h3>
<span class="qa-anchor" id="q-159-a-06"></span><p>拒絕後不能把任意 DW0 當成新 NSID，只有成功 Create 的 DW0 才具有該意義。</p>
<span class="qa-anchor" id="q-159-a-16"></span><p>比對要求量與真正配置量，區分「格式不允許」與「可用容量不足」。</p>
<span class="qa-anchor" id="q-159-a-17"></span><p>先查失敗 Status 的完整 SCT／SC，再決定是哪個資源不足。</p>
</section>
</div>
<span class="qa-anchor" id="q-159-a-08"></span><span class="qa-anchor" id="q-159-a-09"></span><span class="qa-anchor" id="q-159-a-10"></span><span class="qa-anchor" id="q-159-a-11"></span><span class="qa-anchor" id="q-159-a-12"></span><span class="qa-anchor" id="q-159-a-13"></span><span class="qa-anchor" id="q-159-a-14"></span><span class="qa-anchor" id="q-159-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-160" data-question="160" data-answer-kind="process"><h2><a class="qa-qid" href="#q-160">Q160</a> Create 後 Allocated Namespace List 如何更新？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-160-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-160-a-01">Allocated 表示 namespace 已存在；Active 表示可經某 controller 存取。Create 只先建立前者。</p><div class="qa-sections">
<section class="qa-section" id="q-160-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-160-a-02"></span><p>Allocated List 描述適用 inventory；各 controller 的 Active List 可不同。</p>
<span class="qa-anchor" id="q-160-a-03"></span><p>使用 Identify CNS10h 與新 NSID 的 Identify；Active List CNS02h 用於後續 Attach 驗證。</p>
<span class="qa-anchor" id="q-160-a-04"></span><p>Create CQE.DW0 回傳 controller 選出的 NSID，不是 Host 預先保證的連號。</p>
</section>
<section class="qa-section" id="q-160-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-160-a-05"></span><p>保存建立前清單，等待成功後重新列舉，確認新 ID 出現並可讀其已配置屬性。</p>
<span class="qa-anchor" id="q-160-a-06"></span><p>新 ID 應在 Allocated List，但不應因 Create 自動出現在任何 controller 的 Active List。</p>
</section>
<section class="qa-section" id="q-160-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-160-a-07"></span><p>清單太長時依 NSID 起點繼續讀；只讀第一頁就說新 ID 不存在可能是 Host 錯誤。</p>
<span class="qa-anchor" id="q-160-a-16"></span><p>對回 DW0、Allocated List 與 namespace 屬性，避免只用數量增加判斷是哪個物件。</p>
</section>
</div>
<span class="qa-anchor" id="q-160-a-17"></span><span class="qa-anchor" id="q-160-a-08"></span><span class="qa-anchor" id="q-160-a-09"></span><span class="qa-anchor" id="q-160-a-10"></span><span class="qa-anchor" id="q-160-a-11"></span><span class="qa-anchor" id="q-160-a-12"></span><span class="qa-anchor" id="q-160-a-13"></span><span class="qa-anchor" id="q-160-a-14"></span><span class="qa-anchor" id="q-160-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-161" data-question="161" data-answer-kind="process"><h2><a class="qa-qid" href="#q-161">Q161</a> Attach／Detach 如何指定 Controller？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-161-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-161-a-01">Attachment 改變存取關係，不建立或刪除 namespace，也不改它的使用者資料格式。</p><div class="qa-sections">
<section class="qa-section" id="q-161-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-161-a-02"></span><p>命令 NSID 指目標 namespace，資料中的 Controller List 指要變更的 controllers。</p>
<span class="qa-anchor" id="q-161-a-03"></span><p>確認目標已配置、共享能力、controller IDs、Command Set 支援與 MAXCNA／MAXDNA 限制。</p>
<span class="qa-anchor" id="q-161-a-04"></span><p>SEL0=Attach，1=Detach；傳輸 4096-byte Controller List。List 的 entries 是 CNTLID，不是 NSID。</p>
</section>
<section class="qa-section" id="q-161-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-161-a-05"></span><p>建立合法清單，提交並等待完成，再到每個目標 controller 查 Active List 與 namespace 的 Controller List。</p>
<span class="qa-anchor" id="q-161-a-06"></span><p>成功後只有所列關係變更，namespace 仍在 Allocated inventory 中。</p>
</section>
<section class="qa-section" id="q-161-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-161-a-07"></span><p>Controller List 有非法或 Administrative controller 時回 Controller List Invalid；命令集不支援與未啟用各有不同狀態。</p>
<span class="qa-anchor" id="q-161-a-16"></span><p>失敗時 Error Information.CSINFO 指第一個失敗 entry 的 byte offset；遇錯後不再處理後續 entries，不能假設整個清單全部回復。</p>
</section>
</div>
<span class="qa-anchor" id="q-161-a-17"></span><span class="qa-anchor" id="q-161-a-08"></span><span class="qa-anchor" id="q-161-a-09"></span><span class="qa-anchor" id="q-161-a-10"></span><span class="qa-anchor" id="q-161-a-11"></span><span class="qa-anchor" id="q-161-a-12"></span><span class="qa-anchor" id="q-161-a-13"></span><span class="qa-anchor" id="q-161-a-14"></span><span class="qa-anchor" id="q-161-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-162" data-question="162" data-answer-kind="process"><h2><a class="qa-qid" href="#q-162">Q162</a> Attach／Detach 後 Active List 與 Controller List 如何互相驗證？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-162-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-162-a-01">同一關係可以從 controller 看可用 namespaces，也可以從 namespace 看附加 controllers；雙向核對能找出只更新一邊的錯誤。</p><div class="qa-sections">
<section class="qa-section" id="q-162-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-162-a-02"></span><p>每個 controller 的 Active List 只代表自己，不能當成 subsystem 全部 namespace。</p>
<span class="qa-anchor" id="q-162-a-03"></span><p>用 CNS02h 與 CNS12h 等適用 Identify 清單，並核對 controller 身分。</p>
<span class="qa-anchor" id="q-162-a-04"></span><p>保存 NSID、CNTLID、查詢起點與回傳 entries，避免分頁時漏掉目標。</p>
</section>
<section class="qa-section" id="q-162-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-162-a-05"></span><p>Attach 成功後兩個方向都應呈現關係；Detach 成功後兩個方向都不再呈現該附加關係。</p>
<span class="qa-anchor" id="q-162-a-06"></span><p>例如 namespace7 只附加 A，Attach 到 B 後，B 的 Active 含 7，namespace7 的 Controller List 含 A、B。</p>
</section>
<section class="qa-section" id="q-162-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-162-a-07"></span><p>查詢期間若另有管理操作，清單可能代表不同時間；先停止變更或建立穩定快照，再判矛盾。</p>
<span class="qa-anchor" id="q-162-a-16"></span><p>Allocated List 在單純 Attach／Detach 前後仍應保留該 namespace，與 active 關係分開比較。</p>
</section>
</div>
<span class="qa-anchor" id="q-162-a-17"></span><span class="qa-anchor" id="q-162-a-08"></span><span class="qa-anchor" id="q-162-a-09"></span><span class="qa-anchor" id="q-162-a-10"></span><span class="qa-anchor" id="q-162-a-11"></span><span class="qa-anchor" id="q-162-a-12"></span><span class="qa-anchor" id="q-162-a-13"></span><span class="qa-anchor" id="q-162-a-14"></span><span class="qa-anchor" id="q-162-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-163" data-question="163" data-answer-kind="error"><h2><a class="qa-qid" href="#q-163">Q163</a> 重複 Attach、非法 Controller 或未 Attach 就 Detach 如何回應？</h2>
<p class="qa-prompt">先區分失敗條件，再判斷是否有規範明定的回報結果。</p>
<details class="qa-answer" id="q-163-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-163-a-01">這些錯誤描述關係與清單，不代表 namespace 資料必定損壞。</p><div class="qa-sections">
<section class="qa-section" id="q-163-s-01" data-answer-section="1"><h3><span>1.</span> 先區分是哪一種失敗</h3>
<span class="qa-anchor" id="q-163-a-02"></span><p>以每個 Controller List entry 當時的附加狀態判斷，可能在前幾項成功後才遇到錯誤。</p>
<span class="qa-anchor" id="q-163-a-04"></span><p>Already Attached=1/18h，Private=1/19h，Not Attached=1/1Ah，Controller List Invalid=1/1Ch。</p>
<span class="qa-anchor" id="q-163-a-07"></span><p>Private namespace 已附加一個 controller，附加第二個會因 Private 限制被拒絕；不是因容量不足。</p>
</section>
<section class="qa-section" id="q-163-s-02" data-answer-section="2"><h3><span>2.</span> 用哪些資料確認原因</h3>
<span class="qa-anchor" id="q-163-a-03"></span><p>讀目前 Controller List、NMIC 共享設定及目標 controller 能力。</p>
<span class="qa-anchor" id="q-163-a-05"></span><p>一次測一種關係錯誤，收到完成後讀回全部受測 entries，確認第一個錯誤位置與停止處理行為。</p>
</section>
<section class="qa-section" id="q-163-s-03" data-answer-section="3"><h3><span>3.</span> 結果與後續驗證</h3>
<span class="qa-anchor" id="q-163-a-06"></span><p>合法操作改變指定關係；負向操作回相應狀態，且不處理第一個失敗 entry 之後的 entries。</p>
<span class="qa-anchor" id="q-163-a-16"></span><p>把 Status、CSINFO offset 與前後清單一起驗證，避免只看整筆命令失敗就認定無任何變更。</p>
<span class="qa-anchor" id="q-163-a-17"></span><p>先查 namespace 是否為 private，以及是否早已附加。</p>
</section>
</div>
<span class="qa-anchor" id="q-163-a-08"></span><span class="qa-anchor" id="q-163-a-09"></span><span class="qa-anchor" id="q-163-a-10"></span><span class="qa-anchor" id="q-163-a-11"></span><span class="qa-anchor" id="q-163-a-12"></span><span class="qa-anchor" id="q-163-a-13"></span><span class="qa-anchor" id="q-163-a-14"></span><span class="qa-anchor" id="q-163-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-164" data-question="164" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-164">Q164</a> Detach 時還有 Outstanding Command，應如何處理？</h2>
<p class="qa-prompt">先用自己的話解釋機制，再舉一個常見誤解。</p>
<details class="qa-answer" id="q-164-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-164-a-01">Detach 會讓該 controller 對目標 NSID 的存取關係失效。Host 先停止新 I/O 並排空較容易管理，但韌體仍須正確處理未完成命令。</p><div class="qa-sections">
<section class="qa-section" id="q-164-s-01" data-answer-section="1"><h3><span>1.</span> 機制與適用範圍</h3>
<span class="qa-anchor" id="q-164-a-02"></span><p>只改變指定 controller 與 namespace 的關係；其他仍附加的 controller 不因此自動 Detach。</p>
<span class="qa-anchor" id="q-164-a-04"></span><p>Base8.1.17 將已提交但未完成及後續提交的目標命令，按 inactive NSID 規則處理；再套用各命令明文例外。</p>
</section>
<section class="qa-section" id="q-164-s-02" data-answer-section="2"><h3><span>2.</span> 用操作與結果理解</h3>
<span class="qa-anchor" id="q-164-a-03"></span><p>保存 outstanding SQID／CID、目標 NSID 與 Attachment 完成時間。</p>
<span class="qa-anchor" id="q-164-a-05"></span><p>停止新提交，完成需要的資料同步，等待可排空的工作，再 Detach；若刻意測競爭，完整保存命令與狀態轉移順序。</p>
<span class="qa-anchor" id="q-164-a-06"></span><p>Detach 成功後關係消失；先前已完成的命令不重複完成，未完成者按 inactive 規則處理。</p>
</section>
<section class="qa-section" id="q-164-s-03" data-answer-section="3"><h3><span>3.</span> 容易誤判的地方</h3>
<span class="qa-anchor" id="q-164-a-07"></span><p>通用 inactive 規則是 Invalid Field，但命令可另有明確例外；不能把所有命令強制寫成同一碼。</p>
<span class="qa-anchor" id="q-164-a-16"></span><p>確認沒有把已完成的 I/O 誤歸到 Detach 後，也沒有在完成前回收仍可能使用的 buffer。</p>
</section>
</div>
<span class="qa-anchor" id="q-164-a-17"></span><span class="qa-anchor" id="q-164-a-08"></span><span class="qa-anchor" id="q-164-a-09"></span><span class="qa-anchor" id="q-164-a-10"></span><span class="qa-anchor" id="q-164-a-11"></span><span class="qa-anchor" id="q-164-a-12"></span><span class="qa-anchor" id="q-164-a-13"></span><span class="qa-anchor" id="q-164-a-14"></span><span class="qa-anchor" id="q-164-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-165" data-question="165" data-answer-kind="error"><h2><a class="qa-qid" href="#q-165">Q165</a> Detach 後再送 Namespace Command 應得到什麼？</h2>
<p class="qa-prompt">先區分失敗條件，再判斷是否有規範明定的回報結果。</p>
<details class="qa-answer" id="q-165-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-165-a-01">Detach 使 NSID 在該 controller 成為 inactive，不是從 subsystem 刪除。這個區別決定後續命令與查詢怎麼處理。</p><div class="qa-sections">
<section class="qa-section" id="q-165-s-01" data-answer-section="1"><h3><span>1.</span> 先區分是哪一種失敗</h3>
<span class="qa-anchor" id="q-165-a-02"></span><p>同一 NSID 仍可在另一個已附加 controller 上 active，因此路徑是判斷的一部分。</p>
<span class="qa-anchor" id="q-165-a-04"></span><p>對使用 NSID 的命令，Figure93 指定 inactive 預設 Invalid Field；Identify 管理查詢等有自身 selector 規則。</p>
<span class="qa-anchor" id="q-165-a-07"></span><p>不能把所有成功的 Identify 都當成「Detach 沒生效」，也不能把 inactive 與非法 NSID 的 Status 混用。</p>
</section>
<section class="qa-section" id="q-165-s-02" data-answer-section="2"><h3><span>2.</span> 用哪些資料確認原因</h3>
<span class="qa-anchor" id="q-165-a-03"></span><p>查該 controller Active List、Allocated List 與 namespace Controller List。</p>
<span class="qa-anchor" id="q-165-a-05"></span><p>等 Detach 完成，再從已 Detach 的 controller 提交目標命令；對比仍 attached 的 controller，保持其他條件相同。</p>
</section>
<section class="qa-section" id="q-165-s-03" data-answer-section="3"><h3><span>3.</span> 結果與後續驗證</h3>
<span class="qa-anchor" id="q-165-a-06"></span><p>正常資料存取不能因 namespace 仍存在就繼續視為 active；允許查已配置物件的管理命令則仍可合法工作。</p>
<span class="qa-anchor" id="q-165-a-16"></span><p>用具體 Opcode／CNS 的規則比對，而不是只看 NSID 相同。</p>
<span class="qa-anchor" id="q-165-a-17"></span><p>先確認測試送的是 I/O，還是允許查詢 inactive 物件的 Admin 命令。</p>
</section>
</div>
<span class="qa-anchor" id="q-165-a-08"></span><span class="qa-anchor" id="q-165-a-09"></span><span class="qa-anchor" id="q-165-a-10"></span><span class="qa-anchor" id="q-165-a-11"></span><span class="qa-anchor" id="q-165-a-12"></span><span class="qa-anchor" id="q-165-a-13"></span><span class="qa-anchor" id="q-165-a-14"></span><span class="qa-anchor" id="q-165-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-166" data-question="166" data-answer-kind="error"><h2><a class="qa-qid" href="#q-166">Q166</a> 刪除不存在或仍 Attached 的 Namespace 如何處理？</h2>
<p class="qa-prompt">先區分失敗條件，再判斷是否有規範明定的回報結果。</p>
<details class="qa-answer" id="q-166-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-166-a-01">需要修正「Attached 就一定禁止刪除」的前提：規範建議先 Detach，但 Delete 也會將 namespace 從所有 controllers 移除。</p><div class="qa-sections">
<section class="qa-section" id="q-166-s-01" data-answer-section="1"><h3><span>1.</span> 先區分是哪一種失敗</h3>
<span class="qa-anchor" id="q-166-a-02"></span><p>Delete 移除 subsystem 中的物件，不只是某個 controller 的存取關係。</p>
<span class="qa-anchor" id="q-166-a-04"></span><p>Management SEL=1 為 Delete，NSID 選既有物件；FFFFFFFFh 表示刪除全部，沒有任何 valid namespace 時此全刪操作仍成功。</p>
<span class="qa-anchor" id="q-166-a-07"></span><p>特定不存在 ID 依 NSID 類型與命令規則拒絕；不能套用全刪空集合成功的例外。保護或正在清除另有相應拒絕條件。</p>
</section>
<section class="qa-section" id="q-166-s-02" data-answer-section="2"><h3><span>2.</span> 用哪些資料確認原因</h3>
<span class="qa-anchor" id="q-166-a-03"></span><p>確認 Allocated List、保護狀態、背景操作與影響範圍，再選單一或全部刪除。</p>
<span class="qa-anchor" id="q-166-a-05"></span><p>停止相關 I/O，建議先從所有 controllers Detach，再 Delete，最後讀回 Allocated／Active lists。</p>
</section>
<section class="qa-section" id="q-166-s-03" data-answer-section="3"><h3><span>3.</span> 結果與後續驗證</h3>
<span class="qa-anchor" id="q-166-a-06"></span><p>成功後 namespace 不再存在，原附加關係也消失；原 NSID 可能以後重用，不能只用數字當永久身分。</p>
<span class="qa-anchor" id="q-166-a-16"></span><p>對比刪除前後完整 inventory 與識別資訊，確認沒有僅 Detach 而未 Delete。</p>
<span class="qa-anchor" id="q-166-a-17"></span><p>先查是否用了 FFFFFFFFh，這會改變空集合的完成語意。</p>
</section>
</div>
<span class="qa-anchor" id="q-166-a-08"></span><span class="qa-anchor" id="q-166-a-09"></span><span class="qa-anchor" id="q-166-a-10"></span><span class="qa-anchor" id="q-166-a-11"></span><span class="qa-anchor" id="q-166-a-12"></span><span class="qa-anchor" id="q-166-a-13"></span><span class="qa-anchor" id="q-166-a-14"></span><span class="qa-anchor" id="q-166-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-167" data-question="167" data-answer-kind="events"><h2><a class="qa-qid" href="#q-167">Q167</a> Namespace 變更後哪些事件與 Log 應更新？</h2>
<p class="qa-prompt">先說明事件成立的條件，再區分通知、事件確認與紀錄。</p>
<details class="qa-answer" id="q-167-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-167-a-01">變更通知讓 Host 更新已快取的配置；事件、變更清單與 Identify 現況各自回答不同問題。</p><div class="qa-sections">
<section class="qa-section" id="q-167-s-01" data-answer-section="1"><h3><span>1.</span> 事件何時成立、由誰觀察</h3>
<span class="qa-anchor" id="q-167-a-02"></span><p>Create／Delete 改 inventory；Attach／Detach 改特定 controller 的 Active List。</p>
<span class="qa-anchor" id="q-167-a-03"></span><p>確認 Attached／Allocated notices 的支援與 AEC，以及 AER 是否可用。</p>
<span class="qa-anchor" id="q-167-a-04"></span><p>LID04h 列 attached namespace 變更，1Ch 列 allocated 變更；Identify 再查目前狀態，PEL Change Namespace 記錄其定義的管理事件。</p>
</section>
<section class="qa-section" id="q-167-s-02" data-answer-section="2"><h3><span>2.</span> 通知、讀取與確認的關係</h3>
<span class="qa-anchor" id="q-167-a-05"></span><p>管理命令完成後處理各受影響 controller 的通知，保存變更清單，再重新 Identify。</p>
<span class="qa-anchor" id="q-167-a-06"></span><p>Admin Delete 的提交端不回報該次刪除通知；其他符合條件的 controller 仍回報。不能要求每端通知數必須一樣。</p>
</section>
<section class="qa-section" id="q-167-s-03" data-answer-section="3"><h3><span>3.</span> 沒有通知或紀錄時怎麼判斷</h3>
<span class="qa-anchor" id="q-167-a-07"></span><p>未啟用通知、事件已遮蔽或已被讀取確認，都會影響可見 AER；不是只用「命令成功卻沒 AER」判錯。</p>
<span class="qa-anchor" id="q-167-a-16"></span><p>將命令來源、受影響清單與各 controller AEC 放在同一張時間表，避免混淆觀察端。</p>
<span class="qa-anchor" id="q-167-a-17"></span><p>先查自己是不是處理 Admin Delete 的那個 controller。</p>
</section>
<section class="qa-section" id="q-167-s-04" data-answer-section="4"><h3><span>4.</span> 分開核對事件通知與 Log 紀錄</h3>
<span class="qa-anchor" id="q-167-a-09"></span><p>Create／Delete 影響 Allocated List，Attach／Detach 影響指定 controller 的 Active List。 <a class="qa-rule-link" href="#common-namespace_op-9">完整條件見本冊說明</a></p>
<span class="qa-anchor" id="q-167-a-10"></span><p>使用 Identify 的 Allocated、Active 與 Controller List 確認目前配置；Changed Attached Namespace List04h 與 Changed Allocated Namespace List1Ch 指出曾變更的 NSID，不能代替完整現況。 <a class="qa-rule-link" href="#common-namespace_op-10">完整條件見本冊說明</a></p>
<span class="qa-anchor" id="q-167-a-11"></span><p>支援 PEL 時，Namespace Management 對應的 Change Namespace Event06h 記錄建立／刪除等規定事件。 <a class="qa-rule-link" href="#common-namespace_op-11">完整條件見本冊說明</a></p>
</section>
</div>
<span class="qa-anchor" id="q-167-a-08"></span><span class="qa-anchor" id="q-167-a-12"></span><span class="qa-anchor" id="q-167-a-13"></span><span class="qa-anchor" id="q-167-a-14"></span><span class="qa-anchor" id="q-167-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-changedlog">Base 2.4 §5.2.13.1.5</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-168" data-question="168" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-168">Q168</a> Changed Namespace List 超過容量如何表示？</h2>
<p class="qa-prompt">先試著說明欄位的單位與編碼，再用一組數值推導結果。</p>
<details class="qa-answer" id="q-168-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-168-a-01">變更清單容量有限，溢位標記要求 Host 重新探索全部相關 namespace，而不是只相信不完整清單。</p><div class="qa-sections">
<section class="qa-section" id="q-168-s-01" data-answer-section="1"><h3><span>1.</span> 先確認資料的來源與範圍</h3>
<span class="qa-anchor" id="q-168-a-02"></span><p>LID04h 針對該 controller 的 attached namespace 變更，不是整個 subsystem 的通用變更歷史。</p>
<span class="qa-anchor" id="q-168-a-03"></span><p>查看 LID04h 的固定 1024 個 NSID entry 與讀取／清除規則。</p>
</section>
<section class="qa-section" id="q-168-s-02" data-answer-section="2"><h3><span>2.</span> 欄位、單位與判讀例子</h3>
<span class="qa-anchor" id="q-168-a-04"></span><p>超過 1024 個變更 namespace 時，第一筆 FFFFFFFFh，其餘清零，表示不能逐筆列全。</p>
<span class="qa-anchor" id="q-168-a-05"></span><p>先判斷第一筆是否為溢位標記；若是，重新列舉並讀取需要的 namespace 屬性，不把 FFFFFFFFh 當實際 namespace。</p>
<span class="qa-anchor" id="q-168-a-06"></span><p>完整重掃能恢復現況；不要求 controller 透過多讀幾次 04h 分頁吐出被省略的全部歷史。</p>
</section>
<section class="qa-section" id="q-168-s-03" data-answer-section="3"><h3><span>3.</span> 判讀時要保留的條件</h3>
<span class="qa-anchor" id="q-168-a-07"></span><p>Get Log 傳輸截短與清單自身溢位不同；短 buffer 不應被誤判成沒有其他變更。</p>
<span class="qa-anchor" id="q-168-a-16"></span><p>比較最終 Identify 現況與重掃後 Host 快取，確認溢位後仍能正確同步。</p>
</section>
</div>
<span class="qa-anchor" id="q-168-a-17"></span><span class="qa-anchor" id="q-168-a-08"></span><span class="qa-anchor" id="q-168-a-09"></span><span class="qa-anchor" id="q-168-a-10"></span><span class="qa-anchor" id="q-168-a-11"></span><span class="qa-anchor" id="q-168-a-12"></span><span class="qa-anchor" id="q-168-a-13"></span><span class="qa-anchor" id="q-168-a-14"></span><span class="qa-anchor" id="q-168-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-changedlog">Base 2.4 §5.2.13.1.5</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-169" data-question="169" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-169">Q169</a> Reset 或 Power Cycle 後 Namespace 配置與 Attachment 是否保留？</h2>
<p class="qa-prompt">先指明重設或中斷的方式，再分別判斷設定、進行中的操作與資料。</p>
<details class="qa-answer" id="q-169-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-169-a-01">namespace 是持久配置，不隨 queue 重建而重新建立。將這兩層分開，才能避免恢復時誤刪或重複建立物件。</p><div class="qa-sections">
<section class="qa-section" id="q-169-s-01" data-answer-section="1"><h3><span>1.</span> 先界定觸發方式與影響對象</h3>
<span class="qa-anchor" id="q-169-a-02"></span><p>已完成的配置與 attachment 保留；未完成命令則需恢復後查實際狀態。</p>
<span class="qa-anchor" id="q-169-a-03"></span><p>保存 namespace 全球識別、NSID、格式與附加清單，恢復後重新 Identify。</p>
</section>
<section class="qa-section" id="q-169-s-02" data-answer-section="2"><h3><span>2.</span> 哪些狀態改變，恢復後怎麼處理</h3>
<span class="qa-anchor" id="q-169-a-04"></span><p>Controller Reset、Subsystem Reset 與 Power Cycle 不等於 Restore Default Namespace Configuration；後者是明確管理操作。</p>
<span class="qa-anchor" id="q-169-a-05"></span><p>恢復 Admin Queue 後列舉既有 namespace，確認附加關係，再建 I/O queues，而不是無條件重新 Create。</p>
<span class="qa-anchor" id="q-169-a-06"></span><p>原合法配置可恢復存取；Secondary Controller Offline 操作也不應清除 attachment。</p>
</section>
<section class="qa-section" id="q-169-s-03" data-answer-section="3"><h3><span>3.</span> 重設或斷電時，要確認什麼</h3>
<span class="qa-anchor" id="q-169-a-12"></span>
<span class="qa-anchor" id="q-169-a-13"></span>
<span class="qa-anchor" id="q-169-a-14"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">觸發方式</th><th scope="col">這項操作或狀態會如何變化</th></tr></thead><tbody><tr><td>Controller Reset 後是否保留或繼續？</td><td>已完成的 namespace 配置與 Attach／Detach 跨 Reset 保留；重設的是命令通道，不是自動刪除 namespace。若 Reset 前未收到完成，恢復後須查清單確認結果，不能假設整筆操作必定回復。</td></tr><tr><td>NVM Subsystem Reset 後是否保留或繼續？</td><td>Subsystem Reset 不等於 Restore Default Namespace Configuration。恢復後重新探索原 namespace 與附加關係，再建立 I/O queues；多 domain 的實際 Reset 範圍另行確認。</td></tr><tr><td>Power Cycle 後是否保留或繼續？</td><td>Power Cycle 後，已完成的 namespace 配置與附加關係仍需保留。Write Protect 與 Permanent Write Protect 保留；Write Protect Until Power Cycle 則在實際 power cycle 轉回未保護，不能把這個例外套到全部配置。</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-169-s-04" data-answer-section="4"><h3><span>4.</span> 如何驗證保留或恢復結果</h3>
<span class="qa-anchor" id="q-169-a-07"></span><p>若 Reset 前命令結果未知，清單可顯示已成功的變更；不能只因未收到 CQE 就假設沒有執行。</p>
<span class="qa-anchor" id="q-169-a-16"></span><p>用持久身分與屬性比對，避免 NSID 重用造成誤配。</p>
<span class="qa-anchor" id="q-169-a-17"></span><p>先確認 Host 恢復程序有沒有自己做 Restore 或 Delete。</p>
</section>
</div>
<span class="qa-anchor" id="q-169-a-08"></span><span class="qa-anchor" id="q-169-a-09"></span><span class="qa-anchor" id="q-169-a-10"></span><span class="qa-anchor" id="q-169-a-11"></span><span class="qa-anchor" id="q-169-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-170" data-question="170" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-170">Q170</a> Private 與 Shared Namespace 有何差別？</h2>
<p class="qa-prompt">先說出比較對象最重要的差別，並舉一個不能互相代用的例子。</p>
<details class="qa-answer" id="q-170-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-170-a-01">Private 限制同時附加一個 controller；Shared 可允許多 controller 附加。這是存取拓樸，不是資料加密或讀寫權限名稱。</p><div class="qa-sections">
<section class="qa-section" id="q-170-s-01" data-answer-section="1"><h3><span>1.</span> 差別在哪裡</h3>
<span class="qa-anchor" id="q-170-a-02"></span><p>多條路徑可指向同一份 namespace 資料，不能把每條路徑當成獨立副本。</p>
<span class="qa-anchor" id="q-170-a-04"></span><p>Create 時指定 NMIC，Attachment 用 Controller List 操作關係；Shared 仍受 MAXCNA／MAXDNA 等限制。</p>
</section>
<section class="qa-section" id="q-170-s-02" data-answer-section="2"><h3><span>2.</span> 如何選擇與確認</h3>
<span class="qa-anchor" id="q-170-a-03"></span><p>看 Identify Namespace.NMIC 共享能力與實際 Controller List。</p>
<span class="qa-anchor" id="q-170-a-05"></span><p>先配置共享屬性，再附加需要的 controllers，逐端查 Active List。</p>
<span class="qa-anchor" id="q-170-a-06"></span><p>Shared 可由多端存取；Private 從 A Detach 後可再 Attach 到 B，但不能同時保有兩端關係。</p>
</section>
<section class="qa-section" id="q-170-s-03" data-answer-section="3"><h3><span>3.</span> 哪些結論不能互相套用</h3>
<span class="qa-anchor" id="q-170-a-07"></span><p>Private 已附加另一 controller 時，新增附加回 Namespace Is Private。</p>
<span class="qa-anchor" id="q-170-a-16"></span><p>檢查身分、資料與附加關係，避免把多路徑誤算成多份容量。</p>
</section>
</div>
<span class="qa-anchor" id="q-170-a-17"></span><span class="qa-anchor" id="q-170-a-08"></span><span class="qa-anchor" id="q-170-a-09"></span><span class="qa-anchor" id="q-170-a-10"></span><span class="qa-anchor" id="q-170-a-11"></span><span class="qa-anchor" id="q-170-a-12"></span><span class="qa-anchor" id="q-170-a-13"></span><span class="qa-anchor" id="q-170-a-14"></span><span class="qa-anchor" id="q-170-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-171" data-question="171" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-171">Q171</a> 三種 Write Protection 模式與進入條件有何不同？</h2>
<p class="qa-prompt">先說出比較對象最重要的差別，並舉一個不能互相代用的例子。</p>
<details class="qa-answer" id="q-171-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-171-a-01">保護模式決定能否解除以及何時解除；選 Permanent 前必須理解它不是可隨時切回的普通開關。</p><div class="qa-sections">
<section class="qa-section" id="q-171-s-01" data-answer-section="1"><h3><span>1.</span> 差別在哪裡</h3>
<span class="qa-anchor" id="q-171-a-02"></span><p>WPS 屬於 namespace，所有附加 controllers 共同執行。</p>
<span class="qa-anchor" id="q-171-a-04"></span><p>WPS0=未保護，1=Write Protect，2=Until Power Cycle，3=Permanent。一般 Write Protect 可用合法 Set 解除，後兩者不能靠 Set 任意改變。</p>
</section>
<section class="qa-section" id="q-171-s-02" data-answer-section="2"><h3><span>2.</span> 如何選擇與確認</h3>
<span class="qa-anchor" id="q-171-a-03"></span><p>NWPC 宣告支援模式；RPMB 的 WPC 控制進入 Until Power Cycle 或 Permanent 是否被允許；FID84h 回報實際 WPS。</p>
<span class="qa-anchor" id="q-171-a-05"></span><p>查能力與進入許可，設定 WPS，等待完成，再 Get 確認。轉入受保護狀態前，controller 須提交該 namespace 的 volatile cache data／metadata 到非揮發媒體。</p>
<span class="qa-anchor" id="q-171-a-06"></span><p>WPS 與實際禁止改寫的行為一致；Read 仍可依正常條件處理。</p>
</section>
<section class="qa-section" id="q-171-s-03" data-answer-section="3"><h3><span>3.</span> 哪些結論不能互相套用</h3>
<span class="qa-anchor" id="q-171-a-07"></span><p>進入未允許狀態或改變 Until Power Cycle／Permanent 回 Feature Not Changeable；multi-domain 不得使用 Until Power Cycle。</p>
<span class="qa-anchor" id="q-171-a-16"></span><p>WPC 只是進入許可，不是 WPS；把控制位清零不會自動解除既有保護。</p>
</section>
</div>
<span class="qa-anchor" id="q-171-a-17"></span><span class="qa-anchor" id="q-171-a-08"></span><span class="qa-anchor" id="q-171-a-09"></span><span class="qa-anchor" id="q-171-a-10"></span><span class="qa-anchor" id="q-171-a-11"></span><span class="qa-anchor" id="q-171-a-12"></span><span class="qa-anchor" id="q-171-a-13"></span><span class="qa-anchor" id="q-171-a-14"></span><span class="qa-anchor" id="q-171-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-172" data-question="172" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-172">Q172</a> Write Protection 在 Reset 與 Power Cycle 後如何保留？</h2>
<p class="qa-prompt">先指明重設或中斷的方式，再分別判斷設定、進行中的操作與資料。</p>
<details class="qa-answer" id="q-172-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-172-a-01">FID84h 不可保存，不代表保護不持續。其狀態有明確持久性，不能套用一般 Saved Feature 的直覺。</p><div class="qa-sections">
<section class="qa-section" id="q-172-s-01" data-answer-section="1"><h3><span>1.</span> 先界定觸發方式與影響對象</h3>
<span class="qa-anchor" id="q-172-a-02"></span><p>保留規則跟隨 namespace，不因 controller 更換而解除。</p>
<span class="qa-anchor" id="q-172-a-03"></span><p>Get FID84h 讀 Current WPS，並記錄實際 Reset 來源及是否有 power cycle。</p>
</section>
<section class="qa-section" id="q-172-s-02" data-answer-section="2"><h3><span>2.</span> 哪些狀態改變，恢復後怎麼處理</h3>
<span class="qa-anchor" id="q-172-a-04"></span><p>WPS1／3 跨 Reset 與 power cycle 保留；WPS2 跨非 power-cycle 的 CLR 保留，但 power cycle 回 WPS0。</p>
<span class="qa-anchor" id="q-172-a-05"></span><p>建立基準狀態，執行指定事件，恢復後 Get 並驗證寫入限制；不要把 CC.EN 清零當成拔電。</p>
<span class="qa-anchor" id="q-172-a-06"></span><p>普通 Controller Reset 後 WPS2 仍受保護，是正確結果；真正 power cycle 後則解除。</p>
</section>
<section class="qa-section" id="q-172-s-03" data-answer-section="3"><h3><span>3.</span> 如何驗證保留或恢復結果</h3>
<span class="qa-anchor" id="q-172-a-07"></span><p>本 Feature 沒有 Default 值，Get SEL=Default 回 Invalid Field；不能要求一個虛構 Default 來解釋恢復。</p>
<span class="qa-anchor" id="q-172-a-16"></span><p>同時比對讀回 WPS 與 Write／Format 限制，不只確認 Set 曾成功。</p>
<span class="qa-anchor" id="q-172-a-17"></span><p>先查測試使用的 Reset 是否真的包含電源循環。</p>
</section>
</div>
<span class="qa-anchor" id="q-172-a-08"></span><span class="qa-anchor" id="q-172-a-09"></span><span class="qa-anchor" id="q-172-a-10"></span><span class="qa-anchor" id="q-172-a-11"></span><span class="qa-anchor" id="q-172-a-12"></span><span class="qa-anchor" id="q-172-a-13"></span><span class="qa-anchor" id="q-172-a-14"></span><span class="qa-anchor" id="q-172-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/features/zh-tw/#q-065">Q65</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-173" data-question="173" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-173">Q173</a> Write Protection 如何影響 Format、Sanitize 與 Namespace Management？</h2>
<p class="qa-prompt">先用自己的話解釋機制，再舉一個常見誤解。</p>
<details class="qa-answer" id="q-173-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-173-a-01">保護不只阻止 Write；任何會修改受保護 namespace 的操作，都要依命令互動規則檢查，包含未直接指定它的廣範圍操作。</p><div class="qa-sections">
<section class="qa-section" id="q-173-s-01" data-answer-section="1"><h3><span>1.</span> 機制與適用範圍</h3>
<span class="qa-anchor" id="q-173-a-02"></span><p>共享 namespace 在所有附加 controller 受保護；Format 或 Subsystem Sanitize 的 scope 若涵蓋它，也不能繞過。</p>
<span class="qa-anchor" id="q-173-a-04"></span><p>Read／Compare／Verify 等通常允許；Flush 成功且無效果，因進入保護時已提交 cache。Namespace Attachment 允許，但 Delete、Format 或 Sanitize 修改受保護物件會被限制。</p>
</section>
<section class="qa-section" id="q-173-s-02" data-answer-section="2"><h3><span>2.</span> 用操作與結果理解</h3>
<span class="qa-anchor" id="q-173-a-03"></span><p>查 WPS、命令 scope 與 Figure737 允許清單；不能只檢查 Opcode 名稱。</p>
<span class="qa-anchor" id="q-173-a-05"></span><p>先算完整影響範圍，再檢查所有受影響 namespace 的 WPS，最後套用命令的附加條件。</p>
<span class="qa-anchor" id="q-173-a-06"></span><p>允許查詢可正常完成；禁止修改應被拒絕且資料維持受保護，不因換 controller 就成功。</p>
</section>
<section class="qa-section" id="q-173-s-03" data-answer-section="3"><h3><span>3.</span> 容易誤判的地方</h3>
<span class="qa-anchor" id="q-173-a-07"></span><p>符合禁止修改條件時回 Namespace is Write Protected；不能因 Sanitize 通常忽略 SMART 唯讀警告，就忽略 Host 設定的 namespace 保護。</p>
<span class="qa-anchor" id="q-173-a-16"></span><p>以同一受保護資料測直接 Write 與跨 namespace 範圍操作，確認 scope 判斷一致。</p>
</section>
</div>
<span class="qa-anchor" id="q-173-a-17"></span><span class="qa-anchor" id="q-173-a-08"></span><span class="qa-anchor" id="q-173-a-09"></span><span class="qa-anchor" id="q-173-a-10"></span><span class="qa-anchor" id="q-173-a-11"></span><span class="qa-anchor" id="q-173-a-12"></span><span class="qa-anchor" id="q-173-a-13"></span><span class="qa-anchor" id="q-173-a-14"></span><span class="qa-anchor" id="q-173-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-namespace_op-9"><h3>本主題的共用條件 · 是否產生 Asynchronous Event？</h3><p>Create／Delete 影響 Allocated List，Attach／Detach 影響指定 controller 的 Active List。依各 controller 的事件支援與 AEC 回報變更；Admin SQ 收到 Delete 的 controller 不回報該次刪除通知，其他受影響且啟用通知的 controller 仍須依規則回報。</p></article>
<article id="common-namespace_op-10"><h3>本主題的共用條件 · 是否更新 Error Information Log 或其他 Log？</h3><p>使用 Identify 的 Allocated、Active 與 Controller List 確認目前配置；Changed Attached Namespace List04h 與 Changed Allocated Namespace List1Ch 指出曾變更的 NSID，不能代替完整現況。失敗則依 More 與 Error Information 補充欄位處理。</p></article>
<article id="common-namespace_op-11"><h3>本主題的共用條件 · 是否記錄於 Persistent Event Log？</h3><p>支援 PEL 時，Namespace Management 對應的 Change Namespace Event06h 記錄建立／刪除等規定事件。Attach／Detach 不應直接當成 Create／Delete；Write Protection 則依該 Feature 是否支援 Set Feature Event 記錄。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-nsid"><strong>Base 2.4 · §3.2.1</strong><br>文件頁 78–81 · PDF 104–107</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-sqe"><strong>Base 2.4 · §4.1.1</strong><br>文件頁 139–142 · PDF 165–168 · Figure 92–93</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>文件頁 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-format"><strong>Base 2.4 · §5.1.1, 5.2.11</strong><br>文件頁 178–179, 206–209 · PDF 204–205, 232–235 · Figure 144, 194–196</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>文件頁 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-getlog"><strong>Base 2.4 · §5.2.13–5.2.13.1.1</strong><br>文件頁 212–218 · PDF 238–244 · Figure 203–211</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-changedlog"><strong>Base 2.4 · §5.2.13.1.5</strong><br>文件頁 226 · PDF 252</li>
<li id="ref-commandseffects"><strong>Base 2.4 · §5.2.13.1.6</strong><br>文件頁 226–229 · PDF 252–255 · Figure 216–217</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-nspelevent"><strong>Base 2.4 · §5.2.13.1.14.2.6</strong><br>文件頁 258–259 · PDF 284–285 · Figure 247</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>文件頁 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-idlist"><strong>Base 2.4 · §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</strong><br>文件頁 387–399, 402–404 · PDF 413–425, 428–430 · Figure 342–355, 360–362</li>
<li id="ref-nsattach"><strong>Base 2.4 · §5.2.24–5.2.25, 8.1.17–8.1.17.2</strong><br>文件頁 444–448, 660–663 · PDF 470–474, 686–689 · Figure 442–450</li>
<li id="ref-sanitizecmd"><strong>Base 2.4 · §5.2.26–5.2.27</strong><br>文件頁 448–454 · PDF 474–480 · Figure 451–455</li>
<li id="ref-aec"><strong>Base 2.4 · §5.2.30.1.6</strong><br>文件頁 466–468 · PDF 492–494 · Figure 474</li>
<li id="ref-nwp"><strong>Base 2.4 · §5.2.30.1.38, 8.1.18</strong><br>文件頁 512, 664–666 · PDF 538, 690–692 · Figure 541, 735–737</li>
<li id="ref-idns"><strong>NVM Command Set 1.3 · §4.1.5.1–4.1.5.4</strong><br>文件頁 84–107 · PDF 84–107 · Figure 123–130</li>
<li id="ref-nvmcreate"><strong>NVM Command Set 1.3 · §4.1.5.8, 4.1.6, 5.8</strong><br>文件頁 108, 110–113, 162–163 · PDF 108, 110–113, 162–163 · Figure 132–134</li>
</ul><h3>需要看欄位圖時</h3><p>以下連結可開啟對應的圖表教學，查閱欄位及判讀方式。每張圖保留固定的教學位置，方便之後反覆查詢。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/namespace-management/en/">English</a><a href="/DOCS/nvme-question-bank/namespace-management.html">繁中教學 HTML</a></nav>
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
