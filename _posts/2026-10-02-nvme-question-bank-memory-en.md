---
layout: post
title: "NVMe Self-Study Bank: HMB, CMB and PMR"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/memory/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/memory/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/memory.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q223–Q236</p><h1>HMB, CMB and PMR</h1><p class="qr-intro">Compare location, ownership, lifetime and persistence rather than treating all memory facilities alike.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Location, ownership and persistence</h2><p class="qa-takeaway">Retained addressing is not retained content; CQE success alone does not establish PMR persistence.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Facility</th><th scope="col">Location/use</th><th scope="col">Lifetime/evidence</th></tr></thead><tbody><tr><td>HMB</td><td>Host-provided controller buffer</td><td>Reclaim after successful disable</td></tr><tr><td>CMB</td><td>Controller memory with advertised uses</td><td>Reinitialize under reset/CMSE rules</td></tr><tr><td>PMR</td><td>Function-provided persistent region</td><td>Check readiness, health and write barriers</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>HMB cannot be reused before disable; retained CMB addressing can still require content reinitialization; PMR has distinct persistence/health rules.</p>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-223">Q223 · What problems do HMB, CMB and PMR solve?</a></li>
<li><a href="#q-224">Q224 · How are HMB size and descriptor lists configured?</a></li>
<li><a href="#q-225">Q225 · How are malformed HMB allocations handled?</a></li>
<li><a href="#q-226">Q226 · How is HMB enabled, disabled and returned after reset?</a></li>
<li><a href="#q-227">Q227 · What happens if the host prematurely reclaims HMB?</a></li>
<li><a href="#q-228">Q228 · How are CMB location, size and uses discovered?</a></li>
<li><a href="#q-229">Q229 · Which queues, buffers and lists may reside in CMB?</a></li>
<li><a href="#q-230">Q230 · How are out-of-range or unsupported CMB uses handled?</a></li>
<li><a href="#q-231">Q231 · Do CMB configuration and contents survive reset?</a></li>
<li><a href="#q-232">Q232 · How is PMR discovered, enabled and made ready?</a></li>
<li><a href="#q-233">Q233 · What happens for not-ready or unhealthy PMR accesses?</a></li>
<li><a href="#q-234">Q234 · How is PMR safely disabled?</a></li>
<li><a href="#q-235">Q235 · How do resets and power cycles affect PMR state and data?</a></li>
<li><a href="#q-236">Q236 · How do host memory, HMB, CMB and PMR lifetimes compare?</a></li>
</ol></section>
<article class="qa-question" id="q-223" data-question="223" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-223">Q223</a> What problems do HMB, CMB and PMR solve?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-223-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-223-a-01">Their memory location, user and persistence guarantees differ; identify those before placement.</p><div class="qa-sections">
<section class="qa-section" id="q-223-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-223-a-02"></span><p>HMB is host memory dedicated to the controller; CMB is controller memory for supported uses; PMR is directly accessible persistent memory.</p>
<span class="qa-anchor" id="q-223-a-04"></span><p>HMB uses FID 0Dh descriptors; CMB uses address/control registers; PMR uses enable/readiness/health registers.</p>
</section>
<section class="qa-section" id="q-223-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-223-a-03"></span><p>Discover HMB through HMPRE, CMB through CAP/CMBSZ and PMR through CAP/PMRCAP.</p>
<span class="qa-anchor" id="q-223-a-05"></span><p>Match the need: firmware host RAM, supported CMB SQ placement or persistent PMR data with barriers and health checks.</p>
<span class="qa-anchor" id="q-223-a-06"></span><p>Success means supported use within its constraints, not universal placement freedom.</p>
</section>
<section class="qa-section" id="q-223-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-223-a-07"></span><p>Queue/list use in PMR is outside scope and may return Invalid Field; writable PMR is not interchangeable with CMB.</p>
<span class="qa-anchor" id="q-223-a-16"></span><p>Compare support, configuration, access method and restored contents, not only readable bytes.</p>
</section>
</div>
<span class="qa-anchor" id="q-223-a-17"></span><span class="qa-anchor" id="q-223-a-08"></span><span class="qa-anchor" id="q-223-a-09"></span><span class="qa-anchor" id="q-223-a-10"></span><span class="qa-anchor" id="q-223-a-11"></span><span class="qa-anchor" id="q-223-a-12"></span><span class="qa-anchor" id="q-223-a-13"></span><span class="qa-anchor" id="q-223-a-14"></span><span class="qa-anchor" id="q-223-a-15"></span>
<p class="qa-related">Related mechanisms: <a href="/nvme/question-bank/memory/en/#q-226">Q226</a> · <a href="/nvme/question-bank/memory/en/#q-231">Q231</a> · <a href="/nvme/question-bank/memory/en/#q-235">Q235</a></p>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-224" data-question="224" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-224">Q224</a> How are HMB size and descriptor lists configured?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-224-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-224-a-01">Multiple contiguous ranges form HMB; the descriptor list itself must be physically contiguous.</p><div class="qa-sections">
<section class="qa-section" id="q-224-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-224-a-02"></span><p>The allocation is exclusive to one controller and unavailable for ordinary host writes while enabled.</p>
<span class="qa-anchor" id="q-224-a-03"></span><p>Read preferred/minimum size, minimum descriptor size and maximum descriptors; size capability fields use 4 KiB units.</p>
</section>
<section class="qa-section" id="q-224-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-224-a-04"></span><p>HSIZE/BSIZE use CC.MPS pages; HMDLEC is a literal count, list address is 16-byte aligned and BADD page-aligned.</p>
<span class="qa-anchor" id="q-224-a-05"></span><p>Pin memory, construct descriptors, reconcile sizes and enable with EHM=1, awaiting success.</p>
<span class="qa-anchor" id="q-224-a-06"></span><p>Get verifies allocation; with hypothetical 8 KiB pages, HSIZE256 means 2 MiB.</p>
</section>
<section class="qa-section" id="q-224-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-224-a-07"></span><p>Zero HMDLEC requires Invalid Field; exceeding usable descriptor limits may reduce utilization rather than force rejection.</p>
<span class="qa-anchor" id="q-224-a-16"></span><p>Convert capability units before encoding HSIZE and verify readback.</p>
</section>
</div>
<span class="qa-anchor" id="q-224-a-17"></span><span class="qa-anchor" id="q-224-a-08"></span><span class="qa-anchor" id="q-224-a-09"></span><span class="qa-anchor" id="q-224-a-10"></span><span class="qa-anchor" id="q-224-a-11"></span><span class="qa-anchor" id="q-224-a-12"></span><span class="qa-anchor" id="q-224-a-13"></span><span class="qa-anchor" id="q-224-a-14"></span><span class="qa-anchor" id="q-224-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-225" data-question="225" data-answer-kind="error"><h2><a class="qa-qid" href="#q-225">Q225</a> How are malformed HMB allocations handled?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-225-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-225-a-01">Different fields have different rules; isolate one malformed condition at a time.</p><div class="qa-sections">
<section class="qa-section" id="q-225-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-225-a-02"></span><p>Check list structure, ranges and current enable state.</p>
<span class="qa-anchor" id="q-225-a-04"></span><p>Zero entry count is Invalid Field; zero-size descriptors are ignored. The list address low four bits are treated as zero without a required check.</p>
<span class="qa-anchor" id="q-225-a-07"></span><p>Re-enabling active HMB requires Command Sequence Error; unsupported HMNARE requires Invalid Field. Do not demand one status for every alignment defect.</p>
</section>
<section class="qa-section" id="q-225-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-225-a-03"></span><p>Check limits, HMBR, current EHM and submitted fields.</p>
<span class="qa-anchor" id="q-225-a-05"></span><p>Separate specified format errors from inaccessible-memory transfer failures.</p>
</section>
<section class="qa-section" id="q-225-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-225-a-06"></span><p>Valid allocation succeeds; out-of-limit allocation may be only partly used.</p>
<span class="qa-anchor" id="q-225-a-16"></span><p>Match each condition to its rule, preserving ignore versus reject semantics.</p>
<span class="qa-anchor" id="q-225-a-17"></span><p>First check whether multiple faults prevent a unique expected status.</p>
</section>
</div>
<span class="qa-anchor" id="q-225-a-08"></span><span class="qa-anchor" id="q-225-a-09"></span><span class="qa-anchor" id="q-225-a-10"></span><span class="qa-anchor" id="q-225-a-11"></span><span class="qa-anchor" id="q-225-a-12"></span><span class="qa-anchor" id="q-225-a-13"></span><span class="qa-anchor" id="q-225-a-14"></span><span class="qa-anchor" id="q-225-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-226" data-question="226" data-answer-kind="process"><h2><a class="qa-qid" href="#q-226">Q226</a> How is HMB enabled, disabled and returned after reset?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-226-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-226-a-01">Explicit ownership transitions establish when memory may be reclaimed.</p><div class="qa-sections">
<section class="qa-section" id="q-226-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-226-a-02"></span><p>EHM controls use; MR describes whether returned contents are unchanged.</p>
<span class="qa-anchor" id="q-226-a-03"></span><p>Read EHM/allocation rather than assuming pre-reset enablement persists.</p>
<span class="qa-anchor" id="q-226-a-04"></span><p>EHM0 ignores CDW12–15; MR1 requires identical size, list address/content and buffer contents.</p>
</section>
<section class="qa-section" id="q-226-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-226-a-05"></span>
<span class="qa-anchor" id="q-226-a-06"></span>
<span class="qa-anchor" id="q-226-a-16"></span>
<span class="qa-anchor" id="q-226-a-17"></span>
<figure class="qa-flow" id="q-226-flow"><figcaption>HMB ownership changes at disable completion</figcaption>
<p>Submitting a disable request does not yet end controller access. Wait for completion before reclaiming memory.</p><ol class="qa-flow-steps">
<li class="qa-flow-step"><strong>Enable succeeds → controller may use HMB</strong><p>Keep buffers, the descriptor list and mappings valid.</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>Request EHM=0 → await a successful CQE</strong><p>Do not modify or reclaim memory still in use before successful completion.</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>Disable succeeds → host may reclaim or reconfigure</strong><p>The controller must not access HMB until re-enabled. Disabling an already-disabled HMB succeeds without other action.</p></li>
<li class="qa-flow-branch"><strong>Separate case: provide the configuration after reset</strong><p>Reset is not required to disable HMB. After a reset, supply the retained or a new configuration; use MR=1 only when all return-memory conditions hold.</p></li>
</ol><p class="qa-flow-conclusion">Compare the last HMB access, disable completion and host reclamation on one timeline.</p></figure>
</section>
<section class="qa-section" id="q-226-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-226-a-07"></span><p>Re-enable while enabled is a sequence error; claiming MR1 after modification violates the return premise.</p>
</section>
</div>
<span class="qa-anchor" id="q-226-a-08"></span><span class="qa-anchor" id="q-226-a-09"></span><span class="qa-anchor" id="q-226-a-10"></span><span class="qa-anchor" id="q-226-a-11"></span><span class="qa-anchor" id="q-226-a-12"></span><span class="qa-anchor" id="q-226-a-13"></span><span class="qa-anchor" id="q-226-a-14"></span><span class="qa-anchor" id="q-226-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-227" data-question="227" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-227">Q227</a> What happens if the host prematurely reclaims HMB?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-227-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-227-a-01">It violates exclusive ownership and can expose or corrupt memory reassigned to another use.</p><div class="qa-sections">
<section class="qa-section" id="q-227-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-227-a-02"></span><p>Damage may reach unrelated host data in reassigned physical pages.</p>
<span class="qa-anchor" id="q-227-a-04"></span><p>Both descriptors and described ranges must remain intact; retaining only the list is insufficient.</p>
</section>
<section class="qa-section" id="q-227-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-227-a-03"></span><p>Check EHM, disable completion and allocation/mapping lifetime.</p>
<span class="qa-anchor" id="q-227-a-05"></span><p>Disable and await success before unmapping; failure recovery must end old accesses before reclamation.</p>
<span class="qa-anchor" id="q-227-a-06"></span><p>After a valid handoff the old allocation is no longer accessed.</p>
</section>
<section class="qa-section" id="q-227-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-227-a-07"></span><p>Host misuse has no guaranteed detection or fixed status and may corrupt data; error logging is not protection.</p>
<span class="qa-anchor" id="q-227-a-16"></span><p>Distinguish premature host reclamation from controller accesses after successful disable.</p>
</section>
</div>
<span class="qa-anchor" id="q-227-a-17"></span><span class="qa-anchor" id="q-227-a-08"></span><span class="qa-anchor" id="q-227-a-09"></span><span class="qa-anchor" id="q-227-a-10"></span><span class="qa-anchor" id="q-227-a-11"></span><span class="qa-anchor" id="q-227-a-12"></span><span class="qa-anchor" id="q-227-a-13"></span><span class="qa-anchor" id="q-227-a-14"></span><span class="qa-anchor" id="q-227-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-228" data-question="228" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-228">Q228</a> How are CMB location, size and uses discovered?</h2>
<p class="qa-prompt">Choose the interface and target, then identify the returned field that supports your conclusion.</p>
<details class="qa-answer" id="q-228-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-228-a-01">Discover both host access and controller interpretation of command addresses.</p><div class="qa-sections">
<section class="qa-section" id="q-228-s-01" data-answer-section="1"><h3><span>1.</span> Select the target and information</h3>
<span class="qa-anchor" id="q-228-a-02"></span><p>Its PCIe and controller address ranges may have different bases but matching offsets.</p>
<span class="qa-anchor" id="q-228-a-03"></span><p>Check CAP.CMBS, enable CRE and read location/size; zero values with CRE0 do not prove absence.</p>
<span class="qa-anchor" id="q-228-a-04"></span><p>BIR selects BAR, OFST locates the region and SZ×SZU determines size within BAR limits; support bits distinguish uses.</p>
</section>
<section class="qa-section" id="q-228-s-02" data-answer-section="2"><h3><span>2.</span> Query sequence and interpretation</h3>
<span class="qa-anchor" id="q-228-a-05"></span><p>Configure a nonconflicting CBA, enable CMSE, check CBAI and initialize contents.</p>
<span class="qa-anchor" id="q-228-a-06"></span><p>Both address views reach the same contents at matching offsets.</p>
</section>
<section class="qa-section" id="q-228-s-03" data-answer-section="3"><h3><span>3.</span> Handle missing or inconsistent evidence</h3>
<span class="qa-anchor" id="q-228-a-07"></span><p>Invalid CBA sets CBAI and prevents memory-space enablement; it is register state, not an Admin CQE.</p>
<span class="qa-anchor" id="q-228-a-16"></span><p>Cross-check address bounds, units and use flags, not just capability presence.</p>
<span class="qa-anchor" id="q-228-a-17"></span><p>First check confusion between BAR and configured controller addresses.</p>
</section>
</div>
<span class="qa-anchor" id="q-228-a-08"></span><span class="qa-anchor" id="q-228-a-09"></span><span class="qa-anchor" id="q-228-a-10"></span><span class="qa-anchor" id="q-228-a-11"></span><span class="qa-anchor" id="q-228-a-12"></span><span class="qa-anchor" id="q-228-a-13"></span><span class="qa-anchor" id="q-228-a-14"></span><span class="qa-anchor" id="q-228-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-229" data-question="229" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-229">Q229</a> Which queues, buffers and lists may reside in CMB?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-229-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-229-a-01">Independent capability bits govern placement; SQ support does not imply CQ/data support.</p><div class="qa-sections">
<section class="qa-section" id="q-229-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-229-a-02"></span><p>Restrictions apply to an entire queue, a command’s list or its data/metadata set.</p>
<span class="qa-anchor" id="q-229-a-04"></span><p>CQMMS0 prohibits mixed queue placement; CQPDS0 requires contiguous queues. LISTS and related bits govern pointer-list placement and dependencies.</p>
</section>
<section class="qa-section" id="q-229-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-229-a-03"></span><p>Inspect use flags and mixed-memory/discontiguous-list capabilities.</p>
<span class="qa-anchor" id="q-229-a-05"></span><p>Select the object capability, then validate its combined placement constraints before allocating.</p>
<span class="qa-anchor" id="q-229-a-06"></span><p>With hypothetical SQS1/CQS0, an SQ may use CMB while its CQ remains in host memory.</p>
</section>
<section class="qa-section" id="q-229-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-229-a-07"></span><p>General misuse requires Invalid Use of CMB; placing lists with LISTS0 is explicitly undefined, not a fixed-status case.</p>
<span class="qa-anchor" id="q-229-a-16"></span><p>Interpret RDS/WDS by command transfer direction.</p>
</section>
</div>
<span class="qa-anchor" id="q-229-a-17"></span><span class="qa-anchor" id="q-229-a-08"></span><span class="qa-anchor" id="q-229-a-09"></span><span class="qa-anchor" id="q-229-a-10"></span><span class="qa-anchor" id="q-229-a-11"></span><span class="qa-anchor" id="q-229-a-12"></span><span class="qa-anchor" id="q-229-a-13"></span><span class="qa-anchor" id="q-229-a-14"></span><span class="qa-anchor" id="q-229-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-230" data-question="230" data-answer-kind="error"><h2><a class="qa-qid" href="#q-230">Q230</a> How are out-of-range or unsupported CMB uses handled?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-230-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-230-a-01">Distinguish invalid mapping, misuse within a mapped CMB and addresses interpreted elsewhere.</p><div class="qa-sections">
<section class="qa-section" id="q-230-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-230-a-02"></span><p>CBA/size define the controller range; disabled CMSE routes addresses elsewhere.</p>
<span class="qa-anchor" id="q-230-a-04"></span><p>CBA must not overflow the 64-bit address space or overlap enabled PMR space.</p>
<span class="qa-anchor" id="q-230-a-07"></span><p>Mapping failure uses CBAI; misuse uses its specified status. Out-of-range addresses may resolve elsewhere and have no universal CMB-overrun status.</p>
</section>
<section class="qa-section" id="q-230-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-230-a-03"></span><p>Preserve mapping/status/capabilities and the full command range.</p>
<span class="qa-anchor" id="q-230-a-05"></span><p>Calculate both range endpoints, resolve address spaces and check use/mixing rules.</p>
</section>
<section class="qa-section" id="q-230-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-230-a-06"></span><p>Valid ranges and uses follow ordinary command processing.</p>
<span class="qa-anchor" id="q-230-a-16"></span><p>Command outcomes and register status are separate evidence.</p>
<span class="qa-anchor" id="q-230-a-17"></span><p>First check arithmetic overflow and which address space was used.</p>
</section>
</div>
<span class="qa-anchor" id="q-230-a-08"></span><span class="qa-anchor" id="q-230-a-09"></span><span class="qa-anchor" id="q-230-a-10"></span><span class="qa-anchor" id="q-230-a-11"></span><span class="qa-anchor" id="q-230-a-12"></span><span class="qa-anchor" id="q-230-a-13"></span><span class="qa-anchor" id="q-230-a-14"></span><span class="qa-anchor" id="q-230-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-231" data-question="231" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-231">Q231</a> Do CMB configuration and contents survive reset?</h2>
<p class="qa-prompt">Name the reset or interruption, then assess settings, ongoing operations and data separately.</p>
<details class="qa-answer" id="q-231-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-231-a-01">Mapping retention and data retention are distinct.</p><div class="qa-sections">
<section class="qa-section" id="q-231-s-01" data-answer-section="1"><h3><span>1.</span> Identify the trigger and affected objects</h3>
<span class="qa-anchor" id="q-231-a-02"></span><p>CC.EN reset and FLR explicitly retain CMBMSC; other sources use their own register rules.</p>
<span class="qa-anchor" id="q-231-a-03"></span><p>Snapshot source and registers, then reread after recovery.</p>
</section>
<section class="qa-section" id="q-231-s-02" data-answer-section="2"><h3><span>2.</span> State changes and recovery</h3>
<span class="qa-anchor" id="q-231-a-04"></span><p>CMSE0→1, Controller Reset and FLR make CMB contents undefined.</p>
<span class="qa-anchor" id="q-231-a-05"></span><p>Restore mapping, initialize memory and rebuild queues, especially CQ phase bits.</p>
<span class="qa-anchor" id="q-231-a-06"></span><p>A new lifetime uses initialized contents, not old queue state.</p>
</section>
<section class="qa-section" id="q-231-s-03" data-answer-section="3"><h3><span>3.</span> Checks across reset or power loss</h3>
<span class="qa-anchor" id="q-231-a-12"></span>
<span class="qa-anchor" id="q-231-a-13"></span>
<span class="qa-anchor" id="q-231-a-14"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Trigger</th><th scope="col">Effect on this operation or state</th></tr></thead><tbody><tr><td>What survives or continues after Controller Reset?</td><td>CC.EN reset and FLR retain CMBMSC but make CMB contents undefined. Reinitialize memory, especially CQ phases; retained addressing does not preserve valid queues/data.</td></tr><tr><td>What survives or continues after NVM Subsystem Reset?</td><td>Rediscover mappings and rebuild queues after subsystem reset; do not extend specific CC.EN/FLR retention to every reset source.</td></tr><tr><td>What survives or continues after a power cycle?</td><td>CMB has no PMR-style power-cycle persistence guarantee; reconfigure and initialize it.</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-231-s-04" data-answer-section="4"><h3><span>4.</span> Verify retention and recovery</h3>
<span class="qa-anchor" id="q-231-a-07"></span><p>Identical residual bytes do not turn undefined retention into a guarantee.</p>
<span class="qa-anchor" id="q-231-a-16"></span><p>Validate mappings and content/queue initialization separately.</p>
<span class="qa-anchor" id="q-231-a-17"></span><p>First check whether unchanged CMBMSC incorrectly caused initialization to be skipped.</p>
</section>
</div>
<span class="qa-anchor" id="q-231-a-08"></span><span class="qa-anchor" id="q-231-a-09"></span><span class="qa-anchor" id="q-231-a-10"></span><span class="qa-anchor" id="q-231-a-11"></span><span class="qa-anchor" id="q-231-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-232" data-question="232" data-answer-kind="process"><h2><a class="qa-qid" href="#q-232">Q232</a> How is PMR discovered, enabled and made ready?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-232-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-232-a-01">PMR enablement is independent of the command controller and has its own readiness state.</p><div class="qa-sections">
<section class="qa-section" id="q-232-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-232-a-02"></span><p>PMR occupies the selected BAR region, with separately configurable controller addressing.</p>
<span class="qa-anchor" id="q-232-a-03"></span><p>Check support, location, command access, barrier mechanisms and timeout units.</p>
<span class="qa-anchor" id="q-232-a-04"></span><p>EN1 plus NRDY0 establishes readiness, with health/error checks still required.</p>
</section>
<section class="qa-section" id="q-232-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-232-a-05"></span>
<span class="qa-anchor" id="q-232-a-06"></span>
<span class="qa-anchor" id="q-232-a-16"></span>
<span class="qa-anchor" id="q-232-a-17"></span>
<figure class="qa-flow" id="q-232-flow"><figcaption>PMR has its own Enable and Ready</figcaption>
<p>CSTS.RDY and CC.EN do not answer whether PMR is usable.</p><ol class="qa-flow-steps">
<li class="qa-flow-step"><strong>Configure the required address space</strong><p>Establish supported BAR/controller mappings; check CBAI for an invalid controller base address.</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>Set PMRCTL.EN=1</strong><p>PMR can be enabled with CC.EN=0, without first enabling NVMe command processing.</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>Wait for PMRSTS.NRDY=0</strong><p>Before judging the transition incomplete, the host should wait at least PMRTO×PMRTU, using the indicated minutes or 500 ms unit.</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>Check HSTS, ERR and permitted use</strong><p>Access only when enabled, ready, healthy and correctly mapped, and only for supported uses.</p></li>
</ol><p class="qa-flow-conclusion">NRDY=1 means not ready. PMRTO is not an execution deadline for an arbitrary I/O command.</p></figure>
</section>
<section class="qa-section" id="q-232-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-232-a-07"></span><p>PMRTO is a transition wait allowance, not a per-command timeout; invalid addressing is reported by CBAI.</p>
</section>
</div>
<span class="qa-anchor" id="q-232-a-08"></span><span class="qa-anchor" id="q-232-a-09"></span><span class="qa-anchor" id="q-232-a-10"></span><span class="qa-anchor" id="q-232-a-11"></span><span class="qa-anchor" id="q-232-a-12"></span><span class="qa-anchor" id="q-232-a-13"></span><span class="qa-anchor" id="q-232-a-14"></span><span class="qa-anchor" id="q-232-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-233" data-question="233" data-answer-kind="error"><h2><a class="qa-qid" href="#q-233">Q233</a> What happens for not-ready or unhealthy PMR accesses?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-233-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-233-a-01">Completion of an access does not establish valid contents without PMR status.</p><div class="qa-sections">
<section class="qa-section" id="q-233-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-233-a-02"></span><p>Direct accesses and commands using PMR buffers expose errors differently.</p>
<span class="qa-anchor" id="q-233-a-04"></span><p>Not-ready reads can succeed with undefined data and writes can succeed without updating memory; health distinguishes restore failure, read-only and unreliable states.</p>
<span class="qa-anchor" id="q-233-a-07"></span><p>Detected failure writing an associated PMR should produce Data Transfer Error for the command; direct accesses have no NVMe CQE.</p>
</section>
<section class="qa-section" id="q-233-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-233-a-03"></span><p>Inspect EN/NRDY/HSTS/ERR; HSTS clears when not ready, so zero alone does not prove usable health.</p>
<span class="qa-anchor" id="q-233-a-05"></span><p>Establish readiness, access, then verify barriers/status and reconsider accesses since the last normal health observation.</p>
</section>
<section class="qa-section" id="q-233-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-233-a-06"></span><p>A successful NVMe command targeting PMR does not alone prove the PMR write succeeded.</p>
<span class="qa-anchor" id="q-233-a-16"></span><p>Validate command success and PMR health separately.</p>
<span class="qa-anchor" id="q-233-a-17"></span><p>First inspect readiness at access time, not merely after later recovery.</p>
</section>
</div>
<span class="qa-anchor" id="q-233-a-08"></span><span class="qa-anchor" id="q-233-a-09"></span><span class="qa-anchor" id="q-233-a-10"></span><span class="qa-anchor" id="q-233-a-11"></span><span class="qa-anchor" id="q-233-a-12"></span><span class="qa-anchor" id="q-233-a-13"></span><span class="qa-anchor" id="q-233-a-14"></span><span class="qa-anchor" id="q-233-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-234" data-question="234" data-answer-kind="process"><h2><a class="qa-qid" href="#q-234">Q234</a> How is PMR safely disabled?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-234-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-234-a-01">Establish completion and persistence before disabling rather than assuming in-flight writes are safe.</p><div class="qa-sections">
<section class="qa-section" id="q-234-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-234-a-02"></span><p>Coordinate direct users and commands still using PMR buffers.</p>
<span class="qa-anchor" id="q-234-a-03"></span><p>Check supported barriers, health and transition wait units.</p>
<span class="qa-anchor" id="q-234-a-04"></span><p>Use the advertised PMR-read or PMRSTS-read barrier, not an arbitrary register read.</p>
</section>
<section class="qa-section" id="q-234-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-234-a-05"></span><p>Stop accesses, drain users, perform the supported barrier/health check, clear EN and wait for NRDY1.</p>
<span class="qa-anchor" id="q-234-a-06"></span><p>NRDY1 indicates disabled readiness for re-enable; valid persistent content is not made undefined as CMB would be.</p>
</section>
<section class="qa-section" id="q-234-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-234-a-07"></span><p>Successful disable cannot prove earlier data valid when error/health state says otherwise.</p>
<span class="qa-anchor" id="q-234-a-16"></span><p>Verify barrier/health and enable-state ordering, not only final EN0.</p>
</section>
</div>
<span class="qa-anchor" id="q-234-a-17"></span><span class="qa-anchor" id="q-234-a-08"></span><span class="qa-anchor" id="q-234-a-09"></span><span class="qa-anchor" id="q-234-a-10"></span><span class="qa-anchor" id="q-234-a-11"></span><span class="qa-anchor" id="q-234-a-12"></span><span class="qa-anchor" id="q-234-a-13"></span><span class="qa-anchor" id="q-234-a-14"></span><span class="qa-anchor" id="q-234-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-235" data-question="235" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-235">Q235</a> How do resets and power cycles affect PMR state and data?</h2>
<p class="qa-prompt">Name the reset or interruption, then assess settings, ongoing operations and data separately.</p>
<details class="qa-answer" id="q-235-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-235-a-01">Persistence and current accessibility differ; restoration can leave retained data temporarily unavailable.</p><div class="qa-sections">
<section class="qa-section" id="q-235-s-01" data-answer-section="1"><h3><span>1.</span> Identify the trigger and affected objects</h3>
<span class="qa-anchor" id="q-235-a-02"></span><p>Retention applies to completed persistent writes, not unverified in-flight writes.</p>
<span class="qa-anchor" id="q-235-a-03"></span><p>Preserve barrier evidence and inspect enable/readiness/health/mapping after recovery.</p>
</section>
<section class="qa-section" id="q-235-s-02" data-answer-section="2"><h3><span>2.</span> State changes and recovery</h3>
<span class="qa-anchor" id="q-235-a-04"></span><p>Restore Error means current normal persistent operation with possibly incorrect restored content, unlike ongoing Unreliable status.</p>
<span class="qa-anchor" id="q-235-a-05"></span><p>Restore readiness, inspect health and verify content, accounting separately for Sanitize.</p>
<span class="qa-anchor" id="q-235-a-06"></span><p>Qualified persistent data survives CLR, disable and power cycle; register retention remains source-specific.</p>
</section>
<section class="qa-section" id="q-235-s-03" data-answer-section="3"><h3><span>3.</span> Checks across reset or power loss</h3>
<span class="qa-anchor" id="q-235-a-12"></span>
<span class="qa-anchor" id="q-235-a-13"></span>
<span class="qa-anchor" id="q-235-a-14"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Trigger</th><th scope="col">Effect on this operation or state</th></tr></thead><tbody><tr><td>What survives or continues after Controller Reset?</td><td>Ready-state persistent data survives CLR. CC.EN reset also retains PMR control/status registers; inspect health and Restore Error nonetheless.</td></tr><tr><td>What survives or continues after NVM Subsystem Reset?</td><td>Recheck enable/readiness and HSTS after subsystem reset. Data persistence differs from register restoration; Restore Error questions restored contents.</td></tr><tr><td>What survives or continues after a power cycle?</td><td>Confirmed persistent writes survive power cycles, subject to restored health checks. Sanitize can purge PMR and is distinct from ordinary power-loss behavior.</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-235-s-04" data-answer-section="4"><h3><span>4.</span> Verify retention and recovery</h3>
<span class="qa-anchor" id="q-235-a-07"></span><p>Nonzero ERR persists until PCI Function reset; clearing CC.EN does not necessarily clear it.</p>
<span class="qa-anchor" id="q-235-a-16"></span><p>Verify data, registers and errors as separate requirements.</p>
<span class="qa-anchor" id="q-235-a-17"></span><p>First distinguish persistent-data loss from incomplete writes or premature reads.</p>
</section>
</div>
<span class="qa-anchor" id="q-235-a-08"></span><span class="qa-anchor" id="q-235-a-09"></span><span class="qa-anchor" id="q-235-a-10"></span><span class="qa-anchor" id="q-235-a-11"></span><span class="qa-anchor" id="q-235-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-236" data-question="236" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-236">Q236</a> How do host memory, HMB, CMB and PMR lifetimes compare?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-236-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-236-a-01">Equal-looking data addresses can have different owners, initialization duties and reclamation conditions.</p><div class="qa-sections">
<section class="qa-section" id="q-236-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-236-a-02"></span><p>Ordinary host buffers are command-scoped; HMB is controller-exclusive; CMB is device-local; PMR adds persistence mechanisms.</p>
<span class="qa-anchor" id="q-236-a-04"></span><p>Reclaim ordinary buffers by command/queue lifetime, HMB after disable, initialize CMB after reset and verify PMR barriers/health.</p>
</section>
<section class="qa-section" id="q-236-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-236-a-03"></span><p>Use capabilities and command pointers to identify the actual space.</p>
<span class="qa-anchor" id="q-236-a-05"></span><p>Map host/controller addresses to physical memory and mark access/reclamation boundaries.</p>
<span class="qa-anchor" id="q-236-a-06"></span><p>A Write completion can end source-buffer use without releasing HMB or performing a PMR barrier.</p>
</section>
<section class="qa-section" id="q-236-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-236-a-07"></span><p>Error outcomes depend on the violated interface, not one universal memory-error status.</p>
<span class="qa-anchor" id="q-236-a-16"></span><p>Verify ownership, mapping, completion and persistence rather than merely readable contents.</p>
</section>
</div>
<span class="qa-anchor" id="q-236-a-17"></span><span class="qa-anchor" id="q-236-a-08"></span><span class="qa-anchor" id="q-236-a-09"></span><span class="qa-anchor" id="q-236-a-10"></span><span class="qa-anchor" id="q-236-a-11"></span><span class="qa-anchor" id="q-236-a-12"></span><span class="qa-anchor" id="q-236-a-13"></span><span class="qa-anchor" id="q-236-a-14"></span><span class="qa-anchor" id="q-236-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-hmb">Base 2.4 §5.2.30.2.3, 8.2.4</a> · <a href="#ref-cmb">Base 2.4 §8.2.1 (memory placement and lifetime)</a> · <a href="#ref-cmbreg">Base 2.4 §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</a> · <a href="#ref-pmr">Base 2.4 §8.2.5 (memory behavior; exclude PCIe packet detail)</a> · <a href="#ref-pmrreg">Base 2.4 §3.1.4 (PMR properties)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>

<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-cmbreg"><strong>Base 2.4 · §3.1.4 (CMBLOC, CMBSZ, CMBMSC, CMBSTS)</strong><br>Printed pages 67–69, 70–72 · PDF 93–95, 96–98 · Figure 47–48, 52–55</li>
<li id="ref-pmrreg"><strong>Base 2.4 · §3.1.4 (PMR properties)</strong><br>Printed pages 73–77 · PDF 99–103 · Figure 58–64</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-hmb"><strong>Base 2.4 · §5.2.30.2.3, 8.2.4</strong><br>Printed pages 515–519, 744 · PDF 541–545, 770 · Figure 545–553</li>
<li id="ref-cmb"><strong>Base 2.4 · §8.2.1 (memory placement and lifetime)</strong><br>Printed pages 742–744 · PDF 768–770</li>
<li id="ref-pmr"><strong>Base 2.4 · §8.2.5 (memory behavior; exclude PCIe packet detail)</strong><br>Printed pages 745–746 · PDF 771–772</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/memory/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/memory.html">Chinese tutorial HTML</a></nav>
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
