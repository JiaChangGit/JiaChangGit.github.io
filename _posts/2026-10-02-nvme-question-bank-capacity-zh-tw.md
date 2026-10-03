---
layout: post
title: "NVMe 自問自答題庫：NVM Set、Endurance Group 與容量"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/capacity/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/capacity/en/">English</a><a href="/DOCS/nvme-question-bank/capacity.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–320</p>
<header><p class="qa-range">Q256–Q267</p><h1>NVM Set、Endurance Group 與容量</h1><p class="qr-intro">容量欄位分布於不同管理層級，健康計數也有自己的範圍。本冊先理解歸屬，再計算 Create／Delete 實際改變哪一層的容量。</p><p>先練習，再展開每題的 17 項解答。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>容量不是只有一個剩餘數字</h2><p class="qa-takeaway">namespace 的 blocks、Group 的 bytes 與實體容量調整不能混算。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">層級</th><th scope="col">觀察</th><th scope="col">常見誤解</th></tr></thead><tbody><tr><td>Namespace</td><td>NSZE、NCAP、LBA Format</td><td>把 blocks 直接當 bytes</td></tr><tr><td>Set／Group</td><td>總容量與未配置容量</td><td>把不同資源池加總兩次</td></tr><tr><td>實體配置</td><td>CAF、配置粒度</td><td>假設邏輯容量等於消耗量</td></tr><tr><td>健康</td><td>LID09h、EGCW</td><td>用 SMART 單位解 Group 計數</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>CAF=200 時，要求 5GiB 的 Group 可消耗 10GiB 的上層容量，還需考慮配置粒度。這不表示 namespace 的每個 LBA 大小也加倍。</p>
<p class="qa-citations">來源：<a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-256">Q256 · NVM Set、Endurance Group 與 Namespace 是什麼關係？</a></li>
<li><a href="#q-257">Q257 · 如何從 Identify 探索 NVM Set 與 Endurance Group？</a></li>
<li><a href="#q-258">Q258 · Namespace 如何建立於指定 Set 或 Group？</a></li>
<li><a href="#q-259">Q259 · 指定不存在的 NVM Set 或 Endurance Group 時會怎樣？</a></li>
<li><a href="#q-260">Q260 · Endurance Group Information Log 提供哪些健康與容量資訊？</a></li>
<li><a href="#q-261">Q261 · Endurance Group 的警告、Spare 與壽命事件如何更新？</a></li>
<li><a href="#q-262">Q262 · 如何確認總容量與未配置容量？</a></li>
<li><a href="#q-263">Q263 · Namespace 建立與刪除如何改變未配置容量？</a></li>
<li><a href="#q-264">Q264 · Capacity Management 如何配置或釋放 Group 與 Set？</a></li>
<li><a href="#q-265">Q265 · 要求容量或物件數超過可用資源時應回什麼？</a></li>
<li><a href="#q-266">Q266 · 容量配置完成後，哪些 Identify 與 Log 應更新？</a></li>
<li><a href="#q-267">Q267 · Reset 與 Power Cycle 後 Group、Set 與容量配置如何保留？</a></li>
</ol></section>
<article class="qa-question" id="q-256" data-question="256"><h2><a class="qa-qid" href="#q-256">Q256</a> NVM Set、Endurance Group 與 Namespace 是什麼關係？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-256-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-256-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這些物件分別組織容量、耐用度與邏輯存取，不能把它們當作同一個 ID 的不同名字。</p>
</li>
<li id="q-256-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>支援 NVM Set 時，formatted namespace 完整位於一個 Set；Set 完整位於一個 Endurance Group；Group 完整位於一個 domain。</p>
</li>
<li id="q-256-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 CTRATT 的 Set／Group 支援與各 List，再讀 namespace 的 NVMSETID、ENDGID。</p>
</li>
<li id="q-256-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>NVM Set List 回容量與所屬 Group；Endurance Group Log 回其健康與容量；Identify Namespace 回邏輯 block 與歸屬。</p>
</li>
<li id="q-256-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先畫支援的層級，再填實際 ID。未支援 NVM Sets 時，不要畫出虛構的 Set0 當必要中間層。</p>
</li>
<li id="q-256-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例如 EG1 有 Set2、Set3，各有 namespaces；同 Group 的 Sets 由該 Group 共同管理耐用度。</p>
</li>
<li id="q-256-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>NVM Sets 支援要求同時支援 Endurance Groups；反方向不成立，Group 可以存在而沒有 Set 功能。</p>
</li>
<li id="q-256-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-256-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>容量配置本身不保證一個通用完成 AER；若刪除 Set／Group 連帶刪除 namespaces，須依明定的 namespace 清單與通知規則更新受影響 controller。 <a class="qa-rule-link" href="#common-capacity_op-9">本冊完整規則</a></p>
</li>
<li id="q-256-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>配置完成後核對 Group／Set／Namespace 清單與對應層級的容量欄位。 <a class="qa-rule-link" href="#common-capacity_op-10">本冊完整規則</a></p>
</li>
<li id="q-256-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Capacity Management 本身沒有一個通用的專用 PEL 完成事件。 <a class="qa-rule-link" href="#common-capacity_op-11">本冊完整規則</a></p>
</li>
<li id="q-256-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>已完成的 Group、Set 與 namespace 配置不是普通 CLR 的暫存 queue，不能因 controller 重設就當作刪除。 <a class="qa-rule-link" href="#common-capacity_op-12">本冊完整規則</a></p>
</li>
<li id="q-256-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 與 Restore Default Capacity Configuration 是不同操作。 <a class="qa-rule-link" href="#common-capacity_op-13">本冊完整規則</a></p>
</li>
<li id="q-256-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>已完成的容量配置跨 Power Cycle 保留。 <a class="qa-rule-link" href="#common-capacity_op-14">本冊完整規則</a></p>
</li>
<li id="q-256-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>刪除 Endurance Group 會連帶刪除所含 NVM Sets 與 namespaces；刪 Set 也會刪其 namespaces，影響所有附加路徑。 <a class="qa-rule-link" href="#common-capacity_op-15">本冊完整規則</a></p>
</li>
<li id="q-256-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>用 namespace、Set、Group 三種查詢確認相同歸屬，避免只看一個名稱相近的 ID。</p>
</li>
<li id="q-256-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查裝置實際支援哪些層級，再判斷欄位的零值。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-257" data-question="257"><h2><a class="qa-qid" href="#q-257">Q257</a> 如何從 Identify 探索 NVM Set 與 Endurance Group？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-257-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-257-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>支援位元回答有沒有能力，清單回答目前有哪些物件，最大 ID 則不是目前物件數。</p>
</li>
<li id="q-257-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>探索以所查 controller 能取得的 subsystem／domain 資訊為準。</p>
</li>
<li id="q-257-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 CTRATT、NSETIDMAX、ENDGIDMAX；再取 NVM Set List 與 Endurance Group List。</p>
</li>
<li id="q-257-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Set 屬性有總容量、未配置容量及 ENDGID；Group 的詳細容量和健康需再讀 LID09h。</p>
</li>
<li id="q-257-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先讀能力，再分段列舉有效 ID，最後逐個讀屬性與健康；不要從 1 到最大 ID 全部假定存在。</p>
</li>
<li id="q-257-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>取得目前物件及歸屬，能分清沒有配置與不支援能力。</p>
</li>
<li id="q-257-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援時輸出的相應 ID 欄位須按規範清零；這不代表真的存在可供指定的有效 ID0。</p>
</li>
<li id="q-257-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-257-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>容量配置本身不保證一個通用完成 AER；若刪除 Set／Group 連帶刪除 namespaces，須依明定的 namespace 清單與通知規則更新受影響 controller。 <a class="qa-rule-link" href="#common-capacity_op-9">本冊完整規則</a></p>
</li>
<li id="q-257-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>配置完成後核對 Group／Set／Namespace 清單與對應層級的容量欄位。 <a class="qa-rule-link" href="#common-capacity_op-10">本冊完整規則</a></p>
</li>
<li id="q-257-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Capacity Management 本身沒有一個通用的專用 PEL 完成事件。 <a class="qa-rule-link" href="#common-capacity_op-11">本冊完整規則</a></p>
</li>
<li id="q-257-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>已完成的 Group、Set 與 namespace 配置不是普通 CLR 的暫存 queue，不能因 controller 重設就當作刪除。 <a class="qa-rule-link" href="#common-capacity_op-12">本冊完整規則</a></p>
</li>
<li id="q-257-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 與 Restore Default Capacity Configuration 是不同操作。 <a class="qa-rule-link" href="#common-capacity_op-13">本冊完整規則</a></p>
</li>
<li id="q-257-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>已完成的容量配置跨 Power Cycle 保留。 <a class="qa-rule-link" href="#common-capacity_op-14">本冊完整規則</a></p>
</li>
<li id="q-257-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>刪除 Endurance Group 會連帶刪除所含 NVM Sets 與 namespaces；刪 Set 也會刪其 namespaces，影響所有附加路徑。 <a class="qa-rule-link" href="#common-capacity_op-15">本冊完整規則</a></p>
</li>
<li id="q-257-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>核對宣告、清單、最大 ID 與 namespace 歸屬的一致性。</p>
</li>
<li id="q-257-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否把 NSETIDMAX／ENDGIDMAX 誤當成現有總數。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-258" data-question="258"><h2><a class="qa-qid" href="#q-258">Q258</a> Namespace 如何建立於指定 Set 或 Group？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-258-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-258-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>選擇歸屬可讓新 namespace 使用指定資源池；邏輯容量還需換算成該格式的 blocks。</p>
</li>
<li id="q-258-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Create 的歸屬欄位決定新物件所在位置，不是把既有 namespace 搬過去。</p>
</li>
<li id="q-258-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查支援的 Lists、可用容量與 LBA Format，再確認 NVMSETID／ENDGID 的組合。</p>
</li>
<li id="q-258-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>NVM Namespace Create 資料包含 NSZE、NCAP、FLBAS、DPS 與歸屬 ID；NCAP 不得大於 NSZE。</p>
</li>
<li id="q-258-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>兩個 ID 都為 0 可由 controller 選擇；指定 Group 而 Set=0 時在該 Group 中選；指定 Set 必須搭配正確的非零 Group。</p>
</li>
<li id="q-258-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功 CQE.DW0 回新 NSID，再讀 allocated Identify 確認實際歸屬；Create 不會自動完成 Attachment。</p>
</li>
<li id="q-258-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>指定不存在或不匹配的組合不能當成自動選擇；須按 Create 的非法欄位／資源錯誤處理。</p>
</li>
<li id="q-258-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-258-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>容量配置本身不保證一個通用完成 AER；若刪除 Set／Group 連帶刪除 namespaces，須依明定的 namespace 清單與通知規則更新受影響 controller。 <a class="qa-rule-link" href="#common-capacity_op-9">本冊完整規則</a></p>
</li>
<li id="q-258-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>配置完成後核對 Group／Set／Namespace 清單與對應層級的容量欄位。 <a class="qa-rule-link" href="#common-capacity_op-10">本冊完整規則</a></p>
</li>
<li id="q-258-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Capacity Management 本身沒有一個通用的專用 PEL 完成事件。 <a class="qa-rule-link" href="#common-capacity_op-11">本冊完整規則</a></p>
</li>
<li id="q-258-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>已完成的 Group、Set 與 namespace 配置不是普通 CLR 的暫存 queue，不能因 controller 重設就當作刪除。 <a class="qa-rule-link" href="#common-capacity_op-12">本冊完整規則</a></p>
</li>
<li id="q-258-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 與 Restore Default Capacity Configuration 是不同操作。 <a class="qa-rule-link" href="#common-capacity_op-13">本冊完整規則</a></p>
</li>
<li id="q-258-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>已完成的容量配置跨 Power Cycle 保留。 <a class="qa-rule-link" href="#common-capacity_op-14">本冊完整規則</a></p>
</li>
<li id="q-258-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>刪除 Endurance Group 會連帶刪除所含 NVM Sets 與 namespaces；刪 Set 也會刪其 namespaces，影響所有附加路徑。 <a class="qa-rule-link" href="#common-capacity_op-15">本冊完整規則</a></p>
</li>
<li id="q-258-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>比對回傳 NVMSETID、ENDGID 與容量扣除的層級，確認不是只建立成功卻查錯物件。</p>
</li>
<li id="q-258-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查所選 Set 真的屬於指定 Group，而不是只確認兩個 ID 各自存在。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-259" data-question="259"><h2><a class="qa-qid" href="#q-259">Q259</a> 指定不存在的 NVM Set 或 Endurance Group 時會怎樣？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-259-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-259-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>ID0 與不存在的非零 ID 可能有不同意義，而且同一個零值在不同命令也不同。</p>
</li>
<li id="q-259-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>先限定操作是 Namespace Create、Capacity Create/Delete、Get Log 還是 Feature。</p>
</li>
<li id="q-259-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>從相應 List 驗證目前有效 ID，再讀該命令欄位的特殊值定義。</p>
</li>
<li id="q-259-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>例如 Capacity Create Group 的 ELID=0 可自動選 domain；Delete Group 的 ELID=0 則非法。</p>
</li>
<li id="q-259-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先建立合法對照案例，再只換成不存在的非零 ID，避免混入格式、scope 等其他錯誤。</p>
</li>
<li id="q-259-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>合法自動選擇應成功並回實際 ID；非法明確 ID 不應悄悄改成別的物件。</p>
</li>
<li id="q-259-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Capacity Management 非零 ELID 不對應既有物件、Delete 指定 0 或不存在物件，須 Invalid Field；FID18h 指定不存在 Group 也須 Invalid Field。</p>
</li>
<li id="q-259-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-259-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>容量配置本身不保證一個通用完成 AER；若刪除 Set／Group 連帶刪除 namespaces，須依明定的 namespace 清單與通知規則更新受影響 controller。 <a class="qa-rule-link" href="#common-capacity_op-9">本冊完整規則</a></p>
</li>
<li id="q-259-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>配置完成後核對 Group／Set／Namespace 清單與對應層級的容量欄位。 <a class="qa-rule-link" href="#common-capacity_op-10">本冊完整規則</a></p>
</li>
<li id="q-259-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Capacity Management 本身沒有一個通用的專用 PEL 完成事件。 <a class="qa-rule-link" href="#common-capacity_op-11">本冊完整規則</a></p>
</li>
<li id="q-259-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>已完成的 Group、Set 與 namespace 配置不是普通 CLR 的暫存 queue，不能因 controller 重設就當作刪除。 <a class="qa-rule-link" href="#common-capacity_op-12">本冊完整規則</a></p>
</li>
<li id="q-259-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 與 Restore Default Capacity Configuration 是不同操作。 <a class="qa-rule-link" href="#common-capacity_op-13">本冊完整規則</a></p>
</li>
<li id="q-259-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>已完成的容量配置跨 Power Cycle 保留。 <a class="qa-rule-link" href="#common-capacity_op-14">本冊完整規則</a></p>
</li>
<li id="q-259-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>刪除 Endurance Group 會連帶刪除所含 NVM Sets 與 namespaces；刪 Set 也會刪其 namespaces，影響所有附加路徑。 <a class="qa-rule-link" href="#common-capacity_op-15">本冊完整規則</a></p>
</li>
<li id="q-259-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>沒有 Group 支援時，Base 對命令中 ENDGID 有忽略規則；必須先分清未支援功能與已支援但 ID 非法。</p>
</li>
<li id="q-259-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查該命令對 0 的明確定義，不能套一個全域「0 永遠非法」規則。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-260" data-question="260"><h2><a class="qa-qid" href="#q-260">Q260</a> Endurance Group Information Log 提供哪些健康與容量資訊？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-260-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-260-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這份 Log 將健康與工作量縮小到一個 Group，適合比較不同資源池，而不只看整顆 SSD 的 SMART。</p>
</li>
<li id="q-260-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>LID09h 以 LSI.ENDGID 選目標，資料涵蓋該 Group 的生命週期。</p>
</li>
<li id="q-260-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>確認 Group 支援及存在，再讀 512-byte Log。</p>
</li>
<li id="q-260-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>EGCW、AVSP、AVSPT、PUSED 描述健康；DUR、DUW、MUW 描述讀寫量；HRC、HWC、MDIE、NEILE 描述計數；TEGCAP、UEGCAP 為容量 bytes。</p>
</li>
<li id="q-260-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先讀健康狀態，再用前後快照比較工作量。此處 DUR／DUW／MUW 用 10^9 bytes 向上取整，不能套 SMART 的 512000-byte 單位。</p>
</li>
<li id="q-260-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>MUW 包含內部資料搬移，DUW 不含，因此可用來分析額外媒體寫入；仍要考慮取整與 0 代表未回報。</p>
</li>
<li id="q-260-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>沒有回報值不等於真實消耗為 0；不能對分母為 0 或未回報的 DUW 計算有效 write amplification。</p>
</li>
<li id="q-260-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-260-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>容量配置本身不保證一個通用完成 AER；若刪除 Set／Group 連帶刪除 namespaces，須依明定的 namespace 清單與通知規則更新受影響 controller。 <a class="qa-rule-link" href="#common-capacity_op-9">本冊完整規則</a></p>
</li>
<li id="q-260-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>配置完成後核對 Group／Set／Namespace 清單與對應層級的容量欄位。 <a class="qa-rule-link" href="#common-capacity_op-10">本冊完整規則</a></p>
</li>
<li id="q-260-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Capacity Management 本身沒有一個通用的專用 PEL 完成事件。 <a class="qa-rule-link" href="#common-capacity_op-11">本冊完整規則</a></p>
</li>
<li id="q-260-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Group 的累計健康資訊不因查詢 controller 的 CLR 就重新開始；目前警告則需在恢復後依實際狀態判讀。未完成的 Log 查詢要重新送出。</p>
</li>
<li id="q-260-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 不等於刪除 Endurance Group。恢復後讀同一 ENDGID，分開比較累計值、目前狀態及已確認的事件。</p>
</li>
<li id="q-260-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>未被刪除的 Group 保留其生命週期資訊；Power Cycle 後重新讀取。FID18h 與 AEC 的設定恢復另依 Feature 規則，不由 Log 保留性推論。</p>
</li>
<li id="q-260-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>健康資料以 Group 為範圍；多個 controllers 可能查看同一資料。RAE 確認也會影響後續事件觀察，需保存讀取者與時間。</p>
</li>
<li id="q-260-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Group Log 與 namespace membership、SMART 的整體警告需一致，但不能要求各欄逐 byte 相同。</p>
</li>
<li id="q-260-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是不是把兩種 Log 名稱相同的 Data Units 用錯單位。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-261" data-question="261"><h2><a class="qa-qid" href="#q-261">Q261</a> Endurance Group 的警告、Spare 與壽命事件如何更新？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-261-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-261-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Group 健康值、待確認事件清單與 Host AER 通知各負責不同階段，要分開設定和確認。</p>
</li>
<li id="q-261-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>FID18h 逐 Group 設定，AEC 則控制 aggregate log change 通知。</p>
</li>
<li id="q-261-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 EGCW、AVSP／AVSPT／PUSED、FID18h.EGCW 與 AEC 的相關 notice bit。</p>
</li>
<li id="q-261-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>EGCW bit0 低 spare、bit2 可靠性降低、bit3 Group 唯讀；namespace Write Protection 不得造成 EGRO。bit1 保留，不能照抄 SMART 溫度 bit。</p>
</li>
<li id="q-261-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>啟用 Group 事件後，有待處理條件就列入 LID0Fh；Host 讀 0Fh 找 ID，再讀各 Group 的 09h。09h 成功 RAE=0 才清該 Group 事件並移除其 entry。</p>
</li>
<li id="q-261-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>讀 0Fh 確認通知不等於逐 Group 事件全部清除；事件目前已消退時，09h 的 EGCW 也可能已為 0。</p>
</li>
<li id="q-261-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>FID18h 設保留警告 bit 或不存在 Group 須 Invalid Field。</p>
</li>
<li id="q-261-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-261-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Group 事件新增至 aggregate log 後，依 AEC 與 AER 條件通知；FID18h 管哪種 Group 警告加入清單，AEC 管清單變更是否通知 Host。</p>
</li>
<li id="q-261-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>LID0Fh 回待確認的 Group IDs；LID09h 回指定 Group 的目前健康。成功讀 09h 且 RAE=0，才清除該 Group 的待處理事件。</p>
</li>
<li id="q-261-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Capacity Management 本身沒有一個通用的專用 PEL 完成事件。 <a class="qa-rule-link" href="#common-capacity_op-11">本冊完整規則</a></p>
</li>
<li id="q-261-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Group 的累計健康資訊不因查詢 controller 的 CLR 就重新開始；目前警告則需在恢復後依實際狀態判讀。未完成的 Log 查詢要重新送出。</p>
</li>
<li id="q-261-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 不等於刪除 Endurance Group。恢復後讀同一 ENDGID，分開比較累計值、目前狀態及已確認的事件。</p>
</li>
<li id="q-261-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>未被刪除的 Group 保留其生命週期資訊；Power Cycle 後重新讀取。FID18h 與 AEC 的設定恢復另依 Feature 規則，不由 Log 保留性推論。</p>
</li>
<li id="q-261-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>健康資料以 Group 為範圍；多個 controllers 可能查看同一資料。RAE 確認也會影響後續事件觀察，需保存讀取者與時間。</p>
</li>
<li id="q-261-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>只有全部 Groups 都設相應 warning bit，才依規範要求在整體 SMART 設對應 bit；單一 Group 警告不可直接當成全部媒體唯讀。</p>
</li>
<li id="q-261-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否只確認 0Fh 就以為 09h 的 Group 事件也已清除。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-262" data-question="262"><h2><a class="qa-qid" href="#q-262">Q262</a> 如何確認總容量與未配置容量？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-262-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-262-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>未配置容量必須先問「還沒分給哪一層」，否則容易把已分給 Group 但尚未建立 namespace 的空間算錯。</p>
</li>
<li id="q-262-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>可能分別是 subsystem、domain、Group 或 Set 的容量池。</p>
</li>
<li id="q-262-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 TNVMCAP／UNVMCAP、Domain Attributes、TEGCAP／UEGCAP，以及 Set 的 Total／Unallocated Capacity。</p>
</li>
<li id="q-262-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>這些實體容量欄位使用 bytes；namespace NSZE／NCAP 使用目前 LBA 格式的 blocks，不能直接把原始數字相減。</p>
</li>
<li id="q-262-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>依將執行的管理操作選 Figure89 指定的容量來源，再計入配置粒度與 Capacity Adjustment Factor。</p>
</li>
<li id="q-262-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例如 Create Set 從既有 Group 的 UEGCAP 分配，成功不要求 subsystem UNVMCAP 再減一次。</p>
</li>
<li id="q-262-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>零值有時表示未回報，需讀該欄定義與支援條件；不能一律當作沒有容量。</p>
</li>
<li id="q-262-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-262-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>容量配置本身不保證一個通用完成 AER；若刪除 Set／Group 連帶刪除 namespaces，須依明定的 namespace 清單與通知規則更新受影響 controller。 <a class="qa-rule-link" href="#common-capacity_op-9">本冊完整規則</a></p>
</li>
<li id="q-262-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>配置完成後核對 Group／Set／Namespace 清單與對應層級的容量欄位。 <a class="qa-rule-link" href="#common-capacity_op-10">本冊完整規則</a></p>
</li>
<li id="q-262-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Capacity Management 本身沒有一個通用的專用 PEL 完成事件。 <a class="qa-rule-link" href="#common-capacity_op-11">本冊完整規則</a></p>
</li>
<li id="q-262-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>已完成的 Group、Set 與 namespace 配置不是普通 CLR 的暫存 queue，不能因 controller 重設就當作刪除。 <a class="qa-rule-link" href="#common-capacity_op-12">本冊完整規則</a></p>
</li>
<li id="q-262-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 與 Restore Default Capacity Configuration 是不同操作。 <a class="qa-rule-link" href="#common-capacity_op-13">本冊完整規則</a></p>
</li>
<li id="q-262-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>已完成的容量配置跨 Power Cycle 保留。 <a class="qa-rule-link" href="#common-capacity_op-14">本冊完整規則</a></p>
</li>
<li id="q-262-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>刪除 Endurance Group 會連帶刪除所含 NVM Sets 與 namespaces；刪 Set 也會刪其 namespaces，影響所有附加路徑。 <a class="qa-rule-link" href="#common-capacity_op-15">本冊完整規則</a></p>
</li>
<li id="q-262-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>以同一層級的前後數值驗證，避免把不同配置階段相加造成雙重計算。</p>
</li>
<li id="q-262-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先明確說出這次要建立的是 Group、Set 還是 namespace。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-263" data-question="263"><h2><a class="qa-qid" href="#q-263">Q263</a> Namespace 建立與刪除如何改變未配置容量？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-263-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-263-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Namespace 使用所屬容量池，並非每次都直接改變 Identify Controller.UNVMCAP。</p>
</li>
<li id="q-263-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>有 Set 用 Set 容量；無 Set 但有 Group 用 Group；更簡單配置則使用對應 domain／subsystem 容量。</p>
</li>
<li id="q-263-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>保存 namespace 所屬 ID、LBA 格式、實際 NVMCAP 與該池前後容量。</p>
</li>
<li id="q-263-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>NSZE 描述邏輯大小，NCAP 描述可配置邏輯 blocks；實體消耗還有配置粒度，不必精確等於 NSZE×LBA bytes。</p>
</li>
<li id="q-263-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>成功 Create 後查新 namespace 與池餘額；Delete 完成後查清單移除與可重新使用的容量。</p>
</li>
<li id="q-263-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>容量應依該層級與規則釋出／扣除；Detach 只移除路徑，不能當成 Delete 來預期容量歸還。</p>
</li>
<li id="q-263-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>容量不足與 NSID 數量耗盡是不同錯誤，不能只看到 Create 失敗就判定 bytes 不足。</p>
</li>
<li id="q-263-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-263-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>容量配置本身不保證一個通用完成 AER；若刪除 Set／Group 連帶刪除 namespaces，須依明定的 namespace 清單與通知規則更新受影響 controller。 <a class="qa-rule-link" href="#common-capacity_op-9">本冊完整規則</a></p>
</li>
<li id="q-263-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>配置完成後核對 Group／Set／Namespace 清單與對應層級的容量欄位。 <a class="qa-rule-link" href="#common-capacity_op-10">本冊完整規則</a></p>
</li>
<li id="q-263-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Capacity Management 本身沒有一個通用的專用 PEL 完成事件。 <a class="qa-rule-link" href="#common-capacity_op-11">本冊完整規則</a></p>
</li>
<li id="q-263-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>已完成的 Group、Set 與 namespace 配置不是普通 CLR 的暫存 queue，不能因 controller 重設就當作刪除。 <a class="qa-rule-link" href="#common-capacity_op-12">本冊完整規則</a></p>
</li>
<li id="q-263-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 與 Restore Default Capacity Configuration 是不同操作。 <a class="qa-rule-link" href="#common-capacity_op-13">本冊完整規則</a></p>
</li>
<li id="q-263-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>已完成的容量配置跨 Power Cycle 保留。 <a class="qa-rule-link" href="#common-capacity_op-14">本冊完整規則</a></p>
</li>
<li id="q-263-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>刪除 Endurance Group 會連帶刪除所含 NVM Sets 與 namespaces；刪 Set 也會刪其 namespaces，影響所有附加路徑。 <a class="qa-rule-link" href="#common-capacity_op-15">本冊完整規則</a></p>
</li>
<li id="q-263-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>把有效資料內容、namespace 存在與容量帳目分開驗證，刪 namespace 也不等於已做資料抹除。</p>
</li>
<li id="q-263-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否看錯層級的 Unallocated 欄位，或把 Detach 當成容量釋放。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-264" data-question="264"><h2><a class="qa-qid" href="#q-264">Q264</a> Capacity Management 如何配置或釋放 Group 與 Set？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-264-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-264-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Fixed 模式選既有配置，Variable 模式指定新物件容量，兩者不是同一組操作流程。</p>
</li>
<li id="q-264-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Group／Set 變更可連帶影響包含的 namespaces 與所有存取路徑。</p>
</li>
<li id="q-264-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 CTRATT 的 Fixed／Variable 與 Delete 支援；Fixed 再讀 Supported Capacity Configuration List。</p>
</li>
<li id="q-264-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>OPER0 選配置，1／2 建立／刪 Group，3／4 建立／刪 Set，5 恢復預設。ELID 意義隨 OPER 變，CAPU:CAPL 為建立容量 bytes。</p>
</li>
<li id="q-264-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>Variable 通常先 Group 再 Set 再 namespace；Fixed 改到另一配置前須依條件清除原配置，不能任意覆蓋正在使用的配置。</p>
</li>
<li id="q-264-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Create 成功 CQE.DW0.CELID 回建立的 ID；其他操作不能把同一欄當作永遠有效的物件 ID。</p>
</li>
<li id="q-264-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>刪 Group／Set 會連帶刪子物件；恢復預設前仍有 Group／Set 時須 Command Sequence Error。</p>
</li>
<li id="q-264-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-264-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>容量配置本身不保證一個通用完成 AER；若刪除 Set／Group 連帶刪除 namespaces，須依明定的 namespace 清單與通知規則更新受影響 controller。 <a class="qa-rule-link" href="#common-capacity_op-9">本冊完整規則</a></p>
</li>
<li id="q-264-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>配置完成後核對 Group／Set／Namespace 清單與對應層級的容量欄位。 <a class="qa-rule-link" href="#common-capacity_op-10">本冊完整規則</a></p>
</li>
<li id="q-264-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Capacity Management 本身沒有一個通用的專用 PEL 完成事件。 <a class="qa-rule-link" href="#common-capacity_op-11">本冊完整規則</a></p>
</li>
<li id="q-264-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>已完成的 Group、Set 與 namespace 配置不是普通 CLR 的暫存 queue，不能因 controller 重設就當作刪除。 <a class="qa-rule-link" href="#common-capacity_op-12">本冊完整規則</a></p>
</li>
<li id="q-264-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 與 Restore Default Capacity Configuration 是不同操作。 <a class="qa-rule-link" href="#common-capacity_op-13">本冊完整規則</a></p>
</li>
<li id="q-264-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>已完成的容量配置跨 Power Cycle 保留。 <a class="qa-rule-link" href="#common-capacity_op-14">本冊完整規則</a></p>
</li>
<li id="q-264-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>刪除 Endurance Group 會連帶刪除所含 NVM Sets 與 namespaces；刪 Set 也會刪其 namespaces，影響所有附加路徑。 <a class="qa-rule-link" href="#common-capacity_op-15">本冊完整規則</a></p>
</li>
<li id="q-264-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>完成後重新讀清單、歸屬與容量；操作過程中的中間觀察可能 indeterminate，不宜拿單一中間快照作最終結果。</p>
</li>
<li id="q-264-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認 OPER 選的是預期模式與動作，尤其 ELID=0 在各動作的不同意義。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-265" data-question="265"><h2><a class="qa-qid" href="#q-265">Q265</a> 要求容量或物件數超過可用資源時應回什麼？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-265-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-265-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>容量 bytes 不夠與沒有可用 ID 是不同限制，題目應先固定是哪一種。</p>
</li>
<li id="q-265-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Create Group 核對 domain／subsystem 可配置量與最大 Group 大小；Create Set 核對 Group 的 UEGCAP。</p>
</li>
<li id="q-265-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 MEGCAP、UNVMCAP、domain 容量、UEGCAP 與目前 ID 清單。</p>
</li>
<li id="q-265-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>容量請求使用 CAPU:CAPL bytes，並考慮調整因子與實作配置粒度後所需資源。</p>
</li>
<li id="q-265-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先做只超容量但 ID 尚可用的案例，再做容量足夠但 ID 耗盡的案例，以隔離不同限制。</p>
</li>
<li id="q-265-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>資源足夠時建立成功且回 CELID；不足時不應假裝建立了不存在的物件。</p>
</li>
<li id="q-265-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>容量不足回命令特定 Insufficient Capacity（1/26h）；無可用 ID 回 Identifier Unavailable（1/2Dh）。</p>
</li>
<li id="q-265-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-265-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>容量配置本身不保證一個通用完成 AER；若刪除 Set／Group 連帶刪除 namespaces，須依明定的 namespace 清單與通知規則更新受影響 controller。 <a class="qa-rule-link" href="#common-capacity_op-9">本冊完整規則</a></p>
</li>
<li id="q-265-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>容量不足的 Create Group／Set 在支援 Error Log 時，必須記錄明定的 CSINFO 補充容量資訊；其數字語意在正文與 Figure165 有差異，應一併記錄來源。</p>
</li>
<li id="q-265-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Capacity Management 本身沒有一個通用的專用 PEL 完成事件。 <a class="qa-rule-link" href="#common-capacity_op-11">本冊完整規則</a></p>
</li>
<li id="q-265-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>已完成的 Group、Set 與 namespace 配置不是普通 CLR 的暫存 queue，不能因 controller 重設就當作刪除。 <a class="qa-rule-link" href="#common-capacity_op-12">本冊完整規則</a></p>
</li>
<li id="q-265-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 與 Restore Default Capacity Configuration 是不同操作。 <a class="qa-rule-link" href="#common-capacity_op-13">本冊完整規則</a></p>
</li>
<li id="q-265-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>已完成的容量配置跨 Power Cycle 保留。 <a class="qa-rule-link" href="#common-capacity_op-14">本冊完整規則</a></p>
</li>
<li id="q-265-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>刪除 Endurance Group 會連帶刪除所含 NVM Sets 與 namespaces；刪 Set 也會刪其 namespaces，影響所有附加路徑。 <a class="qa-rule-link" href="#common-capacity_op-15">本冊完整規則</a></p>
</li>
<li id="q-265-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>正文要求 Error.CSINFO 回可建立的最大容量；Figure165 卻寫所需容量，兩處不一致。教材保留這項來源差異，不以其中一個數字直接替韌體判定合規。</p>
</li>
<li id="q-265-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認失敗的限制種類；涉及 CSINFO 語意時再核對這項規格內部差異。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-266" data-question="266"><h2><a class="qa-qid" href="#q-266">Q266</a> 容量配置完成後，哪些 Identify 與 Log 應更新？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-266-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-266-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>單一成功 CQE 不足以驗證配置；所有描述同一物件的查詢都應形成一致結果。</p>
</li>
<li id="q-266-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>依變更層級檢查 Group、Set、namespace、domain 及 Media Unit 歸屬。</p>
</li>
<li id="q-266-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>保存前後 Identify Lists、容量欄位、Group Log 與受支援的 Media Unit Status。</p>
</li>
<li id="q-266-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Create Group 更新 Group List 與上層容量；Create Set 更新 Set List 與 UEGCAP，卻不改 UNVMCAP；刪除則依序移除子物件與回收該層容量。</p>
</li>
<li id="q-266-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先等管理命令完成，再重讀受影響物件；若仍有其他 Host 同時改配置，需記錄時序才能比較。</p>
</li>
<li id="q-266-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例如刪 Set 後，其 namespaces 從 allocated list 移除，Media Unit 的 NVMSETID 清零，Group 可用容量增加。</p>
</li>
<li id="q-266-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>操作中間的清單先後更新有明定順序，不能一律要求每個 byte 對所有讀者瞬間原子變更。</p>
</li>
<li id="q-266-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-266-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>容量配置本身不保證一個通用完成 AER；若刪除 Set／Group 連帶刪除 namespaces，須依明定的 namespace 清單與通知規則更新受影響 controller。 <a class="qa-rule-link" href="#common-capacity_op-9">本冊完整規則</a></p>
</li>
<li id="q-266-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>配置完成後核對 Group／Set／Namespace 清單與對應層級的容量欄位。 <a class="qa-rule-link" href="#common-capacity_op-10">本冊完整規則</a></p>
</li>
<li id="q-266-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Capacity Management 本身沒有一個通用的專用 PEL 完成事件。 <a class="qa-rule-link" href="#common-capacity_op-11">本冊完整規則</a></p>
</li>
<li id="q-266-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>已完成的 Group、Set 與 namespace 配置不是普通 CLR 的暫存 queue，不能因 controller 重設就當作刪除。 <a class="qa-rule-link" href="#common-capacity_op-12">本冊完整規則</a></p>
</li>
<li id="q-266-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 與 Restore Default Capacity Configuration 是不同操作。 <a class="qa-rule-link" href="#common-capacity_op-13">本冊完整規則</a></p>
</li>
<li id="q-266-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>已完成的容量配置跨 Power Cycle 保留。 <a class="qa-rule-link" href="#common-capacity_op-14">本冊完整規則</a></p>
</li>
<li id="q-266-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>刪除 Endurance Group 會連帶刪除所含 NVM Sets 與 namespaces；刪 Set 也會刪其 namespaces，影響所有附加路徑。 <a class="qa-rule-link" href="#common-capacity_op-15">本冊完整規則</a></p>
</li>
<li id="q-266-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>用完整變更鏈確認：物件消失、子物件消失、容量回到正確父層、通知讓其他讀者重查。</p>
</li>
<li id="q-266-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查觀察是在完成前還是完成後，以及是否有人同時進行第二次配置。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-267" data-question="267"><h2><a class="qa-qid" href="#q-267">Q267</a> Reset 與 Power Cycle 後 Group、Set 與容量配置如何保留？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-267-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-267-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>容量配置代表儲存組織，與需要重建的 I/O queues 不同，重設不能被當成清空配置命令。</p>
</li>
<li id="q-267-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>已完成的 Group、Set、namespace 歸屬與容量帳目是比對對象。</p>
</li>
<li id="q-267-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>保存配置清單、識別資訊、容量及是否有待完成管理操作。</p>
</li>
<li id="q-267-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Restore Default Capacity Configuration 是另外的 OPER5，並有清空現有物件的先決條件；普通 Reset 不等於這項命令。</p>
</li>
<li id="q-267-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>恢復命令通道後重新探索，再確認物件與歸屬；對失電時未完成的操作，不假定成功、失敗或 rollback。</p>
</li>
<li id="q-267-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>已完成配置應能對回原物件，容量差異則需由其他合法管理變更或可說明的狀態解釋。</p>
</li>
<li id="q-267-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>未收到 CQE 只表示 Host 不知道結果，不表示原配置必定完整未改。</p>
</li>
<li id="q-267-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-267-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>容量配置本身不保證一個通用完成 AER；若刪除 Set／Group 連帶刪除 namespaces，須依明定的 namespace 清單與通知規則更新受影響 controller。 <a class="qa-rule-link" href="#common-capacity_op-9">本冊完整規則</a></p>
</li>
<li id="q-267-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>配置完成後核對 Group／Set／Namespace 清單與對應層級的容量欄位。 <a class="qa-rule-link" href="#common-capacity_op-10">本冊完整規則</a></p>
</li>
<li id="q-267-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Capacity Management 本身沒有一個通用的專用 PEL 完成事件。 <a class="qa-rule-link" href="#common-capacity_op-11">本冊完整規則</a></p>
</li>
<li id="q-267-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>已完成的 Group、Set 與 namespace 配置不是普通 CLR 的暫存 queue，不能因 controller 重設就當作刪除。 <a class="qa-rule-link" href="#common-capacity_op-12">本冊完整規則</a></p>
</li>
<li id="q-267-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 與 Restore Default Capacity Configuration 是不同操作。 <a class="qa-rule-link" href="#common-capacity_op-13">本冊完整規則</a></p>
</li>
<li id="q-267-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>已完成的容量配置跨 Power Cycle 保留。 <a class="qa-rule-link" href="#common-capacity_op-14">本冊完整規則</a></p>
</li>
<li id="q-267-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>刪除 Endurance Group 會連帶刪除所含 NVM Sets 與 namespaces；刪 Set 也會刪其 namespaces，影響所有附加路徑。 <a class="qa-rule-link" href="#common-capacity_op-15">本冊完整規則</a></p>
</li>
<li id="q-267-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>先區分「重設造成暫時不可查」與「配置已真正消失」，前者不能直接判成持久性失敗。</p>
</li>
<li id="q-267-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先查這段期間是否還執行了 Restore、Delete 或其他容量管理操作。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-capacitymodel">Base 2.4 §3.2.2–3.2.3, 3.8</a> · <a href="#ref-capacitycmd">Base 2.4 §5.2.3</a> · <a href="#ref-capacityop">Base 2.4 §8.1.4</a> · <a href="#ref-eghealth">Base 2.4 §5.2.13.1.10</a> · <a href="#ref-egevents">Base 2.4 §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nvmcreate">NVM Command Set 1.3 §4.1.5.8, 4.1.6, 5.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-capacity_op-9"><h3>本主題的共用條件 · 是否產生 Asynchronous Event？</h3><p>容量配置本身不保證一個通用完成 AER；若刪除 Set／Group 連帶刪除 namespaces，須依明定的 namespace 清單與通知規則更新受影響 controller。健康事件則另由 FID18h 與 AEC 控制。</p></article>
<article id="common-capacity_op-10"><h3>本主題的共用條件 · 是否更新 Error Information Log 或其他 Log？</h3><p>配置完成後核對 Group／Set／Namespace 清單與對應層級的容量欄位。Media Unit Status 受支援時，也應反映歸屬。容量不足的 Create 有明定 Error Information 補充資料要求，不能只保留 CQE。</p></article>
<article id="common-capacity_op-11"><h3>本主題的共用條件 · 是否記錄於 Persistent Event Log？</h3><p>Capacity Management 本身沒有一個通用的專用 PEL 完成事件。若操作另外符合支援的 namespace、硬體警告等事件條件，依那些條件記錄，不按建立／刪除每個物件自行編造事件。</p></article>
<article id="common-capacity_op-12"><h3>本主題的共用條件 · Controller Reset 後是否保留或繼續？</h3><p>已完成的 Group、Set 與 namespace 配置不是普通 CLR 的暫存 queue，不能因 controller 重設就當作刪除。未完成管理操作則重查實際清單與容量，不能假設自動 rollback。</p></article>
<article id="common-capacity_op-13"><h3>本主題的共用條件 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>Subsystem Reset 與 Restore Default Capacity Configuration 是不同操作。重設後保留已完成的儲存配置並重新探索；只有另行執行配置操作，才依該操作的要求變更物件。</p></article>
<article id="common-capacity_op-14"><h3>本主題的共用條件 · Power Cycle 後是否保留或繼續？</h3><p>已完成的容量配置跨 Power Cycle 保留。若失電打斷配置，恢復後用可讀的清單、容量及事件判斷，不能將未收到 CQE 直接視為未修改。</p></article>
<article id="common-capacity_op-15"><h3>本主題的共用條件 · 是否影響其他 Controller 或 Namespace？</h3><p>刪除 Endurance Group 會連帶刪除所含 NVM Sets 與 namespaces；刪 Set 也會刪其 namespaces，影響所有附加路徑。單一 namespace 的容量配置則應在它所在的資源層級核算。</p></article>
<article id="common-command-8"><h3>命令完成、事件與紀錄 · DNR 與 More 應如何設定？</h3><p>只有收到 CQE，才有 DNR 與 More 可供判讀。DNR=1 表示相同命令即使重送到此 NVM subsystem 的任一 controller，仍預期會失敗；DNR=0 則只表示可能成功。除非個別錯誤條件另有明定，不能只看 Status 名稱就要求 DNR=1。More=1 表示 Error Information Log 有這筆命令的補充資訊。SCT=SC=0 時，DNR 應為 0。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-capacitymodel"><strong>Base 2.4 · §3.2.2–3.2.3, 3.8</strong><br>文件頁 80–84, 125–129 · PDF 106–110, 151–155 · Figure 67–69, 86–89</li>
<li id="ref-egevents"><strong>Base 2.4 · §3.2.3.1, 5.2.13.1.15, 5.2.30.1.17</strong><br>文件頁 84, 270, 478 · PDF 110, 296, 504 · Figure 261, 493</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-capacitycmd"><strong>Base 2.4 · §5.2.3</strong><br>文件頁 191–195 · PDF 217–221 · Figure 162–166</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-eghealth"><strong>Base 2.4 · §5.2.13.1.10</strong><br>文件頁 237–239 · PDF 263–265 · Figure 224–225</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>文件頁 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-idlist"><strong>Base 2.4 · §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</strong><br>文件頁 387–399, 402–404 · PDF 413–425, 428–430 · Figure 342–355, 360–362</li>
<li id="ref-capacityop"><strong>Base 2.4 · §8.1.4</strong><br>文件頁 594–597 · PDF 620–623</li>
<li id="ref-nvmcreate"><strong>NVM Command Set 1.3 · §4.1.5.8, 4.1.6, 5.8</strong><br>文件頁 108, 110–113, 162–163 · PDF 108, 110–113, 162–163 · Figure 132–134</li>
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
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/capacity/en/">English</a><a href="/DOCS/nvme-question-bank/capacity.html">繁中教學 HTML</a></nav>
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
