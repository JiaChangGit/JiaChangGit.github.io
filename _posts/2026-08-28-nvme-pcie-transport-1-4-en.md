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
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">NVMe over PCIe Transport explains how NVMe queues, properties, and notifications operate over PCIe. This note connects memory-mapped I/O, DMA, and interrupts to the transfer of an NVMe command.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express, the specification family for a host interface to a non-volatile-memory subsystem.</dd></div><div><dt>PCIe</dt><dd>PCI Express, the transport and device interconnect used by an NVMe memory-based controller.</dd></div><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl>
<h2 id="main-ideas">The main ideas</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>Interface locations</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">Use BARs and configuration space to find the NVMe interface and capabilities.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express, the specification family for a host interface to a non-volatile-memory subsystem.</dd></div></dl></article>
<article><span class="axis-number">02</span><h3>Commands and notifications</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">Distinguish queue data, doorbells, and interrupts.</span></p></article>
<article><span class="axis-number">03</span><h3>Platform behavior</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">Understand the scope of resets, power, error reporting, and link measurements.</span></p></article>
</div>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">The Base specification defines the common NVMe command and queue model; PCIe Transport supplies the local PCIe binding. Accessing a queue entry in memory and accessing a device MMIO register are different kinds of access.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>MMIO</dt><dd>Memory-Mapped I/O, access to device registers through CPU memory operations.</dd></div><div><dt>PCIe</dt><dd>PCI Express, the transport and device interconnect used by an NVMe memory-based controller.</dd></div></dl>
<div class="overview-connections"><h3>Connecting the main ideas</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.03">00.03.</span><span class="paragraph-text">The submission/completion model defined by Base needs concrete addresses, memory accesses, and notifications over PCIe. Find the controller register space, follow SQ/CQ exchanges, and then interpret interrupts and PCIe status.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>CQ</dt><dd>Completion Queue, the queue into which a controller posts command completions.</dd></div><div><dt>SQ</dt><dd>Submission Queue, the queue into which the host places commands.</dd></div></dl>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.04">00.04.</span><span class="paragraph-text">Configuration Space, error records, and eye measurements describe device presentation, transport events, and receiver measurement layouts at different levels. They are distinct from NVMe command completion status. The aim is to explain the roles of data, doorbells, and interrupts in an exchange.</span></p>
</div>
</section>
<section class="lesson" id="module-layers"><h2 id="heading-layers"><span class="section-number">01</span> How NVMe uses PCIe</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">Figure 1 shows document applicability and Figure 2 separates protocol responsibility. Engineering analysis separates command semantics from the way host memory, MMIO, configuration space, and interrupts carry the operation. The Transport does not rewrite Base when the two conflict.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div><div><dt>MMIO</dt><dd>Memory-Mapped I/O, access to device registers through CPU memory operations.</dd></div></dl>
<details class="technical-note"><summary>Full rules: How NVMe uses PCIe</summary>
<!-- claim:PCIE14-SCOPE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">The PCIe Transport supplements the Base Specification with PCIe-specific structures, extensions, requirements, and behavior; common NVMe behavior remains in Base. In a conflict, Base has higher precedence than a Transport Specification.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §1.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, printed pages 6, PDF pages 6</p></details>
<!-- claim:PCIE14-CONVENTION -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">This document inherits Base conventions. In register or property tables, the Reset column instead denotes the post-reset field value defined by the applicable PCI or PCIe specification.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §1.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.3, printed pages 6-7, PDF pages 6-7</p></details>
<!-- claim:PCIE14-OVERVIEW -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.04">01.04.</span><span class="paragraph-text">The PCIe transport uses memory-mapped I/O for data and register access, along with PCIe configuration space and message-signaled interrupts.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, printed pages 8, PDF pages 8</p></details>
</details>
<div class="table-wrap"><table><caption>How NVMe uses PCIe</caption><thead><tr><th scope="col">Specification layer</th><th scope="col">Behavior defined</th><th scope="col">Use in this report</th></tr></thead><tbody><tr><td>Base</td><td>Common command and completion semantics</td><td>Highest-precedence NVMe definition</td></tr><tr><td>PCIe Transport</td><td>Address, register, doorbell, and interrupt binding</td><td>Adds PCIe-specific requirements</td></tr><tr><td>PCI-SIG specifications</td><td>Native PCIe capability and transaction semantics</td><td>This report covers only NVMe-specific statements present in the supplied source</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.05">01.05.</span><span class="paragraph-text">Informative example: Base defines Firmware Commit CA/FS and status codes. The PCIe Transport adds where the SQE resides in host memory, where the doorbell resides in BAR0/1 memory space, and how a completion can trigger MSI-X.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>MSI-X</dt><dd>MSI-X, an extended message-signaled-interrupt mechanism with more vectors, per-vector masking, and a table.</dd></div><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div><div><dt>MSI</dt><dd>Message Signaled Interrupt, a PCI mechanism that delivers an interrupt through a memory-write message.</dd></div><div><dt>SQE</dt><dd>Submission Queue Entry, one command structure in an SQ.</dd></div><div><dt>CA</dt><dd>Commit Action, the Firmware Commit field selecting replacement, activation, and reset policy.</dd></div><div><dt>FS</dt><dd>Firmware Slot, the Firmware Commit field selecting the target slot.</dd></div></dl></aside>
<a class="reading-link" href="#reading-layers">Read the related specification figures → How NVMe uses PCIe</a>
</section>
<section class="lesson" id="module-mmio-doorbell"><h2 id="heading-mmio-doorbell"><span class="section-number">02</span> BARs, MMIO, and doorbell addresses</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">NVMe controller registers reside in the memory space designated by BAR0/BAR1. Doorbells begin at 1000h; SQ-tail and CQ-head registers for queue y are spaced using CAP.DSTRD. Figures 3-6 form one address derivation rather than four independent register tables.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>DSTRD</dt><dd>Doorbell Stride, the CAP field determining spacing between adjacent doorbell registers.</dd></div><div><dt>CAP</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities.</dd></div><div><dt>CQ</dt><dd>Completion Queue, the queue into which a controller posts command completions.</dd></div><div><dt>SQ</dt><dd>Submission Queue, the queue into which the host places commands.</dd></div></dl>
<details class="technical-note"><summary>Full rules: BARs, MMIO, and doorbell addresses</summary>
<!-- claim:PCIE14-MMIO -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">NVMe controller registers reside in memory space identified by BAR0/BAR1. The host shall use native-width or aligned 32-bit accesses and shall not issue locked accesses; violation produces undefined behavior.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, printed pages 9-10, PDF pages 9-10</p></details>
<!-- claim:PCIE14-DOORBELL -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">SQ-tail and CQ-head doorbells begin at offset 1000h, with stride determined by CAP.DSTRD; queue identifier y participates in the offset calculation.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>offset</dt><dd>offset: a displacement measured from a stated start. It answers “how far from the start,” unlike an index.</dd></div><div><dt>DSTRD</dt><dd>Doorbell Stride, the CAP field determining spacing between adjacent doorbell registers.</dd></div><div><dt>CAP</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.1.2.1-3.1.2.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, printed pages 10-11, PDF pages 10-11</p></details>
</details>
<div class="table-wrap"><table><caption>BARs, MMIO, and doorbell addresses</caption><thead><tr><th scope="col">Doorbell or written value</th><th scope="col">Address or value calculation</th><th scope="col">Host notification conveyed</th></tr></thead><tbody><tr><td>SQ y tail</td><td>1000h + (2y) x (4 &lt;&lt; DSTRD)</td><td>Host publishes a new SQ tail</td></tr><tr><td>CQ y head</td><td>1000h + (2y+1) x (4 &lt;&lt; DSTRD)</td><td>Host publishes a consumed CQ head</td></tr><tr><td>Doorbell value</td><td>Queue pointer</td><td>Does not contain the SQE or CQE body</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div><div><dt>SQE</dt><dd>Submission Queue Entry, one command structure in an SQ.</dd></div></dl>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.04">02.04.</span><span class="paragraph-text">Informative example: with DSTRD=1, stride=4&lt;&lt;1=8 bytes. SQ-tail offset for queue 3 is 1000h+(6x8)=1030h; CQ-head offset is 1000h+(7x8)=1038h. They differ by one stride. Treating DSTRD itself as a byte count makes every nonzero-DSTRD doorbell address wrong.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>offset</dt><dd>offset: a displacement measured from a stated start. It answers “how far from the start,” unlike an index.</dd></div></dl></aside>
<a class="reading-link" href="#reading-mmio-doorbell">Read the related specification figures → BARs, MMIO, and doorbell addresses</a>
</section>
<section class="lesson" id="module-command"><h2 id="heading-command"><span class="section-number">03</span> Command exchange between host and controller</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">SQE creation, doorbell write, controller fetch, CQE posting, interrupt delivery, and CQ-head update are not names for one event; they are successive ownership handoffs between host and controller. Their order governs both memory ordering and resource reuse.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div></dl>
<figure><figcaption><strong>One command round trip</strong></figcaption><ol class="flow-steps"><li>The host writes a command to the Submission Queue (SQ).</li><li>The host updates the SQ Tail Doorbell to announce new work.</li><li>The controller retrieves and executes the command, then writes its result to the Completion Queue (CQ).</li><li>The host reads the CQE and updates the CQ Head Doorbell to release consumed entries.</li></ol><figcaption>Queues hold commands and results; doorbells announce updated queue positions.</figcaption></figure>

