---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4 第 3 章：Controller、Queue、初始化與重設"
date: 2026-08-28
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
[English]({% post_url 2026-08-28-nvme-base-ch3-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">控制器開始處理 I/O 之前，需要先建立可用的介面、佇列與狀態。本篇沿著控制器的運作生命週期，連起能力查詢、初始化、命令處理、記憶體資源，以及關機、重設與韌體啟用。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>啟動與能力</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">從識別控制器，到設定必要 properties 與確認可處理命令。</span></p></article>
<article><span class="axis-number">02</span><h3>佇列與命令處理</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">理解佇列位置、Doorbell 更新與仲裁分工。</span></p></article>
<article><span class="axis-number">03</span><h3>資源與生命週期</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">區分容量、控制器記憶體與各種狀態改變的影響範圍。</span></p></article>
</div>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">提交佇列保存主機送出的命令，完成佇列保存控制器回報的結果。主機要先建立這些共同機制，再使用讀寫等命令；以下從這個先後關係展開。</span></p>
<div class="overview-connections"><h3>把主軸連起來</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.03">00.03.</span><span class="paragraph-text">控制器從被發現到可接受命令，會經過能力辨識、記憶體及佇列配置、啟用與就緒確認。開始運作後，還要安排不同佇列的工作，管理 namespace 與控制器記憶體，最後處理關機或重設。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div></dl>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.04">00.04.</span><span class="paragraph-text">這條生命週期把各組 properties 連在一起：有些回報能力，有些接受主機設定，有些回報當前狀態。學完應能說明每個階段由誰採取動作、依什麼資訊前進，以及停止或重設後哪些資源需要重新確認。</span></p>
</div>
</section>
<section class="lesson" id="module-identity"><h2 id="heading-identity"><span class="section-number">01</span> Controller 類型、識別碼與能力</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">Controller type 回答『能做哪類工作』，Controller ID 回答『這是哪一個 controller』，support-requirement Figure 回答『在這個上下文中 command／log／feature 的支援強度』。Figures 23-32 應連續閱讀，但三種問題不能合併成一個布林值。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div></dl>
<!-- claim:BASE3-STATIC -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">memory-based controller 必須（shall）只支援 static controller model。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.1, 文件頁 38, PDF 頁 64</p></details>
<div class="table-wrap"><table><caption>Controller 類型、識別碼與能力</caption><thead><tr><th scope="col">控制器類型或標示</th><th scope="col">可以處理的工作</th><th scope="col">支援能力如何確認</th></tr></thead><tbody><tr><td>I/O controller</td><td>可執行使用者資料 I/O</td><td>仍需逐項查 optional capability</td></tr><tr><td>Administrative controller</td><td>管理用途、無資料 I/O command</td><td>不能因有 Admin Queue 就當成 I/O controller</td></tr><tr><td>支援標示</td><td>針對 row 與上下文描述強度</td><td>不能脫離 column／footnote 解讀</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>Administrative controller</dt><dd>Administrative controller，以管理為目的且不執行使用者資料 I/O command 的 controller 類型。</dd></div><div><dt>I/O controller</dt><dd>I/O controller，可執行使用者資料 I/O command 的 controller 類型。</dd></div><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">說明性範例：偵測到一個 Administrative controller 時，軟體仍會建立 Admin SQ/CQ 並執行管理 command，但不應把 namespace data path 掛到它。若只用『存在 Admin Queue』判斷 controller type，I/O 與 Administrative controller 會被錯誤歸成同類。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CQ</dt><dd>Completion Queue，controller 放入完成結果的完成佇列。</dd></div><div><dt>SQ</dt><dd>Submission Queue，主機放入命令的提交佇列。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-properties-init"><h2 id="heading-properties-init"><span class="section-number">02</span> 從設定到 CSTS.RDY：初始化流程</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">Properties 不是彼此獨立的 register 清單。CAP 先限制 page size、queue 與 timeout 能力；AQA、ASQ、ACQ 建立 Admin queues；CC 選擇設定並以 EN 啟動；最後由 CSTS.RDY 宣告 controller 已能正常處理命令。Figures 33-46 與 Figure 57 應沿這條因果鏈閱讀。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CSTS</dt><dd>Controller Status，controller 回報 ready、fatal status 與 shutdown 狀態的 property。</dd></div><div><dt>ACQ</dt><dd>Admin Completion Queue Base Address，Admin CQ 在可定址記憶體中的基底位址。</dd></div><div><dt>AQA</dt><dd>Admin Queue Attributes，描述 Admin SQ 與 Admin CQ 大小的 property。</dd></div><div><dt>ASQ</dt><dd>Admin Submission Queue Base Address，Admin SQ 在可定址記憶體中的基底位址。</dd></div><div><dt>CAP</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。</dd></div><div><dt>RDY</dt><dd>Ready，CSTS 中表示 controller 是否已準備正常處理 command 的 bit。</dd></div><div><dt>CC</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。</dd></div><div><dt>EN</dt><dd>Enable，CC 中控制 controller enable state 的 bit。</dd></div></dl>
<!-- claim:BASE3-PROPERTY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">host 必須（shall）以 property 指定的寬度，從 property 起始 offset 存取；memory-based controller 的實際存取規則由 PCIe Transport 補充。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>offset</dt><dd>offset；從指定起點算出的位移。它回答「離起點多遠」，不等於 index。</dd></div><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div><div><dt>PCIe</dt><dd>PCI Express，NVMe memory-based controller 使用的 transport 與裝置互連。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, 文件頁 52-54, PDF 頁 78-80</p></details>
<div class="table-wrap"><table><caption>從設定到 CSTS.RDY：初始化流程</caption><thead><tr><th scope="col">Property 或設定</th><th scope="col">主機與控制器各自提供什麼</th><th scope="col">初始化時的先後關係</th></tr></thead><tbody><tr><td>CAP</td><td>能力與界限</td><td>在寫設定前讀</td></tr><tr><td>AQA/ASQ/ACQ</td><td>Admin queue 大小與位址</td><td>需符合 page/alignment 能力</td></tr><tr><td>CC</td><td>host 選擇與 enable</td><td>寫入值要與 CAP 相容</td></tr><tr><td>CSTS</td><td>controller 回報狀態</td><td>RDY/CFS/SHST 不可互相替代</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>SHST</dt><dd>Shutdown Status，CSTS 中由 controller 回報 shutdown 進度的欄位。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">說明性範例：host 選擇 4 KiB MPS，ASQ 與 ACQ base address 因而必須依該 page size 對齊。寫 CC.EN=1 後，host 以 CAP／CRTO 指定的時間界限等待 CSTS.RDY=1；若 CFS 先出現，流程應進入 error recovery，而不是繼續建立 I/O queues。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CRTO</dt><dd>Controller Ready Timeouts，回報特定 ready mode 所需等待時間的 property。</dd></div><div><dt>MPS</dt><dd>Memory Page Size，controller 使用的 memory page 大小設定；影響 queue address 與 PRP 對齊。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-queue-arbitration"><h2 id="heading-queue-arbitration"><span class="section-number">03</span> Queue 位置與命令選取</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">Figure 73/74 說明 queue 的 empty/full 判定，Figure 80/81 說明多個 SQ 競爭 controller 服務時的 arbitration。前者處理單一 ring 的 head/tail 狀態，後者處理多個 candidate SQ 的選擇；priority 屬於 SQ，不是每筆 command 自帶的獨立優先權。</span></p>
<!-- claim:BASE3-QUEUE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span><span class="paragraph-text">PCIe queue 由 host-addressable memory 中的環形 buffer、head 與 tail pointer 構成。host 建立 I/O Completion Queue 後再建立對應 Submission Queue，並以 doorbell 推進 pointer。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1, 文件頁 88-91, PDF 頁 114-117</p></details>
<div class="table-wrap"><table><caption>Queue 位置與命令選取</caption><thead><tr><th scope="col">佇列狀態或選取方式</th><th scope="col">它決定什麼</th><th scope="col">不能由此推論什麼</th></tr></thead><tbody><tr><td>empty</td><td>head == tail 且 phase／ownership 符合 empty 定義</td><td>沒有可取走 entry</td></tr><tr><td>full</td><td>下一個 tail 會追上尚未釋放 head</td><td>host 不得覆寫 entry</td></tr><tr><td>Round Robin</td><td>候選 SQ 輪流取得服務</td><td>不代表 command completion 依提交順序</td></tr><tr><td>Weighted RR + Urgent</td><td>priority class 與 weight 影響選擇</td><td>仍需依適用設定解讀</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.03">03.03.</span><span class="paragraph-text">說明性範例：深度 4 的 SQ 只有四個 slot，但 full/empty 判定還需要 ownership 規則；不能只用 tail-head 的無號差值。若 SQ 1 與 SQ 2 同時有 command，arbiter 先選 SQ 2 也不代表 SQ 2 的 command 一定先完成，因 command 執行時間仍可能不同。</span></p></aside>
</section>
<section class="lesson" id="module-memory-capacity"><h2 id="heading-memory-capacity"><span class="section-number">04</span> Namespace、CMB、PMR 與容量</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">CMB/PMR properties 描述 controller 暴露的 memory region 位置、能力與狀態；capacity Figures 86-89 描述 NVM subsystem 各層級可用或已配置容量。兩者都談 memory，卻不是同一種空間，也不能用同一個『剩餘容量』欄位合併。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NVM subsystem</dt><dd>NVM subsystem，包含 controller、port、namespace 與非揮發性儲存資源的 NVMe 系統邊界。</dd></div><div><dt>CMB</dt><dd>Controller Memory Buffer，controller 提供、可放置部分 queue 或資料結構的記憶體區域。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div><div><dt>PMR</dt><dd>Persistent Memory Region，由 controller 暴露、具有持久性語意的記憶體區域。</dd></div></dl>
<!-- claim:BASE3-CAPACITY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">capacity model 分開追蹤 NVM subsystem、Endurance Group、NVM Set 與 namespace 的可用或配置容量；同一數值不可跨層級直接比較。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Endurance Group</dt><dd>Endurance Group，用於隔離與回報耐久度相關狀態的 NVM 資源群組。</dd></div><div><dt>NVM Set</dt><dd>NVM Set，把 namespace 與一組共同管理的 NVM 資源建立關聯的容量集合。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.8</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.8, 文件頁 125-129, PDF 頁 151-155</p></details>
<div class="table-wrap"><table><caption>Namespace、CMB、PMR 與容量</caption><thead><tr><th scope="col">記憶體或容量層級</th><th scope="col">提供哪種資源</th><th scope="col">使用或比較前的確認</th></tr></thead><tbody><tr><td>CMB</td><td>controller-provided working memory</td><td>是否能放 SQ/CQ/list/data 由能力 bit 決定</td></tr><tr><td>PMR</td><td>具有持久性語意的 region</td><td>enable、ready、error 與 address control 要一起看</td></tr><tr><td>capacity model</td><td>subsystem／group／set／namespace 的容量</td><td>不同層級欄位不可直接相減</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.03">04.03.</span><span class="paragraph-text">說明性範例：CMB size 足以容納一個 SQ，不代表 controller 的 namespace 多出同樣容量；前者是 queue/data structure 的放置資源，後者才是 host 可格式化與存取的非揮發性容量。</span></p></aside>
</section>
<section class="lesson" id="module-lifecycle"><h2 id="heading-lifecycle"><span class="section-number">05</span> Shutdown、Reset 與狀態保留</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span><span class="paragraph-text">Lifecycle 事件的共同問題是『哪一層狀態仍有效』。Normal shutdown 由 CC.SHN/CSTS.SHST 協調，reset 分成 subsystem/controller/queue 層級，Keep Alive 監測 host-controller 存活，firmware activation 又可能要求特定 reset。相同的『暫時無法處理 command』症狀，不代表可以使用相同 recovery。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>SHN</dt><dd>Shutdown Notification，CC 中由 host 宣告 shutdown 類型的欄位。</dd></div></dl>
<!-- claim:BASE3-SHUTDOWN -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.02">05.02.</span><span class="paragraph-text">正常 shutdown 由 host 設定 CC.SHN，controller 透過 CSTS.SHST 回報進度；NVM subsystem shutdown 是更大範圍的處理，不能與單一 controller shutdown 混為一談。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.6.1, 3.6.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, 文件頁 113-120, PDF 頁 139-146</p></details>
<div class="table-wrap"><table><caption>Shutdown、Reset 與狀態保留</caption><thead><tr><th scope="col">停止或重設事件</th><th scope="col">影響的對象與目的</th><th scope="col">判斷完成或保留狀態的資訊</th></tr></thead><tbody><tr><td>normal shutdown</td><td>保護性停止與狀態回報</td><td>看 SHN/SHST</td></tr><tr><td>controller reset</td><td>controller 層級狀態</td><td>queue 是否保留要依 reset 類型</td></tr><tr><td>NVM subsystem reset</td><td>更大 subsystem scope</td><td>可能影響多個 controllers</td></tr><tr><td>Keep Alive timeout</td><td>liveness failure</td><td>不能直接等同 media failure</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="05.03">05.03.</span><span class="paragraph-text">說明性範例：host 要做 normal shutdown 時先停止提交新 I/O，設定 CC.SHN，再監看 CSTS.SHST。若等待期間發生 controller fatal status，後續 recovery 應按 reset scope 重建資源，而不是假設 normal shutdown 已完成。</span></p></aside>
</section>
<section id="spec-reading"><h2>接著打開 Spec 看什麼</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.01">06.01.</span><span class="paragraph-text">以下按概念列出閱讀位置。報告時先用上面的流程說明問題，再打開對應章節看欄位與完整條件。中文教學 HTML 另有本篇全部圖表的逐圖重點、案例與細節。</span></p>
<div class="table-wrap"><table><thead><tr><th scope="col">要說明的觀念</th><th scope="col">Spec 閱讀位置</th></tr></thead><tbody><tr><td>Controller 類型、識別碼與能力</td><td>Base 2.4 §3.1.1 · Base 2.4 §3.1.3-3.1.3.2 · Base 2.4 §3.1.3</td></tr><tr><td>從設定到 CSTS.RDY：初始化流程</td><td>Base 2.4 §3.1.4 · Base 2.4 §3.5.1, 3.5.3-3.5.4</td></tr><tr><td>Queue 位置與命令選取</td><td>Base 2.4 §3.3.1 · Base 2.4 §3.4.1-3.4.5 · Base 2.4 §3.1.3</td></tr><tr><td>Namespace、CMB、PMR 與容量</td><td>Base 2.4 §3.1.4 · Base 2.4 §3.8 · Base 2.4 §3.2.2-3.2.4</td></tr><tr><td>Shutdown、Reset 與狀態保留</td><td>Base 2.4 §3.6.1, 3.6.3 · Base 2.4 §3.7 · Base 2.4 §3.9 · Base 2.4 §3.10-3.11</td></tr></tbody></table></div>
<a class="reading-link" href="/DOCS/nvme-spec-report/base-ch3/tutorial-zh-tw.html">開啟完整中文教學與逐圖解釋 →</a></section>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:base-ch3-ready -->
<details class="review-question" id="qa-base-ch3-ready"><summary>1. 讀到 controller 支援某功能，是否表示它已準備接收 I/O？</summary>
<div data-qa-answer="base-ch3-ready"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.01">07.01.</span><span class="paragraph-text">Capability 描述能做什麼；初始化與 ready state 描述目前能否開始操作。仍須完成 queue 設定、啟用與 readiness 確認，再依適用條件使用該功能。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, 文件頁 52-54, PDF 頁 78-80</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, 文件頁 105-113, PDF 頁 131-139</p>
</details></details>
<!-- qa:base-ch3-queue-order -->
<details class="review-question" id="qa-base-ch3-queue-order"><summary>2. SQ 中先提交的命令，是否必定先完成？</summary>
<div data-qa-answer="base-ch3-queue-order"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.02">07.02.</span><span class="paragraph-text">Queue 提交順序、controller 選取工作及完成順序是不同概念。一般不能只靠 SQ 位置推論完成順序；有相依性時應使用規格定義的同步或命令機制。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1, 文件頁 88-91, PDF 頁 114-117</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, 文件頁 101-105, PDF 頁 127-131</p>
</details></details>
<!-- qa:base-ch3-shutdown-reset -->
<details class="review-question" id="qa-base-ch3-shutdown-reset"><summary>3. 為何正常關機流程不能直接等同 reset？</summary>
<div data-qa-answer="base-ch3-shutdown-reset"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.03">07.03.</span><span class="paragraph-text">Shutdown 包含 host 的通知及 controller 的完成狀態，讓關機前的處理有明確交接；reset 依其層級改變 controller 或 subsystem 狀態。它們的觸發、範圍和保留狀態不同。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, 文件頁 113-120, PDF 頁 139-146</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §3.7, 文件頁 120-125, PDF 頁 146-151</p>
</details></details>
<!-- qa:base-ch3-memory-regions -->
<details class="review-question" id="qa-base-ch3-memory-regions"><summary>4. Controller 可見的記憶體區域，為何不能全都當成 namespace 容量？</summary>
<div data-qa-answer="base-ch3-memory-regions"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.04">07.04.</span><span class="paragraph-text">Namespace 提供以 logical blocks 存取的儲存空間；CMB、PMR 等區域有各自用途、存取方式及持久性規則。位於同一裝置不代表它們使用相同的容量與資料模型。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, 文件頁 80-85, PDF 頁 106-111</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §3.8, 文件頁 125-129, PDF 頁 151-155</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
