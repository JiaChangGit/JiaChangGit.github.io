---
layout: post
title: "NVMe 自問自答題庫：Get Features 與 Set Features"
date: 2026-10-01 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/features/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/features/en/">English</a><a href="/DOCS/nvme-question-bank/features.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q54–Q68</p><h1>Get Features 與 Set Features</h1><p class="qr-intro">設定 Feature 前，先確認它影響哪個物件、是否可變更，以及是否可保存。設定後，再分別確認命令成功、Current 讀回值、實際行為與重設後的恢復結果。本冊依這些步驟說明如何驗證設定，避免只看成功 CQE 就跳到功能一定正確的結論。</p><p>先練習，再展開解答。各題依需要使用文字、欄位判讀、比較或流程說明，不要求相同的回答項目。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Current 與 Saved：兩條不同的設定路徑</h2><p class="qa-takeaway">SV=0 只變更目前值；SV=1 才同時要求保存。重設後如何恢復，還要看 Feature 的作用範圍、保存能力及個別例外。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">動作</th><th scope="col">Current</th><th scope="col">Saved／下一次恢復</th></tr></thead><tbody><tr><td>教學起點：可保存的 Feature</td><td>A</td><td>Saved=A</td></tr><tr><td>Set B，SV=0，成功</td><td>B</td><td>仍是 A</td></tr><tr><td>發生會恢復 Saved 的重設</td><td>回到 A</td><td>A</td></tr><tr><td>Set C，SV=1，成功</td><td>C</td><td>更新成 C</td></tr><tr><td>再次發生相同重設</td><td>回到 C</td><td>C</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>這張表假設 Feature 可保存，而且所執行的重設會從 Saved 恢復 Current。若前提不同，就不能直接套用。例如 FID84h 不可保存，也沒有 Default，但 WPS=1 的基本保護仍會跨越 Power Cycle 保留；WPS=2 則在 Power Cycle 後解除。它們的持續性由保護模式本身決定。</p>
<p class="qa-citations">來源：<a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-054">Q54 · Feature 的 Current、Default、Saved Value 及 Supported Capabilities 分別代表什麼？</a></li>
<li><a href="#q-055">Q55 · Set Features 的 Save 位元如何影響 Controller Reset 與 Power Cycle 後的 Feature 值？</a></li>
<li><a href="#q-056">Q56 · 不支援的 Feature、不合法 Feature 值或 Controller 不支援 Save 時，應如何回應？</a></li>
<li><a href="#q-057">Q57 · Host 如何判斷某個 Feature 是否需要指定 NSID？</a></li>
<li><a href="#q-058">Q58 · Arbitration、Number of Queues 及 I/O Command Set Profile Feature 如何設定與驗證？</a></li>
<li><a href="#q-059">Q59 · Interrupt Coalescing 與 Interrupt Vector Configuration 如何設定與驗證？</a></li>
<li><a href="#q-060">Q60 · Volatile Write Cache 與 Write Atomicity Normal 控制什麼行為？</a></li>
<li><a href="#q-061">Q61 · Asynchronous Event Configuration 如何決定哪些事件需要回報？</a></li>
<li><a href="#q-062">Q62 · Power Management、Autonomous Power State Transition 及 Host Controlled Thermal Management 有何差異？</a></li>
<li><a href="#q-063">Q63 · Timestamp、Keep Alive Timer 及 Host Memory Buffer 如何設定與驗證？</a></li>
<li><a href="#q-064">Q64 · Host Behavior Support、Error Recovery 及 Read Recovery Level 有什麼用途？</a></li>
<li><a href="#q-065">Q65 · Namespace Write Protection 如何設定？不同保護模式在 Reset 與 Power Cycle 後是否保留？</a></li>
<li><a href="#q-066">Q66 · Set Features 成功後，為什麼還應使用 Get Features 確認？</a></li>
<li><a href="#q-067">Q67 · Firmware Activation、Namespace 刪除、Controller Reset 及 Power Cycle 後，Feature 應如何變化？</a></li>
<li><a href="#q-068">Q68 · Feature 宣告支援但 Get、Set 或實際功能行為不一致時，應如何驗證？</a></li>
</ol></section>
<article class="qa-question" id="q-054" data-question="54" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-054">Q54</a> Feature 的 Current、Default、Saved Value 及 Supported Capabilities 分別代表什麼？</h2>
<p class="qa-prompt">需求：確認 Volatile Write Cache Feature 是否提供、能否保存，以及目前有沒有啟用。這三個答案分別在哪一份回覆？先想好查詢順序，再展開解答。</p>
<details class="qa-answer" id="q-054-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-054-a-01">Current 是目前使用的值，Default 是預設值，Saved 是已保存的值；Supported Capabilities 則說明這項 Feature 能否變更或保存。前三者描述設定內容，最後一項描述能力，不能當成四份相同設定。</p><div class="qa-sections">
<section class="qa-section" id="q-054-s-01" data-answer-section="1"><h3><span>1.</span> 差別在哪裡</h3>
<span class="qa-anchor" id="q-054-a-02"></span><p>比較這些回覆時，必須使用相同 FID、相同作用範圍及對應的選擇欄位。例如，兩個不同 namespace 的 Current 值，本來就可能不同。</p>
<span class="qa-anchor" id="q-054-a-04"></span><p>SEL=0 Current、1 Default、2 Saved、3 Supported Capabilities。SEL=3 的 DW0 bit2／1／0 分別是 CHANG／NSSPEC／SVBL，不是 Feature 的工作值。</p>
</section>
<section class="qa-section" id="q-054-s-02" data-answer-section="2"><h3><span>2.</span> 如何選擇與確認</h3>
<span class="qa-anchor" id="q-054-a-03"></span><p>先分開查「這個 FID 是否提供」與「提供後有哪些設定能力」。Feature Identifiers Supported and Effects（LID12h）的 FSUPP 回答前者；Identify.ONCS.SSFS 表示是否支援 Save／Select 機制，支援時再用 Get Features.SEL=3 查 CHANG、NSSPEC 及 SVBL。SEL=3 的 DW0 bit0 是 SVBL，不是 FSUPP。</p>
<section class="qa-lookup" id="q-054-lookup"><h4>查詢範例：FSUPP、SVBL 與 Current.WCE 分別回答什麼？</h4>
<p>教學假設：CC.CSS=000b、UUID Index=0；Identify 顯示 LPA.MLPS=1、ONCS.SSFS=1、VWC.VWCP=1。本例只做 Get，不執行 Set Features 或改動快取。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">查詢步驟與原文位置</th><th scope="col">要取出的資訊</th><th scope="col">這一步能判斷什麼</th></tr></thead><tbody><tr><td>1 · Figure 200，文件頁 211／PDF 237</td><td>Volatile Write Cache 對應 FID06h；MLPS=1 也保證 LID12h 可讀。</td><td>找到 Feature 識別碼及查詢入口。VWCP=1 表示有快取，不等於快取目前已啟用。</td></tr><tr><td>2 · Figures 270～271，文件頁 276～278／PDF 302～304</td><td>讀 LID12h 完整 1024 bytes（NUMD=255）；FID06h 位於 4×6=24=18h，取該 entry bit0 FSUPP，假設為 1。</td><td>controller 宣告提供 FID06h。這裡尚未回答是否可保存，也還沒有讀到 WCE。</td></tr><tr><td>3 · Figures 198、201，文件頁 210、212／PDF 236、238</td><td>Get Features：Opcode0Ah、FID06h、SEL=3、NSID=0。假設成功 CQE 的 DW0=00000005h。</td><td>bit2 CHANG=1、bit1 NSSPEC=0、bit0 SVBL=1：可變更且可保存。這個 5 是能力 bitmap，不能解成快取工作值。</td></tr><tr><td>4 · Figure 471，文件頁 464～465／PDF 490～491</td><td>再送相同 FID 的 Get Features，但 SEL=0。假設 DW0=0，依 VWC 格式讀 bit0 WCE=0。</td><td>Feature 受支援、可保存，但快取目前未啟用。不能因 Current=0，就改判成 Feature 不支援；也不能拿它和 SEL=3 的 5 直接比較是否相等。</td></tr></tbody></table></div>
<p>三種 bit0 的名字與用途不同：LID12h entry 是 FSUPP，SEL=3 的 CQE 是 SVBL，本例 SEL=0 的 CQE 則是 WCE。判讀前必須連同 LID 或 FID、SEL 及回覆格式一起保存；只留下數字會失去意義。</p>
<p class="qa-citations">來源：<a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-vwc">Base 2.4 §5.2.30.1.4</a></p>
</section>
<span class="qa-anchor" id="q-054-a-05"></span><p>先查能力，再讀 Current。若要判斷重設後應使用哪個值，才進一步查 Saved 與 Default。Feature 不可保存或尚未有 Saved 值時，SEL=2 回傳 Default；若個別 Feature 本身沒有 Default，則依它的例外規則處理。</p>
<span class="qa-anchor" id="q-054-a-06"></span><p>例如 SEL=3 回傳 DW0=5，表示 CHANG=1、SVBL=1、NSSPEC=0，也就是可變更、可保存。NSSPEC=0 表示這個位元沒有指出 scope，仍需查該 FID 的 FSP 或規範定義；不能直接推成 controller scope。這個 5 也不是 Current 的工作值。</p>
</section>
<section class="qa-section" id="q-054-s-03" data-answer-section="3"><h3><span>3.</span> 哪些結論不能互相套用</h3>
<span class="qa-anchor" id="q-054-a-07"></span><p>不支援 FID 時，回報 Invalid Field（0/02h）；SEL=4～7 則是保留編碼。若 controller 不支援所要求的 SEL，不能將回傳內容當成有效的 CHANG 或 SVBL 來解讀。</p>
<span class="qa-anchor" id="q-054-a-16"></span><p>比較結果時，同時保留 FID、SEL 與回傳值。若只留下 DW0 的數字，之後就無法確認它是工作設定值，還是 Supported Capabilities 的能力 bitmap。</p>
</section>
</div>
<span class="qa-anchor" id="q-054-a-17"></span><span class="qa-anchor" id="q-054-a-08"></span><span class="qa-anchor" id="q-054-a-09"></span><span class="qa-anchor" id="q-054-a-10"></span><span class="qa-anchor" id="q-054-a-11"></span><span class="qa-anchor" id="q-054-a-12"></span><span class="qa-anchor" id="q-054-a-13"></span><span class="qa-anchor" id="q-054-a-14"></span><span class="qa-anchor" id="q-054-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/logs/zh-tw/#q-069">Q69</a> · <a href="/nvme/question-bank/logs/zh-tw/#q-081">Q81</a> · <a href="/nvme/question-bank/features/zh-tw/#q-055">Q55</a> · <a href="/nvme/question-bank/features/zh-tw/#q-060">Q60</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a> · <a href="#ref-vwc">Base 2.4 §5.2.30.1.4</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-055" data-question="55" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-055">Q55</a> Set Features 的 Save 位元如何影響 Controller Reset 與 Power Cycle 後的 Feature 值？</h2>
<p class="qa-prompt">先指明重設或中斷的方式，再分別判斷設定、進行中的操作與資料。</p>
<details class="qa-answer" id="q-055-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-055-a-01">Save 位元讓 Host 選擇：只改變目前使用的值，或同時更新日後恢復設定時使用的保存值。</p><div class="qa-sections">
<section class="qa-section" id="q-055-s-01" data-answer-section="1"><h3><span>1.</span> 先界定觸發方式與影響對象</h3>
<span class="qa-anchor" id="q-055-a-02"></span><p>保存的作用範圍由各 Feature 決定。針對 namespace 保存的設定，與針對 controller 保存的設定，不能當成同一份全域資料。</p>
<span class="qa-anchor" id="q-055-a-03"></span><p>先確認 ONCS.SSFS，再確認這個 FID 的 SVBL。controller 支援 Save 機制，不表示每一種 Feature 都可以保存。</p>
</section>
<section class="qa-section" id="q-055-s-02" data-answer-section="2"><h3><span>2.</span> 哪些狀態改變，恢復後怎麼處理</h3>
<span class="qa-anchor" id="q-055-a-04"></span><p>Set Features 的 SV=0 時，只改 Current，不改 Saved；SV=1 且設定成功時，則同時更新 Current 與 Saved。這兩種操作都不會把 Default 改成 Host 新設定的值。</p>
<span class="qa-anchor" id="q-055-a-05"></span><p>先確認保存能力，送出 Set 並等待成功，再分別讀取 Current 與 Saved。執行指定的重設後，依該 Feature 的作用範圍與例外規則，確認 Current 恢復成正確的值。</p>
<span class="qa-anchor" id="q-055-a-06"></span><p>例如原本 Saved=A，Host 以 SV=0 將 Current 改為 B，此時功能使用 B。之後若發生會從 Saved 恢復設定的重設，Current 應回到 A，而不是保留 B。</p>
</section>
<section class="qa-section" id="q-055-s-03" data-answer-section="3"><h3><span>3.</span> 如何驗證保留或恢復結果</h3>
<span class="qa-anchor" id="q-055-a-07"></span><p>Feature 不可保存，Host 卻使用 SV=1 時，必須回報 Feature Identifier Not Saveable（SCT=1, SC=0Dh）。controller 不能先回報保存成功，之後卻因原本不支援保存而遺失設定。</p>
<span class="qa-anchor" id="q-055-a-16"></span><p>目前是否生效、Saved 是否更新，以及重設後是否正確恢復，是三個不同驗證點。只讀到 Current=B，不能證明 Saved 也已變成 B。</p>
<span class="qa-anchor" id="q-055-a-17"></span><p>先核對原 Set 命令的 SV 及該 FID 的 SVBL，再確認發生的是哪一種重設，以及重設涵蓋哪些物件。</p>
</section>
</div>
<span class="qa-anchor" id="q-055-a-08"></span><span class="qa-anchor" id="q-055-a-09"></span><span class="qa-anchor" id="q-055-a-10"></span><span class="qa-anchor" id="q-055-a-11"></span><span class="qa-anchor" id="q-055-a-12"></span><span class="qa-anchor" id="q-055-a-13"></span><span class="qa-anchor" id="q-055-a-14"></span><span class="qa-anchor" id="q-055-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-056" data-question="56" data-answer-kind="error"><h2><a class="qa-qid" href="#q-056">Q56</a> 不支援的 Feature、不合法 Feature 值或 Controller 不支援 Save 時，應如何回應？</h2>
<p class="qa-prompt">先區分失敗條件，再判斷是否有規範明定的回報結果。</p>
<details class="qa-answer" id="q-056-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-056-a-01">不支援 Feature、Feature 目前不可變更、不可保存，以及設定值非法，是不同失敗原因。先分清楚是哪一種，才能選擇正確的 Status 與修正方法。</p><div class="qa-sections">
<section class="qa-section" id="q-056-s-01" data-answer-section="1"><h3><span>1.</span> 先區分是哪一種失敗</h3>
<span class="qa-anchor" id="q-056-a-02"></span><p>判斷時要看這次 Set 或 Get 使用的 FID、目標範圍及目前狀態，不能只根據 controller 型號就推論命令應成功。</p>
<span class="qa-anchor" id="q-056-a-04"></span><p>一起檢查 FID、SV、NSID、CDW11 及資料 buffer。有些 Feature 還需要額外的選擇欄位，因此只看 CQE DW0，無法確認原命令的全部參數是否合法。</p>
<span class="qa-anchor" id="q-056-a-07"></span><p>不支援的 FID 或已定義欄位的非法值，一般回報 0/02h；不可保存回報 1/0Dh；不可變更回報 1/0Eh。若對 controller scope 的 Feature 執行 Set，卻指定有效 NSID，則回報 1/0Fh。個別 FID 若對操作順序或狀態另有規定，優先依專用規則判斷。</p>
</section>
<section class="qa-section" id="q-056-s-02" data-answer-section="2"><h3><span>2.</span> 用哪些資料確認原因</h3>
<span class="qa-anchor" id="q-056-a-03"></span><p>使用 SEL=3 的能力資料前，先確認 ONCS.SSFS。CHANG=1 只表示這項 Feature 存在可變更的設定，不保證它進入永久狀態後仍可改回。</p>
<span class="qa-anchor" id="q-056-a-05"></span><p>先用合法的 Current 值建立比較基準，再分別測試不支援的 FID、非法設定值、SV=1 及作用範圍錯誤。每次只改一項，避免同一筆命令同時違反多條規則。</p>
</section>
<section class="qa-section" id="q-056-s-03" data-answer-section="3"><h3><span>3.</span> 結果與後續驗證</h3>
<span class="qa-anchor" id="q-056-a-06"></span><p>合法 Set 成功完成後，才表示設定已完成。對不可變更的 Feature 寫入與目前相同的值時，規範允許成功，也允許回報 Feature Not Changeable；驗證不能只接受其中一種結果。</p>
<span class="qa-anchor" id="q-056-a-16"></span><p>收到錯誤 completion 後，重新 Get，確認目前值符合該 Feature 的錯誤處理規則。回報錯誤不一定等於完全沒有副作用，必須依個別定義判斷。</p>
<span class="qa-anchor" id="q-056-a-17"></span><p>先確認測試命令是否同時包含多個非法條件。如果是，controller 可能合法地選擇其中一個錯誤回報，不能只因它沒回預想的那個 Status 就判錯。</p>
</section>
</div>
<span class="qa-anchor" id="q-056-a-08"></span><span class="qa-anchor" id="q-056-a-09"></span><span class="qa-anchor" id="q-056-a-10"></span><span class="qa-anchor" id="q-056-a-11"></span><span class="qa-anchor" id="q-056-a-12"></span><span class="qa-anchor" id="q-056-a-13"></span><span class="qa-anchor" id="q-056-a-14"></span><span class="qa-anchor" id="q-056-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-057" data-question="57" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-057">Q57</a> Host 如何判斷某個 Feature 是否需要指定 NSID？</h2>
<p class="qa-prompt">先選查詢介面與目標，再說明哪個回傳欄位能支持你的結論。</p>
<details class="qa-answer" id="q-057-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-057-a-01">設定 Feature 前，必須先確認它作用於哪個物件，才能正確填寫 NSID 及其他選擇欄位。</p><div class="qa-sections">
<section class="qa-section" id="q-057-s-01" data-answer-section="1"><h3><span>1.</span> 要查哪個對象、哪份資料</h3>
<span class="qa-anchor" id="q-057-a-02"></span><p>Feature 的作用範圍可能是 controller、namespace、NVM subsystem、NVM Set、Endurance Group 或其他管理物件，並非只有 controller 與 namespace 兩種。</p>
<span class="qa-anchor" id="q-057-a-03"></span><p>SEL=3 回傳 NSSPEC=1，表示 Feature 以 namespace 為範圍。若 NSSPEC=0，則還要查 Feature Identifiers Supported and Effects 的 scope，以及 Base Figure 466 或 NVM Figure 92，才能確認真正的作用對象。</p>
<span class="qa-anchor" id="q-057-a-04"></span><p>對 controller scope 的 Feature，Get 與 Set 可以使用 NSID=0 或 FFFFFFFFh。若改填有效 namespace ID，Get 可以回傳 controller 的值，但 Set 必須回報作用範圍錯誤。兩種命令不能套用完全相同的 NSID 判斷。</p>
</section>
<section class="qa-section" id="q-057-s-02" data-answer-section="2"><h3><span>2.</span> 查詢順序與回覆判讀</h3>
<span class="qa-anchor" id="q-057-a-05"></span><p>先確認 FID 的作用範圍，再填入 NSID 及其他物件選擇欄位。namespace scope 通常使用 active NSID；若使用 broadcast，Get 與 Set 的規則不同，multi-domain 配置也可能有額外限制。</p>
<span class="qa-anchor" id="q-057-a-06"></span><p>例如 FID05h Error Recovery 設定的是 namespace，FID01h Arbitration 設定的是 controller。即使兩者都在 CDW11 放入數值，也不能因此使用相同的 NSID 規則。</p>
</section>
<section class="qa-section" id="q-057-s-03" data-answer-section="3"><h3><span>3.</span> 證據不足或不一致時怎麼判斷</h3>
<span class="qa-anchor" id="q-057-a-07"></span><p>對 controller scope 的 Feature 執行 Set，卻給入有效 NSID 時，回報 Feature Not Namespace Specific（1/0Fh）。對 namespace scope 的 Feature 執行 Get，卻使用 FFFFFFFFh 時，一般回報 Invalid Namespace or Format（0/0Bh）；若個別 Feature 有例外，則依例外規則處理。</p>
<span class="qa-anchor" id="q-057-a-16"></span><p>NSSPEC=0 的 Feature 仍可能以 subsystem 或 NVM Set 為範圍。不能把這個值直接解釋為「所有 namespace 都使用同一個 controller 設定」。</p>
<span class="qa-anchor" id="q-057-a-17"></span><p>先讀取 Feature 的作用範圍定義，再檢查原命令的 NSID。若作用對象選錯，失敗不一定與 namespace 本身的狀態有關。</p>
</section>
</div>
<span class="qa-anchor" id="q-057-a-08"></span><span class="qa-anchor" id="q-057-a-09"></span><span class="qa-anchor" id="q-057-a-10"></span><span class="qa-anchor" id="q-057-a-11"></span><span class="qa-anchor" id="q-057-a-12"></span><span class="qa-anchor" id="q-057-a-13"></span><span class="qa-anchor" id="q-057-a-14"></span><span class="qa-anchor" id="q-057-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-058" data-question="58" data-answer-kind="process"><h2><a class="qa-qid" href="#q-058">Q58</a> Arbitration、Number of Queues 及 I/O Command Set Profile Feature 如何設定與驗證？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-058-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-058-a-01">Arbitration 控制排程參數，Number of Queues 協商 queue 配額，I/O Command Set Profile 則選擇可使用的命令集組合。三者用途不同，也各有合適的初始化時機。</p><div class="qa-sections">
<section class="qa-section" id="q-058-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-058-a-02"></span><p>這三種 Feature 都透過 controller 設定；不過，改變 Command Set Profile 還會影響 namespace 及命令集的可用性。</p>
<span class="qa-anchor" id="q-058-a-03"></span><p>Arbitration 要搭配 CAP.AMS 與 CC.AMS；Number of Queues 以成功 Set 的回覆確認實際配額；Command Set Profile 則先查 CAP.CSS.IOCSS 及 CNS1Ch 回傳的組合 vectors。</p>
<span class="qa-anchor" id="q-058-a-04"></span><p>FID01h 使用 AB、HPW、MPW、LPW 設定仲裁；FID07h 由 NSQR、NCQR 提出 queue 數量要求，再以 NSQA、NCQA 回報實際配置。FID19h 的 IOCSCI 則是命令集組合的索引，三者的數值不能使用相同方式解讀。</p>
</section>
<section class="qa-section" id="q-058-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-058-a-05"></span><p>依初始化流程，先選擇 Command Set Profile 並確認 namespace，再設定 Number of Queues，之後才建立 CQ 與 SQ。Arbitration 的參數則必須與 CC.AMS 及各 SQ 的 QPRIO 一起驗證。</p>
<span class="qa-anchor" id="q-058-a-06"></span><p>讀回設定時，使用相同 FID 及對應的選擇欄位。CC.CSS≠110b 時，Set FID19h 會成功，但不產生作用；CC.CSS=110b 時，才使用所選命令集組合。Profile index=0 表示第 0 組，不表示停用命令集。FID07h 回傳的配額也不等於已建立的 queue 數量。</p>
</section>
<section class="qa-section" id="q-058-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-058-a-07"></span><p>I/O queue 建立後再 Set FID07h，回報 0/0Ch。CC.CSS=110b 時，若 IOCSCI 選到內容為 0 的組合，或已附加的 namespace 使用了該組合不支援的命令集，FID19h 必須回報 Combination Rejected。規格對此 Status 有內部差異：Figure 104 列為 1/2Bh，Figure 554 列為 1/15h。因此，本題保留兩處資訊，不單憑其中一張表判定韌體違規。</p>
<span class="qa-anchor" id="q-058-a-16"></span><p>同時驗證設定值、實際可建立的 queue 範圍，以及可使用的命令集。三個 Feature 各自提供不同證據，不能用其中一項的 Get 結果代替另外兩項。</p>
</section>
</div>
<span class="qa-anchor" id="q-058-a-17"></span><span class="qa-anchor" id="q-058-a-08"></span><span class="qa-anchor" id="q-058-a-09"></span><span class="qa-anchor" id="q-058-a-10"></span><span class="qa-anchor" id="q-058-a-11"></span><span class="qa-anchor" id="q-058-a-12"></span><span class="qa-anchor" id="q-058-a-13"></span><span class="qa-anchor" id="q-058-a-14"></span><span class="qa-anchor" id="q-058-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-arbit">Base 2.4 §5.2.30.1.1</a> · <a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-profile">Base 2.4 §5.2.30.1.18</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-setcomplete">Base 2.4 §5.2.30 (Command Completion)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-059" data-question="59" data-answer-kind="process"><h2><a class="qa-qid" href="#q-059">Q59</a> Interrupt Coalescing 與 Interrupt Vector Configuration 如何設定與驗證？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-059-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-059-a-01">Interrupt Coalescing 讓 controller 合併中斷通知，在通知延遲與 Host 處理負擔之間取捨。CQE 已寫入的時間，與中斷實際產生的時間，因而不一定相同。</p><div class="qa-sections">
<section class="qa-section" id="q-059-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-059-a-02"></span><p>FID08h 控制 I/O interrupt coalescing；FID09h 則指定某個 vector 是否使用 coalescing。Admin CQ 不支援 coalescing，不能拿它套用相同的聚合預期。</p>
<span class="qa-anchor" id="q-059-a-03"></span><p>一起檢查 Create CQ 的 IEN／IV、PCIe 中斷模式及 mask。PCIe 規範要求支援這些 Feature，但實際如何合併通知，允許存在實作差異。</p>
<span class="qa-anchor" id="q-059-a-04"></span><p>FID08h 的 TIME 以 100 μs 為單位，THR 使用 zero-based 編碼；任一欄位為 0，都會隱含停用 coalescing。FID09h 透過 IV 指定 vector，CD=1 表示不對該 vector 聚合通知，不是遮蔽中斷。</p>
</section>
<section class="qa-section" id="q-059-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-059-a-05"></span><p>先透過 Create CQ 將 CQ 關聯到合法 vector，再設定 FID09h。設定 FID08h 後，以 Get Features 讀回確認，並一起觀察多筆 completion 的寫入時間與中斷通知行為。</p>
<span class="qa-anchor" id="q-059-a-06"></span><p>設定成功不代表每一種工作負載下，中斷都必須在 TIME 或 THR 指定的精確時點產生。PCIe 規範將這些參數的使用方式留給實作決定，甚至允許不實際執行聚合，因此不能把它們當成固定的通知時間保證。</p>
</section>
<section class="qa-section" id="q-059-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-059-a-07"></span><p>FID09h 指定的 IV 非法，或未關聯到既有 I/O CQ 時，應回報 Invalid Field（0/02h）。這與 Create CQ 所使用的 Invalid Interrupt Vector（1/08h）不同，要依失敗的是哪一條命令判斷。</p>
<span class="qa-anchor" id="q-059-a-16"></span><p>將 Get 值、CQ 配置、mask 與通知行為一起比對。即使 CD=1 已停用聚合，MSI-X mask 仍可能遮蔽中斷；沒有收到中斷，不一定表示 CD 設定失敗。</p>
</section>
</div>
<span class="qa-anchor" id="q-059-a-17"></span><span class="qa-anchor" id="q-059-a-08"></span><span class="qa-anchor" id="q-059-a-09"></span><span class="qa-anchor" id="q-059-a-10"></span><span class="qa-anchor" id="q-059-a-11"></span><span class="qa-anchor" id="q-059-a-12"></span><span class="qa-anchor" id="q-059-a-13"></span><span class="qa-anchor" id="q-059-a-14"></span><span class="qa-anchor" id="q-059-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-irqfeat">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-irq">PCIe Transport 1.4 §3.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-060" data-question="60" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-060">Q60</a> Volatile Write Cache 與 Write Atomicity Normal 控制什麼行為？</h2>
<p class="qa-prompt">先說出比較對象最重要的差別，並舉一個不能互相代用的例子。</p>
<details class="qa-answer" id="q-060-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-060-a-01">持久性問的是資料是否已進入非揮發儲存；原子性問的是一組 logical blocks 是否依規定單位完整更新。這是兩種不同保證，必須分開判斷。</p><div class="qa-sections">
<section class="qa-section" id="q-060-s-01" data-answer-section="1"><h3><span>1.</span> 差別在哪裡</h3>
<span class="qa-anchor" id="q-060-a-02"></span><p>FID06h 控制 controller 的揮發性寫入快取；FID0Ah 控制正常情況下的寫入原子性要求。設定 FID0Ah 不會直接改寫 namespace 宣告的原子寫入單位。</p>
<span class="qa-anchor" id="q-060-a-04"></span><p>FID06h.WCE=0 時，寫入的使用者資料必須符合持久性要求。FID0Ah.DN=1 則解除 AWUN／NAWUN 的正常寫入原子性要求，但不解除 AWUPF／NAWUPF 的斷電原子性要求。</p>
</section>
<section class="qa-section" id="q-060-s-02" data-answer-section="2"><h3><span>2.</span> 如何選擇與確認</h3>
<span class="qa-anchor" id="q-060-a-03"></span><p>先用 VWC 確認是否存在揮發性寫入快取，再查看 AWUN、AWUPF、namespace 的覆寫欄位及邊界資訊，判斷適用的原子性保證。</p>
<span class="qa-anchor" id="q-060-a-05"></span><p>先讀取能力與 namespace 格式，Set 成功後再 Get 確認。接著以符合原子單位及邊界的 Write 情境，比較規範允許的結果。若要明確區分新舊設定，應先等既有命令完成，再變更 Feature。</p>
<span class="qa-anchor" id="q-060-a-06"></span><p>WCE=0 不會讓任意大小的 Write 都具備原子性；DN=1 也不會自動讓已完成的資料具有持久性。兩個設定控制不同性質，不能互相替代。</p>
</section>
<section class="qa-section" id="q-060-s-03" data-answer-section="3"><h3><span>3.</span> 哪些結論不能互相套用</h3>
<span class="qa-anchor" id="q-060-a-07"></span><p>controller 沒有揮發性寫入快取，Host 卻 Get 或 Set FID06h 時，必須回報 Invalid Field（0/02h）。其他參數及 namespace 原子性條件，則依適用命令的規則判斷。</p>
<span class="qa-anchor" id="q-060-a-16"></span><p>一起查看 Current.WCE、Current.DN，以及 Identify 中對此 namespace 有效的原子單位。FUA 是個別命令的持久性要求，不會擴大原子寫入單位。</p>
</section>
</div>
<span class="qa-anchor" id="q-060-a-17"></span><span class="qa-anchor" id="q-060-a-08"></span><span class="qa-anchor" id="q-060-a-09"></span><span class="qa-anchor" id="q-060-a-10"></span><span class="qa-anchor" id="q-060-a-11"></span><span class="qa-anchor" id="q-060-a-12"></span><span class="qa-anchor" id="q-060-a-13"></span><span class="qa-anchor" id="q-060-a-14"></span><span class="qa-anchor" id="q-060-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-vwc">Base 2.4 §5.2.30.1.4</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-nvmatomic">NVM Command Set 1.3 §2.1.2–2.1.4</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-061" data-question="61" data-answer-kind="process"><h2><a class="qa-qid" href="#q-061">Q61</a> Asynchronous Event Configuration 如何決定哪些事件需要回報？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-061-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-061-a-01">Asynchronous Event Configuration 讓 Host 選擇要接收哪些狀態變更通知。不過，設定通知種類後，Host 仍須自行提交 Asynchronous Event Request，等待 controller 回報事件。</p><div class="qa-sections">
<section class="qa-section" id="q-061-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-061-a-02"></span><p>FID0Bh 設定的是此 controller 的通知行為。各種通知所描述的狀態，則可能屬於 SMART、namespace 或其他不同範圍的物件。</p>
<span class="qa-anchor" id="q-061-a-03"></span><p>OAES 表示選配事件支援，SMART 的警告也有相應能力；NVM 特定 bit 另見 NVM 規格。</p>
<span class="qa-anchor" id="q-061-a-04"></span><p>CDW11 的啟用位決定要接收哪些通知；AER completion 中的 AET、AEI、LID 則描述實際發生的事件。兩者用途及編碼不同，不能當成同一份 bitmap 解讀。</p>
</section>
<section class="qa-section" id="q-061-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-061-a-05"></span><p>先確認事件支援能力，設定合法的通知 mask，再提交 AER。事件條件成立並收到回報後，讀取事件資訊及對應 Log，依該事件的規則完成確認，並補送新的 AER，繼續接收後續通知。</p>
<span class="qa-anchor" id="q-061-a-06"></span><p>啟用通知時，如果事件條件已經成立，controller 也會依此 Feature 的規則回報。因此，可能收到的事件不只限於設定完成後才新發生的變化。</p>
</section>
<section class="qa-section" id="q-061-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-061-a-07"></span><p>嘗試啟用 controller 不支援的事件時，必須回報 Invalid Field（0/02h）。若只是沒有未完成的 AER 可供回報，導致 Host 尚未收到通知，則不是 Set Features 的錯誤 Status。</p>
<span class="qa-anchor" id="q-061-a-16"></span><p>一起檢查 OAES、Current mask、是否有等待中的 AER，以及事件是否仍處於遮蔽狀態。通知啟用位為 1，並不足以證明 Host 一定會立即收到事件。</p>
</section>
<section class="qa-section" id="q-061-s-04" data-answer-section="4"><h3><span>4.</span> Asynchronous Event 的通知條件</h3>
<span class="qa-anchor" id="q-061-a-09"></span><p>FID0Bh 用來設定通知，但每種事件仍有各自的發生條件與清除規則。它不是所有 Error 類型事件的總開關；讀取 Get Features，也不能代替提交新的 AER 來接收通知。</p>
</section>
</div>
<span class="qa-anchor" id="q-061-a-17"></span><span class="qa-anchor" id="q-061-a-08"></span><span class="qa-anchor" id="q-061-a-10"></span><span class="qa-anchor" id="q-061-a-11"></span><span class="qa-anchor" id="q-061-a-12"></span><span class="qa-anchor" id="q-061-a-13"></span><span class="qa-anchor" id="q-061-a-14"></span><span class="qa-anchor" id="q-061-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-062" data-question="62" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-062">Q62</a> Power Management、Autonomous Power State Transition 及 Host Controlled Thermal Management 有何差異？</h2>
<p class="qa-prompt">先說出比較對象最重要的差別，並舉一個不能互相代用的例子。</p>
<details class="qa-answer" id="q-062-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-062-a-01">Power Management 讓 Host 直接選擇 power state；APST 依閒置條件自動轉換狀態；HCTM 則依溫度進行熱管理。三者可能都影響功耗與效能，但觸發原因不同。</p><div class="qa-sections">
<section class="qa-section" id="q-062-s-01" data-answer-section="1"><h3><span>1.</span> 差別在哪裡</h3>
<span class="qa-anchor" id="q-062-a-02"></span><p>這些設定透過 controller 操作。多個 controller 共用同一 domain 時，功耗狀態可能互相影響，因此不能只觀察單一路徑就解釋全部變化。</p>
<span class="qa-anchor" id="q-062-a-04"></span><p>FID02h 選擇 PS 及相關限制。FID0Ch 的 APSTE 啟用一張 32-entry 表；每格的 ITPT 是在該狀態下的閒置時間，單位為 ms，ITPS 則指定要進入的非工作狀態。FID10h 的 TMT1 與 TMT2 是熱管理溫度門檻，單位為 Kelvin。</p>
</section>
<section class="qa-section" id="q-062-s-02" data-answer-section="2"><h3><span>2.</span> 如何選擇與確認</h3>
<span class="qa-anchor" id="q-062-a-03"></span><p>讀 NPSS／Power State Descriptors、APSTA 與 HCTMA、MNTMT／MXTMT。</p>
<span class="qa-anchor" id="q-062-a-05"></span><p>先查看可用狀態及進出延遲，再決定由 Host 選擇 PS，或使用 APST 表自動轉換。熱管理門檻另外設定；TMT1、TMT2 都非零時，必須符合 TMT1&lt;TMT2。APST 進入新狀態後，接著使用該新狀態所對應的閒置條件。</p>
<span class="qa-anchor" id="q-062-a-06"></span><p>Set FID02h 成功時，controller 已到達指定 PS；但若 APST 已啟用，之後仍可能再自動轉換狀態。HCTM 因溫度觸發的調整，也不表示 Host 另外送出了一筆 Power Management 命令。</p>
</section>
<section class="qa-section" id="q-062-s-03" data-answer-section="3"><h3><span>3.</span> 重設或斷電時，要確認什麼</h3>
<span class="qa-anchor" id="q-062-a-12"></span>
<span class="qa-anchor" id="q-062-a-14"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">觸發方式</th><th scope="col">這項操作或狀態會如何變化</th></tr></thead><tbody><tr><td>Controller Reset 後是否保留或繼續？</td><td>Power Management 與 APST 若不可保存，重設後依 Figure 466 回到預設；HCTM 即使不可保存，仍規定具有持續性。若 Feature 可保存，則改依 Saved 恢復規則判斷。同一 domain 有多個 controller 時，還要協調它們的控制設定。</td></tr><tr><td>Power Cycle 後是否保留或繼續？</td><td>不能假設這三個 FID 都會在斷電後清除。在不可保存的情況下，HCTM 具有持續性，Power Management 與 APST 則不持續；若 Feature 可保存，就依 Saved 恢復規則處理。</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-062-s-04" data-answer-section="4"><h3><span>4.</span> 哪些結論不能互相套用</h3>
<span class="qa-anchor" id="q-062-a-07"></span><p>不支援的 power state、非法 APST 目標，以及不符合範圍或順序的溫度門檻，依各欄位規則判定 Invalid Field（0/02h）。設定看似比較省電，也不能使非法參數變成合法。</p>
<span class="qa-anchor" id="q-062-a-16"></span><p>分別比對 Get Features 的設定、目前操作狀態、SMART 溫度與 HCTM 計數。單憑功耗下降，無法確定是 APST、Host 指定狀態，還是熱管理造成。</p>
</section>
</div>
<span class="qa-anchor" id="q-062-a-17"></span><span class="qa-anchor" id="q-062-a-08"></span><span class="qa-anchor" id="q-062-a-09"></span><span class="qa-anchor" id="q-062-a-10"></span><span class="qa-anchor" id="q-062-a-11"></span><span class="qa-anchor" id="q-062-a-13"></span><span class="qa-anchor" id="q-062-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a> · <a href="#ref-powerstates">Base 2.4 §8.1.19</a> · <a href="#ref-thermalpel">Base 2.4 §5.2.13.1.14.2.13</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-063" data-question="63" data-answer-kind="process"><h2><a class="qa-qid" href="#q-063">Q63</a> Timestamp、Keep Alive Timer 及 Host Memory Buffer 如何設定與驗證？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-063-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-063-a-01">Timestamp 提供事件的時間基準，Keep Alive Timer 監測通訊是否持續，HMB 則提供 controller 可專用的 Host 記憶體。三者解決的問題不同，需要各自的驗證方法。</p><div class="qa-sections">
<section class="qa-section" id="q-063-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-063-a-02"></span><p>Timestamp 與 Keep Alive 管理 controller 的時間相關狀態；HMB 還涉及 Host 記憶體的使用權，以及何時能安全回收記憶體。</p>
<span class="qa-anchor" id="q-063-a-03"></span><p>Timestamp 看 ONCS；Keep Alive 看 KAS 與 CTRATT.TBKAS；HMB 看 HMPRE、HMMIN、HMMINDS、HMMAXD。</p>
<span class="qa-anchor" id="q-063-a-04"></span><p>FID0Eh 使用 8-byte buffer 設定 48-bit Timestamp，單位為 ms。FID0Fh 的 KATO 也以 ms 表示，並依 KAS×100 ms 的單位向上取整。FID0Dh 則設定 EHM、MR、HSIZE，以及 descriptor 的位址與數量。</p>
</section>
<section class="qa-section" id="q-063-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-063-a-05"></span><p>設定 Timestamp 後再 Get，應將兩次操作間經過的時間納入比較。設定 KATO 後，Get 讀到的是實際取整後的值。HMB 則要先準備合法頁面再啟用，停用成功後才能回收；使用 MR=1 時，記憶體內容及 descriptors 都必須與先前相同。</p>
<span class="qa-anchor" id="q-063-a-06"></span><p>例如 KAS=10，Host 要求 KATO=1500 ms，實際會向上取整為 2000 ms。HMB 的 Get 則同時回傳 CQE 狀態與 attributes buffer，不能只讀一個開關值就認為取得了全部設定。</p>
</section>
<section class="qa-section" id="q-063-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-063-a-07"></span><p>HMB 已啟用卻再次要求 Enable 時，回報 Command Sequence Error（0/0Ch）；HMDLEC=0 時，回報 Invalid Field（0/02h）。PCIe 可以用 KATO=0 停用 Keep Alive，不能套用其他 transport 的強制啟用規則。</p>
<span class="qa-anchor" id="q-063-a-16"></span><p>Timestamp 要搭配 Origin 與 Synch 判讀，不能直接當成已同步的絕對時鐘。KATO 要比較取整後的 Current；HMB 則需一起確認能力、配置、EHM 狀態，以及 Host 是否仍保留原記憶體。</p>
</section>
</div>
<span class="qa-anchor" id="q-063-a-17"></span><span class="qa-anchor" id="q-063-a-08"></span><span class="qa-anchor" id="q-063-a-09"></span><span class="qa-anchor" id="q-063-a-10"></span><span class="qa-anchor" id="q-063-a-11"></span><span class="qa-anchor" id="q-063-a-12"></span><span class="qa-anchor" id="q-063-a-13"></span><span class="qa-anchor" id="q-063-a-14"></span><span class="qa-anchor" id="q-063-a-15"></span>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/persistent-events/zh-tw/#q-216">Q216</a> · <a href="/nvme/question-bank/keep-alive/zh-tw/#q-221">Q221</a> · <a href="/nvme/question-bank/memory/zh-tw/#q-226">Q226</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-064" data-question="64" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-064">Q64</a> Host Behavior Support、Error Recovery 及 Read Recovery Level 有什麼用途？</h2>
<p class="qa-prompt">先說出比較對象最重要的差別，並舉一個不能互相代用的例子。</p>
<details class="qa-answer" id="q-064-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-064-a-01">Host Behavior Support 告訴 controller，Host 能處理哪些擴充行為；Error Recovery 設定指定 namespace 的錯誤恢復屬性；Read Recovery Level 則選擇讀取錯誤的恢復策略。</p><div class="qa-sections">
<section class="qa-section" id="q-064-s-01" data-answer-section="1"><h3><span>1.</span> 差別在哪裡</h3>
<span class="qa-anchor" id="q-064-a-02"></span><p>FID16h 以 controller 為範圍，FID05h 以 namespace 為範圍。FID12h 則依支援的 NVM Set 模型，以 NVM Set 或 NVM subsystem 為範圍。</p>
<span class="qa-anchor" id="q-064-a-04"></span><p>FID16h 的 data buffer 含 ACRE、LBAFEE 等；FID05h.TLER 單位 100 ms、DULBE 在 bit16；FID12h 的 RRL 是等級碼，不是 RRLS bitmap。</p>
</section>
<section class="qa-section" id="q-064-s-02" data-answer-section="2"><h3><span>2.</span> 如何選擇與確認</h3>
<span class="qa-anchor" id="q-064-a-03"></span><p>ACRE 必須搭配相關能力使用。設定 DULBE 前，先查 namespace 的 NSFEAT.DAE；設定 Read Recovery Level 前，則先查 RRLS bitmap，確認要選的等級受支援。</p>
<span class="qa-anchor" id="q-064-a-05"></span><p>先確認能力，再設定對應欄位。TLER 從錯誤恢復開始時才計時，不能把它當成所有命令從提交起算的 timeout。設定 RRL 時，也要選擇受支援的目標與等級，再讀回確認。</p>
<span class="qa-anchor" id="q-064-a-06"></span><p>ACRE 允許使用適用的進階重試行為；DULBE 改變讀取未寫入或已 deallocate 區塊時的回應。選用 Fast Fail 則不表示每次都保證固定延遲，也不表示 controller 完全不能嘗試內部恢復。</p>
</section>
<section class="qa-section" id="q-064-s-03" data-answer-section="3"><h3><span>3.</span> 重設或斷電時，要確認什麼</h3>
<span class="qa-anchor" id="q-064-a-12"></span>
<span class="qa-anchor" id="q-064-a-14"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">觸發方式</th><th scope="col">這項操作或狀態會如何變化</th></tr></thead><tbody><tr><td>Controller Reset 後是否保留或繼續？</td><td>在不可保存的情況下，Host Behavior Support 與 Error Recovery 不具持續性，Read Recovery Level 則持續保留。若 Feature 可保存，就改依 Saved 及作用範圍對應的重設規則處理。</td></tr><tr><td>Power Cycle 後是否保留或繼續？</td><td>Power Cycle 後，重新讀取各 FID 的 Current。Read Recovery Level 即使不可保存，仍具有持續性，不能因為沒有 Saved 就要求它回到 0。Host Behavior Support 與 Error Recovery 則各依自己的恢復規則處理。</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-064-s-04" data-answer-section="4"><h3><span>4.</span> 哪些結論不能互相套用</h3>
<span class="qa-anchor" id="q-064-a-07"></span><p>不支援的等級或非法設定，依對應規則回報 Invalid Field（0/02h）等 Status。Command Interrupted（0/21h）只有在 ACRE=1 時才能回報，而且 DNR 必須為 0。</p>
<span class="qa-anchor" id="q-064-a-16"></span><p>LBAFEE 會影響擴充 LBA 格式如何呈現及使用。因此，controller 能力、Host 宣告支援的行為，以及 namespace 的實際格式，必須放在一起判讀。</p>
</section>
</div>
<span class="qa-anchor" id="q-064-a-17"></span><span class="qa-anchor" id="q-064-a-08"></span><span class="qa-anchor" id="q-064-a-09"></span><span class="qa-anchor" id="q-064-a-10"></span><span class="qa-anchor" id="q-064-a-11"></span><span class="qa-anchor" id="q-064-a-13"></span><span class="qa-anchor" id="q-064-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-behavior">Base 2.4 §5.2.30.1.15</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-rrl">Base 2.4 §5.2.30.1.12, 8.1.23</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-065" data-question="65" data-answer-kind="process"><h2><a class="qa-qid" href="#q-065">Q65</a> Namespace Write Protection 如何設定？不同保護模式在 Reset 與 Power Cycle 後是否保留？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-065-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-065-a-01">Namespace Write Protection 用來防止 namespace 被修改。不同模式分別提供可解除、直到 Power Cycle 才解除，以及永久的保護，必須分清楚它們的有效期間。</p><div class="qa-sections">
<section class="qa-section" id="q-065-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-065-a-02"></span><p>保護狀態屬於 namespace；其他可存取同一 namespace 的 controller 也必須遵守。它不是只影響某條 queue 的 Host 軟體旗標。</p>
<span class="qa-anchor" id="q-065-a-03"></span><p>Identify.NWPC 宣告支援哪些保護能力；WPC 中的 WPUPCC 與 PWPC 控制是否允許進入特定模式；Get FID84h 回傳的 WPS 才是目前保護狀態。能力、進入許可與實際狀態是三種不同資訊。</p>
<span class="qa-anchor" id="q-065-a-04"></span><p>WPS=0 表示無保護，1 表示基本保護，2 表示保護持續到 Power Cycle，3 表示永久保護。這項 Feature 不可保存，也沒有 Default；其持續性由模式本身定義，不能靠 SV=1 改變。</p>
</section>
<section class="qa-section" id="q-065-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-065-a-05"></span><p>先確認能力及進入該模式的許可，再針對 NSID 設定 WPS，並讀取 Current 確認。進入保護時，controller 必須將該 namespace 仍在揮發性儲存中的資料與 metadata 寫入非揮發媒體。</p>
<span class="qa-anchor" id="q-065-a-06"></span><p>設定成功後，受保護模式禁止的操作必須被拒絕；一般 Read 仍依可讀狀態處理。除了確認 Set 成功，也要核對實際命令行為是否符合該模式。</p>
</section>
<section class="qa-section" id="q-065-s-03" data-answer-section="3"><h3><span>3.</span> 重設或斷電時，要確認什麼</h3>
<span class="qa-anchor" id="q-065-a-12"></span>
<span class="qa-anchor" id="q-065-a-13"></span>
<span class="qa-anchor" id="q-065-a-14"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">觸發方式</th><th scope="col">這項操作或狀態會如何變化</th></tr></thead><tbody><tr><td>Controller Reset 後是否保留或繼續？</td><td>Controller Reset 會保留既有 WPS，包括 Until Power Cycle 模式。FID84h 不可使用 Save 保存，不表示 Controller Reset 會解除它的保護。</td></tr><tr><td>NVM Subsystem Reset 後是否保留或繼續？</td><td>NVM Subsystem Reset 與 Power Cycle 是不同事件。WPS 依狀態機規則保留，不能用 NVM Subsystem Reset 來解除 Until Power Cycle 保護。</td></tr><tr><td>Power Cycle 後是否保留或繼續？</td><td>實際發生 Power Cycle 後，WPS=2 會回到 No Write Protect；基本保護 WPS=1 與永久保護 WPS=3 則繼續保留。永久保護不能透過一般 Set 或 Reset 解除。</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-065-s-04" data-answer-section="4"><h3><span>4.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-065-a-07"></span><p>若嘗試改變 WPS=2 或 3 的狀態、缺少進入模式的許可位，或在 multi-domain 配置中要求被禁止的 WPS=2 轉換，回報 Feature Not Changeable（1/0Eh）。Get Default 回報 0/02h；執行受寫保護禁止的命令，則可回報 Namespace is Write Protected（0/20h）。</p>
<span class="qa-anchor" id="q-065-a-16"></span><p>CHANG=1 不表示 namespace 進入永久保護後仍可解除。另外，WPC 控制位在重設後的變化，與 namespace 已經具有的 WPS 狀態，是不同規則，不能互相推論。</p>
</section>
</div>
<span class="qa-anchor" id="q-065-a-17"></span><span class="qa-anchor" id="q-065-a-08"></span><span class="qa-anchor" id="q-065-a-09"></span><span class="qa-anchor" id="q-065-a-10"></span><span class="qa-anchor" id="q-065-a-11"></span><span class="qa-anchor" id="q-065-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-066" data-question="66" data-answer-kind="process"><h2><a class="qa-qid" href="#q-066">Q66</a> Set Features 成功後，為什麼還應使用 Get Features 確認？</h2>
<p class="qa-prompt">先排出操作順序，指出哪一步必須等待完成，才能進行下一步。</p>
<details class="qa-answer" id="q-066-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-066-a-01">Set 成功後再 Get，可以確認 controller 實際使用的值，以及它與 Host 要求值之間是否存在規範允許的換算。只看成功 Status，無法取得這些資訊。</p><div class="qa-sections">
<section class="qa-section" id="q-066-s-01" data-answer-section="1"><h3><span>1.</span> 操作前先準備什麼</h3>
<span class="qa-anchor" id="q-066-a-02"></span><p>Set 與 Get 必須針對相同 FID、相同作用範圍及對應的選擇欄位，而且中間沒有其他配置變更，才適合直接比較。Get Supported Capabilities 也不能拿來代替 Get Current。</p>
<span class="qa-anchor" id="q-066-a-03"></span><p>先確認這項 Feature 的支援能力及回覆格式。有些結果位於 CQE，有些位於資料 buffer，也有些需要同時讀取兩者。</p>
<span class="qa-anchor" id="q-066-a-04"></span><p>保留原 Set 命令的 SV、設定參數及 CQE 結果。接著以 Get Features.SEL=0 讀取 Current；若還要確認保存結果，再以 SEL=2 讀取 Saved。</p>
</section>
<section class="qa-section" id="q-066-s-02" data-answer-section="2"><h3><span>2.</span> 先後順序與完成條件</h3>
<span class="qa-anchor" id="q-066-a-05"></span><p>等待 Set 成功完成後再 Get，並排除其他 Host 同時修改共用設定的情況。Timestamp 等動態值會隨時間增加，應將經過時間納入比較，而不是要求逐 bit 相同。</p>
<span class="qa-anchor" id="q-066-a-06"></span><p>controller 不得在屬性尚未設定完成前，就回報 Set 成功。但成功後的實際值仍可能經過規範允許的處理，例如 KATO 向上取整，或 Number of Queues 回傳實際配置。因此，與原請求數字不同，不一定代表錯誤。</p>
</section>
<section class="qa-section" id="q-066-s-03" data-answer-section="3"><h3><span>3.</span> 未符合條件時如何處理</h3>
<span class="qa-anchor" id="q-066-a-07"></span><p>如果後續 Get 失敗，應保留它自己的 Status，不能用它取代原 Set 的成功結果。先檢查 Get 的選擇欄位、作用範圍，以及兩次命令之間是否發生 Reset。</p>
<span class="qa-anchor" id="q-066-a-16"></span><p>Get 能確認 Host 讀到的設定值；實際行為驗證則確認 controller 是否採用該設定。兩者提供不同證據，應互相配合，而不是反覆讀同一數值就當成已驗證全部功能。</p>
</section>
</div>
<span class="qa-anchor" id="q-066-a-17"></span><span class="qa-anchor" id="q-066-a-08"></span><span class="qa-anchor" id="q-066-a-09"></span><span class="qa-anchor" id="q-066-a-10"></span><span class="qa-anchor" id="q-066-a-11"></span><span class="qa-anchor" id="q-066-a-12"></span><span class="qa-anchor" id="q-066-a-13"></span><span class="qa-anchor" id="q-066-a-14"></span><span class="qa-anchor" id="q-066-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-setcomplete">Base 2.4 §5.2.30 (Command Completion)</a> · <a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-067" data-question="67" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-067">Q67</a> Firmware Activation、Namespace 刪除、Controller Reset 及 Power Cycle 後，Feature 應如何變化？</h2>
<p class="qa-prompt">先指明重設或中斷的方式，再分別判斷設定、進行中的操作與資料。</p>
<details class="qa-answer" id="q-067-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-067-a-01">Feature 在事件之後應保留或恢復成什麼值，要依事件種類與個別 Feature 規則判斷。不能一律假設全部清除，也不能一律假設全部保留。</p><div class="qa-sections">
<section class="qa-section" id="q-067-s-01" data-answer-section="1"><h3><span>1.</span> 先界定觸發方式與影響對象</h3>
<span class="qa-anchor" id="q-067-a-02"></span><p>先確認設定屬於 controller、namespace，還是其他共用管理物件，再分別追蹤 Current、Saved 與 Default。作用範圍不同，事件造成的影響也可能不同。</p>
<span class="qa-anchor" id="q-067-a-03"></span><p>查詢 SEL=3 的 SVBL，並參考 Base Figure 466 或 NVM Figure 92，再核對個別 FID 的特殊規定。Feature 不可用 Save 保存，不等於它的狀態一定無法跨越重設或斷電。</p>
</section>
<section class="qa-section" id="q-067-s-02" data-answer-section="2"><h3><span>2.</span> 哪些狀態改變，恢復後怎麼處理</h3>
<span class="qa-anchor" id="q-067-a-04"></span><p>記錄事件是否真的觸發 Controller Level Reset，以及是否影響整個 NVM subsystem。Namespace Delete 則是移除原物件；即使之後建立了相同 NSID，也不能視為舊 namespace 的設定自然延續。</p>
<span class="qa-anchor" id="q-067-a-05"></span><p>先保存操作前的設定，執行指定事件，等管理通道恢復後，再讀取 Current、Saved 及能力，最後驗證行為。若事件是 Firmware Activation，還要先確認使用哪種啟用方式，以及過程中是否伴隨 Reset。</p>
<span class="qa-anchor" id="q-067-a-06"></span><p>例如，可保存的 Feature 若只用 SV=0 修改 Current，重設後可能恢復成較舊的 Saved 值。HMB 需要重新配置；WPS=2 則在 Controller Reset 後保留，但會在 Power Cycle 後解除。這些差異都來自各自的規則。</p>
</section>
<section class="qa-section" id="q-067-s-03" data-answer-section="3"><h3><span>3.</span> 如何驗證保留或恢復結果</h3>
<span class="qa-anchor" id="q-067-a-07"></span><p>namespace 已刪除後，再 Get 或 Set 它的 Feature，依該 FID 與 NSID 的規則回應。不能只因無法讀取已刪除 NSID 的設定，就判定 controller 保存失敗。</p>
<span class="qa-anchor" id="q-067-a-16"></span><p>比較前後結果時，一起保留 namespace 身分、SV、作用範圍、重設原因及時間。只記錄「Feature 值不同」，不足以判斷這項變化是否合法。</p>
<span class="qa-anchor" id="q-067-a-17"></span><p>先確認前後查詢的是同一物件，再確認事件實際造成的重設範圍，是否就是測試預期的範圍。</p>
</section>
</div>
<span class="qa-anchor" id="q-067-a-08"></span><span class="qa-anchor" id="q-067-a-09"></span><span class="qa-anchor" id="q-067-a-10"></span><span class="qa-anchor" id="q-067-a-11"></span><span class="qa-anchor" id="q-067-a-12"></span><span class="qa-anchor" id="q-067-a-13"></span><span class="qa-anchor" id="q-067-a-14"></span><span class="qa-anchor" id="q-067-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-nsmanage">Base 2.4 §5.2.24–5.2.25, 8.1.17</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-068" data-question="68" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-068">Q68</a> Feature 宣告支援但 Get、Set 或實際功能行為不一致時，應如何驗證？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-068-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-068-a-01">用可重現且條件明確的情境，分辨矛盾來自能力宣告、設定方式、觀察方法，還是 controller 的實際行為。</p><div class="qa-sections">
<section class="qa-section" id="q-068-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-068-a-02"></span><p>固定 controller、FID、NSID 或其他選擇欄位，並確認配置在比較期間沒有改變，避免把不同作用範圍的值混在一起。</p>
<span class="qa-anchor" id="q-068-a-03"></span><p>交叉比對 Identify、Feature Identifiers Supported and Effects，以及 SEL=3 的能力資訊。NSSPEC=0 不一定表示 controller scope；CHANG=1 也不表示任何狀態下都可以變更。</p>
<span class="qa-anchor" id="q-068-a-04"></span><p>保留原 Set 與 Get 的 FID、SEL、SV、CDW11、資料 buffer 及 CQE。另外記錄開始驗證前，哪些命令已經提交但尚未完成，避免混用新舊設定下的行為。</p>
</section>
<section class="qa-section" id="q-068-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-068-a-17"></span><p>先確認 Get 沒有使用錯誤的 SEL 或 NSID，再確認拿來驗證行為的命令，確實是在 Set 成功後才提交。</p>
<span class="qa-anchor" id="q-068-a-05"></span><p>先查能力，再送出合法 Set，等待成功後讀取 Current，最後提交新命令驗證效果。Saved 及重設後的行為則另外驗證，每次只改一項條件，讓差異有明確原因。</p>
</section>
<section class="qa-section" id="q-068-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-068-a-06"></span><p>判斷一致性時，應接受規範允許的結果範圍。例如 KATO 可以取整、Timestamp 會隨時間改變，中斷聚合也允許實作差異；不能只因結果不等於原請求，就直接判錯。</p>
<span class="qa-anchor" id="q-068-a-07"></span><p>先分別排除不支援 FID（0/02h）、非法保存要求（1/0Dh）、不可變更（1/0Eh）及作用範圍錯誤（1/0Fh）。若同時存在多項錯誤，也要保留規範允許 controller 選擇其中一項回報的空間。</p>
<span class="qa-anchor" id="q-068-a-16"></span><p>提出不符合規範的結論時，應附上明確要求、已成立的前提、原始命令與回覆，以及能排除選擇欄位或先後順序誤用的證據。</p>
</section>
</div>
<span class="qa-anchor" id="q-068-a-08"></span><span class="qa-anchor" id="q-068-a-09"></span><span class="qa-anchor" id="q-068-a-10"></span><span class="qa-anchor" id="q-068-a-11"></span><span class="qa-anchor" id="q-068-a-12"></span><span class="qa-anchor" id="q-068-a-13"></span><span class="qa-anchor" id="q-068-a-14"></span><span class="qa-anchor" id="q-068-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-setcomplete">Base 2.4 §5.2.30 (Command Completion)</a> · <a href="#ref-irqfeat">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-effects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>

