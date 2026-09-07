---
permalink: /nvme/nvm-command-set-1-3-en/
layout: post
read_time: true
show_date: true
title: "NVM Command Set 1.3: Logical blocks, I/O commands, and data protection"
date: 2026-09-03
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
[繁體中文]({% post_url 2026-09-03-nvme-nvm-command-set-1-3-zh-tw %})


<div class="nvme-note">
<section id="topic-overview" class="topic-overview">
<p class="reader-paragraph opening"><span class="paragraph-number" aria-label="00.01">00.01.</span>The NVM Command Set defines how a host reads, writes, and manages storage in logical blocks. Its central connections are data formats, command behavior, data integrity, and resource management: a command’s applicable conditions depend on the namespace format, advertised capabilities, and settings.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl>
<h2 id="main-ideas">The main ideas</h2>
<div class="topic-map">
<article><span class="axis-number">01</span><h3>Storage and formats</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-label="00.02">00.02.</span>Establish namespace capacity, LBA formats, and the relationship between data and metadata.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>namespace</dt><dd>Namespace, a formatted quantity of non-volatile memory accessed by a host through a controller.</dd></div><div><dt>metadata</dt><dd>Additional information stored with a logical block; it can contain protection information or serve other purposes.</dd></div><div><dt>LBA</dt><dd>Logical Block Address, measured in blocks of the selected format.</dd></div></dl></article>
<article><span class="axis-number">02</span><h3>Command behavior</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-label="00.03">00.03.</span>Compare Read, Write, Compare, Verify, Copy, and space-management commands and their completion conditions.</p></article>
<article><span class="axis-number">03</span><h3>Integrity and ordering</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-label="00.04">00.04.</span>Understand atomicity, command dependencies, Protection Information, and the scope of checks.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Protection Information</dt><dd>PI: protection fields containing a Guard and tags for checking data and its associated information.</dd></div></dl></article>
<article><span class="axis-number">04</span><h3>Capabilities and resources</h3><p class="reader-paragraph axis-description"><span class="paragraph-number" aria-label="00.05">00.05.</span>Use Identify, Features, and logs to understand format selection, performance limits, and advanced resource features.</p></article>
</div>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>Protection Information</dt><dd>PI: protection fields containing a Guard and tags for checking data and its associated information.</dd></div><div><dt>metadata</dt><dd>Additional information stored with a logical block; it can contain protection information or serve other purposes.</dd></div><div><dt>LBA</dt><dd>Logical Block Address, measured in blocks of the selected format.</dd></div></dl>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="00.06">00.06.</span>The host submits commands through a submission queue, and the controller reports results through a completion queue. The Base specification defines this shared mechanism; this note focuses on how commands act on logical blocks within a namespace.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>Host</dt><dd>The system running the operating system and issuing NVMe commands.</dd></div></dl>
</section>
<section class="lesson" id="module-nvmcs-foundation"><h2 id="heading-nvmcs-foundation"><span class="section-number">01</span> Logical blocks, formats, and units</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.01">01.01.</span>The host addresses namespace storage through logical block addresses. Establish data and metadata sizes before calculating buffers, interpreting command ranges, and choosing data protection. When reading a Format Index, keep index and offset separate: an index selects a format, while an offset is measured from a start.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>logical block</dt><dd>An addressable unit in a namespace; its data size is determined by the active format.</dd></div><div><dt>Format Index</dt><dd>The number selecting a corresponding LBAF/ELBAF format description.</dd></div><div><dt>offset</dt><dd>offset: a displacement measured from a stated start. It answers “how far from the start,” unlike an index.</dd></div><div><dt>index</dt><dd>index: selects an item or format in a list. It answers “which one,” not “how far from the start.”</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-FOUNDATION -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.02">01.02.</span>The NVM Command Set supplements Base with logical-block semantics. Logical block data size excludes metadata, whereas logical block size includes it. NVM uses CSI 00h; equal numeric values in commands, Features, logs, and Identify belong to different identifier spaces.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>logical block</dt><dd>An addressable unit in a namespace; its data size is determined by the active format.</dd></div><div><dt>CSI</dt><dd>I/O Command Set Identifier: selects an I/O command set; NVM uses 00h.</dd></div><div><dt>NVM</dt><dd>Non-Volatile Memory, memory that retains data without power.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §1.1-1.6; 4.1.3.9; 4.1.4.8; 4.1.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §1.1-1.6; 4.1.3.9; 4.1.4.8; 4.1.5, printed pages 9-12,73-75,79-83, PDF pages 9-12,73-75,79-83</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>LBADS</td><td>data bytes = 2^LBADS</td><td>Add MS to obtain logical block size</td></tr><tr><td>Format Index</td><td>Selects both LBAF and ELBAF</td><td>Data size alone is insufficient</td></tr><tr><td>Specification family</td><td>Base defines common mechanisms</td><td>Dependencies carry separate Base citations</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>Format Index</dt><dd>The number selecting a corresponding LBAF/ELBAF format description.</dd></div><div><dt>ELBAF</dt><dd>Extended LBA Format: pairs with LBAF at the same index and adds PI format and Storage Tag size.</dd></div><div><dt>LBADS</dt><dd>LBA Data Size exponent; data bytes=2^LBADS, while zero means currently unavailable.</dd></div><div><dt>index</dt><dd>index: selects an item or format in a list. It answers “which one,” not “how far from the start.”</dd></div><div><dt>LBAF</dt><dd>LBA Format: a description of a logical-block format, including data and metadata sizes.</dd></div><div><dt>MS</dt><dd>Metadata Size; Metadata bytes per logical block.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="01.03">01.03.</span>With LBADS=0Ch and MS=16, data occupies 4096 bytes and the complete logical block 4112 bytes. FID 28h configures limits while LID 28h reports the capability graph, despite their equal numbers.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>LBADS</dt><dd>LBA Data Size exponent; data bytes=2^LBADS, while zero means currently unavailable.</dd></div><div><dt>FID</dt><dd>Feature Identifier: selects the Feature to read or configure.</dd></div><div><dt>LID</dt><dd>Log Page Identifier: selects the type of log page to read.</dd></div><div><dt>MS</dt><dd>Metadata Size; Metadata bytes per logical block.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-001 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-001"><summary>NVM Figure 1 · NVMe Family of Specifications</summary>
<!-- claim:NVMCS13-NVM-FIG-001-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.04">01.04.</span>Figure 1, "NVMe Family of Specifications": Read by functional layer: Base supplies shared mechanisms, PCIe the local transport, and NVM logical-block command semantics.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express, the specification family for a host interface to a non-volatile-memory subsystem.</dd></div><div><dt>PCIe</dt><dd>PCI Express, the transport and device interconnect used by an NVMe memory-based controller.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §1.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §1.1, Figure 1, printed pages 9, PDF pages 9</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>PCIe</dt><dd>PCI Express, the transport and device interconnect used by an NVMe memory-based controller.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-002 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-002"><summary>NVM Figure 2 · Acronym definitions</summary>
<!-- claim:NVMCS13-NVM-FIG-002-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="01.05">01.05.</span>Figure 2, "Acronym definitions": LBA addresses a logical block, not a byte offset; converting to data bytes also requires LBADS from the selected format.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>offset</dt><dd>offset: a displacement measured from a stated start. It answers “how far from the start,” unlike an index.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §1.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §1.5, Figure 2, printed pages 11, PDF pages 11</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-capacity"><h2 id="heading-nvmcs-capacity"><span class="section-number">02</span> Namespace capacity and allocation</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.01">02.01.</span>Separate logical address space from allocated resources before considering writes and deallocation. Returned data and allocation state answer different questions.</p>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 260" role="img"><title>Addressable, allocatable, and allocated are distinct</title><desc>Example: NSZE=1000, NCAP=800, NUSE=600. The LBA address range is distinct from current allocation.</desc><rect x="20" y="20" width="720" height="70" rx="6" class="v-object"/><text x="380.0" y="48.5" text-anchor="middle" font-size="17">NSZE = 1000</text><text x="380.0" y="73.5" text-anchor="middle" font-size="17">LBA 0 … 999</text><rect x="20" y="110" width="576" height="55" rx="6" class="v-command"/><text x="308.0" y="143.5" text-anchor="middle" font-size="17">NCAP = 800</text><rect x="20" y="185" width="432" height="55" rx="6" class="v-success"/><text x="236.0" y="218.5" text-anchor="middle" font-size="17">NUSE = 600</text></svg></div><figcaption>Example: NSZE=1000, NCAP=800, NUSE=600. The LBA address range is distinct from current allocation.</figcaption></figure>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NCAP</dt><dd>Namespace Capacity, the maximum number of simultaneously allocated logical blocks.</dd></div><div><dt>NSZE</dt><dd>Namespace Size, the total number of addressable logical blocks.</dd></div><div><dt>NUSE</dt><dd>Namespace Utilization, the number of currently allocated logical blocks.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-CAPACITY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.02">02.02.</span>NSZE ≥ NCAP ≥ NUSE: NSZE defines the addressable range, NCAP limits simultaneously allocated blocks, and NUSE counts current allocation. THINP=0 requires NCAP=NSZE. NVMCAP is measured in bytes and is not necessarily NSZE multiplied by data size.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVMCAP</dt><dd>NVM Capacity, measured in bytes; not directly comparable to NSZE/NCAP logical-block counts.</dd></div><div><dt>THINP</dt><dd>Thin Provisioning, the NSFEAT bit governing whether NCAP may be below NSZE and whether the controller tracks NUSE.</dd></div><div><dt>NCAP</dt><dd>Namespace Capacity, the maximum number of simultaneously allocated logical blocks.</dd></div><div><dt>NSZE</dt><dd>Namespace Size, the total number of addressable logical blocks.</dd></div><div><dt>NUSE</dt><dd>Namespace Utilization, the number of currently allocated logical blocks.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.1.1; 4.1.5.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1; 4.1.5.1, printed pages 13-14,85-93, PDF pages 13-14,85-93</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>NSZE</td><td>Valid LBAs run from 0 to NSZE−1</td><td>Out-of-range differs from capacity exhaustion</td></tr><tr><td>THINP</td><td>Requires NUSE tracking when supported</td><td>Without support NUSE may remain NCAP</td></tr><tr><td>Allocation</td><td>Write, the Copy destination, and WU allocate</td><td>Read/Verify do not change deallocation state</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>THINP</dt><dd>Thin Provisioning, the NSFEAT bit governing whether NCAP may be below NSZE and whether the controller tracks NUSE.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="02.03">02.03.</span>NSZE=1000, NCAP=800, NUSE=600 can describe a valid thin namespace. LBA 900 is addressable, but additional allocation remains subject to the 800-block capacity.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-123 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-123"><summary>NVM Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</summary>
<!-- claim:NVMCS13-NVM-FIG-123-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="02.04">02.04.</span>Figure 123, "Identify – Identify Namespace Data Structure, NVM Command Set": Partition this multipage structure into capacity, format capability/current format, deallocation, atomicity, performance, Copy limits, and identifiers. Apply each capability gate before using its values.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.5.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1, Figure 123, printed pages 85-93, PDF pages 85-93</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>FLBAS</dt><dd>Formatted LBA Size, selecting the LBA format used by a namespace and related metadata-placement control.</dd></div><div><dt>NLBAF</dt><dd>Zero-based count of LBA formats with common attributes.</dd></div><div><dt>DPS</dt><dd>End-to-end Data Protection Type Settings, the create field selecting Protection Information type and position.</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-identify"><h2 id="heading-nvmcs-identify"><span class="section-number">03</span> Identify: multiple structures for one namespace</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.01">03.01.</span>Write down the roles of CNS, CSI, NSID, and Format Index for each query. Zero-filled results have different meanings across queries and do not always mean absent or unsupported.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NSID</dt><dd>Namespace Identifier; Identifies the namespace addressed by a command.</dd></div><div><dt>CNS</dt><dd>Controller or Namespace Structure: the Identify selector for a response data structure.</dd></div><div><dt>CSI</dt><dd>I/O Command Set Identifier: selects an I/O command set; NVM uses 00h.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-IDENTIFY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.02">03.02.</span>NVM uses CSI=00h. Complete namespace information combines the command-set-independent CNS 08h structure, the NVM CNS 00h structure, and NVM-specific CNS 05h/CSI 00h. CNS 01h and 06h supply controller information.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>controller</dt><dd>Controller, the entity that implements the NVMe interface, fetches commands, and reports completions.</dd></div><div><dt>CNS</dt><dd>Controller or Namespace Structure: the Identify selector for a response data structure.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5, printed pages 83-110, PDF pages 83-110</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>CNS 00h / 05h</td><td>Basic/extended NVM namespace fields</td><td>FLBAS selects the active FIDX; MC/DPC are capabilities</td></tr><tr><td>CNS 01h / 06h</td><td>Common-location AWUN fields and NVM-specific limits</td><td>06h VSL/WZSL fields require variant bits</td></tr><tr><td>CNS 11h / 1Bh</td><td>Allocated-namespace information</td><td>Different from active-namespace queries</td></tr><tr><td>CNS 09h / 0Ah</td><td>Capability queries by FIDX</td><td>Common=No fields are zeroed</td></tr><tr><td>CNS 16h</td><td>Namespace granularity list</td><td>GDM determines descriptor-to-format mapping</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>FLBAS</dt><dd>Formatted LBA Size, selecting the LBA format used by a namespace and related metadata-placement control.</dd></div><div><dt>AWUN</dt><dd>Atomic Write Unit Normal, the controller’s zero-based normal atomic-write size.</dd></div><div><dt>WZSL</dt><dd>Write Zeroes Size Limit; A Write Zeroes size limit, interpreted with its variant capability.</dd></div><div><dt>VSL</dt><dd>Verify Size Limit; A Verify size limit, interpreted with its variant capability.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="03.03">03.03.</span>For NSID=7, read FLBAS and use that index in both LBAF and ELBAF. To query capabilities of FIDX=3 before creation, use 09h/0Ah, CSI=0, NSID=0, FIDX=3, plus common capabilities from CNS08h.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>ELBAF</dt><dd>Extended LBA Format: pairs with LBAF at the same index and adds PI format and Storage Tag size.</dd></div><div><dt>LBAF</dt><dd>LBA Format: a description of a logical-block format, including data and metadata sizes.</dd></div><div><dt>NSID</dt><dd>Namespace Identifier; Identifies the namespace addressed by a command.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-122 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-122"><summary>NVM Figure 122 · CNS Values</summary>
<!-- claim:NVMCS13-NVM-FIG-122-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.04">03.04.</span>Figure 122, "CNS Values": Select the structure with CNS, then check NSID/CSI applicability. Namespace information from 00h, 05h, and 08h is complementary; 09h/0Ah use FIDX.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5, Figure 122, printed pages 83-84, PDF pages 83-84</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-126 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-126"><summary>NVM Figure 126 · Identify – Identify Controller data structure, NVM Command Set Specific Fields</summary>
<!-- claim:NVMCS13-NVM-FIG-126-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.05">03.05.</span>Figure 126, "Identify – Identify Controller data structure, NVM Command Set Specific Fields": Controller atomicity values apply unless qualified namespace values override them. AWUPF does not exceed AWUN; ACWU specifically governs fused Compare-and-Write.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>AWUPF</dt><dd>Atomic Write Unit Power Fail, the zero-based atomic size for failure conditions.</dd></div><div><dt>ACWU</dt><dd>Atomic Compare and Write Unit; The controller fused compare-and-write size limit.</dd></div><div><dt>AWUN</dt><dd>Atomic Write Unit Normal, the controller’s zero-based normal atomic-write size.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.5.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.2, Figure 126, printed pages 94-96, PDF pages 94-96</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>AWUPF</dt><dd>Atomic Write Unit Power Fail, the zero-based atomic size for failure conditions.</dd></div><div><dt>ACWU</dt><dd>Atomic Compare and Write Unit; The controller fused compare-and-write size limit.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-129 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-129"><summary>NVM Figure 129 · I/O Command Set Specific Identify Controller Data Structure for the NVM Command Set</summary>
<!-- claim:NVMCS13-NVM-FIG-129-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.06">03.06.</span>Figure 129, "I/O Command Set Specific Identify Controller Data Structure for the NVM Command Set": This table continues through printed page106, not just captioned page103. Size limits require ONCS variants; SLMC is zero-based and VER identifies the command-set version.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>zero-based</dt><dd>zero-based: numbering starts at zero, so raw=3 can mean the fourth item or four units; the field definition still decides which.</dd></div><div><dt>ONCS</dt><dd>Optional NVM Commands Supported; includes capability/variant information to combine with NVM Identify limits.</dd></div><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.5.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.4, Figure 129, printed pages 103-106, PDF pages 103-106</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>DMRSL</dt><dd>Dataset Management Range Size Limit; The logical-block processing limit for one range.</dd></div><div><dt>WZDSL</dt><dd>Specific Write Zeroes with Deallocate size limit; do not substitute WZSL.</dd></div><div><dt>DMRL</dt><dd>Dataset Management Ranges Limit, an actual range-count limit.</dd></div><div><dt>DMSL</dt><dd>Dataset Management Size Limit; The logical-block processing limit for the command.</dd></div><div><dt>WUSL</dt><dd>Write Uncorrectable Size Limit; A Write Uncorrectable size limit, interpreted with its variant capability.</dd></div><div><dt>WZSL</dt><dd>Write Zeroes Size Limit; A Write Zeroes size limit, interpreted with its variant capability.</dd></div><div><dt>VSL</dt><dd>Verify Size Limit; A Verify size limit, interpreted with its variant capability.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-130 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-130"><summary>NVM Figure 130 · NVM Command Set Specification Version Descriptor Field Values</summary>
<!-- claim:NVMCS13-NVM-FIG-130-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.07">03.07.</span>Figure 130, "NVM Command Set Specification Version Descriptor Field Values": Revision 1.3 maps to MJR=1, MNR=3, TER=0. Record this command-set version separately from the Base version.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.5.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.4, Figure 130, printed pages 107, PDF pages 107</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-131 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-131"><summary>NVM Figure 131 · Command Dword 11 - CNS Specific Identifiers</summary>
<!-- claim:NVMCS13-NVM-FIG-131-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.08">03.08.</span>Figure 131, "Command Dword 11 - CNS Specific Identifiers": For CNS09h/0Ah, CDW11 low16 is Format Index rather than a namespace ID; CSI separately selects the command set.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Dword (double word): 32 bits, or 4 bytes. A word is 16 bits; for example, a zero-based dword count of 3 represents 4 Dwords, or 16 bytes.</dd></div><div><dt>CDW</dt><dd>CDW (Command Dword): a 32-bit command field. In CDW10, 10 is the field index, not a byte offset.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.5.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.5, Figure 131, printed pages 107, PDF pages 107</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-338 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-338"><summary>Base Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</summary>
<!-- claim:NVMCS13-BASE-FIG-338-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.09">03.09.</span>Figure 338, "Identify – Identify Controller Data Structure, I/O Command Set Independent": NVM uses Base Identify capabilities including ONCS variants, CTRATT.ELBAS/MEM, MDTS, and SANICAP.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>MDTS</dt><dd>Maximum Data Transfer Size; an exponent based on minimum page size, with a defined no-limit meaning for zero.</dd></div><div><dt>ONCS</dt><dd>Optional NVM Commands Supported; includes capability/variant information to combine with NVM Identify limits.</dd></div><div><dt>I/O</dt><dd>Input/Output, the class of data operations performed on a namespace.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.1, Figure 338, printed pages 340-382, PDF pages 366-408</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>MDTS</dt><dd>Maximum Data Transfer Size; an exponent based on minimum page size, with a defined no-limit meaning for zero.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-BASE-FIG-346 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-346"><summary>Base Figure 346 · Identify – I/O Command Set Independent Identify Namespace Data Structure</summary>
<!-- claim:NVMCS13-BASE-FIG-346-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="03.10">03.10.</span>Figure 346, "Identify – I/O Command Set Independent Identify Namespace Data Structure": CNS08h provides command-set-independent namespace attributes and combines with NVM CNS00h/05h. No single structure establishes every capability.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.14.2.8</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.14.2.8, Figure 346, printed pages 391-394, PDF pages 417-420</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>ANAGRPID</dt><dd>ANA Group Identifier, identifying the Asymmetric Namespace Access group for a namespace; zero at create lets the controller choose.</dd></div><div><dt>NMIC</dt><dd>Namespace Multi-path I/O and Namespace Sharing Capabilities, the create field declaring namespace sharing and multipath properties.</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-format-list"><h2 id="heading-nvmcs-format-list"><span class="section-number">04</span> LBAF, ELBAF, and unique-attribute formats</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.01">04.01.</span>The basic entry gives data/metadata sizes and relative performance; the extended entry gives PI format and Storage Tag allocation. Query unique-attribute entries individually instead of assuming common capabilities.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PI</dt><dd>Protection Information: Guard and tag fields used to check data and its associated information.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-FORMAT-LIST -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.02">04.02.</span>LBAF and ELBAF pair at the same Format Index. Total format count is raw NLBAF+1+NULBAF: NLBAF is zero-based and NULBAF is an actual count. A valid index still requires checking LBADS; zero means that supported format is currently unavailable.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>zero-based</dt><dd>zero-based: numbering starts at zero, so raw=3 can mean the fourth item or four units; the field definition still decides which.</dd></div><div><dt>NULBAF</dt><dd>Actual count of Unique Attribute LBA Formats; zero is allowed.</dd></div><div><dt>NLBAF</dt><dd>Zero-based count of LBA formats with common attributes.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.5.1; 4.1.5.3; 5.6</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1; 4.1.5.3; 5.6, printed pages 85-94,96-102,160-162, PDF pages 85-94,96-102,160-162</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>LBAF</td><td>LBADS, MS, RP</td><td>RP is a relative class for a specified workload</td></tr><tr><td>ELBAF</td><td>PIF, QPIF, STS</td><td>QPIF applies only to qualified type</td></tr><tr><td>FLBAS</td><td>FIDXU and FIDXL form the index</td><td>MTELBA is a separate metadata bit</td></tr><tr><td>NULBAF</td><td>Appended after common formats</td><td>09h/0Ah retrieve individual capabilities</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>NULBAF</dt><dd>Actual count of Unique Attribute LBA Formats; zero is allowed.</dd></div><div><dt>QPIF</dt><dd>Qualified Protection Information Format; Selects a qualified PI format.</dd></div><div><dt>PIF</dt><dd>Protection Information Format; Selects a PI format; a qualified format additionally uses QPIF.</dd></div><div><dt>STS</dt><dd>Storage Tag Size, the high-bit count within fixed Storage/Reference Space.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="04.03">04.03.</span>Raw NLBAF=3 and NULBAF=2 give four common formats and two unique-attribute formats: six total, indices 0..5. Figure 192 uses conceptual counts; do not substitute raw NLBAF without reading the fields it.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-124 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-124"><summary>NVM Figure 124 · Namespace Alignment and Granularity Attributes</summary>
<!-- claim:NVMCS13-NVM-FIG-124-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.04">04.04.</span>Figure 124, "Namespace Alignment and Granularity Attributes": OPTPERF is a two-bit selector enabling different small/large deallocate-field sets, not a universal performance-enable bit.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.5.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1, Figure 124, printed pages 94, PDF pages 94</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-125 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-125"><summary>NVM Figure 125 · LBA Format Data Structure, NVM Command Set Specific</summary>
<!-- claim:NVMCS13-NVM-FIG-125-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.05">04.05.</span>Figure 125, "LBA Format Data Structure, NVM Command Set Specific": LBADS is an exponent, MS an actual metadata-byte count, and RP a relative performance class. LBADS=0 means currently unavailable, not one byte or 512 bytes.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.5.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1, Figure 125, printed pages 94, PDF pages 94</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-127 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-127"><summary>NVM Figure 127 · NVM Command Set I/O Command Set Specific Identify Namespace Data Structure</summary>
<!-- claim:NVMCS13-NVM-FIG-127-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.06">04.06.</span>Figure 127, "NVM Command Set I/O Command Set Specific Identify Namespace Data Structure": The extended namespace structure separates PI/mask capabilities, per-format ELBAF, and performance/allocation hints. OPTRPERF gates NPRG/NPRA/NORS.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PI</dt><dd>Protection Information: Guard and tag fields used to check data and its associated information.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.5.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.3, Figure 127, printed pages 97-101, PDF pages 97-101</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>LBSTM</dt><dd>Tag comparison mask; zero bits exclude comparison, with extra support/alignment rules for Storage masking.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-128 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-128"><summary>NVM Figure 128 · Extended LBA Format Data Structure, NVM Command Set Specific</summary>
<!-- claim:NVMCS13-NVM-FIG-128-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.07">04.07.</span>Figure 128, "Extended LBA Format Data Structure, NVM Command Set Specific": QPIF applies when PIF=11b and QPIFS is supported. STS counts bits dividing a fixed-width Storage/Reference Space; it does not enlarge PI.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>QPIF</dt><dd>Qualified Protection Information Format; Selects a qualified PI format.</dd></div><div><dt>PIF</dt><dd>Protection Information Format; Selects a PI format; a qualified format additionally uses QPIF.</dd></div><div><dt>STS</dt><dd>Storage Tag Size, the high-bit count within fixed Storage/Reference Space.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.5.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.3, Figure 128, printed pages 101-102, PDF pages 101-102</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-192 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-192"><summary>NVM Figure 192 · LBA Format List Structure</summary>
<!-- claim:NVMCS13-NVM-FIG-192-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.08">04.08.</span>Figure 192, "LBA Format List Structure": Read the fields raw NLBAF by adding one, then add NULBAF. Unique-attribute formats immediately follow the common-format region.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.6</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.6, Figure 192, printed pages 161, PDF pages 161</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-193 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-193"><summary>NVM Figure 193 · LBA Format List Entries Applicability to Identify Command CNS Value</summary>
<!-- claim:NVMCS13-NVM-FIG-193-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="04.09">04.09.</span>Figure 193, "LBA Format List Entries Applicability to Identify Command CNS Value": Common-capability and per-format queries cover different format sets. 09h/0Ah can query unique-attribute entries defined by NULBAF.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.6</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.6, Figure 193, printed pages 162, PDF pages 162</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-format"><h2 id="heading-nvmcs-format"><span class="section-number">05</span> Format, Host Behavior, and extended LBAs</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.01">05.01.</span>Formatting can change block counts and field applicability; re-identify before constructing buffers. Do not confuse capability lists with the active format.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-FORMAT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.02">05.02.</span>Format NVM selects a supported Format Index, PI type, and metadata transfer method. Extended PI and formats beyond the legacy 16 entries require controller ELBAS and host LBAFEE checks; they cannot simply be used without host enablement.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>LBAFEE</dt><dd>Host LBA Format Extension Enable declaration.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.2; 4.1.3.7</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.2; 4.1.3.7, printed pages 62-63,68-69, PDF pages 62-63,68-69</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>PI / PIL</td><td>PI=0 disables protection; 1/2/3 select its type</td><td>This revision requires PIL=0, placing PI last</td></tr><tr><td>MSET</td><td>One: extended LBA; zero: separate metadata</td><td>Ignored when MS=0</td></tr><tr><td>LBAFEE</td><td>FID 16h byte 2, valid values zero/one</td><td>ELBAS also gates extended formats</td></tr><tr><td>STS</td><td>Format cannot freely change STS to a new nonzero value</td><td>Namespace creation can establish a new configuration</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>LBAFEE</dt><dd>Host LBA Format Extension Enable declaration.</dd></div><div><dt>FID</dt><dd>Feature Identifier: selects the Feature to read or configure.</dd></div><div><dt>PIL</dt><dd>Protection Information Location; selects PI placement within metadata subject to Guard-format restrictions.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="05.03">05.03.</span>For 64b Guard with MS=16, first check ELBAS, LBAFEE=1, the corresponding LBAF/ELBAF, and PI capability. Setting Format PI=1 alone does not select 64b Guard.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Guard</dt><dd>The PI check-value field; the selected format determines its width and calculation.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-091 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-091"><summary>NVM Figure 91 · Format NVM – Command Dword 10 – NVM Command Set Specific Fields</summary>
<!-- claim:NVMCS13-NVM-FIG-091-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.04">05.04.</span>Figure 91, "Format NVM – Command Dword 10 – NVM Command Set Specific Fields": PI selects protection type and MSET metadata transfer; this revision requires PIL=0. LBAF/ELBAF separately determine Guard width.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Dword</dt><dd>Dword (double word): 32 bits, or 4 bytes. A word is 16 bits; for example, a zero-based dword count of 3 represents 4 Dwords, or 16 bytes.</dd></div><div><dt>Guard</dt><dd>The PI check-value field; the selected format determines its width and calculation.</dd></div><div><dt>PIL</dt><dd>Protection Information Location; selects PI placement within metadata subject to Guard-format restrictions.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.2, Figure 91, printed pages 63, PDF pages 63</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-101 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-101"><summary>NVM Figure 101 · Host Behavior Support – Data Structure</summary>
<!-- claim:NVMCS13-NVM-FIG-101-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="05.05">05.05.</span>Figure 101, "Host Behavior Support – Data Structure": LBAFEE at Host Behavior Support byte2 declares host extended-LBA-format support. Only zero/one are valid; also check controller ELBAS.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.7</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.7, Figure 101, printed pages 68, PDF pages 68</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-namespace-create"><h2 id="heading-nvmcs-namespace-create"><span class="section-number">06</span> Namespace creation: format, mask, granularity</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.01">06.01.</span>Query Format Index capabilities before filling host-specified fields; do not use an entire unmodified Identify Namespace structure as the create payload.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-NAMESPACE-CREATE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.02">06.02.</span>The NVM create payload specifies NSZE, NCAP, FLBAS, DPS, LBSTM, and placement handles. Namespace Size/Capacity Granularity are byte-valued hints; a create valid in other respects must not be rejected merely for failing these granularities.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>LBSTM</dt><dd>Tag comparison mask; zero bits exclude comparison, with extra support/alignment rules for Storage masking.</dd></div><div><dt>DPS</dt><dd>End-to-end Data Protection Type Settings, the create field selecting Protection Information type and position.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.6; 4.1.5.8; 5.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6; 4.1.5.8; 5.8, printed pages 108,110-113,165, PDF pages 108,110-113,165</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>NSZE / NCAP</td><td>Values are specified in logical blocks</td><td>Convert before comparing with byte granularities</td></tr><tr><td>LBSTM</td><td>Must satisfy PIC/PIFA masking constraints</td><td>Violations return Invalid Field in Command</td></tr><tr><td>GDM / ND</td><td>GDM=0 uses descriptor zero for all formats</td><td>ND is zero-based</td></tr><tr><td>Completion</td><td>Successful creation includes the requested formatting</td><td>Attachment is a separate management action</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="06.03">06.03.</span>With NSG=NCG=1 MiB and logical block size 4096, NSZE=NCAP=256 makes the allocation fully addressable. Choosing 257 may leave extra unaddressable allocation under the hints, but that alone is not a rejection reason.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NCG</dt><dd>Namespace Capacity Granularity, the controller's preferred NCAP allocation granularity in bytes.</dd></div><div><dt>NSG</dt><dd>Namespace Size Granularity, the controller's preferred NSZE allocation granularity in bytes.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-132 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-132"><summary>NVM Figure 132 · Namespace Granularity List</summary>
<!-- claim:NVMCS13-NVM-FIG-132-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.04">06.04.</span>Figure 132, "Namespace Granularity List": GDM=0 applies descriptor0 to all formats and uses ND=0. GDM=1 maps matching indices to formats. ND is zero-based and LBAFEE affects the supported count.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.5.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.8, Figure 132, printed pages 108, PDF pages 108</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-133 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-133"><summary>NVM Figure 133 · Namespace Granularity Descriptor</summary>
<!-- claim:NVMCS13-NVM-FIG-133-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.05">06.05.</span>Figure 133, "Namespace Granularity Descriptor": NSG/NCG report preferred allocation granularity in bytes. Zero means unreported, not a divisor or a requirement for zero namespace size.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NCG</dt><dd>Namespace Capacity Granularity, the controller's preferred NCAP allocation granularity in bytes.</dd></div><div><dt>NSG</dt><dd>Namespace Size Granularity, the controller's preferred NSZE allocation granularity in bytes.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.5.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.8, Figure 133, printed pages 108, PDF pages 108</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-134 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-134"><summary>NVM Figure 134 · Namespace Management – Host Specified Fields</summary>
<!-- claim:NVMCS13-NVM-FIG-134-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="06.06">06.06.</span>Figure 134, "Namespace Management – Host Specified Fields": Only designated create-payload fields are host-specified. LBSTM/placement-list locations differ from the basic Identify area, so copying an entire Identify structure is incorrect.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.6.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.6.4, Figure 134, printed pages 112-113, PDF pages 112-113</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>ANAGRPID</dt><dd>ANA Group Identifier, identifying the Asymmetric Namespace Access group for a namespace; zero at create lets the controller choose.</dd></div><div><dt>NVMSETID</dt><dd>NVM Set Identifier, selecting the NVM Set from which capacity is allocated when creating a namespace.</dd></div><div><dt>NPHNDLS</dt><dd>Number of Placement Handles, the entry count for the Placement Handle List in the NVM create payload, with a maximum of 128.</dd></div><div><dt>ENDGID</dt><dd>Endurance Group Identifier, selecting the Endurance Group for a created namespace.</dd></div><div><dt>NMIC</dt><dd>Namespace Multi-path I/O and Namespace Sharing Capabilities, the create field declaring namespace sharing and multipath properties.</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-metadata"><h2 id="heading-nvmcs-metadata"><span class="section-number">07</span> Metadata transfer and PI placement</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.01">07.01.</span>Metadata need not consist entirely of PI. Mark data, non-PI metadata, and PI separately before computing host-buffer size and CRC coverage.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CRC</dt><dd>Cyclic Redundancy Check: a check value computed from data bits to detect changes.</dd></div></dl>
<figure><div class="diagram-scroll"><svg viewBox="0 0 760 260" role="img"><title>Where data and metadata travel</title><desc>Data and metadata must correspond to the same logical blocks, whether transferred together or separately.</desc><rect x="20" y="30" width="240" height="65" rx="6" class="v-object"/><text x="140.0" y="68.5" text-anchor="middle" font-size="17">Data 0</text><rect x="260" y="30" width="120" height="65" rx="6" class="v-decision"/><text x="320.0" y="68.5" text-anchor="middle" font-size="17">MD 0</text><rect x="390" y="30" width="230" height="65" rx="6" class="v-object"/><text x="505.0" y="68.5" text-anchor="middle" font-size="17">Data 1</text><rect x="620" y="30" width="120" height="65" rx="6" class="v-decision"/><text x="680.0" y="68.5" text-anchor="middle" font-size="17">MD 1</text><rect x="20" y="155" width="350" height="65" rx="6" class="v-command"/><text x="195.0" y="193.5" text-anchor="middle" font-size="17">DPTR: Data 0, Data 1</text><rect x="390" y="155" width="350" height="65" rx="6" class="v-decision"/><text x="565.0" y="193.5" text-anchor="middle" font-size="17">MPTR: MD 0, MD 1</text></svg></div><figcaption>Data and metadata must correspond to the same logical blocks, whether transferred together or separately.</figcaption></figure>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>DPTR</dt><dd>Command data pointer: destination for Read, source for Write, descriptors for Copy/DSM.</dd></div><div><dt>MPTR</dt><dd>Separate-metadata pointer; namespace format and command fields determine metadata placement.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-METADATA -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.02">07.02.</span>Formatting selects one metadata transfer mechanism per namespace: contiguous extended LBAs or a separate buffer addressed by MPTR. Metadata cannot be split between the mechanisms and must be written atomically with its associated logical block.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>MPTR</dt><dd>Separate-metadata pointer; namespace format and command fields determine metadata placement.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.1.6; 5.2.3; 5.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.6; 5.2.3; 5.3, printed pages 22,129-131, PDF pages 22,129-131</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Extended LBA</td><td>DPTR addresses interleaved data+metadata</td><td>MSET/MTELBA reflect the selection</td></tr><tr><td>Separate buffer</td><td>DPTR addresses data; MPTR addresses metadata</td><td>PRP metadata is physically contiguous; SGL metadata may be scattered</td></tr><tr><td>PI location</td><td>Valid current formats put PI at the metadata end</td><td>CRC covers preceding non-PI metadata</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>DPTR</dt><dd>Command data pointer: destination for Read, source for Write, descriptors for Copy/DSM.</dd></div><div><dt>CRC</dt><dd>Cyclic Redundancy Check: a check value computed from data bits to detect changes.</dd></div><div><dt>PRP</dt><dd>Physical Region Page, a pointer format describing a host-addressable data buffer in memory-page units.</dd></div><div><dt>SGL</dt><dd>Scatter Gather List, a descriptor-and-segment format for one or more data-buffer regions.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="07.03">07.03.</span>For eight blocks, data=4096, MS=16, PRACT=0: the extended buffer is 32896 bytes; separate buffers are 32768 data bytes and 128 metadata bytes.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PRACT</dt><dd>Protection Information Action; PI handling depends on command and MS.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-153 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-153"><summary>NVM Figure 153 · Metadata – Contiguous with LBA Data, Forming Extended LBA</summary>
<!-- claim:NVMCS13-NVM-FIG-153-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.04">07.04.</span>Figure 153, "Metadata – Contiguous with LBA Data, Forming Extended LBA": Extended LBAs place metadata immediately after each block’s data, not all data first followed by all metadata.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.2.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.2.3, Figure 153, printed pages 129, PDF pages 129</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-154 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-154"><summary>NVM Figure 154 · Metadata – Transferred as Separate Buffer</summary>
<!-- claim:NVMCS13-NVM-FIG-154-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="07.05">07.05.</span>Figure 154, "Metadata – Transferred as Separate Buffer": Separate mode uses distinct data/metadata buffers with block correspondence, not an arbitrarily reordered metadata list.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.2.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.2.3, Figure 154, printed pages 130, PDF pages 130</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-support-status"><h2 id="heading-nvmcs-support-status"><span class="section-number">08</span> Capabilities, opcodes, and status</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.01">08.01.</span>Build a command/Feature/log capability matrix starting from controller type. A data pointer may reference user data or merely control descriptors.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-SUPPORT-STATUS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.02">08.02.</span>An NVM I/O controller must support Read and Write; other listed NVM commands depend on their capability conditions. The low two opcode bits identify transfer direction. Interpret status values with SCT rather than looking up SC alone.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>I/O controller</dt><dd>I/O controller, a controller type capable of executing user-data I/O commands.</dd></div><div><dt>SCT</dt><dd>Status Code Type: selects the completion-status category and is interpreted with SC.</dd></div><div><dt>SC</dt><dd>Status Code: identifies the completion result within the selected SCT category.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.2; 3.1; 3.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.2; 3.1; 3.3, printed pages 22-27, PDF pages 22-27</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Read 02h / Write 01h</td><td>Mandatory I/O commands</td><td>Administrative controllers do not process I/O</td></tr><tr><td>Get LBA Status 86h</td><td>Optional Admin command</td><td>Capability belongs to I/O controllers</td></tr><tr><td>SC 80h</td><td>SCT distinguishes LBA Out of Range and other meanings</td><td>Record opcode, NSID, SCT, SC, and DNR</td></tr><tr><td>FID / LID</td><td>05h and 0Ah are mandatory NVM Features</td><td>Feature support differs from Persistent Event Log recording</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div><div><dt>DNR</dt><dd>Do Not Retry, a CQE-status bit indicating that retrying the same command is not expected to succeed.</dd></div><div><dt>LID</dt><dd>Log Page Identifier: selects the type of log page to read.</dd></div><div><dt>SCT</dt><dd>Status Code Type: selects the completion-status category and is interpreted with SC.</dd></div><div><dt>SC</dt><dd>Status Code: identifies the completion result within the selected SCT category.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="08.03">08.03.</span>Copy opcode 19h has low bits 01b because the host supplies source descriptors; it does not require the host to retransmit all user data being copied.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-013 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-013"><summary>NVM Figure 13 · NVM Command Set Admin Command Support</summary>
<!-- claim:NVMCS13-NVM-FIG-013-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.04">08.04.</span>Figure 13, "NVM Command Set Admin Command Support": Get LBA Status 86h is optional for an I/O controller and prohibited for an Administrative controller.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Administrative controller</dt><dd>Administrative controller, a management-oriented controller type that does not execute user-data I/O commands.</dd></div><div><dt>I/O controller</dt><dd>I/O controller, a controller type capable of executing user-data I/O commands.</dd></div><div><dt>Admin</dt><dd>Administrative, the control path used to create, configure, query, or manage controllers and queues.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.2.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.2.1, Figure 13, printed pages 23, PDF pages 23</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>Administrative controller</dt><dd>Administrative controller, a management-oriented controller type that does not execute user-data I/O commands.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-014 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-014"><summary>NVM Figure 14 · I/O Controller – NVM Command Set I/O Command Support</summary>
<!-- claim:NVMCS13-NVM-FIG-014-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.05">08.05.</span>Figure 14, "I/O Controller – NVM Command Set I/O Command Support": Read/Write are mandatory. Compare, Verify, Copy, Write Zeroes, Write Uncorrectable, and other optional commands require their own capability checks; appearing in the table does not establish support.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.2.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.2.1, Figure 14, printed pages 23, PDF pages 23</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-015 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-015"><summary>NVM Figure 15 · NVM Command Set Log Page Support</summary>
<!-- claim:NVMCS13-NVM-FIG-015-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.06">08.06.</span>Figure 15, "NVM Command Set Log Page Support": 0Eh is optional for I/O controllers; 28h is optional for I/O and Administrative controllers. Check the log definition separately for scope.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.2.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.2.2, Figure 15, printed pages 23, PDF pages 23</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-016 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-016"><summary>NVM Figure 16 · NVM Command Set Feature Support</summary>
<!-- claim:NVMCS13-NVM-FIG-016-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.07">08.07.</span>Figure 16, "NVM Command Set Feature Support": Match each Feature support row to controller type. Performance Characteristics on an Administrative controller cannot have namespace scope.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.2.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.2.3, Figure 16, printed pages 23-24, PDF pages 23-24</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-017 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-017"><summary>NVM Figure 17 · NVM Command Set Feature Logged in Persistent Event Log Page Requirement</summary>
<!-- claim:NVMCS13-NVM-FIG-017-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.08">08.08.</span>Figure 17, "NVM Command Set Feature Logged in Persistent Event Log Page Requirement": This table governs recording Feature updates in the Persistent Event Log. NR for 03h does not prohibit the Feature and is not another Feature support classification.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NR</dt><dd>Zero-based range-count field; actual descriptor count is NR+1.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.2.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.2.3, Figure 17, printed pages 24, PDF pages 24</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-018 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-018"><summary>NVM Figure 18 · Status Code – Generic Command Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-018-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.09">08.09.</span>Figure 18, "Status Code – Generic Command Status Values": Generic status 80h is LBA Out of Range and 81h Capacity Exceeded. Retain SCT and check NSZE separately from NCAP/NUSE.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.1.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.1.2, Figure 18, printed pages 25, PDF pages 25</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-019 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-019"><summary>NVM Figure 19 · Status Code – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-019-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.10">08.10.</span>Figure 19, "Status Code – Command Specific Status Values": Use opcode and SCT=1 to select command-specific status. Copy format/overlap errors and Read PI errors have different applicability sets.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.1.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.1.2, Figure 19, printed pages 25, PDF pages 25</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-020 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-020"><summary>NVM Figure 20 · Status Code – Media and Data Integrity Error Values</summary>
<!-- claim:NVMCS13-NVM-FIG-020-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.11">08.11.</span>Figure 20, "Status Code – Media and Data Integrity Error Values": Media/Data Integrity status includes Compare miscomparison and deallocated/unwritten access errors. Investigate DULBE for the latter rather than immediately declaring bad media.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DULBE</dt><dd>Deallocated or Unwritten Logical Block Error Enable, requiring namespace DAE support.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.1.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.1.2, Figure 20, printed pages 26, PDF pages 26</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-022 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-022"><summary>NVM Figure 22 · Opcodes for NVM Commands</summary>
<!-- claim:NVMCS13-NVM-FIG-022-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.12">08.12.</span>Figure 22, "Opcodes for NVM Commands": The low two opcode bits encode transfer direction; Copy transfers descriptors host-to-controller. Broadcast NSID is unavailable except for specifically noted commands.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3, Figure 22, printed pages 27, PDF pages 27</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-097 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-097"><summary>Base Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</summary>
<!-- claim:NVMCS13-BASE-FIG-097-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.13">08.13.</span>Figure 97, "Common Completion Queue Entry Layout – Admin and All I/O Command Sets": CQE command-specific results have separate locations from common queue/status information. Copy DW0 and Write Zeroes DW0 have different meanings.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 97, printed pages 144, PDF pages 170</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>SQID</dt><dd>Submission Queue Identifier, the numeric identifier of the SQ containing a command.</dd></div><div><dt>CID</dt><dd>Command Identifier, used with the SQ identifier to identify an outstanding command.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-BASE-FIG-098 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-098"><summary>Base Figure 98 · Completion Queue Entry: DW 2</summary>
<!-- claim:NVMCS13-BASE-FIG-098-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.14">08.14.</span>Figure 98, "Completion Queue Entry: DW 2": DW2 SQHD/SQID report submission-queue information, not the byte count transferred by this command.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SQID</dt><dd>Submission Queue Identifier, the numeric identifier of the SQ containing a command.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 98, printed pages 144, PDF pages 170</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-099 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-099"><summary>Base Figure 99 · Completion Queue Entry: DW 3</summary>
<!-- claim:NVMCS13-BASE-FIG-099-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.15">08.15.</span>Figure 99, "Completion Queue Entry: DW 3": DW3 associates completion through CID and reports its result through Status; command-specific DW0 does not replace Status.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CID</dt><dd>Command Identifier, used with the SQ identifier to identify an outstanding command.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.2.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.1, Figure 99, printed pages 145, PDF pages 171</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-101 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-101"><summary>Base Figure 101 · Completion Queue Entry: Status Field</summary>
<!-- claim:NVMCS13-BASE-FIG-101-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="08.16">08.16.</span>Figure 101, "Completion Queue Entry: Status Field": Interpret SCT/SC together, DNR for retry guidance, and phase for a new completion; these fields answer different questions.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DNR</dt><dd>Do Not Retry, a CQE-status bit indicating that retrying the same command is not expected to succeed.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.2.3</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.2.3, Figure 101, printed pages 145-146, PDF pages 171-172</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>P</dt><dd>Phase Tag, the toggling bit used by the host to decide whether a CQ slot contains a new completion.</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-read-write"><h2 id="heading-nvmcs-read-write"><span class="section-number">09</span> Read/Write data and completion</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.01">09.01.</span>Check range, buffer, PI, and completion separately to distinguish addressing errors, format mismatches, and media failures.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-READ-WRITE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.02">09.02.</span>Read/Write specify a contiguous range with SLBA and zero-based NLB. DPTR is a destination buffer for Read and a source buffer for Write. FUA=1 requires nonvolatile-media handling without implying ordering of other commands.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SLBA</dt><dd>Starting LBA; Starts the command range.</dd></div><div><dt>FUA</dt><dd>Force Unit Access; requires nonvolatile-media semantics without automatically ordering other commands.</dd></div><div><dt>NLB</dt><dd>Number of Logical Blocks; this field in the report’s commands/status descriptors is zero-based. DSM LLB is separately one-based.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.4; 3.3.6</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4; 3.3.6, printed pages 48-51,53-56, PDF pages 48-51,53-56</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>CDW10 / CDW11</td><td>Low/high 32 bits of SLBA</td><td>NLB=0 still requests one block</td></tr><tr><td>CDW12</td><td>LR, FUA, PRINFO, STC, CETYPE, NLB</td><td>The DTYPE area is reserved for Read</td></tr><tr><td>CDW13</td><td>CETYPE selects DSM or CEV interpretation</td><td>Write also carries DTYPE/DSPEC</td></tr><tr><td>MPTR</td><td>Used for separate metadata</td><td>Do not split metadata between both mechanisms</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>CETYPE</dt><dd>Command Extension Type; Selects the interpretation of the command extension value CEV.</dd></div><div><dt>PRINFO</dt><dd>Protection Information; The command field combining PRACT and PRCHK.</dd></div><div><dt>DSPEC</dt><dd>Directive Specific; Its contents depend on the Directive type.</dd></div><div><dt>DTYPE</dt><dd>Directive Type; Selects the Directive type for the command.</dd></div><div><dt>SLBA</dt><dd>Starting LBA; Starts the command range.</dd></div><div><dt>CDW</dt><dd>CDW (Command Dword): a 32-bit command field. In CDW10, 10 is the field index, not a byte offset.</dd></div><div><dt>CEV</dt><dd>Command Extension Value; Its contents are interpreted according to CETYPE.</dd></div><div><dt>DSM</dt><dd>Dataset Management: host hints about use and allocation of data ranges.</dd></div><div><dt>FUA</dt><dd>Force Unit Access; requires nonvolatile-media semantics without automatically ordering other commands.</dd></div><div><dt>NLB</dt><dd>Number of Logical Blocks; this field in the report’s commands/status descriptors is zero-based. DSM LLB is separately one-based.</dd></div><div><dt>STC</dt><dd>Storage Tag Check, separate from three-bit PRCHK and ignored when STS=0.</dd></div><div><dt>LR</dt><dd>Limited Retry; selects retry behavior governed by Error Recovery policy.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="09.03">09.03.</span>With SLBA=100, NLB=7, LBADS=12, and no metadata, Read covers 100..107 and 32768 bytes. An FUA Read commits the corresponding data before retrieving it from media; the host still orders dependent Writes.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-050 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-050"><summary>NVM Figure 50 · Read – Metadata Pointer</summary>
<!-- claim:NVMCS13-NVM-FIG-050-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.04">09.04.</span>Figure 50, "Read – Metadata Pointer": MPTR supplies the metadata location for a separate-metadata format. Check PSDT/metadata format first; it is not the user-data buffer.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PSDT</dt><dd>PRP or SGL for Data Transfer, the CDW0 field selecting PRP or SGL interpretation for DPTR.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 50, printed pages 49, PDF pages 49</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-051 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-051"><summary>NVM Figure 51 · Read – Data Pointer</summary>
<!-- claim:NVMCS13-NVM-FIG-051-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.05">09.05.</span>Figure 51, "Read – Data Pointer": DPTR addresses the host destination: Read returns data and Get LBA Status returns a descriptor list. Their response data formats differ.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 51, printed pages 49, PDF pages 49</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-052 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-052"><summary>NVM Figure 52 · Read – Command Dword 2 and Dword 3</summary>
<!-- claim:NVMCS13-NVM-FIG-052-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.06">09.06.</span>Figure 52, "Read – Command Dword 2 and Dword 3": Combine CDW2/3 upper tags with CDW14 lower tags, then split expected storage/reference fields by PI format and STS. Unused bits are ignored as specified by the format.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 52, printed pages 49, PDF pages 49</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>EILBRT</dt><dd>Initial Logical Block Reference Tag/expected initial value; Type 1/2 increment per block and wrap at the field width.</dd></div><div><dt>ELBST</dt><dd>Logical Block Storage Tag/Expected Logical Block Storage Tag; width is determined by STS.</dd></div><div><dt>ELBTL / ELBTU</dt><dd>Upper/lower Logical Block Tags or expected tags; combine according to Guard format, STS, and Dword position.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-053 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-053"><summary>NVM Figure 53 · Read – Command Dword 10 and Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-053-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.07">09.07.</span>Figure 53, "Read – Command Dword 10 and Command Dword 11": SLBA is 64 bits: low 32 in CDW10, high 32 in CDW11. Check range-specific modes before using it as an address.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 53, printed pages 49, PDF pages 49</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-054 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-054"><summary>NVM Figure 54 · Read – Command Dword 12</summary>
<!-- claim:NVMCS13-NVM-FIG-054-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.08">09.08.</span>Figure 54, "Read – Command Dword 12": CDW12 combines behavior bits with zero-based NLB. Compare/Verify require PRACT=0, while Read/Write select PRACT by metadata format. FUA does not order other commands.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PRACT</dt><dd>Protection Information Action; PI handling depends on command and MS.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 54, printed pages 49, PDF pages 49</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CETYPE</dt><dd>Command Extension Type; Selects the interpretation of the command extension value CEV.</dd></div><div><dt>PRINFO</dt><dd>Protection Information; The command field combining PRACT and PRCHK.</dd></div><div><dt>STC</dt><dd>Storage Tag Check, separate from three-bit PRCHK and ignored when STS=0.</dd></div><div><dt>LR</dt><dd>Limited Retry; selects retry behavior governed by Error Recovery policy.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-055 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-055"><summary>NVM Figure 55 · Read – Command Dword 13 if CETYPE is cleared to 0h</summary>
<!-- claim:NVMCS13-NVM-FIG-055-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.09">09.09.</span>Figure 55, "Read – Command Dword 13 if CETYPE is cleared to 0h": Read uses CDW13 low8 DSM hints only when CETYPE=0. One-time/speculative reads are access-frequency hints, not guaranteed cache-policy changes.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DSM</dt><dd>Dataset Management: host hints about use and allocation of data ranges.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 55, printed pages 50, PDF pages 50</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-056 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-056"><summary>NVM Figure 56 · Read - Command Dword 13 if CETYPE is non-zero</summary>
<!-- claim:NVMCS13-NVM-FIG-056-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.10">09.10.</span>Figure 56, "Read - Command Dword 13 if CETYPE is non-zero": With nonzero CETYPE, CDW13 low16 contains CEV. CETYPE=0 has a different or reserved layout; do not simultaneously encode DSM hints.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CEV</dt><dd>Command Extension Value; Its contents are interpreted according to CETYPE.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 56, printed pages 50, PDF pages 50</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-057 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-057"><summary>NVM Figure 57 · Read – Command Dword 14</summary>
<!-- claim:NVMCS13-NVM-FIG-057-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.11">09.11.</span>Figure 57, "Read – Command Dword 14": CDW14 contains the low 32 bits of expected-tag space. It is not necessarily all Reference Tag: STS may consume some high bits.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 57, printed pages 50, PDF pages 50</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>ELBTL / ELBTU</dt><dd>Upper/lower Logical Block Tags or expected tags; combine according to Guard format, STS, and Dword position.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-058 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-058"><summary>NVM Figure 58 · Read – Command Dword 15</summary>
<!-- claim:NVMCS13-NVM-FIG-058-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.12">09.12.</span>Figure 58, "Read – Command Dword 15": CDW15 high16 is the Application Tag mask and low16 the expected tag. A zero mask bit excludes comparison rather than requiring a zero tag bit.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 58, printed pages 51, PDF pages 51</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>ELBATM</dt><dd>Tag comparison mask; zero bits exclude comparison, with extra support/alignment rules for Storage masking.</dd></div><div><dt>ELBAT</dt><dd>Logical Block Application Tag/expected tag; 16 bits, with checking governed by masks and disable sentinels.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-059 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-059"><summary>NVM Figure 59 · Read – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-059-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.13">09.13.</span>Figure 59, "Read – Command Specific Status Values": Compare SC together with SCT and this command’s applicable entries. Invalid Protection Information concerns settings/initial values incompatible with the format, distinct from a Guard Check Error. Apply only entries listed for the command.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4, Figure 59, printed pages 51, PDF pages 51</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-067 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-067"><summary>NVM Figure 67 · Write – Metadata Pointer</summary>
<!-- claim:NVMCS13-NVM-FIG-067-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.14">09.14.</span>Figure 67, "Write – Metadata Pointer": MPTR supplies the metadata location for a separate-metadata format. Check PSDT/metadata format first; it is not the user-data buffer.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PSDT</dt><dd>PRP or SGL for Data Transfer, the CDW0 field selecting PRP or SGL interpretation for DPTR.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.6</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 67, printed pages 53, PDF pages 53</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-068 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-068"><summary>NVM Figure 68 · Write – Data Pointer</summary>
<!-- claim:NVMCS13-NVM-FIG-068-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.15">09.15.</span>Figure 68, "Write – Data Pointer": Here DPTR addresses host input: expected Compare data or new Write data. The common command format determines PRP/SGL interpretation.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PRP</dt><dd>Physical Region Page, a pointer format describing a host-addressable data buffer in memory-page units.</dd></div><div><dt>SGL</dt><dd>Scatter Gather List, a descriptor-and-segment format for one or more data-buffer regions.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.6</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 68, printed pages 54, PDF pages 54</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-069 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-069"><summary>NVM Figure 69 · Write – Command Dword 2 and Dword 3</summary>
<!-- claim:NVMCS13-NVM-FIG-069-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.16">09.16.</span>Figure 69, "Write – Command Dword 2 and Dword 3": Upper/lower tag fields encode write-side Storage and initial Reference Tags. For Copy these command fields belong to the destination; source expectations are in descriptors.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.6</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 69, printed pages 54, PDF pages 54</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>ILBRT</dt><dd>Initial Logical Block Reference Tag/expected initial value; Type 1/2 increment per block and wrap at the field width.</dd></div><div><dt>LBST</dt><dd>Logical Block Storage Tag/Expected Logical Block Storage Tag; width is determined by STS.</dd></div><div><dt>LBTL / LBTU</dt><dd>Upper/lower Logical Block Tags or expected tags; combine according to Guard format, STS, and Dword position.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-070 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-070"><summary>NVM Figure 70 · Write – Command Dword 10 and Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-070-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.17">09.17.</span>Figure 70, "Write – Command Dword 10 and Command Dword 11": SLBA is 64 bits: low 32 in CDW10, high 32 in CDW11. Check range-specific modes before using it as an address.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.6</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 70, printed pages 54, PDF pages 54</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-071 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-071"><summary>NVM Figure 71 · Write – Command Dword 12</summary>
<!-- claim:NVMCS13-NVM-FIG-071-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.18">09.18.</span>Figure 71, "Write – Command Dword 12": CDW12 combines behavior bits with zero-based NLB. Compare/Verify require PRACT=0, while Read/Write select PRACT by metadata format. FUA does not order other commands.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.6</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 71, printed pages 54, PDF pages 54</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-072 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-072"><summary>NVM Figure 72 · Write – Command Dword 13 if CETYPE is cleared to 0h</summary>
<!-- claim:NVMCS13-NVM-FIG-072-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.19">09.19.</span>Figure 72, "Write – Command Dword 13 if CETYPE is cleared to 0h": The CETYPE=0 Write layout contains high16 DSPEC and low8 DSM. Do not mix it with the nonzero-CETYPE CEV layout.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DSPEC</dt><dd>Directive Specific; Its contents depend on the Directive type.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.6</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 72, printed pages 54-55, PDF pages 54-55</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-073 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-073"><summary>NVM Figure 73 · Write - Command Dword 13 if CETYPE is non-zero</summary>
<!-- claim:NVMCS13-NVM-FIG-073-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.20">09.20.</span>Figure 73, "Write - Command Dword 13 if CETYPE is non-zero": CDW13 high16 carries Directive Specific and low16 carries CEV according to CETYPE. Directive and command extension are separate fields.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.6</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 73, printed pages 55, PDF pages 55</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-074 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-074"><summary>NVM Figure 74 · Write – Command Dword 14</summary>
<!-- claim:NVMCS13-NVM-FIG-074-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.21">09.21.</span>Figure 74, "Write – Command Dword 14": CDW14 supplies the low 32 bits of write tags. Split the space according to STS rather than discarding Storage Tag high bits.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.6</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 74, printed pages 55, PDF pages 55</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>ILBRT</dt><dd>Initial Logical Block Reference Tag/expected initial value; Type 1/2 increment per block and wrap at the field width.</dd></div><div><dt>LBST</dt><dd>Logical Block Storage Tag/Expected Logical Block Storage Tag; width is determined by STS.</dd></div><div><dt>LBTL</dt><dd>Upper/lower Logical Block Tags or expected tags; combine according to Guard format, STS, and Dword position.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-075 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-075"><summary>NVM Figure 75 · Write – Command Dword 15</summary>
<!-- claim:NVMCS13-NVM-FIG-075-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.22">09.22.</span>Figure 75, "Write – Command Dword 15": Application Tag mask/tag occupy CDW15 high16/low16. Copy uses these for the destination write, with separate expected fields for sources.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.6</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 75, printed pages 55, PDF pages 55</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>LBATM</dt><dd>Tag comparison mask; zero bits exclude comparison, with extra support/alignment rules for Storage masking.</dd></div><div><dt>LBAT</dt><dd>Logical Block Application Tag/expected tag; 16 bits, with checking governed by masks and disable sentinels.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-076 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-076"><summary>NVM Figure 76 · Write – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-076-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.23">09.23.</span>Figure 76, "Write – Command Specific Status Values": Compare SC together with SCT and this command’s applicable entries. Invalid Protection Information concerns settings/initial values incompatible with the format, distinct from a Guard Check Error. Apply only entries listed for the command.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.6</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.6, Figure 76, printed pages 56, PDF pages 56</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-093 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-093"><summary>Base Figure 93 · Common Command Format</summary>
<!-- claim:NVMCS13-BASE-FIG-093-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.24">09.24.</span>Figure 93, "Common Command Format": The common SQE separates namespace, data pointers, and command-specific Dwords; NVM sections supply the corresponding command fields.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SQE</dt><dd>Submission Queue Entry, one command structure in an SQ.</dd></div></dl><details class="source-note"><summary>Sources: Base 2.4 §4.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.1.1, Figure 93, printed pages 140-142, PDF pages 166-168</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-110 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-110"><summary>Base Figure 110 · PRP Entry Layout</summary>
<!-- claim:NVMCS13-BASE-FIG-110-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.25">09.25.</span>Figure 110, "PRP Entry Layout": PRP layout contains a page base and first-entry offset. NVM payload can be data or a descriptor list; pointer type does not determine content.</p><details class="source-note"><summary>Sources: Base 2.4 §4.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 110, printed pages 158, PDF pages 184</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-111 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-111"><summary>Base Figure 111 · PRP Entry – Page Base Address and Offset</summary>
<!-- claim:NVMCS13-BASE-FIG-111-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.26">09.26.</span>Figure 111, "PRP Entry – Page Base Address and Offset": Page size determines the base/offset split. Calculate the first page’s remaining space before mapping subsequent PRP pages.</p><details class="source-note"><summary>Sources: Base 2.4 §4.3.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.1, Figure 111, printed pages 158, PDF pages 184</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-116 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-116"><summary>Base Figure 116 · Generic SGL Descriptor Format</summary>
<!-- claim:NVMCS13-BASE-FIG-116-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="09.27">09.27.</span>Figure 116, "Generic SGL Descriptor Format": A local SGL descriptor describes a buffer with address, length, and type.</p><details class="source-note"><summary>Sources: Base 2.4 §4.3.2</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §4.3.2, Figure 116, printed pages 161, PDF pages 187</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-order-fused"><h2 id="heading-nvmcs-order-fused"><span class="section-number">10</span> Ordering and Compare-and-Write</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="10.01">10.01.</span>First establish the ordering requirement, then decide whether conditional updating is needed. A fused operation protects comparison and update of the same LBA range, with atomic-size limits checked separately.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-ORDER-FUSED -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="10.02">10.02.</span>Ordinary commands do not gain LBA dependency ordering merely by sharing an SQ; the host enforces required order. Fused Compare-and-Write compares first and writes only on success; a failed Compare aborts Write with the failed-fused-command status.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SQ</dt><dd>Submission Queue, the queue into which the host places commands.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.1.2-2.1.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.2-2.1.3, printed pages 14-15, PDF pages 14-15</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Ordinary I/O</td><td>Read/Write completion order for one LBA is not guaranteed</td><td>Use host completion dependencies</td></tr><tr><td>Fused pair</td><td>Compare and Write use the same range</td><td>A mismatch should be rejected</td></tr><tr><td>ACWU / NACWU</td><td>Bounds the fused atomic update</td><td>Atomic boundaries also apply</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>NACWU</dt><dd>Namespace Atomic Compare and Write Unit; The namespace fused compare-and-write size limit.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="10.03">10.03.</span>For “replace A with B only if A is still present,” an independent Compare followed by Write permits an intervening write. A fused pair within its size and boundary limits provides the conditional atomic update.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-003 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-003"><summary>NVM Figure 3 · Supported Fused Operations</summary>
<!-- claim:NVMCS13-NVM-FIG-003-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="10.04">10.04.</span>Figure 3, "Supported Fused Operations": Compare must succeed before Write updates the same range. Two CQEs report comparison and write outcomes separately; fused atomicity limits still apply.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.1.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.3, Figure 3, printed pages 14, PDF pages 14</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-atomic"><h2 id="heading-nvmcs-atomic"><span class="section-number">11</span> Normal, power-fail, and multiple atomicity</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.01">11.01.</span>Read size, starting alignment, NSABP, and MAM together. Atomicity and persistence on nonvolatile media are separate checks; FUA/Flush do not establish ordering for other commands.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NSABP</dt><dd>Namespace Atomic Boundary Parameters: indicates applicability of namespace atomic-write parameters.</dd></div><div><dt>MAM</dt><dd>Multiple Atomicity Mode; a crossing command is divided into independently atomic subranges.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-ATOMIC -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.02">11.02.</span>AWUN/NAWUN and AWUPF/NAWUPF describe normal and failure-condition atomicity. Single Atomicity Mode provides no whole-command guarantee across a boundary; Multiple Atomicity Mode divides the range at boundaries into separately atomic subranges, without promising one combined outcome.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NAWUPF</dt><dd>Namespace Atomic Write Unit Power Fail; Namespace failure-condition atomic-write size, subject to applicability and zero-value rules.</dd></div><div><dt>NAWUN</dt><dd>Namespace Atomic Write Unit Normal; Namespace normal atomic-write size, subject to applicability and zero-value rules.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.1.4; 4.1.3.4; 5.9</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4; 4.1.3.4; 5.9, printed pages 15-21,66-67,165, PDF pages 15-21,66-67,165</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>AWUN / AWUPF</td><td>Sizes use zero-based encoding</td><td>AWUPF does not exceed AWUN</td></tr><tr><td>NABO / NABSN / NABSPF</td><td>Boundaries occur at offset + k × size</td><td>Read each field and its unreported cases</td></tr><tr><td>MAM</td><td>Each atomic subrange has its own guarantee</td><td>Fused operations still use Single mode</td></tr><tr><td>FID 0Ah.DN</td><td>DN=1 releases normal-atomicity requirements</td><td>Power-fail guarantees remain</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>NABSPF</dt><dd>Namespace Atomic Boundary Size Power Fail; The failure-condition atomic boundary size.</dd></div><div><dt>NABSN</dt><dd>Namespace Atomic Boundary Size Normal; The normal-operation atomic boundary size.</dd></div><div><dt>NABO</dt><dd>Namespace Atomic Boundary Offset; determines the first boundary location.</dd></div><div><dt>MAM</dt><dd>Multiple Atomicity Mode; a crossing command is divided into independently atomic subranges.</dd></div><div><dt>DN</dt><dd>Disable Normal in Write Atomicity Normal; does not remove power-fail atomicity.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="11.03">11.03.</span>For interpret the fields boundary size 8 blocks and offset zero, a 12-block write starting at LBA 4 splits into [4..7] and [8..15]. Under MAM each part is atomic, not one transaction. Raw AWUN=7h represents eight blocks.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-004 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-004"><summary>NVM Figure 4 · Atomicity Parameters for Single Atomicity Mode</summary>
<!-- claim:NVMCS13-NVM-FIG-004-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.04">11.04.</span>Figure 4, "Atomicity Parameters for Single Atomicity Mode": Use NSABP to select controller or namespace parameters, then interpret the fields zero-based sizes and namespace zero-value inheritance. Raw zero does not universally mean one block.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NSABP</dt><dd>Namespace Atomic Boundary Parameters: indicates applicability of namespace atomic-write parameters.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 4, printed pages 15-16, PDF pages 15-16</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NABSPF</dt><dd>Namespace Atomic Boundary Size Power Fail; The failure-condition atomic boundary size.</dd></div><div><dt>NAWUPF</dt><dd>Namespace Atomic Write Unit Power Fail; Namespace failure-condition atomic-write size, subject to applicability and zero-value rules.</dd></div><div><dt>NABSN</dt><dd>Namespace Atomic Boundary Size Normal; The normal-operation atomic boundary size.</dd></div><div><dt>NACWU</dt><dd>Namespace Atomic Compare and Write Unit; The namespace fused compare-and-write size limit.</dd></div><div><dt>NAWUN</dt><dd>Namespace Atomic Write Unit Normal; Namespace normal atomic-write size, subject to applicability and zero-value rules.</dd></div><div><dt>NABO</dt><dd>Namespace Atomic Boundary Offset; determines the first boundary location.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-005 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-005"><summary>NVM Figure 5 · AWUN/NAWUN Example Results</summary>
<!-- claim:NVMCS13-NVM-FIG-005-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.05">11.05.</span>Figure 5, "AWUN/NAWUN Example Results": This table concerns observable overlapping-write results during normal operation. Compare write size with interpret the fields AWUN and find the read within atomic units.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 5, printed pages 17, PDF pages 17</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-006 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-006"><summary>NVM Figure 6 · AWUPF/NAWUPF Example Initial State of NVM</summary>
<!-- claim:NVMCS13-NVM-FIG-006-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.06">11.06.</span>Figure 6, "AWUPF/NAWUPF Example Initial State of NVM": Record pre-failure media contents and the new write range. This initial state supplies the assumptions for the following failure-result table.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 6, printed pages 18, PDF pages 18</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-007 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-007"><summary>NVM Figure 7 · AWUPF/NAWUPF Example Final State of NVM</summary>
<!-- claim:NVMCS13-NVM-FIG-007-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.07">11.07.</span>Figure 7, "AWUPF/NAWUPF Example Final State of NVM": Separate old-data preservation within the power-fail atomic unit from possible torn writes above it. An unfinished write cannot be assumed to contain all-new data.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 7, printed pages 18, PDF pages 18</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-008 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-008"><summary>NVM Figure 8 · Atomic Boundaries Example</summary>
<!-- claim:NVMCS13-NVM-FIG-008-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.08">11.08.</span>Figure 8, "Atomic Boundaries Example": Place boundaries at offset+k×boundary size on the LBA line. A write shorter than the atomic size can still cross a boundary because of its starting position.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 8, printed pages 19, PDF pages 19</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-009 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-009"><summary>NVM Figure 9 · Atomicity Parameter Differences for Multiple Atomicity Mode</summary>
<!-- claim:NVMCS13-NVM-FIG-009-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.09">11.09.</span>Figure 9, "Atomicity Parameter Differences for Multiple Atomicity Mode": Multiple mode aligns the applicable normal/power-fail sizes with both boundary sizes. Fused Compare-and-Write still follows Single mode.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 9, printed pages 20, PDF pages 20</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-010 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-010"><summary>NVM Figure 10 · Multiple Atomicity Example</summary>
<!-- claim:NVMCS13-NVM-FIG-010-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="11.10">11.10.</span>Figure 10, "Multiple Atomicity Example": A/B/C require separate commands for the illustrated Single-mode guarantees. Multiple-mode D can cover them together, but guarantees remain per subrange, not one D-wide transaction.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4, Figure 10, printed pages 21, PDF pages 21</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-compare-verify"><h2 id="heading-nvmcs-compare-verify"><span class="section-number">12</span> Compare and Verify answer different questions</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.01">12.01.</span>Expected-content comparison, integrity verification, and ordinary Read provide different evidence. Compare excludes PI from metadata comparison and checks PI separately as requested.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-COMPARE-VERIFY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.02">12.02.</span>Compare compares media data with a host-supplied buffer. Verify checks stored-data integrity without returning data or metadata to the host. Both require PRACT=0; Verify and Read need not report an identical error code for a detected failure.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.1; 3.3.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1; 3.3.5, printed pages 27-30,51-53, PDF pages 27-30,51-53</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Compare</td><td>A miscompare returns Compare Failure</td><td>PI can be checked on both host and media paths</td></tr><tr><td>Verify</td><td>No data-buffer transfer</td><td>Verified data still counts toward Data Units Read</td></tr><tr><td>VSL / NVMVFYS</td><td>The variant selects recommended size or a hard limit</td><td>Nonzero VSL uses 2^n × minimum page size</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="12.03">12.03.</span>To determine whether stored contents equal zero, Compare can use a zero-filled expected buffer. Successful Verify establishes this integrity check, not that the contents equal zero.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-023 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-023"><summary>NVM Figure 23 · Compare – Metadata Pointer</summary>
<!-- claim:NVMCS13-NVM-FIG-023-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.04">12.04.</span>Figure 23, "Compare – Metadata Pointer": MPTR supplies the metadata location for a separate-metadata format. Check PSDT/metadata format first; it is not the user-data buffer.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 23, printed pages 28, PDF pages 28</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-024 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-024"><summary>NVM Figure 24 · Compare – Data Pointer</summary>
<!-- claim:NVMCS13-NVM-FIG-024-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.05">12.05.</span>Figure 24, "Compare – Data Pointer": Here DPTR addresses host input: expected Compare data or new Write data. The common command format determines PRP/SGL interpretation.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 24, printed pages 28, PDF pages 28</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-025 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-025"><summary>NVM Figure 25 · Compare – Command Dword 2 and Dword 3</summary>
<!-- claim:NVMCS13-NVM-FIG-025-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.06">12.06.</span>Figure 25, "Compare – Command Dword 2 and Dword 3": Combine CDW2/3 upper tags with CDW14 lower tags, then split expected storage/reference fields by PI format and STS. Unused bits are ignored as specified by the format.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 25, printed pages 28, PDF pages 28</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>EILBRT</dt><dd>Initial Logical Block Reference Tag/expected initial value; Type 1/2 increment per block and wrap at the field width.</dd></div><div><dt>ELBST</dt><dd>Logical Block Storage Tag/Expected Logical Block Storage Tag; width is determined by STS.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-026 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-026"><summary>NVM Figure 26 · Compare – Command Dword 10 and Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-026-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.07">12.07.</span>Figure 26, "Compare – Command Dword 10 and Command Dword 11": SLBA is 64 bits: low 32 in CDW10, high 32 in CDW11. Check range-specific modes before using it as an address.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 26, printed pages 28, PDF pages 28</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-027 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-027"><summary>NVM Figure 27 · Compare – Command Dword 12</summary>
<!-- claim:NVMCS13-NVM-FIG-027-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.08">12.08.</span>Figure 27, "Compare – Command Dword 12": CDW12 combines behavior bits with zero-based NLB. Compare/Verify require PRACT=0, while Read/Write select PRACT by metadata format. FUA does not order other commands.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 27, printed pages 28-29, PDF pages 28-29</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-028 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-028"><summary>NVM Figure 28 · Compare - Command Dword 13 if CETYPE is non-zero</summary>
<!-- claim:NVMCS13-NVM-FIG-028-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.09">12.09.</span>Figure 28, "Compare - Command Dword 13 if CETYPE is non-zero": With nonzero CETYPE, CDW13 low16 contains CEV. CETYPE=0 has a different or reserved layout; do not simultaneously encode DSM hints.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 28, printed pages 29, PDF pages 29</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-029 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-029"><summary>NVM Figure 29 · Compare – Command Dword 14</summary>
<!-- claim:NVMCS13-NVM-FIG-029-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.10">12.10.</span>Figure 29, "Compare – Command Dword 14": CDW14 contains the low 32 bits of expected-tag space. It is not necessarily all Reference Tag: STS may consume some high bits.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 29, printed pages 29, PDF pages 29</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-030 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-030"><summary>NVM Figure 30 · Compare – Command Dword 15</summary>
<!-- claim:NVMCS13-NVM-FIG-030-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.11">12.11.</span>Figure 30, "Compare – Command Dword 15": CDW15 high16 is the Application Tag mask and low16 the expected tag. A zero mask bit excludes comparison rather than requiring a zero tag bit.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 30, printed pages 29, PDF pages 29</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>ELBATM</dt><dd>Tag comparison mask; zero bits exclude comparison, with extra support/alignment rules for Storage masking.</dd></div><div><dt>ELBAT</dt><dd>Logical Block Application Tag/expected tag; 16 bits, with checking governed by masks and disable sentinels.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-031 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-031"><summary>NVM Figure 31 · Compare – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-031-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.12">12.12.</span>Figure 31, "Compare – Command Specific Status Values": Compare SC together with SCT and this command’s applicable entries. Invalid Protection Information concerns settings/initial values incompatible with the format, distinct from a Guard Check Error. Apply only entries listed for the command.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1, Figure 31, printed pages 30, PDF pages 30</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-060 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-060"><summary>NVM Figure 60 · Verify – Command Dword 2 and Dword 3</summary>
<!-- claim:NVMCS13-NVM-FIG-060-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.13">12.13.</span>Figure 60, "Verify – Command Dword 2 and Dword 3": Combine CDW2/3 upper tags with CDW14 lower tags, then split expected storage/reference fields by PI format and STS. Unused bits are ignored as specified by the format.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 60, printed pages 52, PDF pages 52</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-061 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-061"><summary>NVM Figure 61 · Verify – Command Dword 10 and Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-061-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.14">12.14.</span>Figure 61, "Verify – Command Dword 10 and Command Dword 11": SLBA is 64 bits: low 32 in CDW10, high 32 in CDW11. Check range-specific modes before using it as an address.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 61, printed pages 52, PDF pages 52</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-062 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-062"><summary>NVM Figure 62 · Verify – Command Dword 12</summary>
<!-- claim:NVMCS13-NVM-FIG-062-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.15">12.15.</span>Figure 62, "Verify – Command Dword 12": CDW12 combines behavior bits with zero-based NLB. Compare/Verify require PRACT=0, while Read/Write select PRACT by metadata format. FUA does not order other commands.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 62, printed pages 52, PDF pages 52</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-063 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-063"><summary>NVM Figure 63 · Verify - Command Dword 13 if CETYPE is non-zero</summary>
<!-- claim:NVMCS13-NVM-FIG-063-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.16">12.16.</span>Figure 63, "Verify - Command Dword 13 if CETYPE is non-zero": With nonzero CETYPE, CDW13 low16 contains CEV. CETYPE=0 has a different or reserved layout; do not simultaneously encode DSM hints.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 63, printed pages 52, PDF pages 52</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-064 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-064"><summary>NVM Figure 64 · Verify – Command Dword 14</summary>
<!-- claim:NVMCS13-NVM-FIG-064-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.17">12.17.</span>Figure 64, "Verify – Command Dword 14": CDW14 contains the low 32 bits of expected-tag space. It is not necessarily all Reference Tag: STS may consume some high bits.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 64, printed pages 53, PDF pages 53</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-065 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-065"><summary>NVM Figure 65 · Verify – Command Dword 15</summary>
<!-- claim:NVMCS13-NVM-FIG-065-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.18">12.18.</span>Figure 65, "Verify – Command Dword 15": CDW15 high16 is the Application Tag mask and low16 the expected tag. A zero mask bit excludes comparison rather than requiring a zero tag bit.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 65, printed pages 53, PDF pages 53</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-066 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-066"><summary>NVM Figure 66 · Verify – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-066-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="12.19">12.19.</span>Figure 66, "Verify – Command Specific Status Values": Compare SC together with SCT and this command’s applicable entries. Invalid Protection Information concerns settings/initial values incompatible with the format, distinct from a Guard Check Error. Apply only entries listed for the command.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.5, Figure 66, printed pages 53, PDF pages 53</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-copy"><h2 id="heading-nvmcs-copy"><span class="section-number">13</span> Copy: source descriptors, contiguous destination, partial failure</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.01">13.01.</span>Calculate the expanded destination range before checking formats, limits, overlap, and atomicity. Copy reduces host data movement but is not an unconditional transaction.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-COPY -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.02">13.02.</span>Copy concatenates one or more source ranges in descriptor order into one contiguous destination range. Formats 0h/1h use one namespace; 2h/3h carry SNSID and require controller support and host enablement. Failure CQE DW0 is the lowest unsuccessful source index; later ranges may already have been copied.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SNSID</dt><dd>Source Namespace Identifier; Selects a Copy source namespace.</dd></div><div><dt>CQE</dt><dd>Completion Queue Entry, one completion-result structure in a CQ.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, printed pages 30-44, PDF pages 30-44</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>NR / NLB</td><td>Source count and per-range block count are zero-based</td><td>Check MSRC, MSSRL, and MCL</td></tr><tr><td>FCO</td><td>Formats 2h/3h can request fast copy only</td><td>Inspect DNR after Fast Copy Not Possible</td></tr><tr><td>Overlap</td><td>Formats 2h/3h prohibit source/destination overlap within one namespace</td><td>Formats 0h/1h need their separate overlap rules</td></tr><tr><td>NVMCSA</td><td>Revision 1.3 treats the destination as one write command</td><td>MAM, size, and boundary limits still apply</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>FCO</dt><dd>Fast Copy Only; requests a fast-copy method for the applicable source.</dd></div><div><dt>NR</dt><dd>Zero-based range-count field; actual descriptor count is NR+1.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="13.03">13.03.</span>Two descriptors with NLB=3 and SDLBA=100 write 100..103 and 104..107: eight blocks total. DW0=1 does not prove that the second or any later range is entirely unmodified.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SDLBA</dt><dd>Starting Destination LBA; Starts the contiguous Copy destination range.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-032 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-032"><summary>NVM Figure 32 · Copy – Data Pointer</summary>
<!-- claim:NVMCS13-NVM-FIG-032-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.04">13.04.</span>Figure 32, "Copy – Data Pointer": DPTR addresses descriptors rather than user data to copy or deallocate. Compute buffer length from descriptor size and the range count after reading the fields.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 32, printed pages 30, PDF pages 30</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-033 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-033"><summary>NVM Figure 33 · Copy – Command Dword 2 and Dword 3</summary>
<!-- claim:NVMCS13-NVM-FIG-033-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.05">13.05.</span>Figure 33, "Copy – Command Dword 2 and Dword 3": Upper/lower tag fields encode write-side Storage and initial Reference Tags. For Copy these command fields belong to the destination; source expectations are in descriptors.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 33, printed pages 30, PDF pages 30</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>LBTU</dt><dd>Upper/lower Logical Block Tags or expected tags; combine according to Guard format, STS, and Dword position.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-034 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-034"><summary>NVM Figure 34 · Copy – Command Dword 10 and Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-034-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.06">13.06.</span>Figure 34, "Copy – Command Dword 10 and Command Dword 11": SDLBA identifies the first destination block; subsequent sources concatenate in descriptor order rather than restarting the destination for each range.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SDLBA</dt><dd>Starting Destination LBA; Starts the contiguous Copy destination range.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 34, printed pages 30, PDF pages 30</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-035 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-035"><summary>NVM Figure 35 · Copy – Command Dword 12</summary>
<!-- claim:NVMCS13-NVM-FIG-035-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.07">13.07.</span>Figure 35, "Copy – Command Dword 12": Copy CDW12 separates read/write PI, descriptor format, and zero-based range count. STCRS is defined in Figure 127; this figure’s reference to Figure 115 is misplaced.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 35, printed pages 30-31, PDF pages 30-31</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>PRINFOR</dt><dd>Protection Information Read; Copy read-side PI handling and checking.</dd></div><div><dt>PRINFOW</dt><dd>Protection Information Write; Copy write-side PI handling and checking.</dd></div><div><dt>DESFMT</dt><dd>Copy Source Range Entry format selector; affects descriptor size, source NSID, and PI tag layout.</dd></div><div><dt>STCR</dt><dd>Storage Tag Check Read; Requests Copy read-side Storage Tag checking.</dd></div><div><dt>STCW</dt><dd>Storage Tag Check Write; Requests Copy write-side Storage Tag checking.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-036 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-036"><summary>NVM Figure 36 · Copy – Command Dword 13</summary>
<!-- claim:NVMCS13-NVM-FIG-036-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.08">13.08.</span>Figure 36, "Copy – Command Dword 13": CDW13 high16 carries Directive Specific and low16 carries CEV according to CETYPE. Directive and command extension are separate fields.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 36, printed pages 31, PDF pages 31</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-037 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-037"><summary>NVM Figure 37 · Copy – Command Dword 14</summary>
<!-- claim:NVMCS13-NVM-FIG-037-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.09">13.09.</span>Figure 37, "Copy – Command Dword 14": CDW14 supplies the low 32 bits of write tags. Split the space according to STS rather than discarding Storage Tag high bits.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 37, printed pages 31, PDF pages 31</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-038 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-038"><summary>NVM Figure 38 · Copy – Command Dword 15</summary>
<!-- claim:NVMCS13-NVM-FIG-038-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.10">13.10.</span>Figure 38, "Copy – Command Dword 15": Application Tag mask/tag occupy CDW15 high16/low16. Copy uses these for the destination write, with separate expected fields for sources.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 38, printed pages 32, PDF pages 32</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>LBATM</dt><dd>Tag comparison mask; zero bits exclude comparison, with extra support/alignment rules for Storage masking.</dd></div><div><dt>LBAT</dt><dd>Logical Block Application Tag/expected tag; 16 bits, with checking governed by masks and disable sentinels.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-039 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-039"><summary>NVM Figure 39 · Copy – Copy Descriptor Formats</summary>
<!-- claim:NVMCS13-NVM-FIG-039-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.11">13.11.</span>Figure 39, "Copy – Copy Descriptor Formats": Formats 0h/2h pair with eight-byte PI and 1h/3h with 16-byte PI; 2h/3h contain SNSID. Format 4h refers to Memory Copy in another command set; this NVM document does not provide its complete descriptor layout.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SNSID</dt><dd>Source Namespace Identifier; Selects a Copy source namespace.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 39, printed pages 32, PDF pages 32</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>DESFMT</dt><dd>Copy Source Range Entry format selector; affects descriptor size, source NSID, and PI tag layout.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-040 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-040"><summary>NVM Figure 40 · Copy – Source Range Entries Copy Descriptor Format 0h and Format 2h</summary>
<!-- claim:NVMCS13-NVM-FIG-040-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.12">13.12.</span>Figure 40, "Copy – Source Range Entries Copy Descriptor Format 0h and Format 2h": Formats 0h/2h use 32-byte source entries. SNSID/FCO locations are reserved in 0h and usable in 2h. Add one to NLB before accumulating destination length.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>FCO</dt><dd>Fast Copy Only; requests a fast-copy method for the applicable source.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 40, printed pages 33-34, PDF pages 33-34</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>ELBT</dt><dd>Upper/lower Logical Block Tags or expected tags; combine according to Guard format, STS, and Dword position.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-041 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-041"><summary>NVM Figure 41 · Copy – Source Range Entries Copy Descriptor Format 1h and Format 3h</summary>
<!-- claim:NVMCS13-NVM-FIG-041-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.13">13.13.</span>Figure 41, "Copy – Source Range Entries Copy Descriptor Format 1h and Format 3h": Formats 1h/3h use 40-byte source entries with larger tag fields for 16-byte PI. Format 3h carries SNSID/FCO; a 32-byte parsing stride is incorrect.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 41, printed pages 35-36, PDF pages 35-36</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-042 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-042"><summary>NVM Figure 42 · Source LBA and Destination LBA Relationship Example</summary>
<!-- claim:NVMCS13-NVM-FIG-042-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.14">13.14.</span>Figure 42, "Source LBA and Destination LBA Relationship Example": Sum the source lengths after reading the fields in descriptor order to form the contiguous destination. The diagram sums block counts, not raw NLB values missing one block per range.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 42, printed pages 38, PDF pages 38</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-043 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-043"><summary>NVM Figure 43 · Copy – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-043-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.15">13.15.</span>Figure 43, "Copy – Command Specific Status Values": Read Copy errors with CQE DW0’s lowest failed source index; later entries may already be processed, so rollback is not implied. Use DNR when considering retry after FCO failure.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2, Figure 43, printed pages 43-44, PDF pages 43-44</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-491 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-491"><summary>Base Figure 491 · Host Behavior Support – Data Structure</summary>
<!-- claim:NVMCS13-BASE-FIG-491-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="13.16">13.16.</span>Figure 491, "Host Behavior Support – Data Structure": Host Behavior Support CFD2E/CFD3E declare host acceptance of Copy formats2h/3h. Controller CDF support and host enablement are separate gates.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.30.1.15</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.30.1.15, Figure 491, printed pages 476-477, PDF pages 502-503</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-copy-pi"><h2 id="heading-nvmcs-copy-pi"><span class="section-number">14</span> Copy PI compatibility and transformation</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="14.01">14.01.</span>Classify whether source and destination use PI, then choose PRINFOR.PRACT and PRINFOW.PRACT. Every source must fit the selected mode.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PRINFOR</dt><dd>Protection Information Read; Copy read-side PI handling and checking.</dd></div><div><dt>PRINFOW</dt><dd>Protection Information Write; Copy write-side PI handling and checking.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-COPY-PI -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="14.02">14.02.</span>Matching Copy formats compare data size, metadata size, DPS, PIFA, significant LBSTM bits, PIF/QPIF, and STS. Corresponding PI formats require PI-only metadata on one side and no metadata on the other; Copy is not a general format converter.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.2.3-3.3.2.4; 5.3.2.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.2.3-3.3.2.4; 5.3.2.5, printed pages 40-43,146-150, PDF pages 40-43,146-150</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>PI → PI, 0/0</td><td>Matching formats: pass-through</td><td>Checking remains controlled by check bits</td></tr><tr><td>PI → PI, 1/1</td><td>Matching formats: replace</td><td>Check the read path and generate write PI</td></tr><tr><td>No PI → PI</td><td>Corresponding formats and write PRACT=1: insert</td><td>Destination metadata cannot include other content</td></tr><tr><td>PI → No PI</td><td>Corresponding formats and read PRACT=1: strip</td><td>Source metadata must be PI-only</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="14.03">14.03.</span>A 4096+8-byte namespace with 16b PI can copy to 4096+0 bytes under the corresponding-format conditions. A 4096+16-byte source with eight extra metadata bytes cannot use that strip exception.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-177 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-177"><summary>NVM Figure 177 · PI Processing for Copy MD=8 Pass-through</summary>
<!-- claim:NVMCS13-NVM-FIG-177-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="14.04">14.04.</span>Figure 177, "PI Processing for Copy MD=8 Pass-through": These are pass-through examples for matching PI formats with both PRACT bits zero. The two metadata-size examples retain their distinct layouts.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.2.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.5, Figure 177, printed pages 147, PDF pages 147</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-178 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-178"><summary>NVM Figure 178 · PI Processing for Copy MD=16 Pass-through</summary>
<!-- claim:NVMCS13-NVM-FIG-178-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="14.05">14.05.</span>Figure 178, "PI Processing for Copy MD=16 Pass-through": These are pass-through examples for matching PI formats with both PRACT bits zero. The two metadata-size examples retain their distinct layouts.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.2.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.5, Figure 178, printed pages 147, PDF pages 147</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-179 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-179"><summary>NVM Figure 179 · PI Processing for Copy MD=8 Replace</summary>
<!-- claim:NVMCS13-NVM-FIG-179-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="14.06">14.06.</span>Figure 179, "PI Processing for Copy MD=8 Replace": These are replace examples for matching PI formats with both PRACT bits one. Source PI checking and destination PI generation have distinct roles.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.2.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.5, Figure 179, printed pages 148, PDF pages 148</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-180 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-180"><summary>NVM Figure 180 · PI Processing for Copy MD=16 Replace</summary>
<!-- claim:NVMCS13-NVM-FIG-180-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="14.07">14.07.</span>Figure 180, "PI Processing for Copy MD=16 Replace": These are replace examples for matching PI formats with both PRACT bits one. Source PI checking and destination PI generation have distinct roles.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.2.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.5, Figure 180, printed pages 148, PDF pages 148</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-181 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-181"><summary>NVM Figure 181 · PI Processing for Copy MD=8 Insert</summary>
<!-- claim:NVMCS13-NVM-FIG-181-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="14.08">14.08.</span>Figure 181, "PI Processing for Copy MD=8 Insert": Use the insert exception only with corresponding PI formats and PI-only destination metadata; write PRACT must be one.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.2.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.5, Figure 181, printed pages 149, PDF pages 149</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-182 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-182"><summary>NVM Figure 182 · PI Processing for Copy MD=8 Strip</summary>
<!-- claim:NVMCS13-NVM-FIG-182-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="14.09">14.09.</span>Figure 182, "PI Processing for Copy MD=8 Strip": Use the strip exception only with corresponding PI formats and PI-only source metadata; read PRACT must be one.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.2.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.5, Figure 182, printed pages 149, PDF pages 149</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-dsm"><h2 id="heading-nvmcs-dsm"><span class="section-number">15</span> Dataset Management and three processing limits</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="15.01">15.01.</span>Determine whether each block satisfies all three limits before applying NVMDSMSV. Separate range/hint validity, attribute processing obligations, and actual media actions.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-DSM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="15.02">15.02.</span>Dataset Management is advisory: processing attributes does not guarantee deallocation. NR is zero-based; LLB in each 16-byte descriptor is one-based. DMRL, DMRSL, and DMSL constrain range count, individual range length, and total length.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DMRSL</dt><dd>Dataset Management Range Size Limit; The logical-block processing limit for one range.</dd></div><div><dt>DMRL</dt><dd>Dataset Management Ranges Limit, an actual range-count limit.</dd></div><div><dt>DMSL</dt><dd>Dataset Management Size Limit; The logical-block processing limit for the command.</dd></div><div><dt>LLB</dt><dd>DSM Length in Logical Blocks; one-based, unlike Read/Write NLB encoding.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, printed pages 44-48, PDF pages 44-48</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>AD / IDW / IDR</td><td>Deallocate/integral-write/integral-read hints</td><td>Combinations are permitted</td></tr><tr><td>Limits nonzero, variant=0</td><td>Exceeding a limit returns Command Size Limit Exceeded</td><td>All fitting blocks require attribute processing</td></tr><tr><td>Limits nonzero, variant=1</td><td>Should process the portion satisfying the limits</td><td>Do not report Size Limit Exceeded for this reason</td></tr><tr><td>All limits=0</td><td>Variant=1: no limits reported; variant=0: unsupported</td><td>All three fields must be zero or all nonzero</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>portion</dt><dd>A contiguous portion sent in one firmware-download transfer.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="15.03">15.03.</span>With DMRL=2, DMSL=1048, ranges of 1024 and 512 blocks, and a nonrestrictive DMRSL, variant=1 admits the first range and 24 blocks of the second. This does not guarantee deallocation of 1048 blocks.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-044 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-044"><summary>NVM Figure 44 · Dataset Management – Data Pointer</summary>
<!-- claim:NVMCS13-NVM-FIG-044-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="15.04">15.04.</span>Figure 44, "Dataset Management – Data Pointer": DPTR addresses descriptors rather than user data to copy or deallocate. Compute buffer length from descriptor size and the range count after reading the fields.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, Figure 44, printed pages 44, PDF pages 44</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-045 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-045"><summary>NVM Figure 45 · Dataset Management – Command Dword 10</summary>
<!-- claim:NVMCS13-NVM-FIG-045-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="15.05">15.05.</span>Figure 45, "Dataset Management – Command Dword 10": NR in CDW10 low8 is zero-based: FFh requests 256 ranges. This differs from the one-based DMRL processing limit.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, Figure 45, printed pages 44, PDF pages 44</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-046 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-046"><summary>NVM Figure 46 · Dataset Management – Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-046-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="15.06">15.06.</span>Figure 46, "Dataset Management – Command Dword 11": CDW11 bits2/1/0 select deallocate, integral-write, and integral-read hints. Processing AD does not guarantee deallocation.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, Figure 46, printed pages 44-45, PDF pages 44-45</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-047 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-047"><summary>NVM Figure 47 · Dataset Management – Range Definition</summary>
<!-- claim:NVMCS13-NVM-FIG-047-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="15.07">15.07.</span>Figure 47, "Dataset Management – Range Definition": Each 16-byte entry contains CATTR, one-based LLB, and 64-bit SLBA; 256 entries require 4096 bytes. Do not apply NLB’s add-one reading the fields.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>LLB</dt><dd>DSM Length in Logical Blocks; one-based, unlike Read/Write NLB encoding.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, Figure 47, printed pages 45, PDF pages 45</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-048 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-048"><summary>NVM Figure 48 · Dataset Management – Context Attributes</summary>
<!-- claim:NVMCS13-NVM-FIG-048-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="15.08">15.08.</span>Figure 48, "Dataset Management – Context Attributes": These context attributes describe an expected workload. The controller must preserve data integrity even when host hints are inaccurate.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, Figure 48, printed pages 47, PDF pages 47</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-049 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-049"><summary>NVM Figure 49 · Dataset Management – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-049-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="15.09">15.09.</span>Figure 49, "Dataset Management – Command Specific Status Values": DSM size-limit status depends on NVMDSMSV; variant=1 must not return that error because of processing limits.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3, Figure 49, printed pages 48, PDF pages 48</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-dealloc"><h2 id="heading-nvmcs-dealloc"><span class="section-number">16</span> Reading deallocated/unwritten blocks</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="16.01">16.01.</span>First determine whether successful reading is permitted, then interpret returned bytes. Allocation status, DRB, and PI have separate conditions.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DRB</dt><dd>Deallocated Read Behavior: selects the data-return behavior for deallocated logical blocks.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-DEALLOC -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="16.02">16.02.</span>When supported and enabled, DULBE makes Copy, Read, Verify, and Compare fail on deallocated/unwritten blocks. Otherwise DRB=001b returns zeros, 010b returns FFh, and 000b allows either; a block must return a deterministic value until its next write.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DULBE</dt><dd>Deallocated or Unwritten Logical Block Error Enable, requiring namespace DAE support.</dd></div><div><dt>DRB</dt><dd>Deallocated Read Behavior: selects the data-return behavior for deallocated logical blocks.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.3.2.1; 4.1.3.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3.2.1; 4.1.3.3, printed pages 47-48,66, PDF pages 47-48,66</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>DAE / DULBE</td><td>DAE is capability; DULBE is enablement</td><td>DULBE defaults to zero</td></tr><tr><td>DRB=000b</td><td>Does not mean arbitrary old data</td><td>Section 3.3.3.2.1 limits it to zeros or FFh</td></tr><tr><td>PI after deallocation</td><td>Tag bytes return FFh; Guard is FFh or CRC</td><td>Use DLFEAT.GDS</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="16.03">16.03.</span>One zero-filled Read does not prove successful sanitize; it may reflect DRB on deallocated blocks. Conversely, a DULBE error alone does not establish a media defect.</p></aside>
</section>
<section class="lesson" id="module-nvmcs-zero-uncorrectable"><h2 id="heading-nvmcs-zero-uncorrectable"><span class="section-number">17</span> Write Uncorrectable, Write Zeroes, and whole-namespace zeroing</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.01">17.01.</span>Neither command transfers a host user-data payload, but both change namespace semantics. Identify range mode before checking PI and size limits.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-ZERO-UNCORRECTABLE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.02">17.02.</span>Write Uncorrectable marks a range for unrecovered-read errors. Write Zeroes makes subsequent successful reads return zero data and non-PI metadata. Whole-namespace zeroing with NSZ=1 requires NSZS, DEAC=1, and zero-valued deallocation reads; the host should check CQE.LBACZ.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>LBACZ</dt><dd>LBAs Cleared to Zero; scope-confirmation bit for successful NSZ commands.</dd></div><div><dt>DEAC</dt><dd>Write Zeroes deallocation selection; interpret with namespace support, NSZ, and read behavior.</dd></div><div><dt>NSZ</dt><dd>Namespace Zeroes; requests whole-namespace zeroing with additional capability and DEAC conditions.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.7-3.3.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7-3.3.8, printed pages 56-61, PDF pages 56-61</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Write Uncorrectable</td><td>Marks blocks so later reads can report Unrecovered Read Error</td><td>Interpret WUSL with NVMWUSV</td></tr><tr><td>Write Zeroes PI</td><td>PRCHK=000b, STC=0</td><td>PRACT=1 is recommended for valid PI</td></tr><tr><td>WZSL / WZDSL</td><td>Select the applicable limit using DEAC</td><td>Neither limit applies with NSZ=1</td></tr><tr><td>LBACZ</td><td>One on a successful NSZ command reports the entire namespace</td><td>Zero reports the specified range</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>LBACZ</dt><dd>LBAs Cleared to Zero; scope-confirmation bit for successful NSZ commands.</dd></div><div><dt>PRCHK</dt><dd>Protection Information Check bits for Guard, Application, and Reference.</dd></div><div><dt>WZDSL</dt><dd>Specific Write Zeroes with Deallocate size limit; do not substitute WZSL.</dd></div><div><dt>DEAC</dt><dd>Write Zeroes deallocation selection; interpret with namespace support, NSZ, and read behavior.</dd></div><div><dt>WUSL</dt><dd>Write Uncorrectable Size Limit; A Write Uncorrectable size limit, interpreted with its variant capability.</dd></div><div><dt>NSZ</dt><dd>Namespace Zeroes; requests whole-namespace zeroing with additional capability and DEAC conditions.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="17.03">17.03.</span>Successful Completion with NSZ=1 but LBACZ=0 means only the range was zeroed. An older controller may ignore unsupported NSZ; command success alone does not establish whole-namespace zeroing.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-077 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-077"><summary>NVM Figure 77 · Write Uncorrectable – Command Dword 10 and Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-077-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.04">17.04.</span>Figure 77, "Write Uncorrectable – Command Dword 10 and Command Dword 11": SLBA is 64 bits: low 32 in CDW10, high 32 in CDW11. Check range-specific modes before using it as an address.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.7</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7, Figure 77, printed pages 56, PDF pages 56</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-078 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-078"><summary>NVM Figure 78 · Write Uncorrectable – Command Dword 12</summary>
<!-- claim:NVMCS13-NVM-FIG-078-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.05">17.05.</span>Figure 78, "Write Uncorrectable – Command Dword 12": Write Uncorrectable CDW12 carries Directive Type and zero-based NLB. It lacks Read/Write FUA/PRINFO fields, so their encoding cannot be copied wholesale.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.7</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7, Figure 78, printed pages 56, PDF pages 56</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>DTYPE</dt><dd>Directive Type; Selects the Directive type for the command.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-079 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-079"><summary>NVM Figure 79 · Write Uncorrectable – Command Dword 13</summary>
<!-- claim:NVMCS13-NVM-FIG-079-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.06">17.06.</span>Figure 79, "Write Uncorrectable – Command Dword 13": This CDW13 layout uses only high16 DSPEC, with low16 reserved. Reserved bits are not additional tag or length space.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.7</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7, Figure 79, printed pages 57, PDF pages 57</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-080 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-080"><summary>NVM Figure 80 · Write Uncorrectable – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-080-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.07">17.07.</span>Figure 80, "Write Uncorrectable – Command Specific Status Values": This Write Uncorrectable table lists Attempted Write to Read Only Range only; do not import other commands’ PI status sets.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.7</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7, Figure 80, printed pages 57, PDF pages 57</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-081 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-081"><summary>NVM Figure 81 · Write Zeroes – Command Dword 2 and Dword 3</summary>
<!-- claim:NVMCS13-NVM-FIG-081-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.08">17.08.</span>Figure 81, "Write Zeroes – Command Dword 2 and Dword 3": Upper/lower tag fields encode write-side Storage and initial Reference Tags. For Copy these command fields belong to the destination; source expectations are in descriptors.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 81, printed pages 59, PDF pages 59</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-082 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-082"><summary>NVM Figure 82 · Write Zeroes – Command Dword 10 and Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-082-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.09">17.09.</span>Figure 82, "Write Zeroes – Command Dword 10 and Command Dword 11": SLBA is 64 bits: low 32 in CDW10, high 32 in CDW11. Check range-specific modes before using it as an address.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 82, printed pages 59, PDF pages 59</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-083 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-083"><summary>NVM Figure 83 · Write Zeroes – Command Dword 12</summary>
<!-- claim:NVMCS13-NVM-FIG-083-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.10">17.10.</span>Figure 83, "Write Zeroes – Command Dword 12": NSZ is bit23 and DEAC bit25, leaving DTYPE at bits22:20. PRCHK=000b and STC=0 are required; whole-namespace mode also requires NSZS and zero-valued reads.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>PRCHK</dt><dd>Protection Information Check bits for Guard, Application, and Reference.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 83, printed pages 59-60, PDF pages 59-60</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-084 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-084"><summary>NVM Figure 84 · Write Zeroes – Command Dword 13 if CETYPE is cleared to 0h</summary>
<!-- claim:NVMCS13-NVM-FIG-084-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.11">17.11.</span>Figure 84, "Write Zeroes – Command Dword 13 if CETYPE is cleared to 0h": This CDW13 layout uses only high16 DSPEC, with low16 reserved. Reserved bits are not additional tag or length space.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 84, printed pages 60, PDF pages 60</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-085 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-085"><summary>NVM Figure 85 · Write Zeroes – Command Dword 13 if CETYPE is non-zero</summary>
<!-- claim:NVMCS13-NVM-FIG-085-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.12">17.12.</span>Figure 85, "Write Zeroes – Command Dword 13 if CETYPE is non-zero": CDW13 high16 carries Directive Specific and low16 carries CEV according to CETYPE. Directive and command extension are separate fields.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 85, printed pages 60, PDF pages 60</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-086 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-086"><summary>NVM Figure 86 · Write Zeroes – Command Dword 14</summary>
<!-- claim:NVMCS13-NVM-FIG-086-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.13">17.13.</span>Figure 86, "Write Zeroes – Command Dword 14": CDW14 supplies the low 32 bits of write tags. Split the space according to STS rather than discarding Storage Tag high bits.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 86, printed pages 60, PDF pages 60</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-087 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-087"><summary>NVM Figure 87 · Write Zeroes – Command Dword 15</summary>
<!-- claim:NVMCS13-NVM-FIG-087-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.14">17.14.</span>Figure 87, "Write Zeroes – Command Dword 15": Application Tag mask/tag occupy CDW15 high16/low16. Copy uses these for the destination write, with separate expected fields for sources.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 87, printed pages 60, PDF pages 60</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-088 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-088"><summary>NVM Figure 88 · Write Zeroes – Completion Queue Entry Dword 0</summary>
<!-- claim:NVMCS13-NVM-FIG-088-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.15">17.15.</span>Figure 88, "Write Zeroes – Completion Queue Entry Dword 0": For NSZ=1 with Successful Completion, LBACZ=1 establishes whole-namespace zeroing; zero reports only the command range.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 88, printed pages 61, PDF pages 61</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-089 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-089"><summary>NVM Figure 89 · Write Zeroes – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-089-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="17.16">17.16.</span>Figure 89, "Write Zeroes – Command Specific Status Values": Compare SC together with SCT and this command’s applicable entries. Invalid Protection Information concerns settings/initial values incompatible with the format, distinct from a Guard Check Error. Apply only entries listed for the command.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.3.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.8, Figure 89, printed pages 61, PDF pages 61</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-pi-formats"><h2 id="heading-nvmcs-pi-formats"><span class="section-number">18</span> 16/32/64b Guard and qualified PI</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="18.01">18.01.</span>Select the format with PIF; only PIF=11b delegates Guard width to QPIF, subject to QPIFS and STMLA. DPS separately selects protection type.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-PI-FORMATS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="18.02">18.02.</span>16b Guard PI occupies eight bytes; 32b and 64b Guard PI each occupy 16 bytes. Application Tag is 16 bits, and Storage/Reference Space is respectively 32, 80, or 48 bits. The 32b/64b formats require logical block data size of at least 4 KiB.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1; 4.1.5.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1; 4.1.5.3, printed pages 97-102,130-138, PDF pages 97-102,130-138</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>16b Guard</td><td>2-byte Guard + 2-byte App + 4-byte space</td><td>STS=0..32</td></tr><tr><td>32b Guard</td><td>4-byte Guard + 2-byte App + 10-byte space</td><td>STS=16..64</td></tr><tr><td>64b Guard</td><td>8-byte Guard + 2-byte App + 6-byte space</td><td>STS=0..48</td></tr><tr><td>STMLA</td><td>Bit masking / byte masking / no masking</td><td>Qualified type and QPIFS determine applicability</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="18.03">18.03.</span>With 64b Guard and STS=18, the high 18 bits of the 48-bit space form Storage Tag and the low 30 bits form Reference Tag. Total PI remains 16 bytes; increasing STS does not enlarge it.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-155 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-155"><summary>NVM Figure 155 · 16b Guard Protection Information Format when STS field is cleared to 0h</summary>
<!-- claim:NVMCS13-NVM-FIG-155-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="18.04">18.04.</span>Figure 155, "16b Guard Protection Information Format when STS field is cleared to 0h": With STS=0, eight-byte PI contains a 16-bit Guard, 16-bit Application, and 32-bit Reference field, with most-significant bytes first as shown.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.1, Figure 155, printed pages 131, PDF pages 131</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-156 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-156"><summary>NVM Figure 156 · 16b Guard Protection Information Format with non-zero STS</summary>
<!-- claim:NVMCS13-NVM-FIG-156-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="18.05">18.05.</span>Figure 156, "16b Guard Protection Information Format with non-zero STS": Adding Storage Tag keeps PI at eight bytes by dividing the 32-bit Reference space rather than appending new bytes.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.1, Figure 156, printed pages 132, PDF pages 132</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-157 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-157"><summary>NVM Figure 157 · 32b Guard Protection Information Format</summary>
<!-- claim:NVMCS13-NVM-FIG-157-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="18.06">18.06.</span>Figure 157, "32b Guard Protection Information Format": 16-byte PI with 32b Guard leaves 80 bits for Storage/Reference. STS is at least 16, leaving at least 16 Reference bits.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.2, Figure 157, printed pages 133, PDF pages 133</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-159 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-159"><summary>NVM Figure 159 · 64b Guard Protection Information Format</summary>
<!-- claim:NVMCS13-NVM-FIG-159-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="18.07">18.07.</span>Figure 159, "64b Guard Protection Information Format": 64b Guard PI is also 16 bytes, but only 48 bits remain for Storage/Reference. Do not reuse the 80-bit split from 32b Guard.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.3, Figure 159, printed pages 134, PDF pages 134</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-164 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-164"><summary>NVM Figure 164 · Storage and Reference Space Separation</summary>
<!-- claim:NVMCS13-NVM-FIG-164-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="18.08">18.08.</span>Figure 164, "Storage and Reference Space Separation": High STS bits form Storage Tag and remaining low bits Reference Tag; either can be absent for an allowed STS.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 164, printed pages 137, PDF pages 137</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-165 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-165"><summary>NVM Figure 165 · LBST and LBRT Minimum and Maximum Sizes</summary>
<!-- claim:NVMCS13-NVM-FIG-165-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="18.09">18.09.</span>Figure 165, "LBST and LBRT Minimum and Maximum Sizes": Subtract STS from each format’s total space to obtain Reference width: 32b Guard uses 80−STS, not 32−STS.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 165, printed pages 138, PDF pages 138</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-crc"><h2 id="heading-nvmcs-crc"><span class="section-number">19</span> CRC parameters, bit order, and known vectors</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="19.01">19.01.</span>CRC computations can use different polynomials, initial values, reflection, and final XOR. Those parameters and the stored bit order together determine the Guard result.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-CRC -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="19.02">19.02.</span>32b Guard uses CRC-32C. 64b Guard uses the NVM Express 64b CRC with polynomial AD93D23594C93659h, all-ones Init/XorOut, and RefIn/RefOut=true. The label CRC64 alone does not select the correct polynomial.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.1-5.3.1.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.1-5.3.1.3, printed pages 131-137, PDF pages 131-137</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>CRC-16</td><td>Guard CRC defined by SBC-4</td><td>NVM does not support the optional DIX IP checksum</td></tr><tr><td>CRC-32C</td><td>Polynomial 1EDC6F41h</td><td>4 KiB zero vector → 98F94189h</td></tr><tr><td>CRC-64/NVME</td><td>Reflected-register example 123456789 → AE8B14860A799888h</td><td>4 KiB zero vector → 6482D367EB22B64Eh</td></tr><tr><td>Coverage</td><td>Data plus metadata preceding PI</td><td>Exclude PI itself</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="19.03">19.03.</span>CRC-64/NVME produces C0DDBA7302ECA3ACh for 4 KiB of FFh and 6482D367EB22B64Eh for 4 KiB of zeros. Equal lengths do not imply equal CRCs because the check value depends on contents.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-158 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-158"><summary>NVM Figure 158 · 32b CRC Test Cases for 4 KiB Logical Block with no Metadata</summary>
<!-- claim:NVMCS13-NVM-FIG-158-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="19.04">19.04.</span>Figure 158, "32b CRC Test Cases for 4 KiB Logical Block with no Metadata": Validate CRC32C with all four 4 KiB vectors, not zeros alone. Incrementing/decrementing patterns help expose ordering errors.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.2, Figure 158, printed pages 133, PDF pages 133</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-160 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-160"><summary>NVM Figure 160 · 64b CRC Polynomials</summary>
<!-- claim:NVMCS13-NVM-FIG-160-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="19.05">19.05.</span>Figure 160, "64b CRC Polynomials": Polynomial remainders over GF(2) explain CRC, while actual NVM CRC64 also requires the initialization, reflection, and XOR parameters in Figure161.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.3, Figure 160, printed pages 134-135, PDF pages 134-135</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-161 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-161"><summary>NVM Figure 161 · 64-bit CRC Rocksoft Model Parameters</summary>
<!-- claim:NVMCS13-NVM-FIG-161-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="19.06">19.06.</span>Figure 161, "64-bit CRC Rocksoft Model Parameters": The full set identifies NVM CRC64: Poly=AD93D23594C93659h, all-ones Init/XorOut, RefIn/RefOut=true. Its Check=11199E506128D175h is the 64-bit reversal of the conventional LSB-first register result AE8B14860A799888h. Cross-check representation using Figure 163 vectors.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.3, Figure 161, printed pages 136, PDF pages 136</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-162 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-162"><summary>NVM Figure 162 · Logical Block and Metadata Example</summary>
<!-- claim:NVMCS13-NVM-FIG-162-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="19.07">19.07.</span>Figure 162, "Logical Block and Metadata Example": Bits0..7 of each byte illustrate reflected input. Do not confuse diagram order with a host integer’s native endianness.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.3, Figure 162, printed pages 136, PDF pages 136</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-163 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-163"><summary>NVM Figure 163 · 64b CRC Test Cases for 4 KiB Logical Block with no Metadata</summary>
<!-- claim:NVMCS13-NVM-FIG-163-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="19.08">19.08.</span>Figure 163, "64b CRC Test Cases for 4 KiB Logical Block with no Metadata": Check all four CRC64 vectors against the command-set parameters. Hex grouping does not change the number, but adding or removing digits does.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.3, Figure 163, printed pages 137, PDF pages 137</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-tag-layout"><h2 id="heading-nvmcs-tag-layout"><span class="section-number">20</span> Packing Storage/Reference Tags into Dwords</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.01">20.01.</span>Determine total space width, split the tags, then pack command Dwords. Similar names do not make Write values interchangeable with Read expected values.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-TAG-LAYOUT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.02">20.02.</span>Storage Tag occupies the high STS bits of Storage/Reference Space, with Reference Tag in the remaining low bits. Commands supply actual or expected tags in up to 80 bits across CDW2, CDW3, and CDW14; Guard formats use different subsets.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, printed pages 137-141, PDF pages 137-141</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>16b Guard, STS=0</td><td>CDW14 contains the 32-bit reference</td><td>CDW2/3 are ignored for this tag</td></tr><tr><td>32b Guard, STS=32</td><td>CDW2 low16 + CDW3 high16 carry Storage</td><td>CDW3 low16 + CDW14 carry the 48-bit Reference</td></tr><tr><td>64b Guard, STS=18</td><td>CDW3 low16 + CDW14 high2 carry Storage</td><td>CDW14 low30 carry Reference</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="20.03">20.03.</span>For 64b Guard, STS=18, Storage Tag=0x12345, Reference Tag=0x2A: CDW3 low16=0x48D1 and CDW14=(1&lt;&lt;30)|0x2A=0x4000002A. Read uses expected tags in the same layout.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-166 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-166"><summary>NVM Figure 166 · LBST, ELBST, ILBRT, and EILBRT fields Format in Command Dwords</summary>
<!-- claim:NVMCS13-NVM-FIG-166-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.04">20.04.</span>Figure 166, "LBST, ELBST, ILBRT, and EILBRT fields Format in Command Dwords": Map the abstract space of up to 80 bits across three Dwords. Remove format-specific unused bits before splitting storage/reference.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 166, printed pages 138, PDF pages 138</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-167 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-167"><summary>NVM Figure 167 · I/O Command LBST, ELBST, ILBRT, and EILBRT fields Format</summary>
<!-- claim:NVMCS13-NVM-FIG-167-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.05">20.05.</span>Figure 167, "I/O Command LBST, ELBST, ILBRT, and EILBRT fields Format": This table lists command bits actually used by each Guard format. Unused bits are not new implementation-defined fields.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 167, printed pages 139, PDF pages 139</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-168 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-168"><summary>NVM Figure 168 · 16b Guard Protection Information Write Command Example</summary>
<!-- claim:NVMCS13-NVM-FIG-168-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.06">20.06.</span>Figure 168, "16b Guard Protection Information Write Command Example": With 16b Guard and STS=0, CDW14 alone carries the 32-bit initial/expected reference. Interpret the example’s LBADS through Figure125’s exponent definition.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 168, printed pages 139, PDF pages 139</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-169 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-169"><summary>NVM Figure 169 · 16b Guard Protection Information Read Command Example</summary>
<!-- claim:NVMCS13-NVM-FIG-169-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.07">20.07.</span>Figure 169, "16b Guard Protection Information Read Command Example": With 16b Guard and STS=0, CDW14 alone carries the 32-bit initial/expected reference. Interpret the example’s LBADS through Figure125’s exponent definition.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 169, printed pages 139-140, PDF pages 139-140</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-170 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-170"><summary>NVM Figure 170 · 32b Guard Protection Information Write Command Example</summary>
<!-- claim:NVMCS13-NVM-FIG-170-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.08">20.08.</span>Figure 170, "32b Guard Protection Information Write Command Example": The 80-bit space with STS=32 contains Storage32 followed by Reference48. CDW3 high16 belongs to Storage and low16 to Reference; cross-check Figure171’s overlapping range against Figures166/170.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 170, printed pages 140, PDF pages 140</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-171 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-171"><summary>NVM Figure 171 · 32b Guard Protection Information Read Command Example</summary>
<!-- claim:NVMCS13-NVM-FIG-171-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.09">20.09.</span>Figure 171, "32b Guard Protection Information Read Command Example": The 80-bit space with STS=32 contains Storage32 followed by Reference48. CDW3 high16 belongs to Storage and low16 to Reference; cross-check Figure171’s overlapping range against Figures166/170.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 171, printed pages 140, PDF pages 140</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-172 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-172"><summary>NVM Figure 172 · 64b Guard Protection Information Write Command Example</summary>
<!-- claim:NVMCS13-NVM-FIG-172-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.10">20.10.</span>Figure 172, "64b Guard Protection Information Write Command Example": With a 48-bit space and STS=18, the low two Storage bits occupy CDW14 high2 and Reference30 occupies CDW14 low30.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 172, printed pages 141, PDF pages 141</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-173 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-173"><summary>NVM Figure 173 · 64b Guard Protection Information Read Command Example</summary>
<!-- claim:NVMCS13-NVM-FIG-173-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="20.11">20.11.</span>Figure 173, "64b Guard Protection Information Read Command Example": With a 48-bit space and STS=18, the low two Storage bits occupy CDW14 high2 and Reference30 occupies CDW14 low30.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.1.4, Figure 173, printed pages 141, PDF pages 141</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-pi-checking"><h2 id="heading-nvmcs-pi-checking"><span class="section-number">21</span> Combining PRACT with PRCHK/STC</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="21.01">21.01.</span>First determine whether namespace PI is enabled, then choose a processing branch by command direction and metadata size. Evaluate checking bits and special disable values afterward.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-PI-CHECKING -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="21.02">21.02.</span>PRACT controls PI transfer, insertion, stripping, or replacement. PRCHK Guard/Application/Reference bits and independent STC control checking. With PRACT=1 and MS&gt;PI size, Read still returns all metadata; PRACT=1 does not universally mean stripping PI.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.1.5; 5.3.2-5.3.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5; 5.3.2-5.3.3, printed pages 21-22,141-152, PDF pages 21-22,141-152</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Write, PRACT=1</td><td>Insert PI when MS=PI; replace it when MS&gt;PI</td><td>This generation branch ignores PRCHK/STC</td></tr><tr><td>Read, PRACT=1</td><td>Perform requested checks; strip only when MS=PI</td><td>MS&gt;PI still returns metadata including PI</td></tr><tr><td>Type 1 / Type 2</td><td>Reference increments per block</td><td>Type1 initial value must match relevant low SLBA bits</td></tr><tr><td>Type 3</td><td>Should not compare a computed reference</td><td>An RTCHK rejection uses Invalid Protection Information</td></tr><tr><td>Disable sentinels</td><td>Type 1/2 disable all PI checks when Application Tag=FFFFh; Type 3 additionally requires an all-ones Reference Tag, if defined</td><td>Overrides PRCHK/STC settings</td></tr><tr><td>Masks</td><td>A zero mask bit excludes comparison</td><td>Storage masking also obeys STMLA</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>RTCHK</dt><dd>Reference Tag Check; Requests Reference Tag checking.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="21.03">21.03.</span>For 16b Guard, MS=16, Read PRACT=1, the host still receives 16 metadata bytes. With MS=8 it receives data only. The same PRACT value produces different buffer lengths under different MS.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-011 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-011"><summary>NVM Figure 11 · Protection Information Field Definition</summary>
<!-- claim:NVMCS13-NVM-FIG-011-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="21.04">21.04.</span>Figure 11, "Protection Information Field Definition": PRACT selects an action and PRCHK selects three checks. With PRACT=1, compare MS with PI size to determine stripping/insertion versus preservation of metadata size.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.1.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5, Figure 11, printed pages 21-22, PDF pages 21-22</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>GRDCHK</dt><dd>Guard Check; Requests Guard checking.</dd></div><div><dt>ATCHK</dt><dd>Application Tag Check; Requests Application Tag checking.</dd></div><div><dt>RTCHK</dt><dd>Reference Tag Check; Requests Reference Tag checking.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-012 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-012"><summary>NVM Figure 12 · Storage Tag Check Definition</summary>
<!-- claim:NVMCS13-NVM-FIG-012-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="21.05">21.05.</span>Figure 12, "Storage Tag Check Definition": STC enables Storage Tag checking. When STS=0 there is no Storage Tag and the controller ignores STC.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §2.1.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5, Figure 12, printed pages 22, PDF pages 22</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-174 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-174"><summary>NVM Figure 174 · Write Command 16b Guard Protection Information Processing</summary>
<!-- claim:NVMCS13-NVM-FIG-174-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="21.06">21.06.</span>Figure 174, "Write Command 16b Guard Protection Information Processing": Write PRACT=0 preserves host PI. PRACT=1 inserts when MS=PI and replaces when MS&gt;PI; the PI-generation branch ignores checking bits.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.2.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.1, Figure 174, printed pages 143, PDF pages 143</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-175 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-175"><summary>NVM Figure 175 · Read 16b Guard Command Protection Information Processing</summary>
<!-- claim:NVMCS13-NVM-FIG-175-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="21.07">21.07.</span>Figure 175, "Read 16b Guard Command Protection Information Processing": Read performs requested checks first. PRACT=1 strips PI only when MS=PI; with MS&gt;PI, PI is still returned within metadata.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.2.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.2, Figure 175, printed pages 145, PDF pages 145</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-176 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-176"><summary>NVM Figure 176 · Protection Information Processing for Compare</summary>
<!-- claim:NVMCS13-NVM-FIG-176-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="21.08">21.08.</span>Figure 176, "Protection Information Processing for Compare": Compare performs PI checks on both host and media inputs. Ordinary comparison covers data and non-PI metadata; comparing PI alone does not establish equal contents.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.3.2.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.3.2.4, Figure 176, printed pages 146, PDF pages 146</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-basic-features"><h2 id="heading-nvmcs-basic-features"><span class="section-number">22</span> Basic Feature scopes and exceptions</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="22.01">22.01.</span>Identify scope, units, and saveability when reading Features. Get, Set, and Supported Capabilities responses do not share one payload interpretation.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-BASIC-FEATURES -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="22.02">22.02.</span>FID 03h describes namespace LBA ranges, 05h controls namespace error recovery, and 0Ah controls controller normal atomicity. The NVM Power Management extension uses an NPWG-sized Read as the reference for Idle I/O Exit Latency Limit.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.1-4.1.3.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.1-4.1.3.4, printed pages 64-67, PDF pages 64-67</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>FID 03h</td><td>4096-byte contiguous buffer; up to 64 64-byte entries</td><td>NUM is zero-based; each new Set replaces prior information</td></tr><tr><td>FID 05h.TLER</td><td>100 ms units, timed from error-recovery start</td><td>Zero means no timeout; applies to LR-enabled commands</td></tr><tr><td>FID 03h attributes</td><td>Hide/Overwriteable are host-use hints</td><td>They do not establish security isolation or data protection</td></tr><tr><td>FID 02h extension</td><td>Idle-exit reference is an NPWG-sized Read</td><td>Other commands may exceed that latency limit</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="22.03">22.03.</span>TLER=5 gives an error-recovery limit of 500 ms, not a 500 ms deadline measured from SQ submission. LBA Range Type NUM=0 represents one entry.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SQ</dt><dd>Submission Queue, the queue into which the host places commands.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-092 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-092"><summary>NVM Figure 92 · Feature Identifiers – NVM Command Set</summary>
<!-- claim:NVMCS13-NVM-FIG-092-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="22.04">22.04.</span>Figure 92, "Feature Identifiers – NVM Command Set": Read scope and buffer requirements, then the persistence footnote. The nonsaveable persistence column does not govern saveable Features.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3, Figure 92, printed pages 64, PDF pages 64</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-093 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-093"><summary>NVM Figure 93 · Set Features – Command Specific Status Values</summary>
<!-- claim:NVMCS13-NVM-FIG-093-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="22.05">22.05.</span>Figure 93, "Set Features – Command Specific Status Values": This error is required when the controller checks LBA Range Type and detects overlap. Successful Set does not imply comprehensive validation.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3, Figure 93, printed pages 64, PDF pages 64</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-094 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-094"><summary>NVM Figure 94 · LBA Range Type – Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-094-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="22.06">22.06.</span>Figure 94, "LBA Range Type – Command Dword 11": NUM low6 is zero-based: Set specifies valid entries and Get returns the count in CQE DW0. Neither is a byte count.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.2, Figure 94, printed pages 65, PDF pages 65</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-095 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-095"><summary>NVM Figure 95 · LBA Range Type – Completion Queue Entry Dword 0</summary>
<!-- claim:NVMCS13-NVM-FIG-095-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="22.07">22.07.</span>Figure 95, "LBA Range Type – Completion Queue Entry Dword 0": NUM low6 is zero-based: Set specifies valid entries and Get returns the count in CQE DW0. Neither is a byte count.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.2, Figure 95, printed pages 65, PDF pages 65</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-096 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-096"><summary>NVM Figure 96 · LBA Range Type – Data Structure Entry</summary>
<!-- claim:NVMCS13-NVM-FIG-096-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="22.08">22.08.</span>Figure 96, "LBA Range Type – Data Structure Entry": A 64-byte entry separates intended use, host hints, and range. SLBA/NLB describe logical blocks, while GUID identifies the range type rather than granting authorization.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.2, Figure 96, printed pages 65-66, PDF pages 65-66</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-097 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-097"><summary>NVM Figure 97 · Error Recovery – Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-097-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="22.09">22.09.</span>Figure 97, "Error Recovery – Command Dword 11": DULBE is bit16 and TLER low16 uses 100 ms units. TLER=0 disables the retry timeout; timing begins when recovery starts.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.3, Figure 97, printed pages 66, PDF pages 66</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-098 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-098"><summary>NVM Figure 98 · Write Atomicity Normal – Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-098-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="22.10">22.10.</span>Figure 98, "Write Atomicity Normal – Command Dword 11": DN=1 releases only normal-atomicity obligations; power-fail atomicity remains. This Feature has controller scope.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>DN</dt><dd>Disable Normal in Write Atomicity Normal; does not remove power-fail atomicity.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.4, Figure 98, printed pages 66-67, PDF pages 66-67</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-log-events"><h2 id="heading-nvmcs-log-events"><span class="section-number">23</span> NVM extensions to AER, SMART, and error records</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="23.01">23.01.</span>Use events to direct investigation, then interpret the fields logs using their scope and command-set definitions. Classify commands correctly when interpreting statistics instead of guessing from opcode names.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-LOG-EVENTS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="23.02">23.02.</span>Frequent NUSE changes and ANA-induced capacity-report changes do not generate Namespace Attribute Changed events. Error Information reports the lowest erroneous LBA. Self-test FLBA is meaningful only with its valid bit and may identify only one of several failing blocks.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>FLBA</dt><dd>Failing LBA, defined by the NVM Command Set as one logical block address that caused self-test failure.</dd></div><div><dt>ANA</dt><dd>Asymmetric Namespace Access: the state of access to a namespace through different controllers.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §1.4.2; 4.1.1; 4.1.3.5; 4.1.4.1-4.1.4.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §1.4.2; 4.1.1; 4.1.3.5; 4.1.4.1-4.1.4.4, printed pages 10-11,62,67,75-77, PDF pages 10-11,62,67,75-77</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>LBASIN / RLCCN</td><td>FID0Bh bits 13/22</td><td>Enable LBA Status / Rate Limiting notices</td></tr><tr><td>SMART units</td><td>Convert to 512-byte units, then apply Base counter encoding</td><td>One 4 KiB block is not one Data Unit</td></tr><tr><td>Read categories</td><td>Data Units Read includes Verify; Host Read includes Copy</td><td>Compare and Read belong to both categories</td></tr><tr><td>Persistent Event 06h</td><td>Create/single-delete records contain FLBAS and DPS</td><td>Both fields are reserved for delete-all</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="23.03">23.03.</span>A Self-test record with FLBA=100 and valid=1 identifies one failing LBA, not a clean bill of health for all others. Error Information’s “lowest LBA” semantics cannot be applied to FLBA.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>FLBA</dt><dd>Failing LBA, defined by the NVM Command Set as one logical block address that caused self-test failure.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-090 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-090"><summary>NVM Figure 90 · Asynchronous Event Information – Notice</summary>
<!-- claim:NVMCS13-NVM-FIG-090-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="23.04">23.04.</span>Figure 90, "Asynchronous Event Information – Notice": Distinguish namespace-attribute, LBA Status, and Rate Limiting notices. NUSE and ANA capacity exceptions do not generate attribute-change notices.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>ANA</dt><dd>Asymmetric Namespace Access: the state of access to a namespace through different controllers.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.1, Figure 90, printed pages 62, PDF pages 62</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-099 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-099"><summary>NVM Figure 99 · Asynchronous Event Configuration – NVM Command Set specific Bit Definitions</summary>
<!-- claim:NVMCS13-NVM-FIG-099-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="23.05">23.05.</span>Figure 99, "Asynchronous Event Configuration – NVM Command Set specific Bit Definitions": Bits13/22 control LBA Status and Rate Limiting notices respectively. Log retrieval and event clearing still follow each log’s RAE procedure.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>RAE</dt><dd>Retain Asynchronous Event, the Get Log Page selector controlling retention of a related asynchronous event.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.5, Figure 99, printed pages 67, PDF pages 67</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-109 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-109"><summary>NVM Figure 109 · Get Log Page – Log Page Identifiers</summary>
<!-- claim:NVMCS13-NVM-FIG-109-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="23.06">23.06.</span>Figure 109, "Get Log Page – Log Page Identifiers": The log index lists NVM extensions, scope, and CSI applicability. 28h uses CSI; restore-to-default behavior is not ordinary reset persistence.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4, Figure 109, printed pages 75-76, PDF pages 75-76</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-110 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-110"><summary>NVM Figure 110 · Error Information Log Entry Data Structure – User Data</summary>
<!-- claim:NVMCS13-NVM-FIG-110-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="23.07">23.07.</span>Figure 110, "Error Information Log Entry Data Structure – User Data": Error Information bytes23:16 contain the lowest erroneous LBA when applicable. Associate it with the original command and namespace, not a subsystem-wide byte address.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.4.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.1, Figure 110, printed pages 76, PDF pages 76</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-111 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-111"><summary>NVM Figure 111 · Self-test Results Data Structure</summary>
<!-- claim:NVMCS13-NVM-FIG-111-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="23.08">23.08.</span>Figure 111, "Self-test Results Data Structure": Use FLBA only when its valid bit is one. One failing block may represent several failures, unlike Error Information’s lowest-LBA rule.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.4.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.3, Figure 111, printed pages 76, PDF pages 76</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-112 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-112"><summary>NVM Figure 112 · Change Namespace Event Data Format (Event Type 06h)</summary>
<!-- claim:NVMCS13-NVM-FIG-112-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="23.09">23.09.</span>Figure 112, "Change Namespace Event Data Format (Event Type 06h)": Create records host-specified values, single-delete records the deleted namespace’s Identify values, and delete-all reserves both fields.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.4.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.4, Figure 112, printed pages 77, PDF pages 77</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-lba-status"><h2 id="heading-nvmcs-lba-status"><span class="section-number">24</span> LBA Status: notices, scans, and recovery</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.01">24.01.</span>Potentially unrecoverable does not mean every block necessarily fails to read. Identify ATYPE, check buffer capacity and completion condition, then arrange data recovery.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>ATYPE</dt><dd>Get LBA Status Action Type: 02h allocated, 10h scan, 11h tracked.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-LBA-STATUS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.02">24.02.</span>LID 0Eh first identifies namespace ranges worth investigating; Get LBA Status returns detailed descriptors. ATYPE=02h reports tracked allocated LBAs, 10h scans and returns tracked/untracked candidates, and 11h returns tracked candidates without a foreground scan.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>ATYPE</dt><dd>Get LBA Status Action Type: 02h allocated, 10h scan, 11h tracked.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.6; 4.1.4.5; 4.2.1; 5.2.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.6; 4.1.4.5; 4.2.1; 5.2.1, printed pages 67-68,77-79,114-122, PDF pages 67-68,77-79,114-122</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>MNDW / RL</td><td>MNDW is zero-based dwords; RL=0 runs through NSZE−1</td><td>RL=0 does not query one block</td></tr><tr><td>NLSD / CMPC</td><td>Actual descriptor count / completion reason</td><td>CMPC=1 means more data or incomplete scan; 2 means complete</td></tr><tr><td>LSIPI / LSIRI</td><td>100 ms units; host cannot change the poll interval</td><td>Set returns the closest supported value</td></tr><tr><td>RAE / LSGC</td><td>Read chunks with RAE=1; RAE=0 clears the event and allows updates</td><td>Reread the header and check generation</td></tr><tr><td>TLBAAG</td><td>02h may report allocation at a larger granularity</td><td>A mixed unit is reported allocated as a whole</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>CMPC</dt><dd>Completion Condition; describes whether Get LBA Status finished the requested range.</dd></div><div><dt>MNDW</dt><dd>Maximum Number of Dwords; bounds Get LBA Status response length.</dd></div><div><dt>NLSD</dt><dd>Number of LBA Status Descriptors; an actual descriptor count.</dd></div><div><dt>RAE</dt><dd>Retain Asynchronous Event, the Get Log Page selector controlling retention of a related asynchronous event.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="24.03">24.03.</span>NLSLNE=0 with nonzero ESTULB is not an all-clear: examine the full ranges of attached namespaces. Recover suspect LBAs from another reliable source and rewrite them; later queries remove successfully rewritten entries unless newly detected again.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-100 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-100"><summary>NVM Figure 100 · LBA Status Information Attributes – Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-100-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.04">24.04.</span>Figure 100, "LBA Status Information Attributes – Command Dword 11": High16 LSIPI is the unchangeable poll interval, low16 LSIRI the report interval. Both use 100 ms units; Set returns the nearest supported value.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.6</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.6, Figure 100, printed pages 68, PDF pages 68</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-113 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-113"><summary>NVM Figure 113 · LBA Status Information Log Page</summary>
<!-- claim:NVMCS13-NVM-FIG-113-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.05">24.05.</span>Figure 113, "LBA Status Information Log Page": Read byte length and namespace-element count first. NLSLNE=0 with nonzero ESTULB still warrants investigation; LSGC is a wrapping 16-bit counter.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.4.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.5, Figure 113, printed pages 77-78, PDF pages 77-78</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-114 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-114"><summary>NVM Figure 114 · LBA Status Log Namespace Element</summary>
<!-- claim:NVMCS13-NVM-FIG-114-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.06">24.06.</span>Figure 114, "LBA Status Log Namespace Element": NEID identifies the namespace and RATYPE recommends the later Get LBA Status ATYPE. NLRD=FFFFFFFFh means no range list is available and the whole namespace should be examined.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.4.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.5, Figure 114, printed pages 78, PDF pages 78</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-115 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-115"><summary>NVM Figure 115 · LBA Range Descriptor</summary>
<!-- claim:NVMCS13-NVM-FIG-115-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.07">24.07.</span>Figure 115, "LBA Range Descriptor": Each 16-byte range uses RSLBA and zero-based RNLB. It is a coarse log range, not the final status descriptor from Get LBA Status.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>RNLB</dt><dd>Range Number of Logical Blocks in the LBA Status log; zero-based.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.4.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.5, Figure 115, printed pages 78, PDF pages 78</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>RNLB</dt><dd>Range Number of Logical Blocks in the LBA Status log; zero-based.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-135 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-135"><summary>NVM Figure 135 · Get LBA Status – Data Pointer</summary>
<!-- claim:NVMCS13-NVM-FIG-135-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.08">24.08.</span>Figure 135, "Get LBA Status – Data Pointer": DPTR addresses the host destination: Read returns data and Get LBA Status returns a descriptor list. Their response data formats differ.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.2.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.2.1, Figure 135, printed pages 114, PDF pages 114</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-136 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-136"><summary>NVM Figure 136 · Get LBA Status – Command Dword 10 and Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-136-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.09">24.09.</span>Figure 136, "Get LBA Status – Command Dword 10 and Command Dword 11": SLBA is 64 bits: low 32 in CDW10, high 32 in CDW11. Check range-specific modes before using it as an address.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.2.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.2.1, Figure 136, printed pages 114, PDF pages 114</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-137 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-137"><summary>NVM Figure 137 · Get LBA Status – Command Dword 12</summary>
<!-- claim:NVMCS13-NVM-FIG-137-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.10">24.10.</span>Figure 137, "Get LBA Status – Command Dword 12": MNDW is the zero-based maximum dword count: buffer bytes=(MNDW+1)×4. NLSD determines the actual returned descriptor count.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>MNDW</dt><dd>Maximum Number of Dwords; bounds Get LBA Status response length.</dd></div><div><dt>NLSD</dt><dd>Number of LBA Status Descriptors; an actual descriptor count.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.2.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.2.1, Figure 137, printed pages 114, PDF pages 114</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-138 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-138"><summary>NVM Figure 138 · Get LBA Status – Command Dword 13</summary>
<!-- claim:NVMCS13-NVM-FIG-138-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.11">24.11.</span>Figure 138, "Get LBA Status – Command Dword 13": ATYPE=02h/10h/11h selects allocated/scan/tracked behavior. RL=0 runs from SLBA through the final namespace LBA rather than requesting zero length.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.2.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.2.1, Figure 138, printed pages 114-115, PDF pages 114-115</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-139 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-139"><summary>NVM Figure 139 · LBA Status Descriptor List</summary>
<!-- claim:NVMCS13-NVM-FIG-139-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.12">24.12.</span>Figure 139, "LBA Status Descriptor List": An eight-byte header precedes 16-byte descriptors; NLSD is an actual count. CMPC=1 means information is incomplete even if the CQE succeeded.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CMPC</dt><dd>Completion Condition; describes whether Get LBA Status finished the requested range.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.2.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.2.1, Figure 139, printed pages 116-117, PDF pages 116-117</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-140 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-140"><summary>NVM Figure 140 · LBA Status Descriptor Entry</summary>
<!-- claim:NVMCS13-NVM-FIG-140-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.13">24.13.</span>Figure 140, "LBA Status Descriptor Entry": NLB is zero-based. LBARS=010b applies to ATYPE02h and means at least one block is allocated, not that every block is individually allocated.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>LBARS</dt><dd>LBA Range Status; Describes the state of an LBA range.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.2.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.2.1, Figure 140, printed pages 117-118, PDF pages 117-118</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>DSLBA</dt><dd>Descriptor Starting LBA; Starts an LBA Status descriptor range.</dd></div><div><dt>LBARS</dt><dd>LBA Range Status; Describes the state of an LBA range.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-142 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-142"><summary>NVM Figure 142 · Example LBA Status Log Namespace Element returned by LBA Status Information</summary>
<!-- claim:NVMCS13-NVM-FIG-142-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.14">24.14.</span>Figure 142, "Example LBA Status Log Namespace Element returned by LBA Status Information": The example namespace element supplies two candidate ranges and RATYPE=11h as input to later queries, not a final diagnosis for every candidate block.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.2.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.2.1, Figure 142, printed pages 121, PDF pages 121</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-143 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-143"><summary>NVM Figure 143 · Example Get LBA Status Descriptors for LBA Range Descriptor 0</summary>
<!-- claim:NVMCS13-NVM-FIG-143-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.15">24.15.</span>Figure 143, "Example Get LBA Status Descriptors for LBA Range Descriptor 0": A log range can yield different numbers of detailed Get LBA Status descriptors. Use actual NLSD, NLB, and CMPC to determine whether follow-up is needed.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.2.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.2.1, Figure 143, printed pages 121, PDF pages 121</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>DSLBA</dt><dd>Descriptor Starting LBA; Starts an LBA Status descriptor range.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-144 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-144"><summary>NVM Figure 144 · Example Get LBA Status Descriptors for LBA Range Descriptor 1</summary>
<!-- claim:NVMCS13-NVM-FIG-144-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="24.16">24.16.</span>Figure 144, "Example Get LBA Status Descriptors for LBA Range Descriptor 1": A log range can yield different numbers of detailed Get LBA Status descriptors. Use actual NLSD, NLB, and CMPC to determine whether follow-up is needed.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.2.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.2.1, Figure 144, printed pages 121-122, PDF pages 121-122</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-sanitize"><h2 id="heading-nvmcs-sanitize"><span class="section-number">25</span> NVM rules for Sanitize and Media Verification</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="25.01">25.01.</span>Identify target, operation state, and allocation before deciding what can be verified. The initiating CQE and completion of the sanitize operation require different evidence.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-SANITIZE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="25.02">25.02.</span>The NVM Sanitize command follows Base, with §5.12 adding data semantics for the background operation. After success, Block Erase returns vendor-defined values, Crypto Erase indeterminate values, and Overwrite follows its pattern rules; deallocated blocks instead follow deallocated-read rules.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.7; 5.12</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.7; 5.12, printed pages 113,173-175, PDF pages 113,173-175</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>LID81h</td><td>Tracks operation status/progress</td><td>Successful initiation is not operation completion</td></tr><tr><td>Error Information</td><td>The NVM LBA field returns zero during sanitize</td><td>This NVM extension still obeys the Base command allowlist</td></tr><tr><td>Media Verification Read</td><td>PRCHK=000b, STC=0</td><td>Requesting checking gives Invalid Field in Command</td></tr><tr><td>Allocated media</td><td>Return actual data if readable; error if unreadable</td><td>Qualifying reads return Successful Media Verification Read</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="25.03">25.03.</span>In Media Verification, a Read without PI checking can ignore integrity errors when allocated media remains readable and return the specific success status. Repeated reads of one LBA may differ, so ordinary stable-value assumptions do not apply.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-200 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-200"><summary>NVM Figure 200 · Sanitize Operations – Admin Commands Allowed</summary>
<!-- claim:NVMCS13-NVM-FIG-200-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="25.04">25.04.</span>Figure 200, "Sanitize Operations – Admin Commands Allowed": NVM Figure200 adds zero-valued Error Information LBA during sanitize. It is not the Base Feature table with the same number and does not replace the Base permitted-command list.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.12</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12, Figure 200, printed pages 173, PDF pages 173</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-201 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-201"><summary>NVM Figure 201 · Sanitize Operation Types – User Data Values</summary>
<!-- claim:NVMCS13-NVM-FIG-201-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="25.05">25.05.</span>Figure 201, "Sanitize Operation Types – User Data Values": Successful sanitize values on allocated media depend on the method. Deallocated blocks follow deallocated-read rules; no universal all-zero result is implied.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.12</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.12, Figure 201, printed pages 174, PDF pages 174</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-312 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-312"><summary>Base Figure 312 · Sanitize Status Log Page</summary>
<!-- claim:NVMCS13-BASE-FIG-312-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="25.06">25.06.</span>Figure 312, "Sanitize Status Log Page": Sanitize Status supplies operation progress, outcome, initiating command, and state. A successful initiating CQE cannot replace this log.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.13.1.38</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.13.1.38, Figure 312, printed pages 314-319, PDF pages 340-345</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-451 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-451"><summary>Base Figure 451 · Sanitize – Command Dword 10</summary>
<!-- claim:NVMCS13-BASE-FIG-451-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="25.07">25.07.</span>Figure 451, "Sanitize – Command Dword 10": Subsystem Sanitize CDW10 separates method from modifiers. NVM §4.1.7 uses this Base command format.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.26</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 451, printed pages 450-451, PDF pages 476-477</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-452 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-452"><summary>Base Figure 452 · Sanitize – Command Dword 11</summary>
<!-- claim:NVMCS13-BASE-FIG-452-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="25.08">25.08.</span>Figure 452, "Sanitize – Command Dword 11": CDW11 OVRPAT is the Overwrite pattern. Not every SANACT uses it, and it does not define Crypto Erase read values.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.26</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.26, Figure 452, printed pages 451, PDF pages 477</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-alignment"><h2 id="heading-nvmcs-alignment"><span class="section-number">26</span> Alignment, granularity, and performance hints</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="26.01">26.01.</span>Read the fields raw fields into blocks, then evaluate starting alignment and length granularity. Meeting only one can still cause read-modify-write.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-ALIGNMENT -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="26.02">26.02.</span>NPWG/NPWA and NPRG/NPRA describe recommended write and read granularities and alignments; NOWS/NORS describe optimal sizes. These performance hints do not replace atomic boundaries, command hard limits, or format rules.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.2.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, printed pages 122-129, PDF pages 122-129</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>NPWG / NPWA</td><td>Meet both length and start recommendations</td><td>First check NSFEAT.OPTPERF</td></tr><tr><td>NPRG / NPRA / NORS</td><td>Guide read optimization</td><td>First check OPTRPERF</td></tr><tr><td>NPDG / NPDGL</td><td>Alternative deallocate-granularity fields</td><td>Select via OPTPERF; Large fields do not universally add one</td></tr><tr><td>NOIOB / NABO</td><td>Optimal I/O boundary differs from atomic offset</td><td>I/O can be split to satisfy multiple conditions</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="26.03">26.03.</span>With NPWG=8 and NPWA=8, writing LBAs 8..15 meets both. Writing 9..16 also has eight blocks but crosses two units and may require reading old data at both ends.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-145 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-145"><summary>NVM Figure 145 · An example namespace with four NOIOBs</summary>
<!-- claim:NVMCS13-NVM-FIG-145-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="26.04">26.04.</span>Figure 145, "An example namespace with four NOIOBs": The optimal-I/O boundary illustration is independent of atomic boundaries. Splitting crossings can meet recommendations while increasing command count.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.2.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 145, printed pages 124, PDF pages 124</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-146 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-146"><summary>NVM Figure 146 · Example namespace illustrating a potential NABO and NABSN</summary>
<!-- claim:NVMCS13-NVM-FIG-146-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="26.05">26.05.</span>Figure 146, "Example namespace illustrating a potential NABO and NABSN": Mark the atomic offset separately from the namespace origin; not all boundaries necessarily start at LBA0.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.2.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 146, printed pages 124, PDF pages 124</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-147 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-147"><summary>NVM Figure 147 · Example namespace broken down to illustrate potential NPWA and NPWG settings</summary>
<!-- claim:NVMCS13-NVM-FIG-147-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="26.06">26.06.</span>Figure 147, "Example namespace broken down to illustrate potential NPWA and NPWG settings": NPWA governs the start and NPWG the length granularity. The illustrated eight blocks are a size after reading the fields, not raw field value eight.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.2.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 147, printed pages 125, PDF pages 125</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-148 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-148"><summary>NVM Figure 148 · Example namespace broken down to illustrate potential NPRA and NPRG settings</summary>
<!-- claim:NVMCS13-NVM-FIG-148-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="26.07">26.07.</span>Figure 148, "Example namespace broken down to illustrate potential NPRA and NPRG settings": Read alignment and granularity differ: the example uses four-block alignment and eight-block granularity. Short misaligned reads may affect performance.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.2.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 148, printed pages 126, PDF pages 126</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-149 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-149"><summary>NVM Figure 149 · Non-conformant Write Impact</summary>
<!-- claim:NVMCS13-NVM-FIG-149-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="26.08">26.08.</span>Figure 149, "Non-conformant Write Impact": Updating only three blocks of the illustrated eight-block unit requires reading five old prefix/suffix blocks before combining them: a possible read-modify-write cost.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.2.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 149, printed pages 127, PDF pages 127</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-150 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-150"><summary>NVM Figure 150 · Host write I/O command following NPWA and NPWG</summary>
<!-- claim:NVMCS13-NVM-FIG-150-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="26.09">26.09.</span>Figure 150, "Host write I/O command following NPWA and NPWG": The illustrated range satisfies NPWA and NPWG and avoids the example’s edge reads. It does not guarantee that all hardware performs no internal reads.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.2.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 150, printed pages 127, PDF pages 127</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-151 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-151"><summary>NVM Figure 151 · Host write I/O command following NPWG but not NPWA attributes</summary>
<!-- claim:NVMCS13-NVM-FIG-151-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="26.10">26.10.</span>Figure 151, "Host write I/O command following NPWG but not NPWA attributes": A length of exactly one NPWG can still touch two units when misaligned. Checking length modulo NPWG alone is insufficient.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.2.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 151, printed pages 128, PDF pages 128</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-performance-feature"><h2 id="heading-nvmcs-performance-feature"><span class="section-number">27</span> Performance Characteristics attributes</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="27.01">27.01.</span>This Feature reports or manages performance attributes; its standard latency class is not a service guarantee for arbitrary workloads.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-PERFORMANCE-FEATURE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="27.02">27.02.</span>FID 1Ch selects attributes through ATTRI: 00h is read-only standard performance, C0h a read-only identifier list, and C1h..FFh vendor attributes. Current, Default, and Saved are distinct views; RVSPA removes a selected vendor attribute’s saved value.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, printed pages 69-73, PDF pages 69-73</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>R4KARL</td><td>Average-latency range for standardized 4 KiB random reads</td><td>00h means unreported</td></tr><tr><td>MSVSPA / USVSPA</td><td>Saveable capacity / unused capacity</td><td>Indices can be noncontiguous</td></tr><tr><td>PAID / ATTRL</td><td>128-bit identifier / valid vendor bytes</td><td>ATTRL is at most FE0h</td></tr><tr><td>RVSPA</td><td>Delete the saved value to return to default</td><td>The data-buffer contents are unused</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="27.03">27.03.</span>R4KARL=0Eh means 50 μs ≤ average latency &lt;100 μs, not 14 μs. When reading the C0h list, match ATTRTYP with Get SEL and use PAID to interpret vendor payloads.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SEL</dt><dd>Select, the Get Features field choosing current, default, saved, or supported-capabilities view.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-102 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-102"><summary>NVM Figure 102 · Performance Characteristics – Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-102-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="27.04">27.04.</span>Figure 102, "Performance Characteristics – Command Dword 11": ATTRI low8 selects standard, list, or vendor attributes. RVSPA bit8 deletes a saved vendor value, not the entire Feature.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, Figure 102, printed pages 69, PDF pages 69</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-103 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-103"><summary>NVM Figure 103 · Performance Characteristics – Standard Performance Attribute</summary>
<!-- claim:NVMCS13-NVM-FIG-103-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="27.05">27.05.</span>Figure 103, "Performance Characteristics – Standard Performance Attribute": R4KARL is a latency bucket rather than a direct time value. 0Eh is the half-open 50–100 μs interval, and 00h means unreported.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, Figure 103, printed pages 71, PDF pages 71</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-104 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-104"><summary>NVM Figure 104 · Performance Characteristics – Performance Attribute Identifier List</summary>
<!-- claim:NVMCS13-NVM-FIG-104-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="27.06">27.06.</span>Figure 104, "Performance Characteristics – Performance Attribute Identifier List": Match ATTRTYP to Get SEL. Use MSVSPA/USVSPA for saved slots and each 128-bit PAID to identify payloads; slots need not be contiguous.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SEL</dt><dd>Select, the Get Features field choosing current, default, saved, or supported-capabilities view.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, Figure 104, printed pages 72, PDF pages 72</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-105 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-105"><summary>NVM Figure 105 · Performance Characteristics – Vendor Specific Performance Attribute</summary>
<!-- claim:NVMCS13-NVM-FIG-105-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="27.07">27.07.</span>Figure 105, "Performance Characteristics – Vendor Specific Performance Attribute": PAID identifies the vendor payload definition and ATTRL bounds valid VS bytes, at most FE0h. Do not invent a standard reading the fields for an unknown PAID.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.8, Figure 105, printed pages 73, PDF pages 73</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-rate-config"><h2 id="heading-nvmcs-rate-config"><span class="section-number">28</span> Rate Limiting configuration fields</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="28.01">28.01.</span>Obtain supported targets from LID 28h, then check HLS/SLS and the soft-controller count. Record requested limits separately from attainable device capabilities.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-RATE-CONFIG -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="28.02">28.02.</span>FID 28h selects a target with TGT/TID and uses a 1024-byte buffer for enablement, mode, bandwidth, IOPS, and write/read ratios. TGT=0 selects a controller; an Admin controller or reserved ID is invalid. This Feature must be saveable.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>IOPS</dt><dd>Input/Output Operations Per Second; an operation rate, distinct from byte throughput.</dd></div><div><dt>TGT</dt><dd>Target; Selects the rate-limit target type.</dd></div><div><dt>TID</dt><dd>Target Identifier; Identifies an entity of the selected target type.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.9; 4.1.5.4; 5.10</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.9; 4.1.5.4; 5.10, printed pages 73-75,106,165-168, PDF pages 73-75,106,165-168</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>TGT / TID</td><td>CDW11[23:16] / [15:0]</td><td>TGT=0 is the standard controller target</td></tr><tr><td>RLC</td><td>RLE bit15; RLM=0 Hard, 1 Soft</td><td>Soft support requires Hard support</td></tr><tr><td>BWSF</td><td>0/1/2 = 1/10/100 MiB/s; 3/4/5 = 1/10/100 GiB/s</td><td>Multiply the value by the scale</td></tr><tr><td>WRIOPSR / WRBWR</td><td>Write numerator divided by read denominator</td><td>Every ratio component byte must be nonzero</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>WRIOPSR</dt><dd>Write-to-Read IOPS Ratio; The write-to-read operation-count weight.</dd></div><div><dt>WRBWR</dt><dd>Write-to-Read Bandwidth Ratio; The write-to-read bandwidth weight.</dd></div><div><dt>BWSF</dt><dd>Bandwidth Scale Factor; multiply by the bandwidth value in MiB/s or GiB/s.</dd></div><div><dt>TGT</dt><dd>Target; Selects the rate-limit target type.</dd></div><div><dt>TID</dt><dd>Target Identifier; Identifies an entity of the selected target type.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="28.03">28.03.</span>BWSF=1 and TBWV=50 specify 500 MiB/s. WBWV/WIOPS govern writes, while total consumption is weighted by WRBWR/WRIOPSR; total limits are not simply read limits.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>WRIOPSR</dt><dd>Write-to-Read IOPS Ratio; The write-to-read operation-count weight.</dd></div><div><dt>WIOPS</dt><dd>Write IOPS; The write operation-rate value.</dd></div><div><dt>WRBWR</dt><dd>Write-to-Read Bandwidth Ratio; The write-to-read bandwidth weight.</dd></div><div><dt>BWSF</dt><dd>Bandwidth Scale Factor; multiply by the bandwidth value in MiB/s or GiB/s.</dd></div><div><dt>TBWV</dt><dd>Total Bandwidth Value; Total bandwidth value, scaled by BWSF.</dd></div><div><dt>WBWV</dt><dd>Write Bandwidth Value; Write bandwidth value, scaled by BWSF.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-106 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-106"><summary>NVM Figure 106 · Rate Limits – Command Dword 11</summary>
<!-- claim:NVMCS13-NVM-FIG-106-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="28.04">28.04.</span>Figure 106, "Rate Limits – Command Dword 11": Interpret TID after TGT. TGT=0 uses a controller ID and excludes Admin controllers, invalid IDs, and FFFDh..FFFFh.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.9</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.9, Figure 106, printed pages 73, PDF pages 73</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-107 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-107"><summary>NVM Figure 107 · Rate Limiting – Data Buffer</summary>
<!-- claim:NVMCS13-NVM-FIG-107-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="28.05">28.05.</span>Figure 107, "Rate Limiting – Data Buffer": The 1024-byte configuration separates enable/mode, two bandwidth limits, two IOPS limits, and two write/read ratios. Calculate weighted total and write-only consumption separately.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>IOPS</dt><dd>Input/Output Operations Per Second; an operation rate, distinct from byte throughput.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.9</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.9, Figure 107, printed pages 74-75, PDF pages 74-75</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>TIOPS</dt><dd>Total IOPS; The total I/O operation-rate value.</dd></div><div><dt>WIOPS</dt><dd>Write IOPS; The write operation-rate value.</dd></div><div><dt>TBWV</dt><dd>Total Bandwidth Value; Total bandwidth value, scaled by BWSF.</dd></div><div><dt>WBWV</dt><dd>Write Bandwidth Value; Write bandwidth value, scaled by BWSF.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-108 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-108"><summary>NVM Figure 108 · Bandwidth Scale Factors</summary>
<!-- claim:NVMCS13-NVM-FIG-108-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="28.06">28.06.</span>Figure 108, "Bandwidth Scale Factors": The shared scale table applies to configured, maximum, and available bandwidth. Values 0..2 are MiB/s scales and 3..5 GiB/s scales.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.3.9</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.3.9, Figure 108, printed pages 75, PDF pages 75</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-rate-modes"><h2 id="heading-nvmcs-rate-modes"><span class="section-number">29</span> Hard/Soft modes and token-bucket examples</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="29.01">29.01.</span>Interpret results using capability, configured limits, and actual demand. A configured ratio does not force a fixed throughput ratio at every instant; internal resources and workload still matter.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-RATE-MODES -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="29.02">29.02.</span>Hard Limit sets a ceiling; Soft Limit can use unused bandwidth/IOPS. Resource shortfalls are shared proportionally to configured limits. Appendix A illustrates multiple token buckets without requiring one identical controller implementation.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.10.1-5.10.2; Appendix A</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.10.1-5.10.2; Appendix A, printed pages 166-168,176-177, PDF pages 166-168,176-177</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Hard</td><td>Proportional sharing under demand and resource shortage</td><td>A configured ceiling is not a performance floor</td></tr><tr><td>Soft</td><td>May consume unused capacity</td><td>Multiple soft targets share it in proportion to limits</td></tr><tr><td>Write tokens</td><td>Total bytes × WRBWR; write bytes; total IOPS × WRIOPSR; one write IOPS</td><td>Check each of four buckets</td></tr><tr><td>Read tokens</td><td>Total bytes and one total IOPS</td><td>Does not consume write-only buckets</td></tr></tbody></table></div>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="29.03">29.03.</span>Teaching setup: a 4 KiB Write with WRBWR=2 and WRIOPSR=3 consumes 8 KiB total-bandwidth, 4 KiB write-bandwidth, three total-IOPS, and one write-IOPS token. A 4 KiB Read consumes only 4 KiB total-bandwidth and one total-IOPS token.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-202 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-202"><summary>NVM Figure 202 · Example Token Bucket</summary>
<!-- claim:NVMCS13-NVM-FIG-202-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="29.04">29.04.</span>Figure 202, "Example Token Bucket": Insufficient tokens make commands wait. Partial processing is possible, but CQE publication follows complete processing. This is an informative implementation example, not the only scheduler.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>token bucket</dt><dd>A rate-control model that accumulates credits and consumes them when admitting work.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §Appendix A</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §Appendix A, Figure 202, printed pages 176, PDF pages 176</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-rate-graph"><h2 id="heading-nvmcs-rate-graph"><span class="section-number">30</span> The Rate Limiting log is a capability graph</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.01">30.01.</span>Validate structure bounds before analyzing bandwidth bottlenecks. Port capability differs from shared Endurance Group capability; do not simply add all reported numbers.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Endurance Group</dt><dd>Endurance Group, a group of NVM resources for isolating and reporting endurance-related state.</dd></div></dl>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-RATE-GRAPH -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.02">30.02.</span>LID 28h links ports, controllers, and storage-medium access descriptors using dword offsets from the log start. Descriptors may be shared rather than forming one fixed-order array. After chunked reads, reread GC and recollect if it changed.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>GC</dt><dd>32-bit Generation Count in the Rate Limiting log, used for chunk consistency.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.4.8; 5.10.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8; 5.10.3, printed pages 79-83,168-172, PDF pages 79-83,168-172</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>LPL / offsets</td><td>Lengths and pointers use dword units</td><td>Byte offset = dword offset ×4</td></tr><tr><td>NP / NC / NST</td><td>All are zero-based counts</td><td>NNSMAD is an actual count</td></tr><tr><td>SC / SI</td><td>Subsystem/domain/EG/namespace and its ID</td><td>Interpret scope and avoid double-counting shared nodes</td></tr><tr><td>RLMA</td><td>Maximum read/write bandwidth/IOPS</td><td>Relevant size/queue-depth workload conditions apply</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>NNSMAD</dt><dd>Actual number of Non-Volatile Storage Medium Access Descriptors; zero means no downstream descriptors.</dd></div><div><dt>RLMA</dt><dd>Rate Limiting Maximum Access; maximum capability for the described port/controller/storage access, not current traffic.</dd></div><div><dt>LPL</dt><dd>Rate Limiting Log Page Length in dwords; multiply by four and validate bounds before reading bytes.</dd></div><div><dt>NC</dt><dd>Number of Controllers; The 0-based controller count in the Rate Limiting log.</dd></div><div><dt>NP</dt><dd>Number of Ports; The 0-based port count in the Rate Limiting log.</dd></div><div><dt>SI</dt><dd>Scope Identifier: identifies the entity in the scope selected by SC.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="30.03">30.03.</span>Two PCIe ports may share one Endurance Group. If controller 0 consumes all EG bandwidth, the extra port does not create more media bandwidth for controller 1. Both controllers may reference one descriptor for identical EG access capabilities.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Endurance Group</dt><dd>Endurance Group, a group of NVM resources for isolating and reporting endurance-related state.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-117 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-117"><summary>NVM Figure 117 · Rate Limiting Log Page</summary>
<!-- claim:NVMCS13-NVM-FIG-117-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.04">30.04.</span>Figure 117, "Rate Limiting Log Page": NP/NST are zero-based, LPL is dwords, and port pointers are dword offsets from the log start. Recheck GC after collecting the log.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>LPL</dt><dd>Rate Limiting Log Page Length in dwords; multiply by four and validate bounds before reading bytes.</dd></div><div><dt>GC</dt><dd>32-bit Generation Count in the Rate Limiting log, used for chunk consistency.</dd></div><div><dt>NP</dt><dd>Number of Ports; The 0-based port count in the Rate Limiting log.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.4.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8, Figure 117, printed pages 80, PDF pages 80</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-118 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-118"><summary>NVM Figure 118 · Rate Limiting Port Descriptor</summary>
<!-- claim:NVMCS13-NVM-FIG-118-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.05">30.05.</span>Figure 118, "Rate Limiting Port Descriptor": Available fields in a port descriptor report unassigned capacity, distinct from RLMA maximums. Controller-list offsets remain relative to the whole log.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>RLMA</dt><dd>Rate Limiting Maximum Access; maximum capability for the described port/controller/storage access, not current traffic.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.4.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8, Figure 118, printed pages 80-81, PDF pages 80-81</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NC</dt><dd>Number of Controllers; The 0-based controller count in the Rate Limiting log.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-119 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-119"><summary>NVM Figure 119 · Rate Limiting Controller Descriptor</summary>
<!-- claim:NVMCS13-NVM-FIG-119-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.06">30.06.</span>Figure 119, "Rate Limiting Controller Descriptor": A controller descriptor gives the actual access-descriptor count in NNSMAD. It does not use NP/NC add-one reading the fields.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NNSMAD</dt><dd>Actual number of Non-Volatile Storage Medium Access Descriptors; zero means no downstream descriptors.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.4.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8, Figure 119, printed pages 81, PDF pages 81</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-120 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-120"><summary>NVM Figure 120 · Non-Volatile Storage Medium Access Descriptor</summary>
<!-- claim:NVMCS13-NVM-FIG-120-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.07">30.07.</span>Figure 120, "Non-Volatile Storage Medium Access Descriptor": Select scope with SC before interpreting SI and nested access lists. The SI prose still mentions NSET and misplaced example bytes; SC and the tabulated bytes7:4 provide the field location.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SI</dt><dd>Scope Identifier: identifies the entity in the scope selected by SC.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.4.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8, Figure 120, printed pages 81-82, PDF pages 81-82</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-121 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-121"><summary>NVM Figure 121 · Rate Limiting Maximum Access Descriptor</summary>
<!-- claim:NVMCS13-NVM-FIG-121-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.08">30.08.</span>Figure 121, "Rate Limiting Maximum Access Descriptor": Scale bandwidth using MBSF. The four maximums depend on workload size and queue depth and are not minimum guarantees for arbitrary workloads.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.4.8</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.8, Figure 121, printed pages 82-83, PDF pages 82-83</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-195 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-195"><summary>NVM Figure 195 · Port Graph Example</summary>
<!-- claim:NVMCS13-NVM-FIG-195-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.09">30.09.</span>Figure 195, "Port Graph Example": This is a graph with shared nodes, not a tree. Two controllers may reference one EG without doubling its shared media capability.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.10.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.10.3, Figure 195, printed pages 169, PDF pages 169</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-196 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-196"><summary>NVM Figure 196 · Rate Limiting Log Page Example</summary>
<!-- claim:NVMCS13-NVM-FIG-196-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.10">30.10.</span>Figure 196, "Rate Limiting Log Page Example": Descriptors connect through dword offsets from the log start. For example, offset=299 means 299×4=1196 bytes; multiple connections can reference a shared descriptor.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.10.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.10.3, Figure 196, printed pages 169-170, PDF pages 169-170</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-197 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-197"><summary>NVM Figure 197 · Example Dual Port PCIe NVMe SSD</summary>
<!-- claim:NVMCS13-NVM-FIG-197-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.11">30.11.</span>Figure 197, "Example Dual Port PCIe NVMe SSD": Two ports do not duplicate the media capability of their shared EG; analyze contention at the shared storage bottleneck.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVMe</dt><dd>Non-Volatile Memory Express, the specification family for a host interface to a non-volatile-memory subsystem.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.10.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.10.3, Figure 197, printed pages 171, PDF pages 171</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-198 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-198"><summary>NVM Figure 198 · Dual Port PCIe NVMe SSD Rate Limiting Log Page Example</summary>
<!-- claim:NVMCS13-NVM-FIG-198-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="30.12">30.12.</span>Figure 198, "Dual Port PCIe NVMe SSD Rate Limiting Log Page Example": Preserve the two-port/shared-storage relationship. The example gives LPL=570 dwords while listing structures beyond 2280 bytes, so it is not a valid input fixture.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.10.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.10.3, Figure 198, printed pages 171-172, PDF pages 171-172</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-fdp"><h2 id="heading-nvmcs-fdp"><span class="section-number">31</span> FDP: placement, RUHs, and observable data</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="31.01">31.01.</span>Creation establishes placement relationships; handle status describes operation, and statistics/events explain later media movement. These evidence types are not interchangeable.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-FDP -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="31.02">31.02.</span>FDP namespace placement handles map to Reclaim Unit Handles. Namespaces sharing a RUH must use the same Format Index, and host-specified handle lists cannot repeat RUHIDs. RUH Status descriptors sort first by Placement Handle, then by Reclaim Group Identifier.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Reclaim Group</dt><dd>Reclaim Group, a set of non-volatile storage resources with shared reclamation behavior.</dd></div><div><dt>Reclaim Unit</dt><dd>Reclaim Unit, a smaller management granularity used when a controller reclaims media.</dd></div><div><dt>FDP</dt><dd>Flexible Data Placement, a capability connecting data-placement hints with media-reclamation management.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.2.1; 4.1.4.6-4.1.4.7; 4.1.6.3</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.2.1; 4.1.4.6-4.1.4.7; 4.1.6.3, printed pages 26,79,110-113, PDF pages 26,79,110-113</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>NPHNDLS</td><td>At most 128 and no more than the configuration RUH count</td><td>Zero invokes controller-selection and sharing rules</td></tr><tr><td>EARUTR / RUAMW</td><td>Estimated remaining seconds / writable logical blocks</td><td>EARUTR=0 means unreported; not a lifetime guarantee</td></tr><tr><td>LID 22h</td><td>HBMW/MBMW include the specified NVM write-class commands</td><td>Includes Copy destination, Zeroes, and Uncorrectable</td></tr><tr><td>LID 23h event 0h</td><td>LBAV governs LBA validity</td><td>NLBAM=FFFFh means at least FFFFh</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>NPHNDLS</dt><dd>Number of Placement Handles, the entry count for the Placement Handle List in the NVM create payload, with a maximum of 128.</dd></div><div><dt>LBAV</dt><dd>LBA Valid; Indicates whether the reported LBA is valid.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="31.03">31.03.</span>If two namespaces share RUH 5 and one uses FIDX=2, creating the other with FIDX=3 violates the shared-RUH Format Index rule even if both have 4 KiB data blocks.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-021 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-021"><summary>NVM Figure 21 · Reclaim Unit Handle Status Descriptor</summary>
<!-- claim:NVMCS13-NVM-FIG-021-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="31.04">31.04.</span>Figure 21, "Reclaim Unit Handle Status Descriptor": Use PID for Placement Handle/Reclaim Group, then interpret RUHID, estimated time remaining, and writable blocks. RUAMW is not a fixed nominal RU size.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>Reclaim Group</dt><dd>Reclaim Group, a set of non-volatile storage resources with shared reclamation behavior.</dd></div><div><dt>Reclaim Unit</dt><dd>Reclaim Unit, a smaller management granularity used when a controller reclaims media.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §3.2.1.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.2.1.1, Figure 21, printed pages 26, PDF pages 26</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-116 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-116"><summary>NVM Figure 116 · Media Reallocated - Event Type Specific Data Structure</summary>
<!-- claim:NVMCS13-NVM-FIG-116-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="31.05">31.05.</span>Figure 116, "Media Reallocated - Event Type Specific Data Structure": Validate LBAV before using LBA. NLBAM=0 means unreported and FFFFh means at least that many, not exactly 65535 moved blocks.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>LBAV</dt><dd>LBA Valid; Indicates whether the reported LBA is valid.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.4.7</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.4.7, Figure 116, printed pages 79, PDF pages 79</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-streams"><h2 id="heading-nvmcs-streams"><span class="section-number">32</span> NVM units and priorities for Streams</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="32.01">32.01.</span>Use two size levels: Stream Write Size and the larger stream granularity. They may be integer multiples of namespace hints, but this is not guaranteed for every namespace.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-STREAMS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="32.02">32.02.</span>NVM Stream Write Size is expressed in logical blocks. Stream granularity length is SGS multiplied by the SWS value after reading the fields. When using Streams, hosts should follow SGS/SWS guidance for writes/deallocation and reconcile namespace hints.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>SWS</dt><dd>Stream Write Size; the NVM command-set unit is logical blocks.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.2.2.3; 5.13</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2.3; 5.13, printed pages 128-129,175, PDF pages 128-129,175</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>SWS</td><td>Recommended write size in blocks</td><td>Should be a multiple of NPWG</td></tr><tr><td>SGS × SWS</td><td>Length of the stream granularity</td><td>Guides stream deallocate alignment/length</td></tr><tr><td>Priority</td><td>Prefer Streams attributes when Streams are used</td><td>Otherwise use namespace hints</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>SWS</dt><dd>Stream Write Size; the NVM command-set unit is logical blocks.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="32.03">32.03.</span>Reading the fields gives SWS=8 blocks and SGS=4 give a 32-block stream granularity. An eight-block Write can meet SWS, while deallocating one full granularity unit uses 32 blocks.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-152 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-152"><summary>NVM Figure 152 · Two streams composed of SGS and SWS</summary>
<!-- claim:NVMCS13-NVM-FIG-152-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="32.04">32.04.</span>Figure 152, "Two streams composed of SGS and SWS": A stream granularity contains SGS units of SWS. Coordinate writes with SWS and stream deallocation with the larger granularity.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.2.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.2.2, Figure 152, printed pages 128, PDF pages 128</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-712 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-712"><summary>Base Figure 712 · Streams Directive – Return Parameters Data Structure</summary>
<!-- claim:NVMCS13-BASE-FIG-712-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="32.05">32.05.</span>Figure 712, "Streams Directive – Return Parameters Data Structure": SWS/SGS in Streams Return Parameters describe write size and granularity. NVM §5.13 defines the command-set unit of SWS as logical blocks.</p><details class="source-note"><summary>Sources: Base 2.4 §8.1.9.3.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §8.1.9.3.1.1, Figure 712, printed pages 624-625, PDF pages 650-651</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-ana-reservations"><h2 id="heading-nvmcs-ana-reservations"><span class="section-number">33</span> NVM behavior under ANA and Reservations</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="33.01">33.01.</span>Check namespace access state separately from access permissions; path state does not establish reservation ownership.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-ANA-RESERVATIONS -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="33.02">33.02.</span>ANA state can restrict specified Features and alter capacity reporting. Reservations determine command permissions from reservation type, holder, and registration state. These shared-namespace capabilities can apply in PCIe multi-controller configurations.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.1; 5.11</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.1; 5.11, printed pages 119,172-173, PDF pages 119,172-173</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>ANA Identify</td><td>NUSE/NVMCAP return zero in Inaccessible/Persistent Loss</td><td>This does not mean media was erased</td></tr><tr><td>ANA FID05h</td><td>Get is restricted in Inaccessible/Persistent Loss/Change</td><td>Use the corresponding ANA status</td></tr><tr><td>Write Exclusive / Exclusive Access</td><td>For nonholders, the former allows read-like commands; the latter conflicts with read-like and write-like commands</td><td>Nonholder write-like commands conflict for both</td></tr><tr><td>Registrants Only / All Registrants</td><td>Write Exclusive variants allow reads by anyone and writes by registrants; Exclusive Access variants allow reads/writes only by registrants</td><td>Copy checks each source as read and its destination as write</td></tr><tr><td>Reservations</td><td>Check the matrix for read-like/write-like commands</td><td>Holder, registrant, and type all matter</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>NVMCAP</dt><dd>NVM Capacity, measured in bytes; not directly comparable to NSZE/NCAP logical-block counts.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="33.03">33.03.</span>Two PCIe controllers of one SSD may share a namespace. Controller 1 can have an accessible path yet be unable to Write due to reservation type and its registration state; Read permissions require a separate matrix lookup.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-141 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-141"><summary>NVM Figure 141 · ANA effects on NVM Command Set Command Processing</summary>
<!-- claim:NVMCS13-NVM-FIG-141-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="33.04">33.04.</span>Figure 141, "ANA effects on NVM Command Set Command Processing": Cross-reference command and ANA state. FID05h Get/Set restrictions differ; Identify capacity zeroing describes reported values only.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.1, Figure 141, printed pages 119, PDF pages 119</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-199 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-199"><summary>NVM Figure 199 · Command Behavior in the Presence of a Reservation</summary>
<!-- claim:NVMCS13-NVM-FIG-199-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="33.05">33.05.</span>Figure 199, "Command Behavior in the Presence of a Reservation": Classify read-like/write-like commands, then apply holder/registration state and reservation type. Nonholders do not all have identical permissions.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.11</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.11, Figure 199, printed pages 173, PDF pages 173</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-key-per-io"><h2 id="heading-nvmcs-key-per-io"><span class="section-number">34</span> NVM alignment constraints for Key Per I/O</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="34.01">34.01.</span>Determine applicability from KPIOCAP and namespace status before reading the fields the CETYPE/CEV command extension. This NVM supplement does not fully define key creation or management.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-KEY-PER-IO -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="34.02">34.02.</span>The NVM Key Per I/O extension requires key-tagged commands to meet KPIODAAG starting-LBA alignment and length granularity; violations return Invalid Field in Command. Capability, namespace enablement, and key management are separate layers.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>KPIODAAG</dt><dd>Key Per I/O Data Access Alignment and Granularity, in zero-based blocks.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.5; 4.1.5</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.5; 4.1.5, printed pages 91-92,105,160, PDF pages 91-92,105,160</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>KPIOCAP</td><td>Support and subsystem/namespace scope</td><td>Do not rely on an enable bit alone</td></tr><tr><td>KPIOSNS / KPIOENS</td><td>Namespace support / enablement</td><td>Enable must be zero without support</td></tr><tr><td>KPIODAAG</td><td>Zero-based logical-block granularity</td><td>Both start and length must conform</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>KPIODAAG</dt><dd>Key Per I/O Data Access Alignment and Granularity, in zero-based blocks.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="34.03">34.03.</span>Raw KPIODAAG=7 represents eight-block granularity. SLBA=16 and length=8 fit; SLBA=17 or length=7 do not, even when all other PI fields are correct.</p></aside>
</section>
<section class="lesson" id="module-nvmcs-migration-queue"><h2 id="heading-nvmcs-migration-queue"><span class="section-number">35</span> LBA Migration Queue and change tracking</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="35.01">35.01.</span>The queue records changed ranges and sequence markers rather than complete new data. The host still retrieves data with appropriate I/O and handles the logging-stop boundary caused by a full queue.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-MIGRATION-QUEUE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="35.02">35.02.</span>After Track Send enables an LBA Migration Queue, the controller may aggregate logical-block modifications or deallocations. Entries are posted only after the reported effects take place and may precede the command CQE; queue entry and I/O completion are distinct milestones.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §4.1.8; 5.7</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.8; 5.7, printed pages 113-114,162-164, PDF pages 113-114,162-164</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>LBACIR</td><td>00: range; 01: whole namespace; 10: no range</td><td>Determine field validity first</td></tr><tr><td>ESA</td><td>001 start/resume; 010 stop; 011 suspend; 111 full</td><td>Full means logging stopped</td></tr><tr><td>DLBA / CDQP</td><td>Deallocation flag / entry phase</td><td>DLBA=0 may still describe a deallocation-related change</td></tr><tr><td>RALBAS</td><td>ATYPE02h covers changes during the start command when supported</td><td>Start/stop markers need not precede Track Send CQE</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>LBACIR</dt><dd>LBA Change Indication Range; selects explicit range, whole namespace, or no-range entry interpretation.</dd></div><div><dt>CDQP</dt><dd>Controller Data Queue Phase; Lets the host identify a new entry at a queue location.</dd></div><div><dt>DLBA</dt><dd>Deallocated LBA; An entry flag indicating deallocation.</dd></div><div><dt>ESA</dt><dd>Entry Sequence Attribute, marking start/stop/suspend/full in the LBA Migration Queue.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="35.03">35.03.</span>Three sequential Writes may become one range entry, so entry count is not write-command count. After ESA=111b, the host cannot assume subsequent changes continue to be logged.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>ESA</dt><dd>Entry Sequence Attribute, marking start/stop/suspend/full in the LBA Migration Queue.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-194 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-194"><summary>NVM Figure 194 · LBA Migration Queue Entry Type 0</summary>
<!-- claim:NVMCS13-NVM-FIG-194-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="35.04">35.04.</span>Figure 194, "LBA Migration Queue Entry Type 0": The final byte of a 32-byte entry carries range applicability, deallocation, sequence, and phase. Check LBACIR before using SLBA/NLB; NLB is zero-based.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>LBACIR</dt><dd>LBA Change Indication Range; selects explicit range, whole namespace, or no-range entry interpretation.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.7</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.7, Figure 194, printed pages 163-164, PDF pages 163-164</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>CDQP</dt><dd>Controller Data Queue Phase; Lets the host identify a new entry at a queue location.</dd></div><div><dt>DLBA</dt><dd>Deallocated LBA; An entry flag indicating deallocation.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-BASE-FIG-561 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-561"><summary>Base Figure 561 · Track Send – Command Dword 10</summary>
<!-- claim:NVMCS13-BASE-FIG-561-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="35.05">35.05.</span>Figure 561, "Track Send – Command Dword 10": Track Send CDW10 selects a management operation before MOS is interpreted. Log User Data Changes tracks changes to NVM data.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.32</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.32, Figure 561, printed pages 523, PDF pages 549</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-562 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-562"><summary>Base Figure 562 · Log User Data Changes – Management Operation Specific Field</summary>
<!-- claim:NVMCS13-BASE-FIG-562-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="35.06">35.06.</span>Figure 562, "Log User Data Changes – Management Operation Specific Field": LACT controls starting/stopping user-data change logging and must be combined with CDQID for a created LBA Migration Queue.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.32.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.32.1.1, Figure 562, printed pages 523, PDF pages 549</p></details>

