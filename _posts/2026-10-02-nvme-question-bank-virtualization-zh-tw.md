---
layout: post
title: "NVMe 自問自答題庫：Multi-Controller 與 Virtualization"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/virtualization/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/virtualization/en/">English</a><a href="/DOCS/nvme-question-bank/virtualization.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q246–Q255</p><h1>Multi-Controller 與 Virtualization</h1><p class="qr-intro">多路徑、shared namespace 與虛擬化是不同關係。本冊先畫 controller 拓樸，再加入 attachment、ANA 及可分配 queue／interrupt 資源。</p><p>先練習，再展開每題的 17 項解答。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>同一張拓樸上有三種狀態</h2><p class="qa-takeaway">Online、Enabled 與 namespace 可存取不是同一件事。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">狀態</th><th scope="col">查詢</th><th scope="col">用途</th></tr></thead><tbody><tr><td>管理角色</td><td>Primary Capabilities、Secondary List</td><td>誰可管理誰的資源</td></tr><tr><td>可啟用性</td><td>Secondary state、VQ／VI</td><td>是否具備 Online 前提</td></tr><tr><td>命令介面</td><td>CC、CSTS</td><td>controller 是否已啟用</td></tr><tr><td>namespace 路徑</td><td>Active List、ANA</td><td>目前可否經此路徑存取</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>Secondary Online 之後仍需 Host 初始化並 Enable；把 Online 直接當 RDY=1，會跳過必要步驟。</p>
<p class="qa-citations">來源：<a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-analog">Base 2.4 §5.2.13.1.13</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-246">Q246 · Subsystem、Primary 與 Secondary Controller 是什麼關係？</a></li>
<li><a href="#q-247">Q247 · Private 與 Shared Namespace 如何 Attach 到 Controller？</a></li>
<li><a href="#q-248">Q248 · 如何取得 Namespace 對應的 Controller List？</a></li>
<li><a href="#q-249">Q249 · 一台 Controller Reset 時，其他路徑能否繼續存取 Shared Namespace？</a></li>
<li><a href="#q-250">Q250 · NVM Subsystem Reset 會影響哪些 Controller？</a></li>
<li><a href="#q-251">Q251 · Namespace 變更如何通知其他 Controller？</a></li>
<li><a href="#q-252">Q252 · Asymmetric Controller Behavior 與 ANA 如何協助選路徑？</a></li>
<li><a href="#q-253">Q253 · Secondary Controller 如何 Online 或 Offline？</a></li>
<li><a href="#q-254">Q254 · Virtualization Management 如何分配與釋放資源？</a></li>
<li><a href="#q-255">Q255 · Reset 與 Power Cycle 後 Virtualization 資源如何恢復？</a></li>
</ol></section>
<article class="qa-question" id="q-246" data-question="246"><h2><a class="qa-qid" href="#q-246">Q246</a> Subsystem、Primary 與 Secondary Controller 是什麼關係？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-246-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-246-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Controller 是命令入口，namespace 是儲存物件；虛擬化把部分 queue 與 interrupt 資源交由 primary 管理分配。</p>
</li>
<li id="q-246-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>一個 subsystem 可有多個 primary，各有 secondary 群組；secondary 與其 primary 必須在同一 domain。</p>
</li>
<li id="q-246-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 OACS.VMS、Primary Controller Capabilities 與 Secondary Controller List，不憑 PCI function 編號猜 parent。</p>
</li>
<li id="q-246-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>VQ 管一組 SQ／CQ，VI 管一個 interrupt vector；Private Resources 固定歸屬，Flexible Resources 可受管理重新分配。</p>
</li>
<li id="q-246-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先畫出 primary→secondary 關係，再標每個 controller 的可用資源與 attached namespaces，最後才規劃 queues。</p>
</li>
<li id="q-246-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>每個 Online 且啟用的 secondary 仍是完整 NVMe controller，Host 可用正常 NVMe 命令操作。</p>
</li>
<li id="q-246-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援 Virtualization Management 的 controller 不能被要求接受資源管理命令；管理命令需送到對應 primary。</p>
</li>
<li id="q-246-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-246-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>資源配置與 Online／Offline 不定義統一成功 AER。 <a class="qa-rule-link" href="#common-virtual_op-9">本冊完整規則</a></p>
</li>
<li id="q-246-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>用 Primary Controller Capabilities、Secondary Controller List 及目前 queue／interrupt 能力確認配置；namespace 路徑則讀 Active List、Controller List 與適用 ANA Log。 <a class="qa-rule-link" href="#common-virtual_op-10">本冊完整規則</a></p>
</li>
<li id="q-246-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Virtualization Management 不是專用 PEL 事件。 <a class="qa-rule-link" href="#common-virtual_op-11">本冊完整規則</a></p>
</li>
<li id="q-246-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Primary 被 Disable、CLR 或 Shutdown 時，其 secondary 必須轉 Offline；Online 轉 Offline 會移除 Flexible Resources。 <a class="qa-rule-link" href="#common-virtual_op-12">本冊完整規則</a></p>
</li>
<li id="q-246-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 影響範圍內的 primary／secondary 操作環境須重建。 <a class="qa-rule-link" href="#common-virtual_op-13">本冊完整規則</a></p>
</li>
<li id="q-246-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Primary Flexible Allocation 跨 Power Cycle 保留；secondary 的 Online 狀態與資源需重新查詢及配置。 <a class="qa-rule-link" href="#common-virtual_op-14">本冊完整規則</a></p>
</li>
<li id="q-246-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Primary 管理自己的 secondary 群組及 Flexible Resource pool，同一份資源不能同時分給兩個 controller。 <a class="qa-rule-link" href="#common-virtual_op-15">本冊完整規則</a></p>
</li>
<li id="q-246-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>PCIe PF／VF 與 NVMe primary／secondary 在支援兩者時相對應，但不能把所有多 controller 裝置都假定有 SR-IOV。</p>
</li>
<li id="q-246-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認實際拓樸與能力，再討論哪一台可以配置哪一台。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-247" data-question="247"><h2><a class="qa-qid" href="#q-247">Q247</a> Private 與 Shared Namespace 如何 Attach 到 Controller？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-247-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-247-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Attach 建立存取路徑，不是複製 namespace 資料。Private／Shared 決定能否同時附加到多個 controller。</p>
</li>
<li id="q-247-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Private 同時只附加一台，Shared 可附加多台，但仍受命令集、資源與數量限制。</p>
</li>
<li id="q-247-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 namespace.NMIC、相關 controller 能力與已附加 Controller List。</p>
</li>
<li id="q-247-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Namespace Attachment 以 NSID 指目標，SEL 指 Attach／Detach，資料 buffer 列出 CNTLID。</p>
</li>
<li id="q-247-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先確認目標已配置與分享能力，再 Attach 所選 controller，讀各台 Active List 驗證。</p>
</li>
<li id="q-247-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Shared 的多個入口看到同一份資料；Private 已有一個入口時，不能再同時增加另一個。</p>
</li>
<li id="q-247-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Private 已附加其他 controller 時，可對應 Namespace Is Private；重複附加同一台則是 Namespace Already Attached。</p>
</li>
<li id="q-247-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-247-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Create／Delete 影響 Allocated List，Attach／Detach 影響指定 controller 的 Active List。 <a class="qa-rule-link" href="#common-namespace_op-9">本冊完整規則</a></p>
</li>
<li id="q-247-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>使用 Identify 的 Allocated、Active 與 Controller List 確認目前配置；Changed Attached Namespace List04h 與 Changed Allocated Namespace List1Ch 指出曾變更的 NSID，不能代替完整現況。 <a class="qa-rule-link" href="#common-namespace_op-10">本冊完整規則</a></p>
</li>
<li id="q-247-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 時，Namespace Management 對應的 Change Namespace Event06h 記錄建立／刪除等規定事件。 <a class="qa-rule-link" href="#common-namespace_op-11">本冊完整規則</a></p>
</li>
<li id="q-247-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>已完成的 namespace 配置與 Attach／Detach 跨 Reset 保留；重設的是命令通道，不是自動刪除 namespace。 <a class="qa-rule-link" href="#common-namespace_op-12">本冊完整規則</a></p>
</li>
<li id="q-247-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 不等於 Restore Default Namespace Configuration。 <a class="qa-rule-link" href="#common-namespace_op-13">本冊完整規則</a></p>
</li>
<li id="q-247-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後，已完成的 namespace 配置與附加關係仍需保留。 <a class="qa-rule-link" href="#common-namespace_op-14">本冊完整規則</a></p>
</li>
<li id="q-247-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>建立／刪除影響 subsystem 的 namespace inventory；附加清單指定哪些 controllers 改變存取關係。 <a class="qa-rule-link" href="#common-namespace_op-15">本冊完整規則</a></p>
</li>
<li id="q-247-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>用每台 Active List 與 namespace Controller List 雙向核對，避免只看一條路徑。</p>
</li>
<li id="q-247-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是「已存在」還是「已附加」，兩者不同。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-248" data-question="248"><h2><a class="qa-qid" href="#q-248">Q248</a> 如何取得 Namespace 對應的 Controller List？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-248-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-248-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這份清單回答 namespace 已附加在哪些 controller，與列出 subsystem 全部 controller 的清單不同。</p>
</li>
<li id="q-248-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>查詢以指定 namespace 為範圍；同一 subsystem 中未附加的 controller 不應被誤算為可用路徑。</p>
</li>
<li id="q-248-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>使用 Identify 的 Attached Controller List 選擇，核對 CNS、NSID 與起始 Controller Identifier。</p>
</li>
<li id="q-248-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>回覆有數量及 Controller Identifier entries；分段時遵守起始 ID 的包含規則，不套用 Active Namespace List 的不同條件。</p>
</li>
<li id="q-248-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>讀第一段，依最後 ID 推進下一次起點直到讀完，並留意期間 attachment 可能改變。</p>
</li>
<li id="q-248-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>取得當時 attached controllers，再逐台確認 Online、Ready 與 ANA，才知道哪條路徑現在能用。</p>
</li>
<li id="q-248-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>NSID 或 CNS 不合法依 Identify 規則回應；一份空清單不代表 namespace 一定已刪除。</p>
</li>
<li id="q-248-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-248-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>資源配置與 Online／Offline 不定義統一成功 AER。 <a class="qa-rule-link" href="#common-virtual_op-9">本冊完整規則</a></p>
</li>
<li id="q-248-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>用 Primary Controller Capabilities、Secondary Controller List 及目前 queue／interrupt 能力確認配置；namespace 路徑則讀 Active List、Controller List 與適用 ANA Log。 <a class="qa-rule-link" href="#common-virtual_op-10">本冊完整規則</a></p>
</li>
<li id="q-248-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Virtualization Management 不是專用 PEL 事件。 <a class="qa-rule-link" href="#common-virtual_op-11">本冊完整規則</a></p>
</li>
<li id="q-248-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>查詢若因重設中止，恢復後須重新送出。比較回覆時，再逐欄區分固定身分、配置與動態狀態。 <a class="qa-rule-link" href="#common-identify-12">本冊完整規則</a></p>
</li>
<li id="q-248-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>重設後重新查詢受影響的物件。重設本身不表示 namespace 已刪除，也不表示配置已恢復出廠值。 <a class="qa-rule-link" href="#common-identify-13">本冊完整規則</a></p>
</li>
<li id="q-248-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新查詢並比較。若期間還有韌體啟用或管理操作，必須分清楚差異是由哪個事件造成。 <a class="qa-rule-link" href="#common-identify-14">本冊完整規則</a></p>
</li>
<li id="q-248-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Identify 是唯讀查詢。不同 controller 的 Active List 可能不同，因此比較時必須確認查詢對象。 <a class="qa-rule-link" href="#common-identify-15">本冊完整規則</a></p>
</li>
<li id="q-248-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>與各台 Active Namespace List 交叉確認，必要時在管理操作完成後重讀，避免比較不同時點。</p>
</li>
<li id="q-248-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認使用的是 attached list，還是 subsystem controller inventory。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-249" data-question="249"><h2><a class="qa-qid" href="#q-249">Q249</a> 一台 Controller Reset 時，其他路徑能否繼續存取 Shared Namespace？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-249-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-249-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Shared namespace 提供多條路徑，但不能保證任何故障都完全不影響其他路徑。</p>
</li>
<li id="q-249-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>一般 CLR 針對一台；primary 重設可使其 secondary Offline，共用媒體或 domain 問題也可能擴大影響。</p>
</li>
<li id="q-249-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 parent 關係、domain、attachment、ANA 及其他路徑 Ready 狀態。</p>
</li>
<li id="q-249-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>其他 controller 的獨立 queues 可繼續有效；但資料命令是否可執行仍受 namespace Ready、ANA 與存取限制。</p>
</li>
<li id="q-249-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>停止失效路徑新提交，確認替代路徑可用，再處理原路徑未完成命令與新命令的相依性。</p>
</li>
<li id="q-249-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>在其他路徑與共享資源都正常時，可以繼續存取同一資料，不需要再建立一份 namespace。</p>
</li>
<li id="q-249-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不能因路徑切換成功，就假定舊路徑的 Write 全部未執行；重試可能與原操作效果重疊。</p>
</li>
<li id="q-249-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-249-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Create／Delete 影響 Allocated List，Attach／Detach 影響指定 controller 的 Active List。 <a class="qa-rule-link" href="#common-namespace_op-9">本冊完整規則</a></p>
</li>
<li id="q-249-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>使用 Identify 的 Allocated、Active 與 Controller List 確認目前配置；Changed Attached Namespace List04h 與 Changed Allocated Namespace List1Ch 指出曾變更的 NSID，不能代替完整現況。 <a class="qa-rule-link" href="#common-namespace_op-10">本冊完整規則</a></p>
</li>
<li id="q-249-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 時，Namespace Management 對應的 Change Namespace Event06h 記錄建立／刪除等規定事件。 <a class="qa-rule-link" href="#common-namespace_op-11">本冊完整規則</a></p>
</li>
<li id="q-249-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>已完成的 namespace 配置與 Attach／Detach 跨 Reset 保留；重設的是命令通道，不是自動刪除 namespace。 <a class="qa-rule-link" href="#common-namespace_op-12">本冊完整規則</a></p>
</li>
<li id="q-249-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 不等於 Restore Default Namespace Configuration。 <a class="qa-rule-link" href="#common-namespace_op-13">本冊完整規則</a></p>
</li>
<li id="q-249-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後，已完成的 namespace 配置與附加關係仍需保留。 <a class="qa-rule-link" href="#common-namespace_op-14">本冊完整規則</a></p>
</li>
<li id="q-249-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>建立／刪除影響 subsystem 的 namespace inventory；附加清單指定哪些 controllers 改變存取關係。 <a class="qa-rule-link" href="#common-namespace_op-15">本冊完整規則</a></p>
</li>
<li id="q-249-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>以控制關係與命令結果判斷影響，避免「一台 Reset 一定不影響其他台」的過度概括。</p>
</li>
<li id="q-249-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查被 Reset 的是否是替代路徑所依賴的 primary。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-250" data-question="250"><h2><a class="qa-qid" href="#q-250">Q250</a> NVM Subsystem Reset 會影響哪些 Controller？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-250-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-250-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Reset 名稱包含 subsystem，但多 domain 裝置仍可能只重設一個 domain，必須確認實作範圍。</p>
</li>
<li id="q-250-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>單 domain 涵蓋全部；multi-domain 依實作涵蓋發起所在 domain，或全部 domains。</p>
</li>
<li id="q-250-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 domain 拓樸、CAP.NSSRS 與重設後 CSTS.NSSRO。</p>
</li>
<li id="q-250-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>NSSR.NSSRC=4E564D65h 是受支援時的觸發方式；受影響範圍會 CLR 各 controller，並停用其 PMR。</p>
</li>
<li id="q-250-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先停止範圍內工作，觸發 Reset，逐台確認重新初始化與路徑恢復。</p>
</li>
<li id="q-250-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>受影響 queues 必須重建；範圍外 controller 是否可用仍由其自身與共享媒體狀態決定。</p>
</li>
<li id="q-250-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Register Reset 沒有一筆可指定 DNR／More 的 CQE；不能等待虛構的 Reset Command Completion。</p>
</li>
<li id="q-250-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>NSSR Register 寫入沒有 CQE，因此 DNR 與 More 不適用；恢復後查詢命令的 CQE 是另一筆命令的結果。</p>
</li>
<li id="q-250-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>資源配置與 Online／Offline 不定義統一成功 AER。 <a class="qa-rule-link" href="#common-virtual_op-9">本冊完整規則</a></p>
</li>
<li id="q-250-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>用 Primary Controller Capabilities、Secondary Controller List 及目前 queue／interrupt 能力確認配置；namespace 路徑則讀 Active List、Controller List 與適用 ANA Log。 <a class="qa-rule-link" href="#common-virtual_op-10">本冊完整規則</a></p>
</li>
<li id="q-250-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Virtualization Management 不是專用 PEL 事件。 <a class="qa-rule-link" href="#common-virtual_op-11">本冊完整規則</a></p>
</li>
<li id="q-250-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Primary 被 Disable、CLR 或 Shutdown 時，其 secondary 必須轉 Offline；Online 轉 Offline 會移除 Flexible Resources。 <a class="qa-rule-link" href="#common-virtual_op-12">本冊完整規則</a></p>
</li>
<li id="q-250-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 影響範圍內的 primary／secondary 操作環境須重建。 <a class="qa-rule-link" href="#common-virtual_op-13">本冊完整規則</a></p>
</li>
<li id="q-250-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Primary Flexible Allocation 跨 Power Cycle 保留；secondary 的 Online 狀態與資源需重新查詢及配置。 <a class="qa-rule-link" href="#common-virtual_op-14">本冊完整規則</a></p>
</li>
<li id="q-250-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Primary 管理自己的 secondary 群組及 Flexible Resource pool，同一份資源不能同時分給兩個 controller。 <a class="qa-rule-link" href="#common-virtual_op-15">本冊完整規則</a></p>
</li>
<li id="q-250-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>把實際受影響 controller 清單與 domain 配置比較，而不只觀察發起端。</p>
</li>
<li id="q-250-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認裝置宣告或實作的是單 domain 還是多 domain 的 reset 範圍。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-251" data-question="251"><h2><a class="qa-qid" href="#q-251">Q251</a> Namespace 變更如何通知其他 Controller？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-251-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-251-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>管理操作可能由一條路徑發起，其他 Host 仍需要更新自己的 namespace 視圖。</p>
</li>
<li id="q-251-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>通知依受影響的 attached namespace 與 controller 觀察範圍，不是每台都無條件收到同一個通知。</p>
</li>
<li id="q-251-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 AEC.NAN、待處理 AER、Changed Namespace List 與各台 Active List；ANA 變更另外查其通知設定。</p>
</li>
<li id="q-251-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Attached Namespace Attribute Changed 提醒 Host 重查，Changed Namespace List 提供需重查的 NSID；清單溢位以 FFFFFFFFh 表示需全面重查。</p>
</li>
<li id="q-251-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>操作完成後處理通知、讀清單並更新 Identify；讀取確認與遮蔽規則影響後續同類通知。</p>
</li>
<li id="q-251-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>其他受影響 controller 的視圖與新配置一致；不要求每次改動一筆對一筆保留無限通知。</p>
</li>
<li id="q-251-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Admin Namespace Delete 的處理 controller 有通知排除規則，不能要求它因自己的刪除再收到相同通知。</p>
</li>
<li id="q-251-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-251-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Create／Delete 影響 Allocated List，Attach／Detach 影響指定 controller 的 Active List。 <a class="qa-rule-link" href="#common-namespace_op-9">本冊完整規則</a></p>
</li>
<li id="q-251-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>使用 Identify 的 Allocated、Active 與 Controller List 確認目前配置；Changed Attached Namespace List04h 與 Changed Allocated Namespace List1Ch 指出曾變更的 NSID，不能代替完整現況。 <a class="qa-rule-link" href="#common-namespace_op-10">本冊完整規則</a></p>
</li>
<li id="q-251-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 時，Namespace Management 對應的 Change Namespace Event06h 記錄建立／刪除等規定事件。 <a class="qa-rule-link" href="#common-namespace_op-11">本冊完整規則</a></p>
</li>
<li id="q-251-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>已完成的 namespace 配置與 Attach／Detach 跨 Reset 保留；重設的是命令通道，不是自動刪除 namespace。 <a class="qa-rule-link" href="#common-namespace_op-12">本冊完整規則</a></p>
</li>
<li id="q-251-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 不等於 Restore Default Namespace Configuration。 <a class="qa-rule-link" href="#common-namespace_op-13">本冊完整規則</a></p>
</li>
<li id="q-251-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後，已完成的 namespace 配置與附加關係仍需保留。 <a class="qa-rule-link" href="#common-namespace_op-14">本冊完整規則</a></p>
</li>
<li id="q-251-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>建立／刪除影響 subsystem 的 namespace inventory；附加清單指定哪些 controllers 改變存取關係。 <a class="qa-rule-link" href="#common-namespace_op-15">本冊完整規則</a></p>
</li>
<li id="q-251-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Namespace attribute notice 與 ANA change notice 描述不同變化，不能拿其中一份 Log 取代另一份。</p>
</li>
<li id="q-251-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查事件是否對這個 controller 適用，以及舊事件是否仍遮蔽新回報。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-changedlog">Base 2.4 §5.2.13.1.5</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-analog">Base 2.4 §5.2.13.1.13</a> · <a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-252" data-question="252"><h2><a class="qa-qid" href="#q-252">Q252</a> Asymmetric Controller Behavior 與 ANA 如何協助選路徑？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-252-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-252-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>相同 namespace 經不同 controller 存取，可能有不同效能或可用性；非對稱行為不只出現在網路傳輸。</p>
</li>
<li id="q-252-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>ANA 狀態描述 controller 與 ANA Group 的關係；不是 namespace 永久只有一個全域狀態。</p>
</li>
<li id="q-252-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 CMIC.ANARS、ANACAP、ANATT、namespace.ANAGRPID 與 LID0Ch。</p>
</li>
<li id="q-252-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Optimized／Non-Optimized 都可正常執行支援命令；Inaccessible、Persistent Loss 與 Change 對資料存取有不同限制與恢復建議。</p>
</li>
<li id="q-252-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先找可用路徑，再優先考慮 Optimized；遇到通知重新讀 ANA，不能永久把某 controller 寫死為最佳路徑。</p>
</li>
<li id="q-252-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Non-Optimized 可能較慢但不是錯誤；另一條路徑可對同一群組回不同狀態。</p>
</li>
<li id="q-252-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>受限制狀態對非例外命令分別回 Asymmetric Access Inaccessible、Persistent Loss 或 Transition；不是所有 Admin 命令都被一律禁止。</p>
</li>
<li id="q-252-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-252-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>資源配置與 Online／Offline 不定義統一成功 AER。 <a class="qa-rule-link" href="#common-virtual_op-9">本冊完整規則</a></p>
</li>
<li id="q-252-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>用 Primary Controller Capabilities、Secondary Controller List 及目前 queue／interrupt 能力確認配置；namespace 路徑則讀 Active List、Controller List 與適用 ANA Log。 <a class="qa-rule-link" href="#common-virtual_op-10">本冊完整規則</a></p>
</li>
<li id="q-252-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Virtualization Management 不是專用 PEL 事件。 <a class="qa-rule-link" href="#common-virtual_op-11">本冊完整規則</a></p>
</li>
<li id="q-252-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>查詢若因重設中止，恢復後須重新送出。比較回覆時，再逐欄區分固定身分、配置與動態狀態。 <a class="qa-rule-link" href="#common-identify-12">本冊完整規則</a></p>
</li>
<li id="q-252-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>重設後重新查詢受影響的物件。重設本身不表示 namespace 已刪除，也不表示配置已恢復出廠值。 <a class="qa-rule-link" href="#common-identify-13">本冊完整規則</a></p>
</li>
<li id="q-252-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新查詢並比較。若期間還有韌體啟用或管理操作，必須分清楚差異是由哪個事件造成。 <a class="qa-rule-link" href="#common-identify-14">本冊完整規則</a></p>
</li>
<li id="q-252-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Identify 是唯讀查詢。不同 controller 的 Active List 可能不同，因此比較時必須確認查詢對象。 <a class="qa-rule-link" href="#common-identify-15">本冊完整規則</a></p>
</li>
<li id="q-252-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>僅量到效能不同，不能反推必定支援 ANA Reporting；應先確認宣告再用 Log 解釋。</p>
</li>
<li id="q-252-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認 ANAGRPID 對應的 controller 視圖，而不是讀錯路徑的 Log。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-ana">Base 2.4 §2.4.2, 8.1.1 (PCIe namespace access)</a> · <a href="#ref-analog">Base 2.4 §5.2.13.1.13</a> · <a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-253" data-question="253"><h2><a class="qa-qid" href="#q-253">Q253</a> Secondary Controller 如何 Online 或 Offline？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-253-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-253-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Online 代表資源與狀態允許 Host 使用，還不等於 CC.EN／RDY 已經完成啟用。</p>
</li>
<li id="q-253-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>由 associated primary 管理該 secondary；Offline 時 CSTS.CFS=1，其他 controller properties undefined。</p>
</li>
<li id="q-253-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 Secondary List.SCS、NVQ、NVI 與 primary 是否已 enabled。</p>
</li>
<li id="q-253-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Virtualization Management ACT=7 Offline、8 Assign、9 Online；Offline 會移除 Flexible Resources。</p>
</li>
<li id="q-253-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>建議先 Offline，再配置 VQ／VI，做 CLR；若為 VF 建議 VF FLR，再 Online，最後執行 NVMe enable 與 queue 初始化。</p>
</li>
<li id="q-253-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>支援 VQ 時至少 2 組，包含 Admin 與至少 1 組 I/O；支援 VI 時至少 vector0 的資源，才可 Online。</p>
</li>
<li id="q-253-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>未 Offline 就 Assign，或資源不足／primary 未 enabled 卻要求 Online，回 Invalid Secondary Controller State；重複相同 Online／Offline 不是錯誤。</p>
</li>
<li id="q-253-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-253-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>資源配置與 Online／Offline 不定義統一成功 AER。 <a class="qa-rule-link" href="#common-virtual_op-9">本冊完整規則</a></p>
</li>
<li id="q-253-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>用 Primary Controller Capabilities、Secondary Controller List 及目前 queue／interrupt 能力確認配置；namespace 路徑則讀 Active List、Controller List 與適用 ANA Log。 <a class="qa-rule-link" href="#common-virtual_op-10">本冊完整規則</a></p>
</li>
<li id="q-253-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Virtualization Management 不是專用 PEL 事件。 <a class="qa-rule-link" href="#common-virtual_op-11">本冊完整規則</a></p>
</li>
<li id="q-253-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Primary 被 Disable、CLR 或 Shutdown 時，其 secondary 必須轉 Offline；Online 轉 Offline 會移除 Flexible Resources。 <a class="qa-rule-link" href="#common-virtual_op-12">本冊完整規則</a></p>
</li>
<li id="q-253-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 影響範圍內的 primary／secondary 操作環境須重建。 <a class="qa-rule-link" href="#common-virtual_op-13">本冊完整規則</a></p>
</li>
<li id="q-253-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Primary Flexible Allocation 跨 Power Cycle 保留；secondary 的 Online 狀態與資源需重新查詢及配置。 <a class="qa-rule-link" href="#common-virtual_op-14">本冊完整規則</a></p>
</li>
<li id="q-253-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Primary 管理自己的 secondary 群組及 Flexible Resource pool，同一份資源不能同時分給兩個 controller。 <a class="qa-rule-link" href="#common-virtual_op-15">本冊完整規則</a></p>
</li>
<li id="q-253-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>把 SCS 與 CC.EN／CSTS.RDY 分開驗證，避免把 Offline 的 CFS 當成一定發生未知硬體故障。</p>
</li>
<li id="q-253-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查資源與狀態前提是否完成，再判斷啟用超時。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-254" data-question="254"><h2><a class="qa-qid" href="#q-254">Q254</a> Virtualization Management 如何分配與釋放資源？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-254-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-254-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Flexible Resource pool 可在 primary 與它的 secondary 間分配，但不是動態擴充實體總資源。</p>
</li>
<li id="q-254-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>VQ 與 VI 分開計數；Private Resources 不可用此命令重新指派。</p>
</li>
<li id="q-254-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 CRT、總量、已分配量、secondary 最大值與 preferred granularity。</p>
</li>
<li id="q-254-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CDW10.CNTLID／RT／ACT 選目標、種類與動作，CDW11.NR 指要求數量；CQE.DW0.NRM 是實際修改數量。</p>
</li>
<li id="q-254-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>secondary 先 Offline，再 Assign；要釋放 Online secondary 的 Flexible Resources，可將其 Offline。Primary 新配置則等指定類型的 CLR 才生效。</p>
</li>
<li id="q-254-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>NRM 可比 NR 小或大，須讀回能力與清單確認，不能把 requested count 當成實際值。</p>
</li>
<li id="q-254-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>超出總量或每台上限對應 Invalid Number of Controller Resources；不存在、Private 或已被使用的資源範圍對應 Invalid Resource Identifier。</p>
</li>
<li id="q-254-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-254-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>資源配置與 Online／Offline 不定義統一成功 AER。 <a class="qa-rule-link" href="#common-virtual_op-9">本冊完整規則</a></p>
</li>
<li id="q-254-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>用 Primary Controller Capabilities、Secondary Controller List 及目前 queue／interrupt 能力確認配置；namespace 路徑則讀 Active List、Controller List 與適用 ANA Log。 <a class="qa-rule-link" href="#common-virtual_op-10">本冊完整規則</a></p>
</li>
<li id="q-254-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Virtualization Management 不是專用 PEL 事件。 <a class="qa-rule-link" href="#common-virtual_op-11">本冊完整規則</a></p>
</li>
<li id="q-254-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Primary 被 Disable、CLR 或 Shutdown 時，其 secondary 必須轉 Offline；Online 轉 Offline 會移除 Flexible Resources。 <a class="qa-rule-link" href="#common-virtual_op-12">本冊完整規則</a></p>
</li>
<li id="q-254-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 影響範圍內的 primary／secondary 操作環境須重建。 <a class="qa-rule-link" href="#common-virtual_op-13">本冊完整規則</a></p>
</li>
<li id="q-254-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Primary Flexible Allocation 跨 Power Cycle 保留；secondary 的 Online 狀態與資源需重新查詢及配置。 <a class="qa-rule-link" href="#common-virtual_op-14">本冊完整規則</a></p>
</li>
<li id="q-254-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Primary 管理自己的 secondary 群組及 Flexible Resource pool，同一份資源不能同時分給兩個 controller。 <a class="qa-rule-link" href="#common-virtual_op-15">本冊完整規則</a></p>
</li>
<li id="q-254-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>將所有配置加總與 pool 比較；相同 resource 不能同時屬兩台，preferred granularity 也不能直接當成任意硬性拒絕規則。</p>
</li>
<li id="q-254-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查 CQE.NRM 與 readback，而不是只看送出的 NR。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-255" data-question="255"><h2><a class="qa-qid" href="#q-255">Q255</a> Reset 與 Power Cycle 後 Virtualization 資源如何恢復？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-255-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-255-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Primary 的持久配置與 secondary 的即時資源指派有不同生命週期，必須分開保存與驗證。</p>
</li>
<li id="q-255-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>除了被重設的 controller，也要檢查依賴該 primary 的 secondary 群組。</p>
</li>
<li id="q-255-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>保存 Primary Capabilities、Secondary List、重設來源與 PCIe function 關係。</p>
</li>
<li id="q-255-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Primary Flexible Allocation 是持久設定，新值在非 Controller Reset 的 CLR 後生效；僅清 CC.EN 不符合這個生效條件。</p>
</li>
<li id="q-255-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>Primary 恢復後重新查 secondary 狀態，依 Offline→Assign→適當 CLR→Online→Enable 重建使用環境。</p>
</li>
<li id="q-255-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>可保留的 allocation 設定正確恢復，secondary 重新取得適足資源，新的 queues 才有效。</p>
</li>
<li id="q-255-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不能因 primary allocation 還在，就要求 secondary 原 I/O queues 或原 Online 狀態一併保留。</p>
</li>
<li id="q-255-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-255-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>資源配置與 Online／Offline 不定義統一成功 AER。 <a class="qa-rule-link" href="#common-virtual_op-9">本冊完整規則</a></p>
</li>
<li id="q-255-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>用 Primary Controller Capabilities、Secondary Controller List 及目前 queue／interrupt 能力確認配置；namespace 路徑則讀 Active List、Controller List 與適用 ANA Log。 <a class="qa-rule-link" href="#common-virtual_op-10">本冊完整規則</a></p>
</li>
<li id="q-255-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Virtualization Management 不是專用 PEL 事件。 <a class="qa-rule-link" href="#common-virtual_op-11">本冊完整規則</a></p>
</li>
<li id="q-255-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>Primary 被 Disable、CLR 或 Shutdown 時，其 secondary 必須轉 Offline；Online 轉 Offline 會移除 Flexible Resources。 <a class="qa-rule-link" href="#common-virtual_op-12">本冊完整規則</a></p>
</li>
<li id="q-255-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 影響範圍內的 primary／secondary 操作環境須重建。 <a class="qa-rule-link" href="#common-virtual_op-13">本冊完整規則</a></p>
</li>
<li id="q-255-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Primary Flexible Allocation 跨 Power Cycle 保留；secondary 的 Online 狀態與資源需重新查詢及配置。 <a class="qa-rule-link" href="#common-virtual_op-14">本冊完整規則</a></p>
</li>
<li id="q-255-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Primary 管理自己的 secondary 群組及 Flexible Resource pool，同一份資源不能同時分給兩個 controller。 <a class="qa-rule-link" href="#common-virtual_op-15">本冊完整規則</a></p>
</li>
<li id="q-255-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Namespace attachment 可持續存在，即使 secondary 暫時 Offline；不應因此重複 Create Namespace。</p>
</li>
<li id="q-255-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查 Reset 是否使 primary Disable，連帶造成 secondary Offline 與資源移除。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-multipath">Base 2.4 §2.4.1–2.4.2 (PCIe topology)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-virtualcmd">Base 2.4 §5.3.6</a> · <a href="#ref-virtualid">Base 2.4 §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</a> · <a href="#ref-nsattach">Base 2.4 §5.2.24–5.2.25, 8.1.17–8.1.17.2</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-command-8"><h3>命令完成、事件與紀錄 · DNR 與 More 應如何設定？</h3><p>只有收到 CQE，才有 DNR 與 More 可供判讀。DNR=1 表示相同命令即使重送到此 NVM subsystem 的任一 controller，仍預期會失敗；DNR=0 則只表示可能成功。除非個別錯誤條件另有明定，不能只看 Status 名稱就要求 DNR=1。More=1 表示 Error Information Log 有這筆命令的補充資訊。SCT=SC=0 時，DNR 應為 0。</p></article>
<article id="common-identify-12"><h3>查詢的重設與影響範圍 · Controller Reset 後是否保留或繼續？</h3><p>Controller Reset 會中止尚未完成的查詢。沒有收到回覆，不等於 controller 回傳全零資料；Host 應等查詢通道恢復後重新讀取，再逐欄分辨固定識別、目前配置與動態狀態。Reset 本身也不表示 namespace 已刪除。</p></article>
<article id="common-identify-13"><h3>查詢的重設與影響範圍 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>重設完成後，重新查詢受影響的 controller 與 namespace。NVM Subsystem Reset 重設的是通訊及控制狀態，不能直接推論所有儲存配置都回到出廠值。若期間還執行了其他管理操作，則另依該操作的規則確認變更。</p></article>
<article id="common-identify-14"><h3>查詢的重設與影響範圍 · Power Cycle 後是否保留或繼續？</h3><p>Power Cycle 後，重新查詢版本、能力、目前格式及附加清單。固定識別資訊與持續配置，不應當成一般暫存 Feature 處理。不過，若同時發生韌體啟用或配置變更，結果可能不同，因此要保留前後資料及事件時間，才能解釋差異。</p></article>
<article id="common-identify-15"><h3>查詢的重設與影響範圍 · 是否影響其他 Controller 或 Namespace？</h3><p>Identify 只讀取資訊，不會建立、格式化或附加 namespace。回覆描述哪個物件，由 CNS 與相關選擇欄位決定。不同 controller 的 Active List 可以不同，不能只因清單不同就判定資料損壞。</p></article>
<article id="common-namespace_op-9"><h3>本主題的共用條件 · 是否產生 Asynchronous Event？</h3><p>Create／Delete 影響 Allocated List，Attach／Detach 影響指定 controller 的 Active List。依各 controller 的事件支援與 AEC 回報變更；Admin SQ 收到 Delete 的 controller 不回報該次刪除通知，其他受影響且啟用通知的 controller 仍須依規則回報。</p></article>
<article id="common-namespace_op-10"><h3>本主題的共用條件 · 是否更新 Error Information Log 或其他 Log？</h3><p>使用 Identify 的 Allocated、Active 與 Controller List 確認目前配置；Changed Attached Namespace List04h 與 Changed Allocated Namespace List1Ch 指出曾變更的 NSID，不能代替完整現況。失敗則依 More 與 Error Information 補充欄位處理。</p></article>
<article id="common-namespace_op-11"><h3>本主題的共用條件 · 是否記錄於 Persistent Event Log？</h3><p>支援 PEL 時，Namespace Management 對應的 Change Namespace Event06h 記錄建立／刪除等規定事件。Attach／Detach 不應直接當成 Create／Delete；Write Protection 則依該 Feature 是否支援 Set Feature Event 記錄。</p></article>
<article id="common-namespace_op-12"><h3>本主題的共用條件 · Controller Reset 後是否保留或繼續？</h3><p>已完成的 namespace 配置與 Attach／Detach 跨 Reset 保留；重設的是命令通道，不是自動刪除 namespace。若 Reset 前未收到完成，恢復後須查清單確認結果，不能假設整筆操作必定回復。</p></article>
<article id="common-namespace_op-13"><h3>本主題的共用條件 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>Subsystem Reset 不等於 Restore Default Namespace Configuration。恢復後重新探索原 namespace 與附加關係，再建立 I/O queues；多 domain 的實際 Reset 範圍另行確認。</p></article>
<article id="common-namespace_op-14"><h3>本主題的共用條件 · Power Cycle 後是否保留或繼續？</h3><p>Power Cycle 後，已完成的 namespace 配置與附加關係仍需保留。Write Protect 與 Permanent Write Protect 保留；Write Protect Until Power Cycle 則在實際 power cycle 轉回未保護，不能把這個例外套到全部配置。</p></article>
<article id="common-namespace_op-15"><h3>本主題的共用條件 · 是否影響其他 Controller 或 Namespace？</h3><p>建立／刪除影響 subsystem 的 namespace inventory；附加清單指定哪些 controllers 改變存取關係。共享 namespace 的保護狀態必須由所有附加的 controllers 執行，不因換路徑而解除。</p></article>
<article id="common-virtual_op-9"><h3>本主題的共用條件 · 是否產生 Asynchronous Event？</h3><p>資源配置與 Online／Offline 不定義統一成功 AER。Namespace 屬性或 ANA 狀態若另外符合變更條件，才依各自通知設定與規則回報。</p></article>
<article id="common-virtual_op-10"><h3>本主題的共用條件 · 是否更新 Error Information Log 或其他 Log？</h3><p>用 Primary Controller Capabilities、Secondary Controller List 及目前 queue／interrupt 能力確認配置；namespace 路徑則讀 Active List、Controller List 與適用 ANA Log。不要把資源數量變更當成 Error Log 紀錄。</p></article>
<article id="common-virtual_op-11"><h3>本主題的共用條件 · 是否記錄於 Persistent Event Log？</h3><p>Virtualization Management 不是專用 PEL 事件。若流程包含已完成的 Reset 或符合條件的 namespace 管理，則依那些事件記錄；不能要求每次 Assign 都新增 Reset event。</p></article>
<article id="common-virtual_op-12"><h3>本主題的共用條件 · Controller Reset 後是否保留或繼續？</h3><p>Primary 被 Disable、CLR 或 Shutdown 時，其 secondary 必須轉 Offline；Online 轉 Offline 會移除 Flexible Resources。Primary 的 Flexible Allocation 設定可持續，但新配置需由非 CC.EN Controller Reset 的 CLR 生效。</p></article>
<article id="common-virtual_op-13"><h3>本主題的共用條件 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>Subsystem Reset 影響範圍內的 primary／secondary 操作環境須重建。不要把持續的 primary allocation 設定，誤當成 secondary 仍 Online 或原 queues 仍存在。</p></article>
<article id="common-virtual_op-14"><h3>本主題的共用條件 · Power Cycle 後是否保留或繼續？</h3><p>Primary Flexible Allocation 跨 Power Cycle 保留；secondary 的 Online 狀態與資源需重新查詢及配置。Namespace 與 attachment 的持續性是另一項規則，不因 secondary Offline 就刪除。</p></article>
<article id="common-virtual_op-15"><h3>本主題的共用條件 · 是否影響其他 Controller 或 Namespace？</h3><p>Primary 管理自己的 secondary 群組及 Flexible Resource pool，同一份資源不能同時分給兩個 controller。Shared namespace 則讓多條路徑存取同一份資料，Host 仍需協調同時寫入。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-multipath"><strong>Base 2.4 · §2.4.1–2.4.2 (PCIe topology)</strong><br>文件頁 34–37 · PDF 60–63 · Figure 19–22</li>
<li id="ref-ana"><strong>Base 2.4 · §2.4.2, 8.1.1 (PCIe namespace access)</strong><br>文件頁 37, 578–584 · PDF 63, 604–610 · Figure 675–678</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>文件頁 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-changedlog"><strong>Base 2.4 · §5.2.13.1.5</strong><br>文件頁 226 · PDF 252</li>
<li id="ref-analog"><strong>Base 2.4 · §5.2.13.1.13</strong><br>文件頁 241–244 · PDF 267–270 · Figure 229–231</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idlist"><strong>Base 2.4 · §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</strong><br>文件頁 387–399, 402–404 · PDF 413–425, 428–430 · Figure 342–355, 360–362</li>
<li id="ref-virtualid"><strong>Base 2.4 · §5.2.14.3.1–5.2.14.3.2 (Primary Capabilities, Secondary List)</strong><br>文件頁 402–404 · PDF 428–430 · Figure 360–362</li>
<li id="ref-nsattach"><strong>Base 2.4 · §5.2.24–5.2.25, 8.1.17–8.1.17.2</strong><br>文件頁 444–448, 660–663 · PDF 470–474, 686–689 · Figure 442–450</li>
<li id="ref-virtualcmd"><strong>Base 2.4 · §5.3.6</strong><br>文件頁 533–535 · PDF 559–561 · Figure 587–590</li>
<li id="ref-virtual"><strong>Base 2.4 · §8.2.7</strong><br>文件頁 754–758 · PDF 780–784 · Figure 796</li>
</ul><h3>需要看欄位圖時</h3><p>以下連結可開啟對應的圖表教學，查閱欄位及判讀方式。每張圖保留固定的教學位置，方便之後反覆查詢。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/virtualization/en/">English</a><a href="/DOCS/nvme-question-bank/virtualization.html">繁中教學 HTML</a></nav>
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
