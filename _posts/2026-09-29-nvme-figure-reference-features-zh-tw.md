---
layout: "post"
title: "NVMe 圖表速查 05 · Features、電源、效能與資源"
date: "2026-09-29 09:00:00 +0800"
categories: ["nvme"]
tags: ["NVMe", "Reference"]
permalink: "/nvme/figure-reference/features/zh-tw/"
nvme_quickref: true
lang: "zh-Hant-TW"
description: "NVMe 原圖用途、欄位與判讀速查，附完整 Spec 位置。"
---

<div class="nvme-quickref">
<nav class="qr-top" aria-label="版本與索引"><a href="#content">跳到內容</a><a href="/nvme/figure-reference/zh-tw/">總索引</a><a href="/nvme/figure-reference/features/en/">English</a><a href="/DOCS/nvme-quick-reference/features.html">繁中 HTML</a></nav>
<main id="content">
<header><p class="qr-eyebrow">反覆查詢 · 欄位判讀 · 原文定位</p><h1>NVMe 圖表速查 05 · Features、電源、效能與資源</h1><p class="qr-intro">先分辨支援能力、目前值、預設值與保存值，再查各 Feature。電源延遲、排程權重、佇列數與回收資源各有單位，不能互相替代。</p></header>
<aside class="qr-note"><p>每張原圖都有用途、欄位和判讀例子。例子中的數值用於說明，不代表你的裝置設定；原文另有條件時，依該欄位與命令定義判斷。</p><p>用瀏覽器「在頁面中尋找」搜尋欄位、FID、LID、CNS 或 Figure。bit／byte 位置沿用原圖：bit 是位元，byte 是 8 bits，Dword 是 4 bytes；index 是第幾筆，offset 是相對起點的偏移，須看當處使用的單位。</p><p>FID（Feature Identifier）選擇功能；LID（Log Page Identifier）選擇紀錄頁；CNS（Controller or Namespace Structure）選擇 Identify 回傳的資料結構。</p></aside>
<nav class="qr-toc" id="figure-index" aria-label="本冊圖表索引"><h2>本冊圖表</h2><ol>
<li><a href="#figure-b198">Base 2.4 Figure 198 · Get Features：現在值、預設值、保存值或能力</a></li>
<li><a href="#figure-b201">Base 2.4 Figure 201 · Feature 能力：可改、可保存及 namespace 範圍</a></li>
<li><a href="#figure-b464">Base 2.4 Figure 464 · Set Features：要求生效與要求保存分開</a></li>
<li><a href="#figure-b466">Base 2.4 Figure 466 · FID 總表：功能名稱、資料 buffer 與作用範圍</a></li>
<li><a href="#figure-b340">Base 2.4 Figure 340 · Power State Descriptor：功耗、延遲與可執行 I/O</a></li>
<li><a href="#figure-b467">Base 2.4 Figure 467 · Arbitration：權重不是效能保證</a></li>
<li><a href="#figure-b468">Base 2.4 Figure 468 · Power Management：指定 state 與 idle 回應限制</a></li>
<li><a href="#figure-b471">Base 2.4 Figure 471 · Volatile Write Cache：目前 enable 位</a></li>
<li><a href="#figure-b472">Base 2.4 Figure 472 · Number of Queues：主機要求的數量</a></li>
<li><a href="#figure-b473">Base 2.4 Figure 473 · Number of Queues：實際分配的數量</a></li>
<li><a href="#figure-b475">Base 2.4 Figure 475 · APST：是否允許自動切換</a></li>
<li><a href="#figure-b477">Base 2.4 Figure 477 · APST Entry：從哪個 state、等多久、到哪裡</a></li>
<li><a href="#figure-b482">Base 2.4 Figure 482 · HCTM：兩個熱管理門檻</a></li>
<li><a href="#figure-b543">Base 2.4 Figure 543 · Interrupt Coalescing：延後中斷的時間與數量</a></li>
<li><a href="#figure-b545">Base 2.4 Figure 545 · HMB：啟用、新配置或返還原記憶體</a></li>
<li><a href="#figure-b294">Base 2.4 Figure 294 · FDP Configuration：配置大小、資源數與 PID 切割</a></li>
<li><a href="#figure-n21">NVM Command Set 1.3 Figure 21 · RUH Status：目前剩餘可寫量</a></li>
</ol></nav>
<article class="qr-card" id="figure-b198" data-figure="B198">
<h2><span class="qr-number">01</span>Get Features：現在值、預設值、保存值或能力</h2>
<p class="qr-original">Base 2.4 · Figure 198 · Get Features – Command Dword 10</p>
<p class="qr-location">§5.2.12 · 文件頁 209–210 · PDF 235–236</p>
<p class="qr-explanation" data-paragraph="B198-1"><span class="qr-step">01.1 · 用途</span>讀到的 Feature 值與剛設定的值不同，先查 SEL 選了哪種回覆。Get Features 不一定是在讀目前設定。</p>
<p class="qr-explanation" data-paragraph="B198-2"><span class="qr-step">01.2 · 欄位與關係</span>FID bits7:0 選功能，SEL bits10:8 的 0／1／2／3 分別為 Current、Default、Saved、Supported Capabilities。SEL=2 但不支援保存或沒有保存值時，依規格按 Default 處理。</p>
<p class="qr-explanation" data-paragraph="B198-3"><span class="qr-step">01.3 · 判讀與例子</span>同一 FID 用 SEL=3 回 DW0=4，不代表功能目前設為 4；它是能力 bitmap，應依 Figure201 解讀。比較設定前後，要記錄 SEL 與 Feature 作用對象。</p>
<p class="qr-tags">搜尋詞：Get Features · FID · SEL · current · default · saved</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/features/zh-tw/#figure-b201">Base 2.4 Figure 201 · Feature 能力：可改、可保存及 namespace 範圍</a><a href="/nvme/figure-reference/features/zh-tw/#figure-b464">Base 2.4 Figure 464 · Set Features：要求生效與要求保存分開</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b201" data-figure="B201">
<h2><span class="qr-number">02</span>Feature 能力：可改、可保存及 namespace 範圍</h2>
<p class="qr-original">Base 2.4 · Figure 201 · Completion Queue Entry Dword 0 when Select is set to 11b</p>
<p class="qr-location">§5.2.12 · 文件頁 212 · PDF 238</p>
<p class="qr-explanation" data-paragraph="B201-1"><span class="qr-step">02.1 · 用途</span>這張表只用於 Get Features 的 SEL=3 回覆。它回答該 Feature 有哪些操作能力，不能直接套到 SEL=0 取得的目前值。</p>
<p class="qr-explanation" data-paragraph="B201-2"><span class="qr-step">02.2 · 欄位與關係</span>DW0 bit2 是 CHANG、bit1 是 NSSPEC、bit0 是 SVBL。NSSPEC=0 不直接表示 controller scope，還要依 Feature 定義及 effects log。CHANG=1 也只表示有可更改屬性，不保證每個已進入的狀態都可解除。</p>
<p class="qr-explanation" data-paragraph="B201-3"><span class="qr-step">02.3 · 判讀與例子</span>DW0=6 表示可改、namespace-specific、不可保存。若該功能已進入永久寫入保護，CHANG 仍不能被解成「一定能改回未保護」。</p>
<p class="qr-tags">搜尋詞：SEL 3 · CHANG · NSSPEC · SVBL</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/features/zh-tw/#figure-b198">Base 2.4 Figure 198 · Get Features：現在值、預設值、保存值或能力</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b541">Base 2.4 Figure 541 · Namespace Write Protection：目前保護狀態</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b464" data-figure="B464">
<h2><span class="qr-number">03</span>Set Features：要求生效與要求保存分開</h2>
<p class="qr-original">Base 2.4 · Figure 464 · Set Features – Command Dword 10</p>
<p class="qr-location">§5.2.30 · 文件頁 457 · PDF 483</p>
<p class="qr-explanation" data-paragraph="B464-1"><span class="qr-step">03.1 · 用途</span>設定當下生效、重設後卻不同時，用這張表確認是否提出保存要求，再查該 Feature 本身的持續性規則。</p>
<p class="qr-explanation" data-paragraph="B464-2"><span class="qr-step">03.2 · 欄位與關係</span>FID 在 bits7:0，SV 在 bit31；其餘 bits30:8 保留。SV=1 要求保存屬性以跨所有 power states 與 reset 持續；若該 FID 不可保存，命令會以 Feature Identifier Not Saveable 中止。</p>
<p class="qr-explanation" data-paragraph="B464-3"><span class="qr-step">03.3 · 判讀與例子</span>不能把 SV=0 直接翻成「下次 reset 一定清除」。部分功能本來就定義某些狀態持續，是否可保存與目前狀態是否持續是兩個判斷。</p>
<p class="qr-tags">搜尋詞：Set Features · SV · FID · Feature Identifier Not Saveable</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/features/zh-tw/#figure-b201">Base 2.4 Figure 201 · Feature 能力：可改、可保存及 namespace 範圍</a><a href="/nvme/figure-reference/features/zh-tw/#figure-b466">Base 2.4 Figure 466 · FID 總表：功能名稱、資料 buffer 與作用範圍</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b466" data-figure="B466">
<h2><span class="qr-number">04</span>FID 總表：功能名稱、資料 buffer 與作用範圍</h2>
<p class="qr-original">Base 2.4 · Figure 466 · Set Features – Feature Identifiers</p>
<p class="qr-location">§5.2.30 · 文件頁 457–459 · PDF 483–485</p>
<p class="qr-explanation" data-paragraph="B466-1"><span class="qr-step">04.1 · 用途</span>只有 FID 數字或不知道 Feature 影響哪個對象時，從此表找名稱、範圍及是否使用資料 buffer。指向 NVM 規格的列，表示定義分工，不是該 FID 沒有作用。</p>
<p class="qr-explanation" data-paragraph="B466-2"><span class="qr-step">04.2 · 欄位與關係</span>表按 FID 排列，欄位包含 Current Setting Persists、Uses Data Buffer、Feature Name 及 Scope。持續性欄有腳註：其判讀對象是不可保存的 Feature，不能拿來推翻可保存功能的 Saved 值語意。</p>
<p class="qr-explanation" data-paragraph="B466-3"><span class="qr-step">04.3 · 判讀與例子</span>APST FID0Ch 需要 data buffer 保存逐 state 條目；Power Management FID02h 主要由 CDW11 指定。只複製 CDW11 而漏掉 APST 表，無法完整重建當時設定。</p>
<p class="qr-tags">搜尋詞：FID · Feature Identifier · scope · persistence · data buffer</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/features/zh-tw/#figure-b475">Base 2.4 Figure 475 · APST：是否允許自動切換</a><a href="/nvme/figure-reference/features/zh-tw/#figure-b477">Base 2.4 Figure 477 · APST Entry：從哪個 state、等多久、到哪裡</a><a href="/nvme/figure-reference/features/zh-tw/#figure-b468">Base 2.4 Figure 468 · Power Management：指定 state 與 idle 回應限制</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b340" data-figure="B340">
<h2><span class="qr-number">05</span>Power State Descriptor：功耗、延遲與可執行 I/O</h2>
<p class="qr-original">Base 2.4 · Figure 340 · Identify – Power State Descriptor Data Structure</p>
<p class="qr-location">§5.2.14.2.1 · 文件頁 384–386 · PDF 410–412</p>
<p class="qr-explanation" data-paragraph="B340-1"><span class="qr-step">05.1 · 用途</span>比較 power states 或排查喚醒延遲時，查各 state 的 32-byte 描述子。state 編號只用來選狀態，不能直接當功耗或效能排名。</p>
<p class="qr-explanation" data-paragraph="B340-2"><span class="qr-step">05.2 · 欄位與關係</span>NOPS bit25 區分是否處理 I/O；MP bits15:0 與 MXPS bit24 一起換算最大功耗；ENLAT bits63:32、EXLAT95:64 以微秒計。IDLP 配 IPS 讀 idle 功耗；RRT／RRL／RWT／RWL 是相對等級。後面另有 Active Power、掉電處理時間與頻寬欄位。</p>
<p class="qr-explanation" data-paragraph="B340-3"><span class="qr-step">05.3 · 判讀與例子</span>MP=350、MXPS=0 是 3.50 W；MXPS=1 則是 0.035 W。EXLAT=0 表示未回報，不能寫成零延遲。選 APST 目的 state 前，先看 NOPS 及有效功耗、延遲值。</p>
<p class="qr-tags">搜尋詞：PSD · NOPS · MP · MXPS · ENLAT · EXLAT · IDLP · IPS · RRT · RRL</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/features/zh-tw/#figure-b468">Base 2.4 Figure 468 · Power Management：指定 state 與 idle 回應限制</a><a href="/nvme/figure-reference/features/zh-tw/#figure-b477">Base 2.4 Figure 477 · APST Entry：從哪個 state、等多久、到哪裡</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b467" data-figure="B467">
<h2><span class="qr-number">06</span>Arbitration：權重不是效能保證</h2>
<p class="qr-original">Base 2.4 · Figure 467 · Arbitration &amp; Command Processing – Command Dword 11</p>
<p class="qr-location">§5.2.30.1.1 · 文件頁 460 · PDF 486</p>
<p class="qr-explanation" data-paragraph="B467-1"><span class="qr-step">06.1 · 用途</span>比較不同 SQ 優先級或命令取走節奏時，查此表。但設定權重不保證應用程式獲得固定比例 IOPS，還受排程模式與工作負載影響。</p>
<p class="qr-explanation" data-paragraph="B467-2"><span class="qr-step">06.2 · 欄位與關係</span>HPW bits31:24、MPW23:16、LPW15:8 是各 service class 每輪可執行命令數減 1。AB bits2:0 是單次由一個 SQ 取命令的上限，按 2^AB 計，AB=7 特別表示無限制。</p>
<p class="qr-explanation" data-paragraph="B467-3"><span class="qr-step">06.3 · 判讀與例子</span>HPW=3 代表 4 個命令，AB=3 代表 burst 上限 8 個；相同原始值使用不同編碼。先確認 CC.AMS 使用的排程模式，才有意義地解讀 priority 權重。</p>
<p class="qr-tags">搜尋詞：FID 01h · HPW · MPW · LPW · AB · arbitration</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/init/zh-tw/#figure-b41">Base 2.4 Figure 41 · CC：主機實際選了什麼</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b468" data-figure="B468">
<h2><span class="qr-number">07</span>Power Management：指定 state 與 idle 回應限制</h2>
<p class="qr-original">Base 2.4 · Figure 468 · Power Management – Command Dword 11</p>
<p class="qr-location">§5.2.30.1.2 · 文件頁 461 · PDF 487</p>
<p class="qr-explanation" data-paragraph="B468-1"><span class="qr-step">07.1 · 用途</span>主機明確要求切 power state 時，這張表定義 CDW11。它與 APST 的自動轉換表不同，不能只看到 PS 值就重建全部自動轉換行為。</p>
<p class="qr-explanation" data-paragraph="B468-2"><span class="qr-step">07.2 · 欄位與關係</span>PS bits4:0 選 state，WH bits7:5 給 workload hint；IIELL bits31:16 在支援且選 operational state 時，以 100 微秒指定 idle 後 I/O 額外延遲限制。IIELL 的作用範圍另由 IIELLSS 決定。</p>
<p class="qr-explanation" data-paragraph="B468-3"><span class="qr-step">07.3 · 判讀與例子</span>IIELL=5 表示 500 微秒，不是 5 毫秒。對 non-operational state 設定非 0 IIELL，在此能力受支援時會因 Invalid Field in Command 失敗；先由 Power State Descriptor 確認 state 種類。</p>
<p class="qr-tags">搜尋詞：FID 02h · PS · WH · IIELL · IIELLSS</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/features/zh-tw/#figure-b340">Base 2.4 Figure 340 · Power State Descriptor：功耗、延遲與可執行 I/O</a><a href="/nvme/figure-reference/features/zh-tw/#figure-b475">Base 2.4 Figure 475 · APST：是否允許自動切換</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b471" data-figure="B471">
<h2><span class="qr-number">08</span>Volatile Write Cache：目前 enable 位</h2>
<p class="qr-original">Base 2.4 · Figure 471 · Volatile Write Cache – Command Dword 11</p>
<p class="qr-location">§5.2.30.1.4 · 文件頁 464–465 · PDF 490–491</p>
<p class="qr-explanation" data-paragraph="B471-1"><span class="qr-step">08.1 · 用途</span>判斷 Write 完成是否可能只到揮發性 cache 時，查 WCE 設定，再結合 cache 是否存在與命令 FUA。WCE 不是硬體是否有 cache 的能力位。</p>
<p class="qr-explanation" data-paragraph="B471-2"><span class="qr-step">08.2 · 欄位與關係</span>CDW11 bit0 為 WCE，1 啟用、0 停用，bits31:1 保留。實際 cache 存在性還需依 Identify 與 namespace／FDP 配置判斷；Flush 與 FUA 另有各自的非揮發要求。</p>
<p class="qr-explanation" data-paragraph="B471-3"><span class="qr-step">08.3 · 判讀與例子</span>WCE=1 不能單獨證明某筆 Write 只在 cache 中，因為那筆命令可能 FUA=1。比較資料保留結果，需同時保存 cache 能力、WCE 及命令內容。</p>
<p class="qr-tags">搜尋詞：FID 06h · WCE · VWC · volatile cache · Flush</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify Controller：能力與限制的主要入口</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-b346">Base 2.4 Figure 346 · Namespace 共通狀態：可用、受保護與儲存歸屬</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n71">NVM Command Set 1.3 Figure 71 · Write CDW12：持久性、PI 與配置提示</a><a href="/nvme/figure-reference/features/zh-tw/#figure-b294">Base 2.4 Figure 294 · FDP Configuration：配置大小、資源數與 PID 切割</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b472" data-figure="B472">
<h2><span class="qr-number">09</span>Number of Queues：主機要求的數量</h2>
<p class="qr-original">Base 2.4 · Figure 472 · Number of Queues – Command Dword 11</p>
<p class="qr-location">§5.2.30.1.5 · 文件頁 465 · PDF 491</p>
<p class="qr-explanation" data-paragraph="B472-1"><span class="qr-step">09.1 · 用途</span>初始化要建立多組 I/O queues 前，用此表解讀主機要求分配的數量。它不是每個 queue 的深度，也不包括 Admin queues。</p>
<p class="qr-explanation" data-paragraph="B472-2"><span class="qr-step">09.2 · 欄位與關係</span>NSQR bits15:0 要求 SQ 數，NCQR bits31:16 要求 CQ 數，兩者都減 1 編碼；最大可指定原始值 FFFEh。此設定應在建立 I/O queues 前完成，實際分配量由 CQE DW0 回報。</p>
<p class="qr-explanation" data-paragraph="B472-3"><span class="qr-step">09.3 · 判讀與例子</span>要求 8 個 SQ 與 4 個 CQ，CDW11=00030007h。主機不能直接依要求值建立全部 queues，而要先讀 Figure473 的實際結果。</p>
<p class="qr-tags">搜尋詞：FID 07h · NSQR · NCQR · queue allocation</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/features/zh-tw/#figure-b473">Base 2.4 Figure 473 · Number of Queues：實際分配的數量</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b473" data-figure="B473">
<h2><span class="qr-number">10</span>Number of Queues：實際分配的數量</h2>
<p class="qr-original">Base 2.4 · Figure 473 · Number of Queues – Completion Queue Entry Dword 0</p>
<p class="qr-location">§5.2.30.1.5 · 文件頁 466 · PDF 492</p>
<p class="qr-explanation" data-paragraph="B473-1"><span class="qr-step">10.1 · 用途</span>這張表解 Number of Queues 的完成回覆，用於確認 controller 實際保留多少 I/O queue 資源。要求量與分配量可以不同。</p>
<p class="qr-explanation" data-paragraph="B473-2"><span class="qr-step">10.2 · 欄位與關係</span>DW0 的 NSQA bits15:0、NCQA bits31:16 分別是實際 SQ／CQ 數減 1。它不是 queue ID 清單，也不表示這些 queue 已完成 Create。</p>
<p class="qr-explanation" data-paragraph="B473-3"><span class="qr-step">10.3 · 判讀與例子</span>DW0=00010003h 表示 4 個 SQ、2 個 CQ。即使先前要求 8 與 4，也要依回覆安排後續建立；分配資源與建立 queue 是兩個步驟。</p>
<p class="qr-tags">搜尋詞：NSQA · NCQA · CQE DW0 · allocated queues</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/features/zh-tw/#figure-b472">Base 2.4 Figure 472 · Number of Queues：主機要求的數量</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b475" data-figure="B475">
<h2><span class="qr-number">11</span>APST：是否允許自動切換</h2>
<p class="qr-original">Base 2.4 · Figure 475 · Autonomous Power State Transition – Command Dword 11</p>
<p class="qr-location">§5.2.30.1.7 · 文件頁 468 · PDF 494</p>
<p class="qr-explanation" data-paragraph="B475-1"><span class="qr-step">11.1 · 用途</span>設定了 idle 轉換表卻沒有預期省電行為時，先查 APSTE 是否開啟。這張表只定義總開關，不包含每個 state 的等待時間。</p>
<p class="qr-explanation" data-paragraph="B475-2"><span class="qr-step">11.2 · 欄位與關係</span>CDW11 bit0 為 APSTE，1 啟用、0 停用，預設 0；其他 bits 保留。每個來源 power state 的等待條件與目的 state 另放在 APST data structure。</p>
<p class="qr-explanation" data-paragraph="B475-3"><span class="qr-step">11.3 · 判讀與例子</span>APSTE=1 不代表立刻進入最低功耗 state。仍需該來源 state 的 ITPT 非 0，並滿足連續 idle 條件；因此 trace 應一起保存總開關與對應 table entry。</p>
<p class="qr-tags">搜尋詞：FID 0Ch · APSTE · APST · autonomous power</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/features/zh-tw/#figure-b477">Base 2.4 Figure 477 · APST Entry：從哪個 state、等多久、到哪裡</a><a href="/nvme/figure-reference/features/zh-tw/#figure-b340">Base 2.4 Figure 340 · Power State Descriptor：功耗、延遲與可執行 I/O</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b477" data-figure="B477">
<h2><span class="qr-number">12</span>APST Entry：從哪個 state、等多久、到哪裡</h2>
<p class="qr-original">Base 2.4 · Figure 477 · Autonomous Power State Transition Data Structure Entry</p>
<p class="qr-location">§5.2.30.1.7 · 文件頁 469 · PDF 495</p>
<p class="qr-explanation" data-paragraph="B477-1"><span class="qr-step">12.1 · 用途</span>這張表用於解每個來源 state 的 8-byte 轉換條目。條目的陣列位置決定來源 state，ITPS 決定目的 state，兩者不能對調。</p>
<p class="qr-explanation" data-paragraph="B477-2"><span class="qr-step">12.2 · 欄位與關係</span>ITPT bits31:8 以毫秒表示連續 idle 門檻，0 停用該來源 state 的轉換；ITPS bits7:3 指定目的 state。ITPT 非 0 時目的 state 須為 non-operational。高 32bits 與低 3bits 保留。</p>
<p class="qr-explanation" data-paragraph="B477-3"><span class="qr-step">12.3 · 判讀與例子</span>來源 PS0 條目設定 ITPT=2000、ITPS=3，低 Dword 是(2000&lt;&lt;8)|(3&lt;&lt;3)=0007D018h。表示在 PS0 連續 idle 超過 2000 ms 後可依規則到 PS3，不是進入 PS3 後再等 2000 ms。</p>
<p class="qr-tags">搜尋詞：ITPT · ITPS · APST entry · idle transition</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/features/zh-tw/#figure-b475">Base 2.4 Figure 475 · APST：是否允許自動切換</a><a href="/nvme/figure-reference/features/zh-tw/#figure-b340">Base 2.4 Figure 340 · Power State Descriptor：功耗、延遲與可執行 I/O</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b482" data-figure="B482">
<h2><span class="qr-number">13</span>HCTM：兩個熱管理門檻</h2>
<p class="qr-original">Base 2.4 · Figure 482 · HCTM – Command Dword 11</p>
<p class="qr-location">§5.2.30.1.10 · 文件頁 472 · PDF 498</p>
<p class="qr-explanation" data-paragraph="B482-1"><span class="qr-step">13.1 · 用途</span>效能隨溫度下降時，查 Host Controlled Thermal Management 的門檻。它們是主機要求的管理條件，不等於 SMART 當下溫度。</p>
<p class="qr-explanation" data-paragraph="B482-2"><span class="qr-step">13.2 · 欄位與關係</span>TMT1 bits31:16 為較輕管理門檻，TMT2 bits15:0 為較重管理門檻，皆以 Kelvin 計；0 停用該部分。非 0 值須落在 Identify 允許範圍；TMT2 非 0 時必須大於 TMT1。</p>
<p class="qr-explanation" data-paragraph="B482-3"><span class="qr-step">13.3 · 判讀與例子</span>TMT1=343、TMT2=353 約為 69.85°C 與 79.85°C，不是 343°C 和 353°C。是否實際啟動與累計多久，可再查 SMART 的 transition count 與 total time。</p>
<p class="qr-tags">搜尋詞：FID 10h · HCTM · TMT1 · TMT2 · Kelvin · throttling</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-b213">Base 2.4 Figure 213 · SMART：警告、累計量、溫度與時間</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify Controller：能力與限制的主要入口</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b543" data-figure="B543">
<h2><span class="qr-number">14</span>Interrupt Coalescing：延後中斷的時間與數量</h2>
<p class="qr-original">Base 2.4 · Figure 543 · Interrupt Coalescing – Command Dword 11</p>
<p class="qr-location">§5.2.30.2.1 · 文件頁 515 · PDF 541</p>
<p class="qr-explanation" data-paragraph="B543-1"><span class="qr-step">14.1 · 用途</span>CQ 已有資料但中斷時間較晚時，可用此表核對 coalescing 設定。它控制中斷聚合，不改變 CQE 本身的命令 status。</p>
<p class="qr-explanation" data-paragraph="B543-2"><span class="qr-step">14.2 · 欄位與關係</span>TIME bits15:8 以 100 微秒為單位，0 無延遲；THR bits7:0 為建議聚合 CQE 數減 1。任一欄為 0 時隱含停用 coalescing。只適用 I/O queues，Admin CQ 不支援；每個向量還有自己的設定。</p>
<p class="qr-explanation" data-paragraph="B543-3"><span class="qr-step">14.3 · 判讀與例子</span>TIME=5、THR=7 代表 500 微秒與 8 筆的建議條件，不是每個 I/O 必定延遲 500 微秒。主機持續更新 CQ head 時，聚合條件可能重啟，因此不能把 TIME 直接當端到端延遲上限。</p>
<p class="qr-tags">搜尋詞：FID 08h · TIME · THR · coalescing · interrupt latency</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/init/zh-tw/#figure-p44">PCIe Transport 1.4 Figure 44 · MSI-X：總開關、遮罩與向量數</a><a href="/nvme/figure-reference/init/zh-tw/#figure-p6">PCIe Transport 1.4 Figure 6 · CQ doorbell：歸還已讀取的位置</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b545" data-figure="B545">
<h2><span class="qr-number">15</span>HMB：啟用、新配置或返還原記憶體</h2>
<p class="qr-original">Base 2.4 · Figure 545 · Host Memory Buffer – Command Dword 11</p>
<p class="qr-location">§5.2.30.2.3 · 文件頁 516–517 · PDF 542–543</p>
<p class="qr-explanation" data-paragraph="B545-1"><span class="qr-step">15.1 · 用途</span>重設或電源切換後重新啟用 Host Memory Buffer 時，查 MR 和 EHM，避免把重新配置的記憶體宣稱成原封不動返還。HMB 是提供 controller 使用的 host 記憶體。</p>
<p class="qr-explanation" data-paragraph="B545-2"><span class="qr-step">15.2 · 欄位與關係</span>EHM bit0 為啟用，MR bit1 表示返還先前的同一份 HMB；HMNARE bit2 在支援時限制 non-operational state 存取，仍有 Admin 處理例外。bit3 必須清 0。MR=1 要求 size、descriptor 地址／內容及 buffer 內容與停用前一致。</p>
<p class="qr-explanation" data-paragraph="B545-3"><span class="qr-step">15.3 · 判讀與例子</span>若重新配置後清掉了 buffer，即使實體地址剛好一樣，也不能使用 MR=1 宣稱原內容仍在。EHM=0 時 CDW12～15 被忽略，不能拿那些 bytes 推論已啟用的大小。</p>
<p class="qr-tags">搜尋詞：FID 0Dh · HMB · EHM · MR · HMNARE</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify Controller：能力與限制的主要入口</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b294" data-figure="B294">
<h2><span class="qr-number">16</span>FDP Configuration：配置大小、資源數與 PID 切割</h2>
<p class="qr-original">Base 2.4 · Figure 294 · FDP Configuration Descriptor</p>
<p class="qr-location">§5.2.13.1.29 · 文件頁 293–295 · PDF 319–321</p>
<p class="qr-explanation" data-paragraph="B294-1"><span class="qr-step">16.1 · 用途</span>解 FDP 資源配置或 Placement Identifier 前，查目前配置描述子。PID 不是固定格式的任意數字，Reclaim Group 與 Placement Handle 的切割取決於 RGIF。</p>
<p class="qr-explanation" data-paragraph="B294-2"><span class="qr-step">16.2 · 欄位與關係</span>DSZE bytes1:0 給整個描述子大小；FDPA byte2 含 FDPCV 有效位、FDPVWC 及 RGIF。NRG bytes7:4、NRUH9:8 是直接數量，MAXPIDS11:10 則減 1 編碼。RUNS23:16 是 nominal bytes，ERUTL27:24 是秒，0 表示未回報。</p>
<p class="qr-explanation" data-paragraph="B294-3"><span class="qr-step">16.3 · 判讀與例子</span>NRUH=4 表示 4 個 handle 描述子，不是 5 個；MAXPIDS=3 才對應最多 4 個 placement identifiers。變長清單後還可能有 vendor bytes 及 padding，走到下一份 configuration 應依 DSZE。</p>
<p class="qr-tags">搜尋詞：LID 20h · FDP · DSZE · FDPCV · RGIF · NRG · NRUH · RUNS · ERUTL</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/features/zh-tw/#figure-n21">NVM Command Set 1.3 Figure 21 · RUH Status：目前剩餘可寫量</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n71">NVM Command Set 1.3 Figure 71 · Write CDW12：持久性、PI 與配置提示</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n21" data-figure="N21">
<h2><span class="qr-number">17</span>RUH Status：目前剩餘可寫量</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 21 · Reclaim Unit Handle Status Descriptor</p>
<p class="qr-location">§3.2.1.1 · 文件頁 26 · PDF 26</p>
<p class="qr-explanation" data-paragraph="N21-1"><span class="qr-step">17.1 · 用途</span>想知道某個 placement 指向的 Reclaim Unit 目前還可寫多少，查這張 NVM 專屬 status 描述子。它是當下回報，不能用 nominal 容量直接取代。</p>
<p class="qr-explanation" data-paragraph="N21-2"><span class="qr-step">17.2 · 欄位與關係</span>PID bytes1:0、RUHID3:2 對應 placement 與 handle；EARUTR7:4 是估計剩餘秒數，0 表示未回報；RUAMW15:8 是目前可寫入的 logical blocks。後 16bytes 保留。</p>
<p class="qr-explanation" data-paragraph="N21-3"><span class="qr-step">17.3 · 判讀與例子</span>RUAMW=1000 且格式 4 KiB，表示 4,096,000bytes 的 blocks 計量；它可小於或大於 RUNS 所報 nominal bytes。EARUTR=0 不表示 Reclaim Unit 已立刻過期。</p>
<p class="qr-tags">搜尋詞：RUH · PID · RUHID · EARUTR · RUAMW · I/O Management Receive</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/features/zh-tw/#figure-b294">Base 2.4 Figure 294 · FDP Configuration：配置大小、資源數與 PID 切割</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-n125">NVM Command Set 1.3 Figure 125 · LBAF：資料大小、metadata 大小與相對效能</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<footer id="source-files"><h2>原始文件</h2><p>頁碼採本次提供的 ratified PDF；Base 的 PDF 頁＝文件頁＋26，另兩份相同。圖號與英文原名保留，可用 PDF 搜尋定位。公開網站不附原始 PDF。</p><ul class="qr-sources"><li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li></ul></footer>
</main></div>