</details>
<!-- figure-table:NVMCS13-BASE-FIG-563 -->
<details class="field-note" id="figure-NVMCS13-BASE-FIG-563"><summary>Base Figure 563 · Log User Data Changes – Command Dword 11</summary>
<!-- claim:NVMCS13-BASE-FIG-563-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="35.07">35.07.</span>Figure 563, "Log User Data Changes – Command Dword 11": CDQID identifies the controller data queue, not NSID or SQID, selecting the destination for change records.</p><details class="source-note"><summary>Sources: Base 2.4 §5.2.32.1.1</summary><p>Source: NVME-BASE-2.4, Rev. 2.4, §5.2.32.1.1, Figure 563, printed pages 523, PDF pages 549</p></details>

</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-export-template"><h2 id="heading-nvmcs-export-template"><span class="section-number">36</span> Memory-based resource export template</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.01">36.01.</span>The template compatibility interface and underlying device capabilities are separate layers. Check namespace-format compatibility, then configure limits no greater than underlying capabilities; do not advertise capabilities the template does not permit.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-EXPORT-TEMPLATE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.02">36.02.</span>The optional Reference Exported NVM Subsystem Template is memory-based and permits one controller (ID 0h) and one namespace (ID 1h). Creation requires TR=1. Configuration state is set once in one command; repeated setting returns Command Sequence Error.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.4.1-5.4.1.1</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.4.1-5.4.1.1, printed pages 152-159, PDF pages 152-159</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Identity and version</td><td>CAP.CSS=1, VS=020300h; NVM VER=010200h</td><td>The template fixes Base 2.3/NVM 1.2; the enclosing PDF revision does not upgrade it</td></tr><tr><td>Controller limits</td><td>MDTS, RAB, NCQS, NSQS, MQES, AWUN/AWUPF are bounded by underlying support</td><td>NCQS/NSQS are zero-based</td></tr><tr><td>Namespace compatibility</td><td>LBAF0 must match underlying LBADS/MS, with MS=0; DPS/KPIOENS/CWP must be zero</td><td>The controller handles Format Index remapping</td></tr><tr><td>Observable defaults</td><td>Error entries and SMART are zero; firmware active slot is 1</td><td>Support lists, Feature defaults, and Identify exceptions have fixed rules</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>MQES</dt><dd>Maximum Queue Entries Supported; The maximum queue-entry count, using 0-based encoding.</dd></div><div><dt>NCQS</dt><dd>Number of I/O Completion Queues Supported; The supported I/O CQ count, using 0-based encoding.</dd></div><div><dt>NSQS</dt><dd>Number of I/O Submission Queues Supported; The supported I/O SQ count, using 0-based encoding.</dd></div><div><dt>CAP</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="36.03">36.03.</span>Underlying NCQS=7 supports eight queues; configured NCQS=3 permits four queues, not three. A zero namespace NGUID requires a valid NUUID.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>NGUID</dt><dd>Namespace Globally Unique Identifier, a 128-bit global identifier for a namespace.</dd></div><div><dt>NCQS</dt><dd>Number of I/O Completion Queues Supported; The supported I/O CQ count, using 0-based encoding.</dd></div></dl></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-183 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-183"><summary>NVM Figure 183 · Reference Exported Configuration State</summary>
<!-- claim:NVMCS13-NVM-FIG-183-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.04">36.04.</span>Figure 183, "Reference Exported Configuration State": Separate the fixed 364-byte controller configuration from the 48-byte namespace configuration: 412 bytes total, set once in one command.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 183, printed pages 153, PDF pages 153</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>RENSCS / RECCS</dt><dd>Reference Exported Controller/Namespace Configuration State, 364/48 bytes respectively.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-184 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-184"><summary>NVM Figure 184 · Reference Controller Capabilities Register Values</summary>
<!-- claim:NVMCS13-NVM-FIG-184-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.05">36.05.</span>Figure 184, "Reference Controller Capabilities Register Values": Unlisted CAP bits are zero. CSS indicates NVM only, TO=FFh means 127.5 seconds, queues must be physically contiguous, and MQES is bounded by the underlying controller. The figure labels the contiguous-queue field CQE.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>MQES</dt><dd>Maximum Queue Entries Supported; The maximum queue-entry count, using 0-based encoding.</dd></div><div><dt>CAP</dt><dd>Controller Capabilities, the controller property at offset 00h that reports queue, page-size, timeout, and other capabilities.</dd></div><div><dt>TO</dt><dd>CAP Timeout in 500 ms units; FFh means 127.5 seconds.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 184, printed pages 153, PDF pages 153</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>TO</dt><dd>CAP Timeout in 500 ms units; FFh means 127.5 seconds.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-185 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-185"><summary>NVM Figure 185 · Reference Version Register Values</summary>
<!-- claim:NVMCS13-NVM-FIG-185-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.06">36.06.</span>Figure 185, "Reference Version Register Values": The template fixes VS=020300h, meaning 2.3.0; do not change it to 2.4 because that is the supplied Base revision.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 185, printed pages 153, PDF pages 153</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-186 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-186"><summary>NVM Figure 186 · Reference Firmware Slot Information Log Page</summary>
<!-- claim:NVMCS13-NVM-FIG-186-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.07">36.07.</span>Figure 186, "Reference Firmware Slot Information Log Page": The active firmware slot is fixed to 1. Other firmware-log values follow the zeroing rule and the configuration-state FR exception.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>FR</dt><dd>Firmware Revision, the eight-byte ASCII Identify Controller field reporting the active firmware revision.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 186, printed pages 154, PDF pages 154</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>AFI</dt><dd>Active Firmware Info, the LID 03h byte containing the current active slot and the slot scheduled for the next reset.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-187 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-187"><summary>NVM Figure 187 · Reference Feature Default Values</summary>
<!-- claim:NVMCS13-NVM-FIG-187-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.08">36.08.</span>Figure 187, "Reference Feature Default Values": Composite over/under thresholds default to FFFFh/0. IV=0 has CD=1, other vectors CD=0. Number of Queues depends on requested and allocated counts, not a fixed zero.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>IV</dt><dd>Interrupt Vector, the vector number assigned to a Completion Queue.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 187, printed pages 155, PDF pages 155</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>TMPSEL</dt><dd>Temperature Sensor Select, the field choosing Composite Temperature or sensor 1 through 8.</dd></div><div><dt>THSEL</dt><dd>Threshold Type Select, choosing an over-temperature or under-temperature threshold.</dd></div><div><dt>TMPTH</dt><dd>Temperature Threshold, a 16-bit threshold value in Kelvin.</dd></div><div><dt>NSQS</dt><dd>Number of I/O Submission Queues Supported; The supported I/O SQ count, using 0-based encoding.</dd></div><div><dt>IV</dt><dd>Interrupt Vector, the vector number assigned to a Completion Queue.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-188 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-188"><summary>NVM Figure 188 · Reference Identify Controller or Namespace Data Structures</summary>
<!-- claim:NVMCS13-NVM-FIG-188-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.09">36.09.</span>Figure 188, "Reference Identify Controller or Namespace Data Structures": Identify permits the listed exceptions: NCAP=NSZE, SQES=66h for 64-byte SQEs, CQES=44h for 16-byte CQEs, and NVM VER=1.2.0 in CNS06h.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CQES</dt><dd>Completion Queue Entry Size; Encodes minimum and maximum CQE bytes as powers of 2.</dd></div><div><dt>SQES</dt><dd>Submission Queue Entry Size; Encodes minimum and maximum SQE bytes as powers of 2.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 188, printed pages 156, PDF pages 156</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>NGUID</dt><dd>Namespace Globally Unique Identifier, a 128-bit global identifier for a namespace.</dd></div><div><dt>CQES</dt><dd>Completion Queue Entry Size; Encodes minimum and maximum CQE bytes as powers of 2.</dd></div><div><dt>SQES</dt><dd>Submission Queue Entry Size; Encodes minimum and maximum SQE bytes as powers of 2.</dd></div><div><dt>UUID</dt><dd>Universally Unique Identifier, a 128-bit identifier whose association scope is defined by the containing structure.</dd></div></dl>
</details>
<!-- figure-table:NVMCS13-NVM-FIG-189 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-189"><summary>NVM Figure 189 · Reference Exported Controller Configuration State</summary>
<!-- claim:NVMCS13-NVM-FIG-189-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.10">36.10.</span>Figure 189, "Reference Exported Controller Configuration State": ECNTLID=0 and limits must not exceed underlying support. Read the fields zero-based NCQS/NSQS. WZS/DSMS must correspond to underlying support and reported Commands Supported and Effects.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 189, printed pages 157-158, PDF pages 157-158</p></details>

