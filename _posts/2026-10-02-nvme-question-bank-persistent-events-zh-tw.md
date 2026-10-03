---
layout: post
title: "NVMe 自問自答題庫：Persistent Event Log 與 Timestamp"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/persistent-events/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/persistent-events/en/">English</a><a href="/DOCS/nvme-question-bank/persistent-events.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–320</p>
<header><p class="qa-range">Q205–Q216</p><h1>Persistent Event Log 與 Timestamp</h1><p class="qr-intro">PEL 保存重要事件，Timestamp 協助解釋事件時間。本冊先教一致地取回完整 Log，再說明可變長度、事件類型與時鐘變更。</p><p>先練習，再展開每題的 17 項解答。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>讀取的 context 與事件的持久性分開</h2><p class="qa-takeaway">事件仍保留，不代表舊 context 在 reset 後仍可沿用。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">讀取步驟</th><th scope="col">需要欄位</th><th scope="col">注意事項</th></tr></thead><tbody><tr><td>建立觀察範圍</td><td>ACT、RCE</td><td>ACT3 的 RCE=0 可表示剛建立成功</td></tr><tr><td>走訪 Log</td><td>LHL、TLL、TNEV</td><td>不能把每筆事件固定為同樣大小</td></tr><tr><td>解析事件</td><td>EHL、EL、VSIL</td><td>整筆=EHL+3+EL</td></tr><tr><td>解釋時間</td><td>Origin、SYNC、Timestamp Change</td><td>不能一律要求 timestamp 單調增加</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>EHL=21、EL=20、VSIL=4 時，整筆事件 44bytes，其中 Event Data 為 16bytes。VSIL 已包含在 EL，若再加一次就會走錯下一筆。</p>
<p class="qa-citations">來源：<a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-205">Q205 · 如何確認 Persistent Event Log 及個別事件的支援能力？</a></li>
<li><a href="#q-206">Q206 · PEL Context 如何建立、分段讀取與釋放？</a></li>
<li><a href="#q-207">Q207 · Context 不存在或重複建立時，應如何回應？</a></li>
<li><a href="#q-208">Q208 · SMART、Firmware、Timestamp、Reset 與 Hardware Error 如何記錄？</a></li>
<li><a href="#q-209">Q209 · Namespace、Format 與 Sanitize 對應哪些 Persistent Events？</a></li>
<li><a href="#q-210">Q210 · PEL 達容量上限時，舊事件如何處理？</a></li>
<li><a href="#q-211">Q211 · PEL 新增事件後，是否一定發送 Asynchronous Event？</a></li>
<li><a href="#q-212">Q212 · Reset 與 Power Cycle 後，PEL 哪些東西應保留？</a></li>
<li><a href="#q-213">Q213 · PEL 的 Header、長度與事件順序如何驗證？</a></li>
<li><a href="#q-214">Q214 · Timestamp 如何設定並以 Get Features 驗證？</a></li>
<li><a href="#q-215">Q215 · Timestamp 如何增加、Wrap-around，Origin 與 SYNC 怎麼看？</a></li>
<li><a href="#q-216">Q216 · Timestamp 變更如何記錄，Reset 與 Power Cycle 後怎麼判讀？</a></li>
</ol></section>
<article class="qa-question" id="q-205" data-question="205"><h2><a class="qa-qid" href="#q-205">Q205</a> 如何確認 Persistent Event Log 及個別事件的支援能力？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-205-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-205-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>先確認整份 Log，再確認事件種類，才能判斷缺少紀錄是否合理。支援 PEL 不表示所有選配事件都必須實作。</p>
</li>
<li id="q-205-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>PEL 是 NVM subsystem 全域資訊；Header 中的 controller 識別不會把它變成私有 Log。</p>
</li>
<li id="q-205-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 Identify.LPA 的 PEL 支援位元、PELS 的最大容量，以及 Supported Log Pages 對 LID0Dh 的宣告。建立 context 後再看 Supported Events Bitmap。</p>
</li>
<li id="q-205-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>PELS 以 64 KiB 為單位；ECRH 表示 ACT=3 與 GNUM 支援。符合 Base 2.0 以後版本且支援 PEL 的實作必須設 ECRH=1。</p>
</li>
<li id="q-205-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>確認 Log 能力後讀 Header，依事件支援及命令支援核對必要事件，再設計測試。</p>
</li>
<li id="q-205-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>取得支援矩陣，而不是只得到「有／沒有 PEL」一個結論。</p>
</li>
<li id="q-205-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援的 LID 使用 Invalid Log Page 等對應錯誤；不能因某個選配事件未宣告就判定整份 Log 違規。</p>
</li>
<li id="q-205-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-205-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Base 2.4 沒有「每新增 PEL entry 就回報 PEL Changed AER」的一般事件。 <a class="qa-rule-link" href="#common-pel_query-9">本冊完整規則</a></p>
</li>
<li id="q-205-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>建立 context 固定這次要回報的事件集合；期間新事件仍要記錄，但不能混入既有 context。 <a class="qa-rule-link" href="#common-pel_query-10">本冊完整規則</a></p>
</li>
<li id="q-205-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>PEL 的查詢不是另一筆 PEL 讀取事件。 <a class="qa-rule-link" href="#common-pel_query-11">本冊完整規則</a></p>
</li>
<li id="q-205-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Level Reset 後，PEL 事件內容須保留，但查詢 context 不保證仍有效。 <a class="qa-rule-link" href="#common-pel_query-12">本冊完整規則</a></p>
</li>
<li id="q-205-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 不清除持久事件；Reset 完成時還可能依支援規則新增 Power-on or Reset 事件。 <a class="qa-rule-link" href="#common-pel_query-13">本冊完整規則</a></p>
</li>
<li id="q-205-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>事件內容須跨 Power Cycle 保留，規範也建議設計盡量降低失電時的事件遺失。 <a class="qa-rule-link" href="#common-pel_query-14">本冊完整規則</a></p>
</li>
<li id="q-205-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>PEL 是 subsystem 全域的事件歷史。 <a class="qa-rule-link" href="#common-pel_query-15">本冊完整規則</a></p>
</li>
<li id="q-205-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Figure 233 的 bitmap 將 bits221:16 列保留，但 Figure 236 又列 ET10h，這是來源內部不一致；涉及該事件時須保留差異，不自行編造一致的位元表。</p>
</li>
<li id="q-205-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查測試期待的事件是 mandatory、依命令支援而 mandatory，還是 optional。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-206" data-question="206"><h2><a class="qa-qid" href="#q-206">Q206</a> PEL Context 如何建立、分段讀取與釋放？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-206-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-206-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Context 固定一份可一致讀取的事件集合，避免大型 Log 在分段傳輸期間被新事件改變內容。</p>
</li>
<li id="q-206-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Context 是這次回報的視圖，不是停止 controller 記錄新事件。</p>
</li>
<li id="q-206-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>確認 LID0Dh、ECRH 與 Header 的 TLL、LHL、GNUM、RCI。</p>
</li>
<li id="q-206-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>ACT=1 建立並讀取；ACT=0 讀既有 context；ACT=2 釋放；ACT=3 建立或沿用 context 並固定回 512-byte Header。</p>
</li>
<li id="q-206-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先 ACT=3 讀 Header，記錄 GNUM；依 TLL 用 ACT=0 與 LPO 分段讀取，讀完再讀 GNUM，確認相同後 ACT=2 釋放。</p>
</li>
<li id="q-206-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>各段來自相同 context；期間新發生事件留待下一次 context 回報。ACT=3 的 buffer 至少配置 512 bytes。</p>
</li>
<li id="q-206-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>ACT=0 無 context 或 ACT=1 已有 context，須回 Command Sequence Error。ACT=2 沒有 context 也不是錯誤。</p>
</li>
<li id="q-206-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-206-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Base 2.4 沒有「每新增 PEL entry 就回報 PEL Changed AER」的一般事件。 <a class="qa-rule-link" href="#common-pel_query-9">本冊完整規則</a></p>
</li>
<li id="q-206-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>建立 context 固定這次要回報的事件集合；期間新事件仍要記錄，但不能混入既有 context。 <a class="qa-rule-link" href="#common-pel_query-10">本冊完整規則</a></p>
</li>
<li id="q-206-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>PEL 的查詢不是另一筆 PEL 讀取事件。 <a class="qa-rule-link" href="#common-pel_query-11">本冊完整規則</a></p>
</li>
<li id="q-206-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Level Reset 後，PEL 事件內容須保留，但查詢 context 不保證仍有效。 <a class="qa-rule-link" href="#common-pel_query-12">本冊完整規則</a></p>
</li>
<li id="q-206-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 不清除持久事件；Reset 完成時還可能依支援規則新增 Power-on or Reset 事件。 <a class="qa-rule-link" href="#common-pel_query-13">本冊完整規則</a></p>
</li>
<li id="q-206-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>事件內容須跨 Power Cycle 保留，規範也建議設計盡量降低失電時的事件遺失。 <a class="qa-rule-link" href="#common-pel_query-14">本冊完整規則</a></p>
</li>
<li id="q-206-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>PEL 是 subsystem 全域的事件歷史。 <a class="qa-rule-link" href="#common-pel_query-15">本冊完整規則</a></p>
</li>
<li id="q-206-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>GNUM 不一致時，已讀資料可能無效，Host 應重新讀取，不能只補最後一段。</p>
</li>
<li id="q-206-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認每段 ACT、LPO 與 GNUM，避免把不同 context 的資料拼在一起。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-207" data-question="207"><h2><a class="qa-qid" href="#q-207">Q207</a> Context 不存在或重複建立時，應如何回應？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-207-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-207-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>原題的「超過 context 數量上限」應改成檢查 ACT 與既有 context。這套介面沒有讓 Host 任意建立帶不同 ID 的 context 清單。</p>
</li>
<li id="q-207-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>判斷的是處理命令當下，是否已有 persistent reporting context。</p>
</li>
<li id="q-207-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>使用 ACT=3 的 RCE 與 RCPIT／RCPID，了解既有 context 及建立來源。</p>
</li>
<li id="q-207-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>RCE=0 代表這次命令處理前沒有 context；ACT=3 仍會建立成功，不能把 0 翻成建立失敗。</p>
</li>
<li id="q-207-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>需要沿用就 ACT=0；要取得新事件集合，先協調讀者，再 ACT=2 釋放並重新建立。</p>
</li>
<li id="q-207-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>ACT=3 不論原本是否存在都成功回 Header，RCE 區分先前狀態；ACT=2 可重複釋放。</p>
</li>
<li id="q-207-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>ACT=1 重複建立與 ACT=0 無 context 都是 Command Sequence Error，不能替這兩種條件改用假想的資源數量錯誤。</p>
</li>
<li id="q-207-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-207-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Base 2.4 沒有「每新增 PEL entry 就回報 PEL Changed AER」的一般事件。 <a class="qa-rule-link" href="#common-pel_query-9">本冊完整規則</a></p>
</li>
<li id="q-207-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>建立 context 固定這次要回報的事件集合；期間新事件仍要記錄，但不能混入既有 context。 <a class="qa-rule-link" href="#common-pel_query-10">本冊完整規則</a></p>
</li>
<li id="q-207-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>PEL 的查詢不是另一筆 PEL 讀取事件。 <a class="qa-rule-link" href="#common-pel_query-11">本冊完整規則</a></p>
</li>
<li id="q-207-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Level Reset 後，PEL 事件內容須保留，但查詢 context 不保證仍有效。 <a class="qa-rule-link" href="#common-pel_query-12">本冊完整規則</a></p>
</li>
<li id="q-207-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 不清除持久事件；Reset 完成時還可能依支援規則新增 Power-on or Reset 事件。 <a class="qa-rule-link" href="#common-pel_query-13">本冊完整規則</a></p>
</li>
<li id="q-207-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>事件內容須跨 Power Cycle 保留，規範也建議設計盡量降低失電時的事件遺失。 <a class="qa-rule-link" href="#common-pel_query-14">本冊完整規則</a></p>
</li>
<li id="q-207-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>PEL 是 subsystem 全域的事件歷史。 <a class="qa-rule-link" href="#common-pel_query-15">本冊完整規則</a></p>
</li>
<li id="q-207-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>把 CQE 成功與 RCE 的前置狀態放在一起解讀，兩者並不矛盾。</p>
</li>
<li id="q-207-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否把 RCE 誤解成命令執行後的「目前已建立」布林值。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-208" data-question="208"><h2><a class="qa-qid" href="#q-208">Q208</a> SMART、Firmware、Timestamp、Reset 與 Hardware Error 如何記錄？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-208-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-208-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>每類事件有不同觸發點與資料格式；辨認事件後才能決定哪個欄位能回答問題。</p>
</li>
<li id="q-208-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Header.CNTLID 標示記錄來源；多 controller 的共同事件建議只記一次，事件資料可列多個 controller。</p>
</li>
<li id="q-208-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>確認 PEL 與所需事件支援；PCIe 的 SMART Snapshot 是 PEL 支援後的必要事件。</p>
</li>
<li id="q-208-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>ET01h 帶 512-byte SMART 快照；02h 帶 Firmware Commit 的 action、slot、status 與 requested revision；03h 帶變更前時間；04h 帶 reset descriptors；05h 以硬體錯誤代碼選 payload。</p>
</li>
<li id="q-208-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先讀 ET、ETR、EL，再按該格式解析。SMART 快照至少每 24 power-on hours 記錄一次；Reset 事件於重設完成時記錄。</p>
</li>
<li id="q-208-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Firmware NFR 代表要求啟用的版本，不保證已啟用；Reset descriptor 的 FA 能補充有無啟用及是否失敗。</p>
</li>
<li id="q-208-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>硬體錯誤只要求記錄已支援且符合條件者，並有高頻抑制例外；不能要求每個命令 Invalid Field 都有硬體錯誤事件。</p>
</li>
<li id="q-208-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-208-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Base 2.4 沒有「每新增 PEL entry 就回報 PEL Changed AER」的一般事件。 <a class="qa-rule-link" href="#common-pel_query-9">本冊完整規則</a></p>
</li>
<li id="q-208-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>建立 context 固定這次要回報的事件集合；期間新事件仍要記錄，但不能混入既有 context。 <a class="qa-rule-link" href="#common-pel_query-10">本冊完整規則</a></p>
</li>
<li id="q-208-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>PEL 的查詢不是另一筆 PEL 讀取事件。 <a class="qa-rule-link" href="#common-pel_query-11">本冊完整規則</a></p>
</li>
<li id="q-208-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Level Reset 後，PEL 事件內容須保留，但查詢 context 不保證仍有效。 <a class="qa-rule-link" href="#common-pel_query-12">本冊完整規則</a></p>
</li>
<li id="q-208-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 不清除持久事件；Reset 完成時還可能依支援規則新增 Power-on or Reset 事件。 <a class="qa-rule-link" href="#common-pel_query-13">本冊完整規則</a></p>
</li>
<li id="q-208-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>事件內容須跨 Power Cycle 保留，規範也建議設計盡量降低失電時的事件遺失。 <a class="qa-rule-link" href="#common-pel_query-14">本冊完整規則</a></p>
</li>
<li id="q-208-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>PEL 是 subsystem 全域的事件歷史。 <a class="qa-rule-link" href="#common-pel_query-15">本冊完整規則</a></p>
</li>
<li id="q-208-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>使用實際 CQE、Identify.FR、SMART 快照與事件 payload 互證，避免只憑事件名稱猜結果。</p>
</li>
<li id="q-208-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認使用的 ETR 與 payload 格式一致，並分清「要求」與「完成」。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-209" data-question="209"><h2><a class="qa-qid" href="#q-209">Q209</a> Namespace、Format 與 Sanitize 對應哪些 Persistent Events？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-209-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-209-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>管理操作的開始與完成可能相隔很久，需要不同事件才能重建過程。</p>
</li>
<li id="q-209-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Namespace 事件辨認目標 NSID；Format 與 Sanitize 還要依命令判斷單一 namespace 或較廣範圍。</p>
</li>
<li id="q-209-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>確認操作支援與事件支援；PEL 的條件性必要事件隨對應命令能力判斷。</p>
</li>
<li id="q-209-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>ET06h 記 Namespace Create／Delete；07h、08h 為 Format Start／Completion；09h、0Ah 為 Sanitize Start／Completion。NVM 的 FLBAS、DPS 解釋來自 NVM Command Set。</p>
</li>
<li id="q-209-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>以目標、action、開始資料與完成資料配對；Attach／Detach 不是 Namespace Create／Delete，不應硬套 ET06h。</p>
</li>
<li id="q-209-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Format completion 需連 FNVMS 與 INFO 判讀；Sanitize 進入 Media Verification 並不等於已產生正常最終完成事件。</p>
</li>
<li id="q-209-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Reset 導致沒有 Format CQE 時，不能把紀錄中保留或零值 Status 當成成功證明。</p>
</li>
<li id="q-209-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-209-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Base 2.4 沒有「每新增 PEL entry 就回報 PEL Changed AER」的一般事件。 <a class="qa-rule-link" href="#common-pel_query-9">本冊完整規則</a></p>
</li>
<li id="q-209-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>建立 context 固定這次要回報的事件集合；期間新事件仍要記錄，但不能混入既有 context。 <a class="qa-rule-link" href="#common-pel_query-10">本冊完整規則</a></p>
</li>
<li id="q-209-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>PEL 的查詢不是另一筆 PEL 讀取事件。 <a class="qa-rule-link" href="#common-pel_query-11">本冊完整規則</a></p>
</li>
<li id="q-209-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Level Reset 後，PEL 事件內容須保留，但查詢 context 不保證仍有效。 <a class="qa-rule-link" href="#common-pel_query-12">本冊完整規則</a></p>
</li>
<li id="q-209-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 不清除持久事件；Reset 完成時還可能依支援規則新增 Power-on or Reset 事件。 <a class="qa-rule-link" href="#common-pel_query-13">本冊完整規則</a></p>
</li>
<li id="q-209-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>事件內容須跨 Power Cycle 保留，規範也建議設計盡量降低失電時的事件遺失。 <a class="qa-rule-link" href="#common-pel_query-14">本冊完整規則</a></p>
</li>
<li id="q-209-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>PEL 是 subsystem 全域的事件歷史。 <a class="qa-rule-link" href="#common-pel_query-15">本冊完整規則</a></p>
</li>
<li id="q-209-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>NVM Namespace 刪除全部時，FLBAS／DPS 保留；單一刪除則描述被刪前的格式，不能在物件消失後仍要求 Identify 可讀。</p>
</li>
<li id="q-209-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查這筆紀錄是 Start 還是 Completion，以及完成資料是否真的有效。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-nspelevent">Base 2.4 §5.2.13.1.14.2.6</a> · <a href="#ref-formatpel">Base 2.4 §5.2.13.1.14.2.7–5.2.13.1.14.2.8</a> · <a href="#ref-sanitizepel">Base 2.4 §5.2.13.1.14.2.9–5.2.13.1.14.2.10</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-210" data-question="210"><h2><a class="qa-qid" href="#q-210">Q210</a> PEL 達容量上限時，舊事件如何處理？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-210-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-210-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>PEL 有容量限制，Host 不能假設所有事件從出廠開始永久逐筆保存。</p>
</li>
<li id="q-210-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>限制可能來自總 bytes、總事件數，或個別事件類別的內部容量。</p>
</li>
<li id="q-210-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 PELS、TLL、TNEV 與產品的廠商定義政策；Header 的目前數量不是終身發生次數。</p>
</li>
<li id="q-210-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>到達限制後，刪除哪些事件由廠商決定，可能保留較舊但較重要的紀錄；不保證嚴格 FIFO。</p>
</li>
<li id="q-210-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>取得前後兩份完整 context，按事件內容比對，再考慮容量淘汰、高頻抑制與 Sanitize 的影響。</p>
</li>
<li id="q-210-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Controller 可回報仍保留的有效集合；事件數沒有單調增加，不足以單獨判定資料遺失違規。</p>
</li>
<li id="q-210-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>規範建議容量足以支應使用壽命，但這是 should；不能改寫成永遠不得淘汰的 shall。</p>
</li>
<li id="q-210-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-210-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Base 2.4 沒有「每新增 PEL entry 就回報 PEL Changed AER」的一般事件。 <a class="qa-rule-link" href="#common-pel_query-9">本冊完整規則</a></p>
</li>
<li id="q-210-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>建立 context 固定這次要回報的事件集合；期間新事件仍要記錄，但不能混入既有 context。 <a class="qa-rule-link" href="#common-pel_query-10">本冊完整規則</a></p>
</li>
<li id="q-210-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>PEL 的查詢不是另一筆 PEL 讀取事件。 <a class="qa-rule-link" href="#common-pel_query-11">本冊完整規則</a></p>
</li>
<li id="q-210-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Level Reset 後，PEL 事件內容須保留，但查詢 context 不保證仍有效。 <a class="qa-rule-link" href="#common-pel_query-12">本冊完整規則</a></p>
</li>
<li id="q-210-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 不清除持久事件；Reset 完成時還可能依支援規則新增 Power-on or Reset 事件。 <a class="qa-rule-link" href="#common-pel_query-13">本冊完整規則</a></p>
</li>
<li id="q-210-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>事件內容須跨 Power Cycle 保留，規範也建議設計盡量降低失電時的事件遺失。 <a class="qa-rule-link" href="#common-pel_query-14">本冊完整規則</a></p>
</li>
<li id="q-210-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>PEL 是 subsystem 全域的事件歷史。 <a class="qa-rule-link" href="#common-pel_query-15">本冊完整規則</a></p>
</li>
<li id="q-210-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>GNUM 表示新 context 的內容相較前次改變，不是累計事件總數；兩者不應混算。</p>
</li>
<li id="q-210-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認是否已達任一廠商定義限制，而不是只檢查 TLL 是否剛好等於 PELS。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-211" data-question="211"><h2><a class="qa-qid" href="#q-211">Q211</a> PEL 新增事件後，是否一定發送 Asynchronous Event？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-211-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-211-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>本題要修正「有持久紀錄就一定有即時通知」的假設，這是兩條不同的回報途徑。</p>
</li>
<li id="q-211-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>PEL 提供跨重設歷史；AER 回報受支援且符合通知條件的即時事件。</p>
</li>
<li id="q-211-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>分別查 Supported Events Bitmap 與 AER/AEC 的支援設定，不能拿 PEL bitmap 當 AER 遮罩。</p>
</li>
<li id="q-211-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>例如 SMART Critical Warning 可能同時符合 PEL hardware event 與 SMART AER；一般 Timestamp Change 則沒有因此定義一個 PEL Changed 通知。</p>
</li>
<li id="q-211-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先找造成 PEL 紀錄的原始事件，再檢查它是否另有 AER 類型、設定、遮蔽與 request 條件。</p>
</li>
<li id="q-211-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>可能只看到 PEL，也可能兩者都有；須按事件種類而不是按「Log 改了」判定。</p>
</li>
<li id="q-211-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>沒有規範定義的通知時，不能要求回報自行命名的 AER，或把沒有 AER 判成命令錯誤。</p>
</li>
<li id="q-211-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-211-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Base 2.4 沒有「每新增 PEL entry 就回報 PEL Changed AER」的一般事件。 <a class="qa-rule-link" href="#common-pel_query-9">本冊完整規則</a></p>
</li>
<li id="q-211-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>建立 context 固定這次要回報的事件集合；期間新事件仍要記錄，但不能混入既有 context。 <a class="qa-rule-link" href="#common-pel_query-10">本冊完整規則</a></p>
</li>
<li id="q-211-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>PEL 的查詢不是另一筆 PEL 讀取事件。 <a class="qa-rule-link" href="#common-pel_query-11">本冊完整規則</a></p>
</li>
<li id="q-211-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Level Reset 後，PEL 事件內容須保留，但查詢 context 不保證仍有效。 <a class="qa-rule-link" href="#common-pel_query-12">本冊完整規則</a></p>
</li>
<li id="q-211-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 不清除持久事件；Reset 完成時還可能依支援規則新增 Power-on or Reset 事件。 <a class="qa-rule-link" href="#common-pel_query-13">本冊完整規則</a></p>
</li>
<li id="q-211-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>事件內容須跨 Power Cycle 保留，規範也建議設計盡量降低失電時的事件遺失。 <a class="qa-rule-link" href="#common-pel_query-14">本冊完整規則</a></p>
</li>
<li id="q-211-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>PEL 是 subsystem 全域的事件歷史。 <a class="qa-rule-link" href="#common-pel_query-15">本冊完整規則</a></p>
</li>
<li id="q-211-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>為每個測試列出兩條獨立預期：是否記錄，以及是否通知。</p>
</li>
<li id="q-211-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查測試是否把不存在的一般 PEL Changed AER 當成必需。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-212" data-question="212"><h2><a class="qa-qid" href="#q-212">Q212</a> Reset 與 Power Cycle 後，PEL 哪些東西應保留？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-212-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-212-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>要分清持久事件與暫時的讀取 context：事件保留不表示查詢可以從中斷處無條件接續。</p>
</li>
<li id="q-212-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>持久性涵蓋 subsystem 的事件內容；context 則服務一次一致的報告讀取。</p>
</li>
<li id="q-212-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>保存重設前的完整 Header、事件資料與 GNUM，重設後重新建立 context。</p>
</li>
<li id="q-212-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>新 Header 的時間、GNUM、事件數可能改變；新增 Power-on or Reset entry 也會改變低 offset 的事件排列。</p>
</li>
<li id="q-212-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>按事件內容與來源關聯前後紀錄，不要求同一事件永遠位於同一 byte offset。</p>
</li>
<li id="q-212-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>原有持久事件依保留規則仍可讀；context 若已失效，就重新開始一致的讀取。</p>
</li>
<li id="q-212-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不能把舊 context 的 Command Sequence Error 當成 PEL 已清空。容量淘汰、抑制或 Sanitize 也需獨立排除。</p>
</li>
<li id="q-212-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-212-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Base 2.4 沒有「每新增 PEL entry 就回報 PEL Changed AER」的一般事件。 <a class="qa-rule-link" href="#common-pel_query-9">本冊完整規則</a></p>
</li>
<li id="q-212-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>建立 context 固定這次要回報的事件集合；期間新事件仍要記錄，但不能混入既有 context。 <a class="qa-rule-link" href="#common-pel_query-10">本冊完整規則</a></p>
</li>
<li id="q-212-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>PEL 的查詢不是另一筆 PEL 讀取事件。 <a class="qa-rule-link" href="#common-pel_query-11">本冊完整規則</a></p>
</li>
<li id="q-212-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Level Reset 後，PEL 事件內容須保留，但查詢 context 不保證仍有效。 <a class="qa-rule-link" href="#common-pel_query-12">本冊完整規則</a></p>
</li>
<li id="q-212-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 不清除持久事件；Reset 完成時還可能依支援規則新增 Power-on or Reset 事件。 <a class="qa-rule-link" href="#common-pel_query-13">本冊完整規則</a></p>
</li>
<li id="q-212-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>事件內容須跨 Power Cycle 保留，規範也建議設計盡量降低失電時的事件遺失。 <a class="qa-rule-link" href="#common-pel_query-14">本冊完整規則</a></p>
</li>
<li id="q-212-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>PEL 是 subsystem 全域的事件歷史。 <a class="qa-rule-link" href="#common-pel_query-15">本冊完整規則</a></p>
</li>
<li id="q-212-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>用新 context 取得的完整資料驗證事件，而不是只檢查 Reset 前後第一筆是否相同。</p>
</li>
<li id="q-212-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認消失的是事件本身，還是只失去讀取 context。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-213" data-question="213"><h2><a class="qa-qid" href="#q-213">Q213</a> PEL 的 Header、長度與事件順序如何驗證？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-213-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-213-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>PEL 是可變長度紀錄，錯算一個長度會讓後面每筆事件都解析錯位。</p>
</li>
<li id="q-213-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>先區分「整份 Log」與「單筆事件」兩層資料。Log Revision（LREV）指出整份 Log 的格式版本；每筆事件內的 Event Type Revision（ETR）則指出該類事件資料的格式版本。兩者不是同一個版本欄位，解析時要分別確認。</p>
</li>
<li id="q-213-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先由 Identify Controller.LPA 確認 PEL 支援能力，再讀 Log Header。Total Log Length（TLL）是整份資料的 bytes 數，Total Number of Events（TNEV）是事件筆數；Log Header Length（LHL）用來計算第一筆事件從哪裡開始，Generation Number（GNUM）則用來辨認 Log 是否已更新。界定整份資料後，再檢查每筆事件的長度。</p>
</li>
<li id="q-213-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>LHL 的計算起點是 Log 的 byte 20，因此 Log Header 總長為 LHL+20。每筆事件的 Event Header Length（EHL）也不包含最前面的 3 bytes，所以事件標頭總長為 EHL+3。Event Length（EL）描述標頭後方的資料，且已包含 Vendor Specific Information Length（VSIL）指定的廠商資訊；因此整筆事件長度是 EHL+3+EL，而扣除廠商資訊後的 Event Data 長度是 EL−VSIL。</p>
</li>
<li id="q-213-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>從 Header 結尾開始，依每筆總長前進並檢查界限。例如 EHL=21、EL=20、VSIL=4，整筆 44 bytes，其中 Event Data 為 16 bytes。</p>
</li>
<li id="q-213-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>解析完 TNEV 筆事件後，所有已解析的事件都應落在 TLL 指定的有效資料範圍內。每筆事件不保證從 4-byte 對齊的位置開始，因此不能擅自插入 padding，否則下一筆事件的起點就會算錯。</p>
</li>
<li id="q-213-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>若 VSIL&gt;EL，表示宣告的廠商資訊比包含它的資料範圍還大；若事件結尾超過 TLL，則表示解析結果已超出整份 Log。這兩種情況都需要檢查長度欄位與取得的資料是否一致。Get Log Page 的傳輸對齊要求，不會讓每筆事件自動變成相同長度。</p>
</li>
<li id="q-213-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-213-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Base 2.4 沒有「每新增 PEL entry 就回報 PEL Changed AER」的一般事件。 <a class="qa-rule-link" href="#common-pel_query-9">本冊完整規則</a></p>
</li>
<li id="q-213-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>建立 context 固定這次要回報的事件集合；期間新事件仍要記錄，但不能混入既有 context。 <a class="qa-rule-link" href="#common-pel_query-10">本冊完整規則</a></p>
</li>
<li id="q-213-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>PEL 的查詢不是另一筆 PEL 讀取事件。 <a class="qa-rule-link" href="#common-pel_query-11">本冊完整規則</a></p>
</li>
<li id="q-213-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Level Reset 後，PEL 事件內容須保留，但查詢 context 不保證仍有效。 <a class="qa-rule-link" href="#common-pel_query-12">本冊完整規則</a></p>
</li>
<li id="q-213-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 不清除持久事件；Reset 完成時還可能依支援規則新增 Power-on or Reset 事件。 <a class="qa-rule-link" href="#common-pel_query-13">本冊完整規則</a></p>
</li>
<li id="q-213-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>事件內容須跨 Power Cycle 保留，規範也建議設計盡量降低失電時的事件遺失。 <a class="qa-rule-link" href="#common-pel_query-14">本冊完整規則</a></p>
</li>
<li id="q-213-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>PEL 是 subsystem 全域的事件歷史。 <a class="qa-rule-link" href="#common-pel_query-15">本冊完整規則</a></p>
</li>
<li id="q-213-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>較新事件建議放較低 offset，但發生順序判定由廠商決定；Timestamp 可改變，不能直接依數值重排後宣稱原 Log 錯誤。</p>
</li>
<li id="q-213-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否重複把 VSIL 加進總長，或漏了 EHL 的 +3。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-214" data-question="214"><h2><a class="qa-qid" href="#q-214">Q214</a> Timestamp 如何設定並以 Get Features 驗證？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-214-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-214-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Timestamp 讓 Host 提供事件關聯用的時間基準；它不保證可作安全用途，也不是所有 controller 共用的一只時鐘。</p>
</li>
<li id="q-214-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>設定作用於目標 controller；跨 controller 比對仍需處理時間差與 Reset 資訊。</p>
</li>
<li id="q-214-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 Identify.ONCS 的 Timestamp 支援，以及 FID0Eh 的保存能力。</p>
</li>
<li id="q-214-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Set 傳 8-byte buffer，bytes5:0 為自 1970-01-01 UTC 起的毫秒數，bytes7:6 保留；Get 多回 Timestamp Origin 與 SYNC。</p>
</li>
<li id="q-214-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先記錄 Host 時間，送 Set 並等成功，再 Get Current；比較時容許已經過的時間，而不是要求與 Set 值逐 byte 相等。</p>
</li>
<li id="q-214-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Origin=001b 表示由 Set Features 初始化；回值為設定值加上 controller 計入的經過時間。</p>
</li>
<li id="q-214-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援的 Feature、非法欄位或 Save 要求依各自 Feature 錯誤回應。不能把失敗 Set 當成時鐘已更新。</p>
</li>
<li id="q-214-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-214-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Set Timestamp 本身沒有一般的成功 AER；事件時間可能因此改變，但不代表須送出 PEL Changed 通知。 <a class="qa-rule-link" href="#common-timestamp_op-9">本冊完整規則</a></p>
</li>
<li id="q-214-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>成功 Set 後 Get Current 應反映新時間基準；Error Information 仍依命令失敗與記錄條件處理。 <a class="qa-rule-link" href="#common-timestamp_op-10">本冊完整規則</a></p>
</li>
<li id="q-214-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Timestamp 使用專屬 Timestamp Change Event，不得記成一般 Set Feature Event。 <a class="qa-rule-link" href="#common-timestamp_op-11">本冊完整規則</a></p>
</li>
<li id="q-214-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>若此種 CLR 保持 Timestamp 持續計時，就必須保留 Origin；不保持時則依 Timestamp 的初始化／保存規則重新判讀。 <a class="qa-rule-link" href="#common-timestamp_op-12">本冊完整規則</a></p>
</li>
<li id="q-214-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>對每個受重設 controller 分別檢查 Timestamp 是否持續及 Origin；不能假設 subsystem 中所有時鐘數值完全相同。 <a class="qa-rule-link" href="#common-timestamp_op-13">本冊完整規則</a></p>
</li>
<li id="q-214-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>若功能可保存且曾保存，恢復的是 Saved 值，時間可能向後跳；不能要求斷電期間仍一定連續增加。 <a class="qa-rule-link" href="#common-timestamp_op-14">本冊完整規則</a></p>
</li>
<li id="q-214-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>設定一個 controller 的時間不代表替所有 controller 校時。 <a class="qa-rule-link" href="#common-timestamp_op-15">本冊完整規則</a></p>
</li>
<li id="q-214-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>比較設定、Origin、SYNC 與讀取時間點，再決定差值是否合理。</p>
</li>
<li id="q-214-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查傳輸的是毫秒，不是秒，並確認只有低 48 bits 是 Timestamp。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-215" data-question="215"><h2><a class="qa-qid" href="#q-215">Q215</a> Timestamp 如何增加、Wrap-around，Origin 與 SYNC 怎麼看？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-215-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-215-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>同樣的數字可能是 UTC 時間，也可能只是 Reset 後經過時間；必須先解讀屬性。</p>
</li>
<li id="q-215-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>48-bit 值屬於該 controller 的時間基準，不能直接推論跨 controller 的絕對先後。</p>
</li>
<li id="q-215-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Get FID0Eh Current，讀 Timestamp 及 TSTMPS；需要歷史變更時搭配 PEL 的 Timestamp Change。</p>
</li>
<li id="q-215-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Origin=000b 表示 CLR 初始化為 0；001b 表示 Host Set 初始化。SYNC=0 表示初始化後連續計毫秒；SYNC=1 表示可能省略廠商定義的時間區間。</p>
</li>
<li id="q-215-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先確認 Origin，再算經過時間；設定值加經過時間超出 48 bits 時，回報值應以 2^48 取模。</p>
</li>
<li id="q-215-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>在相同基準且沒有其他變更時，差值可按 48-bit 模數計算；SYNC=1 則不能要求與壁鐘完全一致。</p>
</li>
<li id="q-215-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>時間變小可能是 Wrap-around、重設、恢復 Saved 或重新 Set，不必然代表計數器壞掉。</p>
</li>
<li id="q-215-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-215-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Set Timestamp 本身沒有一般的成功 AER；事件時間可能因此改變，但不代表須送出 PEL Changed 通知。 <a class="qa-rule-link" href="#common-timestamp_op-9">本冊完整規則</a></p>
</li>
<li id="q-215-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>成功 Set 後 Get Current 應反映新時間基準；Error Information 仍依命令失敗與記錄條件處理。 <a class="qa-rule-link" href="#common-timestamp_op-10">本冊完整規則</a></p>
</li>
<li id="q-215-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Timestamp 使用專屬 Timestamp Change Event，不得記成一般 Set Feature Event。 <a class="qa-rule-link" href="#common-timestamp_op-11">本冊完整規則</a></p>
</li>
<li id="q-215-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>若此種 CLR 保持 Timestamp 持續計時，就必須保留 Origin；不保持時則依 Timestamp 的初始化／保存規則重新判讀。 <a class="qa-rule-link" href="#common-timestamp_op-12">本冊完整規則</a></p>
</li>
<li id="q-215-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>對每個受重設 controller 分別檢查 Timestamp 是否持續及 Origin；不能假設 subsystem 中所有時鐘數值完全相同。 <a class="qa-rule-link" href="#common-timestamp_op-13">本冊完整規則</a></p>
</li>
<li id="q-215-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>若功能可保存且曾保存，恢復的是 Saved 值，時間可能向後跳；不能要求斷電期間仍一定連續增加。 <a class="qa-rule-link" href="#common-timestamp_op-14">本冊完整規則</a></p>
</li>
<li id="q-215-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>設定一個 controller 的時間不代表替所有 controller 校時。 <a class="qa-rule-link" href="#common-timestamp_op-15">本冊完整規則</a></p>
</li>
<li id="q-215-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>用 Origin、SYNC、Reset 事件與 Timestamp Change 排除基準切換後，再比較先後。</p>
</li>
<li id="q-215-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查比較的兩個時間點是否仍屬同一個時間基準。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-216" data-question="216"><h2><a class="qa-qid" href="#q-216">Q216</a> Timestamp 變更如何記錄，Reset 與 Power Cycle 後怎麼判讀？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-216-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-216-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>事件時間會因校時而不連續，Timestamp Change 提供連接新舊時間基準的資訊。</p>
</li>
<li id="q-216-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>變更與 Reset 都要依相關 controller 判讀，不能把整個 subsystem 當成單一時鐘。</p>
</li>
<li id="q-216-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>確認 Timestamp 與 PEL 支援，保存目前值、Origin、SYNC、Saved 及 Reset 來源。</p>
</li>
<li id="q-216-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>ET03h 的 Header 時間描述新時間，PTSTP 保存變更前時間，MSR 表示距上次 CLR 的毫秒數。</p>
</li>
<li id="q-216-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先用 PTSTP 與 Header 建立新舊基準關係，再用 MSR、Power-on or Reset descriptors 比對控制器間的觀察。</p>
</li>
<li id="q-216-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>若 CLR 持續維持 Timestamp，Origin 也必須保留；若不維持，須按初始化與可能的 Saved 恢復重新解讀。</p>
</li>
<li id="q-216-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不能把校時造成的時間倒退判成 PEL 順序違規，也不能把 Timestamp 記成 ET0Bh 的普通 Set Feature 事件。</p>
</li>
<li id="q-216-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-216-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Set Timestamp 本身沒有一般的成功 AER；事件時間可能因此改變，但不代表須送出 PEL Changed 通知。 <a class="qa-rule-link" href="#common-timestamp_op-9">本冊完整規則</a></p>
</li>
<li id="q-216-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>成功 Set 後 Get Current 應反映新時間基準；Error Information 仍依命令失敗與記錄條件處理。 <a class="qa-rule-link" href="#common-timestamp_op-10">本冊完整規則</a></p>
</li>
<li id="q-216-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Timestamp 使用專屬 Timestamp Change Event，不得記成一般 Set Feature Event。 <a class="qa-rule-link" href="#common-timestamp_op-11">本冊完整規則</a></p>
</li>
<li id="q-216-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>若此種 CLR 保持 Timestamp 持續計時，就必須保留 Origin；不保持時則依 Timestamp 的初始化／保存規則重新判讀。 <a class="qa-rule-link" href="#common-timestamp_op-12">本冊完整規則</a></p>
</li>
<li id="q-216-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>對每個受重設 controller 分別檢查 Timestamp 是否持續及 Origin；不能假設 subsystem 中所有時鐘數值完全相同。 <a class="qa-rule-link" href="#common-timestamp_op-13">本冊完整規則</a></p>
</li>
<li id="q-216-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>若功能可保存且曾保存，恢復的是 Saved 值，時間可能向後跳；不能要求斷電期間仍一定連續增加。 <a class="qa-rule-link" href="#common-timestamp_op-14">本冊完整規則</a></p>
</li>
<li id="q-216-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>設定一個 controller 的時間不代表替所有 controller 校時。 <a class="qa-rule-link" href="#common-timestamp_op-15">本冊完整規則</a></p>
</li>
<li id="q-216-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>重設後的 Get、Timestamp Change 與 Power-on or Reset 應能形成合理的時間解釋，但不能假設所有事件時間都單調增加。</p>
</li>
<li id="q-216-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查時間是否被重新設定或恢復 Saved，再調查事件排序。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-nvmpel">NVM Command Set 1.3 §4.1.4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-command-8"><h3>命令完成、事件與紀錄 · DNR 與 More 應如何設定？</h3><p>只有收到 CQE，才有 DNR 與 More 可供判讀。DNR=1 表示相同命令即使重送到此 NVM subsystem 的任一 controller，仍預期會失敗；DNR=0 則只表示可能成功。除非個別錯誤條件另有明定，不能只看 Status 名稱就要求 DNR=1。More=1 表示 Error Information Log 有這筆命令的補充資訊。SCT=SC=0 時，DNR 應為 0。</p></article>
<article id="common-pel_query-9"><h3>本主題的共用條件 · 是否產生 Asynchronous Event？</h3><p>Base 2.4 沒有「每新增 PEL entry 就回報 PEL Changed AER」的一般事件。造成紀錄的原始狀況可能有自己的通知，例如 SMART 警告或 Sanitize；必須依原始事件的條件判斷。</p></article>
<article id="common-pel_query-10"><h3>本主題的共用條件 · 是否更新 Error Information Log 或其他 Log？</h3><p>建立 context 固定這次要回報的事件集合；期間新事件仍要記錄，但不能混入既有 context。讀取或釋放 context 不代表清空 PEL，錯誤的 Get Log 則另依 Error Information 規則處理。</p></article>
<article id="common-pel_query-11"><h3>本主題的共用條件 · 是否記錄於 Persistent Event Log？</h3><p>PEL 的查詢不是另一筆 PEL 讀取事件。只有受支援的原始事件才依各自觸發條件記錄；高頻相同事件可依規範允許的廠商門檻抑制，不能要求無限逐筆重複。</p></article>
<article id="common-pel_query-12"><h3>本主題的共用條件 · Controller Reset 後是否保留或繼續？</h3><p>Controller Level Reset 後，PEL 事件內容須保留，但查詢 context 不保證仍有效。恢復查詢通道後重新建立 context，不能把中斷前的半份資料接上新的 context。</p></article>
<article id="common-pel_query-13"><h3>本主題的共用條件 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>Subsystem Reset 不清除持久事件；Reset 完成時還可能依支援規則新增 Power-on or Reset 事件。報告 context 的保留是另一回事，應重新建立一致的讀取範圍。</p></article>
<article id="common-pel_query-14"><h3>本主題的共用條件 · Power Cycle 後是否保留或繼續？</h3><p>事件內容須跨 Power Cycle 保留，規範也建議設計盡量降低失電時的事件遺失。容量淘汰、高頻抑制，以及 Sanitize 為避免洩漏使用者資料而移除或修改事件，是不同的例外，不能把它們誤認為一般斷電清空。</p></article>
<article id="common-pel_query-15"><h3>本主題的共用條件 · 是否影響其他 Controller 或 Namespace？</h3><p>PEL 是 subsystem 全域的事件歷史。事件 Header 的 CNTLID 指出建立紀錄的 controller；影響多個 controller 的事件建議只記一次，不要求每條路徑都有一份副本。共享查詢 context 時須避免一端釋放另一端仍在讀的 context。</p></article>
<article id="common-timestamp_op-9"><h3>本主題的共用條件 · 是否產生 Asynchronous Event？</h3><p>Set Timestamp 本身沒有一般的成功 AER；事件時間可能因此改變，但不代表須送出 PEL Changed 通知。</p></article>
<article id="common-timestamp_op-10"><h3>本主題的共用條件 · 是否更新 Error Information Log 或其他 Log？</h3><p>成功 Set 後 Get Current 應反映新時間基準；Error Information 仍依命令失敗與記錄條件處理。</p></article>
<article id="common-timestamp_op-11"><h3>本主題的共用條件 · 是否記錄於 Persistent Event Log？</h3><p>Timestamp 使用專屬 Timestamp Change Event，不得記成一般 Set Feature Event。</p></article>
<article id="common-timestamp_op-12"><h3>本主題的共用條件 · Controller Reset 後是否保留或繼續？</h3><p>若此種 CLR 保持 Timestamp 持續計時，就必須保留 Origin；不保持時則依 Timestamp 的初始化／保存規則重新判讀。</p></article>
<article id="common-timestamp_op-13"><h3>本主題的共用條件 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>對每個受重設 controller 分別檢查 Timestamp 是否持續及 Origin；不能假設 subsystem 中所有時鐘數值完全相同。</p></article>
<article id="common-timestamp_op-14"><h3>本主題的共用條件 · Power Cycle 後是否保留或繼續？</h3><p>若功能可保存且曾保存，恢復的是 Saved 值，時間可能向後跳；不能要求斷電期間仍一定連續增加。</p></article>
<article id="common-timestamp_op-15"><h3>本主題的共用條件 · 是否影響其他 Controller 或 Namespace？</h3><p>設定一個 controller 的時間不代表替所有 controller 校時。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>文件頁 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>文件頁 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-getfeat"><strong>Base 2.4 · §5.2.12</strong><br>文件頁 209–212 · PDF 235–238 · Figure 197–202</li>
<li id="ref-getlog"><strong>Base 2.4 · §5.2.13–5.2.13.1.1</strong><br>文件頁 212–218 · PDF 238–244 · Figure 203–211</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-smart"><strong>Base 2.4 · §5.2.13.1.3</strong><br>文件頁 220–225 · PDF 246–251 · Figure 213–214</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-pelcontext"><strong>Base 2.4 · §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</strong><br>文件頁 244–256, 258 · PDF 270–282, 284 · Figure 232–244, 246</li>
<li id="ref-fwpel"><strong>Base 2.4 · §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</strong><br>文件頁 252–255 · PDF 278–281 · Figure 238, 240–241</li>
<li id="ref-nspelevent"><strong>Base 2.4 · §5.2.13.1.14.2.6</strong><br>文件頁 258–259 · PDF 284–285 · Figure 247</li>
<li id="ref-formatpel"><strong>Base 2.4 · §5.2.13.1.14.2.7–5.2.13.1.14.2.8</strong><br>文件頁 259–261 · PDF 285–287 · Figure 248–249</li>
<li id="ref-sanitizepel"><strong>Base 2.4 · §5.2.13.1.14.2.9–5.2.13.1.14.2.10</strong><br>文件頁 261–262 · PDF 287–288 · Figure 250–251</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>文件頁 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>文件頁 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-aec"><strong>Base 2.4 · §5.2.30.1.6</strong><br>文件頁 466–468 · PDF 492–494 · Figure 474</li>
<li id="ref-timestamp"><strong>Base 2.4 · §5.2.30.1.8</strong><br>文件頁 469–471 · PDF 495–497 · Figure 479–480</li>
<li id="ref-nvmpel"><strong>NVM Command Set 1.3 · §4.1.4.4</strong><br>文件頁 76–77 · PDF 76–77 · Figure 112</li>
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
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/persistent-events/en/">English</a><a href="/DOCS/nvme-question-bank/persistent-events.html">繁中教學 HTML</a></nav>
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
