---
permalink: /nvme/namespace-management-zh-tw/
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4：Namespace Management：容量、建立與附加"
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
[English]({% post_url 2026-09-11-nvme-base-namespace-management-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">Namespace Management 管理主機可使用的儲存空間。建立 namespace 決定容量與格式；附加 namespace 才把它連到指定控制器。因此，存在一份儲存空間，與主機能經由某個控制器使用它，是兩個不同狀態。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div></dl>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>規劃要建立的儲存空間</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">先分清容量、格式與配置粒度：需要多少可定址空間、每個區塊多大，以及控制器建議如何配置。</span></p></article>
<article><span class="axis-number">02</span><h3>從建立走到可存取</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">Create 建立 namespace 並回傳識別碼；Attach 讓指定控制器能存取它。用這個流程理解兩種命令各自完成什麼。</span></p></article>
<article><span class="axis-number">03</span><h3>分清移除連接與刪除資料空間</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">Detach 移除控制器的存取關係，Delete 刪除 namespace；還原預設配置又有不同的前提與結果。</span></p></article>
<article><span class="axis-number">04</span><h3>讓主機得知配置變動</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="04-01">04-01</span><span class="paragraph-text">建立、附加或刪除後，其他控制器與主機看到的資訊可能改變；透過通知及重新識別更新認識。</span></p></article>
</div>
<div class="overview-connections"><h3>把主軸連起來</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">先理解容量與識別碼，再準備建立資料；Create 成功後取得 NSID，接著以 Attachment 建立存取關係。需要調整配置時，分別考慮 Detach、Delete 或還原預設配置，並處理受影響控制器收到的變更通知。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div></dl>
</div>
</section>
<section class="lesson" id="module-capacity-granularity-math"><h2 id="heading-capacity-granularity-math"><span class="section-number">01</span> 容量數值與配置粒度</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">先分清各種容量數值的單位，再比較必要的容量關係與建議配置粒度。前者決定是否符合規格要求，後者用來減少配置空間的浪費。</span></p>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 260" role="img"><title>可定址、可配置、已配置是 3 個不同的量</title><desc>教學例：NSZE=1000、NCAP=800、NUSE=600。LBA 編號的範圍與目前配置量要分開理解。</desc><rect x="20" y="20" width="720" height="70" rx="6" class="v-object"/><text x="380.0" y="48.5" text-anchor="middle" font-size="17">NSZE = 1000</text><text x="380.0" y="73.5" text-anchor="middle" font-size="17">LBA 0 … 999</text><rect x="20" y="110" width="576" height="55" rx="6" class="v-command"/><text x="308.0" y="143.5" text-anchor="middle" font-size="17">NCAP = 800</text><rect x="20" y="185" width="432" height="55" rx="6" class="v-success"/><text x="236.0" y="218.5" text-anchor="middle" font-size="17">NUSE = 600</text></svg></div><figcaption>教學例：NSZE=1000、NCAP=800、NUSE=600。LBA 編號的範圍與目前配置量要分開理解。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>NCAP</dt><dd>Namespace Capacity，任一時點最多可配置給 namespace 的 logical blocks。</dd></div><div><dt>NSZE</dt><dd>Namespace Size，namespace 的總 logical block 數，LBA 範圍為 0 到 NSZE−1。</dd></div><div><dt>NUSE</dt><dd>Namespace Utilization，目前已配置給 namespace 的 logical blocks。</dd></div></dl>
<!-- claim:BASENAMESPACE-CAPACITY-MODEL -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">Namespace Size（NSZE）是 LBA 0 到 n−1 的總 logical blocks；Namespace Capacity（NCAP）是任一時點最多可配置的 blocks；Namespace Utilization（NUSE）是目前已配置 blocks。永遠遵守 NSZE ≥ NCAP ≥ NUSE。</span></p><details class="source-note"><summary>來源：NVM Command Set 1.3 §2.1.1</summary><p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1, 文件頁 13-14, PDF 頁 13-14</p></details>
<div class="table-wrap"><table><caption>容量數值與配置粒度</caption><thead><tr><th scope="col">容量欄位</th><th scope="col">使用的單位</th><th scope="col">這個數值描述什麼</th></tr></thead><tbody><tr><td>NSZE</td><td>logical blocks</td><td>LBA 0..NSZE−1</td></tr><tr><td>NCAP</td><td>logical blocks</td><td>最大可配置容量</td></tr><tr><td>NUSE</td><td>logical blocks</td><td>THINP=1 時需追蹤</td></tr><tr><td>NSG／NCG</td><td>bytes</td><td>建議配置粒度；未符合這項建議，不能單獨成為拒絕命令的理由</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>THINP</dt><dd>Thin Provisioning，NSFEAT 中決定 NCAP 是否可小於 NSZE，以及 controller 是否必須追蹤 NUSE 的 bit。</dd></div><div><dt>NCG</dt><dd>Namespace Capacity Granularity，以 bytes 表示 controller 偏好的 NCAP allocation granularity。</dd></div><div><dt>NSG</dt><dd>Namespace Size Granularity，以 bytes 表示 controller 偏好的 NSZE allocation granularity。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">每個區塊 4 KiB、NSG=1 MiB、NCG=2 MiB。NSZE=NCAP=1024 時，1024×4 KiB=4 MiB，是兩種粒度的整數倍。改成 1000 時，1000×4 KiB=4000 KiB=3.90625 MiB，不是 1 MiB 或 2 MiB 的整數倍；可能浪費部分配置容量。但只要其他要求符合，不能只因未符合粒度建議而中止建立命令。</span></p></aside>
</section>
<section class="lesson" id="module-namespace-create-payload"><h2 id="heading-namespace-create-payload"><span class="section-number">02</span> 建立 Namespace 所需的資料</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">Base Figure 448 定義 4096-byte envelope，NVM Command Set Figure 134 只定義前 768 bytes 中的 NVM 欄位與 Placement Handle List。Host 先以 SEL／CSI 決定 operation 與 command set，再填 NSZE、NCAP、format、protection、sharing 與 group IDs。Reserved areas 要清零，Protection Information 與 FDP 又各有獨立 功能支援條件。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Protection Information</dt><dd>資料保護資訊，縮寫 PI；包含 Guard 與 tags，用來檢查資料及其關聯資訊。</dd></div><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div><div><dt>CSI</dt><dd>I/O Command Set Identifier；選擇 I/O 命令集，NVM Command Set 使用 00h。</dd></div><div><dt>FDP</dt><dd>Flexible Data Placement，把資料放置提示與媒體回收管理連結的能力。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div><div><dt>SEL</dt><dd>Select；Namespace Management 的 create/delete/restore selector，與 Get Features 的 SEL 不同。</dd></div></dl>
<!-- claim:BASENAMESPACE-CREATE-BASE-COMMAND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">Create 使用 NSID=0、SEL=0h 與 CSI=00h（NVM Command Set）。DPTR 指向 4096-byte data structure：bytes 0:511 是 I/O Command Set specific、512:1023 reserved、1024:4095 vendor specific。reserved bytes 由 host 清為 0。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>DPTR</dt><dd>Data Pointer，SQE 中指出 command data buffer 的欄位。</dd></div><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §5.2.25</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 文件頁 446-448, PDF 頁 472-474</p></details>
<div class="table-wrap"><table><caption>建立 Namespace 所需的資料</caption><thead><tr><th scope="col">資料區域與解讀格式</th><th scope="col">該區域的用途</th><th scope="col">欄位有效的條件</th></tr></thead><tbody><tr><td>Base 0:511</td><td>SIOCS</td><td>NVM-specific create data</td></tr><tr><td>Base 512:1023</td><td>Reserved</td><td>host 清 0</td></tr><tr><td>Base 1024:4095</td><td>Vendor Specific</td><td>沒有來源定義就不猜</td></tr><tr><td>NVM 512:767</td><td>Placement Handle List</td><td>只在 FDP enable 時驗證</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>SIOCS</dt><dd>Specified I/O Command Set，Base create buffer bytes 0:511 中放置所選 I/O Command Set specific fields 的區域。</dd></div></dl>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">建立 4 MiB namespace：LBA=4096 bytes、NSZE=NCAP=1024，因此 bytes 7:0 與 15:8 都寫 0000000000000400h。NVMSETID=0、ENDGID=5 表示由 Endurance Group 5 內選 NVM Set；反過來 NVMSETID=7、ENDGID=0 是 Invalid Field。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>Endurance Group</dt><dd>Endurance Group，用於隔離與回報耐久度相關狀態的 NVM 資源群組。</dd></div><div><dt>NVMSETID</dt><dd>NVM Set Identifier，指定建立 namespace 時要從哪個 NVM Set 配置容量。</dd></div><div><dt>NVM Set</dt><dd>NVM Set，把 namespace 與一組共同管理的 NVM 資源建立關聯的容量集合。</dd></div><div><dt>ENDGID</dt><dd>Endurance Group Identifier，指定建立 namespace 時所屬 Endurance Group。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-namespace-lifecycle"><h2 id="heading-namespace-lifecycle"><span class="section-number">03</span> 建立、連接與使用 Namespace</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">Create、Attach、Detach、Delete 分別改變兩個狀態維度：namespace 是否 allocated，以及某 controller 是否 attached。Create CQE.DW0 回 NSID 後，object 已 allocated 但所有 controller 都未 attached；Attach 的 Controller List 才建立 access。Detach 不刪容量，Delete 才使 NSID unallocated。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div></dl>
<figure><figcaption><strong>Namespace 從建立到可存取</strong></figcaption><ol class="flow-steps"><li>建立 namespace，取得 NSID。</li><li>將 namespace 附加至指定 controller。</li><li>由該 controller 的 Identify 結果確認 namespace 與格式。</li><li>I/O 命令使用 NSID 指定要存取的 namespace。</li></ol><figcaption>建立儲存物件與讓 controller 可以存取它，是分開的動作。</figcaption></figure>

<!-- claim:BASENAMESPACE-NSMGMT-CAPABILITY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span><span class="paragraph-text">完整 Namespace Management capability 由 Namespace Management command 與 Namespace Attachment command 組成。支援時 controller 必須支援兩者、設 OACS.NMS=1、支援 Attached Namespace Attribute Changed event；Allocated event 為 should，Namespace Granularity 與 Restore Default 為 may。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>OACS.NMS</dt><dd>Optional Admin Command Support 的 Namespace Management Supported bit；設為 1 才宣告完整 Manage 加 Attach capability。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §8.1.17</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 660, PDF 頁 686</p></details>
<div class="table-wrap"><table><caption>建立、連接與使用 Namespace</caption><thead><tr><th scope="col">管理動作</th><th scope="col">改變哪個物件或關係</th><th scope="col">操作後仍保留什麼</th></tr></thead><tbody><tr><td>Create</td><td>object／capacity</td><td>不自動 attach</td></tr><tr><td>Attach</td><td>access relationship</td><td>Controller List 可含多個 CNTLID</td></tr><tr><td>Detach</td><td>對指定控制器的可存取狀態</td><td>namespace 仍 allocated</td></tr><tr><td>Delete</td><td>subsystem inventory</td><td>NSID 變 unallocated</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.03">03.03.</span><span class="paragraph-text">Create 回 NSID=7。Controller List 的 NUMCIDS 與 entries 指定 controllers 3、5；Attach 成功後 NSID 7 對 3、5 active。再只 detach controller 3，NSID 7 對 3 inactive、對 5 仍 active，namespace 本身仍 allocated。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>NUMCIDS</dt><dd>Number of Controller Identifiers；Controller List 中有效 controller IDs 的數量。</dd></div></dl></aside>
</section>
<section class="lesson" id="module-delete-restore-state"><h2 id="heading-delete-restore-state"><span class="section-number">04</span> 刪除與恢復預設配置</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">Delete all 與 Restore Default 是兩個不同 operation。NSID=FFFFFFFFh 的 Delete All 在零個 namespaces 時也成功；Restore Default 則要求 RDNCS capability、SEL=2h，以及 subsystem 中已不存在任何 namespace。成功前 controller 套用 current active firmware image defaults 並設 DNCS=1。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>RDNCS</dt><dd>Restore Default Namespace Configuration Supported，宣告 Restore Default operation 是否支援的 capability bit。</dd></div><div><dt>DNCS</dt><dd>Default Namespace Configuration Status，表示目前 namespace configuration 是否等於 active firmware image defaults 的 status bit。</dd></div></dl>
<!-- claim:BASENAMESPACE-DELETE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">Delete 的 NSID 指定已建立 namespace；FFFFFFFFh 表示 delete all，即使目前零個 namespaces 也成功。delete 會使 namespace 從 subsystem 消失並具有 detach side effect；host 應先 detach 所有 controllers，讓 event 與 outstanding-I/O 行為更可控。</span></p><details class="source-note"><summary>來源：Base 2.4 §5.2.25, 8.1.17.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446, 448, 662, PDF 頁 472, 474, 688</p></details>
<div class="table-wrap"><table><caption>刪除與恢復預設配置</caption><thead><tr><th scope="col">刪除或恢復動作</th><th scope="col">命令如何選對象</th><th scope="col">完成後如何確認配置</th></tr></thead><tbody><tr><td>Delete one</td><td>NSID=target</td><td>成功後 object 消失</td></tr><tr><td>Delete all</td><td>NSID=FFFFFFFFh</td><td>zero namespace 仍成功</td></tr><tr><td>Restore</td><td>SEL=2h、NSID ignored</td><td>剩餘 namespace→Sequence Error</td></tr><tr><td>Post-condition</td><td>DNCS=1</td><td>仍要重新 Identify actual defaults</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.03">04.03.</span><span class="paragraph-text">先 detach NSID 7，再 Delete 7；讀 Allocated Namespace ID list 確認為空。若 RDNCS=1，送 SEL=2h、NSID=0。CQE success 後讀 DNCS=1，最後重新列舉 default namespaces；DNCS 是狀態證據，不是 default layout 的完整描述。</span></p></aside>
</section>
<section class="lesson" id="module-namespace-events"><h2 id="heading-namespace-events"><span class="section-number">05</span> Namespace 變更通知與重新辨識</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span><span class="paragraph-text">Attached 與 Allocated Namespace Attribute Changed notices 對應不同 inventory。Create 通常改 Allocated list；Attach／Detach 改 Active list；Delete 可能同時改兩者。event code 不是新清單本身，因此 host 收到 AEN 後要依 CNS 重新 Identify。Delete reporting 還要分辨 processing controller 與其他 controllers。</span></p><dl class="term-note" aria-label="本段名詞"><div><dt>AEN</dt><dd>Asynchronous Event Notification，controller 透過已提交 Asynchronous Event Request 回報事件的通知。</dd></div><div><dt>CNS</dt><dd>Controller or Namespace Structure；Identify 命令用來選擇回傳資料結構的欄位。</dd></div></dl>
<!-- claim:BASENAMESPACE-NAMESPACE-EVENTS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.02">05.02.</span><span class="paragraph-text">create 改變 Allocated Namespace ID list；attach／detach 改變 Active Namespace ID list；delete 可能同時改變兩者。啟用對應 notice 時，host 收到 asynchronous event 後應重新 Identify，而不是只用 event code 猜新 inventory。§8.1.17.2 對處理 delete 的 controller 與其他 controllers 規定不同 event reporting。</span></p><details class="source-note"><summary>來源：Base 2.4 §8.1.17.1-8.1.17.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17.1-8.1.17.2, 文件頁 662-663, PDF 頁 688-689</p></details>
<div class="table-wrap"><table><caption>Namespace 變更通知與重新辨識</caption><thead><tr><th scope="col">通知或清單</th><th scope="col">描述哪種配置變化</th><th scope="col">應重新查詢什麼</th></tr></thead><tbody><tr><td>CNS 02h</td><td>Active Namespace ID list</td><td>Attached notice</td></tr><tr><td>CNS 10h</td><td>Allocated Namespace ID list</td><td>Allocated notice</td></tr><tr><td>Create</td><td>Allocated change</td><td>新 NSID 尚未 active</td></tr><tr><td>Delete</td><td>Allocated＋可能 Active</td><td>processing controller 規則不同</td></tr></tbody></table></div>
<aside class="worked-example"><h3>說明性範例</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="05.03">05.03.</span><span class="paragraph-text">Controller 3 處理 attached NSID 7 的 Delete。其他已啟用 notice 的 controllers 依 §8.1.17.2 回報；processing controller 的要求不同。host 不應只計算 event 數量，而要為每個 controller 保存 before/after Active 與 Allocated lists。</span></p></aside>
</section>
<section id="spec-reading"><h2>接著打開 Spec 看什麼</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.01">06.01.</span><span class="paragraph-text">以下按概念列出閱讀位置。報告時先用上面的流程說明問題，再打開對應章節看欄位與完整條件。中文教學 HTML 另有本篇全部圖表的逐圖重點、案例與細節。</span></p>
<div class="table-wrap"><table><thead><tr><th scope="col">要說明的觀念</th><th scope="col">Spec 閱讀位置</th></tr></thead><tbody><tr><td>容量數值與配置粒度</td><td>NVM 1.3 §2.1.1 · Base 2.4 §8.1.17 · NVM 1.3 §5.8</td></tr><tr><td>建立 Namespace 所需的資料</td><td>Base 2.4 §5.2.25 · NVM 1.3 §4.1.6.4 · NVM 1.3 §4.1.6.2 · NVM 1.3 §4.1.6.3 · Base 2.4 §8.1.17</td></tr><tr><td>建立、連接與使用 Namespace</td><td>Base 2.4 §8.1.17 · Base 2.4 §5.2.24 · Base 2.4 §5.2.25, 8.1.17.1</td></tr><tr><td>刪除與恢復預設配置</td><td>Base 2.4 §5.2.25, 8.1.17.1 · Base 2.4 §5.2.25.1 · Base 2.4 §8.1.17.1-8.1.17.2</td></tr><tr><td>Namespace 變更通知與重新辨識</td><td>Base 2.4 §8.1.17 · Base 2.4 §8.1.17.1-8.1.17.2 · Base 2.4 §5.2.25, 8.1.17.1 · Base 2.4 §5.2.24-5.2.25</td></tr></tbody></table></div>
<a class="reading-link" href="/DOCS/nvme-spec-report/base-namespace-management/tutorial-zh-tw.html">開啟完整中文教學與逐圖解釋 →</a></section>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:base-namespace-management-1 -->
<details class="review-question" id="qa-base-namespace-management-1"><summary>1. Namespace Create 成功並回傳 NSID，為何還不能直接假設某 controller 可以對它做 I/O？</summary>
<div data-qa-answer="base-namespace-management-1"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.01">07.01.</span><span class="paragraph-text">Create 建立 namespace；Attachment 決定哪些 controllers 可以存取。還要確認 attachment 與 Identify 所回報的可見性、格式及可用狀態。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446-448, 662, PDF 頁 472-474, 688</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.24, 文件頁 444-445, PDF 頁 470-471</p>
</details></details>
<!-- qa:base-namespace-management-2 -->
<details class="review-question" id="qa-base-namespace-management-2"><summary>2. Namespace granularity hint 與實際媒體配置的 rounding，為何不能混為一談？</summary>
<div data-qa-answer="base-namespace-management-2"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.02">07.02.</span><span class="paragraph-text">Hint 協助 host 選擇合適的 size 或 capacity；rounding 描述實際配置可能耗用的資源。Hint 不是任意加上的命令合法性限制，容量規劃也不能只看 host 要求的數值。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §8.1.17, 文件頁 661, PDF 頁 687</p>
<p>來源：NVME-NVM-CS-1.3, Rev. 1.3, §5.8, 文件頁 165, PDF 頁 165</p>
</details></details>
<!-- qa:base-namespace-management-3 -->
<details class="review-question" id="qa-base-namespace-management-3"><summary>3. Restore Default Namespace 是否表示恢復已刪除 namespace 的原有資料？</summary>
<div data-qa-answer="base-namespace-management-3"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.03">07.03.</span><span class="paragraph-text">它處理預設 namespace 配置，不是資料復原命令。Namespace 的建立、刪除與預設配置流程，不能被當成保留或找回舊資料的保證。</span></p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25.1, 文件頁 447-448, PDF 頁 473-474</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §5.2.25, 8.1.17.1, 文件頁 446, 448, 662, PDF 頁 472, 474, 688</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express NVM Command Set Specification, Revision 1.3</p><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