<details class="technical-note"><summary>Full rules: Command exchange between host and controller</summary>
<!-- claim:PCIE14-COMMAND -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span><span class="paragraph-text">The command flow writes an SQE, updates the SQ-tail doorbell, lets the controller fetch and execute, posts a CQE, optionally interrupts, processes the CQE, and updates the CQ-head doorbell. A doorbell conveys a pointer, not the command body.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.4</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, printed pages 12-13, PDF pages 12-13</p></details>
<!-- claim:PCIE14-QUEUE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.03">03.03.</span><span class="paragraph-text">PCIe permits multiple Submission Queues to share a Completion Queue. If interrupts are enabled when creating the CQ, Interrupt Vector shall be initialized to the corresponding MSI-X or multiple-message MSI vector.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>MSI-X</dt><dd>MSI-X, an extended message-signaled-interrupt mechanism with more vectors, per-vector masking, and a table.</dd></div><div><dt>MSI</dt><dd>Message Signaled Interrupt, a PCI mechanism that delivers an interrupt through a memory-write message.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, printed pages 11, PDF pages 11</p></details>
</details>
<div class="table-wrap"><table><caption>Command exchange between host and controller</caption><thead><tr><th scope="col">Resource to reuse</th><th scope="col">When prior use ends</th><th scope="col">Host observation</th></tr></thead><tbody><tr><td>SQ-slot reuse</td><td>Controller has consumed the SQE</td><td>Completion SQHD assists tracking</td></tr><tr><td>Command-buffer reuse</td><td>Command completed and data is visible</td><td>Check command and data direction</td></tr><tr><td>CQ-slot release</td><td>Host completely consumed the CQE</td><td>Then write the CQ-head doorbell</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.04">03.04.</span><span class="paragraph-text">Informative example: if the host rings the doorbell before writing the final SQE dword, the controller may fetch a partial command. In the other direction, updating CQ head before fully reading the CQE can let the controller reuse that CQ slot. Both are ownership-ordering failures, not opcode failures.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Dword (double word): 32 bits, or 4 bytes. A word is 16 bits; for example, a zero-based dword count of 3 represents 4 Dwords, or 16 bytes.</dd></div></dl></aside>
<a class="reading-link" href="#reading-command">Read the related specification figures → Command exchange between host and controller</a>
</section>
<section class="lesson" id="module-interrupts"><h2 id="heading-interrupts"><span class="section-number">04</span> Interrupt modes and notification behavior</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">Pin-based, single-message MSI, multiple-message MSI, and MSI-X differ in more than performance. They provide different vector counts, masking locations, and capability structures; interrupt coalescing separately controls when multiple completions produce a notification. Figure 9 and Figures 34-46 belong with queue-to-vector mapping.</span></p>
<details class="technical-note"><summary>Full rules: Interrupt modes and notification behavior</summary>
<!-- claim:PCIE14-INTERRUPT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">Modes are pin-based, single-message MSI, multiple-message MSI, and MSI-X. The specification recommends MSI-X. Coalescing can reduce interrupt rate at the cost of latency, and Admin-CQ interrupts should not be delayed.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.5</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, printed pages 13-16, PDF pages 13-16</p></details>
<!-- claim:PCIE14-HOST -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.03">04.03.</span><span class="paragraph-text">Annex A is an informative host checklist: write the SQE before its doorbell, use phase to identify a new CQE, advance CQ head after consumption, and service every relevant CQ associated with an interrupt vector.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §Annex A</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §Annex A, printed pages 47-48, PDF pages 47-48</p></details>
</details>
<div class="table-wrap"><table><caption>Interrupt modes and notification behavior</caption><thead><tr><th scope="col">Interrupt mechanism</th><th scope="col">Notification and masking arrangement</th><th scope="col">Resources or limits affected</th></tr></thead><tbody><tr><td>Pin-based</td><td>Legacy shared signaling</td><td>Sharing and masking differ</td></tr><tr><td>Single MSI</td><td>One message/vector</td><td>Multiple CQs may share a service path</td></tr><tr><td>Multiple MSI</td><td>A set of contiguous messages</td><td>Constrained by MME/MMC capability</td></tr><tr><td>MSI-X</td><td>Table-based vectors with independent masks</td><td>Preferred by the specification</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.04">04.04.</span><span class="paragraph-text">Informative example: CQ 1 and CQ 2 share vector 5. When vector 5 arrives, the handler cannot inspect only CQ 1; it services every relevant CQ mapped to the vector. Raising the coalescing threshold can reduce interrupt rate while increasing CQE wait time.</span></p></aside>
<a class="reading-link" href="#reading-interrupts">Read the related specification figures → Interrupt modes and notification behavior</a>
</section>
<section class="lesson" id="module-config-error"><h2 id="heading-config-error"><span class="section-number">05</span> Configuration space and PCIe error reporting</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span><span class="paragraph-text">Figures 10-67 traverse the Type 0 header, Power Management, MSI/MSI-X, PCIe capability, and AER. Find the capability or extended-capability base before applying offsets. AER status, mask, severity, and header log form one diagnostic set rather than isolated error bits.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>AER</dt><dd>Advanced Error Reporting, the PCIe capability for classifying, masking, and logging link or transaction errors.</dd></div></dl>
<details class="technical-note"><summary>Full rules: Configuration space and PCIe error reporting</summary>
<!-- claim:PCIE14-CONFIG -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.02">05.02.</span><span class="paragraph-text">Section 3.8 defines additional NVMe-controller requirements for the PCI header, Power Management, MSI/MSI-X, PCIe capability, and AER. Original PCI/PCIe field semantics remain governed by PCI-SIG specifications.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>AER</dt><dd>Advanced Error Reporting, the PCIe capability for classifying, masking, and logging link or transaction errors.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1-3.8.7</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, printed pages 16-35, PDF pages 16-35</p></details>
<!-- claim:PCIE14-ERROR -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.03">05.03.</span><span class="paragraph-text">NVMe command errors are reported in CQE status, while PCIe transport or link errors use PCIe mechanisms plus this document’s NVMe-specific requirements. Their recovery scopes differ.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.7</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, printed pages 16, PDF pages 16</p></details>
<!-- claim:PCIE14-POWER -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.04">05.04.</span><span class="paragraph-text">The host shall never select an NVMe power state whose consumption exceeds the PCIe slot power limit; violation results in undefined power behavior.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.6</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.6, printed pages 16, PDF pages 16</p></details>
</details>
<div class="table-wrap"><table><caption>Configuration space and PCIe error reporting</caption><thead><tr><th scope="col">Reporting layer or capability</th><th scope="col">Event or resource described</th><th scope="col">Information needed alongside it</th></tr></thead><tbody><tr><td>NVMe CQE status</td><td>Command execution result</td><td>Read the fields in NVMe command context</td></tr><tr><td>PCIe Device Status</td><td>PCIe Function status summary</td><td>Found in PCIe capability</td></tr><tr><td>AER</td><td>Correctable/uncorrectable transport errors</td><td>Read status, mask, severity, and header together</td></tr><tr><td>Power state</td><td>Slot limit and device power control</td><td>Never choose an NVMe state above the slot power limit</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="05.05">05.05.</span><span class="paragraph-text">Informative example: when an AERUCES bit is set, first check its mask to determine reporting, then its severity for handling, and finally the header log for transaction context. The bit cannot be translated directly into an NVMe SC.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SC</dt><dd>Status Code: identifies the completion result within the selected SCT category.</dd></div></dl></aside>
<a class="reading-link" href="#reading-config-error">Read the related specification figures → Configuration space and PCIe error reporting</a>
</section>
<section class="lesson" id="module-eom"><h2 id="heading-eom"><span class="section-number">06</span> Receiver eye-opening measurement data layout</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.01">06.01.</span><span class="paragraph-text">The receiver eye-opening measurement log has variable length. Its header describes the whole dataset, while lane descriptors describe individual lanes. Structure levels and length units identify which lane each measurement belongs to.</span></p>
<details class="technical-note"><summary>Full rules: Receiver eye-opening measurement data layout</summary>
<!-- claim:PCIE14-EOM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.02">06.02.</span><span class="paragraph-text">The Physical Interface Receiver Eye Opening Measurement log page reports measurements through a header, lane descriptors, and EOM data. The host checks support and size before parsing lanes and parameters.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>EOM</dt><dd>Eye Opening Measurement, the procedure and log data for measuring a PCIe receiver eye opening.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.9</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, printed pages 39-46, PDF pages 39-46</p></details>
</details>
<div class="table-wrap"><table><caption>Receiver eye-opening measurement data layout</caption><thead><tr><th scope="col">Measurement region</th><th scope="col">Measurement or location described</th><th scope="col">Checks before comparison</th></tr></thead><tbody><tr><td>Specific parameter</td><td>Selects measurement action and quality/state</td><td>Establish request context first</td></tr><tr><td>Specific identifier</td><td>Selects lane/test context</td><td>Prevents mixing different measurements</td></tr><tr><td>Header</td><td>Global length and layout</td><td>Base for every later offset</td></tr><tr><td>Lane descriptor</td><td>Per-lane boundaries and status</td><td>Walk only within returned buffer</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="06.03">06.03.</span><span class="paragraph-text">To compare two lanes, find each measurement through its lane descriptor and compare using the same measurement format. The header lane count describes structure, not measurement quality.</span></p></aside>
<a class="reading-link" href="#reading-eom">Read the related specification figures → Receiver eye-opening measurement data layout</a>
</section>
<details class="figure-reading-fold"><summary>Expand figure teaching: read source figures by concept</summary>
<section id="figure-reading"><h2><span class="section-number">07</span> Reading the specification figures</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.01">07.01.</span><span class="paragraph-text">The specification figures below are grouped by concept. Each group explains the reading order and question to resolve, followed by the fields or behavior described by each figure. Follow links from the lessons or use this section to connect fields to complete operations.</span></p>
<div class="figure-reading-group" id="reading-layers"><h3>Figure group 01 · How NVMe uses PCIe</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.02">07.02.</span><span class="paragraph-text">Separate command semantics, the NVMe-to-PCIe binding, and native PCIe capabilities. Trace one command through SQE, host buffer, doorbell, and interrupt locations rather than treating the documents as sequential execution stages.</span></p>
<a class="reading-link" href="#module-layers">Return to the explanation and example</a>
<!-- figure-table:PCIE14-FIG-001 -->
<details class="field-note" id="figure-PCIE14-FIG-001"><summary>PCIe Figure 1 · NVMe Family of Specifications</summary>
<!-- claim:PCIE14-FIG-001-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.03">07.03.</span><span class="paragraph-text">Figure 1, "NVMe Family of Specifications": Layer diagrams separate NVMe command mechanisms from PCIe exchange details. Data pointers, queue memory, and doorbells work together, while block-operation semantics remain defined by the appropriate NVMe specification.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §1.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §1.2, Figure 1, printed pages 6, PDF pages 6</p></details>

