---
layout: post
title: "NVMe Self-Study Bank: Error status and Error Information"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/errors/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/errors/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/errors.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q93–Q106</p><h1>Error status and Error Information</h1><p class="qr-intro">Start with one failed command, classify it and correlate completion with supplemental records and recovery evidence.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Three different kinds of evidence</h2><p class="qa-takeaway">Establish command identity before comparing records.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Evidence</th><th scope="col">What it establishes</th><th scope="col">What it does not prove</th></tr></thead><tbody><tr><td>CQE</td><td>Command completion result</td><td>All media effects were undone</td></tr><tr><td>Error Information</td><td>Additional failure detail</td><td>One entry for every failed command</td></tr><tr><td>PEL</td><td>Supported persistent events</td><td>A complete command trace</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>A request with both bad NSID and PRP may expose either fault first. Isolate NSID to test its required status.</p>
<p class="qa-citations">Sources: <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pelcontext">Base 2.4 §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-093">Q93 · How do opcode, field, CID and sequence errors differ?</a></li>
<li><a href="#q-094">Q94 · How are namespace, log, queue, size and vector errors located?</a></li>
<li><a href="#q-095">Q95 · Why must firmware, format and capacity errors be tied to their commands?</a></li>
<li><a href="#q-096">Q96 · How do transfer, internal and namespace-readiness errors differ?</a></li>
<li><a href="#q-097">Q97 · How do power loss, abort, SQ deletion and fused failures appear?</a></li>
<li><a href="#q-098">Q98 · How do status, More, DNR and CRD guide recovery?</a></li>
<li><a href="#q-099">Q99 · Which errors require Error Information?</a></li>
<li><a href="#q-100">Q100 · How is an error entry correlated with its command and parameter?</a></li>
<li><a href="#q-101">Q101 · Must an error entry match every CQE status bit?</a></li>
<li><a href="#q-102">Q102 · How do concurrent errors, log capacity and Error Count interact?</a></li>
<li><a href="#q-103">Q103 · Is a non-success CQE without a new error entry always nonconforming?</a></li>
<li><a href="#q-104">Q104 · Can other commands continue after an ordinary command error?</a></li>
<li><a href="#q-105">Q105 · When may serious failures set CFS, and how should the host interpret it?</a></li>
<li><a href="#q-106">Q106 · How are CQEs, Error Information and persistent events correlated?</a></li>
</ol></section>
<article class="qa-question" id="q-093" data-question="93" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-093">Q93</a> How do opcode, field, CID and sequence errors differ?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-093-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-093-a-01">Classify the failure before changing command encoding or host bookkeeping. An unsupported opcode differs from reusing an outstanding CID in the same SQ.</p><div class="qa-sections">
<section class="qa-section" id="q-093-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-093-a-02"></span><p>Status describes the identified command. A parameter error does not establish queue-wide or controller-wide failure.</p>
<span class="qa-anchor" id="q-093-a-04"></span><p>For SCT=0, SC 01h is Invalid Command Opcode, 02h Invalid Field, 03h CID Conflict and 0Ch Command Sequence Error. CID uniqueness applies to outstanding commands within one SQ.</p>
</section>
<section class="qa-section" id="q-093-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-093-a-03"></span><p>Check opcode support using Identify and Commands Supported and Effects, then command fields and sequence requirements. CID reuse requires the host outstanding list.</p>
<span class="qa-anchor" id="q-093-a-05"></span><p>Preserve the SQE, establish command set and support, inspect fields, then reconstruct sequencing. Change one identified defect at a time.</p>
<span class="qa-anchor" id="q-093-a-06"></span><p>A valid, successfully executed command returns success; a negative test passes by returning the applicable error, not by succeeding.</p>
</section>
<section class="qa-section" id="q-093-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-093-a-07"></span><p>Use Invalid Field unless a more specific status is specified. For multiple simultaneous faults, status selection is vendor-defined unless priority is specified; CID-conflict search depth is implementation-specific.</p>
<span class="qa-anchor" id="q-093-a-16"></span><p>Correlate support, SQE and CQE. A command with both an invalid opcode and invalid NSID does not isolate an exact-status test.</p>
</section>
</div>
<span class="qa-anchor" id="q-093-a-17"></span><span class="qa-anchor" id="q-093-a-08"></span><span class="qa-anchor" id="q-093-a-09"></span><span class="qa-anchor" id="q-093-a-10"></span><span class="qa-anchor" id="q-093-a-11"></span><span class="qa-anchor" id="q-093-a-12"></span><span class="qa-anchor" id="q-093-a-13"></span><span class="qa-anchor" id="q-093-a-14"></span><span class="qa-anchor" id="q-093-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-094" data-question="94" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-094">Q94</a> How are namespace, log, queue, size and vector errors located?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-094-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-094-a-01">These errors concern different identified objects. Determine what the command addresses before testing existence, range and applicability.</p><div class="qa-sections">
<section class="qa-section" id="q-094-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-094-a-02"></span><p>NSID, LID and QID identify different objects; QSIZE encodes depth and IV selects a vector. Their numerical ranges are unrelated.</p>
<span class="qa-anchor" id="q-094-a-04"></span><p>Typical SCT/SC pairs are namespace 0/0Bh, log 1/09h, queue ID 1/01h, queue size 1/02h and vector 1/08h. Invalid CQID in Create SQ uses Completion Queue Invalid 1/00h.</p>
</section>
<section class="qa-section" id="q-094-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-094-a-03"></span><p>Snapshot namespace lists, Supported Log Pages, CAP.MQES, Number of Queues and available interrupt resources.</p>
<span class="qa-anchor" id="q-094-a-05"></span><p>Start with a valid command and alter only the tested field. A size test should keep QID, address and vector valid.</p>
<span class="qa-anchor" id="q-094-a-06"></span><p>Only successful creation establishes a queue. After a negative test, ensure no usable partial queue configuration was left behind.</p>
</section>
<section class="qa-section" id="q-094-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-094-a-07"></span><p>Apply codes to their defined commands and conditions. An inappropriate NSID in Get Log may require Invalid Field under the log-scope rules, not universally Invalid Namespace.</p>
<span class="qa-anchor" id="q-094-a-16"></span><p>Compare the command-specific completion definition with the configuration at submission time.</p>
</section>
</div>
<span class="qa-anchor" id="q-094-a-17"></span><span class="qa-anchor" id="q-094-a-08"></span><span class="qa-anchor" id="q-094-a-09"></span><span class="qa-anchor" id="q-094-a-10"></span><span class="qa-anchor" id="q-094-a-11"></span><span class="qa-anchor" id="q-094-a-12"></span><span class="qa-anchor" id="q-094-a-13"></span><span class="qa-anchor" id="q-094-a-14"></span><span class="qa-anchor" id="q-094-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-create">Base 2.4 §5.3.1–5.3.2</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-getlog">Base 2.4 §5.2.13–5.2.13.1.1</a> · <a href="#ref-nsid">Base 2.4 §3.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-095" data-question="95" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-095">Q95</a> Why must firmware, format and capacity errors be tied to their commands?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-095-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-095-a-01">Distinguish image, format and resource problems. Correcting a firmware slot cannot fix insufficient namespace allocation capacity.</p><div class="qa-sections">
<section class="qa-section" id="q-095-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-095-a-02"></span><p>Firmware Commit concerns images and activation; Format concerns namespace format; Namespace and Capacity Management manage different resource levels.</p>
<span class="qa-anchor" id="q-095-a-04"></span><p>Codes are firmware slot 1/06h, image 1/07h and format 1/0Ah. Namespace Insufficient Capacity is 1/15h, Capacity Management Insufficient Capacity 1/26h and generic Capacity Exceeded 0/81h.</p>
</section>
<section class="qa-section" id="q-095-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-095-a-03"></span><p>Check FRMW, Firmware Slot Information, supported LBA formats, total/unallocated capacity and command scope.</p>
<span class="qa-anchor" id="q-095-a-05"></span><p>Identify the opcode and its error conditions, then calculate requested bytes, logical blocks or allocation units consistently.</p>
<span class="qa-anchor" id="q-095-a-06"></span><p>Positive tests establish the operation’s completion; negative tests establish rejection and the command-defined disposition of existing configuration.</p>
</section>
<section class="qa-section" id="q-095-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-095-a-07"></span><p>These capacity codes are not interchangeable. Firmware Activation Requires Reset can indicate an additional activation step rather than an invalid image.</p>
<span class="qa-anchor" id="q-095-a-16"></span><p>Compare pre/post Identify and logs and retain SCT with SC; SC alone loses its category.</p>
</section>
</div>
<span class="qa-anchor" id="q-095-a-17"></span><span class="qa-anchor" id="q-095-a-08"></span><span class="qa-anchor" id="q-095-a-09"></span><span class="qa-anchor" id="q-095-a-10"></span><span class="qa-anchor" id="q-095-a-11"></span><span class="qa-anchor" id="q-095-a-12"></span><span class="qa-anchor" id="q-095-a-13"></span><span class="qa-anchor" id="q-095-a-14"></span><span class="qa-anchor" id="q-095-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-nsmanage">Base 2.4 §5.2.24–5.2.25, 8.1.17</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-096" data-question="96" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-096">Q96</a> How do transfer, internal and namespace-readiness errors differ?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-096-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-096-a-01">These identify data movement, internal processing and namespace accessibility, requiring different recovery actions.</p><div class="qa-sections">
<section class="qa-section" id="q-096-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-096-a-02"></span><p>Transfer/internal errors describe a command; readiness concerns the selected namespace. None alone proves destruction of all namespaces.</p>
<span class="qa-anchor" id="q-096-a-04"></span><p>Codes are 0/04h, 0/06h and 0/82h. Admin Command Media Not Ready, 0/24h, has separate CRIME and timing conditions.</p>
</section>
<section class="qa-section" id="q-096-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-096-a-03"></span><p>Preserve pointers, host memory mappings, CSTS and namespace state; read Error Information when applicable. Ready mode and CFS provide distinct evidence.</p>
<span class="qa-anchor" id="q-096-a-05"></span><p>Preserve the CQE, check buffer addresses and lifetime, then logs, CSTS and namespace state. Do not treat failed-read data as a valid result.</p>
<span class="qa-anchor" id="q-096-a-06"></span><p>A successful command after recovery establishes its result; RDY=1 alone does not establish immediate access to every namespace.</p>
</section>
<section class="qa-section" id="q-096-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-096-a-07"></span><p>Namespace Not Ready does not replace defined ANA statuses. Internal Error does not universally require CFS=1.</p>
<span class="qa-anchor" id="q-096-a-16"></span><p>Valid pointers do not rule out internal errors, and temporary namespace unavailability does not imply an unsupported opcode.</p>
</section>
<section class="qa-section" id="q-096-s-04" data-answer-section="4"><h3><span>4.</span> Asynchronous Event notification conditions</h3>
<span class="qa-anchor" id="q-096-a-09"></span><p>Internal Error details should be reported through an appropriate error AER; transfer or readiness errors do not universally require that same event. Distinguish occurrence, reporting conditions and available requests.</p>
</section>
</div>
<span class="qa-anchor" id="q-096-a-17"></span><span class="qa-anchor" id="q-096-a-08"></span><span class="qa-anchor" id="q-096-a-10"></span><span class="qa-anchor" id="q-096-a-11"></span><span class="qa-anchor" id="q-096-a-12"></span><span class="qa-anchor" id="q-096-a-13"></span><span class="qa-anchor" id="q-096-a-14"></span><span class="qa-anchor" id="q-096-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-ready">Base 2.4 §3.5.3–3.5.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-097" data-question="97" data-answer-kind="error"><h2><a class="qa-qid" href="#q-097">Q97</a> How do power loss, abort, SQ deletion and fused failures appear?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-097-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-097-a-01">Abort cause determines status and whether a completion can be expected. Sudden power loss or reset can remove the completion channel.</p><div class="qa-sections">
<section class="qa-section" id="q-097-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-097-a-02"></span><p>Abort targets one command, SQ deletion covers its outstanding commands and fused failure affects the pair; power and reset can have broader scope.</p>
<span class="qa-anchor" id="q-097-a-04"></span><p>Target-command codes are power-loss notification 0/05h, abort requested 0/07h, SQ deletion 0/08h, failed fused 0/09h and missing fused 0/0Ah.</p>
<span class="qa-anchor" id="q-097-a-07"></span><p>A power-loss-notification status does not mean every power removal produces CQEs. A missing fused partner differs from a partner that failed.</p>
</section>
<section class="qa-section" id="q-097-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-097-a-03"></span><p>Preserve target IDs, Abort/Delete completions, CC/CSTS and FUSE encoding to reconstruct the cause.</p>
<span class="qa-anchor" id="q-097-a-05"></span><p>Establish queue validity before consuming target completions. After reset, rebuild queues and tracking; handle Abort and target CQEs separately.</p>
</section>
<section class="qa-section" id="q-097-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-097-a-06"></span><p>Correct cancellation does not require target success. Verify one target completion, or abandon old completion expectations under reset rules.</p>
<span class="qa-anchor" id="q-097-a-16"></span><p>Correlate target, management completions and queue/power transitions by time rather than using one final status for the entire sequence.</p>
<span class="qa-anchor" id="q-097-a-17"></span><p>First distinguish an actual power-loss notification from abrupt loss of power, since completion expectations differ.</p>
</section>
</div>
<span class="qa-anchor" id="q-097-a-08"></span><span class="qa-anchor" id="q-097-a-09"></span><span class="qa-anchor" id="q-097-a-10"></span><span class="qa-anchor" id="q-097-a-11"></span><span class="qa-anchor" id="q-097-a-12"></span><span class="qa-anchor" id="q-097-a-13"></span><span class="qa-anchor" id="q-097-a-14"></span><span class="qa-anchor" id="q-097-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-098" data-question="98" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-098">Q98</a> How do status, More, DNR and CRD guide recovery?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-098-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-098-a-01">Diagnose before retrying. DNR=0 permits the possibility of success, not unlimited immediate retries or assumptions about partial effects.</p><div class="qa-sections">
<section class="qa-section" id="q-098-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-098-a-02"></span><p>These fields describe one completion; Abort, queue deletion and reset have broader scopes and depend on failure severity and channel availability.</p>
<span class="qa-anchor" id="q-098-a-03"></span><p>Use SCT/SC, M, DNR and CRD with ACRE and CRDT1–3; M=1 points to additional Error Information.</p>
<span class="qa-anchor" id="q-098-a-04"></span><p>With ACRE=1 and DNR=0, CRD selects CRDT1–3 or zero extra delay. CRD is reserved when DNR=1 or ACRE=0.</p>
</section>
<section class="qa-section" id="q-098-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-098-a-17"></span><p>First check whether the test incorrectly interprets DNR=0 as a guarantee of immediate retry success.</p>
<span class="qa-anchor" id="q-098-a-05"></span><p>Decode the error and additional information, correct parameters or wait for state, then assess retry safety. Recover queues or the controller when their channels are compromised.</p>
</section>
<section class="qa-section" id="q-098-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-098-a-06"></span><p>Successful recovery needs a valid new result and control over old-command effects; retry success alone does not rule out duplicate writes.</p>
<span class="qa-anchor" id="q-098-a-07"></span><p>Command Interrupted 0/21h requires ACRE=1 and DNR=0. Format In Progress also requires DNR=0; other names do not establish a universal DNR value.</p>
<span class="qa-anchor" id="q-098-a-16"></span><p>Compare retry timing with CRD/CRDT. Waiting at least the indicated delay is recommended, but an earlier retry is not itself an error.</p>
</section>
</div>
<span class="qa-anchor" id="q-098-a-08"></span><span class="qa-anchor" id="q-098-a-09"></span><span class="qa-anchor" id="q-098-a-10"></span><span class="qa-anchor" id="q-098-a-11"></span><span class="qa-anchor" id="q-098-a-12"></span><span class="qa-anchor" id="q-098-a-13"></span><span class="qa-anchor" id="q-098-a-14"></span><span class="qa-anchor" id="q-098-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-behavior">Base 2.4 §5.2.30.1.15</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-099" data-question="99" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-099">Q99</a> Which errors require Error Information?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-099-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-099-a-01">Error Information extends CQEs and can describe non-command errors; it is not a mandatory transaction ledger of every failed command.</p><div class="qa-sections">
<section class="qa-section" id="q-099-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-099-a-02"></span><p>LID 01h is controller-wide; SQID/CID validity determines whether an entry is command-specific.</p>
<span class="qa-anchor" id="q-099-a-04"></span><p>Read LID 01h and retain ECNT, SQID, CID, STS, Parameter Error Location, NSID and LPVER.</p>
</section>
<section class="qa-section" id="q-099-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-099-a-03"></span><p>ELPE determines entry capacity; CQE.M identifies additional command information, and error AERs can also lead to this log.</p>
<span class="qa-anchor" id="q-099-a-05"></span><p>After an error with M=1, promptly preserve enough entries rather than assuming the newest entry is the target.</p>
<span class="qa-anchor" id="q-099-a-06"></span><p>Success is a correlated explanatory entry; SQID/CID=FFFFh can be correct for a non-command-specific error.</p>
</section>
<section class="qa-section" id="q-099-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-099-a-07"></span><p>M=0 does not mandate an entry for every Invalid Field. For M=1 with missing information, exclude overwrite, reset clearing and querying the wrong controller.</p>
<span class="qa-anchor" id="q-099-a-16"></span><p>Validate correlation among M, error AERs and entries rather than requiring failure count to equal entry count.</p>
</section>
<section class="qa-section" id="q-099-s-04" data-answer-section="4"><h3><span>4.</span> Evidence supplied by the log</h3>
<span class="qa-anchor" id="q-099-a-10"></span><p>A successful CQE does not require a new Error Information entry. <a class="qa-rule-link" href="#common-command-10">Read the complete conditions in this volume</a></p>
</section>
</div>
<span class="qa-anchor" id="q-099-a-17"></span><span class="qa-anchor" id="q-099-a-08"></span><span class="qa-anchor" id="q-099-a-09"></span><span class="qa-anchor" id="q-099-a-11"></span><span class="qa-anchor" id="q-099-a-12"></span><span class="qa-anchor" id="q-099-a-13"></span><span class="qa-anchor" id="q-099-a-14"></span><span class="qa-anchor" id="q-099-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-100" data-question="100" data-answer-kind="fields"><h2><a class="qa-qid" href="#q-100">Q100</a> How is an error entry correlated with its command and parameter?</h2>
<p class="qa-prompt">Explain the units and encoding, then work through one set of values.</p>
<details class="qa-answer" id="q-100-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-100-a-01">Correlation turns a reported parameter fault into inspectable original bytes; a status name alone rarely locates the actual encoding mistake.</p><div class="qa-sections">
<section class="qa-section" id="q-100-s-01" data-answer-section="1"><h3><span>1.</span> Establish the source and scope</h3>
<span class="qa-anchor" id="q-100-a-02"></span><p>SQID+CID identifies a command within one queue lifetime; reuse requires ECNT, timing and a submission snapshot.</p>
<span class="qa-anchor" id="q-100-a-03"></span><p>Check LPVER, which is 1 in Base 2.4; CSI/OPC are valid for LPVER≥1.</p>
</section>
<section class="qa-section" id="q-100-s-02" data-answer-section="2"><h3><span>2.</span> Fields, units and worked interpretation</h3>
<span class="qa-anchor" id="q-100-a-04"></span><p>Parameter Error Location bits 7:0 give SQE byte offset and bits 10:8 the bit within it; multi-bit/byte fields use their least-significant position. This PEL abbreviation differs from Persistent Event Log.</p>
<span class="qa-anchor" id="q-100-a-05"></span><p>Establish queue lifetime, match IDs/opcode/namespace, then decode the original SQE at the reported byte and bit.</p>
<span class="qa-anchor" id="q-100-a-06"></span><p>A successful correlation identifies the submitted value and violated condition, enabling a one-field correction test.</p>
</section>
<section class="qa-section" id="q-100-s-03" data-answer-section="3"><h3><span>3.</span> Conditions that change the interpretation</h3>
<span class="qa-anchor" id="q-100-a-07"></span><p>Non-command-specific errors use FFFFh for SQID, CID and Parameter Error Location; do not use it as a command-memory offset.</p>
<span class="qa-anchor" id="q-100-a-16"></span><p>Interpret LBA/CSINFO only after identifying namespace and command set; not every error carries a failing LBA.</p>
</section>
</div>
<span class="qa-anchor" id="q-100-a-17"></span><span class="qa-anchor" id="q-100-a-08"></span><span class="qa-anchor" id="q-100-a-09"></span><span class="qa-anchor" id="q-100-a-10"></span><span class="qa-anchor" id="q-100-a-11"></span><span class="qa-anchor" id="q-100-a-12"></span><span class="qa-anchor" id="q-100-a-13"></span><span class="qa-anchor" id="q-100-a-14"></span><span class="qa-anchor" id="q-100-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-101" data-question="101" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-101">Q101</a> Must an error entry match every CQE status bit?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-101-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-101-a-01">Separate command status from phase; comparing the entire word can reject a valid entry.</p><div class="qa-sections">
<section class="qa-section" id="q-101-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-101-a-02"></span><p>Compare matched command-specific records; non-command errors have no originating CQE for exact comparison.</p>
<span class="qa-anchor" id="q-101-a-04"></span><p>Error STS bits 15:1 contain command status; bit 0 may indicate the CQE phase. Normalize their different placements before comparison.</p>
</section>
<section class="qa-section" id="q-101-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-101-a-03"></span><p>Decode Figure 212 STS and Figure 101 status rather than assuming an OS-transformed numeric representation.</p>
<span class="qa-anchor" id="q-101-a-05"></span><p>Preserve raw data, extract status components and handle phase separately, confirming ECNT and command IDs.</p>
<span class="qa-anchor" id="q-101-a-06"></span><p>Matched command status should agree; phase follows its optional-reporting definition rather than requiring identical raw words.</p>
</section>
<section class="qa-section" id="q-101-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-101-a-07"></span><p>Non-command errors use the most applicable status; absence of a CQE is not itself a defect. For multiple faults compare the selected completion status.</p>
<span class="qa-anchor" id="q-101-a-16"></span><p>Check decoder shifts for SC, SCT and phase; a parser defect can make every entry appear inconsistent.</p>
</section>
</div>
<span class="qa-anchor" id="q-101-a-17"></span><span class="qa-anchor" id="q-101-a-08"></span><span class="qa-anchor" id="q-101-a-09"></span><span class="qa-anchor" id="q-101-a-10"></span><span class="qa-anchor" id="q-101-a-11"></span><span class="qa-anchor" id="q-101-a-12"></span><span class="qa-anchor" id="q-101-a-13"></span><span class="qa-anchor" id="q-101-a-14"></span><span class="qa-anchor" id="q-101-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-102" data-question="102" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-102">Q102</a> How do concurrent errors, log capacity and Error Count interact?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-102-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-102-a-01">Error Count identifies records while capacity limits visible history; a small log can contain large cumulative identifiers.</p><div class="qa-sections">
<section class="qa-section" id="q-102-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-102-a-02"></span><p>Capacity and ordering are per-controller Error Information, not separate identical arrays for every namespace.</p>
<span class="qa-anchor" id="q-102-a-04"></span><p>ECNT is 64-bit and begins at one; zero marks an invalid entry. Incrementing the maximum wraps to one, not zero.</p>
</section>
<section class="qa-section" id="q-102-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-102-a-03"></span><p>ELPE is zero-based: ELPE=3 means at most four 64-byte entries.</p>
<span class="qa-anchor" id="q-102-a-05"></span><p>Read newest first. When full, the controller should insert the new entry and discard the oldest; retain ECNT across samples to detect updates.</p>
<span class="qa-anchor" id="q-102-a-06"></span><p>With capacity four and latest count nine, entries 9,8,7,6 can be visible; absence of 1–5 does not mean they never occurred.</p>
</section>
<section class="qa-section" id="q-102-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-102-a-07"></span><p>Zero is not a zeroth error. Gaps require considering updates and removed records before diagnosing corruption.</p>
<span class="qa-anchor" id="q-102-a-16"></span><p>Distinguish the SMART cumulative entry count from current log occupancy; they need not be equal.</p>
</section>
</div>
<span class="qa-anchor" id="q-102-a-17"></span><span class="qa-anchor" id="q-102-a-08"></span><span class="qa-anchor" id="q-102-a-09"></span><span class="qa-anchor" id="q-102-a-10"></span><span class="qa-anchor" id="q-102-a-11"></span><span class="qa-anchor" id="q-102-a-12"></span><span class="qa-anchor" id="q-102-a-13"></span><span class="qa-anchor" id="q-102-a-14"></span><span class="qa-anchor" id="q-102-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-103" data-question="103" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-103">Q103</a> Is a non-success CQE without a new error entry always nonconforming?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-103-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-103-a-01">This tests sufficiency of evidence: command failure and required additional error information are separate requirements.</p><div class="qa-sections">
<section class="qa-section" id="q-103-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-103-a-02"></span><p>Evaluate this command and its logging conditions; an unrelated new entry does not satisfy its evidence requirement.</p>
<span class="qa-anchor" id="q-103-a-04"></span><p>More is central: M=1 identifies additional information for this command. Error AERs and particular command rules may impose further requirements.</p>
</section>
<section class="qa-section" id="q-103-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-103-a-03"></span><p>Preserve M, SCT/SC, ECNT before/after, ELPE and reset timing.</p>
<span class="qa-anchor" id="q-103-a-05"></span><p>Establish the logging requirement, exclude wrong controller, short read, overwrite and reset clearing, then evaluate missing required information.</p>
<span class="qa-anchor" id="q-103-a-06"></span><p>A valid result may be that no entry is required or that required information exists. Compliance does not require every failure to increment Error Count.</p>
</section>
<section class="qa-section" id="q-103-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-103-a-07"></span><p>Unexplained missing information for M=1 is a concrete inconsistency; M=0 without an additional rule does not establish the same defect.</p>
<span class="qa-anchor" id="q-103-a-16"></span><p>Attach the requirement, original CQE and log snapshots rather than only stating that no entry was seen.</p>
</section>
<section class="qa-section" id="q-103-s-04" data-answer-section="4"><h3><span>4.</span> Evidence supplied by the log</h3>
<span class="qa-anchor" id="q-103-a-10"></span><p>A successful CQE does not require a new Error Information entry. <a class="qa-rule-link" href="#common-command-10">Read the complete conditions in this volume</a></p>
</section>
</div>
<span class="qa-anchor" id="q-103-a-17"></span><span class="qa-anchor" id="q-103-a-08"></span><span class="qa-anchor" id="q-103-a-09"></span><span class="qa-anchor" id="q-103-a-11"></span><span class="qa-anchor" id="q-103-a-12"></span><span class="qa-anchor" id="q-103-a-13"></span><span class="qa-anchor" id="q-103-a-14"></span><span class="qa-anchor" id="q-103-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-104" data-question="104" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-104">Q104</a> Can other commands continue after an ordinary command error?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-104-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-104-a-01">Most command errors do not compromise queues, so recovery can remain local instead of aborting unrelated work.</p><div class="qa-sections">
<section class="qa-section" id="q-104-s-01" data-answer-section="1"><h3><span>1.</span> Mechanism and scope</h3>
<span class="qa-anchor" id="q-104-a-02"></span><p>Distinguish command, queue and controller failures, widening recovery only with broader evidence.</p>
<span class="qa-anchor" id="q-104-a-04"></span><p>Base 9.1 recommends continued processing for most command errors and queue recreation for serious queue failures.</p>
</section>
<section class="qa-section" id="q-104-s-02" data-answer-section="2"><h3><span>2.</span> Understand it through actions and results</h3>
<span class="qa-anchor" id="q-104-a-03"></span><p>Inspect CQEs, CFS, queue pointers and continued completion of other commands, with Error Information for context.</p>
<span class="qa-anchor" id="q-104-a-05"></span><p>Preserve the failed command and continue valid work if queues remain sound; stop and recover damaged queues in dependency order.</p>
<span class="qa-anchor" id="q-104-a-06"></span><p>Later valid commands can succeed while the earlier failure remains a distinct result.</p>
</section>
<section class="qa-section" id="q-104-s-03" data-answer-section="3"><h3><span>3.</span> Avoid a misleading conclusion</h3>
<span class="qa-anchor" id="q-104-a-07"></span><p>Serious Admin-channel failure or an uncompleted queue deletion calls for Controller Level Reset, unlike ordinary Invalid Field.</p>
<span class="qa-anchor" id="q-104-a-16"></span><p>Observe commands in the same SQ, shared CQ and other CQs to distinguish congestion from a global processing stop.</p>
</section>
</div>
<span class="qa-anchor" id="q-104-a-17"></span><span class="qa-anchor" id="q-104-a-08"></span><span class="qa-anchor" id="q-104-a-09"></span><span class="qa-anchor" id="q-104-a-10"></span><span class="qa-anchor" id="q-104-a-11"></span><span class="qa-anchor" id="q-104-a-12"></span><span class="qa-anchor" id="q-104-a-13"></span><span class="qa-anchor" id="q-104-a-14"></span><span class="qa-anchor" id="q-104-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-delete">Base 2.4 §5.3.3–5.3.4</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-105" data-question="105" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-105">Q105</a> When may serious failures set CFS, and how should the host interpret it?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-105-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-105-a-01">CFS exposes a serious condition when completion communication may fail; it is not a mandatory flag for every command error.</p><div class="qa-sections">
<section class="qa-section" id="q-105-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-105-a-02"></span><p>CFS is controller state; impact on other controllers requires separate evidence.</p>
<span class="qa-anchor" id="q-105-a-03"></span><p>Read CFS directly and preserve CC, CAP, readiness and timing; for secondary controllers also check Online/Offline state.</p>
<span class="qa-anchor" id="q-105-a-04"></span><p>Base 9.5 permits CFS for serious conditions preventing CQE communication. Offline secondary controllers have a separate virtualization use of CFS.</p>
</section>
<section class="qa-section" id="q-105-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-105-a-17"></span><p>First determine whether this is an Offline secondary controller rather than a hardware failure.</p>
<span class="qa-anchor" id="q-105-a-05"></span><p>On timeouts or repeated errors, read CFS. For a fatal condition, reset/reinitialize that controller, then consider supported platform-appropriate subsystem reset if the condition persists.</p>
</section>
<section class="qa-section" id="q-105-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-105-a-06"></span><p>Recovery must restore usable state and command processing; CFS clearing does not replace queue and readiness initialization.</p>
<span class="qa-anchor" id="q-105-a-07"></span><p>CFS is not a CQE and its condition is not signaled by an interrupt. Lost completion communication cannot support a requirement for every outstanding command to return Internal Error.</p>
<span class="qa-anchor" id="q-105-a-16"></span><p>Correlate role, virtualization state, communication and reset outcome to distinguish expected Offline state from fatal failure.</p>
</section>
<section class="qa-section" id="q-105-s-04" data-answer-section="4"><h3><span>4.</span> Whether CQE, DNR and More apply here</h3>
<span class="qa-anchor" id="q-105-a-08"></span><p>Reading CFS has no CQE, so DNR/More do not apply to the register read; decode them only in a separately received completion.</p>
</section>
</div>
<span class="qa-anchor" id="q-105-a-09"></span><span class="qa-anchor" id="q-105-a-10"></span><span class="qa-anchor" id="q-105-a-11"></span><span class="qa-anchor" id="q-105-a-12"></span><span class="qa-anchor" id="q-105-a-13"></span><span class="qa-anchor" id="q-105-a-14"></span><span class="qa-anchor" id="q-105-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-cc">Base 2.4 §3.1.4 (CC, CSTS, NSSR)</a> · <a href="#ref-virtual">Base 2.4 §8.2.7</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-106" data-question="106" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-106">Q106</a> How are CQEs, Error Information and persistent events correlated?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-106-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-106-a-01">CQEs describe commands, Error Information extends errors and PEL records significant events. Correlation adds evidence without requiring one-to-one records.</p><div class="qa-sections">
<section class="qa-section" id="q-106-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-106-a-02"></span><p>Establish controller, namespace, queue lifetime and event scope; related scopes do not necessarily identify one command.</p>
<span class="qa-anchor" id="q-106-a-03"></span><p>Check ELPE, PEL support/event bitmap and timestamp origin/synchronization.</p>
<span class="qa-anchor" id="q-106-a-04"></span><p>Use SQID/CID/status, then ECNT/NSID/opcode, then PEL event type/controller/time/data. Parameter Error Location is not a PEL file offset.</p>
</section>
<section class="qa-section" id="q-106-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-106-a-17"></span><p>First align sampling times and controller identity before interpreting apparent contradictions.</p>
<span class="qa-anchor" id="q-106-a-05"></span><p>Match command and error entry first, then related PEL events; account for timestamp changes before ordering events.</p>
</section>
<section class="qa-section" id="q-106-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-106-a-06"></span><p>A useful result states what each source establishes and leaves unresolved; Format Start does not establish Format Completion.</p>
<span class="qa-anchor" id="q-106-a-07"></span><p>A missing PEL entry is not automatically a defect; check support and recording conditions, but optional support does not excuse required behavior once advertised.</p>
<span class="qa-anchor" id="q-106-a-16"></span><p>Correlate capability, trigger, CQE and retention on one timeline; entries clearing and counters persisting after reset can both be correct.</p>
</section>
</div>
<span class="qa-anchor" id="q-106-a-08"></span><span class="qa-anchor" id="q-106-a-09"></span><span class="qa-anchor" id="q-106-a-10"></span><span class="qa-anchor" id="q-106-a-11"></span><span class="qa-anchor" id="q-106-a-12"></span><span class="qa-anchor" id="q-106-a-13"></span><span class="qa-anchor" id="q-106-a-14"></span><span class="qa-anchor" id="q-106-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a> · <a href="#ref-timestamp">Base 2.4 §5.2.30.1.8</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<section id="common-rules" class="qa-common"><h2>Shared rules linked from the answers</h2><p>Each shared mechanism is explained in full once in this volume. Use browser Back to return to the question; explicit command or feature exceptions take precedence.</p>
<article id="common-command-10"><h3>Command completion, events and records · Are Error Information or other logs updated?</h3><p>A successful CQE does not require a new Error Information entry. For an error with More=1, read LID 01h and correlate SQID, CID and Error Count; not every unsuccessful CQE requires a new entry. Re-read the interfaces named in this question for the state the operation changes.</p></article>
</section>
<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-cc"><strong>Base 2.4 · §3.1.4 (CC, CSTS, NSSR)</strong><br>Printed pages 60–66 · PDF 86–92 · Figure 41–43</li>
<li id="ref-nsid"><strong>Base 2.4 · §3.2.1</strong><br>Printed pages 78–81 · PDF 104–107</li>
<li id="ref-order"><strong>Base 2.4 · §3.4.1–3.4.5</strong><br>Printed pages 101–105 · PDF 127–131 · Figure 80–81</li>
<li id="ref-ready"><strong>Base 2.4 · §3.5.3–3.5.4</strong><br>Printed pages 109–113 · PDF 135–139 · Figure 84–85</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-sqe"><strong>Base 2.4 · §4.1.1</strong><br>Printed pages 139–142 · PDF 165–168 · Figure 92–93</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>Printed pages 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-abort"><strong>Base 2.4 · §5.2.1</strong><br>Printed pages 181–182 · PDF 207–208 · Figure 147–149</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>Printed pages 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-getlog"><strong>Base 2.4 · §5.2.13–5.2.13.1.1</strong><br>Printed pages 212–218 · PDF 238–244 · Figure 203–211</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-pelcontext"><strong>Base 2.4 · §5.2.13.1.14–5.2.13.1.14.2.5 (exclude PCIe link/packet decoding)</strong><br>Printed pages 244–256, 258 · PDF 270–282, 284 · Figure 232–244, 246</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-nsmanage"><strong>Base 2.4 · §5.2.24–5.2.25, 8.1.17</strong><br>Printed pages 442–448, 660–664 · PDF 468–474, 686–690 · Figure 442–450</li>
<li id="ref-timestamp"><strong>Base 2.4 · §5.2.30.1.8</strong><br>Printed pages 469–471 · PDF 495–497 · Figure 479–480</li>
<li id="ref-behavior"><strong>Base 2.4 · §5.2.30.1.15</strong><br>Printed pages 475–477 · PDF 501–503 · Figure 491</li>
<li id="ref-create"><strong>Base 2.4 · §5.3.1–5.3.2</strong><br>Printed pages 527–531 · PDF 553–557 · Figure 571–579</li>
<li id="ref-delete"><strong>Base 2.4 · §5.3.3–5.3.4</strong><br>Printed pages 531–532 · PDF 557–558 · Figure 580–583</li>
<li id="ref-virtual"><strong>Base 2.4 · §8.2.7</strong><br>Printed pages 754–758 · PDF 780–784 · Figure 796</li>
<li id="ref-fatal"><strong>Base 2.4 · §9.1–9.6.1</strong><br>Printed pages 825–826 · PDF 851–852</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b41">Base 2.4 Figure 41 · Offset 14h: CC – Controller Configuration</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b42">Base 2.4 Figure 42 · Offset 1Ch: CSTS – Controller Status</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/errors/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/errors.html">Chinese tutorial HTML</a></nav>
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