</details>
<!-- figure-table:NVMCS13-NVM-FIG-190 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-190"><summary>NVM Figure 190 · Reference Exported Controller Configuration State</summary>
<!-- claim:NVMCS13-NVM-FIG-190-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="36.11">36.11.</span>Figure 190, "Reference Exported Controller Configuration State": Despite Controller in the caption, this is namespace configuration: ENSID=1, MS=0, RP=0, with LBADS matching the underlying namespace. A zero NGUID requires a valid NUUID.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>ENSID</dt><dd>Exported Namespace Identifier; Identifies an exported namespace.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 190, printed pages 158-159, PDF pages 158-159</p></details>
<dl class="term-note" aria-label="Terms in this passage"><div><dt>ENSID</dt><dd>Exported Namespace Identifier; Identifies an exported namespace.</dd></div></dl>
</details>
</details>
</section>
<section class="lesson" id="module-nvmcs-export-state"><h2 id="heading-nvmcs-export-state"><span class="section-number">37</span> Exported-state length and consistency</h2>
<p class="reader-paragraph"><span class="paragraph-number" aria-label="37.01">37.01.</span>Configuration state describes resource setup, while runtime state describes current Features and controller state. The latter begins with a fixed 64-byte header followed by variable-length contents.</p>
<details class="technical-note"><summary>Mechanism and applicable conditions</summary>
<!-- claim:NVMCS13-EXPORT-STATE -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="37.02">37.02.</span>Reference Exported NVM Subsystem State stores current Feature values and controller state. CSATTR.CP=1 means the controller remained suspended throughout Migration Receive processing. NVMECSS gives the variable NVMECS length in dwords; the nested VER is fixed to 1h.</p><dl class="term-note" aria-label="Terms in this passage"><div><dt>CSATTR.CP</dt><dd>Controller Suspended; one means suspended throughout Migration Receive processing.</dd></div><div><dt>NVMECSS</dt><dd>NVMe Controller State Size in dwords; zero omits the variable state field.</dd></div></dl><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.4.1.2</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.4.1.2, printed pages 159-160, PDF pages 159-160</p></details>
</details>
<div class="table-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Role or distinction</th><th scope="col">Conditions</th></tr></thead><tbody><tr><td>Feature values</td><td>Saves arbitration, power, temperature, error recovery, queues, interrupt, atomicity, and AEC</td><td>These are current values, not Figure 187 defaults</td></tr><tr><td>CSATTR.CP</td><td>1 means suspended throughout processing</td><td>0 does not mean there was no suspension at all</td></tr><tr><td>NVMECSS</td><td>Total length = 64 + 4 × NVMECSS bytes</td><td>NVMECS is absent when zero</td></tr></tbody></table></div><dl class="term-note" aria-label="Terms in this passage"><div><dt>CSATTR.CP</dt><dd>Controller Suspended; one means suspended throughout Migration Receive processing.</dd></div><div><dt>NVMECSS</dt><dd>NVMe Controller State Size in dwords; zero omits the variable state field.</dd></div></dl>
<aside class="worked-example"><h3>Example</h3><p class="reader-paragraph"><span class="paragraph-number" aria-label="37.03">37.03.</span>NVMECSS=16 gives 16×4=64 bytes of NVMECS. Adding the fixed 64-byte header yields a 128-byte structure; the nested VER identifies that state format version.</p></aside>
<details class="technical-note"><summary>Fields and data structures in more depth</summary>
<!-- figure-table:NVMCS13-NVM-FIG-191 -->
<details class="field-note" id="figure-NVMCS13-NVM-FIG-191"><summary>NVM Figure 191 · Reference Exported NVM Subsystem State</summary>
<!-- claim:NVMCS13-NVM-FIG-191-CLAIM -->
<p class="reader-paragraph"><span class="paragraph-number" aria-label="37.04">37.04.</span>Figure 191, "Reference Exported NVM Subsystem State": A 64-byte header precedes NVMECSS×4 bytes of NVMECS, absent at zero length. CP=1 establishes suspension throughout Receive processing; nested VER must be 1h.</p><details class="source-note"><summary>Sources: NVM Command Set 1.3 §5.4</summary><p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.4, Figure 191, printed pages 159-160, PDF pages 159-160</p></details>

