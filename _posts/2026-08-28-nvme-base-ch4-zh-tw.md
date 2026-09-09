---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4 第 4 章：SQE、CQE、Status、PRP 與 SGL"
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
[English]({% post_url 2026-08-28-nvme-base-ch4-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">一筆 NVMe 命令必須告訴控制器要做什麼、對哪個 namespace 操作，以及資料放在哪裡；完成結果則必須讓主機認出是哪筆命令、結果如何。本篇從這兩個方向拆解 SQE、CQE 與 PRP／SGL。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div><div><dt>NVMe</dt><dd>Non-Volatile Memory Express，主機與非揮發性記憶體子系統之間的介面規範家族。</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div><div><dt>PRP</dt><dd>Physical Region Page，以 memory page 為單位描述 host-addressable data buffer 的 pointer 格式。</dd></div><div><dt>SGL</dt><dd>Scatter Gather List，以 descriptor 與 segment 描述一段或多段 data buffer 的格式。</dd></div><div><dt>SQE</dt><dd>Submission Queue Entry，SQ 中的一筆命令資料結構。</dd></div></dl>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>命令內容 SQE</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">理解命令識別、操作碼與資料指標的分工。</span></p></article>
<article><span class="axis-number">02</span><h3>完成結果 CQE</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">分開理解新完成項目、命令身分與狀態碼。</span></p></article>
<article><span class="axis-number">03</span><h3>資料位址 PRP／SGL</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">把作業系統的記憶體頁面概念接到 NVMe 資料傳輸。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express，主機與非揮發性記憶體子系統之間的介面規範家族。</dd></div></dl></article>
<article><span class="axis-number">04</span><h3>其他共用資料結構</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="04-01">04-01</span><span class="paragraph-text">理解功能值、識別碼、清單與文字的表示方式。</span></p></article>
</div>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">命令與完成項目是佇列中的記錄，讀寫的資料通常由資料指標指定。先分清楚「命令記錄」與「命令要搬移的資料」，就能理解後面的欄位配置。</span></p>
<div class="overview-connections"><h3>把主軸連起來</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.03">00.03.</span><span class="paragraph-text">把一次操作拆成三份資訊：SQE 說明主機要做什麼，PRP／SGL 描述資料在哪裡，CQE 回報是哪筆命令完成及其結果。識別碼與清單則協助主機選擇正確對象。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div><div><dt>PRP</dt><dd>Physical Region Page，以 memory page 為單位描述 host-addressable data buffer 的 pointer 格式。</dd></div><div><dt>SGL</dt><dd>Scatter Gather List，以 descriptor 與 segment 描述一段或多段 data buffer 的格式。</dd></div><div><dt>SQE</dt><dd>Submission Queue Entry，SQ 中的一筆命令資料結構。</dd></div></dl>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.04">00.04.</span><span class="paragraph-text">本篇由共同布局逐步深入位元、長度與指標。讀完應能從一個命令範圍算出資料量，選擇正確的指標解讀方式，再利用完成項目找回原命令。每次計算都要先確認單位，而不是只憑欄位名稱推測。</span></p>
</div>
</section>
<section class="lesson" id="module-sqe"><h2 id="heading-sqe"><span class="section-number">01</span> SQE 的共用格式與命令欄位</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">Common SQE 先固定 CDW0、NSID、metadata/data pointer 與 CDW10-15 的位置。OPC 選 command，CID 建立完成關聯，PSDT 決定 DPTR 解讀方式；只有完成這些 common 欄位後，才應進入個別 command 的 CDW10-15 定義。Figures 92-94 是後續所有 command construction 的座標系。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>metadata</dt><dd>隨 logical block 儲存的附加資料，可包含資料保護資訊，也可有其他用途。</dd></div><div><dt>DPTR</dt><dd>Data Pointer，SQE 中指出 command data buffer 的欄位。</dd></div><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div><div><dt>PSDT</dt><dd>PRP or SGL for Data Transfer，CDW0 中決定 DPTR 應按 PRP 或 SGL 解讀的欄位。</dd></div><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div><div><dt>CID</dt><dd>Command Identifier，與 SQ identifier 合用以辨識 outstanding command。</dd></div></dl>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 160" role="img"><title>CDW0 · 32 bits</title><desc>CDW0 把命令識別、資料指標類型、融合操作與操作碼放在同一個 Dword。欄位寬度以標示的 bit 範圍為準，圖塊為閱讀需要調整。</desc><rect x="20" y="35" width="300" height="85" rx="6" class="v-object"/><text x="170.0" y="71.0" text-anchor="middle" font-size="17">CID</text><text x="170.0" y="96.0" text-anchor="middle" font-size="17">31:16</text><rect x="320" y="35" width="90" height="85" rx="6" class="v-command"/><text x="365.0" y="71.0" text-anchor="middle" font-size="17">PSDT</text><text x="365.0" y="96.0" text-anchor="middle" font-size="17">15:14</text><rect x="410" y="35" width="130" height="85" rx="6" class="v-decision"/><text x="475.0" y="71.0" text-anchor="middle" font-size="17">Reserved</text><text x="475.0" y="96.0" text-anchor="middle" font-size="17">13:10</text><rect x="540" y="35" width="90" height="85" rx="6" class="v-command"/><text x="585.0" y="71.0" text-anchor="middle" font-size="17">FUSE</text><text x="585.0" y="96.0" text-anchor="middle" font-size="17">9:8</text><rect x="630" y="35" width="110" height="85" rx="6" class="v-success"/><text x="685.0" y="71.0" text-anchor="middle" font-size="17">OPC</text><text x="685.0" y="96.0" text-anchor="middle" font-size="17">7:0</text></svg></div><figcaption>CDW0 把命令識別、資料指標類型、融合操作與操作碼放在同一個 Dword。欄位寬度以標示的 bit 範圍為準，圖塊為閱讀需要調整。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>Dword</dt><dd>Dword（Double word）；32 bits，也就是 4 bytes。對比 word=16 bits；例如 zero-based dword count=3 代表 4 個 Dwords，也就是 16 bytes。</dd></div><div><dt>PSDT</dt><dd>PRP or SGL for Data Transfer，CDW0 中決定 DPTR 應按 PRP 或 SGL 解讀的欄位。</dd></div><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div><div><dt>CID</dt><dd>Command Identifier，與 SQ identifier 合用以辨識 outstanding command。</dd></div></dl>
<details class="technical-note"><summary>完整規則：SQE 的共用格式與命令欄位</summary>
<!-- claim:BASE4-SQE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">Admin 與 I/O common SQE 固定為 64 bytes。CDW0、NSID、data pointer 與 CDW10-15 的通用位置先固定，再由各 command 定義命令專屬內容。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 文件頁 139-143, PDF 頁 165-169</p></details>
<!-- claim:BASE4-CID -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">CID 與 Submission Queue identifier 的組合用來唯一識別 command；FFFFh 宜（should）避免使用，因 Error Information log 以該值表示錯誤未對應特定 command。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 文件頁 140, PDF 頁 166</p></details>
<!-- claim:BASE4-PSDT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.04">01.04.</span><span class="paragraph-text">CDW0.PSDT 決定 DPTR 解讀為 PRP 或 SGL。NVMe over PCIe 的 Admin command 原則上必須（shall）使用 PRP，除非 command 定義另有規定。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div><div><dt>DPTR</dt><dd>Data Pointer，SQE 中指出 command data buffer 的欄位。</dd></div><div><dt>PCIe</dt><dd>PCI Express，NVMe memory-based controller 使用的 transport 與裝置互連。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 文件頁 140-142, PDF 頁 166-168</p></details>
</details>
<div class="table-wrap"><table><caption>SQE 的共用格式與命令欄位</caption><thead><tr><th scope="col">SQE 區域</th><th scope="col">主機在這裡描述什麼</th><th scope="col">如何選擇正確的欄位定義</th></tr></thead><tbody><tr><td>CDW0</td><td>命令身分 與 資料指標選擇欄位</td><td>所有 commands 共用</td></tr><tr><td>NSID</td><td>指定的 namespace 範圍</td><td>不用時必須依 command 定義清零或使用特殊值</td></tr><tr><td>MPTR/DPTR</td><td>metadata 與 data buffer</td><td>由 PSDT 與 command 規則決定</td></tr><tr><td>CDW10-15</td><td>命令專用參數</td><td>不能跨 command 借用語意</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div><div><dt>metadata</dt><dd>隨 logical block 儲存的附加資料，可包含資料保護資訊，也可有其他用途。</dd></div><div><dt>MPTR</dt><dd>Metadata Pointer，SQE 中指出獨立 metadata buffer 的欄位。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.05">01.05.</span><span class="paragraph-text">說明性範例：同一個 CID 可以在不同 SQ 使用，但同一 SQ 內 outstanding command 不可用相同 CID 造成識別衝突。driver 建 SQE 時以 (SQID,CID) 建 tracking key，填完全部欄位並完成必要 memory ordering 後才更新 SQ tail。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>SQID</dt><dd>Submission Queue Identifier，辨識 command 所屬 SQ 的數值。</dd></div><div><dt>SQ</dt><dd>Submission Queue，主機放入命令的提交佇列。</dd></div></dl></aside>
<a class="reading-link" href="#reading-sqe">閱讀相關規格圖表 → SQE 的共用格式與命令欄位</a>
</section>
<section class="lesson" id="module-cqe-status"><h2 id="heading-cqe-status"><span class="section-number">02</span> CQE：新完成項目、命令識別與結果</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">host 先用 Phase Tag 判斷 CQ slot 是否是新 completion；確定 ownership 後再用 SQID/CID 找回 command，最後以 SCT 選 status 類別並解 SC、DNR、CRD。Figures 97-109 必須按這個順序讀，否則 stale CQE 或錯誤類別會被當成真實 command failure。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div><div><dt>SQID</dt><dd>Submission Queue Identifier，辨識 command 所屬 SQ 的數值。</dd></div><div><dt>CRD</dt><dd>Command Retry Delay，status 中選擇 controller 建議重試延遲值的欄位。</dd></div><div><dt>DNR</dt><dd>Do Not Retry，CQE status 中提示以相同 command 重試預期不會成功的 bit。</dd></div><div><dt>SCT</dt><dd>Status Code Type；指定完成狀態碼所屬類別，需與 SC 一起解讀。</dd></div><div><dt>CQ</dt><dd>Completion Queue，controller 放入完成結果的完成佇列。</dd></div><div><dt>SC</dt><dd>Status Code；指定所選 SCT 類別中的完成結果。</dd></div></dl>
<details class="technical-note"><summary>完整規則：CQE：新完成項目、命令識別與結果</summary>
<!-- claim:BASE4-CQE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">common CQE 至少 16 bytes；若以多次寫入建立 CQE，Phase Tag 必須（shall）在最後一次寫入更新，避免 host 看到半成品。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, 文件頁 144-145, PDF 頁 170-171</p></details>
<!-- claim:BASE4-STATUS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">status 要先解 Status Code Type（SCT），再解 Status Code（SC），同時檢查 Do Not Retry（DNR）等控制 bit；數值不能脫離 SCT 單獨解讀。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>DNR</dt><dd>Do Not Retry，CQE status 中提示以相同 command 重試預期不會成功的 bit。</dd></div><div><dt>SCT</dt><dd>Status Code Type；指定完成狀態碼所屬類別，需與 SC 一起解讀。</dd></div><div><dt>SC</dt><dd>Status Code；指定所選 SCT 類別中的完成結果。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, 文件頁 145-155, PDF 頁 171-181</p></details>
<!-- claim:BASE4-PHASE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.04">02.04.</span><span class="paragraph-text">Phase Tag 讓 host 判斷環形 Completion Queue slot 是否為新完成項目；host 消費 CQE 後推進 CQ head doorbell，wrap 時預期 phase 翻轉。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CQ</dt><dd>Completion Queue，controller 放入完成結果的完成佇列。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.2.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.4, 文件頁 155-158, PDF 頁 181-184</p></details>
</details>
<div class="table-wrap"><table><caption>CQE：新完成項目、命令識別與結果</caption><thead><tr><th scope="col">完成狀態欄位</th><th scope="col">回答哪個問題</th><th scope="col">解讀時還需哪些資訊</th></tr></thead><tbody><tr><td>SCT</td><td>status 大類</td><td>一定先解</td></tr><tr><td>SC</td><td>類別內具體結果</td><td>不能脫離 SCT</td></tr><tr><td>DNR</td><td>同 command 重試預期</td><td>不是永久硬體故障的同義詞</td></tr><tr><td>CRD</td><td>建議 retry delay selector</td><td>只有適用 status 才使用</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>CRD</dt><dd>Command Retry Delay，status 中選擇 controller 建議重試延遲值的欄位。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.05">02.05.</span><span class="paragraph-text">說明性範例：SC 數值 02h 在不同 SCT 下可能屬於不同 status 表。正確 log 應保存完整 status field，再輸出 P、SCT、SC、DNR、CRD 與原始 16-bit value。只印『SC=2』不足以決定 recovery。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>P</dt><dd>Phase Tag，讓 host 判斷 CQ slot 是否包含新 completion 的翻轉 bit。</dd></div></dl></aside>
<a class="reading-link" href="#reading-cqe-status">閱讀相關規格圖表 → CQE：新完成項目、命令識別與結果</a>
</section>
<section class="lesson" id="module-prp"><h2 id="heading-prp"><span class="section-number">03</span> PRP 如何描述跨頁資料</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">PRP1 可以指向第一個 memory page 內任意 byte，能承載的第一段長度是 page_size - offset。若資料跨過第一頁，PRP2 依剩餘長度代表第二頁或 PRP List；後續 page address 必須符合 page alignment。Figures 110-113 是 address calculation，不只是 pointer 名稱表。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>offset</dt><dd>offset；從指定起點算出的位移。它回答「離起點多遠」，不等於 index。</dd></div></dl>
<details class="technical-note"><summary>完整規則：PRP 如何描述跨頁資料</summary>
<!-- claim:BASE4-PRP -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span><span class="paragraph-text">PRP 以固定大小 entry 指向 physical memory page。第一個 entry 可含 page offset；後續 PRP 必須（shall）符合 page alignment，資料長度決定需要幾個 entry。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>page offset</dt><dd>page offset；資料在第一個記憶體 page 內的起始位移；跨過 page boundary 後，位置由下一個 page pointer 決定。</dd></div><div><dt>offset</dt><dd>offset；從指定起點算出的位移。它回答「離起點多遠」，不等於 index。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, 文件頁 158-159, PDF 頁 184-185</p></details>
</details>
<div class="table-wrap"><table><caption>PRP 如何描述跨頁資料</caption><thead><tr><th scope="col">資料跨頁情況</th><th scope="col">PRP2 的解讀方式</th><th scope="col">指標與對齊要求</th></tr></thead><tbody><tr><td>資料不跨第一頁</td><td>只需 PRP1</td><td>PRP2 不承載下一段</td></tr><tr><td>剩餘資料只需一頁</td><td>PRP2 指第二個 data page</td><td>address page-aligned</td></tr><tr><td>剩餘資料超過一頁</td><td>PRP2 指 PRP List</td><td>list entries 再指 data pages</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.03">03.03.</span><span class="paragraph-text">若 PRP1 的 page offset 是 512 bytes，第一頁只承載從 512 bytes 開始的資料；跨過 page boundary 後，下一段位置由下一個 page pointer 指定，不是把同一個實體位址繼續加上去。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>page offset</dt><dd>page offset；資料在第一個記憶體 page 內的起始位移；跨過 page boundary 後，位置由下一個 page pointer 決定。</dd></div></dl></aside>
<a class="reading-link" href="#reading-prp">閱讀相關規格圖表 → PRP 如何描述跨頁資料</a>
</section>
<section class="lesson" id="module-sgl"><h2 id="heading-sgl"><span class="section-number">04</span> SGL 的資料與串接描述子</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">SGL descriptor 同時包含 type/subtype、address 與 length；Data Block 指向資料，Segment／Last Segment 指向更多 descriptors，Bit Bucket 表示資料不需實際放入 memory。Figures 114-125 應先讀 type，再讀該 type 對 address/length 的語意，不能只沿 address 盲走。</span></p>
<details class="technical-note"><summary>完整規則：SGL 的資料與串接描述子</summary>
<!-- claim:BASE4-SGL -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">SGL 由一個以上 descriptor／segment 描述資料 buffer。SGL length 必須（shall）大於等於 requested transfer length；本報告只介紹 PCIe 可用的通用 descriptor。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>PCIe</dt><dd>PCI Express，NVMe memory-based controller 使用的 transport 與裝置互連。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, 文件頁 159-166, PDF 頁 185-192</p></details>
</details>
<div class="table-wrap"><table><caption>SGL 的資料與串接描述子</caption><thead><tr><th scope="col">指標或描述子種類</th><th scope="col">位址與長度描述什麼</th><th scope="col">沿指標會找到什麼</th></tr></thead><tbody><tr><td>PRP</td><td>以記憶體頁描述位址</td><td>第一頁 offset + 後續 page alignment</td></tr><tr><td>SGL Data Block</td><td>起始位址與資料長度（bytes）</td><td>資料區段可用 descriptor 表示</td></tr><tr><td>SGL Segment</td><td>清單位址與清單長度（bytes）</td><td>指向下一層 descriptors，不是 data</td></tr><tr><td>Bit Bucket</td><td>只消耗 transfer length</td><td>不代表可讀寫的 memory buffer</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.03">04.03.</span><span class="paragraph-text">一筆 12 KiB 的資料傳輸，可以由 2 個 Data Block descriptors 描述 8 KiB 與 4 KiB。若 descriptor 類型是 Segment，它的 length 則描述下一段 descriptor list 的大小，並非使用者資料的大小。</span></p></aside>
<a class="reading-link" href="#reading-sgl">閱讀相關規格圖表 → SGL 的資料與串接描述子</a>
</section>
<section class="lesson" id="module-identity-text"><h2 id="heading-identity-text"><span class="section-number">05</span> Feature 值、識別碼、清單與字串</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span><span class="paragraph-text">解讀數值前要先確定它代表什麼：Feature 值具有目前與保存狀態的差別；identifier 具有識別範圍；清單與字串則各有排列及長度規則。</span></p>
<details class="technical-note"><summary>完整規則：Feature 值、識別碼、清單與字串</summary>
<!-- claim:BASE4-FEATURE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.02">05.02.</span><span class="paragraph-text">Feature 可能具有 default、saved、目前值；保存值 支援與跨 reset／power cycle 的 persistence 由 SSFS 與各 Feature capability 判定。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.4, 文件頁 166-169, PDF 頁 192-195</p></details>
<!-- claim:BASE4-IDENTIFIER -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.03">05.03.</span><span class="paragraph-text">VID／SSVID、SN／MN、IEEE OUI、EUI64、NGUID 與 UUID 的來源、長度與唯一性範圍不同；不能只因外觀相似就互換。此節為 informative。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>EUI64</dt><dd>64-bit Extended Unique Identifier，使用 IEEE 配置空間建立的 64-bit identifier。</dd></div><div><dt>NGUID</dt><dd>Namespace Globally Unique Identifier，namespace 的 128-bit 全域識別值。</dd></div><div><dt>SSVID</dt><dd>Subsystem Vendor ID，辨識 subsystem vendor 的 PCI identifier。</dd></div><div><dt>UUID</dt><dd>Universally Unique Identifier，128-bit identifier；其實際關聯範圍仍由使用它的資料結構決定。</dd></div><div><dt>OUI</dt><dd>Organizationally Unique Identifier，由 IEEE 配置給組織的 identifier 前綴。</dd></div><div><dt>VID</dt><dd>Vendor ID，由 PCI-SIG 配置、辨識 vendor 的 identifier。</dd></div><div><dt>MN</dt><dd>Model Number，辨識產品型號的字串。</dd></div><div><dt>SN</dt><dd>Serial Number，辨識一個產品實例的序號字串。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.5, 文件頁 169-172, PDF 頁 195-198</p></details>
<!-- claim:BASE4-LISTS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.04">05.04.</span><span class="paragraph-text">Controller List 先以 NUMCIDS 指定數量，再依遞增順序排列最多 2047 個 16-bit controller identifiers。Namespace List 沒有數量 header，直接依遞增順序排列 32-bit NSIDs；兩種清單未使用的 entries 都填 0。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div><div><dt>NUMCIDS</dt><dd>Number of Controller Identifiers；Controller List 中有效 controller IDs 的數量。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.6, 文件頁 172-173, PDF 頁 198-199</p></details>
<!-- claim:BASE4-UTF8 -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.05">05.05.</span><span class="paragraph-text">處理 UTF-8 輸入時要依規格流程驗證編碼、禁止的 code point 與截斷情況；不可把任意 byte sequence 當成有效字串。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>UTF-8</dt><dd>Unicode Transformation Format - 8-bit，以一到四個 bytes 編碼 Unicode code point 的文字格式。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.8</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.8, 文件頁 175, PDF 頁 201</p></details>
</details>
<div class="table-wrap"><table><caption>Feature 值、識別碼、清單與字串</caption><thead><tr><th scope="col">識別欄位或清單</th><th scope="col">辨認的對象與格式</th><th scope="col">長度及數量如何解讀</th></tr></thead><tbody><tr><td>VID／SSVID</td><td>廠商與 subsystem 廠商識別值</td><td>按各自欄位辨認對象</td></tr><tr><td>SN／MN</td><td>產品序號與型號字串</td><td>依固定欄位長度與填補規則閱讀</td></tr><tr><td>EUI64／NGUID／UUID</td><td>不同格式的物件識別值</td><td>長度及身分範圍不能互換</td></tr><tr><td>Controller List</td><td>NUMCIDS 加上 16-bit IDs</td><td>有明確數量欄位</td></tr><tr><td>Namespace List</td><td>直接排列 32-bit NSIDs</td><td>沒有 Controller List 的數量標頭</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>NUMCIDS</dt><dd>Number of Controller Identifiers；Controller List 中有效 controller IDs 的數量。</dd></div><div><dt>EUI64</dt><dd>64-bit Extended Unique Identifier，使用 IEEE 配置空間建立的 64-bit identifier。</dd></div><div><dt>NGUID</dt><dd>Namespace Globally Unique Identifier，namespace 的 128-bit 全域識別值。</dd></div><div><dt>SSVID</dt><dd>Subsystem Vendor ID，辨識 subsystem vendor 的 PCI identifier。</dd></div><div><dt>UUID</dt><dd>Universally Unique Identifier，128-bit identifier；其實際關聯範圍仍由使用它的資料結構決定。</dd></div><div><dt>VID</dt><dd>Vendor ID，由 PCI-SIG 配置、辨識 vendor 的 identifier。</dd></div><div><dt>MN</dt><dd>Model Number，辨識產品型號的字串。</dd></div><div><dt>SN</dt><dd>Serial Number，辨識一個產品實例的序號字串。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="05.06">05.06.</span><span class="paragraph-text">含 3 個 controllers 的清單以 NUMCIDS=3 開始，後接 3 個 16-bit IDs。含 3 個 namespaces 的清單則直接從第 1 個 32-bit NSID 開始。UTF-8 字串的 byte 數也不等於字元數，例如「中」占 3 bytes。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>UTF-8</dt><dd>Unicode Transformation Format - 8-bit，以一到四個 bytes 編碼 Unicode code point 的文字格式。</dd></div></dl></aside>
<a class="reading-link" href="#reading-identity-text">閱讀相關規格圖表 → Feature 值、識別碼、清單與字串</a>
</section>
<details class="figure-reading-fold"><summary>展開圖表教學：依主軸閱讀來源圖表</summary>
<section id="figure-reading"><h2><span class="section-number">06</span> 讀懂本篇的規格圖表</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.01">06.01.</span><span class="paragraph-text">以下依概念整理規格中的圖表。每組先說明讀取順序與要判斷的問題，接著列出各圖的欄位或行為說明。可以由正文的連結跳到對應組別，也可以用這一節檢查自己能否把欄位連回完整操作。</span></p>
<div class="figure-reading-group" id="reading-sqe"><h3>圖表組 01 · SQE 的共用格式與命令欄位</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.02">06.02.</span><span class="paragraph-text">共用布局圖先找 CDW0、NSID、MPTR／DPTR 與命令專用區域，再看 CDW0 的 bit 範圍。圖塊為方便閱讀而調整寬度時，以標註的 bits 為準，不能拿像素寬度計算欄位大小。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>MPTR</dt><dd>Metadata Pointer，SQE 中指出獨立 metadata buffer 的欄位。</dd></div></dl>
<a class="reading-link" href="#module-sqe">回到本節的解釋與範例</a>
<!-- figure-table:BASE4-FIG-092 -->
<details class="field-note" id="figure-BASE4-FIG-092"><summary>Base Figure 92 · Command Dword 0</summary>
<!-- claim:BASE4-FIG-092-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.03">06.03.</span><span class="paragraph-text">Figure 92〈Command Dword 0〉：共同 SQE 先以 CDW0 描述 opcode、命令識別與資料指標選擇，再以 NSID 選對象、MPTR／DPTR 指向資料。CDW10–15 的意義由個別命令決定，不能跨 opcode 沿用。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Dword</dt><dd>Dword（Double word）；32 bits，也就是 4 bytes。對比 word=16 bits；例如 zero-based dword count=3 代表 4 個 Dwords，也就是 16 bytes。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 92, 文件頁 139-140, PDF 頁 165-166</p></details>

</details>
<!-- figure-table:BASE4-FIG-093 -->
<details class="field-note" id="figure-BASE4-FIG-093"><summary>Base Figure 93 · Common Command Format</summary>
<!-- claim:BASE4-FIG-093-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.04">06.04.</span><span class="paragraph-text">Figure 93〈Common Command Format〉：共同 SQE 先以 CDW0 描述 opcode、命令識別與資料指標選擇，再以 NSID 選對象、MPTR／DPTR 指向資料。CDW10–15 的意義由個別命令決定，不能跨 opcode 沿用。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, 文件頁 140-142, PDF 頁 166-168</p></details>

</details>
<!-- figure-table:BASE4-FIG-094 -->
<details class="field-note" id="figure-BASE4-FIG-094"><summary>Base Figure 94 · Common Command Format - Vendor Specific Commands (Optional)</summary>
<!-- claim:BASE4-FIG-094-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.05">06.05.</span><span class="paragraph-text">Figure 94〈Common Command Format - Vendor Specific Commands (Optional)〉：廠商自訂命令的標準格式以 NDT 和 NDM 分別描述 data 與 metadata 的 Dword 數量，兩者是直接計數。先確認 VSCF／SNVSCF 對應的格式支援，再解讀指標和長度；格式本身不定義廠商 payload。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>SNVSCF</dt><dd>Same NVM Vendor Specific Command Format，ICSVSCC 中表示 I/O commands 是否使用 Figure 94 的 bit。</dd></div><div><dt>VSCF</dt><dd>Vendor Specific Command Format，AVSCC 中表示 Admin commands 是否使用 Figure 94 的 bit。</dd></div><div><dt>NDM</dt><dd>Number of Dwords in Metadata Transfer，standard vendor-specific format 中的實際 metadata dword 數。</dd></div><div><dt>NDT</dt><dd>Number of Dwords in Data Transfer，standard vendor-specific format 中的實際 data dword 數。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 94, 文件頁 143, PDF 頁 169</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NDM</dt><dd>Number of Dwords in Metadata Transfer，standard vendor-specific format 中的實際 metadata dword 數。</dd></div><div><dt>NDT</dt><dd>Number of Dwords in Data Transfer，standard vendor-specific format 中的實際 data dword 數。</dd></div></dl>
</details>
</div>
<div class="figure-reading-group" id="reading-cqe-status"><h3>圖表組 02 · CQE：新完成項目、命令識別與結果</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.06">06.06.</span><span class="paragraph-text">完成布局圖按「新項目→原命令→結果」閱讀：先確認 P，再連接 SQID、CID，最後用 SCT 選狀態表並查 SC。DNR、CRD 接在主要結果後解釋。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>P</dt><dd>Phase Tag，讓 host 判斷 CQ slot 是否包含新 completion 的翻轉 bit。</dd></div></dl>
<a class="reading-link" href="#module-cqe-status">回到本節的解釋與範例</a>
<!-- figure-table:BASE4-FIG-097 -->
<details class="field-note" id="figure-BASE4-FIG-097"><summary>Base Figure 97 · Common Completion Queue Entry Layout - Admin and All I/O Command Sets</summary>
<!-- claim:BASE4-FIG-097-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.07">06.07.</span><span class="paragraph-text">Figure 97〈Common Completion Queue Entry Layout - Admin and All I/O Command Sets〉：CQE 用 SQID／CID 找回原命令，SQHD 回報提交佇列的消費位置，Status 則描述完成結果。這些欄位不能互代：SQHD 前進不表示所有較早提交命令都已完成。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 97, 文件頁 144, PDF 頁 170</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>SQ</dt><dd>Submission Queue，主機放入命令的提交佇列。</dd></div></dl>
</details>
<!-- figure-table:BASE4-FIG-098 -->
<details class="field-note" id="figure-BASE4-FIG-098"><summary>Base Figure 98 · Completion Queue Entry: DW 2</summary>
<!-- claim:BASE4-FIG-098-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.08">06.08.</span><span class="paragraph-text">Figure 98〈Completion Queue Entry: DW 2〉：CQE 用 SQID／CID 找回原命令，SQHD 回報提交佇列的消費位置，Status 則描述完成結果。這些欄位不能互代：SQHD 前進不表示所有較早提交命令都已完成。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 98, 文件頁 144, PDF 頁 170</p></details>

</details>
<!-- figure-table:BASE4-FIG-099 -->
<details class="field-note" id="figure-BASE4-FIG-099"><summary>Base Figure 99 · Completion Queue Entry: DW 3</summary>
<!-- claim:BASE4-FIG-099-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.09">06.09.</span><span class="paragraph-text">Figure 99〈Completion Queue Entry: DW 3〉：CQE 用 SQID／CID 找回原命令，SQHD 回報提交佇列的消費位置，Status 則描述完成結果。這些欄位不能互代：SQHD 前進不表示所有較早提交命令都已完成。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 99, 文件頁 145, PDF 頁 171</p></details>

</details>
<!-- figure-table:BASE4-FIG-101 -->
<details class="field-note" id="figure-BASE4-FIG-101"><summary>Base Figure 101 · Completion Queue Entry: Status Field</summary>
<!-- claim:BASE4-FIG-101-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.10">06.10.</span><span class="paragraph-text">Figure 101〈Completion Queue Entry: Status Field〉：先讀 SCT 選擇狀態類別，再用 SC 查該類別中的結果。Generic、command-specific、media/data integrity 和 path-related 分別解釋不同原因；DNR 與 CRD 補充重試資訊，不能由單一 SC 數字推論全部處理方式。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 101, 文件頁 145-146, PDF 頁 171-172</p></details>

</details>
<!-- figure-table:BASE4-FIG-102 -->
<details class="field-note" id="figure-BASE4-FIG-102"><summary>Base Figure 102 · Status Code - Status Code Type Values</summary>
<!-- claim:BASE4-FIG-102-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.11">06.11.</span><span class="paragraph-text">Figure 102〈Status Code - Status Code Type Values〉：先讀 SCT 選擇狀態類別，再用 SC 查該類別中的結果。Generic、command-specific、media/data integrity 和 path-related 分別解釋不同原因；DNR 與 CRD 補充重試資訊，不能由單一 SC 數字推論全部處理方式。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 102, 文件頁 146, PDF 頁 172</p></details>

</details>
<!-- figure-table:BASE4-FIG-103 -->
<details class="field-note" id="figure-BASE4-FIG-103"><summary>Base Figure 103 · Status Code - Generic Command Status Values</summary>
<!-- claim:BASE4-FIG-103-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.12">06.12.</span><span class="paragraph-text">Figure 103〈Status Code - Generic Command Status Values〉：先讀 SCT 選擇狀態類別，再用 SC 查該類別中的結果。Generic、command-specific、media/data integrity 和 path-related 分別解釋不同原因；DNR 與 CRD 補充重試資訊，不能由單一 SC 數字推論全部處理方式。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 103, 文件頁 147-150, PDF 頁 173-176</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CMB</dt><dd>Controller Memory Buffer，controller 提供、可放置部分 queue 或資料結構的記憶體區域。</dd></div></dl>
</details>
<!-- figure-table:BASE4-FIG-104 -->
<details class="field-note" id="figure-BASE4-FIG-104"><summary>Base Figure 104 · Status Code - Command Specific Status Values</summary>
<!-- claim:BASE4-FIG-104-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.13">06.13.</span><span class="paragraph-text">Figure 104〈Status Code - Command Specific Status Values〉：先讀 SCT 選擇狀態類別，再用 SC 查該類別中的結果。Generic、command-specific、media/data integrity 和 path-related 分別解釋不同原因；DNR 與 CRD 補充重試資訊，不能由單一 SC 數字推論全部處理方式。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.2.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 104, 文件頁 151-152, PDF 頁 177-178</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>ANA</dt><dd>Asymmetric Namespace Access；描述同一 namespace 經不同 controllers 存取時的路徑狀態。</dd></div></dl>
</details>
<!-- figure-table:BASE4-FIG-105 -->
<details class="field-note" id="figure-BASE4-FIG-105"><summary>Base Figure 105 · Status Code - Command Specific Status Values, I/O Command Set Specific</summary>
<!-- claim:BASE4-FIG-105-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.14">06.14.</span><span class="paragraph-text">Figure 105〈Status Code - Command Specific Status Values, I/O Command Set Specific〉：先讀 SCT 選擇狀態類別，再用 SC 查該類別中的結果。Generic、command-specific、media/data integrity 和 path-related 分別解釋不同原因；DNR 與 CRD 補充重試資訊，不能由單一 SC 數字推論全部處理方式。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.2.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 105, 文件頁 152-153, PDF 頁 178-179</p></details>

</details>
<!-- figure-table:BASE4-FIG-107 -->
<details class="field-note" id="figure-BASE4-FIG-107"><summary>Base Figure 107 · Status Code - Media and Data Integrity Error Values</summary>
<!-- claim:BASE4-FIG-107-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.15">06.15.</span><span class="paragraph-text">Figure 107〈Status Code - Media and Data Integrity Error Values〉：先讀 SCT 選擇狀態類別，再用 SC 查該類別中的結果。Generic、command-specific、media/data integrity 和 path-related 分別解釋不同原因；DNR 與 CRD 補充重試資訊，不能由單一 SC 數字推論全部處理方式。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.2.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 107, 文件頁 154-155, PDF 頁 180-181</p></details>

</details>
<!-- figure-table:BASE4-FIG-108 -->
<details class="field-note" id="figure-BASE4-FIG-108"><summary>Base Figure 108 · Status Code - Path Related Status Values</summary>
<!-- claim:BASE4-FIG-108-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.16">06.16.</span><span class="paragraph-text">Figure 108〈Status Code - Path Related Status Values〉：先讀 SCT 選擇狀態類別，再用 SC 查該類別中的結果。Generic、command-specific、media/data integrity 和 path-related 分別解釋不同原因；DNR 與 CRD 補充重試資訊，不能由單一 SC 數字推論全部處理方式。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.2.3.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3.3, Figure 108, 文件頁 155, PDF 頁 181</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>ANA</dt><dd>Asymmetric Namespace Access；描述同一 namespace 經不同 controllers 存取時的路徑狀態。</dd></div></dl>
</details>
<!-- figure-table:BASE4-FIG-109 -->
<details class="field-note" id="figure-BASE4-FIG-109"><summary>Base Figure 109 · Phase Tag bit Transition Example</summary>
<!-- claim:BASE4-FIG-109-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.17">06.17.</span><span class="paragraph-text">Figure 109〈Phase Tag bit Transition Example〉：Phase Tag 讓主機區分 CQ slot 中的新完成項目與上一次繞行留下的內容。讀圖時沿同一個 slot 追蹤每次繞回後的 phase，而不是把 P=1 永遠當成新項目的通用條件。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.2.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.4, Figure 109, 文件頁 156-157, PDF 頁 182-183</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-prp"><h3>圖表組 03 · PRP 如何描述跨頁資料</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.18">06.18.</span><span class="paragraph-text">先算第一頁剩餘量，再算未覆蓋的資料長度，用這個結果選 PRP2 分支。沿 PRP List 圖中的箭頭辨認「清單所在頁」和「資料頁」，兩者的用途不同。</span></p>
<a class="reading-link" href="#module-prp">回到本節的解釋與範例</a>
<!-- figure-table:BASE4-FIG-110 -->
<details class="field-note" id="figure-BASE4-FIG-110"><summary>Base Figure 110 · PRP Entry Layout</summary>
<!-- claim:BASE4-FIG-110-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.19">06.19.</span><span class="paragraph-text">Figure 110〈PRP Entry Layout〉：PRP1 可同時帶頁基底與頁內位移，後續資料頁依相應對齊規則描述。PRP2 的解讀取決於剩餘資料跨幾頁；PRP List 可以指向不連續的資料頁，所以清單順序與實體位址是否連續是不同問題。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 110, 文件頁 158, PDF 頁 184</p></details>

</details>
<!-- figure-table:BASE4-FIG-111 -->
<details class="field-note" id="figure-BASE4-FIG-111"><summary>Base Figure 111 · PRP Entry - Page Base Address and Offset</summary>
<!-- claim:BASE4-FIG-111-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.20">06.20.</span><span class="paragraph-text">Figure 111〈PRP Entry - Page Base Address and Offset〉：PRP1 可同時帶頁基底與頁內位移，後續資料頁依相應對齊規則描述。PRP2 的解讀取決於剩餘資料跨幾頁；PRP List 可以指向不連續的資料頁，所以清單順序與實體位址是否連續是不同問題。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 111, 文件頁 158, PDF 頁 184</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>PBAO</dt><dd>Page Base Address and Offset，第一個 PRP entry 中同時包含 page base 與 page 內 offset 的配置。</dd></div></dl>
</details>
<!-- figure-table:BASE4-FIG-112 -->
<details class="field-note" id="figure-BASE4-FIG-112"><summary>Base Figure 112 · PRP List Layout for Physically Contiguous Memory Pages</summary>
<!-- claim:BASE4-FIG-112-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.21">06.21.</span><span class="paragraph-text">Figure 112〈PRP List Layout for Physically Contiguous Memory Pages〉：PRP1 可同時帶頁基底與頁內位移，後續資料頁依相應對齊規則描述。PRP2 的解讀取決於剩餘資料跨幾頁；PRP List 可以指向不連續的資料頁，所以清單順序與實體位址是否連續是不同問題。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 112, 文件頁 159, PDF 頁 185</p></details>

</details>
<!-- figure-table:BASE4-FIG-113 -->
<details class="field-note" id="figure-BASE4-FIG-113"><summary>Base Figure 113 · PRP List Layout for Physically Non-Contiguous Memory Pages</summary>
<!-- claim:BASE4-FIG-113-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.22">06.22.</span><span class="paragraph-text">Figure 113〈PRP List Layout for Physically Non-Contiguous Memory Pages〉：PRP1 可同時帶頁基底與頁內位移，後續資料頁依相應對齊規則描述。PRP2 的解讀取決於剩餘資料跨幾頁；PRP List 可以指向不連續的資料頁，所以清單順序與實體位址是否連續是不同問題。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 113, 文件頁 159, PDF 頁 185</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CC.MPS</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.MPS 進一步指定其中的 MPS 子欄位。</dd></div><div><dt>MPS</dt><dd>Memory Page Size，controller 使用的 memory page 大小設定；影響 queue address 與 PRP 對齊。</dd></div><div><dt>CC</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。</dd></div></dl>
</details>
</div>
<div class="figure-reading-group" id="reading-sgl"><h3>圖表組 04 · SGL 的資料與串接描述子</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.23">06.23.</span><span class="paragraph-text">每次沿箭頭前先讀 descriptor type，區分目的地是 data 還是 descriptor list。加總傳輸資料量只計入相應的資料描述，不能把存放清單的 bytes 也當作使用者資料。</span></p>
<a class="reading-link" href="#module-sgl">回到本節的解釋與範例</a>
<!-- figure-table:BASE4-FIG-114 -->
<details class="field-note" id="figure-BASE4-FIG-114"><summary>Base Figure 114 · SGL Validation Error Conditions</summary>
<!-- claim:BASE4-FIG-114-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.24">06.24.</span><span class="paragraph-text">Figure 114〈SGL Validation Error Conditions〉：SGL 先用 descriptor type 和 subtype 決定後續位址、長度如何解讀，再檢查該類型允許的組合。描述子清單中的長度與資料傳輸量不同，不能先把所有 LEN 相加再判斷類型。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 114, 文件頁 161, PDF 頁 187</p></details>

</details>
<!-- figure-table:BASE4-FIG-115 -->
<details class="field-note" id="figure-BASE4-FIG-115"><summary>Base Figure 115 · SGL Segment</summary>
<!-- claim:BASE4-FIG-115-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.25">06.25.</span><span class="paragraph-text">Figure 115〈SGL Segment〉：SGL 先用 descriptor type 和 subtype 決定後續位址、長度如何解讀，再檢查該類型允許的組合。描述子清單中的長度與資料傳輸量不同，不能先把所有 LEN 相加再判斷類型。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 115, 文件頁 161, PDF 頁 187</p></details>

</details>
<!-- figure-table:BASE4-FIG-116 -->
<details class="field-note" id="figure-BASE4-FIG-116"><summary>Base Figure 116 · Generic SGL Descriptor Format</summary>
<!-- claim:BASE4-FIG-116-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.26">06.26.</span><span class="paragraph-text">Figure 116〈Generic SGL Descriptor Format〉：SGL 先用 descriptor type 和 subtype 決定後續位址、長度如何解讀，再檢查該類型允許的組合。描述子清單中的長度與資料傳輸量不同，不能先把所有 LEN 相加再判斷類型。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 116, 文件頁 161, PDF 頁 187</p></details>

</details>
<!-- figure-table:BASE4-FIG-117 -->
<details class="field-note" id="figure-BASE4-FIG-117"><summary>Base Figure 117 · SGL Descriptor Type</summary>
<!-- claim:BASE4-FIG-117-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.27">06.27.</span><span class="paragraph-text">Figure 117〈SGL Descriptor Type〉：SGL 先用 descriptor type 和 subtype 決定後續位址、長度如何解讀，再檢查該類型允許的組合。描述子清單中的長度與資料傳輸量不同，不能先把所有 LEN 相加再判斷類型。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 117, 文件頁 161-162, PDF 頁 187-188</p></details>

</details>
<!-- figure-table:BASE4-FIG-118 -->
<details class="field-note" id="figure-BASE4-FIG-118"><summary>Base Figure 118 · SGL Descriptor Sub Type Values</summary>
<!-- claim:BASE4-FIG-118-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.28">06.28.</span><span class="paragraph-text">Figure 118〈SGL Descriptor Sub Type Values〉：SGL 先用 descriptor type 和 subtype 決定後續位址、長度如何解讀，再檢查該類型允許的組合。描述子清單中的長度與資料傳輸量不同，不能先把所有 LEN 相加再判斷類型。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 118, 文件頁 162, PDF 頁 188</p></details>

</details>
<!-- figure-table:BASE4-FIG-119 -->
<details class="field-note" id="figure-BASE4-FIG-119"><summary>Base Figure 119 · SGL Data Block descriptor</summary>
<!-- claim:BASE4-FIG-119-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.29">06.29.</span><span class="paragraph-text">Figure 119〈SGL Data Block descriptor〉：Data Block 指向資料，Segment／Last Segment 指向描述子清單，Bit Bucket 則有自己的傳輸量語意。沿 Read 例子的箭頭先辨認目的物件，再加總資料量；存放描述子的記憶體不是使用者資料。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 119, 文件頁 162-163, PDF 頁 188-189</p></details>

</details>
<!-- figure-table:BASE4-FIG-120 -->
<details class="field-note" id="figure-BASE4-FIG-120"><summary>Base Figure 120 · SGL Bit Bucket descriptor</summary>
<!-- claim:BASE4-FIG-120-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.30">06.30.</span><span class="paragraph-text">Figure 120〈SGL Bit Bucket descriptor〉：Data Block 指向資料，Segment／Last Segment 指向描述子清單，Bit Bucket 則有自己的傳輸量語意。沿 Read 例子的箭頭先辨認目的物件，再加總資料量；存放描述子的記憶體不是使用者資料。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 120, 文件頁 163, PDF 頁 189</p></details>

</details>
<!-- figure-table:BASE4-FIG-121 -->
<details class="field-note" id="figure-BASE4-FIG-121"><summary>Base Figure 121 · SGL Segment descriptor</summary>
<!-- claim:BASE4-FIG-121-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.31">06.31.</span><span class="paragraph-text">Figure 121〈SGL Segment descriptor〉：Data Block 指向資料，Segment／Last Segment 指向描述子清單，Bit Bucket 則有自己的傳輸量語意。沿 Read 例子的箭頭先辨認目的物件，再加總資料量；存放描述子的記憶體不是使用者資料。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 121, 文件頁 163, PDF 頁 189</p></details>

</details>
<!-- figure-table:BASE4-FIG-122 -->
<details class="field-note" id="figure-BASE4-FIG-122"><summary>Base Figure 122 · SGL Last Segment descriptor</summary>
<!-- claim:BASE4-FIG-122-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.32">06.32.</span><span class="paragraph-text">Figure 122〈SGL Last Segment descriptor〉：Data Block 指向資料，Segment／Last Segment 指向描述子清單，Bit Bucket 則有自己的傳輸量語意。沿 Read 例子的箭頭先辨認目的物件，再加總資料量；存放描述子的記憶體不是使用者資料。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 122, 文件頁 164, PDF 頁 190</p></details>

</details>
<!-- figure-table:BASE4-FIG-125 -->
<details class="field-note" id="figure-BASE4-FIG-125"><summary>Base Figure 125 · SGL Read Example</summary>
<!-- claim:BASE4-FIG-125-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.33">06.33.</span><span class="paragraph-text">Figure 125〈SGL Read Example〉：Data Block 指向資料，Segment／Last Segment 指向描述子清單，Bit Bucket 則有自己的傳輸量語意。沿 Read 例子的箭頭先辨認目的物件，再加總資料量；存放描述子的記憶體不是使用者資料。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.3.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2.1, Figure 125, 文件頁 166, PDF 頁 192</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-identity-text"><h3>圖表組 05 · Feature 值、識別碼、清單與字串</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.34">06.34.</span><span class="paragraph-text">識別格式圖先看對象、寬度及字串填補規則。Controller List 依 NUMCIDS 讀有效項目；Namespace List 依自己的結構和零值規則讀取，不借用另一張清單的 header 格式。</span></p>
<a class="reading-link" href="#module-identity-text">回到本節的解釋與範例</a>
<!-- figure-table:BASE4-FIG-126 -->
<details class="field-note" id="figure-BASE4-FIG-126"><summary>Base Figure 126 · Current Value after Reset with Scope of Entire NVM Subsystem</summary>
<!-- claim:BASE4-FIG-126-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.35">06.35.</span><span class="paragraph-text">Figure 126〈Current Value after Reset with Scope of Entire NVM Subsystem〉：Feature 目前值 在重設後如何改變，需要同時看 Feature 的作用範圍與重設影響的範圍。整個 subsystem 與其子集合的重設可能影響不同對象，不能把一張保留表套到所有重設事件。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.4, Figure 126, 文件頁 167, PDF 頁 193</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl>
</details>
<!-- figure-table:BASE4-FIG-127 -->
<details class="field-note" id="figure-BASE4-FIG-127"><summary>Base Figure 127 · Current Value after Reset with Scope of Subset of the NVM Subsystem</summary>
<!-- claim:BASE4-FIG-127-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.36">06.36.</span><span class="paragraph-text">Figure 127〈Current Value after Reset with Scope of Subset of the NVM Subsystem〉：Feature 目前值 在重設後如何改變，需要同時看 Feature 的作用範圍與重設影響的範圍。整個 subsystem 與其子集合的重設可能影響不同對象，不能把一張保留表套到所有重設事件。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.4, Figure 127, 文件頁 168, PDF 頁 194</p></details>

</details>
<!-- figure-table:BASE4-FIG-128 -->
<details class="field-note" id="figure-BASE4-FIG-128"><summary>Base Figure 128 · PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)</summary>
<!-- claim:BASE4-FIG-128-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.37">06.37.</span><span class="paragraph-text">Figure 128〈PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)〉：VID／SSVID 辨認廠商，SN／MN 描述序號與型號。固定字串欄位要依寬度及填補規則閱讀；不能把字串直接當成以零結尾的任意長度資料。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.5.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.5.1, Figure 128, 文件頁 169, PDF 頁 195</p></details>

</details>
<!-- figure-table:BASE4-FIG-129 -->
<details class="field-note" id="figure-BASE4-FIG-129"><summary>Base Figure 129 · Serial Number (SN) and Model Number (MN)</summary>
<!-- claim:BASE4-FIG-129-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.38">06.38.</span><span class="paragraph-text">Figure 129〈Serial Number (SN) and Model Number (MN)〉：VID／SSVID 辨認廠商，SN／MN 描述序號與型號。固定字串欄位要依寬度及填補規則閱讀；不能把字串直接當成以零結尾的任意長度資料。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.5.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.5.2, Figure 129, 文件頁 170, PDF 頁 196</p></details>

</details>
<!-- figure-table:BASE4-FIG-130 -->
<details class="field-note" id="figure-BASE4-FIG-130"><summary>Base Figure 130 · IEEE OUI Identifier (IEEE)</summary>
<!-- claim:BASE4-FIG-130-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.39">06.39.</span><span class="paragraph-text">Figure 130〈IEEE OUI Identifier (IEEE)〉：OUI、EUI64、NGUID 與 WWN 對照圖用來辨認識別值的組成及配置關係。外觀相似不代表格式可互換；先確認欄位寬度及定義，再辨認廠商部分與其他識別部分。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>OUI</dt><dd>Organizationally Unique Identifier，由 IEEE 配置給組織的 identifier 前綴。</dd></div><div><dt>WWN</dt><dd>World Wide Name，用於儲存與網路裝置識別的全域名稱格式。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.5.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.5.3, Figure 130, 文件頁 170, PDF 頁 196</p></details>

</details>
<!-- figure-table:BASE4-FIG-131 -->
<details class="field-note" id="figure-BASE4-FIG-131"><summary>Base Figure 131 · IEEE Extended Unique Identifier (EUI64), MA-L Format</summary>
<!-- claim:BASE4-FIG-131-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.40">06.40.</span><span class="paragraph-text">Figure 131〈IEEE Extended Unique Identifier (EUI64), MA-L Format〉：OUI、EUI64、NGUID 與 WWN 對照圖用來辨認識別值的組成及配置關係。外觀相似不代表格式可互換；先確認欄位寬度及定義，再辨認廠商部分與其他識別部分。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>WWN</dt><dd>World Wide Name，用於儲存與網路裝置識別的全域名稱格式。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.5.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 131, 文件頁 170, PDF 頁 196</p></details>

</details>
<!-- figure-table:BASE4-FIG-132 -->
<details class="field-note" id="figure-BASE4-FIG-132"><summary>Base Figure 132 · IEEE Extended Unique Identifier (EUI64), OUI Identifier</summary>
<!-- claim:BASE4-FIG-132-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.41">06.41.</span><span class="paragraph-text">Figure 132〈IEEE Extended Unique Identifier (EUI64), OUI Identifier〉：OUI、EUI64、NGUID 與 WWN 對照圖用來辨認識別值的組成及配置關係。外觀相似不代表格式可互換；先確認欄位寬度及定義，再辨認廠商部分與其他識別部分。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.5.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 132, 文件頁 170, PDF 頁 196</p></details>

</details>
<!-- figure-table:BASE4-FIG-133 -->
<details class="field-note" id="figure-BASE4-FIG-133"><summary>Base Figure 133 · IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)</summary>
<!-- claim:BASE4-FIG-133-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.42">06.42.</span><span class="paragraph-text">Figure 133〈IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)〉：OUI、EUI64、NGUID 與 WWN 對照圖用來辨認識別值的組成及配置關係。外觀相似不代表格式可互換；先確認欄位寬度及定義，再辨認廠商部分與其他識別部分。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.5.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 133, 文件頁 170-171, PDF 頁 196-197</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NAA</dt><dd>Network Address Authority，WWN 中選擇 identifier 格式與配置方式的 nibble。</dd></div></dl>
</details>
<!-- figure-table:BASE4-FIG-134 -->
<details class="field-note" id="figure-BASE4-FIG-134"><summary>Base Figure 134 · MA-L similarity to WWN</summary>
<!-- claim:BASE4-FIG-134-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.43">06.43.</span><span class="paragraph-text">Figure 134〈MA-L similarity to WWN〉：OUI、EUI64、NGUID 與 WWN 對照圖用來辨認識別值的組成及配置關係。外觀相似不代表格式可互換；先確認欄位寬度及定義，再辨認廠商部分與其他識別部分。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.5.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 134, 文件頁 171, PDF 頁 197</p></details>

