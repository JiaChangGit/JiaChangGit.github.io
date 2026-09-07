---
permalink: /nvme/nvm-command-set-1-3-zh-tw/
layout: post
read_time: true
show_date: true
title: "NVM Command Set 1.3：邏輯區塊、I/O 命令與資料保護"
date: 2026-09-03
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
[English]({% post_url 2026-09-03-nvme-nvm-command-set-1-3-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span>NVM Command Set 說明主機如何以 logical block 為單位讀寫與管理儲存空間。理解它的關鍵，是把資料格式、命令行為、資料完整性與資源管理連起來：同一筆命令，會因 namespace 格式、支援能力與設定不同而有不同的適用條件。</p><dl class="term-note" aria-label="本段名詞"><div><dt>logical block</dt><dd>邏輯區塊；namespace 可定址的基本單位，其資料大小由使用中的格式決定。</dd></div><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>儲存空間與格式</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span>先理解 namespace 的容量、LBA 格式，以及資料與 metadata 的關係。</p><dl class="term-note" aria-label="本段名詞"><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div><div><dt>metadata</dt><dd>隨 logical block 儲存的附加資料，可包含資料保護資訊，也可有其他用途。</dd></div><div><dt>LBA</dt><dd>Logical Block Address；以所選格式的 block 為單位。</dd></div></dl></article>
<article><span class="axis-number">02</span><h3>命令做了什麼</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span>比較 Read、Write、Compare、Verify、Copy 與空間管理命令的作用及完成條件。</p></article>
<article><span class="axis-number">03</span><h3>資料完整性與順序</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span>理解原子性、命令相依、Protection Information，以及資料檢查的範圍。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Protection Information</dt><dd>資料保護資訊，縮寫 PI；包含 Guard 與 tags，用來檢查資料及其關聯資訊。</dd></div></dl></article>
<article><span class="axis-number">04</span><h3>能力與資源管理</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="04-01">04-01</span>以 Identify、Features 和 log 理解格式選擇、效能限制及進階資源功能。</p></article>
</div>
<dl class="term-note" aria-label="本段名詞"><div><dt>Protection Information</dt><dd>資料保護資訊，縮寫 PI；包含 Guard 與 tags，用來檢查資料及其關聯資訊。</dd></div><div><dt>metadata</dt><dd>隨 logical block 儲存的附加資料，可包含資料保護資訊，也可有其他用途。</dd></div><div><dt>LBA</dt><dd>Logical Block Address；以所選格式的 block 為單位。</dd></div></dl>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span>主機透過提交佇列送出命令，控制器透過完成佇列回報結果。Base 規格定義這套共同機制；本篇聚焦命令如何作用於 namespace 內的 logical blocks。</p>
</section>
<section class="lesson" id="module-nvmcs-foundation"><h2 id="heading-nvmcs-foundation"><span class="section-number">01</span> Logical block、格式與單位</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span>Host 透過 logical block address 存取 namespace。先確定一個 block 的 data 與 metadata 大小，才能計算 buffer、理解命令範圍，並選擇適用的資料保護方式。讀 Format Index 時把 index 與 offset 分開：index 選格式，offset 才是從起點算出的位移。</p><dl class="term-note" aria-label="本段名詞"><div><dt>logical block</dt><dd>邏輯區塊；namespace 可定址的基本單位，其資料大小由使用中的格式決定。</dd></div><div><dt>Format Index</dt><dd>格式索引；用來選取一組 LBAF／ELBAF 格式資訊的編號。</dd></div><div><dt>offset</dt><dd>offset；從指定起點算出的位移。它回答「離起點多遠」，不等於 index。</dd></div><div><dt>index</dt><dd>index；用來選取清單中的項目或格式。它回答「選哪一項」，不是「離起點多遠」。</dd></div><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-FOUNDATION -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span>NVM Command Set 補充 Base 的 logical-block 語意；logical block data size 不含 metadata，logical block size 則包含。NVM 的 CSI 是 00h，命令、Feature、log 與 Identify 的相同數字分屬不同識別空間。</p><dl class="term-note" aria-label="本段名詞"><div><dt>CSI</dt><dd>I/O Command Set Identifier；選擇 I/O 命令集，NVM Command Set 使用 00h。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §1.1-1.6; 4.1.3.9; 4.1.4.8; 4.1.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §1.1-1.6; 4.1.3.9; 4.1.4.8; 4.1.5, 文件頁 9-12,73-75,79-83, PDF 頁 9-12,73-75,79-83</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>LBADS</td><td>data bytes = 2^LBADS</td><td>另加 MS 才是 logical block size</td></tr><tr><td>Format Index</td><td>同時選 LBAF 與 ELBAF</td><td>不能只看資料大小</td></tr><tr><td>Specification family</td><td>通用機制由 Base 定義</td><td>相依欄位另以 Base 來源標示</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>Format Index</dt><dd>格式索引；用來選取一組 LBAF／ELBAF 格式資訊的編號。</dd></div><div><dt>ELBAF</dt><dd>Extended LBA Format；與相同 index 的 LBAF 配對，補充 PI 格式與 Storage Tag 大小。</dd></div><div><dt>LBADS</dt><dd>LBA Data Size 的 exponent；資料 bytes=2^LBADS，0表示目前不可用。</dd></div><div><dt>index</dt><dd>index；用來選取清單中的項目或格式。它回答「選哪一項」，不是「離起點多遠」。</dd></div><div><dt>LBAF</dt><dd>LBA Format；描述一種 logical block 格式，包括資料及 metadata 大小。</dd></div><div><dt>MS</dt><dd>Metadata Size；每個 logical block 的 metadata bytes 數。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span>LBADS=0Ch、MS=16 時，資料為 4096 bytes，含 metadata 的 logical block 是 4112 bytes。FID 28h 與 LID 28h 雖相同，前者設定限制，後者回報能力圖。</p><dl class="term-note" aria-label="本段名詞"><div><dt>LBADS</dt><dd>LBA Data Size 的 exponent；資料 bytes=2^LBADS，0表示目前不可用。</dd></div><div><dt>FID</dt><dd>Feature Identifier；指定要讀取或設定哪一項 Feature 的編號。</dd></div><div><dt>LID</dt><dd>Log Page Identifier；指定要讀取哪一種 log page 的編號。</dd></div><div><dt>MS</dt><dd>Metadata Size；每個 logical block 的 metadata bytes 數。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-001 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-001"><summary>NVM Figure 1 · NVMe Family of Specifications</summary>
<!-- claim:NVMCS13-NVM-FIG-001-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.04">01.04.</span>Figure 1〈NVMe Family of Specifications〉：依功能層分開閱讀：Base 給共同機制，PCIe 給本機 transport，NVM 給 logical-block 命令語意。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express，主機與非揮發性記憶體子系統之間的介面規範家族。</dd></div><div><dt>PCIe</dt><dd>PCI Express，NVMe memory-based controller 使用的 transport 與裝置互連。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §1.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §1.1, Figure 1, 文件頁 9, PDF 頁 9</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>PCIe</dt><dd>PCI Express，NVMe memory-based controller 使用的 transport 與裝置互連。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-002 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-002"><summary>NVM Figure 2 · Acronym definitions</summary>
<!-- claim:NVMCS13-NVM-FIG-002-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.05">01.05.</span>Figure 2〈Acronym definitions〉：LBA 是 logical block 的位址，不是 byte offset；要換成資料 bytes，還需所選格式的 LBADS。</p><dl class="term-note" aria-label="本段名詞"><div><dt>offset</dt><dd>offset；從指定起點算出的位移。它回答「離起點多遠」，不等於 index。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §1.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §1.5, Figure 2, 文件頁 11, PDF 頁 11</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-capacity"><h2 id="heading-nvmcs-capacity"><span class="section-number">02</span> Namespace 容量與配置狀態</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span>先區分 logical address space 與實際配置，再分析寫入及 deallocate。讀取值與 allocation 狀態回答不同問題。</p>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 260" role="img"><title>可定址、可配置、已配置是 3 個不同的量</title><desc>教學例：NSZE=1000、NCAP=800、NUSE=600。LBA 編號的範圍與目前配置量要分開理解。</desc><rect x="20" y="20" width="720" height="70" rx="6" class="v-object"/><text x="380.0" y="48.5" text-anchor="middle" font-size="17">NSZE = 1000</text><text x="380.0" y="73.5" text-anchor="middle" font-size="17">LBA 0 … 999</text><rect x="20" y="110" width="576" height="55" rx="6" class="v-command"/><text x="308.0" y="143.5" text-anchor="middle" font-size="17">NCAP = 800</text><rect x="20" y="185" width="432" height="55" rx="6" class="v-success"/><text x="236.0" y="218.5" text-anchor="middle" font-size="17">NUSE = 600</text></svg></div><figcaption>教學例：NSZE=1000、NCAP=800、NUSE=600。LBA 編號的範圍與目前配置量要分開理解。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>NCAP</dt><dd>Namespace Capacity；同時可配置 logical blocks 最大數量。</dd></div><div><dt>NSZE</dt><dd>Namespace Size；可定址 logical blocks 總數。</dd></div><div><dt>NUSE</dt><dd>Namespace Utilization；目前配置 logical blocks 數量。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-CAPACITY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span>NSZE ≥ NCAP ≥ NUSE；NSZE 定義可定址範圍，NCAP 限制同時配置的 blocks，NUSE 計算目前已配置 blocks。THINP=0 時 NCAP=NSZE；NVMCAP 以 bytes 計，不能直接當成 NSZE 乘資料大小。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NVMCAP</dt><dd>NVM Capacity；以 bytes 計，不能與 NSZE／NCAP 的 logical-block 數直接比較。</dd></div><div><dt>THINP</dt><dd>Thin Provisioning，NSFEAT 中決定 NCAP 是否可小於 NSZE，以及 controller 是否必須追蹤 NUSE 的 bit。</dd></div><div><dt>NCAP</dt><dd>Namespace Capacity；同時可配置 logical blocks 最大數量。</dd></div><div><dt>NSZE</dt><dd>Namespace Size；可定址 logical blocks 總數。</dd></div><div><dt>NUSE</dt><dd>Namespace Utilization；目前配置 logical blocks 數量。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.1.1; 4.1.5.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1; 4.1.5.1, 文件頁 13-14,85-93, PDF 頁 13-14,85-93</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>NSZE</td><td>有效 LBA 為 0 到 NSZE−1</td><td>LBA 越界與容量不足不同</td></tr><tr><td>THINP</td><td>支援時須追蹤 NUSE</td><td>不支援時可固定回 NCAP</td></tr><tr><td>Allocation</td><td>Write、Copy 寫入端及 WU 可配置</td><td>Read／Verify 不改 deallocation 狀態</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>THINP</dt><dd>Thin Provisioning，NSFEAT 中決定 NCAP 是否可小於 NSZE，以及 controller 是否必須追蹤 NUSE 的 bit。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span>NSZE=1000、NCAP=800、NUSE=600 可是合法 thin namespace。LBA 900 在可定址範圍內，但新增配置仍受 800-block capacity 限制。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-123 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-123"><summary>NVM Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</summary>
<!-- claim:NVMCS13-NVM-FIG-123-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.04">02.04.</span>Figure 123〈Identify – Identify Namespace Data Structure, NVM Command Set〉：把這張跨頁資料結構分成容量、格式能力／目前格式、deallocation、atomicity、performance、Copy limits 與識別資料七組；每組先看 capability gate 再使用數值。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.5.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1, Figure 123, 文件頁 85-93, PDF 頁 85-93</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>FLBAS</dt><dd>Formatted LBA Size，選擇 namespace 使用的 LBA format，並包含 metadata placement 相關控制。</dd></div><div><dt>NLBAF</dt><dd>共同屬性 LBA formats 數的 0-based 欄位。</dd></div><div><dt>DPS</dt><dd>End-to-end Data Protection Type Settings，create 時選擇 Protection Information type 與位置的欄位。</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-identify"><h2 id="heading-nvmcs-identify"><span class="section-number">03</span> Identify：同一 namespace 的多份資料結構</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span>每次查詢都寫出 CNS、CSI、NSID、Format Index 的角色。不同查詢回零有不同含義，不能一律解讀為不存在或不支援。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NSID</dt><dd>Namespace Identifier；識別命令作用的 namespace。</dd></div><div><dt>CNS</dt><dd>Controller or Namespace Structure；Identify 命令用來選擇回傳資料結構的欄位。</dd></div><div><dt>CSI</dt><dd>I/O Command Set Identifier；選擇 I/O 命令集，NVM Command Set 使用 00h。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-IDENTIFY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span>NVM CSI=00h。完整 namespace 資訊需結合 CNS 08h 的 command-set-independent 結構、CNS 00h 的 NVM 結構與 CNS 05h／CSI 00h 的 NVM 延伸結構；CNS 01h 與 06h 則提供 controller 資訊。</p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div><div><dt>CNS</dt><dd>Controller or Namespace Structure；Identify 命令用來選擇回傳資料結構的欄位。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5, 文件頁 83-110, PDF 頁 83-110</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>CNS 00h / 05h</td><td>namespace 的 NVM 基本／延伸欄位</td><td>FLBAS 決定目前 FIDX；MC／DPC 是能力</td></tr><tr><td>CNS 01h / 06h</td><td>AWUN 等通用位置與 NVM 專屬限制</td><td>06h 的 VSL／WZSL 等需結合 variant bits</td></tr><tr><td>CNS 11h / 1Bh</td><td>allocated namespace 資訊</td><td>不等同 active namespace 查詢</td></tr><tr><td>CNS 09h / 0Ah</td><td>以 FIDX 查能力</td><td>Common=No 欄位清零</td></tr><tr><td>CNS 16h</td><td>namespace granularity list</td><td>GDM 決定 descriptor 如何對應 format</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>FLBAS</dt><dd>Formatted LBA Size，選擇 namespace 使用的 LBA format，並包含 metadata placement 相關控制。</dd></div><div><dt>AWUN</dt><dd>Atomic Write Unit Normal；controller 正常原子寫入大小的 0-based 欄位。</dd></div><div><dt>WZSL</dt><dd>Write Zeroes Size Limit；Write Zeroes 的大小限制，需結合 variant 能力判讀。</dd></div><div><dt>VSL</dt><dd>Verify Size Limit；Verify 的大小限制，需結合 variant 能力判讀。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.03">03.03.</span>NSID=7 的目前格式需讀 FLBAS 再取同 index 的 LBAF 與 ELBAF。查尚未建立的 FIDX=3 能力，使用 09h／0Ah、CSI=0、NSID=0、FIDX=3，另結合 CNS08h 的共同能力。</p><dl class="term-note" aria-label="本段名詞"><div><dt>ELBAF</dt><dd>Extended LBA Format；與相同 index 的 LBAF 配對，補充 PI 格式與 Storage Tag 大小。</dd></div><div><dt>LBAF</dt><dd>LBA Format；描述一種 logical block 格式，包括資料及 metadata 大小。</dd></div><div><dt>NSID</dt><dd>Namespace Identifier；識別命令作用的 namespace。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-122 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-122"><summary>NVM Figure 122 · CNS Values</summary>
<!-- claim:NVMCS13-NVM-FIG-122-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.04">03.04.</span>Figure 122〈CNS Values〉：以 CNS 選資料結構，再看 NSID／CSI 是否使用；00h、05h、08h 的 namespace 資訊互補，09h／0Ah 用 FIDX。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5, Figure 122, 文件頁 83-84, PDF 頁 83-84</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-126 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-126"><summary>NVM Figure 126 · Identify – Identify Controller data structure, NVM Command Set Specific Fields</summary>
<!-- claim:NVMCS13-NVM-FIG-126-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.05">03.05.</span>Figure 126〈Identify – Identify Controller data structure, NVM Command Set Specific Fields〉：controller atomicity 值供適用 namespaces 使用；namespace capability 可覆寫，AWUPF 不大於 AWUN，ACWU 專供 fused Compare-and-Write。</p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div><div><dt>AWUPF</dt><dd>Atomic Write Unit Power Fail；失敗條件原子大小的0-based欄位。</dd></div><div><dt>ACWU</dt><dd>Atomic Compare and Write Unit；controller 的 fused compare-and-write 大小限制。</dd></div><div><dt>AWUN</dt><dd>Atomic Write Unit Normal；controller 正常原子寫入大小的 0-based 欄位。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.5.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.2, Figure 126, 文件頁 94-96, PDF 頁 94-96</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>AWUPF</dt><dd>Atomic Write Unit Power Fail；失敗條件原子大小的0-based欄位。</dd></div><div><dt>ACWU</dt><dd>Atomic Compare and Write Unit；controller 的 fused compare-and-write 大小限制。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-129 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-129"><summary>NVM Figure 129 · I/O Command Set Specific Identify Controller Data Structure for the NVM Command Set</summary>
<!-- claim:NVMCS13-NVM-FIG-129-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.06">03.06.</span>Figure 129〈I/O Command Set Specific Identify Controller Data Structure for the NVM Command Set〉：本表實際延伸到文件頁106，不能只讀有 caption 的103頁。Size limits 要結合 ONCS variants；SLMC 是 0-based，VER 為 command-set 版本。</p><dl class="term-note" aria-label="本段名詞"><div><dt>ONCS</dt><dd>Optional NVM Commands Supported；包含能力及 variant，需結合 NVM Identify 的 limits。</dd></div><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.5.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.4, Figure 129, 文件頁 103-106, PDF 頁 103-106</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>DMRSL</dt><dd>Dataset Management Range Size Limit；單一 range 的 logical block 處理數量限制。</dd></div><div><dt>WZDSL</dt><dd>Write Zeroes with Deallocate 的專用大小限制；不可直接沿用 WZSL。</dd></div><div><dt>DMRL</dt><dd>Dataset Management Ranges Limit，實際 range 數上限。</dd></div><div><dt>DMSL</dt><dd>Dataset Management Size Limit；整筆命令的 logical block 處理數量限制。</dd></div><div><dt>WUSL</dt><dd>Write Uncorrectable Size Limit；Write Uncorrectable 的大小限制，需結合 variant 能力判讀。</dd></div><div><dt>WZSL</dt><dd>Write Zeroes Size Limit；Write Zeroes 的大小限制，需結合 variant 能力判讀。</dd></div><div><dt>VSL</dt><dd>Verify Size Limit；Verify 的大小限制，需結合 variant 能力判讀。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-130 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-130"><summary>NVM Figure 130 · NVM Command Set Specification Version Descriptor Field Values</summary>
<!-- claim:NVMCS13-NVM-FIG-130-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.07">03.07.</span>Figure 130〈NVM Command Set Specification Version Descriptor Field Values〉：1.3 對應 MJR=1、MNR=3、TER=0；此為 NVM command-set version，與 Base version 另記。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.5.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.4, Figure 130, 文件頁 107, PDF 頁 107</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-131 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-131"><summary>NVM Figure 131 · Command Dword 11 - CNS Specific Identifiers</summary>
<!-- claim:NVMCS13-NVM-FIG-131-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.08">03.08.</span>Figure 131〈Command Dword 11 - CNS Specific Identifiers〉：CNS09h／0Ah 的 CDW11 low16 是 Format Index，不能同時當成某個 namespace ID；CSI 另選 command set。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Dword</dt><dd>Dword（Double word）；32 bits，也就是 4 bytes。對比 word=16 bits；例如 zero-based dword count=3 代表 4 個 Dwords，也就是 16 bytes。</dd></div><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.5.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.5, Figure 131, 文件頁 107, PDF 頁 107</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-338 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-338"><summary>Base Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</summary>
<!-- claim:NVMCS13-BASE-FIG-338-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.09">03.09.</span>Figure 338〈Identify – Identify Controller Data Structure, I/O Command Set Independent〉：NVM 需要 Base Identify 的 ONCS variants、CTRATT.ELBAS／MEM、MDTS 與 SANICAP 等能力。</p><dl class="term-note" aria-label="本段名詞"><div><dt>MDTS</dt><dd>Maximum Data Transfer Size；以 minimum page size 為基準的 exponent；零有特定無限制語意。</dd></div><div><dt>ONCS</dt><dd>Optional NVM Commands Supported；包含能力及 variant，需結合 NVM Identify 的 limits。</dd></div><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.14.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, 文件頁 340-382, PDF 頁 366-408</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>MDTS</dt><dd>Maximum Data Transfer Size；以 minimum page size 為基準的 exponent；零有特定無限制語意。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-BASE-FIG-346 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-346"><summary>Base Figure 346 · Identify – I/O Command Set Independent Identify Namespace Data Structure</summary>
<!-- claim:NVMCS13-BASE-FIG-346-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.10">03.10.</span>Figure 346〈Identify – I/O Command Set Independent Identify Namespace Data Structure〉：CNS08h 提供 command-set-independent namespace 屬性，與 NVM CNS00h／05h 組合；不應只依其中一份結構推論全部能力。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.14.2.8</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.8, Figure 346, 文件頁 391-394, PDF 頁 417-420</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>ANAGRPID</dt><dd>ANA Group Identifier，namespace 所屬 Asymmetric Namespace Access group 的 identifier；create 值 0 讓 controller 選擇。</dd></div><div><dt>NMIC</dt><dd>Namespace Multi-path I/O and Namespace Sharing Capabilities，create 時宣告 namespace sharing／multipath 屬性的欄位。</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-format-list"><h2 id="heading-nvmcs-format-list"><span class="section-number">04</span> LBAF、ELBAF 與唯一屬性格式</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span>基本 entry 給資料／metadata 大小與相對效能，extended entry 給 PI 格式與 Storage Tag 分配。Unique-attribute entries 要個別查詢，不能沿用共同能力。</p><dl class="term-note" aria-label="本段名詞"><div><dt>PI</dt><dd>Protection Information；用 Guard 與 tags 檢查資料及其關聯資訊的保護欄位。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-FORMAT-LIST -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span>LBAF 與 ELBAF 以同一 Format Index 配對；總 format 數為 raw NLBAF+1+NULBAF。NLBAF 是 0-based、NULBAF 是實際數量。有效 index 還要檢查 LBADS：值 0 表示該支援格式目前不可用。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NULBAF</dt><dd>Unique Attribute LBA Formats 的實際數量；可以為0。</dd></div><div><dt>NLBAF</dt><dd>共同屬性 LBA formats 數的 0-based 欄位。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.5.1; 4.1.5.3; 5.6</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1; 4.1.5.3; 5.6, 文件頁 85-94,96-102,160-162, PDF 頁 85-94,96-102,160-162</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>LBAF</td><td>LBADS、MS、RP</td><td>RP 是指定 workload 的相對級別</td></tr><tr><td>ELBAF</td><td>PIF、QPIF、STS</td><td>QPIF 只在 qualified type 下適用</td></tr><tr><td>FLBAS</td><td>FIDXU 與 FIDXL 組成 index</td><td>MTELBA 是另一個 metadata bit</td></tr><tr><td>NULBAF</td><td>追加在共同格式之後</td><td>09h／0Ah 能讀各自能力</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>NULBAF</dt><dd>Unique Attribute LBA Formats 的實際數量；可以為0。</dd></div><div><dt>QPIF</dt><dd>Qualified Protection Information Format；指定 qualified PI 的格式。</dd></div><div><dt>PIF</dt><dd>Protection Information Format；選擇 PI 格式；qualified 格式再使用 QPIF。</dd></div><div><dt>STS</dt><dd>Storage Tag Size；固定 Storage/Reference Space 中的高位 bit 數。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.03">04.03.</span>raw NLBAF=3、NULBAF=2：有 4 個共同格式及 2 個唯一屬性格式，共 6 個，合法 index 為 0..5。Figure 192 圖示採概念數量，不能直接代入未依欄位換算的 raw NLBAF。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-124 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-124"><summary>NVM Figure 124 · Namespace Alignment and Granularity Attributes</summary>
<!-- claim:NVMCS13-NVM-FIG-124-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.04">04.04.</span>Figure 124〈Namespace Alignment and Granularity Attributes〉：OPTPERF 是 2-bit selector：不同值啟用不同 small／large deallocate 欄位組；不是一個通用的 performance enabled bit。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.5.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1, Figure 124, 文件頁 94, PDF 頁 94</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-125 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-125"><summary>NVM Figure 125 · LBA Format Data Structure, NVM Command Set Specific</summary>
<!-- claim:NVMCS13-NVM-FIG-125-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.05">04.05.</span>Figure 125〈LBA Format Data Structure, NVM Command Set Specific〉：LBADS 為 exponent，MS 為實際 metadata bytes，RP 為相對效能級別；LBADS=0 是目前不可用，不能解成一個 byte 或 512 bytes。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.5.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1, Figure 125, 文件頁 94, PDF 頁 94</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-127 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-127"><summary>NVM Figure 127 · NVM Command Set I/O Command Set Specific Identify Namespace Data Structure</summary>
<!-- claim:NVMCS13-NVM-FIG-127-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.06">04.06.</span>Figure 127〈NVM Command Set I/O Command Set Specific Identify Namespace Data Structure〉：延伸 namespace 結構把 PI／mask 能力、每-format ELBAF 與性能／allocation hints 分開；NPRG／NPRA／NORS 受 OPTRPERF 限制。</p><dl class="term-note" aria-label="本段名詞"><div><dt>PI</dt><dd>Protection Information；用 Guard 與 tags 檢查資料及其關聯資訊的保護欄位。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.5.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.3, Figure 127, 文件頁 97-101, PDF 頁 97-101</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>LBSTM</dt><dd>Tag comparison mask；bit=0 排除比較，Storage mask 額外受支援與對齊限制。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-128 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-128"><summary>NVM Figure 128 · Extended LBA Format Data Structure, NVM Command Set Specific</summary>
<!-- claim:NVMCS13-NVM-FIG-128-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.07">04.07.</span>Figure 128〈Extended LBA Format Data Structure, NVM Command Set Specific〉：PIF=11b 且支援 QPIFS 才使用 QPIF；STS 是 bits count，切分固定寬度的 Storage/Reference Space，沒有增大 PI。</p><dl class="term-note" aria-label="本段名詞"><div><dt>QPIF</dt><dd>Qualified Protection Information Format；指定 qualified PI 的格式。</dd></div><div><dt>PIF</dt><dd>Protection Information Format；選擇 PI 格式；qualified 格式再使用 QPIF。</dd></div><div><dt>STS</dt><dd>Storage Tag Size；固定 Storage/Reference Space 中的高位 bit 數。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.5.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.3, Figure 128, 文件頁 101-102, PDF 頁 101-102</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-192 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-192"><summary>NVM Figure 192 · LBA Format List Structure</summary>
<!-- claim:NVMCS13-NVM-FIG-192-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.08">04.08.</span>Figure 192〈LBA Format List Structure〉：先把 raw NLBAF 加1成共同格式數，再加 NULBAF；unique attributes 區緊接在共同區之後。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.6</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.6, Figure 192, 文件頁 161, PDF 頁 161</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-193 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-193"><summary>NVM Figure 193 · LBA Format List Entries Applicability to Identify Command CNS Value</summary>
<!-- claim:NVMCS13-NVM-FIG-193-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.09">04.09.</span>Figure 193〈LBA Format List Entries Applicability to Identify Command CNS Value〉：共同能力查詢與 per-format 查詢覆蓋的格式集合不同；09h／0Ah 可查 NULBAF 定義的 unique-attribute entries。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.6</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.6, Figure 193, 文件頁 162, PDF 頁 162</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-format"><h2 id="heading-nvmcs-format"><span class="section-number">05</span> Format、Host Behavior 與延伸 LBA</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span>格式切換會改變 block 數與欄位適用性，建立 buffer 前要重新 Identify。能力列表與目前格式不能混用。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-FORMAT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.02">05.02.</span>Format NVM 選取已支援的 Format Index、PI type 與 metadata 傳輸方式。延伸 PI 及超過 legacy 16 個 entries 的 LBA formats 需檢查 controller ELBAS 與 host LBAFEE；沒有 host 啟用不可直接使用。</p><dl class="term-note" aria-label="本段名詞"><div><dt>LBAFEE</dt><dd>Host 的 LBA Format Extension Enable 宣告。</dd></div><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.2; 4.1.3.7</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.2; 4.1.3.7, 文件頁 62-63,68-69, PDF 頁 62-63,68-69</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>PI / PIL</td><td>PI=0 關閉，1/2/3 選 protection type</td><td>本版 PIL 必須 0，PI 位於末端</td></tr><tr><td>MSET</td><td>1：extended LBA；0：separate metadata</td><td>MS=0 時忽略</td></tr><tr><td>LBAFEE</td><td>FID 16h byte 2，合法值 0／1</td><td>配合 ELBAS 決定延伸格式</td></tr><tr><td>STS</td><td>Format 不提供自由改成非零 STS 的方法</td><td>新配置可由 namespace create 建立</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>LBAFEE</dt><dd>Host 的 LBA Format Extension Enable 宣告。</dd></div><div><dt>FID</dt><dd>Feature Identifier；指定要讀取或設定哪一項 Feature 的編號。</dd></div><div><dt>PIL</dt><dd>Protection Information Location；用來判斷 PI 在 metadata 前端或後端，需遵守所選 Guard 格式限制。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="05.03">05.03.</span>要使用 64b Guard、MS=16 的格式，先確認 ELBAS、LBAFEE=1、對應 LBAF／ELBAF 及 PI capability。不能只設定 Format 的 PI=1 就宣告 64b Guard。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Guard</dt><dd>PI 的檢查值欄位；所選格式決定檢查值的寬度與計算方法。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-091 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-091"><summary>NVM Figure 91 · Format NVM – Command Dword 10 – NVM Command Set Specific Fields</summary>
<!-- claim:NVMCS13-NVM-FIG-091-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.04">05.04.</span>Figure 91〈Format NVM – Command Dword 10 – NVM Command Set Specific Fields〉：PI 選 protection type，MSET 選 metadata transfer；本版 PIL=0。Guard width 另由 LBAF／ELBAF 決定。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Dword</dt><dd>Dword（Double word）；32 bits，也就是 4 bytes。對比 word=16 bits；例如 zero-based dword count=3 代表 4 個 Dwords，也就是 16 bytes。</dd></div><div><dt>Guard</dt><dd>PI 的檢查值欄位；所選格式決定檢查值的寬度與計算方法。</dd></div><div><dt>PIL</dt><dd>Protection Information Location；用來判斷 PI 在 metadata 前端或後端，需遵守所選 Guard 格式限制。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.2, Figure 91, 文件頁 63, PDF 頁 63</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-101 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-101"><summary>NVM Figure 101 · Host Behavior Support – Data Structure</summary>
<!-- claim:NVMCS13-NVM-FIG-101-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.05">05.05.</span>Figure 101〈Host Behavior Support – Data Structure〉：Host Behavior Support byte2 的 LBAFEE 允許 host 宣告延伸 LBA formats；只允許 0／1，並需對照 controller ELBAS。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.7</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.7, Figure 101, 文件頁 68, PDF 頁 68</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-namespace-create"><h2 id="heading-nvmcs-namespace-create"><span class="section-number">06</span> 建立 namespace：格式、mask 與 granularity</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.01">06.01.</span>先取得 Format Index 能力再填 host-specified fields；不可直接把整份 Identify Namespace 原封不動當作 create payload。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-NAMESPACE-CREATE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.02">06.02.</span>Namespace create 的 NVM payload 指定 NSZE、NCAP、FLBAS、DPS、LBSTM 與 placement handles。Namespace Size／Capacity Granularity 以 bytes 回報且是 hints；不符合 granularity 但其他條件合法時，不得僅因此拒絕 create。</p><dl class="term-note" aria-label="本段名詞"><div><dt>LBSTM</dt><dd>Tag comparison mask；bit=0 排除比較，Storage mask 額外受支援與對齊限制。</dd></div><div><dt>DPS</dt><dd>End-to-end Data Protection Type Settings，create 時選擇 Protection Information type 與位置的欄位。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.6; 4.1.5.8; 5.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6; 4.1.5.8; 5.8, 文件頁 108,110-113,165, PDF 頁 108,110-113,165</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>NSZE / NCAP</td><td>值以 logical blocks 指定</td><td>與 bytes granularity 比較前先換算</td></tr><tr><td>LBSTM</td><td>需符合 PIC／PIFA mask 約束</td><td>不符回 Invalid Field in Command</td></tr><tr><td>GDM / ND</td><td>GDM=0 使用 descriptor 0 對全部格式</td><td>ND 是 0-based</td></tr><tr><td>Completion</td><td>成功 create 後已按指定屬性 format</td><td>attachment 是另一個管理動作</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="06.03">06.03.</span>假設 NSG=1 MiB、NCG=1 MiB、logical block size=4096，NSZE=NCAP=256 的容量可完整定址；若改成 257，granularity hints 可能造成額外不可定址配置，但本身不是拒絕理由。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NCG</dt><dd>Namespace Capacity Granularity，以 bytes 表示 controller 偏好的 NCAP allocation granularity。</dd></div><div><dt>NSG</dt><dd>Namespace Size Granularity，以 bytes 表示 controller 偏好的 NSZE allocation granularity。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-132 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-132"><summary>NVM Figure 132 · Namespace Granularity List</summary>
<!-- claim:NVMCS13-NVM-FIG-132-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.04">06.04.</span>Figure 132〈Namespace Granularity List〉：GDM=0 時 descriptor0 套全部格式，ND=0；GDM=1 以相同 index 對應 format。ND 是 0-based，支援數量受 LBAFEE 影響。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.5.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.8, Figure 132, 文件頁 108, PDF 頁 108</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-133 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-133"><summary>NVM Figure 133 · Namespace Granularity Descriptor</summary>
<!-- claim:NVMCS13-NVM-FIG-133-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.05">06.05.</span>Figure 133〈Namespace Granularity Descriptor〉：NSG／NCG 以 bytes 表示 preferred allocation granularity；0 表示未回報，不能拿來做除法或要求 namespace 大小為零。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NCG</dt><dd>Namespace Capacity Granularity，以 bytes 表示 controller 偏好的 NCAP allocation granularity。</dd></div><div><dt>NSG</dt><dd>Namespace Size Granularity，以 bytes 表示 controller 偏好的 NSZE allocation granularity。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.5.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.8, Figure 133, 文件頁 108, PDF 頁 108</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-134 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-134"><summary>NVM Figure 134 · Namespace Management – Host Specified Fields</summary>
<!-- claim:NVMCS13-NVM-FIG-134-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.06">06.06.</span>Figure 134〈Namespace Management – Host Specified Fields〉：Create payload 只有指定欄位可由 host 填寫；LBSTM／placement list 不在基本 Identify 相同區段，不能直接 memcpy 整份 Identify 結構。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.6.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.4, Figure 134, 文件頁 112-113, PDF 頁 112-113</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>ANAGRPID</dt><dd>ANA Group Identifier，namespace 所屬 Asymmetric Namespace Access group 的 identifier；create 值 0 讓 controller 選擇。</dd></div><div><dt>NVMSETID</dt><dd>NVM Set Identifier，指定建立 namespace 時要從哪個 NVM Set 配置容量。</dd></div><div><dt>NPHNDLS</dt><dd>Number of Placement Handles，NVM create payload 中 Placement Handle List 的 entry count，最大 128。</dd></div><div><dt>ENDGID</dt><dd>Endurance Group Identifier，指定建立 namespace 時所屬 Endurance Group。</dd></div><div><dt>NMIC</dt><dd>Namespace Multi-path I/O and Namespace Sharing Capabilities，create 時宣告 namespace sharing／multipath 屬性的欄位。</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-metadata"><h2 id="heading-nvmcs-metadata"><span class="section-number">07</span> Metadata 傳輸與 PI 的位置</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.01">07.01.</span>Metadata 不一定全是 PI。先標示 data、非 PI metadata 與 PI 三個區域，再計算 host buffer 大小與 CRC coverage。</p><dl class="term-note" aria-label="本段名詞"><div><dt>CRC</dt><dd>Cyclic Redundancy Check，循環冗餘檢查；由資料位元計算檢查值，以偵測資料變化。</dd></div></dl>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 260" role="img"><title>資料與 Metadata 放在哪裡</title><desc>同一批 logical blocks 的資料與 metadata 必須對應；可以交錯傳輸，也可以分開傳輸。</desc><rect x="20" y="30" width="240" height="65" rx="6" class="v-object"/><text x="140.0" y="68.5" text-anchor="middle" font-size="17">Data 0</text><rect x="260" y="30" width="120" height="65" rx="6" class="v-decision"/><text x="320.0" y="68.5" text-anchor="middle" font-size="17">MD 0</text><rect x="390" y="30" width="230" height="65" rx="6" class="v-object"/><text x="505.0" y="68.5" text-anchor="middle" font-size="17">Data 1</text><rect x="620" y="30" width="120" height="65" rx="6" class="v-decision"/><text x="680.0" y="68.5" text-anchor="middle" font-size="17">MD 1</text><rect x="20" y="155" width="350" height="65" rx="6" class="v-command"/><text x="195.0" y="193.5" text-anchor="middle" font-size="17">DPTR: Data 0, Data 1</text><rect x="390" y="155" width="350" height="65" rx="6" class="v-decision"/><text x="565.0" y="193.5" text-anchor="middle" font-size="17">MPTR: MD 0, MD 1</text></svg></div><figcaption>同一批 logical blocks 的資料與 metadata 必須對應；可以交錯傳輸，也可以分開傳輸。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>DPTR</dt><dd>命令 data pointer；Read 是目的、Write 是來源、Copy／DSM 指向 descriptors。</dd></div><div><dt>MPTR</dt><dd>Separate metadata 的指標；metadata placement 由 namespace format 與命令欄位決定。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-METADATA -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.02">07.02.</span>每個 namespace 在 format 時選一種 metadata 傳輸機制：與 data 相連形成 extended LBA，或由 MPTR 指向 separate buffer。不能把 metadata 分拆到兩種機制；寫入時 metadata 必須與其 logical block 原子寫入。</p><dl class="term-note" aria-label="本段名詞"><div><dt>MPTR</dt><dd>Separate metadata 的指標；metadata placement 由 namespace format 與命令欄位決定。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.1.6; 5.2.3; 5.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.6; 5.2.3; 5.3, 文件頁 22,129-131, PDF 頁 22,129-131</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>Extended LBA</td><td>DPTR 指向 data+metadata 交錯序列</td><td>MSET／MTELBA 反映此選擇</td></tr><tr><td>Separate buffer</td><td>DPTR 給 data，MPTR 給 metadata</td><td>PRP metadata 需 physically contiguous；SGL 可分散</td></tr><tr><td>PI location</td><td>本版有效格式的 PI 在 metadata 末端</td><td>CRC 包含之前的非 PI metadata</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>DPTR</dt><dd>命令 data pointer；Read 是目的、Write 是來源、Copy／DSM 指向 descriptors。</dd></div><div><dt>CRC</dt><dd>Cyclic Redundancy Check，循環冗餘檢查；由資料位元計算檢查值，以偵測資料變化。</dd></div><div><dt>PRP</dt><dd>Physical Region Page，以 memory page 為單位描述 host-addressable data buffer 的 pointer 格式。</dd></div><div><dt>SGL</dt><dd>Scatter Gather List，以 descriptor 與 segment 描述一段或多段 data buffer 的格式。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="07.03">07.03.</span>8 blocks、data=4096、MS=16、PRACT=0：extended buffer 為 32896 bytes；separate 模式 data buffer=32768、metadata buffer=128 bytes。</p><dl class="term-note" aria-label="本段名詞"><div><dt>PRACT</dt><dd>Protection Information Action；依命令與 MS 選擇 PI 處理。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-153 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-153"><summary>NVM Figure 153 · Metadata – Contiguous with LBA Data, Forming Extended LBA</summary>
<!-- claim:NVMCS13-NVM-FIG-153-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.04">07.04.</span>Figure 153〈Metadata – Contiguous with LBA Data, Forming Extended LBA〉：extended LBA 依序排列每個 block 的 data 後接 metadata；不可把全部 data 排完才接全部 metadata。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.2.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.3, Figure 153, 文件頁 129, PDF 頁 129</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-154 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-154"><summary>NVM Figure 154 · Metadata – Transferred as Separate Buffer</summary>
<!-- claim:NVMCS13-NVM-FIG-154-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.05">07.05.</span>Figure 154〈Metadata – Transferred as Separate Buffer〉：separate 模式保留 data 與 metadata 兩個 buffer 並保持 block 對應；不是把 metadata 任意重排成無序清單。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.2.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.3, Figure 154, 文件頁 130, PDF 頁 130</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-support-status"><h2 id="heading-nvmcs-support-status"><span class="section-number">08</span> 能力探索、Opcode 與狀態</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.01">08.01.</span>從 controller 類型開始建立命令、Feature、log 的能力矩陣。資料指標指向的可能是使用者資料，也可能只是控制 descriptor。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-SUPPORT-STATUS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.02">08.02.</span>NVM I/O controller 必須支援 Read 與 Write；其他列出的 NVM 命令依各能力條件判斷。Opcode 低兩 bits 表示資料傳輸方向，狀態值必須連同 SCT 解讀，不能只用 SC 數值查錯誤。</p><dl class="term-note" aria-label="本段名詞"><div><dt>I/O controller</dt><dd>I/O controller，可執行使用者資料 I/O command 的 controller 類型。</dd></div><div><dt>SCT</dt><dd>Status Code Type；指定完成狀態碼所屬類別，需與 SC 一起解讀。</dd></div><div><dt>SC</dt><dd>Status Code；指定所選 SCT 類別中的完成結果。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.2; 3.1; 3.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.2; 3.1; 3.3, 文件頁 22-27, PDF 頁 22-27</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>Read 02h / Write 01h</td><td>必要 I/O 命令</td><td>Administrative controller 不處理 I/O</td></tr><tr><td>Get LBA Status 86h</td><td>選用 Admin 命令</td><td>I/O controller 適用能力</td></tr><tr><td>SC 80h</td><td>依 SCT 區分 LBA Out of Range 等</td><td>同時記錄 opcode、NSID、SCT、SC、DNR</td></tr><tr><td>FID / LID</td><td>05h、0Ah 為必要 NVM Features</td><td>功能支援不等於要求寫入 Persistent Event Log</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>Administrative controller</dt><dd>Administrative controller，以管理為目的且不執行使用者資料 I/O command 的 controller 類型。</dd></div><div><dt>I/O controller</dt><dd>I/O controller，可執行使用者資料 I/O command 的 controller 類型。</dd></div><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div><div><dt>DNR</dt><dd>Do Not Retry，CQE status 中提示以相同 command 重試預期不會成功的 bit。</dd></div><div><dt>LID</dt><dd>Log Page Identifier；指定要讀取哪一種 log page 的編號。</dd></div><div><dt>SCT</dt><dd>Status Code Type；指定完成狀態碼所屬類別，需與 SC 一起解讀。</dd></div><div><dt>SC</dt><dd>Status Code；指定所選 SCT 類別中的完成結果。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="08.03">08.03.</span>Copy opcode=19h 的低 bits 是 01b，因 host 傳入 source descriptors；並不表示需要把整份待複製資料從 host 再傳一次。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-013 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-013"><summary>NVM Figure 13 · NVM Command Set Admin Command Support</summary>
<!-- claim:NVMCS13-NVM-FIG-013-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.04">08.04.</span>Figure 13〈NVM Command Set Admin Command Support〉：Get LBA Status 86h 對 I/O controller 是 optional、對 Administrative controller 禁止。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Administrative controller</dt><dd>Administrative controller，以管理為目的且不執行使用者資料 I/O command 的 controller 類型。</dd></div><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.2.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.2.1, Figure 13, 文件頁 23, PDF 頁 23</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-014 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-014"><summary>NVM Figure 14 · I/O Controller – NVM Command Set I/O Command Support</summary>
<!-- claim:NVMCS13-NVM-FIG-014-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.05">08.05.</span>Figure 14〈I/O Controller – NVM Command Set I/O Command Support〉：Read／Write 是 mandatory；Compare、Verify、Copy、Write Zeroes、Write Uncorrectable 等須檢查各自能力，不能用表列存在代替支援宣告。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.2.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.2.1, Figure 14, 文件頁 23, PDF 頁 23</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-015 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-015"><summary>NVM Figure 15 · NVM Command Set Log Page Support</summary>
<!-- claim:NVMCS13-NVM-FIG-015-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.06">08.06.</span>Figure 15〈NVM Command Set Log Page Support〉：0Eh 為 I/O controller 的 optional log；28h 對 I/O 與 Administrative controllers 都是 optional。支援與作用域另查 log 定義。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.2.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.2.2, Figure 15, 文件頁 23, PDF 頁 23</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-016 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-016"><summary>NVM Figure 16 · NVM Command Set Feature Support</summary>
<!-- claim:NVMCS13-NVM-FIG-016-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.07">08.07.</span>Figure 16〈NVM Command Set Feature Support〉：將各 Feature 的 support row 與 controller 類型對照；Administrative controller 的 Performance Characteristics 不允許 namespace scope。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.2.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.2.3, Figure 16, 文件頁 23-24, PDF 頁 23-24</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-017 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-017"><summary>NVM Figure 17 · NVM Command Set Feature Logged in Persistent Event Log Page Requirement</summary>
<!-- claim:NVMCS13-NVM-FIG-017-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.08">08.08.</span>Figure 17〈NVM Command Set Feature Logged in Persistent Event Log Page Requirement〉：此表是是否將 Feature 更新寫入 Persistent Event Log 的要求；03h 的 NR 不是禁止使用該 Feature，也不是其他 Features 的支援等級。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NR</dt><dd>Range count 的 0-based 欄位；實際 descriptors 數為 NR+1。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.2.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.2.3, Figure 17, 文件頁 24, PDF 頁 24</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-018 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-018"><summary>NVM Figure 18 · Status Code – Generic Command Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-018-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.09">08.09.</span>Figure 18〈Status Code – Generic Command Status Values〉：Generic status 80h 是 LBA Out of Range，81h 是 Capacity Exceeded；依欄位換算前保留 SCT，並分別核對 NSZE 與 NCAP／NUSE。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.1.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.1.2, Figure 18, 文件頁 25, PDF 頁 25</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-019 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-019"><summary>NVM Figure 19 · Status Code – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-019-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.10">08.10.</span>Figure 19〈Status Code – Command Specific Status Values〉：用 opcode 與 SCT=1 找對應 command-specific status；例如 Copy 的格式／重疊錯誤與 Read 的 PI 錯誤有不同適用集合。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.1.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.1.2, Figure 19, 文件頁 25, PDF 頁 25</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-020 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-020"><summary>NVM Figure 20 · Status Code – Media and Data Integrity Error Values</summary>
<!-- claim:NVMCS13-NVM-FIG-020-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.11">08.11.</span>Figure 20〈Status Code – Media and Data Integrity Error Values〉：Media/Data Integrity 類型含 Compare miscompare 與 deallocated/unwritten 存取錯誤；後者要回查 DULBE，而非直接判為壞媒體。</p><dl class="term-note" aria-label="本段名詞"><div><dt>DULBE</dt><dd>Deallocated or Unwritten Logical Block Error Enable，需 namespace DAE 支援。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.1.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.1.2, Figure 20, 文件頁 26, PDF 頁 26</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-022 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-022"><summary>NVM Figure 22 · Opcodes for NVM Commands</summary>
<!-- claim:NVMCS13-NVM-FIG-022-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.12">08.12.</span>Figure 22〈Opcodes for NVM Commands〉：Opcode 低兩 bits 指示資料傳輸方向；Copy 的 host-to-controller 是 descriptors。除特別註明的命令外，不能使用 broadcast NSID。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3, Figure 22, 文件頁 27, PDF 頁 27</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-097 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-097"><summary>Base Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</summary>
<!-- claim:NVMCS13-BASE-FIG-097-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.13">08.13.</span>Figure 97〈Common Completion Queue Entry Layout – Admin and All I/O Command Sets〉：CQE 的 command-specific result 與共同 queue／status 資訊各有位置；Copy DW0 與 Write Zeroes DW0 使用不同意義。</p><dl class="term-note" aria-label="本段名詞"><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 97, 文件頁 144, PDF 頁 170</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>SQID</dt><dd>Submission Queue Identifier，辨識 command 所屬 SQ 的數值。</dd></div><div><dt>CID</dt><dd>Command Identifier，與 SQ identifier 合用以辨識 outstanding command。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-BASE-FIG-098 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-098"><summary>Base Figure 98 · Completion Queue Entry: DW 2</summary>
<!-- claim:NVMCS13-BASE-FIG-098-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.14">08.14.</span>Figure 98〈Completion Queue Entry: DW 2〉：DW2 的 SQHD／SQID 回報對應 submission queue 資訊，不能當作此次命令已傳輸的 byte count。</p><dl class="term-note" aria-label="本段名詞"><div><dt>SQID</dt><dd>Submission Queue Identifier，辨識 command 所屬 SQ 的數值。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 98, 文件頁 144, PDF 頁 170</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-099 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-099"><summary>Base Figure 99 · Completion Queue Entry: DW 3</summary>
<!-- claim:NVMCS13-BASE-FIG-099-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.15">08.15.</span>Figure 99〈Completion Queue Entry: DW 3〉：DW3 以 CID 配回命令、Status 判定結果；command-specific DW0 不取代 status。</p><dl class="term-note" aria-label="本段名詞"><div><dt>CID</dt><dd>Command Identifier，與 SQ identifier 合用以辨識 outstanding command。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 99, 文件頁 145, PDF 頁 171</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-101 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-101"><summary>Base Figure 101 · Completion Queue Entry: Status Field</summary>
<!-- claim:NVMCS13-BASE-FIG-101-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.16">08.16.</span>Figure 101〈Completion Queue Entry: Status Field〉：Status 要一併解讀 SCT／SC，DNR 用於重試判斷，phase 用於辨識新 completion；它們回答不同問題。</p><dl class="term-note" aria-label="本段名詞"><div><dt>DNR</dt><dd>Do Not Retry，CQE status 中提示以相同 command 重試預期不會成功的 bit。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 101, 文件頁 145-146, PDF 頁 171-172</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>P</dt><dd>Phase Tag，讓 host 判斷 CQ slot 是否包含新 completion 的翻轉 bit。</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-read-write"><h2 id="heading-nvmcs-read-write"><span class="section-number">09</span> Read／Write 的資料與完成條件</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.01">09.01.</span>把範圍、buffer、PI 與完成狀態分成四項檢查，才能分辨資料位址錯誤、格式不符與真正的媒體失敗。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-READ-WRITE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.02">09.02.</span>Read／Write 以 SLBA 與 0-based NLB 指定連續範圍。Read 的 DPTR 是目的 buffer，Write 的 DPTR 是來源 buffer；FUA=1 要求使用 nonvolatile media，並沒有隱含其他命令的順序。</p><dl class="term-note" aria-label="本段名詞"><div><dt>SLBA</dt><dd>Starting LBA；指定命令範圍的起點。</dd></div><div><dt>FUA</dt><dd>Force Unit Access；要求 nonvolatile-media 語意，不自動建立其他命令的順序。</dd></div><div><dt>NLB</dt><dd>Number of Logical Blocks；本報告命令／status descriptors 的該欄為 0-based。DSM 的 LLB 另為1-based。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.4; 3.3.6</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4; 3.3.6, 文件頁 48-51,53-56, PDF 頁 48-51,53-56</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>CDW10 / CDW11</td><td>SLBA 低／高 32 bits</td><td>NLB=0 仍有一個 block</td></tr><tr><td>CDW12</td><td>LR、FUA、PRINFO、STC、CETYPE、NLB</td><td>Read 的 DTYPE 區是 reserved</td></tr><tr><td>CDW13</td><td>CETYPE 決定 DSM 或 CEV 解讀</td><td>Write 另含 DTYPE／DSPEC</td></tr><tr><td>MPTR</td><td>單獨傳 metadata 時使用</td><td>不可把一部分 metadata 分到兩種機制</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>CETYPE</dt><dd>Command Extension Type；選擇命令延伸欄位 CEV 的用途。</dd></div><div><dt>PRINFO</dt><dd>Protection Information；命令內的 PRACT 與 PRCHK 組合欄位。</dd></div><div><dt>DSPEC</dt><dd>Directive Specific；內容由 Directive 類型決定。</dd></div><div><dt>DTYPE</dt><dd>Directive Type；指定命令使用哪一類 Directive。</dd></div><div><dt>SLBA</dt><dd>Starting LBA；指定命令範圍的起點。</dd></div><div><dt>CDW</dt><dd>CDW（Command Dword）；命令中的 32-bit 欄位單位，例如 CDW10 的 10 是欄位 index，不是 byte offset。</dd></div><div><dt>CEV</dt><dd>Command Extension Value；內容依 CETYPE 的選擇解讀。</dd></div><div><dt>DSM</dt><dd>Dataset Management；由 host 提供資料範圍的使用與配置提示。</dd></div><div><dt>FUA</dt><dd>Force Unit Access；要求 nonvolatile-media 語意，不自動建立其他命令的順序。</dd></div><div><dt>NLB</dt><dd>Number of Logical Blocks；本報告命令／status descriptors 的該欄為 0-based。DSM 的 LLB 另為1-based。</dd></div><div><dt>STC</dt><dd>Storage Tag Check；獨立於三位元 PRCHK，STS=0 時忽略。</dd></div><div><dt>LR</dt><dd>Limited Retry；指定受 Error Recovery policy 約束的重試行為。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="09.03">09.03.</span>SLBA=100、NLB=7、LBADS=12 且無 metadata：讀取 100..107，共 32768 bytes。FUA Read 先使對應資料持久化，再取自媒體；仍需 host 保證相依 Write 的排序。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-050 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-050"><summary>NVM Figure 50 · Read – Metadata Pointer</summary>
<!-- claim:NVMCS13-NVM-FIG-050-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.04">09.04.</span>Figure 50〈Read – Metadata Pointer〉：MPTR 只在所選格式使用 separate metadata 時提供 metadata 位置；先核對 PSDT／metadata 格式，不能把它當成 user-data buffer。</p><dl class="term-note" aria-label="本段名詞"><div><dt>PSDT</dt><dd>PRP or SGL for Data Transfer，CDW0 中決定 DPTR 應按 PRP 或 SGL 解讀的欄位。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 50, 文件頁 49, PDF 頁 49</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-051 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-051"><summary>NVM Figure 51 · Read – Data Pointer</summary>
<!-- claim:NVMCS13-NVM-FIG-051-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.05">09.05.</span>Figure 51〈Read – Data Pointer〉：DPTR 是 controller 回傳資料的 host 目的位置；Read 回 data，Get LBA Status 回 descriptor list；兩者的回傳資料格式不同。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 51, 文件頁 49, PDF 頁 49</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-052 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-052"><summary>NVM Figure 52 · Read – Command Dword 2 and Dword 3</summary>
<!-- claim:NVMCS13-NVM-FIG-052-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.06">09.06.</span>Figure 52〈Read – Command Dword 2 and Dword 3〉：CDW2／3 的 upper tags 要和 CDW14 lower tags 合併，再依 PI 格式與 STS 拆成 expected storage／reference；unused bits 依格式忽略。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 52, 文件頁 49, PDF 頁 49</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>EILBRT</dt><dd>Initial Logical Block Reference Tag／expected 初值；Type 1／2 依 block 遞增並在欄位寬度處回捲。</dd></div><div><dt>ELBST</dt><dd>Logical Block Storage Tag／Expected Logical Block Storage Tag；寬度由 STS 決定。</dd></div><div><dt>ELBTL / ELBTU</dt><dd>Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-053 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-053"><summary>NVM Figure 53 · Read – Command Dword 10 and Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-053-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.07">09.07.</span>Figure 53〈Read – Command Dword 10 and Command Dword 11〉：64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 53, 文件頁 49, PDF 頁 49</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-054 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-054"><summary>NVM Figure 54 · Read – Command Dword 12</summary>
<!-- claim:NVMCS13-NVM-FIG-054-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.08">09.08.</span>Figure 54〈Read – Command Dword 12〉：CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。</p><dl class="term-note" aria-label="本段名詞"><div><dt>PRACT</dt><dd>Protection Information Action；依命令與 MS 選擇 PI 處理。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 54, 文件頁 49, PDF 頁 49</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CETYPE</dt><dd>Command Extension Type；選擇命令延伸欄位 CEV 的用途。</dd></div><div><dt>PRINFO</dt><dd>Protection Information；命令內的 PRACT 與 PRCHK 組合欄位。</dd></div><div><dt>STC</dt><dd>Storage Tag Check；獨立於三位元 PRCHK，STS=0 時忽略。</dd></div><div><dt>LR</dt><dd>Limited Retry；指定受 Error Recovery policy 約束的重試行為。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-055 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-055"><summary>NVM Figure 55 · Read – Command Dword 13 if CETYPE is cleared to 0h</summary>
<!-- claim:NVMCS13-NVM-FIG-055-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.09">09.09.</span>Figure 55〈Read – Command Dword 13 if CETYPE is cleared to 0h〉：Read 在 CETYPE=0 才用 CDW13 low8 提供 DSM hints；one-time／speculative read 是 access-frequency hints，不保證 controller 一定改變 cache 策略。</p><dl class="term-note" aria-label="本段名詞"><div><dt>DSM</dt><dd>Dataset Management；由 host 提供資料範圍的使用與配置提示。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 55, 文件頁 50, PDF 頁 50</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-056 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-056"><summary>NVM Figure 56 · Read - Command Dword 13 if CETYPE is non-zero</summary>
<!-- claim:NVMCS13-NVM-FIG-056-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.10">09.10.</span>Figure 56〈Read - Command Dword 13 if CETYPE is non-zero〉：CETYPE 非零時 CDW13 low16 解讀為 CEV；CETYPE=0 的 layout 另有定義或 reserved，不能同時塞 DSM hints。</p><dl class="term-note" aria-label="本段名詞"><div><dt>CEV</dt><dd>Command Extension Value；內容依 CETYPE 的選擇解讀。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 56, 文件頁 50, PDF 頁 50</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-057 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-057"><summary>NVM Figure 57 · Read – Command Dword 14</summary>
<!-- claim:NVMCS13-NVM-FIG-057-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.11">09.11.</span>Figure 57〈Read – Command Dword 14〉：CDW14 是 expected-tag 空間低 32 bits；它未必全是 Reference Tag，STS 可能占用其中高 bits。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 57, 文件頁 50, PDF 頁 50</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>ELBTL / ELBTU</dt><dd>Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-058 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-058"><summary>NVM Figure 58 · Read – Command Dword 15</summary>
<!-- claim:NVMCS13-NVM-FIG-058-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.12">09.12.</span>Figure 58〈Read – Command Dword 15〉：CDW15 high16 是 Application Tag mask，low16 是 expected tag；mask bit=0 表示不比較該位，不是要求 tag bit=0。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 58, 文件頁 51, PDF 頁 51</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>ELBATM</dt><dd>Tag comparison mask；bit=0 排除比較，Storage mask 額外受支援與對齊限制。</dd></div><div><dt>ELBAT</dt><dd>Logical Block Application Tag／expected tag；16-bit，checking 與 mask 及停用值規則共同決定。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-059 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-059"><summary>NVM Figure 59 · Read – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-059-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.13">09.13.</span>Figure 59〈Read – Command Specific Status Values〉：把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 59, 文件頁 51, PDF 頁 51</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-067 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-067"><summary>NVM Figure 67 · Write – Metadata Pointer</summary>
<!-- claim:NVMCS13-NVM-FIG-067-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.14">09.14.</span>Figure 67〈Write – Metadata Pointer〉：MPTR 只在所選格式使用 separate metadata 時提供 metadata 位置；先核對 PSDT／metadata 格式，不能把它當成 user-data buffer。</p><dl class="term-note" aria-label="本段名詞"><div><dt>PSDT</dt><dd>PRP or SGL for Data Transfer，CDW0 中決定 DPTR 應按 PRP 或 SGL 解讀的欄位。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.6</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 67, 文件頁 53, PDF 頁 53</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-068 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-068"><summary>NVM Figure 68 · Write – Data Pointer</summary>
<!-- claim:NVMCS13-NVM-FIG-068-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.15">09.15.</span>Figure 68〈Write – Data Pointer〉：這裡的 DPTR 指向 host 輸入資料：Compare 的 expected data 或 Write 的新資料；PRP／SGL 由 common command format 決定。</p><dl class="term-note" aria-label="本段名詞"><div><dt>PRP</dt><dd>Physical Region Page，以 memory page 為單位描述 host-addressable data buffer 的 pointer 格式。</dd></div><div><dt>SGL</dt><dd>Scatter Gather List，以 descriptor 與 segment 描述一段或多段 data buffer 的格式。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.6</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 68, 文件頁 54, PDF 頁 54</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-069 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-069"><summary>NVM Figure 69 · Write – Command Dword 2 and Dword 3</summary>
<!-- claim:NVMCS13-NVM-FIG-069-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.16">09.16.</span>Figure 69〈Write – Command Dword 2 and Dword 3〉：Upper／lower tag 欄位組成寫入端的 Storage 與初始 Reference Tag；Copy 的這組 command fields 屬於 destination，source expectations 在 descriptors。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.6</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 69, 文件頁 54, PDF 頁 54</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>ILBRT</dt><dd>Initial Logical Block Reference Tag／expected 初值；Type 1／2 依 block 遞增並在欄位寬度處回捲。</dd></div><div><dt>LBST</dt><dd>Logical Block Storage Tag／Expected Logical Block Storage Tag；寬度由 STS 決定。</dd></div><div><dt>LBTL / LBTU</dt><dd>Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-070 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-070"><summary>NVM Figure 70 · Write – Command Dword 10 and Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-070-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.17">09.17.</span>Figure 70〈Write – Command Dword 10 and Command Dword 11〉：64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.6</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 70, 文件頁 54, PDF 頁 54</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-071 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-071"><summary>NVM Figure 71 · Write – Command Dword 12</summary>
<!-- claim:NVMCS13-NVM-FIG-071-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.18">09.18.</span>Figure 71〈Write – Command Dword 12〉：CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.6</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 71, 文件頁 54, PDF 頁 54</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-072 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-072"><summary>NVM Figure 72 · Write – Command Dword 13 if CETYPE is cleared to 0h</summary>
<!-- claim:NVMCS13-NVM-FIG-072-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.19">09.19.</span>Figure 72〈Write – Command Dword 13 if CETYPE is cleared to 0h〉：Write 的 CETYPE=0 layout 包含 high16 DSPEC 與 low8 DSM；不要與 CETYPE 非零的 CEV layout 混寫。</p><dl class="term-note" aria-label="本段名詞"><div><dt>DSPEC</dt><dd>Directive Specific；內容由 Directive 類型決定。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.6</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 72, 文件頁 54-55, PDF 頁 54-55</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-073 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-073"><summary>NVM Figure 73 · Write - Command Dword 13 if CETYPE is non-zero</summary>
<!-- claim:NVMCS13-NVM-FIG-073-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.20">09.20.</span>Figure 73〈Write - Command Dword 13 if CETYPE is non-zero〉：CDW13 high16 保存 Directive Specific，low16 依 CETYPE 保存 CEV；Directive 與 command extension 是獨立欄位。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.6</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 73, 文件頁 55, PDF 頁 55</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-074 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-074"><summary>NVM Figure 74 · Write – Command Dword 14</summary>
<!-- claim:NVMCS13-NVM-FIG-074-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.21">09.21.</span>Figure 74〈Write – Command Dword 14〉：CDW14 提供寫入 tags 的低 32 bits；依 STS 將 space 分割，不能把高位 Storage Tag 全部丟棄。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.6</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 74, 文件頁 55, PDF 頁 55</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>ILBRT</dt><dd>Initial Logical Block Reference Tag／expected 初值；Type 1／2 依 block 遞增並在欄位寬度處回捲。</dd></div><div><dt>LBST</dt><dd>Logical Block Storage Tag／Expected Logical Block Storage Tag；寬度由 STS 決定。</dd></div><div><dt>LBTL</dt><dd>Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-075 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-075"><summary>NVM Figure 75 · Write – Command Dword 15</summary>
<!-- claim:NVMCS13-NVM-FIG-075-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.22">09.22.</span>Figure 75〈Write – Command Dword 15〉：Application Tag mask 與 tag 分別在 CDW15 high16／low16；Copy 使用於寫入目的端，來源端有獨立 expected 欄位。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.6</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 75, 文件頁 55, PDF 頁 55</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>LBATM</dt><dd>Tag comparison mask；bit=0 排除比較，Storage mask 額外受支援與對齊限制。</dd></div><div><dt>LBAT</dt><dd>Logical Block Application Tag／expected tag；16-bit，checking 與 mask 及停用值規則共同決定。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-076 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-076"><summary>NVM Figure 76 · Write – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-076-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.23">09.23.</span>Figure 76〈Write – Command Specific Status Values〉：把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.6</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 76, 文件頁 56, PDF 頁 56</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-093 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-093"><summary>Base Figure 93 · Common Command Format</summary>
<!-- claim:NVMCS13-BASE-FIG-093-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.24">09.24.</span>Figure 93〈Common Command Format〉：Common SQE 將 namespace、data pointers 與 command-specific Dwords 分開；NVM 章節只補充相應 command fields。</p><dl class="term-note" aria-label="本段名詞"><div><dt>SQE</dt><dd>Submission Queue Entry，SQ 中的一筆命令資料結構。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §4.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, 文件頁 140-142, PDF 頁 166-168</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-110 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-110"><summary>Base Figure 110 · PRP Entry Layout</summary>
<!-- claim:NVMCS13-BASE-FIG-110-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.25">09.25.</span>Figure 110〈PRP Entry Layout〉：PRP layout 包含頁基址與首筆 offset；NVM payload 可能是 data 或 descriptor list，不能由 pointer 類型推定內容。</p><details class="source-note"><summary>來源：Base 2.4 §4.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 110, 文件頁 158, PDF 頁 184</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-111 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-111"><summary>Base Figure 111 · PRP Entry – Page Base Address and Offset</summary>
<!-- claim:NVMCS13-BASE-FIG-111-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.26">09.26.</span>Figure 111〈PRP Entry – Page Base Address and Offset〉：頁大小決定 base／offset 切分。計算第一頁剩餘空間後才決定後續 PRP pages。</p><details class="source-note"><summary>來源：Base 2.4 §4.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 111, 文件頁 158, PDF 頁 184</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-116 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-116"><summary>Base Figure 116 · Generic SGL Descriptor Format</summary>
<!-- claim:NVMCS13-BASE-FIG-116-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.27">09.27.</span>Figure 116〈Generic SGL Descriptor Format〉：本機 SGL descriptor 用 address、length 與 type 描述 buffer。</p><details class="source-note"><summary>來源：Base 2.4 §4.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 116, 文件頁 161, PDF 頁 187</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-order-fused"><h2 id="heading-nvmcs-order-fused"><span class="section-number">10</span> 命令順序與 Compare-and-Write</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="10.01">10.01.</span>先說明何時要排序，再判斷是否需要條件式更新。Fused 保護同一 LBA range 的比對與更新，原子大小仍須另外檢查。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-ORDER-FUSED -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="10.02">10.02.</span>一般命令不因同在一個 SQ 就取得 LBA 相依順序；host 必須建立必要順序。Fused Compare-and-Write 先比對，成功才寫入；Compare 失敗則 Write 以 Failed Fused Command 類別中止。</p><dl class="term-note" aria-label="本段名詞"><div><dt>SQ</dt><dd>Submission Queue，主機放入命令的提交佇列。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.1.2-2.1.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.2-2.1.3, 文件頁 14-15, PDF 頁 14-15</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>Ordinary I/O</td><td>同 LBA 的 Read／Write 完成先後無保證</td><td>host 以完成相依控制</td></tr><tr><td>Fused pair</td><td>Compare 與 Write 的 range 相同</td><td>範圍不符 should 拒絕</td></tr><tr><td>ACWU / NACWU</td><td>限制 fused atomic update 大小</td><td>還要遵守 atomic boundaries</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>NACWU</dt><dd>Namespace Atomic Compare and Write Unit；namespace 的 fused compare-and-write 大小限制。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="10.03">10.03.</span>Host 想「目前值等於 A 才更新 B」時，獨立 Compare 成功後再送 Write 中間仍可能插入別人的寫入；符合大小與邊界的 fused pair 才提供此操作所需的條件式原子更新。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-003 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-003"><summary>NVM Figure 3 · Supported Fused Operations</summary>
<!-- claim:NVMCS13-NVM-FIG-003-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="10.04">10.04.</span>Figure 3〈Supported Fused Operations〉：先 Compare 成功才執行同 range 的 Write；兩個 CQE 分別表示比對與寫入結果，並須檢查 fused atomicity limits。</p><dl class="term-note" aria-label="本段名詞"><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.1.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.3, Figure 3, 文件頁 14, PDF 頁 14</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-atomic"><h2 id="heading-nvmcs-atomic"><span class="section-number">11</span> 正常、斷電與多段原子性</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.01">11.01.</span>把大小、起始對齊、NSABP 與 MAM 一起讀。Atomicity 與資料已進入 nonvolatile media 是不同檢查項目，FUA／Flush 也不建立其他命令的排序。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NSABP</dt><dd>Namespace Atomic Boundary Parameters；表示 namespace 的原子寫入參數是否適用。</dd></div><div><dt>MAM</dt><dd>Multiple Atomicity Mode；跨 boundary 的命令分成各自原子的 subranges。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-ATOMIC -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.02">11.02.</span>AWUN／NAWUN 與 AWUPF／NAWUPF 分別描述正常及失敗條件原子性。Single Atomicity Mode 跨 boundary 不保證整筆原子；Multiple Atomicity Mode 在每個 boundary 切成各自原子的 subranges，並不承諾整筆一起成功。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NAWUPF</dt><dd>Namespace Atomic Write Unit Power Fail；namespace 失敗條件的原子寫入大小；依適用與零值規則判讀。</dd></div><div><dt>NAWUN</dt><dd>Namespace Atomic Write Unit Normal；namespace 正常情況原子寫入大小；依適用與零值規則判讀。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.1.4; 4.1.3.4; 5.9</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4; 4.1.3.4; 5.9, 文件頁 15-21,66-67,165, PDF 頁 15-21,66-67,165</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>AWUN / AWUPF</td><td>大小採 0-based 編碼</td><td>AWUPF 不大於 AWUN</td></tr><tr><td>NABO / NABSN / NABSPF</td><td>邊界在 offset + k × size</td><td>需依各欄位換算與未回報規則</td></tr><tr><td>MAM</td><td>每個 atomic subrange 獨立保證</td><td>fused 仍用 Single 模式</td></tr><tr><td>FID 0Ah.DN</td><td>DN=1 可不遵守 normal atomicity</td><td>仍須遵守 power-fail 保證</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>NABSPF</dt><dd>Namespace Atomic Boundary Size Power Fail；失敗條件的原子邊界大小。</dd></div><div><dt>NABSN</dt><dd>Namespace Atomic Boundary Size Normal；正常情況的原子邊界大小。</dd></div><div><dt>NABO</dt><dd>Namespace Atomic Boundary Offset；決定第一個 boundary 的位置。</dd></div><div><dt>MAM</dt><dd>Multiple Atomicity Mode；跨 boundary 的命令分成各自原子的 subranges。</dd></div><div><dt>DN</dt><dd>Write Atomicity Normal 的 Disable Normal；不免除 power-fail atomicity。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="11.03">11.03.</span>假設依欄位換算後 boundary size=8 blocks、offset=0，從 LBA 4 寫 12 blocks 跨成 [4..7] 與 [8..15]。MAM 下各段原子，不能將兩段當作一個 transaction。原始 AWUN=7h 才代表 8 blocks。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-004 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-004"><summary>NVM Figure 4 · Atomicity Parameters for Single Atomicity Mode</summary>
<!-- claim:NVMCS13-NVM-FIG-004-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.04">11.04.</span>Figure 4〈Atomicity Parameters for Single Atomicity Mode〉：先用 NSABP 選 controller 或 namespace 值，再依欄位換算 0-based 大小及 namespace 的零值繼承規則；不可把每個 raw 0 都解釋成一個 block。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NSABP</dt><dd>Namespace Atomic Boundary Parameters；表示 namespace 的原子寫入參數是否適用。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 4, 文件頁 15-16, PDF 頁 15-16</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NABSPF</dt><dd>Namespace Atomic Boundary Size Power Fail；失敗條件的原子邊界大小。</dd></div><div><dt>NAWUPF</dt><dd>Namespace Atomic Write Unit Power Fail；namespace 失敗條件的原子寫入大小；依適用與零值規則判讀。</dd></div><div><dt>NABSN</dt><dd>Namespace Atomic Boundary Size Normal；正常情況的原子邊界大小。</dd></div><div><dt>NACWU</dt><dd>Namespace Atomic Compare and Write Unit；namespace 的 fused compare-and-write 大小限制。</dd></div><div><dt>NAWUN</dt><dd>Namespace Atomic Write Unit Normal；namespace 正常情況原子寫入大小；依適用與零值規則判讀。</dd></div><div><dt>NABO</dt><dd>Namespace Atomic Boundary Offset；決定第一個 boundary 的位置。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-005 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-005"><summary>NVM Figure 5 · AWUN/NAWUN Example Results</summary>
<!-- claim:NVMCS13-NVM-FIG-005-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.05">11.05.</span>Figure 5〈AWUN/NAWUN Example Results〉：本圖討論正常運作下重疊寫入的可觀測結果；將 write size 與依欄位換算後 AWUN 比較，再看讀取是否落在相同 atomic unit。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 5, 文件頁 17, PDF 頁 17</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-006 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-006"><summary>NVM Figure 6 · AWUPF/NAWUPF Example Initial State of NVM</summary>
<!-- claim:NVMCS13-NVM-FIG-006-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.06">11.06.</span>Figure 6〈AWUPF/NAWUPF Example Initial State of NVM〉：先保存失敗前的媒體內容與此次 write 範圍，這個 initial state 是下一張 failure-result 表的前提。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 6, 文件頁 18, PDF 頁 18</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-007 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-007"><summary>NVM Figure 7 · AWUPF/NAWUPF Example Final State of NVM</summary>
<!-- claim:NVMCS13-NVM-FIG-007-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.07">11.07.</span>Figure 7〈AWUPF/NAWUPF Example Final State of NVM〉：把 power-fail 原子大小內的舊資料保留保證，與超過大小時可能 torn write 的結果分開；未完成寫入不能當作全新資料。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 7, 文件頁 18, PDF 頁 18</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-008 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-008"><summary>NVM Figure 8 · Atomic Boundaries Example</summary>
<!-- claim:NVMCS13-NVM-FIG-008-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.08">11.08.</span>Figure 8〈Atomic Boundaries Example〉：在數線標出 offset+k×boundary size；長度小於 atomic size 仍可能因起點而跨 boundary。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 8, 文件頁 19, PDF 頁 19</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-009 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-009"><summary>NVM Figure 9 · Atomicity Parameter Differences for Multiple Atomicity Mode</summary>
<!-- claim:NVMCS13-NVM-FIG-009-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.09">11.09.</span>Figure 9〈Atomicity Parameter Differences for Multiple Atomicity Mode〉：Multiple 模式將適用 normal／power-fail size 與兩種 boundary size 對齊成相同值；fused 比對寫入仍遵守 Single 模式。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 9, 文件頁 20, PDF 頁 20</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-010 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-010"><summary>NVM Figure 10 · Multiple Atomicity Example</summary>
<!-- claim:NVMCS13-NVM-FIG-010-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.10">11.10.</span>Figure 10〈Multiple Atomicity Example〉：Single 模式要分開的 A/B/C，在 Multiple 模式可由 D 覆蓋，但保證仍以每個切出的 subrange 為單位，不是 D 整體 transaction。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 10, 文件頁 21, PDF 頁 21</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-compare-verify"><h2 id="heading-nvmcs-compare-verify"><span class="section-number">12</span> Compare 與 Verify 解決不同問題</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.01">12.01.</span>比對預期內容、驗證完整性與一般 Read 三者的證據不同。Compare 的 metadata 比對排除 PI；PI 另依要求的 checking 執行。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-COMPARE-VERIFY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.02">12.02.</span>Compare 比較媒體資料與 host 提供的 buffer；Verify 檢查已儲存資料完整性而不把資料或 metadata 回傳 host。兩者要求 PRACT=0；Verify 與 Read 偵測到的失敗不必使用相同錯誤碼。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.1; 3.3.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1; 3.3.5, 文件頁 27-30,51-53, PDF 頁 27-30,51-53</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>Compare</td><td>miscompare 回 Compare Failure</td><td>host 與 media 兩側 PI 可分別檢查</td></tr><tr><td>Verify</td><td>沒有資料 buffer 傳輸</td><td>驗證量仍計入 Data Units Read</td></tr><tr><td>VSL / NVMVFYS</td><td>variant 決定建議大小或硬上限</td><td>非零 VSL 以 2^n × minimum page size 表示</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="12.03">12.03.</span>要知道儲存內容是否等於全零，Compare 可提供預期全零 buffer；Verify 成功只能證明此次完整性檢查成功，不能證明內容是全零。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-023 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-023"><summary>NVM Figure 23 · Compare – Metadata Pointer</summary>
<!-- claim:NVMCS13-NVM-FIG-023-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.04">12.04.</span>Figure 23〈Compare – Metadata Pointer〉：MPTR 只在所選格式使用 separate metadata 時提供 metadata 位置；先核對 PSDT／metadata 格式，不能把它當成 user-data buffer。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 23, 文件頁 28, PDF 頁 28</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-024 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-024"><summary>NVM Figure 24 · Compare – Data Pointer</summary>
<!-- claim:NVMCS13-NVM-FIG-024-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.05">12.05.</span>Figure 24〈Compare – Data Pointer〉：這裡的 DPTR 指向 host 輸入資料：Compare 的 expected data 或 Write 的新資料；PRP／SGL 由 common command format 決定。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 24, 文件頁 28, PDF 頁 28</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-025 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-025"><summary>NVM Figure 25 · Compare – Command Dword 2 and Dword 3</summary>
<!-- claim:NVMCS13-NVM-FIG-025-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.06">12.06.</span>Figure 25〈Compare – Command Dword 2 and Dword 3〉：CDW2／3 的 upper tags 要和 CDW14 lower tags 合併，再依 PI 格式與 STS 拆成 expected storage／reference；unused bits 依格式忽略。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 25, 文件頁 28, PDF 頁 28</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>EILBRT</dt><dd>Initial Logical Block Reference Tag／expected 初值；Type 1／2 依 block 遞增並在欄位寬度處回捲。</dd></div><div><dt>ELBST</dt><dd>Logical Block Storage Tag／Expected Logical Block Storage Tag；寬度由 STS 決定。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-026 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-026"><summary>NVM Figure 26 · Compare – Command Dword 10 and Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-026-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.07">12.07.</span>Figure 26〈Compare – Command Dword 10 and Command Dword 11〉：64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 26, 文件頁 28, PDF 頁 28</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-027 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-027"><summary>NVM Figure 27 · Compare – Command Dword 12</summary>
<!-- claim:NVMCS13-NVM-FIG-027-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.08">12.08.</span>Figure 27〈Compare – Command Dword 12〉：CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 27, 文件頁 28-29, PDF 頁 28-29</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-028 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-028"><summary>NVM Figure 28 · Compare - Command Dword 13 if CETYPE is non-zero</summary>
<!-- claim:NVMCS13-NVM-FIG-028-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.09">12.09.</span>Figure 28〈Compare - Command Dword 13 if CETYPE is non-zero〉：CETYPE 非零時 CDW13 low16 解讀為 CEV；CETYPE=0 的 layout 另有定義或 reserved，不能同時塞 DSM hints。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 28, 文件頁 29, PDF 頁 29</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-029 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-029"><summary>NVM Figure 29 · Compare – Command Dword 14</summary>
<!-- claim:NVMCS13-NVM-FIG-029-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.10">12.10.</span>Figure 29〈Compare – Command Dword 14〉：CDW14 是 expected-tag 空間低 32 bits；它未必全是 Reference Tag，STS 可能占用其中高 bits。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 29, 文件頁 29, PDF 頁 29</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-030 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-030"><summary>NVM Figure 30 · Compare – Command Dword 15</summary>
<!-- claim:NVMCS13-NVM-FIG-030-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.11">12.11.</span>Figure 30〈Compare – Command Dword 15〉：CDW15 high16 是 Application Tag mask，low16 是 expected tag；mask bit=0 表示不比較該位，不是要求 tag bit=0。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 30, 文件頁 29, PDF 頁 29</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>ELBATM</dt><dd>Tag comparison mask；bit=0 排除比較，Storage mask 額外受支援與對齊限制。</dd></div><div><dt>ELBAT</dt><dd>Logical Block Application Tag／expected tag；16-bit，checking 與 mask 及停用值規則共同決定。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-031 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-031"><summary>NVM Figure 31 · Compare – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-031-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.12">12.12.</span>Figure 31〈Compare – Command Specific Status Values〉：把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 31, 文件頁 30, PDF 頁 30</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-060 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-060"><summary>NVM Figure 60 · Verify – Command Dword 2 and Dword 3</summary>
<!-- claim:NVMCS13-NVM-FIG-060-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.13">12.13.</span>Figure 60〈Verify – Command Dword 2 and Dword 3〉：CDW2／3 的 upper tags 要和 CDW14 lower tags 合併，再依 PI 格式與 STS 拆成 expected storage／reference；unused bits 依格式忽略。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 60, 文件頁 52, PDF 頁 52</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-061 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-061"><summary>NVM Figure 61 · Verify – Command Dword 10 and Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-061-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.14">12.14.</span>Figure 61〈Verify – Command Dword 10 and Command Dword 11〉：64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 61, 文件頁 52, PDF 頁 52</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-062 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-062"><summary>NVM Figure 62 · Verify – Command Dword 12</summary>
<!-- claim:NVMCS13-NVM-FIG-062-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.15">12.15.</span>Figure 62〈Verify – Command Dword 12〉：CDW12 合併行為 bits 與 0-based NLB；Compare／Verify 要 PRACT=0，Read／Write 才依 metadata 格式選 PRACT。FUA 不建立其他命令順序。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 62, 文件頁 52, PDF 頁 52</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-063 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-063"><summary>NVM Figure 63 · Verify - Command Dword 13 if CETYPE is non-zero</summary>
<!-- claim:NVMCS13-NVM-FIG-063-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.16">12.16.</span>Figure 63〈Verify - Command Dword 13 if CETYPE is non-zero〉：CETYPE 非零時 CDW13 low16 解讀為 CEV；CETYPE=0 的 layout 另有定義或 reserved，不能同時塞 DSM hints。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 63, 文件頁 52, PDF 頁 52</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-064 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-064"><summary>NVM Figure 64 · Verify – Command Dword 14</summary>
<!-- claim:NVMCS13-NVM-FIG-064-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.17">12.17.</span>Figure 64〈Verify – Command Dword 14〉：CDW14 是 expected-tag 空間低 32 bits；它未必全是 Reference Tag，STS 可能占用其中高 bits。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 64, 文件頁 53, PDF 頁 53</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-065 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-065"><summary>NVM Figure 65 · Verify – Command Dword 15</summary>
<!-- claim:NVMCS13-NVM-FIG-065-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.18">12.18.</span>Figure 65〈Verify – Command Dword 15〉：CDW15 high16 是 Application Tag mask，low16 是 expected tag；mask bit=0 表示不比較該位，不是要求 tag bit=0。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 65, 文件頁 53, PDF 頁 53</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-066 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-066"><summary>NVM Figure 66 · Verify – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-066-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.19">12.19.</span>Figure 66〈Verify – Command Specific Status Values〉：把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 66, 文件頁 53, PDF 頁 53</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-copy"><h2 id="heading-nvmcs-copy"><span class="section-number">13</span> Copy：描述來源、連續目的與部分失敗</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.01">13.01.</span>先計算展開後的目的區間，再檢查格式、長度限制、重疊與 atomicity。Copy 可少用 host 資料傳輸，但不是無條件的 transaction。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-COPY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.02">13.02.</span>Copy 把一個或多個 source ranges 依 descriptor 順序接成單一連續目的範圍。Format 0h/1h 來源與目的在同一 namespace；2h/3h 帶 SNSID，需 controller 支援與 host 啟用。失敗 CQE DW0 是最低未成功 source index，後面的 ranges 仍可能已複製。</p><dl class="term-note" aria-label="本段名詞"><div><dt>SNSID</dt><dd>Source Namespace Identifier；指定 Copy 的來源 namespace。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, 文件頁 30-44, PDF 頁 30-44</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>NR / NLB</td><td>source count 與各範圍 block count 都是 0-based</td><td>檢查 MSRC、MSSRL、MCL</td></tr><tr><td>FCO</td><td>2h/3h 可要求 fast copy only</td><td>Fast Copy Not Possible 再看 DNR</td></tr><tr><td>Overlap</td><td>2h/3h 禁止同 namespace source 與 destination 重疊</td><td>0h/1h 重疊結果需依原子條件另讀</td></tr><tr><td>NVMCSA</td><td>1.3 將目的寫入視為單一 write command</td><td>仍受 MAM、大小及 boundary 限制</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>FCO</dt><dd>Fast Copy Only；要求適用來源以 fast copy 方法執行。</dd></div><div><dt>NR</dt><dd>Range count 的 0-based 欄位；實際 descriptors 數為 NR+1。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="13.03">13.03.</span>兩個 source descriptors 的 NLB 都是 3，SDLBA=100：第一段寫 100..103、第二段寫 104..107，共 8 blocks。若 DW0=1，不能據此保證第二段或更後面完全未修改。</p><dl class="term-note" aria-label="本段名詞"><div><dt>SDLBA</dt><dd>Starting Destination LBA；指定 Copy 連續目的範圍的起點。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-032 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-032"><summary>NVM Figure 32 · Copy – Data Pointer</summary>
<!-- claim:NVMCS13-NVM-FIG-032-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.04">13.04.</span>Figure 32〈Copy – Data Pointer〉：DPTR 指向 descriptors，而不是待複製或 deallocate 的 user data；buffer 長度需由 descriptor size 與依欄位換算後 range count 計算。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 32, 文件頁 30, PDF 頁 30</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-033 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-033"><summary>NVM Figure 33 · Copy – Command Dword 2 and Dword 3</summary>
<!-- claim:NVMCS13-NVM-FIG-033-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.05">13.05.</span>Figure 33〈Copy – Command Dword 2 and Dword 3〉：Upper／lower tag 欄位組成寫入端的 Storage 與初始 Reference Tag；Copy 的這組 command fields 屬於 destination，source expectations 在 descriptors。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 33, 文件頁 30, PDF 頁 30</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>LBTU</dt><dd>Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-034 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-034"><summary>NVM Figure 34 · Copy – Command Dword 10 and Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-034-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.06">13.06.</span>Figure 34〈Copy – Command Dword 10 and Command Dword 11〉：SDLBA 指第一個 destination block，後續來源按 descriptor 順序連接；它不會為每個 source range 重新歸零。</p><dl class="term-note" aria-label="本段名詞"><div><dt>SDLBA</dt><dd>Starting Destination LBA；指定 Copy 連續目的範圍的起點。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 34, 文件頁 30, PDF 頁 30</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-035 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-035"><summary>NVM Figure 35 · Copy – Command Dword 12</summary>
<!-- claim:NVMCS13-NVM-FIG-035-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.07">13.07.</span>Figure 35〈Copy – Command Dword 12〉：Copy 在同一 CDW12 分開讀端／寫端 PI、descriptor format 與 0-based range count。STCRS 的正確能力定義在 Figure 127；本圖指 Figure 115 的文字引用錯置。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 35, 文件頁 30-31, PDF 頁 30-31</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>PRINFOR</dt><dd>Protection Information Read；Copy 讀取端的 PI 處理與檢查欄位。</dd></div><div><dt>PRINFOW</dt><dd>Protection Information Write；Copy 寫入端的 PI 處理與檢查欄位。</dd></div><div><dt>DESFMT</dt><dd>Copy Source Range Entry 格式 selector；同時影響 descriptor 大小、來源 NSID 與 PI tag layout。</dd></div><div><dt>STCR</dt><dd>Storage Tag Check Read；要求 Copy 讀取端的 Storage Tag 檢查。</dd></div><div><dt>STCW</dt><dd>Storage Tag Check Write；要求 Copy 寫入端的 Storage Tag 檢查。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-036 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-036"><summary>NVM Figure 36 · Copy – Command Dword 13</summary>
<!-- claim:NVMCS13-NVM-FIG-036-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.08">13.08.</span>Figure 36〈Copy – Command Dword 13〉：CDW13 high16 保存 Directive Specific，low16 依 CETYPE 保存 CEV；Directive 與 command extension 是獨立欄位。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 36, 文件頁 31, PDF 頁 31</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-037 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-037"><summary>NVM Figure 37 · Copy – Command Dword 14</summary>
<!-- claim:NVMCS13-NVM-FIG-037-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.09">13.09.</span>Figure 37〈Copy – Command Dword 14〉：CDW14 提供寫入 tags 的低 32 bits；依 STS 將 space 分割，不能把高位 Storage Tag 全部丟棄。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 37, 文件頁 31, PDF 頁 31</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-038 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-038"><summary>NVM Figure 38 · Copy – Command Dword 15</summary>
<!-- claim:NVMCS13-NVM-FIG-038-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.10">13.10.</span>Figure 38〈Copy – Command Dword 15〉：Application Tag mask 與 tag 分別在 CDW15 high16／low16；Copy 使用於寫入目的端，來源端有獨立 expected 欄位。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 38, 文件頁 32, PDF 頁 32</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>LBATM</dt><dd>Tag comparison mask；bit=0 排除比較，Storage mask 額外受支援與對齊限制。</dd></div><div><dt>LBAT</dt><dd>Logical Block Application Tag／expected tag；16-bit，checking 與 mask 及停用值規則共同決定。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-039 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-039"><summary>NVM Figure 39 · Copy – Copy Descriptor Formats</summary>
<!-- claim:NVMCS13-NVM-FIG-039-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.11">13.11.</span>Figure 39〈Copy – Copy Descriptor Formats〉：0h/2h 搭配 8-byte PI、1h/3h 搭配 16-byte PI；2h/3h 有 SNSID。4h 指向另一 command set 的 Memory Copy 定義，這份 NVM 文件沒有其完整 descriptor layout。</p><dl class="term-note" aria-label="本段名詞"><div><dt>SNSID</dt><dd>Source Namespace Identifier；指定 Copy 的來源 namespace。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 39, 文件頁 32, PDF 頁 32</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>DESFMT</dt><dd>Copy Source Range Entry 格式 selector；同時影響 descriptor 大小、來源 NSID 與 PI tag layout。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-040 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-040"><summary>NVM Figure 40 · Copy – Source Range Entries Copy Descriptor Format 0h and Format 2h</summary>
<!-- claim:NVMCS13-NVM-FIG-040-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.12">13.12.</span>Figure 40〈Copy – Source Range Entries Copy Descriptor Format 0h and Format 2h〉：0h/2h 每個 source entry 32 bytes；0h 的 SNSID／FCO 位置 reserved，2h 可使用。NLB 先加一，再累加至 destination length。</p><dl class="term-note" aria-label="本段名詞"><div><dt>FCO</dt><dd>Fast Copy Only；要求適用來源以 fast copy 方法執行。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 40, 文件頁 33-34, PDF 頁 33-34</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>ELBT</dt><dd>Logical Block Tags／expected tags 的上／下部分；依 Guard 格式、STS 與 Dword 位置組合。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-041 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-041"><summary>NVM Figure 41 · Copy – Source Range Entries Copy Descriptor Format 1h and Format 3h</summary>
<!-- claim:NVMCS13-NVM-FIG-041-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.13">13.13.</span>Figure 41〈Copy – Source Range Entries Copy Descriptor Format 1h and Format 3h〉：1h/3h 每個 source entry 40 bytes，以較大的 tags 支援 16-byte PI；3h 帶 SNSID／FCO，不能用 32-byte stride 解析。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 41, 文件頁 35-36, PDF 頁 35-36</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-042 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-042"><summary>NVM Figure 42 · Source LBA and Destination LBA Relationship Example</summary>
<!-- claim:NVMCS13-NVM-FIG-042-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.14">13.14.</span>Figure 42〈Source LBA and Destination LBA Relationship Example〉：依 source descriptor 順序把各段長度相加，產生連續 destination；圖中的加總是 block 數，不能直接累加 raw NLB 而漏掉每段的一。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 42, 文件頁 38, PDF 頁 38</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-043 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-043"><summary>NVM Figure 43 · Copy – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-043-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.15">13.15.</span>Figure 43〈Copy – Command Specific Status Values〉：Copy 錯誤要合看 CQE DW0 的最低失敗 source index；後續 entries 可能已處理，不能假設回滾。FCO 失敗再依 DNR 判斷重試。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 43, 文件頁 43-44, PDF 頁 43-44</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-491 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-491"><summary>Base Figure 491 · Host Behavior Support – Data Structure</summary>
<!-- claim:NVMCS13-BASE-FIG-491-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.16">13.16.</span>Figure 491〈Host Behavior Support – Data Structure〉：Host Behavior Support 的 CFD2E／CFD3E 宣告 host 接受 Copy formats2h／3h；controller CDF support 與 host enablement 是兩項門檻。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.30.1.15</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.15, Figure 491, 文件頁 476-477, PDF 頁 502-503</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-copy-pi"><h2 id="heading-nvmcs-copy-pi"><span class="section-number">14</span> Copy 的 PI 格式相容與轉換</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="14.01">14.01.</span>以來源與目的是否有 PI 建立四種情況，再決定 PRINFOR.PRACT 與 PRINFOW.PRACT。每個 source 都必須符合選定模式。</p><dl class="term-note" aria-label="本段名詞"><div><dt>PRINFOR</dt><dd>Protection Information Read；Copy 讀取端的 PI 處理與檢查欄位。</dd></div><div><dt>PRINFOW</dt><dd>Protection Information Write；Copy 寫入端的 PI 處理與檢查欄位。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-COPY-PI -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="14.02">14.02.</span>Copy 的 matching formats 要比對資料大小、metadata 大小、DPS、PIFA、有效 LBSTM、PIF／QPIF 與 STS。Corresponding PI formats 只容許有 PI 的一方 metadata 全為 PI，另一方完全沒有 metadata；不能拿 Copy 任意轉換資料格式。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.2.3-3.3.2.4; 5.3.2.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2.3-3.3.2.4; 5.3.2.5, 文件頁 40-43,146-150, PDF 頁 40-43,146-150</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>PI → PI, 0/0</td><td>matching formats：pass-through</td><td>保護檢查仍由 checking bits 控制</td></tr><tr><td>PI → PI, 1/1</td><td>matching formats：replace</td><td>讀端檢查，寫端產生 PI</td></tr><tr><td>No PI → PI</td><td>corresponding formats 且 write PRACT=1：insert</td><td>目的 metadata 不得包含其他用途</td></tr><tr><td>PI → No PI</td><td>corresponding formats 且 read PRACT=1：strip</td><td>來源 metadata 只能是 PI</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="14.03">14.03.</span>4096+8 bytes 的 16b PI namespace 可在符合 corresponding 條件時轉到 4096+0 bytes；4096+16 bytes 且其中 8 bytes 是額外 metadata，不能走這個 strip 特例。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-177 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-177"><summary>NVM Figure 177 · PI Processing for Copy MD=8 Pass-through</summary>
<!-- claim:NVMCS13-NVM-FIG-177-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="14.04">14.04.</span>Figure 177〈PI Processing for Copy MD=8 Pass-through〉：這兩圖是 matching PI formats 的 pass-through：讀／寫 PRACT 都為0；metadata 大小不同的兩個例子仍須保留各自 layout。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.2.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.5, Figure 177, 文件頁 147, PDF 頁 147</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-178 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-178"><summary>NVM Figure 178 · PI Processing for Copy MD=16 Pass-through</summary>
<!-- claim:NVMCS13-NVM-FIG-178-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="14.05">14.05.</span>Figure 178〈PI Processing for Copy MD=16 Pass-through〉：這兩圖是 matching PI formats 的 pass-through：讀／寫 PRACT 都為0；metadata 大小不同的兩個例子仍須保留各自 layout。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.2.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.5, Figure 178, 文件頁 147, PDF 頁 147</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-179 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-179"><summary>NVM Figure 179 · PI Processing for Copy MD=8 Replace</summary>
<!-- claim:NVMCS13-NVM-FIG-179-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="14.06">14.06.</span>Figure 179〈PI Processing for Copy MD=8 Replace〉：這兩圖是 matching PI formats 的 replace：讀／寫 PRACT 都為1；來源 PI 檢查與目的 PI 產生有不同角色。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.2.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.5, Figure 179, 文件頁 148, PDF 頁 148</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-180 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-180"><summary>NVM Figure 180 · PI Processing for Copy MD=16 Replace</summary>
<!-- claim:NVMCS13-NVM-FIG-180-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="14.07">14.07.</span>Figure 180〈PI Processing for Copy MD=16 Replace〉：這兩圖是 matching PI formats 的 replace：讀／寫 PRACT 都為1；來源 PI 檢查與目的 PI 產生有不同角色。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.2.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.5, Figure 180, 文件頁 148, PDF 頁 148</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-181 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-181"><summary>NVM Figure 181 · PI Processing for Copy MD=8 Insert</summary>
<!-- claim:NVMCS13-NVM-FIG-181-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="14.08">14.08.</span>Figure 181〈PI Processing for Copy MD=8 Insert〉：只有 corresponding PI formats 且 destination metadata 全為 PI 時使用 insert 特例，write PRACT 必須1。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.2.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.5, Figure 181, 文件頁 149, PDF 頁 149</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-182 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-182"><summary>NVM Figure 182 · PI Processing for Copy MD=8 Strip</summary>
<!-- claim:NVMCS13-NVM-FIG-182-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="14.09">14.09.</span>Figure 182〈PI Processing for Copy MD=8 Strip〉：只有 corresponding PI formats 且 source metadata 全為 PI 時使用 strip 特例，read PRACT 必須1。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.2.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.5, Figure 182, 文件頁 149, PDF 頁 149</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-dsm"><h2 id="heading-nvmcs-dsm"><span class="section-number">15</span> Dataset Management 與三種 processing limits</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="15.01">15.01.</span>先計算每個 block 是否同時通過三種 limit，再套用 NVMDSMSV。範圍與 hints 的合法性、處理義務以及實際媒體動作分開判斷。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-DSM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="15.02">15.02.</span>Dataset Management 是 advisory：處理 attributes 不等於一定執行 deallocate。NR 是 0-based，16-byte descriptor 的 LLB 是 1-based；DMRL、DMRSL、DMSL 分別約束 range 數、單一 range 長度與總長度。</p><dl class="term-note" aria-label="本段名詞"><div><dt>DMRSL</dt><dd>Dataset Management Range Size Limit；單一 range 的 logical block 處理數量限制。</dd></div><div><dt>DMRL</dt><dd>Dataset Management Ranges Limit，實際 range 數上限。</dd></div><div><dt>DMSL</dt><dd>Dataset Management Size Limit；整筆命令的 logical block 處理數量限制。</dd></div><div><dt>LLB</dt><dd>DSM 的 Length in Logical Blocks；1-based，與 Read／Write 的 NLB 編碼不同。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, 文件頁 44-48, PDF 頁 44-48</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>AD / IDW / IDR</td><td>deallocate／整體寫入／整體讀取 hints</td><td>可組合使用</td></tr><tr><td>Limits nonzero, variant=0</td><td>超過任一 limit 回 Command Size Limit Exceeded</td><td>全部符合則須處理 attributes</td></tr><tr><td>Limits nonzero, variant=1</td><td>宜處理符合 limits 的部分</td><td>不以此原因回 Size Limit Exceeded</td></tr><tr><td>All limits=0</td><td>variant=1：不回報 limits；variant=0：不支援</td><td>三欄需全零或全非零</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="15.03">15.03.</span>DMRL=2、DMSL=1048，range 0 有 1024 blocks、range 1 有 512，且 DMRSL 不限制：variant=1 時前段與後段前 24 blocks 符合 limits。這不等於保證 1048 blocks 都已釋放。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-044 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-044"><summary>NVM Figure 44 · Dataset Management – Data Pointer</summary>
<!-- claim:NVMCS13-NVM-FIG-044-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="15.04">15.04.</span>Figure 44〈Dataset Management – Data Pointer〉：DPTR 指向 descriptors，而不是待複製或 deallocate 的 user data；buffer 長度需由 descriptor size 與依欄位換算後 range count 計算。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, Figure 44, 文件頁 44, PDF 頁 44</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-045 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-045"><summary>NVM Figure 45 · Dataset Management – Command Dword 10</summary>
<!-- claim:NVMCS13-NVM-FIG-045-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="15.05">15.05.</span>Figure 45〈Dataset Management – Command Dword 10〉：CDW10 low8 的 NR 是 0-based，最大 FFh 表示 256 個 ranges；這與 DMRL 的 1-based limit 不同。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, Figure 45, 文件頁 44, PDF 頁 44</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-046 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-046"><summary>NVM Figure 46 · Dataset Management – Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-046-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="15.06">15.06.</span>Figure 46〈Dataset Management – Command Dword 11〉：CDW11 bits2/1/0 分別是 deallocate、integral write、integral read hints；處理 AD 不代表一定釋放。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, Figure 46, 文件頁 44-45, PDF 頁 44-45</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-047 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-047"><summary>NVM Figure 47 · Dataset Management – Range Definition</summary>
<!-- claim:NVMCS13-NVM-FIG-047-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="15.07">15.07.</span>Figure 47〈Dataset Management – Range Definition〉：每筆 16 bytes：CATTR、1-based LLB、64-bit SLBA；256 筆需要 4096 bytes。不要沿用 NLB 的加一依欄位換算。</p><dl class="term-note" aria-label="本段名詞"><div><dt>LLB</dt><dd>DSM 的 Length in Logical Blocks；1-based，與 Read／Write 的 NLB 編碼不同。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, Figure 47, 文件頁 45, PDF 頁 45</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-048 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-048"><summary>NVM Figure 48 · Dataset Management – Context Attributes</summary>
<!-- claim:NVMCS13-NVM-FIG-048-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="15.08">15.08.</span>Figure 48〈Dataset Management – Context Attributes〉：這些 context attributes 描述預期 workload；即使 host hints 不精確，controller 仍須維持資料完整性。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, Figure 48, 文件頁 47, PDF 頁 47</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-049 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-049"><summary>NVM Figure 49 · Dataset Management – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-049-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="15.09">15.09.</span>Figure 49〈Dataset Management – Command Specific Status Values〉：DSM 的 size-limit error 受 NVMDSMSV 影響；variant=1 不得因 processing limits 回報該錯誤。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, Figure 49, 文件頁 48, PDF 頁 48</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-dealloc"><h2 id="heading-nvmcs-dealloc"><span class="section-number">16</span> Deallocated／unwritten 讀取規則</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="16.01">16.01.</span>先判斷是否允許成功讀取，再解釋成功回傳的 bytes。Allocation status、DRB 與 PI 有各自的條件。</p><dl class="term-note" aria-label="本段名詞"><div><dt>DRB</dt><dd>Deallocated Read Behavior；指定 deallocated logical block 的資料回傳規則。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-DEALLOC -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="16.02">16.02.</span>支援且啟用 DULBE 時，Copy、Read、Verify、Compare 存取 deallocated／unwritten blocks 會失敗。未啟用時，DRB=001b 回零、010b 回 FFh、000b 可選其一；同 block 在下一次寫入前的回值須保持 deterministic。</p><dl class="term-note" aria-label="本段名詞"><div><dt>DULBE</dt><dd>Deallocated or Unwritten Logical Block Error Enable，需 namespace DAE 支援。</dd></div><div><dt>DRB</dt><dd>Deallocated Read Behavior；指定 deallocated logical block 的資料回傳規則。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.3.2.1; 4.1.3.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3.2.1; 4.1.3.3, 文件頁 47-48,66, PDF 頁 47-48,66</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>DAE / DULBE</td><td>DAE 是 capability，DULBE 是啟用</td><td>DULBE 預設 0</td></tr><tr><td>DRB=000b</td><td>不是任意舊資料</td><td>依 §3.3.3.2.1 為零或 FFh</td></tr><tr><td>PI after deallocation</td><td>tag bytes 回 FFh；Guard 為 FFh 或 CRC</td><td>配合 DLFEAT.GDS</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="16.03">16.03.</span>一次 Read 全零不能證明 sanitize 成功，可能只是 deallocated 的 DRB。反過來 DULBE 啟用後讀取報錯，也不能單凭此錯誤認定媒體故障。</p></aside>
</section>
<section class="lesson" id="module-nvmcs-zero-uncorrectable"><h2 id="heading-nvmcs-zero-uncorrectable"><span class="section-number">17</span> Write Uncorrectable、Write Zeroes 與整體清零</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.01">17.01.</span>這兩個命令沒有 host user-data payload，但會改變 namespace 語意。先辨識範圍模式，再分配 PI 與 size-limit 檢查。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-ZERO-UNCORRECTABLE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.02">17.02.</span>Write Uncorrectable 將範圍標為無法修復的讀取錯誤；Write Zeroes 使成功的後續讀取資料及非 PI metadata 回零。NSZ=1 的整個 namespace 清零需 NSZS、DEAC=1 與零值 deallocation read behavior，且 host 應檢查 CQE.LBACZ。</p><dl class="term-note" aria-label="本段名詞"><div><dt>LBACZ</dt><dd>LBAs Cleared to Zero；成功 NSZ 命令的範圍確認 bit。</dd></div><div><dt>DEAC</dt><dd>Write Zeroes 的 deallocate 選擇；與 namespace 支援、NSZ、回讀規則一起判讀。</dd></div><div><dt>NSZ</dt><dd>Namespace Zeroes；要求全 namespace 清零，需額外 capability 與 DEAC 條件。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.7-3.3.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7-3.3.8, 文件頁 56-61, PDF 頁 56-61</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>Write Uncorrectable</td><td>標記 block 後，讀取可能報 Unrecovered Read Error</td><td>WUSL 與 NVMWUSV 需成對看</td></tr><tr><td>Write Zeroes PI</td><td>PRCHK=000b、STC=0</td><td>PRACT=1 宜用於產生有效 PI</td></tr><tr><td>WZSL / WZDSL</td><td>依 DEAC 選適用 limit</td><td>NSZ=1 不受這兩欄限制</td></tr><tr><td>LBACZ</td><td>成功 NSZ 命令回 1 才表示全 namespace</td><td>回 0 是指定 range</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>LBACZ</dt><dd>LBAs Cleared to Zero；成功 NSZ 命令的範圍確認 bit。</dd></div><div><dt>PRCHK</dt><dd>Protection Information Check；Guard、Application、Reference 的檢查 bits。</dd></div><div><dt>WZDSL</dt><dd>Write Zeroes with Deallocate 的專用大小限制；不可直接沿用 WZSL。</dd></div><div><dt>DEAC</dt><dd>Write Zeroes 的 deallocate 選擇；與 namespace 支援、NSZ、回讀規則一起判讀。</dd></div><div><dt>WUSL</dt><dd>Write Uncorrectable Size Limit；Write Uncorrectable 的大小限制，需結合 variant 能力判讀。</dd></div><div><dt>NSZ</dt><dd>Namespace Zeroes；要求全 namespace 清零，需額外 capability 與 DEAC 條件。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="17.03">17.03.</span>Host 送 NSZ=1 後得到 Successful Completion 與 LBACZ=0，必須判為僅 range 被清零；舊 controller 可能忽略不支援的 NSZ。不能將 command success 自動升格為整個 namespace 清零。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-077 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-077"><summary>NVM Figure 77 · Write Uncorrectable – Command Dword 10 and Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-077-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.04">17.04.</span>Figure 77〈Write Uncorrectable – Command Dword 10 and Command Dword 11〉：64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.7</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7, Figure 77, 文件頁 56, PDF 頁 56</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-078 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-078"><summary>NVM Figure 78 · Write Uncorrectable – Command Dword 12</summary>
<!-- claim:NVMCS13-NVM-FIG-078-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.05">17.05.</span>Figure 78〈Write Uncorrectable – Command Dword 12〉：Write Uncorrectable 的 CDW12 保留 Directive Type 與 0-based NLB；沒有 Read／Write 的 FUA／PRINFO 欄位，不能直接複用那些命令。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.7</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7, Figure 78, 文件頁 56, PDF 頁 56</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>DTYPE</dt><dd>Directive Type；指定命令使用哪一類 Directive。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-079 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-079"><summary>NVM Figure 79 · Write Uncorrectable – Command Dword 13</summary>
<!-- claim:NVMCS13-NVM-FIG-079-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.06">17.06.</span>Figure 79〈Write Uncorrectable – Command Dword 13〉：此 CDW13 layout 只使用 high16 DSPEC，low16 reserved；保留位不是額外的 tag 或長度空間。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.7</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7, Figure 79, 文件頁 57, PDF 頁 57</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-080 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-080"><summary>NVM Figure 80 · Write Uncorrectable – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-080-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.07">17.07.</span>Figure 80〈Write Uncorrectable – Command Specific Status Values〉：Write Uncorrectable 的本表只列 Attempted Write to Read Only Range；不能把其他命令的 PI 狀態集合套進來。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.7</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7, Figure 80, 文件頁 57, PDF 頁 57</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-081 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-081"><summary>NVM Figure 81 · Write Zeroes – Command Dword 2 and Dword 3</summary>
<!-- claim:NVMCS13-NVM-FIG-081-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.08">17.08.</span>Figure 81〈Write Zeroes – Command Dword 2 and Dword 3〉：Upper／lower tag 欄位組成寫入端的 Storage 與初始 Reference Tag；Copy 的這組 command fields 屬於 destination，source expectations 在 descriptors。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 81, 文件頁 59, PDF 頁 59</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-082 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-082"><summary>NVM Figure 82 · Write Zeroes – Command Dword 10 and Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-082-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.09">17.09.</span>Figure 82〈Write Zeroes – Command Dword 10 and Command Dword 11〉：64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 82, 文件頁 59, PDF 頁 59</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-083 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-083"><summary>NVM Figure 83 · Write Zeroes – Command Dword 12</summary>
<!-- claim:NVMCS13-NVM-FIG-083-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.10">17.10.</span>Figure 83〈Write Zeroes – Command Dword 12〉：NSZ 在 bit23，DEAC 在 bit25，因此這裡 DTYPE 只有 bits22:20。PRCHK=000b、STC=0；整個 namespace 模式還要 NSZS 與零值讀取條件。</p><dl class="term-note" aria-label="本段名詞"><div><dt>PRCHK</dt><dd>Protection Information Check；Guard、Application、Reference 的檢查 bits。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 83, 文件頁 59-60, PDF 頁 59-60</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-084 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-084"><summary>NVM Figure 84 · Write Zeroes – Command Dword 13 if CETYPE is cleared to 0h</summary>
<!-- claim:NVMCS13-NVM-FIG-084-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.11">17.11.</span>Figure 84〈Write Zeroes – Command Dword 13 if CETYPE is cleared to 0h〉：此 CDW13 layout 只使用 high16 DSPEC，low16 reserved；保留位不是額外的 tag 或長度空間。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 84, 文件頁 60, PDF 頁 60</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-085 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-085"><summary>NVM Figure 85 · Write Zeroes – Command Dword 13 if CETYPE is non-zero</summary>
<!-- claim:NVMCS13-NVM-FIG-085-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.12">17.12.</span>Figure 85〈Write Zeroes – Command Dword 13 if CETYPE is non-zero〉：CDW13 high16 保存 Directive Specific，low16 依 CETYPE 保存 CEV；Directive 與 command extension 是獨立欄位。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 85, 文件頁 60, PDF 頁 60</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-086 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-086"><summary>NVM Figure 86 · Write Zeroes – Command Dword 14</summary>
<!-- claim:NVMCS13-NVM-FIG-086-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.13">17.13.</span>Figure 86〈Write Zeroes – Command Dword 14〉：CDW14 提供寫入 tags 的低 32 bits；依 STS 將 space 分割，不能把高位 Storage Tag 全部丟棄。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 86, 文件頁 60, PDF 頁 60</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-087 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-087"><summary>NVM Figure 87 · Write Zeroes – Command Dword 15</summary>
<!-- claim:NVMCS13-NVM-FIG-087-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.14">17.14.</span>Figure 87〈Write Zeroes – Command Dword 15〉：Application Tag mask 與 tag 分別在 CDW15 high16／low16；Copy 使用於寫入目的端，來源端有獨立 expected 欄位。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 87, 文件頁 60, PDF 頁 60</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-088 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-088"><summary>NVM Figure 88 · Write Zeroes – Completion Queue Entry Dword 0</summary>
<!-- claim:NVMCS13-NVM-FIG-088-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.15">17.15.</span>Figure 88〈Write Zeroes – Completion Queue Entry Dword 0〉：只在 NSZ=1 且 Successful Completion 下，LBACZ=1 證明整個 namespace 已清零；0 只表示命令 range。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 88, 文件頁 61, PDF 頁 61</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-089 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-089"><summary>NVM Figure 89 · Write Zeroes – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-089-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.16">17.16.</span>Figure 89〈Write Zeroes – Command Specific Status Values〉：把此命令列出的 SC 與 SCT 一起比對；Invalid Protection Information 指設定／初值不適合所選格式，與實際 Guard Check Error 不同。只適用於本表列出的命令。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.3.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 89, 文件頁 61, PDF 頁 61</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-pi-formats"><h2 id="heading-nvmcs-pi-formats"><span class="section-number">18</span> 16／32／64b Guard 與 Qualified PI</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="18.01">18.01.</span>先由 PIF 決定格式；PIF=11b 才由 QPIF 決定 Guard width，並受 QPIFS 與 STMLA 條件限制。Protection type 仍由 DPS 決定。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-PI-FORMATS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="18.02">18.02.</span>16b Guard PI 共 8 bytes；32b 與 64b Guard PI 各 16 bytes。Application Tag 固定 16 bits，Storage/Reference Space 分別為 32、80、48 bits。32b／64b 格式限 logical block data size 至少 4 KiB。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1; 4.1.5.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1; 4.1.5.3, 文件頁 97-102,130-138, PDF 頁 97-102,130-138</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>16b Guard</td><td>2-byte Guard + 2-byte App + 4-byte space</td><td>STS=0..32</td></tr><tr><td>32b Guard</td><td>4-byte Guard + 2-byte App + 10-byte space</td><td>STS=16..64</td></tr><tr><td>64b Guard</td><td>8-byte Guard + 2-byte App + 6-byte space</td><td>STS=0..48</td></tr><tr><td>STMLA</td><td>bit mask／byte mask／no mask</td><td>qualified type 與 QPIFS 共同決定適用</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="18.03">18.03.</span>64b Guard、STS=18：48-bit space 中高 18 bits 是 Storage Tag、低 30 bits 是 Reference Tag。PI 總大小仍為 16 bytes，不會因 STS 增加而變大。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-155 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-155"><summary>NVM Figure 155 · 16b Guard Protection Information Format when STS field is cleared to 0h</summary>
<!-- claim:NVMCS13-NVM-FIG-155-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="18.04">18.04.</span>Figure 155〈16b Guard Protection Information Format when STS field is cleared to 0h〉：STS=0 的 8-byte PI 由 16-bit Guard、16-bit Application 與 32-bit Reference 組成，各欄位依圖採高位在前。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.1, Figure 155, 文件頁 131, PDF 頁 131</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-156 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-156"><summary>NVM Figure 156 · 16b Guard Protection Information Format with non-zero STS</summary>
<!-- claim:NVMCS13-NVM-FIG-156-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="18.05">18.05.</span>Figure 156〈16b Guard Protection Information Format with non-zero STS〉：加入 Storage Tag 後仍維持 8 bytes；只把原先的 32-bit Reference space 切開，不在末端追加新 bytes。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.1, Figure 156, 文件頁 132, PDF 頁 132</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-157 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-157"><summary>NVM Figure 157 · 32b Guard Protection Information Format</summary>
<!-- claim:NVMCS13-NVM-FIG-157-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="18.06">18.06.</span>Figure 157〈32b Guard Protection Information Format〉：32b Guard 的 16-byte PI 留 80 bits 給 Storage／Reference；STS 至少 16，Reference 至少保留 16 bits。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.2, Figure 157, 文件頁 133, PDF 頁 133</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-159 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-159"><summary>NVM Figure 159 · 64b Guard Protection Information Format</summary>
<!-- claim:NVMCS13-NVM-FIG-159-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="18.07">18.07.</span>Figure 159〈64b Guard Protection Information Format〉：64b Guard 的 PI 雖與 32b Guard 同為 16 bytes，Storage／Reference 只剩 48 bits；不能複用 80-bit 切分。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.3, Figure 159, 文件頁 134, PDF 頁 134</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-164 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-164"><summary>NVM Figure 164 · Storage and Reference Space Separation</summary>
<!-- claim:NVMCS13-NVM-FIG-164-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="18.08">18.08.</span>Figure 164〈Storage and Reference Space Separation〉：高 STS bits 是 Storage Tag，低剩餘 bits 是 Reference Tag；某一側可依合法 STS 不存在。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 164, 文件頁 137, PDF 頁 137</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-165 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-165"><summary>NVM Figure 165 · LBST and LBRT Minimum and Maximum Sizes</summary>
<!-- claim:NVMCS13-NVM-FIG-165-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="18.09">18.09.</span>Figure 165〈LBST and LBRT Minimum and Maximum Sizes〉：以各格式總 space 減 STS 得 Reference width：32b Guard 是 80−STS，並不是 32−STS。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 165, 文件頁 138, PDF 頁 138</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-crc"><h2 id="heading-nvmcs-crc"><span class="section-number">19</span> CRC 參數、位元順序與已知向量</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="19.01">19.01.</span>同樣稱為 CRC 的計算，可能使用不同 polynomial、初值、reflection 與 final XOR。這些參數加上位元儲存順序，才共同決定 Guard 的結果。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-CRC -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="19.02">19.02.</span>32b Guard 使用 CRC-32C；64b Guard 使用 NVM Express 64b CRC，polynomial AD93D23594C93659h、全一 Init／XorOut、RefIn／RefOut=true。不能只用「CRC64」名稱選任意 polynomial。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.1-5.3.1.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.1-5.3.1.3, 文件頁 131-137, PDF 頁 131-137</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>CRC-16</td><td>SBC-4 定義的 Guard CRC</td><td>NVM 不支援 DIX 的 optional IP checksum</td></tr><tr><td>CRC-32C</td><td>polynomial 1EDC6F41h</td><td>4 KiB zero vector → 98F94189h</td></tr><tr><td>CRC-64/NVME</td><td>反射式 register 算例 123456789 → AE8B14860A799888h</td><td>4 KiB zero vector → 6482D367EB22B64Eh</td></tr><tr><td>Coverage</td><td>data + PI 前的 metadata</td><td>排除 PI 本身</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="19.03">19.03.</span>CRC-64/NVME 對 4 KiB 全 FFh 資料計算得到 C0DDBA7302ECA3ACh；全 0 資料得到 6482D367EB22B64Eh。兩個資料集長度相同，CRC 仍不同，因為檢查值取決於資料內容。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-158 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-158"><summary>NVM Figure 158 · 32b CRC Test Cases for 4 KiB Logical Block with no Metadata</summary>
<!-- claim:NVMCS13-NVM-FIG-158-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="19.04">19.04.</span>Figure 158〈32b CRC Test Cases for 4 KiB Logical Block with no Metadata〉：用四組 4 KiB vectors 驗證 CRC32C，而非只驗證全零；incrementing／decrementing patterns 更容易找出順序錯誤。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.2, Figure 158, 文件頁 133, PDF 頁 133</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-160 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-160"><summary>NVM Figure 160 · 64b CRC Polynomials</summary>
<!-- claim:NVMCS13-NVM-FIG-160-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="19.05">19.05.</span>Figure 160〈64b CRC Polynomials〉：以 GF(2) 的 polynomial remainder 解釋 CRC；實際 NVM CRC64 仍需套用後續 Figure161 的 init、reflection 與 XOR 參數。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.3, Figure 160, 文件頁 134-135, PDF 頁 134-135</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-161 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-161"><summary>NVM Figure 161 · 64-bit CRC Rocksoft Model Parameters</summary>
<!-- claim:NVMCS13-NVM-FIG-161-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="19.06">19.06.</span>Figure 161〈64-bit CRC Rocksoft Model Parameters〉：完整參數組才辨識 NVM CRC64：Poly=AD93D23594C93659h、Init／XorOut 全一、RefIn／RefOut=true。此圖 Check=11199E506128D175h 是常見 LSB-first register 結果 AE8B14860A799888h 的 64-bit 反轉；以 Figure 163 向量交叉驗證表示方式。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.3, Figure 161, 文件頁 136, PDF 頁 136</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-162 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-162"><summary>NVM Figure 162 · Logical Block and Metadata Example</summary>
<!-- claim:NVMCS13-NVM-FIG-162-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="19.07">19.07.</span>Figure 162〈Logical Block and Metadata Example〉：逐 byte 的 bits 0..7 對應 reflected input；不要把圖中顯示順序誤當 host integer 的原生 endian。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.3, Figure 162, 文件頁 136, PDF 頁 136</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-163 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-163"><summary>NVM Figure 163 · 64b CRC Test Cases for 4 KiB Logical Block with no Metadata</summary>
<!-- claim:NVMCS13-NVM-FIG-163-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="19.08">19.08.</span>Figure 163〈64b CRC Test Cases for 4 KiB Logical Block with no Metadata〉：核對四組 CRC64 vectors 與 command-set 指定參數；十六進位分組樣式不改變數值，但不可自行補或刪除 hex digits。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.3, Figure 163, 文件頁 137, PDF 頁 137</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-tag-layout"><h2 id="heading-nvmcs-tag-layout"><span class="section-number">20</span> Storage／Reference Tag 的 Dword 封裝</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.01">20.01.</span>先決定總 space 大小，再切 tag，最後拆到命令 Dwords。不要因 tag 的名稱相似就把 Write 的值與 Read 的 expected 值交換。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-TAG-LAYOUT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.02">20.02.</span>Storage Tag 使用 Storage/Reference Space 的高 STS bits，其餘低 bits 是 Reference Tag。命令以 CDW2、CDW3、CDW14 的最多 80 bits 傳入實際或 expected tags；不同 Guard 格式使用不同子集合。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, 文件頁 137-141, PDF 頁 137-141</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>16b Guard, STS=0</td><td>CDW14 為 32-bit reference</td><td>CDW2／3 對此 tag 忽略</td></tr><tr><td>32b Guard, STS=32</td><td>CDW2 low16 + CDW3 high16 是 Storage</td><td>CDW3 low16 + CDW14 為 48-bit Reference</td></tr><tr><td>64b Guard, STS=18</td><td>CDW3 low16 + CDW14 high2 是 Storage</td><td>CDW14 low30 是 Reference</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="20.03">20.03.</span>64b Guard、STS=18、Storage Tag=0x12345、Reference Tag=0x2A：CDW3 low16=0x48D1，CDW14=(1&lt;&lt;30)|0x2A=0x4000002A。Read 使用相同布局的 expected tags。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-166 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-166"><summary>NVM Figure 166 · LBST, ELBST, ILBRT, and EILBRT fields Format in Command Dwords</summary>
<!-- claim:NVMCS13-NVM-FIG-166-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.04">20.04.</span>Figure 166〈LBST, ELBST, ILBRT, and EILBRT fields Format in Command Dwords〉：用最多 80-bit 的抽象 space 連接三個 Dwords；依 PI format 先去掉 unused bits，再切 storage／reference。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 166, 文件頁 138, PDF 頁 138</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-167 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-167"><summary>NVM Figure 167 · I/O Command LBST, ELBST, ILBRT, and EILBRT fields Format</summary>
<!-- claim:NVMCS13-NVM-FIG-167-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.05">20.05.</span>Figure 167〈I/O Command LBST, ELBST, ILBRT, and EILBRT fields Format〉：此表列出每個 Guard 格式實際使用的命令 bits；unused 不等於可自行定義的新欄位。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 167, 文件頁 139, PDF 頁 139</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-168 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-168"><summary>NVM Figure 168 · 16b Guard Protection Information Write Command Example</summary>
<!-- claim:NVMCS13-NVM-FIG-168-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.06">20.06.</span>Figure 168〈16b Guard Protection Information Write Command Example〉：16b Guard 且 STS=0 時只有 CDW14 的 32-bit initial／expected reference；範例 LBADS 應依 Figure125 的 exponent 定義判讀。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 168, 文件頁 139, PDF 頁 139</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-169 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-169"><summary>NVM Figure 169 · 16b Guard Protection Information Read Command Example</summary>
<!-- claim:NVMCS13-NVM-FIG-169-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.07">20.07.</span>Figure 169〈16b Guard Protection Information Read Command Example〉：16b Guard 且 STS=0 時只有 CDW14 的 32-bit initial／expected reference；範例 LBADS 應依 Figure125 的 exponent 定義判讀。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 169, 文件頁 139-140, PDF 頁 139-140</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-170 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-170"><summary>NVM Figure 170 · 32b Guard Protection Information Write Command Example</summary>
<!-- claim:NVMCS13-NVM-FIG-170-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.08">20.08.</span>Figure 170〈32b Guard Protection Information Write Command Example〉：STS=32 的 80-bit space 先放 Storage32 再放 Reference48；CDW3 high16 屬 Storage、low16 屬 Reference。Figure171 的重疊 range 需交叉查 Figure166／170。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 170, 文件頁 140, PDF 頁 140</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-171 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-171"><summary>NVM Figure 171 · 32b Guard Protection Information Read Command Example</summary>
<!-- claim:NVMCS13-NVM-FIG-171-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.09">20.09.</span>Figure 171〈32b Guard Protection Information Read Command Example〉：STS=32 的 80-bit space 先放 Storage32 再放 Reference48；CDW3 high16 屬 Storage、low16 屬 Reference。Figure171 的重疊 range 需交叉查 Figure166／170。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 171, 文件頁 140, PDF 頁 140</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-172 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-172"><summary>NVM Figure 172 · 64b Guard Protection Information Write Command Example</summary>
<!-- claim:NVMCS13-NVM-FIG-172-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.10">20.10.</span>Figure 172〈64b Guard Protection Information Write Command Example〉：48-bit space 且 STS=18 時，Storage 低2 bits 進 CDW14 high2，其餘 Reference30 佔 CDW14 low30。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 172, 文件頁 141, PDF 頁 141</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-173 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-173"><summary>NVM Figure 173 · 64b Guard Protection Information Read Command Example</summary>
<!-- claim:NVMCS13-NVM-FIG-173-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.11">20.11.</span>Figure 173〈64b Guard Protection Information Read Command Example〉：48-bit space 且 STS=18 時，Storage 低2 bits 進 CDW14 high2，其餘 Reference30 佔 CDW14 low30。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 173, 文件頁 141, PDF 頁 141</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-pi-checking"><h2 id="heading-nvmcs-pi-checking"><span class="section-number">21</span> PRACT 與 PRCHK／STC 的組合</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="21.01">21.01.</span>先檢查 namespace 是否啟用 PI，再依命令方向及 metadata 大小選處理分支。Checking bits 與可能的特殊停用值放在最後判斷。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-PI-CHECKING -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="21.02">21.02.</span>PRACT 決定 PI 的傳遞、插入、移除或取代；PRCHK 的 Guard／Application／Reference bits 與獨立 STC 決定檢查要求。PRACT=1 且 MS&gt;PI size 時，Read 仍傳回全部 metadata，不能一律解讀為刪除 PI。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.1.5; 5.3.2-5.3.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5; 5.3.2-5.3.3, 文件頁 21-22,141-152, PDF 頁 21-22,141-152</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>Write, PRACT=1</td><td>MS=PI 時插入；MS&gt;PI 時取代 PI</td><td>此生成分支忽略 PRCHK／STC</td></tr><tr><td>Read, PRACT=1</td><td>先做要求的檢查；MS=PI 才移除</td><td>MS&gt;PI 仍回 metadata 與 PI</td></tr><tr><td>Type 1 / Type 2</td><td>Reference 每個 block 遞增</td><td>Type1 初值須等於對應 SLBA 低 bits</td></tr><tr><td>Type 3</td><td>不宜比對 computed reference</td><td>若因 RTCHK 拒絕，使用 Invalid Protection Information</td></tr><tr><td>Disable sentinels</td><td>Type 1／2：Application Tag=FFFFh 時停用所有 PI checks；Type 3 另要求 Reference Tag（若有）也全一</td><td>不受 PRCHK／STC 設定影響</td></tr><tr><td>Masks</td><td>mask bit=0 不比較</td><td>Storage mask 另受 STMLA 約束</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>RTCHK</dt><dd>Reference Tag Check；要求 Reference Tag 檢查。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="21.03">21.03.</span>16b Guard、MS=16、Read PRACT=1：host 仍接收 16 bytes metadata；若 MS=8，則 host 只接收 data。相同 PRACT 在不同 MS 下造成不同 buffer 大小。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-011 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-011"><summary>NVM Figure 11 · Protection Information Field Definition</summary>
<!-- claim:NVMCS13-NVM-FIG-011-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="21.04">21.04.</span>Figure 11〈Protection Information Field Definition〉：PRACT 是 action，PRCHK 是三種檢查的 bit mask。PRACT=1 時先比較 MS 與 PI size，才能知道資料是否 strip／insert 或維持 metadata 大小。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.1.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5, Figure 11, 文件頁 21-22, PDF 頁 21-22</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>GRDCHK</dt><dd>Guard Check；要求 Guard 檢查。</dd></div><div><dt>ATCHK</dt><dd>Application Tag Check；要求 Application Tag 檢查。</dd></div><div><dt>RTCHK</dt><dd>Reference Tag Check；要求 Reference Tag 檢查。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-012 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-012"><summary>NVM Figure 12 · Storage Tag Check Definition</summary>
<!-- claim:NVMCS13-NVM-FIG-012-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="21.05">21.05.</span>Figure 12〈Storage Tag Check Definition〉：STC 啟用 Storage Tag checking；STS=0 時沒有 Storage Tag，controller 忽略 STC。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.1.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5, Figure 12, 文件頁 22, PDF 頁 22</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-174 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-174"><summary>NVM Figure 174 · Write Command 16b Guard Protection Information Processing</summary>
<!-- claim:NVMCS13-NVM-FIG-174-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="21.06">21.06.</span>Figure 174〈Write Command 16b Guard Protection Information Processing〉：Write PRACT=0 保留 host PI；PRACT=1 在 MS=PI 時插入、MS&gt;PI 時取代。生成 PI 的分支忽略 checking bits。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.2.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.1, Figure 174, 文件頁 143, PDF 頁 143</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-175 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-175"><summary>NVM Figure 175 · Read 16b Guard Command Protection Information Processing</summary>
<!-- claim:NVMCS13-NVM-FIG-175-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="21.07">21.07.</span>Figure 175〈Read 16b Guard Command Protection Information Processing〉：Read 先依要求檢查；PRACT=1 且 MS=PI 才 strip，MS&gt;PI 則仍把 PI 隨 metadata 回傳。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.2.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.2, Figure 175, 文件頁 145, PDF 頁 145</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-176 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-176"><summary>NVM Figure 176 · Protection Information Processing for Compare</summary>
<!-- claim:NVMCS13-NVM-FIG-176-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="21.08">21.08.</span>Figure 176〈Protection Information Processing for Compare〉：Compare 的 host 與 media 輸入各有 PI checking；一般比較涵蓋 data 與非 PI metadata，不能只比對 PI 就宣告內容相同。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.3.2.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.4, Figure 176, 文件頁 146, PDF 頁 146</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-basic-features"><h2 id="heading-nvmcs-basic-features"><span class="section-number">22</span> 基本 Features 的作用域與例外</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="22.01">22.01.</span>讀 Feature 時先辨識 scope、unit 與可儲存條件。Get、Set、Supported Capabilities 回覆也不能套用同一 payload 依欄位換算。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-BASIC-FEATURES -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="22.02">22.02.</span>FID 03h 描述 namespace LBA ranges，05h 控制 namespace error recovery，0Ah 控制 controller normal atomicity。Power Management 的 NVM 補充以 NPWG 大小的 Read 作為 Idle I/O Exit Latency Limit 的參考命令。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.1-4.1.3.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.1-4.1.3.4, 文件頁 64-67, PDF 頁 64-67</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>FID 03h</td><td>4096-byte contiguous buffer；最多 64 個 64-byte entries</td><td>NUM 是 0-based；新 Set 取代前一次</td></tr><tr><td>FID 05h.TLER</td><td>100 ms 單位，從 error recovery 開始計時</td><td>0 代表不設 timeout；適用 LR 命令</td></tr><tr><td>FID 03h attributes</td><td>Hide／Overwriteable 是 host 使用提示</td><td>不是安全隔離或資料保護機制</td></tr><tr><td>FID 02h extension</td><td>idle exit 參考 NPWG-sized Read</td><td>其他命令可超過該 latency limit</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="22.03">22.03.</span>TLER=5 表示 error recovery 的 500 ms 限制，並不是從 SQ submit 起算的整筆命令 500 ms deadline。LBA Range Type 的 NUM=0 表示一個 entry。</p><dl class="term-note" aria-label="本段名詞"><div><dt>SQ</dt><dd>Submission Queue，主機放入命令的提交佇列。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-092 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-092"><summary>NVM Figure 92 · Feature Identifiers – NVM Command Set</summary>
<!-- claim:NVMCS13-NVM-FIG-092-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="22.04">22.04.</span>Figure 92〈Feature Identifiers – NVM Command Set〉：讀 scope 與 buffer 需求，再看 persistence 註腳；對 saveable Feature 不使用本表 nonsaveable persistence 欄。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3, Figure 92, 文件頁 64, PDF 頁 64</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-093 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-093"><summary>NVM Figure 93 · Set Features – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-093-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="22.05">22.05.</span>Figure 93〈Set Features – Command Specific Status Values〉：只有 controller 實際檢查 LBA Range Type 且發現 overlap 時才必須回此錯誤；不可假設成功 Set 已完成全面驗證。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3, Figure 93, 文件頁 64, PDF 頁 64</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-094 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-094"><summary>NVM Figure 94 · LBA Range Type – Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-094-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="22.06">22.06.</span>Figure 94〈LBA Range Type – Command Dword 11〉：NUM low6 是 0-based：Set 時指定有效 entries，Get 時從 CQE DW0 讀實際回傳 entries；兩者都不是 byte count。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.2, Figure 94, 文件頁 65, PDF 頁 65</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-095 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-095"><summary>NVM Figure 95 · LBA Range Type – Completion Queue Entry Dword 0</summary>
<!-- claim:NVMCS13-NVM-FIG-095-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="22.07">22.07.</span>Figure 95〈LBA Range Type – Completion Queue Entry Dword 0〉：NUM low6 是 0-based：Set 時指定有效 entries，Get 時從 CQE DW0 讀實際回傳 entries；兩者都不是 byte count。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.2, Figure 95, 文件頁 65, PDF 頁 65</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-096 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-096"><summary>NVM Figure 96 · LBA Range Type – Data Structure Entry</summary>
<!-- claim:NVMCS13-NVM-FIG-096-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="22.08">22.08.</span>Figure 96〈LBA Range Type – Data Structure Entry〉：64-byte entry 分開描述用途、host hints 與 range；SLBA／NLB 是 logical blocks，GUID 是識別欄位，不是授權。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.2, Figure 96, 文件頁 65-66, PDF 頁 65-66</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-097 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-097"><summary>NVM Figure 97 · Error Recovery – Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-097-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="22.09">22.09.</span>Figure 97〈Error Recovery – Command Dword 11〉：DULBE 是 bit16，TLER low16 以 100 ms 計；TLER=0 表示不限制 retry timeout，須由 recovery 起點計時。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.3, Figure 97, 文件頁 66, PDF 頁 66</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-098 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-098"><summary>NVM Figure 98 · Write Atomicity Normal – Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-098-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="22.10">22.10.</span>Figure 98〈Write Atomicity Normal – Command Dword 11〉：DN=1 只解除 normal atomicity 保證，power-fail atomicity 仍須遵守；這是 controller-scoped Feature。</p><dl class="term-note" aria-label="本段名詞"><div><dt>DN</dt><dd>Write Atomicity Normal 的 Disable Normal；不免除 power-fail atomicity。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.4, Figure 98, 文件頁 66-67, PDF 頁 66-67</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-log-events"><h2 id="heading-nvmcs-log-events"><span class="section-number">23</span> AER、SMART 與錯誤記錄的 NVM 補充</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="23.01">23.01.</span>用事件找調查方向，再用正確 scope 的 log 與 command set 定義依欄位換算。統計數據也要依命令分類，不能只按 opcode 名稱猜。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-LOG-EVENTS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="23.02">23.02.</span>NUSE 的頻繁改變及 ANA 造成的 capacity 回報變動不產生 Namespace Attribute Changed 事件。Error Information 的 LBA 指最低發生錯誤的 LBA；Self-test FLBA 只在 valid bit 設定時有效，且可只代表多個失敗 blocks 中的一個。</p><dl class="term-note" aria-label="本段名詞"><div><dt>FLBA</dt><dd>Failing LBA，NVM Command Set 定義為造成 self-test failure 的其中一個 logical block address。</dd></div><div><dt>ANA</dt><dd>Asymmetric Namespace Access；描述同一 namespace 經不同 controllers 存取時的路徑狀態。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §1.4.2; 4.1.1; 4.1.3.5; 4.1.4.1-4.1.4.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §1.4.2; 4.1.1; 4.1.3.5; 4.1.4.1-4.1.4.4, 文件頁 10-11,62,67,75-77, PDF 頁 10-11,62,67,75-77</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>LBASIN / RLCCN</td><td>FID0Bh bits 13／22</td><td>分別啟用 LBA Status／Rate Limiting notices</td></tr><tr><td>SMART units</td><td>先換算 512-byte units，再套 Base counter 編碼</td><td>不是每個 4 KiB block 加一個 Data Unit</td></tr><tr><td>Read categories</td><td>Data Units Read 含 Verify；Host Read 含 Copy</td><td>Compare、Read 為兩類共同項</td></tr><tr><td>Persistent Event 06h</td><td>create／single-delete 有 FLBAS、DPS</td><td>delete-all 時這兩欄 reserved</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="23.03">23.03.</span>一個 Self-test FLBA=100、valid=1 的紀錄只能找出一個失敗 LBA，不能據此宣告其他 LBAs 全部正常。Error Information LBA=100 的「最低」語意也不能直接套到 FLBA。</p><dl class="term-note" aria-label="本段名詞"><div><dt>FLBA</dt><dd>Failing LBA，NVM Command Set 定義為造成 self-test failure 的其中一個 logical block address。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-090 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-090"><summary>NVM Figure 90 · Asynchronous Event Information – Notice</summary>
<!-- claim:NVMCS13-NVM-FIG-090-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="23.04">23.04.</span>Figure 90〈Asynchronous Event Information – Notice〉：分別辨識 namespace attribute、LBA Status 與 Rate Limiting notices；NUSE 與 ANA capacity 特例不產生 attribute-change 通知。</p><dl class="term-note" aria-label="本段名詞"><div><dt>ANA</dt><dd>Asymmetric Namespace Access；描述同一 namespace 經不同 controllers 存取時的路徑狀態。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.1, Figure 90, 文件頁 62, PDF 頁 62</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-099 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-099"><summary>NVM Figure 99 · Asynchronous Event Configuration – NVM Command Set specific Bit Definitions</summary>
<!-- claim:NVMCS13-NVM-FIG-099-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="23.05">23.05.</span>Figure 99〈Asynchronous Event Configuration – NVM Command Set specific Bit Definitions〉：bits13／22 分別控制 LBA Status 與 Rate Limiting notices；取得 log 和清除事件還須依各 log 的 RAE 流程。</p><dl class="term-note" aria-label="本段名詞"><div><dt>RAE</dt><dd>Retain Asynchronous Event，Get Log Page 是否保留相關 asynchronous event 的 selector。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.5, Figure 99, 文件頁 67, PDF 頁 67</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-109 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-109"><summary>NVM Figure 109 · Get Log Page – Log Page Identifiers</summary>
<!-- claim:NVMCS13-NVM-FIG-109-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="23.06">23.06.</span>Figure 109〈Get Log Page – Log Page Identifiers〉：log 表列出 NVM 補充及 scope／CSI；28h 使用 CSI，restore-to-default 欄也不能當成一般 reset persistence。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4, Figure 109, 文件頁 75-76, PDF 頁 75-76</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-110 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-110"><summary>NVM Figure 110 · Error Information Log Entry Data Structure – User Data</summary>
<!-- claim:NVMCS13-NVM-FIG-110-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="23.07">23.07.</span>Figure 110〈Error Information Log Entry Data Structure – User Data〉：Error Information bytes23:16 是適用時最低錯誤 LBA；需與原命令與 namespace 相連，不當成全 subsystem 的 byte address。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.4.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.1, Figure 110, 文件頁 76, PDF 頁 76</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-111 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-111"><summary>NVM Figure 111 · Self-test Results Data Structure</summary>
<!-- claim:NVMCS13-NVM-FIG-111-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="23.08">23.08.</span>Figure 111〈Self-test Results Data Structure〉：FLBA 只有 valid bit=1 時可用；多個失敗 blocks 時只需回一個，與 Error Information 的最低 LBA 定義不同。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.4.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, Figure 111, 文件頁 76, PDF 頁 76</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-112 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-112"><summary>NVM Figure 112 · Change Namespace Event Data Format (Event Type 06h)</summary>
<!-- claim:NVMCS13-NVM-FIG-112-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="23.09">23.09.</span>Figure 112〈Change Namespace Event Data Format (Event Type 06h)〉：create 取 host-specified values，single delete 取被刪 namespace 的 Identify 值；delete all 時兩欄 reserved。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.4.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.4, Figure 112, 文件頁 77, PDF 頁 77</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-lba-status"><h2 id="heading-nvmcs-lba-status"><span class="section-number">24</span> LBA Status：通知、掃描與修復流程</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.01">24.01.</span>讀到 potentially unrecoverable 不是每個 block 一定無法讀取。先辨識 ATYPE，再檢查 buffer 是否足夠與 completion condition，最後安排資料修復。</p><dl class="term-note" aria-label="本段名詞"><div><dt>ATYPE</dt><dd>Get LBA Status Action Type；02h allocated，10h scan，11h tracked。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-LBA-STATUS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.02">24.02.</span>LID 0Eh 先指出值得調查的 namespace ranges；Get LBA Status 再回詳細 descriptors。ATYPE=02h 回 tracked allocated LBAs，10h 掃描並回 tracked／untracked 候選，11h 只回 tracked 候選且不做 foreground scan。</p><dl class="term-note" aria-label="本段名詞"><div><dt>ATYPE</dt><dd>Get LBA Status Action Type；02h allocated，10h scan，11h tracked。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.6; 4.1.4.5; 4.2.1; 5.2.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.6; 4.1.4.5; 4.2.1; 5.2.1, 文件頁 67-68,77-79,114-122, PDF 頁 67-68,77-79,114-122</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>MNDW / RL</td><td>MNDW 是 0-based dwords；RL=0 到 NSZE−1</td><td>不是 RL=0 查一個 block</td></tr><tr><td>NLSD / CMPC</td><td>實際 descriptor 數／完成原因</td><td>CMPC=1 尚有資料或 scan 未完成；2 完成</td></tr><tr><td>LSIPI / LSIRI</td><td>100 ms 單位；poll interval 不可由 host 改</td><td>Set 回傳最接近支援值</td></tr><tr><td>RAE / LSGC</td><td>RAE=1 分段讀，RAE=0 清事件並允許更新</td><td>重讀 header 檢查 generation</td></tr><tr><td>TLBAAG</td><td>02h 可用較大 allocation granularity</td><td>混合 allocated／deallocated unit 會整段回 allocated</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>CMPC</dt><dd>Completion Condition；描述 Get LBA Status 是否已完成所要求的範圍。</dd></div><div><dt>MNDW</dt><dd>Maximum Number of Dwords；限制 Get LBA Status 回傳資料長度。</dd></div><div><dt>NLSD</dt><dd>Number of LBA Status Descriptors；實際 descriptor 數量。</dd></div><div><dt>RAE</dt><dd>Retain Asynchronous Event，Get Log Page 是否保留相關 asynchronous event 的 selector。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="24.03">24.03.</span>log 有 NLSLNE=0 但 ESTULB 非零時，不能當作沒有問題，宜檢查 attached namespaces 的完整 LBA 範圍。取得可疑 LBAs 後，可從其他可靠來源恢復並寫回；後續查詢會移除成功重寫且未再偵測的項目。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-100 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-100"><summary>NVM Figure 100 · LBA Status Information Attributes – Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-100-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.04">24.04.</span>Figure 100〈LBA Status Information Attributes – Command Dword 11〉：high16 LSIPI 是不可改的 poll interval，low16 LSIRI 是 report interval；兩者均為 100 ms 單位，Set 回傳最接近可支援值。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.6</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.6, Figure 100, 文件頁 68, PDF 頁 68</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-113 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-113"><summary>NVM Figure 113 · LBA Status Information Log Page</summary>
<!-- claim:NVMCS13-NVM-FIG-113-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.05">24.05.</span>Figure 113〈LBA Status Information Log Page〉：先讀 bytes 長度與 namespace-element 數；NLSLNE=0 且 ESTULB 非零仍有需調查範圍，LSGC 是 16-bit 可回繞 counter。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.4.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.5, Figure 113, 文件頁 77-78, PDF 頁 77-78</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-114 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-114"><summary>NVM Figure 114 · LBA Status Log Namespace Element</summary>
<!-- claim:NVMCS13-NVM-FIG-114-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.06">24.06.</span>Figure 114〈LBA Status Log Namespace Element〉：NEID 找出 namespace，RATYPE 建議後續 Get LBA Status 的 ATYPE；NLRD=FFFFFFFFh 表示無 range list 且宜檢查全 namespace。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.4.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.5, Figure 114, 文件頁 78, PDF 頁 78</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-115 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-115"><summary>NVM Figure 115 · LBA Range Descriptor</summary>
<!-- claim:NVMCS13-NVM-FIG-115-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.07">24.07.</span>Figure 115〈LBA Range Descriptor〉：每筆 16-byte range 用 RSLBA 與 0-based RNLB；它是 log 提供的粗範圍，還不是 Get LBA Status 的最終 status descriptor。</p><dl class="term-note" aria-label="本段名詞"><div><dt>RNLB</dt><dd>LBA Status log 的 Range Number of Logical Blocks；0-based。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.4.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.5, Figure 115, 文件頁 78, PDF 頁 78</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>RNLB</dt><dd>LBA Status log 的 Range Number of Logical Blocks；0-based。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-135 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-135"><summary>NVM Figure 135 · Get LBA Status – Data Pointer</summary>
<!-- claim:NVMCS13-NVM-FIG-135-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.08">24.08.</span>Figure 135〈Get LBA Status – Data Pointer〉：DPTR 是 controller 回傳資料的 host 目的位置；Read 回 data，Get LBA Status 回 descriptor list；兩者的回傳資料格式不同。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.2.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.2.1, Figure 135, 文件頁 114, PDF 頁 114</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-136 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-136"><summary>NVM Figure 136 · Get LBA Status – Command Dword 10 and Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-136-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.09">24.09.</span>Figure 136〈Get LBA Status – Command Dword 10 and Command Dword 11〉：64-bit SLBA 的低 32 bits 在 CDW10、高 32 bits 在 CDW11；先完成 range-specific 模式檢查，才把它作為位址使用。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.2.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.2.1, Figure 136, 文件頁 114, PDF 頁 114</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-137 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-137"><summary>NVM Figure 137 · Get LBA Status – Command Dword 12</summary>
<!-- claim:NVMCS13-NVM-FIG-137-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.10">24.10.</span>Figure 137〈Get LBA Status – Command Dword 12〉：MNDW 是 0-based 最大 dword 數；buffer bytes=(MNDW+1)×4，實際回量再看 NLSD。</p><dl class="term-note" aria-label="本段名詞"><div><dt>MNDW</dt><dd>Maximum Number of Dwords；限制 Get LBA Status 回傳資料長度。</dd></div><div><dt>NLSD</dt><dd>Number of LBA Status Descriptors；實際 descriptor 數量。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.2.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.2.1, Figure 137, 文件頁 114, PDF 頁 114</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-138 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-138"><summary>NVM Figure 138 · Get LBA Status – Command Dword 13</summary>
<!-- claim:NVMCS13-NVM-FIG-138-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.11">24.11.</span>Figure 138〈Get LBA Status – Command Dword 13〉：ATYPE=02h／10h／11h 選 allocated／scan／tracked 行為；RL=0 是從 SLBA 到 namespace 最後 LBA，不是零長度。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.2.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.2.1, Figure 138, 文件頁 114-115, PDF 頁 114-115</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-139 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-139"><summary>NVM Figure 139 · LBA Status Descriptor List</summary>
<!-- claim:NVMCS13-NVM-FIG-139-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.12">24.12.</span>Figure 139〈LBA Status Descriptor List〉：8-byte header 後跟 16-byte descriptors；NLSD 是實際數量。CMPC=1 表示資訊尚未完整，即使 CQE 已成功。</p><dl class="term-note" aria-label="本段名詞"><div><dt>CMPC</dt><dd>Completion Condition；描述 Get LBA Status 是否已完成所要求的範圍。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.2.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.2.1, Figure 139, 文件頁 116-117, PDF 頁 116-117</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-140 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-140"><summary>NVM Figure 140 · LBA Status Descriptor Entry</summary>
<!-- claim:NVMCS13-NVM-FIG-140-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.13">24.13.</span>Figure 140〈LBA Status Descriptor Entry〉：NLB 是 0-based；LBARS=010b 適用 ATYPE02h，表示至少一個 block 已配置，不表示每個 block 都獨立配置。</p><dl class="term-note" aria-label="本段名詞"><div><dt>LBARS</dt><dd>LBA Range Status；描述 LBA range 的狀態。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.2.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.2.1, Figure 140, 文件頁 117-118, PDF 頁 117-118</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>DSLBA</dt><dd>Descriptor Starting LBA；指定 LBA Status descriptor 的範圍起點。</dd></div><div><dt>LBARS</dt><dd>LBA Range Status；描述 LBA range 的狀態。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-142 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-142"><summary>NVM Figure 142 · Example LBA Status Log Namespace Element returned by LBA Status Information</summary>
<!-- claim:NVMCS13-NVM-FIG-142-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.14">24.14.</span>Figure 142〈Example LBA Status Log Namespace Element returned by LBA Status Information〉：示例 namespace element 指出兩段候選 ranges 與 RATYPE=11h；這是後續查詢輸入，不是每個候選 block 的最終診斷。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.2.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.1, Figure 142, 文件頁 121, PDF 頁 121</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-143 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-143"><summary>NVM Figure 143 · Example Get LBA Status Descriptors for LBA Range Descriptor 0</summary>
<!-- claim:NVMCS13-NVM-FIG-143-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.15">24.15.</span>Figure 143〈Example Get LBA Status Descriptors for LBA Range Descriptor 0〉：同一 log range 可由後續 Get LBA Status 產生不同數量的精細 descriptors；以實際 NLSD、NLB 與 CMPC 判斷是否需要續查。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.2.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.1, Figure 143, 文件頁 121, PDF 頁 121</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>DSLBA</dt><dd>Descriptor Starting LBA；指定 LBA Status descriptor 的範圍起點。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-144 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-144"><summary>NVM Figure 144 · Example Get LBA Status Descriptors for LBA Range Descriptor 1</summary>
<!-- claim:NVMCS13-NVM-FIG-144-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.16">24.16.</span>Figure 144〈Example Get LBA Status Descriptors for LBA Range Descriptor 1〉：同一 log range 可由後續 Get LBA Status 產生不同數量的精細 descriptors；以實際 NLSD、NLB 與 CMPC 判斷是否需要續查。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.2.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.1, Figure 144, 文件頁 121-122, PDF 頁 121-122</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-sanitize"><h2 id="heading-nvmcs-sanitize"><span class="section-number">25</span> Sanitize 與 Media Verification 的 NVM 規則</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="25.01">25.01.</span>先辨識 target、operation state 與 allocation，再決定可以驗證什麼。命令 CQE 與 sanitize operation 完成分別由不同證據表示。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-SANITIZE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="25.02">25.02.</span>NVM Sanitize 命令採 Base 定義，背景 operation 的資料語意由 §5.12 補充。成功後 Block Erase 回值由廠商定義、Crypto Erase 回值不確定、Overwrite 依 pattern 規則；若 block 已 deallocate，則改用 deallocated-read 規則。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.7; 5.12</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.7; 5.12, 文件頁 113,173-175, PDF 頁 113,173-175</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>LID81h</td><td>追蹤 operation status／progress</td><td>啟動命令成功不是 operation 完成</td></tr><tr><td>Error Information</td><td>sanitize 期間 NVM LBA 欄位回 0</td><td>僅此 NVM 補充，仍須遵守 Base command allowlist</td></tr><tr><td>Media Verification Read</td><td>PRCHK=000b、STC=0</td><td>要求 checking 則 Invalid Field in Command</td></tr><tr><td>Allocated media</td><td>可讀則回實際資料；不可讀則錯誤</td><td>符合條件回 Successful Media Verification Read</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="25.03">25.03.</span>Media Verification state 中，Read 不要求 PI checking 且 allocated media 可讀時，可以忽略讀得出資料的 integrity error 並回特定成功狀態；同一 LBA 連續讀值仍 may 不同。不能用平常 Read 的固定值假設評估它。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-200 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-200"><summary>NVM Figure 200 · Sanitize Operations – Admin Commands Allowed</summary>
<!-- claim:NVMCS13-NVM-FIG-200-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="25.04">25.04.</span>Figure 200〈Sanitize Operations – Admin Commands Allowed〉：NVM 這張 Figure200 補充 sanitize 期間 Error Information 的 LBA 回0；它不是 Base 同號的 Feature 表，也不能取代 Base 的允許命令清單。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.12</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12, Figure 200, 文件頁 173, PDF 頁 173</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-201 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-201"><summary>NVM Figure 201 · Sanitize Operation Types – User Data Values</summary>
<!-- claim:NVMCS13-NVM-FIG-201-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="25.05">25.05.</span>Figure 201〈Sanitize Operation Types – User Data Values〉：保留已配置 media 的成功 sanitize 回值依方法不同；若已 deallocate，改採 deallocated-read 規則，不將任何方法一概寫成全零。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.12</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.12, Figure 201, 文件頁 174, PDF 頁 174</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-312 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-312"><summary>Base Figure 312 · Sanitize Status Log Page</summary>
<!-- claim:NVMCS13-BASE-FIG-312-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="25.06">25.06.</span>Figure 312〈Sanitize Status Log Page〉：Sanitize Status 提供 operation 的進度、結果、起始命令及 state；成功的啟動 CQE 無法取代這份 log。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.13.1.38</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, Figure 312, 文件頁 314-319, PDF 頁 340-345</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-451 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-451"><summary>Base Figure 451 · Sanitize – Command Dword 10</summary>
<!-- claim:NVMCS13-BASE-FIG-451-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="25.07">25.07.</span>Figure 451〈Sanitize – Command Dword 10〉：Subsystem Sanitize 的 CDW10 分開方法及修飾 bits；NVM §4.1.7 使用這個 Base 命令格式。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.26</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 451, 文件頁 450-451, PDF 頁 476-477</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-452 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-452"><summary>Base Figure 452 · Sanitize – Command Dword 11</summary>
<!-- claim:NVMCS13-BASE-FIG-452-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="25.08">25.08.</span>Figure 452〈Sanitize – Command Dword 11〉：CDW11 的 OVRPAT 是 Overwrite pattern；不是所有 SANACT 都使用此值，也不能套用於 Crypto Erase 的讀值預期。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.26</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 452, 文件頁 451, PDF 頁 477</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-alignment"><h2 id="heading-nvmcs-alignment"><span class="section-number">26</span> 對齊、granularity 與效能提示</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="26.01">26.01.</span>先把 raw 欄位轉成 blocks，再評估 start alignment 與 length granularity。只滿足其中一項可能仍引發 read-modify-write。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-ALIGNMENT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="26.02">26.02.</span>NPWG／NPWA、NPRG／NPRA 分別描述寫入與讀取的建議大小及對齊，NOWS／NORS 描述最佳大小。這些 performance hints 不取代 atomic boundaries、命令硬限制或格式規則。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.2.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, 文件頁 122-129, PDF 頁 122-129</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>NPWG / NPWA</td><td>長度與起點同時符合</td><td>先看 NSFEAT.OPTPERF</td></tr><tr><td>NPRG / NPRA / NORS</td><td>適用讀取最佳化</td><td>先看 OPTRPERF</td></tr><tr><td>NPDG / NPDGL</td><td>deallocate granularity 的不同欄位</td><td>用 OPTPERF 決定；Large 不一律加一</td></tr><tr><td>NOIOB / NABO</td><td>最佳 I/O boundary 與 atomic offset 不同</td><td>可分割 I/O 以符合多種條件</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="26.03">26.03.</span>依欄位換算後 NPWG=8、NPWA=8。寫 LBA 8..15 同時符合；寫 9..16 雖然也是 8 blocks，仍跨兩個 granularity units，可能需要讀取兩端舊資料。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-145 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-145"><summary>NVM Figure 145 · An example namespace with four NOIOBs</summary>
<!-- claim:NVMCS13-NVM-FIG-145-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="26.04">26.04.</span>Figure 145〈An example namespace with four NOIOBs〉：最佳 I/O boundary 的示意獨立於 atomic boundary；跨線命令可分割以符合建議，但分割本身會增加命令數。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.2.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 145, 文件頁 124, PDF 頁 124</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-146 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-146"><summary>NVM Figure 146 · Example namespace illustrating a potential NABO and NABSN</summary>
<!-- claim:NVMCS13-NVM-FIG-146-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="26.05">26.05.</span>Figure 146〈Example namespace illustrating a potential NABO and NABSN〉：在 namespace 起點之外另標 atomic offset；不能把所有 boundaries 都預設從 LBA0 開始。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.2.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 146, 文件頁 124, PDF 頁 124</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-147 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-147"><summary>NVM Figure 147 · Example namespace broken down to illustrate potential NPWA and NPWG settings</summary>
<!-- claim:NVMCS13-NVM-FIG-147-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="26.06">26.06.</span>Figure 147〈Example namespace broken down to illustrate potential NPWA and NPWG settings〉：NPWA 指起點，NPWG 指長度 granularity；示意的 8 blocks 是依欄位換算後大小，並非 raw field=8。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.2.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 147, 文件頁 125, PDF 頁 125</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-148 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-148"><summary>NVM Figure 148 · Example namespace broken down to illustrate potential NPRA and NPRG settings</summary>
<!-- claim:NVMCS13-NVM-FIG-148-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="26.07">26.07.</span>Figure 148〈Example namespace broken down to illustrate potential NPRA and NPRG settings〉：讀取 alignment 與 granularity 分開，示例為 4-block alignment 與 8-block granularity；較短且錯位的讀取可能影響效能。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.2.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 148, 文件頁 126, PDF 頁 126</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-149 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-149"><summary>NVM Figure 149 · Non-conformant Write Impact</summary>
<!-- claim:NVMCS13-NVM-FIG-149-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="26.08">26.08.</span>Figure 149〈Non-conformant Write Impact〉：只更新 8-block unit 中的 3 blocks，示例需讀回前後共 5 blocks 舊資料再合成；這是可能的 read-modify-write 成本。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.2.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 149, 文件頁 127, PDF 頁 127</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-150 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-150"><summary>NVM Figure 150 · Host write I/O command following NPWA and NPWG</summary>
<!-- claim:NVMCS13-NVM-FIG-150-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="26.09">26.09.</span>Figure 150〈Host write I/O command following NPWA and NPWG〉：示意同時滿足 NPWA 與 NPWG 的範圍，可避免範例中的頭尾補讀；不是對所有硬體保證沒有任何內部讀取。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.2.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 150, 文件頁 127, PDF 頁 127</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-151 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-151"><summary>NVM Figure 151 · Host write I/O command following NPWG but not NPWA attributes</summary>
<!-- claim:NVMCS13-NVM-FIG-151-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="26.10">26.10.</span>Figure 151〈Host write I/O command following NPWG but not NPWA attributes〉：長度剛好一個 NPWG，起點仍可能錯位而觸及兩個 units；只檢查 length modulo NPWG 不足。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.2.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 151, 文件頁 128, PDF 頁 128</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-performance-feature"><h2 id="heading-nvmcs-performance-feature"><span class="section-number">27</span> Performance Characteristics 的屬性模型</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="27.01">27.01.</span>此 Feature 回報或管理效能屬性，不能把標準 latency 級別當成對任意 workload 的服務保證。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-PERFORMANCE-FEATURE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="27.02">27.02.</span>FID 1Ch 用 ATTRI 選屬性：00h 為只讀標準效能，C0h 為只讀 identifier list，C1h..FFh 為 vendor attributes。Current、Default、Saved 是不同視圖，RVSPA 用來移除指定 vendor attribute 的 saved value。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, 文件頁 69-73, PDF 頁 69-73</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>R4KARL</td><td>標準化 4 KiB random read 的平均 latency 區間</td><td>00h 是未回報</td></tr><tr><td>MSVSPA / USVSPA</td><td>可 save 總數／剩餘數</td><td>index 可不連續</td></tr><tr><td>PAID / ATTRL</td><td>128-bit identifier／有效 vendor bytes</td><td>ATTRL 最大 FE0h</td></tr><tr><td>RVSPA</td><td>刪除 saved value 後取 default</td><td>此操作不使用 data buffer 內容</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="27.03">27.03.</span>R4KARL=0Eh 表示 50 μs ≤ 平均 latency &lt;100 μs，並非 14 μs。讀 C0h list 時應使 ATTRTYP 與 Get 的 SEL 一致，再用 PAID 解釋 vendor payload。</p><dl class="term-note" aria-label="本段名詞"><div><dt>SEL</dt><dd>Select，Get Features 用來選 current、default、saved 或 supported-capabilities view 的欄位。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-102 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-102"><summary>NVM Figure 102 · Performance Characteristics – Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-102-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="27.04">27.04.</span>Figure 102〈Performance Characteristics – Command Dword 11〉：ATTRI low8 選擇標準、list 或 vendor attribute；bit8 RVSPA 刪除 saved vendor value，並非刪除整個 Feature。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, Figure 102, 文件頁 69, PDF 頁 69</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-103 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-103"><summary>NVM Figure 103 · Performance Characteristics – Standard Performance Attribute</summary>
<!-- claim:NVMCS13-NVM-FIG-103-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="27.05">27.05.</span>Figure 103〈Performance Characteristics – Standard Performance Attribute〉：R4KARL 是 latency bucket 而非直接時間；0Eh 是 50–100 μs 的半開區間，00h 為未回報。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, Figure 103, 文件頁 71, PDF 頁 71</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-104 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-104"><summary>NVM Figure 104 · Performance Characteristics – Performance Attribute Identifier List</summary>
<!-- claim:NVMCS13-NVM-FIG-104-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="27.06">27.06.</span>Figure 104〈Performance Characteristics – Performance Attribute Identifier List〉：ATTRTYP 應與 Get SEL 相符；用 MSVSPA／USVSPA 看 saved slots，再以每個 128-bit PAID 辨識 payload，不假設 slots 連續。</p><dl class="term-note" aria-label="本段名詞"><div><dt>SEL</dt><dd>Select，Get Features 用來選 current、default、saved 或 supported-capabilities view 的欄位。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, Figure 104, 文件頁 72, PDF 頁 72</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-105 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-105"><summary>NVM Figure 105 · Performance Characteristics – Vendor Specific Performance Attribute</summary>
<!-- claim:NVMCS13-NVM-FIG-105-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="27.07">27.07.</span>Figure 105〈Performance Characteristics – Vendor Specific Performance Attribute〉：PAID 指出 vendor payload 的定義，ATTRL 限制有效 VS bytes，最大 FE0h；未知 PAID 不應由標準表格猜測。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, Figure 105, 文件頁 73, PDF 頁 73</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-rate-config"><h2 id="heading-nvmcs-rate-config"><span class="section-number">28</span> Rate Limiting 的設定欄位</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="28.01">28.01.</span>先從 LID 28h 取得支援 target，再檢查 HLS／SLS 與 soft-controller 數量。把 host 請求限制和裝置可達能力分開記錄。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-RATE-CONFIG -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="28.02">28.02.</span>FID 28h 以 TGT／TID 選 target，1024-byte buffer 指定 enable、mode、bandwidth、IOPS 與 write/read ratios。TGT=0 指 controller，不能指定 Admin controller 或保留 ID。此 Feature 必須可 save。</p><dl class="term-note" aria-label="本段名詞"><div><dt>IOPS</dt><dd>Input/Output Operations Per Second；每秒 I/O 操作數，與每秒傳輸 bytes 的頻寬不同。</dd></div><div><dt>TGT</dt><dd>Target；選擇 Rate Limiting 設定的目標類型。</dd></div><div><dt>TID</dt><dd>Target Identifier；指定所選目標類型中的實體。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.9; 4.1.5.4; 5.10</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.9; 4.1.5.4; 5.10, 文件頁 73-75,106,165-168, PDF 頁 73-75,106,165-168</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>TGT / TID</td><td>CDW11[23:16]／[15:0]</td><td>TGT=0 才是標準 controller target</td></tr><tr><td>RLC</td><td>RLE bit15；RLM=0 Hard、1 Soft</td><td>支援 Soft 必須也支援 Hard</td></tr><tr><td>BWSF</td><td>0/1/2 = 1/10/100 MiB/s；3/4/5 = 1/10/100 GiB/s</td><td>值乘 scale 才是 bandwidth</td></tr><tr><td>WRIOPSR / WRBWR</td><td>write 分子除 read 分母</td><td>兩者的各 ratio bytes 均需非零</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>WRIOPSR</dt><dd>Write-to-Read IOPS Ratio；寫入相對於讀取的操作數權重。</dd></div><div><dt>WRBWR</dt><dd>Write-to-Read Bandwidth Ratio；寫入相對於讀取的頻寬權重。</dd></div><div><dt>BWSF</dt><dd>Bandwidth Scale Factor；需乘 bandwidth value，單位為 MiB/s 或 GiB/s。</dd></div><div><dt>TGT</dt><dd>Target；選擇 Rate Limiting 設定的目標類型。</dd></div><div><dt>TID</dt><dd>Target Identifier；指定所選目標類型中的實體。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="28.03">28.03.</span>BWSF=1、TBWV=50 表示 500 MiB/s。WBWV 與 WIOPS 控制寫入部分，總量還會按 WRBWR／WRIOPSR 加權；不能把 total 限制只當 read limit。</p><dl class="term-note" aria-label="本段名詞"><div><dt>WRIOPSR</dt><dd>Write-to-Read IOPS Ratio；寫入相對於讀取的操作數權重。</dd></div><div><dt>WIOPS</dt><dd>Write IOPS；寫入操作速率設定值。</dd></div><div><dt>WRBWR</dt><dd>Write-to-Read Bandwidth Ratio；寫入相對於讀取的頻寬權重。</dd></div><div><dt>BWSF</dt><dd>Bandwidth Scale Factor；需乘 bandwidth value，單位為 MiB/s 或 GiB/s。</dd></div><div><dt>TBWV</dt><dd>Total Bandwidth Value；總頻寬設定值，需乘上 BWSF 指定的單位。</dd></div><div><dt>WBWV</dt><dd>Write Bandwidth Value；寫入頻寬設定值，需乘上 BWSF 指定的單位。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-106 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-106"><summary>NVM Figure 106 · Rate Limits – Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-106-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="28.04">28.04.</span>Figure 106〈Rate Limits – Command Dword 11〉：先辨識 TGT 再解讀 TID；TGT=0 使用 controller ID，不能指定 Admin controller、無效 ID 或 FFFDh..FFFFh。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.9</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.9, Figure 106, 文件頁 73, PDF 頁 73</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-107 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-107"><summary>NVM Figure 107 · Rate Limiting – Data Buffer</summary>
<!-- claim:NVMCS13-NVM-FIG-107-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="28.05">28.05.</span>Figure 107〈Rate Limiting – Data Buffer〉：1024-byte 設定分出 enable/mode、兩種 bandwidth、兩種 IOPS 與兩個 write/read ratios；加權 total consumption 與 write-only consumption 分開計。</p><dl class="term-note" aria-label="本段名詞"><div><dt>IOPS</dt><dd>Input/Output Operations Per Second；每秒 I/O 操作數，與每秒傳輸 bytes 的頻寬不同。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.9</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.9, Figure 107, 文件頁 74-75, PDF 頁 74-75</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>TIOPS</dt><dd>Total IOPS；總 I/O 操作速率設定值。</dd></div><div><dt>WIOPS</dt><dd>Write IOPS；寫入操作速率設定值。</dd></div><div><dt>TBWV</dt><dd>Total Bandwidth Value；總頻寬設定值，需乘上 BWSF 指定的單位。</dd></div><div><dt>WBWV</dt><dd>Write Bandwidth Value；寫入頻寬設定值，需乘上 BWSF 指定的單位。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-108 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-108"><summary>NVM Figure 108 · Bandwidth Scale Factors</summary>
<!-- claim:NVMCS13-NVM-FIG-108-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="28.06">28.06.</span>Figure 108〈Bandwidth Scale Factors〉：共同 scale 表供設定、maximum 與 available bandwidth 使用；0..2 是 MiB/s 階梯，3..5 是 GiB/s 階梯。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.3.9</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.9, Figure 108, 文件頁 75, PDF 頁 75</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-rate-modes"><h2 id="heading-nvmcs-rate-modes"><span class="section-number">29</span> Hard／Soft 與 token-bucket 算例</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="29.01">29.01.</span>用能力、limits、實際 demand 三個值判讀結果。設定比例不等於任何時刻都固定吞吐；內部資源與工作負載仍會改變觀測值。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-RATE-MODES -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="29.02">29.02.</span>Hard Limit 設 ceiling，Soft Limit 可利用未用 bandwidth／IOPS；資源不足時依設定比例分配。Appendix A 是多個 token buckets 的實作範例，不要求所有 controllers 採用相同內部實作。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.10.1-5.10.2; Appendix A</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.10.1-5.10.2; Appendix A, 文件頁 166-168,176-177, PDF 頁 166-168,176-177</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>Hard</td><td>有需求且資源不足時按比例分享</td><td>設定上限不是最低效能保證</td></tr><tr><td>Soft</td><td>可使用閒置額度</td><td>多個 soft targets 依 limits 比例分享</td></tr><tr><td>Write tokens</td><td>total bytes × WRBWR；write bytes；total IOPS × WRIOPSR；write IOPS 1</td><td>四個 buckets 各自檢查</td></tr><tr><td>Read tokens</td><td>total bytes 及 total IOPS 1</td><td>不扣 write-only buckets</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="29.03">29.03.</span>教學設定：4 KiB Write，WRBWR=2、WRIOPSR=3，分別消耗 total-bandwidth 8 KiB、write-bandwidth 4 KiB、total-IOPS 3、write-IOPS 1。4 KiB Read 只消耗 total-bandwidth 4 KiB 與 total-IOPS 1。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-202 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-202"><summary>NVM Figure 202 · Example Token Bucket</summary>
<!-- claim:NVMCS13-NVM-FIG-202-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="29.04">29.04.</span>Figure 202〈Example Token Bucket〉：Token 不足讓命令等候；可處理部分但整筆完成才發布 CQE。此圖為 informative implementation example，不是唯一排程演算法。</p><dl class="term-note" aria-label="本段名詞"><div><dt>token bucket</dt><dd>權杖桶；以累積的額度限制操作速率，執行操作時扣除所需額度。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §Appendix A</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §Appendix A, Figure 202, 文件頁 176, PDF 頁 176</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-rate-graph"><h2 id="heading-nvmcs-rate-graph"><span class="section-number">30</span> Rate Limiting log 是能力圖</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.01">30.01.</span>先做結構邊界檢查，再分析 bandwidth bottleneck。Port 的能力與共同 Endurance Group 的能力不同，不能把所有數字直接相加。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Endurance Group</dt><dd>Endurance Group，用於隔離與回報耐久度相關狀態的 NVM 資源群組。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-RATE-GRAPH -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.02">30.02.</span>LID 28h 以 log 起點為基準的 dword offsets 連接 port、controller 與 storage-medium access descriptors；descriptor 可共享，不能假設為固定順序陣列。分段讀取後應重讀 GC，改變時重收整份資料。</p><dl class="term-note" aria-label="本段名詞"><div><dt>GC</dt><dd>Rate Limiting log 的 32-bit Generation Count，用於分段讀取一致性。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.4.8; 5.10.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8; 5.10.3, 文件頁 79-83,168-172, PDF 頁 79-83,168-172</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>LPL / offsets</td><td>長度與指標皆有 dword 單位</td><td>byte offset = dword offset ×4</td></tr><tr><td>NP / NC / NST</td><td>都是 0-based counts</td><td>NNSMAD 是實際數量</td></tr><tr><td>SC / SI</td><td>subsystem／domain／EG／namespace 及其 ID</td><td>依 scope 解讀，避免共享節點重算</td></tr><tr><td>RLMA</td><td>最大 read/write bandwidth／IOPS</td><td>workload 需符合相關 size／queue-depth 條件</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>NNSMAD</dt><dd>Non-Volatile Storage Medium Access Descriptors 數；實際數量，零表示此節點沒有下游 descriptors。</dd></div><div><dt>RLMA</dt><dd>Rate Limiting Maximum Access；所述 port、controller 或 storage access 的最大能力，不是目前流量。</dd></div><div><dt>LPL</dt><dd>Rate Limiting Log Page Length；單位是 dwords，讀取 bytes 前乘 4 並檢查邊界。</dd></div><div><dt>NC</dt><dd>Number of Controllers；Rate Limiting log 的 controller 數，採 0-based 編碼。</dd></div><div><dt>NP</dt><dd>Number of Ports；Rate Limiting log 的 port 數，採 0-based 編碼。</dd></div><div><dt>SI</dt><dd>Scope Identifier；指定 SC 所選範圍中的實體。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="30.03">30.03.</span>兩個 PCIe ports 都能使用一個 Endurance Group，若 EG 的 bandwidth 已被 controller 0 用滿，controller 1 不會因多一個 port 就多一份媒體頻寬。相同 EG 能力可由兩個 controller 指向同一 descriptor。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Endurance Group</dt><dd>Endurance Group，用於隔離與回報耐久度相關狀態的 NVM 資源群組。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-117 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-117"><summary>NVM Figure 117 · Rate Limiting Log Page</summary>
<!-- claim:NVMCS13-NVM-FIG-117-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.04">30.04.</span>Figure 117〈Rate Limiting Log Page〉：NP／NST 是 0-based，LPL 是 dwords，port 指標也以 log 起點的 dwords 表示；讀完整 log 後重驗 GC。</p><dl class="term-note" aria-label="本段名詞"><div><dt>LPL</dt><dd>Rate Limiting Log Page Length；單位是 dwords，讀取 bytes 前乘 4 並檢查邊界。</dd></div><div><dt>GC</dt><dd>Rate Limiting log 的 32-bit Generation Count，用於分段讀取一致性。</dd></div><div><dt>NP</dt><dd>Number of Ports；Rate Limiting log 的 port 數，採 0-based 編碼。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.4.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8, Figure 117, 文件頁 80, PDF 頁 80</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-118 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-118"><summary>NVM Figure 118 · Rate Limiting Port Descriptor</summary>
<!-- claim:NVMCS13-NVM-FIG-118-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.05">30.05.</span>Figure 118〈Rate Limiting Port Descriptor〉：port descriptor 的 available 指尚未分配額度，與 RLMA 的 maximum 不同；controller-list offset 仍相對整份 log。</p><dl class="term-note" aria-label="本段名詞"><div><dt>RLMA</dt><dd>Rate Limiting Maximum Access；所述 port、controller 或 storage access 的最大能力，不是目前流量。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.4.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8, Figure 118, 文件頁 80-81, PDF 頁 80-81</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NC</dt><dd>Number of Controllers；Rate Limiting log 的 controller 數，採 0-based 編碼。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-119 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-119"><summary>NVM Figure 119 · Rate Limiting Controller Descriptor</summary>
<!-- claim:NVMCS13-NVM-FIG-119-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.06">30.06.</span>Figure 119〈Rate Limiting Controller Descriptor〉：controller descriptor 以實際 NNSMAD 指出 access descriptors 數；這個 count 不採 NP／NC 的加一規則。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NNSMAD</dt><dd>Non-Volatile Storage Medium Access Descriptors 數；實際數量，零表示此節點沒有下游 descriptors。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.4.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8, Figure 119, 文件頁 81, PDF 頁 81</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-120 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-120"><summary>NVM Figure 120 · Non-Volatile Storage Medium Access Descriptor</summary>
<!-- claim:NVMCS13-NVM-FIG-120-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.07">30.07.</span>Figure 120〈Non-Volatile Storage Medium Access Descriptor〉：先以 SC 選 scope 再解讀 SI 與巢狀 access list；本表 SI 說明仍提 NSET 且 byte 例子錯置，應以 SC 與表列 bytes7:4 找出。</p><dl class="term-note" aria-label="本段名詞"><div><dt>SI</dt><dd>Scope Identifier；指定 SC 所選範圍中的實體。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.4.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8, Figure 120, 文件頁 81-82, PDF 頁 81-82</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-121 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-121"><summary>NVM Figure 121 · Rate Limiting Maximum Access Descriptor</summary>
<!-- claim:NVMCS13-NVM-FIG-121-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.08">30.08.</span>Figure 121〈Rate Limiting Maximum Access Descriptor〉：以 MBSF 轉 bandwidth；四個 maximum 需配合 workload size 與 queue depth，不能當成任意 workload 的最低保證。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.4.8</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8, Figure 121, 文件頁 82-83, PDF 頁 82-83</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-195 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-195"><summary>NVM Figure 195 · Port Graph Example</summary>
<!-- claim:NVMCS13-NVM-FIG-195-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.09">30.09.</span>Figure 195〈Port Graph Example〉：這是共享節點的 graph，不是單一樹；同一 EG 可被兩個 controllers 引用，且不能因此重算共享媒體能力。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.10.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.10.3, Figure 195, 文件頁 169, PDF 頁 169</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-196 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-196"><summary>NVM Figure 196 · Rate Limiting Log Page Example</summary>
<!-- claim:NVMCS13-NVM-FIG-196-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.10">30.10.</span>Figure 196〈Rate Limiting Log Page Example〉：描述子以相對於 log 起點的 dword offset 連接。例如 offset=299 對應 299×4=1196 bytes；共享的 descriptor 可由多條連接指向。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.10.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.10.3, Figure 196, 文件頁 169-170, PDF 頁 169-170</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-197 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-197"><summary>NVM Figure 197 · Example Dual Port PCIe NVMe SSD</summary>
<!-- claim:NVMCS13-NVM-FIG-197-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.11">30.11.</span>Figure 197〈Example Dual Port PCIe NVMe SSD〉：雙 port 的 transport 能力不會複製 shared EG 的媒體能力；由同一 storage bottleneck 解釋競爭。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express，主機與非揮發性記憶體子系統之間的介面規範家族。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.10.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.10.3, Figure 197, 文件頁 171, PDF 頁 171</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-198 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-198"><summary>NVM Figure 198 · Dual Port PCIe NVMe SSD Rate Limiting Log Page Example</summary>
<!-- claim:NVMCS13-NVM-FIG-198-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.12">30.12.</span>Figure 198〈Dual Port PCIe NVMe SSD Rate Limiting Log Page Example〉：保留双 port 共用一個 storage node 的關係；原範例 LPL=570 dwords 但列出超出2280 bytes的結構，因此不可當成有效輸入樣本。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.10.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.10.3, Figure 198, 文件頁 171-172, PDF 頁 171-172</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-fdp"><h2 id="heading-nvmcs-fdp"><span class="section-number">31</span> FDP：placement、RUH 與可觀測數據</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="31.01">31.01.</span>建立時決定 placement 關係，執行時看 handle status，事後再用 statistics／events 解釋媒體搬移。三種資料不能互相代替。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-FDP -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="31.02">31.02.</span>FDP namespace 的 placement handles 對應 Reclaim Unit Handles。共享 RUH 的 namespaces 必須使用相同 Format Index；host 指定的 handle list 不得重複 RUHID。RUH Status descriptors 先依 Placement Handle、再依 Reclaim Group Identifier 排序。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Reclaim Group</dt><dd>Reclaim Group，具有共同回收行為的一組非揮發性儲存資源。</dd></div><div><dt>Reclaim Unit</dt><dd>Reclaim Unit，controller 執行媒體回收時使用的較小管理粒度。</dd></div><div><dt>FDP</dt><dd>Flexible Data Placement，把資料放置提示與媒體回收管理連結的能力。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.2.1; 4.1.4.6-4.1.4.7; 4.1.6.3</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.2.1; 4.1.4.6-4.1.4.7; 4.1.6.3, 文件頁 26,79,110-113, PDF 頁 26,79,110-113</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>NPHNDLS</td><td>最多 128，且不超過 configuration 的 RUH 數</td><td>0 有 controller 選擇與共享規則</td></tr><tr><td>EARUTR / RUAMW</td><td>剩餘秒數估計／可寫 logical blocks</td><td>EARUTR=0 未回報；不是保證壽命</td></tr><tr><td>LID 22h</td><td>HBMW／MBMW 含 NVM 指定寫入類命令</td><td>含 Copy 寫入端、Zeroes、Uncorrectable</td></tr><tr><td>LID 23h event 0h</td><td>LBAV 控制 LBA 有效性</td><td>NLBAM=FFFFh 表示至少 FFFFh</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>NPHNDLS</dt><dd>Number of Placement Handles，NVM create payload 中 Placement Handle List 的 entry count，最大 128。</dd></div><div><dt>LBAV</dt><dd>LBA Valid；指出回報的 LBA 是否有效。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="31.03">31.03.</span>兩個 namespaces 共享 RUH 5，第一個使用 FIDX=2，第二個 create 指定 FIDX=3，即使資料大小同為 4 KiB，也不符合共享 RUH 的 Format Index 條件。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-021 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-021"><summary>NVM Figure 21 · Reclaim Unit Handle Status Descriptor</summary>
<!-- claim:NVMCS13-NVM-FIG-021-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="31.04">31.04.</span>Figure 21〈Reclaim Unit Handle Status Descriptor〉：以 PID 找 Placement Handle／Reclaim Group，再解讀 RUHID、剩餘時間估計及可寫 blocks；RUAMW 不是固定的 nominal RU size。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Reclaim Group</dt><dd>Reclaim Group，具有共同回收行為的一組非揮發性儲存資源。</dd></div><div><dt>Reclaim Unit</dt><dd>Reclaim Unit，controller 執行媒體回收時使用的較小管理粒度。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §3.2.1.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.2.1.1, Figure 21, 文件頁 26, PDF 頁 26</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-116 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-116"><summary>NVM Figure 116 · Media Reallocated - Event Type Specific Data Structure</summary>
<!-- claim:NVMCS13-NVM-FIG-116-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="31.05">31.05.</span>Figure 116〈Media Reallocated - Event Type Specific Data Structure〉：先驗 LBAV 再使用 LBA；NLBAM=0 未回報數量、FFFFh 表示至少該數量，不是一定恰好搬移 65535 blocks。</p><dl class="term-note" aria-label="本段名詞"><div><dt>LBAV</dt><dd>LBA Valid；指出回報的 LBA 是否有效。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.4.7</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.7, Figure 116, 文件頁 79, PDF 頁 79</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-streams"><h2 id="heading-nvmcs-streams"><span class="section-number">32</span> Streams 的 NVM 單位與優先順序</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="32.01">32.01.</span>用兩層大小模型解釋 Stream Write Size 與較大的 stream granularity。它們可能和 namespace hints 成整數倍，但規格不保證每個 namespace 都如此。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-STREAMS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="32.02">32.02.</span>NVM 的 Stream Write Size 以 logical blocks 表示；stream granularity length 是 SGS 乘依欄位換算後 SWS blocks。使用 Streams 時，host 宜依 SGS／SWS 的建議處理 write／deallocate，再協調 namespace hints。</p><dl class="term-note" aria-label="本段名詞"><div><dt>SWS</dt><dd>Stream Write Size；NVM command-set 單位為 logical blocks。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.2.2.3; 5.13</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2.3; 5.13, 文件頁 128-129,175, PDF 頁 128-129,175</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>SWS</td><td>建議寫入大小，以 blocks 計</td><td>宜為 NPWG 的倍數</td></tr><tr><td>SGS × SWS</td><td>stream granularity 的長度</td><td>適用 stream deallocate 對齊／長度</td></tr><tr><td>Priority</td><td>用 Streams 時優先 Streams attributes</td><td>未使用則用 namespace hints</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>SWS</dt><dd>Stream Write Size；NVM command-set 單位為 logical blocks。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="32.03">32.03.</span>依欄位換算後 SWS=8 blocks、SGS=4，stream granularity 是 32 blocks。8-block Write 可符合 SWS，但一個完整 granularity-unit 的 deallocate 長度是 32 blocks。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-152 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-152"><summary>NVM Figure 152 · Two streams composed of SGS and SWS</summary>
<!-- claim:NVMCS13-NVM-FIG-152-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="32.04">32.04.</span>Figure 152〈Two streams composed of SGS and SWS〉：以 SGS 個 SWS units 組成 stream granularity；寫入依 SWS、stream deallocate 依較大 granularity 協調。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.2.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 152, 文件頁 128, PDF 頁 128</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-712 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-712"><summary>Base Figure 712 · Streams Directive – Return Parameters Data Structure</summary>
<!-- claim:NVMCS13-BASE-FIG-712-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="32.05">32.05.</span>Figure 712〈Streams Directive – Return Parameters Data Structure〉：Streams Return Parameters 的 SWS／SGS 描述寫入大小與配置粒度；NVM §5.13 將 SWS 的 command-set 單位定義為 logical blocks。</p><details class="source-note"><summary>來源：Base 2.4 §8.1.9.3.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.9.3.1.1, Figure 712, 文件頁 624-625, PDF 頁 650-651</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-ana-reservations"><h2 id="heading-nvmcs-ana-reservations"><span class="section-number">33</span> ANA 與 Reservations 的 NVM 行為</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="33.01">33.01.</span>同一 namespace 的可達性與存取權限要分開檢查；不能將路徑狀態等同 reservation ownership。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-ANA-RESERVATIONS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="33.02">33.02.</span>ANA 狀態會限制指定 Features 並改變 capacity 回報；Reservations 則依 reservation type、holder 與 registration 狀態決定各命令是否允許。這些共用 namespace 能力可適用於 PCIe 多 controller 情境。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.1; 5.11</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.1; 5.11, 文件頁 119,172-173, PDF 頁 119,172-173</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>ANA Identify</td><td>Inaccessible／Persistent Loss 下 NUSE、NVMCAP 回零</td><td>不是 media 被清空</td></tr><tr><td>ANA FID05h</td><td>Get 的 Inaccessible／Persistent Loss／Change 受限</td><td>使用對應 ANA status</td></tr><tr><td>Write Exclusive / Exclusive Access</td><td>非 holder：前者允許 read-like；後者 read／write-like 都衝突</td><td>兩者的非 holder write-like 都衝突</td></tr><tr><td>Registrants Only / All Registrants</td><td>Write Exclusive 類允許所有人 read、registrants write；Exclusive Access 類僅 registrants read／write</td><td>Copy 每個 source 用 read 權限，destination 用 write 權限</td></tr><tr><td>Reservations</td><td>分 read-like、write-like 命令查矩陣</td><td>holder、registrant 與 type 必須一起看</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>NVMCAP</dt><dd>NVM Capacity；以 bytes 計，不能與 NSZE／NCAP 的 logical-block 數直接比較。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="33.03">33.03.</span>同一 SSD 的兩個 PCIe controllers 可共享 namespace。Controller 1 的路徑可用，仍可能因 reservation 類型與自身 registration 狀態而無法 Write；Read 是否允許需另外查表。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-141 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-141"><summary>NVM Figure 141 · ANA effects on NVM Command Set Command Processing</summary>
<!-- claim:NVMCS13-NVM-FIG-141-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="33.04">33.04.</span>Figure 141〈ANA effects on NVM Command Set Command Processing〉：按 command 與 ANA state 交叉查：FID05h 的 Get／Set 限制列並不完全相同，Identify 的容量回零只描述報告值。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.1, Figure 141, 文件頁 119, PDF 頁 119</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-199 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-199"><summary>NVM Figure 199 · Command Behavior in the Presence of a Reservation</summary>
<!-- claim:NVMCS13-NVM-FIG-199-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="33.05">33.05.</span>Figure 199〈Command Behavior in the Presence of a Reservation〉：逐列區分 read-like／write-like 命令，再按 holder／registration 與 reservation type 判斷；不可把所有非 holder 視為相同。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.11</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.11, Figure 199, 文件頁 173, PDF 頁 173</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-key-per-io"><h2 id="heading-nvmcs-key-per-io"><span class="section-number">34</span> Key Per I/O 的 NVM 對齊約束</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="34.01">34.01.</span>先從 KPIOCAP 與 namespace status 判斷適用，再解讀 CETYPE／CEV 的 command extension。金鑰建立及管理不由這份 NVM 補充完整定義。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-KEY-PER-IO -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="34.02">34.02.</span>Key Per I/O 的 NVM 補充要求使用 key tag 的命令符合 KPIODAAG 的 LBA 起點對齊與長度 granularity；不符合時回 Invalid Field in Command。Capability、namespace enablement 與 key 管理是不同層次。</p><dl class="term-note" aria-label="本段名詞"><div><dt>KPIODAAG</dt><dd>Key Per I/O Data Access Alignment and Granularity；0-based blocks。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.5; 4.1.5</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.5; 4.1.5, 文件頁 91-92,105,160, PDF 頁 91-92,105,160</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>KPIOCAP</td><td>支援與 subsystem／namespace scope</td><td>不能只看單一 enable bit</td></tr><tr><td>KPIOSNS / KPIOENS</td><td>namespace 支援／啟用</td><td>未支援時 enable 必須為 0</td></tr><tr><td>KPIODAAG</td><td>0-based logical-block granularity</td><td>起點及長度都必須符合</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>KPIODAAG</dt><dd>Key Per I/O Data Access Alignment and Granularity；0-based blocks。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="34.03">34.03.</span>raw KPIODAAG=7 代表 8-block granularity。SLBA=16、length=8 符合；SLBA=17 或 length=7 都不符合，即使其他 PI 欄位完全正確也不能使用。</p></aside>
</section>
<section class="lesson" id="module-nvmcs-migration-queue"><h2 id="heading-nvmcs-migration-queue"><span class="section-number">35</span> LBA Migration Queue 與變更追蹤</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="35.01">35.01.</span>這個 queue 保存變更範圍與序列標記，不保存完整新資料。Host 讀 entry 後仍需以適當 I/O 取得資料，並處理滿 queue 的停止邊界。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-MIGRATION-QUEUE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="35.02">35.02.</span>Track Send 啟用 LBA Migration Queue 後，controller 可聚合邏輯 block 修改或 deallocation 記錄。Entry 只在所報命令效果生效後發布，可早於該命令 CQE；queue entry 與 I/O completion 是不同時間點。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §4.1.8; 5.7</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.8; 5.7, 文件頁 113-114,162-164, PDF 頁 113-114,162-164</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>LBACIR</td><td>00：range；01：整個 namespace；10：無 range</td><td>先判斷欄位是否有效</td></tr><tr><td>ESA</td><td>001 start／resume；010 stop；011 suspend；111 full</td><td>full 表示 logging 已停止</td></tr><tr><td>DLBA / CDQP</td><td>deallocated 標記／entry phase</td><td>DLBA=0 仍可能描述 deallocate 類修改</td></tr><tr><td>RALBAS</td><td>開始命令處理期間的變更可由 ATYPE02h 補齊</td><td>start／stop marker 不要求先於 Track Send CQE</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>LBACIR</dt><dd>LBA Change Indication Range；指定 range、整個 namespace 或無 range 的 entry 解讀。</dd></div><div><dt>CDQP</dt><dd>Controller Data Queue Phase；讓 host 判別 queue 位置的新 entry。</dd></div><div><dt>DLBA</dt><dd>Deallocated LBA；entry 中的 deallocation 標記。</dd></div><div><dt>ESA</dt><dd>Entry Sequence Attribute；LBA Migration Queue 的 start／stop／suspend／full 標記。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="35.03">35.03.</span>三筆連續 Write 可合併成一個 range entry；所以 queue entry 數不等於寫入命令數。ESA=111b 後，host 不能假設後續每次修改仍持續記錄。</p><dl class="term-note" aria-label="本段名詞"><div><dt>ESA</dt><dd>Entry Sequence Attribute；LBA Migration Queue 的 start／stop／suspend／full 標記。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-194 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-194"><summary>NVM Figure 194 · LBA Migration Queue Entry Type 0</summary>
<!-- claim:NVMCS13-NVM-FIG-194-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="35.04">35.04.</span>Figure 194〈LBA Migration Queue Entry Type 0〉：32-byte entry 最後一 byte 含範圍有效性、deallocation、sequence 與 phase；先看 LBACIR 再用 SLBA／NLB，NLB 是0-based。</p><dl class="term-note" aria-label="本段名詞"><div><dt>LBACIR</dt><dd>LBA Change Indication Range；指定 range、整個 namespace 或無 range 的 entry 解讀。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.7</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.7, Figure 194, 文件頁 163-164, PDF 頁 163-164</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CDQP</dt><dd>Controller Data Queue Phase；讓 host 判別 queue 位置的新 entry。</dd></div><div><dt>DLBA</dt><dd>Deallocated LBA；entry 中的 deallocation 標記。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-BASE-FIG-561 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-561"><summary>Base Figure 561 · Track Send – Command Dword 10</summary>
<!-- claim:NVMCS13-BASE-FIG-561-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="35.05">35.05.</span>Figure 561〈Track Send – Command Dword 10〉：Track Send CDW10 先選 management operation，MOS 再依 operation 解讀；Log User Data Changes 用來追蹤 NVM 資料變更。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.32</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.32, Figure 561, 文件頁 523, PDF 頁 549</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-562 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-562"><summary>Base Figure 562 · Log User Data Changes – Management Operation Specific Field</summary>
<!-- claim:NVMCS13-BASE-FIG-562-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="35.06">35.06.</span>Figure 562〈Log User Data Changes – Management Operation Specific Field〉：LACT 控制開始／停止 user-data changes logging；必須配合 CDQID 指定已建立的 LBA Migration Queue。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.32.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.32.1.1, Figure 562, 文件頁 523, PDF 頁 549</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-563 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-563"><summary>Base Figure 563 · Log User Data Changes – Command Dword 11</summary>
<!-- claim:NVMCS13-BASE-FIG-563-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="35.07">35.07.</span>Figure 563〈Log User Data Changes – Command Dword 11〉：CDQID 是 controller data queue identifier；不是 NSID 或 SQID，識別此次變更記錄送往哪個 queue。</p><details class="source-note"><summary>來源：Base 2.4 §5.2.32.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.32.1.1, Figure 563, 文件頁 523, PDF 頁 549</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-export-template"><h2 id="heading-nvmcs-export-template"><span class="section-number">36</span> Memory-based 資源匯出範本</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.01">36.01.</span>範本固定的相容性介面與 underlying 裝置能力是兩層。先確認 namespace 格式相容，再設定不超過 underlying 能力的限制；沒有被範本開放的能力不能自行宣告。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-EXPORT-TEMPLATE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.02">36.02.</span>Reference Exported NVM Subsystem Template 是選用的 memory-based 範本，限定一個 controller（ID 0h）及一個 namespace（ID 1h）。建立時必須設 TR=1；configuration state 只能以一筆命令設定一次，重複設定回 Command Sequence Error。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.4.1-5.4.1.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4.1-5.4.1.1, 文件頁 152-159, PDF 頁 152-159</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>Identity and version</td><td>CAP.CSS=1、VS=020300h；NVM VER=010200h</td><td>範本固定 Base 2.3／NVM 1.2，不隨本 PDF 版本自動升級</td></tr><tr><td>Controller limits</td><td>MDTS、RAB、NCQS、NSQS、MQES、AWUN／AWUPF 受 underlying 限制</td><td>NCQS／NSQS 是 0-based</td></tr><tr><td>Namespace compatibility</td><td>LBAF0 的 LBADS／MS 必須相同，MS=0；DPS／KPIOENS／CWP 必須為零</td><td>controller 負責 Format Index remapping</td></tr><tr><td>Observable defaults</td><td>Error entries 與 SMART 為零；firmware active slot=1</td><td>支援清單、Feature defaults 與 Identify exceptions 另有固定規則</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>MQES</dt><dd>Maximum Queue Entries Supported；queue entry 數上限，採 0-based 編碼。</dd></div><div><dt>NCQS</dt><dd>Number of I/O Completion Queues Supported；支援的 I/O CQ 數，採 0-based 編碼。</dd></div><div><dt>NSQS</dt><dd>Number of I/O Submission Queues Supported；支援的 I/O SQ 數，採 0-based 編碼。</dd></div><div><dt>CAP</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="36.03">36.03.</span>Underlying NCQS=7 可支援 8 queues，範本設定 NCQS=3 表示最多 4 queues；不能把 raw 3 誤解成 3 queues。Namespace 的 NGUID 為零時，NUUID 必須提供有效 UUID。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NGUID</dt><dd>Namespace Globally Unique Identifier，namespace 的 128-bit 全域識別值。</dd></div><div><dt>NCQS</dt><dd>Number of I/O Completion Queues Supported；支援的 I/O CQ 數，採 0-based 編碼。</dd></div><div><dt>UUID</dt><dd>Universally Unique Identifier，128-bit identifier；其實際關聯範圍仍由使用它的資料結構決定。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-183 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-183"><summary>NVM Figure 183 · Reference Exported Configuration State</summary>
<!-- claim:NVMCS13-NVM-FIG-183-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.04">36.04.</span>Figure 183〈Reference Exported Configuration State〉：先分固定 364-byte controller configuration 與 48-byte namespace configuration；總長 412 bytes，僅能單筆設定一次。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 183, 文件頁 153, PDF 頁 153</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>RENSCS / RECCS</dt><dd>Reference Exported Controller／Namespace Configuration State；分別是 364／48 bytes。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-184 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-184"><summary>NVM Figure 184 · Reference Controller Capabilities Register Values</summary>
<!-- claim:NVMCS13-NVM-FIG-184-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.05">36.05.</span>Figure 184〈Reference Controller Capabilities Register Values〉：未列出的 CAP bits 清零；CSS 表示僅 NVM，TO=FFh 表示 127.5 秒，queues 要 physically contiguous，MQES 受 underlying 限制。圖中 CQE 名稱對應 contiguous-queue 欄位。</p><dl class="term-note" aria-label="本段名詞"><div><dt>MQES</dt><dd>Maximum Queue Entries Supported；queue entry 數上限，採 0-based 編碼。</dd></div><div><dt>CAP</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。</dd></div><div><dt>TO</dt><dd>CAP Timeout；每單位 500 ms，FFh 為 127.5 秒。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 184, 文件頁 153, PDF 頁 153</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>TO</dt><dd>CAP Timeout；每單位 500 ms，FFh 為 127.5 秒。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-185 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-185"><summary>NVM Figure 185 · Reference Version Register Values</summary>
<!-- claim:NVMCS13-NVM-FIG-185-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.06">36.06.</span>Figure 185〈Reference Version Register Values〉：範本的 VS 固定 020300h，即 2.3.0；不要因手上的 Base 版本為 2.4 就改成 2.4。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 185, 文件頁 153, PDF 頁 153</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-186 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-186"><summary>NVM Figure 186 · Reference Firmware Slot Information Log Page</summary>
<!-- claim:NVMCS13-NVM-FIG-186-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.07">36.07.</span>Figure 186〈Reference Firmware Slot Information Log Page〉：Active firmware slot 固定為 1；其餘 firmware log 值依零值規則及 configuration state 的 FR exception。</p><dl class="term-note" aria-label="本段名詞"><div><dt>FR</dt><dd>Firmware Revision，Identify Controller 回報目前 active firmware revision 的八-byte ASCII 欄位。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 186, 文件頁 154, PDF 頁 154</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>AFI</dt><dd>Active Firmware Info，LID 03h 中同時包含目前 active slot 與下一次 reset 後預定 active slot 的 byte。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-187 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-187"><summary>NVM Figure 187 · Reference Feature Default Values</summary>
<!-- claim:NVMCS13-NVM-FIG-187-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.08">36.08.</span>Figure 187〈Reference Feature Default Values〉：Composite over／under 預設 FFFFh／0；IV=0 的 CD=1，其他 IV 的 CD=0。Number of Queues 取決於請求與配置結果，不是固定零。</p><dl class="term-note" aria-label="本段名詞"><div><dt>IV</dt><dd>Interrupt Vector，Completion Queue 指定的 interrupt vector 編號。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 187, 文件頁 155, PDF 頁 155</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>TMPSEL</dt><dd>Temperature Sensor Select，選擇 Composite Temperature 或 sensor 1 到 8 的欄位。</dd></div><div><dt>THSEL</dt><dd>Threshold Type Select，選擇 over-temperature 或 under-temperature threshold。</dd></div><div><dt>TMPTH</dt><dd>Temperature Threshold，16-bit Kelvin threshold value。</dd></div><div><dt>NSQS</dt><dd>Number of I/O Submission Queues Supported；支援的 I/O SQ 數，採 0-based 編碼。</dd></div><div><dt>IV</dt><dd>Interrupt Vector，Completion Queue 指定的 interrupt vector 編號。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-188 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-188"><summary>NVM Figure 188 · Reference Identify Controller or Namespace Data Structures</summary>
<!-- claim:NVMCS13-NVM-FIG-188-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.09">36.09.</span>Figure 188〈Reference Identify Controller or Namespace Data Structures〉：Identify 只開放列出的 exceptions：NCAP=NSZE、SQES=66h 為 64-byte SQE、CQES=44h 為 16-byte CQE；CNS06h 的 NVM VER 固定 1.2.0。</p><dl class="term-note" aria-label="本段名詞"><div><dt>CQES</dt><dd>Completion Queue Entry Size；以 2 的次方表示 CQE 的最小與最大 bytes。</dd></div><div><dt>SQES</dt><dd>Submission Queue Entry Size；以 2 的次方表示 SQE 的最小與最大 bytes。</dd></div><div><dt>SQE</dt><dd>Submission Queue Entry，SQ 中的一筆命令資料結構。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 188, 文件頁 156, PDF 頁 156</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NGUID</dt><dd>Namespace Globally Unique Identifier，namespace 的 128-bit 全域識別值。</dd></div><div><dt>CQES</dt><dd>Completion Queue Entry Size；以 2 的次方表示 CQE 的最小與最大 bytes。</dd></div><div><dt>SQES</dt><dd>Submission Queue Entry Size；以 2 的次方表示 SQE 的最小與最大 bytes。</dd></div><div><dt>UUID</dt><dd>Universally Unique Identifier，128-bit identifier；其實際關聯範圍仍由使用它的資料結構決定。</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-189 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-189"><summary>NVM Figure 189 · Reference Exported Controller Configuration State</summary>
<!-- claim:NVMCS13-NVM-FIG-189-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.10">36.10.</span>Figure 189〈Reference Exported Controller Configuration State〉：ECNTLID=0，限制值不得超過 underlying；NCQS／NSQS 先解 0-based。WZS／DSMS 需對應底層能力與所報 Commands Supported and Effects。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 189, 文件頁 157-158, PDF 頁 157-158</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-190 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-190"><summary>NVM Figure 190 · Reference Exported Controller Configuration State</summary>
<!-- claim:NVMCS13-NVM-FIG-190-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.11">36.11.</span>Figure 190〈Reference Exported Controller Configuration State〉：caption 雖寫 Controller，內容是 namespace：ENSID=1、MS=0、RP=0；LBADS 必須與 underlying 相同。NGUID=0 時 NUUID 必須有效。</p><dl class="term-note" aria-label="本段名詞"><div><dt>ENSID</dt><dd>Exported Namespace Identifier；指定匯出的 namespace。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 190, 文件頁 158-159, PDF 頁 158-159</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>ENSID</dt><dd>Exported Namespace Identifier；指定匯出的 namespace。</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-export-state"><h2 id="heading-nvmcs-export-state"><span class="section-number">37</span> 匯出狀態的長度與一致性</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="37.01">37.01.</span>Configuration state 描述資源配置，執行中 state 描述當下的 Feature 與 controller 狀態。後者先有固定 64-byte header，再接可變長度的內容。</p>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:NVMCS13-EXPORT-STATE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="37.02">37.02.</span>Reference Exported NVM Subsystem State 保存目前 Feature values 與 controller state。CSATTR.CP=1 表示整段 Migration Receive 處理期間 controller 都處於 suspended；NVMECSS 以 dwords 指出可變 NVMECS 長度，內層 VER 固定為 1h。</p><dl class="term-note" aria-label="本段名詞"><div><dt>CSATTR.CP</dt><dd>Controller Suspended；1 表示整段 Migration Receive 處理期間皆 suspended。</dd></div><div><dt>NVMECSS</dt><dd>NVMe Controller State Size；單位 dwords，0 時可變 state 欄位不存在。</dd></div></dl><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.4.1.2</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4.1.2, 文件頁 159-160, PDF 頁 159-160</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>Feature values</td><td>保存 arbitration、power、temperature、error recovery、queues、interrupt、atomicity 與 AEC</td><td>是 current values，不是 Figure 187 defaults</td></tr><tr><td>CSATTR.CP</td><td>1 表示整段處理期間 suspended</td><td>0 不保證完全沒有 suspension</td></tr><tr><td>NVMECSS</td><td>總長度 = 64 + 4 × NVMECSS bytes</td><td>0 時 NVMECS 欄位不存在</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>CSATTR.CP</dt><dd>Controller Suspended；1 表示整段 Migration Receive 處理期間皆 suspended。</dd></div><div><dt>NVMECSS</dt><dd>NVMe Controller State Size；單位 dwords，0 時可變 state 欄位不存在。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="37.03">37.03.</span>NVMECSS=16 代表 NVMECS 有 16×4=64 bytes。加上固定 64-byte header，整個結構是 128 bytes；內層 VER 再指定這段 state 的格式版本。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:NVMCS13-NVM-FIG-191 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-191"><summary>NVM Figure 191 · Reference Exported NVM Subsystem State</summary>
<!-- claim:NVMCS13-NVM-FIG-191-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="37.04">37.04.</span>Figure 191〈Reference Exported NVM Subsystem State〉：固定 header 為 64 bytes，後接 NVMECSS×4 bytes 的 NVMECS；零長度時欄位不存在。CP=1 只證明整段 Receive 期間 suspended，內層 VER 須為 1h。</p><details class="source-note"><summary>來源：NVM Command Set 1.3 §5.4</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 191, 文件頁 159-160, PDF 頁 159-160</p></details>

</details>
</details>
</section>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:nvm-command-set-1.3-capacity -->
<details class="review-question" id="qa-nvm-command-set-1.3-capacity"><summary>1. NSZE=1000、NCAP=800、NUSE=600 時，3 個數值各回答什麼問題？</summary>
<div data-qa-answer="nvm-command-set-1.3-capacity"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="38.01">38.01.</span>NSZE 描述可定址的範圍，LBA 從 0 到 999；NCAP 描述最多可配置 800 個 logical blocks；NUSE 描述目前已配置 600 個。這些都是 logical block 數，換成 bytes 還需要 data size。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1; 4.1.5.1, 文件頁 13-14,85-93, PDF 頁 13-14,85-93</p>
</details></details>
<!-- qa:nvm-command-set-1.3-fused -->
<details class="review-question" id="qa-nvm-command-set-1.3-fused"><summary>2. 把 Compare 和 Write 相鄰放入 SQ，就能保證兩者之間沒有其他修改嗎？</summary>
<div data-qa-answer="nvm-command-set-1.3-fused"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="38.02">38.02.</span>不能只靠相鄰位置。要使用支援的 fused operation，依規則設定第 1 與第 2 個命令，並滿足相同範圍等配對條件；一般命令的提交順序不提供這種保證。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.2-2.1.3, 文件頁 14-15, PDF 頁 14-15</p>
</details></details>
<!-- qa:nvm-command-set-1.3-atomic-persistent -->
<details class="review-question" id="qa-nvm-command-set-1.3-atomic-persistent"><summary>3. 符合 atomic write 大小，是否就表示斷電後資料一定保存？</summary>
<div data-qa-answer="nvm-command-set-1.3-atomic-persistent"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="38.03">38.03.</span>Atomicity 關注規定情境下是否可能讀到部分更新；persistence 關注資料是否已保存到非揮發性媒體。仍要分別考慮 normal／power-fail atomicity、對齊邊界、volatile write cache 與 FUA／Flush 規則。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4; 4.1.3.4; 5.9, 文件頁 15-21,66-67,165, PDF 頁 15-21,66-67,165</p>
<p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4; 3.3.6, 文件頁 48-51,53-56, PDF 頁 48-51,53-56</p>
</details></details>
<!-- qa:nvm-command-set-1.3-compare-verify -->
<details class="review-question" id="qa-nvm-command-set-1.3-compare-verify"><summary>4. 已知一段預期資料，想確認媒體內容與它相同，應使用 Compare 還是 Verify？</summary>
<div data-qa-answer="nvm-command-set-1.3-compare-verify"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="38.04">38.04.</span>Compare 會使用 host 提供的比較資料。Verify 用來確認指定範圍的可讀性及適用的完整性檢查，不會把資料傳回 host，也不以一份 host 預期內容作逐項比較。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1; 3.3.5, 文件頁 27-30,51-53, PDF 頁 27-30,51-53</p>
</details></details>
<!-- qa:nvm-command-set-1.3-zero-allocation -->
<details class="review-question" id="qa-nvm-command-set-1.3-zero-allocation"><summary>5. Read 得到全零，可以推論這些 LBAs 仍然已配置嗎？</summary>
<div data-qa-answer="nvm-command-set-1.3-zero-allocation"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="38.05">38.05.</span>不能。已寫入的零資料與 deallocated block 的零值讀取行為都可能產生相同結果。要結合配置狀態、DRB，以及 DULBE 是否支援且啟用，才能解釋這次讀取。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3.2.1; 4.1.3.3, 文件頁 47-48,66, PDF 頁 47-48,66</p>
<p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7-3.3.8, 文件頁 56-61, PDF 頁 56-61</p>
</details></details>
<!-- qa:nvm-command-set-1.3-format -->
<details class="review-question" id="qa-nvm-command-set-1.3-format"><summary>6. 只知道 data size 是 4096 bytes，足以建立正確的 I/O buffer 嗎？</summary>
<div data-qa-answer="nvm-command-set-1.3-format"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="38.06">38.06.</span>還不夠。需要確認使用中的 Format Index、metadata 大小、PI 格式與 metadata 傳輸方式；separate buffer 與 extended LBA 的記憶體排列不同。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §1.1-1.6; 4.1.3.9; 4.1.4.8; 4.1.5, 文件頁 9-12,73-75,79-83, PDF 頁 9-12,73-75,79-83</p>
<p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1; 4.1.5.3; 5.6, 文件頁 85-94,96-102,160-162, PDF 頁 85-94,96-102,160-162</p>
<p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.6; 5.2.3; 5.3, 文件頁 22,129-131, PDF 頁 22,129-131</p>
</details></details>
<!-- qa:nvm-command-set-1.3-pi-checks -->
<details class="review-question" id="qa-nvm-command-set-1.3-pi-checks"><summary>7. PRACT=1 是否代表關閉所有 PI 檢查？</summary>
<div data-qa-answer="nvm-command-set-1.3-pi-checks"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="38.07">38.07.</span>PRACT 控制 PI 如何在傳輸中處理，並非總檢查開關。Guard、Application Tag、Reference Tag 的要求由 PRCHK 指定，Storage Tag 另由 STC 指定；實際傳輸內容還取決於 metadata 與 PI 大小。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5; 5.3.2-5.3.3, 文件頁 21-22,141-152, PDF 頁 21-22,141-152</p>
</details></details>
<!-- qa:nvm-command-set-1.3-rate-modes -->
<details class="review-question" id="qa-nvm-command-set-1.3-rate-modes"><summary>8. Soft Limit 為何可能觀察到高於設定值的 throughput？</summary>
<div data-qa-answer="nvm-command-set-1.3-rate-modes"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="38.08">38.08.</span>Soft Limit 允許利用尚未被其他工作使用的頻寬或 IOPS；當資源不足時才依設定比例分配。Hard Limit 則提供上限。Appendix A 的 token buckets 是說明性實作，不能視為所有 controller 的內部結構。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.10.1-5.10.2; Appendix A, 文件頁 166-168,176-177, PDF 頁 166-168,176-177</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express NVM Command Set Specification, Revision 1.3</p><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
