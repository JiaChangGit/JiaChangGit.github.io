---
layout: "post"
title: "NVMe 圖表判讀與情境練習 06 · 健康、事件與診斷紀錄"
date: "2026-09-29 09:00:00 +0800"
categories: ["nvme"]
tags: ["NVMe", "Reference"]
permalink: "/nvme/figure-reference/logs/zh-tw/"
nvme_quickref: true
last_modified_at: "2026-10-01"
lang: "zh-Hant-TW"
description: "NVMe 情境練習與圖表速查：查詢路徑、欄位推導、完整解答及 Spec 位置。"
---

<div class="nvme-quickref">
<nav class="qr-top" aria-label="版本與索引"><a href="#content">跳到內容</a><a href="/nvme/figure-reference/zh-tw/">總索引</a><a href="/nvme/figure-reference/logs/en/">English</a><a href="/DOCS/nvme-quick-reference/logs.html">繁中 HTML</a></nav>
<main id="content">
<header><p class="qr-eyebrow">反覆查詢 · 欄位判讀 · 原文定位</p><h1>NVMe 圖表判讀與情境練習 06 · 健康、事件與診斷紀錄</h1><p class="qr-intro">先確認讀取參數與支援，再分清目前狀態、累計數與歷史快照。Telemetry 和持久事件的版本、長度與讀取生命週期，會決定資料能否正確串接。</p></header>
<aside class="qr-note"><p>每張原圖都有用途、欄位和判讀例子。例子中的數值用於說明，不代表你的裝置設定；原文另有條件時，依該欄位與命令定義判斷。</p><p>用瀏覽器「在頁面中尋找」搜尋欄位、FID、LID、CNS 或 Figure。bit／byte 位置沿用原圖：bit 是位元，byte 是 8 bits，Dword 是 4 bytes；index 是第幾筆，offset 是相對起點的偏移，須看當處使用的單位。</p><p>FID（Feature Identifier）選擇功能；LID（Log Page Identifier）選擇紀錄頁；CNS（Controller or Namespace Structure）選擇 Identify 回傳的資料結構。</p></aside>
<nav class="qr-top" aria-label="本冊閱讀入口"><a href="#exercises">從情境練習開始</a><a href="#figure-index">直接查圖表</a></nav>
<section id="exercises"><h2>先做情境練習</h2>
<p>每題資料均為教學假設，不是實際裝置回傳。先寫下查詢介面、目標、欄位與可支持的結論，再展開解答。題目只做 Spec 推導，不會執行命令。</p>
<nav class="qr-toc" id="exercise-toc" aria-label="情境索引"><ol>
<li><a href="#exercise-logs-01">SMART 顯示 120%，是不是已經不能用了？</a></li>
<li><a href="#exercise-logs-02">Data Units Written 增加 4，實際寫了多少？</a></li>
<li><a href="#exercise-logs-03">指定 NSID，就能得到該 namespace 的 SMART 嗎？</a></li>
<li><a href="#exercise-logs-04">兩個 namespace 的警告其實來自同一個 group？</a></li>
<li><a href="#exercise-logs-05">Self-test 沒有在跑，FLBA=0 就表示 LBA 0 壞了？</a></li>
<li><a href="#exercise-logs-06">分段 Telemetry 可以把兩個 generation 拼在一起嗎？</a></li>
<li><a href="#exercise-logs-07">Persistent Event Log 的下一筆應從哪裡開始？</a></li>
</ol></nav>
<article class="qr-card qr-case" id="exercise-logs-01" data-scenario="logs-01"><h3><span class="qr-number">練習 01</span>SMART 顯示 120%，是不是已經不能用了？</h3>
<p class="qr-case-question">健康報告只顯示一個紅色「120%」。請把真正能從 SMART 得到的結論拆開。</p><div class="qr-observations"><h4>模擬回傳與已知條件</h4><ul>
<li>LID=02h：Percentage Used=120；Available Spare=9；Available Spare Threshold=10；Critical Warning 的 spare 位=1。</li>
<li>Composite Temperature=300 K；本次沒有提供近期 I/O 成敗紀錄。</li>
</ul></div><details class="qr-answer"><summary>展開解答：查詢路徑與完整推導</summary>
<p class="qr-route"><strong>查詢次序：</strong>Get Log Page LID=02h 取得 SMART／Health；保留 warning bitmap 與各自的數值欄位，不合併成一個「健康分數」。</p>
<p data-reasoning="logs-01-1"><span class="qr-step">推導 1</span>Percentage Used 是預估壽命耗用，容許超過 100；120 不等於已損壞 120%，也不能單獨證明裝置現在不能讀寫。</p>
<p data-reasoning="logs-01-2"><span class="qr-step">推導 2</span>Available Spare=9 低於門檻 10，且對應 warning 已置位，這才是本例可直接說明的備援空間警告。300 K 約為 26.85°C，屬另一種量測，不應與百分比相加。</p>
<p data-reasoning="logs-01-3"><span class="qr-step">推導 3</span>完整報告應分列壽命估計、目前警告及近期錯誤／I/O 行為。要判定能否繼續服務，還需要系統需求與實際行為資料；這份 log 不提供一個能替代全部判斷的總分。</p>
<div class="qr-related">需要重看欄位時，接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-b213">Base 2.4 Figure 213 · SMART：警告、累計量、溫度與時間</a></div>
<h4>本題原文定位</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.13.1.3 · Figure 213 · SMART / Health Information Log Page · 文件頁 221–225 · PDF 247–251</li></ul></details>
<a href="#exercise-toc">回情境索引</a></article>
<article class="qr-card qr-case" id="exercise-logs-02" data-scenario="logs-02"><h3><span class="qr-number">練習 02</span>Data Units Written 增加 4，實際寫了多少？</h3>
<p class="qr-case-question">監控程式將 SMART 的 Data Units Written 差值乘以 512，得到很小的寫入量。這少算了什麼？</p><div class="qr-observations"><h4>模擬回傳與已知條件</h4><ul>
<li>相同對象的兩次 DUW：1000 → 1004；計數有效，無重置或飽和；取樣相隔 60 seconds。</li>
<li>Host Write Commands 同期增加 80；沒有完整命令大小清單。</li>
</ul></div><details class="qr-answer"><summary>展開解答：查詢路徑與完整推導</summary>
<p class="qr-route"><strong>查詢次序：</strong>兩次 Get Log Page LID=02h；同時保存 NSID、取樣時間、DUW 與 Host Write Commands。</p>
<p data-reasoning="logs-02-1"><span class="qr-step">推導 1</span>DUW 以 1000 個 512-byte units 為一個回報單位，並向上取整。差值 4 對應約 4×1000×512=2048000 bytes 的量級，不是 2048 bytes。</p>
<p data-reasoning="logs-02-2"><span class="qr-step">推導 2</span>兩個端點都經過取整，因此這不是精確的 60 秒 payload byte 數。拿它除以 80，也只能得到粗略平均，不能反推每個 Write 都是同樣大小。</p>
<p data-reasoning="logs-02-3"><span class="qr-step">推導 3</span>要驗證某筆命令的長度，回到命令 NLB 與使用中 LBA 格式；要看长期趨勢，才使用這種累計差值。也不要把 host 寫入量直接當作 NAND 實際寫入量。</p>
<div class="qr-related">需要重看欄位時，接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-b213">Base 2.4 Figure 213 · SMART：警告、累計量、溫度與時間</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n54">NVM Command Set 1.3 Figure 54 · Read CDW12：範圍、重試與保護要求</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-n125">NVM Command Set 1.3 Figure 125 · LBAF：資料大小、metadata 大小與相對效能</a></div>
<h4>本題原文定位</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.13.1.3 · Figure 213 · SMART / Health Information Log Page · 文件頁 221–225 · PDF 247–251</li><li>NVM Command Set 1.3 · §3.3.4 · Figure 54 · Read – Command Dword 12 · 文件頁 49 · PDF 49</li><li>NVM Command Set 1.3 · §4.1.5.1 · Figure 125 · LBA Format Data Structure, NVM Command Set Specific · 文件頁 94 · PDF 94</li></ul></details>
<a href="#exercise-toc">回情境索引</a></article>
<article class="qr-card qr-case" id="exercise-logs-03" data-scenario="logs-03"><h3><span class="qr-number">練習 03</span>指定 NSID，就能得到該 namespace 的 SMART 嗎？</h3>
<p class="qr-case-question">報表把同一張 SMART 複製到每個 namespace，並聲稱是各自的使用量。能力資料是否支持這樣標示？</p><div class="qr-observations"><h4>模擬回傳與已知條件</h4><ul>
<li>Identify Controller 的 LPA：per-namespace SMART／Health 支援位=0。</li>
<li>目前讀取的是 NSID=FFFFFFFFh 的 LID=02h；controller 有 4 個 active namespaces。</li>
</ul></div><details class="qr-answer"><summary>展開解答：查詢路徑與完整推導</summary>
<p class="qr-route"><strong>查詢次序：</strong>Identify CNS=01h 查 LPA；按 SMART 定義選擇 NSID；能力不提供的細分資訊不能靠改報表標籤補出來。</p>
<p data-reasoning="logs-03-1"><span class="qr-step">推導 1</span>此份資料不是 4 份獨立的 per-namespace 統計。NSID=FFFFFFFFh 的回報應依該 log 的總體範圍標示，不能複製後再相加，否則同一份量會被重複算 4 次。</p>
<p data-reasoning="logs-03-2"><span class="qr-step">推導 2</span>想改用特定 NSID，先要有 per-namespace SMART 支援，並遵守該 log 的 namespace 規則。不能因 Get Log Page 有 NSID 欄位，就假設每個 LID 都提供任意層級的統計。</p>
<p data-reasoning="logs-03-3"><span class="qr-step">推導 3</span>若需要區分 Endurance Group，可再查 namespace 的 ENDGID 與 LID=09h；那仍是 group 統計，不是自動變成單一 namespace 或檔案系統統計。</p>
<div class="qr-related">需要重看欄位時，接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify Controller：能力與限制的主要入口</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b213">Base 2.4 Figure 213 · SMART：警告、累計量、溫度與時間</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b225">Base 2.4 Figure 225 · Endurance Group：逐組健康與容量</a></div>
<h4>本題原文定位</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.14.2.1 · Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent · 文件頁 355–356 · PDF 381–382</li><li>Base 2.4 · §5.2.13.1.3 · Figure 213 · SMART / Health Information Log Page · 文件頁 221–225 · PDF 247–251</li><li>Base 2.4 · §5.2.13.1.10 · Figure 225 · Endurance Group Information Log Page · 文件頁 238–239 · PDF 264–265</li></ul></details>
<a href="#exercise-toc">回情境索引</a></article>
<article class="qr-card qr-case" id="exercise-logs-04" data-scenario="logs-04"><h3><span class="qr-number">練習 04</span>兩個 namespace 的警告其實來自同一個 group？</h3>
<p class="qr-case-question">管理系統對 NSID=2、NSID=9 各發出一次耐久度警告。要怎麼判斷是否重複通報同一個對象？</p><div class="qr-observations"><h4>模擬回傳與已知條件</h4><ul>
<li>兩個 namespace 的 Identify 資料均為 ENDGID=3；LID=09h、LSI=3 的 Critical Warning 非零。</li>
<li>沒有 group 4 的查詢結果，也沒有證據顯示 namespace 配置在期間變更。</li>
</ul></div><details class="qr-answer"><summary>展開解答：查詢路徑與完整推導</summary>
<p class="qr-route"><strong>查詢次序：</strong>Identify CNS=00h、各自 NSID → ENDGID → Get Log Page LID=09h、LSI=ENDGID。</p>
<p data-reasoning="logs-04-1"><span class="qr-step">推導 1</span>兩個 namespace 都指向 group 3，因此同一份 group log 可以影響兩個 namespace 的風險呈現；但警告來源只有一個 group。報表應保留 namespace 與 group 的對應，不把它算成兩個獨立 group 故障。</p>
<p data-reasoning="logs-04-2"><span class="qr-step">推導 2</span>LSI 在這個 LID 用來選 Endurance Group，不是 NSID，也不是傳輸長度的高位。把 NSID=9 填成 LSI=9，會查另一個對象，無法回答 group 3 的問題。</p>
<p data-reasoning="logs-04-3"><span class="qr-step">推導 3</span>group 3 的警告也不能延伸成所有 group 都有警告。若要比較 group 4，必須先確認其存在並取得同時段、相同欄位的資料。</p>
<div class="qr-related">需要重看欄位時，接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-b225">Base 2.4 Figure 225 · Endurance Group：逐組健康與容量</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b205">Base 2.4 Figure 205 · Get Log CDW11：長度高位與目標識別</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-n123">NVM Command Set 1.3 Figure 123 · NVM Namespace：容量、格式、原子性與建議粒度</a></div>
<h4>本題原文定位</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.13.1.10 · Figure 225 · Endurance Group Information Log Page · 文件頁 238–239 · PDF 264–265</li><li>Base 2.4 · §5.2.13 · Figure 205 · Get Log Page – Command Dword 11 · 文件頁 214 · PDF 240</li><li>NVM Command Set 1.3 · §4.1.5.1 · Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set · 文件頁 90–93 · PDF 90–93</li></ul></details>
<a href="#exercise-toc">回情境索引</a></article>
<article class="qr-card qr-case" id="exercise-logs-05" data-scenario="logs-05"><h3><span class="qr-number">練習 05</span>Self-test 沒有在跑，FLBA=0 就表示 LBA 0 壞了？</h3>
<p class="qr-case-question">工具同時顯示「測試卡在 45%」及「LBA 0 故障」。請用欄位有效性找出兩個誤判。</p><div class="qr-observations"><h4>模擬回傳與已知條件</h4><ul>
<li>LID=06h：目前 DSTOS=0，完成百分比 bytes 留著 45。最新結果 DSTR=2。</li>
<li>最新結果的 VDINFO.FVLD=0，而 FLBA 原始 bytes 全為 0。</li>
</ul></div><details class="qr-answer"><summary>展開解答：查詢路徑與完整推導</summary>
<p class="qr-route"><strong>查詢次序：</strong>Get Log Page LID=06h；先讀目前 operation，再讀最新 Result 的 DSTR 與 VDINFO，最後才使用診斷欄位。</p>
<p data-reasoning="logs-05-1"><span class="qr-step">推導 1</span>DSTOS=0 表示沒有正在執行的 self-test，進度欄應忽略。它不是一個仍有效但停住的 45% 進度，不能拿來計算「已經卡住多久」。</p>
<p data-reasoning="logs-05-2"><span class="qr-step">推導 2</span>DSTR=2 表示操作因 Controller Level Reset 中止，與測試發現媒體失敗不同。應報告中止原因，而不是將所有非零結果統稱為測試失敗。</p>
<p data-reasoning="logs-05-3"><span class="qr-step">推導 3</span>FVLD=0 使 FLBA 無效；零只是無效欄位中的原始值，不是有效的故障 LBA 0。對 NSID、SCT、SC 也要依各自有效位判斷，不能從填充 bytes 編造診斷。</p>
<div class="qr-related">需要重看欄位時，接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b218">Base 2.4 Figure 218 · Self-test Log：目前進度與最近 20 筆結果</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b219">Base 2.4 Figure 219 · Self-test Result：先看有效位再讀失敗位置</a></div>
<h4>本題原文定位</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.13.1.7 · Figure 218 · Device Self-test Log Page · 文件頁 230 · PDF 256</li><li>Base 2.4 · §5.2.13.1.7 · Figure 219 · Self-test Result Data Structure · 文件頁 231–232 · PDF 257–258</li></ul></details>
<a href="#exercise-toc">回情境索引</a></article>
<article class="qr-card qr-case" id="exercise-logs-06" data-scenario="logs-06"><h3><span class="qr-number">練習 06</span>分段 Telemetry 可以把兩個 generation 拼在一起嗎？</h3>
<p class="qr-case-question">你要保存一次 controller-initiated telemetry，讀完後才發現前後 header 不同。這份合併檔還能當同一次快照嗎？</p><div class="qr-observations"><h4>模擬回傳與已知條件</h4><ul>
<li>LID=08h 首次 header：TCDGN=10、TCDA=1、DA1LB=3；最後重讀：TCDGN=11、TCDA=1。</li>
<li>兩次 header 之間分段讀取資料；無完整紀錄證明各 chunk 屬於哪一代。</li>
</ul></div><details class="qr-answer"><summary>展開解答：查詢路徑與完整推導</summary>
<p class="qr-route"><strong>查詢次序：</strong>Get Log Page LID=08h，保留 RAE、header 與每次 offset；對照 TCDGN、TCDA 及 Data Area 邊界。</p>
<p data-reasoning="logs-06-1"><span class="qr-step">推導 1</span>generation 改變表示不能直接把這些 chunks 宣稱為同一份 capture。應標示一致性未確認，重新按該 log 的擷取與確認流程取得一份可追蹤的資料，而非只保留最後的 header。</p>
<p data-reasoning="logs-06-2"><span class="qr-step">推導 2</span>DA1LB=3 表示 Data Area 1 到 block 3；block 0 是 512-byte header，因此 header 加 Area 1 的範圍是 4×512=2048 bytes。這個長度資訊不會消除 generation 不一致。</p>
<p data-reasoning="logs-06-3"><span class="qr-step">推導 3</span>TCDA 是更新確認相關狀態，不是 payload 格式解碼器。即使完整取到同一代資料，內部內容仍可能由廠商定義；不能從共同 header 推測每個 vendor byte 的意義。</p>
<div class="qr-related">需要重看欄位時，接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-b223">Base 2.4 Figure 223 · Controller Telemetry：更新通知與 generation</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b204">Base 2.4 Figure 204 · Get Log CDW10：讀哪份、讀多少、是否確認事件</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b208">Base 2.4 Figure 208 · Get Log offset：byte 位置或清單 index</a></div>
<h4>本題原文定位</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.13.1.9 · Figure 223 · Telemetry Controller-Initiated Log Page · 文件頁 236–237 · PDF 262–263</li><li>Base 2.4 · §5.2.13 · Figure 204 · Get Log Page – Command Dword 10 · 文件頁 213 · PDF 239</li><li>Base 2.4 · §5.2.13 · Figure 208 · Get Log Page – Command Dword 14 · 文件頁 214–215 · PDF 240–241</li></ul></details>
<a href="#exercise-toc">回情境索引</a></article>
<article class="qr-card qr-case" id="exercise-logs-07" data-scenario="logs-07"><h3><span class="qr-number">練習 07</span>Persistent Event Log 的下一筆應從哪裡開始？</h3>
<p class="qr-case-question">解析器讀完第一筆就錯位，而且重新建立 context 後遇到 Command Sequence Error。請分別檢查生命週期與長度計算。</p><div class="qr-observations"><h4>模擬回傳與已知條件</h4><ul>
<li>ACT=3 成功回傳 header，RCE=0；未釋放 context。第一筆 offset=512、EHL=21、EL=28、VSIL=8。</li>
<li>header 的總長度足以容納此筆；ET／ETR 已確認為支援的格式。</li>
</ul></div><details class="qr-answer"><summary>展開解答：查詢路徑與完整推導</summary>
<p class="qr-route"><strong>查詢次序：</strong>Get Log Page LID=0Dh，以 ACT 管理 context；讀 header 後使用 ACT=0 讀取同一份 report，按 event header 走訪。</p>
<p data-reasoning="logs-07-1"><span class="qr-step">推導 1</span>ACT=3 的 RCE=0 表示命令處理前沒有 reporting context，不表示成功後仍沒有。此時再送 ACT=1 去建立，會與已存在的 context 衝突；後續讀取應沿用它。</p>
<p data-reasoning="logs-07-2"><span class="qr-step">推導 2</span>共同 header 長度為 EHL+3=24 bytes；EL=28 已包括 VSIL=8。Event Data 為 28−8=20 bytes，下一筆起點為 512+24+28=564，不能再加一次 VSIL。</p>
<p data-reasoning="logs-07-3"><span class="qr-step">推導 3</span>每筆仍要檢查長度是否超出 TLL、ET／ETR 是否可解，再繼續讀。完成後按規則釋放 context；讀完整個報告並不代表其中一定保存了系統歷史上每件事。</p>
<div class="qr-related">需要重看欄位時，接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-b232">Base 2.4 Figure 232 · Persistent Event Log：建立、讀取與釋放 context</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b233">Base 2.4 Figure 233 · Persistent Event header：總長、筆數與讀取版本</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b234">Base 2.4 Figure 234 · Persistent Event：下一筆從哪裡開始</a></div>
<h4>本題原文定位</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.13.1.14 · Figure 232 · Persistent Event Log Specific Parameter Field · 文件頁 246 · PDF 272</li><li>Base 2.4 · §5.2.13.1.14 · Figure 233 · Persistent Event Log Page · 文件頁 247–249 · PDF 273–275</li><li>Base 2.4 · §5.2.13.1.14 · Figure 234 · Persistent Event Format · 文件頁 249–250 · PDF 275–276</li></ul></details>
<a href="#exercise-toc">回情境索引</a></article>
</section>
<nav class="qr-toc" id="figure-index" aria-label="本冊圖表索引"><h2>本冊圖表</h2><ol>
<li><a href="#figure-b204">Base 2.4 Figure 204 · Get Log CDW10：讀哪份、讀多少、是否確認事件</a></li>
<li><a href="#figure-b205">Base 2.4 Figure 205 · Get Log CDW11：長度高位與目標識別</a></li>
<li><a href="#figure-b208">Base 2.4 Figure 208 · Get Log offset：byte 位置或清單 index</a></li>
<li><a href="#figure-b211">Base 2.4 Figure 211 · Supported Log Pages：這個 LID 能不能用</a></li>
<li><a href="#figure-b212">Base 2.4 Figure 212 · Error Information：把錯誤對回命令與欄位</a></li>
<li><a href="#figure-b213">Base 2.4 Figure 213 · SMART：警告、累計量、溫度與時間</a></li>
<li><a href="#figure-b217">Base 2.4 Figure 217 · Command Effects：支援與執行影響</a></li>
<li><a href="#figure-b221">Base 2.4 Figure 221 · Host Telemetry：header 與累積資料區邊界</a></li>
<li><a href="#figure-b223">Base 2.4 Figure 223 · Controller Telemetry：更新通知與 generation</a></li>
<li><a href="#figure-b225">Base 2.4 Figure 225 · Endurance Group：逐組健康與容量</a></li>
<li><a href="#figure-b232">Base 2.4 Figure 232 · Persistent Event Log：建立、讀取與釋放 context</a></li>
<li><a href="#figure-b233">Base 2.4 Figure 233 · Persistent Event header：總長、筆數與讀取版本</a></li>
<li><a href="#figure-b234">Base 2.4 Figure 234 · Persistent Event：下一筆從哪裡開始</a></li>
<li><a href="#figure-b236">Base 2.4 Figure 236 · Persistent Event 類型：去哪個內容格式查</a></li>
<li><a href="#figure-p75">PCIe Transport 1.4 Figure 75 · PCIe EOM Header：量測完成了嗎、有多少描述子</a></li>
<li><a href="#figure-p76">PCIe Transport 1.4 Figure 76 · EOM Lane Descriptor：眼圖外框與資料限制</a></li>
</ol></nav>
<article class="qr-card" id="figure-b204" data-figure="B204">
<h2><span class="qr-number">01</span>Get Log CDW10：讀哪份、讀多少、是否確認事件</h2>
<p class="qr-original">Base 2.4 · Figure 204 · Get Log Page – Command Dword 10</p>
<p class="qr-location">§5.2.13 · 文件頁 213 · PDF 239</p>
<p class="qr-explanation" data-paragraph="B204-1"><span class="qr-step">01.1 · 用途</span>同一個 log 讀取命令可能附帶確認非同步事件的效果。查此表時，同時保留 LID、LSP 和 RAE，不只記錄 buffer 長度。</p>
<p class="qr-explanation" data-paragraph="B204-2"><span class="qr-step">01.2 · 欄位與關係</span>LID bits7:0 選 log；LSP bits14:8 由該 log 定義；RAE bit15 為保留事件；NUMDL bits31:16 是 Dwords 數量的低 16bits，與 NUMDU 合成後為減 1 編碼。RAE=0 通常在命令成功時確認相應事件，並非刪除所有 log 內容。</p>
<p class="qr-explanation" data-paragraph="B204-3"><span class="qr-step">01.3 · 判讀與例子</span>一般 512-byte 讀取需 128 Dwords，因此 NUMD=127。失敗的 Get Log 不能視為已確認事件；各 log 若另定動作或長度規則，應使用該 log 規則，例如 PEL 的 ACT3。</p>
<p class="qr-tags">搜尋詞：Get Log Page · LID · LSP · RAE · NUMDL</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-b205">Base 2.4 Figure 205 · Get Log CDW11：長度高位與目標識別</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b232">Base 2.4 Figure 232 · Persistent Event Log：建立、讀取與釋放 context</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b205" data-figure="B205">
<h2><span class="qr-number">02</span>Get Log CDW11：長度高位與目標識別</h2>
<p class="qr-original">Base 2.4 · Figure 205 · Get Log Page – Command Dword 11</p>
<p class="qr-location">§5.2.13 · 文件頁 214 · PDF 240</p>
<p class="qr-explanation" data-paragraph="B205-1"><span class="qr-step">02.1 · 用途</span>需要讀大型 log 或指定某個資源對象時，查 CDW11。上半部 LSI 不是 NUMD 的更多高位。</p>
<p class="qr-explanation" data-paragraph="B205-2"><span class="qr-step">02.2 · 欄位與關係</span>NUMDU bits15:0 與 CDW10.NUMDL 組成 32-bit 減 1Dword 數；LSI bits31:16 是 log-specific identifier，含義由 LID 決定。一般長度為 4×(((NUMDU&lt;&lt;16)|NUMDL)+1) bytes。</p>
<p class="qr-explanation" data-paragraph="B205-3"><span class="qr-step">02.3 · 判讀與例子</span>NUMDU=1、NUMDL=0 對應 262148bytes，不是 65536bytes。LID09h 則利用 LSI 指定 Endurance Group，不能把其值誤加到傳輸長度。</p>
<p class="qr-tags">搜尋詞：NUMDU · LSI · Endurance Group Identifier · Get Log Page</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-b204">Base 2.4 Figure 204 · Get Log CDW10：讀哪份、讀多少、是否確認事件</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b225">Base 2.4 Figure 225 · Endurance Group：逐組健康與容量</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b208" data-figure="B208">
<h2><span class="qr-number">03</span>Get Log offset：byte 位置或清單 index</h2>
<p class="qr-original">Base 2.4 · Figure 208 · Get Log Page – Command Dword 14</p>
<p class="qr-location">§5.2.13 · 文件頁 214–215 · PDF 240–241</p>
<p class="qr-explanation" data-paragraph="B208-1"><span class="qr-step">03.1 · 用途</span>分段讀 log 位置不對時，先查 OT。相同 LPO 數字可以表示 bytes，也可以表示第幾個資料結構；這就是 index offset 與 byte offset 的差別。</p>
<p class="qr-explanation" data-paragraph="B208-2"><span class="qr-step">03.2 · 欄位與關係</span>OT bit23 為 0 時，CDW12／13 的 LPO 表示 byte offset；為 1 時表示清單 index，需該 log 支援。CSI bits31:24 選相關 I/O command set，UIDX bits6:0 為 UUID index；兩者也有各自使用條件。</p>
<p class="qr-explanation" data-paragraph="B208-3"><span class="qr-step">03.3 · 判讀與例子</span>對支援 index 的 log，LPO=2、OT=1 表示 index2；OT=0 則只是距 log 起點 2bytes，而且還需符合該讀取方式的對齊要求。不能把兩種值直接互換。</p>
<p class="qr-tags">搜尋詞：OT · LPO · index offset · byte offset · CSI · UIDX</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-b211">Base 2.4 Figure 211 · Supported Log Pages：這個 LID 能不能用</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b204">Base 2.4 Figure 204 · Get Log CDW10：讀哪份、讀多少、是否確認事件</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b211" data-figure="B211">
<h2><span class="qr-number">04</span>Supported Log Pages：這個 LID 能不能用</h2>
<p class="qr-original">Base 2.4 · Figure 211 · LID Supported and Effects Data Structure</p>
<p class="qr-location">§5.2.13.1.1 · 文件頁 217–218 · PDF 243–244</p>
<p class="qr-explanation" data-paragraph="B211-1"><span class="qr-step">04.1 · 用途</span>在送特殊 log 動作或 index-offset 讀取前，查該 LID 的能力描述子。知道 LID 有標準定義，不等於此裝置一定支援。</p>
<p class="qr-explanation" data-paragraph="B211-2"><span class="qr-step">04.2 · 欄位與關係</span>LSUPP bit0 表示支援，IOS bit1 表示可用 index offset，LIDSP bits31:16 補此 LID 特定能力。LSUPP=0 時忽略其他欄位；IOS 也受 Get Log extended-data 能力條件限制。</p>
<p class="qr-explanation" data-paragraph="B211-3"><span class="qr-step">04.3 · 判讀與例子</span>LSUPP=1、IOS=0 表示可讀此 log，但不能送 OT=1。PEL 的 LIDSP 還可告知擴充 context/header 能力，不能把所有 LIDSP 都當同一種 bitmap。</p>
<p class="qr-tags">搜尋詞：LID 00h · LSUPP · IOS · LIDSP · SPEDS</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-b208">Base 2.4 Figure 208 · Get Log offset：byte 位置或清單 index</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b232">Base 2.4 Figure 232 · Persistent Event Log：建立、讀取與釋放 context</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b212" data-figure="B212">
<h2><span class="qr-number">05</span>Error Information：把錯誤對回命令與欄位</h2>
<p class="qr-original">Base 2.4 · Figure 212 · Error Information Log Entry Data Structure</p>
<p class="qr-location">§5.2.13.1.2 · 文件頁 218–220 · PDF 244–246</p>
<p class="qr-explanation" data-paragraph="B212-1"><span class="qr-step">05.1 · 用途</span>CQE 的 M=1 或錯誤事件需要更多資訊時，查此 64-byte entry。清單從較新錯誤開始，單筆 entry 包含命令身分、狀態與可能的參數位置。</p>
<p class="qr-explanation" data-paragraph="B212-2"><span class="qr-step">05.2 · 欄位與關係</span>ECNT bytes7:0 是錯誤序號，0 表示無效 entry；SQID9:8、CID11:10 對命令，STS13:12 對狀態。Parameter Error Location 在 15:14，BYTLOC 指定 SQE byte、BITLOC 指定該 byte 的 bit。NSID、CSI、OPC、CSINFO 與 LPVER 進一步限定解讀。</p>
<p class="qr-explanation" data-paragraph="B212-3"><span class="qr-step">05.3 · 判讀與例子</span>BYTLOC=40、BITLOC=3 指向 SQE byte40 的 bit3，即 CDW10 bit3，不是第 40 個 Dword。不是特定命令的錯誤可用 FFFFh 表示 SQID／CID；這裡 PEL 是 Parameter Error Location，與 Persistent Event Log 縮寫相同但含義不同。</p>
<p class="qr-tags">搜尋詞：LID 01h · ECNT · SQID · CID · PEL · BYTLOC · BITLOC · LPVER</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Status：類別、錯誤碼與重試提示</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b93">Base 2.4 Figure 93 · 64-byte 命令的共同位置</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b213" data-figure="B213">
<h2><span class="qr-number">06</span>SMART：警告、累計量、溫度與時間</h2>
<p class="qr-original">Base 2.4 · Figure 213 · SMART / Health Information Log Page</p>
<p class="qr-location">§5.2.13.1.3 · 文件頁 221–225 · PDF 247–251</p>
<p class="qr-explanation" data-paragraph="B213-1"><span class="qr-step">06.1 · 用途</span>健康與效能驗證常讀這張表，但它混合目前狀態、終生累計量與不同單位的時間。先分欄位種類，才有意義地比較兩次快照。</p>
<p class="qr-explanation" data-paragraph="B213-2"><span class="qr-step">06.2 · 欄位與關係</span>CW 是警告 bitmap，CTEMP 是 Kelvin，PUSED 是壽命估計百分比；DUR／DUW 以 1000×512-byte 單位向上取整，0 表示未回報。HRC／HWC 計命令，CBT 計分鐘，POH 計小時；thermal 管理總時間則以秒計。sensor 值 0 表示未實作。</p>
<p class="qr-explanation" data-paragraph="B213-3"><span class="qr-step">06.3 · 判讀與例子</span>DUR 增加 1 不必然等於剛好傳了 512000bytes，因為它是取整後計量。PUSED 超過 100 也不直接等於裝置已故障；需一起看警告、媒體錯誤與具體行為。</p>
<p class="qr-tags">搜尋詞：LID 02h · SMART · CW · CTEMP · DUR · DUW · POH · PUSED · TMT</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/features/zh-tw/#figure-b482">Base 2.4 Figure 482 · HCTM：兩個熱管理門檻</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b225">Base 2.4 Figure 225 · Endurance Group：逐組健康與容量</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b233">Base 2.4 Figure 233 · Persistent Event header：總長、筆數與讀取版本</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b217" data-figure="B217">
<h2><span class="qr-number">07</span>Command Effects：支援與執行影響</h2>
<p class="qr-original">Base 2.4 · Figure 217 · Commands Supported and Effects Data Structure</p>
<p class="qr-location">§5.2.13.1.6 · 文件頁 228–229 · PDF 254–255</p>
<p class="qr-explanation" data-paragraph="B217-1"><span class="qr-step">07.1 · 用途</span>操作前要知道會改資料、namespace 清單還是 controller 能力，查這張 effects 描述子。它提供能力與協調建議，不是某次命令已造成哪些改動的歷史紀錄。</p>
<p class="qr-explanation" data-paragraph="B217-2"><span class="qr-step">07.2 · 欄位與關係</span>CSUPP bit0 為支援；LBCC1、NCC2、NIC3、CCC4 分別表示可能改資料、單一 namespace 能力、namespace inventory 與 controller 能力。CSE bits18:16 及 CSER15:14 給提交／執行建議；CSP31:20 描述可能作用範圍。</p>
<p class="qr-explanation" data-paragraph="B217-3"><span class="qr-step">07.3 · 判讀與例子</span>NIC=1 表示操作可能改變 namespace 清單，成功後應考慮重新查詢；不能由此推論剛剛一定新增一個 namespace。理解非 0 CSER 的主機應依其較新建議判讀，而非把 CSE 與 CSER 不加區分地疊加。</p>
<p class="qr-tags">搜尋詞：LID 05h · CSUPP · LBCC · NCC · NIC · CCC · CSE · CSER · CSP</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify Controller：能力與限制的主要入口</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b446">Base 2.4 Figure 446 · Namespace Management：Create、Delete 或 Restore</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b221" data-figure="B221">
<h2><span class="qr-number">08</span>Host Telemetry：header 與累積資料區邊界</h2>
<p class="qr-original">Base 2.4 · Figure 221 · Telemetry Host-Initiated Log Page</p>
<p class="qr-location">§5.2.13.1.8 · 文件頁 234–235 · PDF 260–261</p>
<p class="qr-explanation" data-paragraph="B221-1"><span class="qr-step">08.1 · 用途</span>擷取 host-initiated telemetry 後，用此 header 決定資料區大小和本次版本。資料 payload 通常由廠商定義，header 提供可共同判讀的外框。</p>
<p class="qr-explanation" data-paragraph="B221-2"><span class="qr-step">08.2 · 欄位與關係</span>前 512bytes 為 header；DA1／2／3／4 Last Block 指出各區最後的 512-byte block 編號，資料從 block1 開始，區域是累積擴大的集合。THS 在 byte380、THDGN381；382／383 另帶 controller telemetry 的狀態與 generation 副本。</p>
<p class="qr-explanation" data-paragraph="B221-3"><span class="qr-step">08.3 · 判讀與例子</span>DA1LB=2、DA2LB=5 代表區域 1 含 blocks1～2，區域 2 含 1～5，不是另外接 5blocks。分段讀取要保留 generation 及擷取操作，避免把不同時點資料拼在一起。</p>
<p class="qr-tags">搜尋詞：LID 07h · Telemetry Host-Initiated · THDA1LB · THDGN · THS</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-b223">Base 2.4 Figure 223 · Controller Telemetry：更新通知與 generation</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b204">Base 2.4 Figure 204 · Get Log CDW10：讀哪份、讀多少、是否確認事件</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b223" data-figure="B223">
<h2><span class="qr-number">09</span>Controller Telemetry：更新通知與 generation</h2>
<p class="qr-original">Base 2.4 · Figure 223 · Telemetry Controller-Initiated Log Page</p>
<p class="qr-location">§5.2.13.1.9 · 文件頁 236–237 · PDF 262–263</p>
<p class="qr-explanation" data-paragraph="B223-1"><span class="qr-step">09.1 · 用途</span>controller 主動保存 telemetry 時，這張 header 用於判斷回報範圍、未確認更新與資料版本。不要把通知狀態當資料長度。</p>
<p class="qr-explanation" data-paragraph="B223-2"><span class="qr-step">09.2 · 欄位與關係</span>TCS 在 byte381，TCDA382，TCDGN383；各 data-area last-block 欄仍描述累積範圍。Base2.4 的 TCDA 表示自上次成功 RAE=0 確認後是否有更新，TCDGN 則追蹤擷取代數。</p>
<p class="qr-explanation" data-paragraph="B223-3"><span class="qr-step">09.3 · 判讀與例子</span>TCDA=0 可以是先前更新已確認，不足以證明沒有 saved telemetry 資料。把 LID07h 的 byte381 當 TCS 也會讀錯，因為 07h 在此位置是 THDGN。</p>
<p class="qr-tags">搜尋詞：LID 08h · TCDA · TCDGN · TCS · Telemetry Controller-Initiated</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-b221">Base 2.4 Figure 221 · Host Telemetry：header 與累積資料區邊界</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b204">Base 2.4 Figure 204 · Get Log CDW10：讀哪份、讀多少、是否確認事件</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b225" data-figure="B225">
<h2><span class="qr-number">10</span>Endurance Group：逐組健康與容量</h2>
<p class="qr-original">Base 2.4 · Figure 225 · Endurance Group Information Log Page</p>
<p class="qr-location">§5.2.13.1.10 · 文件頁 238–239 · PDF 264–265</p>
<p class="qr-explanation" data-paragraph="B225-1"><span class="qr-step">10.1 · 用途</span>controller 的總體 SMART 不能完整回答每個 Endurance Group 的健康狀況時，查 LID09h。先用 LSI 指定 group，避免比較到不同群組。</p>
<p class="qr-explanation" data-paragraph="B225-2"><span class="qr-step">10.2 · 欄位與關係</span>內容包括 Critical Warning、Available Spare／Threshold、Percentage Used、資料讀寫及媒體寫入累計量、錯誤數與容量欄位。每個欄位的計量不同，Group 的 ENDGID 可由 namespace Identify 找到。</p>
<p class="qr-explanation" data-paragraph="B225-3"><span class="qr-step">10.3 · 判讀與例子</span>同一 controller 下 group1 出現警告，不表示 group2 同時有相同警告。比較兩份 log 時先固定 ENDGID 與時間；讀取確認通知，也不代表原健康問題已被修復。</p>
<p class="qr-tags">搜尋詞：LID 09h · Endurance Group · CW · AVSP · PUSED · ENDGID</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-b205">Base 2.4 Figure 205 · Get Log CDW11：長度高位與目標識別</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-b346">Base 2.4 Figure 346 · Namespace 共通狀態：可用、受保護與儲存歸屬</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b213">Base 2.4 Figure 213 · SMART：警告、累計量、溫度與時間</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b232" data-figure="B232">
<h2><span class="qr-number">11</span>Persistent Event Log：建立、讀取與釋放 context</h2>
<p class="qr-original">Base 2.4 · Figure 232 · Persistent Event Log Specific Parameter Field</p>
<p class="qr-location">§5.2.13.1.14 · 文件頁 246 · PDF 272</p>
<p class="qr-explanation" data-paragraph="B232-1"><span class="qr-step">11.1 · 用途</span>分多次讀持久事件時，用 ACT 管理 reporting context，也就是這次固定下來供讀取的事件集合。context 不是事件種類。</p>
<p class="qr-explanation" data-paragraph="B232-2"><span class="qr-step">11.2 · 欄位與關係</span>ACT=0 讀既有 context，1 建立並讀取，2 釋放，3 在必要時建立或沿用並讀 header。ACT1 遇到已存在 context 會出錯；ACT3 成功時固定回 offset0 的 512-byte header，忽略一般 NUMD／LPO 長度位置，buffer 仍須足夠。</p>
<p class="qr-explanation" data-paragraph="B232-3"><span class="qr-step">11.3 · 判讀與例子</span>ACT3 回 RCE=0 表示處理命令前尚無 context，不表示建立失敗。成功後接 ACT0 讀事件即可；再送 ACT1 反而可能得到 Command Sequence Error。</p>
<p class="qr-tags">搜尋詞：LID 0Dh · ACT · context · ACT 3 · PEL</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-b233">Base 2.4 Figure 233 · Persistent Event header：總長、筆數與讀取版本</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b234">Base 2.4 Figure 234 · Persistent Event：下一筆從哪裡開始</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b233" data-figure="B233">
<h2><span class="qr-number">12</span>Persistent Event header：總長、筆數與讀取版本</h2>
<p class="qr-original">Base 2.4 · Figure 233 · Persistent Event Log Page</p>
<p class="qr-location">§5.2.13.1.14 · 文件頁 247–249 · PDF 273–275</p>
<p class="qr-explanation" data-paragraph="B233-1"><span class="qr-step">12.1 · 用途</span>開始走訪持久事件前，先從 header 取得總長與版本。log header 版本、generation 及單筆 event revision 是不同欄位。</p>
<p class="qr-explanation" data-paragraph="B233-2"><span class="qr-step">12.2 · 欄位與關係</span>TNEV bytes7:4 為事件筆數，TLL15:8 為整份 bytes，LREV16 為版本，LHL19:18 加 20 才是 header 長度。GNUM373:372 用於識別新建立且內容不同的 report；RCI 含 RCE。SEB511:480 則表示事件種類支援，不是目前有哪些事件。</p>
<p class="qr-explanation" data-paragraph="B233-3"><span class="qr-step">12.3 · 判讀與例子</span>LHL=492 得到 512-byte header；TNEV=0 仍有 header。分段讀取需比對 context 與 GNUM，但相同 generation 不應被當成跨 reset 資料必定相同的無限期保證。</p>
<p class="qr-tags">搜尋詞：TLL · TNEV · LHL · LREV · GNUM · RCE · SEB</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-b232">Base 2.4 Figure 232 · Persistent Event Log：建立、讀取與釋放 context</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b234">Base 2.4 Figure 234 · Persistent Event：下一筆從哪裡開始</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b234" data-figure="B234">
<h2><span class="qr-number">13</span>Persistent Event：下一筆從哪裡開始</h2>
<p class="qr-original">Base 2.4 · Figure 234 · Persistent Event Format</p>
<p class="qr-location">§5.2.13.1.14 · 文件頁 249–250 · PDF 275–276</p>
<p class="qr-explanation" data-paragraph="B234-1"><span class="qr-step">13.1 · 用途</span>持久事件長度可變，這張表是逐筆走訪的關鍵。先由 header 決定事件邊界，再按種類解內容，不使用固定 stride。</p>
<p class="qr-explanation" data-paragraph="B234-2"><span class="qr-step">13.2 · 欄位與關係</span>ET byte0 選種類，ETR1 選內容版本，EHL2 加 3 是共同 header 長度；VSIL bytes21:20 給 vendor 資訊長度，EL23:22 包含 VSI 與 Event Data。下一筆起點=目前起點+EHL+3+EL，ED 長度=EL−VSIL。</p>
<p class="qr-explanation" data-paragraph="B234-3"><span class="qr-step">13.3 · 判讀與例子</span>起點 512、EHL21、VSIL4、EL20 時，header24bytes，ED16bytes，下一筆在 556。若再把 VSIL 加一次會走到 560 而錯位；也不能擅自讓每筆補到 4-byte 倍數。</p>
<p class="qr-tags">搜尋詞：ET · ETR · EHL · VSIL · EL · VSI · ED · ETSTP</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-b233">Base 2.4 Figure 233 · Persistent Event header：總長、筆數與讀取版本</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b236">Base 2.4 Figure 236 · Persistent Event 類型：去哪個內容格式查</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b236" data-figure="B236">
<h2><span class="qr-number">14</span>Persistent Event 類型：去哪個內容格式查</h2>
<p class="qr-original">Base 2.4 · Figure 236 · Persistent Event Log Event Types</p>
<p class="qr-location">§5.2.13.1.14.2 · 文件頁 251 · PDF 277</p>
<p class="qr-explanation" data-paragraph="B236-1"><span class="qr-step">14.1 · 用途</span>共同 event header 解完後，用此表按 ET 找到內容格式。它也列出記錄要求和版本，適合查「這個 ET 代表什麼」及「應套哪版格式」。</p>
<p class="qr-explanation" data-paragraph="B236-2"><span class="qr-step">14.2 · 欄位與關係</span>常用 01h 健康快照、02h 韌體、04hreset、05h 硬體、06hnamespace、07h／08h Format 開始／完成、09h／0Ah Sanitize 開始／完成、0Bh 設定、0Ch Telemetry、0Dh 溫度。支援要求還受起因命令與控制器條件影響。</p>
<p class="qr-explanation" data-paragraph="B236-3"><span class="qr-step">14.3 · 判讀與例子</span>看見 ET0Ah 只能先辨認 Sanitize 完成事件類型，成功與否仍看其 payload 的結果狀態。ETR 不是事件計數；支援某種類型也不保證此次 report 一定包含該類事件。</p>
<p class="qr-tags">搜尋詞：ET · ETR · Firmware Event · Namespace Change · Sanitize Event</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-b234">Base 2.4 Figure 234 · Persistent Event：下一筆從哪裡開始</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b312">Base 2.4 Figure 312 · Sanitize Status：進度、結果與目前狀態</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-p75" data-figure="P75">
<h2><span class="qr-number">15</span>PCIe EOM Header：量測完成了嗎、有多少描述子</h2>
<p class="qr-original">PCIe Transport 1.4 · Figure 75 · EOM Header</p>
<p class="qr-location">§3.9.1.1 · 文件頁 42–43 · PDF 42–43</p>
<p class="qr-explanation" data-paragraph="P75-1"><span class="qr-step">15.1 · 用途</span>需要接收端眼圖資料時，先查 Eye Opening Measurement header，確認量測是否完成、版本與資料長度。不能看到 log 有回覆就直接分析眼圖。</p>
<p class="qr-explanation" data-paragraph="P75-2"><span class="qr-step">15.2 · 欄位與關係</span>EOMIP byte1 的 0／1／2 為未啟動、進行中、已完成；HSIZE bytes3:2 為 64，RSZ7:4 為 log bytes，EDGN8 為 generation，LREV9 本版為 3。DS bytes23:20 給描述子大小，ND25:24 給筆數；ODP 決定可選眼圖資料是否存在。</p>
<p class="qr-explanation" data-paragraph="P75-3"><span class="qr-step">15.3 · 判讀與例子</span>ND 是實際回傳描述子數，不能只用 lane 數當迴圈上限；每 lane 可能有多個 eye。先確認 EOMIP=2，再按 DS 前進，並保留量測時的 link 資訊。</p>
<p class="qr-tags">搜尋詞：LID 19h · EOM · EOMIP · EDGN · HSIZE · RSZ · DS · ND · EPL</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-p76">PCIe Transport 1.4 Figure 76 · EOM Lane Descriptor：眼圖外框與資料限制</a><a href="/nvme/figure-reference/init/zh-tw/#figure-p55">PCIe Transport 1.4 Figure 55 · PCIe Link：目前談成的速度與寬度</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-p76" data-figure="P76">
<h2><span class="qr-number">16</span>EOM Lane Descriptor：眼圖外框與資料限制</h2>
<p class="qr-original">PCIe Transport 1.4 · Figure 76 · EOM Lane Descriptor</p>
<p class="qr-location">§3.9.1.1 · 文件頁 43–45 · PDF 43–45</p>
<p class="qr-explanation" data-paragraph="P76-1"><span class="qr-step">16.1 · 用途</span>每份描述子對應一個 lane 的一個 eye。查此表可把量測對象、成功狀態與可列印圖形對上，避免把不同 lane 或 eye 混在一起。</p>
<p class="qr-explanation" data-paragraph="P76-2"><span class="qr-step">16.2 · 欄位與關係</span>MSTAT byte1 的 bit0 為量測成功，LN2 為 lane、EYE3 為 eye；TOP／BTM／LFT／RGT 描述圖形邊界，NROWS13:12 與 NCOLS15:14 給字元矩陣大小，EDLEN19:16 給 vendor eye data 長度。Printable Eye 從 byte32 開始，是否存在看 header ODP。</p>
<p class="qr-explanation" data-paragraph="P76-3"><span class="qr-step">16.3 · 判讀與例子</span>若 NROWS=5、NCOLS=7，字元矩陣佔 35bytes；若它存在，後面的 Eye Data 從 67 開始。可列印的 0／1 形狀不足以判定 signal integrity，還需電壓、時間尺度、BER 門檻等量測資訊。</p>
<p class="qr-tags">搜尋詞：MSTAT · LN · EYE · NROWS · NCOLS · EDLEN · Printable Eye · BER</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-p75">PCIe Transport 1.4 Figure 75 · PCIe EOM Header：量測完成了嗎、有多少描述子</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<footer id="source-files"><h2>原始文件</h2><p>頁碼採本次提供的 ratified PDF；Base 的 PDF 頁＝文件頁＋26，另兩份相同。圖號與英文原名保留，可用 PDF 搜尋定位。公開網站不附原始 PDF。</p><ul class="qr-sources"><li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li></ul></footer>
</main></div>
