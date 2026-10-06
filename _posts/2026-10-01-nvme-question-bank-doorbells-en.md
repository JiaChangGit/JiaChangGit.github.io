---
layout: post
title: "NVMe Self-Study Bank: Doorbells, full queues and wrap-around"
date: 2026-10-01 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/doorbells/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/doorbells/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/doorbells.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q22–Q30</p><h1>Doorbells, full queues and wrap-around</h1><p class="qr-intro">Doorbells communicate pointer positions; phase tells the host whether a CQ slot belongs to the next completion generation. Together they distinguish wrap-around from an invalid movement and new completions from stale ones.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>An eight-entry CQ: wrap-around and phase together</h2><p class="qa-takeaway">Returning to slot 0 does not make old data valid again; the host must also compare the expected phase.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Point in time</th><th scope="col">Host next slot / expected phase</th><th scope="col">Read result and action</th></tr></thead><tbody><tr><td>Initialization</td><td>Slot 0, expect P=1; initialize memory P to 0</td><td>No new completion yet</td></tr><tr><td>End of first traversal</td><td>Slot 7, expect P=1</td><td>P=1: consume CQE, wrap to 0, change expectation to 0</td></tr><tr><td>Start of second traversal</td><td>Slot 0, expect P=0</td><td>Ignore stale P=1; consume only new P=0</td></tr><tr><td>Report consumption</td><td>CQ Head advances from 7 to 2</td><td>Consumed slots 7, 0, 1: 3 entries, not a retreat by 5</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>Modular distance is (2−7+8) mod 8=3. The doorbell reports position 2, not “free two more slots.” Phase establishes CQE validity; the head doorbell reports consumption to the controller.</p>
<p class="qa-citations">Sources: <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-022">Q22 · When should the host update SQ Tail and CQ Head doorbells?</a></li>
<li><a href="#q-023">Q23 · What happens with repeated, apparently backward, out-of-range or wrong-QID doorbells?</a></li>
<li><a href="#q-024">Q24 · How are SQ/CQ doorbell addresses calculated from CAP.DSTRD?</a></li>
<li><a href="#q-025">Q25 · May the host access doorbells of uncreated/deleted queues or a disabled controller?</a></li>
<li><a href="#q-026">Q26 · How should SQ Tail and CQ Head wrap around?</a></li>
<li><a href="#q-027">Q27 · How does the CQ phase change across wrap, and how does the host identify a new completion?</a></li>
<li><a href="#q-028">Q28 · How does CQ Full arise, and may related SQ processing continue?</a></li>
<li><a href="#q-029">Q29 · How does processing resume when the host releases CQ space?</a></li>
<li><a href="#q-030">Q30 · How does the host identify completions from SQs sharing a CQ?</a></li>
</ol></section>
<article class="qa-question" id="q-022" data-question="22" data-answer-kind="process"><h2><a class="qa-qid" href="#q-022">Q22</a> When should the host update SQ Tail and CQ Head doorbells?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-022-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-022-a-01">Notify the controller of completed host memory work: SQ Tail submits commands, while CQ Head releases completion slots.</p><div class="qa-sections">
<section class="qa-section" id="q-022-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-022-a-02"></span><p>Each SQ/CQ has its own doorbell; updating one does not update another.</p>
<span class="qa-anchor" id="q-022-a-03"></span><p>Verify a valid queue, a ready controller, sufficient free slots and the register address derived from CAP.DSTRD.</p>
<span class="qa-anchor" id="q-022-a-04"></span><p>SQ Tail points to the next insertion slot; CQ Head points to the next completion to consume. Writes contain new pointer values, not increments.</p>
</section>
<section class="qa-section" id="q-022-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-022-a-05"></span><p>Make complete SQEs visible using the platform&#x27;s memory-ordering requirements before updating Tail. Consume valid CQEs before updating Head; batching is allowed.</p>
<span class="qa-anchor" id="q-022-a-06"></span><p>The controller learns which commands can be fetched and which CQ slots can be reused. Advancing CQ Head does not submit new I/O.</p>
</section>
<section class="qa-section" id="q-022-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-022-a-07"></span><p>Releasing unconsumed CQEs risks overwrite. Submitting incomplete SQEs violates usage ordering and has no guaranteed single error CQE.</p>
<span class="qa-anchor" id="q-022-a-16"></span><p>Build a timeline of SQE writes, Tail updates, CQE phase changes and Head updates; they have distinct roles.</p>
</section>
</div>
<span class="qa-anchor" id="q-022-a-17"></span><span class="qa-anchor" id="q-022-a-08"></span><span class="qa-anchor" id="q-022-a-09"></span><span class="qa-anchor" id="q-022-a-10"></span><span class="qa-anchor" id="q-022-a-11"></span><span class="qa-anchor" id="q-022-a-12"></span><span class="qa-anchor" id="q-022-a-13"></span><span class="qa-anchor" id="q-022-a-14"></span><span class="qa-anchor" id="q-022-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-023" data-question="23" data-answer-kind="error"><h2><a class="qa-qid" href="#q-023">Q23</a> What happens with repeated, apparently backward, out-of-range or wrong-QID doorbells?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-023-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-023-a-01">Validate pointer movement without treating a ring index as a monotonically increasing counter.</p><div class="qa-sections">
<section class="qa-section" id="q-023-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-023-a-02"></span><p>Errors affect the target queue and possibly SQs sharing its CQ. Access to a nonexistent queue differs from an invalid value on an existing queue.</p>
<span class="qa-anchor" id="q-023-a-04"></span><p>New values lie in 0..size−1. A repeated value announces no new slots; a numerically smaller value may be a valid wrap.</p>
<span class="qa-anchor" id="q-023-a-07"></span><p>Invalid values on an existing queue have Invalid Doorbell Write Value asynchronous handling; writing a nonexistent queue doorbell is undefined. Event information is not a CQE status for the MMIO write.</p>
</section>
<section class="qa-section" id="q-023-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-023-a-03"></span><p>Need size, previous pointer, available/consumed slots and QID mapping. The new value alone is insufficient.</p>
<span class="qa-anchor" id="q-023-a-05"></span><p>For size=8, Tail 6→1 advances three slots, provided three are free and populated. A 6→6 write cannot announce a full ring of new commands.</p>
</section>
<section class="qa-section" id="q-023-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-023-a-06"></span><p>A valid movement communicates the correct count. Doorbell readback is vendor-specific and is not a verification method.</p>
<span class="qa-anchor" id="q-023-a-16"></span><p>Compare old pointer, ring size and available space, not just numeric ordering. Correlate the error event with affected-queue command consumption.</p>
<span class="qa-anchor" id="q-023-a-17"></span><p>First calculate (new−old+size) modulo size and verify that the resulting advance is legal.</p>
</section>
<section class="qa-section" id="q-023-s-04" data-answer-section="4"><h3><span>4.</span> Check notifications and log records separately</h3>
<span class="qa-anchor" id="q-023-a-09"></span><p>Base §3.3.1.2 specifies an error event for an invalid doorbell value with an outstanding Asynchronous Event Request. An affected SQ may complete consumed commands but consumes no new ones; the host deletes and recreates the queue.</p>
<span class="qa-anchor" id="q-023-a-10"></span><p>Follow the Error event’s indicated log for additional information; the MMIO write itself has no More bit. Do not invent mandatory logging for undefined nonexistent-QID accesses.</p>
</section>
</div>
<span class="qa-anchor" id="q-023-a-08"></span><span class="qa-anchor" id="q-023-a-11"></span><span class="qa-anchor" id="q-023-a-12"></span><span class="qa-anchor" id="q-023-a-13"></span><span class="qa-anchor" id="q-023-a-14"></span><span class="qa-anchor" id="q-023-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-024" data-question="24" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-024">Q24</a> How are SQ/CQ doorbell addresses calculated from CAP.DSTRD?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-024-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-024-a-01">Derive the unique doorbell address from the NVMe register base and QID.</p><div class="qa-sections">
<section class="qa-section" id="q-024-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-024-a-02"></span><p>Offsets are relative to the controller&#x27;s MMIO base, not a queue&#x27;s memory address.</p>
<span class="qa-anchor" id="q-024-a-03"></span><p>PCI BAR0/BAR1 locate the NVMe register space; CAP.DSTRD provides adjacent-doorbell stride.</p>
</section>
<section class="qa-section" id="q-024-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-024-a-04"></span><p>stride=4×2^DSTRD; SQy offset=1000h+2y×stride; CQy offset=1000h+(2y+1)×stride. Each doorbell itself remains 32 bits.</p>
<span class="qa-anchor" id="q-024-a-05"></span><p>Obtain the mapped base, calculate stride, select the SQ/CQ expression for QID, then access with a legal MMIO width.</p>
<span class="qa-anchor" id="q-024-a-06"></span><p>DSTRD=2 and QID=3 give SQ offset 1060h and CQ offset 1070h. Add the controller base for full addresses.</p>
</section>
<section class="qa-section" id="q-024-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-024-a-07"></span><p>Address calculation has no status. A wrong address can select another valid queue or an undefined location; the controller cannot infer host intent.</p>
<span class="qa-anchor" id="q-024-a-16"></span><p>Match results against created QIDs and the mapped BAR range. DSTRD is an exponent, not a byte count or a direct QID multiplier.</p>
</section>
</div>
<span class="qa-anchor" id="q-024-a-17"></span><span class="qa-anchor" id="q-024-a-08"></span><span class="qa-anchor" id="q-024-a-09"></span><span class="qa-anchor" id="q-024-a-10"></span><span class="qa-anchor" id="q-024-a-11"></span><span class="qa-anchor" id="q-024-a-12"></span><span class="qa-anchor" id="q-024-a-13"></span><span class="qa-anchor" id="q-024-a-14"></span><span class="qa-anchor" id="q-024-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-pciconfig">PCIe Transport 1.4 §3.8.1 (NVMe configuration access)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-025" data-question="25" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-025">Q25</a> May the host access doorbells of uncreated/deleted queues or a disabled controller?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-025-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-025-a-01">Respect queue lifetime: an address in the doorbell region does not mean a queue currently exists.</p><div class="qa-sections">
<section class="qa-section" id="q-025-s-01" data-answer-section="1"><h3><span>1.</span> Establish the queue lifetime</h3>
<span class="qa-anchor" id="q-025-a-02"></span><p>Use each queue after successful creation and retire it after successful deletion or controller reset.</p>
<span class="qa-anchor" id="q-025-a-03"></span><p>Check host queue-lifetime records, CC.EN and CSTS.RDY; doorbell readback cannot establish queue existence.</p>
<span class="qa-anchor" id="q-025-a-04"></span><p>SQyTDBL/CQyHDBL announce pointers for valid queues. Admin Q0&#x27;s environment comes from AQA/ASQ/ACQ and initialization.</p>
<span class="qa-anchor" id="q-025-a-05"></span><p>Create successfully, use, stop submissions, successfully delete, then stop all use. Reused QIDs after reset still require reconstruction.</p>
</section>
<section class="qa-section" id="q-025-s-02" data-answer-section="2"><h3><span>2.</span> No fixed response for a nonexistent queue</h3>
<span class="qa-anchor" id="q-025-a-07"></span><p>PCIe §3.1.2 defines writes to nonexistent SQ/CQ doorbells as undefined. RDY=0 violates submission prerequisites. No guaranteed Invalid Queue Identifier or AER follows.</p>
<span class="qa-anchor" id="q-025-a-16"></span><p>Use Create/Delete completion times to establish the valid interval and check doorbell timestamps against it.</p>
</section>
</div>
<span class="qa-anchor" id="q-025-a-06"></span><span class="qa-anchor" id="q-025-a-17"></span><span class="qa-anchor" id="q-025-a-08"></span><span class="qa-anchor" id="q-025-a-09"></span><span class="qa-anchor" id="q-025-a-10"></span><span class="qa-anchor" id="q-025-a-11"></span><span class="qa-anchor" id="q-025-a-12"></span><span class="qa-anchor" id="q-025-a-13"></span><span class="qa-anchor" id="q-025-a-14"></span><span class="qa-anchor" id="q-025-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-qattr">Base 2.4 §3.3.3–3.4.1</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-026" data-question="26" data-answer-kind="process"><h2><a class="qa-qid" href="#q-026">Q26</a> How should SQ Tail and CQ Head wrap around?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-026-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-026-a-01">Reuse fixed storage as a ring without recreating the queue each turn.</p><div class="qa-sections">
<section class="qa-section" id="q-026-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-026-a-02"></span><p>The host advances SQ Tail and CQ Head; the controller maintains SQ Head and CQ Tail.</p>
<span class="qa-anchor" id="q-026-a-03"></span><p>Use the actual N=QSIZE+1 slots, not CAP.MQES as every queue&#x27;s size.</p>
<span class="qa-anchor" id="q-026-a-04"></span><p>Advance with (index+1) modulo N. Tail is the next insertion position, Head the next consumption position; equality means empty.</p>
</section>
<section class="qa-section" id="q-026-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-026-a-05"></span><p>Wrap N−1 to zero while tracking the real count. Do not overfill the SQ or release unconsumed CQ entries.</p>
<span class="qa-anchor" id="q-026-a-06"></span><p>With N=8, CQ Head 7→2 consumes slots 7, 0 and 1: three entries, not a backward movement of five.</p>
</section>
<section class="qa-section" id="q-026-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-026-a-07"></span><p>Valid wrap is not an error. Writing N as an index is out of range; invalid-pointer handling follows Question 23.</p>
<span class="qa-anchor" id="q-026-a-16"></span><p>Validate modulo relationships among Head, Tail and size. A decreasing doorbell value alone is not a violation.</p>
</section>
</div>
<span class="qa-anchor" id="q-026-a-17"></span><span class="qa-anchor" id="q-026-a-08"></span><span class="qa-anchor" id="q-026-a-09"></span><span class="qa-anchor" id="q-026-a-10"></span><span class="qa-anchor" id="q-026-a-11"></span><span class="qa-anchor" id="q-026-a-12"></span><span class="qa-anchor" id="q-026-a-13"></span><span class="qa-anchor" id="q-026-a-14"></span><span class="qa-anchor" id="q-026-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-027" data-question="27" data-answer-kind="process"><h2><a class="qa-qid" href="#q-027">Q27</a> How does the CQ phase change across wrap, and how does the host identify a new completion?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-027-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-027-a-01">Let the host distinguish a newly posted completion from data left in the same slot by a previous pass.</p><div class="qa-sections">
<section class="qa-section" id="q-027-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-027-a-02"></span><p>Phase belongs to the CQ ring lifetime; it is neither CID success/failure nor an SQ pointer.</p>
<span class="qa-anchor" id="q-027-a-03"></span><p>This is a basic PCIe CQE mechanism, not an optional feature. Initialize every slot&#x27;s phase to zero before creation and initially expect one.</p>
<span class="qa-anchor" id="q-027-a-04"></span><p>CQE DW3 bit 16 is P. Each new posting in a slot inverts that slot&#x27;s previous phase.</p>
</section>
<section class="qa-section" id="q-027-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-027-a-05"></span>
<span class="qa-anchor" id="q-027-a-06"></span>
<span class="qa-anchor" id="q-027-a-17"></span>
<figure class="qa-flow" id="q-027-flow"><figcaption>Phase changes per traversal, not per CQE</figcaption>
<p>Assume a four-entry CQ; the host initially expects P=1.</p><ol class="qa-flow-steps">
<li class="qa-flow-step"><strong>Inspect P at the current head</strong><p>If P does not match, wait: the slot has no new result for this traversal. Do not decode its stale CID or status.</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>P matches → process the CQE</strong><p>Head visits 0, 1, 2 and 3. New CQEs in this traversal all use P=1.</p></li>
<li class="qa-flow-step"><span class="qa-flow-arrow" aria-hidden="true">↓</span><strong>Head wraps from 3 to 0 → invert expected phase</strong><p>Expect P=0 in the next traversal. Moving from slot 1 to 2 does not change the expected phase.</p></li>
</ol><p class="qa-flow-conclusion">Recreating the CQ requires reinitializing phase bits and the host expectation. Four entries are used only to illustrate wrapping.</p></figure>
</section>
<section class="qa-section" id="q-027-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-027-a-07"></span><p>A phase mismatch means no new completion at that position, not an error status. Do not decode stale CID/SC as a new result.</p>
<span class="qa-anchor" id="q-027-a-16"></span><p>Exercise at least one wrap and compare Head, expected P and actual P. Reinitialize after queue recreation rather than inheriting the old phase.</p>
</section>
</div>
<span class="qa-anchor" id="q-027-a-08"></span><span class="qa-anchor" id="q-027-a-09"></span><span class="qa-anchor" id="q-027-a-10"></span><span class="qa-anchor" id="q-027-a-11"></span><span class="qa-anchor" id="q-027-a-12"></span><span class="qa-anchor" id="q-027-a-13"></span><span class="qa-anchor" id="q-027-a-14"></span><span class="qa-anchor" id="q-027-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-028" data-question="28" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-028">Q28</a> How does CQ Full arise, and may related SQ processing continue?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-028-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-028-a-01">Flow control prevents overwriting unconsumed completions. Fullness usually means completions arrive faster than the host releases slots.</p><div class="qa-sections">
<section class="qa-section" id="q-028-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-028-a-02"></span><p>It affects the CQ and associated SQs. Processing must continue for SQs not associated with that full CQ.</p>
<span class="qa-anchor" id="q-028-a-04"></span><p>Full means (Tail+1) modulo N = Head, leaving one slot unused. Tail is controller-internal, not directly readable by the host.</p>
</section>
<section class="qa-section" id="q-028-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-028-a-03"></span><p>Inspect actual CQ size, Head updates and pending completions, not Number of Queues.</p>
<span class="qa-anchor" id="q-028-a-05"></span><p>The host validates phases, processes results and advances Head. The controller shall not post another completion to this CQ until a slot is available.</p>
<span class="qa-anchor" id="q-028-a-06"></span><p>The controller may stop processing further associated SQ entries. This does not require all consumed commands either to stop instantly or to continue unconditionally.</p>
</section>
<section class="qa-section" id="q-028-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-028-a-07"></span><p>CQ Full is a capacity state, not a required error status. Overwriting unacknowledged entries to make room violates correctness.</p>
<span class="qa-anchor" id="q-028-a-16"></span><p>If only its associated SQs stall, inspect consumption first. If independent SQs stop because of this full CQ, check the requirement to continue their processing.</p>
</section>
</div>
<span class="qa-anchor" id="q-028-a-17"></span><span class="qa-anchor" id="q-028-a-08"></span><span class="qa-anchor" id="q-028-a-09"></span><span class="qa-anchor" id="q-028-a-10"></span><span class="qa-anchor" id="q-028-a-11"></span><span class="qa-anchor" id="q-028-a-12"></span><span class="qa-anchor" id="q-028-a-13"></span><span class="qa-anchor" id="q-028-a-14"></span><span class="qa-anchor" id="q-028-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-029" data-question="29" data-answer-kind="process"><h2><a class="qa-qid" href="#q-029">Q29</a> How does processing resume when the host releases CQ space?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-029-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-029-a-01">Resume work after capacity becomes available rather than treating ordinary CQ Full as a recreation error.</p><div class="qa-sections">
<section class="qa-section" id="q-029-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-029-a-02"></span><p>Released slots serve completions from associated SQs; queue allocations and namespace capabilities do not change.</p>
<span class="qa-anchor" id="q-029-a-03"></span><p>Verify a live queue and no independent stop condition such as reset, CFS or Processing Paused.</p>
<span class="qa-anchor" id="q-029-a-04"></span><p>The host writes the new CQ Head, allowing the controller to reuse released slots with correct phases for subsequent completions.</p>
</section>
<section class="qa-section" id="q-029-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-029-a-05"></span><p>Consume CQEs, update Head, allow slots to become available, then post waiting completions and continue affected work under normal scheduling and other constraints.</p>
<span class="qa-anchor" id="q-029-a-06"></span><p>Released slots are reusable without recreation. There is no universal fixed latency from a Head update to the next CQE.</p>
</section>
<section class="qa-section" id="q-029-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-029-a-07"></span><p>Correct release has no special success CQE. An invalid Head remains a doorbell-usage issue, not a Create Queue error.</p>
<span class="qa-anchor" id="q-029-a-16"></span><p>Verify legal reuse of released slots and compare progress on associated and independent SQs.</p>
</section>
</div>
<span class="qa-anchor" id="q-029-a-17"></span><span class="qa-anchor" id="q-029-a-08"></span><span class="qa-anchor" id="q-029-a-09"></span><span class="qa-anchor" id="q-029-a-10"></span><span class="qa-anchor" id="q-029-a-11"></span><span class="qa-anchor" id="q-029-a-12"></span><span class="qa-anchor" id="q-029-a-13"></span><span class="qa-anchor" id="q-029-a-14"></span><span class="qa-anchor" id="q-029-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-030" data-question="30" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-030">Q30</a> How does the host identify completions from SQs sharing a CQ?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-030-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-030-a-01">Deliver completion to the correct request. CID uniqueness is required among outstanding commands of the same SQ.</p><div class="qa-sections">
<section class="qa-section" id="q-030-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-030-a-02"></span><p>Matching includes controller, SQ lifetime, SQID and CID. Controller/lifetime are host context, not additional CQE fields.</p>
<span class="qa-anchor" id="q-030-a-03"></span><p>Use the creation-time SQ-to-CQ map and outstanding table, not Identify for per-command locations.</p>
</section>
<section class="qa-section" id="q-030-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-030-a-04"></span><p>SQID identifies the SQ and CID its command. SQHD reports consumption progress, not the original slot of that command.</p>
<span class="qa-anchor" id="q-030-a-05"></span><p>Validate phase first, match SQID/CID, process status/data, update that SQ&#x27;s head information, then release the CQ slot.</p>
<span class="qa-anchor" id="q-030-a-06"></span><p>SQ1/CID 9 and SQ2/CID 9 are matched correctly even if they complete in reverse order.</p>
</section>
<section class="qa-section" id="q-030-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-030-a-07"></span><p>Reusing an outstanding CID in one SQ may return Command ID Conflict (0/03h). The conflict-search extent is implementation-specific; host uniqueness obligations remain.</p>
<span class="qa-anchor" id="q-030-a-16"></span><p>Check that SQID is associated with this CQ and CID belongs to its current queue lifetime.</p>
</section>
</div>
<span class="qa-anchor" id="q-030-a-17"></span><span class="qa-anchor" id="q-030-a-08"></span><span class="qa-anchor" id="q-030-a-09"></span><span class="qa-anchor" id="q-030-a-10"></span><span class="qa-anchor" id="q-030-a-11"></span><span class="qa-anchor" id="q-030-a-12"></span><span class="qa-anchor" id="q-030-a-13"></span><span class="qa-anchor" id="q-030-a-14"></span><span class="qa-anchor" id="q-030-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>

