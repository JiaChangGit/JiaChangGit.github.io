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
<p class="opening">An NVMe command must identify the operation, target namespace, and data location. Its completion must identify the command and report the outcome. This note uses these two directions to explain SQEs, CQEs, and PRP/SGL data pointers.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div><div><dt>NVMe</dt><dd>Non-Volatile Memory Express, the specification family for a host interface to a non-volatile-memory subsystem.</dd></div><div><dt>PRP</dt><dd>Physical Region Page, a pointer format describing a host-addressable data buffer in memory-page units.</dd></div><div><dt>SGL</dt><dd>Scatter Gather List, a descriptor-and-segment format for one or more data-buffer regions.</dd></div></dl>
<h2 id="main-ideas">The main ideas</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>Command contents: SQE</h3><p>Understand command identifiers, opcodes, and data pointers.</p></article>
<article><span class="axis-number">02</span><h3>Completion results: CQE</h3><p>Distinguish new entries, command identity, and status codes.</p></article>
<article><span class="axis-number">03</span><h3>Data addresses: PRP/SGL</h3><p>Connect memory-page concepts to NVMe data transfers.</p></article>
<article><span class="axis-number">04</span><h3>Other shared structures</h3><p>Understand representations for Feature values, identifiers, lists, and text.</p></article>
</div>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div><div><dt>SQE</dt><dd>Submission Queue Entry, one command structure in an SQ.</dd></div></dl>
<p>Command and completion entries are records in queues; data pointers identify the data involved in a transfer. Distinguishing the command record from its transfer data is the starting point for the field layouts.</p>
</section>
<section class="lesson" id="module-sqe"><h2 id="heading-sqe"><span class="section-number">01</span> The common SQE format and command fields</h2>
<p>The common SQE fixes the locations of CDW0, NSID, metadata/data pointers, and CDW10-15. OPC selects the command, CID creates the completion association, and PSDT selects DPTR interpretation. Only after these common fields are established should command-specific CDW10-15 definitions be applied. Figures 92-94 are the coordinate system for all later command construction.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DPTR</dt><dd>Data Pointer, the SQE field identifying a command data buffer.</dd></div><div><dt>NSID</dt><dd>Namespace Identifier, a controller-visible numeric handle for a namespace; the identifier is not the namespace object itself.</dd></div><div><dt>PSDT</dt><dd>PRP or SGL for Data Transfer, the CDW0 field selecting PRP or SGL interpretation for DPTR.</dd></div><div><dt>CID</dt><dd>Command Identifier, used with the SQ identifier to identify an outstanding command.</dd></div></dl>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 160" role="img"><title>CDW0 · 32 bits</title><desc>CDW0 holds command identity, data-pointer type, fused-operation selection, and opcode. Labeled bit ranges determine widths; boxes are sized for readability.</desc><rect x="20" y="35" width="300" height="85" rx="6" class="v-object"/><text x="170.0" y="71.0" text-anchor="middle" font-size="17">CID</text><text x="170.0" y="96.0" text-anchor="middle" font-size="17">31:16</text><rect x="320" y="35" width="90" height="85" rx="6" class="v-command"/><text x="365.0" y="71.0" text-anchor="middle" font-size="17">PSDT</text><text x="365.0" y="96.0" text-anchor="middle" font-size="17">15:14</text><rect x="410" y="35" width="130" height="85" rx="6" class="v-decision"/><text x="475.0" y="71.0" text-anchor="middle" font-size="17">Reserved</text><text x="475.0" y="96.0" text-anchor="middle" font-size="17">13:10</text><rect x="540" y="35" width="90" height="85" rx="6" class="v-command"/><text x="585.0" y="71.0" text-anchor="middle" font-size="17">FUSE</text><text x="585.0" y="96.0" text-anchor="middle" font-size="17">9:8</text><rect x="630" y="35" width="110" height="85" rx="6" class="v-success"/><text x="685.0" y="71.0" text-anchor="middle" font-size="17">OPC</text><text x="685.0" y="96.0" text-anchor="middle" font-size="17">7:0</text></svg></div><figcaption>CDW0 holds command identity, data-pointer type, fused-operation selection, and opcode. Labeled bit ranges determine widths; boxes are sized for readability.</figcaption></figure>

