---
layout: post
read_time: true
show_date: true
title: "NVMe Base 2.4 Chapter 4: SQE, CQE, Status, PRP, and SGL"
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
[繁體中文]({% post_url 2026-08-28-nvme-base-ch4-zh-tw %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span><span class="paragraph-text">An NVMe command must identify the operation, target namespace, and data location. Its completion must identify the command and report the outcome. This note uses these two directions to explain SQEs, CQEs, and PRP/SGL data pointers.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div><div><dt>NVMe</dt><dd>Non-Volatile Memory Express, the specification family for a host interface to a non-volatile-memory subsystem.</dd></div><div><dt>PRP</dt><dd>Physical Region Page, a pointer format describing a host-addressable data buffer in memory-page units.</dd></div><div><dt>SGL</dt><dd>Scatter Gather List, a descriptor-and-segment format for one or more data-buffer regions.</dd></div></dl>
<h2 id="main-ideas">The main ideas</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>Command contents: SQE</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="01-01">01-01</span><span class="paragraph-text">Understand command identifiers, opcodes, and data pointers.</span></p></article>
<article><span class="axis-number">02</span><h3>Completion results: CQE</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="02-01">02-01</span><span class="paragraph-text">Distinguish new entries, command identity, and status codes.</span></p></article>
<article><span class="axis-number">03</span><h3>Data addresses: PRP/SGL</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="03-01">03-01</span><span class="paragraph-text">Connect memory-page concepts to NVMe data transfers.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express, the specification family for a host interface to a non-volatile-memory subsystem.</dd></div></dl></article>
<article><span class="axis-number">04</span><h3>Other shared structures</h3><p class="axis-paragraph"><span class="axis-paragraph-number" aria-label="04-01">04-01</span><span class="paragraph-text">Understand representations for Feature values, identifiers, lists, and text.</span></p></article>
</div>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.02">00.02.</span><span class="paragraph-text">Command and completion entries are records in queues; data pointers identify the data involved in a transfer. Distinguishing the command record from its transfer data is the starting point for the field layouts.</span></p>
<div class="overview-connections"><h3>Connecting the main ideas</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.03">00.03.</span><span class="paragraph-text">Separate an operation into the request in the SQE, data locations described by PRP/SGL, and the command identity and result in the CQE. Identifiers and lists help select the intended objects.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div><div><dt>PRP</dt><dd>Physical Region Page, a pointer format describing a host-addressable data buffer in memory-page units.</dd></div><div><dt>SGL</dt><dd>Scatter Gather List, a descriptor-and-segment format for one or more data-buffer regions.</dd></div><div><dt>SQE</dt><dd>Submission Queue Entry, one command structure in an SQ.</dd></div></dl>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.04">00.04.</span><span class="paragraph-text">The lessons move from common layouts to bits, lengths, and pointers. The aim is to calculate transfer size, interpret pointers correctly, and associate a completion with its command. Establish units before calculations rather than inferring them from field names.</span></p>
</div>
</section>
<section class="lesson" id="module-sqe"><h2 id="heading-sqe"><span class="section-number">01</span> The common SQE format and command fields</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span><span class="paragraph-text">The common SQE fixes the locations of CDW0, NSID, metadata/data pointers, and CDW10-15. OPC selects the command, CID creates the completion association, and PSDT selects DPTR interpretation. Only after these common fields are established should command-specific CDW10-15 definitions be applied. Figures 92-94 are the coordinate system for all later command construction.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>metadata</dt><dd>Additional information stored with a logical block; it can contain protection information or serve other purposes.</dd></div><div><dt>DPTR</dt><dd>Data Pointer, the SQE field identifying a command data buffer.</dd></div><div><dt>NSID</dt><dd>Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself.</dd></div><div><dt>PSDT</dt><dd>PRP or SGL for Data Transfer, the CDW0 field selecting PRP or SGL interpretation for DPTR.</dd></div><div><dt>CDW</dt><dd>CDW (Command Dword): a 32-bit command field. In CDW10, 10 is the field index, not a byte offset.</dd></div><div><dt>CID</dt><dd>Command Identifier, used with the SQ identifier to identify an outstanding command.</dd></div><div><dt>SQE</dt><dd>Submission Queue Entry, one command structure in an SQ.</dd></div></dl>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 160" role="img"><title>CDW0 · 32 bits</title><desc>CDW0 holds command identity, data-pointer type, fused-operation selection, and opcode. Labeled bit ranges determine widths; boxes are sized for readability.</desc><rect x="20" y="35" width="300" height="85" rx="6" class="v-object"/><text x="170.0" y="71.0" text-anchor="middle" font-size="17">CID</text><text x="170.0" y="96.0" text-anchor="middle" font-size="17">31:16</text><rect x="320" y="35" width="90" height="85" rx="6" class="v-command"/><text x="365.0" y="71.0" text-anchor="middle" font-size="17">PSDT</text><text x="365.0" y="96.0" text-anchor="middle" font-size="17">15:14</text><rect x="410" y="35" width="130" height="85" rx="6" class="v-decision"/><text x="475.0" y="71.0" text-anchor="middle" font-size="17">Reserved</text><text x="475.0" y="96.0" text-anchor="middle" font-size="17">13:10</text><rect x="540" y="35" width="90" height="85" rx="6" class="v-command"/><text x="585.0" y="71.0" text-anchor="middle" font-size="17">FUSE</text><text x="585.0" y="96.0" text-anchor="middle" font-size="17">9:8</text><rect x="630" y="35" width="110" height="85" rx="6" class="v-success"/><text x="685.0" y="71.0" text-anchor="middle" font-size="17">OPC</text><text x="685.0" y="96.0" text-anchor="middle" font-size="17">7:0</text></svg></div><figcaption>CDW0 holds command identity, data-pointer type, fused-operation selection, and opcode. Labeled bit ranges determine widths; boxes are sized for readability.</figcaption></figure>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>PSDT</dt><dd>PRP or SGL for Data Transfer, the CDW0 field selecting PRP or SGL interpretation for DPTR.</dd></div><div><dt>CDW</dt><dd>CDW (Command Dword): a 32-bit command field. In CDW10, 10 is the field index, not a byte offset.</dd></div><div><dt>CID</dt><dd>Command Identifier, used with the SQ identifier to identify an outstanding command.</dd></div></dl>
<details class="technical-note"><summary>Full rules: The common SQE format and command fields</summary>
<!-- claim:BASE4-SQE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span><span class="paragraph-text">The common Admin and I/O SQE is 64 bytes. CDW0, NSID, data pointers, and CDW10-15 establish the common layout before each command defines command-specific content.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div><div><dt>NSID</dt><dd>Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself.</dd></div><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 139-143, PDF pages 165-169</p></details>
<!-- claim:BASE4-CID -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span><span class="paragraph-text">CID in combination with the Submission Queue identifier uniquely identifies a command. FFFFh should be avoided because the Error Information log uses it when an error is not associated with a particular command.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 140, PDF pages 166</p></details>
<!-- claim:BASE4-PSDT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.04">01.04.</span><span class="paragraph-text">CDW0.PSDT selects PRP or SGL interpretation for DPTR. An Admin command over PCIe shall use PRPs unless its command definition specifies otherwise.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div><div><dt>DPTR</dt><dd>Data Pointer, the SQE field identifying a command data buffer.</dd></div><div><dt>PCIe</dt><dd>PCI Express, the transport and device interconnect used by an NVMe memory-based controller.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 140-142, PDF pages 166-168</p></details>
</details>
<div class="table-wrap"><table><caption>The common SQE format and command fields</caption><thead><tr><th scope="col">SQE region</th><th scope="col">Information provided by the host</th><th scope="col">Selecting the right field definition</th></tr></thead><tbody><tr><td>CDW0</td><td>Command identity and data-pointer selector</td><td>Common to all commands</td></tr><tr><td>NSID</td><td>Namespace scope</td><td>When unused, clear or use a special value only as the command defines</td></tr><tr><td>MPTR/DPTR</td><td>Metadata and data buffers</td><td>Selected by PSDT and command rules</td></tr><tr><td>CDW10-15</td><td>Command-specific payload</td><td>Never borrow semantics from another command</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>metadata</dt><dd>Additional information stored with a logical block; it can contain protection information or serve other purposes.</dd></div><div><dt>MPTR</dt><dd>Metadata Pointer, the SQE field identifying a separate metadata buffer.</dd></div></dl>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.05">01.05.</span><span class="paragraph-text">Informative example: the same CID can be used on different SQs, but outstanding commands within one SQ must not create an identity collision. The driver tracks commands by (SQID,CID), completes every SQE field and required memory ordering, and only then updates the SQ tail.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SQID</dt><dd>Submission Queue Identifier, the numeric identifier of the SQ containing a command.</dd></div><div><dt>SQ</dt><dd>Submission Queue, the queue into which the host places commands.</dd></div></dl></aside>
<a class="reading-link" href="#reading-sqe">Read the related specification figures → The common SQE format and command fields</a>
</section>
<section class="lesson" id="module-cqe-status"><h2 id="heading-cqe-status"><span class="section-number">02</span> CQEs: new entries, command identity, and results</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span><span class="paragraph-text">The host first uses the Phase Tag to determine whether a CQ slot contains a new completion. After ownership is established, SQID/CID recovers the command; SCT then selects the status category before SC, DNR, and CRD are interpreted. Figures 97-109 must be read in this order so a stale CQE or wrong category is not mistaken for a command failure.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div><div><dt>SQID</dt><dd>Submission Queue Identifier, the numeric identifier of the SQ containing a command.</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div><div><dt>CRD</dt><dd>Command Retry Delay, the status field selecting a controller-recommended retry delay.</dd></div><div><dt>DNR</dt><dd>Do Not Retry, a CQE-status bit indicating that retrying the same command is not expected to succeed.</dd></div><div><dt>SCT</dt><dd>Status Code Type: selects the completion-status category and is interpreted with SC.</dd></div><div><dt>CQ</dt><dd>Completion Queue, the queue into which a controller posts command completions.</dd></div><div><dt>SC</dt><dd>Status Code: identifies the completion result within the selected SCT category.</dd></div></dl>
<details class="technical-note"><summary>Full rules: CQEs: new entries, command identity, and results</summary>
<!-- claim:BASE4-CQE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span><span class="paragraph-text">The common CQE is at least 16 bytes. If multiple writes construct it, the Phase Tag shall be updated in the last write so the host does not consume a partial entry.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, printed pages 144-145, PDF pages 170-171</p></details>
<!-- claim:BASE4-STATUS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span><span class="paragraph-text">Status reading the fields starts with Status Code Type (SCT), then Status Code (SC), together with control bits such as Do Not Retry (DNR). An SC value is not interpreted without its SCT.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DNR</dt><dd>Do Not Retry, a CQE-status bit indicating that retrying the same command is not expected to succeed.</dd></div><div><dt>SCT</dt><dd>Status Code Type: selects the completion-status category and is interpreted with SC.</dd></div><div><dt>SC</dt><dd>Status Code: identifies the completion result within the selected SCT category.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, printed pages 145-155, PDF pages 171-181</p></details>
<!-- claim:BASE4-PHASE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.04">02.04.</span><span class="paragraph-text">The Phase Tag lets the host distinguish a new entry in a circular Completion Queue. After consuming CQEs, the host advances the CQ head doorbell and expects phase inversion on wrap.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CQ</dt><dd>Completion Queue, the queue into which a controller posts command completions.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.2.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.4, printed pages 155-158, PDF pages 181-184</p></details>
</details>
<div class="table-wrap"><table><caption>CQEs: new entries, command identity, and results</caption><thead><tr><th scope="col">Completion-status field</th><th scope="col">Question answered</th><th scope="col">Other required information</th></tr></thead><tbody><tr><td>SCT</td><td>Status category</td><td>Always interpret the fields first</td></tr><tr><td>SC</td><td>Specific result within the category</td><td>Never interpret without SCT</td></tr><tr><td>DNR</td><td>Expectation for retrying the same command</td><td>Not synonymous with permanent hardware failure</td></tr><tr><td>CRD</td><td>Recommended retry-delay selector</td><td>Use only for an applicable status</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>CRD</dt><dd>Command Retry Delay, the status field selecting a controller-recommended retry delay.</dd></div></dl>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.05">02.05.</span><span class="paragraph-text">Informative example: SC value 02h can belong to different status tables under different SCT values. A correct log retains the complete status field and reports P, SCT, SC, DNR, CRD, and the raw 16-bit value. 'SC=2' alone is insufficient for recovery.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>P</dt><dd>Phase Tag, the toggling bit used by the host to decide whether a CQ slot contains a new completion.</dd></div></dl></aside>
<a class="reading-link" href="#reading-cqe-status">Read the related specification figures → CQEs: new entries, command identity, and results</a>
</section>
<section class="lesson" id="module-prp"><h2 id="heading-prp"><span class="section-number">03</span> How PRPs describe data across pages</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span><span class="paragraph-text">PRP1 may address any byte within the first memory page, so first-segment capacity is page_size minus offset. If data crosses that page, PRP2 represents either the second page or a PRP List depending on remaining length; later page addresses must be page aligned. Figures 110-113 define address calculation, not merely pointer names.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>offset</dt><dd>offset: a displacement measured from a stated start. It answers “how far from the start,” unlike an index.</dd></div></dl>
<details class="technical-note"><summary>Full rules: How PRPs describe data across pages</summary>
<!-- claim:BASE4-PRP -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span><span class="paragraph-text">A fixed-size PRP entry points to a physical memory page. The first entry may contain a page offset; subsequent PRPs shall obey page alignment, and transfer length determines the required entry count.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>page offset</dt><dd>page offset: the starting displacement inside the first memory page; after a page boundary, the next page pointer determines the location.</dd></div><div><dt>offset</dt><dd>offset: a displacement measured from a stated start. It answers “how far from the start,” unlike an index.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, printed pages 158-159, PDF pages 184-185</p></details>
</details>
<div class="table-wrap"><table><caption>How PRPs describe data across pages</caption><thead><tr><th scope="col">Page-span case</th><th scope="col">Meaning of PRP2</th><th scope="col">Pointer and alignment requirement</th></tr></thead><tbody><tr><td>Data stays in first page</td><td>PRP1 is sufficient</td><td>PRP2 does not carry another segment</td></tr><tr><td>Remaining data fits one page</td><td>PRP2 addresses the second data page</td><td>Address is page aligned</td></tr><tr><td>Remaining data exceeds one page</td><td>PRP2 addresses a PRP List</td><td>List entries address data pages</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.03">03.03.</span><span class="paragraph-text">If PRP1 has a 512-byte page offset, the first page carries data beginning at byte 512. After the page boundary, the next location comes from the next page pointer; the same physical address is not simply extended.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>page offset</dt><dd>page offset: the starting displacement inside the first memory page; after a page boundary, the next page pointer determines the location.</dd></div></dl></aside>
<a class="reading-link" href="#reading-prp">Read the related specification figures → How PRPs describe data across pages</a>
</section>
<section class="lesson" id="module-sgl"><h2 id="heading-sgl"><span class="section-number">04</span> SGL data and segment descriptors</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span><span class="paragraph-text">An SGL descriptor combines type/subtype, address, and length. A Data Block addresses data, Segment and Last Segment address more descriptors, and Bit Bucket represents data that need not be stored in memory. Figures 114-125 require type-first reading the fields; blindly following an address before reading the fields type is incorrect.</span></p>
<details class="technical-note"><summary>Full rules: SGL data and segment descriptors</summary>
<!-- claim:BASE4-SGL -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span><span class="paragraph-text">An SGL describes a data buffer through one or more descriptors and segments. SGL length shall equal or exceed the requested transfer length; this report covers only generic descriptors applicable to PCIe.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PCIe</dt><dd>PCI Express, the transport and device interconnect used by an NVMe memory-based controller.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, printed pages 159-166, PDF pages 185-192</p></details>
</details>
<div class="table-wrap"><table><caption>SGL data and segment descriptors</caption><thead><tr><th scope="col">Pointer or descriptor type</th><th scope="col">Meaning of address and length</th><th scope="col">Object reached by following the pointer</th></tr></thead><tbody><tr><td>PRP</td><td>Page-based addresses</td><td>First-page offset plus later-page alignment</td></tr><tr><td>SGL Data Block</td><td>Address plus byte length</td><td>A descriptor represents a data region</td></tr><tr><td>SGL Segment</td><td>Address plus descriptor-list length</td><td>Points to more descriptors, not data</td></tr><tr><td>Bit Bucket</td><td>Consumes transfer length only</td><td>Does not represent a readable or writable memory buffer</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.03">04.03.</span><span class="paragraph-text">A 12 KiB data transfer can use two Data Block descriptors of 8 KiB and 4 KiB. A Segment descriptor instead uses length for the next descriptor list, rather than user-data length.</span></p></aside>
<a class="reading-link" href="#reading-sgl">Read the related specification figures → SGL data and segment descriptors</a>
</section>
<section class="lesson" id="module-identity-text"><h2 id="heading-identity-text"><span class="section-number">05</span> Feature values, identifiers, lists, and strings</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span><span class="paragraph-text">Establish what a value represents before interpreting it: Feature values distinguish active from saved state, identifiers have an identity scope, and lists and strings each have layout and length rules.</span></p>
<details class="technical-note"><summary>Full rules: Feature values, identifiers, lists, and strings</summary>
<!-- claim:BASE4-FEATURE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.02">05.02.</span><span class="paragraph-text">A Feature may have default, saved, and current values. Saved-value support and persistence across resets or power cycles are determined from SSFS and each Feature capability.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.4, printed pages 166-169, PDF pages 192-195</p></details>
<!-- claim:BASE4-IDENTIFIER -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.03">05.03.</span><span class="paragraph-text">VID/SSVID, SN/MN, IEEE OUI, EUI64, NGUID, and UUID differ in origin, length, and uniqueness scope and are not interchangeable. This section is informative.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>EUI64</dt><dd>64-bit Extended Unique Identifier, a 64-bit identifier constructed from IEEE-assigned space.</dd></div><div><dt>NGUID</dt><dd>Namespace Globally Unique Identifier, a 128-bit global identifier for a namespace.</dd></div><div><dt>SSVID</dt><dd>Subsystem Vendor ID, the PCI identifier for a subsystem vendor.</dd></div><div><dt>UUID</dt><dd>Universally Unique Identifier, a 128-bit identifier whose association scope is defined by the containing structure.</dd></div><div><dt>OUI</dt><dd>Organizationally Unique Identifier, an IEEE-assigned identifier prefix for an organization.</dd></div><div><dt>VID</dt><dd>Vendor ID, a PCI-SIG-assigned identifier for a vendor.</dd></div><div><dt>MN</dt><dd>Model Number, a string identifying a product model.</dd></div><div><dt>SN</dt><dd>Serial Number, a string identifying a product instance.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5, printed pages 169-172, PDF pages 195-198</p></details>
<!-- claim:BASE4-LISTS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.04">05.04.</span><span class="paragraph-text">A Controller List starts with NUMCIDS and then up to 2047 ascending 16-bit controller identifiers. A Namespace List has no count header and directly lists ascending 32-bit NSIDs. Unused entries in both lists are zero filled.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>NUMCIDS</dt><dd>Number of Controller Identifiers: the count of valid controller IDs in a Controller List.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.6, printed pages 172-173, PDF pages 198-199</p></details>
<!-- claim:BASE4-UTF8 -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.05">05.05.</span><span class="paragraph-text">UTF-8 input processing validates encoding, prohibited code points, and truncation using the specified flow; an arbitrary byte sequence is not automatically a valid string.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>UTF-8</dt><dd>Unicode Transformation Format - 8-bit, a text encoding that represents a Unicode code point with one to four bytes.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.8</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.8, printed pages 175, PDF pages 201</p></details>
</details>
<div class="table-wrap"><table><caption>Feature values, identifiers, lists, and strings</caption><thead><tr><th scope="col">Identifier or list</th><th scope="col">Object and format identified</th><th scope="col">Length and count interpretation</th></tr></thead><tbody><tr><td>VID/SSVID</td><td>Vendor and subsystem vendor identifiers</td><td>Interpret each field for its own object</td></tr><tr><td>SN/MN</td><td>Product serial and model strings</td><td>Read fixed lengths and padding rules</td></tr><tr><td>EUI64/NGUID/UUID</td><td>Different object identifier formats</td><td>Widths and identity scopes are not interchangeable</td></tr><tr><td>Controller List</td><td>NUMCIDS followed by 16-bit IDs</td><td>Has an explicit count header</td></tr><tr><td>Namespace List</td><td>Direct sequence of 32-bit NSIDs</td><td>Does not have the Controller List count header</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>NUMCIDS</dt><dd>Number of Controller Identifiers: the count of valid controller IDs in a Controller List.</dd></div><div><dt>EUI64</dt><dd>64-bit Extended Unique Identifier, a 64-bit identifier constructed from IEEE-assigned space.</dd></div><div><dt>NGUID</dt><dd>Namespace Globally Unique Identifier, a 128-bit global identifier for a namespace.</dd></div><div><dt>SSVID</dt><dd>Subsystem Vendor ID, the PCI identifier for a subsystem vendor.</dd></div><div><dt>UUID</dt><dd>Universally Unique Identifier, a 128-bit identifier whose association scope is defined by the containing structure.</dd></div><div><dt>VID</dt><dd>Vendor ID, a PCI-SIG-assigned identifier for a vendor.</dd></div><div><dt>MN</dt><dd>Model Number, a string identifying a product model.</dd></div><div><dt>SN</dt><dd>Serial Number, a string identifying a product instance.</dd></div></dl>
<aside class="worked-example"><h3>Illustrative example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="05.06">05.06.</span><span class="paragraph-text">A three-controller list starts with NUMCIDS=3 followed by three 16-bit IDs. A three-namespace list starts directly with the first 32-bit NSID. UTF-8 byte length also differs from character count: “中” occupies three bytes.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div><div><dt>UTF-8</dt><dd>Unicode Transformation Format - 8-bit, a text encoding that represents a Unicode code point with one to four bytes.</dd></div></dl></aside>
<a class="reading-link" href="#reading-identity-text">Read the related specification figures → Feature values, identifiers, lists, and strings</a>
</section>
<details class="figure-reading-fold"><summary>Expand figure teaching: read source figures by concept</summary>
<section id="figure-reading"><h2><span class="section-number">06</span> Reading the specification figures</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.01">06.01.</span><span class="paragraph-text">The specification figures below are grouped by concept. Each group explains the reading order and question to resolve, followed by the fields or behavior described by each figure. Follow links from the lessons or use this section to connect fields to complete operations.</span></p>
<div class="figure-reading-group" id="reading-sqe"><h3>Figure group 01 · The common SQE format and command fields</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.02">06.02.</span><span class="paragraph-text">Find CDW0, NSID, MPTR/DPTR, and the command-specific region in the common layout before reading CDW0 bit ranges. When boxes are sized for legibility, labeled bits rather than pixel widths determine field size.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>MPTR</dt><dd>Metadata Pointer, the SQE field identifying a separate metadata buffer.</dd></div></dl>
<a class="reading-link" href="#module-sqe">Return to the explanation and example</a>
<!-- figure-table:BASE4-FIG-092 -->
<details class="field-note" id="figure-BASE4-FIG-092"><summary>Base Figure 92 · Command Dword 0</summary>
<!-- claim:BASE4-FIG-092-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.03">06.03.</span><span class="paragraph-text">Figure 92, "Command Dword 0": The common SQE uses CDW0 for opcode, command identity, and data-pointer selection, then NSID for the target and MPTR/DPTR for buffers. CDW10–15 meanings come from the specific command and cannot be borrowed across opcodes.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Dword (double word): 32 bits, or 4 bytes. A word is 16 bits; for example, a zero-based dword count of 3 represents 4 Dwords, or 16 bytes.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 92, printed pages 139-140, PDF pages 165-166</p></details>

</details>
<!-- figure-table:BASE4-FIG-093 -->
<details class="field-note" id="figure-BASE4-FIG-093"><summary>Base Figure 93 · Common Command Format</summary>
<!-- claim:BASE4-FIG-093-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.04">06.04.</span><span class="paragraph-text">Figure 93, "Common Command Format": The common SQE uses CDW0 for opcode, command identity, and data-pointer selection, then NSID for the target and MPTR/DPTR for buffers. CDW10–15 meanings come from the specific command and cannot be borrowed across opcodes.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, printed pages 140-142, PDF pages 166-168</p></details>

</details>
<!-- figure-table:BASE4-FIG-094 -->
<details class="field-note" id="figure-BASE4-FIG-094"><summary>Base Figure 94 · Common Command Format - Vendor Specific Commands (Optional)</summary>
<!-- claim:BASE4-FIG-094-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.05">06.05.</span><span class="paragraph-text">Figure 94, "Common Command Format - Vendor Specific Commands (Optional)": The standard vendor-command format uses NDT and NDM as direct Dword counts for data and metadata. Check the relevant VSCF/SNVSCF support before interpreting pointers and lengths; the format does not define vendor payload semantics.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SNVSCF</dt><dd>Same NVM Vendor Specific Command Format, the ICSVSCC bit indicating whether I/O commands use Figure 94.</dd></div><div><dt>Dword</dt><dd>Dword (double word): 32 bits, or 4 bytes. A word is 16 bits; for example, a zero-based dword count of 3 represents 4 Dwords, or 16 bytes.</dd></div><div><dt>VSCF</dt><dd>Vendor Specific Command Format, the AVSCC bit indicating whether Admin commands use Figure 94.</dd></div><div><dt>NDM</dt><dd>Number of Dwords in Metadata Transfer, the actual metadata-dword count in the standard vendor-specific format.</dd></div><div><dt>NDT</dt><dd>Number of Dwords in Data Transfer, the actual data-dword count in the standard vendor-specific format.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 94, printed pages 143, PDF pages 169</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NDM</dt><dd>Number of Dwords in Metadata Transfer, the actual metadata-dword count in the standard vendor-specific format.</dd></div><div><dt>NDT</dt><dd>Number of Dwords in Data Transfer, the actual data-dword count in the standard vendor-specific format.</dd></div></dl>
</details>
</div>
<div class="figure-reading-group" id="reading-cqe-status"><h3>Figure group 02 · CQEs: new entries, command identity, and results</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.06">06.06.</span><span class="paragraph-text">Read completion layouts as new entry, originating command, and result: check P, connect SQID/CID, then select the status table with SCT and look up SC. Interpret DNR and CRD after the primary result.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>P</dt><dd>Phase Tag, the toggling bit used by the host to decide whether a CQ slot contains a new completion.</dd></div></dl>
<a class="reading-link" href="#module-cqe-status">Return to the explanation and example</a>
<!-- figure-table:BASE4-FIG-097 -->
<details class="field-note" id="figure-BASE4-FIG-097"><summary>Base Figure 97 · Common Completion Queue Entry Layout - Admin and All I/O Command Sets</summary>
<!-- claim:BASE4-FIG-097-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.07">06.07.</span><span class="paragraph-text">Figure 97, "Common Completion Queue Entry Layout - Admin and All I/O Command Sets": SQID/CID associate the CQE with a command, SQHD reports SQ consumption, and Status describes the result. SQHD advancing does not mean every earlier submitted command has completed.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div><div><dt>SQ</dt><dd>Submission Queue, the queue into which the host places commands.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 97, printed pages 144, PDF pages 170</p></details>

</details>
<!-- figure-table:BASE4-FIG-098 -->
<details class="field-note" id="figure-BASE4-FIG-098"><summary>Base Figure 98 · Completion Queue Entry: DW 2</summary>
<!-- claim:BASE4-FIG-098-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.08">06.08.</span><span class="paragraph-text">Figure 98, "Completion Queue Entry: DW 2": SQID/CID associate the CQE with a command, SQHD reports SQ consumption, and Status describes the result. SQHD advancing does not mean every earlier submitted command has completed.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 98, printed pages 144, PDF pages 170</p></details>

</details>
<!-- figure-table:BASE4-FIG-099 -->
<details class="field-note" id="figure-BASE4-FIG-099"><summary>Base Figure 99 · Completion Queue Entry: DW 3</summary>
<!-- claim:BASE4-FIG-099-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.09">06.09.</span><span class="paragraph-text">Figure 99, "Completion Queue Entry: DW 3": SQID/CID associate the CQE with a command, SQHD reports SQ consumption, and Status describes the result. SQHD advancing does not mean every earlier submitted command has completed.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 99, printed pages 145, PDF pages 171</p></details>

</details>
<!-- figure-table:BASE4-FIG-101 -->
<details class="field-note" id="figure-BASE4-FIG-101"><summary>Base Figure 101 · Completion Queue Entry: Status Field</summary>
<!-- claim:BASE4-FIG-101-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.10">06.10.</span><span class="paragraph-text">Figure 101, "Completion Queue Entry: Status Field": Read SCT to select the status class before using SC within that class. Generic, command-specific, media/data-integrity, and path-related results explain different causes. DNR/CRD add retry information; SC alone does not determine all handling.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 101, printed pages 145-146, PDF pages 171-172</p></details>

</details>
<!-- figure-table:BASE4-FIG-102 -->
<details class="field-note" id="figure-BASE4-FIG-102"><summary>Base Figure 102 · Status Code - Status Code Type Values</summary>
<!-- claim:BASE4-FIG-102-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.11">06.11.</span><span class="paragraph-text">Figure 102, "Status Code - Status Code Type Values": Read SCT to select the status class before using SC within that class. Generic, command-specific, media/data-integrity, and path-related results explain different causes. DNR/CRD add retry information; SC alone does not determine all handling.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 102, printed pages 146, PDF pages 172</p></details>

</details>
<!-- figure-table:BASE4-FIG-103 -->
<details class="field-note" id="figure-BASE4-FIG-103"><summary>Base Figure 103 · Status Code - Generic Command Status Values</summary>
<!-- claim:BASE4-FIG-103-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.12">06.12.</span><span class="paragraph-text">Figure 103, "Status Code - Generic Command Status Values": Read SCT to select the status class before using SC within that class. Generic, command-specific, media/data-integrity, and path-related results explain different causes. DNR/CRD add retry information; SC alone does not determine all handling.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 103, printed pages 147-150, PDF pages 173-176</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CMB</dt><dd>Controller Memory Buffer, controller-provided memory in which selected queues or data structures may reside.</dd></div></dl>
</details>
<!-- figure-table:BASE4-FIG-104 -->
<details class="field-note" id="figure-BASE4-FIG-104"><summary>Base Figure 104 · Status Code - Command Specific Status Values</summary>
<!-- claim:BASE4-FIG-104-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.13">06.13.</span><span class="paragraph-text">Figure 104, "Status Code - Command Specific Status Values": Read SCT to select the status class before using SC within that class. Generic, command-specific, media/data-integrity, and path-related results explain different causes. DNR/CRD add retry information; SC alone does not determine all handling.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.2.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 104, printed pages 151-152, PDF pages 177-178</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>ANA</dt><dd>Asymmetric Namespace Access: the state of access to a namespace through different controllers.</dd></div></dl>
</details>
<!-- figure-table:BASE4-FIG-105 -->
<details class="field-note" id="figure-BASE4-FIG-105"><summary>Base Figure 105 · Status Code - Command Specific Status Values, I/O Command Set Specific</summary>
<!-- claim:BASE4-FIG-105-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.14">06.14.</span><span class="paragraph-text">Figure 105, "Status Code - Command Specific Status Values, I/O Command Set Specific": Read SCT to select the status class before using SC within that class. Generic, command-specific, media/data-integrity, and path-related results explain different causes. DNR/CRD add retry information; SC alone does not determine all handling.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.2.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 105, printed pages 152-153, PDF pages 178-179</p></details>

</details>
<!-- figure-table:BASE4-FIG-107 -->
<details class="field-note" id="figure-BASE4-FIG-107"><summary>Base Figure 107 · Status Code - Media and Data Integrity Error Values</summary>
<!-- claim:BASE4-FIG-107-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.15">06.15.</span><span class="paragraph-text">Figure 107, "Status Code - Media and Data Integrity Error Values": Read SCT to select the status class before using SC within that class. Generic, command-specific, media/data-integrity, and path-related results explain different causes. DNR/CRD add retry information; SC alone does not determine all handling.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.2.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 107, printed pages 154-155, PDF pages 180-181</p></details>

</details>
<!-- figure-table:BASE4-FIG-108 -->
<details class="field-note" id="figure-BASE4-FIG-108"><summary>Base Figure 108 · Status Code - Path Related Status Values</summary>
<!-- claim:BASE4-FIG-108-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.16">06.16.</span><span class="paragraph-text">Figure 108, "Status Code - Path Related Status Values": Read SCT to select the status class before using SC within that class. Generic, command-specific, media/data-integrity, and path-related results explain different causes. DNR/CRD add retry information; SC alone does not determine all handling.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.2.3.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.3, Figure 108, printed pages 155, PDF pages 181</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>ANA</dt><dd>Asymmetric Namespace Access: the state of access to a namespace through different controllers.</dd></div></dl>
</details>
<!-- figure-table:BASE4-FIG-109 -->
<details class="field-note" id="figure-BASE4-FIG-109"><summary>Base Figure 109 · Phase Tag bit Transition Example</summary>
<!-- claim:BASE4-FIG-109-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.17">06.17.</span><span class="paragraph-text">Figure 109, "Phase Tag bit Transition Example": Phase Tag distinguishes a new CQ entry from contents left by an earlier traversal. Follow one slot across wraps; P=1 is not a universal condition for a new entry.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.2.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.4, Figure 109, printed pages 156-157, PDF pages 182-183</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-prp"><h3>Figure group 03 · How PRPs describe data across pages</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.18">06.18.</span><span class="paragraph-text">Calculate space remaining in the first page, then the uncovered transfer length, and select the PRP2 case. Follow list arrows while distinguishing a page holding list entries from pages holding transferred data.</span></p>
<a class="reading-link" href="#module-prp">Return to the explanation and example</a>
<!-- figure-table:BASE4-FIG-110 -->
<details class="field-note" id="figure-BASE4-FIG-110"><summary>Base Figure 110 · PRP Entry Layout</summary>
<!-- claim:BASE4-FIG-110-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.19">06.19.</span><span class="paragraph-text">Figure 110, "PRP Entry Layout": PRP1 may contain a page base and in-page offset; later data pages follow their alignment rules. PRP2 interpretation depends on the remaining page span. PRP Lists can reference noncontiguous data pages, separating transfer order from physical contiguity.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 110, printed pages 158, PDF pages 184</p></details>

</details>
<!-- figure-table:BASE4-FIG-111 -->
<details class="field-note" id="figure-BASE4-FIG-111"><summary>Base Figure 111 · PRP Entry - Page Base Address and Offset</summary>
<!-- claim:BASE4-FIG-111-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.20">06.20.</span><span class="paragraph-text">Figure 111, "PRP Entry - Page Base Address and Offset": PRP1 may contain a page base and in-page offset; later data pages follow their alignment rules. PRP2 interpretation depends on the remaining page span. PRP Lists can reference noncontiguous data pages, separating transfer order from physical contiguity.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 111, printed pages 158, PDF pages 184</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>PBAO</dt><dd>Page Base Address and Offset, the first-PRP layout combining a page base address with an in-page offset.</dd></div></dl>
</details>
<!-- figure-table:BASE4-FIG-112 -->
<details class="field-note" id="figure-BASE4-FIG-112"><summary>Base Figure 112 · PRP List Layout for Physically Contiguous Memory Pages</summary>
<!-- claim:BASE4-FIG-112-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.21">06.21.</span><span class="paragraph-text">Figure 112, "PRP List Layout for Physically Contiguous Memory Pages": PRP1 may contain a page base and in-page offset; later data pages follow their alignment rules. PRP2 interpretation depends on the remaining page span. PRP Lists can reference noncontiguous data pages, separating transfer order from physical contiguity.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 112, printed pages 159, PDF pages 185</p></details>

</details>
<!-- figure-table:BASE4-FIG-113 -->
<details class="field-note" id="figure-BASE4-FIG-113"><summary>Base Figure 113 · PRP List Layout for Physically Non-Contiguous Memory Pages</summary>
<!-- claim:BASE4-FIG-113-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.22">06.22.</span><span class="paragraph-text">Figure 113, "PRP List Layout for Physically Non-Contiguous Memory Pages": PRP1 may contain a page base and in-page offset; later data pages follow their alignment rules. PRP2 interpretation depends on the remaining page span. PRP Lists can reference noncontiguous data pages, separating transfer order from physical contiguity.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 113, printed pages 159, PDF pages 185</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CC.MPS</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.MPS selects its MPS member field.</dd></div><div><dt>MPS</dt><dd>Memory Page Size, the controller memory-page-size setting; it affects queue addresses and PRP alignment.</dd></div><div><dt>CC</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller.</dd></div></dl>
</details>
</div>
<div class="figure-reading-group" id="reading-sgl"><h3>Figure group 04 · SGL data and segment descriptors</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.23">06.23.</span><span class="paragraph-text">Read descriptor type before following each arrow to distinguish data from another descriptor list. When totaling transferred data, do not count bytes occupied by the descriptor list as user data.</span></p>
<a class="reading-link" href="#module-sgl">Return to the explanation and example</a>
<!-- figure-table:BASE4-FIG-114 -->
<details class="field-note" id="figure-BASE4-FIG-114"><summary>Base Figure 114 · SGL Validation Error Conditions</summary>
<!-- claim:BASE4-FIG-114-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.24">06.24.</span><span class="paragraph-text">Figure 114, "SGL Validation Error Conditions": SGL type and subtype select the meanings of addresses and lengths and their permitted combinations. Descriptor-list length differs from data-transfer length; do not total all LEN fields before interpreting types.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 114, printed pages 161, PDF pages 187</p></details>

</details>
<!-- figure-table:BASE4-FIG-115 -->
<details class="field-note" id="figure-BASE4-FIG-115"><summary>Base Figure 115 · SGL Segment</summary>
<!-- claim:BASE4-FIG-115-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.25">06.25.</span><span class="paragraph-text">Figure 115, "SGL Segment": SGL type and subtype select the meanings of addresses and lengths and their permitted combinations. Descriptor-list length differs from data-transfer length; do not total all LEN fields before interpreting types.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 115, printed pages 161, PDF pages 187</p></details>

</details>
<!-- figure-table:BASE4-FIG-116 -->
<details class="field-note" id="figure-BASE4-FIG-116"><summary>Base Figure 116 · Generic SGL Descriptor Format</summary>
<!-- claim:BASE4-FIG-116-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.26">06.26.</span><span class="paragraph-text">Figure 116, "Generic SGL Descriptor Format": SGL type and subtype select the meanings of addresses and lengths and their permitted combinations. Descriptor-list length differs from data-transfer length; do not total all LEN fields before interpreting types.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 116, printed pages 161, PDF pages 187</p></details>

</details>
<!-- figure-table:BASE4-FIG-117 -->
<details class="field-note" id="figure-BASE4-FIG-117"><summary>Base Figure 117 · SGL Descriptor Type</summary>
<!-- claim:BASE4-FIG-117-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.27">06.27.</span><span class="paragraph-text">Figure 117, "SGL Descriptor Type": SGL type and subtype select the meanings of addresses and lengths and their permitted combinations. Descriptor-list length differs from data-transfer length; do not total all LEN fields before interpreting types.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 117, printed pages 161-162, PDF pages 187-188</p></details>

</details>
<!-- figure-table:BASE4-FIG-118 -->
<details class="field-note" id="figure-BASE4-FIG-118"><summary>Base Figure 118 · SGL Descriptor Sub Type Values</summary>
<!-- claim:BASE4-FIG-118-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.28">06.28.</span><span class="paragraph-text">Figure 118, "SGL Descriptor Sub Type Values": SGL type and subtype select the meanings of addresses and lengths and their permitted combinations. Descriptor-list length differs from data-transfer length; do not total all LEN fields before interpreting types.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 118, printed pages 162, PDF pages 188</p></details>

</details>
<!-- figure-table:BASE4-FIG-119 -->
<details class="field-note" id="figure-BASE4-FIG-119"><summary>Base Figure 119 · SGL Data Block descriptor</summary>
<!-- claim:BASE4-FIG-119-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.29">06.29.</span><span class="paragraph-text">Figure 119, "SGL Data Block descriptor": Data Block points to data, Segment/Last Segment to descriptor lists, and Bit Bucket has its own transfer-length semantics. Follow the Read example by identifying each destination object before totaling data; descriptor storage is not user data.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 119, printed pages 162-163, PDF pages 188-189</p></details>

</details>
<!-- figure-table:BASE4-FIG-120 -->
<details class="field-note" id="figure-BASE4-FIG-120"><summary>Base Figure 120 · SGL Bit Bucket descriptor</summary>
<!-- claim:BASE4-FIG-120-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.30">06.30.</span><span class="paragraph-text">Figure 120, "SGL Bit Bucket descriptor": Data Block points to data, Segment/Last Segment to descriptor lists, and Bit Bucket has its own transfer-length semantics. Follow the Read example by identifying each destination object before totaling data; descriptor storage is not user data.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 120, printed pages 163, PDF pages 189</p></details>

</details>
<!-- figure-table:BASE4-FIG-121 -->
<details class="field-note" id="figure-BASE4-FIG-121"><summary>Base Figure 121 · SGL Segment descriptor</summary>
<!-- claim:BASE4-FIG-121-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.31">06.31.</span><span class="paragraph-text">Figure 121, "SGL Segment descriptor": Data Block points to data, Segment/Last Segment to descriptor lists, and Bit Bucket has its own transfer-length semantics. Follow the Read example by identifying each destination object before totaling data; descriptor storage is not user data.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 121, printed pages 163, PDF pages 189</p></details>

</details>
<!-- figure-table:BASE4-FIG-122 -->
<details class="field-note" id="figure-BASE4-FIG-122"><summary>Base Figure 122 · SGL Last Segment descriptor</summary>
<!-- claim:BASE4-FIG-122-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.32">06.32.</span><span class="paragraph-text">Figure 122, "SGL Last Segment descriptor": Data Block points to data, Segment/Last Segment to descriptor lists, and Bit Bucket has its own transfer-length semantics. Follow the Read example by identifying each destination object before totaling data; descriptor storage is not user data.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 122, printed pages 164, PDF pages 190</p></details>

</details>
<!-- figure-table:BASE4-FIG-125 -->
<details class="field-note" id="figure-BASE4-FIG-125"><summary>Base Figure 125 · SGL Read Example</summary>
<!-- claim:BASE4-FIG-125-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.33">06.33.</span><span class="paragraph-text">Figure 125, "SGL Read Example": Data Block points to data, Segment/Last Segment to descriptor lists, and Bit Bucket has its own transfer-length semantics. Follow the Read example by identifying each destination object before totaling data; descriptor storage is not user data.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2.1, Figure 125, printed pages 166, PDF pages 192</p></details>

</details>
</div>
<div class="figure-reading-group" id="reading-identity-text"><h3>Figure group 05 · Feature values, identifiers, lists, and strings</h3>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.34">06.34.</span><span class="paragraph-text">Read object identity, width, and string-padding rules first. Use NUMCIDS for valid Controller List entries. Read a Namespace List under its own structure and zero-value rules rather than borrowing another list’s header format.</span></p>
<a class="reading-link" href="#module-identity-text">Return to the explanation and example</a>
<!-- figure-table:BASE4-FIG-126 -->
<details class="field-note" id="figure-BASE4-FIG-126"><summary>Base Figure 126 · Current Value after Reset with Scope of Entire NVM Subsystem</summary>
<!-- claim:BASE4-FIG-126-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.35">06.35.</span><span class="paragraph-text">Figure 126, "Current Value after Reset with Scope of Entire NVM Subsystem": A Feature’s current value after reset depends on both Feature scope and reset scope. Resetting a whole subsystem versus a subset can affect different objects; one retention table cannot govern every reset event.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.4, Figure 126, printed pages 167, PDF pages 193</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl>
</details>
<!-- figure-table:BASE4-FIG-127 -->
<details class="field-note" id="figure-BASE4-FIG-127"><summary>Base Figure 127 · Current Value after Reset with Scope of Subset of the NVM Subsystem</summary>
<!-- claim:BASE4-FIG-127-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.36">06.36.</span><span class="paragraph-text">Figure 127, "Current Value after Reset with Scope of Subset of the NVM Subsystem": A Feature’s current value after reset depends on both Feature scope and reset scope. Resetting a whole subsystem versus a subset can affect different objects; one retention table cannot govern every reset event.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.4, Figure 127, printed pages 168, PDF pages 194</p></details>

</details>
<!-- figure-table:BASE4-FIG-128 -->
<details class="field-note" id="figure-BASE4-FIG-128"><summary>Base Figure 128 · PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)</summary>
<!-- claim:BASE4-FIG-128-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.37">06.37.</span><span class="paragraph-text">Figure 128, "PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)": VID/SSVID identify vendors, while SN/MN describe serial number and model. Read fixed string fields using their widths and padding rules rather than assuming arbitrary null-terminated strings.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.5.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.1, Figure 128, printed pages 169, PDF pages 195</p></details>

