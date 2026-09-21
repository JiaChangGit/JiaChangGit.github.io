---
permalink: /nvme/read-recovery-level-zh-tw/
layout: post
read_time: true
show_date: true
title: "NVMe Read Recovery Level：讀取復原、作用範圍與設定"
date: 2026-09-21
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
[English]({% post_url 2026-09-21-nvme-read-recovery-level-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">讀取遇到難以復原的資料時，控制器應該再多試一些，還是少做一些復原、讓主機早點取得結果？Read Recovery Level 提供這項取捨。本文從等級與影響範圍開始，再把支援位元、設定命令、讀回格式和重設後的行為接起來，讓每個欄位都對應到一個具體問題。</span></p>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>先理解取捨</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">等級調整的是讀取錯誤復原的程度。比較最多、預設與最少復原，並分清策略、實際延遲與成功結果。</span></p></article>
<article><span class="axis-number">02</span><h3>找到共用設定的對象</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">先看是否有儲存集合，再找哪些 namespace 在同一集合內。這決定一次設定影響誰，以及哪些空間無法各自選不同等級。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>namespace</dt><dd>主機透過控制器存取的一份邏輯儲存空間。</dd></div></dl></article>
<article><span class="axis-number">03</span><h3>把能力、要求與結果接起來</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">先查哪些等級受支援，再指定目標與新值，最後以正確的查詢格式讀回。支援清單、目前值與保存能力分別回答不同問題。</span></p></article>
<article><span class="axis-number">04</span><h3>沿著時間追蹤設定</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="04-01">04-01</span><span class="paragraph-text">以設定成功區分先前與後續命令；再判斷重設覆蓋範圍、目前值與已保存值。這樣才能解釋何時用新值、何時可能回到另一個值。</span></p></article>
</div>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">讀者已學過 OS、Computer Organization，並了解 SSD 的基本概念。本文的 Set 7／9、namespace A／B／C 與位元數值均為說明性範例；使用前須以實際裝置回報的集合與能力為準。</span></p>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.03">00.03.</span><span class="paragraph-text">先用一個 Set 的設定情境串起觀念，再比較容易混淆的值與範圍；讀完應能解釋哪些空間共用設定，以及每次查詢究竟回答什麼。</span></p>
<div class="overview-connections"><h3>把主軸連起來</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.04">00.04.</span><span class="paragraph-text">可以用同一個問題貫穿全文：想讓 Set 7 內的讀取採用最少復原，需要查哪些能力、送出什麼參數，又要怎樣知道目前真的在用這個設定？先理解這條流程，再看每個欄位的位置。</span></p>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.05">00.05.</span><span class="paragraph-text">後半部會刻意比較相同數值在不同格式下的意思，以及相同設定在不同重設範圍下的結果。這些對比能避免只背等級名稱，卻把查詢或持續性判斷用錯。</span></p>
</div>
</section>
<section id="spec-route"><h2>開著 Spec 的順向報告路徑</h2>
<p class="reader-paragraph"><span class="paragraph-number figure-paragraph-number" aria-label="R-1">R-1</span><span class="paragraph-text">先用本文建立全貌，再開 Base PDF：499 → 715～716，只往後翻一次。以下採 PDF 檢視器頁碼；共用頁從指定標題開始，在下一節標題前停止。必要引用的欄位已在中文教學整理，不必為每一個引用反覆跳頁。</span></p>
<div class="table-wrap"><table><thead><tr><th scope="col">翻頁順序</th><th scope="col">主範圍</th><th scope="col">講解重點與停止位置</th></tr></thead><tbody><tr><td>R1 · Base PDF 499</td><td>§5.2.30.1.12</td><td>從 Read Recovery Level Config 標題起，先解釋 Set／subsystem 範圍，再用 Set 7、Level 15 連看 Figures 484／485，最後指出 Get 回覆位置與 SEL=3 例外。 在 §5.2.30.1.13 前停下。</td></tr><tr><td>R2 · Base PDF 715–716</td><td>§8.1.23</td><td>從 Read Recovery Level 標題起，把設定連回復原取捨、namespace 繼承與 LR 限制；Figure 755 收束方向、必備與選用等級。 在 §8.1.24 前停下。</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>SEL</dt><dd>Select；Get Features 要求回傳目前值、預設值、已保存值或能力的選擇欄位。</dd></div><div><dt>LR</dt><dd>Limited Retry；I/O 命令中與限制復原相關的控制資訊，和 RRL 的互動由實作決定。</dd></div></dl>
</section>
<section class="lesson" id="module-rrl-levels"><h2 id="heading-rrl-levels"><span class="section-number">01</span> 讀取遇到困難時，要花多少力氣復原？</h2>
<!-- claim:RRL-LEVELS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">Read Recovery Level（RRL）在讀取完成時間與錯誤復原投入之間提供取捨。支援此功能時，Level 4 是必備的預設等級，Level 15 是必備的 Fast Fail；Level 0 若有支援，提供最多復原。等級越高，復原量越少；與 I/O 命令 LR 的互動由實作決定。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Fast Fail</dt><dd>RRL Level 15 的正式名稱，表示最少復原量；沒有在此定義固定完成時間。</dd></div><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div><div><dt>RRL</dt><dd>Read Recovery Level；讀取錯誤復原等級，用來選擇讀取遇到困難時投入的復原程度。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.23</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.23, 文件頁 689-690, PDF 頁 715-716</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">說明性情境：資料有另一份可用副本的服務，可能希望裝置少做復原，早些交由上層決定下一步；願意等待這份媒體資料的工作，可能選較多復原的受支援等級。這是選擇策略的理由，不是特定等級的延遲或成功率保證。</span></p></aside>
</section>
<section class="lesson" id="module-rrl-scope"><h2 id="heading-rrl-scope"><span class="section-number">02</span> 一個設定，會影響哪些儲存空間？</h2>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 410" role="img"><title>同一 Set 內共用等級</title><desc>說明性範例：設定目標是 Set 7，A、B 一起使用 15；C 沿用 Set 9 的 4。若無 NVM Sets，則所有 namespace 共用 subsystem 的一份 RRL。來源：Base §8.1.23、§5.2.30.1.12、Figure 67。</desc><rect x="20" y="20" width="720" height="70" rx="6" class="v-object"/><text x="380.0" y="61.0" text-anchor="middle" font-size="17">NVM subsystem</text><path d="M190,90 L190,140" class="v-line"/><path d="M186,133 L190,140 L194,133" class="v-line"/><path d="M565,90 L565,140" class="v-line"/><path d="M561,133 L565,140 L569,133" class="v-line"/><rect x="20" y="140" width="345" height="95" rx="6" class="v-command"/><text x="192.5" y="181.0" text-anchor="middle" font-size="17">NVM Set 7</text><text x="192.5" y="206.0" text-anchor="middle" font-size="17">RRL: 4 → 15</text><rect x="395" y="140" width="345" height="95" rx="6" class="v-object"/><text x="567.5" y="181.0" text-anchor="middle" font-size="17">NVM Set 9</text><text x="567.5" y="206.0" text-anchor="middle" font-size="17">RRL: 4</text><path d="M190,235 L190,285" class="v-line"/><path d="M186,278 L190,285 L194,278" class="v-line"/><path d="M565,235 L565,285" class="v-line"/><path d="M561,278 L565,285 L569,278" class="v-line"/><rect x="20" y="285" width="345" height="100" rx="6" class="v-success"/><text x="192.5" y="328.5" text-anchor="middle" font-size="17">namespace A + B</text><text x="192.5" y="353.5" text-anchor="middle" font-size="17">RRL = 15</text><rect x="395" y="285" width="345" height="100" rx="6" class="v-object"/><text x="567.5" y="328.5" text-anchor="middle" font-size="17">namespace C</text><text x="567.5" y="353.5" text-anchor="middle" font-size="17">RRL = 4</text></svg></div><figcaption>說明性範例：設定目標是 Set 7，A、B 一起使用 15；C 沿用 Set 9 的 4。若無 NVM Sets，則所有 namespace 共用 subsystem 的一份 RRL。來源：Base §8.1.23、§5.2.30.1.12、Figure 67。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>NVM subsystem</dt><dd>NVMe 儲存子系統，可包含多個控制器及 namespace。</dd></div><div><dt>NVM Set</dt><dd>一組在邏輯上與其他集合分開的非揮發性儲存，可包含多個 namespace；本篇用它界定共用 RRL 的範圍。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl>
<!-- claim:RRL-SCOPE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">有 NVM Sets 時，FID 12h 以 NVM Set 為範圍，選中的集合共用一份 RRL。沒有 NVM Sets 時，範圍改為整個 NVM subsystem，所有 namespace 使用同一等級。改變 RRL 不會改變 namespace 中已有的資料。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>FID</dt><dd>Feature Identifier；指定要讀取或設定哪一項 Feature 的編號。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.12, 文件頁 473, PDF 頁 499</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">說明性範例：Set 7 內有 namespace A、B，Set 9 內有 C。把 Set 7 改成 15，A、B 共用這個新等級，C 仍使用 Set 9 的設定。不能把 A 改成 15、同時要求同一 Set 內的 B 保持 4。</span></p></aside>
</section>
<section class="lesson" id="module-rrl-discover"><h2 id="heading-rrl-discover"><span class="section-number">03</span> 讀懂支援位元，才知道哪些值能選</h2>
<figure><figcaption><strong>從支援清單走到一個設定值</strong></figcaption><div class="table-wrap"><table><thead><tr><th scope="col">想選的等級</th><th scope="col">檢查 RRLS=8011h 的哪個 bit</th><th scope="col">送進 RRL 的值</th></tr></thead><tbody><tr><td>0</td><td>bit 0 = 1，支援</td><td>0h</td></tr><tr><td>4</td><td>bit 4 = 1，支援</td><td>4h</td></tr><tr><td>8</td><td>bit 8 = 0，不支援</td><td>不選此值</td></tr><tr><td>15</td><td>bit 15 = 1，支援</td><td>Fh</td></tr></tbody></table></div><figcaption>RRLS 的 bit 位置選一個是／否答案；RRL 則直接保存等級代碼。兩者不能互換。來源：Base Figures 338、485。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>RRLS</dt><dd>Read Recovery Levels Supported；每個 bit 對應一個等級是否受支援。</dd></div></dl>
<!-- claim:RRL-DISCOVER -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">Identify Controller 的 CTRATT.RRLVLS 表示是否支援功能，RRLS 的 16 個 bits 分別表示各等級是否支援。CTRATT.NSETS 決定使用 Set 或 subsystem 範圍；ONCS.SSFS 則決定能否使用非零 SEL 與 SV。這些能力不能互相替代。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>CTRATT</dt><dd>Controller Attributes；Identify Controller 中的控制器屬性位元欄位。</dd></div><div><dt>RRLVLS</dt><dd>Read Recovery Levels；CTRATT 中表示是否支援 RRL 功能的 bit。</dd></div><div><dt>NSETS</dt><dd>NVM Sets；CTRATT 中的 NVM Set 支援 bit。</dd></div><div><dt>ONCS</dt><dd>Optional NVM Command Support；Identify Controller 中的能力欄位，本篇只使用其中 SSFS。</dd></div><div><dt>SSFS</dt><dd>Save and Select Feature Support；表示是否支援 Set 的非零 SV 與 Get 的非零 SEL。</dd></div><div><dt>SV</dt><dd>Save；Set Features 中提出保存設定要求的 bit。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.14.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 文件頁 344-347,371-372, PDF 頁 370-373,397-398</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span><span class="paragraph-text">說明性範例：RRLS=8011h，拆成 (1&lt;&lt;15) | (1&lt;&lt;4) | (1&lt;&lt;0)，表示只支援 0、4、15。byte 100、101 若是 11 80，依 little-endian 組合後才是 8011h；它不是目前等級，也不是「共有 8011h 個等級」。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>little-endian</dt><dd>低位 byte 先存；例如 11 80 組成 16-bit 值 8011h。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-rrl-set"><h2 id="heading-rrl-set"><span class="section-number">04</span> 把「哪個集合、哪個等級」組成設定命令</h2>
<!-- claim:RRL-SET -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">Set Features 用 FID 12h 選 Read Recovery Level Config，CDW11 的低 16 bits 放 NVMSETID，CDW12 的低 4 bits 放 RRL。這個 Feature 不使用資料 buffer；NVM Set 或 subsystem 範圍的 NSID 應為 0。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NVMSETID</dt><dd>NVM Set Identifier；16-bit 集合識別碼，與 namespace 的 NSID 分開。</dd></div><div><dt>buffer</dt><dd>資料緩衝區；本 Feature 的參數與回覆不需要額外的資料緩衝區。</dd></div><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.12, 文件頁 473, PDF 頁 499</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">說明性範例：已確認 Set 7 存在且支援 Level 15，以 SV=0 設定：NSID=0、CDW10=00000012h、CDW11=00000007h、CDW12=0000000Fh。三個數值依序回答「改哪項功能、改哪個 Set、改成哪個等級」。</span></p></aside>
</section>
<section class="lesson" id="module-rrl-get"><h2 id="heading-rrl-get"><span class="section-number">05</span> 讀回時先看 SEL，才知道 DW0 在回答什麼</h2>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 455" role="img"><title>同一個 DW0=4，先確認查詢問題</title><desc>假設 SSFS=1，兩次都成功。SEL=0 的回覆採 RRL 格式；SEL=3 的回覆採能力格式。能力查詢不會改變目前等級。來源：Base Figures 198、201、485。</desc><rect x="20" y="20" width="720" height="70" rx="6" class="v-object"/><text x="380.0" y="61.0" text-anchor="middle" font-size="17">Get Features · FID 12h · CQE DW0 = 00000004h</text><path d="M190,90 L190,160" class="v-line"/><path d="M186,153 L190,160 L194,153" class="v-line"/><path d="M565,90 L565,160" class="v-line"/><path d="M561,153 L565,160 L569,153" class="v-line"/><rect x="20" y="160" width="345" height="105" rx="6" class="v-command"/><text x="192.5" y="206.0" text-anchor="middle" font-size="17">SEL = 0</text><text x="192.5" y="231.0" text-anchor="middle" font-size="17">問目前值</text><rect x="395" y="160" width="345" height="105" rx="6" class="v-command"/><text x="567.5" y="206.0" text-anchor="middle" font-size="17">SEL = 3</text><text x="567.5" y="231.0" text-anchor="middle" font-size="17">問能力</text><path d="M190,265 L190,325" class="v-line"/><path d="M186,318 L190,325 L194,318" class="v-line"/><path d="M565,265 L565,325" class="v-line"/><path d="M561,318 L565,325 L569,318" class="v-line"/><rect x="20" y="325" width="345" height="105" rx="6" class="v-success"/><text x="192.5" y="371.0" text-anchor="middle" font-size="17">DW0[3:0] = 4</text><text x="192.5" y="396.0" text-anchor="middle" font-size="17">RRL = 4</text><rect x="395" y="325" width="345" height="105" rx="6" class="v-success"/><text x="567.5" y="371.0" text-anchor="middle" font-size="17">CHANG = 1</text><text x="567.5" y="396.0" text-anchor="middle" font-size="17">NSSPEC = 0 · SVBL = 0</text></svg></div><figcaption>假設 SSFS=1，兩次都成功。SEL=0 的回覆採 RRL 格式；SEL=3 的回覆採能力格式。能力查詢不會改變目前等級。來源：Base Figures 198、201、485。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>NSSPEC</dt><dd>NS Specific；1 表示 namespace scope，0 本身不指定其他範圍。</dd></div><div><dt>CHANG</dt><dd>Changeable；回報該 Feature 是否有可變更的設定值。</dd></div><div><dt>SVBL</dt><dd>Saveable；回報該 Feature 的值是否可保存。</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry；完成佇列中回報命令執行結果的項目。</dd></div></dl>
<!-- claim:RRL-GET -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span><span class="paragraph-text">成功的 Get Features 在 SEL≠3 時，以 CQE DW0 回傳 Figure 485 格式的 RRL。SEL=3 則改回 Supported Capabilities：CHANG、NSSPEC、SVBL。相同 DW0 數值可能有完全不同的意思；RRLS 等級清單仍應從 Identify Controller 取得。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.12, 文件頁 473, PDF 頁 499</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="05.02">05.02.</span><span class="paragraph-text">同樣收到 DW0=00000004h：SEL=0 時表示目前 Level 4；SEL=3 時表示 CHANG=1、NSSPEC=0、SVBL=0，也就是可變更、非 指定的 namespace 範圍、不可保存。後者不能讀成「目前 Level 4」。</span></p></aside>
</section>
<section class="lesson" id="module-rrl-activation"><h2 id="heading-rrl-activation"><span class="section-number">06</span> 以成功完成為界，區分舊命令與新命令</h2>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 480" role="img"><title>設定成功是後續提交的保證界線</title><desc>時間由上往下。A 在界線前提交，不能保證採用新設定；B 在成功後才提交，必須採用新設定。這張圖沒有替 RRL 指定固定完成時間。來源：Base §5.2.30.1。</desc><rect x="20" y="20" width="720" height="80" rx="6" class="v-object"/><text x="380.0" y="53.5" text-anchor="middle" font-size="17">提交 Read A；A 仍可能在執行</text><text x="380.0" y="78.5" text-anchor="middle" font-size="17">新設定是否套用到 A：不保證</text><path d="M380,100 L380,145" class="v-line"/><path d="M376,138 L380,145 L384,138" class="v-line"/><rect x="20" y="145" width="720" height="70" rx="6" class="v-command"/><text x="380.0" y="186.0" text-anchor="middle" font-size="17">提交 Set Features：RRL = 15</text><path d="M380,215 L380,260" class="v-line"/><path d="M376,253 L380,260 L384,253" class="v-line"/><rect x="20" y="260" width="720" height="70" rx="6" class="v-decision"/><text x="380.0" y="301.0" text-anchor="middle" font-size="17">Set 成功完成</text><path d="M380,330 L380,375" class="v-line"/><path d="M376,368 L380,375 L384,368" class="v-line"/><rect x="20" y="375" width="720" height="80" rx="6" class="v-success"/><text x="380.0" y="408.5" text-anchor="middle" font-size="17">此後才提交 Read B</text><text x="380.0" y="433.5" text-anchor="middle" font-size="17">B 必須使用新設定</text></svg></div><figcaption>時間由上往下。A 在界線前提交，不能保證採用新設定；B 在成功後才提交，必須採用新設定。這張圖沒有替 RRL 指定固定完成時間。來源：Base §5.2.30.1。</figcaption></figure>

<!-- claim:RRL-ACTIVATION -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.01">06.01.</span><span class="paragraph-text">已提交而尚在執行的命令，可能套用或不套用剛改好的 Feature。Set Features 成功完成後才提交的命令，必須使用新設定。若希望明確區隔兩批讀取，主機宜先讓原有命令完成，再改設定。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1, 文件頁 459, PDF 頁 485</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="06.02">06.02.</span><span class="paragraph-text">說明性時間順序：Read A 先提交，接著 Set RRL=15；Set 成功後才提交 Read B。B 必須使用新設定，但不能對仍未完成的 A 作相同保證。若先等 A 完成再送 Set，就能明確分成兩批。</span></p></aside>
</section>
<section class="lesson" id="module-rrl-lifetime"><h2 id="heading-rrl-lifetime"><span class="section-number">07</span> 重設後保留什麼，要分可保存性與重設範圍</h2>
<figure><figcaption><strong>相同 current=15，重設後為何不同？</strong></figcaption><div class="table-wrap"><table><thead><tr><th scope="col">Feature 能力與原值</th><th scope="col">這次事件的判斷條件</th><th scope="col">之後的 current</th></tr></thead><tbody><tr><td>不可保存；current=15</td><td>Power cycle 或 reset：FID12h 具持續性</td><td>15</td></tr><tr><td>可保存；current=15、saved=4</td><td>Figure126 的全體範圍重設</td><td>4：取 saved</td></tr><tr><td>可保存；current=15、沒有 saved</td><td>Figure126 的全體範圍重設</td><td>4：取 default</td></tr><tr><td>可保存；current=15、saved=4</td><td>Figure127 的局部範圍重設；Set／subsystem scope</td><td>15：維持目前值</td></tr></tbody></table></div><figcaption>先查可保存性，再確認配置與重設範圍。表內都是說明性原值；兩種重設表的完整適用條件在相鄰段落說明。來源：Base §4.4、Figures 126／127／466。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>current</dt><dd>目前值；控制器現在使用的 Feature 設定。</dd></div><div><dt>default</dt><dd>預設值；本篇 RRL 預設為 Level 4，與目前值分開。</dd></div><div><dt>saved</dt><dd>已保存值；成功要求保存的 Feature 設定，用於適用的恢復情境。</dd></div><div><dt>scope</dt><dd>作用範圍；一份設定由哪些物件共用，例如同一 NVM Set 或整個 subsystem。</dd></div></dl>
<!-- claim:RRL-LIFETIME -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.01">07.01.</span><span class="paragraph-text">Figure 466 把 FID 12h 的持續性列為 Yes，但該欄只適用於不可保存的 Feature。若本 Feature 可保存，應依 current／saved 與重設範圍判斷：整個 subsystem 範圍的重設按 Figure 126，局部範圍按 Figure 127。例如多控制器的 subsystem 只重設一個控制器，Set／subsystem 的共用目前值維持不變；符合全體條件的重設則回到 saved，沒有 saved 才回 default。</span></p><details class="source-note"><summary>來源：Base 2.4 §4.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.4, 文件頁 167-169, PDF 頁 193-195</p></details>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="07.02">07.02.</span><span class="paragraph-text">說明性範例：可保存的 FID 12h 目前是 15、saved 是 4。遇到 Figure 126 適用的全體重設後，current 回到 saved=4；若是 Figure 127 適用的局部重設，NVM Set／subsystem 範圍的 current 維持 15。</span></p></aside>
</section>
<section id="spec-reading"><h2>接著打開 Spec 看什麼</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.01">08.01.</span><span class="paragraph-text">以下按概念列出閱讀位置。報告時先用上面的流程說明問題，再打開對應章節看欄位與完整條件。中文教學 HTML 另有本篇全部圖表的逐圖重點、案例與細節。</span></p>
<div class="table-wrap"><table><thead><tr><th scope="col">要說明的觀念</th><th scope="col">Spec 閱讀位置</th></tr></thead><tbody><tr><td>讀取遇到困難時，要花多少力氣復原？</td><td>Base 2.4 §8.1.23</td></tr><tr><td>一個設定，會影響哪些儲存空間？</td><td>Base 2.4 §5.2.30.1.12 · Base 2.4 §8.1.23 · Base 2.4 §3.2.2</td></tr><tr><td>讀懂支援位元，才知道哪些值能選</td><td>Base 2.4 §5.2.14.2.1</td></tr><tr><td>把「哪個集合、哪個等級」組成設定命令</td><td>Base 2.4 §5.2.30.1.12 · Base 2.4 §4.4 · Base 2.4 §5.2.30</td></tr><tr><td>讀回時先看 SEL，才知道 DW0 在回答什麼</td><td>Base 2.4 §5.2.30.1.12 · Base 2.4 §5.2.12</td></tr><tr><td>以成功完成為界，區分舊命令與新命令</td><td>Base 2.4 §5.2.30.1 · Base 2.4 §4.4</td></tr><tr><td>重設後保留什麼，要分可保存性與重設範圍</td><td>Base 2.4 §4.4 · Base 2.4 §5.2.30</td></tr></tbody></table></div>
<a class="reading-link" href="/DOCS/nvme-spec-report/base-read-recovery-level/tutorial-zh-tw.html">開啟完整中文教學與逐圖解釋 →</a></section>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:rrl-bitmap -->
<details class="review-question" id="qa-rrl-bitmap"><summary>1. RRLS=8011h，能選 Level 8 嗎？Level 15 應填 8000h 嗎？</summary>
<div data-qa-answer="rrl-bitmap"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="09.01">09.01.</span><span class="paragraph-text">不能選 8，因為 bit 8 是 0。要選 15，先用 RRLS bit 15 確認支援，再在 4-bit RRL 欄填 Fh；8000h 是支援位元的遮罩，不是等級代碼。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, 文件頁 344-347,371-372, PDF 頁 370-373,397-398</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.12, 文件頁 473, PDF 頁 499</p>
</details></details>
<!-- qa:rrl-scope -->
<details class="review-question" id="qa-rrl-scope"><summary>2. A、B 在同一 Set，能靠填 A 的 NSID 只讓 A 用 Level 15 嗎？</summary>
<div data-qa-answer="rrl-scope"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="09.02">09.02.</span><span class="paragraph-text">不能。RRL 依 Set 共用，命令的 NVMSETID 選該集合；這種 scope 的 NSID 應為 0，非零不會縮小作用範圍，而會使命令被中止。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.12, 文件頁 473, PDF 頁 499</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §4.4, 文件頁 169, PDF 頁 195</p>
</details></details>
<!-- qa:rrl-result -->
<details class="review-question" id="qa-rrl-result"><summary>3. 成功 Get 的 DW0=4，為什麼還不能立即說目前是 Level 4？</summary>
<div data-qa-answer="rrl-result"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="09.03">09.03.</span><span class="paragraph-text">還要看 SEL。SEL=0 才回 current；SEL=3 的 4 是 CHANG=1、NSSPEC=0、SVBL=0 的能力組合。若 SEL=1，4 說的是預設值。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.12, 文件頁 473, PDF 頁 499</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.12, 文件頁 209-212, PDF 頁 235-238</p>
</details></details>
<!-- qa:rrl-timing -->
<details class="review-question" id="qa-rrl-timing"><summary>4. Set Level 15 成功後，仍在途的 Read A 與之後才提交的 Read B 都保證用 15 嗎？</summary>
<div data-qa-answer="rrl-timing"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="09.04">09.04.</span><span class="paragraph-text">B 必須使用新設定；A 已先提交，可能套用或不套用新值。Level 15 本身也沒有固定毫秒上限。需要清楚區分兩批時，宜先完成 A，再修改設定。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1, 文件頁 459, PDF 頁 485</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.23, 文件頁 689-690, PDF 頁 715-716</p>
</details></details>
<!-- qa:rrl-reset -->
<details class="review-question" id="qa-rrl-reset"><summary>5. SV=0 成功設成 15，是否一重設就回到 4？</summary>
<div data-qa-answer="rrl-reset"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="09.05">09.05.</span><span class="paragraph-text">不一定。不可保存的 FID 12h 本身具持續性；可保存者還要看重設範圍。Figure 126 的全體情況回 saved 或 default，Figure 127 的局部情況對 Set／subsystem scope 維持 current。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §4.4, 文件頁 167-169, PDF 頁 193-195</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30, 文件頁 458-459, PDF 頁 484-485</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