<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASE4-SQE -->
<p>The common Admin and I/O SQE is 64 bytes. CDW0, NSID, data pointers, and CDW10-15 establish the common layout before each command defines command-specific content.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 139-143, PDF pages 165-169</p></details>
<!-- claim:BASE4-CID -->
<p>CID in combination with the Submission Queue identifier uniquely identifies a command. FFFFh should be avoided because the Error Information log uses it when an error is not associated with a particular command.</p><details class="source-note"><summary>Sources: Base 2.4 §4.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 140, PDF pages 166</p></details>
<!-- claim:BASE4-PSDT -->
<p>CDW0.PSDT selects PRP or SGL interpretation for DPTR. An Admin command over PCIe shall use PRPs unless its command definition specifies otherwise.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PCIe</dt><dd>PCI Express, the transport and device interconnect used by an NVMe memory-based controller.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 140-142, PDF pages 166-168</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>CDW0</td><td>Command identity and data-pointer selector</td><td>Common to all commands</td></tr><tr><td>NSID</td><td>Namespace scope</td><td>When unused, clear or use a special value only as the command defines</td></tr><tr><td>MPTR/DPTR</td><td>Metadata and data buffers</td><td>Selected by PSDT and command rules</td></tr><tr><td>CDW10-15</td><td>Command-specific payload</td><td>Never borrow semantics from another command</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>MPTR</dt><dd>Metadata Pointer, the SQE field identifying a separate metadata buffer.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p>Informative example: the same CID can be used on different SQs, but outstanding commands within one SQ must not create an identity collision. The driver tracks commands by (SQID,CID), completes every SQE field and required memory ordering, and only then updates the SQ tail.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SQID</dt><dd>Submission Queue Identifier, the numeric identifier of the SQ containing a command.</dd></div><div><dt>SQ</dt><dd>Submission Queue, the queue into which the host places commands.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASE4-FIG-092 -->
<details class="field-note" id="figure-BASE4-FIG-092"><summary>Base Figure 92 · Command Dword 0</summary>
<!-- claim:BASE4-FIG-092-CLAIM -->
<p>Figure 92, "Command Dword 0": Defines the concrete layout or value relationships for Command Dword 0.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Double word, four bytes or 32 bits; NVMe command fields are commonly identified by CDW number.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 92, printed pages 139-140, PDF pages 165-166</p></details>

</details>
<!-- figure-table:BASE4-FIG-093 -->
<details class="field-note" id="figure-BASE4-FIG-093"><summary>Base Figure 93 · Common Command Format</summary>
<!-- claim:BASE4-FIG-093-CLAIM -->
<p>Figure 93, "Common Command Format": Defines the concrete layout or value relationships for Common Command Format.</p><details class="source-note"><summary>Sources: Base 2.4 §4.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, printed pages 140-142, PDF pages 166-168</p></details>

</details>
<!-- figure-table:BASE4-FIG-094 -->
<details class="field-note" id="figure-BASE4-FIG-094"><summary>Base Figure 94 · Common Command Format - Vendor Specific Commands (Optional)</summary>
<!-- claim:BASE4-FIG-094-CLAIM -->
<p>Figure 94, "Common Command Format - Vendor Specific Commands (Optional)": Defines the concrete layout or value relationships for Common Command Format - Vendor Specific Commands (Optional).</p><details class="source-note"><summary>Sources: Base 2.4 §4.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 94, printed pages 143, PDF pages 169</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NDM</dt><dd>Number of Dwords in Metadata Transfer, the actual metadata-dword count in the standard vendor-specific format.</dd></div><div><dt>NDT</dt><dd>Number of Dwords in Data Transfer, the actual data-dword count in the standard vendor-specific format.</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-cqe-status"><h2 id="heading-cqe-status"><span class="section-number">02</span> CQEs: new entries, command identity, and results</h2>
<p>The host first uses the Phase Tag to determine whether a CQ slot contains a new completion. After ownership is established, SQID/CID recovers the command; SCT then selects the status category before SC, DNR, and CRD are interpreted. Figures 97-109 must be read in this order so a stale CQE or wrong category is not mistaken for a command failure.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CRD</dt><dd>Command Retry Delay, the status field selecting a controller-recommended retry delay.</dd></div><div><dt>DNR</dt><dd>Do Not Retry, a CQE-status bit indicating that retrying the same command is not expected to succeed.</dd></div><div><dt>SCT</dt><dd>Status Code Type, the category selected before interpreting SC.</dd></div><div><dt>CQ</dt><dd>Completion Queue, the queue into which a controller posts command completions.</dd></div><div><dt>SC</dt><dd>Status Code, the specific completion result interpreted in the context of SCT.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASE4-CQE -->
<p>The common CQE is at least 16 bytes. If multiple writes construct it, the Phase Tag shall be updated in the last write so the host does not consume a partial entry.</p><details class="source-note"><summary>Sources: Base 2.4 §4.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, printed pages 144-145, PDF pages 170-171</p></details>
<!-- claim:BASE4-STATUS -->
<p>Status decoding starts with Status Code Type (SCT), then Status Code (SC), together with control bits such as Do Not Retry (DNR). An SC value is not interpreted without its SCT.</p><details class="source-note"><summary>Sources: Base 2.4 §4.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, printed pages 145-155, PDF pages 171-181</p></details>
<!-- claim:BASE4-PHASE -->
<p>The Phase Tag lets the host distinguish a new entry in a circular Completion Queue. After consuming CQEs, the host advances the CQ head doorbell and expects phase inversion on wrap.</p><details class="source-note"><summary>Sources: Base 2.4 §4.2.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.4, printed pages 155-158, PDF pages 181-184</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>SCT</td><td>Status category</td><td>Always decode first</td></tr><tr><td>SC</td><td>Specific result within the category</td><td>Never interpret without SCT</td></tr><tr><td>DNR</td><td>Expectation for retrying the same command</td><td>Not synonymous with permanent hardware failure</td></tr><tr><td>CRD</td><td>Recommended retry-delay selector</td><td>Use only for an applicable status</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p>Informative example: SC value 02h can belong to different status tables under different SCT values. A correct log retains the complete status field and reports P, SCT, SC, DNR, CRD, and the raw 16-bit value. 'SC=2' alone is insufficient for recovery.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>P</dt><dd>Phase Tag, the toggling bit used by the host to decide whether a CQ slot contains a new completion.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASE4-FIG-097 -->
<details class="field-note" id="figure-BASE4-FIG-097"><summary>Base Figure 97 · Common Completion Queue Entry Layout - Admin and All I/O Command Sets</summary>
<!-- claim:BASE4-FIG-097-CLAIM -->
<p>Figure 97, "Common Completion Queue Entry Layout - Admin and All I/O Command Sets": Defines the concrete layout or value relationships for Common Completion Queue Entry Layout - Admin and All I/O Command Sets.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 97, printed pages 144, PDF pages 170</p></details>

