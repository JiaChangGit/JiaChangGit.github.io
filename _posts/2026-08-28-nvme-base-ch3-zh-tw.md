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
<details class="technical-note"><summary>完整規則：Controller 類型、識別碼與能力</summary>
<!-- claim:BASE3-STATIC -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">memory-based controller 必須（shall）只支援 static controller model。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.1, 文件頁 38, PDF 頁 64</p></details>
<!-- claim:BASE3-TYPES -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">本輪只使用 I/O controller 與 Administrative controller：前者可執行使用者資料的 I/O，後者以管理為目的且不支援資料 I/O command。兩者都具有一組 Admin Submission／Completion Queue。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Administrative controller</dt><dd>Administrative controller，以管理為目的且不執行使用者資料 I/O command 的 controller 類型。</dd></div><div><dt>I/O controller</dt><dd>I/O controller，可執行使用者資料 I/O command 的 controller 類型。</dd></div><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.3-3.1.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3-3.1.3.2, 文件頁 39-43, PDF 頁 65-69</p></details>
<!-- claim:BASE3-ORDER -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.04">01.04.</span><span class="paragraph-text">除 fused operation 外，controller 取走的命令與完成沒有一般性的先後保證；若有順序需求，強制該順序是 host 的責任。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3, 文件頁 40, PDF 頁 66</p></details>
</details>
<div class="table-wrap"><table><caption>Controller 類型、識別碼與能力</caption><thead><tr><th scope="col">控制器類型或標示</th><th scope="col">可以處理的工作</th><th scope="col">支援能力如何確認</th></tr></thead><tbody><tr><td>I/O controller</td><td>可執行使用者資料 I/O</td><td>仍需逐項查 optional capability</td></tr><tr><td>Administrative controller</td><td>管理用途、無資料 I/O command</td><td>不能因有 Admin Queue 就當成 I/O controller</td></tr><tr><td>支援標示</td><td>針對 row 與上下文描述強度</td><td>不能脫離 column／footnote 解讀</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>Administrative controller</dt><dd>Administrative controller，以管理為目的且不執行使用者資料 I/O command 的 controller 類型。</dd></div><div><dt>I/O controller</dt><dd>I/O controller，可執行使用者資料 I/O command 的 controller 類型。</dd></div><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.05">01.05.</span><span class="paragraph-text">說明性範例：偵測到一個 Administrative controller 時，軟體仍會建立 Admin SQ/CQ 並執行管理 command，但不應把 namespace data path 掛到它。若只用『存在 Admin Queue』判斷 controller type，I/O 與 Administrative controller 會被錯誤歸成同類。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div><div><dt>CQ</dt><dd>Completion Queue，controller 放入完成結果的完成佇列。</dd></div><div><dt>SQ</dt><dd>Submission Queue，主機放入命令的提交佇列。</dd></div></dl></aside>
<a class="reading-link" href="#reading-identity">閱讀相關規格圖表 → Controller 類型、識別碼與能力</a>
</section>
<section class="lesson" id="module-properties-init"><h2 id="heading-properties-init"><span class="section-number">02</span> 從設定到 CSTS.RDY：初始化流程</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">Properties 不是彼此獨立的 register 清單。CAP 先限制 page size、queue 與 timeout 能力；AQA、ASQ、ACQ 建立 Admin queues；CC 選擇設定並以 EN 啟動；最後由 CSTS.RDY 宣告 controller 已能正常處理命令。Figures 33-46 與 Figure 57 應沿這條因果鏈閱讀。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CSTS</dt><dd>Controller Status，controller 回報 ready、fatal status 與 shutdown 狀態的 property。</dd></div><div><dt>ACQ</dt><dd>Admin Completion Queue Base Address，Admin CQ 在可定址記憶體中的基底位址。</dd></div><div><dt>AQA</dt><dd>Admin Queue Attributes，描述 Admin SQ 與 Admin CQ 大小的 property。</dd></div><div><dt>ASQ</dt><dd>Admin Submission Queue Base Address，Admin SQ 在可定址記憶體中的基底位址。</dd></div><div><dt>CAP</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。</dd></div><div><dt>RDY</dt><dd>Ready，CSTS 中表示 controller 是否已準備正常處理 command 的 bit。</dd></div><div><dt>CC</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。</dd></div><div><dt>EN</dt><dd>Enable，CC 中控制 controller enable state 的 bit。</dd></div></dl>
<details class="technical-note"><summary>完整規則：從設定到 CSTS.RDY：初始化流程</summary>
<!-- claim:BASE3-PROPERTY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">host 必須（shall）以 property 指定的寬度，從 property 起始 offset 存取；memory-based controller 的實際存取規則由 PCIe Transport 補充。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>offset</dt><dd>offset；從指定起點算出的位移。它回答「離起點多遠」，不等於 index。</dd></div><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div><div><dt>PCIe</dt><dd>PCI Express，NVMe memory-based controller 使用的 transport 與裝置互連。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, 文件頁 52-54, PDF 頁 78-80</p></details>
<!-- claim:BASE3-INIT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">PCIe 初始化以 CAP 判斷能力與 timeout，設定 AQA／ASQ／ACQ 與 CC，接著等待 CSTS.RDY。ready mode 與 CRTO 會影響 host 等待與錯誤處理。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CRTO</dt><dd>Controller Ready Timeouts，回報特定 ready mode 所需等待時間的 property。</dd></div><div><dt>CSTS</dt><dd>Controller Status，controller 回報 ready、fatal status 與 shutdown 狀態的 property。</dd></div><div><dt>PCIe</dt><dd>PCI Express，NVMe memory-based controller 使用的 transport 與裝置互連。</dd></div><div><dt>ACQ</dt><dd>Admin Completion Queue Base Address，Admin CQ 在可定址記憶體中的基底位址。</dd></div><div><dt>AQA</dt><dd>Admin Queue Attributes，描述 Admin SQ 與 Admin CQ 大小的 property。</dd></div><div><dt>ASQ</dt><dd>Admin Submission Queue Base Address，Admin SQ 在可定址記憶體中的基底位址。</dd></div><div><dt>CAP</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。</dd></div><div><dt>RDY</dt><dd>Ready，CSTS 中表示 controller 是否已準備正常處理 command 的 bit。</dd></div><div><dt>CC</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.5.1, 3.5.3-3.5.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, 文件頁 105-113, PDF 頁 131-139</p></details>
</details>
<div class="table-wrap"><table><caption>從設定到 CSTS.RDY：初始化流程</caption><thead><tr><th scope="col">Property 或設定</th><th scope="col">主機與控制器各自提供什麼</th><th scope="col">初始化時的先後關係</th></tr></thead><tbody><tr><td>CAP</td><td>能力與界限</td><td>在寫設定前讀</td></tr><tr><td>AQA/ASQ/ACQ</td><td>Admin queue 大小與位址</td><td>需符合 page/alignment 能力</td></tr><tr><td>CC</td><td>host 選擇與 enable</td><td>寫入值要與 CAP 相容</td></tr><tr><td>CSTS</td><td>controller 回報狀態</td><td>RDY/CFS/SHST 不可互相替代</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>SHST</dt><dd>Shutdown Status，CSTS 中由 controller 回報 shutdown 進度的欄位。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.04">02.04.</span><span class="paragraph-text">說明性範例：host 選擇 4 KiB MPS，ASQ 與 ACQ base address 因而必須依該 page size 對齊。寫 CC.EN=1 後，host 以 CAP／CRTO 指定的時間界限等待 CSTS.RDY=1；若 CFS 先出現，流程應進入 error recovery，而不是繼續建立 I/O queues。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CRTO</dt><dd>Controller Ready Timeouts，回報特定 ready mode 所需等待時間的 property。</dd></div><div><dt>MPS</dt><dd>Memory Page Size，controller 使用的 memory page 大小設定；影響 queue address 與 PRP 對齊。</dd></div><div><dt>EN</dt><dd>Enable，CC 中控制 controller enable state 的 bit。</dd></div></dl></aside>
<a class="reading-link" href="#reading-properties-init">閱讀相關規格圖表 → 從設定到 CSTS.RDY：初始化流程</a>
</section>
<section class="lesson" id="module-queue-arbitration"><h2 id="heading-queue-arbitration"><span class="section-number">03</span> Queue 位置與命令選取</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">Figure 73/74 說明 queue 的 empty/full 判定，Figure 80/81 說明多個 SQ 競爭 controller 服務時的 arbitration。前者處理單一 ring 的 head/tail 狀態，後者處理多個 candidate SQ 的選擇；priority 屬於 SQ，不是每筆 command 自帶的獨立優先權。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>SQ</dt><dd>Submission Queue，主機放入命令的提交佇列。</dd></div></dl>
<details class="technical-note"><summary>完整規則：Queue 位置與命令選取</summary>
<!-- claim:BASE3-QUEUE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span><span class="paragraph-text">PCIe queue 由 host-addressable memory 中的環形 buffer、head 與 tail pointer 構成。host 建立 I/O Completion Queue 後再建立對應 Submission Queue，並以 doorbell 推進 pointer。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1, 文件頁 88-91, PDF 頁 114-117</p></details>
<!-- claim:BASE3-PROCESS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.03">03.03.</span><span class="paragraph-text">command processing 要分開看 ordering、fused／atomic semantics、arbitration 與 outstanding command 上限；priority 屬於 Submission Queue，不是每一筆 command 的獨立欄位。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.4.1-3.4.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, 文件頁 101-105, PDF 頁 127-131</p></details>
</details>
<div class="table-wrap"><table><caption>Queue 位置與命令選取</caption><thead><tr><th scope="col">佇列狀態或選取方式</th><th scope="col">它決定什麼</th><th scope="col">不能由此推論什麼</th></tr></thead><tbody><tr><td>empty</td><td>head == tail 且 phase／ownership 符合 empty 定義</td><td>沒有可取走 entry</td></tr><tr><td>full</td><td>下一個 tail 會追上尚未釋放 head</td><td>host 不得覆寫 entry</td></tr><tr><td>Round Robin</td><td>候選 SQ 輪流取得服務</td><td>不代表 command completion 依提交順序</td></tr><tr><td>Weighted RR + Urgent</td><td>priority class 與 weight 影響選擇</td><td>仍需依適用設定解讀</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.04">03.04.</span><span class="paragraph-text">說明性範例：深度 4 的 SQ 只有四個 slot，但 full/empty 判定還需要 ownership 規則；不能只用 tail-head 的無號差值。若 SQ 1 與 SQ 2 同時有 command，arbiter 先選 SQ 2 也不代表 SQ 2 的 command 一定先完成，因 command 執行時間仍可能不同。</span></p></aside>
<a class="reading-link" href="#reading-queue-arbitration">閱讀相關規格圖表 → Queue 位置與命令選取</a>
</section>
<section class="lesson" id="module-memory-capacity"><h2 id="heading-memory-capacity"><span class="section-number">04</span> Namespace、CMB、PMR 與容量</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">CMB/PMR properties 描述 controller 暴露的 memory region 位置、能力與狀態；capacity Figures 86-89 描述 NVM subsystem 各層級可用或已配置容量。兩者都談 memory，卻不是同一種空間，也不能用同一個『剩餘容量』欄位合併。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NVM subsystem</dt><dd>NVM subsystem，包含 controller、port、namespace 與非揮發性儲存資源的 NVMe 系統邊界。</dd></div><div><dt>CMB</dt><dd>Controller Memory Buffer，controller 提供、可放置部分 queue 或資料結構的記憶體區域。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div><div><dt>PMR</dt><dd>Persistent Memory Region，由 controller 暴露、具有持久性語意的記憶體區域。</dd></div></dl>
<details class="technical-note"><summary>完整規則：Namespace、CMB、PMR 與容量</summary>
<!-- claim:BASE3-CAPACITY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">capacity model 分開追蹤 NVM subsystem、Endurance Group、NVM Set 與 namespace 的可用或配置容量；同一數值不可跨層級直接比較。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Endurance Group</dt><dd>Endurance Group，用於隔離與回報耐久度相關狀態的 NVM 資源群組。</dd></div><div><dt>NVM subsystem</dt><dd>NVM subsystem，包含 controller、port、namespace 與非揮發性儲存資源的 NVMe 系統邊界。</dd></div><div><dt>NVM Set</dt><dd>NVM Set，把 namespace 與一組共同管理的 NVM 資源建立關聯的容量集合。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.8</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.8, 文件頁 125-129, PDF 頁 151-155</p></details>
<!-- claim:BASE3-MEDIA -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.03">04.03.</span><span class="paragraph-text">NVM Set、Endurance Group、Reclaim Group 與 Reclaim Unit 分別描述容量集合、耐久度管理與回收粒度。是否支援及其 identifier 由 Identify／log page 能力判定。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Endurance Group</dt><dd>Endurance Group，用於隔離與回報耐久度相關狀態的 NVM 資源群組。</dd></div><div><dt>Reclaim Group</dt><dd>Reclaim Group，具有共同回收行為的一組非揮發性儲存資源。</dd></div><div><dt>Reclaim Unit</dt><dd>Reclaim Unit，controller 執行媒體回收時使用的較小管理粒度。</dd></div><div><dt>NVM Set</dt><dd>NVM Set，把 namespace 與一組共同管理的 NVM 資源建立關聯的容量集合。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.2.2-3.2.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, 文件頁 80-85, PDF 頁 106-111</p></details>
</details>
<div class="table-wrap"><table><caption>Namespace、CMB、PMR 與容量</caption><thead><tr><th scope="col">記憶體或容量層級</th><th scope="col">提供哪種資源</th><th scope="col">使用或比較前的確認</th></tr></thead><tbody><tr><td>CMB</td><td>controller-provided working memory</td><td>是否能放 SQ/CQ/list/data 由能力 bit 決定</td></tr><tr><td>PMR</td><td>具有持久性語意的 region</td><td>enable、ready、error 與 address control 要一起看</td></tr><tr><td>capacity model</td><td>subsystem／group／set／namespace 的容量</td><td>不同層級欄位不可直接相減</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>CMB</dt><dd>Controller Memory Buffer，controller 提供、可放置部分 queue 或資料結構的記憶體區域。</dd></div><div><dt>PMR</dt><dd>Persistent Memory Region，由 controller 暴露、具有持久性語意的記憶體區域。</dd></div><div><dt>CQ</dt><dd>Completion Queue，controller 放入完成結果的完成佇列。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.04">04.04.</span><span class="paragraph-text">說明性範例：CMB size 足以容納一個 SQ，不代表 controller 的 namespace 多出同樣容量；前者是 queue/data structure 的放置資源，後者才是 host 可格式化與存取的非揮發性容量。</span></p></aside>
<a class="reading-link" href="#reading-memory-capacity">閱讀相關規格圖表 → Namespace、CMB、PMR 與容量</a>
</section>
<section class="lesson" id="module-lifecycle"><h2 id="heading-lifecycle"><span class="section-number">05</span> Shutdown、Reset 與狀態保留</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span><span class="paragraph-text">Lifecycle 事件的共同問題是『哪一層狀態仍有效』。Normal shutdown 由 CC.SHN/CSTS.SHST 協調，reset 分成 subsystem/controller/queue 層級，Keep Alive 監測 host-controller 存活，firmware activation 又可能要求特定 reset。相同的『暫時無法處理 command』症狀，不代表可以使用相同 recovery。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>SHST</dt><dd>Shutdown Status，CSTS 中由 controller 回報 shutdown 進度的欄位。</dd></div><div><dt>SHN</dt><dd>Shutdown Notification，CC 中由 host 宣告 shutdown 類型的欄位。</dd></div></dl>
<details class="technical-note"><summary>完整規則：Shutdown、Reset 與狀態保留</summary>
<!-- claim:BASE3-SHUTDOWN -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.02">05.02.</span><span class="paragraph-text">正常 shutdown 由 host 設定 CC.SHN，controller 透過 CSTS.SHST 回報進度；NVM subsystem shutdown 是更大範圍的處理，不能與單一 controller shutdown 混為一談。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>SHN</dt><dd>Shutdown Notification，CC 中由 host 宣告 shutdown 類型的欄位。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.6.1, 3.6.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, 文件頁 113-120, PDF 頁 139-146</p></details>
<!-- claim:BASE3-RESET -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.03">05.03.</span><span class="paragraph-text">NVM Subsystem Reset、Controller Level Reset 與 Queue Level Reset 的影響範圍不同；設計 recovery flow 前先確認哪一層狀態會被清除、queue 是否仍存在。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.7, 文件頁 120-125, PDF 頁 146-151</p></details>
<!-- claim:BASE3-KEEPALIVE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.04">05.04.</span><span class="paragraph-text">Keep Alive 以 KATO／KATT 建立 host 與 controller 的存活監測；本報告只保留 controller 共通與 PCIe 可用的 timer、command 與 timeout 行為。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>KATO</dt><dd>Keep Alive Timeout，host 與 controller 約定的存活逾時設定。</dd></div><div><dt>KATT</dt><dd>Keep Alive Timeout Total，controller 用於偵測逾時的總時間基準。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.9</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.9, 文件頁 129-135, PDF 頁 155-161</p></details>
<!-- claim:BASE3-FIRMWARE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.05">05.05.</span><span class="paragraph-text">privileged action 會影響其他 host 或 controller；firmware update 分成 image download、commit／activate 與可能的 reset，host 依回報的 activation action 安排流程。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.10-3.11</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.10-3.11, 文件頁 135-138, PDF 頁 161-164</p></details>
</details>
<div class="table-wrap"><table><caption>Shutdown、Reset 與狀態保留</caption><thead><tr><th scope="col">停止或重設事件</th><th scope="col">影響的對象與目的</th><th scope="col">判斷完成或保留狀態的資訊</th></tr></thead><tbody><tr><td>normal shutdown</td><td>保護性停止與狀態回報</td><td>看 SHN/SHST</td></tr><tr><td>controller reset</td><td>controller 層級狀態</td><td>queue 是否保留要依 reset 類型</td></tr><tr><td>NVM subsystem reset</td><td>更大 subsystem scope</td><td>可能影響多個 controllers</td></tr><tr><td>Keep Alive timeout</td><td>liveness failure</td><td>不能直接等同 media failure</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="05.06">05.06.</span><span class="paragraph-text">說明性範例：host 要做 normal shutdown 時先停止提交新 I/O，設定 CC.SHN，再監看 CSTS.SHST。若等待期間發生 controller fatal status，後續 recovery 應按 reset scope 重建資源，而不是假設 normal shutdown 已完成。</span></p></aside>
<a class="reading-link" href="#reading-lifecycle">閱讀相關規格圖表 → Shutdown、Reset 與狀態保留</a>
</section>
<details class="figure-reading-fold"><summary>展開圖表教學：依主軸閱讀來源圖表</summary>
<section id="figure-reading"><h2><span class="section-number">06</span> 讀懂本篇的規格圖表</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.01">06.01.</span><span class="paragraph-text">以下依概念整理規格中的圖表。每組先說明讀取順序與要判斷的問題，接著列出各圖的欄位或行為說明。可以由正文的連結跳到對應組別，也可以用這一節檢查自己能否把欄位連回完整操作。</span></p>
<div class="figure-reading-group" id="reading-identity"><h3>圖表組 01 · Controller 類型、識別碼與能力</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.02">06.02.</span><span class="paragraph-text">先按 controller type 選表格欄，再看每項命令或功能的支援標示。識別碼表回答「是哪一個」，能力表回答「能做什麼」；兩者要在同一控制器的上下文中連接。</span></p>
<a class="reading-link" href="#module-identity">回到本節的解釋與範例</a>
<!-- figure-table:BASE3-FIG-023 -->
<details class="field-note" id="figure-BASE3-FIG-023"><summary>Base Figure 23 · Controller Types</summary>
<!-- claim:BASE3-FIG-023-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.03">06.03.</span><span class="paragraph-text">Figure 23〈Controller Types〉：Controller type 決定控制器角色，Controller ID 辨認具體對象。高值識別碼另有保留或特殊用途，應依清單解讀，不能把 FFF0h–FFFFh 全部當成一般可指派的控制器編號。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3, Figure 23, 文件頁 39, PDF 頁 65</p></details>

