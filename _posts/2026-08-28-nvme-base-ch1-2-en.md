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
<p class="reader-paragraph opening"><span class="paragraph-number" aria-hidden="true">01.</span>NVMe is an interface between a host and a storage controller. This note establishes how the host submits commands, how the controller reports results, and what namespaces, controllers, and NVM subsystems represent. These concepts provide the foundation for later commands and fields.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div><div><dt>NVMe</dt><dd>Non-Volatile Memory Express, the specification family for a host interface to a non-volatile-memory subsystem.</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl>
<h2 id="main-ideas">The main ideas</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>Specification responsibilities</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-hidden="true">02.</span>Distinguish what Base, Transport, and I/O Command Set specifications define.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl></article>
<article><span class="axis-number">02</span><h3>Command round trips</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-hidden="true">03.</span>Understand cooperation between host and controller through submission and completion queues.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div></dl></article>
<article><span class="axis-number">03</span><h3>Storage objects and paths</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-hidden="true">04.</span>Distinguish namespaces, controllers, and subsystems, including multiple access paths.</p></article>
</div>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">05.</span>The host includes the operating system and driver; the controller provides the NVMe interface accessible to that host. NVMe describes host-visible behavior, which does not directly specify the SSD’s physical NAND organization.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express, the specification family for a host interface to a non-volatile-memory subsystem.</dd></div></dl>
</section>
<section class="lesson" id="module-family"><h2 id="heading-family"><span class="section-number">01</span> Roles of Base, Command Set, and Transport</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">06.</span>When a command, register, or data format appears, the first question is not merely where it is found, but which specification owns the definition. Base supplies the common protocol, the Transport adds the PCIe binding, and an I/O Command Set defines namespace data operations. The boxes in Figure 1 show applicability, not mandatory packet traversal through a stack.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div><div><dt>PCIe</dt><dd>PCI Express, the transport and device interconnect used by an NVMe memory-based controller.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASE12-FAMILY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">07.</span>The Base Specification defines the common NVMe protocol; a Transport Specification binds it to a transport, and an I/O Command Set Specification extends commands and data structures. This is an applicability relationship, not a protocol stack.</p><details class="source-note"><summary>Sources: Base 2.4 §1.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §1.1.1, printed pages 1, PDF pages 27</p></details>
<!-- claim:BASE12-COMMANDSET -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">08.</span>The Admin Command Set manages controllers and queues; an I/O Command Set defines data operations on namespaces. Base describes common mechanisms, while each I/O Command Set Specification describes command semantics.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §2.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.2, printed pages 33, PDF pages 59</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Base</td><td>Common commands, queues, status, and structures</td><td>Do not assume it owns every PCIe-register detail</td></tr><tr><td>PCIe Transport</td><td>BARs, MMIO, doorbells, interrupts, and PCIe-specific behavior</td><td>It does not override Base in a conflict</td></tr><tr><td>I/O Command Set</td><td>Specific namespace I/O commands and extensions</td><td>It does not redefine the transport</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div><div><dt>MMIO</dt><dd>Memory-Mapped I/O, access to device registers through CPU memory operations.</dd></div><div><dt>PCIe</dt><dd>PCI Express, the transport and device interconnect used by an NVMe memory-based controller.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">09.</span>To implement Firmware Image Download, read Base for command fields and completion status, then use the PCIe Transport for Admin-command data-pointer and memory-access constraints. The Admin command can be understood without an I/O Command Set, while the PCIe Transport alone does not provide complete command semantics.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASE12-FIG-001 -->
<details class="field-note" id="figure-BASE12-FIG-001"><summary>Base Figure 1 · NVMe Family of Specifications</summary>
<!-- claim:BASE12-FIG-001-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">10.</span>Figure 1, "NVMe Family of Specifications": Places NVMe Family of Specifications in the NVMe document and command-set hierarchy.</p><details class="source-note"><summary>Sources: Base 2.4 §1.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §1.1.1, Figure 1, printed pages 1, PDF pages 27</p></details>