</details>
<!-- figure-table:BASE4-FIG-135 -->
<details class="field-note" id="figure-BASE4-FIG-135"><summary>Base Figure 135 · Namespace Globally Unique Identifier (NGUID)</summary>
<!-- claim:BASE4-FIG-135-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.44">06.44.</span><span class="paragraph-text">Figure 135〈Namespace Globally Unique Identifier (NGUID)〉：OUI、EUI64、NGUID 與 WWN 對照圖用來辨認識別值的組成及配置關係。外觀相似不代表格式可互換；先確認欄位寬度及定義，再辨認廠商部分與其他識別部分。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.5.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 135, 文件頁 171, PDF 頁 197</p></details>

</details>
<!-- figure-table:BASE4-FIG-136 -->
<details class="field-note" id="figure-BASE4-FIG-136"><summary>Base Figure 136 · Namespace Globally Unique Identifier (NGUID), OUI</summary>
<!-- claim:BASE4-FIG-136-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.45">06.45.</span><span class="paragraph-text">Figure 136〈Namespace Globally Unique Identifier (NGUID), OUI〉：OUI、EUI64、NGUID 與 WWN 對照圖用來辨認識別值的組成及配置關係。外觀相似不代表格式可互換；先確認欄位寬度及定義，再辨認廠商部分與其他識別部分。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.5.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 136, 文件頁 171, PDF 頁 197</p></details>

