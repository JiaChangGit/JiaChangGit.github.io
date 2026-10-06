---
layout: post
title: "NVMe 自問自答題庫：錯誤 Status 與 Error Information"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/errors/zh-tw/
lang: zh-TW
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/errors/en/">English</a><a href="/DOCS/nvme-question-bank/errors.html">繁中教學 HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q93–Q106</p><h1>錯誤 Status 與 Error Information</h1><p class="qr-intro">本冊從一筆失敗命令出發，先判斷錯誤類型，再找補充記錄與恢復依據。重點是把原命令、完成狀態及歷史資料對回同一件事。</p><p>先練習，再展開解答。各題依需要使用文字、欄位判讀、比較或流程說明，不要求相同的回答項目。所有數字案例均為教學假設；Status 以 SCT/SC 表示，代碼後的 h 代表十六進位。</p></header>
<aside class="qa-glossary"><h2>先認識本文使用的字詞</h2><dl><dt>Controller / namespace</dt><dd>controller 接收命令並管理存取；namespace 是命令可指定的一份邏輯儲存空間。NVM subsystem 則包含 controller 與非揮發儲存資源，同一 subsystem 可以有多個 controller。</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission Queue（SQ）是提交佇列，Completion Queue（CQ）是完成佇列；SQE 與 CQE 分別是其中的一筆命令及完成項目。QID 識別 queue，CID 區分同一 SQ 中尚未完成的命令，NSID 則識別 namespace。</dd><dt>Register / Identify / Feature / Log</dt><dd>Register 提供可存取的控制或狀態資訊；Identify 查詢物件的能力與屬性；Feature 用來讀取或變更工作設定；Log Page 回報特定種類的狀態或紀錄。FID、LID、CNS、CSI 則分別用來選擇 Feature、Log Page、Identify 資料結構及命令集。</dd><dt>index / offset / zero-based</dt><dd>index 指出清單中的第幾筆，通常從 0 起算；offset 表示與起點相隔多遠，解讀時必須確認單位。若數量欄位採 zero-based 編碼，實際數量等於欄位值加 1；但不是所有欄位看到 0 都要加 1。Dword 是 4 bytes，1 byte 是 8 bits。</dd><dt>Scope / reset / retention</dt><dd>scope 表示操作影響哪些物件；retention 表示狀態是否保留。清除 CC.EN 所觸發的 Controller Reset，是 Controller Level Reset（CLR）的一種。同屬 CLR 的不同觸發方式，仍可能採用不同的 Register 保留規則。</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>把三種證據分開讀</h2><p class="qa-takeaway">先確認命令身分，再比較錯誤；名稱相似的紀錄不一定描述相同事件。</p>
<div class="qr-table" tabindex="0" role="region" aria-label="可橫向捲動的比較表"><table><thead><tr><th scope="col">證據</th><th scope="col">能回答什麼</th><th scope="col">不能直接推論什麼</th></tr></thead><tbody><tr><td>CQE</td><td>該命令的完成結果</td><td>所有媒體效果已撤銷</td></tr><tr><td>Error Information</td><td>錯誤補充欄位及參數位置</td><td>每個失敗都必有一筆</td></tr><tr><td>PEL</td><td>支援的持續事件</td><td>完整命令執行歷史</td></tr></tbody></table></div>
<p><strong>舉例看懂：</strong>一筆命令同時有非法 NSID 與壞的 PRP，可能先檢出任一條件。若要驗證 Invalid Namespace，就應先修正指標，只保留一個錯誤原因。</p>
<p class="qa-citations">來源：<a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a></p>
</section>
<div class="qa-controls" hidden><label>搜尋本頁 <input type="search" id="qa-search" placeholder="題號、欄位或關鍵字"></label><button type="button" data-expand="true">展開全部解答</button><button type="button" data-expand="false">收合全部解答</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>本冊題目</h2><ol class="qa-index">
<li><a href="#q-093">Q93 · Invalid Opcode、Invalid Field、CID Conflict 與 Sequence Error 如何區分？</a></li>
<li><a href="#q-094">Q94 · Namespace、Log、Queue、Queue Size 與 Interrupt Vector 錯誤如何定位？</a></li>
<li><a href="#q-095">Q95 · Firmware、Format 與容量錯誤為何不能只看名稱？</a></li>
<li><a href="#q-096">Q96 · Data Transfer Error、Internal Error 與 Namespace Not Ready 有何不同？</a></li>
<li><a href="#q-097">Q97 · Power Loss、Abort、SQ Deletion 與 Fused 失敗如何反映於完成？</a></li>
<li><a href="#q-098">Q98 · Host 如何依 Status、More、DNR 與 CRD 決定下一步？</a></li>
<li><a href="#q-099">Q99 · 哪些錯誤需要 Error Information？</a></li>
<li><a href="#q-100">Q100 · 如何從 Error Information 對回原始命令與錯誤欄位？</a></li>
<li><a href="#q-101">Q101 · Error Log 的 Status 必須與 CQE 完全逐 bit 相同嗎？</a></li>
<li><a href="#q-102">Q102 · 多個錯誤、Log 容量與 Error Count 如何處理？</a></li>
<li><a href="#q-103">Q103 · 非 Success CQE 沒有新增 Error Entry，一定違規嗎？</a></li>
<li><a href="#q-104">Q104 · 一般命令錯誤後，其他命令是否可以繼續？</a></li>
<li><a href="#q-105">Q105 · 哪些嚴重情況可能設定 CSTS.CFS，Host 應怎麼判斷？</a></li>
<li><a href="#q-106">Q106 · 如何交叉比對 CQE、Error Information 與 Persistent Event？</a></li>
</ol></section>
<article class="qa-question" id="q-093" data-question="93" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-093">Q93</a> Invalid Opcode、Invalid Field、CID Conflict 與 Sequence Error 如何區分？</h2>
<p class="qa-prompt">先說出比較對象最重要的差別，並舉一個不能互相代用的例子。</p>
<details class="qa-answer" id="q-093-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-093-a-01">先判斷錯誤發生在哪一層，才知道要修改命令內容，還是修正 Host 的命令管理。例如 Opcode 不受支援，與同一條 SQ 重複使用尚未完成的 CID，是兩種不同問題。</p><div class="qa-sections">
<section class="qa-section" id="q-093-s-01" data-answer-section="1"><h3><span>1.</span> 差別在哪裡</h3>
<span class="qa-anchor" id="q-093-a-02"></span><p>Status 描述指定 SQID／CID 的完成；除非另外發現 queue 或 controller 故障，不應把單一命令的參數錯誤擴大成整個裝置失效。</p>
<span class="qa-anchor" id="q-093-a-04"></span><p>SCT=0：SC=01h 是 Invalid Command Opcode；02h 是 Invalid Field in Command；03h 是 Command ID Conflict；0Ch 是 Command Sequence Error。CID 的唯一性以同一條 SQ 的未完成命令為範圍。</p>
</section>
<section class="qa-section" id="q-093-s-02" data-answer-section="2"><h3><span>2.</span> 如何選擇與確認</h3>
<span class="qa-anchor" id="q-093-a-03"></span><p>先以 Identify 與 Commands Supported and Effects 確認 Opcode，再查該命令的欄位與順序要求。CID 是否重複，則要查看 Host 的 outstanding 清單。</p>
<span class="qa-anchor" id="q-093-a-05"></span><p>保留原始 SQE，確認命令集與支援能力，逐一檢查指定欄位，再重建命令先後順序。一次只改一個已確認的問題，才能知道哪項修正有效。</p>
<span class="qa-anchor" id="q-093-a-06"></span><p>合法且成功執行的命令回成功 CQE；如果測試故意製造錯誤，正確結果則是符合該條件的錯誤完成，不能要求所有測試都回成功。</p>
</section>
<section class="qa-section" id="q-093-s-03" data-answer-section="3"><h3><span>3.</span> 哪些結論不能互相套用</h3>
<span class="qa-anchor" id="q-093-a-07"></span><p>Invalid Field 應在沒有更明確指定 Status 時使用。若同時存在多個錯誤，除非另有優先規則，controller 可選擇其中一個；CID Conflict 的搜尋深度也是實作相關。</p>
<span class="qa-anchor" id="q-093-a-16"></span><p>將支援宣告、SQE 與 CQE 對在一起。若用一筆同時有非法 Opcode、非法 NSID 的命令驗證精確 Status，測試本身就無法隔離原因。</p>
</section>
</div>
<span class="qa-anchor" id="q-093-a-17"></span><span class="qa-anchor" id="q-093-a-08"></span><span class="qa-anchor" id="q-093-a-09"></span><span class="qa-anchor" id="q-093-a-10"></span><span class="qa-anchor" id="q-093-a-11"></span><span class="qa-anchor" id="q-093-a-12"></span><span class="qa-anchor" id="q-093-a-13"></span><span class="qa-anchor" id="q-093-a-14"></span><span class="qa-anchor" id="q-093-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-094" data-question="94" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-094">Q94</a> Namespace、Log、Queue、Queue Size 與 Interrupt Vector 錯誤如何定位？</h2>
<p class="qa-prompt">先說出比較對象最重要的差別，並舉一個不能互相代用的例子。</p>
<details class="qa-answer" id="q-094-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-094-a-01">這些錯誤都與識別或範圍有關，但所指的物件不同。先知道命令要查或建立哪個物件，才能判斷數值是否存在、是否有效，以及是否允許在這裡使用。</p><div class="qa-sections">
<section class="qa-section" id="q-094-s-01" data-answer-section="1"><h3><span>1.</span> 差別在哪裡</h3>
<span class="qa-anchor" id="q-094-a-02"></span><p>NSID 指 namespace，LID 指 Log 類型，QID 指 queue；QSIZE 是深度的編碼，IV 是中斷向量。它們不能因為都是數字，就共用同一套有效範圍。</p>
<span class="qa-anchor" id="q-094-a-04"></span><p>常見對照為 Invalid Namespace or Format 0/0Bh、Invalid Log Page 1/09h、Invalid Queue Identifier 1/01h、Invalid Queue Size 1/02h、Invalid Interrupt Vector 1/08h；Create SQ 的無效 CQID 則有 Completion Queue Invalid 1/00h。</p>
</section>
<section class="qa-section" id="q-094-s-02" data-answer-section="2"><h3><span>2.</span> 如何選擇與確認</h3>
<span class="qa-anchor" id="q-094-a-03"></span><p>使用 Active／Allocated Namespace List、Supported Log Pages、CAP.MQES、Number of Queues 與可用中斷資源，建立測試前的配置快照。</p>
<span class="qa-anchor" id="q-094-a-05"></span><p>先建立合法基準命令，再只替換目標欄位。例如測 QSIZE 超限時，應保留合法 QID、位址及 IV，避免另一個錯誤先被回報。</p>
<span class="qa-anchor" id="q-094-a-06"></span><p>合法建立成功後，Host 才能將 queue 視為存在。錯誤測試完成後，還要確認沒有留下可使用的半完成 queue 配置。</p>
</section>
<section class="qa-section" id="q-094-s-03" data-answer-section="3"><h3><span>3.</span> 哪些結論不能互相套用</h3>
<span class="qa-anchor" id="q-094-a-07"></span><p>上述代碼只適用於對應命令及條件。對 Get Log 使用錯誤 NSID，可能依該 Log 的 scope 規則回 Invalid Field；不能一律要求 Invalid Namespace。</p>
<span class="qa-anchor" id="q-094-a-16"></span><p>把命令專屬完成表與當時配置共同驗證，而不是只用通用 Status 名稱比對。</p>
</section>
</div>
<span class="qa-anchor" id="q-094-a-17"></span><span class="qa-anchor" id="q-094-a-08"></span><span class="qa-anchor" id="q-094-a-09"></span><span class="qa-anchor" id="q-094-a-10"></span><span class="qa-anchor" id="q-094-a-11"></span><span class="qa-anchor" id="q-094-a-12"></span><span class="qa-anchor" id="q-094-a-13"></span><span class="qa-anchor" id="q-094-a-14"></span><span class="qa-anchor" id="q-094-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-095" data-question="95" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-095">Q95</a> Firmware、Format 與容量錯誤為何不能只看名稱？</h2>
<p class="qa-prompt">先說出比較對象最重要的差別，並舉一個不能互相代用的例子。</p>
<details class="qa-answer" id="q-095-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-095-a-01">目的在區分映像、格式與資源問題，避免將不同命令回傳的「容量不足」混成同一件事。修正 slot 選擇，不會解決 namespace 配置容量不足。</p><div class="qa-sections">
<section class="qa-section" id="q-095-s-01" data-answer-section="1"><h3><span>1.</span> 差別在哪裡</h3>
<span class="qa-anchor" id="q-095-a-02"></span><p>Firmware Commit 影響韌體映像與啟用安排；Format 改變目標 namespace 的格式；Namespace Management 與 Capacity Management 分別管理不同層級的容量。</p>
<span class="qa-anchor" id="q-095-a-04"></span><p>Invalid Firmware Slot=1/06h，Invalid Firmware Image=1/07h，Invalid Format=1/0Ah。Namespace Insufficient Capacity=1/15h；Capacity Management 的 Insufficient Capacity=1/26h；一般 Capacity Exceeded=0/81h。</p>
</section>
<section class="qa-section" id="q-095-s-02" data-answer-section="2"><h3><span>2.</span> 如何選擇與確認</h3>
<span class="qa-anchor" id="q-095-a-03"></span><p>檢查 FRMW／Firmware Slot Information、支援的 LBA formats、總容量與未配置容量，以及命令的操作範圍。</p>
<span class="qa-anchor" id="q-095-a-05"></span><p>先確認 Opcode，再讀它的錯誤條件；重算要求的 bytes、logical blocks 或配置單位。只有單位一致，要求量與可用量才有比較意義。</p>
<span class="qa-anchor" id="q-095-a-06"></span><p>正向測試應得到該操作的完成結果；負向測試則確認錯誤被拒絕，且原先有效的配置仍符合該命令的失敗處理規則。</p>
</section>
<section class="qa-section" id="q-095-s-03" data-answer-section="3"><h3><span>3.</span> 哪些結論不能互相套用</h3>
<span class="qa-anchor" id="q-095-a-07"></span><p>不要把 1/15h 與 0/81h 視為可任意替換。也不要將 Firmware Activation Requires Reset 類型的狀態直接當成映像損壞，它可能是啟用還需要另一個步驟。</p>
<span class="qa-anchor" id="q-095-a-16"></span><p>比較配置前後 Identify 與 Log，並保留完整 SCT／SC；只儲存 SC 會遺失類別資訊。</p>
</section>
</div>
<span class="qa-anchor" id="q-095-a-17"></span><span class="qa-anchor" id="q-095-a-08"></span><span class="qa-anchor" id="q-095-a-09"></span><span class="qa-anchor" id="q-095-a-10"></span><span class="qa-anchor" id="q-095-a-11"></span><span class="qa-anchor" id="q-095-a-12"></span><span class="qa-anchor" id="q-095-a-13"></span><span class="qa-anchor" id="q-095-a-14"></span><span class="qa-anchor" id="q-095-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-nsmanage">Base 2.4 §5.2.24–5.2.25, 8.1.17</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-096" data-question="96" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-096">Q96</a> Data Transfer Error、Internal Error 與 Namespace Not Ready 有何不同？</h2>
<p class="qa-prompt">先說出比較對象最重要的差別，並舉一個不能互相代用的例子。</p>
<details class="qa-answer" id="q-096-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-096-a-01">三者分別指出資料傳輸、controller 內部處理及 namespace 可存取狀態。區分原因，才能選擇修正記憶體映射、處理裝置錯誤，或等待狀態改變。</p><div class="qa-sections">
<section class="qa-section" id="q-096-s-01" data-answer-section="1"><h3><span>1.</span> 差別在哪裡</h3>
<span class="qa-anchor" id="q-096-a-02"></span><p>Data Transfer Error 與 Internal Error 通常針對該命令；Namespace Not Ready 針對所選 namespace 的可用性。任何一項都不能單憑名稱推論全部 namespace 已毀損。</p>
<span class="qa-anchor" id="q-096-a-04"></span><p>Data Transfer Error=0/04h；Internal Error=0/06h；Namespace Not Ready=0/82h。Admin Command Media Not Ready=0/24h 另有 CRIME 與時間限制，不能和 namespace 狀態互換。</p>
</section>
<section class="qa-section" id="q-096-s-02" data-answer-section="2"><h3><span>2.</span> 如何選擇與確認</h3>
<span class="qa-anchor" id="q-096-a-03"></span><p>保存資料指標、Host 記憶體配置、CSTS 與 namespace 狀態，必要時讀 Error Information。Ready Mode 與 CFS 用來補足判斷，但不是同一欄位。</p>
<span class="qa-anchor" id="q-096-a-05"></span><p>先保存 CQE，再檢查資料位址與 buffer 使用期間；若位址正確，結合 Error Log、CSTS 及 namespace 狀態定位。失敗的 Read buffer 不應當成有效讀取結果。</p>
<span class="qa-anchor" id="q-096-a-06"></span><p>恢復後的成功命令才提供有效結果；看到 RDY=1，只表示對應 controller ready 條件成立，不保證每個 namespace 可立即存取。</p>
</section>
<section class="qa-section" id="q-096-s-03" data-answer-section="3"><h3><span>3.</span> 哪些結論不能互相套用</h3>
<span class="qa-anchor" id="q-096-a-07"></span><p>Namespace Not Ready 不用來取代已定義的 ANA 狀態錯誤。Internal Error 也不必然要求 CFS=1；只有更嚴重的 controller 情況才另行判定。</p>
<span class="qa-anchor" id="q-096-a-16"></span><p>確認錯誤種類與證據一致：合法資料指標不排除裝置內部錯誤；namespace 暫時不可用也不表示 Opcode 不受支援。</p>
</section>
<section class="qa-section" id="q-096-s-04" data-answer-section="4"><h3><span>4.</span> Asynchronous Event 的通知條件</h3>
<span class="qa-anchor" id="q-096-a-09"></span><p>Internal Error 的細節建議透過對應錯誤 AER 回報；Data Transfer Error 或 Namespace Not Ready 則不能一律要求同樣的事件。仍需區分事件發生、回報條件與是否有 AER 可用。</p>
</section>
</div>
<span class="qa-anchor" id="q-096-a-17"></span><span class="qa-anchor" id="q-096-a-08"></span><span class="qa-anchor" id="q-096-a-10"></span><span class="qa-anchor" id="q-096-a-11"></span><span class="qa-anchor" id="q-096-a-12"></span><span class="qa-anchor" id="q-096-a-13"></span><span class="qa-anchor" id="q-096-a-14"></span><span class="qa-anchor" id="q-096-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-ready">Base 2.4 §3.5.3–3.5.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-097" data-question="97" data-answer-kind="error"><h2><a class="qa-qid" href="#q-097">Q97</a> Power Loss、Abort、SQ Deletion 與 Fused 失敗如何反映於完成？</h2>
<p class="qa-prompt">先區分失敗條件，再判斷是否有規範明定的回報結果。</p>
<details class="qa-answer" id="q-097-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-097-a-01">中止原因決定 Status，也決定 Host 能否期待 CQE。尤其突然斷電或 Reset 可能讓完成通道消失，不能要求裝置在無法通訊後仍逐筆回報。</p><div class="qa-sections">
<section class="qa-section" id="q-097-s-01" data-answer-section="1"><h3><span>1.</span> 先區分是哪一種失敗</h3>
<span class="qa-anchor" id="q-097-a-02"></span><p>Abort 指向一筆命令，SQ Deletion 涵蓋該 SQ 的未完成命令，Fused 失敗涉及配對操作；電源及 Reset 的範圍則可能更大。</p>
<span class="qa-anchor" id="q-097-a-04"></span><p>Power Loss Notification=0/05h；Command Abort Requested=0/07h；SQ Deletion=0/08h；Failed Fused Command=0/09h；Missing Fused Command=0/0Ah。這些是目標命令的 Status。</p>
<span class="qa-anchor" id="q-097-a-07"></span><p>Power Loss Notification Status 不表示每次拔電都能留下 CQE。Fused missing 與另一筆已執行失敗也不同；應依配對、相鄰及順序條件判斷。</p>
</section>
<section class="qa-section" id="q-097-s-02" data-answer-section="2"><h3><span>2.</span> 用哪些資料確認原因</h3>
<span class="qa-anchor" id="q-097-a-03"></span><p>保存目標 SQID／CID、Delete 或 Abort 完成、CC／CSTS 及 FUSE 設定，才能重建真正的中止原因。</p>
<span class="qa-anchor" id="q-097-a-05"></span><p>先判斷 queue 是否仍有效，再讀目標完成；若已 Reset，依新生命週期重建 queue 與追蹤資料。Abort 本身的 CQE 與目標命令 CQE 要各自處理。</p>
</section>
<section class="qa-section" id="q-097-s-03" data-answer-section="3"><h3><span>3.</span> 結果與後續驗證</h3>
<span class="qa-anchor" id="q-097-a-06"></span><p>成功處理中止，並不等於目標命令回 Success。測試應驗證目標只完成一次，或在 Reset 規則下不再等待舊 queue 的完成。</p>
<span class="qa-anchor" id="q-097-a-16"></span><p>將目標 CQE、管理命令 CQE 與 queue／電源事件按時間比對，不要只用最後讀到的一個 Status 代表整段流程。</p>
<span class="qa-anchor" id="q-097-a-17"></span><p>先確認是否真的收到 Power Loss Notification，或其實是突然失去電源；這會改變對完成回報的期待。</p>
</section>
</div>
<span class="qa-anchor" id="q-097-a-08"></span><span class="qa-anchor" id="q-097-a-09"></span><span class="qa-anchor" id="q-097-a-10"></span><span class="qa-anchor" id="q-097-a-11"></span><span class="qa-anchor" id="q-097-a-12"></span><span class="qa-anchor" id="q-097-a-13"></span><span class="qa-anchor" id="q-097-a-14"></span><span class="qa-anchor" id="q-097-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-098" data-question="98" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-098">Q98</a> Host 如何依 Status、More、DNR 與 CRD 決定下一步？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-098-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-098-a-01">復原要先找出失敗原因，再決定重試是否合理。DNR=0 只是相同命令可能成功，不代表可以忽略資料是否已部分執行，或無限立即重送。</p><div class="qa-sections">
<section class="qa-section" id="q-098-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-098-a-02"></span><p>這些欄位屬於單一命令完成；Abort、刪 queue 或 Reset 則會擴大處理範圍，應以失敗影響與通道可用性決定。</p>
<span class="qa-anchor" id="q-098-a-03"></span><p>用 CQE 的 SCT／SC、M、DNR、CRD，搭配 Host Behavior Support.ACRE 與 Identify.CRDT1～3。M=1 時另讀 Error Information。</p>
<span class="qa-anchor" id="q-098-a-04"></span><p>ACRE=1 且 DNR=0 時，CRD=1、2、3 分別選 CRDT1、2、3；CRD=0 不要求額外延遲。DNR=1 或 ACRE=0 時，CRD 為保留欄位。</p>
</section>
<section class="qa-section" id="q-098-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-098-a-17"></span><p>先檢查測試是否把 DNR=0 誤寫成「必須立即重試成功」。</p>
<span class="qa-anchor" id="q-098-a-05"></span><p>先解析錯誤與補充資訊，修正非法參數或等待必要狀態，再判斷命令是否適合重試。若 queue 失效，才進入 queue 復原；Admin 通道失效則考慮 controller 復原。</p>
</section>
<section class="qa-section" id="q-098-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-098-a-06"></span><p>成功的復原包含有效的新結果，以及不再受舊命令後續動作影響；單純重試回 Success，仍不足以證明先前命令未重複寫入。</p>
<span class="qa-anchor" id="q-098-a-07"></span><p>Command Interrupted=0/21h 只能在 ACRE=1 時回傳，且 DNR 必須為 0。Format In Progress 也要求 DNR=0；其他錯誤不能只憑名稱自行指定 DNR。</p>
<span class="qa-anchor" id="q-098-a-16"></span><p>將 Host 的重試時間與 CRD／CRDT 比較；規範建議至少等待該時間，但提早重試本身不算錯誤。</p>
</section>
</div>
<span class="qa-anchor" id="q-098-a-08"></span><span class="qa-anchor" id="q-098-a-09"></span><span class="qa-anchor" id="q-098-a-10"></span><span class="qa-anchor" id="q-098-a-11"></span><span class="qa-anchor" id="q-098-a-12"></span><span class="qa-anchor" id="q-098-a-13"></span><span class="qa-anchor" id="q-098-a-14"></span><span class="qa-anchor" id="q-098-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-behavior">Base 2.4 §5.2.30.1.15</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-099" data-question="99" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-099">Q99</a> 哪些錯誤需要 Error Information？</h2>
<p class="qa-prompt">先用自己的話解釋機制，再舉一個常見誤解。</p>
<details class="qa-answer" id="q-099-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-099-a-01">Error Information 補充 CQE 無法容納的錯誤資訊，也能記錄不屬於特定命令的錯誤。它不是全部命令失敗的逐筆交易明細。</p><div class="qa-sections">
<section class="qa-section" id="q-099-s-01" data-answer-section="1"><h3><span>1.</span> 機制與適用範圍</h3>
<span class="qa-anchor" id="q-099-a-02"></span><p>LID 01h 的範圍是 controller；entry 是否能對應命令，要看 SQID、CID 及其有效條件。</p>
<span class="qa-anchor" id="q-099-a-04"></span><p>讀 Get Log Page LID=01h，保留 ECNT、SQID、CID、STS、Parameter Error Location、NSID 與 LPVER。</p>
</section>
<section class="qa-section" id="q-099-s-02" data-answer-section="2"><h3><span>2.</span> 用操作與結果理解</h3>
<span class="qa-anchor" id="q-099-a-03"></span><p>ELPE 決定最多 entry 數，CQE.M 表示該命令有補充資訊，Error 類型 AER 也可能引導 Host 查這份 Log。</p>
<span class="qa-anchor" id="q-099-a-05"></span><p>收到 M=1 的錯誤完成後儘快保存 Log，並讀取足夠多 entry，避免只看最新一筆卻漏掉較早發生的目標錯誤。</p>
<span class="qa-anchor" id="q-099-a-06"></span><p>找到可關聯的 entry，並能以補充欄位解釋原始錯誤。若是非命令錯誤，SQID／CID=FFFFh 本身可以是正確回覆。</p>
</section>
<section class="qa-section" id="q-099-s-03" data-answer-section="3"><h3><span>3.</span> 容易誤判的地方</h3>
<span class="qa-anchor" id="q-099-a-07"></span><p>M=0 表示這筆命令沒有額外狀態資訊，不能強制每次 Invalid Field 都新增 entry。若 M=1 卻缺少資訊，仍先排除覆寫、Reset 清除及查錯 controller。</p>
<span class="qa-anchor" id="q-099-a-16"></span><p>將 M、Error AER 與 entry 的關聯條件一起驗證；不要只比較「失敗 CQE 數」與「entry 數」。</p>
</section>
<section class="qa-section" id="q-099-s-04" data-answer-section="4"><h3><span>4.</span> 用 Log 補充哪些證據</h3>
<span class="qa-anchor" id="q-099-a-10"></span><p>成功 CQE 不會單憑成功這件事，就要求新增 Error Information entry。 <a class="qa-rule-link" href="#common-command-10">完整條件見本冊說明</a></p>
</section>
</div>
<span class="qa-anchor" id="q-099-a-17"></span><span class="qa-anchor" id="q-099-a-08"></span><span class="qa-anchor" id="q-099-a-09"></span><span class="qa-anchor" id="q-099-a-11"></span><span class="qa-anchor" id="q-099-a-12"></span><span class="qa-anchor" id="q-099-a-13"></span><span class="qa-anchor" id="q-099-a-14"></span><span class="qa-anchor" id="q-099-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-100" data-question="100" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-100">Q100</a> 如何從 Error Information 對回原始命令與錯誤欄位？</h2>
<p class="qa-prompt">先試著說明欄位的單位與編碼，再用一組數值推導結果。</p>
<details class="qa-answer" id="q-100-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-100-a-01">關聯紀錄可把「哪個欄位錯了」轉成可驗證的原始 bytes。只看自然語言 Status，通常不足以找到 Host 真正送出的錯誤參數。</p><div class="qa-sections">
<section class="qa-section" id="q-100-s-01" data-answer-section="1"><h3><span>1.</span> 先確認資料的來源與範圍</h3>
<span class="qa-anchor" id="q-100-a-02"></span><p>SQID＋CID 對應同一個 queue 使用期間的命令；因為 CID 會重用，還必須搭配 ECNT、時間與當時的命令快照。</p>
<span class="qa-anchor" id="q-100-a-03"></span><p>確認 LPVER，Base 2.4 的 entry 設為 1；CSI／OPC 在 LPVER≥1 才有效。</p>
</section>
<section class="qa-section" id="q-100-s-02" data-answer-section="2"><h3><span>2.</span> 欄位、單位與判讀例子</h3>
<span class="qa-anchor" id="q-100-a-04"></span><p>Parameter Error Location 的 bits 7:0 是 SQE byte offset，10:8 是該 byte 的 bit；多 byte／bit 欄位指向最低有效位置。此 PEL 縮寫不要與 Persistent Event Log 混淆。</p>
<span class="qa-anchor" id="q-100-a-05"></span><p>先對回 queue 使用期間，再比 SQID／CID／OPC／NSID；最後依 byte、bit 位置解碼原 SQE。例如位置指向 CDW10，就檢查那個命令對 CDW10 的定義。</p>
<span class="qa-anchor" id="q-100-a-06"></span><p>成功關聯後，可指出實際送出的值與違反條件，並用只修正該欄位的重測驗證。</p>
</section>
<section class="qa-section" id="q-100-s-03" data-answer-section="3"><h3><span>3.</span> 判讀時要保留的條件</h3>
<span class="qa-anchor" id="q-100-a-07"></span><p>非命令錯誤的 SQID、CID、Parameter Error Location 應為 FFFFh；不能把 FFFFh 當成合法命令的資料偏移去讀記憶體。</p>
<span class="qa-anchor" id="q-100-a-16"></span><p>比對 namespace 與命令集後再解讀 LBA／CSINFO，因為這些欄位的意義取決於命令，而不是每個錯誤都一定有 failing LBA。</p>
</section>
</div>
<span class="qa-anchor" id="q-100-a-17"></span><span class="qa-anchor" id="q-100-a-08"></span><span class="qa-anchor" id="q-100-a-09"></span><span class="qa-anchor" id="q-100-a-10"></span><span class="qa-anchor" id="q-100-a-11"></span><span class="qa-anchor" id="q-100-a-12"></span><span class="qa-anchor" id="q-100-a-13"></span><span class="qa-anchor" id="q-100-a-14"></span><span class="qa-anchor" id="q-100-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-101" data-question="101" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-101">Q101</a> Error Log 的 Status 必須與 CQE 完全逐 bit 相同嗎？</h2>
<p class="qa-prompt">先說出比較對象最重要的差別，並舉一個不能互相代用的例子。</p>
<details class="qa-answer" id="q-101-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-101-a-01">需要區分命令狀態與 Phase。若把包含 Phase 的整個 word 直接比較，可能將合法紀錄判成不一致。</p><div class="qa-sections">
<section class="qa-section" id="q-101-s-01" data-answer-section="1"><h3><span>1.</span> 差別在哪裡</h3>
<span class="qa-anchor" id="q-101-a-02"></span><p>只對同一筆命令的 entry 與 CQE 做比較；非命令錯誤並沒有原始 CQE 可逐 bit 對照。</p>
<span class="qa-anchor" id="q-101-a-04"></span><p>Error STS bits15:1 保存該命令的 Status；bit0 是 Phase，可表示原 CQE 的 P。CQE 中 Status 與 P 的位置不同，需先正規化再比較。</p>
</section>
<section class="qa-section" id="q-101-s-02" data-answer-section="2"><h3><span>2.</span> 如何選擇與確認</h3>
<span class="qa-anchor" id="q-101-a-03"></span><p>依 Figure 212 的 STS 與 Figure 101 的 Status 解碼，不要套用作業系統已移位或移除 Phase 的數值格式。</p>
<span class="qa-anchor" id="q-101-a-05"></span><p>保存原始 CQE 與 entry，先抽出 SCT／SC／DNR／M／CRD，再獨立處理 Phase；並確認 ECNT、SQID 與 CID。</p>
<span class="qa-anchor" id="q-101-a-06"></span><p>同一命令的 Status 應一致；Phase 依其「可回報」的定義處理，不要求所有記錄格式的完整 word 一樣。</p>
</section>
<section class="qa-section" id="q-101-s-03" data-answer-section="3"><h3><span>3.</span> 哪些結論不能互相套用</h3>
<span class="qa-anchor" id="q-101-a-07"></span><p>非命令錯誤使用最適合的 Status，不是缺少 CQE 就代表錯誤。多個錯誤條件時，也要以實際選定的完成 Status 比對。</p>
<span class="qa-anchor" id="q-101-a-16"></span><p>同時檢查解析程式是否把 SC、SCT 或 Phase 錯移一位；錯誤的 decoder 會讓所有 entry 都看似不符。</p>
</section>
</div>
<span class="qa-anchor" id="q-101-a-17"></span><span class="qa-anchor" id="q-101-a-08"></span><span class="qa-anchor" id="q-101-a-09"></span><span class="qa-anchor" id="q-101-a-10"></span><span class="qa-anchor" id="q-101-a-11"></span><span class="qa-anchor" id="q-101-a-12"></span><span class="qa-anchor" id="q-101-a-13"></span><span class="qa-anchor" id="q-101-a-14"></span><span class="qa-anchor" id="q-101-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-102" data-question="102" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-102">Q102</a> 多個錯誤、Log 容量與 Error Count 如何處理？</h2>
<p class="qa-prompt">先用自己的話解釋機制，再舉一個常見誤解。</p>
<details class="qa-answer" id="q-102-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-102-a-01">Error Count 用來辨識錯誤紀錄，而 Log 容量決定目前看得到多少歷史。兩者不同，所以有限的 Log 可以包含很大的累計序號。</p><div class="qa-sections">
<section class="qa-section" id="q-102-s-01" data-answer-section="1"><h3><span>1.</span> 機制與適用範圍</h3>
<span class="qa-anchor" id="q-102-a-02"></span><p>容量與 entry 排序以 controller 的 Error Information 為範圍，不是每個 namespace 各自建立相同數量的 entry。</p>
<span class="qa-anchor" id="q-102-a-04"></span><p>ECNT 是 64-bit 計數，從 1 開始；0 表示無效 entry。最大值再增加時必須回到 1，不經過 0。</p>
</section>
<section class="qa-section" id="q-102-s-02" data-answer-section="2"><h3><span>2.</span> 用操作與結果理解</h3>
<span class="qa-anchor" id="q-102-a-03"></span><p>Identify.ELPE 為零起算，ELPE=3 表示最多 4 筆，每筆 64 bytes。</p>
<span class="qa-anchor" id="q-102-a-05"></span><p>依發生時間由新到舊讀取。Log 滿時，controller 建議插入新 entry 並丟棄最舊 entry；取樣前後要保留 ECNT，才知道是否已有更新。</p>
<span class="qa-anchor" id="q-102-a-06"></span><p>假設容量 4、最近序號為 9，正常可見 9、8、7、6；看不到 1～5 不表示它們沒有發生。</p>
</section>
<section class="qa-section" id="q-102-s-03" data-answer-section="3"><h3><span>3.</span> 容易誤判的地方</h3>
<span class="qa-anchor" id="q-102-a-07"></span><p>ECNT=0 的空 entry 不能當成第零次錯誤；也不要因序號有間隔，就直接判定 Log 壞掉，應先考慮取樣期間新增及被移除的紀錄。</p>
<span class="qa-anchor" id="q-102-a-16"></span><p>比較 SMART Error Information Log Entries 時，要分清累計值與目前 entry 數；它們的數值不需要相同。</p>
</section>
</div>
<span class="qa-anchor" id="q-102-a-17"></span><span class="qa-anchor" id="q-102-a-08"></span><span class="qa-anchor" id="q-102-a-09"></span><span class="qa-anchor" id="q-102-a-10"></span><span class="qa-anchor" id="q-102-a-11"></span><span class="qa-anchor" id="q-102-a-12"></span><span class="qa-anchor" id="q-102-a-13"></span><span class="qa-anchor" id="q-102-a-14"></span><span class="qa-anchor" id="q-102-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-103" data-question="103" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-103">Q103</a> 非 Success CQE 沒有新增 Error Entry，一定違規嗎？</h2>
<p class="qa-prompt">先用自己的話解釋機制，再舉一個常見誤解。</p>
<details class="qa-answer" id="q-103-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-103-a-01">這題練習判斷證據是否足夠。命令失敗與必須提供額外錯誤資訊不是同一項要求，不能只看非零 Status 就宣告韌體違規。</p><div class="qa-sections">
<section class="qa-section" id="q-103-s-01" data-answer-section="1"><h3><span>1.</span> 機制與適用範圍</h3>
<span class="qa-anchor" id="q-103-a-02"></span><p>判斷限於這筆命令與其對應的記錄條件，不能用另一筆命令的新 entry 填補這筆命令的證據。</p>
<span class="qa-anchor" id="q-103-a-04"></span><p>關鍵欄位是 More；M=1 表示有這筆命令的補充資訊。Error AER 或個別命令規則也可能建立額外的記錄要求。</p>
</section>
<section class="qa-section" id="q-103-s-02" data-answer-section="2"><h3><span>2.</span> 用操作與結果理解</h3>
<span class="qa-anchor" id="q-103-a-03"></span><p>保存 CQE.M、SCT／SC、錯誤前後 ECNT、ELPE 與 Reset 時間。</p>
<span class="qa-anchor" id="q-103-a-05"></span><p>先找出要求記錄的規範條件，再排除讀錯 controller、讀取太短、較新錯誤覆寫及 Reset 清除。最後才評估是否缺少必要 entry。</p>
<span class="qa-anchor" id="q-103-a-06"></span><p>合理結果可能是「這次不要求新增」；也可能是「要求的資訊仍可找到」。合規判斷不應預設每次都要讓 Error Count 增加。</p>
</section>
<section class="qa-section" id="q-103-s-03" data-answer-section="3"><h3><span>3.</span> 容易誤判的地方</h3>
<span class="qa-anchor" id="q-103-a-07"></span><p>如果在排除其他原因後，M=1 仍沒有可關聯資訊，就有具體不一致可追查；M=0 且沒有額外條件時，不能用同一標準定罪。</p>
<span class="qa-anchor" id="q-103-a-16"></span><p>測試報告應附上規範條件、原 CQE 與 Log 快照，而不是只有「沒有看到 entry」一句結論。</p>
</section>
<section class="qa-section" id="q-103-s-04" data-answer-section="4"><h3><span>4.</span> 用 Log 補充哪些證據</h3>
<span class="qa-anchor" id="q-103-a-10"></span><p>成功 CQE 不會單憑成功這件事，就要求新增 Error Information entry。 <a class="qa-rule-link" href="#common-command-10">完整條件見本冊說明</a></p>
</section>
</div>
<span class="qa-anchor" id="q-103-a-17"></span><span class="qa-anchor" id="q-103-a-08"></span><span class="qa-anchor" id="q-103-a-09"></span><span class="qa-anchor" id="q-103-a-11"></span><span class="qa-anchor" id="q-103-a-12"></span><span class="qa-anchor" id="q-103-a-13"></span><span class="qa-anchor" id="q-103-a-14"></span><span class="qa-anchor" id="q-103-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-104" data-question="104" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-104">Q104</a> 一般命令錯誤後，其他命令是否可以繼續？</h2>
<p class="qa-prompt">先用自己的話解釋機制，再舉一個常見誤解。</p>
<details class="qa-answer" id="q-104-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-104-a-01">多數命令錯誤不會破壞 queue，因此復原可以限制在失敗命令。這能避免為了單一非法參數，無故中止其他正常工作。</p><div class="qa-sections">
<section class="qa-section" id="q-104-s-01" data-answer-section="1"><h3><span>1.</span> 機制與適用範圍</h3>
<span class="qa-anchor" id="q-104-a-02"></span><p>先區分命令、queue 與 controller 三層。只有發現更廣泛的故障證據，才擴大復原範圍。</p>
<span class="qa-anchor" id="q-104-a-04"></span><p>Base 9.1 說明大多數命令錯誤仍應繼續處理命令；嚴重 queue 錯誤則建議刪除並重建相關 SQ／CQ。</p>
</section>
<section class="qa-section" id="q-104-s-02" data-answer-section="2"><h3><span>2.</span> 用操作與結果理解</h3>
<span class="qa-anchor" id="q-104-a-03"></span><p>檢查 CQE、CSTS.CFS、queue 指標及其他命令是否仍正常完成；Error Information 用來補充原因。</p>
<span class="qa-anchor" id="q-104-a-05"></span><p>保存失敗命令，確認 queue 沒有損壞後繼續合法命令；若 queue 受損，停止使用並依 SQ→CQ 的相依關係復原。</p>
<span class="qa-anchor" id="q-104-a-06"></span><p>後續合法命令可以成功完成，同時先前失敗仍保留為一次独立結果。不能因後續成功，就抹去原本的錯誤。</p>
</section>
<section class="qa-section" id="q-104-s-03" data-answer-section="3"><h3><span>3.</span> 容易誤判的地方</h3>
<span class="qa-anchor" id="q-104-a-07"></span><p>若 Admin 命令遇到嚴重通道錯誤，或 Delete Queue 沒有完成，規範建議 Controller Level Reset；這與普通 Invalid Field 不同。</p>
<span class="qa-anchor" id="q-104-a-16"></span><p>驗證錯誤隔離能力時，分別觀察同 SQ、共享 CQ 與其他 CQ 的命令，避免將資源壅塞誤認為全部停止。</p>
</section>
</div>
<span class="qa-anchor" id="q-104-a-17"></span><span class="qa-anchor" id="q-104-a-08"></span><span class="qa-anchor" id="q-104-a-09"></span><span class="qa-anchor" id="q-104-a-10"></span><span class="qa-anchor" id="q-104-a-11"></span><span class="qa-anchor" id="q-104-a-12"></span><span class="qa-anchor" id="q-104-a-13"></span><span class="qa-anchor" id="q-104-a-14"></span><span class="qa-anchor" id="q-104-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-105" data-question="105" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-105">Q105</a> 哪些嚴重情況可能設定 CSTS.CFS，Host 應怎麼判斷？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-105-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-105-a-01">CFS 提供 Host 在正常完成通道可能失效時仍可查看的嚴重狀態。它不是每筆失敗命令都必須設定的錯誤總旗標。</p><div class="qa-sections">
<section class="qa-section" id="q-105-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-105-a-02"></span><p>CFS 屬於 controller。共享 subsystem 的其他 controller 是否受影響，必須另外觀察，不能只靠一個 CFS 位元推論。</p>
<span class="qa-anchor" id="q-105-a-03"></span><p>直接讀 CSTS.CFS，保存 CC、CAP、Ready 狀態及時間；若是 Secondary Controller，也先查 Online／Offline 狀態。</p>
<span class="qa-anchor" id="q-105-a-04"></span><p>Base 9.5 允許在嚴重錯誤導致無法透過 Admin 或 I/O CQE 通訊時設定 CFS。Offline Secondary Controller 的 CFS 則有虛擬化定義。</p>
</section>
<section class="qa-section" id="q-105-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-105-a-17"></span><p>先確認這是不是 Offline 的 Secondary Controller，避免把預期的管理狀態誤判成硬體損壞。</p>
<span class="qa-anchor" id="q-105-a-05"></span><p>遇到 timeout 或重複錯誤時讀 CFS；確認是需復原的 fatal 狀態後，先做該 controller 的 Reset 與重新初始化，仍無法清除才評估支援且平台適用的 Subsystem Reset。</p>
</section>
<section class="qa-section" id="q-105-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-105-a-06"></span><p>復原後應恢復可用狀態與正常命令處理。僅 CFS 清為 0，仍不足以省略 Admin Queue、Ready 與 I/O queue 的重新建立。</p>
<span class="qa-anchor" id="q-105-a-07"></span><p>CFS 本身不是 CQE，也不以中斷表示此狀態。若 controller 已無法回 CQE，就不能再要求每筆未完成命令都有 Internal Error CQE。</p>
<span class="qa-anchor" id="q-105-a-16"></span><p>比對 controller 角色、虛擬化狀態、實際通訊能力與 Reset 結果，才可區分預期 Offline 與真正 fatal 問題。</p>
</section>
<section class="qa-section" id="q-105-s-04" data-answer-section="4"><h3><span>4.</span> CQE、DNR 與 More 在這裡是否適用</h3>
<span class="qa-anchor" id="q-105-a-08"></span><p>讀取 CFS 沒有 CQE，因此 DNR／More 不適用於這個 Register 讀取。只有另外收到命令 CQE 時，才解讀該 CQE 的位元。</p>
</section>
</div>
<span class="qa-anchor" id="q-105-a-09"></span><span class="qa-anchor" id="q-105-a-10"></span><span class="qa-anchor" id="q-105-a-11"></span><span class="qa-anchor" id="q-105-a-12"></span><span class="qa-anchor" id="q-105-a-13"></span><span class="qa-anchor" id="q-105-a-14"></span><span class="qa-anchor" id="q-105-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<article class="qa-question" id="q-106" data-question="106" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-106">Q106</a> 如何交叉比對 CQE、Error Information 與 Persistent Event？</h2>
<p class="qa-prompt">先列出已知證據與仍缺少的資訊，再決定能不能判定韌體違規。</p>
<details class="qa-answer" id="q-106-answer"><summary>展開解答與推導</summary>
<p class="qa-answer-lead" id="q-106-a-01">三份證據的粒度不同：CQE 是單一命令結果，Error Information 是補充錯誤，PEL 是重要事件歷史。交叉比對能補足資訊，但不應要求一對一出現。</p><div class="qa-sections">
<section class="qa-section" id="q-106-s-01" data-answer-section="1"><h3><span>1.</span> 先保留哪些證據</h3>
<span class="qa-anchor" id="q-106-a-02"></span><p>先標明 controller、namespace、queue 使用期間與事件範圍；不同範圍的紀錄可以有關聯，卻不一定代表同一筆命令。</p>
<span class="qa-anchor" id="q-106-a-03"></span><p>確認 Error Log 的 ELPE、PEL 支援與 Supported Events Bitmap，以及 Timestamp 的來源與同步狀態。</p>
<span class="qa-anchor" id="q-106-a-04"></span><p>CQE 用 SQID／CID／Status；Error entry 加 ECNT、NSID、OPC；PEL 用事件類型、controller 身分、時間及事件資料。Parameter Error Location 不是 Persistent Event Log 的位置。</p>
</section>
<section class="qa-section" id="q-106-s-02" data-answer-section="2"><h3><span>2.</span> 依什麼順序排除原因</h3>
<span class="qa-anchor" id="q-106-a-17"></span><p>先確認三份紀錄的取樣時間與 controller 身分一致，再分析看似矛盾的值。</p>
<span class="qa-anchor" id="q-106-a-05"></span><p>先對回命令與 Error entry，再找同一操作或時段的 PEL；若 Timestamp 曾變更，先重建時間關係，再下事件順序的結論。</p>
</section>
<section class="qa-section" id="q-106-s-03" data-answer-section="3"><h3><span>3.</span> 什麼結果足以支持結論</h3>
<span class="qa-anchor" id="q-106-a-06"></span><p>成功的判讀會說明哪份證據支持哪個結論，以及哪些部分仍無法確認。例如有 Format Start，不代表已有 Format Completion。</p>
<span class="qa-anchor" id="q-106-a-07"></span><p>缺少 PEL entry 不一定違規，先檢查該事件是否受支援及應記錄。另一方面，不能以「Log 選配」否定已宣告支援後的必要行為。</p>
<span class="qa-anchor" id="q-106-a-16"></span><p>將能力、事件條件、CQE 與各自保留規則放在同一條時間線；Reset 後 entry 消失與計數保留可以同時成立。</p>
</section>
</div>
<span class="qa-anchor" id="q-106-a-08"></span><span class="qa-anchor" id="q-106-a-09"></span><span class="qa-anchor" id="q-106-a-10"></span><span class="qa-anchor" id="q-106-a-11"></span><span class="qa-anchor" id="q-106-a-12"></span><span class="qa-anchor" id="q-106-a-13"></span><span class="qa-anchor" id="q-106-a-14"></span><span class="qa-anchor" id="q-106-a-15"></span>
<details class="qa-source-links"><summary>本題原文定位</summary>
<p class="qa-citations">來源：<a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">回本冊題目</a></article>
<section id="common-rules" class="qa-common"><h2>共用規則：各題連到的完整解釋</h2><p>這些規則在本冊只完整說明一次。返回剛才的題目可用瀏覽器「上一頁」；特定命令或 Feature 的明文例外優先。</p>
<article id="common-command-10"><h3>命令完成、事件與紀錄 · 是否更新 Error Information Log 或其他 Log？</h3><p>成功 CQE 不會單憑成功這件事，就要求新增 Error Information entry。若錯誤 CQE 的 More=1，則讀取 LID01h，並以 SQID、CID 及 Error Count 關聯紀錄。其他非成功 CQE 是否需要新增 entry，仍須依記錄規則判斷，不能直接以失敗次數推算。至於操作造成的狀態變化，則用本題列出的查詢介面重新確認。</p></article>
</section>
<section id="source-index"><h2>原文定位與既有圖表判讀</h2><p>Base 的文件頁碼等於 PDF 頁碼減 26；NVM 與 PCIe 兩份規格的文件頁碼則與 PDF 頁碼相同。以下依提供的 PDF 本文列出章節、頁碼及 Figure 編號。若同一頁包含其他主題，只引用本題需要的定義，不納入 Fabrics 或 PCIe Link、封包內容。</p><ul class="qa-references">
<li id="ref-cc"><strong>Base 2.4 · §3.1.4 (CC, CSTS, NSSR)</strong><br>文件頁 60–66 · PDF 86–92 · Figure 41–43</li>
<li id="ref-nsid"><strong>Base 2.4 · §3.2.1</strong><br>文件頁 78–81 · PDF 104–107</li>
<li id="ref-order"><strong>Base 2.4 · §3.4.1–3.4.5</strong><br>文件頁 101–105 · PDF 127–131 · Figure 80–81</li>
<li id="ref-ready"><strong>Base 2.4 · §3.5.3–3.5.4</strong><br>文件頁 109–113 · PDF 135–139 · Figure 84–85</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>文件頁 120–124 · PDF 146–150</li>
<li id="ref-sqe"><strong>Base 2.4 · §4.1.1</strong><br>文件頁 139–142 · PDF 165–168 · Figure 92–93</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>文件頁 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>文件頁 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-abort"><strong>Base 2.4 · §5.2.1</strong><br>文件頁 181–182 · PDF 207–208 · Figure 147–149</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>文件頁 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>文件頁 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-getlog"><strong>Base 2.4 · §5.2.13–5.2.13.1.1</strong><br>文件頁 212–218 · PDF 238–244 · Figure 203–211</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>文件頁 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>文件頁 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-pelcontext"><strong>Base 2.4 · §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</strong><br>文件頁 244–256, 258 · PDF 270–282, 284 · Figure 232–244, 246</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>文件頁 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-nsmanage"><strong>Base 2.4 · §5.2.24–5.2.25, 8.1.17</strong><br>文件頁 442–448, 660–664 · PDF 468–474, 686–690 · Figure 442–450</li>
<li id="ref-timestamp"><strong>Base 2.4 · §5.2.30.1.8</strong><br>文件頁 469–471 · PDF 495–497 · Figure 479–480</li>
<li id="ref-behavior"><strong>Base 2.4 · §5.2.30.1.15</strong><br>文件頁 475–477 · PDF 501–503 · Figure 491</li>
<li id="ref-create"><strong>Base 2.4 · §5.3.1–5.3.2</strong><br>文件頁 527–531 · PDF 553–557 · Figure 571–579</li>
<li id="ref-delete"><strong>Base 2.4 · §5.3.3–5.3.4</strong><br>文件頁 531–532 · PDF 557–558 · Figure 580–583</li>
<li id="ref-virtual"><strong>Base 2.4 · §8.2.7</strong><br>文件頁 754–758 · PDF 780–784 · Figure 796</li>
<li id="ref-fatal"><strong>Base 2.4 · §9.1–9.6.1</strong><br>文件頁 825–826 · PDF 851–852</li>
</ul><h3>需要看欄位圖時</h3><p>以下連結可開啟對應的圖表教學，查閱欄位及判讀方式。每張圖保留固定的教學位置，方便之後反覆查詢。</p><ul>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a></li>
<li><a href="/nvme/figure-reference/init/zh-tw/#figure-b42">Base 2.4 Figure 42 · Offset 1Ch: CSTS – Controller Status</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></li>
<li><a href="/nvme/figure-reference/command/zh-tw/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>使用的原始文件</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="題庫與版本"><a href="#content">跳到內容</a><a href="/nvme/question-bank/zh-tw/">題庫總索引</a><a href="/nvme/question-bank/errors/en/">English</a><a href="/DOCS/nvme-question-bank/errors.html">繁中教學 HTML</a></nav>
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
