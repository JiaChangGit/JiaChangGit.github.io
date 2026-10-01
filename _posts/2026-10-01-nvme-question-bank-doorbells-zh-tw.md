---
layout: post
title: "NVMe 自問自答題庫：Doorbell、Queue Full 與 Wrap-around"
date: 2026-10-01 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/doorbells/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/doorbells/en/">English</a><a href="/DOCS/nvme-question-bank/doorbells.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–68</p>
<header><p class="qa-range">Q22–Q30</p><h1>Doorbell、Queue Full 與 Wrap-around</h1><p class="qr-intro">Doorbell 告訴另一端指標移到哪裡；Phase 告訴 Host，這個 CQ 位置是不是新一輪的完成。兩者一起使用，才不會把繞回誤判成倒退，或把舊完成誤判成新完成。</p><p>先練習，再展開每題的 17 項解答。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可以指定的一份邏輯儲存空間。多個 controller 可以屬於同一 NVM subsystem（包含 controller 與非揮發儲存資源的整體）。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue 是提交佇列，Completion Queue 是完成佇列；SQE／CQE 是其中的一筆 entry。QID 識別 queue，CID 識別同一 SQ 內尚未完成的命令，NSID 識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 是可存取的控制或狀態欄位；Identify 查物件能力與屬性；Feature 查／設工作設定；Log Page 回報指定種類的狀態或紀錄。FID、LID、CNS、CSI 分別選 Feature、Log、Identify 結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 是第幾筆，通常由 0 起算；offset 是離起點多遠，要看單位。zero-based 數量欄位的實際數量＝編碼＋1，但不是每個寫 0 的欄位都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 指一項操作影響的物件範圍。retention 是狀態是否保留。Controller Reset（清 CC.EN）是一種 Controller Level Reset，簡稱 CLR；同一類 CLR 的不同觸發方式，Register 保留規則仍可能不同。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>8 格 CQ：把繞回與 Phase 放在同一張表</h2><p class="qa-takeaway">位置回到 0 不代表舊資料重新有效；Host 還要比對這一輪預期的 Phase。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">時點</th><th scope="col">Host 下一格／預期 Phase</th><th scope="col">讀取結果與動作</th></tr></thead><tbody><tr><td>初始化</td><td>位置 0，預期 P=1；記憶體 P 初始化為 0</td><td>目前沒有新完成</td></tr><tr><td>第一輪末端</td><td>位置 7，預期 P=1</td><td>讀到 P=1：處理 CQE，下一格回 0，預期改 0</td></tr><tr><td>第二輪起點</td><td>位置 0，預期 P=0</td><td>若仍是舊 P=1，不處理；讀到新 P=0 才處理</td></tr><tr><td>通知已消費</td><td>CQ Head 從 7 更新成 2</td><td>表示消費位置 7、0、1，共 3 格；不是倒退 5 格</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>算指標距離時使用 (2−7+8) mod 8=3。Doorbell 值是位置 2，並不是「新增釋放 2 格」。CQE 的 Phase 是有效性判斷；CQ Head Doorbell 則把已消費位置告知 controller，兩者不可互相代替。</p>
<p class="qa-citations">來源：<a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-022">Q22 · Host 應在什麼時候更新 SQ Tail Doorbell 與 CQ Head Doorbell？</a></li>
<li><a href="#q-023">Q23 · Doorbell 值重複、倒退、超過 Queue 範圍或寫到錯誤 QID 時，可能造成什麼問題？</a></li>
<li><a href="#q-024">Q24 · Host 如何根據 CAP.DSTRD 計算每個 SQ 與 CQ Doorbell 的位置？</a></li>
<li><a href="#q-025">Q25 · Host 能否存取未建立、已刪除或 Controller 未 Enable 時的 Queue Doorbell？</a></li>
<li><a href="#q-026">Q26 · SQ Tail 與 CQ Head 發生 Wrap-around 時，Host 與 Controller 應如何處理？</a></li>
<li><a href="#q-027">Q27 · CQ Wrap-around 後 Phase Tag 如何變化？Host 如何利用 Phase Tag 辨識新 Completion？</a></li>
<li><a href="#q-028">Q28 · CQ Full 通常如何形成？CQ Full 時 Controller 能否繼續處理相關 SQ？</a></li>
<li><a href="#q-029">Q29 · Host 釋放 CQ 空間後，Controller 應如何恢復 Command 處理？</a></li>
<li><a href="#q-030">Q30 · 多個 SQ 共用一個 CQ 時，Host 如何依 SQID 與 CID 辨識 Completion 來源？</a></li>
</ol></section>
<article class="qa-question" id="q-022" data-question="22"><h2><a class="qa-qid" href="#q-022">Q22</a> Host 應在什麼時候更新 SQ Tail Doorbell 與 CQ Head Doorbell？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-022-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-022-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>把 Host 已做完的記憶體工作通知 controller：SQ Tail 提交命令，CQ Head 釋放完成位置。</p>
</li>
<li id="q-022-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>每條 SQ／CQ 各有自己的 Doorbell；更新其中一條不會自動更新另一條。</p>
</li>
<li id="q-022-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>確認 queue 有效、controller ready、剩餘 slots 足夠，並依 CAP.DSTRD 找到正確 Register。</p>
</li>
<li id="q-022-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>SQ Tail 指向下一個可放 SQE 的 slot；CQ Head 指向下一個待消費 CQE。寫入的是新指標值，不是增加多少筆。</p>
</li>
<li id="q-022-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先寫完整 SQE 並完成平台要求的記憶體可見性，再更新 Tail；讀取並處理有效 CQE 後再更新 Head，可一次提交或確認多筆。</p>
</li>
<li id="q-022-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>controller 得知哪些命令可讀，以及哪些 CQ slots 可重用。CQ Head 前進不代表提交了新 I/O。</p>
</li>
<li id="q-022-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>未消費 CQE 就提前釋放位置，可能使資料被覆寫；未準備好 SQE 就提交，違反正確使用順序，不能期待一個固定錯誤 CQE。</p>
</li>
<li id="q-022-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>本次 MMIO 存取沒有 NVMe CQE，因此 DNR／More 不適用。 <a class="qa-rule-link" href="#common-register-8">本冊完整規則</a></p>
</li>
<li id="q-022-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Register 存取本身沒有成功事件；另有硬體錯誤時使用該事件的條件。 <a class="qa-rule-link" href="#common-register-9">本冊完整規則</a></p>
</li>
<li id="q-022-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>不逐次記錄 Register 讀寫；先保留 Register 值與時間，再取得可用的診斷紀錄。 <a class="qa-rule-link" href="#common-register-10">本冊完整規則</a></p>
</li>
<li id="q-022-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Register 存取不構成 PEL 事件；完成的 Reset 或支援的硬體錯誤另判斷。 <a class="qa-rule-link" href="#common-register-11">本冊完整規則</a></p>
</li>
<li id="q-022-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-022-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-022-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-022-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-022-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>把 Host 記憶體寫入、Tail 更新、CQE Phase 改變與 Head 更新排成時間線，四個動作各有不同用途。</p>
</li>
<li id="q-022-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否把 Doorbell 值寫成「本次筆數」，而不是 modulo queue size 的新索引。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-023" data-question="23"><h2><a class="qa-qid" href="#q-023">Q23</a> Doorbell 值重複、倒退、超過 Queue 範圍或寫到錯誤 QID 時，可能造成什麼問題？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-023-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-023-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>判斷指標移動是否合法，避免把環狀索引當成只會遞增的計數器。</p>
</li>
<li id="q-023-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>錯誤影響該 queue；若 CQ 共享，還會牽動使用它的 SQ。寫到不存在 queue 與有效 queue 的非法值要分開。</p>
</li>
<li id="q-023-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>需要 queue size、前次指標、可用／已消費 slots 與 QID 映射；只有新值不夠判斷。</p>
</li>
<li id="q-023-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>新值應在 0 到 size−1；同值沒有宣布新的 slots。較小值可能是合法 wrap，而非真正「倒退」。</p>
</li>
<li id="q-023-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>例：size=8，Tail 6→1 代表前進 3 slots，前提是有三個可用位置及有效 SQE。6→6 不能用來表示提交一整圈。</p>
</li>
<li id="q-023-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>合法移動讓 controller 辨識正確數量；Host 不應讀 Doorbell 回值驗證，讀回值是 vendor specific。</p>
</li>
<li id="q-023-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>有效 queue 上非法值有 Invalid Doorbell Write Value 的非同步錯誤處理；寫不存在 queue 的 Doorbell 結果 undefined。不要把事件資訊碼當成該 MMIO write 的 CQE Status。</p>
</li>
<li id="q-023-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>本次 MMIO 存取沒有 NVMe CQE，因此 DNR／More 不適用。 <a class="qa-rule-link" href="#common-register-8">本冊完整規則</a></p>
</li>
<li id="q-023-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Base §3.3.1.2 規定：非法 Doorbell 值且有 outstanding Asynchronous Event Request 時，張貼對應錯誤事件。受影響 SQ 可完成已取得命令，但不再取得新命令；Host 刪除並重建 queue。</p>
</li>
<li id="q-023-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>此錯誤事件屬 Error 類型，應依其指定的 Log 查補充資料；MMIO 寫入本身沒有 More 位元。不要把錯誤 QID 的 undefined 情況強行規定成一定有 Log。</p>
</li>
<li id="q-023-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Register 存取不構成 PEL 事件；完成的 Reset 或支援的硬體錯誤另判斷。 <a class="qa-rule-link" href="#common-register-11">本冊完整規則</a></p>
</li>
<li id="q-023-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-023-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-023-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-023-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-023-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>核對原指標、環大小與空間，而非只比新舊數字大小。錯誤事件與受影響 queue 的停止取新命令也應一起確認。</p>
</li>
<li id="q-023-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先算 (new−old+size) modulo size，並核對這個前進量是否真的合法。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-024" data-question="24"><h2><a class="qa-qid" href="#q-024">Q24</a> Host 如何根據 CAP.DSTRD 計算每個 SQ 與 CQ Doorbell 的位置？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-024-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-024-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>從 NVMe Register base 與 QID 找到唯一的 Doorbell 位址，避免通知錯 queue。</p>
</li>
<li id="q-024-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>計算以此 controller 的 MMIO base 為起點；不是相對某條 queue 的記憶體 base。</p>
</li>
<li id="q-024-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>PCI BAR0／BAR1 提供 NVMe Register 空間位置，CAP.DSTRD 提供相鄰 Doorbell stride。</p>
</li>
<li id="q-024-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>stride=4×2^DSTRD；SQy offset=1000h+2y×stride；CQy offset=1000h+(2y+1)×stride。每個 Doorbell 本身仍是 32 bits。</p>
</li>
<li id="q-024-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先取得映射 base，算 stride，再依 QID 選 SQ 或 CQ 公式，最後做合法寬度的 MMIO 存取。</p>
</li>
<li id="q-024-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例：DSTRD=2、QID=3，SQ offset=1060h、CQ offset=1070h。把各 offset 加到 controller base，才是完整位址。</p>
</li>
<li id="q-024-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>位址計算本身沒有 Status。錯位址可能指到別的有效 queue，甚至造成 undefined access，不能期待 controller 自動知道 Host 原本想寫哪條。</p>
</li>
<li id="q-024-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>本次 MMIO 存取沒有 NVMe CQE，因此 DNR／More 不適用。 <a class="qa-rule-link" href="#common-register-8">本冊完整規則</a></p>
</li>
<li id="q-024-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Register 存取本身沒有成功事件；另有硬體錯誤時使用該事件的條件。 <a class="qa-rule-link" href="#common-register-9">本冊完整規則</a></p>
</li>
<li id="q-024-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>不逐次記錄 Register 讀寫；先保留 Register 值與時間，再取得可用的診斷紀錄。 <a class="qa-rule-link" href="#common-register-10">本冊完整規則</a></p>
</li>
<li id="q-024-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Register 存取不構成 PEL 事件；完成的 Reset 或支援的硬體錯誤另判斷。 <a class="qa-rule-link" href="#common-register-11">本冊完整規則</a></p>
</li>
<li id="q-024-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-024-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-024-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-024-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-024-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>將計算結果與建立時 QID、映射 BAR 範圍核對。DSTRD 不是 bytes，也不是直接乘在 QID 上的係數。</p>
</li>
<li id="q-024-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認公式是否漏掉 SQ／CQ 交錯所需的 2y 與 2y+1。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-pciconfig">PCIe Transport 1.4 §3.8.1 (NVMe configuration access)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-025" data-question="25"><h2><a class="qa-qid" href="#q-025">Q25</a> Host 能否存取未建立、已刪除或 Controller 未 Enable 時的 Queue Doorbell？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-025-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-025-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>保護 queue 的有效使用期間：有 Register 位址不代表那條 queue 目前存在。</p>
</li>
<li id="q-025-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>每條 queue 必須在建立成功後使用，刪除成功或 controller reset 後停止沿用。</p>
</li>
<li id="q-025-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>檢查 Host 的 queue 存在紀錄、CC.EN、CSTS.RDY；不能從 Doorbell 讀回值判斷 queue 是否存在。</p>
</li>
<li id="q-025-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>SQyTDBL 與 CQyHDBL 只通知有效 queue 的新指標；Admin Q0 的有效環境來自 AQA／ASQ／ACQ 及初始化。</p>
</li>
<li id="q-025-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>建立並確認成功→使用→停止提交→Delete 成功→停止使用。Controller Reset 之後即使 QID 相同也重新經過建立。</p>
</li>
<li id="q-025-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功的生命周期管理不應對不存在 queue 寫 Doorbell；Doorbell 不會幫 Host 自動建立 queue。</p>
</li>
<li id="q-025-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>PCIe §3.1.2 將不存在 SQ／CQ 的 Doorbell 寫入列為 undefined；RDY=0 不符合命令提交前提。不能要求一定回 Invalid Queue Identifier 或某個 AER。</p>
</li>
<li id="q-025-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>本次 MMIO 存取沒有 NVMe CQE，因此 DNR／More 不適用。 <a class="qa-rule-link" href="#common-register-8">本冊完整規則</a></p>
</li>
<li id="q-025-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Register 存取本身沒有成功事件；另有硬體錯誤時使用該事件的條件。 <a class="qa-rule-link" href="#common-register-9">本冊完整規則</a></p>
</li>
<li id="q-025-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>不逐次記錄 Register 讀寫；先保留 Register 值與時間，再取得可用的診斷紀錄。 <a class="qa-rule-link" href="#common-register-10">本冊完整規則</a></p>
</li>
<li id="q-025-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Register 存取不構成 PEL 事件；完成的 Reset 或支援的硬體錯誤另判斷。 <a class="qa-rule-link" href="#common-register-11">本冊完整規則</a></p>
</li>
<li id="q-025-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-025-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-025-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-025-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-025-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>用 Create／Delete completion 的時間建立有效區間，再檢查 Doorbell 是否落在區間內。</p>
</li>
<li id="q-025-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否有其他 CPU 還持有已刪 queue 的舊引用。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-qattr">Base 2.4 §3.3.3–3.4.1</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-026" data-question="26"><h2><a class="qa-qid" href="#q-026">Q26</a> SQ Tail 與 CQ Head 發生 Wrap-around 時，Host 與 Controller 應如何處理？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-026-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-026-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>將固定大小記憶體重複作為環狀 queue 使用，不需要每走一圈重新建立。</p>
</li>
<li id="q-026-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>SQ Tail 由 Host 前進，CQ Head 也由 Host 前進；相對的 SQ Head、CQ Tail 是 controller 維護。</p>
</li>
<li id="q-026-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>使用實際 queue slots 數 N，也就是 QSIZE+1；不是拿 CAP.MQES 當每條 queue 的實際大小。</p>
</li>
<li id="q-026-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>每前進一步計算 (index+1) modulo N。Tail 是下一個寫入位置，Head 是下一個讀取位置，兩者相等表示空。</p>
</li>
<li id="q-026-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>從 N−1 前進到 0，保留實際前進筆數；SQ 不超過可用容量，CQ 不跳過尚未處理的 entry。</p>
</li>
<li id="q-026-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例：N=8，CQ Head 7→2 表示消費 slots 7、0、1 共 3 筆，不是倒退 5 筆。</p>
</li>
<li id="q-026-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>合法 wrap 不是錯誤；錯把 size 當最大索引而寫 N，才是超出 queue 範圍。非法指標的處理與第 23 題相同。</p>
</li>
<li id="q-026-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>本次 MMIO 存取沒有 NVMe CQE，因此 DNR／More 不適用。 <a class="qa-rule-link" href="#common-register-8">本冊完整規則</a></p>
</li>
<li id="q-026-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Register 存取本身沒有成功事件；另有硬體錯誤時使用該事件的條件。 <a class="qa-rule-link" href="#common-register-9">本冊完整規則</a></p>
</li>
<li id="q-026-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>不逐次記錄 Register 讀寫；先保留 Register 值與時間，再取得可用的診斷紀錄。 <a class="qa-rule-link" href="#common-register-10">本冊完整規則</a></p>
</li>
<li id="q-026-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Register 存取不構成 PEL 事件；完成的 Reset 或支援的硬體錯誤另判斷。 <a class="qa-rule-link" href="#common-register-11">本冊完整規則</a></p>
</li>
<li id="q-026-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-026-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-026-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-026-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-026-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>同時驗 Head／Tail 與 queue size 的 modulo 關係；只看 Doorbell 值下降不能判定違規。</p>
</li>
<li id="q-026-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查環大小用的是 slots N 還是編碼值 QSIZE；少加 1 會每圈錯一格。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-027" data-question="27"><h2><a class="qa-qid" href="#q-027">Q27</a> CQ Wrap-around 後 Phase Tag 如何變化？Host 如何利用 Phase Tag 辨識新 Completion？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-027-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-027-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>讓 Host 在重用同一個 CQ slot 時，辨識新寫入的完成與上一圈殘留資料。</p>
</li>
<li id="q-027-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Phase 是 CQ 的環狀生命週期資訊，不是某個 CID 的成功／失敗，也不是 SQ 的指標。</p>
</li>
<li id="q-027-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>這是 PCIe CQE 的基本機制，不需要額外 Feature。建立前 Host 把各 slot Phase 初始化為 0，初次期待 1。</p>
</li>
<li id="q-027-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CQE DW3 bit16 為 P；controller 每次在同一 slot 放入新 CQE 時反轉該 slot 的前次 Phase。</p>
</li>
<li id="q-027-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>Host 只讀當前 Head，P 符合期待值才處理；Head 跨 N−1→0 時反轉自己的期待 Phase，再檢查下一圈。</p>
</li>
<li id="q-027-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>第一圈的新 CQE 為 P=1，下一圈為 P=0。不是每相鄰一筆 completion 就 1、0、1、0 交替。</p>
</li>
<li id="q-027-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Phase 不符表示該位置還沒有本圈新完成，並非錯誤 Status；不能接著解讀殘留 CID／SC 作為新命令結果。</p>
</li>
<li id="q-027-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-027-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-027-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-027-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-027-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-027-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-027-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-027-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-027-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>測試至少跨一圈，核對 CQ Head、期待 P 與實際 P；重建 queue 後重新初始化，不能繼承前次期待值。</p>
</li>
<li id="q-027-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查 Host 是否每一筆都反轉期待 P，或重設後忘記清 CQ。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-028" data-question="28"><h2><a class="qa-qid" href="#q-028">Q28</a> CQ Full 通常如何形成？CQ Full 時 Controller 能否繼續處理相關 SQ？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-028-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-028-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>用 flow control 防止尚未消費的完成被覆寫。CQ 滿通常表示完成產生速度超過 Host 釋放速度。</p>
</li>
<li id="q-028-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>影響該 CQ 與其關聯 SQ；其他不使用此 CQ 的 SQ 必須繼續處理。</p>
</li>
<li id="q-028-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>看實際 CQ size、Host CQ Head 更新與待處理完成，不以 Number of Queues 推斷容量。</p>
</li>
<li id="q-028-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Full 條件是 (Tail+1) modulo N = Head，保留一格；Tail 是 controller 內部狀態，Host 不直接讀它。</p>
</li>
<li id="q-028-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>Host 逐筆驗 Phase、處理結果，再更新 Head。controller 在可用 slot 出現前不得張貼新完成到此 CQ。</p>
</li>
<li id="q-028-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>controller 可停止處理相關 SQ 的新增 entry；規範是 may，不能推論所有已取得命令必須瞬間停止或全部繼續。</p>
</li>
<li id="q-028-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>CQ Full 是容量狀態，不是要求回報的 NVMe 錯誤码。為騰空間覆寫未確認 CQE 才破壞正確性。</p>
</li>
<li id="q-028-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-028-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-028-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-028-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-028-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-028-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-028-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-028-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-028-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>若只有共享此 CQ 的 SQ 停滯，先驗 Host 消費；若獨立 CQ 的 SQ 也被此狀態停止，需檢查是否符合繼續處理要求。</p>
</li>
<li id="q-028-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先看 Host 是否讀了 CQE 卻忘記更新 CQ Head Doorbell；讀取本身不會釋放 controller 看見的空間。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-029" data-question="29"><h2><a class="qa-qid" href="#q-029">Q29</a> Host 釋放 CQ 空間後，Controller 應如何恢復 Command 處理？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-029-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-029-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>讓被 CQ 容量限制的正常工作繼續，而不是把 CQ Full 當成需要重新 Create 的錯誤。</p>
</li>
<li id="q-029-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>釋放的是此 CQ 的 slots，供關聯 SQ 的命令完成使用；不改變 queue 配額或 namespace 能力。</p>
</li>
<li id="q-029-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>確認 queue 仍存在且没有其他停止原因，例如正在 reset、CFS 或 Processing Paused。</p>
</li>
<li id="q-029-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Host 寫 CQ Head 新索引；controller 依 Head 推進取得可再用 slots，後續完成仍使用正確 Phase。</p>
</li>
<li id="q-029-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>消費 CQE→更新 Head→controller 得到空間→張貼等待完成並繼續受影響工作的處理。排程仍受正常仲裁與其他條件約束。</p>
</li>
<li id="q-029-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>已釋放的 slots 可以重用，不必重建 queue；規範沒有給所有裝置一個固定的「Head 更新到下一 CQE」延遲。</p>
</li>
<li id="q-029-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>正確釋放沒有特殊成功 CQE；Head 非法仍是 Doorbell 使用問題，而不是 Create Queue 的錯誤。</p>
</li>
<li id="q-029-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-029-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-029-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-029-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-029-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-029-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-029-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-029-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-029-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>檢查新的 CQE 是否占用合法可用 slot，並比較相關與獨立 SQ 的進度。</p>
</li>
<li id="q-029-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認 Head 寫到對的 CQ Register；錯 QID 會讓 Host 以為已釋放，實際滿的 CQ 卻沒有變。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-030" data-question="30"><h2><a class="qa-qid" href="#q-030">Q30</a> 多個 SQ 共用一個 CQ 時，Host 如何依 SQID 與 CID 辨識 Completion 來源？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-030-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-030-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>把每個完成交給正確原始要求；CID 只在同一 SQ 的 outstanding 命令中要求唯一。</p>
</li>
<li id="q-030-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>辨識鍵包含 controller、SQ lifetime、SQID 與 CID；controller／lifetime 是 Host 追蹤上下文，不是新增 CQE 欄位。</p>
</li>
<li id="q-030-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>使用建立時的 SQ→CQ 映射與 outstanding 表，不靠 Identify 回傳每筆命令位置。</p>
</li>
<li id="q-030-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CQE.SQID 指來源 SQ，CID 指該 SQ 內命令；SQHD 只報已消費 SQ 位置，不是該命令最初所在 slot。</p>
</li>
<li id="q-030-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先驗 CQE Phase，再讀 SQID／CID，定位原要求、處理 Status 和資料、更新該 SQ 的 Head 資訊，最後釋放 CQ slot。</p>
</li>
<li id="q-030-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>SQ1/CID9 和 SQ2/CID9 的完成能獨立正確配對，即使它們反序完成。</p>
</li>
<li id="q-030-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>同 SQ 的 CID 重複可能回 Command ID Conflict（0/03h）；實作搜尋多少既有命令以偵測衝突是 implementation specific，Host 仍有唯一性義務。</p>
</li>
<li id="q-030-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-030-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-030-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-030-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-030-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-030-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-030-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-030-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-030-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>核對 CQE 的 SQID 是否確實關聯這個 CQ，以及該 CID 是否屬於當前 queue 生命週期。</p>
</li>
<li id="q-030-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查完成表是否錯用「CQID+CID」當唯一鍵。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-command-8"><h3>命令完成、事件與紀錄 · DNR 與 More 應如何設定？</h3><p>有 CQE 時，DNR=1 表示相同命令再送到此 NVM subsystem 的任一 controller 仍預期失敗；DNR=0 只表示可能成功。除非本題錯誤另有明定，不把某個 Status 固定綁成 DNR=1。More=1 表示 Error Information Log 有這筆命令的補充資訊。SCT=SC=0 時 DNR 應為 0。</p></article>
<article id="common-command-9"><h3>命令完成、事件與紀錄 · 是否產生 Asynchronous Event？</h3><p>命令完成與非同步通知是兩件事；本題操作成功本身不保證有事件。若操作引起規範列出的事件，還要核對事件支援、適用的通知設定、是否已遮蔽，以及 Host 是否掛入 Asynchronous Event Request。</p></article>
<article id="common-command-10"><h3>命令完成、事件與紀錄 · 是否更新 Error Information Log 或其他 Log？</h3><p>成功 CQE 不是要求新增 Error Information 的理由。錯誤有 More=1 時，查 LID 01h 並用 SQID、CID 和 Error Count 對應；不能把每個非成功 CQE 都當成必須新增一筆。操作改變的狀態則由本題列出的查詢介面重新讀取。</p></article>
<article id="common-command-11"><h3>命令完成、事件與紀錄 · 是否記錄於 Persistent Event Log？</h3><p>Persistent Event Log 是選配的事件歷史，不是所有命令的執行清單。先查 LPA 的支援與 Supported Events Bitmap，再判斷本次是否符合指定事件的記錄條件；不能只因命令成功或失敗就要求新增一筆。</p></article>
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
<li id="ref-queue"><strong>Base 2.4 · §3.3.1</strong><br>文件頁 88–91 · PDF 114–117 · Figure 73–74</li>
<li id="ref-order"><strong>Base 2.4 · §3.4.1–3.4.5</strong><br>文件頁 101–105 · PDF 127–131 · Figure 80–81</li>
<li id="ref-qattr"><strong>Base 2.4 · §3.3.3–3.4.1</strong><br>文件頁 101 · PDF 127</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-sqe"><strong>Base 2.4 · §4.1.1</strong><br>文件頁 139–142 · PDF 165–168 · Figure 92–93</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>文件頁 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-delete"><strong>Base 2.4 · §5.3.3–5.3.4</strong><br>文件頁 531–532 · PDF 557–558 · Figure 580–583</li>
<li id="ref-fatal"><strong>Base 2.4 · §9.1–9.6.1</strong><br>文件頁 825–826 · PDF 851–852</li>
<li id="ref-pcie"><strong>PCIe Transport 1.4 · §3.1–3.4</strong><br>文件頁 9–13 · PDF 9–13 · Figure 3–8</li>
<li id="ref-pciconfig"><strong>PCIe Transport 1.4 · §3.8.1 (NVMe configuration access)</strong><br>文件頁 16–18 · PDF 16–18 · Figure 10–17</li>
</ul><h3>需要看欄位圖時</h3><p>既有圖表教學各有固定位置。這裡連回相關圖，不複製另一份圖解。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/doorbells/en/">English</a><a href="/DOCS/nvme-question-bank/doorbells.html">繁中教學 HTML</a></nav>
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