</details>
<!-- figure-table:PCIE14-FIG-002 -->
<details class="field-note" id="figure-PCIE14-FIG-002"><summary>PCIe Figure 2 · Example of Transport Protocol Layers</summary>
<!-- claim:PCIE14-FIG-002-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.04">07.04.</span><span class="paragraph-text">Figure 2, "Example of Transport Protocol Layers": Layer diagrams separate NVMe command mechanisms from PCIe exchange details. Data pointers, queue memory, and doorbells work together, while block-operation semantics remain defined by the appropriate NVMe specification.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §2, Figure 2, printed pages 8, PDF pages 8</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-mmio-doorbell"><h3>Figure group 02 · BARs, MMIO, and doorbell addresses</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.05">07.05.</span><span class="paragraph-text">Calculate the BAR base, 1000h origin, queue ID, and stride separately. Find the register before interpreting the head/tail value written to it; register address and register contents are different quantities.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>BAR</dt><dd>Base Address Register, a PCI-configuration-space register finding a device memory space.</dd></div></dl>
<a class="reading-link" href="#module-mmio-doorbell">Return to the explanation and example</a>
<!-- figure-table:PCIE14-FIG-003 -->
<details class="field-note" id="figure-PCIE14-FIG-003"><summary>PCIe Figure 3 · PCI Express Registers</summary>
<!-- claim:PCIE14-FIG-003-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.06">07.06.</span><span class="paragraph-text">Figure 3, "PCI Express Registers": Use Configuration Space to find BARs and capabilities before entering memory-mapped controller space. Configuration offsets and offsets within a BAR have different origins and are not interchangeable.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>BAR</dt><dd>Base Address Register, a PCI-configuration-space register finding a device memory space.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, Figure 3, printed pages 9, PDF pages 9</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>MSIXCAP</dt><dd>MSI-X Capability, the base of the MSI-X capability structure.</dd></div><div><dt>AERCAP</dt><dd>Advanced Error Reporting Capability, the base of the AER extended-capability structure.</dd></div><div><dt>MSICAP</dt><dd>MSI Capability, the base of the MSI capability structure.</dd></div><div><dt>PMCAP</dt><dd>Power Management Capability, the base of the PCI power-management capability structure.</dd></div><div><dt>PXCAP</dt><dd>PCI Express Capability, the base of the PCIe capability structure.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-004 -->
<details class="field-note" id="figure-PCIE14-FIG-004"><summary>PCIe Figure 4 · PCI Express Specific Controller Property Definitions</summary>
<!-- claim:PCIE14-FIG-004-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.07">07.07.</span><span class="paragraph-text">Figure 4, "PCI Express Specific Controller Property Definitions": Use Configuration Space to find BARs and capabilities before entering memory-mapped controller space. Configuration offsets and offsets within a BAR have different origins and are not interchangeable.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, Figure 4, printed pages 9-10, PDF pages 9-10</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CAP.DSTRD</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.DSTRD selects its DSTRD member field.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-005 -->
<details class="field-note" id="figure-PCIE14-FIG-005"><summary>PCIe Figure 5 · Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL - Submission Queue y Tail</summary>
<!-- claim:PCIE14-FIG-005-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.08">07.08.</span><span class="paragraph-text">Figure 5, "Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL - Submission Queue y Tail": SQ Tail and CQ Head locations depend on queue ID and spacing of 4×2^DSTRD. The registers alternate, and their contents are queue positions rather than command or completion data.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SQyTDBL</dt><dd>Submission Queue y Tail Doorbell, the MMIO register through which the host publishes the new tail of SQ y.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.1.2.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1, Figure 5, printed pages 10, PDF pages 10</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CAP.DSTRD</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities. Here CAP.DSTRD selects its DSTRD member field.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-006 -->
<details class="field-note" id="figure-PCIE14-FIG-006"><summary>PCIe Figure 6 · Offset (1000h + ((2y + 1) * (4 &lt;&lt; CAP.DSTRD))): CQyHDBL - Completion Queue y Head</summary>
<!-- claim:PCIE14-FIG-006-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.09">07.09.</span><span class="paragraph-text">Figure 6, "Offset (1000h + ((2y + 1) * (4 &lt;&lt; CAP.DSTRD))): CQyHDBL - Completion Queue y Head": SQ Tail and CQ Head locations depend on queue ID and spacing of 4×2^DSTRD. The registers alternate, and their contents are queue positions rather than command or completion data.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CQyHDBL</dt><dd>Completion Queue y Head Doorbell, the MMIO register through which the host publishes the consumed head of CQ y.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.1.2.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1, Figure 6, printed pages 10-11, PDF pages 10-11</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CC.PI</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.PI selects its PI member field.</dd></div><div><dt>CC</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller.</dd></div><div><dt>PI</dt><dd>Protection Information: Guard and tag fields used to check data and its associated information.</dd></div></dl>
</details>
</div>
<div class="figure-reading-group" id="reading-command"><h3>Figure group 03 · Command exchange between host and controller</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.10">07.10.</span><span class="paragraph-text">Read three lifetimes: SQE publication/fetch, data-buffer use, and CQE production/release. SQHD helps track SQ consumption, SQID/CID identify the completed command, and CQ Head releases completion slots.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SQID</dt><dd>Submission Queue Identifier, the numeric identifier of the SQ containing a command.</dd></div><div><dt>CID</dt><dd>Command Identifier, used with the SQ identifier to identify an outstanding command.</dd></div></dl>
<a class="reading-link" href="#module-command">Return to the explanation and example</a>
<!-- figure-table:PCIE14-FIG-007 -->
<details class="field-note" id="figure-PCIE14-FIG-007"><summary>PCIe Figure 7 · Create I/O Completion Queue - Command Dword 11</summary>
<!-- claim:PCIE14-FIG-007-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.11">07.11.</span><span class="paragraph-text">Figure 7, "Create I/O Completion Queue - Command Dword 11": Create CQ IV associates a completion queue with an interrupt vector. The controller updates the CQ and notifies under the chosen interrupt mechanism. Shared vectors require examining all associated CQs.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Dword (double word): 32 bits, or 4 bytes. A word is 16 bits; for example, a zero-based dword count of 3 represents 4 Dwords, or 16 bytes.</dd></div><div><dt>IV</dt><dd>Interrupt Vector, the vector number assigned to a Completion Queue.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, Figure 7, printed pages 11, PDF pages 11</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>MSIXCAP.MXC.TS</dt><dd>MSI-X Capability, the base of the MSI-X capability structure. Here MSIXCAP.MXC.TS selects its MXC.TS member field.</dd></div><div><dt>MSICAP.MC.MME</dt><dd>MSI Capability, the base of the MSI capability structure. Here MSICAP.MC.MME selects its MC.MME member field.</dd></div><div><dt>MSIXCAP</dt><dd>MSI-X Capability, the base of the MSI-X capability structure.</dd></div><div><dt>MSICAP</dt><dd>MSI Capability, the base of the MSI capability structure.</dd></div><div><dt>IV</dt><dd>Interrupt Vector, the vector number assigned to a Completion Queue.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-008 -->
<details class="field-note" id="figure-PCIE14-FIG-008"><summary>PCIe Figure 8 · Command Processing</summary>
<!-- claim:PCIE14-FIG-008-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.12">07.12.</span><span class="paragraph-text">Figure 8, "Command Processing": Create CQ IV associates a completion queue with an interrupt vector. The controller updates the CQ and notifies under the chosen interrupt mechanism. Shared vectors require examining all associated CQs.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.4.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4.1, Figure 8, printed pages 13, PDF pages 13</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-interrupts"><h3>Figure group 04 · Interrupt modes and notification behavior</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.13">07.13.</span><span class="paragraph-text">Connect CQs to vectors before reading enable, mask, and table fields for the chosen interrupt mechanism. For shared vectors, follow all associated CQs. Coalescing changes notification timing, not the meaning of CQE status.</span></p>
<a class="reading-link" href="#module-interrupts">Return to the explanation and example</a>
<!-- figure-table:PCIE14-FIG-009 -->
<details class="field-note" id="figure-PCIE14-FIG-009"><summary>PCIe Figure 9 · Pin Based, Single MSI, and Multiple MSI Behavior</summary>
<!-- claim:PCIE14-FIG-009-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.14">07.14.</span><span class="paragraph-text">Figure 9, "Pin Based, Single MSI, and Multiple MSI Behavior": Create CQ IV associates a completion queue with an interrupt vector. The controller updates the CQ and notifies under the chosen interrupt mechanism. Shared vectors require examining all associated CQs.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.5.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5.1, Figure 9, printed pages 15, PDF pages 15</p></details>

</details>
<!-- figure-table:PCIE14-FIG-034 -->
<details class="field-note" id="figure-PCIE14-FIG-034"><summary>PCIe Figure 34 · Message Signaled Interrupt Capability (Optional)</summary>
<!-- claim:PCIE14-FIG-034-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.15">07.15.</span><span class="paragraph-text">Figure 34, "Message Signaled Interrupt Capability (Optional)": MSI signals interrupts through message address/data, with Message Control governing enablement and message counts. Masks control reporting and Pending records deferred notification; none is the command-completion content stored in a CQ.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.2.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.3, Figure 34, printed pages 22, PDF pages 22</p></details>

</details>
<!-- figure-table:PCIE14-FIG-035 -->
<details class="field-note" id="figure-PCIE14-FIG-035"><summary>PCIe Figure 35 · Offset MSICAP: MID - Message Signaled Interrupt Identifiers</summary>
<!-- claim:PCIE14-FIG-035-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.16">07.16.</span><span class="paragraph-text">Figure 35, "Offset MSICAP: MID - Message Signaled Interrupt Identifiers": MSI signals interrupts through message address/data, with Message Control governing enablement and message counts. Masks control reporting and Pending records deferred notification; none is the command-completion content stored in a CQ.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.3.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.1, Figure 35, printed pages 23, PDF pages 23</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CID</dt><dd>Command Identifier, used with the SQ identifier to identify an outstanding command.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-036 -->
<details class="field-note" id="figure-PCIE14-FIG-036"><summary>PCIe Figure 36 · Offset MSICAP + 2h: MC - Message Signaled Interrupt Message Control</summary>
<!-- claim:PCIE14-FIG-036-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.17">07.17.</span><span class="paragraph-text">Figure 36, "Offset MSICAP + 2h: MC - Message Signaled Interrupt Message Control": MSI signals interrupts through message address/data, with Message Control governing enablement and message counts. Masks control reporting and Pending records deferred notification; none is the command-completion content stored in a CQ.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.3.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.2, Figure 36, printed pages 23, PDF pages 23</p></details>