</details>
<!-- figure-table:BASE3-FIG-024 -->
<details class="field-note" id="figure-BASE3-FIG-024"><summary>Base Figure 24 · NVM Subsystem with Three I/O Controllers</summary>
<!-- claim:BASE3-FIG-024-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.04">06.04.</span><span class="paragraph-text">Figure 24〈NVM Subsystem with Three I/O Controllers〉：將 controller、port 與 namespace 分別標示，再沿連線看存取關係。多個控制器可以處在同一 subsystem；Administrative controller 的管理角色不能用來推論它也處理 namespace 資料 I/O。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.1, Figure 24, 文件頁 41, PDF 頁 67</p></details>

</details>
<!-- figure-table:BASE3-FIG-025 -->
<details class="field-note" id="figure-BASE3-FIG-025"><summary>Base Figure 25 · NVM Subsystem with One Administrative and Two I/O Controllers</summary>
<!-- claim:BASE3-FIG-025-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.05">06.05.</span><span class="paragraph-text">Figure 25〈NVM Subsystem with One Administrative and Two I/O Controllers〉：將 controller、port 與 namespace 分別標示，再沿連線看存取關係。多個控制器可以處在同一 subsystem；Administrative controller 的管理角色不能用來推論它也處理 namespace 資料 I/O。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.2, Figure 25, 文件頁 42, PDF 頁 68</p></details>