</details>
<!-- figure-table:BASE4-FIG-098 -->
<details class="field-note" id="figure-BASE4-FIG-098"><summary>Base Figure 98 · Completion Queue Entry: DW 2</summary>
<!-- claim:BASE4-FIG-098-CLAIM -->
<p>Figure 98, "Completion Queue Entry: DW 2": Shows the queue or command relationship expressed by Completion Queue Entry: DW 2.</p><details class="source-note"><summary>Sources: Base 2.4 §4.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 98, printed pages 144, PDF pages 170</p></details>

</details>
<!-- figure-table:BASE4-FIG-099 -->
<details class="field-note" id="figure-BASE4-FIG-099"><summary>Base Figure 99 · Completion Queue Entry: DW 3</summary>
<!-- claim:BASE4-FIG-099-CLAIM -->
<p>Figure 99, "Completion Queue Entry: DW 3": Shows the queue or command relationship expressed by Completion Queue Entry: DW 3.</p><details class="source-note"><summary>Sources: Base 2.4 §4.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 99, printed pages 145, PDF pages 171</p></details>

</details>
<!-- figure-table:BASE4-FIG-101 -->
<details class="field-note" id="figure-BASE4-FIG-101"><summary>Base Figure 101 · Completion Queue Entry: Status Field</summary>
<!-- claim:BASE4-FIG-101-CLAIM -->
<p>Figure 101, "Completion Queue Entry: Status Field": Defines the concrete layout or value relationships for Completion Queue Entry: Status Field.</p><details class="source-note"><summary>Sources: Base 2.4 §4.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 101, printed pages 145-146, PDF pages 171-172</p></details>

</details>
<!-- figure-table:BASE4-FIG-102 -->
<details class="field-note" id="figure-BASE4-FIG-102"><summary>Base Figure 102 · Status Code - Status Code Type Values</summary>
<!-- claim:BASE4-FIG-102-CLAIM -->
<p>Figure 102, "Status Code - Status Code Type Values": Defines the status/error classification represented by Status Code - Status Code Type Values.</p><details class="source-note"><summary>Sources: Base 2.4 §4.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 102, printed pages 146, PDF pages 172</p></details>

</details>
<!-- figure-table:BASE4-FIG-103 -->
<details class="field-note" id="figure-BASE4-FIG-103"><summary>Base Figure 103 · Status Code - Generic Command Status Values</summary>
<!-- claim:BASE4-FIG-103-CLAIM -->
<p>Figure 103, "Status Code - Generic Command Status Values": Defines the status/error classification represented by Status Code - Generic Command Status Values.</p><details class="source-note"><summary>Sources: Base 2.4 §4.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 103, printed pages 147-150, PDF pages 173-176</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CMB</dt><dd>Controller Memory Buffer, controller-provided memory in which selected queues or data structures may reside.</dd></div></dl>
</details>
<!-- figure-table:BASE4-FIG-104 -->
<details class="field-note" id="figure-BASE4-FIG-104"><summary>Base Figure 104 · Status Code - Command Specific Status Values</summary>
<!-- claim:BASE4-FIG-104-CLAIM -->
<p>Figure 104, "Status Code - Command Specific Status Values": Defines the status/error classification represented by Status Code - Command Specific Status Values.</p><details class="source-note"><summary>Sources: Base 2.4 §4.2.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 104, printed pages 151-152, PDF pages 177-178</p></details>

</details>
<!-- figure-table:BASE4-FIG-105 -->
<details class="field-note" id="figure-BASE4-FIG-105"><summary>Base Figure 105 · Status Code - Command Specific Status Values, I/O Command Set Specific</summary>
<!-- claim:BASE4-FIG-105-CLAIM -->
<p>Figure 105, "Status Code - Command Specific Status Values, I/O Command Set Specific": Defines the status/error classification represented by Status Code - Command Specific Status Values, I/O Command Set Specific.</p><details class="source-note"><summary>Sources: Base 2.4 §4.2.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 105, printed pages 152-153, PDF pages 178-179</p></details>

</details>
<!-- figure-table:BASE4-FIG-107 -->
<details class="field-note" id="figure-BASE4-FIG-107"><summary>Base Figure 107 · Status Code - Media and Data Integrity Error Values</summary>
<!-- claim:BASE4-FIG-107-CLAIM -->
<p>Figure 107, "Status Code - Media and Data Integrity Error Values": Defines the status/error classification represented by Status Code - Media and Data Integrity Error Values.</p><details class="source-note"><summary>Sources: Base 2.4 §4.2.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.2, Figure 107, printed pages 154-155, PDF pages 180-181</p></details>