</details>
<!-- figure-table:BASE12-FIG-005 -->
<details class="field-note" id="figure-BASE12-FIG-005"><summary>Base Figure 5 · Types of NVMe Command Sets</summary>
<!-- claim:BASE12-FIG-005-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">11.</span>Figure 5, "Types of NVMe Command Sets": Places Types of NVMe Command Sets in the NVMe document and command-set hierarchy.</p><details class="source-note"><summary>Sources: Base 2.4 §2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2, Figure 5, printed pages 21, PDF pages 47</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-objects"><h2 id="heading-objects"><span class="section-number">02</span> Namespaces, controllers, and access paths</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">12.</span>A namespace is the formatted capacity actually accessed by the host, while capacity management, endurance, reclamation, and paths live at different levels. Figures 11-18 describe containment using NVM Sets or Reclaim Groups; Figures 19-22 instead show controllers, ports, paths, and PCIe Functions. The two groups answer different questions and must not be collapsed into a falsely one-to-one tree.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASE12-STORAGE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">13.</span>The storage model expresses containment through the NVM subsystem, domain, Endurance Group, NVM Set or Reclaim Group, Reclaim Unit, and namespace. A namespace is the formatted capacity a host accesses through a controller.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Endurance Group</dt><dd>Endurance Group, a group of NVM resources for isolating and reporting endurance-related state.</dd></div><div><dt>NVM subsystem</dt><dd>NVM subsystem, the NVMe system boundary containing controllers, ports, namespaces, and non-volatile storage resources.</dd></div><div><dt>Reclaim Group</dt><dd>Reclaim Group, a set of non-volatile storage resources with shared reclamation behavior.</dd></div><div><dt>Reclaim Unit</dt><dd>Reclaim Unit, a smaller management granularity used when a controller reclaims media.</dd></div><div><dt>NVM Set</dt><dd>NVM Set, a capacity grouping that associates namespaces with a managed set of NVM resources.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §2.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, printed pages 26-33, PDF pages 52-59</p></details>
<!-- claim:BASE12-SUBSYSTEM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">14.</span>Controllers, ports, namespaces, and PCI Functions are distinct objects. An NSID is a controller-visible handle for a namespace, not the namespace itself.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NSID</dt><dd>Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §2.3.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.3, printed pages 33-35, PDF pages 59-61</p></details>
<!-- claim:BASE12-MULTIPATH -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">15.</span>Multi-path I/O provides two or more independent paths from one host to one namespace; namespace sharing lets two or more hosts access one shared namespace through different controllers. Both require at least two controllers.</p><details class="source-note"><summary>Sources: Base 2.4 §2.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, printed pages 35-37, PDF pages 61-63</p></details>
<!-- claim:BASE12-ASYMMETRY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">16.</span>With multi-path or sharing, controllers need not provide identical access characteristics to the same namespace; the host may select paths using the state reported by each controller.</p><details class="source-note"><summary>Sources: Base 2.4 §2.4.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.4.2, printed pages 37, PDF pages 63</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Multi-path I/O</td><td>One host and one namespace with two or more independent paths</td><td>Focus: path redundancy</td></tr><tr><td>Namespace sharing</td><td>Two or more hosts access one shared namespace</td><td>Focus: host ownership and coordination</td></tr><tr><td>SR-IOV</td><td>One PCIe device exposes PFs/VFs</td><td>A PCIe Function need not be an independent subsystem</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>SR-IOV</dt><dd>Single Root I/O Virtualization, a PCIe capability that exposes one PF and multiple VFs from one device.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">17.</span>Informative example: host A accesses namespace X through controllers 1 and 2, creating multi-path I/O. When host B also accesses the same namespace X through controller 2, namespace sharing is present as well. NSIDs may differ between controllers, so cross-controller comparison begins with namespace identity rather than raw NSID equality.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NSID</dt><dd>Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASE12-FIG-011 -->
<details class="field-note" id="figure-BASE12-FIG-011"><summary>Base Figure 11 · Simple NVM Storage Hierarchy with NVM Sets</summary>
<!-- claim:BASE12-FIG-011-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">18.</span>Figure 11, "Simple NVM Storage Hierarchy with NVM Sets": Shows the object or capacity relationships in Simple NVM Storage Hierarchy with NVM Sets.</p><details class="source-note"><summary>Sources: Base 2.4 §2.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 11, printed pages 27, PDF pages 53</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM Set</dt><dd>NVM Set, a capacity grouping that associates namespaces with a managed set of NVM resources.</dd></div></dl>
</details>
<!-- figure-table:BASE12-FIG-012 -->
<details class="field-note" id="figure-BASE12-FIG-012"><summary>Base Figure 12 · Simple NVM Storage Hierarchy with One Reclaim Group</summary>
<!-- claim:BASE12-FIG-012-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">19.</span>Figure 12, "Simple NVM Storage Hierarchy with One Reclaim Group": Shows the object or capacity relationships in Simple NVM Storage Hierarchy with One Reclaim Group.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Reclaim Group</dt><dd>Reclaim Group, a set of non-volatile storage resources with shared reclamation behavior.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §2.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 12, printed pages 28, PDF pages 54</p></details>

