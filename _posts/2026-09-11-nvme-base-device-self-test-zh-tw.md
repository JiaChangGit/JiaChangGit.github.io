---
permalink: /nvme/device-self-test-zh-tw/
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4：Device Self-test：執行、進度與結果"
date: 2026-09-11
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
[English]({% post_url 2026-09-11-nvme-base-device-self-test-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">Device Self-test 讓控制器在背景執行內部測試。讀懂這項功能，必須分清「接受測試要求」、「正在測試」與「留下測試結果」三件事；主機收到命令成功完成，並不表示裝置已通過測試。</span></p>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>決定測試對象</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">先確認支援能力，再選擇測試種類及要納入的 namespace；控制器接受要求後，才開始背景測試。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div></dl></article>
<article><span class="axis-number">02</span><h3>追蹤正在進行的作業</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">用目前作業與完成百分比回答「是否還在測試、做到哪裡」；新的命令、重設或中止要求可能影響進行中的作業。</span></p></article>
<article><span class="axis-number">03</span><h3>判讀留下的結果</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">測試停止後，再看結果紀錄。先確認哪些欄位有效，才能解釋失敗位置與相關資訊。</span></p></article>
</div>
<div class="overview-connections"><h3>把主軸連起來</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">先確認控制器支援哪些測試，再選擇測試種類與 namespace，送出命令後觀察目前作業及進度，最後閱讀歷史結果與有效性標記。相同的 Get Log Page 可以在不同時間回答「做到哪裡」和「最後結果如何」，但兩者使用不同欄位。</span></p>
</div>
</section>
<section class="lesson" id="module-selftest-command-state-machine"><h2 id="heading-selftest-command-state-machine"><span class="section-number">01</span> Device Self-test 的啟動與執行</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">Self-test 不是同步 diagnostic RPC。Host 先用 OACS.DSTS、DSTO.SDSO 與 EDSTT 決定支援、concurrency scope 與時間預期，再用 NSID 與 STC 建構 command。Admin CQE 回來時，背景 operation 才剛進入可由 LID 06h 觀察的生命週期。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>OACS.DSTS</dt><dd>Optional Admin Command Support 的 Device Self-test Supported bit，判斷 command 是否可用。</dd></div><div><dt>LID 06h</dt><dd>Device Self-test Log Page 的 identifier 06h；同時包含 current operation 與 20 筆歷史結果。</dd></div><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div><div><dt>EDSTT</dt><dd>Extended Device Self-test Time，在 power state 0 下的 extended test 名目完成分鐘數。</dd></div><div><dt>DSTO</dt><dd>Device Self-test Options，Identify Controller 中回報 refresh 與 concurrency 選項的欄位。</dd></div><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div><div><dt>SDSO</dt><dd>Single Device Self-test Operation，選擇 subsystem-wide 單一 operation 或 per-controller operation 的 bit。</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div><div><dt>LID</dt><dd>Log Page Identifier；指定要讀取哪一種 log page 的編號。</dd></div><div><dt>STC</dt><dd>Self-test Code 是 Device Self-test CDW10 的動作 nibble；result entry 的 STC 則是 Status Code，須依 SCVLD 判斷有效。</dd></div></dl>
<!-- claim:BASESELFTEST-SELFTEST-GATE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">啟動 Device Self-test 前，先讀 Identify Controller：OACS.DSTS 判斷 command 是否支援；EDSTT 是 extended operation 在 power state 0 的名目分鐘數；DSTO.SDSO 決定同時只能有一個 subsystem-wide operation，或每個 controller 各一個。這三個欄位回答不同問題。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.14.2.1, 8.1.8</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 8.1.8, 文件頁 352-358, 614, PDF 頁 378-384, 640</p></details>
<div class="table-wrap"><table><caption>Device Self-test 的啟動與執行</caption><thead><tr><th scope="col">測試對象或控制值</th><th scope="col">涵蓋的範圍或動作</th><th scope="col">執行與結果的規則</th></tr></thead><tbody><tr><td>NSID=0</td><td>只包含 controller</td><td>不測 namespace media</td></tr><tr><td>目前可存取的 NSID</td><td>指定 namespace</td><td>invalid 與 inactive status 不同</td></tr><tr><td>NSID=FFFFFFFFh</td><td>所有 attached／accessible namespaces</td><td>集合以 start 時點為準</td></tr><tr><td>STC=Fh</td><td>abort current operation</td><td>成功不代表曾有 operation</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">啟動 namespace 5 的 short test：NSID=00000005h、STC=1h，因此 CDW10=00000001h、CDW15=0。若立刻再送 extended STC=2h，應預期 command-specific status 1Dh，而不是建立第二個 operation。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-selftest-observe-results"><h2 id="heading-selftest-observe-results"><span class="section-number">02</span> LID 06h 的目前進度與歷史結果</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">log header 的 DSTOS／DSTCS 回答『現在跑到哪裡』；RDS1～RDS20 回答『之前怎麼結束』。result entry 又分成 operation code、result reason、segment、validity bitmap 與 diagnostic payload。NVM Command Set 只在 FVLD=1 時賦予 FLBA 明確的 LBA 語意。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>DSTCS</dt><dd>Device Self-test Completion Status，LID 06h 中的 0 到 100 完成百分比。</dd></div><div><dt>DSTOS</dt><dd>Device Self-test Operation Status，LID 06h 中表示目前 operation 類型的 nibble。</dd></div><div><dt>FLBA</dt><dd>Failing LBA，NVM Command Set 定義為造成 self-test failure 的其中一個 logical block address。</dd></div><div><dt>FVLD</dt><dd>Failing LBA Valid，決定 FLBA 欄位是否可解讀的 validity bit。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl>
<!-- claim:BASESELFTEST-SELFTEST-LOG-COMMAND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">讀取 LID 06h 所需的最小 Get Log Page slice 是：LID=06h、LSP=0、RAE 依事件策略選擇、NUMD 表示 564 bytes、LPOL/LPOU=0、OT=0、CSI=0、UIDX=0。564 bytes=141 dwords，因此 0's-based NUMD=140=008Ch；RAE=0 時 CDW10=008C0006h。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>0's-based</dt><dd>0's-based encoding，以 0 表示實際數量 1；依欄位換算公式通常是欄位值加 1。</dd></div><div><dt>LPOL</dt><dd>Log Page Offset Lower，Get Log Page byte offset 的低 32 bits。</dd></div><div><dt>LPOU</dt><dd>Log Page Offset Upper，Get Log Page byte offset 的高 32 bits。</dd></div><div><dt>NUMD</dt><dd>Number of Dwords，0's-based transfer dword count；實際 bytes = (NUMD + 1) × 4。</dd></div><div><dt>UIDX</dt><dd>UUID Index，指向 UUID List 位置的 index；0 表示未指定 UUID。</dd></div><div><dt>CSI</dt><dd>I/O Command Set Identifier；選擇 I/O 命令集，NVM Command Set 使用 00h。</dd></div><div><dt>LSP</dt><dd>Log Specific Field，意義由所選 log page 定義的 command selector。</dd></div><div><dt>RAE</dt><dd>Retain Asynchronous Event，Get Log Page 是否保留相關 asynchronous event 的 selector。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13, 文件頁 213-216, PDF 頁 239-242</p></details>
<div class="table-wrap"><table><caption>LID 06h 的目前進度與歷史結果</caption><thead><tr><th scope="col">進度或歷史欄位</th><th scope="col">描述什麼資訊</th><th scope="col">何時可以使用這個欄位</th></tr></thead><tbody><tr><td>DSTOS/DSTCS</td><td>current state/progress</td><td>DSTOS=0 時忽略 percentage</td></tr><tr><td>DSTR=7h + SEGN</td><td>已知第一個 failed segment</td><td>其他 DSTR 忽略 SEGN</td></tr><tr><td>FVLD + FLBA</td><td>其中一個 failing LBA</td><td>不是所有失敗 LBA 清單</td></tr><tr><td>POH + STCT/STC</td><td>failure context</td><td>仍需 validity bits</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>DSTR</dt><dd>Device Self-test Result，結果 entry 中表示成功、abort 或 segment failure 的 nibble。</dd></div><div><dt>SEGN</dt><dd>Segment Number，只有 DSTR=7h 時指出第一個失敗 diagnostic segment。</dd></div><div><dt>POH</dt><dd>Power On Hours，self-test result 建立時累積的 power-on hours，不含指定 low-power 時間。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">完整 log 是 564 bytes=141 dwords，因此 NUMD=140=008Ch。LSP=0、RAE=0 時 CDW10=008C0006h。若 RDS1.DSTS=17h，high nibble 1h 表示 short test，low nibble 7h 表示已知 failed segment；此時才讀 SEGN。</span></p></aside>
</section>
<section id="spec-reading"><h2>接著打開 Spec 看什麼</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">以下按概念列出閱讀位置。報告時先用上面的流程說明問題，再打開對應章節看欄位與完整條件。中文教學 HTML 另有本篇全部圖表的逐圖重點、案例與細節。</span></p>
<div class="table-wrap"><table><thead><tr><th scope="col">要說明的觀念</th><th scope="col">Spec 閱讀位置</th></tr></thead><tbody><tr><td>Device Self-test 的啟動與執行</td><td>Base 2.4 §5.2.14.2.1, 8.1.8 · Base 2.4 §5.2.6</td></tr><tr><td>LID 06h 的目前進度與歷史結果</td><td>Base 2.4 §5.2.13 · Base 2.4 §5.2.13.1.7 · NVM 1.3 §4.1.4.3</td></tr></tbody></table></div>
<a class="reading-link" href="/DOCS/nvme-spec-report/base-device-self-test/tutorial-zh-tw.html">開啟完整中文教學與逐圖解釋 →</a></section>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:base-device-self-test-1 -->
<details class="review-question" id="qa-base-device-self-test-1"><summary>1. Device Self-test 啟動命令成功後，如何知道測試是否還在執行？</summary>
<div data-qa-answer="base-device-self-test-1"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">啟動 completion 不包含整個測試的最終結果。Device Self-test log 的 current operation 與 completion percentage 描述目前進度；結果紀錄則用於已結束的測試。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.6, 文件頁 201, PDF 頁 227</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 229-230, PDF 頁 255-256</p>
</details></details>
<!-- qa:base-device-self-test-2 -->
<details class="review-question" id="qa-base-device-self-test-2"><summary>2. Self-test result 中 FLBA 看起來是合理地址，就一定可以當作失敗位置嗎？</summary>
<div data-qa-answer="base-device-self-test-2"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">要先檢查對應的 validity bit；未宣告有效時不能依數值推論。即使有效，也可能只描述多個失敗 logical blocks 中的一個，並非完整範圍。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.7, 文件頁 231-232, PDF 頁 257-258</p>
<p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, 文件頁 76, PDF 頁 76</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express Base Specification, Revision 2.4</p><p>NVM Express NVM Command Set Specification, Revision 1.3</p></details></footer>
</div>
