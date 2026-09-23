---
permalink: /nvme/namespace-write-protection-zh-tw/
layout: post
read_time: true
show_date: true
title: "NVMe Namespace Write Protection：狀態、控制與命令行為"
date: 2026-09-23
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
[English]({% post_url 2026-09-23-nvme-namespace-write-protection-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">一份已寫好的資料要繼續提供讀取，又要避免後續命令改動它，可以對所在的 namespace 設定寫入保護。Namespace Write Protection 不只是一個開關：它有可解除、直到斷電、永久等不同狀態，並把裝置支援、進入許可與實際保護分開。本篇把這些關係接到 FID 84h，最後說明保護如何改變命令處理。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Namespace Write Protection</dt><dd>namespace寫入保護；控制一份namespace能否接受受限制的修改操作。</dd></div><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div><div><dt>FID</dt><dd>Feature Identifier；指定要讀取或設定哪一項 Feature 的編號。</dd></div></dl>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>保護的對象與邊界</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">設定跟著 namespace，所有附接它的控制器都要遵守。先分清資料對象與傳送命令的控制器，再看會影響多個 namespace 的操作。</span></p></article>
<article><span class="axis-number">02</span><h3>用事件追蹤狀態</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">四種狀態各有允許的進入與離開路徑。Set Features、控制器重設與 power cycle 造成的結果不同，圖上的箭頭必須帶著事件讀。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>power cycle</dt><dd>電源循環，即斷電後重新上電；不等同於所有形式的控制器重設。</dd></div></dl></article>
<article><span class="axis-number">03</span><h3>從能力走到成功設定</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">NWPC 回答能不能支援，WPC 決定特定進入要求是否獲准，WPS 回報目前狀態。設定成功還包含將既有寫入快取提交到媒體。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NWPC</dt><dd>Namespace Write Protection Capabilities，控制器支援哪些保護狀態的位元欄位。</dd></div><div><dt>WPC</dt><dd>Write Protection Control，決定是否接受進入特定保護狀態之要求的控制欄位。</dd></div><div><dt>WPS</dt><dd>Write Protection State，namespace目前的寫入保護狀態代碼。</dd></div></dl></article>
<article><span class="axis-number">04</span><h3>保護後如何使用與觀察</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="04-01">04-01</span><span class="paragraph-text">Read、Flush、管理命令各有處理規則；跨 namespace 的操作也受影響。用目前 WPS、完成狀態與健康警告回答各自的問題。</span></p></article>
</div>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">讀者已學過 OS 與 Computer Organization，並了解 SSD 基本概念。本文使用 namespace 7／8 與控制器 A／B 作為說明性範例；數值不代表裝置一定具備這些配置。</span></p>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.03">00.03.</span><span class="paragraph-text">先掌握四種狀態，再讀支援與控制位，接著完成一個設定案例；最後把狀態套回實際命令。欄位說明按相關概念分組，可從正文直接連到對應圖表。</span></p>
<div class="overview-connections"><h3>把主軸連起來</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.04">00.04.</span><span class="paragraph-text">全文以 namespace 7 的資料集為例：先決定需要哪種保護與解除方式，再確認裝置能否接受該轉換，等待設定成功，最後解釋哪些操作還能執行。每個欄位都有一個具體要回答的問題。</span></p>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.05">00.05.</span><span class="paragraph-text">最容易混淆的三組關係是：支援能力與進入許可、不可保存與跨斷電保留、namespace 保護狀態與全體媒體健康警告。後面的對比會分別處理它們。</span></p>
</div>
</section>
<section class="lesson" id="module-nwp-model"><h2 id="heading-nwp-model"><span class="section-number">01</span> 先看保護誰，再看四種狀態</h2>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 410" role="img"><title>設定經由控制器送出，保護跟著 namespace</title><desc>A、B 的箭頭都指向同一份namespace7；它們必須遵守相同保護。下方namespace8是另一個設定對象。此圖說明附接關係，不表示命令執行順序。來源：Base §8.1.18。</desc><rect x="20" y="20" width="340" height="85" rx="6" class="v-command"/><text x="190.0" y="56.0" text-anchor="middle" font-size="17">Controller A</text><text x="190.0" y="81.0" text-anchor="middle" font-size="17">送出 Set FID84h</text><rect x="400" y="20" width="340" height="85" rx="6" class="v-command"/><text x="570.0" y="56.0" text-anchor="middle" font-size="17">Controller B</text><text x="570.0" y="81.0" text-anchor="middle" font-size="17">同樣遵守 WPS</text><path d="M190,105 L190,165" class="v-line"/><path d="M186,158 L190,165 L194,158" class="v-line"/><path d="M570,105 L570,165" class="v-line"/><path d="M566,158 L570,165 L574,158" class="v-line"/><rect x="20" y="165" width="720" height="90" rx="6" class="v-success"/><text x="380.0" y="203.5" text-anchor="middle" font-size="17">Namespace 7 · WPS=1</text><text x="380.0" y="228.5" text-anchor="middle" font-size="17">所有附接的控制器共同遵守</text><rect x="20" y="305" width="720" height="80" rx="6" class="v-object"/><text x="380.0" y="338.5" text-anchor="middle" font-size="17">Namespace 8 · WPS=0</text><text x="380.0" y="363.5" text-anchor="middle" font-size="17">獨立的 namespace 設定</text></svg></div><figcaption>A、B 的箭頭都指向同一份namespace7；它們必須遵守相同保護。下方namespace8是另一個設定對象。此圖說明附接關係，不表示命令執行順序。來源：Base §8.1.18。</figcaption></figure>

<!-- claim:NWP-MODEL -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">Namespace Write Protection 讓主機控制單一 namespace 的寫入保護狀態。支援這項能力時，No Write Protect 與 Write Protect 必備；Until Power Cycle 與 Permanent 兩種狀態選用。namespace 建立時從 No Write Protect 開始；同一 namespace 的狀態須由所有附接它的控制器共同遵守。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.18</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.18, 文件頁 664-666, PDF 頁 690-692</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">說明性範例：namespace 7 由 A、B 共同存取。經 A 成功設為 WPS=1 後，B 也必須遵守保護；不能把設定命令的傳送入口當作保護的邊界。</span></p></aside>
</section>
<section class="lesson" id="module-nwp-transitions"><h2 id="heading-nwp-transitions"><span class="section-number">02</span> 沿著狀態圖理解解除與重設</h2>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 580" role="img"><title>四種狀態：先看起點，再看事件</title><desc>普通箭頭為Set Features；通往2、3的箭頭另須能力、WPC及相關配置條件成立。圖中2回到0的箭頭由power cycle觸發，3沒有解除箭頭。為了讓線條清楚，兩條垂直分支分別標明可從0或1出發。來源：Base Figures735／736、§5.2.30.1.38。</desc><rect x="50" y="30" width="275" height="90" rx="6" class="v-success"/><text x="187.5" y="68.5" text-anchor="middle" font-size="17">0 · No Write Protect</text><text x="187.5" y="93.5" text-anchor="middle" font-size="17">建立時的狀態</text><rect x="435" y="30" width="275" height="90" rx="6" class="v-command"/><text x="572.5" y="68.5" text-anchor="middle" font-size="17">1 · Write Protect</text><text x="572.5" y="93.5" text-anchor="middle" font-size="17">可由 Set 解除</text><path d="M325,55 L435,55" class="v-line"/><path d="M428,51 L435,55 L428,59" class="v-line"/><path d="M435,95 L325,95 M332,91 L325,95 L332,99" class="v-line"/><rect x="30" y="185" width="330" height="65" rx="6" class="v-command"/><text x="195.0" y="223.5" text-anchor="middle" font-size="17">從 0 或 1；要求 WPS2</text><rect x="400" y="185" width="330" height="65" rx="6" class="v-command"/><text x="565.0" y="223.5" text-anchor="middle" font-size="17">從 0 或 1；要求 WPS3</text><path d="M195,250 L195,315" class="v-line"/><path d="M191,308 L195,315 L199,308" class="v-line"/><path d="M565,250 L565,315" class="v-line"/><path d="M561,308 L565,315 L569,308" class="v-line"/><rect x="30" y="315" width="330" height="110" rx="6" class="v-decision"/><text x="195.0" y="363.5" text-anchor="middle" font-size="17">2 · Until Power Cycle</text><text x="195.0" y="388.5" text-anchor="middle" font-size="17">Set 不能改變此狀態</text><rect x="400" y="315" width="330" height="110" rx="6" class="v-decision"/><text x="565.0" y="363.5" text-anchor="middle" font-size="17">3 · Permanent</text><text x="565.0" y="388.5" text-anchor="middle" font-size="17">沒有解除路徑</text><path d="M195,425 L195,485" class="v-line"/><path d="M191,478 L195,485 L199,478" class="v-line"/><rect x="30" y="485" width="330" height="70" rx="6" class="v-success"/><text x="195.0" y="526.0" text-anchor="middle" font-size="17">Power cycle → WPS0</text><rect x="400" y="485" width="330" height="70" rx="6" class="v-object"/><text x="565.0" y="526.0" text-anchor="middle" font-size="17">power cycle 後仍為 3</text></svg></div><figcaption>普通箭頭為Set Features；通往2、3的箭頭另須能力、WPC及相關配置條件成立。圖中2回到0的箭頭由power cycle觸發，3沒有解除箭頭。為了讓線條清楚，兩條垂直分支分別標明可從0或1出發。來源：Base Figures735／736、§5.2.30.1.38。</figcaption></figure>

<!-- claim:NWP-TRANSITIONS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">Set Features 可在 0 與 1 之間切換，也可從 0 或 1 進入受支援且獲准的 2 或 3。處於 2 或 3 時，用 Set Features 要求改變狀態會得到 Feature Not Changeable。一般狀態機中，2 經 power cycle 回到 0；沒有 power cycle 的 Controller Level Reset 不解除它。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Controller Level Reset</dt><dd>控制器層級重設；狀態2是否解除仍要辨認有沒有發生power cycle。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.18; 5.2.30.1.38</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.18; 5.2.30.1.38, 文件頁 512-513,664-665, PDF 頁 538-539,690-691</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">同樣先成功設為 WPS=2：沒有斷電的控制器重設後仍為 2；power cycle 後為 0。若原本是 WPS=1，兩種事件之後都仍為 1。</span></p></aside>
</section>
<section class="lesson" id="module-nwp-controls"><h2 id="heading-nwp-controls"><span class="section-number">03</span> 能力、進入許可與目前狀態是三件事</h2>
<figure><figcaption><strong>相同的數字，放在不同欄位意思不同</strong></figcaption><div class="table-wrap"><table><thead><tr><th scope="col">觀察到的值</th><th scope="col">它回答的問題</th><th scope="col">不能推出的結論</th></tr></thead><tbody><tr><td>NWPC=03h</td><td>支援0／1及2，不支援3</td><td>目前已永久保護</td></tr><tr><td>WPC=03h</td><td>允許處理進入2與3的要求</td><td>所有namespace已保護</td></tr><tr><td>WPS=3</td><td>這個namespace已永久保護</td><td>這是一份支援bitmap</td></tr><tr><td>MDS=1</td><td>多domain；禁止進入2</td><td>禁止所有寫入保護</td></tr></tbody></table></div><figcaption>每列獨立示範欄位意義，不是同一台裝置的完整配置。Source：Base Figures338／756／541。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>domain</dt><dd>subsystem內用來界定通訊與故障影響的範圍；本篇用它判斷是否允許直到斷電的保護。</dd></div><div><dt>MDS</dt><dd>Multi-Domain Subsystem，Identify Controller中表示支援多domain的位元。</dd></div></dl>
<!-- claim:NWP-CONTROLS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">NWPC 宣告控制器支援哪些狀態；RPMB 的 WPC 控制是否允許命令進入狀態 2 或 3；FID 84h 的 WPS 才是 namespace 目前的狀態。WPUPCC=0 或 PWPC=0 會阻止對應的進入要求。MDS=1 的多 domain subsystem 禁止使用狀態 2，即使相關能力與控制位已設為 1。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>WPUPCC</dt><dd>Write Protect Until Power Cycle Control，WPC內允許進入狀態2的控制位。</dd></div><div><dt>PWPC</dt><dd>Permanent Write Protect Control，WPC內允許進入永久保護的控制位。</dd></div><div><dt>RPMB</dt><dd>Replay Protected Memory Block，使用認證與防重播機制存取的記憶區；本篇只取其WPC控制欄位。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.18; 5.2.30.1.38</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.18; 5.2.30.1.38, 文件頁 512-513,664-665, PDF 頁 538-539,690-691</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span><span class="paragraph-text">NWPC=07h、WPC=01h、目前 WPS=0：單 domain 可在其餘條件滿足時要求 WPS=2；WPS=3 因 PWPC=0 被拒絕。若改成 MDS=1，WPS=2 的要求也會被拒絕。</span></p></aside>
</section>
<section class="lesson" id="module-nwp-configure"><h2 id="heading-nwp-configure"><span class="section-number">04</span> 把查詢、設定與成功完成接起來</h2>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 610" role="img"><title>成功切入保護，包含先把既有快取提交到媒體</title><desc>範例採WPS0 → 1、NSID7。主機宜先等舊命令完成；控制器在轉換時提交該namespace的快取資料與metadata。完成後才提交的命令必須用新設定；較早在途的命令不能一概推定。來源：Base §§5.2.30.1、5.2.30.1.38、5.2.30.4。</desc><rect x="20" y="20" width="720" height="70" rx="6" class="v-command"/><text x="380.0" y="61.0" text-anchor="middle" font-size="17">主機：先等待前一批命令完成</text><path d="M380,90 L380,130" class="v-line"/><path d="M376,123 L380,130 L384,123" class="v-line"/><rect x="20" y="130" width="720" height="90" rx="6" class="v-command"/><text x="380.0" y="168.5" text-anchor="middle" font-size="17">Set · NSID7 · FID84h · SV0</text><text x="380.0" y="193.5" text-anchor="middle" font-size="17">CDW11 = 00000001h</text><path d="M380,220 L380,260" class="v-line"/><path d="M376,253 L380,260 L384,253" class="v-line"/><rect x="20" y="260" width="720" height="95" rx="6" class="v-object"/><text x="380.0" y="301.0" text-anchor="middle" font-size="17">控制器：將此 namespace 的快取提交到媒體</text><text x="380.0" y="326.0" text-anchor="middle" font-size="17">包含 data 與 metadata</text><path d="M380,355 L380,395" class="v-line"/><path d="M376,388 L380,395 L384,388" class="v-line"/><rect x="20" y="395" width="720" height="75" rx="6" class="v-success"/><text x="380.0" y="438.5" text-anchor="middle" font-size="17">完成設定後，回覆成功 CQE</text><path d="M380,470 L380,510" class="v-line"/><path d="M376,503 L380,510 L384,503" class="v-line"/><rect x="20" y="510" width="720" height="75" rx="6" class="v-success"/><text x="380.0" y="541.0" text-anchor="middle" font-size="17">Get · SEL0 → CQE DW0 = 1</text><text x="380.0" y="566.0" text-anchor="middle" font-size="17">確認目前保護狀態</text></svg></div><figcaption>範例採WPS0 → 1、NSID7。主機宜先等舊命令完成；控制器在轉換時提交該namespace的快取資料與metadata。完成後才提交的命令必須用新設定；較早在途的命令不能一概推定。來源：Base §§5.2.30.1、5.2.30.1.38、5.2.30.4。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>metadata</dt><dd>隨 logical block 儲存的附加資料，可包含資料保護資訊，也可有其他用途。</dd></div><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div></dl>
<!-- claim:NWP-CONFIGURE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">以有效且 active 的 NSID 選 namespace；Get FID 84h、SEL=0 讀目前 WPS，Set 在 CDW11 bits 2:0 放新 WPS。設定不可使用 SV=1；SEL=1 沒有 default 可讀，回 Invalid Field in Command。成功進入寫入保護時，控制器必須把該 namespace 的所有揮發性寫入快取資料及 metadata 寫入非揮發媒體。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>active</dt><dd>已附接於處理命令之控制器的namespace狀態。</dd></div><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div><div><dt>SEL</dt><dd>Select，Get Features中選擇目前值、預設值、已保存值或能力的欄位。</dd></div><div><dt>SV</dt><dd>Save，Set Features中要求保存屬性值的位元。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.38</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.38, 文件頁 512-513, PDF 頁 538-539</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">namespace 7 原為 0：Set 的 CDW10=00000084h、CDW11=00000001h；等待成功完成後，Get SEL=0 回 DW0=1 才能確認目前為 Write Protect。能力查詢 DW0=6 回答的是另一個問題。</span></p></aside>
</section>
<section class="lesson" id="module-nwp-commands"><h2 id="heading-nwp-commands"><span class="section-number">05</span> 保護後，哪些命令仍能做什麼</h2>
<figure><figcaption><strong>命令名稱只是起點，實際動作決定判斷</strong></figcaption><div class="table-wrap"><table><thead><tr><th scope="col">命令或情境</th><th scope="col">是否被寫入保護阻擋</th><th scope="col">原因</th></tr></thead><tbody><tr><td>Read／Compare／Verify</td><td>正常處理；仍可能有其他錯誤</td><td>保護不封鎖這些操作</td></tr><tr><td>Dataset Management修改受保護媒體</td><td>必須失敗</td><td>表內命令仍受註腳1約束</td></tr><tr><td>受保護NSID的Flush</td><td>成功且無作用</td><td>進入保護時已提交快取</td></tr><tr><td>Format指向8但也修改受保護的7</td><td>Namespace is Write Protected</td><td>實際影響包含受保護namespace</td></tr><tr><td>Sanitize會修改受保護namespace</td><td>Namespace is Write Protected</td><td>沒有指定NSID也須遵守保護</td></tr></tbody></table></div><figcaption>每列示範不同判斷，不構成執行順序。完整允許清單與三項註腳在圖表閱讀區逐組說明。來源：Base Figure737及其後條文。</figcaption></figure>

<!-- claim:NWP-COMMANDS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span><span class="paragraph-text">Figure 737 列出對受保護 NSID 正常處理的命令，但註腳仍限制會修改非揮發媒體的動作。Flush 成功且不產生作用；Directive Receive 若要求配置 Streams 資源則回 Namespace is Write Protected。未列出的命令只要符合本節列出的受保護目標或跨 namespace 修改條件，就會被拒絕。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.18.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.18.2, 文件頁 665-666, PDF 頁 691-692</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="05.02">05.02.</span><span class="paragraph-text">namespace 7 已受保護、8 未受保護。如果某次 Format NVM 雖指定 8，其格式化範圍卻包含 7，該命令仍須以 Namespace is Write Protected 中止。範圍只含 8 的另一個操作不能直接套用這個案例。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-nwp-observe"><h2 id="heading-nwp-observe"><span class="section-number">06</span> 用正確的狀態與錯誤解釋結果</h2>
<figure><figcaption><strong>先問正在觀察什麼，再選資料來源</strong></figcaption><div class="table-wrap"><table><thead><tr><th scope="col">想回答的問題</th><th scope="col">查看哪裡</th><th scope="col">代表性判讀</th></tr></thead><tbody><tr><td>namespace7目前是哪種保護？</td><td>Get FID84h、SEL0的WPS</td><td>1是一般Write Protect</td></tr><tr><td>裝置是否支援永久保護？</td><td>Identify的NWPC bit2</td><td>1是支援，不是已進入</td></tr><tr><td>為何要求改變狀態失敗？</td><td>完成狀態＋原狀態／控制條件</td><td>WPS2要求0：Feature Not Changeable</td></tr><tr><td>是否回報全體媒體唯讀警告？</td><td>SMART的AMRO</td><td>不能只因WPS變化而設1</td></tr></tbody></table></div><figcaption>這些資料可同時存在；它們分別描述設定、能力、一次命令的結果與健康狀況。來源：Base §8.1.18與Figures338／541／554／213。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>AMRO</dt><dd>All Media Read-Only，SMART健康資訊中表示全體媒體唯讀的警告位。</dd></div></dl>
<!-- claim:NWP-OBSERVE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.01">06.01.</span><span class="paragraph-text">主機應以 Get FID 84h 查 namespace 寫入保護狀態。控制器不得只因本狀態機造成的唯讀條件，就把 SMART Critical Warning 的 All Media Read-Only 設為 1；AMRO=0 也不能證明 namespace 沒有設保護。外部寫入保護系統與本機制組合的結果不在此規格定義內。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.18.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.18.1, 文件頁 665, PDF 頁 691</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="06.02">06.02.</span><span class="paragraph-text">WPS=1 且 AMRO=0 完全可能同時成立：namespace 受到設定保護，但不能因此回報全體媒體唯讀警告。Read 仍按自身條件處理，Write 則受保護限制。</span></p></aside>
</section>
<section id="spec-reading"><section id="spec-route"><h2>開著 Spec 的順向報告路徑</h2>
<p class="reader-paragraph"><span class="paragraph-number figure-paragraph-number" aria-label="R-1">R-1</span><span class="paragraph-text">先用本文的全貌與案例說明機制，再按下列 Base PDF 檢視器頁碼往後讀。共用頁從指定標題開始，在停止標題前結束；必要背景已在中文教學說明，不必為每個引用往返翻頁。</span></p>
<div class="table-wrap"><table><thead><tr><th scope="col">頁碼順序</th><th scope="col">章節起點</th><th scope="col">重點與停止位置</th></tr></thead><tbody><tr><td>R1 · Base PDF 538–539</td><td>§5.2.30.1.38</td><td>從 Namespace Write Protection Config 開始，用 Figure541 讀WPS編碼，再說不可保存、沒有default、拒絕轉換的條件，以及下一頁的快取提交。 在 §5.2.30.1.39 前停止。</td></tr><tr><td>R2 · Base PDF 690–692</td><td>§8.1.18</td><td>從 Namespace Write Protection 標題開始。Figure735比較四種狀態，Figure736沿箭頭解釋事件，Theory of Operation接能力與共享保護，Figure737連同下一頁三項註腳說明命令。 在 §8.1.19 前停止。</td></tr><tr><td>R3 · Base PDF 718</td><td>§8.1.24 · Figure756 byte2</td><td>最後只補看Device Configuration Block的WPC byte2，對照PWPC、WPUPCC與重設清零。不要從此展開其餘RPMB訊息表。 在 Figure757 前停止。</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>Device Configuration Block</dt><dd>RPMB target0的裝置設定資料結構，WPC位於其中byte2。</dd></div></dl>
</section></section>
<a class="reading-link" href="/DOCS/nvme-spec-report/base-namespace-write-protection/tutorial-zh-tw.html">開啟完整中文教學與逐圖解釋 →</a>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:nwp-reset -->
<details class="review-question" id="qa-nwp-reset"><summary>1. WPS=2，沒有斷電的控制器重設後，能用 Set WPS=0 解除嗎？</summary>
<div data-qa-answer="nwp-reset"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="08.01">08.01.</span><span class="paragraph-text">不能。這種重設維持狀態2，Set不能改變它；power cycle才沿著圖上的特殊箭頭回到0。WPUPCC清零只是關閉之後的進入許可，不是解除現有保護。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.18; 5.2.30.1.38, 文件頁 512-513,664-665, PDF 頁 538-539,690-691</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.24, 文件頁 691-692, PDF 頁 717-718</p>
</details></details>
<!-- qa:nwp-support -->
<details class="review-question" id="qa-nwp-support"><summary>2. NWPC=07h、PWPC=1，是否代表任何 namespace 現在都能進入永久保護？</summary>
<div data-qa-answer="nwp-support"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="08.02">08.02.</span><span class="paragraph-text">還要看目前狀態。0或1才有進入3的Set路徑；原本在2時，改成3仍會被拒絕。NWPC是支援，PWPC是許可，兩者都不取代狀態機。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.18; 5.2.30.1.38, 文件頁 512-513,664-665, PDF 頁 538-539,690-691</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.18; 5.2.30.1.38, 文件頁 512-513,664-665, PDF 頁 538-539,690-691</p>
</details></details>
<!-- qa:nwp-capability -->
<details class="review-question" id="qa-nwp-capability"><summary>3. 成功的能力查詢回 DW0=6，能否說目前 WPS=6，而且可解除永久保護？</summary>
<div data-qa-answer="nwp-capability"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="08.03">08.03.</span><span class="paragraph-text">兩個結論都不對。SEL3的6解成CHANG1、NSSPEC1、SVBL0；CHANG表示此Feature有可變更的值，不保證目前值可改。查WPS要另用SEL0。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12; 5.2.12.2; 5.2.30.1.38, 文件頁 209-212,512, PDF 頁 235-238,538</p>
</details></details>
<!-- qa:nwp-flush -->
<details class="review-question" id="qa-nwp-flush"><summary>4. 保護後 Flush 為什麼成功卻不寫回資料？</summary>
<div data-qa-answer="nwp-flush"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="08.04">08.04.</span><span class="paragraph-text">轉入保護時已要求提交該namespace全部揮發性寫入快取資料與metadata。因此這裡的成功不代表還有一次額外寫入，也不能反推其他未受保護namespace的Flush同樣無作用。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.38, 文件頁 512-513, PDF 頁 538-539</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.18.2, 文件頁 665-666, PDF 頁 691-692</p>
</details></details>
<!-- qa:nwp-scope -->
<details class="review-question" id="qa-nwp-scope"><summary>5. 7受保護、8未受保護，把 Format NVM 的 NSID 填8就一定能執行嗎？</summary>
<div data-qa-answer="nwp-scope"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="08.05">08.05.</span><span class="paragraph-text">不一定。還要判斷這次format真正涵蓋哪些namespace；若也會修改7，就必須因保護而拒絕。保護依實際影響判斷，不只看命令上的目標編號。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.18.2, 文件頁 665-666, PDF 頁 691-692</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
