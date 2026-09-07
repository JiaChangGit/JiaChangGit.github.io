---
layout: post
read_time: true
show_date: true
title: "NVMe over PCIe Transport 1.4: Complete Transport Binding"
date: 2026-08-28
description: "An NVMe technical report covering the main ideas, mechanisms, conditions, and examples."
lang: en
img: posts/2026/catFlower_title.jpg
tags: [NVMe, PCIe, Specification]
category: NVMe
author: Jia-Chang
github: JiaChangGit/JiaChangGit.github.io/tree/main/DOCS/nvme-spec-report
toc: yes
nvme_notes: true
---
[繁體中文]({% post_url 2026-08-28-nvme-pcie-transport-1-4-zh-tw %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="opening">NVMe over PCIe Transport explains how NVMe queues, properties, and notifications operate over PCIe. This note connects memory-mapped I/O, DMA, and interrupts to the transfer of an NVMe command.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express, the specification family for a host interface to a non-volatile-memory subsystem.</dd></div><div><dt>PCIe</dt><dd>PCI Express, the transport and device interconnect used by an NVMe memory-based controller.</dd></div><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl>
<h2 id="main-ideas">The main ideas</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>Interface locations</h3><p>Use BARs and configuration space to find the NVMe interface and capabilities.</p></article>
<article><span class="axis-number">02</span><h3>Commands and notifications</h3><p>Distinguish queue data, doorbells, and interrupts.</p></article>
<article><span class="axis-number">03</span><h3>Platform behavior</h3><p>Understand the scope of resets, power, error reporting, and link measurements.</p></article>
</div>

<p>The Base specification defines the common NVMe command and queue model; PCIe Transport supplies the local PCIe binding. Accessing a queue entry in memory and accessing a device MMIO register are different kinds of access.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>MMIO</dt><dd>Memory-Mapped I/O, access to device registers through CPU memory operations.</dd></div></dl>
</section>
<section class="lesson" id="module-layers"><h2 id="heading-layers"><span class="section-number">01</span> How NVMe uses PCIe</h2>
<p>Figure 1 shows document applicability and Figure 2 separates protocol responsibility. Engineering analysis separates command semantics from the way host memory, MMIO, configuration space, and interrupts carry the operation. The Transport does not rewrite Base when the two conflict.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:PCIE14-SCOPE -->
<p>The PCIe Transport supplements the Base Specification with PCIe-specific structures, extensions, requirements, and behavior; common NVMe behavior remains in Base. In a conflict, Base has higher precedence than a Transport Specification.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §1.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, printed pages 6, PDF pages 6</p></details>
<!-- claim:PCIE14-CONVENTION -->
<p>This document inherits Base conventions. In register or property tables, the Reset column instead denotes the post-reset field value defined by the applicable PCI or PCIe specification.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §1.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.3, printed pages 6-7, PDF pages 6-7</p></details>
<!-- claim:PCIE14-OVERVIEW -->
<p>The PCIe transport uses memory-mapped I/O for data and register access, along with PCIe configuration space and message-signaled interrupts.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, printed pages 8, PDF pages 8</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Base</td><td>Common command and completion semantics</td><td>Highest-precedence NVMe definition</td></tr><tr><td>PCIe Transport</td><td>Address, register, doorbell, and interrupt binding</td><td>Adds PCIe-specific requirements</td></tr><tr><td>PCI-SIG specifications</td><td>Native PCIe capability and transaction semantics</td><td>This report covers only NVMe-specific statements present in the supplied source</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p>Informative example: Base defines Firmware Commit CA/FS and status codes. The PCIe Transport adds where the SQE resides in host memory, where the doorbell resides in BAR0/1 memory space, and how a completion can trigger MSI-X.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>MSI-X</dt><dd>MSI-X, an extended message-signaled-interrupt mechanism with more vectors, per-vector masking, and a table.</dd></div><div><dt>MSI</dt><dd>Message Signaled Interrupt, a PCI mechanism that delivers an interrupt through a memory-write message.</dd></div><div><dt>SQE</dt><dd>Submission Queue Entry, one command structure in an SQ.</dd></div><div><dt>CA</dt><dd>Commit Action, the Firmware Commit field selecting replacement, activation, and reset policy.</dd></div><div><dt>FS</dt><dd>Firmware Slot, the Firmware Commit field selecting the target slot.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:PCIE14-FIG-001 -->
<details class="field-note" id="figure-PCIE14-FIG-001"><summary>PCIe Figure 1 · NVMe Family of Specifications</summary>
<!-- claim:PCIE14-FIG-001-CLAIM -->
<p>Figure 1, "NVMe Family of Specifications": Places NVMe Family of Specifications in the NVMe document and command-set hierarchy.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §1.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, Figure 1, printed pages 6, PDF pages 6</p></details>

</details>
<!-- figure-table:PCIE14-FIG-002 -->
<details class="field-note" id="figure-PCIE14-FIG-002"><summary>PCIe Figure 2 · Example of Transport Protocol Layers</summary>
<!-- claim:PCIE14-FIG-002-CLAIM -->
<p>Figure 2, "Example of Transport Protocol Layers": Separates the responsibilities of the protocol layers in Example of Transport Protocol Layers.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, Figure 2, printed pages 8, PDF pages 8</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-mmio-doorbell"><h2 id="heading-mmio-doorbell"><span class="section-number">02</span> BARs, MMIO, and doorbell addresses</h2>
<p>NVMe controller registers reside in the memory space designated by BAR0/BAR1. Doorbells begin at 1000h; SQ-tail and CQ-head registers for queue y are spaced using CAP.DSTRD. Figures 3-6 form one address derivation rather than four independent register tables.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>DSTRD</dt><dd>Doorbell Stride, the CAP field determining spacing between adjacent doorbell registers.</dd></div><div><dt>CAP</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities.</dd></div><div><dt>CQ</dt><dd>Completion Queue, the queue into which a controller posts command completions.</dd></div><div><dt>SQ</dt><dd>Submission Queue, the queue into which the host places commands.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:PCIE14-MMIO -->
<p>NVMe controller registers reside in memory space identified by BAR0/BAR1. The host shall use native-width or aligned 32-bit accesses and shall not issue locked accesses; violation produces undefined behavior.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, printed pages 9-10, PDF pages 9-10</p></details>
<!-- claim:PCIE14-DOORBELL -->
<p>SQ-tail and CQ-head doorbells begin at offset 1000h, with stride determined by CAP.DSTRD; queue identifier y participates in the offset calculation.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.1.2.1-3.1.2.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, printed pages 10-11, PDF pages 10-11</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>SQ y tail</td><td>1000h + (2y) x (4 &lt;&lt; DSTRD)</td><td>Host publishes a new SQ tail</td></tr><tr><td>CQ y head</td><td>1000h + (2y+1) x (4 &lt;&lt; DSTRD)</td><td>Host publishes a consumed CQ head</td></tr><tr><td>Doorbell value</td><td>Queue pointer</td><td>Does not contain the SQE or CQE body</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p>Informative example: with DSTRD=1, stride=4&lt;&lt;1=8 bytes. SQ-tail offset for queue 3 is 1000h+(6x8)=1030h; CQ-head offset is 1000h+(7x8)=1038h. They differ by one stride. Treating DSTRD itself as a byte count makes every nonzero-DSTRD doorbell address wrong.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:PCIE14-FIG-003 -->
<details class="field-note" id="figure-PCIE14-FIG-003"><summary>PCIe Figure 3 · PCI Express Registers</summary>
<!-- claim:PCIE14-FIG-003-CLAIM -->
<p>Figure 3, "PCI Express Registers": Defines the concrete layout or value relationships for PCI Express Registers.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, Figure 3, printed pages 9, PDF pages 9</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>MSIXCAP</dt><dd>MSI-X Capability, the base of the MSI-X capability structure.</dd></div><div><dt>AERCAP</dt><dd>Advanced Error Reporting Capability, the base of the AER extended-capability structure.</dd></div><div><dt>MSICAP</dt><dd>MSI Capability, the base of the MSI capability structure.</dd></div><div><dt>PMCAP</dt><dd>Power Management Capability, the base of the PCI power-management capability structure.</dd></div><div><dt>PXCAP</dt><dd>PCI Express Capability, the base of the PCIe capability structure.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-004 -->
<details class="field-note" id="figure-PCIE14-FIG-004"><summary>PCIe Figure 4 · PCI Express Specific Controller Property Definitions</summary>
<!-- claim:PCIE14-FIG-004-CLAIM -->
<p>Figure 4, "PCI Express Specific Controller Property Definitions": Defines the concrete layout or value relationships for PCI Express Specific Controller Property Definitions.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, Figure 4, printed pages 9-10, PDF pages 9-10</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CAP.DSTRD</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.DSTRD selects its DSTRD member field.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-005 -->
<details class="field-note" id="figure-PCIE14-FIG-005"><summary>PCIe Figure 5 · Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL - Submission Queue y Tail</summary>
<!-- claim:PCIE14-FIG-005-CLAIM -->
<p>Figure 5, "Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL - Submission Queue y Tail": Shows the queue or command relationship expressed by Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL - Submission Queue y Tail.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SQyTDBL</dt><dd>Submission Queue y Tail Doorbell, the MMIO register through which the host publishes the new tail of SQ y.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.1.2.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1, Figure 5, printed pages 10, PDF pages 10</p></details>

</details>
<!-- figure-table:PCIE14-FIG-006 -->
<details class="field-note" id="figure-PCIE14-FIG-006"><summary>PCIe Figure 6 · Offset (1000h + ((2y + 1) * (4 &lt;&lt; CAP.DSTRD))): CQyHDBL - Completion Queue y Head</summary>
<!-- claim:PCIE14-FIG-006-CLAIM -->
<p>Figure 6, "Offset (1000h + ((2y + 1) * (4 &lt;&lt; CAP.DSTRD))): CQyHDBL - Completion Queue y Head": Shows the queue or command relationship expressed by Offset (1000h + ((2y + 1) * (4 &lt;&lt; CAP.DSTRD))): CQyHDBL - Completion Queue y Head.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CQyHDBL</dt><dd>Completion Queue y Head Doorbell, the MMIO register through which the host publishes the consumed head of CQ y.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.1.2.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1, Figure 6, printed pages 10-11, PDF pages 10-11</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CC.PI</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.PI selects its PI member field.</dd></div><div><dt>CC</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller.</dd></div><div><dt>PI</dt><dd>Protection Information: Guard and tag fields used to check data and its associated information.</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-command"><h2 id="heading-command"><span class="section-number">03</span> Command exchange between host and controller</h2>
<p>SQE creation, doorbell write, controller fetch, CQE posting, interrupt delivery, and CQ-head update are not names for one event; they are successive ownership handoffs between host and controller. Their order governs both memory ordering and resource reuse.</p>
<figure><figcaption><strong>One command round trip</strong></figcaption><ol class="flow-steps"><li>The host writes a command to the Submission Queue (SQ).</li><li>The host updates the SQ Tail Doorbell to announce new work.</li><li>The controller retrieves and executes the command, then writes its result to the Completion Queue (CQ).</li><li>The host reads the CQE and updates the CQ Head Doorbell to release consumed entries.</li></ol><figcaption>Queues hold commands and results; doorbells announce updated queue positions.</figcaption></figure>

<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:PCIE14-COMMAND -->
<p>The command flow writes an SQE, updates the SQ-tail doorbell, lets the controller fetch and execute, posts a CQE, optionally interrupts, processes the CQE, and updates the CQ-head doorbell. A doorbell conveys a pointer, not the command body.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.4</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, printed pages 12-13, PDF pages 12-13</p></details>
<!-- claim:PCIE14-QUEUE -->
<p>PCIe permits multiple Submission Queues to share a Completion Queue. If interrupts are enabled when creating the CQ, Interrupt Vector shall be initialized to the corresponding MSI-X or multiple-message MSI vector.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, printed pages 11, PDF pages 11</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>SQ-slot reuse</td><td>Controller has consumed the SQE</td><td>Completion SQHD assists tracking</td></tr><tr><td>Command-buffer reuse</td><td>Command completed and data is visible</td><td>Check command and data direction</td></tr><tr><td>CQ-slot release</td><td>Host completely consumed the CQE</td><td>Then write the CQ-head doorbell</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p>Informative example: if the host rings the doorbell before writing the final SQE dword, the controller may fetch a partial command. In the other direction, updating CQ head before fully reading the CQE can let the controller reuse that CQ slot. Both are ownership-ordering failures, not opcode failures.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Double word: 32 bits, or 4 bytes.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:PCIE14-FIG-007 -->
<details class="field-note" id="figure-PCIE14-FIG-007"><summary>PCIe Figure 7 · Create I/O Completion Queue - Command Dword 11</summary>
<!-- claim:PCIE14-FIG-007-CLAIM -->
<p>Figure 7, "Create I/O Completion Queue - Command Dword 11": Defines command-specific fields in CDW11 for Create I/O Completion Queue.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CDW</dt><dd>Command Dword: a 32-bit unit in a command, followed by its index.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, Figure 7, printed pages 11, PDF pages 11</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>MSIXCAP.MXC.TS</dt><dd>MSI-X Capability, the base of the MSI-X capability structure. Here MSIXCAP.MXC.TS selects its MXC.TS member field.</dd></div><div><dt>MSICAP.MC.MME</dt><dd>MSI Capability, the base of the MSI capability structure. Here MSICAP.MC.MME selects its MC.MME member field.</dd></div><div><dt>MSIXCAP</dt><dd>MSI-X Capability, the base of the MSI-X capability structure.</dd></div><div><dt>MSICAP</dt><dd>MSI Capability, the base of the MSI capability structure.</dd></div><div><dt>IV</dt><dd>Interrupt Vector, the vector number assigned to a Completion Queue.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-008 -->
<details class="field-note" id="figure-PCIE14-FIG-008"><summary>PCIe Figure 8 · Command Processing</summary>
<!-- claim:PCIE14-FIG-008-CLAIM -->
<p>Figure 8, "Command Processing": Shows the queue or command relationship expressed by Command Processing.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.4.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4.1, Figure 8, printed pages 13, PDF pages 13</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-interrupts"><h2 id="heading-interrupts"><span class="section-number">04</span> Interrupt modes and notification behavior</h2>
<p>Pin-based, single-message MSI, multiple-message MSI, and MSI-X differ in more than performance. They provide different vector counts, masking locations, and capability structures; interrupt coalescing separately controls when multiple completions produce a notification. Figure 9 and Figures 34-46 belong with queue-to-vector mapping.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:PCIE14-INTERRUPT -->
<p>Modes are pin-based, single-message MSI, multiple-message MSI, and MSI-X. The specification recommends MSI-X. Coalescing can reduce interrupt rate at the cost of latency, and Admin-CQ interrupts should not be delayed.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.5</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, printed pages 13-16, PDF pages 13-16</p></details>
<!-- claim:PCIE14-HOST -->
<p>Annex A is an informative host checklist: write the SQE before its doorbell, use phase to identify a new CQE, advance CQ head after consumption, and service every relevant CQ associated with an interrupt vector.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §Annex A</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, printed pages 47-48, PDF pages 47-48</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Pin-based</td><td>Legacy shared signaling</td><td>Sharing and masking differ</td></tr><tr><td>Single MSI</td><td>One message/vector</td><td>Multiple CQs may share a service path</td></tr><tr><td>Multiple MSI</td><td>A set of contiguous messages</td><td>Constrained by MME/MMC capability</td></tr><tr><td>MSI-X</td><td>Table-based vectors with independent masks</td><td>Preferred by the specification</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p>Informative example: CQ 1 and CQ 2 share vector 5. When vector 5 arrives, the handler cannot inspect only CQ 1; it services every relevant CQ mapped to the vector. Raising the coalescing threshold can reduce interrupt rate while increasing CQE wait time.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:PCIE14-FIG-009 -->
<details class="field-note" id="figure-PCIE14-FIG-009"><summary>PCIe Figure 9 · Pin Based, Single MSI, and Multiple MSI Behavior</summary>
<!-- claim:PCIE14-FIG-009-CLAIM -->
<p>Figure 9, "Pin Based, Single MSI, and Multiple MSI Behavior": Shows the interrupt delivery or masking relationship represented by Pin Based, Single MSI, and Multiple MSI Behavior.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.5.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5.1, Figure 9, printed pages 15, PDF pages 15</p></details>

</details>
<!-- figure-table:PCIE14-FIG-034 -->
<details class="field-note" id="figure-PCIE14-FIG-034"><summary>PCIe Figure 34 · Message Signaled Interrupt Capability (Optional)</summary>
<!-- claim:PCIE14-FIG-034-CLAIM -->
<p>Figure 34, "Message Signaled Interrupt Capability (Optional)": Defines the concrete layout or value relationships for Message Signaled Interrupt Capability (Optional).</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.2.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.3, Figure 34, printed pages 22, PDF pages 22</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>MSICAP</dt><dd>MSI Capability, the base of the MSI capability structure.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-035 -->
<details class="field-note" id="figure-PCIE14-FIG-035"><summary>PCIe Figure 35 · Offset MSICAP: MID - Message Signaled Interrupt Identifiers</summary>
<!-- claim:PCIE14-FIG-035-CLAIM -->
<p>Figure 35, "Offset MSICAP: MID - Message Signaled Interrupt Identifiers": Defines MID (Message Signaled Interrupt Identifiers) at offset MSICAP and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.3.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.1, Figure 35, printed pages 23, PDF pages 23</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CID</dt><dd>Command Identifier, used with the SQ identifier to identify an outstanding command.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-036 -->
<details class="field-note" id="figure-PCIE14-FIG-036"><summary>PCIe Figure 36 · Offset MSICAP + 2h: MC - Message Signaled Interrupt Message Control</summary>
<!-- claim:PCIE14-FIG-036-CLAIM -->
<p>Figure 36, "Offset MSICAP + 2h: MC - Message Signaled Interrupt Message Control": Defines MC (Message Signaled Interrupt Message Control) at offset MSICAP + 2h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.3.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.2, Figure 36, printed pages 23, PDF pages 23</p></details>

</details>
<!-- figure-table:PCIE14-FIG-037 -->
<details class="field-note" id="figure-PCIE14-FIG-037"><summary>PCIe Figure 37 · Offset MSICAP + 4h: MA - Message Signaled Interrupt Message Address</summary>
<!-- claim:PCIE14-FIG-037-CLAIM -->
<p>Figure 37, "Offset MSICAP + 4h: MA - Message Signaled Interrupt Message Address": Defines MA (Message Signaled Interrupt Message Address) at offset MSICAP + 4h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.3.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.3, Figure 37, printed pages 23, PDF pages 23</p></details>

</details>
<!-- figure-table:PCIE14-FIG-038 -->
<details class="field-note" id="figure-PCIE14-FIG-038"><summary>PCIe Figure 38 · Offset MSICAP + 8h: MUA - Message Signaled Interrupt Upper Address</summary>
<!-- claim:PCIE14-FIG-038-CLAIM -->
<p>Figure 38, "Offset MSICAP + 8h: MUA - Message Signaled Interrupt Upper Address": Defines MUA (Message Signaled Interrupt Upper Address) at offset MSICAP + 8h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.3.4</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.4, Figure 38, printed pages 23, PDF pages 23</p></details>

</details>
<!-- figure-table:PCIE14-FIG-039 -->
<details class="field-note" id="figure-PCIE14-FIG-039"><summary>PCIe Figure 39 · Offset MSICAP + Ch: MD - Message Signaled Interrupt Message Data</summary>
<!-- claim:PCIE14-FIG-039-CLAIM -->
<p>Figure 39, "Offset MSICAP + Ch: MD - Message Signaled Interrupt Message Data": Defines MD (Message Signaled Interrupt Message Data) at offset MSICAP + Ch and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.3.5</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.5, Figure 39, printed pages 23, PDF pages 23</p></details>

</details>
<!-- figure-table:PCIE14-FIG-040 -->
<details class="field-note" id="figure-PCIE14-FIG-040"><summary>PCIe Figure 40 · Offset MSICAP + 10h: MMASK - Message Signaled Interrupt Mask Bits (Optional)</summary>
<!-- claim:PCIE14-FIG-040-CLAIM -->
<p>Figure 40, "Offset MSICAP + 10h: MMASK - Message Signaled Interrupt Mask Bits (Optional)": Defines MMASK (Message Signaled Interrupt Mask Bits (Optional)) at offset MSICAP + 10h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.3.6</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.6, Figure 40, printed pages 24, PDF pages 24</p></details>

</details>
<!-- figure-table:PCIE14-FIG-041 -->
<details class="field-note" id="figure-PCIE14-FIG-041"><summary>PCIe Figure 41 · Offset MSICAP + 14h: MPEND - Message Signaled Interrupt Pending Bits (Optional)</summary>
<!-- claim:PCIE14-FIG-041-CLAIM -->
<p>Figure 41, "Offset MSICAP + 14h: MPEND - Message Signaled Interrupt Pending Bits (Optional)": Defines MPEND (Message Signaled Interrupt Pending Bits (Optional)) at offset MSICAP + 14h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.3.7</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.7, Figure 41, printed pages 24, PDF pages 24</p></details>

</details>
<!-- figure-table:PCIE14-FIG-042 -->
<details class="field-note" id="figure-PCIE14-FIG-042"><summary>PCIe Figure 42 · MSI-X Capability (Optional)</summary>
<!-- claim:PCIE14-FIG-042-CLAIM -->
<p>Figure 42, "MSI-X Capability (Optional)": Defines the concrete layout or value relationships for MSI-X Capability (Optional).</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.3.7</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.7, Figure 42, printed pages 24, PDF pages 24</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>MSIXCAP</dt><dd>MSI-X Capability, the base of the MSI-X capability structure.</dd></div><div><dt>BIR</dt><dd>BAR Indicator Register, a selector identifying the PCIe BAR that contains a memory structure.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-043 -->
<details class="field-note" id="figure-PCIE14-FIG-043"><summary>PCIe Figure 43 · Offset MSIXCAP: MXID - MSI-X Identifiers</summary>
<!-- claim:PCIE14-FIG-043-CLAIM -->
<p>Figure 43, "Offset MSIXCAP: MXID - MSI-X Identifiers": Defines MXID (MSI-X Identifiers) at offset MSIXCAP and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.4.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.1, Figure 43, printed pages 24, PDF pages 24</p></details>

</details>
<!-- figure-table:PCIE14-FIG-044 -->
<details class="field-note" id="figure-PCIE14-FIG-044"><summary>PCIe Figure 44 · Offset MSIXCAP + 2h: MXC - MSI-X Message Control</summary>
<!-- claim:PCIE14-FIG-044-CLAIM -->
<p>Figure 44, "Offset MSIXCAP + 2h: MXC - MSI-X Message Control": Defines MXC (MSI-X Message Control) at offset MSIXCAP + 2h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.4.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.2, Figure 44, printed pages 24-25, PDF pages 24-25</p></details>

</details>
<!-- figure-table:PCIE14-FIG-045 -->
<details class="field-note" id="figure-PCIE14-FIG-045"><summary>PCIe Figure 45 · Offset MSIXCAP + 4h: MTAB - MSI-X Table Offset / Table BIR</summary>
<!-- claim:PCIE14-FIG-045-CLAIM -->
<p>Figure 45, "Offset MSIXCAP + 4h: MTAB - MSI-X Table Offset / Table BIR": Defines MTAB (MSI-X Table Offset / Table BIR) at offset MSIXCAP + 4h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.4.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.3, Figure 45, printed pages 25, PDF pages 25</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>BAR</dt><dd>Base Address Register, a PCI-configuration-space register finding a device memory space.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-046 -->
<details class="field-note" id="figure-PCIE14-FIG-046"><summary>PCIe Figure 46 · Offset MSIXCAP + 8h: MPBA - MSI-X PBA Offset / PBA BIR</summary>
<!-- claim:PCIE14-FIG-046-CLAIM -->
<p>Figure 46, "Offset MSIXCAP + 8h: MPBA - MSI-X PBA Offset / PBA BIR": Defines MPBA (MSI-X PBA Offset / PBA BIR) at offset MSIXCAP + 8h and identifies the fields that software must read the fields at that location.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PBA</dt><dd>Pending Bit Array, the MSI-X bit array recording vectors that are pending service.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.4.4</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.4, Figure 46, printed pages 25, PDF pages 25</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>PBAO</dt><dd>Page Base Address and Offset, the first-PRP layout combining a page base address with an in-page offset.</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-config-error"><h2 id="heading-config-error"><span class="section-number">05</span> Configuration space and PCIe error reporting</h2>
<p>Figures 10-67 traverse the Type 0 header, Power Management, MSI/MSI-X, PCIe capability, and AER. Find the capability or extended-capability base before applying offsets. AER status, mask, severity, and header log form one diagnostic set rather than isolated error bits.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>AER</dt><dd>Advanced Error Reporting, the PCIe capability for classifying, masking, and logging link or transaction errors.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:PCIE14-CONFIG -->
<p>Section 3.8 defines additional NVMe-controller requirements for the PCI header, Power Management, MSI/MSI-X, PCIe capability, and AER. Original PCI/PCIe field semantics remain governed by PCI-SIG specifications.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1-3.8.7</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, printed pages 16-35, PDF pages 16-35</p></details>
<!-- claim:PCIE14-ERROR -->
<p>NVMe command errors are reported in CQE status, while PCIe transport or link errors use PCIe mechanisms plus this document’s NVMe-specific requirements. Their recovery scopes differ.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.7</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, printed pages 16, PDF pages 16</p></details>
<!-- claim:PCIE14-POWER -->
<p>The host shall never select an NVMe power state whose consumption exceeds the PCIe slot power limit; violation results in undefined power behavior.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.6</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.6, printed pages 16, PDF pages 16</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>NVMe CQE status</td><td>Command execution result</td><td>Read the fields in NVMe command context</td></tr><tr><td>PCIe Device Status</td><td>PCIe Function status summary</td><td>Found in PCIe capability</td></tr><tr><td>AER</td><td>Correctable/uncorrectable transport errors</td><td>Read status, mask, severity, and header together</td></tr><tr><td>Power state</td><td>Slot limit and device power control</td><td>Never choose an NVMe state above the slot power limit</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p>Informative example: when an AERUCES bit is set, first check its mask to determine reporting, then its severity for handling, and finally the header log for transaction context. The bit cannot be translated directly into an NVMe SC.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SC</dt><dd>Status Code: identifies the completion result within the selected SCT category.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:PCIE14-FIG-010 -->
<details class="field-note" id="figure-PCIE14-FIG-010"><summary>PCIe Figure 10 · PCI Express Type 0/1 Common Configuration Space</summary>
<!-- claim:PCIE14-FIG-010-CLAIM -->
<p>Figure 10, "PCI Express Type 0/1 Common Configuration Space": Defines the concrete layout or value relationships for PCI Express Type 0/1 Common Configuration Space.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8, Figure 10, printed pages 16-17, PDF pages 16-17</p></details>

</details>
<!-- figure-table:PCIE14-FIG-011 -->
<details class="field-note" id="figure-PCIE14-FIG-011"><summary>PCIe Figure 11 · Offset 00h: ID - Identifiers</summary>
<!-- claim:PCIE14-FIG-011-CLAIM -->
<p>Figure 11, "Offset 00h: ID - Identifiers": Defines ID (Identifiers) at offset 00h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.1, Figure 11, printed pages 17, PDF pages 17</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>DID</dt><dd>Domain Identifier, the identifier of a domain within an NVM subsystem.</dd></div><div><dt>VID</dt><dd>Vendor ID, a PCI-SIG-assigned identifier for a vendor.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-012 -->
<details class="field-note" id="figure-PCIE14-FIG-012"><summary>PCIe Figure 12 · Offset 04h: CMD - Command</summary>
<!-- claim:PCIE14-FIG-012-CLAIM -->
<p>Figure 12, "Offset 04h: CMD - Command": Defines CMD (Command) at offset 04h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.2, Figure 12, printed pages 17, PDF pages 17</p></details>

</details>
<!-- figure-table:PCIE14-FIG-013 -->
<details class="field-note" id="figure-PCIE14-FIG-013"><summary>PCIe Figure 13 · Offset 06h: STS - Device Status</summary>
<!-- claim:PCIE14-FIG-013-CLAIM -->
<p>Figure 13, "Offset 06h: STS - Device Status": Defines STS (Device Status) at offset 06h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.3, Figure 13, printed pages 18, PDF pages 18</p></details>

</details>
<!-- figure-table:PCIE14-FIG-014 -->
<details class="field-note" id="figure-PCIE14-FIG-014"><summary>PCIe Figure 14 · Offset 08h: RID - Revision ID</summary>
<!-- claim:PCIE14-FIG-014-CLAIM -->
<p>Figure 14, "Offset 08h: RID - Revision ID": Defines RID (Revision ID) at offset 08h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.4</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.4, Figure 14, printed pages 18, PDF pages 18</p></details>

</details>
<!-- figure-table:PCIE14-FIG-015 -->
<details class="field-note" id="figure-PCIE14-FIG-015"><summary>PCIe Figure 15 · Offset 09h: CC - Class Code</summary>
<!-- claim:PCIE14-FIG-015-CLAIM -->
<p>Figure 15, "Offset 09h: CC - Class Code": Defines CC (Class Code) at offset 09h and identifies the fields that software must read the fields at that location.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CC</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.5</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.5, Figure 15, printed pages 18, PDF pages 18</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>PI</dt><dd>Protection Information: Guard and tag fields used to check data and its associated information.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-016 -->
<details class="field-note" id="figure-PCIE14-FIG-016"><summary>PCIe Figure 16 · Offset 0Ch: CLS - Cache Line Size</summary>
<!-- claim:PCIE14-FIG-016-CLAIM -->
<p>Figure 16, "Offset 0Ch: CLS - Cache Line Size": Defines CLS (Cache Line Size) at offset 0Ch and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.6</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.6, Figure 16, printed pages 18, PDF pages 18</p></details>

</details>
<!-- figure-table:PCIE14-FIG-017 -->
<details class="field-note" id="figure-PCIE14-FIG-017"><summary>PCIe Figure 17 · Offset 0Dh: MLT - Master Latency Timer</summary>
<!-- claim:PCIE14-FIG-017-CLAIM -->
<p>Figure 17, "Offset 0Dh: MLT - Master Latency Timer": Defines MLT (Master Latency Timer) at offset 0Dh and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.7</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.7, Figure 17, printed pages 18, PDF pages 18</p></details>

</details>
<!-- figure-table:PCIE14-FIG-018 -->
<details class="field-note" id="figure-PCIE14-FIG-018"><summary>PCIe Figure 18 · Offset 0Eh: HTYPE - Header Type</summary>
<!-- claim:PCIE14-FIG-018-CLAIM -->
<p>Figure 18, "Offset 0Eh: HTYPE - Header Type": Defines HTYPE (Header Type) at offset 0Eh and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.8</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.8, Figure 18, printed pages 19, PDF pages 19</p></details>

</details>
<!-- figure-table:PCIE14-FIG-019 -->
<details class="field-note" id="figure-PCIE14-FIG-019"><summary>PCIe Figure 19 · Offset 0Fh: BIST - Built-In Self Test (Optional)</summary>
<!-- claim:PCIE14-FIG-019-CLAIM -->
<p>Figure 19, "Offset 0Fh: BIST - Built-In Self Test (Optional)": Defines BIST (Built-In Self Test (Optional)) at offset 0Fh and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.9</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.9, Figure 19, printed pages 19, PDF pages 19</p></details>

</details>
<!-- figure-table:PCIE14-FIG-020 -->
<details class="field-note" id="figure-PCIE14-FIG-020"><summary>PCIe Figure 20 · Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits</summary>
<!-- claim:PCIE14-FIG-020-CLAIM -->
<p>Figure 20, "Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits": Defines the concrete layout or value relationships for Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.10</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.10, Figure 20, printed pages 19, PDF pages 19</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>PF</dt><dd>Physical Function, a full-featured PCIe function that can manage associated VFs.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-021 -->
<details class="field-note" id="figure-PCIE14-FIG-021"><summary>PCIe Figure 21 · Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits</summary>
<!-- claim:PCIE14-FIG-021-CLAIM -->
<p>Figure 21, "Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits": Defines the concrete layout or value relationships for Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.11</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.11, Figure 21, printed pages 19, PDF pages 19</p></details>

</details>
<!-- figure-table:PCIE14-FIG-022 -->
<details class="field-note" id="figure-PCIE14-FIG-022"><summary>PCIe Figure 22 · Offset 18h: BAR2 - Index/Data Pair Register Base Address or Vendor Specific</summary>
<!-- claim:PCIE14-FIG-022-CLAIM -->
<p>Figure 22, "Offset 18h: BAR2 - Index/Data Pair Register Base Address or Vendor Specific": Defines BAR2 (Index/Data Pair Register Base Address or Vendor Specific) at offset 18h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.12</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.12, Figure 22, printed pages 20, PDF pages 20</p></details>

</details>
<!-- figure-table:PCIE14-FIG-023 -->
<details class="field-note" id="figure-PCIE14-FIG-023"><summary>PCIe Figure 23 · Offset 28h: CCPTR - CardBus CIS Pointer</summary>
<!-- claim:PCIE14-FIG-023-CLAIM -->
<p>Figure 23, "Offset 28h: CCPTR - CardBus CIS Pointer": Defines CCPTR (CardBus CIS Pointer) at offset 28h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.16</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.16, Figure 23, printed pages 20, PDF pages 20</p></details>

</details>
<!-- figure-table:PCIE14-FIG-024 -->
<details class="field-note" id="figure-PCIE14-FIG-024"><summary>PCIe Figure 24 · Offset 2Ch: SS - Subsystem Identifiers</summary>
<!-- claim:PCIE14-FIG-024-CLAIM -->
<p>Figure 24, "Offset 2Ch: SS - Subsystem Identifiers": Defines SS (Subsystem Identifiers) at offset 2Ch and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.17</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.17, Figure 24, printed pages 20, PDF pages 20</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>SSVID</dt><dd>Subsystem Vendor ID, the PCI identifier for a subsystem vendor.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-025 -->
<details class="field-note" id="figure-PCIE14-FIG-025"><summary>PCIe Figure 25 · Offset 30h: EROM - Expansion ROM (Optional)</summary>
<!-- claim:PCIE14-FIG-025-CLAIM -->
<p>Figure 25, "Offset 30h: EROM - Expansion ROM (Optional)": Defines EROM (Expansion ROM (Optional)) at offset 30h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.18</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.18, Figure 25, printed pages 20, PDF pages 20</p></details>

</details>
<!-- figure-table:PCIE14-FIG-026 -->
<details class="field-note" id="figure-PCIE14-FIG-026"><summary>PCIe Figure 26 · Offset 34h: CAP - Capabilities Pointer</summary>
<!-- claim:PCIE14-FIG-026-CLAIM -->
<p>Figure 26, "Offset 34h: CAP - Capabilities Pointer": Defines CAP (Capabilities Pointer) at offset 34h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.19</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.19, Figure 26, printed pages 21, PDF pages 21</p></details>

</details>
<!-- figure-table:PCIE14-FIG-027 -->
<details class="field-note" id="figure-PCIE14-FIG-027"><summary>PCIe Figure 27 · Offset 3Ch: INTR - Interrupt Information</summary>
<!-- claim:PCIE14-FIG-027-CLAIM -->
<p>Figure 27, "Offset 3Ch: INTR - Interrupt Information": Defines INTR (Interrupt Information) at offset 3Ch and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.20</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.20, Figure 27, printed pages 21, PDF pages 21</p></details>

</details>
<!-- figure-table:PCIE14-FIG-028 -->
<details class="field-note" id="figure-PCIE14-FIG-028"><summary>PCIe Figure 28 · Offset 3Eh: MGNT - Minimum Grant</summary>
<!-- claim:PCIE14-FIG-028-CLAIM -->
<p>Figure 28, "Offset 3Eh: MGNT - Minimum Grant": Defines MGNT (Minimum Grant) at offset 3Eh and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.21</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.21, Figure 28, printed pages 21, PDF pages 21</p></details>

</details>
<!-- figure-table:PCIE14-FIG-029 -->
<details class="field-note" id="figure-PCIE14-FIG-029"><summary>PCIe Figure 29 · Offset 3Fh: MLAT - Maximum Latency</summary>
<!-- claim:PCIE14-FIG-029-CLAIM -->
<p>Figure 29, "Offset 3Fh: MLAT - Maximum Latency": Defines MLAT (Maximum Latency) at offset 3Fh and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.22</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.22, Figure 29, printed pages 21, PDF pages 21</p></details>

</details>
<!-- figure-table:PCIE14-FIG-030 -->
<details class="field-note" id="figure-PCIE14-FIG-030"><summary>PCIe Figure 30 · PCI Power Management Capabilities</summary>
<!-- claim:PCIE14-FIG-030-CLAIM -->
<p>Figure 30, "PCI Power Management Capabilities": Defines the concrete layout or value relationships for PCI Power Management Capabilities.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.22</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.22, Figure 30, printed pages 21, PDF pages 21</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>PMCAP</dt><dd>Power Management Capability, the base of the PCI power-management capability structure.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-031 -->
<details class="field-note" id="figure-PCIE14-FIG-031"><summary>PCIe Figure 31 · Offset PMCAP: PID - PCI Power Management Capability ID</summary>
<!-- claim:PCIE14-FIG-031-CLAIM -->
<p>Figure 31, "Offset PMCAP: PID - PCI Power Management Capability ID": Defines PID (PCI Power Management Capability ID) at offset PMCAP and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.2.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.1, Figure 31, printed pages 21, PDF pages 21</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CID</dt><dd>Command Identifier, used with the SQ identifier to identify an outstanding command.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-032 -->
<details class="field-note" id="figure-PCIE14-FIG-032"><summary>PCIe Figure 32 · Offset PMCAP + 2h: PC - PCI Power Management Capabilities</summary>
<!-- claim:PCIE14-FIG-032-CLAIM -->
<p>Figure 32, "Offset PMCAP + 2h: PC - PCI Power Management Capabilities": Defines PC (PCI Power Management Capabilities) at offset PMCAP + 2h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.2.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.2, Figure 32, printed pages 22, PDF pages 22</p></details>

</details>
<!-- figure-table:PCIE14-FIG-033 -->
<details class="field-note" id="figure-PCIE14-FIG-033"><summary>PCIe Figure 33 · Offset PMCAP + 4h: PMCS - PCI Power Management Control and Status</summary>
<!-- claim:PCIE14-FIG-033-CLAIM -->
<p>Figure 33, "Offset PMCAP + 4h: PMCS - PCI Power Management Control and Status": Defines PMCS (PCI Power Management Control and Status) at offset PMCAP + 4h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.2.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.3, Figure 33, printed pages 22, PDF pages 22</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>PS</dt><dd>Power State, a controller power/performance operating point; PS0 has the highest maximum power.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-047 -->
<details class="field-note" id="figure-PCIE14-FIG-047"><summary>PCIe Figure 47 · PCI Express Capability</summary>
<!-- claim:PCIE14-FIG-047-CLAIM -->
<p>Figure 47, "PCI Express Capability": Defines the concrete layout or value relationships for PCI Express Capability.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5, Figure 47, printed pages 26, PDF pages 26</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>PXCAP</dt><dd>PCI Express Capability, the base of the PCIe capability structure.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-048 -->
<details class="field-note" id="figure-PCIE14-FIG-048"><summary>PCIe Figure 48 · Offset PXCAP: PXID - PCI Express Capability ID</summary>
<!-- claim:PCIE14-FIG-048-CLAIM -->
<p>Figure 48, "Offset PXCAP: PXID - PCI Express Capability ID": Defines PXID (PCI Express Capability ID) at offset PXCAP and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.1, Figure 48, printed pages 26, PDF pages 26</p></details>

</details>
<!-- figure-table:PCIE14-FIG-049 -->
<details class="field-note" id="figure-PCIE14-FIG-049"><summary>PCIe Figure 49 · Offset PXCAP + 2h: PXCAP - PCI Express Capabilities</summary>
<!-- claim:PCIE14-FIG-049-CLAIM -->
<p>Figure 49, "Offset PXCAP + 2h: PXCAP - PCI Express Capabilities": Defines PXCAP (PCI Express Capabilities) at offset PXCAP + 2h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.2, Figure 49, printed pages 26, PDF pages 26</p></details>

</details>
<!-- figure-table:PCIE14-FIG-050 -->
<details class="field-note" id="figure-PCIE14-FIG-050"><summary>PCIe Figure 50 · Offset PXCAP + 4h: PXDCAP - PCI Express Device Capabilities</summary>
<!-- claim:PCIE14-FIG-050-CLAIM -->
<p>Figure 50, "Offset PXCAP + 4h: PXDCAP - PCI Express Device Capabilities": Defines PXDCAP (PCI Express Device Capabilities) at offset PXCAP + 4h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.3, Figure 50, printed pages 26-27, PDF pages 26-27</p></details>

</details>
<!-- figure-table:PCIE14-FIG-051 -->
<details class="field-note" id="figure-PCIE14-FIG-051"><summary>PCIe Figure 51 · Offset PXCAP + 8h: PXDC - PCI Express Device Control</summary>
<!-- claim:PCIE14-FIG-051-CLAIM -->
<p>Figure 51, "Offset PXCAP + 8h: PXDC - PCI Express Device Control": Defines PXDC (PCI Express Device Control) at offset PXCAP + 8h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.4</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.4, Figure 51, printed pages 27-28, PDF pages 27-28</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>MRRS</dt><dd>Max Read Request Size, the setting limiting the size of read requests issued by a PCIe Function.</dd></div><div><dt>MPS</dt><dd>Memory Page Size, the controller memory-page-size setting; it affects queue addresses and PRP alignment.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-052 -->
<details class="field-note" id="figure-PCIE14-FIG-052"><summary>PCIe Figure 52 · Offset PXCAP + Ah: PXDS - PCI Express Device Status</summary>
<!-- claim:PCIE14-FIG-052-CLAIM -->
<p>Figure 52, "Offset PXCAP + Ah: PXDS - PCI Express Device Status": Defines PXDS (PCI Express Device Status) at offset PXCAP + Ah and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.5</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.5, Figure 52, printed pages 28, PDF pages 28</p></details>

</details>
<!-- figure-table:PCIE14-FIG-053 -->
<details class="field-note" id="figure-PCIE14-FIG-053"><summary>PCIe Figure 53 · Offset PXCAP + Ch: PXLCAP - PCI Express Link Capabilities</summary>
<!-- claim:PCIE14-FIG-053-CLAIM -->
<p>Figure 53, "Offset PXCAP + Ch: PXLCAP - PCI Express Link Capabilities": Defines PXLCAP (PCI Express Link Capabilities) at offset PXCAP + Ch and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.6</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.6, Figure 53, printed pages 28-29, PDF pages 28-29</p></details>

</details>
<!-- figure-table:PCIE14-FIG-054 -->
<details class="field-note" id="figure-PCIE14-FIG-054"><summary>PCIe Figure 54 · Offset PXCAP + 10h: PXLC - PCI Express Link Control</summary>
<!-- claim:PCIE14-FIG-054-CLAIM -->
<p>Figure 54, "Offset PXCAP + 10h: PXLC - PCI Express Link Control": Defines PXLC (PCI Express Link Control) at offset PXCAP + 10h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.7</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.7, Figure 54, printed pages 29, PDF pages 29</p></details>

</details>
<!-- figure-table:PCIE14-FIG-055 -->
<details class="field-note" id="figure-PCIE14-FIG-055"><summary>PCIe Figure 55 · Offset PXCAP + 12h: PXLS - PCI Express Link Status</summary>
<!-- claim:PCIE14-FIG-055-CLAIM -->
<p>Figure 55, "Offset PXCAP + 12h: PXLS - PCI Express Link Status": Defines PXLS (PCI Express Link Status) at offset PXCAP + 12h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.8</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.8, Figure 55, printed pages 29, PDF pages 29</p></details>

</details>
<!-- figure-table:PCIE14-FIG-056 -->
<details class="field-note" id="figure-PCIE14-FIG-056"><summary>PCIe Figure 56 · Offset PXCAP + 24h: PXDCAP2 - PCI Express Device Capabilities 2</summary>
<!-- claim:PCIE14-FIG-056-CLAIM -->
<p>Figure 56, "Offset PXCAP + 24h: PXDCAP2 - PCI Express Device Capabilities 2": Defines PXDCAP2 (PCI Express Device Capabilities 2) at offset PXCAP + 24h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.9</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.9, Figure 56, printed pages 30, PDF pages 30</p></details>

</details>
<!-- figure-table:PCIE14-FIG-057 -->
<details class="field-note" id="figure-PCIE14-FIG-057"><summary>PCIe Figure 57 · Offset PXCAP + 28h: PXDC2 - PCI Express Device Control 2</summary>
<!-- claim:PCIE14-FIG-057-CLAIM -->
<p>Figure 57, "Offset PXCAP + 28h: PXDC2 - PCI Express Device Control 2": Defines PXDC2 (PCI Express Device Control 2) at offset PXCAP + 28h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.10</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.10, Figure 57, printed pages 30-31, PDF pages 30-31</p></details>

</details>
<!-- figure-table:PCIE14-FIG-058 -->
<details class="field-note" id="figure-PCIE14-FIG-058"><summary>PCIe Figure 58 · Advanced Error Reporting Capability (Optional)</summary>
<!-- claim:PCIE14-FIG-058-CLAIM -->
<p>Figure 58, "Advanced Error Reporting Capability (Optional)": Defines the status/error classification represented by Advanced Error Reporting Capability (Optional).</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.10</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.10, Figure 58, printed pages 31, PDF pages 31</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>AERCAP</dt><dd>Advanced Error Reporting Capability, the base of the AER extended-capability structure.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-059 -->
<details class="field-note" id="figure-PCIE14-FIG-059"><summary>PCIe Figure 59 · Offset AERCAP: AERID - AER Capability ID</summary>
<!-- claim:PCIE14-FIG-059-CLAIM -->
<p>Figure 59, "Offset AERCAP: AERID - AER Capability ID": Defines AERID (AER Capability ID) at offset AERCAP and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.6.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.1, Figure 59, printed pages 31, PDF pages 31</p></details>

</details>
<!-- figure-table:PCIE14-FIG-060 -->
<details class="field-note" id="figure-PCIE14-FIG-060"><summary>PCIe Figure 60 · Offset AERCAP + 4: AERUCES - AER Uncorrectable Error Status Register</summary>
<!-- claim:PCIE14-FIG-060-CLAIM -->
<p>Figure 60, "Offset AERCAP + 4: AERUCES - AER Uncorrectable Error Status Register": Defines AERUCES (AER Uncorrectable Error Status Register) at offset AERCAP + 4 and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.6.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.2, Figure 60, printed pages 31-32, PDF pages 31-32</p></details>

</details>
<!-- figure-table:PCIE14-FIG-061 -->
<details class="field-note" id="figure-PCIE14-FIG-061"><summary>PCIe Figure 61 · Offset AERCAP + 8: AERUCEM - AER Uncorrectable Error Mask Register</summary>
<!-- claim:PCIE14-FIG-061-CLAIM -->
<p>Figure 61, "Offset AERCAP + 8: AERUCEM - AER Uncorrectable Error Mask Register": Defines AERUCEM (AER Uncorrectable Error Mask Register) at offset AERCAP + 8 and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.6.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.3, Figure 61, printed pages 32, PDF pages 32</p></details>

</details>
<!-- figure-table:PCIE14-FIG-062 -->
<details class="field-note" id="figure-PCIE14-FIG-062"><summary>PCIe Figure 62 · Offset AERCAP + Ch: AERUCESEV - AER Uncorrectable Error Severity Register</summary>
<!-- claim:PCIE14-FIG-062-CLAIM -->
<p>Figure 62, "Offset AERCAP + Ch: AERUCESEV - AER Uncorrectable Error Severity Register": Defines AERUCESEV (AER Uncorrectable Error Severity Register) at offset AERCAP + Ch and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.6.4</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.4, Figure 62, printed pages 32-33, PDF pages 32-33</p></details>

</details>
<!-- figure-table:PCIE14-FIG-063 -->
<details class="field-note" id="figure-PCIE14-FIG-063"><summary>PCIe Figure 63 · Offset AERCAP + 10h: AERCES - AER Correctable Error Status Register</summary>
<!-- claim:PCIE14-FIG-063-CLAIM -->
<p>Figure 63, "Offset AERCAP + 10h: AERCES - AER Correctable Error Status Register": Defines AERCES (AER Correctable Error Status Register) at offset AERCAP + 10h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.6.5</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.5, Figure 63, printed pages 33, PDF pages 33</p></details>

</details>
<!-- figure-table:PCIE14-FIG-064 -->
<details class="field-note" id="figure-PCIE14-FIG-064"><summary>PCIe Figure 64 · Offset AERCAP + 14h: AERCEM - AER Correctable Error Mask Register</summary>
<!-- claim:PCIE14-FIG-064-CLAIM -->
<p>Figure 64, "Offset AERCAP + 14h: AERCEM - AER Correctable Error Mask Register": Defines AERCEM (AER Correctable Error Mask Register) at offset AERCAP + 14h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.6.6</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.6, Figure 64, printed pages 33, PDF pages 33</p></details>

</details>
<!-- figure-table:PCIE14-FIG-065 -->
<details class="field-note" id="figure-PCIE14-FIG-065"><summary>PCIe Figure 65 · Offset AERCAP + 18h: AERCC - AER Capabilities and Control Register</summary>
<!-- claim:PCIE14-FIG-065-CLAIM -->
<p>Figure 65, "Offset AERCAP + 18h: AERCC - AER Capabilities and Control Register": Defines AERCC (AER Capabilities and Control Register) at offset AERCAP + 18h and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.6.7</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.7, Figure 65, printed pages 34, PDF pages 34</p></details>

</details>
<!-- figure-table:PCIE14-FIG-066 -->
<details class="field-note" id="figure-PCIE14-FIG-066"><summary>PCIe Figure 66 · Offset AERCAP + 1Ch: AERHL - AER Header Log Register</summary>
<!-- claim:PCIE14-FIG-066-CLAIM -->
<p>Figure 66, "Offset AERCAP + 1Ch: AERHL - AER Header Log Register": Defines AERHL (AER Header Log Register) at offset AERCAP + 1Ch and identifies the fields that software must read the fields at that location.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.6.8</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.8, Figure 66, printed pages 34, PDF pages 34</p></details>

</details>
<!-- figure-table:PCIE14-FIG-067 -->
<details class="field-note" id="figure-PCIE14-FIG-067"><summary>PCIe Figure 67 · Offset AERCAP + 38h: AERTLP - AER TLP Prefix Log Register (Optional)</summary>
<!-- claim:PCIE14-FIG-067-CLAIM -->
<p>Figure 67, "Offset AERCAP + 38h: AERTLP - AER TLP Prefix Log Register (Optional)": Defines AERTLP (AER TLP Prefix Log Register (Optional)) at offset AERCAP + 38h and identifies the fields that software must read the fields at that location.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>TLP</dt><dd>Transaction Layer Packet, a packet carried by the PCIe transaction layer.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.6.9</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.9, Figure 67, printed pages 35, PDF pages 35</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-eom"><h2 id="heading-eom"><span class="section-number">06</span> Receiver eye-opening measurement data layout</h2>
<p>The receiver eye-opening measurement log has variable length. Its header describes the whole dataset, while lane descriptors describe individual lanes. Structure levels and length units identify which lane each measurement belongs to.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:PCIE14-EOM -->
<p>The Physical Interface Receiver Eye Opening Measurement log page reports measurements through a header, lane descriptors, and EOM data. The host checks support and size before parsing lanes and parameters.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>EOM</dt><dd>Eye Opening Measurement, the procedure and log data for measuring a PCIe receiver eye opening.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.9</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, printed pages 39-46, PDF pages 39-46</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Specific parameter</td><td>Selects measurement action and quality/state</td><td>Establish request context first</td></tr><tr><td>Specific identifier</td><td>Selects lane/test context</td><td>Prevents mixing different measurements</td></tr><tr><td>Header</td><td>Global length and layout</td><td>Base for every later offset</td></tr><tr><td>Lane descriptor</td><td>Per-lane boundaries and status</td><td>Walk only within returned buffer</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p>To compare two lanes, find each measurement through its lane descriptor and compare using the same measurement format. The header lane count describes structure, not measurement quality.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:PCIE14-FIG-070 -->
<details class="field-note" id="figure-PCIE14-FIG-070"><summary>PCIe Figure 70 · Get Log Page - Log Page Identifiers</summary>
<!-- claim:PCIE14-FIG-070-CLAIM -->
<p>Figure 70, "Get Log Page - Log Page Identifiers": Defines the identifier composition or namespace of values shown by Get Log Page - Log Page Identifiers.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.9</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, Figure 70, printed pages 39, PDF pages 39</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CSI</dt><dd>I/O Command Set Identifier: selects an I/O command set; NVM uses 00h.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-071 -->
<details class="field-note" id="figure-PCIE14-FIG-071"><summary>PCIe Figure 71 · Size of Physical Interface Receiver Eye Opening Measurement Log Page</summary>
<!-- claim:PCIE14-FIG-071-CLAIM -->
<p>Figure 71, "Size of Physical Interface Receiver Eye Opening Measurement Log Page": Shows the receiver-eye measurement information in Size of Physical Interface Receiver Eye Opening Measurement Log Page.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.9.1.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 71, printed pages 40, PDF pages 40</p></details>

</details>
<!-- figure-table:PCIE14-FIG-072 -->
<details class="field-note" id="figure-PCIE14-FIG-072"><summary>PCIe Figure 72 · Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field</summary>
<!-- claim:PCIE14-FIG-072-CLAIM -->
<p>Figure 72, "Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field": Defines the concrete layout or value relationships for Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.9.1.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 72, printed pages 40-41, PDF pages 40-41</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>LPOL</dt><dd>Log Page Offset Lower, the low 32 bits of the Get Log Page byte offset.</dd></div><div><dt>LPOU</dt><dd>Log Page Offset Upper, the high 32 bits of the Get Log Page byte offset.</dd></div><div><dt>EOM</dt><dd>Eye Opening Measurement, the procedure and log data for measuring a PCIe receiver eye opening.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-073 -->
<details class="field-note" id="figure-PCIE14-FIG-073"><summary>PCIe Figure 73 · Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field</summary>
<!-- claim:PCIE14-FIG-073-CLAIM -->
<p>Figure 73, "Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field": Defines the concrete layout or value relationships for Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.9.1.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 73, printed pages 41, PDF pages 41</p></details>

</details>
<!-- figure-table:PCIE14-FIG-074 -->
<details class="field-note" id="figure-PCIE14-FIG-074"><summary>PCIe Figure 74 · Physical Interface Receiver Eye Opening Measurement Log Page</summary>
<!-- claim:PCIE14-FIG-074-CLAIM -->
<p>Figure 74, "Physical Interface Receiver Eye Opening Measurement Log Page": Shows the receiver-eye measurement information in Physical Interface Receiver Eye Opening Measurement Log Page.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.9.1.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 74, printed pages 41, PDF pages 41</p></details>

</details>
<!-- figure-table:PCIE14-FIG-075 -->
<details class="field-note" id="figure-PCIE14-FIG-075"><summary>PCIe Figure 75 · EOM Header</summary>
<!-- claim:PCIE14-FIG-075-CLAIM -->
<p>Figure 75, "EOM Header": Shows the receiver-eye measurement information in EOM Header.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.9.1.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 75, printed pages 42-43, PDF pages 42-43</p></details>

</details>
<!-- figure-table:PCIE14-FIG-076 -->
<details class="field-note" id="figure-PCIE14-FIG-076"><summary>PCIe Figure 76 · EOM Lane Descriptor</summary>
<!-- claim:PCIE14-FIG-076-CLAIM -->
<p>Figure 76, "EOM Lane Descriptor": Defines the concrete layout or value relationships for EOM Lane Descriptor.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.9.1.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 76, printed pages 43-45, PDF pages 43-45</p></details>

</details>
<!-- figure-table:PCIE14-FIG-077 -->
<details class="field-note" id="figure-PCIE14-FIG-077"><summary>PCIe Figure 77 · Example of an Eve Diagram in the Printable Eye Field</summary>
<!-- claim:PCIE14-FIG-077-CLAIM -->
<p>Figure 77, "Example of an Eve Diagram in the Printable Eye Field": Defines the concrete layout or value relationships for Example of an Eve Diagram in the Printable Eye Field.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.9.1.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 77, printed pages 46, PDF pages 46</p></details>

</details>
</details>
</section>
<section id="additional-details"><h2 id="further-mechanisms">Additional mechanisms and data formats</h2>
<!-- claim:PCIE14-KEYWORDS -->
<p>The force of shall, may, and should remains defined by Base 2.4; a Transport summary must not strengthen or weaken the normative language.</p><details class="source-note"><summary>Sources: Base 2.4 §1.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §1.4.1, printed pages 2-3, PDF pages 28-29</p></details>
<!-- claim:PCIE14-RESET -->
<p>PCIe reset sources include Base controller/reset flows and PCIe-level resets. Recovery logic uses the reset type to determine controller-property, queue, and PCI-configuration state.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.3, printed pages 11-12, PDF pages 11-12</p></details>
<!-- claim:PCIE14-SECURITY -->
<p>Power-loss signaling, confidential computing, and TDISP map platform events or isolation state to NVMe-controller behavior. Implementation still requires external PCIe/TDISP specifications not supplied for this report.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>TDISP</dt><dd>TEE Device Interface Security Protocol, a PCIe security protocol related to platform isolation and device-interface state.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.8-3.8.10</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.8-3.8.10, printed pages 35-39, PDF pages 35-39</p></details>
<!-- figure-table:PCIE14-FIG-068 -->
<details class="field-note" id="figure-PCIE14-FIG-068"><summary>PCIe Figure 68 · Example of an Eve Diagram in the Printable Eye Field</summary>
<!-- claim:PCIE14-FIG-068-CLAIM -->
<p>Figure 68, "Example of an Eve Diagram in the Printable Eye Field": Defines the concrete layout or value relationships for Example of an Eve Diagram in the Printable Eye Field.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.9</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.9, Figure 68, printed pages 37, PDF pages 37</p></details>

</details>
<!-- figure-table:PCIE14-FIG-069 -->
<details class="field-note" id="figure-PCIE14-FIG-069"><summary>PCIe Figure 69 · NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure</summary>
<!-- claim:PCIE14-FIG-069-CLAIM -->
<p>Figure 69, "NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure": Defines the concrete layout or value relationships for NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure.</p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.10</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.10, Figure 69, printed pages 38-39, PDF pages 38-39</p></details>

</details>
</section>
<section id="knowledge-check"><h2 id="review-questions">Check your understanding</h2>
<!-- qa:pcie-transport-1.4-memory-mmio -->
<details class="review-question" id="qa-pcie-transport-1.4-memory-mmio"><summary>1. What roles do PCIe MMIO properties and host-memory queues play?</summary>
<div data-qa-answer="pcie-transport-1.4-memory-mmio"><p>Properties provide controller configuration, status, and queue notification interfaces. Queues carry command and completion entries. Separating the control interface from those structures explains how submission works.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, printed pages 9-10, PDF pages 9-10</p>
<p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, printed pages 11, PDF pages 11</p>
</details></details>
<!-- qa:pcie-transport-1.4-doorbell-stride -->
<details class="review-question" id="qa-pcie-transport-1.4-doorbell-stride"><summary>2. Why is it unsafe to assume adjacent doorbells are always 4 bytes apart?</summary>
<div data-qa-answer="pcie-transport-1.4-doorbell-stride"><p>CAP.DSTRD determines the spacing: stride is 2^(2+DSTRD) bytes. It is 4 bytes only when DSTRD=0; queue ID also determines the SQ Tail and CQ Head locations.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, printed pages 10-11, PDF pages 10-11</p>
</details></details>
<!-- qa:pcie-transport-1.4-interrupt -->
<details class="review-question" id="qa-pcie-transport-1.4-interrupt"><summary>3. Why must the host inspect the CQ after an interrupt?</summary>
<div data-qa-answer="pcie-transport-1.4-interrupt"><p>The interrupt is a notification; CQEs contain command identity and completion status. One notification need not correspond to one completion entry, so the host processes valid entries according to queue progress.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, printed pages 13-16, PDF pages 13-16</p>
<p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, printed pages 12-13, PDF pages 12-13</p>
</details></details>
<!-- qa:pcie-transport-1.4-error-layer -->
<details class="review-question" id="qa-pcie-transport-1.4-error-layer"><summary>4. Why distinguish NVMe command status from PCIe error reporting?</summary>
<div data-qa-answer="pcie-transport-1.4-error-layer"><p>The former describes command processing; the latter describes transport and device-level errors. They can be related, but they address different objects. Success in one layer does not establish the state of every layer.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, printed pages 16, PDF pages 16</p>
<p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, printed pages 16-35, PDF pages 16-35</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>Specification editions</summary><p>NVM Express NVMe over PCIe Transport Specification, Revision 1.4</p><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