</details>
<!-- figure-table:PCIE14-FIG-037 -->
<details class="field-note" id="figure-PCIE14-FIG-037"><summary>PCIe Figure 37 · Offset MSICAP + 4h: MA - Message Signaled Interrupt Message Address</summary>
<!-- claim:PCIE14-FIG-037-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.18">07.18.</span><span class="paragraph-text">Figure 37, "Offset MSICAP + 4h: MA - Message Signaled Interrupt Message Address": MSI signals interrupts through message address/data, with Message Control governing enablement and message counts. Masks control reporting and Pending records deferred notification; none is the command-completion content stored in a CQ.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.3.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.3, Figure 37, printed pages 23, PDF pages 23</p></details>

</details>
<!-- figure-table:PCIE14-FIG-038 -->
<details class="field-note" id="figure-PCIE14-FIG-038"><summary>PCIe Figure 38 · Offset MSICAP + 8h: MUA - Message Signaled Interrupt Upper Address</summary>
<!-- claim:PCIE14-FIG-038-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.19">07.19.</span><span class="paragraph-text">Figure 38, "Offset MSICAP + 8h: MUA - Message Signaled Interrupt Upper Address": MSI signals interrupts through message address/data, with Message Control governing enablement and message counts. Masks control reporting and Pending records deferred notification; none is the command-completion content stored in a CQ.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.3.4</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.4, Figure 38, printed pages 23, PDF pages 23</p></details>

</details>
<!-- figure-table:PCIE14-FIG-039 -->
<details class="field-note" id="figure-PCIE14-FIG-039"><summary>PCIe Figure 39 · Offset MSICAP + Ch: MD - Message Signaled Interrupt Message Data</summary>
<!-- claim:PCIE14-FIG-039-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.20">07.20.</span><span class="paragraph-text">Figure 39, "Offset MSICAP + Ch: MD - Message Signaled Interrupt Message Data": MSI signals interrupts through message address/data, with Message Control governing enablement and message counts. Masks control reporting and Pending records deferred notification; none is the command-completion content stored in a CQ.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.3.5</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.5, Figure 39, printed pages 23, PDF pages 23</p></details>

</details>
<!-- figure-table:PCIE14-FIG-040 -->
<details class="field-note" id="figure-PCIE14-FIG-040"><summary>PCIe Figure 40 · Offset MSICAP + 10h: MMASK - Message Signaled Interrupt Mask Bits (Optional)</summary>
<!-- claim:PCIE14-FIG-040-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.21">07.21.</span><span class="paragraph-text">Figure 40, "Offset MSICAP + 10h: MMASK - Message Signaled Interrupt Mask Bits (Optional)": MSI signals interrupts through message address/data, with Message Control governing enablement and message counts. Masks control reporting and Pending records deferred notification; none is the command-completion content stored in a CQ.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.3.6</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.6, Figure 40, printed pages 24, PDF pages 24</p></details>

</details>
<!-- figure-table:PCIE14-FIG-041 -->
<details class="field-note" id="figure-PCIE14-FIG-041"><summary>PCIe Figure 41 · Offset MSICAP + 14h: MPEND - Message Signaled Interrupt Pending Bits (Optional)</summary>
<!-- claim:PCIE14-FIG-041-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.22">07.22.</span><span class="paragraph-text">Figure 41, "Offset MSICAP + 14h: MPEND - Message Signaled Interrupt Pending Bits (Optional)": MSI signals interrupts through message address/data, with Message Control governing enablement and message counts. Masks control reporting and Pending records deferred notification; none is the command-completion content stored in a CQ.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.3.7</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.7, Figure 41, printed pages 24, PDF pages 24</p></details>

</details>
<!-- figure-table:PCIE14-FIG-042 -->
<details class="field-note" id="figure-PCIE14-FIG-042"><summary>PCIe Figure 42 · MSI-X Capability (Optional)</summary>
<!-- claim:PCIE14-FIG-042-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.23">07.23.</span><span class="paragraph-text">Figure 42, "MSI-X Capability (Optional)": MSI-X control describes enablement, Function Mask, and table size. MTAB/MPBA find the Table and Pending Bit Array with a BIR and offset. Select the BAR using BIR before adding the offset; the whole field is not an absolute address.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>BIR</dt><dd>BAR Indicator Register, a selector identifying the PCIe BAR that contains a memory structure.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.3.7</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.3.7, Figure 42, printed pages 24, PDF pages 24</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>BIR</dt><dd>BAR Indicator Register, a selector identifying the PCIe BAR that contains a memory structure.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-043 -->
<details class="field-note" id="figure-PCIE14-FIG-043"><summary>PCIe Figure 43 · Offset MSIXCAP: MXID - MSI-X Identifiers</summary>
<!-- claim:PCIE14-FIG-043-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.24">07.24.</span><span class="paragraph-text">Figure 43, "Offset MSIXCAP: MXID - MSI-X Identifiers": MSI-X control describes enablement, Function Mask, and table size. MTAB/MPBA find the Table and Pending Bit Array with a BIR and offset. Select the BAR using BIR before adding the offset; the whole field is not an absolute address.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.4.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.1, Figure 43, printed pages 24, PDF pages 24</p></details>

</details>
<!-- figure-table:PCIE14-FIG-044 -->
<details class="field-note" id="figure-PCIE14-FIG-044"><summary>PCIe Figure 44 · Offset MSIXCAP + 2h: MXC - MSI-X Message Control</summary>
<!-- claim:PCIE14-FIG-044-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.25">07.25.</span><span class="paragraph-text">Figure 44, "Offset MSIXCAP + 2h: MXC - MSI-X Message Control": MSI-X control describes enablement, Function Mask, and table size. MTAB/MPBA find the Table and Pending Bit Array with a BIR and offset. Select the BAR using BIR before adding the offset; the whole field is not an absolute address.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.4.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.2, Figure 44, printed pages 24-25, PDF pages 24-25</p></details>

</details>
<!-- figure-table:PCIE14-FIG-045 -->
<details class="field-note" id="figure-PCIE14-FIG-045"><summary>PCIe Figure 45 · Offset MSIXCAP + 4h: MTAB - MSI-X Table Offset / Table BIR</summary>
<!-- claim:PCIE14-FIG-045-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.26">07.26.</span><span class="paragraph-text">Figure 45, "Offset MSIXCAP + 4h: MTAB - MSI-X Table Offset / Table BIR": MSI-X control describes enablement, Function Mask, and table size. MTAB/MPBA find the Table and Pending Bit Array with a BIR and offset. Select the BAR using BIR before adding the offset; the whole field is not an absolute address.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.4.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.3, Figure 45, printed pages 25, PDF pages 25</p></details>

</details>
<!-- figure-table:PCIE14-FIG-046 -->
<details class="field-note" id="figure-PCIE14-FIG-046"><summary>PCIe Figure 46 · Offset MSIXCAP + 8h: MPBA - MSI-X PBA Offset / PBA BIR</summary>
<!-- claim:PCIE14-FIG-046-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.27">07.27.</span><span class="paragraph-text">Figure 46, "Offset MSIXCAP + 8h: MPBA - MSI-X PBA Offset / PBA BIR": MSI-X control describes enablement, Function Mask, and table size. MTAB/MPBA find the Table and Pending Bit Array with a BIR and offset. Select the BAR using BIR before adding the offset; the whole field is not an absolute address.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PBA</dt><dd>Pending Bit Array, the MSI-X bit array recording vectors that are pending service.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.4.4</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.4.4, Figure 46, printed pages 25, PDF pages 25</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>PBAO</dt><dd>Page Base Address and Offset, the first-PRP layout combining a page base address with an in-page offset.</dd></div><div><dt>PBA</dt><dd>Pending Bit Array, the MSI-X bit array recording vectors that are pending service.</dd></div></dl>
</details>
</div>
<div class="figure-reading-group" id="reading-config-error"><h3>Figure group 05 · Configuration space and PCIe error reporting</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.28">07.28.</span><span class="paragraph-text">Identify the PCIe capability, then pair status, mask, severity, and header-log information. Read TDISP DEVICE_INTERFACE_REPORT under its own layout rather than applying error-log or NVMe CQE formats.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>TDISP</dt><dd>TEE Device Interface Security Protocol, a PCIe security protocol related to platform isolation and device-interface state.</dd></div></dl>
<a class="reading-link" href="#module-config-error">Return to the explanation and example</a>
<!-- figure-table:PCIE14-FIG-010 -->
<details class="field-note" id="figure-PCIE14-FIG-010"><summary>PCIe Figure 10 · PCI Express Type 0/1 Common Configuration Space</summary>
<!-- claim:PCIE14-FIG-010-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.29">07.29.</span><span class="paragraph-text">Figure 10, "PCI Express Type 0/1 Common Configuration Space": Use Configuration Space to find BARs and capabilities before entering memory-mapped controller space. Configuration offsets and offsets within a BAR have different origins and are not interchangeable.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8, Figure 10, printed pages 16-17, PDF pages 16-17</p></details>

</details>
<!-- figure-table:PCIE14-FIG-011 -->
<details class="field-note" id="figure-PCIE14-FIG-011"><summary>PCIe Figure 11 · Offset 00h: ID - Identifiers</summary>
<!-- claim:PCIE14-FIG-011-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.30">07.30.</span><span class="paragraph-text">Figure 11, "Offset 00h: ID - Identifiers": Device identity, revision, class code, header type, and subsystem identity describe different attributes. Find each Configuration Space field before interpretation. PI in PCIe Class Code is not NVM Protection Information.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Protection Information</dt><dd>PI: protection fields containing a Guard and tags for checking data and its associated information.</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div><div><dt>PI</dt><dd>Protection Information: Guard and tag fields used to check data and its associated information.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.1, Figure 11, printed pages 17, PDF pages 17</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>DID</dt><dd>Domain Identifier, the identifier of a domain within an NVM subsystem.</dd></div><div><dt>VID</dt><dd>Vendor ID, a PCI-SIG-assigned identifier for a vendor.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-012 -->
<details class="field-note" id="figure-PCIE14-FIG-012"><summary>PCIe Figure 12 · Offset 04h: CMD - Command</summary>
<!-- claim:PCIE14-FIG-012-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.31">07.31.</span><span class="paragraph-text">Figure 12, "Offset 04h: CMD - Command": These common Configuration Space fields include control, status, and compatibility fields. Follow the access types and fixed values specified by Transport. PCIe BIST is distinct from NVMe Device Self-test and does not share its result format.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.2, Figure 12, printed pages 17, PDF pages 17</p></details>