</details>
<!-- figure-table:BASE4-FIG-129 -->
<details class="field-note" id="figure-BASE4-FIG-129"><summary>Base Figure 129 · Serial Number (SN) and Model Number (MN)</summary>
<!-- claim:BASE4-FIG-129-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.38">06.38.</span><span class="paragraph-text">Figure 129, "Serial Number (SN) and Model Number (MN)": VID/SSVID identify vendors, while SN/MN describe serial number and model. Read fixed string fields using their widths and padding rules rather than assuming arbitrary null-terminated strings.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.5.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.2, Figure 129, printed pages 170, PDF pages 196</p></details>

</details>
<!-- figure-table:BASE4-FIG-130 -->
<details class="field-note" id="figure-BASE4-FIG-130"><summary>Base Figure 130 · IEEE OUI Identifier (IEEE)</summary>
<!-- claim:BASE4-FIG-130-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.39">06.39.</span><span class="paragraph-text">Figure 130, "IEEE OUI Identifier (IEEE)": OUI, EUI64, NGUID, and WWN comparison diagrams describe identifier composition and allocation relationships. Similar appearance does not make formats interchangeable; establish width and definition before identifying vendor and other components.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>OUI</dt><dd>Organizationally Unique Identifier, an IEEE-assigned identifier prefix for an organization.</dd></div><div><dt>WWN</dt><dd>World Wide Name, a global naming format used for storage and networking devices.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.5.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.3, Figure 130, printed pages 170, PDF pages 196</p></details>