</details>
<!-- figure-table:BASE4-FIG-108 -->
<details class="field-note" id="figure-BASE4-FIG-108"><summary>Base Figure 108 · Status Code - Path Related Status Values</summary>
<!-- claim:BASE4-FIG-108-CLAIM -->
<p>Figure 108, "Status Code - Path Related Status Values": Defines the status/error classification represented by Status Code - Path Related Status Values.</p><details class="source-note"><summary>Sources: Base 2.4 §4.2.3.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3.3, Figure 108, printed pages 155, PDF pages 181</p></details>

</details>
<!-- figure-table:BASE4-FIG-109 -->
<details class="field-note" id="figure-BASE4-FIG-109"><summary>Base Figure 109 · Phase Tag bit Transition Example</summary>
<!-- claim:BASE4-FIG-109-CLAIM -->
<p>Figure 109, "Phase Tag bit Transition Example": Shows the queue or command relationship expressed by Phase Tag bit Transition Example.</p><details class="source-note"><summary>Sources: Base 2.4 §4.2.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.4, Figure 109, printed pages 156-157, PDF pages 182-183</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-prp"><h2 id="heading-prp"><span class="section-number">03</span> How PRPs describe data across pages</h2>
<p>PRP1 may address any byte within the first memory page, so first-segment capacity is page_size minus offset. If data crosses that page, PRP2 represents either the second page or a PRP List depending on remaining length; later page addresses must be page aligned. Figures 110-113 define address calculation, not merely pointer names.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASE4-PRP -->
<p>A fixed-size PRP entry points to a physical memory page. The first entry may contain a page offset; subsequent PRPs shall obey page alignment, and transfer length determines the required entry count.</p><details class="source-note"><summary>Sources: Base 2.4 §4.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, printed pages 158-159, PDF pages 184-185</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Data stays in first page</td><td>PRP1 is sufficient</td><td>PRP2 does not carry another segment</td></tr><tr><td>Remaining data fits one page</td><td>PRP2 addresses the second data page</td><td>Address is page aligned</td></tr><tr><td>Remaining data exceeds one page</td><td>PRP2 addresses a PRP List</td><td>List entries address data pages</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p>Informative example: with a 4096-byte page, PRP1 offset 1000, and a 9000-byte transfer, the first page carries 4096-1000=3096 bytes. The remaining 5904 bytes require two later pages, so PRP2 addresses a PRP List containing at least two data-page addresses.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASE4-FIG-110 -->
<details class="field-note" id="figure-BASE4-FIG-110"><summary>Base Figure 110 · PRP Entry Layout</summary>
<!-- claim:BASE4-FIG-110-CLAIM -->
<p>Figure 110, "PRP Entry Layout": Defines the concrete layout or value relationships for PRP Entry Layout.</p><details class="source-note"><summary>Sources: Base 2.4 §4.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 110, printed pages 158, PDF pages 184</p></details>

</details>
<!-- figure-table:BASE4-FIG-111 -->
<details class="field-note" id="figure-BASE4-FIG-111"><summary>Base Figure 111 · PRP Entry - Page Base Address and Offset</summary>
<!-- claim:BASE4-FIG-111-CLAIM -->
<p>Figure 111, "PRP Entry - Page Base Address and Offset": Shows how PRP Entry - Page Base Address and Offset maps a transfer onto host-memory locations.</p><details class="source-note"><summary>Sources: Base 2.4 §4.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 111, printed pages 158, PDF pages 184</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>PBAO</dt><dd>Page Base Address and Offset, the first-PRP layout combining a page base address with an in-page offset.</dd></div></dl>
</details>
<!-- figure-table:BASE4-FIG-112 -->
<details class="field-note" id="figure-BASE4-FIG-112"><summary>Base Figure 112 · PRP List Layout for Physically Contiguous Memory Pages</summary>
<!-- claim:BASE4-FIG-112-CLAIM -->
<p>Figure 112, "PRP List Layout for Physically Contiguous Memory Pages": Defines the concrete layout or value relationships for PRP List Layout for Physically Contiguous Memory Pages.</p><details class="source-note"><summary>Sources: Base 2.4 §4.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 112, printed pages 159, PDF pages 185</p></details>

