---
layout: post
title: "NVMe 自問自答題庫：資料 I/O：長度、持久性與完整性"
date: 2026-10-03 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/data-io/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/data-io/en/">English</a><a href="/DOCS/nvme-question-bank/data-io.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q321–Q328</p><h1>資料 I/O：長度、持久性與完整性</h1><p class="qr-intro">本冊補充原題庫尚未展開的資料 I/O 判讀：命令能不能接受、完成後保證什麼、資料內容如何驗證，以及失敗後可能留下哪些結果。先把四個問題分開，再用具體欄位值推導；既有 Feature、queue 與指標規則則連回原題。</p><p>先練習，再展開每題的 17 項解答。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>先說清楚要證明哪件事，再選命令</h2><p class="qa-takeaway">可接受的命令、正確的內容、持久性與原子性，是四個不同判斷；一個 Success 不能代替全部證據。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">要回答的問題</th><th scope="col">需要一起看的資訊</th><th scope="col">容易漏掉的條件</th></tr></thead><tbody><tr><td>這筆資料範圍合法嗎？</td><td>MDTS、MPSMIN、NLB、NSZE、實際傳輸格式</td><td>NLB 加 1；metadata 是否計入 MDTS</td></tr><tr><td>完成的寫入能否耐斷電？</td><td>WCE、FUA、Flush 範圍與時間線</td><td>Flush 提交前，目標 Write 是否已完成</td></tr><tr><td>中斷後能否只更新一部分？</td><td>有效原子單位、MAM、邊界與起訖 LBA</td><td>正常原子性與斷電原子性不同</td></tr><tr><td>讀得到，是否就等於內容正確？</td><td>Read、Compare、Verify 及 PI 檢查條件</td><td>Verify 沒有拿應用程式預期內容做比較</td></tr><tr><td>失敗後哪些資料可能已改？</td><td>Copy.DW0、目的讀回、原始來源快照</td><td>DW0=0 不是「完全沒寫入」的證明</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>教學假設先讓 Write A 成功，再提交同一 namespace 的 Flush。Flush 成功後，才有這條路徑提供的持久性保證。如果把兩個命令同時送出，即使 Flush 先成功，也不能宣稱尚未完成的 A 已被涵蓋。這個差別取決於時間關係，不是 CQE 的成功數量。</p>
<p class="qa-citations">來源：<a href="#ref-flushdata">Base 2.4 §7.2–7.2.1</a> · <a href="#ref-iofields">NVM Command Set 1.3 §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</a> · <a href="#ref-atomicdata">NVM Command Set 1.3 §2.1.4–2.1.4.6</a> · <a href="#ref-verifydata">NVM Command Set 1.3 §3.3.5–3.3.5.1</a> · <a href="#ref-copydata">NVM Command Set 1.3 §3.3.2–3.3.2.3, 3.3.2.5 (Formats 0h/1h; cross-namespace formats only for contrast)</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-321">Q321 · 一筆 Read／Write 的長度合法嗎？如何一起檢查 MDTS、NLB 與 Namespace 範圍？</a></li>
<li><a href="#q-322">Q322 · Write 已成功，資料就一定耐斷電嗎？Flush 與 FUA 各保證什麼？</a></li>
<li><a href="#q-323">Q323 · 原子單位足夠，為什麼跨邊界的 Write 仍可能不具整筆原子性？</a></li>
<li><a href="#q-324">Q324 · Read、Compare 與 Verify 成功，各能證明什麼？</a></li>
<li><a href="#q-325">Q325 · Write Zeroes 與 Deallocate 之後，Read 一定回全零嗎？</a></li>
<li><a href="#q-326">Q326 · PI 檢查為什麼沒有抓到錯誤？以 Type 1、16-bit Guard 格式逐步判讀</a></li>
<li><a href="#q-327">Q327 · Copy 失敗後，CQE.DW0 能告訴我哪些資料已經複製？</a></li>
<li><a href="#q-328">Q328 · Write Uncorrectable 後 Read 失敗，是媒體壞掉了嗎？</a></li>
</ol></section>
<article class="qa-question" id="q-321" data-question="321"><h2><a class="qa-qid" href="#q-321">Q321</a> 一筆 Read／Write 的長度合法嗎？如何一起檢查 MDTS、NLB 與 Namespace 範圍？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-321-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-321-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>長度是否合法，需要同時回答三件事：命令指定幾個 logical blocks、Host 要傳多少 bytes，以及最後一個 LBA 是否仍在 namespace 內。PRP 清單能描述這些 bytes，不代表傳輸大小就一定符合命令限制。</p>
</li>
<li id="q-321-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>本題限定一般 Read／Write，先假設無其他命令擴充。命令作用於 NSID 指定的 namespace；MDTS 限制 Host 與 controller 之間的資料傳輸，NSZE 則界定合法 LBA，兩者衡量的對象不同。</p>
</li>
<li id="q-321-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Identify Controller 提供 MDTS 與 CTRATT.MEM，CAP.MPSMIN 提供最小記憶體頁面大小；Identify Namespace 提供 NSZE、目前 LBA Format、LBADS、MS 及 metadata 配置。MDTS 非零時，上限為 2^MDTS × 2^(12+MPSMIN) bytes，不能改用目前 CC.MPS。</p>
</li>
<li id="q-321-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>SLBA 是起始位址；Read／Write 的 NLB 採 zero-based 編碼，所以實際區塊數為 NLB+1，最後一個 LBA 為 SLBA+NLB。LBADS 表示每個資料區塊有 2^LBADS bytes。若 metadata 與資料交錯傳輸且 MEM=0，MDTS 計算需包含 metadata；MEM=1 則排除 metadata。</p>
</li>
<li id="q-321-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先固定 namespace 格式並計算 LBA 範圍，再算實際傳輸 bytes，最後才配置 PRP／SGL。教學假設 MPSMIN=0、MDTS=5、資料 4096 bytes、交錯 metadata 8 bytes（本例不使用 PI）、MEM=0：NLB=31 代表 32 個區塊，需傳 131328 bytes，超過 131072-byte 上限；只算使用者資料就會漏掉 256 bytes。</p>
</li>
<li id="q-321-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>在同一假設下，31 個區塊需 127224 bytes，可以符合 MDTS；命令的 NLB 應填 30。這只證明長度條件成立，還要滿足 NSID、存取權限、指標與 PI 等條件，成功 CQE 才代表這次 I/O 正常完成。</p>
</li>
<li id="q-321-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>超過 MDTS 會以 Invalid Field in Command（SCT/SC=0/02h）中止；LBA 範圍超過 NSZE 則是 LBA Out of Range（0/80h）。例如 NSZE=1024、SLBA=1000、NLB=31，最後 LBA=1031，已超過 1023。驗證特定錯誤時，一次只留下其中一種違規。</p>
</li>
<li id="q-321-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-321-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>一般 I/O 的成功 CQE 不是 Asynchronous Event。 <a class="qa-rule-link" href="#common-data_io-9">本冊完整規則</a></p>
</li>
<li id="q-321-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>保留原始命令、CQE、資料與 metadata，再按實際命令種類核對 SMART 計數。 <a class="qa-rule-link" href="#common-data_io-10">本冊完整規則</a></p>
</li>
<li id="q-321-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Read、Write、Compare 或 Copy 不是 PEL 的逐筆命令歷史。 <a class="qa-rule-link" href="#common-data_io-11">本冊完整規則</a></p>
</li>
<li id="q-321-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Level Reset 使原 I/O queues 與未完成命令的追蹤關係失效，但不會替 Host 撤銷已發生的資料修改。 <a class="qa-rule-link" href="#common-data_io-12">本冊完整規則</a></p>
</li>
<li id="q-321-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後，受影響的 controllers 都要恢復命令通道。 <a class="qa-rule-link" href="#common-data_io-13">本冊完整規則</a></p>
</li>
<li id="q-321-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後，先分清「命令已成功完成且資料符合持久性要求」與「命令在寫入途中被中斷」。 <a class="qa-rule-link" href="#common-data_io-14">本冊完整規則</a></p>
</li>
<li id="q-321-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>I/O 以指定 namespace 及 LBA 範圍為主要對象。 <a class="qa-rule-link" href="#common-data_io-15">本冊完整規則</a></p>
</li>
<li id="q-321-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>MDTS=0 只表示沒有 MDTS 這項上限，不會取消 NLB 的編碼範圍、namespace 邊界或命令專屬限制。也不能把 MDTS 直接套到不傳送 Host 資料的 Verify、Write Zeroes 或 Write Uncorrectable。</p>
</li>
<li id="q-321-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否把 CC.MPS 當成 MDTS 的基準、漏算 NLB 的加 1，或使用 Format 前的 LBA 大小。這三種錯誤都可能讓看似相同的 I/O 長度得到不同結果。</p>
</li>
</ol>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/identify/zh-tw/#q-049">Q49</a> · <a href="/nvme/question-bank/pointers/zh-tw/#q-276">Q276</a> · <a href="/nvme/question-bank/pointers/zh-tw/#q-279">Q279</a> · <a href="/nvme/question-bank/data-io/zh-tw/#q-326">Q326</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-pointers">Base 2.4 §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-iofields">NVM Command Set 1.3 §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</a> · <a href="#ref-mediaerrors">Base 2.4 §4.2.3 (Media and Data Integrity Errors only)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-322" data-question="322"><h2><a class="qa-qid" href="#q-322">Q322</a> Write 已成功，資料就一定耐斷電嗎？Flush 與 FUA 各保證什麼？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-322-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-322-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Write 成功表示命令完成，但在允許使用揮發性寫入快取的情況下，資料可能仍在快取。持久性要判斷資料是否已符合非揮發儲存要求，不能只用一般讀回成功或 CQE Success 代替證明。</p>
</li>
<li id="q-322-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Write.FUA 作用於該筆命令的資料及 metadata。Flush 則作用於指定 namespace 中，在 Flush 提交前已由 controller 完成的命令；它不是自動排序其他仍在執行中命令的全域屏障。</p>
</li>
<li id="q-322-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先確認 VWC.VWCP 是否有揮發性快取、FID06h.WCE 是否啟用，以及 VWC.FB 是否允許 Flush 的 NSID=FFFFFFFFh。namespace 的 VWCNP 也可能指出該 namespace 沒有揮發性快取，不能只看 controller 的整體宣告。</p>
</li>
<li id="q-322-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Write 的 FUA=1 要求其資料及 metadata 在命令完成前提交至非揮發媒體；FUA=0 本身不增加要求。Flush 使用 NSID 選範圍，其他命令專屬欄位為 Reserved。FB=11b 才表示廣播 Flush 涵蓋提交端已附加的 namespaces。</p>
</li>
<li id="q-322-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>要保證一組已提交寫入的持久性，Host 可先等所有目標 Write 成功，再對正確 NSID 提交 Flush，最後等 Flush 成功。假設 Write A 與 Flush 同時提交，不能因 Flush 比 A 先完成，就宣告 A 已被涵蓋。另一種做法是讓各筆 Write 自己帶 FUA=1，並等待各筆成功。</p>
</li>
<li id="q-322-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>符合範圍與先後條件的 Flush 成功後，所涵蓋資料須具備持久性。沒有或未啟用揮發性快取時，Flush 沒有效果；若也沒有進行中的 Sanitize，仍須成功完成。這不是不支援 Flush 的錯誤。</p>
</li>
<li id="q-322-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>FB=10b 時使用 NSID=FFFFFFFFh，須回 Invalid Namespace or Format（0/0Bh）；Base 2.4 controller 不得用 FB=00b 的舊版未定義廣播行為。進行中的 Sanitize 有自己的命令限制，不能把平常無快取時的成功要求直接套過去。</p>
</li>
<li id="q-322-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-322-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>一般 I/O 的成功 CQE 不是 Asynchronous Event。 <a class="qa-rule-link" href="#common-data_io-9">本冊完整規則</a></p>
</li>
<li id="q-322-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>保留原始命令、CQE、資料與 metadata，再按實際命令種類核對 SMART 計數。 <a class="qa-rule-link" href="#common-data_io-10">本冊完整規則</a></p>
</li>
<li id="q-322-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Read、Write、Compare 或 Copy 不是 PEL 的逐筆命令歷史。 <a class="qa-rule-link" href="#common-data_io-11">本冊完整規則</a></p>
</li>
<li id="q-322-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Level Reset 使原 I/O queues 與未完成命令的追蹤關係失效，但不會替 Host 撤銷已發生的資料修改。 <a class="qa-rule-link" href="#common-data_io-12">本冊完整規則</a></p>
</li>
<li id="q-322-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後，受影響的 controllers 都要恢復命令通道。 <a class="qa-rule-link" href="#common-data_io-13">本冊完整規則</a></p>
</li>
<li id="q-322-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後，先分清「命令已成功完成且資料符合持久性要求」與「命令在寫入途中被中斷」。 <a class="qa-rule-link" href="#common-data_io-14">本冊完整規則</a></p>
</li>
<li id="q-322-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>I/O 以指定 namespace 及 LBA 範圍為主要對象。 <a class="qa-rule-link" href="#common-data_io-15">本冊完整規則</a></p>
</li>
<li id="q-322-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>FUA 與 Flush 不會增加原子寫入單位。原子性限制中斷或競爭時可觀察到哪些資料組合；持久性則約束成功後是否可因失電退回舊資料。應把命令時間線、Current.WCE、FUA 與 Flush 的涵蓋範圍放在一起判讀。</p>
</li>
<li id="q-322-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查 Flush 是否在目標 Write 完成之後才提交，以及是否指定同一 namespace。只看到一筆 Flush Success，還無法知道它是否涵蓋這次正在調查的資料。</p>
</li>
</ol>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/commands/zh-tw/#q-038">Q38</a> · <a href="/nvme/question-bank/commands/zh-tw/#q-039">Q39</a> · <a href="/nvme/question-bank/features/zh-tw/#q-060">Q60</a> · <a href="/nvme/question-bank/reset-shutdown/zh-tw/#q-182">Q182</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-flushdata">Base 2.4 §7.2–7.2.1</a> · <a href="#ref-vwc">Base 2.4 §5.2.30.1.4</a> · <a href="#ref-atomicdata">NVM Command Set 1.3 §2.1.4–2.1.4.6</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-iofields">NVM Command Set 1.3 §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</a> · <a href="#ref-mediaerrors">Base 2.4 §4.2.3 (Media and Data Integrity Errors only)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-323" data-question="323"><h2><a class="qa-qid" href="#q-323">Q323</a> 原子單位足夠，為什麼跨邊界的 Write 仍可能不具整筆原子性？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-323-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-323-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>判斷原子性不能只比較 Write 長度與某個最大值，還要確認 namespace 使用哪種原子模式，以及起訖 LBA 是否跨越邊界。長度相同的兩筆 Write，只因起點不同，就可能得到不同保證。</p>
</li>
<li id="q-323-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>正常原子性限制與其他 Read／Write 交錯時可見的結果；斷電原子性則限制寫入被失電或錯誤中斷時的新舊資料組合。本題的兩種保證都不是「成功之後必定持久」的替代說法。</p>
</li>
<li id="q-323-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先查 NSFEAT.NSABP 與 MAM。NSABP 決定 namespace 的 NAWUN／NAWUPF 是否有效；有效欄位若為 0，表示退回 controller 的 AWUN／AWUPF，非零值則按 zero-based 編碼加 1。MAM=0 是 Single，MAM=1 是 Multiple Atomicity Mode；正常原子性另確認 FID0Ah.DN 沒有解除該要求。</p>
</li>
<li id="q-323-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>NABSN 與 NABSPF 分別定義正常及斷電邊界大小；0 表示沒有這項邊界，非零編碼需加 1 才是區塊數。NABO 是第一個邊界的 LBA，不是數量欄位。解碼後的邊界位置為 NABO+y×邊界大小，y 為非負整數。</p>
</li>
<li id="q-323-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>教學假設 NSABP=1、MAM=0、DN=0、AWUN=AWUPF=0、NAWUN=7、NAWUPF=1、NABSN=NABSPF=15、NABO=0。正常單位是 8 個區塊，斷電單位是 2 個，邊界每 16 個區塊出現。Write 範圍 14～15 沒有跨界；改成 15～16 便跨過 LBA16。</p>
</li>
<li id="q-323-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>正常完成的 Write 回報 Success；但若要驗證中斷時的原子性，還需讀回資料。前例 14～15 的 2-block Write，在符合斷電原子性前提且被中斷時，後續讀回須是整組舊資料或整組新資料，不能一個新、一個舊。15～16 則沒有這項整筆 2-block 保證。若另採合法的 Multiple Atomicity 配置，跨界命令按邊界拆成各自原子的子範圍，仍不等於整筆一起原子更新。</p>
</li>
<li id="q-323-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>一般 Write 超過原子單位或跨界，不代表 controller 一定要拒絕；命令仍可能成功，只是保證範圍不同。不能將 fused Compare-and-Write 的 Atomic Write Unit Exceeded 條件，直接套到所有 Write。</p>
</li>
<li id="q-323-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-323-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>一般 I/O 的成功 CQE 不是 Asynchronous Event。 <a class="qa-rule-link" href="#common-data_io-9">本冊完整規則</a></p>
</li>
<li id="q-323-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>保留原始命令、CQE、資料與 metadata，再按實際命令種類核對 SMART 計數。 <a class="qa-rule-link" href="#common-data_io-10">本冊完整規則</a></p>
</li>
<li id="q-323-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Read、Write、Compare 或 Copy 不是 PEL 的逐筆命令歷史。 <a class="qa-rule-link" href="#common-data_io-11">本冊完整規則</a></p>
</li>
<li id="q-323-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Level Reset 使原 I/O queues 與未完成命令的追蹤關係失效，但不會替 Host 撤銷已發生的資料修改。 <a class="qa-rule-link" href="#common-data_io-12">本冊完整規則</a></p>
</li>
<li id="q-323-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後，受影響的 controllers 都要恢復命令通道。 <a class="qa-rule-link" href="#common-data_io-13">本冊完整規則</a></p>
</li>
<li id="q-323-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後，先分清「命令已成功完成且資料符合持久性要求」與「命令在寫入途中被中斷」。 <a class="qa-rule-link" href="#common-data_io-14">本冊完整規則</a></p>
</li>
<li id="q-323-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>I/O 以指定 namespace 及 LBA 範圍為主要對象。 <a class="qa-rule-link" href="#common-data_io-15">本冊完整規則</a></p>
</li>
<li id="q-323-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Format 後應重新取得 namespace 的原子欄位，不能沿用舊格式下的 bytes 換算。若同時測試其他寫入者，還要保留命令交錯證據；單次剛好讀到完整新資料，只證明這次結果，不能證明超出規範宣告的更大原子單位。</p>
</li>
<li id="q-323-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認目前比較的是原始編碼還是解碼後的區塊數，再檢查邊界。尤其 NAWUN=0、NABSN=0 與 NLB=0 分別代表退回基準、無邊界與 1 個區塊，不能套用同一個加 1 公式。</p>
</li>
</ol>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/features/zh-tw/#q-060">Q60</a> · <a href="/nvme/question-bank/data-io/zh-tw/#q-322">Q322</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-atomicdata">NVM Command Set 1.3 §2.1.4–2.1.4.6</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-iofields">NVM Command Set 1.3 §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</a> · <a href="#ref-mediaerrors">Base 2.4 §4.2.3 (Media and Data Integrity Errors only)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-324" data-question="324"><h2><a class="qa-qid" href="#q-324">Q324</a> Read、Compare 與 Verify 成功，各能證明什麼？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-324-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-324-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這三種命令回答不同問題：Read 將資料交給 Host；Compare 用 Host 提供的預期內容做比對；Verify 檢查儲存資訊的完整性，不將資料傳回 Host。Verify 成功不能證明資料等於應用程式心中的預期值。</p>
</li>
<li id="q-324-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>三者都指定 namespace 與 LBA 範圍，但資料方向不同。Compare 的 buffer 由 Host 傳入，Read 的 buffer 接收資料，Verify 則沒有這份 Host 資料傳輸；不能用相同 buffer 期待三者留下同樣結果。</p>
</li>
<li id="q-324-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先查對應 Opcode 的支援宣告與 Commands Supported and Effects。Verify 的大小需另外讀 VSL 及 ONCS.NVMVFYS：非零 VSL 搭配該支援位元，可表示建議最大值，而非一律拒絕超限。MDTS 不直接限制沒有 Host 資料傳輸的 Verify。</p>
</li>
<li id="q-324-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>SLBA／NLB 選範圍，PRCHK 選要檢查的 PI。Compare 的非 PI metadata 也參與比對，PI 則依檢查規則處理。Verify 的 PRACT 必須為 0；其 FUA=1 要求先提交相關快取，再對已提交至非揮發媒體的內容執行 Verify，仍不建立其他命令的提交順序。</p>
</li>
<li id="q-324-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>教學假設 LBA100 的正確內容是 A。先等寫入 A 完成，Read 取得 A；Compare 的輸入 A 應可成功，輸入不同的 B 應得到 Compare Failure。Verify 只檢查所存資訊是否可通過完整性檢查，所以即使應用程式原本想存 B，它仍可能成功。</p>
</li>
<li id="q-324-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Read Success 配合收到的 bytes，才可確認讀回內容；Compare Success 證明選定範圍與提供的比較資料相符；Verify Success 證明執行了所要求的完整性檢查。若有其他 controller 同時改寫同一範圍，三次不同時點的結果不能直接互相比較。</p>
</li>
<li id="q-324-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>內容不符使用 Compare Failure（2/85h），不等於 Unrecovered Read Error（2/81h）。Verify.PRACT 非零須回 Invalid Field（0/02h）；已偵測到的 PI 錯誤另用對應的資料完整性 Status。規範不要求同一媒體問題讓 Verify 與 Read 回傳完全相同的錯誤代碼。</p>
</li>
<li id="q-324-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-324-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>一般 I/O 的成功 CQE 不是 Asynchronous Event。 <a class="qa-rule-link" href="#common-data_io-9">本冊完整規則</a></p>
</li>
<li id="q-324-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Verify 的讀取及完整性檢查工作須計入 Data Units Read，即使沒有 Host 資料傳輸。錯誤細節仍依 CQE 的 More 及 Error Information 規則關聯；不是每次正常檢查都新增 Error entry。</p>
</li>
<li id="q-324-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Read、Write、Compare 或 Copy 不是 PEL 的逐筆命令歷史。 <a class="qa-rule-link" href="#common-data_io-11">本冊完整規則</a></p>
</li>
<li id="q-324-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Level Reset 使原 I/O queues 與未完成命令的追蹤關係失效，但不會替 Host 撤銷已發生的資料修改。 <a class="qa-rule-link" href="#common-data_io-12">本冊完整規則</a></p>
</li>
<li id="q-324-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後，受影響的 controllers 都要恢復命令通道。 <a class="qa-rule-link" href="#common-data_io-13">本冊完整規則</a></p>
</li>
<li id="q-324-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後，先分清「命令已成功完成且資料符合持久性要求」與「命令在寫入途中被中斷」。 <a class="qa-rule-link" href="#common-data_io-14">本冊完整規則</a></p>
</li>
<li id="q-324-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>I/O 以指定 namespace 及 LBA 範圍為主要對象。 <a class="qa-rule-link" href="#common-data_io-15">本冊完整規則</a></p>
</li>
<li id="q-324-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Verify 沒有把資料送回 Host，但其讀取或檢查的資料仍須計入 SMART 的 Data Units Read。這個計數表示規範定義的工作量，不代表 Host 一定收到那些 bytes。比對時也要考慮計數的單位與向上取整。</p>
</li>
<li id="q-324-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先釐清要證明的是「可讀」、「等於某份內容」還是「通過完整性檢查」，再選命令。若問題是應用程式資料不對，只做 Verify 不足以排除寫入錯誤內容的可能。</p>
</li>
</ol>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/identify/zh-tw/#q-050">Q50</a> · <a href="/nvme/question-bank/health/zh-tw/#q-198">Q198</a> · <a href="/nvme/question-bank/data-io/zh-tw/#q-326">Q326</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-comparedata">NVM Command Set 1.3 §3.3.1–3.3.1.1</a> · <a href="#ref-verifydata">NVM Command Set 1.3 §3.3.5–3.3.5.1</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-iofields">NVM Command Set 1.3 §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</a> · <a href="#ref-mediaerrors">Base 2.4 §4.2.3 (Media and Data Integrity Errors only)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-325" data-question="325"><h2><a class="qa-qid" href="#q-325">Q325</a> Write Zeroes 與 Deallocate 之後，Read 一定回全零嗎？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-325-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-325-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Write Zeroes 要讓後續成功讀取呈現全零；Dataset Management 的 Deallocate 則提供不再需要資料的資訊，controller 可選擇不採取動作。兩者的成功完成不能直接視為相同效果，也都不是敏感資料已不可復原的證明。</p>
</li>
<li id="q-325-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>本題比較指定 namespace 中的 LBA 範圍，先以 NSZ=0 的一般 Write Zeroes 為例。整個 namespace 清零的 NSZ=1 有額外條件，不可用普通範圍操作的成功去推論一定支援。</p>
</li>
<li id="q-325-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先查 Write Zeroes／Dataset Management 支援、namespace 的 DLFEAT.DRB 與 NSFEAT.DAE，再讀 FID05h.DULBE。DRB 描述解除配置後的讀取值；DAE 表示能否回報解除配置或未寫入錯誤；DULBE 決定是否啟用該錯誤。</p>
</li>
<li id="q-325-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Write Zeroes 的 NLB 採 zero-based，DEAC 表示 Host 是否請求解除配置；Dataset Management 的 NR 也是 zero-based，但每筆 Range 的 Length in Logical Blocks 是 1-based 數量。兩種命令都需區分「欄位的編碼」與「實際處理多少區塊」。</p>
</li>
<li id="q-325-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>教學假設 DRB=001b、DAE=1，先完成一筆合法 Write Zeroes，再讀同一範圍。若 controller 有解除配置且 DULBE=1，Read 應回 Deallocated or Unwritten Logical Block；若 DULBE=0 且讀取成功，則回全零。DEAC=0 也不代表禁止 controller 在仍能保證全零讀值的情況下解除配置。</p>
</li>
<li id="q-325-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>不能把「Write Zeroes 後 Read 得到 DULBE 錯誤」直接判成清零失敗。另一方面，Dataset Management Success 也不能證明每個範圍真的被解除配置；其處理限制與允許不採取動作的規則，需和讀回結果分開判讀。</p>
</li>
<li id="q-325-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>已解除配置或未寫入，且錯誤已受支援並啟用時，適用 Read 類命令須回 Deallocated or Unwritten Logical Block（2/87h）。若 NSZ=1 但 DEAC=0，或 namespace 不支援解除配置後回全零，Write Zeroes 須回 Invalid Field（0/02h）。</p>
</li>
<li id="q-325-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-325-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>一般 I/O 的成功 CQE 不是 Asynchronous Event。 <a class="qa-rule-link" href="#common-data_io-9">本冊完整規則</a></p>
</li>
<li id="q-325-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>保留原始命令、CQE、資料與 metadata，再按實際命令種類核對 SMART 計數。 <a class="qa-rule-link" href="#common-data_io-10">本冊完整規則</a></p>
</li>
<li id="q-325-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Read、Write、Compare 或 Copy 不是 PEL 的逐筆命令歷史。 <a class="qa-rule-link" href="#common-data_io-11">本冊完整規則</a></p>
</li>
<li id="q-325-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Level Reset 使原 I/O queues 與未完成命令的追蹤關係失效，但不會替 Host 撤銷已發生的資料修改。 <a class="qa-rule-link" href="#common-data_io-12">本冊完整規則</a></p>
</li>
<li id="q-325-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後，受影響的 controllers 都要恢復命令通道。 <a class="qa-rule-link" href="#common-data_io-13">本冊完整規則</a></p>
</li>
<li id="q-325-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後，先分清「命令已成功完成且資料符合持久性要求」與「命令在寫入途中被中斷」。 <a class="qa-rule-link" href="#common-data_io-14">本冊完整規則</a></p>
</li>
<li id="q-325-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>I/O 以指定 namespace 及 LBA 範圍為主要對象。 <a class="qa-rule-link" href="#common-data_io-15">本冊完整規則</a></p>
</li>
<li id="q-325-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>DULBE 停用時，真正已解除配置的區塊按 DRB 回全 00h 或全 FFh；DRB=000b 可為其中之一，但同一區塊在再次寫入前必須保持確定的讀值。Read 或 Verify 不會把該區塊變回已配置。</p>
</li>
<li id="q-325-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先讀回 DULBE 並確認 DRB，再分辨測的是 Write Zeroes 的讀值保證，還是 Dataset Management 的解除配置效果。把「命令成功」、「真的解除配置」及「後續讀取結果」分成三個觀察，才不會互相代替。</p>
</li>
</ol>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/features/zh-tw/#q-064">Q64</a> · <a href="/nvme/question-bank/format-sanitize/zh-tw/#q-127">Q127</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-deallocateddata">NVM Command Set 1.3 §3.3.3–3.3.3.3, 3.3.8–3.3.8.2</a> · <a href="#ref-nvmfeat">NVM Command Set 1.3 §4.1.3.1–4.1.3.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-iofields">NVM Command Set 1.3 §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</a> · <a href="#ref-mediaerrors">Base 2.4 §4.2.3 (Media and Data Integrity Errors only)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-326" data-question="326"><h2><a class="qa-qid" href="#q-326">Q326</a> PI 檢查為什麼沒有抓到錯誤？以 Type 1、16-bit Guard 格式逐步判讀</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-326-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-326-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Protection Information（PI）用來檢查資料完整性及區塊對應關係，但「namespace 有 PI」不代表每次命令都會檢查所有欄位。格式、PRACT、PRCHK 與 tag 的特殊值，共同決定哪些檢查真的發生。</p>
</li>
<li id="q-326-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>本題限定 16-bit Guard、STS=0、Type 1 的 8-byte PI 範例；不把這個位元配置套到 32-bit 或 64-bit Guard。Guard 占 2 bytes，Application Tag 占 2 bytes，Reference Tag 占 4 bytes，三者位於該區塊的 metadata。</p>
</li>
<li id="q-326-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Identify 的 DPC 告訴你支援哪些保護配置，DPS 表示目前使用的保護類型，LBA Format 的 MS 表示 metadata 大小；另確認使用中的 PI Format 與 STS。只查支援能力，卻沒查目前格式，可能會拿錯長度或錯誤 tag 配置來驗證。</p>
</li>
<li id="q-326-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>PRCHK 的 bit2、bit1、bit0 分別控制 Guard、Application Tag、Reference Tag 檢查；PRACT 控制 PI 的傳遞、產生或移除。本題啟用 Reference Tag 檢查時，Type 1 的 ILBRT／EILBRT 必須符合 SLBA 的低位元；Application Tag Mask 中的 1 表示要比較該位元，0 表示遮蔽。</p>
</li>
<li id="q-326-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>教學假設資料 4096 bytes、MS=8、PRACT=0、PRCHK=111b，先準備正確 PI，並避免 Application Tag=FFFFh 這個免檢查值。先確認合法案例成功，再分別只改 Guard、Application Tag 或 Reference Tag，並保持其他欄位及資料不變，才能分辨是哪項檢查回報錯誤。</p>
</li>
<li id="q-326-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>合法基準案例應成功完成；Read 的資料與 metadata 則依 PRACT 決定傳回內容。在此格式且 MS=8 時，Write.PRACT=1 由 controller 產生並附加 PI，Host 不提供那 8 bytes，PRCHK 會被忽略；Read.PRACT=1 則先按條件檢查，再移除 PI，只把資料交給 Host。若 MS 大於 PI 大小，不能再假設整份 metadata 都從 Host buffer 消失。</p>
</li>
<li id="q-326-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>已啟用且未被特殊值停用的檢查，失敗時分別回 Guard 2/82h、Application Tag 2/83h、Reference Tag 2/84h。本題若啟用該檢查，而 Type 1 命令中的 ILBRT／EILBRT 本身不符合 SLBA，則屬 Invalid Protection Information（1/81h）；這和資料中存放錯誤 tag 是不同條件。</p>
</li>
<li id="q-326-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-326-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>一般 I/O 的成功 CQE 不是 Asynchronous Event。 <a class="qa-rule-link" href="#common-data_io-9">本冊完整規則</a></p>
</li>
<li id="q-326-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>保留原始命令、CQE、資料與 metadata，再按實際命令種類核對 SMART 計數。 <a class="qa-rule-link" href="#common-data_io-10">本冊完整規則</a></p>
</li>
<li id="q-326-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Read、Write、Compare 或 Copy 不是 PEL 的逐筆命令歷史。 <a class="qa-rule-link" href="#common-data_io-11">本冊完整規則</a></p>
</li>
<li id="q-326-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Level Reset 使原 I/O queues 與未完成命令的追蹤關係失效，但不會替 Host 撤銷已發生的資料修改。 <a class="qa-rule-link" href="#common-data_io-12">本冊完整規則</a></p>
</li>
<li id="q-326-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後，受影響的 controllers 都要恢復命令通道。 <a class="qa-rule-link" href="#common-data_io-13">本冊完整規則</a></p>
</li>
<li id="q-326-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後，先分清「命令已成功完成且資料符合持久性要求」與「命令在寫入途中被中斷」。 <a class="qa-rule-link" href="#common-data_io-14">本冊完整規則</a></p>
</li>
<li id="q-326-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>I/O 以指定 namespace 及 LBA 範圍為主要對象。 <a class="qa-rule-link" href="#common-data_io-15">本冊完整規則</a></p>
</li>
<li id="q-326-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Type 1／Type 2 的 Application Tag=FFFFh 會停用 PI 檢查，即使 PRCHK 已開啟。因此，「故意放錯 Guard 卻成功」可能是 PRACT 讓 controller 重建 PI，或 tag 的特殊值停用了檢查；不能直接判定 controller 沒做資料保護。</p>
</li>
<li id="q-326-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認 metadata 是否真的由 Host 傳入、PRACT 的處理方式，以及 tag 是否用了免檢查值。接著再看對應 PRCHK 位元與 mask，而不是只盯著錯誤 CQE 是否出現。</p>
</li>
</ol>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/format-sanitize/zh-tw/#q-120">Q120</a> · <a href="/nvme/question-bank/pointers/zh-tw/#q-279">Q279</a> · <a href="/nvme/question-bank/pointers/zh-tw/#q-284">Q284</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-pidata">NVM Command Set 1.3 §2.1.5, 5.3.1.1 (STS=0), 5.3.2.1–5.3.2.2, 5.3.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-iofields">NVM Command Set 1.3 §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</a> · <a href="#ref-mediaerrors">Base 2.4 §4.2.3 (Media and Data Integrity Errors only)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-327" data-question="327"><h2><a class="qa-qid" href="#q-327">Q327</a> Copy 失敗後，CQE.DW0 能告訴我哪些資料已經複製？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-327-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-327-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Copy 可以在 controller 內把多個來源範圍接成一段連續目的資料，減少經過 Host 的資料搬移。但失敗時可能已複製部分資料，不能把錯誤 CQE 當成整筆回復原狀的交易。</p>
</li>
<li id="q-327-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>本題先限定同一 namespace、Copy Descriptor Format 0h 的範例。NSID 指向目的 namespace，SDLBA 指向目的起點；來源範圍由 descriptor 順序排列。跨 namespace 的 Formats 2h／3h 還有額外規則，不能只換一個 NSID 就照抄。</p>
</li>
<li id="q-327-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先確認 Copy 與 descriptor format 的支援，再讀 MSRC、MSSRL、MCL。MSRC 採 zero-based，限制來源範圍筆數；MSSRL 限制單一來源的區塊數；MCL 限制全部來源的總區塊數。目的端的原子單位另行限制可獲得的寫入原子性。</p>
</li>
<li id="q-327-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>命令的 NR 與每筆來源 NLB 都採 zero-based，先解碼再加總。教學假設 NR=1，兩筆來源 NLB 分別是 3 與 1，表示 4+2 個區塊；若 SDLBA=1000，依序寫入 1000～1003 與 1004～1005，而不是各自從 1000 開始。</p>
</li>
<li id="q-327-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先確認來源與目的範圍有效、未重疊且符合三項 Copy 限制，再保留來源快照與目的舊內容。失敗時讀 CQE.DW0，將其解釋為「最低編號、未成功複製的 Source Range entry」，而非成功區塊總數或下一個一定尚未執行的位置。</p>
</li>
<li id="q-327-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Copy 成功時，目的範圍應依 descriptor 順序包含全部來源內容；失敗時則不能要求完全沒有修改。例如四筆來源中 0、1、3 已成功，但 2 未成功，DW0=2；它無法證明 3 完全沒執行，也無法證明 2 沒有任何部分寫入。若完全沒有寫入目的資料，DW0 必須為 0；反過來，DW0=0 並不能證明目的資料完全沒改變。</p>
</li>
<li id="q-327-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>超過來源範圍或總長度限制使用 Command Size Limit Exceeded（1/83h）。Format0h／1h 的來源與目的重疊是 Host 應避免的情況，不能一律要求 Overlapping I/O Range；Formats2h／3h 則明定禁止相應重疊並回 1/87h。驗證 Status 前必須固定 descriptor format。</p>
</li>
<li id="q-327-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-327-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>一般 I/O 的成功 CQE 不是 Asynchronous Event。 <a class="qa-rule-link" href="#common-data_io-9">本冊完整規則</a></p>
</li>
<li id="q-327-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>保留原始命令、CQE、資料與 metadata，再按實際命令種類核對 SMART 計數。 <a class="qa-rule-link" href="#common-data_io-10">本冊完整規則</a></p>
</li>
<li id="q-327-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Read、Write、Compare 或 Copy 不是 PEL 的逐筆命令歷史。 <a class="qa-rule-link" href="#common-data_io-11">本冊完整規則</a></p>
</li>
<li id="q-327-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Level Reset 使原 I/O queues 與未完成命令的追蹤關係失效，但不會替 Host 撤銷已發生的資料修改。 <a class="qa-rule-link" href="#common-data_io-12">本冊完整規則</a></p>
</li>
<li id="q-327-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後，受影響的 controllers 都要恢復命令通道。 <a class="qa-rule-link" href="#common-data_io-13">本冊完整規則</a></p>
</li>
<li id="q-327-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後，先分清「命令已成功完成且資料符合持久性要求」與「命令在寫入途中被中斷」。 <a class="qa-rule-link" href="#common-data_io-14">本冊完整規則</a></p>
</li>
<li id="q-327-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>I/O 以指定 namespace 及 LBA 範圍為主要對象。 <a class="qa-rule-link" href="#common-data_io-15">本冊完整規則</a></p>
</li>
<li id="q-327-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>NVM 1.3 適用的 NVMCSA 規則，將 Copy 的目的寫入當成一個 Write 套用原子性要求，不表示任意大小的 Copy 都是整筆原子操作。失敗重試前，要查目的內容、原子子範圍與來源是否已被其他寫入者更動，不能只從 DW0 指定的位置繼續就宣告安全。</p>
</li>
<li id="q-327-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否把 DW0 當成已完成數量，再確認來源 NLB 是否已加 1。這兩種解讀錯誤會分別造成錯誤恢復位置與目的範圍偏移。</p>
</li>
</ol>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/recovery/zh-tw/#q-112">Q112</a> · <a href="/nvme/question-bank/data-io/zh-tw/#q-323">Q323</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-copydata">NVM Command Set 1.3 §3.3.2–3.3.2.3, 3.3.2.5 (Formats 0h/1h; cross-namespace formats only for contrast)</a> · <a href="#ref-atomicdata">NVM Command Set 1.3 §2.1.4–2.1.4.6</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-iofields">NVM Command Set 1.3 §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</a> · <a href="#ref-mediaerrors">Base 2.4 §4.2.3 (Media and Data Integrity Errors only)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-328" data-question="328"><h2><a class="qa-qid" href="#q-328">Q328</a> Write Uncorrectable 後 Read 失敗，是媒體壞掉了嗎？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-328-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-328-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Write Uncorrectable 主動把指定 logical blocks 標示為無效，讓之後的讀取回報錯誤。這是 Host 要求的邏輯狀態變更；單憑隨後的 Unrecovered Read Error，不能推論 NAND 真的發生物理損壞。</p>
</li>
<li id="q-328-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>操作影響 NSID 指定的 LBA 範圍，不等於停用整個 namespace。共享該 namespace 的其他 controllers 也可能觀察到這個無效狀態，因此比對前要確認是否有其他 Host 改寫相同範圍。</p>
</li>
<li id="q-328-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>確認 Write Uncorrectable 支援，以及 NVM Identify Controller 的 WUSL 與 ONCS.NVMWUSV。WUSL 非零時，NVMWUSV=1 表示建議最大大小；NVMWUSV=0 才依該值套用必須拒絕超限的規則。命令不傳 Host 資料，所以不能直接套 MDTS。</p>
</li>
<li id="q-328-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>SLBA 指起點，NLB 採 zero-based。教學假設 SLBA=200、NLB=1，目標是 200 及 201 兩個區塊；它不使用 Read／Write 的資料 buffer 來裝無效標記，而是由命令本身要求狀態改變。</p>
</li>
<li id="q-328-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先對目標寫入已知合法資料並確認成功，再執行 Write Uncorrectable。等其成功後，單獨讀取標示範圍與一個未標示的對照範圍；最後以合法 Write 重新寫入目標，確認無效狀態被清除，而不是只做 Reset 期待它消失。</p>
</li>
<li id="q-328-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Write Uncorrectable 本身可以成功；隨後對標示區塊的 Read 應回 Unrecovered Read Error。重新寫入該區塊會清除無效狀態，之後在沒有其他錯誤的情況下，可以讀回新寫入資料。這三個結果一起才構成完整驗證。</p>
</li>
<li id="q-328-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>後續 Read 的 Unrecovered Read Error 是 2/81h，不是標示命令必須回報失敗。WUSL 有效且 NVMWUSV=0 時，超過大小限制的標示命令須回 Invalid Field（0/02h）；NVMWUSV=1 的建議大小不能當成相同的強制拒絕條件。</p>
</li>
<li id="q-328-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-328-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>一般 I/O 的成功 CQE 不是 Asynchronous Event。 <a class="qa-rule-link" href="#common-data_io-9">本冊完整規則</a></p>
</li>
<li id="q-328-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>保留原始命令、CQE、資料與 metadata，再按實際命令種類核對 SMART 計數。 <a class="qa-rule-link" href="#common-data_io-10">本冊完整規則</a></p>
</li>
<li id="q-328-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>一般 Read、Write、Compare 或 Copy 不是 PEL 的逐筆命令歷史。 <a class="qa-rule-link" href="#common-data_io-11">本冊完整規則</a></p>
</li>
<li id="q-328-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Controller Level Reset 使原 I/O queues 與未完成命令的追蹤關係失效，但不會替 Host 撤銷已發生的資料修改。 <a class="qa-rule-link" href="#common-data_io-12">本冊完整規則</a></p>
</li>
<li id="q-328-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後，受影響的 controllers 都要恢復命令通道。 <a class="qa-rule-link" href="#common-data_io-13">本冊完整規則</a></p>
</li>
<li id="q-328-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後，先分清「命令已成功完成且資料符合持久性要求」與「命令在寫入途中被中斷」。 <a class="qa-rule-link" href="#common-data_io-14">本冊完整規則</a></p>
</li>
<li id="q-328-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>I/O 以指定 namespace 及 LBA 範圍為主要對象。 <a class="qa-rule-link" href="#common-data_io-15">本冊完整規則</a></p>
</li>
<li id="q-328-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>將標示命令的成功、後續 Read 的錯誤及重寫後的結果，與當時 Error Information／SMART 一起保存。即使讀取錯誤被計入相應統計，也不能據此把已知由 Host 標示造成的錯誤，改解釋成硬體退化。</p>
</li>
<li id="q-328-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查該 LBA 是否曾成功執行 Write Uncorrectable，以及之後是否已被重新寫入。若省略操作歷史，只看最後一筆 Read Status，很容易判錯原因。</p>
</li>
</ol>
<p class="qa-related">相關機制：<a href="/nvme/question-bank/errors/zh-tw/#q-096">Q96</a> · <a href="/nvme/question-bank/health/zh-tw/#q-199">Q199</a></p>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-uncorrectabledata">NVM Command Set 1.3 §3.3.7–3.3.7.1</a> · <a href="#ref-atomicdata">NVM Command Set 1.3 §2.1.4–2.1.4.6</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-iofields">NVM Command Set 1.3 §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</a> · <a href="#ref-mediaerrors">Base 2.4 §4.2.3 (Media and Data Integrity Errors only)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-command-8"><h3>命令完成、事件與紀錄 · DNR 與 More 應如何設定？</h3><p>只有收到 CQE，才有 DNR 與 More 可供判讀。DNR=1 表示相同命令即使重送到此 NVM subsystem 的任一 controller，仍預期會失敗；DNR=0 則只表示可能成功。除非個別錯誤條件另有明定，不能只看 Status 名稱就要求 DNR=1。More=1 表示 Error Information Log 有這筆命令的補充資訊。SCT=SC=0 時，DNR 應為 0。</p></article>
<article id="common-data_io-9"><h3>資料 I/O 的事件、紀錄與重設 · 是否產生 Asynchronous Event？</h3><p>一般 I/O 的成功 CQE 不是 Asynchronous Event。若另外發生符合定義的健康警告或錯誤事件，再依事件條件、AEC 設定及等待中的 AER 回報；故意製造一次 Compare 不相符，不能直接要求出現硬體故障通知。</p></article>
<article id="common-data_io-10"><h3>資料 I/O 的事件、紀錄與重設 · 是否更新 Error Information Log 或其他 Log？</h3><p>保留原始命令、CQE、資料與 metadata，再按實際命令種類核對 SMART 計數。More=1 時讀取相符的 Error Information；More=0 不代表禁止建立 entry，也不是每個失敗都必須新增 entry。計數或 Log 不能代替資料內容與範圍的核對。</p></article>
<article id="common-data_io-11"><h3>資料 I/O 的事件、紀錄與重設 · 是否記錄於 Persistent Event Log？</h3><p>一般 Read、Write、Compare 或 Copy 不是 PEL 的逐筆命令歷史。若操作期間另有受支援的硬體、健康或電源事件，才依該事件的記錄條件檢查 PEL；不能因為有一筆失敗 CQE，就要求一筆同名 Persistent Event。</p></article>
<article id="common-data_io-12"><h3>資料 I/O 的事件、紀錄與重設 · Controller Reset 後是否保留或繼續？</h3><p>Controller Level Reset 使原 I/O queues 與未完成命令的追蹤關係失效，但不會替 Host 撤銷已發生的資料修改。恢復後重建 queue，再查受影響 LBA；未完成寫入允許出現哪些結果，仍要配合有效原子單位、邊界及命令規則判斷。</p></article>
<article id="common-data_io-13"><h3>資料 I/O 的事件、紀錄與重設 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>Subsystem Reset 後，受影響的 controllers 都要恢復命令通道。這不是清除 namespace 內容的操作，也不是重送所有舊 I/O 的理由；先確認操作結果及共用資料是否已被其他路徑更新，再決定後續動作。</p></article>
<article id="common-data_io-14"><h3>資料 I/O 的事件、紀錄與重設 · Power Cycle 後是否保留或繼續？</h3><p>Power Cycle 後，先分清「命令已成功完成且資料符合持久性要求」與「命令在寫入途中被中斷」。前者核對已提交到非揮發媒體的資料；後者依斷電原子性與命令專屬規則判讀。另行重新查詢 Feature，不能把暫存設定的恢復方式當成資料保留規則。</p></article>
<article id="common-data_io-15"><h3>資料 I/O 的事件、紀錄與重設 · 是否影響其他 Controller 或 Namespace？</h3><p>I/O 以指定 namespace 及 LBA 範圍為主要對象。共享 namespace 的其他 controllers 會存取同一份邏輯資料，因此讀回驗證前要排除其他寫入者。命令從哪條 queue 送入，不能用來推論資料只屬於該 controller。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-cap"><strong>Base 2.4 · §3.1.4 (CAP, VS)</strong><br>文件頁 54–59 · PDF 80–85 · Figure 36–37</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-pointers"><strong>Base 2.4 · §4.2.1, 4.3.1–4.3.2 (PCIe-applicable layouts)</strong><br>文件頁 140–142, 158–164 · PDF 166–168, 184–190 · Figure 93, 110–122</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-mediaerrors"><strong>Base 2.4 · §4.2.3 (Media and Data Integrity Errors only)</strong><br>文件頁 154–155 · PDF 180–181 · Figure 107</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-smart"><strong>Base 2.4 · §5.2.13.1.3</strong><br>文件頁 220–225 · PDF 246–251 · Figure 213–214</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>文件頁 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-vwc"><strong>Base 2.4 · §5.2.30.1.4</strong><br>文件頁 464–465 · PDF 490–491 · Figure 471</li>
<li id="ref-flushdata"><strong>Base 2.4 · §7.2–7.2.1</strong><br>文件頁 567 · PDF 593</li>
<li id="ref-atomicdata"><strong>NVM Command Set 1.3 · §2.1.4–2.1.4.6</strong><br>文件頁 15–21 · PDF 15–21 · Figure 4–10</li>
<li id="ref-pidata"><strong>NVM Command Set 1.3 · §2.1.5, 5.3.1.1 (STS=0), 5.3.2.1–5.3.2.2, 5.3.3</strong><br>文件頁 21–22, 131, 141–145, 151–152 · PDF 21–22, 131, 141–145, 151–152 · Figure 11–12, 155, 174–175</li>
<li id="ref-comparedata"><strong>NVM Command Set 1.3 · §3.3.1–3.3.1.1</strong><br>文件頁 27–30 · PDF 27–30 · Figure 24, 26–27, 31</li>
<li id="ref-copydata"><strong>NVM Command Set 1.3 · §3.3.2–3.3.2.3, 3.3.2.5 (Formats 0h/1h; cross-namespace formats only for contrast)</strong><br>文件頁 30–40, 43–44 · PDF 30–40, 43–44 · Figure 34–35, 39–40, 42–43</li>
<li id="ref-deallocateddata"><strong>NVM Command Set 1.3 · §3.3.3–3.3.3.3, 3.3.8–3.3.8.2</strong><br>文件頁 44–48, 57–61 · PDF 44–48, 57–61 · Figure 45–47, 49, 83, 88–89</li>
<li id="ref-iofields"><strong>NVM Command Set 1.3 · §3.3.4, 3.3.6 (data pointers, SLBA, NLB, FUA and completion)</strong><br>文件頁 48–51, 53–56 · PDF 48–51, 53–56 · Figure 53–54, 59, 68, 70–71, 76</li>
<li id="ref-verifydata"><strong>NVM Command Set 1.3 · §3.3.5–3.3.5.1</strong><br>文件頁 51–53 · PDF 51–53 · Figure 61–62, 66</li>
<li id="ref-uncorrectabledata"><strong>NVM Command Set 1.3 · §3.3.7–3.3.7.1</strong><br>文件頁 56–57 · PDF 56–57 · Figure 77–80</li>
<li id="ref-nvmfeat"><strong>NVM Command Set 1.3 · §4.1.3.1–4.1.3.7</strong><br>文件頁 64–69 · PDF 64–69 · Figure 92–101</li>
<li id="ref-idns"><strong>NVM Command Set 1.3 · §4.1.5.1–4.1.5.4</strong><br>文件頁 84–107 · PDF 84–107 · Figure 123–130</li>
</ul><h3>需要看欄位圖時</h3><p>以下連結可開啟對應的圖表教學，查閱欄位及判讀方式。每張圖保留固定的教學位置，方便之後反覆查詢。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></li>
<li><a href="/nvme/figure-reference/io/zh-tw/#figure-n155">NVM Command Set 1.3 Figure 155 · 16b Guard Protection Information Format when STS field is cleared to 0h</a></li>
<li><a href="/nvme/figure-reference/io/zh-tw/#figure-n174">NVM Command Set 1.3 Figure 174 · Write Command 16b Guard Protection Information Processing</a></li>
<li><a href="/nvme/figure-reference/io/zh-tw/#figure-n175">NVM Command Set 1.3 Figure 175 · Read 16b Guard Command Protection Information Processing</a></li>
<li><a href="/nvme/figure-reference/io/zh-tw/#figure-n39">NVM Command Set 1.3 Figure 39 · Copy – Copy Descriptor Formats</a></li>
<li><a href="/nvme/figure-reference/io/zh-tw/#figure-n4">NVM Command Set 1.3 Figure 4 · Atomicity Parameters for Single Atomicity Mode</a></li>
<li><a href="/nvme/figure-reference/io/zh-tw/#figure-n47">NVM Command Set 1.3 Figure 47 · Dataset Management – Range Definition</a></li>
<li><a href="/nvme/figure-reference/io/zh-tw/#figure-n53">NVM Command Set 1.3 Figure 53 · Read – Command Dword 10 and Command Dword 11</a></li>
<li><a href="/nvme/figure-reference/io/zh-tw/#figure-n54">NVM Command Set 1.3 Figure 54 · Read – Command Dword 12</a></li>
<li><a href="/nvme/figure-reference/io/zh-tw/#figure-n70">NVM Command Set 1.3 Figure 70 · Write – Command Dword 10 and Command Dword 11</a></li>
<li><a href="/nvme/figure-reference/io/zh-tw/#figure-n71">NVM Command Set 1.3 Figure 71 · Write – Command Dword 12</a></li>
<li><a href="/nvme/figure-reference/io/zh-tw/#figure-n8">NVM Command Set 1.3 Figure 8 · Atomic Boundaries Example</a></li>
<li><a href="/nvme/figure-reference/io/zh-tw/#figure-n83">NVM Command Set 1.3 Figure 83 · Write Zeroes – Command Dword 12</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/data-io/en/">English</a><a href="/DOCS/nvme-question-bank/data-io.html">繁中教學 HTML</a></nav>
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