</details>
<!-- figure-table:BASE4-FIG-137 -->
<details class="field-note" id="figure-BASE4-FIG-137"><summary>Base Figure 137 · Namespace Globally Unique Identifier</summary>
<!-- claim:BASE4-FIG-137-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.46">06.46.</span><span class="paragraph-text">Figure 137〈Namespace Globally Unique Identifier〉：OUI、EUI64、NGUID 與 WWN 對照圖用來辨認識別值的組成及配置關係。外觀相似不代表格式可互換；先確認欄位寬度及定義，再辨認廠商部分與其他識別部分。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.5.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 137, 文件頁 171, PDF 頁 197</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NAA</dt><dd>Network Address Authority，WWN 中選擇 identifier 格式與配置方式的 nibble。</dd></div></dl>
</details>
<!-- figure-table:BASE4-FIG-138 -->
<details class="field-note" id="figure-BASE4-FIG-138"><summary>Base Figure 138 · Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN</summary>
<!-- claim:BASE4-FIG-138-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.47">06.47.</span><span class="paragraph-text">Figure 138〈Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN〉：OUI、EUI64、NGUID 與 WWN 對照圖用來辨認識別值的組成及配置關係。外觀相似不代表格式可互換；先確認欄位寬度及定義，再辨認廠商部分與其他識別部分。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.5.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 138, 文件頁 171, PDF 頁 197</p></details>

