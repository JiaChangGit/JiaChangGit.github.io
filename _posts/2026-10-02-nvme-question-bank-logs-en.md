---
layout: post
title: "NVMe Self-Study Bank: Get Log Page and data consistency"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/logs/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/logs/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/logs.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q69–Q81</p><h1>Get Log Page and data consistency</h1><p class="qr-intro">Logs expose state, history or capability, with different lifetimes and read effects. Choose the view and scope before length, pagination, acknowledgment and consistency.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Four separate questions when reading logs</h2><p class="qa-takeaway">Choose the evidence first; a successful read does not complete the operation being observed.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Evidence needed</th><th scope="col">View</th><th scope="col">Limitation</th></tr></thead><tbody><tr><td>Supported logs</td><td>LID 00h</td><td>Support does not imply a current event</td></tr><tr><td>Current health</td><td>SMART LID 02h</td><td>Current warnings and lifetime counters differ</td></tr><tr><td>Command error details</td><td>Error LID 01h</td><td>Correlate identity; old entries can disappear</td></tr><tr><td>Persistent event history</td><td>PEL LID 0Dh</td><td>Capacity and supported-event limits remain</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>A 4096-byte read encodes NUMD1023. The next byte offset is 4096, but index-offset logs require their own entry progression.</p>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-069">Q69 · What does Supported Log Pages provide, and how should support be checked before reading another log?</a></li>
<li><a href="#q-070">Q70 · What do Error Information and SMART/Health Information record?</a></li>
<li><a href="#q-071">Q71 · What do Firmware Slot, Changed Namespace and Commands Supported and Effects logs establish?</a></li>
<li><a href="#q-072">Q72 · When should Device Self-test, Persistent Event and Sanitize Status logs be used?</a></li>
<li><a href="#q-073">Q73 · What do Endurance Group, Predictable Latency, Lockdown, Boot Partition and Media Unit Status logs contain?</a></li>
<li><a href="#q-074">Q74 · How should NSID and other selectors follow a log’s scope?</a></li>
<li><a href="#q-075">Q75 · How are large logs read in chunks, including offsets, lengths, overlaps and gaps?</a></li>
<li><a href="#q-076">Q76 · What are LSI, UUID Index and Retain Asynchronous Event used for?</a></li>
<li><a href="#q-077">Q77 · How can a host detect inconsistent log chunks when content changes?</a></li>
<li><a href="#q-078">Q78 · How are old records handled when Error Information or PEL reaches capacity?</a></li>
<li><a href="#q-079">Q79 · Which log data survives controller reset, subsystem reset or power cycling?</a></li>
<li><a href="#q-080">Q80 · How should advertised log/command support be checked against actual behavior?</a></li>
<li><a href="#q-081">Q81 · How does Commands Supported and Effects describe opcode support and impact?</a></li>
</ol></section>
<article class="qa-question" id="q-069" data-question="69" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-069">Q69</a> What does Supported Log Pages provide, and how should support be checked before reading another log?</h2>
<p class="qa-prompt">Task: discover Sanitize Status support and whether it accepts index offsets. Do the two questions use the same bit? Find the directory and entry before revealing the answer.</p>
<details class="qa-answer" id="q-069-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-069-a-01">Supported Log Pages is a directory of LIDs and index-offset support on the current interface. It distinguishes lack of support from zero-valued data. Reading it is a discovery method, not a mandatory command before every log request.</p><div class="qa-sections">
<section class="qa-section" id="q-069-s-01" data-answer-section="1"><h3><span>1.</span> Select the target and information</h3>
<span class="qa-anchor" id="q-069-a-02"></span><p>Results describe the receiving interface and controller. Interfaces can differ; with CC.CSS=110b, CSI and the enabled command-set profile also affect support. Another interface’s directory is not interchangeable.</p>
<span class="qa-anchor" id="q-069-a-03"></span><p>Use LID 00h. LPA.MLPS=1 guarantees Supported Log Pages, while MLPS=0 may still provide it and does not negate all logs. Figure 338 LPA.LPEDS bit 2 describes extended offsets/length; per-LID LSUPP and IOS describe log support and index-offset support.</p>
<section class="qa-lookup" id="q-069-lookup"><h4>Worked lookup: log support versus permitted read modes</h4>
<p>Assume one PCIe Admin interface, CC.CSS=000b, UUID Index 0, MLPS=1 and LPEDS=1. Discover Sanitize Status LID 81h, not Sanitize Namespace opcode 8Ch.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Step and source location</th><th scope="col">Information to retrieve</th><th scope="col">What this establishes</th></tr></thead><tbody><tr><td>1 · §5.2.13.1.1/Figure 210, printed 217/PDF 243</td><td>Get Log Page with LID 00h, NSID 0, NUMDL=00FFh, NUMDU=0, LPO=0, OT=0 and RAE=0.</td><td>Retrieves 256 four-byte entries (1024 bytes), not a declaration that every LID is supported.</td></tr><tr><td>2 · Figure 210, printed 217/PDF 243</td><td>LID 81h=129 selects offset 4×129=516=204h and bytes 516–519.</td><td>Index by LID; an opcode or FID with the same numeric value is a different identifier.</td></tr><tr><td>3 · Figure 211, printed 217–218/PDF 243–244</td><td>Assume entry 00000001h: LSUPP bit 0=1 and IOS bit 1=0.</td><td>Sanitize Status is supported, but its index-offset mode is not. General extended-read support does not override IOS=0.</td></tr><tr><td>4 · Figures 206/312, printed 214,313 onward/PDF 240,339 onward</td><td>Read LID 81h with OT=0 and the correct target NSID, then decode the returned status.</td><td>LSUPP establishes availability; operation progress/outcome requires the actual status. Unsupported OT=1 still requires Invalid Field despite LSUPP=1.</td></tr></tbody></table></div>
<p>An unavailable directory does not establish that every LID is unsupported; use log-specific specification requirements and Identify fields. A failed query’s buffer is not valid LSUPP evidence.</p>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a></p>
</section>
<span class="qa-anchor" id="q-069-a-04"></span><p>There are 256 four-byte entries. LID n is at byte 4n; bit 0 is LSUPP, bit 1 IOS, and LIDSP is log-specific. The host should ignore other fields when LSUPP=0.</p>
</section>
<section class="qa-section" id="q-069-s-02" data-answer-section="2"><h3><span>2.</span> Query sequence and interpretation</h3>
<span class="qa-anchor" id="q-069-a-05"></span><p>Select the controller and command set, read 00h, and inspect the target entry. Then apply that log’s scope, length and parameters. Rediscover capability after relevant firmware or configuration changes.</p>
<span class="qa-anchor" id="q-069-a-06"></span><p>Success returns a capability directory, not the logs themselves. LSUPP=1 for 81h establishes Sanitize Status availability, not that sanitization has run or completed.</p>
</section>
<section class="qa-section" id="q-069-s-03" data-answer-section="3"><h3><span>3.</span> Handle missing or inconsistent evidence</h3>
<span class="qa-anchor" id="q-069-a-07"></span><p>An unsupported LID normally returns Invalid Log Page (1/09h). Using unsupported OT=1 returns Invalid Field (0/02h), even when the LID is supported. These are different failures.</p>
<span class="qa-anchor" id="q-069-a-16"></span><p>Compare LSUPP, IOS and LPA against a valid request. Supported logs need not support index offsets; an invalid request does not by itself contradict LSUPP.</p>
<span class="qa-anchor" id="q-069-a-17"></span><p>First establish the same interface, CSI and configuration period, then verify four-byte entry addressing.</p>
</section>
</div>
<span class="qa-anchor" id="q-069-a-08"></span><span class="qa-anchor" id="q-069-a-09"></span><span class="qa-anchor" id="q-069-a-10"></span><span class="qa-anchor" id="q-069-a-11"></span><span class="qa-anchor" id="q-069-a-12"></span><span class="qa-anchor" id="q-069-a-13"></span><span class="qa-anchor" id="q-069-a-14"></span><span class="qa-anchor" id="q-069-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/logs/en/#q-081">Q81</a> · <a href="/nvme/question-bank/features/en/#q-054">Q54</a> · <a href="/nvme/question-bank/format-sanitize/en/#q-128">Q128</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-profile">Base 2.4 §5.2.30.1.18</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-sanitizelog">Base 2.4 §5.2.13.1.38</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-070" data-question="70" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-070">Q70</a> What do Error Information and SMART/Health Information record?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-070-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-070-a-01">Error Information explains individual errors; SMART/Health describes current warnings and lifetime usage. They answer different questions and are not substitutes.</p><div class="qa-sections">
<section class="qa-section" id="q-070-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-070-a-02"></span><p>LID 01h is controller-scoped. LID 02h may accept namespace requests, but Base 2.4 defines no namespace-specific SMART information, so controller and namespace reports contain identical information rather than independent usage totals.</p>
<span class="qa-anchor" id="q-070-a-04"></span><p>Each 01h entry is 64 bytes, with ECNT, SQID, CID, status, parameter location and NSID. The 512-byte 02h page contains warnings, temperature, spare, endurance estimate and cumulative usage/error counters.</p>
</section>
<section class="qa-section" id="q-070-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-070-a-03"></span><p>ELPE+1 gives the maximum Error Information entry count. The LPA SMART bit determines whether per-namespace requests are accepted; establish support before interpreting the data.</p>
<span class="qa-anchor" id="q-070-a-05"></span><p>Preserve the CQE, correlate 01h to the command, then sample 02h for health context. Record times to avoid pairing an old error with an unrelated current warning.</p>
<span class="qa-anchor" id="q-070-a-06"></span><p>A successful read does not mean an error-free device. ECNT=0 marks an invalid entry; Percentage Used=100 describes estimated endurance consumption, not necessarily device failure.</p>
</section>
<section class="qa-section" id="q-070-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-070-a-07"></span><p>A specific-NSID SMART request without support returns Invalid Field (0/02h). Historical status in the log is distinct from the status of the current Get Log Page command.</p>
<span class="qa-anchor" id="q-070-a-16"></span><p>The SMART Error Log Entries total is not the number of entries currently visible in 01h. Finite capacity and reset clearing can make the lifetime total larger.</p>
</section>
</div>
<span class="qa-anchor" id="q-070-a-17"></span><span class="qa-anchor" id="q-070-a-08"></span><span class="qa-anchor" id="q-070-a-09"></span><span class="qa-anchor" id="q-070-a-10"></span><span class="qa-anchor" id="q-070-a-11"></span><span class="qa-anchor" id="q-070-a-12"></span><span class="qa-anchor" id="q-070-a-13"></span><span class="qa-anchor" id="q-070-a-14"></span><span class="qa-anchor" id="q-070-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-071" data-question="71" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-071">Q71</a> What do Firmware Slot, Changed Namespace and Commands Supported and Effects logs establish?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-071-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-071-a-01">These logs identify the running firmware slot, namespaces with reported changes, and command support/effects. None is a universal operation history.</p><div class="qa-sections">
<section class="qa-section" id="q-071-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-071-a-02"></span><p>03h is domain or subsystem scoped; 04h describes attached-namespace changes for this controller; 05h describes its commands for the selected command set.</p>
<span class="qa-anchor" id="q-071-a-04"></span><p>Read CAFS, NAFS and FRS1–7 in 03h; NSIDs and the leading FFFFFFFFh overflow marker in 04h; and CSUPP, effects, CSE/CSER and CSP in 05h.</p>
</section>
<section class="qa-section" id="q-071-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-071-a-03"></span><p>Check 00h and relevant Identify capabilities. Slot count and read-only restrictions come from FRMW, not merely the number of nonzero strings in 03h.</p>
<span class="qa-anchor" id="q-071-a-05"></span><p>Choose by purpose: compare 03h with Identify.FR after activation; read 04h and rediscover namespaces after notification; use 05h before a management operation and refresh affected capabilities afterward.</p>
<span class="qa-anchor" id="q-071-a-06"></span><p>NAFS=2 identifies a slot awaiting an applicable CLR, not the currently running slot. NSID 7 in 04h signals change without specifying whether it was formatted or deleted.</p>
</section>
<section class="qa-section" id="q-071-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-071-a-07"></span><p>Separate retrieval errors from reported state. Unsupported LIDs return 1/09h; invalid defined parameters follow 0/02h rules. Empty slots or empty change lists are not themselves retrieval failures.</p>
<span class="qa-anchor" id="q-071-a-16"></span><p>Correlate the active slot with FR, changed IDs with fresh Identify, and CSUPP with valid command behavior. The three logs need not contain matching values.</p>
</section>
</div>
<span class="qa-anchor" id="q-071-a-17"></span><span class="qa-anchor" id="q-071-a-08"></span><span class="qa-anchor" id="q-071-a-09"></span><span class="qa-anchor" id="q-071-a-10"></span><span class="qa-anchor" id="q-071-a-11"></span><span class="qa-anchor" id="q-071-a-12"></span><span class="qa-anchor" id="q-071-a-13"></span><span class="qa-anchor" id="q-071-a-14"></span><span class="qa-anchor" id="q-071-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-fwlog">Base 2.4 §5.2.13.1.4</a> · <a href="#ref-changedlog">Base 2.4 §5.2.13.1.5</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-072" data-question="72" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-072">Q72</a> When should Device Self-test, Persistent Event and Sanitize Status logs be used?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-072-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-072-a-01">Self-test logs show progress and recent results; PEL provides supported historical events; Sanitize Status reports sanitization state and outcome. Choose the right evidence before equating acceptance with completion.</p><div class="qa-sections">
<section class="qa-section" id="q-072-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-072-a-02"></span><p>Self-test scope depends on capabilities such as DSTO.SDSO. PEL is subsystem-scoped; 81h uses NSID to distinguish subsystem and namespace targets. The querying controller is not necessarily the full affected scope.</p>
<span class="qa-anchor" id="q-072-a-04"></span><p>For 06h read DSTOS before progress and validity-qualified results. For 0Dh establish or obtain a reporting context and traverse lengths. For 81h inspect SSTAT before SPROG and outcome fields.</p>
</section>
<section class="qa-section" id="q-072-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-072-a-03"></span><p>Check self-test OACS, PEL LPA and subsystem/namespace sanitize capabilities, then the relevant LIDs. A readable status log does not establish every operation method.</p>
<span class="qa-anchor" id="q-072-a-05"></span><p>Poll 81h after sanitize acceptance for background completion; inspect the newest valid 06h result after self-test; use PEL for supported historical reset or management events.</p>
<span class="qa-anchor" id="q-072-a-06"></span><p>Successful Get establishes retrieval, not a passed test or successful sanitize. Missing PEL events require checking event support, logging conditions and retained history.</p>
</section>
<section class="qa-section" id="q-072-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-072-a-07"></span><p>Unsupported LIDs return 1/09h; invalid PEL context sequencing can return 0/0Ch. Operation failures in returned data do not turn a successful retrieval CQE into failure.</p>
<span class="qa-anchor" id="q-072-a-16"></span><p>Correlate target, time and latest results. An old test result or previous sanitize success is not proof of success for the current operation.</p>
</section>
</div>
<span class="qa-anchor" id="q-072-a-17"></span><span class="qa-anchor" id="q-072-a-08"></span><span class="qa-anchor" id="q-072-a-09"></span><span class="qa-anchor" id="q-072-a-10"></span><span class="qa-anchor" id="q-072-a-11"></span><span class="qa-anchor" id="q-072-a-12"></span><span class="qa-anchor" id="q-072-a-13"></span><span class="qa-anchor" id="q-072-a-14"></span><span class="qa-anchor" id="q-072-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-dstlog">Base 2.4 §5.2.13.1.7</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-073" data-question="73" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-073">Q73</a> What do Endurance Group, Predictable Latency, Lockdown, Boot Partition and Media Unit Status logs contain?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-073-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-073-a-01">These logs describe group endurance, predictable-latency state, prohibited operations, boot partitions and media-unit resources. They are not interchangeable health reports.</p><div class="qa-sections">
<section class="qa-section" id="q-073-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-073-a-02"></span><p>Establish the management object: endurance group, NVM set, lockdown selection/scope, controller-accessed boot partitions, or domain/subsystem media units.</p>
<span class="qa-anchor" id="q-073-a-04"></span><p>Inspect group warnings/spare/endurance in 09h, set latency state/events in 0Ah/0Bh, prohibited opcodes/FIDs in 14h, partition identity/protection in 15h, and media-unit identity/association/state in 10h.</p>
</section>
<section class="qa-section" id="q-073-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-073-a-03"></span><p>Check 00h and relevant Identify capabilities. The main LIDs are 09h, 0Ah/0Bh, 14h, 15h and 10h. LSI can mean different things for different logs.</p>
<span class="qa-anchor" id="q-073-a-05"></span><p>Choose the LID by question, map resource IDs through Identify, then apply the log’s selectors and structure. Group-3 health requires ENDGID=3, not an arbitrary NSID substituted into LSI.</p>
<span class="qa-anchor" id="q-073-a-06"></span><p>Results describe the selected object. One group warning does not establish identical media faults in every namespace; lockdown entries are prohibitions, not execution history.</p>
</section>
<section class="qa-section" id="q-073-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-073-a-07"></span><p>Distinguish unsupported LIDs (1/09h) from invalid resource selectors governed by each log’s defined fields and specific status. Do not classify all selector failures as Invalid Namespace.</p>
<span class="qa-anchor" id="q-073-a-16"></span><p>Correlate resource association, reported state and behavior. Prohibited FIDs should match lockdown policy; media-unit state must be related to namespace dependencies.</p>
</section>
</div>
<span class="qa-anchor" id="q-073-a-17"></span><span class="qa-anchor" id="q-073-a-08"></span><span class="qa-anchor" id="q-073-a-09"></span><span class="qa-anchor" id="q-073-a-10"></span><span class="qa-anchor" id="q-073-a-11"></span><span class="qa-anchor" id="q-073-a-12"></span><span class="qa-anchor" id="q-073-a-13"></span><span class="qa-anchor" id="q-073-a-14"></span><span class="qa-anchor" id="q-073-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-074" data-question="74" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-074">Q74</a> How should NSID and other selectors follow a log’s scope?</h2>
<p class="qa-prompt">Choose the interface and target, then identify the returned field that supports your conclusion.</p>
<details class="qa-answer" id="q-074-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-074-a-01">Scope identifies the kind of object described; selectors identify its instance. A common NSID field does not make every log per-namespace.</p><div class="qa-sections">
<section class="qa-section" id="q-074-s-01" data-answer-section="1"><h3><span>1.</span> Select the target and information</h3>
<span class="qa-anchor" id="q-074-a-02"></span><p>Figure 209 lists scopes, while individual fields may define more specific ones. Read both the directory and the selected LID’s exceptions.</p>
<span class="qa-anchor" id="q-074-a-03"></span><p>Check LSUPP, LPA, multi-domain support and whether CSI/UUID selection applies. Together they determine valid query combinations.</p>
<span class="qa-anchor" id="q-074-a-04"></span><p>Controller/subsystem logs normally use NSID=0 or FFFFFFFFh. LSI, LSP, CSI and UIDX are separate selectors, not extensions of NSID.</p>
</section>
<section class="qa-section" id="q-074-s-02" data-answer-section="2"><h3><span>2.</span> Query sequence and interpretation</h3>
<span class="qa-anchor" id="q-074-a-05"></span><p>Name the target object first, then map it to the specified fields. Fill unused fields according to reserved-field rules.</p>
<span class="qa-anchor" id="q-074-a-06"></span><p>A valid request returns the selected scope. Aggregate SMART and group endurance are different views; copying an aggregate does not create independent namespace statistics.</p>
</section>
<section class="qa-section" id="q-074-s-03" data-answer-section="3"><h3><span>3.</span> Handle missing or inconsistent evidence</h3>
<span class="qa-anchor" id="q-074-a-07"></span><p>Under the common rule, controller/subsystem logs with another NSID return Invalid Field (0/02h). Other scopes use their LID-specific and NSID rules.</p>
<span class="qa-anchor" id="q-074-a-16"></span><p>Retain command selectors, Identify associations and returned data so comparisons refer to the same object.</p>
<span class="qa-anchor" id="q-074-a-17"></span><p>Check the LID’s scope first; a nonzero NSID alone does not establish namespace-specific information.</p>
</section>
</div>
<span class="qa-anchor" id="q-074-a-08"></span><span class="qa-anchor" id="q-074-a-09"></span><span class="qa-anchor" id="q-074-a-10"></span><span class="qa-anchor" id="q-074-a-11"></span><span class="qa-anchor" id="q-074-a-12"></span><span class="qa-anchor" id="q-074-a-13"></span><span class="qa-anchor" id="q-074-a-14"></span><span class="qa-anchor" id="q-074-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-uuid">Base 2.4 §8.1.31.1–8.1.31.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-075" data-question="75" data-answer-kind="process"><h2><a class="qa-qid" href="#q-075">Q75</a> How are large logs read in chunks, including offsets, lengths, overlaps and gaps?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-075-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-075-a-01">Chunking reads a large log with bounded buffers. Both coverage and consistency matter; individually successful reads do not establish a complete coherent file.</p><div class="qa-sections">
<section class="qa-section" id="q-075-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-075-a-02"></span><p>Offsets locate data within the log, not host memory. OT=0 uses bytes; OT=1 uses log-defined entry indices. Do not mix their units.</p>
<span class="qa-anchor" id="q-075-a-03"></span><p>Check LPA.LPEDS and per-LID IOS, then size transfers using MDTS and log-specific length rules.</p>
<span class="qa-anchor" id="q-075-a-04"></span><p>NUMD=(NUMDU&lt;&lt;16)|NUMDL normally encodes bytes/4−1. LPOU/LPOL form the 64-bit offset; byte offsets require Dword alignment, with further log-specific constraints.</p>
</section>
<section class="qa-section" id="q-075-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-075-a-06"></span><p>Success covers the requested valid range. Unless otherwise specified, bytes beyond the log end are undefined and are not additional log content.</p>
<span class="qa-anchor" id="q-075-a-05"></span>
<figure class="qa-flow" id="q-075-flow"><figcaption>Place every chunk at its correct log offset</figcaption>
<p>Example: read an 8192-byte log with OT=0 in 4096-byte transfers.</p><ol class="qa-flow-steps">
<li class="qa-flow-step"><strong>Chunk 1: LPO=0, NUMD=1023</strong><p>This transfer covers log bytes 0–4095; preserve the target, response and sampling information.</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>Chunk 2: LPO=4096, NUMD=1023</strong><p>This covers bytes 4096–8191, immediately after the first chunk with no gap.</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>Check coverage and consistency before merging</strong><p>Overlapping bytes can be compared; if content changed between reads, do not arbitrarily overwrite one version with another.</p></li>
</ol><p class="qa-flow-conclusion">Covering all 8192 bytes proves coverage only. Use the particular log’s generation or context mechanism to establish consistency.</p></figure>
</section>
<section class="qa-section" id="q-075-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-075-a-07"></span><p>An offset beyond the log or OT=1 without IOS returns 0/02h. For nonzero low two byte-offset bits, the controller may reject or operate as if those bits were zero; neither outcome is universally mandatory.</p>
<span class="qa-anchor" id="q-075-a-16"></span><p>Verify total length, offsets/NUMD and generation or reporting context. Complete coverage and one coherent snapshot are separate requirements.</p>
</section>
</div>
<span class="qa-anchor" id="q-075-a-17"></span><span class="qa-anchor" id="q-075-a-08"></span><span class="qa-anchor" id="q-075-a-09"></span><span class="qa-anchor" id="q-075-a-10"></span><span class="qa-anchor" id="q-075-a-11"></span><span class="qa-anchor" id="q-075-a-12"></span><span class="qa-anchor" id="q-075-a-13"></span><span class="qa-anchor" id="q-075-a-14"></span><span class="qa-anchor" id="q-075-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-telemetrylog">Base 2.4 §5.2.13.1.8–5.2.13.1.9</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-076" data-question="76" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-076">Q76</a> What are LSI, UUID Index and Retain Asynchronous Event used for?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-076-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-076-a-01">These fields select a resource, a data-definition context, and event retention. Their roles are independent.</p><div class="qa-sections">
<section class="qa-section" id="q-076-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-076-a-02"></span><p>LSI is LID-specific; UIDX selects a UUID-list definition; RAE controls the associated event. Not every log uses all three.</p>
<span class="qa-anchor" id="q-076-a-03"></span><p>Check whether LSI is defined and UUID selection supported. RAE behavior depends on the event’s acknowledgment rules.</p>
</section>
<section class="qa-section" id="q-076-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-076-a-04"></span><p>LSI is CDW11[31:16], UIDX CDW14[6:0] with zero meaning no UUID selection, and RAE CDW10[15]. UIDX is an index, not the UUID itself.</p>
<span class="qa-anchor" id="q-076-a-05"></span><p>Fix the target and UUID definition, then decide whether the event should remain pending. Record RAE for each chunk and follow the selected log’s acknowledgment procedure.</p>
<span class="qa-anchor" id="q-076-a-06"></span><p>Successful RAE=1 reads retain the event; successful RAE=0 reads clear it as defined. Failed reads must retain it; an attempted read is not acknowledgment.</p>
</section>
<section class="qa-section" id="q-076-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-076-a-07"></span><p>Invalid UUID selection follows 0/02h rules in §8.1.31; invalid LSI follows the LID definition. Changing RAE does not fix the selected resource.</p>
<span class="qa-anchor" id="q-076-a-16"></span><p>Compare the target, UUID mapping and pending-event state. Identical returned bytes with different RAE can produce different subsequent notification behavior.</p>
</section>
</div>
<span class="qa-anchor" id="q-076-a-17"></span><span class="qa-anchor" id="q-076-a-08"></span><span class="qa-anchor" id="q-076-a-09"></span><span class="qa-anchor" id="q-076-a-10"></span><span class="qa-anchor" id="q-076-a-11"></span><span class="qa-anchor" id="q-076-a-12"></span><span class="qa-anchor" id="q-076-a-13"></span><span class="qa-anchor" id="q-076-a-14"></span><span class="qa-anchor" id="q-076-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-uuid">Base 2.4 §8.1.31.1–8.1.31.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-077" data-question="77" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-077">Q77</a> How can a host detect inconsistent log chunks when content changes?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-077-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-077-a-01">This prevents combining different times into an apparently complete report. Correct length and coverage do not establish a single capture.</p><div class="qa-sections">
<section class="qa-section" id="q-077-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-077-a-02"></span><p>Consistency is log-specific: Telemetry has generations, PEL reporting contexts. Other dynamic logs do not gain cross-command atomic snapshots by assumption.</p>
<span class="qa-anchor" id="q-077-a-03"></span><p>Check the supported log structure/version and its generation, total length, availability or context action. Common command fields alone are insufficient.</p>
<span class="qa-anchor" id="q-077-a-04"></span><p>Retain Telemetry generation and area boundaries, or PEL context/TLL/event lengths and versions, together with each chunk’s offset, length and acquisition time.</p>
</section>
<section class="qa-section" id="q-077-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-077-a-17"></span><p>Check generation/context continuity before blaming the parser.</p>
<span class="qa-anchor" id="q-077-a-05"></span><p>Read the header, use the same capture/context and recheck the header where applicable. A changed generation requires reacquisition or an explicit consistency limitation, not just replacement of the header.</p>
</section>
<section class="qa-section" id="q-077-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-077-a-06"></span><p>Initial TCDGN=10 and final=11 leave intervening chunks unproven even when all Gets succeed. Retain consistency evidence with the resulting report.</p>
<span class="qa-anchor" id="q-077-a-07"></span><p>Content changes need not produce an error CQE. Invalid PEL context operations can produce 0/0Ch, which is distinct from a legitimate generation change.</p>
<span class="qa-anchor" id="q-077-a-16"></span><p>Treat headers, chunks and query order as one evidence set. The last capability or generation value cannot retroactively validate every earlier chunk.</p>
</section>
</div>
<span class="qa-anchor" id="q-077-a-08"></span><span class="qa-anchor" id="q-077-a-09"></span><span class="qa-anchor" id="q-077-a-10"></span><span class="qa-anchor" id="q-077-a-11"></span><span class="qa-anchor" id="q-077-a-12"></span><span class="qa-anchor" id="q-077-a-13"></span><span class="qa-anchor" id="q-077-a-14"></span><span class="qa-anchor" id="q-077-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-telemetrylog">Base 2.4 §5.2.13.1.8–5.2.13.1.9</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-078" data-question="78" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-078">Q78</a> How are old records handled when Error Information or PEL reaches capacity?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-078-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-078-a-01">Finite logs cannot preserve unlimited history. Distinguish cumulative counts from currently readable records; a missing old entry does not prove the event never occurred.</p><div class="qa-sections">
<section class="qa-section" id="q-078-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-078-a-02"></span><p>Error Information is controller-scoped; PEL contains supported subsystem events accessed through reporting contexts. Capacity and read lifecycles differ.</p>
<span class="qa-anchor" id="q-078-a-04"></span><p>Error entries are newest first with ECNT identity. PEL traversal uses EHL, EL, ET and ETR; events are not fixed 64-byte error entries.</p>
</section>
<section class="qa-section" id="q-078-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-078-a-03"></span><p>ELPE+1 sets Error Information capacity. For PEL inspect support, report length/event count and maximum capacity; SMART totals do not size the current buffer.</p>
<span class="qa-anchor" id="q-078-a-05"></span><p>Record valid entries and boundary identities, then correlate overlapping samples. Mark lost history explicitly rather than inventing missing records or their order.</p>
<span class="qa-anchor" id="q-078-a-06"></span><p>When Error Information is full, the specification recommends inserting the new entry and discarding the oldest. A complete finite PEL report is not the device’s entire lifetime history.</p>
</section>
<section class="qa-section" id="q-078-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-078-a-07"></span><p>Full storage does not automatically make a valid Get fail. Inspect retention behavior; invalid parameters or contexts are separate command errors.</p>
<span class="qa-anchor" id="q-078-a-16"></span><p>ECNT/SMART totals may diverge from visible entry counts. Explain the difference using capacity and retention, not an expectation of unlimited historical preservation.</p>
</section>
</div>
<span class="qa-anchor" id="q-078-a-17"></span><span class="qa-anchor" id="q-078-a-08"></span><span class="qa-anchor" id="q-078-a-09"></span><span class="qa-anchor" id="q-078-a-10"></span><span class="qa-anchor" id="q-078-a-11"></span><span class="qa-anchor" id="q-078-a-12"></span><span class="qa-anchor" id="q-078-a-13"></span><span class="qa-anchor" id="q-078-a-14"></span><span class="qa-anchor" id="q-078-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-079" data-question="79" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-079">Q79</a> Which log data survives controller reset, subsystem reset or power cycling?</h2>
<p class="qa-prompt">Name the reset or interruption, then assess settings, ongoing operations and data separately.</p>
<details class="qa-answer" id="q-079-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-079-a-01">Separate the query command, temporary reporting state and retained history. An aborted Get does not imply erasure of all underlying data.</p><div class="qa-sections">
<section class="qa-section" id="q-079-s-01" data-answer-section="1"><h3><span>1.</span> Identify the trigger and affected objects</h3>
<span class="qa-anchor" id="q-079-a-02"></span><p>Retention may apply to a whole log or individual fields. Establish reset coverage in multi-controller and multi-domain configurations.</p>
<span class="qa-anchor" id="q-079-a-03"></span><p>Use log-specific retention text and reset rules. Figure 209’s Restore to Default Content concerns manufacturing defaults, not clearing on every reset.</p>
</section>
<section class="qa-section" id="q-079-s-02" data-answer-section="2"><h3><span>2.</span> State changes and recovery</h3>
<span class="qa-anchor" id="q-079-a-04"></span><p>Compare error entries, their ECNT, SMART totals, current temperature, PEL events and PEL context separately. Proximity does not imply identical retention.</p>
<span class="qa-anchor" id="q-079-a-05"></span><p>Capture the same target before reset, perform the specified event, recover and read again. Record concurrent activation, format or manufacturing-default restoration as separate causes.</p>
<span class="qa-anchor" id="q-079-a-06"></span><p>Error entries should clear on CLR/power cycle while ECNT persists. SMART lifetime data persists across power cycles unless a field says otherwise. Persistent PEL events do not make reporting contexts persistent.</p>
</section>
<section class="qa-section" id="q-079-s-03" data-answer-section="3"><h3><span>3.</span> Checks across reset or power loss</h3>
<span class="qa-anchor" id="q-079-a-12"></span>
<span class="qa-anchor" id="q-079-a-13"></span>
<span class="qa-anchor" id="q-079-a-14"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Trigger</th><th scope="col">Effect on this operation or state</th></tr></thead><tbody><tr><td>What survives or continues after Controller Reset?</td><td>Controller Reset stops outstanding queries, which are reissued after Admin Queue recovery. Content retention is separate: Error Information entries should clear but Error Count persists; SMART cumulative information and PEL follow their field-specific persistence rules.</td></tr><tr><td>What survives or continues after NVM Subsystem Reset?</td><td>After subsystem reset, recover query access on affected controllers and re-read the logs. This is not restoration of manufacturing defaults; Figure 209’s Restore to Default Content column is not an ordinary reset-retention table.</td></tr><tr><td>What survives or continues after a power cycle?</td><td>Reissue the query after a power cycle. SMART lifetime information and PEL have persistent content; Error Information entries should clear while the cumulative Error Count persists. Reassess current temperature, active operations and reporting contexts under their own rules rather than expecting every byte to remain fixed.</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-079-s-04" data-answer-section="4"><h3><span>4.</span> Verify retention and recovery</h3>
<span class="qa-anchor" id="q-079-a-07"></span><p>Comparing values creates no status. A failed post-reset Get first requires checking readiness, selectors and context; it is not evidence of cleared data.</p>
<span class="qa-anchor" id="q-079-a-16"></span><p>Compare field semantics and validity rather than requiring byte-identical buffers. Persistent counters can coexist with newly sampled current state.</p>
<span class="qa-anchor" id="q-079-a-17"></span><p>First determine whether the discrepancy concerns stored content, an invalidated context or an interrupted query.</p>
</section>
</div>
<span class="qa-anchor" id="q-079-a-08"></span><span class="qa-anchor" id="q-079-a-09"></span><span class="qa-anchor" id="q-079-a-10"></span><span class="qa-anchor" id="q-079-a-11"></span><span class="qa-anchor" id="q-079-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-080" data-question="80" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-080">Q80</a> How should advertised log/command support be checked against actual behavior?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-080-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-080-a-01">Build a reproducible support-consistency check. Support establishes valid uses, not success for every parameter combination.</p><div class="qa-sections">
<section class="qa-section" id="q-080-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-080-a-02"></span><p>Fix interface, controller, CSI, UUID selection and configuration time. With CC.CSS=110b, a command set not enabled by the profile is treated as unsupported.</p>
<span class="qa-anchor" id="q-080-a-03"></span><p>Preserve LSUPP/IOS, CSUPP, Identify capability bits and FID 19h. Log support and opcode support are different declarations.</p>
<span class="qa-anchor" id="q-080-a-04"></span><p>Retain all relevant selectors, length and data pointers, then decode CQE SCT/SC rather than only a tool’s error string.</p>
</section>
<section class="qa-section" id="q-080-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-080-a-17"></span><p>First verify the same interface and command-set configuration on both sides of the comparison.</p>
<span class="qa-anchor" id="q-080-a-05"></span><p>Construct a request meeting capability, scope and state requirements, execute, then exclude invalid fields, lockdown, namespace readiness and intervening changes before declaring a contradiction.</p>
</section>
<section class="qa-section" id="q-080-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-080-a-06"></span><p>In a stable context, unsupported status for a valid advertised operation is a contradiction to investigate. A legitimate restrictive status is not equivalent to lack of support.</p>
<span class="qa-anchor" id="q-080-a-07"></span><p>Unsupported LID uses 1/09h; unsupported opcode uses 0/01h; 0/02h calls for parameter review. Preserve specific exceptions and allowed choices for multiple errors.</p>
<span class="qa-anchor" id="q-080-a-16"></span><p>Compare declarations, behavior and timing. After activation, rediscover support instead of imposing an old table on new firmware.</p>
</section>
</div>
<span class="qa-anchor" id="q-080-a-08"></span><span class="qa-anchor" id="q-080-a-09"></span><span class="qa-anchor" id="q-080-a-10"></span><span class="qa-anchor" id="q-080-a-11"></span><span class="qa-anchor" id="q-080-a-12"></span><span class="qa-anchor" id="q-080-a-13"></span><span class="qa-anchor" id="q-080-a-14"></span><span class="qa-anchor" id="q-080-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-profile">Base 2.4 §5.2.30.1.18</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-081" data-question="81" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-081">Q81</a> How does Commands Supported and Effects describe opcode support and impact?</h2>
<p class="qa-prompt">Choose the interface and target, then identify the returned field that supports your conclusion.</p>
<details class="qa-answer" id="q-081-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-081-a-01">The table describes support and possible effects on data, namespaces and controller capability. It reports overall possible effects, not effects guaranteed on every invocation.</p><div class="qa-sections">
<section class="qa-section" id="q-081-s-01" data-answer-section="1"><h3><span>1.</span> Select the target and information</h3>
<span class="qa-anchor" id="q-081-a-02"></span><p>Admin and I/O opcodes occupy separate regions; the I/O region also requires the correct command set. CSP can name several possible scopes because parameters affect actual impact.</p>
<span class="qa-anchor" id="q-081-a-03"></span><p>First check Figure 338 LPA.CSES bit 1 for LID 05h availability and fix command-set/UUID selection. CSES advertises the log, while per-opcode CSUPP advertises each command. CSP=0 means unreported scope, not no impact.</p>
<span class="qa-anchor" id="q-081-a-04"></span><p>Figure 216 locates the four-byte entry: Admin uses 4×opcode and I/O uses 1024+4×opcode, in bytes. Figure 217 decodes its support/effect fields. Admin opcode 02h is Get Log Page, whereas NVM I/O opcode 02h is Read; identical numbers do not identify the same entry.</p>
</section>
<section class="qa-section" id="q-081-s-02" data-answer-section="2"><h3><span>2.</span> Query sequence and interpretation</h3>
<span class="qa-anchor" id="q-081-a-05"></span><p>Select the entry and coordinate work under CSE/CSER recommendations. Use a supported nonzero CSER relaxation; otherwise use CSE. Rediscover potentially changed capabilities or inventory afterward.</p>
<span class="qa-anchor" id="q-081-a-06"></span><p>NIC=1 permits inventory or multi-namespace capability changes; it does not guarantee one new namespace per call. CSUPP=0 requires all other entry fields to be zero.</p>
</section>
<section class="qa-section" id="q-081-s-03" data-answer-section="3"><h3><span>3.</span> Handle missing or inconsistent evidence</h3>
<span class="qa-anchor" id="q-081-a-07"></span><p>Retrieval errors follow Get Log Page; operation errors follow the command. Submission recommendations do not authorize inventing a mandatory status for every violation.</p>
<span class="qa-anchor" id="q-081-a-16"></span><p>Correlate effects with before/after Identify, inventory and data. Support declarations should agree; actual effects depend on this invocation’s parameters.</p>
<span class="qa-anchor" id="q-081-a-17"></span><p>First establish Admin/I/O region, opcode, byte offset and query success. Log-relative position, segment-buffer position and entry bit position are distinct coordinates; confusing them can select another command or field.</p>
</section>
</div>
<span class="qa-anchor" id="q-081-a-08"></span><span class="qa-anchor" id="q-081-a-09"></span><span class="qa-anchor" id="q-081-a-10"></span><span class="qa-anchor" id="q-081-a-11"></span><span class="qa-anchor" id="q-081-a-12"></span><span class="qa-anchor" id="q-081-a-13"></span><span class="qa-anchor" id="q-081-a-14"></span><span class="qa-anchor" id="q-081-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/format-sanitize/en/#q-118">Q118</a> · <a href="/nvme/question-bank/logs/en/#q-069">Q69</a> · <a href="/nvme/question-bank/features/en/#q-054">Q54</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-commandseffects">Base 2.4 §5.2.13.1.6</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-profile">Base 2.4 §5.2.30.1.18</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-adminsupport">Base 2.4 §3.1.3.4 (Figure 28 PCIe I/O-controller rows and O/M/P note only)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>

