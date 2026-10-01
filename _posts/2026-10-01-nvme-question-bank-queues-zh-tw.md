---
layout: post
title: "NVMe 自問自答題庫：Admin Queue 與 I/O Queue"
date: 2026-10-01 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/queues/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/queues/en/">English</a><a href="/DOCS/nvme-question-bank/queues.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–68</p>
<header><p class="qa-range">Q10–Q21</p><h1>Admin Queue 與 I/O Queue</h1><p class="qr-intro">Queue 的記憶體、controller 分配的數量，以及已成功建立的 queue，是三件事。先理解 SQ 與 CQ 的依賴，再看大小、識別碼、刪除與重設，才能判斷何時可以安全回收記憶體。</p><p>先練習，再展開每題的 17 項解答。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可以指定的一份邏輯儲存空間。多個 controller 可以屬於同一 NVM subsystem（包含 controller 與非揮發儲存資源的整體）。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue 是提交佇列，Completion Queue 是完成佇列；SQE／CQE 是其中的一筆 entry。QID 識別 queue，CID 識別同一 SQ 內尚未完成的命令，NSID 識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 是可存取的控制或狀態欄位；Identify 查物件能力與屬性；Feature 查／設工作設定；Log Page 回報指定種類的狀態或紀錄。FID、LID、CNS、CSI 分別選 Feature、Log、Identify 結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 是第幾筆，通常由 0 起算；offset 是離起點多遠，要看單位。zero-based 數量欄位的實際數量＝編碼＋1，但不是每個寫 0 的欄位都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 指一項操作影響的物件範圍。retention 是狀態是否保留。Controller Reset（清 CC.EN）是一種 Controller Level Reset，簡稱 CLR；同一類 CLR 的不同觸發方式，Register 保留規則仍可能不同。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>一個 CQ、兩個 SQ：建立與回收是相反方向</h2><p class="qa-takeaway">CQ 是 SQ 回報完成的目的地；仍有 SQ 依賴它時，不能先刪掉它。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">觀察層次</th><th scope="col">教學假設</th><th scope="col">可以推論什麼</th></tr></thead><tbody><tr><td>數量配額</td><td>FID07h 回 NSQA=3、NCQA=1</td><td>分配 4 個 I/O SQ、2 個 I/O CQ；尚未建立</td></tr><tr><td>單一 queue 深度</td><td>Create CQ：QID=1、QSIZE=7</td><td>8 個 entries；ring 要保留一格辨認 Full</td></tr><tr><td>依賴關係</td><td>SQ1.CQID=1；SQ2.CQID=1</td><td>先建 CQ1，再建 SQ1、SQ2</td></tr><tr><td>回收順序</td><td>刪 SQ1、SQ2，各自等成功完成</td><td>再刪 CQ1；相關生命週期結束後才回收記憶體</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>假設 SQ1 已刪除，但 SQ2 仍存在。此時刪 CQ1 仍是非法順序，因為 SQ2 還要向 CQ1 回報。SQ1 的刪除完成，也不代表 SQ2 的資料 buffer 可以回收。</p>
<p class="qa-citations">來源：<a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-010">Q10 · Admin Submission Queue 與 Admin Completion Queue 如何透過 AQA、ASQ 及 ACQ 建立？</a></li>
<li><a href="#q-011">Q11 · Admin Queue 與 I/O Queue 的 Size、Base Address 及 Memory Page 對齊有哪些要求？</a></li>
<li><a href="#q-012">Q12 · Host 如何建立 I/O Completion Queue 與 I/O Submission Queue？兩者必須遵守什麼建立順序？</a></li>
<li><a href="#q-013">Q13 · 多個 SQ 共用一個 CQ 與每個 SQ 使用獨立 CQ 有什麼差異？</a></li>
<li><a href="#q-014">Q14 · Host 如何確認 Controller 支援 Physically Contiguous 或其他 Queue 形式？</a></li>
<li><a href="#q-015">Q15 · QID 重複、QID 為 0、CQID 不存在、Queue Size 超過 CAP.MQES 或 Interrupt Vector 非法時，Controller 應如何回應？</a></li>
<li><a href="#q-016">Q16 · Number of Queues Feature 回傳的數值與實際可建立的 Queue 數量有什麼關係？</a></li>
<li><a href="#q-017">Q17 · Host 刪除 I/O Queue 時，SQ 與 CQ 的相依關係如何限制刪除順序？</a></li>
<li><a href="#q-018">Q18 · 刪除不存在的 Queue、仍被 SQ 使用的 CQ 或仍有 Outstanding Command 的 SQ 時，應如何處理？</a></li>
<li><a href="#q-019">Q19 · Queue 刪除後，Controller 是否還能存取原 Queue Memory 或回報原 Queue 的 Completion？</a></li>
<li><a href="#q-020">Q20 · Queue Level Reset 的影響範圍是什麼？Outstanding Command 應如何處理？</a></li>
<li><a href="#q-021">Q21 · Controller Reset 後，原有 I/O Queue 是否有效？Host 需要重新執行哪些操作？</a></li>
</ol></section>
<article class="qa-question" id="q-010" data-question="10"><h2><a class="qa-qid" href="#q-010">Q10</a> Admin Submission Queue 與 Admin Completion Queue 如何透過 AQA、ASQ 及 ACQ 建立？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-010-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-010-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>先提供承載管理命令的通道，才有辦法使用 Create I/O Queue；Admin queue 不能用尚不存在的自己來建立自己。</p>
</li>
<li id="q-010-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>每個 controller 有 QID=0 的 Admin SQ／CQ；這不是一般 I/O QID。</p>
</li>
<li id="q-010-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>AQA 決定各自長度；ASQ／ACQ 提供各自實體起點。Admin queue 必須實體連續，不能用 PC=0 的 Create Queue PRP list 方式建立。</p>
</li>
<li id="q-010-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>ASQS、ACQS 均為 zero-based；64 entries 寫 63。Admin SQE 64 bytes、CQE 16 bytes；兩條 queue 可以有不同長度。</p>
</li>
<li id="q-010-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>配置並清理記憶體，在 EN=0 時寫入三個 Register，清 Admin CQ Phase；完成 CC 設定後 Enable，等 RDY=1 再提交第一個 Admin command。</p>
</li>
<li id="q-010-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Admin SQ 可送 Identify，Admin CQ 可回對應 CID；ACQ 關聯 interrupt vector 0，但 Host 仍可透過 Phase 輪詢完成。</p>
</li>
<li id="q-010-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>size=0 對應一個 slot，不是停用 queue 的合法方法；以此 Enable 的結果 undefined。也不能用 Delete I/O Queue 刪 Admin queue。</p>
</li>
<li id="q-010-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>本次 MMIO 存取沒有 NVMe CQE，因此 DNR／More 不適用。 <a class="qa-rule-link" href="#common-register-8">本冊完整規則</a></p>
</li>
<li id="q-010-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Register 存取本身沒有成功事件；另有硬體錯誤時使用該事件的條件。 <a class="qa-rule-link" href="#common-register-9">本冊完整規則</a></p>
</li>
<li id="q-010-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>不逐次記錄 Register 讀寫；先保留 Register 值與時間，再取得可用的診斷紀錄。 <a class="qa-rule-link" href="#common-register-10">本冊完整規則</a></p>
</li>
<li id="q-010-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Register 存取不構成 PEL 事件；完成的 Reset 或支援的硬體錯誤另判斷。 <a class="qa-rule-link" href="#common-register-11">本冊完整規則</a></p>
</li>
<li id="q-010-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-010-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-010-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-010-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-010-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>核對 AQA 長度、實際記憶體配置與第一筆 CQE。Register 可讀回正確不代表裝置能存取 Host 所給記憶體。</p>
</li>
<li id="q-010-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先看 ASQ／ACQ 的位址與 CC.MPS 對齊，再看是否清除舊 Phase。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-adminreg">Base 2.4 §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</a> · <a href="#ref-init">Base 2.4 §3.5.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-011" data-question="11"><h2><a class="qa-qid" href="#q-011">Q11</a> Admin Queue 與 I/O Queue 的 Size、Base Address 及 Memory Page 對齊有哪些要求？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-011-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-011-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>避免把 entries、bytes、memory pages 當成同一個長度，也避免 queue 超出配置記憶體。</p>
</li>
<li id="q-011-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>規則分 Admin 與 I/O，也分 Host memory 與能力允許的 CMB；不能從其中一種推論全部配置。</p>
</li>
<li id="q-011-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Admin 看 AQA；I/O 看 CAP.MQES、CQR 與 CC.IOSQES／IOCQES。CMB 例外另看 CMBLOC.CQDA／CQPDS 與 CMBSZ 的 queue 支援。</p>
</li>
<li id="q-011-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>長度欄位是 entries−1。一般 queue base 與非連續 queue 的每個 PRP 頁依 CC.MPS 對齊；PRP1 的 offset 為 0。</p>
</li>
<li id="q-011-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先決定 slots 和 entry size，再計算 bytes、配置頁面、建立 PRP list（若允許），最後提交 Create。PRP list 在 queue 有效期間不得任意改動。</p>
</li>
<li id="q-011-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>最少 2 slots；Admin 最多 4096，I/O 最多 min(65536, MQES+1)。為分辨滿與空，每條 queue 保留一個不能使用的 slot。</p>
</li>
<li id="q-011-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>I/O 大小錯誤對應 Invalid Queue Size（1/02h）；非零 PRP offset 應回 PRP Offset Invalid（0/13h）；違反 CQR 的 PC 設定依 Create SQ／CQ 的規範強度判斷。</p>
</li>
<li id="q-011-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-011-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-011-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-011-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-011-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-011-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-011-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-011-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-011-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>例：128-slot NVM SQ 需要 8192 bytes，CQ 需要 2048 bytes；不是因為 QSIZE 都是 127 就配置相同 bytes。</p>
</li>
<li id="q-011-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查 QSIZE 是否重複加 1、entry size 是否誤用，以及對齊採用的是 CC.MPS 而非任意 OS page size。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-adminreg">Base 2.4 §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</a> · <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-qattr">Base 2.4 §3.3.3–3.4.1</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-012" data-question="12"><h2><a class="qa-qid" href="#q-012">Q12</a> Host 如何建立 I/O Completion Queue 與 I/O Submission Queue？兩者必須遵守什麼建立順序？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-012-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-012-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>每筆 I/O 必須有合法的回覆目的地，所以先建立 CQ，再把 SQ 指向它；這是相依順序要求，不只是效能建議。</p>
</li>
<li id="q-012-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>一個 SQ 在建立時指定其 CQ；多個 SQ 可以指向同一個已存在的 CQ。</p>
</li>
<li id="q-012-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先配置 Number of Queues，再核對 CAP.MQES／CQR、entry sizes 與 interrupt vector 範圍。</p>
</li>
<li id="q-012-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Create CQ 用 PRP1、QID、QSIZE、PC、IEN、IV；Create SQ 加上 CQID、QPRIO、NVMSETID。NVMSETID=0 表示沒有指定 Set 關聯。</p>
</li>
<li id="q-012-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>準備 CQ 記憶體及初始 Phase→Create CQ 並等成功→Create SQ 指向 CQID 並等成功→填 SQE、更新 Tail。</p>
</li>
<li id="q-012-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>兩個 Create 都在 Admin CQ 回成功（0/00h），之後 I/O 命令的完成寫入新 I/O CQ；不能到新 CQ 等待它自己的 Create completion。</p>
</li>
<li id="q-012-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>CQID 在支援範圍內但未建立，回 Completion Queue Invalid（1/00h）；CQID=0 或超界回 Invalid Queue Identifier（1/01h）。</p>
</li>
<li id="q-012-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-012-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-012-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-012-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-012-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-012-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-012-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-012-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-012-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>核對 Create SQ 中的 CQID 與 Host 的 SQ→CQ 映射；成功的 Create CQ 不代表任意 SQ 都自動連到它。</p>
</li>
<li id="q-012-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查 CQ Create 是否已成功完成，而非只是已提交。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-013" data-question="13"><h2><a class="qa-qid" href="#q-013">Q13</a> 多個 SQ 共用一個 CQ 與每個 SQ 使用獨立 CQ 有什麼差異？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-013-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-013-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>在資源用量與完成處理隔離之間取捨；共用 CQ 可以減少 CQ 資源，但會把完成流量集中。</p>
</li>
<li id="q-013-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>共享的是 completion slots 與 CQ 關聯通知，不是讓所有 SQ 共用同一個 CID 空間。</p>
</li>
<li id="q-013-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Number of Queues 分別回 SQ／CQ 配額；Create SQ 的 CQID 指定映射，CQ 的 IEN／IV 決定通知配置。</p>
</li>
<li id="q-013-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CQE 的 SQID+CID 對回原命令，SQHD 則更新該 SQ 的消費位置。</p>
</li>
<li id="q-013-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先建 CQ，再建兩條以上 SQ 指向同一 CQID；Host 消費每筆 CQE 時按 SQID 分派，最後更新該 CQ 的 Head。</p>
</li>
<li id="q-013-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例：SQ1/CID7 與 SQ2/CID7 可以同時存在，回覆必須分別對回；這與在同一 SQ 重用 outstanding CID 不同。</p>
</li>
<li id="q-013-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>合法共用不產生錯誤；不存在 CQID 用 Create SQ 的專用 Status。共用 CQ 已滿不等於每個 SQ 自動回 Invalid Queue Size。</p>
</li>
<li id="q-013-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-013-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-013-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-013-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-013-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-013-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-013-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-013-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-013-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>比較可用 completion slots、SQ 流量與 Host 消費速率；不能只看 SQ 數量推測沒有瓶頸。</p>
</li>
<li id="q-013-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先看 completion 對應是不是只用 CID，漏了 SQID。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-014" data-question="14"><h2><a class="qa-qid" href="#q-014">Q14</a> Host 如何確認 Controller 支援 Physically Contiguous 或其他 Queue 形式？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-014-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-014-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>讓 queue 的記憶體描述方式符合 controller 可使用的形式；虛擬位址連續不等於實體連續。</p>
</li>
<li id="q-014-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Admin queue 固定要求實體連續；I/O queue 是否可由多個頁面組成，依 CAP.CQR 與配置位置決定。</p>
</li>
<li id="q-014-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>CQR=1 要求實體連續；CQR=0 允許 I/O 使用非連續頁面。放在 CMB 時還要查 CMBSZ.SQS／CQS、CMBLOC.CQPDS／CQDA。</p>
</li>
<li id="q-014-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Create I/O Queue 的 PC=1：PRP1 是 queue base；PC=0：PRP1 是描述 queue 頁面的 PRP list 位址，並非資料傳輸的一般 PRP2 規則。</p>
</li>
<li id="q-014-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>確認位置和能力，建立對齊且完整的 page list，提交 Create；直到成功 Delete 或 reset 前保留 list 位置與內容。</p>
</li>
<li id="q-014-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>controller 能依所選形式取 SQE／寫 CQE；成功 Create 不授權 Host 在執行中重新排列頁面。</p>
</li>
<li id="q-014-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>CQR=1 且 PC=0：Create CQ 必須（shall）回 Invalid Field（0/02h），Create SQ 的對應要求為建議（should）回覆；不支援的 CMB 用法可能為 Invalid Use of Controller Memory Buffer（0/12h）。</p>
</li>
<li id="q-014-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-014-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-014-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-014-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-014-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-014-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-014-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-014-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-014-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>把 CQR、PC、PRP1 解讀與實際頁面布局四者核對；不要只驗證 Create completion。</p>
</li>
<li id="q-014-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先問 PRP1 指向 queue 本體，還是 PRP list；兩者搞反會讓有效位址也變成錯誤結構。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-adminreg">Base 2.4 §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-015" data-question="15"><h2><a class="qa-qid" href="#q-015">Q15</a> QID 重複、QID 為 0、CQID 不存在、Queue Size 超過 CAP.MQES 或 Interrupt Vector 非法時，Controller 應如何回應？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-015-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-015-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>把不同參數錯誤對到各自的 Status，不能全部統一寫 Invalid Field。</p>
</li>
<li id="q-015-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>檢查的是 Create I/O Queue Admin command；QID 重複依 SQ 或 CQ 各自的識別空間判斷。</p>
</li>
<li id="q-015-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>CAP.MQES、Number of Queues 回覆和 PCIe interrupt 配置是合法範圍的依據。</p>
</li>
<li id="q-015-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>以 QID、CQID、QSIZE、IV 為主，並確認 IOSQES／IOCQES 已初始化；錯誤欄位在 CDW10／11。</p>
</li>
<li id="q-015-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>學習測例一次只改一個條件：先建立合法參考配置，再分別送重複 QID、缺 CQID 等假設命令，避免多錯誤遮蔽預期。</p>
</li>
<li id="q-015-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>合法參數回成功並建立指定 queue；失敗後不能把該 QID 當成已建立。</p>
</li>
<li id="q-015-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>同類 QID 重複／0／超範圍：1/01h；QSIZE=0 或超支援：1/02h；合法範圍內 CQID 未建立：1/00h；CQID=0／超界：1/01h；非法 IV：1/08h。多個錯誤同時成立時，除特別規定外由實作選擇回哪個。</p>
</li>
<li id="q-015-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-015-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-015-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-015-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-015-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-015-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-015-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-015-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-015-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Error Information 若有資料，可用 Parameter Error Location 回指欄位；但沒有 More=1 不能硬要求該錯誤一定有 entry。</p>
</li>
<li id="q-015-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先检查測例是否真的只有一個非法欄位，以及 expected SCT 是否為 1，避免只比較 SC。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-irq">PCIe Transport 1.4 §3.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-016" data-question="16"><h2><a class="qa-qid" href="#q-016">Q16</a> Number of Queues Feature 回傳的數值與實際可建立的 Queue 數量有什麼關係？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-016-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-016-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>先取得 I/O SQ 與 CQ 配額，再在配額內建立 queue；配額不是 queue 本身，也不是每條 queue 的深度。</p>
</li>
<li id="q-016-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>FID 07h 作用於 controller，不包含 Admin SQ／CQ。</p>
</li>
<li id="q-016-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>用 Set Features FID 07h 的 CQE DW0 回覆判斷實際配置，之後可 Get Features 讀回。CAP.MQES 另限制每條深度。</p>
</li>
<li id="q-016-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CDW11 的 NSQR／NCQR 與 DW0 的 NSQA／NCQA 都是 zero-based；回覆可能比要求少，也可能因配置單位而較多。</p>
</li>
<li id="q-016-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>CLR 後、任何 I/O Queue 建立前設定；第一筆成功設定決定此次配置。之後到下一次 CLR 前配置數不改變。</p>
</li>
<li id="q-016-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例：DW0=00030007h 表示 4 個 CQ、8 個 SQ 配額；仍須個別 Create，QID 範圍分別依 4 與 8 判斷。</p>
</li>
<li id="q-016-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>已有 I/O queue 再 Set 必須回 Command Sequence Error（0/0Ch）；Requested=FFFFh 應回 Invalid Field（0/02h）。尚未建 queue 的後續 Set 應成功但不改已配置數。</p>
</li>
<li id="q-016-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-016-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-016-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-016-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get 本身不產生 Set Feature Event；Set 則要確認此 FID 的記錄支援、是否成功及設定是否改變。 <a class="qa-rule-link" href="#common-feature_events-11">本冊完整規則</a></p>
</li>
<li id="q-016-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後第一筆成功 Set FID 07h 重新配置 queue 數；Host 應重新取得回覆，再重建 I/O queue，不能直接沿用前次配額。</p>
</li>
<li id="q-016-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 經 CLR 後重新協商 Number of Queues；NVM Subsystem Reset 不會保留舊 I/O Queue 配置讓 Host 直接送 I/O。</p>
</li>
<li id="q-016-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化、設定 FID 07h 並建立 queue；Saved／Default 的一般概念不能代替這個初始化順序。</p>
</li>
<li id="q-016-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-016-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>核對回覆的配額、實際已建 queue 清單與 MQES 三份資訊，不能把 Get 的配額解成目前存在數。</p>
</li>
<li id="q-016-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否用了 requested 值而忽略 returned 值，或忘記對 NSQA／NCQA 加 1。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-017" data-question="17"><h2><a class="qa-qid" href="#q-017">Q17</a> Host 刪除 I/O Queue 時，SQ 與 CQ 的相依關係如何限制刪除順序？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-017-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-017-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>避免仍有命令要完成的 SQ 失去回覆位置。對關聯 queue，這是 Host 必須遵守的刪除順序。</p>
</li>
<li id="q-017-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>一個 CQ 可能被多條 SQ 使用，必須刪除所有相關 SQ，不是只刪 QID 相同的 SQ。</p>
</li>
<li id="q-017-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>使用 Host 在 Create SQ 時保存的 SQ→CQID 對照；Number of Queues 不提供這張連線清單。</p>
</li>
<li id="q-017-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Delete I/O SQ／CQ 的 CDW10.QID 指定對象；它們都透過 Admin SQ 提交。</p>
</li>
<li id="q-017-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>停止向目標 SQ 提交，適當等待既有命令，逐一 Delete SQ 並等成功，消費需要處理的舊完成，再 Delete CQ。</p>
</li>
<li id="q-017-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Delete CQ 成功後，Host 才可收回其 PRP list 與 queue 資源；Delete SQ 的成功另建立該 SQ 命令處理的終止界線。</p>
</li>
<li id="q-017-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>尚有相關 SQ 時 Delete CQ 必須回 Invalid Queue Deletion（1/0Ch）；QID=0 或非法對象回 Invalid Queue Identifier（1/01h）。</p>
</li>
<li id="q-017-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-017-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-017-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-017-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-017-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-017-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-017-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-017-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-017-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>把刪除成功時間接到記憶體釋放時間；「已送 Delete」不足以允許提前收回 DMA 記憶體。</p>
</li>
<li id="q-017-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查 CQ 是否還被另一條 SQ 指向，而非只檢查 CQ 自己是否已空。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-018" data-question="18"><h2><a class="qa-qid" href="#q-018">Q18</a> 刪除不存在的 Queue、仍被 SQ 使用的 CQ 或仍有 Outstanding Command 的 SQ 時，應如何處理？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-018-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-018-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>分開「刪除要求非法」與「合法刪除造成命令終止」；仍有 outstanding 並不直接讓 Delete SQ 變成非法。</p>
</li>
<li id="q-018-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>刪 SQ 影響那條 SQ 的所有未完成 I/O；刪 CQ 先受所有相關 SQ 的存在狀態限制。</p>
</li>
<li id="q-018-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先查 Host 的建立／刪除紀錄與 outstanding 清單。這些是執行狀態，不是 Identify 的選配能力。</p>
</li>
<li id="q-018-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Delete 的 QID 必須有效且不為 0；目標 I/O 命令仍以各自 SQID／CID 辨識。</p>
</li>
<li id="q-018-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>正常拆除先排空再刪。若為中止工作而刪 SQ，等 Delete 成功後，把未收到 CQE 的原命令作隱含中止處理。</p>
</li>
<li id="q-018-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Delete SQ 成功前，原命令可能已成功或回中止 CQE；成功之後不得再為原 SQ 命令寫 completion。</p>
</li>
<li id="q-018-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>非法 QID：1/01h；仍有 SQ 的 CQ：1/0Ch。原 I/O 若因刪 SQ 中止，狀態為 Command Aborted due to SQ Deletion（0/08h），也可能以 Delete 成功形成隱含完成。</p>
</li>
<li id="q-018-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-018-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-018-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-018-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-018-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-018-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-018-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-018-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-018-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>測試應同時計數已收到 CQE 與 Delete 成功後隱含中止者；不要要求每個原命令都必須實際出現一筆 CQE。</p>
</li>
<li id="q-018-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查 Delete SQ 是否已成功完成；在它還 outstanding 時，不能宣布所有原命令已停止。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-019" data-question="19"><h2><a class="qa-qid" href="#q-019">Q19</a> Queue 刪除後，Controller 是否還能存取原 Queue Memory 或回報原 Queue 的 Completion？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-019-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-019-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>找出可以安全收回記憶體的界線，並區分「先前已寫入但 Host 晚看到」與「刪除成功後才寫入」。</p>
</li>
<li id="q-019-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Delete SQ 不會同時刪除共用 CQ；CQ 中先前完成仍可能等待 Host 消費。</p>
</li>
<li id="q-019-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>以 Admin CQ 上 Delete 的成功結果為界，不以 Host 送出時間或自訂 timeout 為界。</p>
</li>
<li id="q-019-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>追蹤被刪 QID、關聯 CQID、PRP list 位址及 memory lifetime。相同位址重新使用後必須能區分新舊 queue。</p>
</li>
<li id="q-019-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>停止提交、Delete 並等成功，再收回對應 queue／PRP list。只刪 SQ 時繼續妥善處理仍存在 CQ 的已張貼內容。</p>
</li>
<li id="q-019-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功 Delete SQ 後不得新增原 SQ 命令的 completion；成功 Delete CQ 後其描述 PRP list 可釋放，已刪 queue 不再是可用 DMA 目標。</p>
</li>
<li id="q-019-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>若 Delete 本身失敗或沒有完成，不能推論記憶體已可收回。逾時不是另一種 Successful Completion。</p>
</li>
<li id="q-019-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-019-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-019-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-019-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-019-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-019-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-019-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-019-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-019-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>用寫入時間、CQ Phase、Delete completion 與 Host 消費時間核對；晚消費的舊 CQE 不等於違規的晚寫入。</p>
</li>
<li id="q-019-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認所見 CQE 真正寫入於 Delete 成功之前還是之後。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-020" data-question="20"><h2><a class="qa-qid" href="#q-020">Q20</a> Queue Level Reset 的影響範圍是什麼？Outstanding Command 應如何處理？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-020-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-020-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>在不重設整個 controller 的情況下重建 I/O queue。PCIe 的 Queue Level Reset 是刪除再建立，不是另一個 Reset opcode。</p>
</li>
<li id="q-020-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>只重設目標 queue 及必要相依 queue；若重建 CQ，所有使用它的 SQ 都需先刪除並在 CQ 重建後再建。</p>
</li>
<li id="q-020-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>依已建立的 queue 關係與 Create／Delete 規則執行，不靠一個另行定義的 Queue Reset Feature。</p>
</li>
<li id="q-020-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Delete SQ／CQ、Create CQ／SQ；QID 可重用，但 queue 記憶體與指標從新生命週期開始。</p>
</li>
<li id="q-020-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>正常應先讓工作完成，再刪除；需要中止時按 Delete SQ 的明確／隱含完成規則。新 CQ 初始化 Phase，先 CQ 後 SQ。</p>
</li>
<li id="q-020-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>重建成功後新命令可執行，原 outstanding 命令不會自動搬入新 SQ。</p>
</li>
<li id="q-020-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>錯誤刪 CQ 得 1/0Ch；沒有有效 CQ 就先建 SQ 得相應 CQID 錯誤。Queue reset 本身沒有額外統一 Status。</p>
</li>
<li id="q-020-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-020-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-020-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-020-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-020-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-020-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-020-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-020-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-020-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>核對刪除／建立順序與新舊 CID 對照，並檢查其他獨立 queue 是否保持正常。</p>
</li>
<li id="q-020-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先列出目標 CQ 的所有使用者；漏一條共享 SQ 就可能使重設流程不合法。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-021" data-question="21"><h2><a class="qa-qid" href="#q-021">Q21</a> Controller Reset 後，原有 I/O Queue 是否有效？Host 需要重新執行哪些操作？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-021-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-021-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>把故障前的命令與恢複後的新命令分開，避免誤認殘留 completion。</p>
</li>
<li id="q-021-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Controller Level Reset 刪除該 controller 的全部 I/O SQ／CQ；不同於只刪除一條 SQ。</p>
</li>
<li id="q-021-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>重讀必要 Identify，確認 Number of Queues 配額與 entry size／interrupt 設定，不能直接假設前次值仍有效。</p>
</li>
<li id="q-021-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Admin Register、CC、Get／Set Features、Create CQ／SQ 共同構成重建路徑。</p>
</li>
<li id="q-021-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>確認 RDY=0→初始化 Admin CQ Phase 與 CC→Enable、等 RDY→恢復必要 Feature→Set Number of Queues→建 CQ→建 SQ→允許新 I/O。</p>
</li>
<li id="q-021-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>每次 Create 在 Admin CQ 成功後，對應新 queue 才有效；不論是否沿用相同 QID 或位址。</p>
</li>
<li id="q-021-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>直接更新舊 queue Doorbell 不構成合法恢復，不能要求它繼續處理；重建命令的失敗則依各自 Status 處理。</p>
</li>
<li id="q-021-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-021-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-021-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-021-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-021-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-021-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-021-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-021-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-021-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>保存 reset 前後的 queue generation 與命令對照；這是 Host 追蹤方法，不是新增一個 NVMe wire field。</p>
</li>
<li id="q-021-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先看 Host 是否在新 Create 成功前就恢復 I/O。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-init">Base 2.4 §3.5.1</a> · <a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-command-8"><h3>命令完成、事件與紀錄 · DNR 與 More 應如何設定？</h3><p>有 CQE 時，DNR=1 表示相同命令再送到此 NVM subsystem 的任一 controller 仍預期失敗；DNR=0 只表示可能成功。除非本題錯誤另有明定，不把某個 Status 固定綁成 DNR=1。More=1 表示 Error Information Log 有這筆命令的補充資訊。SCT=SC=0 時 DNR 應為 0。</p></article>
<article id="common-command-9"><h3>命令完成、事件與紀錄 · 是否產生 Asynchronous Event？</h3><p>命令完成與非同步通知是兩件事；本題操作成功本身不保證有事件。若操作引起規範列出的事件，還要核對事件支援、適用的通知設定、是否已遮蔽，以及 Host 是否掛入 Asynchronous Event Request。</p></article>
<article id="common-command-10"><h3>命令完成、事件與紀錄 · 是否更新 Error Information Log 或其他 Log？</h3><p>成功 CQE 不是要求新增 Error Information 的理由。錯誤有 More=1 時，查 LID 01h 並用 SQID、CID 和 Error Count 對應；不能把每個非成功 CQE 都當成必須新增一筆。操作改變的狀態則由本題列出的查詢介面重新讀取。</p></article>
<article id="common-command-11"><h3>命令完成、事件與紀錄 · 是否記錄於 Persistent Event Log？</h3><p>Persistent Event Log 是選配的事件歷史，不是所有命令的執行清單。先查 LPA 的支援與 Supported Events Bitmap，再判斷本次是否符合指定事件的記錄條件；不能只因命令成功或失敗就要求新增一筆。</p></article>
<article id="common-feature-15"><h3>Feature 的重設與影響範圍 · 是否影響其他 Controller 或 Namespace？</h3><p>依 Feature scope 決定。Controller scope 通常只控制目標 controller；namespace、NVM Set 或 subsystem scope 可能由其他 controller 共同觀察。跨 Host 修改共用設定需要協調，不能把 NSID=FFFFFFFFh 當成所有 Feature 通用的廣播。</p></article>
<article id="common-feature_events-11"><h3>Set Feature 的事件記錄 · 是否記錄於 Persistent Event Log？</h3><p>若支援 PEL 的 Set Feature Event，還要看 Figure 252 是否支援記錄此 FID：Set 成功且設定改變時必須記錄；成功但重設相同值則允許記錄。不是每個 FID 都能套用此事件；Timestamp 的 Set Feature Event 明確禁止，另用 Timestamp Change Event 判斷。</p></article>
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
<li id="ref-adminreg"><strong>Base 2.4 · §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</strong><br>文件頁 66–68 · PDF 92–94 · Figure 44–47</li>
<li id="ref-queue"><strong>Base 2.4 · §3.3.1</strong><br>文件頁 88–91 · PDF 114–117 · Figure 73–74</li>
<li id="ref-qattr"><strong>Base 2.4 · §3.3.3–3.4.1</strong><br>文件頁 101 · PDF 127</li>
<li id="ref-init"><strong>Base 2.4 · §3.5.1</strong><br>文件頁 105–106 · PDF 131–132</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>文件頁 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>文件頁 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-featureeffects"><strong>Base 2.4 · §5.2.13.1.18</strong><br>文件頁 276–278 · PDF 302–304 · Figure 270–271</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>文件頁 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-number"><strong>Base 2.4 · §5.2.30.1.5</strong><br>文件頁 465–466 · PDF 491–492 · Figure 472–473</li>
<li id="ref-create"><strong>Base 2.4 · §5.3.1–5.3.2</strong><br>文件頁 527–531 · PDF 553–557 · Figure 571–579</li>
<li id="ref-delete"><strong>Base 2.4 · §5.3.3–5.3.4</strong><br>文件頁 531–532 · PDF 557–558 · Figure 580–583</li>
<li id="ref-fatal"><strong>Base 2.4 · §9.1–9.6.1</strong><br>文件頁 825–826 · PDF 851–852</li>
<li id="ref-irq"><strong>PCIe Transport 1.4 · §3.5</strong><br>文件頁 13–16 · PDF 13–16 · Figure 9</li>
</ul><h3>需要看欄位圖時</h3><p>既有圖表教學各有固定位置。這裡連回相關圖，不複製另一份圖解。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b44">Base 2.4 Figure 44 · Offset 24h: AQA – Admin Queue Attributes</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b45">Base 2.4 Figure 45 · Offset 28h: ASQ – Admin Submission Queue Base Address</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b46">Base 2.4 Figure 46 · Offset 30h: ACQ – Admin Completion Queue Base Address</a></li>
<li><a href="/nvme/figure-reference/features/zh-tw/#figure-b473">Base 2.4 Figure 473 · Number of Queues – Completion Queue Entry Dword 0</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/queues/en/">English</a><a href="/DOCS/nvme-question-bank/queues.html">繁中教學 HTML</a></nav>
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
