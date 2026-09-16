---
permalink: /nvme/command-feature-lockdown-zh-tw/
layout: post
read_time: true
show_date: true
title: "NVMe Command and Feature Lockdown：查詢、限制範圍與持續性"
date: 2026-09-16
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
[English]({% post_url 2026-09-16-nvme-command-feature-lockdown-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">Command and Feature Lockdown 處理的是「哪些管理操作，在什麼入口、哪些控制器上不准執行」。理解它需要把能力、目前狀態與修改命令接起來，再分清限制何時解除、斷電後是否保留。本文以一個 FID 的限制與讀回為例，從全貌走到命令欄位、兩種 Log 格式與必要的持續性例外。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Lockdown</dt><dd>本篇指 Command and Feature Lockdown：以操作種類、接收介面與控制器範圍限制管理操作的機制。</dd></div><div><dt>FID</dt><dd>Feature Identifier；指定要讀取或設定哪一項 Feature 的編號。</dd></div></dl>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>先知道能限制什麼</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">先查裝置是否支援整體限制或逐一指定控制器，再查哪些操作允許被禁止。功能存在、操作受支援、操作可禁止，是三個不同問題。</span></p></article>
<article><span class="axis-number">02</span><h3>把限制範圍說清楚</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">依序選操作、接收入口與控制器。只禁止一項設定、只限制某個入口，或只選某台控制器，會得到不同的影響範圍。</span></p></article>
<article><span class="axis-number">03</span><h3>查詢要能驗證設定</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">一般格式看全體共同項目；增強格式看指定控制器或全體彙整，再分辨某項是否所有控制器都符合。用相同條件讀回才有比較意義。</span></p></article>
<article><span class="axis-number">04</span><h3>理解限制的生命週期</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="04-01">04-01</span><span class="paragraph-text">限制可以用命令解除；經過斷電循環後是否仍保留，還要看最初選的控制器範圍與持續性設定。最後補足認證解凍與廠商定義的必要條件。</span></p></article>
</div>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">適合學過 OS、Computer Organization 並了解 SSD 基本概念的讀者。以 PCIe 主機管理流程為主要情境；Management Endpoint 只解釋 Base 明載的關係。所有控制器編號、可禁止清單及命令編碼案例均為說明性範例，實際可用項目由裝置能力決定。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Management Endpoint</dt><dd>帶外管理接收入口；與主機的 Admin Submission Queue 分開選擇限制。</dd></div><div><dt>PCIe</dt><dd>PCI Express，NVMe memory-based controller 使用的 transport 與裝置互連。</dd></div></dl>
<div class="overview-connections"><h3>把主軸連起來</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.03">00.03.</span><span class="paragraph-text">可以用一個問題帶著讀：如果只想限制控制器 7 經 Admin Queue 修改 FID 06h，應查哪些能力、送哪些參數、用什麼回覆證明限制成立？沿著這條線，清單、欄位與錯誤碼才有各自的位置。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div></dl>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.04">00.04.</span><span class="paragraph-text">中文教學先補足每一步的理由，再在問答前整理相關規格圖表的欄位關係。兩種 Log 的長度、控制器編號、代碼清單與 UUID 索引會各自演算，避免只記住縮寫而失去它所描述的對象。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>UUID</dt><dd>Universally Unique Identifier；128-bit 識別值，本篇用來區分同一廠商 FID 的不同定義。</dd></div></dl>
</div>
</section>
<section id="spec-route"><h2>開著 Spec 的順向報告路徑</h2>
<p class="reader-paragraph"><span class="paragraph-number figure-paragraph-number" aria-label="R-1">R-1</span><span class="paragraph-text">先用本文的全貌、流程與案例說明目的，再依下列 Base PDF 檢視器頁碼向後翻。共用頁只讀指定起始標題到停止標題；不必為每個必要引用往返翻頁，中文教學已集中解釋其欄位與條件。</span></p>
<div class="table-wrap"><table><thead><tr><th scope="col">翻頁順序</th><th scope="col">主範圍</th><th scope="col">重點與停止位置</th></tr></thead><tbody><tr><td>R1 · Base PDF 305–309</td><td>§5.2.13.1.20</td><td>從 Command and Feature Lockdown 標題起：查詢選擇 → 一般清單 → 增強外框與描述器。用 A／B 例子比較全體共同項目與部分控制器項目。 在 §5.2.13.1.21 前停下。</td></tr><tr><td>R2 · Base PDF 431–434</td><td>§5.2.16</td><td>從 Lockdown command 標題起：用 controller7／FID06h 算 CDW10、14，再分清設定失敗與後續命令被禁止。 在 §5.2.17 前停下。</td></tr><tr><td>R3 · Base PDF 623–625</td><td>§8.1.5</td><td>從 Command and Feature Lockdown 標題起，收束介面、能力與持續性規則；以 CSEL0 對照 CSEL1/2 的 power cycle 結果。 在 §8.1.6 前停下。</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>power cycle</dt><dd>整個指定裝置或 subsystem 的電源循環；本篇不能以一般 Controller Reset 代替。</dd></div><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div></dl>
</section>
<section class="lesson" id="module-lockdown-model"><h2 id="heading-lockdown-model"><span class="section-number">01</span> 先理解：限制的是哪個操作從哪裡進來</h2>
<figure><figcaption><strong>從意圖到可確認的限制</strong></figcaption><ol class="flow-steps"><li>先說清楚：要限制哪個操作、接收介面與控制器集合。</li><li>Identify 查 CFLS／CCFLS，再讀 LID14h 的可禁止清單。</li><li>Lockdown 填 SCP、OFI、IFC、CSEL／CSS、PRHBT，等完成。</li><li>用相同範圍讀 LID14h 的目前禁止清單，確認設定結果。</li><li>後續符合條件的命令被拒絕；解除與 power cycle 另依持續性規則判斷。</li></ol><figcaption>查詢取得資訊；Lockdown 改變狀態；後續命令才接受限制檢查。來源：Base §8.1.5、§5.2.16。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>CCFLS</dt><dd>Controller-scoped Command and Feature Lockdown Supported；可選控制器範圍的擴充支援位元。</dd></div><div><dt>PRHBT</dt><dd>Prohibit；1 要求禁止，0 要求允許，作用對象由其餘選擇欄位決定。</dd></div><div><dt>CFLS</dt><dd>Command and Feature Lockdown Supported；基本 Lockdown 支援位元。</dd></div><div><dt>CSEL</dt><dd>Controller Select；選全部、單一或某 primary 所屬 secondary 控制器集合。</dd></div><div><dt>CSS</dt><dd>Controller Select Specific；在本命令 CDW14 中依 CSEL 提供目標或 primary 控制器編號。</dd></div><div><dt>IFC</dt><dd>Interface；指定受限制操作從哪個介面收到時套用限制。</dd></div><div><dt>OFI</dt><dd>Opcode or Feature Identifier；Lockdown 要禁止或允許的代碼，其種類由 SCP 選定。</dd></div><div><dt>SCP</dt><dd>Scope；指定代碼屬於 Admin opcode、Set Features FID 或管理介面命令集。</dd></div></dl>
<!-- claim:LOCKDOWN-MODEL -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">Command and Feature Lockdown 讓主機限制特定管理命令，或 Set Features 對某個 FID 的設定操作。限制同時有操作種類、接收介面與控制器範圍；LID 14h 用來查可禁止項目與目前禁止狀態，Lockdown 命令用來改變它們。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>LID</dt><dd>Log Page Identifier；指定要讀取哪一種 log page 的編號。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.5, 文件頁 597-599, PDF 頁 623-625</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">假設 FID 06h 可被禁止：只限制「Set Features / FID 06h」與限制整個 Set Features opcode，影響不同。前者不會只因這條規則而禁止其他 FID 的設定，也不等同禁止 Get Features 讀取。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>opcode</dt><dd>操作代碼；先選要執行的命令，再由該命令的其他欄位提供參數。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-lockdown-capability"><h2 id="heading-lockdown-capability"><span class="section-number">02</span> 先查支援層級，再查可禁止項目</h2>
<!-- claim:LOCKDOWN-CAPABILITY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">Identify Controller 的 OACS.CFLS 表示基本 Lockdown 能力，CCFLS 表示可選控制器的擴充能力。CFLS=1 保證 CSEL=0 與 LID 14h；CCFLS=1 還要求 CSEL=1、2 與增強版 Log。每個 OFI 能否被禁止仍需查清單。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>OACS</dt><dd>Optional Admin Command Support；Identify Controller 的選用管理命令與功能能力位元欄位。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.5, 文件頁 599, PDF 頁 625</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">只觀察 OACS 的 bits 13、10：2400h 同時設了 CCFLS 與 CFLS；0400h 只表示基本能力。不能把 0400h 的裝置當成一定支援 CSEL=1 或 ELPF=1。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>ELPF</dt><dd>Enhanced Log Page Format；選一般或增強版 LID14h 資料格式。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-lockdown-targets"><h2 id="heading-lockdown-targets"><span class="section-number">03</span> 介面與控制器是兩個獨立選擇</h2>
<figure><figcaption><strong>只改一個選擇，觀察受影響範圍</strong></figcaption><div class="table-wrap"><table><thead><tr><th scope="col">固定條件</th><th scope="col">改變的欄位</th><th scope="col">限制涵蓋的對象</th></tr></thead><tbody><tr><td>FID06h、Admin Queue</td><td>CSEL0</td><td>全部控制器</td></tr><tr><td>FID06h、Admin Queue</td><td>CSEL1、CSS7</td><td>控制器 7</td></tr><tr><td>FID06h、Admin Queue</td><td>CSEL2、CSS7</td><td>primary7 所屬 secondaries，非 primary7 本身</td></tr><tr><td>FID06h、controller7</td><td>IFC 由 0 改 2</td><td>從 Admin Queue 改為 Management Endpoint</td></tr></tbody></table></div><figcaption>每列假設相關能力與入口均受支援；這些選擇分別管控制器集合與接收入口。來源：Base Figures365、366。</figcaption></figure>

<!-- claim:LOCKDOWN-TARGETS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">IFC 選命令接收介面：00b 為 Admin Submission Queue，01b 為該 Queue 加 Management Endpoint，10b 為 Management Endpoint。CSEL 選全部控制器、單一控制器或某 primary 的 secondary controllers，CSS 再提供所需控制器編號。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Admin Submission Queue</dt><dd>主機提交管理命令的佇列，本文也簡稱 Admin Queue。</dd></div><div><dt>secondary</dt><dd>附屬控制器；本篇只需知道其與 primary 的所屬關係，不以名稱推論效能或優先級。</dd></div><div><dt>primary</dt><dd>主要控制器；本篇 CSEL=2 用它的 Identifier 選其所屬 secondary 控制器集合。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.16</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.16, 文件頁 406-407, PDF 頁 432-433</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span><span class="paragraph-text">要限制控制器 7 的 Admin Queue：CSEL=1、CSS=7、IFC=00b。送 Lockdown 的控制器與受影響的控制器不能混為一談；IFC 也不是在描述這次 Lockdown 是從哪裡送進去。</span></p></aside>
</section>
<section class="lesson" id="module-lockdown-query"><h2 id="heading-lockdown-query"><span class="section-number">04</span> 把 LID 14h 的查詢問題寫完整</h2>
<!-- claim:LOCKDOWN-QUERY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">LID 14h 的 SCP 選項目種類，CNTTS=00b 查可禁止、01b 查 Admin Queue 目前禁止、10b 查 Management Endpoint 目前禁止。ELPF=0 使用一般格式；ELPF=1 使用增強格式，並以 LSI.CNTLID 選控制器，FFFFh 查所有控制器。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CNTLID</dt><dd>Controller Identifier；控制器的識別編號，增強 Log 查詢以 FFFFh 指定全體。</dd></div><div><dt>CNTTS</dt><dd>Contents；選可禁止清單，或某種接收介面目前禁止的清單。</dd></div><div><dt>LSI</dt><dd>Log Specific Identifier；Get Log 中依 Log 種類解讀的 16-bit 識別值。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.20</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.20, 文件頁 279-280, PDF 頁 305-306</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">讀 512 bytes 的一般格式、查 Admin Queue 已禁止 FID：LID=14h、SCP=2、CNTTS=1、ELPF=0，NUMD=127，得到 CDW10=007F1214h。這是查詢，不會新增任何禁止項目。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NUMD</dt><dd>Number of Dwords；本篇 Get Log 傳輸長度採 Dword 數量減 1。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-lockdown-basic"><h2 id="heading-lockdown-basic"><span class="section-number">05</span> 一般格式：一串代碼代表全體共同的項目</h2>
<figure><figcaption><strong>把 6 個 bytes 分成 header 與有效清單</strong></figcaption><div class="table-wrap"><table><thead><tr><th scope="col">byte offset</th><th scope="col">範例值</th><th scope="col">如何解讀</th></tr></thead><tbody><tr><td>0</td><td>12h</td><td>CS1：Admin 已禁止；SS2：FID</td></tr><tr><td>1～2</td><td>00 00</td><td>保留，不是清單內容</td></tr><tr><td>3</td><td>02h</td><td>LNGTH=2，直接計數</td></tr><tr><td>4～5</td><td>06 07</td><td>2 筆 FID：06h、07h</td></tr><tr><td>6～511</td><td>保留</td><td>不解析為其他 FID</td></tr></tbody></table></div><figcaption>索引 0、offset4、FID06h 是第幾筆、存在哪、代表什麼的三種答案。來源：Base Figure276。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>byte offset</dt><dd>以 byte 計算、相對結構起點的距離；索引 2 不一定代表 offset2。</dd></div><div><dt>header</dt><dd>資料結構開頭的固定欄位區，用來說明後方內容的種類、長度或數量。</dd></div><div><dt>offset</dt><dd>offset；從指定起點算出的位移。它回答「離起點多遠」，不等於 index。</dd></div><div><dt>LNGTH</dt><dd>Length；一般格式代碼清單的 byte 數，直接計數，0 表示空清單。</dd></div></dl>
<!-- claim:LOCKDOWN-BASIC -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span><span class="paragraph-text">一般 Log 固定 512 bytes，CFILA 回報查詢種類，LNGTH 直接表示後方代碼清單的 byte 數，清單從 byte 4 開始並由小到大排列。對全體控制器的可禁止項目與 Admin Queue 目前禁止項目，不能把一般清單當成任何一台控制器的聯集。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CFILA</dt><dd>Command and Feature Identifier List Attributes；一般 Log 中描述清單種類的屬性。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.20</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.20, 文件頁 281, PDF 頁 307</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="05.02">05.02.</span><span class="paragraph-text">回覆開頭 12 00 00 02 06 07：CFILA=12h 表示 Admin Queue 已禁止 FID；LNGTH=2，後面兩個 FID 是 06h、07h。02h 是長度，不是第三個 FID。</span></p></aside>
</section>
<section class="lesson" id="module-lockdown-enhanced"><h2 id="heading-lockdown-enhanced"><span class="section-number">06</span> 增強格式：分清至少一台與全部控制器</h2>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 450" role="img"><title>A／B 的禁止狀態，如何變成兩種 Log</title><desc>固定查 SCP2、CNTTS1；假設 subsystem 只有 A、B。全體增強清單保留 06h 的部分控制器資訊，一般格式只留下全體共同的 07h。來源：Base Figures276～278。</desc><rect x="20" y="20" width="345" height="90" rx="6" class="v-command"/><text x="192.5" y="58.5" text-anchor="middle" font-size="17">控制器 A 目前禁止</text><text x="192.5" y="83.5" text-anchor="middle" font-size="17">FID 06h, 07h</text><rect x="395" y="20" width="345" height="90" rx="6" class="v-command"/><text x="567.5" y="58.5" text-anchor="middle" font-size="17">控制器 B 目前禁止</text><text x="567.5" y="83.5" text-anchor="middle" font-size="17">FID 07h</text><path d="M190,110 L190,175" class="v-line"/><path d="M186,168 L190,175 L194,168" class="v-line"/><path d="M565,110 L565,175" class="v-line"/><path d="M561,168 L565,175 L569,168" class="v-line"/><rect x="20" y="175" width="720" height="75" rx="6" class="v-object"/><text x="380.0" y="218.5" text-anchor="middle" font-size="17">相同 SCP／CNTTS，改變回覆格式</text><path d="M190,250 L190,315" class="v-line"/><path d="M186,308 L190,315 L194,308" class="v-line"/><path d="M565,250 L565,315" class="v-line"/><path d="M561,308 L565,315 L569,308" class="v-line"/><rect x="20" y="315" width="345" height="110" rx="6" class="v-object"/><text x="192.5" y="363.5" text-anchor="middle" font-size="17">一般 ELPF0</text><text x="192.5" y="388.5" text-anchor="middle" font-size="17">LNGTH=1 → 07h</text><rect x="395" y="315" width="345" height="110" rx="6" class="v-success"/><text x="567.5" y="351.0" text-anchor="middle" font-size="17">ELPF1 / CNTLID=FFFFh</text><text x="567.5" y="376.0" text-anchor="middle" font-size="17">06h: ACNTL0</text><text x="567.5" y="401.0" text-anchor="middle" font-size="17">07h: ACNTL1</text></svg></div><figcaption>固定查 SCP2、CNTTS1；假設 subsystem 只有 A、B。全體增強清單保留 06h 的部分控制器資訊，一般格式只留下全體共同的 07h。來源：Base Figures276～278。</figcaption></figure>

<!-- claim:LOCKDOWN-ENHANCED -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.01">06.01.</span><span class="paragraph-text">增強 Log 用 16-byte header 說明版本、查詢種類、CNTLID、SZE、NCFID 與 CFIDS，描述器按 CFI 遞增排列。CNTLID=FFFFh 時清單含至少一台控制器回報的項目；每筆 ACNTL=1 才表示所有控制器都回報這項。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>ACNTL</dt><dd>All Controllers；1 表示所有控制器回報此項，0 表示至少一台但非全部。</dd></div><div><dt>CFIDS</dt><dd>Command and Feature Identifier Descriptors Size；增強 Log 每筆描述器占用的 byte 數。</dd></div><div><dt>NCFID</dt><dd>Number of Command and Feature Identifier Descriptors；增強 Log 中的描述器數量，直接計數。</dd></div><div><dt>CFI</dt><dd>Command and Feature Identifier；一筆增強描述器中，依 SCP 解讀的操作代碼。</dd></div><div><dt>SZE</dt><dd>Size；增強 Log 的完整 byte 大小，不是項目數。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.20</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.20, 文件頁 282-283, PDF 頁 308-309</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="06.02">06.02.</span><span class="paragraph-text">A 禁止 06h、07h，B 只禁止 07h：查全體 Admin Queue 已禁止 FID，增強清單可回 (06h,ACNTL=0)、(07h,ACNTL=1)。06h 的 0 不是「沒禁止」，而是「不是全部都有」。</span></p></aside>
</section>
<section class="lesson" id="module-lockdown-command"><h2 id="heading-lockdown-command"><span class="section-number">07</span> 完整編碼一次禁止與解除操作</h2>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 415" role="img"><title>同一目標：禁止與允許只差 bit4</title><desc>假設功能、controller7 與 FID06h 均符合條件，且 Lockdown 入口可執行。低位 SCP2 選 FID；高位 CSEL1 仍需 CDW14 的 CSS7 提供實際編號。來源：Base Figures365、366。</desc><rect x="20" y="20" width="720" height="80" rx="6" class="v-command"/><text x="380.0" y="53.5" text-anchor="middle" font-size="17">OPC=24h · CSEL1 · OFI06h · IFC0 · SCP2</text><text x="380.0" y="78.5" text-anchor="middle" font-size="17">CSS7 → CDW14=00070000h</text><path d="M190,100 L190,175" class="v-line"/><path d="M186,168 L190,175 L194,168" class="v-line"/><path d="M565,100 L565,175" class="v-line"/><path d="M561,168 L565,175 L569,168" class="v-line"/><rect x="20" y="175" width="345" height="90" rx="6" class="v-object"/><text x="192.5" y="213.5" text-anchor="middle" font-size="17">PRHBT=1</text><text x="192.5" y="238.5" text-anchor="middle" font-size="17">禁止：00010612h</text><rect x="395" y="175" width="345" height="90" rx="6" class="v-success"/><text x="567.5" y="213.5" text-anchor="middle" font-size="17">PRHBT=0</text><text x="567.5" y="238.5" text-anchor="middle" font-size="17">允許：00010602h</text><rect x="20" y="330" width="720" height="60" rx="6" class="v-object"/><text x="380.0" y="366.0" text-anchor="middle" font-size="17">每次成功後，按相同目標讀回 LID14h</text></svg></div><figcaption>假設功能、controller7 與 FID06h 均符合條件，且 Lockdown 入口可執行。低位 SCP2 選 FID；高位 CSEL1 仍需 CDW14 的 CSS7 提供實際編號。來源：Base Figures365、366。</figcaption></figure>

<!-- claim:LOCKDOWN-COMMAND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.01">07.01.</span><span class="paragraph-text">Lockdown 使用 CDW10 的 CSEL、OFI、IFC、PRHBT、SCP，以及 CDW14 的 CSS／UIDX。PRHBT=1 禁止、0 允許；其他欄位保留原本要作用的種類、介面與控制器集合。重複禁止已禁止項目或允許已允許項目，本身不是錯誤。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>UIDX</dt><dd>UUID Index；命令帶入的 UUID List 索引，0 不指定 UUID。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.16</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.16, 文件頁 405-407, PDF 頁 431-433</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="07.02">07.02.</span><span class="paragraph-text">假設能力與清單均允許：禁止控制器 7 的 Admin Queue 設定 FID 06h，CDW10=00010612h、CDW14=00070000h。解除同一項限制只改 PRHBT=0，CDW10=00010602h；兩次都使用 Lockdown opcode 24h。</span></p></aside>
</section>
<section class="lesson" id="module-lockdown-result"><h2 id="heading-lockdown-result"><span class="section-number">08</span> 把設定失敗與命令被禁止分開判斷</h2>
<!-- claim:LOCKDOWN-RESULT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.01">08.01.</span><span class="paragraph-text">Lockdown 設定本身可因項目不可禁止、介面不支援或控制器選擇無效而失敗。28h 是 Prohibition of Command Execution Not Supported；1Fh 是 Invalid Controller Identifier。已受限制的 Admin 命令則回通用狀態 Command Prohibited by Command and Feature Lockdown。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.16</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.16, 文件頁 407-408, PDF 頁 433-434</p></details>
<!-- claim:LOCKDOWN-PROHIBITED-EXECUTION -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.02">08.02.</span><span class="paragraph-text">受限制的操作從 Admin Queue 收到時，命令以 Command Prohibited by Command and Feature Lockdown 中止；從 Management Endpoint 收到時，回 Access Denied Error Response。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.5, 文件頁 598, PDF 頁 624</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="08.03">08.03.</span><span class="paragraph-text">第一次 Lockdown 成功；第二次送出的 Set Features 被禁止，回 SCT=0、SC=23h。若第一次 Lockdown 就因 OFI 不可禁止而回 SCT=1、SC=28h，代表沒有得到成功設定的證據，不能把這兩種失敗當成一件事。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>SCT</dt><dd>Status Code Type；指定完成狀態碼所屬類別，需與 SC 一起解讀。</dd></div><div><dt>SC</dt><dd>Status Code；指定所選 SCT 類別中的完成結果。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-lockdown-persistence"><h2 id="heading-lockdown-persistence"><span class="section-number">09</span> 限制何時消失，要看 CSEL 與持續性設定</h2>
<figure><figcaption><strong>一個 subsystem power cycle 之後，哪些限制保留？</strong></figcaption><div class="table-wrap"><table><thead><tr><th scope="col">建立限制時的 CSEL</th><th scope="col">Lockdown Persistence</th><th scope="col">斷電循環後的規則</th></tr></thead><tbody><tr><td>0：全部控制器</td><td>已啟用</td><td>保留，後續 Lockdown 可解除</td></tr><tr><td>0：全部控制器</td><td>已停用</td><td>原禁止不跨 power cycle 保留</td></tr><tr><td>1：單一控制器</td><td>任一狀態</td><td>不因 LDPE1 而跨 power cycle 保留</td></tr><tr><td>2：指定 primary 的 secondaries</td><td>任一狀態</td><td>同樣在 power cycle 或後續解除時結束</td></tr></tbody></table></div><figcaption>比較的是 power cycle；不能把一般 Controller Reset 代入這一欄。凍結與認證例外則在正文另行說明其條件。來源：Base §8.1.5。</figcaption></figure>

<!-- claim:LOCKDOWN-PERSISTENCE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.01">09.01.</span><span class="paragraph-text">CSEL=0 的全體限制在 Lockdown Persistence 啟用時跨 power cycle 保留；停用時持續到 subsystem power cycle 或後續解除。CSEL=1、2 的限制持續到 power cycle 或後續解除，不因 LDPE=1 自動取得全體限制的跨斷電保留規則。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>LDPE</dt><dd>Lockdown Persistence Enable；啟用全體限制跨 power cycle 保留的設定。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.5, 文件頁 598-599, PDF 頁 624-625</p></details>
<!-- claim:LOCKDOWN-PERSISTENCE-EXCEPTIONS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.02">09.02.</span><span class="paragraph-text">持續性啟用時，未凍結或無認證解凍支援的 Lockdown Persistence Personality，不能透過 Lockdown 禁止 Set Features 或 FID 22h。若任一 personality 支援認證解凍，特定 CDP Authentication 的 Security Send／Receive 必須仍被允許。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>personality</dt><dd>規格中的一組裝置配置；本篇只用 Lockdown Persistence 這一種配置及其必要條件。</dd></div><div><dt>CDP</dt><dd>Configurable Device Personality；將裝置配置分為可查詢、設定或凍結的 personality。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.25.4.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.25.4.1, 文件頁 494, PDF 頁 520</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="09.03">09.03.</span><span class="paragraph-text">同時有「CSEL=0 禁止 FID 06h」與「CSEL=1 禁止 FID 07h」，且 Lockdown Persistence 已啟用。subsystem power cycle 後，前者按全體持續性規則保留，後者不因這個設定而跨斷電保留。</span></p></aside>
</section>
<section class="lesson" id="module-lockdown-uuid"><h2 id="heading-lockdown-uuid"><span class="section-number">10</span> 同一廠商 FID 有不同定義時，用 UUID 選版本</h2>
<!-- claim:LOCKDOWN-UUID -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="10.01">10.01.</span><span class="paragraph-text">廠商定義 FID 的 Lockdown 在 SCP=2 且相關命令與項目支援 UUID 選擇時，使用 CDW14.UIDX 選 UUID List 項目。LID 14h 對 SCP=2 的廠商 FID 查詢也可使用 UIDX；SCP≠2 時忽略 UIDX。UIDX 是清單索引，不是 FID 或 byte offset。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.16</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.16, 文件頁 406-407, PDF 頁 432-433</p></details>
<!-- claim:LOCKDOWN-UUID-VALIDITY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="10.02">10.02.</span><span class="paragraph-text">UIDX=0 不指定 UUID；非零索引需指向該資訊支援的有效 UUID。全 0、NVMe Invalid UUID 或不支援於該資訊的 UUID 會導向 Invalid Field in Command。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express，主機與非揮發性記憶體子系統之間的介面規範家族。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.31.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.31.2, 文件頁 737-738, PDF 頁 763-764</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="10.03">10.03.</span><span class="paragraph-text">假設兩份廠商定義都使用 FID C0h，UUID List 的第 2 項對應所需定義。使用 UIDX=2；不是把 C0h 填 UIDX，也不是填第 2 項的 byte offset 64。</span></p></aside>
</section>
<section id="spec-reading"><h2>接著打開 Spec 看什麼</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.01">11.01.</span><span class="paragraph-text">以下按概念列出閱讀位置。報告時先用上面的流程說明問題，再打開對應章節看欄位與完整條件。中文教學 HTML 另有本篇全部圖表的逐圖重點、案例與細節。</span></p>
<div class="table-wrap"><table><thead><tr><th scope="col">要說明的觀念</th><th scope="col">Spec 閱讀位置</th></tr></thead><tbody><tr><td>先理解：限制的是哪個操作從哪裡進來</td><td>Base 2.4 §8.1.5</td></tr><tr><td>先查支援層級，再查可禁止項目</td><td>Base 2.4 §8.1.5</td></tr><tr><td>介面與控制器是兩個獨立選擇</td><td>Base 2.4 §5.2.16</td></tr><tr><td>把 LID 14h 的查詢問題寫完整</td><td>Base 2.4 §5.2.13.1.20</td></tr><tr><td>一般格式：一串代碼代表全體共同的項目</td><td>Base 2.4 §5.2.13.1.20</td></tr><tr><td>增強格式：分清至少一台與全部控制器</td><td>Base 2.4 §5.2.13.1.20</td></tr><tr><td>完整編碼一次禁止與解除操作</td><td>Base 2.4 §5.2.16</td></tr><tr><td>把設定失敗與命令被禁止分開判斷</td><td>Base 2.4 §5.2.16 · Base 2.4 §8.1.5</td></tr><tr><td>限制何時消失，要看 CSEL 與持續性設定</td><td>Base 2.4 §8.1.5 · Base 2.4 §5.2.30.1.25.4.1</td></tr><tr><td>同一廠商 FID 有不同定義時，用 UUID 選版本</td><td>Base 2.4 §5.2.16 · Base 2.4 §8.1.31.2</td></tr></tbody></table></div>
<a class="reading-link" href="/DOCS/nvme-spec-report/base-command-feature-lockdown/tutorial-zh-tw.html">開啟完整中文教學與逐圖解釋 →</a></section>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:lockdown-eligibility -->
<details class="review-question" id="qa-lockdown-eligibility"><summary>1. LID 14h 可禁止清單含 06h，就代表目前已禁止嗎？</summary>
<div data-qa-answer="lockdown-eligibility"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="12.01">12.01.</span><span class="paragraph-text">不代表。先看 SCP 確認它是哪種代碼，CNTTS=0 只表示可禁止。要查目前 Admin Queue 限制，應用同一種類並選 CNTTS=1，再配合正確格式與控制器範圍。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.20, 文件頁 279-280, PDF 頁 305-306</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.20, 文件頁 281, PDF 頁 307</p>
</details></details>
<!-- qa:lockdown-union -->
<details class="review-question" id="qa-lockdown-union"><summary>2. 全體增強清單回 06 00，能說全部控制器都允許 06h 嗎？</summary>
<div data-qa-answer="lockdown-union"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="12.02">12.02.</span><span class="paragraph-text">不能。這是一筆已回報的 CFI=06h，ACNTL=0 表示至少一台但非全部符合這次查詢。如果 CNTTS=1，它表示只有部分控制器目前禁止；要找是哪台需用特定 CNTLID 查詢。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.20, 文件頁 282-283, PDF 頁 308-309</p>
</details></details>
<!-- qa:lockdown-encoding -->
<details class="review-question" id="qa-lockdown-encoding"><summary>3. 要解除 controller7 的 FID06h 限制，能只送 PRHBT=0 嗎？</summary>
<div data-qa-answer="lockdown-encoding"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="12.03">12.03.</span><span class="paragraph-text">還需保留 SCP=2、OFI=06h、IFC=0、CSEL=1、CSS=7 等相同選擇，並確保執行 Lockdown 的入口仍允許。PRHBT 只決定禁止或允許，不指定對象。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.16, 文件頁 405-407, PDF 頁 431-433</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.16, 文件頁 406-407, PDF 頁 432-433</p>
</details></details>
<!-- qa:lockdown-persist -->
<details class="review-question" id="qa-lockdown-persist"><summary>4. LDPE=1，是否每個 CSEL 建立的限制都能跨斷電保留？</summary>
<div data-qa-answer="lockdown-persist"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="12.04">12.04.</span><span class="paragraph-text">不是。跨 power cycle 的 Lockdown Persistence 規則針對 CSEL=0 的全體限制；CSEL=1、2 仍依其在 power cycle 或後續解除時結束的規則。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.5, 文件頁 598-599, PDF 頁 624-625</p>
</details></details>
<!-- qa:lockdown-offset -->
<details class="review-question" id="qa-lockdown-offset"><summary>5. 增強 Log 第二筆在 byte18，UUID 第二項在 byte64，兩個 2 可以互用嗎？</summary>
<div data-qa-answer="lockdown-offset"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="12.05">12.05.</span><span class="paragraph-text">不能。CFIDS=2 時增強 Log 第 2 筆從 16+1×2=18 開始；UIDX=2 選 UUID 第 2 項，其 entry 從 64 開始。OT=0 的 Get Log 起點還要 4-byte 對齊，所以讀含 byte18 的資料可從 16 開始。索引和值的位置是不同單位。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.20, 文件頁 282-283, PDF 頁 308-309</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.20, 文件頁 279-280, PDF 頁 305-306</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.16, 文件頁 406-407, PDF 頁 432-433</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