</details>
<!-- figure-table:PCIE14-FIG-013 -->
<details class="field-note" id="figure-PCIE14-FIG-013"><summary>PCIe Figure 13 · Offset 06h: STS - Device Status</summary>
<!-- claim:PCIE14-FIG-013-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.32">07.32.</span><span class="paragraph-text">Figure 13, "Offset 06h: STS - Device Status": These common Configuration Space fields include control, status, and compatibility fields. Follow the access types and fixed values specified by Transport. PCIe BIST is distinct from NVMe Device Self-test and does not share its result format.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.3, Figure 13, printed pages 18, PDF pages 18</p></details>

</details>
<!-- figure-table:PCIE14-FIG-014 -->
<details class="field-note" id="figure-PCIE14-FIG-014"><summary>PCIe Figure 14 · Offset 08h: RID - Revision ID</summary>
<!-- claim:PCIE14-FIG-014-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.33">07.33.</span><span class="paragraph-text">Figure 14, "Offset 08h: RID - Revision ID": Device identity, revision, class code, header type, and subsystem identity describe different attributes. Find each Configuration Space field before interpretation. PI in PCIe Class Code is not NVM Protection Information.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Protection Information</dt><dd>PI: protection fields containing a Guard and tags for checking data and its associated information.</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.4</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.4, Figure 14, printed pages 18, PDF pages 18</p></details>

</details>
<!-- figure-table:PCIE14-FIG-015 -->
<details class="field-note" id="figure-PCIE14-FIG-015"><summary>PCIe Figure 15 · Offset 09h: CC - Class Code</summary>
<!-- claim:PCIE14-FIG-015-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.34">07.34.</span><span class="paragraph-text">Figure 15, "Offset 09h: CC - Class Code": Device identity, revision, class code, header type, and subsystem identity describe different attributes. Find each Configuration Space field before interpretation. PI in PCIe Class Code is not NVM Protection Information.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CC</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.5</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.5, Figure 15, printed pages 18, PDF pages 18</p></details>

</details>
<!-- figure-table:PCIE14-FIG-016 -->
<details class="field-note" id="figure-PCIE14-FIG-016"><summary>PCIe Figure 16 · Offset 0Ch: CLS - Cache Line Size</summary>
<!-- claim:PCIE14-FIG-016-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.35">07.35.</span><span class="paragraph-text">Figure 16, "Offset 0Ch: CLS - Cache Line Size": These common Configuration Space fields include control, status, and compatibility fields. Follow the access types and fixed values specified by Transport. PCIe BIST is distinct from NVMe Device Self-test and does not share its result format.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.6</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.6, Figure 16, printed pages 18, PDF pages 18</p></details>

</details>
<!-- figure-table:PCIE14-FIG-017 -->
<details class="field-note" id="figure-PCIE14-FIG-017"><summary>PCIe Figure 17 · Offset 0Dh: MLT - Master Latency Timer</summary>
<!-- claim:PCIE14-FIG-017-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.36">07.36.</span><span class="paragraph-text">Figure 17, "Offset 0Dh: MLT - Master Latency Timer": These common Configuration Space fields include control, status, and compatibility fields. Follow the access types and fixed values specified by Transport. PCIe BIST is distinct from NVMe Device Self-test and does not share its result format.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.7</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.7, Figure 17, printed pages 18, PDF pages 18</p></details>

</details>
<!-- figure-table:PCIE14-FIG-018 -->
<details class="field-note" id="figure-PCIE14-FIG-018"><summary>PCIe Figure 18 · Offset 0Eh: HTYPE - Header Type</summary>
<!-- claim:PCIE14-FIG-018-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.37">07.37.</span><span class="paragraph-text">Figure 18, "Offset 0Eh: HTYPE - Header Type": Device identity, revision, class code, header type, and subsystem identity describe different attributes. Find each Configuration Space field before interpretation. PI in PCIe Class Code is not NVM Protection Information.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.8</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.8, Figure 18, printed pages 19, PDF pages 19</p></details>

</details>
<!-- figure-table:PCIE14-FIG-019 -->
<details class="field-note" id="figure-PCIE14-FIG-019"><summary>PCIe Figure 19 · Offset 0Fh: BIST - Built-In Self Test (Optional)</summary>
<!-- claim:PCIE14-FIG-019-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.38">07.38.</span><span class="paragraph-text">Figure 19, "Offset 0Fh: BIST - Built-In Self Test (Optional)": These common Configuration Space fields include control, status, and compatibility fields. Follow the access types and fixed values specified by Transport. PCIe BIST is distinct from NVMe Device Self-test and does not share its result format.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.9</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.9, Figure 19, printed pages 19, PDF pages 19</p></details>

</details>
<!-- figure-table:PCIE14-FIG-020 -->
<details class="field-note" id="figure-PCIE14-FIG-020"><summary>PCIe Figure 20 · Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits</summary>
<!-- claim:PCIE14-FIG-020-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.39">07.39.</span><span class="paragraph-text">Figure 20, "Offset 10h: MLBAR (BAR0) - Memory Register Base Address, lower 32-bits": BAR0/BAR1 halves describe the controller memory base, while other BARs, Expansion ROM, and Capabilities Pointer serve different purposes. Separate address and attribute bits; a capability-list pointer is not an MMIO data address.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.10</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.10, Figure 20, printed pages 19, PDF pages 19</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>PF</dt><dd>Physical Function, a full-featured PCIe function that can manage associated VFs.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-021 -->
<details class="field-note" id="figure-PCIE14-FIG-021"><summary>PCIe Figure 21 · Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits</summary>
<!-- claim:PCIE14-FIG-021-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.40">07.40.</span><span class="paragraph-text">Figure 21, "Offset 14h: MUBAR (BAR1) - Memory Register Base Address, upper 32-bits": BAR0/BAR1 halves describe the controller memory base, while other BARs, Expansion ROM, and Capabilities Pointer serve different purposes. Separate address and attribute bits; a capability-list pointer is not an MMIO data address.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.11</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.11, Figure 21, printed pages 19, PDF pages 19</p></details>

</details>
<!-- figure-table:PCIE14-FIG-022 -->
<details class="field-note" id="figure-PCIE14-FIG-022"><summary>PCIe Figure 22 · Offset 18h: BAR2 - Index/Data Pair Register Base Address or Vendor Specific</summary>
<!-- claim:PCIE14-FIG-022-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.41">07.41.</span><span class="paragraph-text">Figure 22, "Offset 18h: BAR2 - Index/Data Pair Register Base Address or Vendor Specific": BAR0/BAR1 halves describe the controller memory base, while other BARs, Expansion ROM, and Capabilities Pointer serve different purposes. Separate address and attribute bits; a capability-list pointer is not an MMIO data address.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>index</dt><dd>index: selects an item or format in a list. It answers “which one,” not “how far from the start.”</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.12</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.12, Figure 22, printed pages 20, PDF pages 20</p></details>

</details>
<!-- figure-table:PCIE14-FIG-023 -->
<details class="field-note" id="figure-PCIE14-FIG-023"><summary>PCIe Figure 23 · Offset 28h: CCPTR - CardBus CIS Pointer</summary>
<!-- claim:PCIE14-FIG-023-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.42">07.42.</span><span class="paragraph-text">Figure 23, "Offset 28h: CCPTR - CardBus CIS Pointer": These common Configuration Space fields include control, status, and compatibility fields. Follow the access types and fixed values specified by Transport. PCIe BIST is distinct from NVMe Device Self-test and does not share its result format.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.16</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.16, Figure 23, printed pages 20, PDF pages 20</p></details>

</details>
<!-- figure-table:PCIE14-FIG-024 -->
<details class="field-note" id="figure-PCIE14-FIG-024"><summary>PCIe Figure 24 · Offset 2Ch: SS - Subsystem Identifiers</summary>
<!-- claim:PCIE14-FIG-024-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.43">07.43.</span><span class="paragraph-text">Figure 24, "Offset 2Ch: SS - Subsystem Identifiers": Device identity, revision, class code, header type, and subsystem identity describe different attributes. Find each Configuration Space field before interpretation. PI in PCIe Class Code is not NVM Protection Information.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.17</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.17, Figure 24, printed pages 20, PDF pages 20</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>SSVID</dt><dd>Subsystem Vendor ID, the PCI identifier for a subsystem vendor.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-025 -->
<details class="field-note" id="figure-PCIE14-FIG-025"><summary>PCIe Figure 25 · Offset 30h: EROM - Expansion ROM (Optional)</summary>
<!-- claim:PCIE14-FIG-025-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.44">07.44.</span><span class="paragraph-text">Figure 25, "Offset 30h: EROM - Expansion ROM (Optional)": BAR0/BAR1 halves describe the controller memory base, while other BARs, Expansion ROM, and Capabilities Pointer serve different purposes. Separate address and attribute bits; a capability-list pointer is not an MMIO data address.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.18</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.18, Figure 25, printed pages 20, PDF pages 20</p></details>

</details>
<!-- figure-table:PCIE14-FIG-026 -->
<details class="field-note" id="figure-PCIE14-FIG-026"><summary>PCIe Figure 26 · Offset 34h: CAP - Capabilities Pointer</summary>
<!-- claim:PCIE14-FIG-026-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.45">07.45.</span><span class="paragraph-text">Figure 26, "Offset 34h: CAP - Capabilities Pointer": BAR0/BAR1 halves describe the controller memory base, while other BARs, Expansion ROM, and Capabilities Pointer serve different purposes. Separate address and attribute bits; a capability-list pointer is not an MMIO data address.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.19</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.19, Figure 26, printed pages 21, PDF pages 21</p></details>

</details>
<!-- figure-table:PCIE14-FIG-027 -->
<details class="field-note" id="figure-PCIE14-FIG-027"><summary>PCIe Figure 27 · Offset 3Ch: INTR - Interrupt Information</summary>
<!-- claim:PCIE14-FIG-027-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.46">07.46.</span><span class="paragraph-text">Figure 27, "Offset 3Ch: INTR - Interrupt Information": Interrupt Information describes legacy interrupt information; the Power Management capability describes PCIe power capabilities and state. PCIe power state and NVMe Power State are different levels, even when numeric values happen to match.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.20</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.20, Figure 27, printed pages 21, PDF pages 21</p></details>

