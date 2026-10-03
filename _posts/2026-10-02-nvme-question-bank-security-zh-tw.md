---
layout: post
title: "NVMe 自問自答題庫：Security 與 Lockdown"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/security/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/security/en/">English</a><a href="/DOCS/nvme-question-bank/security.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–320</p>
<header><p class="qa-range">Q237–Q245</p><h1>Security 與 Lockdown</h1><p class="qr-intro">Security Send／Receive 承載協定資料；Lockdown 限制命令或 Feature。先分清資料交換結果與禁止範圍，再討論 reset 及斷電持續性。</p><p>先練習，再展開每題的 17 項解答。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>傳輸成功、協定成功與允許執行</h2><p class="qa-takeaway">NVMe Success 不自動等於認證成功；被鎖定 Feature 的 Get 也不自動被禁止。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">問題</th><th scope="col">需要的資訊</th><th scope="col">結果所在位置</th></tr></thead><tbody><tr><td>資料有沒有交換</td><td>Security CQE</td><td>NVMe 命令結果</td></tr><tr><td>安全操作是否成功</td><td>SECP、SPSP、payload</td><td>所選協定定義</td></tr><tr><td>命令是否被禁止</td><td>IFC、CSEL、SCP、清單</td><td>Lockdown 及目標 CQE</td></tr><tr><td>斷電後是否保留</td><td>CSEL 與 LDPE</td><td>範圍專屬規則</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>CSEL=0、LDPE=1 的禁止可跨 Power Cycle 保留；CSEL=1／2 不能只因 LDPE=1 就取得同樣持續性。</p>
<p class="qa-citations">來源：<a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-237">Q237 · 如何確認 Security Send／Receive 與實際協定支援？</a></li>
<li><a href="#q-238">Q238 · Security Protocol、欄位或資料長度不合法時如何處理？</a></li>
<li><a href="#q-239">Q239 · Security 資料傳輸失敗應如何區分 Status 與協定錯誤？</a></li>
<li><a href="#q-240">Q240 · Security 狀態如何影響其他 Admin Command？</a></li>
<li><a href="#q-241">Q241 · Reset 與 Power Cycle 後 Security 狀態是否保留？</a></li>
<li><a href="#q-242">Q242 · Lockdown 如何限制指定 Command 或 Feature？</a></li>
<li><a href="#q-243">Q243 · 執行被 Lockdown 禁止的命令或 Feature 應如何回應？</a></li>
<li><a href="#q-244">Q244 · Lockdown Log 的一般與增強格式如何解讀？</a></li>
<li><a href="#q-245">Q245 · Reset 與 Power Cycle 後 Lockdown 是否保留？</a></li>
</ol></section>
<article class="qa-question" id="q-237" data-question="237"><h2><a class="qa-qid" href="#q-237">Q237</a> 如何確認 Security Send／Receive 與實際協定支援？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-237-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-237-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>NVMe 命令支援與特定安全協定支援是兩層能力，先確認前者，才能安全解讀後者的回覆。</p>
</li>
<li id="q-237-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>OACS 描述 controller 的命令能力；協定探索回覆才說明它能處理哪些 SECP。</p>
</li>
<li id="q-237-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 Identify.OACS 的 Security Send／Receive 支援，並核對 Commands Supported and Effects。</p>
</li>
<li id="q-237-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Security Receive 使用 SECP=00h 探索支援協定；這次查詢不需要先送 Security Send。</p>
</li>
<li id="q-237-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先探索，再依所選協定配置 SPSP、NSSF 與資料長度，後續 Send／Receive 配對依協定定義。</p>
</li>
<li id="q-237-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>NVMe 成功表示命令完成；協定清單指出可繼續使用的安全協定，不表示已完成認證。</p>
</li>
<li id="q-237-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Security Receive 指定不支援 SECP 必須 Invalid Field in Command；完全不支援 Opcode 則是另一層命令支援問題。</p>
</li>
<li id="q-237-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-237-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Security Send／Receive 的一般資料交換不定義統一成功 AER。 <a class="qa-rule-link" href="#common-security_op-9">本冊完整規則</a></p>
</li>
<li id="q-237-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>先分開 NVMe CQE 與安全協定回覆：CQE 說明命令傳輸／處理，Security Receive 的 payload 才依協定描述安全操作結果。 <a class="qa-rule-link" href="#common-security_op-10">本冊完整規則</a></p>
</li>
<li id="q-237-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Security 資料交換不是 PEL 的通用逐命令稽核紀錄。 <a class="qa-rule-link" href="#common-security_op-11">本冊完整規則</a></p>
</li>
<li id="q-237-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後 Security Receive 待取的結果可能不保留。 <a class="qa-rule-link" href="#common-security_op-12">本冊完整規則</a></p>
</li>
<li id="q-237-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新確認通訊及協定狀態。 <a class="qa-rule-link" href="#common-security_op-13">本冊完整規則</a></p>
</li>
<li id="q-237-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後不能只因 NVMe queues 已重建，就推論安全狀態回到未鎖定。 <a class="qa-rule-link" href="#common-security_op-14">本冊完整規則</a></p>
</li>
<li id="q-237-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>資料經目標 controller 傳送，但安全操作可能影響一個範圍、namespace 或整個 subsystem；真正範圍由 SECP、SPSP 與 payload 指定的協定決定，不能只看 Admin Queue 所屬 controller。 <a class="qa-rule-link" href="#common-security_op-15">本冊完整規則</a></p>
</li>
<li id="q-237-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Identify、效果 Log 與探索結果應一致，但不能因 Opcode 受支援就要求每個 SECP 都成功。</p>
</li>
<li id="q-237-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查失敗出在 NVMe 命令層，還是選到未支援的安全協定。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-238" data-question="238"><h2><a class="qa-qid" href="#q-238">Q238</a> Security Protocol、欄位或資料長度不合法時如何處理？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-238-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-238-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>必須分清外層 NVMe 欄位與內層安全資料，否則容易期待錯的 Status。</p>
</li>
<li id="q-238-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>SECP、SPSP、NSSF 與 DPTR／長度都屬查證範圍，但 payload 格式由協定定義。</p>
</li>
<li id="q-238-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先查 SECP 探索結果與 NVMe 命令支援，再選具體協定。</p>
</li>
<li id="q-238-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Receive 的 AL 與 Send 的 TL 依 Security Protocol In／Out、INC_512=0 的定義使用；不能當成 NVMe 一般 zero-based Dword 數。</p>
</li>
<li id="q-238-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先核對 NVMe 欄位與 buffer 長度，再解析協定內容；NSSF 只在 EAh 的指定用途下有定義。</p>
</li>
<li id="q-238-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>合法傳輸取得對應資料或協定回覆；應按協定結果決定認證或安全操作是否成功。</p>
</li>
<li id="q-238-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Receive 不支援 SECP、Send 使用保留 SECP 須 Invalid Field。內層認證失敗可能以協定 payload 表示，不能全部改寫成 Invalid Field 或 Access Denied CQE。</p>
</li>
<li id="q-238-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-238-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Security Send／Receive 的一般資料交換不定義統一成功 AER。 <a class="qa-rule-link" href="#common-security_op-9">本冊完整規則</a></p>
</li>
<li id="q-238-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>先分開 NVMe CQE 與安全協定回覆：CQE 說明命令傳輸／處理，Security Receive 的 payload 才依協定描述安全操作結果。 <a class="qa-rule-link" href="#common-security_op-10">本冊完整規則</a></p>
</li>
<li id="q-238-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Security 資料交換不是 PEL 的通用逐命令稽核紀錄。 <a class="qa-rule-link" href="#common-security_op-11">本冊完整規則</a></p>
</li>
<li id="q-238-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後 Security Receive 待取的結果可能不保留。 <a class="qa-rule-link" href="#common-security_op-12">本冊完整規則</a></p>
</li>
<li id="q-238-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新確認通訊及協定狀態。 <a class="qa-rule-link" href="#common-security_op-13">本冊完整規則</a></p>
</li>
<li id="q-238-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後不能只因 NVMe queues 已重建，就推論安全狀態回到未鎖定。 <a class="qa-rule-link" href="#common-security_op-14">本冊完整規則</a></p>
</li>
<li id="q-238-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>資料經目標 controller 傳送，但安全操作可能影響一個範圍、namespace 或整個 subsystem；真正範圍由 SECP、SPSP 與 payload 指定的協定決定，不能只看 Admin Queue 所屬 controller。 <a class="qa-rule-link" href="#common-security_op-15">本冊完整規則</a></p>
</li>
<li id="q-238-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>對同一測試記錄外層 CQE 與內層 result，避免把兩者混為一個錯誤碼。</p>
</li>
<li id="q-238-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查 AL／TL 單位與實際 buffer 是否足夠，而不是直接猜密碼錯誤。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-239" data-question="239"><h2><a class="qa-qid" href="#q-239">Q239</a> Security 資料傳輸失敗應如何區分 Status 與協定錯誤？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-239-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-239-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>資料根本沒有正確傳送，與資料送到後協定拒絕，是不同故障階段。</p>
</li>
<li id="q-239-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>先看 NVMe 命令，再看所選安全協定；同一個安全動作可能涉及多筆 Send／Receive。</p>
</li>
<li id="q-239-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>保存完整 SQE、DPTR、長度、CQE 與有效的 Receive payload。</p>
</li>
<li id="q-239-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Data Transfer Error 表示命令資料傳輸問題；安全結果可能另外以協定欄位回報，不能只靠字面上的「Security」決定 Status。</p>
</li>
<li id="q-239-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先檢查 CQE 是否允許信任回傳資料，再依協定解碼；失敗傳輸的舊 buffer 內容不能當新回覆。</p>
</li>
<li id="q-239-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功 CQE 只證明該 NVMe 命令成功完成，還需讀協定結果才知道操作是否獲准。</p>
</li>
<li id="q-239-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>未支援欄位、傳輸錯誤、內部錯誤與認證拒絕各有不同前提；沒有「所有安全失敗都回同一 Status」的規則。</p>
</li>
<li id="q-239-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-239-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Security Send／Receive 的一般資料交換不定義統一成功 AER。 <a class="qa-rule-link" href="#common-security_op-9">本冊完整規則</a></p>
</li>
<li id="q-239-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>先分開 NVMe CQE 與安全協定回覆：CQE 說明命令傳輸／處理，Security Receive 的 payload 才依協定描述安全操作結果。 <a class="qa-rule-link" href="#common-security_op-10">本冊完整規則</a></p>
</li>
<li id="q-239-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Security 資料交換不是 PEL 的通用逐命令稽核紀錄。 <a class="qa-rule-link" href="#common-security_op-11">本冊完整規則</a></p>
</li>
<li id="q-239-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後 Security Receive 待取的結果可能不保留。 <a class="qa-rule-link" href="#common-security_op-12">本冊完整規則</a></p>
</li>
<li id="q-239-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新確認通訊及協定狀態。 <a class="qa-rule-link" href="#common-security_op-13">本冊完整規則</a></p>
</li>
<li id="q-239-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後不能只因 NVMe queues 已重建，就推論安全狀態回到未鎖定。 <a class="qa-rule-link" href="#common-security_op-14">本冊完整規則</a></p>
</li>
<li id="q-239-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>資料經目標 controller 傳送，但安全操作可能影響一個範圍、namespace 或整個 subsystem；真正範圍由 SECP、SPSP 與 payload 指定的協定決定，不能只看 Admin Queue 所屬 controller。 <a class="qa-rule-link" href="#common-security_op-15">本冊完整規則</a></p>
</li>
<li id="q-239-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>將兩層結果與先後順序對回原始 request，避免讀到上一個 exchange 的結果。</p>
</li>
<li id="q-239-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是不是把成功傳輸的「協定拒絕」誤認成 DMA 失敗。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-240" data-question="240"><h2><a class="qa-qid" href="#q-240">Q240</a> Security 狀態如何影響其他 Admin Command？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-240-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-240-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>安全協定可能限制其他操作，但不能用一個抽象的「Locked」推論所有 Admin 都被禁止。</p>
</li>
<li id="q-240-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>影響範圍由協定、保護對象與 NVMe 明定互動共同決定。</p>
</li>
<li id="q-240-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>確認實際 SECP／安全狀態、Lockdown Log，以及適用的 Security Personality 設定。</p>
</li>
<li id="q-240-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Security Send／Receive 傳送協定；Lockdown 是另一个命令禁止機制；Namespace Write Protection 又控制另一種存取狀態。</p>
</li>
<li id="q-240-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先判斷被拒命令與範圍，再確認哪一項機制要求拒絕，最後對照該機制指定的 Status。</p>
</li>
<li id="q-240-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>被允許的查詢仍可能正常運作；解除一種限制不保證其他限制一起解除。</p>
</li>
<li id="q-240-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不能把所有拒絕都要求回 Command Prohibited by Lockdown；只有符合 Lockdown 條件才使用該通用 SC23h。</p>
</li>
<li id="q-240-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-240-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Security Send／Receive 的一般資料交換不定義統一成功 AER。 <a class="qa-rule-link" href="#common-security_op-9">本冊完整規則</a></p>
</li>
<li id="q-240-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>先分開 NVMe CQE 與安全協定回覆：CQE 說明命令傳輸／處理，Security Receive 的 payload 才依協定描述安全操作結果。 <a class="qa-rule-link" href="#common-security_op-10">本冊完整規則</a></p>
</li>
<li id="q-240-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Security 資料交換不是 PEL 的通用逐命令稽核紀錄。 <a class="qa-rule-link" href="#common-security_op-11">本冊完整規則</a></p>
</li>
<li id="q-240-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後 Security Receive 待取的結果可能不保留。 <a class="qa-rule-link" href="#common-security_op-12">本冊完整規則</a></p>
</li>
<li id="q-240-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新確認通訊及協定狀態。 <a class="qa-rule-link" href="#common-security_op-13">本冊完整規則</a></p>
</li>
<li id="q-240-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後不能只因 NVMe queues 已重建，就推論安全狀態回到未鎖定。 <a class="qa-rule-link" href="#common-security_op-14">本冊完整規則</a></p>
</li>
<li id="q-240-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>資料經目標 controller 傳送，但安全操作可能影響一個範圍、namespace 或整個 subsystem；真正範圍由 SECP、SPSP 與 payload 指定的協定決定，不能只看 Admin Queue 所屬 controller。 <a class="qa-rule-link" href="#common-security_op-15">本冊完整規則</a></p>
</li>
<li id="q-240-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>原始協定回覆、Lockdown 清單與命令行為要分層吻合，不能混用安全狀態名稱。</p>
</li>
<li id="q-240-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先指出是哪一個具體機制阻擋命令，再談解鎖與重試。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-241" data-question="241"><h2><a class="qa-qid" href="#q-241">Q241</a> Reset 與 Power Cycle 後 Security 狀態是否保留？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-241-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-241-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>原問題必須指定「哪個安全協定的哪個狀態」，才會有可驗證的保留答案。</p>
</li>
<li id="q-241-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>長期金鑰、持久鎖定設定、暫時 session 與待取的 Receive 資料，不是同一種狀態。</p>
</li>
<li id="q-241-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>記錄 SECP、協定版本、操作前狀態與 Reset 來源；三份 NVMe 規格只提供其明定的傳輸邊界。</p>
</li>
<li id="q-241-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Base 明定失聯或 CLR 可能不保留 Security Receive 資料；這不等於永久設定被擦除。</p>
</li>
<li id="q-241-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>恢復後重新建立需要的交換並查詢狀態，再依協定確認是否需重新認證。</p>
</li>
<li id="q-241-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>正確結果是符合已指定協定的保留規則，而不是所有狀態一律保留或一律清空。</p>
</li>
<li id="q-241-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>協定未指定時，不得捏造固定 Status、解鎖結果或金鑰處理；應明確標示來源未定義的部分。</p>
</li>
<li id="q-241-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-241-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Security Send／Receive 的一般資料交換不定義統一成功 AER。 <a class="qa-rule-link" href="#common-security_op-9">本冊完整規則</a></p>
</li>
<li id="q-241-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>先分開 NVMe CQE 與安全協定回覆：CQE 說明命令傳輸／處理，Security Receive 的 payload 才依協定描述安全操作結果。 <a class="qa-rule-link" href="#common-security_op-10">本冊完整規則</a></p>
</li>
<li id="q-241-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Security 資料交換不是 PEL 的通用逐命令稽核紀錄。 <a class="qa-rule-link" href="#common-security_op-11">本冊完整規則</a></p>
</li>
<li id="q-241-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>CLR 後 Security Receive 待取的結果可能不保留。 <a class="qa-rule-link" href="#common-security_op-12">本冊完整規則</a></p>
</li>
<li id="q-241-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 後重新確認通訊及協定狀態。 <a class="qa-rule-link" href="#common-security_op-13">本冊完整規則</a></p>
</li>
<li id="q-241-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後不能只因 NVMe queues 已重建，就推論安全狀態回到未鎖定。 <a class="qa-rule-link" href="#common-security_op-14">本冊完整規則</a></p>
</li>
<li id="q-241-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>資料經目標 controller 傳送，但安全操作可能影響一個範圍、namespace 或整個 subsystem；真正範圍由 SECP、SPSP 與 payload 指定的協定決定，不能只看 Admin Queue 所屬 controller。 <a class="qa-rule-link" href="#common-security_op-15">本冊完整規則</a></p>
</li>
<li id="q-241-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>把傳輸重新初始化、session 重建與持久設定驗證拆成三項，比單看命令成功更可靠。</p>
</li>
<li id="q-241-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查題目中的「Security 狀態」究竟指哪個欄位或協定物件。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-242" data-question="242"><h2><a class="qa-qid" href="#q-242">Q242</a> Lockdown 如何限制指定 Command 或 Feature？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-242-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-242-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Lockdown 限制命令在選定介面與 controller 執行，用來控制管理入口；它不是加密資料或設定 namespace 唯讀。</p>
</li>
<li id="q-242-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>CSEL=0 選 subsystem，1 選指定 controller，2 選指定 primary 的 secondary 群組；IFC 另選收命令的介面。</p>
</li>
<li id="q-242-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 OACS.CFLS／CCFLS 與 LID14h 的可禁止清單；哪些 Opcode／FID 可禁止由實作宣告。</p>
</li>
<li id="q-242-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CDW10.SCP 選 Admin Opcode 或 Set Features FID，OFI 指目標，PRHBT=1 禁止、0 允許；CDW14.CSS 選 controller，必要時 UIDX 選定義。</p>
</li>
<li id="q-242-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先查能力與清單，再送 Lockdown，等成功後讀目前禁止清單，最後以相同介面驗證目標命令。</p>
</li>
<li id="q-242-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功後選定目標受限制；重複禁止已禁止項目，或允許已允許項目，都不是錯誤。</p>
</li>
<li id="q-242-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不可禁止項目必須回命令特定 Prohibition of Command Execution Not Supported；不支援 CCFLS 卻指定非零 CSEL 須 Invalid Field。</p>
</li>
<li id="q-242-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-242-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Lockdown 成功不定義一個一般性的設定完成 AER。 <a class="qa-rule-link" href="#common-lockdown_op-9">本冊完整規則</a></p>
</li>
<li id="q-242-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Lockdown Log 的目前禁止清單應反映成功操作，並要用相同的介面、scope、controller 與 UUID 選擇比較。 <a class="qa-rule-link" href="#common-lockdown_op-10">本冊完整規則</a></p>
</li>
<li id="q-242-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Lockdown 命令本身不是專用的標準 PEL 事件。 <a class="qa-rule-link" href="#common-lockdown_op-11">本冊完整規則</a></p>
</li>
<li id="q-242-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>成功建立的禁止狀態不因一般 CLR 解除；要允許命令，需合法的後續 Lockdown 操作，或符合指定的 power-cycle 解除條件。 <a class="qa-rule-link" href="#common-lockdown_op-12">本冊完整規則</a></p>
</li>
<li id="q-242-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 不等於 Power Cycle，不能用它自動解除禁止。 <a class="qa-rule-link" href="#common-lockdown_op-13">本冊完整規則</a></p>
</li>
<li id="q-242-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>CSEL=0 的 subsystem 禁止，LDPE=1 時跨 Power Cycle 保留，直到後續操作解除；LDPE=0 則在 Power Cycle 解除。 <a class="qa-rule-link" href="#common-lockdown_op-14">本冊完整規則</a></p>
</li>
<li id="q-242-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>CSEL 選全部、指定 controller 或指定 primary 的 secondary 群組；IFC 選收命令介面。 <a class="qa-rule-link" href="#common-lockdown_op-15">本冊完整規則</a></p>
</li>
<li id="q-242-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>一個 FID 被禁止是阻止 Set，不是同時禁止 Get；也不等於 Set Features 全部 Opcode 被禁止。</p>
</li>
<li id="q-242-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先核對 SCP、OFI、CSEL、CSS 與 IFC 五個選擇是否對到同一個測試目標。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-243" data-question="243"><h2><a class="qa-qid" href="#q-243">Q243</a> 執行被 Lockdown 禁止的命令或 Feature 應如何回應？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-243-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-243-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>成功設下禁止後，還要驗證目標操作真的被阻擋，不能只看到設定命令成功就結束。</p>
</li>
<li id="q-243-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>條件包含目標 controller、收到命令的介面、Opcode 或 Set FID，以及適用 UUID。</p>
</li>
<li id="q-243-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>讀目前禁止清單，並確認原 Lockdown 的 CQE 與所選範圍。</p>
</li>
<li id="q-243-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Admin SQ 上收到符合禁止條件的命令，必須中止並回 Command Prohibited by Command and Feature Lockdown，SCT=0、SC=23h。</p>
</li>
<li id="q-243-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先成功建立禁止，再送一筆其餘參數合法的目標命令，最後查 CQE 及操作是否未執行。</p>
</li>
<li id="q-243-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>驗證中的預期成功，是禁止生效而目標命令被拒絕；不是要求目標也回 Successful Completion。</p>
</li>
<li id="q-243-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>Lockdown 命令自己不被支援或參數非法，與已禁止的目標命令被拒絕，是不同 Status。Personality 的 CDP Authentication 明定例外也要保留。</p>
</li>
<li id="q-243-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-243-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Lockdown 成功不定義一個一般性的設定完成 AER。 <a class="qa-rule-link" href="#common-lockdown_op-9">本冊完整規則</a></p>
</li>
<li id="q-243-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Lockdown Log 的目前禁止清單應反映成功操作，並要用相同的介面、scope、controller 與 UUID 選擇比較。 <a class="qa-rule-link" href="#common-lockdown_op-10">本冊完整規則</a></p>
</li>
<li id="q-243-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Lockdown 命令本身不是專用的標準 PEL 事件。 <a class="qa-rule-link" href="#common-lockdown_op-11">本冊完整規則</a></p>
</li>
<li id="q-243-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>成功建立的禁止狀態不因一般 CLR 解除；要允許命令，需合法的後續 Lockdown 操作，或符合指定的 power-cycle 解除條件。 <a class="qa-rule-link" href="#common-lockdown_op-12">本冊完整規則</a></p>
</li>
<li id="q-243-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 不等於 Power Cycle，不能用它自動解除禁止。 <a class="qa-rule-link" href="#common-lockdown_op-13">本冊完整規則</a></p>
</li>
<li id="q-243-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>CSEL=0 的 subsystem 禁止，LDPE=1 時跨 Power Cycle 保留，直到後續操作解除；LDPE=0 則在 Power Cycle 解除。 <a class="qa-rule-link" href="#common-lockdown_op-14">本冊完整規則</a></p>
</li>
<li id="q-243-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>CSEL 選全部、指定 controller 或指定 primary 的 secondary 群組；IFC 選收命令介面。 <a class="qa-rule-link" href="#common-lockdown_op-15">本冊完整規則</a></p>
</li>
<li id="q-243-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>LDPE 啟用且符合 authenticated unfreeze 支援條件時，指定 CDP Authentication 的 Security Send／Receive 必須允許，即使先前被禁止。</p>
</li>
<li id="q-243-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否測到錯誤介面、錯誤 controller，或規範明定的允許例外。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-244" data-question="244"><h2><a class="qa-qid" href="#q-244">Q244</a> Lockdown Log 的一般與增強格式如何解讀？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-244-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-244-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Log 分開回報「可以禁止」與「目前禁止」，這兩份清單不能互換。</p>
</li>
<li id="q-244-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>一般格式的部分清單描述全體 controller；增強格式可指定單台或以 FFFFh 彙整至少一台回報的項目。</p>
</li>
<li id="q-244-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>查 CFLS、CCFLS；ELPF=1 需要 controller-scoped 支援，LSI.CNTLID 只在增強格式使用。</p>
</li>
<li id="q-244-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>LSP.CNTTS=0 可禁止、1 Admin 已禁止、2 帶外已禁止；SCP 選 Opcode／FID。一般 LNGTH 是 bytes 數；增強依 SZE、NCFID、CFIDS 解析 descriptors。</p>
</li>
<li id="q-244-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先確定查詢條件，再檢查 Header 回報的 CS／SS。增強 FFFFh 清單中 ACNTL=1 表示全體，0 表示至少一台但非全體。</p>
</li>
<li id="q-244-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例如兩台中只有 controller1 禁止 FID12h，增強彙整可列它且 ACNTL=0；不能因此說「沒有禁止」。</p>
</li>
<li id="q-244-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援 CCFLS 卻要求增強格式須 Invalid Field；不能把每份增強 Log 固定當成 512 bytes。</p>
</li>
<li id="q-244-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-244-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Lockdown 成功不定義一個一般性的設定完成 AER。 <a class="qa-rule-link" href="#common-lockdown_op-9">本冊完整規則</a></p>
</li>
<li id="q-244-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Lockdown Log 的目前禁止清單應反映成功操作，並要用相同的介面、scope、controller 與 UUID 選擇比較。 <a class="qa-rule-link" href="#common-lockdown_op-10">本冊完整規則</a></p>
</li>
<li id="q-244-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Lockdown 命令本身不是專用的標準 PEL 事件。 <a class="qa-rule-link" href="#common-lockdown_op-11">本冊完整規則</a></p>
</li>
<li id="q-244-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>成功建立的禁止狀態不因一般 CLR 解除；要允許命令，需合法的後續 Lockdown 操作，或符合指定的 power-cycle 解除條件。 <a class="qa-rule-link" href="#common-lockdown_op-12">本冊完整規則</a></p>
</li>
<li id="q-244-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 不等於 Power Cycle，不能用它自動解除禁止。 <a class="qa-rule-link" href="#common-lockdown_op-13">本冊完整規則</a></p>
</li>
<li id="q-244-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>CSEL=0 的 subsystem 禁止，LDPE=1 時跨 Power Cycle 保留，直到後續操作解除；LDPE=0 則在 Power Cycle 解除。 <a class="qa-rule-link" href="#common-lockdown_op-14">本冊完整規則</a></p>
</li>
<li id="q-244-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>CSEL 選全部、指定 controller 或指定 primary 的 secondary 群組；IFC 選收命令介面。 <a class="qa-rule-link" href="#common-lockdown_op-15">本冊完整規則</a></p>
</li>
<li id="q-244-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>以特定 controller 查詢驗證彙整清單，再比較實際命令，避免把聯集誤看成交集。</p>
</li>
<li id="q-244-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查 ELPF 與 CNTLID，確認使用的是哪一種全體／部分語意。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-245" data-question="245"><h2><a class="qa-qid" href="#q-245">Q245</a> Reset 與 Power Cycle 後 Lockdown 是否保留？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-245-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-245-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>持續性取決於 CSEL 與 Lockdown Persistence，不能只用「Lockdown 已啟用」一個布林值判斷。</p>
</li>
<li id="q-245-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>先區分 subsystem 禁止與指定 controller／secondary 群組禁止。</p>
</li>
<li id="q-245-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>保存原 Lockdown 的 CSEL、PRHBT、IFC 與目標，並讀 Personality 的實際 LDPS。</p>
</li>
<li id="q-245-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>LDPE 是設定輸入，LDPS 是回覆狀態；前者寫入不等於後者必然已成功生效。</p>
</li>
<li id="q-245-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>重設前讀清單，執行指定種類的 Reset 或 Power Cycle，再以相同 selector 讀回並驗證目標命令。</p>
</li>
<li id="q-245-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>一般 Reset 保留禁止；Power Cycle 後 CSEL0 依 LDPS 保留或解除，CSEL1／2 不取得跨斷電持續性。</p>
</li>
<li id="q-245-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不能因 Subsystem Reset 沒解除就當作失敗，也不能因 LDPE=1 就要求所有 controller-scoped 禁止跨斷電存在。</p>
</li>
<li id="q-245-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-245-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Lockdown 成功不定義一個一般性的設定完成 AER。 <a class="qa-rule-link" href="#common-lockdown_op-9">本冊完整規則</a></p>
</li>
<li id="q-245-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>Lockdown Log 的目前禁止清單應反映成功操作，並要用相同的介面、scope、controller 與 UUID 選擇比較。 <a class="qa-rule-link" href="#common-lockdown_op-10">本冊完整規則</a></p>
</li>
<li id="q-245-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>Lockdown 命令本身不是專用的標準 PEL 事件。 <a class="qa-rule-link" href="#common-lockdown_op-11">本冊完整規則</a></p>
</li>
<li id="q-245-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>成功建立的禁止狀態不因一般 CLR 解除；要允許命令，需合法的後續 Lockdown 操作，或符合指定的 power-cycle 解除條件。 <a class="qa-rule-link" href="#common-lockdown_op-12">本冊完整規則</a></p>
</li>
<li id="q-245-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>Subsystem Reset 不等於 Power Cycle，不能用它自動解除禁止。 <a class="qa-rule-link" href="#common-lockdown_op-13">本冊完整規則</a></p>
</li>
<li id="q-245-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>CSEL=0 的 subsystem 禁止，LDPE=1 時跨 Power Cycle 保留，直到後續操作解除；LDPE=0 則在 Power Cycle 解除。 <a class="qa-rule-link" href="#common-lockdown_op-14">本冊完整規則</a></p>
</li>
<li id="q-245-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>CSEL 選全部、指定 controller 或指定 primary 的 secondary 群組；IFC 選收命令介面。 <a class="qa-rule-link" href="#common-lockdown_op-15">本冊完整規則</a></p>
</li>
<li id="q-245-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>同時核對範圍、實際 personality 狀態與重設種類，才能得出唯一預期。</p>
</li>
<li id="q-245-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否把 Controller Reset、Subsystem Reset 與真的斷電混稱為 Reset。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-security">Base 2.4 §5.2.28–5.2.29</a> · <a href="#ref-lockdown">Base 2.4 §5.2.16, 8.1.5</a> · <a href="#ref-locklog">Base 2.4 §5.2.13.1.20</a> · <a href="#ref-lockpersist">Base 2.4 §5.2.30.1.25.4–5.2.30.1.25.4.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-command-8"><h3>命令完成、事件與紀錄 · DNR 與 More 應如何設定？</h3><p>只有收到 CQE，才有 DNR 與 More 可供判讀。DNR=1 表示相同命令即使重送到此 NVM subsystem 的任一 controller，仍預期會失敗；DNR=0 則只表示可能成功。除非個別錯誤條件另有明定，不能只看 Status 名稱就要求 DNR=1。More=1 表示 Error Information Log 有這筆命令的補充資訊。SCT=SC=0 時，DNR 應為 0。</p></article>
<article id="common-lockdown_op-9"><h3>本主題的共用條件 · 是否產生 Asynchronous Event？</h3><p>Lockdown 成功不定義一個一般性的設定完成 AER。Host 應用 Lockdown Log 與目標命令結果確認；其他獨立事件才依其通知規則處理。</p></article>
<article id="common-lockdown_op-10"><h3>本主題的共用條件 · 是否更新 Error Information Log 或其他 Log？</h3><p>Lockdown Log 的目前禁止清單應反映成功操作，並要用相同的介面、scope、controller 與 UUID 選擇比較。被禁止命令的錯誤 CQE 則另依 Error Information 記錄規則關聯。</p></article>
<article id="common-lockdown_op-11"><h3>本主題的共用條件 · 是否記錄於 Persistent Event Log？</h3><p>Lockdown 命令本身不是專用的標準 PEL 事件。若另外修改 Lockdown Persistence Personality，須按其支援的 personality 事件規則判斷，不能把兩個操作混成同一筆紀錄。</p></article>
<article id="common-lockdown_op-12"><h3>本主題的共用條件 · Controller Reset 後是否保留或繼續？</h3><p>成功建立的禁止狀態不因一般 CLR 解除；要允許命令，需合法的後續 Lockdown 操作，或符合指定的 power-cycle 解除條件。</p></article>
<article id="common-lockdown_op-13"><h3>本主題的共用條件 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>Subsystem Reset 不等於 Power Cycle，不能用它自動解除禁止。仍要保留相同 scope 的狀態，並考慮 personality 明定的例外。</p></article>
<article id="common-lockdown_op-14"><h3>本主題的共用條件 · Power Cycle 後是否保留或繼續？</h3><p>CSEL=0 的 subsystem 禁止，LDPE=1 時跨 Power Cycle 保留，直到後續操作解除；LDPE=0 則在 Power Cycle 解除。CSEL=1／2 的禁止到 Power Cycle 為止，不因 LDPE=1 就取得跨斷電持續性。</p></article>
<article id="common-lockdown_op-15"><h3>本主題的共用條件 · 是否影響其他 Controller 或 Namespace？</h3><p>CSEL 選全部、指定 controller 或指定 primary 的 secondary 群組；IFC 選收命令介面。禁止一個介面不表示其他介面也被禁止；FID scope 只限制對該 FID 的 Set Features，不能誤當成 Get 也自動禁止。</p></article>
<article id="common-security_op-9"><h3>本主題的共用條件 · 是否產生 Asynchronous Event？</h3><p>Security Send／Receive 的一般資料交換不定義統一成功 AER。若所選協定或其他功能造成特定狀態變化，須依該功能另行確認；不能自行編造「認證完成」NVMe 事件。</p></article>
<article id="common-security_op-10"><h3>本主題的共用條件 · 是否更新 Error Information Log 或其他 Log？</h3><p>先分開 NVMe CQE 與安全協定回覆：CQE 說明命令傳輸／處理，Security Receive 的 payload 才依協定描述安全操作結果。Error Information 仍依 NVMe 錯誤記錄條件處理。</p></article>
<article id="common-security_op-11"><h3>本主題的共用條件 · 是否記錄於 Persistent Event Log？</h3><p>Security 資料交換不是 PEL 的通用逐命令稽核紀錄。若裝置支援 TCG-defined 或其他相關事件，需使用該事件的實際定義；三份 NVMe 規格不足以自行定義外部安全協定內容。</p></article>
<article id="common-security_op-12"><h3>本主題的共用條件 · Controller Reset 後是否保留或繼續？</h3><p>CLR 後 Security Receive 待取的結果可能不保留。安全鎖定、認證 session 與金鑰的持續性由所選協定決定，不能把失去傳輸結果解讀成自動解鎖或清除金鑰。</p></article>
<article id="common-security_op-13"><h3>本主題的共用條件 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>Subsystem Reset 後重新確認通訊及協定狀態。NVMe Base 不給所有 Security Protocol 一個共同的認證或鎖定保留答案，因此測試須先指定協定與狀態。</p></article>
<article id="common-security_op-14"><h3>本主題的共用條件 · Power Cycle 後是否保留或繼續？</h3><p>Power Cycle 後不能只因 NVMe queues 已重建，就推論安全狀態回到未鎖定。以協定的持久設定、session 規則與查詢結果判斷；未指定協定時，結論只能是 NVMe 三份來源未定義。</p></article>
<article id="common-security_op-15"><h3>本主題的共用條件 · 是否影響其他 Controller 或 Namespace？</h3><p>資料經目標 controller 傳送，但安全操作可能影響一個範圍、namespace 或整個 subsystem；真正範圍由 SECP、SPSP 與 payload 指定的協定決定，不能只看 Admin Queue 所屬 controller。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-locklog"><strong>Base 2.4 · §5.2.13.1.20</strong><br>文件頁 279–283 · PDF 305–309 · Figure 274–278</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>文件頁 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-lockdown"><strong>Base 2.4 · §5.2.16, 8.1.5</strong><br>文件頁 405–408, 597–599 · PDF 431–434, 623–625 · Figure 365–367</li>
<li id="ref-security"><strong>Base 2.4 · §5.2.28–5.2.29</strong><br>文件頁 454–456 · PDF 480–482 · Figure 456–462</li>
<li id="ref-lockpersist"><strong>Base 2.4 · §5.2.30.1.25.4–5.2.30.1.25.4.1</strong><br>文件頁 493–494 · PDF 519–520 · Figure 518–519</li>
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
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/security/en/">English</a><a href="/DOCS/nvme-question-bank/security.html">繁中教學 HTML</a></nav>
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
