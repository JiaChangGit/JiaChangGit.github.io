---
layout: post
title: "NVMe Self-Study Bank: Interrupt configuration and completion delivery"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/interrupts/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/interrupts/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/interrupts.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q286–Q296</p><h1>Interrupt configuration and completion delivery</h1><p class="qr-intro">Establish CQE posting before diagnosing routing, aggregation, masks and host consumption.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Four controls answer different questions</h2><p class="qa-takeaway">FID 09h.CD disables coalescing, not interrupts.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Control</th><th scope="col">Interface</th><th scope="col">Meaning</th></tr></thead><tbody><tr><td>CQ routing</td><td>IV/IEN</td><td>Vector and notification enable</td></tr><tr><td>Aggregation</td><td>TIME/THR</td><td>Recommended delay/count</td></tr><tr><td>Per-vector override</td><td>CD</td><td>Disable aggregation for this vector</td></tr><tr><td>Masking</td><td>Mode-specific masks</td><td>Allow delivery</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>Shared masked CQs can accumulate entries; one later interrupt can cover many completions.</p>
<p class="qa-citations">Sources: <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-286">Q286 · How does a CQ select an interrupt vector?</a></li>
<li><a href="#q-287">Q287 · How do shared and dedicated CQ vectors differ?</a></li>
<li><a href="#q-288">Q288 · How do coalescing threshold and time work?</a></li>
<li><a href="#q-289">Q289 · How is interrupt coalescing disabled?</a></li>
<li><a href="#q-290">Q290 · Does FID 09h mask interrupts, and where are actual masks configured?</a></li>
<li><a href="#q-291">Q291 · Can completions be posted while a vector is masked?</a></li>
<li><a href="#q-292">Q292 · How are accumulated completions handled after unmasking?</a></li>
<li><a href="#q-293">Q293 · Can an in-use vector be reconfigured?</a></li>
<li><a href="#q-294">Q294 · How are interrupts restored after reset?</a></li>
<li><a href="#q-295">Q295 · How are interrupt resources reclaimed after queue deletion?</a></li>
<li><a href="#q-296">Q296 · How are interrupt settings, CQ state and completions cross-checked?</a></li>
</ol></section>
<article class="qa-question" id="q-286" data-question="286" data-answer-kind="process"><h2><a class="qa-qid" href="#q-286">Q286</a> How does a CQ select an interrupt vector?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-286-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-286-a-01">CQ identity selects completion storage, while IV selects notification; the numbers need not match.</p><div class="qa-sections">
<section class="qa-section" id="q-286-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-286-a-02"></span><p>I/O CQs own vector associations; SQs use them through CQID.</p>
<span class="qa-anchor" id="q-286-a-03"></span><p>Establish interrupt mode and allocated vectors before CQ creation.</p>
<span class="qa-anchor" id="q-286-a-04"></span><p>IV selects the vector, IEN enables CQ interrupts and PC selects memory contiguity.</p>
</section>
<section class="qa-section" id="q-286-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-286-a-05"></span><p>Allocate vectors, create CQ and SQ, then verify with I/O.</p>
<span class="qa-anchor" id="q-286-a-06"></span><p>CQ5 can use IV2; an SQ7 completion goes to CQ5 and is identified by SQID/CID after IV2 notification.</p>
</section>
<section class="qa-section" id="q-286-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-286-a-07"></span><p>Invalid vector selection maps to 1/08h, independently of QID validity.</p>
<span class="qa-anchor" id="q-286-a-16"></span><p>Correlate successful creation, IV/IEN and the host handler’s CQ list.</p>
</section>
</div>
<span class="qa-anchor" id="q-286-a-17"></span><span class="qa-anchor" id="q-286-a-08"></span><span class="qa-anchor" id="q-286-a-09"></span><span class="qa-anchor" id="q-286-a-10"></span><span class="qa-anchor" id="q-286-a-11"></span><span class="qa-anchor" id="q-286-a-12"></span><span class="qa-anchor" id="q-286-a-13"></span><span class="qa-anchor" id="q-286-a-14"></span><span class="qa-anchor" id="q-286-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-287" data-question="287" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-287">Q287</a> How do shared and dedicated CQ vectors differ?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-287-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-287-a-01">Sharing saves vectors but requires scanning more CQs; dedicated vectors simplify distribution.</p><div class="qa-sections">
<section class="qa-section" id="q-287-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-287-a-02"></span><p>Aggregation thresholds apply per vector and may cover several CQs.</p>
<span class="qa-anchor" id="q-287-a-04"></span><p>CQEs retain command identity; the interrupt does not enumerate completed commands.</p>
</section>
<section class="qa-section" id="q-287-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-287-a-03"></span><p>Inspect available vectors and CQ IV/IEN associations.</p>
<span class="qa-anchor" id="q-287-a-05"></span><p>Maintain vector-to-CQ membership, consume valid entries and acknowledge each CQ.</p>
<span class="qa-anchor" id="q-287-a-06"></span><p>One IV3 interrupt can cover multiple completions in two CQs.</p>
</section>
<section class="qa-section" id="q-287-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-287-a-07"></span><p>Interrupt and CQE counts need not match under sharing and aggregation.</p>
<span class="qa-anchor" id="q-287-a-16"></span><p>Measure per-CQ posting and consumption, not only shared-vector counts.</p>
</section>
</div>
<span class="qa-anchor" id="q-287-a-17"></span><span class="qa-anchor" id="q-287-a-08"></span><span class="qa-anchor" id="q-287-a-09"></span><span class="qa-anchor" id="q-287-a-10"></span><span class="qa-anchor" id="q-287-a-11"></span><span class="qa-anchor" id="q-287-a-12"></span><span class="qa-anchor" id="q-287-a-13"></span><span class="qa-anchor" id="q-287-a-14"></span><span class="qa-anchor" id="q-287-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-288" data-question="288" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-288">Q288</a> How do coalescing threshold and time work?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-288-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-288-a-01">Aggregation reduces host overhead at possible notification-latency cost without requiring delayed CQE posting.</p><div class="qa-sections">
<section class="qa-section" id="q-288-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-288-a-02"></span><p>FID 08h applies to I/O queues, not Admin CQ.</p>
<span class="qa-anchor" id="q-288-a-03"></span><p>Read/configure TIME/THR and check each vector’s coalescing-disable bit.</p>
</section>
<section class="qa-section" id="q-288-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-288-a-04"></span><p>TIME is in 100 µs units and THR is a zero-based recommended completion count.</p>
<span class="qa-anchor" id="q-288-a-05"></span><p>Establish nonzero settings and CD0 before comparing notification timing under a fixed workload.</p>
<span class="qa-anchor" id="q-288-a-06"></span><p>TIME5/THR7 recommends 500 µs and 8 completions, not waiting for both exact values.</p>
</section>
<section class="qa-section" id="q-288-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-288-a-07"></span><p>PCIe permits implementation-specific aggregation, including none; deviation from recommended timing alone is not a violation.</p>
<span class="qa-anchor" id="q-288-a-16"></span><p>CQ-head updates may restart aggregation and ongoing servicing can continually postpone another notification.</p>
</section>
</div>
<span class="qa-anchor" id="q-288-a-17"></span><span class="qa-anchor" id="q-288-a-08"></span><span class="qa-anchor" id="q-288-a-09"></span><span class="qa-anchor" id="q-288-a-10"></span><span class="qa-anchor" id="q-288-a-11"></span><span class="qa-anchor" id="q-288-a-12"></span><span class="qa-anchor" id="q-288-a-13"></span><span class="qa-anchor" id="q-288-a-14"></span><span class="qa-anchor" id="q-288-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-289" data-question="289" data-answer-kind="process"><h2><a class="qa-qid" href="#q-289">Q289</a> How is interrupt coalescing disabled?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-289-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-289-a-01">Disabling aggregation removes coalescing, not interrupts.</p><div class="qa-sections">
<section class="qa-section" id="q-289-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-289-a-02"></span><p>FID 08h controls I/O aggregation globally, while FID 09h.CD disables it per vector.</p>
<span class="qa-anchor" id="q-289-a-03"></span><p>Read aggregation settings, vector overrides and CQ interrupt enable.</p>
<span class="qa-anchor" id="q-289-a-04"></span><p>Either zero TIME or zero THR implicitly disables aggregation; CD1 prevents aggregation on that vector.</p>
</section>
<section class="qa-section" id="q-289-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-289-a-05"></span><p>Use FID 08h globally, or associate an I/O CQ before setting a per-vector override.</p>
<span class="qa-anchor" id="q-289-a-06"></span><p>Verify readback and apply delivery/mask rules rather than the previous aggregation threshold.</p>
</section>
<section class="qa-section" id="q-289-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-289-a-07"></span><p>THR0 has an explicit disable meaning despite ordinary zero-based count interpretation.</p>
<span class="qa-anchor" id="q-289-a-16"></span><p>No aggregation does not require one separate interrupt per CQE.</p>
</section>
</div>
<span class="qa-anchor" id="q-289-a-17"></span><span class="qa-anchor" id="q-289-a-08"></span><span class="qa-anchor" id="q-289-a-09"></span><span class="qa-anchor" id="q-289-a-10"></span><span class="qa-anchor" id="q-289-a-11"></span><span class="qa-anchor" id="q-289-a-12"></span><span class="qa-anchor" id="q-289-a-13"></span><span class="qa-anchor" id="q-289-a-14"></span><span class="qa-anchor" id="q-289-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-290" data-question="290" data-answer-kind="process"><h2><a class="qa-qid" href="#q-290">Q290</a> Does FID 09h mask interrupts, and where are actual masks configured?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-290-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-290-a-01">Interrupt Vector Configuration (FID 09h) does not mask interrupts. Its CD bit controls whether that vector uses interrupt coalescing; inspect the active interrupt mechanism for the actual mask.</p><div class="qa-sections">
<section class="qa-section" id="q-290-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-290-a-02"></span><p>A mask blocks delivery for all CQs sharing that vector.</p>
<span class="qa-anchor" id="q-290-a-03"></span><p>Select the masking interface after establishing the active interrupt mode.</p>
<span class="qa-anchor" id="q-290-a-04"></span><p>INTMS write-one sets and INTMC write-one clears pin/MSI masks; MSI-X uses function and table-vector masks.</p>
</section>
<section class="qa-section" id="q-290-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-290-a-05"></span><p>Preserve state, mask, service/acknowledge CQs, unmask and check remaining work.</p>
<span class="qa-anchor" id="q-290-a-06"></span><p>INTMC requires writing one to clear a mask; zero has no effect.</p>
</section>
<section class="qa-section" id="q-290-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-290-a-07"></span><p>INTMS/INTMC access is prohibited and undefined under MSI-X, not a guaranteed NVMe status.</p>
<span class="qa-anchor" id="q-290-a-16"></span><p>FID 09h readback does not establish MSI-X mask state.</p>
</section>
<section class="qa-section" id="q-290-s-04" data-answer-section="4"><h3><span>4.</span> Whether CQE, DNR and More apply here</h3>
<span class="qa-anchor" id="q-290-a-08"></span><p>Mask register accesses have no NVMe CQE; only separate Get/Set Feature commands carry DNR/More.</p>
</section>
</div>
<span class="qa-anchor" id="q-290-a-17"></span><span class="qa-anchor" id="q-290-a-09"></span><span class="qa-anchor" id="q-290-a-10"></span><span class="qa-anchor" id="q-290-a-11"></span><span class="qa-anchor" id="q-290-a-12"></span><span class="qa-anchor" id="q-290-a-13"></span><span class="qa-anchor" id="q-290-a-14"></span><span class="qa-anchor" id="q-290-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-291" data-question="291" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-291">Q291</a> Can completions be posted while a vector is masked?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-291-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-291-a-01">Masking controls notification rather than command execution or CQ posting.</p><div class="qa-sections">
<section class="qa-section" id="q-291-s-01" data-answer-section="1"><h3><span>1.</span> Masking suppresses notification, not CQ progress</h3>
<span class="qa-anchor" id="q-291-a-02"></span><p>Associated CQs can accumulate completions until their capacity limits intervene.</p>
<span class="qa-anchor" id="q-291-a-04"></span><p>Normal CQE posting continues; MSI-X masks cause pending-interrupt indication.</p>
<span class="qa-anchor" id="q-291-a-06"></span><p>A new valid CQE without an interrupt can be normal while masked.</p>
</section>
<section class="qa-section" id="q-291-s-02" data-answer-section="2"><h3><span>2.</span> Observe completions and avoid a full CQ</h3>
<span class="qa-anchor" id="q-291-a-03"></span><p>Inspect masks, IEN, CQ position/phase and applicable MSI-X pending bits.</p>
<span class="qa-anchor" id="q-291-a-05"></span><p>Poll and consume valid CQEs, then update head to release space.</p>
<span class="qa-anchor" id="q-291-a-07"></span><p>CQ fullness is a capacity consequence of nonconsumption, not a direct masking rule.</p>
</section>
</div>
<span class="qa-anchor" id="q-291-a-16"></span><span class="qa-anchor" id="q-291-a-17"></span><span class="qa-anchor" id="q-291-a-08"></span><span class="qa-anchor" id="q-291-a-09"></span><span class="qa-anchor" id="q-291-a-10"></span><span class="qa-anchor" id="q-291-a-11"></span><span class="qa-anchor" id="q-291-a-12"></span><span class="qa-anchor" id="q-291-a-13"></span><span class="qa-anchor" id="q-291-a-14"></span><span class="qa-anchor" id="q-291-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-292" data-question="292" data-answer-kind="process"><h2><a class="qa-qid" href="#q-292">Q292</a> How are accumulated completions handled after unmasking?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-292-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-292-a-01">One pending interrupt can represent many completions whose results remain in CQs.</p><div class="qa-sections">
<section class="qa-section" id="q-292-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-292-a-02"></span><p>Service all relevant CQs sharing the vector.</p>
<span class="qa-anchor" id="q-292-a-03"></span><p>Check mode-specific masks/pending state and associated queues.</p>
<span class="qa-anchor" id="q-292-a-04"></span><p>Pending MSI-X delivery requires both mask layers clear.</p>
</section>
<section class="qa-section" id="q-292-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-292-a-05"></span><p>Unmask, process valid CQEs and acknowledge heads while handling arrival races.</p>
<span class="qa-anchor" id="q-292-a-06"></span><p>Ten accumulated completions need not cause ten replayed interrupts.</p>
</section>
<section class="qa-section" id="q-292-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-292-a-07"></span><p>INTM masking suppresses MSI pending assertion; MSI-X PBA semantics cannot be copied to it.</p>
<span class="qa-anchor" id="q-292-a-16"></span><p>Judge consumption completeness, not equality of interrupt and command counts.</p>
</section>
</div>
<span class="qa-anchor" id="q-292-a-17"></span><span class="qa-anchor" id="q-292-a-08"></span><span class="qa-anchor" id="q-292-a-09"></span><span class="qa-anchor" id="q-292-a-10"></span><span class="qa-anchor" id="q-292-a-11"></span><span class="qa-anchor" id="q-292-a-12"></span><span class="qa-anchor" id="q-292-a-13"></span><span class="qa-anchor" id="q-292-a-14"></span><span class="qa-anchor" id="q-292-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-293" data-question="293" data-answer-kind="process"><h2><a class="qa-qid" href="#q-293">Q293</a> Can an in-use vector be reconfigured?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-293-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-293-a-01">Distinguish coalescing changes, masking and reassignment of CQ association.</p><div class="qa-sections">
<section class="qa-section" id="q-293-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-293-a-02"></span><p>FID 09h changes aggregation for the selected vector and its associated CQs.</p>
<span class="qa-anchor" id="q-293-a-03"></span><p>FID 09h requires prior association with an existing I/O CQ.</p>
<span class="qa-anchor" id="q-293-a-04"></span><p>CD selects aggregation behavior, not reassignment of Create CQ.IV.</p>
</section>
<section class="qa-section" id="q-293-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-293-a-05"></span><p>Change/read back vector settings; recreate the queue association when a different IV is needed.</p>
<span class="qa-anchor" id="q-293-a-06"></span><p>An existing CQ is the feature’s prerequisite, not a prohibition on change.</p>
</section>
<section class="qa-section" id="q-293-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-293-a-07"></span><p>Invalid/unassociated IV should produce Invalid Field, preserving the recommendation strength.</p>
<span class="qa-anchor" id="q-293-a-16"></span><p>Preserve shared-CQ and mask state to isolate feature effects.</p>
</section>
</div>
<span class="qa-anchor" id="q-293-a-17"></span><span class="qa-anchor" id="q-293-a-08"></span><span class="qa-anchor" id="q-293-a-09"></span><span class="qa-anchor" id="q-293-a-10"></span><span class="qa-anchor" id="q-293-a-11"></span><span class="qa-anchor" id="q-293-a-12"></span><span class="qa-anchor" id="q-293-a-13"></span><span class="qa-anchor" id="q-293-a-14"></span><span class="qa-anchor" id="q-293-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-294" data-question="294" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-294">Q294</a> How are interrupts restored after reset?</h2>
<p class="qa-prompt">Name the reset or interruption, then assess settings, ongoing operations and data separately.</p>
<details class="qa-answer" id="q-294-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-294-a-01">Queue associations end with queue lifetime; PCIe mode/mask retention depends on the reset source.</p><div class="qa-sections">
<section class="qa-section" id="q-294-s-01" data-answer-section="1"><h3><span>1.</span> Identify the trigger and affected objects</h3>
<span class="qa-anchor" id="q-294-a-02"></span><p>One-controller reset differs from broader reset and does not justify reconfiguring unaffected controllers.</p>
<span class="qa-anchor" id="q-294-a-03"></span><p>Inspect controller state, interrupt mode and feature current values.</p>
</section>
<section class="qa-section" id="q-294-s-02" data-answer-section="2"><h3><span>2.</span> State changes and recovery</h3>
<span class="qa-anchor" id="q-294-a-04"></span><p>FID 08h resets to zero; default per-vector coalescing permission does not enable a disabled global aggregation policy.</p>
<span class="qa-anchor" id="q-294-a-05"></span><p>Recover Admin access, vectors and queues before configuring per-vector/global aggregation.</p>
<span class="qa-anchor" id="q-294-a-06"></span><p>New completions are consumed through the rebuilt path without importing stale CQEs.</p>
</section>
<section class="qa-section" id="q-294-s-03" data-answer-section="3"><h3><span>3.</span> Verify retention and recovery</h3>
<span class="qa-anchor" id="q-294-a-07"></span><p>Setting FID 09h before rebuilding its CQ can violate the association prerequisite.</p>
<span class="qa-anchor" id="q-294-a-16"></span><p>Mode changes may lose aggregation settings; CC.EN testing does not establish power-cycle behavior.</p>
<span class="qa-anchor" id="q-294-a-17"></span><p>First check reset type and successful new-CQ creation time.</p>
</section>
</div>
<span class="qa-anchor" id="q-294-a-08"></span><span class="qa-anchor" id="q-294-a-09"></span><span class="qa-anchor" id="q-294-a-10"></span><span class="qa-anchor" id="q-294-a-11"></span><span class="qa-anchor" id="q-294-a-12"></span><span class="qa-anchor" id="q-294-a-13"></span><span class="qa-anchor" id="q-294-a-14"></span><span class="qa-anchor" id="q-294-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-295" data-question="295" data-answer-kind="process"><h2><a class="qa-qid" href="#q-295">Q295</a> How are interrupt resources reclaimed after queue deletion?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-295-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-295-a-01">CQ deletion removes one completion destination, not the host-allocated PCIe vector itself.</p><div class="qa-sections">
<section class="qa-section" id="q-295-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-295-a-02"></span><p>Other CQs may still use the vector, requiring association-aware reclamation.</p>
<span class="qa-anchor" id="q-295-a-03"></span><p>Preserve SQ-to-CQ-to-IV dependencies and outstanding commands.</p>
<span class="qa-anchor" id="q-295-a-04"></span><p>Delete dependent SQs and wait, then delete CQ and retire its host handling state.</p>
</section>
<section class="qa-section" id="q-295-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-295-a-05"></span><p>Release the handler/vector only after checking remaining CQ users.</p>
<span class="qa-anchor" id="q-295-a-06"></span><p>Deleting CQ1 leaves IV3 serving CQ2 when both shared it.</p>
</section>
<section class="qa-section" id="q-295-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-295-a-07"></span><p>Referenced CQs cannot be deleted successfully, nor their memory reclaimed early.</p>
<span class="qa-anchor" id="q-295-a-16"></span><p>Correlate deletion completion, host membership and remaining notification paths.</p>
</section>
</div>
<span class="qa-anchor" id="q-295-a-17"></span><span class="qa-anchor" id="q-295-a-08"></span><span class="qa-anchor" id="q-295-a-09"></span><span class="qa-anchor" id="q-295-a-10"></span><span class="qa-anchor" id="q-295-a-11"></span><span class="qa-anchor" id="q-295-a-12"></span><span class="qa-anchor" id="q-295-a-13"></span><span class="qa-anchor" id="q-295-a-14"></span><span class="qa-anchor" id="q-295-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-296" data-question="296" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-296">Q296</a> How are interrupt settings, CQ state and completions cross-checked?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-296-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-296-a-01">Separating completion from notification distinguishes execution failures from delivery/consumption failures.</p><div class="qa-sections">
<section class="qa-section" id="q-296-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-296-a-02"></span><p>Follow a complete SQ-command-to-CQ-to-vector-to-handler path.</p>
<span class="qa-anchor" id="q-296-a-03"></span><p>Inspect routing, aggregation, masks and phase.</p>
<span class="qa-anchor" id="q-296-a-04"></span><p>Preserve submission, CQE posting, notification and head-update times separately.</p>
</section>
<section class="qa-section" id="q-296-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-296-a-17"></span><p>First inspect the command’s CQ position and phase.</p>
<span class="qa-anchor" id="q-296-a-05"></span><p>Establish a valid CQE, assess notification, then verify consumption and reclamation.</p>
</section>
<section class="qa-section" id="q-296-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-296-a-06"></span><p>A posted CQE consumed by polling while masked can be valid normal behavior.</p>
<span class="qa-anchor" id="q-296-a-07"></span><p>Resolve wrong phase/CQ or missing head updates before diagnosing a lost command from absent interrupts.</p>
<span class="qa-anchor" id="q-296-a-16"></span><p>Correlate settings and observations from the same test interval.</p>
</section>
</div>
<span class="qa-anchor" id="q-296-a-08"></span><span class="qa-anchor" id="q-296-a-09"></span><span class="qa-anchor" id="q-296-a-10"></span><span class="qa-anchor" id="q-296-a-11"></span><span class="qa-anchor" id="q-296-a-12"></span><span class="qa-anchor" id="q-296-a-13"></span><span class="qa-anchor" id="q-296-a-14"></span><span class="qa-anchor" id="q-296-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-interruptfull">PCIe Transport 1.4 §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</a> · <a href="#ref-interruptmask">Base 2.4 §3.1.4 (INTMS, INTMC)</a> · <a href="#ref-interruptfeature">Base 2.4 §5.2.30.2.1–5.2.30.2.2</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>

<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-interruptmask"><strong>Base 2.4 · §3.1.4 (INTMS, INTMC)</strong><br>Printed pages 59 · PDF 85 · Figure 39–40</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>Printed pages 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>Printed pages 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>Printed pages 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-interruptfeature"><strong>Base 2.4 · §5.2.30.2.1–5.2.30.2.2</strong><br>Printed pages 514–515 · PDF 540–541 · Figure 543–544</li>
<li id="ref-create"><strong>Base 2.4 · §5.3.1–5.3.2</strong><br>Printed pages 527–531 · PDF 553–557 · Figure 571–579</li>
<li id="ref-delete"><strong>Base 2.4 · §5.3.3–5.3.4</strong><br>Printed pages 531–532 · PDF 557–558 · Figure 580–583</li>
<li id="ref-interruptfull"><strong>PCIe Transport 1.4 · §3.5–3.5.2 (interrupt delivery and masks), 3.8.4</strong><br>Printed pages 13–16, 24–26 · PDF 13–16, 24–26 · Figure 9, 42–48</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/features/en/#figure-b543">Base 2.4 Figure 543 · Interrupt Coalescing – Command Dword 11</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/interrupts/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/interrupts.html">Chinese tutorial HTML</a></nav>
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
