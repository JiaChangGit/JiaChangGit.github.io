---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4 Chapter 3: Controllers, Queues, Initialization, and Resets"
date: 2026-08-28
description: "An NVMe technical report covering the main ideas, mechanisms, conditions, and examples."
lang: en
img: posts/2026/cat_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
nvme_notes: true
---
[繁體中文]({% post_url 2026-08-28-nvme-base-ch3-zh-tw %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-hidden="true">01.</span>Before a controller can process I/O, its interface, queues, and operating state must be established. This note follows the controller lifecycle through capabilities, initialization, command processing, memory resources, shutdown, resets, and firmware activation.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl>
<h2 id="main-ideas">The main ideas</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>Startup and capabilities</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-hidden="true">02.</span>Identify the controller, configure required properties, and establish readiness.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div></dl></article>
<article><span class="axis-number">02</span><h3>Queues and processing</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-hidden="true">03.</span>Understand queue positions, doorbell updates, and arbitration.</p></article>
<article><span class="axis-number">03</span><h3>Resources and lifecycle</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-hidden="true">04.</span>Distinguish capacity, controller memory, and the scope of state changes.</p></article>
</div>

<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">05.</span>Submission queues hold commands from the host, and completion queues hold results from the controller. The host establishes these shared mechanisms before using commands such as reads and writes.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div></dl>
</section>
<section class="lesson" id="module-identity"><h2 id="heading-identity"><span class="section-number">01</span> Controller types, identifiers, and capabilities</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">06.</span>Controller type answers what work a controller can perform, Controller ID answers which controller it is, and support-requirement Figures answer the required support level of a command, log, or feature in a particular context. Figures 23-32 belong in one reading sequence, but the three questions cannot be collapsed into one Boolean.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASE3-STATIC -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">07.</span>A memory-based controller shall support only the static controller model.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.1, printed pages 38, PDF pages 64</p></details>
<!-- claim:BASE3-TYPES -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">08.</span>This report uses the I/O and Administrative controller roles. The former performs user-data I/O; the latter is management-oriented and does not support data I/O commands. Both have one Admin Submission/Completion Queue pair.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Administrative controller</dt><dd>Administrative controller, a management-oriented controller type that does not execute user-data I/O commands.</dd></div><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.1.3-3.1.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3-3.1.3.2, printed pages 39-43, PDF pages 65-69</p></details>
<!-- claim:BASE3-ORDER -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">09.</span>Except for fused operations, fetched commands and completions have no general ordering guarantee. Enforcing any required order is the host's responsibility.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.1.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3, printed pages 40, PDF pages 66</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>I/O controller</td><td>Can execute user-data I/O</td><td>Optional capabilities still require individual checks</td></tr><tr><td>Administrative controller</td><td>Management purpose without data I/O commands</td><td>An Admin Queue does not make it an I/O controller</td></tr><tr><td>Support marker</td><td>Expresses support strength for a row and context</td><td>Never interpret the fields it without its column and footnote</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>Administrative controller</dt><dd>Administrative controller, a management-oriented controller type that does not execute user-data I/O commands.</dd></div><div><dt>I/O controller</dt><dd>I/O controller, a controller type capable of executing user-data I/O commands.</dd></div><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">10.</span>Informative example: after detecting an Administrative controller, software still creates the Admin SQ/CQ and performs management commands, but it must not attach a namespace data path to that controller. Classifying by the mere presence of an Admin Queue incorrectly merges I/O and Administrative controllers.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div><div><dt>CQ</dt><dd>Completion Queue, the queue into which a controller posts command completions.</dd></div><div><dt>SQ</dt><dd>Submission Queue, the queue into which the host places commands.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASE3-FIG-023 -->
<details class="field-note" id="figure-BASE3-FIG-023"><summary>Base Figure 23 · Controller Types</summary>
<!-- claim:BASE3-FIG-023-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">11.</span>Figure 23, "Controller Types": Shows the object or capacity relationships in Controller Types.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3, Figure 23, printed pages 39, PDF pages 65</p></details>

</details>
<!-- figure-table:BASE3-FIG-024 -->
<details class="field-note" id="figure-BASE3-FIG-024"><summary>Base Figure 24 · NVM Subsystem with Three I/O Controllers</summary>
<!-- claim:BASE3-FIG-024-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">12.</span>Figure 24, "NVM Subsystem with Three I/O Controllers": Shows the object or capacity relationships in NVM Subsystem with Three I/O Controllers.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.1.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.1, Figure 24, printed pages 41, PDF pages 67</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-025 -->
<details class="field-note" id="figure-BASE3-FIG-025"><summary>Base Figure 25 · NVM Subsystem with One Administrative and Two I/O Controllers</summary>
<!-- claim:BASE3-FIG-025-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">13.</span>Figure 25, "NVM Subsystem with One Administrative and Two I/O Controllers": Shows the object or capacity relationships in NVM Subsystem with One Administrative and Two I/O Controllers.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.2, Figure 25, printed pages 42, PDF pages 68</p></details>

</details>
<!-- figure-table:BASE3-FIG-026 -->
<details class="field-note" id="figure-BASE3-FIG-026"><summary>Base Figure 26 · NVM Subsystem with One Administrative Controller</summary>
<!-- claim:BASE3-FIG-026-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">14.</span>Figure 26, "NVM Subsystem with One Administrative Controller": Shows the object or capacity relationships in NVM Subsystem with One Administrative Controller.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.2, Figure 26, printed pages 42, PDF pages 68</p></details>

</details>
<!-- figure-table:BASE3-FIG-027 -->
<details class="field-note" id="figure-BASE3-FIG-027"><summary>Base Figure 27 · Controller IDs FFF0h to FFFFh</summary>
<!-- claim:BASE3-FIG-027-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">15.</span>Figure 27, "Controller IDs FFF0h to FFFFh": Defines the identifier composition or namespace of values shown by Controller IDs FFF0h to FFFFh.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.1.3.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.3, Figure 27, printed pages 44, PDF pages 70</p></details>

</details>
<!-- figure-table:BASE3-FIG-028 -->
<details class="field-note" id="figure-BASE3-FIG-028"><summary>Base Figure 28 · Admin Command Support Requirements</summary>
<!-- claim:BASE3-FIG-028-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">16.</span>Figure 28, "Admin Command Support Requirements": Summarizes the support levels assigned by Admin Command Support Requirements.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.3.3.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.3.3, Figure 28, printed pages 45-47, PDF pages 71-73</p></details>

</details>
<!-- figure-table:BASE3-FIG-030 -->
<details class="field-note" id="figure-BASE3-FIG-030"><summary>Base Figure 30 · Common I/O Command Support Requirements</summary>
<!-- claim:BASE3-FIG-030-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">17.</span>Figure 30, "Common I/O Command Support Requirements": Summarizes the support levels assigned by Common I/O Command Support Requirements.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.3.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.4, Figure 30, printed pages 47-48, PDF pages 73-74</p></details>

</details>
<!-- figure-table:BASE3-FIG-031 -->
<details class="field-note" id="figure-BASE3-FIG-031"><summary>Base Figure 31 · Log Page Support Requirements</summary>
<!-- claim:BASE3-FIG-031-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">18.</span>Figure 31, "Log Page Support Requirements": Summarizes the support levels assigned by Log Page Support Requirements.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.3.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.4, Figure 31, printed pages 48-50, PDF pages 74-76</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>FDP</dt><dd>Flexible Data Placement, a capability connecting data-placement hints with media-reclamation management.</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-032 -->
<details class="field-note" id="figure-BASE3-FIG-032"><summary>Base Figure 32 · Feature Support Requirements</summary>
<!-- claim:BASE3-FIG-032-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">19.</span>Figure 32, "Feature Support Requirements": Summarizes the support levels assigned by Feature Support Requirements.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.3.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.3.5, Figure 32, printed pages 50-52, PDF pages 76-78</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-properties-init"><h2 id="heading-properties-init"><span class="section-number">02</span> Initialization from configuration to CSTS.RDY</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">20.</span>Properties are not an independent register list. CAP constrains page-size, queue, and timeout capabilities; AQA, ASQ, and ACQ establish Admin queues; CC selects settings and enables the controller; CSTS.RDY finally declares readiness for normal command processing. Figures 33-46 and Figure 57 should be read along this causal chain.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CSTS</dt><dd>Controller Status, the property through which a controller reports ready, fatal-status, and shutdown state.</dd></div><div><dt>ACQ</dt><dd>Admin Completion Queue Base Address, the base address of the Admin CQ in addressable memory.</dd></div><div><dt>AQA</dt><dd>Admin Queue Attributes, the property describing Admin SQ and Admin CQ sizes.</dd></div><div><dt>ASQ</dt><dd>Admin Submission Queue Base Address, the base address of the Admin SQ in addressable memory.</dd></div><div><dt>CAP</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities.</dd></div><div><dt>RDY</dt><dd>Ready, the CSTS bit indicating whether the controller is ready for normal command processing.</dd></div><div><dt>CC</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASE3-PROPERTY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">21.</span>The host shall access a property at its starting offset using the specified width; the PCIe Transport adds the access rules for a memory-based controller.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>offset</dt><dd>offset: a displacement measured from a stated start. It answers “how far from the start,” unlike an index.</dd></div><div><dt>PCIe</dt><dd>PCI Express, the transport and device interconnect used by an NVMe memory-based controller.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.1.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, printed pages 52-54, PDF pages 78-80</p></details>
<!-- claim:BASE3-INIT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">22.</span>PCIe initialization reads CAP, configures AQA/ASQ/ACQ and CC, then waits for CSTS.RDY. Ready mode and CRTO affect host wait and error handling.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CRTO</dt><dd>Controller Ready Timeouts, the property reporting wait times for specific ready modes.</dd></div><div><dt>CSTS</dt><dd>Controller Status, the property through which a controller reports ready, fatal-status, and shutdown state.</dd></div><div><dt>PCIe</dt><dd>PCI Express, the transport and device interconnect used by an NVMe memory-based controller.</dd></div><div><dt>ACQ</dt><dd>Admin Completion Queue Base Address, the base address of the Admin CQ in addressable memory.</dd></div><div><dt>AQA</dt><dd>Admin Queue Attributes, the property describing Admin SQ and Admin CQ sizes.</dd></div><div><dt>ASQ</dt><dd>Admin Submission Queue Base Address, the base address of the Admin SQ in addressable memory.</dd></div><div><dt>CAP</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities.</dd></div><div><dt>RDY</dt><dd>Ready, the CSTS bit indicating whether the controller is ready for normal command processing.</dd></div><div><dt>CC</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.5.1, 3.5.3-3.5.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pages 105-113, PDF pages 131-139</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>CAP</td><td>Capabilities and limits</td><td>Read before writing configuration</td></tr><tr><td>AQA/ASQ/ACQ</td><td>Admin-queue sizes and addresses</td><td>Must match page and alignment capabilities</td></tr><tr><td>CC</td><td>Host selections and enable</td><td>Written values must be compatible with CAP</td></tr><tr><td>CSTS</td><td>Controller-reported state</td><td>RDY, CFS, and SHST are not interchangeable</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>SHST</dt><dd>Shutdown Status, the CSTS field through which the controller reports shutdown progress.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">23.</span>Informative example: the host selects a 4 KiB MPS, so ASQ and ACQ base addresses must obey that page-size alignment. After writing CC.EN=1, the host waits for CSTS.RDY=1 within the CAP/CRTO time bound. If CFS appears first, the flow enters error recovery rather than creating I/O queues.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CRTO</dt><dd>Controller Ready Timeouts, the property reporting wait times for specific ready modes.</dd></div><div><dt>MPS</dt><dd>Memory Page Size, the controller memory-page-size setting; it affects queue addresses and PRP alignment.</dd></div><div><dt>EN</dt><dd>Enable, the CC bit controlling controller enable state.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASE3-FIG-033 -->
<details class="field-note" id="figure-BASE3-FIG-033"><summary>Base Figure 33 · Property Definition</summary>
<!-- claim:BASE3-FIG-033-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">24.</span>Figure 33, "Property Definition": Defines the concrete layout or value relationships for Property Definition.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, Figure 33, printed pages 52-53, PDF pages 78-79</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>OFST</dt><dd>Offset, the dword-based image-relative offset in Firmware Image Download.</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-034 -->
<details class="field-note" id="figure-BASE3-FIG-034"><summary>Base Figure 34 · Memory-Based Property Definition</summary>
<!-- claim:BASE3-FIG-034-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">25.</span>Figure 34, "Memory-Based Property Definition": Defines the concrete layout or value relationships for Memory-Based Property Definition.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, Figure 34, printed pages 54, PDF pages 80</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CAP.DSTRD</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.DSTRD selects its DSTRD member field.</dd></div><div><dt>DSTRD</dt><dd>Doorbell Stride, the CAP field determining spacing between adjacent doorbell registers.</dd></div><div><dt>OFST</dt><dd>Offset, the dword-based image-relative offset in Firmware Image Download.</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-036 -->
<details class="field-note" id="figure-BASE3-FIG-036"><summary>Base Figure 36 · Offset 0h: CAP - Controller Capabilities</summary>
<!-- claim:BASE3-FIG-036-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">26.</span>Figure 36, "Offset 0h: CAP - Controller Capabilities": Defines CAP (Controller Capabilities) at offset 0h and identifies the fields that software must read the fields at that location.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>offset</dt><dd>offset: a displacement measured from a stated start. It answers “how far from the start,” unlike an index.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 36, printed pages 55-58, PDF pages 81-84</p></details>

</details>
<!-- figure-table:BASE3-FIG-037 -->
<details class="field-note" id="figure-BASE3-FIG-037"><summary>Base Figure 37 · Specification Version Descriptor</summary>
<!-- claim:BASE3-FIG-037-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">27.</span>Figure 37, "Specification Version Descriptor": Defines the concrete layout or value relationships for Specification Version Descriptor.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 37, printed pages 58, PDF pages 84</p></details>

</details>
<!-- figure-table:BASE3-FIG-038 -->
<details class="field-note" id="figure-BASE3-FIG-038"><summary>Base Figure 38 · NVM Express Base Specification Version Property Reset Values</summary>
<!-- claim:BASE3-FIG-038-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">28.</span>Figure 38, "NVM Express Base Specification Version Property Reset Values": Defines the concrete layout or value relationships for NVM Express Base Specification Version Property Reset Values.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.1, Figure 38, printed pages 58-59, PDF pages 84-85</p></details>

</details>
<!-- figure-table:BASE3-FIG-041 -->
<details class="field-note" id="figure-BASE3-FIG-041"><summary>Base Figure 41 · Offset 14h: CC - Controller Configuration</summary>
<!-- claim:BASE3-FIG-041-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">29.</span>Figure 41, "Offset 14h: CC - Controller Configuration": Defines CC (Controller Configuration) at offset 14h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.5, Figure 41, printed pages 60-63, PDF pages 86-89</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>MPS</dt><dd>Memory Page Size, the controller memory-page-size setting; it affects queue addresses and PRP alignment.</dd></div><div><dt>SHN</dt><dd>Shutdown Notification, the CC field through which the host declares a shutdown type.</dd></div><div><dt>EN</dt><dd>Enable, the CC bit controlling controller enable state.</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-042 -->
<details class="field-note" id="figure-BASE3-FIG-042"><summary>Base Figure 42 · Offset 1Ch: CSTS - Controller Status</summary>
<!-- claim:BASE3-FIG-042-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">30.</span>Figure 42, "Offset 1Ch: CSTS - Controller Status": Defines CSTS (Controller Status) at offset 1Ch and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.5, Figure 42, printed pages 63-65, PDF pages 89-91</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>SHST</dt><dd>Shutdown Status, the CSTS field through which the controller reports shutdown progress.</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-044 -->
<details class="field-note" id="figure-BASE3-FIG-044"><summary>Base Figure 44 · Offset 24h: AQA - Admin Queue Attributes</summary>
<!-- claim:BASE3-FIG-044-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">31.</span>Figure 44, "Offset 24h: AQA - Admin Queue Attributes": Defines AQA (Admin Queue Attributes) at offset 24h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 44, printed pages 66, PDF pages 92</p></details>

</details>
<!-- figure-table:BASE3-FIG-045 -->
<details class="field-note" id="figure-BASE3-FIG-045"><summary>Base Figure 45 · Offset 28h: ASQ - Admin Submission Queue Base Address</summary>
<!-- claim:BASE3-FIG-045-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">32.</span>Figure 45, "Offset 28h: ASQ - Admin Submission Queue Base Address": Defines ASQ (Admin Submission Queue Base Address) at offset 28h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 45, printed pages 66, PDF pages 92</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CC.MPS</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.MPS selects its MPS member field.</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-046 -->
<details class="field-note" id="figure-BASE3-FIG-046"><summary>Base Figure 46 · Offset 30h: ACQ - Admin Completion Queue Base Address</summary>
<!-- claim:BASE3-FIG-046-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">33.</span>Figure 46, "Offset 30h: ACQ - Admin Completion Queue Base Address": Defines ACQ (Admin Completion Queue Base Address) at offset 30h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.9</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.9, Figure 46, printed pages 67, PDF pages 93</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CC.MPS</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.MPS selects its MPS member field.</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-057 -->
<details class="field-note" id="figure-BASE3-FIG-057"><summary>Base Figure 57 · Offset 68h: CRTO - Controller Ready Timeouts</summary>
<!-- claim:BASE3-FIG-057-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">34.</span>Figure 57, "Offset 68h: CRTO - Controller Ready Timeouts": Defines CRTO (Controller Ready Timeouts) at offset 68h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.21</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.21, Figure 57, printed pages 73, PDF pages 99</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CAP.CRMS.CRIMS</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.CRMS.CRIMS selects its CRMS.CRIMS member field.</dd></div><div><dt>CC.CRIME</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.CRIME selects its CRIME member field.</dd></div><div><dt>CC.EN</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.EN selects its EN member field.</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-queue-arbitration"><h2 id="heading-queue-arbitration"><span class="section-number">03</span> Queue positions and command selection</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">35.</span>Figures 73 and 74 define empty/full state for a queue, while Figures 80 and 81 define arbitration among SQs competing for controller service. The first problem concerns head/tail state within one ring; the second selects among candidate SQs. Priority belongs to the SQ, not to each command as an independent priority.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SQ</dt><dd>Submission Queue, the queue into which the host places commands.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASE3-QUEUE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">36.</span>A PCIe queue is a circular buffer in host-addressable memory with head and tail pointers. The host creates an I/O Completion Queue before its Submission Queue and advances pointers through doorbells.</p><details class="source-note"><summary>Sources: Base 2.4 §3.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.3.1, printed pages 88-91, PDF pages 114-117</p></details>
<!-- claim:BASE3-PROCESS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">37.</span>Command processing separates ordering, fused and atomic semantics, arbitration, and outstanding-command limits. Priority belongs to a Submission Queue, not to each command as an independent attribute.</p><details class="source-note"><summary>Sources: Base 2.4 §3.4.1-3.4.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, printed pages 101-105, PDF pages 127-131</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Empty</td><td>Head equals tail under the empty ownership definition</td><td>No entry can be fetched</td></tr><tr><td>Full</td><td>The next tail would reach an unreleased head</td><td>The host must not overwrite an entry</td></tr><tr><td>Round Robin</td><td>Candidate SQs take turns receiving service</td><td>Completion order is not submission order</td></tr><tr><td>Weighted RR + Urgent</td><td>Priority class and weight influence selection</td><td>Interpret only under the applicable configuration</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">38.</span>Informative example: an SQ of depth four has four slots, but full/empty detection still needs the ownership rule; an unsigned tail-minus-head value alone is insufficient. If SQ 1 and SQ 2 both contain commands, selecting SQ 2 first does not guarantee its command completes first because execution times may differ.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASE3-FIG-073 -->
<details class="field-note" id="figure-BASE3-FIG-073"><summary>Base Figure 73 · Empty Queue Definition</summary>
<!-- claim:BASE3-FIG-073-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">39.</span>Figure 73, "Empty Queue Definition": Defines the concrete layout or value relationships for Empty Queue Definition.</p><details class="source-note"><summary>Sources: Base 2.4 §3.3.1.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.3.1.4, Figure 73, printed pages 91, PDF pages 117</p></details>

</details>
<!-- figure-table:BASE3-FIG-074 -->
<details class="field-note" id="figure-BASE3-FIG-074"><summary>Base Figure 74 · Full Queue Definition</summary>
<!-- claim:BASE3-FIG-074-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">40.</span>Figure 74, "Full Queue Definition": Defines the concrete layout or value relationships for Full Queue Definition.</p><details class="source-note"><summary>Sources: Base 2.4 §3.3.1.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.3.1.4, Figure 74, printed pages 91, PDF pages 117</p></details>

</details>
<!-- figure-table:BASE3-FIG-080 -->
<details class="field-note" id="figure-BASE3-FIG-080"><summary>Base Figure 80 · Round Robin Arbitration</summary>
<!-- claim:BASE3-FIG-080-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">41.</span>Figure 80, "Round Robin Arbitration": Shows how Round Robin Arbitration selects work from competing Submission Queues.</p><details class="source-note"><summary>Sources: Base 2.4 §3.4.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.4.4, Figure 80, printed pages 103, PDF pages 129</p></details>

</details>
<!-- figure-table:BASE3-FIG-081 -->
<details class="field-note" id="figure-BASE3-FIG-081"><summary>Base Figure 81 · Weighted Round Robin with Urgent Priority Class Arbitration</summary>
<!-- claim:BASE3-FIG-081-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">42.</span>Figure 81, "Weighted Round Robin with Urgent Priority Class Arbitration": Shows how Weighted Round Robin with Urgent Priority Class Arbitration selects work from competing Submission Queues.</p><details class="source-note"><summary>Sources: Base 2.4 §3.4.4.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.4.4.2, Figure 81, printed pages 104, PDF pages 130</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-memory-capacity"><h2 id="heading-memory-capacity"><span class="section-number">04</span> Namespaces, CMB, PMR, and capacity</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">43.</span>CMB and PMR properties describe the location, capability, and state of controller-exposed memory regions; capacity Figures 86-89 describe available or allocated capacity at NVM-subsystem levels. Both concern memory, but they are different spaces and cannot be merged into one free-capacity value.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CMB</dt><dd>Controller Memory Buffer, controller-provided memory in which selected queues or data structures may reside.</dd></div><div><dt>PMR</dt><dd>Persistent Memory Region, a controller-exposed memory region with persistence semantics.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASE3-CAPACITY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">44.</span>The capacity model tracks available or configured capacity separately at subsystem, Endurance Group, NVM Set, and namespace levels. Values from different levels are not directly interchangeable.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Endurance Group</dt><dd>Endurance Group, a group of NVM resources for isolating and reporting endurance-related state.</dd></div><div><dt>NVM Set</dt><dd>NVM Set, a capacity grouping that associates namespaces with a managed set of NVM resources.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.8</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.8, printed pages 125-129, PDF pages 151-155</p></details>
<!-- claim:BASE3-MEDIA -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">45.</span>NVM Sets, Endurance Groups, Reclaim Groups, and Reclaim Units describe capacity grouping, endurance management, and reclamation granularity. Support and identifiers are determined from Identify data and log-page capabilities.</p><details class="source-note"><summary>Sources: Base 2.4 §3.2.2-3.2.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, printed pages 80-85, PDF pages 106-111</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>CMB</td><td>Controller-provided working memory</td><td>Capability bits decide whether SQs, CQs, lists, or data may reside there</td></tr><tr><td>PMR</td><td>A region with persistence semantics</td><td>Enable, ready, error, and address control must be read together</td></tr><tr><td>Capacity model</td><td>Capacity of subsystem/group/set/namespace levels</td><td>Fields from different levels must not be subtracted directly</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>CMB</dt><dd>Controller Memory Buffer, controller-provided memory in which selected queues or data structures may reside.</dd></div><div><dt>PMR</dt><dd>Persistent Memory Region, a controller-exposed memory region with persistence semantics.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">46.</span>Informative example: enough CMB space for an SQ does not add the same amount of namespace capacity. The former is placement space for queues or data structures; the latter is formatted non-volatile capacity accessible to the host.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASE3-FIG-047 -->
<details class="field-note" id="figure-BASE3-FIG-047"><summary>Base Figure 47 · Offset 38h: CMBLOC - Controller Memory Buffer Location</summary>
<!-- claim:BASE3-FIG-047-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">47.</span>Figure 47, "Offset 38h: CMBLOC - Controller Memory Buffer Location": Defines CMBLOC (Controller Memory Buffer Location) at offset 38h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.9</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.9, Figure 47, printed pages 67-68, PDF pages 93-94</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>BAR</dt><dd>Base Address Register, a PCI-configuration-space register finding a device memory space.</dd></div><div><dt>BIR</dt><dd>BAR Indicator Register, a selector identifying the PCIe BAR that contains a memory structure.</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-048 -->
<details class="field-note" id="figure-BASE3-FIG-048"><summary>Base Figure 48 · Offset 3Ch: CMBSZ - Controller Memory Buffer Size</summary>
<!-- claim:BASE3-FIG-048-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">48.</span>Figure 48, "Offset 3Ch: CMBSZ - Controller Memory Buffer Size": Defines CMBSZ (Controller Memory Buffer Size) at offset 3Ch and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.11</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.11, Figure 48, printed pages 68-69, PDF pages 94-95</p></details>

</details>
<!-- figure-table:BASE3-FIG-052 -->
<details class="field-note" id="figure-BASE3-FIG-052"><summary>Base Figure 52 · Offset 50h: CMBMSC - Controller Memory Buffer Memory Space Control</summary>
<!-- claim:BASE3-FIG-052-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">49.</span>Figure 52, "Offset 50h: CMBMSC - Controller Memory Buffer Memory Space Control": Defines CMBMSC (Controller Memory Buffer Memory Space Control) at offset 50h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.14</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 52, printed pages 70-71, PDF pages 96-97</p></details>

</details>
<!-- figure-table:BASE3-FIG-053 -->
<details class="field-note" id="figure-BASE3-FIG-053"><summary>Base Figure 53 · Offset 58h: CMBSTS - Controller Memory Buffer Status</summary>
<!-- claim:BASE3-FIG-053-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">50.</span>Figure 53, "Offset 58h: CMBSTS - Controller Memory Buffer Status": Defines CMBSTS (Controller Memory Buffer Status) at offset 58h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.16</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.16, Figure 53, printed pages 71, PDF pages 97</p></details>

</details>
<!-- figure-table:BASE3-FIG-054 -->
<details class="field-note" id="figure-BASE3-FIG-054"><summary>Base Figure 54 · Offset 5Ch: CMBEBS - Controller Memory Buffer Elasticity Buffer Size</summary>
<!-- claim:BASE3-FIG-054-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">51.</span>Figure 54, "Offset 5Ch: CMBEBS - Controller Memory Buffer Elasticity Buffer Size": Defines CMBEBS (Controller Memory Buffer Elasticity Buffer Size) at offset 5Ch and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.16</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.16, Figure 54, printed pages 71, PDF pages 97</p></details>

</details>
<!-- figure-table:BASE3-FIG-055 -->
<details class="field-note" id="figure-BASE3-FIG-055"><summary>Base Figure 55 · Offset 60h: CMBSWTP - Controller Memory Buffer Sustained Write Throughput</summary>
<!-- claim:BASE3-FIG-055-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">52.</span>Figure 55, "Offset 60h: CMBSWTP - Controller Memory Buffer Sustained Write Throughput": Defines CMBSWTP (Controller Memory Buffer Sustained Write Throughput) at offset 60h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.19</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.19, Figure 55, printed pages 72, PDF pages 98</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>TLP</dt><dd>Transaction Layer Packet, a packet carried by the PCIe transaction layer.</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-058 -->
<details class="field-note" id="figure-BASE3-FIG-058"><summary>Base Figure 58 · Offset E00h: PMRCAP - Persistent Memory Region Capabilities</summary>
<!-- claim:BASE3-FIG-058-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">53.</span>Figure 58, "Offset E00h: PMRCAP - Persistent Memory Region Capabilities": Defines PMRCAP (Persistent Memory Region Capabilities) at offset E00h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.21</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.21, Figure 58, printed pages 73-74, PDF pages 99-100</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>BIR</dt><dd>BAR Indicator Register, a selector identifying the PCIe BAR that contains a memory structure.</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-059 -->
<details class="field-note" id="figure-BASE3-FIG-059"><summary>Base Figure 59 · Offset E04h: PMRCTL - Persistent Memory Region Control</summary>
<!-- claim:BASE3-FIG-059-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">54.</span>Figure 59, "Offset E04h: PMRCTL - Persistent Memory Region Control": Defines PMRCTL (Persistent Memory Region Control) at offset E04h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.22</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.22, Figure 59, printed pages 74, PDF pages 100</p></details>

</details>
<!-- figure-table:BASE3-FIG-060 -->
<details class="field-note" id="figure-BASE3-FIG-060"><summary>Base Figure 60 · Offset E08h: PMRSTS - Persistent Memory Region Status</summary>
<!-- claim:BASE3-FIG-060-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">55.</span>Figure 60, "Offset E08h: PMRSTS - Persistent Memory Region Status": Defines PMRSTS (Persistent Memory Region Status) at offset E08h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.23</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.23, Figure 60, printed pages 75, PDF pages 101</p></details>

</details>
<!-- figure-table:BASE3-FIG-061 -->
<details class="field-note" id="figure-BASE3-FIG-061"><summary>Base Figure 61 · Offset E0Ch: PMREBS - Persistent Memory Region Elasticity Buffer Size</summary>
<!-- claim:BASE3-FIG-061-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">56.</span>Figure 61, "Offset E0Ch: PMREBS - Persistent Memory Region Elasticity Buffer Size": Defines PMREBS (Persistent Memory Region Elasticity Buffer Size) at offset E0Ch and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.24</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.24, Figure 61, printed pages 76, PDF pages 102</p></details>

</details>
<!-- figure-table:BASE3-FIG-062 -->
<details class="field-note" id="figure-BASE3-FIG-062"><summary>Base Figure 62 · Offset E10h: PMRSWTP - Persistent Memory Region Sustained Write Throughput</summary>
<!-- claim:BASE3-FIG-062-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">57.</span>Figure 62, "Offset E10h: PMRSWTP - Persistent Memory Region Sustained Write Throughput": Defines PMRSWTP (Persistent Memory Region Sustained Write Throughput) at offset E10h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.24</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.24, Figure 62, printed pages 76, PDF pages 102</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>TLP</dt><dd>Transaction Layer Packet, a packet carried by the PCIe transaction layer.</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-063 -->
<details class="field-note" id="figure-BASE3-FIG-063"><summary>Base Figure 63 · Offset E14h: PMRMSCL - Persistent Memory Region Memory Space Control Lower</summary>
<!-- claim:BASE3-FIG-063-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">58.</span>Figure 63, "Offset E14h: PMRMSCL - Persistent Memory Region Memory Space Control Lower": Defines PMRMSCL (Persistent Memory Region Memory Space Control Lower) at offset E14h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.26</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.26, Figure 63, printed pages 77, PDF pages 103</p></details>

</details>
<!-- figure-table:BASE3-FIG-064 -->
<details class="field-note" id="figure-BASE3-FIG-064"><summary>Base Figure 64 · Offset E18h: PMRMSCU - Persistent Memory Region Memory Space Control Upper</summary>
<!-- claim:BASE3-FIG-064-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">59.</span>Figure 64, "Offset E18h: PMRMSCU - Persistent Memory Region Memory Space Control Upper": Defines PMRMSCU (Persistent Memory Region Memory Space Control Upper) at offset E18h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.26</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.26, Figure 64, printed pages 77, PDF pages 103</p></details>

</details>
<!-- figure-table:BASE3-FIG-086 -->
<details class="field-note" id="figure-BASE3-FIG-086"><summary>Base Figure 86 · Simple NVM Subsystem</summary>
<!-- claim:BASE3-FIG-086-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">60.</span>Figure 86, "Simple NVM Subsystem": Shows the object or capacity relationships in Simple NVM Subsystem.</p><details class="source-note"><summary>Sources: Base 2.4 §3.8.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.8.2, Figure 86, printed pages 126, PDF pages 152</p></details>

</details>
<!-- figure-table:BASE3-FIG-087 -->
<details class="field-note" id="figure-BASE3-FIG-087"><summary>Base Figure 87 · Vertically-Organized NVM Subsystem</summary>
<!-- claim:BASE3-FIG-087-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">61.</span>Figure 87, "Vertically-Organized NVM Subsystem": Shows the object or capacity relationships in Vertically-Organized NVM Subsystem.</p><details class="source-note"><summary>Sources: Base 2.4 §3.8.2.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.8.2.2, Figure 87, printed pages 127, PDF pages 153</p></details>

</details>
<!-- figure-table:BASE3-FIG-088 -->
<details class="field-note" id="figure-BASE3-FIG-088"><summary>Base Figure 88 · Horizontally-Organized Dual NAND NVM Subsystem</summary>
<!-- claim:BASE3-FIG-088-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">62.</span>Figure 88, "Horizontally-Organized Dual NAND NVM Subsystem": Shows the object or capacity relationships in Horizontally-Organized Dual NAND NVM Subsystem.</p><details class="source-note"><summary>Sources: Base 2.4 §3.8.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.8.2.3, Figure 88, printed pages 128, PDF pages 154</p></details>

</details>
<!-- figure-table:BASE3-FIG-089 -->
<details class="field-note" id="figure-BASE3-FIG-089"><summary>Base Figure 89 · Capacity Information Field Usage</summary>
<!-- claim:BASE3-FIG-089-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">63.</span>Figure 89, "Capacity Information Field Usage": Defines the concrete layout or value relationships for Capacity Information Field Usage.</p><details class="source-note"><summary>Sources: Base 2.4 §3.8.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.8.3, Figure 89, printed pages 129, PDF pages 155</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-lifecycle"><h2 id="heading-lifecycle"><span class="section-number">05</span> Shutdown, reset, and retained state</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">64.</span>The common lifecycle question is which layer of state remains valid. Normal shutdown coordinates through CC.SHN and CSTS.SHST; resets exist at subsystem, controller, and queue levels; Keep Alive monitors host-controller liveness; firmware activation may require a particular reset. The same temporary inability to process commands does not imply the same recovery.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SHN</dt><dd>Shutdown Notification, the CC field through which the host declares a shutdown type.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASE3-SHUTDOWN -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">65.</span>Normal shutdown begins when the host sets CC.SHN and the controller reports progress in CSTS.SHST. NVM subsystem shutdown has a wider scope and is not the same as one controller shutdown.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM subsystem</dt><dd>NVM subsystem, the NVMe system boundary containing controllers, ports, namespaces, and non-volatile storage resources.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.6.1, 3.6.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, printed pages 113-120, PDF pages 139-146</p></details>
<!-- claim:BASE3-RESET -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">66.</span>NVM Subsystem, Controller Level, and Queue Level resets have different scopes. A recovery flow first determines which state is cleared and whether queues still exist.</p><details class="source-note"><summary>Sources: Base 2.4 §3.7</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.7, printed pages 120-125, PDF pages 146-151</p></details>
<!-- claim:BASE3-KEEPALIVE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">67.</span>Keep Alive uses KATO and KATT for host/controller liveness monitoring. This report retains only controller-common and PCIe-applicable timer, command, and timeout behavior.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>KATO</dt><dd>Keep Alive Timeout, the negotiated liveness timeout between host and controller.</dd></div><div><dt>KATT</dt><dd>Keep Alive Timeout Total, the controller timing basis for detecting a keep-alive timeout.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.9</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.9, printed pages 129-135, PDF pages 155-161</p></details>
<!-- claim:BASE3-FIRMWARE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">68.</span>A privileged action may affect other hosts or controllers. Firmware update separates image download, commit/activation, and any required reset; the host sequences the flow using the reported activation action.</p><details class="source-note"><summary>Sources: Base 2.4 §3.10-3.11</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.10-3.11, printed pages 135-138, PDF pages 161-164</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Normal shutdown</td><td>Protected stop with progress reporting</td><td>Observe SHN/SHST</td></tr><tr><td>Controller reset</td><td>Controller-scope state</td><td>Queue preservation depends on reset type</td></tr><tr><td>NVM subsystem reset</td><td>Wider subsystem scope</td><td>May affect multiple controllers</td></tr><tr><td>Keep Alive timeout</td><td>Liveness failure</td><td>Must not be equated with media failure</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM subsystem</dt><dd>NVM subsystem, the NVMe system boundary containing controllers, ports, namespaces, and non-volatile storage resources.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">69.</span>Informative example: for a normal shutdown, the host stops submitting new I/O, sets CC.SHN, and observes CSTS.SHST. If controller fatal status appears while waiting, subsequent recovery follows reset scope and rebuilds resources rather than assuming normal shutdown completed.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASE3-FIG-043 -->
<details class="field-note" id="figure-BASE3-FIG-043"><summary>Base Figure 43 · Offset 20h: NSSR - NVM Subsystem Reset</summary>
<!-- claim:BASE3-FIG-043-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">70.</span>Figure 43, "Offset 20h: NSSR - NVM Subsystem Reset": Defines NSSR (NVM Subsystem Reset) at offset 20h and identifies the fields that software must read the fields at that location.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NSSR</dt><dd>NVM Subsystem Reset, the property used to initiate an NVM subsystem reset.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.6, Figure 43, printed pages 66, PDF pages 92</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NSSR</dt><dd>NVM Subsystem Reset, the property used to initiate an NVM subsystem reset.</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-056 -->
<details class="field-note" id="figure-BASE3-FIG-056"><summary>Base Figure 56 · Offset 64h: NSSD - NVM Subsystem Shutdown</summary>
<!-- claim:BASE3-FIG-056-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">71.</span>Figure 56, "Offset 64h: NSSD - NVM Subsystem Shutdown": Defines NSSD (NVM Subsystem Shutdown) at offset 64h and identifies the fields that software must read the fields at that location.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NSSD</dt><dd>NVM Subsystem Shutdown, the property controlling the wider-scope subsystem shutdown.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.19</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.19, Figure 56, printed pages 72, PDF pages 98</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CAP.CPS</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.CPS selects its CPS member field.</dd></div><div><dt>NSSD</dt><dd>NVM Subsystem Shutdown, the property controlling the wider-scope subsystem shutdown.</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-084 -->
<details class="field-note" id="figure-BASE3-FIG-084"><summary>Base Figure 84 · Admin Commands Permitted to Return a Status Code of Admin Command Media Not</summary>
<!-- claim:BASE3-FIG-084-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">72.</span>Figure 84, "Admin Commands Permitted to Return a Status Code of Admin Command Media Not": Defines the status/error classification represented by Admin Commands Permitted to Return a Status Code of Admin Command Media Not.</p><details class="source-note"><summary>Sources: Base 2.4 §3.5.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.5.3, Figure 84, printed pages 110-111, PDF pages 136-137</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CAP.CRMS.CRIMS</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.CRMS.CRIMS selects its CRMS.CRIMS member field.</dd></div><div><dt>CAP.CRMS.CRWMS</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.CRMS.CRWMS selects its CRMS.CRWMS member field.</dd></div><div><dt>CAP.CRMS</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.CRMS selects its CRMS member field.</dd></div><div><dt>CC.CRIME</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.CRIME selects its CRIME member field.</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-085 -->
<details class="field-note" id="figure-BASE3-FIG-085"><summary>Base Figure 85 · Shutdown Processing Interactions</summary>
<!-- claim:BASE3-FIG-085-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">73.</span>Figure 85, "Shutdown Processing Interactions": Shows the state or timing progression represented by Shutdown Processing Interactions.</p><details class="source-note"><summary>Sources: Base 2.4 §3.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.6, Figure 85, printed pages 113, PDF pages 139</p></details>

</details>
<!-- figure-table:BASE3-FIG-090 -->
<details class="field-note" id="figure-BASE3-FIG-090"><summary>Base Figure 90 · Detecting Timeout Takes up to 2 * KATT</summary>
<!-- claim:BASE3-FIG-090-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">74.</span>Figure 90, "Detecting Timeout Takes up to 2 * KATT": Shows the state or timing progression represented by Detecting Timeout Takes up to 2 * KATT.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>KATT</dt><dd>Keep Alive Timeout Total, the controller timing basis for detecting a keep-alive timeout.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.9.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.9.4.1, Figure 90, printed pages 133, PDF pages 159</p></details>

</details>
<!-- figure-table:BASE3-FIG-091 -->
<details class="field-note" id="figure-BASE3-FIG-091"><summary>Base Figure 91 · Example Privileged Action Admin Commands</summary>
<!-- claim:BASE3-FIG-091-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">75.</span>Figure 91, "Example Privileged Action Admin Commands": Identifies the privileged-operation boundary illustrated by Example Privileged Action Admin Commands.</p><details class="source-note"><summary>Sources: Base 2.4 §3.10</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.10, Figure 91, printed pages 135, PDF pages 161</p></details>

</details>
</details>
</section>
<section id="additional-details"><h2 id="further-mechanisms">Additional mechanisms and data formats</h2>
<!-- claim:BASE3-NAMESPACE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">76.</span>NSID 0h is invalid and FFFFFFFFh is the broadcast value. Other NSIDs still need allocated/unallocated and active/inactive classification; numeric range alone is insufficient.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NSID</dt><dd>Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.2.1, printed pages 78-80, PDF pages 104-106</p></details>
<!-- claim:BASE3-DOMAIN -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">77.</span>A domain is a failure or communication boundary inside an NVM subsystem. In a multi-domain subsystem, each domain identifier shall be unique within that subsystem.</p><details class="source-note"><summary>Sources: Base 2.4 §3.2.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.2.5, printed pages 85-88, PDF pages 111-114</p></details>
<!-- figure-table:BASE3-FIG-039 -->
<details class="field-note" id="figure-BASE3-FIG-039"><summary>Base Figure 39 · Offset Ch: INTMS - Interrupt Mask Set</summary>
<!-- claim:BASE3-FIG-039-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">78.</span>Figure 39, "Offset Ch: INTMS - Interrupt Mask Set": Defines INTMS (Interrupt Mask Set) at offset Ch and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.2, Figure 39, printed pages 59, PDF pages 85</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>MSI</dt><dd>Message Signaled Interrupt, a PCI mechanism that delivers an interrupt through a memory-write message.</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-040 -->
<details class="field-note" id="figure-BASE3-FIG-040"><summary>Base Figure 40 · Offset 10h: INTMC - Interrupt Mask Clear</summary>
<!-- claim:BASE3-FIG-040-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">79.</span>Figure 40, "Offset 10h: INTMC - Interrupt Mask Clear": Defines INTMC (Interrupt Mask Clear) at offset 10h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.2, Figure 40, printed pages 59, PDF pages 85</p></details>

</details>
<!-- figure-table:BASE3-FIG-049 -->
<details class="field-note" id="figure-BASE3-FIG-049"><summary>Base Figure 49 · Offset 40h: BPINFO - Boot Partition Information</summary>
<!-- claim:BASE3-FIG-049-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">80.</span>Figure 49, "Offset 40h: BPINFO - Boot Partition Information": Defines BPINFO (Boot Partition Information) at offset 40h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.12</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.12, Figure 49, printed pages 69, PDF pages 95</p></details>

</details>
<!-- figure-table:BASE3-FIG-050 -->
<details class="field-note" id="figure-BASE3-FIG-050"><summary>Base Figure 50 · Offset 44h: BPRSEL - Boot Partition Read Select</summary>
<!-- claim:BASE3-FIG-050-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">81.</span>Figure 50, "Offset 44h: BPRSEL - Boot Partition Read Select": Defines BPRSEL (Boot Partition Read Select) at offset 44h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.12</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.12, Figure 50, printed pages 69-70, PDF pages 95-96</p></details>

</details>
<!-- figure-table:BASE3-FIG-051 -->
<details class="field-note" id="figure-BASE3-FIG-051"><summary>Base Figure 51 · Offset 48h: BPMBL - Boot Partition Memory Buffer Location</summary>
<!-- claim:BASE3-FIG-051-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">82.</span>Figure 51, "Offset 48h: BPMBL - Boot Partition Memory Buffer Location": Defines BPMBL (Boot Partition Memory Buffer Location) at offset 48h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: Base 2.4 §3.1.4.14</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4.14, Figure 51, printed pages 70, PDF pages 96</p></details>

</details>
<!-- figure-table:BASE3-FIG-065 -->
<details class="field-note" id="figure-BASE3-FIG-065"><summary>Base Figure 65 · NSID Types and Relationship to Namespace</summary>
<!-- claim:BASE3-FIG-065-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">83.</span>Figure 65, "NSID Types and Relationship to Namespace": Defines the identifier composition or namespace of values shown by NSID Types and Relationship to Namespace.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NSID</dt><dd>Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §3.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.2.1, Figure 65, printed pages 78-79, PDF pages 104-105</p></details>

</details>
<!-- figure-table:BASE3-FIG-066 -->
<details class="field-note" id="figure-BASE3-FIG-066"><summary>Base Figure 66 · NSID Types</summary>
<!-- claim:BASE3-FIG-066-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">84.</span>Figure 66, "NSID Types": Defines the identifier composition or namespace of values shown by NSID Types.</p><details class="source-note"><summary>Sources: Base 2.4 §3.2.1.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.2.1.5, Figure 66, printed pages 79, PDF pages 105</p></details>

</details>
<!-- figure-table:BASE3-FIG-067 -->
<details class="field-note" id="figure-BASE3-FIG-067"><summary>Base Figure 67 · NVM Sets and Associated Namespaces</summary>
<!-- claim:BASE3-FIG-067-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">85.</span>Figure 67, "NVM Sets and Associated Namespaces": Shows the object or capacity relationships in NVM Sets and Associated Namespaces.</p><details class="source-note"><summary>Sources: Base 2.4 §3.2.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.2.2, Figure 67, printed pages 81, PDF pages 107</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM Set</dt><dd>NVM Set, a capacity grouping that associates namespaces with a managed set of NVM resources.</dd></div></dl>
</details>
<!-- figure-table:BASE3-FIG-068 -->
<details class="field-note" id="figure-BASE3-FIG-068"><summary>Base Figure 68 · NVM Set Aware Admin Commands</summary>
<!-- claim:BASE3-FIG-068-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">86.</span>Figure 68, "NVM Set Aware Admin Commands": Shows the object or capacity relationships in NVM Set Aware Admin Commands.</p><details class="source-note"><summary>Sources: Base 2.4 §3.2.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.2.2, Figure 68, printed pages 81, PDF pages 107</p></details>

</details>
<!-- figure-table:BASE3-FIG-069 -->
<details class="field-note" id="figure-BASE3-FIG-069"><summary>Base Figure 69 · NVM Sets and Associated Namespaces</summary>
<!-- claim:BASE3-FIG-069-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">87.</span>Figure 69, "NVM Sets and Associated Namespaces": Shows the object or capacity relationships in NVM Sets and Associated Namespaces.</p><details class="source-note"><summary>Sources: Base 2.4 §3.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.2.3, Figure 69, printed pages 83, PDF pages 109</p></details>

</details>
<!-- figure-table:BASE3-FIG-070 -->
<details class="field-note" id="figure-BASE3-FIG-070"><summary>Base Figure 70 · Flexible Data Placement Logical View of Non-Volatile Storage</summary>
<!-- claim:BASE3-FIG-070-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">88.</span>Figure 70, "Flexible Data Placement Logical View of Non-Volatile Storage": Shows the object or capacity relationships in Flexible Data Placement Logical View of Non-Volatile Storage.</p><details class="source-note"><summary>Sources: Base 2.4 §3.2.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.2.4, Figure 70, printed pages 85, PDF pages 111</p></details>

</details>
<!-- figure-table:BASE3-FIG-071 -->
<details class="field-note" id="figure-BASE3-FIG-071"><summary>Base Figure 71 · Example 1 Domain Structure</summary>
<!-- claim:BASE3-FIG-071-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">89.</span>Figure 71, "Example 1 Domain Structure": Defines the concrete layout or value relationships for Example 1 Domain Structure.</p><details class="source-note"><summary>Sources: Base 2.4 §3.2.5.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §3.2.5.1, Figure 71, printed pages 86, PDF pages 112</p></details>

</details>
</section>
<section id="knowledge-check"><h2 id="review-questions">Check your understanding</h2>
<!-- qa:base-ch3-ready -->
<details class="review-question" id="qa-base-ch3-ready"><summary>1. Does discovering a controller capability establish that it is ready for I/O?</summary>
<div data-qa-answer="base-ch3-ready"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">90.</span>Capability describes what is supported; initialization and ready state describe whether operation can begin now. Queue setup, enablement, and readiness checks still precede use under the applicable conditions.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §3.1.4, printed pages 52-54, PDF pages 78-80</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §3.5.1, 3.5.3-3.5.4, printed pages 105-113, PDF pages 131-139</p>
</details></details>
<!-- qa:base-ch3-queue-order -->
<details class="review-question" id="qa-base-ch3-queue-order"><summary>2. Must a command submitted earlier in an SQ complete first?</summary>
<div data-qa-answer="base-ch3-queue-order"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">91.</span>Submission order, controller work selection, and completion order are distinct. SQ position alone generally cannot establish completion order; dependencies require the synchronization or command mechanisms defined by the specification.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §3.3.1, printed pages 88-91, PDF pages 114-117</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §3.4.1-3.4.5, printed pages 101-105, PDF pages 127-131</p>
</details></details>
<!-- qa:base-ch3-shutdown-reset -->
<details class="review-question" id="qa-base-ch3-shutdown-reset"><summary>3. Why is an orderly shutdown not equivalent to a reset?</summary>
<div data-qa-answer="base-ch3-shutdown-reset"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">92.</span>Shutdown includes host notification and controller completion status, providing an explicit handoff before power removal. A reset changes controller or subsystem state according to its level. Their triggers, scope, and retained states differ.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §3.6.1, 3.6.3, printed pages 113-120, PDF pages 139-146</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §3.7, printed pages 120-125, PDF pages 146-151</p>
</details></details>
<!-- qa:base-ch3-memory-regions -->
<details class="review-question" id="qa-base-ch3-memory-regions"><summary>4. Why can controller-visible memory regions not all be counted as namespace capacity?</summary>
<div data-qa-answer="base-ch3-memory-regions"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">93.</span>A namespace provides storage addressed as logical blocks. Regions such as CMB and PMR have their own purposes, access methods, and persistence rules. Being on the same device does not give them the same capacity or data model.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §3.2.2-3.2.4, printed pages 80-85, PDF pages 106-111</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §3.8, printed pages 125-129, PDF pages 151-155</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>Specification editions</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