</details>
<!-- figure-table:BASE3-FIG-026 -->
<details class="field-note" id="figure-BASE3-FIG-026"><summary>Base Figure 26 · NVM Subsystem with One Administrative Controller</summary>
<!-- claim:BASE3-FIG-026-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.06">06.06.</span><span class="paragraph-text">Figure 26〈NVM Subsystem with One Administrative Controller〉：將 controller、port 與 namespace 分別標示，再沿連線看存取關係。多個控制器可以處在同一 subsystem；Administrative controller 的管理角色不能用來推論它也處理 namespace 資料 I/O。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.2, Figure 26, 文件頁 42, PDF 頁 68</p></details>

</details>
<!-- figure-table:BASE3-FIG-027 -->
<details class="field-note" id="figure-BASE3-FIG-027"><summary>Base Figure 27 · Controller IDs FFF0h to FFFFh</summary>
<!-- claim:BASE3-FIG-027-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.07">06.07.</span><span class="paragraph-text">Figure 27〈Controller IDs FFF0h to FFFFh〉：Controller type 決定控制器角色，Controller ID 辨認具體對象。高值識別碼另有保留或特殊用途，應依清單解讀，不能把 FFF0h–FFFFh 全部當成一般可指派的控制器編號。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.3.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.3, Figure 27, 文件頁 44, PDF 頁 70</p></details>

</details>
<!-- figure-table:BASE3-FIG-028 -->
<details class="field-note" id="figure-BASE3-FIG-028"><summary>Base Figure 28 · Admin Command Support Requirements</summary>
<!-- claim:BASE3-FIG-028-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.08">06.08.</span><span class="paragraph-text">Figure 28〈Admin Command Support Requirements〉：先選控制器類型，再讀命令、log 或 Feature 所在列的支援標示。帶有數字註腳的標示必須連同條件閱讀；同一功能在另一種控制器類型下可能有不同要求。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.3.3.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.3.3, Figure 28, 文件頁 45-47, PDF 頁 71-73</p></details>

</details>
<!-- figure-table:BASE3-FIG-030 -->
<details class="field-note" id="figure-BASE3-FIG-030"><summary>Base Figure 30 · Common I/O Command Support Requirements</summary>
<!-- claim:BASE3-FIG-030-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.09">06.09.</span><span class="paragraph-text">Figure 30〈Common I/O Command Support Requirements〉：先選控制器類型，再讀命令、log 或 Feature 所在列的支援標示。帶有數字註腳的標示必須連同條件閱讀；同一功能在另一種控制器類型下可能有不同要求。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.3.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.4, Figure 30, 文件頁 47-48, PDF 頁 73-74</p></details>

