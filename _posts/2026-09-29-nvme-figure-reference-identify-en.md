---
layout: "post"
title: "NVMe Figure Reference 03 · Identify, Namespaces, and Data Formats"
date: "2026-09-29 09:00:00 +0800"
categories: ["nvme"]
tags: ["NVMe", "Reference"]
permalink: "/nvme/figure-reference/identify/en/"
nvme_quickref: true
lang: "en"
description: "NVMe source figures: uses, fields and interpretation with precise specification locations."
---

<div class="nvme-quickref">
<nav class="qr-top" aria-label="Editions and index"><a href="#content">Skip to content</a><a href="/nvme/figure-reference/en/">Index</a><a href="/nvme/figure-reference/identify/zh-tw/">繁體中文</a><a href="/DOCS/nvme-quick-reference/identify.html">Chinese HTML</a></nav>
<main id="content">
<header><p class="qr-eyebrow">LOOKUP · FIELD INTERPRETATION · SOURCE LOCATIONS</p><h1>NVMe Figure Reference 03 · Identify, Namespaces, and Data Formats</h1><p class="qr-intro">CNS selects the Identify structure. Look up controller capabilities, namespace configuration and selected-format sizes separately, then combine them into a valid configuration.</p></header>
<aside class="qr-note"><p>Each source figure has a use, field guide and worked interpretation. Example numbers are illustrative, not assumed device settings. Apply the conditions belonging to the field and command.</p><p>Use browser Find for fields, FID, LID, CNS or Figure. Positions follow the source: a byte is 8 bits and a Dword is 4 bytes. An index counts entries; an offset measures displacement from an origin in the specified unit.</p><p>FID (Feature Identifier) selects a feature; LID (Log Page Identifier) selects a log page; CNS (Controller or Namespace Structure) selects the structure returned by Identify.</p></aside>
<nav class="qr-toc" id="figure-index" aria-label="Volume figure index"><h2>Figures in this volume</h2><ol>
<li><a href="#figure-b333">Base 2.4 Figure 333 · Identify – Command Dword 10</a></li>
<li><a href="#figure-b336">Base 2.4 Figure 336 · Identify – CNS Values</a></li>
<li><a href="#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="#figure-b342">Base 2.4 Figure 342 · Identify – Namespace Identification Descriptor</a></li>
<li><a href="#figure-b346">Base 2.4 Figure 346 · Identify – I/O Command Set Independent Identify Namespace Data Structure</a></li>
<li><a href="#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></li>
<li><a href="#figure-n125">NVM Command Set 1.3 Figure 125 · LBA Format Data Structure, NVM Command Set Specific</a></li>
<li><a href="#figure-n127">NVM Command Set 1.3 Figure 127 · NVM Command Set I/O Command Set Specific Identify Namespace Data Structure</a></li>
<li><a href="#figure-n128">NVM Command Set 1.3 Figure 128 · Extended LBA Format Data Structure, NVM Command Set Specific</a></li>
<li><a href="#figure-n129">NVM Command Set 1.3 Figure 129 · I/O Command Set Specific Identify Controller Data Structure for the NVM Command Set</a></li>
</ol></nav>
<article class="qr-card" id="figure-b333" data-figure="B333">
<h2><span class="qr-number">01</span>Identify – Command Dword 10</h2>
<p class="qr-original">Base 2.4 · Figure 333 · Identify – Command Dword 10</p>
<p class="qr-location">§5.2.14 · Printed pages 337 · PDF 363</p>
<p class="qr-explanation" data-paragraph="B333-1"><span class="qr-step">01.1 · Use</span>If Identify data appears to contain impossible capacities or capabilities, check which structure the command selected. Equal buffer sizes do not imply identical byte meanings.</p>
<p class="qr-explanation" data-paragraph="B333-2"><span class="qr-step">01.2 · Fields and relationships</span>CNS bits 7:0 selects the returned structure; CNTID bits 31:16 is used by only some operations; bits 15:8 are reserved. Clear unused CNTID as specified rather than treating it as a universal controller selector.</p>
<p class="qr-explanation" data-paragraph="B333-3"><span class="qr-step">01.3 · Interpretation and example</span>CNS=01h returns information for the controller processing the command; CNS=00h returns NVM namespace data. Applying 01h byte offsets to 00h can produce meaningless results despite a correct buffer length.</p>
<p class="qr-tags">Search terms: Identify · CNS · CNTID · CNS 01h · CNS 00h</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-b336">Base 2.4 Figure 336 · Identify – CNS Values</a><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a><a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b336" data-figure="B336">
<h2><span class="qr-number">02</span>Identify – CNS Values</h2>
<p class="qr-original">Base 2.4 · Figure 336 · Identify – CNS Values</p>
<p class="qr-location">§5.2.14 · Printed pages 338–339 · PDF 364–365</p>
<p class="qr-explanation" data-paragraph="B336-1"><span class="qr-step">02.1 · Use</span>Choose an Identify operation by the object being queried. Each row also states whether NSID, CNTID and CSI are used; copying only the CNS value is insufficient.</p>
<p class="qr-explanation" data-paragraph="B336-2"><span class="qr-step">02.2 · Fields and relationships</span>Common values are 01h controller, 02h active NSID list, 03h namespace identifiers, 05h/06h command-set-specific namespace/controller and 08h command-set-independent namespace.10h lists allocated NSIDs; 16h granularity and 17h UUID-list rows provide further entry points.</p>
<p class="qr-explanation" data-paragraph="B336-3"><span class="qr-step">02.3 · Interpretation and example</span>Active and allocated lists can differ: a created but unattached namespace need not appear in this controller’s active list. Check the selected list before concluding that the namespace does not exist.</p>
<p class="qr-tags">Search terms: CNS · NSID · CNTID · CSI · Identify list</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-b333">Base 2.4 Figure 333 · Identify – Command Dword 10</a><a href="/nvme/figure-reference/identify/en/#figure-b342">Base 2.4 Figure 342 · Identify – Namespace Identification Descriptor</a><a href="/nvme/figure-reference/identify/en/#figure-b346">Base 2.4 Figure 346 · Identify – I/O Command Set Independent Identify Namespace Data Structure</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b338" data-figure="B338">
<h2><span class="qr-number">03</span>Identify – Identify Controller Data Structure, I/O Command Set Independent</h2>
<p class="qr-original">Base 2.4 · Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</p>
<p class="qr-location">§5.2.14.2.1 · Printed pages 340–382 · PDF 366–408</p>
<p class="qr-explanation" data-paragraph="B338-1"><span class="qr-step">03.1 · Use</span>This 43-page table is the main source for controller identity, capabilities and limits. Select a question first and use the field-page map below instead of scanning from beginning to end.</p>
<p class="qr-explanation" data-paragraph="B338-2"><span class="qr-step">03.2 · Fields and relationships</span>Use MDTS for transfer size, OACS for Admin commands, ONCS for I/O capabilities, LPA/ELPE for logs, FRMW for firmware and SANICAP for sanitization. SQES/CQES describes entry sizes and SGLS pointer support. Interpret NPSS together with Power State Descriptors.</p>
<p class="qr-explanation" data-paragraph="B338-3"><span class="qr-step">03.3 · Interpretation and example</span>For nonzero MDTS, multiply the minimum page size from CAP.MPSMIN by 2^MDTS:4 KiB and MDTS=5 gives 128 KiB. MDTS=0 removes this field’s limit, not every command or namespace limit. O/M/R markings, controller type and footnotes remain part of applicability.</p>
<h3>Field locations within the large table</h3>
<div class="qr-table"><table class=""><thead><tr><th scope="col">Fields</th><th scope="col">Information to find</th><th scope="col">PDF pages</th></tr></thead><tbody><tr><td>MDTS</td><td>Transfer size limit</td><td>368</td></tr><tr><td>OACS</td><td>Admin command support</td><td>378–380</td></tr><tr><td>FRMW</td><td>Firmware slots and update capabilities</td><td>380–381</td></tr><tr><td>LPA</td><td>Log-page capabilities</td><td>381–382</td></tr><tr><td>ELPE / NPSS</td><td>Error-entry limit / power-state count</td><td>382</td></tr><tr><td>SANICAP</td><td>Sanitize capabilities</td><td>387–388</td></tr><tr><td>SQES / CQES</td><td>Queue-entry sizes</td><td>396</td></tr><tr><td>ONCS</td><td>I/O command and feature support</td><td>397–399</td></tr><tr><td>VWC / AWUN / AWUPF</td><td>Cache and atomicity fields</td><td>400</td></tr><tr><td>SGLS</td><td>SGL types and alignment</td><td>403–404</td></tr></tbody></table></div>
<p class="qr-tags">Search terms: Identify Controller · MDTS · OACS · ONCS · LPA · ELPE · FRMW · SANICAP · SQES · CQES · SGLS · NPSS</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a><a href="/nvme/figure-reference/features/en/#figure-b340">Base 2.4 Figure 340 · Identify – Power State Descriptor Data Structure</a><a href="/nvme/figure-reference/logs/en/#figure-b217">Base 2.4 Figure 217 · Commands Supported and Effects Data Structure</a><a href="/nvme/figure-reference/identify/en/#figure-n129">NVM Command Set 1.3 Figure 129 · I/O Command Set Specific Identify Controller Data Structure for the NVM Command Set</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b342" data-figure="B342">
<h2><span class="qr-number">04</span>Identify – Namespace Identification Descriptor</h2>
<p class="qr-original">Base 2.4 · Figure 342 · Identify – Namespace Identification Descriptor</p>
<p class="qr-location">§5.2.14.2.3 · Printed pages 388 · PDF 414</p>
<p class="qr-explanation" data-paragraph="B342-1"><span class="qr-step">04.1 · Use</span>Use identification descriptors to compare namespace identity across queries or controllers. An NSID used to address commands is not a substitute for persistent identity information.</p>
<p class="qr-explanation" data-paragraph="B342-2"><span class="qr-step">04.2 · Fields and relationships</span>NIDT byte 0 chooses the type; NIDL byte 1 gives NID length; bytes 3:2 are reserved and NID begins at byte 4. Types 1/2/3/4 contain 8-byte EUI64, 16-byte NGUID, 16-byte UUID and 1-byte CSI. Total size is NIDL+4; NIDL=0 ends the list.</p>
<p class="qr-explanation" data-paragraph="B342-3"><span class="qr-step">04.3 · Interpretation and example</span>An entry with NIDL=16 occupies 20 bytes, so the next starts at the old offset plus 20, not 16. CSI identifies a command set, not a globally unique namespace despite occupying the NID field.</p>
<p class="qr-tags">Search terms: NIDT · NIDL · NID · EUI64 · NGUID · UUID · CSI</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-b336">Base 2.4 Figure 336 · Identify – CNS Values</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b346" data-figure="B346">
<h2><span class="qr-number">05</span>Identify – I/O Command Set Independent Identify Namespace Data Structure</h2>
<p class="qr-original">Base 2.4 · Figure 346 · Identify – I/O Command Set Independent Identify Namespace Data Structure</p>
<p class="qr-location">§5.2.14.2.8 · Printed pages 391–394 · PDF 417–420</p>
<p class="qr-explanation" data-paragraph="B346-1"><span class="qr-step">05.1 · Use</span>Use this command-set-independent structure for namespace readiness, write protection and resource membership. Its byte layout differs from NVM CNS=00h.</p>
<p class="qr-explanation" data-paragraph="B346-2"><span class="qr-step">05.2 · Fields and relationships</span>Common fields are NSFEAT byte 0, NMIC byte 1, RESCAP byte 2, FPI byte 3, ANAGRPID bytes 7:4 and NSATTR byte 8, followed by NVMSETID, ENDGID and NSTAT. FPI reports remaining Format percentage; NSATTR.CWP reports current write protection; NSTAT.NRDY reports namespace readiness.</p>
<p class="qr-explanation" data-paragraph="B346-3"><span class="qr-step">05.3 · Interpretation and example</span>CSTS.RDY=1 with namespace NRDY=0 can describe different readiness levels during media-independent initialization rather than a contradiction. Use ENDGID to select the corresponding Endurance Group health log.</p>
<p class="qr-tags">Search terms: CNS 08h · NSTAT · NRDY · NSATTR · FPI · ENDGID · NVMSETID · ANAGRPID</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-b42">Base 2.4 Figure 42 · Offset 1Ch: CSTS – Controller Status</a><a href="/nvme/figure-reference/logs/en/#figure-b225">Base 2.4 Figure 225 · Endurance Group Information Log Page</a><a href="/nvme/figure-reference/maintenance/en/#figure-b541">Base 2.4 Figure 541 · Write Protection – Command Dword 11</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n123" data-figure="N123">
<h2><span class="qr-number">06</span>Identify – Identify Namespace Data Structure, NVM Command Set</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</p>
<p class="qr-location">§4.1.5.1 · Printed pages 85–93 · PDF 85–93</p>
<p class="qr-explanation" data-paragraph="N123-1"><span class="qr-step">06.1 · Use</span>This is the primary NVM namespace lookup for capacity, format and alignment behavior. Distinguish the active format, supported-format list and performance recommendations.</p>
<p class="qr-explanation" data-paragraph="N123-2"><span class="qr-step">06.2 · Fields and relationships</span>NSZE bytes 7:0 counts addressable blocks; NCAP bytes 15:8 gives maximum allocation; NUSE bytes 23:16 current allocation. FLBAS byte 26 selects a format, DPS byte 29 selects PI settings and DLFEAT byte 33 describes deallocation behavior. NAWUN/NAWUPF and boundaries qualify atomicity; LBAF entries provide format sizes.</p>
<p class="qr-explanation" data-paragraph="N123-3"><span class="qr-step">06.3 · Interpretation and example</span>NSZE=1000 means LBAs 0–999. With selected LBADS=12, data capacity is 1000×4096=4,096,000 bytes. FLBAS=12h is not an 18-byte format: it selects index 2 and metadata placement, with sizes obtained from that LBAF.</p>
<h3>Field locations within the large table</h3>
<div class="qr-table"><table class=""><thead><tr><th scope="col">Fields</th><th scope="col">Information to find</th><th scope="col">PDF pages</th></tr></thead><tbody><tr><td>NSZE / NCAP / NUSE / NSFEAT</td><td>Capacity and feature conditions</td><td>85–86</td></tr><tr><td>FLBAS / MC / DPC / DPS</td><td>Format and protection configuration</td><td>86–87</td></tr><tr><td>DLFEAT / NAWUN / NAWUPF</td><td>Deallocation behavior and atomic units</td><td>88–89</td></tr><tr><td>NABSN / NABO / NABSPF</td><td>Atomicity boundaries</td><td>89</td></tr><tr><td>NPWG / NPWA / NPDG / NPDA</td><td>Recommended performance granularity and alignment</td><td>90</td></tr><tr><td>LBAF</td><td>Format-list location and count</td><td>93</td></tr></tbody></table></div>
<p class="qr-tags">Search terms: CNS 00h · NSZE · NCAP · NUSE · FLBAS · DPS · DLFEAT · LBAF · NAWUN · NABSN</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-n125">NVM Command Set 1.3 Figure 125 · LBA Format Data Structure, NVM Command Set Specific</a><a href="/nvme/figure-reference/io/en/#figure-n4">NVM Command Set 1.3 Figure 4 · Atomicity Parameters for Single Atomicity Mode</a><a href="/nvme/figure-reference/io/en/#figure-n8">NVM Command Set 1.3 Figure 8 · Atomic Boundaries Example</a><a href="/nvme/figure-reference/identify/en/#figure-n127">NVM Command Set 1.3 Figure 127 · NVM Command Set I/O Command Set Specific Identify Namespace Data Structure</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n125" data-figure="N125">
<h2><span class="qr-number">07</span>LBA Format Data Structure, NVM Command Set Specific</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 125 · LBA Format Data Structure, NVM Command Set Specific</p>
<p class="qr-location">§4.1.5.1 · Printed pages 94 · PDF 94</p>
<p class="qr-explanation" data-paragraph="N125-1"><span class="qr-step">07.1 · Use</span>After FLBAS selects a format index, decode its four-byte LBAF entry here. It gives per-block data and metadata sizes.</p>
<p class="qr-explanation" data-paragraph="N125-2"><span class="qr-step">07.2 · Fields and relationships</span>MS bits 15:0 directly counts metadata bytes. LBADS bits 23:16 is the data-size exponent; zero means the format is currently unavailable. RP bits 25:24 ranks relative performance for the specified workload, not IOPS.</p>
<p class="qr-explanation" data-paragraph="N125-3"><span class="qr-step">07.3 · Interpretation and example</span>LBADS=12 and MS=8 mean 4096 data bytes plus 8 metadata bytes. Extended-LBA placement occupies 4104 bytes per block. LBADS excludes metadata, and RP=0 does not guarantee the fastest result for every workload.</p>
<p class="qr-tags">Search terms: LBAF · LBADS · MS · RP</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a><a href="/nvme/figure-reference/io/en/#figure-n153">NVM Command Set 1.3 Figure 153 · Metadata – Contiguous with LBA Data, Forming Extended LBA</a><a href="/nvme/figure-reference/io/en/#figure-n154">NVM Command Set 1.3 Figure 154 · Metadata – Transferred as Separate Buffer</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n127" data-figure="N127">
<h2><span class="qr-number">08</span>NVM Command Set I/O Command Set Specific Identify Namespace Data Structure</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 127 · NVM Command Set I/O Command Set Specific Identify Namespace Data Structure</p>
<p class="qr-location">§4.1.5.3 · Printed pages 97–101 · PDF 97–101</p>
<p class="qr-explanation" data-paragraph="N127-1"><span class="qr-step">08.1 · Use</span>For 32/64-bit Guard, Storage Tags and extended formats, supplement CNS=00h with this CNS=05h/CSI=00h structure. It adds format capabilities rather than replacing FLBAS/DPS.</p>
<p class="qr-explanation" data-paragraph="N127-2"><span class="qr-step">08.2 · Fields and relationships</span>LBSTM supplies a Storage Tag mask, PIC reports protection-format capabilities, and the ELBAF array describes Guard format and tag width for each format index. Mask applicability also depends on PI enablement, PIC and masking-level capabilities.</p>
<p class="qr-explanation" data-paragraph="N127-3"><span class="qr-step">08.3 · Interpretation and example</span>Match the same index in LBAF and ELBAF: one supplies data/metadata sizes, the other PI layout. Sixteen metadata bytes alone do not establish a 64-bit Guard format.</p>
<p class="qr-tags">Search terms: CNS 05h · CSI 00h · LBSTM · PIC · ELBAF · Storage Tag</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-n128">NVM Command Set 1.3 Figure 128 · Extended LBA Format Data Structure, NVM Command Set Specific</a><a href="/nvme/figure-reference/identify/en/#figure-n125">NVM Command Set 1.3 Figure 125 · LBA Format Data Structure, NVM Command Set Specific</a><a href="/nvme/figure-reference/io/en/#figure-n159">NVM Command Set 1.3 Figure 159 · 64b Guard Protection Information Format</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n128" data-figure="N128">
<h2><span class="qr-number">09</span>Extended LBA Format Data Structure, NVM Command Set Specific</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 128 · Extended LBA Format Data Structure, NVM Command Set Specific</p>
<p class="qr-location">§4.1.5.3 · Printed pages 101–102 · PDF 101–102</p>
<p class="qr-explanation" data-paragraph="N128-1"><span class="qr-step">09.1 · Use</span>Use ELBAF to resolve Guard format and the split between Storage and Reference Tags. STS here means Storage Tag Size, not status.</p>
<p class="qr-explanation" data-paragraph="N128-2"><span class="qr-step">09.2 · Fields and relationships</span>STS bits 6:0 gives Storage Tag width. PIF bits 8:7 selects 16/32/64-bit Guard or a qualified format. QPIF bits 12:9 applies only with PIF=11b and the required capability. These fields do not establish transmitted PI when PI is disabled.</p>
<p class="qr-explanation" data-paragraph="N128-3"><span class="qr-step">09.3 · Interpretation and example</span>PIF=10b and STS=16 selects 64-bit Guard with 16 high bits of its 48-bit Storage/Reference space assigned to Storage Tag and 32 remaining for Reference Tag. Allowed STS ranges differ across Guard formats.</p>
<p class="qr-tags">Search terms: ELBAF · PIF · QPIF · STS · QPIFS</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-n127">NVM Command Set 1.3 Figure 127 · NVM Command Set I/O Command Set Specific Identify Namespace Data Structure</a><a href="/nvme/figure-reference/io/en/#figure-n155">NVM Command Set 1.3 Figure 155 · 16b Guard Protection Information Format when STS field is cleared to 0h</a><a href="/nvme/figure-reference/io/en/#figure-n157">NVM Command Set 1.3 Figure 157 · 32b Guard Protection Information Format</a><a href="/nvme/figure-reference/io/en/#figure-n159">NVM Command Set 1.3 Figure 159 · 64b Guard Protection Information Format</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n129" data-figure="N129">
<h2><span class="qr-number">10</span>I/O Command Set Specific Identify Controller Data Structure for the NVM Command Set</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 129 · I/O Command Set Specific Identify Controller Data Structure for the NVM Command Set</p>
<p class="qr-location">§4.1.5.4 · Printed pages 103–106 · PDF 103–106</p>
<p class="qr-explanation" data-paragraph="N129-1"><span class="qr-step">10.1 · Use</span>Consult this CNS=06h/CSI=00h structure when Verify, Write Zeroes or Dataset Management encounters a size limit. Base MDTS is not every command’s sole constraint.</p>
<p class="qr-explanation" data-paragraph="N129-2"><span class="qr-step">10.2 · Fields and relationships</span>VSL/WZSL/WUSL use minimum-memory-page-based exponential sizes. DMRL counts ranges, DMRSL blocks per range and DMSL total blocks. ONCS support-variant bits determine whether limits are mandatory or recommended and change zero semantics.</p>
<p class="qr-explanation" data-paragraph="N129-3"><span class="qr-step">10.3 · Interpretation and example</span>DMRL=0 with NVMDSMSV=1 means no recommended range-count limit is reported. With NVMDSMSV=0, DMRL=0 means Dataset Management is unsupported. Do not translate every zero as unlimited.</p>
<h3>Field locations within the large table</h3>
<div class="qr-table"><table class=""><thead><tr><th scope="col">Fields</th><th scope="col">Information to find</th><th scope="col">PDF pages</th></tr></thead><tbody><tr><td>VSL / WZSL</td><td>Verify / Write Zeroes sizes</td><td>103</td></tr><tr><td>WUSL / DMRL / DMRSL</td><td>Write Uncorrectable and DSM range limits</td><td>104</td></tr><tr><td>DMSL / KPIOCAP / WZDSL</td><td>Total blocks, key capabilities, deallocate size</td><td>105</td></tr><tr><td>AOCS / VER / RLA</td><td>Admin support, version and rate-limit capabilities</td><td>106</td></tr></tbody></table></div>
<p class="qr-tags">Search terms: CNS 06h · CSI 00h · VSL · WZSL · WUSL · DMRL · DMRSL · DMSL · NVMDSMSV</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a><a href="/nvme/figure-reference/io/en/#figure-n47">NVM Command Set 1.3 Figure 47 · Dataset Management – Range Definition</a><a href="/nvme/figure-reference/io/en/#figure-n83">NVM Command Set 1.3 Figure 83 · Write Zeroes – Command Dword 12</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<footer id="source-files"><h2>Source documents</h2><p>Locations refer to the supplied ratified PDFs. For Base, PDF page = printed page +26; the other two use identical page numbers. Original figure numbers and English titles are retained for PDF search. Source PDFs are not redistributed.</p><ul class="qr-sources"><li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li></ul></footer>
</main></div>
