---
layout: post
title: "NVMe 自問自答題庫：Command、Completion 與處理順序"
date: 2026-10-01 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/commands/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/commands/en/">English</a><a href="/DOCS/nvme-question-bank/commands.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q31–Q43</p><h1>Command、Completion 與處理順序</h1><p class="qr-intro">從 Host 提交命令，到 controller 取得、處理並回報完成，再到 Host 回收資源，各階段能證明的事情不同。本冊沿著這條流程解讀 Command 與 CQE，並說明順序、仲裁及中斷各自控制什麼。只有完成順序，還不足以推論 controller 內部的全部行為。</p><p>先練習，再展開解答。各題依需要使用文字、欄位判讀、比較或流程說明，不要求相同的回答項目。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>同一筆命令，五個不同的觀察時點</h2><p class="qa-takeaway">觀察到流程有進展，不表示命令已成功完成。先確認觀察的是哪個階段，才能知道這份資訊足以支持什麼結論。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">時點</th><th scope="col">能確認的事情</th><th scope="col">尚不能確認的事情</th></tr></thead><tbody><tr><td>寫好 SQE</td><td>Host 已填 Opcode、CID、NSID、資料指標</td><td>controller 是否已能看見這筆 SQE</td></tr><tr><td>更新 SQ Tail</td><td>命令已提交；Host 仍須另行確保記憶體內容對 controller 可見</td><td>controller 是否已取得 SQE，或命令是否已完成</td></tr><tr><td>CQE 回報 SQHD 前進</td><td>controller 已消費至回報的位置</td><td>這些位置原先放置的命令是否全部完成</td></tr><tr><td>目標 CQE Phase 有效</td><td>可用 SQID＋CID 對回這筆完成，讀 SCT／SC</td><td>中斷是否已送達，以及資料是否已持久保存</td></tr><tr><td>Host 更新 CQ Head</td><td>Host 已處理 CQE，並釋放對應的 CQ 空間</td><td>其他 SQ 或其他 CID 的命令是否也已完成</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>SQ1 的 CID=7 與 SQ2 的 CID=7 可以同時存在。若它們共用 CQ，Host 只看到 CID=7 還無法找到原命令，必須搭配 CQE.SQID 才能正確配對。若要進一步確認 Write 的資料是否已持久保存，還需核對 WCE、FUA 或 Flush 的完成條件，不能只看成功 Status。</p>
<p class="qa-citations">來源：<a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-vwc">Base 2.4 §5.2.30.1.4</a> · <a href="#ref-nvmatomic">NVM Command Set 1.3 §2.1.2–2.1.4</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-031">Q31 · 一筆 NVMe Command 的 Opcode、CID、NSID、Data Pointer 及 Command Dword 各有什麼用途？</a></li>
<li><a href="#q-032">Q32 · Reserved 欄位非零、不合法 Command Dword 組合或不支援 Opcode 應如何處理？</a></li>
<li><a href="#q-033">Q33 · NSID 不存在、Inactive、不適用或錯誤使用 Broadcast NSID 時，應回傳什麼類型的 Status？</a></li>
<li><a href="#q-034">Q34 · CQE 中的 SQHD、SQID、CID、Phase Tag 及 Status 分別有什麼用途？</a></li>
<li><a href="#q-035">Q35 · Status Code Type 與 Status Code 應如何解析？</a></li>
<li><a href="#q-036">Q36 · More 與 Do Not Retry 位元分別代表什麼？DNR 為 0 是否代表一定能直接重試？</a></li>
<li><a href="#q-037">Q37 · Completion 已寫入但 Host 未處理，可能與 Phase Tag、CQ 位置或 Interrupt 有什麼關係？</a></li>
<li><a href="#q-038">Q38 · 多個 Command 同時 Outstanding 時，Controller 是否必須按照提交順序完成？</a></li>
<li><a href="#q-039">Q39 · 哪些 Command 具有順序相依性？Host 為什麼不能假設所有 Command 都依序完成？</a></li>
<li><a href="#q-040">Q40 · Outstanding Command 達到限制或 CQ Full 時，Controller 如何限制取得新 Command？</a></li>
<li><a href="#q-041">Q41 · Round Robin 與 Weighted Round Robin Arbitration 有什麼差異？</a></li>
<li><a href="#q-042">Q42 · Urgent、High、Medium 及 Low Queue Priority 在哪些情況下生效？</a></li>
<li><a href="#q-043">Q43 · 多個 Queue 競爭資源時，如何判斷 Arbitration 是否符合設定？</a></li>
</ol></section>
<article class="qa-question" id="q-031" data-question="31" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-031">Q31</a> 一筆 NVMe Command 的 Opcode、CID、NSID、Data Pointer 及 Command Dword 各有什麼用途？</h2>
<p class="qa-prompt">先試著說明欄位的單位與編碼，再用一組數值推導結果。</p>
<details class="qa-answer" id="q-031-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-031-a-01">一筆命令必須讓 controller 知道要執行什麼操作、目標是誰、資料放在哪裡，以及要使用哪些參數。Command 格式就是把這些資訊放進各自指定的欄位。</p><div class="qa-sections">
<section class="qa-section" id="q-031-s-01" data-answer-section="1"><h3><span>1.</span> 先確認資料的來源與範圍</h3>
<span class="qa-anchor" id="q-031-a-02"></span><p>解讀 Opcode 前，先確認這是 Admin 命令，還是哪一種 I/O command set 的命令。相同的 Opcode 數值，在不同命令集中不一定代表相同操作。</p>
<span class="qa-anchor" id="q-031-a-03"></span><p>先確認對應能力，例如 OACS、ONCS、SGLS，並核對 namespace 使用的 CSI。接著再看該命令實際使用哪些公共欄位，不能假設每條命令都使用全部欄位。</p>
</section>
<section class="qa-section" id="q-031-s-02" data-answer-section="2"><h3><span>2.</span> 欄位、單位與判讀例子</h3>
<span class="qa-anchor" id="q-031-a-04"></span><p>公共 Command 格式為 64 bytes。CDW0 包含 OPC、FUSE、PSDT、CID；NSID 指定目標 namespace；MPTR 與 DPTR 描述 metadata 及資料的位置；CDW10～15 則由各命令定義用途。</p>
<span class="qa-anchor" id="q-031-a-05"></span><p>先選定命令集，查明 Opcode 及支援能力，再設定合法的 NSID 與命令參數。準備好資料及指標後，分配一個在同一 SQ 中尚未使用的 CID，最後提交命令。PCIe Admin 命令使用 PRP，不能任意改用 SGL。</p>
<span class="qa-anchor" id="q-031-a-06"></span><p>Host 透過 SQID 與 CID 將 completion 配對回原命令。Status 表示完成狀態；命令產生的資料或其他結果，則可能放在 Host buffer 或 CQE DW0／1，並不是全部都放在 Status 裡。</p>
</section>
<section class="qa-section" id="q-031-s-03" data-answer-section="3"><h3><span>3.</span> 判讀時要保留的條件</h3>
<span class="qa-anchor" id="q-031-a-07"></span><p>不支援的 Opcode 回報 Invalid Command Opcode（0/01h）。已定義欄位的值不合法時，通常回報 Invalid Field（0/02h）；如果該命令對此情況定義了專用 Status，則依專用規則處理。</p>
<span class="qa-anchor" id="q-031-a-16"></span><p>一起核對 Opcode 所屬的命令集、controller 宣告的能力，以及資料長度。即使 DPTR 位址合法，也不表示它描述的記憶體範圍足以容納這次傳輸的全部資料。</p>
</section>
</div>
<span class="qa-anchor" id="q-031-a-17"></span><span class="qa-anchor" id="q-031-a-08"></span><span class="qa-anchor" id="q-031-a-09"></span><span class="qa-anchor" id="q-031-a-10"></span><span class="qa-anchor" id="q-031-a-11"></span><span class="qa-anchor" id="q-031-a-12"></span><span class="qa-anchor" id="q-031-a-13"></span><span class="qa-anchor" id="q-031-a-14"></span><span class="qa-anchor" id="q-031-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-032" data-question="32" data-answer-kind="error"><h2><a class="qa-qid" href="#q-032">Q32</a> Reserved 欄位非零、不合法 Command Dword 組合或不支援 Opcode 應如何處理？</h2>
<p class="qa-prompt">先區分失敗條件，再判斷是否有規範明定的回報結果。</p>
<details class="qa-answer" id="q-032-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-032-a-01">必須分清楚「整個 bit 或欄位被標為 Reserved」與「已定義欄位中的某個編碼值被保留」這兩種情況。它們對 controller 的檢查要求不同，不能一律要求保留位非零就必須報錯。</p><div class="qa-sections">
<section class="qa-section" id="q-032-s-01" data-answer-section="1"><h3><span>1.</span> 先區分是哪一種失敗</h3>
<span class="qa-anchor" id="q-032-a-02"></span><p>Host 如何填寫命令，以及 controller 必須檢查哪些內容，是兩組不同的義務。Host 填錯欄位，不一定代表 controller 也有義務偵測該錯誤。</p>
<span class="qa-anchor" id="q-032-a-04"></span><p>Host 必須將 Reserved 欄位清零，但接收端不必檢查 Reserved bits、bytes 或 fields。另一種情況是：欄位本身已有定義，Host 卻填入其中保留不用的編碼；對這種保留編碼，controller 必須報錯。</p>
<span class="qa-anchor" id="q-032-a-07"></span><p>不支援或保留的 Opcode 回報 0/01h；已定義欄位中的非法值，一般回報 0/02h，除非另有專用 Status。多個錯誤同時存在時，通常可以選擇其中一種回報。因此，不能把「Reserved bit 非零」一律判定為必須回報 0/02h。</p>
</section>
<section class="qa-section" id="q-032-s-02" data-answer-section="2"><h3><span>2.</span> 用哪些資料確認原因</h3>
<span class="qa-anchor" id="q-032-a-03"></span><p>查 Base §1.4.1 的 reserved 定義、Opcode 支援與每個命令的欄位限制。</p>
<span class="qa-anchor" id="q-032-a-05"></span><p>Host 可先將 SQE 全部清零，再填入命令實際使用的欄位。驗證錯誤處理時，每次只改一項條件，並記錄規範對該條件使用的是 shall 還是 should，避免把建議要求當成強制要求。</p>
</section>
<section class="qa-section" id="q-032-s-03" data-answer-section="3"><h3><span>3.</span> 結果與後續驗證</h3>
<span class="qa-anchor" id="q-032-a-06"></span><p>合法的欄位組合應依命令定義正常處理。如果 controller 沒有檢查某個 Reserved bit，也不能因此推論 Host 將該 bit 寫成非零就是合法用法。</p>
<span class="qa-anchor" id="q-032-a-16"></span><p>驗證紀錄應分別說明：Host 是否違反填寫規則，以及 controller 是否有義務偵測這項錯誤。只有把兩者分開，才不會將規範允許不檢查的情況，誤判成韌體缺陷。</p>
<span class="qa-anchor" id="q-032-a-17"></span><p>先問改到的是「保留位」還是「已定義欄位中的保留編碼」。</p>
</section>
</div>
<span class="qa-anchor" id="q-032-a-08"></span><span class="qa-anchor" id="q-032-a-09"></span><span class="qa-anchor" id="q-032-a-10"></span><span class="qa-anchor" id="q-032-a-11"></span><span class="qa-anchor" id="q-032-a-12"></span><span class="qa-anchor" id="q-032-a-13"></span><span class="qa-anchor" id="q-032-a-14"></span><span class="qa-anchor" id="q-032-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-conventions">Base 2.4 §1.4.1</a> · <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-033" data-question="33" data-answer-kind="error"><h2><a class="qa-qid" href="#q-033">Q33</a> NSID 不存在、Inactive、不適用或錯誤使用 Broadcast NSID 時，應回傳什麼類型的 Status？</h2>
<p class="qa-prompt">先區分失敗條件，再判斷是否有規範明定的回報結果。</p>
<details class="qa-answer" id="q-033-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-033-a-01">命令指定的 namespace 不存在、尚未對此 controller 啟用，以及命令根本不使用 NSID，是不同情況。先分清楚原因，才能選對 Status。</p><div class="qa-sections">
<section class="qa-section" id="q-033-s-01" data-answer-section="1"><h3><span>1.</span> 先區分是哪一種失敗</h3>
<span class="qa-anchor" id="q-033-a-02"></span><p>namespace 是否為 active，是相對於接收命令的 controller 而言。它可以經由另一個 controller 存取，不代表目前這個 controller 也能存取它。</p>
<span class="qa-anchor" id="q-033-a-04"></span><p>NSID=0、有效且已配置的 NSID、inactive NSID，以及 FFFFFFFFh，必須依命令規則分別判讀。尤其 FFFFFFFFh 影響哪些 namespace，要看各命令自己的定義，不能一律視為同一種廣播範圍。</p>
<span class="qa-anchor" id="q-033-a-07"></span><p>依 Figure 93 的一般規則，使用 NSID 的命令若指定 inactive namespace，回報 Invalid Field（0/02h）；若指定無效 NSID，則回報 Invalid Namespace or Format（0/0Bh）。命令不支援 broadcast 卻填入 FFFFFFFFh，或命令不使用 NSID 卻填入非零值時，回報 0/02h。若命令另有明確例外，則優先依例外規則處理。</p>
</section>
<section class="qa-section" id="q-033-s-02" data-answer-section="2"><h3><span>2.</span> 用哪些資料確認原因</h3>
<span class="qa-anchor" id="q-033-a-03"></span><p>先用 Active 與 Allocated Namespace ID List 確認狀態，再查該命令如何使用 NSID，以及是否定義了例外處理。</p>
<span class="qa-anchor" id="q-033-a-05"></span><p>先確認命令是否使用 NSID，再確認它是否允許目前的 namespace 狀態及 broadcast 用法。例如，Identify 的某些 CNS 本來就是查詢 allocated 或 inactive namespace，不能直接套用一般 I/O 命令的限制。</p>
</section>
<section class="qa-section" id="q-033-s-03" data-answer-section="3"><h3><span>3.</span> 結果與後續驗證</h3>
<span class="qa-anchor" id="q-033-a-06"></span><p>目標合法時，依該命令的定義完成處理。有些查詢對不存在或 inactive namespace 定義了特殊回覆，因此必須先看命令本身的規則，再使用通用 Status 表。</p>
<span class="qa-anchor" id="q-033-a-16"></span><p>一起核對原 SQE 的 NSID、提交當時的 active list，以及該 CNS、FID 或 Opcode 的使用規則。namespace 狀態之後可能改變，不能只拿現在的清單解釋過去命令的結果。</p>
<span class="qa-anchor" id="q-033-a-17"></span><p>先查命令是否真的屬於 Figure 93 的一般情況，或已有明確例外。</p>
</section>
</div>
<span class="qa-anchor" id="q-033-a-08"></span><span class="qa-anchor" id="q-033-a-09"></span><span class="qa-anchor" id="q-033-a-10"></span><span class="qa-anchor" id="q-033-a-11"></span><span class="qa-anchor" id="q-033-a-12"></span><span class="qa-anchor" id="q-033-a-13"></span><span class="qa-anchor" id="q-033-a-14"></span><span class="qa-anchor" id="q-033-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-034" data-question="34" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-034">Q34</a> CQE 中的 SQHD、SQID、CID、Phase Tag 及 Status 分別有什麼用途？</h2>
<p class="qa-prompt">先試著說明欄位的單位與編碼，再用一組數值推導結果。</p>
<details class="qa-answer" id="q-034-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-034-a-01">一筆 CQE 同時提供命令結果、原命令身分與 queue 進度；這些欄位不能彼此代替。</p><div class="qa-sections">
<section class="qa-section" id="q-034-s-01" data-answer-section="1"><h3><span>1.</span> 先確認資料的來源與範圍</h3>
<span class="qa-anchor" id="q-034-a-02"></span><p>SQHD 描述的是 SQID 指定之 SQ 的進度；P 用來辨識目前 CQ 位置中的資料是否有效；Status 則是 SQID 與 CID 指定之命令的結果。三者描述的對象不同。</p>
<span class="qa-anchor" id="q-034-a-03"></span><p>判讀時使用目前的 queue 配置及 CQE 公共格式。SQHD 的意義由格式定義，不會因某個 Feature 的選擇而改變。</p>
</section>
<section class="qa-section" id="q-034-s-02" data-answer-section="2"><h3><span>2.</span> 欄位、單位與判讀例子</h3>
<span class="qa-anchor" id="q-034-a-04"></span><p>DW2：SQHD、SQID；DW3：CID、P、Status；DW0／1 是命令特定結果。SQHD 表示建立 CQE 當時已消費的位置。</p>
<span class="qa-anchor" id="q-034-a-05"></span><p>先以 P 確認 CQE 有效，再透過 SQID 與 CID 找到原命令，解析 Status 及其他結果。接著更新 SQ 可用位置的紀錄，最後釋放這筆 CQE 所占的位置。</p>
<span class="qa-anchor" id="q-034-a-06"></span><p>例如，一筆 completion 回報 SQHD=8，只表示 controller 的 SQ Head 已前進到 8。它不表示原先放在索引 0～7 的所有命令，都已經執行完成。</p>
</section>
<section class="qa-section" id="q-034-s-03" data-answer-section="3"><h3><span>3.</span> 判讀時要保留的條件</h3>
<span class="qa-anchor" id="q-034-a-07"></span><p>解析 Status 時，必須一起讀取 SCT 與 SC；P 不屬於錯誤碼。如果 CQE 格式異常或 CID 無法對回命令，先檢查記憶體內容及 queue 是否已重建，不要替這類現象自行定義新的 NVMe Status。</p>
<span class="qa-anchor" id="q-034-a-16"></span><p>分別確認 SQHD 的進度、命令是否完成，以及資料 buffer 何時可以回收。SQ 位置已可重用，只表示 controller 已消費該 SQE，不表示 Host 可以提前釋放命令仍在使用的資料 buffer。</p>
</section>
</div>
<span class="qa-anchor" id="q-034-a-17"></span><span class="qa-anchor" id="q-034-a-08"></span><span class="qa-anchor" id="q-034-a-09"></span><span class="qa-anchor" id="q-034-a-10"></span><span class="qa-anchor" id="q-034-a-11"></span><span class="qa-anchor" id="q-034-a-12"></span><span class="qa-anchor" id="q-034-a-13"></span><span class="qa-anchor" id="q-034-a-14"></span><span class="qa-anchor" id="q-034-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-035" data-question="35" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-035">Q35</a> Status Code Type 與 Status Code 應如何解析？</h2>
<p class="qa-prompt">先試著說明欄位的單位與編碼，再用一組數值推導結果。</p>
<details class="qa-answer" id="q-035-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-035-a-01">同一個 SC 數值在不同 SCT 有不同意義，必須用成對值判讀。</p><div class="qa-sections">
<section class="qa-section" id="q-035-s-01" data-answer-section="1"><h3><span>1.</span> 先確認資料的來源與範圍</h3>
<span class="qa-anchor" id="q-035-a-02"></span><p>Status 是這一筆命令的完成狀態。解讀時還要搭配 Opcode、所屬命令集及當時的錯誤條件，才能知道這個結果代表什麼。</p>
<span class="qa-anchor" id="q-035-a-03"></span><p>公共 SCT／SC 定義在 Base；NVM 命令特有的狀態則由 NVM Command Set 補充。查表時必須使用對應命令集的定義，不能拿另一種命令集的同一數值來解釋。</p>
</section>
<section class="qa-section" id="q-035-s-02" data-answer-section="2"><h3><span>2.</span> 欄位、單位與判讀例子</h3>
<span class="qa-anchor" id="q-035-a-04"></span><p>在 CQE DW3 中 SCT=bits27:25、SC=24:17，P=16；若程式先取最後 16-bit word，SCT 位置變為 11:9、SC 為 8:1。</p>
<span class="qa-anchor" id="q-035-a-05"></span><p>先確認程式讀取的資料寬度及位元組順序，再取出 SCT 與 SC，查閱對應的 Status 表。之後再解讀 DNR、More、CRD 及命令特定的結果欄位。</p>
<span class="qa-anchor" id="q-035-a-06"></span><p>SCT=0、SC=00h 表示 Successful Completion。不過，Host 仍須先確認 P 有效，而且 SQID 與 CID 能對回原命令；不能只因部分低位元為零，就認定讀到了一筆新的成功完成。</p>
</section>
<section class="qa-section" id="q-035-s-03" data-answer-section="3"><h3><span>3.</span> 判讀時要保留的條件</h3>
<span class="qa-anchor" id="q-035-a-07"></span><p>例：0/01h 是 Invalid Command Opcode；1/01h 是 Invalid Queue Identifier。SCT=2 為 Media and Data Integrity，3 為 Path Related，7 為 Vendor Specific。</p>
<span class="qa-anchor" id="q-035-a-16"></span><p>驗證時同時保留原始 CQE bytes 與解碼後的欄位值。有些工具會先移除 P，或重新排列 Status 的位元，因此不同工具輸出的整數，不能在未確認格式前直接比較。</p>
</section>
</div>
<span class="qa-anchor" id="q-035-a-17"></span><span class="qa-anchor" id="q-035-a-08"></span><span class="qa-anchor" id="q-035-a-09"></span><span class="qa-anchor" id="q-035-a-10"></span><span class="qa-anchor" id="q-035-a-11"></span><span class="qa-anchor" id="q-035-a-12"></span><span class="qa-anchor" id="q-035-a-13"></span><span class="qa-anchor" id="q-035-a-14"></span><span class="qa-anchor" id="q-035-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-036" data-question="36" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-036">Q36</a> More 與 Do Not Retry 位元分別代表什麼？DNR 為 0 是否代表一定能直接重試？</h2>
<p class="qa-prompt">先用自己的話解釋機制，再舉一個常見誤解。</p>
<details class="qa-answer" id="q-036-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-036-a-01">判讀重試時，有三個問題要分開：相同命令是否可能成功、是否有補充錯誤資訊，以及再次執行是否安全。DNR 與 More 不能單獨回答全部問題。</p><div class="qa-sections">
<section class="qa-section" id="q-036-s-01" data-answer-section="1"><h3><span>1.</span> 機制與適用範圍</h3>
<span class="qa-anchor" id="q-036-a-02"></span><p>DNR 與 More 都針對目前這筆 CQE。DNR 所說的「重試相同命令」，也包含改由同一 NVM subsystem 的其他 controller 提交，不能只換 controller 就忽略它的含義。</p>
<span class="qa-anchor" id="q-036-a-04"></span><p>DNR 不表示命令一定尚未修改資料。More=1 則表示 Error Information Log（LID 01h）包含這筆命令的額外 Status 資訊，不是表示後面還會有另一筆 completion。</p>
</section>
<section class="qa-section" id="q-036-s-02" data-answer-section="2"><h3><span>2.</span> 用操作與結果理解</h3>
<span class="qa-anchor" id="q-036-a-03"></span><p>這些公共位元固定存在於 CQE 格式中。若要使用 CRD 指示的重試延遲，還需確認 Host Behavior Support.ACRE，以及 Identify.CRDT1～3 的設定與數值。</p>
<span class="qa-anchor" id="q-036-a-05"></span><p>先分析錯誤原因。若 DNR=0，應處理暫時性的失敗條件，依有效的 CRD 等待，再判斷能否安全重送。若同一操作執行兩次可能產生不同結果，還要先確認前一次操作是否已經生效，避免重複作用。</p>
<span class="qa-anchor" id="q-036-a-06"></span><p>重試是否成功，必須看重試命令的新 CQE。DNR=0 只表示重試可能成功，不保證立刻重送就會成功，也不保證再次執行不會造成重複作用。</p>
</section>
<section class="qa-section" id="q-036-s-03" data-answer-section="3"><h3><span>3.</span> 容易誤判的地方</h3>
<span class="qa-anchor" id="q-036-a-07"></span><p>若命令因參數非法而失敗，卻完全不修改參數就重送，通常無法解決問題。對明確規定 DNR 的 Status，則必須遵守該規則；例如 Command Interrupted（0/21h）要求 DNR=0，而且只有在 ACRE 已啟用時才能回報。</p>
<span class="qa-anchor" id="q-036-a-16"></span><p>More=1 時，應能在 Error Information Log 中找到可與此命令關聯的額外資訊。CRD 是否有效，則必須搭配 DNR 與 ACRE 判斷，不能只看到非零值就直接使用。</p>
</section>
</div>
<span class="qa-anchor" id="q-036-a-17"></span><span class="qa-anchor" id="q-036-a-08"></span><span class="qa-anchor" id="q-036-a-09"></span><span class="qa-anchor" id="q-036-a-10"></span><span class="qa-anchor" id="q-036-a-11"></span><span class="qa-anchor" id="q-036-a-12"></span><span class="qa-anchor" id="q-036-a-13"></span><span class="qa-anchor" id="q-036-a-14"></span><span class="qa-anchor" id="q-036-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-behavior">Base 2.4 §5.2.30.1.15</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-037" data-question="37" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-037">Q37</a> Completion 已寫入但 Host 未處理，可能與 Phase Tag、CQ 位置或 Interrupt 有什麼關係？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-037-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-037-a-01">controller 已寫入 completion、Host 已收到中斷通知，以及 Host 已處理 CQE，是三個不同階段。前一階段完成，不代表後一階段也已完成。</p><div class="qa-sections">
<section class="qa-section" id="q-037-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-037-a-02"></span><p>需要檢查目標 CQ 的記憶體、Host 維護的 Head 與期待 Phase，以及這條 CQ 使用的中斷。Host 尚未處理結果，不一定表示命令執行失敗。</p>
<span class="qa-anchor" id="q-037-a-03"></span><p>確認 Create CQ.IEN／IV、使用的 MSI 或 MSI-X 模式、mask 與中斷 Feature。</p>
<span class="qa-anchor" id="q-037-a-04"></span><p>使用 MSI-X 時，檢查 Function Mask、vector mask 與 PBA；使用一般 MSI 時，則依 INTMS／INTMC 的規則判斷。無論中斷如何設定，CQE 是否有效仍由正確的 CQ 位置與 Phase 決定。</p>
</section>
<section class="qa-section" id="q-037-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-037-a-17"></span><p>先確認 Host 是否讀錯 CQ、讀錯位置，或使用錯誤的期待 Phase。這些資訊能直接判斷 CQE 是否被漏讀，再進一步追查中斷路徑。</p>
<span class="qa-anchor" id="q-037-a-05"></span><p>先確認 Host 讀取的是正確 CQ 的目前 Head，再檢查 P。有有效的新 CQE 就應處理；如果問題是沒有收到中斷，再檢查 IEN、IV、mask、coalescing 設定及 Host 的中斷處理程式。</p>
</section>
<section class="qa-section" id="q-037-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-037-a-06"></span><p>Host 可以透過輪詢處理合法的 CQE，即使這筆完成沒有各自對應一個中斷。中斷可能合併通知，因此中斷數量不必等於 completion 數量。</p>
<span class="qa-anchor" id="q-037-a-07"></span><p>沒有收到中斷，本身不對應某個 NVMe 錯誤 Status，原來的 CQE 甚至可能表示成功。不能只因中斷未到達，就判定 controller 應回報 Internal Error。</p>
<span class="qa-anchor" id="q-037-a-16"></span><p>比對 CQE 寫入、mask 變更、中斷到達及 Head 更新的時間。中斷負責通知 Host；真正的命令結果仍在 CQE 中。</p>
</section>
</div>
<span class="qa-anchor" id="q-037-a-08"></span><span class="qa-anchor" id="q-037-a-09"></span><span class="qa-anchor" id="q-037-a-10"></span><span class="qa-anchor" id="q-037-a-11"></span><span class="qa-anchor" id="q-037-a-12"></span><span class="qa-anchor" id="q-037-a-13"></span><span class="qa-anchor" id="q-037-a-14"></span><span class="qa-anchor" id="q-037-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-irq">PCIe Transport 1.4 §3.5</a> · <a href="#ref-irqfeat">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-038" data-question="38" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-038">Q38</a> 多個 Command 同時 Outstanding 時，Controller 是否必須按照提交順序完成？</h2>
<p class="qa-prompt">先用自己的話解釋機制，再舉一個常見誤解。</p>
<details class="qa-answer" id="q-038-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-038-a-01">SQ 保留命令的提交順序，但這不表示 controller 必須依相同順序執行或完成所有命令。理解這個差別，才能正確建立命令之間的依賴。</p><div class="qa-sections">
<section class="qa-section" id="q-038-s-01" data-answer-section="1"><h3><span>1.</span> 哪些階段有順序，哪些沒有</h3>
<span class="qa-anchor" id="q-038-a-02"></span><p>一般互不相依的命令，即使放在同一條 SQ，也不能假設先提交就一定先完成。來自不同 SQ 的命令，更不能只因提交時間接近，就推論它們有先後保證。</p>
<span class="qa-anchor" id="q-038-a-03"></span><p>先看命令是否屬 fused operation 或有專屬順序規則；FUSES 表示 fused 支援。</p>
<span class="qa-anchor" id="q-038-a-04"></span><p>應分清楚命令已提交、SQE 已被消費、命令開始處理，以及命令已完成這四個階段。SQHD 只反映 SQE 已被消費的進度，不直接表示命令已完成。</p>
</section>
<section class="qa-section" id="q-038-s-02" data-answer-section="2"><h3><span>2.</span> 有相依關係時，Host 要怎麼做</h3>
<span class="qa-anchor" id="q-038-a-05"></span><p>如果命令 B 需要使用命令 A 的結果，Host 應等 A 成功完成後才提交 B。如果還要求資料已持久保存，則要另外依 Flush 或 FUA 的規則處理，不能只靠提交順序保證。</p>
<span class="qa-anchor" id="q-038-a-06"></span><p>若 Read A 與 Read B 沒有相依關係，較晚提交的 B 先完成可以是合法行為。Host 必須依 SQID 與 CID 配對結果，不能假設 completion 會按照提交陣列的順序回來。</p>
<span class="qa-anchor" id="q-038-a-07"></span><p>單純以相反順序完成，不構成某個錯誤 Status。只有違反規範明定的多命令先後規則時，才依該序列的專用錯誤條件判斷。</p>
<span class="qa-anchor" id="q-038-a-16"></span><p>驗證時，應指出命令之間實際要求哪一種先後關係，再檢查結果是否符合。只說「看起來沒有依序完成」，不足以判定不符合規範。</p>
</section>
</div>
<span class="qa-anchor" id="q-038-a-17"></span><span class="qa-anchor" id="q-038-a-08"></span><span class="qa-anchor" id="q-038-a-09"></span><span class="qa-anchor" id="q-038-a-10"></span><span class="qa-anchor" id="q-038-a-11"></span><span class="qa-anchor" id="q-038-a-12"></span><span class="qa-anchor" id="q-038-a-13"></span><span class="qa-anchor" id="q-038-a-14"></span><span class="qa-anchor" id="q-038-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-nvmatomic">NVM Command Set 1.3 §2.1.2–2.1.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-039" data-question="39" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-039">Q39</a> 哪些 Command 具有順序相依性？Host 為什麼不能假設所有 Command 都依序完成？</h2>
<p class="qa-prompt">先用自己的話解釋機制，再舉一個常見誤解。</p>
<details class="qa-answer" id="q-039-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-039-a-01">Host 必須明確建立真正需要的命令依賴。把命令依序放入 queue，不會自動得到一組不可分割、依序完成的操作。</p><div class="qa-sections">
<section class="qa-section" id="q-039-s-01" data-answer-section="1"><h3><span>1.</span> 機制與適用範圍</h3>
<span class="qa-anchor" id="q-039-a-02"></span><p>例如，先成功建立 CQ，才能建立使用它的 SQ；刪除時則先刪 SQ，再刪 CQ。另一類例子是等 Set Features 成功後，再提交需要使用新設定的命令。支援的 fused pair 則有自己的成對提交規則。</p>
<span class="qa-anchor" id="q-039-a-04"></span><p>FUSE=01b／10b 表示成對第一／第二筆；PCIe 中必須在同一 SQ 相鄰並用同一次 Tail 更新提交。</p>
</section>
<section class="qa-section" id="q-039-s-02" data-answer-section="2"><h3><span>2.</span> 用操作與結果理解</h3>
<span class="qa-anchor" id="q-039-a-03"></span><p>分別查閱 FUSES、使用中的 Feature，以及相關命令的順序要求。不存在一個通用能力位，可以替所有命令建立相同的順序保證。</p>
<span class="qa-anchor" id="q-039-a-05"></span><p>一般命令的相依關係，可以透過等待前一筆 completion 來建立；fused pair 則必須依專用規則一起提交，而且兩筆命令各自有 CQE。不能將兩筆相依命令同時送出後，就假設 controller 會自動安排成 Host 想要的順序。</p>
<span class="qa-anchor" id="q-039-a-06"></span><p>Set Features 成功後才提交的命令，使用新的設定；在此之前已提交的命令，則可能使用舊值或新值。如果驗證需要排除這種差異，應先等待既有命令完成，再變更設定。</p>
</section>
<section class="qa-section" id="q-039-s-03" data-answer-section="3"><h3><span>3.</span> 容易誤判的地方</h3>
<span class="qa-anchor" id="q-039-a-07"></span><p>缺少相鄰的 fused partner 時，回報 Command Aborted due to Missing Fused Command（0/0Ah）。CQ 與 SQ 的建立或刪除順序錯誤，則依各自的 Create／Delete Status 處理，不能全部套用 0/0Ch。</p>
<span class="qa-anchor" id="q-039-a-16"></span><p>在時間線上標出前一步 completion 與下一步 submission，確認 Host 確實建立了必要的先後關係。FUA 控制的是資料持久性，不能替代這些命令之間的依賴。</p>
</section>
</div>
<span class="qa-anchor" id="q-039-a-17"></span><span class="qa-anchor" id="q-039-a-08"></span><span class="qa-anchor" id="q-039-a-09"></span><span class="qa-anchor" id="q-039-a-10"></span><span class="qa-anchor" id="q-039-a-11"></span><span class="qa-anchor" id="q-039-a-12"></span><span class="qa-anchor" id="q-039-a-13"></span><span class="qa-anchor" id="q-039-a-14"></span><span class="qa-anchor" id="q-039-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-nvmatomic">NVM Command Set 1.3 §2.1.2–2.1.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-040" data-question="40" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-040">Q40</a> Outstanding Command 達到限制或 CQ Full 時，Controller 如何限制取得新 Command？</h2>
<p class="qa-prompt">先用自己的話解釋機制，再舉一個常見誤解。</p>
<details class="qa-answer" id="q-040-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-040-a-01">必須分清楚三種限制：SQ 還能放多少命令、controller 內部還有多少執行資源，以及 CQ 還能放多少完成結果。單用一個 queue depth 數字，無法解釋所有停滯原因。</p><div class="qa-sections">
<section class="qa-section" id="q-040-s-01" data-answer-section="1"><h3><span>1.</span> 機制與適用範圍</h3>
<span class="qa-anchor" id="q-040-a-02"></span><p>限制可針對 SQ、共享 CQ 或 controller 內部資源；不是每個限制都代表整個 controller 失效。</p>
<span class="qa-anchor" id="q-040-a-04"></span><p>controller 如何從已提交的 SQE 取得命令，由廠商實作決定；仲裁則決定從哪條 SQ 選出候選命令，開始處理。取得 SQE 與開始執行命令，仍是不同動作。</p>
</section>
<section class="qa-section" id="q-040-s-02" data-answer-section="2"><h3><span>2.</span> 用操作與結果理解</h3>
<span class="qa-anchor" id="q-040-a-03"></span><p>Host 根據 queue 大小及 SQHD 追蹤可用位置，同時維持未完成命令的 CID 唯一性。其他 transport 使用的 MAXCMD 流量控制假設，不能直接套用到 PCIe。</p>
<span class="qa-anchor" id="q-040-a-05"></span><p>Host 不得覆寫 controller 尚未消費的 SQE；controller 也不得向已滿的 CQ 寫入 completion。必要時，controller 可以停止處理關聯 SQ 的更多命令，但使用其他獨立 CQ 的 SQ 仍須繼續處理。</p>
<span class="qa-anchor" id="q-040-a-06"></span><p>空間釋放後，處理可以繼續。SQ 的某個位置已經可用，但原先放在那裡的命令仍未完成，是可能發生的情況，因為取得 SQE 不等於完成命令。</p>
</section>
<section class="qa-section" id="q-040-s-03" data-answer-section="3"><h3><span>3.</span> 容易誤判的地方</h3>
<span class="qa-anchor" id="q-040-a-07"></span><p>正常達到資源限制，不表示 controller 必須回報錯誤 CQE。如果 Host 違反 queue 指標規則、重用未完成命令的 CID，或超過某類命令的專用限制，才依各項錯誤規則處理。</p>
<span class="qa-anchor" id="q-040-a-16"></span><p>分別收集提交、取得、開始處理及完成的證據。只看到 Host 已提交多少筆命令，不能推論 controller 已同時開始執行全部命令。</p>
</section>
</div>
<span class="qa-anchor" id="q-040-a-17"></span><span class="qa-anchor" id="q-040-a-08"></span><span class="qa-anchor" id="q-040-a-09"></span><span class="qa-anchor" id="q-040-a-10"></span><span class="qa-anchor" id="q-040-a-11"></span><span class="qa-anchor" id="q-040-a-12"></span><span class="qa-anchor" id="q-040-a-13"></span><span class="qa-anchor" id="q-040-a-14"></span><span class="qa-anchor" id="q-040-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-041" data-question="41" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-041">Q41</a> Round Robin 與 Weighted Round Robin Arbitration 有什麼差異？</h2>
<p class="qa-prompt">先說出比較對象最重要的差別，並舉一個不能互相代用的例子。</p>
<details class="qa-answer" id="q-041-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-041-a-01">多條 SQ 同時有可處理的命令時，仲裁決定下一批從哪條 SQ 開始處理。不同仲裁方式也讓 Host 能表達各 SQ 希望取得的服務優先順序。</p><div class="qa-sections">
<section class="qa-section" id="q-041-s-01" data-answer-section="1"><h3><span>1.</span> 差別在哪裡</h3>
<span class="qa-anchor" id="q-041-a-02"></span><p>仲裁影響的是哪些候選命令先開始處理，不保證 completion 的回報順序，也不保證量測到固定的 IOPS 比例。</p>
<span class="qa-anchor" id="q-041-a-04"></span><p>FID 01h 提供 Arbitration Burst（AB）及 HPW／MPW／LPW；SQ.QPRIO 在 WRR 生效。AB=7 表示不限 burst，其他值為 2^AB；權重為欄位值+1。</p>
</section>
<section class="qa-section" id="q-041-s-02" data-answer-section="2"><h3><span>2.</span> 如何選擇與確認</h3>
<span class="qa-anchor" id="q-041-a-03"></span><p>所有 controller 都支援 Round Robin。若要使用選配的 Weighted Round Robin（WRR），先查 CAP.AMS 確認支援，再透過 CC.AMS 選用。</p>
<span class="qa-anchor" id="q-041-a-05"></span><p>在 controller 停用時選定 CC.AMS。啟用後設定 FID 01h，並在建立 SQ 時設定 QPRIO。驗證時，持續提供可執行的命令，觀察 controller 如何選擇開始處理的 SQ。</p>
<span class="qa-anchor" id="q-041-a-06"></span><p>Round Robin 讓各 SQ 輪流獲得處理機會，Admin SQ 也包含在內。WRR 則先處理 Admin，再處理 Urgent，之後依權重分配 High、Medium、Low；同一類別內仍有輪流選擇的規則。</p>
</section>
<section class="qa-section" id="q-041-s-03" data-answer-section="3"><h3><span>3.</span> 哪些結論不能互相套用</h3>
<span class="qa-anchor" id="q-041-a-07"></span><p>若將 CC.AMS 設為不支援的值，該 Register 操作的結果未定義，不能要求回傳 Set Features 的 Invalid Field。若是 FID 01h 中已定義的參數值非法，則依 Set Features 的命令規則處理。</p>
<span class="qa-anchor" id="q-041-a-16"></span><p>Get Features 讀回 FID 01h，只能證明目前設定值。命令執行時間、媒體資源衝突及 CQ 空間也會影響吞吐量，因此不能只看 IOPS 比例，就判定 WRR 是否正確。</p>
</section>
</div>
<span class="qa-anchor" id="q-041-a-17"></span><span class="qa-anchor" id="q-041-a-08"></span><span class="qa-anchor" id="q-041-a-09"></span><span class="qa-anchor" id="q-041-a-10"></span><span class="qa-anchor" id="q-041-a-11"></span><span class="qa-anchor" id="q-041-a-12"></span><span class="qa-anchor" id="q-041-a-13"></span><span class="qa-anchor" id="q-041-a-14"></span><span class="qa-anchor" id="q-041-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-arbit">Base 2.4 §5.2.30.1.1</a> · <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-042" data-question="42" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-042">Q42</a> Urgent、High、Medium 及 Low Queue Priority 在哪些情況下生效？</h2>
<p class="qa-prompt">先用自己的話解釋機制，再舉一個常見誤解。</p>
<details class="qa-answer" id="q-042-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-042-a-01">Queue Priority 用來讓不同 SQ 取得不同的服務機會，但只有在選用對應仲裁機制時，這項設定才會生效。</p><div class="qa-sections">
<section class="qa-section" id="q-042-s-01" data-answer-section="1"><h3><span>1.</span> 機制與適用範圍</h3>
<span class="qa-anchor" id="q-042-a-02"></span><p>QPRIO 是 SQ 層級設定，不是每筆 Read／Write 的 priority 欄位。</p>
<span class="qa-anchor" id="q-042-a-04"></span><p>Create SQ CDW11.QPRIO：00b Urgent、01b High、10b Medium、11b Low；FID 01h 為後三種設定權重。</p>
</section>
<section class="qa-section" id="q-042-s-02" data-answer-section="2"><h3><span>2.</span> 用操作與結果理解</h3>
<span class="qa-anchor" id="q-042-a-03"></span><p>CAP.AMS 支援 WRR 且 CC.AMS 已選 WRR 才使用 QPRIO；否則 controller 必須忽略它。</p>
<span class="qa-anchor" id="q-042-a-05"></span><p>Host 可依工作類型建立不同 SQ，並設定各自的 QPRIO。若要改變既有 SQ 的這項屬性，需依 queue 重建流程處理；修改 Host 記憶體中已提交過的 Create SQE，不會改變現有 SQ 的設定。</p>
<span class="qa-anchor" id="q-042-a-06"></span><p>Urgent 的優先順序高於 High、Medium、Low，但低於 Admin。若 Urgent 工作持續不斷，較低類別可能長時間得不到處理機會，因此不能假設 High 一定享有固定的最低頻寬。</p>
</section>
<section class="qa-section" id="q-042-s-03" data-answer-section="3"><h3><span>3.</span> 容易誤判的地方</h3>
<span class="qa-anchor" id="q-042-a-07"></span><p>Round Robin 模式下，controller 忽略 QPRIO 是合法行為，不能因此判定優先級功能失效。若 queue 參數本身非法，仍依 Create Queue 的 Status 規則處理。</p>
<span class="qa-anchor" id="q-042-a-16"></span><p>驗證時一起記錄每條 SQ 的 QPRIO、CC.AMS 及 FID 01h。只有優先級而不知道仲裁模式，或只有模式而不知道權重，都不足以解釋實際選擇順序。</p>
</section>
</div>
<span class="qa-anchor" id="q-042-a-17"></span><span class="qa-anchor" id="q-042-a-08"></span><span class="qa-anchor" id="q-042-a-09"></span><span class="qa-anchor" id="q-042-a-10"></span><span class="qa-anchor" id="q-042-a-11"></span><span class="qa-anchor" id="q-042-a-12"></span><span class="qa-anchor" id="q-042-a-13"></span><span class="qa-anchor" id="q-042-a-14"></span><span class="qa-anchor" id="q-042-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-arbit">Base 2.4 §5.2.30.1.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-043" data-question="43" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-043">Q43</a> 多個 Queue 競爭資源時，如何判斷 Arbitration 是否符合設定？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-043-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-043-a-01">判斷仲裁是否符合規範，需要觀察 controller 如何選擇開始處理的命令。延遲或吞吐量有差異，不一定表示選擇規則遭到違反。</p><div class="qa-sections">
<section class="qa-section" id="q-043-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-043-a-02"></span><p>比較同一 controller 上互相競爭的 SQ，並先排除 CQ Full、命令相依、處理成本不同，以及 Host 沒有持續提供命令等干擾因素。</p>
<span class="qa-anchor" id="q-043-a-03"></span><p>記錄 CAP.AMS、CC.AMS、FID 01h 的 AB／權重及每條 SQ 的 QPRIO。</p>
<span class="qa-anchor" id="q-043-a-04"></span><p>WRR 在 High、Medium、Low 類別中，每輪能開始處理的命令數，受到剩餘服務額度及 AB 限制。因此，不只要看 SQ 是否非空，還要確認其中確實有可開始處理的候選命令。</p>
</section>
<section class="qa-section" id="q-043-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-043-a-17"></span><p>先確認高優先級 SQ 是否持續有可開始處理的命令，再確認關聯 CQ 沒有因空間已滿而阻塞。</p>
<span class="qa-anchor" id="q-043-a-05"></span><p>可用命令類型與大小相近、Host 持續提交，而且 CQ 不阻塞的情境來比較。若能取得開始處理或排程紀錄，就直接核對選擇順序；如果只有 CQE，則必須承認完成結果不足以還原全部內部排程。</p>
</section>
<section class="qa-section" id="q-043-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-043-a-06"></span><p>例如 High 與 Low 的權重為 4:1，描述的是分配服務額度的比例，不代表每個短時間區間內，完成命令數都必須剛好是 4:1。</p>
<span class="qa-anchor" id="q-043-a-07"></span><p>仲裁量測本身不會產生錯誤 CQE。應先確認設定命令成功，再對照規範中的 shall 與 may。如果測試期間沒有持續提供可處理的命令，就不宜單憑吞吐結果判定不符合規範。</p>
<span class="qa-anchor" id="q-043-a-16"></span><p>要判定違反規範，必須指出具體的選擇規則，以及哪一段觀察結果與它矛盾。只有「高優先級比較慢」的現象，還不足以完成這項判斷。</p>
</section>
</div>
<span class="qa-anchor" id="q-043-a-08"></span><span class="qa-anchor" id="q-043-a-09"></span><span class="qa-anchor" id="q-043-a-10"></span><span class="qa-anchor" id="q-043-a-11"></span><span class="qa-anchor" id="q-043-a-12"></span><span class="qa-anchor" id="q-043-a-13"></span><span class="qa-anchor" id="q-043-a-14"></span><span class="qa-anchor" id="q-043-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-arbit">Base 2.4 §5.2.30.1.1</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>

