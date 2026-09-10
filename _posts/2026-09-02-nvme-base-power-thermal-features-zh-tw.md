---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4：Power／Thermal Features 與 Power Management"
date: 2026-09-02
description: "從主題主軸到關鍵機制、條件與例子的 NVMe 技術報告。"
lang: zh-Hant-TW
img: posts/2026/dogMC_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
nvme_notes: true
---
[English]({% post_url 2026-09-02-nvme-base-power-thermal-features-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">NVMe 的功耗與溫度管理是在耗電、回應延遲與工作能力之間做取捨。本篇先建立 power state 的意義，再說明主機設定、自動閒置轉移與溫度相關控制如何分工。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express，主機與非揮發性記憶體子系統之間的介面規範家族。</dd></div></dl>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>功耗狀態</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">比較功耗、可否處理 I/O，以及進出狀態的延遲。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl></article>
<article><span class="axis-number">02</span><h3>設定與自動轉移</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">理解 Get／Set Features、APST 與背景工作的限制。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>APST</dt><dd>Autonomous Power State Transition；依設定的閒置條件自動轉換電源狀態。</dd></div></dl></article>
<article><span class="axis-number">03</span><h3>溫度控制</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">分開溫度事件通知與控制器的熱管理行為。</span></p></article>
</div>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">Features 是控制器提供給主機查詢或設定的功能。支援某個功能、目前功能值，以及設定能否跨斷電保存，是不同資訊。</span></p>
<div class="overview-connections"><h3>把主軸連起來</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.03">00.03.</span><span class="paragraph-text">電源管理在功耗、恢復服務所需時間與溫度之間安排操作。先理解電源狀態有哪些能力，再看主機如何讀寫 Feature；APST 依閒置時間轉換狀態，溫度門檻與 HCTM 則依溫度處理不同問題。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>HCTM</dt><dd>Host Controlled Thermal Management；由 host 設定溫度門檻的熱管理機制。</dd></div></dl>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.04">00.04.</span><span class="paragraph-text">通知門檻用來回報溫度事件，熱管理門檻用來控制行為，兩者不能互換。學完應能解釋選擇較省電狀態可能帶來哪些延遲，以及設定值、目前狀態和累計統計分別告訴我們什麼。</span></p>
</div>
</section>
<section class="lesson" id="module-feature-read-set-loop"><h2 id="heading-feature-read-set-loop"><span class="section-number">01</span> Feature 的能力、讀取與設定</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">Feature 不是一個單純 register。Host 要先用 SEL=011b 讀 capability，再分別讀 current／default／saved view，確認 scope 與 persistence 後才寫入。Set completion 只證明 command outcome；重新 Get 與 runtime telemetry 才能證明軟體看見的新 policy。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div><div><dt>SEL</dt><dd>Select，Get Features 用來選 current、default、saved 或 supported-capabilities view 的欄位。</dd></div></dl>
<!-- claim:BASEPOWER-READ-FIRST -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">Get Features 是讀取 Feature 屬性的 Admin command。工程流程不應從寫入猜測開始，而要先辨認 FID、查 capability，再取得 current／default／保存值。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div><div><dt>FID</dt><dd>Feature Identifier；指定要讀取或設定哪一項 Feature 的編號。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, 文件頁 209, PDF 頁 235</p></details>
<div class="table-wrap"><table><caption>Feature 的能力、讀取與設定</caption><thead><tr><th scope="col">Get Features 選擇值</th><th scope="col">要求讀取什麼</th><th scope="col">可用來做哪種判斷</th></tr></thead><tbody><tr><td>SEL=000b</td><td>目前值</td><td>確認控制器目前採用的設定</td></tr><tr><td>SEL=001b</td><td>預設值</td><td>了解預設設定</td></tr><tr><td>SEL=010b</td><td>保存值</td><td>不等於一定曾經 save</td></tr><tr><td>SEL=011b</td><td>CHANG／NSSPEC／SVBL</td><td>寫入前的 功能支援條件</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>NSSPEC</dt><dd>Namespace Specific，指出 Feature 是否具有 per-namespace scope 的 capability bit。</dd></div><div><dt>CHANG</dt><dd>Changeable，指出 Feature value 是否可由 Set Features 變更的 capability bit。</dd></div><div><dt>SVBL</dt><dd>Saveable，supported-capabilities result 中指出 Feature 是否可保存的 bit。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">讀 FID 02h current 時 CDW10=00000002h；讀 supported capabilities 時 SEL=3，所以 CDW10=(3×100h)+02h=00000302h。若 CHANG=0，流程在 Set 前停止；若 CHANG=1，再依 NPSS 與 PSD 組合 CDW11。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NPSS</dt><dd>Number of Power States Support，以 0's-based 方式回報最高支援 power-state number。</dd></div><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div><div><dt>PSD</dt><dd>Power State Descriptor，描述一個 power state 的 power、latency、operational 屬性與 relative performance。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-power-state-mental-model"><h2 id="heading-power-state-mental-model"><span class="section-number">02</span> Power State 的功率、延遲與效能</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">只看 state number 無法判斷是否適合 workload。每一個 PSD 要一起讀 MP、NOPS、ENLAT／EXLAT、IDLP／ACTP 與 relative performance。PS 數字增加通常降低 maximum power，但不代表所有 latency 或 throughput 一定以固定比例變差。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>ENLAT</dt><dd>Entry Latency，進入該 power state 的 maximum latency，單位為 microseconds。</dd></div><div><dt>EXLAT</dt><dd>Exit Latency，離開該 power state 的 maximum latency，單位為 microseconds。</dd></div><div><dt>ACTP</dt><dd>Active Power，在指定 workload 與時間窗下描述的 average active power。</dd></div><div><dt>IDLP</dt><dd>Idle Power，依規格 idle 測量條件描述的 typical power。</dd></div><div><dt>NOPS</dt><dd>Non-Operational State，Power State Descriptor 中指出該 state 不處理 I/O commands 的 bit。</dd></div><div><dt>MP</dt><dd>Maximum Power，一個 power state 的 sustained maximum power。</dd></div><div><dt>PS</dt><dd>Power State，controller 的功耗／效能 operating point；PS0 是最高 maximum-power state。</dd></div></dl>
<!-- claim:BASEPOWER-POWER-STATES -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">controller 必須（shall）至少支援一個 power state，最多可（may）支援 32 個，編號從 0 連續排列。PS0 的 maximum power 最高；後續 state 的 maximum power 不得高於前一個 state。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.19</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19, 文件頁 666-667, PDF 頁 692-693</p></details>
<div class="table-wrap"><table><caption>Power State 的功率、延遲與效能</caption><thead><tr><th scope="col">電源狀態屬性</th><th scope="col">描述的功耗或效能</th><th scope="col">比較時需要的條件</th></tr></thead><tbody><tr><td>MP</td><td>持續最大功率</td><td>不是瞬間 sample</td></tr><tr><td>IDLP／ACTP</td><td>閒置典型功率／工作中平均功率</td><td>測量條件不同</td></tr><tr><td>ENLAT／EXLAT</td><td>進入／離開 maximum latency</td><td>跨 state 必須相加</td></tr><tr><td>RRT/RRL/RWT/RWL</td><td>相對吞吐量／相對延遲</td><td>只在同類 characteristic 比較</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">說明性計算：目前 PS1.EXLAT=100 µs，目標 PS3.ENLAT=2500 µs，直接 transition budget=2600 µs。若 controller 路徑是 PS1→PS2→PS3，還要加入 PS1.EXLAT+PS2.ENLAT 與 PS2.EXLAT+PS3.ENLAT 的每一段，不可仍用 2600 µs。</span></p></aside>
</section>
<section class="lesson" id="module-apst-state-machine"><h2 id="heading-apst-state-machine"><span class="section-number">03</span> APST 的閒置條件與自動轉換</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">APST 的 256-byte buffer 不是 performance table，而是 32 個『idle 多久後進哪個 non-operational state』的 rules。APSTE 決定 timer rules 是否生效；每個 ITPT=0 entry 不參與；I/O 到達又會讓 controller 回到最近 operational state。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>APSTE</dt><dd>Autonomous Power State Transition Enable，啟用 APST table timer 判斷的 bit。</dd></div><div><dt>ITPT</dt><dd>Idle Time Prior to Transition，APST entry 的 idle threshold，單位為 milliseconds。</dd></div></dl>
<figure><figcaption><strong>閒置時間如何影響功耗狀態</strong></figcaption><ol class="flow-steps"><li>Host 設定 APST entries 的閒置時間 ITPT 與目標狀態 ITPS。</li><li>啟用 APST 後，controller 依閒置計時判斷轉移。</li><li>到達適用門檻後，進入指定 non-operational power state。</li><li>恢復處理 I/O 前，需要計入離開該狀態的延遲。</li></ol><figcaption>APST 以閒置時間換取節能，同時引入狀態轉移延遲。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>ITPS</dt><dd>Idle Transition Power State，APST entry 選擇的目標 non-operational power state。</dd></div></dl>
<!-- claim:BASEPOWER-FID0C -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span><span class="paragraph-text">FID 0Ch 的 APSTE=1 啟用 Autonomous Power State Transition（APST）；預設值是 0。啟用只表示 controller 可依 APST table 的 idle timer 自主切換，並不保證一定進入任何特定 state。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, 文件頁 468-469, PDF 頁 494-495</p></details>
<div class="table-wrap"><table><caption>APST 的閒置條件與自動轉換</caption><thead><tr><th scope="col">APST 或背景工作設定</th><th scope="col">控制器如何進入或使用狀態</th><th scope="col">受哪些條件限制</th></tr></thead><tbody><tr><td>APSTE=0</td><td>只允許 host-directed entry</td><td>table 可存在但 timer 不驅動</td></tr><tr><td>APSTE=1</td><td>host 或 timer entry</td><td>ITPT 必須連續滿足</td></tr><tr><td>NOPPME=0</td><td>background work 不得超過 non-op limits</td><td>可能延後 controller work</td></tr><tr><td>NOPPME=1</td><td>background work 可暫時提高 power</td><td>上限仍受最後 operational state 限制</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>NOPPME</dt><dd>Non-Operational Power State Permissive Mode Enable，控制 controller background work 能否暫時超過 non-operational power limit。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.03">03.03.</span><span class="paragraph-text">閒置 2000 ms 後進 PS3：ITPT=2000=07D0h，放入 bits31:8 得 0007D000h；ITPS=3，放入 bits7:3 得 18h。相加得到低 Dword=0007D018h，其餘保留位與高 Dword 為 0。32 個 8-byte 項目合計 256 bytes。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Dword</dt><dd>Dword（Double word）；32 bits，也就是 4 bytes。對比 word=16 bits；例如 zero-based dword count=3 代表 4 個 Dwords，也就是 16 bytes。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-temperature-event-loop"><h2 id="heading-temperature-event-loop"><span class="section-number">04</span> 溫度門檻、感測器與通知</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">FID 04h 不只是一個溫度數字。TMPSEL 決定讀哪個 sensor，THSEL 決定 over 或 under，TMPTH 決定觸發點，TMPTHH 決定離開 event 的 clear point；SMART/Health.TTC 與 AEC enable 則把 controller 狀態送回 host。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>TMPSEL</dt><dd>Temperature Sensor Select，選擇 Composite Temperature 或 sensor 1 到 8 的欄位。</dd></div><div><dt>TMPTHH</dt><dd>Temperature Threshold Hysteresis，結束 threshold event 時使用的 Kelvin hysteresis。</dd></div><div><dt>THSEL</dt><dd>Threshold Type Select，選擇 over-temperature 或 under-temperature threshold。</dd></div><div><dt>TMPTH</dt><dd>Temperature Threshold，16-bit Kelvin threshold value。</dd></div><div><dt>TTC</dt><dd>Temperature Threshold Critical Warning，SMART／Health Critical Warning 中的溫度 threshold bit。</dd></div></dl>
<!-- claim:BASEPOWER-FID04 -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">FID 04h 可為 Composite Temperature 與最多八個實作的 temperature sensors 設 over／under threshold。溫度以 Kelvin 編碼；到達 over threshold 或低於等於 under threshold 時，SMART/Health 的 Temperature Threshold critical warning 可能觸發 asynchronous event。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3, 文件頁 462-463, PDF 頁 488-489</p></details>
<div class="table-wrap"><table><caption>溫度門檻、感測器與通知</caption><thead><tr><th scope="col">門檻欄位</th><th scope="col">選擇或設定什麼</th><th scope="col">事件觸發與解除如何判斷</th></tr></thead><tbody><tr><td>TMPSEL</td><td>Composite 或 sensor 1-8</td><td>Get 不使用 all-sensors selector</td></tr><tr><td>THSEL</td><td>over／under</td><td>比較方向相反</td></tr><tr><td>TMPTH</td><td>觸發 Kelvin</td><td>log raw K 及轉換後 °C</td></tr><tr><td>TMPTHH</td><td>clear hysteresis Kelvin</td><td>不是第二個觸發 threshold</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.03">04.03.</span><span class="paragraph-text">Composite over threshold=343 K（約 70 °C）、hysteresis=5 K：TMPSEL=0、THSEL=0、TMPTH=0157h、TMPTHH=5，所以 CDW11=(5&lt;&lt;22)+0157h=01400157h。event 於 ≥343 K 觸發，降到 338 K（約 65 °C）才結束。</span></p></aside>
</section>
<section class="lesson" id="module-hctm-control-loop"><h2 id="heading-hctm-control-loop"><span class="section-number">05</span> HCTM 的兩級熱管理</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span><span class="paragraph-text">HCTM 的目的不是指定固定 clock 或固定 power state，而是讓 host 提供 TMT1／TMT2 兩個 temperature boundaries。controller 在 TMT1 優先降低 performance impact，在 TMT2 則必須更積極控制 temperature；實際 hysteresis 與內部動作屬 vendor implementation。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>TMT1</dt><dd>Thermal Management Temperature 1，較輕度 thermal-management threshold，單位 Kelvin。</dd></div><div><dt>TMT2</dt><dd>Thermal Management Temperature 2，較強 thermal-management threshold，單位 Kelvin。</dd></div></dl>
<!-- claim:BASEPOWER-FID10 -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.02">05.02.</span><span class="paragraph-text">FID 10h 的 TMT1[31:16] 是較輕度 thermal management threshold，TMT2[15:0] 是較重度 threshold，單位都是 Kelvin；0h 分別停用對應 threshold。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.10</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, 文件頁 471-472, PDF 頁 497-498</p></details>
<div class="table-wrap"><table><caption>HCTM 的兩級熱管理</caption><thead><tr><th scope="col">熱管理欄位或統計</th><th scope="col">設定或觀察的內容</th><th scope="col">使用前需確認什麼</th></tr></thead><tbody><tr><td>TMT1</td><td>較輕度控制起點</td><td>目標是 minimize impact</td></tr><tr><td>TMT2</td><td>較強控制起點</td><td>溫控優先於 impact</td></tr><tr><td>MNTMT／MXTMT</td><td>合法設定範圍</td><td>先做 host-side validation</td></tr><tr><td>SMART counters</td><td>transition count／time</td><td>證明 control loop 真的動作</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>MNTMT</dt><dd>Minimum Thermal Management Temperature，HCTM 可設定的最低 Kelvin 值。</dd></div><div><dt>MXTMT</dt><dd>Maximum Thermal Management Temperature，HCTM 可設定的最高 Kelvin 值。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="05.03">05.03.</span><span class="paragraph-text">若 MNTMT=273 K、MXTMT=373 K，選 TMT1=343 K、TMT2=353 K 合法，CDW11=(0157h&lt;&lt;16)+0161h=01570161h。FID 10h 可 save；若 capability.SVBL=1 且 policy 要保存，CDW10.SV=1、FID=10h，所以 CDW10=80000010h。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>SV</dt><dd>Save，Set Features 要求 controller 同時保存所設定 value 的 bit。</dd></div></dl></aside>
</section>
<section id="spec-reading"><h2>接著打開 Spec 看什麼</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.01">06.01.</span><span class="paragraph-text">以下按概念列出閱讀位置。報告時先用上面的流程說明問題，再打開對應章節看欄位與完整條件。中文教學 HTML 另有本篇全部圖表的逐圖重點、案例與細節。</span></p>
<div class="table-wrap"><table><thead><tr><th scope="col">要說明的觀念</th><th scope="col">Spec 閱讀位置</th></tr></thead><tbody><tr><td>Feature 的能力、讀取與設定</td><td>Base 2.4 §5.2.12 · Base 2.4 §5.2.12.1 · Base 2.4 §5.2.30</td></tr><tr><td>Power State 的功率、延遲與效能</td><td>Base 2.4 §8.1.19 · Base 2.4 §8.1.19.1 · Base 2.4 §8.1.19.2 · Base 2.4 §5.2.30.1.2 · Base 2.4 §8.1.19.3</td></tr><tr><td>APST 的閒置條件與自動轉換</td><td>Base 2.4 §5.2.30.1.7 · Base 2.4 §8.1.19 · Base 2.4 §5.2.30</td></tr><tr><td>溫度門檻、感測器與通知</td><td>Base 2.4 §5.2.30.1.3 · Base 2.4 §5.2.30.1.3.1 · Base 2.4 §5.2.13.1.3</td></tr><tr><td>HCTM 的兩級熱管理</td><td>Base 2.4 §5.2.30.1.10 · Base 2.4 §5.2.30.1.10, 8.1.19.5 · Base 2.4 §5.2.13.1.3 · Base 2.4 §5.2.30.1.11 · Base 2.4 §8.1.19.4 · Base 2.4 §5.2.12.2</td></tr></tbody></table></div>
<a class="reading-link" href="/DOCS/nvme-spec-report/base-power-features/tutorial-zh-tw.html">開啟完整中文教學與逐圖解釋 →</a></section>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:base-power-features-feature-values -->
<details class="review-question" id="qa-base-power-features-feature-values"><summary>1. Supported、Current、Default、Saved 為何不能視為同一個 Feature 值？</summary>
<div data-qa-answer="base-power-features-feature-values"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.01">07.01.</span><span class="paragraph-text">Supported Capabilities 描述該 Feature 可如何使用；Current 是目前值，Default 是預設值，Saved 是已保存值且須符合支援條件。讀取時的選擇決定回覆意義。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, 文件頁 209-210, PDF 頁 235-236</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, 文件頁 210, PDF 頁 236</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12.1, 文件頁 211-212, PDF 頁 237-238</p>
</details></details>
<!-- qa:base-power-features-power-latency -->
<details class="review-question" id="qa-base-power-features-power-latency"><summary>2. 閒置功率最低的 Power State，為何未必適合頻繁進出 I/O 的負載？</summary>
<div data-qa-answer="base-power-features-power-latency"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.02">07.02.</span><span class="paragraph-text">每次進出狀態都可能付出 transition latency。短暫閒置省下的電力，需要連同進入與離開延遲、工作反應時間一起評估；不能只比較 power 數字。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19, 文件頁 666-668, PDF 頁 692-694</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19.1, 文件頁 668-669, PDF 頁 694-695</p>
</details></details>
<!-- qa:base-power-features-apst -->
<details class="review-question" id="qa-base-power-features-apst"><summary>3. APST entry 的 idle time 與 target state 各決定什麼？</summary>
<div data-qa-answer="base-power-features-apst"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.03">07.03.</span><span class="paragraph-text">Idle time 指定符合條件後等待多久才自動轉換；target 指定要轉往哪個 Power State。兩者要搭配目標狀態的能力與限制，才能形成可用的節能策略。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, 文件頁 468-469, PDF 頁 494-495</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, 文件頁 469, PDF 頁 495</p>
</details></details>
<!-- qa:base-power-features-thermal-controls -->
<details class="review-question" id="qa-base-power-features-thermal-controls"><summary>4. Temperature Threshold 和 HCTM 為何需要分開設定與解讀？</summary>
<div data-qa-answer="base-power-features-thermal-controls"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.04">07.04.</span><span class="paragraph-text">Temperature Threshold 用於溫度條件與通知；HCTM 提供 host 控制的熱管理行為。得知溫度越界與要求 controller 採取熱管理不是同一動作。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3, 文件頁 462-463, PDF 頁 488-489</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, 8.1.19.5, 文件頁 472, 670-671, PDF 頁 498, 696-697</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
