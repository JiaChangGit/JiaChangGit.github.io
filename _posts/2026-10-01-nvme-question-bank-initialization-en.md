---
layout: post
title: "NVMe Self-Study Bank: Controller initialization and disable"
date: 2026-10-01 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/initialization/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/initialization/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/initialization.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q1–Q9</p><h1>Controller initialization and disable</h1><p class="qr-intro">Understand controller state transitions before commands. Discovering capabilities is not enabling; setting EN is not readiness; RDY=1 need not establish readiness of every media operation. This volume connects timing, state and permitted actions.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>From disabled to command submission</h2><p class="qa-takeaway">Wait for the previous lifetime to end before configuring the next; both waits require RDY, not merely the EN value written by the host.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Stage</th><th scope="col">Observation or action</th><th scope="col">Condition for advancing</th></tr></thead><tbody><tr><td>Disable complete</td><td>CC.EN=0; CSTS.RDY=0</td><td>Configure AQA, ASQ, ACQ and CC</td></tr><tr><td>Enabling</td><td>EN 0→1 starts the timer</td><td>Wait for RDY=1; check CFS and applicable timeout</td></tr><tr><td>Interface ready</td><td>RDY=1; apply media restrictions for the ready mode</td><td>Submit permitted Admin commands, then create I/O queues</td></tr><tr><td>Disabling again</td><td>EN 1→0; stop new submissions</td><td>Wait for RDY=0 before another lifetime</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>With hypothetical CAP.TO=4, the disable timeout is 4×500 ms=2 s. This is not an I/O command timeout. Enable additionally requires CAP.CRMS and the selected CRTO rules; 2 s is not universal.</p>
<p class="qa-citations">Sources: <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-adminreg">Base 2.4 §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</a> · <a href="#ref-crto">Base 2.4 §3.1.4 (CRTO)</a> · <a href="#ref-init">Base 2.4 §3.5.1</a> · <a href="#ref-ready">Base 2.4 §3.5.3–3.5.4</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-001">Q01 · How does a host discover version, queue limits, timeouts, doorbell stride, page sizes and command sets from CAP and VS?</a></li>
<li><a href="#q-002">Q02 · In what order are AQA, ASQ, ACQ and CC programmed, and what happens if they are wrong?</a></li>
<li><a href="#q-003">Q03 · How does a host judge enable completion using CC.EN, CSTS.RDY and the timeout fields?</a></li>
<li><a href="#q-004">Q04 · How is disable completion detected, and may the host re-enable before it completes?</a></li>
<li><a href="#q-005">Q05 · May a host submit commands or update doorbells while CSTS.RDY is zero?</a></li>
<li><a href="#q-006">Q06 · What does CSTS.CFS mean, and how should the host recover from initialization failure or a fatal state?</a></li>
<li><a href="#q-007">Q07 · Which ready modes exist, and how should the host handle limited readiness?</a></li>
<li><a href="#q-008">Q08 · How do Enable, Disable, Controller Reset, NVM Subsystem Reset and Shutdown differ?</a></li>
<li><a href="#q-009">Q09 · What must be reinitialized after Controller Reset?</a></li>
</ol></section>
<article class="qa-question" id="q-001" data-question="1" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-001">Q01</a> How does a host discover version, queue limits, timeouts, doorbell stride, page sizes and command sets from CAP and VS?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-001-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-001-a-01">Discover legal interface configurations before issuing commands. CAP advertises capabilities; CC contains host selections. Capability bits are not values to copy blindly into configuration fields.</p><div class="qa-sections">
<section class="qa-section" id="q-001-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-001-a-02"></span><p>These reads observe one controller without changing queues or media. A version number does not establish support for every optional feature.</p>
<span class="qa-anchor" id="q-001-a-03"></span><p>VS.MJR/MNR/TER encode the version. CAP.MQES+1 limits I/O queue entries, CQR specifies physical-contiguity requirements, and CSS describes command-set support.</p>
</section>
<section class="qa-section" id="q-001-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-001-a-04"></span><p>CAP.TO uses 500 ms units. Doorbell stride is 2^(2+DSTRD) bytes; supported pages range from 2^(12+MPSMIN) to 2^(12+MPSMAX) bytes. Enable timeout also requires CRTO.</p>
<span class="qa-anchor" id="q-001-a-05"></span><p>Map the NVMe registers, read VS/CAP, select legal MPS/CSS/AMS and ready mode, then configure queues. If IOCSS=1, discover combinations with Identify CNS 1Ch after enabling.</p>
<span class="qa-anchor" id="q-001-a-06"></span><p>The result is configuration information, not a CQE. For example, MQES=03FFh means up to 1024 slots; DSTRD=2 means adjacent doorbells are 16 bytes apart.</p>
</section>
<section class="qa-section" id="q-001-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-001-a-07"></span><p>Reading read-only registers has no Invalid Field CQE. Later programming unsupported CC.MPS/AMS values can be undefined behavior, not a condition with a guaranteed error completion.</p>
<span class="qa-anchor" id="q-001-a-16"></span><p>Cross-check CAP.CSS against CC.CSS and Identify combinations, and MQES against Create Queue QSIZE. Admin queues have their separate 4096-slot AQA limit.</p>
</section>
</div>
<span class="qa-anchor" id="q-001-a-17"></span><span class="qa-anchor" id="q-001-a-08"></span><span class="qa-anchor" id="q-001-a-09"></span><span class="qa-anchor" id="q-001-a-10"></span><span class="qa-anchor" id="q-001-a-11"></span><span class="qa-anchor" id="q-001-a-12"></span><span class="qa-anchor" id="q-001-a-13"></span><span class="qa-anchor" id="q-001-a-14"></span><span class="qa-anchor" id="q-001-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-crto">Base 2.4 §3.1.4 (CRTO)</a> · <a href="#ref-init">Base 2.4 §3.5.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-002" data-question="2" data-answer-kind="process"><h2><a class="qa-qid" href="#q-002">Q02</a> In what order are AQA, ASQ, ACQ and CC programmed, and what happens if they are wrong?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-002-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-002-a-01">Provide valid Admin SQ/CQ storage before enabling the controller. Establish memory and pointers before allowing command processing.</p><div class="qa-sections">
<section class="qa-section" id="q-002-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-002-a-02"></span><p>This controls the controller&#x27;s management interface. A wrong queue address may prevent every subsequent Identify or Get Features from completing.</p>
<span class="qa-anchor" id="q-002-a-03"></span><p>Check CAP&#x27;s MPS range, CSS, AMS and CRMS, together with AQA&#x27;s Admin queue limits.</p>
<span class="qa-anchor" id="q-002-a-04"></span><p>AQA.ASQS/ACQS encode entries−1. ASQ/ACQ contain physical bases aligned to CC.MPS. Configure CSS, MPS, AMS and CRIME in CC; NVM I/O uses IOSQES=6 and IOCQES=4.</p>
</section>
<section class="qa-section" id="q-002-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-002-a-05"></span><p>Wait for the previous reset to reach RDY=0. Allocate contiguous Admin queues and clear Admin CQ phases. Program AQA/ASQ/ACQ and legal CC fields with EN=0, then enable and wait for RDY=1. Set I/O entry sizes before Create I/O Queue.</p>
<span class="qa-anchor" id="q-002-a-06"></span><p>The Admin queues become usable for Identify. I/O queues are not automatically created, and independent mode does not imply that every medium is ready.</p>
</section>
<section class="qa-section" id="q-002-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-002-a-07"></span><p>Enabling with an AQA size of zero, changing MPS while enabled or selecting unsupported MPS/AMS has undefined results. Do not invent Invalid Field CQEs for these register violations.</p>
<span class="qa-anchor" id="q-002-a-16"></span><p>Validate register encodings and then a correctly identified Identify completion. CC.EN=1 alone does not establish successful initialization.</p>
</section>
</div>
<span class="qa-anchor" id="q-002-a-17"></span><span class="qa-anchor" id="q-002-a-08"></span><span class="qa-anchor" id="q-002-a-09"></span><span class="qa-anchor" id="q-002-a-10"></span><span class="qa-anchor" id="q-002-a-11"></span><span class="qa-anchor" id="q-002-a-12"></span><span class="qa-anchor" id="q-002-a-13"></span><span class="qa-anchor" id="q-002-a-14"></span><span class="qa-anchor" id="q-002-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-adminreg">Base 2.4 §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-init">Base 2.4 §3.5.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-003" data-question="3" data-answer-kind="process"><h2><a class="qa-qid" href="#q-003">Q03</a> How does a host judge enable completion using CC.EN, CSTS.RDY and the timeout fields?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-003-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-003-a-01">Separate the enable request from readiness and avoid premature recovery caused by a wrong timeout. Base 2.4 requires considering CRTO as well.</p><div class="qa-sections">
<section class="qa-section" id="q-003-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-003-a-02"></span><p>This establishes readiness of the target controller; media availability also depends on the selected ready mode.</p>
<span class="qa-anchor" id="q-003-a-03"></span><p>Read CAP.CRMS, CC.CRIME, CRTO.CRWMT/CRIMT and CAP.TO. CAP.TO alone does not cover every enable timeout.</p>
</section>
<section class="qa-section" id="q-003-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-003-a-04"></span>
<span class="qa-anchor" id="q-003-a-05"></span>
<span class="qa-anchor" id="q-003-a-06"></span>
<span class="qa-anchor" id="q-003-a-17"></span>
<figure class="qa-flow" id="q-003-flow"><figcaption>The two readiness deadlines</figcaption>
<p>Interface readiness and media readiness are separate. Both deadlines start at Enable; the media timer does not restart when RDY becomes 1.</p><ol class="qa-flow-steps">
<li class="qa-flow-step"><strong>Start: CC.EN changes from 0 to 1</strong><p>Record the time and CC.CRIME; observe RDY and CFS throughout initialization.</p></li>
<li class="qa-flow-branch"><strong>Branch A: With Media</strong><p>Use CRWMT for the readiness deadline, in 500 ms units. Submit commands permitted by this mode only after RDY=1.</p></li>
<li class="qa-flow-branch"><strong>Branch B: Independent</strong><p>Use CRIMT for interface readiness and CRWMT for the media deadline. RDY=1 does not prove media health or availability; command-specific media conditions still apply.</p></li>
<li class="qa-flow-step"><strong>Check a single timeline</strong><p>With hypothetical CRIMT=2 and CRWMT=20, the deadlines are 1 s and 10 s after Enable.</p></li>
</ol><p class="qa-flow-conclusion">A and B are alternative modes, not consecutive actions. Evaluate CFS and failure conditions; merely observing RDY=1 does not establish successful initialization.</p></figure>
</section>
<section class="qa-section" id="q-003-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-003-a-07"></span><p>Register enabling has no CQE. While media is unready, eligible commands may return Namespace Not Ready (SCT=0, SC=82h) or Admin Command Media Not Ready (0/24h).</p>
<span class="qa-anchor" id="q-003-a-16"></span><p>Correlate timing, CRIME, command type and status. Figure 84&#x27;s eligible Admin commands and restrictions do not permit rejecting every Admin command temporarily.</p>
</section>
<section class="qa-section" id="q-003-s-04" data-answer-section="4"><h3><span>4.</span> Correlate error completions and records</h3>
<span class="qa-anchor" id="q-003-a-08"></span><p>Enabling has no DNR/More. Eligible media-not-ready responses may have DNR=0 during the allowed Independent-mode interval; that transient explanation cannot continue with DNR=0 beyond CRWMT. More reflects additional Error Information.</p>
<span class="qa-anchor" id="q-003-a-11"></span><p>For an initialization-deadline failure meeting §3.5.4.1, a controller supporting PEL shall record an NVM Subsystem Hardware Error Event with Controller Ready Timeout Exceeded. This is not a record for every successful enable.</p>
</section>
</div>
<span class="qa-anchor" id="q-003-a-09"></span><span class="qa-anchor" id="q-003-a-10"></span><span class="qa-anchor" id="q-003-a-12"></span><span class="qa-anchor" id="q-003-a-13"></span><span class="qa-anchor" id="q-003-a-14"></span><span class="qa-anchor" id="q-003-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-crto">Base 2.4 §3.1.4 (CRTO)</a> · <a href="#ref-ready">Base 2.4 §3.5.3–3.5.4</a> · <a href="#ref-init">Base 2.4 §3.5.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-004" data-question="4" data-answer-kind="process"><h2><a class="qa-qid" href="#q-004">Q04</a> How is disable completion detected, and may the host re-enable before it completes?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-004-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-004-a-01">Establish that old command processing has stopped before beginning another initialization lifetime.</p><div class="qa-sections">
<section class="qa-section" id="q-004-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-004-a-02"></span><p>Clearing EN resets this controller and all its I/O queues; it does not merely pause one SQ.</p>
<span class="qa-anchor" id="q-004-a-03"></span><p>CAP.TO defines the worst-case wait for RDY 1→0 after EN is cleared. Preserve CC/CSTS snapshots too.</p>
<span class="qa-anchor" id="q-004-a-04"></span><p>In the normal enabled state, initiate EN 1→0 with RDY=1; RDY=0 indicates readiness to enable again.</p>
</section>
<section class="qa-section" id="q-004-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-004-a-05"></span><p>Stop new submissions, clear EN and poll RDY. Once zero, reinitialize Admin CQ and host tracking, configure CC and enable again.</p>
<span class="qa-anchor" id="q-004-a-06"></span><p>RDY=0 establishes disable completion; receiving a CQE for every old command is not required. Old I/O queues are invalid.</p>
</section>
<section class="qa-section" id="q-004-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-004-a-07"></span><p>Setting EN 0→1 while RDY remains 1 has undefined results. This is not an Admin request requiring Command Sequence Error.</p>
<span class="qa-anchor" id="q-004-a-16"></span><p>Check EN/RDY transitions and retirement of old queues. Residual data in an old queue does not prove it is reusable.</p>
</section>
</div>
<span class="qa-anchor" id="q-004-a-17"></span><span class="qa-anchor" id="q-004-a-08"></span><span class="qa-anchor" id="q-004-a-09"></span><span class="qa-anchor" id="q-004-a-10"></span><span class="qa-anchor" id="q-004-a-11"></span><span class="qa-anchor" id="q-004-a-12"></span><span class="qa-anchor" id="q-004-a-13"></span><span class="qa-anchor" id="q-004-a-14"></span><span class="qa-anchor" id="q-004-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-005" data-question="5" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-005">Q05</a> May a host submit commands or update doorbells while CSTS.RDY is zero?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-005-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-005-a-01">Distinguish preparing an SQE in host memory from submitting it. A doorbell is the submission boundary and cannot be used prematurely.</p><div class="qa-sections">
<section class="qa-section" id="q-005-s-01" data-answer-section="1"><h3><span>1.</span> When commands may be submitted</h3>
<span class="qa-anchor" id="q-005-a-02"></span><p>This applies to Admin and I/O submission on this PCIe controller. Configuring Admin queue registers during initialization is different from command submission.</p>
<span class="qa-anchor" id="q-005-a-03"></span><p>Check CSTS.RDY, CC.EN and queue existence. Even RDY=1 requires a created queue and consideration of shutdown state.</p>
<span class="qa-anchor" id="q-005-a-05"></span><p>Wait for RDY=1 and a valid queue lifetime, make the SQE visible to the device, then update SQ Tail.</p>
</section>
<section class="qa-section" id="q-005-s-02" data-answer-section="2"><h3><span>2.</span> Doorbells do not replace readiness</h3>
<span class="qa-anchor" id="q-005-a-04"></span><p>SQ Tail announces submissions; CQ Head announces consumed completions. Neither is a command for making the controller ready.</p>
<span class="qa-anchor" id="q-005-a-07"></span><p>Violating readiness or queue-lifetime preconditions has no guaranteed CQE. A disabled Admin Queue cannot be relied upon to report the misuse.</p>
<span class="qa-anchor" id="q-005-a-16"></span><p>EN=1, RDY=0 and a timeout first indicate an initialization-state issue; an illegally early Identify is not evidence that Identify is unsupported.</p>
</section>
</div>
<span class="qa-anchor" id="q-005-a-06"></span><span class="qa-anchor" id="q-005-a-17"></span><span class="qa-anchor" id="q-005-a-08"></span><span class="qa-anchor" id="q-005-a-09"></span><span class="qa-anchor" id="q-005-a-10"></span><span class="qa-anchor" id="q-005-a-11"></span><span class="qa-anchor" id="q-005-a-12"></span><span class="qa-anchor" id="q-005-a-13"></span><span class="qa-anchor" id="q-005-a-14"></span><span class="qa-anchor" id="q-005-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-qattr">Base 2.4 §3.3.3–3.4.1</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-006" data-question="6" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-006">Q06</a> What does CSTS.CFS mean, and how should the host recover from initialization failure or a fatal state?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-006-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-006-a-01">CFS normally signals a serious controller condition rather than an individual command error. A virtualized secondary controller also sets CFS when Offline, so establish its role and Online/Offline state before diagnosing a hardware failure.</p><div class="qa-sections">
<section class="qa-section" id="q-006-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-006-a-02"></span><p>The failure may affect controller-wide command service. CFS and an individual namespace media error are not interchangeable.</p>
<span class="qa-anchor" id="q-006-a-03"></span><p>Observe CSTS.CFS with RDY, CC.EN and the applicable timeout. No Identify optional-capability bit permits ignoring CFS.</p>
<span class="qa-anchor" id="q-006-a-04"></span><p>Preserve registers and available CQEs/logs first. Collect diagnostics if the Admin path still works, without waiting indefinitely for an inaccessible Get Log Page.</p>
</section>
<section class="qa-section" id="q-006-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-006-a-17"></span><p>First confirm valid register access and an actual CFS value of 1. An all-ones failed read is not evidence that every status bit is asserted.</p>
<span class="qa-anchor" id="q-006-a-05"></span><p>Perform Controller Level Reset as appropriate to the failure and accessible interface, then reinitialize. An unresponsive interface requires platform recovery; a CC.EN reset is not guaranteed to repair every fault.</p>
</section>
<section class="qa-section" id="q-006-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-006-a-06"></span><p>Verify RDY, Identify and command completion on new queues after recovery. Clearing CFS alone does not validate data integrity.</p>
<span class="qa-anchor" id="q-006-a-07"></span><p>Internal Error (SCT=0, SC=06h) may apply when affected commands can still complete. Serious failure preventing CQE communication may set CFS; do not require a CQE for every command.</p>
<span class="qa-anchor" id="q-006-a-16"></span><p>Correlate CFS, initialization deadlines and hardware records at the same time. One Invalid Field completion is not itself controller-fatal evidence.</p>
</section>
</div>
<span class="qa-anchor" id="q-006-a-08"></span><span class="qa-anchor" id="q-006-a-09"></span><span class="qa-anchor" id="q-006-a-10"></span><span class="qa-anchor" id="q-006-a-11"></span><span class="qa-anchor" id="q-006-a-12"></span><span class="qa-anchor" id="q-006-a-13"></span><span class="qa-anchor" id="q-006-a-14"></span><span class="qa-anchor" id="q-006-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-ready">Base 2.4 §3.5.3–3.5.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-007" data-question="7" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-007">Q07</a> Which ready modes exist, and how should the host handle limited readiness?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-007-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-007-a-01">Allow management work before media initialization finishes while retaining an explicit media-readiness deadline.</p><div class="qa-sections">
<section class="qa-section" id="q-007-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-007-a-02"></span><p>The modes are Controller Ready With Media and Controller Ready Independent of Media, not arbitrary degraded-ready encodings.</p>
<span class="qa-anchor" id="q-007-a-04"></span><p>CRIME=0 selects With Media; CRIME=1 selects Independent. RDY, CRTO.CRIMT/CRWMT and Figure 84&#x27;s command classes determine permitted work.</p>
</section>
<section class="qa-section" id="q-007-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-007-a-03"></span><p>CAP.CRMS.CRWMS/CRIMS advertise support. With CAP.CRMS=11b, CC.CRIME selects the mode.</p>
<span class="qa-anchor" id="q-007-a-05"></span><p>Select before enable. After Independent-mode RDY=1, perform media-independent discovery; defer eligible media operations based on transient status and track CRWMT from enable.</p>
<span class="qa-anchor" id="q-007-a-06"></span><p>Normal With Media readiness includes required media readiness. Independent RDY=1 initially establishes interface and eligible-command readiness, not readiness of every namespace.</p>
</section>
<section class="qa-section" id="q-007-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-007-a-07"></span><p>Eligible cases may return 0/82h or 0/24h. The latter is restricted to appropriate Admin commands in Independent mode. Continuing the same transient DNR=0 explanation beyond the media deadline violates that timing rule.</p>
<span class="qa-anchor" id="q-007-a-16"></span><p>Cross-check CAP support, CC selection, timeouts and behavior. CSTS.PP is a separate processing-pause indication, not a third ready mode.</p>
</section>
</div>
<span class="qa-anchor" id="q-007-a-17"></span><span class="qa-anchor" id="q-007-a-08"></span><span class="qa-anchor" id="q-007-a-09"></span><span class="qa-anchor" id="q-007-a-10"></span><span class="qa-anchor" id="q-007-a-11"></span><span class="qa-anchor" id="q-007-a-12"></span><span class="qa-anchor" id="q-007-a-13"></span><span class="qa-anchor" id="q-007-a-14"></span><span class="qa-anchor" id="q-007-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/initialization/en/#q-003">Q3</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-ready">Base 2.4 §3.5.3–3.5.4</a> · <a href="#ref-crto">Base 2.4 §3.1.4 (CRTO)</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-008" data-question="8" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-008">Q08</a> How do Enable, Disable, Controller Reset, NVM Subsystem Reset and Shutdown differ?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-008-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-008-a-01">Separate starting service, stopping/resetting and preparing for power removal. Reset is not a replacement for orderly shutdown.</p><div class="qa-sections">
<section class="qa-section" id="q-008-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-008-a-02"></span><p>Enable and CC.EN clearing target a controller. NVM Subsystem Reset covers its defined subsystem/domain scope. Shutdown also distinguishes controller and subsystem types.</p>
<span class="qa-anchor" id="q-008-a-04"></span><p>Enable is EN 0→1; Controller Reset is EN 1→0. Writing 4E564D65h to supported NSSR.NSSRC requests subsystem reset. Normal controller shutdown uses CC.SHN=01b and waits for SHST=10b.</p>
</section>
<section class="qa-section" id="q-008-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-008-a-03"></span><p>CAP.NSSRS advertises NSSR support; shutdown capability and CSTS.ST distinguish shutdown scope.</p>
<span class="qa-anchor" id="q-008-a-05"></span><p>Coordinate I/O, notify shutdown and await completion before normal power removal. Select a suitable reset for recovery, then rebuild the operating environment.</p>
<span class="qa-anchor" id="q-008-a-06"></span><p>Enable uses RDY=1; disable/reset uses its corresponding state; shutdown uses SHST=10b. Completed shutdown does not mean every register has its reset value.</p>
</section>
<section class="qa-section" id="q-008-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-008-a-07"></span><p>Register operations have no common CQE. During shutdown, commands may return Commands Aborted due to Power Loss Notification (0/05h); that code is not universal for commands interrupted by reset.</p>
<span class="qa-anchor" id="q-008-a-16"></span><p>Record the trigger and scope before comparing retained state. A log saying only “reset” cannot explain differences in AQA, PCIe state or features.</p>
</section>
</div>
<span class="qa-anchor" id="q-008-a-17"></span><span class="qa-anchor" id="q-008-a-08"></span><span class="qa-anchor" id="q-008-a-09"></span><span class="qa-anchor" id="q-008-a-10"></span><span class="qa-anchor" id="q-008-a-11"></span><span class="qa-anchor" id="q-008-a-12"></span><span class="qa-anchor" id="q-008-a-13"></span><span class="qa-anchor" id="q-008-a-14"></span><span class="qa-anchor" id="q-008-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-shutdown">Base 2.4 §3.6.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-009" data-question="9" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-009">Q09</a> What must be reinitialized after Controller Reset?</h2>
<p class="qa-prompt">Name the reset or interruption, then assess settings, ongoing operations and data separately.</p>
<details class="qa-answer" id="q-009-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-009-a-01">Establish a fresh operating lifetime rather than reusing old pointers, phases and outstanding commands.</p><div class="qa-sections">
<section class="qa-section" id="q-009-s-01" data-answer-section="1"><h3><span>1.</span> Identify the trigger and affected objects</h3>
<span class="qa-anchor" id="q-009-a-02"></span><p>Here Controller Reset specifically means clearing CC.EN. Do not mix in the register-retention rules of FLR or NVM Subsystem Reset.</p>
<span class="qa-anchor" id="q-009-a-03"></span><p>Use §3.7.2&#x27;s exceptions and register Reset columns; for features examine scope, saveability and Figures 126/127/466.</p>
</section>
<section class="qa-section" id="q-009-s-02" data-answer-section="2"><h3><span>2.</span> State changes and recovery</h3>
<span class="qa-anchor" id="q-009-a-04"></span><p>This reset preserves AQA/ASQ/ACQ, specified PMR registers and CMBMSC, but still resets Admin Queue pointers. All I/O queues are deleted and CC selections require reconfiguration. Saveable features restore Saved, or Default without Saved, under reset-scope rules; unsaveable features use their persistence rules. Reconfigure HMB.</p>
<span class="qa-anchor" id="q-009-a-05"></span><p>Wait for RDY=0, verify retained Admin memory remains valid and initialize Admin CQ phases to zero. Configure and enable, rediscover needed capabilities/features, renegotiate Number of Queues, then create CQs before SQs.</p>
<span class="qa-anchor" id="q-009-a-06"></span><p>New commands complete in the new queue lifetime. Reusing a QID or address does not resume the old queue.</p>
</section>
<section class="qa-section" id="q-009-s-03" data-answer-section="3"><h3><span>3.</span> Verify retention and recovery</h3>
<span class="qa-anchor" id="q-009-a-07"></span><p>There is no universal Reset Status owed for every old command. Invalid reconstruction parameters follow Create-command rules; writing doorbells for stale memory is not a recovery method.</p>
<span class="qa-anchor" id="q-009-a-16"></span><p>Compare register values, Get Features and actual queue capability. Retention of AQA is distinct from validity of Admin CQ contents.</p>
<span class="qa-anchor" id="q-009-a-17"></span><p>First check retirement of old outstanding tracking and phase reinitialization. A reused CID must not resolve to a command from the previous lifetime.</p>
</section>
</div>
<span class="qa-anchor" id="q-009-a-08"></span><span class="qa-anchor" id="q-009-a-09"></span><span class="qa-anchor" id="q-009-a-10"></span><span class="qa-anchor" id="q-009-a-11"></span><span class="qa-anchor" id="q-009-a-12"></span><span class="qa-anchor" id="q-009-a-13"></span><span class="qa-anchor" id="q-009-a-14"></span><span class="qa-anchor" id="q-009-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-adminreg">Base 2.4 §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>