</details>
<!-- figure-table:BASE4-FIG-131 -->
<details class="field-note" id="figure-BASE4-FIG-131"><summary>Base Figure 131 · IEEE Extended Unique Identifier (EUI64), MA-L Format</summary>
<!-- claim:BASE4-FIG-131-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.40">06.40.</span><span class="paragraph-text">Figure 131, "IEEE Extended Unique Identifier (EUI64), MA-L Format": OUI, EUI64, NGUID, and WWN comparison diagrams describe identifier composition and allocation relationships. Similar appearance does not make formats interchangeable; establish width and definition before identifying vendor and other components.</span></p><dl class="term-note" aria-label="Terms in this passage"><div><dt>WWN</dt><dd>World Wide Name, a global naming format used for storage and networking devices.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.5.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 131, printed pages 170, PDF pages 196</p></details>

</details>
<!-- figure-table:BASE4-FIG-132 -->
<details class="field-note" id="figure-BASE4-FIG-132"><summary>Base Figure 132 · IEEE Extended Unique Identifier (EUI64), OUI Identifier</summary>
<!-- claim:BASE4-FIG-132-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.41">06.41.</span><span class="paragraph-text">Figure 132, "IEEE Extended Unique Identifier (EUI64), OUI Identifier": OUI, EUI64, NGUID, and WWN comparison diagrams describe identifier composition and allocation relationships. Similar appearance does not make formats interchangeable; establish width and definition before identifying vendor and other components.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.5.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 132, printed pages 170, PDF pages 196</p></details>