</details>
<!-- figure-table:BASE3-FIG-031 -->
<details class="field-note" id="figure-BASE3-FIG-031"><summary>Base Figure 31 · Log Page Support Requirements</summary>
<!-- claim:BASE3-FIG-031-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.10">06.10.</span><span class="paragraph-text">Figure 31〈Log Page Support Requirements〉：先選控制器類型，再讀命令、log 或 Feature 所在列的支援標示。帶有數字註腳的標示必須連同條件閱讀；同一功能在另一種控制器類型下可能有不同要求。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.3.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.4, Figure 31, 文件頁 48-50, PDF 頁 74-76</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>FDP</dt><dd>Flexible Data Placement，把資料放置提示與媒體回收管理連結的能力。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-032 -->
<details class="field-note" id="figure-BASE3-FIG-032"><summary>Base Figure 32 · Feature Support Requirements</summary>
<!-- claim:BASE3-FIG-032-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.11">06.11.</span><span class="paragraph-text">Figure 32〈Feature Support Requirements〉：先選控制器類型，再讀命令、log 或 Feature 所在列的支援標示。帶有數字註腳的標示必須連同條件閱讀；同一功能在另一種控制器類型下可能有不同要求。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.3.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.5, Figure 32, 文件頁 50-52, PDF 頁 76-78</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-properties-init"><h3>圖表組 02 · 從設定到 CSTS.RDY：初始化流程</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.12">06.12.</span><span class="paragraph-text">沿能力→佇列配置→啟用→就緒的順序連接 CAP、AQA／ASQ／ACQ、CC、CSTS。寄存器布局圖中的 offset 是定位欄位，狀態圖中的箭頭才描述條件成立後的轉移。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>offset</dt><dd>offset；從指定起點算出的位移。它回答「離起點多遠」，不等於 index。</dd></div></dl>
<a class="reading-link" href="#module-properties-init">回到本節的解釋與範例</a>
<!-- figure-table:BASE3-FIG-033 -->
<details class="field-note" id="figure-BASE3-FIG-033"><summary>Base Figure 33 · Property Definition</summary>
<!-- claim:BASE3-FIG-033-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.13">06.13.</span><span class="paragraph-text">Figure 33〈Property Definition〉：Property 索引先列出位址與名稱，個別欄位表再定義讀寫方式和內容。Memory-based 的 Doorbell 間距由 CAP.DSTRD 決定，不能把索引表中的第一組位置直接複製到所有佇列。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>DSTRD</dt><dd>Doorbell Stride，CAP 中決定相鄰 doorbell register 間距的欄位。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, Figure 33, 文件頁 52-53, PDF 頁 78-79</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>OFST</dt><dd>Offset，Firmware Image Download 中以 dword 為單位的 image-relative offset。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-034 -->
<details class="field-note" id="figure-BASE3-FIG-034"><summary>Base Figure 34 · Memory-Based Property Definition</summary>
<!-- claim:BASE3-FIG-034-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.14">06.14.</span><span class="paragraph-text">Figure 34〈Memory-Based Property Definition〉：Property 索引先列出位址與名稱，個別欄位表再定義讀寫方式和內容。Memory-based 的 Doorbell 間距由 CAP.DSTRD 決定，不能把索引表中的第一組位置直接複製到所有佇列。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>DSTRD</dt><dd>Doorbell Stride，CAP 中決定相鄰 doorbell register 間距的欄位。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, Figure 34, 文件頁 54, PDF 頁 80</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CAP.DSTRD</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.DSTRD 進一步指定其中的 DSTRD 子欄位。</dd></div><div><dt>OFST</dt><dd>Offset，Firmware Image Download 中以 dword 為單位的 image-relative offset。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-036 -->
<details class="field-note" id="figure-BASE3-FIG-036"><summary>Base Figure 36 · Offset 0h: CAP - Controller Capabilities</summary>
<!-- claim:BASE3-FIG-036-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.15">06.15.</span><span class="paragraph-text">Figure 36〈Offset 0h: CAP - Controller Capabilities〉：CAP 回報支援能力、大小與時間限制，主機以這些資訊選擇可用設定。讀到支援位並不表示對應功能已啟用或控制器已就緒；設定與目前狀態要再讀各自的欄位。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, 文件頁 55-58, PDF 頁 81-84</p></details>

</details>
<!-- figure-table:BASE3-FIG-037 -->
<details class="field-note" id="figure-BASE3-FIG-037"><summary>Base Figure 37 · Specification Version Descriptor</summary>
<!-- claim:BASE3-FIG-037-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.16">06.16.</span><span class="paragraph-text">Figure 37〈Specification Version Descriptor〉：版本描述子把 major、minor、tertiary 分開編碼。先分解欄位再比較版本；Version property 的重設值描述回報的版本，不是命令執行次數，也不代表所有選用功能都支援。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 37, 文件頁 58, PDF 頁 84</p></details>

</details>
<!-- figure-table:BASE3-FIG-038 -->
<details class="field-note" id="figure-BASE3-FIG-038"><summary>Base Figure 38 · NVM Express Base Specification Version Property Reset Values</summary>
<!-- claim:BASE3-FIG-038-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.17">06.17.</span><span class="paragraph-text">Figure 38〈NVM Express Base Specification Version Property Reset Values〉：版本描述子把 major、minor、tertiary 分開編碼。先分解欄位再比較版本；Version property 的重設值描述回報的版本，不是命令執行次數，也不代表所有選用功能都支援。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 38, 文件頁 58-59, PDF 頁 84-85</p></details>

</details>
<!-- figure-table:BASE3-FIG-041 -->
<details class="field-note" id="figure-BASE3-FIG-041"><summary>Base Figure 41 · Offset 14h: CC - Controller Configuration</summary>
<!-- claim:BASE3-FIG-041-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.18">06.18.</span><span class="paragraph-text">Figure 41〈Offset 14h: CC - Controller Configuration〉：CC 記錄主機的設定與要求，CSTS 回報控制器當前狀態。例如 EN 與 RDY 分別是啟用要求和就緒結果；SHN 與 SHST 則對應關機要求及處理階段。不要只看要求位就判斷動作已完成。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.5, Figure 41, 文件頁 60-63, PDF 頁 86-89</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>MPS</dt><dd>Memory Page Size，controller 使用的 memory page 大小設定；影響 queue address 與 PRP 對齊。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-042 -->
<details class="field-note" id="figure-BASE3-FIG-042"><summary>Base Figure 42 · Offset 1Ch: CSTS - Controller Status</summary>
<!-- claim:BASE3-FIG-042-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.19">06.19.</span><span class="paragraph-text">Figure 42〈Offset 1Ch: CSTS - Controller Status〉：CC 記錄主機的設定與要求，CSTS 回報控制器當前狀態。例如 EN 與 RDY 分別是啟用要求和就緒結果；SHN 與 SHST 則對應關機要求及處理階段。不要只看要求位就判斷動作已完成。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.5, Figure 42, 文件頁 63-65, PDF 頁 89-91</p></details>

</details>
<!-- figure-table:BASE3-FIG-044 -->
<details class="field-note" id="figure-BASE3-FIG-044"><summary>Base Figure 44 · Offset 24h: AQA - Admin Queue Attributes</summary>
<!-- claim:BASE3-FIG-044-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.20">06.20.</span><span class="paragraph-text">Figure 44〈Offset 24h: AQA - Admin Queue Attributes〉：AQA 描述 Admin SQ／CQ 的大小，ASQ 與 ACQ 提供兩個佇列的基底位址。大小欄位採其數量編碼解讀，位址則依所選 page size 對齊；大小正確不能取代位址對齊檢查。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 44, 文件頁 66, PDF 頁 92</p></details>

