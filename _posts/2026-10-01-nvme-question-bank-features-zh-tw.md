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
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–68</p>
<header><p class="qa-range">Q54–Q68</p><h1>Get Features 與 Set Features</h1><p class="qr-intro">先確認設定作用在哪裡、能不能改及保存，再執行 Set。成功完成、Current 回讀、實際行為與重設後恢復，都要各自確認；一次成功 CQE 無法替代這四個觀察。</p><p>先練習，再展開每題的 17 項解答。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可以指定的一份邏輯儲存空間。多個 controller 可以屬於同一 NVM subsystem（包含 controller 與非揮發儲存資源的整體）。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue 是提交佇列，Completion Queue 是完成佇列；SQE／CQE 是其中的一筆 entry。QID 識別 queue，CID 識別同一 SQ 內尚未完成的命令，NSID 識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 是可存取的控制或狀態欄位；Identify 查物件能力與屬性；Feature 查／設工作設定；Log Page 回報指定種類的狀態或紀錄。FID、LID、CNS、CSI 分別選 Feature、Log、Identify 結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 是第幾筆，通常由 0 起算；offset 是離起點多遠，要看單位。zero-based 數量欄位的實際數量＝編碼＋1，但不是每個寫 0 的欄位都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 指一項操作影響的物件範圍。retention 是狀態是否保留。Controller Reset（清 CC.EN）是一種 Controller Level Reset，簡稱 CLR；同一類 CLR 的不同觸發方式，Register 保留規則仍可能不同。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Current 與 Saved：兩條不同的設定路徑</h2><p class="qa-takeaway">SV=0 改現在；SV=1 才要求保存。重設恢復仍要配合 scope、saveable 與個別 Feature 例外。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">動作</th><th scope="col">Current</th><th scope="col">Saved／下一次恢復</th></tr></thead><tbody><tr><td>教學起點：可保存的 Feature</td><td>A</td><td>Saved=A</td></tr><tr><td>Set B，SV=0，成功</td><td>B</td><td>仍是 A</td></tr><tr><td>發生會恢復 Saved 的重設</td><td>回到 A</td><td>A</td></tr><tr><td>Set C，SV=1，成功</td><td>C</td><td>更新成 C</td></tr><tr><td>再次發生相同重設</td><td>回到 C</td><td>C</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>這張表刻意假設 Feature 可保存，且該重設適用 Saved 恢復；不能套到所有 Feature。例如 FID84h 不可保存且沒有 Default，但 WPS=1 的基本保護仍跨斷電持續，WPS=2 則在 Power Cycle 解除。</p>
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
<article class="qa-question" id="q-054" data-question="54"><h2><a class="qa-qid" href="#q-054">Q54</a> Feature 的 Current、Default、Saved Value 及 Supported Capabilities 分別代表什麼？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-054-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-054-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>分開正在使用的值、出廠預設、持續保存值及「能不能改／存」的能力；這四者不是四份相同設定。</p>
</li>
<li id="q-054-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>同一 FID、scope 與 selector 下比較才有意義；不同 namespace 的 Current 可能不同。</p>
</li>
<li id="q-054-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Identify.ONCS.SSFS 表示 Save／Select 支援；具備此機制後用 Get Features.SEL=3 查該 FID 的 CHANG、NSSPEC、SVBL。</p>
</li>
<li id="q-054-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>SEL=0 Current、1 Default、2 Saved、3 Supported Capabilities。SEL=3 的 DW0 bit2／1／0 分別是 CHANG／NSSPEC／SVBL，不是 Feature 的工作值。</p>
</li>
<li id="q-054-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先讀能力，再讀 Current；需要比較重設結果時才讀 Saved／Default。不可保存或尚無 Saved 時，SEL=2 回 Default；個別 Feature 沒有 Default 的例外另處理。</p>
</li>
<li id="q-054-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例如 SEL3 回 5 表示可改、可存、NSSPEC=0；不表示 Current=5。NSSPEC=0 也不能單獨推論一定是 controller scope。</p>
</li>
<li id="q-054-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援 FID 為 Invalid Field（0/02h）。SEL=4～7 是保留編碼；SEL 未支援時不能把能力查詢結果當成有效 CHANG／SVBL。</p>
</li>
<li id="q-054-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-054-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-054-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-054-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get 本身不產生 Set Feature Event；Set 則要確認此 FID 的記錄支援、是否成功及設定是否改變。 <a class="qa-rule-link" href="#common-feature_events-11">本冊完整規則</a></p>
</li>
<li id="q-054-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>依 scope、可保存能力及重設涵蓋範圍決定；整體與部分重設的恢復規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-054-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確定整個或部分 subsystem 受影響；不可保存但持續的值不會因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-054-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存值依 Saved 恢復；不可保存的值另查持續性及該 Feature 的例外。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-054-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-054-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>比對時同時保留 FID 與 SEL；只有回傳 DW0 數字沒有辦法知道是值還是能力 bitmap。</p>
</li>
<li id="q-054-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查 SEL，這通常比懷疑 Set 沒生效更早排除解碼錯誤。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-055" data-question="55"><h2><a class="qa-qid" href="#q-055">Q55</a> Set Features 的 Save 位元如何影響 Controller Reset 與 Power Cycle 後的 Feature 值？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-055-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-055-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>讓 Host 決定只改目前值，或同時更新下次恢復時使用的持續值。</p>
</li>
<li id="q-055-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>保存依 Feature scope；namespace-scoped 保存與 controller-scoped 保存不能混成一份全域設定。</p>
</li>
<li id="q-055-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>確認 ONCS.SSFS 與此 FID 的 SVBL；「裝置支援 Save」不保證每個 Feature 都可保存。</p>
</li>
<li id="q-055-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Set CDW10.SV=0 改 Current、不改 Saved；SV=1 成功時改 Current 與 Saved。Default 不因此變成 Host 設的值。</p>
</li>
<li id="q-055-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先查支援，Set 並等待完成，再分別 Get Current／Saved；經指定重設後依 scope 及例外驗 Current。</p>
</li>
<li id="q-055-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例：Saved=A，SV=0 改成 B，目前應使用 B；符合 Saved 恢復條件的重設後回 A，不是 B。</p>
</li>
<li id="q-055-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不可保存卻 SV=1 必須回 Feature Identifier Not Saveable（SCT=1, SC=0Dh）；不能默默成功後遺失設定。</p>
</li>
<li id="q-055-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-055-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-055-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-055-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get 本身不產生 Set Feature Event；Set 則要確認此 FID 的記錄支援、是否成功及設定是否改變。 <a class="qa-rule-link" href="#common-feature_events-11">本冊完整規則</a></p>
</li>
<li id="q-055-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>依 scope、可保存能力及重設涵蓋範圍決定；整體與部分重設的恢復規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-055-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確定整個或部分 subsystem 受影響；不可保存但持續的值不會因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-055-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存值依 Saved 恢復；不可保存的值另查持續性及該 Feature 的例外。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-055-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-055-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>保存成功、目前生效與重設後恢復是三個驗證點；僅 Get Current=B 不證明 Saved=B。</p>
</li>
<li id="q-055-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先看原 Set 的 SV 與該 FID 的 SVBL，再看發生的是哪種、哪個範圍的重設。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-056" data-question="56"><h2><a class="qa-qid" href="#q-056">Q56</a> 不支援的 Feature、不合法 Feature 值或 Controller 不支援 Save 時，應如何回應？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-056-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-056-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>區分不支援功能、不能改、不能保存與值不合法；它們有不同原因和修正方法。</p>
</li>
<li id="q-056-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>針對該 FID、目標 scope、目前狀態與此次 Set／Get，不是只看 controller 型號。</p>
</li>
<li id="q-056-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Get SEL3 的能力需配合 ONCS.SSFS；CHANG=1 只代表至少有可改的值，不保證目前進入的永久狀態仍可改。</p>
</li>
<li id="q-056-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>檢查 FID、SV、NSID、CDW11 及資料 buffer；有些 Feature 需要特定 selector，不能只檢查 DW0。</p>
</li>
<li id="q-056-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>用合法 Current 建基準，再分開測不支援 FID、非法值、SV=1、scope 錯誤；避免一筆同時違反多項。</p>
</li>
<li id="q-056-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>合法 Set 完成後才是已設定；對不可改 Feature 寫相同值，規範允許成功或 Feature Not Changeable，不能只接受其中一種。</p>
</li>
<li id="q-056-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援 FID／非法定義值：0/02h；不可保存：1/0Dh；不可改：1/0Eh；controller-scope 的 Set 卻給有效 NSID：1/0Fh。個別 FID 的順序或狀態錯誤優先。</p>
</li>
<li id="q-056-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-056-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-056-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-056-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get 本身不產生 Set Feature Event；Set 則要確認此 FID 的記錄支援、是否成功及設定是否改變。 <a class="qa-rule-link" href="#common-feature_events-11">本冊完整規則</a></p>
</li>
<li id="q-056-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>依 scope、可保存能力及重設涵蓋範圍決定；整體與部分重設的恢復規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-056-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確定整個或部分 subsystem 受影響；不可保存但持續的值不會因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-056-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存值依 Saved 恢復；不可保存的值另查持續性及該 Feature 的例外。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-056-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-056-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>錯誤完成後重新 Get，確認結果符合那個 Feature 的錯誤處理；不要把回錯誤與一定完全沒有副作用畫等號。</p>
</li>
<li id="q-056-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先排除測例同時非法的情況，否則不同合法錯誤碼可能被誤判。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-057" data-question="57"><h2><a class="qa-qid" href="#q-057">Q57</a> Host 如何判斷某個 Feature 是否需要指定 NSID？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-057-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-057-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>在寫設定前選對作用對象，避免把 controller 設定誤送成 namespace 設定。</p>
</li>
<li id="q-057-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Feature scope 可為 controller、namespace、subsystem、Set、Group 或其他管理物件；不是只有兩種。</p>
</li>
<li id="q-057-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>SEL3.NSSPEC=1 表示 namespace scope；=0 時再看 Feature Identifiers Supported and Effects 的 scope 及 Figure 466／NVM Figure92。</p>
</li>
<li id="q-057-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>controller scope 的 Get／Set 可用 NSID=0 或 FFFFFFFFh；有效 namespace ID 用於 controller-scope Get 可回 controller 值，但 Set 要回 scope 錯誤。</p>
</li>
<li id="q-057-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先確認 FID scope，再填 NSID 與其他物件 selector。namespace scope 通常用 active NSID；broadcast Get 與 Set 的規則不同，multi-domain 還有限制。</p>
</li>
<li id="q-057-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例：FID05h Error Recovery 設 namespace，FID01h Arbitration 設 controller；兩者即使 CDW11 都是數值也不能共用相同 NSID 規則。</p>
</li>
<li id="q-057-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>controller-scope Set 給有效 NSID：Feature Not Namespace Specific（1/0Fh）。namespace-scope Get 用 FFFFFFFFh 一般為 Invalid Namespace or Format（0/0Bh），個別例外優先。</p>
</li>
<li id="q-057-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-057-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-057-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-057-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get 本身不產生 Set Feature Event；Set 則要確認此 FID 的記錄支援、是否成功及設定是否改變。 <a class="qa-rule-link" href="#common-feature_events-11">本冊完整規則</a></p>
</li>
<li id="q-057-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>依 scope、可保存能力及重設涵蓋範圍決定；整體與部分重設的恢復規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-057-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確定整個或部分 subsystem 受影響；不可保存但持續的值不會因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-057-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存值依 Saved 恢復；不可保存的值另查持續性及該 Feature 的例外。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-057-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-057-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>NSSPEC=0 與 subsystem／Set scope 可以同時成立，不能把它解成「所有 namespace 都套同一個 controller 值」。</p>
</li>
<li id="q-057-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先看 scope 定義，再檢查原命令 NSID，不先猜 namespace 是否壞掉。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-058" data-question="58"><h2><a class="qa-qid" href="#q-058">Q58</a> Arbitration、Number of Queues 及 I/O Command Set Profile Feature 如何設定與驗證？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-058-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-058-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>三者分別控制排程參數、queue 配額與可使用的 command-set 組合，必須放在正確初始化階段。</p>
</li>
<li id="q-058-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>本題三個 Feature 都以 controller 為作用入口，但改 Profile 會影響 namespace 與命令集可用性。</p>
</li>
<li id="q-058-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Arbitration 看 CAP.AMS／CC.AMS；Number of Queues 看成功 Set 回覆；Profile 先看 CAP.CSS.IOCSS 與 CNS1Ch vectors。</p>
</li>
<li id="q-058-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>FID01h：AB／HPW／MPW／LPW；FID07h：NSQR／NCQR→NSQA／NCQA；FID19h：IOCSCI 是組合 index。</p>
</li>
<li id="q-058-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>按初始化流程先選 Command Set Profile、確認 namespace，再配置 Number of Queues 並建 CQ／SQ；Arbitration 參数與 CC.AMS／QPRIO 協同驗證。</p>
</li>
<li id="q-058-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Get 回讀需用同 FID 與 selector。CC.CSS≠110b 時，Set FID19h 成功但沒有作用；CC.CSS=110b 時才使用選到的組合。Profile index=0 指第 0 組，不代表停用命令集；FID07h 的配額則不代表已建立 queue 數。</p>
</li>
<li id="q-058-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>FID07h 建 queue 後再 Set 是 0/0Ch。CC.CSS=110b 時，若 IOCSCI 選到值為 0 的組合，或已 attach 的 namespace 使用了該組合不支援的命令集，FID19h 須回 Combination Rejected。注意規格內部差異：Figure104 將 Combination Rejected 列為 1/2Bh，Figure554 列為 1/15h；本題保留此差異，不僅靠其中一表判韌體違規。</p>
</li>
<li id="q-058-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-058-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-058-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-058-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get 本身不產生 Set Feature Event；Set 則要確認此 FID 的記錄支援、是否成功及設定是否改變。 <a class="qa-rule-link" href="#common-feature_events-11">本冊完整規則</a></p>
</li>
<li id="q-058-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>依 scope、可保存能力及重設涵蓋範圍決定；整體與部分重設的恢復規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-058-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確定整個或部分 subsystem 受影響；不可保存但持續的值不會因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-058-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存值依 Saved 恢復；不可保存的值另查持續性及該 Feature 的例外。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-058-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-058-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>同時驗設定、可建立 queue 範圍與實際可用命令集；三個 Feature 的 Get 值不能互相代替。</p>
</li>
<li id="q-058-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認順序：是否在已建 I/O queue 後才想重新分配數量。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-arbit">Base 2.4 §5.2.30.1.1</a> · <a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-profile">Base 2.4 §5.2.30.1.18</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-setcomplete">Base 2.4 §5.2.30 (Command Completion)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-059" data-question="59"><h2><a class="qa-qid" href="#q-059">Q59</a> Interrupt Coalescing 與 Interrupt Vector Configuration 如何設定與驗證？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-059-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-059-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>以可接受的通知延遲換取較低的中斷處理負擔；completion 張貼與 IRQ 產生不是同一時間點。</p>
</li>
<li id="q-059-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>FID08h 控制 I/O interrupt coalescing；FID09h 對指定 vector 決定是否套用 coalescing。Admin CQ 不支援 coalescing。</p>
</li>
<li id="q-059-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>檢查 CQ.IEN／IV、PCIe interrupt 模式及 mask。PCIe 規範要求支援這些 Feature，但聚合演算法可以有實作差異。</p>
</li>
<li id="q-059-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>FID08h：TIME 單位 100 μs、THR 為 zero-based；任一為 0 會隱含停用 coalescing。FID09h：IV 與 CD，CD=1 是不聚合，不是遮蔽中斷。</p>
</li>
<li id="q-059-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先以 Create CQ 關聯合法 vector，再 Set FID09h；設定 FID08h 後 Get 回讀，以多筆 completion 的時間與 IRQ 行為一起觀察。</p>
</li>
<li id="q-059-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>參數成功生效，但不能把 TIME／THR 當成對每個 workload 絕對精準的中斷時刻；PCIe 描述其使用方式為 implementation specific，甚至可不實作聚合。</p>
</li>
<li id="q-059-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>FID09h 的 IV 非法或未關聯既有 I/O CQ，應回 Invalid Field（0/02h）；這不同於 Create CQ 的 Invalid Interrupt Vector（1/08h）。</p>
</li>
<li id="q-059-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-059-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-059-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-059-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get 本身不產生 Set Feature Event；Set 則要確認此 FID 的記錄支援、是否成功及設定是否改變。 <a class="qa-rule-link" href="#common-feature_events-11">本冊完整規則</a></p>
</li>
<li id="q-059-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>依 scope、可保存能力及重設涵蓋範圍決定；整體與部分重設的恢復規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-059-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確定整個或部分 subsystem 受影響；不可保存但持續的值不會因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-059-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存值依 Saved 恢復；不可保存的值另查持續性及該 Feature 的例外。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-059-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-059-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>驗 Get 值、CQ 配置、mask 與通知行為；CD=1 後仍被 MSI-X mask 遮住，不是不聚合設定失敗。</p>
</li>
<li id="q-059-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先區分 coalescing disable 與 interrupt masking，兩者不能用同一個 bit 解釋。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-irqfeat">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-irq">PCIe Transport 1.4 §3.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-060" data-question="60"><h2><a class="qa-qid" href="#q-060">Q60</a> Volatile Write Cache 與 Write Atomicity Normal 控制什麼行為？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-060-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-060-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>分開持久性與原子性：資料是否已進入非揮發儲存，與多個 logical blocks 是否以規定單位更新，是不同保證。</p>
</li>
<li id="q-060-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>FID06h 管 controller volatile write cache；FID0Ah 決定正常寫入原子性要求，不能直接改 namespace 的 atomic unit 宣告。</p>
</li>
<li id="q-060-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>VWC 宣告 cache 是否存在；AWUN／AWUPF、namespace overrides 與 boundary 描述原子性。</p>
</li>
<li id="q-060-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>FID06h.WCE=0 時寫入使用者資料必須持久；FID0Ah.DN=1 不要求 AWUN／NAWUN，但仍須遵守 AWUPF／NAWUPF。</p>
</li>
<li id="q-060-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先讀能力與格式，Set 後 Get，再用符合單位和邊界的假設 Write 比較允許結果；若需讓既有工作與新設定分界清楚，先排空。</p>
</li>
<li id="q-060-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>WCE=0 不會讓任意大小 Write 都原子；DN=1 也不會自動讓完成資料持久。兩個控制不能互相代替。</p>
</li>
<li id="q-060-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>沒有 volatile cache 卻 Get／Set FID06h，須回 Invalid Field（0/02h）；其他參數與 namespace／atomic 規則依適用命令判斷。</p>
</li>
<li id="q-060-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-060-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-060-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-060-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get 本身不產生 Set Feature Event；Set 則要確認此 FID 的記錄支援、是否成功及設定是否改變。 <a class="qa-rule-link" href="#common-feature_events-11">本冊完整規則</a></p>
</li>
<li id="q-060-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>依 scope、可保存能力及重設涵蓋範圍決定；整體與部分重設的恢復規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-060-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確定整個或部分 subsystem 受影響；不可保存但持續的值不會因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-060-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存值依 Saved 恢復；不可保存的值另查持續性及該 Feature 的例外。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-060-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-060-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>把 Current.WCE／DN 與 Identify 的有效 atomic unit 一起看；FUA 是個別命令持久性要求，不擴大 atomic unit。</p>
</li>
<li id="q-060-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先釐清預期是「不撕裂」還是「斷電不遺失」，再選驗證欄位。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-vwc">Base 2.4 §5.2.30.1.4</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-nvmatomic">NVM Command Set 1.3 §2.1.2–2.1.4</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-061" data-question="61"><h2><a class="qa-qid" href="#q-061">Q61</a> Asynchronous Event Configuration 如何決定哪些事件需要回報？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-061-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-061-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>讓 Host 選擇需要的狀態變更通知；它不會替 Host 自動送出等待事件的 Request。</p>
</li>
<li id="q-061-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>FID0Bh 作用於 controller 的通知設定，個別通知對應 SMART、namespace 或其他不同 scope 的狀態。</p>
</li>
<li id="q-061-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>OAES 表示選配事件支援，SMART 的警告也有相應能力；NVM 特定 bit 另見 NVM 規格。</p>
</li>
<li id="q-061-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CDW11 的各啟用 bit 選通知；AER completion 的 AET／AEI／LID 描述實際事件。兩者不是相同 bitmap。</p>
</li>
<li id="q-061-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>查支援→Set 合法事件 mask→掛 AER→條件成立→讀事件及對應 Log→依事件規則確認並補 Request。</p>
</li>
<li id="q-061-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>若啟用時條件已成立，也會依本 Feature 的規則送事件；不是只有設定後新發生的變化才可能回報。</p>
</li>
<li id="q-061-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>嘗試啟用 controller 不支援的事件，須回 Invalid Field（0/02h）。沒有 outstanding AER 導致尚未收到通知，不是 Set Features 錯誤 Status。</p>
</li>
<li id="q-061-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-061-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>本題正是設定通知。事件種類有各自條件與清除規則；FID0Bh 不是所有 Error 類型事件的通用總開關，也不能用 Get Features 代替補 AER。</p>
</li>
<li id="q-061-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-061-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get 本身不產生 Set Feature Event；Set 則要確認此 FID 的記錄支援、是否成功及設定是否改變。 <a class="qa-rule-link" href="#common-feature_events-11">本冊完整規則</a></p>
</li>
<li id="q-061-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>依 scope、可保存能力及重設涵蓋範圍決定；整體與部分重設的恢復規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-061-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確定整個或部分 subsystem 受影響；不可保存但持續的值不會因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-061-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存值依 Saved 恢復；不可保存的值另查持續性及該 Feature 的例外。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-061-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-061-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>核對 OAES、Current mask、pending Request 與事件是否仍被遮蔽；只看 mask=1 不能證明 Host 一定立即收到。</p>
</li>
<li id="q-061-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否真的掛入尚未完成的 AER，以及先前事件是否已按規則確認。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-062" data-question="62"><h2><a class="qa-qid" href="#q-062">Q62</a> Power Management、Autonomous Power State Transition 及 Host Controlled Thermal Management 有何差異？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-062-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-062-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>分開 Host 直接選 power state、閒置時自動轉換，以及依溫度降低功耗／效能三種控制。</p>
</li>
<li id="q-062-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>設定以 controller 為入口；多 controller 共用 domain 時，功耗狀態可能互相影響，不能只觀察單一路徑。</p>
</li>
<li id="q-062-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀 NPSS／Power State Descriptors、APSTA 與 HCTMA、MNTMT／MXTMT。</p>
</li>
<li id="q-062-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>FID02h 選 PS 與相關限制；FID0Ch.APSTE 啟用 32-entry 表，每格 ITPT 是該狀態的 idle ms、ITPS 是目標非工作狀態；FID10h.TMT1／TMT2 是 Kelvin 溫度。</p>
</li>
<li id="q-062-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先看可用 states 與 latency，再決定主動 PS 或 APST 表；另設定合法 TMT1&lt;TMT2（兩者非零時）。APST 每到新 state，使用新 state 的 idle 條件。</p>
</li>
<li id="q-062-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Set FID02h 成功時已到指定 PS，但 APST 啟用後還可再自動轉移；HCTM 觸發不等於 Host 又送了一筆 Power Management。</p>
</li>
<li id="q-062-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援 state、非法 APST 目標或溫度範圍／順序，用對應欄位要求判 Invalid Field（0/02h）；不能以「較省電」合理化非法設定。</p>
</li>
<li id="q-062-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-062-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-062-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-062-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Power Management 的 Set Feature Event 為 Not Recommended；APST 與 HCTM 的 Set Feature 記錄為 Optional，支援後依成功且設定改變的條件記錄。實際跨越熱門檻另看 Thermal Excursion Event，不把一次設溫度等同一次溫度異常。</p>
</li>
<li id="q-062-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Power Management／APST 不可保存時依 Figure466 回預設；HCTM 在不可保存情況仍標為持續。若可保存，改按 Saved 規則；同 domain 多 controller 的控制還需協調。</p>
</li>
<li id="q-062-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確定整個或部分 subsystem 受影響；不可保存但持續的值不會因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-062-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>不能把這三個 FID 都歸成斷電清除：不可保存的 HCTM 持續，而 Power Management／APST 不持續；可保存者依 Saved 恢復。</p>
</li>
<li id="q-062-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-062-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Get 設定、目前操作狀態、SMART 溫度與 HCTM 計數分開比對；不能只用功耗下降推論是 APST。</p>
</li>
<li id="q-062-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先辨認觸發來源是 Host Set、idle 計時還是溫度，再檢查該路徑設定。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a> · <a href="#ref-powerstates">Base 2.4 §8.1.19</a> · <a href="#ref-thermalpel">Base 2.4 §5.2.13.1.14.2.13</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-063" data-question="63"><h2><a class="qa-qid" href="#q-063">Q63</a> Timestamp、Keep Alive Timer 及 Host Memory Buffer 如何設定與驗證？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-063-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-063-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>三者分別提供事件時間基準、通訊存活監測與 controller 可專用的 Host 記憶體；不可共用同一種驗證方法。</p>
</li>
<li id="q-063-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Timestamp／Keep Alive 是 controller 時間狀態；HMB 還涉及 Host 記憶體使用權與生命週期。</p>
</li>
<li id="q-063-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Timestamp 看 ONCS；Keep Alive 看 KAS 與 CTRATT.TBKAS；HMB 看 HMPRE、HMMIN、HMMINDS、HMMAXD。</p>
</li>
<li id="q-063-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>FID0Eh 用 8-byte buffer 設 48-bit ms Timestamp；FID0Fh 用 KATO ms 並按 KAS×100 ms 向上取整；FID0Dh 設 EHM／MR、HSIZE、descriptor address／count。</p>
</li>
<li id="q-063-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>Timestamp Set 後 Get 應增加已過時間；KATO Set 後 Get 讀實際取整值；HMB 準備合法頁面再 Enable，停用成功後才能收回。MR=1 必須連內容與 descriptor 都與先前相同。</p>
</li>
<li id="q-063-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例：KAS=10、KATO 要求 1500 ms，取整後為 2000 ms。HMB 的 Get 同時回 CQE 狀態及 attributes buffer，不是只有一個開關值。</p>
</li>
<li id="q-063-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>HMB 已啟用再 Enable：Command Sequence Error（0/0Ch）；HMDLEC=0：Invalid Field（0/02h）。PCIe KATO=0 可停用，不能套用其他 transport 的強制啟用規則。</p>
</li>
<li id="q-063-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-063-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-063-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-063-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Timestamp 不得記成 Set Feature Event；支援 PEL 時改看 Timestamp Change Event（03h），保留變更前後值。KATO 與 HMB 的 Set Feature 記錄為 Optional，若支援，成功且設定改變時需記錄；不能要求所有 Get 都留一筆。</p>
</li>
<li id="q-063-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>HMB 不保留啟用設定，重設後重新配置；MR=1 只在記憶體及內容完整保留時可用。Timestamp 若跨該種 CLR 繼續更新須保留 Origin；不繼續更新時，CLR 會將 Timestamp 清為 0；若有 Saved 恢復，還須配合保存值，並回讀 Origin。Keep Alive 依其可保存／預設規則重新確認。</p>
</li>
<li id="q-063-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 HMB 需重配；Timestamp 不能假設每種 CLR 都有相同延續結果；Keep Alive 必須依恢復後 Current 重建 Host 的維持計時。</p>
</li>
<li id="q-063-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>HMB 不是非揮發儲存，不能因位址相同就宣稱 MR=1。Timestamp 若恢復 Saved 可能倒退至保存值；PCIe Keep Alive 未另保存時預設 KATO=0。</p>
</li>
<li id="q-063-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-063-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Timestamp 看 Origin／Synch，不硬當絕對時鐘；KATO 看取整後 Current；HMB 看能力、配置、實際 EHM 與記憶體是否仍被保留。</p>
</li>
<li id="q-063-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先分清此次 FID 的結果在 CQE 還是 data buffer，並確認各時間和大小單位。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-064" data-question="64"><h2><a class="qa-qid" href="#q-064">Q64</a> Host Behavior Support、Error Recovery 及 Read Recovery Level 有什麼用途？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-064-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-064-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>分別告訴 controller Host 懂哪些擴充、設定特定 namespace 的錯誤恢復屬性、選擇讀取恢復策略。</p>
</li>
<li id="q-064-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>FID16h 為 controller；FID05h 為 namespace；FID12h 依支援的 NVM Set 模型為 NVM Set 或 subsystem。</p>
</li>
<li id="q-064-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>ACRE 與相關能力配合使用；DULBE 先查 namespace NSFEAT.DAE；Read Recovery Level 先查 RRLS 支援 bitmap。</p>
</li>
<li id="q-064-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>FID16h 的 data buffer 含 ACRE、LBAFEE 等；FID05h.TLER 單位 100 ms、DULBE 在 bit16；FID12h 的 RRL 是等級碼，不是 RRLS bitmap。</p>
</li>
<li id="q-064-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先確認能力再設定；TLER 從錯誤恢復開始計時，不能拿它當從提交起算的所有命令 timeout。RRL 需對支援的目標設定後讀回。</p>
</li>
<li id="q-064-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>ACRE 允許適用的 advanced retry 行為；DULBE 改變未寫／deallocated block 的回應；選 Fast Fail 不表示保證固定 latency 或零次內部嘗試。</p>
</li>
<li id="q-064-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>未支援等級、非法設定按 Invalid Field（0/02h）等專屬規則；Command Interrupted（0/21h）只有 ACRE=1 才能回，且 DNR 必須 0。</p>
</li>
<li id="q-064-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-064-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-064-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-064-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get 本身不產生 Set Feature Event；Set 則要確認此 FID 的記錄支援、是否成功及設定是否改變。 <a class="qa-rule-link" href="#common-feature_events-11">本冊完整規則</a></p>
</li>
<li id="q-064-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>不可保存的 Host Behavior Support 與 Error Recovery 不持續，Read Recovery Level 則持續；可保存時改按 Saved 與 scope 的重設規則。</p>
</li>
<li id="q-064-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確定整個或部分 subsystem 受影響；不可保存但持續的值不會因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-064-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新取得各 FID 的 Current。不可保存的 RRL 仍持續，不能因沒有 Saved 就認定應回 0；Host Behavior Support／Error Recovery 另按其恢復規則。</p>
</li>
<li id="q-064-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-064-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>LBAFEE 會影響可用擴充格式的呈現與使用；能力、Host 宣告與 namespace 格式需一起解讀。</p>
</li>
<li id="q-064-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是不是把 TLER 当整筆命令期限，或把 RRLS 的位元位置直接當 RRL 數值。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-behavior">Base 2.4 §5.2.30.1.15</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-rrl">Base 2.4 §5.2.30.1.12, 8.1.23</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-065" data-question="65"><h2><a class="qa-qid" href="#q-065">Q65</a> Namespace Write Protection 如何設定？不同保護模式在 Reset 與 Power Cycle 後是否保留？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-065-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-065-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>防止 namespace 被修改，並區分可解除、直到斷電及永久三種保護生命週期。</p>
</li>
<li id="q-065-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>保護屬於 namespace，其他可存取該 namespace 的 controller 也必須遵守；不只是這條 queue 的軟體旗標。</p>
</li>
<li id="q-065-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Identify.NWPC 是能力；WPC 的 WPUPCC／PWPC 是允許進入特定模式的控制；Get FID84h.WPS 才是目前狀態。</p>
</li>
<li id="q-065-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>WPS=0 無保護、1 基本保護、2 到 Power Cycle、3 永久。此 Feature 不可保存、沒有 Default，不能用 SV=1 製造持續性。</p>
</li>
<li id="q-065-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>查能力與進入許可，針對 NSID Set WPS，再 Get Current；進入保護時 controller 須將該 namespace 的 volatile data／metadata 提交到非揮發媒體。</p>
</li>
<li id="q-065-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功後被禁止的操作須依寫保護規則拒絕；一般 Read 仍以可讀狀態處理。不能只看到 Set 成功就省略行為核對。</p>
</li>
<li id="q-065-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>試圖改變 WPS2／3、缺許可位或 multi-domain 禁止的 WPS2 轉換：Feature Not Changeable（1/0Eh）；Get Default：0/02h；受禁止的命令可回 Namespace is Write Protected（0/20h）。</p>
</li>
<li id="q-065-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-065-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-065-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-065-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get 本身不產生 Set Feature Event；Set 則要確認此 FID 的記錄支援、是否成功及設定是否改變。 <a class="qa-rule-link" href="#common-feature_events-11">本冊完整規則</a></p>
</li>
<li id="q-065-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 保留既有 WPS，包括 Until Power Cycle；不會因 FID84h 不可保存就解除保護。</p>
</li>
<li id="q-065-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 不等於 Power Cycle，WPS 依狀態機持續；不能用 NSSR 當解除 Until Power Cycle 的方法。</p>
</li>
<li id="q-065-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>實際 Power Cycle 後，WPS2 回 No Write Protect；基本 WPS1 與永久 WPS3 持續。永久保護不能用一般 Set／Reset 解開。</p>
</li>
<li id="q-065-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-065-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>CHANG=1 不表示進入永久保護後能解除。WPC 控制位重設與 namespace 已存在的 WPS 狀態是不同事情。</p>
</li>
<li id="q-065-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先讀 Current.WPS 與 WPC，確認是能力不支援、進入不允許，還是已處在不可改狀態。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-066" data-question="66"><h2><a class="qa-qid" href="#q-066">Q66</a> Set Features 成功後，為什麼還應使用 Get Features 確認？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-066-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-066-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>確認實際使用的值和 Host 要求的值之間是否有規範允許的轉換，並避免只看成功碼。</p>
</li>
<li id="q-066-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>同一 FID、scope、selector 與操作時期才可比較；Get Supported Capabilities 不等於 Get Current。</p>
</li>
<li id="q-066-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先知道 Feature 的回覆格式與支援能力；某些值在 CQE，某些在 data buffer，某些兩處都有。</p>
</li>
<li id="q-066-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>保存原 Set 的 SV／參數、Set CQE 結果，Get SEL0 讀 Current，必要時 SEL2 讀 Saved。</p>
</li>
<li id="q-066-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>等 Set 成功完成再 Get；避免另一個 Host 同時修改共用 scope。動態值如 Timestamp 以合理經過時間比較，不要求逐 bit 相同。</p>
</li>
<li id="q-066-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功 Set 的 CQE 不得早於屬性設定完成；KATO 可能向上取整，Number of Queues 回實際配置，這些不同於原請求不一定是錯。</p>
</li>
<li id="q-066-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>若後續 Get 失敗，它有自己的 Status，不能將它覆蓋原 Set 結果；先檢查 selector、scope 和中間 reset。</p>
</li>
<li id="q-066-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-066-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-066-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-066-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get 本身不產生 Set Feature Event；Set 則要確認此 FID 的記錄支援、是否成功及設定是否改變。 <a class="qa-rule-link" href="#common-feature_events-11">本冊完整規則</a></p>
</li>
<li id="q-066-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>依 scope、可保存能力及重設涵蓋範圍決定；整體與部分重設的恢復規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-066-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確定整個或部分 subsystem 受影響；不可保存但持續的值不會因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-066-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存值依 Saved 恢復；不可保存的值另查持續性及該 Feature 的例外。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-066-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-066-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Get 證明可讀到設定，行為驗證另證明功能採用它；兩者都需要，但不用重複把相同數值測成多個題目。</p>
</li>
<li id="q-066-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先核對 SEL 是否為 Current，以及 Set 與 Get 之間是否有 reset／其他 Set。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-setcomplete">Base 2.4 §5.2.30 (Command Completion)</a> · <a href="#ref-keepalive">Base 2.4 §3.9 (common and PCIe rules), 5.2.30.1.9</a> · <a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-067" data-question="67"><h2><a class="qa-qid" href="#q-067">Q67</a> Firmware Activation、Namespace 刪除、Controller Reset 及 Power Cycle 後，Feature 應如何變化？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-067-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-067-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>按事件與 Feature 的個別規則建立持續性預期，避免一律判「都清除」或「都保留」。</p>
</li>
<li id="q-067-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>先分 controller、namespace 與共享管理物件 scope，再分 Current／Saved／Default。</p>
</li>
<li id="q-067-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 SEL3.SVBL、Figure466 或 NVM Figure92，再看該 FID 的特殊規定；不可保存與不可持續不是同義詞。</p>
</li>
<li id="q-067-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>記錄事件是否真的造成 CLR、是否含整個 subsystem；Namespace Delete 移除的是該物件，不能將同號新 NSID 當成原設定的自然延續。</p>
</li>
<li id="q-067-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>保存前快照→執行已定義事件→恢復管理通道→讀 Current／Saved／能力→驗行為；對 Firmware Activation 先確認它採用哪種啟用與 Reset 路徑。</p>
</li>
<li id="q-067-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例：SV=0 的可保存 Feature 可在重設後回較舊 Saved；HMB 需重配；WPS2 撐過 Controller Reset 卻在 Power Cycle 解除。</p>
</li>
<li id="q-067-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>物件已刪後的 Get／Set 依該 FID 與 NSID 規則回應；不能因無法讀舊 NSID 的 Feature 就判保存失敗。</p>
</li>
<li id="q-067-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-067-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-067-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-067-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get 本身不產生 Set Feature Event；Set 則要確認此 FID 的記錄支援、是否成功及設定是否改變。 <a class="qa-rule-link" href="#common-feature_events-11">本冊完整規則</a></p>
</li>
<li id="q-067-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>依 scope、可保存能力及重設涵蓋範圍決定；整體與部分重設的恢復規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-067-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確定整個或部分 subsystem 受影響；不可保存但持續的值不會因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-067-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存值依 Saved 恢復；不可保存的值另查持續性及該 Feature 的例外。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-067-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-067-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>對比前後要保留 namespace 身分、SV、scope、重設原因與發生時間，不只一欄「Feature 值不同」。</p>
</li>
<li id="q-067-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認測到的是同一物件，以及事件是否真的觸發預期的重設範圍。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-nwp">Base 2.4 §5.2.30.1.38, 8.1.18</a> · <a href="#ref-nsmanage">Base 2.4 §5.2.24–5.2.25, 8.1.17</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-068" data-question="68"><h2><a class="qa-qid" href="#q-068">Q68</a> Feature 宣告支援但 Get、Set 或實際功能行為不一致時，應如何驗證？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-068-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-068-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>用可重現的最小條件找出矛盾屬於能力、設定、觀察方式還是韌體行為。</p>
</li>
<li id="q-068-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>鎖定同一 controller、FID、NSID／其他 selector 與配置時期，防止跨 scope 的數值混用。</p>
</li>
<li id="q-068-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>對照 Identify、Feature Supported and Effects、SEL3 能力；NSSPEC=0 不一定 controller scope，CHANG=1 不一定任何時候可改。</p>
</li>
<li id="q-068-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>保存原 Set、Get 的 FID／SEL／SV／CDW11／buffer 與 CQE，並記下開始驗行為前有哪些命令已 outstanding。</p>
</li>
<li id="q-068-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>能力查詢→合法 Set→等完成→Get Current→提交新命令驗效果；再單獨驗 Saved 與 reset。一次只改一個因素。</p>
</li>
<li id="q-068-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>一致結果須符合規範允許範圍：KATO 取整、動態 Timestamp、implementation-specific interrupt coalescing 都不能用「不等於請求」直接判錯。</p>
</li>
<li id="q-068-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援 FID=0/02h、SV 錯=1/0Dh、不可改=1/0Eh、scope 錯=1/0Fh 先各自排除；多錯誤共存時保留規範允許的選擇。</p>
</li>
<li id="q-068-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-068-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-068-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-068-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get 本身不產生 Set Feature Event；Set 則要確認此 FID 的記錄支援、是否成功及設定是否改變。 <a class="qa-rule-link" href="#common-feature_events-11">本冊完整規則</a></p>
</li>
<li id="q-068-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>依 scope、可保存能力及重設涵蓋範圍決定；整體與部分重設的恢復規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-068-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確定整個或部分 subsystem 受影響；不可保存但持續的值不會因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-068-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存值依 Saved 恢復；不可保存的值另查持續性及該 Feature 的例外。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-068-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-068-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>不合規結論應附一條明確要求、成立的前提、原始命令與回覆，以及能排除 selector／時序誤用的證據。</p>
</li>
<li id="q-068-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查 Get 是否讀了錯誤 SEL／NSID，或測行為的命令其實在 Set 成功前已提交。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-setcomplete">Base 2.4 §5.2.30 (Command Completion)</a> · <a href="#ref-irqfeat">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-effects">Base 2.4 §5.2.13.1.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-command-8"><h3>命令完成、事件與紀錄 · DNR 與 More 應如何設定？</h3><p>有 CQE 時，DNR=1 表示相同命令再送到此 NVM subsystem 的任一 controller 仍預期失敗；DNR=0 只表示可能成功。除非本題錯誤另有明定，不把某個 Status 固定綁成 DNR=1。More=1 表示 Error Information Log 有這筆命令的補充資訊。SCT=SC=0 時 DNR 應為 0。</p></article>
<article id="common-command-9"><h3>命令完成、事件與紀錄 · 是否產生 Asynchronous Event？</h3><p>命令完成與非同步通知是兩件事；本題操作成功本身不保證有事件。若操作引起規範列出的事件，還要核對事件支援、適用的通知設定、是否已遮蔽，以及 Host 是否掛入 Asynchronous Event Request。</p></article>
<article id="common-command-10"><h3>命令完成、事件與紀錄 · 是否更新 Error Information Log 或其他 Log？</h3><p>成功 CQE 不是要求新增 Error Information 的理由。錯誤有 More=1 時，查 LID 01h 並用 SQID、CID 和 Error Count 對應；不能把每個非成功 CQE 都當成必須新增一筆。操作改變的狀態則由本題列出的查詢介面重新讀取。</p></article>
<article id="common-feature-12"><h3>Feature 的重設與影響範圍 · Controller Reset 後是否保留或繼續？</h3><p>先分 scope 與 saveable。整個 subsystem 受重設影響時，可保存 Feature 的 Current 回 Saved（沒有 Saved 則 Default）；不可保存且不持續的回 Default。多 controller 只重設其中一個時，共用 scope 另依 Figure 127 保留；本題列出的個別 Feature 規則優先。</p></article>
<article id="common-feature-13"><h3>Feature 的重設與影響範圍 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>不能只看 Reset 名稱。若重設涵蓋整個 subsystem，使用 Figure 126；若 multi-domain 的重設只涵蓋一部分，使用 Figure 127。不可保存但規定持續的值繼續保留，不能誤用「不可保存＝重設清零」。</p></article>
<article id="common-feature-14"><h3>Feature 的重設與影響範圍 · Power Cycle 後是否保留或繼續？</h3><p>可保存且 SV=1 成功的設定，在斷電後依 Saved 恢復；SV=0 不會更新 Saved。不可保存的 Feature 才看 Figure 466 的持續性欄與個別例外。重新取得 Current 和行為結果，不能只看到 Saved 存在就假設硬體正在使用它。</p></article>
<article id="common-feature-15"><h3>Feature 的重設與影響範圍 · 是否影響其他 Controller 或 Namespace？</h3><p>依 Feature scope 決定。Controller scope 通常只控制目標 controller；namespace、NVM Set 或 subsystem scope 可能由其他 controller 共同觀察。跨 Host 修改共用設定需要協調，不能把 NSID=FFFFFFFFh 當成所有 Feature 通用的廣播。</p></article>
<article id="common-feature_events-11"><h3>Set Feature 的事件記錄 · 是否記錄於 Persistent Event Log？</h3><p>若支援 PEL 的 Set Feature Event，還要看 Figure 252 是否支援記錄此 FID：Set 成功且設定改變時必須記錄；成功但重設相同值則允許記錄。不是每個 FID 都能套用此事件；Timestamp 的 Set Feature Event 明確禁止，另用 Timestamp Change Event 判斷。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁＝PDF 頁−26；另兩份相同。以下依本次提供的 PDF 本文定位，保留 Figure 編號；共享頁只引用本題需要的定義，不納入 Fabrics 或 PCIe Link／封包內容。</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-keepalive"><strong>Base 2.4 · §3.9 (common and PCIe rules), 5.2.30.1.9</strong><br>文件頁 129–135, 471 · PDF 155–161, 497 · Figure 481</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>文件頁 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-getfeat"><strong>Base 2.4 · §5.2.12</strong><br>文件頁 209–212 · PDF 235–238 · Figure 197–202</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-effects"><strong>Base 2.4 · §5.2.13.1.5</strong><br>文件頁 226–230 · PDF 252–256 · Figure 216–218</li>
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
</ul><h3>需要看欄位圖時</h3><p>既有圖表教學各有固定位置。這裡連回相關圖，不複製另一份圖解。</p><ul>
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