</details>
<!-- figure-table:BASE12-FIG-013 -->
<details class="field-note" id="figure-BASE12-FIG-013"><summary>Base Figure 13 · Simple NVM Storage Hierarchy with Multiple Reclaim Groups</summary>
<!-- claim:BASE12-FIG-013-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">20.</span>Figure 13, "Simple NVM Storage Hierarchy with Multiple Reclaim Groups": Shows the object or capacity relationships in Simple NVM Storage Hierarchy with Multiple Reclaim Groups.</p><details class="source-note"><summary>Sources: Base 2.4 §2.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 13, printed pages 29, PDF pages 55</p></details>

</details>
<!-- figure-table:BASE12-FIG-014 -->
<details class="field-note" id="figure-BASE12-FIG-014"><summary>Base Figure 14 · Complex NVM Storage Hierarchy with NVM Sets</summary>
<!-- claim:BASE12-FIG-014-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">21.</span>Figure 14, "Complex NVM Storage Hierarchy with NVM Sets": Shows the object or capacity relationships in Complex NVM Storage Hierarchy with NVM Sets.</p><details class="source-note"><summary>Sources: Base 2.4 §2.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 14, printed pages 30, PDF pages 56</p></details>

</details>
<!-- figure-table:BASE12-FIG-015 -->
<details class="field-note" id="figure-BASE12-FIG-015"><summary>Base Figure 15 · Complex NVM Storage Hierarchy with Multiple Reclaim Groups</summary>
<!-- claim:BASE12-FIG-015-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">22.</span>Figure 15, "Complex NVM Storage Hierarchy with Multiple Reclaim Groups": Shows the object or capacity relationships in Complex NVM Storage Hierarchy with Multiple Reclaim Groups.</p><details class="source-note"><summary>Sources: Base 2.4 §2.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.1, Figure 15, printed pages 31, PDF pages 57</p></details>

</details>
<!-- figure-table:BASE12-FIG-016 -->
<details class="field-note" id="figure-BASE12-FIG-016"><summary>Base Figure 16 · Single-Namespace NVM Subsystem</summary>
<!-- claim:BASE12-FIG-016-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">23.</span>Figure 16, "Single-Namespace NVM Subsystem": Shows the object or capacity relationships in Single-Namespace NVM Subsystem.</p><details class="source-note"><summary>Sources: Base 2.4 §2.3.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 16, printed pages 32, PDF pages 58</p></details>

</details>
<!-- figure-table:BASE12-FIG-017 -->
<details class="field-note" id="figure-BASE12-FIG-017"><summary>Base Figure 17 · Two-Namespace NVM Subsystem</summary>
<!-- claim:BASE12-FIG-017-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">24.</span>Figure 17, "Two-Namespace NVM Subsystem": Shows the object or capacity relationships in Two-Namespace NVM Subsystem.</p><details class="source-note"><summary>Sources: Base 2.4 §2.3.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 17, printed pages 33, PDF pages 59</p></details>

</details>
<!-- figure-table:BASE12-FIG-018 -->
<details class="field-note" id="figure-BASE12-FIG-018"><summary>Base Figure 18 · Complex NVM Subsystem</summary>
<!-- claim:BASE12-FIG-018-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">25.</span>Figure 18, "Complex NVM Subsystem": Shows the object or capacity relationships in Complex NVM Subsystem.</p><details class="source-note"><summary>Sources: Base 2.4 §2.3.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.3, Figure 18, printed pages 34, PDF pages 60</p></details>

</details>
<!-- figure-table:BASE12-FIG-019 -->
<details class="field-note" id="figure-BASE12-FIG-019"><summary>Base Figure 19 · NVM Express Controller with Two Namespaces</summary>
<!-- claim:BASE12-FIG-019-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">26.</span>Figure 19, "NVM Express Controller with Two Namespaces": Shows the object or capacity relationships in NVM Express Controller with Two Namespaces.</p><details class="source-note"><summary>Sources: Base 2.4 §2.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 19, printed pages 35, PDF pages 61</p></details>