</details>
<!-- figure-table:BASE3-FIG-045 -->
<details class="field-note" id="figure-BASE3-FIG-045"><summary>Base Figure 45 · Offset 28h: ASQ - Admin Submission Queue Base Address</summary>
<!-- claim:BASE3-FIG-045-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.21">06.21.</span><span class="paragraph-text">Figure 45〈Offset 28h: ASQ - Admin Submission Queue Base Address〉：AQA 描述 Admin SQ／CQ 的大小，ASQ 與 ACQ 提供兩個佇列的基底位址。大小欄位採其數量編碼解讀，位址則依所選 page size 對齊；大小正確不能取代位址對齊檢查。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 45, 文件頁 66, PDF 頁 92</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CC.MPS</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.MPS 進一步指定其中的 MPS 子欄位。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-046 -->
<details class="field-note" id="figure-BASE3-FIG-046"><summary>Base Figure 46 · Offset 30h: ACQ - Admin Completion Queue Base Address</summary>
<!-- claim:BASE3-FIG-046-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.22">06.22.</span><span class="paragraph-text">Figure 46〈Offset 30h: ACQ - Admin Completion Queue Base Address〉：AQA 描述 Admin SQ／CQ 的大小，ASQ 與 ACQ 提供兩個佇列的基底位址。大小欄位採其數量編碼解讀，位址則依所選 page size 對齊；大小正確不能取代位址對齊檢查。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.9</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.9, Figure 46, 文件頁 67, PDF 頁 93</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CC.MPS</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.MPS 進一步指定其中的 MPS 子欄位。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-057 -->
<details class="field-note" id="figure-BASE3-FIG-057"><summary>Base Figure 57 · Offset 68h: CRTO - Controller Ready Timeouts</summary>
<!-- claim:BASE3-FIG-057-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.23">06.23.</span><span class="paragraph-text">Figure 57〈Offset 68h: CRTO - Controller Ready Timeouts〉：Ready timeout 與選擇的就緒模式有關。先核對 CAP.CRMS 的支援及 CC.CRIME 的設定，再選 CRTO 中適用時間；某些 Admin 命令的媒體尚未就緒狀態另依命令清單判斷。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.21</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.21, Figure 57, 文件頁 73, PDF 頁 99</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CAP.CRMS.CRIMS</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.CRMS.CRIMS 進一步指定其中的 CRMS.CRIMS 子欄位。</dd></div><div><dt>CC.CRIME</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.CRIME 進一步指定其中的 CRIME 子欄位。</dd></div><div><dt>CC.EN</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.EN 進一步指定其中的 EN 子欄位。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-039 -->
<details class="field-note" id="figure-BASE3-FIG-039"><summary>Base Figure 39 · Offset Ch: INTMS - Interrupt Mask Set</summary>
<!-- claim:BASE3-FIG-039-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.24">06.24.</span><span class="paragraph-text">Figure 39〈Offset Ch: INTMS - Interrupt Mask Set〉：INTMS 和 INTMC 分別用來設定與清除中斷遮罩。相同 bit 位置對應相同遮罩對象，但寫入語意相反；清除遮罩不代表已移除 CQ 中尚未處理的完成項目。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.2, Figure 39, 文件頁 59, PDF 頁 85</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>MSI</dt><dd>Message Signaled Interrupt，透過 memory write message 傳遞 interrupt 的 PCI 機制。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-040 -->
<details class="field-note" id="figure-BASE3-FIG-040"><summary>Base Figure 40 · Offset 10h: INTMC - Interrupt Mask Clear</summary>
<!-- claim:BASE3-FIG-040-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.25">06.25.</span><span class="paragraph-text">Figure 40〈Offset 10h: INTMC - Interrupt Mask Clear〉：INTMS 和 INTMC 分別用來設定與清除中斷遮罩。相同 bit 位置對應相同遮罩對象，但寫入語意相反；清除遮罩不代表已移除 CQ 中尚未處理的完成項目。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.2, Figure 40, 文件頁 59, PDF 頁 85</p></details>

</details>
<!-- figure-table:BASE3-FIG-049 -->
<details class="field-note" id="figure-BASE3-FIG-049"><summary>Base Figure 49 · Offset 40h: BPINFO - Boot Partition Information</summary>
<!-- claim:BASE3-FIG-049-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.26">06.26.</span><span class="paragraph-text">Figure 49〈Offset 40h: BPINFO - Boot Partition Information〉：BPINFO 提供 active partition、大小與讀取狀態；BPRSEL 選擇要讀取的 partition、範圍；BPMBL 指向主機接收資料的記憶體。要求讀哪個 partition 與目前 active partition 是兩個不同資訊。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.12, Figure 49, 文件頁 69, PDF 頁 95</p></details>

</details>
<!-- figure-table:BASE3-FIG-050 -->
<details class="field-note" id="figure-BASE3-FIG-050"><summary>Base Figure 50 · Offset 44h: BPRSEL - Boot Partition Read Select</summary>
<!-- claim:BASE3-FIG-050-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.27">06.27.</span><span class="paragraph-text">Figure 50〈Offset 44h: BPRSEL - Boot Partition Read Select〉：BPINFO 提供 active partition、大小與讀取狀態；BPRSEL 選擇要讀取的 partition、範圍；BPMBL 指向主機接收資料的記憶體。要求讀哪個 partition 與目前 active partition 是兩個不同資訊。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.12, Figure 50, 文件頁 69-70, PDF 頁 95-96</p></details>

</details>
<!-- figure-table:BASE3-FIG-051 -->
<details class="field-note" id="figure-BASE3-FIG-051"><summary>Base Figure 51 · Offset 48h: BPMBL - Boot Partition Memory Buffer Location</summary>
<!-- claim:BASE3-FIG-051-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.28">06.28.</span><span class="paragraph-text">Figure 51〈Offset 48h: BPMBL - Boot Partition Memory Buffer Location〉：BPINFO 提供 active partition、大小與讀取狀態；BPRSEL 選擇要讀取的 partition、範圍；BPMBL 指向主機接收資料的記憶體。要求讀哪個 partition 與目前 active partition 是兩個不同資訊。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.14</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 51, 文件頁 70, PDF 頁 96</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-queue-arbitration"><h3>圖表組 03 · Queue 位置與命令選取</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.29">06.29.</span><span class="paragraph-text">先用環形圖追蹤 head／tail 移動及位置釋放，再閱讀 Round Robin 或權重選擇流程。佇列位置圖與仲裁圖回答不同問題，不用其中一張推論完成順序。</span></p>
<a class="reading-link" href="#module-queue-arbitration">回到本節的解釋與範例</a>
<!-- figure-table:BASE3-FIG-073 -->
<details class="field-note" id="figure-BASE3-FIG-073"><summary>Base Figure 73 · Empty Queue Definition</summary>
<!-- claim:BASE3-FIG-073-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.30">06.30.</span><span class="paragraph-text">Figure 73〈Empty Queue Definition〉：環狀佇列用 head／tail 及各自的使用規則區分空與滿。索引回到開頭不代表所有舊資料都可覆寫；必須看對方是否已消費或釋放相應位置。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.3.1.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1.4, Figure 73, 文件頁 91, PDF 頁 117</p></details>

</details>
<!-- figure-table:BASE3-FIG-074 -->
<details class="field-note" id="figure-BASE3-FIG-074"><summary>Base Figure 74 · Full Queue Definition</summary>
<!-- claim:BASE3-FIG-074-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.31">06.31.</span><span class="paragraph-text">Figure 74〈Full Queue Definition〉：環狀佇列用 head／tail 及各自的使用規則區分空與滿。索引回到開頭不代表所有舊資料都可覆寫；必須看對方是否已消費或釋放相應位置。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.3.1.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1.4, Figure 74, 文件頁 91, PDF 頁 117</p></details>

</details>
<!-- figure-table:BASE3-FIG-080 -->
<details class="field-note" id="figure-BASE3-FIG-080"><summary>Base Figure 80 · Round Robin Arbitration</summary>
<!-- claim:BASE3-FIG-080-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.32">06.32.</span><span class="paragraph-text">Figure 80〈Round Robin Arbitration〉：Round Robin 輪流選取候選佇列，Weighted Round Robin 再考慮優先級及權重。圖中選取先後不是完成順序，因為不同命令的執行時間及相依條件可能不同。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.4.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.4.4, Figure 80, 文件頁 103, PDF 頁 129</p></details>

