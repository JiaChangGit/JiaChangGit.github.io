---
layout: post
title: "NVMe 自問自答題庫：Power、Thermal 與 Health Monitoring"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/health/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/health/en/">English</a><a href="/DOCS/nvme-question-bank/health.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q188–Q204</p><h1>Power、Thermal 與 Health Monitoring</h1><p class="qr-intro">功耗狀態、溫度控制與健康計數互相關聯，但各自回答不同問題。本冊先建立狀態與時間概念，再學習如何讀取警告與工作量。</p><p>先練習，再展開每題的 17 項解答。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>控制值、目前值、累計值分開看</h2><p class="qa-takeaway">設定門檻不等於發生警告；警告恢復也不會把累計工作量清除。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">種類</th><th scope="col">例子</th><th scope="col">比較方式</th></tr></thead><tbody><tr><td>控制</td><td>APST.ITPT、HCTM.TMT1／2</td><td>先確認單位與支援</td></tr><tr><td>目前狀態</td><td>溫度、Critical Warning</td><td>與同時點條件比對</td></tr><tr><td>累計</td><td>Data Units、Busy Time、UPL</td><td>前後差值與取整</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>APST 閒置 2000ms 與 PSD.EXLAT=100µs 發生在不同階段：前者是開始進入低功耗前的等待，後者是離開時延遲。不能把它們當成每筆命令固定延遲。</p>
<p class="qa-citations">來源：<a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-188">Q188 · Power State Descriptor 能告訴 Host 哪些事情？</a></li>
<li><a href="#q-189">Q189 · Operational 與 Non-Operational Power State 差在哪裡？</a></li>
<li><a href="#q-190">Q190 · Entry 與 Exit Latency 如何影響命令等待時間？</a></li>
<li><a href="#q-191">Q191 · APST 如何設定、觸發與停用？</a></li>
<li><a href="#q-192">Q192 · 量到恢復延遲超過 EXLAT，如何判斷是否違規？</a></li>
<li><a href="#q-193">Q193 · HCTM 的 TMT1 與 TMT2 應如何設定？</a></li>
<li><a href="#q-194">Q194 · Controller 何時開始或停止 Thermal Management？</a></li>
<li><a href="#q-195">Q195 · Reset 與 Power Cycle 後，Power／Thermal 設定如何恢復？</a></li>
<li><a href="#q-196">Q196 · SMART Critical Warning 的各 bit 代表什麼？</a></li>
<li><a href="#q-197">Q197 · Available Spare、Threshold 與 Percentage Used 如何解讀？</a></li>
<li><a href="#q-198">Q198 · 資料量、命令數、Busy Time、Power Cycles 與 Power On Hours 如何累計？</a></li>
<li><a href="#q-199">Q199 · Unexpected Power Losses、媒體錯誤與 Error Log Entries 如何累計？</a></li>
<li><a href="#q-200">Q200 · Warning 與 Critical Composite Temperature Time 如何累計？</a></li>
<li><a href="#q-201">Q201 · 多個 Temperature Sensor 與 Composite Temperature 如何比較？</a></li>
<li><a href="#q-202">Q202 · 哪些 Health 變化會產生 AER？</a></li>
<li><a href="#q-203">Q203 · SMART 資料的 Scope 如何判斷？</a></li>
<li><a href="#q-204">Q204 · SMART、實際操作、Error Log 與 PEL 如何交叉驗證？</a></li>
</ol></section>
<article class="qa-question" id="q-188" data-question="188"><h2><a class="qa-qid" href="#q-188">Q188</a> Power State Descriptor 能告訴 Host 哪些事情？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-188-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-188-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Host 需要在功耗、效能與喚醒時間之間選擇。Descriptor 提供可比較的狀態資料，但不是保證每一筆命令都在相同時間內完成。</p>
</li>
<li id="q-188-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>每個 controller 依 NPSS 提供 PS0 到 PSn；NPSS 採 zero-based 編碼，例如 4 代表 5 個狀態。</p>
</li>
<li id="q-188-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先確認 Power Management 適用於此 controller，再查 NPSS 與各筆 PSD。對不支援此功能的 controller，Host 應忽略 PSD。</p>
</li>
<li id="q-188-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>NOPS 區分工作與非工作狀態；MP 配合功率尺度，ENLAT／EXLAT 以微秒描述進出延遲。RRT、RRL、RWT、RWL 是相對效能排序；IDLP、ACTP 各有尺度與量測條件，MBW 配合 MBWS 表示宣告的最高頻寬。</p>
</li>
<li id="q-188-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先比較 NOPS 與最大功率，再比較進出延遲，最後以相同種類的相對效能欄位排序。不同欄位的數字不能交叉比較。</p>
</li>
<li id="q-188-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Identify 成功後，Host 能挑出合適狀態；真正設定仍須透過 Power Management 或 APST。</p>
</li>
<li id="q-188-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>超出 NPSS 的狀態不是合法選項；設定非法 Power State 時應回報 Invalid Field in Command。未宣告的量測值也不能解讀成零功耗或零延遲保證。</p>
</li>
<li id="q-188-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-188-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>切換 Power State 或開始降速，不會自動產生同名的 AER。 <a class="qa-rule-link" href="#common-power_config-9">本冊完整規則</a></p>
</li>
<li id="q-188-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>SMART 的 Thermal Management transition count 與累計時間可協助確認 HCTM 行為；一般 Power State 切換沒有逐次記錄的標準 Log。 <a class="qa-rule-link" href="#common-power_config-10">本冊完整規則</a></p>
</li>
<li id="q-188-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>若支援 PEL 的 Set Feature Event，先確認該 FID 可記錄且已宣告支援。 <a class="qa-rule-link" href="#common-power_config-11">本冊完整規則</a></p>
</li>
<li id="q-188-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>先確認 Feature 作用範圍、保存能力及重設實際涵蓋的物件，再決定恢復方式。整個 subsystem 與只有部分範圍受重設時，規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-188-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確認重設影響整個 NVM subsystem，還是其中一部分。Feature 即使不可保存，只要明定具有持續性，就不能要求它因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-188-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存的 Feature 依 Saved 恢復；不可保存的 Feature，則依持續性及個別例外判斷。不能只用有沒有 Save 能力決定是否保留。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-188-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>先查 Feature 的作用範圍，再判斷其他 controller 或 namespace 是否共用這項設定，以及是否會一同受影響。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-188-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>把 PSD 的 NOPS、功率尺度與 Feature 選中的狀態一起核對；不要把相對排名當作實際 IOPS。</p>
</li>
<li id="q-188-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否把 NPSS 當成狀態總數，或漏乘功率、頻寬的尺度。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-189" data-question="189"><h2><a class="qa-qid" href="#q-189">Q189</a> Operational 與 Non-Operational Power State 差在哪裡？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-189-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-189-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這個分類回答「目前是否準備好處理 I/O」，不是在說 controller 是否完全斷電。</p>
</li>
<li id="q-189-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>NOPS=0 為工作狀態；NOPS=1 為非工作狀態。非工作狀態仍可能處理 Register、Admin 命令與允許的背景工作。</p>
</li>
<li id="q-189-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 PSD.NOPS、目前 Power Management 設定與 Non-Operational Power State Config。</p>
</li>
<li id="q-189-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>APST 可自動進入非工作狀態；NOPPME 控制非工作狀態中的背景工作政策，不能當成禁止所有 Admin 存取的開關。</p>
</li>
<li id="q-189-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>進入非工作狀態後若需處理 I/O，controller 自動回到最近的工作狀態，再處理 I/O；這項恢復不以 APST 是否啟用為前提。</p>
</li>
<li id="q-189-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>I/O 能在恢復工作狀態後完成；Host 不需先用 Set Features 喚醒每一筆 I/O。</p>
</li>
<li id="q-189-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不能因合法 I/O 到達非工作狀態就直接判定命令非法；若指定不存在的 Power State，才是設定參數問題。</p>
</li>
<li id="q-189-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-189-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>切換 Power State 或開始降速，不會自動產生同名的 AER。 <a class="qa-rule-link" href="#common-power_config-9">本冊完整規則</a></p>
</li>
<li id="q-189-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>SMART 的 Thermal Management transition count 與累計時間可協助確認 HCTM 行為；一般 Power State 切換沒有逐次記錄的標準 Log。 <a class="qa-rule-link" href="#common-power_config-10">本冊完整規則</a></p>
</li>
<li id="q-189-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>若支援 PEL 的 Set Feature Event，先確認該 FID 可記錄且已宣告支援。 <a class="qa-rule-link" href="#common-power_config-11">本冊完整規則</a></p>
</li>
<li id="q-189-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>先確認 Feature 作用範圍、保存能力及重設實際涵蓋的物件，再決定恢復方式。整個 subsystem 與只有部分範圍受重設時，規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-189-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確認重設影響整個 NVM subsystem，還是其中一部分。Feature 即使不可保存，只要明定具有持續性，就不能要求它因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-189-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存的 Feature 依 Saved 恢復；不可保存的 Feature，則依持續性及個別例外判斷。不能只用有沒有 Save 能力決定是否保留。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-189-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>先查 Feature 的作用範圍，再判斷其他 controller 或 namespace 是否共用這項設定，以及是否會一同受影響。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-189-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>看到非工作狀態期間仍有 Admin 活動或暫時較高功耗，不足以單獨判定違規；須核對允許的操作與功率上限。</p>
</li>
<li id="q-189-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認測到的是 I/O、Admin 還是背景工作，不能只看「裝置仍有活動」。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-190" data-question="190"><h2><a class="qa-qid" href="#q-190">Q190</a> Entry 與 Exit Latency 如何影響命令等待時間？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-190-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-190-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>命令可能必須等狀態切換完成，因此需把轉換時間與命令本身的執行時間分開。</p>
</li>
<li id="q-190-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>ENLAT 描述進入目標狀態，EXLAT 描述離開原狀態；切換路徑涉及多個狀態時，不能只取其中最小值。</p>
</li>
<li id="q-190-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀取原狀態與目標狀態的 PSD；非工作狀態恢復 I/O 時也需知道最近的工作狀態。</p>
</li>
<li id="q-190-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>以微秒為單位計算原狀態 EXLAT 加目標狀態 ENLAT。ITPT 則是進入轉換之前的閒置等待時間，單位是毫秒。</p>
</li>
<li id="q-190-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先確認切換開始時間與路徑，量測恢復可處理命令的時間，再另計命令執行與 Host 排程延遲。</p>
</li>
<li id="q-190-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例如假設 PS3.EXLAT=2000 μs、PS0.ENLAT=500 μs，這段轉換的宣告上限為 2500 μs；不能要求完整 Read 也一定在 2500 μs 內完成。</p>
</li>
<li id="q-190-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Host 量到較慢的 CQE 不會直接產生一個「Exit Latency Error」Status；必須先證明超時發生在受規範限制的轉換階段。</p>
</li>
<li id="q-190-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-190-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>切換 Power State 或開始降速，不會自動產生同名的 AER。 <a class="qa-rule-link" href="#common-power_config-9">本冊完整規則</a></p>
</li>
<li id="q-190-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>SMART 的 Thermal Management transition count 與累計時間可協助確認 HCTM 行為；一般 Power State 切換沒有逐次記錄的標準 Log。 <a class="qa-rule-link" href="#common-power_config-10">本冊完整規則</a></p>
</li>
<li id="q-190-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>若支援 PEL 的 Set Feature Event，先確認該 FID 可記錄且已宣告支援。 <a class="qa-rule-link" href="#common-power_config-11">本冊完整規則</a></p>
</li>
<li id="q-190-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>先確認 Feature 作用範圍、保存能力及重設實際涵蓋的物件，再決定恢復方式。整個 subsystem 與只有部分範圍受重設時，規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-190-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確認重設影響整個 NVM subsystem，還是其中一部分。Feature 即使不可保存，只要明定具有持續性，就不能要求它因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-190-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存的 Feature 依 Saved 恢復；不可保存的 Feature，則依持續性及個別例外判斷。不能只用有沒有 Save 能力決定是否保留。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-190-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>先查 Feature 的作用範圍，再判斷其他 controller 或 namespace 是否共用這項設定，以及是否會一同受影響。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-190-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>比對 PSD、實際原始狀態、APST 路徑與量測邊界，而不是只比 Read 總延遲。</p>
</li>
<li id="q-190-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查微秒與毫秒是否混用，以及是否把媒體讀取時間算進 EXLAT。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-191" data-question="191"><h2><a class="qa-qid" href="#q-191">Q191</a> APST 如何設定、觸發與停用？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-191-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-191-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>APST 讓 controller 在 I/O 閒置時自動降低功耗，Host 不必為每次閒置另送切換命令。</p>
</li>
<li id="q-191-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>每個來源 Power State 有一筆 8-byte entry；整份資料有 32 筆，共 256 bytes。</p>
</li>
<li id="q-191-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>確認 Identify.APSTA 與 NPSS，並核對目標 PSD.NOPS。</p>
</li>
<li id="q-191-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>FID0Ch 的 APSTE 啟用整體功能；entry.ITPT 指定閒置毫秒數，ITPS 指定目標。ITPT=0 停用該來源狀態的自動轉換。</p>
</li>
<li id="q-191-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>填好各來源 entry，Set Features，再 Get Features 核對。沒有 outstanding I/O，且連續閒置時間超過 ITPT，才符合這條轉換的觸發條件。</p>
</li>
<li id="q-191-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例如 PS0 entry 設 ITPT=2000、ITPS=3，低 Dword 為 0007D018h；APSTE=1 時，PS0 閒置超過 2 s 可轉入受支援的非工作 PS3。</p>
</li>
<li id="q-191-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>ITPT 非零時，ITPS 必須是非工作狀態；指定工作狀態應以 Invalid Field in Command 中止。停用整體功能使用 APSTE=0。</p>
</li>
<li id="q-191-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-191-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>切換 Power State 或開始降速，不會自動產生同名的 AER。 <a class="qa-rule-link" href="#common-power_config-9">本冊完整規則</a></p>
</li>
<li id="q-191-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>SMART 的 Thermal Management transition count 與累計時間可協助確認 HCTM 行為；一般 Power State 切換沒有逐次記錄的標準 Log。 <a class="qa-rule-link" href="#common-power_config-10">本冊完整規則</a></p>
</li>
<li id="q-191-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>若支援 PEL 的 Set Feature Event，先確認該 FID 可記錄且已宣告支援。 <a class="qa-rule-link" href="#common-power_config-11">本冊完整規則</a></p>
</li>
<li id="q-191-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>先確認 Feature 作用範圍、保存能力及重設實際涵蓋的物件，再決定恢復方式。整個 subsystem 與只有部分範圍受重設時，規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-191-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確認重設影響整個 NVM subsystem，還是其中一部分。Feature 即使不可保存，只要明定具有持續性，就不能要求它因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-191-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存的 Feature 依 Saved 恢復；不可保存的 Feature，則依持續性及個別例外判斷。不能只用有沒有 Save 能力決定是否保留。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-191-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>先查 Feature 的作用範圍，再判斷其他 controller 或 namespace 是否共用這項設定，以及是否會一同受影響。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-191-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Get 回傳的是設定表，不是每次切換的歷史。若背景工作阻止進入較低功耗狀態，還要核對背景功耗與政策。</p>
</li>
<li id="q-191-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查設定的是「目前來源狀態」那一筆 entry，還是誤把目標狀態當作表格索引。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-192" data-question="192"><h2><a class="qa-qid" href="#q-192">Q192</a> 量到恢復延遲超過 EXLAT，如何判斷是否違規？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-192-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-192-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>要判斷韌體是否超過宣告，必須量到相同的事件邊界，不能把 Host 等待時間全部歸給 controller。</p>
</li>
<li id="q-192-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>先限定一個 controller、一條已知狀態路徑與一次喚醒。</p>
</li>
<li id="q-192-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>保存 PSD、APST、Power Management、溫度與目前背景操作。</p>
</li>
<li id="q-192-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>使用原狀態 EXLAT 與目標 ENLAT；若測的是 RTD3，則是另一套供電恢復與初始化條件，不能沿用 NOPS 退出公式。</p>
</li>
<li id="q-192-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先排除命令尚未提交、Host 排程、中斷合併及媒體執行時間，再定位真正的轉換區間。</p>
</li>
<li id="q-192-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>在前提一致下，量測可支持「轉換符合／超過宣告」；前提不明時，只能說端到端延遲較高。</p>
</li>
<li id="q-192-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>EXLAT 超出不是要求 controller 回傳某個固定 CQE 的命令參數錯誤。</p>
</li>
<li id="q-192-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-192-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>切換 Power State 或開始降速，不會自動產生同名的 AER。 <a class="qa-rule-link" href="#common-power_config-9">本冊完整規則</a></p>
</li>
<li id="q-192-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>SMART 的 Thermal Management transition count 與累計時間可協助確認 HCTM 行為；一般 Power State 切換沒有逐次記錄的標準 Log。 <a class="qa-rule-link" href="#common-power_config-10">本冊完整規則</a></p>
</li>
<li id="q-192-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>若支援 PEL 的 Set Feature Event，先確認該 FID 可記錄且已宣告支援。 <a class="qa-rule-link" href="#common-power_config-11">本冊完整規則</a></p>
</li>
<li id="q-192-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>先確認 Feature 作用範圍、保存能力及重設實際涵蓋的物件，再決定恢復方式。整個 subsystem 與只有部分範圍受重設時，規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-192-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確認重設影響整個 NVM subsystem，還是其中一部分。Feature 即使不可保存，只要明定具有持續性，就不能要求它因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-192-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存的 Feature 依 Saved 恢復；不可保存的 Feature，則依持續性及個別例外判斷。不能只用有沒有 Save 能力決定是否保留。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-192-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>先查 Feature 的作用範圍，再判斷其他 controller 或 namespace 是否共用這項設定，以及是否會一同受影響。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-192-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>用重複的受控量測核對宣告上限，保留時間解析度與量測誤差，不用單次應用程式時間直接定罪。</p>
</li>
<li id="q-192-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認延遲起點是否真的代表 controller 開始離開該 Power State。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-193" data-question="193"><h2><a class="qa-qid" href="#q-193">Q193</a> HCTM 的 TMT1 與 TMT2 應如何設定？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-193-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-193-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>HCTM 讓 Host 指定希望 controller 採取散熱措施的溫度，並區分較輕與較重的效能影響。</p>
</li>
<li id="q-193-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>以 Composite Temperature 作判斷，作用於目標 controller 的熱管理。</p>
</li>
<li id="q-193-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 Identify.HCTMA、MNTMT、MXTMT；不是所有 controller 都支援 Host 控制熱管理。</p>
</li>
<li id="q-193-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>FID10h 的 CDW11[31:16] 為 TMT1，[15:0] 為 TMT2，單位都是 Kelvin；0 停用對應部分。</p>
</li>
<li id="q-193-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>將非零門檻設在宣告範圍；兩者皆非零時必須 TMT1&lt;TMT2。Set 成功後 Get 確認，不要直接填攝氏數字。</p>
</li>
<li id="q-193-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>假設允許 300～360 K，設定 330 K 與 340 K 合法；設定 340 K 與 330 K 則顛倒輕重門檻。</p>
</li>
<li id="q-193-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>非零門檻超出範圍，或兩個啟用門檻不符合先後關係，須回 Invalid Field in Command。</p>
</li>
<li id="q-193-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-193-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>切換 Power State 或開始降速，不會自動產生同名的 AER。 <a class="qa-rule-link" href="#common-power_config-9">本冊完整規則</a></p>
</li>
<li id="q-193-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>SMART 的 Thermal Management transition count 與累計時間可協助確認 HCTM 行為；一般 Power State 切換沒有逐次記錄的標準 Log。 <a class="qa-rule-link" href="#common-power_config-10">本冊完整規則</a></p>
</li>
<li id="q-193-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>若支援 PEL 的 Set Feature Event，先確認該 FID 可記錄且已宣告支援。 <a class="qa-rule-link" href="#common-power_config-11">本冊完整規則</a></p>
</li>
<li id="q-193-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>先確認 Feature 作用範圍、保存能力及重設實際涵蓋的物件，再決定恢復方式。整個 subsystem 與只有部分範圍受重設時，規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-193-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確認重設影響整個 NVM subsystem，還是其中一部分。Feature 即使不可保存，只要明定具有持續性，就不能要求它因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-193-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存的 Feature 依 Saved 恢復；不可保存的 Feature，則依持續性及個別例外判斷。不能只用有沒有 Save 能力決定是否保留。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-193-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>先查 Feature 的作用範圍，再判斷其他 controller 或 namespace 是否共用這項設定，以及是否會一同受影響。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-193-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Get 的門檻、SMART 溫度與熱管理累計應一起看；溫度警告 FID04h 另有自己的設定。</p>
</li>
<li id="q-193-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查單位、上下 16 bits 的位置與 0 的停用意義。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-194" data-question="194"><h2><a class="qa-qid" href="#q-194">Q194</a> Controller 何時開始或停止 Thermal Management？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-194-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-194-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>門檻決定何時採取措施，但規範沒有替所有裝置指定相同的降速曲線。</p>
</li>
<li id="q-194-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>判斷使用 Composite Temperature，而不是任選一個實體 sensor。</p>
</li>
<li id="q-194-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先確認 HCTM 已啟用的門檻，以及 SMART 的 CTEMP、TMT1TC、TMT2TC 與累計秒數。</p>
</li>
<li id="q-194-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>TMT1 啟用且溫度達 TMT1、未達啟用的 TMT2 時，controller 應開始較輕措施；達啟用的 TMT2 時，必須採取措施而不受效能影響限制。</p>
</li>
<li id="q-194-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>追蹤升溫跨越門檻及降溫恢復的過程。恢復溫度有廠商定義的遲滯，不能要求溫度一低於 TMT2 就立即完全恢復。</p>
</li>
<li id="q-194-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>可觀察到功率或效能調整，且對應 transition count／time 有一致紀錄；實際措施可由廠商決定。</p>
</li>
<li id="q-194-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>低於 TMT2 後仍降速，不足以直接判定錯誤；先核對 TMT1、遲滯及其他熱保護來源。</p>
</li>
<li id="q-194-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-194-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>切換 Power State 或開始降速，不會自動產生同名的 AER。 <a class="qa-rule-link" href="#common-power_config-9">本冊完整規則</a></p>
</li>
<li id="q-194-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>SMART 的 Thermal Management transition count 與累計時間可協助確認 HCTM 行為；一般 Power State 切換沒有逐次記錄的標準 Log。 <a class="qa-rule-link" href="#common-power_config-10">本冊完整規則</a></p>
</li>
<li id="q-194-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>若支援 PEL 的 Set Feature Event，先確認該 FID 可記錄且已宣告支援。 <a class="qa-rule-link" href="#common-power_config-11">本冊完整規則</a></p>
</li>
<li id="q-194-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>先確認 Feature 作用範圍、保存能力及重設實際涵蓋的物件，再決定恢復方式。整個 subsystem 與只有部分範圍受重設時，規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-194-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確認重設影響整個 NVM subsystem，還是其中一部分。Feature 即使不可保存，只要明定具有持續性，就不能要求它因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-194-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存的 Feature 依 Saved 恢復；不可保存的 Feature，則依持續性及個別例外判斷。不能只用有沒有 Save 能力決定是否保留。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-194-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>先查 Feature 的作用範圍，再判斷其他 controller 或 namespace 是否共用這項設定，以及是否會一同受影響。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-194-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>把 should 與 shall 分開檢查，不把輕度門檻的建議要求提高成重度門檻的強制要求。</p>
</li>
<li id="q-194-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認正在生效的是 HCTM，還是裝置自己的其他熱保護。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-195" data-question="195"><h2><a class="qa-qid" href="#q-195">Q195</a> Reset 與 Power Cycle 後，Power／Thermal 設定如何恢復？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-195-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-195-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>要分開「保存的設定」、「目前設定」與「正在發生的熱或電源狀態」，否則容易把正常恢復誤判成設定遺失。</p>
</li>
<li id="q-195-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>逐一檢查 Power Management、APST、HCTM 與 NOPS Config，不能將它們當成一個 Feature。</p>
</li>
<li id="q-195-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Get Features SEL=3 查保存能力，SEL=0／1／2 分別觀察 Current、Default、Saved；另查 Feature scope。</p>
</li>
<li id="q-195-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>SV=1 的成功 Set 更新 Saved；SV=0 只改 Current。不可保存的 Feature 依明定的持續性恢復。</p>
</li>
<li id="q-195-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>重設前保存四種查詢結果，重設後先恢復 Admin Queue，再重新 Get，最後檢查狀態轉換是否符合恢復後的設定。</p>
</li>
<li id="q-195-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Current 應等於該範圍與重設條件所要求的恢復值；不是一定等於重設前最後一次 SV=0 的值。</p>
</li>
<li id="q-195-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援 Save 卻要求 SV=1 時，應使用對應 Feature Not Saveable 等明定錯誤；不能把失敗 Set 當成已保存。</p>
</li>
<li id="q-195-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-195-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>切換 Power State 或開始降速，不會自動產生同名的 AER。 <a class="qa-rule-link" href="#common-power_config-9">本冊完整規則</a></p>
</li>
<li id="q-195-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>SMART 的 Thermal Management transition count 與累計時間可協助確認 HCTM 行為；一般 Power State 切換沒有逐次記錄的標準 Log。 <a class="qa-rule-link" href="#common-power_config-10">本冊完整規則</a></p>
</li>
<li id="q-195-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>若支援 PEL 的 Set Feature Event，先確認該 FID 可記錄且已宣告支援。 <a class="qa-rule-link" href="#common-power_config-11">本冊完整規則</a></p>
</li>
<li id="q-195-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>先確認 Feature 作用範圍、保存能力及重設實際涵蓋的物件，再決定恢復方式。整個 subsystem 與只有部分範圍受重設時，規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-195-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確認重設影響整個 NVM subsystem，還是其中一部分。Feature 即使不可保存，只要明定具有持續性，就不能要求它因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-195-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存的 Feature 依 Saved 恢復；不可保存的 Feature，則依持續性及個別例外判斷。不能只用有沒有 Save 能力決定是否保留。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-195-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>先查 Feature 的作用範圍，再判斷其他 controller 或 namespace 是否共用這項設定，以及是否會一同受影響。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-195-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>SMART 溫度與累計計數不因 Feature 回到 Default 就必須歸零。</p>
</li>
<li id="q-195-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查最後一次 Set 的 SV、實際 CQE，以及重設是否涵蓋全部共用範圍。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-196" data-question="196"><h2><a class="qa-qid" href="#q-196">Q196</a> SMART Critical Warning 的各 bit 代表什麼？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-196-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-196-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Critical Warning 提供現在的警告狀態，讓 Host 判斷是否需要處理容量、溫度、可靠性或唯讀問題。它不是永久鎖存的事件歷史。</p>
</li>
<li id="q-196-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>每個 bit 獨立，可同時成立；讀取時的狀態可能與先前 AER 產生時不同。</p>
</li>
<li id="q-196-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀 SMART LID02h，並核對 AEC 的 SHCW 啟用遮罩與相關硬體能力。</p>
</li>
<li id="q-196-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>bit0 備用容量低於門檻；bit1 溫度達上限或下限；bit2 可靠性降低；bit3 全部媒體唯讀；bit4 揮發記憶體備援失敗；bit5 PMR 唯讀或不可靠；bit6 personality 設定處於未定狀態。bit7 保留。</p>
</li>
<li id="q-196-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先找出設為 1 的 bits，再讀對應欄位與事件資訊。例如 bit1 必須核對上、下溫度門檻，不能一律翻成過熱。</p>
</li>
<li id="q-196-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功讀取回傳目前狀態；多個 bits 為 1 不代表 Log 格式錯誤。</p>
</li>
<li id="q-196-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Namespace Write Protection 造成的唯讀不得設定 AMRO；備援不存在時，也不能把無效 VMBF 當作故障證據。</p>
</li>
<li id="q-196-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-196-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-196-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-196-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-196-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-196-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-196-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-196-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-196-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>用警告類型、相應數值及 AER 發生時間互相核對，而不是要求稍後讀到的 CW 永遠等於事件當時。</p>
</li>
<li id="q-196-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查 bit 定義是否沿用舊版，漏掉 Base 2.4 的 personality 警告。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-197" data-question="197"><h2><a class="qa-qid" href="#q-197">Q197</a> Available Spare、Threshold 與 Percentage Used 如何解讀？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-197-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-197-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>三個值分別回答「剩多少備援」、「何時警告」與「估計壽命用了多少」，不能拿同一個百分比公式套用。</p>
</li>
<li id="q-197-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>SMART 描述所定義的整體健康範圍；它不是 namespace 的剩餘檔案空間。</p>
</li>
<li id="q-197-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀 AVSP、AVSPT、PUSED 及 CW.ASCBT；需要分組健康時另查 Endurance Group Log。</p>
</li>
<li id="q-197-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>AVSP 與 AVSPT 為 0～100%；AVSP&lt;AVSPT 才是低於門檻。PUSED 是廠商估算，100 不代表當下必然故障，且允許超過 100；大於 254 表示為 255。</p>
</li>
<li id="q-197-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>例如 AVSP=8、AVSPT=10 表示已低於門檻；PUSED=105 則表示估計耐用額度已用超過，兩者可以同時存在。</p>
</li>
<li id="q-197-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功讀取取得估計值；PUSED 在非睡眠期間每個 power-on hour 更新一次，不要求每次 Write 立即改變。</p>
</li>
<li id="q-197-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不能因 PUSED&gt;100 判為非法欄位，也不能因 AVSP=AVSPT 就要求「低於」警告。</p>
</li>
<li id="q-197-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-197-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-197-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-197-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-197-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-197-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-197-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-197-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-197-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>交叉比較警告與 AVSP，而不要用 PUSED 直接推算剩餘 spare。</p>
</li>
<li id="q-197-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認讀者是否把 Percentage Used 誤當成使用者容量使用率。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-198" data-question="198"><h2><a class="qa-qid" href="#q-198">Q198</a> 資料量、命令數、Busy Time、Power Cycles 與 Power On Hours 如何累計？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-198-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-198-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這些計數用不同單位描述工作量與使用時間；先理解單位，才能比較兩次快照。</p>
</li>
<li id="q-198-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>計數涵蓋 SMART 定義的範圍；多條 queue 的重疊工作時間不能直接相加成 Busy Time。</p>
</li>
<li id="q-198-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀 DUR、DUW、HRC、HWC、CBT、PWR_CYC 與 POH，並保留快照時間。</p>
</li>
<li id="q-198-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Data Units 以 1000 個 512-byte units 為單位並向上取整，0 表示未回報。Busy Time 以分鐘計，從 I/O 提交 Doorbell 到 CQE 寫入之間有未完成 I/O 即可能計入；不是等 Host 消費 CQE 才結束。</p>
</li>
<li id="q-198-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>以兩次快照算差，再依單位轉換。Host Read／Write Commands 依命令集定義的已完成命令類別累計；POH 可不含非工作狀態的時間。</p>
</li>
<li id="q-198-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例如資料量欄增加 2，只支持增加約 2×512000 bytes 的量化刻度；短小操作可能因取整而未立即增加。</p>
</li>
<li id="q-198-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不能用應用程式 I/O 次數要求 Host Command 計數完全相等，因為合併、重試與命令類型可能不同。</p>
</li>
<li id="q-198-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-198-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-198-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-198-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-198-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-198-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-198-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-198-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-198-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>核對 controller 真正完成的命令與計數單位，而不是只比檔案大小或壁鐘時間。</p>
</li>
<li id="q-198-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否漏掉 ×1000、512 bytes、分鐘與小時之間的換算。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-199" data-question="199"><h2><a class="qa-qid" href="#q-199">Q199</a> Unexpected Power Losses、媒體錯誤與 Error Log Entries 如何累計？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-199-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-199-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這三項分別記錄失電條件、無法恢復的資料完整性錯誤與已產生的 Error Log entries，不能互相代替。</p>
</li>
<li id="q-199-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>它們是生命週期累計，不是目前 Log 裡仍保留多少筆紀錄。</p>
</li>
<li id="q-199-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀 UPL、MDIE、NEILE，並保存失電前 CSTS.SHST 與是否因 OOB 管理而繼續存取媒體。</p>
</li>
<li id="q-199-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Base 2.4 將舊稱 Unsafe Shutdowns 的欄位稱為 Unexpected Power Losses。主電源失去時，SHST 不是 10b，或媒體因適用的 OOB Ignore Shutdown 操作尚未關閉，才符合規定的累計條件。</p>
</li>
<li id="q-199-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先辨認是否真的失去主電源，再判斷當時狀態；另外以未恢復的完整性錯誤核對 MDIE，以實際新增 Error entry 核對 NEILE。</p>
</li>
<li id="q-199-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Reset 而未失電不增加 UPL；完成 Abrupt Shutdown 且符合可斷電狀態後失電，也不能只因「Abrupt」就要求增加。</p>
</li>
<li id="q-199-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>一次命令失敗不必然同時增加 MDIE 與 NEILE。Write Uncorrectable 引入的錯誤是否計入 MDIE，規範允許實作選擇。</p>
</li>
<li id="q-199-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-199-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-199-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-199-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-199-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-199-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-199-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-199-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-199-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Error entries 被覆寫或重設後建議清除，不會讓生命週期 NEILE 倒退。</p>
</li>
<li id="q-199-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查測試到底執行 Shutdown、Reset，還是真的切斷主電源。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-200" data-question="200"><h2><a class="qa-qid" href="#q-200">Q200</a> Warning 與 Critical Composite Temperature Time 如何累計？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-200-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-200-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這兩欄描述處於警告或危急溫度區間的累計時間，不是 HCTM 降速次數。</p>
</li>
<li id="q-200-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>在工作狀態中，依 Composite Temperature 與 WCTEMP、CCTEMP 判斷，單位為分鐘。</p>
</li>
<li id="q-200-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀 Identify.WCTEMP、CCTEMP 與 SMART 的 WCTT、CCTT，並確認適用的溫度遲滯設定。</p>
</li>
<li id="q-200-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>WCTT 對應 WCTEMP≤溫度&lt;CCTEMP 的警告區間；CCTT 對應溫度≥CCTEMP。門檻未實作的零值有指定的零回報規則。</p>
</li>
<li id="q-200-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>按時間序列確認每段工作狀態及溫度區間，再累計；不要把取樣到一次高溫直接算成一整分鐘。</p>
</li>
<li id="q-200-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>假設持續 2 分鐘處於危急區間，應檢查 CCTT 的變化；不能同時要求這 2 分鐘全部加進警告區間。</p>
</li>
<li id="q-200-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>WCTEMP 或 CCTEMP 為 0 時，WCTT 為 0；CCTEMP 為 0 時，CCTT 為 0。零值不能一律解釋為裝置從未過熱。</p>
</li>
<li id="q-200-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-200-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-200-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-200-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-200-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-200-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-200-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-200-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-200-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>另把 HCTM 的累計秒數分開比較，因為門檻、單位與事件意義都不同。</p>
</li>
<li id="q-200-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查比較的是溫度區間時間，還是 HCTM 動作時間。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-201" data-question="201"><h2><a class="qa-qid" href="#q-201">Q201</a> 多個 Temperature Sensor 與 Composite Temperature 如何比較？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-201-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-201-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>多個 sensor 可觀察不同位置；Composite Temperature 是 controller 用於整體判斷的值，不保證等於其中最高、最低或平均值。</p>
</li>
<li id="q-201-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>sensor 位置與 Composite 的計算方式由實作定義；跨產品比較前需知道量測意義。</p>
</li>
<li id="q-201-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀 SMART.CTEMP 與 TSEN1～TSEN8，再查看裝置提供的 sensor 對應說明。</p>
</li>
<li id="q-201-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>數值以 Kelvin 表示；TSEN=0 表示未實作，不能當成 0 K 的有效溫度。</p>
</li>
<li id="q-201-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先排除未實作欄位，再轉換成需要的單位；例如 300 K 約為 26.85°C。警告門檻要搭配它所選的 sensor。</p>
</li>
<li id="q-201-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Get Log 成功可回傳彼此不同的溫度，差異本身不代表資料損壞。</p>
</li>
<li id="q-201-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不能要求所有 TSEN 都非零，也不能因 Composite 不等於平均值就判定違規。</p>
</li>
<li id="q-201-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-201-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-201-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-201-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-201-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-201-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-201-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-201-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-201-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>把警告、門檻所選 sensor 與該 sensor 的數值一起比對。</p>
</li>
<li id="q-201-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否將 0 當有效量測，以及是否選錯警告對應的 sensor。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-202" data-question="202"><h2><a class="qa-qid" href="#q-202">Q202</a> 哪些 Health 變化會產生 AER？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-202-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-202-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>健康通知讓 Host 不必持續輪詢，但它仍受支援、啟用及事件遮蔽條件限制。</p>
</li>
<li id="q-202-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>SMART／Health 事件報告規範定義的警告，不是每次溫度或計數變動都發通知。</p>
</li>
<li id="q-202-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 AEC.SHCW、SMART.CW、待處理 AER 數量，以及相關溫度或 spare 門檻。</p>
</li>
<li id="q-202-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>事件類型與資訊指向相應健康條件，LID 通常指向 SMART；Host 依實際 AER 回覆的 LID 讀取資料。</p>
</li>
<li id="q-202-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先掛入 AER，再啟用需要的通知；事件發生後保存 CQE，讀對應 Log 並依 RAE 完成確認，再補送 AER。</p>
</li>
<li id="q-202-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>符合通知條件且有可完成的 AER 時，Host 能取得事件；稍後 CW 已恢復不代表先前通知錯誤。</p>
</li>
<li id="q-202-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>沒有 AER Completion 時，不能直接判定韌體漏報；未啟用、已遮蔽或尚無可用 request 都要先查。</p>
</li>
<li id="q-202-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-202-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>本題討論的就是 SMART／Health AER；事件條件、SHCW、遮蔽狀態及 outstanding request 必須一起判斷。普通計數增加不要求另外發送事件。</p>
</li>
<li id="q-202-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-202-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-202-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-202-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-202-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-202-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-202-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>以事件當時設定與條件核對，不只看事後單一 SMART 快照。</p>
</li>
<li id="q-202-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認 SHCW 對應 bit 已啟用，且前一次同類事件已按規定確認。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-203" data-question="203"><h2><a class="qa-qid" href="#q-203">Q203</a> SMART 資料的 Scope 如何判斷？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-203-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-203-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Scope 決定同一組健康數字描述哪個範圍，避免把總體資料當成指定 namespace 的獨立健康。</p>
</li>
<li id="q-203-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Base 2.4 的 SMART／Health Log 不提供 namespace-specific 資訊；接受不同 NSID 不表示資料因此成為該 namespace 專屬。</p>
</li>
<li id="q-203-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查本版 SMART 定義與 Get Log Page 的選擇規則；需要 Endurance Group 資料時改查相應 Log。</p>
</li>
<li id="q-203-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Get Log Page 的 NSID 與 LID 仍須正確填寫，但每個回傳欄位的實際範圍由定義決定。</p>
</li>
<li id="q-203-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先記錄查詢的 controller 與 NSID，再比較回覆。對不同 NSID 回傳相同 SMART 資料，是本版定義允許且要求理解的行為。</p>
</li>
<li id="q-203-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功讀取取得整體資訊，不能據此分攤哪個 namespace 消耗多少壽命。</p>
</li>
<li id="q-203-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不能沿用舊版 namespace-specific SMART 的理解，要求每個 namespace 有不同計數。</p>
</li>
<li id="q-203-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-203-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-203-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-203-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-203-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-203-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-203-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-203-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-203-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>把 Identify 版本、Log 定義與實際回覆一起核對，避免只憑舊工具標籤判斷。</p>
</li>
<li id="q-203-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否把合法 NSID 的接受能力誤當成 per-namespace 計數能力。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-204" data-question="204"><h2><a class="qa-qid" href="#q-204">Q204</a> SMART、實際操作、Error Log 與 PEL 如何交叉驗證？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-204-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-204-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>交叉比對要建立合理關係，而不是要求所有資料來源每次都增加一筆。</p>
</li>
<li id="q-204-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>先固定 controller、操作時間區間與各資料的 scope；不同時間或不同物件不能直接相減。</p>
</li>
<li id="q-204-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>保存支援能力、SMART 前後快照、CQE、Error entries 與可用的 PEL context。</p>
</li>
<li id="q-204-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>用 SQID／CID 對回命令，以 Error Count 區分紀錄，以 PEL Event Type 與事件資料確認操作；SMART 則依單位與累計條件解讀。</p>
</li>
<li id="q-204-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先預測這個操作應改變哪些資料，再執行一次可隔離的情境，最後比較每一條預期關係。</p>
</li>
<li id="q-204-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例如一次正常讀取可增加 Read Commands 與資料量，卻不要求新增 Error entry 或 PEL 命令紀錄。</p>
</li>
<li id="q-204-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>缺少非必要紀錄不能算違規；若 More=1 卻找不到補充資訊，則須進一步檢查覆寫、讀取時序與記錄規則。</p>
</li>
<li id="q-204-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-204-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。 <a class="qa-rule-link" href="#common-log_query-9">本冊完整規則</a></p>
</li>
<li id="q-204-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Log Page 回傳指定 Log 的資料。 <a class="qa-rule-link" href="#common-log_query-10">本冊完整規則</a></p>
</li>
<li id="q-204-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。 <a class="qa-rule-link" href="#common-log_query-11">本冊完整規則</a></p>
</li>
<li id="q-204-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。 <a class="qa-rule-link" href="#common-log_query-12">本冊完整規則</a></p>
</li>
<li id="q-204-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。 <a class="qa-rule-link" href="#common-log_query-13">本冊完整規則</a></p>
</li>
<li id="q-204-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新提交查詢。 <a class="qa-rule-link" href="#common-log_query-14">本冊完整規則</a></p>
</li>
<li id="q-204-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。 <a class="qa-rule-link" href="#common-log_query-15">本冊完整規則</a></p>
</li>
<li id="q-204-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>結論分成「規範要求已滿足」、「明確不符」與「證據不足」，不要把無法觀察寫成已證明失敗。</p>
</li>
<li id="q-204-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查每個被期待改變的欄位，是否真的由這個操作觸發。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-command-8"><h3>命令完成、事件與紀錄 · DNR 與 More 應如何設定？</h3><p>只有收到 CQE，才有 DNR 與 More 可供判讀。DNR=1 表示相同命令即使重送到此 NVM subsystem 的任一 controller，仍預期會失敗；DNR=0 則只表示可能成功。除非個別錯誤條件另有明定，不能只看 Status 名稱就要求 DNR=1。More=1 表示 Error Information Log 有這筆命令的補充資訊。SCT=SC=0 時，DNR 應為 0。</p></article>
<article id="common-feature-12"><h3>Feature 的重設與影響範圍 · Controller Reset 後是否保留或繼續？</h3><p>先確認 Feature 的作用範圍及保存能力。如果重設影響整個 NVM subsystem，可保存 Feature 的 Current 會恢復為 Saved；沒有 Saved 時，則使用 Default。不可保存且不具持續性的 Feature 回到 Default。若多個 controller 中只有部分受到重設，共用設定則依 Figure 127 判斷是否保留。個別 Feature 的明確例外，優先於這些一般規則。</p></article>
<article id="common-feature-13"><h3>Feature 的重設與影響範圍 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>判斷恢復方式時，不能只看 Reset 名稱，還要確認它實際涵蓋哪些物件。重設影響整個 NVM subsystem 時，使用 Figure 126；multi-domain 配置中只有部分範圍受影響時，使用 Figure 127。若 Feature 雖不可保存，卻明定具有持續性，就仍須保留，不能誤解為重設後一律清零。</p></article>
<article id="common-feature-14"><h3>Feature 的重設與影響範圍 · Power Cycle 後是否保留或繼續？</h3><p>可保存的 Feature 若以 SV=1 成功更新 Saved，Power Cycle 後便依 Saved 恢復；SV=0 則不會改變 Saved。對不可保存的 Feature，另查 Figure 466 的持續性規則及個別例外。恢復後仍要讀取 Current 並驗證行為，不能只因 Saved 存在，就假設 controller 已正在使用它。</p></article>
<article id="common-feature-15"><h3>Feature 的重設與影響範圍 · 是否影響其他 Controller 或 Namespace？</h3><p>其他 controller 或 namespace 是否受影響，由 Feature 的作用範圍決定。controller scope 通常只控制目標 controller；namespace、NVM Set 或 NVM subsystem 的設定，則可能由多個 controller 共同觀察。多個 Host 修改共用設定時需要協調，也不能將 NSID=FFFFFFFFh 當成所有 Feature 都適用的廣播方式。</p></article>
<article id="common-log_query-9"><h3>本主題的共用條件 · 是否產生 Asynchronous Event？</h3><p>讀取 Log 本身不是新增一個事件的理由；不過，RAE=0 的成功讀取可能確認並清除對應事件。RAE=1 保留事件，讀取失敗也必須保留。Immediate 與 One-Shot 事件另有清除方式，不能全部套用讀 Log 確認。</p></article>
<article id="common-log_query-10"><h3>本主題的共用條件 · 是否更新 Error Information Log 或其他 Log？</h3><p>Get Log Page 回傳指定 Log 的資料。某些清單會因讀取而清除已回報的變更，某些事件也受 RAE 影響；讀取前先保存需要比對的狀態。讀取成功本身不要求新增 Error Information，失敗時則依 CQE 與錯誤記錄規則判斷。</p></article>
<article id="common-log_query-11"><h3>本主題的共用條件 · 是否記錄於 Persistent Event Log？</h3><p>Get Log Page 不是 PEL 中逐筆記錄的讀取歷史。即使讀取的是 PEL，也不表示這次讀取會新增同類事件；只有另行發生且符合支援與記錄條件的事件，才依規則記錄。</p></article>
<article id="common-log_query-12"><h3>本主題的共用條件 · Controller Reset 後是否保留或繼續？</h3><p>Controller Reset 會中止未完成的查詢，Host 恢復 Admin Queue 後重新讀取。Log 內容是否保留則是另一個問題：Error Information entries 建議清除，但 Error Count 保留；SMART 的累計資訊與 PEL 依各欄位規則持續，不能隨查詢一起當成遺失。</p></article>
<article id="common-log_query-13"><h3>本主題的共用條件 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>NVM Subsystem Reset 後，先恢復受影響 controller 的查詢通道，再讀取 Log。它不等於恢復出廠設定；Figure 209 的 Restore to Default Content 欄描述製造預設內容的恢復，不能拿來當一般 Reset 的保留表。</p></article>
<article id="common-log_query-14"><h3>本主題的共用條件 · Power Cycle 後是否保留或繼續？</h3><p>Power Cycle 後重新提交查詢。SMART 的生命週期資訊及 PEL 具有跨斷電的保留規則；Error Information entries 則建議清除，但其累計 Error Count 仍保留。目前溫度、正在執行的操作及回報 context 必須依各自定義重新判讀，不能把所有 bytes 當成固定不變。</p></article>
<article id="common-log_query-15"><h3>本主題的共用條件 · 是否影響其他 Controller 或 Namespace？</h3><p>查詢不會改寫 namespace 的使用者資料，但某些 Log 的讀取會確認事件或清除已回報清單。controller、namespace、domain 與 subsystem 的資料範圍也不同；多個 Host 共同查詢時，應記錄由誰讀取及何時確認，避免誤以為另一端沒有發生事件。</p></article>
<article id="common-power_config-9"><h3>本主題的共用條件 · 是否產生 Asynchronous Event？</h3><p>切換 Power State 或開始降速，不會自動產生同名的 AER。若溫度另外達到已設定的警告條件，才依 SMART／Health 事件與通知設定回報；HCTM 的 TMT1、TMT2 不是 Temperature Threshold Feature 的同一組門檻。</p></article>
<article id="common-power_config-10"><h3>本主題的共用條件 · 是否更新 Error Information Log 或其他 Log？</h3><p>SMART 的 Thermal Management transition count 與累計時間可協助確認 HCTM 行為；一般 Power State 切換沒有逐次記錄的標準 Log。成功設定不要求 Error Information entry，設定失敗時才依 CQE 與記錄條件查證。</p></article>
<article id="common-power_config-11"><h3>本主題的共用條件 · 是否記錄於 Persistent Event Log？</h3><p>若支援 PEL 的 Set Feature Event，先確認該 FID 可記錄且已宣告支援。符合條件的設定變更依規則記錄；自動進入 Power State 或每次降速，不等於又執行一次 Set Features。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>文件頁 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>文件頁 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-smart"><strong>Base 2.4 · §5.2.13.1.3</strong><br>文件頁 220–225 · PDF 246–251 · Figure 213–214</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-psd"><strong>Base 2.4 · §5.2.14.2.1 (Power State Descriptor)</strong><br>文件頁 384–387 · PDF 410–413 · Figure 340–341</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>文件頁 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-power"><strong>Base 2.4 · §5.2.30.1.2, 5.2.30.1.7</strong><br>文件頁 460–462, 468–469 · PDF 486–488, 494–495 · Figure 468–469, 475–478</li>
<li id="ref-aec"><strong>Base 2.4 · §5.2.30.1.6</strong><br>文件頁 466–468 · PDF 492–494 · Figure 474</li>
<li id="ref-thermal"><strong>Base 2.4 · §5.2.30.1.10</strong><br>文件頁 471–472 · PDF 497–498 · Figure 482</li>
<li id="ref-powerdetail"><strong>Base 2.4 · §8.1.19.1–8.1.19.5</strong><br>文件頁 666–671 · PDF 692–697 · Figure 738–741</li>
</ul><h3>需要看欄位圖時</h3><p>以下連結可開啟對應的圖表教學，查閱欄位及判讀方式。每張圖保留固定的教學位置，方便之後反覆查詢。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/health/en/">English</a><a href="/DOCS/nvme-question-bank/health.html">繁中教學 HTML</a></nav>
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