</details>
</details>
</section>
<section id="knowledge-check"><h2 id="review-questions">Check your understanding</h2>
<!-- qa:nvm-command-set-1.3-capacity -->
<details class="review-question" id="qa-nvm-command-set-1.3-capacity"><summary>1. With NSZE=1000, NCAP=800, and NUSE=600, what question does each value answer?</summary>
<div data-qa-answer="nvm-command-set-1.3-capacity"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="38.01">38.01.</span>NSZE gives the addressable range, LBA 0 through 999; NCAP allows up to 800 allocated logical blocks; NUSE reports 600 currently allocated blocks. These are logical-block counts, so conversion to bytes also needs the data size.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.1; 4.1.5.1, printed pages 13-14,85-93, PDF pages 13-14,85-93</p>
</details></details>
<!-- qa:nvm-command-set-1.3-fused -->
<details class="review-question" id="qa-nvm-command-set-1.3-fused"><summary>2. Does placing Compare and Write next to each other in an SQ prevent intervening modifications?</summary>
<div data-qa-answer="nvm-command-set-1.3-fused"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="38.02">38.02.</span>Adjacency alone is insufficient. Use a supported fused operation, mark its first and second commands correctly, and satisfy pairing conditions such as matching ranges. Ordinary submission order does not provide that guarantee.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.2-2.1.3, printed pages 14-15, PDF pages 14-15</p>
</details></details>
<!-- qa:nvm-command-set-1.3-atomic-persistent -->
<details class="review-question" id="qa-nvm-command-set-1.3-atomic-persistent"><summary>3. Does satisfying the atomic-write size guarantee that the data survives a power loss?</summary>
<div data-qa-answer="nvm-command-set-1.3-atomic-persistent"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="38.03">38.03.</span>Atomicity concerns whether a partial update can be observed in the specified circumstances; persistence concerns storage on nonvolatile media. Normal versus power-fail atomicity, boundaries, volatile write cache, and FUA/Flush rules still need separate consideration.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.4; 4.1.3.4; 5.9, printed pages 15-21,66-67,165, PDF pages 15-21,66-67,165</p>
<p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.4; 3.3.6, printed pages 48-51,53-56, PDF pages 48-51,53-56</p>
</details></details>
<!-- qa:nvm-command-set-1.3-compare-verify -->
<details class="review-question" id="qa-nvm-command-set-1.3-compare-verify"><summary>4. Given expected data, should Compare or Verify be used to check that stored content matches it?</summary>
<div data-qa-answer="nvm-command-set-1.3-compare-verify"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="38.04">38.04.</span>Compare uses comparison data supplied by the host. Verify checks readability and applicable integrity conditions for the range without returning its data or comparing it against a host-supplied expected payload.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.1; 3.3.5, printed pages 27-30,51-53, PDF pages 27-30,51-53</p>
</details></details>
<!-- qa:nvm-command-set-1.3-zero-allocation -->
<details class="review-question" id="qa-nvm-command-set-1.3-zero-allocation"><summary>5. Can an all-zero Read establish that the LBAs remain allocated?</summary>
<div data-qa-answer="nvm-command-set-1.3-zero-allocation"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="38.05">38.05.</span>No. Written zero data and zero-valued reads from deallocated blocks can produce the same result. Interpret the read using allocation state, DRB, and whether DULBE is supported and enabled.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.3.2.1; 4.1.3.3, printed pages 47-48,66, PDF pages 47-48,66</p>
<p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §3.3.7-3.3.8, printed pages 56-61, PDF pages 56-61</p>
</details></details>
<!-- qa:nvm-command-set-1.3-format -->
<details class="review-question" id="qa-nvm-command-set-1.3-format"><summary>6. Is a data size of 4096 bytes enough to construct the correct I/O buffer?</summary>
<div data-qa-answer="nvm-command-set-1.3-format"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="38.06">38.06.</span>No. The active Format Index, metadata size, PI format, and metadata transfer mechanism are also needed. A separate buffer and extended LBAs use different memory layouts.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §1.1-1.6; 4.1.3.9; 4.1.4.8; 4.1.5, printed pages 9-12,73-75,79-83, PDF pages 9-12,73-75,79-83</p>
<p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §4.1.5.1; 4.1.5.3; 5.6, printed pages 85-94,96-102,160-162, PDF pages 85-94,96-102,160-162</p>
<p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.6; 5.2.3; 5.3, printed pages 22,129-131, PDF pages 22,129-131</p>
</details></details>
<!-- qa:nvm-command-set-1.3-pi-checks -->
<details class="review-question" id="qa-nvm-command-set-1.3-pi-checks"><summary>7. Does PRACT=1 turn off every PI check?</summary>
<div data-qa-answer="nvm-command-set-1.3-pi-checks"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="38.07">38.07.</span>PRACT controls how PI is handled during transfer; it is not a master check switch. PRCHK specifies Guard, Application Tag, and Reference Tag checks, while STC controls Storage Tag checking. Transferred contents also depend on metadata and PI sizes.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §2.1.5; 5.3.2-5.3.3, printed pages 21-22,141-152, PDF pages 21-22,141-152</p>
</details></details>
<!-- qa:nvm-command-set-1.3-rate-modes -->
<details class="review-question" id="qa-nvm-command-set-1.3-rate-modes"><summary>8. Why can throughput under a Soft Limit exceed its configured value?</summary>
<div data-qa-answer="nvm-command-set-1.3-rate-modes"><p class="reader-paragraph review-answer"><span class="paragraph-number" aria-label="38.08">38.08.</span>A Soft Limit permits use of bandwidth or IOPS left unused by other work; resource shortfalls are distributed proportionally to configured limits. A Hard Limit supplies a ceiling. Appendix A token buckets are an illustrative implementation, not a required controller architecture.</p></div>
<details class="source-note"><summary>Sources</summary>
<p>Source: NVME-NVM-CS-1.3, Rev. 1.3, §5.10.1-5.10.2; Appendix A, printed pages 166-168,176-177, PDF pages 166-168,176-177</p>
</details></details>
</section>
<footer class="reference-editions"><details class="source-note"><summary>Specification editions</summary><p>NVM Express NVM Command Set Specification, Revision 1.3</p><p>NVM Express Base Specification, Revision 2.4</p></details></footer>
</div>