</details>
<!-- figure-table:BASE3-FIG-081 -->
<details class="field-note" id="figure-BASE3-FIG-081"><summary>Base Figure 81 · Weighted Round Robin with Urgent Priority Class Arbitration</summary>
<!-- claim:BASE3-FIG-081-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.33">06.33.</span><span class="paragraph-text">Figure 81〈Weighted Round Robin with Urgent Priority Class Arbitration〉：Round Robin 輪流選取候選佇列，Weighted Round Robin 再考慮優先級及權重。圖中選取先後不是完成順序，因為不同命令的執行時間及相依條件可能不同。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.4.4.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.4.4.2, Figure 81, 文件頁 104, PDF 頁 130</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-memory-capacity"><h3>圖表組 04 · Namespace、CMB、PMR 與容量</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.34">06.34.</span><span class="paragraph-text">資源關係圖先區分工作記憶體和區塊儲存容量，再沿 subsystem 到各群組及 namespace 的關係閱讀。CMB／PMR 欄位則配對位置、大小、允許用途、啟用及就緒狀態。</span></p>
<a class="reading-link" href="#module-memory-capacity">回到本節的解釋與範例</a>
<!-- figure-table:BASE3-FIG-047 -->
<details class="field-note" id="figure-BASE3-FIG-047"><summary>Base Figure 47 · Offset 38h: CMBLOC - Controller Memory Buffer Location</summary>
<!-- claim:BASE3-FIG-047-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.35">06.35.</span><span class="paragraph-text">Figure 47〈Offset 38h: CMBLOC - Controller Memory Buffer Location〉：CMBLOC 與 CMBSZ 一起決定 CMB 的位置、大小及允許用途，CMBMSC 控制其位址空間，CMBSTS 回報相關狀態。先確認用途支援，再計算位置和大小；有足夠空間不表示允許放入任意資料結構。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.9</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.9, Figure 47, 文件頁 67-68, PDF 頁 93-94</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>BAR</dt><dd>Base Address Register，PCI configuration space 中用來找出裝置 memory space 的 register。</dd></div><div><dt>BIR</dt><dd>BAR Indicator Register，指出某個記憶體結構位於哪一個 PCIe BAR。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-048 -->
<details class="field-note" id="figure-BASE3-FIG-048"><summary>Base Figure 48 · Offset 3Ch: CMBSZ - Controller Memory Buffer Size</summary>
<!-- claim:BASE3-FIG-048-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.36">06.36.</span><span class="paragraph-text">Figure 48〈Offset 3Ch: CMBSZ - Controller Memory Buffer Size〉：CMBLOC 與 CMBSZ 一起決定 CMB 的位置、大小及允許用途，CMBMSC 控制其位址空間，CMBSTS 回報相關狀態。先確認用途支援，再計算位置和大小；有足夠空間不表示允許放入任意資料結構。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.11</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.11, Figure 48, 文件頁 68-69, PDF 頁 94-95</p></details>

</details>
<!-- figure-table:BASE3-FIG-052 -->
<details class="field-note" id="figure-BASE3-FIG-052"><summary>Base Figure 52 · Offset 50h: CMBMSC - Controller Memory Buffer Memory Space Control</summary>
<!-- claim:BASE3-FIG-052-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.37">06.37.</span><span class="paragraph-text">Figure 52〈Offset 50h: CMBMSC - Controller Memory Buffer Memory Space Control〉：CMBLOC 與 CMBSZ 一起決定 CMB 的位置、大小及允許用途，CMBMSC 控制其位址空間，CMBSTS 回報相關狀態。先確認用途支援，再計算位置和大小；有足夠空間不表示允許放入任意資料結構。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.14</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 52, 文件頁 70-71, PDF 頁 96-97</p></details>

</details>
<!-- figure-table:BASE3-FIG-053 -->
<details class="field-note" id="figure-BASE3-FIG-053"><summary>Base Figure 53 · Offset 58h: CMBSTS - Controller Memory Buffer Status</summary>
<!-- claim:BASE3-FIG-053-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.38">06.38.</span><span class="paragraph-text">Figure 53〈Offset 58h: CMBSTS - Controller Memory Buffer Status〉：CMBLOC 與 CMBSZ 一起決定 CMB 的位置、大小及允許用途，CMBMSC 控制其位址空間，CMBSTS 回報相關狀態。先確認用途支援，再計算位置和大小；有足夠空間不表示允許放入任意資料結構。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.16</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.16, Figure 53, 文件頁 71, PDF 頁 97</p></details>

</details>
<!-- figure-table:BASE3-FIG-054 -->
<details class="field-note" id="figure-BASE3-FIG-054"><summary>Base Figure 54 · Offset 5Ch: CMBEBS - Controller Memory Buffer Elasticity Buffer Size</summary>
<!-- claim:BASE3-FIG-054-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.39">06.39.</span><span class="paragraph-text">Figure 54〈Offset 5Ch: CMBEBS - Controller Memory Buffer Elasticity Buffer Size〉：CMB 的彈性緩衝大小與持續寫入吞吐量是兩種資源資訊。大小欄位先配對其尺度換成 bytes，吞吐量則配對其速率尺度；不能把容量數值直接當成每秒可寫入量。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.16</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.16, Figure 54, 文件頁 71, PDF 頁 97</p></details>

</details>
<!-- figure-table:BASE3-FIG-055 -->
<details class="field-note" id="figure-BASE3-FIG-055"><summary>Base Figure 55 · Offset 60h: CMBSWTP - Controller Memory Buffer Sustained Write Throughput</summary>
<!-- claim:BASE3-FIG-055-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.40">06.40.</span><span class="paragraph-text">Figure 55〈Offset 60h: CMBSWTP - Controller Memory Buffer Sustained Write Throughput〉：CMB 的彈性緩衝大小與持續寫入吞吐量是兩種資源資訊。大小欄位先配對其尺度換成 bytes，吞吐量則配對其速率尺度；不能把容量數值直接當成每秒可寫入量。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.19</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.19, Figure 55, 文件頁 72, PDF 頁 98</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>TLP</dt><dd>Transaction Layer Packet，PCIe transaction layer 傳送的 packet。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-058 -->
<details class="field-note" id="figure-BASE3-FIG-058"><summary>Base Figure 58 · Offset E00h: PMRCAP - Persistent Memory Region Capabilities</summary>
<!-- claim:BASE3-FIG-058-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.41">06.41.</span><span class="paragraph-text">Figure 58〈Offset E00h: PMRCAP - Persistent Memory Region Capabilities〉：PMRCAP 描述 PMR 支援、位置與等待條件，PMRCTL 提出啟用要求，PMRSTS 回報就緒或錯誤。PMRMSCL／PMRMSCU 組成位址控制；位址、啟用與就緒必須分開讀取。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.21</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.21, Figure 58, 文件頁 73-74, PDF 頁 99-100</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>BIR</dt><dd>BAR Indicator Register，指出某個記憶體結構位於哪一個 PCIe BAR。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-059 -->
<details class="field-note" id="figure-BASE3-FIG-059"><summary>Base Figure 59 · Offset E04h: PMRCTL - Persistent Memory Region Control</summary>
<!-- claim:BASE3-FIG-059-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.42">06.42.</span><span class="paragraph-text">Figure 59〈Offset E04h: PMRCTL - Persistent Memory Region Control〉：PMRCAP 描述 PMR 支援、位置與等待條件，PMRCTL 提出啟用要求，PMRSTS 回報就緒或錯誤。PMRMSCL／PMRMSCU 組成位址控制；位址、啟用與就緒必須分開讀取。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.22</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.22, Figure 59, 文件頁 74, PDF 頁 100</p></details>

</details>
<!-- figure-table:BASE3-FIG-060 -->
<details class="field-note" id="figure-BASE3-FIG-060"><summary>Base Figure 60 · Offset E08h: PMRSTS - Persistent Memory Region Status</summary>
<!-- claim:BASE3-FIG-060-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.43">06.43.</span><span class="paragraph-text">Figure 60〈Offset E08h: PMRSTS - Persistent Memory Region Status〉：PMRCAP 描述 PMR 支援、位置與等待條件，PMRCTL 提出啟用要求，PMRSTS 回報就緒或錯誤。PMRMSCL／PMRMSCU 組成位址控制；位址、啟用與就緒必須分開讀取。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.23</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.23, Figure 60, 文件頁 75, PDF 頁 101</p></details>

</details>
<!-- figure-table:BASE3-FIG-061 -->
<details class="field-note" id="figure-BASE3-FIG-061"><summary>Base Figure 61 · Offset E0Ch: PMREBS - Persistent Memory Region Elasticity Buffer Size</summary>
<!-- claim:BASE3-FIG-061-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.44">06.44.</span><span class="paragraph-text">Figure 61〈Offset E0Ch: PMREBS - Persistent Memory Region Elasticity Buffer Size〉：PMR 的彈性緩衝量與持續寫入速率使用各自的數值和尺度。先將 size 與 throughput 分成不同單位，再與相應操作需求比較；兩者不是可以直接相加的容量。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.24</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.24, Figure 61, 文件頁 76, PDF 頁 102</p></details>