<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-keepalive"><strong>Base 2.4 · §3.9 (common and PCIe rules), 5.2.30.1.9</strong><br>文件頁 129–135, 471 · PDF 155–161, 497 · Figure 481</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>文件頁 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-getfeat"><strong>Base 2.4 · §5.2.12</strong><br>文件頁 209–212 · PDF 235–238 · Figure 197–202</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-effects"><strong>Base 2.4 · §5.2.13.1.6</strong><br>文件頁 226–229 · PDF 252–255 · Figure 216–217</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-thermalpel"><strong>Base 2.4 · §5.2.13.1.14.2.13</strong><br>文件頁 265–266 · PDF 291–292 · Figure 255</li>
<li id="ref-featureeffects"><strong>Base 2.4 · §5.2.13.1.18</strong><br>文件頁 276–278 · PDF 302–304 · Figure 270–271</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>文件頁 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-idlist"><strong>Base 2.4 · §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</strong><br>文件頁 387–399, 402–404 · PDF 413–425, 428–430 · Figure 342–355, 360–362</li>
<li id="ref-nsmanage"><strong>Base 2.4 · §5.2.24–5.2.25, 8.1.17</strong><br>文件頁 442–448, 660–664 · PDF 468–474, 686–690 · Figure 442–450</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>文件頁 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-arbit"><strong>Base 2.4 · §5.2.30.1.1</strong><br>文件頁 460 · PDF 486 · Figure 467</li>
<li id="ref-power"><strong>Base 2.4 · §5.2.30.1.2, 5.2.30.1.7</strong><br>文件頁 460–462, 468–469 · PDF 486–488, 494–495 · Figure 468–469, 475–478</li>
<li id="ref-vwc"><strong>Base 2.4 · §5.2.30.1.4</strong><br>文件頁 464–465 · PDF 490–491 · Figure 471</li>
<li id="ref-number"><strong>Base 2.4 · §5.2.30.1.5</strong><br>文件頁 465–466 · PDF 491–492 · Figure 472–473</li>
<li id="ref-aec"><strong>Base 2.4 · §5.2.30.1.6</strong><br>文件頁 466–468 · PDF 492–494 · Figure 474</li>
<li id="ref-timestamp"><strong>Base 2.4 · §5.2.30.1.8</strong><br>文件頁 469–471 · PDF 495–497 · Figure 479–480</li>
<li id="ref-thermal"><strong>Base 2.4 · §5.2.30.1.10</strong><br>文件頁 471–472 · PDF 497–498 · Figure 482</li>
<li id="ref-rrl"><strong>Base 2.4 · §5.2.30.1.12, 8.1.23</strong><br>文件頁 473, 689–690 · PDF 499, 715–716 · Figure 484–485, 755</li>
<li id="ref-behavior"><strong>Base 2.4 · §5.2.30.1.15</strong><br>文件頁 475–477 · PDF 501–503 · Figure 491</li>
<li id="ref-profile"><strong>Base 2.4 · §5.2.30.1.18</strong><br>文件頁 478–479 · PDF 504–505 · Figure 494–495</li>
<li id="ref-nwp"><strong>Base 2.4 · §5.2.30.1.38, 8.1.18</strong><br>文件頁 512, 664–666 · PDF 538, 690–692 · Figure 541, 735–737</li>
<li id="ref-irqfeat"><strong>Base 2.4 · §5.2.30.2.1–5.2.30.2.2</strong><br>文件頁 514–515 · PDF 540–541 · Figure 543–544</li>
<li id="ref-hmb"><strong>Base 2.4 · §5.2.30.2.3, 8.2.4</strong><br>文件頁 515–519, 744 · PDF 541–545, 770 · Figure 545–553</li>
<li id="ref-setcomplete"><strong>Base 2.4 · §5.2.30 (Command Completion)</strong><br>文件頁 519 · PDF 545 · Figure 554</li>
<li id="ref-create"><strong>Base 2.4 · §5.3.1–5.3.2</strong><br>文件頁 527–531 · PDF 553–557 · Figure 571–579</li>
<li id="ref-powerstates"><strong>Base 2.4 · §8.1.19</strong><br>文件頁 666–672 · PDF 692–698 · Figure 738–740</li>
<li id="ref-nvmatomic"><strong>NVM Command Set 1.3 · §2.1.2–2.1.4</strong><br>文件頁 14–20 · PDF 14–20 · Figure 3–9</li>
<li id="ref-nvmfeat"><strong>NVM Command Set 1.3 · §4.1.3.1–4.1.3.7</strong><br>文件頁 64–69 · PDF 64–69 · Figure 92–101</li>
<li id="ref-idns"><strong>NVM Command Set 1.3 · §4.1.5.1–4.1.5.4</strong><br>文件頁 84–107 · PDF 84–107 · Figure 123–130</li>
<li id="ref-irq"><strong>PCIe Transport 1.4 · §3.5</strong><br>文件頁 13–16 · PDF 13–16 · Figure 9</li>
</ul><h3>需要看欄位圖時</h3><p>以下連結可開啟對應的圖表教學，查閱欄位及判讀方式。每張圖保留固定的教學位置，方便之後反覆查詢。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/features/zh-tw/#figure-b473">Base 2.4 Figure 473 · Number of Queues – Completion Queue Entry Dword 0</a></li>
<li><a href="/nvme/figure-reference/features/zh-tw/#figure-b543">Base 2.4 Figure 543 · Interrupt Coalescing – Command Dword 11</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/features/en/">English</a><a href="/DOCS/nvme-question-bank/features.html">繁中教學 HTML</a></nav>
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
