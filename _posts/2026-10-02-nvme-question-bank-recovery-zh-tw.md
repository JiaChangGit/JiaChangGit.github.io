---
layout: post
title: "NVMe 自問自答題庫：Abort、Timeout 與錯誤恢復"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/recovery/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/recovery/en/">English</a><a href="/DOCS/nvme-question-bank/recovery.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q107–Q117</p><h1>Abort、Timeout 與錯誤恢復</h1><p class="qr-intro">Timeout 是 Host 的觀察，未必能說明命令停在哪裡。本冊沿提交、取得、執行、完成與處理的路徑找證據，再決定 Abort 或較大範圍 reset。</p><p>先練習，再展開解答。各題依需要使用文字、欄位判讀、比較或流程說明，不要求相同的回答項目。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>先確認命令走到哪一步</h2><p class="qa-takeaway">未看到完成，不代表命令沒有執行，也不代表媒體沒有變動。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">可觀察階段</th><th scope="col">主要證據</th><th scope="col">下一個疑點</th></tr></thead><tbody><tr><td>已提交</td><td>SQE、Tail Doorbell</td><td>Controller 是否取得</td></tr><tr><td>已取得</td><td>適用的 SQHD 與追蹤資料</td><td>是否正在長操作</td></tr><tr><td>已完成</td><td>CQE 與 Phase</td><td>Host 是否漏處理</td></tr><tr><td>恢復中</td><td>Abort CQE／reset 狀態</td><td>原操作結果是否仍不確定</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>Abort 指向 SQ5/CID9，Abort 本身是另一筆 Admin command。兩者各回一筆 CQE 可以正常；只有同一目標命令真的完成兩次，才是重複完成問題。</p>
<p class="qa-citations">來源：<a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-107">Q107 · Abort 如何用 SQID 與 CID 指定目標？</a></li>
<li><a href="#q-108">Q108 · Abort 已完成、不存在或指定錯誤 SQID／CID 的命令時會怎樣？</a></li>
<li><a href="#q-109">Q109 · 重複 Abort 與並行 Abort 如何套用 ACL？</a></li>
<li><a href="#q-110">Q110 · Abort 成功是否代表目標完全沒有執行？</a></li>
<li><a href="#q-111">Q111 · Abort 未立即中止時，目標還能正常完成嗎？</a></li>
<li><a href="#q-112">Q112 · Abort 與目標完成同時到達，Host 如何避免重複處理？</a></li>
<li><a href="#q-113">Q113 · Timeout 後一定要依 Abort、Queue Reset、Controller Reset 的順序嗎？</a></li>
<li><a href="#q-114">Q114 · Abort 本身也 Timeout，Host 應如何復原？</a></li>
<li><a href="#q-115">Q115 · Reset 後如何處理舊命令、舊完成與舊 Queue？</a></li>
<li><a href="#q-116">Q116 · 如何區分 Command Timeout、Ready Timeout 與長時間操作？</a></li>
<li><a href="#q-117">Q117 · Timeout 時如何定位提交、取得、執行、完成或 Host 處理階段？</a></li>
</ol></section>
<article class="qa-question" id="q-107" data-question="107" data-answer-kind="process"><h2><a class="qa-qid" href="#q-107">Q107</a> Abort 如何用 SQID 與 CID 指定目標？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-107-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-107-a-01">Abort 請求中止一筆先前提交的命令，讓 Host 不必只為一筆逾時操作立即重設整個 controller。它是請求，不是保證目標尚未執行。</p><div class="qa-sections">
<section class="qa-section" id="q-107-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-107-a-02"></span><p>目標可以位於 Admin SQ 或 I/O SQ。Abort 自己也是 Admin 命令，有自己的 CID 與完成結果。</p>
<span class="qa-anchor" id="q-107-a-03"></span><p>Identify.ACL 宣告可同時 outstanding 的 Abort 數量，零起算；一般命令的 queue 深度不能代替 ACL。</p>
<span class="qa-anchor" id="q-107-a-04"></span><p>Abort CDW10 bits31:16 是目標 CID，15:0 是目標 SQID；Abort 自己的 CDW0.CID 則用來配對 Abort 的 CQE。</p>
</section>
<section class="qa-section" id="q-107-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-107-a-05"></span><p>從 outstanding 清單找到目標 SQID／CID，保留目標的 buffer，再以新的 Admin CID 提交 Abort；分別追蹤兩筆完成。</p>
<span class="qa-anchor" id="q-107-a-06"></span><p>Abort 成功 CQE 的 DW0.IANP=0 表示立即中止已執行；IANP=1 表示未執行立即中止，仍可能稍後中止。最後也要查看目標 CQE。</p>
</section>
<section class="qa-section" id="q-107-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-107-a-07"></span><p>超過 ACL 時，controller 可回 Abort Command Limit Exceeded（1/03h）。目標找不到則可由成功 Abort 的 IANP=1 表示，不應固定要求 Invalid Queue Identifier。</p>
<span class="qa-anchor" id="q-107-a-16"></span><p>模擬 SQ3／CID7 與 SQ4／CID7 同時存在時，CDW10=(7&lt;&lt;16)|3 只指定前者。用這個例子驗證解析是否把兩個欄位顛倒。</p>
</section>
</div>
<span class="qa-anchor" id="q-107-a-17"></span><span class="qa-anchor" id="q-107-a-08"></span><span class="qa-anchor" id="q-107-a-09"></span><span class="qa-anchor" id="q-107-a-10"></span><span class="qa-anchor" id="q-107-a-11"></span><span class="qa-anchor" id="q-107-a-12"></span><span class="qa-anchor" id="q-107-a-13"></span><span class="qa-anchor" id="q-107-a-14"></span><span class="qa-anchor" id="q-107-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-108" data-question="108" data-answer-kind="error"><h2><a class="qa-qid" href="#q-108">Q108</a> Abort 已完成、不存在或指定錯誤 SQID／CID 的命令時會怎樣？</h2>
<p class="qa-prompt">先區分失敗條件，再判斷是否有規範明定的回報結果。</p>
<details class="qa-answer" id="q-108-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-108-a-01">目標在 Host 決定中止與 controller 處理 Abort 之間可能已完成，所以「沒找到」是必須處理的正常競爭情況。</p><div class="qa-sections">
<section class="qa-section" id="q-108-s-01" data-answer-section="1"><h3><span>1.</span> 先區分是哪一種失敗</h3>
<span class="qa-anchor" id="q-108-a-02"></span><p>判斷的是指定 SQID／CID 在那個時點的命令，不是 Host 曾經提交過同一編號就永遠存在。</p>
<span class="qa-anchor" id="q-108-a-04"></span><p>讀 Abort 的 CQE Status 及 DW0.IANP，並檢查目標是否已留下有效 CQE。IANP=1 的原因可以是找不到目標，也可以是無法立即中止。</p>
<span class="qa-anchor" id="q-108-a-07"></span><p>不要把所有不存在的 SQID／CID 都要求成某個固定錯誤 Status。若 Abort 本身欄位另有非法值，則依該非法條件處理。</p>
</section>
<section class="qa-section" id="q-108-s-02" data-answer-section="2"><h3><span>2.</span> 用哪些資料確認原因</h3>
<span class="qa-anchor" id="q-108-a-03"></span><p>保留 queue 使用期間與 CID 配置紀錄，避免 Abort 延遲到 CID 已被下一筆命令重用。</p>
<span class="qa-anchor" id="q-108-a-05"></span><p>先處理已收到的目標完成，再處理 Abort 結果；如果目標仍 outstanding 且 IANP=1，繼續追蹤目標，不能擅自釋放 buffer。</p>
</section>
<section class="qa-section" id="q-108-s-03" data-answer-section="3"><h3><span>3.</span> 結果與後續驗證</h3>
<span class="qa-anchor" id="q-108-a-06"></span><p>有效的 Abort 命令即使沒中止目標，也可回成功且 IANP=1。這表示請求處理完成，不是目標操作成功或回復。</p>
<span class="qa-anchor" id="q-108-a-16"></span><p>如果測試期待「目標已完成後 Abort 必須失敗」，應修正為核對 IANP 與既有目標結果。</p>
<span class="qa-anchor" id="q-108-a-17"></span><p>先查目標是否其實早已完成，只是 Host 尚未消費 CQE。</p>
</section>
</div>
<span class="qa-anchor" id="q-108-a-08"></span><span class="qa-anchor" id="q-108-a-09"></span><span class="qa-anchor" id="q-108-a-10"></span><span class="qa-anchor" id="q-108-a-11"></span><span class="qa-anchor" id="q-108-a-12"></span><span class="qa-anchor" id="q-108-a-13"></span><span class="qa-anchor" id="q-108-a-14"></span><span class="qa-anchor" id="q-108-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-109" data-question="109" data-answer-kind="error"><h2><a class="qa-qid" href="#q-109">Q109</a> 重複 Abort 與並行 Abort 如何套用 ACL？</h2>
<p class="qa-prompt">先區分失敗條件，再判斷是否有規範明定的回報結果。</p>
<details class="qa-answer" id="q-109-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-109-a-01">ACL 限制同時處理的 Abort 請求數量，不是每秒可中止多少命令，也不是可被中止的 namespace 數。</p><div class="qa-sections">
<section class="qa-section" id="q-109-s-01" data-answer-section="1"><h3><span>1.</span> 先區分是哪一種失敗</h3>
<span class="qa-anchor" id="q-109-a-02"></span><p>每一筆尚未完成的 Abort 都占用其並行配額；多筆指向同一目標，也不能當成只送了一筆。</p>
<span class="qa-anchor" id="q-109-a-04"></span><p>分開記錄 Abort 自己的 Admin CID、目標 SQID／CID 及結果。大量中止可考慮支援的 Cancel，或刪除並重建 I/O SQ。</p>
<span class="qa-anchor" id="q-109-a-07"></span><p>controller 可將超額請求完成為 Abort Command Limit Exceeded（1/03h），規範不是要求每個超額時點都必定看到此碼。</p>
</section>
<section class="qa-section" id="q-109-s-02" data-answer-section="2"><h3><span>2.</span> 用哪些資料確認原因</h3>
<span class="qa-anchor" id="q-109-a-03"></span><p>Identify.ACL=0 表示支援至少 1 筆並行 Abort；ACL=3 表示 4 筆。Host 應依完成回收這份配額。</p>
<span class="qa-anchor" id="q-109-a-05"></span><p>提交前檢查配額，達上限就等待先前 Abort 完成。重複目標時仍逐筆處理 Abort CQE，但目標命令不能因此完成兩次。</p>
</section>
<section class="qa-section" id="q-109-s-03" data-answer-section="3"><h3><span>3.</span> 結果與後續驗證</h3>
<span class="qa-anchor" id="q-109-a-06"></span><p>例如 ACL=1，兩筆 Abort outstanding 符合配額；其中一筆完成後才提交下一筆，就不會因 Host 超量造成干擾。</p>
<span class="qa-anchor" id="q-109-a-16"></span><p>測量 outstanding 數時，以提交到完成的期間計算；不要拿累計 Abort 次數與 ACL 比較。</p>
<span class="qa-anchor" id="q-109-a-17"></span><p>先確認測試是否漏掉 ACL 的零起算，或重複計入已完成的 Abort。</p>
</section>
</div>
<span class="qa-anchor" id="q-109-a-08"></span><span class="qa-anchor" id="q-109-a-09"></span><span class="qa-anchor" id="q-109-a-10"></span><span class="qa-anchor" id="q-109-a-11"></span><span class="qa-anchor" id="q-109-a-12"></span><span class="qa-anchor" id="q-109-a-13"></span><span class="qa-anchor" id="q-109-a-14"></span><span class="qa-anchor" id="q-109-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-110" data-question="110" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-110">Q110</a> Abort 成功是否代表目標完全沒有執行？</h2>
<p class="qa-prompt">先用自己的話解釋機制，再舉一個常見誤解。</p>
<details class="qa-answer" id="q-110-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-110-a-01">不代表。Abort 能停止後續處理，卻不是交易回復機制；目標可能在中止前已傳輸部分資料或改變狀態。</p><div class="qa-sections">
<section class="qa-section" id="q-110-s-01" data-answer-section="1"><h3><span>1.</span> IANP 決定的是中止後的保證</h3>
<span class="qa-anchor" id="q-110-a-03"></span><p>Base 2.4 的關鍵證據是成功 Abort 的 IANP，而不是單看 Status=Success。</p>
<span class="qa-anchor" id="q-110-a-04"></span><p>IANP=0 時，除之後張貼目標 CQE 外，Abort CQE 張貼後不得再有目標命令造成的 Host memory 存取或媒體／管理狀態改變。</p>
<span class="qa-anchor" id="q-110-a-06"></span><p>立即中止後，目標以 Command Abort Requested 完成。目標 CQE 可在 Abort CQE 之前，也可在滿足無後續效果條件下之後出現。</p>
<span class="qa-anchor" id="q-110-a-07"></span><p>IANP=1 不保證無後續效果；如果資料傳輸已開始而未完成，且目標 CQE 尚未張貼，就不能宣稱符合立即中止條件。</p>
</section>
<section class="qa-section" id="q-110-s-02" data-answer-section="2"><h3><span>2.</span> 已經發生的效果仍要另外確認</h3>
<span class="qa-anchor" id="q-110-a-05"></span><p>記錄 Abort CQE 時點及 IANP，等待並處理目標 CQE，再依命令語意確認資料結果。若需重試 Write，先處理可能已執行部分與重試的關係。</p>
<span class="qa-anchor" id="q-110-a-16"></span><p>合規測試應檢查 Abort CQE 之後是否仍有被禁止的目標效果，而不是要求整個命令從來沒有做過任何事。</p>
</section>
</div>
<span class="qa-anchor" id="q-110-a-02"></span><span class="qa-anchor" id="q-110-a-17"></span><span class="qa-anchor" id="q-110-a-08"></span><span class="qa-anchor" id="q-110-a-09"></span><span class="qa-anchor" id="q-110-a-10"></span><span class="qa-anchor" id="q-110-a-11"></span><span class="qa-anchor" id="q-110-a-12"></span><span class="qa-anchor" id="q-110-a-13"></span><span class="qa-anchor" id="q-110-a-14"></span><span class="qa-anchor" id="q-110-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-111" data-question="111" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-111">Q111</a> Abort 未立即中止時，目標還能正常完成嗎？</h2>
<p class="qa-prompt">先用自己的話解釋機制，再舉一個常見誤解。</p>
<details class="qa-answer" id="q-111-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-111-a-01">可以。IANP=1 表示未執行立即中止，controller 仍可稍後中止，也可能讓目標正常完成。Host 必須保留兩種可能。</p><div class="qa-sections">
<section class="qa-section" id="q-111-s-01" data-answer-section="1"><h3><span>1.</span> 先分開判讀 Abort 與目標的 CQE</h3>
<span class="qa-anchor" id="q-111-a-03"></span><p>查看成功 Abort 的 IANP 及目標 CQE。若 Abort 自己以錯誤完成，不應把保留或未定義的 DW0 當成有效 IANP 結果。</p>
<span class="qa-anchor" id="q-111-a-04"></span><p>目標若延後被中止，Status 必須是 Command Abort Requested；若正常執行完成，則依目標命令回報實際結果。</p>
<span class="qa-anchor" id="q-111-a-06"></span><p>收到目標成功 CQE 是合法可能；收到 Command Abort Requested 也是合法可能。兩者都不需要再產生第二筆目標完成。</p>
</section>
<section class="qa-section" id="q-111-s-02" data-answer-section="2"><h3><span>2.</span> IANP=1 後仍要追蹤目標</h3>
<span class="qa-anchor" id="q-111-a-05"></span><p>IANP=1 後持續等待有效目標 CQE，同時依 Host 復原策略控制等待時間。若需要擴大到 Reset，先完成 queue 使用期間的切換與資源保護。</p>
<span class="qa-anchor" id="q-111-a-07"></span><p>不要將 IANP=1 解釋成「永遠不會中止」，也不要解釋成「一定晚一點中止」。</p>
</section>
</div>
<span class="qa-anchor" id="q-111-a-02"></span><span class="qa-anchor" id="q-111-a-16"></span><span class="qa-anchor" id="q-111-a-17"></span><span class="qa-anchor" id="q-111-a-08"></span><span class="qa-anchor" id="q-111-a-09"></span><span class="qa-anchor" id="q-111-a-10"></span><span class="qa-anchor" id="q-111-a-11"></span><span class="qa-anchor" id="q-111-a-12"></span><span class="qa-anchor" id="q-111-a-13"></span><span class="qa-anchor" id="q-111-a-14"></span><span class="qa-anchor" id="q-111-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-112" data-question="112" data-answer-kind="process"><h2><a class="qa-qid" href="#q-112">Q112</a> Abort 與目標完成同時到達，Host 如何避免重複處理？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-112-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-112-a-01">並行完成會讓 Host 的 timeout 路徑與一般完成路徑同時碰到同一份追蹤資料。需要同步的是 Host 狀態，不是要求 controller 將所有完成排成固定順序。</p><div class="qa-sections">
<section class="qa-section" id="q-112-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-112-a-02"></span><p>一筆 Abort 與一筆目標命令有各自的生命週期；共享目標不代表兩個 CQE 是同一個完成。</p>
<span class="qa-anchor" id="q-112-a-03"></span><p>用 CQE.SQID＋CID、有效 Phase 與 queue 使用期間識別命令；只比 CID 不足以跨 queue 關聯。</p>
<span class="qa-anchor" id="q-112-a-04"></span><p>追蹤資料要能表示目標未完成、已完成，以及 Abort 尚未完成／已完成。只有目標結果才能交付目標的上層完成。</p>
</section>
<section class="qa-section" id="q-112-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-112-a-05"></span><p>收到任一 CQE 時，以同步方式更新相應狀態。目標先完成就保存結果，之後 Abort CQE 只結束 Abort；Abort 先完成則依 IANP 與目標狀態繼續處理。</p>
<span class="qa-anchor" id="q-112-a-06"></span><p>每筆命令各完成一次，每份資源各回收一次。兩個不同命令的 CQE 都存在是正常，不能誤算成目標完成兩次。</p>
</section>
<section class="qa-section" id="q-112-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-112-a-07"></span><p>不能固定要求目標 CQE 一定先於 Abort CQE；Base 2.4 在滿足立即中止的無後續效果保證時，允許任一張貼順序。</p>
<span class="qa-anchor" id="q-112-a-16"></span><p>驗證同一 target SQID／CID 沒有被上層完成兩次，且新的 CID 使用期間不會吃到舊 Abort 的結果。</p>
</section>
</div>
<span class="qa-anchor" id="q-112-a-17"></span><span class="qa-anchor" id="q-112-a-08"></span><span class="qa-anchor" id="q-112-a-09"></span><span class="qa-anchor" id="q-112-a-10"></span><span class="qa-anchor" id="q-112-a-11"></span><span class="qa-anchor" id="q-112-a-12"></span><span class="qa-anchor" id="q-112-a-13"></span><span class="qa-anchor" id="q-112-a-14"></span><span class="qa-anchor" id="q-112-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-113" data-question="113" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-113">Q113</a> Timeout 後一定要依 Abort、Queue Reset、Controller Reset 的順序嗎？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-113-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-113-a-01">沒有適用於所有命令的固定三步程序。Host 要先判斷是單筆命令太慢、queue 失效，還是 controller 已無法通訊，再選擇能解決問題的範圍。</p><div class="qa-sections">
<section class="qa-section" id="q-113-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-113-a-02"></span><p>Abort 針對命令；I/O queue 刪除／重建針對相關 queue；Controller Reset 會影響該 controller 的全部 queue 與未完成命令。</p>
<span class="qa-anchor" id="q-113-a-03"></span><p>保存 CQ 指標、Phase、中斷設定、CSTS 與其他命令的進度。CAP.TO 不代表每條 I/O 的 timeout。</p>
<span class="qa-anchor" id="q-113-a-04"></span><p>可用操作包括 Abort、Delete I/O SQ／CQ、重新建立 queue，以及 CC.EN 觸發的重設；每種操作都需要有效的前提與完成確認。</p>
</section>
<section class="qa-section" id="q-113-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-113-a-05"></span>
<span class="qa-anchor" id="q-113-a-17"></span>
<figure class="qa-flow" id="q-113-flow"><figcaption>先定位失效範圍，再選復原方式</figcaption>
<p>下列分支是 Host 選擇復原範圍的判斷方式，不是規格要求每次都走完的固定三步。</p><ol class="qa-flow-steps">
<li class="qa-flow-step"><strong>先看 CQ：是否已經有有效 Completion？</strong><p>若只是 Host 漏處理或沒有收到中斷，先處理 CQE 並追查通知路徑。</p></li>
<li class="qa-flow-branch"><strong>單筆命令仍未完成，Admin 通道正常</strong><p>可考慮針對目標送 Abort，再分別追蹤 Abort 與目標命令的結果。</p></li>
<li class="qa-flow-branch"><strong>Queue 受損，但管理通道可用</strong><p>按 Delete／Create 規則復原相關 queue，確認舊存取已停止，再交接記憶體。</p></li>
<li class="qa-flow-branch"><strong>Admin 嚴重失效，或 Delete 沒有完成</strong><p>考慮 Controller Reset；不必先強迫送出一筆已無法完成的 Abort。</p></li>
</ol><p class="qa-flow-conclusion">沒有 CQE 時，Host timeout 本身沒有 DNR 可讀。復原後仍需確認背景管理操作是否持續，不能只以新 queue 能送命令作為全部完成的證據。</p></figure>
</section>
<section class="qa-section" id="q-113-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-113-a-06"></span><p>復原完成應同時建立可用新通道、結束舊命令的後續存取風險，並重新確認可能持續的背景管理操作。</p>
<span class="qa-anchor" id="q-113-a-07"></span><p>Host 計時器到期不是 controller 回傳的 NVMe Status。不能為「沒收到 CQE」捏造 Timeout CQE，也不能無條件要求先送一筆注定無法完成的 Abort。</p>
<span class="qa-anchor" id="q-113-a-16"></span><p>測試計畫要標示哪些是 Spec 要求，哪些是 Host 選定的 timeout 與升級策略。</p>
</section>
</div>
<span class="qa-anchor" id="q-113-a-08"></span><span class="qa-anchor" id="q-113-a-09"></span><span class="qa-anchor" id="q-113-a-10"></span><span class="qa-anchor" id="q-113-a-11"></span><span class="qa-anchor" id="q-113-a-12"></span><span class="qa-anchor" id="q-113-a-13"></span><span class="qa-anchor" id="q-113-a-14"></span><span class="qa-anchor" id="q-113-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-114" data-question="114" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-114">Q114</a> Abort 本身也 Timeout，Host 應如何復原？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-114-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-114-a-01">這時不只目標結果不明，連 Admin 通道是否可完成命令都需要確認。無限追加 Abort 會增加未完成請求，卻不能證明舊命令已停止。</p><div class="qa-sections">
<section class="qa-section" id="q-114-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-114-a-02"></span><p>復原可能從單一命令擴大到 controller；應先通知使用這個 controller 的 queue 管理與資源回收邏輯。</p>
<span class="qa-anchor" id="q-114-a-03"></span><p>檢查 Admin CQ 的 Phase／Head、CSTS.CFS／RDY，以及 Abort outstanding 是否超過 ACL。</p>
<span class="qa-anchor" id="q-114-a-04"></span><p>保存 Abort 的 Admin CID、目標 IDs、提交時間及已觀察的 CQE。後續 Reset 是另一項操作，不應偽造 Abort 的完成結果。</p>
</section>
<section class="qa-section" id="q-114-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-114-a-17"></span><p>先檢查 Admin CQ 是否已滿或被 Host 停止消費。</p>
<span class="qa-anchor" id="q-114-a-05"></span><p>先排除 Admin CQ 已有完成但 Host 漏讀。若確認嚴重 Admin 問題，依 Base 9.1／9.5 進行 Controller Reset、等待狀態，再重建操作環境。</p>
</section>
<section class="qa-section" id="q-114-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-114-a-06"></span><p>成功復原後，新命令可以使用新 queue；舊目標是否曾完成其資料效果，仍需依命令與持久化語意判斷。</p>
<span class="qa-anchor" id="q-114-a-07"></span><p>沒有 Abort CQE 就沒有可解讀的 IANP、DNR 或 More。也不能將 Reset 成功當成目標 Write 從未發生的證明。</p>
<span class="qa-anchor" id="q-114-a-16"></span><p>以 Register 狀態、新 queue 的可用性及持續操作的 Log 交叉確認，不只用「Reset 函式回傳成功」當成全部證據。</p>
</section>
</div>
<span class="qa-anchor" id="q-114-a-08"></span><span class="qa-anchor" id="q-114-a-09"></span><span class="qa-anchor" id="q-114-a-10"></span><span class="qa-anchor" id="q-114-a-11"></span><span class="qa-anchor" id="q-114-a-12"></span><span class="qa-anchor" id="q-114-a-13"></span><span class="qa-anchor" id="q-114-a-14"></span><span class="qa-anchor" id="q-114-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-115" data-question="115" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-115">Q115</a> Reset 後如何處理舊命令、舊完成與舊 Queue？</h2>
<p class="qa-prompt">先指明重設或中斷的方式，再分別判斷設定、進行中的操作與資料。</p>
<details class="qa-answer" id="q-115-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-115-a-01">Reset 劃分命令與 queue 的使用期間。記憶體內還看得到舊 bytes，不代表它們仍是可用的命令或完成。</p><div class="qa-sections">
<section class="qa-section" id="q-115-s-01" data-answer-section="1"><h3><span>1.</span> 先界定觸發方式與影響對象</h3>
<span class="qa-anchor" id="q-115-a-02"></span><p>受影響 controller 的 I/O queues 與未完成追蹤要重建。媒體上的既有資料與獨立背景操作，則有各自的保留或繼續規則。</p>
<span class="qa-anchor" id="q-115-a-03"></span><p>查看 Reset 類型、CC／CSTS 及 Admin Queue Register 保留條件；不要把清 CC.EN 的例外套到所有 Reset 來源。</p>
</section>
<section class="qa-section" id="q-115-s-02" data-answer-section="2"><h3><span>2.</span> 哪些狀態改變，恢復後怎麼處理</h3>
<span class="qa-anchor" id="q-115-a-04"></span><p>Host 重設 SQ／CQ 指標與期待 Phase，將新提交與舊追蹤隔離；背景 Sanitize 等另用對應 Log 查進度。</p>
<span class="qa-anchor" id="q-115-a-05"></span><p>先停止新提交，完成 Reset 的等待與存取停止確認，再建立新 queue，最後恢復 I/O。需要重試時，先分析原命令是否可能已產生效果。</p>
<span class="qa-anchor" id="q-115-a-06"></span><p>新 queue 只接受新生命週期的有效完成；Host 不再以舊 CID 清單等待已被 Reset 結束的所有 CQE。</p>
</section>
<section class="qa-section" id="q-115-s-03" data-answer-section="3"><h3><span>3.</span> 如何驗證保留或恢復結果</h3>
<span class="qa-anchor" id="q-115-a-07"></span><p>Reset 通常不是逐筆回傳某個固定錯誤碼。AER 更明定因 Reset 中止時不得回 CQE；其他命令也不能一律要求 Command Abort Requested。</p>
<span class="qa-anchor" id="q-115-a-16"></span><p>同時驗證新 queue 正常，以及舊 buffer 不再被舊命令使用；僅看新命令成功，無法排除舊命令晚到的存取。</p>
<span class="qa-anchor" id="q-115-a-17"></span><p>先查 Host 是否重用了舊 Phase 或追蹤資料，造成把舊 CQE 當成新完成。</p>
</section>
</div>
<span class="qa-anchor" id="q-115-a-08"></span><span class="qa-anchor" id="q-115-a-09"></span><span class="qa-anchor" id="q-115-a-10"></span><span class="qa-anchor" id="q-115-a-11"></span><span class="qa-anchor" id="q-115-a-12"></span><span class="qa-anchor" id="q-115-a-13"></span><span class="qa-anchor" id="q-115-a-14"></span><span class="qa-anchor" id="q-115-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-116" data-question="116" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-116">Q116</a> 如何區分 Command Timeout、Ready Timeout 與長時間操作？</h2>
<p class="qa-prompt">先說出比較對象最重要的差別，並舉一個不能互相代用的例子。</p>
<details class="qa-answer" id="q-116-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-116-a-01">不同等待對象需要不同期限：命令等待 CQE，初始化等待 RDY，背景操作則可能在命令已完成後持續。混用期限會造成不必要的 Reset。</p><div class="qa-sections">
<section class="qa-section" id="q-116-s-01" data-answer-section="1"><h3><span>1.</span> 差別在哪裡</h3>
<span class="qa-anchor" id="q-116-a-02"></span><p>Host 命令 timeout 是軟體政策；Ready 等待針對 controller 狀態；Sanitize 等進度則屬指定管理操作的範圍。</p>
<span class="qa-anchor" id="q-116-a-04"></span><p>觀察 CQE、CSTS.RDY 及操作狀態 Log。AER 沒事件時應保持 outstanding，規範建議不套一般命令 timeout。</p>
</section>
<section class="qa-section" id="q-116-s-02" data-answer-section="2"><h3><span>2.</span> 如何選擇與確認</h3>
<span class="qa-anchor" id="q-116-a-03"></span><p>停用看 CAP.TO；啟用依 Ready Mode 與 CRTO／CAP 規則；個別功能若宣告預估時間或最大時間，則按其欄位定義使用。</p>
<span class="qa-anchor" id="q-116-a-05"></span><p>先寫清楚正在等待哪個狀態轉移，再從正確起點計時。例如成功啟動 Sanitize 後，改查 Sanitize Status，不繼續等第二個 Sanitize CQE。</p>
<span class="qa-anchor" id="q-116-a-06"></span><p>期限內達到指定狀態才是該項等待成功。命令回 Success 與媒體工作完成，可能分屬不同時間。</p>
</section>
<section class="qa-section" id="q-116-s-03" data-answer-section="3"><h3><span>3.</span> 哪些結論不能互相套用</h3>
<span class="qa-anchor" id="q-116-a-07"></span><p>沒有全 NVMe 命令共用的 CAP.TO。預估完成時間也不應自動升級成必須遵守的硬性 timeout。</p>
<span class="qa-anchor" id="q-116-a-16"></span><p>將測試報告中的每個 timeout 註明來源、單位、起算時點與是估計還是上限。</p>
</section>
</div>
<span class="qa-anchor" id="q-116-a-17"></span><span class="qa-anchor" id="q-116-a-08"></span><span class="qa-anchor" id="q-116-a-09"></span><span class="qa-anchor" id="q-116-a-10"></span><span class="qa-anchor" id="q-116-a-11"></span><span class="qa-anchor" id="q-116-a-12"></span><span class="qa-anchor" id="q-116-a-13"></span><span class="qa-anchor" id="q-116-a-14"></span><span class="qa-anchor" id="q-116-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-crto">Base 2.4 §3.1.4 (CRTO)</a> · <a href="#ref-ready">Base 2.4 §3.5.3–3.5.4</a> · <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-117" data-question="117" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-117">Q117</a> Timeout 時如何定位提交、取得、執行、完成或 Host 處理階段？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-117-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-117-a-01">沿命令生命週期保存證據，可以把「沒完成」拆成可查的階段，而不急著歸咎韌體執行太慢。</p><div class="qa-sections">
<section class="qa-section" id="q-117-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-117-a-02"></span><p>分析一筆目標命令時，也要觀察其 SQ、關聯 CQ、共享向量與其他命令，因為瓶頸可能位於共用資源。</p>
<span class="qa-anchor" id="q-117-a-03"></span><p>使用 SQE 快照、SQ Tail Doorbell、回報的 SQHD、CQ Phase／Head、中斷設定與 CSTS；這些都是 PCIe NVMe 介面層證據。</p>
<span class="qa-anchor" id="q-117-a-04"></span><p>SQHD 前進表示已消費位置，不表示每筆命令完成；有效目標 CQE 才提供完成結果；中斷則是通知 Host 查 CQ 的機制。</p>
</section>
<section class="qa-section" id="q-117-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-117-a-17"></span><p>先直接檢查目標 CQ 的期待 Phase 位置；這通常最快區分「尚未回報」與「已回報但未處理」。</p>
<span class="qa-anchor" id="q-117-a-05"></span><p>依序確認 SQE 對 controller 可見、Doorbell 已更新、CQ 是否有新 Phase、Host 是否消費並更新 Head。若無法觀察內部取得時點，就明確保留這項不確定性。</p>
</section>
<section class="qa-section" id="q-117-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-117-a-06"></span><p>能定位到「CQE 已存在但中斷或 Host 處理遺漏」，就不應再宣稱命令未執行。若只有 Doorbell 證據，也不能宣稱 controller 已取得命令。</p>
<span class="qa-anchor" id="q-117-a-07"></span><p>這項診斷本身沒有固定 NVMe Status。不同階段的錯誤應保留各自證據，不用一個自創 Timeout Status 取代。</p>
<span class="qa-anchor" id="q-117-a-16"></span><p>比對同時間的有效 CQE、共享 CQ 空間及中斷遮蔽，排除 Host 端的進度阻塞。</p>
</section>
</div>
<span class="qa-anchor" id="q-117-a-08"></span><span class="qa-anchor" id="q-117-a-09"></span><span class="qa-anchor" id="q-117-a-10"></span><span class="qa-anchor" id="q-117-a-11"></span><span class="qa-anchor" id="q-117-a-12"></span><span class="qa-anchor" id="q-117-a-13"></span><span class="qa-anchor" id="q-117-a-14"></span><span class="qa-anchor" id="q-117-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-irq">PCIe Transport 1.4 §3.5</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>

