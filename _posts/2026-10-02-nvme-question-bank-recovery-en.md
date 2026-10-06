---
layout: post
title: "NVMe Self-Study Bank: Abort, timeout and recovery"
date: 2026-10-02 00:00:00 +0800
categories: [nvme]
permalink: /nvme/question-bank/recovery/en/
lang: en
nvme_quickref: true
nvme_qa: true
---

<div class="nvme-quickref nvme-qa">
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/recovery/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/recovery.html">Chinese tutorial HTML</a></nav>
<main id="content"><p class="qr-eyebrow">BASE 2.4 / NVM 1.3 / PCIe 1.4 · Q1–328</p>
<header><p class="qa-range">Q107–Q117</p><h1>Abort, timeout and recovery</h1><p class="qr-intro">A timeout is an observation, not a location. Follow submission through consumption before choosing abort or reset.</p><p>Practice first, then reveal the explanation. Each question uses the prose, field interpretation, comparison or flow that suits it. All numerical examples are hypothetical. Status is written SCT/SC; h indicates hexadecimal.</p></header>
<aside class="qa-glossary"><h2>Terms used in this volume</h2><dl><dt>Controller / namespace</dt><dd>A controller receives commands and manages access. A namespace is a logical storage space that commands can address. An NVM subsystem contains controllers and nonvolatile storage resources.</dd><dt>SQ / CQ / SQE / CQE</dt><dd>Submission and Completion Queues carry command entries (SQEs) and completion entries (CQEs). QID identifies a queue, CID distinguishes outstanding commands in one SQ, and NSID identifies a namespace.</dd><dt>Register / Identify / Feature / Log</dt><dd>A register exposes control or state. Identify queries capabilities and attributes; features query or configure operation; log pages report specific state or records. FID, LID, CNS and CSI select features, logs, Identify structures and command sets.</dd><dt>index / offset / zero-based</dt><dd>An index selects an entry, usually starting at 0; an offset measures distance from an origin in specified units. A zero-based count encodes count−1, but not every zero-valued field is a count. A Dword is 4 bytes; a byte is 8 bits.</dd><dt>Scope / reset / retention</dt><dd>Scope names the affected objects; retention means preserving state. Controller Reset (clearing CC.EN) is one form of Controller Level Reset, or CLR. Different CLR triggers can retain different registers.</dd></dl></aside>
<section id="overview" class="qa-overview"><h2>Find the command stage first</h2><p class="qa-takeaway">Missing completion proves neither nonexecution nor unchanged media.</p>
<div class="qr-table" tabindex="0" role="region" aria-label="Horizontally scrollable comparison table"><table><thead><tr><th scope="col">Stage</th><th scope="col">Evidence</th><th scope="col">Next question</th></tr></thead><tbody><tr><td>Submitted</td><td>SQE and tail</td><td>Was it consumed?</td></tr><tr><td>Consumed</td><td>SQHD and tracking</td><td>Is it a long operation?</td></tr><tr><td>Completed</td><td>CQE and phase</td><td>Did the host miss it?</td></tr><tr><td>Recovering</td><td>Abort/reset state</td><td>Are prior effects uncertain?</td></tr></tbody></table></div>
<p><strong>Worked interpretation: </strong>Abort targeting SQ5/CID 9 has its own Admin completion. One CQE for each is normal; duplicate target completion is different.</p>
<p class="qa-citations">Sources: <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a></p>
</section>
<div class="qa-controls" hidden><label>Search this page <input type="search" id="qa-search" placeholder="Question number, field or keyword"></label><button type="button" data-expand="true">Expand all answers</button><button type="button" data-expand="false">Collapse all answers</button><output id="qa-count" aria-live="polite"></output></div>
<section id="question-index"><h2>Questions in this volume</h2><ol class="qa-index">
<li><a href="#q-107">Q107 · How does Abort identify its target with SQID and CID?</a></li>
<li><a href="#q-108">Q108 · What happens when Abort targets a completed or missing command?</a></li>
<li><a href="#q-109">Q109 · How does ACL apply to repeated and concurrent Abort commands?</a></li>
<li><a href="#q-110">Q110 · Does successful Abort prove that the target never executed?</a></li>
<li><a href="#q-111">Q111 · Can a target complete normally if Abort did not immediately cancel it?</a></li>
<li><a href="#q-112">Q112 · How does the host handle racing Abort and target completions?</a></li>
<li><a href="#q-113">Q113 · Must every timeout follow Abort, queue reset, then controller reset?</a></li>
<li><a href="#q-114">Q114 · How should the host recover when Abort itself times out?</a></li>
<li><a href="#q-115">Q115 · How are old commands, completions and queues handled after reset?</a></li>
<li><a href="#q-116">Q116 · How do command, ready and long-operation timeouts differ?</a></li>
<li><a href="#q-117">Q117 · How is a timeout located along submission, execution and completion?</a></li>
</ol></section>
<article class="qa-question" id="q-107" data-question="107" data-answer-kind="process"><h2><a class="qa-qid" href="#q-107">Q107</a> How does Abort identify its target with SQID and CID?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-107-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-107-a-01">Abort requests cancellation of a previously submitted command without necessarily resetting the controller; it does not prove the target was never executed.</p><div class="qa-sections">
<section class="qa-section" id="q-107-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-107-a-02"></span><p>The target can be in the Admin SQ or an I/O SQ. Abort is itself an Admin command with its own CID and completion.</p>
<span class="qa-anchor" id="q-107-a-03"></span><p>Identify.ACL is the zero-based concurrent Abort limit; queue depth does not replace it.</p>
<span class="qa-anchor" id="q-107-a-04"></span><p>Abort CDW10 bits 31:16 select target CID and bits 15:0 target SQID; CDW0.CID identifies the Abort command itself.</p>
</section>
<section class="qa-section" id="q-107-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-107-a-05"></span><p>Locate the target in outstanding tracking, retain its buffers, submit Abort with a distinct Admin CID and track both completions.</p>
<span class="qa-anchor" id="q-107-a-06"></span><p>On successful Abort, DW0.IANP=0 reports immediate abort; IANP=1 reports no immediate abort but allows deferred abort. Inspect the target CQE too.</p>
</section>
<section class="qa-section" id="q-107-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-107-a-07"></span><p>Excess outstanding Aborts may receive 1/03h. A missing target can be represented by successful Abort with IANP=1, not a universal Invalid Queue Identifier requirement.</p>
<span class="qa-anchor" id="q-107-a-16"></span><p>If SQ3/CID 7 and SQ4/CID 7 coexist, CDW10=(7&lt;&lt;16)|3 targets only the former; this detects swapped fields.</p>
</section>
</div>
<span class="qa-anchor" id="q-107-a-17"></span><span class="qa-anchor" id="q-107-a-08"></span><span class="qa-anchor" id="q-107-a-09"></span><span class="qa-anchor" id="q-107-a-10"></span><span class="qa-anchor" id="q-107-a-11"></span><span class="qa-anchor" id="q-107-a-12"></span><span class="qa-anchor" id="q-107-a-13"></span><span class="qa-anchor" id="q-107-a-14"></span><span class="qa-anchor" id="q-107-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-108" data-question="108" data-answer-kind="error"><h2><a class="qa-qid" href="#q-108">Q108</a> What happens when Abort targets a completed or missing command?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-108-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-108-a-01">A target may finish between the host deciding to abort and the controller processing Abort; absence is a normal race to handle.</p><div class="qa-sections">
<section class="qa-section" id="q-108-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-108-a-02"></span><p>The target is the command at the specified IDs at that time, not every historic use of those numbers.</p>
<span class="qa-anchor" id="q-108-a-04"></span><p>Read Abort status and IANP and check for a target CQE. IANP=1 can mean absence or inability to abort immediately.</p>
<span class="qa-anchor" id="q-108-a-07"></span><p>Do not assign a universal error status to every missing SQID/CID target; separate any independent invalid encoding in Abort itself.</p>
</section>
<section class="qa-section" id="q-108-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-108-a-03"></span><p>Preserve queue-lifetime and CID-allocation records so a delayed Abort is not misdirected to a later reuse.</p>
<span class="qa-anchor" id="q-108-a-05"></span><p>Process an already received target completion; if it remains outstanding with IANP=1, continue tracking and retain its buffers.</p>
</section>
<section class="qa-section" id="q-108-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-108-a-06"></span><p>A valid Abort can succeed with IANP=1 without cancelling the target; this reports request processing, not target success or rollback.</p>
<span class="qa-anchor" id="q-108-a-16"></span><p>Replace a test requiring Abort failure for a completed target with checks of IANP and the existing target result.</p>
<span class="qa-anchor" id="q-108-a-17"></span><p>First check whether the target already completed but its CQE has not been consumed.</p>
</section>
</div>
<span class="qa-anchor" id="q-108-a-08"></span><span class="qa-anchor" id="q-108-a-09"></span><span class="qa-anchor" id="q-108-a-10"></span><span class="qa-anchor" id="q-108-a-11"></span><span class="qa-anchor" id="q-108-a-12"></span><span class="qa-anchor" id="q-108-a-13"></span><span class="qa-anchor" id="q-108-a-14"></span><span class="qa-anchor" id="q-108-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-109" data-question="109" data-answer-kind="error"><h2><a class="qa-qid" href="#q-109">Q109</a> How does ACL apply to repeated and concurrent Abort commands?</h2>
<p class="qa-prompt">Distinguish failure conditions before deciding whether a particular response is required.</p>
<details class="qa-answer" id="q-109-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-109-a-01">ACL limits concurrent Abort requests, not cancellations per second or namespace count.</p><div class="qa-sections">
<section class="qa-section" id="q-109-s-01" data-answer-section="1"><h3><span>1.</span> Distinguish the failure conditions</h3>
<span class="qa-anchor" id="q-109-a-02"></span><p>Each outstanding Abort consumes concurrent capacity, including several targeting the same command.</p>
<span class="qa-anchor" id="q-109-a-04"></span><p>Track each Abort CID, target IDs and result separately. Bulk cancellation can use supported Cancel or I/O SQ deletion/recreation.</p>
<span class="qa-anchor" id="q-109-a-07"></span><p>The controller may complete excess requests with 1/03h; the specification does not mandate observing that code on every over-limit test.</p>
</section>
<section class="qa-section" id="q-109-s-02" data-answer-section="2"><h3><span>2.</span> Establish the cause from evidence</h3>
<span class="qa-anchor" id="q-109-a-03"></span><p>ACL=0 permits one outstanding Abort and ACL=3 four; release host accounting on completion.</p>
<span class="qa-anchor" id="q-109-a-05"></span><p>Check capacity before submission and wait at the limit. Repeated targets still have separate Abort CQEs but only one target completion.</p>
</section>
<section class="qa-section" id="q-109-s-03" data-answer-section="3"><h3><span>3.</span> Outcome and follow-up checks</h3>
<span class="qa-anchor" id="q-109-a-06"></span><p>With ACL=1, two outstanding Aborts fit the limit; submitting another after one completes avoids host overrun.</p>
<span class="qa-anchor" id="q-109-a-16"></span><p>Count submissions not yet completed rather than cumulative Abort operations.</p>
<span class="qa-anchor" id="q-109-a-17"></span><p>First check zero-based ACL interpretation and removal of completed requests from the count.</p>
</section>
</div>
<span class="qa-anchor" id="q-109-a-08"></span><span class="qa-anchor" id="q-109-a-09"></span><span class="qa-anchor" id="q-109-a-10"></span><span class="qa-anchor" id="q-109-a-11"></span><span class="qa-anchor" id="q-109-a-12"></span><span class="qa-anchor" id="q-109-a-13"></span><span class="qa-anchor" id="q-109-a-14"></span><span class="qa-anchor" id="q-109-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-110" data-question="110" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-110">Q110</a> Does successful Abort prove that the target never executed?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-110-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-110-a-01">No. Abort can stop further processing but is not transaction rollback; data transfer or state changes may already have occurred.</p><div class="qa-sections">
<section class="qa-section" id="q-110-s-01" data-answer-section="1"><h3><span>1.</span> IANP defines the guarantee after abort</h3>
<span class="qa-anchor" id="q-110-a-03"></span><p>The Base 2.4 evidence is IANP in a successful Abort, not success status alone.</p>
<span class="qa-anchor" id="q-110-a-04"></span><p>IANP=0 prohibits subsequent target effects after the Abort CQE, including host-memory access and media/management changes, except posting the target CQE.</p>
<span class="qa-anchor" id="q-110-a-06"></span><p>Immediate abort yields target Command Abort Requested. The target CQE may precede or, under the no-subsequent-effects guarantee, follow the Abort CQE.</p>
<span class="qa-anchor" id="q-110-a-07"></span><p>IANP=1 gives no no-subsequent-effects guarantee. An initiated but incomplete transfer without a posted target CQE precludes immediate abort.</p>
</section>
<section class="qa-section" id="q-110-s-02" data-answer-section="2"><h3><span>2.</span> Earlier effects still need checking</h3>
<span class="qa-anchor" id="q-110-a-05"></span><p>Record Abort completion and IANP, handle target completion and assess data under command semantics before retrying a possibly partially executed write.</p>
<span class="qa-anchor" id="q-110-a-16"></span><p>Test prohibited effects after Abort completion rather than requiring that the target never performed any work.</p>
</section>
</div>
<span class="qa-anchor" id="q-110-a-02"></span><span class="qa-anchor" id="q-110-a-17"></span><span class="qa-anchor" id="q-110-a-08"></span><span class="qa-anchor" id="q-110-a-09"></span><span class="qa-anchor" id="q-110-a-10"></span><span class="qa-anchor" id="q-110-a-11"></span><span class="qa-anchor" id="q-110-a-12"></span><span class="qa-anchor" id="q-110-a-13"></span><span class="qa-anchor" id="q-110-a-14"></span><span class="qa-anchor" id="q-110-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-order">Base 2.4 §3.4.1–3.4.5</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-111" data-question="111" data-answer-kind="concept"><h2><a class="qa-qid" href="#q-111">Q111</a> Can a target complete normally if Abort did not immediately cancel it?</h2>
<p class="qa-prompt">Explain the mechanism in your own words and identify a common misconception.</p>
<details class="qa-answer" id="q-111-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-111-a-01">Yes. IANP=1 allows either deferred cancellation or normal target completion.</p><div class="qa-sections">
<section class="qa-section" id="q-111-s-01" data-answer-section="1"><h3><span>1.</span> Read the Abort and target CQEs separately</h3>
<span class="qa-anchor" id="q-111-a-03"></span><p>Inspect IANP on successful Abort and the target CQE. Do not interpret reserved/undefined DW0 from a failed Abort as a valid IANP result.</p>
<span class="qa-anchor" id="q-111-a-04"></span><p>A deferred-aborted target must report Command Abort Requested; otherwise it reports its actual execution result.</p>
<span class="qa-anchor" id="q-111-a-06"></span><p>Either target success or Command Abort Requested can be valid, without a second target completion.</p>
</section>
<section class="qa-section" id="q-111-s-02" data-answer-section="2"><h3><span>2.</span> Continue tracking the target after IANP=1</h3>
<span class="qa-anchor" id="q-111-a-05"></span><p>After IANP=1, track the target under host recovery time limits; escalating to reset requires proper queue-lifetime and resource handling.</p>
<span class="qa-anchor" id="q-111-a-07"></span><p>IANP=1 means neither that cancellation will never occur nor that it definitely will occur later.</p>
</section>
</div>
<span class="qa-anchor" id="q-111-a-02"></span><span class="qa-anchor" id="q-111-a-16"></span><span class="qa-anchor" id="q-111-a-17"></span><span class="qa-anchor" id="q-111-a-08"></span><span class="qa-anchor" id="q-111-a-09"></span><span class="qa-anchor" id="q-111-a-10"></span><span class="qa-anchor" id="q-111-a-11"></span><span class="qa-anchor" id="q-111-a-12"></span><span class="qa-anchor" id="q-111-a-13"></span><span class="qa-anchor" id="q-111-a-14"></span><span class="qa-anchor" id="q-111-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-112" data-question="112" data-answer-kind="process"><h2><a class="qa-qid" href="#q-112">Q112</a> How does the host handle racing Abort and target completions?</h2>
<p class="qa-prompt">Order the actions and identify which completion must precede the next action.</p>
<details class="qa-answer" id="q-112-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-112-a-01">Timeout and normal completion paths can race over host tracking. Synchronize host state rather than demanding a universal completion order.</p><div class="qa-sections">
<section class="qa-section" id="q-112-s-01" data-answer-section="1"><h3><span>1.</span> Prepare the operation</h3>
<span class="qa-anchor" id="q-112-a-02"></span><p>Abort and target have separate lifetimes; their CQEs are distinct even though they refer to one target.</p>
<span class="qa-anchor" id="q-112-a-03"></span><p>Identify completions by SQID+CID, phase and queue lifetime; CID alone is insufficient across queues.</p>
<span class="qa-anchor" id="q-112-a-04"></span><p>Track target and Abort completion independently; only the target result completes the target to higher software layers.</p>
</section>
<section class="qa-section" id="q-112-s-02" data-answer-section="2"><h3><span>2.</span> Sequence and completion conditions</h3>
<span class="qa-anchor" id="q-112-a-05"></span><p>Update the appropriate state atomically. A later Abort CQE closes Abort only; an earlier Abort CQE requires IANP and target-state handling.</p>
<span class="qa-anchor" id="q-112-a-06"></span><p>Each command completes once and resources are reclaimed once. Two CQEs for two different commands are not duplicate target completion.</p>
</section>
<section class="qa-section" id="q-112-s-03" data-answer-section="3"><h3><span>3.</span> Handle unmet conditions</h3>
<span class="qa-anchor" id="q-112-a-07"></span><p>Do not universally require target CQE first; Base 2.4 permits either posting order when immediate-abort no-subsequent-effects conditions are met.</p>
<span class="qa-anchor" id="q-112-a-16"></span><p>Verify single upper-layer completion and prevent old Abort results from affecting a reused CID lifetime.</p>
</section>
</div>
<span class="qa-anchor" id="q-112-a-17"></span><span class="qa-anchor" id="q-112-a-08"></span><span class="qa-anchor" id="q-112-a-09"></span><span class="qa-anchor" id="q-112-a-10"></span><span class="qa-anchor" id="q-112-a-11"></span><span class="qa-anchor" id="q-112-a-12"></span><span class="qa-anchor" id="q-112-a-13"></span><span class="qa-anchor" id="q-112-a-14"></span><span class="qa-anchor" id="q-112-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-113" data-question="113" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-113">Q113</a> Must every timeout follow Abort, queue reset, then controller reset?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-113-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-113-a-01">There is no universal three-step sequence. Diagnose a slow command, failed queue or lost controller communication before selecting recovery scope.</p><div class="qa-sections">
<section class="qa-section" id="q-113-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-113-a-02"></span><p>Abort targets a command; queue deletion/recreation targets queues; controller reset affects all its queues and outstanding commands.</p>
<span class="qa-anchor" id="q-113-a-03"></span><p>Preserve CQ position/phase, interrupts, CSTS and other-command progress. CAP.TO is not a per-I/O timeout.</p>
<span class="qa-anchor" id="q-113-a-04"></span><p>Available actions include Abort, queue deletion/recreation and reset via CC.EN, each with its own preconditions and completion checks.</p>
</section>
<section class="qa-section" id="q-113-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-113-a-05"></span>
<span class="qa-anchor" id="q-113-a-17"></span>
<figure class="qa-flow" id="q-113-flow"><figcaption>Locate the failure before selecting recovery</figcaption>
<p>These branches guide the host’s recovery choice; they are not a mandatory three-step sequence.</p><ol class="qa-flow-steps">
<li class="qa-flow-step"><strong>First inspect the CQ: is a valid completion already present?</strong><p>If the host missed processing or an interrupt, consume the CQE and investigate notification.</p></li>
<li class="qa-flow-branch"><strong>One command remains outstanding; Admin path works</strong><p>Consider a targeted Abort, tracking its result separately from the target command.</p></li>
<li class="qa-flow-branch"><strong>Queue failure with a usable management path</strong><p>Recover the affected queues under Delete/Create rules, confirming old accesses have stopped before reusing memory.</p></li>
<li class="qa-flow-branch"><strong>Severe Admin failure or a Delete that does not complete</strong><p>Consider Controller Reset without forcing an Abort through an unusable path.</p></li>
</ol><p class="qa-flow-conclusion">Without a CQE, a host timeout provides no DNR bit. After recovery, also check ongoing background operations; a working new queue is not the whole result.</p></figure>
</section>
<section class="qa-section" id="q-113-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-113-a-06"></span><p>Recovery establishes usable new channels, resolves old-command access risks and rechecks any continuing background operations.</p>
<span class="qa-anchor" id="q-113-a-07"></span><p>A host timeout is not an NVMe completion status. Do not fabricate a timeout CQE or require Abort when the Admin path cannot complete it.</p>
<span class="qa-anchor" id="q-113-a-16"></span><p>Mark specification requirements separately from host-selected timeouts and escalation policies.</p>
</section>
</div>
<span class="qa-anchor" id="q-113-a-08"></span><span class="qa-anchor" id="q-113-a-09"></span><span class="qa-anchor" id="q-113-a-10"></span><span class="qa-anchor" id="q-113-a-11"></span><span class="qa-anchor" id="q-113-a-12"></span><span class="qa-anchor" id="q-113-a-13"></span><span class="qa-anchor" id="q-113-a-14"></span><span class="qa-anchor" id="q-113-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-114" data-question="114" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-114">Q114</a> How should the host recover when Abort itself times out?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-114-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-114-a-01">Now both target outcome and Admin-channel health are uncertain. Repeated Abort submissions do not establish that old commands stopped.</p><div class="qa-sections">
<section class="qa-section" id="q-114-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-114-a-02"></span><p>Recovery may widen to the controller, requiring coordination with all its queue and resource management.</p>
<span class="qa-anchor" id="q-114-a-03"></span><p>Check Admin CQ phase/head, CFS/RDY and ACL accounting.</p>
<span class="qa-anchor" id="q-114-a-04"></span><p>Preserve Abort CID, target IDs, timing and observed CQEs; a subsequent reset does not fabricate an Abort result.</p>
</section>
<section class="qa-section" id="q-114-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-114-a-17"></span><p>First check whether the Admin CQ is full or no longer being consumed.</p>
<span class="qa-anchor" id="q-114-a-05"></span><p>Exclude missed Admin CQEs; serious Admin failure calls for controller reset, state confirmation and reinitialization under Base 9.1/9.5.</p>
</section>
<section class="qa-section" id="q-114-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-114-a-06"></span><p>New commands use recovered queues; prior data effects still require command-specific persistence analysis.</p>
<span class="qa-anchor" id="q-114-a-07"></span><p>Without an Abort CQE there is no IANP, DNR or More to decode. Successful reset does not prove a target write never happened.</p>
<span class="qa-anchor" id="q-114-a-16"></span><p>Correlate registers, new queue usability and background-operation logs rather than relying only on a host reset routine’s return value.</p>
</section>
</div>
<span class="qa-anchor" id="q-114-a-08"></span><span class="qa-anchor" id="q-114-a-09"></span><span class="qa-anchor" id="q-114-a-10"></span><span class="qa-anchor" id="q-114-a-11"></span><span class="qa-anchor" id="q-114-a-12"></span><span class="qa-anchor" id="q-114-a-13"></span><span class="qa-anchor" id="q-114-a-14"></span><span class="qa-anchor" id="q-114-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-115" data-question="115" data-answer-kind="lifecycle"><h2><a class="qa-qid" href="#q-115">Q115</a> How are old commands, completions and queues handled after reset?</h2>
<p class="qa-prompt">Name the reset or interruption, then assess settings, ongoing operations and data separately.</p>
<details class="qa-answer" id="q-115-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-115-a-01">Reset separates queue lifetimes; surviving memory bytes are not evidence of valid commands or completions.</p><div class="qa-sections">
<section class="qa-section" id="q-115-s-01" data-answer-section="1"><h3><span>1.</span> Identify the trigger and affected objects</h3>
<span class="qa-anchor" id="q-115-a-02"></span><p>Rebuild affected I/O queues and outstanding tracking; stored data and independent background operations follow separate rules.</p>
<span class="qa-anchor" id="q-115-a-03"></span><p>Check reset type, CC/CSTS and Admin-register retention; CC.EN-reset exceptions do not apply to every source.</p>
</section>
<section class="qa-section" id="q-115-s-02" data-answer-section="2"><h3><span>2.</span> State changes and recovery</h3>
<span class="qa-anchor" id="q-115-a-04"></span><p>Reset host queue pointers/expected phase and separate new submissions from old tracking; inspect continuing operations through their logs.</p>
<span class="qa-anchor" id="q-115-a-05"></span><p>Stop submissions, complete reset and access-termination checks, create new queues, then resume I/O with retry analysis of possible prior effects.</p>
<span class="qa-anchor" id="q-115-a-06"></span><p>New queues accept completions for their new lifetime; the host does not wait for all old CQEs after reset termination.</p>
</section>
<section class="qa-section" id="q-115-s-03" data-answer-section="3"><h3><span>3.</span> Verify retention and recovery</h3>
<span class="qa-anchor" id="q-115-a-07"></span><p>Reset is not universal per-command completion with one error code. Reset-aborted AERs expressly have no CQE; other commands do not universally return Command Abort Requested.</p>
<span class="qa-anchor" id="q-115-a-16"></span><p>Validate new queues and termination of old-buffer accesses; new-command success alone does not exclude late old-command activity.</p>
<span class="qa-anchor" id="q-115-a-17"></span><p>First inspect reused phase or tracking state that could make stale CQEs appear new.</p>
</section>
</div>
<span class="qa-anchor" id="q-115-a-08"></span><span class="qa-anchor" id="q-115-a-09"></span><span class="qa-anchor" id="q-115-a-10"></span><span class="qa-anchor" id="q-115-a-11"></span><span class="qa-anchor" id="q-115-a-12"></span><span class="qa-anchor" id="q-115-a-13"></span><span class="qa-anchor" id="q-115-a-14"></span><span class="qa-anchor" id="q-115-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-commrecovery">Base 2.4 §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-116" data-question="116" data-answer-kind="compare"><h2><a class="qa-qid" href="#q-116">Q116</a> How do command, ready and long-operation timeouts differ?</h2>
<p class="qa-prompt">Identify the key difference and one case where the alternatives are not interchangeable.</p>
<details class="qa-answer" id="q-116-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-116-a-01">Command completion, readiness and background-operation completion are different waits; sharing one deadline causes false timeouts.</p><div class="qa-sections">
<section class="qa-section" id="q-116-s-01" data-answer-section="1"><h3><span>1.</span> What differs</h3>
<span class="qa-anchor" id="q-116-a-02"></span><p>Host command timeouts are software policy, readiness concerns controller state and background progress belongs to the management operation.</p>
<span class="qa-anchor" id="q-116-a-04"></span><p>Observe CQEs, RDY and operation logs. AER remains outstanding without an event and should not use an ordinary command timeout.</p>
</section>
<section class="qa-section" id="q-116-s-02" data-answer-section="2"><h3><span>2.</span> How to choose and verify</h3>
<span class="qa-anchor" id="q-116-a-03"></span><p>Disable uses CAP.TO; enable uses ready-mode and CRTO/CAP rules; interpret function estimates and maxima under their own definitions.</p>
<span class="qa-anchor" id="q-116-a-05"></span><p>Name the awaited transition and timer start. After Sanitize initiation succeeds, monitor its status rather than expecting a second command CQE.</p>
<span class="qa-anchor" id="q-116-a-06"></span><p>The wait succeeds when its specified state is reached; command success and media-operation completion can occur separately.</p>
</section>
<section class="qa-section" id="q-116-s-03" data-answer-section="3"><h3><span>3.</span> Where the comparison stops</h3>
<span class="qa-anchor" id="q-116-a-07"></span><p>CAP.TO is not universal across commands, and an estimated duration is not automatically a mandatory deadline.</p>
<span class="qa-anchor" id="q-116-a-16"></span><p>Record source, units, starting event and whether each timeout is an estimate or limit.</p>
</section>
</div>
<span class="qa-anchor" id="q-116-a-17"></span><span class="qa-anchor" id="q-116-a-08"></span><span class="qa-anchor" id="q-116-a-09"></span><span class="qa-anchor" id="q-116-a-10"></span><span class="qa-anchor" id="q-116-a-11"></span><span class="qa-anchor" id="q-116-a-12"></span><span class="qa-anchor" id="q-116-a-13"></span><span class="qa-anchor" id="q-116-a-14"></span><span class="qa-anchor" id="q-116-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-cap">Base 2.4 §3.1.4 (CAP, VS)</a> · <a href="#ref-crto">Base 2.4 §3.1.4 (CRTO)</a> · <a href="#ref-ready">Base 2.4 §3.5.3–3.5.4</a> · <a href="#ref-abort">Base 2.4 §5.2.1</a> · <a href="#ref-aerfull">Base 2.4 §5.2.2 (PCIe-applicable events)</a> · <a href="#ref-idctrl">Base 2.4 §5.2.14.2.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>
<article class="qa-question" id="q-117" data-question="117" data-answer-kind="diagnose"><h2><a class="qa-qid" href="#q-117">Q117</a> How is a timeout located along submission, execution and completion?</h2>
<p class="qa-prompt">Separate available evidence from missing information before judging conformance.</p>
<details class="qa-answer" id="q-117-answer"><summary>Reveal the explanation</summary>
<p class="qa-answer-lead" id="q-117-a-01">Evidence along the command lifetime localizes missing progress before blaming slow firmware execution.</p><div class="qa-sections">
<section class="qa-section" id="q-117-s-01" data-answer-section="1"><h3><span>1.</span> Preserve the evidence first</h3>
<span class="qa-anchor" id="q-117-a-02"></span><p>Analyze the target together with its SQ, CQ, shared vector and neighboring commands to locate shared bottlenecks.</p>
<span class="qa-anchor" id="q-117-a-03"></span><p>Use SQE snapshots, tail doorbell, reported SQHD, CQ phase/head, interrupt configuration and CSTS as interface evidence.</p>
<span class="qa-anchor" id="q-117-a-04"></span><p>Advanced SQHD establishes consumption, not completion of every command; a valid target CQE establishes its result, while interrupts notify the host to inspect CQs.</p>
</section>
<section class="qa-section" id="q-117-s-02" data-answer-section="2"><h3><span>2.</span> Work through the possible causes</h3>
<span class="qa-anchor" id="q-117-a-17"></span><p>First inspect the expected-phase CQ slot to distinguish an unreported result from an unconsumed completion.</p>
<span class="qa-anchor" id="q-117-a-05"></span><p>Check visibility, doorbell update, new CQ phase and host consumption/head updates. State uncertainty when internal fetch timing is unobservable.</p>
</section>
<section class="qa-section" id="q-117-s-03" data-answer-section="3"><h3><span>3.</span> Decide what the evidence supports</h3>
<span class="qa-anchor" id="q-117-a-06"></span><p>An existing CQE localizes the issue beyond execution; a doorbell write alone does not prove command fetch.</p>
<span class="qa-anchor" id="q-117-a-07"></span><p>This diagnosis has no single NVMe status; preserve stage-specific evidence rather than inventing a timeout status.</p>
<span class="qa-anchor" id="q-117-a-16"></span><p>Correlate valid completions, shared CQ space and interrupt masking to identify host-side stalls.</p>
</section>
</div>
<span class="qa-anchor" id="q-117-a-08"></span><span class="qa-anchor" id="q-117-a-09"></span><span class="qa-anchor" id="q-117-a-10"></span><span class="qa-anchor" id="q-117-a-11"></span><span class="qa-anchor" id="q-117-a-12"></span><span class="qa-anchor" id="q-117-a-13"></span><span class="qa-anchor" id="q-117-a-14"></span><span class="qa-anchor" id="q-117-a-15"></span>
<details class="qa-source-links"><summary>Source locations for this question</summary>
<p class="qa-citations">Sources: <a href="#ref-sqe">Base 2.4 §4.1.1</a> · <a href="#ref-cqe">Base 2.4 §4.2.1, 4.2.3–4.2.4</a> · <a href="#ref-queue">Base 2.4 §3.3.1</a> · <a href="#ref-pcie">PCIe Transport 1.4 §3.1–3.4</a> · <a href="#ref-irq">PCIe Transport 1.4 §3.5</a> · <a href="#ref-fatal">Base 2.4 §9.1–9.6.1</a> · <a href="#ref-reset">Base 2.4 §3.7.1–3.7.4</a> · <a href="#ref-status">Base 2.4 §4.2.3</a> · <a href="#ref-error">Base 2.4 §5.2.13.1.2</a> · <a href="#ref-aer">Base 2.4 §5.2.2</a> · <a href="#ref-pel">Base 2.4 §5.2.13.1.14 (header, reset, hardware, Set Feature events)</a></p>
</details></details><a class="qa-back" href="#question-index">Back to questions</a></article>

