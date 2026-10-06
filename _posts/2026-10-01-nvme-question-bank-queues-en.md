---
layout: post
title: "NVMe Self-Study Bank: Admin and I/O queues"
date: 2026-10-01 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/queues/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/queues/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/queues.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q10–Q21</p><h1>Admin and I/O queues</h1><p class="qr-intro">Queue memory, allocated queue counts and successfully created queues are distinct. Learn SQ/CQ dependencies before size, identifiers, deletion and reset so memory can be reclaimed at the right time.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>One CQ and two SQs: creation and reclamation run in opposite directions</h2><p class="qa-takeaway">The CQ is the completion destination for its SQs; it cannot be deleted while an SQ still depends on it.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Observation</th><th scope="col">Hypothetical value</th><th scope="col">What it establishes</th></tr></thead><tbody><tr><td>Count allocation</td><td>FID 07h returns NSQA=3, NCQA=1</td><td>4 I/O SQs and 2 I/O CQs allocated, not created</td></tr><tr><td>Queue depth</td><td>Create CQ: QID=1, QSIZE=7</td><td>8 entries; the ring reserves one slot to distinguish full</td></tr><tr><td>Dependencies</td><td>SQ1.CQID=1; SQ2.CQID=1</td><td>Create CQ1 before SQ1 and SQ2</td></tr><tr><td>Reclamation</td><td>Delete SQ1/SQ2 and wait for their successful completions</td><td>Delete CQ1 next; reclaim memory after the relevant lifetime ends</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>If SQ1 is deleted but SQ2 remains, deleting CQ1 is still an invalid sequence: SQ2 still uses it. SQ1 deletion also does not authorize reclaiming SQ2 data buffers.</p>
<p class="qa-citations">Sources: <a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-010">Q10 · How are the Admin Submission and Completion Queues established through AQA, ASQ and ACQ?</a></li>
<li><a href="#q-011">Q11 · What are the size, base-address and page-alignment requirements for Admin and I/O queues?</a></li>
<li><a href="#q-012">Q12 · How are I/O CQs and SQs created, and why must the CQ be created first?</a></li>
<li><a href="#q-013">Q13 · How does sharing a CQ differ from giving every SQ its own CQ?</a></li>
<li><a href="#q-014">Q14 · How does the host determine supported queue memory layouts?</a></li>
<li><a href="#q-015">Q15 · Which statuses apply to duplicate/zero QIDs, missing CQIDs, oversized queues and invalid vectors?</a></li>
<li><a href="#q-016">Q16 · How do Number of Queues results relate to queues that can actually be created?</a></li>
<li><a href="#q-017">Q17 · Why must associated SQs be deleted before their CQ?</a></li>
<li><a href="#q-018">Q18 · What happens when deleting a missing queue, a referenced CQ or an SQ with outstanding commands?</a></li>
<li><a href="#q-019">Q19 · May the controller access deleted queue memory or post completions for its old commands?</a></li>
<li><a href="#q-020">Q20 · What is the scope of Queue Level Reset, and how is outstanding work handled?</a></li>
<li><a href="#q-021">Q21 · Are old I/O queues valid after Controller Reset, and what must the host do again?</a></li>
</ol></section>
<article class="qa-question" id="q-010" data-question="10" data-answer-kind="process"><h2><a class="qa-qid" href="#q-010">Q10</a> How are the Admin Submission and Completion Queues established through AQA, ASQ and ACQ?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-010-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-010-a-01">Establish the management channel before using Create I/O Queue. An absent Admin queue cannot create itself through a command.</p><div class="qa-sections">
<section class="qa-section" id="q-010-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-010-a-02"></span><p>Each controller has an Admin SQ/CQ with QID=0, separate from I/O queue identifiers.</p>
<span class="qa-anchor" id="q-010-a-03"></span><p>AQA gives both lengths; ASQ/ACQ give their physical bases. Admin queues require physical contiguity and are not created with a PC=0 Create Queue PRP list.</p>
<span class="qa-anchor" id="q-010-a-04"></span><p>ASQS/ACQS are zero-based: 64 entries encode as 63. Admin SQEs are 64 bytes and CQEs 16 bytes; the two queues need not have equal lengths.</p>
</section>
<section class="qa-section" id="q-010-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-010-a-05"></span><p>Allocate and initialize memory, write the three registers with EN=0 and clear Admin CQ phases. Configure CC, enable, wait for RDY=1, then submit the first Admin command.</p>
<span class="qa-anchor" id="q-010-a-06"></span><p>Identify can be submitted and matched by CID in Admin CQ. ACQ is associated with interrupt vector 0, while the host can also poll phase tags.</p>
</section>
<section class="qa-section" id="q-010-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-010-a-07"></span><p>Size=0 encodes one slot and is not a legal way to disable an Admin queue; enabling in that configuration is undefined. Delete I/O Queue cannot delete Admin queues.</p>
<span class="qa-anchor" id="q-010-a-16"></span><p>Compare AQA, allocated memory and the first CQE. Correct register readback does not establish device access to the supplied memory.</p>
</section>
</div>
<span class="qa-anchor" id="q-010-a-17"></span><span class="qa-anchor" id="q-010-a-08"></span><span class="qa-anchor" id="q-010-a-09"></span><span class="qa-anchor" id="q-010-a-10"></span><span class="qa-anchor" id="q-010-a-11"></span><span class="qa-anchor" id="q-010-a-12"></span><span class="qa-anchor" id="q-010-a-13"></span><span class="qa-anchor" id="q-010-a-14"></span><span class="qa-anchor" id="q-010-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-adminreg">Base 2.4 §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</a> · <a href="#ref-init">Base 2.4 §3.5.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-011" data-question="11" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-011">Q11</a> What are the size, base-address and page-alignment requirements for Admin and I/O queues?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-011-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-011-a-01">Keep entry counts, byte sizes and memory pages distinct, and prevent a queue from exceeding allocated memory.</p><div class="qa-sections">
<section class="qa-section" id="q-011-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-011-a-02"></span><p>Distinguish Admin/I/O and host-memory/CMB configurations. A rule for one is not automatically universal.</p>
<span class="qa-anchor" id="q-011-a-03"></span><p>Check AQA for Admin, and CAP.MQES/CQR and CC.IOSQES/IOCQES for I/O. CMB exceptions depend on CMBLOC.CQDA/CQPDS and CMBSZ queue support.</p>
</section>
<section class="qa-section" id="q-011-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-011-a-04"></span><p>Length fields encode entries−1. Ordinary bases and each PRP page of a discontiguous queue align to CC.MPS; PRP1 has offset zero.</p>
<span class="qa-anchor" id="q-011-a-05"></span><p>Choose slots and entry size, calculate bytes, allocate pages and a PRP list if supported, then Create. Do not alter a queue&#x27;s live PRP list.</p>
<span class="qa-anchor" id="q-011-a-06"></span><p>Minimum size is two slots; Admin maximum is 4096 and I/O maximum min(65536, MQES+1). One slot remains unavailable to distinguish full from empty.</p>
</section>
<section class="qa-section" id="q-011-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-011-a-07"></span><p>Invalid I/O sizes map to Invalid Queue Size (1/02h); nonzero PRP offsets should return PRP Offset Invalid (0/13h). Apply the specific SQ/CQ requirement for PC violating CQR.</p>
<span class="qa-anchor" id="q-011-a-16"></span><p>A 128-slot NVM SQ needs 8192 bytes, its CQ 2048 bytes. Equal QSIZE=127 does not imply equal byte allocations.</p>
</section>
</div>
<span class="qa-anchor" id="q-011-a-17"></span><span class="qa-anchor" id="q-011-a-08"></span><span class="qa-anchor" id="q-011-a-09"></span><span class="qa-anchor" id="q-011-a-10"></span><span class="qa-anchor" id="q-011-a-11"></span><span class="qa-anchor" id="q-011-a-12"></span><span class="qa-anchor" id="q-011-a-13"></span><span class="qa-anchor" id="q-011-a-14"></span><span class="qa-anchor" id="q-011-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-adminreg">Base 2.4 §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</a> · <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-qattr">Base 2.4 §3.3.3–3.4.1</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-012" data-question="12" data-answer-kind="process"><h2><a class="qa-qid" href="#q-012">Q12</a> How are I/O CQs and SQs created, and why must the CQ be created first?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-012-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-012-a-01">Every I/O needs a valid completion destination. Create the CQ before its SQ: this is an ordering requirement, not merely a performance recommendation.</p><div class="qa-sections">
<section class="qa-section" id="q-012-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-012-a-02"></span><p>An SQ selects its CQ at creation; several SQs may use one existing CQ.</p>
<span class="qa-anchor" id="q-012-a-03"></span><p>Allocate Number of Queues first, then check MQES/CQR, entry sizes and interrupt-vector limits.</p>
<span class="qa-anchor" id="q-012-a-04"></span><p>Create CQ uses PRP1, QID, QSIZE, PC, IEN and IV. Create SQ additionally uses CQID, QPRIO and NVMSETID; zero NVMSETID means no specific set association.</p>
</section>
<section class="qa-section" id="q-012-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-012-a-05"></span>
<span class="qa-anchor" id="q-012-a-06"></span>
<span class="qa-anchor" id="q-012-a-17"></span>
<figure class="qa-flow" id="q-012-flow"><figcaption>Create the CQ before an SQ refers to it</figcaption>
<p>Each arrow requires completion of the preceding step, not merely submission order.</p><ol class="qa-flow-steps">
<li class="qa-flow-step"><strong>Prepare CQ memory</strong><p>Allocate with the required size and alignment, and initialize CQE phase bits.</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>Create I/O CQ → await success on the Admin CQ</strong><p>This Create completes on the Admin CQ, not on the new I/O CQ.</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>Create I/O SQ → await success on the Admin CQ</strong><p>CQID refers to the successfully created CQ. Both successful Creates report SCT=0, SC=00h.</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>Start I/O</strong><p>Only after both steps succeed, populate I/O SQEs and update the SQ Tail Doorbell.</p></li>
</ol><p class="qa-flow-conclusion">If CQ creation fails, that CQ is not available to the SQ. Resolve the failure; submitted is not the same as successfully created.</p></figure>
</section>
<section class="qa-section" id="q-012-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-012-a-07"></span><p>An in-range CQID that has not been created returns Completion Queue Invalid (1/00h); CQID=0 or out of range returns Invalid Queue Identifier (1/01h).</p>
<span class="qa-anchor" id="q-012-a-16"></span><p>Match CQID against the host&#x27;s SQ-to-CQ map. Creating a CQ does not automatically associate every SQ with it.</p>
</section>
</div>
<span class="qa-anchor" id="q-012-a-08"></span><span class="qa-anchor" id="q-012-a-09"></span><span class="qa-anchor" id="q-012-a-10"></span><span class="qa-anchor" id="q-012-a-11"></span><span class="qa-anchor" id="q-012-a-12"></span><span class="qa-anchor" id="q-012-a-13"></span><span class="qa-anchor" id="q-012-a-14"></span><span class="qa-anchor" id="q-012-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-013" data-question="13" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-013">Q13</a> How does sharing a CQ differ from giving every SQ its own CQ?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-013-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-013-a-01">Trade resource usage against completion-path isolation. Shared CQs reduce CQ resources but concentrate completion traffic.</p><div class="qa-sections">
<section class="qa-section" id="q-013-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-013-a-02"></span><p>Completion slots and CQ notification are shared; the SQs do not become one CID namespace.</p>
<span class="qa-anchor" id="q-013-a-04"></span><p>CQE.SQID+CID identifies the original command; SQHD updates consumption for that SQ.</p>
</section>
<section class="qa-section" id="q-013-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-013-a-03"></span><p>Number of Queues returns separate SQ/CQ allocations. Create SQ.CQID selects the mapping; CQ.IEN/IV configures notification.</p>
<span class="qa-anchor" id="q-013-a-05"></span><p>Create the CQ and multiple SQs referencing it. Dispatch each CQE by SQID, then advance the shared CQ head.</p>
<span class="qa-anchor" id="q-013-a-06"></span><p>SQ1/CID 7 and SQ2/CID 7 may coexist and must be matched separately, unlike reusing an outstanding CID within one SQ.</p>
</section>
<section class="qa-section" id="q-013-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-013-a-07"></span><p>Valid sharing is not an error. Missing CQIDs follow Create SQ status rules; a full shared CQ does not automatically produce Invalid Queue Size for each SQ.</p>
<span class="qa-anchor" id="q-013-a-16"></span><p>Compare completion capacity, submission traffic and host consumption rate; SQ count alone does not establish freedom from bottlenecks.</p>
</section>
</div>
<span class="qa-anchor" id="q-013-a-17"></span><span class="qa-anchor" id="q-013-a-08"></span><span class="qa-anchor" id="q-013-a-09"></span><span class="qa-anchor" id="q-013-a-10"></span><span class="qa-anchor" id="q-013-a-11"></span><span class="qa-anchor" id="q-013-a-12"></span><span class="qa-anchor" id="q-013-a-13"></span><span class="qa-anchor" id="q-013-a-14"></span><span class="qa-anchor" id="q-013-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-014" data-question="14" data-answer-kind="lookup"><h2><a class="qa-qid" href="#q-014">Q14</a> How does the host determine supported queue memory layouts?</h2>
<p class="qa-prompt">Choose the interface and target, then identify the returned field that supports your conclusion.</p>
<details class="qa-answer" id="q-014-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-014-a-01">Describe queue memory in a layout the controller supports. Virtual contiguity does not establish physical contiguity.</p><div class="qa-sections">
<section class="qa-section" id="q-014-s-01" data-answer-section="1"><h3><span>1.</span> Select the target and information</h3>
<span class="qa-anchor" id="q-014-a-02"></span><p>Admin queues require physical contiguity. Discontiguous I/O queues depend on CAP.CQR and memory location.</p>
<span class="qa-anchor" id="q-014-a-03"></span><p>CQR=1 requires physical contiguity; CQR=0 allows discontiguous I/O queues. CMB placement additionally requires CMBSZ.SQS/CQS and CMBLOC.CQPDS/CQDA checks.</p>
<span class="qa-anchor" id="q-014-a-04"></span><p>With Create I/O Queue.PC=1, PRP1 is the queue base; with PC=0 it points to a queue-page PRP list, distinct from ordinary data-transfer PRP2 rules.</p>
</section>
<section class="qa-section" id="q-014-s-02" data-answer-section="2"><h3><span>2.</span> Query sequence and interpretation</h3>
<span class="qa-anchor" id="q-014-a-05"></span><p>Confirm placement/support, build a complete aligned page list and Create. Retain the list&#x27;s address and contents until successful deletion or reset.</p>
<span class="qa-anchor" id="q-014-a-06"></span><p>The controller fetches SQEs/writes CQEs through the chosen layout. Successful Create does not authorize rearranging its pages while live.</p>
</section>
<section class="qa-section" id="q-014-s-03" data-answer-section="3"><h3><span>3.</span> Handle missing or inconsistent evidence</h3>
<span class="qa-anchor" id="q-014-a-07"></span><p>For CQR=1 and PC=0, Create CQ shall return Invalid Field (0/02h), while Create SQ says should. Unsupported CMB usage may return Invalid Use of Controller Memory Buffer (0/12h).</p>
<span class="qa-anchor" id="q-014-a-16"></span><p>Cross-check CQR, PC, PRP1 interpretation and actual page layout, rather than validating only the completion.</p>
<span class="qa-anchor" id="q-014-a-17"></span><p>First ask whether PRP1 addresses queue storage or its page list. Confusing them breaks the layout even with valid addresses.</p>
</section>
</div>
<span class="qa-anchor" id="q-014-a-08"></span><span class="qa-anchor" id="q-014-a-09"></span><span class="qa-anchor" id="q-014-a-10"></span><span class="qa-anchor" id="q-014-a-11"></span><span class="qa-anchor" id="q-014-a-12"></span><span class="qa-anchor" id="q-014-a-13"></span><span class="qa-anchor" id="q-014-a-14"></span><span class="qa-anchor" id="q-014-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-adminreg">Base 2.4 §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-015" data-question="15" data-answer-kind="error"><h2><a class="qa-qid" href="#q-015">Q15</a> Which statuses apply to duplicate/zero QIDs, missing CQIDs, oversized queues and invalid vectors?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-015-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-015-a-01">Match distinct parameter errors to their defined statuses instead of flattening them into Invalid Field.</p><div class="qa-sections">
<section class="qa-section" id="q-015-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-015-a-02"></span><p>This concerns Create I/O Queue Admin commands. Duplicate QIDs are checked within the SQ or CQ identifier space respectively.</p>
<span class="qa-anchor" id="q-015-a-04"></span><p>Inspect QID, CQID, QSIZE and IV, and initialization of IOSQES/IOCQES. The relevant parameters are in CDW10/11.</p>
<span class="qa-anchor" id="q-015-a-07"></span><p>Duplicate/zero/out-of-range QID: 1/01h. Zero/unsupported QSIZE: 1/02h. In-range uncreated CQID: 1/00h. Zero/out-of-range CQID: 1/01h. Invalid IV: 1/08h. Unless specified otherwise, implementations choose among simultaneously applicable errors.</p>
</section>
<section class="qa-section" id="q-015-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-015-a-03"></span><p>CAP.MQES, Number of Queues allocations and PCIe interrupt configuration establish legal ranges.</p>
<span class="qa-anchor" id="q-015-a-05"></span><p>For a learning test, change one condition at a time from a valid baseline; multiple errors can obscure the expected result.</p>
</section>
<section class="qa-section" id="q-015-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-015-a-06"></span><p>Valid parameters successfully create the queue; after failure, do not treat the requested QID as created.</p>
<span class="qa-anchor" id="q-015-a-16"></span><p>When available, Error Information Parameter Error Location can identify the field. Without More=1, do not assume every such error must have an entry.</p>
<span class="qa-anchor" id="q-015-a-17"></span><p>First check that only one field is invalid and the expected SCT is 1, rather than comparing SC alone.</p>
</section>
</div>
<span class="qa-anchor" id="q-015-a-08"></span><span class="qa-anchor" id="q-015-a-09"></span><span class="qa-anchor" id="q-015-a-10"></span><span class="qa-anchor" id="q-015-a-11"></span><span class="qa-anchor" id="q-015-a-12"></span><span class="qa-anchor" id="q-015-a-13"></span><span class="qa-anchor" id="q-015-a-14"></span><span class="qa-anchor" id="q-015-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-irq">PCIe Transport 1.4 §3.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-016" data-question="16" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-016">Q16</a> How do Number of Queues results relate to queues that can actually be created?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-016-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-016-a-01">Obtain SQ/CQ allocations before creating queues. Allocation is neither an instantiated queue nor queue depth.</p><div class="qa-sections">
<section class="qa-section" id="q-016-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-016-a-02"></span><p>FID 07h has controller scope and excludes Admin SQ/CQ.</p>
<span class="qa-anchor" id="q-016-a-03"></span><p>Use Set Features FID 07h CQE DW0 for actual allocations, with Get Features readback. CAP.MQES separately limits per-queue depth.</p>
</section>
<section class="qa-section" id="q-016-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-016-a-04"></span><p>Requested NSQR/NCQR and returned NSQA/NCQA are zero-based. Allocations may be smaller or larger than requested because of allocation units.</p>
<span class="qa-anchor" id="q-016-a-05"></span><p>Set it after CLR and before creating any I/O queue. The first successful setting fixes allocation until the next CLR.</p>
<span class="qa-anchor" id="q-016-a-06"></span><p>DW0=00030007h allocates four CQs and eight SQs. Each still requires Create, with the respective QID ranges.</p>
</section>
<section class="qa-section" id="q-016-s-03" data-answer-section="3"><h3><span>3.</span> Checks across reset or power loss</h3>
<span class="qa-anchor" id="q-016-a-12"></span>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Trigger</th><th scope="col">Effect on this operation or state</th></tr></thead><tbody><tr><td>What survives or continues after Controller Reset?</td><td>The first successful Set FID 07h after CLR allocates anew. Read the result and recreate queues rather than assuming the previous allocation.</td></tr></tbody></table></div>
</section>
<section class="qa-section" id="q-016-s-04" data-answer-section="4"><h3><span>4.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-016-a-07"></span><p>Setting after an I/O queue exists shall return Command Sequence Error (0/0Ch). Requested=FFFFh should return Invalid Field (0/02h). Subsequent Set before queue creation should succeed without changing allocation.</p>
<span class="qa-anchor" id="q-016-a-16"></span><p>Compare allocations, the actual created-queue list and MQES. Allocated counts are not current existence counts.</p>
</section>
</div>
<span class="qa-anchor" id="q-016-a-17"></span><span class="qa-anchor" id="q-016-a-08"></span><span class="qa-anchor" id="q-016-a-09"></span><span class="qa-anchor" id="q-016-a-10"></span><span class="qa-anchor" id="q-016-a-11"></span><span class="qa-anchor" id="q-016-a-13"></span><span class="qa-anchor" id="q-016-a-14"></span><span class="qa-anchor" id="q-016-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-feature">Base 2.4 §4.4</a> · <a href="#ref-setfeat">Base 2.4 §5.2.30.1 (common fields, scope and persistence)</a> · <a href="#ref-featureeffects">Base 2.4 §5.2.13.1.18</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-017" data-question="17" data-answer-kind="process"><h2><a class="qa-qid" href="#q-017">Q17</a> Why must associated SQs be deleted before their CQ?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-017-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-017-a-01">Prevent active SQs from losing their completion destination. For associated queues this is a required host deletion order.</p><div class="qa-sections">
<section class="qa-section" id="q-017-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-017-a-02"></span><p>A CQ may serve multiple SQs. Delete every associated SQ, not only an SQ with the same numeric QID.</p>
<span class="qa-anchor" id="q-017-a-03"></span><p>Use the host&#x27;s SQ-to-CQID map from creation. Number of Queues does not provide this association list.</p>
<span class="qa-anchor" id="q-017-a-04"></span><p>Delete I/O SQ/CQ selects the target with CDW10.QID; both travel through Admin SQ.</p>
</section>
<section class="qa-section" id="q-017-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-017-a-05"></span><p>Stop submissions, appropriately drain work, delete each associated SQ and await success, process needed old completions, then delete the CQ.</p>
<span class="qa-anchor" id="q-017-a-06"></span><p>Successful Delete CQ allows reclamation of its PRP list and queue resources. Successful Delete SQ separately establishes termination of processing for that SQ&#x27;s commands.</p>
</section>
<section class="qa-section" id="q-017-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-017-a-07"></span><p>Delete CQ with associated SQs shall return Invalid Queue Deletion (1/0Ch); zero or invalid QID returns Invalid Queue Identifier (1/01h).</p>
<span class="qa-anchor" id="q-017-a-16"></span><p>Correlate successful deletion with memory reclamation. Merely submitting Delete does not authorize early reclamation of DMA memory.</p>
</section>
</div>
<span class="qa-anchor" id="q-017-a-17"></span><span class="qa-anchor" id="q-017-a-08"></span><span class="qa-anchor" id="q-017-a-09"></span><span class="qa-anchor" id="q-017-a-10"></span><span class="qa-anchor" id="q-017-a-11"></span><span class="qa-anchor" id="q-017-a-12"></span><span class="qa-anchor" id="q-017-a-13"></span><span class="qa-anchor" id="q-017-a-14"></span><span class="qa-anchor" id="q-017-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-018" data-question="18" data-answer-kind="error"><h2><a class="qa-qid" href="#q-018">Q18</a> What happens when deleting a missing queue, a referenced CQ or an SQ with outstanding commands?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-018-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-018-a-01">Distinguish an invalid deletion request from valid deletion terminating commands. Outstanding work does not itself make Delete SQ illegal.</p><div class="qa-sections">
<section class="qa-section" id="q-018-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-018-a-02"></span><p>SQ deletion affects its outstanding I/O; CQ deletion depends on the existence of every associated SQ.</p>
<span class="qa-anchor" id="q-018-a-04"></span><p>Delete requires a valid nonzero QID; affected I/O commands retain their own SQID/CID identities.</p>
<span class="qa-anchor" id="q-018-a-07"></span><p>Invalid QID: 1/01h. CQ still referenced: 1/0Ch. I/O aborted by SQ deletion uses 0/08h, including implicit completion established by successful Delete.</p>
</section>
<section class="qa-section" id="q-018-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-018-a-03"></span><p>Consult host creation/deletion and outstanding-command records. These are runtime state, not Identify optional capabilities.</p>
<span class="qa-anchor" id="q-018-a-05"></span><p>Drain before normal teardown. If deleting an SQ to stop work, treat remaining commands without CQEs as implicitly aborted after successful Delete.</p>
</section>
<section class="qa-section" id="q-018-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-018-a-06"></span><p>Before successful Delete SQ, original commands may complete normally or with abort status. After success, no further completions may be posted for those commands.</p>
<span class="qa-anchor" id="q-018-a-16"></span><p>Account for both received CQEs and implicit aborts after successful Delete; do not require a physical CQE for every original command.</p>
<span class="qa-anchor" id="q-018-a-17"></span><p>First check whether Delete SQ itself completed successfully. Its outstanding state does not establish that all original work stopped.</p>
</section>
</div>
<span class="qa-anchor" id="q-018-a-08"></span><span class="qa-anchor" id="q-018-a-09"></span><span class="qa-anchor" id="q-018-a-10"></span><span class="qa-anchor" id="q-018-a-11"></span><span class="qa-anchor" id="q-018-a-12"></span><span class="qa-anchor" id="q-018-a-13"></span><span class="qa-anchor" id="q-018-a-14"></span><span class="qa-anchor" id="q-018-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-019" data-question="19" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-019">Q19</a> May the controller access deleted queue memory or post completions for its old commands?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-019-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-019-a-01">Establish the memory-reclamation boundary and distinguish an earlier write observed late from a new write after successful deletion.</p><div class="qa-sections">
<section class="qa-section" id="q-019-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-019-a-02"></span><p>Deleting an SQ does not delete its shared CQ; already posted completions may remain for host consumption.</p>
<span class="qa-anchor" id="q-019-a-04"></span><p>Track deleted QID, associated CQID, PRP-list address and memory lifetime. Reused addresses require distinguishing queue lifetimes.</p>
</section>
<section class="qa-section" id="q-019-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-019-a-03"></span><p>Use successful Delete completion on Admin CQ as the boundary, not submission time or a host timeout.</p>
<span class="qa-anchor" id="q-019-a-05"></span><p>Stop submissions, successfully delete, then reclaim the corresponding queue/list memory. With SQ-only deletion, handle existing posted entries in the surviving CQ.</p>
<span class="qa-anchor" id="q-019-a-06"></span><p>After successful Delete SQ, no new completions for its old commands may be posted. Successful Delete CQ permits releasing its list; a deleted queue is no longer a valid DMA target.</p>
</section>
<section class="qa-section" id="q-019-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-019-a-07"></span><p>Failure or absence of Delete completion does not authorize memory reclamation. Timeout is not a substitute for success.</p>
<span class="qa-anchor" id="q-019-a-16"></span><p>Correlate write time, phase, Delete completion and host consumption. Late consumption of an old CQE is not necessarily a prohibited late write.</p>
</section>
</div>
<span class="qa-anchor" id="q-019-a-17"></span><span class="qa-anchor" id="q-019-a-08"></span><span class="qa-anchor" id="q-019-a-09"></span><span class="qa-anchor" id="q-019-a-10"></span><span class="qa-anchor" id="q-019-a-11"></span><span class="qa-anchor" id="q-019-a-12"></span><span class="qa-anchor" id="q-019-a-13"></span><span class="qa-anchor" id="q-019-a-14"></span><span class="qa-anchor" id="q-019-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-020" data-question="20" data-answer-kind="process"><h2><a class="qa-qid" href="#q-020">Q20</a> What is the scope of Queue Level Reset, and how is outstanding work handled?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-020-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-020-a-01">Rebuild I/O queues without resetting the whole controller. PCIe Queue Level Reset means deletion and recreation, not a separate reset opcode.</p><div class="qa-sections">
<section class="qa-section" id="q-020-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-020-a-02"></span><p>Reset the target and its necessary dependencies. Rebuilding a CQ requires deleting its SQs first and recreating them afterward.</p>
<span class="qa-anchor" id="q-020-a-03"></span><p>Use existing queue associations and Create/Delete rules, not a separate Queue Reset feature.</p>
<span class="qa-anchor" id="q-020-a-04"></span><p>Use Delete SQ/CQ and Create CQ/SQ. QIDs may be reused, but memory and pointers begin a new lifetime.</p>
</section>
<section class="qa-section" id="q-020-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-020-a-05"></span><p>Normally let work finish before deletion. For cancellation, apply explicit/implicit Delete SQ completion rules. Initialize new CQ phases and create CQ before SQ.</p>
<span class="qa-anchor" id="q-020-a-06"></span><p>New commands execute after reconstruction; old outstanding commands are not automatically migrated into the new SQ.</p>
</section>
<section class="qa-section" id="q-020-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-020-a-07"></span><p>Deleting a referenced CQ returns 1/0Ch; premature SQ creation returns the applicable CQID error. Queue reset has no additional universal status.</p>
<span class="qa-anchor" id="q-020-a-16"></span><p>Check teardown/recreation ordering, command-lifetime tracking and continued operation of independent queues.</p>
</section>
</div>
<span class="qa-anchor" id="q-020-a-17"></span><span class="qa-anchor" id="q-020-a-08"></span><span class="qa-anchor" id="q-020-a-09"></span><span class="qa-anchor" id="q-020-a-10"></span><span class="qa-anchor" id="q-020-a-11"></span><span class="qa-anchor" id="q-020-a-12"></span><span class="qa-anchor" id="q-020-a-13"></span><span class="qa-anchor" id="q-020-a-14"></span><span class="qa-anchor" id="q-020-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-021" data-question="21" data-answer-kind="process"><h2><a class="qa-qid" href="#q-021">Q21</a> Are old I/O queues valid after Controller Reset, and what must the host do again?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-021-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-021-a-01">Separate pre-failure commands from new work after recovery to avoid accepting stale completions.</p><div class="qa-sections">
<section class="qa-section" id="q-021-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-021-a-02"></span><p>Controller Level Reset deletes all I/O SQs/CQs of that controller, unlike deleting only one SQ.</p>
<span class="qa-anchor" id="q-021-a-03"></span><p>Re-read necessary Identify data and verify queue allocations, entry sizes and interrupt settings rather than assuming previous values remain usable.</p>
<span class="qa-anchor" id="q-021-a-04"></span><p>Admin registers, CC, Get/Set Features and Create CQ/SQ together establish the recovery path.</p>
</section>
<section class="qa-section" id="q-021-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-021-a-05"></span><p>Confirm RDY=0, initialize Admin CQ phases and CC, enable/wait ready, restore needed features, set Number of Queues, create CQ then SQ, and allow new I/O.</p>
<span class="qa-anchor" id="q-021-a-06"></span><p>Each new queue becomes valid after its successful Create completion on Admin CQ, even when reusing an identifier or address.</p>
</section>
<section class="qa-section" id="q-021-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-021-a-07"></span><p>Updating old queue doorbells is not a valid recovery method. Failures of reconstruction commands follow their specific status rules.</p>
<span class="qa-anchor" id="q-021-a-16"></span><p>Track queue lifetimes and command mappings across reset in host software; this is not a new NVMe wire field.</p>
</section>
</div>
<span class="qa-anchor" id="q-021-a-17"></span><span class="qa-anchor" id="q-021-a-08"></span><span class="qa-anchor" id="q-021-a-09"></span><span class="qa-anchor" id="q-021-a-10"></span><span class="qa-anchor" id="q-021-a-11"></span><span class="qa-anchor" id="q-021-a-12"></span><span class="qa-anchor" id="q-021-a-13"></span><span class="qa-anchor" id="q-021-a-14"></span><span class="qa-anchor" id="q-021-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-init">Base 2.4 §3.5.1</a> · <a href="#ref-number">Base 2.4 §5.2.30.1.5</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>