</details>
<!-- figure-table:BASE4-FIG-113 -->
<details class="field-note" id="figure-BASE4-FIG-113"><summary>Base Figure 113 · PRP List Layout for Physically Non-Contiguous Memory Pages</summary>
<!-- claim:BASE4-FIG-113-CLAIM -->
<p>Figure 113, "PRP List Layout for Physically Non-Contiguous Memory Pages": Defines the concrete layout or value relationships for PRP List Layout for Physically Non-Contiguous Memory Pages.</p><details class="source-note"><summary>Sources: Base 2.4 §4.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 113, printed pages 159, PDF pages 185</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CC.MPS</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller. Here CC.MPS selects its MPS member field.</dd></div><div><dt>MPS</dt><dd>Memory Page Size, the controller memory-page-size setting; it affects queue addresses and PRP alignment.</dd></div><div><dt>CC</dt><dd>Controller Configuration, the property through which the host selects settings and enables or disables a controller.</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-sgl"><h2 id="heading-sgl"><span class="section-number">04</span> SGL data and segment descriptors</h2>
<p>An SGL descriptor combines type/subtype, address, and length. A Data Block addresses data, Segment and Last Segment address more descriptors, and Bit Bucket represents data that need not be stored in memory. Figures 114-125 require type-first decoding; blindly following an address before decoding type is incorrect.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASE4-SGL -->
<p>An SGL describes a data buffer through one or more descriptors and segments. SGL length shall equal or exceed the requested transfer length; this report covers only generic descriptors applicable to PCIe.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PCIe</dt><dd>PCI Express, the transport and device interconnect used by an NVMe memory-based controller.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, printed pages 159-166, PDF pages 185-192</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>PRP</td><td>Page-based addresses</td><td>First-page offset plus later-page alignment</td></tr><tr><td>SGL Data Block</td><td>Address plus byte length</td><td>A descriptor represents a data region</td></tr><tr><td>SGL Segment</td><td>Address plus descriptor-list length</td><td>Points to more descriptors, not data</td></tr><tr><td>Bit Bucket</td><td>Consumes transfer length only</td><td>Does not represent a readable or writable memory buffer</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p>A 12 KiB data transfer can use two Data Block descriptors of 8 KiB and 4 KiB. A Segment descriptor instead uses length for the next descriptor list, rather than user-data length.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASE4-FIG-114 -->
<details class="field-note" id="figure-BASE4-FIG-114"><summary>Base Figure 114 · SGL Validation Error Conditions</summary>
<!-- claim:BASE4-FIG-114-CLAIM -->
<p>Figure 114, "SGL Validation Error Conditions": Defines the status/error classification represented by SGL Validation Error Conditions.</p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 114, printed pages 161, PDF pages 187</p></details>

</details>
<!-- figure-table:BASE4-FIG-115 -->
<details class="field-note" id="figure-BASE4-FIG-115"><summary>Base Figure 115 · SGL Segment</summary>
<!-- claim:BASE4-FIG-115-CLAIM -->
<p>Figure 115, "SGL Segment": Shows how SGL Segment maps a transfer onto host-memory locations.</p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 115, printed pages 161, PDF pages 187</p></details>

</details>
<!-- figure-table:BASE4-FIG-116 -->
<details class="field-note" id="figure-BASE4-FIG-116"><summary>Base Figure 116 · Generic SGL Descriptor Format</summary>
<!-- claim:BASE4-FIG-116-CLAIM -->
<p>Figure 116, "Generic SGL Descriptor Format": Defines the concrete layout or value relationships for Generic SGL Descriptor Format.</p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 116, printed pages 161, PDF pages 187</p></details>

</details>
<!-- figure-table:BASE4-FIG-117 -->
<details class="field-note" id="figure-BASE4-FIG-117"><summary>Base Figure 117 · SGL Descriptor Type</summary>
<!-- claim:BASE4-FIG-117-CLAIM -->
<p>Figure 117, "SGL Descriptor Type": Defines the concrete layout or value relationships for SGL Descriptor Type.</p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 117, printed pages 161-162, PDF pages 187-188</p></details>

</details>
<!-- figure-table:BASE4-FIG-118 -->
<details class="field-note" id="figure-BASE4-FIG-118"><summary>Base Figure 118 · SGL Descriptor Sub Type Values</summary>
<!-- claim:BASE4-FIG-118-CLAIM -->
<p>Figure 118, "SGL Descriptor Sub Type Values": Defines the concrete layout or value relationships for SGL Descriptor Sub Type Values.</p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 118, printed pages 162, PDF pages 188</p></details>

</details>
<!-- figure-table:BASE4-FIG-119 -->
<details class="field-note" id="figure-BASE4-FIG-119"><summary>Base Figure 119 · SGL Data Block descriptor</summary>
<!-- claim:BASE4-FIG-119-CLAIM -->
<p>Figure 119, "SGL Data Block descriptor": Defines the concrete layout or value relationships for SGL Data Block descriptor.</p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 119, printed pages 162-163, PDF pages 188-189</p></details>

</details>
<!-- figure-table:BASE4-FIG-120 -->
<details class="field-note" id="figure-BASE4-FIG-120"><summary>Base Figure 120 · SGL Bit Bucket descriptor</summary>
<!-- claim:BASE4-FIG-120-CLAIM -->
<p>Figure 120, "SGL Bit Bucket descriptor": Defines the concrete layout or value relationships for SGL Bit Bucket descriptor.</p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 120, printed pages 163, PDF pages 189</p></details>

</details>
<!-- figure-table:BASE4-FIG-121 -->
<details class="field-note" id="figure-BASE4-FIG-121"><summary>Base Figure 121 · SGL Segment descriptor</summary>
<!-- claim:BASE4-FIG-121-CLAIM -->
<p>Figure 121, "SGL Segment descriptor": Defines the concrete layout or value relationships for SGL Segment descriptor.</p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 121, printed pages 163, PDF pages 189</p></details>

</details>
<!-- figure-table:BASE4-FIG-122 -->
<details class="field-note" id="figure-BASE4-FIG-122"><summary>Base Figure 122 · SGL Last Segment descriptor</summary>
<!-- claim:BASE4-FIG-122-CLAIM -->
<p>Figure 122, "SGL Last Segment descriptor": Defines the concrete layout or value relationships for SGL Last Segment descriptor.</p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 122, printed pages 164, PDF pages 190</p></details>

