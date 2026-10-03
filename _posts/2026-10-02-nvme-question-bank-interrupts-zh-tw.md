---
layout: post
title: "NVMe 自問自答題庫：Interrupt 設定與完成通知"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/interrupts/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/interrupts/en/">English</a><a href="/DOCS/nvme-question-bank/interrupts.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q286–Q296</p><h1>Interrupt 設定與完成通知</h1><p class="qr-intro">先確認 CQE 真的存在，再查通知如何送到 Host。本冊把 CQ 關聯、合併、mask 與 Host 處理分開，避免把沒有中斷當成沒有完成。</p><p>先練習，再展開每題的 17 項解答。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>四個控制，四個不同問題</h2><p class="qa-takeaway">FID09h.CD 停用的是 coalescing，不是 interrupt。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">控制</th><th scope="col">欄位／介面</th><th scope="col">決定什麼</th></tr></thead><tbody><tr><td>CQ 通知路徑</td><td>Create CQ.IV／IEN</td><td>用哪個 vector、是否通知</td></tr><tr><td>合併</td><td>FID08h.TIME／THR</td><td>建議合併時間與數量</td></tr><tr><td>單 vector 例外</td><td>FID09h.CD</td><td>是否停用該 vector 合併</td></tr><tr><td>遮蔽</td><td>INTMS／INTMC 或 MSI-X masks</td><td>是否允許送出中斷</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>兩條 CQ 共用 IV3，mask=1 時仍可能寫入 CQE。解除 mask 後，一次通知可讓 Host 處理多筆完成，不要求每筆補送一次中斷。</p>
<p class="qa-citations">來源：<a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-286">Q286 · CQ 如何指定 Interrupt Vector？</a></li>
<li><a href="#q-287">Q287 · 多條 CQ 共用 Vector 與獨立 Vector 有何不同？</a></li>
<li><a href="#q-288">Q288 · Interrupt Coalescing 的 Threshold 與 Time 如何作用？</a></li>
<li><a href="#q-289">Q289 · 如何停用 Interrupt Coalescing？</a></li>
<li><a href="#q-290">Q290 · FID09h 是遮蔽中斷嗎？真正的 Mask 要如何設定？</a></li>
<li><a href="#q-291">Q291 · Vector 被遮蔽時，Controller 還能寫 CQE 嗎？</a></li>
<li><a href="#q-292">Q292 · 解除 Mask 後如何處理累積完成？</a></li>
<li><a href="#q-293">Q293 · 已被 CQ 使用的 Vector 可以修改設定嗎？</a></li>
<li><a href="#q-294">Q294 · Reset 後中斷設定要如何恢復？</a></li>
<li><a href="#q-295">Q295 · Queue 刪除後如何回收中斷資源？</a></li>
<li><a href="#q-296">Q296 · 如何比對 Interrupt、CQ 與實際完成行為？</a></li>
</ol></section>
<article class="qa-question" id="q-286" data-question="286"><h2><a class="qa-qid" href="#q-286">Q286</a> CQ 如何指定 Interrupt Vector？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-286-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-286-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>CQ 決定完成結果放在哪裡，IV 決定透過哪個中斷通知 Host，兩個編號不必相同。</p>
</li>
<li id="q-286-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>關聯建立在 I/O CQ 上，SQ 透過 CQID 間接使用該通知路徑。</p>
</li>
<li id="q-286-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先確認 PCIe 中斷模式及已配置的 vector 數，再建立 CQ。</p>
</li>
<li id="q-286-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Create CQ.CDW11 的 IV[31:16] 選 vector，IEN[1] 啟用該 CQ 中斷；PC[0] 控制記憶體配置。</p>
</li>
<li id="q-286-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>配置中斷資源、建立 CQ、建立關聯 SQ，之後才送 I/O 驗證通知。</p>
</li>
<li id="q-286-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例如 CQ5 使用 IV2；來自 SQ7 的完成寫入 CQ5，Host 收 IV2 後查 CQ5，再由 CQE.SQID／CID 找命令。</p>
</li>
<li id="q-286-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Create CQ 指定不合法 vector 時對應 Invalid Interrupt Vector（SCT1、SC08h）；不能以 QID 是否有效代替 IV 檢查。</p>
</li>
<li id="q-286-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-286-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Completion 中斷與 Asynchronous Event Request 是不同機制。 <a class="qa-rule-link" href="#common-interrupt_op-9">本冊完整規則</a></p>
</li>
<li id="q-286-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>合法中斷設定與傳送本身不要求新增 Error Information。 <a class="qa-rule-link" href="#common-interrupt_op-10">本冊完整規則</a></p>
</li>
<li id="q-286-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>中斷不逐次記入 PEL。 <a class="qa-rule-link" href="#common-interrupt_op-11">本冊完整規則</a></p>
</li>
<li id="q-286-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後原 I/O queues 失效，CQ 與 vector 關係需隨 queue 重建。 <a class="qa-rule-link" href="#common-interrupt_op-12">本冊完整規則</a></p>
</li>
<li id="q-286-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新建立受影響 controller 的 queue、vector 關聯與需要的設定。 <a class="qa-rule-link" href="#common-interrupt_op-13">本冊完整規則</a></p>
</li>
<li id="q-286-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新配置中斷模式與 queues，再讀回或設定所需 Feature。 <a class="qa-rule-link" href="#common-interrupt_op-14">本冊完整規則</a></p>
</li>
<li id="q-286-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 vector 可服務多條 CQ，遮蔽或變更該 vector 的合併設定會影響這些 CQ 的通知。 <a class="qa-rule-link" href="#common-interrupt_op-15">本冊完整規則</a></p>
</li>
<li id="q-286-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>核對 CQ 建立成功、IV、IEN 與 Host 處理程序的 CQ 清單。</p>
</li>
<li id="q-286-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認 Host 收到該 vector 後，實際輪詢的是哪條 CQ。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-287" data-question="287"><h2><a class="qa-qid" href="#q-287">Q287</a> 多條 CQ 共用 Vector 與獨立 Vector 有何不同？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-287-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-287-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>共用 vector 節省中斷資源，但 Host 收到通知後可能需要查多條 CQ；獨立 vector 較容易分散處理。</p>
</li>
<li id="q-287-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>合併門檻以 vector 為單位，同 vector 的多條 CQ 可能共同參與通知判斷。</p>
</li>
<li id="q-287-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查目前模式的 vector 能力與已建立 CQ 的 IV／IEN。</p>
</li>
<li id="q-287-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CQE 仍以 SQID、CID 識別命令，中斷訊息不攜帶每筆命令的完整身分。</p>
</li>
<li id="q-287-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>建立 vector→CQ 清單，收到通知後檢查相關 CQ，處理有效 Phase 的 entries，再更新各自 Head Doorbell。</p>
</li>
<li id="q-287-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>兩條 CQ 共用 IV3 時，一次中斷可引導 Host 處理兩邊多筆完成；不能期待每條 CQ 各一個通知。</p>
</li>
<li id="q-287-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>沒有一個通用「中斷數必須等於 CQE 數」規則；共用加上合併會讓兩者自然不同。</p>
</li>
<li id="q-287-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-287-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Completion 中斷與 Asynchronous Event Request 是不同機制。 <a class="qa-rule-link" href="#common-interrupt_op-9">本冊完整規則</a></p>
</li>
<li id="q-287-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>合法中斷設定與傳送本身不要求新增 Error Information。 <a class="qa-rule-link" href="#common-interrupt_op-10">本冊完整規則</a></p>
</li>
<li id="q-287-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>中斷不逐次記入 PEL。 <a class="qa-rule-link" href="#common-interrupt_op-11">本冊完整規則</a></p>
</li>
<li id="q-287-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後原 I/O queues 失效，CQ 與 vector 關係需隨 queue 重建。 <a class="qa-rule-link" href="#common-interrupt_op-12">本冊完整規則</a></p>
</li>
<li id="q-287-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新建立受影響 controller 的 queue、vector 關聯與需要的設定。 <a class="qa-rule-link" href="#common-interrupt_op-13">本冊完整規則</a></p>
</li>
<li id="q-287-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新配置中斷模式與 queues，再讀回或設定所需 Feature。 <a class="qa-rule-link" href="#common-interrupt_op-14">本冊完整規則</a></p>
</li>
<li id="q-287-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 vector 可服務多條 CQ，遮蔽或變更該 vector 的合併設定會影響這些 CQ 的通知。 <a class="qa-rule-link" href="#common-interrupt_op-15">本冊完整規則</a></p>
</li>
<li id="q-287-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>比較延遲與公平性時，分別統計每條 CQ 的寫入及 Host 處理時間，避免只看共用 vector 次數。</p>
</li>
<li id="q-287-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查共用關係是否完整，尤其有沒有漏查其中一條 CQ。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-288" data-question="288"><h2><a class="qa-qid" href="#q-288">Q288</a> Interrupt Coalescing 的 Threshold 與 Time 如何作用？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-288-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-288-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>合併多筆完成通知可減少 Host 中斷開銷，但可能增加通知延遲；CQE 本身仍可先寫入。</p>
</li>
<li id="q-288-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>FID08h 僅適用 I/O queues，不適用 Admin CQ。</p>
</li>
<li id="q-288-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Get／Set FID08h 取得或設定 TIME 與 THR；再查各 vector 的 FID09h.CD。</p>
</li>
<li id="q-288-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>TIME[15:8] 單位 100µs；THR[7:0] 是 zero-based 建議最小完成數。</p>
</li>
<li id="q-288-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先確保兩欄非零且 CD=0，再以固定 workload 比較通知與 CQE 時間。</p>
</li>
<li id="q-288-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>TIME=5、THR=7 表示 500µs 與 8 筆完成的建議值；不是 controller 必須恰好等滿兩者才發通知。</p>
</li>
<li id="q-288-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>PCIe 規範允許實作選擇合併算法，甚至不實作合併；不能因提早或稍晚於建議值就單獨判違規。</p>
</li>
<li id="q-288-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-288-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Completion 中斷與 Asynchronous Event Request 是不同機制。 <a class="qa-rule-link" href="#common-interrupt_op-9">本冊完整規則</a></p>
</li>
<li id="q-288-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>合法中斷設定與傳送本身不要求新增 Error Information。 <a class="qa-rule-link" href="#common-interrupt_op-10">本冊完整規則</a></p>
</li>
<li id="q-288-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>中斷不逐次記入 PEL。 <a class="qa-rule-link" href="#common-interrupt_op-11">本冊完整規則</a></p>
</li>
<li id="q-288-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後原 I/O queues 失效，CQ 與 vector 關係需隨 queue 重建。 <a class="qa-rule-link" href="#common-interrupt_op-12">本冊完整規則</a></p>
</li>
<li id="q-288-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新建立受影響 controller 的 queue、vector 關聯與需要的設定。 <a class="qa-rule-link" href="#common-interrupt_op-13">本冊完整規則</a></p>
</li>
<li id="q-288-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新配置中斷模式與 queues，再讀回或設定所需 Feature。 <a class="qa-rule-link" href="#common-interrupt_op-14">本冊完整規則</a></p>
</li>
<li id="q-288-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 vector 可服務多條 CQ，遮蔽或變更該 vector 的合併設定會影響這些 CQ 的通知。 <a class="qa-rule-link" href="#common-interrupt_op-15">本冊完整規則</a></p>
</li>
<li id="q-288-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Host 更新 CQ Head 可讓計時或門檻重新開始；持續處理某 vector 的 workload 可能持續延後新通知。</p>
</li>
<li id="q-288-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認測到的是 CQE 寫入延遲，還是中斷通知延遲。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-289" data-question="289"><h2><a class="qa-qid" href="#q-289">Q289</a> 如何停用 Interrupt Coalescing？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-289-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-289-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>停用合併讓通知不再套用聚合延遲，並不是關閉中斷。</p>
</li>
<li id="q-289-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>FID08h 影響 controller 的 I/O 中斷設定；FID09h.CD 可只停用指定 vector 的合併。</p>
</li>
<li id="q-289-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀 FID08h、FID09h 及 CQ.IEN，確認目前設定與通知路徑。</p>
</li>
<li id="q-289-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>TIME=0 或 THR=0 任一成立就隱含停用合併；CD=1 則禁止對該 vector 套用合併設定。</p>
</li>
<li id="q-289-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>需要全部停用時設定 FID08h；只停一條 vector 時，先有關聯 I/O CQ，再設定 FID09h。</p>
</li>
<li id="q-289-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>設定後 Get 讀回正確；有可通知的完成時，依模式與 mask 判斷中斷，而非仍等待原聚合門檻。</p>
</li>
<li id="q-289-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>即使 THR=0 的一般數量編碼看似 1，這裡仍有明確的停用規則，不能忽略。</p>
</li>
<li id="q-289-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-289-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Completion 中斷與 Asynchronous Event Request 是不同機制。 <a class="qa-rule-link" href="#common-interrupt_op-9">本冊完整規則</a></p>
</li>
<li id="q-289-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>合法中斷設定與傳送本身不要求新增 Error Information。 <a class="qa-rule-link" href="#common-interrupt_op-10">本冊完整規則</a></p>
</li>
<li id="q-289-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>中斷不逐次記入 PEL。 <a class="qa-rule-link" href="#common-interrupt_op-11">本冊完整規則</a></p>
</li>
<li id="q-289-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後原 I/O queues 失效，CQ 與 vector 關係需隨 queue 重建。 <a class="qa-rule-link" href="#common-interrupt_op-12">本冊完整規則</a></p>
</li>
<li id="q-289-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新建立受影響 controller 的 queue、vector 關聯與需要的設定。 <a class="qa-rule-link" href="#common-interrupt_op-13">本冊完整規則</a></p>
</li>
<li id="q-289-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新配置中斷模式與 queues，再讀回或設定所需 Feature。 <a class="qa-rule-link" href="#common-interrupt_op-14">本冊完整規則</a></p>
</li>
<li id="q-289-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 vector 可服務多條 CQ，遮蔽或變更該 vector 的合併設定會影響這些 CQ 的通知。 <a class="qa-rule-link" href="#common-interrupt_op-15">本冊完整規則</a></p>
</li>
<li id="q-289-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>關閉合併不保證每筆 CQE 都對應一次獨立中斷；共用 vector 與 Host 處理中的行為仍存在。</p>
</li>
<li id="q-289-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是不是把 CD=1 誤當成 vector 被遮蔽。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-290" data-question="290"><h2><a class="qa-qid" href="#q-290">Q290</a> FID09h 是遮蔽中斷嗎？真正的 Mask 要如何設定？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-290-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-290-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>原題把 Interrupt Vector Configuration 當成 mask；實際上 FID09h 的 CD 只控制該 vector 是否使用合併。</p>
</li>
<li id="q-290-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Mask 阻止中斷送出，影響所有使用該 vector 的 CQ 通知。</p>
</li>
<li id="q-290-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先確認目前是 pin-based、MSI 還是 MSI-X，才能選正確的 mask 介面。</p>
</li>
<li id="q-290-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Pin／MSI 用 INTMS 寫 1 設 mask、INTMC 寫 1 清 mask；MSI-X 用 Function Mask 與 Table 的 Vector Mask。</p>
</li>
<li id="q-290-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先保留原設定，再遮蔽、處理 CQ、更新 Head，最後解除遮蔽並檢查是否仍有待處理完成。</p>
</li>
<li id="q-290-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>INTMC 對目標 bit 寫 1 才解除，寫 0 沒有作用；這和一般「寫 0 就是清除」的 Register 不同。</p>
</li>
<li id="q-290-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>MSI-X 模式下 Host 不得存取 INTMS／INTMC，若違反，其結果未定義，不能編造必定的 NVMe Status。</p>
</li>
<li id="q-290-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>Mask Register 讀寫沒有 NVMe CQE，DNR／More 不適用；如果同時用 Get／Set FID09h 查合併，只有那些命令才有 CQE。</p>
</li>
<li id="q-290-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Completion 中斷與 Asynchronous Event Request 是不同機制。 <a class="qa-rule-link" href="#common-interrupt_op-9">本冊完整規則</a></p>
</li>
<li id="q-290-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>合法中斷設定與傳送本身不要求新增 Error Information。 <a class="qa-rule-link" href="#common-interrupt_op-10">本冊完整規則</a></p>
</li>
<li id="q-290-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>中斷不逐次記入 PEL。 <a class="qa-rule-link" href="#common-interrupt_op-11">本冊完整規則</a></p>
</li>
<li id="q-290-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後原 I/O queues 失效，CQ 與 vector 關係需隨 queue 重建。 <a class="qa-rule-link" href="#common-interrupt_op-12">本冊完整規則</a></p>
</li>
<li id="q-290-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新建立受影響 controller 的 queue、vector 關聯與需要的設定。 <a class="qa-rule-link" href="#common-interrupt_op-13">本冊完整規則</a></p>
</li>
<li id="q-290-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新配置中斷模式與 queues，再讀回或設定所需 Feature。 <a class="qa-rule-link" href="#common-interrupt_op-14">本冊完整規則</a></p>
</li>
<li id="q-290-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 vector 可服務多條 CQ，遮蔽或變更該 vector 的合併設定會影響這些 CQ 的通知。 <a class="qa-rule-link" href="#common-interrupt_op-15">本冊完整規則</a></p>
</li>
<li id="q-290-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Get FID09h.CD 只能證明合併設定，不能證明 MSI-X table 已解除 mask。</p>
</li>
<li id="q-290-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先讀目前模式及真正的 mask 位元。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-291" data-question="291"><h2><a class="qa-qid" href="#q-291">Q291</a> Vector 被遮蔽時，Controller 還能寫 CQE 嗎？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-291-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-291-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Mask 控制通知，並不暫停命令執行或凍結 CQ。</p>
</li>
<li id="q-291-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>所有使用該 vector 的 CQ 都可能繼續累積完成，直到各自空間不足。</p>
</li>
<li id="q-291-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀實際 mask、CQ.IEN、CQ 位置與 Phase；MSI-X 可另看 PBA。</p>
</li>
<li id="q-291-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Controller 仍依正常規則寫 CQE；MSI-X 因 mask 不能送出的中斷會以對應 pending bit 表示。</p>
</li>
<li id="q-291-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>遮蔽後可用合法的 CQ 輪詢確認完成，處理後仍需更新 Head Doorbell 釋放空間。</p>
</li>
<li id="q-291-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>看見新 Phase 的 CQE 卻沒有通知，在 mask 尚未解除時可能完全正常。</p>
</li>
<li id="q-291-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>CQ Full 是空間問題，與 mask 不同；長期不處理完成會間接讓 CQ 滿，但不是 mask 直接禁止寫入。</p>
</li>
<li id="q-291-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-291-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Completion 中斷與 Asynchronous Event Request 是不同機制。 <a class="qa-rule-link" href="#common-interrupt_op-9">本冊完整規則</a></p>
</li>
<li id="q-291-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>合法中斷設定與傳送本身不要求新增 Error Information。 <a class="qa-rule-link" href="#common-interrupt_op-10">本冊完整規則</a></p>
</li>
<li id="q-291-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>中斷不逐次記入 PEL。 <a class="qa-rule-link" href="#common-interrupt_op-11">本冊完整規則</a></p>
</li>
<li id="q-291-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後原 I/O queues 失效，CQ 與 vector 關係需隨 queue 重建。 <a class="qa-rule-link" href="#common-interrupt_op-12">本冊完整規則</a></p>
</li>
<li id="q-291-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新建立受影響 controller 的 queue、vector 關聯與需要的設定。 <a class="qa-rule-link" href="#common-interrupt_op-13">本冊完整規則</a></p>
</li>
<li id="q-291-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新配置中斷模式與 queues，再讀回或設定所需 Feature。 <a class="qa-rule-link" href="#common-interrupt_op-14">本冊完整規則</a></p>
</li>
<li id="q-291-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 vector 可服務多條 CQ，遮蔽或變更該 vector 的合併設定會影響這些 CQ 的通知。 <a class="qa-rule-link" href="#common-interrupt_op-15">本冊完整規則</a></p>
</li>
<li id="q-291-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>不要用「沒有 interrupt」推導「沒有完成」；兩者需分開觀察。</p>
</li>
<li id="q-291-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先讀 CQ 的有效 Phase，再看通知設定。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-292" data-question="292"><h2><a class="qa-qid" href="#q-292">Q292</a> 解除 Mask 後如何處理累積完成？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-292-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-292-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>一個 pending 中斷可以代表多筆完成，Host 仍必須從 CQ 逐筆取得真正結果。</p>
</li>
<li id="q-292-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>共享 vector 時，要處理所有關聯且可能有新完成的 CQ。</p>
</li>
<li id="q-292-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>核對 MSI-X 的 Function／Vector Mask、PBA，或 pin／MSI 的 INTM 及對應 CQ。</p>
</li>
<li id="q-292-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>MSI-X 兩層 mask 都清除後，待送中斷才可送出；只清其中一層仍可能不通知。</p>
</li>
<li id="q-292-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>解除遮蔽後讀 CQ、依 Phase 處理，再更新各 Head；處理與重新掛通知間要避免漏掉剛到的新 CQE。</p>
</li>
<li id="q-292-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>累積 10 筆完成可能由一次通知引導 Host 全部處理，不要求補送 10 次歷史中斷。</p>
</li>
<li id="q-292-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>INTM 遮蔽 MSI 時，對應 MSI Capability pending 不會因此設起；不能把 MSI-X PBA 規則原封套用。</p>
</li>
<li id="q-292-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-292-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Completion 中斷與 Asynchronous Event Request 是不同機制。 <a class="qa-rule-link" href="#common-interrupt_op-9">本冊完整規則</a></p>
</li>
<li id="q-292-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>合法中斷設定與傳送本身不要求新增 Error Information。 <a class="qa-rule-link" href="#common-interrupt_op-10">本冊完整規則</a></p>
</li>
<li id="q-292-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>中斷不逐次記入 PEL。 <a class="qa-rule-link" href="#common-interrupt_op-11">本冊完整規則</a></p>
</li>
<li id="q-292-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後原 I/O queues 失效，CQ 與 vector 關係需隨 queue 重建。 <a class="qa-rule-link" href="#common-interrupt_op-12">本冊完整規則</a></p>
</li>
<li id="q-292-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新建立受影響 controller 的 queue、vector 關聯與需要的設定。 <a class="qa-rule-link" href="#common-interrupt_op-13">本冊完整規則</a></p>
</li>
<li id="q-292-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新配置中斷模式與 queues，再讀回或設定所需 Feature。 <a class="qa-rule-link" href="#common-interrupt_op-14">本冊完整規則</a></p>
</li>
<li id="q-292-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 vector 可服務多條 CQ，遮蔽或變更該 vector 的合併設定會影響這些 CQ 的通知。 <a class="qa-rule-link" href="#common-interrupt_op-15">本冊完整規則</a></p>
</li>
<li id="q-292-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>以「所有有效 CQE 是否被處理」判斷完整性，不以通知次數等於命令數判斷。</p>
</li>
<li id="q-292-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否還有另一層 mask 或漏列的共用 CQ。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-293" data-question="293"><h2><a class="qa-qid" href="#q-293">Q293</a> 已被 CQ 使用的 Vector 可以修改設定嗎？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-293-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-293-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>需先分清修改合併、修改 mask，還是改變 CQ 的 vector 關聯，這不是同一件事。</p>
</li>
<li id="q-293-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>FID09h 改指定 vector 的合併設定，會影響目前共用該 vector 的所有 CQ。</p>
</li>
<li id="q-293-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>設定 FID09h 前，該 IV 必須已關聯一條存在的 I/O CQ。</p>
</li>
<li id="q-293-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CD=1 停用合併，CD=0 使用全域合併；它沒有修改 Create CQ.IV 的功能。</p>
</li>
<li id="q-293-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>保留 CQ 關聯，Set FID09h 後 Get 相同 IV；若需要換 CQ 的 IV，依合法 queue 生命週期重建該關聯。</p>
</li>
<li id="q-293-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>已存在 CQ 正是設定 FID09h 的前提，不是禁止修改的理由。</p>
</li>
<li id="q-293-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>IV 非法或未關聯存在的 I/O CQ 時，controller 應回 Invalid Field；這裡的 should 不等於強制唯一結果。</p>
</li>
<li id="q-293-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-293-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Completion 中斷與 Asynchronous Event Request 是不同機制。 <a class="qa-rule-link" href="#common-interrupt_op-9">本冊完整規則</a></p>
</li>
<li id="q-293-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>合法中斷設定與傳送本身不要求新增 Error Information。 <a class="qa-rule-link" href="#common-interrupt_op-10">本冊完整規則</a></p>
</li>
<li id="q-293-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>中斷不逐次記入 PEL。 <a class="qa-rule-link" href="#common-interrupt_op-11">本冊完整規則</a></p>
</li>
<li id="q-293-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後原 I/O queues 失效，CQ 與 vector 關係需隨 queue 重建。 <a class="qa-rule-link" href="#common-interrupt_op-12">本冊完整規則</a></p>
</li>
<li id="q-293-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新建立受影響 controller 的 queue、vector 關聯與需要的設定。 <a class="qa-rule-link" href="#common-interrupt_op-13">本冊完整規則</a></p>
</li>
<li id="q-293-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新配置中斷模式與 queues，再讀回或設定所需 Feature。 <a class="qa-rule-link" href="#common-interrupt_op-14">本冊完整規則</a></p>
</li>
<li id="q-293-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 vector 可服務多條 CQ，遮蔽或變更該 vector 的合併設定會影響這些 CQ 的通知。 <a class="qa-rule-link" href="#common-interrupt_op-15">本冊完整規則</a></p>
</li>
<li id="q-293-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>比較前後結果時，保存其他共用 CQ 與 mask 狀態，避免把外部條件變更誤算成 Feature 行為。</p>
</li>
<li id="q-293-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認真正想修改的是 CD、mask，還是 CQ.IV。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-294" data-question="294"><h2><a class="qa-qid" href="#q-294">Q294</a> Reset 後中斷設定要如何恢復？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-294-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-294-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Queue 與 vector 的關聯會隨 queue 生命週期結束；PCIe 模式與 mask 是否保留則依 reset 來源不同。</p>
</li>
<li id="q-294-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>只重設一個 controller 與更大範圍 reset 不同，不能重配未受影響的另一台 controller。</p>
</li>
<li id="q-294-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先查 CC／CSTS 與 PCIe interrupt mode，再讀需要的 Feature Current。</p>
</li>
<li id="q-294-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>FID08h 的 TIME／THR reset 值 0；FID09h 預設允許合併，但當全域合併停用時，不會因此自動啟用延遲。</p>
</li>
<li id="q-294-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>恢復 Admin 通道、配置 vectors、重建 CQ／SQ，再設定 FID09h 與需要的 FID08h。</p>
</li>
<li id="q-294-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>新的合法 CQE 可以經正確 vector 被 Host 找到，舊 CQE 不應混進新 queue 的完成追蹤。</p>
</li>
<li id="q-294-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>FID09h 在 CQ 尚未重建前就設定，可能觸發未關聯 IV 的錯誤。</p>
</li>
<li id="q-294-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-294-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Completion 中斷與 Asynchronous Event Request 是不同機制。 <a class="qa-rule-link" href="#common-interrupt_op-9">本冊完整規則</a></p>
</li>
<li id="q-294-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>合法中斷設定與傳送本身不要求新增 Error Information。 <a class="qa-rule-link" href="#common-interrupt_op-10">本冊完整規則</a></p>
</li>
<li id="q-294-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>中斷不逐次記入 PEL。 <a class="qa-rule-link" href="#common-interrupt_op-11">本冊完整規則</a></p>
</li>
<li id="q-294-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後原 I/O queues 失效，CQ 與 vector 關係需隨 queue 重建。 <a class="qa-rule-link" href="#common-interrupt_op-12">本冊完整規則</a></p>
</li>
<li id="q-294-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新建立受影響 controller 的 queue、vector 關聯與需要的設定。 <a class="qa-rule-link" href="#common-interrupt_op-13">本冊完整規則</a></p>
</li>
<li id="q-294-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新配置中斷模式與 queues，再讀回或設定所需 Feature。 <a class="qa-rule-link" href="#common-interrupt_op-14">本冊完整規則</a></p>
</li>
<li id="q-294-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 vector 可服務多條 CQ，遮蔽或變更該 vector 的合併設定會影響這些 CQ 的通知。 <a class="qa-rule-link" href="#common-interrupt_op-15">本冊完整規則</a></p>
</li>
<li id="q-294-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>模式切換也可能失去合併設定，需重新設定；不能只測 CC.EN reset 就推論 Power Cycle。</p>
</li>
<li id="q-294-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先核對 reset 類型及新 CQ 建立成功的時點。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-295" data-question="295"><h2><a class="qa-qid" href="#q-295">Q295</a> Queue 刪除後如何回收中斷資源？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-295-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-295-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>刪除 CQ 結束一個完成目的地，不代表 Host 配置的 PCIe vector 自動從整個 function 消失。</p>
</li>
<li id="q-295-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>同一 vector 可能仍被其他 CQ 使用，因此要按關聯計數回收。</p>
</li>
<li id="q-295-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>保存 SQ→CQ→IV 關係與尚未完成命令，不能只列 SQ 編號。</p>
</li>
<li id="q-295-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>先刪依賴的 SQ 並等待完成，再刪 CQ；成功後解除 Host 對該 CQ 的處理資料。</p>
</li>
<li id="q-295-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>最後檢查同 IV 是否還有其他 CQ，才決定移除 handler 或釋放 Host 中斷資源。</p>
</li>
<li id="q-295-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>CQ1、CQ2 共用 IV3，刪 CQ1 後 IV3 仍需服務 CQ2；不應把 CQ2 的通知一起關掉。</p>
</li>
<li id="q-295-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>CQ 仍被 SQ 引用時不能合法刪除；成功刪除前也不能提前回收 CQ 記憶體。</p>
</li>
<li id="q-295-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-295-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Completion 中斷與 Asynchronous Event Request 是不同機制。 <a class="qa-rule-link" href="#common-interrupt_op-9">本冊完整規則</a></p>
</li>
<li id="q-295-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>合法中斷設定與傳送本身不要求新增 Error Information。 <a class="qa-rule-link" href="#common-interrupt_op-10">本冊完整規則</a></p>
</li>
<li id="q-295-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>中斷不逐次記入 PEL。 <a class="qa-rule-link" href="#common-interrupt_op-11">本冊完整規則</a></p>
</li>
<li id="q-295-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後原 I/O queues 失效，CQ 與 vector 關係需隨 queue 重建。 <a class="qa-rule-link" href="#common-interrupt_op-12">本冊完整規則</a></p>
</li>
<li id="q-295-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新建立受影響 controller 的 queue、vector 關聯與需要的設定。 <a class="qa-rule-link" href="#common-interrupt_op-13">本冊完整規則</a></p>
</li>
<li id="q-295-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新配置中斷模式與 queues，再讀回或設定所需 Feature。 <a class="qa-rule-link" href="#common-interrupt_op-14">本冊完整規則</a></p>
</li>
<li id="q-295-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 vector 可服務多條 CQ，遮蔽或變更該 vector 的合併設定會影響這些 CQ 的通知。 <a class="qa-rule-link" href="#common-interrupt_op-15">本冊完整規則</a></p>
</li>
<li id="q-295-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>同時比對 queue 刪除 CQE、Host 關聯清單與剩餘 CQ 通知，避免資源洩漏或過早釋放。</p>
</li>
<li id="q-295-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認 vector 是獨占還是共用。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-296" data-question="296"><h2><a class="qa-qid" href="#q-296">Q296</a> 如何比對 Interrupt、CQ 與實際完成行為？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-296-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-296-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>將命令完成與通知分開，才能定位是 controller 沒完成，還是 Host 沒被通知或沒處理。</p>
</li>
<li id="q-296-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>追蹤一條完整路徑：SQ 的命令、關聯 CQ、使用的 vector 與 Host 處理程序。</p>
</li>
<li id="q-296-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀 CQ.IEN／IV、FID08h、FID09h、真實 mask 與 CQ Phase。</p>
</li>
<li id="q-296-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>保存提交時間、CQE 出現時間、通知時間與 Head 更新時間，四者不是同一時點。</p>
</li>
<li id="q-296-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先確認新 CQE，再查是否應通知；最後核對 Host 是否處理並釋放空間。</p>
</li>
<li id="q-296-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>完成已存在、mask=1 且 Host 用輪詢處理，是可以成立的正常案例；中斷不是完成有效性的唯一證據。</p>
</li>
<li id="q-296-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>如果 Phase 不匹配、查錯 CQ 或漏更新 Head，先修正 Host 證據；不能只因未收到 interrupt 就判 SSD 丟命令。</p>
</li>
<li id="q-296-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-296-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Completion 中斷與 Asynchronous Event Request 是不同機制。 <a class="qa-rule-link" href="#common-interrupt_op-9">本冊完整規則</a></p>
</li>
<li id="q-296-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>合法中斷設定與傳送本身不要求新增 Error Information。 <a class="qa-rule-link" href="#common-interrupt_op-10">本冊完整規則</a></p>
</li>
<li id="q-296-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>中斷不逐次記入 PEL。 <a class="qa-rule-link" href="#common-interrupt_op-11">本冊完整規則</a></p>
</li>
<li id="q-296-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後原 I/O queues 失效，CQ 與 vector 關係需隨 queue 重建。 <a class="qa-rule-link" href="#common-interrupt_op-12">本冊完整規則</a></p>
</li>
<li id="q-296-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新建立受影響 controller 的 queue、vector 關聯與需要的設定。 <a class="qa-rule-link" href="#common-interrupt_op-13">本冊完整規則</a></p>
</li>
<li id="q-296-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新配置中斷模式與 queues，再讀回或設定所需 Feature。 <a class="qa-rule-link" href="#common-interrupt_op-14">本冊完整規則</a></p>
</li>
<li id="q-296-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 vector 可服務多條 CQ，遮蔽或變更該 vector 的合併設定會影響這些 CQ 的通知。 <a class="qa-rule-link" href="#common-interrupt_op-15">本冊完整規則</a></p>
</li>
<li id="q-296-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>用同一次測試的設定快照與時間線互相比對，避免拿測試後讀值解釋測試中行為。</p>
</li>
<li id="q-296-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先從該命令的 CQ 位置與 Phase 查起。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-command-8"><h3>命令完成、事件與紀錄 · DNR 與 More 應如何設定？</h3><p>只有收到 CQE，才有 DNR 與 More 可供判讀。DNR=1 表示相同命令即使重送到此 NVM subsystem 的任一 controller，仍預期會失敗；DNR=0 則只表示可能成功。除非個別錯誤條件另有明定，不能只看 Status 名稱就要求 DNR=1。More=1 表示 Error Information Log 有這筆命令的補充資訊。SCT=SC=0 時，DNR 應為 0。</p></article>
<article id="common-interrupt_op-9"><h3>本主題的共用條件 · 是否產生 Asynchronous Event？</h3><p>Completion 中斷與 Asynchronous Event Request 是不同機制。AER 本身完成時也會產生 CQE，但不能把一般 I/O interrupt 當成新的 NVMe 非同步事件。</p></article>
<article id="common-interrupt_op-10"><h3>本主題的共用條件 · 是否更新 Error Information Log 或其他 Log？</h3><p>合法中斷設定與傳送本身不要求新增 Error Information。設定命令若失敗，才依錯誤條件比對；CQE 已寫入而 Host 沒處理，也不自動構成 controller 的 Error Log entry。</p></article>
<article id="common-interrupt_op-11"><h3>本主題的共用條件 · 是否記錄於 Persistent Event Log？</h3><p>中斷不逐次記入 PEL。Feature 設定是否記錄仍須符合該 FID 的 Set Feature Event 支援與成功變更條件，不能用 PEL 計算中斷總數。</p></article>
<article id="common-interrupt_op-12"><h3>本主題的共用條件 · Controller Reset 後是否保留或繼續？</h3><p>CLR 後原 I/O queues 失效，CQ 與 vector 關係需隨 queue 重建。FID08h 的 reset 值為 0，FID09h 預設不停用合併；PCIe mask 與中斷模式則須依實際 reset 來源核對，不能將 CC.EN 與 FLR 混用。</p></article>
<article id="common-interrupt_op-13"><h3>本主題的共用條件 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>Subsystem Reset 後重新建立受影響 controller 的 queue、vector 關聯與需要的設定。不能只因同一個 vector 編號還存在，就沿用舊 CQ 的處理資料。</p></article>
<article id="common-interrupt_op-14"><h3>本主題的共用條件 · Power Cycle 後是否保留或繼續？</h3><p>Power Cycle 後重新配置中斷模式與 queues，再讀回或設定所需 Feature。切換中斷模式時，規範也不要求保留原 coalescing 設定，建議重新設定。</p></article>
<article id="common-interrupt_op-15"><h3>本主題的共用條件 · 是否影響其他 Controller 或 Namespace？</h3><p>同一 vector 可服務多條 CQ，遮蔽或變更該 vector 的合併設定會影響這些 CQ 的通知。不同 controller 的相同 vector 數值不代表同一份 NVMe 設定。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-interruptmask"><strong>Base 2.4 · §3.1.4 (INTMS, INTMC)</strong><br>文件頁 59 · PDF 85 · Figure 39–40</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>文件頁 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>文件頁 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>文件頁 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-interruptfeature"><strong>Base 2.4 · §5.2.30.2.1–5.2.30.2.2</strong><br>文件頁 514–515 · PDF 540–541 · Figure 543–544</li>
<li id="ref-create"><strong>Base 2.4 · §5.3.1–5.3.2</strong><br>文件頁 527–531 · PDF 553–557 · Figure 571–579</li>
<li id="ref-delete"><strong>Base 2.4 · §5.3.3–5.3.4</strong><br>文件頁 531–532 · PDF 557–558 · Figure 580–583</li>
<li id="ref-interruptfull"><strong>PCIe Transport 1.4 · §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</strong><br>文件頁 13–16, 24–26 · PDF 13–16, 24–26 · Figure 9, 42–48</li>
</ul><h3>需要看欄位圖時</h3><p>以下連結可開啟對應的圖表教學，查閱欄位及判讀方式。每張圖保留固定的教學位置，方便之後反覆查詢。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/features/zh-tw/#figure-b543">Base 2.4 Figure 543 · Interrupt Coalescing – Command Dword 11</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/interrupts/en/">English</a><a href="/DOCS/nvme-question-bank/interrupts.html">繁中教學 HTML</a></nav>
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