</details>
<!-- figure-table:BASE4-FIG-133 -->
<details class="field-note" id="figure-BASE4-FIG-133"><summary>Base Figure 133 · IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)</summary>
<!-- claim:BASE4-FIG-133-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.42">06.42.</span><span class="paragraph-text">Figure 133, "IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)": OUI, EUI64, NGUID, and WWN comparison diagrams describe identifier composition and allocation relationships. Similar appearance does not make formats interchangeable; establish width and definition before identifying vendor and other components.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.5.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 133, printed pages 170-171, PDF pages 196-197</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NAA</dt><dd>Network Address Authority, the WWN nibble selecting an identifier format and assignment method.</dd></div></dl>
</details>
<!-- figure-table:BASE4-FIG-134 -->
<details class="field-note" id="figure-BASE4-FIG-134"><summary>Base Figure 134 · MA-L similarity to WWN</summary>
<!-- claim:BASE4-FIG-134-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.43">06.43.</span><span class="paragraph-text">Figure 134, "MA-L similarity to WWN": OUI, EUI64, NGUID, and WWN comparison diagrams describe identifier composition and allocation relationships. Similar appearance does not make formats interchangeable; establish width and definition before identifying vendor and other components.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.5.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 134, printed pages 171, PDF pages 197</p></details>