</details>
<!-- figure-table:BASE4-FIG-125 -->
<details class="field-note" id="figure-BASE4-FIG-125"><summary>Base Figure 125 · SGL Read Example</summary>
<!-- claim:BASE4-FIG-125-CLAIM -->
<p>Figure 125, "SGL Read Example": Shows how SGL Read Example maps a transfer onto host-memory locations.</p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2.1, Figure 125, printed pages 166, PDF pages 192</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-identity-text"><h2 id="heading-identity-text"><span class="section-number">05</span> Feature values, identifiers, lists, and strings</h2>
<p>Establish what a value represents before interpreting it: Feature values distinguish active from saved state, identifiers have an identity scope, and lists and strings each have layout and length rules.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:BASE4-FEATURE -->
<p>A Feature may have default, saved, and current values. Saved-value support and persistence across resets or power cycles are determined from SSFS and each Feature capability.</p><details class="source-note"><summary>Sources: Base 2.4 §4.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.4, printed pages 166-169, PDF pages 192-195</p></details>
<!-- claim:BASE4-IDENTIFIER -->
<p>VID/SSVID, SN/MN, IEEE OUI, EUI64, NGUID, and UUID differ in origin, length, and uniqueness scope and are not interchangeable. This section is informative.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>EUI64</dt><dd>64-bit Extended Unique Identifier, a 64-bit identifier constructed from IEEE-assigned space.</dd></div><div><dt>NGUID</dt><dd>Namespace Globally Unique Identifier, a 128-bit global identifier for a namespace.</dd></div><div><dt>SSVID</dt><dd>Subsystem Vendor ID, the PCI identifier for a subsystem vendor.</dd></div><div><dt>UUID</dt><dd>Universally Unique Identifier, a 128-bit identifier whose association scope is defined by the containing structure.</dd></div><div><dt>OUI</dt><dd>Organizationally Unique Identifier, an IEEE-assigned identifier prefix for an organization.</dd></div><div><dt>VID</dt><dd>Vendor ID, a PCI-SIG-assigned identifier for a vendor.</dd></div><div><dt>MN</dt><dd>Model Number, a string identifying a product model.</dd></div><div><dt>SN</dt><dd>Serial Number, a string identifying a product instance.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5, printed pages 169-172, PDF pages 195-198</p></details>
<!-- claim:BASE4-LISTS -->
<p>A Controller List starts with NUMCIDS and then up to 2047 ascending 16-bit controller identifiers. A Namespace List has no count header and directly lists ascending 32-bit NSIDs. Unused entries in both lists are zero filled.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.6</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.6, printed pages 172-173, PDF pages 198-199</p></details>
<!-- claim:BASE4-UTF8 -->
<p>UTF-8 input processing validates encoding, prohibited code points, and truncation using the specified flow; an arbitrary byte sequence is not automatically a valid string.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>UTF-8</dt><dd>Unicode Transformation Format - 8-bit, a text encoding that represents a Unicode code point with one to four bytes.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.8</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.8, printed pages 175, PDF pages 201</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>VID/SSVID</td><td>Vendor/subsystem-vendor identity</td><td>Assignment authorities differ</td></tr><tr><td>SN/MN</td><td>Product instance/model strings</td><td>Interpret fixed fields and padding</td></tr><tr><td>EUI64/NGUID/UUID</td><td>Different formats and uniqueness scopes</td><td>Similar length does not make them interchangeable</td></tr><tr><td>List</td><td>Count plus identifiers</td><td>Validate count before iteration</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>EUI64</dt><dd>64-bit Extended Unique Identifier, a 64-bit identifier constructed from IEEE-assigned space.</dd></div><div><dt>NGUID</dt><dd>Namespace Globally Unique Identifier, a 128-bit global identifier for a namespace.</dd></div><div><dt>SSVID</dt><dd>Subsystem Vendor ID, the PCI identifier for a subsystem vendor.</dd></div><div><dt>UUID</dt><dd>Universally Unique Identifier, a 128-bit identifier whose association scope is defined by the containing structure.</dd></div><div><dt>VID</dt><dd>Vendor ID, a PCI-SIG-assigned identifier for a vendor.</dd></div><div><dt>MN</dt><dd>Model Number, a string identifying a product model.</dd></div><div><dt>SN</dt><dd>Serial Number, a string identifying a product instance.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p>A three-controller list starts with NUMCIDS=3 followed by three 16-bit IDs. A three-namespace list starts directly with the first 32-bit NSID. UTF-8 byte length also differs from character count: “中” occupies three bytes.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>UTF-8</dt><dd>Unicode Transformation Format - 8-bit, a text encoding that represents a Unicode code point with one to four bytes.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:BASE4-FIG-126 -->
<details class="field-note" id="figure-BASE4-FIG-126"><summary>Base Figure 126 · Current Value after Reset with Scope of Entire NVM Subsystem</summary>
<!-- claim:BASE4-FIG-126-CLAIM -->
<p>Figure 126, "Current Value after Reset with Scope of Entire NVM Subsystem": Shows the object or capacity relationships in Current Value after Reset with Scope of Entire NVM Subsystem.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.4, Figure 126, printed pages 167, PDF pages 193</p></details>

</details>
<!-- figure-table:BASE4-FIG-127 -->
<details class="field-note" id="figure-BASE4-FIG-127"><summary>Base Figure 127 · Current Value after Reset with Scope of Subset of the NVM Subsystem</summary>
<!-- claim:BASE4-FIG-127-CLAIM -->
<p>Figure 127, "Current Value after Reset with Scope of Subset of the NVM Subsystem": Shows the object or capacity relationships in Current Value after Reset with Scope of Subset of the NVM Subsystem.</p><details class="source-note"><summary>Sources: Base 2.4 §4.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.4, Figure 127, printed pages 168, PDF pages 194</p></details>

