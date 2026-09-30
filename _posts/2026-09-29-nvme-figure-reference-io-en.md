---
layout: "post"
title: "NVMe Figure Reference 04 · I/O Commands and Data Integrity"
date: "2026-09-29 09:00:00 +0800"
categories: ["nvme"]
tags: ["NVMe", "Reference"]
permalink: "/nvme/figure-reference/io/en/"
nvme_quickref: true
lang: "en"
description: "NVMe source figures: uses, fields and interpretation with precise specification locations."
---

<div class="nvme-quickref">
<nav class="qr-top" aria-label="Editions and index"><a href="#content">Skip to content</a><a href="/nvme/figure-reference/en/">Index</a><a href="/nvme/figure-reference/io/zh-tw/">繁體中文</a><a href="/DOCS/nvme-quick-reference/io.html">Chinese HTML</a></nav>
<main id="content">
<header><p class="qr-eyebrow">LOOKUP · FIELD INTERPRETATION · SOURCE LOCATIONS</p><h1>NVMe Figure Reference 04 · I/O Commands and Data Integrity</h1><p class="qr-intro">Follow command addresses and counts into metadata, protection information and atomicity. Equal field widths do not imply equal counting rules; command success alone does not establish every persistence or atomicity guarantee.</p></header>
<aside class="qr-note"><p>Each source figure has a use, field guide and worked interpretation. Example numbers are illustrative, not assumed device settings. Apply the conditions belonging to the field and command.</p><p>Use browser Find for fields, FID, LID, CNS or Figure. Positions follow the source: a byte is 8 bits and a Dword is 4 bytes. An index counts entries; an offset measures displacement from an origin in the specified unit.</p><p>FID (Feature Identifier) selects a feature; LID (Log Page Identifier) selects a log page; CNS (Controller or Namespace Structure) selects the structure returned by Identify.</p></aside>
<nav class="qr-toc" id="figure-index" aria-label="Volume figure index"><h2>Figures in this volume</h2><ol>
<li><a href="#figure-n4">NVM Command Set 1.3 Figure 4 · Atomicity Parameters for Single Atomicity Mode</a></li>
<li><a href="#figure-n8">NVM Command Set 1.3 Figure 8 · Atomic Boundaries Example</a></li>
<li><a href="#figure-n22">NVM Command Set 1.3 Figure 22 · Opcodes for NVM Commands</a></li>
<li><a href="#figure-n53">NVM Command Set 1.3 Figure 53 · Read – Command Dword 10 and Command Dword 11</a></li>
<li><a href="#figure-n54">NVM Command Set 1.3 Figure 54 · Read – Command Dword 12</a></li>
<li><a href="#figure-n70">NVM Command Set 1.3 Figure 70 · Write – Command Dword 10 and Command Dword 11</a></li>
<li><a href="#figure-n71">NVM Command Set 1.3 Figure 71 · Write – Command Dword 12</a></li>
<li><a href="#figure-n39">NVM Command Set 1.3 Figure 39 · Copy – Copy Descriptor Formats</a></li>
<li><a href="#figure-n47">NVM Command Set 1.3 Figure 47 · Dataset Management – Range Definition</a></li>
<li><a href="#figure-n83">NVM Command Set 1.3 Figure 83 · Write Zeroes – Command Dword 12</a></li>
<li><a href="#figure-n153">NVM Command Set 1.3 Figure 153 · Metadata – Contiguous with LBA Data, Forming Extended LBA</a></li>
<li><a href="#figure-n154">NVM Command Set 1.3 Figure 154 · Metadata – Transferred as Separate Buffer</a></li>
<li><a href="#figure-n155">NVM Command Set 1.3 Figure 155 · 16b Guard Protection Information Format when STS field is cleared to 0h</a></li>
<li><a href="#figure-n157">NVM Command Set 1.3 Figure 157 · 32b Guard Protection Information Format</a></li>
<li><a href="#figure-n159">NVM Command Set 1.3 Figure 159 · 64b Guard Protection Information Format</a></li>
<li><a href="#figure-n174">NVM Command Set 1.3 Figure 174 · Write Command 16b Guard Protection Information Processing</a></li>
<li><a href="#figure-n175">NVM Command Set 1.3 Figure 175 · Read 16b Guard Command Protection Information Processing</a></li>
</ol></nav>
<article class="qr-card" id="figure-n4" data-figure="N4">
<h2><span class="qr-number">01</span>Atomicity Parameters for Single Atomicity Mode</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 4 · Atomicity Parameters for Single Atomicity Mode</p>
<p class="qr-location">§2.1.4 · Printed pages 15–16 · PDF 15–16</p>
<p class="qr-explanation" data-paragraph="N4-1"><span class="qr-step">01.1 · Use</span>Use this table to organize controller baselines, namespace-specific values and boundaries when assessing whole-write atomicity. It explicitly concerns Single Atomicity Mode.</p>
<p class="qr-explanation" data-paragraph="N4-2"><span class="qr-step">01.2 · Fields and relationships</span>AWUN/AWUPF distinguish normal and power-failure conditions; ACWU applies to fused Compare and Write. The NA-prefixed fields are namespace values. NABSN/NABSPF and NABO define boundaries. Inequalities constrain supported parameters; decode each field’s representation separately.</p>
<p class="qr-explanation" data-paragraph="N4-3"><span class="qr-step">01.3 · Interpretation and example</span>Even a write within NAWUN can lose the namespace-level whole-write guarantee if it crosses an atomic boundary in Single Atomicity Mode. Check mode, unit size, starting address and extent rather than NLB alone.</p>
<p class="qr-tags">Search terms: AWUN · AWUPF · NAWUN · NAWUPF · ACWU · NACWU · atomicity</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/io/en/#figure-n8">NVM Command Set 1.3 Figure 8 · Atomic Boundaries Example</a><a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n8" data-figure="N8">
<h2><span class="qr-number">02</span>Atomic Boundaries Example</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 8 · Atomic Boundaries Example</p>
<p class="qr-location">§2.1.4.4 · Printed pages 19 · PDF 19</p>
<p class="qr-explanation" data-paragraph="N8-1"><span class="qr-step">02.1 · Use</span>The diagram divides LBA space into atomic-boundary intervals. Colors distinguish intervals, not namespaces or media.</p>
<p class="qr-explanation" data-paragraph="N8-2"><span class="qr-step">02.2 · Fields and relationships</span>NABO positions the first boundary; decoded boundary size spaces subsequent ones. SLBA and block count locate the write. NABSN/NABSPF cover different conditions, with special zero and minus-one encodings in the original fields.</p>
<p class="qr-explanation" data-paragraph="N8-3"><span class="qr-step">02.3 · Interpretation and example</span>For a decoded boundary size of 8 blocks and offset 0, LBAs 4–7 stay within one interval while 6–9 cross boundary 8. Both contain four blocks, but size alone cannot establish the Single Atomicity whole-write guarantee for the latter.</p>
<p class="qr-tags">Search terms: NABO · NABSN · NABSPF · atomic boundary · alignment</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/io/en/#figure-n4">NVM Command Set 1.3 Figure 4 · Atomicity Parameters for Single Atomicity Mode</a><a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n22" data-figure="N22">
<h2><span class="qr-number">03</span>Opcodes for NVM Commands</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 22 · Opcodes for NVM Commands</p>
<p class="qr-location">§3.3 · Printed pages 27 · PDF 27</p>
<p class="qr-explanation" data-paragraph="N22-1"><span class="qr-step">03.1 · Use</span>Map opcodes to NVM I/O commands here. The same opcode can have a different meaning on Admin and I/O queues.</p>
<p class="qr-explanation" data-paragraph="N22-2"><span class="qr-step">03.2 · Fields and relationships</span>Rows provide opcode, command and definition location, including Flush 00h, Write 01h, Read 02h, Compare 05h, Write Zeroes 08h, Dataset Management 09h, Verify 0Ch and Copy 19h. Check capabilities for support.</p>
<p class="qr-explanation" data-paragraph="N22-3"><span class="qr-step">03.3 · Interpretation and example</span>OPC=02h on an NVM I/O SQ means Read; on Admin SQ this table does not apply. Preserve queue type, CSI and opcode together to avoid mistaking log retrieval for media reads.</p>
<p class="qr-tags">Search terms: opcode · Read 02h · Write 01h · Flush 00h · Compare 05h · Copy 19h</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b92">Base 2.4 Figure 92 · Command Dword 0</a><a href="/nvme/figure-reference/io/en/#figure-n53">NVM Command Set 1.3 Figure 53 · Read – Command Dword 10 and Command Dword 11</a><a href="/nvme/figure-reference/io/en/#figure-n70">NVM Command Set 1.3 Figure 70 · Write – Command Dword 10 and Command Dword 11</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n53" data-figure="N53">
<h2><span class="qr-number">04</span>Read – Command Dword 10 and Command Dword 11</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 53 · Read – Command Dword 10 and Command Dword 11</p>
<p class="qr-location">§3.3.4 · Printed pages 49 · PDF 49</p>
<p class="qr-explanation" data-paragraph="N53-1"><span class="qr-step">04.1 · Use</span>Combine CDW10/11 into the full SLBA when checking a Read address. It addresses logical blocks within the namespace, not host memory.</p>
<p class="qr-explanation" data-paragraph="N53-2"><span class="qr-step">04.2 · Fields and relationships</span>SLBA is 64 bits: low 32 in CDW10 and high 32 in CDW11. Its byte position depends on the current LBA size; CDW12.NLB supplies the length separately.</p>
<p class="qr-explanation" data-paragraph="N53-3"><span class="qr-step">04.3 · Interpretation and example</span>CDW11=1 and CDW10=0 means SLBA=4294967296, not LBA 0. The inclusive final LBA is SLBA+NLB because raw NLB encodes block count minus one.</p>
<p class="qr-tags">Search terms: Read · SLBA · CDW10 · CDW11</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/io/en/#figure-n54">NVM Command Set 1.3 Figure 54 · Read – Command Dword 12</a><a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n54" data-figure="N54">
<h2><span class="qr-number">05</span>Read – Command Dword 12</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 54 · Read – Command Dword 12</p>
<p class="qr-location">§3.3.4 · Printed pages 49 · PDF 49</p>
<p class="qr-explanation" data-paragraph="N54-1"><span class="qr-step">05.1 · Use</span>Use CDW12 when Read length, recovery or protection behavior differs from expectation. Its controls are separate mechanisms, not one “strict read” switch.</p>
<p class="qr-explanation" data-paragraph="N54-2"><span class="qr-step">05.2 · Fields and relationships</span>NLB bits 15:0 encodes blocks minus one; CETYPE bits 19:16 selects extensions; STC bit 24 checks Storage Tags; PRINFO bits 29:26 controls PI action/checks. FUA bit 30 commits relevant data/metadata to nonvolatile media and reads it from there. LR bit 31 requests limited retries.</p>
<p class="qr-explanation" data-paragraph="N54-3"><span class="qr-step">05.3 · Interpretation and example</span>NLB=7 with 4096-byte blocks transfers 32768 data bytes. FUA does not order other commands, and LR does not guarantee a fixed completion deadline.</p>
<p class="qr-tags">Search terms: Read NLB · LR · FUA · PRINFO · STC · CETYPE</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/io/en/#figure-n53">NVM Command Set 1.3 Figure 53 · Read – Command Dword 10 and Command Dword 11</a><a href="/nvme/figure-reference/io/en/#figure-n175">NVM Command Set 1.3 Figure 175 · Read 16b Guard Command Protection Information Processing</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n70" data-figure="N70">
<h2><span class="qr-number">06</span>Write – Command Dword 10 and Command Dword 11</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 70 · Write – Command Dword 10 and Command Dword 11</p>
<p class="qr-location">§3.3.6 · Printed pages 54 · PDF 54</p>
<p class="qr-explanation" data-paragraph="N70-1"><span class="qr-step">06.1 · Use</span>Separate the destination LBA from the host source buffer when investigating misplaced writes. This figure defines Write SLBA, not PRP or SGL addresses.</p>
<p class="qr-explanation" data-paragraph="N70-2"><span class="qr-step">06.2 · Fields and relationships</span>CDW10/11 combines low/high 32-bit halves into a 64-bit SLBA. Units are blocks of the selected namespace format, not universally 512-byte sectors.</p>
<p class="qr-explanation" data-paragraph="N70-3"><span class="qr-step">06.3 · Interpretation and example</span>SLBA=8 corresponds to byte 4096 with 512-byte blocks and byte 32768 with 4 KiB blocks. Confirm the format before comparing application byte-offset calculations.</p>
<p class="qr-tags">Search terms: Write · SLBA · destination LBA</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/io/en/#figure-n71">NVM Command Set 1.3 Figure 71 · Write – Command Dword 12</a><a href="/nvme/figure-reference/identify/en/#figure-n125">NVM Command Set 1.3 Figure 125 · LBA Format Data Structure, NVM Command Set Specific</a><a href="/nvme/figure-reference/command/en/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n71" data-figure="N71">
<h2><span class="qr-number">07</span>Write – Command Dword 12</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 71 · Write – Command Dword 12</p>
<p class="qr-location">§3.3.6 · Printed pages 54 · PDF 54</p>
<p class="qr-explanation" data-paragraph="N71-1"><span class="qr-step">07.1 · Use</span>Inspect FUA and PI controls when determining what Write completion guarantees, retaining namespace format and cache context. Completion does not automatically persist every other write.</p>
<p class="qr-explanation" data-paragraph="N71-2"><span class="qr-step">07.2 · Fields and relationships</span>NLB bits 15:0 is blocks minus one; CETYPE bits 19:16 and DTYPE bits 23:20 select extensions and directives. STC bit 24/PRINFO bits 29:26 control protection. FUA bit 30 requires this command’s data/metadata on nonvolatile media before completion; LR bit 31 controls recovery effort.</p>
<p class="qr-explanation" data-paragraph="N71-3"><span class="qr-step">07.3 · Interpretation and example</span>FUA=1 strengthens this Write’s completion condition without implicitly ordering another Write. For FDP or Streams, decode CDW13 using DTYPE and CETYPE rather than assigning a fixed meaning to the same identifier bits.</p>
<p class="qr-tags">Search terms: Write NLB · FUA · LR · PRINFO · DTYPE · CETYPE · STC</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/features/en/#figure-b471">Base 2.4 Figure 471 · Volatile Write Cache – Command Dword 11</a><a href="/nvme/figure-reference/io/en/#figure-n174">NVM Command Set 1.3 Figure 174 · Write Command 16b Guard Protection Information Processing</a><a href="/nvme/figure-reference/features/en/#figure-b294">Base 2.4 Figure 294 · FDP Configuration Descriptor</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n39" data-figure="N39">
<h2><span class="qr-number">08</span>Copy – Copy Descriptor Formats</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 39 · Copy – Copy Descriptor Formats</p>
<p class="qr-location">§3.3.2 · Printed pages 32 · PDF 32</p>
<p class="qr-explanation" data-paragraph="N39-1"><span class="qr-step">08.1 · Use</span>Select the Copy descriptor format before decoding its source list. It determines presence of source NSID and PI layout; a wrong format shifts the interpretation of subsequent bytes.</p>
<p class="qr-explanation" data-paragraph="N39-2"><span class="qr-step">08.2 · Fields and relationships</span>Formats 0/1 omit SNSID and use the destination namespace as source; 2/3 include SNSID and permit a different source.0/2 use 8-byte 16-bit-Guard PI; 1/3 use 16-byte 32/64-bit-Guard PI. Format 4 references SLM, whose full definition is outside the three supplied sources.</p>
<p class="qr-explanation" data-paragraph="N39-3"><span class="qr-step">08.3 · Interpretation and example</span>For DF=2, do not use a format 0 decoder that assumes SNSID is absent. Cross-namespace support, format compatibility and range limits still require Copy capability and command checks.</p>
<p class="qr-tags">Search terms: Copy · DF · SNSID · descriptor format</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-n19">NVM Command Set 1.3 Figure 19 · Status Code – Command Specific Status Values</a><a href="/nvme/figure-reference/identify/en/#figure-n125">NVM Command Set 1.3 Figure 125 · LBA Format Data Structure, NVM Command Set Specific</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n47" data-figure="N47">
<h2><span class="qr-number">09</span>Dataset Management – Range Definition</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 47 · Dataset Management – Range Definition</p>
<p class="qr-location">§3.3.3 · Printed pages 45 · PDF 45</p>
<p class="qr-explanation" data-paragraph="N47-1"><span class="qr-step">09.1 · Use</span>This table maps Dataset Management range indices to byte positions. An index counts entries; an offset counts bytes from the buffer start.</p>
<p class="qr-explanation" data-paragraph="N47-2"><span class="qr-step">09.2 · Fields and relationships</span>Each entry is 16 bytes: CATTR at relative 3:0, LLB bytes 7:4 and SLBA bytes 15:8. Entry i starts at 16×i. LLB directly counts blocks rather than using Read/Write’s plus-one NLB encoding. NR separately specifies the command’s range count.</p>
<p class="qr-explanation" data-paragraph="N47-3"><span class="qr-step">09.3 · Interpretation and example</span>The second entry, index 1, starts at byte 16. SLBA=100 with LLB=8 describes LBAs 100–107, not nine blocks. Processing extent also depends on DMRL/DMRSL/DMSL and support-variant capabilities.</p>
<p class="qr-tags">Search terms: DSM · CATTR · LLB · SLBA · range index · offset</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-n129">NVM Command Set 1.3 Figure 129 · I/O Command Set Specific Identify Controller Data Structure for the NVM Command Set</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n83" data-figure="N83">
<h2><span class="qr-number">10</span>Write Zeroes – Command Dword 12</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 83 · Write Zeroes – Command Dword 12</p>
<p class="qr-location">§3.3.8 · Printed pages 59–60 · PDF 59–60</p>
<p class="qr-explanation" data-paragraph="N83-1"><span class="qr-step">10.1 · Use</span>Distinguish range zeroing, deallocation requests and whole-namespace zeroing here. Similar names do not confer Sanitize’s security guarantees.</p>
<p class="qr-explanation" data-paragraph="N83-2"><span class="qr-step">10.2 · Fields and relationships</span>NLB bits 15:0 encodes blocks minus one. NSZ bit 23 requests whole-namespace processing in conjunction with DEAC bit 25 and support. STC bit 24 and PRCHK must be zero. FUA bit 30 specifies the nonvolatile completion condition.</p>
<p class="qr-explanation" data-paragraph="N83-3"><span class="qr-step">10.3 · Interpretation and example</span>NSZ=1 with DEAC=0 returns Invalid Field in Command. With NSZ=1, the controller ignores NLB, so NLB=0 cannot be used to infer a one-block operation. Establish scope from NSZ and capabilities first.</p>
<p class="qr-tags">Search terms: Write Zeroes · DEAC · NSZ · NLB · PRCHK · STC</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-n129">NVM Command Set 1.3 Figure 129 · I/O Command Set Specific Identify Controller Data Structure for the NVM Command Set</a><a href="/nvme/figure-reference/maintenance/en/#figure-b451">Base 2.4 Figure 451 · Sanitize – Command Dword 10</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n153" data-figure="N153">
<h2><span class="qr-number">11</span>Metadata – Contiguous with LBA Data, Forming Extended LBA</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 153 · Metadata – Contiguous with LBA Data, Forming Extended LBA</p>
<p class="qr-location">§5.2.3 · Printed pages 129 · PDF 129</p>
<p class="qr-explanation" data-paragraph="N153-1"><span class="qr-step">11.1 · Use</span>Use this diagram to calculate transfer length and successive block positions in extended-LBA layout. It does not place one metadata batch after the entire data batch.</p>
<p class="qr-explanation" data-paragraph="N153-2"><span class="qr-step">11.2 · Fields and relationships</span>Each block’s data is followed by its metadata, then the next block. Both use the data buffer. LBADS defines data size, MS metadata bytes, and namespace configuration selects the layout.</p>
<p class="qr-explanation" data-paragraph="N153-3"><span class="qr-step">11.3 · Interpretation and example</span>With 4096 data bytes and 8 metadata bytes per block, the second starts at 4104 and the third at 8208. A4096-byte stride incorrectly treats metadata as the next block’s beginning.</p>
<p class="qr-tags">Search terms: extended LBA · metadata · MS · FLBAS</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-n125">NVM Command Set 1.3 Figure 125 · LBA Format Data Structure, NVM Command Set Specific</a><a href="/nvme/figure-reference/io/en/#figure-n154">NVM Command Set 1.3 Figure 154 · Metadata – Transferred as Separate Buffer</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n154" data-figure="N154">
<h2><span class="qr-number">12</span>Metadata – Transferred as Separate Buffer</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 154 · Metadata – Transferred as Separate Buffer</p>
<p class="qr-location">§5.2.3 · Printed pages 130 · PDF 130</p>
<p class="qr-explanation" data-paragraph="N154-1"><span class="qr-step">12.1 · Use</span>This diagram pairs two separate buffers by LBA. Physical separation does not remove the one-to-one relationship between each block and its metadata.</p>
<p class="qr-explanation" data-paragraph="N154-2"><span class="qr-step">12.2 · Fields and relationships</span>DPTR describes data and MPTR metadata, each ordered by LBA. PRP-form metadata uses physically contiguous memory; SGL metadata follows PSDT and support requirements.</p>
<p class="qr-explanation" data-paragraph="N154-3"><span class="qr-step">12.3 · Interpretation and example</span>Two blocks of 4096+8 bytes require 8192 data bytes and 16 separate metadata bytes. Merely pointing MPTR after byte 8192 of a data allocation does not create valid metadata; it must describe the prepared metadata storage.</p>
<p class="qr-tags">Search terms: MPTR · separate metadata · DPTR · metadata buffer</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a><a href="/nvme/figure-reference/io/en/#figure-n153">NVM Command Set 1.3 Figure 153 · Metadata – Contiguous with LBA Data, Forming Extended LBA</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n155" data-figure="N155">
<h2><span class="qr-number">13</span>16b Guard Protection Information Format when STS field is cleared to 0h</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 155 · 16b Guard Protection Information Format when STS field is cleared to 0h</p>
<p class="qr-location">§5.3.1.1 · Printed pages 131 · PDF 131</p>
<p class="qr-explanation" data-paragraph="N155-1"><span class="qr-step">13.1 · Use</span>This layout applies to 16-bit Guard PI with STS=0 and is useful for checking offsets and byte order. It is not a universal PI layout.</p>
<p class="qr-explanation" data-paragraph="N155-2"><span class="qr-step">13.2 · Fields and relationships</span>Guard occupies bytes 0–1, Application Tag 2–3 and Reference Tag 4–7. MSB at the lower byte position means these multibyte PI fields use most-significant byte first, unlike ordinary little-endian NVMe fields.</p>
<p class="qr-explanation" data-paragraph="N155-3"><span class="qr-step">13.3 · Interpretation and example</span>Reference Tag 00000001h is stored 00 00 00 01 here, not 01 00 00 00. For nonzero STS, use the Storage/Reference split instead of assuming all 32 bits remain Reference Tag.</p>
<p class="qr-tags">Search terms: 16b Guard · Application Tag · Reference Tag · STS 0 · PI endian</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-n128">NVM Command Set 1.3 Figure 128 · Extended LBA Format Data Structure, NVM Command Set Specific</a><a href="/nvme/figure-reference/io/en/#figure-n174">NVM Command Set 1.3 Figure 174 · Write Command 16b Guard Protection Information Processing</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n157" data-figure="N157">
<h2><span class="qr-number">14</span>32b Guard Protection Information Format</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 157 · 32b Guard Protection Information Format</p>
<p class="qr-location">§5.3.1.2 · Printed pages 133 · PDF 133</p>
<p class="qr-explanation" data-paragraph="N157-1"><span class="qr-step">14.1 · Use</span>Use this figure to distinguish 32-bit and 64-bit Guard layouts even though both occupy 16 PI bytes. Changing Guard width also moves later fields.</p>
<p class="qr-explanation" data-paragraph="N157-2"><span class="qr-step">14.2 · Fields and relationships</span>Guard is bytes 0–3, Application Tag 4–5 and the 80-bit Storage/Reference space 6–15. ELBAF.STS determines the split of that final space.</p>
<p class="qr-explanation" data-paragraph="N157-3"><span class="qr-step">14.3 · Interpretation and example</span>With STS=16, its high 16 bits are Storage Tag and the remaining 64 bits Reference Tag. Applying the 64-bit Guard layout would misplace even the Application Tag.</p>
<p class="qr-tags">Search terms: 32b Guard · PI layout · Storage and Reference Space</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-n128">NVM Command Set 1.3 Figure 128 · Extended LBA Format Data Structure, NVM Command Set Specific</a><a href="/nvme/figure-reference/io/en/#figure-n159">NVM Command Set 1.3 Figure 159 · 64b Guard Protection Information Format</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n159" data-figure="N159">
<h2><span class="qr-number">15</span>64b Guard Protection Information Format</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 159 · 64b Guard Protection Information Format</p>
<p class="qr-location">§5.3.1.3 · Printed pages 134 · PDF 134</p>
<p class="qr-explanation" data-paragraph="N159-1"><span class="qr-step">15.1 · Use</span>Decode 64-bit Guard PI with this layout rather than assuming every field becomes 64 bits. The entire PI remains 16 bytes.</p>
<p class="qr-explanation" data-paragraph="N159-2"><span class="qr-step">15.2 · Fields and relationships</span>Guard occupies bytes 0–7, Application Tag 8–9 and the 48-bit Storage/Reference space 10–15. Follow the MSB/LSB byte ordering and use STS for the tag split.</p>
<p class="qr-explanation" data-paragraph="N159-3"><span class="qr-step">15.3 · Interpretation and example</span>STS=0 leaves all 48 bits for Reference Tag; STS=48 uses all of them for Storage Tag with no Reference Tag. Absence of a field is not the same as a field whose value is zero.</p>
<p class="qr-tags">Search terms: 64b Guard · PI layout · Storage Tag · Reference Tag</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-n128">NVM Command Set 1.3 Figure 128 · Extended LBA Format Data Structure, NVM Command Set Specific</a><a href="/nvme/figure-reference/io/en/#figure-n157">NVM Command Set 1.3 Figure 157 · 32b Guard Protection Information Format</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n174" data-figure="N174">
<h2><span class="qr-number">16</span>Write Command 16b Guard Protection Information Processing</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 174 · Write Command 16b Guard Protection Information Processing</p>
<p class="qr-location">§5.3.2.1 · Printed pages 143 · PDF 143</p>
<p class="qr-explanation" data-paragraph="N174-1"><span class="qr-step">16.1 · Use</span>These four 16-bit-Guard scenarios compare host buffers with media format, particularly useful for transfer-length mismatches after enabling PI.</p>
<p class="qr-explanation" data-paragraph="N174-2"><span class="qr-step">16.2 · Fields and relationships</span>With PRACT=0 the host transfers metadata including PI. With PRACT=1 and exactly 8 metadata bytes, those bytes are not transferred by the host and the controller generates PI. When metadata exceeds 8 bytes, its host-side size remains unchanged; do not always subtract eight.</p>
<p class="qr-explanation" data-paragraph="N174-3"><span class="qr-step">16.3 · Interpretation and example</span>For 4096 data bytes, 8 metadata bytes and PRACT=1, the host supplies data only. With 16 metadata bytes, retain the 16-byte metadata transfer layout. PRCHK controls checks; PRACT alone does not disable every check.</p>
<p class="qr-tags">Search terms: PRACT · Write PI · MD 8 · MD 16 · 16b Guard</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/io/en/#figure-n175">NVM Command Set 1.3 Figure 175 · Read 16b Guard Command Protection Information Processing</a><a href="/nvme/figure-reference/io/en/#figure-n71">NVM Command Set 1.3 Figure 71 · Write – Command Dword 12</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n175" data-figure="N175">
<h2><span class="qr-number">17</span>Read 16b Guard Command Protection Information Processing</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 175 · Read 16b Guard Command Protection Information Processing</p>
<p class="qr-location">§5.3.2.2 · Printed pages 145 · PDF 145</p>
<p class="qr-explanation" data-paragraph="N175-1"><span class="qr-step">17.1 · Use</span>Follow NVM→controller→host in this Read diagram. It complements the Write flow and helps verify whether returned metadata was omitted from or double-counted in buffer sizing.</p>
<p class="qr-explanation" data-paragraph="N175-2"><span class="qr-step">17.2 · Fields and relationships</span>PRACT=0 returns full metadata. PRACT=1 with exactly 8 metadata bytes removes PI from the host transfer. Metadata larger than 8 bytes retains its original size; controller PI processing does not imply that the host receives no metadata.</p>
<p class="qr-explanation" data-paragraph="N175-3"><span class="qr-step">17.3 · Interpretation and example</span>For 16 metadata bytes, allocating only data capacity may be insufficient even with PRACT=1. Determine the transfer form here, then use namespace metadata placement to configure DPTR/MPTR.</p>
<p class="qr-tags">Search terms: PRACT · Read PI · metadata transfer · 16b Guard</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/io/en/#figure-n174">NVM Command Set 1.3 Figure 174 · Write Command 16b Guard Protection Information Processing</a><a href="/nvme/figure-reference/io/en/#figure-n54">NVM Command Set 1.3 Figure 54 · Read – Command Dword 12</a><a href="/nvme/figure-reference/io/en/#figure-n154">NVM Command Set 1.3 Figure 154 · Metadata – Transferred as Separate Buffer</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<footer id="source-files"><h2>Source documents</h2><p>Locations refer to the supplied ratified PDFs. For Base, PDF page = printed page +26; the other two use identical page numbers. Original figure numbers and English titles are retained for PDF search. Source PDFs are not redistributed.</p><ul class="qr-sources"><li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li></ul></footer>
</main></div>
