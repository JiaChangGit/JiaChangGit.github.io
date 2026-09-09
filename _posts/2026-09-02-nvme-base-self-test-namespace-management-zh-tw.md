---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4：Device Self-test 與 Namespace Management"
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
[English]({% post_url 2026-09-02-nvme-base-self-test-namespace-management-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">Device Self-test 用來理解裝置測試的結果；Namespace Management 用來建立與管理主機可存取的儲存空間。本篇把測試結果、容量與格式選擇，以及 namespace 的建立、附加、刪除和還原分開說清楚。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div></dl>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>測試與結果</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">分清命令完成、測試完成與有效的結果欄位。</span></p></article>
<article><span class="axis-number">02</span><h3>容量與格式</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">理解容量單位、配置粒度及 LBA 格式選擇。</span></p></article>
<article><span class="axis-number">03</span><h3>Namespace 生命週期</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">把建立、附加、刪除與還原視為不同的狀態改變。</span></p></article>
</div>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">Namespace 是控制器呈現給主機的邏輯儲存空間，以 NSID 識別。建立 namespace 與把它附加至 controller 是兩個步驟，不能由其中一步推論另一步已完成。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div></dl>
<div class="overview-connections"><h3>把主軸連起來</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.03">00.03.</span><span class="paragraph-text">診斷裝置與配置儲存空間是不同工作。前者啟動背景測試並讀取結果，後者先決定容量與格式，再建立 namespace 和控制器的存取關係。兩者都需要把命令完成與後續狀態分開閱讀。</span></p>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.04">00.04.</span><span class="paragraph-text">Namespace 的主線是容量→建立資料→Create→Attach→存取→Detach／Delete，恢復預設配置與通知則接在這條主線上理解。學完應能分清空間是否存在、是否已連接到特定控制器，以及容量是否符合所選格式與粒度。</span></p>
</div>
</section>
<section class="lesson" id="module-diagnostic-and-provisioning"><h2 id="heading-diagnostic-and-provisioning"><span class="section-number">01</span> 裝置診斷與 Namespace 配置</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">Device Self-test 與 Namespace Management 都使用 Admin command，但它們改變的物件完全不同。Self-test 建立一個背景 operation，command CQE 只是接受點，最後要靠 LID 06h 證明結果；Namespace Management 建立或移除 namespace object，Create CQE 回傳 NSID，但還要 Attach 才建立 controller access。先分開兩條線，才能理解 completion 為何不是終點。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div><div><dt>LID 06h</dt><dd>Device Self-test Log Page 的 identifier 06h；同時包含 current operation 與 20 筆歷史結果。</dd></div><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div><div><dt>LID</dt><dd>Log Page Identifier；指定要讀取哪一種 log page 的編號。</dd></div></dl>
<details class="technical-note"><summary>完整規則：裝置診斷與 Namespace 配置</summary>
<!-- claim:BASENSMGMT-SELFTEST-COMPLETION -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">Device Self-test 的 Admin CQE 只證明啟動或中止動作已被處理，不代表背景測試完成。software 必須把 command CQE、LID 06h current state 與最後 result entry 當成三個不同時間點。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>LID 06h</dt><dd>Device Self-test Log Page 的 identifier 06h；同時包含 current operation 與 20 筆歷史結果。</dd></div><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div><div><dt>LID</dt><dd>Log Page Identifier；指定要讀取哪一種 log page 的編號。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 201, PDF 頁 227</p></details>
<!-- claim:BASENSMGMT-NSID-LIFECYCLE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">create 成功後 namespace 已 allocated 但尚未 attached，因此對 controller 尚非 active。detach 使該 controller 上的 NSID 變 inactive；delete 使 subsystem 中的 NSID 變 unallocated。受影響的 outstanding 或後續 commands 依 in目前可存取的 NSID 處理。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.17</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686</p></details>
<!-- claim:BASENSMGMT-CREATE-COMPLETION -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.04">01.04.</span><span class="paragraph-text">Create 成功時 controller 選擇可用 NSID，CQE.DW0 回傳該 NSID；此刻 namespace 尚未 attached。software 必須先保存 returned NSID，再以 Namespace Attachment 建立 controller access，不能在 create CQE 後直接送 I/O。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.25, 8.1.17.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446-448, 662, PDF 頁 472-474, 688</p></details>
</details>
<div class="table-wrap"><table><caption>裝置診斷與 Namespace 配置</caption><thead><tr><th scope="col">管理對象</th><th scope="col">主機要建立或觀察什麼</th><th scope="col">用哪個結果接續操作</th></tr></thead><tbody><tr><td>Self-test object</td><td>background operation</td><td>CQE→current state→history result</td></tr><tr><td>Namespace object</td><td>allocated capacity + format</td><td>Create CQE.DW0→NSID</td></tr><tr><td>Access relationship</td><td>namespace↔controller attachment</td><td>Attach CQE→Active NSID list</td></tr><tr><td>Inventory evidence</td><td>Allocated／Active lists</td><td>AEN 後重新 Identify</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>AEN</dt><dd>Asynchronous Event Notification，controller 透過已提交 Asynchronous Event Request 回報事件的通知。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.05">01.05.</span><span class="paragraph-text">Create 成功回 NSID=7 只證明 namespace 7 已建立；它仍未 attached，不能立刻做 I/O。相反地，Self-test 啟動成功的 CQE 也只證明 operation 已開始，不能把它記成 test passed。兩種 CQE 都要再接下一個證據，但下一個證據不同。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl></aside>
<a class="reading-link" href="#reading-diagnostic-and-provisioning">閱讀相關規格圖表 → 裝置診斷與 Namespace 配置</a>
</section>
<section class="lesson" id="module-selftest-command-state-machine"><h2 id="heading-selftest-command-state-machine"><span class="section-number">02</span> Device Self-test 的執行與結果</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">先用 OACS.DSTS、EDSTT 與 DSTO.SDSO 建立支援、時間與 concurrency 預期，再以 NSID 與 STC 建構 command。CQE 到達後輪詢 DSTOS／DSTCS；operation 結束時，先建立 RDS1，再把 current status 清零。這個先後順序讓 software 不會在短暫視窗遺失最後結果。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>OACS.DSTS</dt><dd>Optional Admin Command Support 的 Device Self-test Supported bit，判斷 command 是否可用。</dd></div><div><dt>DSTCS</dt><dd>Device Self-test Completion Status，LID 06h 中的 0 到 100 完成百分比。</dd></div><div><dt>DSTOS</dt><dd>Device Self-test Operation Status，LID 06h 中表示目前 operation 類型的 nibble。</dd></div><div><dt>EDSTT</dt><dd>Extended Device Self-test Time，在 power state 0 下的 extended test 名目完成分鐘數。</dd></div><div><dt>DSTO</dt><dd>Device Self-test Options，Identify Controller 中回報 refresh 與 concurrency 選項的欄位。</dd></div><div><dt>SDSO</dt><dd>Single Device Self-test Operation，選擇 subsystem-wide 單一 operation 或 per-controller operation 的 bit。</dd></div><div><dt>STC</dt><dd>Self-test Code 是 Device Self-test CDW10 的動作 nibble；result entry 的 STC 則是 Status Code，須依 SCVLD 判斷有效。</dd></div></dl>
<details class="technical-note"><summary>完整規則：Device Self-test 的執行與結果</summary>
<!-- claim:BASENSMGMT-SELFTEST-GATE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">啟動 Device Self-test 前先讀 Identify Controller：OACS.DSTS 判斷 command 是否支援；EDSTT 是 extended operation 在 power state 0 的名目分鐘數；DSTO.SDSO 決定同時只有一個 subsystem-wide operation，或每個 controller 各一個。三者分別是支援、時間與 concurrency scope。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>OACS.DSTS</dt><dd>Optional Admin Command Support 的 Device Self-test Supported bit，判斷 command 是否可用。</dd></div><div><dt>EDSTT</dt><dd>Extended Device Self-test Time，在 power state 0 下的 extended test 名目完成分鐘數。</dd></div><div><dt>DSTO</dt><dd>Device Self-test Options，Identify Controller 中回報 refresh 與 concurrency 選項的欄位。</dd></div><div><dt>SDSO</dt><dd>Single Device Self-test Operation，選擇 subsystem-wide 單一 operation 或 per-controller operation 的 bit。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.14.2.1, 8.1.8</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, 文件頁 353-358, 614, PDF 頁 379-384, 640</p></details>
<!-- claim:BASENSMGMT-SELFTEST-NSID -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">Device Self-test 由收到 command 的 controller 執行。NSID=00000000h 只測 controller；00000001h～FFFFFFFEh 指定一個 active namespace；FFFFFFFFh 包含提交當下該 controller 可存取的所有 attached namespaces。invalid 與 in目前可存取的 NSID 是不同錯誤。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 199, PDF 頁 225</p></details>
<!-- claim:BASENSMGMT-SELFTEST-STC -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.04">02.04.</span><span class="paragraph-text">CDW10.STC[3:0] 選動作：1h=short、2h=extended、3h=Host-Initiated Refresh、Eh=vendor specific、Fh=abort；其餘 encoding reserved。只有 STC=Eh 時 CDW15.DSTP 才是 vendor specific，其他 STC 下 CDW15 reserved。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>DSTP</dt><dd>Device Self-test Parameter，只有 vendor-specific STC=Eh 時才有 vendor-defined 語意的 CDW15。</dd></div><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div><div><dt>STC</dt><dd>Self-test Code 是 Device Self-test CDW10 的動作 nibble；result entry 的 STC 則是 Status Code，須依 SCVLD 判斷有效。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 199-200, PDF 頁 225-226</p></details>
<!-- claim:BASENSMGMT-SELFTEST-CURRENT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.05">02.05.</span><span class="paragraph-text">LID 06h byte 0 的 DSTOS 表示目前 operation，byte 1 的 DSTCS[6:0] 是完成百分比；DSTOS=0 時 host 應忽略 DSTCS。operation 完成或中止時，controller 必須先建立 result entry，再把 in-progress status 清為 0。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>DSTCS</dt><dd>Device Self-test Completion Status，LID 06h 中的 0 到 100 完成百分比。</dd></div><div><dt>DSTOS</dt><dd>Device Self-test Operation Status，LID 06h 中表示目前 operation 類型的 nibble。</dd></div><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-230, PDF 頁 255-256</p></details>
<!-- claim:BASENSMGMT-SELFTEST-HISTORY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.06">02.06.</span><span class="paragraph-text">LID 06h 保留 20 筆、每筆 28 bytes 的結果，RDS1 是最新一筆。DSTS 高 nibble DSTC 記原始 self-test code，低 nibble DSTR 記完成或中止原因；只有 DSTR=7h 時 SEGN 才可解讀。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>DSTR</dt><dd>Device Self-test Result，結果 entry 中表示成功、abort 或 segment failure 的 nibble。</dd></div><div><dt>SEGN</dt><dd>Segment Number，只有 DSTR=7h 時指出第一個失敗 diagnostic segment。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-232, PDF 頁 255-258</p></details>
<!-- claim:BASENSMGMT-SELFTEST-VALIDITY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.07">02.07.</span><span class="paragraph-text">VDINFO 的 NSIDVLD、FVLD、SCTVLD、SCVLD 是四個獨立 有效性判斷。NSID、FLBA、STCT、STC 只有在對應 bit=1 時才可讀；parser 不得以欄位非零猜測有效。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>VDINFO</dt><dd>Valid Diagnostic Information，分別 gate NSID、FLBA、SCT 與 SC 的 validity bitmap。</dd></div><div><dt>parser</dt><dd>資料解析器；依資料結構的長度、欄位與適用條件讀取輸入。</dd></div><div><dt>FLBA</dt><dd>Failing LBA，NVM Command Set 定義為造成 self-test failure 的其中一個 logical block address。</dd></div><div><dt>FVLD</dt><dd>Failing LBA Valid，決定 FLBA 欄位是否可解讀的 validity bit。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 231-232, PDF 頁 257-258</p></details>
<!-- claim:BASENSMGMT-SELFTEST-NVM-FLBA -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.08">02.08.</span><span class="paragraph-text">NVM Command Set 1.3 將 result bytes 23:16 定義為造成失敗的 logical block address。若多個 logical blocks 失敗，只回其中一個，而且僅在 FVLD=1 時有效。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>logical block</dt><dd>邏輯區塊；namespace 可定址的基本單位，其資料大小由使用中的格式決定。</dd></div><div><dt>FVLD</dt><dd>Failing LBA Valid，決定 FLBA 欄位是否可解讀的 validity bit。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.4.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, 文件頁 76, PDF 頁 76</p></details>
</details>
<div class="table-wrap"><table><caption>Device Self-test 的執行與結果</caption><thead><tr><th scope="col">測試對象或控制值</th><th scope="col">涵蓋的範圍或動作</th><th scope="col">執行與結果的規則</th></tr></thead><tbody><tr><td>NSID=0</td><td>只測試控制器</td><td>不包含 namespace media</td></tr><tr><td>目前可存取的 NSID</td><td>單一 namespace</td><td>invalid／inactive status 分開</td></tr><tr><td>NSID=FFFFFFFFh</td><td>開始時可存取的 attached set</td><td>集合不是動態追蹤</td></tr><tr><td>STC=Fh</td><td>abort current operation</td><td>先寫 result 再清 current</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.09">02.09.</span><span class="paragraph-text">讀完整 LID 06h：564÷4=141 dwords，NUMD=141−1=140=008Ch。RAE=0、LSP=0、LID=06h，因此 CDW10=008C0006h。若 RDS1.DSTS=17h，DSTC=1h 是 short、DSTR=7h 才允許讀 SEGN。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>DSTR</dt><dd>Device Self-test Result，結果 entry 中表示成功、abort 或 segment failure 的 nibble。</dd></div><div><dt>NUMD</dt><dd>Number of Dwords，0's-based transfer dword count；實際 bytes = (NUMD + 1) × 4。</dd></div><div><dt>SEGN</dt><dd>Segment Number，只有 DSTR=7h 時指出第一個失敗 diagnostic segment。</dd></div><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div><div><dt>LSP</dt><dd>Log Specific Field，意義由所選 log page 定義的 command selector。</dd></div><div><dt>RAE</dt><dd>Retain Asynchronous Event，Get Log Page 是否保留相關 asynchronous event 的 selector。</dd></div></dl></aside>
<a class="reading-link" href="#reading-selftest-command-state-machine">閱讀相關規格圖表 → Device Self-test 的執行與結果</a>
</section>
<section class="lesson" id="module-capacity-granularity-math"><h2 id="heading-capacity-granularity-math"><span class="section-number">03</span> 容量數值與配置粒度</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">先分清各種容量數值的單位，再比較必要的容量關係與建議配置粒度。前者決定是否符合規格要求，後者用來減少配置空間的浪費。</span></p>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 260" role="img"><title>可定址、可配置、已配置是 3 個不同的量</title><desc>教學例：NSZE=1000、NCAP=800、NUSE=600。LBA 編號的範圍與目前配置量要分開理解。</desc><rect x="20" y="20" width="720" height="70" rx="6" class="v-object"/><text x="380.0" y="48.5" text-anchor="middle" font-size="17">NSZE = 1000</text><text x="380.0" y="73.5" text-anchor="middle" font-size="17">LBA 0 … 999</text><rect x="20" y="110" width="576" height="55" rx="6" class="v-command"/><text x="308.0" y="143.5" text-anchor="middle" font-size="17">NCAP = 800</text><rect x="20" y="185" width="432" height="55" rx="6" class="v-success"/><text x="236.0" y="218.5" text-anchor="middle" font-size="17">NUSE = 600</text></svg></div><figcaption>教學例：NSZE=1000、NCAP=800、NUSE=600。LBA 編號的範圍與目前配置量要分開理解。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>NCAP</dt><dd>Namespace Capacity，任一時點最多可配置給 namespace 的 logical blocks。</dd></div><div><dt>NSZE</dt><dd>Namespace Size，namespace 的總 logical block 數，LBA 範圍為 0 到 NSZE−1。</dd></div><div><dt>NUSE</dt><dd>Namespace Utilization，目前已配置給 namespace 的 logical blocks。</dd></div></dl>
<details class="technical-note"><summary>完整規則：容量數值與配置粒度</summary>
<!-- claim:BASENSMGMT-CAPACITY-MODEL -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span><span class="paragraph-text">Namespace Size（NSZE）是 LBA 0 到 n−1 的總 logical blocks；Namespace Capacity（NCAP）是任一時點最多可配置的 blocks；Namespace Utilization（NUSE）是目前已配置 blocks。永遠遵守 NSZE ≥ NCAP ≥ NUSE。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NCAP</dt><dd>Namespace Capacity，任一時點最多可配置給 namespace 的 logical blocks。</dd></div><div><dt>NSZE</dt><dd>Namespace Size，namespace 的總 logical block 數，LBA 範圍為 0 到 NSZE−1。</dd></div><div><dt>NUSE</dt><dd>Namespace Utilization，目前已配置給 namespace 的 logical blocks。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.1.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, 文件頁 13-14, PDF 頁 13-14</p></details>
<!-- claim:BASENSMGMT-THIN-PROVISIONING -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.03">03.03.</span><span class="paragraph-text">NSFEAT.THINP=1 時，controller 可（may）回報 NCAP&lt;NSZE，並必須（shall）追蹤 NUSE。THINP=0 時，controller 必須回報 NCAP=NSZE，且可讓 NUSE 永遠等於 NCAP。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>THINP</dt><dd>Thin Provisioning，NSFEAT 中決定 NCAP 是否可小於 NSZE，以及 controller 是否必須追蹤 NUSE 的 bit。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.1.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, 文件頁 13, PDF 頁 13</p></details>
<!-- claim:BASENSMGMT-ALLOCATION-ROUNDING -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.04">03.04.</span><span class="paragraph-text">controller 可（may）按內部 內部配置單位 把實際消耗容量向上取整。Spec 範例中，32 blocks×4 KiB=128 KiB 的 namespace，在 1 MiB 內部配置單位 下可消耗 1 MiB；因此 實際消耗容量 不一定等於 logical block size×block count。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>logical block</dt><dd>邏輯區塊；namespace 可定址的基本單位，其資料大小由使用中的格式決定。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.17</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 661, PDF 頁 687</p></details>
<!-- claim:BASENSMGMT-GRANULARITY-HINTS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.05">03.05.</span><span class="paragraph-text">Namespace Granularity 的 NSG 與 NCG 都是 以 bytes 為單位的配置粒度建議。若 NSZE×LBA size 可整除 NSG、NCAP×LBA size 可整除 NCG 且 NSZE=NCAP，配置為 完整配置 且全部容量可由 LBA 定址；不符合 hint 可能浪費容量，但 符合其他所有要求的建立命令 不得只因違反 hint 被中止。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NCG</dt><dd>Namespace Capacity Granularity，以 bytes 表示 controller 偏好的 NCAP allocation granularity。</dd></div><div><dt>NSG</dt><dd>Namespace Size Granularity，以 bytes 表示 controller 偏好的 NSZE allocation granularity。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.8, 文件頁 165, PDF 頁 165</p></details>
<!-- claim:BASENSMGMT-GRANULARITY-EXAMPLE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.06">03.06.</span><span class="paragraph-text">說明性範例：LBA=4 KiB、NSG=1 MiB（256 LBAs）、NCG=2 MiB（512 LBAs）。NSZE=NCAP=1024 同時滿足兩種 granularity；NSZE=1000、NCAP=1000 不滿足 NSG／NCG 整除，但若其他欄位都合法，controller 不得只因這個 hint violation 中止 create。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NCG</dt><dd>Namespace Capacity Granularity，以 bytes 表示 controller 偏好的 NCAP allocation granularity。</dd></div><div><dt>NSG</dt><dd>Namespace Size Granularity，以 bytes 表示 controller 偏好的 NSZE allocation granularity。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.8, 文件頁 165, PDF 頁 165</p></details>
</details>
<div class="table-wrap"><table><caption>容量數值與配置粒度</caption><thead><tr><th scope="col">容量欄位</th><th scope="col">使用的單位</th><th scope="col">這個數值描述什麼</th></tr></thead><tbody><tr><td>NSZE</td><td>logical blocks</td><td>LBA 0..NSZE−1</td></tr><tr><td>NCAP</td><td>logical blocks</td><td>最大可配置容量</td></tr><tr><td>NUSE</td><td>logical blocks</td><td>THINP=1 時需追蹤</td></tr><tr><td>NSG／NCG</td><td>bytes</td><td>建議配置粒度；未符合這項建議，不能單獨成為拒絕命令的理由</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>THINP</dt><dd>Thin Provisioning，NSFEAT 中決定 NCAP 是否可小於 NSZE，以及 controller 是否必須追蹤 NUSE 的 bit。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.07">03.07.</span><span class="paragraph-text">每個區塊 4 KiB、NSG=1 MiB、NCG=2 MiB。NSZE=NCAP=1024 時，1024×4 KiB=4 MiB，是兩種粒度的整數倍。改成 1000 時，1000×4 KiB=4000 KiB=3.90625 MiB，不是 1 MiB 或 2 MiB 的整數倍；可能浪費部分配置容量。但只要其他要求符合，不能只因未符合粒度建議而中止建立命令。</span></p></aside>
<a class="reading-link" href="#reading-capacity-granularity-math">閱讀相關規格圖表 → 容量數值與配置粒度</a>
</section>
<section class="lesson" id="module-namespace-create-payload"><h2 id="heading-namespace-create-payload"><span class="section-number">04</span> 建立 Namespace 所需的資料</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">Base Figure 448 定義 4096-byte envelope，NVM Command Set Figure 134 只定義前 768 bytes 中的 NVM 欄位與 Placement Handle List。Host 先以 SEL／CSI 決定 operation 與 command set，再填 NSZE、NCAP、format、protection、sharing 與 group IDs。Reserved areas 要清零，Protection Information 與 FDP 又各有獨立 功能支援條件。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Protection Information</dt><dd>資料保護資訊，縮寫 PI；包含 Guard 與 tags，用來檢查資料及其關聯資訊。</dd></div><div><dt>CSI</dt><dd>I/O Command Set Identifier；選擇 I/O 命令集，NVM Command Set 使用 00h。</dd></div><div><dt>FDP</dt><dd>Flexible Data Placement，把資料放置提示與媒體回收管理連結的能力。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div><div><dt>SEL</dt><dd>Select；Namespace Management 的 create/delete/restore selector，與 Get Features 的 SEL 不同。</dd></div></dl>
<details class="technical-note"><summary>完整規則：建立 Namespace 所需的資料</summary>
<!-- claim:BASENSMGMT-CREATE-BASE-COMMAND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">Create 使用 NSID=0、SEL=0h 與 CSI=00h（NVM Command Set）。DPTR 指向 4096-byte data structure：bytes 0:511 是 I/O Command Set specific、512:1023 reserved、1024:4095 vendor specific。reserved bytes 由 host 清為 0。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>DPTR</dt><dd>Data Pointer，SQE 中指出 command data buffer 的欄位。</dd></div><div><dt>CSI</dt><dd>I/O Command Set Identifier；選擇 I/O 命令集，NVM Command Set 使用 00h。</dd></div><div><dt>SEL</dt><dd>Select；Namespace Management 的 create/delete/restore selector，與 Get Features 的 SEL 不同。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.25</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 文件頁 446-448, PDF 頁 472-474</p></details>
<!-- claim:BASENSMGMT-CREATE-NVM-PAYLOAD -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.03">04.03.</span><span class="paragraph-text">NVM create payload 的主要 host-specified fields 是 NSZE、NCAP、FLBAS、DPS、NMIC、ANAGRPID、NVMSETID、ENDGID、LBSTM、NPHNDLS 與 Placement Handle List。成功 create 後，namespace 依這些屬性格式化；未使用的 reserved fields 應清為 0。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>ANAGRPID</dt><dd>ANA Group Identifier，namespace 所屬 Asymmetric Namespace Access group 的 identifier；create 值 0 讓 controller 選擇。</dd></div><div><dt>NVMSETID</dt><dd>NVM Set Identifier，指定建立 namespace 時要從哪個 NVM Set 配置容量。</dd></div><div><dt>NPHNDLS</dt><dd>Number of Placement Handles，NVM create payload 中 Placement Handle List 的 entry count，最大 128。</dd></div><div><dt>ENDGID</dt><dd>Endurance Group Identifier，指定建立 namespace 時所屬 Endurance Group。</dd></div><div><dt>FLBAS</dt><dd>Formatted LBA Size，選擇 namespace 使用的 LBA format，並包含 metadata placement 相關控制。</dd></div><div><dt>LBSTM</dt><dd>Logical Block Storage Tag Mask，create 時指定哪些 Storage Tag bits 被 mask 的 64-bit 欄位。</dd></div><div><dt>NMIC</dt><dd>Namespace Multi-path I/O and Namespace Sharing Capabilities，create 時宣告 namespace sharing／multipath 屬性的欄位。</dd></div><div><dt>DPS</dt><dd>End-to-end Data Protection Type Settings，create 時選擇 Protection Information type 與位置的欄位。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.6.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.4, 文件頁 111-113, PDF 頁 111-113</p></details>
<!-- claim:BASENSMGMT-PROTECTION-VALIDATION -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.04">04.04.</span><span class="paragraph-text">End-to-end Data Protection 設定在 create 時套用。LBAFEE 未啟用時，特定 16-bit STS 非零、32-bit 或 64-bit Guard Protection Information 組合必須以 Invalid Namespace or Format 中止；LBSTM 不符合 Figure 127 capability 時則回 Invalid Field in Command。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Protection Information</dt><dd>資料保護資訊，縮寫 PI；包含 Guard 與 tags，用來檢查資料及其關聯資訊。</dd></div><div><dt>Guard</dt><dd>PI 的檢查值欄位；所選格式決定檢查值的寬度與計算方法。</dd></div><div><dt>LBSTM</dt><dd>Logical Block Storage Tag Mask，create 時指定哪些 Storage Tag bits 被 mask 的 64-bit 欄位。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.6.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.2, 文件頁 110, PDF 頁 110</p></details>
<!-- claim:BASENSMGMT-FDP-VALIDATION -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.05">04.05.</span><span class="paragraph-text">只有指定 Endurance Group 已啟用 Flexible Data Placement（FDP）且 SEL=Create 時，NPHNDLS 與 Placement Handle List 才參與驗證。NPHNDLS 不得大於支援的 Reclaim Unit Handles 或 128；重複、越界、格式不相容或無可用 handle 會導向 Invalid Placement Handle List 或 Invalid Format。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Endurance Group</dt><dd>Endurance Group，用於隔離與回報耐久度相關狀態的 NVM 資源群組。</dd></div><div><dt>Reclaim Unit</dt><dd>Reclaim Unit，controller 執行媒體回收時使用的較小管理粒度。</dd></div><div><dt>NPHNDLS</dt><dd>Number of Placement Handles，NVM create payload 中 Placement Handle List 的 entry count，最大 128。</dd></div><div><dt>FDP</dt><dd>Flexible Data Placement，把資料放置提示與媒體回收管理連結的能力。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.6.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.3, 文件頁 110-111, PDF 頁 110-111</p></details>
<!-- claim:BASENSMGMT-GROUP-SELECTION -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.06">04.06.</span><span class="paragraph-text">NVMSETID／ENDGID 的決策矩陣為：兩者 0 由 controller 選兩者；NVMSETID=0、ENDGID≠0 時由指定 Endurance Group 內選 NVM Set；NVMSETID≠0、ENDGID=0 必須 Invalid Field；兩者非 0 時只有該 NVM Set 確實屬於指定 Endurance Group 才可配置。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Endurance Group</dt><dd>Endurance Group，用於隔離與回報耐久度相關狀態的 NVM 資源群組。</dd></div><div><dt>NVMSETID</dt><dd>NVM Set Identifier，指定建立 namespace 時要從哪個 NVM Set 配置容量。</dd></div><div><dt>NVM Set</dt><dd>NVM Set，把 namespace 與一組共同管理的 NVM 資源建立關聯的容量集合。</dd></div><div><dt>ENDGID</dt><dd>Endurance Group Identifier，指定建立 namespace 時所屬 Endurance Group。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.17</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 661, PDF 頁 687</p></details>
</details>
<div class="table-wrap"><table><caption>建立 Namespace 所需的資料</caption><thead><tr><th scope="col">資料區域與解讀格式</th><th scope="col">該區域的用途</th><th scope="col">欄位有效的條件</th></tr></thead><tbody><tr><td>Base 0:511</td><td>SIOCS</td><td>NVM-specific create data</td></tr><tr><td>Base 512:1023</td><td>Reserved</td><td>host 清 0</td></tr><tr><td>Base 1024:4095</td><td>Vendor Specific</td><td>沒有來源定義就不猜</td></tr><tr><td>NVM 512:767</td><td>Placement Handle List</td><td>只在 FDP enable 時驗證</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>SIOCS</dt><dd>Specified I/O Command Set，Base create buffer bytes 0:511 中放置所選 I/O Command Set specific fields 的區域。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.07">04.07.</span><span class="paragraph-text">建立 4 MiB namespace：LBA=4096 bytes、NSZE=NCAP=1024，因此 bytes 7:0 與 15:8 都寫 0000000000000400h。NVMSETID=0、ENDGID=5 表示由 Endurance Group 5 內選 NVM Set；反過來 NVMSETID=7、ENDGID=0 是 Invalid Field。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NVM Set</dt><dd>NVM Set，把 namespace 與一組共同管理的 NVM 資源建立關聯的容量集合。</dd></div></dl></aside>
<a class="reading-link" href="#reading-namespace-create-payload">閱讀相關規格圖表 → 建立 Namespace 所需的資料</a>
</section>
<section class="lesson" id="module-namespace-lifecycle"><h2 id="heading-namespace-lifecycle"><span class="section-number">05</span> 建立、連接與使用 Namespace</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span><span class="paragraph-text">Create、Attach、Detach、Delete 分別改變兩個狀態維度：namespace 是否 allocated，以及某 controller 是否 attached。Create CQE.DW0 回 NSID 後，object 已 allocated 但所有 controller 都未 attached；Attach 的 Controller List 才建立 access。Detach 不刪容量，Delete 才使 NSID unallocated。</span></p>
<figure><figcaption><strong>Namespace 從建立到可存取</strong></figcaption><ol class="flow-steps"><li>建立 namespace，取得 NSID。</li><li>將 namespace 附加至指定 controller。</li><li>由該 controller 的 Identify 結果確認 namespace 與格式。</li><li>I/O 命令使用 NSID 指定要存取的 namespace。</li></ol><figcaption>建立儲存物件與讓 controller 可以存取它，是分開的動作。</figcaption></figure>

<details class="technical-note"><summary>完整規則：建立、連接與使用 Namespace</summary>
<!-- claim:BASENSMGMT-NSMGMT-CAPABILITY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.02">05.02.</span><span class="paragraph-text">完整 Namespace Management capability 由 Namespace Management command 與 Namespace Attachment command 組成。支援時 controller 必須支援兩者、設 OACS.NMS=1、支援 Attached Namespace Attribute Changed event；Allocated event 為 should，Namespace Granularity 與 Restore Default 為 may。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>OACS.NMS</dt><dd>Optional Admin Command Support 的 Namespace Management Supported bit；設為 1 才宣告完整 Manage 加 Attach capability。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.17</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686</p></details>
<!-- claim:BASENSMGMT-ATTACH-COMMAND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.03">05.03.</span><span class="paragraph-text">Namespace Attachment 的 DPTR 指向 4096-byte Controller List；SEL=0h attach、SEL=1h detach。以 PRP 指向此 buffer 時不得使用 PRP List，因 buffer 不可跨越超過一個 memory-page boundary。attach／detach 狀態跨所有 reset events 保留。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>DPTR</dt><dd>Data Pointer，SQE 中指出 command data buffer 的欄位。</dd></div><div><dt>PRP</dt><dd>Physical Region Page，以 memory page 為單位描述 host-addressable data buffer 的 pointer 格式。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.24</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, 文件頁 444-445, PDF 頁 470-471</p></details>
<!-- claim:BASENSMGMT-ATTACH-LIMITS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.04">05.04.</span><span class="paragraph-text">attach 前分別核對 Domain aggregate MAXDNA 與每個 I/O controller 的 MAXCNA；非零 limit 被超過時回 Namespace Attachment Limit Exceeded。還要核對 I/O Command Set support／enable state，不能把所有 attach failure 都歸成同一種 status。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>I/O controller</dt><dd>I/O controller，可執行使用者資料 I/O command 的 controller 類型。</dd></div><div><dt>MAXCNA</dt><dd>Maximum I/O Controller Namespace Attachments，單一 I/O controller 可附掛 namespaces 的上限。</dd></div><div><dt>MAXDNA</dt><dd>Maximum Domain Namespace Attachments，整個 Domain 內所有 I/O controller attachment 數量總和的上限。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.24</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, 文件頁 444-445, PDF 頁 470-471</p></details>
</details>
<div class="table-wrap"><table><caption>建立、連接與使用 Namespace</caption><thead><tr><th scope="col">管理動作</th><th scope="col">改變哪個物件或關係</th><th scope="col">操作後仍保留什麼</th></tr></thead><tbody><tr><td>Create</td><td>object／capacity</td><td>不自動 attach</td></tr><tr><td>Attach</td><td>access relationship</td><td>Controller List 可含多個 CNTLID</td></tr><tr><td>Detach</td><td>對指定控制器的可存取狀態</td><td>namespace 仍 allocated</td></tr><tr><td>Delete</td><td>subsystem inventory</td><td>NSID 變 unallocated</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="05.05">05.05.</span><span class="paragraph-text">Create 回 NSID=7。Controller List 的 NUMCIDS 與 entries 指定 controllers 3、5；Attach 成功後 NSID 7 對 3、5 active。再只 detach controller 3，NSID 7 對 3 inactive、對 5 仍 active，namespace 本身仍 allocated。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NUMCIDS</dt><dd>Number of Controller Identifiers；Controller List 中有效 controller IDs 的數量。</dd></div></dl></aside>
<a class="reading-link" href="#reading-namespace-lifecycle">閱讀相關規格圖表 → 建立、連接與使用 Namespace</a>
</section>
<section class="lesson" id="module-delete-restore-state"><h2 id="heading-delete-restore-state"><span class="section-number">06</span> 刪除與恢復預設配置</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.01">06.01.</span><span class="paragraph-text">Delete all 與 Restore Default 是兩個不同 operation。NSID=FFFFFFFFh 的 Delete All 在零個 namespaces 時也成功；Restore Default 則要求 RDNCS capability、SEL=2h，以及 subsystem 中已不存在任何 namespace。成功前 controller 套用 current active firmware image defaults 並設 DNCS=1。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>RDNCS</dt><dd>Restore Default Namespace Configuration Supported，宣告 Restore Default operation 是否支援的 capability bit。</dd></div><div><dt>DNCS</dt><dd>Default Namespace Configuration Status，表示目前 namespace configuration 是否等於 active firmware image defaults 的 status bit。</dd></div></dl>
<details class="technical-note"><summary>完整規則：刪除與恢復預設配置</summary>
<!-- claim:BASENSMGMT-DELETE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.02">06.02.</span><span class="paragraph-text">Delete 的 NSID 指定已建立 namespace；FFFFFFFFh 表示 delete all，即使目前零個 namespaces 也成功。delete 會使 namespace 從 subsystem 消失並具有 detach side effect；host 應先 detach 所有 controllers，讓 event 與 outstanding-I/O 行為更可控。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.25, 8.1.17.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446, 448, 662, PDF 頁 472, 474, 688</p></details>
<!-- claim:BASENSMGMT-RESTORE-DEFAULT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.03">06.03.</span><span class="paragraph-text">Restore Default 使用 SEL=2h，NSID 應為 0 且 controller 會忽略它。先讀 RDNCS，刪除 subsystem 中所有 namespaces，再送 restore；若仍有 namespace，回 Command Sequence Error。成功前 controller 必須套用 current active firmware image 的 default configuration 並設 DNCS=1。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>RDNCS</dt><dd>Restore Default Namespace Configuration Supported，宣告 Restore Default operation 是否支援的 capability bit。</dd></div><div><dt>DNCS</dt><dd>Default Namespace Configuration Status，表示目前 namespace configuration 是否等於 active firmware image defaults 的 status bit。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.25.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25.1, 文件頁 447-448, PDF 頁 473-474</p></details>
<!-- claim:BASENSMGMT-NAMESPACE-EVENTS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.04">06.04.</span><span class="paragraph-text">create 改變 Allocated Namespace ID list；attach／detach 改變 Active Namespace ID list；delete 可能同時改變兩者。啟用對應 notice 時，host 收到 asynchronous event 後應重新 Identify，而不是只用 event code 猜新 inventory。§8.1.17.2 對處理 delete 的 controller 與其他 controllers 規定不同 event reporting。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.17.1-8.1.17.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, 文件頁 662-663, PDF 頁 688-689</p></details>
</details>
<div class="table-wrap"><table><caption>刪除與恢復預設配置</caption><thead><tr><th scope="col">刪除或恢復動作</th><th scope="col">命令如何選對象</th><th scope="col">完成後如何確認配置</th></tr></thead><tbody><tr><td>Delete one</td><td>NSID=target</td><td>成功後 object 消失</td></tr><tr><td>Delete all</td><td>NSID=FFFFFFFFh</td><td>zero namespace 仍成功</td></tr><tr><td>Restore</td><td>SEL=2h、NSID ignored</td><td>剩餘 namespace→Sequence Error</td></tr><tr><td>Post-condition</td><td>DNCS=1</td><td>仍要重新 Identify actual defaults</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="06.05">06.05.</span><span class="paragraph-text">先 detach NSID 7，再 Delete 7；讀 Allocated Namespace ID list 確認為空。若 RDNCS=1，送 SEL=2h、NSID=0。CQE success 後讀 DNCS=1，最後重新列舉 default namespaces；DNCS 是狀態證據，不是 default layout 的完整描述。</span></p></aside>
<a class="reading-link" href="#reading-delete-restore-state">閱讀相關規格圖表 → 刪除與恢復預設配置</a>
</section>
<section class="lesson" id="module-namespace-events"><h2 id="heading-namespace-events"><span class="section-number">07</span> Namespace 變更通知與重新辨識</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.01">07.01.</span><span class="paragraph-text">Attached 與 Allocated Namespace Attribute Changed notices 對應不同 inventory。Create 通常改 Allocated list；Attach／Detach 改 Active list；Delete 可能同時改兩者。event code 不是新清單本身，因此 host 收到 AEN 後要依 CNS 重新 Identify。Delete reporting 還要分辨 processing controller 與其他 controllers。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>AEN</dt><dd>Asynchronous Event Notification，controller 透過已提交 Asynchronous Event Request 回報事件的通知。</dd></div><div><dt>CNS</dt><dd>Controller or Namespace Structure；Identify 命令用來選擇回傳資料結構的欄位。</dd></div></dl>
<details class="technical-note"><summary>完整規則：Namespace 變更通知與重新辨識</summary>
<!-- claim:BASENSMGMT-COMMAND-STATUS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.02">07.02.</span><span class="paragraph-text">Namespace Attachment 與 Management 有各自的 command-specific status。Attachment 包括 already attached 18h、private 19h、not attached 1Ah、Controller List invalid 1Ch、ANA attach failed 25h、limit 27h、I/O Command Set 29h／2Ah；Management 包括 Invalid Format 0Ah、insufficient capacity 15h、NSID unavailable 16h、thin provisioning unsupported 1Bh、ANA group invalid 24h。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>ANA</dt><dd>Asymmetric Namespace Access；描述同一 namespace 經不同 controllers 存取時的路徑狀態。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.24-5.2.25</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24-5.2.25, 文件頁 445, 448, PDF 頁 471, 474</p></details>
</details>
<div class="table-wrap"><table><caption>Namespace 變更通知與重新辨識</caption><thead><tr><th scope="col">通知或清單</th><th scope="col">描述哪種配置變化</th><th scope="col">應重新查詢什麼</th></tr></thead><tbody><tr><td>CNS 02h</td><td>Active Namespace ID list</td><td>Attached notice</td></tr><tr><td>CNS 10h</td><td>Allocated Namespace ID list</td><td>Allocated notice</td></tr><tr><td>Create</td><td>Allocated change</td><td>新 NSID 尚未 active</td></tr><tr><td>Delete</td><td>Allocated＋可能 Active</td><td>processing controller 規則不同</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>CNS</dt><dd>Controller or Namespace Structure；Identify 命令用來選擇回傳資料結構的欄位。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="07.03">07.03.</span><span class="paragraph-text">Controller 3 處理 attached NSID 7 的 Delete。其他已啟用 notice 的 controllers 依 §8.1.17.2 回報；processing controller 的要求不同。host 不應只計算 event 數量，而要為每個 controller 保存 before/after Active 與 Allocated lists。</span></p></aside>
<a class="reading-link" href="#reading-namespace-events">閱讀相關規格圖表 → Namespace 變更通知與重新辨識</a>
</section>
<details class="figure-reading-fold"><summary>展開圖表教學：依主軸閱讀來源圖表</summary>
<section id="figure-reading"><h2><span class="section-number">08</span> 讀懂本篇的規格圖表</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.01">08.01.</span><span class="paragraph-text">以下依概念整理規格中的圖表。每組先說明讀取順序與要判斷的問題，接著列出各圖的欄位或行為說明。可以由正文的連結跳到對應組別，也可以用這一節檢查自己能否把欄位連回完整操作。</span></p>
<div class="figure-reading-group" id="reading-diagnostic-and-provisioning"><h3>圖表組 01 · 裝置診斷與 Namespace 配置</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.02">08.02.</span><span class="paragraph-text">先用關係表選對象：測試、儲存物件、控制器的存取關係或清單。再追蹤對應的完成資訊及後續查詢，避免用 Self-test 的完成語意解釋 Namespace Create。</span></p>
<a class="reading-link" href="#module-diagnostic-and-provisioning">回到本節的解釋與範例</a>
<!-- figure-table:BASENSMGMT-FIG-176 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-176"><summary>Base Figure 176 · Device Self-test Namespace Test Action</summary>
<!-- claim:BASENSMGMT-FIG-176-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.03">08.03.</span><span class="paragraph-text">Figure 176〈Device Self-test Namespace Test Action〉：Self-test 的 NSID 選擇測試範圍，STC 選動作，DSTP 則依相應測試格式解讀。狀態流程區分啟動、已在執行及中止；啟動命令的完成不表示背景測試通過。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>DSTP</dt><dd>Device Self-test Parameter，只有 vendor-specific STC=Eh 時才有 vendor-defined 語意的 CDW15。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 176, 文件頁 199, PDF 頁 225</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-218 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-218"><summary>Base Figure 218 · Device Self-test Log Page</summary>
<!-- claim:BASENSMGMT-FIG-218-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.04">08.04.</span><span class="paragraph-text">Figure 218〈Device Self-test Log Page〉：Self-test log 把 current operation 與最多 20 筆歷史結果分開。歷史項目先讀測試種類和結果碼，再按有效位讀 NSID、FLBA 或狀態；有數值不代表欄位有效。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>FLBA</dt><dd>Failing LBA，NVM Command Set 定義為造成 self-test failure 的其中一個 logical block address。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, Figure 218, 文件頁 230, PDF 頁 256</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-445 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-445"><summary>Base Figure 445 · Namespace Management - Data Pointer</summary>
<!-- claim:BASENSMGMT-FIG-445-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.05">08.05.</span><span class="paragraph-text">Figure 445〈Namespace Management - Data Pointer〉：Namespace Management 用 SEL 選 Create、Delete 或 Restore，Create 的資料依 CSI 解讀。成功建立時 CQE DW0 回傳 NSID；這表示儲存物件已建立，並未自動替主機完成 Attachment。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.25</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 445, 文件頁 446, PDF 頁 472</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-450 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-450"><summary>Base Figure 450 · Namespace Management - Completion Queue Entry Dword 0</summary>
<!-- claim:BASENSMGMT-FIG-450-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.06">08.06.</span><span class="paragraph-text">Figure 450〈Namespace Management - Completion Queue Entry Dword 0〉：Namespace Management 用 SEL 選 Create、Delete 或 Restore，Create 的資料依 CSI 解讀。成功建立時 CQE DW0 回傳 NSID；這表示儲存物件已建立，並未自動替主機完成 Attachment。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Dword</dt><dd>Dword（Double word）；32 bits，也就是 4 bytes。對比 word=16 bits；例如 zero-based dword count=3 代表 4 個 Dwords，也就是 16 bytes。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.25</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 450, 文件頁 448, PDF 頁 474</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-093 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-093"><summary>Base Figure 93 · Common Command Format</summary>
<!-- claim:BASENSMGMT-FIG-093-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.07">08.07.</span><span class="paragraph-text">Figure 93〈Common Command Format〉：共同 SQE 先以 CDW0 描述 opcode、命令識別與資料指標選擇，再以 NSID 選對象、MPTR／DPTR 指向資料。CDW10–15 的意義由個別命令決定，不能跨 opcode 沿用。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>MPTR</dt><dd>Metadata Pointer，SQE 中指出獨立 metadata buffer 的欄位。</dd></div><div><dt>SQE</dt><dd>Submission Queue Entry，SQ 中的一筆命令資料結構。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, 文件頁 140-142, PDF 頁 166-168</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-155 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-155"><summary>Base Figure 155 · Asynchronous Event Information - Notice</summary>
<!-- claim:BASENSMGMT-FIG-155-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.08">08.08.</span><span class="paragraph-text">Figure 155〈Asynchronous Event Information - Notice〉：事件種類與事件啟用是兩份不同資訊。先以通知種類找到本篇使用的事件，再看相應啟用位；取得通知後仍需讀對應狀態或 log，通知本身不包含完整結果。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.2.1, Figure 155, 文件頁 186, PDF 頁 212</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-selftest-command-state-machine"><h3>圖表組 02 · Device Self-test 的執行與結果</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.09">08.09.</span><span class="paragraph-text">命令格式先讀 NSID 與 STC，再沿狀態流程找到 LID 06h。結果布局先拆開測試種類與結果碼，再依 SEGN、FVLD 等有效性條件決定要讀哪些細節。</span></p>
<a class="reading-link" href="#module-selftest-command-state-machine">回到本節的解釋與範例</a>
<!-- figure-table:BASENSMGMT-FIG-111 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-111"><summary>NVM Figure 111 · Self-test Results Data Structure</summary>
<!-- claim:BASENSMGMT-FIG-111-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.10">08.10.</span><span class="paragraph-text">Figure 111〈Self-test Results Data Structure〉：定義〈Self-test Results Data Structure〉的實際配置或數值關係。</span></p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.4.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, Figure 111, 文件頁 76, PDF 頁 76</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-177 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-177"><summary>Base Figure 177 · Device Self-test - Command Dword 10</summary>
<!-- claim:BASENSMGMT-FIG-177-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.11">08.11.</span><span class="paragraph-text">Figure 177〈Device Self-test - Command Dword 10〉：Self-test 的 NSID 選擇測試範圍，STC 選動作，DSTP 則依相應測試格式解讀。狀態流程區分啟動、已在執行及中止；啟動命令的完成不表示背景測試通過。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Dword</dt><dd>Dword（Double word）；32 bits，也就是 4 bytes。對比 word=16 bits；例如 zero-based dword count=3 代表 4 個 Dwords，也就是 16 bytes。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 177, 文件頁 199, PDF 頁 225</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-178 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-178"><summary>Base Figure 178 · Device Self-test - Command Dword 15</summary>
<!-- claim:BASENSMGMT-FIG-178-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.12">08.12.</span><span class="paragraph-text">Figure 178〈Device Self-test - Command Dword 15〉：Self-test 的 NSID 選擇測試範圍，STC 選動作，DSTP 則依相應測試格式解讀。狀態流程區分啟動、已在執行及中止；啟動命令的完成不表示背景測試通過。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 178, 文件頁 200, PDF 頁 226</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-179 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-179"><summary>Base Figure 179 · Device Self-test - Command Processing</summary>
<!-- claim:BASENSMGMT-FIG-179-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.13">08.13.</span><span class="paragraph-text">Figure 179〈Device Self-test - Command Processing〉：Self-test 的 NSID 選擇測試範圍，STC 選動作，DSTP 則依相應測試格式解讀。狀態流程區分啟動、已在執行及中止；啟動命令的完成不表示背景測試通過。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 179, 文件頁 200, PDF 頁 226</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-180 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-180"><summary>Base Figure 180 · Device Self-test - Command Specific Status Values</summary>
<!-- claim:BASENSMGMT-FIG-180-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.14">08.14.</span><span class="paragraph-text">Figure 180〈Device Self-test - Command Specific Status Values〉：Self-test 的 NSID 選擇測試範圍，STC 選動作，DSTP 則依相應測試格式解讀。狀態流程區分啟動、已在執行及中止；啟動命令的完成不表示背景測試通過。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, Figure 180, 文件頁 201, PDF 頁 227</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-219 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-219"><summary>Base Figure 219 · Self-test Result Data Structure</summary>
<!-- claim:BASENSMGMT-FIG-219-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.15">08.15.</span><span class="paragraph-text">Figure 219〈Self-test Result Data Structure〉：Self-test log 把 current operation 與最多 20 筆歷史結果分開。歷史項目先讀測試種類和結果碼，再按有效位讀 NSID、FLBA 或狀態；有數值不代表欄位有效。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, Figure 219, 文件頁 231-232, PDF 頁 257-258</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>VDINFO</dt><dd>Valid Diagnostic Information，分別 gate NSID、FLBA、SCT 與 SC 的 validity bitmap。</dd></div></dl>
</details>
<!-- figure-table:BASENSMGMT-FIG-700 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-700"><summary>Base Figure 700 · Example Device Self-test Operation (Informative)</summary>
<!-- claim:BASENSMGMT-FIG-700-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.16">08.16.</span><span class="paragraph-text">Figure 700〈Example Device Self-test Operation (Informative)〉：自我測試操作圖是說明性例子，不能將它的每個 segment 當成裝置必須採用的實作。Format NVM 是否中止測試，則要把 Format 的對象、設定與目前測試範圍一起比較。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.8</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.8, Figure 700, 文件頁 615, PDF 頁 641</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-701 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-701"><summary>Base Figure 701 · Format NVM command Aborting a Device Self-Test Operation</summary>
<!-- claim:BASENSMGMT-FIG-701-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.17">08.17.</span><span class="paragraph-text">Figure 701〈Format NVM command Aborting a Device Self-Test Operation〉：自我測試操作圖是說明性例子，不能將它的每個 segment 當成裝置必須採用的實作。Format NVM 是否中止測試，則要把 Format 的對象、設定與目前測試範圍一起比較。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.8.1-8.1.8.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, Figure 701, 文件頁 616, PDF 頁 642</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-203 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-203"><summary>Base Figure 203 · Get Log Page - Data Pointer</summary>
<!-- claim:BASENSMGMT-FIG-203-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.18">08.18.</span><span class="paragraph-text">Figure 203〈Get Log Page - Data Pointer〉：Get Log Page 先由 LID 選資料，再以 NUMDU／NUMDL 描述傳輸長度、LPOU／LPOL 描述位移，RAE 控制事件保留。LSI、CSI、UIDX 的意義由所選 log 決定，不能直接沿用其他 log 的選擇值。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NUMDL</dt><dd>Number of Dwords Lower，Get Log Page 的 NUMD 低 16 bits。</dd></div><div><dt>NUMDU</dt><dd>Number of Dwords Upper，Get Log Page 的 NUMD 高 16 bits。</dd></div><div><dt>LPOL</dt><dd>Log Page Offset Lower，Get Log Page byte offset 的低 32 bits。</dd></div><div><dt>LPOU</dt><dd>Log Page Offset Upper，Get Log Page byte offset 的高 32 bits。</dd></div><div><dt>UIDX</dt><dd>UUID Index，指向 UUID List 位置的 index；0 表示未指定 UUID。</dd></div><div><dt>LSI</dt><dd>Log Specific Identifier，意義由所選 log page 定義的 identifier。</dd></div><div><dt>RAE</dt><dd>Retain Asynchronous Event，Get Log Page 是否保留相關 asynchronous event 的 selector。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 203, 文件頁 213, PDF 頁 239</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-204 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-204"><summary>Base Figure 204 · Get Log Page - Command Dword 10</summary>
<!-- claim:BASENSMGMT-FIG-204-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.19">08.19.</span><span class="paragraph-text">Figure 204〈Get Log Page - Command Dword 10〉：Get Log Page 先由 LID 選資料，再以 NUMDU／NUMDL 描述傳輸長度、LPOU／LPOL 描述位移，RAE 控制事件保留。LSI、CSI、UIDX 的意義由所選 log 決定，不能直接沿用其他 log 的選擇值。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NUMDL</dt><dd>Number of Dwords Lower，Get Log Page 的 NUMD 低 16 bits。</dd></div><div><dt>NUMDU</dt><dd>Number of Dwords Upper，Get Log Page 的 NUMD 高 16 bits。</dd></div><div><dt>LPOL</dt><dd>Log Page Offset Lower，Get Log Page byte offset 的低 32 bits。</dd></div><div><dt>LPOU</dt><dd>Log Page Offset Upper，Get Log Page byte offset 的高 32 bits。</dd></div><div><dt>UIDX</dt><dd>UUID Index，指向 UUID List 位置的 index；0 表示未指定 UUID。</dd></div><div><dt>LSI</dt><dd>Log Specific Identifier，意義由所選 log page 定義的 identifier。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 204, 文件頁 213, PDF 頁 239</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>LSP</dt><dd>Log Specific Field，意義由所選 log page 定義的 command selector。</dd></div></dl>
</details>
<!-- figure-table:BASENSMGMT-FIG-205 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-205"><summary>Base Figure 205 · Get Log Page - Command Dword 11</summary>
<!-- claim:BASENSMGMT-FIG-205-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.20">08.20.</span><span class="paragraph-text">Figure 205〈Get Log Page - Command Dword 11〉：Get Log Page 先由 LID 選資料，再以 NUMDU／NUMDL 描述傳輸長度、LPOU／LPOL 描述位移，RAE 控制事件保留。LSI、CSI、UIDX 的意義由所選 log 決定，不能直接沿用其他 log 的選擇值。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 205, 文件頁 214, PDF 頁 240</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-206 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-206"><summary>Base Figure 206 · Get Log Page - Command Dword 12</summary>
<!-- claim:BASENSMGMT-FIG-206-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.21">08.21.</span><span class="paragraph-text">Figure 206〈Get Log Page - Command Dword 12〉：Get Log Page 先由 LID 選資料，再以 NUMDU／NUMDL 描述傳輸長度、LPOU／LPOL 描述位移，RAE 控制事件保留。LSI、CSI、UIDX 的意義由所選 log 決定，不能直接沿用其他 log 的選擇值。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 206, 文件頁 214, PDF 頁 240</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-207 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-207"><summary>Base Figure 207 · Get Log Page - Command Dword 13</summary>
<!-- claim:BASENSMGMT-FIG-207-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.22">08.22.</span><span class="paragraph-text">Figure 207〈Get Log Page - Command Dword 13〉：Get Log Page 先由 LID 選資料，再以 NUMDU／NUMDL 描述傳輸長度、LPOU／LPOL 描述位移，RAE 控制事件保留。LSI、CSI、UIDX 的意義由所選 log 決定，不能直接沿用其他 log 的選擇值。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 207, 文件頁 214, PDF 頁 240</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-208 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-208"><summary>Base Figure 208 · Get Log Page - Command Dword 14</summary>
<!-- claim:BASENSMGMT-FIG-208-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.23">08.23.</span><span class="paragraph-text">Figure 208〈Get Log Page - Command Dword 14〉：Get Log Page 先由 LID 選資料，再以 NUMDU／NUMDL 描述傳輸長度、LPOU／LPOL 描述位移，RAE 控制事件保留。LSI、CSI、UIDX 的意義由所選 log 決定，不能直接沿用其他 log 的選擇值。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 208, 文件頁 214-215, PDF 頁 240-241</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-209 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-209"><summary>Base Figure 209 · Get Log Page - Log Page Identifiers</summary>
<!-- claim:BASENSMGMT-FIG-209-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.24">08.24.</span><span class="paragraph-text">Figure 209〈Get Log Page - Log Page Identifiers〉：Get Log Page 先由 LID 選資料，再以 NUMDU／NUMDL 描述傳輸長度、LPOU／LPOL 描述位移，RAE 控制事件保留。LSI、CSI、UIDX 的意義由所選 log 決定，不能直接沿用其他 log 的選擇值。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, Figure 209, 文件頁 215-216, PDF 頁 241-242</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NVM subsystem</dt><dd>NVM subsystem，包含 controller、port、namespace 與非揮發性儲存資源的 NVMe 系統邊界。</dd></div></dl>
</details>
</div>
<div class="figure-reading-group" id="reading-capacity-granularity-math"><h3>圖表組 03 · 容量數值與配置粒度</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.25">08.25.</span><span class="paragraph-text">容量圖比較 NSZE、NCAP、NUSE 的數量，粒度表則以 bytes 比較。先列出區塊數×區塊大小，再計算對 NSG、NCG 的餘數；不要直接拿區塊數除以 byte 粒度。</span></p>
<a class="reading-link" href="#module-capacity-granularity-math">回到本節的解釋與範例</a>
<!-- figure-table:BASENSMGMT-FIG-123 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-123"><summary>NVM Figure 123 · Identify - Identify Namespace Data Structure, NVM Command Set</summary>
<!-- claim:BASENSMGMT-FIG-123-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.26">08.26.</span><span class="paragraph-text">Figure 123〈Identify - Identify Namespace Data Structure, NVM Command Set〉：定義〈Identify - Identify Namespace Data Structure, NVM Command Set〉的實際配置或數值關係。</span></p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.5.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1, Figure 123, 文件頁 85-87, PDF 頁 85-87</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>FLBAS</dt><dd>Formatted LBA Size，選擇 namespace 使用的 LBA format，並包含 metadata placement 相關控制。</dd></div><div><dt>NMIC</dt><dd>Namespace Multi-path I/O and Namespace Sharing Capabilities，create 時宣告 namespace sharing／multipath 屬性的欄位。</dd></div><div><dt>DPS</dt><dd>End-to-end Data Protection Type Settings，create 時選擇 Protection Information type 與位置的欄位。</dd></div></dl>
</details>
<!-- figure-table:BASENSMGMT-FIG-132 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-132"><summary>NVM Figure 132 · Namespace Granularity List</summary>
<!-- claim:BASENSMGMT-FIG-132-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.27">08.27.</span><span class="paragraph-text">Figure 132〈Namespace Granularity List〉：呈現〈Namespace Granularity List〉中的物件或容量關係。</span></p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.5.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.8, Figure 132, 文件頁 108, PDF 頁 108</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-133 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-133"><summary>NVM Figure 133 · Namespace Granularity Descriptor</summary>
<!-- claim:BASENSMGMT-FIG-133-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.28">08.28.</span><span class="paragraph-text">Figure 133〈Namespace Granularity Descriptor〉：定義〈Namespace Granularity Descriptor〉的實際配置或數值關係。</span></p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.5.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.8, Figure 133, 文件頁 108, PDF 頁 108</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-namespace-create-payload"><h3>圖表組 04 · 建立 Namespace 所需的資料</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.29">08.29.</span><span class="paragraph-text">先從 Base 的資料外框進入 NVM 專用解讀，再對照相同 offset 的欄位。容量值按所選格式換算，Placement Handle List 按 FDP 啟用條件讀取；表中的不同列不是互相獨立且可以相加的 buffer。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>offset</dt><dd>offset；從指定起點算出的位移。它回答「離起點多遠」，不等於 index。</dd></div></dl>
<a class="reading-link" href="#module-namespace-create-payload">回到本節的解釋與範例</a>
<!-- figure-table:BASENSMGMT-FIG-134 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-134"><summary>NVM Figure 134 · Namespace Management - Host Specified Fields</summary>
<!-- claim:BASENSMGMT-FIG-134-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.30">08.30.</span><span class="paragraph-text">Figure 134〈Namespace Management - Host Specified Fields〉：定義〈Namespace Management - Host Specified Fields〉的實際配置或數值關係。</span></p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.6.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.4, Figure 134, 文件頁 112-113, PDF 頁 112-113</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>ANAGRPID</dt><dd>ANA Group Identifier，namespace 所屬 Asymmetric Namespace Access group 的 identifier；create 值 0 讓 controller 選擇。</dd></div></dl>
</details>
<!-- figure-table:BASENSMGMT-FIG-446 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-446"><summary>Base Figure 446 · Namespace Management - Command Dword 10</summary>
<!-- claim:BASENSMGMT-FIG-446-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.31">08.31.</span><span class="paragraph-text">Figure 446〈Namespace Management - Command Dword 10〉：Namespace Management 用 SEL 選 Create、Delete 或 Restore，Create 的資料依 CSI 解讀。成功建立時 CQE DW0 回傳 NSID；這表示儲存物件已建立，並未自動替主機完成 Attachment。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.25</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 446, 文件頁 446-447, PDF 頁 472-473</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-447 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-447"><summary>Base Figure 447 · Namespace Management - Command Dword 11</summary>
<!-- claim:BASENSMGMT-FIG-447-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.32">08.32.</span><span class="paragraph-text">Figure 447〈Namespace Management - Command Dword 11〉：Namespace Management 用 SEL 選 Create、Delete 或 Restore，Create 的資料依 CSI 解讀。成功建立時 CQE DW0 回傳 NSID；這表示儲存物件已建立，並未自動替主機完成 Attachment。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.25</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 447, 文件頁 447, PDF 頁 473</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-448 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-448"><summary>Base Figure 448 · Namespace Management - Data Structure for Create</summary>
<!-- claim:BASENSMGMT-FIG-448-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.33">08.33.</span><span class="paragraph-text">Figure 448〈Namespace Management - Data Structure for Create〉：Namespace Management 用 SEL 選 Create、Delete 或 Restore，Create 的資料依 CSI 解讀。成功建立時 CQE DW0 回傳 NSID；這表示儲存物件已建立，並未自動替主機完成 Attachment。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.25</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 448, 文件頁 447, PDF 頁 473</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>SIOCS</dt><dd>Specified I/O Command Set，Base create buffer bytes 0:511 中放置所選 I/O Command Set specific fields 的區域。</dd></div></dl>
</details>
<!-- figure-table:BASENSMGMT-FIG-036 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-036"><summary>Base Figure 36 · Offset 0h: CAP - Controller Capabilities</summary>
<!-- claim:BASENSMGMT-FIG-036-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.34">08.34.</span><span class="paragraph-text">Figure 36〈Offset 0h: CAP - Controller Capabilities〉：CAP 回報支援能力、大小與時間限制，主機以這些資訊選擇可用設定。讀到支援位並不表示對應功能已啟用或控制器已就緒；設定與目前狀態要再讀各自的欄位。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>offset</dt><dd>offset；從指定起點算出的位移。它回答「離起點多遠」，不等於 index。</dd></div><div><dt>CAP</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.4.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, 文件頁 55-58, PDF 頁 81-84</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-127 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-127"><summary>NVM Figure 127 · NVM Command Set I/O Command Set Specific Identify Namespace Data Structure</summary>
<!-- claim:BASENSMGMT-FIG-127-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.35">08.35.</span><span class="paragraph-text">Figure 127〈NVM Command Set I/O Command Set Specific Identify Namespace Data Structure〉：定義〈NVM Command Set I/O Command Set Specific Identify Namespace Data Structure〉的實際配置或數值關係。</span></p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.5.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.3, Figure 127, 文件頁 97-101, PDF 頁 97-101</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-namespace-lifecycle"><h3>圖表組 05 · 建立、連接與使用 Namespace</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.36">08.36.</span><span class="paragraph-text">生命週期圖用實線物件表示 namespace，用連線表示 attachment。Create／Delete 改變物件，Attach／Detach 改變連線；Controller List 指定要改哪些控制器的關係。</span></p>
<a class="reading-link" href="#module-namespace-lifecycle">回到本節的解釋與範例</a>
<!-- figure-table:BASENSMGMT-FIG-442 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-442"><summary>Base Figure 442 · Namespace Attachment - Data Pointer</summary>
<!-- claim:BASENSMGMT-FIG-442-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.37">08.37.</span><span class="paragraph-text">Figure 442〈Namespace Attachment - Data Pointer〉：Namespace Attachment 的 DPTR 指向 Controller List，SEL 選 Attach 或 Detach。命令改變的是指定控制器與 namespace 的關係；完成狀態如已連接、未連接或清單不合法，要按該關係解讀。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.24</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, Figure 442, 文件頁 445, PDF 頁 471</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-443 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-443"><summary>Base Figure 443 · Namespace Attachment - Command Dword 10</summary>
<!-- claim:BASENSMGMT-FIG-443-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.38">08.38.</span><span class="paragraph-text">Figure 443〈Namespace Attachment - Command Dword 10〉：Namespace Attachment 的 DPTR 指向 Controller List，SEL 選 Attach 或 Detach。命令改變的是指定控制器與 namespace 的關係；完成狀態如已連接、未連接或清單不合法，要按該關係解讀。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.24</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, Figure 443, 文件頁 445, PDF 頁 471</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-444 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-444"><summary>Base Figure 444 · Namespace Attachment - Command Specific Status Values</summary>
<!-- claim:BASENSMGMT-FIG-444-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.39">08.39.</span><span class="paragraph-text">Figure 444〈Namespace Attachment - Command Specific Status Values〉：Namespace Attachment 的 DPTR 指向 Controller List，SEL 選 Attach 或 Detach。命令改變的是指定控制器與 namespace 的關係；完成狀態如已連接、未連接或清單不合法，要按該關係解讀。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.24</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, Figure 444, 文件頁 445, PDF 頁 471</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-139 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-139"><summary>Base Figure 139 · Controller List Format</summary>
<!-- claim:BASENSMGMT-FIG-139-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.40">08.40.</span><span class="paragraph-text">Figure 139〈Controller List Format〉：Controller List 以 NUMCIDS 開頭，後接 16-bit controller IDs；Namespace List 直接列出 32-bit NSIDs。兩者都依各自排序及未使用項目規則讀取，但不能共用同一種 header。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NUMCIDS</dt><dd>Number of Controller Identifiers；Controller List 中有效 controller IDs 的數量。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.6.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.6.1, Figure 139, 文件頁 172, PDF 頁 198</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-338 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-338"><summary>Base Figure 338 · Identify Controller Data Structure</summary>
<!-- claim:BASENSMGMT-FIG-338-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.41">08.41.</span><span class="paragraph-text">Figure 338〈Identify Controller Data Structure〉：Identify Controller 的欄位分別描述能力、限制、身分與目前資訊。依本篇主題選出需要的欄位後，再連到相應命令；支援位和大小上限必須一起用，不能以單一旗標推論所有參數都有效。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.14.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, 文件頁 340, 353, 365, 378, PDF 頁 366, 379, 391, 404</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>DSTO.SDSO</dt><dd>Device Self-test Options，Identify Controller 中回報 refresh 與 concurrency 選項的欄位。 此處的 DSTO.SDSO 進一步指定其中的 SDSO 子欄位。</dd></div><div><dt>OACS.NMS</dt><dd>Optional Admin Command Support 的 Namespace Management Supported bit；設為 1 才宣告完整 Manage 加 Attach capability。</dd></div><div><dt>MAXCNA</dt><dd>Maximum I/O Controller Namespace Attachments，單一 I/O controller 可附掛 namespaces 的上限。</dd></div><div><dt>MAXDNA</dt><dd>Maximum Domain Namespace Attachments，整個 Domain 內所有 I/O controller attachment 數量總和的上限。</dd></div></dl>
</details>
</div>
<div class="figure-reading-group" id="reading-delete-restore-state"><h3>圖表組 06 · 刪除與恢復預設配置</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.42">08.42.</span><span class="paragraph-text">先區分單一 Delete、Delete all 與 Restore 的 SEL／NSID 用法，再沿流程核對剩餘 namespace 及支援能力。結果圖把 DNCS 和重新取得的 namespace 清單並列閱讀。</span></p>
<a class="reading-link" href="#module-delete-restore-state">回到本節的解釋與範例</a>
<!-- figure-table:BASENSMGMT-FIG-449 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-449"><summary>Base Figure 449 · Namespace Management - Command Specific Status Values</summary>
<!-- claim:BASENSMGMT-FIG-449-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.43">08.43.</span><span class="paragraph-text">Figure 449〈Namespace Management - Command Specific Status Values〉：Namespace Management 用 SEL 選 Create、Delete 或 Restore，Create 的資料依 CSI 解讀。成功建立時 CQE DW0 回傳 NSID；這表示儲存物件已建立，並未自動替主機完成 Attachment。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.25</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, Figure 449, 文件頁 448, PDF 頁 474</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-304 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-304"><summary>Base Figure 304 · Manufacturer Default Configuration Status Log Page</summary>
<!-- claim:BASENSMGMT-FIG-304-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.44">08.44.</span><span class="paragraph-text">Figure 304〈Manufacturer Default Configuration Status Log Page〉：DNCS 描述是否處於製造商預設 namespace 配置。它是一個狀態判斷，並未列出每個預設 namespace 的容量及格式；這些內容仍需重新 Identify。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.31</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.31, Figure 304, 文件頁 301-302, PDF 頁 327-328</p></details>

</details>
<!-- figure-table:BASENSMGMT-FIG-474 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-474"><summary>Base Figure 474 · Asynchronous Event Configuration - Command Dword 11</summary>
<!-- claim:BASENSMGMT-FIG-474-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.45">08.45.</span><span class="paragraph-text">Figure 474〈Asynchronous Event Configuration - Command Dword 11〉：事件種類與事件啟用是兩份不同資訊。先以通知種類找到本篇使用的事件，再看相應啟用位；取得通知後仍需讀對應狀態或 log，通知本身不包含完整結果。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.6, Figure 474, 文件頁 466-468, PDF 頁 492-494</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-namespace-events"><h3>圖表組 07 · Namespace 變更通知與重新辨識</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.46">08.46.</span><span class="paragraph-text">事件圖從 Create／Attach／Detach／Delete 出發，分別連到 Allocated 和 Active 清單。CNS 02h 和 CNS 10h 查不同集合；namespace 的獨立屬性查詢則補足清單沒有提供的內容。</span></p>
<a class="reading-link" href="#module-namespace-events">回到本節的解釋與範例</a>
<!-- figure-table:BASENSMGMT-FIG-346 -->
<details class="field-note" id="figure-BASENSMGMT-FIG-346"><summary>Base Figure 346 · Identify - I/O Command Set Independent Identify Namespace Data Structure</summary>
<!-- claim:BASENSMGMT-FIG-346-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.47">08.47.</span><span class="paragraph-text">Figure 346〈Identify - I/O Command Set Independent Identify Namespace Data Structure〉：Command Set Independent Identify Namespace 提供跨命令集的 namespace 屬性。ANAGRPID、NVMSETID、ENDGID 分別連到不同資源群組，不能因都是 ID 就把它們當成同一層級。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.14.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.3, Figure 346, 文件頁 391-394, PDF 頁 417-420</p></details>

</details>
</div>
<!-- claim:BASENSMGMT-SELFTEST-INPROGRESS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.48">08.48.</span><span class="paragraph-text">已有 operation 時，再送 short、extended 或 Host-Initiated Refresh 必須以 Device Self-test in Progress 中止；STC=Fh 則依序中止目前 operation、建立最新 result、清除 current status，再成功完成 abort command。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 200, PDF 頁 226</p></details>
<!-- claim:BASENSMGMT-SELFTEST-BACKGROUND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.49">08.49.</span><span class="paragraph-text">Device Self-test 是由 vendor-specific segments 組成的背景工作。若處理另一個 command 必須暫停測試，controller 必須（shall）依序 suspend self-test、處理並完成該 command、再 resume self-test；可同時處理哪些 command 仍由 vendor 決定。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.8</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.8, 文件頁 614, PDF 頁 640</p></details>
<!-- claim:BASENSMGMT-SELFTEST-TIMING -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.50">08.50.</span><span class="paragraph-text">short operation 應（should）在兩分鐘內完成，Controller Level Reset 會中止；extended operation 應在 EDSTT 內完成，必須跨 Controller Level Reset 與 power restoration 持續並於之後 resume。兩種測試不能共用同一套 reset 預期。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.8.1-8.1.8.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, 文件頁 615-616, PDF 頁 641-642</p></details>
<!-- claim:BASENSMGMT-SELFTEST-ABORTS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.51">08.51.</span><span class="paragraph-text">short 與 extended 都會被適用的 Format NVM、sanitize start 或 STC=Fh 中止，namespace 從 inventory 移除時則可能（may）中止。Figure 701 顯示必須同時看 Format NSID、secure-erase 選項與 Self-test NSID。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.8.1-8.1.8.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.8.1-8.1.8.2, 文件頁 615-616, PDF 頁 641-642</p></details>
<!-- claim:BASENSMGMT-SELFTEST-LOG-COMMAND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.52">08.52.</span><span class="paragraph-text">完整讀取 LID 06h 使用 564 bytes=141 dwords，因此 0's-based NUMD=140=008Ch；LID=06h、LSP=0、LPOL/LPOU=0、OT=0、CSI=0、UIDX=0。RAE=0 時 CDW10=008C0006h。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>0's-based</dt><dd>0's-based encoding，以 0 表示實際數量 1；依欄位換算公式通常是欄位值加 1。</dd></div><div><dt>NUMD</dt><dd>Number of Dwords，0's-based transfer dword count；實際 bytes = (NUMD + 1) × 4。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, 文件頁 213-216, PDF 頁 239-242</p></details>
<!-- claim:BASENSMGMT-CREATE-PREFLIGHT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.53">08.53.</span><span class="paragraph-text">create 前先以 NSID=FFFFFFFFh、CNS=00h 讀 common namespace capabilities；若支援，再用 CNS=16h 讀 Namespace Granularity，並確認可用 capacity。這三步完成後才建立 4096-byte create buffer。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.17.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17.1, 文件頁 661-662, PDF 頁 687-688</p></details>
</section>
</details>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:base-self-test-namespace-management-create-attach -->
<details class="review-question" id="qa-base-self-test-namespace-management-create-attach"><summary>1. Namespace Create 成功並回傳 NSID，為何還不能直接假設某 controller 可以對它做 I/O？</summary>
<div data-qa-answer="base-self-test-namespace-management-create-attach"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="09.01">09.01.</span><span class="paragraph-text">Create 建立 namespace；Attachment 決定哪些 controllers 可以存取。還要確認 attachment 與 Identify 所回報的可見性、格式及可用狀態。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446-448, 662, PDF 頁 472-474, 688</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, 文件頁 444-445, PDF 頁 470-471</p>
</details></details>
<!-- qa:base-self-test-namespace-management-granularity -->
<details class="review-question" id="qa-base-self-test-namespace-management-granularity"><summary>2. Namespace granularity hint 與實際媒體配置的 rounding，為何不能混為一談？</summary>
<div data-qa-answer="base-self-test-namespace-management-granularity"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="09.02">09.02.</span><span class="paragraph-text">Hint 協助 host 選擇合適的 size 或 capacity；rounding 描述實際配置可能耗用的資源。Hint 不是任意加上的命令合法性限制，容量規劃也不能只看 host 要求的數值。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 661, PDF 頁 687</p>
<p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.8, 文件頁 165, PDF 頁 165</p>
</details></details>
<!-- qa:base-self-test-namespace-management-restore-default -->
<details class="review-question" id="qa-base-self-test-namespace-management-restore-default"><summary>3. Restore Default Namespace 是否表示恢復已刪除 namespace 的原有資料？</summary>
<div data-qa-answer="base-self-test-namespace-management-restore-default"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="09.03">09.03.</span><span class="paragraph-text">它處理預設 namespace 配置，不是資料復原命令。Namespace 的建立、刪除與預設配置流程，不能被當成保留或找回舊資料的保證。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25.1, 文件頁 447-448, PDF 頁 473-474</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446, 448, 662, PDF 頁 472, 474, 688</p>
</details></details>
<!-- qa:base-self-test-namespace-management-test-history -->
<details class="review-question" id="qa-base-self-test-namespace-management-test-history"><summary>4. 最新一筆 self-test 歷史紀錄，是否必定屬於目前正在執行的測試？</summary>
<div data-qa-answer="base-self-test-namespace-management-test-history"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="09.04">09.04.</span><span class="paragraph-text">歷史紀錄描述已產生的結果；目前 operation 與其進度另有欄位。閱讀時先分清 ongoing test 與 completed result，才不會把上一次結果當作這次結果。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-230, PDF 頁 255-256</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-232, PDF 頁 255-258</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express Base Specification, Revision 2.4</p><p>NVM Express NVM Command Set Specification, Revision 1.3</p></details></footer>
</div>
