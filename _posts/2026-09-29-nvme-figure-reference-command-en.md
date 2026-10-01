---
layout: "post"
title: "NVMe Figures and Scenarios 02 · Commands, Data Pointers, and Completion Status"
date: "2026-09-29 09:00:00 +0800"
categories: ["nvme"]
tags: ["NVMe", "Reference"]
permalink: "/nvme/figure-reference/command/en/"
nvme_quickref: true
last_modified_at: "2026-10-01"
lang: "en"
description: "NVMe scenarios and source figures: lookup routes, field reasoning, worked answers and precise specification locations."
---

<div class="nvme-quickref">
<nav class="qr-top" aria-label="Editions and index"><a href="#content">Skip to content</a><a href="/nvme/figure-reference/en/">Index</a><a href="/nvme/figure-reference/command/zh-tw/">繁體中文</a><a href="/DOCS/nvme-quick-reference/command.html">Chinese HTML</a></nav>
<main id="content">
<header><p class="qr-eyebrow">LOOKUP · FIELD INTERPRETATION · SOURCE LOCATIONS</p><h1>NVMe Figures and Scenarios 02 · Commands, Data Pointers, and Completion Status</h1><p class="qr-intro">Match the command using SQID/CID before decoding SCT/SC. For data-transfer problems, distinguish PRP pages from SGL addresses, lengths and descriptor types.</p></header>
<aside class="qr-note"><p>Each source figure has a use, field guide and worked interpretation. Example numbers are illustrative, not assumed device settings. Apply the conditions belonging to the field and command.</p><p>Use browser Find for fields, FID, LID, CNS or Figure. Positions follow the source: a byte is 8 bits and a Dword is 4 bytes. An index counts entries; an offset measures displacement from an origin in the specified unit.</p><p>FID (Feature Identifier) selects a feature; LID (Log Page Identifier) selects a log page; CNS (Controller or Namespace Structure) selects the structure returned by Identify.</p></aside>
<nav class="qr-top" aria-label="Volume entry points"><a href="#exercises">Start with scenarios</a><a href="#figure-index">Go to figures</a></nav>
<section id="exercises"><h2>Try the scenarios first</h2>
<p>All observations are hypothetical, not device measurements. Before opening an answer, identify the interface, target, fields and supported conclusion. These are specification exercises; no commands are executed.</p>
<nav class="qr-toc" id="exercise-toc" aria-label="Exercise index"><ol>
<li><a href="#exercise-command-01">Does the same CID twice imply duplicate completion?</a></li>
<li><a href="#exercise-command-02">Which bit does Invalid Field identify?</a></li>
<li><a href="#exercise-command-03">Is PRP2 a data page or a list address?</a></li>
<li><a href="#exercise-command-04">Can correct SGL addresses still describe too little data?</a></li>
<li><a href="#exercise-command-05">Which NUMD retrieves 3 KiB from offset 1024?</a></li>
<li><a href="#exercise-command-06">Does an effects flag prove that a namespace was just created?</a></li>
</ol></nav>
<article class="qr-card qr-case" id="exercise-command-01" data-scenario="command-01"><h3><span class="qr-number">EXERCISE 01</span>Does the same CID twice imply duplicate completion?</h3>
<p class="qr-case-question">A debugger matches commands only by CID and reports two entries with CID=12h as duplicate completions. What is the correct matching order?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>Two new CQEs have SQID=2 and SQID=5, both CID=12h; each SQ has one matching outstanding command.</li>
<li>Another CQ slot has a phase different from the host’s expected phase for this traversal; memory synchronization requirements are satisfied.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Check expected phase → read SQID/CID only from new CQEs → recover the SQE → decode SCT/SC.</p>
<p data-reasoning="command-01-1"><span class="qr-step">Step 1</span>CID uniqueness applies to outstanding commands within an SQ, not a controller-wide permanent sequence. Thus (SQID=2, CID=12h) and (SQID=5, CID=12h) can identify different commands.</p>
<p data-reasoning="command-01-2"><span class="qr-step">Step 2</span>A slot with the wrong phase is not a new completion in this traversal. Scanning CID before phase can mistake previous contents for a duplicate, and the host must update expected phase on CQ wrap.</p>
<p data-reasoning="command-01-3"><span class="qr-step">Step 3</span>Even matching SQID/CID requires lifecycle and timing context across queue recreation or later CID reuse. Preserve complete SQEs/CQEs and queue identity for reliable correlation.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/command/en/#figure-b92">Base 2.4 Figure 92 · Command Dword 0</a><a href="/nvme/figure-reference/command/en/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a><a href="/nvme/figure-reference/command/en/#figure-b98">Base 2.4 Figure 98 · Completion Queue Entry: DW 2</a><a href="/nvme/figure-reference/command/en/#figure-b99">Base 2.4 Figure 99 · Completion Queue Entry: DW 3</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §4.1.1 · Figure 92 · Command Dword 0 · Printed pages 139–140 · PDF 165–166</li><li>Base 2.4 · §4.2.1 · Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets · Printed pages 144 · PDF 170</li><li>Base 2.4 · §4.2.1 · Figure 98 · Completion Queue Entry: DW 2 · Printed pages 144 · PDF 170</li><li>Base 2.4 · §4.2.1 · Figure 99 · Completion Queue Entry: DW 3 · Printed pages 145 · PDF 171</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-command-02" data-scenario="command-02"><h3><span class="qr-number">EXERCISE 02</span>Which bit does Invalid Field identify?</h3>
<p class="qr-case-question">CQE reports Invalid Field in Command. How do you map the Error Information location into a 64-byte SQE?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>SQID/CID identify the same command; Error Information has nonzero ECNT and a valid location, BYTLOC=52, BITLOC=6.</li>
<li>The original SQE, opcode, CSI and full completion status are retained.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Use CQE SCT/SC to identify the error class → Get Log Page LID=01h for the matching entry → map its byte offset into that command’s format.</p>
<p data-reasoning="command-02-1"><span class="qr-step">Step 1</span>Each Dword has four bytes, so byte 52 is the first byte of CDW13; BITLOC=6 identifies CDW13 bit six. BYTLOC is neither a Dword index nor byte 52 of the data buffer.</p>
<p data-reasoning="command-02-2"><span class="qr-step">Step 2</span>Next use opcode and command set to interpret CDW13 and identify the containing field. The common SQE layout supplies a location, not the command-specific meaning of that location.</p>
<p data-reasoning="command-02-3"><span class="qr-step">Step 3</span>A reported location identifies a parameter to inspect, not an instruction to flip that bit. It may contain a reserved value, unsupported choice or invalid combination; a correction requires the command’s conditions.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/logs/en/#figure-b212">Base 2.4 Figure 212 · Error Information Log Entry Data Structure</a><a href="/nvme/figure-reference/command/en/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a><a href="/nvme/figure-reference/command/en/#figure-b103">Base 2.4 Figure 103 · Status Code – Generic Command Status Values</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.13.1.2 · Figure 212 · Error Information Log Entry Data Structure · Printed pages 218–220 · PDF 244–246</li><li>Base 2.4 · §4.1.1 · Figure 93 · Common Command Format · Printed pages 140–142 · PDF 166–168</li><li>Base 2.4 · §4.2.3 · Figure 101 · Completion Queue Entry: Status Field · Printed pages 145–146 · PDF 171–172</li><li>Base 2.4 · §4.2.3.1 · Figure 103 · Status Code – Generic Command Status Values · Printed pages 147–150 · PDF 173–176</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-command-03" data-scenario="command-03"><h3><span class="qr-number">EXERCISE 03</span>Is PRP2 a data page or a list address?</h3>
<p class="qr-case-question">Why can changing transfer length from 5120 to 6144 bytes change the interpretation of PRP2 at the same starting address?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>Current memory page size is 4096 bytes; PRP1 has offset=3072 within its first page and meets alignment requirements.</li>
<li>Data pages are noncontiguous; PRPs are used, with no metadata affecting these lengths.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Read CC.MPS for page size → calculate transfer bytes from command and format → calculate first-page space before interpreting PRP2.</p>
<p data-reasoning="command-03-1"><span class="qr-step">Step 1</span>The first page has 4096−3072=1024 bytes remaining. A 5120-byte transfer leaves exactly 4096 bytes, so PRP2 directly identifies the one additional data page.</p>
<p data-reasoning="command-03-2"><span class="qr-step">Step 2</span>A 6144-byte transfer leaves 5120 bytes requiring two additional data pages. PRP2 then points to a PRP list whose entries identify those pages, rather than directly pointing to the first subsequent data buffer.</p>
<p data-reasoning="command-03-3"><span class="qr-step">Step 3</span>The deciding factor is pages spanned, not whether total length exceeds a fixed constant. Moving the same 6144-byte transfer to a page-aligned start spans only two pages and changes PRP2’s role.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/command/en/#figure-b111">Base 2.4 Figure 111 · PRP Entry – Page Base Address and Offset</a><a href="/nvme/figure-reference/command/en/#figure-b113">Base 2.4 Figure 113 · PRP List Layout for Physically Non-Contiguous Memory Pages</a><a href="/nvme/figure-reference/init/en/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §4.3.1 · Figure 111 · PRP Entry – Page Base Address and Offset · Printed pages 158 · PDF 184</li><li>Base 2.4 · §4.3.1 · Figure 113 · PRP List Layout for Physically Non-Contiguous Memory Pages · Printed pages 159 · PDF 185</li><li>Base 2.4 · §4.3.1 · Printed pages 158–160 · PDF 184–186</li><li>Base 2.4 · §3.1.4.5 · Figure 41 · Offset 14h: CC – Controller Configuration · Printed pages 60–63 · PDF 86–89</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-command-04" data-scenario="command-04"><h3><span class="qr-number">EXERCISE 04</span>Can correct SGL addresses still describe too little data?</h3>
<p class="qr-case-question">Buffer addresses are accessible, but the command has a transfer-length problem. What can descriptor inspection establish before reading memory?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>The command requires 8192 data bytes; its complete SGL contains two valid Data Block descriptors with Length=4096 and 2048.</li>
<li>There are no Bit Bucket, metadata or additional descriptors; support and SGL arrangement are valid.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Compute required bytes from command and LBA format → traverse the complete SGL by descriptor type → sum Data Block lengths.</p>
<p data-reasoning="command-04-1"><span class="qr-step">Step 1</span>The descriptors total 6144 bytes, 2048 short of the required 8192. Address validity identifies where memory is; Length defines the described extent. One cannot substitute for the other.</p>
<p data-reasoning="command-04-2"><span class="qr-step">Step 2</span>A Segment descriptor’s Length describes a segment of descriptors, not payload bytes to add to the data total. Distinguish data descriptors from list-segment descriptors before summing.</p>
<p data-reasoning="command-04-3"><span class="qr-step">Step 3</span>The described payload is insufficient here. Retain actual SCT/SC and compare with SGL validation rules; identifying one length problem does not rule out concurrent format errors.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/command/en/#figure-b114">Base 2.4 Figure 114 · SGL Validation Error Conditions</a><a href="/nvme/figure-reference/command/en/#figure-b116">Base 2.4 Figure 116 · Generic SGL Descriptor Format</a><a href="/nvme/figure-reference/command/en/#figure-b119">Base 2.4 Figure 119 · SGL Data Block descriptor</a><a href="/nvme/figure-reference/command/en/#figure-b121">Base 2.4 Figure 121 · SGL Segment descriptor</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §4.3.2 · Figure 114 · SGL Validation Error Conditions · Printed pages 161 · PDF 187</li><li>Base 2.4 · §4.3.2 · Figure 116 · Generic SGL Descriptor Format · Printed pages 161 · PDF 187</li><li>Base 2.4 · §4.3.2 · Figure 119 · SGL Data Block descriptor · Printed pages 162–163 · PDF 188–189</li><li>Base 2.4 · §4.3.2 · Figure 121 · SGL Segment descriptor · Printed pages 163 · PDF 189</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-command-05" data-scenario="command-05"><h3><span class="qr-number">EXERCISE 05</span>Which NUMD retrieves 3 KiB from offset 1024?</h3>
<p class="qr-case-question">A conventional byte-offset log supports this range. Encode length and starting position separately rather than putting a byte count in NUMD.</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>Required length is 3072 bytes, starting 1024 bytes from the log origin; OT=0, with no special length override.</li>
<li>LID, NSID, CSI, LSP and LSI are correctly selected for the target log.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Get Log Page uses NUMDU/NUMDL for length and LPO with OT for position; first check for log-specific exceptions.</p>
<p data-reasoning="command-05-1"><span class="qr-step">Step 1</span>3072÷4=768 Dwords; subtracting one gives NUMD=767=02FFh, so NUMDU=0 and NUMDL=02FFh. Encoding 3072 directly requests a different Dword count, not 3072 bytes.</p>
<p data-reasoning="command-05-2"><span class="qr-step">Step 2</span>With OT=0, LPO=1024 is a byte offset, yielding bytes 1024–4095. With OT=1 it is a structure index, usable only by supporting logs; the same number does not identify the same position.</p>
<p data-reasoning="command-05-3"><span class="qr-step">Step 3</span>Also choose RAE deliberately because retrieval may acknowledge notifications. Persistent Event Log ACT=3 has a fixed-header rule, so this ordinary length calculation does not control its returned range.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/logs/en/#figure-b204">Base 2.4 Figure 204 · Get Log Page – Command Dword 10</a><a href="/nvme/figure-reference/logs/en/#figure-b205">Base 2.4 Figure 205 · Get Log Page – Command Dword 11</a><a href="/nvme/figure-reference/logs/en/#figure-b208">Base 2.4 Figure 208 · Get Log Page – Command Dword 14</a><a href="/nvme/figure-reference/logs/en/#figure-b232">Base 2.4 Figure 232 · Persistent Event Log Specific Parameter Field</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.13 · Figure 204 · Get Log Page – Command Dword 10 · Printed pages 213 · PDF 239</li><li>Base 2.4 · §5.2.13 · Figure 205 · Get Log Page – Command Dword 11 · Printed pages 214 · PDF 240</li><li>Base 2.4 · §5.2.13 · Figure 208 · Get Log Page – Command Dword 14 · Printed pages 214–215 · PDF 240–241</li><li>Base 2.4 · §5.2.13.1.14 · Figure 232 · Persistent Event Log Specific Parameter Field · Printed pages 246 · PDF 272</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-command-06" data-scenario="command-06"><h3><span class="qr-number">EXERCISE 06</span>Does an effects flag prove that a namespace was just created?</h3>
<p class="qr-case-question">After an operation, a tool increments its namespace count solely because NIC=1. Is that interpreting capability data or history?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>Commands Supported and Effects reports CSUPP=1 and NIC=1 for the target Admin opcode.</li>
<li>A command with that opcode completed, but its action, status and updated Identify lists were not retained.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Get Log Page LID=05h for the correct Admin/I/O opcode table; then obtain the actual request/completion and refresh Identify where necessary.</p>
<p data-reasoning="command-06-1"><span class="qr-step">Step 1</span>CSUPP reports support and NIC possible namespace-inventory change. Neither is an event timeline nor proof of success or a Create action in this execution.</p>
<p data-reasoning="command-06-2"><span class="qr-step">Step 2</span>Use the action and completion status to decide when to refresh allocated/active inventories. Unconditionally adding one corrupts cached inventory for Delete, failed Create or non-changing operations.</p>
<p data-reasoning="command-06-3"><span class="qr-step">Step 3</span>Interpret I/O opcodes in the correct command set. The same numeric opcode in another table need not name the same command; effects scope and coordination rules do not replace outcome evidence.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/logs/en/#figure-b217">Base 2.4 Figure 217 · Commands Supported and Effects Data Structure</a><a href="/nvme/figure-reference/identify/en/#figure-b336">Base 2.4 Figure 336 · Identify – CNS Values</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.13.1.6 · Figure 217 · Commands Supported and Effects Data Structure · Printed pages 228–229 · PDF 254–255</li><li>Base 2.4 · §5.2.14 · Figure 336 · Identify – CNS Values · Printed pages 338–339 · PDF 364–365</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
</section>
<nav class="qr-toc" id="figure-index" aria-label="Volume figure index"><h2>Figures in this volume</h2><ol>
<li><a href="#figure-b92">Base 2.4 Figure 92 · Command Dword 0</a></li>
<li><a href="#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></li>
<li><a href="#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
<li><a href="#figure-b98">Base 2.4 Figure 98 · Completion Queue Entry: DW 2</a></li>
<li><a href="#figure-b99">Base 2.4 Figure 99 · Completion Queue Entry: DW 3</a></li>
<li><a href="#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="#figure-b102">Base 2.4 Figure 102 · Status Code – Status Code Type Values</a></li>
<li><a href="#figure-b103">Base 2.4 Figure 103 · Status Code – Generic Command Status Values</a></li>
<li><a href="#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="#figure-b107">Base 2.4 Figure 107 · Status Code – Media and Data Integrity Error Values</a></li>
<li><a href="#figure-b110">Base 2.4 Figure 110 · PRP Entry Layout</a></li>
<li><a href="#figure-b111">Base 2.4 Figure 111 · PRP Entry – Page Base Address and Offset</a></li>
<li><a href="#figure-b113">Base 2.4 Figure 113 · PRP List Layout for Physically Non-Contiguous Memory Pages</a></li>
<li><a href="#figure-b114">Base 2.4 Figure 114 · SGL Validation Error Conditions</a></li>
<li><a href="#figure-b116">Base 2.4 Figure 116 · Generic SGL Descriptor Format</a></li>
<li><a href="#figure-b119">Base 2.4 Figure 119 · SGL Data Block descriptor</a></li>
<li><a href="#figure-b121">Base 2.4 Figure 121 · SGL Segment descriptor</a></li>
<li><a href="#figure-b122">Base 2.4 Figure 122 · SGL Last Segment descriptor</a></li>
<li><a href="#figure-n18">NVM Command Set 1.3 Figure 18 · Status Code – Generic Command Status Values</a></li>
<li><a href="#figure-n19">NVM Command Set 1.3 Figure 19 · Status Code – Command Specific Status Values</a></li>
<li><a href="#figure-n20">NVM Command Set 1.3 Figure 20 · Status Code – Media and Data Integrity Error Values</a></li>
</ol></nav>
<article class="qr-card" id="figure-b92" data-figure="B92">
<h2><span class="qr-number">01</span>Command Dword 0</h2>
<p class="qr-original">Base 2.4 · Figure 92 · Command Dword 0</p>
<p class="qr-location">§4.1.1 · Printed pages 139–140 · PDF 165–166</p>
<p class="qr-explanation" data-paragraph="B92-1"><span class="qr-step">01.1 · Use</span>Start a submission-entry decode with CDW0: command identity, opcode and pointer format. CID identifies an outstanding command uniquely only together with its SQID.</p>
<p class="qr-explanation" data-paragraph="B92-2"><span class="qr-step">01.2 · Fields and relationships</span>CID occupies bits 31:16, PSDT bits 15:14, FUSE bits 9:8 and OPC bits 7:0. PSDT=00b uses PRPs; 01b/10b use SGLs with different metadata-pointer interpretations. PCIe Admin commands use PRPs. FUSE identifies ordinary operations or the first/second fused command.</p>
<p class="qr-explanation" data-paragraph="B92-3"><span class="qr-step">01.3 · Interpretation and example</span>The same DPTR bytes may represent two PRP pointers or one SGL descriptor depending on PSDT. A plausible address alone does not validate the decode; check PSDT and the command’s permitted format first.</p>
<p class="qr-tags">Search terms: CDW0 · OPC · CID · PSDT · FUSE</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a><a href="/nvme/figure-reference/command/en/#figure-b98">Base 2.4 Figure 98 · Completion Queue Entry: DW 2</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b93" data-figure="B93">
<h2><span class="qr-number">02</span>Common Command Format</h2>
<p class="qr-original">Base 2.4 · Figure 93 · Common Command Format</p>
<p class="qr-location">§4.1.1 · Printed pages 140–142 · PDF 166–168</p>
<p class="qr-explanation" data-paragraph="B93-1"><span class="qr-step">02.1 · Use</span>This is the byte map for the common 64-byte command. It separates common fields from positions whose definitions belong to individual commands.</p>
<p class="qr-explanation" data-paragraph="B93-2"><span class="qr-step">02.2 · Fields and relationships</span>CDW0 is bytes 3:0, NSID bytes 7:4, CDW2/3 15:8, MPTR bytes 23:16, DPTR bytes 39:24 and CDW10–15 63:40. In PRP mode DPTR contains PRP1/PRP2; PRP2 is reserved, a second-page pointer or a list pointer according to page-boundary crossings.</p>
<p class="qr-explanation" data-paragraph="B93-3"><span class="qr-step">02.3 · Interpretation and example</span>With 4 KiB pages, initial offset 512 and 8192 transferred bytes, three data pages are needed. PRP2 therefore points to a list rather than the second data page. Also, NSID=FFFFFFFFh is not a universally accepted broadcast value.</p>
<p class="qr-tags">Search terms: SQE · NSID · MPTR · DPTR · CDW10 · PRP2</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b92">Base 2.4 Figure 92 · Command Dword 0</a><a href="/nvme/figure-reference/command/en/#figure-b111">Base 2.4 Figure 111 · PRP Entry – Page Base Address and Offset</a><a href="/nvme/figure-reference/command/en/#figure-b113">Base 2.4 Figure 113 · PRP List Layout for Physically Non-Contiguous Memory Pages</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b97" data-figure="B97">
<h2><span class="qr-number">03</span>Common Completion Queue Entry Layout – Admin and All I/O Command Sets</h2>
<p class="qr-original">Base 2.4 · Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</p>
<p class="qr-location">§4.2.1 · Printed pages 144 · PDF 170</p>
<p class="qr-explanation" data-paragraph="B97-1"><span class="qr-step">03.1 · Use</span>Use this layout to separate command-specific results, queue information, command identity and status. The common format is at least 16 bytes; this figure describes its first 16.</p>
<p class="qr-explanation" data-paragraph="B97-2"><span class="qr-step">03.2 · Fields and relationships</span>DW0/DW1 are command-specific, not universally zero or status fields. DW2 contains SQID/SQHD; DW3 contains STATUS, P and CID. P is the phase tag identifying new entries in the circular CQ.</p>
<p class="qr-explanation" data-paragraph="B97-3"><span class="qr-step">03.3 · Interpretation and example</span>Get Features may return a feature value in DW0; Namespace Management may return a new NSID there. Decode those through their command definitions and determine completion status from DW3.</p>
<p class="qr-tags">Search terms: CQE · DW0 · DW1 · DW2 · DW3</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b98">Base 2.4 Figure 98 · Completion Queue Entry: DW 2</a><a href="/nvme/figure-reference/command/en/#figure-b99">Base 2.4 Figure 99 · Completion Queue Entry: DW 3</a><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b98" data-figure="B98">
<h2><span class="qr-number">04</span>Completion Queue Entry: DW 2</h2>
<p class="qr-original">Base 2.4 · Figure 98 · Completion Queue Entry: DW 2</p>
<p class="qr-location">§4.2.1 · Printed pages 144 · PDF 170</p>
<p class="qr-explanation" data-paragraph="B98-1"><span class="qr-step">04.1 · Use</span>When several SQs share a CQ, SQID identifies the source queue. SQHD tells the host which submission positions the controller has consumed.</p>
<p class="qr-explanation" data-paragraph="B98-2"><span class="qr-step">04.2 · Fields and relationships</span>SQID occupies bits 31:16 and SQHD bits 15:0. SQID plus DW3.CID identifies the command. SQHD snapshots the SQ head when the CQE was created; it is not the completed command’s SQ index.</p>
<p class="qr-explanation" data-paragraph="B98-3"><span class="qr-step">04.3 · Interpretation and example</span>SQHD=12 does not mean CID=12 completed or that the current controller head remains 12. Track reusable submission slots separately from command completion because completion order can differ.</p>
<p class="qr-tags">Search terms: SQID · SQHD · CQE DW2</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b99">Base 2.4 Figure 99 · Completion Queue Entry: DW 3</a><a href="/nvme/figure-reference/init/en/#figure-p5">PCIe Transport 1.4 Figure 5 · Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL – Submission Queue y Tail Doorbell</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b99" data-figure="B99">
<h2><span class="qr-number">05</span>Completion Queue Entry: DW 3</h2>
<p class="qr-original">Base 2.4 · Figure 99 · Completion Queue Entry: DW 3</p>
<p class="qr-location">§4.2.1 · Printed pages 145 · PDF 171</p>
<p class="qr-explanation" data-paragraph="B99-1"><span class="qr-step">05.1 · Use</span>During CQ scanning, this table separates freshness from command identity and outcome. P is not a success flag.</p>
<p class="qr-explanation" data-paragraph="B99-2"><span class="qr-step">05.2 · Fields and relationships</span>CID occupies bits 15:0, P bit 16 and STATUS bits 31:17. Compare P with the phase expected for the current CQ cycle. If a CQE is written through multiple writes, its phase bit must be updated in the final write.</p>
<p class="qr-explanation" data-paragraph="B99-3"><span class="qr-step">05.3 · Interpretation and example</span>After confirming the expected phase, match SQID/CID and decode status. P=1 alone does not establish freshness because the expected value changes on CQ wraparound.</p>
<p class="qr-tags">Search terms: CID · P · Phase Tag · STATUS · CQE DW3</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b98">Base 2.4 Figure 98 · Completion Queue Entry: DW 2</a><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b101" data-figure="B101">
<h2><span class="qr-number">06</span>Completion Queue Entry: Status Field</h2>
<p class="qr-original">Base 2.4 · Figure 101 · Completion Queue Entry: Status Field</p>
<p class="qr-location">§4.2.3 · Printed pages 145–146 · PDF 171–172</p>
<p class="qr-explanation" data-paragraph="B101-1"><span class="qr-step">06.1 · Use</span>For unsuccessful completions, split status here before choosing a code table. Figure bit positions are relative to the complete CQE DW3, not an already shifted 15-bit STATUS value.</p>
<p class="qr-explanation" data-paragraph="B101-2"><span class="qr-step">06.2 · Fields and relationships</span>DNR bit 31 predicts failure of resubmitting the same command; M bit 30 indicates extra Error Information. CRD bits 29:28 selects retry delay, SCT bits 27:25 gives the category and SC bits 24:17 the code. CRD applies only with DNR=0 and ACRE=1 in Host Behavior Support.</p>
<p class="qr-explanation" data-paragraph="B101-3"><span class="qr-step">06.3 · Interpretation and example</span>DW3=8005002Ah decodes to DNR=1, SCT=0, SC=02h, P=1 and CID=002Ah: generic Invalid Field in Command. Do not interpret 02h without its category. Conversely, DNR=0 does not guarantee a successful retry.</p>
<p class="qr-tags">Search terms: SCT · SC · DNR · M · CRD · ACRE</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b102">Base 2.4 Figure 102 · Status Code – Status Code Type Values</a><a href="/nvme/figure-reference/command/en/#figure-b103">Base 2.4 Figure 103 · Status Code – Generic Command Status Values</a><a href="/nvme/figure-reference/logs/en/#figure-b212">Base 2.4 Figure 212 · Error Information Log Entry Data Structure</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b102" data-figure="B102">
<h2><span class="qr-number">07</span>Status Code – Status Code Type Values</h2>
<p class="qr-original">Base 2.4 · Figure 102 · Status Code – Status Code Type Values</p>
<p class="qr-location">§4.2.3 · Printed pages 146 · PDF 172</p>
<p class="qr-explanation" data-paragraph="B102-1"><span class="qr-step">07.1 · Use</span>This table routes a status lookup. Identical SC values can mean entirely different things under different SCT values.</p>
<p class="qr-explanation" data-paragraph="B102-2"><span class="qr-step">07.2 · Fields and relationships</span>SCT=0 is generic, 1 command-specific, 2 media/data integrity, 3 path-related and 7 vendor-specific; 4–6 are reserved. The Reference column leads to the corresponding Base section, with additional command-set definitions where applicable.</p>
<p class="qr-explanation" data-paragraph="B102-3"><span class="qr-step">07.3 · Interpretation and example</span>For NVM commands, SC=80h with SCT=0 means LBA Out of Range; SC=80h with SCT=1 means Conflicting Attributes. A tool displaying only 80h has not provided enough information.</p>
<p class="qr-tags">Search terms: SCT · Generic · Command Specific · Media · Path Related</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-n18">NVM Command Set 1.3 Figure 18 · Status Code – Generic Command Status Values</a><a href="/nvme/figure-reference/command/en/#figure-n19">NVM Command Set 1.3 Figure 19 · Status Code – Command Specific Status Values</a><a href="/nvme/figure-reference/command/en/#figure-b107">Base 2.4 Figure 107 · Status Code – Media and Data Integrity Error Values</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b103" data-figure="B103">
<h2><span class="qr-number">08</span>Status Code – Generic Command Status Values</h2>
<p class="qr-original">Base 2.4 · Figure 103 · Status Code – Generic Command Status Values</p>
<p class="qr-location">§4.2.3.1 · Printed pages 147–150 · PDF 173–176</p>
<p class="qr-explanation" data-paragraph="B103-1"><span class="qr-step">08.1 · Use</span>For SCT=0, look up generic opcode, field, namespace, transfer and sequencing outcomes here. This is not the complete list of I/O-specific errors.</p>
<p class="qr-explanation" data-paragraph="B103-2"><span class="qr-step">08.2 · Fields and relationships</span>Value is SC; Definition describes the condition. Common entries include 00h success, 01h invalid opcode, 02h invalid field and 0Bh invalid namespace or format. Similar names do not imply identical conditions; inactive and invalid NSIDs are distinct.</p>
<p class="qr-explanation" data-paragraph="B103-3"><span class="qr-step">08.3 · Interpretation and example</span>For 02h, inspect command fields and their validity conditions, then use M and Parameter Error Location in Error Information to narrow the location. Not every 02h is an NSID error.</p>
<p class="qr-tags">Search terms: generic status · Invalid Field · Invalid Namespace · SC</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/logs/en/#figure-b212">Base 2.4 Figure 212 · Error Information Log Entry Data Structure</a><a href="/nvme/figure-reference/command/en/#figure-n18">NVM Command Set 1.3 Figure 18 · Status Code – Generic Command Status Values</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b104" data-figure="B104">
<h2><span class="qr-number">09</span>Status Code – Command Specific Status Values</h2>
<p class="qr-original">Base 2.4 · Figure 104 · Status Code – Command Specific Status Values</p>
<p class="qr-location">§4.2.3.2 · Printed pages 151–152 · PDF 177–178</p>
<p class="qr-explanation" data-paragraph="B104-1"><span class="qr-step">09.1 · Use</span>For SCT=1 on Admin operations, start here and then return to the issued command’s definition. Some statuses request further action rather than fitting a simple success/hardware-failure split.</p>
<p class="qr-explanation" data-paragraph="B104-2"><span class="qr-step">09.2 · Fields and relationships</span>The table maps SC to descriptions including invalid queue identifiers or sizes, firmware slot/image problems and activation results requiring reset. Keep the original opcode because command-specific status requires command context.</p>
<p class="qr-explanation" data-paragraph="B104-3"><span class="qr-step">09.3 · Interpretation and example</span>A firmware result requiring reset differs from an invalid image. The former calls for checking activation timing and reset scope; the latter calls for inspecting the image and commit parameters. Repeatedly submitting the same update is not a universal response.</p>
<p class="qr-tags">Search terms: command specific · queue error · firmware status · SCT 1</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/maintenance/en/#figure-b187">Base 2.4 Figure 187 · Firmware Commit – Command Dword 10</a><a href="/nvme/figure-reference/command/en/#figure-n19">NVM Command Set 1.3 Figure 19 · Status Code – Command Specific Status Values</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b107" data-figure="B107">
<h2><span class="qr-number">10</span>Status Code – Media and Data Integrity Error Values</h2>
<p class="qr-original">Base 2.4 · Figure 107 · Status Code – Media and Data Integrity Error Values</p>
<p class="qr-location">§4.2.3.3 · Printed pages 154–155 · PDF 180–181</p>
<p class="qr-explanation" data-paragraph="B107-1"><span class="qr-step">10.1 · Use</span>For SCT=2, separate media read/write failures from protection-check failures. A protection mismatch does not by itself establish physical NAND damage.</p>
<p class="qr-explanation" data-paragraph="B107-2"><span class="qr-step">10.2 · Fields and relationships</span>The codes include Write Fault, Unrecovered Read and Guard, Application Tag or Reference Tag checks. Preserve the specific failure category and correlate namespace format, command check controls and expected tags.</p>
<p class="qr-explanation" data-paragraph="B107-3"><span class="qr-step">10.3 · Interpretation and example</span>For a Reference Tag failure, inspect the starting LBA, PI type and tag configuration. Reducing it to “read error” discards useful evidence. NVM adds Compare Failure and deallocated/unwritten-block codes.</p>
<p class="qr-tags">Search terms: SCT 2 · Guard · Application Tag · Reference Tag · Media Error</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-n20">NVM Command Set 1.3 Figure 20 · Status Code – Media and Data Integrity Error Values</a><a href="/nvme/figure-reference/io/en/#figure-n155">NVM Command Set 1.3 Figure 155 · 16b Guard Protection Information Format when STS field is cleared to 0h</a><a href="/nvme/figure-reference/io/en/#figure-n174">NVM Command Set 1.3 Figure 174 · Write Command 16b Guard Protection Information Processing</a><a href="/nvme/figure-reference/io/en/#figure-n175">NVM Command Set 1.3 Figure 175 · Read 16b Guard Command Protection Information Processing</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b110" data-figure="B110">
<h2><span class="qr-number">11</span>PRP Entry Layout</h2>
<p class="qr-original">Base 2.4 · Figure 110 · PRP Entry Layout</p>
<p class="qr-location">§4.3.1 · Printed pages 158 · PDF 184</p>
<p class="qr-explanation" data-paragraph="B110-1"><span class="qr-step">11.1 · Use</span>This bit diagram explains the split within a PRP address. An offset counts bytes from the page start, not PRP entries.</p>
<p class="qr-explanation" data-paragraph="B110-2"><span class="qr-step">11.2 · Fields and relationships</span>Upper bits hold the page base; the lower n+1 bits hold the page offset. CC.MPS determines the split:12 low bits for 4 KiB pages and 13 for 8 KiB. A fixed FFFh mask is not valid for every configuration.</p>
<p class="qr-explanation" data-paragraph="B110-3"><span class="qr-step">11.3 · Interpretation and example</span>Address 12345000h has offset zero with 4 KiB pages but 1000h with 8 KiB pages. Its validity also depends on the PRP’s role in the command or list.</p>
<p class="qr-tags">Search terms: PRP · Page Base Address · offset · CC.MPS</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b111">Base 2.4 Figure 111 · PRP Entry – Page Base Address and Offset</a><a href="/nvme/figure-reference/init/en/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b111" data-figure="B111">
<h2><span class="qr-number">12</span>PRP Entry – Page Base Address and Offset</h2>
<p class="qr-original">Base 2.4 · Figure 111 · PRP Entry – Page Base Address and Offset</p>
<p class="qr-location">§4.3.1 · Printed pages 158 · PDF 184</p>
<p class="qr-explanation" data-paragraph="B111-1"><span class="qr-step">12.1 · Use</span>Use this definition and its following text to distinguish alignment rules for the initial data pointer, a PRP-list pointer and data-page pointers inside a list.</p>
<p class="qr-explanation" data-paragraph="B111-2"><span class="qr-step">12.2 · Fields and relationships</span>PBAO spans 64 bits. A PRP offset is at least Dword-aligned. The initial data PRP may permit a nonzero offset, while list data-page entries are page-aligned. The initial list pointer must be 8-byte-aligned; subsequent list pages are page-aligned.</p>
<p class="qr-explanation" data-paragraph="B111-3"><span class="qr-step">12.3 · Interpretation and example</span>With 4 KiB pages, 200004h may be valid as an initial data PRP but is not page-aligned for an entry inside the list. Checking only the bottom two bits is insufficient.</p>
<p class="qr-tags">Search terms: PBAO · PRP1 · PRP2 · alignment</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b110">Base 2.4 Figure 110 · PRP Entry Layout</a><a href="/nvme/figure-reference/command/en/#figure-b113">Base 2.4 Figure 113 · PRP List Layout for Physically Non-Contiguous Memory Pages</a><a href="/nvme/figure-reference/command/en/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b113" data-figure="B113">
<h2><span class="qr-number">13</span>PRP List Layout for Physically Non-Contiguous Memory Pages</h2>
<p class="qr-original">Base 2.4 · Figure 113 · PRP List Layout for Physically Non-Contiguous Memory Pages</p>
<p class="qr-location">§4.3.1 · Printed pages 159 · PDF 185</p>
<p class="qr-explanation" data-paragraph="B113-1"><span class="qr-step">13.1 · Use</span>This diagram shows a PRP list describing physically noncontiguous pages. Logical data continuity does not require consecutive physical addresses.</p>
<p class="qr-explanation" data-paragraph="B113-2"><span class="qr-step">13.2 · Fields and relationships</span>Each entry is 8 bytes; data-page addresses have zero page offset. Entries are packed from entry 0. If another list page is needed, the final entry points to that page rather than to data.</p>
<p class="qr-explanation" data-paragraph="B113-3"><span class="qr-step">13.3 · Interpretation and example</span>A4 KiB list page holds 512 eight-byte entries. With chaining, the last entry is a link, leaving at most 511 data-page addresses on that page. Do not count the list-page address as transferred data.</p>
<p class="qr-tags">Search terms: PRP List · page chain · non-contiguous</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a><a href="/nvme/figure-reference/command/en/#figure-b111">Base 2.4 Figure 111 · PRP Entry – Page Base Address and Offset</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b114" data-figure="B114">
<h2><span class="qr-number">14</span>SGL Validation Error Conditions</h2>
<p class="qr-original">Base 2.4 · Figure 114 · SGL Validation Error Conditions</p>
<p class="qr-location">§4.3.2 · Printed pages 161 · PDF 187</p>
<p class="qr-explanation" data-paragraph="B114-1"><span class="qr-step">14.1 · Use</span>Consult this condition-to-status table when apparently valid SGL addresses are rejected. It checks descriptor arrangement and types, not just buffer length.</p>
<p class="qr-explanation" data-paragraph="B114-2"><span class="qr-step">14.2 · Fields and relationships</span>A Segment/Last Segment descriptor before a segment’s final position yields Invalid Number of SGL Descriptors. A link descriptor inside the final segment yields Invalid SGL Segment Descriptor. Unsupported types or type/subtype combinations yield SGL Descriptor Type Invalid.</p>
<p class="qr-explanation" data-paragraph="B114-3"><span class="qr-step">14.3 · Interpretation and example</span>If descriptor 2 of 3 is a Segment descriptor followed by a Data Block, the link is in the wrong position. Enlarging the third descriptor’s data buffer does not repair that structural error.</p>
<p class="qr-tags">Search terms: SGL validation · Invalid Number of SGL Descriptors · Invalid SGL Segment Descriptor</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b116">Base 2.4 Figure 116 · Generic SGL Descriptor Format</a><a href="/nvme/figure-reference/command/en/#figure-b121">Base 2.4 Figure 121 · SGL Segment descriptor</a><a href="/nvme/figure-reference/command/en/#figure-b122">Base 2.4 Figure 122 · SGL Last Segment descriptor</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b116" data-figure="B116">
<h2><span class="qr-number">15</span>Generic SGL Descriptor Format</h2>
<p class="qr-original">Base 2.4 · Figure 116 · Generic SGL Descriptor Format</p>
<p class="qr-location">§4.3.2 · Printed pages 161 · PDF 187</p>
<p class="qr-explanation" data-paragraph="B116-1"><span class="qr-step">15.1 · Use</span>An SGL descriptor is 16 bytes. Inspect its last byte before interpreting the first 15; the first eight bytes are not always a user-data address.</p>
<p class="qr-explanation" data-paragraph="B116-2"><span class="qr-step">15.2 · Fields and relationships</span>Byte 15 is SGLID: bits 7:4 selects type and bits 3:0 subtype. Bytes 14:0 are type-specific. Common Data Block, Segment and Last Segment types are 0, 2 and 3.</p>
<p class="qr-explanation" data-paragraph="B116-3"><span class="qr-step">15.3 · Interpretation and example</span>SGLID=30h means type 3/subtype 0: its address points to the final descriptor segment rather than directly to data. Supported types still depend on Identify and PCIe applicability.</p>
<p class="qr-tags">Search terms: SGLID · SGLDT · SGLDST · descriptor</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b119">Base 2.4 Figure 119 · SGL Data Block descriptor</a><a href="/nvme/figure-reference/command/en/#figure-b121">Base 2.4 Figure 121 · SGL Segment descriptor</a><a href="/nvme/figure-reference/command/en/#figure-b122">Base 2.4 Figure 122 · SGL Last Segment descriptor</a><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b119" data-figure="B119">
<h2><span class="qr-number">16</span>SGL Data Block descriptor</h2>
<p class="qr-original">Base 2.4 · Figure 119 · SGL Data Block descriptor</p>
<p class="qr-location">§4.3.2 · Printed pages 162–163 · PDF 188–189</p>
<p class="qr-explanation" data-paragraph="B119-1"><span class="qr-step">16.1 · Use</span>Decode actual data-buffer extents here. For the PCIe memory-address use covered by this series, ADDR is the buffer start and LEN its length.</p>
<p class="qr-explanation" data-paragraph="B119-2"><span class="qr-step">16.2 · Fields and relationships</span>ADDR is bytes 7:0, LEN bytes 11:8, bytes 12–14 reserved, and byte 15 has type 0. LEN counts bytes directly; zero describes a valid zero-length transfer. Alignment and granularity depend on Identify.SGLS.</p>
<p class="qr-explanation" data-paragraph="B119-3"><span class="qr-step">16.3 · Interpretation and example</span>LEN=4096 means 4096 bytes, without the NLB plus-one rule. If four-byte granularity is required, both ADDR and LEN must comply; aligning the address does not make a 4097-byte length valid.</p>
<p class="qr-tags">Search terms: SGL Data Block · ADDR · LEN · SGLS</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b116">Base 2.4 Figure 116 · Generic SGL Descriptor Format</a><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b121" data-figure="B121">
<h2><span class="qr-number">17</span>SGL Segment descriptor</h2>
<p class="qr-original">Base 2.4 · Figure 121 · SGL Segment descriptor</p>
<p class="qr-location">§4.3.2 · Printed pages 163 · PDF 189</p>
<p class="qr-explanation" data-paragraph="B121-1"><span class="qr-step">17.1 · Use</span>A Segment descriptor links to another SGL segment when one descriptor cannot describe the transfer. Its length measures descriptor storage, not the data buffer.</p>
<p class="qr-explanation" data-paragraph="B121-2"><span class="qr-step">17.2 · Fields and relationships</span>ADDR bytes 7:0 points to the next segment; LEN bytes 11:8 must be nonzero and a multiple of 16; byte 15 has type 2. The link descriptor must be last in its containing segment.</p>
<p class="qr-explanation" data-paragraph="B121-3"><span class="qr-step">17.3 · Interpretation and example</span>LEN=48 means three 16-byte descriptors in the next segment, not a 48-byte data transfer. Obtain the actual transfer extent from data descriptors.</p>
<p class="qr-tags">Search terms: SGL Segment · type 2 · LEN · ADDR</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b114">Base 2.4 Figure 114 · SGL Validation Error Conditions</a><a href="/nvme/figure-reference/command/en/#figure-b119">Base 2.4 Figure 119 · SGL Data Block descriptor</a><a href="/nvme/figure-reference/command/en/#figure-b122">Base 2.4 Figure 122 · SGL Last Segment descriptor</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b122" data-figure="B122">
<h2><span class="qr-number">18</span>SGL Last Segment descriptor</h2>
<p class="qr-original">Base 2.4 · Figure 122 · SGL Last Segment descriptor</p>
<p class="qr-location">§4.3.2 · Printed pages 164 · PDF 190</p>
<p class="qr-explanation" data-paragraph="B122-1"><span class="qr-step">18.1 · Use</span>This descriptor marks the next segment as the final one. “Last” does not mean it directly identifies the last user-data block.</p>
<p class="qr-explanation" data-paragraph="B122-2"><span class="qr-step">18.2 · Fields and relationships</span>ADDR bytes 7:0 and LEN bytes 11:8 describe the next and final descriptor array. LEN is nonzero and a multiple of 16; type is 3. That final segment cannot contain another Segment or Last Segment link.</p>
<p class="qr-explanation" data-paragraph="B122-3"><span class="qr-step">18.3 · Interpretation and example</span>A Last Segment with LEN=32 can point to two Data Block descriptors. If the second is another Segment link, the final-segment constraint is violated; use Figure 114 to identify the error.</p>
<p class="qr-tags">Search terms: SGL Last Segment · type 3 · last segment</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b114">Base 2.4 Figure 114 · SGL Validation Error Conditions</a><a href="/nvme/figure-reference/command/en/#figure-b121">Base 2.4 Figure 121 · SGL Segment descriptor</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n18" data-figure="N18">
<h2><span class="qr-number">19</span>Status Code – Generic Command Status Values</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 18 · Status Code – Generic Command Status Values</p>
<p class="qr-location">§3.1.2 · Printed pages 25 · PDF 25</p>
<p class="qr-explanation" data-paragraph="N18-1"><span class="qr-step">19.1 · Use</span>Use this extension when the Base generic table does not cover the NVM-specific condition. SCT remains 0; the status format is unchanged.</p>
<p class="qr-explanation" data-paragraph="N18-2"><span class="qr-step">19.2 · Fields and relationships</span>SC=14h exceeds an atomic write unit, 1Eh indicates invalid SGL alignment/granularity, 25h an invalid key tag, 80h an LBA beyond namespace size, and 81h utilization exceeding namespace capacity.</p>
<p class="qr-explanation" data-paragraph="N18-3"><span class="qr-step">19.3 · Interpretation and example</span>For 80h, inspect SLBA/NLB and NSZE. For 81h, inspect NUSE/NCAP and allocation context. Address range and allocated-capacity exhaustion require different checks.</p>
<p class="qr-tags">Search terms: SCT 0 · LBA Out of Range · Capacity Exceeded · Atomic Write Unit Exceeded</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a><a href="/nvme/figure-reference/io/en/#figure-n4">NVM Command Set 1.3 Figure 4 · Atomicity Parameters for Single Atomicity Mode</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n19" data-figure="N19">
<h2><span class="qr-number">20</span>Status Code – Command Specific Status Values</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 19 · Status Code – Command Specific Status Values</p>
<p class="qr-location">§3.1.2 · Printed pages 25 · PDF 25</p>
<p class="qr-explanation" data-paragraph="N19-1"><span class="qr-step">20.1 · Use</span>For SCT=1 on NVM commands, this table lists both meanings and affected commands. It helps detect use of the wrong command-set decoder.</p>
<p class="qr-explanation" data-paragraph="N19-2"><span class="qr-step">20.2 · Fields and relationships</span>80h is Conflicting Attributes, 81h Invalid Protection Information and 82h Attempted Write to Read Only Range. Copy adds size-limit 83h, incompatible-format 85h, fast-copy 86h, overlapping-range 87h and insufficient-resource 89h outcomes.</p>
<p class="qr-explanation" data-paragraph="N19-3"><span class="qr-step">20.3 · Interpretation and example</span>SC=81h here indicates invalid PI parameters, not the SCT=2 Guard Check Error. Check whether the requested protection configuration is valid before treating it as a mismatch between data and protection values.</p>
<p class="qr-tags">Search terms: SCT 1 · Conflicting Attributes · Invalid Protection Information · Copy errors</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b107">Base 2.4 Figure 107 · Status Code – Media and Data Integrity Error Values</a><a href="/nvme/figure-reference/io/en/#figure-n39">NVM Command Set 1.3 Figure 39 · Copy – Copy Descriptor Formats</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n20" data-figure="N20">
<h2><span class="qr-number">21</span>Status Code – Media and Data Integrity Error Values</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 20 · Status Code – Media and Data Integrity Error Values</p>
<p class="qr-location">§3.1.2 · Printed pages 26 · PDF 26</p>
<p class="qr-explanation" data-paragraph="N20-1"><span class="qr-step">21.1 · Use</span>This table adds NVM content-comparison and deallocated/unwritten-block failures. It prevents misclassifying every Compare mismatch as unreadable media.</p>
<p class="qr-explanation" data-paragraph="N20-2"><span class="qr-step">21.2 · Fields and relationships</span>SC=85h means Compare Failure.87h reports a failed Copy, Read or Verify involving deallocated or unwritten LBAs. Interpret 87h together with namespace behavior and the Deallocated or Unwritten Logical Block Error configuration.</p>
<p class="qr-explanation" data-paragraph="N20-3"><span class="qr-step">21.3 · Interpretation and example</span>Compare 85h establishes a miscompare, not necessarily a CRC failure. Read 87h likewise does not by itself establish physical damage; first check whether the range was deallocated or never written.</p>
<p class="qr-tags">Search terms: SCT 2 · Compare Failure · Deallocated or Unwritten Logical Block · DULBE</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b107">Base 2.4 Figure 107 · Status Code – Media and Data Integrity Error Values</a><a href="/nvme/figure-reference/io/en/#figure-n47">NVM Command Set 1.3 Figure 47 · Dataset Management – Range Definition</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<footer id="source-files"><h2>Source documents</h2><p>Locations refer to the supplied ratified PDFs. For Base, PDF page = printed page +26; the other two use identical page numbers. Original figure numbers and English titles are retained for PDF search. Source PDFs are not redistributed.</p><ul class="qr-sources"><li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li></ul></footer>
</main></div>