</details>
<!-- figure-table:PCIE14-FIG-028 -->
<details class="field-note" id="figure-PCIE14-FIG-028"><summary>PCIe Figure 28 · Offset 3Eh: MGNT - Minimum Grant</summary>
<!-- claim:PCIE14-FIG-028-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.47">07.47.</span><span class="paragraph-text">Figure 28, "Offset 3Eh: MGNT - Minimum Grant": These common Configuration Space fields include control, status, and compatibility fields. Follow the access types and fixed values specified by Transport. PCIe BIST is distinct from NVMe Device Self-test and does not share its result format.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.21</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.21, Figure 28, printed pages 21, PDF pages 21</p></details>

</details>
<!-- figure-table:PCIE14-FIG-029 -->
<details class="field-note" id="figure-PCIE14-FIG-029"><summary>PCIe Figure 29 · Offset 3Fh: MLAT - Maximum Latency</summary>
<!-- claim:PCIE14-FIG-029-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.48">07.48.</span><span class="paragraph-text">Figure 29, "Offset 3Fh: MLAT - Maximum Latency": These common Configuration Space fields include control, status, and compatibility fields. Follow the access types and fixed values specified by Transport. PCIe BIST is distinct from NVMe Device Self-test and does not share its result format.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.22</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.22, Figure 29, printed pages 21, PDF pages 21</p></details>

</details>
<!-- figure-table:PCIE14-FIG-030 -->
<details class="field-note" id="figure-PCIE14-FIG-030"><summary>PCIe Figure 30 · PCI Power Management Capabilities</summary>
<!-- claim:PCIE14-FIG-030-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.49">07.49.</span><span class="paragraph-text">Figure 30, "PCI Power Management Capabilities": Interrupt Information describes legacy interrupt information; the Power Management capability describes PCIe power capabilities and state. PCIe power state and NVMe Power State are different levels, even when numeric values happen to match.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.1.22</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1.22, Figure 30, printed pages 21, PDF pages 21</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>PMCAP</dt><dd>Power Management Capability, the base of the PCI power-management capability structure.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-031 -->
<details class="field-note" id="figure-PCIE14-FIG-031"><summary>PCIe Figure 31 · Offset PMCAP: PID - PCI Power Management Capability ID</summary>
<!-- claim:PCIE14-FIG-031-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.50">07.50.</span><span class="paragraph-text">Figure 31, "Offset PMCAP: PID - PCI Power Management Capability ID": Interrupt Information describes legacy interrupt information; the Power Management capability describes PCIe power capabilities and state. PCIe power state and NVMe Power State are different levels, even when numeric values happen to match.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.2.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.1, Figure 31, printed pages 21, PDF pages 21</p></details>

</details>
<!-- figure-table:PCIE14-FIG-032 -->
<details class="field-note" id="figure-PCIE14-FIG-032"><summary>PCIe Figure 32 · Offset PMCAP + 2h: PC - PCI Power Management Capabilities</summary>
<!-- claim:PCIE14-FIG-032-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.51">07.51.</span><span class="paragraph-text">Figure 32, "Offset PMCAP + 2h: PC - PCI Power Management Capabilities": Interrupt Information describes legacy interrupt information; the Power Management capability describes PCIe power capabilities and state. PCIe power state and NVMe Power State are different levels, even when numeric values happen to match.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.2.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.2, Figure 32, printed pages 22, PDF pages 22</p></details>

</details>
<!-- figure-table:PCIE14-FIG-033 -->
<details class="field-note" id="figure-PCIE14-FIG-033"><summary>PCIe Figure 33 · Offset PMCAP + 4h: PMCS - PCI Power Management Control and Status</summary>
<!-- claim:PCIE14-FIG-033-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.52">07.52.</span><span class="paragraph-text">Figure 33, "Offset PMCAP + 4h: PMCS - PCI Power Management Control and Status": Interrupt Information describes legacy interrupt information; the Power Management capability describes PCIe power capabilities and state. PCIe power state and NVMe Power State are different levels, even when numeric values happen to match.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.2.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.2.3, Figure 33, printed pages 22, PDF pages 22</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>PS</dt><dd>Power State, a controller power/performance operating point; PS0 has the highest maximum power.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-047 -->
<details class="field-note" id="figure-PCIE14-FIG-047"><summary>PCIe Figure 47 · PCI Express Capability</summary>
<!-- claim:PCIE14-FIG-047-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.53">07.53.</span><span class="paragraph-text">Figure 47, "PCI Express Capability": PCIe capabilities, control, and status describe support, configuration, and current results. Separate Link Capability limits from negotiated Link Status values. Device Control transfer settings are not directly the NVMe maximum I/O size.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5, Figure 47, printed pages 26, PDF pages 26</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>PXCAP</dt><dd>PCI Express Capability, the base of the PCIe capability structure.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-048 -->
<details class="field-note" id="figure-PCIE14-FIG-048"><summary>PCIe Figure 48 · Offset PXCAP: PXID - PCI Express Capability ID</summary>
<!-- claim:PCIE14-FIG-048-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.54">07.54.</span><span class="paragraph-text">Figure 48, "Offset PXCAP: PXID - PCI Express Capability ID": PCIe capabilities, control, and status describe support, configuration, and current results. Separate Link Capability limits from negotiated Link Status values. Device Control transfer settings are not directly the NVMe maximum I/O size.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.1, Figure 48, printed pages 26, PDF pages 26</p></details>

</details>
<!-- figure-table:PCIE14-FIG-049 -->
<details class="field-note" id="figure-PCIE14-FIG-049"><summary>PCIe Figure 49 · Offset PXCAP + 2h: PXCAP - PCI Express Capabilities</summary>
<!-- claim:PCIE14-FIG-049-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.55">07.55.</span><span class="paragraph-text">Figure 49, "Offset PXCAP + 2h: PXCAP - PCI Express Capabilities": PCIe capabilities, control, and status describe support, configuration, and current results. Separate Link Capability limits from negotiated Link Status values. Device Control transfer settings are not directly the NVMe maximum I/O size.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.2, Figure 49, printed pages 26, PDF pages 26</p></details>

</details>
<!-- figure-table:PCIE14-FIG-050 -->
<details class="field-note" id="figure-PCIE14-FIG-050"><summary>PCIe Figure 50 · Offset PXCAP + 4h: PXDCAP - PCI Express Device Capabilities</summary>
<!-- claim:PCIE14-FIG-050-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.56">07.56.</span><span class="paragraph-text">Figure 50, "Offset PXCAP + 4h: PXDCAP - PCI Express Device Capabilities": PCIe capabilities, control, and status describe support, configuration, and current results. Separate Link Capability limits from negotiated Link Status values. Device Control transfer settings are not directly the NVMe maximum I/O size.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.3, Figure 50, printed pages 26-27, PDF pages 26-27</p></details>

</details>
<!-- figure-table:PCIE14-FIG-051 -->
<details class="field-note" id="figure-PCIE14-FIG-051"><summary>PCIe Figure 51 · Offset PXCAP + 8h: PXDC - PCI Express Device Control</summary>
<!-- claim:PCIE14-FIG-051-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.57">07.57.</span><span class="paragraph-text">Figure 51, "Offset PXCAP + 8h: PXDC - PCI Express Device Control": PCIe capabilities, control, and status describe support, configuration, and current results. Separate Link Capability limits from negotiated Link Status values. Device Control transfer settings are not directly the NVMe maximum I/O size.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.4</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.4, Figure 51, printed pages 27-28, PDF pages 27-28</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>MRRS</dt><dd>Max Read Request Size, the setting limiting the size of read requests issued by a PCIe Function.</dd></div><div><dt>MPS</dt><dd>Memory Page Size, the controller memory-page-size setting; it affects queue addresses and PRP alignment.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-052 -->
<details class="field-note" id="figure-PCIE14-FIG-052"><summary>PCIe Figure 52 · Offset PXCAP + Ah: PXDS - PCI Express Device Status</summary>
<!-- claim:PCIE14-FIG-052-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.58">07.58.</span><span class="paragraph-text">Figure 52, "Offset PXCAP + Ah: PXDS - PCI Express Device Status": PCIe capabilities, control, and status describe support, configuration, and current results. Separate Link Capability limits from negotiated Link Status values. Device Control transfer settings are not directly the NVMe maximum I/O size.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.5</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.5, Figure 52, printed pages 28, PDF pages 28</p></details>

</details>
<!-- figure-table:PCIE14-FIG-053 -->
<details class="field-note" id="figure-PCIE14-FIG-053"><summary>PCIe Figure 53 · Offset PXCAP + Ch: PXLCAP - PCI Express Link Capabilities</summary>
<!-- claim:PCIE14-FIG-053-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.59">07.59.</span><span class="paragraph-text">Figure 53, "Offset PXCAP + Ch: PXLCAP - PCI Express Link Capabilities": PCIe capabilities, control, and status describe support, configuration, and current results. Separate Link Capability limits from negotiated Link Status values. Device Control transfer settings are not directly the NVMe maximum I/O size.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.6</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.6, Figure 53, printed pages 28-29, PDF pages 28-29</p></details>

</details>
<!-- figure-table:PCIE14-FIG-054 -->
<details class="field-note" id="figure-PCIE14-FIG-054"><summary>PCIe Figure 54 · Offset PXCAP + 10h: PXLC - PCI Express Link Control</summary>
<!-- claim:PCIE14-FIG-054-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.60">07.60.</span><span class="paragraph-text">Figure 54, "Offset PXCAP + 10h: PXLC - PCI Express Link Control": PCIe capabilities, control, and status describe support, configuration, and current results. Separate Link Capability limits from negotiated Link Status values. Device Control transfer settings are not directly the NVMe maximum I/O size.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.7</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.7, Figure 54, printed pages 29, PDF pages 29</p></details>

