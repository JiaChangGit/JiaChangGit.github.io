---
layout: post
title: "NVMe 自問自答題庫：Get Log Page 與資料一致性"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/logs/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/logs/en/">English</a><a href="/DOCS/nvme-question-bank/logs.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–320</p>
<header><p class="qa-range">Q69–Q81</p><h1>Get Log Page 與資料一致性</h1><p class="qr-intro">Log 回答狀態、歷史或支援能力，但不是每份 Log 都保存歷史，也不是讀取後一定不變。本冊先選對資料與範圍，再處理長度、分段、事件確認與一致性。</p><p>先練習，再展開每題的 17 項解答。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>同樣是讀 Log，四個問題要分開</h2><p class="qa-takeaway">先決定要證明什麼，再選 Log；讀成功只代表查詢成功，不代表被查的管理操作已完成。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">需要的證據</th><th scope="col">查詢對象</th><th scope="col">判讀限制</th></tr></thead><tbody><tr><td>支援哪些 Log</td><td>LID00h</td><td>支援不等於目前有事件</td></tr><tr><td>目前健康</td><td>SMART LID02h</td><td>警告可恢復；累計值則有生命週期</td></tr><tr><td>這次命令的錯誤細節</td><td>Error LID01h</td><td>需對回命令，且舊 entries 可能消失</td></tr><tr><td>持續事件歷史</td><td>PEL LID0Dh</td><td>容量與事件支援限制仍存在</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>假設一次讀 4096 bytes，NUMD=1023。下一段若採 byte offset，LPO=4096；若 Log 使用 index offset，則要依該 Log 的索引規則前進，不能照抄 4096。</p>
<p class="qa-citations">來源：<a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-069">Q69 · Supported Log Pages 有什麼用途？讀取其他 Log 前，應如何確認支援能力？</a></li>
<li><a href="#q-070">Q70 · Error Information Log 與 SMART / Health Information Log 分別記錄什麼？</a></li>
<li><a href="#q-071">Q71 · Firmware Slot Information、Changed Namespace List 及 Commands Supported and Effects Log 分別用來確認什麼？</a></li>
<li><a href="#q-072">Q72 · Device Self-test、Persistent Event 及 Sanitize Status Log 分別適用於哪些情境？</a></li>
<li><a href="#q-073">Q73 · Endurance Group、Predictable Latency、Lockdown、Boot Partition 及 Media Unit Status Log 各記錄什麼？</a></li>
<li><a href="#q-074">Q74 · Host 如何依 Log Page 的 Scope 正確設定 NSID 及其他欄位？</a></li>
<li><a href="#q-075">Q75 · 大型 Log 如何分段讀取？Offset、Length、重疊及缺口應如何處理？</a></li>
<li><a href="#q-076">Q76 · Log Specific Identifier、UUID Index 及 Retain Asynchronous Event 有什麼用途？</a></li>
<li><a href="#q-077">Q77 · 分段讀取期間 Log 內容改變時，Host 如何判斷資料是否一致？</a></li>
<li><a href="#q-078">Q78 · Error Information Log 或 Persistent Event Log 到達容量上限時，舊紀錄如何處理？</a></li>
<li><a href="#q-079">Q79 · 哪些 Log 資料在 Controller Reset、NVM Subsystem Reset 或 Power Cycle 後仍可保留？</a></li>
<li><a href="#q-080">Q80 · Supported Log Pages 或 Commands Supported and Effects 的宣告與實際行為不一致時，如何判斷？</a></li>
<li><a href="#q-081">Q81 · Host 如何從 Commands Supported and Effects Log 確認 Opcode 支援及影響範圍？</a></li>
</ol></section>
<article class="qa-question" id="q-069" data-question="69"><h2><a class="qa-qid" href="#q-069">Q69</a> Supported Log Pages 有什麼用途？讀取其他 Log 前，應如何確認支援能力？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-069-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-069-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Supported Log Pages 提供查詢目錄，讓 Host 知道目前這個介面支援哪些 LID，以及各 LID 是否允許用 entry 索引讀取。它能避免把不支援誤認為資料為零；不過，先讀它是探索方法，不是每次 Get Log Page 前都必須重送的命令。</p>
</li>
<li id="q-069-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>回覆屬於收到命令的介面與 controller。不同介面可能支援不同 Log；CC.CSS=110b 時，CSI 與已啟用的 Command Set Profile 也會影響結果，不能把另一個介面的清單直接當成本介面的能力。</p>
</li>
<li id="q-069-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Get Log Page 使用 LID=00h。Identify.LPA 的 SPEDS 決定延伸 offset 與長度能力；各 LID 的 LSUPP、IOS 則分別表示支援及 index-offset 能力。</p>
</li>
<li id="q-069-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>整張表有 256 個 4-byte entries。LID=n 的 entry 位於 4×n；bit0 是 LSUPP，bit1 是 IOS，高位 LIDSP 另依該 Log 定義。LSUPP=0 時，Host 應忽略其餘欄位。</p>
</li>
<li id="q-069-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先選對 controller 與命令集，讀取 00h，再找到目標 LID 的 entry。確認支援後，才依該 Log 的 scope、長度及參數讀取內容；能力在韌體或配置變更後需要重新確認。</p>
</li>
<li id="q-069-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功取得的是能力表，不是各 Log 的內容。例如 LID=81h 的 LSUPP=1，只能證明可以查 Sanitize Status，不能據此宣稱已執行或完成 Sanitize。</p>
</li>
<li id="q-069-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援的 LID 一般回 Invalid Log Page（1/09h）；若 LSUPP=1，卻使用不支援的 OT=1，回 Invalid Field（0/02h）。兩者分別是 Log 不支援與讀取方式非法。</p>
</li>
<li id="q-069-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-069-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-069-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-069-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-069-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-069-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-069-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-069-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-069-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>將 LSUPP、IOS、LPA 與實際合法查詢一起比較。不能要求所有支援的 Log 都支援 index offset，也不能用一次非法參數失敗推翻 LSUPP。</p>
</li>
<li id="q-069-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認清單與後續命令來自同一介面、相同 CSI 及設定期間，再檢查目標 entry 是否按 4 bytes 定位。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-profile">Base 2.4 §5.2.30.1.18</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-070" data-question="70"><h2><a class="qa-qid" href="#q-070">Q70</a> Error Information Log 與 SMART / Health Information Log 分別記錄什麼？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-070-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-070-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Error Information 用來追查某次錯誤的細節；SMART / Health 則提供目前警告及生命週期累計資訊。前者回答哪筆命令或哪個錯誤，後者回答目前健康狀態與長期使用情況，不能互相替代。</p>
</li>
<li id="q-070-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>LID01h 是 controller 的錯誤紀錄。LID02h 可依支援情況接受 namespace 查詢，但 Base 2.4 明確指出本版沒有 namespace-specific SMART 欄位，因此兩種回覆包含相同資訊，不能自行標成各 namespace 的獨立使用量。</p>
</li>
<li id="q-070-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>ELPE+1 表示最多可讀多少個 Error Information entries；LPA 的 SMART 支援位決定是否接受 per-namespace 請求。先確認支援，再解讀 Log 內容。</p>
</li>
<li id="q-070-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>01h 每筆 64 bytes，重點是 ECNT、SQID、CID、Status、參數錯誤位置與 NSID。02h 為 512 bytes，重點是 Critical Warning、溫度、spare、Percentage Used，以及資料量、命令、時間和錯誤累計。</p>
</li>
<li id="q-070-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>遇到錯誤時先保存 CQE，接著讀 01h 對回命令，再以同時段 02h 觀察健康狀態。先記錄取樣時間，避免將很久以前的錯誤與目前警告錯配。</p>
</li>
<li id="q-070-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功讀取不代表裝置沒有錯誤。ECNT=0 表示該 entry 無效；Percentage Used=100 表示估計耐久度已耗用，並不直接表示裝置已失效。</p>
</li>
<li id="q-070-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援 per-namespace SMART 卻指定一般 NSID，須回 Invalid Field（0/02h）。Log 中的舊錯誤 Status 是紀錄內容，與本次 Get Log Page 的完成 Status 不同。</p>
</li>
<li id="q-070-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-070-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-070-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-070-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-070-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-070-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-070-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-070-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-070-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>SMART 的 Error Log Entries 累計不等於目前 01h buffer 裡的有效筆數；有限容量與重設清除可能讓歷史總量大於現存 entries。</p>
</li>
<li id="q-070-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認你比較的是錯誤歷史、目前警告，還是累計計數，再核對各欄位的有效性與時間。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-071" data-question="71"><h2><a class="qa-qid" href="#q-071">Q71</a> Firmware Slot Information、Changed Namespace List 及 Commands Supported and Effects Log 分別用來確認什麼？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-071-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-071-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這三張 Log 分別回答韌體從哪個 slot 執行、哪些 namespace 發生過變更，以及命令受不受支援、可能造成什麼影響。它們不是通用的操作歷史清單。</p>
</li>
<li id="q-071-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>03h 的資料依 multi-domain 能力屬於 domain 或 subsystem；04h 描述此 controller 的 attached namespace 變更；05h 的命令支援則以接收命令的 controller 與命令集為準。</p>
</li>
<li id="q-071-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先查 00h 支援表及相關 Identify 能力。Firmware 的 slot 數與唯讀限制由 Identify.FRMW 提供，不能只靠 03h 中非零字串的數量推算。</p>
</li>
<li id="q-071-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>03h 讀 CAFS、NAFS 與 FRS1～7；04h 讀 NSID 清單及首筆 FFFFFFFFh 的溢位標記；05h 讀各 Opcode 的 CSUPP、effects、CSE／CSER 與 CSP。</p>
</li>
<li id="q-071-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先根據問題選 Log：更新韌體後比較 03h 與 Identify.FR；收到 namespace 通知後讀 04h，再查 Identify；執行管理命令前讀 05h，完成後重查可能被改變的能力。</p>
</li>
<li id="q-071-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例如 NAFS=2 只表示 slot 2 等待適用的 CLR 啟用，不表示目前已從 slot 2 執行。04h 出現 NSID=7 也只指出有變更，不能單憑清單判斷它被 Format 或刪除。</p>
</li>
<li id="q-071-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>各次 Get 的錯誤與 Log 所描述的事件分開。不存在支援的 LID 回 1/09h；非法已定義參數依 Get 規則回 0/02h，不能把空 slot 或空變更清單本身當成失敗。</p>
</li>
<li id="q-071-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-071-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-071-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-071-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-071-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-071-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-071-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-071-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-071-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>核對 active slot 與 FR、變更清單與新的 Identify，以及 CSUPP 與合法命令行為。每一組對照有不同目的，不要求三張 Log 的數值彼此相同。</p>
</li>
<li id="q-071-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認是否把 NAFS 當 CAFS，或把 Changed List 當成完整 Active Namespace List。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-changedlog">Base 2.4 §5.2.13.1.5</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-072" data-question="72"><h2><a class="qa-qid" href="#q-072">Q72</a> Device Self-test、Persistent Event 及 Sanitize Status Log 分別適用於哪些情境？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-072-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-072-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Self-test Log 用來看測試進度與最近結果；PEL 用來追查跨時間的特定事件；Sanitize Status 用來判斷清除操作的目前狀態及最後結果。先選對證據種類，才不會把命令接受當成工作完成。</p>
</li>
<li id="q-072-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Self-test scope 受 DSTO.SDSO 等能力影響；PEL 屬於 subsystem；81h 的 NSID 則用來区分 subsystem 與 namespace sanitization target。查詢的 controller 不一定就是事件影響的全部範圍。</p>
</li>
<li id="q-072-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀 OACS 的 Self-test 能力、LPA 的 PEL 能力，以及 SANICAP／namespace Sanitize 能力，再確認 LID06h、0Dh、81h 受支援。Log 可讀不代表任意操作方法都可用。</p>
</li>
<li id="q-072-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>06h 先讀 DSTOS，再解釋進度與結果有效位；0Dh 先建立或取得 reporting context，再依事件長度走訪；81h 先看 SSTAT，再使用 SPROG 及相關結果欄位。</p>
</li>
<li id="q-072-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>例如 Sanitize 命令完成後，持續查 81h 判斷背景操作；Self-test 結束後讀 06h 最新有效結果；要追查先前重設或管理操作，才到 PEL 找支援的事件。</p>
</li>
<li id="q-072-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Get 成功表示讀取成功，不表示 Self-test 通過或 Sanitize 成功。PEL 沒有某筆事件，也要先確認事件支援、記錄條件與保存範圍。</p>
</li>
<li id="q-072-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援的 LID 回 1/09h；PEL context 順序錯誤可能回 Command Sequence Error（0/0Ch）。操作本身失敗要看其專用 Log 狀態，不能替本次成功 Get 改成失敗 CQE。</p>
</li>
<li id="q-072-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-072-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-072-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-072-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-072-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-072-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-072-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-072-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-072-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>以操作目標、時間及最新結果交叉比對。不得將舊 Self-test 結果或上次 Sanitize 成功，當成目前這次作業已成功的證據。</p>
</li>
<li id="q-072-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認讀取對象與 operation 是否相符，再判斷進度或歷史事件。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-073" data-question="73"><h2><a class="qa-qid" href="#q-073">Q73</a> Endurance Group、Predictable Latency、Lockdown、Boot Partition 及 Media Unit Status Log 各記錄什麼？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-073-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-073-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這些 Log 分別描述群組耐久度、可預測延遲狀態、禁止操作清單、開機分割區狀態，以及媒體單元資源。目的不同，不能把它們統稱為健康資訊後使用相同欄位判讀。</p>
</li>
<li id="q-073-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>先辨認管理對象：Endurance Group 使用 ENDGID，Predictable Latency 針對 NVM Set；Lockdown 依選擇與支援範圍，Boot Partition 透過 controller 查詢，Media Unit 則反映 domain 或 subsystem 資源。</p>
</li>
<li id="q-073-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先查 00h 及相關 Identify 能力。主要 LID 為 09h、0Ah／0Bh、14h、15h、10h；同一個 LSI 在不同 LID 的意義可能不同。</p>
</li>
<li id="q-073-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>09h 看警告、spare 與壽命計數；0Ah／0Bh 看 Set 的 latency 狀態及事件集合；14h 看禁止的 Opcode／FID；15h 看分割區識別與保護狀態；10h 看 Media Unit 識別、歸屬及狀態。</p>
</li>
<li id="q-073-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>由待回答的問題選 LID，再由 Identify 建立資源 ID 的對應，最後依該 Log 的參數與結構解碼。例如要查 group 3 的健康狀態，LSI 應選 ENDGID=3，而不是隨手填 NSID。</p>
</li>
<li id="q-073-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功回覆只描述選定對象。例如一個 group 的警告不能推論成全部 namespace 都有相同媒體故障；Lockdown 列出禁止項目，也不是那些命令的執行歷史。</p>
</li>
<li id="q-073-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援的 LID 與非法資源選擇須分開處理。前者是 1/09h；後者依該 Log 的已定義參數與專用 Status 判斷，不能一律改成 Invalid Namespace。</p>
</li>
<li id="q-073-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-073-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-073-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-073-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-073-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-073-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-073-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-073-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-073-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>核對資源歸屬、Log 狀態及實際功能。例如被禁止的 FID，應與 Lockdown 設定一致；Media Unit 狀態則要連同 namespace 所依賴的資源判斷。</p>
</li>
<li id="q-073-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否把 ENDGID、NVMSETID、NSID 或 Media Unit ID 混用。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-074" data-question="74"><h2><a class="qa-qid" href="#q-074">Q74</a> Host 如何依 Log Page 的 Scope 正確設定 NSID 及其他欄位？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-074-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-074-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>scope 決定資料描述哪個物件；選擇欄位則指出這次要查哪個實例。NSID 出現在公共命令格式中，不表示每張 Log 都可以查任意 namespace。</p>
</li>
<li id="q-074-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Figure 209 列出 controller、namespace、domain、subsystem 等範圍，但個別欄位也可能有更具體的定義。讀完整張表後，仍要核對該 LID 的例外。</p>
</li>
<li id="q-074-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>用 LSUPP 確認 Log 支援，再查 LPA、multi-domain 能力，以及該 LID 是否使用 CSI 或 UUID 選擇。這些能力決定哪些查詢組合有效。</p>
</li>
<li id="q-074-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>controller 或 subsystem scope 的 Log，一般使用 NSID=0 或 FFFFFFFFh；LSI、LSP、CSI 與 UIDX 各有獨立用途。不能把 LSI 當成 NSID 的延伸位元。</p>
</li>
<li id="q-074-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先寫出要查的物件，例如某 controller、ENDGID=3 或某 sanitization target，再把它映射到正確欄位。其餘未定義欄位依 Reserved 規則填寫。</p>
</li>
<li id="q-074-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>合法查詢回傳所選範圍的資料。例如 aggregate SMART 與某 group 的耐久度是不同範圍，不能複製同一份資料後標成每個 namespace 的獨立統計。</p>
</li>
<li id="q-074-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>依共同規則，controller 或 subsystem scope 的 Log 若指定 0／FFFFFFFFh 以外的 NSID，須回 Invalid Field（0/02h）。其他 scope 則按各 LID 與 NSID 規則處理。</p>
</li>
<li id="q-074-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-074-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-074-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-074-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-074-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-074-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-074-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-074-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-074-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>將命令中的選擇欄位、Identify 的資源對應與回傳內容一起保存，才能確定比較的是同一物件。</p>
</li>
<li id="q-074-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查該 LID 的 scope，而不是看到 NSID 非零就認定回覆是 namespace 專屬資料。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-uuid">Base 2.4 §8.1.31.1–8.1.31.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-075" data-question="75"><h2><a class="qa-qid" href="#q-075">Q75</a> 大型 Log 如何分段讀取？Offset、Length、重疊及缺口應如何處理？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-075-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-075-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>分段讀取讓 Host 用有限 buffer 取得大型 Log，但必須同時保證位址連續及內容一致。每段 Get 都成功，只能證明各段傳輸成功，不能自動證明合併檔完整。</p>
</li>
<li id="q-075-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Offset 是 Log 內的位置，不是 Host buffer 位址。OT=0 使用 byte offset；OT=1 使用該 Log 定義的 entry index，兩種單位不能混算。</p>
</li>
<li id="q-075-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>LPA.SPEDS 確認延伸長度與 offset，目標 LID 的 IOS 確認 index offset；另依 MDTS 與此 Log 的長度規則選擇每次傳輸量。</p>
</li>
<li id="q-075-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>NUMD=(NUMDU&lt;&lt;16)|NUMDL，通常傳輸 bytes=4×(NUMD+1)。LPOU／LPOL 組成 64-bit offset；byte offset 要 Dword 對齊。某些 Log 另有 entry 或 header 規則。</p>
</li>
<li id="q-075-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>例如讀取 8192 bytes，可用兩段 4096 bytes，offset 分別為 0、4096，NUMD 都是 1023。記錄每段範圍，確認沒有缺口；重疊區可比對，但若期間內容改變，不能任意挑一段覆蓋另一段。</p>
</li>
<li id="q-075-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功後應取得預定範圍。若要求長度超過 Log 尾端，除另有規定外，超出部分的結果未定義；不能把那些 bytes 當成 Log 的延伸資料。</p>
</li>
<li id="q-075-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Offset 大於 Log 大小，或不支援 IOS 卻使用 OT=1，須回 0/02h。byte offset 低兩位非零時，controller 可回 0/02h，也可依低兩位為零處理；不能把這個允許選擇寫成唯一錯誤結果。</p>
</li>
<li id="q-075-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-075-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-075-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-075-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-075-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-075-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-075-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-075-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-075-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>核對總長度、各段 offset／NUMD、generation 或 reporting context。涵蓋完整與同一份快照，是兩個都要成立的條件。</p>
</li>
<li id="q-075-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認 Offset 單位及 NUMD 的加 1 換算，再檢查是否混入另一代資料。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-telemetrylog">Base 2.4 §5.2.13.1.8–5.2.13.1.9</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-076" data-question="76"><h2><a class="qa-qid" href="#q-076">Q76</a> Log Specific Identifier、UUID Index 及 Retain Asynchronous Event 有什麼用途？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-076-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-076-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這三個欄位分別選資源、選資料定義，以及決定讀取後是否保留事件。它們控制不同部分，不能因為都叫參數就互相替代。</p>
</li>
<li id="q-076-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>LSI 的意義由 LID 決定；UIDX 從 UUID List 選擇適用定義；RAE 則影響這次讀取所對應的非同步事件。不是所有 Log 都使用三者。</p>
</li>
<li id="q-076-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先看該 LID 是否定義 LSI，以及 Get Log Page 是否支援 UUID 選擇。RAE 是否有實際作用，則要看該事件如何確認與清除。</p>
</li>
<li id="q-076-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>LSI 在 CDW11 bits31:16；UIDX 在 CDW14 bits6:0，0 表示不指定 UUID；RAE 在 CDW10 bit15。UIDX 是索引，不是 UUID 的數值本體。</p>
</li>
<li id="q-076-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先固定目標與 UUID 定義，再決定是否要保留事件以繼續取樣。若需要分段讀取與事後確認，保存每次 RAE，並遵守該 Log 的特定確認方式。</p>
</li>
<li id="q-076-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>RAE=1 的成功讀取保留對應事件；RAE=0 的成功讀取依規則清除。若命令未成功，事件必須保留，不能因 Host 已嘗試讀取就視為確認。</p>
</li>
<li id="q-076-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>非法 UUID 選擇依 §8.1.31 回 Invalid Field（0/02h）；LSI 非法則按該 LID 定義處理。不能用改 RAE 的方式修正錯誤的資源 ID。</p>
</li>
<li id="q-076-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-076-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-076-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-076-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-076-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-076-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-076-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-076-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-076-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>核對 LSI 的目標、UIDX 對應資料及事件是否仍 pending。讀取相同 bytes 但 RAE 不同，後續通知行為可能不同。</p>
</li>
<li id="q-076-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否曾有另一個成功的 RAE=0 讀取，提前確認了正在追蹤的事件。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-uuid">Base 2.4 §8.1.31.1–8.1.31.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-077" data-question="77"><h2><a class="qa-qid" href="#q-077">Q77</a> 分段讀取期間 Log 內容改變時，Host 如何判斷資料是否一致？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-077-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-077-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這題要防止把不同時點的資料拼成一份看似完整的報告。長度正確、沒有缺口，仍不代表所有欄位屬於同一次擷取。</p>
</li>
<li id="q-077-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>一致性判斷由各 Log 提供的機制決定。Telemetry 有 generation，PEL 有 reporting context；沒有此類機制的動態 Log，不能自行假設跨命令原子快照。</p>
</li>
<li id="q-077-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先確認支援的 Log 結構與版本，再找 generation、總長度、可用狀態或 context action。不能只查看 Get Log Page 的公共欄位。</p>
</li>
<li id="q-077-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Telemetry 記錄 TCDGN／相關 generation 及資料區邊界；PEL 記錄 context、TLL、事件長度與版本。每段同時保存 offset、length 及取得時間。</p>
</li>
<li id="q-077-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先取得 header，再按同一擷取或 context 讀取；必要時重讀 header。若前後 generation 改變，應重新取得一致資料，或明確標示無法證明一致，不能只換掉最後一份 header。</p>
</li>
<li id="q-077-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例如最初 TCDGN=10、最後=11，兩次 Get 都成功仍不足以證明中間所有 chunks 來自第 10 代。成功的分析結果必須連同一致性證據保存。</p>
</li>
<li id="q-077-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>內容改變不一定產生錯誤 CQE；動態更新本身可以合法。PEL 的非法 context 操作則可能得到 0/0Ch，應和資料版本改變分開判斷。</p>
</li>
<li id="q-077-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-077-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-077-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-077-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-077-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-077-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-077-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-077-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-077-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>將 header、每段資料及查詢順序當成一組證據，不能拿最後讀到的 capability 或 generation 回頭替所有舊 chunks 背書。</p>
</li>
<li id="q-077-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先看 generation 或 context 是否在整段讀取期間保持一致，再檢查解析器。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-telemetrylog">Base 2.4 §5.2.13.1.8–5.2.13.1.9</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-078" data-question="78"><h2><a class="qa-qid" href="#q-078">Q78</a> Error Information Log 或 Persistent Event Log 到達容量上限時，舊紀錄如何處理？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-078-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-078-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>有限容量的 Log 不可能無限保存歷史，因此必須分清楚累計事件數與目前還能讀到的紀錄。缺少舊 entry 不一定表示事件從未發生。</p>
</li>
<li id="q-078-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Error Information 以 controller 為範圍；PEL 保存 subsystem 的支援事件，並透過 reporting context 提供報告。兩者的容量與讀取生命週期不同。</p>
</li>
<li id="q-078-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Error Information 的容量由 ELPE+1 決定；PEL 先看支援能力、報告 TLL、事件數與最大容量資訊。不能把 SMART 累計值當成目前 buffer 的長度。</p>
</li>
<li id="q-078-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Error entries 依新到舊排列，ECNT 識別每次錯誤。PEL 依 event header 的 EHL、EL、ET、ETR 走訪，不能假設每筆固定 64 bytes。</p>
</li>
<li id="q-078-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>取樣時記錄有效 entries 與首尾識別，再於後次取樣找重疊範圍。若最舊紀錄已不在可讀範圍，標示歷史缺口，不能補造它的內容或順序。</p>
</li>
<li id="q-078-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Error Log 已滿又新增 entry 時，規範建議插入新 entry 並丟棄最舊 entry。PEL 是有限的持續歷史，讀完整份報告也不等於讀到裝置全部生命週期事件。</p>
</li>
<li id="q-078-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>容量用完不會使合法 Get 自動回失敗；應檢查回覆內容與各 Log 的保存規則。只有查詢參數或 context 不合法時，才依相應 Status 處理。</p>
</li>
<li id="q-078-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-078-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-078-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-078-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-078-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-078-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-078-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-078-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-078-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>ECNT／SMART 的累計變化與目前筆數可能不同；應以容量及保留規則解釋，不能要求每次取樣都仍含所有舊紀錄。</p>
</li>
<li id="q-078-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認讀取長度是否只要求前幾筆，再判斷是真的被淘汰，還是 Host 根本沒讀完整。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-079" data-question="79"><h2><a class="qa-qid" href="#q-079">Q79</a> 哪些 Log 資料在 Controller Reset、NVM Subsystem Reset 或 Power Cycle 後仍可保留？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-079-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-079-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>判斷保留性時，要把查詢命令、暫時回報狀態與真正保存的歷史分開。重設使 Get 中止，不表示它原本要讀的所有資料都被清除。</p>
</li>
<li id="q-079-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>保留規則可能適用整張 Log，也可能只適用其中某個欄位。多 controller 或 multi-domain 配置還要先確認重設影響哪些範圍。</p>
</li>
<li id="q-079-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀各 Log 的保留敘述與 Reset 章節。Figure 209 的 Restore to Default Content 指製造預設內容的恢復，並不是「遇到任何 Reset 就清空」的能力位。</p>
</li>
<li id="q-079-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>典型比較是 Error Information entries、其 ECNT、SMART 累計值、即時溫度、PEL 事件及 PEL context。這六種資訊即使相鄰，也不能套用同一保留結論。</p>
</li>
<li id="q-079-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先取得同一對象的前置快照，執行指定重設，恢復查詢後再讀。記錄中間是否同時發生 Firmware Activation、Format 或出廠配置恢復，避免把多個原因混成一個。</p>
</li>
<li id="q-079-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Error entries 在 CLR 與 Power Cycle 後建議清除，但 ECNT 持續；SMART 生命週期資訊原則上跨 Power Cycle 保留，個別欄位另有例外；PEL 事件的持續性不能套到 reporting context。</p>
</li>
<li id="q-079-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>比較前後值本身沒有新的 Status。如果恢復後 Get 失敗，先檢查 controller 是否 Ready、選擇欄位與 context 是否有效，不能將查詢失敗解釋成內容已被清零。</p>
</li>
<li id="q-079-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-079-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-079-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-079-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-079-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-079-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-079-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-079-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-079-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>以欄位的有效條件與單位比較，而不是要求整個 buffer 完全相同。累計保留與目前狀態重新取樣可以同時成立。</p>
</li>
<li id="q-079-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認是在比較內容保留，還是在比較一個已失效的 context 或未完成查詢。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-080" data-question="80"><h2><a class="qa-qid" href="#q-080">Q80</a> Supported Log Pages 或 Commands Supported and Effects 的宣告與實際行為不一致時，如何判斷？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-080-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-080-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這題要建立可重現的能力一致性檢查。宣告支援只表示存在合法用法，不能把任何參數下的失敗都判為能力造假。</p>
</li>
<li id="q-080-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>固定接收介面、controller、CSI、UUID 選擇及配置時間。尤其 CC.CSS=110b 時，尚未啟用的命令集會被視為不支援。</p>
</li>
<li id="q-080-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>一起保存 LSUPP、IOS、CSUPP、Identify 的功能位與 FID19h 設定。不要拿 LID 的支援位去判斷任意 Opcode，也不要反過來混用。</p>
</li>
<li id="q-080-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>測試命令保留 LID 或 Opcode、NSID、CSI、LSP、LSI、OT、長度及資料指標。取得 CQE 後再讀 SCT／SC，而不是只記一個工具錯誤訊息。</p>
</li>
<li id="q-080-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先構造符合能力、scope 及狀態的合法命令，再執行並核對結果。若失敗，逐項排除非法參數、被 Lockdown 禁止、namespace 未就緒及配置變更。</p>
</li>
<li id="q-080-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>在同一穩定配置下，明確宣告支援卻對合法請求回不支援，才形成需要追查的矛盾；合法的限制性 Status 不能直接當成不支援。</p>
</li>
<li id="q-080-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Get 不支援 LID 使用 1/09h；不支援 Opcode 使用 0/01h；0/02h 通常需要回頭檢查參數。保留規範的專用例外與多重錯誤選擇，不能只比一個預期數字。</p>
</li>
<li id="q-080-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-080-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-080-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-080-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-080-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-080-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-080-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-080-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-080-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>比較內容、行為與時間關係三者。若韌體已啟用新版本，應先重讀宣告，不能用舊表要求新 controller 行為。</p>
</li>
<li id="q-080-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認兩份證據來自同一介面與同一命令集配置，這通常比先懷疑韌體更能排除誤判。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-profile">Base 2.4 §5.2.30.1.18</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-081" data-question="81"><h2><a class="qa-qid" href="#q-081">Q81</a> Host 如何從 Commands Supported and Effects Log 確認 Opcode 支援及影響範圍？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-081-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-081-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這張表讓 Host 在執行命令前，了解是否支援，以及操作可能改變資料、namespace 配置或 controller 能力。它描述可能效果，不是每次執行一定發生的全部效果。</p>
</li>
<li id="q-081-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Admin Opcode 與 I/O Opcode 使用不同區域；I/O 區還要選對命令集。CSP 可以同時表示多種 scope，因為實際參數可能決定不同影響對象。</p>
</li>
<li id="q-081-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先確認 LPA.CELP、LID05h 支援與命令集選擇。CSP=0 表示未回報 scope，不能解成「不影響任何物件」。</p>
</li>
<li id="q-081-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Admin entry 位於 4×Opcode；I/O entry 位於 1024+4×Opcode。讀 CSUPP、LBCC、NCC、NIC、CCC，並搭配 CSE、CSER、USS 與 CSP，不只看最低位。</p>
</li>
<li id="q-081-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先找到正確 entry，再依 CSE／CSER 的建議協調其他工作。Host 支援非零 CSER 值時，使用其放寬建議；不支援時回到 CSE。命令完成後，重新查詢可能改變的能力或清單。</p>
</li>
<li id="q-081-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例如 NIC=1 表示命令可能改變 namespace 數量或多個 namespace 的能力，不表示這次呼叫一定新增一個 namespace。CSUPP=0 時，其餘 entry 欄位須為零。</p>
</li>
<li id="q-081-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>讀表失敗依 Get Log Page 處理；實際命令失敗則依該命令 Status。CSE 的建議不能任意提高成一個固定的強制錯誤碼。</p>
</li>
<li id="q-081-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-081-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-081-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-081-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-081-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-081-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-081-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-081-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-081-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>將 effects 與操作前後 Identify、清單及使用者資料影響交叉比對。CSUPP 與 Identify 宣告應一致，但實際效果仍須依本次參數判斷。</p>
</li>
<li id="q-081-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認 entry 偏移是否漏加 I/O 區的 1024 bytes，再檢查 CSI 與 CSP=0 是否被誤解。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-profile">Base 2.4 §5.2.30.1.18</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-command-8"><h3>命令完成、事件與紀錄 · DNR 與 More 應如何設定？</h3><p>只有收到 CQE，才有 DNR 與 More 可供判讀。DNR=1 表示相同命令即使重送到此 NVM subsystem 的任一 controller，仍預期會失敗；DNR=0 則只表示可能成功。除非個別錯誤條件另有明定，不能只看 Status 名稱就要求 DNR=1。More=1 表示 Error Information Log 有這筆命令的補充資訊。SCT=SC=0 時，DNR 應為 0。</p></article>
<article id="common-log_query-9"><h3>本主題的共用條件 · 是否產生 Asynchronous Event？</h3><p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。RAE=1 保留事件，讀取失敗也必須保留。Immediate 與 One-Shot 事件另有清除方式，不能全部套用讀 Log 確認。</p></article>
<article id="common-log_query-10"><h3>本主題的共用條件 · 是否更新 Error Information Log 或其他 Log？</h3><p>Get Log Page 回傳指定 Log 的資料。某些清單會因讀取而清除已回報的變更，某些事件也受 RAE 影響；讀取前先保存需要比對的狀態。讀取成功本身不要求新增 Error Information，失敗時則依 CQE 與錯誤記錄規則判斷。</p></article>
<article id="common-log_query-11"><h3>本主題的共用條件 · 是否記錄於 Persistent Event Log？</h3><p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。即使讀取的是 PEL，也不表示這次讀取會新增同類事件；只有另行發生且符合支援與記錄條件的事件，才依規則記錄。</p></article>
<article id="common-log_query-12"><h3>本主題的共用條件 · Controller Reset 後是否保留或繼續？</h3><p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。Log 內容是否保留則是另一個問題：Error Information entries 建議清除，但 Error Count 保留；SMART 的累計資訊與 PEL 依各欄位規則持續，不能隨查詢一起當成遺失。</p></article>
<article id="common-log_query-13"><h3>本主題的共用條件 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。它不等於恢復出廠設定；Figure 209 的 Restore to Default Content 欄描述製造預設內容的恢復，不能拿來當一般 Reset 的保留表。</p></article>
<article id="common-log_query-14"><h3>本主題的共用條件 · Power Cycle 後是否保留或繼續？</h3><p>Power Cycle 後重新提交查詢。SMART 的生命週期資訊及 PEL 具有跨斷電的保留規則；Error Information entries 則建議清除，但其累計 Error Count 仍保留。目前溫度、正在執行的操作及回報 context 必須依各自定義重新判讀，不能把所有 bytes 當成固定不變。</p></article>
<article id="common-log_query-15"><h3>本主題的共用條件 · 是否影響其他 Controller 或 Namespace？</h3><p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。controller、namespace、domain 與 subsystem 的資料範圍也不同；多個 Host 共同查詢時，應記錄由誰讀取及何時確認，避免誤以為另一端沒有發生事件。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-getlog"><strong>Base 2.4 · §5.2.13–5.2.13.1.1</strong><br>文件頁 212–218 · PDF 238–244 · Figure 203–211</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-smart"><strong>Base 2.4 · §5.2.13.1.3</strong><br>文件頁 220–225 · PDF 246–251 · Figure 213–214</li>
<li id="ref-fwlog"><strong>Base 2.4 · §5.2.13.1.4</strong><br>文件頁 225–226 · PDF 251–252 · Figure 215</li>
<li id="ref-changedlog"><strong>Base 2.4 · §5.2.13.1.5</strong><br>文件頁 226 · PDF 252</li>
<li id="ref-commandseffects"><strong>Base 2.4 · §5.2.13.1.6</strong><br>文件頁 226–229 · PDF 252–255 · Figure 216–217</li>
<li id="ref-dstlog"><strong>Base 2.4 · §5.2.13.1.7</strong><br>文件頁 229–232 · PDF 255–258 · Figure 218–219</li>
<li id="ref-telemetrylog"><strong>Base 2.4 · §5.2.13.1.8–5.2.13.1.9</strong><br>文件頁 232–237 · PDF 258–263 · Figure 220–223</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-pelcontext"><strong>Base 2.4 · §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</strong><br>文件頁 244–256, 258 · PDF 270–282, 284 · Figure 232–244, 246</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>文件頁 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-profile"><strong>Base 2.4 · §5.2.30.1.18</strong><br>文件頁 478–479 · PDF 504–505 · Figure 494–495</li>
<li id="ref-uuid"><strong>Base 2.4 · §8.1.31.1–8.1.31.2</strong><br>文件頁 737–738 · PDF 763–764 · Figure 782</li>
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
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/logs/en/">English</a><a href="/DOCS/nvme-question-bank/logs.html">繁中教學 HTML</a></nav>
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