</details>
<!-- figure-table:BASE12-FIG-020 -->
<details class="field-note" id="figure-BASE12-FIG-020"><summary>Base Figure 20 · NVM Subsystem with Two Controllers and One Port</summary>
<!-- claim:BASE12-FIG-020-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">27.</span>Figure 20, "NVM Subsystem with Two Controllers and One Port": Shows the object or capacity relationships in NVM Subsystem with Two Controllers and One Port.</p><details class="source-note"><summary>Sources: Base 2.4 §2.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 20, printed pages 35, PDF pages 61</p></details>

</details>
<!-- figure-table:BASE12-FIG-021 -->
<details class="field-note" id="figure-BASE12-FIG-021"><summary>Base Figure 21 · NVM Subsystem with Two Controllers and Two Ports</summary>
<!-- claim:BASE12-FIG-021-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">28.</span>Figure 21, "NVM Subsystem with Two Controllers and Two Ports": Shows the object or capacity relationships in NVM Subsystem with Two Controllers and Two Ports.</p><details class="source-note"><summary>Sources: Base 2.4 §2.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 21, printed pages 36, PDF pages 62</p></details>

</details>
<!-- figure-table:BASE12-FIG-022 -->
<details class="field-note" id="figure-BASE12-FIG-022"><summary>Base Figure 22 · PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)</summary>
<!-- claim:BASE12-FIG-022-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">29.</span>Figure 22, "PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV)": Shows the Physical Function and Virtual Function relationships in PCI Express Device Supporting Single Root I/O Virtualization (SR-IOV).</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SR-IOV</dt><dd>Single Root I/O Virtualization, a PCIe capability that exposes one PF and multiple VFs from one device.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §2.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, Figure 22, printed pages 37, PDF pages 63</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-queues"><h2 id="heading-queues"><span class="section-number">03</span> Command submission and completion</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">30.</span>The host does not write a command directly into the controller. It builds an SQE in memory and publishes a new SQ tail; the controller fetches and executes the command, then places a CQE into a CQ. The 1:1 and n:1 distinction in Figures 6 and 7 concerns whether multiple SQs share one CQ, not whether commands share one SQE.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div><div><dt>SQE</dt><dd>Submission Queue Entry, one command structure in an SQ.</dd></div><div><dt>CQ</dt><dd>Completion Queue, the queue into which a controller posts command completions.</dd></div><div><dt>SQ</dt><dd>Submission Queue, the queue into which the host places commands.</dd></div></dl>
<figure><figcaption><strong>One command round trip</strong></figcaption><ol class="flow-steps"><li>The host writes a command to the Submission Queue (SQ).</li><li>The host updates the SQ Tail Doorbell to announce new work.</li><li>The controller retrieves and executes the command, then writes its result to the Completion Queue (CQ).</li><li>The host reads the CQE and updates the CQ Head Doorbell to release consumed entries.</li></ol><figcaption>Queues hold commands and results; doorbells announce updated queue positions.</figcaption></figure>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div><div><dt>CQ</dt><dd>Completion Queue, the queue into which a controller posts command completions.</dd></div><div><dt>SQ</dt><dd>Submission Queue, the queue into which the host places commands.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASE12-QUEUE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">31.</span>In the PCIe memory-based model, Submission and Completion Queues reside in memory. Multiple I/O Submission Queues may share an I/O Completion Queue, while the Admin queue pair remains one-to-one.</p><details class="source-note"><summary>Sources: Base 2.4 §2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.1, printed pages 21-23, PDF pages 47-49</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Admin queue pair</td><td>One Admin SQ to one Admin CQ</td><td>Initialization and management path</td></tr><tr><td>I/O 1:1</td><td>One I/O SQ to one I/O CQ</td><td>Simple tracking and clear isolation</td></tr><tr><td>I/O n:1</td><td>Multiple I/O SQs share one I/O CQ</td><td>Merged completion path; SQID/CID still recover the command</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>SQID</dt><dd>Submission Queue Identifier, the numeric identifier of the SQ containing a command.</dd></div><div><dt>CID</dt><dd>Command Identifier, used with the SQ identifier to identify an outstanding command.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">32.</span>Informative example: SQ 3 and SQ 4 share CQ 2. Both commands may use CID 5 and remain distinguishable because the identity key is (SQID, CID): (3,5) and (4,5). An outstanding-command map keyed only by CID can associate a completion with the wrong command.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SQID</dt><dd>Submission Queue Identifier, the numeric identifier of the SQ containing a command.</dd></div><div><dt>CID</dt><dd>Command Identifier, used with the SQ identifier to identify an outstanding command.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASE12-FIG-006 -->
<details class="field-note" id="figure-BASE12-FIG-006"><summary>Base Figure 6 · Queue Pair Example, 1:1 Mapping</summary>
<!-- claim:BASE12-FIG-006-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">33.</span>Figure 6, "Queue Pair Example, 1:1 Mapping": Shows the queue or command relationship expressed by Queue Pair Example, 1:1 Mapping.</p><details class="source-note"><summary>Sources: Base 2.4 §2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.1, Figure 6, printed pages 22, PDF pages 48</p></details>

