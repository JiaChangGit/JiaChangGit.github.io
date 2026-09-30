---
layout: "post"
title: "NVMe 圖表速查 02 · 命令格式、資料指標與完成狀態"
date: "2026-09-29 09:00:00 +0800"
categories: ["nvme"]
tags: ["NVMe", "Reference"]
permalink: "/nvme/figure-reference/command/zh-tw/"
nvme_quickref: true
lang: "zh-Hant-TW"
description: "NVMe 原圖用途、欄位與判讀速查，附完整 Spec 位置。"
---

<div class="nvme-quickref">
<nav class="qr-top" aria-label="版本與索引"><a href="#content">跳到內容</a><a href="/nvme/figure-reference/zh-tw/">總索引</a><a href="/nvme/figure-reference/command/en/">English</a><a href="/DOCS/nvme-quick-reference/command.html">繁中 HTML</a></nav>
<main id="content">
<header><p class="qr-eyebrow">反覆查詢 · 欄位判讀 · 原文定位</p><h1>NVMe 圖表速查 02 · 命令格式、資料指標與完成狀態</h1><p class="qr-intro">先用 SQID／CID 對回命令，再解 SCT／SC。資料搬移異常時，分清 PRP 的頁面指標與 SGL 的位址、長度和描述子類型。</p></header>
<aside class="qr-note"><p>每張原圖都有用途、欄位和判讀例子。例子中的數值用於說明，不代表你的裝置設定；原文另有條件時，依該欄位與命令定義判斷。</p><p>用瀏覽器「在頁面中尋找」搜尋欄位、FID、LID、CNS 或 Figure。bit／byte 位置沿用原圖：bit 是位元，byte 是 8 bits，Dword 是 4 bytes；index 是第幾筆，offset 是相對起點的偏移，須看當處使用的單位。</p><p>FID（Feature Identifier）選擇功能；LID（Log Page Identifier）選擇紀錄頁；CNS（Controller or Namespace Structure）選擇 Identify 回傳的資料結構。</p></aside>
<nav class="qr-toc" id="figure-index" aria-label="本冊圖表索引"><h2>本冊圖表</h2><ol>
<li><a href="#figure-b92">Base 2.4 Figure 92 · CDW0：先辨認命令與資料指標格式</a></li>
<li><a href="#figure-b93">Base 2.4 Figure 93 · 64-byte 命令的共同位置</a></li>
<li><a href="#figure-b97">Base 2.4 Figure 97 · CQE：完成結果的外框</a></li>
<li><a href="#figure-b98">Base 2.4 Figure 98 · CQE DW2：對回 SQ 與已消耗的位置</a></li>
<li><a href="#figure-b99">Base 2.4 Figure 99 · CQE DW3：新舊判別、CID 與狀態</a></li>
<li><a href="#figure-b101">Base 2.4 Figure 101 · Status：類別、錯誤碼與重試提示</a></li>
<li><a href="#figure-b102">Base 2.4 Figure 102 · SCT：決定去哪張錯誤碼表</a></li>
<li><a href="#figure-b103">Base 2.4 Figure 103 · 通用錯誤碼：先區分哪類參數問題</a></li>
<li><a href="#figure-b104">Base 2.4 Figure 104 · Admin 命令專屬狀態</a></li>
<li><a href="#figure-b107">Base 2.4 Figure 107 · 媒體與保護檢查錯誤</a></li>
<li><a href="#figure-b110">Base 2.4 Figure 110 · PRP 地址如何分成頁基底與 offset</a></li>
<li><a href="#figure-b111">Base 2.4 Figure 111 · PRP：哪些位置允許頁內 offset</a></li>
<li><a href="#figure-b113">Base 2.4 Figure 113 · PRP List：不連續實體頁的排列</a></li>
<li><a href="#figure-b114">Base 2.4 Figure 114 · SGL 結構錯誤如何對應 status</a></li>
<li><a href="#figure-b116">Base 2.4 Figure 116 · SGL 描述子的 type 與 subtype</a></li>
<li><a href="#figure-b119">Base 2.4 Figure 119 · SGL Data Block：直接描述資料 buffer</a></li>
<li><a href="#figure-b121">Base 2.4 Figure 121 · SGL Segment：指向下一段描述子</a></li>
<li><a href="#figure-b122">Base 2.4 Figure 122 · SGL Last Segment：最後一段仍是一份清單</a></li>
<li><a href="#figure-n18">NVM Command Set 1.3 Figure 18 · NVM 通用狀態補充：地址、容量與原子性</a></li>
<li><a href="#figure-n19">NVM Command Set 1.3 Figure 19 · NVM 命令專屬錯誤與命令清單</a></li>
<li><a href="#figure-n20">NVM Command Set 1.3 Figure 20 · NVM 媒體狀態補充：Compare 與未寫入區塊</a></li>
</ol></nav>
<article class="qr-card" id="figure-b92" data-figure="B92">
<h2><span class="qr-number">01</span>CDW0：先辨認命令與資料指標格式</h2>
<p class="qr-original">Base 2.4 · Figure 92 · Command Dword 0</p>
<p class="qr-location">§4.1.1 · 文件頁 139–140 · PDF 165–166</p>
<p class="qr-explanation" data-paragraph="B92-1"><span class="qr-step">01.1 · 用途</span>解讀一筆 SQE 時，先看 CDW0，確定命令識別、opcode 及後續資料指標的格式。CID 要連同 SQID 才能唯一識別尚未完成的命令。</p>
<p class="qr-explanation" data-paragraph="B92-2"><span class="qr-step">01.2 · 欄位與關係</span>CID 在 bits31:16，PSDT 在 15:14，FUSE 在 9:8，OPC 在 7:0。PSDT=00b 使用 PRP；01b／10b 使用 SGL 但 metadata 指標解讀不同。PCIe Admin 命令使用 PRP。FUSE 區分一般操作與融合操作中的第一／第二筆。</p>
<p class="qr-explanation" data-paragraph="B92-3"><span class="qr-step">01.3 · 判讀與例子</span>同樣的 DPTR bytes，PSDT 不同就可能代表兩個 PRP 指標或一個 SGL 描述子。因此看到一個似乎合理的地址，不足以證明解析正確；先核對 PSDT 和命令所允許的格式。</p>
<p class="qr-tags">搜尋詞：CDW0 · OPC · CID · PSDT · FUSE</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b93">Base 2.4 Figure 93 · 64-byte 命令的共同位置</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b98">Base 2.4 Figure 98 · CQE DW2：對回 SQ 與已消耗的位置</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b93" data-figure="B93">
<h2><span class="qr-number">02</span>64-byte 命令的共同位置</h2>
<p class="qr-original">Base 2.4 · Figure 93 · Common Command Format</p>
<p class="qr-location">§4.1.1 · 文件頁 140–142 · PDF 166–168</p>
<p class="qr-explanation" data-paragraph="B93-1"><span class="qr-step">02.1 · 用途</span>這張表是把原始命令 bytes 對回欄位的總地圖。它告訴你哪些位置共通，哪些位置必須接到個別命令定義。</p>
<p class="qr-explanation" data-paragraph="B93-2"><span class="qr-step">02.2 · 欄位與關係</span>CDW0 在 bytes3:0，NSID 在 7:4，CDW2／3 在 15:8，MPTR 在 23:16，DPTR 在 39:24，CDW10～15 在 63:40。PRP 模式下，DPTR 分為 PRP1 與 PRP2；PRP2 可能保留、指第二頁或指 PRP List，取決於傳輸跨越多少頁邊界。</p>
<p class="qr-explanation" data-paragraph="B93-3"><span class="qr-step">02.3 · 判讀與例子</span>例如 4 KiB 頁、PRP1 頁內 offset=512、傳輸 8192 bytes，需要 3 個資料頁；PRP2 因此指向清單，而不是第二資料頁。NSID=FFFFFFFFh 也不是所有命令都接受的通用廣播值。</p>
<p class="qr-tags">搜尋詞：SQE · NSID · MPTR · DPTR · CDW10 · PRP2</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b92">Base 2.4 Figure 92 · CDW0：先辨認命令與資料指標格式</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b111">Base 2.4 Figure 111 · PRP：哪些位置允許頁內 offset</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b113">Base 2.4 Figure 113 · PRP List：不連續實體頁的排列</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b97" data-figure="B97">
<h2><span class="qr-number">03</span>CQE：完成結果的外框</h2>
<p class="qr-original">Base 2.4 · Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</p>
<p class="qr-location">§4.2.1 · 文件頁 144 · PDF 170</p>
<p class="qr-explanation" data-paragraph="B97-1"><span class="qr-step">03.1 · 用途</span>拿到 completion 原始資料時，先用此配置圖分出回傳值、queue 位置、命令識別與 status。共同格式至少 16 bytes，圖中只描述前 16 bytes。</p>
<p class="qr-explanation" data-paragraph="B97-2"><span class="qr-step">03.2 · 欄位與關係</span>DW0 與 DW1 依命令定義，不能一律當 0 或一般 status；DW2 含 SQID 與 SQHD，DW3 含 STATUS、P 與 CID。P 是 phase tag，用來辨認環形 CQ 中的新項目。</p>
<p class="qr-explanation" data-paragraph="B97-3"><span class="qr-step">03.3 · 判讀與例子</span>Get Features 的 DW0 可能是 Feature 值，Namespace Management 的 DW0 可能是新 NSID。兩者都應先查命令定義；是否成功則由 DW3 的 status 判斷。</p>
<p class="qr-tags">搜尋詞：CQE · DW0 · DW1 · DW2 · DW3</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b98">Base 2.4 Figure 98 · CQE DW2：對回 SQ 與已消耗的位置</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b99">Base 2.4 Figure 99 · CQE DW3：新舊判別、CID 與狀態</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Status：類別、錯誤碼與重試提示</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b98" data-figure="B98">
<h2><span class="qr-number">04</span>CQE DW2：對回 SQ 與已消耗的位置</h2>
<p class="qr-original">Base 2.4 · Figure 98 · Completion Queue Entry: DW 2</p>
<p class="qr-location">§4.2.1 · 文件頁 144 · PDF 170</p>
<p class="qr-explanation" data-paragraph="B98-1"><span class="qr-step">04.1 · 用途</span>多個 SQ 共用同一個 CQ 時，SQID 協助把完成結果對回來源。SQHD 則讓主機知道提交佇列哪些位置已被 controller 消耗。</p>
<p class="qr-explanation" data-paragraph="B98-2"><span class="qr-step">04.2 · 欄位與關係</span>SQID 在 bits31:16，SQHD 在 15:0。SQID 加上 DW3 的 CID 識別命令；SQHD 是建立這筆 CQE 時的 SQ head 快照，不是完成的命令在 SQ 中的 index。</p>
<p class="qr-explanation" data-paragraph="B98-3"><span class="qr-step">04.3 · 判讀與例子</span>SQHD=12 不代表 CID12 完成，也不保證主機讀取時 controller 仍停在 12。命令可以不同順序完成，應分開追蹤 buffer 可重用位置與命令完成狀態。</p>
<p class="qr-tags">搜尋詞：SQID · SQHD · CQE DW2</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b99">Base 2.4 Figure 99 · CQE DW3：新舊判別、CID 與狀態</a><a href="/nvme/figure-reference/init/zh-tw/#figure-p5">PCIe Transport 1.4 Figure 5 · SQ doorbell：告知新的提交位置</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b99" data-figure="B99">
<h2><span class="qr-number">05</span>CQE DW3：新舊判別、CID 與狀態</h2>
<p class="qr-original">Base 2.4 · Figure 99 · Completion Queue Entry: DW 3</p>
<p class="qr-location">§4.2.1 · 文件頁 145 · PDF 171</p>
<p class="qr-explanation" data-paragraph="B99-1"><span class="qr-step">05.1 · 用途</span>主機掃描 CQ 時，這張表把「是否新完成項目」與「哪筆命令、什麼結果」分開。P 不是成功旗標。</p>
<p class="qr-explanation" data-paragraph="B99-2"><span class="qr-step">05.2 · 欄位與關係</span>CID 在 bits15:0，P 在 bit16，STATUS 在 bits31:17。主機按目前 CQ 循環所期待的 phase 判斷新項目；若 CQE 分多次寫入，phase bit 必須在最後一次寫入更新。</p>
<p class="qr-explanation" data-paragraph="B99-3"><span class="qr-step">05.3 · 判讀與例子</span>P 符合目前期待值後，再用 SQID／CID 對命令並解析 status。P=1 本身不代表新項目，因為期待值會隨 CQ 回繞改變。</p>
<p class="qr-tags">搜尋詞：CID · P · Phase Tag · STATUS · CQE DW3</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b98">Base 2.4 Figure 98 · CQE DW2：對回 SQ 與已消耗的位置</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b101">Base 2.4 Figure 101 · Status：類別、錯誤碼與重試提示</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b101" data-figure="B101">
<h2><span class="qr-number">06</span>Status：類別、錯誤碼與重試提示</h2>
<p class="qr-original">Base 2.4 · Figure 101 · Completion Queue Entry: Status Field</p>
<p class="qr-location">§4.2.3 · 文件頁 145–146 · PDF 171–172</p>
<p class="qr-explanation" data-paragraph="B101-1"><span class="qr-step">06.1 · 用途</span>命令有完成結果但不成功時，從這張表拆出狀態欄位，再選正確的錯誤碼表。原圖 bit 位置是相對整個 CQE DW3，不是已移位的 15-bit STATUS。</p>
<p class="qr-explanation" data-paragraph="B101-2"><span class="qr-step">06.2 · 欄位與關係</span>DNR bit31 表示相同命令重送是否預期仍失敗；M bit30 表示 Error Information 有額外資訊；CRD bits29:28 選重試等待時間；SCT bits27:25 為類別，SC bits24:17 為代碼。CRD 只有 DNR=0 且 Host Behavior Support 的 ACRE=1 才適用。</p>
<p class="qr-explanation" data-paragraph="B101-3"><span class="qr-step">06.3 · 判讀與例子</span>DW3=8005002Ah 可拆出 DNR=1、SCT=0、SC=02h、P=1、CID=002Ah。這表示通用 Invalid Field in Command，不能只取 02h 就忽略類別；DNR=0 的情況也不保證重試成功。</p>
<p class="qr-tags">搜尋詞：SCT · SC · DNR · M · CRD · ACRE</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b102">Base 2.4 Figure 102 · SCT：決定去哪張錯誤碼表</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b103">Base 2.4 Figure 103 · 通用錯誤碼：先區分哪類參數問題</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b212">Base 2.4 Figure 212 · Error Information：把錯誤對回命令與欄位</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b102" data-figure="B102">
<h2><span class="qr-number">07</span>SCT：決定去哪張錯誤碼表</h2>
<p class="qr-original">Base 2.4 · Figure 102 · Status Code – Status Code Type Values</p>
<p class="qr-location">§4.2.3 · 文件頁 146 · PDF 172</p>
<p class="qr-explanation" data-paragraph="B102-1"><span class="qr-step">07.1 · 用途</span>這張表是 status 查詢的分流入口。同一個 SC 數值，在不同 SCT 下可能完全不同。</p>
<p class="qr-explanation" data-paragraph="B102-2"><span class="qr-step">07.2 · 欄位與關係</span>SCT=0 是通用命令狀態，1 是命令專屬狀態，2 是媒體與資料完整性，3 是路徑相關，7 是廠商專屬，4～6 保留。表的 Reference 欄帶你到對應 Base 小節；I/O 命令還可能有 command set 補充。</p>
<p class="qr-explanation" data-paragraph="B102-3"><span class="qr-step">07.3 · 判讀與例子</span>SC=80h、SCT=0 在 NVM 代表 LBA Out of Range；SC=80h、SCT=1 則是 Conflicting Attributes。工具若只印 80h，資訊不足以判讀。</p>
<p class="qr-tags">搜尋詞：SCT · Generic · Command Specific · Media · Path Related</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-n18">NVM Command Set 1.3 Figure 18 · NVM 通用狀態補充：地址、容量與原子性</a><a href="/nvme/figure-reference/command/zh-tw/#figure-n19">NVM Command Set 1.3 Figure 19 · NVM 命令專屬錯誤與命令清單</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b107">Base 2.4 Figure 107 · 媒體與保護檢查錯誤</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b103" data-figure="B103">
<h2><span class="qr-number">08</span>通用錯誤碼：先區分哪類參數問題</h2>
<p class="qr-original">Base 2.4 · Figure 103 · Status Code – Generic Command Status Values</p>
<p class="qr-location">§4.2.3.1 · 文件頁 147–150 · PDF 173–176</p>
<p class="qr-explanation" data-paragraph="B103-1"><span class="qr-step">08.1 · 用途</span>SCT=0 時，這張表可查 opcode、欄位、namespace、資料傳輸與命令順序等通用結果。它不是所有 I/O 特有錯誤的完整清單。</p>
<p class="qr-explanation" data-paragraph="B103-2"><span class="qr-step">08.2 · 欄位與關係</span>Value 欄是 SC，Definition 描述觸發情況。常查 00h 成功、01h 非法 opcode、02h 非法欄位、0Bh 非法 namespace 或格式。錯誤名稱相近不代表相同條件；inactive NSID 與 invalid NSID 也不能混為一談。</p>
<p class="qr-explanation" data-paragraph="B103-3"><span class="qr-step">08.3 · 判讀與例子</span>收到 02h 時先看命令的欄位及有效條件，再用 M 和 Error Information 中的 Parameter Error Location 縮小位置。不能把每個 02h 都直接歸因為 NSID 錯誤。</p>
<p class="qr-tags">搜尋詞：generic status · Invalid Field · Invalid Namespace · SC</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/logs/zh-tw/#figure-b212">Base 2.4 Figure 212 · Error Information：把錯誤對回命令與欄位</a><a href="/nvme/figure-reference/command/zh-tw/#figure-n18">NVM Command Set 1.3 Figure 18 · NVM 通用狀態補充：地址、容量與原子性</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b104" data-figure="B104">
<h2><span class="qr-number">09</span>Admin 命令專屬狀態</h2>
<p class="qr-original">Base 2.4 · Figure 104 · Status Code – Command Specific Status Values</p>
<p class="qr-location">§4.2.3.2 · 文件頁 151–152 · PDF 177–178</p>
<p class="qr-explanation" data-paragraph="B104-1"><span class="qr-step">09.1 · 用途</span>SCT=1 且涉及 Admin 操作時，先在這張表找原因，再回到發出命令的章節。部分狀態表示需要後續動作，不宜只分成成功／硬體故障。</p>
<p class="qr-explanation" data-paragraph="B104-2"><span class="qr-step">09.2 · 欄位與關係</span>表以 SC 對應描述，包含 queue ID 或大小錯誤、韌體 slot／image 問題，以及需要 reset 的啟用結果。對照時保留原 opcode，因為命令專屬碼必須放回命令情境。</p>
<p class="qr-explanation" data-paragraph="B104-3"><span class="qr-step">09.3 · 判讀與例子</span>韌體要求 reset 的完成結果，和下載 image 無效是兩種處理方向：前者應確認啟用時點與所需 reset 層級，後者應檢查 image 及提交參數。不要看到非 0 狀態就反覆重送相同更新。</p>
<p class="qr-tags">搜尋詞：command specific · queue error · firmware status · SCT 1</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b187">Base 2.4 Figure 187 · Firmware Commit：放進 slot 與啟用的差別</a><a href="/nvme/figure-reference/command/zh-tw/#figure-n19">NVM Command Set 1.3 Figure 19 · NVM 命令專屬錯誤與命令清單</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b107" data-figure="B107">
<h2><span class="qr-number">10</span>媒體與保護檢查錯誤</h2>
<p class="qr-original">Base 2.4 · Figure 107 · Status Code – Media and Data Integrity Error Values</p>
<p class="qr-location">§4.2.3.3 · 文件頁 154–155 · PDF 180–181</p>
<p class="qr-explanation" data-paragraph="B107-1"><span class="qr-step">10.1 · 用途</span>SCT=2 時，用這張表區分媒體讀寫錯誤與資料保護檢查失敗。保護資訊不符不必然等於 NAND 物理損壞。</p>
<p class="qr-explanation" data-paragraph="B107-2"><span class="qr-step">10.2 · 欄位與關係</span>SC 及描述涵蓋 Write Fault、Unrecovered Read，以及 Guard、Application Tag、Reference Tag 檢查錯誤。先保留失敗種類，再查 namespace 格式、命令的檢查旗標與預期 tag。</p>
<p class="qr-explanation" data-paragraph="B107-3"><span class="qr-step">10.3 · 判讀與例子</span>Reference Tag 失敗時，LBA 起點、PI 類型或 tag 設定不一致都值得核對；若只記成「讀取錯誤」，會失去定位線索。NVM 另補 Compare Failure 及 Deallocated／Unwritten 相關碼。</p>
<p class="qr-tags">搜尋詞：SCT 2 · Guard · Application Tag · Reference Tag · Media Error</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-n20">NVM Command Set 1.3 Figure 20 · NVM 媒體狀態補充：Compare 與未寫入區塊</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n155">NVM Command Set 1.3 Figure 155 · 16-bit Guard PI：8 bytes 的實際配置</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n174">NVM Command Set 1.3 Figure 174 · Write 的 PRACT：host 要提供多少 metadata</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n175">NVM Command Set 1.3 Figure 175 · Read 的 PRACT：回主機時保留或移除哪些資料</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b110" data-figure="B110">
<h2><span class="qr-number">11</span>PRP 地址如何分成頁基底與 offset</h2>
<p class="qr-original">Base 2.4 · Figure 110 · PRP Entry Layout</p>
<p class="qr-location">§4.3.1 · 文件頁 158 · PDF 184</p>
<p class="qr-explanation" data-paragraph="B110-1"><span class="qr-step">11.1 · 用途</span>這張位元圖用來確認 PRP 的地址切割。頁內 offset 是從該頁起點算起的 bytes，不是第幾個 PRP entry。</p>
<p class="qr-explanation" data-paragraph="B110-2"><span class="qr-step">11.2 · 欄位與關係</span>高位是 Page Base Address，低 n+1 位是頁內 offset；分界由 CC.MPS 決定。4 KiB 頁使用低 12bits，8 KiB 頁使用低 13bits，不能在所有配置硬套同一個 FFFh 遮罩。</p>
<p class="qr-explanation" data-paragraph="B110-3"><span class="qr-step">11.3 · 判讀與例子</span>地址 12345000h 在 4 KiB 頁下 offset 為 0；在 8 KiB 頁下 offset 為 1000h。相同地址的 PRP 是否合法，還要看它在命令或清單中的角色。</p>
<p class="qr-tags">搜尋詞：PRP · Page Base Address · offset · CC.MPS</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b111">Base 2.4 Figure 111 · PRP：哪些位置允許頁內 offset</a><a href="/nvme/figure-reference/init/zh-tw/#figure-b41">Base 2.4 Figure 41 · CC：主機實際選了什麼</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b111" data-figure="B111">
<h2><span class="qr-number">12</span>PRP：哪些位置允許頁內 offset</h2>
<p class="qr-original">Base 2.4 · Figure 111 · PRP Entry – Page Base Address and Offset</p>
<p class="qr-location">§4.3.1 · 文件頁 158 · PDF 184</p>
<p class="qr-explanation" data-paragraph="B111-1"><span class="qr-step">12.1 · 用途</span>看懂位址分界後，查這張表與其後段落判斷對齊要求。第一個資料指標、PRP List 指標和清單內資料頁指標，規則不同。</p>
<p class="qr-explanation" data-paragraph="B111-2"><span class="qr-step">12.2 · 欄位與關係</span>PBAO 佔 64bits。一般 PRP offset 至少 Dword 對齊；資料起始 PRP 可依命令允許非 0 offset，清單內資料頁指標則頁對齊。初始 PRP List 指標另須 8-byte 對齊，後續 list page 須頁對齊。</p>
<p class="qr-explanation" data-paragraph="B111-3"><span class="qr-step">12.3 · 判讀與例子</span>4 KiB 頁下，作為第一個資料 PRP 的 200004h 可能合法，作為清單內資料頁指標卻不合頁對齊要求。不能只檢查最低 2bits 就放行所有 PRP 位置。</p>
<p class="qr-tags">搜尋詞：PBAO · PRP1 · PRP2 · alignment</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b110">Base 2.4 Figure 110 · PRP 地址如何分成頁基底與 offset</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b113">Base 2.4 Figure 113 · PRP List：不連續實體頁的排列</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b93">Base 2.4 Figure 93 · 64-byte 命令的共同位置</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b113" data-figure="B113">
<h2><span class="qr-number">13</span>PRP List：不連續實體頁的排列</h2>
<p class="qr-original">Base 2.4 · Figure 113 · PRP List Layout for Physically Non-Contiguous Memory Pages</p>
<p class="qr-location">§4.3.1 · 文件頁 159 · PDF 185</p>
<p class="qr-explanation" data-paragraph="B113-1"><span class="qr-step">13.1 · 用途</span>主機資料 buffer 跨多個不連續實體頁時，這張圖展示 PRP List 如何保存每頁地址。資料邏輯上連續，不代表實體地址必須連續。</p>
<p class="qr-explanation" data-paragraph="B113-2"><span class="qr-step">13.2 · 欄位與關係</span>每個清單項目 8bytes，資料頁地址的 offset 為 0；項目緊密排列，從 entry0 開始。若清單需要下一頁，當頁最後一項改為下一個 list page 的指標，因此不是每一項都代表資料頁。</p>
<p class="qr-explanation" data-paragraph="B113-3"><span class="qr-step">13.3 · 判讀與例子</span>4 KiB 清單頁可容納 512 個 8-byte 項目；需要串接時，最後一項用於串接，這一頁最多剩 511 個資料頁地址。不能把清單 page 地址也算入資料傳輸。</p>
<p class="qr-tags">搜尋詞：PRP List · page chain · non-contiguous</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b93">Base 2.4 Figure 93 · 64-byte 命令的共同位置</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b111">Base 2.4 Figure 111 · PRP：哪些位置允許頁內 offset</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b114" data-figure="B114">
<h2><span class="qr-number">14</span>SGL 結構錯誤如何對應 status</h2>
<p class="qr-original">Base 2.4 · Figure 114 · SGL Validation Error Conditions</p>
<p class="qr-location">§4.3.2 · 文件頁 161 · PDF 187</p>
<p class="qr-explanation" data-paragraph="B114-1"><span class="qr-step">14.1 · 用途</span>SGL 地址看來正確卻被拒絕時，查這張條件對照表。它針對描述子排列與類型的錯誤，不只檢查 buffer 是否夠長。</p>
<p class="qr-explanation" data-paragraph="B114-2"><span class="qr-step">14.2 · 欄位與關係</span>Segment／Last Segment 描述子出現在 segment 中非最後位置，對應 Invalid Number of SGL Descriptors；最後一個 segment 又含串接描述子，對應 Invalid SGL Segment Descriptor；不支援的 type 或 type/subtype 組合則是 SGL Descriptor Type Invalid。</p>
<p class="qr-explanation" data-paragraph="B114-3"><span class="qr-step">14.3 · 判讀與例子</span>若 3 個描述子中第 2 個是 Segment，第 3 個還是 Data Block，錯在串接描述子的位置；把第 3 個資料 buffer 加大不會解決這個結構錯誤。</p>
<p class="qr-tags">搜尋詞：SGL validation · Invalid Number of SGL Descriptors · Invalid SGL Segment Descriptor</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b116">Base 2.4 Figure 116 · SGL 描述子的 type 與 subtype</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b121">Base 2.4 Figure 121 · SGL Segment：指向下一段描述子</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b122">Base 2.4 Figure 122 · SGL Last Segment：最後一段仍是一份清單</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b116" data-figure="B116">
<h2><span class="qr-number">15</span>SGL 描述子的 type 與 subtype</h2>
<p class="qr-original">Base 2.4 · Figure 116 · Generic SGL Descriptor Format</p>
<p class="qr-location">§4.3.2 · 文件頁 161 · PDF 187</p>
<p class="qr-explanation" data-paragraph="B116-1"><span class="qr-step">15.1 · 用途</span>每個 SGL 描述子長 16bytes，先看最後一個 byte，才能決定前 15bytes 如何解讀。不能看見前 8bytes 就一律當使用者資料地址。</p>
<p class="qr-explanation" data-paragraph="B116-2"><span class="qr-step">15.2 · 欄位與關係</span>byte15 為 SGLID，上半 byte bits7:4 是 type，下半 byte bits3:0 是 subtype；bytes14:0 依類型定義。常見 Data Block、Segment、Last Segment 的 type 分別為 0、2、3。</p>
<p class="qr-explanation" data-paragraph="B116-3"><span class="qr-step">15.3 · 判讀與例子</span>SGLID=30h 表示 type3、subtype0，地址指向最後一段描述子清單，而不是直接指資料。支援哪些類型仍要查 Identify 及 PCIe 適用條件。</p>
<p class="qr-tags">搜尋詞：SGLID · SGLDT · SGLDST · descriptor</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b119">Base 2.4 Figure 119 · SGL Data Block：直接描述資料 buffer</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b121">Base 2.4 Figure 121 · SGL Segment：指向下一段描述子</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b122">Base 2.4 Figure 122 · SGL Last Segment：最後一段仍是一份清單</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify Controller：能力與限制的主要入口</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b119" data-figure="B119">
<h2><span class="qr-number">16</span>SGL Data Block：直接描述資料 buffer</h2>
<p class="qr-original">Base 2.4 · Figure 119 · SGL Data Block descriptor</p>
<p class="qr-location">§4.3.2 · 文件頁 162–163 · PDF 188–189</p>
<p class="qr-explanation" data-paragraph="B119-1"><span class="qr-step">16.1 · 用途</span>這張表用來解讀真正的資料範圍。以本系列的 PCIe memory address 用法，ADDR 是 buffer 起點，LEN 是資料長度。</p>
<p class="qr-explanation" data-paragraph="B119-2"><span class="qr-step">16.2 · 欄位與關係</span>ADDR 在 bytes7:0，LEN 在 11:8，12～14 保留，byte15 的 type 為 0。LEN 直接以 bytes 計，0 表示不傳資料，仍是有效描述子；對齊與粒度須配合 Identify 的 SGLS。</p>
<p class="qr-explanation" data-paragraph="B119-3"><span class="qr-step">16.3 · 判讀與例子</span>LEN=4096 是 4096 bytes，不能套用 NLB 的加 1 規則。若 controller 要求 4-byte 粒度，ADDR 及 LEN 都要符合，不能只把地址對齊而保留 4097-byte 長度。</p>
<p class="qr-tags">搜尋詞：SGL Data Block · ADDR · LEN · SGLS</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b116">Base 2.4 Figure 116 · SGL 描述子的 type 與 subtype</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify Controller：能力與限制的主要入口</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b121" data-figure="B121">
<h2><span class="qr-number">17</span>SGL Segment：指向下一段描述子</h2>
<p class="qr-original">Base 2.4 · Figure 121 · SGL Segment descriptor</p>
<p class="qr-location">§4.3.2 · 文件頁 163 · PDF 189</p>
<p class="qr-explanation" data-paragraph="B121-1"><span class="qr-step">17.1 · 用途</span>當單一描述子不能描述所有資料時，Segment 描述子把讀取者帶到下一段 SGL。它的長度是描述子清單大小，不是資料 buffer 大小。</p>
<p class="qr-explanation" data-paragraph="B121-2"><span class="qr-step">17.2 · 欄位與關係</span>ADDR bytes7:0 指向下一段，LEN bytes11:8 必須非 0 且是 16 的倍數，byte15 的 type 為 2。這種串接描述子必須位於所屬 segment 的最後。</p>
<p class="qr-explanation" data-paragraph="B121-3"><span class="qr-step">17.3 · 判讀與例子</span>LEN=48 表示下一段有 3 個 16-byte 描述子，不能推論只傳 48bytes 使用者資料；實際資料量要由 Data Block 等資料描述子計算。</p>
<p class="qr-tags">搜尋詞：SGL Segment · type 2 · LEN · ADDR</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b114">Base 2.4 Figure 114 · SGL 結構錯誤如何對應 status</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b119">Base 2.4 Figure 119 · SGL Data Block：直接描述資料 buffer</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b122">Base 2.4 Figure 122 · SGL Last Segment：最後一段仍是一份清單</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b122" data-figure="B122">
<h2><span class="qr-number">18</span>SGL Last Segment：最後一段仍是一份清單</h2>
<p class="qr-original">Base 2.4 · Figure 122 · SGL Last Segment descriptor</p>
<p class="qr-location">§4.3.2 · 文件頁 164 · PDF 190</p>
<p class="qr-explanation" data-paragraph="B122-1"><span class="qr-step">18.1 · 用途</span>這張表標示接下來指向的 segment 已是最後一段。Last 不表示這個描述子直接指向最後一塊使用者資料。</p>
<p class="qr-explanation" data-paragraph="B122-2"><span class="qr-step">18.2 · 欄位與關係</span>ADDR bytes7:0 及 LEN bytes11:8 描述下一段，也是最後一段的描述子陣列；LEN 非 0 且是 16 的倍數。type=3；被指向的最後 segment 不能再放 Segment 或 Last Segment 串接描述子。</p>
<p class="qr-explanation" data-paragraph="B122-3"><span class="qr-step">18.3 · 判讀與例子</span>LEN=32 的 Last Segment 可指向兩個 Data Block 描述子。若第二個又是 Segment，就違反最後 segment 的結構限制，應回查 Figure114。</p>
<p class="qr-tags">搜尋詞：SGL Last Segment · type 3 · last segment</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b114">Base 2.4 Figure 114 · SGL 結構錯誤如何對應 status</a><a href="/nvme/figure-reference/command/zh-tw/#figure-b121">Base 2.4 Figure 121 · SGL Segment：指向下一段描述子</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n18" data-figure="N18">
<h2><span class="qr-number">19</span>NVM 通用狀態補充：地址、容量與原子性</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 18 · Status Code – Generic Command Status Values</p>
<p class="qr-location">§3.1.2 · 文件頁 25 · PDF 25</p>
<p class="qr-explanation" data-paragraph="N18-1"><span class="qr-step">19.1 · 用途</span>Base 通用表找不到 NVM 特有原因時，接著查這張補充表，SCT 仍然是 0。這不是新的 status 編碼格式。</p>
<p class="qr-explanation" data-paragraph="N18-2"><span class="qr-step">19.2 · 欄位與關係</span>SC14h 為超過 atomic write unit，1Eh 為 SGL 地址或長度粒度錯誤，25h 為 Invalid Key Tag，80h 為 LBA 超出 namespace 大小，81h 為配置使用量超過 namespace 容量。</p>
<p class="qr-explanation" data-paragraph="N18-3"><span class="qr-step">19.3 · 判讀與例子</span>80h 查 SLBA、NLB 與 NSZE；81h 查 NUSE、NCAP 及配置情境。兩者都與容量相關，但「位址越界」和「使用量超過可配置容量」不應使用同一個判斷式。</p>
<p class="qr-tags">搜尋詞：SCT 0 · LBA Out of Range · Capacity Exceeded · Atomic Write Unit Exceeded</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-n123">NVM Command Set 1.3 Figure 123 · NVM Namespace：容量、格式、原子性與建議粒度</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n4">NVM Command Set 1.3 Figure 4 · Single Atomicity：單位、條件與邊界的關係</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n19" data-figure="N19">
<h2><span class="qr-number">20</span>NVM 命令專屬錯誤與命令清單</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 19 · Status Code – Command Specific Status Values</p>
<p class="qr-location">§3.1.2 · 文件頁 25 · PDF 25</p>
<p class="qr-explanation" data-paragraph="N19-1"><span class="qr-step">20.1 · 用途</span>收到 NVM 命令的 SCT=1 時，這張表除了錯誤名稱，也直接列出哪些命令可能回它。適合檢查工具是否套錯 command set。</p>
<p class="qr-explanation" data-paragraph="N19-2"><span class="qr-step">20.2 · 欄位與關係</span>80h 為 Conflicting Attributes，81h 為 Invalid Protection Information，82h 為 Attempted Write to Read Only Range；Copy 還有 83h 大小限制、85h 格式不相容、86h 無法 fast copy、87h 重疊範圍與 89h 資源不足。</p>
<p class="qr-explanation" data-paragraph="N19-3"><span class="qr-step">20.3 · 判讀與例子</span>SC81h 在這裡是 PI 設定無效，不等於 SCT2 的 Guard Check Error；前者先檢查要求的保護參數是否成立，後者則檢查資料與保護值是否吻合。</p>
<p class="qr-tags">搜尋詞：SCT 1 · Conflicting Attributes · Invalid Protection Information · Copy errors</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b107">Base 2.4 Figure 107 · 媒體與保護檢查錯誤</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n39">NVM Command Set 1.3 Figure 39 · Copy 描述子：格式決定 namespace 與 PI 配置</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n20" data-figure="N20">
<h2><span class="qr-number">21</span>NVM 媒體狀態補充：Compare 與未寫入區塊</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 20 · Status Code – Media and Data Integrity Error Values</p>
<p class="qr-location">§3.1.2 · 文件頁 26 · PDF 26</p>
<p class="qr-explanation" data-paragraph="N20-1"><span class="qr-step">21.1 · 用途</span>此表補上 NVM 命令對資料內容或已釋放區塊的失敗原因。它能避免把 Compare 不一致一律記成媒體不可讀。</p>
<p class="qr-explanation" data-paragraph="N20-2"><span class="qr-step">21.2 · 欄位與關係</span>SC85h 表示 Compare Failure；87h 表示 Copy、Read 或 Verify 嘗試使用 deallocated 或 unwritten 的 LBA 範圍而失敗。解讀 87h 時，還應核對 namespace 行為與 Deallocated or Unwritten Logical Block Error 相關設定。</p>
<p class="qr-explanation" data-paragraph="N20-3"><span class="qr-step">21.3 · 判讀與例子</span>Compare 回 85h 表示比較不相符，不是該命令一定遇到 CRC 失敗。Read 回 87h 也不能直接推論實體媒體損壞，先確認這段 LBA 是否被 deallocate 或尚未寫入。</p>
<p class="qr-tags">搜尋詞：SCT 2 · Compare Failure · Deallocated or Unwritten Logical Block · DULBE</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/command/zh-tw/#figure-b107">Base 2.4 Figure 107 · 媒體與保護檢查錯誤</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n47">NVM Command Set 1.3 Figure 47 · Dataset Management：每段 LBA 範圍如何排列</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<footer id="source-files"><h2>原始文件</h2><p>頁碼採本次提供的 ratified PDF；Base 的 PDF 頁＝文件頁＋26，另兩份相同。圖號與英文原名保留，可用 PDF 搜尋定位。公開網站不附原始 PDF。</p><ul class="qr-sources"><li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li></ul></footer>
</main></div>
