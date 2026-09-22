---
permalink: /nvme/sq-associations-zh-tw/
layout: post
read_time: true
show_date: true
title: "NVMe SQ Associations：從儲存歸屬到 I/O 佇列分流"
date: 2026-09-22
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
[English]({% post_url 2026-09-22-nvme-sq-associations-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">主機知道每筆 I/O 要讀寫哪個 namespace，但控制器也需要知道：這個提交佇列預計服務哪一組儲存空間？SQ Associations 讓主機在建立佇列時提供這項提示。本文把儲存歸屬、佇列配置與命令分流接起來，說明提示何時有幫助，以及為什麼「命令完成」還不足以證明分流正確。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>SQ Associations</dt><dd>提交佇列關聯；建立 SQ 時，提示控制器這個佇列預計服務哪個 NVM Set。</dd></div><div><dt>namespace</dt><dd>主機以 NSID 指定的一份邏輯儲存空間。</dd></div><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div><div><dt>SQ</dt><dd>Submission Queue，提交佇列；主機放置待執行命令的記憶體佇列。</dd></div></dl>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>看懂三種關係</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">namespace 屬於哪個 NVM Set，SQ 關聯哪個 Set，完成結果送往哪個 CQ：這三種關係各回答不同問題，不能因為編號接近就混在一起。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NVM Set</dt><dd>在邏輯上與其他集合分開的一組非揮發性儲存，可包含多個 namespace。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div><div><dt>CQ</dt><dd>Completion Queue，完成佇列；控制器放置命令完成結果的記憶體佇列。</dd></div></dl></article>
<article><span class="axis-number">02</span><h3>確認提示的前提</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">先查控制器能力，再分清 Predictable Latency Mode 是否啟用、Set 目前處於哪種工作視窗。支援位元本身沒有提供固定的應用程式延遲上限。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Predictable Latency Mode</dt><dd>可預測延遲模式；以 NVM Set 為單位，在符合操作條件的工作視窗提供確定性讀寫延遲。</dd></div></dl></article>
<article><span class="axis-number">03</span><h3>把儲存清單接到建立命令</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">讀出 Set 的實際識別值及 namespace 歸屬，再放進 Create I/O SQ。清單索引、byte 位置與識別值各有用途，64 筆佇列也有自己的數量編碼。</span></p></article>
<article><span class="axis-number">04</span><h3>用每筆 I/O 檢查分流</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="04-01">04-01</span><span class="paragraph-text">從命令 NSID 找到 Set，再選已關聯該 Set 的 SQ。比較建立參數錯誤與後續送錯佇列，理解規格對兩者規定的不同後果。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NSID</dt><dd>Namespace Identifier；I/O 命令用來指定 namespace 的識別值。</dd></div></dl></article>
</div>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">預備知識是 OS、Computer Organization 與基本 SSD 概念。本文的 Set 7／9、SQ3／4／5、CQ2 與 namespace 編號均為說明性範例；能力與可用編號以裝置實際回覆為準。</span></p>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.03">00.03.</span><span class="paragraph-text">從「這筆 I/O 應送到哪個佇列」出發，先建立全貌，再逐步追蹤查詢、欄位與結果。</span></p>
<div class="overview-connections"><h3>把主軸連起來</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.04">00.04.</span><span class="paragraph-text">同一組例子貫穿本文：namespace A、B 在 Set 7，C 在 Set 9。主機讓 SQ3、SQ4 服務 Set 7，SQ5 服務 Set 9，而完成結果可以共用 CQ2。讀完應能說明每個編號從哪裡取得、填在哪裡，以及後續怎樣選對 SQ。</span></p>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.05">00.05.</span><span class="paragraph-text">SQ Associations 是配合 Predictable Latency Mode 的選用提示。提示是否受支援、提示是否正確、模式當下能提供什麼服務品質，需要分別確認。</span></p>
</div>
</section>
<section class="lesson" id="module-sqa-model"><h2 id="heading-sqa-model"><span class="section-number">01</span> 把佇列用途告訴控制器</h2>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 470" role="img"><title>儲存歸屬、工作提示、完成路徑各有一條關係</title><desc>由上往下追蹤。上層是 namespace 的儲存歸屬；中層表示主機為各 SQ 選擇相符的 Set；下層只表示完成結果匯入同一 CQ。這些連線不表示把 namespace 容量搬進主機佇列。來源：Base §3.2.2、§3.3、§5.3.2、§8.1.28。</desc><rect x="20" y="20" width="345" height="100" rx="6" class="v-object"/><text x="192.5" y="63.5" text-anchor="middle" font-size="17">NVM Set 7</text><text x="192.5" y="88.5" text-anchor="middle" font-size="17">A: NSID11 · B: NSID12</text><rect x="395" y="20" width="345" height="100" rx="6" class="v-object"/><text x="567.5" y="63.5" text-anchor="middle" font-size="17">NVM Set 9</text><text x="567.5" y="88.5" text-anchor="middle" font-size="17">C: NSID21</text><path d="M192,120 L192,190" class="v-line"/><path d="M188,183 L192,190 L196,183" class="v-line"/><path d="M567,120 L567,190" class="v-line"/><path d="M563,183 L567,190 L571,183" class="v-line"/><rect x="20" y="190" width="345" height="100" rx="6" class="v-command"/><text x="192.5" y="233.5" text-anchor="middle" font-size="17">SQ3 + SQ4</text><text x="192.5" y="258.5" text-anchor="middle" font-size="17">NVMSETID = 7</text><rect x="395" y="190" width="345" height="100" rx="6" class="v-command"/><text x="567.5" y="233.5" text-anchor="middle" font-size="17">SQ5</text><text x="567.5" y="258.5" text-anchor="middle" font-size="17">NVMSETID = 9</text><path d="M192,290 L192,360" class="v-line"/><path d="M188,353 L192,360 L196,353" class="v-line"/><path d="M567,290 L567,360" class="v-line"/><path d="M563,353 L567,360 L571,353" class="v-line"/><rect x="20" y="360" width="720" height="85" rx="6" class="v-success"/><text x="380.0" y="396.0" text-anchor="middle" font-size="17">CQ2</text><text x="380.0" y="421.0" text-anchor="middle" font-size="17">完成結果共用；Set 歸屬維持不變</text></svg></div><figcaption>由上往下追蹤。上層是 namespace 的儲存歸屬；中層表示主機為各 SQ 選擇相符的 Set；下層只表示完成結果匯入同一 CQ。這些連線不表示把 namespace 容量搬進主機佇列。來源：Base §3.2.2、§3.3、§5.3.2、§8.1.28。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>NVMSETID</dt><dd>NVM Set Identifier；Set 的 16-bit 識別值，和 SQ 編號、NSID 都不同。</dd></div></dl>
<!-- claim:SQA-MODEL -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">SQ Associations 讓主機在建立 I/O Submission Queue 時，提供該 SQ 對應的 NVM Set，作為控制器在 Predictable Latency Mode 下改善效能的提示。這是選用能力；Predictable Latency Mode 不依賴主機一定使用 SQ Associations。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.28</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.28, 文件頁 732-733, PDF 頁 758-759</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">說明性範例：Set 7 內有 namespace A、B，Set 9 內有 C。主機先安排 SQ3、SQ4 服務 Set 7，SQ5 服務 Set 9，再在建立各 SQ 時送入對應的 Set 編號。控制器因此知道這些佇列預期承載哪一組儲存空間的 I/O。</span></p></aside>
</section>
<section class="lesson" id="module-sqa-support"><h2 id="heading-sqa-support"><span class="section-number">02</span> 支援能力、模式狀態與工作視窗</h2>
<figure><figcaption><strong>同一個控制器，三種問題要分別回答</strong></figcaption><div class="table-wrap"><table><thead><tr><th scope="col">觀察到的資訊</th><th scope="col">足以說明什麼</th><th scope="col">還不能據此推出什麼</th></tr></thead><tbody><tr><td>CTRATT 三個 bit 為 1</td><td>控制器支援 SQA、NVM Sets、PLM</td><td>Set 7 現在已啟用模式</td></tr><tr><td>Set 7 已啟用模式</td><td>該 Set 使用模式的工作視窗規則</td><td>此刻必定在 DTWIN</td></tr><tr><td>Set 7 目前在 DTWIN</td><td>現在能在符合條件時提供確定性延遲</td><td>主機可無限增加工作量，或保證全部 PCIe 延遲</td></tr><tr><td>SQ3 已關聯 Set 7</td><td>控制器收到此 SQ 的預定用途</td><td>主機之後一定送對每筆 I/O</td></tr></tbody></table></div><figcaption>由支援走到實際效果，中間仍有設定、視窗及主機分流條件。來源：Base §8.1.28、§8.1.21、Figure 338。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>CTRATT</dt><dd>Controller Attributes；Identify Controller 中由多個能力 bit 組成的屬性欄位。</dd></div><div><dt>DTWIN</dt><dd>Deterministic Window；Set 可以提供確定性讀寫延遲的工作視窗。</dd></div><div><dt>PCIe</dt><dd>PCI Express，NVMe memory-based controller 使用的 transport 與裝置互連。</dd></div><div><dt>PLM</dt><dd>Predictable Latency Mode；CTRATT 中表示是否支援可預測延遲模式的 bit。</dd></div><div><dt>SQA</dt><dd>SQ Associations；CTRATT 中表示是否支援提交佇列關聯的 bit。</dd></div></dl>
<!-- claim:SQA-SUPPORT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">支援 SQ Associations 的控制器必須在 CTRATT 同時宣告 SQA、NVM Sets 與 Predictable Latency Mode 支援。這些支援位元不表示每個 Set 目前都已啟用模式，也不表示目前處於可提供確定性延遲的視窗。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.28</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.28, 文件頁 732-733, PDF 頁 758-759</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">只觀察相關三個 bit：SQA bit 8、PLM bit 5、NSETS bit 2 的遮罩合計為 0124h。用 (CTRATT &amp; 0124h)==0124h 檢查三者，不要求整個 CTRATT 恰好等於 0124h，因為控制器可能還有其他能力。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NSETS</dt><dd>NVM Sets；CTRATT 中表示是否支援 NVM 集合的 bit。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-sqa-inventory"><h2 id="heading-sqa-inventory"><span class="section-number">03</span> 先建立 namespace 到 Set 的對照</h2>
<figure><figcaption><strong>清單位置不是 Set 識別值</strong></figcaption><div class="table-wrap"><table><thead><tr><th scope="col">清單內的索引</th><th scope="col">整份清單的 byte 範圍</th><th scope="col">entry 內的 NSETID</th><th scope="col">建立 SQ 時使用</th></tr></thead><tbody><tr><td>0</td><td>128～255</td><td>7</td><td>CDW12=00000007h</td></tr><tr><td>1</td><td>256～383</td><td>9</td><td>CDW12=00000009h</td></tr></tbody></table></div><figcaption>說明性範例 NUMENT=2。先用位置找到資料，再從資料取識別值；不要把左邊的 0／1 或 128／256 填成 Set ID。來源：Base Figures 344／345／578。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>NSETID</dt><dd>NVM Set Identifier；NVM Set Attributes Entry 內對 Set 識別欄位使用的縮寫。</dd></div><div><dt>NUMENT</dt><dd>Number of Entries；這份清單中實際回傳的項目數。</dd></div><div><dt>entry</dt><dd>清單中的一筆資料；此處每筆 NVM Set Attributes Entry 為 128 bytes。</dd></div><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div></dl>
<!-- claim:SQA-INVENTORY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">主機需要兩份資訊：NVM Set List 說明控制器可存取哪些 Set，Identify Namespace 則說明指定 namespace 屬於哪個 Set。清單位置、NVM Set Identifier 與 NSID 是不同數值，不能用同一個編號代替。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.14.2.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.4, 文件頁 388-389, PDF 頁 414-415</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span><span class="paragraph-text">說明性範例：NUMENT=2，Entry 0 的 NSETID=7，Entry 1 的 NSETID=9；兩筆分別從 byte 128、256 開始。另查 NSID=11、12 得到 Set 7，查 NSID=21 得到 Set 9。路由表應保存這些實際值，不是把清單索引 0、1 當 Set 編號。</span></p></aside>
</section>
<section class="lesson" id="module-sqa-create"><h2 id="heading-sqa-create"><span class="section-number">04</span> 建立 SQ 時，同時指定 Set 與完成佇列</h2>
<figure><figcaption><strong>把 64-entry SQ3 的建立參數拆開檢查</strong></figcaption><div class="table-wrap"><table><thead><tr><th scope="col">命令位置</th><th scope="col">本例如何組成</th><th scope="col">送出的值</th></tr></thead><tbody><tr><td>CDW10</td><td>高 16 bits：64−1=63；低 16 bits：QID3</td><td>003F0003h</td></tr><tr><td>CDW11</td><td>高 16 bits：CQID2；PC=1；QPRIO=0</td><td>00020001h</td></tr><tr><td>CDW12</td><td>低 16 bits：Set 7；高 16 bits 保留</td><td>00000007h</td></tr><tr><td>PRP1</td><td>4 KiB 對齊、已配置的連續主機記憶體</td><td>0000000000100000h</td></tr></tbody></table></div><figcaption>前提：CQ2 已建立，Set 7 可用且支援 SQA，控制器已初始化且支援此佇列深度；採 round robin，所以 QPRIO 被忽略。來源：Base §5.3.2、Figures 575～578。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>round robin</dt><dd>輪詢仲裁；輪流從佇列選取待處理命令，本例不使用加權優先級。</dd></div><div><dt>QPRIO</dt><dd>Queue Priority；僅在指定的加權輪詢仲裁機制下使用的 SQ 優先級。</dd></div><div><dt>PRP1</dt><dd>PRP Entry 1；本命令依 PC 選擇存放 SQ 基底位址或 PRP List 位址。</dd></div><div><dt>PC</dt><dd>Physically Contiguous；1 表示 SQ 的記憶體實體連續，0 表示用頁面清單描述。</dd></div></dl>
<!-- claim:SQA-CREATE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">Create I/O Submission Queue 的 CDW12.NVMSETID 建立 SQ 與 Set 的關聯；CDW11.CQID 則指定完成結果送往哪個 CQ。兩個欄位用途不同。NVMSETID=0 或不支援 SQA 時不建立特定 Set 關聯；SQA 支援時指定清單外的非零 Set，命令必須以 Invalid Field in Command 中止。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CQID</dt><dd>Completion Queue Identifier；這個 SQ 的完成項目要送往哪個 CQ。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.3.2, 文件頁 529-531, PDF 頁 555-557</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">說明性範例：CQ2 已建立且裝置支援所需深度，建立 64 筆的 SQ3，關聯 Set 7，採實體連續記憶體與 round-robin 仲裁：CDW10=003F0003h、CDW11=00020001h、CDW12=00000007h。若每個 SQE 為 64 bytes，64 筆需 4096 bytes。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>SQE</dt><dd>Submission Queue Entry；SQ 內的一個命令項目。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-sqa-routing"><h2 id="heading-sqa-routing"><span class="section-number">05</span> 讓每筆 I/O 的 Set 與 SQ 關聯一致</h2>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 430" role="img"><title>以命令的 NSID 選 SQ，而不是以 CQID 選儲存空間</title><desc>本例只追蹤 NSID21。SQ3 即使較空，也不符合 Set 9 的提示；兩個 SQ 共用 CQ2 不會改變這個判斷。來源：Base §8.1.28、Figures 346／578。</desc><rect x="20" y="20" width="720" height="70" rx="6" class="v-object"/><text x="380.0" y="61.0" text-anchor="middle" font-size="17">I/O · NSID21</text><path d="M380,90 L380,145" class="v-line"/><path d="M376,138 L380,145 L384,138" class="v-line"/><rect x="20" y="145" width="720" height="85" rx="6" class="v-command"/><text x="380.0" y="181.0" text-anchor="middle" font-size="17">Identify namespace → NVMSETID = 9</text><text x="380.0" y="206.0" text-anchor="middle" font-size="17">先確認資料對象的儲存歸屬</text><path d="M190,230 L190,295" class="v-line"/><path d="M186,288 L190,295 L194,288" class="v-line"/><path d="M565,230 L565,295" class="v-line"/><path d="M561,288 L565,295 L569,288" class="v-line"/><rect x="20" y="295" width="345" height="105" rx="6" class="v-success"/><text x="192.5" y="341.0" text-anchor="middle" font-size="17">SQ5 → Set 9</text><text x="192.5" y="366.0" text-anchor="middle" font-size="17">相符：使用 SQ5</text><rect x="395" y="295" width="345" height="105" rx="6" class="v-decision"/><text x="567.5" y="341.0" text-anchor="middle" font-size="17">SQ3 → Set 7</text><text x="567.5" y="366.0" text-anchor="middle" font-size="17">不符：不要選 SQ3</text></svg></div><figcaption>本例只追蹤 NSID21。SQ3 即使較空，也不符合 Set 9 的提示；兩個 SQ 共用 CQ2 不會改變這個判斷。來源：Base §8.1.28、Figures 346／578。</figcaption></figure>

<!-- claim:SQA-ROUTING -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span><span class="paragraph-text">要取得 SQ Associations 的效益，主機必須把每個 I/O SQ 關聯到某個 NVM Set，並只把命令送入與該命令 NSID 所屬 Set 相符的 SQ。不遵守操作規則可能影響 Predictable Latency；這不是一個由本節定義的強制拒絕其他 Set 命令的存取保護機制。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.28</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.28, 文件頁 733, PDF 頁 759</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="05.02">05.02.</span><span class="paragraph-text">已知 NSID11／12→Set7、NSID21→Set9，且 SQ3／SQ4→Set7、SQ5→Set9。NSID11 可以選 SQ3 或 SQ4；NSID21 應選 SQ5。即使三個 SQ 都把完成項目送往 CQ2，也不會改變這個分流判斷。</span></p></aside>
</section>
<section id="spec-reading"><section id="spec-route"><h2>開著 Spec 的順向報告路徑</h2>
<p class="reader-paragraph"><span class="paragraph-number figure-paragraph-number" aria-label="R-1">R-1</span><span class="paragraph-text">先用本文的全貌與案例說明機制，再按下列 Base PDF 檢視器頁碼往後讀。共用頁從指定標題開始，在停止標題前結束；必要背景已在中文教學說明，不必為每個引用往返翻頁。</span></p>
<div class="table-wrap"><table><thead><tr><th scope="col">頁碼順序</th><th scope="col">章節起點</th><th scope="col">重點與停止位置</th></tr></thead><tbody><tr><td>R1 · Base PDF 363–365</td><td>§5.2.14</td><td>只讀 Figures 333／334 的 CNS 與 CNSSID，再用 Figure 336 的 01h／04h／08h 三列說明三種查詢；到表格註腳即停止，不展開其他 CNS。 在 §5.2.14.1 前停止。</td></tr><tr><td>R2 · Base PDF 370–372</td><td>§5.2.14.2.1</td><td>在 Figure 338 只找 bytes 99:96 的 CTRATT，讀 SQA bit 8、PLM bit 5、NSETS bit 2。讀完這三個 bit 就停止，不讀完整 Identify Controller 表。 在 §5.2.14.2.2 前停止。</td></tr><tr><td>R3 · Base PDF 414–415</td><td>§5.2.14.2.4</td><td>從 NVM Set List 標題起，用兩筆 Set 7／9 說明起始 ID、NUMENT 與 entry；分清 128-byte 步距和實際 Set ID。 在 §5.2.14.2.5 前停止。</td></tr><tr><td>R4 · Base PDF 416–419</td><td>§5.2.14.2.8</td><td>先確認 active NSID 的回覆條件，再直接在 Figure 346 找 bytes 11:10 的 NVMSETID 與相鄰 ENDGID；讀完歸屬欄即停止。 在 §5.2.14.2.9 前停止。</td></tr><tr><td>R5 · Base PDF 555–557</td><td>§5.3.2</td><td>以 SQ3、CQ2、Set 7 串起 Figures 575～579；重點在 CDW12 與 CDW11 不同用途，以及非法 Set 的建立結果。 在 §5.3.3 前停止。</td></tr><tr><td>R6 · Base PDF 708–709</td><td>§8.1.21</td><td>只補模式開頭、Figure 751 與 §8.1.21.1 的操作條件；在 Figure 752 前停止。視窗名稱與模式啟用分開，不展開完整模式設定。 在 §8.1.21.2 前停止。</td></tr><tr><td>R7 · Base PDF 758–759</td><td>§8.1.28</td><td>從 Submission Queue (SQ) Associations 標題開始，最後完整講主範圍：選用提示、支援前提、建立時關聯，以及兩項主機分流規則。 在 §8.1.29 前停止。</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>CNSSID</dt><dd>CNS Specific Identifier；用途由 CNS 選項決定的識別欄位。</dd></div><div><dt>ENDGID</dt><dd>Endurance Group Identifier；Set 或 namespace 所屬耐用度群組的識別值。</dd></div><div><dt>CNS</dt><dd>Controller or Namespace Structure；Identify 用來選擇回覆哪種資料的欄位。</dd></div></dl>
</section></section>
<a class="reading-link" href="/DOCS/nvme-spec-report/base-sq-associations/tutorial-zh-tw.html">開啟完整中文教學與逐圖解釋 →</a>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:sqa-support -->
<details class="review-question" id="qa-sqa-support"><summary>1. CTRATT 的三個相關 bit 都是 1，能否直接保證下一筆 Read 的完成時間？</summary>
<div data-qa-answer="sqa-support"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.01">07.01.</span><span class="paragraph-text">不能。它們只表示支援能力。還要確認目標 Set 的模式已啟用、目前的工作視窗與操作限制；而服務品質描述也不包括 PCIe 連線的全部延遲。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.28, 文件頁 732-733, PDF 頁 758-759</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.21, 文件頁 682-683, PDF 頁 708-709</p>
</details></details>
<!-- qa:sqa-list -->
<details class="review-question" id="qa-sqa-list"><summary>2. 清單 Entry 1 的 NSETID=9，建立 SQ 時填 1、256，還是 9？</summary>
<div data-qa-answer="sqa-list"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.02">07.02.</span><span class="paragraph-text">填 9。1 是索引；256 是該筆相對整份清單起點的 byte 位置；9 才是要填入 CDW12 的 Set 識別值。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.4, 文件頁 388-389, PDF 頁 414-415</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.3.2, 文件頁 529-531, PDF 頁 555-557</p>
</details></details>
<!-- qa:sqa-route -->
<details class="review-question" id="qa-sqa-route"><summary>3. NSID21 屬於 Set 9，SQ3 與 SQ5 都使用 CQ2，是否可以任選一個 SQ？</summary>
<div data-qa-answer="sqa-route"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.03">07.03.</span><span class="paragraph-text">依本例應選關聯 Set 9 的 SQ5。共用 CQ 只代表完成結果送到相同地方，不能改變 SQ3 關聯 Set 7 的事實。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.28, 文件頁 733, PDF 頁 759</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §3.3, 文件頁 88, PDF 頁 114</p>
</details></details>
<!-- qa:sqa-zero -->
<details class="review-question" id="qa-sqa-zero"><summary>4. 把 NVMSETID 設為 0，是建立通往所有 Set 的共同提示嗎？</summary>
<div data-qa-answer="sqa-zero"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.04">07.04.</span><span class="paragraph-text">不是。Create I/O SQ 把 0 定義為沒有特定 Set 關聯；它不能滿足本篇「先建立關聯，再按 Set 分流」的提示使用方式。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.3.2, 文件頁 529-531, PDF 頁 555-557</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.28, 文件頁 733, PDF 頁 759</p>
</details></details>
<!-- qa:sqa-errors -->
<details class="review-question" id="qa-sqa-errors"><summary>5. Set 9 的命令送到關聯 Set 7 的 SQ，而且成功完成，是否表示主機使用正確？</summary>
<div data-qa-answer="sqa-errors"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.05">07.05.</span><span class="paragraph-text">不表示。送錯 SQ 違反分流規則，可能影響可預測延遲；§8.1.28 沒有要求每次都用錯誤碼拒絕。這與建立 SQ 時填入清單外非零 Set、必須回 Invalid Field in Command 的規則不同。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.28, 文件頁 733, PDF 頁 759</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.3.2, 文件頁 529-531, PDF 頁 555-557</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
