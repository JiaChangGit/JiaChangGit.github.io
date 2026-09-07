---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4 第 1、2 章：規格語言、PCIe 佇列與儲存模型"
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
[English]({% post_url 2026-08-28-nvme-base-ch1-2-en %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-hidden="true">01.</span>NVMe 是主機與儲存控制器之間的介面。本篇先建立整體關係：主機如何送出命令、控制器如何回報結果，以及 namespace、controller、NVM subsystem 各代表什麼。這些概念是閱讀後續命令與欄位的起點。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NVM subsystem</dt><dd>NVM subsystem，包含 controller、port、namespace 與非揮發性儲存資源的 NVMe 系統邊界。</dd></div><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div><div><dt>NVMe</dt><dd>Non-Volatile Memory Express，主機與非揮發性記憶體子系統之間的介面規範家族。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl>
<h2 id="main-ideas">這篇的主軸</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>規格如何分工</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-hidden="true">02.</span>分辨 Base、Transport 與 I/O Command Set 各自定義的內容。</p><dl class="term-note" aria-label="本段名詞"><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl></article>
<article><span class="axis-number">02</span><h3>命令如何往返</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-hidden="true">03.</span>以提交佇列與完成佇列理解主機和控制器的合作。</p></article>
<article><span class="axis-number">03</span><h3>儲存物件與路徑</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-hidden="true">04.</span>分清 namespace、controller 與 subsystem，並理解多條存取路徑。</p><dl class="term-note" aria-label="本段名詞"><div><dt>controller</dt><dd>controller，實作 NVMe 介面、取走 command 並回報 completion 的控制實體。</dd></div><div><dt>namespace</dt><dd>namespace，主機透過 controller 存取的一份已格式化非揮發性容量。</dd></div></dl></article>
</div>
<dl class="term-note" aria-label="本段名詞"><div><dt>I/O</dt><dd>Input/Output，對 namespace 執行資料輸入與輸出的操作類別。</dd></div></dl>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">05.</span>這裡的主機包含作業系統與驅動程式；控制器提供主機可存取的 NVMe 介面。NVMe 描述主機可見的行為，不能直接等同 SSD 內部 NAND 的實體配置。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express，主機與非揮發性記憶體子系統之間的介面規範家族。</dd></div></dl>
</section>
<section class="lesson" id="module-family"><h2 id="heading-family"><span class="section-number">01</span> Base、Command Set 與 Transport 的分工</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">06.</span>遇到一個 command、register 或資料格式時，第一個問題不是『它在哪一頁』，而是『哪一份規格擁有這個定義』。Base 提供通用協定，Transport 補上 PCIe 綁定，I/O Command Set 再定義 namespace 資料操作。Figure 1 的框線代表適用關係，不代表封包一定逐層穿過這些方塊。</p><dl class="term-note" aria-label="本段名詞"><div><dt>PCIe</dt><dd>PCI Express，NVMe memory-based controller 使用的 transport 與裝置互連。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASE12-FAMILY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">07.</span>Base Specification 定義通用 NVMe 協定；Transport Specification 綁定特定傳輸，I/O Command Set Specification 擴充命令與資料結構。這是適用關係，不是協定堆疊。</p><details class="source-note"><summary>來源：Base 2.4 §1.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §1.1.1, 文件頁 1, PDF 頁 27</p></details>
<!-- claim:BASE12-COMMANDSET -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">08.</span>Admin Command Set 管理 controller 與 queue；I/O Command Set 定義對 namespace 的資料操作。Base 說明通用機制，個別 I/O Command Set Specification 說明命令語意。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §2.3.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.3.2, 文件頁 33, PDF 頁 59</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>Base</td><td>共通 command、queue、status 與資料結構</td><td>不要假設它定義所有 PCIe register 細節</td></tr><tr><td>PCIe Transport</td><td>BAR、MMIO、doorbell、interrupt 與 PCIe-specific 行為</td><td>衝突時不能覆蓋 Base</td></tr><tr><td>I/O Command Set</td><td>特定 namespace I/O command 與延伸資料結構</td><td>不負責重新定義 transport</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>MMIO</dt><dd>Memory-Mapped I/O，以 CPU memory access 形式讀寫裝置 register。</dd></div><div><dt>PCIe</dt><dd>PCI Express，NVMe memory-based controller 使用的 transport 與裝置互連。</dd></div><div><dt>BAR</dt><dd>Base Address Register，PCI configuration space 中用來找出裝置 memory space 的 register。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">09.</span>要實作 Firmware Image Download：先在 Base 找 command 欄位與 completion status，再到 PCIe Transport 確認 Admin command 的資料指標與 memory access 限制。若未閱讀 I/O Command Set，仍可理解此 Admin command；反過來只讀 PCIe Transport 則得不到完整 command 語意。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Admin</dt><dd>Administrative，建立、設定、查詢或管理 controller 與 queue 的控制路徑。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:BASE12-FIG-001 -->
<details class="field-note" id="figure-BASE12-FIG-001"><summary>Base Figure 1 · NVMe Family of Specifications</summary>
<!-- claim:BASE12-FIG-001-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">10.</span>Figure 1〈NVMe Family of Specifications〉：定位〈NVMe Family of Specifications〉在 NVMe 文件與 command set 階層中的位置。</p><details class="source-note"><summary>來源：Base 2.4 §1.1.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §1.1.1, Figure 1, 文件頁 1, PDF 頁 27</p></details>

</details>
<!-- figure-table:BASE12-FIG-005 -->
<details class="field-note" id="figure-BASE12-FIG-005"><summary>Base Figure 5 · Types of NVMe Command Sets</summary>
<!-- claim:BASE12-FIG-005-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">11.</span>Figure 5〈Types of NVMe Command Sets〉：定位〈Types of NVMe Command Sets〉在 NVMe 文件與 command set 階層中的位置。</p><details class="source-note"><summary>來源：Base 2.4 §2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2, Figure 5, 文件頁 21, PDF 頁 47</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-objects"><h2 id="heading-objects"><span class="section-number">02</span> Namespace、Controller 與存取路徑</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">12.</span>namespace 是 host 實際存取的格式化容量，但容量管理、耐久度、回收與路徑都發生在不同層級。Figures 11-18 用 NVM Set 或 Reclaim Group 描述容量包含關係，Figures 19-22 則改看 controller、port、path 與 PCIe Function。兩組圖回答不同問題，不能疊成單一樹狀圖後便認為每層都一對一。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Reclaim Group</dt><dd>Reclaim Group，具有共同回收行為的一組非揮發性儲存資源。</dd></div><div><dt>NVM Set</dt><dd>NVM Set，把 namespace 與一組共同管理的 NVM 資源建立關聯的容量集合。</dd></div><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory，斷電後仍能保存資料的記憶體。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASE12-STORAGE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">13.</span>儲存模型用 NVM subsystem、domain、Endurance Group、NVM Set／Reclaim Group、Reclaim Unit 與 namespace 表達包含關係。namespace 是 host 實際透過 controller 存取的格式化容量。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Endurance Group</dt><dd>Endurance Group，用於隔離與回報耐久度相關狀態的 NVM 資源群組。</dd></div><div><dt>NVM subsystem</dt><dd>NVM subsystem，包含 controller、port、namespace 與非揮發性儲存資源的 NVMe 系統邊界。</dd></div><div><dt>Reclaim Group</dt><dd>Reclaim Group，具有共同回收行為的一組非揮發性儲存資源。</dd></div><div><dt>Reclaim Unit</dt><dd>Reclaim Unit，controller 執行媒體回收時使用的較小管理粒度。</dd></div><div><dt>NVM Set</dt><dd>NVM Set，把 namespace 與一組共同管理的 NVM 資源建立關聯的容量集合。</dd></div><div><dt>Host</dt><dd>主機；執行作業系統並送出 NVMe 命令的一端。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §2.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, 文件頁 26-33, PDF 頁 52-59</p></details>
<!-- claim:BASE12-SUBSYSTEM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">14.</span>controller、port、namespace 與 PCI Function 是不同物件；NSID 是 controller 用來指向 namespace 的 handle，不是 namespace 本身。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §2.3.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.3.3, 文件頁 33-35, PDF 頁 59-61</p></details>
<!-- claim:BASE12-MULTIPATH -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">15.</span>multi-path I/O 是同一 host 到同一 namespace 的兩條以上獨立路徑；namespace sharing 是兩個以上 host 經不同 controller 存取同一 shared namespace。兩者都需要至少兩個 controller。</p><details class="source-note"><summary>來源：Base 2.4 §2.4.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, 文件頁 35-37, PDF 頁 61-63</p></details>
<!-- claim:BASE12-ASYMMETRY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">16.</span>支援多路徑或共享時，各 controller 對同一 namespace 的存取特性不一定相同；host 可依 controller 所回報的狀態選擇路徑。</p><details class="source-note"><summary>來源：Base 2.4 §2.4.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.4.2, 文件頁 37, PDF 頁 63</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>multi-path I/O</td><td>同一 host、同一 namespace、兩條以上獨立路徑</td><td>重點是 path redundancy</td></tr><tr><td>namespace sharing</td><td>兩個以上 hosts 存取同一 shared namespace</td><td>重點是 host ownership 與 coordination</td></tr><tr><td>SR-IOV</td><td>一個 PCIe 裝置呈現 PF/VF</td><td>PCIe Function 不必等同獨立 subsystem</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>SR-IOV</dt><dd>Single Root I/O Virtualization，讓一個 PCIe 裝置呈現一個 PF 與多個 VF 的虛擬化能力。</dd></div><div><dt>PF</dt><dd>Physical Function，具有完整 PCIe 設定能力、可管理相關 VF 的實體功能。</dd></div><div><dt>VF</dt><dd>Virtual Function，由 SR-IOV 建立、資源較受限的 PCIe 虛擬功能。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">17.</span>說明性範例：host A 經 controller 1 與 controller 2 都能存取 namespace X，這是 multi-path。host B 也經 controller 2 存取同一 namespace X，才同時構成 namespace sharing。NSID 在兩個 controller 上可能不同，因此跨 controller 比對時應先確認 namespace identity，而不是直接比較 NSID 數值。</p><dl class="term-note" aria-label="本段名詞"><div><dt>NSID</dt><dd>Namespace Identifier，controller 用來指向 namespace 的數值 handle；identifier 不等於 namespace 物件本身。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:BASE12-FIG-011 -->
<details class="field-note" id="figure-BASE12-FIG-011"><summary>Base Figure 11 · Simple NVM Storage Hierarchy with NVM Sets</summary>
<!-- claim:BASE12-FIG-011-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">18.</span>Figure 11〈Simple NVM Storage Hierarchy with NVM Sets〉：呈現〈Simple NVM Storage Hierarchy with NVM Sets〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §2.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 11, 文件頁 27, PDF 頁 53</p></details>

</details>
<!-- figure-table:BASE12-FIG-012 -->
<details class="field-note" id="figure-BASE12-FIG-012"><summary>Base Figure 12 · Simple NVM Storage Hierarchy with One Reclaim Group</summary>
<!-- claim:BASE12-FIG-012-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">19.</span>Figure 12〈Simple NVM Storage Hierarchy with One Reclaim Group〉：呈現〈Simple NVM Storage Hierarchy with One Reclaim Group〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §2.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 12, 文件頁 28, PDF 頁 54</p></details>

</details>
<!-- figure-table:BASE12-FIG-013 -->
<details class="field-note" id="figure-BASE12-FIG-013"><summary>Base Figure 13 · Simple NVM Storage Hierarchy with Multiple Reclaim Groups</summary>
<!-- claim:BASE12-FIG-013-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">20.</span>Figure 13〈Simple NVM Storage Hierarchy with Multiple Reclaim Groups〉：呈現〈Simple NVM Storage Hierarchy with Multiple Reclaim Groups〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §2.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 13, 文件頁 29, PDF 頁 55</p></details>

</details>
<!-- figure-table:BASE12-FIG-014 -->
<details class="field-note" id="figure-BASE12-FIG-014"><summary>Base Figure 14 · Complex NVM Storage Hierarchy with NVM Sets</summary>
<!-- claim:BASE12-FIG-014-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">21.</span>Figure 14〈Complex NVM Storage Hierarchy with NVM Sets〉：呈現〈Complex NVM Storage Hierarchy with NVM Sets〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §2.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 14, 文件頁 30, PDF 頁 56</p></details>

</details>
<!-- figure-table:BASE12-FIG-015 -->
<details class="field-note" id="figure-BASE12-FIG-015"><summary>Base Figure 15 · Complex NVM Storage Hierarchy with Multiple Reclaim Groups</summary>
<!-- claim:BASE12-FIG-015-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">22.</span>Figure 15〈Complex NVM Storage Hierarchy with Multiple Reclaim Groups〉：呈現〈Complex NVM Storage Hierarchy with Multiple Reclaim Groups〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §2.3.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 15, 文件頁 31, PDF 頁 57</p></details>

</details>
<!-- figure-table:BASE12-FIG-016 -->
<details class="field-note" id="figure-BASE12-FIG-016"><summary>Base Figure 16 · Single-Namespace NVM Subsystem</summary>
<!-- claim:BASE12-FIG-016-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">23.</span>Figure 16〈Single-Namespace NVM Subsystem〉：呈現〈Single-Namespace NVM Subsystem〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §2.3.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 16, 文件頁 32, PDF 頁 58</p></details>

</details>
<!-- figure-table:BASE12-FIG-017 -->
<details class="field-note" id="figure-BASE12-FIG-017"><summary>Base Figure 17 · Two-Namespace NVM Subsystem</summary>
<!-- claim:BASE12-FIG-017-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">24.</span>Figure 17〈Two-Namespace NVM Subsystem〉：呈現〈Two-Namespace NVM Subsystem〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §2.3.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 17, 文件頁 33, PDF 頁 59</p></details>

</details>
<!-- figure-table:BASE12-FIG-018 -->
<details class="field-note" id="figure-BASE12-FIG-018"><summary>Base Figure 18 · Complex NVM Subsystem</summary>
<!-- claim:BASE12-FIG-018-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">25.</span>Figure 18〈Complex NVM Subsystem〉：呈現〈Complex NVM Subsystem〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §2.3.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 18, 文件頁 34, PDF 頁 60</p></details>

</details>
<!-- figure-table:BASE12-FIG-019 -->
<details class="field-note" id="figure-BASE12-FIG-019"><summary>Base Figure 19 · NVM Express Controller with Two Namespaces</summary>
<!-- claim:BASE12-FIG-019-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">26.</span>Figure 19〈NVM Express Controller with Two Namespaces〉：呈現〈NVM Express Controller with Two Namespaces〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §2.4.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 19, 文件頁 35, PDF 頁 61</p></details>

</details>
<!-- figure-table:BASE12-FIG-020 -->
<details class="field-note" id="figure-BASE12-FIG-020"><summary>Base Figure 20 · NVM Subsystem with Two Controllers and One Port</summary>
<!-- claim:BASE12-FIG-020-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">27.</span>Figure 20〈NVM Subsystem with Two Controllers and One Port〉：呈現〈NVM Subsystem with Two Controllers and One Port〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §2.4.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 20, 文件頁 35, PDF 頁 61</p></details>

</details>
<!-- figure-table:BASE12-FIG-021 -->
<details class="field-note" id="figure-BASE12-FIG-021"><summary>Base Figure 21 · NVM Subsystem with Two Controllers and Two Ports</summary>
<!-- claim:BASE12-FIG-021-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">28.</span>Figure 21〈NVM Subsystem with Two Controllers and Two Ports〉：呈現〈NVM Subsystem with Two Controllers and Two Ports〉中的物件或容量關係。</p><details class="source-note"><summary>來源：Base 2.4 §2.4.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 21, 文件頁 36, PDF 頁 62</p></details>

</details>
<!-- figure-table:BASE12-FIG-022 -->
<details class="field-note" id="figure-BASE12-FIG-022"><summary>Base Figure 22 · PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)</summary>
<!-- claim:BASE12-FIG-022-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">29.</span>Figure 22〈PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)〉：呈現〈PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)〉中 Physical Function 與 Virtual Function 的關係。</p><dl class="term-note" aria-label="本段名詞"><div><dt>SR-IOV</dt><dd>Single Root I/O Virtualization，讓一個 PCIe 裝置呈現一個 PF 與多個 VF 的虛擬化能力。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §2.4.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 22, 文件頁 37, PDF 頁 63</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-queues"><h2 id="heading-queues"><span class="section-number">03</span> 命令提交與完成的往返</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">30.</span>host 不把 command 直接寫進 controller。host 先在記憶體中的 SQE 建好命令，再公布新的 SQ tail；controller 取走命令後執行，最後把 CQE 放進 CQ。Figure 6 的 1:1 與 Figure 7 的 n:1 差異在於多個 SQ 是否共用同一個 CQ，不是 command 是否共用同一個 SQE。</p><dl class="term-note" aria-label="本段名詞"><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div><div><dt>SQE</dt><dd>Submission Queue Entry，SQ 中的一筆命令資料結構。</dd></div><div><dt>CQ</dt><dd>Completion Queue，controller 放入完成結果的完成佇列。</dd></div><div><dt>SQ</dt><dd>Submission Queue，主機放入命令的提交佇列。</dd></div></dl>
<figure><figcaption><strong>一筆命令如何往返</strong></figcaption><ol class="flow-steps"><li>Host 將命令寫入 SQ（提交佇列）。</li><li>Host 更新 SQ Tail Doorbell，通知 Controller 有新命令。</li><li>Controller 取出並執行命令，將結果寫入 CQ（完成佇列）。</li><li>Host 讀取 CQE，再更新 CQ Head Doorbell，交還已讀取的位置。</li></ol><figcaption>命令與結果放在佇列；Doorbell 傳達佇列位置的更新。</figcaption></figure>
<dl class="term-note" aria-label="本段名詞"><div><dt>CQE</dt><dd>Completion Queue Entry，CQ 中的一筆完成結果資料結構。</dd></div><div><dt>CQ</dt><dd>Completion Queue，controller 放入完成結果的完成佇列。</dd></div><div><dt>SQ</dt><dd>Submission Queue，主機放入命令的提交佇列。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASE12-QUEUE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">31.</span>PCIe memory-based model 把 Submission Queue 與 Completion Queue 配置在記憶體。多個 I/O Submission Queues 可共用一個 I/O Completion Queue；Admin queue pair 維持一對一。</p><details class="source-note"><summary>來源：Base 2.4 §2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.1, 文件頁 21-23, PDF 頁 47-49</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>Admin queue pair</td><td>一個 Admin SQ 對一個 Admin CQ</td><td>初始化與管理路徑</td></tr><tr><td>I/O 1:1</td><td>一個 I/O SQ 對一個 I/O CQ</td><td>追蹤簡單、隔離清楚</td></tr><tr><td>I/O n:1</td><td>多個 I/O SQ 共用一個 I/O CQ</td><td>完成路徑整併，仍以 SQID/CID 找回命令</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>SQID</dt><dd>Submission Queue Identifier，辨識 command 所屬 SQ 的數值。</dd></div><div><dt>CID</dt><dd>Command Identifier，與 SQ identifier 合用以辨識 outstanding command。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">32.</span>說明性範例：SQ 3 與 SQ 4 共用 CQ 2。兩筆 command 都使用 CID 5 仍可區分，因唯一鍵是 (SQID, CID)：(3,5) 與 (4,5)。只用 CID 建 outstanding-command map，會把其中一筆 completion 配錯。</p><dl class="term-note" aria-label="本段名詞"><div><dt>SQID</dt><dd>Submission Queue Identifier，辨識 command 所屬 SQ 的數值。</dd></div><div><dt>CID</dt><dd>Command Identifier，與 SQ identifier 合用以辨識 outstanding command。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:BASE12-FIG-006 -->
<details class="field-note" id="figure-BASE12-FIG-006"><summary>Base Figure 6 · Queue Pair Example, 1:1 Mapping</summary>
<!-- claim:BASE12-FIG-006-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">33.</span>Figure 6〈Queue Pair Example, 1:1 Mapping〉：呈現〈Queue Pair Example, 1:1 Mapping〉中的 queue 或 command 關係。</p><details class="source-note"><summary>來源：Base 2.4 §2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.1, Figure 6, 文件頁 22, PDF 頁 48</p></details>

</details>
<!-- figure-table:BASE12-FIG-007 -->
<details class="field-note" id="figure-BASE12-FIG-007"><summary>Base Figure 7 · Queue Pair Example, n:1 Mapping</summary>
<!-- claim:BASE12-FIG-007-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">34.</span>Figure 7〈Queue Pair Example, n:1 Mapping〉：呈現〈Queue Pair Example, n:1 Mapping〉中的 queue 或 command 關係。</p><details class="source-note"><summary>來源：Base 2.4 §2.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §2.1, Figure 7, 文件頁 22, PDF 頁 48</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-numbers"><h2 id="heading-numbers"><span class="section-number">04</span> 數值編碼與單位</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">35.</span>讀任何 raw value 前先確認單位與編碼。zero-based count=3 可能代表 4 個單位；index 選清單項目，offset 則表示離起點的距離，兩者不能互換。</p><dl class="term-note" aria-label="本段名詞"><div><dt>zero-based</dt><dd>zero-based；數值從 0 開始計算，因此 raw=3 代表第 4 個項目或 4 個單位，實際含義仍要看欄位定義。</dd></div><div><dt>raw value</dt><dd>raw value；欄位直接讀出的數值，尚未套用 zero-based、單位或縮放規則；先確認定義再換算。</dd></div><div><dt>offset</dt><dd>offset；從指定起點算出的位移。它回答「離起點多遠」，不等於 index。</dd></div><div><dt>index</dt><dd>index；用來選取清單中的項目或格式。它回答「選哪一項」，不是「離起點多遠」。</dd></div></dl>
<details class="technical-note"><summary>機制與適用條件</summary>
<!-- claim:BASE12-NUMBERS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">36.</span>數值的解讀同時包含進位與單位；十六進位使用 h 後綴，二進位使用 b 後綴，十進位可省略 d。十進位與二進位容量前綴代表不同倍率。</p><details class="source-note"><summary>來源：Base 2.4 §1.4.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §1.4.2, 文件頁 3-5, PDF 頁 29-31</p></details>
<!-- claim:BASE12-DWORD -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">37.</span>NVMe 以 byte、word、dword 表示欄位位置；一個 word 為 2 bytes，一個 dword 為 4 bytes。解欄位時先確認 byte 與 bit 編號。</p><dl class="term-note" aria-label="本段名詞"><div><dt>Dword</dt><dd>Dword（Double word）；32 bits，也就是 4 bytes。對比 word=16 bits；例如 zero-based dword count=3 代表 4 個 Dwords，也就是 16 bytes。</dd></div><div><dt>word</dt><dd>word；16 bits，也就是 2 bytes。它比 Dword 小一半；欄位長度不能只看數字，還要看單位。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §1.4.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §1.4.3, 文件頁 5, PDF 頁 31</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">項目</th><th scope="col">作用或差異</th><th scope="col">適用條件</th></tr></thead><tbody><tr><td>1000</td><td>十進位 1000</td><td>若無 b/h 後綴則按十進位</td></tr><tr><td>1000b</td><td>二進位 8</td><td>b 是 radix，不是 bit 單位</td></tr><tr><td>1000h</td><td>十六進位 4096</td><td>常見於 offset 與 register value</td></tr><tr><td>NUMD=0</td><td>實際 1 dword</td><td>只有欄位明載 0's-based 才加 1</td></tr></tbody></table></div><dl class="term-note" aria-label="本段名詞"><div><dt>0's-based</dt><dd>0's-based encoding，以 0 表示實際數量 1；依欄位換算公式通常是欄位值加 1。</dd></div><div><dt>offset</dt><dd>offset；從指定起點算出的位移。它回答「離起點多遠」，不等於 index。</dd></div><div><dt>Dword</dt><dd>Dword（Double word）；32 bits，也就是 4 bytes。對比 word=16 bits；例如 zero-based dword count=3 代表 4 個 Dwords，也就是 16 bytes。</dd></div><div><dt>NUMD</dt><dd>Number of Dwords，0's-based transfer dword count；實際 bytes = (NUMD + 1) × 4。</dd></div></dl>
<aside class="worked-example"><h3>例子</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">38.</span>說明性範例：一個 512-byte transfer 含 512 ÷ 4 = 128 dwords。若 NUMD 是 0's-based，編碼值為 128 - 1 = 127 = 007Fh。若錯把 007Fh 當成 byte count，buffer 會短少；若忘記減 1，controller 會被要求傳輸 129 dwords。</p><dl class="term-note" aria-label="本段名詞"><div><dt>0's-based</dt><dd>0's-based encoding，以 0 表示實際數量 1；依欄位換算公式通常是欄位值加 1。</dd></div><div><dt>NUMD</dt><dd>Number of Dwords，0's-based transfer dword count；實際 bytes = (NUMD + 1) × 4。</dd></div></dl></aside>
<details class="technical-note"><summary>進一步理解欄位與資料結構</summary>
<!-- figure-table:BASE12-FIG-002 -->
<details class="field-note" id="figure-BASE12-FIG-002"><summary>Base Figure 2 · Decimal and Binary Units</summary>
<!-- claim:BASE12-FIG-002-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">39.</span>Figure 2〈Decimal and Binary Units〉：定義〈Decimal and Binary Units〉使用的數值單位或 byte 寬度慣例。</p><details class="source-note"><summary>來源：Base 2.4 §1.4.2</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §1.4.2, Figure 2, 文件頁 3, PDF 頁 29</p></details>

</details>
<!-- figure-table:BASE12-FIG-003 -->
<details class="field-note" id="figure-BASE12-FIG-003"><summary>Base Figure 3 · Byte, Word, and Dword Relationships</summary>
<!-- claim:BASE12-FIG-003-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">40.</span>Figure 3〈Byte, Word, and Dword Relationships〉：定義〈Byte, Word, and Dword Relationships〉使用的數值單位或 byte 寬度慣例。</p><dl class="term-note" aria-label="本段名詞"><div><dt>word</dt><dd>word；16 bits，也就是 2 bytes。它比 Dword 小一半；欄位長度不能只看數字，還要看單位。</dd></div></dl><details class="source-note"><summary>來源：Base 2.4 §1.4.3</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §1.4.3, Figure 3, 文件頁 5, PDF 頁 31</p></details>

</details>
</details>
</section>
<section id="additional-details"><h2 id="further-mechanisms">補充機制與資料格式</h2>
<!-- claim:BASE12-KEYWORDS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">41.</span>規格的 mandatory、may、optional、reserved、shall、should 各有固定語氣；引用時保留英文 keyword，不能把 may 或 should 翻成 shall。</p><details class="source-note"><summary>來源：Base 2.4 §1.4.1</summary><p>來源：NVME-BASE-2.4, Rev. 2.4, §1.4.1, 文件頁 2-3, PDF 頁 28-29</p></details>
</section>
<section id="knowledge-check"><h2 id="review-questions">學完後想一想</h2>
<!-- qa:base-ch1-2-spec-family -->
<details class="review-question" id="qa-base-ch1-2-spec-family"><summary>1. 要了解 Read 做什麼，以及它如何經 PCIe 傳送，為何需要查不同規格？</summary>
<div data-qa-answer="base-ch1-2-spec-family"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">42.</span>Command Set 定義命令對資料的作用；Transport 定義命令與完成如何經連接方式交換；Base 提供共用的 controller、queue 與管理模型。三者共同描述一次完整操作。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §1.1.1, 文件頁 1, PDF 頁 27</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §2.3.2, 文件頁 33, PDF 頁 59</p>
</details></details>
<!-- qa:base-ch1-2-queue-doorbell -->
<details class="review-question" id="qa-base-ch1-2-queue-doorbell"><summary>2. Host 寫 doorbell 時，命令本身放在哪裡？</summary>
<div data-qa-answer="base-ch1-2-queue-doorbell"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">43.</span>命令已放在 Submission Queue 的 entry 中。Doorbell 更新 queue 的進度資訊，讓 controller 知道可處理的範圍；它不是整筆命令的承載位置。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §2.1, 文件頁 21-23, PDF 頁 47-49</p>
</details></details>
<!-- qa:base-ch1-2-shared-namespace -->
<details class="review-question" id="qa-base-ch1-2-shared-namespace"><summary>3. 同一 namespace 可由 2 個 controllers 存取，是否代表有 2 份資料？</summary>
<div data-qa-answer="base-ch1-2-shared-namespace"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">44.</span>不代表。Controller 是存取端點，namespace 是邏輯儲存空間；多個存取端點可以連到同一空間。是否有實體副本屬另一層的儲存實作問題。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §2.3.3, 文件頁 33-35, PDF 頁 59-61</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §2.4.1, 文件頁 35-37, PDF 頁 61-63</p>
</details></details>
<!-- qa:base-ch1-2-units -->
<details class="review-question" id="qa-base-ch1-2-units"><summary>4. 看到某長度欄位的 raw value 為 3，為何不能立即說它是 3 bytes？</summary>
<div data-qa-answer="base-ch1-2-units"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">45.</span>必須先確認單位和編碼。若是 zero-based 的 dword 數，3 代表 4 dwords，也就是 16 bytes；若是實際 byte 數，才是 3 bytes。</p></div>
<details class="source-note"><summary>來源</summary>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §1.4.2, 文件頁 3-5, PDF 頁 29-31</p>
<p>來源：NVME-BASE-2.4, Rev. 2.4, §1.4.3, 文件頁 5, PDF 頁 31</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>採用的規格版本</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