<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-cap"><strong>Base 2.4 · §3.1.4 (CAP, VS)</strong><br>Printed pages 54–59 · PDF 80–85 · Figure 36–37</li>
<li id="ref-queue"><strong>Base 2.4 · §3.3.1</strong><br>Printed pages 88–91 · PDF 114–117 · Figure 73–74</li>
<li id="ref-order"><strong>Base 2.4 · §3.4.1–3.4.5</strong><br>Printed pages 101–105 · PDF 127–131 · Figure 80–81</li>
<li id="ref-qattr"><strong>Base 2.4 · §3.3.3–3.4.1</strong><br>Printed pages 101 · PDF 127</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-sqe"><strong>Base 2.4 · §4.1.1</strong><br>Printed pages 139–142 · PDF 165–168 · Figure 92–93</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>Printed pages 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-delete"><strong>Base 2.4 · §5.3.3–5.3.4</strong><br>Printed pages 531–532 · PDF 557–558 · Figure 580–583</li>
<li id="ref-fatal"><strong>Base 2.4 · §9.1–9.6.1</strong><br>Printed pages 825–826 · PDF 851–852</li>
<li id="ref-pcie"><strong>PCIe Transport 1.4 · §3.1–3.4</strong><br>Printed pages 9–13 · PDF 9–13 · Figure 3–8</li>
<li id="ref-pciconfig"><strong>PCIe Transport 1.4 · §3.8.1 (NVMe configuration access)</strong><br>Printed pages 16–18 · PDF 16–18 · Figure 10–17</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/doorbells/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/doorbells.html">Chinese tutorial HTML</a></nav>
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
