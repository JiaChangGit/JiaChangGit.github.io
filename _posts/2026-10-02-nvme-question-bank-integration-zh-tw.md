---
layout: post
title: "NVMe 自問自答題庫：整合驗證與證據交叉比對"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/integration/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/integration/en/">English</a><a href="/DOCS/nvme-question-bank/integration.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q297–Q320</p><h1>整合驗證與證據交叉比對</h1><p class="qr-intro">本冊把前面機制放進具體矛盾情境：先確認比較的是同一對象與同一時點，再判斷證據是否足夠。相關機制使用固定連結，不重複整段教學。</p><p>先練習，再展開解答。各題依需要使用文字、欄位判讀、比較或流程說明，不要求相同的回答項目。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>一條可重走的驗證路徑</h2><p class="qa-takeaway">先寫出要驗證的規範要求，再選資料；資料多不等於證據完整。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">階段</th><th scope="col">保存什麼</th><th scope="col">避免什麼誤判</th></tr></thead><tbody><tr><td>前提</td><td>能力、scope、設定、狀態</td><td>把支援當成所有參數皆合法</td></tr><tr><td>操作</td><td>原命令、selector、時間</td><td>用事後重建內容代替原件</td></tr><tr><td>結果</td><td>CQE、狀態 Log、事件</td><td>把接受當成背景操作結束</td></tr><tr><td>持續性</td><td>reset 來源及前後狀態</td><td>把全部 reset 當成同一件事</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>「Sanitize CQE 成功、Log 仍進行中」可正常；「同一操作確定已結束、相同 scope 的 Log 仍永久進行中」才需要進一步找新操作、快取或狀態更新問題。</p>
<p class="qa-citations">來源：<a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-297">Q297 · 宣告支援的 Command 卻失敗，第一步怎麼查？</a></li>
<li><a href="#q-298">Q298 · 未宣告支援的 Command 卻成功，是否一定合規？</a></li>
<li><a href="#q-299">Q299 · Set 成功但 Get 或行為不同，如何縮小問題？</a></li>
<li><a href="#q-300">Q300 · AER 已完成，但對應 Log 看不到資訊，怎麼查？</a></li>
<li><a href="#q-301">Q301 · 失敗 CQE 沒新增 Error Entry，一定違規嗎？</a></li>
<li><a href="#q-302">Q302 · CQE、Error Information 與 PEL 不同，何時才是矛盾？</a></li>
<li><a href="#q-303">Q303 · Reset 後 Feature 保留或 Saved 遺失，如何判斷？</a></li>
<li><a href="#q-304">Q304 · Namespace 變更後，Identify、Changed List 與 AER 如何對照？</a></li>
<li><a href="#q-305">Q305 · Firmware Activation 後 FR 或 Slot 沒改，如何判斷？</a></li>
<li><a href="#q-306">Q306 · Sanitize 命令成功後 Log 還在進行中，是錯誤嗎？</a></li>
<li><a href="#q-307">Q307 · Self-test 已結束但沒有結果，如何驗證？</a></li>
<li><a href="#q-308">Q308 · Shutdown 與 Unsafe Shutdowns 計數不符直覺，如何判斷？</a></li>
<li><a href="#q-309">Q309 · Critical Warning 改變卻沒有 AER，先看哪些設定？</a></li>
<li><a href="#q-310">Q310 · PEL 事件排列與實際時間不同，如何驗證？</a></li>
<li><a href="#q-311">Q311 · CFS=1 卻缺少錯誤資訊，還能查什麼？</a></li>
<li><a href="#q-312">Q312 · Abort 後看見兩次 Completion，如何判斷是否重複？</a></li>
<li><a href="#q-313">Q313 · Delete 完成後仍存取 Queue Memory，有何問題？</a></li>
<li><a href="#q-314">Q314 · Reset 後讀到舊 CQE，如何處理？</a></li>
<li><a href="#q-315">Q315 · Detach 後 Namespace Command 仍成功，何時合理？</a></li>
<li><a href="#q-316">Q316 · Lockdown 後仍可操作，如何確認是否漏鎖？</a></li>
<li><a href="#q-317">Q317 · Power State 恢復太慢，如何量測才公平？</a></li>
<li><a href="#q-318">Q318 · 如何比較三種 Reset 對同一功能的影響？</a></li>
<li><a href="#q-319">Q319 · 如何判斷操作真正影響誰？</a></li>
<li><a href="#q-320">Q320 · 如何把所有介面串成一次完整的符合性驗證？</a></li>
</ol></section>
<article class="qa-question" id="q-297" data-question="297" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-297">Q297</a> 宣告支援的 Command 卻失敗，第一步怎麼查？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-297-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-297-a-01">本題練習區分「支援命令」與「這次要求合法且可執行」。支援並不保證所有參數及狀態都成功。</p><div class="qa-sections">
<section class="qa-section" id="q-297-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-297-a-02"></span><p>先固定同一 controller、命令集、namespace 與測試時點，避免拿另一條路徑的能力來比。</p>
<span class="qa-anchor" id="q-297-a-03"></span><p>保存 Identify 的支援位元與 Effects.CSUPP，並記錄 CSI／UUID 選擇。</p>
<span class="qa-anchor" id="q-297-a-04"></span><p>假設支援 Format，卻回 Invalid Format；先讀原命令的 LBAF 與 namespace 可用格式。</p>
</section>
<section class="qa-section" id="q-297-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-297-a-17"></span><p>先檢查實際 SCT／SC，而不是只看應用程式顯示的「失敗」。</p>
<span class="qa-anchor" id="q-297-a-05"></span><p>先解 CQE，再逐項核對參數、namespace 狀態、Write Protection 與當時的管理操作限制。</p>
</section>
<section class="qa-section" id="q-297-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-297-a-06"></span><p>若只因選到不支援的 LBA Format 而失敗，這可與「支援 Format」完全一致。</p>
<span class="qa-anchor" id="q-297-a-07"></span><p>若所有前提成立卻回 Invalid Opcode，才進一步核對命令集及支援宣告是否矛盾；單次失敗不能直接定案。</p>
<span class="qa-anchor" id="q-297-a-16"></span><p>以同時點、單一變因的合法對照命令驗證，避免用另一組不同參數的成功取代原問題。</p>
</section>
</div>
<span class="qa-anchor" id="q-297-a-08"></span><span class="qa-anchor" id="q-297-a-09"></span><span class="qa-anchor" id="q-297-a-10"></span><span class="qa-anchor" id="q-297-a-11"></span><span class="qa-anchor" id="q-297-a-12"></span><span class="qa-anchor" id="q-297-a-13"></span><span class="qa-anchor" id="q-297-a-14"></span><span class="qa-anchor" id="q-297-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/identify/zh-tw/#q-050">Q50</a> · <a href="/nvme/question-bank/logs/zh-tw/#q-081">Q81</a> · <a href="/nvme/question-bank/errors/zh-tw/#q-093">Q93</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-298" data-question="298" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-298">Q298</a> 未宣告支援的 Command 卻成功，是否一定合規？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-298-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-298-a-01">Success 只能說明這次命令的回覆，不能補正本來應準確回報的支援資訊。</p><div class="qa-sections">
<section class="qa-section" id="q-298-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-298-a-02"></span><p>先確認欄位確實適用於這個 controller 類型、命令集與查詢版本。</p>
<span class="qa-anchor" id="q-298-a-03"></span><p>對照 Identify、Supported Log Pages 或 Commands Supported and Effects 的對應宣告，不混用不同能力欄。</p>
<span class="qa-anchor" id="q-298-a-04"></span><p>例如 Effects 中某 opcode 的 CSUPP=0，但相同 CSI 下合法命令完成且有實際效果，兩項證據需要調查。</p>
</section>
<section class="qa-section" id="q-298-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-298-a-17"></span><p>先檢查查詢 selector 與命令 selector 是否一致。</p>
<span class="qa-anchor" id="q-298-a-05"></span><p>先排除舊快照、Firmware Activation、錯誤 opcode 分類與誤解保留欄位，再重做同時點查詢。</p>
</section>
<section class="qa-section" id="q-298-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-298-a-06"></span><p>宣告應與當前支援一致；驗證要同時看回覆與可觀察結果，避免假的 Success 沒做事。</p>
<span class="qa-anchor" id="q-298-a-07"></span><p>只有規範要求不支援時拒絕，才能指定對應錯誤；不能把未知／不適用欄位清零一概當成禁止命令。</p>
<span class="qa-anchor" id="q-298-a-16"></span><p>若確認同一合法條件下宣告與執行矛盾，保留兩份原始回覆，指出違反的具體欄位規則。</p>
</section>
</div>
<span class="qa-anchor" id="q-298-a-08"></span><span class="qa-anchor" id="q-298-a-09"></span><span class="qa-anchor" id="q-298-a-10"></span><span class="qa-anchor" id="q-298-a-11"></span><span class="qa-anchor" id="q-298-a-12"></span><span class="qa-anchor" id="q-298-a-13"></span><span class="qa-anchor" id="q-298-a-14"></span><span class="qa-anchor" id="q-298-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/identify/zh-tw/#q-048">Q48</a> · <a href="/nvme/question-bank/identify/zh-tw/#q-050">Q50</a> · <a href="/nvme/question-bank/logs/zh-tw/#q-080">Q80</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-299" data-question="299" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-299">Q299</a> Set 成功但 Get 或行為不同，如何縮小問題？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-299-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-299-a-01">將接受設定、目前值、保存值與實際效果拆開，才知道差異發生在哪一層。</p><div class="qa-sections">
<section class="qa-section" id="q-299-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-299-a-02"></span><p>Feature 可能屬於 controller、namespace 或其他實體，Get 必須指定相同目標。</p>
<span class="qa-anchor" id="q-299-a-03"></span><p>查 SEL=3 的能力與該 FID 的欄位定義，確認是否允許 controller 調整要求值。</p>
<span class="qa-anchor" id="q-299-a-04"></span><p>例如 KATO 可依 KAS 向上調整，讀回值大於要求不必然是錯誤；不能只做逐 bit 相等比較。</p>
</section>
<section class="qa-section" id="q-299-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-299-a-05"></span>
<span class="qa-anchor" id="q-299-a-06"></span>
<span class="qa-anchor" id="q-299-a-17"></span>
<figure class="qa-flow" id="q-299-flow"><figcaption>Set 與 Get 不同時，先對齊查詢條件</figcaption>
<p>先排除讀到不同種類設定值的情況，再判斷 controller 是否沒有套用設定。</p><ol class="qa-flow-steps">
<li class="qa-flow-step"><strong>保存 Set 要求與成功結果</strong><p>記錄 FID、SV、NSID、其他選擇欄位及資料內容。</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>同一目標，以 SEL=0 讀 Current</strong><p>讀 Default、Saved 或另一個 namespace，都不能直接驗證這次目前設定。</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>檢查是否允許調整，再觀察實際效果</strong><p>讀回合法調整後的值，且行為符合該值，仍可構成成功驗證。</p></li>
<li class="qa-flow-branch"><strong>若要驗證保存，另查 Saved 與指定 Reset</strong><p>保存是另一個測試目標，不要把 Current 的驗證與重設恢復混成一次數字比較。</p></li>
</ol><p class="qa-flow-conclusion">若選擇條件相同，也沒有合法調整、其他 Set 或中途 Reset，才進一步追查實作不一致。</p></figure>
</section>
<section class="qa-section" id="q-299-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-299-a-07"></span><p>若讀的是 Default 或另一 NSID，先修正查詢；若 selector 都相同且沒有允許調整或並行修改，才定位 controller 不一致。</p>
<span class="qa-anchor" id="q-299-a-16"></span><p>保存中途的其他 Set、reset、模式切換；它們都可能使測試後的 Current 不同。</p>
</section>
</div>
<span class="qa-anchor" id="q-299-a-08"></span><span class="qa-anchor" id="q-299-a-09"></span><span class="qa-anchor" id="q-299-a-10"></span><span class="qa-anchor" id="q-299-a-11"></span><span class="qa-anchor" id="q-299-a-12"></span><span class="qa-anchor" id="q-299-a-13"></span><span class="qa-anchor" id="q-299-a-14"></span><span class="qa-anchor" id="q-299-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/features/zh-tw/#q-054">Q54</a> · <a href="/nvme/question-bank/features/zh-tw/#q-055">Q55</a> · <a href="/nvme/question-bank/features/zh-tw/#q-066">Q66</a> · <a href="/nvme/question-bank/features/zh-tw/#q-068">Q68</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-300" data-question="300" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-300">Q300</a> AER 已完成，但對應 Log 看不到資訊，怎麼查？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-300-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-300-a-01">通知指出曾發生符合條件的事件；後續 Log 可能是目前狀態，不一定保存事件發生時的完整快照。</p><div class="qa-sections">
<section class="qa-section" id="q-300-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-300-a-02"></span><p>讀取範圍與事件的 controller、namespace 或 Group 必須相符。</p>
<span class="qa-anchor" id="q-300-a-03"></span><p>保存 AER.CQE.DW0 的事件分類、資訊與 LID，並核對所需額外 selector。</p>
<span class="qa-anchor" id="q-300-a-04"></span><p>例如溫度越過門檻後又恢復，SMART Current Warning 可能已清除；這不否定稍早通知。</p>
</section>
<section class="qa-section" id="q-300-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-300-a-17"></span><p>先檢查 LID、scope 與事件至讀取之間的時間差。</p>
<span class="qa-anchor" id="q-300-a-05"></span><p>先讀正確 Log，再查其他 Host 或程式是否已用 RAE=0 確認，及 Log 是否在兩次讀取間變動。</p>
</section>
<section class="qa-section" id="q-300-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-300-a-06"></span><p>事件資訊、讀取時間與目前狀態能形成合理時間線，即使目前警告已消失也可能正常。</p>
<span class="qa-anchor" id="q-300-a-07"></span><p>Immediate、One-Shot 與一般事件清除方式不同；不能要求每種事件都必須留在 Log 等 Host 讀。</p>
<span class="qa-anchor" id="q-300-a-16"></span><p>若事件與 Log 持續矛盾，保存首次讀取原件與所有 RAE 操作，避免重讀把證據改掉。</p>
</section>
</div>
<span class="qa-anchor" id="q-300-a-08"></span><span class="qa-anchor" id="q-300-a-09"></span><span class="qa-anchor" id="q-300-a-10"></span><span class="qa-anchor" id="q-300-a-11"></span><span class="qa-anchor" id="q-300-a-12"></span><span class="qa-anchor" id="q-300-a-13"></span><span class="qa-anchor" id="q-300-a-14"></span><span class="qa-anchor" id="q-300-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/asynchronous-events/zh-tw/#q-083">Q83</a> · <a href="/nvme/question-bank/asynchronous-events/zh-tw/#q-084">Q84</a> · <a href="/nvme/question-bank/asynchronous-events/zh-tw/#q-090">Q90</a> · <a href="/nvme/question-bank/asynchronous-events/zh-tw/#q-092">Q92</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-301" data-question="301" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-301">Q301</a> 失敗 CQE 沒新增 Error Entry，一定違規嗎？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-301-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-301-a-01">Error Information 不是所有失敗 CQE 的逐筆必備副本；必須找出此錯誤是否有明確記錄要求。</p><div class="qa-sections">
<section class="qa-section" id="q-301-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-301-a-02"></span><p>以同一 controller 的命令與 Error Count 比較；短時間多個錯誤可能覆蓋舊 entry。</p>
<span class="qa-anchor" id="q-301-a-03"></span><p>查 CQE.More、錯誤類別與該命令專屬的補充記錄要求。</p>
<span class="qa-anchor" id="q-301-a-04"></span><p>More=1 指出有額外狀態資訊；More=0 不能反推絕不記錄。</p>
</section>
<section class="qa-section" id="q-301-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-301-a-17"></span><p>先找出這一個錯誤的 shall／should／may 記錄要求。</p>
<span class="qa-anchor" id="q-301-a-05"></span><p>保存失敗前後的 Error Count 與所有有效 entries，再依 SQID／CID／Status 關聯。</p>
</section>
<section class="qa-section" id="q-301-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-301-a-06"></span><p>若該類錯誤不強制新增且沒有其他違反條件，沒有新 entry 可以合規。</p>
<span class="qa-anchor" id="q-301-a-07"></span><p>若命令明定必須寫 Error Information 補充資訊，例如特定容量不足條件，缺少記錄就不能用一般可選規則帶過。</p>
<span class="qa-anchor" id="q-301-a-16"></span><p>排除 ring 覆蓋、重設清除與錯誤讀取長度後，才判斷記錄是否真的缺失。</p>
</section>
<section class="qa-section" id="q-301-s-04" data-answer-section="4"><h3><span>4.</span> 用 Log 補充哪些證據</h3>
<span class="qa-anchor" id="q-301-a-10"></span><p>成功 CQE 不會單憑成功這件事，就要求新增 Error Information entry。 <a class="qa-rule-link" href="#common-command-10">完整條件見本冊說明</a></p>
</section>
</div>
<span class="qa-anchor" id="q-301-a-08"></span><span class="qa-anchor" id="q-301-a-09"></span><span class="qa-anchor" id="q-301-a-11"></span><span class="qa-anchor" id="q-301-a-12"></span><span class="qa-anchor" id="q-301-a-13"></span><span class="qa-anchor" id="q-301-a-14"></span><span class="qa-anchor" id="q-301-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/errors/zh-tw/#q-099">Q99</a> · <a href="/nvme/question-bank/errors/zh-tw/#q-103">Q103</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-302" data-question="302" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-302">Q302</a> CQE、Error Information 與 PEL 不同，何時才是矛盾？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-302-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-302-a-01">三者記錄目的與時間不同，不能要求整筆資料逐 byte 一致。</p><div class="qa-sections">
<section class="qa-section" id="q-302-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-302-a-02"></span><p>CQE 屬於一筆命令，Error entry 補充錯誤，PEL 描述持續事件及其影響範圍。</p>
<span class="qa-anchor" id="q-302-a-03"></span><p>查事件支援、More 與原始命令身分，確認比較的是同一件事。</p>
<span class="qa-anchor" id="q-302-a-04"></span><p>Error Status 的 15:1 應與相符 CQE Status 相同；Phase 可有其規範允許處理，不應當作錯誤碼的一部分。</p>
</section>
<section class="qa-section" id="q-302-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-302-a-17"></span><p>先確認三份紀錄各自能證明什麼，而不是先找相同文字。</p>
<span class="qa-anchor" id="q-302-a-05"></span><p>先關聯 controller、SQID、CID 與時間，再解析 PEL 的事件專屬欄位，例如 Format 的 INFO／FNVMS。</p>
</section>
<section class="qa-section" id="q-302-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-302-a-06"></span><p>Sanitize 命令成功接受，但稍後操作失敗時，早先 Success CQE 與失敗完成事件可以同時正確。</p>
<span class="qa-anchor" id="q-302-a-07"></span><p>若把不同時間的同 CID 或 PEL 請求值當成完成值，會形成假矛盾；真正違規需指明同一欄位關係的要求。</p>
<span class="qa-anchor" id="q-302-a-16"></span><p>建立含「接受、開始、操作完成、查詢」的時間線，再逐欄比對。</p>
</section>
</div>
<span class="qa-anchor" id="q-302-a-08"></span><span class="qa-anchor" id="q-302-a-09"></span><span class="qa-anchor" id="q-302-a-10"></span><span class="qa-anchor" id="q-302-a-11"></span><span class="qa-anchor" id="q-302-a-12"></span><span class="qa-anchor" id="q-302-a-13"></span><span class="qa-anchor" id="q-302-a-14"></span><span class="qa-anchor" id="q-302-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/errors/zh-tw/#q-100">Q100</a> · <a href="/nvme/question-bank/errors/zh-tw/#q-101">Q101</a> · <a href="/nvme/question-bank/errors/zh-tw/#q-106">Q106</a> · <a href="/nvme/question-bank/persistent-events/zh-tw/#q-213">Q213</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-303" data-question="303" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-303">Q303</a> Reset 後 Feature 保留或 Saved 遺失，如何判斷？</h2>
<p class="qa-prompt">先指明重設或中斷的方式，再分別判斷設定、進行中的操作與資料。</p>
<details class="qa-answer" id="q-303-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-303-a-01">不可保存不等於不持續；可保存也不代表最近一次未設定 SV 的 Current 值必須跨斷電保留。</p><div class="qa-sections">
<section class="qa-section" id="q-303-s-01" data-answer-section="1"><h3><span>1.</span> 先界定觸發方式與影響對象</h3>
<span class="qa-anchor" id="q-303-a-02"></span><p>先判斷 Feature scope 與 reset 實際涵蓋的物件，部分重設和整體重設可能不同。</p>
<span class="qa-anchor" id="q-303-a-03"></span><p>保存 Supported Capabilities、Current、Saved 與 Default，以及最後一次成功 Set 的 SV。</p>
</section>
<section class="qa-section" id="q-303-s-02" data-answer-section="2"><h3><span>2.</span> 哪些狀態改變，恢復後怎麼處理</h3>
<span class="qa-anchor" id="q-303-a-04"></span><p>例如 Namespace Write Protection 具有專屬持續性，不能只因不可保存就要求 CLR 清除。</p>
<span class="qa-anchor" id="q-303-a-05"></span><p>先用成功 Set 建立已知 Saved，再執行明確 reset 類型，恢復後查同一目標的 Current／Saved。</p>
<span class="qa-anchor" id="q-303-a-06"></span><p>恢復值符合一般 Feature 規則及個別例外才通過，不以「所有值變 0」當成功。</p>
</section>
<section class="qa-section" id="q-303-s-03" data-answer-section="3"><h3><span>3.</span> 如何驗證保留或恢復結果</h3>
<span class="qa-anchor" id="q-303-a-07"></span><p>若 Set.SV 未成功或中途另有合法 Set，就不能把差異直接歸為保存遺失。</p>
<span class="qa-anchor" id="q-303-a-16"></span><p>將每個 FID 的保存與持續性分欄，並記錄 reset 來源和範圍。</p>
<span class="qa-anchor" id="q-303-a-17"></span><p>先檢查成功 Set 的 SV 與該 FID 的例外。</p>
</section>
</div>
<span class="qa-anchor" id="q-303-a-08"></span><span class="qa-anchor" id="q-303-a-09"></span><span class="qa-anchor" id="q-303-a-10"></span><span class="qa-anchor" id="q-303-a-11"></span><span class="qa-anchor" id="q-303-a-12"></span><span class="qa-anchor" id="q-303-a-13"></span><span class="qa-anchor" id="q-303-a-14"></span><span class="qa-anchor" id="q-303-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/features/zh-tw/#q-055">Q55</a> · <a href="/nvme/question-bank/features/zh-tw/#q-067">Q67</a> · <a href="/nvme/question-bank/integration/zh-tw/#q-318">Q318</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-304" data-question="304" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-304">Q304</a> Namespace 變更後，Identify、Changed List 與 AER 如何對照？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-304-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-304-a-01">Identify 描述目前配置，Changed List 列出曾變更的 NSID，AER 則提醒 Host 需要重新查詢。</p><div class="qa-sections">
<section class="qa-section" id="q-304-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-304-a-02"></span><p>同一 namespace 的變更不一定讓每台 controller 看到相同清單；需看各台 attachment 與通知規則。</p>
<span class="qa-anchor" id="q-304-a-03"></span><p>查支援、AEC 與等待中的 AER，再保存管理命令前後的清單。</p>
<span class="qa-anchor" id="q-304-a-04"></span><p>Attach 後看 Active List，Create 後看 Allocated List；兩者不能互相代替。</p>
</section>
<section class="qa-section" id="q-304-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-304-a-17"></span><p>先確認此次變更是 Create／Delete 還是 Attach／Detach。</p>
<span class="qa-anchor" id="q-304-a-05"></span><p>以單一操作建立時間線，等命令完成，再讀事件與清單，最後重讀 Identify 確认目前結果。</p>
</section>
<section class="qa-section" id="q-304-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-304-a-06"></span><p>Changed List 有 NSID 並不表示該 namespace 目前仍存在；Delete 也能讓 Host 需要更新舊資訊。</p>
<span class="qa-anchor" id="q-304-a-07"></span><p>清單超量可用 FFFFFFFFh 表示無法逐一列出，此時應重新探索全部，不把它當成真實 NSID。</p>
<span class="qa-anchor" id="q-304-a-16"></span><p>先保存首次清單讀取，並區分管理命令所在 controller 與其他被通知 controller。</p>
</section>
</div>
<span class="qa-anchor" id="q-304-a-08"></span><span class="qa-anchor" id="q-304-a-09"></span><span class="qa-anchor" id="q-304-a-10"></span><span class="qa-anchor" id="q-304-a-11"></span><span class="qa-anchor" id="q-304-a-12"></span><span class="qa-anchor" id="q-304-a-13"></span><span class="qa-anchor" id="q-304-a-14"></span><span class="qa-anchor" id="q-304-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/namespace-management/zh-tw/#q-160">Q160</a> · <a href="/nvme/question-bank/namespace-management/zh-tw/#q-162">Q162</a> · <a href="/nvme/question-bank/namespace-management/zh-tw/#q-167">Q167</a> · <a href="/nvme/question-bank/namespace-management/zh-tw/#q-168">Q168</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-changedlog">Base 2.4 §5.2.13.1.5</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-305" data-question="305" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-305">Q305</a> Firmware Activation 後 FR 或 Slot 沒改，如何判斷？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-305-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-305-a-01">下載、存入 slot、排程啟用與真正啟用是不同階段，不能把 Download Success 當成已換韌體。</p><div class="qa-sections">
<section class="qa-section" id="q-305-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-305-a-02"></span><p>Firmware 的 slot 與啟用可由同 Domain 的 controllers 共用，查詢必須在相關範圍內。</p>
<span class="qa-anchor" id="q-305-a-03"></span><p>查 FRMW、LID03h 的 CAFS／NAFS／FRS，以及 Identify.FR。</p>
<span class="qa-anchor" id="q-305-a-04"></span><p>保存 Commit Action、Slot 與 CQE；某些結果要求 CLR、Subsystem 或 Conventional Reset，不是任意 reset 都能替代。</p>
</section>
<section class="qa-section" id="q-305-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-305-a-17"></span><p>先檢查 Commit Action 與是否做了正確類型的啟用。</p>
<span class="qa-anchor" id="q-305-a-05"></span><p>先確認 Commit 有效，再執行指定啟用步驟，恢復後讀 FR 與目前 slot。</p>
</section>
<section class="qa-section" id="q-305-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-305-a-06"></span><p>若新映像版本字串與舊版相同，FR 沒變不證明沒啟用；還需 slot 與其他可靠版本證據。</p>
<span class="qa-anchor" id="q-305-a-07"></span><p>啟用失敗可回復可用映像；PEL 的 New Firmware Revision 是要求的新版本，不自動證明已成為目前版本。</p>
<span class="qa-anchor" id="q-305-a-16"></span><p>把 pending slot、active slot、實際 FR 與 Firmware Commit／Reset 事件分開核對。</p>
</section>
</div>
<span class="qa-anchor" id="q-305-a-08"></span><span class="qa-anchor" id="q-305-a-09"></span><span class="qa-anchor" id="q-305-a-10"></span><span class="qa-anchor" id="q-305-a-11"></span><span class="qa-anchor" id="q-305-a-12"></span><span class="qa-anchor" id="q-305-a-13"></span><span class="qa-anchor" id="q-305-a-14"></span><span class="qa-anchor" id="q-305-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/firmware-boot/zh-tw/#q-139">Q139</a> · <a href="/nvme/question-bank/firmware-boot/zh-tw/#q-140">Q140</a> · <a href="/nvme/question-bank/firmware-boot/zh-tw/#q-144">Q144</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-306" data-question="306" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-306">Q306</a> Sanitize 命令成功後 Log 還在進行中，是錯誤嗎？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-306-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-306-a-01">Sanitize 的命令完成只表示操作已被接受並啟動；清除媒體可在背景繼續。</p><div class="qa-sections">
<section class="qa-section" id="q-306-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-306-a-02"></span><p>先分 Subsystem 與 Namespace Sanitize，並查正確 NSID 的結果。</p>
<span class="qa-anchor" id="q-306-a-03"></span><p>查 SANICAP、命令類型、Sanitize Status 及支援的完成事件。</p>
<span class="qa-anchor" id="q-306-a-04"></span><p>SPROG 是進度，SOS 是操作狀態；不能只看到 SPROG=FFFFh 就忽略 SOS 與 verification state。</p>
</section>
<section class="qa-section" id="q-306-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-306-a-17"></span><p>先檢查你稱為「完成」的證據到底是哪一種。</p>
<span class="qa-anchor" id="q-306-a-05"></span><p>保存啟動 CQE，持續查狀態；有完成 AER 時再查相同操作的最終結果。</p>
</section>
<section class="qa-section" id="q-306-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-306-a-06"></span><p>啟動成功後 SOS=進行中可以正常；真正完成時才應切換相應完成狀態並符合事件／Log 順序。</p>
<span class="qa-anchor" id="q-306-a-07"></span><p>若已確認同一操作完成，Log 卻持續顯示進行中，先排除新的 Sanitize、錯誤 scope 或舊快取回覆。</p>
<span class="qa-anchor" id="q-306-a-16"></span><p>比對命令、Log、AER 及 PEL 的同一次操作，分清「命令完成」與「清除完成」。</p>
</section>
</div>
<span class="qa-anchor" id="q-306-a-08"></span><span class="qa-anchor" id="q-306-a-09"></span><span class="qa-anchor" id="q-306-a-10"></span><span class="qa-anchor" id="q-306-a-11"></span><span class="qa-anchor" id="q-306-a-12"></span><span class="qa-anchor" id="q-306-a-13"></span><span class="qa-anchor" id="q-306-a-14"></span><span class="qa-anchor" id="q-306-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/format-sanitize/zh-tw/#q-128">Q128</a> · <a href="/nvme/question-bank/format-sanitize/zh-tw/#q-130">Q130</a> · <a href="/nvme/question-bank/format-sanitize/zh-tw/#q-131">Q131</a> · <a href="/nvme/question-bank/format-sanitize/zh-tw/#q-133">Q133</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-307" data-question="307" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-307">Q307</a> Self-test 已結束但沒有結果，如何驗證？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-307-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-307-a-01">啟動命令成功不代表測試成功；測試結束要由 Current Operation 與結果紀錄一起確認。</p><div class="qa-sections">
<section class="qa-section" id="q-307-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-307-a-02"></span><p>確認查同一 controller／共享操作範圍，並使用正確的 Log 版本與完整長度。</p>
<span class="qa-anchor" id="q-307-a-03"></span><p>查 OACS、DSTO、EDSTT 與 LID06h；結果最新在前，有 20 筆結果位置。</p>
<span class="qa-anchor" id="q-307-a-04"></span><p>Current Operation、Completion Percentage、DSTR、DSTC 與 VDINFO 分別描述進行狀態、結果及欄位有效性。</p>
</section>
<section class="qa-section" id="q-307-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-307-a-17"></span><p>先確認真的曾啟動測試，而非只成功送出 idle Abort。</p>
<span class="qa-anchor" id="q-307-a-05"></span><p>保存開始前結果，啟動一次測試，等 Log 顯示結束，再與最新結果比對。</p>
</section>
<section class="qa-section" id="q-307-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-307-a-06"></span><p>規範要求結果更新與 Current Operation 回到 idle 的順序一致；讀到 idle 時應能查到本次應記錄的結果。</p>
<span class="qa-anchor" id="q-307-a-07"></span><p>Idle 時送 Abort 可成功但不新增結果；不能把這種情況誤判為漏記一次測試。</p>
<span class="qa-anchor" id="q-307-a-16"></span><p>Short 遇 CLR 會中止，Extended 具有不同持續性；用測試種類與中斷時間解釋結果代碼。</p>
</section>
</div>
<span class="qa-anchor" id="q-307-a-08"></span><span class="qa-anchor" id="q-307-a-09"></span><span class="qa-anchor" id="q-307-a-10"></span><span class="qa-anchor" id="q-307-a-11"></span><span class="qa-anchor" id="q-307-a-12"></span><span class="qa-anchor" id="q-307-a-13"></span><span class="qa-anchor" id="q-307-a-14"></span><span class="qa-anchor" id="q-307-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/self-test/zh-tw/#q-152">Q152</a> · <a href="/nvme/question-bank/self-test/zh-tw/#q-153">Q153</a> · <a href="/nvme/question-bank/self-test/zh-tw/#q-155">Q155</a> · <a href="/nvme/question-bank/self-test/zh-tw/#q-156">Q156</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-selftest">Base 2.4 §5.2.6, 8.1.8</a> · <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-nvmselftest">NVM Command Set 1.3 §4.1.4.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-308" data-question="308" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-308">Q308</a> Shutdown 與 Unsafe Shutdowns 計數不符直覺，如何判斷？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-308-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-308-a-01">計數不能只按 Host 寫了 Normal 或 Abrupt 分類；需看主電源移除時的實際完成狀態。</p><div class="qa-sections">
<section class="qa-section" id="q-308-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-308-a-02"></span><p>Base2.4 使用 Unexpected Power Loss Count（UPL）；它是裝置記錄的失電事件，不是 Host 呼叫 Shutdown 的次數。</p>
<span class="qa-anchor" id="q-308-a-03"></span><p>保存 SMART 計數、CC.SHN、CSTS.SHST 及實際失電時點。</p>
<span class="qa-anchor" id="q-308-a-04"></span><p>一般條件為主電源移除時 SHST 尚未 10b；適用的帶外 Ignore Shutdown 情況另看媒體是否仍活躍。</p>
</section>
<section class="qa-section" id="q-308-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-308-a-17"></span><p>先確認主電源是否真的移除，以及當時 SHST 是否已 10b。</p>
<span class="qa-anchor" id="q-308-a-05"></span><p>先讀基準計數，發出 shutdown，觀察狀態，再於指定時點斷電，恢復後比較。</p>
</section>
<section class="qa-section" id="q-308-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-308-a-06"></span><p>Abrupt 也可能達到 Shutdown Complete 後才失電，因此不能要求每次 Abrupt 都增加 UPL。</p>
<span class="qa-anchor" id="q-308-a-07"></span><p>Normal 要求若尚未完成就掉電，仍可能計數增加；沒有失電的 controller reset 也不能自動算一次。</p>
<span class="qa-anchor" id="q-308-a-16"></span><p>比對真正失電前最後狀態，避免使用重啟後 SHST 的值倒推。</p>
</section>
</div>
<span class="qa-anchor" id="q-308-a-08"></span><span class="qa-anchor" id="q-308-a-09"></span><span class="qa-anchor" id="q-308-a-10"></span><span class="qa-anchor" id="q-308-a-11"></span><span class="qa-anchor" id="q-308-a-12"></span><span class="qa-anchor" id="q-308-a-13"></span><span class="qa-anchor" id="q-308-a-14"></span><span class="qa-anchor" id="q-308-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/reset-shutdown/zh-tw/#q-183">Q183</a> · <a href="/nvme/question-bank/reset-shutdown/zh-tw/#q-184">Q184</a> · <a href="/nvme/question-bank/reset-shutdown/zh-tw/#q-186">Q186</a> · <a href="/nvme/question-bank/health/zh-tw/#q-199">Q199</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-309" data-question="309" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-309">Q309</a> Critical Warning 改變卻沒有 AER，先看哪些設定？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-309-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-309-a-01">狀態改變與應通知的事件條件不同；警告消失不一定與警告出現有同樣通知要求。</p><div class="qa-sections">
<section class="qa-section" id="q-309-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-309-a-02"></span><p>SMART 整體警告與 Group-specific 警告要用各自 scope 與設定。</p>
<span class="qa-anchor" id="q-309-a-03"></span><p>確認 AEC 對應位元、支援能力、是否有 outstanding AER，以及舊同類事件是否尚未確認。</p>
<span class="qa-anchor" id="q-309-a-04"></span><p>保存變化前後 CW、溫度／spare 等原始值及門檻；不要只保存應用程式的警告文字。</p>
</section>
<section class="qa-section" id="q-309-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-309-a-17"></span><p>先確認事件發生時的 AEC，而不是事後才讀到的設定。</p>
<span class="qa-anchor" id="q-309-a-05"></span><p>先確認達到事件條件，再查 AER 是否被其他事件占用或通知被合併，最後檢查相關 Log 的 RAE 讀取。</p>
</section>
<section class="qa-section" id="q-309-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-309-a-06"></span><p>已啟用且符合條件的事件，應依該類型排隊與回報規則被處理；不一定每次取樣變動都另完成一筆 AER。</p>
<span class="qa-anchor" id="q-309-a-07"></span><p>如果沒有等待中的 AER，不能要求當下就有 CQE；同樣地，不應把未處理 CQE 誤判成 controller 沒通知。</p>
<span class="qa-anchor" id="q-309-a-16"></span><p>將 CW 時間線、AEC、AER 清單及 RAE 操作放在一起，找出真正缺少的一步。</p>
</section>
</div>
<span class="qa-anchor" id="q-309-a-08"></span><span class="qa-anchor" id="q-309-a-09"></span><span class="qa-anchor" id="q-309-a-10"></span><span class="qa-anchor" id="q-309-a-11"></span><span class="qa-anchor" id="q-309-a-12"></span><span class="qa-anchor" id="q-309-a-13"></span><span class="qa-anchor" id="q-309-a-14"></span><span class="qa-anchor" id="q-309-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/features/zh-tw/#q-061">Q61</a> · <a href="/nvme/question-bank/asynchronous-events/zh-tw/#q-088">Q88</a> · <a href="/nvme/question-bank/health/zh-tw/#q-196">Q196</a> · <a href="/nvme/question-bank/health/zh-tw/#q-202">Q202</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-310" data-question="310" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-310">Q310</a> PEL 事件排列與實際時間不同，如何驗證？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-310-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-310-a-01">事件在 Log 的排列、Header timestamp 與操作實際先後是三種不同資訊。</p><div class="qa-sections">
<section class="qa-section" id="q-310-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-310-a-02"></span><p>PEL 為 subsystem 範圍，多個 controller 的事件可能交錯，也可能受供應商允許的排序影響。</p>
<span class="qa-anchor" id="q-310-a-03"></span><p>查目前報告 context、Generation Number 與 Timestamp Origin／SYNC。</p>
<span class="qa-anchor" id="q-310-a-04"></span><p>Timestamp 可因 Host Set、reset 或 saved-value 恢復而跳變；不能把它一律當嚴格遞增序號。</p>
</section>
<section class="qa-section" id="q-310-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-310-a-17"></span><p>先確認是否讀了同一份 context 與正確事件邊界。</p>
<span class="qa-anchor" id="q-310-a-05"></span><p>先在同一 context 讀完整事件，依 EHL／EL 正確走訪，再用 Timestamp Change 與 Reset 事件解釋時間變化。</p>
</section>
<section class="qa-section" id="q-310-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-310-a-06"></span><p>規範建議新到舊排列，但允許供應商定義的事件順序；測試不能把 should 改成絕對排序要求。</p>
<span class="qa-anchor" id="q-310-a-07"></span><p>若分段讀取混用不同 context，或把 EL 不含 vendor bytes 來算，可能產生假的亂序或壞事件。</p>
<span class="qa-anchor" id="q-310-a-16"></span><p>用 Host 單調時間保存提交與完成，作為比對線索，但不要求它與未同步的裝置時計完全相等。</p>
</section>
</div>
<span class="qa-anchor" id="q-310-a-08"></span><span class="qa-anchor" id="q-310-a-09"></span><span class="qa-anchor" id="q-310-a-10"></span><span class="qa-anchor" id="q-310-a-11"></span><span class="qa-anchor" id="q-310-a-12"></span><span class="qa-anchor" id="q-310-a-13"></span><span class="qa-anchor" id="q-310-a-14"></span><span class="qa-anchor" id="q-310-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/persistent-events/zh-tw/#q-213">Q213</a> · <a href="/nvme/question-bank/persistent-events/zh-tw/#q-214">Q214</a> · <a href="/nvme/question-bank/persistent-events/zh-tw/#q-215">Q215</a> · <a href="/nvme/question-bank/persistent-events/zh-tw/#q-216">Q216</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-311" data-question="311" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-311">Q311</a> CFS=1 卻缺少錯誤資訊，還能查什麼？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-311-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-311-a-01">Fatal 狀態可能讓正常查詢也失敗；缺少 Log 不表示 CFS 不合理，也不代表應持續送更多命令。</p><div class="qa-sections">
<section class="qa-section" id="q-311-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-311-a-02"></span><p>先判斷這是一般 controller，還是正處 Offline 的 secondary；後者也會設定 CFS。</p>
<span class="qa-anchor" id="q-311-a-03"></span><p>保存 CC、CSTS、CAP、VS、可存取的設定資訊與近期管理操作。</p>
<span class="qa-anchor" id="q-311-a-04"></span><p>若通道仍允許，讀 Error、SMART、PEL 或先前已存在的 Telemetry；不保證每個 CFS 原因都有專用可讀紀錄。</p>
</section>
<section class="qa-section" id="q-311-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-311-a-17"></span><p>先確認 controller 角色與目前 Register 讀取是否可信。</p>
<span class="qa-anchor" id="q-311-a-05"></span><p>先留存最小原始證據，再依裝置可用狀態做 reset 與恢復，之後補查持續性紀錄。</p>
</section>
<section class="qa-section" id="q-311-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-311-a-06"></span><p>恢復後重新初始化及探索，確認 CFS 不再阻止服務；舊命令結果仍需按中斷的不確定性處理。</p>
<span class="qa-anchor" id="q-311-a-07"></span><p>若 MMIO 無法可靠讀取，就不能把全 1 或預設值直接解析成真實 NVMe 狀態。</p>
<span class="qa-anchor" id="q-311-a-16"></span><p>分開 controller 回報、Host timeout 與通訊失效的證據，避免將其中一項代替全部原因。</p>
</section>
</div>
<span class="qa-anchor" id="q-311-a-08"></span><span class="qa-anchor" id="q-311-a-09"></span><span class="qa-anchor" id="q-311-a-10"></span><span class="qa-anchor" id="q-311-a-11"></span><span class="qa-anchor" id="q-311-a-12"></span><span class="qa-anchor" id="q-311-a-13"></span><span class="qa-anchor" id="q-311-a-14"></span><span class="qa-anchor" id="q-311-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/initialization/zh-tw/#q-006">Q6</a> · <a href="/nvme/question-bank/errors/zh-tw/#q-105">Q105</a> · <a href="/nvme/question-bank/recovery/zh-tw/#q-117">Q117</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-ready">Base 2.4 §3.5.3–3.5.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-312" data-question="312" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-312">Q312</a> Abort 後看見兩次 Completion，如何判斷是否重複？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-312-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-312-a-01">Abort 命令與目標命令各自有完成結果，所以總共兩筆 CQE 可以正常；真正要檢查的是目標命令是否被完成兩次。</p><div class="qa-sections">
<section class="qa-section" id="q-312-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-312-a-02"></span><p>使用 controller、SQID、CID 與 queue 使用期間識別每筆命令。</p>
<span class="qa-anchor" id="q-312-a-03"></span><p>保存 Abort 指定的 SQID／CID、Abort 自己的 CID 及 CQE.DW0.IANP。</p>
<span class="qa-anchor" id="q-312-a-04"></span><p>IANP=0 表示 Abort 已達成規定的立即中止效果，但目標命令仍須依其完成規則結束，不能因此省略目標命令的 CQE。IANP=1 則表示沒有取得這項立即效果，目標命令之後仍可能正常完成。</p>
</section>
<section class="qa-section" id="q-312-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-312-a-17"></span><p>先檢查兩筆 CQE 的 SQID／CID，哪一筆其實屬於 Abort。</p>
<span class="qa-anchor" id="q-312-a-05"></span><p>先分出 Admin Abort CQE 與原 I/O CQE，再檢查 Host 是否因 Phase 或 Head 錯誤讀了同一筆兩次。</p>
</section>
<section class="qa-section" id="q-312-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-312-a-06"></span><p>正常情況可以是一筆 Abort CQE 加上一筆目標命令 CQE，Host 應將兩者分別對回各自的命令。目標命令可能已經修改部分資料，因此看到 Abort 完成後，不能直接假設原命令完全沒執行而原樣重送。</p>
<span class="qa-anchor" id="q-312-a-07"></span><p>若已排除 Host 重複讀取同一 CQE，也確認 CID 沒有重用，controller 卻仍對同一次提交的目標命令產生兩筆有效 CQE，才是同一命令被完成兩次的問題。</p>
<span class="qa-anchor" id="q-312-a-16"></span><p>CID 重用與 CQ 繞回必須排除，不能只憑兩張截圖顯示相同 CID 就判重複。</p>
</section>
</div>
<span class="qa-anchor" id="q-312-a-08"></span><span class="qa-anchor" id="q-312-a-09"></span><span class="qa-anchor" id="q-312-a-10"></span><span class="qa-anchor" id="q-312-a-11"></span><span class="qa-anchor" id="q-312-a-12"></span><span class="qa-anchor" id="q-312-a-13"></span><span class="qa-anchor" id="q-312-a-14"></span><span class="qa-anchor" id="q-312-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/recovery/zh-tw/#q-107">Q107</a> · <a href="/nvme/question-bank/recovery/zh-tw/#q-110">Q110</a> · <a href="/nvme/question-bank/recovery/zh-tw/#q-112">Q112</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-313" data-question="313" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-313">Q313</a> Delete 完成後仍存取 Queue Memory，有何問題？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-313-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-313-a-01">Queue 記憶體回收以完成的生命週期為界；越過界線的存取可能破壞已重新分配給其他用途的資料。</p><div class="qa-sections">
<section class="qa-section" id="q-313-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-313-a-02"></span><p>先限定是被刪除 SQ／CQ 本身，還是其他仍有效命令的 buffer；兩者不能混為一談。</p>
<span class="qa-anchor" id="q-313-a-03"></span><p>保存 Delete 的目標 QID、成功 CQE 與 queue 記憶體位址範圍。</p>
<span class="qa-anchor" id="q-313-a-04"></span><p>刪 SQ 與刪 CQ 的依賴及完成要求不同；提交 Delete 不代表已成功結束使用。</p>
</section>
<section class="qa-section" id="q-313-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-313-a-17"></span><p>先確認成功 Delete CQE 已經完成，而非命令還在 outstanding。</p>
<span class="qa-anchor" id="q-313-a-05"></span><p>先等刪除成功，再判斷觀察到的存取是否確實來自該 queue，排除位址被新 queue 合法重用。</p>
</section>
<section class="qa-section" id="q-313-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-313-a-06"></span><p>成功回收後，controller 不應再把該範圍當成已刪除 queue 使用。</p>
<span class="qa-anchor" id="q-313-a-07"></span><p>若仍有這類存取，可能覆寫 Host 資料、使用錯誤命令或產生無法關聯完成，不能以一般 timeout 掩蓋。</p>
<span class="qa-anchor" id="q-313-a-16"></span><p>保留位址重用時間與新舊 QID 對照；只有位址相同仍不足以證明舊 queue 在存取。</p>
</section>
</div>
<span class="qa-anchor" id="q-313-a-08"></span><span class="qa-anchor" id="q-313-a-09"></span><span class="qa-anchor" id="q-313-a-10"></span><span class="qa-anchor" id="q-313-a-11"></span><span class="qa-anchor" id="q-313-a-12"></span><span class="qa-anchor" id="q-313-a-13"></span><span class="qa-anchor" id="q-313-a-14"></span><span class="qa-anchor" id="q-313-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/queues/zh-tw/#q-019">Q19</a> · <a href="/nvme/question-bank/memory/zh-tw/#q-227">Q227</a> · <a href="/nvme/question-bank/interrupts/zh-tw/#q-295">Q295</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-retirement">PCIe Transport 1.4 §3.4 (Command Related Resource Retirement)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-314" data-question="314" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-314">Q314</a> Reset 後讀到舊 CQE，如何處理？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-314-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-314-a-01">舊記憶體殘留與 reset 完成後新發出的非法舊完成，是兩種不同問題。</p><div class="qa-sections">
<section class="qa-section" id="q-314-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-314-a-02"></span><p>Reset 結束受影響 queue 的舊使用期間，新 queue 即使沿用位址與 QID 也屬於新的期間。</p>
<span class="qa-anchor" id="q-314-a-03"></span><p>查 reset 來源、RDY 變化、CQ 初始化與 Host 期待的 Phase。</p>
<span class="qa-anchor" id="q-314-a-04"></span><p>Host 重建 outstanding map，將舊命令與新命令分開；不能用相同 CID 自動配到新請求。</p>
</section>
<section class="qa-section" id="q-314-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-314-a-17"></span><p>先檢查新 queue 的 Phase 與命令追蹤是否重新初始化。</p>
<span class="qa-anchor" id="q-314-a-05"></span><p>先完成 reset 與記憶體初始化，再啟用新 queue；只處理新使用期間中有效的 CQE。</p>
</section>
<section class="qa-section" id="q-314-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-314-a-06"></span><p>殘留的舊 CQE 不作正常新完成處理；中斷前操作是否已修改媒體，另用操作結果與恢復規則判斷。</p>
<span class="qa-anchor" id="q-314-a-07"></span><p>如果 controller 在重設完成後仍主動寫入舊 queue，需按生命週期違規調查；單純殘留 bytes 不足以證明它做了這件事。</p>
<span class="qa-anchor" id="q-314-a-16"></span><p>用記憶體初始化前後與寫入時點分辨殘留、Host 重複處理及真正晚到的存取。</p>
</section>
</div>
<span class="qa-anchor" id="q-314-a-08"></span><span class="qa-anchor" id="q-314-a-09"></span><span class="qa-anchor" id="q-314-a-10"></span><span class="qa-anchor" id="q-314-a-11"></span><span class="qa-anchor" id="q-314-a-12"></span><span class="qa-anchor" id="q-314-a-13"></span><span class="qa-anchor" id="q-314-a-14"></span><span class="qa-anchor" id="q-314-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/initialization/zh-tw/#q-009">Q9</a> · <a href="/nvme/question-bank/queues/zh-tw/#q-021">Q21</a> · <a href="/nvme/question-bank/recovery/zh-tw/#q-115">Q115</a> · <a href="/nvme/question-bank/reset-shutdown/zh-tw/#q-179">Q179</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-315" data-question="315" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-315">Q315</a> Detach 後 Namespace Command 仍成功，何時合理？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-315-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-315-a-01">「接受進 SQ」不等於成功完成；也不是所有帶 NSID 的命令都要求 namespace 已附加。</p><div class="qa-sections">
<section class="qa-section" id="q-315-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-315-a-02"></span><p>Detach 影響指定 controller 的 attachment，其他仍 attached 的 controller 可以保留存取。</p>
<span class="qa-anchor" id="q-315-a-03"></span><p>讀該 controller 的 Active List 與 namespace 的 Attached Controller List，確認操作真的完成。</p>
<span class="qa-anchor" id="q-315-a-04"></span><p>分清一般 I/O、allocated-namespace Identify 與其他有特殊 NSID 規則的管理命令。</p>
</section>
<section class="qa-section" id="q-315-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-315-a-17"></span><p>先確認命令送到哪台 controller，以及命令種類是否真的需要 active namespace。</p>
<span class="qa-anchor" id="q-315-a-05"></span><p>先等 Detach 成功，再送全新的命令到被移除的路徑；不要拿 Detach 前已完成的 CQE 來比較。</p>
</section>
<section class="qa-section" id="q-315-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-315-a-06"></span><p>另一條仍附加路徑的 I/O 成功可以正常；查 allocated 資料也可能合法。</p>
<span class="qa-anchor" id="q-315-a-07"></span><p>對已 inactive namespace 的一般適用命令，若無例外應回 Invalid Field；invalid NSID 則是不同條件的 Invalid Namespace or Format。</p>
<span class="qa-anchor" id="q-315-a-16"></span><p>Outstanding 命令依 Detach 與各命令規則處理，測試要分開操作前後提交的命令。</p>
</section>
</div>
<span class="qa-anchor" id="q-315-a-08"></span><span class="qa-anchor" id="q-315-a-09"></span><span class="qa-anchor" id="q-315-a-10"></span><span class="qa-anchor" id="q-315-a-11"></span><span class="qa-anchor" id="q-315-a-12"></span><span class="qa-anchor" id="q-315-a-13"></span><span class="qa-anchor" id="q-315-a-14"></span><span class="qa-anchor" id="q-315-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/namespace-management/zh-tw/#q-164">Q164</a> · <a href="/nvme/question-bank/namespace-management/zh-tw/#q-165">Q165</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-316" data-question="316" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-316">Q316</a> Lockdown 後仍可操作，如何確認是否漏鎖？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-316-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-316-a-01">Lockdown 指定介面、controller 範圍及命令或 Feature；只符合其中一項不代表必須被禁止。</p><div class="qa-sections">
<section class="qa-section" id="q-316-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-316-a-02"></span><p>CSEL、CNTLID、IFC 與 SCP 共同決定目標，不能只記 opcode。</p>
<span class="qa-anchor" id="q-316-a-03"></span><p>先讀 Lockdown 支援與適用的目前禁止清單，使用相同 UUID、介面及 controller 選擇。</p>
<span class="qa-anchor" id="q-316-a-04"></span><p>SCP 指 Feature 時限制 Set Features，不自動禁止 Get；增強 FFFFh 彙整的 ACNTL=0 也不代表無人受限制。</p>
</section>
<section class="qa-section" id="q-316-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-316-a-17"></span><p>先檢查 IFC／CSEL／SCP，而不是只看功能名稱。</p>
<span class="qa-anchor" id="q-316-a-05"></span><p>確認 Lockdown 成功後，對完全符合 selector 的目標重試；同時設一個應允許的對照命令。</p>
</section>
<section class="qa-section" id="q-316-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-316-a-06"></span><p>匹配的被禁止 Admin command 應回 Command Prohibited by Command and Feature Lockdown（0/23h）。</p>
<span class="qa-anchor" id="q-316-a-07"></span><p>先排除 Power Cycle 解除、後續允許操作、不同介面或 personality 的明文例外，再判斷執行成功是否矛盾。</p>
<span class="qa-anchor" id="q-316-a-16"></span><p>比對 Lockdown CQE、清單與目標命令行為，三者必須使用同一組選擇條件。</p>
</section>
</div>
<span class="qa-anchor" id="q-316-a-08"></span><span class="qa-anchor" id="q-316-a-09"></span><span class="qa-anchor" id="q-316-a-10"></span><span class="qa-anchor" id="q-316-a-11"></span><span class="qa-anchor" id="q-316-a-12"></span><span class="qa-anchor" id="q-316-a-13"></span><span class="qa-anchor" id="q-316-a-14"></span><span class="qa-anchor" id="q-316-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/security/zh-tw/#q-242">Q242</a> · <a href="/nvme/question-bank/security/zh-tw/#q-243">Q243</a> · <a href="/nvme/question-bank/security/zh-tw/#q-244">Q244</a> · <a href="/nvme/question-bank/security/zh-tw/#q-245">Q245</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-317" data-question="317" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-317">Q317</a> Power State 恢復太慢，如何量測才公平？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-317-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-317-a-01">命令總延遲包含退出狀態、進入目標狀態與實際工作，不能全部算成 EXLAT。</p><div class="qa-sections">
<section class="qa-section" id="q-317-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-317-a-02"></span><p>先確認來源與目標 Power State，以及當時是否受 thermal management 等其他條件影響。</p>
<span class="qa-anchor" id="q-317-a-03"></span><p>查 PSD 的 NOPS、ENLAT、EXLAT，及 Power Management／APST 設定。</p>
<span class="qa-anchor" id="q-317-a-04"></span><p>APST.ITPT 是閒置等待時間，單位 ms；ENLAT／EXLAT 是轉換延遲，單位µs，不能相加前忘記換算。</p>
</section>
<section class="qa-section" id="q-317-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-317-a-17"></span><p>先確認單位及計時起點。</p>
<span class="qa-anchor" id="q-317-a-05"></span><p>記錄最後一次活動、進入省電狀態、觸發退出及恢復處理命令的時間。量測轉換延遲時，應將命令本身的執行時間分開，避免把媒體讀取時間也算成退出省電狀態的時間。</p>
</section>
<section class="qa-section" id="q-317-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-317-a-06"></span><p>例如從非工作狀態回到前一工作狀態，按相關退出與進入延遲判斷，而不是把完整 Read 完成時間等同 EXLAT。</p>
<span class="qa-anchor" id="q-317-a-07"></span><p>若只有 CQE 時間而無法分辨內部狀態切換，證據不足以單獨證明 EXLAT 違規。</p>
<span class="qa-anchor" id="q-317-a-16"></span><p>用同 workload 的工作狀態基準、溫度與設定快照做比較，說明仍無法排除的因素。</p>
</section>
</div>
<span class="qa-anchor" id="q-317-a-08"></span><span class="qa-anchor" id="q-317-a-09"></span><span class="qa-anchor" id="q-317-a-10"></span><span class="qa-anchor" id="q-317-a-11"></span><span class="qa-anchor" id="q-317-a-12"></span><span class="qa-anchor" id="q-317-a-13"></span><span class="qa-anchor" id="q-317-a-14"></span><span class="qa-anchor" id="q-317-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/health/zh-tw/#q-188">Q188</a> · <a href="/nvme/question-bank/health/zh-tw/#q-190">Q190</a> · <a href="/nvme/question-bank/health/zh-tw/#q-192">Q192</a> · <a href="/nvme/question-bank/health/zh-tw/#q-194">Q194</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-318" data-question="318" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-318">Q318</a> 如何比較三種 Reset 對同一功能的影響？</h2>
<p class="qa-prompt">先指明重設或中斷的方式，再分別判斷設定、進行中的操作與資料。</p>
<details class="qa-answer" id="q-318-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-318-a-01">要判斷差異是否由 reset 引起，每次測試都應從相同的初始狀態開始，再分別套用不同 reset。若連測試前的設定都不同，就無法把觀察到的差異歸因於 reset 類型。</p><div class="qa-sections">
<section class="qa-section" id="q-318-s-01" data-answer-section="1"><h3><span>1.</span> 先界定觸發方式與影響對象</h3>
<span class="qa-anchor" id="q-318-a-02"></span><p>Controller Level Reset、Subsystem Reset 與 Power Cycle 的範圍及持續性條件不同。</p>
<span class="qa-anchor" id="q-318-a-03"></span><p>先選一個明確功能，保存其能力、Current／Saved、Log 與涉及的其他 controllers。</p>
</section>
<section class="qa-section" id="q-318-s-02" data-answer-section="2"><h3><span>2.</span> 哪些狀態改變，恢復後怎麼處理</h3>
<span class="qa-anchor" id="q-318-a-04"></span><p>分欄記錄 Register、queue、設定值、操作是否持續及儲存資料；不要把全部寫成單一「保留／不保留」。</p>
<span class="qa-anchor" id="q-318-a-05"></span><p>每次恢復相同初始條件，只改 reset 類型；完成後先恢復查詢通道，再檢查各欄。</p>
<span class="qa-anchor" id="q-318-a-06"></span><p>例如 Extended Self-test 可在 CLR 後持續，但 I/O queues 仍失效；兩個結果可以同時成立。</p>
</section>
<section class="qa-section" id="q-318-s-03" data-answer-section="3"><h3><span>3.</span> 如何驗證保留或恢復結果</h3>
<span class="qa-anchor" id="q-318-a-07"></span><p>CC.EN reset 的 Register 保留例外不能套用到所有 CLR；同樣，Subsystem Reset 不是 Restore Defaults。</p>
<span class="qa-anchor" id="q-318-a-16"></span><p>每個差異都連到明確規則，未定義的行為標示證據界線，不猜一個統一答案。</p>
<span class="qa-anchor" id="q-318-a-17"></span><p>先把 reset 的實際觸發方式寫清楚。</p>
</section>
</div>
<span class="qa-anchor" id="q-318-a-08"></span><span class="qa-anchor" id="q-318-a-09"></span><span class="qa-anchor" id="q-318-a-10"></span><span class="qa-anchor" id="q-318-a-11"></span><span class="qa-anchor" id="q-318-a-12"></span><span class="qa-anchor" id="q-318-a-13"></span><span class="qa-anchor" id="q-318-a-14"></span><span class="qa-anchor" id="q-318-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/reset-shutdown/zh-tw/#q-174">Q174</a> · <a href="/nvme/question-bank/reset-shutdown/zh-tw/#q-178">Q178</a> · <a href="/nvme/question-bank/reset-shutdown/zh-tw/#q-180">Q180</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pciereset">PCIe Transport 1.4 §3.3</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-shutdownfull">Base 2.4 §3.6–3.6.1 (memory-based scope and shutdown)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-319" data-question="319" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-319">Q319</a> 如何判斷操作真正影響誰？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-319-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-319-a-01">命令從某個 Admin Queue 送入，不代表效果只限於該 controller。</p><div class="qa-sections">
<section class="qa-section" id="q-319-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-319-a-02"></span><p>作用範圍可能是 namespace、controller、Group、Domain 或 subsystem，需由命令與欄位共同決定。</p>
<span class="qa-anchor" id="q-319-a-03"></span><p>查命令欄位、Feature scope、Identify 的能力及 Commands Supported and Effects 的相關資訊。</p>
<span class="qa-anchor" id="q-319-a-04"></span><p>NSID=FFFFFFFFh 的意思因命令而異；Effects 未回報某 scope 也不能取代命令的明文定義。</p>
</section>
<section class="qa-section" id="q-319-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-319-a-17"></span><p>先讀該命令對 selector 的定義，特別是 0 與 FFFFFFFFh。</p>
<span class="qa-anchor" id="q-319-a-05"></span><p>列出提交端、目標與共用資源，再選一個範圍內及一個範圍外對照物件觀察。</p>
</section>
<section class="qa-section" id="q-319-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-319-a-06"></span><p>例如 Detach 指定一台 controller，而共享 namespace 資料並未因此複製或刪除。</p>
<span class="qa-anchor" id="q-319-a-07"></span><p>對範圍外物件的變化，先排除共用資源與同時發生的另一操作，再判是否超出規範。</p>
<span class="qa-anchor" id="q-319-a-16"></span><p>比較使用相同物件 ID 與穩定時點；不同 controller 的 Active List 本來就可能不同。</p>
</section>
</div>
<span class="qa-anchor" id="q-319-a-08"></span><span class="qa-anchor" id="q-319-a-09"></span><span class="qa-anchor" id="q-319-a-10"></span><span class="qa-anchor" id="q-319-a-11"></span><span class="qa-anchor" id="q-319-a-12"></span><span class="qa-anchor" id="q-319-a-13"></span><span class="qa-anchor" id="q-319-a-14"></span><span class="qa-anchor" id="q-319-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/initialization/zh-tw/#q-002">Q2</a> · <a href="/nvme/question-bank/identify/zh-tw/#q-047">Q47</a> · <a href="/nvme/question-bank/logs/zh-tw/#q-081">Q81</a> · <a href="/nvme/question-bank/media/zh-tw/#q-275">Q275</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-320" data-question="320" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-320">Q320</a> 如何把所有介面串成一次完整的符合性驗證？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-320-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-320-a-01">完整驗證要形成可追溯的證據鏈：宣告、前提、操作、結果、通知、紀錄及持續性各自有依據。</p><div class="qa-sections">
<section class="qa-section" id="q-320-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-320-a-02"></span><p>先界定功能與受影響物件，避免一次測多個功能而無法分清哪個造成差異。</p>
<span class="qa-anchor" id="q-320-a-03"></span><p>保存 Identify、Supported／Effects Logs 與需要的 Feature 設定作為基準。</p>
<span class="qa-anchor" id="q-320-a-04"></span><p>保存原命令及 selector、CQE、相關 Log、AER 與 PEL；不適用或不支援的介面明確標記理由。</p>
</section>
<section class="qa-section" id="q-320-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-320-a-17"></span><p>先寫出這次要驗證的一條具體規範要求，再決定需要哪些證據。</p>
<span class="qa-anchor" id="q-320-a-05"></span><p>先做合法正常案例，再一次只改一個非法參數或順序；最後從相同基準分別驗證 reset 與 Power Cycle。</p>
</section>
<section class="qa-section" id="q-320-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-320-a-06"></span><p>結論能指出哪個規範要求被哪些觀察支持，以及哪些資料仍不足以判斷。</p>
<span class="qa-anchor" id="q-320-a-07"></span><p>禁止把 may 當 shall、把未定義行為指定為固定 Status，或用「命令成功」省略背景操作最終結果。</p>
<span class="qa-anchor" id="q-320-a-16"></span><p>用一張時間線串起原始資料，保留規格章節、Figure 與 PDF 頁碼，讓另一位讀者能重走推理。</p>
</section>
</div>
<span class="qa-anchor" id="q-320-a-08"></span><span class="qa-anchor" id="q-320-a-09"></span><span class="qa-anchor" id="q-320-a-10"></span><span class="qa-anchor" id="q-320-a-11"></span><span class="qa-anchor" id="q-320-a-12"></span><span class="qa-anchor" id="q-320-a-13"></span><span class="qa-anchor" id="q-320-a-14"></span><span class="qa-anchor" id="q-320-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/integration/zh-tw/#q-297">Q297</a> · <a href="/nvme/question-bank/integration/zh-tw/#q-299">Q299</a> · <a href="/nvme/question-bank/integration/zh-tw/#q-300">Q300</a> · <a href="/nvme/question-bank/integration/zh-tw/#q-301">Q301</a> · <a href="/nvme/question-bank/integration/zh-tw/#q-302">Q302</a> · <a href="/nvme/question-bank/integration/zh-tw/#q-318">Q318</a> · <a href="/nvme/question-bank/integration/zh-tw/#q-319">Q319</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-command-10"><h3>命令完成、事件與紀錄 · 是否更新 Error Information Log 或其他 Log？</h3><p>成功 CQE 不會單憑成功這件事，就要求新增 Error Information entry。若錯誤 CQE 的 More=1，則讀取 LID01h，並以 SQID、CID 及 Error Count 關聯紀錄。其他非成功 CQE 是否需要新增 entry，仍須依記錄規則判斷，不能直接以失敗次數推算。至於操作造成的狀態變化，則用本題列出的查詢介面重新確認。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-cc"><strong>Base 2.4 · §3.1.4 (CC, CSTS, NSSR)</strong><br>文件頁 60–66 · PDF 86–92 · Figure 41–43</li>
<li id="ref-capacitymodel"><strong>Base 2.4 · §3.2.2–3.2.3, 3.8</strong><br>文件頁 80–84, 125–129 · PDF 106–110, 151–155 · Figure 67–69, 86–89</li>
<li id="ref-ready"><strong>Base 2.4 · §3.5.3–3.5.4</strong><br>文件頁 109–113 · PDF 135–139 · Figure 84–85</li>
<li id="ref-shutdownfull"><strong>Base 2.4 · §3.6–3.6.1 (memory-based scope and shutdown)</strong><br>文件頁 113–115 · PDF 139–141 · Figure 85</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-firmware"><strong>Base 2.4 · §3.11–3.11.1, 5.2.9–5.2.10</strong><br>文件頁 135–138, 202–206 · PDF 161–164, 228–232 · Figure 187–193</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>文件頁 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>文件頁 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-abort"><strong>Base 2.4 · §5.2.1</strong><br>文件頁 181–182 · PDF 207–208 · Figure 147–149</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>文件頁 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-selftest"><strong>Base 2.4 · §5.2.6, 8.1.8</strong><br>文件頁 199–201, 614–616 · PDF 225–227, 640–642 · Figure 176–180, 700–701</li>
<li id="ref-getlog"><strong>Base 2.4 · §5.2.13–5.2.13.1.1</strong><br>文件頁 212–218 · PDF 238–244 · Figure 203–211</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-smart"><strong>Base 2.4 · §5.2.13.1.3</strong><br>文件頁 220–225 · PDF 246–251 · Figure 213–214</li>
<li id="ref-fwlog"><strong>Base 2.4 · §5.2.13.1.4</strong><br>文件頁 225–226 · PDF 251–252 · Figure 215</li>
<li id="ref-changedlog"><strong>Base 2.4 · §5.2.13.1.5</strong><br>文件頁 226 · PDF 252</li>
<li id="ref-commandseffects"><strong>Base 2.4 · §5.2.13.1.6</strong><br>文件頁 226–229 · PDF 252–255 · Figure 216–217</li>
<li id="ref-dstlog"><strong>Base 2.4 · §5.2.13.1.7</strong><br>文件頁 229–232 · PDF 255–258 · Figure 218–219</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-pelcontext"><strong>Base 2.4 · §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</strong><br>文件頁 244–256, 258 · PDF 270–282, 284 · Figure 232–244, 246</li>
<li id="ref-fwpel"><strong>Base 2.4 · §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</strong><br>文件頁 252–255 · PDF 278–281 · Figure 238, 240–241</li>
<li id="ref-nspelevent"><strong>Base 2.4 · §5.2.13.1.14.2.6</strong><br>文件頁 258–259 · PDF 284–285 · Figure 247</li>
<li id="ref-sanitizepel"><strong>Base 2.4 · §5.2.13.1.14.2.9–5.2.13.1.14.2.10</strong><br>文件頁 261–262 · PDF 287–288 · Figure 250–251</li>
<li id="ref-featureeffects"><strong>Base 2.4 · §5.2.13.1.18</strong><br>文件頁 276–278 · PDF 302–304 · Figure 270–271</li>
<li id="ref-locklog"><strong>Base 2.4 · §5.2.13.1.20</strong><br>文件頁 279–283 · PDF 305–309 · Figure 274–278</li>
<li id="ref-sanitizelog"><strong>Base 2.4 · §5.2.13.1.38</strong><br>文件頁 313–320 · PDF 339–346 · Figure 312</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>文件頁 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-psd"><strong>Base 2.4 · §5.2.14.2.1 (Power State Descriptor)</strong><br>文件頁 384–387 · PDF 410–413 · Figure 340–341</li>
<li id="ref-idlist"><strong>Base 2.4 · §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</strong><br>文件頁 387–399, 402–404 · PDF 413–425, 428–430 · Figure 342–355, 360–362</li>
<li id="ref-lockdown"><strong>Base 2.4 · §5.2.16, 8.1.5</strong><br>文件頁 405–408, 597–599 · PDF 431–434, 623–625 · Figure 365–367</li>
<li id="ref-nsattach"><strong>Base 2.4 · §5.2.24–5.2.25, 8.1.17–8.1.17.2</strong><br>文件頁 444–448, 660–663 · PDF 470–474, 686–689 · Figure 442–450</li>
<li id="ref-sanitizecmd"><strong>Base 2.4 · §5.2.26–5.2.27</strong><br>文件頁 448–454 · PDF 474–480 · Figure 451–455</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>文件頁 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-power"><strong>Base 2.4 · §5.2.30.1.2, 5.2.30.1.7</strong><br>文件頁 460–462, 468–469 · PDF 486–488, 494–495 · Figure 468–469, 475–478</li>
<li id="ref-timestamp"><strong>Base 2.4 · §5.2.30.1.8</strong><br>文件頁 469–471 · PDF 495–497 · Figure 479–480</li>
<li id="ref-lockpersist"><strong>Base 2.4 · §5.2.30.1.25.4–5.2.30.1.25.4.1</strong><br>文件頁 493–494 · PDF 519–520 · Figure 518–519</li>
<li id="ref-create"><strong>Base 2.4 · §5.3.1–5.3.2</strong><br>文件頁 527–531 · PDF 553–557 · Figure 571–579</li>
<li id="ref-delete"><strong>Base 2.4 · §5.3.3–5.3.4</strong><br>文件頁 531–532 · PDF 557–558 · Figure 580–583</li>
<li id="ref-powerdetail"><strong>Base 2.4 · §8.1.19.1–8.1.19.5</strong><br>文件頁 666–671 · PDF 692–697 · Figure 738–741</li>
<li id="ref-sanitizestate"><strong>Base 2.4 · §8.1.27.1–8.1.27.5</strong><br>文件頁 711–732 · PDF 737–758 · Figure 770–779</li>
<li id="ref-virtual"><strong>Base 2.4 · §8.2.7</strong><br>文件頁 754–758 · PDF 780–784 · Figure 796</li>
<li id="ref-commrecovery"><strong>Base 2.4 · §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</strong><br>文件頁 825–828 · PDF 851–854</li>
<li id="ref-nvmselftest"><strong>NVM Command Set 1.3 · §4.1.4.3</strong><br>文件頁 75–76 · PDF 75–76 · Figure 111</li>
<li id="ref-nvmpel"><strong>NVM Command Set 1.3 · §4.1.4.4</strong><br>文件頁 76–77 · PDF 76–77 · Figure 112</li>
<li id="ref-pciereset"><strong>PCIe Transport 1.4 · §3.3</strong><br>文件頁 11–12 · PDF 11–12</li>
<li id="ref-retirement"><strong>PCIe Transport 1.4 · §3.4 (Command Related Resource Retirement)</strong><br>文件頁 13 · PDF 13</li>
</ul><h3>需要看欄位圖時</h3><p>以下連結可開啟對應的圖表教學，查閱欄位及判讀方式。每張圖保留固定的教學位置，方便之後反覆查詢。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b42">Base 2.4 Figure 42 · Offset 1Ch: CSTS – Controller Status</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/integration/en/">English</a><a href="/DOCS/nvme-question-bank/integration.html">繁中教學 HTML</a></nav>
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