</details>
<!-- figure-table:BASE12-FIG-007 -->
<details class="field-note" id="figure-BASE12-FIG-007"><summary>Base Figure 7 · Queue Pair Example, n:1 Mapping</summary>
<!-- claim:BASE12-FIG-007-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">34.</span>Figure 7, "Queue Pair Example, n:1 Mapping": Shows the queue or command relationship expressed by Queue Pair Example, n:1 Mapping.</p><details class="source-note"><summary>Sources: Base 2.4 §2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §2.1, Figure 7, printed pages 22, PDF pages 48</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-numbers"><h2 id="heading-numbers"><span class="section-number">04</span> Numeric encodings and units</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">35.</span>Before reading any raw value, establish its unit and encoding. A zero-based count of 3 may represent 4 units; an index selects a list item, while an offset measures distance from a start. They are not interchangeable.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>zero-based</dt><dd>zero-based: numbering starts at zero, so raw=3 can mean the fourth item or four units; the field definition still decides which.</dd></div><div><dt>raw value</dt><dd>raw value: the value read directly from a field before applying zero-based, unit, or scaling rules; confirm the definition before converting it.</dd></div><div><dt>offset</dt><dd>offset: a displacement measured from a stated start. It answers “how far from the start,” unlike an index.</dd></div><div><dt>index</dt><dd>index: selects an item or format in a list. It answers “which one,” not “how far from the start.”</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASE12-NUMBERS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">36.</span>A value is interpreted together with its radix and units. Hexadecimal uses the h suffix, binary uses b, and decimal may omit d. Decimal and binary capacity prefixes represent different multipliers.</p><details class="source-note"><summary>Sources: Base 2.4 §1.4.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §1.4.2, printed pages 3-5, PDF pages 29-31</p></details>
<!-- claim:BASE12-DWORD -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">37.</span>NVMe expresses field locations in bytes, words, and dwords. A word is two bytes and a dword is four bytes; field reading the fields starts by confirming byte and bit numbering.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Dword (double word): 32 bits, or 4 bytes. A word is 16 bits; for example, a zero-based dword count of 3 represents 4 Dwords, or 16 bytes.</dd></div><div><dt>word</dt><dd>word: 16 bits, or 2 bytes. It is half a Dword; a field length must be read with its unit.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §1.4.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §1.4.3, printed pages 5, PDF pages 31</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>1000</td><td>Decimal 1000</td><td>No b/h suffix means decimal</td></tr><tr><td>1000b</td><td>Binary value 8</td><td>b is a radix marker, not a bit unit</td></tr><tr><td>1000h</td><td>Hexadecimal value 4096</td><td>Common for offsets and register values</td></tr><tr><td>NUMD=0</td><td>One actual dword</td><td>Add one only when the field is explicitly zero-based</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>zero-based</dt><dd>zero-based: numbering starts at zero, so raw=3 can mean the fourth item or four units; the field definition still decides which.</dd></div><div><dt>Dword</dt><dd>Dword (double word): 32 bits, or 4 bytes. A word is 16 bits; for example, a zero-based dword count of 3 represents 4 Dwords, or 16 bytes.</dd></div><div><dt>NUMD</dt><dd>Number of Dwords, a zero-based transfer-dword count; actual bytes = (NUMD + 1) × 4.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">38.</span>Informative example: a 512-byte transfer contains 512 / 4 = 128 dwords. If NUMD is zero-based, the encoded value is 128 - 1 = 127 = 007Fh. Treating 007Fh as a byte count under-allocates the buffer; forgetting the subtraction requests 129 dwords.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NUMD</dt><dd>Number of Dwords, a zero-based transfer-dword count; actual bytes = (NUMD + 1) × 4.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASE12-FIG-002 -->
<details class="field-note" id="figure-BASE12-FIG-002"><summary>Base Figure 2 · Decimal and Binary Units</summary>
<!-- claim:BASE12-FIG-002-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">39.</span>Figure 2, "Decimal and Binary Units": Defines the numeric-unit or byte-width convention illustrated by Decimal and Binary Units.</p><details class="source-note"><summary>Sources: Base 2.4 §1.4.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §1.4.2, Figure 2, printed pages 3, PDF pages 29</p></details>