<section id="source-index"><h2>Source locations and existing figure guides</h2><p>Base printed page = PDF page−26; the other two use identical numbers. Locations follow the supplied PDF body and retain figure numbers. Shared pages contribute only the relevant definitions, excluding Fabrics and PCIe link/packet content.</p><ul class="qa-references">
<li id="ref-cap"><strong>Base 2.4 · §3.1.4 (CAP, VS)</strong><br>Printed pages 54–59 · PDF 80–85 · Figure 36–37</li>
<li id="ref-crto"><strong>Base 2.4 · §3.1.4 (CRTO)</strong><br>Printed pages 72–73 · PDF 98–99 · Figure 57</li>
<li id="ref-queue"><strong>Base 2.4 · §3.3.1</strong><br>Printed pages 88–91 · PDF 114–117 · Figure 73–74</li>
<li id="ref-order"><strong>Base 2.4 · §3.4.1–3.4.5</strong><br>Printed pages 101–105 · PDF 127–131 · Figure 80–81</li>
<li id="ref-ready"><strong>Base 2.4 · §3.5.3–3.5.4</strong><br>Printed pages 109–113 · PDF 135–139 · Figure 84–85</li>
<li id="ref-reset"><strong>Base 2.4 · §3.7.1–3.7.4</strong><br>Printed pages 120–124 · PDF 146–150</li>
<li id="ref-sqe"><strong>Base 2.4 · §4.1.1</strong><br>Printed pages 139–142 · PDF 165–168 · Figure 92–93</li>
<li id="ref-cqe"><strong>Base 2.4 · §4.2.1, 4.2.3–4.2.4</strong><br>Printed pages 144–157 · PDF 170–183 · Figure 97–105, 109</li>
<li id="ref-status"><strong>Base 2.4 · §4.2.3</strong><br>Printed pages 145–155 · PDF 171–181 · Figure 101–105</li>
<li id="ref-abort"><strong>Base 2.4 · §5.2.1</strong><br>Printed pages 181–182 · PDF 207–208 · Figure 147–149</li>
<li id="ref-aer"><strong>Base 2.4 · §5.2.2</strong><br>Printed pages 183–190 · PDF 209–216 · Figure 150–156</li>
<li id="ref-aerfull"><strong>Base 2.4 · §5.2.2 (PCIe-applicable events)</strong><br>Printed pages 183–191 · PDF 209–217 · Figure 150–160</li>
<li id="ref-error"><strong>Base 2.4 · §5.2.13.1.2</strong><br>Printed pages 218–220 · PDF 244–246 · Figure 212</li>
<li id="ref-pel"><strong>Base 2.4 · §5.2.13.1.14 (header, reset, hardware, Set Feature events)</strong><br>Printed pages 244–256, 258, 262–264 · PDF 270–282, 284, 288–290 · Figure 232–244, 246, 252–253</li>
<li id="ref-idctrl"><strong>Base 2.4 · §5.2.14.2.1</strong><br>Printed pages 340–387 · PDF 366–413 · Figure 338–341</li>
<li id="ref-commrecovery"><strong>Base 2.4 · §9.1–9.6.2.1 (PCIe-applicable rules; stop before 9.6.2.2)</strong><br>Printed pages 825–828 · PDF 851–854</li>
<li id="ref-fatal"><strong>Base 2.4 · §9.1–9.6.1</strong><br>Printed pages 825–826 · PDF 851–852</li>
<li id="ref-pcie"><strong>PCIe Transport 1.4 · §3.1–3.4</strong><br>Printed pages 9–13 · PDF 9–13 · Figure 3–8</li>
<li id="ref-irq"><strong>PCIe Transport 1.4 · §3.5</strong><br>Printed pages 13–16 · PDF 13–16 · Figure 9</li>
</ul><h3>When you need a field guide</h3><p>Existing figure explanations have canonical locations; use these links instead of duplicating the same guide.</p><ul>
<li><a href="/nvme/figure-reference/command/en/#figure-b101">Base 2.4 Figure 101 · Completion Queue Entry: Status Field</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b104">Base 2.4 Figure 104 · Status Code – Command Specific Status Values</a></li>
<li><a href="/nvme/figure-reference/identify/en/#figure-b338">Base 2.4 Figure 338 · Identify – Identify Controller Data Structure, I/O Command Set Independent</a></li>
<li><a href="/nvme/figure-reference/init/en/#figure-b36">Base 2.4 Figure 36 · Offset 0h: CAP – Controller Capabilities</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b93">Base 2.4 Figure 93 · Common Command Format</a></li>
<li><a href="/nvme/figure-reference/command/en/#figure-b97">Base 2.4 Figure 97 · Common Completion Queue Entry Layout – Admin and All I/O Command Sets</a></li>
</ul><details><summary>Original documents used</summary><ul class="qr-sources">
<li>NVM Express Base Specification · Revision 2.4 · 2026-07-31<br><code>NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVM Command Set Specification · Revision 1.3 · 2026-07-31<br><code>NVM-Express-NVM-Command-Set-Specification-Revision-1.3-Ratified-2026.07.31.pdf</code></li>
<li>NVM Express NVMe over PCIe Transport Specification · Revision 1.4 · 2026-07-31<br><code>NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.4-Ratified-2026.07.31.pdf</code></li>
</ul></details></section>
</main>
<nav class="qr-top" aria-label="Bank and editions"><a href="#content">Skip to content</a><a href="/nvme/question-bank/en/">Question index</a><a href="/nvme/question-bank/recovery/zh-tw/">繁體中文</a><a href="/DOCS/nvme-question-bank/recovery.html">Chinese tutorial HTML</a></nav>
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