<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-adminsupport"><strong>Base 2.4 · §3.1.3.4 (Figure 28 PCIe I/O-controller rows and O/M/P note only)</strong><br>Printed pages 45–47 · PDF 71–73 · Figure 28</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-getlog"><strong>Base 2.4 · §5.2.13–5.2.13.1.1</strong><br>Printed pages 212–218 · PDF 238–244 · Figure 203–211</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-smart"><strong>Base 2.4 · §5.2.13.1.3</strong><br>Printed pages 220–225 · PDF 246–251 · Figure 213–214</li>
<li id="ref-fwlog"><strong>Base 2.4 · §5.2.13.1.4</strong><br>Printed pages 225–226 · PDF 251–252 · Figure 215</li>
<li id="ref-changedlog"><strong>Base 2.4 · §5.2.13.1.5</strong><br>Printed pages 226 · PDF 252</li>
<li id="ref-commandseffects"><strong>Base 2.4 · §5.2.13.1.6</strong><br>Printed pages 226–229 · PDF 252–255 · Figure 216–217</li>
<li id="ref-dstlog"><strong>Base 2.4 · §5.2.13.1.7</strong><br>Printed pages 229–232 · PDF 255–258 · Figure 218–219</li>
<li id="ref-telemetrylog"><strong>Base 2.4 · §5.2.13.1.8–5.2.13.1.9</strong><br>Printed pages 232–237 · PDF 258–263 · Figure 220–223</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-pelcontext"><strong>Base 2.4 · §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</strong><br>Printed pages 244–256, 258 · PDF 270–282, 284 · Figure 232–244, 246</li>
<li id="ref-sanitizelog"><strong>Base 2.4 · §5.2.13.1.38</strong><br>Printed pages 313–320 · PDF 339–346 · Figure 312</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-profile"><strong>Base 2.4 · §5.2.30.1.18</strong><br>Printed pages 478–479 · PDF 504–505 · Figure 494–495</li>
<li id="ref-uuid"><strong>Base 2.4 · §8.1.31.1–8.1.31.2</strong><br>Printed pages 737–738 · PDF 763–764 · Figure 782</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/logs/en/#figure-b217">Base 2.4 Figure 217 · Commands Supported and Effects Data Structure</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/logs/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/logs.html">Chinese tutorial HTML</a></nav>
</div>
<script>
(function(){
 const root=document.querySelector('.nvme-qa'); if(!root)return;
 root.querySelectorAll('.qa-controls').forEach(x=>x.hidden=false);
 root.querySelectorAll('[data-expand]').forEach(b=>b.addEventListener('click',()=>root.querySelectorAll('.qa-answer').forEach(d=>d.open=b.dataset.expand==='true')));
 const input=root.querySelector('#qa-search'),items=[...root.querySelectorAll('.qa-question,.qa-search-item')],output=root.querySelector('#qa-count');
 if(input)input.addEventListener('input',()=>{const q=input.value.trim().toLowerCase();let n=0;items.forEach(el=>{el.hidden=!el.textContent.toLowerCase().includes(q);if(!el.hidden)n++;});output.textContent=n+' / '+items.length;});
 function reveal(){let el=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(el){for(let p=el;p;p=p.parentElement){if(p.tagName==='DETAILS')p.open=true;}el.hidden=false;}}
 addEventListener('hashchange',reveal);reveal();
 let printState=[];addEventListener('beforeprint',()=>{printState=[...root.querySelectorAll('details')].map(d=>[d,d.open]);printState.forEach(([d])=>d.open=true);});addEventListener('afterprint',()=>printState.forEach(([d,open])=>d.open=open));
 const toggle=root.querySelector('[data-theme-toggle]');if(toggle)toggle.addEventListener('click',()=>{const dark=document.documentElement.dataset.theme?document.documentElement.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;document.documentElement.dataset.theme=dark?'light':'dark';});
})();
</script>
