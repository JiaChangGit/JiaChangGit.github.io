---
layout: post
title: "NVMe 自問自答題庫：總索引 · Q1–68"
date: 2026-10-01 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/en/">English</a><a href="/DOCS/nvme-question-bank/index.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–68</p>
<h1>NVMe Base 2.4 自問自答題庫</h1><p class="qr-intro">本題庫收錄第 1～68 題，依主題分成六冊。先理解 controller 啟用、queue 及 command 的運作，再學習如何查詢能力與設定功能。每題除了說明機制，也練習將實際觀察結果與規範要求互相比對。</p><div class="qr-series">
<article><h2><a href="/nvme/question-bank/initialization/zh-tw/">Controller 初始化與停用</a></h2><p class="qr-tags">Q1–Q9</p><p>先理解 controller 如何從停用轉為就緒，再開始處理命令。讀到能力，不表示 controller 已啟用；Host 設定 EN，也還要等待 RDY。即使 RDY=1，仍可能需要依 Ready Mode 確認媒體是否可用。本冊將狀態、等待時間及允許執行的動作放在一起，說明每個階段應如何判斷。</p></article>
<article><h2><a href="/nvme/question-bank/queues/zh-tw/">Admin Queue 與 I/O Queue</a></h2><p class="qr-tags">Q10–Q21</p><p>Host 準備的 queue 記憶體、controller 分配的 queue 配額，以及已成功建立的 queue，是三種不同資訊。本冊先說明 SQ 與 CQ 的依賴關係，再討論大小、識別碼、刪除及重設，讓你能判斷何時可以使用 queue，以及何時能安全回收記憶體。</p></article>
<article><h2><a href="/nvme/question-bank/doorbells/zh-tw/">Doorbell、Queue Full 與 Wrap-around</a></h2><p class="qr-tags">Q22–Q30</p><p>Doorbell 告訴 controller，Host 的指標已前進到哪個位置；Phase 則讓 Host 分辨 CQ 中的是新完成結果，還是上一圈留下的資料。本冊將位置與有效性一起說明，幫助你正確處理繞回及空間釋放，避免將正常繞回誤判成倒退，或把舊 CQE 處理兩次。</p></article>
<article><h2><a href="/nvme/question-bank/commands/zh-tw/">Command、Completion 與處理順序</a></h2><p class="qr-tags">Q31–Q43</p><p>從 Host 提交命令，到 controller 取得、處理並回報完成，再到 Host 回收資源，各階段能證明的事情不同。本冊沿著這條流程解讀 Command 與 CQE，並說明順序、仲裁及中斷各自控制什麼。只有完成順序，還不足以推論 controller 內部的全部行為。</p></article>
<article><h2><a href="/nvme/question-bank/identify/zh-tw/">Identify 與能力探索</a></h2><p class="qr-tags">Q44–Q53</p><p>Identify 提供多種查詢結構。先確定要查哪個物件、需要哪一種資訊，再選擇 CNS、CSI、NSID 及其他欄位。本冊分別說明能力、目前配置與清單變更，讓你知道不同回覆如何互相補充，以及哪些差異才可能構成矛盾。</p></article>
<article><h2><a href="/nvme/question-bank/features/zh-tw/">Get Features 與 Set Features</a></h2><p class="qr-tags">Q54–Q68</p><p>設定 Feature 前，先確認它影響哪個物件、是否可變更，以及是否可保存。設定後，再分別確認命令成功、Current 讀回值、實際行為與重設後的恢復結果。本冊依這些步驟說明如何驗證設定，避免只看成功 CQE 就跳到功能一定正確的結論。</p></article>
</div><section><h2>怎麼使用這份題庫</h2><ol><li>先說出功能的目的、影響對象與正常順序，再選查詢欄位。</li><li>展開解答後，分別檢查成功結果、錯誤處理、事件、紀錄，以及三種重設的影響。MMIO 存取沒有 CQE，因此相關的 Status 或 DNR／More 項目會標示不適用。</li><li>判斷韌體是否符合規範前，先確認要求適用的前提。shall 表示強制要求，should 表示建議，may 表示允許。若規範將行為列為 undefined，就沒有固定結果可供驗收，不能自行指定必須回報的 Status。</li></ol><p>所有算例皆為教學假設，不是實體裝置量測。範圍是 PCIe SSD 使用的三份規格；不含 NVMe over Fabrics、PCIe Link 與封包細節。必要的 PCIe 設定、中斷、Register 及 Doorbell 仍包含在內。</p></section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>全部題目</h2><ol class="qa-index">
<li class="qa-search-item"><a href="/nvme/question-bank/initialization/zh-tw/#q-001">Q01 · Host 應如何從 CAP 與 VS 確認 NVMe 版本、最大 Queue 大小、Timeout、Doorbell 間距、Memory Page Size 及支援的 Command Set？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/initialization/zh-tw/#q-002">Q02 · AQA、ASQ、ACQ 與 CC 各欄位應按照什麼順序設定？設定錯誤時可能發生什麼？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/initialization/zh-tw/#q-003">Q03 · Host 設定 CC.EN 後，應如何根據 CAP.TO 與 CSTS.RDY 判斷 Controller 是否成功 Enable？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/initialization/zh-tw/#q-004">Q04 · Host 清除 CC.EN 後，應如何判斷 Controller 是否成功 Disable？尚未 Disable 完成時能否重新 Enable？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/initialization/zh-tw/#q-005">Q05 · Host 能否在 CSTS.RDY 為 0 時送出 Command 或更新 Doorbell？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/initialization/zh-tw/#q-006">Q06 · CSTS.CFS 代表什麼？Controller 初始化失敗或進入 Fatal 狀態時，Host 應如何恢復？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/initialization/zh-tw/#q-007">Q07 · Controller 初始化後可能進入哪些 Ready Mode？Host 應如何處理暫時或限制性的 Ready 狀態？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/initialization/zh-tw/#q-008">Q08 · Controller Enable、Disable、Controller Reset、NVM Subsystem Reset 與 Shutdown 有什麼差異？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/initialization/zh-tw/#q-009">Q09 · Controller Reset 後，哪些 Register、Admin Queue、Feature 與 I/O Queue 需要重新設定？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/zh-tw/#q-010">Q10 · Admin Submission Queue 與 Admin Completion Queue 如何透過 AQA、ASQ 及 ACQ 建立？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/zh-tw/#q-011">Q11 · Admin Queue 與 I/O Queue 的 Size、Base Address 及 Memory Page 對齊有哪些要求？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/zh-tw/#q-012">Q12 · Host 如何建立 I/O Completion Queue 與 I/O Submission Queue？兩者必須遵守什麼建立順序？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/zh-tw/#q-013">Q13 · 多個 SQ 共用一個 CQ 與每個 SQ 使用獨立 CQ 有什麼差異？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/zh-tw/#q-014">Q14 · Host 如何確認 Controller 支援 Physically Contiguous 或其他 Queue 形式？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/zh-tw/#q-015">Q15 · QID 重複、QID 為 0、CQID 不存在、Queue Size 超過 CAP.MQES 或 Interrupt Vector 非法時，Controller 應如何回應？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/zh-tw/#q-016">Q16 · Number of Queues Feature 回傳的數值與實際可建立的 Queue 數量有什麼關係？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/zh-tw/#q-017">Q17 · Host 刪除 I/O Queue 時，SQ 與 CQ 的相依關係如何限制刪除順序？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/zh-tw/#q-018">Q18 · 刪除不存在的 Queue、仍被 SQ 使用的 CQ 或仍有 Outstanding Command 的 SQ 時，應如何處理？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/zh-tw/#q-019">Q19 · Queue 刪除後，Controller 是否還能存取原 Queue Memory 或回報原 Queue 的 Completion？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/zh-tw/#q-020">Q20 · Queue Level Reset 的影響範圍是什麼？Outstanding Command 應如何處理？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/queues/zh-tw/#q-021">Q21 · Controller Reset 後，原有 I/O Queue 是否有效？Host 需要重新執行哪些操作？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/doorbells/zh-tw/#q-022">Q22 · Host 應在什麼時候更新 SQ Tail Doorbell 與 CQ Head Doorbell？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/doorbells/zh-tw/#q-023">Q23 · Doorbell 值重複、倒退、超過 Queue 範圍或寫到錯誤 QID 時，可能造成什麼問題？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/doorbells/zh-tw/#q-024">Q24 · Host 如何根據 CAP.DSTRD 計算每個 SQ 與 CQ Doorbell 的位置？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/doorbells/zh-tw/#q-025">Q25 · Host 能否存取未建立、已刪除或 Controller 未 Enable 時的 Queue Doorbell？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/doorbells/zh-tw/#q-026">Q26 · SQ Tail 與 CQ Head 發生 Wrap-around 時，Host 與 Controller 應如何處理？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/doorbells/zh-tw/#q-027">Q27 · CQ Wrap-around 後 Phase Tag 如何變化？Host 如何利用 Phase Tag 辨識新 Completion？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/doorbells/zh-tw/#q-028">Q28 · CQ Full 通常如何形成？CQ Full 時 Controller 能否繼續處理相關 SQ？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/doorbells/zh-tw/#q-029">Q29 · Host 釋放 CQ 空間後，Controller 應如何恢復 Command 處理？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/doorbells/zh-tw/#q-030">Q30 · 多個 SQ 共用一個 CQ 時，Host 如何依 SQID 與 CID 辨識 Completion 來源？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/zh-tw/#q-031">Q31 · 一筆 NVMe Command 的 Opcode、CID、NSID、Data Pointer 及 Command Dword 各有什麼用途？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/zh-tw/#q-032">Q32 · Reserved 欄位非零、不合法 Command Dword 組合或不支援 Opcode 應如何處理？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/zh-tw/#q-033">Q33 · NSID 不存在、Inactive、不適用或錯誤使用 Broadcast NSID 時，應回傳什麼類型的 Status？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/zh-tw/#q-034">Q34 · CQE 中的 SQHD、SQID、CID、Phase Tag 及 Status 分別有什麼用途？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/zh-tw/#q-035">Q35 · Status Code Type 與 Status Code 應如何解析？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/zh-tw/#q-036">Q36 · More 與 Do Not Retry 位元分別代表什麼？DNR 為 0 是否代表一定能直接重試？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/zh-tw/#q-037">Q37 · Completion 已寫入但 Host 未處理，可能與 Phase Tag、CQ 位置或 Interrupt 有什麼關係？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/zh-tw/#q-038">Q38 · 多個 Command 同時 Outstanding 時，Controller 是否必須按照提交順序完成？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/zh-tw/#q-039">Q39 · 哪些 Command 具有順序相依性？Host 為什麼不能假設所有 Command 都依序完成？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/zh-tw/#q-040">Q40 · Outstanding Command 達到限制或 CQ Full 時，Controller 如何限制取得新 Command？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/zh-tw/#q-041">Q41 · Round Robin 與 Weighted Round Robin Arbitration 有什麼差異？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/zh-tw/#q-042">Q42 · Urgent、High、Medium 及 Low Queue Priority 在哪些情況下生效？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/commands/zh-tw/#q-043">Q43 · 多個 Queue 競爭資源時，如何判斷 Arbitration 是否符合設定？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/zh-tw/#q-044">Q44 · Identify Controller 與 Identify Namespace 分別提供哪些重要資訊？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/zh-tw/#q-045">Q45 · Active Namespace ID List、Allocated Namespace ID List 及 Namespace Descriptor List 有什麼差異？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/zh-tw/#q-046">Q46 · Controller List、UUID List 及 I/O Command Set Identify 資料分別有什麼用途？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/zh-tw/#q-047">Q47 · NVM Set、Endurance Group、Domain 及 Secondary Controller 資訊應從哪種 Identify 資料取得？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/zh-tw/#q-048">Q48 · CNS、CSI、NSID 或 UUID Index 不支援或不合法時，Controller 應如何回應？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/zh-tw/#q-049">Q49 · Serial Number、Model Number、Firmware Revision、MDTS 及 Optional Admin Command 欄位應如何解讀？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/zh-tw/#q-050">Q50 · Identify 宣告支援某功能後，應如何透過對應 Command 及 Commands Supported and Effects Log 驗證？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/zh-tw/#q-051">Q51 · Namespace 建立、刪除、Attach、Detach 或 Format 後，哪些 Identify 資料與 Namespace List 應更新？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/zh-tw/#q-052">Q52 · Firmware Activation、Reset 及 Power Cycle 後，哪些 Identify 資料可能改變，哪些應保持不變？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/identify/zh-tw/#q-053">Q53 · Identify、Feature、Log Page 與實際 Command 行為不一致時，應如何定位問題？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/zh-tw/#q-054">Q54 · Feature 的 Current、Default、Saved Value 及 Supported Capabilities 分別代表什麼？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/zh-tw/#q-055">Q55 · Set Features 的 Save 位元如何影響 Controller Reset 與 Power Cycle 後的 Feature 值？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/zh-tw/#q-056">Q56 · 不支援的 Feature、不合法 Feature 值或 Controller 不支援 Save 時，應如何回應？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/zh-tw/#q-057">Q57 · Host 如何判斷某個 Feature 是否需要指定 NSID？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/zh-tw/#q-058">Q58 · Arbitration、Number of Queues 及 I/O Command Set Profile Feature 如何設定與驗證？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/zh-tw/#q-059">Q59 · Interrupt Coalescing 與 Interrupt Vector Configuration 如何設定與驗證？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/zh-tw/#q-060">Q60 · Volatile Write Cache 與 Write Atomicity Normal 控制什麼行為？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/zh-tw/#q-061">Q61 · Asynchronous Event Configuration 如何決定哪些事件需要回報？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/zh-tw/#q-062">Q62 · Power Management、Autonomous Power State Transition 及 Host Controlled Thermal Management 有何差異？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/zh-tw/#q-063">Q63 · Timestamp、Keep Alive Timer 及 Host Memory Buffer 如何設定與驗證？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/zh-tw/#q-064">Q64 · Host Behavior Support、Error Recovery 及 Read Recovery Level 有什麼用途？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/zh-tw/#q-065">Q65 · Namespace Write Protection 如何設定？不同保護模式在 Reset 與 Power Cycle 後是否保留？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/zh-tw/#q-066">Q66 · Set Features 成功後，為什麼還應使用 Get Features 確認？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/zh-tw/#q-067">Q67 · Firmware Activation、Namespace 刪除、Controller Reset 及 Power Cycle 後，Feature 應如何變化？</a></li>
<li class="qa-search-item"><a href="/nvme/question-bank/features/zh-tw/#q-068">Q68 · Feature 宣告支援但 Get、Set 或實際功能行為不一致時，應如何驗證？</a></li>
</ol></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/en/">English</a><a href="/DOCS/nvme-question-bank/index.html">繁中教學 HTML</a></nav>
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
