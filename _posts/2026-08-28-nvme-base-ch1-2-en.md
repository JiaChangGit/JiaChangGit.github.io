---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4 Chapters 1-2: Specification Language, PCIe Queues, and Storage Model"
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
[繁體中文]({% post_url 2026-08-28-nvme-base-ch1-2-zh-tw %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">NVMe is an interface between a host and a storage controller. This note establishes how the host submits commands, how the controller reports results, and what namespaces, controllers, and NVM subsystems represent. These concepts provide the foundation for later commands and fields.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div><div><dt>NVMe</dt><dd>Non-Volatile Memory Express, the specification family for a host interface to a non-volatile-memory subsystem.</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl>
<h2 id="main-ideas">The main ideas</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>Specification responsibilities</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">Distinguish what Base, Transport, and I/O Command Set specifications define.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl></article>
<article><span class="axis-number">02</span><h3>Command round trips</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">Understand cooperation between host and controller through submission and completion queues.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div></dl></article>
<article><span class="axis-number">03</span><h3>Storage objects and paths</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">Distinguish namespaces, controllers, and subsystems, including multiple access paths.</span></p></article>
</div>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">The host includes the operating system and driver; the controller provides the NVMe interface accessible to that host. NVMe describes host-visible behavior, which does not directly specify the SSD’s physical NAND organization.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express, the specification family for a host interface to a non-volatile-memory subsystem.</dd></div></dl>
<div class="overview-connections"><h3>Connecting the main ideas</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.03">00.03.</span><span class="paragraph-text">Establish hosts, controllers, and namespaces, then follow command submission and completion. The specification family assigns responsibility for those relationships, while numeric conventions and units provide the tools for reading later fields.</span></p>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.04">00.04.</span><span class="paragraph-text">The aim is to draw the path from host to storage, explain where commands and data reside, and distinguish multiple paths to one storage object from sharing by multiple hosts. Later reports apply these foundations to specific mechanisms.</span></p>
</div>
</section>
<section class="lesson" id="module-family"><h2 id="heading-family"><span class="section-number">01</span> Roles of Base, Command Set, and Transport</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">When a command, register, or data format appears, the first question is not merely where it is found, but which specification owns the definition. Base supplies the common protocol, the Transport adds the PCIe binding, and an I/O Command Set defines namespace data operations. The boxes in Figure 1 show applicability, not mandatory packet traversal through a stack.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div><div><dt>PCIe</dt><dd>PCI Express, the transport and device interconnect used by an NVMe memory-based controller.</dd></div><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl>
<details class="technical-note"><summary>Full rules: Roles of Base, Command Set, and Transport</summary>
<!-- claim:BASE12-FAMILY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">The Base Specification defines the common NVMe protocol; a Transport Specification binds it to a transport, and an I/O Command Set Specification extends commands and data structures. This is an applicability relationship, not a protocol stack.</span></p><details class="source-note"><summary>Sources: Base 2.4 §1.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §1.1.1, printed pages 1, PDF pages 27</p></details>
<!-- claim:BASE12-COMMANDSET -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">The Admin Command Set manages controllers and queues; an I/O Command Set defines data operations on namespaces. Base describes common mechanisms, while each I/O Command Set Specification describes command semantics.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §2.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.2, printed pages 33, PDF pages 59</p></details>
</details>
<div class="table-wrap"><table><caption>Roles of Base, Command Set, and Transport</caption><thead><tr><th scope="col">Specification</th><th scope="col">Content defined</th><th scope="col">Relationship to other specifications</th></tr></thead><tbody><tr><td>Base</td><td>Common commands, queues, status, and structures</td><td>Do not assume it owns every PCIe-register detail</td></tr><tr><td>PCIe Transport</td><td>BARs, MMIO, doorbells, interrupts, and PCIe-specific behavior</td><td>It does not override Base in a conflict</td></tr><tr><td>I/O Command Set</td><td>Specific namespace I/O commands and extensions</td><td>It does not redefine the transport</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div><div><dt>MMIO</dt><dd>Memory-Mapped I/O, access to device registers through CPU memory operations.</dd></div><div><dt>PCIe</dt><dd>PCI Express, the transport and device interconnect used by an NVMe memory-based controller.</dd></div></dl>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.04">01.04.</span><span class="paragraph-text">To implement Firmware Image Download, read Base for command fields and completion status, then use the PCIe Transport for Admin-command data-pointer and memory-access constraints. The Admin command can be understood without an I/O Command Set, while the PCIe Transport alone does not provide complete command semantics.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div></dl></aside>
<a class="reading-link" href="#reading-family">Read the related specification figures → Roles of Base, Command Set, and Transport</a>
</section>
<section class="lesson" id="module-objects"><h2 id="heading-objects"><span class="section-number">02</span> Namespaces, controllers, and access paths</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">A namespace is the formatted capacity actually accessed by the host, while capacity management, endurance, reclamation, and paths live at different levels. Figures 11-18 describe containment using NVM Sets or Reclaim Groups; Figures 19-22 instead show controllers, ports, paths, and PCIe Functions. The two groups answer different questions and must not be collapsed into a falsely one-to-one tree.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl>
<details class="technical-note"><summary>Full rules: Namespaces, controllers, and access paths</summary>
<!-- claim:BASE12-STORAGE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">The storage model expresses containment through the NVM subsystem, domain, Endurance Group, NVM Set or Reclaim Group, Reclaim Unit, and namespace. A namespace is the formatted capacity a host accesses through a controller.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Endurance Group</dt><dd>Endurance Group, a group of NVM resources for isolating and reporting endurance-related state.</dd></div><div><dt>NVM subsystem</dt><dd>NVM subsystem, the NVMe system boundary containing controllers, ports, namespaces, and non-volatile storage resources.</dd></div><div><dt>Reclaim Group</dt><dd>Reclaim Group, a set of non-volatile storage resources with shared reclamation behavior.</dd></div><div><dt>Reclaim Unit</dt><dd>Reclaim Unit, a smaller management granularity used when a controller reclaims media.</dd></div><div><dt>NVM Set</dt><dd>NVM Set, a capacity grouping that associates namespaces with a managed set of NVM resources.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §2.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, printed pages 26-33, PDF pages 52-59</p></details>
<!-- claim:BASE12-SUBSYSTEM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">Controllers, ports, namespaces, and PCI Functions are distinct objects. An NSID is a controller-visible handle for a namespace, not the namespace itself.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NSID</dt><dd>Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §2.3.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.3, printed pages 33-35, PDF pages 59-61</p></details>
<!-- claim:BASE12-MULTIPATH -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.04">02.04.</span><span class="paragraph-text">Multi-path I/O provides two or more independent paths from one host to one namespace; namespace sharing lets two or more hosts access one shared namespace through different controllers. Both require at least two controllers.</span></p><details class="source-note"><summary>Sources: Base 2.4 §2.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, printed pages 35-37, PDF pages 61-63</p></details>
<!-- claim:BASE12-ASYMMETRY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.05">02.05.</span><span class="paragraph-text">With multi-path or sharing, controllers need not provide identical access characteristics to the same namespace; the host may select paths using the state reported by each controller.</span></p><details class="source-note"><summary>Sources: Base 2.4 §2.4.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.4.2, printed pages 37, PDF pages 63</p></details>
</details>
<div class="table-wrap"><table><caption>Namespaces, controllers, and access paths</caption><thead><tr><th scope="col">Access arrangement</th><th scope="col">Hosts and storage objects involved</th><th scope="col">Problem addressed</th></tr></thead><tbody><tr><td>Multi-path I/O</td><td>One host and one namespace with two or more independent paths</td><td>Focus: path redundancy</td></tr><tr><td>Namespace sharing</td><td>Two or more hosts access one shared namespace</td><td>Focus: host ownership and coordination</td></tr><tr><td>SR-IOV</td><td>One PCIe device exposes PFs/VFs</td><td>A PCIe Function need not be an independent subsystem</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>SR-IOV</dt><dd>Single Root I/O Virtualization, a PCIe capability that exposes one PF and multiple VFs from one device.</dd></div></dl>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.06">02.06.</span><span class="paragraph-text">Informative example: host A accesses namespace X through controllers 1 and 2, creating multi-path I/O. When host B also accesses the same namespace X through controller 2, namespace sharing is present as well. NSIDs may differ between controllers, so cross-controller comparison begins with namespace identity rather than raw NSID equality.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NSID</dt><dd>Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself.</dd></div></dl></aside>
<a class="reading-link" href="#reading-objects">Read the related specification figures → Namespaces, controllers, and access paths</a>
</section>
<section class="lesson" id="module-queues"><h2 id="heading-queues"><span class="section-number">03</span> Command submission and completion</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">The host does not write a command directly into the controller. It builds an SQE in memory and publishes a new SQ tail; the controller fetches and executes the command, then places a CQE into a CQ. The 1:1 and n:1 distinction in Figures 6 and 7 concerns whether multiple SQs share one CQ, not whether commands share one SQE.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div><div><dt>SQE</dt><dd>Submission Queue Entry, one command structure in an SQ.</dd></div><div><dt>CQ</dt><dd>Completion Queue, the queue into which a controller posts command completions.</dd></div><div><dt>SQ</dt><dd>Submission Queue, the queue into which the host places commands.</dd></div></dl>
<figure><figcaption><strong>One command round trip</strong></figcaption><ol class="flow-steps"><li>The host writes a command to the Submission Queue (SQ).</li><li>The host updates the SQ Tail Doorbell to announce new work.</li><li>The controller retrieves and executes the command, then writes its result to the Completion Queue (CQ).</li><li>The host reads the CQE and updates the CQ Head Doorbell to release consumed entries.</li></ol><figcaption>Queues hold commands and results; doorbells announce updated queue positions.</figcaption></figure>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div><div><dt>CQ</dt><dd>Completion Queue, the queue into which a controller posts command completions.</dd></div><div><dt>SQ</dt><dd>Submission Queue, the queue into which the host places commands.</dd></div></dl>
<details class="technical-note"><summary>Full rules: Command submission and completion</summary>
<!-- claim:BASE12-QUEUE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span><span class="paragraph-text">In the PCIe memory-based model, Submission and Completion Queues reside in memory. Multiple I/O Submission Queues may share an I/O Completion Queue, while the Admin queue pair remains one-to-one.</span></p><details class="source-note"><summary>Sources: Base 2.4 §2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.1, printed pages 21-23, PDF pages 47-49</p></details>
</details>
<div class="table-wrap"><table><caption>Command submission and completion</caption><thead><tr><th scope="col">Queue arrangement</th><th scope="col">SQ-to-CQ relationship</th><th scope="col">Identifying a completed command</th></tr></thead><tbody><tr><td>Admin queue pair</td><td>One Admin SQ to one Admin CQ</td><td>Initialization and management path</td></tr><tr><td>I/O 1:1</td><td>One I/O SQ to one I/O CQ</td><td>Simple tracking and clear isolation</td></tr><tr><td>I/O n:1</td><td>Multiple I/O SQs share one I/O CQ</td><td>Merged completion path; SQID/CID still recover the command</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>SQID</dt><dd>Submission Queue Identifier, the numeric identifier of the SQ containing a command.</dd></div><div><dt>CID</dt><dd>Command Identifier, used with the SQ identifier to identify an outstanding command.</dd></div></dl>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.03">03.03.</span><span class="paragraph-text">Informative example: SQ 3 and SQ 4 share CQ 2. Both commands may use CID 5 and remain distinguishable because the identity key is (SQID, CID): (3,5) and (4,5). An outstanding-command map keyed only by CID can associate a completion with the wrong command.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SQID</dt><dd>Submission Queue Identifier, the numeric identifier of the SQ containing a command.</dd></div><div><dt>CID</dt><dd>Command Identifier, used with the SQ identifier to identify an outstanding command.</dd></div></dl></aside>
<a class="reading-link" href="#reading-queues">Read the related specification figures → Command submission and completion</a>
</section>
<section class="lesson" id="module-numbers"><h2 id="heading-numbers"><span class="section-number">04</span> Numeric encodings and units</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">Before reading any raw value, establish its unit and encoding. A zero-based count of 3 may represent 4 units; an index selects a list item, while an offset measures distance from a start. They are not interchangeable.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>zero-based</dt><dd>zero-based: numbering starts at zero, so raw=3 can mean the fourth item or four units; the field definition still decides which.</dd></div><div><dt>raw value</dt><dd>raw value: the value read directly from a field before applying zero-based, unit, or scaling rules; confirm the definition before converting it.</dd></div><div><dt>offset</dt><dd>offset: a displacement measured from a stated start. It answers “how far from the start,” unlike an index.</dd></div><div><dt>index</dt><dd>index: selects an item or format in a list. It answers “which one,” not “how far from the start.”</dd></div></dl>
<details class="technical-note"><summary>Full rules: Numeric encodings and units</summary>
<!-- claim:BASE12-NUMBERS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">A value is interpreted together with its radix and units. Hexadecimal uses the h suffix, binary uses b, and decimal may omit d. Decimal and binary capacity prefixes represent different multipliers.</span></p><details class="source-note"><summary>Sources: Base 2.4 §1.4.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §1.4.2, printed pages 3-5, PDF pages 29-31</p></details>
<!-- claim:BASE12-DWORD -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.03">04.03.</span><span class="paragraph-text">NVMe expresses field locations in bytes, words, and dwords. A word is two bytes and a dword is four bytes; field reading the fields starts by confirming byte and bit numbering.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Dword (double word): 32 bits, or 4 bytes. A word is 16 bits; for example, a zero-based dword count of 3 represents 4 Dwords, or 16 bytes.</dd></div><div><dt>word</dt><dd>word: 16 bits, or 2 bytes. It is half a Dword; a field length must be read with its unit.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §1.4.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §1.4.3, printed pages 5, PDF pages 31</p></details>
</details>
<div class="table-wrap"><table><caption>Numeric encodings and units</caption><thead><tr><th scope="col">Field or notation</th><th scope="col">Interpreted values value</th><th scope="col">Basis for the interpretation</th></tr></thead><tbody><tr><td>1000</td><td>Decimal 1000</td><td>No b/h suffix means decimal</td></tr><tr><td>1000b</td><td>Binary value 8</td><td>b is a radix marker, not a bit unit</td></tr><tr><td>1000h</td><td>Hexadecimal value 4096</td><td>Common for offsets and register values</td></tr><tr><td>NUMD=0</td><td>One actual dword</td><td>Add one only when the field is explicitly zero-based</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>zero-based</dt><dd>zero-based: numbering starts at zero, so raw=3 can mean the fourth item or four units; the field definition still decides which.</dd></div><div><dt>Dword</dt><dd>Dword (double word): 32 bits, or 4 bytes. A word is 16 bits; for example, a zero-based dword count of 3 represents 4 Dwords, or 16 bytes.</dd></div><div><dt>NUMD</dt><dd>Number of Dwords, a zero-based transfer-dword count; actual bytes = (NUMD + 1) × 4.</dd></div></dl>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.04">04.04.</span><span class="paragraph-text">Informative example: a 512-byte transfer contains 512 / 4 = 128 dwords. If NUMD is zero-based, the encoded value is 128 - 1 = 127 = 007Fh. Treating 007Fh as a byte count under-allocates the buffer; forgetting the subtraction requests 129 dwords.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NUMD</dt><dd>Number of Dwords, a zero-based transfer-dword count; actual bytes = (NUMD + 1) × 4.</dd></div></dl></aside>
<a class="reading-link" href="#reading-numbers">Read the related specification figures → Numeric encodings and units</a>
</section>
<details class="figure-reading-fold"><summary>Expand figure teaching: read source figures by concept</summary>
<section id="figure-reading"><h2><span class="section-number">05</span> Reading the specification figures</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span><span class="paragraph-text">The specification figures below are grouped by concept. Each group explains the reading order and question to resolve, followed by the fields or behavior described by each figure. Follow links from the lessons or use this section to connect fields to complete operations.</span></p>
<div class="figure-reading-group" id="reading-family"><h3>Figure group 01 · Roles of Base, Command Set, and Transport</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.02">05.02.</span><span class="paragraph-text">The specification-family diagram connects responsibilities; its arrows are not an execution sequence. Classify an operation into common format, command behavior, and transport mechanism before finding the corresponding documents.</span></p>
<a class="reading-link" href="#module-family">Return to the explanation and example</a>
<!-- figure-table:BASE12-FIG-001 -->
<details class="field-note" id="figure-BASE12-FIG-001"><summary>Base Figure 1 · NVMe Family of Specifications</summary>
<!-- claim:BASE12-FIG-001-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.03">05.03.</span><span class="paragraph-text">Figure 1, "NVMe Family of Specifications": Base defines common commands and structures, Transport defines exchange mechanisms, and an I/O Command Set defines operations on its storage data. Place the question at the appropriate layer before following references to supporting layers.</span></p><details class="source-note"><summary>Sources: Base 2.4 §1.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §1.1.1, Figure 1, printed pages 1, PDF pages 27</p></details>

</details>
<!-- figure-table:BASE12-FIG-005 -->
<details class="field-note" id="figure-BASE12-FIG-005"><summary>Base Figure 5 · Types of NVMe Command Sets</summary>
<!-- claim:BASE12-FIG-005-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.04">05.04.</span><span class="paragraph-text">Figure 5, "Types of NVMe Command Sets": Base defines common commands and structures, Transport defines exchange mechanisms, and an I/O Command Set defines operations on its storage data. Place the question at the appropriate layer before following references to supporting layers.</span></p><details class="source-note"><summary>Sources: Base 2.4 §2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2, Figure 5, printed pages 21, PDF pages 47</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-objects"><h3>Figure group 02 · Namespaces, controllers, and access paths</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.05">05.05.</span><span class="paragraph-text">Find the namespace first, then follow connections to controllers and hosts. Multiple paths to one object are distinct from multiple hosts sharing that object. SR-IOV diagrams separately describe the presentation of PCIe Functions.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SR-IOV</dt><dd>Single Root I/O Virtualization, a PCIe capability that exposes one PF and multiple VFs from one device.</dd></div></dl>
<a class="reading-link" href="#module-objects">Return to the explanation and example</a>
<!-- figure-table:BASE12-FIG-011 -->
<details class="field-note" id="figure-BASE12-FIG-011"><summary>Base Figure 11 · Simple NVM Storage Hierarchy with NVM Sets</summary>
<!-- claim:BASE12-FIG-011-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.06">05.06.</span><span class="paragraph-text">Figure 11, "Simple NVM Storage Hierarchy with NVM Sets": NVM Sets group relationships between storage resources and namespaces. Establish namespace membership before interpreting Set-aware commands. Multiple namespaces do not imply the same number of independent storage devices.</span></p><details class="source-note"><summary>Sources: Base 2.4 §2.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 11, printed pages 27, PDF pages 53</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM Set</dt><dd>NVM Set, a capacity grouping that associates namespaces with a managed set of NVM resources.</dd></div></dl>
</details>
<!-- figure-table:BASE12-FIG-012 -->
<details class="field-note" id="figure-BASE12-FIG-012"><summary>Base Figure 12 · Simple NVM Storage Hierarchy with One Reclaim Group</summary>
<!-- claim:BASE12-FIG-012-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.07">05.07.</span><span class="paragraph-text">Figure 12, "Simple NVM Storage Hierarchy with One Reclaim Group": Reclaim Group and placement diagrams show how storage resources are grouped and shared. When comparing single and multiple groups, follow the resources available to a namespace rather than counting every box as additional total capacity.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Reclaim Group</dt><dd>Reclaim Group, a set of non-volatile storage resources with shared reclamation behavior.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §2.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 12, printed pages 28, PDF pages 54</p></details>

</details>
<!-- figure-table:BASE12-FIG-013 -->
<details class="field-note" id="figure-BASE12-FIG-013"><summary>Base Figure 13 · Simple NVM Storage Hierarchy with Multiple Reclaim Groups</summary>
<!-- claim:BASE12-FIG-013-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.08">05.08.</span><span class="paragraph-text">Figure 13, "Simple NVM Storage Hierarchy with Multiple Reclaim Groups": Reclaim Group and placement diagrams show how storage resources are grouped and shared. When comparing single and multiple groups, follow the resources available to a namespace rather than counting every box as additional total capacity.</span></p><details class="source-note"><summary>Sources: Base 2.4 §2.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 13, printed pages 29, PDF pages 55</p></details>

</details>
<!-- figure-table:BASE12-FIG-014 -->
<details class="field-note" id="figure-BASE12-FIG-014"><summary>Base Figure 14 · Complex NVM Storage Hierarchy with NVM Sets</summary>
<!-- claim:BASE12-FIG-014-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.09">05.09.</span><span class="paragraph-text">Figure 14, "Complex NVM Storage Hierarchy with NVM Sets": NVM Sets group relationships between storage resources and namespaces. Establish namespace membership before interpreting Set-aware commands. Multiple namespaces do not imply the same number of independent storage devices.</span></p><details class="source-note"><summary>Sources: Base 2.4 §2.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 14, printed pages 30, PDF pages 56</p></details>

</details>
<!-- figure-table:BASE12-FIG-015 -->
<details class="field-note" id="figure-BASE12-FIG-015"><summary>Base Figure 15 · Complex NVM Storage Hierarchy with Multiple Reclaim Groups</summary>
<!-- claim:BASE12-FIG-015-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.10">05.10.</span><span class="paragraph-text">Figure 15, "Complex NVM Storage Hierarchy with Multiple Reclaim Groups": Reclaim Group and placement diagrams show how storage resources are grouped and shared. When comparing single and multiple groups, follow the resources available to a namespace rather than counting every box as additional total capacity.</span></p><details class="source-note"><summary>Sources: Base 2.4 §2.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 15, printed pages 31, PDF pages 57</p></details>

</details>
<!-- figure-table:BASE12-FIG-016 -->
<details class="field-note" id="figure-BASE12-FIG-016"><summary>Base Figure 16 · Single-Namespace NVM Subsystem</summary>
<!-- claim:BASE12-FIG-016-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.11">05.11.</span><span class="paragraph-text">Figure 16, "Single-Namespace NVM Subsystem": Hold the NVM subsystem fixed and identify its controllers and namespaces. A namespace is an addressable storage object and a controller processes commands; adding a namespace does not necessarily add a controller.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM subsystem</dt><dd>NVM subsystem, the NVMe system boundary containing controllers, ports, namespaces, and non-volatile storage resources.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §2.3.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 16, printed pages 32, PDF pages 58</p></details>

</details>
<!-- figure-table:BASE12-FIG-017 -->
<details class="field-note" id="figure-BASE12-FIG-017"><summary>Base Figure 17 · Two-Namespace NVM Subsystem</summary>
<!-- claim:BASE12-FIG-017-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.12">05.12.</span><span class="paragraph-text">Figure 17, "Two-Namespace NVM Subsystem": Hold the NVM subsystem fixed and identify its controllers and namespaces. A namespace is an addressable storage object and a controller processes commands; adding a namespace does not necessarily add a controller.</span></p><details class="source-note"><summary>Sources: Base 2.4 §2.3.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 17, printed pages 33, PDF pages 59</p></details>

</details>
<!-- figure-table:BASE12-FIG-018 -->
<details class="field-note" id="figure-BASE12-FIG-018"><summary>Base Figure 18 · Complex NVM Subsystem</summary>
<!-- claim:BASE12-FIG-018-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.13">05.13.</span><span class="paragraph-text">Figure 18, "Complex NVM Subsystem": Hold the NVM subsystem fixed and identify its controllers and namespaces. A namespace is an addressable storage object and a controller processes commands; adding a namespace does not necessarily add a controller.</span></p><details class="source-note"><summary>Sources: Base 2.4 §2.3.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 18, printed pages 34, PDF pages 60</p></details>

</details>
<!-- figure-table:BASE12-FIG-019 -->
<details class="field-note" id="figure-BASE12-FIG-019"><summary>Base Figure 19 · NVM Express Controller with Two Namespaces</summary>
<!-- claim:BASE12-FIG-019-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.14">05.14.</span><span class="paragraph-text">Figure 19, "NVM Express Controller with Two Namespaces": Hold the NVM subsystem fixed and identify its controllers and namespaces. A namespace is an addressable storage object and a controller processes commands; adding a namespace does not necessarily add a controller.</span></p><details class="source-note"><summary>Sources: Base 2.4 §2.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 19, printed pages 35, PDF pages 61</p></details>

</details>
<!-- figure-table:BASE12-FIG-020 -->
<details class="field-note" id="figure-BASE12-FIG-020"><summary>Base Figure 20 · NVM Subsystem with Two Controllers and One Port</summary>
<!-- claim:BASE12-FIG-020-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.15">05.15.</span><span class="paragraph-text">Figure 20, "NVM Subsystem with Two Controllers and One Port": Label controllers, ports, and namespaces separately and follow their access relationships. Multiple controllers can belong to one subsystem. An Administrative controller’s management role does not imply that it handles namespace data I/O.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Administrative controller</dt><dd>Administrative controller, a management-oriented controller type that does not execute user-data I/O commands.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §2.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 20, printed pages 35, PDF pages 61</p></details>

</details>
<!-- figure-table:BASE12-FIG-021 -->
<details class="field-note" id="figure-BASE12-FIG-021"><summary>Base Figure 21 · NVM Subsystem with Two Controllers and Two Ports</summary>
<!-- claim:BASE12-FIG-021-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.16">05.16.</span><span class="paragraph-text">Figure 21, "NVM Subsystem with Two Controllers and Two Ports": Label controllers, ports, and namespaces separately and follow their access relationships. Multiple controllers can belong to one subsystem. An Administrative controller’s management role does not imply that it handles namespace data I/O.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Administrative controller</dt><dd>Administrative controller, a management-oriented controller type that does not execute user-data I/O commands.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §2.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 21, printed pages 36, PDF pages 62</p></details>

</details>
<!-- figure-table:BASE12-FIG-022 -->
<details class="field-note" id="figure-BASE12-FIG-022"><summary>Base Figure 22 · PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)</summary>
<!-- claim:BASE12-FIG-022-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.17">05.17.</span><span class="paragraph-text">Figure 22, "PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)": The SR-IOV diagram separates a Physical Function from Virtual Functions exposed by a PCIe device. Function identity is an interface-level distinction; follow controller and namespace relationships to identify the storage resource behind it.</span></p><details class="source-note"><summary>Sources: Base 2.4 §2.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 22, printed pages 37, PDF pages 63</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-queues"><h3>Figure group 03 · Command submission and completion</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.18">05.18.</span><span class="paragraph-text">Distinguish command and result storage, then follow host→SQ→controller→CQ→host. In queue-association diagrams, use SQID and CID in each completion to trace it to the originating command.</span></p>
<a class="reading-link" href="#module-queues">Return to the explanation and example</a>
<!-- figure-table:BASE12-FIG-006 -->
<details class="field-note" id="figure-BASE12-FIG-006"><summary>Base Figure 6 · Queue Pair Example, 1:1 Mapping</summary>
<!-- claim:BASE12-FIG-006-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.19">05.19.</span><span class="paragraph-text">Figure 6, "Queue Pair Example, 1:1 Mapping": A 1:1 arrangement associates each SQ with its own CQ; n:1 lets multiple SQs share a CQ. Use the completion’s SQID and CID to identify the originating command in a shared CQ.</span></p><details class="source-note"><summary>Sources: Base 2.4 §2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.1, Figure 6, printed pages 22, PDF pages 48</p></details>

