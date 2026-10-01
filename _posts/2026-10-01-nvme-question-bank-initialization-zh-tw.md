---
layout: post
title: "NVMe 自問自答題庫：Controller 初始化與停用"
date: 2026-10-01 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/initialization/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/initialization/en/">English</a><a href="/DOCS/nvme-question-bank/initialization.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–68</p>
<header><p class="qa-range">Q1–Q9</p><h1>Controller 初始化與停用</h1><p class="qr-intro">先把 controller 的狀態轉移看懂，再處理命令。讀到能力不代表已啟用；設下 EN 不代表已 Ready；RDY=1 也不一定代表所有媒體存取都已就緒。這一冊用時間、狀態與可執行的動作來核對初始化。</p><p>先練習，再展開每題的 17 項解答。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可以指定的一份邏輯儲存空間。多個 controller 可以屬於同一 NVM subsystem（包含 controller 與非揮發儲存資源的整體）。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue 是提交佇列，Completion Queue 是完成佇列；SQE／CQE 是其中的一筆 entry。QID 識別 queue，CID 識別同一 SQ 內尚未完成的命令，NSID 識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 是可存取的控制或狀態欄位；Identify 查物件能力與屬性；Feature 查／設工作設定；Log Page 回報指定種類的狀態或紀錄。FID、LID、CNS、CSI 分別選 Feature、Log、Identify 結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 是第幾筆，通常由 0 起算；offset 是離起點多遠，要看單位。zero-based 數量欄位的實際數量＝編碼＋1，但不是每個寫 0 的欄位都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 指一項操作影響的物件範圍。retention 是狀態是否保留。Controller Reset（清 CC.EN）是一種 Controller Level Reset，簡稱 CLR；同一類 CLR 的不同觸發方式，Register 保留規則仍可能不同。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>從未啟用到能送命令</h2><p class="qa-takeaway">先等前一輪停完，再設定下一輪；兩次等待都要看 RDY，不能只看自己寫入的 EN。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">階段</th><th scope="col">觀察／動作</th><th scope="col">下一步的條件</th></tr></thead><tbody><tr><td>停用完成</td><td>CC.EN=0；CSTS.RDY=0</td><td>設定 AQA、ASQ、ACQ 與 CC</td></tr><tr><td>啟用中</td><td>EN 0→1，開始計時</td><td>等 RDY=1；檢查 CFS 與適用 timeout</td></tr><tr><td>介面就緒</td><td>RDY=1；依 Ready Mode 判斷媒體限制</td><td>先送合法 Admin 命令，再建立 I/O queue</td></tr><tr><td>再次停用</td><td>EN 1→0；不再新增提交</td><td>等 RDY=0，才開始下一輪</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>假設 CAP.TO=4，停用等待上限的單位換算是 4×500 ms=2 s。這不是每筆 I/O 命令的 timeout。啟用則還須依 CAP.CRMS 與所選模式檢查 CRTO，不能把這個 2 s 套到所有情況。</p>
<p class="qa-citations">來源：<a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-adminreg">Base 2.4 §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</a> · <a href="#ref-crto">Base 2.4 §3.1.4 (CRTO)</a> · <a href="#ref-init">Base 2.4 §3.5.1</a> · <a href="#ref-ready">Base 2.4 §3.5.3–3.5.4</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-001">Q01 · Host 應如何從 CAP 與 VS 確認 NVMe 版本、最大 Queue 大小、Timeout、Doorbell 間距、Memory Page Size 及支援的 Command Set？</a></li>
<li><a href="#q-002">Q02 · AQA、ASQ、ACQ 與 CC 各欄位應按照什麼順序設定？設定錯誤時可能發生什麼？</a></li>
<li><a href="#q-003">Q03 · Host 設定 CC.EN 後，應如何根據 CAP.TO 與 CSTS.RDY 判斷 Controller 是否成功 Enable？</a></li>
<li><a href="#q-004">Q04 · Host 清除 CC.EN 後，應如何判斷 Controller 是否成功 Disable？尚未 Disable 完成時能否重新 Enable？</a></li>
<li><a href="#q-005">Q05 · Host 能否在 CSTS.RDY 為 0 時送出 Command 或更新 Doorbell？</a></li>
<li><a href="#q-006">Q06 · CSTS.CFS 代表什麼？Controller 初始化失敗或進入 Fatal 狀態時，Host 應如何恢復？</a></li>
<li><a href="#q-007">Q07 · Controller 初始化後可能進入哪些 Ready Mode？Host 應如何處理暫時或限制性的 Ready 狀態？</a></li>
<li><a href="#q-008">Q08 · Controller Enable、Disable、Controller Reset、NVM Subsystem Reset 與 Shutdown 有什麼差異？</a></li>
<li><a href="#q-009">Q09 · Controller Reset 後，哪些 Register、Admin Queue、Feature 與 I/O Queue 需要重新設定？</a></li>
</ol></section>
<article class="qa-question" id="q-001" data-question="1"><h2><a class="qa-qid" href="#q-001">Q01</a> Host 應如何從 CAP 與 VS 確認 NVMe 版本、最大 Queue 大小、Timeout、Doorbell 間距、Memory Page Size 及支援的 Command Set？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-001-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-001-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>在送命令以前，先知道介面允許的配置；CAP 是能力，CC 才是 Host 選擇。不要把能力位元直接複製成設定值。</p>
</li>
<li id="q-001-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>這次讀取只觀察目標 controller，不改變 queue 或媒體。版本號也不能代替逐項選配能力檢查。</p>
</li>
<li id="q-001-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>VS 的 MJR／MNR／TER 表示版本；CAP.MQES+1 是 I/O queue entry 上限，CQR 是實體連續要求，CSS 表示 command set 支援方式。</p>
</li>
<li id="q-001-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CAP.TO 單位為 500 ms；Doorbell stride=2^(2+DSTRD) bytes；支援頁面範圍為 2^(12+MPSMIN) 至 2^(12+MPSMAX) bytes。啟用逾時還要讀 CRTO。</p>
</li>
<li id="q-001-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先映射 NVMe Register，讀 VS、CAP，選合法 MPS／CSS／AMS／Ready Mode，再配置 queue。若 IOCSS=1，Enable 後用 Identify CNS 1Ch 探索組合。</p>
</li>
<li id="q-001-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>得到可用的配置範圍，不是 CQE。例：MQES=03FFh 表示最多 1024 slots；DSTRD=2 表示相鄰 Doorbell 間距 16 bytes。</p>
</li>
<li id="q-001-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>讀唯讀 Register 沒有 Invalid Field CQE。後續若把不支援值寫入 CC.MPS／AMS，規範可定義為 undefined behavior，不能要求固定錯誤碼。</p>
</li>
<li id="q-001-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>本次 MMIO 存取沒有 NVMe CQE，因此 DNR／More 不適用。 <a class="qa-rule-link" href="#common-register-8">本冊完整規則</a></p>
</li>
<li id="q-001-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Register 存取本身沒有成功事件；另有硬體錯誤時使用該事件的條件。 <a class="qa-rule-link" href="#common-register-9">本冊完整規則</a></p>
</li>
<li id="q-001-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>不逐次記錄 Register 讀寫；先保留 Register 值與時間，再取得可用的診斷紀錄。 <a class="qa-rule-link" href="#common-register-10">本冊完整規則</a></p>
</li>
<li id="q-001-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Register 存取不構成 PEL 事件；完成的 Reset 或支援的硬體錯誤另判斷。 <a class="qa-rule-link" href="#common-register-11">本冊完整規則</a></p>
</li>
<li id="q-001-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CAP／VS 是能力與版本 Register。Controller Reset 後重新讀它們，再重設 CC 的選擇；不要將唯讀能力當成需寫回的設定。</p>
</li>
<li id="q-001-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>NVM Subsystem Reset 後重新確認 Register 可存取及版本／能力，尤其重設同時啟用新韌體時。</p>
</li>
<li id="q-001-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新探索 CAP／VS；本次讀取沒有需要保存的 Host 設定。</p>
</li>
<li id="q-001-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>讀取不改變其他 controller 或 namespace；不同 controller 可以有不同能力，不能用一份快照代替全部。</p>
</li>
<li id="q-001-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>將 CAP.CSS 接到 CC.CSS 與 Identify 的 command-set 組合；將 MQES 接到 Create Queue 的 QSIZE。Admin Queue 的 4096-slot 上限另看 AQA，不把兩個上限混用。</p>
</li>
<li id="q-001-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查位元位置、little-endian 讀取及 zero-based 編碼；MQES=1023 不是只能放 1023 個實體 slots。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-crto">Base 2.4 §3.1.4 (CRTO)</a> · <a href="#ref-init">Base 2.4 §3.5.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-002" data-question="2"><h2><a class="qa-qid" href="#q-002">Q02</a> AQA、ASQ、ACQ 與 CC 各欄位應按照什麼順序設定？設定錯誤時可能發生什麼？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-002-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-002-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>讓 controller 在 Enable 時就能找到合法的 Admin SQ／CQ；先有記憶體和指標，再允許處理命令。</p>
</li>
<li id="q-002-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>影響此 controller 的管理介面。錯誤 queue 位址可能使所有後續 Identify、Get Features 都無法正常完成。</p>
</li>
<li id="q-002-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀 CAP 的 MPS 範圍、CSS、AMS、CRMS，並使用 AQA 的 Admin queue 長度限制。</p>
</li>
<li id="q-002-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>AQA.ASQS／ACQS 是 entries−1；ASQ／ACQ 是對齊 CC.MPS 的實體起始位址。CC 設 CSS、MPS、AMS、CRIME；NVM I/O 的 IOSQES=6、IOCQES=4。</p>
</li>
<li id="q-002-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>等待前次重設的 RDY=0；配置連續 Admin queue 記憶體，清 Admin CQ Phase；在 EN=0 時寫 AQA／ASQ／ACQ 與合法 CC 設定；設 EN=1 後等待 RDY=1。I/O entry size 必須在 Create I/O Queue 前設定。</p>
</li>
<li id="q-002-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Admin queue 可用，Host 可提交 Identify。這不表示 I/O queue 已自動建立，也不表示所有媒體在 independent mode 中已 ready。</p>
</li>
<li id="q-002-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>AQA size=0 後 Enable、EN=1 時改 MPS、不支援 MPS／AMS 等有 undefined 結果；不能替這些 Register 誤用指定 Invalid Field CQE。</p>
</li>
<li id="q-002-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>本次 MMIO 存取沒有 NVMe CQE，因此 DNR／More 不適用。 <a class="qa-rule-link" href="#common-register-8">本冊完整規則</a></p>
</li>
<li id="q-002-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Register 存取本身沒有成功事件；另有硬體錯誤時使用該事件的條件。 <a class="qa-rule-link" href="#common-register-9">本冊完整規則</a></p>
</li>
<li id="q-002-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>不逐次記錄 Register 讀寫；先保留 Register 值與時間，再取得可用的診斷紀錄。 <a class="qa-rule-link" href="#common-register-10">本冊完整規則</a></p>
</li>
<li id="q-002-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Register 存取不構成 PEL 事件；完成的 Reset 或支援的硬體錯誤另判斷。 <a class="qa-rule-link" href="#common-register-11">本冊完整規則</a></p>
</li>
<li id="q-002-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-002-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-002-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-002-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-002-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>先驗 Register 編碼，再驗 Admin CQ 可收到正確 CID 的 Identify 回覆；只看到 CC.EN=1 不足以證明初始化完成。</p>
</li>
<li id="q-002-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查 ASQ／ACQ 是裝置可使用的位址、頁面對齊與配置長度；不要拿一般程式的虛擬位址直接當 queue base。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-adminreg">Base 2.4 §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-init">Base 2.4 §3.5.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-003" data-question="3"><h2><a class="qa-qid" href="#q-003">Q03</a> Host 設定 CC.EN 後，應如何根據 CAP.TO 與 CSTS.RDY 判斷 Controller 是否成功 Enable？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-003-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-003-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>區分「要求啟用」與「已可處理命令」，並避免 Host 用錯逾時而過早重設。Base 2.4 需要把 CRTO 納入判斷。</p>
</li>
<li id="q-003-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>判斷目標 controller 的啟用；媒體是否可用還取決於 Ready Mode。</p>
</li>
<li id="q-003-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀 CAP.CRMS、CC.CRIME、CRTO.CRWMT／CRIMT 與 CAP.TO；不可只假設 CAP.TO 足以表示所有 Enable 等待時間。</p>
</li>
<li id="q-003-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CC.EN 由 0→1 是計時起點；CSTS.RDY 是觀察值。CRTO 單位為 500 ms：With Media 用 CRWMT，Independent 用 CRIMT 判 RDY，再以 CRWMT 判媒體期限。</p>
</li>
<li id="q-003-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>記錄模式與啟用時間，poll RDY／CFS；RDY=1 後按該模式送合法命令。初始化失败處理另有要求，不可把每個 RDY=1 都解讀成媒體健康。</p>
</li>
<li id="q-003-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>正常情況在適用期限內 RDY=1。例：CRIMT=2、CRWMT=20，分別是 1 s 的介面就緒期限與 10 s 的媒體期限，兩者都從 Enable 起算。</p>
</li>
<li id="q-003-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Register 啟用沒有 CQE。媒體尚未 ready 時，僅符合條件的命令可回 Namespace Not Ready（SCT=0, SC=82h）或 Admin Command Media Not Ready（0/24h）。</p>
</li>
<li id="q-003-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>Register 啟用本身無 DNR／More。Independent mode 合法等待期間的媒體未就緒回覆允許 DNR=0；超過 CRWMT 不得繼續用同一暫時性理由回報 DNR=0。More 依有無 Error Information 補充資訊設定。</p>
</li>
<li id="q-003-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Register 存取本身沒有成功事件；另有硬體錯誤時使用該事件的條件。 <a class="qa-rule-link" href="#common-register-9">本冊完整規則</a></p>
</li>
<li id="q-003-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>不逐次記錄 Register 讀寫；先保留 Register 值與時間，再取得可用的診斷紀錄。 <a class="qa-rule-link" href="#common-register-10">本冊完整規則</a></p>
</li>
<li id="q-003-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>符合 §3.5.4.1 的初始化期限失敗時，若支援 PEL，須記錄 NVM Subsystem Hardware Error Event，錯誤原因為 Controller Ready Timeout Exceeded。這不是每次成功 Enable 都記一筆。</p>
</li>
<li id="q-003-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-003-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-003-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-003-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-003-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>把時間軸、CRIME、命令種類與回傳 Status 一起核對。Figure 84 列出的 Admin 命令及限制，不能擴張成所有 Admin 都可暫時拒絕。</p>
</li>
<li id="q-003-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查用了哪個 timeout、起算點與 500 ms 單位；不要在 RDY=1 時把媒體等待時間重新從零計算。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-crto">Base 2.4 §3.1.4 (CRTO)</a> · <a href="#ref-ready">Base 2.4 §3.5.3–3.5.4</a> · <a href="#ref-init">Base 2.4 §3.5.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-004" data-question="4"><h2><a class="qa-qid" href="#q-004">Q04</a> Host 清除 CC.EN 後，應如何判斷 Controller 是否成功 Disable？尚未 Disable 完成時能否重新 Enable？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-004-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-004-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>確保舊命令處理已停止，才能安全開始下一輪 controller 初始化。</p>
</li>
<li id="q-004-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>清 EN 觸發此 controller 的重設，包括所有 I/O queue；不是只暫停一條 SQ。</p>
</li>
<li id="q-004-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>CAP.TO 定義清 EN 後等待 RDY 由 1→0 的最壞等待時間；同時保留 CC／CSTS 快照。</p>
</li>
<li id="q-004-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>只在已啟用且 RDY=1 的正常條件下啟動 EN 1→0；觀察 RDY=0 才代表 controller 已可重新 Enable。</p>
</li>
<li id="q-004-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>停止新增提交，清 EN，poll RDY；等 RDY=0 後重整 Admin CQ 與 Host 追蹤，設定 CC，再設 EN。</p>
</li>
<li id="q-004-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功停用的證據是 RDY=0，不是收齊每一筆舊命令 CQE。舊 I/O queue 已失效。</p>
</li>
<li id="q-004-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>在 RDY 仍為 1 時把 EN 由 0→1，結果 undefined。不是規範要求回 Command Sequence Error 的 Admin 命令錯誤。</p>
</li>
<li id="q-004-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>本次 MMIO 存取沒有 NVMe CQE，因此 DNR／More 不適用。 <a class="qa-rule-link" href="#common-register-8">本冊完整規則</a></p>
</li>
<li id="q-004-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Register 存取本身沒有成功事件；另有硬體錯誤時使用該事件的條件。 <a class="qa-rule-link" href="#common-register-9">本冊完整規則</a></p>
</li>
<li id="q-004-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>不逐次記錄 Register 讀寫；先保留 Register 值與時間，再取得可用的診斷紀錄。 <a class="qa-rule-link" href="#common-register-10">本冊完整規則</a></p>
</li>
<li id="q-004-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Register 存取不構成 PEL 事件；完成的 Reset 或支援的硬體錯誤另判斷。 <a class="qa-rule-link" href="#common-register-11">本冊完整規則</a></p>
</li>
<li id="q-004-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-004-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-004-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-004-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-004-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>核對 EN／RDY 轉移及舊 queue 不再被使用；不能用舊 queue 上偶然看見的資料證明它可繼續工作。</p>
</li>
<li id="q-004-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先看是不是清 EN 後立刻設回 1，或把 CAP.TO 當成毫秒值直接使用。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-005" data-question="5"><h2><a class="qa-qid" href="#q-005">Q05</a> Host 能否在 CSTS.RDY 為 0 時送出 Command 或更新 Doorbell？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-005-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-005-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>將「在 Host 記憶體準備 SQE」與「正式提交命令」分開；Doorbell 是提交邊界，不能提早使用。</p>
</li>
<li id="q-005-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>適用此 PCIe controller 的 Admin 及 I/O 提交；先配置 Admin queue Register 是初始化的一部分，與送命令不同。</p>
</li>
<li id="q-005-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>用 CSTS.RDY、CC.EN 及該 queue 是否存在判斷。RDY=1 仍須確認 queue 已建立及 shutdown 狀態。</p>
</li>
<li id="q-005-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>SQ Tail Doorbell 通知新命令；CQ Head Doorbell 通知已消費完成。它們不是讓 controller 變 ready 的命令。</p>
</li>
<li id="q-005-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>等待 RDY=1，確認 queue 的有效生命週期，先讓 SQE 對裝置可見，再更新 SQ Tail。</p>
</li>
<li id="q-005-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>正確提交後 controller 才能取得命令；準備好記憶體但沒更新 Tail，還不能算命令已提交。</p>
</li>
<li id="q-005-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>違反 ready／queue 使用前提，不可期待固定 CQE；停用狀態本來就不能依賴 Admin Queue 回覆錯誤。</p>
</li>
<li id="q-005-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>本次 MMIO 存取沒有 NVMe CQE，因此 DNR／More 不適用。 <a class="qa-rule-link" href="#common-register-8">本冊完整規則</a></p>
</li>
<li id="q-005-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Register 存取本身沒有成功事件；另有硬體錯誤時使用該事件的條件。 <a class="qa-rule-link" href="#common-register-9">本冊完整規則</a></p>
</li>
<li id="q-005-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>不逐次記錄 Register 讀寫；先保留 Register 值與時間，再取得可用的診斷紀錄。 <a class="qa-rule-link" href="#common-register-10">本冊完整規則</a></p>
</li>
<li id="q-005-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Register 存取不構成 PEL 事件；完成的 Reset 或支援的硬體錯誤另判斷。 <a class="qa-rule-link" href="#common-register-11">本冊完整規則</a></p>
</li>
<li id="q-005-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-005-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-005-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-005-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-005-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>若看見 EN=1、RDY=0 與超時，先判初始化階段；不要把尚未合法提交的 Identify 當作裝置不支援 Identify。</p>
</li>
<li id="q-005-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先比對 Doorbell 寫入時間與 RDY 變成 1 的時間，再檢查 queue 建立成功時間。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-qattr">Base 2.4 §3.3.3–3.4.1</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-006" data-question="6"><h2><a class="qa-qid" href="#q-006">Q06</a> CSTS.CFS 代表什麼？Controller 初始化失敗或進入 Fatal 狀態時，Host 應如何恢復？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-006-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-006-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>CFS 通常表示嚴重 controller 狀態，與單一命令失敗不同。但若是 virtualization 的 secondary controller，進入 Offline 也會設定 CFS；先確認 controller 角色與 Online／Offline，不能直接宣判硬體故障。</p>
</li>
<li id="q-006-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>可能影響該 controller 整體命令服務。CFS 與某個 namespace 的媒體錯誤不能互相替代。</p>
</li>
<li id="q-006-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>CSTS.CFS 與 RDY、CC.EN、適用 timeout 一起觀察；沒有一個 Identify 選配位元能讓 Host 忽略 CFS。</p>
</li>
<li id="q-006-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>先保存 Register 與已取得的 CQE／Log；若管理路徑仍可用再取診斷，不能無限等待不可能回覆的 Get Log Page。</p>
</li>
<li id="q-006-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>依故障及控制介面可達性執行 Controller Level Reset，等待合法狀態轉移，再重新初始化。若控制介面無回應，交由平台恢復；不把所有故障都保證成一次 CC.EN 重設即可修好。</p>
</li>
<li id="q-006-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>恢復後需再次驗證 RDY、Identify 與新 queue 的命令完成；CFS 消失本身不是資料完整性驗證。</p>
</li>
<li id="q-006-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>若仍能完成受影響命令，Internal Error（SCT=0, SC=06h）可能適用；無法經 CQE 溝通的嚴重故障可能設定 CFS，不能要求每筆都留下 CQE。</p>
</li>
<li id="q-006-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>本次 MMIO 存取沒有 NVMe CQE，因此 DNR／More 不適用。 <a class="qa-rule-link" href="#common-register-8">本冊完整規則</a></p>
</li>
<li id="q-006-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Register 存取本身沒有成功事件；另有硬體錯誤時使用該事件的條件。 <a class="qa-rule-link" href="#common-register-9">本冊完整規則</a></p>
</li>
<li id="q-006-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>不逐次記錄 Register 讀寫；先保留 Register 值與時間，再取得可用的診斷紀錄。 <a class="qa-rule-link" href="#common-register-10">本冊完整規則</a></p>
</li>
<li id="q-006-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Register 存取不構成 PEL 事件；完成的 Reset 或支援的硬體錯誤另判斷。 <a class="qa-rule-link" href="#common-register-11">本冊完整規則</a></p>
</li>
<li id="q-006-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-006-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-006-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-006-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-006-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>把同一時間的 CFS、初始化期限與硬體錯誤紀錄核對；不要把一次命令 Invalid Field 升級解釋為 controller fatal。</p>
</li>
<li id="q-006-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認 Register 讀取仍有效，以及 CFS 真的是 1；不可將失效讀取的全 1 值直接解碼成每個狀態位都成立。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-ready">Base 2.4 §3.5.3–3.5.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-007" data-question="7"><h2><a class="qa-qid" href="#q-007">Q07</a> Controller 初始化後可能進入哪些 Ready Mode？Host 應如何處理暫時或限制性的 Ready 狀態？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-007-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-007-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>讓管理命令可以在媒體初始化尚未完成前開始，但仍有明確的媒體就緒期限。</p>
</li>
<li id="q-007-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>兩種模式是 Controller Ready With Media 與 Controller Ready Independent of Media；不是新增一組任意的 degraded-ready 編碼。</p>
</li>
<li id="q-007-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>CAP.CRMS.CRWMS／CRIMS 表示支援；CAP.CRMS=11b 時可用 CC.CRIME 選擇模式。</p>
</li>
<li id="q-007-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CRIME=0 選 With Media；CRIME=1 選 Independent。CSTS.RDY、CRTO.CRIMT／CRWMT 及 Figure 84 的命令分類共同決定當下可做什麼。</p>
</li>
<li id="q-007-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>在 Enable 前選模式。Independent 的 RDY=1 後先做不依賴媒體的探索，媒體命令依暫時性 Status 延後，並追蹤自 Enable 起的 CRWMT。</p>
</li>
<li id="q-007-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>With Media 正常完成時可處理所要求的媒體存取；Independent 的 RDY=1 只先滿足介面及適用命令就緒，不代表所有 namespace ready。</p>
</li>
<li id="q-007-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>符合條件時可回 0/82h 或 0/24h；0/24h 只限 Independent mode 的合適 Admin 命令。媒體期限後仍用 DNR=0 表示暫時等待，不符合該期限規則。</p>
</li>
<li id="q-007-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>本題的 Register 讀寫沒有 DNR／More；媒體未就緒的 CQE 則按條件處理。在允許等待期間可用 DNR=0，CRWMT 後不得繼續用同一暫時性理由；More 仍表示 Error Information 的額外資訊。</p>
</li>
<li id="q-007-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Register 存取本身沒有成功事件；另有硬體錯誤時使用該事件的條件。 <a class="qa-rule-link" href="#common-register-9">本冊完整規則</a></p>
</li>
<li id="q-007-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>不逐次記錄 Register 讀寫；先保留 Register 值與時間，再取得可用的診斷紀錄。 <a class="qa-rule-link" href="#common-register-10">本冊完整規則</a></p>
</li>
<li id="q-007-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>若符合 §3.5.4.1 的初始化失敗條件且支援 PEL，須記錄 Controller Ready Timeout Exceeded 的 NVM Subsystem Hardware Error Event。正常選擇某種 Ready Mode 本身不要求此錯誤事件。</p>
</li>
<li id="q-007-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-007-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-007-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-007-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-007-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>同時核對 CAP 宣告、CC 選擇、timeout 與命令行為。CSTS.PP 是另一種暫停處理指示，不是第三個 Ready Mode。</p>
</li>
<li id="q-007-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先問正在失敗的命令是否需要媒體，再看它是否真的屬 Figure 84 允許的種類。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-ready">Base 2.4 §3.5.3–3.5.4</a> · <a href="#ref-crto">Base 2.4 §3.1.4 (CRTO)</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-008" data-question="8"><h2><a class="qa-qid" href="#q-008">Q08</a> Controller Enable、Disable、Controller Reset、NVM Subsystem Reset 與 Shutdown 有什麼差異？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-008-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-008-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>分開「開始服務」「停止並重設」與「為移除電源做準備」，避免用 Reset 代替正常 Shutdown。</p>
</li>
<li id="q-008-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Enable／CC.EN 清除針對 controller；NVM Subsystem Reset 涵蓋規定的 subsystem／domain 範圍；Shutdown 另有 controller 與 subsystem 類型。</p>
</li>
<li id="q-008-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>CAP.NSSRS 確認 NSSR 支援；CAP 的 shutdown 能力與 CSTS.ST 區分 Shutdown 範圍。</p>
</li>
<li id="q-008-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Enable：EN 0→1。Controller Reset：EN 1→0。NSSR.NSSRC 寫 4E564D65h 觸發支援的 subsystem reset。正常 controller shutdown 用 CC.SHN=01b，觀察 CSTS.SHST=10b。</p>
</li>
<li id="q-008-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>正常移除電源前協調 I/O，再通知 Shutdown 並等待完成；故障恢復才選合適 Reset，之後重建操作環境。</p>
</li>
<li id="q-008-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Enable 看 RDY=1；Disable／Reset 完成看相應狀態；Shutdown 看 SHST=10b。Shutdown 完成不是所有 Register 都回到 reset value。</p>
</li>
<li id="q-008-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Register 操作沒有統一 CQE。Shutdown 中 controller 可對命令回 Commands Aborted due to Power Loss Notification（0/05h）；不能將此碼套用到所有 Reset 的未完成命令。</p>
</li>
<li id="q-008-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>本次 MMIO 存取沒有 NVMe CQE，因此 DNR／More 不適用。 <a class="qa-rule-link" href="#common-register-8">本冊完整規則</a></p>
</li>
<li id="q-008-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Register 存取本身沒有成功事件；另有硬體錯誤時使用該事件的條件。 <a class="qa-rule-link" href="#common-register-9">本冊完整規則</a></p>
</li>
<li id="q-008-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>不逐次記錄 Register 讀寫；先保留 Register 值與時間，再取得可用的診斷紀錄。 <a class="qa-rule-link" href="#common-register-10">本冊完整規則</a></p>
</li>
<li id="q-008-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Register 存取不構成 PEL 事件；完成的 Reset 或支援的硬體錯誤另判斷。 <a class="qa-rule-link" href="#common-register-11">本冊完整規則</a></p>
</li>
<li id="q-008-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-008-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-008-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-008-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-008-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>記錄觸發方法與 scope，再對照保留值；只在紀錄寫「reset」不足以解釋 AQA、PCIe 狀態與 Feature 為何不同。</p>
</li>
<li id="q-008-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先辨認到底寫了 EN、SHN 還是 NSSRC，以及是否有平台重設同時發生。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-shutdown">Base 2.4 §3.6.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-009" data-question="9"><h2><a class="qa-qid" href="#q-009">Q09</a> Controller Reset 後，哪些 Register、Admin Queue、Feature 與 I/O Queue 需要重新設定？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-009-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-009-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>建立新一輪有效操作環境，避免沿用上一輪 queue 指標、Phase 與尚未完成的命令。</p>
</li>
<li id="q-009-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>本題專指清 CC.EN 觸發的 Controller Reset；FLR、NVM Subsystem Reset 的 Register 保留規則不能混入。</p>
</li>
<li id="q-009-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>看 §3.7.2 的例外清單與個別 Register Reset 欄，Feature 再看 scope、saveable、Figure 126／127 與 466。</p>
</li>
<li id="q-009-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>AQA／ASQ／ACQ、指定 PMR Register、CMBMSC 在此重設中不清除；Admin queue 指標仍會 reset。I/O SQ／CQ 全部刪除，CC 選擇需重新配置。可保存 Feature 按重設範圍恢復 Saved（沒有 Saved 則 Default）；不可保存者另看持續性，HMB 需重新配置。</p>
</li>
<li id="q-009-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>等 RDY=0；確認保留的 Admin 記憶體仍有效，將 Admin CQ Phase 初始化成 0；配置並 Enable；重查必要能力、Feature，重新協商 Number of Queues，再建立 CQ→SQ。</p>
</li>
<li id="q-009-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>新命令在新 queue 生命週期正確完成。即使使用相同 QID／位址，也不能把它當成舊 queue 繼續。</p>
</li>
<li id="q-009-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>舊 CQE 沒有可要求的統一「Reset Status」；重建時的非法 QID／大小依 Create 命令判斷。對舊記憶體誤寫 Doorbell 不能期待正常恢復。</p>
</li>
<li id="q-009-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>本次 MMIO 存取沒有 NVMe CQE，因此 DNR／More 不適用。 <a class="qa-rule-link" href="#common-register-8">本冊完整規則</a></p>
</li>
<li id="q-009-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Register 存取本身沒有成功事件；另有硬體錯誤時使用該事件的條件。 <a class="qa-rule-link" href="#common-register-9">本冊完整規則</a></p>
</li>
<li id="q-009-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>不逐次記錄 Register 讀寫；先保留 Register 值與時間，再取得可用的診斷紀錄。 <a class="qa-rule-link" href="#common-register-10">本冊完整規則</a></p>
</li>
<li id="q-009-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Register 存取不構成 PEL 事件；完成的 Reset 或支援的硬體錯誤另判斷。 <a class="qa-rule-link" href="#common-register-11">本冊完整規則</a></p>
</li>
<li id="q-009-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-009-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-009-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-009-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-009-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>前後比對 Register、Get Features 與實際 Queue 能力。尤其 AQA 值保留與 Admin CQ 內容有效，是不同事情。</p>
</li>
<li id="q-009-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查 Host 是否清除舊 outstanding 對照與重新初始化 Phase；相同 CID 不應對到前一輪命令。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-adminreg">Base 2.4 §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-queue-12"><h3>Queue 的重設與影響範圍 · Controller Reset 後是否保留或繼續？</h3><p>清除 CC.EN 使 Controller Level Reset 執行：I/O SQ／CQ 被刪除，Admin Queue 的指標重設；AQA／ASQ／ACQ 在這種重設中保留不代表舊 CQE 仍有效。重新初始化 Admin CQ 的 Phase，Enable 後重新配置及建立 I/O Queue。</p></article>
<article id="common-queue-13"><h3>Queue 的重設與影響範圍 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>受 NVM Subsystem Reset 影響的 controller 執行 Controller Level Reset；舊 Queue 不能沿用。Host 應重新確認傳輸與 Register 狀態，再建立 Admin／I/O 操作環境，不套用 CC.EN 重設對 AQA 等 Register 的保留例外。</p></article>
<article id="common-queue-14"><h3>Queue 的重設與影響範圍 · Power Cycle 後是否保留或繼續？</h3><p>斷電後重新走初始化與 Queue 建立流程。主機記憶體中即使還有舊 SQE／CQE 位元，也不是新一輪 Queue 的有效命令或完成；Host 必須重建自己的指標、Phase 與 outstanding 對照。</p></article>
<article id="common-queue-15"><h3>Queue 的重設與影響範圍 · 是否影響其他 Controller 或 Namespace？</h3><p>Queue 屬於建立它的 controller，不因相同 QID 就和別的 controller 共用。共用 CQ 的多個 SQ 則有直接關係：CQ 空間不足或刪除順序會影響它們。Queue 重設不等於刪除 namespace 或撤銷已完成的資料寫入。</p></article>
<article id="common-register-8"><h3>Register 存取 · DNR 與 More 應如何設定？</h3><p>不適用於這次 Register 存取：它沒有 NVMe CQE，因此沒有可設定的 DNR／More。若之後的 Admin 或 I/O 命令失敗，才解讀那筆命令的 CQE。</p></article>
<article id="common-register-9"><h3>Register 存取 · 是否產生 Asynchronous Event？</h3><p>這次 Register 存取本身不定義一筆成功通知。若另發生 Internal Error 等已定義事件，使用該事件規則；Controller 還不能處理 Admin Queue 時，不能把等待事件當成初始化完成判斷。</p></article>
<article id="common-register-10"><h3>Register 存取 · 是否更新 Error Information Log 或其他 Log？</h3><p>不會因每次讀寫 Register 就要求建立 Error Information entry。初始化問題先保存 CAP、CC、CSTS、CRTO 與時間；若之後能讀 Log，再用事件及錯誤內容補足證據。</p></article>
<article id="common-register-11"><h3>Register 存取 · 是否記錄於 Persistent Event Log？</h3><p>一般 Register 存取不是獨立的 Persistent Event。若發生重設、電源或硬體錯誤，只有在支援 PEL 且符合對應事件條件時才要求記錄；不能將每次 CC 寫入都等同 Power-on or Reset 事件。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁＝PDF 頁−26；另兩份相同。以下依本次提供的 PDF 本文定位，保留 Figure 編號；共享頁只引用本題需要的定義，不納入 Fabrics 或 PCIe Link／封包內容。</p><ul class="qa-references">
<li id="ref-cap"><strong>Base 2.4 · §3.1.4 (CAP, VS)</strong><br>文件頁 54–59 · PDF 80–85 · Figure 36–37</li>
<li id="ref-cc"><strong>Base 2.4 · §3.1.4 (CC, CSTS, NSSR)</strong><br>文件頁 60–66 · PDF 86–92 · Figure 41–43</li>
<li id="ref-adminreg"><strong>Base 2.4 · §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</strong><br>文件頁 66–68 · PDF 92–94 · Figure 44–47</li>
<li id="ref-crto"><strong>Base 2.4 · §3.1.4 (CRTO)</strong><br>文件頁 72–73 · PDF 98–99 · Figure 57</li>
<li id="ref-queue"><strong>Base 2.4 · §3.3.1</strong><br>文件頁 88–91 · PDF 114–117 · Figure 73–74</li>
<li id="ref-qattr"><strong>Base 2.4 · §3.3.3–3.4.1</strong><br>文件頁 101 · PDF 127</li>
<li id="ref-init"><strong>Base 2.4 · §3.5.1</strong><br>文件頁 105–106 · PDF 131–132</li>
<li id="ref-ready"><strong>Base 2.4 · §3.5.3–3.5.4</strong><br>文件頁 109–113 · PDF 135–139 · Figure 84–85</li>
<li id="ref-shutdown"><strong>Base 2.4 · §3.6.1</strong><br>文件頁 114–115 · PDF 140–141</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>文件頁 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>文件頁 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-virtual"><strong>Base 2.4 · §8.2.7</strong><br>文件頁 754–759 · PDF 780–785 · Figure 796</li>
<li id="ref-fatal"><strong>Base 2.4 · §9.1–9.6.1</strong><br>文件頁 825–826 · PDF 851–852</li>
<li id="ref-pcie"><strong>PCIe Transport 1.4 · §3.1–3.4</strong><br>文件頁 9–13 · PDF 9–13 · Figure 3–8</li>
</ul><h3>需要看欄位圖時</h3><p>既有圖表教學各有固定位置。這裡連回相關圖，不複製另一份圖解。</p><ul>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b42">Base 2.4 Figure 42 · Offset 1Ch: CSTS – Controller Status</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b44">Base 2.4 Figure 44 · Offset 24h: AQA – Admin Queue Attributes</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b45">Base 2.4 Figure 45 · Offset 28h: ASQ – Admin Submission Queue Base Address</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b46">Base 2.4 Figure 46 · Offset 30h: ACQ – Admin Completion Queue Base Address</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/initialization/en/">English</a><a href="/DOCS/nvme-question-bank/initialization.html">繁中教學 HTML</a></nav>
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
