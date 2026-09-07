---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4 第 3 章：Controller、Queue、初始化與重設"
date: 2026-08-28
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
[English]({% post_url 2026-08-28-nvme-base-ch3-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-hidden="true">01.</span>控制器開始處理 I/O 之前，需要先建立可用的介面、佇列與狀態。本篇沿著控制器的運作生命週期，連起能力查詢、初始化、命令處理、記憶體資源，以及關機、重設與韌體啟用。</p><dl class="term-note" aria-label="本段名詞"><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>啟動與能力</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-hidden="true">02.</span>從識別控制器，到設定必要 properties 與確認可處理命令。</p></article>
<article><span class="axis-number">02</span><h3>佇列與命令處理</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-hidden="true">03.</span>理解佇列位置、Doorbell 更新與仲裁分工。</p></article>
<article><span class="axis-number">03</span><h3>資源與生命週期</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-hidden="true">04.</span>區分容量、控制器記憶體與各種狀態改變的影響範圍。</p></article>
</div>

<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">05.</span>提交佇列保存主機送出的命令，完成佇列保存控制器回報的結果。主機要先建立這些共同機制，再使用讀寫等命令；以下從這個先後關係展開。</p>
</section>
<section class="lesson" id="module-identity"><h2 id="heading-identity"><span class="section-number">01</span> Controller 類型、識別碼與能力</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">06.</span>Controller type 回答『能做哪類工作』，Controller ID 回答『這是哪一個 controller』，support-requirement Figure 回答『在這個上下文中 command／log／feature 的支援強度』。Figures 23-32 應連續閱讀，但三種問題不能合併成一個布林值。</p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASE3-STATIC -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">07.</span>memory-based controller 必須（shall）只支援 static controller model。</p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.1, 文件頁 38, PDF 頁 64</p></details>
<!-- claim:BASE3-TYPES -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">08.</span>本輪只使用 I/O controller 與 Administrative controller：前者可執行使用者資料的 I/O，後者以管理為目的且不支援資料 I/O command。兩者都具有一組 Admin Submission／Completion Queue。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Administrative controller</dt><dd>Administrative controller，以管理為目的且不執行使用者資料 I/O command 的 controller 類型。</dd></div><div><dt>I/O controller</dt><dd>I/O controller，可執行使用者資料 I/O command 的 controller 類型。</dd></div><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.3-3.1.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3-3.1.3.2, 文件頁 39-43, PDF 頁 65-69</p></details>
<!-- claim:BASE3-ORDER -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">09.</span>除 fused operation 外，controller 取走的命令與完成沒有一般性的先後保證；若有順序需求，強制該順序是 host 的責任。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3, 文件頁 40, PDF 頁 66</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>I/O controller</td><td>可執行使用者資料 I/O</td><td>仍需逐項查 optional capability</td></tr><tr><td>Administrative controller</td><td>管理用途、無資料 I/O command</td><td>不能因有 Admin Queue 就當成 I/O controller</td></tr><tr><td>support marker</td><td>針對 row 與上下文描述強度</td><td>不能脫離 column／footnote 解讀</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>Administrative controller</dt><dd>Administrative controller，以管理為目的且不執行使用者資料 I/O command 的 controller 類型。</dd></div><div><dt>I/O controller</dt><dd>I/O controller，可執行使用者資料 I/O command 的 controller 類型。</dd></div><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">10.</span>說明性範例：偵測到一個 Administrative controller 時，軟體仍會建立 Admin SQ/CQ 並執行管理 command，但不應把 namespace data path 掛到它。若只用『存在 Admin Queue』判斷 controller type，I/O 與 Administrative controller 會被錯誤歸成同類。</p><dl class="term-note" aria-label="本段名詞"><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div><div><dt>CQ</dt><dd>Completion Queue，controller 放入完成結果的完成佇列。</dd></div><div><dt>SQ</dt><dd>Submission Queue，主機放入命令的提交佇列。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:BASE3-FIG-023 -->
<details class="field-note" id="figure-BASE3-FIG-023"><summary>Base Figure 23 · Controller Types</summary>
<!-- claim:BASE3-FIG-023-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">11.</span>Figure 23〈Controller Types〉：呈現〈Controller Types〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3, Figure 23, 文件頁 39, PDF 頁 65</p></details>

</details>
<!-- figure-table:BASE3-FIG-024 -->
<details class="field-note" id="figure-BASE3-FIG-024"><summary>Base Figure 24 · NVM Subsystem with Three I/O Controllers</summary>
<!-- claim:BASE3-FIG-024-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">12.</span>Figure 24〈NVM Subsystem with Three I/O Controllers〉：呈現〈NVM Subsystem with Three I/O Controllers〉中的物件或容量關係。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.1, Figure 24, 文件頁 41, PDF 頁 67</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-025 -->
<details class="field-note" id="figure-BASE3-FIG-025"><summary>Base Figure 25 · NVM Subsystem with One Administrative and Two I/O Controllers</summary>
<!-- claim:BASE3-FIG-025-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">13.</span>Figure 25〈NVM Subsystem with One Administrative and Two I/O Controllers〉：呈現〈NVM Subsystem with One Administrative and Two I/O Controllers〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.2, Figure 25, 文件頁 42, PDF 頁 68</p></details>

</details>
<!-- figure-table:BASE3-FIG-026 -->
<details class="field-note" id="figure-BASE3-FIG-026"><summary>Base Figure 26 · NVM Subsystem with One Administrative Controller</summary>
<!-- claim:BASE3-FIG-026-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">14.</span>Figure 26〈NVM Subsystem with One Administrative Controller〉：呈現〈NVM Subsystem with One Administrative Controller〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.2, Figure 26, 文件頁 42, PDF 頁 68</p></details>

</details>
<!-- figure-table:BASE3-FIG-027 -->
<details class="field-note" id="figure-BASE3-FIG-027"><summary>Base Figure 27 · Controller IDs FFF0h to FFFFh</summary>
<!-- claim:BASE3-FIG-027-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">15.</span>Figure 27〈Controller IDs FFF0h to FFFFh〉：定義〈Controller IDs FFF0h to FFFFh〉的識別碼組成或數值空間。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.3.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.3, Figure 27, 文件頁 44, PDF 頁 70</p></details>

</details>
<!-- figure-table:BASE3-FIG-028 -->
<details class="field-note" id="figure-BASE3-FIG-028"><summary>Base Figure 28 · Admin Command Support Requirements</summary>
<!-- claim:BASE3-FIG-028-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">16.</span>Figure 28〈Admin Command Support Requirements〉：統整〈Admin Command Support Requirements〉指定的支援等級。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.3.3.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.3.3, Figure 28, 文件頁 45-47, PDF 頁 71-73</p></details>

</details>
<!-- figure-table:BASE3-FIG-030 -->
<details class="field-note" id="figure-BASE3-FIG-030"><summary>Base Figure 30 · Common I/O Command Support Requirements</summary>
<!-- claim:BASE3-FIG-030-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">17.</span>Figure 30〈Common I/O Command Support Requirements〉：統整〈Common I/O Command Support Requirements〉指定的支援等級。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.3.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.4, Figure 30, 文件頁 47-48, PDF 頁 73-74</p></details>

</details>
<!-- figure-table:BASE3-FIG-031 -->
<details class="field-note" id="figure-BASE3-FIG-031"><summary>Base Figure 31 · Log Page Support Requirements</summary>
<!-- claim:BASE3-FIG-031-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">18.</span>Figure 31〈Log Page Support Requirements〉：統整〈Log Page Support Requirements〉指定的支援等級。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.3.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.4, Figure 31, 文件頁 48-50, PDF 頁 74-76</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>FDP</dt><dd>Flexible Data Placement，把資料放置提示與媒體回收管理連結的能力。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-032 -->
<details class="field-note" id="figure-BASE3-FIG-032"><summary>Base Figure 32 · Feature Support Requirements</summary>
<!-- claim:BASE3-FIG-032-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">19.</span>Figure 32〈Feature Support Requirements〉：統整〈Feature Support Requirements〉指定的支援等級。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.3.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.3.5, Figure 32, 文件頁 50-52, PDF 頁 76-78</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-properties-init"><h2 id="heading-properties-init"><span class="section-number">02</span> 從設定到 CSTS.RDY：初始化流程</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">20.</span>Properties 不是彼此獨立的 register 清單。CAP 先限制 page size、queue 與 timeout 能力；AQA、ASQ、ACQ 建立 Admin queues；CC 選擇設定並以 EN 啟動；最後由 CSTS.RDY 宣告 controller 已能正常處理命令。Figures 33-46 與 Figure 57 應沿這條因果鏈閱讀。</p><dl class="term-note" aria-label="本段名詞"><div><dt>CSTS</dt><dd>Controller Status，controller 回報 ready、fatal status 與 shutdown 狀態的 property。</dd></div><div><dt>ACQ</dt><dd>Admin Completion Queue Base Address，Admin CQ 在可定址記憶體中的基底位址。</dd></div><div><dt>AQA</dt><dd>Admin Queue Attributes，描述 Admin SQ 與 Admin CQ 大小的 property。</dd></div><div><dt>ASQ</dt><dd>Admin Submission Queue Base Address，Admin SQ 在可定址記憶體中的基底位址。</dd></div><div><dt>CAP</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。</dd></div><div><dt>RDY</dt><dd>Ready，CSTS 中表示 controller 是否已準備正常處理 command 的 bit。</dd></div><div><dt>CC</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。</dd></div><div><dt>EN</dt><dd>Enable，CC 中控制 controller enable state 的 bit。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASE3-PROPERTY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">21.</span>host 必須（shall）以 property 指定的寬度，從 property 起始 offset 存取；memory-based controller 的實際存取規則由 PCIe Transport 補充。</p><dl class="term-note" aria-label="本段名詞"><div><dt>offset</dt><dd>offset；從指定起點算出的位移。它回答「離起點多遠」，不等於 index。</dd></div><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div><div><dt>PCIe</dt><dd>PCI Express，NVMe memory-based controller 使用的 transport 與裝置互連。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, 文件頁 52-54, PDF 頁 78-80</p></details>
<!-- claim:BASE3-INIT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">22.</span>PCIe 初始化以 CAP 判斷能力與 timeout，設定 AQA／ASQ／ACQ 與 CC，接著等待 CSTS.RDY。ready mode 與 CRTO 會影響 host 等待與錯誤處理。</p><dl class="term-note" aria-label="本段名詞"><div><dt>CRTO</dt><dd>Controller Ready Timeouts，回報特定 ready mode 所需等待時間的 property。</dd></div><div><dt>CSTS</dt><dd>Controller Status，controller 回報 ready、fatal status 與 shutdown 狀態的 property。</dd></div><div><dt>PCIe</dt><dd>PCI Express，NVMe memory-based controller 使用的 transport 與裝置互連。</dd></div><div><dt>ACQ</dt><dd>Admin Completion Queue Base Address，Admin CQ 在可定址記憶體中的基底位址。</dd></div><div><dt>AQA</dt><dd>Admin Queue Attributes，描述 Admin SQ 與 Admin CQ 大小的 property。</dd></div><div><dt>ASQ</dt><dd>Admin Submission Queue Base Address，Admin SQ 在可定址記憶體中的基底位址。</dd></div><div><dt>CAP</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。</dd></div><div><dt>RDY</dt><dd>Ready，CSTS 中表示 controller 是否已準備正常處理 command 的 bit。</dd></div><div><dt>CC</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.5.1, 3.5.3-3.5.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, 文件頁 105-113, PDF 頁 131-139</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>CAP</td><td>能力與界限</td><td>在寫設定前讀</td></tr><tr><td>AQA/ASQ/ACQ</td><td>Admin queue 大小與位址</td><td>需符合 page/alignment 能力</td></tr><tr><td>CC</td><td>host 選擇與 enable</td><td>寫入值要與 CAP 相容</td></tr><tr><td>CSTS</td><td>controller 回報狀態</td><td>RDY/CFS/SHST 不可互相替代</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>SHST</dt><dd>Shutdown Status，CSTS 中由 controller 回報 shutdown 進度的欄位。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">23.</span>說明性範例：host 選擇 4 KiB MPS，ASQ 與 ACQ base address 因而必須依該 page size 對齊。寫 CC.EN=1 後，host 以 CAP／CRTO 指定的時間界限等待 CSTS.RDY=1；若 CFS 先出現，流程應進入 error recovery，而不是繼續建立 I/O queues。</p><dl class="term-note" aria-label="本段名詞"><div><dt>CRTO</dt><dd>Controller Ready Timeouts，回報特定 ready mode 所需等待時間的 property。</dd></div><div><dt>MPS</dt><dd>Memory Page Size，controller 使用的 memory page 大小設定；影響 queue address 與 PRP 對齊。</dd></div><div><dt>EN</dt><dd>Enable，CC 中控制 controller enable state 的 bit。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:BASE3-FIG-033 -->
<details class="field-note" id="figure-BASE3-FIG-033"><summary>Base Figure 33 · Property Definition</summary>
<!-- claim:BASE3-FIG-033-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">24.</span>Figure 33〈Property Definition〉：定義〈Property Definition〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, Figure 33, 文件頁 52-53, PDF 頁 78-79</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>OFST</dt><dd>Offset，Firmware Image Download 中以 dword 為單位的 image-relative offset。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-034 -->
<details class="field-note" id="figure-BASE3-FIG-034"><summary>Base Figure 34 · Memory-Based Property Definition</summary>
<!-- claim:BASE3-FIG-034-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">25.</span>Figure 34〈Memory-Based Property Definition〉：定義〈Memory-Based Property Definition〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, Figure 34, 文件頁 54, PDF 頁 80</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CAP.DSTRD</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.DSTRD 進一步指定其中的 DSTRD 子欄位。</dd></div><div><dt>DSTRD</dt><dd>Doorbell Stride，CAP 中決定相鄰 doorbell register 間距的欄位。</dd></div><div><dt>OFST</dt><dd>Offset，Firmware Image Download 中以 dword 為單位的 image-relative offset。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-036 -->
<details class="field-note" id="figure-BASE3-FIG-036"><summary>Base Figure 36 · Offset 0h: CAP - Controller Capabilities</summary>
<!-- claim:BASE3-FIG-036-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">26.</span>Figure 36〈Offset 0h: CAP - Controller Capabilities〉：定義 offset 0h 的 CAP（Controller Capabilities），並指出軟體在該位置必須分別依欄位換算的欄位。</p><dl class="term-note" aria-label="本段名詞"><div><dt>offset</dt><dd>offset；從指定起點算出的位移。它回答「離起點多遠」，不等於 index。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.4.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, 文件頁 55-58, PDF 頁 81-84</p></details>

</details>
<!-- figure-table:BASE3-FIG-037 -->
<details class="field-note" id="figure-BASE3-FIG-037"><summary>Base Figure 37 · Specification Version Descriptor</summary>
<!-- claim:BASE3-FIG-037-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">27.</span>Figure 37〈Specification Version Descriptor〉：定義〈Specification Version Descriptor〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 37, 文件頁 58, PDF 頁 84</p></details>

</details>
<!-- figure-table:BASE3-FIG-038 -->
<details class="field-note" id="figure-BASE3-FIG-038"><summary>Base Figure 38 · NVM Express Base Specification Version Property Reset Values</summary>
<!-- claim:BASE3-FIG-038-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">28.</span>Figure 38〈NVM Express Base Specification Version Property Reset Values〉：定義〈NVM Express Base Specification Version Property Reset Values〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 38, 文件頁 58-59, PDF 頁 84-85</p></details>

</details>
<!-- figure-table:BASE3-FIG-041 -->
<details class="field-note" id="figure-BASE3-FIG-041"><summary>Base Figure 41 · Offset 14h: CC - Controller Configuration</summary>
<!-- claim:BASE3-FIG-041-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">29.</span>Figure 41〈Offset 14h: CC - Controller Configuration〉：定義 offset 14h 的 CC（Controller Configuration），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.5, Figure 41, 文件頁 60-63, PDF 頁 86-89</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>MPS</dt><dd>Memory Page Size，controller 使用的 memory page 大小設定；影響 queue address 與 PRP 對齊。</dd></div><div><dt>SHN</dt><dd>Shutdown Notification，CC 中由 host 宣告 shutdown 類型的欄位。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-042 -->
<details class="field-note" id="figure-BASE3-FIG-042"><summary>Base Figure 42 · Offset 1Ch: CSTS - Controller Status</summary>
<!-- claim:BASE3-FIG-042-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">30.</span>Figure 42〈Offset 1Ch: CSTS - Controller Status〉：定義 offset 1Ch 的 CSTS（Controller Status），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.5, Figure 42, 文件頁 63-65, PDF 頁 89-91</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>SHST</dt><dd>Shutdown Status，CSTS 中由 controller 回報 shutdown 進度的欄位。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-044 -->
<details class="field-note" id="figure-BASE3-FIG-044"><summary>Base Figure 44 · Offset 24h: AQA - Admin Queue Attributes</summary>
<!-- claim:BASE3-FIG-044-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">31.</span>Figure 44〈Offset 24h: AQA - Admin Queue Attributes〉：定義 offset 24h 的 AQA（Admin Queue Attributes），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 44, 文件頁 66, PDF 頁 92</p></details>

</details>
<!-- figure-table:BASE3-FIG-045 -->
<details class="field-note" id="figure-BASE3-FIG-045"><summary>Base Figure 45 · Offset 28h: ASQ - Admin Submission Queue Base Address</summary>
<!-- claim:BASE3-FIG-045-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">32.</span>Figure 45〈Offset 28h: ASQ - Admin Submission Queue Base Address〉：定義 offset 28h 的 ASQ（Admin Submission Queue Base Address），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 45, 文件頁 66, PDF 頁 92</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CC.MPS</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.MPS 進一步指定其中的 MPS 子欄位。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-046 -->
<details class="field-note" id="figure-BASE3-FIG-046"><summary>Base Figure 46 · Offset 30h: ACQ - Admin Completion Queue Base Address</summary>
<!-- claim:BASE3-FIG-046-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">33.</span>Figure 46〈Offset 30h: ACQ - Admin Completion Queue Base Address〉：定義 offset 30h 的 ACQ（Admin Completion Queue Base Address），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.9</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.9, Figure 46, 文件頁 67, PDF 頁 93</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CC.MPS</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.MPS 進一步指定其中的 MPS 子欄位。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-057 -->
<details class="field-note" id="figure-BASE3-FIG-057"><summary>Base Figure 57 · Offset 68h: CRTO - Controller Ready Timeouts</summary>
<!-- claim:BASE3-FIG-057-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">34.</span>Figure 57〈Offset 68h: CRTO - Controller Ready Timeouts〉：定義 offset 68h 的 CRTO（Controller Ready Timeouts），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.21</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.21, Figure 57, 文件頁 73, PDF 頁 99</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CAP.CRMS.CRIMS</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.CRMS.CRIMS 進一步指定其中的 CRMS.CRIMS 子欄位。</dd></div><div><dt>CC.CRIME</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.CRIME 進一步指定其中的 CRIME 子欄位。</dd></div><div><dt>CC.EN</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.EN 進一步指定其中的 EN 子欄位。</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-queue-arbitration"><h2 id="heading-queue-arbitration"><span class="section-number">03</span> Queue 位置與命令選取</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">35.</span>Figure 73/74 說明 queue 的 empty/full 判定，Figure 80/81 說明多個 SQ 競爭 controller 服務時的 arbitration。前者處理單一 ring 的 head/tail 狀態，後者處理多個 candidate SQ 的選擇；priority 屬於 SQ，不是每筆 command 自帶的獨立優先權。</p><dl class="term-note" aria-label="本段名詞"><div><dt>SQ</dt><dd>Submission Queue，主機放入命令的提交佇列。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASE3-QUEUE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">36.</span>PCIe queue 由 host-addressable memory 中的環形 buffer、head 與 tail pointer 構成。host 建立 I/O Completion Queue 後再建立對應 Submission Queue，並以 doorbell 推進 pointer。</p><details class="source-note"><summary>來源：Base 2.4 §3.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1, 文件頁 88-91, PDF 頁 114-117</p></details>
<!-- claim:BASE3-PROCESS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">37.</span>command processing 要分開看 ordering、fused／atomic semantics、arbitration 與 outstanding command 上限；priority 屬於 Submission Queue，不是每一筆 command 的獨立欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.4.1-3.4.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, 文件頁 101-105, PDF 頁 127-131</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>empty</td><td>head == tail 且 phase／ownership 符合 empty 定義</td><td>沒有可取走 entry</td></tr><tr><td>full</td><td>下一個 tail 會追上尚未釋放 head</td><td>host 不得覆寫 entry</td></tr><tr><td>Round Robin</td><td>候選 SQ 輪流取得服務</td><td>不代表 command completion 依提交順序</td></tr><tr><td>Weighted RR + Urgent</td><td>priority class 與 weight 影響選擇</td><td>仍需依適用設定解讀</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">38.</span>說明性範例：深度 4 的 SQ 只有四個 slot，但 full/empty 判定還需要 ownership 規則；不能只用 tail-head 的無號差值。若 SQ 1 與 SQ 2 同時有 command，arbiter 先選 SQ 2 也不代表 SQ 2 的 command 一定先完成，因 command 執行時間仍可能不同。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:BASE3-FIG-073 -->
<details class="field-note" id="figure-BASE3-FIG-073"><summary>Base Figure 73 · Empty Queue Definition</summary>
<!-- claim:BASE3-FIG-073-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">39.</span>Figure 73〈Empty Queue Definition〉：定義〈Empty Queue Definition〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.3.1.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1.4, Figure 73, 文件頁 91, PDF 頁 117</p></details>

</details>
<!-- figure-table:BASE3-FIG-074 -->
<details class="field-note" id="figure-BASE3-FIG-074"><summary>Base Figure 74 · Full Queue Definition</summary>
<!-- claim:BASE3-FIG-074-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">40.</span>Figure 74〈Full Queue Definition〉：定義〈Full Queue Definition〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.3.1.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1.4, Figure 74, 文件頁 91, PDF 頁 117</p></details>

</details>
<!-- figure-table:BASE3-FIG-080 -->
<details class="field-note" id="figure-BASE3-FIG-080"><summary>Base Figure 80 · Round Robin Arbitration</summary>
<!-- claim:BASE3-FIG-080-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">41.</span>Figure 80〈Round Robin Arbitration〉：呈現〈Round Robin Arbitration〉如何在多個 Submission Queue 間選擇工作。</p><details class="source-note"><summary>來源：Base 2.4 §3.4.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.4.4, Figure 80, 文件頁 103, PDF 頁 129</p></details>

</details>
<!-- figure-table:BASE3-FIG-081 -->
<details class="field-note" id="figure-BASE3-FIG-081"><summary>Base Figure 81 · Weighted Round Robin with Urgent Priority Class Arbitration</summary>
<!-- claim:BASE3-FIG-081-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">42.</span>Figure 81〈Weighted Round Robin with Urgent Priority Class Arbitration〉：呈現〈Weighted Round Robin with Urgent Priority Class Arbitration〉如何在多個 Submission Queue 間選擇工作。</p><details class="source-note"><summary>來源：Base 2.4 §3.4.4.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.4.4.2, Figure 81, 文件頁 104, PDF 頁 130</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-memory-capacity"><h2 id="heading-memory-capacity"><span class="section-number">04</span> Namespace、CMB、PMR 與容量</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">43.</span>CMB/PMR properties 描述 controller 暴露的 memory region 位置、能力與狀態；capacity Figures 86-89 描述 NVM subsystem 各層級可用或已配置容量。兩者都談 memory，卻不是同一種空間，也不能用同一個『剩餘容量』欄位合併。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NVM subsystem</dt><dd>NVM subsystem，包含 controller、port、namespace 與非揮發性儲存資源的 NVMe 系統邊界。</dd></div><div><dt>CMB</dt><dd>Controller Memory Buffer，controller 提供、可放置部分 queue 或資料結構的記憶體區域。</dd></div><div><dt>PMR</dt><dd>Persistent Memory Region，由 controller 暴露、具有持久性語意的記憶體區域。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASE3-CAPACITY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">44.</span>capacity model 分開追蹤 NVM subsystem、Endurance Group、NVM Set 與 namespace 的可用或配置容量；同一數值不可跨層級直接比較。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Endurance Group</dt><dd>Endurance Group，用於隔離與回報耐久度相關狀態的 NVM 資源群組。</dd></div><div><dt>NVM subsystem</dt><dd>NVM subsystem，包含 controller、port、namespace 與非揮發性儲存資源的 NVMe 系統邊界。</dd></div><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div><div><dt>NVM Set</dt><dd>NVM Set，把 namespace 與一組共同管理的 NVM 資源建立關聯的容量集合。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.8</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.8, 文件頁 125-129, PDF 頁 151-155</p></details>
<!-- claim:BASE3-MEDIA -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">45.</span>NVM Set、Endurance Group、Reclaim Group 與 Reclaim Unit 分別描述容量集合、耐久度管理與回收粒度。是否支援及其 identifier 由 Identify／log page 能力判定。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Endurance Group</dt><dd>Endurance Group，用於隔離與回報耐久度相關狀態的 NVM 資源群組。</dd></div><div><dt>Reclaim Group</dt><dd>Reclaim Group，具有共同回收行為的一組非揮發性儲存資源。</dd></div><div><dt>Reclaim Unit</dt><dd>Reclaim Unit，controller 執行媒體回收時使用的較小管理粒度。</dd></div><div><dt>NVM Set</dt><dd>NVM Set，把 namespace 與一組共同管理的 NVM 資源建立關聯的容量集合。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.2.2-3.2.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, 文件頁 80-85, PDF 頁 106-111</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>CMB</td><td>controller-provided working memory</td><td>是否能放 SQ/CQ/list/data 由能力 bit 決定</td></tr><tr><td>PMR</td><td>具有持久性語意的 region</td><td>enable、ready、error 與 address control 要一起看</td></tr><tr><td>capacity model</td><td>subsystem／group／set／namespace 的容量</td><td>不同層級欄位不可直接相減</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>CMB</dt><dd>Controller Memory Buffer，controller 提供、可放置部分 queue 或資料結構的記憶體區域。</dd></div><div><dt>PMR</dt><dd>Persistent Memory Region，由 controller 暴露、具有持久性語意的記憶體區域。</dd></div><div><dt>CQ</dt><dd>Completion Queue，controller 放入完成結果的完成佇列。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">46.</span>說明性範例：CMB size 足以容納一個 SQ，不代表 controller 的 namespace 多出同樣容量；前者是 queue/data structure 的放置資源，後者才是 host 可格式化與存取的非揮發性容量。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:BASE3-FIG-047 -->
<details class="field-note" id="figure-BASE3-FIG-047"><summary>Base Figure 47 · Offset 38h: CMBLOC - Controller Memory Buffer Location</summary>
<!-- claim:BASE3-FIG-047-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">47.</span>Figure 47〈Offset 38h: CMBLOC - Controller Memory Buffer Location〉：定義 offset 38h 的 CMBLOC（Controller Memory Buffer Location），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.9</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.9, Figure 47, 文件頁 67-68, PDF 頁 93-94</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>BAR</dt><dd>Base Address Register，PCI configuration space 中用來找出裝置 memory space 的 register。</dd></div><div><dt>BIR</dt><dd>BAR Indicator Register，指出某個記憶體結構位於哪一個 PCIe BAR。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-048 -->
<details class="field-note" id="figure-BASE3-FIG-048"><summary>Base Figure 48 · Offset 3Ch: CMBSZ - Controller Memory Buffer Size</summary>
<!-- claim:BASE3-FIG-048-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">48.</span>Figure 48〈Offset 3Ch: CMBSZ - Controller Memory Buffer Size〉：定義 offset 3Ch 的 CMBSZ（Controller Memory Buffer Size），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.11</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.11, Figure 48, 文件頁 68-69, PDF 頁 94-95</p></details>

</details>
<!-- figure-table:BASE3-FIG-052 -->
<details class="field-note" id="figure-BASE3-FIG-052"><summary>Base Figure 52 · Offset 50h: CMBMSC - Controller Memory Buffer Memory Space Control</summary>
<!-- claim:BASE3-FIG-052-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">49.</span>Figure 52〈Offset 50h: CMBMSC - Controller Memory Buffer Memory Space Control〉：定義 offset 50h 的 CMBMSC（Controller Memory Buffer Memory Space Control），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.14</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 52, 文件頁 70-71, PDF 頁 96-97</p></details>

</details>
<!-- figure-table:BASE3-FIG-053 -->
<details class="field-note" id="figure-BASE3-FIG-053"><summary>Base Figure 53 · Offset 58h: CMBSTS - Controller Memory Buffer Status</summary>
<!-- claim:BASE3-FIG-053-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">50.</span>Figure 53〈Offset 58h: CMBSTS - Controller Memory Buffer Status〉：定義 offset 58h 的 CMBSTS（Controller Memory Buffer Status），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.16</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.16, Figure 53, 文件頁 71, PDF 頁 97</p></details>

</details>
<!-- figure-table:BASE3-FIG-054 -->
<details class="field-note" id="figure-BASE3-FIG-054"><summary>Base Figure 54 · Offset 5Ch: CMBEBS - Controller Memory Buffer Elasticity Buffer Size</summary>
<!-- claim:BASE3-FIG-054-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">51.</span>Figure 54〈Offset 5Ch: CMBEBS - Controller Memory Buffer Elasticity Buffer Size〉：定義 offset 5Ch 的 CMBEBS（Controller Memory Buffer Elasticity Buffer Size），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.16</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.16, Figure 54, 文件頁 71, PDF 頁 97</p></details>

</details>
<!-- figure-table:BASE3-FIG-055 -->
<details class="field-note" id="figure-BASE3-FIG-055"><summary>Base Figure 55 · Offset 60h: CMBSWTP - Controller Memory Buffer Sustained Write Throughput</summary>
<!-- claim:BASE3-FIG-055-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">52.</span>Figure 55〈Offset 60h: CMBSWTP - Controller Memory Buffer Sustained Write Throughput〉：定義 offset 60h 的 CMBSWTP（Controller Memory Buffer Sustained Write Throughput），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.19</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.19, Figure 55, 文件頁 72, PDF 頁 98</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>TLP</dt><dd>Transaction Layer Packet，PCIe transaction layer 傳送的 packet。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-058 -->
<details class="field-note" id="figure-BASE3-FIG-058"><summary>Base Figure 58 · Offset E00h: PMRCAP - Persistent Memory Region Capabilities</summary>
<!-- claim:BASE3-FIG-058-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">53.</span>Figure 58〈Offset E00h: PMRCAP - Persistent Memory Region Capabilities〉：定義 offset E00h 的 PMRCAP（Persistent Memory Region Capabilities），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.21</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.21, Figure 58, 文件頁 73-74, PDF 頁 99-100</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>BIR</dt><dd>BAR Indicator Register，指出某個記憶體結構位於哪一個 PCIe BAR。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-059 -->
<details class="field-note" id="figure-BASE3-FIG-059"><summary>Base Figure 59 · Offset E04h: PMRCTL - Persistent Memory Region Control</summary>
<!-- claim:BASE3-FIG-059-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">54.</span>Figure 59〈Offset E04h: PMRCTL - Persistent Memory Region Control〉：定義 offset E04h 的 PMRCTL（Persistent Memory Region Control），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.22</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.22, Figure 59, 文件頁 74, PDF 頁 100</p></details>

</details>
<!-- figure-table:BASE3-FIG-060 -->
<details class="field-note" id="figure-BASE3-FIG-060"><summary>Base Figure 60 · Offset E08h: PMRSTS - Persistent Memory Region Status</summary>
<!-- claim:BASE3-FIG-060-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">55.</span>Figure 60〈Offset E08h: PMRSTS - Persistent Memory Region Status〉：定義 offset E08h 的 PMRSTS（Persistent Memory Region Status），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.23</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.23, Figure 60, 文件頁 75, PDF 頁 101</p></details>

</details>
<!-- figure-table:BASE3-FIG-061 -->
<details class="field-note" id="figure-BASE3-FIG-061"><summary>Base Figure 61 · Offset E0Ch: PMREBS - Persistent Memory Region Elasticity Buffer Size</summary>
<!-- claim:BASE3-FIG-061-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">56.</span>Figure 61〈Offset E0Ch: PMREBS - Persistent Memory Region Elasticity Buffer Size〉：定義 offset E0Ch 的 PMREBS（Persistent Memory Region Elasticity Buffer Size），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.24</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.24, Figure 61, 文件頁 76, PDF 頁 102</p></details>

</details>
<!-- figure-table:BASE3-FIG-062 -->
<details class="field-note" id="figure-BASE3-FIG-062"><summary>Base Figure 62 · Offset E10h: PMRSWTP - Persistent Memory Region Sustained Write Throughput</summary>
<!-- claim:BASE3-FIG-062-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">57.</span>Figure 62〈Offset E10h: PMRSWTP - Persistent Memory Region Sustained Write Throughput〉：定義 offset E10h 的 PMRSWTP（Persistent Memory Region Sustained Write Throughput），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.24</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.24, Figure 62, 文件頁 76, PDF 頁 102</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>TLP</dt><dd>Transaction Layer Packet，PCIe transaction layer 傳送的 packet。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-063 -->
<details class="field-note" id="figure-BASE3-FIG-063"><summary>Base Figure 63 · Offset E14h: PMRMSCL - Persistent Memory Region Memory Space Control Lower</summary>
<!-- claim:BASE3-FIG-063-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">58.</span>Figure 63〈Offset E14h: PMRMSCL - Persistent Memory Region Memory Space Control Lower〉：定義 offset E14h 的 PMRMSCL（Persistent Memory Region Memory Space Control Lower），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.26</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.26, Figure 63, 文件頁 77, PDF 頁 103</p></details>

</details>
<!-- figure-table:BASE3-FIG-064 -->
<details class="field-note" id="figure-BASE3-FIG-064"><summary>Base Figure 64 · Offset E18h: PMRMSCU - Persistent Memory Region Memory Space Control Upper</summary>
<!-- claim:BASE3-FIG-064-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">59.</span>Figure 64〈Offset E18h: PMRMSCU - Persistent Memory Region Memory Space Control Upper〉：定義 offset E18h 的 PMRMSCU（Persistent Memory Region Memory Space Control Upper），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.26</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.26, Figure 64, 文件頁 77, PDF 頁 103</p></details>

</details>
<!-- figure-table:BASE3-FIG-086 -->
<details class="field-note" id="figure-BASE3-FIG-086"><summary>Base Figure 86 · Simple NVM Subsystem</summary>
<!-- claim:BASE3-FIG-086-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">60.</span>Figure 86〈Simple NVM Subsystem〉：呈現〈Simple NVM Subsystem〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.8.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.8.2, Figure 86, 文件頁 126, PDF 頁 152</p></details>

</details>
<!-- figure-table:BASE3-FIG-087 -->
<details class="field-note" id="figure-BASE3-FIG-087"><summary>Base Figure 87 · Vertically-Organized NVM Subsystem</summary>
<!-- claim:BASE3-FIG-087-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">61.</span>Figure 87〈Vertically-Organized NVM Subsystem〉：呈現〈Vertically-Organized NVM Subsystem〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.8.2.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.8.2.2, Figure 87, 文件頁 127, PDF 頁 153</p></details>

</details>
<!-- figure-table:BASE3-FIG-088 -->
<details class="field-note" id="figure-BASE3-FIG-088"><summary>Base Figure 88 · Horizontally-Organized Dual NAND NVM Subsystem</summary>
<!-- claim:BASE3-FIG-088-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">62.</span>Figure 88〈Horizontally-Organized Dual NAND NVM Subsystem〉：呈現〈Horizontally-Organized Dual NAND NVM Subsystem〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.8.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.8.2.3, Figure 88, 文件頁 128, PDF 頁 154</p></details>

</details>
<!-- figure-table:BASE3-FIG-089 -->
<details class="field-note" id="figure-BASE3-FIG-089"><summary>Base Figure 89 · Capacity Information Field Usage</summary>
<!-- claim:BASE3-FIG-089-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">63.</span>Figure 89〈Capacity Information Field Usage〉：定義〈Capacity Information Field Usage〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.8.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.8.3, Figure 89, 文件頁 129, PDF 頁 155</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-lifecycle"><h2 id="heading-lifecycle"><span class="section-number">05</span> Shutdown、Reset 與狀態保留</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">64.</span>Lifecycle 事件的共同問題是『哪一層狀態仍有效』。Normal shutdown 由 CC.SHN/CSTS.SHST 協調，reset 分成 subsystem/controller/queue 層級，Keep Alive 監測 host-controller 存活，firmware activation 又可能要求特定 reset。相同的『暫時無法處理 command』症狀，不代表可以使用相同 recovery。</p><dl class="term-note" aria-label="本段名詞"><div><dt>SHN</dt><dd>Shutdown Notification，CC 中由 host 宣告 shutdown 類型的欄位。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASE3-SHUTDOWN -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">65.</span>正常 shutdown 由 host 設定 CC.SHN，controller 透過 CSTS.SHST 回報進度；NVM subsystem shutdown 是更大範圍的處理，不能與單一 controller shutdown 混為一談。</p><details class="source-note"><summary>來源：Base 2.4 §3.6.1, 3.6.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, 文件頁 113-120, PDF 頁 139-146</p></details>
<!-- claim:BASE3-RESET -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">66.</span>NVM Subsystem Reset、Controller Level Reset 與 Queue Level Reset 的影響範圍不同；設計 recovery flow 前先確認哪一層狀態會被清除、queue 是否仍存在。</p><details class="source-note"><summary>來源：Base 2.4 §3.7</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.7, 文件頁 120-125, PDF 頁 146-151</p></details>
<!-- claim:BASE3-KEEPALIVE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">67.</span>Keep Alive 以 KATO／KATT 建立 host 與 controller 的存活監測；本報告只保留 controller 共通與 PCIe 可用的 timer、command 與 timeout 行為。</p><dl class="term-note" aria-label="本段名詞"><div><dt>KATO</dt><dd>Keep Alive Timeout，host 與 controller 約定的存活逾時設定。</dd></div><div><dt>KATT</dt><dd>Keep Alive Timeout Total，controller 用於偵測逾時的總時間基準。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.9</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.9, 文件頁 129-135, PDF 頁 155-161</p></details>
<!-- claim:BASE3-FIRMWARE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">68.</span>privileged action 會影響其他 host 或 controller；firmware update 分成 image download、commit／activate 與可能的 reset，host 依回報的 activation action 安排流程。</p><details class="source-note"><summary>來源：Base 2.4 §3.10-3.11</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.10-3.11, 文件頁 135-138, PDF 頁 161-164</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>normal shutdown</td><td>保護性停止與狀態回報</td><td>看 SHN/SHST</td></tr><tr><td>controller reset</td><td>controller 層級狀態</td><td>queue 是否保留要依 reset 類型</td></tr><tr><td>NVM subsystem reset</td><td>更大 subsystem scope</td><td>可能影響多個 controllers</td></tr><tr><td>Keep Alive timeout</td><td>liveness failure</td><td>不能直接等同 media failure</td></tr></tbody></table></div>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">69.</span>說明性範例：host 要做 normal shutdown 時先停止提交新 I/O，設定 CC.SHN，再監看 CSTS.SHST。若等待期間發生 controller fatal status，後續 recovery 應按 reset scope 重建資源，而不是假設 normal shutdown 已完成。</p></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:BASE3-FIG-043 -->
<details class="field-note" id="figure-BASE3-FIG-043"><summary>Base Figure 43 · Offset 20h: NSSR - NVM Subsystem Reset</summary>
<!-- claim:BASE3-FIG-043-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">70.</span>Figure 43〈Offset 20h: NSSR - NVM Subsystem Reset〉：定義 offset 20h 的 NSSR（NVM Subsystem Reset），並指出軟體在該位置必須分別依欄位換算的欄位。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NSSR</dt><dd>NVM Subsystem Reset，觸發 NVM subsystem reset 的 property。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.4.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 43, 文件頁 66, PDF 頁 92</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>NSSR</dt><dd>NVM Subsystem Reset，觸發 NVM subsystem reset 的 property。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-056 -->
<details class="field-note" id="figure-BASE3-FIG-056"><summary>Base Figure 56 · Offset 64h: NSSD - NVM Subsystem Shutdown</summary>
<!-- claim:BASE3-FIG-056-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">71.</span>Figure 56〈Offset 64h: NSSD - NVM Subsystem Shutdown〉：定義 offset 64h 的 NSSD（NVM Subsystem Shutdown），並指出軟體在該位置必須分別依欄位換算的欄位。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NSSD</dt><dd>NVM Subsystem Shutdown，控制較大範圍 subsystem shutdown 的 property。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.1.4.19</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.19, Figure 56, 文件頁 72, PDF 頁 98</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CAP.CPS</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.CPS 進一步指定其中的 CPS 子欄位。</dd></div><div><dt>NSSD</dt><dd>NVM Subsystem Shutdown，控制較大範圍 subsystem shutdown 的 property。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-084 -->
<details class="field-note" id="figure-BASE3-FIG-084"><summary>Base Figure 84 · Admin Commands Permitted to Return a Status Code of Admin Command Media Not</summary>
<!-- claim:BASE3-FIG-084-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">72.</span>Figure 84〈Admin Commands Permitted to Return a Status Code of Admin Command Media Not〉：定義〈Admin Commands Permitted to Return a Status Code of Admin Command Media Not〉所表示的 status／error 分類。</p><details class="source-note"><summary>來源：Base 2.4 §3.5.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.5.3, Figure 84, 文件頁 110-111, PDF 頁 136-137</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>CAP.CRMS.CRIMS</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.CRMS.CRIMS 進一步指定其中的 CRMS.CRIMS 子欄位。</dd></div><div><dt>CAP.CRMS.CRWMS</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.CRMS.CRWMS 進一步指定其中的 CRMS.CRWMS 子欄位。</dd></div><div><dt>CAP.CRMS</dt><dd>Controller Capabilities，offset 00h 的 controller property，回報 queue、page size、timeout 與其他能力。 此處的 CAP.CRMS 進一步指定其中的 CRMS 子欄位。</dd></div><div><dt>CC.CRIME</dt><dd>Controller Configuration，host 用來選擇設定並啟用或停用 controller 的 property。 此處的 CC.CRIME 進一步指定其中的 CRIME 子欄位。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-085 -->
<details class="field-note" id="figure-BASE3-FIG-085"><summary>Base Figure 85 · Shutdown Processing Interactions</summary>
<!-- claim:BASE3-FIG-085-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">73.</span>Figure 85〈Shutdown Processing Interactions〉：呈現〈Shutdown Processing Interactions〉的狀態或時間推進關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.6</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.6, Figure 85, 文件頁 113, PDF 頁 139</p></details>

</details>
<!-- figure-table:BASE3-FIG-090 -->
<details class="field-note" id="figure-BASE3-FIG-090"><summary>Base Figure 90 · Detecting Timeout Takes up to 2 * KATT</summary>
<!-- claim:BASE3-FIG-090-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">74.</span>Figure 90〈Detecting Timeout Takes up to 2 * KATT〉：呈現〈Detecting Timeout Takes up to 2 * KATT〉的狀態或時間推進關係。</p><dl class="term-note" aria-label="本段名詞"><div><dt>KATT</dt><dd>Keep Alive Timeout Total，controller 用於偵測逾時的總時間基準。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.9.4.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.9.4.1, Figure 90, 文件頁 133, PDF 頁 159</p></details>

</details>
<!-- figure-table:BASE3-FIG-091 -->
<details class="field-note" id="figure-BASE3-FIG-091"><summary>Base Figure 91 · Example Privileged Action Admin Commands</summary>
<!-- claim:BASE3-FIG-091-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">75.</span>Figure 91〈Example Privileged Action Admin Commands〉：界定〈Example Privileged Action Admin Commands〉所示的 privileged operation 邊界。</p><details class="source-note"><summary>來源：Base 2.4 §3.10</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.10, Figure 91, 文件頁 135, PDF 頁 161</p></details>

</details>
</details>
</section>
<section id="additional-details"><h2 id="further-mechanisms">補充機制與資料格式</h2>
<!-- claim:BASE3-NAMESPACE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">76.</span>NSID 0h 無效，FFFFFFFFh 是 broadcast 值；其餘 NSID 還要區分 allocated／unallocated 與 active／inactive，不能只看數字是否落在範圍內。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.1, 文件頁 78-80, PDF 頁 104-106</p></details>
<!-- claim:BASE3-DOMAIN -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">77.</span>domain 是 NVM subsystem 內的故障／通訊邊界。多 domain subsystem 的 identifier 必須（shall）在該 subsystem 內唯一。</p><details class="source-note"><summary>來源：Base 2.4 §3.2.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.5, 文件頁 85-88, PDF 頁 111-114</p></details>
<!-- figure-table:BASE3-FIG-039 -->
<details class="field-note" id="figure-BASE3-FIG-039"><summary>Base Figure 39 · Offset Ch: INTMS - Interrupt Mask Set</summary>
<!-- claim:BASE3-FIG-039-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">78.</span>Figure 39〈Offset Ch: INTMS - Interrupt Mask Set〉：定義 offset Ch 的 INTMS（Interrupt Mask Set），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.2, Figure 39, 文件頁 59, PDF 頁 85</p></details>
<dl class="term-note" aria-label="本段名詞"><div><dt>MSI</dt><dd>Message Signaled Interrupt，透過 memory write message 傳遞 interrupt 的 PCI 機制。</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-040 -->
<details class="field-note" id="figure-BASE3-FIG-040"><summary>Base Figure 40 · Offset 10h: INTMC - Interrupt Mask Clear</summary>
<!-- claim:BASE3-FIG-040-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">79.</span>Figure 40〈Offset 10h: INTMC - Interrupt Mask Clear〉：定義 offset 10h 的 INTMC（Interrupt Mask Clear），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.2, Figure 40, 文件頁 59, PDF 頁 85</p></details>

</details>
<!-- figure-table:BASE3-FIG-049 -->
<details class="field-note" id="figure-BASE3-FIG-049"><summary>Base Figure 49 · Offset 40h: BPINFO - Boot Partition Information</summary>
<!-- claim:BASE3-FIG-049-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">80.</span>Figure 49〈Offset 40h: BPINFO - Boot Partition Information〉：定義 offset 40h 的 BPINFO（Boot Partition Information），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.12, Figure 49, 文件頁 69, PDF 頁 95</p></details>

</details>
<!-- figure-table:BASE3-FIG-050 -->
<details class="field-note" id="figure-BASE3-FIG-050"><summary>Base Figure 50 · Offset 44h: BPRSEL - Boot Partition Read Select</summary>
<!-- claim:BASE3-FIG-050-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">81.</span>Figure 50〈Offset 44h: BPRSEL - Boot Partition Read Select〉：定義 offset 44h 的 BPRSEL（Boot Partition Read Select），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.12</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.12, Figure 50, 文件頁 69-70, PDF 頁 95-96</p></details>

</details>
<!-- figure-table:BASE3-FIG-051 -->
<details class="field-note" id="figure-BASE3-FIG-051"><summary>Base Figure 51 · Offset 48h: BPMBL - Boot Partition Memory Buffer Location</summary>
<!-- claim:BASE3-FIG-051-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">82.</span>Figure 51〈Offset 48h: BPMBL - Boot Partition Memory Buffer Location〉：定義 offset 48h 的 BPMBL（Boot Partition Memory Buffer Location），並指出軟體在該位置必須分別依欄位換算的欄位。</p><details class="source-note"><summary>來源：Base 2.4 §3.1.4.14</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 51, 文件頁 70, PDF 頁 96</p></details>

</details>
<!-- figure-table:BASE3-FIG-065 -->
<details class="field-note" id="figure-BASE3-FIG-065"><summary>Base Figure 65 · NSID Types and Relationship to Namespace</summary>
<!-- claim:BASE3-FIG-065-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">83.</span>Figure 65〈NSID Types and Relationship to Namespace〉：定義〈NSID Types and Relationship to Namespace〉的識別碼組成或數值空間。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §3.2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.1, Figure 65, 文件頁 78-79, PDF 頁 104-105</p></details>

</details>
<!-- figure-table:BASE3-FIG-066 -->
<details class="field-note" id="figure-BASE3-FIG-066"><summary>Base Figure 66 · NSID Types</summary>
<!-- claim:BASE3-FIG-066-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">84.</span>Figure 66〈NSID Types〉：定義〈NSID Types〉的識別碼組成或數值空間。</p><details class="source-note"><summary>來源：Base 2.4 §3.2.1.5</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.1.5, Figure 66, 文件頁 79, PDF 頁 105</p></details>

</details>
<!-- figure-table:BASE3-FIG-067 -->
<details class="field-note" id="figure-BASE3-FIG-067"><summary>Base Figure 67 · NVM Sets and Associated Namespaces</summary>
<!-- claim:BASE3-FIG-067-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">85.</span>Figure 67〈NVM Sets and Associated Namespaces〉：呈現〈NVM Sets and Associated Namespaces〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.2.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2, Figure 67, 文件頁 81, PDF 頁 107</p></details>

</details>
<!-- figure-table:BASE3-FIG-068 -->
<details class="field-note" id="figure-BASE3-FIG-068"><summary>Base Figure 68 · NVM Set Aware Admin Commands</summary>
<!-- claim:BASE3-FIG-068-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">86.</span>Figure 68〈NVM Set Aware Admin Commands〉：呈現〈NVM Set Aware Admin Commands〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.2.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2, Figure 68, 文件頁 81, PDF 頁 107</p></details>

</details>
<!-- figure-table:BASE3-FIG-069 -->
<details class="field-note" id="figure-BASE3-FIG-069"><summary>Base Figure 69 · NVM Sets and Associated Namespaces</summary>
<!-- claim:BASE3-FIG-069-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">87.</span>Figure 69〈NVM Sets and Associated Namespaces〉：呈現〈NVM Sets and Associated Namespaces〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.2.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.3, Figure 69, 文件頁 83, PDF 頁 109</p></details>

</details>
<!-- figure-table:BASE3-FIG-070 -->
<details class="field-note" id="figure-BASE3-FIG-070"><summary>Base Figure 70 · Flexible Data Placement Logical View of Non-Volatile Storage</summary>
<!-- claim:BASE3-FIG-070-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">88.</span>Figure 70〈Flexible Data Placement Logical View of Non-Volatile Storage〉：呈現〈Flexible Data Placement Logical View of Non-Volatile Storage〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.2.4</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.4, Figure 70, 文件頁 85, PDF 頁 111</p></details>

</details>
<!-- figure-table:BASE3-FIG-071 -->
<details class="field-note" id="figure-BASE3-FIG-071"><summary>Base Figure 71 · Example 1 Domain Structure</summary>
<!-- claim:BASE3-FIG-071-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">89.</span>Figure 71〈Example 1 Domain Structure〉：定義〈Example 1 Domain Structure〉的實際配置或數值關係。</p><details class="source-note"><summary>來源：Base 2.4 §3.2.5.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.5.1, Figure 71, 文件頁 86, PDF 頁 112</p></details>

</details>
</section>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:base-ch3-ready -->
<details class="review-question" id="qa-base-ch3-ready"><summary>1. 讀到 controller 支援某功能，是否表示它已準備接收 I/O？</summary>
<div data-qa-answer="base-ch3-ready"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">90.</span>Capability 描述能做什麼；初始化與 ready state 描述目前能否開始操作。仍須完成 queue 設定、啟用與 readiness 確認，再依適用條件使用該功能。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §3.1.4, 文件頁 52-54, PDF 頁 78-80</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, 文件頁 105-113, PDF 頁 131-139</p>
</details></details>
<!-- qa:base-ch3-queue-order -->
<details class="review-question" id="qa-base-ch3-queue-order"><summary>2. SQ 中先提交的命令，是否必定先完成？</summary>
<div data-qa-answer="base-ch3-queue-order"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">91.</span>Queue 提交順序、controller 選取工作及完成順序是不同概念。一般不能只靠 SQ 位置推論完成順序；有相依性時應使用規格定義的同步或命令機制。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §3.3.1, 文件頁 88-91, PDF 頁 114-117</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, 文件頁 101-105, PDF 頁 127-131</p>
</details></details>
<!-- qa:base-ch3-shutdown-reset -->
<details class="review-question" id="qa-base-ch3-shutdown-reset"><summary>3. 為何正常關機流程不能直接等同 reset？</summary>
<div data-qa-answer="base-ch3-shutdown-reset"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">92.</span>Shutdown 包含 host 的通知及 controller 的完成狀態，讓關機前的處理有明確交接；reset 依其層級改變 controller 或 subsystem 狀態。它們的觸發、範圍和保留狀態不同。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, 文件頁 113-120, PDF 頁 139-146</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §3.7, 文件頁 120-125, PDF 頁 146-151</p>
</details></details>
<!-- qa:base-ch3-memory-regions -->
<details class="review-question" id="qa-base-ch3-memory-regions"><summary>4. Controller 可見的記憶體區域，為何不能全都當成 namespace 容量？</summary>
<div data-qa-answer="base-ch3-memory-regions"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">93.</span>Namespace 提供以 logical blocks 存取的儲存空間；CMB、PMR 等區域有各自用途、存取方式及持久性規則。位於同一裝置不代表它們使用相同的容量與資料模型。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, 文件頁 80-85, PDF 頁 106-111</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §3.8, 文件頁 125-129, PDF 頁 151-155</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
