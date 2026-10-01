---
layout: "post"
title: "NVMe Figures and Scenarios 01 · Initialization, Queues, and PCIe"
date: "2026-09-29 09:00:00 +0800"
categories: ["nvme"]
tags: ["NVMe", "Reference"]
permalink: "/nvme/figure-reference/init/en/"
nvme_quickref: true
last_modified_at: "2026-10-01"
lang: "en"
description: "NVMe scenarios and source figures: lookup routes, field reasoning, worked answers and precise specification locations."
---

<div class="nvme-quickref">
<nav class="qr-top" aria-label="Editions and index"><a href="#content">Skip to content</a><a href="/nvme/figure-reference/en/">Index</a><a href="/nvme/figure-reference/init/zh-tw/">繁體中文</a><a href="/DOCS/nvme-quick-reference/init.html">Chinese HTML</a></nav>
<main id="content">
<header><p class="qr-eyebrow">LOOKUP · FIELD INTERPRETATION · SOURCE LOCATIONS</p><h1>NVMe Figures and Scenarios 01 · Initialization, Queues, and PCIe</h1><p class="qr-intro">Start with addresses and capabilities, then readiness, queue locations and interrupts. Link and PCIe error registers distinguish transport observations from command completions.</p></header>
<aside class="qr-note"><p>Each source figure has a use, field guide and worked interpretation. Example numbers are illustrative, not assumed device settings. Apply the conditions belonging to the field and command.</p><p>Use browser Find for fields, FID, LID, CNS or Figure. Positions follow the source: a byte is 8 bits and a Dword is 4 bytes. An index counts entries; an offset measures displacement from an origin in the specified unit.</p><p>FID (Feature Identifier) selects a feature; LID (Log Page Identifier) selects a log page; CNS (Controller or Namespace Structure) selects the structure returned by Identify.</p></aside>
<nav class="qr-top" aria-label="Volume entry points"><a href="#exercises">Start with scenarios</a><a href="#figure-index">Go to figures</a></nav>
<section id="exercises"><h2>Try the scenarios first</h2>
<p>All observations are hypothetical, not device measurements. Before opening an answer, identify the interface, target, fields and supported conclusion. These are specification exercises; no commands are executed.</p>
<nav class="qr-toc" id="exercise-toc" aria-label="Exercise index"><ol>
<li><a href="#exercise-init-01">Why does PCIe enumeration not establish I/O readiness?</a></li>
<li><a href="#exercise-init-02">How do a 64-bit BAR and doorbell offset combine?</a></li>
<li><a href="#exercise-init-03">Why does RDY=1 not always establish media readiness?</a></li>
<li><a href="#exercise-init-04">Can an x4-capable device currently operate at x2?</a></li>
<li><a href="#exercise-init-05">Why might a CQE appear without an MSI-X notification?</a></li>
<li><a href="#exercise-init-06">Are PCIe AER and NVMe AER the same mechanism?</a></li>
</ol></nav>
<article class="qr-card qr-case" id="exercise-init-01" data-scenario="init-01"><h3><span class="qr-number">EXERCISE 01</span>Why does PCIe enumeration not establish I/O readiness?</h3>
<p class="qr-case-question">The system reads PCI Vendor ID and Device ID and declares NVMe ready. Which evidence layers are still missing?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>PCI configuration CMD has MSE=0 and BME=0; BARs have assigned values.</li>
<li>NVMe CAP, CC and CSTS have not been verified; there is no successful Admin Queue or Identify trace.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>PCI configuration → BARs and PCI CMD → NVMe memory-mapped properties → Admin Queue/Identify → I/O queues and namespaces.</p>
<p data-reasoning="init-01-1"><span class="qr-step">Step 1</span>Readable PCI configuration establishes access to that function’s configuration, not full operation. MSE controls memory-space access and BME concerns device-initiated memory transactions; these operating conditions are not established here.</p>
<p data-reasoning="init-01-2"><span class="qr-step">Step 2</span>Next come NVMe CAP capabilities, CC configuration, CSTS status and queue-memory locations. PCI CMD, NVMe CC and Identify Controller belong to different interfaces; one field cannot substitute for the other layers.</p>
<p data-reasoning="init-01-3"><span class="qr-step">Step 3</span>This exercise establishes an inspection sequence without enabling hardware. PCI IDs alone do not answer LBA formats, Sanitize methods or namespace capacity; those require NVMe command responses.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/init/en/#figure-p12">PCIe Transport 1.4 Figure 12 · Offset 04h: CMD - Command</a><a href="/nvme/figure-reference/init/en/#figure-p20">PCIe Transport 1.4 Figure 20 · Offset 10h: MLBAR (BAR0) – Memory Register Base Address, lower 32-bits</a><a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a><a href="/nvme/figure-reference/init/en/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a><a href="/nvme/figure-reference/init/en/#figure-b42">Base 2.4 Figure 42 · Offset 1Ch: CSTS – Controller Status</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>PCIe Transport 1.4 · §3.8.1.2 · Figure 12 · Offset 04h: CMD - Command · Printed pages 17 · PDF 17</li><li>PCIe Transport 1.4 · §3.8.1.10 · Figure 20 · Offset 10h: MLBAR (BAR0) – Memory Register Base Address, lower 32-bits · Printed pages 19 · PDF 19</li><li>Base 2.4 · §3.1.4.1 · Figure 36 · Offset 0h: CAP – Controller Capabilities · Printed pages 55–58 · PDF 81–84</li><li>Base 2.4 · §3.1.4.5 · Figure 41 · Offset 14h: CC – Controller Configuration · Printed pages 60–63 · PDF 86–89</li><li>Base 2.4 · §3.1.4.6 · Figure 42 · Offset 1Ch: CSTS – Controller Status · Printed pages 63–65 · PDF 89–91</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-init-02" data-scenario="init-02"><h3><span class="qr-number">EXERCISE 02</span>How do a 64-bit BAR and doorbell offset combine?</h3>
<p class="qr-case-question">A trace tool retains only BAR0 and places queue 3’s doorbell below 4 GiB. Reconstruct the address from configuration.</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>BAR0=40000004h, confirmed as a 64-bit memory BAR; BAR1=00000002h.</li>
<li>CAP.DSTRD=2; target queue identifier y=3 for SQ tail and CQ head doorbells.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>PCI configuration BAR0/BAR1 → register base → CAP.DSTRD → SQ/CQ doorbell offsets for the queue ID.</p>
<p data-reasoning="init-02-1"><span class="qr-step">Step 1</span>Remove BAR0 attribute bits before combining: base=(2&lt;&lt;32)|40000000h=0000000240000000h. The trailing four in BAR0 is an attribute, not four extra address bytes.</p>
<p data-reasoning="init-02-2"><span class="qr-step">Step 2</span>Stride is 4&lt;&lt;2=16 bytes. SQ3 offset is 1000h+(2×3)×16=1060h; CQ3 offset is 1000h+(2×3+1)×16=1070h. Three is the queue ID, not a current ring-entry index.</p>
<p data-reasoning="init-02-3"><span class="qr-step">Step 3</span>The addresses are 0000000240001060h and 0000000240001070h. This locates registers only; tail/head values come from queue state, not from register addresses or byte offsets.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/init/en/#figure-p20">PCIe Transport 1.4 Figure 20 · Offset 10h: MLBAR (BAR0) – Memory Register Base Address, lower 32-bits</a><a href="/nvme/figure-reference/init/en/#figure-p21">PCIe Transport 1.4 Figure 21 · Offset 14h: MUBAR (BAR1) – Memory Register Base Address, upper 32-bits</a><a href="/nvme/figure-reference/init/en/#figure-p5">PCIe Transport 1.4 Figure 5 · Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL – Submission Queue y Tail Doorbell</a><a href="/nvme/figure-reference/init/en/#figure-p6">PCIe Transport 1.4 Figure 6 · Offset (1000h + ((2y + 1) * (4 &lt;&lt; CAP.DSTRD))): CQyHDBL – Completion Queue y Head Doorbell</a><a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>PCIe Transport 1.4 · §3.8.1.10 · Figure 20 · Offset 10h: MLBAR (BAR0) – Memory Register Base Address, lower 32-bits · Printed pages 19 · PDF 19</li><li>PCIe Transport 1.4 · §3.8.1.11 · Figure 21 · Offset 14h: MUBAR (BAR1) – Memory Register Base Address, upper 32-bits · Printed pages 19 · PDF 19</li><li>PCIe Transport 1.4 · §3.1.2.1 · Figure 5 · Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL – Submission Queue y Tail Doorbell · Printed pages 10 · PDF 10</li><li>PCIe Transport 1.4 · §3.1.2.2 · Figure 6 · Offset (1000h + ((2y + 1) * (4 &lt;&lt; CAP.DSTRD))): CQyHDBL – Completion Queue y Head Doorbell · Printed pages 10–11 · PDF 10–11</li><li>Base 2.4 · §3.1.4.1 · Figure 36 · Offset 0h: CAP – Controller Capabilities · Printed pages 55–58 · PDF 81–84</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-init-03" data-scenario="init-03"><h3><span class="qr-number">EXERCISE 03</span>Why does RDY=1 not always establish media readiness?</h3>
<p class="qr-case-question">An initialization trace sees RDY=1 after one second and requires every namespace command to work immediately. Which mode did it overlook?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>Media-independent readiness is supported and enabled: CC.CRIME=1; CSTS.RDY=1, CFS=0.</li>
<li>CRTO.CRIMT=3, CRWMT=12; readiness of all required media has not been established.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Read CAP readiness capabilities, CC.CRIME, CSTS and CRTO; distinguish media-independent readiness from readiness with required media.</p>
<p data-reasoning="init-03-1"><span class="qr-step">Step 1</span>CRIMT=3 and CRWMT=12 use 500 ms units, giving 1.5 seconds and six seconds. They describe timeout bounds for their conditions, not mandatory durations for every initialization.</p>
<p data-reasoning="init-03-2"><span class="qr-step">Step 2</span>In this enabled mode, RDY can first establish readiness for media-independent commands. A test must distinguish commands requiring media rather than extending that observation to every data path.</p>
<p data-reasoning="init-03-3"><span class="qr-step">Step 3</span>Identify CNS=08h additionally reports target namespace NSTAT.NRDY: one means that namespace is ready. Retain the CC.EN=1 timing origin and actual command status when assessing the corresponding timeout. CFS=0 means no reported controller-fatal status, not proof of media readiness.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a><a href="/nvme/figure-reference/init/en/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a><a href="/nvme/figure-reference/init/en/#figure-b42">Base 2.4 Figure 42 · Offset 1Ch: CSTS – Controller Status</a><a href="/nvme/figure-reference/init/en/#figure-b57">Base 2.4 Figure 57 · Offset 68h: CRTO – Controller Ready Timeouts</a><a href="/nvme/figure-reference/identify/en/#figure-b346">Base 2.4 Figure 346 · Identify – I/O Command Set Independent Identify Namespace Data Structure</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §3.1.4.1 · Figure 36 · Offset 0h: CAP – Controller Capabilities · Printed pages 55–58 · PDF 81–84</li><li>Base 2.4 · §3.1.4.5 · Figure 41 · Offset 14h: CC – Controller Configuration · Printed pages 60–63 · PDF 86–89</li><li>Base 2.4 · §3.1.4.6 · Figure 42 · Offset 1Ch: CSTS – Controller Status · Printed pages 63–65 · PDF 89–91</li><li>Base 2.4 · §3.1.4.21 · Figure 57 · Offset 68h: CRTO – Controller Ready Timeouts · Printed pages 73 · PDF 99</li><li>Base 2.4 · §5.2.14.2.8 · Figure 346 · Identify – I/O Command Set Independent Identify Namespace Data Structure · Printed pages 394 · PDF 420</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-init-04" data-scenario="init-04"><h3><span class="qr-number">EXERCISE 04</span>Can an x4-capable device currently operate at x2?</h3>
<p class="qr-case-question">The device and its capability report x4 support, yet performance is lower. Where is the actual lane count reported?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>The PCIe link is up; Link Capabilities reports maximum x4, while Link Status NLW=2.</li>
<li>CLS is retained, but complete path, payload and workload throughput evidence is unavailable.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Locate PCI Express Capability in PCI configuration, then read Link Capabilities and Link Status; this is not an Identify CNS response.</p>
<p data-reasoning="init-04-1"><span class="qr-step">Step 1</span>Capability describes supported maximum width; NLW describes negotiated width. The values are consistent: the device can support x4 while this link uses x2.</p>
<p data-reasoning="init-04-2"><span class="qr-step">Step 2</span>This establishes fewer negotiated lanes than the maximum, but endpoint fields alone cannot locate the cause among slot, upstream port, platform configuration or other factors. Compare capabilities and negotiated states along the path.</p>
<p data-reasoning="init-04-3"><span class="qr-step">Step 3</span>CLS is a speed encoding, not a raw GT/s quantity; x2 is not measured bandwidth either. Separate capability from negotiation before applying the applicable speed definition and throughput measurements.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/init/en/#figure-p55">PCIe Transport 1.4 Figure 55 · Offset PXCAP + 12h: PXLS – PCI Express Link Status</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>PCIe Transport 1.4 · §3.8.5.6 · Printed pages 28–29 · PDF 28–29</li><li>PCIe Transport 1.4 · §3.8.5.8 · Figure 55 · Offset PXCAP + 12h: PXLS – PCI Express Link Status · Printed pages 29 · PDF 29</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-init-05" data-scenario="init-05"><h3><span class="qr-number">EXERCISE 05</span>Why might a CQE appear without an MSI-X notification?</h3>
<p class="qr-case-question">Polling finds a new CQE, but the interrupt handler does not run. Should the first check concern media or interrupt configuration?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>MSI-X: MXE=1, FM=0, TS=7; the CQ uses vector five, whose individual mask is one.</li>
<li>The new CQE phase and successful status are verified; PBA and coalescing have not yet been inspected.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>CQ interrupt-vector association → PCI MSI-X Message Control → table-entry mask/PBA → FID=08h and per-vector settings where relevant.</p>
<p data-reasoning="init-05-1"><span class="qr-step">Step 1</span>TS=7 means eight table entries, so vector five is within range. FM=0 removes the function-wide mask, not individual vector masks.</p>
<p data-reasoning="init-05-2"><span class="qr-step">Step 2</span>Vector five remains masked, directly explaining suppressed delivery. Successful completion and interrupt notification are separate observations; an absent handler invocation does not negate the observed CQE.</p>
<p data-reasoning="init-05-3"><span class="qr-step">Step 3</span>If the individual mask is also clear, inspect pending state, coalescing and host routing. This branch does not explain every missing interrupt, and vector count must not be equated with queue count.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/init/en/#figure-p44">PCIe Transport 1.4 Figure 44 · Offset MSIXCAP + 2h: MXC – MSI-X Message Control</a><a href="/nvme/figure-reference/init/en/#figure-p45">PCIe Transport 1.4 Figure 45 · Offset MSIXCAP + 4h: MTAB – MSI-X Table Offset / Table BIR</a><a href="/nvme/figure-reference/init/en/#figure-p46">PCIe Transport 1.4 Figure 46 · Offset MSIXCAP + 8h: MPBA – MSI-X PBA Offset / PBA BIR</a><a href="/nvme/figure-reference/features/en/#figure-b543">Base 2.4 Figure 543 · Interrupt Coalescing – Command Dword 11</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>PCIe Transport 1.4 · §3.8.4.2 · Figure 44 · Offset MSIXCAP + 2h: MXC – MSI-X Message Control · Printed pages 24–25 · PDF 24–25</li><li>PCIe Transport 1.4 · §3.8.4.3 · Figure 45 · Offset MSIXCAP + 4h: MTAB – MSI-X Table Offset / Table BIR · Printed pages 25 · PDF 25</li><li>PCIe Transport 1.4 · §3.8.4.4 · Figure 46 · Offset MSIXCAP + 8h: MPBA – MSI-X PBA Offset / PBA BIR · Printed pages 25 · PDF 25</li><li>Base 2.4 · §5.2.30.2.1 · Figure 543 · Interrupt Coalescing – Command Dword 11 · Printed pages 515 · PDF 541</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-init-06" data-scenario="init-06"><h3><span class="qr-number">EXERCISE 06</span>Are PCIe AER and NVMe AER the same mechanism?</h3>
<p class="qr-case-question">A trace says AER without naming the interface. Can two PCIe status samples equal to one establish two new NVMe errors?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>PCIe AERCES.RTS is one in both samples, with no clearing or reset between them.</li>
<li>An NVMe Asynchronous Event Request completion also exists, but its timing and notification contents are not correlated.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>First identify whether the data comes from the PCIe Advanced Error Reporting extended capability or an NVMe Asynchronous Event Request completion.</p>
<p data-reasoning="init-06-1"><span class="qr-step">Step 1</span>PCIe AER means Advanced Error Reporting, with RTS here reporting Replay Timer Timeout status. NVMe AER is an asynchronous event command. Shared initials do not imply the same structure, target or event semantics.</p>
<p data-reasoning="init-06-2"><span class="qr-step">Step 2</span>RTS is a status bit, not a counter. Without clearing, repeated ones may reflect one retained state; two samples do not establish two occurrences or two failed NVMe commands.</p>
<p data-reasoning="init-06-3"><span class="qr-step">Step 3</span>Correlation needs complete records, timing and device identity from both interfaces. PCIe status can inform transport diagnosis but does not identify an SQID/CID or replace CQE and NVMe-log outcomes.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/init/en/#figure-p60">PCIe Transport 1.4 Figure 60 · Offset AERCAP + 4: AERUCES – AER Uncorrectable Error Status Register</a><a href="/nvme/figure-reference/init/en/#figure-p63">PCIe Transport 1.4 Figure 63 · Offset AERCAP + 10h: AERCES – AER Correctable Error Status Register</a><a href="/nvme/figure-reference/command/en/#figure-b99">Base 2.4 Figure 99 · Completion Queue Entry: DW 3</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>PCIe Transport 1.4 · §3.8.6.2 · Figure 60 · Offset AERCAP + 4: AERUCES – AER Uncorrectable Error Status Register · Printed pages 31–32 · PDF 31–32</li><li>PCIe Transport 1.4 · §3.8.6.5 · Figure 63 · Offset AERCAP + 10h: AERCES – AER Correctable Error Status Register · Printed pages 33 · PDF 33</li><li>Base 2.4 · §5.2.2 · Printed pages 183–190 · PDF 209–216</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
</section>
<nav class="qr-toc" id="figure-index" aria-label="Volume figure index"><h2>Figures in this volume</h2><ol>
<li><a href="#figure-b34">Base 2.4 Figure 34 · Memory-Based Property Definition</a></li>
<li><a href="#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a></li>
<li><a href="#figure-b42">Base 2.4 Figure 42 · Offset 1Ch: CSTS – Controller Status</a></li>
<li><a href="#figure-b43">Base 2.4 Figure 43 · Offset 20h: NSSR – NVM Subsystem Reset</a></li>
<li><a href="#figure-b44">Base 2.4 Figure 44 · Offset 24h: AQA – Admin Queue Attributes</a></li>
<li><a href="#figure-b45">Base 2.4 Figure 45 · Offset 28h: ASQ – Admin Submission Queue Base Address</a></li>
<li><a href="#figure-b46">Base 2.4 Figure 46 · Offset 30h: ACQ – Admin Completion Queue Base Address</a></li>
<li><a href="#figure-b57">Base 2.4 Figure 57 · Offset 68h: CRTO – Controller Ready Timeouts</a></li>
<li><a href="#figure-p5">PCIe Transport 1.4 Figure 5 · Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL – Submission Queue y Tail Doorbell</a></li>
<li><a href="#figure-p6">PCIe Transport 1.4 Figure 6 · Offset (1000h + ((2y + 1) * (4 &lt;&lt; CAP.DSTRD))): CQyHDBL – Completion Queue y Head Doorbell</a></li>
<li><a href="#figure-p12">PCIe Transport 1.4 Figure 12 · Offset 04h: CMD - Command</a></li>
<li><a href="#figure-p20">PCIe Transport 1.4 Figure 20 · Offset 10h: MLBAR (BAR0) – Memory Register Base Address, lower 32-bits</a></li>
<li><a href="#figure-p21">PCIe Transport 1.4 Figure 21 · Offset 14h: MUBAR (BAR1) – Memory Register Base Address, upper 32-bits</a></li>
<li><a href="#figure-p44">PCIe Transport 1.4 Figure 44 · Offset MSIXCAP + 2h: MXC – MSI-X Message Control</a></li>
<li><a href="#figure-p45">PCIe Transport 1.4 Figure 45 · Offset MSIXCAP + 4h: MTAB – MSI-X Table Offset / Table BIR</a></li>
<li><a href="#figure-p46">PCIe Transport 1.4 Figure 46 · Offset MSIXCAP + 8h: MPBA – MSI-X PBA Offset / PBA BIR</a></li>
<li><a href="#figure-p55">PCIe Transport 1.4 Figure 55 · Offset PXCAP + 12h: PXLS – PCI Express Link Status</a></li>
<li><a href="#figure-p60">PCIe Transport 1.4 Figure 60 · Offset AERCAP + 4: AERUCES – AER Uncorrectable Error Status Register</a></li>
<li><a href="#figure-p63">PCIe Transport 1.4 Figure 63 · Offset AERCAP + 10h: AERCES – AER Correctable Error Status Register</a></li>
</ol></nav>
<article class="qr-card" id="figure-b34" data-figure="B34">
<h2><span class="qr-number">01</span>Memory-Based Property Definition</h2>
<p class="qr-original">Base 2.4 · Figure 34 · Memory-Based Property Definition</p>
<p class="qr-location">§3.1.4 · Printed pages 54 · PDF 80</p>
<p class="qr-explanation" data-paragraph="B34-1"><span class="qr-step">01.1 · Use</span>Use this table to locate the transport-specific area after controller properties. PCIe doorbells begin at offset 1000h relative to the register base, not host physical address 1000h.</p>
<p class="qr-explanation" data-paragraph="B34-2"><span class="qr-step">01.2 · Fields and relationships</span>OFST is a byte offset, Size gives occupied space, and T means transport-defined. Variable does not imply a fixed 4 KiB region. Individual SQ/CQ doorbells also depend on CAP.DSTRD.</p>
<p class="qr-explanation" data-paragraph="B34-3"><span class="qr-step">01.3 · Interpretation and example</span>For an illustrative BAR base of 80000000h, the doorbell region begins at 80001000h. Locate queue 2 using PCIe Figures 5 and 6; writing its queue ID at the region start is not equivalent.</p>
<p class="qr-tags">Search terms: MMIO · doorbell · OFST</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-p5">PCIe Transport 1.4 Figure 5 · Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL – Submission Queue y Tail Doorbell</a><a href="/nvme/figure-reference/init/en/#figure-p6">PCIe Transport 1.4 Figure 6 · Offset (1000h + ((2y + 1) * (4 &lt;&lt; CAP.DSTRD))): CQyHDBL – Completion Queue y Head Doorbell</a><a href="/nvme/figure-reference/init/en/#figure-p20">PCIe Transport 1.4 Figure 20 · Offset 10h: MLBAR (BAR0) – Memory Register Base Address, lower 32-bits</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b36" data-figure="B36">
<h2><span class="qr-number">02</span>Offset 0h: CAP – Controller Capabilities</h2>
<p class="qr-original">Base 2.4 · Figure 36 · Offset 0h: CAP – Controller Capabilities</p>
<p class="qr-location">§3.1.4.1 · Printed pages 55–58 · PDF 81–84</p>
<p class="qr-explanation" data-paragraph="B36-1"><span class="qr-step">02.1 · Use</span>Read CAP before choosing queue sizes, memory pages or readiness timeouts. It reports capabilities, not the current CC configuration; advertised support does not mean a function is enabled.</p>
<p class="qr-explanation" data-paragraph="B36-2"><span class="qr-step">02.2 · Fields and relationships</span>Frequently used groups are MQES bits 15:0 (maximum entries minus one), CQR bit 16 (contiguous I/O queue requirement), DSTRD bits 35:32 (2^(2+DSTRD) byte stride), and MPSMIN/MPSMAX bits 51:48/55:52 (page-size exponents). CSS bits 44:37, NSSRS bit 36 and CRMS bits 60:59 describe command sets, subsystem reset and ready modes. TO bits 31:24 uses 500 ms units.</p>
<p class="qr-explanation" data-paragraph="B36-3"><span class="qr-step">02.3 · Interpretation and example</span>For example, MQES=03FFh allows 1024 entries while DSTRD=1 means an 8-byte stride. Neither raw value is a byte count. Check CC.MPS for the selected page size and combine CC.CRIME, CRTO and initialization rules for readiness.</p>
<p class="qr-tags">Search terms: CAP · MQES · MPSMIN · MPSMAX · DSTRD · TO · CRMS · CSS</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a><a href="/nvme/figure-reference/init/en/#figure-b57">Base 2.4 Figure 57 · Offset 68h: CRTO – Controller Ready Timeouts</a><a href="/nvme/figure-reference/init/en/#figure-p5">PCIe Transport 1.4 Figure 5 · Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL – Submission Queue y Tail Doorbell</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b41" data-figure="B41">
<h2><span class="qr-number">03</span>Offset 14h: CC – Controller Configuration</h2>
<p class="qr-original">Base 2.4 · Figure 41 · Offset 14h: CC – Controller Configuration</p>
<p class="qr-location">§3.1.4.5 · Printed pages 60–63 · PDF 86–89</p>
<p class="qr-explanation" data-paragraph="B41-1"><span class="qr-step">03.1 · Use</span>When advertised capabilities look adequate but initialization fails, inspect what the host actually programmed in CC. It combines enablement, command-set selection, page size, entry sizes and shutdown notification.</p>
<p class="qr-explanation" data-paragraph="B41-2"><span class="qr-step">03.2 · Fields and relationships</span>EN bit 0 enables the controller; CSS bits 6:4 selects command sets; MPS bits 10:7 specifies 2^(12+MPS) bytes; AMS bits 13:11 selects arbitration; SHN bits 15:14 requests shutdown. IOSQES bits 19:16 and IOCQES bits 23:20 are entry-size exponents. CRIME bit 24 selects the ready mode at enablement.</p>
<p class="qr-explanation" data-paragraph="B41-3"><span class="qr-step">03.3 · Interpretation and example</span>IOSQES=6 and IOCQES=4 mean 64-byte SQEs and 16-byte CQEs, not queue depths. Clearing EN from one to zero initiates Controller Reset. Fields such as MPS and CSS have disabled-state update requirements; this is not an unrestricted live configuration register.</p>
<p class="qr-tags">Search terms: CC · EN · MPS · IOSQES · IOCQES · SHN · CRIME</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a><a href="/nvme/figure-reference/init/en/#figure-b42">Base 2.4 Figure 42 · Offset 1Ch: CSTS – Controller Status</a><a href="/nvme/figure-reference/init/en/#figure-b44">Base 2.4 Figure 44 · Offset 24h: AQA – Admin Queue Attributes</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b42" data-figure="B42">
<h2><span class="qr-number">04</span>Offset 1Ch: CSTS – Controller Status</h2>
<p class="qr-original">Base 2.4 · Figure 42 · Offset 1Ch: CSTS – Controller Status</p>
<p class="qr-location">§3.1.4.6 · Printed pages 63–65 · PDF 89–91</p>
<p class="qr-explanation" data-paragraph="B42-1"><span class="qr-step">04.1 · Use</span>CC describes the host request; CSTS describes the controller response. Compare them when enablement stalls, completions disappear or shutdown remains incomplete.</p>
<p class="qr-explanation" data-paragraph="B42-2"><span class="qr-step">04.2 · Fields and relationships</span>RDY bit 0 indicates readiness to process submission entries. CFS bit 1 reports a fatal error that could not be communicated through an appropriate CQ. SHST bits 3:2 encodes shutdown progress; ST bit 6 distinguishes controller and subsystem shutdown. NSSRO bit 4 and PP bit 5 report reset occurrence and processing pause.</p>
<p class="qr-explanation" data-paragraph="B42-3"><span class="qr-step">04.3 · Interpretation and example</span>SHST=10b means shutdown completed, not that an ordinary I/O succeeded. The usable scope of RDY=1 depends on the ready mode: media-independent readiness does not establish readiness of every namespace medium.</p>
<p class="qr-tags">Search terms: CSTS · RDY · CFS · SHST · ST</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a><a href="/nvme/figure-reference/init/en/#figure-b57">Base 2.4 Figure 57 · Offset 68h: CRTO – Controller Ready Timeouts</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b43" data-figure="B43">
<h2><span class="qr-number">05</span>Offset 20h: NSSR – NVM Subsystem Reset</h2>
<p class="qr-original">Base 2.4 · Figure 43 · Offset 20h: NSSR – NVM Subsystem Reset</p>
<p class="qr-location">§3.1.4.7 · Printed pages 66 · PDF 92</p>
<p class="qr-explanation" data-paragraph="B43-1"><span class="qr-step">05.1 · Use</span>Use this table to recognize a request for NVM Subsystem Reset in a trace. CAP.NSSRS advertises support. Its scope differs from clearing one controller’s CC.EN.</p>
<p class="qr-explanation" data-paragraph="B43-2"><span class="qr-step">05.2 · Fields and relationships</span>At offset 20h, NSSRC bits 31:0 initiates the reset only when written with 4E564D65h. Other values have no such functional effect. Reads return zero, not the last requested value.</p>
<p class="qr-explanation" data-paragraph="B43-3"><span class="qr-step">05.3 · Interpretation and example</span>A trace containing a write of 4E564D65h followed by a zero readback is consistent with the definition; it does not show that the write was lost. Determine completion and reset scope using status and §3.7.1.</p>
<p class="qr-tags">Search terms: NSSR · NSSRC · NSSRS · 4E564D65h</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a><a href="/nvme/figure-reference/init/en/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a><a href="/nvme/figure-reference/init/en/#figure-b42">Base 2.4 Figure 42 · Offset 1Ch: CSTS – Controller Status</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b44" data-figure="B44">
<h2><span class="qr-number">06</span>Offset 24h: AQA – Admin Queue Attributes</h2>
<p class="qr-original">Base 2.4 · Figure 44 · Offset 24h: AQA – Admin Queue Attributes</p>
<p class="qr-location">§3.1.4.8 · Printed pages 66 · PDF 92</p>
<p class="qr-explanation" data-paragraph="B44-1"><span class="qr-step">06.1 · Use</span>Inspect AQA when Admin commands cannot be submitted or completions reclaimed. It holds queue entry counts, not buffer byte capacities.</p>
<p class="qr-explanation" data-paragraph="B44-2"><span class="qr-step">06.2 · Fields and relationships</span>ASQS bits 11:0 and ACQS bits 27:16 encode submission and completion depths minus one. The intervening and upper bits are reserved. Each queue has 2 to 4096 entries; enabling with either size field zero produces undefined results.</p>
<p class="qr-explanation" data-paragraph="B44-3"><span class="qr-step">06.3 · Interpretation and example</span>Two Admin queues of 64 entries use ASQS=63 and ACQS=63, giving AQA=003F003Fh. Equal depths do not imply equal buffer sizes because SQ and CQ entries have different sizes.</p>
<p class="qr-tags">Search terms: AQA · ASQS · ACQS · queue depth</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-b45">Base 2.4 Figure 45 · Offset 28h: ASQ – Admin Submission Queue Base Address</a><a href="/nvme/figure-reference/init/en/#figure-b46">Base 2.4 Figure 46 · Offset 30h: ACQ – Admin Completion Queue Base Address</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b45" data-figure="B45">
<h2><span class="qr-number">07</span>Offset 28h: ASQ – Admin Submission Queue Base Address</h2>
<p class="qr-original">Base 2.4 · Figure 45 · Offset 28h: ASQ – Admin Submission Queue Base Address</p>
<p class="qr-location">§3.1.4.9 · Printed pages 66 · PDF 92</p>
<p class="qr-explanation" data-paragraph="B45-1"><span class="qr-step">07.1 · Use</span>This table tells where the controller fetches Admin commands. ASQ is the Admin Submission Queue base, not the next command address or SQ tail.</p>
<p class="qr-explanation" data-paragraph="B45-2"><span class="qr-step">07.2 · Fields and relationships</span>ASQB bits 63:12 stores the upper 52 bits of the physical address; bits 11:0 are reserved zero. The complete address must also align to the page size selected by CC.MPS, so clearing 12 low bits is only the minimum requirement.</p>
<p class="qr-explanation" data-paragraph="B45-3"><span class="qr-step">07.3 · Interpretation and example</span>With CC.MPS=1, pages are 8 KiB. Address 00101000h is 4 KiB-aligned but does not meet that configuration. Check AQA and the allocated memory extent before correlating SQ doorbell writes.</p>
<p class="qr-tags">Search terms: ASQ · ASQB · Admin SQ · alignment</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a><a href="/nvme/figure-reference/init/en/#figure-b44">Base 2.4 Figure 44 · Offset 24h: AQA – Admin Queue Attributes</a><a href="/nvme/figure-reference/init/en/#figure-p5">PCIe Transport 1.4 Figure 5 · Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL – Submission Queue y Tail Doorbell</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b46" data-figure="B46">
<h2><span class="qr-number">08</span>Offset 30h: ACQ – Admin Completion Queue Base Address</h2>
<p class="qr-original">Base 2.4 · Figure 46 · Offset 30h: ACQ – Admin Completion Queue Base Address</p>
<p class="qr-location">§3.1.4.10 · Printed pages 67 · PDF 93</p>
<p class="qr-explanation" data-paragraph="B46-1"><span class="qr-step">08.1 · Use</span>Check ACQ when an Admin command was fetched but the host is waiting at the wrong completion address. Commands submitted through Admin SQ complete in this Admin CQ.</p>
<p class="qr-explanation" data-paragraph="B46-2"><span class="qr-step">08.2 · Fields and relationships</span>ACQB bits 63:12 contains the upper address bits; the low 12 bits are reserved. Alignment follows CC.MPS. Admin CQ is associated with interrupt vector 0, not an arbitrary I/O CQ vector.</p>
<p class="qr-explanation" data-paragraph="B46-3"><span class="qr-step">08.3 · Interpretation and example</span>A correct ACQ base does not make every entry new. The consumer must check the CQE phase tag and update the CQ head doorbell. ACQ itself does not advance by 16 after each completion.</p>
<p class="qr-tags">Search terms: ACQ · ACQB · Admin CQ · interrupt vector 0</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b99">Base 2.4 Figure 99 · Completion Queue Entry: DW 3</a><a href="/nvme/figure-reference/init/en/#figure-p6">PCIe Transport 1.4 Figure 6 · Offset (1000h + ((2y + 1) * (4 &lt;&lt; CAP.DSTRD))): CQyHDBL – Completion Queue y Head Doorbell</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b57" data-figure="B57">
<h2><span class="qr-number">09</span>Offset 68h: CRTO – Controller Ready Timeouts</h2>
<p class="qr-original">Base 2.4 · Figure 57 · Offset 68h: CRTO – Controller Ready Timeouts</p>
<p class="qr-location">§3.1.4.21 · Printed pages 73 · PDF 99</p>
<p class="qr-explanation" data-paragraph="B57-1"><span class="qr-step">09.1 · Use</span>Use CRTO to separate readiness for commands independent of media from readiness of all required media. First identify which condition an initialization timeout is testing.</p>
<p class="qr-explanation" data-paragraph="B57-2"><span class="qr-step">09.2 · Fields and relationships</span>CRIMT bits 31:16 and CRWMT bits 15:0 both use 500 ms units. CRIMT applies to supported and enabled media-independent readiness. CRWMT covers the controller and required media becoming ready and must not be smaller than CRIMT.</p>
<p class="qr-explanation" data-paragraph="B57-3"><span class="qr-step">09.3 · Interpretation and example</span>CRIMT=4 and CRWMT=20 mean 2 seconds and 10 seconds. Availability of some Admin commands after 2 seconds does not imply that namespace reads should already succeed. Check CC.CRIME and the command’s media dependency.</p>
<p class="qr-tags">Search terms: CRTO · CRIMT · CRWMT · ready timeout</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a><a href="/nvme/figure-reference/init/en/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a><a href="/nvme/figure-reference/init/en/#figure-b42">Base 2.4 Figure 42 · Offset 1Ch: CSTS – Controller Status</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-p5" data-figure="P5">
<h2><span class="qr-number">10</span>Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL – Submission Queue y Tail Doorbell</h2>
<p class="qr-original">PCIe Transport 1.4 · Figure 5 · Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL – Submission Queue y Tail Doorbell</p>
<p class="qr-location">§3.1.2.1 · Printed pages 10 · PDF 10</p>
<p class="qr-explanation" data-paragraph="P5-1"><span class="qr-step">10.1 · Use</span>After placing commands in an SQ, the host writes its new tail through this doorbell. Here y is the queue ID and the offset is relative to the register base, not the SQ buffer.</p>
<p class="qr-explanation" data-paragraph="P5-2"><span class="qr-step">10.2 · Fields and relationships</span>The address is 1000h+(2y)×(4&lt;&lt;CAP.DSTRD). SQT occupies bits 15:0; bits 31:16 are reserved. The value is the new ring index; derive the number of added commands from the change while accounting for wraparound.</p>
<p class="qr-explanation" data-paragraph="P5-3"><span class="qr-step">10.3 · Interpretation and example</span>With DSTRD=1 and y=2, the offset is 1020h. For a 64-entry SQ, advancing tail from 62 to 1 adds 3 entries. Writing 1 does not mean one new command.</p>
<p class="qr-tags">Search terms: SQyTDBL · SQT · DSTRD · tail · wrap</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-p6">PCIe Transport 1.4 Figure 6 · Offset (1000h + ((2y + 1) * (4 &lt;&lt; CAP.DSTRD))): CQyHDBL – Completion Queue y Head Doorbell</a><a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-p6" data-figure="P6">
<h2><span class="qr-number">11</span>Offset (1000h + ((2y + 1) * (4 &lt;&lt; CAP.DSTRD))): CQyHDBL – Completion Queue y Head Doorbell</h2>
<p class="qr-original">PCIe Transport 1.4 · Figure 6 · Offset (1000h + ((2y + 1) * (4 &lt;&lt; CAP.DSTRD))): CQyHDBL – Completion Queue y Head Doorbell</p>
<p class="qr-location">§3.1.2.2 · Printed pages 10–11 · PDF 10–11</p>
<p class="qr-explanation" data-paragraph="P6-1"><span class="qr-step">11.1 · Use</span>After consuming CQEs, the host updates the CQ head doorbell to release positions for controller reuse. This does not submit commands or read the current head.</p>
<p class="qr-explanation" data-paragraph="P6-2"><span class="qr-step">11.2 · Fields and relationships</span>Its offset is 1000h+(2y+1)×(4&lt;&lt;CAP.DSTRD). CQH occupies bits 15:0, with reserved upper bits. Calculate released entries from the new head with wraparound. Doorbell readback is vendor-specific and unsuitable as a status query.</p>
<p class="qr-explanation" data-paragraph="P6-3"><span class="qr-step">11.3 · Interpretation and example</span>For DSTRD=1, queue 2 uses CQ offset 1028h, eight bytes after SQ offset 1020h. Consuming completions without returning space can leave the controller without reusable CQ positions.</p>
<p class="qr-tags">Search terms: CQyHDBL · CQH · head · wrap</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-p5">PCIe Transport 1.4 Figure 5 · Offset (1000h + ((2y) * (4 &lt;&lt; CAP.DSTRD))): SQyTDBL – Submission Queue y Tail Doorbell</a><a href="/nvme/figure-reference/command/en/#figure-b99">Base 2.4 Figure 99 · Completion Queue Entry: DW 3</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-p12" data-figure="P12">
<h2><span class="qr-number">12</span>Offset 04h: CMD - Command</h2>
<p class="qr-original">PCIe Transport 1.4 · Figure 12 · Offset 04h: CMD - Command</p>
<p class="qr-location">§3.8.1.2 · Printed pages 17 · PDF 17</p>
<p class="qr-explanation" data-paragraph="P12-1"><span class="qr-step">12.1 · Use</span>Start with this PCI configuration table when a device enumerates but register access or host-data transfers fail. PCI CMD is neither an NVMe command nor NVMe CC.</p>
<p class="qr-explanation" data-paragraph="P12-2"><span class="qr-step">12.2 · Fields and relationships</span>Common checks are BME bit 2 (Bus Master Enable), MSE bit 1 (Memory Space Enable) and IOSE bit 0. Bit 10 is Interrupt Disable. Interpret the remaining fields according to their PCI roles.</p>
<p class="qr-explanation" data-paragraph="P12-3"><span class="qr-step">12.3 · Interpretation and example</span>An assigned BAR does not establish that BME and MSE are enabled. Check PCI configuration before queue addresses. Confusing PCI CMD offsets with NVMe CC accesses a different register space.</p>
<p class="qr-tags">Search terms: PCI CMD · BME · MSE · IOSE · MMIO · DMA</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-p20">PCIe Transport 1.4 Figure 20 · Offset 10h: MLBAR (BAR0) – Memory Register Base Address, lower 32-bits</a><a href="/nvme/figure-reference/init/en/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-p20" data-figure="P20">
<h2><span class="qr-number">13</span>Offset 10h: MLBAR (BAR0) – Memory Register Base Address, lower 32-bits</h2>
<p class="qr-original">PCIe Transport 1.4 · Figure 20 · Offset 10h: MLBAR (BAR0) – Memory Register Base Address, lower 32-bits</p>
<p class="qr-location">§3.8.1.10 · Printed pages 19 · PDF 19</p>
<p class="qr-explanation" data-paragraph="P20-1"><span class="qr-step">13.1 · Use</span>Use BAR0 to find the NVMe register mapping and determine whether BAR1 supplies upper address bits. Low bits also contain attributes rather than address data.</p>
<p class="qr-explanation" data-paragraph="P20-2"><span class="qr-step">13.2 · Fields and relationships</span>BA bits 31:14 holds the programmable portion of the lower 32 address bits; bits 13:4 are reserved. PF bit 3 indicates non-prefetchable space, TP bits 2:1 gives the mapping type and RTE bit 0 selects memory space. Larger apertures may make additional address bits read-only.</p>
<p class="qr-explanation" data-paragraph="P20-3"><span class="qr-step">13.3 · Interpretation and example</span>Remove attributes and check TP before assembling the address. Using only BAR0 truncates a 64-bit mapping above 4 GiB; treating every following BAR as an upper half without checking type is also incorrect.</p>
<p class="qr-tags">Search terms: BAR0 · MLBAR · BA · TP · PF · RTE</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-p21">PCIe Transport 1.4 Figure 21 · Offset 14h: MUBAR (BAR1) – Memory Register Base Address, upper 32-bits</a><a href="/nvme/figure-reference/init/en/#figure-b34">Base 2.4 Figure 34 · Memory-Based Property Definition</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-p21" data-figure="P21">
<h2><span class="qr-number">14</span>Offset 14h: MUBAR (BAR1) – Memory Register Base Address, upper 32-bits</h2>
<p class="qr-original">PCIe Transport 1.4 · Figure 21 · Offset 14h: MUBAR (BAR1) – Memory Register Base Address, upper 32-bits</p>
<p class="qr-location">§3.8.1.11 · Printed pages 19 · PDF 19</p>
<p class="qr-explanation" data-paragraph="P21-1"><span class="qr-step">14.1 · Use</span>Once a 64-bit register mapping is established, BAR1 supplies its upper 32 bits. Together with BAR0 it forms one address, not a second NVMe register area.</p>
<p class="qr-explanation" data-paragraph="P21-2"><span class="qr-step">14.2 · Fields and relationships</span>BA bits 31:0 corresponds directly to full-address bits 63:32. BAR0 still supplies the low address and attributes. Platform and bridge resource allocation also constrains usable addresses.</p>
<p class="qr-explanation" data-paragraph="P21-3"><span class="qr-step">14.3 · Interpretation and example</span>An upper value 1 and lower address portion 80000000h form 0000000180000000h. Dropping the upper half accesses 80000000h instead, a 4 GiB difference.</p>
<p class="qr-tags">Search terms: BAR1 · MUBAR · BA · 64-bit address</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-p20">PCIe Transport 1.4 Figure 20 · Offset 10h: MLBAR (BAR0) – Memory Register Base Address, lower 32-bits</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-p44" data-figure="P44">
<h2><span class="qr-number">15</span>Offset MSIXCAP + 2h: MXC – MSI-X Message Control</h2>
<p class="qr-original">PCIe Transport 1.4 · Figure 44 · Offset MSIXCAP + 2h: MXC – MSI-X Message Control</p>
<p class="qr-location">§3.8.4.2 · Printed pages 24–25 · PDF 24–25</p>
<p class="qr-explanation" data-paragraph="P44-1"><span class="qr-step">15.1 · Use</span>When a CQ contains completions but interrupts are absent, check MSI-X enablement, the function-wide mask and available vector count.</p>
<p class="qr-explanation" data-paragraph="P44-2"><span class="qr-step">15.2 · Fields and relationships</span>MXE bit 15 enables MSI-X, FM bit 14 masks all vectors and TS bits 10:0 encodes table entries minus one. MSI enable must be clear for MSI-X use. Clearing FM leaves each vector’s own mask effective.</p>
<p class="qr-explanation" data-paragraph="P44-3"><span class="qr-step">15.3 · Interpretation and example</span>TS=3 means four vectors, not that vector 3 is enabled. Changing FM from one to zero does not clear individual vector masks. Correlate the table with the CQ’s interrupt-vector assignment.</p>
<p class="qr-tags">Search terms: MSI-X · MXE · FM · TS · interrupt</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-p45">PCIe Transport 1.4 Figure 45 · Offset MSIXCAP + 4h: MTAB – MSI-X Table Offset / Table BIR</a><a href="/nvme/figure-reference/init/en/#figure-p46">PCIe Transport 1.4 Figure 46 · Offset MSIXCAP + 8h: MPBA – MSI-X PBA Offset / PBA BIR</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-p45" data-figure="P45">
<h2><span class="qr-number">16</span>Offset MSIXCAP + 4h: MTAB – MSI-X Table Offset / Table BIR</h2>
<p class="qr-original">PCIe Transport 1.4 · Figure 45 · Offset MSIXCAP + 4h: MTAB – MSI-X Table Offset / Table BIR</p>
<p class="qr-location">§3.8.4.3 · Printed pages 25 · PDF 25</p>
<p class="qr-explanation" data-paragraph="P45-1"><span class="qr-step">16.1 · Use</span>To inspect MSI-X vector configuration, locate the table by selecting its BAR and adding its offset. The BAR index and byte displacement are separate fields.</p>
<p class="qr-explanation" data-paragraph="P45-2"><span class="qr-step">16.2 · Fields and relationships</span>TBIR bits 2:0 selects the BAR; TO bits 31:3 holds an 8-byte-aligned offset. Clear the low three bits before adding the offset to the BAR base. A64-bit BAR is identified by its lower Dword BAR.</p>
<p class="qr-explanation" data-paragraph="P45-3"><span class="qr-step">16.3 · Interpretation and example</span>MTAB=00002004h means TBIR=4 and offset 2000h: BAR4’s mapped base plus 2000h, not BAR0 plus 2004h. Use the table’s permitted BIR encodings.</p>
<p class="qr-tags">Search terms: MTAB · TBIR · TO · MSI-X</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-p44">PCIe Transport 1.4 Figure 44 · Offset MSIXCAP + 2h: MXC – MSI-X Message Control</a><a href="/nvme/figure-reference/init/en/#figure-p46">PCIe Transport 1.4 Figure 46 · Offset MSIXCAP + 8h: MPBA – MSI-X PBA Offset / PBA BIR</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-p46" data-figure="P46">
<h2><span class="qr-number">17</span>Offset MSIXCAP + 8h: MPBA – MSI-X PBA Offset / PBA BIR</h2>
<p class="qr-original">PCIe Transport 1.4 · Figure 46 · Offset MSIXCAP + 8h: MPBA – MSI-X PBA Offset / PBA BIR</p>
<p class="qr-location">§3.8.4.4 · Printed pages 25 · PDF 25</p>
<p class="qr-explanation" data-paragraph="P46-1"><span class="qr-step">17.1 · Use</span>This register locates the Pending Bit Array used to inspect pending interrupt state. PBA and the MSI-X table are different structures and need not share an offset.</p>
<p class="qr-explanation" data-paragraph="P46-2"><span class="qr-step">17.2 · Fields and relationships</span>PBIR bits 2:0 selects a BAR; PBAO bits 31:3 supplies an 8-byte-aligned offset. The calculation resembles MTAB but the values may differ. These are location fields, not the per-vector pending bits themselves.</p>
<p class="qr-explanation" data-paragraph="P46-3"><span class="qr-step">17.3 · Interpretation and example</span>MPBA=00003000h locates PBA at BAR0’s mapped base plus 3000h. Inspect CQ memory to determine completed commands; a pending bit does not replace their individual completion statuses.</p>
<p class="qr-tags">Search terms: MPBA · PBA · PBIR · PBAO · pending</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-p45">PCIe Transport 1.4 Figure 45 · Offset MSIXCAP + 4h: MTAB – MSI-X Table Offset / Table BIR</a><a href="/nvme/figure-reference/command/en/#figure-b99">Base 2.4 Figure 99 · Completion Queue Entry: DW 3</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-p55" data-figure="P55">
<h2><span class="qr-number">18</span>Offset PXCAP + 12h: PXLS – PCI Express Link Status</h2>
<p class="qr-original">PCIe Transport 1.4 · Figure 55 · Offset PXCAP + 12h: PXLS – PCI Express Link Status</p>
<p class="qr-location">§3.8.5.8 · Printed pages 29 · PDF 29</p>
<p class="qr-explanation" data-paragraph="P55-1"><span class="qr-step">18.1 · Use</span>When bandwidth is below expectation, inspect negotiated link speed and width here. Maximum advertised capability is not the current negotiated result.</p>
<p class="qr-explanation" data-paragraph="P55-2"><span class="qr-step">18.2 · Fields and relationships</span>NLW bits 9:4 is Negotiated Link Width; CLS bits 3:0 is the Current Link Speed encoding. Both are undefined while the link is down. SCC bit 12 describes use of the platform’s common reference clock, not link speed.</p>
<p class="qr-explanation" data-paragraph="P55-3"><span class="qr-step">18.3 · Interpretation and example</span>NLW=2 means the active link is x 2 even if the product supports x 4. Decode CLS using the applicable PCIe speed encoding; this table does not fully define that external encoding, so the raw code is not a GT/s value.</p>
<p class="qr-tags">Search terms: PXLS · NLW · CLS · SCC · link speed · link width</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-p60">PCIe Transport 1.4 Figure 60 · Offset AERCAP + 4: AERUCES – AER Uncorrectable Error Status Register</a><a href="/nvme/figure-reference/init/en/#figure-p63">PCIe Transport 1.4 Figure 63 · Offset AERCAP + 10h: AERCES – AER Correctable Error Status Register</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-p60" data-figure="P60">
<h2><span class="qr-number">19</span>Offset AERCAP + 4: AERUCES – AER Uncorrectable Error Status Register</h2>
<p class="qr-original">PCIe Transport 1.4 · Figure 60 · Offset AERCAP + 4: AERUCES – AER Uncorrectable Error Status Register</p>
<p class="qr-location">§3.8.6.2 · Printed pages 31–32 · PDF 31–32</p>
<p class="qr-explanation" data-paragraph="P60-1"><span class="qr-step">19.1 · Use</span>Use this register for uncorrectable PCIe transaction or link errors. Here AER means Advanced Error Reporting, not NVMe Asynchronous Event Request.</p>
<p class="qr-explanation" data-paragraph="P60-2"><span class="qr-step">19.2 · Fields and relationships</span>Common bits are CTS bit 14 (Completion Timeout), UCS bit 16 (Unexpected Completion), MTS bit 18 (Malformed TLP), URES bit 20 (Unsupported Request) and DLPES bit 4 (Data Link Protocol Error). TLP means transaction-layer packet. Multiple bits can be set; separate mask and severity registers control reporting and severity.</p>
<p class="qr-explanation" data-paragraph="P60-3"><span class="qr-step">19.3 · Interpretation and example</span>CTS=1 records a PCIe completion timeout but does not identify the failed NVMe CID. Preserve status and header logs before correlating time, queues and CQEs. Save the original status before error recovery so it remains available for correlation.</p>
<p class="qr-tags">Search terms: AERUCES · CTS · URES · MTS · UCS · DLPES · PCIe AER</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-p63">PCIe Transport 1.4 Figure 63 · Offset AERCAP + 10h: AERCES – AER Correctable Error Status Register</a><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a><a href="/nvme/figure-reference/logs/en/#figure-b212">Base 2.4 Figure 212 · Error Information Log Entry Data Structure</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-p63" data-figure="P63">
<h2><span class="qr-number">20</span>Offset AERCAP + 10h: AERCES – AER Correctable Error Status Register</h2>
<p class="qr-original">PCIe Transport 1.4 · Figure 63 · Offset AERCAP + 10h: AERCES – AER Correctable Error Status Register</p>
<p class="qr-location">§3.8.6.5 · Printed pages 33 · PDF 33</p>
<p class="qr-explanation" data-paragraph="P63-1"><span class="qr-step">20.1 · Use</span>Inspect correctable errors when the link operates but performance or stability degrades. Correctable describes recovery of that error class, not whether its frequency matters.</p>
<p class="qr-explanation" data-paragraph="P63-2"><span class="qr-step">20.2 · Fields and relationships</span>RES bit 0 is Receiver Error; BTS bit 6 / BDS bit 7 are Bad TLP/Bad DLLP; RRS bit 8 is replay-number rollover; RTS bit 12 is Replay Timer Timeout. These are status bits, not occurrence counters. AERCEM controls their masks separately.</p>
<p class="qr-explanation" data-paragraph="P63-3"><span class="qr-step">20.3 · Interpretation and example</span>Seeing RTS=1 in two snapshots without an intervening clear does not establish two timeouts. Frequency analysis needs sampling times, clear operations and reproduction conditions, correlated with link status.</p>
<p class="qr-tags">Search terms: AERCES · RES · BTS · BDS · RTS · RRS · correctable</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-p55">PCIe Transport 1.4 Figure 55 · Offset PXCAP + 12h: PXLS – PCI Express Link Status</a><a href="/nvme/figure-reference/init/en/#figure-p60">PCIe Transport 1.4 Figure 60 · Offset AERCAP + 4: AERUCES – AER Uncorrectable Error Status Register</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<footer id="source-files"><h2>Source documents</h2><p>Locations refer to the supplied ratified PDFs. For Base, PDF page = printed page +26; the other two use identical page numbers. Original figure numbers and English titles are retained for PDF search. Source PDFs are not redistributed.</p><ul class="qr-sources"><li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li></ul></footer>
</main></div>