<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-cap"><strong>Base 2.4 · §3.1.4 (CAP, VS)</strong><br>Printed pages 54–59 · PDF 80–85 · Figure 36–37</li>
<li id="ref-cc"><strong>Base 2.4 · §3.1.4 (CC, CSTS, NSSR)</strong><br>Printed pages 60–66 · PDF 86–92 · Figure 41–43</li>
<li id="ref-adminreg"><strong>Base 2.4 · §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</strong><br>Printed pages 66–68 · PDF 92–94 · Figure 44–47</li>
<li id="ref-crto"><strong>Base 2.4 · §3.1.4 (CRTO)</strong><br>Printed pages 72–73 · PDF 98–99 · Figure 57</li>
<li id="ref-queue"><strong>Base 2.4 · §3.3.1</strong><br>Printed pages 88–91 · PDF 114–117 · Figure 73–74</li>
<li id="ref-qattr"><strong>Base 2.4 · §3.3.3–3.4.1</strong><br>Printed pages 101 · PDF 127</li>
<li id="ref-init"><strong>Base 2.4 · §3.5.1</strong><br>Printed pages 105–106 · PDF 131–132</li>
<li id="ref-ready"><strong>Base 2.4 · §3.5.3–3.5.4</strong><br>Printed pages 109–113 · PDF 135–139 · Figure 84–85</li>
<li id="ref-shutdown"><strong>Base 2.4 · §3.6.1</strong><br>Printed pages 114–115 · PDF 140–141</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>Printed pages 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>Printed pages 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-virtual"><strong>Base 2.4 · §8.2.7</strong><br>Printed pages 754–758 · PDF 780–784 · Figure 796</li>
<li id="ref-fatal"><strong>Base 2.4 · §9.1–9.6.1</strong><br>Printed pages 825–826 · PDF 851–852</li>
<li id="ref-pcie"><strong>PCIe Transport 1.4 · §3.1–3.4</strong><br>Printed pages 9–13 · PDF 9–13 · Figure 3–8</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b42">Base 2.4 Figure 42 · Offset 1Ch: CSTS – Controller Status</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b44">Base 2.4 Figure 44 · Offset 24h: AQA – Admin Queue Attributes</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b45">Base 2.4 Figure 45 · Offset 28h: ASQ – Admin Submission Queue Base Address</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b46">Base 2.4 Figure 46 · Offset 30h: ACQ – Admin Completion Queue Base Address</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/initialization/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/initialization.html">Chinese tutorial HTML</a></nav>
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