<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-cap"><strong>Base 2.4 · §3.1.4 (CAP, VS)</strong><br>Printed pages 54–59 · PDF 80–85 · Figure 36–37</li>
<li id="ref-adminreg"><strong>Base 2.4 · §3.1.4 (AQA, ASQ, ACQ, CMBLOC)</strong><br>Printed pages 66–68 · PDF 92–94 · Figure 44–47</li>
<li id="ref-queue"><strong>Base 2.4 · §3.3.1</strong><br>Printed pages 88–91 · PDF 114–117 · Figure 73–74</li>
<li id="ref-qattr"><strong>Base 2.4 · §3.3.3–3.4.1</strong><br>Printed pages 101 · PDF 127</li>
<li id="ref-init"><strong>Base 2.4 · §3.5.1</strong><br>Printed pages 105–106 · PDF 131–132</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>Printed pages 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-feature"><strong>Base 2.4 · §4.4</strong><br>Printed pages 166–169 · PDF 192–195 · Figure 126–127</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-featureeffects"><strong>Base 2.4 · §5.2.13.1.18</strong><br>Printed pages 276–278 · PDF 302–304 · Figure 270–271</li>
<li id="ref-setfeat"><strong>Base 2.4 · §5.2.30.1 (common fields, scope and persistence)</strong><br>Printed pages 456–460 · PDF 482–486 · Figure 463–466</li>
<li id="ref-number"><strong>Base 2.4 · §5.2.30.1.5</strong><br>Printed pages 465–466 · PDF 491–492 · Figure 472–473</li>
<li id="ref-create"><strong>Base 2.4 · §5.3.1–5.3.2</strong><br>Printed pages 527–531 · PDF 553–557 · Figure 571–579</li>
<li id="ref-delete"><strong>Base 2.4 · §5.3.3–5.3.4</strong><br>Printed pages 531–532 · PDF 557–558 · Figure 580–583</li>
<li id="ref-fatal"><strong>Base 2.4 · §9.1–9.6.1</strong><br>Printed pages 825–826 · PDF 851–852</li>
<li id="ref-irq"><strong>PCIe Transport 1.4 · §3.5</strong><br>Printed pages 13–16 · PDF 13–16 · Figure 9</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b44">Base 2.4 Figure 44 · Offset 24h: AQA – Admin Queue Attributes</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b45">Base 2.4 Figure 45 · Offset 28h: ASQ – Admin Submission Queue Base Address</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b46">Base 2.4 Figure 46 · Offset 30h: ACQ – Admin Completion Queue Base Address</a></li>
<li><a href="/nvme/figure-reference/features/en/#figure-b473">Base 2.4 Figure 473 · Number of Queues – Completion Queue Entry Dword 0</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/queues/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/queues.html">Chinese tutorial HTML</a></nav>
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
