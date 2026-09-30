---
layout: "post"
title: "NVMe 圖表速查 03 · Identify、Namespace 與資料格式"
date: "2026-09-29 09:00:00 +0800"
categories: ["nvme"]
tags: ["NVMe", "Reference"]
permalink: "/nvme/figure-reference/identify/zh-tw/"
nvme_quickref: true
lang: "zh-Hant-TW"
description: "NVMe 原圖用途、欄位與判讀速查，附完整 Spec 位置。"
---

<div class="nvme-quickref">
<nav class="qr-top" aria-label="版本與索引"><a href="#content">跳到內容</a><a href="/nvme/figure-reference/zh-tw/">總索引</a><a href="/nvme/figure-reference/identify/en/">English</a><a href="/DOCS/nvme-quick-reference/identify.html">繁中 HTML</a></nav>
<main id="content">
<header><p class="qr-eyebrow">反覆查詢 · 欄位判讀 · 原文定位</p><h1>NVMe 圖表速查 03 · Identify、Namespace 與資料格式</h1><p class="qr-intro">CNS 決定回傳哪一種 Identify 結構；controller 能力、namespace 格式和選定格式的大小要分開查，再組合成可用設定。</p></header>
<aside class="qr-note"><p>每張原圖都有用途、欄位和判讀例子。例子中的數值用於說明，不代表你的裝置設定；原文另有條件時，依該欄位與命令定義判斷。</p><p>用瀏覽器「在頁面中尋找」搜尋欄位、FID、LID、CNS 或 Figure。bit／byte 位置沿用原圖：bit 是位元，byte 是 8 bits，Dword 是 4 bytes；index 是第幾筆，offset 是相對起點的偏移，須看當處使用的單位。</p><p>FID（Feature Identifier）選擇功能；LID（Log Page Identifier）選擇紀錄頁；CNS（Controller or Namespace Structure）選擇 Identify 回傳的資料結構。</p></aside>
<nav class="qr-toc" id="figure-index" aria-label="本冊圖表索引"><h2>本冊圖表</h2><ol>
<li><a href="#figure-b333">Base 2.4 Figure 333 · Identify CDW10：選資料結構，不是選欄位</a></li>
<li><a href="#figure-b336">Base 2.4 Figure 336 · CNS 總表：查結構及有效參數</a></li>
<li><a href="#figure-b338">Base 2.4 Figure 338 · Identify Controller：能力與限制的主要入口</a></li>
<li><a href="#figure-b342">Base 2.4 Figure 342 · Namespace 識別描述子：不要把 NSID 當永久身分</a></li>
<li><a href="#figure-b346">Base 2.4 Figure 346 · Namespace 共通狀態：可用、受保護與儲存歸屬</a></li>
<li><a href="#figure-n123">NVM Command Set 1.3 Figure 123 · NVM Namespace：容量、格式、原子性與建議粒度</a></li>
<li><a href="#figure-n125">NVM Command Set 1.3 Figure 125 · LBAF：資料大小、metadata 大小與相對效能</a></li>
<li><a href="#figure-n127">NVM Command Set 1.3 Figure 127 · NVM 專屬 Namespace：延伸 PI 與格式能力</a></li>
<li><a href="#figure-n128">NVM Command Set 1.3 Figure 128 · ELBAF：Guard 格式與 Storage Tag 位數</a></li>
<li><a href="#figure-n129">NVM Command Set 1.3 Figure 129 · NVM 專屬 Controller：命令大小限制及其有效條件</a></li>
</ol></nav>
<article class="qr-card" id="figure-b333" data-figure="B333">
<h2><span class="qr-number">01</span>Identify CDW10：選資料結構，不是選欄位</h2>
<p class="qr-original">Base 2.4 · Figure 333 · Identify – Command Dword 10</p>
<p class="qr-location">§5.2.14 · 文件頁 337 · PDF 363</p>
<p class="qr-explanation" data-paragraph="B333-1"><span class="qr-step">01.1 · 用途</span>當 Identify 資料被解成不合理的容量或能力時，先回查命令選了哪種結構。不同 CNS 可能回傳同樣大小的 buffer，但各 byte 意義不同。</p>
<p class="qr-explanation" data-paragraph="B333-2"><span class="qr-step">01.2 · 欄位與關係</span>CNS bits7:0 選回傳結構；CNTID bits31:16 只用於部分操作；bits15:8 保留。不使用 CNTID 的操作，主機應依規定清 0，不能把它當任意 controller selector。</p>
<p class="qr-explanation" data-paragraph="B333-3"><span class="qr-step">01.3 · 判讀與例子</span>CNS=01h 讀處理此命令的 controller 資訊；CNS=00h 讀 NVM namespace 資訊。若用 01h 的 byte offset 去解析 00h，即使 buffer 長度正確，結論仍可能完全錯誤。</p>
<p class="qr-tags">搜尋詞：Identify · CNS · CNTID · CNS 01h · CNS 00h</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-b336">Base 2.4 Figure 336 · CNS 總表：查結構及有效參數</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify Controller：能力與限制的主要入口</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-n123">NVM Command Set 1.3 Figure 123 · NVM Namespace：容量、格式、原子性與建議粒度</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b336" data-figure="B336">
<h2><span class="qr-number">02</span>CNS 總表：查結構及有效參數</h2>
<p class="qr-original">Base 2.4 · Figure 336 · Identify – CNS Values</p>
<p class="qr-location">§5.2.14 · 文件頁 338–339 · PDF 364–365</p>
<p class="qr-explanation" data-paragraph="B336-1"><span class="qr-step">02.1 · 用途</span>不知道應送哪個 Identify 操作時，從這張表按查詢對象選 CNS。每列同時列出 NSID、CNTID、CSI 是否使用，不能只抄 CNS 數字。</p>
<p class="qr-explanation" data-paragraph="B336-2"><span class="qr-step">02.2 · 欄位與關係</span>常用 01h 為 controller、02h 為 active NSID list、03h 為 namespace 識別描述子；05h／06h 是 command-set-specific namespace／controller，08h 是 command-set-independent namespace。10h 查 allocated NSID list；16h 粒度、17h UUID list 等列也可由此找到來源。</p>
<p class="qr-explanation" data-paragraph="B336-3"><span class="qr-step">02.3 · 判讀與例子</span>active list 與 allocated list 可能不同：已建立但未附加的 namespace，不一定在此 controller 的 active list。查不到時先確認選了哪份清單，而不是直接判定 namespace 不存在。</p>
<p class="qr-tags">搜尋詞：CNS · NSID · CNTID · CSI · Identify list</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-b333">Base 2.4 Figure 333 · Identify CDW10：選資料結構，不是選欄位</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-b342">Base 2.4 Figure 342 · Namespace 識別描述子：不要把 NSID 當永久身分</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-b346">Base 2.4 Figure 346 · Namespace 共通狀態：可用、受保護與儲存歸屬</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b338" data-figure="B338">
<h2><span class="qr-number">03</span>Identify Controller：能力與限制的主要入口</h2>
<p class="qr-original">Base 2.4 · Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</p>
<p class="qr-location">§5.2.14.2.1 · 文件頁 340–382 · PDF 366–408</p>
<p class="qr-explanation" data-paragraph="B338-1"><span class="qr-step">03.1 · 用途</span>這張跨 43 頁的大表是 controller 能力、限制及識別資訊的主要來源。速查時先決定要確認哪一類問題，再用下方欄位頁碼前往；不要從第一頁一路掃到最後。</p>
<p class="qr-explanation" data-paragraph="B338-2"><span class="qr-step">03.2 · 欄位與關係</span>傳輸大小查 MDTS，Admin 命令支援查 OACS，I/O 能力查 ONCS，log 支援與長度查 LPA／ELPE，韌體查 FRMW，清除查 SANICAP。queue entry 大小查 SQES／CQES，資料指標查 SGLS；NPSS 與 Power State Descriptors 則一起解讀電源狀態。</p>
<p class="qr-explanation" data-paragraph="B338-3"><span class="qr-step">03.3 · 判讀與例子</span>MDTS 非 0 時，以 CAP.MPSMIN 定義的最小頁大小乘 2^MDTS；例如最小頁 4 KiB、MDTS=5 得到 128 KiB。MDTS=0 表示此欄不限制，不代表其他命令或 namespace 限制都消失。欄位的 O／M／R、controller 類型及腳註也屬有效條件。</p>
<h3>大表內的欄位位置</h3>
<div class="qr-table"><table class=""><thead><tr><th scope="col">欄位</th><th scope="col">查詢內容</th><th scope="col">PDF 頁</th></tr></thead><tbody><tr><td>MDTS</td><td>傳輸大小上限</td><td>368</td></tr><tr><td>OACS</td><td>Admin 命令支援</td><td>378–380</td></tr><tr><td>FRMW</td><td>韌體槽位與更新能力</td><td>380–381</td></tr><tr><td>LPA</td><td>Log page 能力</td><td>381–382</td></tr><tr><td>ELPE / NPSS</td><td>錯誤項目上限／電源狀態數</td><td>382</td></tr><tr><td>SANICAP</td><td>Sanitize 能力</td><td>387–388</td></tr><tr><td>SQES / CQES</td><td>佇列項目大小</td><td>396</td></tr><tr><td>ONCS</td><td>I/O 命令與功能支援</td><td>397–399</td></tr><tr><td>VWC / AWUN / AWUPF</td><td>快取與原子性欄位</td><td>400</td></tr><tr><td>SGLS</td><td>SGL 類型與對齊</td><td>403–404</td></tr></tbody></table></div>
<p class="qr-tags">搜尋詞：Identify Controller · MDTS · OACS · ONCS · LPA · ELPE · FRMW · SANICAP · SQES · CQES · SGLS · NPSS</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/init/zh-tw/#figure-b36">Base 2.4 Figure 36 · CAP：設定前先查硬體能力</a><a href="/nvme/figure-reference/features/zh-tw/#figure-b340">Base 2.4 Figure 340 · Power State Descriptor：功耗、延遲與可執行 I/O</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b217">Base 2.4 Figure 217 · Command Effects：支援與執行影響</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-n129">NVM Command Set 1.3 Figure 129 · NVM 專屬 Controller：命令大小限制及其有效條件</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b342" data-figure="B342">
<h2><span class="qr-number">04</span>Namespace 識別描述子：不要把 NSID 當永久身分</h2>
<p class="qr-original">Base 2.4 · Figure 342 · Identify – Namespace Identification Descriptor</p>
<p class="qr-location">§5.2.14.2.3 · 文件頁 388 · PDF 414</p>
<p class="qr-explanation" data-paragraph="B342-1"><span class="qr-step">04.1 · 用途</span>要辨認兩次查詢或不同 controller 看到的 namespace 是否為同一物件，查這張識別描述子表。命令中的 NSID 是存取用的識別值，不能代替所有長期識別資訊。</p>
<p class="qr-explanation" data-paragraph="B342-2"><span class="qr-step">04.2 · 欄位與關係</span>NIDT byte0 選類型，NIDL byte1 給 NID 長度，bytes3:2 保留，NID 從 byte4 開始。類型 1／2／3／4 分別是 8-byte EUI64、16-byte NGUID、16-byte UUID、1-byte CSI。每筆總長 NIDL+4；NIDL=0 表示清單結束。</p>
<p class="qr-explanation" data-paragraph="B342-3"><span class="qr-step">04.3 · 判讀與例子</span>NIDL=16 的一筆佔 20bytes，下一筆從原起點+20 開始，不是+16。CSI 描述命令集，不能因為也放在 NID 位置就當成 globally unique identifier。</p>
<p class="qr-tags">搜尋詞：NIDT · NIDL · NID · EUI64 · NGUID · UUID · CSI</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-b336">Base 2.4 Figure 336 · CNS 總表：查結構及有效參數</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-b346" data-figure="B346">
<h2><span class="qr-number">05</span>Namespace 共通狀態：可用、受保護與儲存歸屬</h2>
<p class="qr-original">Base 2.4 · Figure 346 · Identify – I/O Command Set Independent Identify Namespace Data Structure</p>
<p class="qr-location">§5.2.14.2.8 · 文件頁 391–394 · PDF 417–420</p>
<p class="qr-explanation" data-paragraph="B346-1"><span class="qr-step">05.1 · 用途</span>查 namespace 是否 ready、是否受寫入保護、屬於哪個資源群組時，使用這份與 I/O command set 無關的結構。它與 NVM CNS00h 的 byte 配置不同。</p>
<p class="qr-explanation" data-paragraph="B346-2"><span class="qr-step">05.2 · 欄位與關係</span>常查 NSFEAT byte0、NMIC byte1、RESCAP byte2、FPI byte3；ANAGRPID 在 bytes7:4，NSATTR 在 byte8，後面還有 NVMSETID、ENDGID 與 NSTAT。FPI 表示剩餘 Format 百分比，NSATTR.CWP 表示目前受寫入保護，NSTAT.NRDY 表示 namespace 是否 ready。</p>
<p class="qr-explanation" data-paragraph="B346-3"><span class="qr-step">05.3 · 判讀與例子</span>controller 的 CSTS.RDY=1 而 namespace 的 NRDY=0，可以是 media-independent ready 流程中的不同層級狀態，不應立刻視為互相矛盾。ENDGID 則用來接到對應 Endurance Group 的健康 log。</p>
<p class="qr-tags">搜尋詞：CNS 08h · NSTAT · NRDY · NSATTR · FPI · ENDGID · NVMSETID · ANAGRPID</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/init/zh-tw/#figure-b42">Base 2.4 Figure 42 · CSTS：啟用與關機進度回報</a><a href="/nvme/figure-reference/logs/zh-tw/#figure-b225">Base 2.4 Figure 225 · Endurance Group：逐組健康與容量</a><a href="/nvme/figure-reference/maintenance/zh-tw/#figure-b541">Base 2.4 Figure 541 · Namespace Write Protection：目前保護狀態</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n123" data-figure="N123">
<h2><span class="qr-number">06</span>NVM Namespace：容量、格式、原子性與建議粒度</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</p>
<p class="qr-location">§4.1.5.1 · 文件頁 85–93 · PDF 85–93</p>
<p class="qr-explanation" data-paragraph="N123-1"><span class="qr-step">06.1 · 用途</span>容量數字、LBA 格式或對齊行為有疑問時，這張表是 NVM namespace 的主要入口。先分清目前格式、支援格式清單與建議效能參數。</p>
<p class="qr-explanation" data-paragraph="N123-2"><span class="qr-step">06.2 · 欄位與關係</span>NSZE bytes7:0 是可定址 blocks 總數，NCAP15:8 是最多可配置量，NUSE23:16 是目前配置量。FLBAS byte26 選格式，DPS byte29 選 PI 設定，DLFEAT byte33 描述 deallocate 後行為；後續 NAWUN／NAWUPF 與 boundary 欄位補原子性，LBAF 清單提供各格式大小。</p>
<p class="qr-explanation" data-paragraph="N123-3"><span class="qr-step">06.3 · 判讀與例子</span>NSZE=1000 表示 LBA0～999；若所選 LBADS=12，資料容量是 1000×4096=4,096,000 bytes。FLBAS=12h 不是 18-byte 格式，而是 format index2 加 metadata 傳輸設定；大小要再讀該 LBAF。</p>
<h3>大表內的欄位位置</h3>
<div class="qr-table"><table class=""><thead><tr><th scope="col">欄位</th><th scope="col">查詢內容</th><th scope="col">PDF 頁</th></tr></thead><tbody><tr><td>NSZE / NCAP / NUSE / NSFEAT</td><td>容量與功能條件</td><td>85–86</td></tr><tr><td>FLBAS / MC / DPC / DPS</td><td>格式與保護設定</td><td>86–87</td></tr><tr><td>DLFEAT / NAWUN / NAWUPF</td><td>Deallocate 行為與原子單位</td><td>88–89</td></tr><tr><td>NABSN / NABO / NABSPF</td><td>原子性邊界</td><td>89</td></tr><tr><td>NPWG / NPWA / NPDG / NPDA</td><td>效能建議粒度與對齊</td><td>90</td></tr><tr><td>LBAF</td><td>格式清單的位置與數量</td><td>93</td></tr></tbody></table></div>
<p class="qr-tags">搜尋詞：CNS 00h · NSZE · NCAP · NUSE · FLBAS · DPS · DLFEAT · LBAF · NAWUN · NABSN</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-n125">NVM Command Set 1.3 Figure 125 · LBAF：資料大小、metadata 大小與相對效能</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n4">NVM Command Set 1.3 Figure 4 · Single Atomicity：單位、條件與邊界的關係</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n8">NVM Command Set 1.3 Figure 8 · Atomic Boundary：同樣大小，不同起點會有不同結果</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-n127">NVM Command Set 1.3 Figure 127 · NVM 專屬 Namespace：延伸 PI 與格式能力</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n125" data-figure="N125">
<h2><span class="qr-number">07</span>LBAF：資料大小、metadata 大小與相對效能</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 125 · LBA Format Data Structure, NVM Command Set Specific</p>
<p class="qr-location">§4.1.5.1 · 文件頁 94 · PDF 94</p>
<p class="qr-explanation" data-paragraph="N125-1"><span class="qr-step">07.1 · 用途</span>FLBAS 已選出 format index 後，到這張表解該格式的 4-byte 描述子。它回答每個 logical block 的資料和 metadata 各有多大。</p>
<p class="qr-explanation" data-paragraph="N125-2"><span class="qr-step">07.2 · 欄位與關係</span>MS bits15:0 直接以 bytes 表示 metadata；LBADS bits23:16 是資料 bytes 的 2 次方指數，0 表示該格式目前不可用；RP bits25:24 是指定測試情境下的相對效能等級，不是 IOPS 數值。</p>
<p class="qr-explanation" data-paragraph="N125-3"><span class="qr-step">07.3 · 判讀與例子</span>LBADS=12、MS=8 代表 4096-byte 資料加 8-byte metadata。若採 extended LBA，傳輸排列每 block 共 4104 bytes；LBADS 不包含這 8bytes，也不能把 RP=0 當作所有工作負載一定最快。</p>
<p class="qr-tags">搜尋詞：LBAF · LBADS · MS · RP</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-n123">NVM Command Set 1.3 Figure 123 · NVM Namespace：容量、格式、原子性與建議粒度</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n153">NVM Command Set 1.3 Figure 153 · Extended LBA：資料與 metadata 交錯</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n154">NVM Command Set 1.3 Figure 154 · Separate Metadata：兩個 buffer 依 LBA 配對</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n127" data-figure="N127">
<h2><span class="qr-number">08</span>NVM 專屬 Namespace：延伸 PI 與格式能力</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 127 · NVM Command Set I/O Command Set Specific Identify Namespace Data Structure</p>
<p class="qr-location">§4.1.5.3 · 文件頁 97–101 · PDF 97–101</p>
<p class="qr-explanation" data-paragraph="N127-1"><span class="qr-step">08.1 · 用途</span>需要解 32／64-bit Guard、Storage Tag 或延伸格式時，CNS00h 不夠，還要查這份 CNS05h、CSI00h 資料。它補充格式能力，不取代目前 namespace 的 FLBAS／DPS。</p>
<p class="qr-explanation" data-paragraph="N127-2"><span class="qr-step">08.2 · 欄位與關係</span>LBSTM 提供 Storage Tag mask，PIC 列保護格式能力；ELBAF 陣列對應各 format index，描述 Guard 格式與 Storage Tag 寬度。相關 mask 有效性還受保護資訊是否啟用，以及 PIC 和 masking-level 能力限制。</p>
<p class="qr-explanation" data-paragraph="N127-3"><span class="qr-step">08.3 · 判讀與例子</span>同一個 format index 應在 LBAF 與 ELBAF 配對：前者提供資料／metadata bytes，後者提供 PI 內部格式。只看到 metadata 有 16bytes，無法直接判定 Guard 一定是 64bits。</p>
<p class="qr-tags">搜尋詞：CNS 05h · CSI 00h · LBSTM · PIC · ELBAF · Storage Tag</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-n128">NVM Command Set 1.3 Figure 128 · ELBAF：Guard 格式與 Storage Tag 位數</a><a href="/nvme/figure-reference/identify/zh-tw/#figure-n125">NVM Command Set 1.3 Figure 125 · LBAF：資料大小、metadata 大小與相對效能</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n159">NVM Command Set 1.3 Figure 159 · 64-bit Guard PI：較大 Guard 與 48-bit 標籤空間</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n128" data-figure="N128">
<h2><span class="qr-number">09</span>ELBAF：Guard 格式與 Storage Tag 位數</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 128 · Extended LBA Format Data Structure, NVM Command Set Specific</p>
<p class="qr-location">§4.1.5.3 · 文件頁 101–102 · PDF 101–102</p>
<p class="qr-explanation" data-paragraph="N128-1"><span class="qr-step">09.1 · 用途</span>查 PI 資料為何解析錯位時，用這張表確定 Guard 格式以及 Storage／Reference 區域如何切割。STS 在這裡是 Storage Tag Size，不能當成 status。</p>
<p class="qr-explanation" data-paragraph="N128-2"><span class="qr-step">09.2 · 欄位與關係</span>STS bits6:0 指定 Storage Tag 位數；PIF bits8:7 選 16／32／64-bit Guard 或 qualified 格式；只有 PIF=11b 且相關能力成立時，才使用 QPIF bits12:9。PI 未啟用時，不能依這些欄位推論實際傳輸含有 PI。</p>
<p class="qr-explanation" data-paragraph="N128-3"><span class="qr-step">09.3 · 判讀與例子</span>PIF=10b、STS=16 表示 64-bit Guard 格式，其中 48-bit Storage／Reference 區的高 16bits 給 Storage Tag，剩 32bits 給 Reference Tag。16、32、64-bit Guard 允許的 STS 範圍不同，不能任意套同一個遮罩。</p>
<p class="qr-tags">搜尋詞：ELBAF · PIF · QPIF · STS · QPIFS</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-n127">NVM Command Set 1.3 Figure 127 · NVM 專屬 Namespace：延伸 PI 與格式能力</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n155">NVM Command Set 1.3 Figure 155 · 16-bit Guard PI：8 bytes 的實際配置</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n157">NVM Command Set 1.3 Figure 157 · 32-bit Guard PI：16-byte 格式</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n159">NVM Command Set 1.3 Figure 159 · 64-bit Guard PI：較大 Guard 與 48-bit 標籤空間</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<article class="qr-card" id="figure-n129" data-figure="N129">
<h2><span class="qr-number">10</span>NVM 專屬 Controller：命令大小限制及其有效條件</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 129 · I/O Command Set Specific Identify Controller Data Structure for the NVM Command Set</p>
<p class="qr-location">§4.1.5.4 · 文件頁 103–106 · PDF 103–106</p>
<p class="qr-explanation" data-paragraph="N129-1"><span class="qr-step">10.1 · 用途</span>Verify、Write Zeroes 或 Dataset Management 因大小被拒絕時，查這份 CNS06h、CSI00h 結構。Base 的 MDTS 不是每個命令唯一的大小限制。</p>
<p class="qr-explanation" data-paragraph="N129-2"><span class="qr-step">10.2 · 欄位與關係</span>VSL／WZSL／WUSL 是以最小記憶體頁為基礎的指數式大小；DMRL 是 range 數，DMRSL 是單一 range 的 blocks，DMSL 是合計 blocks。ONCS 內各命令的 support-variant bits 會改變欄位是強制上限還是建議值，也會改變 0 的含義。</p>
<p class="qr-explanation" data-paragraph="N129-3"><span class="qr-step">10.3 · 判讀與例子</span>例如 DMRL=0 且 NVMDSMSV=1 表示未回報建議 range 數上限；NVMDSMSV=0 時，DMRL=0 則表示不支援 Dataset Management。不能把所有 0 都翻成「無限制」。</p>
<h3>大表內的欄位位置</h3>
<div class="qr-table"><table class=""><thead><tr><th scope="col">欄位</th><th scope="col">查詢內容</th><th scope="col">PDF 頁</th></tr></thead><tbody><tr><td>VSL / WZSL</td><td>Verify／Write Zeroes 大小</td><td>103</td></tr><tr><td>WUSL / DMRL / DMRSL</td><td>Write Uncorrectable 與 DSM range 限制</td><td>104</td></tr><tr><td>DMSL / KPIOCAP / WZDSL</td><td>總 blocks、金鑰能力、deallocate 大小</td><td>105</td></tr><tr><td>AOCS / VER / RLA</td><td>Admin 能力、版本與速率限制能力</td><td>106</td></tr></tbody></table></div>
<p class="qr-tags">搜尋詞：CNS 06h · CSI 00h · VSL · WZSL · WUSL · DMRL · DMRSL · DMSL · NVMDSMSV</p>
<div class="qr-related">接著查：<a href="/nvme/figure-reference/identify/zh-tw/#figure-b338">Base 2.4 Figure 338 · Identify Controller：能力與限制的主要入口</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n47">NVM Command Set 1.3 Figure 47 · Dataset Management：每段 LBA 範圍如何排列</a><a href="/nvme/figure-reference/io/zh-tw/#figure-n83">NVM Command Set 1.3 Figure 83 · Write Zeroes：清零範圍與 deallocate 要求</a></div>
<a href="#figure-index">回本冊圖表索引</a></article>
<footer id="source-files"><h2>原始文件</h2><p>頁碼採本次提供的 ratified PDF；Base 的 PDF 頁＝文件頁＋26，另兩份相同。圖號與英文原名保留，可用 PDF 搜尋定位。公開網站不附原始 PDF。</p><ul class="qr-sources"><li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li></ul></footer>
</main></div>
