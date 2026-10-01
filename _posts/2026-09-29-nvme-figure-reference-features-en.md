---
layout: "post"
title: "NVMe Figures and Scenarios 05 · Features, Power, Performance, and Resources"
date: "2026-09-29 09:00:00 +0800"
categories: ["nvme"]
tags: ["NVMe", "Reference"]
permalink: "/nvme/figure-reference/features/en/"
nvme_quickref: true
last_modified_at: "2026-10-01"
lang: "en"
description: "NVMe scenarios and source figures: lookup routes, field reasoning, worked answers and precise specification locations."
---

<div class="nvme-quickref">
<nav class="qr-top" aria-label="Editions and index"><a href="#content">Skip to content</a><a href="/nvme/figure-reference/en/">Index</a><a href="/nvme/figure-reference/features/zh-tw/">繁體中文</a><a href="/DOCS/nvme-quick-reference/features.html">Chinese HTML</a></nav>
<main id="content">
<header><p class="qr-eyebrow">LOOKUP · FIELD INTERPRETATION · SOURCE LOCATIONS</p><h1>NVMe Figures and Scenarios 05 · Features, Power, Performance, and Resources</h1><p class="qr-intro">Separate support, current, default and saved values before interpreting individual features. Power latency, scheduling weights, queue counts and reclamation resources use different units.</p></header>
<aside class="qr-note"><p>Each source figure has a use, field guide and worked interpretation. Example numbers are illustrative, not assumed device settings. Apply the conditions belonging to the field and command.</p><p>Use browser Find for fields, FID, LID, CNS or Figure. Positions follow the source: a byte is 8 bits and a Dword is 4 bytes. An index counts entries; an offset measures displacement from an origin in the specified unit.</p><p>FID (Feature Identifier) selects a feature; LID (Log Page Identifier) selects a log page; CNS (Controller or Namespace Structure) selects the structure returned by Identify.</p></aside>
<nav class="qr-top" aria-label="Volume entry points"><a href="#exercises">Start with scenarios</a><a href="#figure-index">Go to figures</a></nav>
<section id="exercises"><h2>Try the scenarios first</h2>
<p>All observations are hypothetical, not device measurements. Before opening an answer, identify the interface, target, fields and supported conclusion. These are specification exercises; no commands are executed.</p>
<nav class="qr-toc" id="exercise-toc" aria-label="Exercise index"><ol>
<li><a href="#exercise-features-01">Why can a successful Get Features leave the current value unknown?</a></li>
<li><a href="#exercise-features-02">How many queues follow from a request for sixteen?</a></li>
<li><a href="#exercise-features-03">What do two APST transitions imply after 700 ms idle?</a></li>
<li><a href="#exercise-features-04">Does a slowdown at high temperature establish HCTM activity?</a></li>
<li><a href="#exercise-features-05">Does an unchanged HMB address establish an intact return?</a></li>
<li><a href="#exercise-features-06">Do weights seven and three guarantee a two-to-one IOPS ratio?</a></li>
</ol></nav>
<article class="qr-card qr-case" id="exercise-features-01" data-scenario="features-01"><h3><span class="qr-number">EXERCISE 01</span>Why can a successful Get Features leave the current value unknown?</h3>
<p class="qr-case-question">A tool displays DW0=5 as a feature’s current setting. Which interpretation layer did it miss?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>The controller supports Save/Select; SEL=3 targets a valid FID; CQE reports success and DW0=00000005h.</li>
<li>Current, default and saved values have not been retrieved.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Retain FID/SEL/NSID from the request → interpret SEL=3 capabilities → query the same FID and correct target with SEL=0 for the current value.</p>
<p data-reasoning="features-01-1"><span class="qr-step">Step 1</span>Five is binary 101: CHANG=1, NSSPEC=0, SVBL=1. This reports changeable attributes, non-namespace-specific scope and saveability, not a current value of five or proof of enablement.</p>
<p data-reasoning="features-01-2"><span class="qr-step">Step 2</span>SEL=0, 1 and 2 retrieve Current, Default and Saved respectively; they can differ. NSSPEC=0 also does not by itself establish controller-only scope; the feature definition determines that.</p>
<p data-reasoning="features-01-3"><span class="qr-step">Step 3</span>If a report retains DW0 but discards SEL, the meaning cannot be reliably reconstructed. Features with a data buffer also require that buffer; successful completion does not mean DW0 contains the complete response.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/features/en/#figure-b198">Base 2.4 Figure 198 · Get Features – Command Dword 10</a><a href="/nvme/figure-reference/features/en/#figure-b201">Base 2.4 Figure 201 · Completion Queue Entry Dword 0 when Select is set to 11b</a><a href="/nvme/figure-reference/features/en/#figure-b466">Base 2.4 Figure 466 · Set Features – Feature Identifiers</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.12 · Figure 198 · Get Features – Command Dword 10 · Printed pages 209–210 · PDF 235–236</li><li>Base 2.4 · §5.2.12 · Figure 201 · Completion Queue Entry Dword 0 when Select is set to 11b · Printed pages 212 · PDF 238</li><li>Base 2.4 · §5.2.30 · Figure 466 · Set Features – Feature Identifiers · Printed pages 457–459 · PDF 483–485</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-features-02" data-scenario="features-02"><h3><span class="qr-number">EXERCISE 02</span>How many queues follow from a request for sixteen?</h3>
<p class="qr-case-question">A driver requests sixteen SQs and sixteen CQs, then creates QIDs 1 through 16. Does the response allow that?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>Set Features FID=07h requests NSQR=15 and NCQR=15; successful DW0=00030007h.</li>
<li>CAP.MQES=1023; no Create I/O CQ/SQ commands have been issued.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Decode NCQA/NSQA in the FID=07h completion; read CAP.MQES separately before planning queue creation and depths.</p>
<p data-reasoning="features-02-1"><span class="qr-step">Step 1</span>DW0 has upper half three and lower half seven, allocating four CQs and eight SQs. A request for sixteen is not an allocation of sixteen; the response governs the result.</p>
<p data-reasoning="features-02-2"><span class="qr-step">Step 2</span>MQES=1023 allows up to 1024 entries per I/O queue, distinct from the number of queues. Multiple SQs may share a CQ under valid configuration, so the allocated counts need not match.</p>
<p data-reasoning="features-02-3"><span class="qr-step">Step 3</span>Resources have been allocated, but queues do not yet exist. Establish an appropriate CQ before its SQ and verify each Create completion. Queue counts also do not directly specify MSI-X vector counts.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/features/en/#figure-b472">Base 2.4 Figure 472 · Number of Queues – Command Dword 11</a><a href="/nvme/figure-reference/features/en/#figure-b473">Base 2.4 Figure 473 · Number of Queues – Completion Queue Entry Dword 0</a><a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.30.1.5 · Figure 472 · Number of Queues – Command Dword 11 · Printed pages 465 · PDF 491</li><li>Base 2.4 · §5.2.30.1.5 · Figure 473 · Number of Queues – Completion Queue Entry Dword 0 · Printed pages 466 · PDF 492</li><li>Base 2.4 · §3.1.4.1 · Figure 36 · Offset 0h: CAP – Controller Capabilities · Printed pages 55–58 · PDF 81–84</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-features-03" data-scenario="features-03"><h3><span class="qr-number">EXERCISE 03</span>What do two APST transitions imply after 700 ms idle?</h3>
<p class="qr-case-question">You need to explain the autonomous power path, not merely list the lowest-power state. How do the entries define source states and timing?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>APSTE=1; PS0 entry: ITPT=100, ITPS=2; PS2 entry: ITPT=500, ITPS=3.</li>
<li>PS2 and PS3 are supported non-operational states; other relevant entries are disabled. Start in PS0 with 700 ms of uninterrupted idle.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Identify CNS=01h for APST capability and power-state descriptors → Get Features FID=0Ch, SEL=0 for both APSTE and the full APST buffer.</p>
<p data-reasoning="features-03-1"><span class="qr-step">Step 1</span>The entry index selects the source; ITPS selects the destination. The path is PS0 → after its 100 ms idle threshold, PS2 → after the 500 ms threshold in PS2, PS3. The second timer is not simply counted from the initial PS0 idle instant.</p>
<p data-reasoning="features-03-2"><span class="qr-step">Step 2</span>Ignoring transition time for illustration, 700 ms allows the two thresholds to be reached in sequence. This timeline is not a measurement of the current state: actual transition time and controller behavior matter, and the table is configuration evidence.</p>
<p data-reasoning="features-03-3"><span class="qr-step">Step 3</span>To assess the next I/O’s exit cost, inspect the destination descriptor’s EXLAT. Zero means unreported, not zero latency. Work that interrupts idle also invalidates this uninterrupted-idle timeline.</p>
<div class="qr-table"><table class=""><thead><tr><th scope="col">Source entry</th><th scope="col">Condition</th><th scope="col">Destination state</th></tr></thead><tbody><tr><td>PS0</td><td>Reach the 100 ms idle threshold in PS0</td><td>PS2</td></tr><tr><td>PS2</td><td>Reach the 500 ms idle threshold in PS2</td><td>PS3</td></tr></tbody></table></div>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/features/en/#figure-b475">Base 2.4 Figure 475 · Autonomous Power State Transition – Command Dword 11</a><a href="/nvme/figure-reference/features/en/#figure-b477">Base 2.4 Figure 477 · Autonomous Power State Transition Data Structure Entry</a><a href="/nvme/figure-reference/features/en/#figure-b340">Base 2.4 Figure 340 · Identify – Power State Descriptor Data Structure</a><a href="/nvme/figure-reference/features/en/#figure-b468">Base 2.4 Figure 468 · Power Management – Command Dword 11</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.30.1.7 · Figure 475 · Autonomous Power State Transition – Command Dword 11 · Printed pages 468 · PDF 494</li><li>Base 2.4 · §5.2.30.1.7 · Figure 477 · Autonomous Power State Transition Data Structure Entry · Printed pages 469 · PDF 495</li><li>Base 2.4 · §5.2.14.2.1 · Figure 340 · Identify – Power State Descriptor Data Structure · Printed pages 384–386 · PDF 410–412</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-features-04" data-scenario="features-04"><h3><span class="qr-number">EXERCISE 04</span>Does a slowdown at high temperature establish HCTM activity?</h3>
<p class="qr-case-question">Performance falls while temperature is above TMT1. Which reports strengthen the thermal-management interpretation, and what remains unproven?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>Get Features FID=10h: TMT1=340 K, TMT2=350 K; Identify limits permit these settings.</li>
<li>SMART composite temperature is 345 K; during the test, Thermal Management Temperature 1 Transition Count rises by one and Total Time by 20 seconds.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Identify CNS=01h for HCTM capability and valid temperature limits → Get Features FID=10h, SEL=0 → compare two LID=02h SMART samples.</p>
<p data-reasoning="features-04-1"><span class="qr-step">Step 1</span>345 K is about 71.85°C, between the configured thresholds. Confirm units for settings and measurements; Kelvin is not Celsius, and a feature threshold is not the current temperature.</p>
<p data-reasoning="features-04-2"><span class="qr-step">Step 2</span>The counter and time increases support stage-one host-controlled thermal management activity during the interval. This is stronger than a high-temperature snapshot, but remains interval evidence rather than per-I/O timing.</p>
<p data-reasoning="features-04-3"><span class="qr-step">Step 3</span>You can report that thermal management was active, but cannot attribute the entire slowdown to it. Align measurement intervals, workloads, power states and PCIe link observations to investigate contributions.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/features/en/#figure-b482">Base 2.4 Figure 482 · HCTM – Command Dword 11</a><a href="/nvme/figure-reference/logs/en/#figure-b213">Base 2.4 Figure 213 · SMART / Health Information Log Page</a><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.30.1.10 · Figure 482 · HCTM – Command Dword 11 · Printed pages 472 · PDF 498</li><li>Base 2.4 · §5.2.13.1.3 · Figure 213 · SMART / Health Information Log Page · Printed pages 221–225 · PDF 247–251</li><li>Base 2.4 · §5.2.14.2.1 · Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent · Printed pages 359–360 · PDF 385–386</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-features-05" data-scenario="features-05"><h3><span class="qr-number">EXERCISE 05</span>Does an unchanged HMB address establish an intact return?</h3>
<p class="qr-case-question">After reset, the host clears an HMB at the same address and declares MR=1. Is address equality enough?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>Descriptor address and total size match the previous allocation, but buffer contents have been cleared.</li>
<li>The proposed Host Memory Buffer feature has EHM=1, MR=1. This exercise only interprets the trace; no setting is applied.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Identify CNS=01h for HMB capability; inspect FID=0Dh and retained descriptors/buffer records from before disablement.</p>
<p data-reasoning="features-05-1"><span class="qr-step">Step 1</span>MR=1 declares return of the previous HMB, requiring more than matching address and size: descriptors and buffer contents must also remain consistent. Clearing the buffer breaks that condition.</p>
<p data-reasoning="features-05-2"><span class="qr-step">Step 2</span>EHM=1 requests enablement but cannot validate MR. Observing an enabled feature cannot reconstruct whether the host preserved every byte; lifecycle and memory-management records are needed.</p>
<p data-reasoning="features-05-3"><span class="qr-step">Step 3</span>Newly allocated memory must follow the new-HMB configuration path rather than treating an identical address as preserved contents. Controller capability and host compliance require different evidence.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/features/en/#figure-b545">Base 2.4 Figure 545 · Host Memory Buffer – Command Dword 11</a><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.30.2.3 · Figure 545 · Host Memory Buffer – Command Dword 11 · Printed pages 516–517 · PDF 542–543</li><li>Base 2.4 · §5.2.14.2.1 · Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent · Printed pages 357, 362 · PDF 383, 388</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-features-06" data-scenario="features-06"><h3><span class="qr-number">EXERCISE 06</span>Do weights seven and three guarantee a two-to-one IOPS ratio?</h3>
<p class="qr-case-question">Measured high- and low-priority IOPS do not match configured weights. Does that prove an arbitration defect?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>CC.AMS selects a supported weighted arbitration mode; FID=01h reports HPW=7, MPW=3, LPW=3, AB=2.</li>
<li>High- and low-priority workloads use different I/O sizes and read/write mixes.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Read CAP and CC.AMS → Get Features FID=01h, SEL=0 → correlate SQ priorities and actual workloads.</p>
<p data-reasoning="features-06-1"><span class="qr-step">Step 1</span>HPW=7 and LPW=3 encode per-round weights of eight and four commands. AB=2 instead encodes a burst of 2^2=4. Similar-looking numbers do not necessarily use the same encoding.</p>
<p data-reasoning="features-06-2"><span class="qr-step">Step 2</span>Weights describe command-service opportunities, not equal work for commands with different sizes and execution costs. Eight-to-four weights do not directly guarantee a steady two-to-one IOPS or bandwidth ratio.</p>
<p data-reasoning="features-06-3"><span class="qr-step">Step 3</span>Arbitration validation needs the mode, SQ priorities, pending work and observation interval, evaluated against the specified service rules. An application throughput chart alone does not establish a violation.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/features/en/#figure-b467">Base 2.4 Figure 467 · Arbitration &amp; Command Processing – Command Dword 11</a><a href="/nvme/figure-reference/init/en/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a><a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.30.1.1 · Figure 467 · Arbitration &amp; Command Processing – Command Dword 11 · Printed pages 460 · PDF 486</li><li>Base 2.4 · §3.1.4.5 · Figure 41 · Offset 14h: CC – Controller Configuration · Printed pages 60–63 · PDF 86–89</li><li>Base 2.4 · §3.1.4.1 · Figure 36 · Offset 0h: CAP – Controller Capabilities · Printed pages 55–58 · PDF 81–84</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
</section>
<nav class="qr-toc" id="figure-index" aria-label="Volume figure index"><h2>Figures in this volume</h2><ol>
<li><a href="#figure-b198">Base 2.4 Figure 198 · Get Features – Command Dword 10</a></li>
<li><a href="#figure-b201">Base 2.4 Figure 201 · Completion Queue Entry Dword 0 when Select is set to 11b</a></li>
<li><a href="#figure-b464">Base 2.4 Figure 464 · Set Features – Command Dword 10</a></li>
<li><a href="#figure-b466">Base 2.4 Figure 466 · Set Features – Feature Identifiers</a></li>
<li><a href="#figure-b340">Base 2.4 Figure 340 · Identify – Power State Descriptor Data Structure</a></li>
<li><a href="#figure-b467">Base 2.4 Figure 467 · Arbitration &amp; Command Processing – Command Dword 11</a></li>
<li><a href="#figure-b468">Base 2.4 Figure 468 · Power Management – Command Dword 11</a></li>
<li><a href="#figure-b471">Base 2.4 Figure 471 · Volatile Write Cache – Command Dword 11</a></li>
<li><a href="#figure-b472">Base 2.4 Figure 472 · Number of Queues – Command Dword 11</a></li>
<li><a href="#figure-b473">Base 2.4 Figure 473 · Number of Queues – Completion Queue Entry Dword 0</a></li>
<li><a href="#figure-b475">Base 2.4 Figure 475 · Autonomous Power State Transition – Command Dword 11</a></li>
<li><a href="#figure-b477">Base 2.4 Figure 477 · Autonomous Power State Transition Data Structure Entry</a></li>
<li><a href="#figure-b482">Base 2.4 Figure 482 · HCTM – Command Dword 11</a></li>
<li><a href="#figure-b543">Base 2.4 Figure 543 · Interrupt Coalescing – Command Dword 11</a></li>
<li><a href="#figure-b545">Base 2.4 Figure 545 · Host Memory Buffer – Command Dword 11</a></li>
<li><a href="#figure-b294">Base 2.4 Figure 294 · FDP Configuration Descriptor</a></li>
<li><a href="#figure-n21">NVM Command Set 1.3 Figure 21 · Reclaim Unit Handle Status Descriptor</a></li>
</ol></nav>
<article class="qr-card" id="figure-b198" data-figure="B198">
<h2><span class="qr-number">01</span>Get Features – Command Dword 10</h2>
<p class="qr-original">Base 2.4 · Figure 198 · Get Features – Command Dword 10</p>
<p class="qr-location">§5.2.12 · Printed pages 209–210 · PDF 235–236</p>
<p class="qr-explanation" data-paragraph="B198-1"><span class="qr-step">01.1 · Use</span>If a returned feature value differs from the last write, first check SEL. Get Features does not always read the current setting.</p>
<p class="qr-explanation" data-paragraph="B198-2"><span class="qr-step">01.2 · Fields and relationships</span>FID bits 7:0 selects the feature. SEL bits 10:8 values 0/1/2/3 select Current, Default, Saved or Supported Capabilities. A saved-value request falls back to Default if saving is unsupported or no saved value exists.</p>
<p class="qr-explanation" data-paragraph="B198-3"><span class="qr-step">01.3 · Interpretation and example</span>DW0=4 with SEL=3 is a capability bitmap, not a current feature value of 4. Decode it through Figure 201 and retain SEL and the feature’s target when comparing settings.</p>
<p class="qr-tags">Search terms: Get Features · FID · SEL · current · default · saved</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/features/en/#figure-b201">Base 2.4 Figure 201 · Completion Queue Entry Dword 0 when Select is set to 11b</a><a href="/nvme/figure-reference/features/en/#figure-b464">Base 2.4 Figure 464 · Set Features – Command Dword 10</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b201" data-figure="B201">
<h2><span class="qr-number">02</span>Completion Queue Entry Dword 0 when Select is set to 11b</h2>
<p class="qr-original">Base 2.4 · Figure 201 · Completion Queue Entry Dword 0 when Select is set to 11b</p>
<p class="qr-location">§5.2.12 · Printed pages 212 · PDF 238</p>
<p class="qr-explanation" data-paragraph="B201-1"><span class="qr-step">02.1 · Use</span>Use this table only for a Get Features SEL=3 response. It reports operations supported by a feature, not the current value returned by SEL=0.</p>
<p class="qr-explanation" data-paragraph="B201-2"><span class="qr-step">02.2 · Fields and relationships</span>DW0 bit 2 is CHANG, bit 1 NSSPEC and bit 0 SVBL. NSSPEC=0 does not by itself mean controller scope; consult the feature and effects log. CHANG=1 indicates changeable attributes, not reversibility of every entered state.</p>
<p class="qr-explanation" data-paragraph="B201-3"><span class="qr-step">02.3 · Interpretation and example</span>DW0=6 means changeable, namespace-specific and not saveable. If permanent write protection has already been entered, CHANG does not promise it can be undone.</p>
<p class="qr-tags">Search terms: SEL 3 · CHANG · NSSPEC · SVBL</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/features/en/#figure-b198">Base 2.4 Figure 198 · Get Features – Command Dword 10</a><a href="/nvme/figure-reference/maintenance/en/#figure-b541">Base 2.4 Figure 541 · Write Protection – Command Dword 11</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b464" data-figure="B464">
<h2><span class="qr-number">03</span>Set Features – Command Dword 10</h2>
<p class="qr-original">Base 2.4 · Figure 464 · Set Features – Command Dword 10</p>
<p class="qr-location">§5.2.30 · Printed pages 457 · PDF 483</p>
<p class="qr-explanation" data-paragraph="B464-1"><span class="qr-step">03.1 · Use</span>When a setting works immediately but differs after reset, check the save request and then the feature’s persistence rules.</p>
<p class="qr-explanation" data-paragraph="B464-2"><span class="qr-step">03.2 · Fields and relationships</span>FID occupies bits 7:0 and SV bit 31; bits 30:8 are reserved. SV=1 requests saved attributes across all power states and resets. An unsaveable FID returns Feature Identifier Not Saveable.</p>
<p class="qr-explanation" data-paragraph="B464-3"><span class="qr-step">03.3 · Interpretation and example</span>SV=0 does not mean every state must disappear on the next reset. Some features intrinsically retain particular states. Saveability and persistence are separate questions.</p>
<p class="qr-tags">Search terms: Set Features · SV · FID · Feature Identifier Not Saveable</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/features/en/#figure-b201">Base 2.4 Figure 201 · Completion Queue Entry Dword 0 when Select is set to 11b</a><a href="/nvme/figure-reference/features/en/#figure-b466">Base 2.4 Figure 466 · Set Features – Feature Identifiers</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b466" data-figure="B466">
<h2><span class="qr-number">04</span>Set Features – Feature Identifiers</h2>
<p class="qr-original">Base 2.4 · Figure 466 · Set Features – Feature Identifiers</p>
<p class="qr-location">§5.2.30 · Printed pages 457–459 · PDF 483–485</p>
<p class="qr-explanation" data-paragraph="B466-1"><span class="qr-step">04.1 · Use</span>Start here when you have only an FID or need its scope and data-buffer requirement. Rows referring to NVM delegate the definition rather than denoting an inactive FID.</p>
<p class="qr-explanation" data-paragraph="B466-2"><span class="qr-step">04.2 · Fields and relationships</span>Columns cover current-setting persistence, data-buffer usage, name and scope. The persistence-column footnote limits its interpretation to unsaveable features; it does not override Saved-value behavior for saveable ones.</p>
<p class="qr-explanation" data-paragraph="B466-3"><span class="qr-step">04.3 · Interpretation and example</span>APST FID=0Ch uses a data buffer of per-state entries; Power Management FID=02h mainly uses CDW11. Capturing CDW11 without the APST table cannot reconstruct that configuration.</p>
<p class="qr-tags">Search terms: FID · Feature Identifier · scope · persistence · data buffer</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/features/en/#figure-b475">Base 2.4 Figure 475 · Autonomous Power State Transition – Command Dword 11</a><a href="/nvme/figure-reference/features/en/#figure-b477">Base 2.4 Figure 477 · Autonomous Power State Transition Data Structure Entry</a><a href="/nvme/figure-reference/features/en/#figure-b468">Base 2.4 Figure 468 · Power Management – Command Dword 11</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b340" data-figure="B340">
<h2><span class="qr-number">05</span>Identify – Power State Descriptor Data Structure</h2>
<p class="qr-original">Base 2.4 · Figure 340 · Identify – Power State Descriptor Data Structure</p>
<p class="qr-location">§5.2.14.2.1 · Printed pages 384–386 · PDF 410–412</p>
<p class="qr-explanation" data-paragraph="B340-1"><span class="qr-step">05.1 · Use</span>Inspect each 32-byte descriptor when comparing power states or investigating wake latency. State numbers are selectors, not direct power or performance rankings.</p>
<p class="qr-explanation" data-paragraph="B340-2"><span class="qr-step">05.2 · Fields and relationships</span>NOPS bit 25 distinguishes I/O processing. MP bits 15:0 and MXPS bit 24 jointly encode power. ENLAT bits 63:32/EXLAT bits 95:64 use microseconds. IDLP/IPS describes idle power; RRT/RRL/RWT/RWL are relative rankings. Later fields include active power, power-loss timings and bandwidth.</p>
<p class="qr-explanation" data-paragraph="B340-3"><span class="qr-step">05.3 · Interpretation and example</span>MP=350 with MXPS=0 means 3.50 W; MXPS=1 means 0.035 W. EXLAT=0 means unreported, not zero latency. Check NOPS and valid power/latency values before selecting an APST destination.</p>
<p class="qr-tags">Search terms: PSD · NOPS · MP · MXPS · ENLAT · EXLAT · IDLP · IPS · RRT · RRL</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/features/en/#figure-b468">Base 2.4 Figure 468 · Power Management – Command Dword 11</a><a href="/nvme/figure-reference/features/en/#figure-b477">Base 2.4 Figure 477 · Autonomous Power State Transition Data Structure Entry</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b467" data-figure="B467">
<h2><span class="qr-number">06</span>Arbitration &amp; Command Processing – Command Dword 11</h2>
<p class="qr-original">Base 2.4 · Figure 467 · Arbitration &amp; Command Processing – Command Dword 11</p>
<p class="qr-location">§5.2.30.1.1 · Printed pages 460 · PDF 486</p>
<p class="qr-explanation" data-paragraph="B467-1"><span class="qr-step">06.1 · Use</span>Use this table for SQ priority and command-fetch behavior. Weights do not guarantee a fixed application IOPS ratio; arbitration mode and workload still matter.</p>
<p class="qr-explanation" data-paragraph="B467-2"><span class="qr-step">06.2 · Fields and relationships</span>HPW bits 31:24, MPW bits 23:16 and LPW bits 15:8 encode per-round class command counts minus one. AB bits 2:0 limits commands fetched at once from one SQ as 2^AB, except AB=7 means unlimited.</p>
<p class="qr-explanation" data-paragraph="B467-3"><span class="qr-step">06.3 · Interpretation and example</span>HPW=3 means four commands while AB=3 means a burst of eight. Identical raw values use different encodings. Confirm CC.AMS before interpreting priority weights.</p>
<p class="qr-tags">Search terms: FID 01h · HPW · MPW · LPW · AB · arbitration</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b468" data-figure="B468">
<h2><span class="qr-number">07</span>Power Management – Command Dword 11</h2>
<p class="qr-original">Base 2.4 · Figure 468 · Power Management – Command Dword 11</p>
<p class="qr-location">§5.2.30.1.2 · Printed pages 461 · PDF 487</p>
<p class="qr-explanation" data-paragraph="B468-1"><span class="qr-step">07.1 · Use</span>This CDW11 defines an explicit host-requested power-state transition. It is separate from APST; PS alone does not reconstruct autonomous transitions.</p>
<p class="qr-explanation" data-paragraph="B468-2"><span class="qr-step">07.2 · Fields and relationships</span>PS bits 4:0 selects a state, WH bits 7:5 supplies a workload hint, and IIELL bits 31:16 uses 100-microsecond units for supported idle-exit limits on operational states. IIELLSS determines its scope.</p>
<p class="qr-explanation" data-paragraph="B468-3"><span class="qr-step">07.3 · Interpretation and example</span>IIELL=5 means 500 microseconds, not 5 ms. With the capability supported, a nonzero IIELL for a non-operational state causes Invalid Field in Command. Identify the state type through its descriptor first.</p>
<p class="qr-tags">Search terms: FID 02h · PS · WH · IIELL · IIELLSS</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/features/en/#figure-b340">Base 2.4 Figure 340 · Identify – Power State Descriptor Data Structure</a><a href="/nvme/figure-reference/features/en/#figure-b475">Base 2.4 Figure 475 · Autonomous Power State Transition – Command Dword 11</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b471" data-figure="B471">
<h2><span class="qr-number">08</span>Volatile Write Cache – Command Dword 11</h2>
<p class="qr-original">Base 2.4 · Figure 471 · Volatile Write Cache – Command Dword 11</p>
<p class="qr-location">§5.2.30.1.4 · Printed pages 464–465 · PDF 490–491</p>
<p class="qr-explanation" data-paragraph="B471-1"><span class="qr-step">08.1 · Use</span>Inspect WCE with cache presence and command FUA when assessing whether a Write completion may depend on volatile cache. WCE is not the hardware-presence capability.</p>
<p class="qr-explanation" data-paragraph="B471-2"><span class="qr-step">08.2 · Fields and relationships</span>CDW11 bit 0 enables/disables the cache; bits 31:1 are reserved. Presence also depends on Identify and namespace/FDP configuration. Flush and FUA have their own nonvolatile requirements.</p>
<p class="qr-explanation" data-paragraph="B471-3"><span class="qr-step">08.3 · Interpretation and example</span>WCE=1 does not prove that a particular completed Write exists only in cache: the command may have FUA=1. Preserve capability, WCE and command fields when investigating retention.</p>
<p class="qr-tags">Search terms: FID 06h · WCE · VWC · volatile cache · Flush</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a><a href="/nvme/figure-reference/identify/en/#figure-b346">Base 2.4 Figure 346 · Identify – I/O Command Set Independent Identify Namespace Data Structure</a><a href="/nvme/figure-reference/io/en/#figure-n71">NVM Command Set 1.3 Figure 71 · Write – Command Dword 12</a><a href="/nvme/figure-reference/features/en/#figure-b294">Base 2.4 Figure 294 · FDP Configuration Descriptor</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b472" data-figure="B472">
<h2><span class="qr-number">09</span>Number of Queues – Command Dword 11</h2>
<p class="qr-original">Base 2.4 · Figure 472 · Number of Queues – Command Dword 11</p>
<p class="qr-location">§5.2.30.1.5 · Printed pages 465 · PDF 491</p>
<p class="qr-explanation" data-paragraph="B472-1"><span class="qr-step">09.1 · Use</span>Use this table for requested I/O queue allocation during initialization. Counts exclude Admin queues and do not describe individual queue depth.</p>
<p class="qr-explanation" data-paragraph="B472-2"><span class="qr-step">09.2 · Fields and relationships</span>NSQR bits 15:0 requests SQs and NCQR bits 31:16 CQs, both minus-one encoded with maximum raw value FFFEh. Configure before creating I/O queues; actual allocation is returned in CQE DW0.</p>
<p class="qr-explanation" data-paragraph="B472-3"><span class="qr-step">09.3 · Interpretation and example</span>Eight SQs and four CQs use CDW11=00030007h. Do not create queues solely from the requested counts; inspect the actual result in Figure 473.</p>
<p class="qr-tags">Search terms: FID 07h · NSQR · NCQR · queue allocation</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/features/en/#figure-b473">Base 2.4 Figure 473 · Number of Queues – Completion Queue Entry Dword 0</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b473" data-figure="B473">
<h2><span class="qr-number">10</span>Number of Queues – Completion Queue Entry Dword 0</h2>
<p class="qr-original">Base 2.4 · Figure 473 · Number of Queues – Completion Queue Entry Dword 0</p>
<p class="qr-location">§5.2.30.1.5 · Printed pages 466 · PDF 492</p>
<p class="qr-explanation" data-paragraph="B473-1"><span class="qr-step">10.1 · Use</span>Decode the Number of Queues completion here to learn the actual I/O queue resources allocated. Requested and allocated counts can differ.</p>
<p class="qr-explanation" data-paragraph="B473-2"><span class="qr-step">10.2 · Fields and relationships</span>DW0.NSQA bits 15:0 and NCQA bits 31:16 encode actual SQ/CQ counts minus one. This is neither a queue-ID list nor proof that Create commands have established those queues.</p>
<p class="qr-explanation" data-paragraph="B473-3"><span class="qr-step">10.3 · Interpretation and example</span>DW0=00010003h means four SQs and two CQs. Even after requesting eight and four, use the response for subsequent creation. Allocation and queue creation are separate steps.</p>
<p class="qr-tags">Search terms: NSQA · NCQA · CQE DW0 · allocated queues</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/features/en/#figure-b472">Base 2.4 Figure 472 · Number of Queues – Command Dword 11</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b475" data-figure="B475">
<h2><span class="qr-number">11</span>Autonomous Power State Transition – Command Dword 11</h2>
<p class="qr-original">Base 2.4 · Figure 475 · Autonomous Power State Transition – Command Dword 11</p>
<p class="qr-location">§5.2.30.1.7 · Printed pages 468 · PDF 494</p>
<p class="qr-explanation" data-paragraph="B475-1"><span class="qr-step">11.1 · Use</span>If an idle-transition table produces no expected power behavior, check APSTE first. This figure defines only the global switch, not per-state delays.</p>
<p class="qr-explanation" data-paragraph="B475-2"><span class="qr-step">11.2 · Fields and relationships</span>CDW11 bit 0 enables APST when one and disables it when zero, the default. Other bits are reserved. Per-source-state timing and destination settings reside in the APST data structure.</p>
<p class="qr-explanation" data-paragraph="B475-3"><span class="qr-step">11.3 · Interpretation and example</span>APSTE=1 does not immediately select the lowest-power state. The source entry needs nonzero ITPT and the continuous-idle condition must be met. Capture both enablement and the relevant entry.</p>
<p class="qr-tags">Search terms: FID 0Ch · APSTE · APST · autonomous power</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/features/en/#figure-b477">Base 2.4 Figure 477 · Autonomous Power State Transition Data Structure Entry</a><a href="/nvme/figure-reference/features/en/#figure-b340">Base 2.4 Figure 340 · Identify – Power State Descriptor Data Structure</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b477" data-figure="B477">
<h2><span class="qr-number">12</span>Autonomous Power State Transition Data Structure Entry</h2>
<p class="qr-original">Base 2.4 · Figure 477 · Autonomous Power State Transition Data Structure Entry</p>
<p class="qr-location">§5.2.30.1.7 · Printed pages 469 · PDF 495</p>
<p class="qr-explanation" data-paragraph="B477-1"><span class="qr-step">12.1 · Use</span>Decode each eight-byte source-state entry here. Its array index selects the source; ITPS selects the destination. They are not interchangeable.</p>
<p class="qr-explanation" data-paragraph="B477-2"><span class="qr-step">12.2 · Fields and relationships</span>ITPT bits 31:8 is the continuous-idle threshold in milliseconds; zero disables that source entry. ITPS bits 7:3 selects a non-operational destination when ITPT is nonzero. Upper 32 bits and low 3 bits are reserved.</p>
<p class="qr-explanation" data-paragraph="B477-3"><span class="qr-step">12.3 · Interpretation and example</span>For a PS0 entry with ITPT=2000 and ITPS=3, the low Dword is(2000&lt;&lt;8)|(3&lt;&lt;3)=0007D018h. The rule can transition from PS0 to PS3 after more than 2000 ms continuously idle in PS0, not after first entering PS3.</p>
<p class="qr-tags">Search terms: ITPT · ITPS · APST entry · idle transition</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/features/en/#figure-b475">Base 2.4 Figure 475 · Autonomous Power State Transition – Command Dword 11</a><a href="/nvme/figure-reference/features/en/#figure-b340">Base 2.4 Figure 340 · Identify – Power State Descriptor Data Structure</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b482" data-figure="B482">
<h2><span class="qr-number">13</span>HCTM – Command Dword 11</h2>
<p class="qr-original">Base 2.4 · Figure 482 · HCTM – Command Dword 11</p>
<p class="qr-location">§5.2.30.1.10 · Printed pages 472 · PDF 498</p>
<p class="qr-explanation" data-paragraph="B482-1"><span class="qr-step">13.1 · Use</span>Inspect Host Controlled Thermal Management thresholds when performance drops with temperature. They are host-selected controls, not current SMART readings.</p>
<p class="qr-explanation" data-paragraph="B482-2"><span class="qr-step">13.2 · Fields and relationships</span>TMT1 bits 31:16 selects the lighter threshold and TMT2 bits 15:0 the heavier one, both in Kelvin; zero disables that part. Nonzero values must fit Identify limits, and nonzero TMT2 must exceed TMT1.</p>
<p class="qr-explanation" data-paragraph="B482-3"><span class="qr-step">13.3 · Interpretation and example</span>TMT1=343 and TMT2=353 are about 69.85°C and 79.85°C, not 343°C/353°C. Use SMART transition counts and total times to investigate actual activity.</p>
<p class="qr-tags">Search terms: FID 10h · HCTM · TMT1 · TMT2 · Kelvin · throttling</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/logs/en/#figure-b213">Base 2.4 Figure 213 · SMART / Health Information Log Page</a><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b543" data-figure="B543">
<h2><span class="qr-number">14</span>Interrupt Coalescing – Command Dword 11</h2>
<p class="qr-original">Base 2.4 · Figure 543 · Interrupt Coalescing – Command Dword 11</p>
<p class="qr-location">§5.2.30.2.1 · Printed pages 515 · PDF 541</p>
<p class="qr-explanation" data-paragraph="B543-1"><span class="qr-step">14.1 · Use</span>Check coalescing when CQ data exists before its interrupt arrives. It aggregates interrupts without changing command status in CQEs.</p>
<p class="qr-explanation" data-paragraph="B543-2"><span class="qr-step">14.2 · Fields and relationships</span>TIME bits 15:8 uses 100-microsecond units, zero meaning no delay. THR bits 7:0 is the recommended completion threshold minus one. Either field zero implicitly disables coalescing. It applies to I/O queues, not Admin CQ, with additional per-vector configuration.</p>
<p class="qr-explanation" data-paragraph="B543-3"><span class="qr-step">14.3 · Interpretation and example</span>TIME=5/THR=7 specifies recommendations of 500 microseconds and eight entries, not a mandatory 500-microsecond delay per I/O. CQ head updates can restart aggregation conditions, so TIME is not an end-to-end latency bound.</p>
<p class="qr-tags">Search terms: FID 08h · TIME · THR · coalescing · interrupt latency</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/init/en/#figure-p44">PCIe Transport 1.4 Figure 44 · Offset MSIXCAP + 2h: MXC – MSI-X Message Control</a><a href="/nvme/figure-reference/init/en/#figure-p6">PCIe Transport 1.4 Figure 6 · Offset (1000h + ((2y + 1) * (4 &lt;&lt; CAP.DSTRD))): CQyHDBL – Completion Queue y Head Doorbell</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b545" data-figure="B545">
<h2><span class="qr-number">15</span>Host Memory Buffer – Command Dword 11</h2>
<p class="qr-original">Base 2.4 · Figure 545 · Host Memory Buffer – Command Dword 11</p>
<p class="qr-location">§5.2.30.2.3 · Printed pages 516–517 · PDF 542–543</p>
<p class="qr-explanation" data-paragraph="B545-1"><span class="qr-step">15.1 · Use</span>When re-enabling Host Memory Buffer after reset or power changes, inspect MR/EHM so newly allocated memory is not represented as an intact return. HMB is host memory supplied for controller use.</p>
<p class="qr-explanation" data-paragraph="B545-2"><span class="qr-step">15.2 · Fields and relationships</span>EHM bit 0 enables the HMB when set, MR bit 1 declares return of the prior HMB, and HMNARE bit 2 restricts supported non-operational access with Admin-related exceptions. Bit 3 must be zero. MR=1 requires identical size, descriptor address/content and buffer content.</p>
<p class="qr-explanation" data-paragraph="B545-3"><span class="qr-step">15.3 · Interpretation and example</span>If reallocation cleared the buffer, the same physical address does not justify MR=1. With EHM=0, CDW12–15 are ignored, so their bytes do not establish an enabled allocation.</p>
<p class="qr-tags">Search terms: FID 0Dh · HMB · EHM · MR · HMNARE</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b294" data-figure="B294">
<h2><span class="qr-number">16</span>FDP Configuration Descriptor</h2>
<p class="qr-original">Base 2.4 · Figure 294 · FDP Configuration Descriptor</p>
<p class="qr-location">§5.2.13.1.29 · Printed pages 293–295 · PDF 319–321</p>
<p class="qr-explanation" data-paragraph="B294-1"><span class="qr-step">16.1 · Use</span>Check the active FDP configuration before decoding resource counts or Placement Identifiers. RGIF determines the split between Reclaim Group and Placement Handle in a PID.</p>
<p class="qr-explanation" data-paragraph="B294-2"><span class="qr-step">16.2 · Fields and relationships</span>DSZE bytes 1:0 gives descriptor size. FDPA byte 2 contains FDPCV validity, FDPVWC and RGIF. NRG bytes 7:4/NRUH bytes 9:8 are direct counts; MAXPIDS bytes 11:10 is minus-one encoded. RUNS bytes 23:16 counts nominal bytes; ERUTL bytes 27:24 seconds, with zero unreported.</p>
<p class="qr-explanation" data-paragraph="B294-3"><span class="qr-step">16.3 · Interpretation and example</span>NRUH=4 means four handle descriptors, not five; MAXPIDS=3 corresponds to four placement identifiers. Vendor bytes and padding may follow the list, so use DSZE to find the next configuration.</p>
<p class="qr-tags">Search terms: LID 20h · FDP · DSZE · FDPCV · RGIF · NRG · NRUH · RUNS · ERUTL</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/features/en/#figure-n21">NVM Command Set 1.3 Figure 21 · Reclaim Unit Handle Status Descriptor</a><a href="/nvme/figure-reference/io/en/#figure-n71">NVM Command Set 1.3 Figure 71 · Write – Command Dword 12</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-n21" data-figure="N21">
<h2><span class="qr-number">17</span>Reclaim Unit Handle Status Descriptor</h2>
<p class="qr-original">NVM Command Set 1.3 · Figure 21 · Reclaim Unit Handle Status Descriptor</p>
<p class="qr-location">§3.2.1.1 · Printed pages 26 · PDF 26</p>
<p class="qr-explanation" data-paragraph="N21-1"><span class="qr-step">17.1 · Use</span>Use this NVM-specific status descriptor to inspect currently writable capacity in the Reclaim Unit referenced by a placement. Nominal capacity is not a substitute for this snapshot.</p>
<p class="qr-explanation" data-paragraph="N21-2"><span class="qr-step">17.2 · Fields and relationships</span>PID bytes 1:0 and RUHID bytes 3:2 identify placement and handle. EARUTR bytes 7:4 estimates remaining seconds, with zero unreported. RUAMW bytes 15:8 counts currently writable logical blocks. The remaining 16 bytes are reserved.</p>
<p class="qr-explanation" data-paragraph="N21-3"><span class="qr-step">17.3 · Interpretation and example</span>RUAMW=1000 with 4 KiB blocks means 4,096,000 bytes in block units and can differ in either direction from RUNS nominal capacity. EARUTR=0 does not mean immediate expiration.</p>
<p class="qr-tags">Search terms: RUH · PID · RUHID · EARUTR · RUAMW · I/O Management Receive</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/features/en/#figure-b294">Base 2.4 Figure 294 · FDP Configuration Descriptor</a><a href="/nvme/figure-reference/identify/en/#figure-n125">NVM Command Set 1.3 Figure 125 · LBA Format Data Structure, NVM Command Set Specific</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<footer id="source-files"><h2>Source documents</h2><p>Locations refer to the supplied ratified PDFs. For Base, PDF page = printed page +26; the other two use identical page numbers. Original figure numbers and English titles are retained for PDF search. Source PDFs are not redistributed.</p><ul class="qr-sources"><li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li></ul></footer>
</main></div>
