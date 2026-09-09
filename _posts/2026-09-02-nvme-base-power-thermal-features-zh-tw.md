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
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.03">00.03.</span><span class="paragraph-text">電源管理在功耗、恢復服務所需時間與溫度之間安排操作。先理解電源狀態有哪些能力，再看主機如何讀寫 Feature；APST 依閒置時間轉換狀態，溫度門檻與 HCTM 則依溫度處理不同問題。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>APST</dt><dd>Autonomous Power State Transition；依設定的閒置條件自動轉換電源狀態。</dd></div><div><dt>HCTM</dt><dd>Host Controlled Thermal Management；由 host 設定溫度門檻的熱管理機制。</dd></div></dl>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.04">00.04.</span><span class="paragraph-text">通知門檻用來回報溫度事件，熱管理門檻用來控制行為，兩者不能互換。學完應能解釋選擇較省電狀態可能帶來哪些延遲，以及設定值、目前狀態和累計統計分別告訴我們什麼。</span></p>
</div>
</section>
<section class="lesson" id="module-feature-read-set-loop"><h2 id="heading-feature-read-set-loop"><span class="section-number">01</span> Feature 的能力、讀取與設定</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">Feature 不是一個單純 register。Host 要先用 SEL=011b 讀 capability，再分別讀 current／default／saved view，確認 scope 與 persistence 後才寫入。Set completion 只證明 command outcome；重新 Get 與 runtime telemetry 才能證明軟體看見的新 policy。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div><div><dt>SEL</dt><dd>Select，Get Features 用來選 current、default、saved 或 supported-capabilities view 的欄位。</dd></div></dl>
<details class="technical-note"><summary>完整規則：Feature 的能力、讀取與設定</summary>
<!-- claim:BASEPOWER-READ-FIRST -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">Get Features 是讀取 Feature 屬性的 Admin command。工程流程不應從寫入猜測開始，而要先辨認 FID、查 capability，再取得 current／default／保存值。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div><div><dt>FID</dt><dd>Feature Identifier；指定要讀取或設定哪一項 Feature 的編號。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, 文件頁 209, PDF 頁 235</p></details>
<!-- claim:BASEPOWER-GET-SELECT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">CDW10.SEL 選擇 current=000b、default=001b、saved=010b 或 supported capabilities=011b；CDW10.FID 選 Feature。其餘 SEL encoding reserved。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div><div><dt>FID</dt><dd>Feature Identifier；指定要讀取或設定哪一項 Feature 的編號。</dd></div><div><dt>SEL</dt><dd>Select，Get Features 用來選 current、default、saved 或 supported-capabilities view 的欄位。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, 文件頁 209-210, PDF 頁 235-236</p></details>
<!-- claim:BASEPOWER-GET-CAP -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.04">01.04.</span><span class="paragraph-text">SEL=011b 時，CQE.DW0 以 CHANG、NSSPEC、SVBL 回報是否可變更、是否 namespace-specific、是否可 save。這三個 capability bits 與 Feature value 是兩種不同資料，不能混解。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div><div><dt>NSSPEC</dt><dd>Namespace Specific，指出 Feature 是否具有 per-namespace scope 的 capability bit。</dd></div><div><dt>CHANG</dt><dd>Changeable，指出 Feature value 是否可由 Set Features 變更的 capability bit。</dd></div><div><dt>SVBL</dt><dd>Saveable，supported-capabilities result 中指出 Feature 是否可保存的 bit。</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.12.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12.1, 文件頁 211-212, PDF 頁 237-238</p></details>
<!-- claim:BASEPOWER-SET-SAVE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.05">01.05.</span><span class="paragraph-text">CDW10.SV=1 要求把值保存為跨 reset／power cycle 可用的 保存值；若 Feature 不可 save，controller 會回 Feature Identifier Not Saveable。先讀 SVBL，再決定是否設 SV。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div><div><dt>SVBL</dt><dd>Saveable，supported-capabilities result 中指出 Feature 是否可保存的 bit。</dd></div><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div><div><dt>SV</dt><dd>Save，Set Features 要求 controller 同時保存所設定 value 的 bit。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, 文件頁 457, PDF 頁 483</p></details>
<!-- claim:BASEPOWER-SET-AFTER -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.06">01.06.</span><span class="paragraph-text">Set Features 成功後，後續 commands 必須（shall）使用新設定。若軟體需要讓一批 commands 一致套用舊值或新值，host 宜（should）先讓既有 in-flight commands 完成，再切換。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, 文件頁 459, PDF 頁 485</p></details>
</details>
<div class="table-wrap"><table><caption>Feature 的能力、讀取與設定</caption><thead><tr><th scope="col">Get Features 選擇值</th><th scope="col">要求讀取什麼</th><th scope="col">可用來做哪種判斷</th></tr></thead><tbody><tr><td>SEL=000b</td><td>目前值</td><td>確認控制器目前採用的設定</td></tr><tr><td>SEL=001b</td><td>預設值</td><td>了解預設設定</td></tr><tr><td>SEL=010b</td><td>保存值</td><td>不等於一定曾經 save</td></tr><tr><td>SEL=011b</td><td>CHANG／NSSPEC／SVBL</td><td>寫入前的 功能支援條件</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>NSSPEC</dt><dd>Namespace Specific，指出 Feature 是否具有 per-namespace scope 的 capability bit。</dd></div><div><dt>CHANG</dt><dd>Changeable，指出 Feature value 是否可由 Set Features 變更的 capability bit。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.07">01.07.</span><span class="paragraph-text">讀 FID 02h current 時 CDW10=00000002h；讀 supported capabilities 時 SEL=3，所以 CDW10=(3×100h)+02h=00000302h。若 CHANG=0，流程在 Set 前停止；若 CHANG=1，再依 NPSS 與 PSD 組合 CDW11。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NPSS</dt><dd>Number of Power States Support，以 0's-based 方式回報最高支援 power-state number。</dd></div><div><dt>PSD</dt><dd>Power State Descriptor，描述一個 power state 的 power、latency、operational 屬性與 relative performance。</dd></div></dl></aside>
<a class="reading-link" href="#reading-feature-read-set-loop">閱讀相關規格圖表 → Feature 的能力、讀取與設定</a>
</section>
<section class="lesson" id="module-power-state-mental-model"><h2 id="heading-power-state-mental-model"><span class="section-number">02</span> Power State 的功率、延遲與效能</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">只看 state number 無法判斷是否適合 workload。每一個 PSD 要一起讀 MP、NOPS、ENLAT／EXLAT、IDLP／ACTP 與 relative performance。PS 數字增加通常降低 maximum power，但不代表所有 latency 或 throughput 一定以固定比例變差。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>ENLAT</dt><dd>Entry Latency，進入該 power state 的 maximum latency，單位為 microseconds。</dd></div><div><dt>EXLAT</dt><dd>Exit Latency，離開該 power state 的 maximum latency，單位為 microseconds。</dd></div><div><dt>ACTP</dt><dd>Active Power，在指定 workload 與時間窗下描述的 average active power。</dd></div><div><dt>IDLP</dt><dd>Idle Power，依規格 idle 測量條件描述的 typical power。</dd></div><div><dt>NOPS</dt><dd>Non-Operational State，Power State Descriptor 中指出該 state 不處理 I/O commands 的 bit。</dd></div><div><dt>PSD</dt><dd>Power State Descriptor，描述一個 power state 的 power、latency、operational 屬性與 relative performance。</dd></div><div><dt>MP</dt><dd>Maximum Power，一個 power state 的 sustained maximum power。</dd></div><div><dt>PS</dt><dd>Power State，controller 的功耗／效能 operating point；PS0 是最高 maximum-power state。</dd></div></dl>
<details class="technical-note"><summary>完整規則：Power State 的功率、延遲與效能</summary>
<!-- claim:BASEPOWER-POWER-STATES -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">controller 必須（shall）至少支援一個 power state，最多可（may）支援 32 個，編號從 0 連續排列。PS0 的 maximum power 最高；後續 state 的 maximum power 不得高於前一個 state。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.19</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19, 文件頁 666-667, PDF 頁 692-693</p></details>
<!-- claim:BASEPOWER-POWER-METRICS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">Power State Descriptor（PSD）把 maximum power、operational/non-operational、entry/exit latency、idle/active power 與 relative performance 放在同一份描述。MP 是 sustained maximum；IDLP 與 ACTP 是不同測量情境，不能拿單次瞬間功耗互相比。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>ACTP</dt><dd>Active Power，在指定 workload 與時間窗下描述的 average active power。</dd></div><div><dt>IDLP</dt><dd>Idle Power，依規格 idle 測量條件描述的 typical power。</dd></div><div><dt>MP</dt><dd>Maximum Power，一個 power state 的 sustained maximum power。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.19</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19, 文件頁 666-668, PDF 頁 692-694</p></details>
<!-- claim:BASEPOWER-TRANSITION -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.04">02.04.</span><span class="paragraph-text">從舊 state 直接切到新 state 的最大 transition time，是舊 state 的 EXLAT 加上新 state 的 ENLAT。若 controller 內部經過多個 state，則每一段 transition time 相加。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>ENLAT</dt><dd>Entry Latency，進入該 power state 的 maximum latency，單位為 microseconds。</dd></div><div><dt>EXLAT</dt><dd>Exit Latency，離開該 power state 的 maximum latency，單位為 microseconds。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.19.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19.1, 文件頁 668-669, PDF 頁 694-695</p></details>
<!-- claim:BASEPOWER-RELATIVE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.05">02.05.</span><span class="paragraph-text">Relative Read／Write Throughput 與 Latency 都是『值越小越好』，但只可在相同 characteristic 內比較；throughput code 不能與 latency code 混成一個總分。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.19.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19.2, 文件頁 668, PDF 頁 694</p></details>
<!-- claim:BASEPOWER-NONOP -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.06">02.06.</span><span class="paragraph-text">non-operational power state 不處理 I/O commands，但仍可能處理 property、PMR、CMB、Admin／background 或 transport-specific access。『non-operational』不是 controller 關機。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div><div><dt>CMB</dt><dd>Controller Memory Buffer，controller 提供、可放置部分 queue 或資料結構的記憶體區域。</dd></div><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div><div><dt>PMR</dt><dd>Persistent Memory Region，由 controller 暴露、具有持久性語意的記憶體區域。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.19</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19, 文件頁 667-668, PDF 頁 693-694</p></details>
<!-- claim:BASEPOWER-FID02 -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.07">02.07.</span><span class="paragraph-text">FID 02h 用 CDW11.PS[4:0] 選 power state、WH[7:5] 提供 workload hint。指定的 PS 必須（shall）在 Identify Controller.NPSS 宣告範圍內；不支援的 PS 應（should）以 Invalid Field in Command 中止。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NPSS</dt><dd>Number of Power States Support，以 0's-based 方式回報最高支援 power-state number。</dd></div><div><dt>PS</dt><dd>Power State，controller 的功耗／效能 operating point；PS0 是最高 maximum-power state。</dd></div><div><dt>WH</dt><dd>Workload Hint，host 提供給 controller 的 workload category 提示，不是效能保證。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.2, 文件頁 460-461, PDF 頁 486-487</p></details>
<!-- claim:BASEPOWER-WORKLOAD -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.08">02.08.</span><span class="paragraph-text">WH=000b 表示未知 workload；001b 對應先 idle、再做 32 筆 random 1 MiB writes、再 idle 的情境；010b 對應 80,000 筆 sequential 128 KiB writes。011b～111b reserved。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>WH</dt><dd>Workload Hint，host 提供給 controller 的 workload category 提示，不是效能保證。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.19.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19.3, 文件頁 669, PDF 頁 695</p></details>
</details>
<div class="table-wrap"><table><caption>Power State 的功率、延遲與效能</caption><thead><tr><th scope="col">電源狀態屬性</th><th scope="col">描述的功耗或效能</th><th scope="col">比較時需要的條件</th></tr></thead><tbody><tr><td>MP</td><td>持續最大功率</td><td>不是瞬間 sample</td></tr><tr><td>IDLP／ACTP</td><td>閒置典型功率／工作中平均功率</td><td>測量條件不同</td></tr><tr><td>ENLAT／EXLAT</td><td>進入／離開 maximum latency</td><td>跨 state 必須相加</td></tr><tr><td>RRT/RRL/RWT/RWL</td><td>相對吞吐量／相對延遲</td><td>只在同類 characteristic 比較</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.09">02.09.</span><span class="paragraph-text">說明性計算：目前 PS1.EXLAT=100 µs，目標 PS3.ENLAT=2500 µs，直接 transition budget=2600 µs。若 controller 路徑是 PS1→PS2→PS3，還要加入 PS1.EXLAT+PS2.ENLAT 與 PS2.EXLAT+PS3.ENLAT 的每一段，不可仍用 2600 µs。</span></p></aside>
<a class="reading-link" href="#reading-power-state-mental-model">閱讀相關規格圖表 → Power State 的功率、延遲與效能</a>
</section>
<section class="lesson" id="module-apst-state-machine"><h2 id="heading-apst-state-machine"><span class="section-number">03</span> APST 的閒置條件與自動轉換</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">APST 的 256-byte buffer 不是 performance table，而是 32 個『idle 多久後進哪個 non-operational state』的 rules。APSTE 決定 timer rules 是否生效；每個 ITPT=0 entry 不參與；I/O 到達又會讓 controller 回到最近 operational state。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>APSTE</dt><dd>Autonomous Power State Transition Enable，啟用 APST table timer 判斷的 bit。</dd></div><div><dt>ITPT</dt><dd>Idle Time Prior to Transition，APST entry 的 idle threshold，單位為 milliseconds。</dd></div></dl>
<figure><figcaption><strong>閒置時間如何影響功耗狀態</strong></figcaption><ol class="flow-steps"><li>Host 設定 APST entries 的閒置時間 ITPT 與目標狀態 ITPS。</li><li>啟用 APST 後，controller 依閒置計時判斷轉移。</li><li>到達適用門檻後，進入指定 non-operational power state。</li><li>恢復處理 I/O 前，需要計入離開該狀態的延遲。</li></ol><figcaption>APST 以閒置時間換取節能，同時引入狀態轉移延遲。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>ITPS</dt><dd>Idle Transition Power State，APST entry 選擇的目標 non-operational power state。</dd></div><div><dt>ITPT</dt><dd>Idle Time Prior to Transition，APST entry 的 idle threshold，單位為 milliseconds。</dd></div></dl>
<details class="technical-note"><summary>完整規則：APST 的閒置條件與自動轉換</summary>
<!-- claim:BASEPOWER-FID0C -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span><span class="paragraph-text">FID 0Ch 的 APSTE=1 啟用 Autonomous Power State Transition（APST）；預設值是 0。啟用只表示 controller 可依 APST table 的 idle timer 自主切換，並不保證一定進入任何特定 state。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>APSTE</dt><dd>Autonomous Power State Transition Enable，啟用 APST table timer 判斷的 bit。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, 文件頁 468-469, PDF 頁 494-495</p></details>
<!-- claim:BASEPOWER-APST-ENTRY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.03">03.03.</span><span class="paragraph-text">APST data structure 固定 256 bytes，共 32 個 8-byte entries。每格 ITPT[31:8] 是毫秒 idle threshold，ITPS[7:3] 是目標 non-operational state；ITPT=0 會停用該 entry。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>ITPS</dt><dd>Idle Transition Power State，APST entry 選擇的目標 non-operational power state。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, 文件頁 469, PDF 頁 495</p></details>
<!-- claim:BASEPOWER-APST-NOPPME -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.04">03.04.</span><span class="paragraph-text">APSTE 控制 timer-based entry，NOPPME 控制 controller-initiated background operation 是否可暫時超過 non-operational limit。兩者是兩個正交開關：不要把『可自主進 state』誤解成『可為背景工作提高 power』。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NOPPME</dt><dd>Non-Operational Power State Permissive Mode Enable，控制 controller background work 能否暫時超過 non-operational power limit。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, 文件頁 469, PDF 頁 495</p></details>
<!-- claim:BASEPOWER-NONOP-IO -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.05">03.05.</span><span class="paragraph-text">host 在手動切入 non-operational state 前宜（should）先 drain I/O。若 I/O command 到達，controller 會自主回到最近使用的 operational state，再處理 I/O。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.19</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19, 文件頁 668, PDF 頁 694</p></details>
<!-- claim:BASEPOWER-SET-DPTR -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.06">03.06.</span><span class="paragraph-text">Set Features 的 DPTR 只在所選 Feature 定義 data structure 時使用。以 PRP 指向 buffer 時，該 data buffer 不得跨越超過一個 memory page boundary，因 PRP2 不能在此指向 PRP List。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>DPTR</dt><dd>Data Pointer，SQE 中指出 command data buffer 的欄位。</dd></div><div><dt>PRP</dt><dd>Physical Region Page，以 memory page 為單位描述 host-addressable data buffer 的 pointer 格式。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, 文件頁 456-457, PDF 頁 482-483</p></details>
</details>
<div class="table-wrap"><table><caption>APST 的閒置條件與自動轉換</caption><thead><tr><th scope="col">APST 或背景工作設定</th><th scope="col">控制器如何進入或使用狀態</th><th scope="col">受哪些條件限制</th></tr></thead><tbody><tr><td>APSTE=0</td><td>只允許 host-directed entry</td><td>table 可存在但 timer 不驅動</td></tr><tr><td>APSTE=1</td><td>host 或 timer entry</td><td>ITPT 必須連續滿足</td></tr><tr><td>NOPPME=0</td><td>background work 不得超過 non-op limits</td><td>可能延後 controller work</td></tr><tr><td>NOPPME=1</td><td>background work 可暫時提高 power</td><td>上限仍受最後 operational state 限制</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>NOPPME</dt><dd>Non-Operational Power State Permissive Mode Enable，控制 controller background work 能否暫時超過 non-operational power limit。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.07">03.07.</span><span class="paragraph-text">閒置 2000 ms 後進 PS3：ITPT=2000=07D0h，放入 bits31:8 得 07D00000h；ITPS=3，放入 bits7:3 得 18h。相加得到低 Dword=07D00018h，其餘保留位與高 Dword 為 0。32 個 8-byte 項目合計 256 bytes。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Dword</dt><dd>Dword（Double word）；32 bits，也就是 4 bytes。對比 word=16 bits；例如 zero-based dword count=3 代表 4 個 Dwords，也就是 16 bytes。</dd></div></dl></aside>
<a class="reading-link" href="#reading-apst-state-machine">閱讀相關規格圖表 → APST 的閒置條件與自動轉換</a>
</section>
<section class="lesson" id="module-temperature-event-loop"><h2 id="heading-temperature-event-loop"><span class="section-number">04</span> 溫度門檻、感測器與通知</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">FID 04h 不只是一個溫度數字。TMPSEL 決定讀哪個 sensor，THSEL 決定 over 或 under，TMPTH 決定觸發點，TMPTHH 決定離開 event 的 clear point；SMART/Health.TTC 與 AEC enable 則把 controller 狀態送回 host。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>TMPSEL</dt><dd>Temperature Sensor Select，選擇 Composite Temperature 或 sensor 1 到 8 的欄位。</dd></div><div><dt>TMPTHH</dt><dd>Temperature Threshold Hysteresis，結束 threshold event 時使用的 Kelvin hysteresis。</dd></div><div><dt>THSEL</dt><dd>Threshold Type Select，選擇 over-temperature 或 under-temperature threshold。</dd></div><div><dt>TMPTH</dt><dd>Temperature Threshold，16-bit Kelvin threshold value。</dd></div><div><dt>TTC</dt><dd>Temperature Threshold Critical Warning，SMART／Health Critical Warning 中的溫度 threshold bit。</dd></div></dl>
<details class="technical-note"><summary>完整規則：溫度門檻、感測器與通知</summary>
<!-- claim:BASEPOWER-FID04 -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">FID 04h 可為 Composite Temperature 與最多八個實作的 temperature sensors 設 over／under threshold。溫度以 Kelvin 編碼；到達 over threshold 或低於等於 under threshold 時，SMART/Health 的 Temperature Threshold critical warning 可能觸發 asynchronous event。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3, 文件頁 462-463, PDF 頁 488-489</p></details>
<!-- claim:BASEPOWER-HYST -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.03">04.03.</span><span class="paragraph-text">Figure 470 的 TMPSEL 選 sensor、THSEL 選 over/under、TMPTH 是 threshold、TMPTHH 是 hysteresis。over event 在溫度降到 threshold−hysteresis 時結束；under event在溫度升到 threshold+hysteresis 時結束。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>TMPSEL</dt><dd>Temperature Sensor Select，選擇 Composite Temperature 或 sensor 1 到 8 的欄位。</dd></div><div><dt>TMPTHH</dt><dd>Temperature Threshold Hysteresis，結束 threshold event 時使用的 Kelvin hysteresis。</dd></div><div><dt>THSEL</dt><dd>Threshold Type Select，選擇 over-temperature 或 under-temperature threshold。</dd></div><div><dt>TMPTH</dt><dd>Temperature Threshold，16-bit Kelvin threshold value。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3.1, 文件頁 463-464, PDF 頁 489-490</p></details>
<!-- claim:BASEPOWER-OBSERVE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.04">04.04.</span><span class="paragraph-text">設定完成不是驗證終點。SMART/Health 應同時觀察 Composite Temperature、TTC critical warning、warning temperature time、HCTM transition counters 與已實作 sensor readings，再對照 CQE 與 host latency。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>HCTM</dt><dd>Host Controlled Thermal Management；由 host 設定溫度門檻的熱管理機制。</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div><div><dt>TTC</dt><dd>Temperature Threshold Critical Warning，SMART／Health Critical Warning 中的溫度 threshold bit。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, 文件頁 220-225, PDF 頁 246-251</p></details>
</details>
<div class="table-wrap"><table><caption>溫度門檻、感測器與通知</caption><thead><tr><th scope="col">門檻欄位</th><th scope="col">選擇或設定什麼</th><th scope="col">事件觸發與解除如何判斷</th></tr></thead><tbody><tr><td>TMPSEL</td><td>Composite 或 sensor 1-8</td><td>Get 不使用 all-sensors selector</td></tr><tr><td>THSEL</td><td>over／under</td><td>比較方向相反</td></tr><tr><td>TMPTH</td><td>觸發 Kelvin</td><td>log raw K 及轉換後 °C</td></tr><tr><td>TMPTHH</td><td>clear hysteresis Kelvin</td><td>不是第二個觸發 threshold</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.05">04.05.</span><span class="paragraph-text">Composite over threshold=343 K（約 70 °C）、hysteresis=5 K：TMPSEL=0、THSEL=0、TMPTH=0157h、TMPTHH=5，所以 CDW11=(5&lt;&lt;22)+0157h=01400157h。event 於 ≥343 K 觸發，降到 338 K（約 65 °C）才結束。</span></p></aside>
<a class="reading-link" href="#reading-temperature-event-loop">閱讀相關規格圖表 → 溫度門檻、感測器與通知</a>
</section>
<section class="lesson" id="module-hctm-control-loop"><h2 id="heading-hctm-control-loop"><span class="section-number">05</span> HCTM 的兩級熱管理</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span><span class="paragraph-text">HCTM 的目的不是指定固定 clock 或固定 power state，而是讓 host 提供 TMT1／TMT2 兩個 temperature boundaries。controller 在 TMT1 優先降低 performance impact，在 TMT2 則必須更積極控制 temperature；實際 hysteresis 與內部動作屬 vendor implementation。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>TMT1</dt><dd>Thermal Management Temperature 1，較輕度 thermal-management threshold，單位 Kelvin。</dd></div><div><dt>TMT2</dt><dd>Thermal Management Temperature 2，較強 thermal-management threshold，單位 Kelvin。</dd></div></dl>
<details class="technical-note"><summary>完整規則：HCTM 的兩級熱管理</summary>
<!-- claim:BASEPOWER-FID10 -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.02">05.02.</span><span class="paragraph-text">FID 10h 的 TMT1[31:16] 是較輕度 thermal management threshold，TMT2[15:0] 是較重度 threshold，單位都是 Kelvin；0h 分別停用對應 threshold。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>TMT1</dt><dd>Thermal Management Temperature 1，較輕度 thermal-management threshold，單位 Kelvin。</dd></div><div><dt>TMT2</dt><dd>Thermal Management Temperature 2，較強 thermal-management threshold，單位 Kelvin。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.10</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, 文件頁 471-472, PDF 頁 497-498</p></details>
<!-- claim:BASEPOWER-HCTM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.03">05.03.</span><span class="paragraph-text">非零 TMT1 必須（shall）小於 TMT2，且兩者必須落在 MNTMT～MXTMT 內；否則回 Invalid Field in Command。達 TMT1 時 controller 採降低影響的動作，達 TMT2 時採更強動作；hysteresis 由 vendor 決定。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>MNTMT</dt><dd>Minimum Thermal Management Temperature，HCTM 可設定的最低 Kelvin 值。</dd></div><div><dt>MXTMT</dt><dd>Maximum Thermal Management Temperature，HCTM 可設定的最高 Kelvin 值。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.10, 8.1.19.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, 8.1.19.5, 文件頁 472, 670-671, PDF 頁 498, 696-697</p></details>
<!-- claim:BASEPOWER-FID11 -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.04">05.04.</span><span class="paragraph-text">FID 11h 的 NOPPME=1 允許 controller-initiated background operation 暫時把 power 提高到不超過最後一個 operational state 的上限；NOPPME=0 時，這類工作不得超過目前 non-operational state limits。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.11</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.11, 文件頁 472-473, PDF 頁 498-499</p></details>
<!-- claim:BASEPOWER-RTD3 -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.05">05.05.</span><span class="paragraph-text">RTD3E 與 RTD3R 分別描述進入與恢復時間，供 PCIe D3cold 使用情境評估 idle break-even；NVMe 文字明確說這不是 D3hot 的時間。PCIe D-state 的完整原始行為不在目前提供來源內，不能據此自行補寫。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>RTD3E</dt><dd>Runtime D3 Entry Latency，controller 進入 PCIe D3cold 使用情境的預期時間。</dd></div><div><dt>RTD3R</dt><dd>Runtime D3 Resume Latency，controller 從 PCIe D3cold 使用情境恢復的預期時間。</dd></div><div><dt>NVMe</dt><dd>Non-Volatile Memory Express，主機與非揮發性記憶體子系統之間的介面規範家族。</dd></div><div><dt>PCIe</dt><dd>PCI Express，NVMe memory-based controller 使用的 transport 與裝置互連。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.19.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19.4, 文件頁 669-670, PDF 頁 695-696</p></details>
<!-- claim:BASEPOWER-GET-STATUS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.06">05.06.</span><span class="paragraph-text">Get Features 指定不適用的 Controller Identifier 時，command-specific status 1Fh 表示 Invalid Controller Identifier；狀態碼需連同 SCT 解讀。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>SCT</dt><dd>Status Code Type；指定完成狀態碼所屬類別，需與 SC 一起解讀。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.12.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, 文件頁 212, PDF 頁 238</p></details>
</details>
<div class="table-wrap"><table><caption>HCTM 的兩級熱管理</caption><thead><tr><th scope="col">熱管理欄位或統計</th><th scope="col">設定或觀察的內容</th><th scope="col">使用前需確認什麼</th></tr></thead><tbody><tr><td>TMT1</td><td>較輕度控制起點</td><td>目標是 minimize impact</td></tr><tr><td>TMT2</td><td>較強控制起點</td><td>溫控優先於 impact</td></tr><tr><td>MNTMT／MXTMT</td><td>合法設定範圍</td><td>先做 host-side validation</td></tr><tr><td>SMART counters</td><td>transition count／time</td><td>證明 control loop 真的動作</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>MNTMT</dt><dd>Minimum Thermal Management Temperature，HCTM 可設定的最低 Kelvin 值。</dd></div><div><dt>MXTMT</dt><dd>Maximum Thermal Management Temperature，HCTM 可設定的最高 Kelvin 值。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="05.07">05.07.</span><span class="paragraph-text">若 MNTMT=273 K、MXTMT=373 K，選 TMT1=343 K、TMT2=353 K 合法，CDW11=(0157h&lt;&lt;16)+0161h=01570161h。FID 10h 可 save；若 capability.SVBL=1 且 policy 要保存，CDW10.SV=1、FID=10h，所以 CDW10=80000010h。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>SV</dt><dd>Save，Set Features 要求 controller 同時保存所設定 value 的 bit。</dd></div></dl></aside>
<a class="reading-link" href="#reading-hctm-control-loop">閱讀相關規格圖表 → HCTM 的兩級熱管理</a>
</section>
<details class="figure-reading-fold"><summary>展開圖表教學：依主軸閱讀來源圖表</summary>
<section id="figure-reading"><h2><span class="section-number">06</span> 讀懂本篇的規格圖表</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.01">06.01.</span><span class="paragraph-text">以下依概念整理規格中的圖表。每組先說明讀取順序與要判斷的問題，接著列出各圖的欄位或行為說明。可以由正文的連結跳到對應組別，也可以用這一節檢查自己能否把欄位連回完整操作。</span></p>
<div class="figure-reading-group" id="reading-feature-read-set-loop"><h3>圖表組 01 · Feature 的能力、讀取與設定</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.02">06.02.</span><span class="paragraph-text">Get Features 的 CDW10 同時含 FID 與 SEL。先以 FID 選功能，再用 SEL 選 current、default、saved 或 supported capabilities；不要把支援旗標的回傳格式當成一般設定值。</span></p>
<a class="reading-link" href="#module-feature-read-set-loop">回到本節的解釋與範例</a>
<!-- figure-table:BASEPOWER-FIG-197 -->
<details class="field-note" id="figure-BASEPOWER-FIG-197"><summary>Base Figure 197 · Get Features – Data Pointer</summary>
<!-- claim:BASEPOWER-FIG-197-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.03">06.03.</span><span class="paragraph-text">Figure 197〈Get Features – Data Pointer〉：Get／Set Features 共用命令外框，但 Get 的 SEL 選擇要讀哪種值，Set 的 SV 決定是否要求保存。CHANG、NSSPEC、SVBL 描述使用能力，資料指標和 UIDX 則按所選 Feature 的要求使用。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>UIDX</dt><dd>UUID Index，指向 UUID List 位置的 index；0 表示未指定 UUID。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 197, 文件頁 209, PDF 頁 235</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>DPTR</dt><dd>Data Pointer，SQE 中指出 command data buffer 的欄位。</dd></div></dl>
</details>
<!-- figure-table:BASEPOWER-FIG-198 -->
<details class="field-note" id="figure-BASEPOWER-FIG-198"><summary>Base Figure 198 · Get Features – Command Dword 10</summary>
<!-- claim:BASEPOWER-FIG-198-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.04">06.04.</span><span class="paragraph-text">Figure 198〈Get Features – Command Dword 10〉：Get／Set Features 共用命令外框，但 Get 的 SEL 選擇要讀哪種值，Set 的 SV 決定是否要求保存。CHANG、NSSPEC、SVBL 描述使用能力，資料指標和 UIDX 則按所選 Feature 的要求使用。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Dword</dt><dd>Dword（Double word）；32 bits，也就是 4 bytes。對比 word=16 bits；例如 zero-based dword count=3 代表 4 個 Dwords，也就是 16 bytes。</dd></div><div><dt>UIDX</dt><dd>UUID Index，指向 UUID List 位置的 index；0 表示未指定 UUID。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 198, 文件頁 209-210, PDF 頁 235-236</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-199 -->
<details class="field-note" id="figure-BASEPOWER-FIG-199"><summary>Base Figure 199 · Get Features – Command Dword 14</summary>
<!-- claim:BASEPOWER-FIG-199-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.05">06.05.</span><span class="paragraph-text">Figure 199〈Get Features – Command Dword 14〉：Get／Set Features 共用命令外框，但 Get 的 SEL 選擇要讀哪種值，Set 的 SV 決定是否要求保存。CHANG、NSSPEC、SVBL 描述使用能力，資料指標和 UIDX 則按所選 Feature 的要求使用。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 199, 文件頁 210, PDF 頁 236</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-200 -->
<details class="field-note" id="figure-BASEPOWER-FIG-200"><summary>Base Figure 200 · Feature Identifiers for Get Features</summary>
<!-- claim:BASEPOWER-FIG-200-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.06">06.06.</span><span class="paragraph-text">Figure 200〈Feature Identifiers for Get Features〉：Get／Set Features 共用命令外框，但 Get 的 SEL 選擇要讀哪種值，Set 的 SV 決定是否要求保存。CHANG、NSSPEC、SVBL 描述使用能力，資料指標和 UIDX 則按所選 Feature 的要求使用。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, Figure 200, 文件頁 210-211, PDF 頁 236-237</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-201 -->
<details class="field-note" id="figure-BASEPOWER-FIG-201"><summary>Base Figure 201 · Get Features – Select Supported Capabilities</summary>
<!-- claim:BASEPOWER-FIG-201-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.07">06.07.</span><span class="paragraph-text">Figure 201〈Get Features – Select Supported Capabilities〉：Get／Set Features 共用命令外框，但 Get 的 SEL 選擇要讀哪種值，Set 的 SV 決定是否要求保存。CHANG、NSSPEC、SVBL 描述使用能力，資料指標和 UIDX 則按所選 Feature 的要求使用。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.12.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, Figure 201, 文件頁 212, PDF 頁 238</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-202 -->
<details class="field-note" id="figure-BASEPOWER-FIG-202"><summary>Base Figure 202 · Get Features – Command Specific Status Values</summary>
<!-- claim:BASEPOWER-FIG-202-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.08">06.08.</span><span class="paragraph-text">Figure 202〈Get Features – Command Specific Status Values〉：Get／Set Features 共用命令外框，但 Get 的 SEL 選擇要讀哪種值，Set 的 SV 決定是否要求保存。CHANG、NSSPEC、SVBL 描述使用能力，資料指標和 UIDX 則按所選 Feature 的要求使用。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.12.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12.2, Figure 202, 文件頁 212, PDF 頁 238</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-463 -->
<details class="field-note" id="figure-BASEPOWER-FIG-463"><summary>Base Figure 463 · Set Features – Data Pointer</summary>
<!-- claim:BASEPOWER-FIG-463-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.09">06.09.</span><span class="paragraph-text">Figure 463〈Set Features – Data Pointer〉：Get／Set Features 共用命令外框，但 Get 的 SEL 選擇要讀哪種值，Set 的 SV 決定是否要求保存。CHANG、NSSPEC、SVBL 描述使用能力，資料指標和 UIDX 則按所選 Feature 的要求使用。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 463, 文件頁 456, PDF 頁 482</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-464 -->
<details class="field-note" id="figure-BASEPOWER-FIG-464"><summary>Base Figure 464 · Set Features – Command Dword 10</summary>
<!-- claim:BASEPOWER-FIG-464-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.10">06.10.</span><span class="paragraph-text">Figure 464〈Set Features – Command Dword 10〉：Get／Set Features 共用命令外框，但 Get 的 SEL 選擇要讀哪種值，Set 的 SV 決定是否要求保存。CHANG、NSSPEC、SVBL 描述使用能力，資料指標和 UIDX 則按所選 Feature 的要求使用。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 464, 文件頁 457, PDF 頁 483</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-465 -->
<details class="field-note" id="figure-BASEPOWER-FIG-465"><summary>Base Figure 465 · Set Features – Command Dword 14</summary>
<!-- claim:BASEPOWER-FIG-465-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.11">06.11.</span><span class="paragraph-text">Figure 465〈Set Features – Command Dword 14〉：Get／Set Features 共用命令外框，但 Get 的 SEL 選擇要讀哪種值，Set 的 SV 決定是否要求保存。CHANG、NSSPEC、SVBL 描述使用能力，資料指標和 UIDX 則按所選 Feature 的要求使用。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 465, 文件頁 457, PDF 頁 483</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-466 -->
<details class="field-note" id="figure-BASEPOWER-FIG-466"><summary>Base Figure 466 · Feature Identifiers for Set Features</summary>
<!-- claim:BASEPOWER-FIG-466-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.12">06.12.</span><span class="paragraph-text">Figure 466〈Feature Identifiers for Set Features〉：Get／Set Features 共用命令外框，但 Get 的 SEL 選擇要讀哪種值，Set 的 SV 決定是否要求保存。CHANG、NSSPEC、SVBL 描述使用能力，資料指標和 UIDX 則按所選 Feature 的要求使用。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, Figure 466, 文件頁 457-459, PDF 頁 483-485</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-093 -->
<details class="field-note" id="figure-BASEPOWER-FIG-093"><summary>Base Figure 93 · Common Command Format</summary>
<!-- claim:BASEPOWER-FIG-093-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.13">06.13.</span><span class="paragraph-text">Figure 93〈Common Command Format〉：共同 SQE 先以 CDW0 描述 opcode、命令識別與資料指標選擇，再以 NSID 選對象、MPTR／DPTR 指向資料。CDW10–15 的意義由個別命令決定，不能跨 opcode 沿用。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>MPTR</dt><dd>Metadata Pointer，SQE 中指出獨立 metadata buffer 的欄位。</dd></div><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div><div><dt>SQE</dt><dd>Submission Queue Entry，SQ 中的一筆命令資料結構。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, 文件頁 140-142, PDF 頁 166-168</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>MPTR</dt><dd>Metadata Pointer，SQE 中指出獨立 metadata buffer 的欄位。</dd></div><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div><div><dt>CID</dt><dd>Command Identifier，與 SQ identifier 合用以辨識 outstanding command。</dd></div></dl>
</details>
</div>
<div class="figure-reading-group" id="reading-power-state-mental-model"><h3>圖表組 02 · Power State 的功率、延遲與效能</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.14">06.14.</span><span class="paragraph-text">Power State Descriptor 先看 operational 性質，再分組讀功率、進出延遲與相對效能。功率尺度和測量條件要與數值一起看，不能把典型值和最大值放在同一欄直接排名。</span></p>
<a class="reading-link" href="#module-power-state-mental-model">回到本節的解釋與範例</a>
<!-- figure-table:BASEPOWER-FIG-468 -->
<details class="field-note" id="figure-BASEPOWER-FIG-468"><summary>Base Figure 468 · Power Management – Command Dword 11</summary>
<!-- claim:BASEPOWER-FIG-468-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.15">06.15.</span><span class="paragraph-text">Figure 468〈Power Management – Command Dword 11〉：PS 選擇電源狀態，WH 提供工作負載提示。PS 必須對應控制器支援的狀態，WH 則按允許的提示值解讀；提示不會替主機指定一個新的 Power State Descriptor。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.2, Figure 468, 文件頁 461, PDF 頁 487</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-738 -->
<details class="field-note" id="figure-BASEPOWER-FIG-738"><summary>Base Figure 738 · Power Management Overview</summary>
<!-- claim:BASEPOWER-FIG-738-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.16">06.16.</span><span class="paragraph-text">Figure 738〈Power Management Overview〉：Power State Descriptor 把功率、進出延遲和相對效能分開。轉移成本要從目前狀態的離開時間與目標的進入時間計算；Workload Hint 描述負載提示，不是直接指定保證的延遲。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.19</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19, Figure 738, 文件頁 666, PDF 頁 692</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-739 -->
<details class="field-note" id="figure-BASEPOWER-FIG-739"><summary>Base Figure 739 · Power State Characteristics</summary>
<!-- claim:BASEPOWER-FIG-739-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.17">06.17.</span><span class="paragraph-text">Figure 739〈Power State Characteristics〉：Power State Descriptor 把功率、進出延遲和相對效能分開。轉移成本要從目前狀態的離開時間與目標的進入時間計算；Workload Hint 描述負載提示，不是直接指定保證的延遲。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.19</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19, Figure 739, 文件頁 667, PDF 頁 693</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-740 -->
<details class="field-note" id="figure-BASEPOWER-FIG-740"><summary>Base Figure 740 · Workload Hints</summary>
<!-- claim:BASEPOWER-FIG-740-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.18">06.18.</span><span class="paragraph-text">Figure 740〈Workload Hints〉：Power State Descriptor 把功率、進出延遲和相對效能分開。轉移成本要從目前狀態的離開時間與目標的進入時間計算；Workload Hint 描述負載提示，不是直接指定保證的延遲。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.19.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19.3, Figure 740, 文件頁 669, PDF 頁 695</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-338 -->
<details class="field-note" id="figure-BASEPOWER-FIG-338"><summary>Base Figure 338 · Identify Controller Data Structure</summary>
<!-- claim:BASEPOWER-FIG-338-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.19">06.19.</span><span class="paragraph-text">Figure 338〈Identify Controller Data Structure〉：Identify Controller 的欄位分別描述能力、限制、身分與目前資訊。依本篇主題選出需要的欄位後，再連到相應命令；支援位和大小上限必須一起用，不能以單一旗標推論所有參數都有效。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.14.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, 文件頁 340-364, PDF 頁 366-390</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>WCTEMP</dt><dd>Warning Composite Temperature Threshold，Identify Controller 回報的 composite warning threshold。</dd></div><div><dt>RTD3E</dt><dd>Runtime D3 Entry Latency，controller 進入 PCIe D3cold 使用情境的預期時間。</dd></div><div><dt>RTD3R</dt><dd>Runtime D3 Resume Latency，controller 從 PCIe D3cold 使用情境恢復的預期時間。</dd></div></dl>
</details>
<!-- figure-table:BASEPOWER-FIG-340 -->
<details class="field-note" id="figure-BASEPOWER-FIG-340"><summary>Base Figure 340 · Power State Descriptor Data Structure</summary>
<!-- claim:BASEPOWER-FIG-340-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.20">06.20.</span><span class="paragraph-text">Figure 340〈Power State Descriptor Data Structure〉：Power State Descriptor 把功率、進出延遲和相對效能分開。轉移成本要從目前狀態的離開時間與目標的進入時間計算；Workload Hint 描述負載提示，不是直接指定保證的延遲。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.14.2.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.2, Figure 340, 文件頁 383-386, PDF 頁 409-412</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NOPS</dt><dd>Non-Operational State，Power State Descriptor 中指出該 state 不處理 I/O commands 的 bit。</dd></div></dl>
</details>
</div>
<div class="figure-reading-group" id="reading-apst-state-machine"><h3>圖表組 03 · APST 的閒置條件與自動轉換</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.21">06.21.</span><span class="paragraph-text">APST entry 圖先解讀 ITPT 與 ITPS，再連到被選 Power State Descriptor。以 2000 ms、PS3 為例，ITPT 放入 bits31:8，ITPS 放入 bits7:3；時間值移位與目標狀態編碼分開驗算。</span></p>
<a class="reading-link" href="#module-apst-state-machine">回到本節的解釋與範例</a>
<!-- figure-table:BASEPOWER-FIG-475 -->
<details class="field-note" id="figure-BASEPOWER-FIG-475"><summary>Base Figure 475 · Autonomous Power State Transition – Command Dword 11</summary>
<!-- claim:BASEPOWER-FIG-475-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.22">06.22.</span><span class="paragraph-text">Figure 475〈Autonomous Power State Transition – Command Dword 11〉：APSTE 啟用自動轉換，32 個 entry 共 256 bytes，每筆用 ITPT 指定閒置毫秒數、ITPS 指定目標狀態。NOPPME 另外控制 non-operational 狀態的背景工作規則；有 APST 表不表示它已啟用。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, Figure 475, 文件頁 468, PDF 頁 494</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-476 -->
<details class="field-note" id="figure-BASEPOWER-FIG-476"><summary>Base Figure 476 · Autonomous Power State Transition Data Structure</summary>
<!-- claim:BASEPOWER-FIG-476-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.23">06.23.</span><span class="paragraph-text">Figure 476〈Autonomous Power State Transition Data Structure〉：APSTE 啟用自動轉換，32 個 entry 共 256 bytes，每筆用 ITPT 指定閒置毫秒數、ITPS 指定目標狀態。NOPPME 另外控制 non-operational 狀態的背景工作規則；有 APST 表不表示它已啟用。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, Figure 476, 文件頁 469, PDF 頁 495</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-477 -->
<details class="field-note" id="figure-BASEPOWER-FIG-477"><summary>Base Figure 477 · Autonomous Power State Transition Entry</summary>
<!-- claim:BASEPOWER-FIG-477-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.24">06.24.</span><span class="paragraph-text">Figure 477〈Autonomous Power State Transition Entry〉：APSTE 啟用自動轉換，32 個 entry 共 256 bytes，每筆用 ITPT 指定閒置毫秒數、ITPS 指定目標狀態。NOPPME 另外控制 non-operational 狀態的背景工作規則；有 APST 表不表示它已啟用。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, Figure 477, 文件頁 469, PDF 頁 495</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-478 -->
<details class="field-note" id="figure-BASEPOWER-FIG-478"><summary>Base Figure 478 · APST and NOPPME Interaction</summary>
<!-- claim:BASEPOWER-FIG-478-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.25">06.25.</span><span class="paragraph-text">Figure 478〈APST and NOPPME Interaction〉：APSTE 啟用自動轉換，32 個 entry 共 256 bytes，每筆用 ITPT 指定閒置毫秒數、ITPS 指定目標狀態。NOPPME 另外控制 non-operational 狀態的背景工作規則；有 APST 表不表示它已啟用。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.7, Figure 478, 文件頁 469, PDF 頁 495</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-483 -->
<details class="field-note" id="figure-BASEPOWER-FIG-483"><summary>Base Figure 483 · Non-Operational Power State Configuration – Command Dword 11</summary>
<!-- claim:BASEPOWER-FIG-483-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.26">06.26.</span><span class="paragraph-text">Figure 483〈Non-Operational Power State Configuration – Command Dword 11〉：APSTE 啟用自動轉換，32 個 entry 共 256 bytes，每筆用 ITPT 指定閒置毫秒數、ITPS 指定目標狀態。NOPPME 另外控制 non-operational 狀態的背景工作規則；有 APST 表不表示它已啟用。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.11</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.11, Figure 483, 文件頁 472-473, PDF 頁 498-499</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-temperature-event-loop"><h3>圖表組 04 · 溫度門檻、感測器與通知</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.27">06.27.</span><span class="paragraph-text">先看 TMPSEL 與 THSEL，再配對 TMPTH、TMPTHH。在溫度軸上分別標出觸發和解除位置，用規格的比較符號確認邊界，並與 SMART 的感測器讀值對照。</span></p>
<a class="reading-link" href="#module-temperature-event-loop">回到本節的解釋與範例</a>
<!-- figure-table:BASEPOWER-FIG-470 -->
<details class="field-note" id="figure-BASEPOWER-FIG-470"><summary>Base Figure 470 · Temperature Threshold – Command Dword 11</summary>
<!-- claim:BASEPOWER-FIG-470-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.28">06.28.</span><span class="paragraph-text">Figure 470〈Temperature Threshold – Command Dword 11〉：TMPSEL 選感測器，THSEL 選高溫或低溫方向，TMPTH 設門檻，TMPTHH 設遲滯。先固定感測器和方向，再在溫度軸上標出觸發與解除條件，不能把遲滯當成另一個獨立觸發門檻。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.3.1, Figure 470, 文件頁 463-464, PDF 頁 489-490</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-213 -->
<details class="field-note" id="figure-BASEPOWER-FIG-213"><summary>Base Figure 213 · SMART / Health Information Log</summary>
<!-- claim:BASEPOWER-FIG-213-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.29">06.29.</span><span class="paragraph-text">Figure 213〈SMART / Health Information Log〉：溫度、熱管理轉換次數與累計時間回答不同問題。感測器溫度是讀取到的量測值，計數與時間是累積結果；先配對名稱與單位，不能把歷史次數當成目前正在執行的熱管理級別。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.3, Figure 213, 文件頁 220-225, PDF 頁 246-251</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-474 -->
<details class="field-note" id="figure-BASEPOWER-FIG-474"><summary>Base Figure 474 · Asynchronous Event Configuration – Command Dword 11</summary>
<!-- claim:BASEPOWER-FIG-474-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.30">06.30.</span><span class="paragraph-text">Figure 474〈Asynchronous Event Configuration – Command Dword 11〉：事件種類與事件啟用是兩份不同資訊。先以通知種類找到本篇使用的事件，再看相應啟用位；取得通知後仍需讀對應狀態或 log，通知本身不包含完整結果。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.6, Figure 474, 文件頁 466-468, PDF 頁 492-494</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-hctm-control-loop"><h3>圖表組 05 · HCTM 的兩級熱管理</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.31">06.31.</span><span class="paragraph-text">將 TMT1、TMT2 放在同一條溫度軸，再用 MNTMT、MXTMT 檢查允許範圍。SMART 中的次數和時間對應控制活動的累計紀錄，不與門檻設定值混讀。</span></p>
<a class="reading-link" href="#module-hctm-control-loop">回到本節的解釋與範例</a>
<!-- figure-table:BASEPOWER-FIG-482 -->
<details class="field-note" id="figure-BASEPOWER-FIG-482"><summary>Base Figure 482 · Host Controlled Thermal Management – Command Dword 11</summary>
<!-- claim:BASEPOWER-FIG-482-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.32">06.32.</span><span class="paragraph-text">Figure 482〈Host Controlled Thermal Management – Command Dword 11〉：TMT1 與 TMT2 是兩級熱管理門檻，須符合控制器允許範圍及彼此關係。圖中的控制活動與門檻設定分開閱讀；降溫後的解除條件也不等於將兩個門檻設成同一值。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.10</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.10, Figure 482, 文件頁 472, PDF 頁 498</p></details>

