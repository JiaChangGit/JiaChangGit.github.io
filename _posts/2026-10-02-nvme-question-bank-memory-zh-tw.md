---
layout: post
title: "NVMe 自問自答題庫：HMB、CMB 與 PMR"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/memory/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/memory/en/">English</a><a href="/DOCS/nvme-question-bank/memory.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–320</p>
<header><p class="qa-range">Q223–Q236</p><h1>HMB、CMB 與 PMR</h1><p class="qr-intro">先看記憶體位於哪裡、由誰提供與何時可回收，再看持久性。HMB、CMB、PMR 不能因都含 Memory 就套同一組 reset 規則。</p><p>先練習，再展開每題的 17 項解答。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>位置、使用者與持久性</h2><p class="qa-takeaway">位址設定保留，不代表原內容保留；CQE 成功也不必然證明 PMR 資料已持久化。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">機制</th><th scope="col">記憶體與用途</th><th scope="col">結束或確認條件</th></tr></thead><tbody><tr><td>HMB</td><td>Host 提供 controller 專用 buffer</td><td>成功停用後才能回收</td></tr><tr><td>CMB</td><td>Controller 提供可選用途記憶體</td><td>依 reset／CMSE 規則重建內容</td></tr><tr><td>PMR</td><td>PCIe function 提供持久記憶體</td><td>檢查 Ready、健康及 PMRWBM</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>HMB 停用成功前，Host 不能重用其 buffer。CMB 在某些 reset 後即使 CBA 還在，CQ 內容仍須重新初始化；PMR 則另有持久性與健康要求。</p>
<p class="qa-citations">來源：<a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-223">Q223 · HMB、CMB 與 PMR 分別解決什麼問題？</a></li>
<li><a href="#q-224">Q224 · HMB 大小與 Descriptor List 如何配置？</a></li>
<li><a href="#q-225">Q225 · HMB 位址、大小或 Descriptor 數量不合法時如何判斷？</a></li>
<li><a href="#q-226">Q226 · HMB 如何啟用、停用並在 Reset 後重新提供？</a></li>
<li><a href="#q-227">Q227 · Host 提前回收仍在使用的 HMB 會有什麼後果？</a></li>
<li><a href="#q-228">Q228 · Host 如何找出 CMB 的位置、大小與可用用途？</a></li>
<li><a href="#q-229">Q229 · 哪些 Queue、Data、Metadata 與指標清單可放 CMB？</a></li>
<li><a href="#q-230">Q230 · CMB 超出範圍或用於不支援用途時如何處理？</a></li>
<li><a href="#q-231">Q231 · Reset 後 CMB 設定與內容會保留嗎？</a></li>
<li><a href="#q-232">Q232 · PMR 如何確認支援、啟用並等待 Ready？</a></li>
<li><a href="#q-233">Q233 · PMR 未 Ready、發生錯誤或過早存取時會怎樣？</a></li>
<li><a href="#q-234">Q234 · Host 如何安全停用 PMR？</a></li>
<li><a href="#q-235">Q235 · Reset 與 Power Cycle 如何影響 PMR 狀態及持久資料？</a></li>
<li><a href="#q-236">Q236 · Host Memory、HMB、CMB 與 PMR 的存取與生命週期如何比較？</a></li>
</ol></section>
<article class="qa-question" id="q-223" data-question="223"><h2><a class="qa-qid" href="#q-223">Q223</a> HMB、CMB 與 PMR 分別解決什麼問題？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-223-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-223-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>它們都與記憶體有關，但借用方向、使用者與保存承諾不同；先辨認這三件事，才不會錯配 buffer。</p>
</li>
<li id="q-223-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>HMB 位於 Host，專供 controller 使用；CMB 位於 controller，供宣告支援的 queue 或 buffer；PMR 是可直接讀寫的持久記憶體區域。</p>
</li>
<li id="q-223-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>HMB 查 HMPRE；CMB 查 CAP.CMBS、CMBSZ；PMR 查 CAP.PMRS、PMRCAP。</p>
</li>
<li id="q-223-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>HMB 用 FID0Dh 配置 descriptor；CMB 用 CMBMSC／CMBLOC 建立地址關係；PMR 用 PMRCTL 與 PMRSTS 確認啟用和健康。</p>
</li>
<li id="q-223-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>依需求選擇：借 Host RAM 給韌體使用選 HMB；將 SQ 放到裝置記憶體須查 CMB.SQS；要直接存放持久資料則研究 PMR 的 barrier 與健康。</p>
</li>
<li id="q-223-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>正確結果是功能可用且符合各自使用限制，不是所有記憶體都能放所有資料結構。</p>
</li>
<li id="q-223-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>PMR 的 queue、PRP／SGL list 支援不在規範範圍，controller 可回 Invalid Field；不能因 PMR 可讀寫就把它當成另一個 CMB。</p>
</li>
<li id="q-223-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>HMB 透過 Set Features，具有 CQE；CMB／PMR 的直接 Register 存取沒有 CQE。 <a class="qa-rule-link" href="#common-memory_compare-8">本冊完整規則</a></p>
</li>
<li id="q-223-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>配置 HMB、CMB 或 PMR 本身沒有通用成功 AER。PMR 若進入唯讀等符合 SMART 警告的狀態，才依該警告與通知設定回報，不能將 HMB 的正常啟用當成同一種事件。</p>
</li>
<li id="q-223-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>HMB 用 Feature 及實際存取生命週期驗證，CMB 用位置與用途能力驗證，PMR 另需檢查 Ready、ERR、HSTS。這些觀察不是逐次寫入 Error Information 的要求。</p>
</li>
<li id="q-223-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般記憶體存取不是 PEL 事件。支援的 HMB Set Feature 記錄與 PMR 健康／硬體事件需各自符合條件，不能要求每次存取都有事件。</p>
</li>
<li id="q-223-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後 HMB 配置失效；CMB 特定 mapping 可保留，但內容 undefined；PMR 已持久內容保留。 <a class="qa-rule-link" href="#common-memory_compare-12">本冊完整規則</a></p>
</li>
<li id="q-223-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重建受影響控制環境，再分別處理 HMB 配置、CMB 初始化與 PMR 健康檢查；不能把所有記憶體當成同一種保存介面。 <a class="qa-rule-link" href="#common-memory_compare-13">本冊完整規則</a></p>
</li>
<li id="q-223-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>HMB 與 CMB 不提供 PMR 的持久性承諾；PMR 也要先用支援的 write barrier 與健康狀態確認先前寫入。 <a class="qa-rule-link" href="#common-memory_compare-14">本冊完整規則</a></p>
</li>
<li id="q-223-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>先確認記憶體位於 Host 或 controller，再確認使用權與地址空間。 <a class="qa-rule-link" href="#common-memory_compare-15">本冊完整規則</a></p>
</li>
<li id="q-223-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>用能力、配置、存取方式與恢復後內容交叉比對，而不是只看一個地址能不能讀到 bytes。</p>
</li>
<li id="q-223-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查選錯記憶體種類，或把「位於裝置」誤解成「必定持久」。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-224" data-question="224"><h2><a class="qa-qid" href="#q-224">Q224</a> HMB 大小與 Descriptor List 如何配置？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-224-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-224-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Host 以多段實體連續記憶體提供 HMB，不必一次取得整塊連續 RAM，但 descriptor list 本身必須實體連續。</p>
</li>
<li id="q-224-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>配置給一個 controller 專用，Host 啟用後不能當一般工作 buffer 改寫。</p>
</li>
<li id="q-224-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 HMPRE、HMMIN、HMMINDS、HMMAXD；前兩者及 HMMINDS 用 4 KiB 單位。</p>
</li>
<li id="q-224-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>HSIZE 與每筆 BSIZE 卻用 CC.MPS page 單位；HMDLEC 是實際筆數，list address 16-byte 對齊，BADD 按 CC.MPS 對齊。</p>
</li>
<li id="q-224-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先配置並固定 RAM，填 16-byte descriptors，核對各段大小與 HSIZE，再以 EHM=1 啟用，等 CQE 成功才交給 controller 使用。</p>
</li>
<li id="q-224-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Get 回 EHM 與 attributes 可核對實際配置。假設 CC.MPS 選 8 KiB，HSIZE=256 表示 2 MiB，不是 1 MiB。</p>
</li>
<li id="q-224-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>HMDLEC=0 須 Invalid Field；超過建議可用 descriptor 限制可能只使部分記憶體未利用，不能一律預期拒絕整個配置。</p>
</li>
<li id="q-224-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-224-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>啟用或停用 HMB 沒有獨立的成功 AER；若另外發生已定義的硬體錯誤，才依其事件條件回報。 <a class="qa-rule-link" href="#common-hmb_op-9">本冊完整規則</a></p>
</li>
<li id="q-224-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Features 回報 EHM、HMNARE、HMNAR 與配置資料；它不是 HMB 內容的備份。 <a class="qa-rule-link" href="#common-hmb_op-10">本冊完整規則</a></p>
</li>
<li id="q-224-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>若支援該 FID 的 PEL Set Feature Event，依允許記錄與成功變更條件處理；一般 HMB 讀寫不是逐次 Persistent Event。 <a class="qa-rule-link" href="#common-hmb_op-11">本冊完整規則</a></p>
</li>
<li id="q-224-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>HMB 資源配置不跨 CLR 保留。 <a class="qa-rule-link" href="#common-hmb_op-12">本冊完整規則</a></p>
</li>
<li id="q-224-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 使受影響 controller 的 HMB 配置失效，Host 恢復通道後重新配置。 <a class="qa-rule-link" href="#common-hmb_op-13">本冊完整規則</a></p>
</li>
<li id="q-224-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>HMB 不是持久儲存。 <a class="qa-rule-link" href="#common-hmb_op-14">本冊完整規則</a></p>
</li>
<li id="q-224-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>HMB 是 Host 分配給此 controller 專用的記憶體；啟用期間 Host 不得改寫 descriptor list 或 buffer，也不能把同一區域交給其他用途。 <a class="qa-rule-link" href="#common-hmb_op-15">本冊完整規則</a></p>
</li>
<li id="q-224-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>同時比對能力單位、命令單位與 Get attributes，不能直接將 HMPRE 數字抄進 HSIZE。</p>
</li>
<li id="q-224-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查 4 KiB 與 CC.MPS 的差別，以及 HMDLEC 是否錯用 zero-based。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-225" data-question="225"><h2><a class="qa-qid" href="#q-225">Q225</a> HMB 位址、大小或 Descriptor 數量不合法時如何判斷？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-225-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-225-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>不同欄位的錯誤規則不同；驗證時要指定單一錯誤，才知道應預期哪一種反應。</p>
</li>
<li id="q-225-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>包含 descriptor list 本身、每筆記憶體範圍，以及目前 HMB 是否已啟用。</p>
</li>
<li id="q-225-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 HMMINDS／HMMAXD、HMBR 與 Get.EHM，再核對 Set 的欄位。</p>
</li>
<li id="q-225-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>HMDLEC=0 是 Invalid Field；BSIZE=0 的 descriptor 必須忽略。HMDLLA 低 4 bits 要清零，但 controller 必須如同其為零運作，且不必檢查。</p>
</li>
<li id="q-225-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先測可判定的格式錯誤，再將地址無法存取造成的傳輸失敗分開；不要把 Host 錯誤 mapping 當作同一種參數錯誤。</p>
</li>
<li id="q-225-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>合法配置成功；超出可用 descriptor 限制時，可出現未完全利用 HMB 的結果。</p>
</li>
<li id="q-225-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>已啟用又要求 EHM=1 必須 Command Sequence Error；不支援 HMBR 卻設 HMNARE=1 必須 Invalid Field。不能要求每個低位對齊錯誤都回相同 Status。</p>
</li>
<li id="q-225-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-225-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>啟用或停用 HMB 沒有獨立的成功 AER；若另外發生已定義的硬體錯誤，才依其事件條件回報。 <a class="qa-rule-link" href="#common-hmb_op-9">本冊完整規則</a></p>
</li>
<li id="q-225-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Features 回報 EHM、HMNARE、HMNAR 與配置資料；它不是 HMB 內容的備份。 <a class="qa-rule-link" href="#common-hmb_op-10">本冊完整規則</a></p>
</li>
<li id="q-225-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>若支援該 FID 的 PEL Set Feature Event，依允許記錄與成功變更條件處理；一般 HMB 讀寫不是逐次 Persistent Event。 <a class="qa-rule-link" href="#common-hmb_op-11">本冊完整規則</a></p>
</li>
<li id="q-225-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>HMB 資源配置不跨 CLR 保留。 <a class="qa-rule-link" href="#common-hmb_op-12">本冊完整規則</a></p>
</li>
<li id="q-225-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 使受影響 controller 的 HMB 配置失效，Host 恢復通道後重新配置。 <a class="qa-rule-link" href="#common-hmb_op-13">本冊完整規則</a></p>
</li>
<li id="q-225-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>HMB 不是持久儲存。 <a class="qa-rule-link" href="#common-hmb_op-14">本冊完整規則</a></p>
</li>
<li id="q-225-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>HMB 是 Host 分配給此 controller 專用的記憶體；啟用期間 Host 不得改寫 descriptor list 或 buffer，也不能把同一區域交給其他用途。 <a class="qa-rule-link" href="#common-hmb_op-15">本冊完整規則</a></p>
</li>
<li id="q-225-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>將具體欄位條件對到指定反應，保留「忽略」與「必須拒絕」之間的差別。</p>
</li>
<li id="q-225-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認測試是否同時放入多種錯誤，造成 Status 無法唯一預測。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-226" data-question="226"><h2><a class="qa-qid" href="#q-226">Q226</a> HMB 如何啟用、停用並在 Reset 後重新提供？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-226-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-226-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>HMB 的使用權要明確交接，Host 才知道何時能回收記憶體。</p>
</li>
<li id="q-226-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>EHM 控制 controller 是否可使用 HMB，MR 描述返回的內容是否仍符合原狀。</p>
</li>
<li id="q-226-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先 Get.EHM 與配置，Reset 後也重新確認，而不沿用 Host 記錄的啟用狀態。</p>
</li>
<li id="q-226-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>EHM=0 時 CDW12～15 忽略；MR=1 要求原大小、list 位址、list 內容及 buffer 內容完全相同。</p>
</li>
<li id="q-226-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>啟用後交給 controller；需要回收時送 EHM=0 並等成功 CQE，之後才能改寫。Reset 後再提供保留的配置或新的配置。</p>
</li>
<li id="q-226-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>停用成功後 controller 不得再存取 HMB，直到重新啟用；原本未啟用時再停用也成功且不做其他動作。</p>
</li>
<li id="q-226-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>已啟用再次啟用是 Command Sequence Error；內容已被改動卻宣告 MR=1 是 Host 違反前提，不能期待原快取仍安全可用。</p>
</li>
<li id="q-226-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-226-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>啟用或停用 HMB 沒有獨立的成功 AER；若另外發生已定義的硬體錯誤，才依其事件條件回報。 <a class="qa-rule-link" href="#common-hmb_op-9">本冊完整規則</a></p>
</li>
<li id="q-226-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Features 回報 EHM、HMNARE、HMNAR 與配置資料；它不是 HMB 內容的備份。 <a class="qa-rule-link" href="#common-hmb_op-10">本冊完整規則</a></p>
</li>
<li id="q-226-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>若支援該 FID 的 PEL Set Feature Event，依允許記錄與成功變更條件處理；一般 HMB 讀寫不是逐次 Persistent Event。 <a class="qa-rule-link" href="#common-hmb_op-11">本冊完整規則</a></p>
</li>
<li id="q-226-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>HMB 資源配置不跨 CLR 保留。 <a class="qa-rule-link" href="#common-hmb_op-12">本冊完整規則</a></p>
</li>
<li id="q-226-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 使受影響 controller 的 HMB 配置失效，Host 恢復通道後重新配置。 <a class="qa-rule-link" href="#common-hmb_op-13">本冊完整規則</a></p>
</li>
<li id="q-226-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>HMB 不是持久儲存。 <a class="qa-rule-link" href="#common-hmb_op-14">本冊完整規則</a></p>
</li>
<li id="q-226-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>HMB 是 Host 分配給此 controller 專用的記憶體；啟用期間 Host 不得改寫 descriptor list 或 buffer，也不能把同一區域交給其他用途。 <a class="qa-rule-link" href="#common-hmb_op-15">本冊完整規則</a></p>
</li>
<li id="q-226-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>用停用 CQE 當作可修改的交接點；僅送出停用命令並不表示交接完成。</p>
</li>
<li id="q-226-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查 Host 回收記憶體的時點是否早於停用完成。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-227" data-question="227"><h2><a class="qa-qid" href="#q-227">Q227</a> Host 提前回收仍在使用的 HMB 會有什麼後果？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-227-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-227-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這會破壞 controller 專用記憶體的前提，可能讓裝置讀到其他用途的資料，或改寫已被重新分配的 RAM。</p>
</li>
<li id="q-227-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>受影響可能超過 NVMe buffer 本身，因為 Host 已把同一實體頁交给別的程式。</p>
</li>
<li id="q-227-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 EHM 與最後一次停用 CQE，並保存記憶體配置和 mapping 的生命週期。</p>
</li>
<li id="q-227-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>HMB descriptor 與描述的 ranges 都受保護；只保留 list 卻回收資料頁，仍違反規則。</p>
</li>
<li id="q-227-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先請求停用，等成功完成，再解除 mapping 與回收；若故障無法停用，需完成足以終止舊存取的恢復流程後才回收。</p>
</li>
<li id="q-227-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>正確交接後，controller 不再使用舊區域，Host 才可安全重用。</p>
</li>
<li id="q-227-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>這種 Host 違規沒有保證會被 controller 偵測或以固定 Status 拒絕；可能出現資料損壞，不能靠期待 Error Log 防護。</p>
</li>
<li id="q-227-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-227-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>啟用或停用 HMB 沒有獨立的成功 AER；若另外發生已定義的硬體錯誤，才依其事件條件回報。 <a class="qa-rule-link" href="#common-hmb_op-9">本冊完整規則</a></p>
</li>
<li id="q-227-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Get Features 回報 EHM、HMNARE、HMNAR 與配置資料；它不是 HMB 內容的備份。 <a class="qa-rule-link" href="#common-hmb_op-10">本冊完整規則</a></p>
</li>
<li id="q-227-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>若支援該 FID 的 PEL Set Feature Event，依允許記錄與成功變更條件處理；一般 HMB 讀寫不是逐次 Persistent Event。 <a class="qa-rule-link" href="#common-hmb_op-11">本冊完整規則</a></p>
</li>
<li id="q-227-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>HMB 資源配置不跨 CLR 保留。 <a class="qa-rule-link" href="#common-hmb_op-12">本冊完整規則</a></p>
</li>
<li id="q-227-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 使受影響 controller 的 HMB 配置失效，Host 恢復通道後重新配置。 <a class="qa-rule-link" href="#common-hmb_op-13">本冊完整規則</a></p>
</li>
<li id="q-227-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>HMB 不是持久儲存。 <a class="qa-rule-link" href="#common-hmb_op-14">本冊完整規則</a></p>
</li>
<li id="q-227-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>HMB 是 Host 分配給此 controller 專用的記憶體；啟用期間 Host 不得改寫 descriptor list 或 buffer，也不能把同一區域交給其他用途。 <a class="qa-rule-link" href="#common-hmb_op-15">本冊完整規則</a></p>
</li>
<li id="q-227-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>區分 Host 提前回收與 controller 在成功停用後仍存取：前者是 Host 問題，後者才違反明定停止存取要求。</p>
</li>
<li id="q-227-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先比對合法存取結束的時點與記憶體開始重用的時間。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-228" data-question="228"><h2><a class="qa-qid" href="#q-228">Q228</a> Host 如何找出 CMB 的位置、大小與可用用途？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-228-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-228-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>需要同時知道 Host 如何存取 CMB，以及命令中的地址如何讓 controller 指向同一區域。</p>
</li>
<li id="q-228-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>CMB 有 PCIe address range 與 controller address range，兩者基底可不同，相同 offset 對應相同內容。</p>
</li>
<li id="q-228-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 CAP.CMBS，設 CMBMSC.CRE 後讀 CMBLOC 與 CMBSZ；CRE=0 時這兩個屬性可為零。</p>
</li>
<li id="q-228-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CMBLOC.BIR 選 BAR、OFST 配合大小單位求偏移；CMBSZ.SZ×SZU 求大小，再受 BAR 可用範圍限制。SQS、CQS、LISTS、RDS、WDS 各自宣告用途。</p>
</li>
<li id="q-228-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>配置不衝突的 CBA，設 CMSE，檢查 CMBSTS.CBAI，再初始化要放入的 queue 或 buffer。</p>
</li>
<li id="q-228-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Host 與命令使用各自正確的地址，同一 offset 對到同一份 CMB 內容。</p>
</li>
<li id="q-228-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>無效 CBA 會使 CBAI=1 且未成功啟用 controller memory space；這是 Register 狀態，不是回一筆 Admin CQE。</p>
</li>
<li id="q-228-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>CMB Register 與記憶體存取沒有 NVMe CQE；若使用 CMB 的 Admin／I/O 命令回 CQE，才對該命令解讀 DNR、More。 <a class="qa-rule-link" href="#common-cmb_op-8">本冊完整規則</a></p>
</li>
<li id="q-228-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Register 存取本身不產生成功事件。若另外發生硬體錯誤等事件，則依該事件自己的條件判斷。 <a class="qa-rule-link" href="#common-register-9">本冊完整規則</a></p>
</li>
<li id="q-228-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>不要求每次 Register 讀寫都新增錯誤紀錄。先保留 Register 值及時間，再補充 controller 當時允許讀取的診斷資料。 <a class="qa-rule-link" href="#common-register-10">本冊完整規則</a></p>
</li>
<li id="q-228-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Register 存取不是 PEL 事件。若操作同時引發 Reset 或硬體錯誤，再依支援能力與對應事件條件判斷。 <a class="qa-rule-link" href="#common-register-11">本冊完整規則</a></p>
</li>
<li id="q-228-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CC.EN 觸發的 CLR 與 FLR 保留 CMBMSC，但 CMB 內容變成 undefined。 <a class="qa-rule-link" href="#common-cmb_op-12">本冊完整規則</a></p>
</li>
<li id="q-228-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新確認 CMB Register 與 mapping，重建使用它的 queues。 <a class="qa-rule-link" href="#common-cmb_op-13">本冊完整規則</a></p>
</li>
<li id="q-228-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>CMB 不提供 PMR 的跨斷電持久性保證。 <a class="qa-rule-link" href="#common-cmb_op-14">本冊完整規則</a></p>
</li>
<li id="q-228-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>CMB 位於 controller，但 Host 與 controller 使用的地址範圍可以不同。 <a class="qa-rule-link" href="#common-cmb_op-15">本冊完整規則</a></p>
</li>
<li id="q-228-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>比對 BAR 範圍、OFST、SZU、CBA 與支援 flags，不能只看 CAP.CMBS。</p>
</li>
<li id="q-228-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否把 BAR 地址直接拿去當已重新配置的 controller 地址。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-229" data-question="229"><h2><a class="qa-qid" href="#q-229">Q229</a> 哪些 Queue、Data、Metadata 與指標清單可放 CMB？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-229-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-229-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>CMB 用途由多個能力位元分別控制，支援 SQ 不表示同時支援 CQ 或資料。</p>
</li>
<li id="q-229-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>限制可能以整條 queue、單筆命令的 list，或該命令的所有 data／metadata 為單位。</p>
</li>
<li id="q-229-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 CMBSZ.SQS、CQS、LISTS、RDS、WDS，以及 CMBLOC.CQMMS、CQPDS、CDPMLS、CDPCILS、CDMMMS。</p>
</li>
<li id="q-229-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CQMMS=0 要求單一 queue 全在 CMB 或全在外；CQPDS=0 要求 CMB queue 實體連續。LISTS 控制 PRP／SGL list，其他 bits 再決定混放與 SQ 位置限制。</p>
</li>
<li id="q-229-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先按物件選用途 flag，再檢查它和 SQ、data、metadata 的組合條件，最後才配置地址。</p>
</li>
<li id="q-229-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>假設 SQS=1、CQS=0，可把支援的 SQ 放 CMB，CQ 仍放 Host memory；不是兩者一定一起搬。</p>
</li>
<li id="q-229-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>違反使用要求一般須 Invalid Use of Controller Memory Buffer；但 LISTS=0 仍放 list 的條文明定 undefined，不能強行替它指定固定 Status。</p>
</li>
<li id="q-229-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>CMB Register 與記憶體存取沒有 NVMe CQE；若使用 CMB 的 Admin／I/O 命令回 CQE，才對該命令解讀 DNR、More。 <a class="qa-rule-link" href="#common-cmb_op-8">本冊完整規則</a></p>
</li>
<li id="q-229-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Register 存取本身不產生成功事件。若另外發生硬體錯誤等事件，則依該事件自己的條件判斷。 <a class="qa-rule-link" href="#common-register-9">本冊完整規則</a></p>
</li>
<li id="q-229-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>不要求每次 Register 讀寫都新增錯誤紀錄。先保留 Register 值及時間，再補充 controller 當時允許讀取的診斷資料。 <a class="qa-rule-link" href="#common-register-10">本冊完整規則</a></p>
</li>
<li id="q-229-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Register 存取不是 PEL 事件。若操作同時引發 Reset 或硬體錯誤，再依支援能力與對應事件條件判斷。 <a class="qa-rule-link" href="#common-register-11">本冊完整規則</a></p>
</li>
<li id="q-229-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CC.EN 觸發的 CLR 與 FLR 保留 CMBMSC，但 CMB 內容變成 undefined。 <a class="qa-rule-link" href="#common-cmb_op-12">本冊完整規則</a></p>
</li>
<li id="q-229-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新確認 CMB Register 與 mapping，重建使用它的 queues。 <a class="qa-rule-link" href="#common-cmb_op-13">本冊完整規則</a></p>
</li>
<li id="q-229-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>CMB 不提供 PMR 的跨斷電持久性保證。 <a class="qa-rule-link" href="#common-cmb_op-14">本冊完整規則</a></p>
</li>
<li id="q-229-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>CMB 位於 controller，但 Host 與 controller 使用的地址範圍可以不同。 <a class="qa-rule-link" href="#common-cmb_op-15">本冊完整規則</a></p>
</li>
<li id="q-229-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>RDS／WDS 要按命令資料方向解讀，例如 Read 的結果是 controller 傳向 Host 的資料。</p>
</li>
<li id="q-229-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查只確認了功能存在，卻漏查所選物件的用途 flag。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-230" data-question="230"><h2><a class="qa-qid" href="#q-230">Q230</a> CMB 超出範圍或用於不支援用途時如何處理？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-230-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-230-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>要分清無效 mapping、合法 mapping 中的用途違規，以及根本不被解讀成 CMB 的地址。</p>
</li>
<li id="q-230-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>CBA 與大小決定 controller address range；CMSE=0 時 Host 提供的地址不被視為 CMB。</p>
</li>
<li id="q-230-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>保存 CMBMSC、CMBSTS、CMBLOC、CMBSZ 與命令完整資料範圍。</p>
</li>
<li id="q-230-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CBA 不得使範圍溢出 64-bit 地址，也不得與已啟用的 PMR controller range 重疊。</p>
</li>
<li id="q-230-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先算起點與末端，再判斷每個地址落在哪個空間；最後檢查用途旗標與混放條件。</p>
</li>
<li id="q-230-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>合法範圍且符合用途限制時，命令按正常資料存取執行。</p>
</li>
<li id="q-230-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>無效 mapping 看 CBAI；用途違規依 Invalid Use of CMB；範圍外地址可能被當成其他記憶體，不能一律預期「CMB 越界」專用 Status。</p>
</li>
<li id="q-230-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>CMB Register 與記憶體存取沒有 NVMe CQE；若使用 CMB 的 Admin／I/O 命令回 CQE，才對該命令解讀 DNR、More。 <a class="qa-rule-link" href="#common-cmb_op-8">本冊完整規則</a></p>
</li>
<li id="q-230-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Register 存取本身不產生成功事件。若另外發生硬體錯誤等事件，則依該事件自己的條件判斷。 <a class="qa-rule-link" href="#common-register-9">本冊完整規則</a></p>
</li>
<li id="q-230-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>不要求每次 Register 讀寫都新增錯誤紀錄。先保留 Register 值及時間，再補充 controller 當時允許讀取的診斷資料。 <a class="qa-rule-link" href="#common-register-10">本冊完整規則</a></p>
</li>
<li id="q-230-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Register 存取不是 PEL 事件。若操作同時引發 Reset 或硬體錯誤，再依支援能力與對應事件條件判斷。 <a class="qa-rule-link" href="#common-register-11">本冊完整規則</a></p>
</li>
<li id="q-230-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CC.EN 觸發的 CLR 與 FLR 保留 CMBMSC，但 CMB 內容變成 undefined。 <a class="qa-rule-link" href="#common-cmb_op-12">本冊完整規則</a></p>
</li>
<li id="q-230-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新確認 CMB Register 與 mapping，重建使用它的 queues。 <a class="qa-rule-link" href="#common-cmb_op-13">本冊完整規則</a></p>
</li>
<li id="q-230-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>CMB 不提供 PMR 的跨斷電持久性保證。 <a class="qa-rule-link" href="#common-cmb_op-14">本冊完整規則</a></p>
</li>
<li id="q-230-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>CMB 位於 controller，但 Host 與 controller 使用的地址範圍可以不同。 <a class="qa-rule-link" href="#common-cmb_op-15">本冊完整規則</a></p>
</li>
<li id="q-230-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>命令錯誤與 Register 狀態是兩份證據；沒有 CQE 不表示 Register 啟用成功。</p>
</li>
<li id="q-230-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查範圍計算是否溢位，以及計算用的是 Host 還是 controller 地址。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-231" data-question="231"><h2><a class="qa-qid" href="#q-231">Q231</a> Reset 後 CMB 設定與內容會保留嗎？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-231-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-231-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>位址保留與內容保留是兩件事，這是 CMB 恢復時最容易混淆的地方。</p>
</li>
<li id="q-231-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>CC.EN 觸發的 CLR 與 FLR 有明確 CMBMSC 保留例外，其他來源須看對應 Register 規則。</p>
</li>
<li id="q-231-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>保存 Reset 來源、CMBMSC 與 CMBSTS，恢復後再讀取確認。</p>
</li>
<li id="q-231-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CMSE 由 0 轉 1、Controller Reset 或 FLR，都使 CMB 內容 undefined。</p>
</li>
<li id="q-231-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>恢復 mapping 後重新初始化會用到的記憶體，再建立 queue；CQ 尤其要初始化 Phase，避免誤讀殘留完成。</p>
</li>
<li id="q-231-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>新的使用期間從已初始化的內容開始，不能沿用舊 queue 指標或假定資料保存。</p>
</li>
<li id="q-231-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>讀到與 Reset 前相同 bytes 也不代表規範保證保留；undefined 可以碰巧相同。</p>
</li>
<li id="q-231-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>CMB Register 與記憶體存取沒有 NVMe CQE；若使用 CMB 的 Admin／I/O 命令回 CQE，才對該命令解讀 DNR、More。 <a class="qa-rule-link" href="#common-cmb_op-8">本冊完整規則</a></p>
</li>
<li id="q-231-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Register 存取本身不產生成功事件。若另外發生硬體錯誤等事件，則依該事件自己的條件判斷。 <a class="qa-rule-link" href="#common-register-9">本冊完整規則</a></p>
</li>
<li id="q-231-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>不要求每次 Register 讀寫都新增錯誤紀錄。先保留 Register 值及時間，再補充 controller 當時允許讀取的診斷資料。 <a class="qa-rule-link" href="#common-register-10">本冊完整規則</a></p>
</li>
<li id="q-231-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Register 存取不是 PEL 事件。若操作同時引發 Reset 或硬體錯誤，再依支援能力與對應事件條件判斷。 <a class="qa-rule-link" href="#common-register-11">本冊完整規則</a></p>
</li>
<li id="q-231-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CC.EN 觸發的 CLR 與 FLR 保留 CMBMSC，但 CMB 內容變成 undefined。 <a class="qa-rule-link" href="#common-cmb_op-12">本冊完整規則</a></p>
</li>
<li id="q-231-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新確認 CMB Register 與 mapping，重建使用它的 queues。 <a class="qa-rule-link" href="#common-cmb_op-13">本冊完整規則</a></p>
</li>
<li id="q-231-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>CMB 不提供 PMR 的跨斷電持久性保證。 <a class="qa-rule-link" href="#common-cmb_op-14">本冊完整規則</a></p>
</li>
<li id="q-231-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>CMB 位於 controller，但 Host 與 controller 使用的地址範圍可以不同。 <a class="qa-rule-link" href="#common-cmb_op-15">本冊完整規則</a></p>
</li>
<li id="q-231-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>用 Register 保留規則驗 mapping，用 queue 與內容初始化規則驗使用權，兩項分開判定。</p>
</li>
<li id="q-231-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否因 CMBMSC 沒變，就省略了 CQ 與 buffer 初始化。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-232" data-question="232"><h2><a class="qa-qid" href="#q-232">Q232</a> PMR 如何確認支援、啟用並等待 Ready？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-232-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-232-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>PMR 可獨立於 NVMe 命令處理環境啟用，Host 必須等其自己的 Ready 狀態。</p>
</li>
<li id="q-232-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>PMR 占用 PMRCAP.BIR 指定 BAR 的整個區域；controller 地址可另由 PMRMSC 設定。</p>
</li>
<li id="q-232-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 CAP.PMRS、PMRCAP 的 BIR、CMSS、RDS、WDS、PMRWBM、PMRTO、PMRTU。</p>
</li>
<li id="q-232-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>PMRCTL.EN 啟用；PMRSTS.NRDY=0 配合 EN=1 才代表 Ready，還要看 HSTS 與 ERR。</p>
</li>
<li id="q-232-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>配置需要的地址空間，設 EN=1，等待 NRDY=0；Host 應至少等待 PMRTO×PMRTU 指定時間再判斷沒有完成轉換。</p>
</li>
<li id="q-232-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Ready 且健康正常後才能依支援用途讀寫；不需要先設 CC.EN=1 才能啟用 PMR。</p>
</li>
<li id="q-232-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>PMRTO 是 Host 應給的等待時間，不可直接寫成 controller 每筆命令的 timeout。CBA 無效另看 CBAI。</p>
</li>
<li id="q-232-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>直接存取 PMR 或其 Register 沒有 NVMe CQE。 <a class="qa-rule-link" href="#common-pmr_op-8">本冊完整規則</a></p>
</li>
<li id="q-232-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>PMR 變成唯讀或不可靠時，SMART.CW.PMRRO 回報警告，並可能依 SMART AER 設定通知。 <a class="qa-rule-link" href="#common-pmr_op-9">本冊完整規則</a></p>
</li>
<li id="q-232-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>PMRSTS 的 NRDY、HSTS、ERR 是主要證據，SMART 提供 PMR 警告。 <a class="qa-rule-link" href="#common-pmr_op-10">本冊完整規則</a></p>
</li>
<li id="q-232-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>若 PMR 警告符合支援的 PEL Critical Warning hardware event，依事件規則記錄；每次 PMR 讀寫或 EN 切換不是獨立 PEL 事件。 <a class="qa-rule-link" href="#common-pmr_op-11">本冊完整規則</a></p>
</li>
<li id="q-232-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Ready 且已確認持久的內容跨 CLR 保留。 <a class="qa-rule-link" href="#common-pmr_op-12">本冊完整規則</a></p>
</li>
<li id="q-232-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新確認啟用與 Ready 狀態，再檢查 HSTS。 <a class="qa-rule-link" href="#common-pmr_op-13">本冊完整規則</a></p>
</li>
<li id="q-232-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Ready 時已完成且確認持久的寫入應跨 Power Cycle 保留；恢復後仍須確認 HSTS 與 ERR。 <a class="qa-rule-link" href="#common-pmr_op-14">本冊完整規則</a></p>
</li>
<li id="q-232-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>PMR 屬於提供它的 PCIe function，其他存取端也必須核對該 PMR 的健康。 <a class="qa-rule-link" href="#common-pmr_op-15">本冊完整規則</a></p>
</li>
<li id="q-232-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>能力、EN、NRDY、HSTS 與 mapping 一起成立，才是可使用的配置。</p>
</li>
<li id="q-232-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否把 NRDY=1 誤看成 Ready，或漏算 PMRTU 的分鐘／500 ms 單位。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-233" data-question="233"><h2><a class="qa-qid" href="#q-233">Q233</a> PMR 未 Ready、發生錯誤或過早存取時會怎樣？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-233-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-233-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>存取在傳輸層完成，不表示記憶體內容有效；PMR 必須同時檢查自身狀態。</p>
</li>
<li id="q-233-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>直接 PMR 讀寫與 NVMe 命令使用 PMR buffer，兩者的錯誤觀察方式不同。</p>
</li>
<li id="q-233-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>檢查 EN、NRDY、HSTS、ERR；HSTS 在 not-ready 時清零，因此零 HSTS 不能單獨證明健康可用。</p>
</li>
<li id="q-233-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Not-ready 直接讀可成功卻回 undefined；直接寫可成功卻不更新內容。HSTS 可表示 Restore Error、Read Only 或 Unreliable。</p>
</li>
<li id="q-233-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先確認 Ready，再存取；完成後用支援的 barrier 與狀態檢查，遇到健康改變則回查上次正常觀察後的操作。</p>
</li>
<li id="q-233-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>NVMe 命令成功把資料寫向 PMR，也不單憑 CQE 保證 PMR 實際寫入成功。</p>
</li>
<li id="q-233-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>若關聯 controller 偵測命令寫 PMR 未成功，應以 Data Transfer Error 中止；直接 MMIO 存取沒有可要求的 NVMe CQE。</p>
</li>
<li id="q-233-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>直接存取 PMR 或其 Register 沒有 NVMe CQE。 <a class="qa-rule-link" href="#common-pmr_op-8">本冊完整規則</a></p>
</li>
<li id="q-233-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>PMR 變成唯讀或不可靠時，SMART.CW.PMRRO 回報警告，並可能依 SMART AER 設定通知。 <a class="qa-rule-link" href="#common-pmr_op-9">本冊完整規則</a></p>
</li>
<li id="q-233-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>PMRSTS 的 NRDY、HSTS、ERR 是主要證據，SMART 提供 PMR 警告。 <a class="qa-rule-link" href="#common-pmr_op-10">本冊完整規則</a></p>
</li>
<li id="q-233-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>若 PMR 警告符合支援的 PEL Critical Warning hardware event，依事件規則記錄；每次 PMR 讀寫或 EN 切換不是獨立 PEL 事件。 <a class="qa-rule-link" href="#common-pmr_op-11">本冊完整規則</a></p>
</li>
<li id="q-233-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Ready 且已確認持久的內容跨 CLR 保留。 <a class="qa-rule-link" href="#common-pmr_op-12">本冊完整規則</a></p>
</li>
<li id="q-233-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新確認啟用與 Ready 狀態，再檢查 HSTS。 <a class="qa-rule-link" href="#common-pmr_op-13">本冊完整規則</a></p>
</li>
<li id="q-233-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Ready 時已完成且確認持久的寫入應跨 Power Cycle 保留；恢復後仍須確認 HSTS 與 ERR。 <a class="qa-rule-link" href="#common-pmr_op-14">本冊完整規則</a></p>
</li>
<li id="q-233-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>PMR 屬於提供它的 PCIe function，其他存取端也必須核對該 PMR 的健康。 <a class="qa-rule-link" href="#common-pmr_op-15">本冊完整規則</a></p>
</li>
<li id="q-233-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>將 CQE 成功與 PMRSTS 正常分別核對，不可用其中一項替代另一項。</p>
</li>
<li id="q-233-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查存取當時 EN／NRDY，而不只看較晚恢復後的狀態。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-234" data-question="234"><h2><a class="qa-qid" href="#q-234">Q234</a> Host 如何安全停用 PMR？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-234-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-234-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>停用前要先確認先前寫入已完成且持久，避免把仍在路上的寫入誤當成保存完成。</p>
</li>
<li id="q-234-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>包含直接 PMR 存取與仍以 PMR 為 buffer 的命令，所有使用者都要協調停止。</p>
</li>
<li id="q-234-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 PMRWBM 支援的 barrier、PMRSTS 健康與 PMRTO／PMRTU。</p>
</li>
<li id="q-234-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>依能力可用 PMR memory read 或 PMRSTS read 建立先前寫入已持久的保證；不能假設任意 Register read 都是 barrier。</p>
</li>
<li id="q-234-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>停止新存取，等相關工作結束，執行支援的 barrier 並確認健康，再清 PMRCTL.EN，等待 NRDY=1。</p>
</li>
<li id="q-234-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>NRDY=1 表示停用完成到可再次啟用的狀態；先前合法持久內容不因停用就變成 CMB 那樣的 undefined。</p>
</li>
<li id="q-234-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>ERR 非零或 HSTS 不正常時，不能把停用成功當成先前資料已正確保存；應保留錯誤證據。</p>
</li>
<li id="q-234-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>直接存取 PMR 或其 Register 沒有 NVMe CQE。 <a class="qa-rule-link" href="#common-pmr_op-8">本冊完整規則</a></p>
</li>
<li id="q-234-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>PMR 變成唯讀或不可靠時，SMART.CW.PMRRO 回報警告，並可能依 SMART AER 設定通知。 <a class="qa-rule-link" href="#common-pmr_op-9">本冊完整規則</a></p>
</li>
<li id="q-234-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>PMRSTS 的 NRDY、HSTS、ERR 是主要證據，SMART 提供 PMR 警告。 <a class="qa-rule-link" href="#common-pmr_op-10">本冊完整規則</a></p>
</li>
<li id="q-234-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>若 PMR 警告符合支援的 PEL Critical Warning hardware event，依事件規則記錄；每次 PMR 讀寫或 EN 切換不是獨立 PEL 事件。 <a class="qa-rule-link" href="#common-pmr_op-11">本冊完整規則</a></p>
</li>
<li id="q-234-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Ready 且已確認持久的內容跨 CLR 保留。 <a class="qa-rule-link" href="#common-pmr_op-12">本冊完整規則</a></p>
</li>
<li id="q-234-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新確認啟用與 Ready 狀態，再檢查 HSTS。 <a class="qa-rule-link" href="#common-pmr_op-13">本冊完整規則</a></p>
</li>
<li id="q-234-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Ready 時已完成且確認持久的寫入應跨 Power Cycle 保留；恢復後仍須確認 HSTS 與 ERR。 <a class="qa-rule-link" href="#common-pmr_op-14">本冊完整規則</a></p>
</li>
<li id="q-234-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>PMR 屬於提供它的 PCIe function，其他存取端也必須核對該 PMR 的健康。 <a class="qa-rule-link" href="#common-pmr_op-15">本冊完整規則</a></p>
</li>
<li id="q-234-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>用 barrier、健康與 EN／NRDY 的順序驗證，不只看最後 EN=0。</p>
</li>
<li id="q-234-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查所有 PMR 使用者是否已停止，以及 barrier 是否真的受支援。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-235" data-question="235"><h2><a class="qa-qid" href="#q-235">Q235</a> Reset 與 Power Cycle 如何影響 PMR 狀態及持久資料？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-235-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-235-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>持久資料與目前可存取狀態不同；即使內容應保留，恢復期間仍可能尚未 Ready。</p>
</li>
<li id="q-235-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>資料保留適用已完成且持久的 PMR 寫入，不擴張到 Host 尚未確認的寫入。</p>
</li>
<li id="q-235-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>重設前保存 barrier 結果，恢復後讀 EN、NRDY、HSTS、ERR 與 mapping。</p>
</li>
<li id="q-235-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>HSTS=Restore Error 表示 PMR 現在運作且持久，但前次內容可能未正確恢復；與目前 Unreliable 意義不同。</p>
</li>
<li id="q-235-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先恢復 Ready，再驗健康，最後按測試保存的內容核對；若同時做 Sanitize，另依清除規則判斷。</p>
</li>
<li id="q-235-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>符合前提的持久資料應跨 CLR、停用與 Power Cycle 保留；Register 保留則依 Reset 來源分別檢查。</p>
</li>
<li id="q-235-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>PMRSTS.ERR 非零會維持到 PCI Function reset；清 CC.EN 不保證把錯誤清零。</p>
</li>
<li id="q-235-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>直接存取 PMR 或其 Register 沒有 NVMe CQE。 <a class="qa-rule-link" href="#common-pmr_op-8">本冊完整規則</a></p>
</li>
<li id="q-235-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>PMR 變成唯讀或不可靠時，SMART.CW.PMRRO 回報警告，並可能依 SMART AER 設定通知。 <a class="qa-rule-link" href="#common-pmr_op-9">本冊完整規則</a></p>
</li>
<li id="q-235-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>PMRSTS 的 NRDY、HSTS、ERR 是主要證據，SMART 提供 PMR 警告。 <a class="qa-rule-link" href="#common-pmr_op-10">本冊完整規則</a></p>
</li>
<li id="q-235-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>若 PMR 警告符合支援的 PEL Critical Warning hardware event，依事件規則記錄；每次 PMR 讀寫或 EN 切換不是獨立 PEL 事件。 <a class="qa-rule-link" href="#common-pmr_op-11">本冊完整規則</a></p>
</li>
<li id="q-235-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Ready 且已確認持久的內容跨 CLR 保留。 <a class="qa-rule-link" href="#common-pmr_op-12">本冊完整規則</a></p>
</li>
<li id="q-235-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新確認啟用與 Ready 狀態，再檢查 HSTS。 <a class="qa-rule-link" href="#common-pmr_op-13">本冊完整規則</a></p>
</li>
<li id="q-235-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Ready 時已完成且確認持久的寫入應跨 Power Cycle 保留；恢復後仍須確認 HSTS 與 ERR。 <a class="qa-rule-link" href="#common-pmr_op-14">本冊完整規則</a></p>
</li>
<li id="q-235-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>PMR 屬於提供它的 PCIe function，其他存取端也必須核對該 PMR 的健康。 <a class="qa-rule-link" href="#common-pmr_op-15">本冊完整規則</a></p>
</li>
<li id="q-235-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>內容、Register 與錯誤狀態分三項驗證，不能只因其中一項符合就宣稱全部通過。</p>
</li>
<li id="q-235-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認失去的是已持久內容，還是尚未完成的寫入或尚未恢復的讀取。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-236" data-question="236"><h2><a class="qa-qid" href="#q-236">Q236</a> Host Memory、HMB、CMB 與 PMR 的存取與生命週期如何比較？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-236-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-236-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>同樣是資料地址，背後可能有不同擁有者、初始化責任與可回收條件。</p>
</li>
<li id="q-236-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>普通 Host buffer 由 Host 管理，命令期間供 controller 存取；HMB 專供 controller；CMB 位於裝置；PMR 額外提供持久性機制。</p>
</li>
<li id="q-236-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>以 HMPRE、CMB/PMR flags 與每筆命令資料指標，確認實際使用哪一種空間。</p>
</li>
<li id="q-236-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>普通 buffer 按命令與 queue 生命週期回收；HMB 等停用完成；CMB 重設後需初始化；PMR 保存前需支援的 barrier 與健康確認。</p>
</li>
<li id="q-236-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先画出 Host 地址、controller 地址與實際記憶體的對應，再標註從何時開始可存取、何時才能回收。</p>
</li>
<li id="q-236-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例如一個成功 Write CQE 可結束其來源 Host buffer 使用，但不代表整塊 HMB 同時釋放，也不代表 PMR barrier 已執行。</p>
</li>
<li id="q-236-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>錯誤回應依違反哪個介面規則決定，不存在統一「記憶體錯誤」Status 可套用全部情況。</p>
</li>
<li id="q-236-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>HMB 透過 Set Features，具有 CQE；CMB／PMR 的直接 Register 存取沒有 CQE。 <a class="qa-rule-link" href="#common-memory_compare-8">本冊完整規則</a></p>
</li>
<li id="q-236-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>配置 HMB、CMB 或 PMR 本身沒有通用成功 AER。PMR 若進入唯讀等符合 SMART 警告的狀態，才依該警告與通知設定回報，不能將 HMB 的正常啟用當成同一種事件。</p>
</li>
<li id="q-236-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>HMB 用 Feature 及實際存取生命週期驗證，CMB 用位置與用途能力驗證，PMR 另需檢查 Ready、ERR、HSTS。這些觀察不是逐次寫入 Error Information 的要求。</p>
</li>
<li id="q-236-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般記憶體存取不是 PEL 事件。支援的 HMB Set Feature 記錄與 PMR 健康／硬體事件需各自符合條件，不能要求每次存取都有事件。</p>
</li>
<li id="q-236-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後 HMB 配置失效；CMB 特定 mapping 可保留，但內容 undefined；PMR 已持久內容保留。 <a class="qa-rule-link" href="#common-memory_compare-12">本冊完整規則</a></p>
</li>
<li id="q-236-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重建受影響控制環境，再分別處理 HMB 配置、CMB 初始化與 PMR 健康檢查；不能把所有記憶體當成同一種保存介面。 <a class="qa-rule-link" href="#common-memory_compare-13">本冊完整規則</a></p>
</li>
<li id="q-236-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>HMB 與 CMB 不提供 PMR 的持久性承諾；PMR 也要先用支援的 write barrier 與健康狀態確認先前寫入。 <a class="qa-rule-link" href="#common-memory_compare-14">本冊完整規則</a></p>
</li>
<li id="q-236-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>先確認記憶體位於 Host 或 controller，再確認使用權與地址空間。 <a class="qa-rule-link" href="#common-memory_compare-15">本冊完整規則</a></p>
</li>
<li id="q-236-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>核對 ownership、mapping、命令完成與持久性各自的證據，避免用「還能讀到資料」代替全部驗證。</p>
</li>
<li id="q-236-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認正在比較的是哪個生命週期：命令、HMB 配置、CMB mapping，還是 PMR 的持久資料。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-cmb_op-8"><h3>本主題的共用條件 · DNR 與 More 應如何設定？</h3><p>CMB Register 與記憶體存取沒有 NVMe CQE；若使用 CMB 的 Admin／I/O 命令回 CQE，才對該命令解讀 DNR、More。不能替 MMIO 寫入編造 Status。</p></article>
<article id="common-cmb_op-12"><h3>本主題的共用條件 · Controller Reset 後是否保留或繼續？</h3><p>CC.EN 觸發的 CLR 與 FLR 保留 CMBMSC，但 CMB 內容變成 undefined。Host 必須重新初始化要使用的內容，特別是 CQ Phase；位址設定保留不等於 queue 或資料有效。</p></article>
<article id="common-cmb_op-13"><h3>本主題的共用條件 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>Subsystem Reset 後重新確認 CMB Register 與 mapping，重建使用它的 queues。不能把 CC.EN／FLR 的特定 CMBMSC 保留規則擴大成所有重設都保留。</p></article>
<article id="common-cmb_op-14"><h3>本主題的共用條件 · Power Cycle 後是否保留或繼續？</h3><p>CMB 不提供 PMR 的跨斷電持久性保證。Power Cycle 後重新配置、初始化，再使用支援的用途。</p></article>
<article id="common-cmb_op-15"><h3>本主題的共用條件 · 是否影響其他 Controller 或 Namespace？</h3><p>CMB 位於 controller，但 Host 與 controller 使用的地址範圍可以不同。需正確轉換相同 offset，並避免與其他 DMA 及 PMR 範圍衝突。</p></article>
<article id="common-command-8"><h3>命令完成、事件與紀錄 · DNR 與 More 應如何設定？</h3><p>只有收到 CQE，才有 DNR 與 More 可供判讀。DNR=1 表示相同命令即使重送到此 NVM subsystem 的任一 controller，仍預期會失敗；DNR=0 則只表示可能成功。除非個別錯誤條件另有明定，不能只看 Status 名稱就要求 DNR=1。More=1 表示 Error Information Log 有這筆命令的補充資訊。SCT=SC=0 時，DNR 應為 0。</p></article>
<article id="common-hmb_op-9"><h3>本主題的共用條件 · 是否產生 Asynchronous Event？</h3><p>啟用或停用 HMB 沒有獨立的成功 AER；若另外發生已定義的硬體錯誤，才依其事件條件回報。</p></article>
<article id="common-hmb_op-10"><h3>本主題的共用條件 · 是否更新 Error Information Log 或其他 Log？</h3><p>Get Features 回報 EHM、HMNARE、HMNAR 與配置資料；它不是 HMB 內容的備份。成功操作不要求 Error entry，失敗則依實際 CQE 與記錄條件判斷。</p></article>
<article id="common-hmb_op-11"><h3>本主題的共用條件 · 是否記錄於 Persistent Event Log？</h3><p>若支援該 FID 的 PEL Set Feature Event，依允許記錄與成功變更條件處理；一般 HMB 讀寫不是逐次 Persistent Event。</p></article>
<article id="common-hmb_op-12"><h3>本主題的共用條件 · Controller Reset 後是否保留或繼續？</h3><p>HMB 資源配置不跨 CLR 保留。重設後應重新提供先前配置的記憶體；只有大小、descriptor 位址與內容、buffer 內容都符合原狀時，才能用 MR=1 表示原記憶體返回。</p></article>
<article id="common-hmb_op-13"><h3>本主題的共用條件 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>Subsystem Reset 使受影響 controller 的 HMB 配置失效，Host 恢復通道後重新配置。舊 Host RAM 的 bytes 還在，不代表 controller 仍有使用權或已知其地址。</p></article>
<article id="common-hmb_op-14"><h3>本主題的共用條件 · Power Cycle 後是否保留或繼續？</h3><p>HMB 不是持久儲存。若供電變化使內容遺失，重新配置應使用 MR=0，不能謊稱原內容仍在。規範要求 controller 在使用 HMB 時，面對 surprise removal 仍確保不因 HMB 造成資料遺失或損壞。</p></article>
<article id="common-hmb_op-15"><h3>本主題的共用條件 · 是否影響其他 Controller 或 Namespace？</h3><p>HMB 是 Host 分配給此 controller 專用的記憶體；啟用期間 Host 不得改寫 descriptor list 或 buffer，也不能把同一區域交給其他用途。這與 namespace 的共享能力無關。</p></article>
<article id="common-memory_compare-8"><h3>本主題的共用條件 · DNR 與 More 應如何設定？</h3><p>HMB 透過 Set Features，具有 CQE；CMB／PMR 的直接 Register 存取沒有 CQE。若是命令使用其中的 buffer，DNR／More 屬於那筆命令，不能替不同存取方式共用一組固定值。</p></article>
<article id="common-memory_compare-12"><h3>本主題的共用條件 · Controller Reset 後是否保留或繼續？</h3><p>CLR 後 HMB 配置失效；CMB 特定 mapping 可保留，但內容 undefined；PMR 已持久內容保留。三者都需依各自狀態重新確認是否可用。</p></article>
<article id="common-memory_compare-13"><h3>本主題的共用條件 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>Subsystem Reset 後重建受影響控制環境，再分別處理 HMB 配置、CMB 初始化與 PMR 健康檢查；不能把所有記憶體當成同一種保存介面。</p></article>
<article id="common-memory_compare-14"><h3>本主題的共用條件 · Power Cycle 後是否保留或繼續？</h3><p>HMB 與 CMB 不提供 PMR 的持久性承諾；PMR 也要先用支援的 write barrier 與健康狀態確認先前寫入。Host RAM 是否另有持久硬體不是這三種 NVMe 介面替它保證。</p></article>
<article id="common-memory_compare-15"><h3>本主題的共用條件 · 是否影響其他 Controller 或 Namespace？</h3><p>先確認記憶體位於 Host 或 controller，再確認使用權與地址空間。相同數字的地址可能經過不同 mapping，不能只比地址值就判定同一個 buffer。</p></article>
<article id="common-pmr_op-8"><h3>本主題的共用條件 · DNR 與 More 應如何設定？</h3><p>直接存取 PMR 或其 Register 沒有 NVMe CQE。使用 PMR buffer 的命令若有 CQE，才解讀其 Status、DNR 與 More；成功 CQE 仍不能取代 PMR 健康與持久性檢查。</p></article>
<article id="common-pmr_op-9"><h3>本主題的共用條件 · 是否產生 Asynchronous Event？</h3><p>PMR 變成唯讀或不可靠時，SMART.CW.PMRRO 回報警告，並可能依 SMART AER 設定通知。通知可能晚於狀態變化，因此從上次確認 HSTS 正常以來的操作都應納入檢查。</p></article>
<article id="common-pmr_op-10"><h3>本主題的共用條件 · 是否更新 Error Information Log 或其他 Log？</h3><p>PMRSTS 的 NRDY、HSTS、ERR 是主要證據，SMART 提供 PMR 警告。Register 存取不要求每次新增 Error Log；使用 PMR 的命令失敗才另依其 CQE 與記錄條件分析。</p></article>
<article id="common-pmr_op-11"><h3>本主題的共用條件 · 是否記錄於 Persistent Event Log？</h3><p>若 PMR 警告符合支援的 PEL Critical Warning hardware event，依事件規則記錄；每次 PMR 讀寫或 EN 切換不是獨立 PEL 事件。</p></article>
<article id="common-pmr_op-12"><h3>本主題的共用條件 · Controller Reset 後是否保留或繼續？</h3><p>Ready 且已確認持久的內容跨 CLR 保留。CC.EN 觸發的 CLR 另保留 PMR 控制／狀態 Register；但仍應確認健康，不能因 Register 保留就忽略 Restore Error。</p></article>
<article id="common-pmr_op-13"><h3>本主題的共用條件 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>Subsystem Reset 後重新確認啟用與 Ready 狀態，再檢查 HSTS。PMR 的資料持久性與 Register 是否須重建是不同問題；Restore Error 表示原內容可能未正確恢復。</p></article>
<article id="common-pmr_op-14"><h3>本主題的共用條件 · Power Cycle 後是否保留或繼續？</h3><p>Ready 時已完成且確認持久的寫入應跨 Power Cycle 保留；恢復後仍須確認 HSTS 與 ERR。Sanitize 可清除 PMR，不能把同時發生的 Sanitize 當成一般斷電遺失。</p></article>
<article id="common-pmr_op-15"><h3>本主題的共用條件 · 是否影響其他 Controller 或 Namespace？</h3><p>PMR 屬於提供它的 PCIe function，其他存取端也必須核對該 PMR 的健康。命令所有 data 與 metadata 必須全部位於 PMR 或全部在其外，不能任意混放。</p></article>
<article id="common-register-9"><h3>Register 存取 · 是否產生 Asynchronous Event？</h3><p>Register 存取本身不定義一筆成功通知。若另外發生 Internal Error 等已定義事件，則依該事件的規則處理。controller 尚不能處理 Admin Queue 時，Host 仍須直接檢查初始化狀態，不能改以等待事件判斷是否已完成初始化。</p></article>
<article id="common-register-10"><h3>Register 存取 · 是否更新 Error Information Log 或其他 Log？</h3><p>規範不要求每次 Register 讀寫都建立一筆 Error Information entry。遇到初始化問題時，先保存 CAP、CC、CSTS、CRTO 及各次觀察的時間。若之後 controller 允許讀取 Log，再用錯誤與事件紀錄補足資訊。</p></article>
<article id="common-register-11"><h3>Register 存取 · 是否記錄於 Persistent Event Log？</h3><p>一般 Register 存取不是獨立的 Persistent Event。若另外發生重設、電源變化或硬體錯誤，則在支援 PEL 且符合對應事件條件時，依規則記錄。因此，不能將每次 CC 寫入都當成一次 Power-on or Reset 事件。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-cmbreg"><strong>Base 2.4 · §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</strong><br>文件頁 67–69, 70–72 · PDF 93–95, 96–98 · Figure 47–48, 52–55</li>
<li id="ref-pmrreg"><strong>Base 2.4 · §3.1.4 (PMR properties)</strong><br>文件頁 73–77 · PDF 99–103 · Figure 58–64</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>文件頁 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-hmb"><strong>Base 2.4 · §5.2.30.2.3, 8.2.4</strong><br>文件頁 515–519, 744 · PDF 541–545, 770 · Figure 545–553</li>
<li id="ref-cmb"><strong>Base 2.4 · §8.2.1 (memory placement and lifetime)</strong><br>文件頁 742–744 · PDF 768–770</li>
<li id="ref-pmr"><strong>Base 2.4 · §8.2.5 (memory behavior; exclude PCIe packet detail)</strong><br>文件頁 745–746 · PDF 771–772</li>
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
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/memory/en/">English</a><a href="/DOCS/nvme-question-bank/memory.html">繁中教學 HTML</a></nav>
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
