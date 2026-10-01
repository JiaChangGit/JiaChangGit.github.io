---
layout: "post"
title: "NVMe Figures and Scenarios 06 · Health, Events, and Diagnostic Logs"
date: "2026-09-29 09:00:00 +0800"
categories: ["nvme"]
tags: ["NVMe", "Reference"]
permalink: "/nvme/figure-reference/logs/en/"
nvme_quickref: true
last_modified_at: "2026-10-01"
lang: "en"
description: "NVMe scenarios and source figures: lookup routes, field reasoning, worked answers and precise specification locations."
---

<div class="nvme-quickref">
<nav class="qr-top" aria-label="Editions and index"><a href="#content">Skip to content</a><a href="/nvme/figure-reference/en/">Index</a><a href="/nvme/figure-reference/logs/zh-tw/">繁體中文</a><a href="/DOCS/nvme-quick-reference/logs.html">Chinese HTML</a></nav>
<main id="content">
<header><p class="qr-eyebrow">LOOKUP · FIELD INTERPRETATION · SOURCE LOCATIONS</p><h1>NVMe Figures and Scenarios 06 · Health, Events, and Diagnostic Logs</h1><p class="qr-intro">Validate retrieval parameters and support, then distinguish current state, cumulative counters and historical snapshots. Telemetry and persistent-event versions, lengths and retrieval lifecycles determine whether records can be combined.</p></header>
<aside class="qr-note"><p>Each source figure has a use, field guide and worked interpretation. Example numbers are illustrative, not assumed device settings. Apply the conditions belonging to the field and command.</p><p>Use browser Find for fields, FID, LID, CNS or Figure. Positions follow the source: a byte is 8 bits and a Dword is 4 bytes. An index counts entries; an offset measures displacement from an origin in the specified unit.</p><p>FID (Feature Identifier) selects a feature; LID (Log Page Identifier) selects a log page; CNS (Controller or Namespace Structure) selects the structure returned by Identify.</p></aside>
<nav class="qr-top" aria-label="Volume entry points"><a href="#exercises">Start with scenarios</a><a href="#figure-index">Go to figures</a></nav>
<section id="exercises"><h2>Try the scenarios first</h2>
<p>All observations are hypothetical, not device measurements. Before opening an answer, identify the interface, target, fields and supported conclusion. These are specification exercises; no commands are executed.</p>
<nav class="qr-toc" id="exercise-toc" aria-label="Exercise index"><ol>
<li><a href="#exercise-logs-01">Does 120% Percentage Used mean the drive has failed?</a></li>
<li><a href="#exercise-logs-02">How much data does a four-unit DUW increase represent?</a></li>
<li><a href="#exercise-logs-03">Does specifying an NSID guarantee per-namespace SMART?</a></li>
<li><a href="#exercise-logs-04">Do two namespace alerts describe one shared group?</a></li>
<li><a href="#exercise-logs-05">Does FLBA=0 identify a failed LBA when self-test is idle?</a></li>
<li><a href="#exercise-logs-06">Can Telemetry chunks from different generations be combined?</a></li>
<li><a href="#exercise-logs-07">Where does the next Persistent Event Log record begin?</a></li>
</ol></nav>
<article class="qr-card qr-case" id="exercise-logs-01" data-scenario="logs-01"><h3><span class="qr-number">EXERCISE 01</span>Does 120% Percentage Used mean the drive has failed?</h3>
<p class="qr-case-question">A health report shows only a red “120%.” Separate the conclusions that SMART actually supports.</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>LID=02h: Percentage Used=120; Available Spare=9; Available Spare Threshold=10; the spare critical-warning bit is one.</li>
<li>Composite Temperature=300 K; no recent I/O success/failure trace is provided.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Get Log Page LID=02h for SMART/Health; retain the warning bitmap and individual measurements instead of combining them into one health score.</p>
<p data-reasoning="logs-01-1"><span class="qr-step">Step 1</span>Percentage Used estimates endurance consumption and may exceed 100. A value of 120 is not 120% damaged and does not alone establish inability to read or write.</p>
<p data-reasoning="logs-01-2"><span class="qr-step">Step 2</span>Available Spare=9 is below threshold 10 with the corresponding warning asserted. That is a directly supported spare warning. Temperature 300 K is about 26.85°C, a different measurement that cannot be added to percentages.</p>
<p data-reasoning="logs-01-3"><span class="qr-step">Step 3</span>Report endurance estimate, current warnings and recent error/I/O behavior separately. Continued service decisions also need system requirements and observed behavior; the log does not supply one universal decision score.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/logs/en/#figure-b213">Base 2.4 Figure 213 · SMART / Health Information Log Page</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.13.1.3 · Figure 213 · SMART / Health Information Log Page · Printed pages 221–225 · PDF 247–251</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-logs-02" data-scenario="logs-02"><h3><span class="qr-number">EXERCISE 02</span>How much data does a four-unit DUW increase represent?</h3>
<p class="qr-case-question">Monitoring multiplies a SMART Data Units Written delta by 512 and reports a tiny workload. What is missing?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>DUW for the same target changes from 1000 to 1004; counters are valid, without reset or saturation; samples are 60 seconds apart.</li>
<li>Host Write Commands rises by 80; no complete list of command lengths is available.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Take two LID=02h samples, retaining NSID, timestamps, DUW and Host Write Commands.</p>
<p data-reasoning="logs-02-1"><span class="qr-step">Step 1</span>DUW reports thousands of 512-byte units, rounded up. A delta of four corresponds to roughly 4×1000×512=2048000 bytes, not 2048 bytes.</p>
<p data-reasoning="logs-02-2"><span class="qr-step">Step 2</span>Both endpoints are rounded, so this is not the exact payload byte count for those 60 seconds. Dividing by 80 yields only an approximate average, not proof that all Writes had the same size.</p>
<p data-reasoning="logs-02-3"><span class="qr-step">Step 3</span>For one command’s length, use its NLB and active LBA format; cumulative deltas serve longer-term trends. Host-written data also must not be equated directly with physical NAND writes.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/logs/en/#figure-b213">Base 2.4 Figure 213 · SMART / Health Information Log Page</a><a href="/nvme/figure-reference/io/en/#figure-n54">NVM Command Set 1.3 Figure 54 · Read – Command Dword 12</a><a href="/nvme/figure-reference/identify/en/#figure-n125">NVM Command Set 1.3 Figure 125 · LBA Format Data Structure, NVM Command Set Specific</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.13.1.3 · Figure 213 · SMART / Health Information Log Page · Printed pages 221–225 · PDF 247–251</li><li>NVM Command Set 1.3 · §3.3.4 · Figure 54 · Read – Command Dword 12 · Printed pages 49 · PDF 49</li><li>NVM Command Set 1.3 · §4.1.5.1 · Figure 125 · LBA Format Data Structure, NVM Command Set Specific · Printed pages 94 · PDF 94</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-logs-03" data-scenario="logs-03"><h3><span class="qr-number">EXERCISE 03</span>Does specifying an NSID guarantee per-namespace SMART?</h3>
<p class="qr-case-question">A report copies one SMART page to every namespace and labels each as individual usage. Does capability data support that?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>Identify Controller LPA reports no per-namespace SMART/Health support.</li>
<li>The current LID=02h sample uses NSID=FFFFFFFFh; the controller has four active namespaces.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Identify CNS=01h for LPA; select NSID according to SMART rules. A report label cannot create a granularity the capability does not provide.</p>
<p data-reasoning="logs-03-1"><span class="qr-step">Step 1</span>This is not four independent per-namespace measurements. Label the FFFFFFFFh report by its aggregate scope; copying and summing it would count the same measurement four times.</p>
<p data-reasoning="logs-03-2"><span class="qr-step">Step 2</span>A specific-NSID request requires per-namespace SMART support and the log’s namespace rules. The existence of an NSID field in Get Log Page does not grant every LID arbitrary reporting granularity.</p>
<p data-reasoning="logs-03-3"><span class="qr-step">Step 3</span>For Endurance Group granularity, inspect namespace ENDGID and LID=09h. Those remain group statistics, not automatically individual namespace or filesystem measurements.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a><a href="/nvme/figure-reference/logs/en/#figure-b213">Base 2.4 Figure 213 · SMART / Health Information Log Page</a><a href="/nvme/figure-reference/logs/en/#figure-b225">Base 2.4 Figure 225 · Endurance Group Information Log Page</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.14.2.1 · Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent · Printed pages 355–356 · PDF 381–382</li><li>Base 2.4 · §5.2.13.1.3 · Figure 213 · SMART / Health Information Log Page · Printed pages 221–225 · PDF 247–251</li><li>Base 2.4 · §5.2.13.1.10 · Figure 225 · Endurance Group Information Log Page · Printed pages 238–239 · PDF 264–265</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-logs-04" data-scenario="logs-04"><h3><span class="qr-number">EXERCISE 04</span>Do two namespace alerts describe one shared group?</h3>
<p class="qr-case-question">Management issues endurance alerts for NSID=2 and NSID=9. How can you determine whether they duplicate one group-level condition?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>Both namespaces identify ENDGID=3; LID=09h with LSI=3 has a nonzero Critical Warning.</li>
<li>No result is available for group 4, and no inventory change is observed during the interval.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Identify CNS=00h for each NSID → ENDGID → Get Log Page LID=09h with LSI=ENDGID.</p>
<p data-reasoning="logs-04-1"><span class="qr-step">Step 1</span>Both namespaces map to group 3. One group condition can affect how both namespaces are presented, but it remains one group-level source. Retain the mapping rather than counting two independent group failures.</p>
<p data-reasoning="logs-04-2"><span class="qr-step">Step 2</span>For this LID, LSI selects the Endurance Group, not an NSID or high transfer-length bits. Substituting NSID=9 into LSI would select another target rather than answer the group-3 question.</p>
<p data-reasoning="logs-04-3"><span class="qr-step">Step 3</span>A warning in group 3 does not establish a warning in every group. To compare group 4, verify its existence and obtain corresponding measurements from the same interval.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/logs/en/#figure-b225">Base 2.4 Figure 225 · Endurance Group Information Log Page</a><a href="/nvme/figure-reference/logs/en/#figure-b205">Base 2.4 Figure 205 · Get Log Page – Command Dword 11</a><a href="/nvme/figure-reference/identify/en/#figure-n123">NVM Command Set 1.3 Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.13.1.10 · Figure 225 · Endurance Group Information Log Page · Printed pages 238–239 · PDF 264–265</li><li>Base 2.4 · §5.2.13 · Figure 205 · Get Log Page – Command Dword 11 · Printed pages 214 · PDF 240</li><li>NVM Command Set 1.3 · §4.1.5.1 · Figure 123 · Identify – Identify Namespace Data Structure, NVM Command Set · Printed pages 90–93 · PDF 90–93</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-logs-05" data-scenario="logs-05"><h3><span class="qr-number">EXERCISE 05</span>Does FLBA=0 identify a failed LBA when self-test is idle?</h3>
<p class="qr-case-question">A tool reports both “test stuck at 45%” and “LBA 0 failed.” Find the two validity errors.</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>LID=06h: current DSTOS=0, with percentage bytes containing 45; newest result DSTR=2.</li>
<li>The latest result has VDINFO.FVLD=0 and all-zero raw FLBA bytes.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Get Log Page LID=06h; read current operation, then newest-result DSTR and VDINFO, and only then interpret diagnostic fields.</p>
<p data-reasoning="logs-05-1"><span class="qr-step">Step 1</span>DSTOS=0 means no self-test is in progress, so ignore the percentage field. It is not a valid stalled 45% progress measurement from which to calculate a stall duration.</p>
<p data-reasoning="logs-05-2"><span class="qr-step">Step 2</span>DSTR=2 identifies termination by Controller Level Reset, distinct from a test detecting media failure. Report the termination reason rather than collapsing every nonzero result into a detected media defect.</p>
<p data-reasoning="logs-05-3"><span class="qr-step">Step 3</span>FVLD=0 makes FLBA invalid. Zero is merely raw content in an invalid field, not evidence of failed LBA zero. Apply the respective validity bits to NSID, SCT and SC as well.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/maintenance/en/#figure-b218">Base 2.4 Figure 218 · Device Self-test Log Page</a><a href="/nvme/figure-reference/maintenance/en/#figure-b219">Base 2.4 Figure 219 · Self-test Result Data Structure</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.13.1.7 · Figure 218 · Device Self-test Log Page · Printed pages 230 · PDF 256</li><li>Base 2.4 · §5.2.13.1.7 · Figure 219 · Self-test Result Data Structure · Printed pages 231–232 · PDF 257–258</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-logs-06" data-scenario="logs-06"><h3><span class="qr-number">EXERCISE 06</span>Can Telemetry chunks from different generations be combined?</h3>
<p class="qr-case-question">You collect controller-initiated Telemetry in chunks and then notice different headers. Is the combined file one coherent capture?</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>Initial LID=08h header: TCDGN=10, TCDA=1, DA1LB=3; final reread: TCDGN=11, TCDA=1.</li>
<li>Data is read in chunks between the headers; there is no complete record assigning each chunk to a generation.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Get Log Page LID=08h, retaining RAE, headers and each offset; compare TCDGN, TCDA and Data Area boundaries.</p>
<p data-reasoning="logs-06-1"><span class="qr-step">Step 1</span>The generation change prevents claiming these chunks as one coherent capture. Mark consistency as unverified and reacquire through the log’s capture/acknowledgment process rather than merely replacing the file header.</p>
<p data-reasoning="logs-06-2"><span class="qr-step">Step 2</span>DA1LB=3 places the Area 1 endpoint at block three; block zero is the 512-byte header. Header plus Area 1 therefore spans 4×512=2048 bytes. Correct length does not resolve generation inconsistency.</p>
<p data-reasoning="logs-06-3"><span class="qr-step">Step 3</span>TCDA concerns update acknowledgment, not payload decoding. Even a coherent capture can contain vendor-defined internals; a common header does not define every vendor byte.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/logs/en/#figure-b223">Base 2.4 Figure 223 · Telemetry Controller-Initiated Log Page</a><a href="/nvme/figure-reference/logs/en/#figure-b204">Base 2.4 Figure 204 · Get Log Page – Command Dword 10</a><a href="/nvme/figure-reference/logs/en/#figure-b208">Base 2.4 Figure 208 · Get Log Page – Command Dword 14</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.13.1.9 · Figure 223 · Telemetry Controller-Initiated Log Page · Printed pages 236–237 · PDF 262–263</li><li>Base 2.4 · §5.2.13 · Figure 204 · Get Log Page – Command Dword 10 · Printed pages 213 · PDF 239</li><li>Base 2.4 · §5.2.13 · Figure 208 · Get Log Page – Command Dword 14 · Printed pages 214–215 · PDF 240–241</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
<article class="qr-card qr-case" id="exercise-logs-07" data-scenario="logs-07"><h3><span class="qr-number">EXERCISE 07</span>Where does the next Persistent Event Log record begin?</h3>
<p class="qr-case-question">A parser loses alignment after its first record and gets Command Sequence Error when establishing context again. Inspect lifecycle and length separately.</p><div class="qr-observations"><h4>Hypothetical observations and assumptions</h4><ul>
<li>ACT=3 succeeds with header RCE=0; the context has not been released. First record: offset=512, EHL=21, EL=28, VSIL=8.</li>
<li>The header’s total length accommodates this record; ET/ETR identify a supported format.</li>
</ul></div><details class="qr-answer"><summary>Show answer: lookup route and reasoning</summary>
<p class="qr-route"><strong>Lookup sequence: </strong>Get Log Page LID=0Dh with ACT-controlled context; after the header, use ACT=0 on the same report and traverse event headers.</p>
<p data-reasoning="logs-07-1"><span class="qr-step">Step 1</span>For ACT=3, RCE=0 means no reporting context existed before processing, not that none exists after success. A subsequent ACT=1 establishment conflicts with that context; subsequent reads should use it.</p>
<p data-reasoning="logs-07-2"><span class="qr-step">Step 2</span>The common header is EHL+3=24 bytes. EL=28 already includes VSIL=8, leaving 20 bytes of Event Data. The next record begins at 512+24+28=564; do not add VSIL again.</p>
<p data-reasoning="logs-07-3"><span class="qr-step">Step 3</span>For each record, check bounds against TLL and whether ET/ETR can be decoded before continuing. Release the context when finished. A complete report does not imply that every event in system history was retained.</p>
<div class="qr-related">Revisit the field explanations: <a href="/nvme/figure-reference/logs/en/#figure-b232">Base 2.4 Figure 232 · Persistent Event Log Specific Parameter Field</a><a href="/nvme/figure-reference/logs/en/#figure-b233">Base 2.4 Figure 233 · Persistent Event Log Page</a><a href="/nvme/figure-reference/logs/en/#figure-b234">Base 2.4 Figure 234 · Persistent Event Format</a></div>
<h4>Source locations for this exercise</h4><ul class="qr-case-sources"><li>Base 2.4 · §5.2.13.1.14 · Figure 232 · Persistent Event Log Specific Parameter Field · Printed pages 246 · PDF 272</li><li>Base 2.4 · §5.2.13.1.14 · Figure 233 · Persistent Event Log Page · Printed pages 247–249 · PDF 273–275</li><li>Base 2.4 · §5.2.13.1.14 · Figure 234 · Persistent Event Format · Printed pages 249–250 · PDF 275–276</li></ul></details>
<a href="#exercise-toc">Back to exercise index</a></article>
</section>
<nav class="qr-toc" id="figure-index" aria-label="Volume figure index"><h2>Figures in this volume</h2><ol>
<li><a href="#figure-b204">Base 2.4 Figure 204 · Get Log Page – Command Dword 10</a></li>
<li><a href="#figure-b205">Base 2.4 Figure 205 · Get Log Page – Command Dword 11</a></li>
<li><a href="#figure-b208">Base 2.4 Figure 208 · Get Log Page – Command Dword 14</a></li>
<li><a href="#figure-b211">Base 2.4 Figure 211 · LID Supported and Effects Data Structure</a></li>
<li><a href="#figure-b212">Base 2.4 Figure 212 · Error Information Log Entry Data Structure</a></li>
<li><a href="#figure-b213">Base 2.4 Figure 213 · SMART / Health Information Log Page</a></li>
<li><a href="#figure-b217">Base 2.4 Figure 217 · Commands Supported and Effects Data Structure</a></li>
<li><a href="#figure-b221">Base 2.4 Figure 221 · Telemetry Host-Initiated Log Page</a></li>
<li><a href="#figure-b223">Base 2.4 Figure 223 · Telemetry Controller-Initiated Log Page</a></li>
<li><a href="#figure-b225">Base 2.4 Figure 225 · Endurance Group Information Log Page</a></li>
<li><a href="#figure-b232">Base 2.4 Figure 232 · Persistent Event Log Specific Parameter Field</a></li>
<li><a href="#figure-b233">Base 2.4 Figure 233 · Persistent Event Log Page</a></li>
<li><a href="#figure-b234">Base 2.4 Figure 234 · Persistent Event Format</a></li>
<li><a href="#figure-b236">Base 2.4 Figure 236 · Persistent Event Log Event Types</a></li>
<li><a href="#figure-p75">PCIe Transport 1.4 Figure 75 · EOM Header</a></li>
<li><a href="#figure-p76">PCIe Transport 1.4 Figure 76 · EOM Lane Descriptor</a></li>
</ol></nav>
<article class="qr-card" id="figure-b204" data-figure="B204">
<h2><span class="qr-number">01</span>Get Log Page – Command Dword 10</h2>
<p class="qr-original">Base 2.4 · Figure 204 · Get Log Page – Command Dword 10</p>
<p class="qr-location">§5.2.13 · Printed pages 213 · PDF 239</p>
<p class="qr-explanation" data-paragraph="B204-1"><span class="qr-step">01.1 · Use</span>A log read may also acknowledge an asynchronous event. Preserve LID, LSP and RAE, not just buffer length.</p>
<p class="qr-explanation" data-paragraph="B204-2"><span class="qr-step">01.2 · Fields and relationships</span>LID bits 7:0 selects the log, LSP bits 14:8 is log-specific, RAE bit 15 retains the event, and NUMDL bits 31:16 supplies the low 16 bits of the minus-one Dword count combined with NUMDU. RAE=0 normally acknowledges the corresponding event on success rather than deleting all log contents.</p>
<p class="qr-explanation" data-paragraph="B204-3"><span class="qr-step">01.3 · Interpretation and example</span>An ordinary 512-byte read needs 128 Dwords, so NUMD=127. A failed read does not acknowledge the event. Log-specific action or length rules, such as PEL ACT=3, override the general case.</p>
<p class="qr-tags">Search terms: Get Log Page · LID · LSP · RAE · NUMDL</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/logs/en/#figure-b205">Base 2.4 Figure 205 · Get Log Page – Command Dword 11</a><a href="/nvme/figure-reference/logs/en/#figure-b232">Base 2.4 Figure 232 · Persistent Event Log Specific Parameter Field</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b205" data-figure="B205">
<h2><span class="qr-number">02</span>Get Log Page – Command Dword 11</h2>
<p class="qr-original">Base 2.4 · Figure 205 · Get Log Page – Command Dword 11</p>
<p class="qr-location">§5.2.13 · Printed pages 214 · PDF 240</p>
<p class="qr-explanation" data-paragraph="B205-1"><span class="qr-step">02.1 · Use</span>Inspect CDW11 for large reads or resource selection. Its upper LSI half is not an extension of NUMD.</p>
<p class="qr-explanation" data-paragraph="B205-2"><span class="qr-step">02.2 · Fields and relationships</span>NUMDU bits 15:0 combines with CDW10.NUMDL into a 32-bit minus-one Dword count. LSI bits 31:16 is a log-specific identifier. Ordinary transfer size is 4×(((NUMDU&lt;&lt;16)|NUMDL)+1) bytes.</p>
<p class="qr-explanation" data-paragraph="B205-3"><span class="qr-step">02.3 · Interpretation and example</span>NUMDU=1/NUMDL=0 means 262148 bytes, not 65536. For LID=09h, LSI identifies an Endurance Group and must not be included in length arithmetic.</p>
<p class="qr-tags">Search terms: NUMDU · LSI · Endurance Group Identifier · Get Log Page</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/logs/en/#figure-b204">Base 2.4 Figure 204 · Get Log Page – Command Dword 10</a><a href="/nvme/figure-reference/logs/en/#figure-b225">Base 2.4 Figure 225 · Endurance Group Information Log Page</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b208" data-figure="B208">
<h2><span class="qr-number">03</span>Get Log Page – Command Dword 14</h2>
<p class="qr-original">Base 2.4 · Figure 208 · Get Log Page – Command Dword 14</p>
<p class="qr-location">§5.2.13 · Printed pages 214–215 · PDF 240–241</p>
<p class="qr-explanation" data-paragraph="B208-1"><span class="qr-step">03.1 · Use</span>Check OT when chunked reads start at the wrong location. The same LPO can count bytes or data structures: byte offset and index offset are different units.</p>
<p class="qr-explanation" data-paragraph="B208-2"><span class="qr-step">03.2 · Fields and relationships</span>OT bit 23, when clear, interprets CDW12/13.LPO as bytes; OT=1 interprets it as a supported list index. CSI bits 31:24 chooses the applicable command set, while UIDX bits 6:0 selects a UUID index, each subject to its own conditions.</p>
<p class="qr-explanation" data-paragraph="B208-3"><span class="qr-step">03.3 · Interpretation and example</span>For an index-capable log, LPO=2/OT=1 means index 2. OT=0 instead means byte 2 and must also satisfy applicable alignment requirements. Those values are not interchangeable.</p>
<p class="qr-tags">Search terms: OT · LPO · index offset · byte offset · CSI · UIDX</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/logs/en/#figure-b211">Base 2.4 Figure 211 · LID Supported and Effects Data Structure</a><a href="/nvme/figure-reference/logs/en/#figure-b204">Base 2.4 Figure 204 · Get Log Page – Command Dword 10</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b211" data-figure="B211">
<h2><span class="qr-number">04</span>LID Supported and Effects Data Structure</h2>
<p class="qr-original">Base 2.4 · Figure 211 · LID Supported and Effects Data Structure</p>
<p class="qr-location">§5.2.13.1.1 · Printed pages 217–218 · PDF 243–244</p>
<p class="qr-explanation" data-paragraph="B211-1"><span class="qr-step">04.1 · Use</span>Inspect the descriptor for a LID before issuing special actions or index-offset reads. A standardized LID is not proof of device support.</p>
<p class="qr-explanation" data-paragraph="B211-2"><span class="qr-step">04.2 · Fields and relationships</span>LSUPP bit 0 advertises support, IOS bit 1 index-offset support, and LIDSP bits 31:16 log-specific capabilities. Ignore other fields when LSUPP is clear. IOS also depends on extended-data support.</p>
<p class="qr-explanation" data-paragraph="B211-3"><span class="qr-step">04.3 · Interpretation and example</span>LSUPP=1 with IOS=0 supports the log but not OT=1. PEL additionally uses LIDSP for extended context/header capabilities; LIDSP does not have one universal meaning across logs.</p>
<p class="qr-tags">Search terms: LID 00h · LSUPP · IOS · LIDSP · SPEDS</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/logs/en/#figure-b208">Base 2.4 Figure 208 · Get Log Page – Command Dword 14</a><a href="/nvme/figure-reference/logs/en/#figure-b232">Base 2.4 Figure 232 · Persistent Event Log Specific Parameter Field</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b212" data-figure="B212">
<h2><span class="qr-number">05</span>Error Information Log Entry Data Structure</h2>
<p class="qr-original">Base 2.4 · Figure 212 · Error Information Log Entry Data Structure</p>
<p class="qr-location">§5.2.13.1.2 · Printed pages 218–220 · PDF 244–246</p>
<p class="qr-explanation" data-paragraph="B212-1"><span class="qr-step">05.1 · Use</span>Read these 64-byte entries when CQE.M or an error event calls for more detail. Newer errors appear first; each entry can identify a command, status and parameter location.</p>
<p class="qr-explanation" data-paragraph="B212-2"><span class="qr-step">05.2 · Fields and relationships</span>ECNT bytes 7:0 is the error sequence number, with zero denoting an invalid entry. SQID bytes 9:8/CID bytes 11:10 identifies the command; STS bytes 13:12 records status. Parameter Error Location 15:14 contains BYTLOC within the SQE and BITLOC within that byte. NSID, CSI, OPC, CSINFO and LPVER further qualify interpretation.</p>
<p class="qr-explanation" data-paragraph="B212-3"><span class="qr-step">05.3 · Interpretation and example</span>BYTLOC=40/BITLOC=3 means SQE byte 40 bit 3, or CDW10 bit 3, not Dword 40. Non-command-specific errors can use FFFFh SQID/CID. Here PEL means Parameter Error Location, distinct from Persistent Event Log.</p>
<p class="qr-tags">Search terms: LID 01h · ECNT · SQID · CID · PEL · BYTLOC · BITLOC · LPVER</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a><a href="/nvme/figure-reference/command/en/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b213" data-figure="B213">
<h2><span class="qr-number">06</span>SMART / Health Information Log Page</h2>
<p class="qr-original">Base 2.4 · Figure 213 · SMART / Health Information Log Page</p>
<p class="qr-location">§5.2.13.1.3 · Printed pages 221–225 · PDF 247–251</p>
<p class="qr-explanation" data-paragraph="B213-1"><span class="qr-step">06.1 · Use</span>SMART combines current warnings, lifetime counters and durations with different units. Classify a field before comparing snapshots.</p>
<p class="qr-explanation" data-paragraph="B213-2"><span class="qr-step">06.2 · Fields and relationships</span>CW is a warning bitmap, CTEMP Kelvin and PUSED estimated lifetime percentage. DUR/DUW round up in 1000×512-byte units; zero means unreported. HRC/HWC counts commands, CBT minutes, POH hours and thermal-management totals seconds. A zero sensor is unimplemented.</p>
<p class="qr-explanation" data-paragraph="B213-3"><span class="qr-step">06.3 · Interpretation and example</span>A DUR increment of one need not equal exactly 512000 newly transferred bytes because the counter is rounded. PUSED above 100 also does not by itself establish device failure; correlate warnings, media errors and behavior.</p>
<p class="qr-tags">Search terms: LID 02h · SMART · CW · CTEMP · DUR · DUW · POH · PUSED · TMT</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/features/en/#figure-b482">Base 2.4 Figure 482 · HCTM – Command Dword 11</a><a href="/nvme/figure-reference/logs/en/#figure-b225">Base 2.4 Figure 225 · Endurance Group Information Log Page</a><a href="/nvme/figure-reference/logs/en/#figure-b233">Base 2.4 Figure 233 · Persistent Event Log Page</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b217" data-figure="B217">
<h2><span class="qr-number">07</span>Commands Supported and Effects Data Structure</h2>
<p class="qr-original">Base 2.4 · Figure 217 · Commands Supported and Effects Data Structure</p>
<p class="qr-location">§5.2.13.1.6 · Printed pages 228–229 · PDF 254–255</p>
<p class="qr-explanation" data-paragraph="B217-1"><span class="qr-step">07.1 · Use</span>Consult this descriptor before an operation that may change data, namespace inventory or controller capabilities. It describes potential effects and coordination guidance, not a historical result.</p>
<p class="qr-explanation" data-paragraph="B217-2"><span class="qr-step">07.2 · Fields and relationships</span>CSUPP bit 0 reports support; LBCC bit 1, NCC bit 2, NIC bit 3 and CCC bit 4 indicate possible changes to data, one namespace’s capabilities, inventory and controller capabilities. CSE bits 18:16 and CSER bits 15:14 give submission/execution guidance; CSP bits 31:20 gives potential scope.</p>
<p class="qr-explanation" data-paragraph="B217-3"><span class="qr-step">07.3 · Interpretation and example</span>NIC=1 suggests rediscovering namespace inventory after the operation, not that one namespace was definitely added. Hosts understanding a nonzero CSER use its newer guidance rather than indiscriminately combining it with CSE.</p>
<p class="qr-tags">Search terms: LID 05h · CSUPP · LBCC · NCC · NIC · CCC · CSE · CSER · CSP</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a><a href="/nvme/figure-reference/maintenance/en/#figure-b446">Base 2.4 Figure 446 · Namespace Management – Command Dword 10</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b221" data-figure="B221">
<h2><span class="qr-number">08</span>Telemetry Host-Initiated Log Page</h2>
<p class="qr-original">Base 2.4 · Figure 221 · Telemetry Host-Initiated Log Page</p>
<p class="qr-location">§5.2.13.1.8 · Printed pages 234–235 · PDF 260–261</p>
<p class="qr-explanation" data-paragraph="B221-1"><span class="qr-step">08.1 · Use</span>Use this header to determine host-initiated telemetry boundaries and generation. Vendor-defined payloads sit inside a commonly interpretable envelope.</p>
<p class="qr-explanation" data-paragraph="B221-2"><span class="qr-step">08.2 · Fields and relationships</span>The first 512 bytes form the header. Data Area 1/2/3/4 Last Block fields identify final 512-byte block indices; data starts at block 1 and areas are cumulative. THS is byte 380, THDGN is byte 381; bytes 382/383 copy controller-telemetry availability/generation.</p>
<p class="qr-explanation" data-paragraph="B221-3"><span class="qr-step">08.3 · Interpretation and example</span>DA1LB=2 and DA2LB=5 mean blocks 1–2 and 1–5, not two blocks followed by five more. Preserve generation and capture actions across chunked retrieval to avoid combining different captures.</p>
<p class="qr-tags">Search terms: LID 07h · Telemetry Host-Initiated · THDA1LB · THDGN · THS</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/logs/en/#figure-b223">Base 2.4 Figure 223 · Telemetry Controller-Initiated Log Page</a><a href="/nvme/figure-reference/logs/en/#figure-b204">Base 2.4 Figure 204 · Get Log Page – Command Dword 10</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b223" data-figure="B223">
<h2><span class="qr-number">09</span>Telemetry Controller-Initiated Log Page</h2>
<p class="qr-original">Base 2.4 · Figure 223 · Telemetry Controller-Initiated Log Page</p>
<p class="qr-location">§5.2.13.1.9 · Printed pages 236–237 · PDF 262–263</p>
<p class="qr-explanation" data-paragraph="B223-1"><span class="qr-step">09.1 · Use</span>This header describes controller-captured telemetry scope, unacknowledged updates and generation. Notification state is not payload length.</p>
<p class="qr-explanation" data-paragraph="B223-2"><span class="qr-step">09.2 · Fields and relationships</span>TCS is byte 381, TCDA byte 382 and TCDGN byte 383; area last-block fields still describe cumulative extents. In Base 2.4, TCDA tracks updates since a successful RAE=0 acknowledgement, while TCDGN tracks captures.</p>
<p class="qr-explanation" data-paragraph="B223-3"><span class="qr-step">09.3 · Interpretation and example</span>TCDA=0 can mean a previous update was acknowledged; it does not establish absence of saved telemetry. Byte 381 in LID=07h is THDGN, so decoding it as this header’s TCS is also incorrect.</p>
<p class="qr-tags">Search terms: LID 08h · TCDA · TCDGN · TCS · Telemetry Controller-Initiated</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/logs/en/#figure-b221">Base 2.4 Figure 221 · Telemetry Host-Initiated Log Page</a><a href="/nvme/figure-reference/logs/en/#figure-b204">Base 2.4 Figure 204 · Get Log Page – Command Dword 10</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b225" data-figure="B225">
<h2><span class="qr-number">10</span>Endurance Group Information Log Page</h2>
<p class="qr-original">Base 2.4 · Figure 225 · Endurance Group Information Log Page</p>
<p class="qr-location">§5.2.13.1.10 · Printed pages 238–239 · PDF 264–265</p>
<p class="qr-explanation" data-paragraph="B225-1"><span class="qr-step">10.1 · Use</span>Use LID=09h when aggregate SMART cannot answer health questions for each Endurance Group. Select the group through LSI before comparing reports.</p>
<p class="qr-explanation" data-paragraph="B225-2"><span class="qr-step">10.2 · Fields and relationships</span>Fields include Critical Warning, Available Spare/Threshold, Percentage Used, data/media-write counters, errors and capacity. Units differ by field. Namespace Identify provides its ENDGID.</p>
<p class="qr-explanation" data-paragraph="B225-3"><span class="qr-step">10.3 · Interpretation and example</span>A warning for group 1 does not mean group 2 has the same warning. Fix ENDGID and observation time when comparing logs. Acknowledging a notification does not repair the underlying condition.</p>
<p class="qr-tags">Search terms: LID 09h · Endurance Group · CW · AVSP · PUSED · ENDGID</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/logs/en/#figure-b205">Base 2.4 Figure 205 · Get Log Page – Command Dword 11</a><a href="/nvme/figure-reference/identify/en/#figure-b346">Base 2.4 Figure 346 · Identify – I/O Command Set Independent Identify Namespace Data Structure</a><a href="/nvme/figure-reference/logs/en/#figure-b213">Base 2.4 Figure 213 · SMART / Health Information Log Page</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b232" data-figure="B232">
<h2><span class="qr-number">11</span>Persistent Event Log Specific Parameter Field</h2>
<p class="qr-original">Base 2.4 · Figure 232 · Persistent Event Log Specific Parameter Field</p>
<p class="qr-location">§5.2.13.1.14 · Printed pages 246 · PDF 272</p>
<p class="qr-explanation" data-paragraph="B232-1"><span class="qr-step">11.1 · Use</span>ACT manages a reporting context: the fixed event set used for a multipart Persistent Event Log retrieval. It does not select an event type.</p>
<p class="qr-explanation" data-paragraph="B232-2"><span class="qr-step">11.2 · Fields and relationships</span>ACT=0 reads an existing context, 1 establishes and reads, 2 releases, and 3 establishes if needed or reuses it and reads the header. ACT=1 fails if a context exists. ACT=3 returns the 512-byte header at offset 0 regardless of ordinary NUMD/LPO settings, requiring an adequate buffer.</p>
<p class="qr-explanation" data-paragraph="B232-3"><span class="qr-step">11.3 · Interpretation and example</span>RCE=0 after successful ACT=3 means no context existed before processing, not creation failure. Continue with ACT=0; issuing ACT=1 can instead produce Command Sequence Error.</p>
<p class="qr-tags">Search terms: LID 0Dh · ACT · context · ACT 3 · PEL</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/logs/en/#figure-b233">Base 2.4 Figure 233 · Persistent Event Log Page</a><a href="/nvme/figure-reference/logs/en/#figure-b234">Base 2.4 Figure 234 · Persistent Event Format</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b233" data-figure="B233">
<h2><span class="qr-number">12</span>Persistent Event Log Page</h2>
<p class="qr-original">Base 2.4 · Figure 233 · Persistent Event Log Page</p>
<p class="qr-location">§5.2.13.1.14 · Printed pages 247–249 · PDF 273–275</p>
<p class="qr-explanation" data-paragraph="B233-1"><span class="qr-step">12.1 · Use</span>Read total length and version before walking persistent events. Log revision, generation and individual event revision are distinct fields.</p>
<p class="qr-explanation" data-paragraph="B233-2"><span class="qr-step">12.2 · Fields and relationships</span>TNEV bytes 7:4 counts events, TLL bytes 15:8 counts total bytes, LREV byte 16 gives revision and LHL bytes 19:18 plus 20 gives header size. GNUM bytes 373:372 tracks newly established reports with changed content; RCI includes RCE. SEB bytes 511:480 describes supported event types, not present events.</p>
<p class="qr-explanation" data-paragraph="B233-3"><span class="qr-step">12.3 · Interpretation and example</span>LHL=492 gives a 512-byte header even when TNEV=0. Correlate context and GNUM across chunks; equal generation is not an indefinite guarantee across resets.</p>
<p class="qr-tags">Search terms: TLL · TNEV · LHL · LREV · GNUM · RCE · SEB</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/logs/en/#figure-b232">Base 2.4 Figure 232 · Persistent Event Log Specific Parameter Field</a><a href="/nvme/figure-reference/logs/en/#figure-b234">Base 2.4 Figure 234 · Persistent Event Format</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b234" data-figure="B234">
<h2><span class="qr-number">13</span>Persistent Event Format</h2>
<p class="qr-original">Base 2.4 · Figure 234 · Persistent Event Format</p>
<p class="qr-location">§5.2.13.1.14 · Printed pages 249–250 · PDF 275–276</p>
<p class="qr-explanation" data-paragraph="B234-1"><span class="qr-step">13.1 · Use</span>Persistent events are variable length. Use this table to establish record boundaries before type-specific decoding rather than using a fixed stride.</p>
<p class="qr-explanation" data-paragraph="B234-2"><span class="qr-step">13.2 · Fields and relationships</span>ET at byte 0 selects the event type; ETR at byte 1 selects the payload revision. The value in EHL at byte 2, plus 3, gives the common-header size. VSIL bytes 21:20 counts vendor information; EL bytes 23:22 includes both VSI and Event Data. Next=start+EHL+3+EL; ED length=EL−VSIL.</p>
<p class="qr-explanation" data-paragraph="B234-3"><span class="qr-step">13.3 · Interpretation and example</span>At start 512 with EHL=21, VSIL=4 and EL=20, the header is 24 bytes, ED=16 bytes and next record starts at 556. Adding VSIL again incorrectly reaches 560. Do not independently pad each record to four bytes.</p>
<p class="qr-tags">Search terms: ET · ETR · EHL · VSIL · EL · VSI · ED · ETSTP</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/logs/en/#figure-b233">Base 2.4 Figure 233 · Persistent Event Log Page</a><a href="/nvme/figure-reference/logs/en/#figure-b236">Base 2.4 Figure 236 · Persistent Event Log Event Types</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-b236" data-figure="B236">
<h2><span class="qr-number">14</span>Persistent Event Log Event Types</h2>
<p class="qr-original">Base 2.4 · Figure 236 · Persistent Event Log Event Types</p>
<p class="qr-location">§5.2.13.1.14.2 · Printed pages 251 · PDF 277</p>
<p class="qr-explanation" data-paragraph="B236-1"><span class="qr-step">14.1 · Use</span>After decoding the common header, route ET to the payload format here. The table also gives revisions and logging requirements.</p>
<p class="qr-explanation" data-paragraph="B236-2"><span class="qr-step">14.2 · Fields and relationships</span>Common types include 01h health, 02h firmware, 04h reset, 05h hardware, 06h namespace, 07h/08h Format start/completion, 09h/0Ah Sanitize start/completion, 0Bh feature changes, 0Ch telemetry and 0Dh thermal events. Requirements depend on triggering-command and controller conditions.</p>
<p class="qr-explanation" data-paragraph="B236-3"><span class="qr-step">14.3 · Interpretation and example</span>ET=0Ah identifies a Sanitize-completion event, not success; inspect its payload result. ETR is not an event count, and supporting a type does not guarantee its presence in this report.</p>
<p class="qr-tags">Search terms: ET · ETR · Firmware Event · Namespace Change · Sanitize Event</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/logs/en/#figure-b234">Base 2.4 Figure 234 · Persistent Event Format</a><a href="/nvme/figure-reference/maintenance/en/#figure-b312">Base 2.4 Figure 312 · Sanitize Status Log Page</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-p75" data-figure="P75">
<h2><span class="qr-number">15</span>EOM Header</h2>
<p class="qr-original">PCIe Transport 1.4 · Figure 75 · EOM Header</p>
<p class="qr-location">§3.9.1.1 · Printed pages 42–43 · PDF 42–43</p>
<p class="qr-explanation" data-paragraph="P75-1"><span class="qr-step">15.1 · Use</span>Before analyzing receiver-eye data, inspect the Eye Opening Measurement header for completion, revision and length. A successful log response alone does not establish a completed measurement.</p>
<p class="qr-explanation" data-paragraph="P75-2"><span class="qr-step">15.2 · Fields and relationships</span>EOMIP byte 1 values 0/1/2 mean not started/in progress/completed. HSIZE bytes 3:2 is 64, RSZ bytes 7:4 total bytes, EDGN byte 8 generation and LREV byte 9 is 3 here. DS bytes 23:20 gives descriptor size, ND bytes 25:24 count, and ODP controls optional eye data.</p>
<p class="qr-explanation" data-paragraph="P75-3"><span class="qr-step">15.3 · Interpretation and example</span>ND is the actual descriptor count; lane count alone is not a loop bound because a lane can have multiple eyes. Confirm EOMIP=2, advance by DS and preserve the measurement-time link information.</p>
<p class="qr-tags">Search terms: LID 19h · EOM · EOMIP · EDGN · HSIZE · RSZ · DS · ND · EPL</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/logs/en/#figure-p76">PCIe Transport 1.4 Figure 76 · EOM Lane Descriptor</a><a href="/nvme/figure-reference/init/en/#figure-p55">PCIe Transport 1.4 Figure 55 · Offset PXCAP + 12h: PXLS – PCI Express Link Status</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<article class="qr-card" id="figure-p76" data-figure="P76">
<h2><span class="qr-number">16</span>EOM Lane Descriptor</h2>
<p class="qr-original">PCIe Transport 1.4 · Figure 76 · EOM Lane Descriptor</p>
<p class="qr-location">§3.9.1.1 · Printed pages 43–45 · PDF 43–45</p>
<p class="qr-explanation" data-paragraph="P76-1"><span class="qr-step">16.1 · Use</span>Each descriptor describes one eye on one lane. Match measurement identity, success and printable shape without mixing lanes or eyes.</p>
<p class="qr-explanation" data-paragraph="P76-2"><span class="qr-step">16.2 · Fields and relationships</span>MSTAT byte 1 bit 0 indicates success, LN byte 2 lane and EYE byte 3 eye. TOP/BTM/LFT/RGT describe boundaries. NROWS bytes 13:12 and NCOLS bytes 15:14 size the character matrix; EDLEN bytes 19:16 sizes vendor eye data. Printable Eye begins at 32 when present according to ODP.</p>
<p class="qr-explanation" data-paragraph="P76-3"><span class="qr-step">16.3 · Interpretation and example</span>NROWS=5 and NCOLS=7 occupy 35 matrix bytes; when present, subsequent Eye Data starts at 67. A printable 0/1 shape alone cannot establish signal integrity without voltage/time resolution, BER thresholds and other measurement information.</p>
<p class="qr-tags">Search terms: MSTAT · LN · EYE · NROWS · NCOLS · EDLEN · Printable Eye · BER</p>
<div class="qr-related">Related lookups: <a href="/nvme/figure-reference/logs/en/#figure-p75">PCIe Transport 1.4 Figure 75 · EOM Header</a></div>
<a href="#figure-index">Back to this volume’s figure index</a></article>
<footer id="source-files"><h2>Source documents</h2><p>Locations refer to the supplied ratified PDFs. For Base, PDF page = printed page +26; the other two use identical page numbers. Original figure numbers and English titles are retained for PDF search. Source PDFs are not redistributed.</p><ul class="qr-sources"><li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li><li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li></ul></footer>
</main></div>