</details>
<!-- figure-table:BASE12-FIG-007 -->
<details class="field-note" id="figure-BASE12-FIG-007"><summary>Base Figure 7 · Queue Pair Example, n:1 Mapping</summary>
<!-- claim:BASE12-FIG-007-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.20">05.20.</span><span class="paragraph-text">Figure 7, "Queue Pair Example, n:1 Mapping": A 1:1 arrangement associates each SQ with its own CQ; n:1 lets multiple SQs share a CQ. Use the completion’s SQID and CID to identify the originating command in a shared CQ.</span></p><details class="source-note"><summary>Sources: Base 2.4 §2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.1, Figure 7, printed pages 22, PDF pages 48</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-numbers"><h3>Figure group 04 · Numeric encodings and units</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.21">05.21.</span><span class="paragraph-text">Keep raw notation, actual count, and unit in separate columns. An index selects an entry; an offset measures distance from an origin. Converting an index into an offset requires the entry size and the origin.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>offset</dt><dd>offset: a displacement measured from a stated start. It answers “how far from the start,” unlike an index.</dd></div><div><dt>index</dt><dd>index: selects an item or format in a list. It answers “which one,” not “how far from the start.”</dd></div></dl>
<a class="reading-link" href="#module-numbers">Return to the explanation and example</a>
<!-- figure-table:BASE12-FIG-002 -->
<details class="field-note" id="figure-BASE12-FIG-002"><summary>Base Figure 2 · Decimal and Binary Units</summary>
<!-- claim:BASE12-FIG-002-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.22">05.22.</span><span class="paragraph-text">Figure 2, "Decimal and Binary Units": Distinguish decimal and binary units: 1 kB is 1000 bytes and 1 KiB is 1024 bytes. A word is two bytes and a Dword four bytes. These widths do not determine whether a particular count field requires adding one.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>word</dt><dd>word: 16 bits, or 2 bytes. It is half a Dword; a field length must be read with its unit.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §1.4.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §1.4.2, Figure 2, printed pages 3, PDF pages 29</p></details>