</details>
<!-- figure-table:PCIE14-FIG-055 -->
<details class="field-note" id="figure-PCIE14-FIG-055"><summary>PCIe Figure 55 · Offset PXCAP + 12h: PXLS - PCI Express Link Status</summary>
<!-- claim:PCIE14-FIG-055-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.61">07.61.</span><span class="paragraph-text">Figure 55, "Offset PXCAP + 12h: PXLS - PCI Express Link Status": PCIe capabilities, control, and status describe support, configuration, and current results. Separate Link Capability limits from negotiated Link Status values. Device Control transfer settings are not directly the NVMe maximum I/O size.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.8</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.8, Figure 55, printed pages 29, PDF pages 29</p></details>

</details>
<!-- figure-table:PCIE14-FIG-056 -->
<details class="field-note" id="figure-PCIE14-FIG-056"><summary>PCIe Figure 56 · Offset PXCAP + 24h: PXDCAP2 - PCI Express Device Capabilities 2</summary>
<!-- claim:PCIE14-FIG-056-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.62">07.62.</span><span class="paragraph-text">Figure 56, "Offset PXCAP + 24h: PXDCAP2 - PCI Express Device Capabilities 2": PCIe capabilities, control, and status describe support, configuration, and current results. Separate Link Capability limits from negotiated Link Status values. Device Control transfer settings are not directly the NVMe maximum I/O size.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.9</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.9, Figure 56, printed pages 30, PDF pages 30</p></details>

</details>
<!-- figure-table:PCIE14-FIG-057 -->
<details class="field-note" id="figure-PCIE14-FIG-057"><summary>PCIe Figure 57 · Offset PXCAP + 28h: PXDC2 - PCI Express Device Control 2</summary>
<!-- claim:PCIE14-FIG-057-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.63">07.63.</span><span class="paragraph-text">Figure 57, "Offset PXCAP + 28h: PXDC2 - PCI Express Device Control 2": PCIe capabilities, control, and status describe support, configuration, and current results. Separate Link Capability limits from negotiated Link Status values. Device Control transfer settings are not directly the NVMe maximum I/O size.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.10</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.10, Figure 57, printed pages 30-31, PDF pages 30-31</p></details>

</details>
<!-- figure-table:PCIE14-FIG-058 -->
<details class="field-note" id="figure-PCIE14-FIG-058"><summary>PCIe Figure 58 · Advanced Error Reporting Capability (Optional)</summary>
<!-- claim:PCIE14-FIG-058-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.64">07.64.</span><span class="paragraph-text">Figure 58, "Advanced Error Reporting Capability (Optional)": AER Status reports errors, Mask controls reporting, Severity classifies uncorrectable errors, and Header/Prefix logs provide transaction context. Select correctable or uncorrectable class before pairing fields for the same error.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.5.10</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.5.10, Figure 58, printed pages 31, PDF pages 31</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>AERCAP</dt><dd>Advanced Error Reporting Capability, the base of the AER extended-capability structure.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-059 -->
<details class="field-note" id="figure-PCIE14-FIG-059"><summary>PCIe Figure 59 · Offset AERCAP: AERID - AER Capability ID</summary>
<!-- claim:PCIE14-FIG-059-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.65">07.65.</span><span class="paragraph-text">Figure 59, "Offset AERCAP: AERID - AER Capability ID": AER Status reports errors, Mask controls reporting, Severity classifies uncorrectable errors, and Header/Prefix logs provide transaction context. Select correctable or uncorrectable class before pairing fields for the same error.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.6.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.1, Figure 59, printed pages 31, PDF pages 31</p></details>

</details>
<!-- figure-table:PCIE14-FIG-060 -->
<details class="field-note" id="figure-PCIE14-FIG-060"><summary>PCIe Figure 60 · Offset AERCAP + 4: AERUCES - AER Uncorrectable Error Status Register</summary>
<!-- claim:PCIE14-FIG-060-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.66">07.66.</span><span class="paragraph-text">Figure 60, "Offset AERCAP + 4: AERUCES - AER Uncorrectable Error Status Register": AER Status reports errors, Mask controls reporting, Severity classifies uncorrectable errors, and Header/Prefix logs provide transaction context. Select correctable or uncorrectable class before pairing fields for the same error.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.6.2</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.2, Figure 60, printed pages 31-32, PDF pages 31-32</p></details>

</details>
<!-- figure-table:PCIE14-FIG-061 -->
<details class="field-note" id="figure-PCIE14-FIG-061"><summary>PCIe Figure 61 · Offset AERCAP + 8: AERUCEM - AER Uncorrectable Error Mask Register</summary>
<!-- claim:PCIE14-FIG-061-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.67">07.67.</span><span class="paragraph-text">Figure 61, "Offset AERCAP + 8: AERUCEM - AER Uncorrectable Error Mask Register": AER Status reports errors, Mask controls reporting, Severity classifies uncorrectable errors, and Header/Prefix logs provide transaction context. Select correctable or uncorrectable class before pairing fields for the same error.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.6.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.3, Figure 61, printed pages 32, PDF pages 32</p></details>

</details>
<!-- figure-table:PCIE14-FIG-062 -->
<details class="field-note" id="figure-PCIE14-FIG-062"><summary>PCIe Figure 62 · Offset AERCAP + Ch: AERUCESEV - AER Uncorrectable Error Severity Register</summary>
<!-- claim:PCIE14-FIG-062-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.68">07.68.</span><span class="paragraph-text">Figure 62, "Offset AERCAP + Ch: AERUCESEV - AER Uncorrectable Error Severity Register": AER Status reports errors, Mask controls reporting, Severity classifies uncorrectable errors, and Header/Prefix logs provide transaction context. Select correctable or uncorrectable class before pairing fields for the same error.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.6.4</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.4, Figure 62, printed pages 32-33, PDF pages 32-33</p></details>

</details>
<!-- figure-table:PCIE14-FIG-063 -->
<details class="field-note" id="figure-PCIE14-FIG-063"><summary>PCIe Figure 63 · Offset AERCAP + 10h: AERCES - AER Correctable Error Status Register</summary>
<!-- claim:PCIE14-FIG-063-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.69">07.69.</span><span class="paragraph-text">Figure 63, "Offset AERCAP + 10h: AERCES - AER Correctable Error Status Register": AER Status reports errors, Mask controls reporting, Severity classifies uncorrectable errors, and Header/Prefix logs provide transaction context. Select correctable or uncorrectable class before pairing fields for the same error.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.6.5</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.5, Figure 63, printed pages 33, PDF pages 33</p></details>

</details>
<!-- figure-table:PCIE14-FIG-064 -->
<details class="field-note" id="figure-PCIE14-FIG-064"><summary>PCIe Figure 64 · Offset AERCAP + 14h: AERCEM - AER Correctable Error Mask Register</summary>
<!-- claim:PCIE14-FIG-064-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.70">07.70.</span><span class="paragraph-text">Figure 64, "Offset AERCAP + 14h: AERCEM - AER Correctable Error Mask Register": AER Status reports errors, Mask controls reporting, Severity classifies uncorrectable errors, and Header/Prefix logs provide transaction context. Select correctable or uncorrectable class before pairing fields for the same error.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.6.6</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.6, Figure 64, printed pages 33, PDF pages 33</p></details>

</details>
<!-- figure-table:PCIE14-FIG-065 -->
<details class="field-note" id="figure-PCIE14-FIG-065"><summary>PCIe Figure 65 · Offset AERCAP + 18h: AERCC - AER Capabilities and Control Register</summary>
<!-- claim:PCIE14-FIG-065-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.71">07.71.</span><span class="paragraph-text">Figure 65, "Offset AERCAP + 18h: AERCC - AER Capabilities and Control Register": AER Status reports errors, Mask controls reporting, Severity classifies uncorrectable errors, and Header/Prefix logs provide transaction context. Select correctable or uncorrectable class before pairing fields for the same error.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.6.7</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.7, Figure 65, printed pages 34, PDF pages 34</p></details>

</details>
<!-- figure-table:PCIE14-FIG-066 -->
<details class="field-note" id="figure-PCIE14-FIG-066"><summary>PCIe Figure 66 · Offset AERCAP + 1Ch: AERHL - AER Header Log Register</summary>
<!-- claim:PCIE14-FIG-066-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.72">07.72.</span><span class="paragraph-text">Figure 66, "Offset AERCAP + 1Ch: AERHL - AER Header Log Register": AER Status reports errors, Mask controls reporting, Severity classifies uncorrectable errors, and Header/Prefix logs provide transaction context. Select correctable or uncorrectable class before pairing fields for the same error.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.6.8</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.8, Figure 66, printed pages 34, PDF pages 34</p></details>

</details>
<!-- figure-table:PCIE14-FIG-067 -->
<details class="field-note" id="figure-PCIE14-FIG-067"><summary>PCIe Figure 67 · Offset AERCAP + 38h: AERTLP - AER TLP Prefix Log Register (Optional)</summary>
<!-- claim:PCIE14-FIG-067-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.73">07.73.</span><span class="paragraph-text">Figure 67, "Offset AERCAP + 38h: AERTLP - AER TLP Prefix Log Register (Optional)": AER Status reports errors, Mask controls reporting, Severity classifies uncorrectable errors, and Header/Prefix logs provide transaction context. Select correctable or uncorrectable class before pairing fields for the same error.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>TLP</dt><dd>Transaction Layer Packet, a packet carried by the PCIe transaction layer.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.6.9</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.6.9, Figure 67, printed pages 35, PDF pages 35</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>TLP</dt><dd>Transaction Layer Packet, a packet carried by the PCIe transaction layer.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-069 -->
<details class="field-note" id="figure-PCIE14-FIG-069"><summary>PCIe Figure 69 · NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure</summary>
<!-- claim:PCIE14-FIG-069-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.74">07.74.</span><span class="paragraph-text">Figure 69, "NVMe TDISP DEVICE_INTERFACE_REPORT Reporting Structure": DEVICE_INTERFACE_REPORT defines a device-interface reporting structure. Follow each region’s length and definition and distinguish interface information from PCIe error logs; it is not another CQE layout.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>TDISP</dt><dd>TEE Device Interface Security Protocol, a PCIe security protocol related to platform isolation and device-interface state.</dd></div></dl><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.10</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.10, Figure 69, printed pages 38-39, PDF pages 38-39</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-eom"><h3>Figure group 06 · Receiver eye-opening measurement data layout</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.75">07.75.</span><span class="paragraph-text">Read the result layout from the header and follow lane descriptors to measurement data. Establish scales and legends before interpreting positions. Relate Printable Eye to numeric results rather than inferring unspecified performance from pixel widths.</span></p>
<a class="reading-link" href="#module-eom">Return to the explanation and example</a>
<!-- figure-table:PCIE14-FIG-070 -->
<details class="field-note" id="figure-PCIE14-FIG-070"><summary>PCIe Figure 70 · Get Log Page - Log Page Identifiers</summary>
<!-- claim:PCIE14-FIG-070-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.76">07.76.</span><span class="paragraph-text">Figure 70, "Get Log Page - Log Page Identifiers": Eye-measurement logs use parameters and identifiers to select requests, a header to describe layout, and lane descriptors to find results. Total length, lane count, and measurement status are separate; entry count does not establish measurement quality.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.9</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9, Figure 70, printed pages 39, PDF pages 39</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CSI</dt><dd>I/O Command Set Identifier: selects an I/O command set; NVM uses 00h.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-071 -->
<details class="field-note" id="figure-PCIE14-FIG-071"><summary>PCIe Figure 71 · Size of Physical Interface Receiver Eye Opening Measurement Log Page</summary>
<!-- claim:PCIE14-FIG-071-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.77">07.77.</span><span class="paragraph-text">Figure 71, "Size of Physical Interface Receiver Eye Opening Measurement Log Page": Eye-measurement logs use parameters and identifiers to select requests, a header to describe layout, and lane descriptors to find results. Total length, lane count, and measurement status are separate; entry count does not establish measurement quality.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.9.1.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 71, printed pages 40, PDF pages 40</p></details>