</details>
<!-- figure-table:BASEPOWER-FIG-741 -->
<details class="field-note" id="figure-BASEPOWER-FIG-741"><summary>Base Figure 741 · Host Controlled Thermal Management</summary>
<!-- claim:BASEPOWER-FIG-741-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.33">06.33.</span><span class="paragraph-text">Figure 741〈Host Controlled Thermal Management〉：TMT1 與 TMT2 是兩級熱管理門檻，須符合控制器允許範圍及彼此關係。圖中的控制活動與門檻設定分開閱讀；降溫後的解除條件也不等於將兩個門檻設成同一值。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.19.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.19.5, Figure 741, 文件頁 671, PDF 頁 697</p></details>

</details>
</div>
<!-- claim:BASEPOWER-GET-SAVED -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.34">06.34.</span><span class="paragraph-text">若要求 保存值，但 controller 不支援 保存值 或尚無 保存值，controller 會以 預設值 運作。這不是『讀取成功就代表曾經儲存』。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, 文件頁 210, PDF 頁 236</p></details>
<!-- claim:BASEPOWER-GET-UIDX -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.35">06.35.</span><span class="paragraph-text">CDW14.UIDX 只有在 controller 支援 UUID List 且該 Feature 需要 UUID 關聯時才有意義；未使用時保留為 0。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>UUID</dt><dd>Universally Unique Identifier，128-bit identifier；其實際關聯範圍仍由使用它的資料結構決定。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, 文件頁 210, PDF 頁 236</p></details>
<!-- claim:BASEPOWER-FID-SCOPE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.36">06.36.</span><span class="paragraph-text">本報告五個 FID 的 scope 都是 Controller。FID 02h、04h、0Ch、11h 不支援 save；FID 10h 支援 save。只有 FID 0Ch 需要 256-byte data structure。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, 文件頁 457-459, PDF 頁 483-485</p></details>
</section>
</details>
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