</details>
<!-- figure-table:BASE4-FIG-128 -->
<details class="field-note" id="figure-BASE4-FIG-128"><summary>Base Figure 128 · PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)</summary>
<!-- claim:BASE4-FIG-128-CLAIM -->
<p>Figure 128, "PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)": Shows the object or capacity relationships in PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID).</p><details class="source-note"><summary>Sources: Base 2.4 §4.5.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.1, Figure 128, printed pages 169, PDF pages 195</p></details>

</details>
<!-- figure-table:BASE4-FIG-129 -->
<details class="field-note" id="figure-BASE4-FIG-129"><summary>Base Figure 129 · Serial Number (SN) and Model Number (MN)</summary>
<!-- claim:BASE4-FIG-129-CLAIM -->
<p>Figure 129, "Serial Number (SN) and Model Number (MN)": Defines the identifier composition or namespace of values shown by Serial Number (SN) and Model Number (MN).</p><details class="source-note"><summary>Sources: Base 2.4 §4.5.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.2, Figure 129, printed pages 170, PDF pages 196</p></details>

</details>
<!-- figure-table:BASE4-FIG-130 -->
<details class="field-note" id="figure-BASE4-FIG-130"><summary>Base Figure 130 · IEEE OUI Identifier (IEEE)</summary>
<!-- claim:BASE4-FIG-130-CLAIM -->
<p>Figure 130, "IEEE OUI Identifier (IEEE)": Defines the identifier composition or namespace of values shown by IEEE OUI Identifier (IEEE).</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>OUI</dt><dd>Organizationally Unique Identifier, an IEEE-assigned identifier prefix for an organization.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.5.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.3, Figure 130, printed pages 170, PDF pages 196</p></details>

</details>
<!-- figure-table:BASE4-FIG-131 -->
<details class="field-note" id="figure-BASE4-FIG-131"><summary>Base Figure 131 · IEEE Extended Unique Identifier (EUI64), MA-L Format</summary>
<!-- claim:BASE4-FIG-131-CLAIM -->
<p>Figure 131, "IEEE Extended Unique Identifier (EUI64), MA-L Format": Defines the concrete layout or value relationships for IEEE Extended Unique Identifier (EUI64), MA-L Format.</p><details class="source-note"><summary>Sources: Base 2.4 §4.5.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 131, printed pages 170, PDF pages 196</p></details>

</details>
<!-- figure-table:BASE4-FIG-132 -->
<details class="field-note" id="figure-BASE4-FIG-132"><summary>Base Figure 132 · IEEE Extended Unique Identifier (EUI64), OUI Identifier</summary>
<!-- claim:BASE4-FIG-132-CLAIM -->
<p>Figure 132, "IEEE Extended Unique Identifier (EUI64), OUI Identifier": Defines the identifier composition or namespace of values shown by IEEE Extended Unique Identifier (EUI64), OUI Identifier.</p><details class="source-note"><summary>Sources: Base 2.4 §4.5.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 132, printed pages 170, PDF pages 196</p></details>

</details>
<!-- figure-table:BASE4-FIG-133 -->
<details class="field-note" id="figure-BASE4-FIG-133"><summary>Base Figure 133 · IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)</summary>
<!-- claim:BASE4-FIG-133-CLAIM -->
<p>Figure 133, "IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)": Defines the identifier composition or namespace of values shown by IEEE Extended Unique Identifier (EUI64), Ext. ID (cont).</p><details class="source-note"><summary>Sources: Base 2.4 §4.5.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 133, printed pages 170-171, PDF pages 196-197</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NAA</dt><dd>Network Address Authority, the WWN nibble selecting an identifier format and assignment method.</dd></div><div><dt>WWN</dt><dd>World Wide Name, a global naming format used for storage and networking devices.</dd></div></dl>
</details>
<!-- figure-table:BASE4-FIG-134 -->
<details class="field-note" id="figure-BASE4-FIG-134"><summary>Base Figure 134 · MA-L similarity to WWN</summary>
<!-- claim:BASE4-FIG-134-CLAIM -->
<p>Figure 134, "MA-L similarity to WWN": Defines the identifier composition or namespace of values shown by MA-L similarity to WWN.</p><details class="source-note"><summary>Sources: Base 2.4 §4.5.4</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.4, Figure 134, printed pages 171, PDF pages 197</p></details>

</details>
<!-- figure-table:BASE4-FIG-135 -->
<details class="field-note" id="figure-BASE4-FIG-135"><summary>Base Figure 135 · Namespace Globally Unique Identifier (NGUID)</summary>
<!-- claim:BASE4-FIG-135-CLAIM -->
<p>Figure 135, "Namespace Globally Unique Identifier (NGUID)": Defines the identifier composition or namespace of values shown by Namespace Globally Unique Identifier (NGUID).</p><details class="source-note"><summary>Sources: Base 2.4 §4.5.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 135, printed pages 171, PDF pages 197</p></details>