<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-cap"><strong>Base 2.4 · §3.1.4 (CAP, VS)</strong><br>文件頁 54–59 · PDF 80–85 · Figure 36–37</li>
<li id="ref-crto"><strong>Base 2.4 · §3.1.4 (CRTO)</strong><br>文件頁 72–73 · PDF 98–99 · Figure 57</li>
<li id="ref-queue"><strong>Base 2.4 · §3.3.1</strong><br>文件頁 88–91 · PDF 114–117 · Figure 73–74</li>
<li id="ref-order"><strong>Base 2.4 · §3.4.1–3.4.5</strong><br>文件頁 101–105 · PDF 127–131 · Figure 80–81</li>
<li id="ref-ready"><strong>Base 2.4 · §3.5.3–3.5.4</strong><br>文件頁 109–113 · PDF 135–139 · Figure 84–85</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-sqe"><strong>Base 2.4 · §4.1.1</strong><br>文件頁 139–142 · PDF 165–168 · Figure 92–93</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>文件頁 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-abort"><strong>Base 2.4 · §5.2.1</strong><br>文件頁 181–182 · PDF 207–208 · Figure 147–149</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>文件頁 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>文件頁 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-commrecovery"><strong>Base 2.4 · §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</strong><br>文件頁 825–828 · PDF 851–854</li>
<li id="ref-fatal"><strong>Base 2.4 · §9.1–9.6.1</strong><br>文件頁 825–826 · PDF 851–852</li>
<li id="ref-pcie"><strong>PCIe Transport 1.4 · §3.1–3.4</strong><br>文件頁 9–13 · PDF 9–13 · Figure 3–8</li>
<li id="ref-irq"><strong>PCIe Transport 1.4 · §3.5</strong><br>文件頁 13–16 · PDF 13–16 · Figure 9</li>
</ul><h3>需要看欄位圖時</h3><p>以下連結可開啟對應的圖表教學，查閱欄位及判讀方式。每張圖保留固定的教學位置，方便之後反覆查詢。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/recovery/en/">English</a><a href="/DOCS/nvme-question-bank/recovery.html">繁中教學 HTML</a></nav>
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
