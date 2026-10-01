---
layout: "post"
title: "NVMe Figures and Scenarios 04 · I/O Commands and Data Integrity"
date: "2026-09-29 09:00:00 +0800"
categories: ["nvme"]
tags: ["NVMe", "Reference"]
permalink: "/nvme/figure-reference/io/en/"
nvme_quickref: true
last_modified_at: "2026-10-01"
lang: "en"
description: "NVMe scenarios and source figures: lookup routes, field reasoning, worked answers and precise specification locations."
---

<div class="nvme-quickref">
<nav class="qr-top" aria-label="Editions and index"><a href="#content">Skip to content</a><a href="/nvme/figure-reference/en/">Index</a><a href="/nvme/figure-reference/io/zh-tw/">繁體中文</a><a href="/DOCS/nvme-quick-reference/io.html">Chinese HTML</a></nav>
<main id="content">
<header><p class="qr-eyebrow">LOOKUP · FIELD INTERPRETATION · SOURCE LOCATIONS</p><h1>NVMe Figures and Scenarios 04 · I/O Commands and Data Integrity</h1><p class="qr-intro">Follow command addresses and counts into metadata, protection information and atomicity. Equal field widths do not imply equal counting rules; command success alone does not establish every persistence or atomicity guarantee.</p></header>
<aside class="qr-note"><p>Each source figure has a use, field guide and worked interpretation. Example numbers are illustrative, not assumed device settings. Apply the conditions belonging to the field and command.</p><p>Use browser Find for fields, FID, LID, CNS or Figure. Positions follow the source: a byte is 8 bits and a Dword is 4 bytes. An index counts entries; an offset measures displacement from an origin in the specified unit.</p><p>FID (Feature Identifier) selects a feature; LID (Log Page Identifier) selects a log page; CNS (Controller or Namespace Structure) selects the structure returned by Identify.</p></aside>
<nav class="qr-top" aria-label="Volume entry points"><a href="#exercises">Start with scenarios</a><a href="#figure-index">Go to figures</a></nav>
<section id="exercises"><h2>Try the scenarios first</h2>
<p>All observations are hypothetical, not device measurements. Before opening an answer, identify the interface, target, fields and supported conclusion. These are specification exercises; no commands are executed.</p>
<nav class="qr-toc" id="exercise-toc" aria-label="Exercise index"><ol>
<li><a href="#exercise-io-01">Is an eight-block Write also atomic across power failure?</a></li>
<li><a href="#exercise-io-02">Why does NAWUPF=0 not necessarily mean one block?</a></li>
<li><a href="#exercise-io-03">Does a size-compliant Write remain atomic across a boundary?</a></li>
<li><a href="#exercise-io-04">Does a successful Write already establish persistence?</a></li>
<li><a href="#exercise-io-05">Why order data and index Writes if both use FUA?</a></li>
<li><a href="#exercise-io-06">How does PRACT=1 affect metadata larger than PI?</a></li>
<li><a href="#exercise-io-07">Is FFh after deallocation a failure?</a></li>
</ol></nav>
<article class="qr-card qr-case" id="exercise-io-01" data-scenario="io-01"><h3><span class="qr-number">EXERCISE 01</span>Is an eight-block Write also atomic across power failure?</h3>
<p class="qr-case-question">A colleague sees AWUN=7 and claims that an eight-block Write cannot be partially updated by power failure. What is missing?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>AWUN=7, AWUPF=1; NSFEAT.NSABP=0 and MAM=0; current Write Atomicity Normal has DN=0.</li>
<li>LBA data size is 4096 bytes; this is one ordinary Write with NLB=7.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Identify CNS=01h for the NVM-defined AWUN/AWUPF fields; CNS=00h for namespace NSFEAT; Get Features FID=0Ah, SEL=0 to confirm normal atomicity is not disabled.</p>
<p data-reasoning="io-01-1"><span class="qr-step">Step 1</span>AWUN and AWUPF encode block counts minus one. Seven provides an eight-block normal-operation guarantee; one provides a two-block power-failure/error guarantee. NLB=7 requests eight blocks, or 32768 bytes.</p>
<p data-reasoning="io-01-2"><span class="qr-step">Step 2</span>Under these assumptions the Write fits the normal atomic limit but exceeds the power-failure limit. Exceeding a guarantee does not mean a torn write must occur; it means AWUPF cannot guarantee the whole eight-block update.</p>
<p data-reasoning="io-01-3"><span class="qr-step">Step 3</span>If the application needs an indivisible 32 KiB update across power loss, it needs an appropriate supported configuration or higher-level protection. FUA=1 adds a persistence requirement before completion; it does not expand AWUPF from two blocks to eight.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/io/en/#figure-n4">NVM Command Set 1.3 Figure 4 · Atomicity Parameters for Single Atomicity Mode</a><a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a><a href="/nvme/figure-reference/io/en/#figure-n71">NVM Command Set 1.3 Figure 71 · Write – Command Dword 12</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>NVM Command Set 1.3 · §4.1.5.2 · Printed pages 94–96 · PDF 94–96</li><li>NVM Command Set 1.3 · §4.1.5.1 · Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set · Printed pages 85–86, 88 · PDF 85–86, 88</li><li>NVM Command Set 1.3 · §2.1.4 · Printed pages 15–18 · PDF 15–18</li><li>NVM Command Set 1.3 · §4.1.3.4 · Printed pages 67 · PDF 67</li><li>NVM Command Set 1.3 · §3.3.6 · Figure 71 · Write – Command Dword 12 · Printed pages 54 · PDF 54</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-io-02" data-scenario="io-02"><h3><span class="qr-number">EXERCISE 02</span>Why does NAWUPF=0 not necessarily mean one block?</h3>
<p class="qr-case-question">A decoder adds one to every atomic-unit field. Which result does it get wrong here?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>Controller: AWUN=7, AWUPF=3. Namespace: NSABP=1, NAWUN=15, NAWUPF=0, NABSN=0, NABSPF=0, MAM=0.</li>
<li>Normal atomicity is enabled; LBA data size=4096 bytes.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Pair Identify CNS=01h with CNS=00h to obtain the controller baseline and namespace-specific values.</p>
<p data-reasoning="io-02-1"><span class="qr-step">Step 1</span>Check NSABP before interpreting namespace atomic fields. NAWUN=15 is nonzero, providing 16 blocks, or 64 KiB, for normal operation rather than only the controller’s eight-block baseline.</p>
<p data-reasoning="io-02-2"><span class="qr-step">Step 2</span>NAWUPF=0 has a special meaning here: use controller AWUPF rather than adding one to zero. AWUPF=3 provides four blocks, or 16 KiB, for power-failure atomicity.</p>
<p data-reasoning="io-02-3"><span class="qr-step">Step 3</span>NABSN=NABSPF=0 specifies no corresponding atomic boundaries. These zeros, NAWUPF’s fallback zero and controller AWUPF=0 meaning one block have different semantics. A decoder needs field-specific rules.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/io/en/#figure-n4">NVM Command Set 1.3 Figure 4 · Atomicity Parameters for Single Atomicity Mode</a><a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>NVM Command Set 1.3 · §4.1.5.2 · Printed pages 94–96 · PDF 94–96</li><li>NVM Command Set 1.3 · §4.1.5.1 · Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set · Printed pages 85–86, 88–89 · PDF 85–86, 88–89</li><li>NVM Command Set 1.3 · §2.1.4 · Printed pages 16–19 · PDF 16–19</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-io-03" data-scenario="io-03"><h3><span class="qr-number">EXERCISE 03</span>Does a size-compliant Write remain atomic across a boundary?</h3>
<p class="qr-case-question">Two Writes each contain four blocks. Why can their starting LBAs change the namespace atomicity guarantee?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>AWUN=0, AWUPF=0; NSABP=1, NAWUN=7, NAWUPF=7; NABSN=7, NABSPF=7, NABO=0; DN=0.</li>
<li>First consider MAM=0. Write A: SLBA=8, NLB=3. Write B: SLBA=6, NLB=3.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Identify CNS=00h for units, boundaries, offset and NSFEAT.MAM; convert commands into actual LBA intervals before comparing.</p>
<p data-reasoning="io-03-1"><span class="qr-step">Step 1</span>A nonzero encoded boundary size of seven represents eight blocks. With NABO=0, boundaries occur at 0, 8, 16 and so on. A covers LBAs 8–11 within one interval; B covers 6–9 and crosses eight. Equal lengths do not make their positions equivalent.</p>
<p data-reasoning="io-03-2"><span class="qr-step">Step 2</span>MAM=0 selects Single Atomicity Mode. A satisfies the namespace whole-Write conditions here; B crosses a boundary and cannot claim the same four-block guarantee. Boundary and unit-size checks belong together.</p>
<p data-reasoning="io-03-3"><span class="qr-step">Step 3</span>With a valid MAM=1 configuration, B is divided into atomic LBA subranges 6–7 and 8–9. Each subrange receives its own guarantee; the two combined are still not one indivisible update.</p>
<div class="qr-table"><table class=""><thead><tr><th scope="col">Command</th><th scope="col">Actual LBA range</th><th scope="col">Boundary at LBA 8</th></tr></thead><tbody><tr><td>A</td><td>8–11</td><td>8 9 10 11: one interval</td></tr><tr><td>B</td><td>6–9</td><td>6 7 | 8 9: crosses the boundary</td></tr></tbody></table></div>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/io/en/#figure-n8">NVM Command Set 1.3 Figure 8 · Atomic Boundaries Example</a><a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a><a href="/nvme/figure-reference/io/en/#figure-n4">NVM Command Set 1.3 Figure 4 · Atomicity Parameters for Single Atomicity Mode</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>NVM Command Set 1.3 · §2.1.4.4 · Printed pages 19 · PDF 19</li><li>NVM Command Set 1.3 · §2.1.4.5 · Printed pages 19–20 · PDF 19–20</li><li>NVM Command Set 1.3 · §4.1.5.1 · Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set · Printed pages 85, 88–89 · PDF 85, 88–89</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-io-04" data-scenario="io-04"><h3><span class="qr-number">EXERCISE 04</span>Does a successful Write already establish persistence?</h3>
<p class="qr-case-question">With capability data, feature values and a command trace, how can you assess persistence of a successful Write?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>A volatile write cache is confirmed present and enabled for this namespace; Get Features FID=06h reports WCE=1.</li>
<li>A: ordinary Write, FUA=0, successful, with no later Flush. B: Write, FUA=1, successful.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Identify CNS=01h for VWC, CNS=08h for VWCNP and the applicable FDP configuration → Get Features FID=06h, SEL=0 → command FUA and subsequent Flush trace.</p>
<p data-reasoning="io-04-1"><span class="qr-step">Step 1</span>A may already be on nonvolatile media or may still depend on volatile cache. Its successful completion alone does not distinguish those states, so neither definite persistence nor definite cache-only residency follows.</p>
<p data-reasoning="io-04-2"><span class="qr-step">Step 2</span>B’s FUA=1 requires this command’s data and metadata to reach nonvolatile media before completion. Persistence concerns retention after completion; atomicity concerns whether an update can be partial. They are separate questions.</p>
<p data-reasoning="io-04-3"><span class="qr-step">Step 3</span>Another route is to wait for A to complete, then submit a covering Flush and verify its successful completion. Flush covers completed commands for its target namespace before Flush submission. Concurrent submission would lack that ordering condition.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/features/en/#figure-b471">Base 2.4 Figure 471 · Volatile Write Cache – Command Dword 11</a><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a><a href="/nvme/figure-reference/identify/en/#figure-b346">Base 2.4 Figure 346 · Identify – I/O Command Set Independent Identify Namespace Data Structure</a><a href="/nvme/figure-reference/io/en/#figure-n71">NVM Command Set 1.3 Figure 71 · Write – Command Dword 12</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.14.2.1 · Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent · Printed pages 374 · PDF 400</li><li>Base 2.4 · §5.2.14.2.8 · Figure 346 · Identify – I/O Command Set Independent Identify Namespace Data Structure · Printed pages 391–394 · PDF 417–420</li><li>Base 2.4 · §5.2.30.1.4 · Figure 471 · Volatile Write Cache – Command Dword 11 · Printed pages 464–465 · PDF 490–491</li><li>Base 2.4 · §7.2 · Printed pages 567 · PDF 593</li><li>NVM Command Set 1.3 · §3.3.6 · Figure 71 · Write – Command Dword 12 · Printed pages 54 · PDF 54</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-io-05" data-scenario="io-05"><h3><span class="qr-number">EXERCISE 05</span>Why order data and index Writes if both use FUA?</h3>
<p class="qr-case-question">An application places a data Write and then its index Write in the same SQ. Both use FUA=1. Is the index prevented from becoming persistent first?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>Data and index use different LBA ranges and are not a fused operation.</li>
<li>Both are submitted without waiting for the first completion. The goal is to avoid a new index pointing at data not yet persisted after power loss.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Inspect FUA in the SQEs and the submission/completion timeline; apply NVM command-ordering and Write FUA rules.</p>
<p data-reasoning="io-05-1"><span class="qr-step">Step 1</span>SQ position does not enforce this data dependency. FUA=1 imposes persistence before each command completes; it does not add an ordering guarantee between separate commands.</p>
<p data-reasoning="io-05-2"><span class="qr-step">Step 2</span>A suitable illustrative sequence is: submit data Write with FUA=1 → verify successful completion → submit index Write with FUA=1 → verify successful completion. The first completion establishes data persistence before index submission.</p>
<p data-reasoning="io-05-3"><span class="qr-step">Step 3</span>This resolves the stated dependency, not a multi-command transaction. Requiring data and index to revert together or update together needs a fuller transaction or recovery design.</p>
<div class="qr-table"><table class=""><thead><tr><th scope="col">Order</th><th scope="col">Host observation/action</th></tr></thead><tbody><tr><td>1</td><td>Submit data Write, FUA=1</td></tr><tr><td>2</td><td>Wait for and verify data Write success</td></tr><tr><td>3</td><td>Only then submit index Write, FUA=1</td></tr><tr><td>4</td><td>Wait for and verify index Write success</td></tr></tbody></table></div>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/io/en/#figure-n71">NVM Command Set 1.3 Figure 71 · Write – Command Dword 12</a><a href="/nvme/figure-reference/io/en/#figure-n4">NVM Command Set 1.3 Figure 4 · Atomicity Parameters for Single Atomicity Mode</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>NVM Command Set 1.3 · §2.1.2 · Printed pages 14 · PDF 14</li><li>NVM Command Set 1.3 · §3.3.6 · Figure 71 · Write – Command Dword 12 · Printed pages 54 · PDF 54</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-io-06" data-scenario="io-06"><h3><span class="qr-number">EXERCISE 06</span>How does PRACT=1 affect metadata larger than PI?</h3>
<p class="qr-case-question">A port subtracts eight metadata bytes per LBA whenever PRACT=1. Is that correct here?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>16-bit Guard with PI enabled; LBA data=4096 bytes, MS=16, separate metadata buffer.</li>
<li>Write has PRACT=1 and NLB=3; other protection settings are valid.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Identify CNS=00h for LBAF, DPS and metadata settings, plus CNS=05h with CSI=00h for ELBAF where needed → apply Write 16-bit Guard processing rules.</p>
<p data-reasoning="io-06-1"><span class="qr-step">Step 1</span>NLB=3 requests four blocks. The data buffer is 4×4096=16384 bytes. In this metadata-greater-than-eight branch, the host still transfers 4×16=64 metadata bytes, not 32.</p>
<p data-reasoning="io-06-2"><span class="qr-step">Step 2</span>PRACT controls PI generation and processing, not a universal subtract-eight buffer rule. Exactly eight metadata bytes uses a different branch in the processing table; it cannot be applied to MS=16.</p>
<p data-reasoning="io-06-3"><span class="qr-step">Step 3</span>Beyond length, align separate versus extended placement, PI type and Guard format. Only with matching conditions is a byte-level comparison between transfers meaningful.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/identify/en/#figure-n125">NVM Command Set 1.3 Figure 125 · LBA Format Data Structure, NVM Command Set Specific</a><a href="/nvme/figure-reference/identify/en/#figure-n128">NVM Command Set 1.3 Figure 128 · Extended LBA Format Data Structure, NVM Command Set Specific</a><a href="/nvme/figure-reference/io/en/#figure-n154">NVM Command Set 1.3 Figure 154 · Metadata – Transferred as Separate Buffer</a><a href="/nvme/figure-reference/io/en/#figure-n174">NVM Command Set 1.3 Figure 174 · Write Command 16b Guard Protection Information Processing</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>NVM Command Set 1.3 · §4.1.5.1 · Figure 125 · LBA Format Data Structure, NVM Command Set Specific · Printed pages 94 · PDF 94</li><li>NVM Command Set 1.3 · §4.1.5.3 · Figure 128 · Extended LBA Format Data Structure, NVM Command Set Specific · Printed pages 101–102 · PDF 101–102</li><li>NVM Command Set 1.3 · §5.2.3 · Figure 154 · Metadata – Transferred as Separate Buffer · Printed pages 130 · PDF 130</li><li>NVM Command Set 1.3 · §5.3.2.1 · Figure 174 · Write Command 16b Guard Protection Information Processing · Printed pages 143 · PDF 143</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-io-07" data-scenario="io-07"><h3><span class="qr-number">EXERCISE 07</span>Is FFh after deallocation a failure?</h3>
<p class="qr-case-question">A validator requires every deallocated LBA to return zero. Could it reject permitted behavior?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>The range is confirmed deallocated; DLFEAT.DRB=010b; Get Features FID=05h reports DULBE=0.</li>
<li>PI is disabled in this example; Read succeeds and all data bytes are FFh.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Identify CNS=00h for DLFEAT and relevant capabilities; Get Features FID=05h, SEL=0 for the target NSID to read DULBE; then assess Read results.</p>
<p data-reasoning="io-07-1"><span class="qr-step">Step 1</span>DRB=010b describes FFh contents for deallocated reads, so this example agrees with the reported behavior. Successful Read does not inherently require zero; the validator should derive its expectation from DRB.</p>
<p data-reasoning="io-07-2"><span class="qr-step">Step 2</span>If DULBE is supported and enabled, deallocated/unwritten reads can instead take the error-reporting path. Preserve the feature state when comparing devices rather than only comparing returned bytes.</p>
<p data-reasoning="io-07-3"><span class="qr-step">Step 3</span>This tests logical-interface deallocation behavior, not secure erasure of every physical-media copy. Sanitize claims require evidence about that operation’s support, target and completion state.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a><a href="/nvme/figure-reference/io/en/#figure-n47">NVM Command Set 1.3 Figure 47 · Dataset Management – Range Definition</a><a href="/nvme/figure-reference/features/en/#figure-b198">Base 2.4 Figure 198 · Get Features – Command Dword 10</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>NVM Command Set 1.3 · §4.1.5.1 · Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set · Printed pages 88 · PDF 88</li><li>NVM Command Set 1.3 · §3.3.3.2.1 · Printed pages 48 · PDF 48</li><li>NVM Command Set 1.3 · §4.1.3.3 · Printed pages 66 · PDF 66</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
</section>
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