</details>
<!-- figure-table:BASE4-FIG-139 -->
<details class="field-note" id="figure-BASE4-FIG-139"><summary>Base Figure 139 · Controller List Format</summary>
<!-- claim:BASE4-FIG-139-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.48">06.48.</span><span class="paragraph-text">Figure 139〈Controller List Format〉：Controller List 以 NUMCIDS 開頭，後接 16-bit controller IDs；Namespace List 直接列出 32-bit NSIDs。兩者都依各自排序及未使用項目規則讀取，但不能共用同一種 header。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.6.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.6.1, Figure 139, 文件頁 172, PDF 頁 198</p></details>

</details>
<!-- figure-table:BASE4-FIG-140 -->
<details class="field-note" id="figure-BASE4-FIG-140"><summary>Base Figure 140 · Namespace List Format</summary>
<!-- claim:BASE4-FIG-140-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.49">06.49.</span><span class="paragraph-text">Figure 140〈Namespace List Format〉：Controller List 以 NUMCIDS 開頭，後接 16-bit controller IDs；Namespace List 直接列出 32-bit NSIDs。兩者都依各自排序及未使用項目規則讀取，但不能共用同一種 header。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.6.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.6.2, Figure 140, 文件頁 172, PDF 頁 198</p></details>

</details>
<!-- figure-table:BASE4-FIG-142 -->
<details class="field-note" id="figure-BASE4-FIG-142"><summary>Base Figure 142 · UTF-8 Input Processing</summary>
<!-- claim:BASE4-FIG-142-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.50">06.50.</span><span class="paragraph-text">Figure 142〈UTF-8 Input Processing〉：UTF-8 的一個字元可由多個 bytes 編碼。沿輸入處理圖分辨起始 byte 與後續 bytes，長度限制仍按所定義的 byte 數計算；字元數不是 buffer 長度。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.8</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.8, Figure 142, 文件頁 175, PDF 頁 201</p></details>