</details>
<!-- figure-table:BASE12-FIG-003 -->
<details class="field-note" id="figure-BASE12-FIG-003"><summary>Base Figure 3 · Byte, Word, and Dword Relationships</summary>
<!-- claim:BASE12-FIG-003-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.23">05.23.</span><span class="paragraph-text">Figure 3, "Byte, Word, and Dword Relationships": Distinguish decimal and binary units: 1 kB is 1000 bytes and 1 KiB is 1024 bytes. A word is two bytes and a Dword four bytes. These widths do not determine whether a particular count field requires adding one.</span></p><details class="source-note"><summary>Sources: Base 2.4 §1.4.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §1.4.3, Figure 3, printed pages 5, PDF pages 31</p></details>

</details>
</div>
<!-- claim:BASE12-KEYWORDS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.24">05.24.</span><span class="paragraph-text">The specification assigns distinct force to mandatory, may, optional, reserved, shall, and should. A summary must not strengthen may or should into shall.</span></p><details class="source-note"><summary>Sources: Base 2.4 §1.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §1.4.1, printed pages 2-3, PDF pages 28-29</p></details>
</section>
</details>
<section id="knowledge-check"><h2 id="review-questions">Check your understanding</h2>
<!-- qa:base-ch1-2-spec-family -->
<details class="review-question" id="qa-base-ch1-2-spec-family"><summary>1. Why do Read semantics and delivery over PCIe require different specifications?</summary>
<div data-qa-answer="base-ch1-2-spec-family"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="06.01">06.01.</span><span class="paragraph-text">The Command Set defines the operation on data; the Transport defines how commands and completions cross the connection; Base supplies the shared controller, queue, and management model. Together they describe the complete operation.</span></p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §1.1.1, printed pages 1, PDF pages 27</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.2, printed pages 33, PDF pages 59</p>
</details></details>
<!-- qa:base-ch1-2-queue-doorbell -->
<details class="review-question" id="qa-base-ch1-2-queue-doorbell"><summary>2. Where is the command itself when the host writes a doorbell?</summary>
<div data-qa-answer="base-ch1-2-queue-doorbell"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="06.02">06.02.</span><span class="paragraph-text">The command is already in a Submission Queue entry. The doorbell updates queue progress so the controller can determine the available work; it does not carry the entire command.</span></p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §2.1, printed pages 21-23, PDF pages 47-49</p>
</details></details>
<!-- qa:base-ch1-2-shared-namespace -->
<details class="review-question" id="qa-base-ch1-2-shared-namespace"><summary>3. If two controllers access one namespace, does that imply two data copies?</summary>
<div data-qa-answer="base-ch1-2-shared-namespace"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="06.03">06.03.</span><span class="paragraph-text">No. A controller is an access endpoint, while a namespace is logical storage. Multiple endpoints can reach the same space. Physical replication is a separate storage-implementation concern.</span></p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.3, printed pages 33-35, PDF pages 59-61</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, printed pages 35-37, PDF pages 61-63</p>
</details></details>
<!-- qa:base-ch1-2-units -->
<details class="review-question" id="qa-base-ch1-2-units"><summary>4. Why can a raw length value of 3 not immediately be interpreted as 3 bytes?</summary>
<div data-qa-answer="base-ch1-2-units"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="06.04">06.04.</span><span class="paragraph-text">The unit and encoding must be established first. A zero-based dword count of 3 means 4 dwords, or 16 bytes. An actual byte count of 3 instead means 3 bytes.</span></p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §1.4.2, printed pages 3-5, PDF pages 29-31</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §1.4.3, printed pages 5, PDF pages 31</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>Specification editions</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
