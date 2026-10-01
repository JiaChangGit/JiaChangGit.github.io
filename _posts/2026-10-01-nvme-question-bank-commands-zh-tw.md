---
layout: post
title: "NVMe 自問自答題庫：Command、Completion 與處理順序"
date: 2026-10-01 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/commands/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/commands/en/">English</a><a href="/DOCS/nvme-question-bank/commands.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–68</p>
<header><p class="qa-range">Q31–Q43</p><h1>Command、Completion 與處理順序</h1><p class="qr-intro">沿著提交、取得、處理、完成、Host 回收的流程，辨認每個欄位能證明什麼。命令順序、仲裁、公平性與中斷是不同問題；不能用一張完成順序清單推論全部行為。</p><p>先練習，再展開每題的 17 項解答。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可以指定的一份邏輯儲存空間。多個 controller 可以屬於同一 NVM subsystem（包含 controller 與非揮發儲存資源的整體）。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue 是提交佇列，Completion Queue 是完成佇列；SQE／CQE 是其中的一筆 entry。QID 識別 queue，CID 識別同一 SQ 內尚未完成的命令，NSID 識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 是可存取的控制或狀態欄位；Identify 查物件能力與屬性；Feature 查／設工作設定；Log Page 回報指定種類的狀態或紀錄。FID、LID、CNS、CSI 分別選 Feature、Log、Identify 結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 是第幾筆，通常由 0 起算；offset 是離起點多遠，要看單位。zero-based 數量欄位的實際數量＝編碼＋1，但不是每個寫 0 的欄位都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 指一項操作影響的物件範圍。retention 是狀態是否保留。Controller Reset（清 CC.EN）是一種 Controller Level Reset，簡稱 CLR；同一類 CLR 的不同觸發方式，Register 保留規則仍可能不同。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>同一筆命令，五個不同的觀察時點</h2><p class="qa-takeaway">看見進度不等於看見成功；先指出你觀察到哪一個階段。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">時點</th><th scope="col">能確認的事情</th><th scope="col">尚不能確認的事情</th></tr></thead><tbody><tr><td>寫好 SQE</td><td>Host 已填 Opcode、CID、NSID、資料指標</td><td>controller 是否已看見</td></tr><tr><td>更新 SQ Tail</td><td>命令已提交；記憶體可見性另須保證</td><td>命令是否已取得或完成</td></tr><tr><td>CQE 回報 SQHD 前進</td><td>controller 已消費至回報的位置</td><td>那幾格的所有命令都已完成</td></tr><tr><td>目標 CQE Phase 有效</td><td>可用 SQID＋CID 對回這筆完成，讀 SCT／SC</td><td>一定已產生中斷，或資料一定持久</td></tr><tr><td>Host 更新 CQ Head</td><td>Host 已消費完成、歸還 CQ 空間</td><td>其他 SQ 或其他 CID 同時完成</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>SQ1 的 CID=7 與 SQ2 的 CID=7 可以同時存在。若共用 CQ，看到 CID=7 還不夠，要先看 CQE.SQID。若目標是確認 Write 的持久性，還須核對 WCE、FUA 或 Flush 的完成條件，不能只看成功 Status。</p>
<p class="qa-citations">來源：<a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-vwc">Base 2.4 §5.2.30.1.4</a> · <a href="#ref-nvmatomic">NVM Command Set 1.3 §2.1.2–2.1.4</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-031">Q31 · 一筆 NVMe Command 的 Opcode、CID、NSID、Data Pointer 及 Command Dword 各有什麼用途？</a></li>
<li><a href="#q-032">Q32 · Reserved 欄位非零、不合法 Command Dword 組合或不支援 Opcode 應如何處理？</a></li>
<li><a href="#q-033">Q33 · NSID 不存在、Inactive、不適用或錯誤使用 Broadcast NSID 時，應回傳什麼類型的 Status？</a></li>
<li><a href="#q-034">Q34 · CQE 中的 SQHD、SQID、CID、Phase Tag 及 Status 分別有什麼用途？</a></li>
<li><a href="#q-035">Q35 · Status Code Type 與 Status Code 應如何解析？</a></li>
<li><a href="#q-036">Q36 · More 與 Do Not Retry 位元分別代表什麼？DNR 為 0 是否代表一定能直接重試？</a></li>
<li><a href="#q-037">Q37 · Completion 已寫入但 Host 未處理，可能與 Phase Tag、CQ 位置或 Interrupt 有什麼關係？</a></li>
<li><a href="#q-038">Q38 · 多個 Command 同時 Outstanding 時，Controller 是否必須按照提交順序完成？</a></li>
<li><a href="#q-039">Q39 · 哪些 Command 具有順序相依性？Host 為什麼不能假設所有 Command 都依序完成？</a></li>
<li><a href="#q-040">Q40 · Outstanding Command 達到限制或 CQ Full 時，Controller 如何限制取得新 Command？</a></li>
<li><a href="#q-041">Q41 · Round Robin 與 Weighted Round Robin Arbitration 有什麼差異？</a></li>
<li><a href="#q-042">Q42 · Urgent、High、Medium 及 Low Queue Priority 在哪些情況下生效？</a></li>
<li><a href="#q-043">Q43 · 多個 Queue 競爭資源時，如何判斷 Arbitration 是否符合設定？</a></li>
</ol></section>
<article class="qa-question" id="q-031" data-question="31"><h2><a class="qa-qid" href="#q-031">Q31</a> 一筆 NVMe Command 的 Opcode、CID、NSID、Data Pointer 及 Command Dword 各有什麼用途？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-031-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-031-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>把「做什麼、對誰做、資料在哪、用哪些參數」編成 controller 可以讀取的命令。</p>
</li>
<li id="q-031-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Opcode 的意義先由 Admin／I/O command set 決定；相同數值放在不同命令集不一定是相同操作。</p>
</li>
<li id="q-031-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先查對應能力，如 OACS、ONCS、SGLS，並核對 namespace 的 CSI；不是所有命令都使用全部公共欄位。</p>
</li>
<li id="q-031-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CDW0 含 OPC、FUSE、PSDT、CID；NSID 選目標；MPTR／DPTR 描述資料；CDW10～15 由各命令定義。Common command 是 64 bytes。</p>
</li>
<li id="q-031-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>選 command set→查 Opcode 與能力→設定合法 NSID／參數→準備資料與指標→分配同 SQ 唯一 CID→提交。PCIe Admin 使用 PRP，不能任意改用 SGL。</p>
</li>
<li id="q-031-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>完成由 SQID+CID 對回；真正的資料或結果可能在 Host buffer 或 CQE DW0／1，不是全部塞在 Status。</p>
</li>
<li id="q-031-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援 opcode 為 Invalid Command Opcode（0/01h）；非法已定義欄位通常是 Invalid Field（0/02h），有專用錯誤則用其定義。</p>
</li>
<li id="q-031-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-031-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-031-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-031-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-031-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-031-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-031-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-031-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-031-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>核對 Opcode 所屬 command set、宣告能力與 payload 長度；DPTR 位址合法也不保證描述的資料長度足夠。</p>
</li>
<li id="q-031-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認 SQ 是 Admin 還是 I/O，以及使用哪份命令集解碼。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-032" data-question="32"><h2><a class="qa-qid" href="#q-032">Q32</a> Reserved 欄位非零、不合法 Command Dword 組合或不支援 Opcode 應如何處理？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-032-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-032-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>分清 reserved bits 與已定義欄位中的 reserved coded value，避免錯誤地要求所有保留位都必須被檢查。</p>
</li>
<li id="q-032-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>涉及 Host 建構命令的義務與 controller 的檢查義務，兩者不是同一句規定。</p>
</li>
<li id="q-032-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 Base §1.4.1 的 reserved 定義、Opcode 支援與每個命令的欄位限制。</p>
</li>
<li id="q-032-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Host 須將 reserved 欄位清零；接收端不必檢查 reserved bits／bytes／fields。已定義欄位收到 reserved 編碼則須報錯。</p>
</li>
<li id="q-032-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先建立全零 SQE，再填使用欄位；學習錯誤處理時一次只改一項，並記錄該要求是 shall 還是 should。</p>
</li>
<li id="q-032-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>合法組合依命令正常完成；controller 沒檢查某 reserved bit 不代表 Host 寫非零就合法。</p>
</li>
<li id="q-032-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>未支援或 reserved opcode：0/01h。定義欄位非法值：一般 0/02h，除非明定專用 Status。多錯誤並存通常可選其中一種；不把 reserved bit 非零一律判為必須 0/02h。</p>
</li>
<li id="q-032-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-032-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-032-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-032-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-032-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-032-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-032-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-032-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-032-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>測試報告應同時列 Host 是否違規、controller 是否有義務偵測；這樣才不會把合法的未檢查行為判成韌體 bug。</p>
</li>
<li id="q-032-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先問改到的是「保留位」還是「已定義欄位中的保留編碼」。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-conventions">Base 2.4 §1.4.1</a> · <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-033" data-question="33"><h2><a class="qa-qid" href="#q-033">Q33</a> NSID 不存在、Inactive、不適用或錯誤使用 Broadcast NSID 時，應回傳什麼類型的 Status？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-033-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-033-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>避免把不存在、未附加與命令根本不用 NSID 混成同一種錯誤。</p>
</li>
<li id="q-033-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>NSID 的 active 狀態是相對某 controller；另一條路徑可用不代表這個 controller 也可用。</p>
</li>
<li id="q-033-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>用 Active／Allocated namespace lists 及 command 的 NSID 使用規則判斷；再查命令有沒有例外。</p>
</li>
<li id="q-033-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>NSID=0、有效 allocated NSID、inactive NSID 與 FFFFFFFFh 必須分開解讀；FFFFFFFFh 的範圍由每條命令定義。</p>
</li>
<li id="q-033-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先確認命令是否用 NSID，再確認命令是否允許該 namespace 狀態與 broadcast。Identify 某些 CNS 本來就是查 allocated/inactive，不能套用一般 I/O 假設。</p>
</li>
<li id="q-033-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>合法目標依命令完成；某些查詢對不存在或 inactive 的回覆有特別規定，不能只套總表。</p>
</li>
<li id="q-033-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Figure 93 的預設：使用 NSID 的命令遇 inactive 回 Invalid Field（0/02h），invalid 回 Invalid Namespace or Format（0/0Bh）；不支援 broadcast 卻用 FFFFFFFFh，或不用 NSID 卻填非零，回 0/02h。命令例外優先。</p>
</li>
<li id="q-033-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-033-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-033-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-033-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-033-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-033-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-033-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-033-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-033-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>將原 SQE 的 NSID、當時 active list、CNS／FID／Opcode 規則一起核對；不要只用現在的清單解釋過去命令。</p>
</li>
<li id="q-033-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查命令是否真的屬於 Figure 93 的一般情況，或已有明確例外。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-034" data-question="34"><h2><a class="qa-qid" href="#q-034">Q34</a> CQE 中的 SQHD、SQID、CID、Phase Tag 及 Status 分別有什麼用途？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-034-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-034-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>一筆 CQE 同時提供命令結果、原命令身分與 queue 進度；這些欄位不能彼此代替。</p>
</li>
<li id="q-034-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>SQHD 屬於 CQE.SQID 指定的 SQ；P 屬於 CQ slot；Status 屬於 SQID+CID 指定的命令。</p>
</li>
<li id="q-034-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>使用當前 queue 配置與 CQE 的公共格式，不是由某個 Feature 選擇 SQHD 意義。</p>
</li>
<li id="q-034-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>DW2：SQHD、SQID；DW3：CID、P、Status；DW0／1 是命令特定結果。SQHD 表示建立 CQE 當時已消費的位置。</p>
</li>
<li id="q-034-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先以 P 驗有效性，再對 SQID+CID、解析 Status 與結果，更新 SQ 可用 slots，最後釋放 CQ slot。</p>
</li>
<li id="q-034-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例：一筆 completion 報 SQHD=8，表示 Head 已前進到 8，不表示 slots 0～7 的所有命令已執行完成。</p>
</li>
<li id="q-034-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Status 需同讀 SCT、SC；P 不屬錯誤碼。CQE 格式錯誤或未知 CID 先檢查記憶體／lifetime，不替它編造一個新的 NVMe Status。</p>
</li>
<li id="q-034-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-034-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-034-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-034-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-034-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-034-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-034-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-034-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-034-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>SQHD 進度、命令完成與資料 buffer 可回收的時機分開核對；可重用 SQ slot 不代表可提前釋放該命令資料。</p>
</li>
<li id="q-034-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認是新的 P，再解釋其他欄位；順序反過來容易將舊記憶體當錯誤完成。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-035" data-question="35"><h2><a class="qa-qid" href="#q-035">Q35</a> Status Code Type 與 Status Code 應如何解析？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-035-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-035-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>同一個 SC 數值在不同 SCT 有不同意義，必須用成對值判讀。</p>
</li>
<li id="q-035-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Status 屬於這筆完成，還要搭配 Opcode、command set 與錯誤發生條件。</p>
</li>
<li id="q-035-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>公共 SCT／SC 定義在 Base；NVM 特定狀態再看 NVM Command Set，不能用不同 command set 的表解釋。</p>
</li>
<li id="q-035-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>在 CQE DW3 中 SCT=bits27:25、SC=24:17，P=16；若程式先取最後 16-bit word，SCT 位置變為 11:9、SC 為 8:1。</p>
</li>
<li id="q-035-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先確認資料寬度與 endian，再抽 SCT／SC，選正確表，最後讀 DNR、More、CRD 與命令特定結果。</p>
</li>
<li id="q-035-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>SCT=0、SC=00h 表示 Successful Completion；SQID／CID 與 P 仍須正確，不能只看到低位元全零就認定這是新成功完成。</p>
</li>
<li id="q-035-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>例：0/01h 是 Invalid Command Opcode；1/01h 是 Invalid Queue Identifier。SCT=2 為 Media and Data Integrity，3 為 Path Related，7 為 Vendor Specific。</p>
</li>
<li id="q-035-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-035-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-035-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-035-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-035-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-035-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-035-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-035-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-035-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>保留原始 CQE bytes 與解碼值；不同工具若移除 P 或重新打包 Status，輸出的整數不能直接逐值比較。</p>
</li>
<li id="q-035-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否漏移除 Phase 或把 DW3 位元位置套到 16-bit Status word。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-036" data-question="36"><h2><a class="qa-qid" href="#q-036">Q36</a> More 與 Do Not Retry 位元分別代表什麼？DNR 為 0 是否代表一定能直接重試？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-036-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-036-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>把「可能重試成功」「是否有補充錯誤資訊」與「重試是否安全」分開。</p>
</li>
<li id="q-036-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>判讀同一筆 CQE；DNR 的相同命令重試語意涵蓋同一 NVM subsystem 的任何 controller。</p>
</li>
<li id="q-036-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>公共位元固定存在；CRD 的使用還需 Host Behavior Support.ACRE 與 Identify.CRDT1～3。</p>
</li>
<li id="q-036-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>DNR 不表示資料一定沒改；More=1 表示 LID 01h 有此命令的更多 Status 資訊，不是「還有另一筆 completion」。</p>
</li>
<li id="q-036-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先解析錯誤原因；若 DNR=0，修正暫時條件並依有效 CRD 等待，再判斷是否能安全重送。對非冪等操作，還要確認先前作業是否已生效。</p>
</li>
<li id="q-036-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>重試成功須看新 CQE。DNR=0 只說 may succeed，不保證立即成功，也不保證重送不會造成重複作用。</p>
</li>
<li id="q-036-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不變參數的非法命令重送未必有用；明定 DNR 的 Status 按其規則，例如 Command Interrupted（0/21h）要求 DNR=0，且需 ACRE 啟用才可回報。</p>
</li>
<li id="q-036-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-036-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-036-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-036-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-036-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-036-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-036-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-036-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-036-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>More=1 與 Error Information 中可關聯的額外資訊應一致；CRD 必須依 DNR／ACRE 決定是否有意義。</p>
</li>
<li id="q-036-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查錯誤是已明確完成，還是只有 Host timeout；沒有 CQE 時根本沒有可讀的 DNR。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-behavior">Base 2.4 §5.2.30.1.15</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-037" data-question="37"><h2><a class="qa-qid" href="#q-037">Q37</a> Completion 已寫入但 Host 未處理，可能與 Phase Tag、CQ 位置或 Interrupt 有什麼關係？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-037-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-037-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>將 controller 已張貼完成與 Host 已收到通知／已消費完成分成不同階段。</p>
</li>
<li id="q-037-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>涉及目標 CQ 的記憶體、Host Head／expected Phase 與 CQ 關聯中斷，未必是命令執行失敗。</p>
</li>
<li id="q-037-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>確認 Create CQ.IEN／IV、使用的 MSI 或 MSI-X 模式、mask 與中斷 Feature。</p>
</li>
<li id="q-037-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>MSI-X 檢查 Function Mask、vector mask／PBA；一般 MSI 的 INTMS／INTMC 規則不同。CQE 有效性仍以正確位置與 Phase 判斷。</p>
</li>
<li id="q-037-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先驗 Host 正在讀正確 CQ Head，再驗 P；有新 CQE 則處理。沒有中斷時再檢查 IEN、IV、mask、coalescing 與 Host handler。</p>
</li>
<li id="q-037-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>可輪詢處理一筆合法完成，即使它沒有一對一中斷。中斷數不必等於 completion 數。</p>
</li>
<li id="q-037-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>「沒收到中斷」本身沒有 NVMe error Status；原 CQE 甚至可能是成功。不要因此憑空回 Internal Error。</p>
</li>
<li id="q-037-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-037-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-037-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-037-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-037-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-037-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-037-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-037-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-037-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>比較 CQE 張貼、mask 改變、中斷到達與 Head 更新時間；IRQ 是通知，不是完成內容本身。</p>
</li>
<li id="q-037-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查 Host 是否讀錯 CQ／slot 或 expected Phase；這比先猜中斷遺失更直接。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-irq">PCIe Transport 1.4 §3.5</a> · <a href="#ref-irqfeat">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-038" data-question="38"><h2><a class="qa-qid" href="#q-038">Q38</a> 多個 Command 同時 Outstanding 時，Controller 是否必須按照提交順序完成？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-038-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-038-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>理解 queue 保存提交順序，不等於所有命令具備執行或完成的先後保證。</p>
</li>
<li id="q-038-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>一般獨立命令即使在同一 SQ，也不能假設 FIFO completion；跨 SQ 更不能靠相近提交時間建立依賴。</p>
</li>
<li id="q-038-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先看命令是否屬 fused operation 或有專屬順序規則；FUSES 表示 fused 支援。</p>
</li>
<li id="q-038-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>需要分開 submitted、consumed、processing、completed 四個階段；SQHD 只反映其中的 consumed。</p>
</li>
<li id="q-038-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>若 B 依賴 A 的結果，Host 等 A 成功完成後再提交 B；若需要媒體持久性，另套 Flush／FUA，不能只靠順序。</p>
</li>
<li id="q-038-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>沒有依賴的 Read B 先於 Read A 完成可以合法；Host 必須按 SQID／CID 分派，而不是按送出陣列順序。</p>
</li>
<li id="q-038-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>單純反序完成沒有錯誤 Status。若違反明定多命令序列，才依該序列專用錯誤判斷。</p>
</li>
<li id="q-038-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-038-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-038-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-038-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-038-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-038-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-038-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-038-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-038-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>測試需要驗命令要求的因果關係，不能用「看起來沒照順序」當唯一不合規證據。</p>
</li>
<li id="q-038-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先問兩筆命令有沒有規範明定或 Host 主動建立的相依關係。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-nvmatomic">NVM Command Set 1.3 §2.1.2–2.1.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-039" data-question="39"><h2><a class="qa-qid" href="#q-039">Q39</a> 哪些 Command 具有順序相依性？Host 為什麼不能假設所有 Command 都依序完成？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-039-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-039-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>把真正的相依序列明確建立，避免把一般 queue 排隊當成交易機制。</p>
</li>
<li id="q-039-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>典型例子：CQ→SQ 建立、SQ→CQ 刪除、Set Features 成功→受新值影響的新命令，以及支援的 fused pair。</p>
</li>
<li id="q-039-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 FUSES、所選 Feature 與各命令規則；不是用一個全域「按順序」能力位解決所有情況。</p>
</li>
<li id="q-039-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>FUSE=01b／10b 表示成對第一／第二筆；PCIe 中必須在同一 SQ 相鄰並用同一次 Tail 更新提交。</p>
</li>
<li id="q-039-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>一般依賴用等待 completion 建立；fused pair 依其專用規則一同提交，兩筆各有 CQE。不要把兩筆同時提交後再猜 controller 會替 Host 排好。</p>
</li>
<li id="q-039-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Set Features 成功後才提交的命令使用新設定；早已提交的命令可能使用舊或新設定。需要一致測試時先排空。</p>
</li>
<li id="q-039-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>缺少相鄰 fused partner：Command Aborted due to Missing Fused Command（0/0Ah）；CQ/SQ 相依錯誤按 Create／Delete 專用 Status，不一律 0/0Ch。</p>
</li>
<li id="q-039-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-039-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-039-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-039-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-039-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-039-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-039-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-039-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-039-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>畫出各 completion 與下一次 submission 的邊界；FUA 控制持久性，不會代替這些相依關係。</p>
</li>
<li id="q-039-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查 Host 是否真的等待前一步成功，而非只等待提交函式返回。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-nvmatomic">NVM Command Set 1.3 §2.1.2–2.1.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-040" data-question="40"><h2><a class="qa-qid" href="#q-040">Q40</a> Outstanding Command 達到限制或 CQ Full 時，Controller 如何限制取得新 Command？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-040-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-040-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>區分 Host 的可提交容量、controller 內部執行資源與 CQ 可張貼容量，避免用單一 queue depth 解釋全部停滯。</p>
</li>
<li id="q-040-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>限制可針對 SQ、共享 CQ 或 controller 內部資源；不是每個限制都代表整個 controller 失效。</p>
</li>
<li id="q-040-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Host 依 queue size／SQHD 保留空間與唯一 CID；不要把其他 transport 的 MAXCMD 流量控制假設直接套到 PCIe。</p>
</li>
<li id="q-040-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>內部取得已提交 SQE 的算法是 vendor specific；仲裁決定從哪條 SQ 開始處理 candidate commands。取得與開始執行也不同。</p>
</li>
<li id="q-040-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>Host 不覆寫未消費 SQE；controller 不向滿 CQ 張貼，必要時停止處理相關 SQ 的更多命令，獨立 SQ 仍繼續。</p>
</li>
<li id="q-040-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>容量釋放後可正常前進；SQ slot 已釋放但命令仍 outstanding 是可能的，因為取得不等於完成。</p>
</li>
<li id="q-040-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>到達正常資源限制不自动要求錯誤 CQE；違反 queue 指標、重用 CID 或超過特定命令限制時才按各自規則回應。</p>
</li>
<li id="q-040-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-040-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-040-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-040-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>這不是逐命令歷史；只有支援且符合記錄條件的指定事件需要 PEL 紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-040-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>清 CC.EN 後 I/O queue 失效、Admin 指標重設；保留的基底位址不代表舊完成有效。 <a class="qa-rule-link" href="#common-queue-12">本冊完整規則</a></p>
</li>
<li id="q-040-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>受影響 controller 的 queue 要重建；不能沿用 CC.EN Reset 的 Register 保留例外。 <a class="qa-rule-link" href="#common-queue-13">本冊完整規則</a></p>
</li>
<li id="q-040-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>重新初始化 queue 與 Host 追蹤；舊記憶體內容不是新一輪的有效命令。 <a class="qa-rule-link" href="#common-queue-14">本冊完整規則</a></p>
</li>
<li id="q-040-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Queue 隸屬 controller；同一 CQ 的空間與生命週期會影響所有共用它的 SQ。 <a class="qa-rule-link" href="#common-queue-15">本冊完整規則</a></p>
</li>
<li id="q-040-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>以不同階段的證據核對，不可只觀察 Host submission count 就宣告 controller 已同時執行全部命令。</p>
</li>
<li id="q-040-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先辨認滿的是 SQ、CQ，還是僅 Host 的 outstanding 配額。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-041" data-question="41"><h2><a class="qa-qid" href="#q-041">Q41</a> Round Robin 與 Weighted Round Robin Arbitration 有什麼差異？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-041-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-041-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>決定多條 SQ 都有可處理工作時，下一批從哪條開始，並允許 Host 表達服務優先級。</p>
</li>
<li id="q-041-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>仲裁控制開始處理 candidate commands 的選擇，不保證 completion 順序或固定 IOPS 比例。</p>
</li>
<li id="q-041-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>所有 controller 支援 Round Robin；選配 WRR 看 CAP.AMS，再用 CC.AMS 選擇。</p>
</li>
<li id="q-041-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>FID 01h 提供 Arbitration Burst（AB）及 HPW／MPW／LPW；SQ.QPRIO 在 WRR 生效。AB=7 表示不限 burst，其他值為 2^AB；權重為欄位值+1。</p>
</li>
<li id="q-041-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>Disable 時選 CC.AMS；Enable 後設定 FID 01h，建立 SQ 的 QPRIO，再以持續可執行的工作觀察選擇行為。</p>
</li>
<li id="q-041-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>RR 對含 Admin 的 SQ 平等輪流；WRR 先 Admin，再 Urgent，再依權重分配 High／Medium／Low，類別內還有輪流規則。</p>
</li>
<li id="q-041-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援 CC.AMS 的 Register 設定是 undefined，不是 Set Features 的 Invalid Field。FID 01h 非法已定義參數則按命令規則。</p>
</li>
<li id="q-041-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-041-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-041-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-041-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get 本身不產生 Set Feature Event；Set 則要確認此 FID 的記錄支援、是否成功及設定是否改變。 <a class="qa-rule-link" href="#common-feature_events-11">本冊完整規則</a></p>
</li>
<li id="q-041-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>依 scope、可保存能力及重設涵蓋範圍決定；整體與部分重設的恢復規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-041-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確定整個或部分 subsystem 受影響；不可保存但持續的值不會因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-041-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存值依 Saved 恢復；不可保存的值另查持續性及該 Feature 的例外。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-041-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-041-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Get FID 01h 讀回只是設定證據；執行時間、媒體衝突與 CQ 壓力也影響量測吞吐，不能只拿 IOPS 比值判斷 WRR。</p>
</li>
<li id="q-041-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先看 CC.AMS 是否真的選 WRR，再解讀 QPRIO 與權重。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-arbit">Base 2.4 §5.2.30.1.1</a> · <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-042" data-question="42"><h2><a class="qa-qid" href="#q-042">Q42</a> Urgent、High、Medium 及 Low Queue Priority 在哪些情況下生效？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-042-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-042-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>讓不同 SQ 取得不同服務機會，但只有選用對應仲裁機制時才有意義。</p>
</li>
<li id="q-042-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>QPRIO 是 SQ 層級設定，不是每筆 Read／Write 的 priority 欄位。</p>
</li>
<li id="q-042-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>CAP.AMS 支援 WRR 且 CC.AMS 已選 WRR 才使用 QPRIO；否則 controller 必須忽略它。</p>
</li>
<li id="q-042-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Create SQ CDW11.QPRIO：00b Urgent、01b High、10b Medium、11b Low；FID 01h 為後三種設定權重。</p>
</li>
<li id="q-042-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>依工作類型建立 SQ 並設 QPRIO；想改既有 SQ 屬性，須按 queue 重建流程，不是改 Host 記憶體中的舊 Create SQE。</p>
</li>
<li id="q-042-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Urgent 高於加權類別但低於 Admin；連續 Urgent 工作可能讓較低類別飢餓，不能期待 High 永遠有固定最低頻寬。</p>
</li>
<li id="q-042-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>在 RR 模式下 QPRIO 被忽略是合法行為，不應回報「優先級功能失效」；非法 queue 參數仍按 Create Status。</p>
</li>
<li id="q-042-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-042-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-042-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-042-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get 本身不產生 Set Feature Event；Set 則要確認此 FID 的記錄支援、是否成功及設定是否改變。 <a class="qa-rule-link" href="#common-feature_events-11">本冊完整規則</a></p>
</li>
<li id="q-042-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>依 scope、可保存能力及重設涵蓋範圍決定；整體與部分重設的恢復規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-042-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確定整個或部分 subsystem 受影響；不可保存但持續的值不會因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-042-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存值依 Saved 恢復；不可保存的值另查持續性及該 Feature 的例外。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-042-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-042-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>將每條 SQ 的 QPRIO、CC.AMS 與 FID 01h 一起保存；缺任一項都不足以解釋優先行為。</p>
</li>
<li id="q-042-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先排除其實正在用 RR 的情況。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-arbit">Base 2.4 §5.2.30.1.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-043" data-question="43"><h2><a class="qa-qid" href="#q-043">Q43</a> 多個 Queue 競爭資源時，如何判斷 Arbitration 是否符合設定？</h2>
<p class="qa-prompt">先試著說明正常流程與一個不符合前提的例子，再展開核對。</p>
<details class="qa-answer" id="q-043-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-043-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>把規範對 candidate 選擇的要求轉成可判讀證據，避免把延遲或吞吐差異直接當成仲裁違規。</p>
</li>
<li id="q-043-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>觀察同一 controller 的競爭 SQ；先排除 CQ Full、命令依賴、不同服務成本與 Host 供應不足。</p>
</li>
<li id="q-043-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>記錄 CAP.AMS、CC.AMS、FID 01h 的 AB／權重及每條 SQ 的 QPRIO。</p>
</li>
<li id="q-043-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>WRR 高／中／低每輪能開始處理的數量受剩餘 credits 與 AB 限制；需要知道是否有 ready candidate，不只 SQ 是否非空。</p>
</li>
<li id="q-043-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>用相近命令類型與大小、持續供應且 CQ 不阻塞的教學情境；比較可觀測的開始處理或排程紀錄，只有 CQE 時需承認無法還原全部內部選擇。</p>
</li>
<li id="q-043-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例如 High／Low 權重 4:1 指服務 credits，不能要求每個短時間窗口都剛好完成 4:1。</p>
</li>
<li id="q-043-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Arbitration 量測本身没有錯誤 CQE；先驗設定命令成功，再對照規範的 shall／may。供應條件不成立時，不宜判不合規。</p>
</li>
<li id="q-043-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>有 CQE 才適用。本題未另指定固定的 DNR／More 覆寫值，使用本冊 CQE 位元判讀規則。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-043-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>此題的正常完成本身不保證 AER；另有指定事件時，確認支援、設定及 pending request。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-043-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>對照本題的完成結果與錯誤紀錄；新增 Entry 的條件使用本冊共用規則，不以失敗次數直接推算。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-043-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Get 本身不產生 Set Feature Event；Set 則要確認此 FID 的記錄支援、是否成功及設定是否改變。 <a class="qa-rule-link" href="#common-feature_events-11">本冊完整規則</a></p>
</li>
<li id="q-043-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>依 scope、可保存能力及重設涵蓋範圍決定；整體與部分重設的恢復規則不同。 <a class="qa-rule-link" href="#common-feature-12">本冊完整規則</a></p>
</li>
<li id="q-043-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>先確定整個或部分 subsystem 受影響；不可保存但持續的值不會因此清零。 <a class="qa-rule-link" href="#common-feature-13">本冊完整規則</a></p>
</li>
<li id="q-043-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>可保存值依 Saved 恢復；不可保存的值另查持續性及該 Feature 的例外。 <a class="qa-rule-link" href="#common-feature-14">本冊完整規則</a></p>
</li>
<li id="q-043-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>按 Feature scope 判斷其他 controller／namespace 是否共用同一設定。 <a class="qa-rule-link" href="#common-feature-15">本冊完整規則</a></p>
</li>
<li id="q-043-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>要判違規，需指出哪一條明定選擇規則與哪段證據矛盾，而不是只有「高優先比較慢」。</p>
</li>
<li id="q-043-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查高優先 SQ 是否真的持續有可開始處理的 candidate，並確認 CQ 沒滿。</p>
</li>
</ol><details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-arbit">Base 2.4 §5.2.30.1.1</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-command-8"><h3>命令完成、事件與紀錄 · DNR 與 More 應如何設定？</h3><p>有 CQE 時，DNR=1 表示相同命令再送到此 NVM subsystem 的任一 controller 仍預期失敗；DNR=0 只表示可能成功。除非本題錯誤另有明定，不把某個 Status 固定綁成 DNR=1。More=1 表示 Error Information Log 有這筆命令的補充資訊。SCT=SC=0 時 DNR 應為 0。</p></article>
<article id="common-command-9"><h3>命令完成、事件與紀錄 · 是否產生 Asynchronous Event？</h3><p>命令完成與非同步通知是兩件事；本題操作成功本身不保證有事件。若操作引起規範列出的事件，還要核對事件支援、適用的通知設定、是否已遮蔽，以及 Host 是否掛入 Asynchronous Event Request。</p></article>
<article id="common-command-10"><h3>命令完成、事件與紀錄 · 是否更新 Error Information Log 或其他 Log？</h3><p>成功 CQE 不是要求新增 Error Information 的理由。錯誤有 More=1 時，查 LID 01h 並用 SQID、CID 和 Error Count 對應；不能把每個非成功 CQE 都當成必須新增一筆。操作改變的狀態則由本題列出的查詢介面重新讀取。</p></article>
<article id="common-command-11"><h3>命令完成、事件與紀錄 · 是否記錄於 Persistent Event Log？</h3><p>Persistent Event Log 是選配的事件歷史，不是所有命令的執行清單。先查 LPA 的支援與 Supported Events Bitmap，再判斷本次是否符合指定事件的記錄條件；不能只因命令成功或失敗就要求新增一筆。</p></article>
<article id="common-feature-12"><h3>Feature 的重設與影響範圍 · Controller Reset 後是否保留或繼續？</h3><p>先分 scope 與 saveable。整個 subsystem 受重設影響時，可保存 Feature 的 Current 回 Saved（沒有 Saved 則 Default）；不可保存且不持續的回 Default。多 controller 只重設其中一個時，共用 scope 另依 Figure 127 保留；本題列出的個別 Feature 規則優先。</p></article>
<article id="common-feature-13"><h3>Feature 的重設與影響範圍 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>不能只看 Reset 名稱。若重設涵蓋整個 subsystem，使用 Figure 126；若 multi-domain 的重設只涵蓋一部分，使用 Figure 127。不可保存但規定持續的值繼續保留，不能誤用「不可保存＝重設清零」。</p></article>
<article id="common-feature-14"><h3>Feature 的重設與影響範圍 · Power Cycle 後是否保留或繼續？</h3><p>可保存且 SV=1 成功的設定，在斷電後依 Saved 恢復；SV=0 不會更新 Saved。不可保存的 Feature 才看 Figure 466 的持續性欄與個別例外。重新取得 Current 和行為結果，不能只看到 Saved 存在就假設硬體正在使用它。</p></article>
<article id="common-feature-15"><h3>Feature 的重設與影響範圍 · 是否影響其他 Controller 或 Namespace？</h3><p>依 Feature scope 決定。Controller scope 通常只控制目標 controller；namespace、NVM Set 或 subsystem scope 可能由其他 controller 共同觀察。跨 Host 修改共用設定需要協調，不能把 NSID=FFFFFFFFh 當成所有 Feature 通用的廣播。</p></article>
<article id="common-feature_events-11"><h3>Set Feature 的事件記錄 · 是否記錄於 Persistent Event Log？</h3><p>若支援 PEL 的 Set Feature Event，還要看 Figure 252 是否支援記錄此 FID：Set 成功且設定改變時必須記錄；成功但重設相同值則允許記錄。不是每個 FID 都能套用此事件；Timestamp 的 Set Feature Event 明確禁止，另用 Timestamp Change Event 判斷。</p></article>
<article id="common-queue-12"><h3>Queue 的重設與影響範圍 · Controller Reset 後是否保留或繼續？</h3><p>清除 CC.EN 使 Controller Level Reset 執行：I/O SQ／CQ 被刪除，Admin Queue 的指標重設；AQA／ASQ／ACQ 在這種重設中保留不代表舊 CQE 仍有效。重新初始化 Admin CQ 的 Phase，Enable 後重新配置及建立 I/O Queue。</p></article>
<article id="common-queue-13"><h3>Queue 的重設與影響範圍 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>受 NVM Subsystem Reset 影響的 controller 執行 Controller Level Reset；舊 Queue 不能沿用。Host 應重新確認傳輸與 Register 狀態，再建立 Admin／I/O 操作環境，不套用 CC.EN 重設對 AQA 等 Register 的保留例外。</p></article>
<article id="common-queue-14"><h3>Queue 的重設與影響範圍 · Power Cycle 後是否保留或繼續？</h3><p>斷電後重新走初始化與 Queue 建立流程。主機記憶體中即使還有舊 SQE／CQE 位元，也不是新一輪 Queue 的有效命令或完成；Host 必須重建自己的指標、Phase 與 outstanding 對照。</p></article>
<article id="common-queue-15"><h3>Queue 的重設與影響範圍 · 是否影響其他 Controller 或 Namespace？</h3><p>Queue 屬於建立它的 controller，不因相同 QID 就和別的 controller 共用。共用 CQ 的多個 SQ 則有直接關係：CQ 空間不足或刪除順序會影響它們。Queue 重設不等於刪除 namespace 或撤銷已完成的資料寫入。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁＝PDF 頁−26；另兩份相同。以下依本次提供的 PDF 本文定位，保留 Figure 編號；共享頁只引用本題需要的定義，不納入 Fabrics 或 PCIe Link／封包內容。</p><ul class="qa-references">
<li id="ref-conventions"><strong>Base 2.4 · §1.4.1</strong><br>文件頁 2–3 · PDF 28–29</li>
<li id="ref-cap"><strong>Base 2.4 · §3.1.4 (CAP, VS)</strong><br>文件頁 54–59 · PDF 80–85 · Figure 36–37</li>
<li id="ref-nsid"><strong>Base 2.4 · §3.2.1</strong><br>文件頁 78–81 · PDF 104–107</li>
<li id="ref-queue"><strong>Base 2.4 · §3.3.1</strong><br>文件頁 88–91 · PDF 114–117 · Figure 73–74</li>
<li id="ref-order"><strong>Base 2.4 · §3.4.1–3.4.5</strong><br>文件頁 101–105 · PDF 127–131 · Figure 80–81</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-sqe"><strong>Base 2.4 · §4.1.1</strong><br>文件頁 139–142 · PDF 165–168 · Figure 92–93</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>文件頁 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>文件頁 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-featureeffects"><strong>Base 2.4 · §5.2.13.1.18</strong><br>文件頁 276–278 · PDF 302–304 · Figure 270–271</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>文件頁 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>文件頁 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-arbit"><strong>Base 2.4 · §5.2.30.1.1</strong><br>文件頁 460 · PDF 486 · Figure 467</li>
<li id="ref-vwc"><strong>Base 2.4 · §5.2.30.1.4</strong><br>文件頁 464–465 · PDF 490–491 · Figure 471</li>
<li id="ref-behavior"><strong>Base 2.4 · §5.2.30.1.15</strong><br>文件頁 475–477 · PDF 501–503 · Figure 491</li>
<li id="ref-irqfeat"><strong>Base 2.4 · §5.2.30.2.1–5.2.30.2.2</strong><br>文件頁 514–515 · PDF 540–541 · Figure 543–544</li>
<li id="ref-create"><strong>Base 2.4 · §5.3.1–5.3.2</strong><br>文件頁 527–531 · PDF 553–557 · Figure 571–579</li>
<li id="ref-delete"><strong>Base 2.4 · §5.3.3–5.3.4</strong><br>文件頁 531–532 · PDF 557–558 · Figure 580–583</li>
<li id="ref-fatal"><strong>Base 2.4 · §9.1–9.6.1</strong><br>文件頁 825–826 · PDF 851–852</li>
<li id="ref-nvmatomic"><strong>NVM Command Set 1.3 · §2.1.2–2.1.4</strong><br>文件頁 14–20 · PDF 14–20 · Figure 3–9</li>
<li id="ref-pcie"><strong>PCIe Transport 1.4 · §3.1–3.4</strong><br>文件頁 9–13 · PDF 9–13 · Figure 3–8</li>
<li id="ref-irq"><strong>PCIe Transport 1.4 · §3.5</strong><br>文件頁 13–16 · PDF 13–16 · Figure 9</li>
</ul><h3>需要看欄位圖時</h3><p>既有圖表教學各有固定位置。這裡連回相關圖，不複製另一份圖解。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="/nvme/figure-reference/features/zh-tw/#figure-b543">Base 2.4 Figure 543 · Interrupt Coalescing – Command Dword 11</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/commands/en/">English</a><a href="/DOCS/nvme-question-bank/commands.html">繁中教學 HTML</a></nav>
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
