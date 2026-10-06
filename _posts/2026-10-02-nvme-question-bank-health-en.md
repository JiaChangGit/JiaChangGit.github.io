---
layout: post
title: "NVMe Self-Study Bank: Power, thermal and health monitoring"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/health/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/health/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/health.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q188–Q204</p><h1>Power, thermal and health monitoring</h1><p class="qr-intro">Power states, thermal control and health counters are related but answer different questions. Learn state and timing before warnings and workload.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Separate controls, current state and lifetime counts</h2><p class="qa-takeaway">A configured threshold is not a warning, and warning recovery does not clear lifetime workload.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Kind</th><th scope="col">Examples</th><th scope="col">Comparison</th></tr></thead><tbody><tr><td>Control</td><td>APST/HCTM settings</td><td>Check units/support</td></tr><tr><td>Current state</td><td>Temperature and warning</td><td>Compare contemporaneous conditions</td></tr><tr><td>Cumulative</td><td>Data, busy time and power loss</td><td>Differences and quantization</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>A 2000 ms idle threshold and 100 µs exit latency describe different phases, not a fixed per-command delay.</p>
<p class="qa-citations">Sources: <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-188">Q188 · What does a Power State Descriptor tell the host?</a></li>
<li><a href="#q-189">Q189 · How do operational and non-operational power states differ?</a></li>
<li><a href="#q-190">Q190 · How do entry and exit latency affect command waits?</a></li>
<li><a href="#q-191">Q191 · How is APST configured, triggered and disabled?</a></li>
<li><a href="#q-192">Q192 · How should an apparent EXLAT violation be evaluated?</a></li>
<li><a href="#q-193">Q193 · How should HCTM TMT1 and TMT2 be configured?</a></li>
<li><a href="#q-194">Q194 · When does thermal management start and stop?</a></li>
<li><a href="#q-195">Q195 · How are power and thermal settings restored?</a></li>
<li><a href="#q-196">Q196 · What do SMART Critical Warning bits mean?</a></li>
<li><a href="#q-197">Q197 · How are spare capacity and percentage used interpreted?</a></li>
<li><a href="#q-198">Q198 · How do SMART workload and uptime counters accumulate?</a></li>
<li><a href="#q-199">Q199 · How do unexpected power-loss and error counters accumulate?</a></li>
<li><a href="#q-200">Q200 · How are warning and critical temperature times counted?</a></li>
<li><a href="#q-201">Q201 · How do sensor temperatures relate to Composite Temperature?</a></li>
<li><a href="#q-202">Q202 · Which health changes generate asynchronous events?</a></li>
<li><a href="#q-203">Q203 · How is SMART data scope determined?</a></li>
<li><a href="#q-204">Q204 · How are SMART, operations, errors and PEL cross-checked?</a></li>
</ol></section>
<article class="qa-question" id="q-188" data-question="188" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-188">Q188</a> What does a Power State Descriptor tell the host?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-188-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-188-a-01">The host trades power against performance and wake latency. Descriptors characterize states, not the completion time of every command.</p><div class="qa-sections">
<section class="qa-section" id="q-188-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-188-a-02"></span><p>NPSS enumerates controller states PS0 through PSn; a value of 4 means five states.</p>
<span class="qa-anchor" id="q-188-a-03"></span><p>Establish Power Management applicability, then inspect NPSS and PSDs; ignore PSDs for a controller without support.</p>
</section>
<section class="qa-section" id="q-188-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-188-a-04"></span><p>NOPS classifies the state; MP uses its scale; ENLAT/EXLAT are microseconds. Relative performance ranks differ from scaled idle/active power and MBW/MBWS bandwidth.</p>
<span class="qa-anchor" id="q-188-a-05"></span><p>Compare class and power, then transition latency, then like-for-like performance ranks.</p>
<span class="qa-anchor" id="q-188-a-06"></span><p>Successful Identify supports state selection; Power Management or APST performs selection in operation.</p>
</section>
<section class="qa-section" id="q-188-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-188-a-07"></span><p>A state beyond NPSS is invalid for selection. Unreported measurements are not guarantees of zero consumption or latency.</p>
<span class="qa-anchor" id="q-188-a-16"></span><p>Cross-check NOPS, scales and selected state; ranks are not absolute IOPS.</p>
</section>
</div>
<span class="qa-anchor" id="q-188-a-17"></span><span class="qa-anchor" id="q-188-a-08"></span><span class="qa-anchor" id="q-188-a-09"></span><span class="qa-anchor" id="q-188-a-10"></span><span class="qa-anchor" id="q-188-a-11"></span><span class="qa-anchor" id="q-188-a-12"></span><span class="qa-anchor" id="q-188-a-13"></span><span class="qa-anchor" id="q-188-a-14"></span><span class="qa-anchor" id="q-188-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-189" data-question="189" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-189">Q189</a> How do operational and non-operational power states differ?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-189-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-189-a-01">This classifies I/O readiness, not whether the controller is completely unpowered.</p><div class="qa-sections">
<section class="qa-section" id="q-189-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-189-a-02"></span><p>NOPS=0 is operational; NOPS=1 is non-operational, while registers, Admin commands and permitted background work may remain active.</p>
<span class="qa-anchor" id="q-189-a-04"></span><p>APST enters non-operational states; NOPPME controls background policy, not all Admin access.</p>
</section>
<section class="qa-section" id="q-189-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-189-a-03"></span><p>Inspect PSD.NOPS, Power Management and Non-Operational Power State Config.</p>
<span class="qa-anchor" id="q-189-a-05"></span><p>I/O causes return to the last operational state regardless of APST enablement.</p>
<span class="qa-anchor" id="q-189-a-06"></span><p>I/O completes after resumption without a separate Set Features wake command per I/O.</p>
</section>
<section class="qa-section" id="q-189-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-189-a-07"></span><p>Arrival during a non-operational state is not itself an invalid I/O request; selecting a nonexistent state is a configuration error.</p>
<span class="qa-anchor" id="q-189-a-16"></span><p>Admin activity or temporary power above the non-operational limit requires examination of permitted operations and applicable power bounds.</p>
</section>
</div>
<span class="qa-anchor" id="q-189-a-17"></span><span class="qa-anchor" id="q-189-a-08"></span><span class="qa-anchor" id="q-189-a-09"></span><span class="qa-anchor" id="q-189-a-10"></span><span class="qa-anchor" id="q-189-a-11"></span><span class="qa-anchor" id="q-189-a-12"></span><span class="qa-anchor" id="q-189-a-13"></span><span class="qa-anchor" id="q-189-a-14"></span><span class="qa-anchor" id="q-189-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-190" data-question="190" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-190">Q190</a> How do entry and exit latency affect command waits?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-190-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-190-a-01">Separate state-transition delay from command execution time.</p><div class="qa-sections">
<section class="qa-section" id="q-190-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-190-a-02"></span><p>ENLAT applies to entry and EXLAT to exit; a multi-state path cannot be reduced to its smallest value.</p>
<span class="qa-anchor" id="q-190-a-03"></span><p>Read source and destination PSDs and the last operational state.</p>
</section>
<section class="qa-section" id="q-190-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-190-a-04"></span><p>Add source EXLAT and destination ENLAT in microseconds; ITPT is a separate idle delay in milliseconds.</p>
<span class="qa-anchor" id="q-190-a-05"></span><p>Establish transition timing and path, then measure readiness separately from execution and host scheduling.</p>
<span class="qa-anchor" id="q-190-a-06"></span><p>With hypothetical 2000 μs exit and 500 μs entry, the transition bound is 2500 μs, not a bound on the entire Read.</p>
</section>
<section class="qa-section" id="q-190-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-190-a-07"></span><p>A late CQE does not define an Exit Latency Error status; isolate the bounded transition first.</p>
<span class="qa-anchor" id="q-190-a-16"></span><p>Compare PSDs, actual source state, APST path and measurement boundaries.</p>
</section>
</div>
<span class="qa-anchor" id="q-190-a-17"></span><span class="qa-anchor" id="q-190-a-08"></span><span class="qa-anchor" id="q-190-a-09"></span><span class="qa-anchor" id="q-190-a-10"></span><span class="qa-anchor" id="q-190-a-11"></span><span class="qa-anchor" id="q-190-a-12"></span><span class="qa-anchor" id="q-190-a-13"></span><span class="qa-anchor" id="q-190-a-14"></span><span class="qa-anchor" id="q-190-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-191" data-question="191" data-answer-kind="process"><h2><a class="qa-qid" href="#q-191">Q191</a> How is APST configured, triggered and disabled?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-191-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-191-a-01">APST reduces power during I/O idle periods without a host command for every transition.</p><div class="qa-sections">
<section class="qa-section" id="q-191-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-191-a-02"></span><p>Each source state has an eight-byte entry; 32 entries occupy 256 bytes.</p>
<span class="qa-anchor" id="q-191-a-03"></span><p>Check APSTA, NPSS and the target NOPS bit.</p>
<span class="qa-anchor" id="q-191-a-04"></span><p>APSTE enables FID 0Ch; ITPT specifies idle milliseconds and ITPS the destination. ITPT=0 disables that source-state transition.</p>
</section>
<section class="qa-section" id="q-191-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-191-a-05"></span>
<span class="qa-anchor" id="q-191-a-06"></span>
<span class="qa-anchor" id="q-191-a-17"></span>
<figure class="qa-flow" id="q-191-flow"><figcaption>APST: configure the source state, then observe idle transition</figcaption>
<p>Assume operational PS0 and supported non-operational PS3. Only this transition is shown.</p><ol class="qa-flow-steps">
<li class="qa-flow-step"><strong>Set the PS0 entry and verify it</strong><p>Set APSTE=1, ITPT=2000 ms and ITPS=3: low Dword 0007D018h. The entry index is source PS0, not destination PS3.</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>PS0 → no outstanding I/O and continuously idle for over 2000 ms</strong><p>These are the entry’s triggering conditions; time since the last submission alone is insufficient.</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>Transition into PS3</strong><p>ITPT is the idle threshold before transition, not state entry or exit latency.</p></li>
</ol><p class="qa-flow-conclusion">Get Features returns configuration, not proof that a transition occurred. ITPT=0 disables that source entry; APSTE=0 disables APST globally.</p></figure>
</section>
<section class="qa-section" id="q-191-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-191-a-07"></span><p>A nonzero ITPT requires a non-operational target; an operational target should cause Invalid Field in Command. APSTE=0 disables APST globally.</p>
<span class="qa-anchor" id="q-191-a-16"></span><p>Get returns configuration, not transition history; background work and its power policy may prevent entry.</p>
</section>
</div>
<span class="qa-anchor" id="q-191-a-08"></span><span class="qa-anchor" id="q-191-a-09"></span><span class="qa-anchor" id="q-191-a-10"></span><span class="qa-anchor" id="q-191-a-11"></span><span class="qa-anchor" id="q-191-a-12"></span><span class="qa-anchor" id="q-191-a-13"></span><span class="qa-anchor" id="q-191-a-14"></span><span class="qa-anchor" id="q-191-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-192" data-question="192" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-192">Q192</a> How should an apparent EXLAT violation be evaluated?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-192-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-192-a-01">Conformance requires matching measurement boundaries rather than attributing every host delay to the controller.</p><div class="qa-sections">
<section class="qa-section" id="q-192-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-192-a-02"></span><p>Isolate one controller, a known state path and one wake transition.</p>
<span class="qa-anchor" id="q-192-a-03"></span><p>Snapshot PSDs, APST, Power Management, temperature and background activity.</p>
<span class="qa-anchor" id="q-192-a-04"></span><p>Use source EXLAT and destination ENLAT; RTD3 has different power-restoration and initialization conditions.</p>
</section>
<section class="qa-section" id="q-192-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-192-a-17"></span><p>First establish whether the start timestamp marks the actual state exit.</p>
<span class="qa-anchor" id="q-192-a-05"></span><p>Exclude submission delay, host scheduling, interrupt coalescing and media execution before measuring the transition.</p>
</section>
<section class="qa-section" id="q-192-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-192-a-06"></span><p>Matching premises support a transition compliance finding; otherwise the evidence establishes only high end-to-end latency.</p>
<span class="qa-anchor" id="q-192-a-07"></span><p>Exceeding EXLAT is not an invalid-command condition with a mandated fixed CQE.</p>
<span class="qa-anchor" id="q-192-a-16"></span><p>Use controlled repeat measurements with timing resolution and uncertainty.</p>
</section>
</div>
<span class="qa-anchor" id="q-192-a-08"></span><span class="qa-anchor" id="q-192-a-09"></span><span class="qa-anchor" id="q-192-a-10"></span><span class="qa-anchor" id="q-192-a-11"></span><span class="qa-anchor" id="q-192-a-12"></span><span class="qa-anchor" id="q-192-a-13"></span><span class="qa-anchor" id="q-192-a-14"></span><span class="qa-anchor" id="q-192-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-193" data-question="193" data-answer-kind="process"><h2><a class="qa-qid" href="#q-193">Q193</a> How should HCTM TMT1 and TMT2 be configured?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-193-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-193-a-01">HCTM supplies host thermal targets for lighter and heavier mitigation.</p><div class="qa-sections">
<section class="qa-section" id="q-193-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-193-a-02"></span><p>It controls target-controller thermal management using Composite Temperature.</p>
<span class="qa-anchor" id="q-193-a-03"></span><p>Check HCTMA and the MNTMT/MXTMT supported range.</p>
<span class="qa-anchor" id="q-193-a-04"></span><p>FID 10h CDW11[31:16] is TMT1 and [15:0] TMT2, both Kelvin; zero disables the respective part.</p>
</section>
<section class="qa-section" id="q-193-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-193-a-05"></span><p>Keep nonzero values in range and TMT1&lt;TMT2 when both are enabled; verify by Get and do not encode Celsius directly.</p>
<span class="qa-anchor" id="q-193-a-06"></span><p>For a hypothetical 300–360 K range, 330/340 K is valid whereas 340/330 K reverses the thresholds.</p>
</section>
<section class="qa-section" id="q-193-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-193-a-07"></span><p>Out-of-range enabled thresholds or invalid ordering require Invalid Field in Command.</p>
<span class="qa-anchor" id="q-193-a-16"></span><p>Compare thresholds, SMART temperature and thermal counters; temperature-warning FID 04h is separate.</p>
</section>
</div>
<span class="qa-anchor" id="q-193-a-17"></span><span class="qa-anchor" id="q-193-a-08"></span><span class="qa-anchor" id="q-193-a-09"></span><span class="qa-anchor" id="q-193-a-10"></span><span class="qa-anchor" id="q-193-a-11"></span><span class="qa-anchor" id="q-193-a-12"></span><span class="qa-anchor" id="q-193-a-13"></span><span class="qa-anchor" id="q-193-a-14"></span><span class="qa-anchor" id="q-193-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-194" data-question="194" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-194">Q194</a> When does thermal management start and stop?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-194-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-194-a-01">Thresholds trigger action without prescribing one universal throttling curve.</p><div class="qa-sections">
<section class="qa-section" id="q-194-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-194-a-02"></span><p>Decisions use Composite Temperature, not an arbitrary physical sensor.</p>
<span class="qa-anchor" id="q-194-a-04"></span><p>At enabled TMT1 below enabled TMT2, lighter mitigation should begin; reaching enabled TMT2 shall trigger mitigation regardless of performance impact.</p>
</section>
<section class="qa-section" id="q-194-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-194-a-03"></span><p>Check enabled thresholds, CTEMP, transition counts and accumulated seconds.</p>
<span class="qa-anchor" id="q-194-a-05"></span><p>Track rising and falling temperature; vendor-specific hysteresis means crossing below TMT2 need not immediately restore full performance.</p>
<span class="qa-anchor" id="q-194-a-06"></span><p>Observe consistent mitigation and thermal counters; the specific mechanism is vendor-defined.</p>
</section>
<section class="qa-section" id="q-194-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-194-a-07"></span><p>Continued throttling below TMT2 is not alone a violation; inspect TMT1, hysteresis and other protection mechanisms.</p>
<span class="qa-anchor" id="q-194-a-16"></span><p>Preserve the different should/shall strengths for the two thresholds.</p>
</section>
</div>
<span class="qa-anchor" id="q-194-a-17"></span><span class="qa-anchor" id="q-194-a-08"></span><span class="qa-anchor" id="q-194-a-09"></span><span class="qa-anchor" id="q-194-a-10"></span><span class="qa-anchor" id="q-194-a-11"></span><span class="qa-anchor" id="q-194-a-12"></span><span class="qa-anchor" id="q-194-a-13"></span><span class="qa-anchor" id="q-194-a-14"></span><span class="qa-anchor" id="q-194-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-195" data-question="195" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-195">Q195</a> How are power and thermal settings restored?</h2>
<p class="qa-prompt">Name the reset or interruption, then assess settings, ongoing operations and data separately.</p>
<details class="qa-answer" id="q-195-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-195-a-01">Distinguish saved configuration, current configuration and live thermal/power state.</p><div class="qa-sections">
<section class="qa-section" id="q-195-s-01" data-answer-section="1"><h3><span>1.</span> Identify the trigger and affected objects</h3>
<span class="qa-anchor" id="q-195-a-02"></span><p>Treat Power Management, APST, HCTM and NOPS Config as separate features.</p>
<span class="qa-anchor" id="q-195-a-03"></span><p>Use SEL=3 for capabilities and SEL=0/1/2 for Current/Default/Saved, with scope.</p>
</section>
<section class="qa-section" id="q-195-s-02" data-answer-section="2"><h3><span>2.</span> State changes and recovery</h3>
<span class="qa-anchor" id="q-195-a-04"></span><p>Successful SV=1 updates Saved; SV=0 changes Current only. Non-saveable features follow explicit persistence rules.</p>
<span class="qa-anchor" id="q-195-a-05"></span><p>Snapshot values before reset, recover Admin access, reread settings and then validate resulting behavior.</p>
<span class="qa-anchor" id="q-195-a-06"></span><p>Current matches the required restored value, not necessarily the last pre-reset SV=0 setting.</p>
</section>
<section class="qa-section" id="q-195-s-03" data-answer-section="3"><h3><span>3.</span> Verify retention and recovery</h3>
<span class="qa-anchor" id="q-195-a-07"></span><p>Unsupported saving follows the specified Feature Not Saveable handling; a failed Set does not establish saved state.</p>
<span class="qa-anchor" id="q-195-a-16"></span><p>Restoring feature defaults does not imply clearing temperature or lifetime counters.</p>
<span class="qa-anchor" id="q-195-a-17"></span><p>First inspect SV, the actual CQE and reset coverage.</p>
</section>
</div>
<span class="qa-anchor" id="q-195-a-08"></span><span class="qa-anchor" id="q-195-a-09"></span><span class="qa-anchor" id="q-195-a-10"></span><span class="qa-anchor" id="q-195-a-11"></span><span class="qa-anchor" id="q-195-a-12"></span><span class="qa-anchor" id="q-195-a-13"></span><span class="qa-anchor" id="q-195-a-14"></span><span class="qa-anchor" id="q-195-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/features/en/#q-055">Q55</a> · <a href="/nvme/question-bank/features/en/#q-062">Q62</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-196" data-question="196" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-196">Q196</a> What do SMART Critical Warning bits mean?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-196-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-196-a-01">Critical Warning reports current spare, thermal, reliability and read-only concerns; it is not a permanently latched history.</p><div class="qa-sections">
<section class="qa-section" id="q-196-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-196-a-02"></span><p>Bits are independent and may differ from their state when an earlier AER occurred.</p>
<span class="qa-anchor" id="q-196-a-03"></span><p>Read LID 02h and check the AEC SHCW enable mask and applicable hardware capabilities.</p>
</section>
<section class="qa-section" id="q-196-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-196-a-04"></span><p>Bits 0–6 indicate low spare, temperature condition, degraded reliability, all-media read-only, volatile backup failure, PMR read-only/unreliable and indeterminate personality state; bit 7 is reserved.</p>
<span class="qa-anchor" id="q-196-a-05"></span><p>Decode asserted bits and related fields; bit 1 may indicate either over- or under-temperature.</p>
<span class="qa-anchor" id="q-196-a-06"></span><p>A successful read returns the current combination; multiple warnings are valid.</p>
</section>
<section class="qa-section" id="q-196-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-196-a-07"></span><p>Namespace Write Protection shall not set AMRO; an inapplicable backup bit is not failure evidence.</p>
<span class="qa-anchor" id="q-196-a-16"></span><p>Correlate warning type, values and timing rather than requiring later CW to reproduce the event snapshot.</p>
</section>
</div>
<span class="qa-anchor" id="q-196-a-17"></span><span class="qa-anchor" id="q-196-a-08"></span><span class="qa-anchor" id="q-196-a-09"></span><span class="qa-anchor" id="q-196-a-10"></span><span class="qa-anchor" id="q-196-a-11"></span><span class="qa-anchor" id="q-196-a-12"></span><span class="qa-anchor" id="q-196-a-13"></span><span class="qa-anchor" id="q-196-a-14"></span><span class="qa-anchor" id="q-196-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-197" data-question="197" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-197">Q197</a> How are spare capacity and percentage used interpreted?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-197-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-197-a-01">These answer remaining spare, warning threshold and estimated life consumed, not one common percentage formula.</p><div class="qa-sections">
<section class="qa-section" id="q-197-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-197-a-02"></span><p>SMART health scope is not free filesystem space in a namespace.</p>
<span class="qa-anchor" id="q-197-a-03"></span><p>Read AVSP, AVSPT, PUSED and CW.ASCBT; use Endurance Group logs for group-level health.</p>
</section>
<section class="qa-section" id="q-197-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-197-a-04"></span><p>Spare and threshold range from 0–100%; the warning uses strict less-than. PUSED is a vendor estimate; 100 is not proof of failure, values may exceed 100 and values above 254 encode as 255.</p>
<span class="qa-anchor" id="q-197-a-05"></span><p>Hypothetical spare 8 with threshold 10 is low spare, while PUSED=105 indicates estimated endurance consumed beyond 100%.</p>
<span class="qa-anchor" id="q-197-a-06"></span><p>PUSED is updated once per power-on hour outside sleep, not after every Write.</p>
</section>
<section class="qa-section" id="q-197-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-197-a-07"></span><p>PUSED above 100 is legal; equality does not satisfy a below-threshold condition.</p>
<span class="qa-anchor" id="q-197-a-16"></span><p>Compare the warning with AVSP; do not derive spare directly from PUSED.</p>
</section>
</div>
<span class="qa-anchor" id="q-197-a-17"></span><span class="qa-anchor" id="q-197-a-08"></span><span class="qa-anchor" id="q-197-a-09"></span><span class="qa-anchor" id="q-197-a-10"></span><span class="qa-anchor" id="q-197-a-11"></span><span class="qa-anchor" id="q-197-a-12"></span><span class="qa-anchor" id="q-197-a-13"></span><span class="qa-anchor" id="q-197-a-14"></span><span class="qa-anchor" id="q-197-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-198" data-question="198" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-198">Q198</a> How do SMART workload and uptime counters accumulate?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-198-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-198-a-01">These counters measure different workload and uptime quantities; units precede comparison.</p><div class="qa-sections">
<section class="qa-section" id="q-198-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-198-a-02"></span><p>Use SMART scope; overlapping queue activity is not added repeatedly to busy time.</p>
<span class="qa-anchor" id="q-198-a-03"></span><p>Read data units, host command counts, busy time, power cycles and power-on hours with timestamps.</p>
</section>
<section class="qa-section" id="q-198-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-198-a-04"></span><p>Data units count thousands of 512-byte units rounded up; zero means not reported. Busy time counts minutes with outstanding I/O from submission doorbell to CQE posting, not host consumption.</p>
<span class="qa-anchor" id="q-198-a-05"></span><p>Difference two snapshots, convert units and apply command-set classifications for completed reads/user-data-out; POH may exclude non-operational states.</p>
<span class="qa-anchor" id="q-198-a-06"></span><p>A delta of two data units reflects 512000-byte quantization; a small operation need not immediately change the rounded value.</p>
</section>
<section class="qa-section" id="q-198-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-198-a-07"></span><p>Application request count need not equal NVMe command count because of merging, retries and classification.</p>
<span class="qa-anchor" id="q-198-a-16"></span><p>Compare actual completed commands and units rather than only file size or wall-clock time.</p>
</section>
</div>
<span class="qa-anchor" id="q-198-a-17"></span><span class="qa-anchor" id="q-198-a-08"></span><span class="qa-anchor" id="q-198-a-09"></span><span class="qa-anchor" id="q-198-a-10"></span><span class="qa-anchor" id="q-198-a-11"></span><span class="qa-anchor" id="q-198-a-12"></span><span class="qa-anchor" id="q-198-a-13"></span><span class="qa-anchor" id="q-198-a-14"></span><span class="qa-anchor" id="q-198-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-199" data-question="199" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-199">Q199</a> How do unexpected power-loss and error counters accumulate?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-199-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-199-a-01">These count power-loss conditions, unrecovered integrity errors and generated error entries separately.</p><div class="qa-sections">
<section class="qa-section" id="q-199-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-199-a-02"></span><p>They are lifetime counters, not current log occupancy.</p>
<span class="qa-anchor" id="q-199-a-03"></span><p>Read UPL, MDIE and NEILE alongside pre-loss SHST and any OOB media activity.</p>
</section>
<section class="qa-section" id="q-199-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-199-a-04"></span><p>Base 2.4 calls the former Unsafe Shutdowns field Unexpected Power Losses. It increments for main-power loss without SHST=10b or with media still active under the specified OOB Ignore Shutdown condition.</p>
<span class="qa-anchor" id="q-199-a-05"></span><p>Establish actual main-power loss and state; separately correlate unrecovered errors with MDIE and generated entries with NEILE.</p>
<span class="qa-anchor" id="q-199-a-06"></span><p>Reset without power loss does not increase UPL; completed abrupt shutdown does not alone require an increment.</p>
</section>
<section class="qa-section" id="q-199-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-199-a-07"></span><p>One command failure need not increase both counters; inclusion of Write Uncorrectable-induced errors in MDIE is implementation-permitted.</p>
<span class="qa-anchor" id="q-199-a-16"></span><p>Entry overwrite or recommended clearing after reset does not reduce lifetime NEILE.</p>
</section>
</div>
<span class="qa-anchor" id="q-199-a-17"></span><span class="qa-anchor" id="q-199-a-08"></span><span class="qa-anchor" id="q-199-a-09"></span><span class="qa-anchor" id="q-199-a-10"></span><span class="qa-anchor" id="q-199-a-11"></span><span class="qa-anchor" id="q-199-a-12"></span><span class="qa-anchor" id="q-199-a-13"></span><span class="qa-anchor" id="q-199-a-14"></span><span class="qa-anchor" id="q-199-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-200" data-question="200" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-200">Q200</a> How are warning and critical temperature times counted?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-200-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-200-a-01">These accumulate time in warning/critical temperature ranges, not HCTM transitions.</p><div class="qa-sections">
<section class="qa-section" id="q-200-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-200-a-02"></span><p>They use operational-state composite temperature against WCTEMP/CCTEMP in minutes.</p>
<span class="qa-anchor" id="q-200-a-03"></span><p>Read WCTEMP/CCTEMP and SMART WCTT/CCTT, with applicable hysteresis configuration.</p>
</section>
<section class="qa-section" id="q-200-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-200-a-04"></span><p>WCTT covers WCTEMP≤temperature&lt;CCTEMP; CCTT covers temperature≥CCTEMP, with zero-report rules for unimplemented thresholds.</p>
<span class="qa-anchor" id="q-200-a-05"></span><p>Determine the duration in each operational temperature range rather than turning one hot sample into a full minute.</p>
<span class="qa-anchor" id="q-200-a-06"></span><p>For two hypothetical minutes in the critical range, inspect CCTT rather than demanding the same duration in the warning-only range.</p>
</section>
<section class="qa-section" id="q-200-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-200-a-07"></span><p>WCTT is zero if WCTEMP or CCTEMP is zero; CCTT is zero if CCTEMP is zero. Zero does not universally prove no overheating.</p>
<span class="qa-anchor" id="q-200-a-16"></span><p>Keep HCTM seconds separate because its thresholds, units and meaning differ.</p>
</section>
</div>
<span class="qa-anchor" id="q-200-a-17"></span><span class="qa-anchor" id="q-200-a-08"></span><span class="qa-anchor" id="q-200-a-09"></span><span class="qa-anchor" id="q-200-a-10"></span><span class="qa-anchor" id="q-200-a-11"></span><span class="qa-anchor" id="q-200-a-12"></span><span class="qa-anchor" id="q-200-a-13"></span><span class="qa-anchor" id="q-200-a-14"></span><span class="qa-anchor" id="q-200-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-201" data-question="201" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-201">Q201</a> How do sensor temperatures relate to Composite Temperature?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-201-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-201-a-01">Sensors observe different locations; Composite Temperature need not equal their maximum, minimum or average.</p><div class="qa-sections">
<section class="qa-section" id="q-201-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-201-a-02"></span><p>Locations and composite computation are implementation-specific.</p>
<span class="qa-anchor" id="q-201-a-03"></span><p>Read CTEMP and TSEN1–TSEN8 and the device’s sensor mapping.</p>
</section>
<section class="qa-section" id="q-201-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-201-a-04"></span><p>Values are Kelvin; a zero TSEN means unimplemented, not a valid 0 K measurement.</p>
<span class="qa-anchor" id="q-201-a-05"></span><p>Remove unimplemented fields before conversion; 300 K is about 26.85°C. Pair thresholds with their selected sensors.</p>
<span class="qa-anchor" id="q-201-a-06"></span><p>Different returned temperatures are valid and do not themselves imply corruption.</p>
</section>
<section class="qa-section" id="q-201-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-201-a-07"></span><p>Not every TSEN must be implemented, and the composite need not be an average.</p>
<span class="qa-anchor" id="q-201-a-16"></span><p>Correlate warnings, selected sensor and that sensor’s reading.</p>
</section>
</div>
<span class="qa-anchor" id="q-201-a-17"></span><span class="qa-anchor" id="q-201-a-08"></span><span class="qa-anchor" id="q-201-a-09"></span><span class="qa-anchor" id="q-201-a-10"></span><span class="qa-anchor" id="q-201-a-11"></span><span class="qa-anchor" id="q-201-a-12"></span><span class="qa-anchor" id="q-201-a-13"></span><span class="qa-anchor" id="q-201-a-14"></span><span class="qa-anchor" id="q-201-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-202" data-question="202" data-answer-kind="events"><h2><a class="qa-qid" href="#q-202">Q202</a> Which health changes generate asynchronous events?</h2>
<p class="qa-prompt">Establish the event condition, then distinguish notification, acknowledgment and recording.</p>
<details class="qa-answer" id="q-202-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-202-a-01">Health notifications reduce polling but remain subject to support, enablement and masking.</p><div class="qa-sections">
<section class="qa-section" id="q-202-s-01" data-answer-section="1"><h3><span>1.</span> When the event exists and who observes it</h3>
<span class="qa-anchor" id="q-202-a-02"></span><p>SMART/Health events report defined warnings, not every temperature or counter change.</p>
<span class="qa-anchor" id="q-202-a-03"></span><p>Inspect SHCW, CW, outstanding AERs and relevant thresholds.</p>
<span class="qa-anchor" id="q-202-a-04"></span><p>Event type/information identify the condition; follow the returned LID to the associated health data.</p>
</section>
<section class="qa-section" id="q-202-s-02" data-answer-section="2"><h3><span>2.</span> Notification, reading and acknowledgment</h3>
<span class="qa-anchor" id="q-202-a-05"></span><p>Post requests, enable desired notices, preserve event CQEs, read/acknowledge with RAE and replenish requests.</p>
<span class="qa-anchor" id="q-202-a-06"></span><p>Eligible events can complete a request; a subsequently cleared CW does not invalidate an earlier event.</p>
</section>
<section class="qa-section" id="q-202-s-03" data-answer-section="3"><h3><span>3.</span> Evaluate missing notifications or records</h3>
<span class="qa-anchor" id="q-202-a-07"></span><p>Missing completion requires checking enablement, masking and available requests before alleging omission.</p>
<span class="qa-anchor" id="q-202-a-16"></span><p>Compare event-time settings and conditions, not only a later snapshot.</p>
<span class="qa-anchor" id="q-202-a-17"></span><p>First verify the relevant SHCW bit and acknowledgment of the previous masked event.</p>
</section>
<section class="qa-section" id="q-202-s-04" data-answer-section="4"><h3><span>4.</span> Asynchronous Event notification conditions</h3>
<span class="qa-anchor" id="q-202-a-09"></span><p>This question concerns SMART/Health AERs: evaluate conditions, SHCW, masking and requests together. Ordinary counter increments do not require events.</p>
</section>
</div>
<span class="qa-anchor" id="q-202-a-08"></span><span class="qa-anchor" id="q-202-a-10"></span><span class="qa-anchor" id="q-202-a-11"></span><span class="qa-anchor" id="q-202-a-12"></span><span class="qa-anchor" id="q-202-a-13"></span><span class="qa-anchor" id="q-202-a-14"></span><span class="qa-anchor" id="q-202-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-203" data-question="203" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-203">Q203</a> How is SMART data scope determined?</h2>
<p class="qa-prompt">Choose the interface and target, then identify the returned field that supports your conclusion.</p>
<details class="qa-answer" id="q-203-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-203-a-01">Scope identifies what the health values describe and prevents mistaking aggregate data for per-namespace health.</p><div class="qa-sections">
<section class="qa-section" id="q-203-s-01" data-answer-section="1"><h3><span>1.</span> Select the target and information</h3>
<span class="qa-anchor" id="q-203-a-02"></span><p>Base 2.4 SMART/Health does not provide namespace-specific information; acceptance of different NSIDs does not create per-namespace data.</p>
<span class="qa-anchor" id="q-203-a-03"></span><p>Use this revision’s SMART and Get Log rules; use the separate log for Endurance Group health.</p>
<span class="qa-anchor" id="q-203-a-04"></span><p>Encode NSID/LID correctly while interpreting each field under its defined scope.</p>
</section>
<section class="qa-section" id="q-203-s-02" data-answer-section="2"><h3><span>2.</span> Query sequence and interpretation</h3>
<span class="qa-anchor" id="q-203-a-05"></span><p>Record controller/NSID and compare responses; identical data across NSIDs is expected under this revision’s definition.</p>
<span class="qa-anchor" id="q-203-a-06"></span><p>Successful reads do not allocate endurance consumption to individual namespaces.</p>
</section>
<section class="qa-section" id="q-203-s-03" data-answer-section="3"><h3><span>3.</span> Handle missing or inconsistent evidence</h3>
<span class="qa-anchor" id="q-203-a-07"></span><p>Do not import older namespace-specific assumptions and demand distinct counters.</p>
<span class="qa-anchor" id="q-203-a-16"></span><p>Compare revision, log definition and response rather than old tool labels.</p>
<span class="qa-anchor" id="q-203-a-17"></span><p>First distinguish accepted NSIDs from per-namespace accounting capability.</p>
</section>
</div>
<span class="qa-anchor" id="q-203-a-08"></span><span class="qa-anchor" id="q-203-a-09"></span><span class="qa-anchor" id="q-203-a-10"></span><span class="qa-anchor" id="q-203-a-11"></span><span class="qa-anchor" id="q-203-a-12"></span><span class="qa-anchor" id="q-203-a-13"></span><span class="qa-anchor" id="q-203-a-14"></span><span class="qa-anchor" id="q-203-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-204" data-question="204" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-204">Q204</a> How are SMART, operations, errors and PEL cross-checked?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-204-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-204-a-01">Cross-check meaningful relationships rather than demanding one increment in every source per operation.</p><div class="qa-sections">
<section class="qa-section" id="q-204-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-204-a-02"></span><p>Fix controller, time interval and each source’s scope before comparing.</p>
<span class="qa-anchor" id="q-204-a-03"></span><p>Preserve capabilities, before/after SMART, CQEs, errors and an available PEL context.</p>
<span class="qa-anchor" id="q-204-a-04"></span><p>Correlate command IDs, Error Count and PEL event data while interpreting SMART units and accumulation conditions.</p>
</section>
<section class="qa-section" id="q-204-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-204-a-17"></span><p>First verify that the operation actually triggers each expected field change.</p>
<span class="qa-anchor" id="q-204-a-05"></span><p>Predict affected evidence, isolate a scenario and compare each expected relationship.</p>
</section>
<section class="qa-section" id="q-204-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-204-a-06"></span><p>A normal Read may increase read/data counters without requiring an error entry or per-command PEL record.</p>
<span class="qa-anchor" id="q-204-a-07"></span><p>Absence of optional evidence is not a violation; missing advertised More information requires checking overwrite, timing and logging rules.</p>
<span class="qa-anchor" id="q-204-a-16"></span><p>Separate compliance, established violation and insufficient evidence.</p>
</section>
</div>
<span class="qa-anchor" id="q-204-a-08"></span><span class="qa-anchor" id="q-204-a-09"></span><span class="qa-anchor" id="q-204-a-10"></span><span class="qa-anchor" id="q-204-a-11"></span><span class="qa-anchor" id="q-204-a-12"></span><span class="qa-anchor" id="q-204-a-13"></span><span class="qa-anchor" id="q-204-a-14"></span><span class="qa-anchor" id="q-204-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-smart">Base 2.4 §5.2.13.1.3</a> · <a href="#ref-powerdetail">Base 2.4 §8.1.19.1–8.1.19.5</a> · <a href="#ref-psd">Base 2.4 §5.2.14.2.1 (Power State Descriptor)</a> · <a href="#ref-power">Base 2.4 §5.2.30.1.2, 5.2.30.1.7</a> · <a href="#ref-thermal">Base 2.4 §5.2.30.1.10</a> · <a href="#ref-aec">Base 2.4 §5.2.30.1.6</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>

<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>Printed pages 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>Printed pages 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-smart"><strong>Base 2.4 · §5.2.13.1.3</strong><br>Printed pages 220–225 · PDF 246–251 · Figure 213–214</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-psd"><strong>Base 2.4 · §5.2.14.2.1 (Power State Descriptor)</strong><br>Printed pages 384–387 · PDF 410–413 · Figure 340–341</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>Printed pages 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-power"><strong>Base 2.4 · §5.2.30.1.2, 5.2.30.1.7</strong><br>Printed pages 460–462, 468–469 · PDF 486–488, 494–495 · Figure 468–469, 475–478</li>
<li id="ref-aec"><strong>Base 2.4 · §5.2.30.1.6</strong><br>Printed pages 466–468 · PDF 492–494 · Figure 474</li>
<li id="ref-thermal"><strong>Base 2.4 · §5.2.30.1.10</strong><br>Printed pages 471–472 · PDF 497–498 · Figure 482</li>
<li id="ref-powerdetail"><strong>Base 2.4 · §8.1.19.1–8.1.19.5</strong><br>Printed pages 666–671 · PDF 692–697 · Figure 738–741</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/health/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/health.html">Chinese tutorial HTML</a></nav>
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
