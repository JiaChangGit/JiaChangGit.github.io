---
layout: "post"
title: "NVMe 圖表速查 04 · I/O 命令與資料完整性"
date: "2026-09-29 09:00:00 +0800"
categories: ["nvme"]
tags: ["NVMe", "Reference"]
permalink: "/nvme/figure-reference/io/zh-tw/"
nvme_quickref: true
lang: "zh-Hant-TW"
description: "NVMe 原圖用途、欄位與判讀速查，附完整 Spec 位置。"
---

<div class="nvme-quickref">
<nav class="qr-top" aria-label="版本與索引"><a href="#content">跳到內容</a><a href="/nvme/figure-reference/zh-tw/">總索引</a><a href="/nvme/figure-reference/io/en/">English</a><a href="/DOCS/nvme-quick-reference/io.html">繁中 HTML</a></nav>
<main id="content">
<header><p class="qr-eyebrow">反覆查詢 · 欄位判讀 · 原文定位</p><h1>NVMe 圖表速查 04 · I/O 命令與資料完整性</h1><p class="qr-intro">由命令的位址與數量走到 metadata、保護資訊和原子性。相同欄位寬度不代表相同計數方式，命令成功也不等於所有持久性與原子性保證都成立。</p></header>
<aside class="qr-note"><p>每張原圖都有用途、欄位和判讀例子。例子中的數值用於說明，不代表你的裝置設定；原文另有條件時，依該欄位與命令定義判斷。</p><p>用瀏覽器「在頁面中尋找」搜尋欄位、FID、LID、CNS 或 Figure。bit／byte 位置沿用原圖：bit 是位元，byte 是 8 bits，Dword 是 4 bytes；index 是第幾筆，offset 是相對起點的偏移，須看當處使用的單位。</p><p>FID（Feature Identifier）選擇功能；LID（Log Page Identifier）選擇紀錄頁；CNS（Controller or Namespace Structure）選擇 Identify 回傳的資料結構。</p></aside>
<nav class="qr-toc" id="figure-index" aria-label="本冊圖表索引"><h2>本冊圖表</h2><ol>
<li><a href="#figure-n4">NVM Command Set 1.3 Figure 4 · Single Atomicity：單位、條件與邊界的關係</a></li>
<li><a href="#figure-n8">NVM Command Set 1.3 Figure 8 · Atomic Boundary：同樣大小，不同起點會有不同結果</a></li>
<li><a href="#figure-n22">NVM Command Set 1.3 Figure 22 · NVM opcode：先確認命令集再解碼</a></li>
<li><a href="#figure-n53">NVM Command Set 1.3 Figure 53 · Read 起點：64-bit SLBA</a></li>
<li><a href="#figure-n54">NVM Command Set 1.3 Figure 54 · Read CDW12：範圍、重試與保護要求</a></li>
<li><a href="#figure-n70">NVM Command Set 1.3 Figure 70 · Write 起點：把 LBA 與 DMA 地址分開</a></li>
<li><a href="#figure-n71">NVM Command Set 1.3 Figure 71 · Write CDW12：持久性、PI 與配置提示</a></li>
<li><a href="#figure-n39">NVM Command Set 1.3 Figure 39 · Copy 描述子：格式決定 namespace 與 PI 配置</a></li>
<li><a href="#figure-n47">NVM Command Set 1.3 Figure 47 · Dataset Management：每段 LBA 範圍如何排列</a></li>
<li><a href="#figure-n83">NVM Command Set 1.3 Figure 83 · Write Zeroes：清零範圍與 deallocate 要求</a></li>
<li><a href="#figure-n153">NVM Command Set 1.3 Figure 153 · Extended LBA：資料與 metadata 交錯</a></li>
<li><a href="#figure-n154">NVM Command Set 1.3 Figure 154 · Separate Metadata：兩個 buffer 依 LBA 配對</a></li>
<li><a href="#figure-n155">NVM Command Set 1.3 Figure 155 · 16-bit Guard PI：8 bytes 的實際配置</a></li>
<li><a href="#figure-n157">NVM Command Set 1.3 Figure 157 · 32-bit Guard PI：16-byte 格式</a></li>
<li><a href="#figure-n159">NVM Command Set 1.3 Figure 159 · 64-bit Guard PI：較大 Guard 與 48-bit 標籤空間</a></li>
<li><a href="#figure-n174">NVM Command Set 1.3 Figure 174 · Write 的 PRACT：host 要提供多少 metadata</a></li>
<li><a href="#figure-n175">NVM Command Set 1.3 Figure 175 · Read 的 PRACT：回主機時保留或移除哪些資料</a></li>
</ol></nav>
<article class="qr-card" id="figure-n4" data-figure="N4">
<h2><span class="qr-number">01</span>Single Atomicity：單位、條件與邊界的關係</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 4 · Atomicity Parameters for Single Atomicity Mode</p>
<p class="qr-location">§2.1.4 · 文件頁 15–16 · PDF 15–16</p>
<p class="qr-explanation" data-paragraph="N4-1"><span class="qr-step">01.1 · 用途</span>需要驗證某次寫入是否享有整筆原子性時，用這張表整理 controller 基準、namespace 專屬值與 boundary 條件。這張表明確針對 Single Atomicity Mode。</p>
<p class="qr-explanation" data-paragraph="N4-2"><span class="qr-step">01.2 · 欄位與關係</span>AWUN／AWUPF 分別對應正常操作與斷電情境，ACWU 用於融合 Compare and Write；NA 前綴是 namespace 值。NABSN／NABSPF 與 NABO 控制邊界。表中的不等式描述支援時必須成立的參數關係，實際值仍須按各欄編碼換算。</p>
<p class="qr-explanation" data-paragraph="N4-3"><span class="qr-step">01.3 · 判讀與例子</span>一筆寫入即使未超過 NAWUN，跨 namespace atomic boundary 時，Single Atomicity Mode 也不保證該整筆符合 namespace 原子性。先看模式、單位大小，再看起點與範圍，不能只比較 NLB。</p>
<p class="qr-tags">搜尋詞：AWUN · AWUPF · NAWUN · NAWUPF · ACWU · NACWU · atomicity</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/io/zh-tw/#figure-n8">NVM Command Set 1.3 Figure 8 · Atomic Boundary：同樣大小，不同起點會有不同結果</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-n123">NVM Command Set 1.3 Figure 123 · NVM Namespace：容量、格式、原子性與建議粒度</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n8" data-figure="N8">
<h2><span class="qr-number">02</span>Atomic Boundary：同樣大小，不同起點會有不同結果</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 8 · Atomic Boundaries Example</p>
<p class="qr-location">§2.1.4.4 · 文件頁 19 · PDF 19</p>
<p class="qr-explanation" data-paragraph="N8-1"><span class="qr-step">02.1 · 用途</span>這張圖把原子性邊界畫成相鄰區間，適合快速判斷一段 LBA 是否跨界。圖中顏色區分區間，不代表不同 namespace 或不同媒體。</p>
<p class="qr-explanation" data-paragraph="N8-2"><span class="qr-step">02.2 · 欄位與關係</span>第一個界線由 NABO 決定，後續界線依解碼後的 boundary size 等距排列。寫入範圍由 SLBA 與 blocks 數決定；NABSN 和 NABSPF 對應不同情境，原始欄位值還有 0 及減 1 編碼規則。</p>
<p class="qr-explanation" data-paragraph="N8-3"><span class="qr-step">02.3 · 判讀與例子</span>以已解碼的 boundary size=8 blocks、offset=0 為例，LBA4～7 留在一區，LBA6～9 跨越 8 的界線。兩者都是 4 blocks，但後者不能只憑大小就宣稱享有 Single Atomicity 整筆保證。</p>
<p class="qr-tags">搜尋詞：NABO · NABSN · NABSPF · atomic boundary · alignment</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/io/zh-tw/#figure-n4">NVM Command Set 1.3 Figure 4 · Single Atomicity：單位、條件與邊界的關係</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-n123">NVM Command Set 1.3 Figure 123 · NVM Namespace：容量、格式、原子性與建議粒度</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n22" data-figure="N22">
<h2><span class="qr-number">03</span>NVM opcode：先確認命令集再解碼</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 22 · Opcodes for NVM Commands</p>
<p class="qr-location">§3.3 · 文件頁 27 · PDF 27</p>
<p class="qr-explanation" data-paragraph="N22-1"><span class="qr-step">03.1 · 用途</span>解析 I/O trace 時，用這張表把 opcode 對回 NVM 命令。相同 opcode 在 Admin 與 I/O queue 不一定代表相同操作。</p>
<p class="qr-explanation" data-paragraph="N22-2"><span class="qr-step">03.2 · 欄位與關係</span>表列出 opcode、命令名稱與定義位置，包括 Flush00h、Write01h、Read02h、Compare05h、Write Zeroes08h、Dataset Management09h、Verify0Ch、Copy19h。支援要求仍需搭配能力回報。</p>
<p class="qr-explanation" data-paragraph="N22-3"><span class="qr-step">03.3 · 判讀與例子</span>OPC=02h 出現在 NVM I/O SQ 是 Read；出現在 Admin SQ 則不能套用這張表。保留 queue 種類、CSI 與 opcode 一起查，才不會把 log 讀取誤當成媒體讀取。</p>
<p class="qr-tags">搜尋詞：opcode · Read 02h · Write 01h · Flush 00h · Compare 05h · Copy 19h</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b92">Base 2.4 Figure 92 · CDW0：先辨認命令與資料指標格式</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n53">NVM Command Set 1.3 Figure 53 · Read 起點：64-bit SLBA</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n70">NVM Command Set 1.3 Figure 70 · Write 起點：把 LBA 與 DMA 地址分開</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n53" data-figure="N53">
<h2><span class="qr-number">04</span>Read 起點：64-bit SLBA</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 53 · Read – Command Dword 10 and Command Dword 11</p>
<p class="qr-location">§3.3.4 · 文件頁 49 · PDF 49</p>
<p class="qr-explanation" data-paragraph="N53-1"><span class="qr-step">04.1 · 用途</span>核對 Read 是否讀錯位置時，先從 CDW10／11 合成完整 SLBA。這是 namespace 內的 logical block 地址，不是 host buffer 地址。</p>
<p class="qr-explanation" data-paragraph="N53-2"><span class="qr-step">04.2 · 欄位與關係</span>SLBA 佔 64bits，低 32bits 在 CDW10、高 32bits 在 CDW11。實際 bytes 位置取決於目前 LBA 大小；命令長度由 CDW12.NLB 另外提供。</p>
<p class="qr-explanation" data-paragraph="N53-3"><span class="qr-step">04.3 · 判讀與例子</span>CDW11=1、CDW10=0 表示 SLBA=4294967296，不能只看低位而當成 LBA0。範圍尾端是 SLBA+NLB，因為 NLB 原始值是 blocks 數減 1。</p>
<p class="qr-tags">搜尋詞：Read · SLBA · CDW10 · CDW11</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/io/zh-tw/#figure-n54">NVM Command Set 1.3 Figure 54 · Read CDW12：範圍、重試與保護要求</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-n123">NVM Command Set 1.3 Figure 123 · NVM Namespace：容量、格式、原子性與建議粒度</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n54" data-figure="N54">
<h2><span class="qr-number">05</span>Read CDW12：範圍、重試與保護要求</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 54 · Read – Command Dword 12</p>
<p class="qr-location">§3.3.4 · 文件頁 49 · PDF 49</p>
<p class="qr-explanation" data-paragraph="N54-1"><span class="qr-step">05.1 · 用途</span>讀取的長度、重試方式或保護檢查與預期不同時，查 CDW12。這些控制位各自有目的，不是同一種「嚴格讀取」開關。</p>
<p class="qr-explanation" data-paragraph="N54-2"><span class="qr-step">05.2 · 欄位與關係</span>NLB bits15:0 為 blocks 數減 1；CETYPE bits19:16 選命令擴充；STC bit24 控制 Storage Tag 檢查；PRINFO bits29:26 含 PI 動作與檢查；FUA bit30 要求相關資料與 metadata 提交到非揮發媒體並由該媒體讀回，LR bit31 要求有限重試。</p>
<p class="qr-explanation" data-paragraph="N54-3"><span class="qr-step">05.3 · 判讀與例子</span>NLB=7、每 block4096bytes，資料量是 32768bytes。FUA 不隱含與其他命令的先後順序；LR 也不等於固定時間內必定完成。</p>
<p class="qr-tags">搜尋詞：Read NLB · LR · FUA · PRINFO · STC · CETYPE</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/io/zh-tw/#figure-n53">NVM Command Set 1.3 Figure 53 · Read 起點：64-bit SLBA</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n175">NVM Command Set 1.3 Figure 175 · Read 的 PRACT：回主機時保留或移除哪些資料</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n70" data-figure="N70">
<h2><span class="qr-number">06</span>Write 起點：把 LBA 與 DMA 地址分開</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 70 · Write – Command Dword 10 and Command Dword 11</p>
<p class="qr-location">§3.3.6 · 文件頁 54 · PDF 54</p>
<p class="qr-explanation" data-paragraph="N70-1"><span class="qr-step">06.1 · 用途</span>寫錯區域的問題要分別查 NVM 目的 LBA 與主機來源 buffer。這張表只定義 Write 的 SLBA，不描述 PRP 或 SGL 地址。</p>
<p class="qr-explanation" data-paragraph="N70-2"><span class="qr-step">06.2 · 欄位與關係</span>CDW10／11 合成 64-bit SLBA，分別為低 32 與高 32bits。SLBA 以所選 namespace 格式的 blocks 為單位，不直接以 512-byte sectors 計。</p>
<p class="qr-explanation" data-paragraph="N70-3"><span class="qr-step">06.3 · 判讀與例子</span>同樣 SLBA=8，在 512-byte 格式的資料起點是 4096bytes，在 4 KiB 格式是 32768bytes。先確認格式，再與應用程式的 byte offset 換算結果比較。</p>
<p class="qr-tags">搜尋詞：Write · SLBA · destination LBA</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/io/zh-tw/#figure-n71">NVM Command Set 1.3 Figure 71 · Write CDW12：持久性、PI 與配置提示</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-n125">NVM Command Set 1.3 Figure 125 · LBAF：資料大小、metadata 大小與相對效能</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b93">Base 2.4 Figure 93 · 64-byte 命令的共同位置</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n71" data-figure="N71">
<h2><span class="qr-number">07</span>Write CDW12：持久性、PI 與配置提示</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 71 · Write – Command Dword 12</p>
<p class="qr-location">§3.3.6 · 文件頁 54 · PDF 54</p>
<p class="qr-explanation" data-paragraph="N71-1"><span class="qr-step">07.1 · 用途</span>驗證 Write completion 代表哪些保證時，查這張表的 FUA 與 PI 控制，也要保留 namespace 格式和 cache 情境。完成不等於所有其他寫入也一起持久化。</p>
<p class="qr-explanation" data-paragraph="N71-2"><span class="qr-step">07.2 · 欄位與關係</span>NLB bits15:0 是 blocks 數減 1，CETYPE19:16 與 DTYPE23:20 分別指定命令擴充和 Directive；STC24、PRINFO29:26 控制保護，FUA30 要求本命令資料與 metadata 在完成前寫入非揮發媒體，LR31 控制重試努力。</p>
<p class="qr-explanation" data-paragraph="N71-3"><span class="qr-step">07.3 · 判讀與例子</span>FUA=1 強化的是這筆 Write 的完成條件，不建立與另一筆 Write 的隱含順序。使用 FDP 或 Streams 時，也要依 DTYPE 與 CETYPE 解 CDW13，不能把相同 16bits 永遠當同一種 identifier。</p>
<p class="qr-tags">搜尋詞：Write NLB · FUA · LR · PRINFO · DTYPE · CETYPE · STC</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/features/zh-tw/#figure-b471">Base 2.4 Figure 471 · Volatile Write Cache：目前 enable 位</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n174">NVM Command Set 1.3 Figure 174 · Write 的 PRACT：host 要提供多少 metadata</a><a href="/nvme/figure-reference/features/zh-tw/#figure-b294">Base 2.4 Figure 294 · FDP Configuration：配置大小、資源數與 PID 切割</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n39" data-figure="N39">
<h2><span class="qr-number">08</span>Copy 描述子：格式決定 namespace 與 PI 配置</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 39 · Copy – Copy Descriptor Formats</p>
<p class="qr-location">§3.3.2 · 文件頁 32 · PDF 32</p>
<p class="qr-explanation" data-paragraph="N39-1"><span class="qr-step">08.1 · 用途</span>解析 Copy 來源清單前，先查描述子格式。格式決定是否有來源 NSID，以及保護資訊屬於哪種配置；選錯格式會把後續 bytes 全部讀錯。</p>
<p class="qr-explanation" data-paragraph="N39-2"><span class="qr-step">08.2 · 欄位與關係</span>格式 0／1 沒有 SNSID，來源與目的 namespace 相同；格式 2／3 包含 SNSID，可指定不同來源 namespace。0／2 對應 8-byte、16-bit Guard PI；1／3 對應 16-byte、32 或 64-bit Guard PI。格式 4 另涉及 SLM 來源，其完整定義不在這三份來源規格中。</p>
<p class="qr-explanation" data-paragraph="N39-3"><span class="qr-step">08.3 · 判讀與例子</span>若 DF=2，不能使用格式 0 的固定位置假設來源 NSID 不存在。是否允許跨 namespace、格式是否相容與範圍限制，仍需配合 Copy 能力及該命令條件。</p>
<p class="qr-tags">搜尋詞：Copy · DF · SNSID · descriptor format</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-n19">NVM Command Set 1.3 Figure 19 · NVM 命令專屬錯誤與命令清單</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-n125">NVM Command Set 1.3 Figure 125 · LBAF：資料大小、metadata 大小與相對效能</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n47" data-figure="N47">
<h2><span class="qr-number">09</span>Dataset Management：每段 LBA 範圍如何排列</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 47 · Dataset Management – Range Definition</p>
<p class="qr-location">§3.3.3 · 文件頁 45 · PDF 45</p>
<p class="qr-explanation" data-paragraph="N47-1"><span class="qr-step">09.1 · 用途</span>解析 Dataset Management buffer 時，這張表把 range 編號和 byte offset 對在一起。range index 是第幾筆，offset 是距 buffer 起點多少 bytes。</p>
<p class="qr-explanation" data-paragraph="N47-2"><span class="qr-step">09.2 · 欄位與關係</span>每筆 16bytes：CATTR 在相對 bytes3:0，LLB 在 7:4，SLBA 在 15:8。第 i 筆起點為 16×i。LLB 直接表示 blocks 數，不用 Read／Write NLB 的加 1 規則；命令指定的 range 數另看 NR。</p>
<p class="qr-explanation" data-paragraph="N47-3"><span class="qr-step">09.3 · 判讀與例子</span>第 2 筆（index1）從 byte16 開始；SLBA=100、LLB=8 描述 LBA100～107。LLB=8 不表示 9blocks。是否所有範圍都會處理，還需核對 DMRL、DMRSL、DMSL 及 support-variant 能力。</p>
<p class="qr-tags">搜尋詞：DSM · CATTR · LLB · SLBA · range index · offset</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-n129">NVM Command Set 1.3 Figure 129 · NVM 專屬 Controller：命令大小限制及其有效條件</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n83" data-figure="N83">
<h2><span class="qr-number">10</span>Write Zeroes：清零範圍與 deallocate 要求</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 83 · Write Zeroes – Command Dword 12</p>
<p class="qr-location">§3.3.8 · 文件頁 59–60 · PDF 59–60</p>
<p class="qr-explanation" data-paragraph="N83-1"><span class="qr-step">10.1 · 用途</span>這張表可區分一般範圍清零、要求 deallocate 與整個 namespace 清零。名字相近不代表具有 Sanitize 的安全清除保證。</p>
<p class="qr-explanation" data-paragraph="N83-2"><span class="qr-step">10.2 · 欄位與關係</span>NLB bits15:0 為 blocks 數減 1；NSZ bit23 要求整個 namespace 處理，需搭配 DEAC bit25 及支援能力。STC bit24 與 PRCHK 必須清 0；FUA bit30 描述完成前的非揮發要求。</p>
<p class="qr-explanation" data-paragraph="N83-3"><span class="qr-step">10.3 · 判讀與例子</span>NSZ=1 但 DEAC=0 會得到 Invalid Field in Command；NSZ=1 時 NLB 由 controller 忽略，不能再用 NLB=0 推論只處理 1block。操作範圍要先由 NSZ 及能力判斷。</p>
<p class="qr-tags">搜尋詞：Write Zeroes · DEAC · NSZ · NLB · PRCHK · STC</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-n129">NVM Command Set 1.3 Figure 129 · NVM 專屬 Controller：命令大小限制及其有效條件</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b451">Base 2.4 Figure 451 · Subsystem Sanitize：動作與完成模式</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n153" data-figure="N153">
<h2><span class="qr-number">11</span>Extended LBA：資料與 metadata 交錯</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 153 · Metadata – Contiguous with LBA Data, Forming Extended LBA</p>
<p class="qr-location">§5.2.3 · 文件頁 129 · PDF 129</p>
<p class="qr-explanation" data-paragraph="N153-1"><span class="qr-step">11.1 · 用途</span>計算傳輸長度或尋找第 2 個 block 起點時，用此圖確認 extended LBA 的排列。它不是整批資料後面再附一整批 metadata。</p>
<p class="qr-explanation" data-paragraph="N153-2"><span class="qr-step">11.2 · 欄位與關係</span>圖中每個 LBA 的資料後接該 LBA 的 metadata，再接下一個 LBA；兩者透過同一資料 buffer 傳輸。資料大小由 LBADS 決定，metadata bytes 由 MS 決定，格式選擇由 namespace 設定決定。</p>
<p class="qr-explanation" data-paragraph="N153-3"><span class="qr-step">11.3 · 判讀與例子</span>若每 block4096-byte 資料、8-byte metadata，第二個 block 從 4104 開始，第三個從 8208 開始。以 4096 固定跨距讀取會把 metadata 誤當下一個 block 開頭。</p>
<p class="qr-tags">搜尋詞：extended LBA · metadata · MS · FLBAS</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-n125">NVM Command Set 1.3 Figure 125 · LBAF：資料大小、metadata 大小與相對效能</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n154">NVM Command Set 1.3 Figure 154 · Separate Metadata：兩個 buffer 依 LBA 配對</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n154" data-figure="N154">
<h2><span class="qr-number">12</span>Separate Metadata：兩個 buffer 依 LBA 配對</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 154 · Metadata – Transferred as Separate Buffer</p>
<p class="qr-location">§5.2.3 · 文件頁 130 · PDF 130</p>
<p class="qr-explanation" data-paragraph="N154-1"><span class="qr-step">12.1 · 用途</span>資料與 metadata 分開傳輸時，這張圖說明兩份 buffer 如何對應。它們雖不相鄰，每個 LBA 仍要配到自己那一份 metadata。</p>
<p class="qr-explanation" data-paragraph="N154-2"><span class="qr-step">12.2 · 欄位與關係</span>DPTR 指向資料 buffer，MPTR 描述 metadata；資料與 metadata 分別依 LBA 順序排列。使用 PRP 形式的 metadata buffer 時要求實體連續；SGL 用法再依 PSDT 和支援條件解讀。</p>
<p class="qr-explanation" data-paragraph="N154-3"><span class="qr-step">12.3 · 判讀與例子</span>2blocks、每 block4096+8bytes，資料 buffer 需 8192bytes，metadata 另需 16bytes；不是把 MPTR 指向資料 buffer 後第 8192byte 就能自動取得正確配置，必須是實際已準備好的 metadata 地址。</p>
<p class="qr-tags">搜尋詞：MPTR · separate metadata · DPTR · metadata buffer</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b93">Base 2.4 Figure 93 · 64-byte 命令的共同位置</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n153">NVM Command Set 1.3 Figure 153 · Extended LBA：資料與 metadata 交錯</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n155" data-figure="N155">
<h2><span class="qr-number">13</span>16-bit Guard PI：8 bytes 的實際配置</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 155 · 16b Guard Protection Information Format when STS field is cleared to 0h</p>
<p class="qr-location">§5.3.1.1 · 文件頁 131 · PDF 131</p>
<p class="qr-explanation" data-paragraph="N155-1"><span class="qr-step">13.1 · 用途</span>這張圖適用 16-bit Guard 且 STS=0 的 PI，常用來核對保護欄位位置和 byte order。不要把所有 PI 都當成這個 8-byte 格式。</p>
<p class="qr-explanation" data-paragraph="N155-2"><span class="qr-step">13.2 · 欄位與關係</span>Guard 佔 bytes0～1，Application Tag 佔 2～3，Reference Tag 佔 4～7。圖上 MSB 在較低 byte 位置，表示這些多 byte PI 欄位採高位 byte 在前的排列；與一般 NVMe little-endian 欄位不可混用。</p>
<p class="qr-explanation" data-paragraph="N155-3"><span class="qr-step">13.3 · 判讀與例子</span>Reference Tag 值 00000001h 在這個 PI 中排列為 00 00 00 01，不是 01 00 00 00。STS 非 0 時要改看 Storage／Reference 拆分，不能沿用本圖完整 32-bit Reference Tag 假設。</p>
<p class="qr-tags">搜尋詞：16b Guard · Application Tag · Reference Tag · STS 0 · PI endian</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-n128">NVM Command Set 1.3 Figure 128 · ELBAF：Guard 格式與 Storage Tag 位數</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n174">NVM Command Set 1.3 Figure 174 · Write 的 PRACT：host 要提供多少 metadata</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n157" data-figure="N157">
<h2><span class="qr-number">14</span>32-bit Guard PI：16-byte 格式</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 157 · 32b Guard Protection Information Format</p>
<p class="qr-location">§5.3.1.2 · 文件頁 133 · PDF 133</p>
<p class="qr-explanation" data-paragraph="N157-1"><span class="qr-step">14.1 · 用途</span>metadata 同為 16bytes 時，這張圖幫你區分 32-bit 與 64-bit Guard 配置。Guard 寬度改變，後面的欄位位置也會移動。</p>
<p class="qr-explanation" data-paragraph="N157-2"><span class="qr-step">14.2 · 欄位與關係</span>Guard 在 bytes0～3，Application Tag 在 4～5，Storage and Reference Space 在 6～15，共 80bits。這 80bits 如何分成 Storage Tag 與 Reference Tag，另由 ELBAF.STS 決定。</p>
<p class="qr-explanation" data-paragraph="N157-3"><span class="qr-step">14.3 · 判讀與例子</span>STS=16 時，80-bit 區域高 16bits 為 Storage Tag，餘 64bits 為 Reference Tag。若誤套 64-bit Guard 格式，連 Application Tag 的位置都會讀錯。</p>
<p class="qr-tags">搜尋詞：32b Guard · PI layout · Storage and Reference Space</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-n128">NVM Command Set 1.3 Figure 128 · ELBAF：Guard 格式與 Storage Tag 位數</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n159">NVM Command Set 1.3 Figure 159 · 64-bit Guard PI：較大 Guard 與 48-bit 標籤空間</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n159" data-figure="N159">
<h2><span class="qr-number">15</span>64-bit Guard PI：較大 Guard 與 48-bit 標籤空間</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 159 · 64b Guard Protection Information Format</p>
<p class="qr-location">§5.3.1.3 · 文件頁 134 · PDF 134</p>
<p class="qr-explanation" data-paragraph="N159-1"><span class="qr-step">15.1 · 用途</span>此圖用來解析 64-bit Guard 格式，而不是假設所有欄位都變成 64bits。整份 PI 仍是 16bytes。</p>
<p class="qr-explanation" data-paragraph="N159-2"><span class="qr-step">15.2 · 欄位與關係</span>Guard 在 bytes0～7，Application Tag 在 8～9，Storage／Reference 區域在 10～15，共 48bits。各多 byte 欄位按圖中的 MSB／LSB 排列；tag 拆分由 STS 決定。</p>
<p class="qr-explanation" data-paragraph="N159-3"><span class="qr-step">15.3 · 判讀與例子</span>若 STS=0，48bits 全給 Reference Tag；STS=48 則全給 Storage Tag、沒有 Reference Tag。位寬和檢查規則要一起核對，不能把不存在的 Reference Tag 當作值 0。</p>
<p class="qr-tags">搜尋詞：64b Guard · PI layout · Storage Tag · Reference Tag</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-n128">NVM Command Set 1.3 Figure 128 · ELBAF：Guard 格式與 Storage Tag 位數</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n157">NVM Command Set 1.3 Figure 157 · 32-bit Guard PI：16-byte 格式</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n174" data-figure="N174">
<h2><span class="qr-number">16</span>Write 的 PRACT：host 要提供多少 metadata</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 174 · Write Command 16b Guard Protection Information Processing</p>
<p class="qr-location">§5.3.2.1 · 文件頁 143 · PDF 143</p>
<p class="qr-explanation" data-paragraph="N174-1"><span class="qr-step">16.1 · 用途</span>這張四情境圖用來核對 host buffer 與媒體格式的差異，尤其適合排查 PI 啟用後傳輸長度不符。圖的範圍是 16-bit Guard PI。</p>
<p class="qr-explanation" data-paragraph="N174-2"><span class="qr-step">16.2 · 欄位與關係</span>PRACT=0 時，host 傳輸包含 PI 的 metadata。PRACT=1 且 metadata 恰好 8bytes 時，host 不傳這 8bytes，由 controller 產生 PI；metadata 大於 8bytes 時，host 端 metadata 大小維持原值，不能一律減掉 8bytes。</p>
<p class="qr-explanation" data-paragraph="N174-3"><span class="qr-step">16.3 · 判讀與例子</span>4096-byte 資料、8-byte metadata、PRACT=1 時，host 只提供資料；改為 16-byte metadata 時則保留 16-byte metadata 傳輸配置。PRCHK 指定哪些檢查，不能由 PRACT 單獨推論所有檢查都關閉。</p>
<p class="qr-tags">搜尋詞：PRACT · Write PI · MD 8 · MD 16 · 16b Guard</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/io/zh-tw/#figure-n175">NVM Command Set 1.3 Figure 175 · Read 的 PRACT：回主機時保留或移除哪些資料</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n71">NVM Command Set 1.3 Figure 71 · Write CDW12：持久性、PI 與配置提示</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n175" data-figure="N175">
<h2><span class="qr-number">17</span>Read 的 PRACT：回主機時保留或移除哪些資料</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 175 · Read 16b Guard Command Protection Information Processing</p>
<p class="qr-location">§5.3.2.2 · 文件頁 145 · PDF 145</p>
<p class="qr-explanation" data-paragraph="N175-1"><span class="qr-step">17.1 · 用途</span>這張圖沿 NVM→controller→host 方向顯示 Read 的 PI 處理。它補足 Write 圖的反向資料流，適合確認讀回 buffer 是否少算或多算 metadata。</p>
<p class="qr-explanation" data-paragraph="N175-2"><span class="qr-step">17.2 · 欄位與關係</span>PRACT=0 時讀回完整 metadata；PRACT=1 且 metadata 恰好 8bytes 時，PI 不傳回 host。metadata 大於 8bytes 時仍維持原 metadata 大小；不能把「controller 處理 PI」直接等同「host 完全沒有 metadata」。</p>
<p class="qr-explanation" data-paragraph="N175-3"><span class="qr-step">17.3 · 判讀與例子</span>若 metadata=16bytes 而 buffer 只按資料大小配置，即使 PRACT=1 仍可能配置不足。先以本圖決定傳輸形態，再用 namespace 的 metadata 放置方式決定 DPTR 與 MPTR。</p>
<p class="qr-tags">搜尋詞：PRACT · Read PI · metadata transfer · 16b Guard</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/io/zh-tw/#figure-n174">NVM Command Set 1.3 Figure 174 · Write 的 PRACT：host 要提供多少 metadata</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n54">NVM Command Set 1.3 Figure 54 · Read CDW12：範圍、重試與保護要求</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n154">NVM Command Set 1.3 Figure 154 · Separate Metadata：兩個 buffer 依 LBA 配對</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<footer id="source-files"><h2>原始文件</h2><p>頁碼採本次提供的 ratified PDF；Base 的 PDF 頁＝文件頁＋26，另兩份相同。圖號與英文原名保留，可用 PDF 搜尋定位。公開網站不附原始 PDF。</p><ul class="qr-sources"><li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li></ul></footer>
</main></div>