</details>
</div>
</section>
</details>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:base-ch4-command-id -->
<details class="review-question" id="qa-base-ch4-command-id"><summary>1. 2 個 SQ 都使用 CID=5，收到 completion 時該如何分辨命令？</summary>
<div data-qa-answer="base-ch4-command-id"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.01">07.01.</span><span class="paragraph-text">CID 的唯一性範圍是同一 SQ 的 outstanding commands。完成資訊需要連同 SQ identifier 解讀，才能找到正確 SQ 中的那筆命令。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 文件頁 140, PDF 頁 166</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, 文件頁 144-145, PDF 頁 170-171</p>
</details></details>
<!-- qa:base-ch4-phase-status -->
<details class="review-question" id="qa-base-ch4-phase-status"><summary>2. CQE 的 Phase Tag 符合 host 期待值，是否表示命令成功？</summary>
<div data-qa-answer="base-ch4-phase-status"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.02">07.02.</span><span class="paragraph-text">Phase Tag 讓 host 辨認這個位置的新 completion；是否成功則由 Status Code Type、Status Code 等狀態資訊決定。新資料與成功結果是兩個判斷。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.4, 文件頁 155-158, PDF 頁 181-184</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, 文件頁 145-155, PDF 頁 171-181</p>
</details></details>
<!-- qa:base-ch4-prp-offset -->
<details class="review-question" id="qa-base-ch4-prp-offset"><summary>3. PRP1 位於 page 中間時，為何跨頁後不能直接延續同一段實體地址？</summary>
<div data-qa-answer="base-ch4-prp-offset"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.03">07.03.</span><span class="paragraph-text">PRP1 提供第一段的 page offset；跨頁後由後續 PRP page address 或 PRP List 指定資料位置。Host 的邏輯連續 buffer 不必對應連續的實體 pages。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, 文件頁 158-159, PDF 頁 184-185</p>
</details></details>
<!-- qa:base-ch4-pointer-format -->
<details class="review-question" id="qa-base-ch4-pointer-format"><summary>4. 為何解讀 DPTR 前要先看 PSDT？</summary>
<div data-qa-answer="base-ch4-pointer-format"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.04">07.04.</span><span class="paragraph-text">DPTR 的同一組 bits 可依選定格式表達 PRP 或 SGL。先確認 PSDT 與命令支援條件，才知道應把後續資料當 page pointers 或 segment descriptors。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, 文件頁 140-142, PDF 頁 166-168</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, 文件頁 159-166, PDF 頁 185-192</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
