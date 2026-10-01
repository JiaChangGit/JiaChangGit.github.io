---
layout: "post"
title: "NVMe 圖表判讀與情境練習 07 · 維護與管理操作"
date: "2026-09-29 09:00:00 +0800"
categories: ["nvme"]
tags: ["NVMe", "Reference"]
permalink: "/nvme/figure-reference/maintenance/zh-tw/"
nvme_quickref: true
last_modified_at: "2026-10-01"
lang: "zh-Hant-TW"
description: "NVMe 情境練習與圖表速查：查詢路徑、欄位推導、完整解答及 Spec 位置。"
---

<div class="nvme-quickref">
<nav class="qr-top" aria-label="版本與索引"><a href="#content">跳到內容</a><a href="/nvme/figure-reference/zh-tw/">總索引</a><a href="/nvme/figure-reference/maintenance/en/">English</a><a href="/DOCS/nvme-quick-reference/maintenance.html">繁中 HTML</a></nav>
<main id="content">
<header><p class="qr-eyebrow">反覆查詢 · 欄位判讀 · 原文定位</p><h1>NVMe 圖表判讀與情境練習 07 · 維護與管理操作</h1><p class="qr-intro">把要求的動作、命令完成與背景操作結果分開看。韌體提交、namespace 建立和 Sanitize 接受命令，各自都還有不同的後續狀態需要核對。</p></header>
<aside class="qr-note"><p>每張原圖都有用途、欄位和判讀例子。例子中的數值用於說明，不代表你的裝置設定；原文另有條件時，依該欄位與命令定義判斷。</p><p>用瀏覽器「在頁面中尋找」搜尋欄位、FID、LID、CNS 或 Figure。bit／byte 位置沿用原圖：bit 是位元，byte 是 8 bits，Dword 是 4 bytes；index 是第幾筆，offset 是相對起點的偏移，須看當處使用的單位。</p><p>FID（Feature Identifier）選擇功能；LID（Log Page Identifier）選擇紀錄頁；CNS（Controller or Namespace Structure）選擇 Identify 回傳的資料結構。</p></aside>
<nav class="qr-top" aria-label="本冊閱讀入口"><a href="#exercises">從情境練習開始</a><a href="#figure-index">直接查圖表</a></nav>
<section id="exercises"><h2>先做情境練習</h2>
<p>每題資料均為教學假設，不是實際裝置回傳。先寫下查詢介面、目標、欄位與可支持的結論，再展開解答。題目只做 Spec 推導，不會執行命令。</p>
<nav class="qr-toc" id="exercise-toc" aria-label="情境索引"><ol>
<li><a href="#exercise-maintenance-01">如何查詢單一 namespace 是否支援 Overwrite Sanitize？</a></li>
<li><a href="#exercise-maintenance-02">一個 namespace 已清除，是否整台都清除了？</a></li>
<li><a href="#exercise-maintenance-03">新韌體已在 slot 2，現在跑的就是它嗎？</a></li>
<li><a href="#exercise-maintenance-04">Format 指定 NSID，就只會影響那一個嗎？</a></li>
<li><a href="#exercise-maintenance-05">不可保存的保護狀態，reset 後就會解除嗎？</a></li>
<li><a href="#exercise-maintenance-06">Boot protection 的 0，和 namespace 的 0 一樣嗎？</a></li>
</ol></nav>
<article class="qr-card qr-case" id="exercise-maintenance-01" data-scenario="maintenance-01"><h3><span class="qr-number">練習 01</span>如何查詢單一 namespace 是否支援 Overwrite Sanitize？</h3>
<p class="qr-case-question">需求是「只清除 NSID=7，使用 Sanitize Namespace with Overwrite」。Identify 顯示 OWS=1，是否已足夠？</p><div class="qr-observations"><h4>模擬回傳與已知條件</h4><ul>
<li>Base Revision 2.4；SANICAP.OWS=1、CES=1；假設 Commands Supported and Effects 亦回報 Sanitize Namespace 受支援。</li>
<li>需求明確限制單一 namespace，不允許把清除範圍擴大成整個 NVM subsystem。</li>
</ul></div><details class="qr-answer"><summary>展開解答：查詢路徑與完整推導</summary>
<p class="qr-route"><strong>查詢次序：</strong>先查 Base §5.2.27 允許的操作 → Identify CNS=01h 的 SANICAP → Commands Supported and Effects 的命令支援 → 目標 namespace 狀態。</p>
<p data-reasoning="maintenance-01-1"><span class="qr-step">推導 1</span>這版規格的 Sanitize Namespace 只有 Crypto Erase 這一種開始清除的操作。Figure 454 的 SANACT=011b（Overwrite 在另一個命令使用的值）在此屬於 Reserved。因此原需求無法由此標準命令組合實現。</p>
<p data-reasoning="maintenance-01-2"><span class="qr-step">推導 2</span>SANICAP.OWS=1 表示支援 Overwrite sanitize，不會替 Sanitize Namespace 增加新的合法 action。Subsystem Sanitize 與 Sanitize Namespace 必須先分清命令與作用範圍，再解能力。</p>
<p data-reasoning="maintenance-01-3"><span class="qr-step">推導 3</span>應回報「單一 namespace 的 Overwrite Sanitize 不在此版標準命令定義內」，並請需求端決定是否接受單一 namespace Crypto Erase 等其他方式。不能偷偷改送 subsystem Overwrite，也不能用一般 Write 覆寫冒充 Sanitize 保證。</p>
<div class="qr-related">需要重看欄位時，接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify Controller：能力與限制的主要入口</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b454">Base 2.4 Figure 454 · Namespace Sanitize：PREQ 的 bit 位置不同</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b451">Base 2.4 Figure 451 · Subsystem Sanitize：動作與完成模式</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b217">Base 2.4 Figure 217 · Command Effects：支援與執行影響</a></div>
<h4>本題原文定位</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.27 · 文件頁 452–453 · PDF 478–479</li><li>Base 2.4 · §5.2.27 · Figure 454 · Sanitize Namespace – Command Dword 10 · 文件頁 453 · PDF 479</li><li>Base 2.4 · §5.2.14.2.1 · Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent · 文件頁 361–362 · PDF 387–388</li><li>Base 2.4 · §5.2.26 · Figure 451 · Sanitize – Command Dword 10 · 文件頁 450–451 · PDF 476–477</li><li>Base 2.4 · §5.2.13.1.6 · Figure 217 · Commands Supported and Effects Data Structure · 文件頁 228–229 · PDF 254–255</li></ul></details>
<a href="#exercise-toc">回情境索引</a></article>
<article class="qr-card qr-case" id="exercise-maintenance-02" data-scenario="maintenance-02"><h3><span class="qr-number">練習 02</span>一個 namespace 已清除，是否整台都清除了？</h3>
<p class="qr-case-question">驗證程式拿 NSID=7 的成功結果，宣稱整個 subsystem 已清除，而且還能再啟動 4 個並行操作。哪些推論越過了資料範圍？</p><div class="qr-observations"><h4>模擬回傳與已知條件</h4><ul>
<li>LID=81h、NSID=7：STNSID=7、SOS=1；MNSOIP=FFFFFFFFh。</li>
<li>另讀 subsystem target（NSID=0）的 log：MNSOIP=4；尚未盤點其他進行中的 namespace sanitize。</li>
</ul></div><details class="qr-answer"><summary>展開解答：查詢路徑與完整推導</summary>
<p class="qr-route"><strong>查詢次序：</strong>Get Log Page LID=81h，分清 NSID=0／FFFFFFFFh 的 subsystem target 與 allocated NSID 的 namespace target。</p>
<p data-reasoning="maintenance-02-1"><span class="qr-step">推導 1</span>STNSID=7 確認這份回覆是 namespace 7 的狀態；SOS=1 表示相應最近 sanitize 已成功且 state machine 回到 Idle。它沒有宣告其他 namespace 也完成相同操作。</p>
<p data-reasoning="maintenance-02-2"><span class="qr-step">推導 2</span>namespace target 的 MNSOIP 按規則為 FFFFFFFFh，不能解成可並行數十億次。並行上限需讀 subsystem target；其值 4 是最多同時進行 4 個，不是現在剩餘 4 個。</p>
<p data-reasoning="maintenance-02-3"><span class="qr-step">推導 3</span>要算目前餘額，還需完整且時間一致的進行中操作資訊，並考慮並行管理造成的變動。即使有名額，命令被接受也仍須另查目標 log 的最終結果。</p>
<div class="qr-related">需要重看欄位時，接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b312">Base 2.4 Figure 312 · Sanitize Status：進度、結果與目前狀態</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b454">Base 2.4 Figure 454 · Namespace Sanitize：PREQ 的 bit 位置不同</a></div>
<h4>本題原文定位</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.13.1.38 · Figure 312 · Sanitize Status Log Page · 文件頁 314–319 · PDF 340–345</li><li>Base 2.4 · §5.2.27 · 文件頁 452–453 · PDF 478–479</li></ul></details>
<a href="#exercise-toc">回情境索引</a></article>
<article class="qr-card qr-case" id="exercise-maintenance-03" data-scenario="maintenance-03"><h3><span class="qr-number">練習 03</span>新韌體已在 slot 2，現在跑的就是它嗎？</h3>
<p class="qr-case-question">更新工具看到 slot 2 的新版本字串，便把升級標示為已生效。請用目前與下一次啟用欄位重新判讀。</p><div class="qr-observations"><h4>模擬回傳與已知條件</h4><ul>
<li>Firmware Slot Information：CAFS=1、NAFS=2；FRS1=&quot;A100&quot;、FRS2=&quot;B200&quot;。</li>
<li>Identify Controller.FR=&quot;A100&quot;；FRMW.FAWR=0；沒有後續可啟用該版本的 reset 紀錄。</li>
</ul></div><details class="qr-answer"><summary>展開解答：查詢路徑與完整推導</summary>
<p class="qr-route"><strong>查詢次序：</strong>Identify CNS=01h 的 FR／FRMW → Get Log Page LID=03h 的 AFI 與 slot revisions → Firmware Commit 的 action／status 與 reset 紀錄。</p>
<p data-reasoning="maintenance-03-1"><span class="qr-step">推導 1</span>CAFS=1 與 FR=A100 支持目前仍執行 slot 1 的版本。FRS2=B200 證明 slot 2 有該 revision，不等於 controller 現在已執行它。</p>
<p data-reasoning="maintenance-03-2"><span class="qr-step">推導 2</span>NAFS=2 指向下一次能造成啟用的 Controller Level Reset 所要啟用的 slot。FAWR=0 表示不支援無 reset 啟用；不能把任何未分類的 reset 都當作已滿足啟用條件。</p>
<p data-reasoning="maintenance-03-3"><span class="qr-step">推導 3</span>完整驗證應在適用的啟用步驟之後重新讀 FR 與 CAFS，再與預期版本比對。本題只指出尚未生效的證據，不要求現在執行 reset 或下載韌體。</p>
<div class="qr-related">需要重看欄位時，接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b215">Base 2.4 Figure 215 · Firmware Slot Log：目前版本與待啟用 slot</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b187">Base 2.4 Figure 187 · Firmware Commit：放進 slot 與啟用的差別</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify Controller：能力與限制的主要入口</a></div>
<h4>本題原文定位</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.13.1.4 · Figure 215 · Firmware Slot Information Log Page · 文件頁 226 · PDF 252</li><li>Base 2.4 · §5.2.9 · Figure 187 · Firmware Commit – Command Dword 10 · 文件頁 203 · PDF 229</li><li>Base 2.4 · §5.2.14.2.1 · Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent · 文件頁 340–341, 354 · PDF 366–367, 380</li><li>Base 2.4 · §5.2.9 · 文件頁 202–205 · PDF 228–231</li></ul></details>
<a href="#exercise-toc">回情境索引</a></article>
<article class="qr-card qr-case" id="exercise-maintenance-04" data-scenario="maintenance-04"><h3><span class="qr-number">練習 04</span>Format 指定 NSID，就只會影響那一個嗎？</h3>
<p class="qr-case-question">要求是只對 NSID=7 做 secure erase；審查時看到命令 NSID=7 就放行。還少查哪一組 scope？</p><div class="qr-observations"><h4>模擬回傳與已知條件</h4><ul>
<li>OACS.FNVMS=1；FNA.FNS=0、SENS=1、FNVMBS=0。</li>
<li>擬定 Format NVM：NSID=7、SES=1；其他格式欄位均合法，本題不執行命令。</li>
</ul></div><details class="qr-answer"><summary>展開解答：查詢路徑與完整推導</summary>
<p class="qr-route"><strong>查詢次序：</strong>Identify CNS=01h 的 OACS／FNA → Format NVM 的 NSID、SES 與格式參數。</p>
<p data-reasoning="maintenance-04-1"><span class="qr-step">推導 1</span>FNS 與 SENS 回答不同問題：格式變更的範圍與 secure erase 的範圍。本例 FNS=0 不能抵消 SENS=1；所要求的 secure erase 會作用於 subsystem 所有 namespaces。</p>
<p data-reasoning="maintenance-04-2"><span class="qr-step">推導 2</span>因此這組參數不符合「只清除 namespace 7」的需求。NSID 看起來很精確，仍須與 controller attributes 合併判讀，不能只憑命令目標欄位推定所有副作用的範圍。</p>
<p data-reasoning="maintenance-04-3"><span class="qr-step">推導 3</span>FNVMBS 的位值方向也要照定義：1 表示不支援 FFFFFFFFh broadcast，不是支援。這題的重點是先做範圍判定，再決定是否有符合需求的操作方式。</p>
<div class="qr-related">需要重看欄位時，接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify Controller：能力與限制的主要入口</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b195">Base 2.4 Figure 195 · Format CDW10：格式編號與清除選項</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-n91">NVM Command Set 1.3 Figure 91 · NVM Format 補充：PI 類型與 metadata 放置</a></div>
<h4>本題原文定位</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.14.2.1 · Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent · 文件頁 353, 373 · PDF 379, 399</li><li>Base 2.4 · §5.2.11 · Figure 195 · Format NVM – Command Dword 10 · 文件頁 208–209 · PDF 234–235</li><li>NVM Command Set 1.3 · §4.1.1 · Figure 91 · Format NVM – Command Dword 10 – NVM Command Set Specific Fields · 文件頁 63 · PDF 63</li></ul></details>
<a href="#exercise-toc">回情境索引</a></article>
<article class="qr-card qr-case" id="exercise-maintenance-05" data-scenario="maintenance-05"><h3><span class="qr-number">練習 05</span>不可保存的保護狀態，reset 後就會解除嗎？</h3>
<p class="qr-case-question">工具看到 FID=84h 的 SVBL=0，就說 reset 會解除所有 namespace write protection。請比較兩個 namespace。</p><div class="qr-observations"><h4>模擬回傳與已知條件</h4><ul>
<li>Get Features FID=84h、SEL=0：NSID=2 的 WPS=2；NSID=9 的 WPS=3。</li>
<li>controller 支援這些狀態；計畫中的動作只是 Controller Level Reset，沒有斷電。</li>
</ul></div><details class="qr-answer"><summary>展開解答：查詢路徑與完整推導</summary>
<p class="qr-route"><strong>查詢次序：</strong>Identify CNS=01h 查 NWPC → Get Features FID=84h、SEL=0 查各 namespace 目前 WPS → 對照 §8.1.18 的狀態持續規則。</p>
<p data-reasoning="maintenance-05-1"><span class="qr-step">推導 1</span>WPS=2 是 Write Protect Until Power Cycle，會跨沒有斷電的 Controller Level Reset 持續。因此題目的 reset 不能使 NSID=2 回到未保護；真正 power cycle 才是該狀態定義的解除條件。</p>
<p data-reasoning="maintenance-05-2"><span class="qr-step">推導 2</span>WPS=3 是 Permanent Write Protect，不能把 power cycle 當解除方法。可支援某種保護、允許進入保護、目前處在什麼狀態，是三個不同問題。</p>
<p data-reasoning="maintenance-05-3"><span class="qr-step">推導 3</span>SVBL=0 描述 Feature 是否接受保存要求，不改寫狀態本身的持續規則。報告應保留 NWPC、必要的 WPC 許可與 WPS，不能由單一 saveable 位推論復原行為。</p>
<div class="qr-related">需要重看欄位時，接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b541">Base 2.4 Figure 541 · Namespace Write Protection：目前保護狀態</a><a href="/nvme/figure-reference/features/zh-tw/#figure-b201">Base 2.4 Figure 201 · Feature 能力：可改、可保存及 namespace 範圍</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify Controller：能力與限制的主要入口</a></div>
<h4>本題原文定位</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.30.1.38 · Figure 541 · Write Protection – Command Dword 11 · 文件頁 512 · PDF 538</li><li>Base 2.4 · §5.2.12 · Figure 201 · Completion Queue Entry Dword 0 when Select is set to 11b · 文件頁 212 · PDF 238</li><li>Base 2.4 · §5.2.14.2.1 · Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent · 文件頁 375 · PDF 401</li><li>Base 2.4 · §8.1.18 · 文件頁 664–666 · PDF 690–692</li></ul></details>
<a href="#exercise-toc">回情境索引</a></article>
<article class="qr-card qr-case" id="exercise-maintenance-06" data-scenario="maintenance-06"><h3><span class="qr-number">練習 06</span>Boot protection 的 0，和 namespace 的 0 一樣嗎？</h3>
<p class="qr-case-question">一個共用解碼器把所有 protection state=0 都顯示為未保護。用以下歷史命令與讀取結果，判斷會誤解哪裡。</p><div class="qr-observations"><h4>模擬回傳與已知條件</h4><ul>
<li>先前 Set Features FID=85h：BP0WPS=0、BP1WPS=0，成功。</li>
<li>現在 Get Features FID=85h、SEL=0：BP0WPS=2、BP1WPS=4。</li>
</ul></div><details class="qr-answer"><summary>展開解答：查詢路徑與完整推導</summary>
<p class="qr-route"><strong>查詢次序：</strong>按 FID 區分 Namespace Write Protection（84h）與 Boot Partition Write Protection（85h），再區分 Set 要求與 Get 回報。</p>
<p data-reasoning="maintenance-06-1"><span class="qr-step">推導 1</span>FID=85h 的 Set 值 0 是「不要求改變該 partition」，不是解鎖。兩個 0 的成功命令可能保持兩者原狀，不能拿它當作解除保護的證據。</p>
<p data-reasoning="maintenance-06-2"><span class="qr-step">推導 2</span>目前 BP0WPS=2 表示 partition 0 為 Write Locked；BP1WPS=4 表示 partition 1 的保護由 RPMB 控制。4 是可回報的狀態，不能原樣當一般 Set 的要求值。</p>
<p data-reasoning="maintenance-06-3"><span class="qr-step">推導 3</span>Get 不會以 0 表示這兩個 partition 的狀態，因此共用函式至少需要 FID 與方向。若還涉及 shared multi-domain partition，必須另查其特定限制，不能只套 namespace 的 WPS 表。</p>
<div class="qr-related">需要重看欄位時，接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b542">Base 2.4 Figure 542 · Boot Partition 保護：兩個 partition 的獨立欄位</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b541">Base 2.4 Figure 541 · Namespace Write Protection：目前保護狀態</a></div>
<h4>本題原文定位</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.30.1.39 · Figure 542 · Boot Partition Write Protection Config - Command Dword 11 · 文件頁 513–514 · PDF 539–540</li><li>Base 2.4 · §5.2.30.1.38 · Figure 541 · Write Protection – Command Dword 11 · 文件頁 512 · PDF 538</li></ul></details>
<a href="#exercise-toc">回情境索引</a></article>
</section>
<nav class="qr-toc" id="figure-index" aria-label="本冊圖表索引"><h2>本冊圖表</h2><ol>
<li><a href="#figure-b187">Base 2.4 Figure 187 · Firmware Commit：放進 slot 與啟用的差別</a></li>
<li><a href="#figure-b191">Base 2.4 Figure 191 · Firmware Download：每個 chunk 的大小</a></li>
<li><a href="#figure-b215">Base 2.4 Figure 215 · Firmware Slot Log：目前版本與待啟用 slot</a></li>
<li><a href="#figure-b177">Base 2.4 Figure 177 · Device Self-test：選哪種測試或中止</a></li>
<li><a href="#figure-b218">Base 2.4 Figure 218 · Self-test Log：目前進度與最近 20 筆結果</a></li>
<li><a href="#figure-b219">Base 2.4 Figure 219 · Self-test Result：先看有效位再讀失敗位置</a></li>
<li><a href="#figure-b443">Base 2.4 Figure 443 · Namespace Attachment：建立後還要附加到 controller</a></li>
<li><a href="#figure-b446">Base 2.4 Figure 446 · Namespace Management：Create、Delete 或 Restore</a></li>
<li><a href="#figure-n134">NVM Command Set 1.3 Figure 134 · Create Namespace buffer：哪些欄位由主機填</a></li>
<li><a href="#figure-b195">Base 2.4 Figure 195 · Format CDW10：格式編號與清除選項</a></li>
<li><a href="#figure-n91">NVM Command Set 1.3 Figure 91 · NVM Format 補充：PI 類型與 metadata 放置</a></li>
<li><a href="#figure-b451">Base 2.4 Figure 451 · Subsystem Sanitize：動作與完成模式</a></li>
<li><a href="#figure-b454">Base 2.4 Figure 454 · Namespace Sanitize：PREQ 的 bit 位置不同</a></li>
<li><a href="#figure-b312">Base 2.4 Figure 312 · Sanitize Status：進度、結果與目前狀態</a></li>
<li><a href="#figure-b541">Base 2.4 Figure 541 · Namespace Write Protection：目前保護狀態</a></li>
<li><a href="#figure-b542">Base 2.4 Figure 542 · Boot Partition 保護：兩個 partition 的獨立欄位</a></li>
</ol></nav>
<article class="qr-card" id="figure-b187" data-figure="B187">
<h2><span class="qr-number">01</span>Firmware Commit：放進 slot 與啟用的差別</h2>
<p class="qr-original">Base 2.4 · Figure 187 · Firmware Commit – Command Dword 10</p>
<p class="qr-location">§5.2.9 · 文件頁 203 · PDF 229</p>
<p class="qr-explanation" data-paragraph="B187-1"><span class="qr-step">01.1 · 用途</span>韌體已下載但版本未改變時，查 Commit Action，分辨本次是否只放入 slot、等待 reset 或立即啟用。下載與 commit 不是同一步。</p>
<p class="qr-explanation" data-paragraph="B187-2"><span class="qr-step">01.2 · 欄位與關係</span>FS bits2:0 指定 slot，0 讓 controller 選；CA bits5:3 的 0 為放入但不啟用、1 為放入後下次 Controller Level Reset 啟用、2 為既有 slot 下次 reset 啟用、3 為立即啟用。CA6／7 屬 Boot Partition，搭配 BPID bit31。</p>
<p class="qr-explanation" data-paragraph="B187-3"><span class="qr-step">01.3 · 判讀與例子</span>CA=1 命令成功後，當下 active firmware 仍可是舊版；用 Firmware Slot Information 比較目前與下次 active slot，再核對 completion 是否要求特定 reset。</p>
<p class="qr-tags">搜尋詞：Firmware Commit · CA · FS · BPID · activate</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b191">Base 2.4 Figure 191 · Firmware Download：每個 chunk 的大小</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b215">Base 2.4 Figure 215 · Firmware Slot Log：目前版本與待啟用 slot</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b104">Base 2.4 Figure 104 · Admin 命令專屬狀態</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b191" data-figure="B191">
<h2><span class="qr-number">02</span>Firmware Download：每個 chunk 的大小</h2>
<p class="qr-original">Base 2.4 · Figure 191 · Firmware Image Download – Command Dword 10</p>
<p class="qr-location">§5.2.10 · 文件頁 205 · PDF 231</p>
<p class="qr-explanation" data-paragraph="B191-1"><span class="qr-step">02.1 · 用途</span>重建韌體下載分段時，這張表解每一段長度。整份 image 的大小不能直接填到每個 chunk 命令。</p>
<p class="qr-explanation" data-paragraph="B191-2"><span class="qr-step">02.2 · 欄位與關係</span>CDW10 的 NUMD bits31:0 以 Dwords 數減 1 表示本段長度，bytes=4×(NUMD+1)。還需搭配 CDW11 的 Offset 與 Identify.FWUG 要求，確認分段位置、粒度與完整性。</p>
<p class="qr-explanation" data-paragraph="B191-3"><span class="qr-step">02.3 · 判讀與例子</span>4096-byte chunk 的 NUMD=1023，而不是 4096。讀 trace 時要分開記錄長度與目的 image offset；正確長度仍可能因 offset 或 FWUG 條件不符而失敗。</p>
<p class="qr-tags">搜尋詞：Firmware Image Download · NUMD · FWUG · chunk</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b187">Base 2.4 Figure 187 · Firmware Commit：放進 slot 與啟用的差別</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify Controller：能力與限制的主要入口</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b215" data-figure="B215">
<h2><span class="qr-number">03</span>Firmware Slot Log：目前版本與待啟用 slot</h2>
<p class="qr-original">Base 2.4 · Figure 215 · Firmware Slot Information Log Page</p>
<p class="qr-location">§5.2.13.1.4 · 文件頁 226 · PDF 252</p>
<p class="qr-explanation" data-paragraph="B215-1"><span class="qr-step">03.1 · 用途</span>更新後要確認「已存放」與「正在執行」是否相同，查這份 log。某 slot 有版本字串，不代表它就是 active slot。</p>
<p class="qr-explanation" data-paragraph="B215-2"><span class="qr-step">03.2 · 欄位與關係</span>AFI byte0 的 CAFS bits2:0 為目前 active slot，NAFS bits6:4 為下次可造成啟用的 reset 所要啟用 slot；NAFS=0 表示未指示。FRS1～7 每個 8bytes，保存各 slot 的 revision，從 byte8 開始。</p>
<p class="qr-explanation" data-paragraph="B215-3"><span class="qr-step">03.3 · 判讀與例子</span>CAFS=1、NAFS=2、slot2 有新版字串，表示目前仍從 slot1 載入，slot2 等待啟用。FRS 為 0 可能是該 slot 未支援或沒有有效版本，不能單靠 0 區分兩者。</p>
<p class="qr-tags">搜尋詞：LID 03h · AFI · CAFS · NAFS · FRS</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b187">Base 2.4 Figure 187 · Firmware Commit：放進 slot 與啟用的差別</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b177" data-figure="B177">
<h2><span class="qr-number">04</span>Device Self-test：選哪種測試或中止</h2>
<p class="qr-original">Base 2.4 · Figure 177 · Device Self-test – Command Dword 10</p>
<p class="qr-location">§5.2.6 · 文件頁 199 · PDF 225</p>
<p class="qr-explanation" data-paragraph="B177-1"><span class="qr-step">04.1 · 用途</span>測試啟動命令的動作由 STC 決定。命令完成與測試背景流程完成是兩回事，結果應接著看 Self-test log。</p>
<p class="qr-explanation" data-paragraph="B177-2"><span class="qr-step">04.2 · 欄位與關係</span>CDW10 bits3:0 的 STC=1 啟動 short、2 啟動 extended、3 啟動 Host-Initiated Refresh、Eh 為廠商專屬、Fh 中止。NSID 與支援能力另決定測試對象及動作是否適用。</p>
<p class="qr-explanation" data-paragraph="B177-3"><span class="qr-step">04.3 · 判讀與例子</span>STC=2 成功完成提交後，若 log 仍顯示 extended 進行中，並不矛盾。不能把 Admin CQE 成功當成整個測試已通過。</p>
<p class="qr-tags">搜尋詞：Device Self-test · STC · short · extended · Host-Initiated Refresh</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b218">Base 2.4 Figure 218 · Self-test Log：目前進度與最近 20 筆結果</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b219">Base 2.4 Figure 219 · Self-test Result：先看有效位再讀失敗位置</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b218" data-figure="B218">
<h2><span class="qr-number">05</span>Self-test Log：目前進度與最近 20 筆結果</h2>
<p class="qr-original">Base 2.4 · Figure 218 · Device Self-test Log Page</p>
<p class="qr-location">§5.2.13.1.7 · 文件頁 230 · PDF 256</p>
<p class="qr-explanation" data-paragraph="B218-1"><span class="qr-step">05.1 · 用途</span>這張表將目前正在執行的狀態與過去結果分開。查測試進度看前 2bytes；查成敗看後面的 result list。</p>
<p class="qr-explanation" data-paragraph="B218-2"><span class="qr-step">05.2 · 欄位與關係</span>CDSTO byte0 低 4bits 為目前 operation，CDSTC byte1 低 7bits 為完成百分比。DSTOS=0 時進度欄應忽略。從 byte4 開始保存 20 筆 28-byte 結果，第一筆是最新完成或中止的操作。</p>
<p class="qr-explanation" data-paragraph="B218-3"><span class="qr-step">05.3 · 判讀與例子</span>byte1 仍留 25 而 DSTOS 已為 0 時，不應報告「測試卡在 25%」。先讀最新結果，確認是完成、命令中止、reset 中止或其他原因。</p>
<p class="qr-tags">搜尋詞：LID 06h · CDSTO · CDSTC · DSTOS · RDS</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b219">Base 2.4 Figure 219 · Self-test Result：先看有效位再讀失敗位置</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b177">Base 2.4 Figure 177 · Device Self-test：選哪種測試或中止</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b219" data-figure="B219">
<h2><span class="qr-number">06</span>Self-test Result：先看有效位再讀失敗位置</h2>
<p class="qr-original">Base 2.4 · Figure 219 · Self-test Result Data Structure</p>
<p class="qr-location">§5.2.13.1.7 · 文件頁 231–232 · PDF 257–258</p>
<p class="qr-explanation" data-paragraph="B219-1"><span class="qr-step">06.1 · 用途</span>這張表用來判讀一筆 Self-test 結果，並區分「測試失敗」與「操作被中止」。後面的診斷欄位不是每筆都有意義。</p>
<p class="qr-explanation" data-paragraph="B219-2"><span class="qr-step">06.2 · 欄位與關係</span>DSTS byte0 高 4bits 是測試類型、低 4bits 是結果；SEGN byte1 僅特定結果有效。VDINFO byte2 分別標 NSID、FLBA、SCT、SC 是否有效；POH bytes11:4 記完成／中止時通電小時，NSID15:12 與 FLBA23:16 描述失敗對象。</p>
<p class="qr-explanation" data-paragraph="B219-3"><span class="qr-step">06.3 · 判讀與例子</span>VDINFO 的 FVLD=0 時，即使 FLBA bytes 全 0，也不能宣稱 LBA0 故障。DSTR=2 是 Controller Level Reset 中止，也不等於測出媒體損壞。</p>
<p class="qr-tags">搜尋詞：DSTS · DSTR · DSTC · VDINFO · FLBA · SEGN · POH</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b218">Base 2.4 Figure 218 · Self-test Log：目前進度與最近 20 筆結果</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b102">Base 2.4 Figure 102 · SCT：決定去哪張錯誤碼表</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b443" data-figure="B443">
<h2><span class="qr-number">07</span>Namespace Attachment：建立後還要附加到 controller</h2>
<p class="qr-original">Base 2.4 · Figure 443 · Namespace Attachment – Command Dword 10</p>
<p class="qr-location">§5.2.24 · 文件頁 445 · PDF 471</p>
<p class="qr-explanation" data-paragraph="B443-1"><span class="qr-step">07.1 · 用途</span>namespace 存在但某個 controller 看不到時，查 attachment 動作及 controller list。建立儲存物件與讓某 controller 存取，是不同操作。</p>
<p class="qr-explanation" data-paragraph="B443-2"><span class="qr-step">07.2 · 欄位與關係</span>CDW10.SEL bits3:0 的 0 表示 Attach、1 表示 Detach，其他值保留。實際 namespace 由 NSID 指定，目標 controllers 在資料 buffer 清單中。此表的 SEL 數值不能套到 Namespace Management。</p>
<p class="qr-explanation" data-paragraph="B443-3"><span class="qr-step">07.3 · 判讀與例子</span>Detach 不等於 Delete：它解除 controller 與 namespace 的關聯，不是直接刪除 namespace。若清單處理失敗，Error Information 可提供第一個失敗 entry 的 byte offset，不能假設後續 controllers 都已處理。</p>
<p class="qr-tags">搜尋詞：Namespace Attachment · SEL · Attach · Detach · Controller List</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b446">Base 2.4 Figure 446 · Namespace Management：Create、Delete 或 Restore</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b212">Base 2.4 Figure 212 · Error Information：把錯誤對回命令與欄位</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b446" data-figure="B446">
<h2><span class="qr-number">08</span>Namespace Management：Create、Delete 或 Restore</h2>
<p class="qr-original">Base 2.4 · Figure 446 · Namespace Management – Command Dword 10</p>
<p class="qr-location">§5.2.25 · 文件頁 446–447 · PDF 472–473</p>
<p class="qr-explanation" data-paragraph="B446-1"><span class="qr-step">08.1 · 用途</span>這張表用來辨認主機要求改變 namespace 配置的哪一種動作。單靠 opcode 無法區分 Create 與 Delete。</p>
<p class="qr-explanation" data-paragraph="B446-2"><span class="qr-step">08.2 · 欄位與關係</span>CDW10.SEL bits3:0 的 0／1／2 分別為 Create、Delete、Restore Default Namespace Configuration。其餘 bits 保留；資料 buffer 與 NSID 的用途依動作而變，Create 還需搭配 CSI 選格式。</p>
<p class="qr-explanation" data-paragraph="B446-3"><span class="qr-step">08.3 · 判讀與例子</span>Create 成功回傳的新 NSID，只證明 namespace 已建立，不保證已附加給目標 controller。Restore 是恢復預設 namespace 配置，不是任意備份 snapshot 的還原。</p>
<p class="qr-tags">搜尋詞：Namespace Management · SEL · Create · Delete · Restore</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-n134">NVM Command Set 1.3 Figure 134 · Create Namespace buffer：哪些欄位由主機填</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b443">Base 2.4 Figure 443 · Namespace Attachment：建立後還要附加到 controller</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n134" data-figure="N134">
<h2><span class="qr-number">09</span>Create Namespace buffer：哪些欄位由主機填</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 134 · Namespace Management – Host Specified Fields</p>
<p class="qr-location">§4.1.6 · 文件頁 112–113 · PDF 112–113</p>
<p class="qr-explanation" data-paragraph="N134-1"><span class="qr-step">09.1 · 用途</span>建立 NVM namespace 時，此表列出主機可以指定的 buffer 位置。它只沿用部分 Identify 欄位，不應把完整 Identify 回覆不加修改地當 Create 輸入。</p>
<p class="qr-explanation" data-paragraph="N134-2"><span class="qr-step">09.2 · 欄位與關係</span>NSZE 在 bytes7:0、NCAP15:8、FLBAS26、DPS29、NMIC30，後面有 ANAGRPID、NVMSETID、ENDGID。LBSTM 在 391:384，FDP 使用 NPHNDLS393:392 及從 512 開始的 Placement Handle list；保留區須按 Create 格式處理。</p>
<p class="qr-explanation" data-paragraph="N134-3"><span class="qr-step">09.3 · 判讀與例子</span>支援並啟用 FDP 時，placement handle 清單建立到 RUH 的對應；不支援或未啟用時不能依這些 bytes 宣稱配置有效。NSZE 與 NCAP 仍以所選格式的 blocks 為單位，不是 bytes。</p>
<p class="qr-tags">搜尋詞：NSZE · NCAP · FLBAS · DPS · NMIC · NPHNDLS · Placement Handle</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-n123">NVM Command Set 1.3 Figure 123 · NVM Namespace：容量、格式、原子性與建議粒度</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-n125">NVM Command Set 1.3 Figure 125 · LBAF：資料大小、metadata 大小與相對效能</a><a href="/nvme/figure-reference/features/zh-tw/#figure-b294">Base 2.4 Figure 294 · FDP Configuration：配置大小、資源數與 PID 切割</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b195" data-figure="B195">
<h2><span class="qr-number">10</span>Format CDW10：格式編號與清除選項</h2>
<p class="qr-original">Base 2.4 · Figure 195 · Format NVM – Command Dword 10</p>
<p class="qr-location">§5.2.11 · 文件頁 208–209 · PDF 234–235</p>
<p class="qr-explanation" data-paragraph="B195-1"><span class="qr-step">10.1 · 用途</span>Format 要求的是哪個資料格式、是否同時 secure erase，用此表解 CDW10。Base 先定共同外框，PI 和 metadata 語意要接 NVM 補充。</p>
<p class="qr-explanation" data-paragraph="B195-2"><span class="qr-step">10.2 · 欄位與關係</span>LBAFL bits3:0 與 LBAFU13:12 組成 format index；LBAFU 須符合 LBAFEE 條件。SES bits11:9 的 0／1／2 分別為不要求 secure erase、User Data Erase、Cryptographic Erase。PIL8、PI7:5 與 MSET4 依 command set 解讀。</p>
<p class="qr-explanation" data-paragraph="B195-3"><span class="qr-step">10.3 · 判讀與例子</span>format index 是清單索引，不是 bytes 或 LBA 大小。SES=1 後資料內容不保證為零；若驗證程式只接受全 0，會把允許的其他擦除後內容誤判成失敗。</p>
<p class="qr-tags">搜尋詞：Format NVM · LBAFL · LBAFU · SES · LBAFEE · PI · MSET</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-n91">NVM Command Set 1.3 Figure 91 · NVM Format 補充：PI 類型與 metadata 放置</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-n125">NVM Command Set 1.3 Figure 125 · LBAF：資料大小、metadata 大小與相對效能</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n91" data-figure="N91">
<h2><span class="qr-number">11</span>NVM Format 補充：PI 類型與 metadata 放置</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 91 · Format NVM – Command Dword 10 – NVM Command Set Specific Fields</p>
<p class="qr-location">§4.1.1 · 文件頁 63 · PDF 63</p>
<p class="qr-explanation" data-paragraph="N91-1"><span class="qr-step">11.1 · 用途</span>這張表補上 Base Format 表留給 NVM 的三個欄位。PI type 與 Guard 位寬不是同一組選擇，不能因 Type3 就當成 64-bit Guard。</p>
<p class="qr-explanation" data-paragraph="N91-2"><span class="qr-step">11.2 · 欄位與關係</span>MSET bit4 選 extended LBA 或 separate buffer；PI bits7:5 的 0 停用、1／2／3 啟用對應保護類型；PIL bit8 表示 PI 位置。NVM Command Set 1.0 及後續版本要求 PIL 清 0，PI 放 metadata 尾端。</p>
<p class="qr-explanation" data-paragraph="N91-3"><span class="qr-step">11.3 · 判讀與例子</span>選 MSET=1、PI=1 是 extended LBA 加 Type1 保護。實際 metadata 大小與 Guard 格式，仍要讀所選 LBAF／ELBAF，而不是從這兩個值推算。</p>
<p class="qr-tags">搜尋詞：Format NVM · PIL · PI · MSET · Type 1 · Type 2 · Type 3</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b195">Base 2.4 Figure 195 · Format CDW10：格式編號與清除選項</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-n125">NVM Command Set 1.3 Figure 125 · LBAF：資料大小、metadata 大小與相對效能</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-n128">NVM Command Set 1.3 Figure 128 · ELBAF：Guard 格式與 Storage Tag 位數</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b451" data-figure="B451">
<h2><span class="qr-number">12</span>Subsystem Sanitize：動作與完成模式</h2>
<p class="qr-original">Base 2.4 · Figure 451 · Sanitize – Command Dword 10</p>
<p class="qr-location">§5.2.26 · 文件頁 450–451 · PDF 476–477</p>
<p class="qr-explanation" data-paragraph="B451-1"><span class="qr-step">12.1 · 用途</span>查整個 NVM subsystem 的 Sanitize 要求時，這張表解動作、覆寫次數及後續狀態選項。命令接受與 sanitize 完成必須分開驗證。</p>
<p class="qr-explanation" data-paragraph="B451-2"><span class="qr-step">12.2 · 欄位與關係</span>SANACT bits2:0 選 1 退出 failure、2 Block Erase、3 Overwrite、4 Crypto Erase、5 退出 Media Verification；AUSE bit3 選完成模式。OWPASS7:4、OIPBP8 供 Overwrite 使用；NDAS9、EMVS10、PREQ11 另控制 deallocation、驗證與 purge 要求。</p>
<p class="qr-explanation" data-paragraph="B451-3"><span class="qr-step">12.3 · 判讀與例子</span>Overwrite 的 OWPASS=0 表示 16 次，不是 0 次。操作成功接受後應讀 LID81h 追蹤 SOS 等結果，不能把 Admin CQE success 或單一 SPROG 值當成已成功清除。</p>
<p class="qr-tags">搜尋詞：Sanitize · SANACT · AUSE · OWPASS · NDAS · EMVS · PREQ</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b312">Base 2.4 Figure 312 · Sanitize Status：進度、結果與目前狀態</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b454">Base 2.4 Figure 454 · Namespace Sanitize：PREQ 的 bit 位置不同</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b454" data-figure="B454">
<h2><span class="qr-number">13</span>Namespace Sanitize：PREQ 的 bit 位置不同</h2>
<p class="qr-original">Base 2.4 · Figure 454 · Sanitize Namespace – Command Dword 10</p>
<p class="qr-location">§5.2.27 · 文件頁 453 · PDF 479</p>
<p class="qr-explanation" data-paragraph="B454-1"><span class="qr-step">13.1 · 用途</span>針對單一 namespace 的 Sanitize 命令有自己的 CDW10 格式。它不能直接複製 subsystem Sanitize 的所有控制位。</p>
<p class="qr-explanation" data-paragraph="B454-2"><span class="qr-step">13.2 · 欄位與關係</span>SANACT bits2:0、AUSE bit3、PREQ bit4、EMVS bit10 有效；開始操作的動作是 Crypto Erase=4，Block Erase 與 Overwrite 編碼在此保留。bits9:5 與 31:11 保留。</p>
<p class="qr-explanation" data-paragraph="B454-3"><span class="qr-step">13.3 · 判讀與例子</span>例如 CDW10=0000041Ch 包含 SANACT4、AUSE1、PREQ1 及 EMVS1。若把 PREQ 放到 subsystem 用的 bit11，這裡寫到的是保留位，不是提出 purge 要求。</p>
<p class="qr-tags">搜尋詞：Sanitize Namespace · SANACT · PREQ bit4 · EMVS · NSID</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b451">Base 2.4 Figure 451 · Subsystem Sanitize：動作與完成模式</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b312">Base 2.4 Figure 312 · Sanitize Status：進度、結果與目前狀態</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b312" data-figure="B312">
<h2><span class="qr-number">14</span>Sanitize Status：進度、結果與目前狀態</h2>
<p class="qr-original">Base 2.4 · Figure 312 · Sanitize Status Log Page</p>
<p class="qr-location">§5.2.13.1.38 · 文件頁 314–319 · PDF 340–345</p>
<p class="qr-explanation" data-paragraph="B312-1"><span class="qr-step">14.1 · 用途</span>這張 log 同時回答背景操作進行到哪裡、最近結果與當前 sanitize state。查詢時先確認是 subsystem 還是 namespace 目標，再套欄位語意。</p>
<p class="qr-explanation" data-paragraph="B312-2"><span class="qr-step">14.2 · 欄位與關係</span>SPROG bytes1:0 為進度分數，status 內 SOS 區分從未操作、成功、進行中、失敗等。SCDW10 保存啟動參數；估計時間欄位有各自的 0／FFFFFFFFh 意義。SSI 補目前 state 及 failure state，另有清除狀態與 STNSID 等目標資訊。</p>
<p class="qr-explanation" data-paragraph="B312-3"><span class="qr-step">14.3 · 判讀與例子</span>SPROG=FFFFh 不能單獨當成功：SOS=3 仍代表失敗。解析 SCDW10 時，也要按目標選 Figure451 或 454，尤其 PREQ 的 bit 位置不同。</p>
<p class="qr-tags">搜尋詞：LID 81h · SPROG · SOS · SCDW10 · SSI · GDE · NDE · STNSID</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b451">Base 2.4 Figure 451 · Subsystem Sanitize：動作與完成模式</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b454">Base 2.4 Figure 454 · Namespace Sanitize：PREQ 的 bit 位置不同</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b234">Base 2.4 Figure 234 · Persistent Event：下一筆從哪裡開始</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b541" data-figure="B541">
<h2><span class="qr-number">15</span>Namespace Write Protection：目前保護狀態</h2>
<p class="qr-original">Base 2.4 · Figure 541 · Write Protection – Command Dword 11</p>
<p class="qr-location">§5.2.30.1.38 · 文件頁 512 · PDF 538</p>
<p class="qr-explanation" data-paragraph="B541-1"><span class="qr-step">15.1 · 用途</span>寫入命令被拒絕時，查此 namespace 目前 WPS，再分辨是否可解除、需 power cycle 或永久保護。這不是 Boot Partition 的保護編碼。</p>
<p class="qr-explanation" data-paragraph="B541-2"><span class="qr-step">15.2 · 欄位與關係</span>CDW11 bits2:0 為 WPS：0 未保護，1 一般保護，2 直到 power cycle，3 永久保護。支援能力與進入許可另查 NWPC 及 Write Protection Control；WPS 只描述要求或回報的狀態。</p>
<p class="qr-explanation" data-paragraph="B541-3"><span class="qr-step">15.3 · 判讀與例子</span>已進入 WPS=2 或 3 後，直接 Set Features 要求改回 0 會得到 Feature Not Changeable。不能因 SEL=3 回 CHANG=1，就判定當前永久狀態可以反轉。</p>
<p class="qr-tags">搜尋詞：FID 84h · WPS · Write Protect · Permanent Write Protect</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/features/zh-tw/#figure-b201">Base 2.4 Figure 201 · Feature 能力：可改、可保存及 namespace 範圍</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-b346">Base 2.4 Figure 346 · Namespace 共通狀態：可用、受保護與儲存歸屬</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b542">Base 2.4 Figure 542 · Boot Partition 保護：兩個 partition 的獨立欄位</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b542" data-figure="B542">
<h2><span class="qr-number">16</span>Boot Partition 保護：兩個 partition 的獨立欄位</h2>
<p class="qr-original">Base 2.4 · Figure 542 · Boot Partition Write Protection Config - Command Dword 11</p>
<p class="qr-location">§5.2.30.1.39 · 文件頁 513–514 · PDF 539–540</p>
<p class="qr-explanation" data-paragraph="B542-1"><span class="qr-step">16.1 · 用途</span>Boot Partition 更新被阻擋時，查兩個 partition 各自的保護狀態。此表的 0 不是「未保護」，與 namespace WPS 不同。</p>
<p class="qr-explanation" data-paragraph="B542-2"><span class="qr-step">16.2 · 欄位與關係</span>BP0WPS bits2:0、BP1WPS bits5:3：0 僅供 Set 使用、表示不要求改變；1 解鎖、2 鎖定、3 鎖至 power cycle。4 表示由 RPMB 控制，只能回報，不能作 Set 要求；預設兩者都是鎖定。</p>
<p class="qr-explanation" data-paragraph="B542-3"><span class="qr-step">16.3 · 判讀與例子</span>要只解鎖 partition0 並保留 partition1 原狀，兩欄分別為 1 與 0，CDW11=1。不能把兩欄都清 0 當作解鎖兩個 partition；若 NVM subsystem 的 CTRATT.MDS=1，且該 Boot Partition 由多個 controller 共享，將它設成 3（鎖至 power cycle）的要求會以 Feature Not Changeable 中止。</p>
<p class="qr-tags">搜尋詞：FID 85h · BP0WPS · BP1WPS · RPMB · Boot Partition</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b541">Base 2.4 Figure 541 · Namespace Write Protection：目前保護狀態</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b187">Base 2.4 Figure 187 · Firmware Commit：放進 slot 與啟用的差別</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<footer id="source-files"><h2>原始文件</h2><p>頁碼採本次提供的 ratified PDF；Base 的 PDF 頁＝文件頁＋26，另兩份相同。圖號與英文原名保留，可用 PDF 搜尋定位。公開網站不附原始 PDF。</p><ul class="qr-sources"><li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li></ul></footer>
</main></div>
