---
layout: post
title: "NVMe 自問自答題庫：Identify 與能力探索"
date: 2026-10-01 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/identify/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/identify/en/">English</a><a href="/DOCS/nvme-question-bank/identify.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–320</p>
<header><p class="qa-range">Q44–Q53</p><h1>Identify 與能力探索</h1><p class="qr-intro">Identify 提供多種查詢結構。先確定要查哪個物件、需要哪一種資訊，再選擇 CNS、CSI、NSID 及其他欄位。本冊分別說明能力、目前配置與清單變更，讓你知道不同回覆如何互相補充，以及哪些差異才可能構成矛盾。</p><p>先練習，再展開每題的 17 項解答。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>先選問題，再選 Identify 結構</h2><p class="qa-takeaway">每個 CNS 回答的問題不同。namespace 已配置，只表示它存在，不能直接推論目前這個 controller 已能存取它。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">想知道什麼</th><th scope="col">查詢入口</th><th scope="col">回覆如何使用</th></tr></thead><tbody><tr><td>controller 宣告的能力</td><td>CNS=01h</td><td>讀取 OACS、ONCS、MDTS 等欄位，並依各欄位的有效條件判讀</td></tr><tr><td>目前可存取的 namespaces</td><td>CNS=02h</td><td>取得此 controller 的 Active List；這不是全部已配置 namespace 的清單</td></tr><tr><td>已配置的 namespaces</td><td>支援 Namespace Management 時用 CNS=10h</td><td>清單可包含未 attach 到此 controller 的 namespace</td></tr><tr><td>單一 NVM namespace 的格式</td><td>CNS=00h；需要時加 CNS=05h、CSI=00h</td><td>NSZE／NCAP、FLBAS、LBAF 與 PI 格式共同解讀</td></tr><tr><td>不依賴命令集的 namespace 屬性</td><td>CNS=08h</td><td>使用此結構解讀共通屬性，不要套用 NVM 特定 LBA 格式結構的欄位位置</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>假設 Allocated List={1,2}，而目前 controller 的 Active List={1}。這表示 namespace 2 不在此 controller 的 Active List 中，但不能據此判定它已被刪除。下一步應確認附加關係及適用狀態，並保留 controller 身分與查詢時間，讓前後資料可以正確比較。</p>
<p class="qa-citations">來源：<a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-nsmanage">Base 2.4 §5.2.24–5.2.25, 8.1.17</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-044">Q44 · Identify Controller 與 Identify Namespace 分別提供哪些重要資訊？</a></li>
<li><a href="#q-045">Q45 · Active Namespace ID List、Allocated Namespace ID List 及 Namespace Descriptor List 有什麼差異？</a></li>
<li><a href="#q-046">Q46 · Controller List、UUID List 及 I/O Command Set Identify 資料分別有什麼用途？</a></li>
<li><a href="#q-047">Q47 · NVM Set、Endurance Group、Domain 及 Secondary Controller 資訊應從哪種 Identify 資料取得？</a></li>
<li><a href="#q-048">Q48 · CNS、CSI、NSID 或 UUID Index 不支援或不合法時，Controller 應如何回應？</a></li>
<li><a href="#q-049">Q49 · Serial Number、Model Number、Firmware Revision、MDTS 及 Optional Admin Command 欄位應如何解讀？</a></li>
<li><a href="#q-050">Q50 · Identify 宣告支援某功能後，應如何透過對應 Command 及 Commands Supported and Effects Log 驗證？</a></li>
<li><a href="#q-051">Q51 · Namespace 建立、刪除、Attach、Detach 或 Format 後，哪些 Identify 資料與 Namespace List 應更新？</a></li>
<li><a href="#q-052">Q52 · Firmware Activation、Reset 及 Power Cycle 後，哪些 Identify 資料可能改變，哪些應保持不變？</a></li>
<li><a href="#q-053">Q53 · Identify、Feature、Log Page 與實際 Command 行為不一致時，應如何定位問題？</a></li>
</ol></section>
<article class="qa-question" id="q-044" data-question="44"><h2><a class="qa-qid" href="#q-044">Q44</a> Identify Controller 與 Identify Namespace 分別提供哪些重要資訊？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-044-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-044-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Identify Controller 用來了解 controller 支援哪些能力；Identify Namespace 則用來了解指定 namespace 的容量、格式及資料保護設定。先分清楚查詢對象，才知道該讀哪一組欄位。</p>
</li>
<li id="q-044-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Identify Controller 以接收命令的 controller 為查詢入口。Namespace 資料則要搭配 NSID、CNS 及 CSI，確認要查的是哪個 namespace，以及哪一種資料結構。</p>
</li>
<li id="q-044-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>基本查詢入口是 CNS01h 的 Controller 資料，以及 CNS00h 的 NVM Namespace 資料。CNS05h／06h 查詢命令集特定的補充結構，CNS08h 則提供不依賴特定命令集的 Namespace 資料。</p>
</li>
<li id="q-044-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>Controller 看 SN、MN、FR、MDTS、OACS、ONCS、LPA、SQES／CQES；NVM Namespace 看 NSZE／NCAP／NUSE、FLBAS／LBAF、MC／DPC／DPS、原子性及群組識別。</p>
</li>
<li id="q-044-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先查 Controller 資料及 Active Namespace ID List，再逐一查詢各 namespace 適用的資料結構。計算容量時，使用目前選定的 LBA format，將 block 數換算成 bytes。</p>
</li>
<li id="q-044-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Identify 回傳 4096-byte 結構與成功 CQE。例：NSZE=8192、LBADS=12，邏輯位址空間為 8192×4096=32 MiB。</p>
</li>
<li id="q-044-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援 CNS 時，回報 Invalid Field（0/02h）；namespace 所屬命令集不支援該 CNS 時，回報 Invalid I/O Command Set（1/2Ch）。至於 NSID 是否合法，則依該 CNS 的使用規則判斷。</p>
</li>
<li id="q-044-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-044-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>正常完成不保證會回報非同步事件。若另有事件發生，還須確認支援能力、通知設定，以及是否有等待中的 AER。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-044-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>依完成結果與記錄條件核對 Error Information，不能直接用失敗命令的數量推算新增 entry 數。完整條件見本冊共用規則。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-044-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>PEL 記錄符合條件的事件，不是每條命令的執行歷史。只有事件受支援且符合記錄條件時，才依規則要求新增紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-044-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>查詢若因重設中止，恢復後須重新送出。比較回覆時，再逐欄區分固定身分、配置與動態狀態。 <a class="qa-rule-link" href="#common-identify-12">本冊完整規則</a></p>
</li>
<li id="q-044-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>重設後重新查詢受影響的物件。重設本身不表示 namespace 已刪除，也不表示配置已恢復出廠值。 <a class="qa-rule-link" href="#common-identify-13">本冊完整規則</a></p>
</li>
<li id="q-044-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新查詢並比較。若期間還有韌體啟用或管理操作，必須分清楚差異是由哪個事件造成。 <a class="qa-rule-link" href="#common-identify-14">本冊完整規則</a></p>
</li>
<li id="q-044-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Identify 是唯讀查詢。不同 controller 的 Active List 可能不同，因此比較時必須確認查詢對象。 <a class="qa-rule-link" href="#common-identify-15">本冊完整規則</a></p>
</li>
<li id="q-044-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>controller 宣告支援某個命令，不代表每個 namespace 都具備適合的格式，或目前都能由此 controller 存取。因此，驗證時必須同時確認 controller 能力與目標 namespace 的條件。</p>
</li>
<li id="q-044-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認 buffer 是由哪個 CNS 回傳，再使用對應的結構解碼。例如，不能將 CNS08h 的回傳資料當成 CNS00h 的格式讀取。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-045" data-question="45"><h2><a class="qa-qid" href="#q-045">Q45</a> Active Namespace ID List、Allocated Namespace ID List 及 Namespace Descriptor List 有什麼差異？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-045-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-045-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這三種查詢分別回答：哪些 namespace 可由此 controller 使用、哪些 namespace 已經配置，以及某個 namespace 有哪些識別資料。它們不是同一份清單的不同名稱。</p>
</li>
<li id="q-045-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Active List 反映此 controller 可使用的 namespace；Allocated List 可以包含已配置但尚未附加的 namespace。Descriptor List 則不是 namespace 名單，而是單一 NSID 的識別屬性集合。</p>
</li>
<li id="q-045-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>CNS02h 查詢 Active List，CNS10h 查詢 Allocated List，CNS03h 查詢 Namespace Identification Descriptor List。使用 Allocated List 查詢前，還要確認 Namespace Management 支援能力。</p>
</li>
<li id="q-045-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>查詢 ID List 時，NSID 是分頁的起點，回傳清單列出大於該起點的 ID。Descriptor 則透過 NIDT、NIDL、NID 描述識別資料，例如 EUI64、NGUID、UUID 或 CSI；它不是用來列出其他 namespace。</p>
</li>
<li id="q-045-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>讀取 ID List 時，先以 NSID=0 查詢，再依回傳的遞增 ID 繼續讀取下一批。查詢 Descriptor List 時，NSID 改為指定要查的 namespace。因此，同一個 NSID 欄位在這兩類查詢中的用途不同。</p>
</li>
<li id="q-045-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例如 Allocated={1,3,8}，而 Active={1,8}，表示 namespace 3 已配置，但目前不在此 controller 的 Active List 中。這個差異本身不代表 namespace 3 已損壞。</p>
</li>
<li id="q-045-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>CNS02h 或 CNS10h 若將起點設為 FFFFFFFEh 或 FFFFFFFFh，必須回報 Invalid Namespace or Format（0/0Bh）。若問題是 controller 不支援所選 CNS，則回報 0/02h。</p>
</li>
<li id="q-045-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-045-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>正常完成不保證會回報非同步事件。若另有事件發生，還須確認支援能力、通知設定，以及是否有等待中的 AER。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-045-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>依完成結果與記錄條件核對 Error Information，不能直接用失敗命令的數量推算新增 entry 數。完整條件見本冊共用規則。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-045-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>PEL 記錄符合條件的事件，不是每條命令的執行歷史。只有事件受支援且符合記錄條件時，才依規則要求新增紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-045-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>查詢若因重設中止，恢復後須重新送出。比較回覆時，再逐欄區分固定身分、配置與動態狀態。 <a class="qa-rule-link" href="#common-identify-12">本冊完整規則</a></p>
</li>
<li id="q-045-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>重設後重新查詢受影響的物件。重設本身不表示 namespace 已刪除，也不表示配置已恢復出廠值。 <a class="qa-rule-link" href="#common-identify-13">本冊完整規則</a></p>
</li>
<li id="q-045-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新查詢並比較。若期間還有韌體啟用或管理操作，必須分清楚差異是由哪個事件造成。 <a class="qa-rule-link" href="#common-identify-14">本冊完整規則</a></p>
</li>
<li id="q-045-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Identify 是唯讀查詢。不同 controller 的 Active List 可能不同，因此比較時必須確認查詢對象。 <a class="qa-rule-link" href="#common-identify-15">本冊完整規則</a></p>
</li>
<li id="q-045-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>跨時間比對 namespace 時，使用 Descriptor 提供的穩定識別資料，不要假設 NSID 永遠不變。如果分頁讀取期間發生配置變更，則需重新取得彼此一致的清單內容。</p>
</li>
<li id="q-045-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認 NSID 在此次命令中代表目標，還是「從這個 ID 之後開始列」。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-046" data-question="46"><h2><a class="qa-qid" href="#q-046">Q46</a> Controller List、UUID List 及 I/O Command Set Identify 資料分別有什麼用途？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-046-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-046-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這些資料分別回答三個問題：哪些 controller 與 namespace 有存取關係、應使用哪一套廠商定義解讀資料，以及哪些 I/O command sets 可以同時使用。</p>
</li>
<li id="q-046-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Controller List 描述 controller 的名單或附加關係。UUID List 則讓 Host 選擇廠商特定資料所使用的定義；它與 namespace 自身的 UUID Descriptor 是不同資訊。</p>
</li>
<li id="q-046-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>CNS12h 查某 namespace 附加的 controllers，13h 查 subsystem I/O controllers，17h 查 UUID List，1Ch 查 command-set combinations。</p>
</li>
<li id="q-046-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CNTID 的用途取決於 CNS，可能是清單的查詢起點，也可能指定目標 controller。UIDX=0 表示不指定 UUID。CNS1Ch 回傳的每個 vector，則表示一組可同時使用的 CSI。</p>
</li>
<li id="q-046-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先依查詢目的選擇 CNS，再設定它使用的選擇欄位。若從 CNS1Ch 選定一組命令集組合，設定 FID19h 時，IOCSCI 要填該組合的索引，不能直接填入 CSI bitmap。</p>
</li>
<li id="q-046-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Controller List 回傳 controller 識別值及數量；UUID List 回傳依規定順序排列的 entries；命令集組合 vectors 則列出 Host 可選的配置。查到某個組合，不表示它已自動啟用。</p>
</li>
<li id="q-046-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援 CNS 時，回報 0/02h；CNS12h 使用 NSID=FFFFFFFFh 時，也回報 0/02h。UUID 選擇錯誤則依 §8.1.31 判斷，不能一律解釋為 namespace 不存在。</p>
</li>
<li id="q-046-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-046-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>正常完成不保證會回報非同步事件。若另有事件發生，還須確認支援能力、通知設定，以及是否有等待中的 AER。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-046-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>依完成結果與記錄條件核對 Error Information，不能直接用失敗命令的數量推算新增 entry 數。完整條件見本冊共用規則。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-046-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>PEL 記錄符合條件的事件，不是每條命令的執行歷史。只有事件受支援且符合記錄條件時，才依規則要求新增紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-046-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>查詢若因重設中止，恢復後須重新送出。比較回覆時，再逐欄區分固定身分、配置與動態狀態。 <a class="qa-rule-link" href="#common-identify-12">本冊完整規則</a></p>
</li>
<li id="q-046-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>重設後重新查詢受影響的物件。重設本身不表示 namespace 已刪除，也不表示配置已恢復出廠值。 <a class="qa-rule-link" href="#common-identify-13">本冊完整規則</a></p>
</li>
<li id="q-046-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新查詢並比較。若期間還有韌體啟用或管理操作，必須分清楚差異是由哪個事件造成。 <a class="qa-rule-link" href="#common-identify-14">本冊完整規則</a></p>
</li>
<li id="q-046-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Identify 是唯讀查詢。不同 controller 的 Active List 可能不同，因此比較時必須確認查詢對象。 <a class="qa-rule-link" href="#common-identify-15">本冊完整規則</a></p>
</li>
<li id="q-046-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>先核對 CNTID 與 NSID 在所選 CNS 中各自的用途，不要把 Controller List 當成 Active Namespace ID List。設定命令集組合後，另以 FID19h 的 Current 值確認是否選到預期的 vector。</p>
</li>
<li id="q-046-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認 UIDX 填的是 UUID List 的索引。它不是 UUID 本身，也不是 namespace ID。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-uuid">Base 2.4 §8.1.31.1–8.1.31.2</a> · <a href="#ref-profile">Base 2.4 §5.2.30.1.18</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-047" data-question="47"><h2><a class="qa-qid" href="#q-047">Q47</a> NVM Set、Endurance Group、Domain 及 Secondary Controller 資訊應從哪種 Identify 資料取得？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-047-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-047-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>這些 Identify 資料用來建立資源歸屬關係。NVM Set、Endurance Group、Domain 與 controller 分別描述不同的管理對象，不能當成同一層的物件。</p>
</li>
<li id="q-047-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>每種清單都有自己的 ID、容量或資源欄位。本題著重查明它們的關係與屬性，不涉及修改容量配置或虛擬化資源。</p>
</li>
<li id="q-047-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先查 CTRATT 的相關能力與 OACS.VMS；CNS04h、19h、18h、14h／15h 分別對應 Set、Endurance Group、Domain、Primary／Secondary Controller。</p>
</li>
<li id="q-047-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>NVM Set Attributes 透過 ENDGID 表示所屬 Endurance Group；Namespace 資料則提供 NVMSETID 與 ENDGID。Domain entry 的 DID、TDC、UDC 用來描述識別及容量；Secondary Controller entry 的 SCID、PCID、狀態及 VQ／VI 數量，則用來描述 controller 關係與資源。</p>
</li>
<li id="q-047-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先由 namespace 的群組識別資料，查出對應的 NVM Set 與 Endurance Group。再利用 Domain List 確認容量歸屬，並透過 Primary Controller Capabilities 及 Secondary Controller List，了解 queue 與 interrupt 資源的配置。</p>
</li>
<li id="q-047-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>成功查詢後，應取得能互相對應的 ID 與屬性。但欄位為零不一定表示資源數量為零；必須先確認相關能力受支援，而且這個欄位在目前配置下有效。</p>
</li>
<li id="q-047-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援的 CNS 回報 0/02h。某些清單查詢若將起點設在目前最大 ID 之後，則會回傳空清單；不能只因沒有 entry，就要求 controller 回報錯誤。</p>
</li>
<li id="q-047-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-047-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>正常完成不保證會回報非同步事件。若另有事件發生，還須確認支援能力、通知設定，以及是否有等待中的 AER。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-047-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>依完成結果與記錄條件核對 Error Information，不能直接用失敗命令的數量推算新增 entry 數。完整條件見本冊共用規則。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-047-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>PEL 記錄符合條件的事件，不是每條命令的執行歷史。只有事件受支援且符合記錄條件時，才依規則要求新增紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-047-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>查詢若因重設中止，恢復後須重新送出。比較回覆時，再逐欄區分固定身分、配置與動態狀態。 <a class="qa-rule-link" href="#common-identify-12">本冊完整規則</a></p>
</li>
<li id="q-047-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>重設後重新查詢受影響的物件。重設本身不表示 namespace 已刪除，也不表示配置已恢復出廠值。 <a class="qa-rule-link" href="#common-identify-13">本冊完整規則</a></p>
</li>
<li id="q-047-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新查詢並比較。若期間還有韌體啟用或管理操作，必須分清楚差異是由哪個事件造成。 <a class="qa-rule-link" href="#common-identify-14">本冊完整規則</a></p>
</li>
<li id="q-047-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Identify 是唯讀查詢。不同 controller 的 Active List 可能不同，因此比較時必須確認查詢對象。 <a class="qa-rule-link" href="#common-identify-15">本冊完整規則</a></p>
</li>
<li id="q-047-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>比對清單中的資源數、Number of Queues，以及實際可建立的 QID 與可用 IV。同時分清楚 Primary Controller 宣告的能力，與 Secondary Controller 已獲配置的資源，兩者不一定是相同數量。</p>
</li>
<li id="q-047-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認查詢是送到哪個 Primary Controller，再確認清單的查詢起點是否符合預期。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-048" data-question="48"><h2><a class="qa-qid" href="#q-048">Q48</a> CNS、CSI、NSID 或 UUID Index 不支援或不合法時，Controller 應如何回應？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-048-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-048-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Identify 失敗時，必須先看哪個選擇欄位不符合使用規則。CNS、CSI、NSID 與 UUID Index 的用途不同，不能將所有失敗都歸為 Invalid Namespace。</p>
</li>
<li id="q-048-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>相同的 NSID 或 CSI，用在不同 CNS 時，合法性可能不同。因此，測試某個欄位前，必須固定 CNS 及相關前提。</p>
</li>
<li id="q-048-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Figure 336 指定每個 CNS 是否使用 NSID、CNTID、CSI；UIDX 使用還受 UUID 選擇能力控制。</p>
</li>
<li id="q-048-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>CNS 不使用 CNTID 時，Host 將它清零，controller 忽略它。對不使用的 CSI，規範建議 Host 清零，並建議 controller 忽略；若 Host 填入非零值，controller 也可以回報 Invalid Field。</p>
</li>
<li id="q-048-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>驗證時先固定其他選擇欄位，每次只改動待測欄位。先列出所選 CNS 的專用規則，再用通用規則補足，避免忽略例外。</p>
</li>
<li id="q-048-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>有效查詢回傳 4096 bytes。例如，CNS11h 對符合定義的未配置 NSID，可以回傳全零資料；這與指定無效 NSID 而回報錯誤，是不同情況。</p>
</li>
<li id="q-048-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>不支援 CNS 時回報 0/02h；namespace 所屬命令集不支援該 CNS 時回報 1/2Ch；CNS02h／10h 使用非法的末端起點時回報 0/0Bh。如果命令使用 UUID 選擇，而 UIDX 指向不支援該資料的 UUID、全零 UUID 或 NVMe Invalid UUID，則必須回報 0/02h。CSI 的合法性則要看該 CNS 是否使用它，以及 namespace 所屬的命令集。</p>
</li>
<li id="q-048-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-048-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>正常完成不保證會回報非同步事件。若另有事件發生，還須確認支援能力、通知設定，以及是否有等待中的 AER。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-048-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>依完成結果與記錄條件核對 Error Information，不能直接用失敗命令的數量推算新增 entry 數。完整條件見本冊共用規則。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-048-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>PEL 記錄符合條件的事件，不是每條命令的執行歷史。只有事件受支援且符合記錄條件時，才依規則要求新增紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-048-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>查詢若因重設中止，恢復後須重新送出。比較回覆時，再逐欄區分固定身分、配置與動態狀態。 <a class="qa-rule-link" href="#common-identify-12">本冊完整規則</a></p>
</li>
<li id="q-048-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>重設後重新查詢受影響的物件。重設本身不表示 namespace 已刪除，也不表示配置已恢復出廠值。 <a class="qa-rule-link" href="#common-identify-13">本冊完整規則</a></p>
</li>
<li id="q-048-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新查詢並比較。若期間還有韌體啟用或管理操作，必須分清楚差異是由哪個事件造成。 <a class="qa-rule-link" href="#common-identify-14">本冊完整規則</a></p>
</li>
<li id="q-048-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Identify 是唯讀查詢。不同 controller 的 Active List 可能不同，因此比較時必須確認查詢對象。 <a class="qa-rule-link" href="#common-identify-15">本冊完整規則</a></p>
</li>
<li id="q-048-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>保留 CQE 及原命令的 CDW10、CDW11、CDW14。不同欄位錯誤都可能得到 0/02h，只有 Status 數值不足以指出是哪個參數造成失敗。</p>
</li>
<li id="q-048-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認這個 CNS 是否使用待測欄位。若規範要求或允許忽略該欄位，controller 沒有因它報錯，就不能直接判為漏做檢查。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-uuid">Base 2.4 §8.1.31.1–8.1.31.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-049" data-question="49"><h2><a class="qa-qid" href="#q-049">Q49</a> Serial Number、Model Number、Firmware Revision、MDTS 及 Optional Admin Command 欄位應如何解讀？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-049-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-049-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>Identify Controller 同時包含識別字串、傳輸限制及能力 bitmap。這些欄位的資料型態不同，必須各自解讀，不能全部當成一般整數。</p>
</li>
<li id="q-049-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>SN 與 MN 識別 NVM subsystem，FR 描述目前啟用的韌體版本。MDTS 限制單次資料傳輸大小，OACS 則宣告選配 Admin 功能的支援能力。</p>
</li>
<li id="q-049-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>CNS01h：SN bytes23:4、MN63:24、FR71:64、MDTS byte77、OACS bytes257:256。</p>
</li>
<li id="q-049-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>識別字串依 ASCII 解讀，並注意尾端的空白填補。MDTS 非零時，傳輸上限為 2^MDTS×2^(12+CAP.MPSMIN) bytes；計算使用 CAP.MPSMIN，不是 CC.MPS。MDTS=0 只表示此欄位不設定上限，命令本身仍可能有其他長度限制。</p>
</li>
<li id="q-049-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先確認回傳結構及欄位位置，再依資料型態分別讀取字串、能力位及指數編碼。計算傳輸長度時，另查 CTRATT.MEM，確認 metadata 是否計入限制。</p>
</li>
<li id="q-049-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>例如 MPSMIN=0、MDTS=5，傳輸上限為 128 KiB。若 MEM=0，傳送 32 個 4096-byte 資料區塊時，還要計入每塊 16-byte 的 metadata；加總後就超過 128 KiB。</p>
</li>
<li id="q-049-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>超過 MDTS 的命令回報 Invalid Field（0/02h）；不支援的選配 Opcode 通常回報 0/01h。NVMe 版本較新，不代表所有選配命令都必須支援。</p>
</li>
<li id="q-049-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-049-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>正常完成不保證會回報非同步事件。若另有事件發生，還須確認支援能力、通知設定，以及是否有等待中的 AER。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-049-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>依完成結果與記錄條件核對 Error Information，不能直接用失敗命令的數量推算新增 entry 數。完整條件見本冊共用規則。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-049-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>PEL 記錄符合條件的事件，不是每條命令的執行歷史。只有事件受支援且符合記錄條件時，才依規則要求新增紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-049-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>查詢若因重設中止，恢復後須重新送出。比較回覆時，再逐欄區分固定身分、配置與動態狀態。 <a class="qa-rule-link" href="#common-identify-12">本冊完整規則</a></p>
</li>
<li id="q-049-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>重設後重新查詢受影響的物件。重設本身不表示 namespace 已刪除，也不表示配置已恢復出廠值。 <a class="qa-rule-link" href="#common-identify-13">本冊完整規則</a></p>
</li>
<li id="q-049-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新查詢並比較。若期間還有韌體啟用或管理操作，必須分清楚差異是由哪個事件造成。 <a class="qa-rule-link" href="#common-identify-14">本冊完整規則</a></p>
</li>
<li id="q-049-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Identify 是唯讀查詢。不同 controller 的 Active List 可能不同，因此比較時必須確認查詢對象。 <a class="qa-rule-link" href="#common-identify-15">本冊完整規則</a></p>
</li>
<li id="q-049-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>將 FR 與 Firmware Slot Information 中目前 active slot 的版本比對，不要誤拿尚待啟用的 slot 比較。OACS 宣告的能力，則應與 Commands Supported and Effects Log 中對應命令的支援欄位一致。</p>
</li>
<li id="q-049-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查是否把 MDTS 的編碼直接當成 byte 數，或誤用目前的 CC.MPS 來計算傳輸上限。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-conventions">Base 2.4 §1.4.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-050" data-question="50"><h2><a class="qa-qid" href="#q-050">Q50</a> Identify 宣告支援某功能後，應如何透過對應 Command 及 Commands Supported and Effects Log 驗證？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-050-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-050-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>驗證能力時，要確認 Host 能在合法條件下使用該功能，不能只確認 Identify 的支援位為 1，就認定功能已驗證完成。</p>
</li>
<li id="q-050-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>查詢與測試應針對同一 controller、命令集及 namespace 配置，並注意資料取得的時間。不同配置或不同時點的結果，不能直接當成同一狀態比較。</p>
</li>
<li id="q-050-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>先查 Identify 的功能支援欄位，再確認 LPA.CELP。接著從 LID05h 選出正確的 Admin 或 I/O Opcode entry，讀取 CSUPP 與命令效果欄位。</p>
</li>
<li id="q-050-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>除了 CSUPP，還要讀取 LBCC、NCC、NIC、CCC、CSE 等欄位。它們用來說明命令可能如何影響資料、能力與 namespace 清單，以及執行時有哪些限制。</p>
</li>
<li id="q-050-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先確認合法前提與支援能力，準備好參數及資源，再執行命令。完成後檢查 CQE 與實際結果，並依 effects 欄位指出的變更，重新查詢可能受影響的資訊。</p>
</li>
<li id="q-050-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>宣告支援表示這項功能有合法的使用方式，不表示任何參數或任何狀態下都會成功。驗證成功時，也不能只看 CQE，還要確認命令產生了規範要求的效果。</p>
</li>
<li id="q-050-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>若回報 0/01h，可能與 Opcode 支援宣告矛盾。但若回報 0/02h、Namespace Not Ready，或受到 Lockdown 限制，則應先查參數與目前狀態，不能立即判定支援宣告錯誤。</p>
</li>
<li id="q-050-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-050-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>正常完成不保證會回報非同步事件。若另有事件發生，還須確認支援能力、通知設定，以及是否有等待中的 AER。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-050-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>依完成結果與記錄條件核對 Error Information，不能直接用失敗命令的數量推算新增 entry 數。完整條件見本冊共用規則。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-050-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>PEL 記錄符合條件的事件，不是每條命令的執行歷史。只有事件受支援且符合記錄條件時，才依規則要求新增紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-050-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>查詢若因重設中止，恢復後須重新送出。比較回覆時，再逐欄區分固定身分、配置與動態狀態。 <a class="qa-rule-link" href="#common-identify-12">本冊完整規則</a></p>
</li>
<li id="q-050-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>重設後重新查詢受影響的物件。重設本身不表示 namespace 已刪除，也不表示配置已恢復出廠值。 <a class="qa-rule-link" href="#common-identify-13">本冊完整規則</a></p>
</li>
<li id="q-050-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新查詢並比較。若期間還有韌體啟用或管理操作，必須分清楚差異是由哪個事件造成。 <a class="qa-rule-link" href="#common-identify-14">本冊完整規則</a></p>
</li>
<li id="q-050-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Identify 是唯讀查詢。不同 controller 的 Active List 可能不同，因此比較時必須確認查詢對象。 <a class="qa-rule-link" href="#common-identify-15">本冊完整規則</a></p>
</li>
<li id="q-050-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>Commands Supported and Effects Log 描述命令支援能力及可能影響，不是執行歷史。某個 entry 宣告命令受支援，不表示這條命令最近曾經執行過。</p>
</li>
<li id="q-050-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先檢查拿的是 Admin 還是 I/O opcode entry，以及 CSI 是否選對。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-effects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-051" data-question="51"><h2><a class="qa-qid" href="#q-051">Q51</a> Namespace 建立、刪除、Attach、Detach 或 Format 後，哪些 Identify 資料與 Namespace List 應更新？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-051-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-051-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>namespace 配置改變後，Host 必須重新取得受影響的資訊，才能避免沿用舊容量、舊格式或舊的附加關係。</p>
</li>
<li id="q-051-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>Create／Delete 改變 namespace 是否存在；Attach／Detach 改變 controller 是否能使用它；Format 則改變操作範圍內的資料格式。不同操作需要檢查的資料也不同。</p>
</li>
<li id="q-051-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>OACS.NMS 確認管理支援；Format 還看 OACS／FNA 及 NVM 支援格式。</p>
</li>
<li id="q-051-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>分別檢查 Allocated List、Active List、CNS12h 回傳的已附加 Controller List，以及 Namespace 資料中的 FLBAS、DPS、NSZE、NCAP 等欄位，不要期待每種操作都改變相同欄位。</p>
</li>
<li id="q-051-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先記錄操作前的資料，等待管理命令完成，再重新查詢受影響的清單及 namespace。尤其 Create 成功只表示 namespace 已建立，不表示它已自動附加到 controller。</p>
</li>
<li id="q-051-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>Create 後，namespace 應出現在 Allocated List；Attach 後，應出現在目標 controller 的 Active List。Detach 後，它會從該 Active List 移除，但仍可能留在 Allocated List。Format 後則要檢查選定格式是否正確，不能假設 NSID 必須改變。</p>
</li>
<li id="q-051-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>管理命令失敗時，不能直接假設所有資料都已更新，也不能假設完全沒有變動。先查該命令對失敗及部分完成的規則，再重新查詢實際狀態。</p>
</li>
<li id="q-051-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-051-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>Identify 查詢本身不產生變更事件。Create、Delete、Attach、Detach 或 Format 若改變 namespace 屬性，則依受影響對象、事件支援能力與 AEC 設定，判斷是否回報 Namespace Attribute Changed。不同 controller 看到的變更可能不同。</p>
</li>
<li id="q-051-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>將 Changed Namespace List（LID 04h）與重新讀取的 Identify 一起檢查。前者指出哪些 NSID 曾經變更，後者提供目前配置，兩者不能互相代替。讀取 Log 時的 RAE 會影響事件確認，因此先保存原事件與清單，再進行後續查詢。</p>
</li>
<li id="q-051-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>支援 PEL 時，Create／Delete 對應的 Change Namespace Event，與 Format Start／Completion 是不同事件。不能將 Attach／Detach 直接當成 Create／Delete 記錄；Identify 查詢本身也不要求新增這些事件。</p>
</li>
<li id="q-051-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>查詢若因重設中止，恢復後須重新送出。比較回覆時，再逐欄區分固定身分、配置與動態狀態。 <a class="qa-rule-link" href="#common-identify-12">本冊完整規則</a></p>
</li>
<li id="q-051-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>重設後重新查詢受影響的物件。重設本身不表示 namespace 已刪除，也不表示配置已恢復出廠值。 <a class="qa-rule-link" href="#common-identify-13">本冊完整規則</a></p>
</li>
<li id="q-051-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新查詢並比較。若期間還有韌體啟用或管理操作，必須分清楚差異是由哪個事件造成。 <a class="qa-rule-link" href="#common-identify-14">本冊完整規則</a></p>
</li>
<li id="q-051-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Identify 是唯讀查詢。不同 controller 的 Active List 可能不同，因此比較時必須確認查詢對象。 <a class="qa-rule-link" href="#common-identify-15">本冊完整規則</a></p>
</li>
<li id="q-051-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>將管理命令結果、相關清單、Namespace 資料結構，以及適用的 Changed Namespace 通知一起比對。事件用來通知變更，不能代替 Identify 所提供的完整配置資料。</p>
</li>
<li id="q-051-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認查詢送到的是受 Attach／Detach 影響的 controller，並確認前一筆管理命令已經完成，再解讀查詢結果。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idlist">Base 2.4 §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-nsmanage">Base 2.4 §5.2.24–5.2.25, 8.1.17</a> · <a href="#ref-effects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-nschange">Base 2.4 §5.2.13.1.5, 5.2.13.1.14.2.6–5.2.13.1.14.2.8</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-052" data-question="52"><h2><a class="qa-qid" href="#q-052">Q52</a> Firmware Activation、Reset 及 Power Cycle 後，哪些 Identify 資料可能改變，哪些應保持不變？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-052-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-052-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>是否允許 Identify 資料改變，要逐欄依性質判斷。不能將整個 4096-byte buffer 一律要求完全相同，因為其中包含動態狀態及可能更新的能力。</p>
</li>
<li id="q-052-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>可先分成固定身分、韌體宣告能力、持續配置與動態狀態四類。這四類資料允許改變的原因不同，因此比較時也要使用不同的判斷條件。</p>
</li>
<li id="q-052-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>保存 SN／MN、namespace 穩定識別、FR、能力位、容量／格式／附加關係及動態欄位作比較基準。</p>
</li>
<li id="q-052-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>FR 應描述目前已啟用的韌體；韌體更新後，MDTS 及能力位需要重新確認。NUSE 等動態數值則可能隨使用狀態改變，不能拿來當固定的裝置識別資料。</p>
</li>
<li id="q-052-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先記錄發生了哪些操作：只有 Reset 或 Power Cycle，還是同時有韌體啟用或管理配置變更。恢復後，使用相同的 CNS、NSID、CSI 查詢，再逐欄對照其保留及變更規則。</p>
</li>
<li id="q-052-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>一般 Reset 並不是重新命名裝置、刪除 namespace 或執行 Format。如果重設同時啟用了新韌體，則 FR 及規範允許隨之變更的能力，不能一律要求保留舊值。</p>
</li>
<li id="q-052-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>比較前後資料本身不會產生新的 CQE Status。如果重設後 Identify 失敗，應先分辨是初始化尚未完成、NSID 無效，還是 CNS 選錯，不能把所有差異都直接歸為韌體錯誤。</p>
</li>
<li id="q-052-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-052-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>正常完成不保證會回報非同步事件。若另有事件發生，還須確認支援能力、通知設定，以及是否有等待中的 AER。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-052-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>依完成結果與記錄條件核對 Error Information，不能直接用失敗命令的數量推算新增 entry 數。完整條件見本冊共用規則。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-052-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>PEL 記錄符合條件的事件，不是每條命令的執行歷史。只有事件受支援且符合記錄條件時，才依規則要求新增紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-052-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>查詢若因重設中止，恢復後須重新送出。比較回覆時，再逐欄區分固定身分、配置與動態狀態。 <a class="qa-rule-link" href="#common-identify-12">本冊完整規則</a></p>
</li>
<li id="q-052-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>重設後重新查詢受影響的物件。重設本身不表示 namespace 已刪除，也不表示配置已恢復出廠值。 <a class="qa-rule-link" href="#common-identify-13">本冊完整規則</a></p>
</li>
<li id="q-052-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新查詢並比較。若期間還有韌體啟用或管理操作，必須分清楚差異是由哪個事件造成。 <a class="qa-rule-link" href="#common-identify-14">本冊完整規則</a></p>
</li>
<li id="q-052-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Identify 是唯讀查詢。不同 controller 的 Active List 可能不同，因此比較時必須確認查詢對象。 <a class="qa-rule-link" href="#common-identify-15">本冊完整規則</a></p>
</li>
<li id="q-052-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>先用穩定識別資料確認比較的是同一物件，並保留原始 bytes。再分別處理填補空白、Reserved 欄位、動態值及真正有意義的屬性變更，避免只做逐 byte 比較就下結論。</p>
</li>
<li id="q-052-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>先確認這次 Reset 是否同時啟用了待啟用的韌體，或查詢是否實際送到另一個 controller／namespace。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-identity">Base 2.4 §4.7.1</a> · <a href="#ref-idns">NVM Command Set 1.3 §4.1.5.1–4.1.5.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-effects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-053" data-question="53"><h2><a class="qa-qid" href="#q-053">Q53</a> Identify、Feature、Log Page 與實際 Command 行為不一致時，應如何定位問題？</h2>
<p class="qa-prompt">先試著說明正常流程，並舉出一個未滿足執行條件的例子，再展開解答核對。</p>
<details class="qa-answer" id="q-053-answer"><summary>展開完整解答 · 17 個觀察面向</summary><ol class="qa-items">
<li id="q-053-a-01" data-answer="1"><h3><span>01</span> 這個功能要解決什麼問題？</h3>
<p>判定不一致時，要把能力、設定、當下狀態及命令結果連起來檢查。不能只因某個介面顯示支援，就忽略實際使用所需的其他條件。</p>
</li>
<li id="q-053-a-02" data-answer="2"><h3><span>02</span> 它的影響範圍是什麼？</h3>
<p>比對前，先固定 controller、NSID、CSI、時間及配置。來自不同 controller 或不同時點的資料，可能本來就在描述不同狀態。</p>
</li>
<li id="q-053-a-03" data-answer="3"><h3><span>03</span> 支援能力從哪個 Register、Identify 欄位、Feature 或 Log Page 確認？</h3>
<p>Identify 描述能力與屬性；Get Features 查詢設定；Log Page 則依種類提供狀態、事件或命令效果。三者用途不同，數值不相同本身不代表矛盾。</p>
</li>
<li id="q-053-a-04" data-answer="4"><h3><span>04</span> 涉及哪些 Command 與重要欄位？</h3>
<p>保留原 SQE、CQE、Identify 原始 buffer，以及 Get Features 使用的 SEL、Get Log Page 使用的 LID 和其他選擇欄位。尤其要分清楚讀到的是 Current 值，還是 Supported Capabilities。</p>
</li>
<li id="q-053-a-05" data-answer="5"><h3><span>05</span> 正常流程及先後順序是什麼？</h3>
<p>先確認規格版本與解碼方式，再檢查操作範圍及選擇欄位。接著確認參數合法、目前狀態允許執行，而且先後順序正確，最後才判斷結果。若仍有矛盾，可用每次只改一項條件的情境重現。</p>
</li>
<li id="q-053-a-06" data-answer="6"><h3><span>06</span> 成功時應回傳什麼結果？</h3>
<p>一致是指各介面符合規範定義的關係，不是回傳值必須全部相同。例如 CHANG=1 表示 Feature 可變更，Current=0 表示目前設定為 0，兩者可以同時正確。</p>
</li>
<li id="q-053-a-07" data-answer="7"><h3><span>07</span> 不支援、非法參數或錯誤順序時的 Status？</h3>
<p>先依原命令的 SCT／SC 決定下一步；More=1 時，再查可與命令關聯的 Error Information。如果只有 Host timeout 而沒有 CQE，則先追查命令是否提交及完成，不能直接套用某個 Status 的處理方式。</p>
</li>
<li id="q-053-a-08" data-answer="8"><h3><span>08</span> DNR 與 More 應如何設定？</h3>
<p>收到 CQE 時才有 DNR 與 More 可判讀。本題沒有另行指定固定值，請依本冊的共用規則，搭配實際完成條件判斷。 <a class="qa-rule-link" href="#common-command-8">本冊完整規則</a></p>
</li>
<li id="q-053-a-09" data-answer="9"><h3><span>09</span> 是否產生 Asynchronous Event？</h3>
<p>正常完成不保證會回報非同步事件。若另有事件發生，還須確認支援能力、通知設定，以及是否有等待中的 AER。 <a class="qa-rule-link" href="#common-command-9">本冊完整規則</a></p>
</li>
<li id="q-053-a-10" data-answer="10"><h3><span>10</span> 是否更新 Error Information Log 或其他 Log？</h3>
<p>依完成結果與記錄條件核對 Error Information，不能直接用失敗命令的數量推算新增 entry 數。完整條件見本冊共用規則。 <a class="qa-rule-link" href="#common-command-10">本冊完整規則</a></p>
</li>
<li id="q-053-a-11" data-answer="11"><h3><span>11</span> 是否記錄於 Persistent Event Log？</h3>
<p>PEL 記錄符合條件的事件，不是每條命令的執行歷史。只有事件受支援且符合記錄條件時，才依規則要求新增紀錄。 <a class="qa-rule-link" href="#common-command-11">本冊完整規則</a></p>
</li>
<li id="q-053-a-12" data-answer="12"><h3><span>12</span> Controller Reset 後是否保留或繼續？</h3>
<p>查詢若因重設中止，恢復後須重新送出。比較回覆時，再逐欄區分固定身分、配置與動態狀態。 <a class="qa-rule-link" href="#common-identify-12">本冊完整規則</a></p>
</li>
<li id="q-053-a-13" data-answer="13"><h3><span>13</span> NVM Subsystem Reset 後是否保留或繼續？</h3>
<p>重設後重新查詢受影響的物件。重設本身不表示 namespace 已刪除，也不表示配置已恢復出廠值。 <a class="qa-rule-link" href="#common-identify-13">本冊完整規則</a></p>
</li>
<li id="q-053-a-14" data-answer="14"><h3><span>14</span> Power Cycle 後是否保留或繼續？</h3>
<p>Power Cycle 後重新查詢並比較。若期間還有韌體啟用或管理操作，必須分清楚差異是由哪個事件造成。 <a class="qa-rule-link" href="#common-identify-14">本冊完整規則</a></p>
</li>
<li id="q-053-a-15" data-answer="15"><h3><span>15</span> 是否影響其他 Controller 或 Namespace？</h3>
<p>Identify 是唯讀查詢。不同 controller 的 Active List 可能不同，因此比較時必須確認查詢對象。 <a class="qa-rule-link" href="#common-identify-15">本冊完整規則</a></p>
</li>
<li id="q-053-a-16" data-answer="16"><h3><span>16</span> Identify、Feature、Log 與 Command 行為是否一致？</h3>
<p>只有確認必要前提成立、資料來自同一物件，而且時間順序一致後，結果仍違反明確規定，才能提出可驗證的不符合規範結論。</p>
</li>
<li id="q-053-a-17" data-answer="17"><h3><span>17</span> 結果不符預期時，第一個要檢查什麼？</h3>
<p>第一步先確認這些資料是否來自同一 controller／namespace、同一設定期間，並且使用相同或互相對應的選擇欄位。</p>
</li>
</ol>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-idcmd">Base 2.4 §5.2.14.1</a> · <a href="#ref-effects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-getfeat">Base 2.4 §5.2.12</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-command-8"><h3>命令完成、事件與紀錄 · DNR 與 More 應如何設定？</h3><p>只有收到 CQE，才有 DNR 與 More 可供判讀。DNR=1 表示相同命令即使重送到此 NVM subsystem 的任一 controller，仍預期會失敗；DNR=0 則只表示可能成功。除非個別錯誤條件另有明定，不能只看 Status 名稱就要求 DNR=1。More=1 表示 Error Information Log 有這筆命令的補充資訊。SCT=SC=0 時，DNR 應為 0。</p></article>
<article id="common-command-9"><h3>命令完成、事件與紀錄 · 是否產生 Asynchronous Event？</h3><p>命令完成與非同步通知是不同機制，操作成功本身不保證會產生事件。若操作引發規範定義的事件，還要確認事件受支援、相關通知設定允許回報、事件未被遮蔽，而且 Host 已提交等待中的 Asynchronous Event Request。</p></article>
<article id="common-command-10"><h3>命令完成、事件與紀錄 · 是否更新 Error Information Log 或其他 Log？</h3><p>成功 CQE 不會單憑成功這件事，就要求新增 Error Information entry。若錯誤 CQE 的 More=1，則讀取 LID01h，並以 SQID、CID 及 Error Count 關聯紀錄。其他非成功 CQE 是否需要新增 entry，仍須依記錄規則判斷，不能直接以失敗次數推算。至於操作造成的狀態變化，則用本題列出的查詢介面重新確認。</p></article>
<article id="common-command-11"><h3>命令完成、事件與紀錄 · 是否記錄於 Persistent Event Log？</h3><p>Persistent Event Log 是選配的事件歷史，不是每條命令的執行清單。先確認 LPA 宣告的支援能力及 Supported Events Bitmap，再判斷這次操作是否符合某個事件的記錄條件。不能只因命令成功或失敗，就要求新增一筆 PEL 紀錄。</p></article>
<article id="common-identify-12"><h3>查詢的重設與影響範圍 · Controller Reset 後是否保留或繼續？</h3><p>Controller Reset 會中止尚未完成的查詢。沒有收到回覆，不等於 controller 回傳全零資料；Host 應等查詢通道恢復後重新讀取，再逐欄分辨固定識別、目前配置與動態狀態。Reset 本身也不表示 namespace 已刪除。</p></article>
<article id="common-identify-13"><h3>查詢的重設與影響範圍 · NVM Subsystem Reset 後是否保留或繼續？</h3><p>重設完成後，重新查詢受影響的 controller 與 namespace。NVM Subsystem Reset 重設的是通訊及控制狀態，不能直接推論所有儲存配置都回到出廠值。若期間還執行了其他管理操作，則另依該操作的規則確認變更。</p></article>
<article id="common-identify-14"><h3>查詢的重設與影響範圍 · Power Cycle 後是否保留或繼續？</h3><p>Power Cycle 後，重新查詢版本、能力、目前格式及附加清單。固定識別資訊與持續配置，不應當成一般暫存 Feature 處理。不過，若同時發生韌體啟用或配置變更，結果可能不同，因此要保留前後資料及事件時間，才能解釋差異。</p></article>
<article id="common-identify-15"><h3>查詢的重設與影響範圍 · 是否影響其他 Controller 或 Namespace？</h3><p>Identify 只讀取資訊，不會建立、格式化或附加 namespace。回覆描述哪個物件，由 CNS 與相關選擇欄位決定。不同 controller 的 Active List 可以不同，不能只因清單不同就判定資料損壞。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-conventions"><strong>Base 2.4 · §1.4.1</strong><br>文件頁 2–3 · PDF 28–29</li>
<li id="ref-cap"><strong>Base 2.4 · §3.1.4 (CAP, VS)</strong><br>文件頁 54–59 · PDF 80–85 · Figure 36–37</li>
<li id="ref-nsid"><strong>Base 2.4 · §3.2.1</strong><br>文件頁 78–81 · PDF 104–107</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>文件頁 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-identity"><strong>Base 2.4 · §4.7.1</strong><br>文件頁 173–175 · PDF 199–201</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-getfeat"><strong>Base 2.4 · §5.2.12</strong><br>文件頁 209–212 · PDF 235–238 · Figure 197–202</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-effects"><strong>Base 2.4 · §5.2.13.1.6</strong><br>文件頁 226–229 · PDF 252–255 · Figure 216–217</li>
<li id="ref-nschange"><strong>Base 2.4 · §5.2.13.1.5, 5.2.13.1.14.2.6–5.2.13.1.14.2.8</strong><br>文件頁 226, 258–261 · PDF 252, 284–287 · Figure 247–249</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idcmd"><strong>Base 2.4 · §5.2.14.1</strong><br>文件頁 336–340 · PDF 362–366 · Figure 332–337</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>文件頁 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-idlist"><strong>Base 2.4 · §5.2.14.2.2–5.2.14.2.19, 5.2.14.3.1–5.2.14.3.2</strong><br>文件頁 387–399, 402–404 · PDF 413–425, 428–430 · Figure 342–355, 360–362</li>
<li id="ref-nsmanage"><strong>Base 2.4 · §5.2.24–5.2.25, 8.1.17</strong><br>文件頁 442–448, 660–664 · PDF 468–474, 686–690 · Figure 442–450</li>
<li id="ref-profile"><strong>Base 2.4 · §5.2.30.1.18</strong><br>文件頁 478–479 · PDF 504–505 · Figure 494–495</li>
<li id="ref-uuid"><strong>Base 2.4 · §8.1.31.1–8.1.31.2</strong><br>文件頁 737–738 · PDF 763–764 · Figure 782</li>
<li id="ref-virtual"><strong>Base 2.4 · §8.2.7</strong><br>文件頁 754–758 · PDF 780–784 · Figure 796</li>
<li id="ref-idns"><strong>NVM Command Set 1.3 · §4.1.5.1–4.1.5.4</strong><br>文件頁 84–107 · PDF 84–107 · Figure 123–130</li>
</ul><h3>需要看欄位圖時</h3><p>以下連結可開啟對應的圖表教學，查閱欄位及判讀方式。每張圖保留固定的教學位置，方便之後反覆查詢。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/identify/en/">English</a><a href="/DOCS/nvme-question-bank/identify.html">繁中教學 HTML</a></nav>
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