</details>
<!-- figure-table:BASE3-FIG-062 -->
<details class="field-note" id="figure-BASE3-FIG-062"><summary>Base Figure 62 · Offset E10h: PMRSWTP - Persistent Memory Region Sustained Write Throughput</summary>
<!-- claim:BASE3-FIG-062-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.45">06.45.</span><span class="paragraph-text">Figure 62〈Offset E10h: PMRSWTP - Persistent Memory Region Sustained Write Throughput〉：PMR 的彈性緩衝量與持續寫入速率使用各自的數值和尺度。先將 size 與 throughput 分成不同單位，再與相應操作需求比較；兩者不是可以直接相加的容量。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.24</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.24, Figure 62, 文件頁 76, PDF 頁 102</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>TLP</dt><dd>Transaction Layer Packet，PCIe transaction layer 傳送的 packet。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-063 -->
<details class="field-note" id="figure-BASE3-FIG-063"><summary>Base Figure 63 · Offset E14h: PMRMSCL - Persistent Memory Region Memory Space Control Lower</summary>
<!-- claim:BASE3-FIG-063-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.46">06.46.</span><span class="paragraph-text">Figure 63〈Offset E14h: PMRMSCL - Persistent Memory Region Memory Space Control Lower〉：PMRCAP 描述 PMR 支援、位置與等待條件，PMRCTL 提出啟用要求，PMRSTS 回報就緒或錯誤。PMRMSCL／PMRMSCU 組成位址控制；位址、啟用與就緒必須分開讀取。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.26</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.26, Figure 63, 文件頁 77, PDF 頁 103</p></details>

</details>
<!-- figure-table:BASE3-FIG-064 -->
<details class="field-note" id="figure-BASE3-FIG-064"><summary>Base Figure 64 · Offset E18h: PMRMSCU - Persistent Memory Region Memory Space Control Upper</summary>
<!-- claim:BASE3-FIG-064-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.47">06.47.</span><span class="paragraph-text">Figure 64〈Offset E18h: PMRMSCU - Persistent Memory Region Memory Space Control Upper〉：PMRCAP 描述 PMR 支援、位置與等待條件，PMRCTL 提出啟用要求，PMRSTS 回報就緒或錯誤。PMRMSCL／PMRMSCU 組成位址控制；位址、啟用與就緒必須分開讀取。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.26</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.26, Figure 64, 文件頁 77, PDF 頁 103</p></details>

</details>
<!-- figure-table:BASE3-FIG-086 -->
<details class="field-note" id="figure-BASE3-FIG-086"><summary>Base Figure 86 · Simple NVM Subsystem</summary>
<!-- claim:BASE3-FIG-086-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.48">06.48.</span><span class="paragraph-text">Figure 86〈Simple NVM Subsystem〉：容量關係圖先按 subsystem、domain、group、set 與 namespace 分層。容量欄位描述的是特定層級的總量、可用量或群組量；在比較或相減前，先確認兩個值的對象與單位相同。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.8.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.8.2, Figure 86, 文件頁 126, PDF 頁 152</p></details>

</details>
<!-- figure-table:BASE3-FIG-087 -->
<details class="field-note" id="figure-BASE3-FIG-087"><summary>Base Figure 87 · Vertically-Organized NVM Subsystem</summary>
<!-- claim:BASE3-FIG-087-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.49">06.49.</span><span class="paragraph-text">Figure 87〈Vertically-Organized NVM Subsystem〉：容量關係圖先按 subsystem、domain、group、set 與 namespace 分層。容量欄位描述的是特定層級的總量、可用量或群組量；在比較或相減前，先確認兩個值的對象與單位相同。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.8.2.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.8.2.2, Figure 87, 文件頁 127, PDF 頁 153</p></details>

</details>
<!-- figure-table:BASE3-FIG-088 -->
<details class="field-note" id="figure-BASE3-FIG-088"><summary>Base Figure 88 · Horizontally-Organized Dual NAND NVM Subsystem</summary>
<!-- claim:BASE3-FIG-088-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.50">06.50.</span><span class="paragraph-text">Figure 88〈Horizontally-Organized Dual NAND NVM Subsystem〉：容量關係圖先按 subsystem、domain、group、set 與 namespace 分層。容量欄位描述的是特定層級的總量、可用量或群組量；在比較或相減前，先確認兩個值的對象與單位相同。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.8.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.8.2.3, Figure 88, 文件頁 128, PDF 頁 154</p></details>

</details>
<!-- figure-table:BASE3-FIG-089 -->
<details class="field-note" id="figure-BASE3-FIG-089"><summary>Base Figure 89 · Capacity Information Field Usage</summary>
<!-- claim:BASE3-FIG-089-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.51">06.51.</span><span class="paragraph-text">Figure 89〈Capacity Information Field Usage〉：容量關係圖先按 subsystem、domain、group、set 與 namespace 分層。容量欄位描述的是特定層級的總量、可用量或群組量；在比較或相減前，先確認兩個值的對象與單位相同。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.8.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.8.3, Figure 89, 文件頁 129, PDF 頁 155</p></details>

</details>
<!-- figure-table:BASE3-FIG-065 -->
<details class="field-note" id="figure-BASE3-FIG-065"><summary>Base Figure 65 · NSID Types and Relationship to Namespace</summary>
<!-- claim:BASE3-FIG-065-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.52">06.52.</span><span class="paragraph-text">Figure 65〈NSID Types and Relationship to Namespace〉：NSID 的狀態要放在 namespace 與控制器的關係中理解。Namespace 可以已配置但尚未對指定控制器啟用；特殊 NSID 值還可能選擇整個集合，不能把所有非零值都當成單一有效 namespace。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.1, Figure 65, 文件頁 78-79, PDF 頁 104-105</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-066 -->
<details class="field-note" id="figure-BASE3-FIG-066"><summary>Base Figure 66 · NSID Types</summary>
<!-- claim:BASE3-FIG-066-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.53">06.53.</span><span class="paragraph-text">Figure 66〈NSID Types〉：NSID 的狀態要放在 namespace 與控制器的關係中理解。Namespace 可以已配置但尚未對指定控制器啟用；特殊 NSID 值還可能選擇整個集合，不能把所有非零值都當成單一有效 namespace。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.2.1.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.1.5, Figure 66, 文件頁 79, PDF 頁 105</p></details>

</details>
<!-- figure-table:BASE3-FIG-067 -->
<details class="field-note" id="figure-BASE3-FIG-067"><summary>Base Figure 67 · NVM Sets and Associated Namespaces</summary>
<!-- claim:BASE3-FIG-067-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.54">06.54.</span><span class="paragraph-text">Figure 67〈NVM Sets and Associated Namespaces〉：NVM Set 把相關儲存資源與 namespace 的關係分組。先找 namespace 隸屬哪個 Set，再看命令是否需要選擇 Set；多個 namespace 的數量不等於有同樣多個獨立儲存裝置。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.2.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2, Figure 67, 文件頁 81, PDF 頁 107</p></details>

</details>
<!-- figure-table:BASE3-FIG-068 -->
<details class="field-note" id="figure-BASE3-FIG-068"><summary>Base Figure 68 · NVM Set Aware Admin Commands</summary>
<!-- claim:BASE3-FIG-068-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.55">06.55.</span><span class="paragraph-text">Figure 68〈NVM Set Aware Admin Commands〉：NVM Set 把相關儲存資源與 namespace 的關係分組。先找 namespace 隸屬哪個 Set，再看命令是否需要選擇 Set；多個 namespace 的數量不等於有同樣多個獨立儲存裝置。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.2.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2, Figure 68, 文件頁 81, PDF 頁 107</p></details>