<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-conventions"><strong>Base 2.4 · §1.4.1</strong><br>文件頁 2–3 · PDF 28–29</li>
<li id="ref-cap"><strong>Base 2.4 · §3.1.4 (CAP, VS)</strong><br>文件頁 54–59 · PDF 80–85 · Figure 36–37</li>
<li id="ref-nsid"><strong>Base 2.4 · §3.2.1</strong><br>文件頁 78–81 · PDF 104–107</li>
<li id="ref-queue"><strong>Base 2.4 · §3.3.1</strong><br>文件頁 88–91 · PDF 114–117 · Figure 73–74</li>
<li id="ref-order"><strong>Base 2.4 · §3.4.1–3.4.5</strong><br>文件頁 101–105 · PDF 127–131 · Figure 80–81</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-sqe"><strong>Base 2.4 · §4.1.1</strong><br>文件頁 139–142 · PDF 165–168 · Figure 92–93</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>文件頁 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>文件頁 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-featureeffects"><strong>Base 2.4 · §5.2.13.1.18</strong><br>文件頁 276–278 · PDF 302–304 · Figure 270–271</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>文件頁 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>文件頁 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-arbit"><strong>Base 2.4 · §5.2.30.1.1</strong><br>文件頁 460 · PDF 486 · Figure 467</li>
<li id="ref-vwc"><strong>Base 2.4 · §5.2.30.1.4</strong><br>文件頁 464–465 · PDF 490–491 · Figure 471</li>
<li id="ref-behavior"><strong>Base 2.4 · §5.2.30.1.15</strong><br>文件頁 475–477 · PDF 501–503 · Figure 491</li>
<li id="ref-irqfeat"><strong>Base 2.4 · §5.2.30.2.1–5.2.30.2.2</strong><br>文件頁 514–515 · PDF 540–541 · Figure 543–544</li>
<li id="ref-create"><strong>Base 2.4 · §5.3.1–5.3.2</strong><br>文件頁 527–531 · PDF 553–557 · Figure 571–579</li>
<li id="ref-delete"><strong>Base 2.4 · §5.3.3–5.3.4</strong><br>文件頁 531–532 · PDF 557–558 · Figure 580–583</li>
<li id="ref-fatal"><strong>Base 2.4 · §9.1–9.6.1</strong><br>文件頁 825–826 · PDF 851–852</li>
<li id="ref-nvmatomic"><strong>NVM Command Set 1.3 · §2.1.2–2.1.4</strong><br>文件頁 14–20 · PDF 14–20 · Figure 3–9</li>
<li id="ref-pcie"><strong>PCIe Transport 1.4 · §3.1–3.4</strong><br>文件頁 9–13 · PDF 9–13 · Figure 3–8</li>
<li id="ref-irq"><strong>PCIe Transport 1.4 · §3.5</strong><br>文件頁 13–16 · PDF 13–16 · Figure 9</li>
</ul><h3>需要看欄位圖時</h3><p>以下連結可開啟對應的圖表教學，查閱欄位及判讀方式。每張圖保留固定的教學位置，方便之後反覆查詢。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="/nvme/figure-reference/features/zh-tw/#figure-b543">Base 2.4 Figure 543 · Interrupt Coalescing – Command Dword 11</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/commands/en/">English</a><a href="/DOCS/nvme-question-bank/commands.html">繁中教學 HTML</a></nav>
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
