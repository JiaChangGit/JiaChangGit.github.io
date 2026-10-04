---
layout: post
title: "NVMe 自問自答題庫：Format 與 Sanitize"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/format-sanitize/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/format-sanitize/en/">English</a><a href="/DOCS/nvme-question-bank/format-sanitize.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q118–Q135</p><h1>Format 與 Sanitize</h1><p class="qr-intro">Format 改變 namespace 格式；Sanitize 處理資料清除。兩者的範圍、完成點與 reset 行為不同，本冊以一次操作的前、中、後狀態逐步區分。</p><p>先練習，再展開每題的 17 項解答。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>三條操作路徑不能互換</h2><p class="qa-takeaway">支援 subsystem Overwrite，不代表支援 namespace Overwrite。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">操作</th><th scope="col">主要選擇</th><th scope="col">完成證據</th></tr></thead><tbody><tr><td>Format NVM</td><td>LBAF、metadata、PI、SES</td><td>Format CQE 與新格式</td></tr><tr><td>Subsystem Sanitize</td><td>SANACT、範圍與選項</td><td>啟動 CQE 後還看 LID81h</td></tr><tr><td>Namespace Sanitize</td><td>NSID、Crypto Erase</td><td>查目標 namespace 的狀態</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>SANICAP.OWS=1 只能證明相應的 subsystem Overwrite 能力。若要求清除單一 namespace，Base2.4 的 Sanitize Namespace 只允許 Crypto Erase，不能將 SANACT=3 照搬過去。</p>
<p class="qa-citations">來源：<a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-nvmformat">NVM Command Set 1.3 §4.1.2</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-118">Q118 · 如何查詢 Format、Sanitize 與 Sanitize Namespace 的支援能力？</a></li>
<li><a href="#q-119">Q119 · Format、Secure Erase、Subsystem Sanitize 與 Namespace Sanitize 有何差別？</a></li>
<li><a href="#q-120">Q120 · Format 如何選 LBA Format、Metadata、PI 與 SES？</a></li>
<li><a href="#q-121">Q121 · Format 的非法格式、參數與狀態如何回報？</a></li>
<li><a href="#q-122">Q122 · Format 期間哪些 Admin 操作可以繼續？</a></li>
<li><a href="#q-123">Q123 · Format 過程遇到 Reset 或斷電，如何判斷結果？</a></li>
<li><a href="#q-124">Q124 · Format 成功後哪些 Identify 與 Namespace 狀態要更新？</a></li>
<li><a href="#q-125">Q125 · Format 失敗時如何使用 CQE、Error Log 與 PEL？</a></li>
<li><a href="#q-126">Q126 · SANICAP 如何表示 Block Erase、Overwrite 與 Crypto Erase？</a></li>
<li><a href="#q-127">Q127 · NDAS、Overwrite Pattern、Pass Count 與反轉 Pattern 如何使用？</a></li>
<li><a href="#q-128">Q128 · SPROG、SOS、SANS 與 GDE／NDE 要怎麼一起看？</a></li>
<li><a href="#q-129">Q129 · Subsystem Sanitize 期間哪些 Command 允許執行？</a></li>
<li><a href="#q-130">Q130 · Sanitize 遇到 Reset 或 Power Loss 會繼續嗎？</a></li>
<li><a href="#q-131">Q131 · 成功、失敗與 Failure Mode 在 Log 中如何區分？</a></li>
<li><a href="#q-132">Q132 · Exit Failure Mode 能做什麼，不能做什麼？</a></li>
<li><a href="#q-133">Q133 · Sanitize 的 AER 與 PEL 應在何時產生？</a></li>
<li><a href="#q-134">Q134 · Namespace Sanitize 如何指定目標並確認其他 Namespace 未被清除？</a></li>
<li><a href="#q-135">Q135 · Namespace Sanitize 遇到不存在、Inactive 或不支援的目標如何回應？</a></li>
</ol></section>
<article class="qa-question" id="q-118" data-question="118"><h2><a class="qa-qid" href="#q-118">Q118</a> 如何查詢 Format、Sanitize 與 Sanitize Namespace 的支援能力？</h2>
<p class="qa-prompt">需求：只透過查詢，確認 controller 是否支援 Sanitize Namespace。先說明要找哪個 Opcode、讀哪個 Log、取哪個 entry，以及支援位元在哪裡，再展開解答。</p>
<details class="qa-answer" id="q-118-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-118-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>支援 Opcode、支援某種操作，以及當前允許執行，是三個要分開確認的問題。這能避免把「支援 Sanitize」誤讀成任何清除方法都可使用。</p>
</li>
<li id="q-118-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Format 的範圍由 FNA、SES 與 NSID 決定；Sanitize 和 Sanitize Namespace 則是不同命令、不同清除目標。</p>
</li>
<li id="q-118-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Format 查 OACS 與 FNA；Sanitize 查 SANICAP 的 CES、BES、OWS。要確認 Sanitize Namespace 命令本身，先由 Figure 28 找到 Admin Opcode 8Ch，再讀 LID05h 的對應 Admin entry，以 Figure 217 的 bit0（CSUPP）判讀。CSUPP 是命令支援宣告；SANICAP.CES、NVERS 則分別補充清除方法與 namespace 媒體驗證能力。</p>
<section class="qa-lookup" id="q-118-lookup"><h4>查詢範例：從 Sanitize Namespace 名稱找到 CSUPP</h4>
<p>以下回傳值都是教學假設。使用同一個 PCIe I/O controller、CC.CSS=000b 及 UUID Index=0；查詢成功後才解讀 buffer。Figure 28 是規格的命令清單，不是這台 SSD 的實測能力表。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">查詢步驟與原文位置</th><th scope="col">要取出的資訊</th><th scope="col">這一步能判斷什麼</th></tr></thead><tbody><tr><td>1 · Figure 28，文件頁 46／PDF 72</td><td>Sanitize Namespace → Admin Opcode=8Ch，支援要求為 O（Optional）。</td><td>找到要查的命令與編碼。Optional 表示實作可選，還不能判定這台 controller 有支援。</td></tr><tr><td>2 · Identify Controller，Figure 338，文件頁 355、361～362／PDF 381、387～388</td><td>CNS=01h；假設 LPA.CSES=1、SANICAP.CES=1、NVERS=0。CSES 是 LPA bit1。</td><td>可以讀 Commands Supported and Effects；有 Crypto Erase 能力，但沒有 namespace Media Verification 能力。CES 本身不能取代 8Ch 的命令支援查詢。</td></tr><tr><td>3 · Get Log Page，Figures 204～208，文件頁 213～215／PDF 239～241</td><td>Opcode=02h、LID=05h、NSID=0、NUMDL=03FFh、NUMDU=0；LPO=0、OT=0、RAE=0，讀取 4096 bytes。</td><td>NUMD 是數量減 1：(03FFh+1)×4=4096 bytes。這是讀能力表，沒有提交 8Ch 清除命令。</td></tr><tr><td>4 · Figure 216，文件頁 227／PDF 253</td><td>Admin entry 由 byte0 開始，每筆 4 bytes；8Ch=140，因此 4×140=560=230h，取 bytes560～563。</td><td>這是 Admin 命令，不加 I/O 區的 1024-byte 起點。若只讀一段，buffer 內的位置還需扣掉該段的起始 byte offset。</td></tr><tr><td>5 · Figure 217，文件頁 228～229／PDF 254～255</td><td>假設 bytes 依序是 03h、00h、01h、00h，依 little-endian 組成 00010003h；bit0=1。</td><td>Command Supported（CSUPP）=1，所以 controller 宣告支援 8Ch。本例也有 LBCC=1、CSE=001b：命令可能改變資料，且有同 namespace 的提交協調建議；這些不是執行結果。</td></tr><tr><td>6 · §5.2.27、Figure 454，文件頁 452～453／PDF 478～479</td><td>開始 namespace 清除的 SANACT=100b（Crypto Erase）；010b、011b 為 Reserved。準備執行前，再查 Active NSID、保護狀態與並行限制。</td><td>可回答「支援這個命令」，但不能回答「支援 namespace Overwrite」，也不能保證任意目標現在都能執行。範例 NVERS=0，也不提供進入 Media Verification 的能力。</td></tr></tbody></table></div>
<p>如果有效 entry 的 CSUPP=0，就是該命令不受支援，且這筆結構其餘欄位須為 0。若 LPA.CSES=0 或讀 Log 失敗，則這條路徑沒有取得有效命令支援證據，不能把它改寫成「已讀到 CSUPP=0」。</p>
<p class="qa-citations">來源：<a href="#ref-adminsupport">Base 2.4 §3.1.3.4 (Figure 28 PCIe I/O-controller rows and O/M/P note only)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a></p>
</section>
</li>
<li id="q-118-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Format NVM、Sanitize、Sanitize Namespace 的 Admin Opcode 分別是 80h、84h、8Ch。這裡要送出的查詢命令是 Identify（06h）與 Get Log Page（02h）；Get Log Page 的 LID=05h 才選到命令支援表。不能把 8Ch 填進 LID，也不能只查 Get Log Page 本身的 CSUPP，就當成所有 Log 或所有管理命令都受支援。</p>
</li>
<li id="q-118-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先確認查詢通道與 Log 支援，再讀正確 entry；若 CSUPP=1，才繼續查方法、參數與目標狀態。查詢過程只讀取資訊，不需要啟動清除。準備真的執行時，才進一步確認 Active NSID、寫入保護、Sanitize 狀態、並行上限與待啟用韌體限制。</p>
</li>
<li id="q-118-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Identify 與 Get Log Page 成功，表示已取得可判讀的能力資料。若 8Ch 的 CSUPP=1，可以回答「controller 宣告支援 Sanitize Namespace」；這不表示 NSID=7 現在一定能接受命令，更不表示資料已經清除。</p>
</li>
<li id="q-118-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>查詢 LID05h 不受支援時，Get Log Page 一般以 Invalid Log Page（1/09h）失敗；這時沒有有效的 CSUPP 可讀，不能當成 CSUPP=0。真正提交不支援的 Opcode，與受支援命令使用非法 SANACT，是另外兩種條件，分別按 Invalid Command Opcode（0/01h）與 Invalid Field in Command（0/02h）判斷。</p>
</li>
<li id="q-118-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-118-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>這條路徑只讀 Identify 與能力 Log，不會因查到支援就產生 Sanitize 開始或完成通知。其他同時發生的事件仍依各自條件處理。</p>
</li>
<li id="q-118-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>成功的能力查詢不會更新 Sanitize Status 為進行中，也不會替目標 namespace 清除資料。若查詢本身失敗，再依該 CQE 及 Error Information 規則追查；不能拿 Sanitize 背景結果代替查詢的完成結果。</p>
</li>
<li id="q-118-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>唯讀能力查詢不會建立 Sanitize Start 或 Sanitize Completion 的 Persistent Event。這些紀錄屬於實際操作，不能因 controller 宣告支援，就期待 PEL 已有對應歷史。</p>
</li>
<li id="q-118-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>查詢若因重設中止，恢復後須重新送出。比較回覆時，再逐欄區分固定身分、配置與動態狀態。 <a class="qa-rule-link" href="#common-identify-12">本冊完整規則</a></p>
</li>
<li id="q-118-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>重設後重新查詢受影響的物件。重設本身不表示 namespace 已刪除，也不表示配置已恢復出廠值。 <a class="qa-rule-link" href="#common-identify-13">本冊完整規則</a></p>
</li>
<li id="q-118-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新查詢並比較。若期間還有韌體啟用或管理操作，必須分清楚差異是由哪個事件造成。 <a class="qa-rule-link" href="#common-identify-14">本冊完整規則</a></p>
</li>
<li id="q-118-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Identify 是唯讀查詢。不同 controller 的 Active List 可能不同，因此比較時必須確認查詢對象。 <a class="qa-rule-link" href="#common-identify-15">本冊完整規則</a></p>
</li>
<li id="q-118-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>交叉比對時，要保持 controller、命令集與查詢時點一致。CSUPP=1 但操作失敗時，先排除非法參數及目前狀態；CSUPP=0 卻有同一命令的合法成功行為，才構成需要追查的支援宣告矛盾。SANICAP.OWS=1 也不會把 namespace Overwrite 變成合法操作。</p>
</li>
<li id="q-118-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認讀的是 LID05h 的 Admin 區、Opcode8Ch 那一筆，並且 Get Log Page 已成功。讀錯 84h、漏掉位移單位，或把失敗查詢留下的 buffer 當成有效資料，都會讓支援結論出錯。</p>
</li>
</ol>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/logs/zh-tw/#q-081">Q81</a> · <a href="/nvme/question-bank/format-sanitize/zh-tw/#q-126">Q126</a> · <a href="/nvme/question-bank/format-sanitize/zh-tw/#q-134">Q134</a> · <a href="/nvme/question-bank/format-sanitize/zh-tw/#q-135">Q135</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-nvmformat">NVM Command Set 1.3 §4.1.2</a> · <a href="#ref-formatpel">Base 2.4 §5.2.13.1.14.2.7–5.2.13.1.14.2.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-adminsupport">Base 2.4 §3.1.3.4 (Figure 28 PCIe I/O-controller rows and O/M/P note only)</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-idcmd">Base 2.4 §5.2.14.1</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-119" data-question="119"><h2><a class="qa-qid" href="#q-119">Q119</a> Format、Secure Erase、Subsystem Sanitize 與 Namespace Sanitize 有何差別？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-119-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-119-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Format 用於改變媒體格式，也可要求 Secure Erase；Sanitize 則以清除目標中的使用者資料為主，不是一般的格式切換。</p>
</li>
<li id="q-119-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Format 依 FNA／SES／NSID 選範圍；Subsystem Sanitize 包含其規定的全部使用者資料位置；Namespace Sanitize 只清除指定 namespace 的資料範圍。</p>
</li>
<li id="q-119-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>檢查 OACS、FNA、SANICAP、namespace 狀態及支援的格式。不能只看到「Crypto Erase」同名，就省略命令範圍差異。</p>
</li>
<li id="q-119-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Format 的 SES=0 不要求 Secure Erase，1 為 User Data Erase，2 為 Cryptographic Erase。Sanitize 的 SANACT 另行選擇方法；Namespace Sanitize 只支援 Crypto Erase。</p>
</li>
<li id="q-119-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先回答要改格式、清除哪個範圍、是否需要指定清除方法，再選命令。所有 namespace 各做一次 Sanitize，也不等於 subsystem 的全部使用者資料位置都已處理。</p>
</li>
<li id="q-119-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Format CQE 在格式化完成後回傳；Sanitize 啟動成功後仍以背景方式進行，要另查 LID81h。</p>
</li>
<li id="q-119-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不合法格式使用 Invalid Format；不支援 SANACT 使用 Invalid Field。各命令的拒絕條件不能互相套用。</p>
</li>
<li id="q-119-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-119-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>本題比較兩種操作：Format 改變 namespace 屬性時，依支援與通知設定回報對應 Namespace Attribute Changed，並更新 Changed Namespace 清單；FPI 僅由 0 變非 0 或由非 0 變 0 時才符合相關變更通知條件，不是每個百分比都通知。 Sanitize 則不同：依狀態轉移回報 Sanitize Operation Completed、Completed With Unexpected Deallocation 或 Entered Media Verification State，AER 的 LID=81h。由 Admin SQ 啟動時，僅啟動該操作的 controller 回報這次通知；仍須查看 Log 分辨成功、失敗或驗證階段。</p>
</li>
<li id="q-119-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>本題比較兩種操作：成功後重新讀 Identify Namespace 的格式與容量，並查看 Changed Namespace 清單。錯誤時依 CQE.More 讀 Error Information；不能以一筆成功的 Get Log Page 取代 Format 本身的完成結果。 Sanitize 則不同：Sanitize Status 在啟動 CQE 張貼前更新，之後隨狀態轉移更新；它跨 Reset 與斷電保留。用相同目標的 SOS、SANS、SPROG、SCDW10 及 GDE／NDE 比對，不以背景失敗要求原啟動命令再回第二筆 CQE。</p>
</li>
<li id="q-119-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>本題比較兩種操作：支援 PEL 與對應事件時，Format Start（07h）保存要求，Format Completion（08h）保存操作結果。Completion 的 FNVMS 與 INFO 必須一起讀；若原 Format 沒有 CQE，INFO 可為 0，不能直接解成格式化成功。 Sanitize 則不同：支援對應 PEL 事件時，進入 Processing 記錄 Sanitize Start（09h）；進入 Idle、Restricted Failure 或 Unrestricted Failure 記錄 Completion（0Ah）。Completion 也包含失敗，事件 NSID 可用來分辨 subsystem 與 namespace 目標。</p>
</li>
<li id="q-119-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>本題比較兩種操作：Controller Reset 結束舊命令通道，不能沿用原 Format 的 outstanding 狀態或等待舊 CQE。恢復後重新讀格式、FPI 與可取得的 Format Completion Event，確認媒體實際狀態；Reset 本身既不證明格式化成功，也不保證回復舊格式。 Sanitize 則不同：Sanitize 背景操作不因 Controller Level Reset 而中止。Host 重新建立查詢通道後讀同一目標的 LID81h。另需分辨 Reset 來源：傳輸層 Reset 等條件可能取消 Media Verification，使 MVCNCLD 設為 1，而不是取消整個清除操作。</p>
</li>
<li id="q-119-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>本題比較兩種操作：NVM Subsystem Reset 後先恢復通道，再逐一查詢原 Format 範圍內的 namespaces。不能只查提交命令的 controller，就假設所有受影響 namespace 都已完成或恢復。 Sanitize 則不同：NVM Subsystem Reset 也不提供中止 Sanitize 的方法。操作的狀態與 Log 需要保留；如果原本要求 Media Verification，還要檢查 MVCNCLD 及後續 deallocation 階段。</p>
</li>
<li id="q-119-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>本題比較兩種操作：Power Cycle 中斷時若沒有可信的 Format 成功完成，Host 應重新確認目前格式與可用性，必要時重新執行符合當前狀態的 Format。先前資料可能已被破壞，不能因命令沒有回成功就假設資料仍在。 Sanitize 則不同：斷電期間無法進行媒體處理，但重新供電後 Sanitize 仍須依保存的狀態繼續，不可當成從未開始。恢復後查看 SOS／SANS 與進度，不能只見 SPROG=FFFFh 就宣告成功。</p>
</li>
<li id="q-119-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>本題比較兩種操作：依 SES 選擇 FNA.FNS 或 FNA.SENS，再與 NSID 一起決定範圍。同一共享 namespace 可由其他 controller 存取，因此需要協調相關 I/O；提交到某個 controller，不表示只影響它自己的資料。 Sanitize 則不同：Subsystem Sanitize 限制整個 subsystem 的相關存取；Namespace Sanitize 則針對指定 namespace，但所有可存取它的 controller 都受限制。共享韌體更新等操作另有全域限制，不能只因另一 namespace 的資料不被清除，就推論完全沒有影響。</p>
</li>
<li id="q-119-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>例如需要改成 4 KiB LBA，應選 Format；需要清除整個 subsystem，不能只指定一個 namespace 然後把 NDE 當 GDE。</p>
</li>
<li id="q-119-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查需求中的「清乾淨」究竟指一個 namespace，還是 subsystem 的完整清除範圍。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-nvmsanitize">NVM Command Set 1.3 §4.1.7, 5.12</a> · <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-nvmformat">NVM Command Set 1.3 §4.1.2</a> · <a href="#ref-formatpel">Base 2.4 §5.2.13.1.14.2.7–5.2.13.1.14.2.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-120" data-question="120"><h2><a class="qa-qid" href="#q-120">Q120</a> Format 如何選 LBA Format、Metadata、PI 與 SES？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-120-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-120-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>格式選擇決定後續 I/O 的資料長度與 metadata 位置。選錯會讓 Read／Write 的 buffer 與保護資訊不符合 namespace 的格式。</p>
</li>
<li id="q-120-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>設定適用於 Format 所涵蓋的 namespaces，不是只在這一筆命令中暫時使用。</p>
</li>
<li id="q-120-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀 Identify Namespace 的 LBAF／FLBAS、MC、DPC、DPS，以及需要時的 NVM 特定格式擴充；確認 Host Behavior Support.LBAFEE。</p>
</li>
<li id="q-120-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CDW10 的 LBAFL 與有效時的 LBAFU 組成格式索引；MSET 選 extended LBA 或獨立 metadata buffer；PI 選 0～3；本版 NVM PIL 必須為 0。SES 另決定是否 Secure Erase。</p>
</li>
<li id="q-120-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>選定一個已宣告的格式，確認 metadata 與 PI 能力，再組合欄位。假設 LBAF2 是 4096-byte data＋16-byte metadata，MSET=1 時每個 extended LBA 傳輸長度是 4112 bytes。</p>
</li>
<li id="q-120-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功後 FLBAS／DPS 應反映設定；logical block 大小改變時，NSZE／NCAP 可能改變，應重新讀取。</p>
</li>
<li id="q-120-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>未支援格式回 Invalid Format；未啟用必要 LBAFEE 的格式回 Invalid Namespace or Format。共享 FDP RUH 還須符合共同格式限制。</p>
</li>
<li id="q-120-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-120-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Format 改變 namespace 屬性時，依支援與通知設定回報對應 Namespace Attribute Changed，並更新 Changed Namespace 清單；FPI 僅由 0 變非 0 或由非 0 變 0 時才符合相關變更通知條件，不是每個百分比都通知。 <a class="qa-rule-link" href="#common-format_op-9">本冊完整規則</a></p>
</li>
<li id="q-120-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>成功後重新讀 Identify Namespace 的格式與容量，並查看 Changed Namespace 清單。 <a class="qa-rule-link" href="#common-format_op-10">本冊完整規則</a></p>
</li>
<li id="q-120-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 與對應事件時，Format Start（07h）保存要求，Format Completion（08h）保存操作結果。 <a class="qa-rule-link" href="#common-format_op-11">本冊完整規則</a></p>
</li>
<li id="q-120-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 結束舊命令通道，不能沿用原 Format 的 outstanding 狀態或等待舊 CQE。 <a class="qa-rule-link" href="#common-format_op-12">本冊完整規則</a></p>
</li>
<li id="q-120-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後先恢復通道，再逐一查詢原 Format 範圍內的 namespaces。 <a class="qa-rule-link" href="#common-format_op-13">本冊完整規則</a></p>
</li>
<li id="q-120-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 中斷時若沒有可信的 Format 成功完成，Host 應重新確認目前格式與可用性，必要時重新執行符合當前狀態的 Format。 <a class="qa-rule-link" href="#common-format_op-14">本冊完整規則</a></p>
</li>
<li id="q-120-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>依 SES 選擇 FNA.FNS 或 FNA.SENS，再與 NSID 一起決定範圍。 <a class="qa-rule-link" href="#common-format_op-15">本冊完整規則</a></p>
</li>
<li id="q-120-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>用新格式重算 I/O data／metadata 長度，不要沿用 Format 前的 buffer 設定。</p>
</li>
<li id="q-120-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查格式索引的上、下位元與 LBAFEE 是否一致，再查 MSET／PI 組合。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-behavior">Base 2.4 §5.2.30.1.15</a> · <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-nvmformat">NVM Command Set 1.3 §4.1.2</a> · <a href="#ref-formatpel">Base 2.4 §5.2.13.1.14.2.7–5.2.13.1.14.2.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-121" data-question="121"><h2><a class="qa-qid" href="#q-121">Q121</a> Format 的非法格式、參數與狀態如何回報？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-121-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-121-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>拒絕原因可能是格式不存在、Host 未啟用格式、namespace 受保護，或與其他操作衝突。不同原因需要不同修正。</p>
</li>
<li id="q-121-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>先計算 Format 的完整範圍，再查其中每個 namespace；只要範圍內有寫入保護，就不能只看提交時指定的 namespace 是否可寫。</p>
</li>
<li id="q-121-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>用 LBAF、LBAFEE、FNA、Write Protection 狀態，以及現有 I/O／Admin 操作確認前提。</p>
</li>
<li id="q-121-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Invalid Format=1/0Ah；Invalid Namespace or Format=0/0Bh；Namespace is Write Protected=0/20h；Command Sequence Error=0/0Ch；Format In Progress=0/84h。</p>
</li>
<li id="q-121-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>負向測試一次製造一項問題。例如測不支援 LBAF，先確保 NSID 合法、未受保護、沒有其他操作衝突。</p>
</li>
<li id="q-121-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>正確拒絕不等於格式已改變；讀回設定以確認未將失敗命令錯當成成功操作。</p>
</li>
<li id="q-121-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Format 影響的 namespace 尚有 I/O 時，controller 可中止 Format；若因此中止，應回 Command Sequence Error。這裡的「可」不能改寫成每次都必須拒絕。</p>
</li>
<li id="q-121-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-121-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Format 改變 namespace 屬性時，依支援與通知設定回報對應 Namespace Attribute Changed，並更新 Changed Namespace 清單；FPI 僅由 0 變非 0 或由非 0 變 0 時才符合相關變更通知條件，不是每個百分比都通知。 <a class="qa-rule-link" href="#common-format_op-9">本冊完整規則</a></p>
</li>
<li id="q-121-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>成功後重新讀 Identify Namespace 的格式與容量，並查看 Changed Namespace 清單。 <a class="qa-rule-link" href="#common-format_op-10">本冊完整規則</a></p>
</li>
<li id="q-121-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 與對應事件時，Format Start（07h）保存要求，Format Completion（08h）保存操作結果。 <a class="qa-rule-link" href="#common-format_op-11">本冊完整規則</a></p>
</li>
<li id="q-121-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 結束舊命令通道，不能沿用原 Format 的 outstanding 狀態或等待舊 CQE。 <a class="qa-rule-link" href="#common-format_op-12">本冊完整規則</a></p>
</li>
<li id="q-121-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後先恢復通道，再逐一查詢原 Format 範圍內的 namespaces。 <a class="qa-rule-link" href="#common-format_op-13">本冊完整規則</a></p>
</li>
<li id="q-121-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 中斷時若沒有可信的 Format 成功完成，Host 應重新確認目前格式與可用性，必要時重新執行符合當前狀態的 Format。 <a class="qa-rule-link" href="#common-format_op-14">本冊完整規則</a></p>
</li>
<li id="q-121-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>依 SES 選擇 FNA.FNS 或 FNA.SENS，再與 NSID 一起決定範圍。 <a class="qa-rule-link" href="#common-format_op-15">本冊完整規則</a></p>
</li>
<li id="q-121-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>測試需分清 shall、should、may，以及同時多錯誤時的 Status 選擇自由。</p>
</li>
<li id="q-121-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先看是否同時觸發保護與非法格式，導致精確 Status 斷言沒有唯一答案。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-nvmformat">NVM Command Set 1.3 §4.1.2</a> · <a href="#ref-formatpel">Base 2.4 §5.2.13.1.14.2.7–5.2.13.1.14.2.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-122" data-question="122"><h2><a class="qa-qid" href="#q-122">Q122</a> Format 期間哪些 Admin 操作可以繼續？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-122-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-122-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Host 仍需要查詢狀態、維持通知與管理 queue，所以 Format 期間不應一概封鎖全部 Admin 命令。</p>
</li>
<li id="q-122-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>限制取決於操作是否影響正在 Format 的 namespace，以及 Figure144 對命令或 Log 的附加條件。</p>
</li>
<li id="q-122-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先確認命令本身受支援，再查 Format 期間的允許清單；列在允許清單不會讓選配功能自動變成支援。</p>
</li>
<li id="q-122-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>常見允許項包含 Abort、AER、queue 建立／刪除、Identify、Get Features、Get Log Page 的指定 LID 及 Keep Alive。Set Features 中的 Namespace Write Protection Config 不允許。</p>
</li>
<li id="q-122-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>以 Figure144 逐項檢查。Error Information 的 LBA 回 0；Self-test 僅 Controller DST 建議允許；不能由「Get Log Page 允許」推論所有 LID 都允許。</p>
</li>
<li id="q-122-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>允許的查詢回目前狀態，不表示 Format 已完成。Format 的 CQE 或完整結果證據仍要另外確認。</p>
</li>
<li id="q-122-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>未列出的 Admin 若影響被 Format 的 namespace，可中止；因這項理由中止時，建議回 Format In Progress。反向的操作衝突則可能使 Format 回 Command Sequence Error。</p>
</li>
<li id="q-122-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-122-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Format 改變 namespace 屬性時，依支援與通知設定回報對應 Namespace Attribute Changed，並更新 Changed Namespace 清單；FPI 僅由 0 變非 0 或由非 0 變 0 時才符合相關變更通知條件，不是每個百分比都通知。 <a class="qa-rule-link" href="#common-format_op-9">本冊完整規則</a></p>
</li>
<li id="q-122-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>成功後重新讀 Identify Namespace 的格式與容量，並查看 Changed Namespace 清單。 <a class="qa-rule-link" href="#common-format_op-10">本冊完整規則</a></p>
</li>
<li id="q-122-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 與對應事件時，Format Start（07h）保存要求，Format Completion（08h）保存操作結果。 <a class="qa-rule-link" href="#common-format_op-11">本冊完整規則</a></p>
</li>
<li id="q-122-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 結束舊命令通道，不能沿用原 Format 的 outstanding 狀態或等待舊 CQE。 <a class="qa-rule-link" href="#common-format_op-12">本冊完整規則</a></p>
</li>
<li id="q-122-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後先恢復通道，再逐一查詢原 Format 範圍內的 namespaces。 <a class="qa-rule-link" href="#common-format_op-13">本冊完整規則</a></p>
</li>
<li id="q-122-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 中斷時若沒有可信的 Format 成功完成，Host 應重新確認目前格式與可用性，必要時重新執行符合當前狀態的 Format。 <a class="qa-rule-link" href="#common-format_op-14">本冊完整規則</a></p>
</li>
<li id="q-122-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>依 SES 選擇 FNA.FNS 或 FNA.SENS，再與 NSID 一起決定範圍。 <a class="qa-rule-link" href="#common-format_op-15">本冊完整規則</a></p>
</li>
<li id="q-122-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>分別驗證命令允許性、LID 限制與回傳欄位，不用一筆 Get Log 成功概括全部管理操作。</p>
</li>
<li id="q-122-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查 Figure144 的附加限制欄，尤其所查的 LID 是否真的列入。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-sanitizerestrict">Base 2.4 §5.1.1–5.1.2 (PCIe commands)</a> · <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-nvmformat">NVM Command Set 1.3 §4.1.2</a> · <a href="#ref-formatpel">Base 2.4 §5.2.13.1.14.2.7–5.2.13.1.14.2.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-123" data-question="123"><h2><a class="qa-qid" href="#q-123">Q123</a> Format 過程遇到 Reset 或斷電，如何判斷結果？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-123-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-123-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>失去 CQE 代表 Host 不知道結果，不等於操作必定沒做，也不等於已成功。恢復後應以現況與事件證據重新建立判斷。</p>
</li>
<li id="q-123-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>檢查原 Format 範圍內所有 namespaces，以及其他 controller 對共享 namespace 的存取狀態。</p>
</li>
<li id="q-123-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀 Identify Namespace 的 FLBAS、DPS、NSZE／NCAP、支援時的 FPI，及 PEL Format Completion。</p>
</li>
<li id="q-123-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Format Completion Event 的 FNVMS 說明格式化結果，INFO 保存曾回報的 Status；沒有 CQE 時 INFO=0 不能當成功。</p>
</li>
<li id="q-123-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先恢復 controller 與 Admin Queue，再保存事件、讀回新格式、確認可用性；若仍無法確定操作完成，就不要直接以舊格式恢復 I/O。</p>
</li>
<li id="q-123-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>可以確認目前格式與完成狀態後，Host 才配置對應 buffer 與 PI。若需重新 Format，先依目前能力與範圍建立新命令。</p>
</li>
<li id="q-123-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Reset 不保證原資料可復原，Power Cycle 也不是撤銷 Format 的方法；未收到成功不代表舊資料安全。</p>
</li>
<li id="q-123-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-123-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Format 改變 namespace 屬性時，依支援與通知設定回報對應 Namespace Attribute Changed，並更新 Changed Namespace 清單；FPI 僅由 0 變非 0 或由非 0 變 0 時才符合相關變更通知條件，不是每個百分比都通知。 <a class="qa-rule-link" href="#common-format_op-9">本冊完整規則</a></p>
</li>
<li id="q-123-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>成功後重新讀 Identify Namespace 的格式與容量，並查看 Changed Namespace 清單。 <a class="qa-rule-link" href="#common-format_op-10">本冊完整規則</a></p>
</li>
<li id="q-123-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 與對應事件時，Format Start（07h）保存要求，Format Completion（08h）保存操作結果。 <a class="qa-rule-link" href="#common-format_op-11">本冊完整規則</a></p>
</li>
<li id="q-123-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 結束舊命令通道，不能沿用原 Format 的 outstanding 狀態或等待舊 CQE。 <a class="qa-rule-link" href="#common-format_op-12">本冊完整規則</a></p>
</li>
<li id="q-123-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後先恢復通道，再逐一查詢原 Format 範圍內的 namespaces。 <a class="qa-rule-link" href="#common-format_op-13">本冊完整規則</a></p>
</li>
<li id="q-123-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 中斷時若沒有可信的 Format 成功完成，Host 應重新確認目前格式與可用性，必要時重新執行符合當前狀態的 Format。 <a class="qa-rule-link" href="#common-format_op-14">本冊完整規則</a></p>
</li>
<li id="q-123-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>依 SES 選擇 FNA.FNS 或 FNA.SENS，再與 NSID 一起決定範圍。 <a class="qa-rule-link" href="#common-format_op-15">本冊完整規則</a></p>
</li>
<li id="q-123-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>把 Reset 之前最後可信的事件與恢復後第一份快照連起來，標示中間不可觀察的期間。</p>
</li>
<li id="q-123-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查是否有可信的 Format 成功 CQE；若沒有，避免直接用 INFO=0 補出成功結論。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-nvmformat">NVM Command Set 1.3 §4.1.2</a> · <a href="#ref-formatpel">Base 2.4 §5.2.13.1.14.2.7–5.2.13.1.14.2.8</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-124" data-question="124"><h2><a class="qa-qid" href="#q-124">Q124</a> Format 成功後哪些 Identify 與 Namespace 狀態要更新？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-124-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-124-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Format 改變後續 I/O 的解讀方式，因此 Host 必須更新快取的 namespace 資訊，避免用舊 LBA 大小或 PI 設定讀寫。</p>
</li>
<li id="q-124-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>更新的是受影響 namespace 的格式及相關容量；Format 不等同 Create／Delete，不能預設一定產生新 NSID。</p>
</li>
<li id="q-124-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 Identify Namespace 與必要的 NVM 特定結構，確認 FLBAS、DPS、LBAF、NSZE、NCAP 與 FPI。</p>
</li>
<li id="q-124-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>FLBAS 表示使用中的格式及 metadata 傳輸方式；DPS 表示 PI 設定；NSZE／NCAP 以新的 logical block 為單位。</p>
</li>
<li id="q-124-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>等待 Format 成功 CQE，重新 Identify，再依新格式重算 LBA 範圍與 buffer 大小；有共享存取者時同步更新它們的配置。</p>
</li>
<li id="q-124-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>設定讀回應與命令要求一致；若 block 大小改變，NSZE／NCAP 可能不同，不能用「數字必須完全不變」驗證容量。</p>
</li>
<li id="q-124-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>若成功 CQE 後仍回舊格式，先排除讀錯 NSID、讀到快取或命令範圍誤判，再確認不一致。</p>
</li>
<li id="q-124-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-124-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Format 改變 namespace 屬性時，依支援與通知設定回報對應 Namespace Attribute Changed，並更新 Changed Namespace 清單；FPI 僅由 0 變非 0 或由非 0 變 0 時才符合相關變更通知條件，不是每個百分比都通知。 <a class="qa-rule-link" href="#common-format_op-9">本冊完整規則</a></p>
</li>
<li id="q-124-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>成功後重新讀 Identify Namespace 的格式與容量，並查看 Changed Namespace 清單。 <a class="qa-rule-link" href="#common-format_op-10">本冊完整規則</a></p>
</li>
<li id="q-124-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 與對應事件時，Format Start（07h）保存要求，Format Completion（08h）保存操作結果。 <a class="qa-rule-link" href="#common-format_op-11">本冊完整規則</a></p>
</li>
<li id="q-124-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 結束舊命令通道，不能沿用原 Format 的 outstanding 狀態或等待舊 CQE。 <a class="qa-rule-link" href="#common-format_op-12">本冊完整規則</a></p>
</li>
<li id="q-124-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後先恢復通道，再逐一查詢原 Format 範圍內的 namespaces。 <a class="qa-rule-link" href="#common-format_op-13">本冊完整規則</a></p>
</li>
<li id="q-124-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 中斷時若沒有可信的 Format 成功完成，Host 應重新確認目前格式與可用性，必要時重新執行符合當前狀態的 Format。 <a class="qa-rule-link" href="#common-format_op-14">本冊完整規則</a></p>
</li>
<li id="q-124-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>依 SES 選擇 FNA.FNS 或 FNA.SENS，再與 NSID 一起決定範圍。 <a class="qa-rule-link" href="#common-format_op-15">本冊完整規則</a></p>
</li>
<li id="q-124-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>例如同一容量從 512-byte 改為 4096-byte LBA，應比較以 bytes 表示的容量及允許變化，而不是只比較 block 數。</p>
</li>
<li id="q-124-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查 Host 是否真的重新送出 Identify，而非讀取 Format 前留下的 buffer。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-nvmformat">NVM Command Set 1.3 §4.1.2</a> · <a href="#ref-changedlog">Base 2.4 §5.2.13.1.5</a> · <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-formatpel">Base 2.4 §5.2.13.1.14.2.7–5.2.13.1.14.2.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-125" data-question="125"><h2><a class="qa-qid" href="#q-125">Q125</a> Format 失敗時如何使用 CQE、Error Log 與 PEL？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-125-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-125-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>先區分命令因參數被拒絕，與格式化已開始後失敗；後者可能已改變資料，不能當成完全沒有執行。</p>
</li>
<li id="q-125-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>證據需對應同一筆 Format 及同一範圍；其他 namespace 的事件不能當成這筆命令的結果。</p>
</li>
<li id="q-125-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>保存 CQE 的 SCT／SC／M／DNR，及 PEL 支援與事件有效性。</p>
</li>
<li id="q-125-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Error Log 用 SQID／CID／ECNT 關聯；Format Start 保存參數，Completion 的 FNVMS／INFO 記錄結果與曾回報狀態。</p>
</li>
<li id="q-125-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先讀原 CQE，再依 M 取得補充資訊，最後以 PEL 與 Identify 現況補足過程。缺少某種記錄時先確認其要求，不硬湊三份一對一證據。</p>
</li>
<li id="q-125-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>能說明失敗原因及目前是否可用，就是有效診斷。若結果仍不確定，保留不確定性而不是假設格式化回復。</p>
</li>
<li id="q-125-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Multiple errors 可能有不同合法 Status；INFO=0 也可能只是沒有 CQE，不可以忽略 FNVMS。</p>
</li>
<li id="q-125-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-125-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Format 改變 namespace 屬性時，依支援與通知設定回報對應 Namespace Attribute Changed，並更新 Changed Namespace 清單；FPI 僅由 0 變非 0 或由非 0 變 0 時才符合相關變更通知條件，不是每個百分比都通知。 <a class="qa-rule-link" href="#common-format_op-9">本冊完整規則</a></p>
</li>
<li id="q-125-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>成功後重新讀 Identify Namespace 的格式與容量，並查看 Changed Namespace 清單。 <a class="qa-rule-link" href="#common-format_op-10">本冊完整規則</a></p>
</li>
<li id="q-125-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 與對應事件時，Format Start（07h）保存要求，Format Completion（08h）保存操作結果。 <a class="qa-rule-link" href="#common-format_op-11">本冊完整規則</a></p>
</li>
<li id="q-125-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 結束舊命令通道，不能沿用原 Format 的 outstanding 狀態或等待舊 CQE。 <a class="qa-rule-link" href="#common-format_op-12">本冊完整規則</a></p>
</li>
<li id="q-125-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後先恢復通道，再逐一查詢原 Format 範圍內的 namespaces。 <a class="qa-rule-link" href="#common-format_op-13">本冊完整規則</a></p>
</li>
<li id="q-125-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 中斷時若沒有可信的 Format 成功完成，Host 應重新確認目前格式與可用性，必要時重新執行符合當前狀態的 Format。 <a class="qa-rule-link" href="#common-format_op-14">本冊完整規則</a></p>
</li>
<li id="q-125-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>依 SES 選擇 FNA.FNS 或 FNA.SENS，再與 NSID 一起決定範圍。 <a class="qa-rule-link" href="#common-format_op-15">本冊完整規則</a></p>
</li>
<li id="q-125-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>把命令參數、結果與目前格式比對，檢查是否有「回報成功但格式不符」或「失敗卻被 Host 視為成功」的矛盾。</p>
</li>
<li id="q-125-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先看 Format 是否已進入執行階段，以及 PEL 是否存在相符的 Start／Completion。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-format">Base 2.4 §5.1.1, 5.2.11</a> · <a href="#ref-nvmformat">NVM Command Set 1.3 §4.1.2</a> · <a href="#ref-formatpel">Base 2.4 §5.2.13.1.14.2.7–5.2.13.1.14.2.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-126" data-question="126"><h2><a class="qa-qid" href="#q-126">Q126</a> SANICAP 如何表示 Block Erase、Overwrite 與 Crypto Erase？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-126-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-126-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>SANICAP 告訴 Host 哪些清除方法可用，以及 No-Deallocate、驗證等延伸能力。它不是「非零就所有方法皆可用」的布林值。</p>
</li>
<li id="q-126-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>CES、BES、OWS 對應 subsystem 清除方法；namespace 清除另有能力宣告，且本版只定義 Crypto Erase。</p>
</li>
<li id="q-126-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀 Identify Controller.SANICAP，並交叉查 Command Effects 中的 84h／8Ch 與 LID81h 支援。</p>
</li>
<li id="q-126-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CES、BES、OWS 分別為 Crypto Erase、Block Erase、Overwrite 支援位元；NODAS／NDI 相關能力決定 NDAS 的意義，VERS／NVERS 則分別控制兩種目標的 Media Verification。</p>
</li>
<li id="q-126-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>把需求的方法對到它的能力位元，再選對 SANACT。假設只有 BES=1，就選 subsystem Block Erase，不能改用 Overwrite。</p>
</li>
<li id="q-126-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>合法啟動回 Success，且對應 Sanitize Status 已更新；能力支援不保證每次背景清除都能成功。</p>
</li>
<li id="q-126-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>支援命令但 SANACT 不受支援時，必須回 Invalid Field in Command。</p>
</li>
<li id="q-126-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-126-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>依狀態轉移回報 Sanitize Operation Completed、Completed With Unexpected Deallocation 或 Entered Media Verification State，AER 的 LID=81h。 <a class="qa-rule-link" href="#common-sanitize_op-9">本冊完整規則</a></p>
</li>
<li id="q-126-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Sanitize Status 在啟動 CQE 張貼前更新，之後隨狀態轉移更新；它跨 Reset 與斷電保留。 <a class="qa-rule-link" href="#common-sanitize_op-10">本冊完整規則</a></p>
</li>
<li id="q-126-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援對應 PEL 事件時，進入 Processing 記錄 Sanitize Start（09h）；進入 Idle、Restricted Failure 或 Unrestricted Failure 記錄 Completion（0Ah）。 <a class="qa-rule-link" href="#common-sanitize_op-11">本冊完整規則</a></p>
</li>
<li id="q-126-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Sanitize 背景操作不因 Controller Level Reset 而中止。 <a class="qa-rule-link" href="#common-sanitize_op-12">本冊完整規則</a></p>
</li>
<li id="q-126-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 也不提供中止 Sanitize 的方法。 <a class="qa-rule-link" href="#common-sanitize_op-13">本冊完整規則</a></p>
</li>
<li id="q-126-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>斷電期間無法進行媒體處理，但重新供電後 Sanitize 仍須依保存的狀態繼續，不可當成從未開始。 <a class="qa-rule-link" href="#common-sanitize_op-14">本冊完整規則</a></p>
</li>
<li id="q-126-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Subsystem Sanitize 限制整個 subsystem 的相關存取；Namespace Sanitize 則針對指定 namespace，但所有可存取它的 controller 都受限制。 <a class="qa-rule-link" href="#common-sanitize_op-15">本冊完整規則</a></p>
</li>
<li id="q-126-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>若不同 controller 屬於同一 subsystem，支援的相同 Sanitize 命令類型應一致；再另外驗證各命令的目標能力。</p>
</li>
<li id="q-126-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查實際方法的能力位元，不要只檢查 SANICAP 是否非零。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-127" data-question="127"><h2><a class="qa-qid" href="#q-127">Q127</a> NDAS、Overwrite Pattern、Pass Count 與反轉 Pattern 如何使用？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-127-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-127-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Overwrite 的欄位決定覆寫內容與次數；NDAS 則控制成功後是否釋放配置。資料清除與 deallocation 是不同動作，必須分開理解。</p>
</li>
<li id="q-127-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>這些 Overwrite 與 NDAS 欄位屬 subsystem Sanitize，不能照搬到 Sanitize Namespace 的 CDW10。</p>
</li>
<li id="q-127-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>確認 OWS、No-Deallocate Inhibited 與 No-Deallocate Modifies Media After Sanitize，必要時讀 FID17h.NODRM。</p>
</li>
<li id="q-127-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>SANACT=3 選 Overwrite；OVRPAT 為 32-bit pattern；OWPASS=0 表示 16 次，1～15 表示該次數；OIPBP=1 在各次之間反轉 pattern。</p>
</li>
<li id="q-127-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>假設 OVRPAT=AAAAAAAAh、OWPASS=2、OIPBP=1，兩次分別使用 AAAAAAAAh 與 55555555h。再獨立決定是否請求 NDAS。</p>
</li>
<li id="q-127-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功後讀 SOS、完成 passes 與 GDE；若資料被 deallocate，Read 結果應依 deallocated LBA 規則，不保證仍讀出最後 pattern。</p>
</li>
<li id="q-127-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>NDAS=1 但被 NDI 禁止時，NODRM=0 拒絕為 Invalid Field；警告模式可執行並回報 Unexpected Deallocate。非 Overwrite 時覆寫欄位按規定忽略。</p>
</li>
<li id="q-127-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-127-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>依狀態轉移回報 Sanitize Operation Completed、Completed With Unexpected Deallocation 或 Entered Media Verification State，AER 的 LID=81h。 <a class="qa-rule-link" href="#common-sanitize_op-9">本冊完整規則</a></p>
</li>
<li id="q-127-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Sanitize Status 在啟動 CQE 張貼前更新，之後隨狀態轉移更新；它跨 Reset 與斷電保留。 <a class="qa-rule-link" href="#common-sanitize_op-10">本冊完整規則</a></p>
</li>
<li id="q-127-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援對應 PEL 事件時，進入 Processing 記錄 Sanitize Start（09h）；進入 Idle、Restricted Failure 或 Unrestricted Failure 記錄 Completion（0Ah）。 <a class="qa-rule-link" href="#common-sanitize_op-11">本冊完整規則</a></p>
</li>
<li id="q-127-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Sanitize 背景操作不因 Controller Level Reset 而中止。 <a class="qa-rule-link" href="#common-sanitize_op-12">本冊完整規則</a></p>
</li>
<li id="q-127-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 也不提供中止 Sanitize 的方法。 <a class="qa-rule-link" href="#common-sanitize_op-13">本冊完整規則</a></p>
</li>
<li id="q-127-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>斷電期間無法進行媒體處理，但重新供電後 Sanitize 仍須依保存的狀態繼續，不可當成從未開始。 <a class="qa-rule-link" href="#common-sanitize_op-14">本冊完整規則</a></p>
</li>
<li id="q-127-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Subsystem Sanitize 限制整個 subsystem 的相關存取；Namespace Sanitize 則針對指定 namespace，但所有可存取它的 controller 都受限制。 <a class="qa-rule-link" href="#common-sanitize_op-15">本冊完整規則</a></p>
</li>
<li id="q-127-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>比較要求的 pattern／passes、Log 保存的 SCDW10 與實際完成狀態；不要把 OWPASS=0 解成沒有做任何覆寫。</p>
</li>
<li id="q-127-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查 OWPASS 的特殊零值與 NDAS 是否有效，再分析讀回資料。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-sanitizeconfig">Base 2.4 §5.2.30.1.16</a> · <a href="#ref-nvmsanitize">NVM Command Set 1.3 §4.1.7, 5.12</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-128" data-question="128"><h2><a class="qa-qid" href="#q-128">Q128</a> SPROG、SOS、SANS 與 GDE／NDE 要怎麼一起看？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-128-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-128-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>進度比例、操作結果、狀態機位置與資料是否仍保持已清除，是四個不同問題。分開看，才能避免把 FFFFh 或 GDE=1 當成全部流程已完成。</p>
</li>
<li id="q-128-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>LID81h 依 NSID 選 subsystem 或指定 namespace；namespace 回覆中的 NDE 不能當成整個 subsystem 的 GDE。</p>
</li>
<li id="q-128-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>確認 SANICAP 與 verification 能力，再讀同一目標的整份一致狀態快照。</p>
</li>
<li id="q-128-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>SPROG／65536 是適用處理階段的完成比例；SOS 表示未開始、成功、進行中、失敗等；SANS 指狀態機位置；GDE／NDE 還會受後續使用者寫入影響。</p>
</li>
<li id="q-128-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先看 SOS 是否仍 Sanitizing，再看 SANS 在 Processing、Media Verification 或 Post-Verification Deallocation，最後才解讀 SPROG。</p>
</li>
<li id="q-128-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>SPROG=8000h 在適用處理階段代表約 50%；FFFFh 在未處理或 Media Verification 時也可出現，不是獨立成功證據。</p>
</li>
<li id="q-128-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Get Log 查錯目標可有 Invalid Namespace or Format；subsystem 正在清除時讀 namespace 狀態另有 Sanitize In Progress 限制。</p>
</li>
<li id="q-128-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-128-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>依狀態轉移回報 Sanitize Operation Completed、Completed With Unexpected Deallocation 或 Entered Media Verification State，AER 的 LID=81h。 <a class="qa-rule-link" href="#common-sanitize_op-9">本冊完整規則</a></p>
</li>
<li id="q-128-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Sanitize Status 在啟動 CQE 張貼前更新，之後隨狀態轉移更新；它跨 Reset 與斷電保留。 <a class="qa-rule-link" href="#common-sanitize_op-10">本冊完整規則</a></p>
</li>
<li id="q-128-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援對應 PEL 事件時，進入 Processing 記錄 Sanitize Start（09h）；進入 Idle、Restricted Failure 或 Unrestricted Failure 記錄 Completion（0Ah）。 <a class="qa-rule-link" href="#common-sanitize_op-11">本冊完整規則</a></p>
</li>
<li id="q-128-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Sanitize 背景操作不因 Controller Level Reset 而中止。 <a class="qa-rule-link" href="#common-sanitize_op-12">本冊完整規則</a></p>
</li>
<li id="q-128-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 也不提供中止 Sanitize 的方法。 <a class="qa-rule-link" href="#common-sanitize_op-13">本冊完整規則</a></p>
</li>
<li id="q-128-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>斷電期間無法進行媒體處理，但重新供電後 Sanitize 仍須依保存的狀態繼續，不可當成從未開始。 <a class="qa-rule-link" href="#common-sanitize_op-14">本冊完整規則</a></p>
</li>
<li id="q-128-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Subsystem Sanitize 限制整個 subsystem 的相關存取；Namespace Sanitize 則針對指定 namespace，但所有可存取它的 controller 都受限制。 <a class="qa-rule-link" href="#common-sanitize_op-15">本冊完整規則</a></p>
</li>
<li id="q-128-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>比較 SCDW10 與原要求，避免把先前一次清除的結果當成這次結果；再查看後續是否已有寫入清除 GDE／NDE。</p>
</li>
<li id="q-128-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查 SOS 與 SANS，接著才問 SPROG 的數值是否合理。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-nvmsanitize">NVM Command Set 1.3 §4.1.7, 5.12</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-129" data-question="129"><h2><a class="qa-qid" href="#q-129">Q129</a> Subsystem Sanitize 期間哪些 Command 允許執行？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-129-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-129-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>清除期間必須阻止使用者資料重新流入或被讀出，但仍保留查詢、通知與必要管理能力。允許清單因此有命令、選項與 Log 層級限制。</p>
</li>
<li id="q-129-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>限制適用於 subsystem 的全部 controller；換另一個 controller 不能繞過同一清除狀態。</p>
</li>
<li id="q-129-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 Figure144、Sanitize 狀態機，以及 NVM Figure200／201 的命令集補充。</p>
</li>
<li id="q-129-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Identify、AER、Get Features、queue 管理及指定 Log 可用；Sanitize Status 可查。PEL 與 vendor-specific Log 在此清除期間禁止，Self-test 也禁止；Error Log 的 LBA 必須回 0。</p>
</li>
<li id="q-129-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先判斷狀態，再按命令及 LID 套限制。一般 I/O 受阻；Flush 與 Media Verification Read 有特別規則，不能用「全部 I/O 一律禁止」蓋過例外。</p>
</li>
<li id="q-129-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>允許的命令正常完成；不允許的命令被拒絕，而背景 Sanitize 繼續。清除進度查詢建議不要過度頻繁，以免干擾進度。</p>
</li>
<li id="q-129-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>進行中通常回 Sanitize In Progress；進入 failure state 後須依命令類型與失敗規則處理，不能把進行中與失敗混為一個狀態。</p>
</li>
<li id="q-129-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-129-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>依狀態轉移回報 Sanitize Operation Completed、Completed With Unexpected Deallocation 或 Entered Media Verification State，AER 的 LID=81h。 <a class="qa-rule-link" href="#common-sanitize_op-9">本冊完整規則</a></p>
</li>
<li id="q-129-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Sanitize Status 在啟動 CQE 張貼前更新，之後隨狀態轉移更新；它跨 Reset 與斷電保留。 <a class="qa-rule-link" href="#common-sanitize_op-10">本冊完整規則</a></p>
</li>
<li id="q-129-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援對應 PEL 事件時，進入 Processing 記錄 Sanitize Start（09h）；進入 Idle、Restricted Failure 或 Unrestricted Failure 記錄 Completion（0Ah）。 <a class="qa-rule-link" href="#common-sanitize_op-11">本冊完整規則</a></p>
</li>
<li id="q-129-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Sanitize 背景操作不因 Controller Level Reset 而中止。 <a class="qa-rule-link" href="#common-sanitize_op-12">本冊完整規則</a></p>
</li>
<li id="q-129-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 也不提供中止 Sanitize 的方法。 <a class="qa-rule-link" href="#common-sanitize_op-13">本冊完整規則</a></p>
</li>
<li id="q-129-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>斷電期間無法進行媒體處理，但重新供電後 Sanitize 仍須依保存的狀態繼續，不可當成從未開始。 <a class="qa-rule-link" href="#common-sanitize_op-14">本冊完整規則</a></p>
</li>
<li id="q-129-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Subsystem Sanitize 限制整個 subsystem 的相關存取；Namespace Sanitize 則針對指定 namespace，但所有可存取它的 controller 都受限制。 <a class="qa-rule-link" href="#common-sanitize_op-15">本冊完整規則</a></p>
</li>
<li id="q-129-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>驗證同一限制是否在所有相關 controller 生效，也檢查允許的 Get Log 沒有洩漏應清除的使用者資料欄位。</p>
</li>
<li id="q-129-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認 LID 是否在允許清單，而非只看 Opcode=Get Log Page。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-sanitizerestrict">Base 2.4 §5.1.1–5.1.2 (PCIe commands)</a> · <a href="#ref-nvmsanitize">NVM Command Set 1.3 §4.1.7, 5.12</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-130" data-question="130"><h2><a class="qa-qid" href="#q-130">Q130</a> Sanitize 遇到 Reset 或 Power Loss 會繼續嗎？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-130-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-130-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Sanitize 的清除保證不能讓 Reset 或拔電變成逃脫途徑，因此背景操作會跨 Controller Level Reset 與 power cycle 繼續。</p>
</li>
<li id="q-130-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>持續的是所選清除目標的狀態機與操作，不是原本已消失的 Admin Queue 或 AER Request。</p>
</li>
<li id="q-130-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>重新讀 LID81h，確認 SOS、SANS、SCDW10、MVCNCLD 與目標 NSID；先恢復管理通道才能查詢。</p>
</li>
<li id="q-130-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>MVCNCLD 表示 Media Verification 被取消。傳輸層或 Subsystem Reset 的特定條件會設定它，不能把它解讀成 Sanitize 取消。</p>
</li>
<li id="q-130-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>重設前保存狀態；恢復後先讀同一目標的 Log，再判斷是否繼續處理、轉入 deallocation 或已完成，不直接重新開始另一筆操作。</p>
</li>
<li id="q-130-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>合理結果是背景操作持續或已依狀態機完成；斷電期間沒有處理進度並不違規，但恢復後不能忘記操作。</p>
</li>
<li id="q-130-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>仍在處理時重送啟動要求可能被 Sanitize In Progress 拒絕。不要將這個拒絕誤判成 Reset 後功能損壞。</p>
</li>
<li id="q-130-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-130-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>依狀態轉移回報 Sanitize Operation Completed、Completed With Unexpected Deallocation 或 Entered Media Verification State，AER 的 LID=81h。 <a class="qa-rule-link" href="#common-sanitize_op-9">本冊完整規則</a></p>
</li>
<li id="q-130-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Sanitize Status 在啟動 CQE 張貼前更新，之後隨狀態轉移更新；它跨 Reset 與斷電保留。 <a class="qa-rule-link" href="#common-sanitize_op-10">本冊完整規則</a></p>
</li>
<li id="q-130-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援對應 PEL 事件時，進入 Processing 記錄 Sanitize Start（09h）；進入 Idle、Restricted Failure 或 Unrestricted Failure 記錄 Completion（0Ah）。 <a class="qa-rule-link" href="#common-sanitize_op-11">本冊完整規則</a></p>
</li>
<li id="q-130-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Sanitize 背景操作不因 Controller Level Reset 而中止。 <a class="qa-rule-link" href="#common-sanitize_op-12">本冊完整規則</a></p>
</li>
<li id="q-130-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 也不提供中止 Sanitize 的方法。 <a class="qa-rule-link" href="#common-sanitize_op-13">本冊完整規則</a></p>
</li>
<li id="q-130-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>斷電期間無法進行媒體處理，但重新供電後 Sanitize 仍須依保存的狀態繼續，不可當成從未開始。 <a class="qa-rule-link" href="#common-sanitize_op-14">本冊完整規則</a></p>
</li>
<li id="q-130-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Subsystem Sanitize 限制整個 subsystem 的相關存取；Namespace Sanitize 則針對指定 namespace，但所有可存取它的 controller 都受限制。 <a class="qa-rule-link" href="#common-sanitize_op-15">本冊完整規則</a></p>
</li>
<li id="q-130-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>檢查原參數、目標及狀態延續，再與重新建立的 AER／Log 查詢區分。</p>
</li>
<li id="q-130-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認查的是原目標，而不是在 namespace 清除後改查 subsystem Log。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-131" data-question="131"><h2><a class="qa-qid" href="#q-131">Q131</a> 成功、失敗與 Failure Mode 在 Log 中如何區分？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-131-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-131-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>操作結果與目前狀態不一定一樣。離開 Failure Mode 後，狀態可以回 Idle，但最近一次清除仍然是失敗。</p>
</li>
<li id="q-131-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>以同一 target 的 SOS 與 SANS 判斷；namespace 失敗不能直接當成整個 subsystem 的最後清除結果。</p>
</li>
<li id="q-131-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀 LID81h；支援相關 verification 資訊時另讀 FAILS 與 MVCNCLD，補足在哪一階段失敗。</p>
</li>
<li id="q-131-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>SOS=001b 為 Sanitized，010b 為 Sanitizing，011b 為 Sanitize Failed，100b 為 Sanitized Unexpected Deallocate；SANS 再指出 Idle、Processing 或 Failure 等實際狀態。</p>
</li>
<li id="q-131-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先查看結果，再判斷當前是否仍被失敗限制阻擋。若 SANS=Idle 但 SOS=Failed，確認是否曾執行合法 Exit Failure Mode。</p>
</li>
<li id="q-131-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功不只看 SPROG；失敗也不是只看命令 CQE。背景失敗應由狀態與事件反映。</p>
</li>
<li id="q-131-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Restricted Failure 與 Unrestricted Failure 的允許復原動作不同。不能從兩者相同的 Failed 結果推論可使用相同恢復操作。</p>
</li>
<li id="q-131-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-131-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>依狀態轉移回報 Sanitize Operation Completed、Completed With Unexpected Deallocation 或 Entered Media Verification State，AER 的 LID=81h。 <a class="qa-rule-link" href="#common-sanitize_op-9">本冊完整規則</a></p>
</li>
<li id="q-131-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Sanitize Status 在啟動 CQE 張貼前更新，之後隨狀態轉移更新；它跨 Reset 與斷電保留。 <a class="qa-rule-link" href="#common-sanitize_op-10">本冊完整規則</a></p>
</li>
<li id="q-131-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援對應 PEL 事件時，進入 Processing 記錄 Sanitize Start（09h）；進入 Idle、Restricted Failure 或 Unrestricted Failure 記錄 Completion（0Ah）。 <a class="qa-rule-link" href="#common-sanitize_op-11">本冊完整規則</a></p>
</li>
<li id="q-131-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Sanitize 背景操作不因 Controller Level Reset 而中止。 <a class="qa-rule-link" href="#common-sanitize_op-12">本冊完整規則</a></p>
</li>
<li id="q-131-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 也不提供中止 Sanitize 的方法。 <a class="qa-rule-link" href="#common-sanitize_op-13">本冊完整規則</a></p>
</li>
<li id="q-131-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>斷電期間無法進行媒體處理，但重新供電後 Sanitize 仍須依保存的狀態繼續，不可當成從未開始。 <a class="qa-rule-link" href="#common-sanitize_op-14">本冊完整規則</a></p>
</li>
<li id="q-131-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Subsystem Sanitize 限制整個 subsystem 的相關存取；Namespace Sanitize 則針對指定 namespace，但所有可存取它的 controller 都受限制。 <a class="qa-rule-link" href="#common-sanitize_op-15">本冊完整規則</a></p>
</li>
<li id="q-131-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>將 SOS、SANS、原 AUSE 及後續復原要求放在一起，檢查是否存在不合法的狀態轉移。</p>
</li>
<li id="q-131-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先看 SANS，確認讀者所說的「失敗模式」真的是目前狀態，而不是歷史結果。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-132" data-question="132"><h2><a class="qa-qid" href="#q-132">Q132</a> Exit Failure Mode 能做什麼，不能做什麼？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-132-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-132-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Exit Failure Mode 可以在允許的情況下解除失敗狀態造成的存取限制，但它不會把未清除的資料補清，也不會把失敗結果改成成功。</p>
</li>
<li id="q-132-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>動作針對指定清除目標；subsystem 與 namespace 各有狀態機。</p>
</li>
<li id="q-132-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先讀 SANS 與原 SCDW10.AUSE。AUSE 決定操作進入 restricted 或 unrestricted 路徑。</p>
</li>
<li id="q-132-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>SANACT=001b 表示 Exit Failure Mode。它不是新一次 Block／Crypto／Overwrite 清除。</p>
</li>
<li id="q-132-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>Unrestricted Failure 可藉此回 Idle；Restricted Failure 必須以符合限制的新清除操作復原。Idle 收到此動作不視為錯誤。</p>
</li>
<li id="q-132-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>合法退出後可回到允許正常存取的狀態，但 SOS 仍可報告最近操作失敗，GDE／NDE 也不能憑退出動作設成成功清除。</p>
</li>
<li id="q-132-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Restricted Failure 的 Exit Failure Mode 會依目標回相應 Sanitize Failed 類型；不能用反覆重送或 Reset 繞過限制。</p>
</li>
<li id="q-132-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-132-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>依狀態轉移回報 Sanitize Operation Completed、Completed With Unexpected Deallocation 或 Entered Media Verification State，AER 的 LID=81h。 <a class="qa-rule-link" href="#common-sanitize_op-9">本冊完整規則</a></p>
</li>
<li id="q-132-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Sanitize Status 在啟動 CQE 張貼前更新，之後隨狀態轉移更新；它跨 Reset 與斷電保留。 <a class="qa-rule-link" href="#common-sanitize_op-10">本冊完整規則</a></p>
</li>
<li id="q-132-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援對應 PEL 事件時，進入 Processing 記錄 Sanitize Start（09h）；進入 Idle、Restricted Failure 或 Unrestricted Failure 記錄 Completion（0Ah）。 <a class="qa-rule-link" href="#common-sanitize_op-11">本冊完整規則</a></p>
</li>
<li id="q-132-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Sanitize 背景操作不因 Controller Level Reset 而中止。 <a class="qa-rule-link" href="#common-sanitize_op-12">本冊完整規則</a></p>
</li>
<li id="q-132-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 也不提供中止 Sanitize 的方法。 <a class="qa-rule-link" href="#common-sanitize_op-13">本冊完整規則</a></p>
</li>
<li id="q-132-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>斷電期間無法進行媒體處理，但重新供電後 Sanitize 仍須依保存的狀態繼續，不可當成從未開始。 <a class="qa-rule-link" href="#common-sanitize_op-14">本冊完整規則</a></p>
</li>
<li id="q-132-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Subsystem Sanitize 限制整個 subsystem 的相關存取；Namespace Sanitize 則針對指定 namespace，但所有可存取它的 controller 都受限制。 <a class="qa-rule-link" href="#common-sanitize_op-15">本冊完整規則</a></p>
</li>
<li id="q-132-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>驗證成功退出後的 SANS 與失敗歷史同時合理，而不是要求 Log 全部清零。</p>
</li>
<li id="q-132-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查原 AUSE 及現在 SANS，確認是否真的在允許退出的狀態。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-133" data-question="133"><h2><a class="qa-qid" href="#q-133">Q133</a> Sanitize 的 AER 與 PEL 應在何時產生？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-133-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-133-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>通知告訴 Host 狀態有重要變化，PEL 則保存歷史；兩者都不是原 Sanitize 命令的第二次完成。</p>
</li>
<li id="q-133-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>AER 由啟動操作的 controller 回報；事件參數與 PEL.NSID 協助辨別 subsystem 或 namespace 目標。</p>
</li>
<li id="q-133-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>確認通知支援、相關 AEC 設定、outstanding AER 與 PEL 支援。</p>
</li>
<li id="q-133-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>AER 的 AET=6、LID=81h；AEI=01h 是 Completed，02h 是 Unexpected Deallocation，03h 是 Entered Media Verification。DW1 依定義標示目標。</p>
</li>
<li id="q-133-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>啟動後記 Start；進入驗證先通知驗證階段；操作進入 Idle 或 Failure 才形成相應完成事件。收到通知後讀同一目標的 Log。</p>
</li>
<li id="q-133-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Completed 通知可以對應失敗完成，因此仍需讀 SOS／SANS。PEL Completion 同樣要看 SSTAT，不能只看事件名稱。</p>
</li>
<li id="q-133-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>沒有 AER Request 時不能期待立刻收到 CQE；事件是否保留與遮蔽仍遵循 AER 規則。也不要在 Sanitize 期間強迫讀取當時不允許的 PEL。</p>
</li>
<li id="q-133-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-133-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>依狀態轉移回報 Sanitize Operation Completed、Completed With Unexpected Deallocation 或 Entered Media Verification State，AER 的 LID=81h。 <a class="qa-rule-link" href="#common-sanitize_op-9">本冊完整規則</a></p>
</li>
<li id="q-133-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Sanitize Status 在啟動 CQE 張貼前更新，之後隨狀態轉移更新；它跨 Reset 與斷電保留。 <a class="qa-rule-link" href="#common-sanitize_op-10">本冊完整規則</a></p>
</li>
<li id="q-133-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援對應 PEL 事件時，進入 Processing 記錄 Sanitize Start（09h）；進入 Idle、Restricted Failure 或 Unrestricted Failure 記錄 Completion（0Ah）。 <a class="qa-rule-link" href="#common-sanitize_op-11">本冊完整規則</a></p>
</li>
<li id="q-133-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Sanitize 背景操作不因 Controller Level Reset 而中止。 <a class="qa-rule-link" href="#common-sanitize_op-12">本冊完整規則</a></p>
</li>
<li id="q-133-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 也不提供中止 Sanitize 的方法。 <a class="qa-rule-link" href="#common-sanitize_op-13">本冊完整規則</a></p>
</li>
<li id="q-133-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>斷電期間無法進行媒體處理，但重新供電後 Sanitize 仍須依保存的狀態繼續，不可當成從未開始。 <a class="qa-rule-link" href="#common-sanitize_op-14">本冊完整規則</a></p>
</li>
<li id="q-133-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Subsystem Sanitize 限制整個 subsystem 的相關存取；Namespace Sanitize 則針對指定 namespace，但所有可存取它的 controller 都受限制。 <a class="qa-rule-link" href="#common-sanitize_op-15">本冊完整規則</a></p>
</li>
<li id="q-133-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>對照事件的目標、原命令與 Log 狀態，區分「通知未送達」與「背景操作沒有完成」。</p>
</li>
<li id="q-133-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查 AEC、AER Request 及回報 controller，再判斷通知是否真的缺失。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-134" data-question="134"><h2><a class="qa-qid" href="#q-134">Q134</a> Namespace Sanitize 如何指定目標並確認其他 Namespace 未被清除？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-134-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-134-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Namespace Sanitize 提供單一 namespace 的 Crypto Erase，讓清除資料的範圍小於整個 subsystem。資料隔離與共享管理限制仍要分開驗證。</p>
</li>
<li id="q-134-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>NSID 指定一個 active namespace；其他 controller 若能存取同一 namespace，也必須遵守該目標的清除限制。</p>
</li>
<li id="q-134-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先查 LID05h 中 Admin Opcode8Ch 的 CSUPP，再查 SANICAP.CES 及所需的 NVERS／SPRRS 能力；查詢路徑見 Q118。接著確認 Active List、Write Protection 與 MNSOIP 並行上限，不能把命令受支援直接當成目標目前可執行。</p>
</li>
<li id="q-134-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Opcode8Ch、SANACT=100b；PREQ 在 CDW10 bit4，不是 subsystem Sanitize 的 bit11。用該 NSID 讀 LID81h 與 NDE。</p>
</li>
<li id="q-134-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先保存目標與非目標 namespace 的資料／狀態基準，再啟動並追蹤目標。完成後驗證目標清除結果，並確認非目標資料未因這次操作被清除。</p>
</li>
<li id="q-134-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>目標 NDE 可設為 1；其他 namespace 逐一清除也不能自行推成 GDE=1，因 subsystem 清除範圍還包含其他位置。</p>
</li>
<li id="q-134-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>NSID=0、FFFFFFFFh、inactive 或正在刪除會被 Invalid Namespace or Format 拒絕；寫入保護另回 Namespace is Write Protected。</p>
</li>
<li id="q-134-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-134-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>依狀態轉移回報 Sanitize Operation Completed、Completed With Unexpected Deallocation 或 Entered Media Verification State，AER 的 LID=81h。 <a class="qa-rule-link" href="#common-sanitize_op-9">本冊完整規則</a></p>
</li>
<li id="q-134-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Sanitize Status 在啟動 CQE 張貼前更新，之後隨狀態轉移更新；它跨 Reset 與斷電保留。 <a class="qa-rule-link" href="#common-sanitize_op-10">本冊完整規則</a></p>
</li>
<li id="q-134-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援對應 PEL 事件時，進入 Processing 記錄 Sanitize Start（09h）；進入 Idle、Restricted Failure 或 Unrestricted Failure 記錄 Completion（0Ah）。 <a class="qa-rule-link" href="#common-sanitize_op-11">本冊完整規則</a></p>
</li>
<li id="q-134-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Sanitize 背景操作不因 Controller Level Reset 而中止。 <a class="qa-rule-link" href="#common-sanitize_op-12">本冊完整規則</a></p>
</li>
<li id="q-134-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 也不提供中止 Sanitize 的方法。 <a class="qa-rule-link" href="#common-sanitize_op-13">本冊完整規則</a></p>
</li>
<li id="q-134-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>斷電期間無法進行媒體處理，但重新供電後 Sanitize 仍須依保存的狀態繼續，不可當成從未開始。 <a class="qa-rule-link" href="#common-sanitize_op-14">本冊完整規則</a></p>
</li>
<li id="q-134-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Subsystem Sanitize 限制整個 subsystem 的相關存取；Namespace Sanitize 則針對指定 namespace，但所有可存取它的 controller 都受限制。 <a class="qa-rule-link" href="#common-sanitize_op-15">本冊完整規則</a></p>
</li>
<li id="q-134-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>將資料內容隔離、目標 I/O 限制與全域韌體更新限制分別記錄；非目標資料不被清除，不代表所有管理命令都不受影響。</p>
</li>
<li id="q-134-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認測試真的送 8Ch 並指定正確 NSID，而不是誤用 84h 清除 subsystem。</p>
</li>
</ol>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/format-sanitize/zh-tw/#q-118">Q118</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-sanitizerestrict">Base 2.4 §5.1.1–5.1.2 (PCIe commands)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-135" data-question="135"><h2><a class="qa-qid" href="#q-135">Q135</a> Namespace Sanitize 遇到不存在、Inactive 或不支援的目標如何回應？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-135-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-135-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>錯誤可能來自命令不受支援、目標不合法、動作不支援或並行資源不足。這些原因不能統一寫成 Invalid Namespace。</p>
</li>
<li id="q-135-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>檢查指定 namespace 與 subsystem 目前的清除狀態；subsystem failure 也可能阻止新 namespace 操作。</p>
</li>
<li id="q-135-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先以 LID05h 中 8Ch 的 CSUPP 區分命令是否受支援，再以 SANICAP、Active／Allocated Lists、Write Protection 及 LID81h.MNSOIP 建立方法、目標與並行條件。這些欄位回答不同問題，不能用其中一個取代其他前提。</p>
</li>
<li id="q-135-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>SANACT 只有 Crypto Erase 與狀態管理動作，010b／011b 在 Namespace 命令是保留值。</p>
</li>
<li id="q-135-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先用合法基準驗證支援，再分別測非法 NSID、寫入保護、非法 SANACT 與並行超量；保留每次測試前的狀態。</p>
</li>
<li id="q-135-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>若啟動命令以非 Success 完成，不得為該命令開始清除、改寫該目標 Sanitize Status 或改變使用者資料。</p>
</li>
<li id="q-135-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>非法目標用 Invalid Namespace or Format；非法 SANACT 用 Invalid Field；超限用 Request Exceeds Maximum Namespace Sanitize Operations In Progress。原文 Figure104 列 3Ch，Figure455 列 12h，兩表有差異，不能擅自把其中一值當唯一驗收依據。</p>
</li>
<li id="q-135-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-135-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>依狀態轉移回報 Sanitize Operation Completed、Completed With Unexpected Deallocation 或 Entered Media Verification State，AER 的 LID=81h。 <a class="qa-rule-link" href="#common-sanitize_op-9">本冊完整規則</a></p>
</li>
<li id="q-135-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Sanitize Status 在啟動 CQE 張貼前更新，之後隨狀態轉移更新；它跨 Reset 與斷電保留。 <a class="qa-rule-link" href="#common-sanitize_op-10">本冊完整規則</a></p>
</li>
<li id="q-135-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援對應 PEL 事件時，進入 Processing 記錄 Sanitize Start（09h）；進入 Idle、Restricted Failure 或 Unrestricted Failure 記錄 Completion（0Ah）。 <a class="qa-rule-link" href="#common-sanitize_op-11">本冊完整規則</a></p>
</li>
<li id="q-135-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Sanitize 背景操作不因 Controller Level Reset 而中止。 <a class="qa-rule-link" href="#common-sanitize_op-12">本冊完整規則</a></p>
</li>
<li id="q-135-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 也不提供中止 Sanitize 的方法。 <a class="qa-rule-link" href="#common-sanitize_op-13">本冊完整規則</a></p>
</li>
<li id="q-135-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>斷電期間無法進行媒體處理，但重新供電後 Sanitize 仍須依保存的狀態繼續，不可當成從未開始。 <a class="qa-rule-link" href="#common-sanitize_op-14">本冊完整規則</a></p>
</li>
<li id="q-135-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Subsystem Sanitize 限制整個 subsystem 的相關存取；Namespace Sanitize 則針對指定 namespace，但所有可存取它的 controller 都受限制。 <a class="qa-rule-link" href="#common-sanitize_op-15">本冊完整規則</a></p>
</li>
<li id="q-135-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>除核對 Status，也驗證被拒絕的要求沒有啟動背景操作或改寫目標資料。</p>
</li>
<li id="q-135-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認是在驗證哪一個單獨失敗條件；並行數值爭議則保留原文兩處定位供查證。</p>
</li>
</ol>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/format-sanitize/zh-tw/#q-118">Q118</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-sanitizecmd">Base 2.4 §5.2.26–5.2.27</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a> · <a href="#ref-sanitizestate">Base 2.4 §8.1.27.1–8.1.27.5</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-command-8"><h3>命令完成、事件與紀錄 · DNR 與 More 應如何設定？</h3><p>只有收到 CQE，才有 DNR 與 More 可供判讀。DNR=1 表示相同命令即使重送到此 NVM subsystem 的任一 controller，仍預期會失敗；DNR=0 則只表示可能成功。除非個別錯誤條件另有明定，不能只看 Status 名稱就要求 DNR=1。More=1 表示 Error Information Log 有這筆命令的補充資訊。SCT=SC=0 時，DNR 應為 0。</p></article>
<article id="common-format_op-9"><h3>本主題的共用條件 · 是否產生 Asynchronous Event？</h3><p>Format 改變 namespace 屬性時，依支援與通知設定回報對應 Namespace Attribute Changed，並更新 Changed Namespace 清單；FPI 僅由 0 變非 0 或由非 0 變 0 時才符合相關變更通知條件，不是每個百分比都通知。</p></article>
<article id="common-format_op-10"><h3>本主題的共用條件 · 是否更新 Error Information Log 或其他 Log？</h3><p>成功後重新讀 Identify Namespace 的格式與容量，並查看 Changed Namespace 清單。錯誤時依 CQE.More 讀 Error Information；不能以一筆成功的 Get Log Page 取代 Format 本身的完成結果。</p></article>
<article id="common-format_op-11"><h3>本主題的共用條件 · 是否記錄於 Persistent Event Log？</h3><p>支援 PEL 與對應事件時，Format Start（07h）保存要求，Format Completion（08h）保存操作結果。Completion 的 FNVMS 與 INFO 必須一起讀；若原 Format 沒有 CQE，INFO 可為 0，不能直接解成格式化成功。</p></article>
<article id="common-format_op-12"><h3>本主題的共用條件 · Controller Reset 後是否保留或繼續？</h3><p>Controller Reset 結束舊命令通道，不能沿用原 Format 的 outstanding 狀態或等待舊 CQE。恢復後重新讀格式、FPI 與可取得的 Format Completion Event，確認媒體實際狀態；Reset 本身既不證明格式化成功，也不保證回復舊格式。</p></article>
<article id="common-format_op-13"><h3>本主題的共用條件 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>NVM Subsystem Reset 後先恢復通道，再逐一查詢原 Format 範圍內的 namespaces。不能只查提交命令的 controller，就假設所有受影響 namespace 都已完成或恢復。</p></article>
<article id="common-format_op-14"><h3>本主題的共用條件 · Power Cycle 後是否保留或繼續？</h3><p>Power Cycle 中斷時若沒有可信的 Format 成功完成，Host 應重新確認目前格式與可用性，必要時重新執行符合當前狀態的 Format。先前資料可能已被破壞，不能因命令沒有回成功就假設資料仍在。</p></article>
<article id="common-format_op-15"><h3>本主題的共用條件 · 是否影響其他 Controller 或 Namespace？</h3><p>依 SES 選擇 FNA.FNS 或 FNA.SENS，再與 NSID 一起決定範圍。同一共享 namespace 可由其他 controller 存取，因此需要協調相關 I/O；提交到某個 controller，不表示只影響它自己的資料。</p></article>
<article id="common-identify-12"><h3>查詢的重設與影響範圍 · Controller Reset 後是否保留或繼續？</h3><p>Controller Reset 會中止尚未完成的查詢。沒有收到回覆，不等於 controller 回傳全零資料；Host 應等查詢通道恢復後重新讀取，再逐欄分辨固定識別、目前配置與動態狀態。Reset 本身也不表示 namespace 已刪除。</p></article>
<article id="common-identify-13"><h3>查詢的重設與影響範圍 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>重設完成後，重新查詢受影響的 controller 與 namespace。NVM Subsystem Reset 重設的是通訊及控制狀態，不能直接推論所有儲存配置都回到出廠值。若期間還執行了其他管理操作，則另依該操作的規則確認變更。</p></article>
<article id="common-identify-14"><h3>查詢的重設與影響範圍 · Power Cycle 後是否保留或繼續？</h3><p>Power Cycle 後，重新查詢版本、能力、目前格式及附加清單。固定識別資訊與持續配置，不應當成一般暫存 Feature 處理。不過，若同時發生韌體啟用或配置變更，結果可能不同，因此要保留前後資料及事件時間，才能解釋差異。</p></article>
<article id="common-identify-15"><h3>查詢的重設與影響範圍 · 是否影響其他 Controller 或 Namespace？</h3><p>Identify 只讀取資訊，不會建立、格式化或附加 namespace。回覆描述哪個物件，由 CNS 與相關選擇欄位決定。不同 controller 的 Active List 可以不同，不能只因清單不同就判定資料損壞。</p></article>
<article id="common-sanitize_op-9"><h3>本主題的共用條件 · 是否產生 Asynchronous Event？</h3><p>依狀態轉移回報 Sanitize Operation Completed、Completed With Unexpected Deallocation 或 Entered Media Verification State，AER 的 LID=81h。由 Admin SQ 啟動時，僅啟動該操作的 controller 回報這次通知；仍須查看 Log 分辨成功、失敗或驗證階段。</p></article>
<article id="common-sanitize_op-10"><h3>本主題的共用條件 · 是否更新 Error Information Log 或其他 Log？</h3><p>Sanitize Status 在啟動 CQE 張貼前更新，之後隨狀態轉移更新；它跨 Reset 與斷電保留。用相同目標的 SOS、SANS、SPROG、SCDW10 及 GDE／NDE 比對，不以背景失敗要求原啟動命令再回第二筆 CQE。</p></article>
<article id="common-sanitize_op-11"><h3>本主題的共用條件 · 是否記錄於 Persistent Event Log？</h3><p>支援對應 PEL 事件時，進入 Processing 記錄 Sanitize Start（09h）；進入 Idle、Restricted Failure 或 Unrestricted Failure 記錄 Completion（0Ah）。Completion 也包含失敗，事件 NSID 可用來分辨 subsystem 與 namespace 目標。</p></article>
<article id="common-sanitize_op-12"><h3>本主題的共用條件 · Controller Reset 後是否保留或繼續？</h3><p>Sanitize 背景操作不因 Controller Level Reset 而中止。Host 重新建立查詢通道後讀同一目標的 LID81h。另需分辨 Reset 來源：傳輸層 Reset 等條件可能取消 Media Verification，使 MVCNCLD 設為 1，而不是取消整個清除操作。</p></article>
<article id="common-sanitize_op-13"><h3>本主題的共用條件 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>NVM Subsystem Reset 也不提供中止 Sanitize 的方法。操作的狀態與 Log 需要保留；如果原本要求 Media Verification，還要檢查 MVCNCLD 及後續 deallocation 階段。</p></article>
<article id="common-sanitize_op-14"><h3>本主題的共用條件 · Power Cycle 後是否保留或繼續？</h3><p>斷電期間無法進行媒體處理，但重新供電後 Sanitize 仍須依保存的狀態繼續，不可當成從未開始。恢復後查看 SOS／SANS 與進度，不能只見 SPROG=FFFFh 就宣告成功。</p></article>
<article id="common-sanitize_op-15"><h3>本主題的共用條件 · 是否影響其他 Controller 或 Namespace？</h3><p>Subsystem Sanitize 限制整個 subsystem 的相關存取；Namespace Sanitize 則針對指定 namespace，但所有可存取它的 controller 都受限制。共享韌體更新等操作另有全域限制，不能只因另一 namespace 的資料不被清除，就推論完全沒有影響。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-adminsupport"><strong>Base 2.4 · §3.1.3.4 (Figure 28 PCIe I/O-controller rows and O/M/P note only)</strong><br>文件頁 45–47 · PDF 71–73 · Figure 28</li>
<li id="ref-nsid"><strong>Base 2.4 · §3.2.1</strong><br>文件頁 78–81 · PDF 104–107</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-format"><strong>Base 2.4 · §5.1.1, 5.2.11</strong><br>文件頁 178–179, 206–209 · PDF 204–205, 232–235 · Figure 144, 194–196</li>
<li id="ref-sanitizerestrict"><strong>Base 2.4 · §5.1.1–5.1.2 (PCIe commands)</strong><br>文件頁 178–181 · PDF 204–207 · Figure 144–146</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>文件頁 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-getlog"><strong>Base 2.4 · §5.2.13–5.2.13.1.1</strong><br>文件頁 212–218 · PDF 238–244 · Figure 203–211</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-changedlog"><strong>Base 2.4 · §5.2.13.1.5</strong><br>文件頁 226 · PDF 252</li>
<li id="ref-commandseffects"><strong>Base 2.4 · §5.2.13.1.6</strong><br>文件頁 226–229 · PDF 252–255 · Figure 216–217</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-formatpel"><strong>Base 2.4 · §5.2.13.1.14.2.7–5.2.13.1.14.2.8</strong><br>文件頁 259–261 · PDF 285–287 · Figure 248–249</li>
<li id="ref-sanitizepel"><strong>Base 2.4 · §5.2.13.1.14.2.9–5.2.13.1.14.2.10</strong><br>文件頁 261–262 · PDF 287–288 · Figure 250–251</li>
<li id="ref-sanitizelog"><strong>Base 2.4 · §5.2.13.1.38</strong><br>文件頁 313–320 · PDF 339–346 · Figure 312</li>
<li id="ref-idcmd"><strong>Base 2.4 · §5.2.14.1</strong><br>文件頁 336–340 · PDF 362–366 · Figure 332–337</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>文件頁 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-sanitizecmd"><strong>Base 2.4 · §5.2.26–5.2.27</strong><br>文件頁 448–454 · PDF 474–480 · Figure 451–455</li>
<li id="ref-aec"><strong>Base 2.4 · §5.2.30.1.6</strong><br>文件頁 466–468 · PDF 492–494 · Figure 474</li>
<li id="ref-behavior"><strong>Base 2.4 · §5.2.30.1.15</strong><br>文件頁 475–477 · PDF 501–503 · Figure 491</li>
<li id="ref-sanitizeconfig"><strong>Base 2.4 · §5.2.30.1.16</strong><br>文件頁 477–478 · PDF 503–504 · Figure 492</li>
<li id="ref-nwp"><strong>Base 2.4 · §5.2.30.1.38, 8.1.18</strong><br>文件頁 512, 664–666 · PDF 538, 690–692 · Figure 541, 735–737</li>
<li id="ref-sanitizestate"><strong>Base 2.4 · §8.1.27.1–8.1.27.5</strong><br>文件頁 711–732 · PDF 737–758 · Figure 770–779</li>
<li id="ref-nvmformat"><strong>NVM Command Set 1.3 · §4.1.2</strong><br>文件頁 62–63 · PDF 62–63 · Figure 91</li>
<li id="ref-idns"><strong>NVM Command Set 1.3 · §4.1.5.1–4.1.5.4</strong><br>文件頁 84–107 · PDF 84–107 · Figure 123–130</li>
<li id="ref-nvmsanitize"><strong>NVM Command Set 1.3 · §4.1.7, 5.12</strong><br>文件頁 113, 173–175 · PDF 113, 173–175 · Figure 200–201</li>
</ul><h3>需要看欄位圖時</h3><p>以下連結可開啟對應的圖表教學，查閱欄位及判讀方式。每張圖保留固定的教學位置，方便之後反覆查詢。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/logs/zh-tw/#figure-b217">Base 2.4 Figure 217 · Commands Supported and Effects Data Structure</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/format-sanitize/en/">English</a><a href="/DOCS/nvme-question-bank/format-sanitize.html">繁中教學 HTML</a></nav>
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
