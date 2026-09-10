---
layout: post
read_time: true
show_date: true
title: "NVMe over PCIe Transport 1.4：完整傳輸綁定"
date: 2026-08-28
description: "從主題主軸到關鍵機制、條件與例子的 NVMe 技術報告。"
lang: zh-Hant-TW
img: posts/2026/lion_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
nvme_notes: true
---
[English]({% post_url 2026-08-28-nvme-pcie-transport-1-4-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">NVMe over PCIe Transport 說明 NVMe 的佇列、properties 與通知如何透過 PCIe 運作。本篇把作業系統熟悉的記憶體映射 I/O、DMA 與中斷，接到一筆 NVMe 命令的實際傳遞過程。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express，主機與非揮發性記憶體子系統之間的介面規範家族。</dd></div><div><dt>PCIe</dt><dd>PCI Express，NVMe memory-based controller 使用的 transport 與裝置互連。</dd></div><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>介面位置</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">透過 BAR 與 configuration space 找到 NVMe 介面及能力。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>BAR</dt><dd>Base Address Register，PCI configuration space 中用來找出裝置 memory space 的 register。</dd></div></dl></article>
<article><span class="axis-number">02</span><h3>命令與通知</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">區分佇列資料、Doorbell 與 interrupt 的作用。</span></p></article>
<article><span class="axis-number">03</span><h3>平台行為</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">理解 reset、電源、錯誤回報與鏈路量測各自的適用範圍。</span></p></article>
</div>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">Base 規格定義 NVMe 的共同命令與佇列模型；PCIe Transport 補上本機 PCIe 的連接方式。讀取記憶體中的 queue entry，與存取裝置的 MMIO register，是不同種類的存取。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>MMIO</dt><dd>Memory-Mapped I/O，以 CPU memory access 形式讀寫裝置 register。</dd></div></dl>
<div class="overview-connections"><h3>把主軸連起來</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.03">00.03.</span><span class="paragraph-text">Base 定義的提交與完成機制，在 PCIe 上需要具體的位址、記憶體存取和通知方式。先找到控制器的暫存器空間，再看 SQ／CQ 如何交換命令，最後理解中斷及 PCIe 狀態回報。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CQ</dt><dd>Completion Queue，controller 放入完成結果的完成佇列。</dd></div><div><dt>SQ</dt><dd>Submission Queue，主機放入命令的提交佇列。</dd></div></dl>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.04">00.04.</span><span class="paragraph-text">Configuration Space、錯誤紀錄與眼圖量測又提供不同層次的資訊：裝置如何呈現、傳輸發生了什麼、接收端量測資料如何排列。它們不等同 NVMe 命令完成狀態。學完應能沿一次交換辨認資料、Doorbell 和中斷的分工。</span></p>
</div>
</section>
<section class="lesson" id="module-layers"><h2 id="heading-layers"><span class="section-number">01</span> NVMe 如何使用 PCIe</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">Figure 1 說明文件適用關係，Figure 2 再把 protocol responsibility 分層。工程上應把『command 語意』與『如何透過 host memory、MMIO、configuration space、interrupt 傳送』分開查證；Transport 發現衝突時不能改寫 Base。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div></dl>
<!-- claim:PCIE14-SCOPE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">PCIe Transport 補充 Base Specification，定義 PCIe 專屬資料結構、延伸、要求與行為；通用 NVMe 行為仍由 Base 定義。規格衝突時 Base 的優先序高於 Transport。</span></p><details class="source-note"><summary>來源：PCIe Transport 1.4 §1.2</summary><p>來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, 文件頁 6, PDF 頁 6</p></details>
<div class="table-wrap"><table><caption>NVMe 如何使用 PCIe</caption><thead><tr><th scope="col">規格層次</th><th scope="col">負責的行為</th><th scope="col">本篇如何使用它</th></tr></thead><tbody><tr><td>Base</td><td>command 與 completion 的共通語意</td><td>最高優先序的 NVMe 定義</td></tr><tr><td>PCIe Transport</td><td>address、register、doorbell、interrupt 綁定</td><td>補充 PCIe-specific 要求</td></tr><tr><td>PCI-SIG 規格</td><td>原生 PCIe capability/transaction 語意</td><td>本報告只引用來源明載的 NVMe-specific 部分</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">說明性範例：Firmware Commit 的 CA/FS 與 status code 在 Base 解讀；SQE 放在 host memory、doorbell 位於 BAR0/1 memory space、completion 如何觸發 MSI-X，則由 PCIe Transport 補足。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>MSI-X</dt><dd>MSI-X，提供較多 vectors、獨立遮罩與 table 的延伸 message-signaled interrupt 機制。</dd></div><div><dt>MSI</dt><dd>Message Signaled Interrupt，透過 memory write message 傳遞 interrupt 的 PCI 機制。</dd></div><div><dt>SQE</dt><dd>Submission Queue Entry，SQ 中的一筆命令資料結構。</dd></div><div><dt>CA</dt><dd>Commit Action，Firmware Commit 中選擇 replace、activate 與 reset policy 的欄位。</dd></div><div><dt>FS</dt><dd>Firmware Slot，Firmware Commit 中選擇目標 slot 的欄位。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-mmio-doorbell"><h2 id="heading-mmio-doorbell"><span class="section-number">02</span> BAR、MMIO 與 Doorbell 位址</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">NVMe controller registers 位於 BAR0/BAR1 指定的 memory space。Doorbell 從 1000h 起，queue y 的 SQ tail 與 CQ head 依 CAP.DSTRD 計算間距。Figures 3-6 要連成 address derivation，而不是四張獨立 register 表。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div><div><dt>DSTRD</dt><dd>Doorbell Stride，CAP 中決定相鄰 doorbell register 間距的欄位。</dd></div><div><dt>CAP</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。</dd></div></dl>
<!-- claim:PCIE14-MMIO -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">NVMe controller registers 位於 BAR0／BAR1 所指定的 memory space。host 必須（shall）使用 native width 或 aligned 32-bit access，不得發出 locked access；違反時行為未定義。</span></p><details class="source-note"><summary>來源：PCIe Transport 1.4 §3.1</summary><p>來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, 文件頁 9-10, PDF 頁 9-10</p></details>
<div class="table-wrap"><table><caption>BAR、MMIO 與 Doorbell 位址</caption><thead><tr><th scope="col">Doorbell 或寫入值</th><th scope="col">位址或內容如何計算</th><th scope="col">主機用它通知什麼</th></tr></thead><tbody><tr><td>SQ y tail</td><td>1000h + (2y) × (4 &lt;&lt; DSTRD)</td><td>host 公布新 SQ tail</td></tr><tr><td>CQ y head</td><td>1000h + (2y+1) × (4 &lt;&lt; DSTRD)</td><td>host 公布已消費 CQ head</td></tr><tr><td>doorbell value</td><td>queue pointer</td><td>不含 SQE/CQE 本體</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">說明性範例：DSTRD=1，stride=4&lt;&lt;1=8 bytes。queue 3 的 SQ tail offset =1000h+(6×8)=1030h；CQ head offset =1000h+(7×8)=1038h。兩者只差一個 stride。若把 DSTRD 當成 byte count，所有非零 DSTRD 的 doorbell 位址都會錯。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>offset</dt><dd>offset；從指定起點算出的位移。它回答「離起點多遠」，不等於 index。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-command"><h2 id="heading-command"><span class="section-number">03</span> Host 與 Controller 的命令交換</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">SQE、doorbell、controller fetch、CQE、interrupt 與 CQ head 不是同一個事件的不同名稱，而是 host/controller 之間逐步移交 ownership。正確順序同時決定 memory ordering 與資源何時可重用。</span></p>
<figure><figcaption><strong>一筆命令如何往返</strong></figcaption><ol class="flow-steps"><li>Host 將命令寫入 SQ（提交佇列）。</li><li>Host 更新 SQ Tail Doorbell，通知 Controller 有新命令。</li><li>Controller 取出並執行命令，將結果寫入 CQ（完成佇列）。</li><li>Host 讀取 CQE，再更新 CQ Head Doorbell，交還已讀取的位置。</li></ol><figcaption>命令與結果放在佇列；Doorbell 傳達佇列位置的更新。</figcaption></figure>

<!-- claim:PCIE14-COMMAND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span><span class="paragraph-text">command flow 是：寫 SQE、更新 SQ tail doorbell、controller 取走與執行、寫 CQE、發出 interrupt（若啟用）、host 處理 CQE、更新 CQ head doorbell。doorbell 只通告 pointer，不攜帶 command 本體。</span></p><details class="source-note"><summary>來源：PCIe Transport 1.4 §3.4</summary><p>來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, 文件頁 12-13, PDF 頁 12-13</p></details>
<div class="table-wrap"><table><caption>Host 與 Controller 的命令交換</caption><thead><tr><th scope="col">需要重用的資源</th><th scope="col">何時不再由原操作使用</th><th scope="col">主機應觀察的資訊</th></tr></thead><tbody><tr><td>SQ slot reuse</td><td>controller 已消費該 SQE</td><td>由完成資訊的 SQHD 協助追蹤</td></tr><tr><td>command buffer reuse</td><td>command 已 completion 且資料可見</td><td>依 command/data direction 核對</td></tr><tr><td>CQ slot release</td><td>host 已完整消費 CQE</td><td>之後才寫 CQ head doorbell</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.03">03.03.</span><span class="paragraph-text">說明性範例：host 先寫 doorbell、後補 SQE 的最後一個 dword，controller 可能 fetch 到半成品。另一個方向，host 在讀完 CQE 前先更新 CQ head，controller 可能重用該 CQ slot。兩者都是 ownership 順序錯誤，不是 command opcode 問題。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Dword</dt><dd>Dword（Double word）；32 bits，也就是 4 bytes。對比 word=16 bits；例如 zero-based dword count=3 代表 4 個 Dwords，也就是 16 bytes。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-interrupts"><h2 id="heading-interrupts"><span class="section-number">04</span> Interrupt 模式與通知行為</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">pin-based、single-message MSI、multiple-message MSI 與 MSI-X 的差異不只效能。它們提供的 vector 數、masking 位置與 capability structure 不同；interrupt coalescing 另外決定多個 completion 何時合併通知。Figure 9 與 Figures 34-46 應配合 queue-to-vector mapping 閱讀。</span></p>
<!-- claim:PCIE14-INTERRUPT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">可用模式為 pin-based、single-message MSI、multiple-message MSI 與 MSI-X。規格建議 MSI-X；coalescing 可降低 interrupt rate，但通常增加 latency。Admin CQ 的 interrupt 不宜（should not）延遲。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div></dl><details class="source-note"><summary>來源：PCIe Transport 1.4 §3.5</summary><p>來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, 文件頁 13-16, PDF 頁 13-16</p></details>
<div class="table-wrap"><table><caption>Interrupt 模式與通知行為</caption><thead><tr><th scope="col">中斷方式</th><th scope="col">通知與遮罩如何安排</th><th scope="col">影響的資源或限制</th></tr></thead><tbody><tr><td>pin-based</td><td>傳統共享線路</td><td>共享與 masking 行為不同</td></tr><tr><td>single MSI</td><td>單一 message/vector</td><td>多個 CQ 可能共享服務路徑</td></tr><tr><td>multiple MSI</td><td>一組連續 messages</td><td>受 MME/MMC 等能力限制</td></tr><tr><td>MSI-X</td><td>table-based 多 vectors、獨立 mask</td><td>規格建議優先使用</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.03">04.03.</span><span class="paragraph-text">說明性範例：CQ 1 與 CQ 2 共用 vector 5。收到 vector 5 時，handler 不能只檢查 CQ 1；它必須處理所有映射到該 vector 的相關 CQs。提高 coalescing threshold 可減少 interrupts，但可能增加 CQE 等待時間。</span></p></aside>
</section>
<section class="lesson" id="module-config-error"><h2 id="heading-config-error"><span class="section-number">05</span> Configuration Space 與 PCIe 錯誤回報</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span><span class="paragraph-text">Figures 10-67 從 Type 0 header 走到 Power Management、MSI/MSI-X、PCIe capability 與 AER。閱讀順序應先找 capability pointer／extended capability，再以該 capability base 加 offset；AER status/mask/severity/header log 應視為一組，不可只截取單一 error bit。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>AER</dt><dd>Advanced Error Reporting，PCIe 用來分類、遮罩與記錄 link／transaction error 的 capability。</dd></div></dl>
<!-- claim:PCIE14-CONFIG -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.02">05.02.</span><span class="paragraph-text">§3.8 逐欄定義 NVMe controller 的 PCI header、Power Management、MSI／MSI-X、PCIe capability 與 AER 額外要求。PCI／PCIe 原始欄位語意仍以 PCI-SIG 規格為準。</span></p><details class="source-note"><summary>來源：PCIe Transport 1.4 §3.8.1-3.8.7</summary><p>來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, 文件頁 16-35, PDF 頁 16-35</p></details>
<div class="table-wrap"><table><caption>Configuration Space 與 PCIe 錯誤回報</caption><thead><tr><th scope="col">回報層次或能力</th><th scope="col">描述的事件或資源</th><th scope="col">必須連同哪些資訊閱讀</th></tr></thead><tbody><tr><td>NVMe CQE status</td><td>command 執行結果</td><td>由 NVMe command context 解</td></tr><tr><td>PCIe Device Status</td><td>PCIe Function 狀態摘要</td><td>位於 PCIe capability</td></tr><tr><td>AER</td><td>correctable/uncorrectable transport errors</td><td>status、mask、severity、header 一起看</td></tr><tr><td>power state</td><td>slot limit 與 device power 控制</td><td>不得選超過 slot power limit 的 NVMe state</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="05.03">05.03.</span><span class="paragraph-text">說明性範例：AERUCES 某 bit 被設為 1，先查對應 mask 判斷是否會回報，再查 severity 判斷錯誤嚴重程度及其處置，最後用 header log 取得 transaction context。不能把該 bit 直接翻成某個 NVMe SC。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>SC</dt><dd>Status Code；指定所選 SCT 類別中的完成結果。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-eom"><h2 id="heading-eom"><span class="section-number">06</span> 接收端眼圖量測資料的結構</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.01">06.01.</span><span class="paragraph-text">接收端眼圖量測 log 是變長結構。Header 描述整體資料，lane descriptors 描述各 lane；將結構層級與長度單位分開，才能理解每筆量測屬於哪條 lane。</span></p>
<!-- claim:PCIE14-EOM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.02">06.02.</span><span class="paragraph-text">Physical Interface Receiver Eye Opening Measurement log page 以 header、lane descriptor 與 EOM data 回報量測；host 先查支援與大小，再依 lane／parameter 解析。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>EOM</dt><dd>Eye Opening Measurement，量測 PCIe receiver eye opening 的程序與 log data。</dd></div></dl><details class="source-note"><summary>來源：PCIe Transport 1.4 §3.9</summary><p>來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, 文件頁 39-46, PDF 頁 39-46</p></details>
<div class="table-wrap"><table><caption>接收端眼圖量測資料的結構</caption><thead><tr><th scope="col">量測資料區域</th><th scope="col">描述的量測與位置</th><th scope="col">比較前須先確認什麼</th></tr></thead><tbody><tr><td>specific parameter</td><td>選量測動作與品質/狀態</td><td>先決定 request context</td></tr><tr><td>specific identifier</td><td>選 lane/test context</td><td>避免把不同量測混在一起</td></tr><tr><td>header</td><td>全域長度與配置</td><td>所有後續 offset 的基準</td></tr><tr><td>lane descriptor</td><td>每 lane 邊界/狀態</td><td>只在 buffer 內走訪</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="06.03">06.03.</span><span class="paragraph-text">若需要比較 2 條 lanes，先以各自的 lane descriptor 找到量測資料，再依相同的 measurement 格式比較。Header 的 lane 數量用來描述結構，不能直接當成量測品質的指標。</span></p></aside>
</section>
<section id="spec-reading"><h2>接著打開 Spec 看什麼</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.01">07.01.</span><span class="paragraph-text">以下按概念列出閱讀位置。報告時先用上面的流程說明問題，再打開對應章節看欄位與完整條件。中文教學 HTML 另有本篇全部圖表的逐圖重點、案例與細節。</span></p>
<div class="table-wrap"><table><thead><tr><th scope="col">要說明的觀念</th><th scope="col">Spec 閱讀位置</th></tr></thead><tbody><tr><td>NVMe 如何使用 PCIe</td><td>PCIe Transport 1.4 §1.2 · PCIe Transport 1.4 §1.3 · PCIe Transport 1.4 §2</td></tr><tr><td>BAR、MMIO 與 Doorbell 位址</td><td>PCIe Transport 1.4 §3.1 · PCIe Transport 1.4 §3.1.2.1-3.1.2.2</td></tr><tr><td>Host 與 Controller 的命令交換</td><td>PCIe Transport 1.4 §3.4 · PCIe Transport 1.4 §3.2</td></tr><tr><td>Interrupt 模式與通知行為</td><td>PCIe Transport 1.4 §3.5 · PCIe Transport 1.4 §3.2 · PCIe Transport 1.4 §Annex A</td></tr><tr><td>Configuration Space 與 PCIe 錯誤回報</td><td>PCIe Transport 1.4 §3.8.1-3.8.7 · PCIe Transport 1.4 §3.7 · PCIe Transport 1.4 §3.6</td></tr><tr><td>接收端眼圖量測資料的結構</td><td>PCIe Transport 1.4 §3.9 · PCIe Transport 1.4 §Annex A</td></tr></tbody></table></div>
<a class="reading-link" href="/DOCS/nvme-spec-report/pcie-transport-1.4/tutorial-zh-tw.html">開啟完整中文教學與逐圖解釋 →</a></section>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:pcie-transport-1.4-memory-mmio -->
<details class="review-question" id="qa-pcie-transport-1.4-memory-mmio"><summary>1. PCIe MMIO properties 和 host memory 中的 queues 分別扮演什麼角色？</summary>
<div data-qa-answer="pcie-transport-1.4-memory-mmio"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="08.01">08.01.</span><span class="paragraph-text">Properties 提供 controller 設定、狀態與 queue 通知介面；queues 承載命令和完成項目。將控制介面與資料結構分開，才能理解一次提交如何運作。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, 文件頁 9-10, PDF 頁 9-10</p>
<p>來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, 文件頁 11, PDF 頁 11</p>
</details></details>
<!-- qa:pcie-transport-1.4-doorbell-stride -->
<details class="review-question" id="qa-pcie-transport-1.4-doorbell-stride"><summary>2. 為何不能假設所有 controller 的相鄰 doorbells 都相距 4 bytes？</summary>
<div data-qa-answer="pcie-transport-1.4-doorbell-stride"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="08.02">08.02.</span><span class="paragraph-text">Doorbell spacing 由 CAP.DSTRD 決定，stride 是 2^(2+DSTRD) bytes。只有 DSTRD=0 時才是 4 bytes；SQ Tail 與 CQ Head 的位置還需搭配 queue ID 計算。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, 文件頁 10-11, PDF 頁 10-11</p>
</details></details>
<!-- qa:pcie-transport-1.4-interrupt -->
<details class="review-question" id="qa-pcie-transport-1.4-interrupt"><summary>3. 收到 interrupt 後，為何仍需讀取 CQ？</summary>
<div data-qa-answer="pcie-transport-1.4-interrupt"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="08.03">08.03.</span><span class="paragraph-text">Interrupt 是通知，CQE 才包含命令識別與完成狀態。一個通知不必等於一個完成項目；host 應依 queue 的有效項目與進度處理完成。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, 文件頁 13-16, PDF 頁 13-16</p>
<p>來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, 文件頁 12-13, PDF 頁 12-13</p>
</details></details>
<!-- qa:pcie-transport-1.4-error-layer -->
<details class="review-question" id="qa-pcie-transport-1.4-error-layer"><summary>4. NVMe 命令的 status 與 PCIe 錯誤回報，為何需要分開看？</summary>
<div data-qa-answer="pcie-transport-1.4-error-layer"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="08.04">08.04.</span><span class="paragraph-text">前者描述命令處理結果，後者描述傳輸與裝置層的錯誤資訊。兩者可能相關，但解釋的對象不同，不能把某一層的成功當成所有層都沒有問題。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, 文件頁 16, PDF 頁 16</p>
<p>來源：NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, 文件頁 16-35, PDF 頁 16-35</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express NVMe over PCIe Transport Specification, Revision 1.4</p><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