</details>
<!-- figure-table:PCIE14-FIG-072 -->
<details class="field-note" id="figure-PCIE14-FIG-072"><summary>PCIe Figure 72 · Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field</summary>
<!-- claim:PCIE14-FIG-072-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.78">07.78.</span><span class="paragraph-text">Figure 72, "Physical Interface Receiver Eye Opening Measurement Log Specific Parameter Field": Eye-measurement logs use parameters and identifiers to select requests, a header to describe layout, and lane descriptors to find results. Total length, lane count, and measurement status are separate; entry count does not establish measurement quality.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.9.1.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 72, printed pages 40-41, PDF pages 40-41</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>LPOL</dt><dd>Log Page Offset Lower, the low 32 bits of the Get Log Page byte offset.</dd></div><div><dt>LPOU</dt><dd>Log Page Offset Upper, the high 32 bits of the Get Log Page byte offset.</dd></div><div><dt>EOM</dt><dd>Eye Opening Measurement, the procedure and log data for measuring a PCIe receiver eye opening.</dd></div></dl>
</details>
<!-- figure-table:PCIE14-FIG-073 -->
<details class="field-note" id="figure-PCIE14-FIG-073"><summary>PCIe Figure 73 · Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field</summary>
<!-- claim:PCIE14-FIG-073-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.79">07.79.</span><span class="paragraph-text">Figure 73, "Physical Interface Receiver Eye Opening Measurement Log Specific Identifier Field": Eye-measurement logs use parameters and identifiers to select requests, a header to describe layout, and lane descriptors to find results. Total length, lane count, and measurement status are separate; entry count does not establish measurement quality.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.9.1.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 73, printed pages 41, PDF pages 41</p></details>

</details>
<!-- figure-table:PCIE14-FIG-074 -->
<details class="field-note" id="figure-PCIE14-FIG-074"><summary>PCIe Figure 74 · Physical Interface Receiver Eye Opening Measurement Log Page</summary>
<!-- claim:PCIE14-FIG-074-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.80">07.80.</span><span class="paragraph-text">Figure 74, "Physical Interface Receiver Eye Opening Measurement Log Page": Eye-measurement logs use parameters and identifiers to select requests, a header to describe layout, and lane descriptors to find results. Total length, lane count, and measurement status are separate; entry count does not establish measurement quality.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.9.1.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 74, printed pages 41, PDF pages 41</p></details>

</details>
<!-- figure-table:PCIE14-FIG-075 -->
<details class="field-note" id="figure-PCIE14-FIG-075"><summary>PCIe Figure 75 · EOM Header</summary>
<!-- claim:PCIE14-FIG-075-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.81">07.81.</span><span class="paragraph-text">Figure 75, "EOM Header": Eye-measurement logs use parameters and identifiers to select requests, a header to describe layout, and lane descriptors to find results. Total length, lane count, and measurement status are separate; entry count does not establish measurement quality.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.9.1.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 75, printed pages 42-43, PDF pages 42-43</p></details>

</details>
<!-- figure-table:PCIE14-FIG-076 -->
<details class="field-note" id="figure-PCIE14-FIG-076"><summary>PCIe Figure 76 · EOM Lane Descriptor</summary>
<!-- claim:PCIE14-FIG-076-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.82">07.82.</span><span class="paragraph-text">Figure 76, "EOM Lane Descriptor": Eye-measurement logs use parameters and identifiers to select requests, a header to describe layout, and lane descriptors to find results. Total length, lane count, and measurement status are separate; entry count does not establish measurement quality.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.9.1.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 76, printed pages 43-45, PDF pages 43-45</p></details>

</details>
<!-- figure-table:PCIE14-FIG-077 -->
<details class="field-note" id="figure-PCIE14-FIG-077"><summary>PCIe Figure 77 · Example of an Eve Diagram in the Printable Eye Field</summary>
<!-- claim:PCIE14-FIG-077-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.83">07.83.</span><span class="paragraph-text">Figure 77, "Example of an Eve Diagram in the Printable Eye Field": Printable Eye presents measurement results as a readable eye diagram. Establish measurement conditions and coordinate scales before comparison; character or pixel width does not define an unspecified I/O performance metric.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.9.1.1</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.9.1.1, Figure 77, printed pages 46, PDF pages 46</p></details>

</details>
<!-- figure-table:PCIE14-FIG-068 -->
<details class="field-note" id="figure-PCIE14-FIG-068"><summary>PCIe Figure 68 · Example of an Eve Diagram in the Printable Eye Field</summary>
<!-- claim:PCIE14-FIG-068-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.84">07.84.</span><span class="paragraph-text">Figure 68, "Example of an Eve Diagram in the Printable Eye Field": Printable Eye presents measurement results as a readable eye diagram. Establish measurement conditions and coordinate scales before comparison; character or pixel width does not define an unspecified I/O performance metric.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.9</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.9, Figure 68, printed pages 37, PDF pages 37</p></details>

</details>
</div>
<!-- claim:PCIE14-KEYWORDS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.85">07.85.</span><span class="paragraph-text">The force of shall, may, and should remains defined by Base 2.4; a Transport summary must not strengthen or weaken the normative language.</span></p><details class="source-note"><summary>Sources: Base 2.4 §1.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §1.4.1, printed pages 2-3, PDF pages 28-29</p></details>
<!-- claim:PCIE14-RESET -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.86">07.86.</span><span class="paragraph-text">PCIe reset sources include Base controller/reset flows and PCIe-level resets. Recovery logic uses the reset type to determine controller-property, queue, and PCI-configuration state.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.3</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.3, printed pages 11-12, PDF pages 11-12</p></details>
<!-- claim:PCIE14-SECURITY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.87">07.87.</span><span class="paragraph-text">Power-loss signaling, confidential computing, and TDISP map platform events or isolation state to NVMe-controller behavior. Implementation still requires external PCIe/TDISP specifications not supplied for this report.</span></p><details class="source-note"><summary>Sources: PCIe Transport 1.4 §3.8.8-3.8.10</summary><p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.8-3.8.10, printed pages 35-39, PDF pages 35-39</p></details>
</section>
</details>
<section id="knowledge-check"><h2 id="review-questions">Check your understanding</h2>
<!-- qa:pcie-transport-1.4-memory-mmio -->
<details class="review-question" id="qa-pcie-transport-1.4-memory-mmio"><summary>1. What roles do PCIe MMIO properties and host-memory queues play?</summary>
<div data-qa-answer="pcie-transport-1.4-memory-mmio"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="08.01">08.01.</span><span class="paragraph-text">Properties provide controller configuration, status, and queue notification interfaces. Queues carry command and completion entries. Separating the control interface from those structures explains how submission works.</span></p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1, printed pages 9-10, PDF pages 9-10</p>
<p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.2, printed pages 11, PDF pages 11</p>
</details></details>
<!-- qa:pcie-transport-1.4-doorbell-stride -->
<details class="review-question" id="qa-pcie-transport-1.4-doorbell-stride"><summary>2. Why is it unsafe to assume adjacent doorbells are always 4 bytes apart?</summary>
<div data-qa-answer="pcie-transport-1.4-doorbell-stride"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="08.02">08.02.</span><span class="paragraph-text">CAP.DSTRD determines the spacing: stride is 2^(2+DSTRD) bytes. It is 4 bytes only when DSTRD=0; queue ID also determines the SQ Tail and CQ Head locations.</span></p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.1.2.1-3.1.2.2, printed pages 10-11, PDF pages 10-11</p>
</details></details>
<!-- qa:pcie-transport-1.4-interrupt -->
<details class="review-question" id="qa-pcie-transport-1.4-interrupt"><summary>3. Why must the host inspect the CQ after an interrupt?</summary>
<div data-qa-answer="pcie-transport-1.4-interrupt"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="08.03">08.03.</span><span class="paragraph-text">The interrupt is a notification; CQEs contain command identity and completion status. One notification need not correspond to one completion entry, so the host processes valid entries according to queue progress.</span></p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.5, printed pages 13-16, PDF pages 13-16</p>
<p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.4, printed pages 12-13, PDF pages 12-13</p>
</details></details>
<!-- qa:pcie-transport-1.4-error-layer -->
<details class="review-question" id="qa-pcie-transport-1.4-error-layer"><summary>4. Why distinguish NVMe command status from PCIe error reporting?</summary>
<div data-qa-answer="pcie-transport-1.4-error-layer"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="08.04">08.04.</span><span class="paragraph-text">The former describes command processing; the latter describes transport and device-level errors. They can be related, but they address different objects. Success in one layer does not establish the state of every layer.</span></p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.7, printed pages 16, PDF pages 16</p>
<p>Source: NVME-PCIE-TRANSPORT-1.4, Rev. 1.4, §3.8.1-3.8.7, printed pages 16-35, PDF pages 16-35</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>Specification editions</summary><p>NVM Express NVMe over PCIe Transport Specification, Revision 1.4</p><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