</details>
<!-- figure-table:BASE4-FIG-135 -->
<details class="field-note" id="figure-BASE4-FIG-135"><summary>Base Figure 135 · Namespace Globally Unique Identifier (NGUID)</summary>
<!-- claim:BASE4-FIG-135-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.44">06.44.</span><span class="paragraph-text">Figure 135, "Namespace Globally Unique Identifier (NGUID)": OUI, EUI64, NGUID, and WWN comparison diagrams describe identifier composition and allocation relationships. Similar appearance does not make formats interchangeable; establish width and definition before identifying vendor and other components.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.5.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 135, printed pages 171, PDF pages 197</p></details>

</details>
<!-- figure-table:BASE4-FIG-136 -->
<details class="field-note" id="figure-BASE4-FIG-136"><summary>Base Figure 136 · Namespace Globally Unique Identifier (NGUID), OUI</summary>
<!-- claim:BASE4-FIG-136-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.45">06.45.</span><span class="paragraph-text">Figure 136, "Namespace Globally Unique Identifier (NGUID), OUI": OUI, EUI64, NGUID, and WWN comparison diagrams describe identifier composition and allocation relationships. Similar appearance does not make formats interchangeable; establish width and definition before identifying vendor and other components.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.5.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 136, printed pages 171, PDF pages 197</p></details>