</details>
<!-- figure-table:BASE12-FIG-003 -->
<details class="field-note" id="figure-BASE12-FIG-003"><summary>Base Figure 3 · Byte, Word, and Dword Relationships</summary>
<!-- claim:BASE12-FIG-003-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">40.</span>Figure 3, "Byte, Word, and Dword Relationships": Defines the numeric-unit or byte-width convention illustrated by Byte, Word, and Dword Relationships.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>word</dt><dd>word: 16 bits, or 2 bytes. It is half a Dword; a field length must be read with its unit.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §1.4.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §1.4.3, Figure 3, printed pages 5, PDF pages 31</p></details>

</details>
</details>
</section>
<section id="additional-details"><h2 id="further-mechanisms">Additional mechanisms and data formats</h2>
<!-- claim:BASE12-KEYWORDS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-hidden="true">41.</span>The specification assigns distinct force to mandatory, may, optional, reserved, shall, and should. A summary must not strengthen may or should into shall.</p><details class="source-note"><summary>Sources: Base 2.4 §1.4.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §1.4.1, printed pages 2-3, PDF pages 28-29</p></details>
</section>
<section id="knowledge-check"><h2 id="review-questions">Check your understanding</h2>
<!-- qa:base-ch1-2-spec-family -->
<details class="review-question" id="qa-base-ch1-2-spec-family"><summary>1. Why do Read semantics and delivery over PCIe require different specifications?</summary>
<div data-qa-answer="base-ch1-2-spec-family"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">42.</span>The Command Set defines the operation on data; the Transport defines how commands and completions cross the connection; Base supplies the shared controller, queue, and management model. Together they describe the complete operation.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §1.1.1, printed pages 1, PDF pages 27</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.2, printed pages 33, PDF pages 59</p>
</details></details>
<!-- qa:base-ch1-2-queue-doorbell -->
<details class="review-question" id="qa-base-ch1-2-queue-doorbell"><summary>2. Where is the command itself when the host writes a doorbell?</summary>
<div data-qa-answer="base-ch1-2-queue-doorbell"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">43.</span>The command is already in a Submission Queue entry. The doorbell updates queue progress so the controller can determine the available work; it does not carry the entire command.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §2.1, printed pages 21-23, PDF pages 47-49</p>
</details></details>
<!-- qa:base-ch1-2-shared-namespace -->
<details class="review-question" id="qa-base-ch1-2-shared-namespace"><summary>3. If two controllers access one namespace, does that imply two data copies?</summary>
<div data-qa-answer="base-ch1-2-shared-namespace"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">44.</span>No. A controller is an access endpoint, while a namespace is logical storage. Multiple endpoints can reach the same space. Physical replication is a separate storage-implementation concern.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §2.3.3, printed pages 33-35, PDF pages 59-61</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §2.4.1, printed pages 35-37, PDF pages 61-63</p>
</details></details>
<!-- qa:base-ch1-2-units -->
<details class="review-question" id="qa-base-ch1-2-units"><summary>4. Why can a raw length value of 3 not immediately be interpreted as 3 bytes?</summary>
<div data-qa-answer="base-ch1-2-units"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-hidden="true">45.</span>The unit and encoding must be established first. A zero-based dword count of 3 means 4 dwords, or 16 bytes. An actual byte count of 3 instead means 3 bytes.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §1.4.2, printed pages 3-5, PDF pages 29-31</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §1.4.3, printed pages 5, PDF pages 31</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>Specification editions</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