</details>
<!-- figure-table:BASE4-FIG-136 -->
<details class="field-note" id="figure-BASE4-FIG-136"><summary>Base Figure 136 · Namespace Globally Unique Identifier (NGUID), OUI</summary>
<!-- claim:BASE4-FIG-136-CLAIM -->
<p>Figure 136, "Namespace Globally Unique Identifier (NGUID), OUI": Defines the identifier composition or namespace of values shown by Namespace Globally Unique Identifier (NGUID), OUI.</p><details class="source-note"><summary>Sources: Base 2.4 §4.5.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 136, printed pages 171, PDF pages 197</p></details>

</details>
<!-- figure-table:BASE4-FIG-137 -->
<details class="field-note" id="figure-BASE4-FIG-137"><summary>Base Figure 137 · Namespace Globally Unique Identifier</summary>
<!-- claim:BASE4-FIG-137-CLAIM -->
<p>Figure 137, "Namespace Globally Unique Identifier": Defines the identifier composition or namespace of values shown by Namespace Globally Unique Identifier.</p><details class="source-note"><summary>Sources: Base 2.4 §4.5.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 137, printed pages 171, PDF pages 197</p></details>

</details>
<!-- figure-table:BASE4-FIG-138 -->
<details class="field-note" id="figure-BASE4-FIG-138"><summary>Base Figure 138 · Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN</summary>
<!-- claim:BASE4-FIG-138-CLAIM -->
<p>Figure 138, "Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN": Defines the identifier composition or namespace of values shown by Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN.</p><details class="source-note"><summary>Sources: Base 2.4 §4.5.5</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.5.5, Figure 138, printed pages 171, PDF pages 197</p></details>

</details>
<!-- figure-table:BASE4-FIG-139 -->
<details class="field-note" id="figure-BASE4-FIG-139"><summary>Base Figure 139 · Controller List Format</summary>
<!-- claim:BASE4-FIG-139-CLAIM -->
<p>Figure 139, "Controller List Format": Defines the concrete layout or value relationships for Controller List Format.</p><details class="source-note"><summary>Sources: Base 2.4 §4.6.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.6.1, Figure 139, printed pages 172, PDF pages 198</p></details>

</details>
<!-- figure-table:BASE4-FIG-140 -->
<details class="field-note" id="figure-BASE4-FIG-140"><summary>Base Figure 140 · Namespace List Format</summary>
<!-- claim:BASE4-FIG-140-CLAIM -->
<p>Figure 140, "Namespace List Format": Defines the concrete layout or value relationships for Namespace List Format.</p><details class="source-note"><summary>Sources: Base 2.4 §4.6.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.6.2, Figure 140, printed pages 172, PDF pages 198</p></details>

</details>
<!-- figure-table:BASE4-FIG-142 -->
<details class="field-note" id="figure-BASE4-FIG-142"><summary>Base Figure 142 · UTF-8 Input Processing</summary>
<!-- claim:BASE4-FIG-142-CLAIM -->
<p>Figure 142, "UTF-8 Input Processing": Shows the input-validation sequence required by UTF-8 Input Processing.</p><details class="source-note"><summary>Sources: Base 2.4 §4.8</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.8, Figure 142, printed pages 175, PDF pages 201</p></details>

</details>
</details>
</section>
<section id="knowledge-check"><h2 id="review-questions">Check your understanding</h2>
<!-- qa:base-ch4-command-id -->
<details class="review-question" id="qa-base-ch4-command-id"><summary>1. If two SQs use CID=5, how is a completion associated with its command?</summary>
<div data-qa-answer="base-ch4-command-id"><p>CID is unique among outstanding commands within one SQ. Interpret it together with the SQ identifier in the completion information to locate the command in the correct queue.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 140, PDF pages 166</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, printed pages 144-145, PDF pages 170-171</p>
</details></details>
<!-- qa:base-ch4-phase-status -->
<details class="review-question" id="qa-base-ch4-phase-status"><summary>2. Does a CQE with the expected Phase Tag establish command success?</summary>
<div data-qa-answer="base-ch4-phase-status"><p>The Phase Tag identifies a new completion at that location. Success is determined from status information such as Status Code Type and Status Code. Freshness and success are separate decisions.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.4, printed pages 155-158, PDF pages 181-184</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, printed pages 145-155, PDF pages 171-181</p>
</details></details>
<!-- qa:base-ch4-prp-offset -->
<details class="review-question" id="qa-base-ch4-prp-offset"><summary>3. Why can a PRP1 starting inside a page not imply physically contiguous memory across the next page?</summary>
<div data-qa-answer="base-ch4-prp-offset"><p>PRP1 supplies the page offset of the first segment. Subsequent PRP page addresses or a PRP List locate data after a boundary. A logically continuous host buffer need not occupy physically adjacent pages.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, printed pages 158-159, PDF pages 184-185</p>
</details></details>
<!-- qa:base-ch4-pointer-format -->
<details class="review-question" id="qa-base-ch4-pointer-format"><summary>4. Why inspect PSDT before interpreting DPTR?</summary>
<div data-qa-answer="base-ch4-pointer-format"><p>The same DPTR bits can represent PRPs or an SGL depending on the selected format. PSDT and command support determine whether to interpret them as page pointers or segment descriptors.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, printed pages 140-142, PDF pages 166-168</p>
<p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, printed pages 159-166, PDF pages 185-192</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>Specification editions</summary><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