</details>
<!-- figure-table:BASE4-FIG-137 -->
<details class="field-note" id="figure-BASE4-FIG-137"><summary>Base Figure 137 · Namespace Globally Unique Identifier</summary>
<!-- claim:BASE4-FIG-137-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.46">06.46.</span><span class="paragraph-text">Figure 137, "Namespace Globally Unique Identifier": OUI, EUI64, NGUID, and WWN comparison diagrams describe identifier composition and allocation relationships. Similar appearance does not make formats interchangeable; establish width and definition before identifying vendor and other components.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.5.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 137, printed pages 171, PDF pages 197</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NAA</dt><dd>Network Address Authority, the WWN nibble selecting an identifier format and assignment method.</dd></div></dl>
</details>
<!-- figure-table:BASE4-FIG-138 -->
<details class="field-note" id="figure-BASE4-FIG-138"><summary>Base Figure 138 · Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN</summary>
<!-- claim:BASE4-FIG-138-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.47">06.47.</span><span class="paragraph-text">Figure 138, "Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN": OUI, EUI64, NGUID, and WWN comparison diagrams describe identifier composition and allocation relationships. Similar appearance does not make formats interchangeable; establish width and definition before identifying vendor and other components.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.5.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 138, printed pages 171, PDF pages 197</p></details>