</details>
<!-- figure-table:BASE3-FIG-069 -->
<details class="field-note" id="figure-BASE3-FIG-069"><summary>Base Figure 69 · NVM Sets and Associated Namespaces</summary>
<!-- claim:BASE3-FIG-069-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.56">06.56.</span><span class="paragraph-text">Figure 69〈NVM Sets and Associated Namespaces〉：NVM Set 把相關儲存資源與 namespace 的關係分組。先找 namespace 隸屬哪個 Set，再看命令是否需要選擇 Set；多個 namespace 的數量不等於有同樣多個獨立儲存裝置。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.3, Figure 69, 文件頁 83, PDF 頁 109</p></details>

</details>
<!-- figure-table:BASE3-FIG-070 -->
<details class="field-note" id="figure-BASE3-FIG-070"><summary>Base Figure 70 · Flexible Data Placement Logical View of Non-Volatile Storage</summary>
<!-- claim:BASE3-FIG-070-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.57">06.57.</span><span class="paragraph-text">Figure 70〈Flexible Data Placement Logical View of Non-Volatile Storage〉：Reclaim Group 與資料放置的關係圖，說明儲存資源如何分組及共享。比較單一和多個群組時，追蹤同一 namespace 能使用哪些資源，不要將圖中的每個方框當成額外增加的一份總容量。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Reclaim Group</dt><dd>Reclaim Group，具有共同回收行為的一組非揮發性儲存資源。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.2.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.4, Figure 70, 文件頁 85, PDF 頁 111</p></details>

</details>
<!-- figure-table:BASE3-FIG-071 -->
<details class="field-note" id="figure-BASE3-FIG-071"><summary>Base Figure 71 · Example 1 Domain Structure</summary>
<!-- claim:BASE3-FIG-071-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.58">06.58.</span><span class="paragraph-text">Figure 71〈Example 1 Domain Structure〉：容量關係圖先按 subsystem、domain、group、set 與 namespace 分層。容量欄位描述的是特定層級的總量、可用量或群組量；在比較或相減前，先確認兩個值的對象與單位相同。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.2.5.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.5.1, Figure 71, 文件頁 86, PDF 頁 112</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-lifecycle"><h3>圖表組 05 · Shutdown、Reset 與狀態保留</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.59">06.59.</span><span class="paragraph-text">先選事件類型與範圍，再以保留表逐項看設定及資源的結果。關機狀態圖配對 SHN 的要求和 SHST 的回報；不要把重設後某個初始值當成上次關機成功的證明。</span></p>
<a class="reading-link" href="#module-lifecycle">回到本節的解釋與範例</a>
<!-- figure-table:BASE3-FIG-043 -->
<details class="field-note" id="figure-BASE3-FIG-043"><summary>Base Figure 43 · Offset 20h: NSSR - NVM Subsystem Reset</summary>
<!-- claim:BASE3-FIG-043-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.60">06.60.</span><span class="paragraph-text">Figure 43〈Offset 20h: NSSR - NVM Subsystem Reset〉：NSSR 與 NSSD 分別關係到 subsystem 重設及關機，作用範圍比單一控制器的設定更大。先確認能力及合法寫入值，再依對應操作流程解釋結果，不能把兩者都視為一般 controller disable。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NSSD</dt><dd>NVM Subsystem Shutdown，控制較大範圍 subsystem shutdown 的 property。</dd></div><div><dt>NSSR</dt><dd>NVM Subsystem Reset，觸發 NVM subsystem reset 的 property。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.4.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 43, 文件頁 66, PDF 頁 92</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NSSR</dt><dd>NVM Subsystem Reset，觸發 NVM subsystem reset 的 property。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-056 -->
<details class="field-note" id="figure-BASE3-FIG-056"><summary>Base Figure 56 · Offset 64h: NSSD - NVM Subsystem Shutdown</summary>
<!-- claim:BASE3-FIG-056-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.61">06.61.</span><span class="paragraph-text">Figure 56〈Offset 64h: NSSD - NVM Subsystem Shutdown〉：NSSR 與 NSSD 分別關係到 subsystem 重設及關機，作用範圍比單一控制器的設定更大。先確認能力及合法寫入值，再依對應操作流程解釋結果，不能把兩者都視為一般 controller disable。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NSSD</dt><dd>NVM Subsystem Shutdown，控制較大範圍 subsystem shutdown 的 property。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.4.19</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.19, Figure 56, 文件頁 72, PDF 頁 98</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CAP.CPS</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.CPS 進一步指定其中的 CPS 子欄位。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-084 -->
<details class="field-note" id="figure-BASE3-FIG-084"><summary>Base Figure 84 · Admin Commands Permitted to Return a Status Code of Admin Command Media Not</summary>
<!-- claim:BASE3-FIG-084-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.62">06.62.</span><span class="paragraph-text">Figure 84〈Admin Commands Permitted to Return a Status Code of Admin Command Media Not〉：Ready timeout 與選擇的就緒模式有關。先核對 CAP.CRMS 的支援及 CC.CRIME 的設定，再選 CRTO 中適用時間；某些 Admin 命令的媒體尚未就緒狀態另依命令清單判斷。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.5.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.5.3, Figure 84, 文件頁 110-111, PDF 頁 136-137</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CAP.CRMS.CRIMS</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.CRMS.CRIMS 進一步指定其中的 CRMS.CRIMS 子欄位。</dd></div><div><dt>CAP.CRMS.CRWMS</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.CRMS.CRWMS 進一步指定其中的 CRMS.CRWMS 子欄位。</dd></div><div><dt>CAP.CRMS</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.CRMS 進一步指定其中的 CRMS 子欄位。</dd></div><div><dt>CC.CRIME</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.CRIME 進一步指定其中的 CRIME 子欄位。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-085 -->
<details class="field-note" id="figure-BASE3-FIG-085"><summary>Base Figure 85 · Shutdown Processing Interactions</summary>
<!-- claim:BASE3-FIG-085-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.63">06.63.</span><span class="paragraph-text">Figure 85〈Shutdown Processing Interactions〉：Shutdown processing 的互動圖把主機要求與控制器處理階段分開。沿每個條件判斷可執行的動作，並以 SHST 等狀態確認進度；不能只因已寫 SHN 就判斷關機完成。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.6, Figure 85, 文件頁 113, PDF 頁 139</p></details>

</details>
<!-- figure-table:BASE3-FIG-090 -->
<details class="field-note" id="figure-BASE3-FIG-090"><summary>Base Figure 90 · Detecting Timeout Takes up to 2 * KATT</summary>
<!-- claim:BASE3-FIG-090-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.64">06.64.</span><span class="paragraph-text">Figure 90〈Detecting Timeout Takes up to 2 * KATT〉：Keep Alive 的圖以 KATT 時間間隔說明逾時判斷。不同檢查時點可使偵測延後，因此圖中的最長偵測時間不是單次命令允許的執行時間，也不表示媒體發生錯誤。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>KATT</dt><dd>Keep Alive Timeout Total，controller 用於偵測逾時的總時間基準。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.9.4.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.9.4.1, Figure 90, 文件頁 133, PDF 頁 159</p></details>

</details>
<!-- figure-table:BASE3-FIG-091 -->
<details class="field-note" id="figure-BASE3-FIG-091"><summary>Base Figure 91 · Example Privileged Action Admin Commands</summary>
<!-- claim:BASE3-FIG-091-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.65">06.65.</span><span class="paragraph-text">Figure 91〈Example Privileged Action Admin Commands〉：Privileged Action 的例子描述需要特定授權條件的管理操作。先辨認操作對象與權限要求，再看命令格式；僅有 Admin Queue 並不會自動消除這些操作要求。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.10</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.10, Figure 91, 文件頁 135, PDF 頁 161</p></details>

</details>
</div>
<!-- claim:BASE3-NAMESPACE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.66">06.66.</span><span class="paragraph-text">NSID 0h 無效，FFFFFFFFh 是 broadcast 值；其餘 NSID 還要區分 allocated／unallocated 與 active／inactive，不能只看數字是否落在範圍內。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.1, 文件頁 78-80, PDF 頁 104-106</p></details>
<!-- claim:BASE3-DOMAIN -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.67">06.67.</span><span class="paragraph-text">domain 是 NVM subsystem 內的故障／通訊邊界。多 domain subsystem 的 identifier 必須（shall）在該 subsystem 內唯一。</span></p><details class="source-note"><summary>來源：Base 2.4 §3.2.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.5, 文件頁 85-88, PDF 頁 111-114</p></details>
</section>
</details>
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
