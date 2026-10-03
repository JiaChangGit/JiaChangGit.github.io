---
layout: post
title: "NVMe 自問自答題庫：Firmware Update 與 Boot Partition"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/firmware-boot/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/firmware-boot/en/">English</a><a href="/DOCS/nvme-question-bank/firmware-boot.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q136–Q148</p><h1>Firmware Update 與 Boot Partition</h1><p class="qr-intro">先分清下載、提交與啟用，再把 Boot Partition 的讀取和切換放在旁邊比較。資料已傳入 controller，不代表新韌體或新開機映像已開始使用。</p><p>先練習，再展開每題的 17 項解答。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>從映像資料到真正啟用</h2><p class="qa-takeaway">Slot、pending activation 與目前 running revision 各描述一個階段。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">階段</th><th scope="col">查哪些欄位</th><th scope="col">此時能說什麼</th></tr></thead><tbody><tr><td>Download</td><td>OFST、NUMD、完整映像</td><td>資料已傳送，不等於啟用</td></tr><tr><td>Commit</td><td>FS、CA、CQE</td><td>依 Action 存入或安排啟用</td></tr><tr><td>Activation</td><td>所需 reset、FR、CAFS</td><td>確認目前實際版本</td></tr><tr><td>Boot Partition</td><td>ABPID、BRS、FID85h</td><td>判斷映像讀取及保護</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>CA=2 是安排既有 slot 在指定啟用時機生效；若還沒做該步驟，Identify.FR 不必提前改變。Boot 的 CA=7 則是選 Active Partition，不能直接等同一般 Firmware Activation。</p>
<p class="qa-citations">來源：<a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-boot">Base 2.4 §8.1.3–8.1.3.3.3</a> · <a href="#ref-bootreg">Base 2.4 §3.1.4 (BPINFO, BPRSEL, BPMBL)</a> · <a href="#ref-bootprotect">Base 2.4 §5.2.30.1.39</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-136">Q136 · Firmware Slot 的數量、唯讀限制與使用狀態從哪裡查？</a></li>
<li><a href="#q-137">Q137 · Firmware Image Download 如何使用 OFST 與 NUMD？</a></li>
<li><a href="#q-138">Q138 · 下載重疊、缺漏、順序與無效 Image 如何處理？</a></li>
<li><a href="#q-139">Q139 · Firmware Commit 的 FS 與 CA 如何選？</a></li>
<li><a href="#q-140">Q140 · 立即啟用與等待不同 Reset 啟用有何差別？</a></li>
<li><a href="#q-141">Q141 · Firmware Activation Starting 何時產生？</a></li>
<li><a href="#q-142">Q142 · Download、Commit 或 Activation 中發生 Reset／斷電如何處理？</a></li>
<li><a href="#q-143">Q143 · Firmware 載入失敗後如何回復？</a></li>
<li><a href="#q-144">Q144 · Activation 後如何確認版本、Slot 與 Command Effects？</a></li>
<li><a href="#q-145">Q145 · Activation 後哪些設定應保留，哪些需要重新探索？</a></li>
<li><a href="#q-146">Q146 · Boot Partition 支援、狀態與 Active ID 如何確認？</a></li>
<li><a href="#q-147">Q147 · Boot Partition 如何下載、提交與切換 Active？</a></li>
<li><a href="#q-148">Q148 · Boot Partition 更新與 Controller Firmware 更新有何不同？</a></li>
</ol></section>
<article class="qa-question" id="q-136" data-question="136"><h2><a class="qa-qid" href="#q-136">Q136</a> Firmware Slot 的數量、唯讀限制與使用狀態從哪裡查？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-136-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-136-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>原題只用 Firmware Slot Information 判斷全部能力，需要修正：Log 提供 slot 內容與 Active 狀態，數量及 slot1 是否唯讀則在 Identify.FRMW。</p>
</li>
<li id="q-136-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Firmware slots 由同一 domain 的 controllers 共用；查詢前先確認是哪個 domain 的更新。</p>
</li>
<li id="q-136-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>OACS 宣告 firmware download/commit 支援；FRMW 宣告 slot 數、slot1 唯讀與無 Reset 啟用能力。</p>
</li>
<li id="q-136-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>LID03h 中 CAFS 是目前 Active slot，NAFS 是預定下一次適用 Reset 啟用的 slot；FRS1～7 是各 slot 的 revision。</p>
</li>
<li id="q-136-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先讀 FRMW，再讀 LID03h，選可寫且符合更新計畫的 slot；不要透過嘗試覆寫 slot1 來探測它是否唯讀。</p>
</li>
<li id="q-136-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>能分清「存在幾個 slot」、「哪個已有映像」、「目前執行哪個」與「下次準備啟用哪個」。</p>
</li>
<li id="q-136-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>某 slot revision 全為 0 可表示沒有有效映像或不支援，不能只靠 Log 反推 slot 數。非法或唯讀 slot 可回 Invalid Firmware Slot。</p>
</li>
<li id="q-136-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-136-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>開始不經 Reset 的韌體啟用時，受影響 controller 在 Firmware Activation Notices 啟用下回報 Firmware Activation Starting。 <a class="qa-rule-link" href="#common-firmware_op-9">本冊完整規則</a></p>
</li>
<li id="q-136-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>用 Firmware Slot Information 區分目前 Active 與下次 Reset 預定 Active，再用 Identify.FR 確認真正執行的版本。 <a class="qa-rule-link" href="#common-firmware_op-10">本冊完整規則</a></p>
</li>
<li id="q-136-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 時，Firmware Commit 完成記錄 Event02h，含舊版本、要求啟用的新版本、CA、slot 與 Status。 <a class="qa-rule-link" href="#common-firmware_op-11">本冊完整規則</a></p>
</li>
<li id="q-136-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Download 後、Commit 完成前若發生 Controller Level Reset，已下載的暫存映像部分必須丟棄。 <a class="qa-rule-link" href="#common-firmware_op-12">本冊完整規則</a></p>
</li>
<li id="q-136-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 會影響其涵蓋的 controllers，並可滿足明確要求此 Reset 的待啟用映像。 <a class="qa-rule-link" href="#common-firmware_op-13">本冊完整規則</a></p>
</li>
<li id="q-136-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>若在要求啟用的 Commit 尚未完成時進入 D3cold，恢復後可使用原映像或該次新映像，必須實際查證。 <a class="qa-rule-link" href="#common-firmware_op-14">本冊完整規則</a></p>
</li>
<li id="q-136-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 domain 的 controllers 共用 firmware slots，該 domain 使用相同映像；單一 domain 時即涵蓋 subsystem。 <a class="qa-rule-link" href="#common-firmware_op-15">本冊完整規則</a></p>
</li>
<li id="q-136-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Identify.FR 應對應真正執行中的版本，而不是直接取 NAFS 指向的 pending revision。</p>
</li>
<li id="q-136-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查 FRMW，避免把尚未使用的 slot 當成不存在。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-137" data-question="137"><h2><a class="qa-qid" href="#q-137">Q137</a> Firmware Image Download 如何使用 OFST 與 NUMD？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-137-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-137-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>分段下載讓 Host 不必一次提供完整映像，但每段的位置與長度必須能正確重組。</p>
</li>
<li id="q-137-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>OFST 相對於整份待更新映像，不是相對於這一段的 Host buffer。</p>
</li>
<li id="q-137-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>檢查 FWUG 的對齊／粒度限制與 MDTS 等傳輸限制。FWUG 特殊值要依欄位解讀，不能一律當成一般倍數。</p>
</li>
<li id="q-137-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>OFST 以 Dword 為單位；NUMD 為零起算 Dword 數。位元組起點=OFST×4，長度=(NUMD+1)×4。</p>
</li>
<li id="q-137-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>假設每段 4096 bytes，第一段 OFST=0、NUMD=1023，第二段 OFST=1024、NUMD=1023；每段 buffer 都指向該段實際資料。</p>
</li>
<li id="q-137-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Download Success 只表示該段下載完成，還沒有 Commit，也沒有啟用新映像。</p>
</li>
<li id="q-137-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不符合 FWUG 時 controller 可回 Invalid Field；重疊範圍可回 Overlapping Range。單位錯誤會同時造成錯誤位移與資料缺口。</p>
</li>
<li id="q-137-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-137-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>開始不經 Reset 的韌體啟用時，受影響 controller 在 Firmware Activation Notices 啟用下回報 Firmware Activation Starting。 <a class="qa-rule-link" href="#common-firmware_op-9">本冊完整規則</a></p>
</li>
<li id="q-137-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>用 Firmware Slot Information 區分目前 Active 與下次 Reset 預定 Active，再用 Identify.FR 確認真正執行的版本。 <a class="qa-rule-link" href="#common-firmware_op-10">本冊完整規則</a></p>
</li>
<li id="q-137-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 時，Firmware Commit 完成記錄 Event02h，含舊版本、要求啟用的新版本、CA、slot 與 Status。 <a class="qa-rule-link" href="#common-firmware_op-11">本冊完整規則</a></p>
</li>
<li id="q-137-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Download 後、Commit 完成前若發生 Controller Level Reset，已下載的暫存映像部分必須丟棄。 <a class="qa-rule-link" href="#common-firmware_op-12">本冊完整規則</a></p>
</li>
<li id="q-137-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 會影響其涵蓋的 controllers，並可滿足明確要求此 Reset 的待啟用映像。 <a class="qa-rule-link" href="#common-firmware_op-13">本冊完整規則</a></p>
</li>
<li id="q-137-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>若在要求啟用的 Commit 尚未完成時進入 D3cold，恢復後可使用原映像或該次新映像，必須實際查證。 <a class="qa-rule-link" href="#common-firmware_op-14">本冊完整規則</a></p>
</li>
<li id="q-137-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 domain 的 controllers 共用 firmware slots，該 domain 使用相同映像；單一 domain 時即涵蓋 subsystem。 <a class="qa-rule-link" href="#common-firmware_op-15">本冊完整規則</a></p>
</li>
<li id="q-137-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>用每段的起點、終點與長度核對完整覆蓋，並與原始映像內容比對。</p>
</li>
<li id="q-137-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查 NUMD 是否少減了 1，OFST 是否誤用 bytes。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-138" data-question="138"><h2><a class="qa-qid" href="#q-138">Q138</a> 下載重疊、缺漏、順序與無效 Image 如何處理？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-138-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-138-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>需要區分分段傳輸錯誤與整份映像驗證失敗。每段成功，仍可能因資料缺漏或格式錯誤而不能 Commit。</p>
</li>
<li id="q-138-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>同一更新流程應只處理一份映像，並使用同一 controller；不要將兩份 firmware 或 Boot Partition 的下載交錯。</p>
</li>
<li id="q-138-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>確認 FWUG、映像需求與支援時的 Multiple Update Detected 能力。</p>
</li>
<li id="q-138-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Firmware pieces 可以亂序；Boot Partition pieces 必須由映像開頭依序提交。Overlapping Range 與 MUD 是不同資訊，前者檢查範圍，後者報告更新流程重疊。</p>
</li>
<li id="q-138-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>在 Host 建立段落清單，確認無缺口、無重疊且全部成功，再 Commit；一份流程結束後才開始下一份。</p>
</li>
<li id="q-138-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>有效完整映像應能進入適用 Commit 流程；不能要求每一段都單獨驗證整份映像。</p>
</li>
<li id="q-138-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>重疊可回 1/14h；Commit 驗證不合法可回 1/07h。多個更新流程重疊的結果可能未定義，不能要求固定錯誤碼來補救 Host 違反建議。</p>
</li>
<li id="q-138-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-138-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>開始不經 Reset 的韌體啟用時，受影響 controller 在 Firmware Activation Notices 啟用下回報 Firmware Activation Starting。 <a class="qa-rule-link" href="#common-firmware_op-9">本冊完整規則</a></p>
</li>
<li id="q-138-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>用 Firmware Slot Information 區分目前 Active 與下次 Reset 預定 Active，再用 Identify.FR 確認真正執行的版本。 <a class="qa-rule-link" href="#common-firmware_op-10">本冊完整規則</a></p>
</li>
<li id="q-138-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 時，Firmware Commit 完成記錄 Event02h，含舊版本、要求啟用的新版本、CA、slot 與 Status。 <a class="qa-rule-link" href="#common-firmware_op-11">本冊完整規則</a></p>
</li>
<li id="q-138-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Download 後、Commit 完成前若發生 Controller Level Reset，已下載的暫存映像部分必須丟棄。 <a class="qa-rule-link" href="#common-firmware_op-12">本冊完整規則</a></p>
</li>
<li id="q-138-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 會影響其涵蓋的 controllers，並可滿足明確要求此 Reset 的待啟用映像。 <a class="qa-rule-link" href="#common-firmware_op-13">本冊完整規則</a></p>
</li>
<li id="q-138-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>若在要求啟用的 Commit 尚未完成時進入 D3cold，恢復後可使用原映像或該次新映像，必須實際查證。 <a class="qa-rule-link" href="#common-firmware_op-14">本冊完整規則</a></p>
</li>
<li id="q-138-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 domain 的 controllers 共用 firmware slots，該 domain 使用相同映像；單一 domain 時即涵蓋 subsystem。 <a class="qa-rule-link" href="#common-firmware_op-15">本冊完整規則</a></p>
</li>
<li id="q-138-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>保留 Download 範圍與 Commit CQE，區分傳輸完成、資料完整與映像可啟用。</p>
</li>
<li id="q-138-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否把 Boot 的必須依序規則誤套到一般 firmware，或反過來。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-boot">Base 2.4 §8.1.3–8.1.3.3.3</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-139" data-question="139"><h2><a class="qa-qid" href="#q-139">Q139</a> Firmware Commit 的 FS 與 CA 如何選？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-139-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-139-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Commit 可以只保存、安排下次啟用，或立即啟用；選擇取決於更新計畫與裝置能力，不是每次都用同一個 CA。</p>
</li>
<li id="q-139-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>FS 選 firmware slot；Boot 操作用 BPID，不能把 BPID 當成更多的 firmware slots。</p>
</li>
<li id="q-139-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀 FRMW、目前 slot、pending slot 與 MTFA，確認無 Reset 啟用是否適合。</p>
</li>
<li id="q-139-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CA0=保存不啟用；CA1=保存並在下次 CLR 啟用；CA2=下次 CLR 啟用既有 slot；CA3=立即啟用。FS=0 讓 controller 選 slot1～7。</p>
</li>
<li id="q-139-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先完成需要的 Download，再送選定的 Commit；如果只啟用既有映像，就不必先下載相同內容。</p>
</li>
<li id="q-139-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>CA0 成功不改 running version；CA1／2 需等待適用 Reset；CA3 的 Commit 保持執行中直到啟用成功或失敗。</p>
</li>
<li id="q-139-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>唯讀／非法 slot 回 Invalid Firmware Slot；非法映像回 Invalid Firmware Image；需更強 Reset 的回覆表示 Commit 已保存但啟用還缺步驟。</p>
</li>
<li id="q-139-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-139-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>開始不經 Reset 的韌體啟用時，受影響 controller 在 Firmware Activation Notices 啟用下回報 Firmware Activation Starting。 <a class="qa-rule-link" href="#common-firmware_op-9">本冊完整規則</a></p>
</li>
<li id="q-139-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>用 Firmware Slot Information 區分目前 Active 與下次 Reset 預定 Active，再用 Identify.FR 確認真正執行的版本。 <a class="qa-rule-link" href="#common-firmware_op-10">本冊完整規則</a></p>
</li>
<li id="q-139-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 時，Firmware Commit 完成記錄 Event02h，含舊版本、要求啟用的新版本、CA、slot 與 Status。 <a class="qa-rule-link" href="#common-firmware_op-11">本冊完整規則</a></p>
</li>
<li id="q-139-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Download 後、Commit 完成前若發生 Controller Level Reset，已下載的暫存映像部分必須丟棄。 <a class="qa-rule-link" href="#common-firmware_op-12">本冊完整規則</a></p>
</li>
<li id="q-139-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 會影響其涵蓋的 controllers，並可滿足明確要求此 Reset 的待啟用映像。 <a class="qa-rule-link" href="#common-firmware_op-13">本冊完整規則</a></p>
</li>
<li id="q-139-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>若在要求啟用的 Commit 尚未完成時進入 D3cold，恢復後可使用原映像或該次新映像，必須實際查證。 <a class="qa-rule-link" href="#common-firmware_op-14">本冊完整規則</a></p>
</li>
<li id="q-139-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 domain 的 controllers 共用 firmware slots，該 domain 使用相同映像；單一 domain 時即涵蓋 subsystem。 <a class="qa-rule-link" href="#common-firmware_op-15">本冊完整規則</a></p>
</li>
<li id="q-139-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>用 CA 解釋 FR、CAFS 與 NAFS 的預期變化，不要求所有 CA 都立即更新 FR。</p>
</li>
<li id="q-139-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查實際 CA，避免把只保存的操作誤判成啟用失敗。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-140" data-question="140"><h2><a class="qa-qid" href="#q-140">Q140</a> 立即啟用與等待不同 Reset 啟用有何差別？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-140-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-140-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>立即啟用可保留 controller 操作環境，但映像變更可能要求 Reset 才能安全切換。Host 必須尊重 Commit 指定的 Reset 類型。</p>
</li>
<li id="q-140-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>啟用影響同一 domain 的 controllers；Reset 本身的範圍可能再涵蓋更多 controller。</p>
</li>
<li id="q-140-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>看 FRMW 的無 Reset 啟用能力、MTFA 與 Commit Status；能力支援不保證每一份映像都可立即啟用。</p>
</li>
<li id="q-140-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>1/0Bh 要 Conventional Reset，1/10h 要 Subsystem Reset，1/11h 要 CLR；1/12h 表示立即啟用需超過 MTFA，映像已 Commit 但未啟用。</p>
</li>
<li id="q-140-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>CA3 若成功就查新版本；若回要求 Reset，安排對應 Reset 再初始化與查版本。只做較小 Reset 不能滿足明定的較大 Reset 要求。</p>
</li>
<li id="q-140-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>CA1／2 回 Success 時，任一適用 CLR 方法即可啟用；若特別回要求 Conventional 或 Subsystem Reset，則等待那種類型。</p>
</li>
<li id="q-140-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>例如要求 Conventional Reset 後只清 CC.EN，controller 應繼續執行原映像，不能以 FR 沒變判違規。</p>
</li>
<li id="q-140-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-140-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>開始不經 Reset 的韌體啟用時，受影響 controller 在 Firmware Activation Notices 啟用下回報 Firmware Activation Starting。 <a class="qa-rule-link" href="#common-firmware_op-9">本冊完整規則</a></p>
</li>
<li id="q-140-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>用 Firmware Slot Information 區分目前 Active 與下次 Reset 預定 Active，再用 Identify.FR 確認真正執行的版本。 <a class="qa-rule-link" href="#common-firmware_op-10">本冊完整規則</a></p>
</li>
<li id="q-140-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 時，Firmware Commit 完成記錄 Event02h，含舊版本、要求啟用的新版本、CA、slot 與 Status。 <a class="qa-rule-link" href="#common-firmware_op-11">本冊完整規則</a></p>
</li>
<li id="q-140-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Download 後、Commit 完成前若發生 Controller Level Reset，已下載的暫存映像部分必須丟棄。 <a class="qa-rule-link" href="#common-firmware_op-12">本冊完整規則</a></p>
</li>
<li id="q-140-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 會影響其涵蓋的 controllers，並可滿足明確要求此 Reset 的待啟用映像。 <a class="qa-rule-link" href="#common-firmware_op-13">本冊完整規則</a></p>
</li>
<li id="q-140-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>若在要求啟用的 Commit 尚未完成時進入 D3cold，恢復後可使用原映像或該次新映像，必須實際查證。 <a class="qa-rule-link" href="#common-firmware_op-14">本冊完整規則</a></p>
</li>
<li id="q-140-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 domain 的 controllers 共用 firmware slots，該 domain 使用相同映像；單一 domain 時即涵蓋 subsystem。 <a class="qa-rule-link" href="#common-firmware_op-15">本冊完整規則</a></p>
</li>
<li id="q-140-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>同時記錄 CA、Status、實際 Reset 來源與恢復後 FR，才能判斷啟用是否符合規範。</p>
</li>
<li id="q-140-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查做的是哪種 Reset，而不是只看 Host 介面都叫「reset」。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-141" data-question="141"><h2><a class="qa-qid" href="#q-141">Q141</a> Firmware Activation Starting 何時產生？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-141-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-141-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這個事件讓 Host 知道 controller 將進行不經 Reset 的韌體啟用，可能暫停處理；它不是啟用已成功的通知。</p>
</li>
<li id="q-141-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>受新映像影響的 controllers 各自依通知設定回報，並不只限於提交 Commit 的 controller。</p>
</li>
<li id="q-141-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>確認 Firmware Activation Notices 已啟用、AER 已掛入，以及 FRMW／MTFA 等啟用資訊。</p>
</li>
<li id="q-141-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>AER 的 Notice 類型、Firmware Activation Starting 資訊及 LID03h 引導 Host 查 slot；CSTS.PP 表示處理暫停狀態。</p>
</li>
<li id="q-141-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>Commit CA3 開始啟用時處理通知，依 PP 觀察恢復，再查 Commit 結果與 FR。不要在收到 Starting 後立即把新版本列為成功。</p>
</li>
<li id="q-141-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功證據是適用 Commit 完成與實際 running revision；Starting 只證明已開始相應流程。</p>
</li>
<li id="q-141-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>沒有啟用通知或沒有可完成的 AER 時，不能期待同樣的即時 CQE。載入失敗則另有 Firmware Image Load Error。</p>
</li>
<li id="q-141-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-141-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>開始不經 Reset 的韌體啟用時，受影響 controller 在 Firmware Activation Notices 啟用下回報 Firmware Activation Starting。 <a class="qa-rule-link" href="#common-firmware_op-9">本冊完整規則</a></p>
</li>
<li id="q-141-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>用 Firmware Slot Information 區分目前 Active 與下次 Reset 預定 Active，再用 Identify.FR 確認真正執行的版本。 <a class="qa-rule-link" href="#common-firmware_op-10">本冊完整規則</a></p>
</li>
<li id="q-141-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 時，Firmware Commit 完成記錄 Event02h，含舊版本、要求啟用的新版本、CA、slot 與 Status。 <a class="qa-rule-link" href="#common-firmware_op-11">本冊完整規則</a></p>
</li>
<li id="q-141-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Download 後、Commit 完成前若發生 Controller Level Reset，已下載的暫存映像部分必須丟棄。 <a class="qa-rule-link" href="#common-firmware_op-12">本冊完整規則</a></p>
</li>
<li id="q-141-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 會影響其涵蓋的 controllers，並可滿足明確要求此 Reset 的待啟用映像。 <a class="qa-rule-link" href="#common-firmware_op-13">本冊完整規則</a></p>
</li>
<li id="q-141-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>若在要求啟用的 Commit 尚未完成時進入 D3cold，恢復後可使用原映像或該次新映像，必須實際查證。 <a class="qa-rule-link" href="#common-firmware_op-14">本冊完整規則</a></p>
</li>
<li id="q-141-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 domain 的 controllers 共用 firmware slots，該 domain 使用相同映像；單一 domain 時即涵蓋 subsystem。 <a class="qa-rule-link" href="#common-firmware_op-15">本冊完整規則</a></p>
</li>
<li id="q-141-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>比較事件時間、PP 與 Commit 完成，辨別真正卡住與 Host 尚未處理通知。</p>
</li>
<li id="q-141-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查 AEC 的 Firmware Activation Notices，而不是只看是否送過任意 AER。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-142" data-question="142"><h2><a class="qa-qid" href="#q-142">Q142</a> Download、Commit 或 Activation 中發生 Reset／斷電如何處理？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-142-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-142-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>更新有暫存下載、保存到 slot、啟用三個階段，各自的持久性不同；復原時先定位中斷在哪一階段。</p>
</li>
<li id="q-142-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>保存與啟用的範圍是 domain；中斷也可能讓所有共享 controllers 同時失去通訊。</p>
</li>
<li id="q-142-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>保存最後完成的 Download／Commit、CA、FS、FR 及 slot Log，恢復後再次讀取。</p>
</li>
<li id="q-142-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CLR 發生在 Download 與 Commit 完成之間時，controller 必須丟棄下載部分。啟用 Commit 期間進入 D3cold，恢復可使用原映像或新映像。</p>
</li>
<li id="q-142-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>恢復通道後查實際版本與 slot；未完成 Commit 的映像重新下載，不從原暫存 offset 自行續傳。</p>
</li>
<li id="q-142-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>已知目前執行版本、pending 狀態與可用能力後，才能決定重試、重新 Commit 或已完成。</p>
</li>
<li id="q-142-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>沒有 CQE 時不能補造成功或失敗碼。新版本未啟用可能是合法保留原版本，而不是必然毀損。</p>
</li>
<li id="q-142-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-142-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>開始不經 Reset 的韌體啟用時，受影響 controller 在 Firmware Activation Notices 啟用下回報 Firmware Activation Starting。 <a class="qa-rule-link" href="#common-firmware_op-9">本冊完整規則</a></p>
</li>
<li id="q-142-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>用 Firmware Slot Information 區分目前 Active 與下次 Reset 預定 Active，再用 Identify.FR 確認真正執行的版本。 <a class="qa-rule-link" href="#common-firmware_op-10">本冊完整規則</a></p>
</li>
<li id="q-142-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 時，Firmware Commit 完成記錄 Event02h，含舊版本、要求啟用的新版本、CA、slot 與 Status。 <a class="qa-rule-link" href="#common-firmware_op-11">本冊完整規則</a></p>
</li>
<li id="q-142-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Download 後、Commit 完成前若發生 Controller Level Reset，已下載的暫存映像部分必須丟棄。 <a class="qa-rule-link" href="#common-firmware_op-12">本冊完整規則</a></p>
</li>
<li id="q-142-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 會影響其涵蓋的 controllers，並可滿足明確要求此 Reset 的待啟用映像。 <a class="qa-rule-link" href="#common-firmware_op-13">本冊完整規則</a></p>
</li>
<li id="q-142-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>若在要求啟用的 Commit 尚未完成時進入 D3cold，恢復後可使用原映像或該次新映像，必須實際查證。 <a class="qa-rule-link" href="#common-firmware_op-14">本冊完整規則</a></p>
</li>
<li id="q-142-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 domain 的 controllers 共用 firmware slots，該 domain 使用相同映像；單一 domain 時即涵蓋 subsystem。 <a class="qa-rule-link" href="#common-firmware_op-15">本冊完整規則</a></p>
</li>
<li id="q-142-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>使用 PEL Commit 與 Reset Event 補足歷史，但 NFR 只記要求版本，仍須與 FR 比對。</p>
</li>
<li id="q-142-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查最後一筆真正完成的 Commit，而不是最後一段已下載的資料。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-143" data-question="143"><h2><a class="qa-qid" href="#q-143">Q143</a> Firmware 載入失敗後如何回復？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-143-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-143-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>裝置需要在新映像無法載入時恢復可運作映像，但可回復到什麼內容仍取決於先前有效 slot 或 baseline 是否存在。</p>
</li>
<li id="q-143-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>失敗與回復影響該映像涵蓋的 controllers；不應以單一 slot 的內容推論整個更新歷史。</p>
</li>
<li id="q-143-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 FR、CAFS／NAFS、各 slot revision、Firmware Image Load Error 與 PEL。</p>
</li>
<li id="q-143-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>新映像無法載入時，controller 必須回復至最近已啟用 slot 的映像，或可用的 baseline 唯讀映像，並回報 Firmware Image Load Error。</p>
</li>
<li id="q-143-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>恢復後讀實際 FR，確認是否回到可用映像，再檢查失敗的 Commit／activation 狀態；不要立即反覆啟用同一失敗映像。</p>
</li>
<li id="q-143-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>controller 可恢復舊版本運作，同時保留更新失敗的證據；舊版本運作不表示前次更新成功。</p>
</li>
<li id="q-143-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>如果 Host 已覆寫 Active slot，舊映像可能不再存在，因此不能保證永遠回到某個特定歷史版本。</p>
</li>
<li id="q-143-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-143-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>開始不經 Reset 的韌體啟用時，受影響 controller 在 Firmware Activation Notices 啟用下回報 Firmware Activation Starting。 <a class="qa-rule-link" href="#common-firmware_op-9">本冊完整規則</a></p>
</li>
<li id="q-143-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>用 Firmware Slot Information 區分目前 Active 與下次 Reset 預定 Active，再用 Identify.FR 確認真正執行的版本。 <a class="qa-rule-link" href="#common-firmware_op-10">本冊完整規則</a></p>
</li>
<li id="q-143-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 時，Firmware Commit 完成記錄 Event02h，含舊版本、要求啟用的新版本、CA、slot 與 Status。 <a class="qa-rule-link" href="#common-firmware_op-11">本冊完整規則</a></p>
</li>
<li id="q-143-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Download 後、Commit 完成前若發生 Controller Level Reset，已下載的暫存映像部分必須丟棄。 <a class="qa-rule-link" href="#common-firmware_op-12">本冊完整規則</a></p>
</li>
<li id="q-143-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 會影響其涵蓋的 controllers，並可滿足明確要求此 Reset 的待啟用映像。 <a class="qa-rule-link" href="#common-firmware_op-13">本冊完整規則</a></p>
</li>
<li id="q-143-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>若在要求啟用的 Commit 尚未完成時進入 D3cold，恢復後可使用原映像或該次新映像，必須實際查證。 <a class="qa-rule-link" href="#common-firmware_op-14">本冊完整規則</a></p>
</li>
<li id="q-143-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 domain 的 controllers 共用 firmware slots，該 domain 使用相同映像；單一 domain 時即涵蓋 subsystem。 <a class="qa-rule-link" href="#common-firmware_op-15">本冊完整規則</a></p>
</li>
<li id="q-143-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>核對實際 slot 內容與可用 baseline，避免測試把不存在的舊映像當成必須回復的對象。</p>
</li>
<li id="q-143-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查 Active slot 是否曾被覆寫，這會直接影響可回復映像。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-144" data-question="144"><h2><a class="qa-qid" href="#q-144">Q144</a> Activation 後如何確認版本、Slot 與 Command Effects？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-144-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-144-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>啟用完成後可能改變能力與命令效果，Host 必須更新快取，不能只看版本字串就沿用所有舊設定假設。</p>
</li>
<li id="q-144-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>查詢涵蓋受影響 domain 的 controller 與 namespaces，並保留相同身分以便前後比較。</p>
</li>
<li id="q-144-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀 Identify.FR、FRMW、CAP、Firmware Slot Information，並重新取得適用 CSI 的 Commands Supported and Effects。</p>
</li>
<li id="q-144-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CAFS 表示現行 slot，NAFS 表示待啟用安排，FR 是 running revision；Effects 的 CSUPP／CCC／NCC／NIC 等說明支援及可能影響。</p>
</li>
<li id="q-144-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先確認啟用真的完成，再重新查能力，最後依新宣告重新驗證需要使用的命令與格式。</p>
</li>
<li id="q-144-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>FR、目前 slot revision 與啟用結果應能互相解釋；pending slot 尚未啟用時，不應要求 FR 提前更新。</p>
</li>
<li id="q-144-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>查詢失敗先看 Ready／media 限制與新能力，不直接判定映像損壞。</p>
</li>
<li id="q-144-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-144-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>開始不經 Reset 的韌體啟用時，受影響 controller 在 Firmware Activation Notices 啟用下回報 Firmware Activation Starting。 <a class="qa-rule-link" href="#common-firmware_op-9">本冊完整規則</a></p>
</li>
<li id="q-144-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>用 Firmware Slot Information 區分目前 Active 與下次 Reset 預定 Active，再用 Identify.FR 確認真正執行的版本。 <a class="qa-rule-link" href="#common-firmware_op-10">本冊完整規則</a></p>
</li>
<li id="q-144-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 時，Firmware Commit 完成記錄 Event02h，含舊版本、要求啟用的新版本、CA、slot 與 Status。 <a class="qa-rule-link" href="#common-firmware_op-11">本冊完整規則</a></p>
</li>
<li id="q-144-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Download 後、Commit 完成前若發生 Controller Level Reset，已下載的暫存映像部分必須丟棄。 <a class="qa-rule-link" href="#common-firmware_op-12">本冊完整規則</a></p>
</li>
<li id="q-144-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 會影響其涵蓋的 controllers，並可滿足明確要求此 Reset 的待啟用映像。 <a class="qa-rule-link" href="#common-firmware_op-13">本冊完整規則</a></p>
</li>
<li id="q-144-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>若在要求啟用的 Commit 尚未完成時進入 D3cold，恢復後可使用原映像或該次新映像，必須實際查證。 <a class="qa-rule-link" href="#common-firmware_op-14">本冊完整規則</a></p>
</li>
<li id="q-144-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 domain 的 controllers 共用 firmware slots，該 domain 使用相同映像；單一 domain 時即涵蓋 subsystem。 <a class="qa-rule-link" href="#common-firmware_op-15">本冊完整規則</a></p>
</li>
<li id="q-144-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>比較有效欄位與真正變更，避免把保留欄位或不適用 CSI 的資料列當成不一致。</p>
</li>
<li id="q-144-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先排除 Host 使用舊 Identify／Effects buffer 的快取問題。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-145" data-question="145"><h2><a class="qa-qid" href="#q-145">Q145</a> Activation 後哪些設定應保留，哪些需要重新探索？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-145-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-145-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>不能要求整份 Identify、Feature 與所有 bytes 都不變。韌體可更新能力；但使用者資料、namespace 配置及各功能的持久性仍需遵守其規則。</p>
</li>
<li id="q-145-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>先區分不經 Reset 的啟用與實際執行 Reset；後者會另外觸發 queue、Feature 與 Register 的重設規則。</p>
</li>
<li id="q-145-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>比較 Feature 的 Saved／Current／持續性、namespace 身分／attachment，以及新 Identify 能力與 UUID List。</p>
</li>
<li id="q-145-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>FR 預期反映 running image；Current Feature 不可僅依版本字串推論。UUID slot 的不相容變更可能要求 Reset，避免舊 UUID Index 指向另一個意思。</p>
</li>
<li id="q-145-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>建立更新前基準，記錄 CA 與實際 Reset，更新後按每項功能的保留規則分類比對，再重新配置必要的 Host 狀態。</p>
</li>
<li id="q-145-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>結果應符合所執行的更新與 Reset 路徑；正常能力變更與不應遺失的資料／配置要分開驗證。</p>
</li>
<li id="q-145-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不能只用「版本變了所以全部可重設」合理化遺失；也不能用「只是更新」要求 I/O queues 跨真正 Reset 有效。</p>
</li>
<li id="q-145-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-145-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>開始不經 Reset 的韌體啟用時，受影響 controller 在 Firmware Activation Notices 啟用下回報 Firmware Activation Starting。 <a class="qa-rule-link" href="#common-firmware_op-9">本冊完整規則</a></p>
</li>
<li id="q-145-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>用 Firmware Slot Information 區分目前 Active 與下次 Reset 預定 Active，再用 Identify.FR 確認真正執行的版本。 <a class="qa-rule-link" href="#common-firmware_op-10">本冊完整規則</a></p>
</li>
<li id="q-145-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 時，Firmware Commit 完成記錄 Event02h，含舊版本、要求啟用的新版本、CA、slot 與 Status。 <a class="qa-rule-link" href="#common-firmware_op-11">本冊完整規則</a></p>
</li>
<li id="q-145-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Download 後、Commit 完成前若發生 Controller Level Reset，已下載的暫存映像部分必須丟棄。 <a class="qa-rule-link" href="#common-firmware_op-12">本冊完整規則</a></p>
</li>
<li id="q-145-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 會影響其涵蓋的 controllers，並可滿足明確要求此 Reset 的待啟用映像。 <a class="qa-rule-link" href="#common-firmware_op-13">本冊完整規則</a></p>
</li>
<li id="q-145-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>若在要求啟用的 Commit 尚未完成時進入 D3cold，恢復後可使用原映像或該次新映像，必須實際查證。 <a class="qa-rule-link" href="#common-firmware_op-14">本冊完整規則</a></p>
</li>
<li id="q-145-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>同一 domain 的 controllers 共用 firmware slots，該 domain 使用相同映像；單一 domain 時即涵蓋 subsystem。 <a class="qa-rule-link" href="#common-firmware_op-15">本冊完整規則</a></p>
</li>
<li id="q-145-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>把差異逐項對應來源要求，記錄新能力、應保留值及必須重建值。</p>
</li>
<li id="q-145-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認是否真的發生 CLR，再判斷 Feature 與 queue 的預期。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-uuid">Base 2.4 §8.1.31.1–8.1.31.2</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-146" data-question="146"><h2><a class="qa-qid" href="#q-146">Q146</a> Boot Partition 支援、狀態與 Active ID 如何確認？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-146-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-146-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Boot Partition 可讓 Host 在建立 queue 或啟用 controller 前，透過簡化介面讀取開機映像。它不是一般 namespace 的 LBA 區間。</p>
</li>
<li id="q-146-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>支援時有兩個等大的 partitions，ID=0／1；多個 controllers 可能共用它們。</p>
</li>
<li id="q-146-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先讀 CAP.BPS，再讀 BPINFO 的 ABPID、BPSZ、BRS；保護能力看 Identify.BPC，支援時也可讀 Boot Partition Log15h。</p>
</li>
<li id="q-146-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>BPMBL 提供 Host buffer 位址，BPRSEL 指定 BPID、讀取 offset 與大小；BPINFO.BRS 回報進行中、成功或錯誤。</p>
</li>
<li id="q-146-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>配置實體連續 buffer，確認沒有讀取進行中，設定位址與讀取選擇，再等待 BRS 完成。讀取中不得 Reset、Shutdown 或變更相關傳輸屬性。</p>
</li>
<li id="q-146-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>BRS=10b 表示要求內容已傳到 buffer；11b 表示傳輸錯誤。這個 Register 讀取流程沒有 NVMe CQE。</p>
</li>
<li id="q-146-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不要為 BPRSEL 寫入指定 Invalid Field CQE。Log 路徑才按 Get Log Page 的參數與完成規則判讀。</p>
</li>
<li id="q-146-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>Register 讀取流程沒有 CQE，因此沒有 DNR／More；若使用 LID15h 則解讀該 Get Log Page 的 CQE。</p>
</li>
<li id="q-146-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Boot Partition Register 讀取不定義成功 AER。使用 Log 也不因讀取成功就產生 Firmware Activation Starting。</p>
</li>
<li id="q-146-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Register 路徑以 BPINFO.BRS 回報讀取狀態，不會產生 Firmware Slot Log 更新。Get Log Page 路徑則回傳選定 Boot Partition 的資料；讀取失敗依其 CQE 與錯誤記錄條件判斷。</p>
</li>
<li id="q-146-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Boot 讀取不是 Firmware Commit Event；只有另行完成 Commit 時才依 PEL 規則記錄。</p>
</li>
<li id="q-146-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Boot Partition 內容不是隨 CLR 清除的 queue 資料；但 Host 不得在 Register 讀取進行中執行 Reset。重設後重新檢查屬性與 BRS，不能沿用未完成讀取的成功假設。</p>
</li>
<li id="q-146-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新探索共享 Boot Partitions 與讀取狀態；這不是刪除 Boot 映像的操作。若先前讀取未完成，不得將舊 buffer 當作已成功取得完整資料。</p>
</li>
<li id="q-146-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Boot 映像保存在非揮發儲存中，Power Cycle 後重新讀取。FID85h 的預設保護為 Write Locked；保護狀態與映像內容是兩項不同資訊。</p>
</li>
<li id="q-146-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>多個 controllers 可共用 Boot Partitions。查詢時確認目前 controller 的 CAP、BPINFO 與共享關係，不以某台 controller 的讀取完成推論其他台的獨立 buffer 也已完成。</p>
</li>
<li id="q-146-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>將 CAP、ABPID、size、BRS 與實際讀回內容一起確認，不能只靠 ABPID 就宣告映像有效。</p>
</li>
<li id="q-146-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認使用 Register 還是 Log 讀取介面，避免混用 offset、完成與錯誤表示。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-boot">Base 2.4 §8.1.3–8.1.3.3.3</a> · <a href="#ref-bootreg">Base 2.4 §3.1.4 (BPINFO, BPRSEL, BPMBL)</a> · <a href="#ref-bootlog">Base 2.4 §5.2.13.1.21</a> · <a href="#ref-bootprotect">Base 2.4 §5.2.30.1.39</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-147" data-question="147"><h2><a class="qa-qid" href="#q-147">Q147</a> Boot Partition 如何下載、提交與切換 Active？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-147-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-147-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>兩個 partitions 讓 Host 可以先更新非 Active 的一份，讀回確認後才切換，減少中斷更新造成不可用開機映像的風險。</p>
</li>
<li id="q-147-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>BPID 指定要寫入或標為 Active 的 partition；保護狀態必須由所有共享它的 controllers 一致執行。</p>
</li>
<li id="q-147-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>確認 CAP.BPS、BPC、目前 ABPID 與有效保護機制；FID85h 與 RPMB 不一定同時掌控狀態。</p>
</li>
<li id="q-147-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>先用 Firmware Image Download 依序送整份映像；Commit CA6 寫入 BPID，CA7 才標為 Active 並更新 ABPID。</p>
</li>
<li id="q-147-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>完成下載，解除目標寫入鎖定，CA6 提交，讀回驗證，CA7 切換，最後恢復合適的寫入保護。</p>
</li>
<li id="q-147-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>CA6 成功表示寫入該 partition；不代表 ABPID 已切換。CA7 成功後再確認 ABPID。</p>
</li>
<li id="q-147-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>被鎖定而嘗試改寫時回 Boot Partition Write Prohibited。寫入中 Reset／斷電可能留下新舊混合內容，不能直接標為 Active。</p>
</li>
<li id="q-147-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-147-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Boot Partition CA6／CA7 不等同 controller firmware activation，因此不能要求 Firmware Activation Starting。若另有錯誤事件，依其本身條件處理。</p>
</li>
<li id="q-147-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>以 Commit CQE、BPINFO.ABPID、Boot Partition 讀回資料及 FID85h 核對更新。一般 Firmware Slot Information 描述 firmware slots，不是 Boot Partition 映像清單。</p>
</li>
<li id="q-147-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 時，Firmware Commit 完成記錄 Event02h，含舊版本、要求啟用的新版本、CA、slot 與 Status。 <a class="qa-rule-link" href="#common-firmware_op-11">本冊完整規則</a></p>
</li>
<li id="q-147-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 會丟棄未 Commit 的下載；Boot 寫入中重設可能留下舊、新或混合內容，恢復後必須驗證再決定是否切換。</p>
</li>
<li id="q-147-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 中斷 Boot Commit 也不能視為原子回復；恢復後查 Active ID、保護狀態與實際內容。</p>
</li>
<li id="q-147-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Boot Commit 中斷電可留下混合內容。Set Features 保護機制的 Power Cycle 會回到 Write Locked；不要把解鎖狀態當成跨斷電不變。</p>
</li>
<li id="q-147-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Boot partitions 可由多個 controllers 共用；更新與保護需要在所有共享者之間協調，不能只鎖住一條 Host 路徑。</p>
</li>
<li id="q-147-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>分別比較下載內容、讀回內容及 ABPID，避免「切換成功」掩蓋「映像內容錯誤」。</p>
</li>
<li id="q-147-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查是否只做了 CA6，卻期待 ABPID 自動改變。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-boot">Base 2.4 §8.1.3–8.1.3.3.3</a> · <a href="#ref-bootprotect">Base 2.4 §5.2.30.1.39</a> · <a href="#ref-bootreg">Base 2.4 §3.1.4 (BPINFO, BPRSEL, BPMBL)</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-148" data-question="148"><h2><a class="qa-qid" href="#q-148">Q148</a> Boot Partition 更新與 Controller Firmware 更新有何不同？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-148-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-148-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Boot Partition 保存供 Host 開機使用的映像；controller firmware 是 SSD controller 執行的程式。共用下載命令，不代表用途、順序與啟用方式相同。</p>
</li>
<li id="q-148-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Boot 用 BPID0／1；firmware 用 slots1～7 與 domain 範圍。兩者不是同一份儲存清單。</p>
</li>
<li id="q-148-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Boot 看 CAP.BPS／BPC／BPINFO；firmware 看 OACS／FRMW／MTFA 與 LID03h。</p>
</li>
<li id="q-148-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Firmware Download 可亂序，CA0～3 管理保存與啟用；Boot Download 必須依序，CA6／7 管理替換與 Active ID。</p>
</li>
<li id="q-148-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先決定更新對象，再選對能力、下載順序、Commit Action 與驗證方法。不要交錯兩種更新流程。</p>
</li>
<li id="q-148-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Firmware 成功以 running FR／slot 驗證；Boot 成功以內容及 ABPID 驗證。更新 Boot 不要求 Identify.FR 改變。</p>
</li>
<li id="q-148-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Boot Commit 斷電可能混合新舊內容；Firmware load failure 有回復映像的規則。不能將其中一套保證套到另一套。</p>
</li>
<li id="q-148-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-148-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>不經 Reset 的 controller firmware 啟用，依啟用設定回報 Firmware Activation Starting；Boot CA6／CA7 不屬於這種啟用，不要求相同通知。</p>
</li>
<li id="q-148-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Firmware 更新讀 LID03h 與 Identify.FR；Boot 更新讀 ABPID、內容與保護狀態。失敗時各自保留 Commit CQE 及可關聯的 Error Information。</p>
</li>
<li id="q-148-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 時，Firmware Commit 完成記錄 Event02h，含舊版本、要求啟用的新版本、CA、slot 與 Status。 <a class="qa-rule-link" href="#common-firmware_op-11">本冊完整規則</a></p>
</li>
<li id="q-148-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 會丟棄尚未 Commit 的暫存下載。已 Commit 的 firmware 按 CA 與所需 reset 啟用；Boot 寫入中斷則可能留下混合內容，需重新讀回確認。</p>
</li>
<li id="q-148-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 可能滿足 firmware 要求的啟用方式，但不能保證被中斷的 Boot 寫入已成功。恢復後依更新對象查 slot／FR 或 Boot 內容／ABPID。</p>
</li>
<li id="q-148-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Firmware 啟用中失電後需查實際執行映像及可能的回復結果；Boot Commit 失電可留下新舊混合內容。兩者都不能只因重新上電就宣告更新成功。</p>
</li>
<li id="q-148-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Firmware 以共享 slot 的 Domain 為主要範圍；Boot 以共享該 partition 的 controllers 為範圍。更新時先找出所有共用者，不能只協調提交命令的那條路徑。</p>
</li>
<li id="q-148-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>測試報告按對象記錄狀態與持久性，避免把 CA7 的 Active 與 firmware CAFS 混為一談。</p>
</li>
<li id="q-148-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先問「這份映像由 Host 開機使用，還是由 SSD controller 執行」，再查正確介面。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-boot">Base 2.4 §8.1.3–8.1.3.3.3</a> · <a href="#ref-bootprotect">Base 2.4 §5.2.30.1.39</a> · <a href="#ref-firmware">Base 2.4 §3.11–3.11.1, 5.2.9–5.2.10</a> · <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fwpel">Base 2.4 §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-command-8"><h3>命令完成、事件與紀錄 · DNR 與 More 應如何設定？</h3><p>只有收到 CQE，才有 DNR 與 More 可供判讀。DNR=1 表示相同命令即使重送到此 NVM subsystem 的任一 controller，仍預期會失敗；DNR=0 則只表示可能成功。除非個別錯誤條件另有明定，不能只看 Status 名稱就要求 DNR=1。More=1 表示 Error Information Log 有這筆命令的補充資訊。SCT=SC=0 時，DNR 應為 0。</p></article>
<article id="common-firmware_op-9"><h3>本主題的共用條件 · 是否產生 Asynchronous Event？</h3><p>開始不經 Reset 的韌體啟用時，受影響 controller 在 Firmware Activation Notices 啟用下回報 Firmware Activation Starting。載入失敗另有 Firmware Image Load Error；Download 每一段成功不會各自觸發啟用通知。</p></article>
<article id="common-firmware_op-10"><h3>本主題的共用條件 · 是否更新 Error Information Log 或其他 Log？</h3><p>用 Firmware Slot Information 區分目前 Active 與下次 Reset 預定 Active，再用 Identify.FR 確認真正執行的版本。失敗時另依 CQE.More 查 Error Information；slot 中已有新映像，不表示它已執行。</p></article>
<article id="common-firmware_op-11"><h3>本主題的共用條件 · 是否記錄於 Persistent Event Log？</h3><p>支援 PEL 時，Firmware Commit 完成記錄 Event02h，含舊版本、要求啟用的新版本、CA、slot 與 Status。NFR 是要求的新版本，不是啟用成功證明；Reset Event 的 FA／FREV 可補充實際啟用結果。</p></article>
<article id="common-firmware_op-12"><h3>本主題的共用條件 · Controller Reset 後是否保留或繼續？</h3><p>Download 後、Commit 完成前若發生 Controller Level Reset，已下載的暫存映像部分必須丟棄。已完成 Commit 的 slot 與待啟用安排則依 CA 及回傳的必要 Reset 類型判斷；不能只因任何 Reset 就假設新映像會啟用。</p></article>
<article id="common-firmware_op-13"><h3>本主題的共用條件 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>Subsystem Reset 會影響其涵蓋的 controllers，並可滿足明確要求此 Reset 的待啟用映像。恢復後重新查 FR、slot 及能力；未完成 Commit 的暫存下載不能沿用。</p></article>
<article id="common-firmware_op-14"><h3>本主題的共用條件 · Power Cycle 後是否保留或繼續？</h3><p>若在要求啟用的 Commit 尚未完成時進入 D3cold，恢復後可使用原映像或該次新映像，必須實際查證。已完成下載但尚未完成 Commit 的暫存部分，不能當成跨斷電保存的有效 slot。</p></article>
<article id="common-firmware_op-15"><h3>本主題的共用條件 · 是否影響其他 Controller 或 Namespace？</h3><p>同一 domain 的 controllers 共用 firmware slots，該 domain 使用相同映像；單一 domain 時即涵蓋 subsystem。Host 應協調所有受影響存取者，並避免多個更新流程互相重疊。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-cc"><strong>Base 2.4 · §3.1.4 (CC, CSTS, NSSR)</strong><br>文件頁 60–66 · PDF 86–92 · Figure 41–43</li>
<li id="ref-bootreg"><strong>Base 2.4 · §3.1.4 (BPINFO, BPRSEL, BPMBL)</strong><br>文件頁 69–70 · PDF 95–96 · Figure 49–51</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-firmware"><strong>Base 2.4 · §3.11–3.11.1, 5.2.9–5.2.10</strong><br>文件頁 135–138, 202–206 · PDF 161–164, 228–232 · Figure 187–193</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>文件頁 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>文件頁 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-fwlog"><strong>Base 2.4 · §5.2.13.1.4</strong><br>文件頁 225–226 · PDF 251–252 · Figure 215</li>
<li id="ref-commandseffects"><strong>Base 2.4 · §5.2.13.1.6</strong><br>文件頁 226–229 · PDF 252–255 · Figure 216–217</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-fwpel"><strong>Base 2.4 · §5.2.13.1.14.2.2, 5.2.13.1.14.2.4</strong><br>文件頁 252–255 · PDF 278–281 · Figure 238, 240–241</li>
<li id="ref-bootlog"><strong>Base 2.4 · §5.2.13.1.21</strong><br>文件頁 283–284 · PDF 309–310 · Figure 279–280</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>文件頁 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-aec"><strong>Base 2.4 · §5.2.30.1.6</strong><br>文件頁 466–468 · PDF 492–494 · Figure 474</li>
<li id="ref-bootprotect"><strong>Base 2.4 · §5.2.30.1.39</strong><br>文件頁 512–514 · PDF 538–540 · Figure 542</li>
<li id="ref-boot"><strong>Base 2.4 · §8.1.3–8.1.3.3.3</strong><br>文件頁 586–592 · PDF 612–618 · Figure 679–683</li>
<li id="ref-uuid"><strong>Base 2.4 · §8.1.31.1–8.1.31.2</strong><br>文件頁 737–738 · PDF 763–764 · Figure 782</li>
<li id="ref-idns"><strong>NVM Command Set 1.3 · §4.1.5.1–4.1.5.4</strong><br>文件頁 84–107 · PDF 84–107 · Figure 123–130</li>
</ul><h3>需要看欄位圖時</h3><p>以下連結可開啟對應的圖表教學，查閱欄位及判讀方式。每張圖保留固定的教學位置，方便之後反覆查詢。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b42">Base 2.4 Figure 42 · Offset 1Ch: CSTS – Controller Status</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/firmware-boot/en/">English</a><a href="/DOCS/nvme-question-bank/firmware-boot.html">繁中教學 HTML</a></nav>
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