</details>
<!-- figure-table:BASE4-FIG-139 -->
<details class="field-note" id="figure-BASE4-FIG-139"><summary>Base Figure 139 · Controller List Format</summary>
<!-- claim:BASE4-FIG-139-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.48">06.48.</span><span class="paragraph-text">Figure 139, "Controller List Format": A Controller List begins with NUMCIDS and 16-bit controller IDs; a Namespace List directly contains 32-bit NSIDs. Follow each list’s ordering and unused-entry rules without sharing the same header interpretation.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.6.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.6.1, Figure 139, printed pages 172, PDF pages 198</p></details>

</details>
<!-- figure-table:BASE4-FIG-140 -->
<details class="field-note" id="figure-BASE4-FIG-140"><summary>Base Figure 140 · Namespace List Format</summary>
<!-- claim:BASE4-FIG-140-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.49">06.49.</span><span class="paragraph-text">Figure 140, "Namespace List Format": A Controller List begins with NUMCIDS and 16-bit controller IDs; a Namespace List directly contains 32-bit NSIDs. Follow each list’s ordering and unused-entry rules without sharing the same header interpretation.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.6.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.6.2, Figure 140, printed pages 172, PDF pages 198</p></details>

</details>
<!-- figure-table:BASE4-FIG-142 -->
<details class="field-note" id="figure-BASE4-FIG-142"><summary>Base Figure 142 · UTF-8 Input Processing</summary>
<!-- claim:BASE4-FIG-142-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.50">06.50.</span><span class="paragraph-text">Figure 142, "UTF-8 Input Processing": A UTF-8 character can occupy multiple bytes. Distinguish initial and continuation bytes in the input-processing flow. Byte-defined limits still apply to bytes, not character counts.</span></p><details class="source-note"><summary>Sources: Base 2.4 §4.8</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.8, Figure 142, printed pages 175, PDF pages 201</p></details>

