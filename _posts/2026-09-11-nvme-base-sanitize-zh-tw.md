---
permalink: /nvme/sanitize-zh-tw/
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4：Sanitize：清除範圍、方法與完成判斷"
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
[English]({% post_url 2026-09-11-nvme-base-sanitize-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">Sanitize 處理資料清除。理解它需要依序回答：清除哪些資料、使用哪一種方法、控制器目前處於什麼狀態，以及什麼證據能證明清除已完成。命令已被接受，與清除作業已完成，必須分別確認。</span></p>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>決定清除範圍</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">先確認要清除的資料類別與範圍，再看控制器支援哪些清除能力。</span></p></article>
<article><span class="axis-number">02</span><h3>選擇方法與參數</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">比較區塊清除、覆寫及密碼清除的做法；命令參數必須配合所選的方法。</span></p></article>
<article><span class="axis-number">03</span><h3>區分接受、進行與完成</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">命令回覆成功不代表資料已清除完畢；持續從狀態紀錄確認進度、成功或失敗。</span></p></article>
<article><span class="axis-number">04</span><h3>理解清除後的讀取</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="04-01">04-01</span><span class="paragraph-text">媒體驗證和正常讀取的用途不同；讀回資料的意義還要結合 NVM Command Set 的規則。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl></article>
</div>
<div class="overview-connections"><h3>把主軸連起來</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">先選清除目標與支援的方法，再根據方法設定命令；之後由狀態紀錄判斷進度、成功或失敗。若進入媒體驗證狀態，還要分清驗證讀取與正常資料存取，並用 NVM Command Set 的規則理解清除後讀到的內容。</span></p>
</div>
</section>
<section class="lesson" id="module-sanitize-scope"><h2 id="heading-sanitize-scope"><span class="section-number">01</span> 清除會涵蓋哪些資料</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">Sanitize scope 不是『磁碟上所有東西』。以 target、資料來源、是否可能含 user data 判斷；Boot 與診斷機制的交叉關係也從這個範圍開始。</span></p>
<!-- claim:BASESANITIZE-SAN-SCOPE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">Subsystem sanitize 與 namespace sanitize 的資料範圍不同。逐一 sanitize 全部 namespaces 不等同 subsystem sanitize，也不能因此把 subsystem GDE 設為 1。兩者都不影響 Boot Partitions 或 RPMB；含 user data 的 logs/features 則可能必須修改。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.27</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27, 文件頁 711-712, PDF 頁 737-738</p></details>
<div class="table-wrap"><table><caption>清除會涵蓋哪些資料</caption><thead><tr><th scope="col">清除對象或方法</th><th scope="col">包含或排除哪些資料</th><th scope="col">可據此確認的範圍</th></tr></thead><tbody><tr><td>Boot/RPMB</td><td>不受 sanitize 影響</td><td>另由自身管理機制控制</td></tr><tr><td>Logs/features</td><td>必要時修改 user data</td><td>不能只檢查 namespace media</td></tr><tr><td>All namespace sanitizes</td><td>只完成各 target 的工作</td><td>不能因此宣告 subsystem GDE</td></tr><tr><td>Crypto Erase</td><td>改 key 並處理未加密資料</td><td>舊 key 副本也是重要條件</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">即使所有 namespaces 都已 sanitize，CMB 等 subsystem 層級資料仍不能由這個事實證明已完成 subsystem sanitization。相反地，成功 subsystem sanitize 也不會替 Boot Partition 更新或清除開機映像。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CMB</dt><dd>Controller Memory Buffer，controller 提供、可放置部分 queue 或資料結構的記憶體區域。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-sanitize-command"><h2 id="heading-sanitize-command"><span class="section-number">02</span> 清除方法、支援能力與命令參數</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">先把支援能力、命令要求與 Feature policy 分開。命令接受、operation 成功、符合 no-deallocate 要求是三個需要不同證據的結果。</span></p>
<!-- claim:BASESANITIZE-SAN-COMMAND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">CDW10 包含 SANACT[2:0]、AUSE[3]、OWPASS[7:4]、OIPBP[8]、NDAS[9]、EMVS[10]、PREQ[11]；CDW11 是 OVRPAT。SANACT 001b=Exit Failure Mode、010b=Block Erase、011b=Overwrite、100b=Crypto Erase、101b=Exit Media Verification；其他值保留。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>SANACT</dt><dd>Sanitize Action；決定實際方法、退出 Failure 或退出 Media Verification。</dd></div><div><dt>AUSE</dt><dd>Allow Unrestricted Sanitize Exit；選擇失敗時是否允許不經成功重試就退出 Failure。</dd></div><div><dt>EMVS</dt><dd>Enter Media Verification State；成功 processing 後要求進入驗證，受方法與 capability 限制。</dd></div><div><dt>NDAS</dt><dd>No-Deallocate After Sanitize；命令要求，需與 SANICAP.NDI 及 NODRM 一起解讀。</dd></div><div><dt>PREQ</dt><dd>Purge Request；與 SPRRS 一起判定 purge 要求與回報；兩種 Sanitize 命令的 bit 位置不同。</dd></div><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.26</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, 文件頁 448-451, PDF 頁 474-477</p></details>
<div class="table-wrap"><table><caption>清除方法、支援能力與命令參數</caption><thead><tr><th scope="col">命令與能力組合</th><th scope="col">控制器如何處理</th><th scope="col">完成或拒絕的原因</th></tr></thead><tbody><tr><td>NDAS=1, NDI=0</td><td>不得因成功 sanitize deallocate</td><td>其他合法條件仍需符合</td></tr><tr><td>NDAS=1, NDI=1, NODRM=0</td><td>命令拒絕</td><td>Invalid Field in Command</td></tr><tr><td>NDAS=1, NDI=1, NODRM=1</td><td>允許處理</td><td>成功可回 SOS=100b</td></tr><tr><td>EMVS=1</td><td>Subsystem 要 VERS=1</td><td>Block/Crypto + NDAS=0</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>NODRM</dt><dd>No-Deallocate Response Mode；FID 17h bit 0，選擇受抑制 NDAS 的 error 或 warning 回應。</dd></div><div><dt>NDI</dt><dd>No-Deallocate Inhibited；宣告 controller 是否抑制 NDAS 的要求。</dd></div><div><dt>SOS</dt><dd>Sanitize Operation Status；SSTAT bits 2:0，與目前 SANS state 分開判讀。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">SANACT=010b、AUSE=0、EMVS=1、NDAS=0、PREQ=0 的 CDW10 是 0402h。只有支援 VERS/Block Erase 且其他前置條件成立時才適用。另一例：OWPASS=0h 是 16 次，不是『跳過 overwrite』。</span></p></aside>
</section>
<section class="lesson" id="module-sanitize-state"><h2 id="heading-sanitize-state"><span class="section-number">03</span> 背景 Sanitize 的狀態與進度</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">從 Figure 772 的七個 states 出發，逐一把 Figures 773–779 的 transition condition 接上。Status 描述結果，state 描述目前位置，事件描述發生的轉折。</span></p>
<!-- claim:BASESANITIZE-SAN-BACKGROUND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span><span class="paragraph-text">Sanitize 在背景執行。開始 operation 後先更新 LID 81h，再完成啟動命令；Host 需用狀態 log 與事件判定後續進度。執行中的 operation 不能被 abort，並持續跨 reset/power cycle，但 verification 階段可能因指定 reset 被取消。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div><div><dt>LID</dt><dd>Log Page Identifier；指定要讀取哪一種 log page 的編號。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.26.1; 8.1.27.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26.1; 8.1.27.1, 文件頁 451,712-713, PDF 頁 477,738-739</p></details>
<div class="table-wrap"><table><caption>背景 Sanitize 的狀態與進度</caption><thead><tr><th scope="col">作業階段</th><th scope="col">可以採取的後續動作</th><th scope="col">進度與歷史如何回報</th></tr></thead><tbody><tr><td>Restricted Failure</td><td>只以 restricted 重試</td><td>Exit Failure Mode 不可解套</td></tr><tr><td>Unrestricted Failure</td><td>重試或 Exit Failure Mode</td><td>回 Idle 不會改寫失敗歷史</td></tr><tr><td>Media Verification</td><td>Processing 已成功</td><td>整個 operation 仍 Sanitizing</td></tr><tr><td>Post-Verification Deallocation</td><td>SPROG 重新由 0 起算</td><td>失敗 FAILS=6h</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>SPROG</dt><dd>Sanitize Progress；raw/65536，僅表示目前量測階段的進度。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.03">03.03.</span><span class="paragraph-text">SPROG=8000h 表示目前被量測的階段約 50%。進入 Media Verification 後 SPROG=FFFFh，SOS 仍可為 010b；退出驗證進入 deallocation 又從 0 開始。這不是進度倒退。</span></p></aside>
</section>
<section class="lesson" id="module-sanitize-read"><h2 id="heading-sanitize-read"><span class="section-number">04</span> 操作限制與驗證讀取</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">把 command allowlist 與 NVM Read 特例分開判斷。Host 先辨識 target/state，再確認 PI checking 與 allocation，不能把平常 read 的處理完全套入驗證狀態。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>PI</dt><dd>Protection Information；用 Guard 與 tags 檢查資料及其關聯資訊的保護欄位。</dd></div></dl>
<!-- claim:BASESANITIZE-SAN-RESTRICT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">Subsystem sanitize 進行中以 Figure 144 判斷允許的 Admin 命令及 log pages；Boot Partition log 在清單內，Telemetry 07h/08h 不在。未被允許的操作受 Sanitize In Progress 限制；namespace sanitize 另依 Figures 145/146 與 target NSID 判斷。Media Verification 的 NVM Read 有特定例外。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.27.5; 5.1.1-5.1.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.5; 5.1.1-5.1.2, 文件頁 178-181,730-732, PDF 頁 204-207,756-758</p></details>
<div class="table-wrap"><table><caption>操作限制與驗證讀取</caption><thead><tr><th scope="col">驗證讀取條件</th><th scope="col">回傳內容或狀態</th><th scope="col">這個結果能說明什麼</th></tr></thead><tbody><tr><td>PI checking requested</td><td>Invalid Field in Command</td><td>驗證讀取不允許此組合</td></tr><tr><td>Allocated media readable</td><td>回實際 media data</td><td>可忽略可讀情況的 integrity error</td></tr><tr><td>Allocated media unreadable</td><td>Unrecovered Read Error</td><td>不可假造資料</td></tr><tr><td>Deallocated LBA</td><td>依 deallocated/unwritten 規則</td><td>不是檢查原始 media pattern 的證據</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.03">04.03.</span><span class="paragraph-text">驗證讀取 PRCHK=000b、STC=0，所有 allocated LBAs 都能讀取，且沒有其他 abort 原因時，預期 Successful Media Verification Read。只要請求 PI checking，預期分支即改為 Invalid Field in Command。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>PRCHK</dt><dd>Protection Information Check；三個 bits 分別要求 guard、application tag、reference tag 檢查；驗證讀取設 000b。</dd></div><div><dt>STC</dt><dd>Storage Tag Check；本報告指 NVM Read 的 storage tag 檢查，驗證讀取設 0。</dd></div></dl></aside>
</section>
<section id="spec-reading"><h2>接著打開 Spec 看什麼</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span><span class="paragraph-text">以下按概念列出閱讀位置。報告時先用上面的流程說明問題，再打開對應章節看欄位與完整條件。中文教學 HTML 另有本篇全部圖表的逐圖重點、案例與細節。</span></p>
<div class="table-wrap"><table><thead><tr><th scope="col">要說明的觀念</th><th scope="col">Spec 閱讀位置</th></tr></thead><tbody><tr><td>清除會涵蓋哪些資料</td><td>Base 2.4 §8.1.27 · Base 2.4 §8.1.27.2-8.1.27.3 · NVM 1.3 §5.12</td></tr><tr><td>清除方法、支援能力與命令參數</td><td>Base 2.4 §5.2.26 · Base 2.4 §8.1.27.1; 5.2.27 · Base 2.4 §5.2.30.1.16; 8.1.27.2-8.1.27.3 · Base 2.4 §5.2.26; 8.1.27.1 · Base 2.4 §5.2.26; 8.1.27.3</td></tr><tr><td>背景 Sanitize 的狀態與進度</td><td>Base 2.4 §5.2.26.1; 8.1.27.1 · Base 2.4 §8.1.27.4 · Base 2.4 §8.1.27.4.6-8.1.27.4.7 · Base 2.4 §5.2.13.1.38 · Base 2.4 §5.2.13.1.38; 8.1.27.3 · Base 2.4 §8.1.27.1; 8.1.27.4</td></tr><tr><td>操作限制與驗證讀取</td><td>Base 2.4 §8.1.27.5; 5.1.1-5.1.2 · Base 2.4 §8.1.27.5 · NVM 1.3 §4.1.7; 5.12 · NVM 1.3 §5.12 · NVM 1.3 §5.12.1</td></tr></tbody></table></div>
<a class="reading-link" href="/DOCS/nvme-spec-report/base-sanitize/tutorial-zh-tw.html">開啟完整中文教學與逐圖解釋 →</a></section>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:base-sanitize-1 -->
<details class="review-question" id="qa-base-sanitize-1"><summary>1. Sanitize 命令回報 Successful Completion，是否可以立即宣告清除完成？</summary>
<div data-qa-answer="base-sanitize-1"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="06.01">06.01.</span><span class="paragraph-text">它表示啟動命令成功，背景 operation 可能仍在進行。後續要用相應的 Sanitize Status 判斷 operation 狀態；SPROG 與時間估計提供進度資訊，不能取代最終狀態。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26.1; 8.1.27.1, 文件頁 451,712-713, PDF 頁 477,738-739</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, 文件頁 313-319, PDF 頁 339-345</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38; 8.1.27.3, 文件頁 314-319,718, PDF 頁 340-345,744</p>
</details></details>
<!-- qa:base-sanitize-2 -->
<details class="review-question" id="qa-base-sanitize-2"><summary>2. 為何不能用「讀回全零」作為所有 sanitize 方法的共同成功標準？</summary>
<div data-qa-answer="base-sanitize-2"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="06.02">06.02.</span><span class="paragraph-text">各方法的讀值規則不同，且 deallocation 會改用另一組規則。Block Erase、Crypto Erase、Overwrite 不能用同一預期 pattern 判斷；Media Verification state 也有自己的讀取語意。先確認 operation 狀態，再按方法與 block 狀態解釋資料。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.27.2-8.1.27.3, 文件頁 714-717, PDF 頁 740-743</p>
<p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12, 文件頁 174, PDF 頁 174</p>
<p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12.1, 文件頁 174-175, PDF 頁 174-175</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express Base Specification, Revision 2.4</p><p>NVM Express NVM Command Set Specification, Revision 1.3</p></details></footer>
</div>