</details>
</div>
</section>
</details>
<section id="knowledge-check"><h2 id="review-questions">Check your understanding</h2>
<!-- qa:base-ch4-command-id -->
<details class="review-question" id="qa-base-ch4-command-id"><summary>1. If two SQs use CID=5, how is a completion associated with its command?</summary>
<div data-qa-answer="base-ch4-command-id"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.01">07.01.</span><span class="paragraph-text">CID is unique among outstanding commands within one SQ. Interpret it together with the SQ identifier in the completion information to find the command in the correct queue.</span></p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 140, PDF pages 166</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, printed pages 144-145, PDF pages 170-171</p>
</details></details>
<!-- qa:base-ch4-phase-status -->
<details class="review-question" id="qa-base-ch4-phase-status"><summary>2. Does a CQE with the expected Phase Tag establish command success?</summary>
<div data-qa-answer="base-ch4-phase-status"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.02">07.02.</span><span class="paragraph-text">The Phase Tag identifies a new completion at that location. Success is determined from status information such as Status Code Type and Status Code. Freshness and success are separate decisions.</span></p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.4, printed pages 155-158, PDF pages 181-184</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, printed pages 145-155, PDF pages 171-181</p>
</details></details>
<!-- qa:base-ch4-prp-offset -->
<details class="review-question" id="qa-base-ch4-prp-offset"><summary>3. Why can a PRP1 starting inside a page not imply physically contiguous memory across the next page?</summary>
<div data-qa-answer="base-ch4-prp-offset"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.03">07.03.</span><span class="paragraph-text">PRP1 supplies the page offset of the first segment. Subsequent PRP page addresses or a PRP List find data after a boundary. A logically continuous host buffer need not occupy physically adjacent pages.</span></p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, printed pages 158-159, PDF pages 184-185</p>
</details></details>
<!-- qa:base-ch4-pointer-format -->
<details class="review-question" id="qa-base-ch4-pointer-format"><summary>4. Why inspect PSDT before interpreting DPTR?</summary>
<div data-qa-answer="base-ch4-pointer-format"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="07.04">07.04.</span><span class="paragraph-text">The same DPTR bits can represent PRPs or an SGL depending on the selected format. PSDT and command support determine whether to interpret them as page pointers or segment descriptors.</span></p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 140-142, PDF pages 166-168</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, printed pages 159-166, PDF pages 185-192</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>Specification editions</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
